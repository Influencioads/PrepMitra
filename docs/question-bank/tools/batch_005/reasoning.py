"""Builds batches/parts/BATCH_005_REAS.json: the 200 Reasoning Ability questions of BATCH_005.

Same method and helpers as tools/batch_004/reasoning.py, with new puzzle structures, noun sets and scenarios:
- puzzles and seating: the conditions are written once as (text, variables, test) triples; the text goes into the
  stimulus (or the question) and the test into an exhaustive backtracking search that must return exactly one
  arrangement. Every answer is then read off that arrangement;
- syllogisms: checked over every Venn-region model; inequalities: exhaustive integer assignments (with a growing
  value range as a cross-check);
- blood relations (explicit family tree), directions, coding (inferred rules are checked against a library of
  alternative simple rules), series, alphabet, number operations, ranking and input-output: recomputed in code;
  data sufficiency: each statement subset checked by enumerating models.
Verbal-reasoning items (assumptions, conclusions, cause and effect, critical reasoning) are hand-written; they carry
ai:independent-check only after a separate, fresh solver answered them blind and matched the key.
If any assertion fails, nothing is written. --draft prints quota gaps instead of asserting them.

    python tools/batch_005/reasoning.py        (run from docs/question-bank)
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
OUT = ROOT / "batches" / "parts" / "BATCH_005_REAS.json"
TODAY = "2026-11-05"
RA = "Reasoning Ability"
LETTERS = "ABCD"
FIRST_Q, FIRST_STIM = 805, 5001
BRUTE = ("script:brute-force-unique", "ai:author-solve")
RECOMP = ("script:recompute", "ai:author-solve")
VENN = ("script:all-venn-models", "ai:author-solve")
EXHAUST = ("script:exhaustive-integers", "ai:author-solve")
ENUM = ("script:enumerate-models", "ai:author-solve")
HAND = ("ai:author-solve", "ai:independent-check")  # only after a blind match by a fresh solver
SELF = ("ai:author-solve", "ai:self-recheck")
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
      why_others_wrong=None, seconds=60, stimulus=None, verified_by=SELF, tags=None):
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

# ---- L1 Basic set: seven persons facing north, each with a favourite vegetable (seats 1..7 from the left)
P = ["Bhavik", "Dhwani", "Garv", "Ipsita", "Mayank", "Sarthak", "Tamanna"]
VG = ["Beans", "Brinjal", "Cabbage", "Carrot", "Okra", "Peas", "Spinach"]
F_ = ["v" + p for p in P]
VV = P + F_
IXV = {v: i for i, v in enumerate(VV)}
seat_of = lambda v, x: next(v[IXV[p]] for p in P if v[IXV["v" + p]] == x)
conds = [
    ("Ipsita sits exactly in the middle of the row.", ("Ipsita",), lambda i: i == 4),
    ("Dhwani sits second to the right of Ipsita.", ("Dhwani", "Ipsita"), lambda d, i: d == i + 2),
    ("Mayank sits immediately to the right of Dhwani.", ("Mayank", "Dhwani"), lambda m, d: m == d + 1),
    ("The person who likes Carrot sits immediately to the left of Ipsita, and that person is Bhavik.",
     ("Bhavik", "vBhavik", "Ipsita"), lambda b, v, i: b == i - 1 and v == "Carrot"),
    ("Garv sits at one of the extreme ends of the row.", ("Garv",), lambda g: g in (1, 7)),
    ("Sarthak is not an immediate neighbour of Garv.", ("Sarthak", "Garv"), lambda s, g: abs(s - g) != 1),
    ("The person who likes Okra sits immediately to the right of Garv.", tuple(VV),
     lambda *v: seat_of(v, "Okra") == v[IXV["Garv"]] + 1),
    ("Ipsita likes Spinach, and Mayank likes Brinjal.", ("vIpsita", "vMayank"),
     lambda i, m: i == "Spinach" and m == "Brinjal"),
    ("The person who likes Beans sits immediately to the left of the person who likes Cabbage.", tuple(VV),
     lambda *v: seat_of(v, "Beans") == seat_of(v, "Cabbage") - 1),
]
L1 = unique(VV, {p: range(1, 8) for p in P} | {f: VG for f in F_}, conds, [P, F_])
at = {L1[p]: p for p in P}
veg = {p: L1["v" + p] for p in P}
assert [(at[i], veg[at[i]]) for i in range(1, 8)] == [
    ("Garv", "Peas"), ("Tamanna", "Okra"), ("Bhavik", "Carrot"), ("Ipsita", "Spinach"), ("Sarthak", "Beans"),
    ("Dhwani", "Cabbage"), ("Mayank", "Brinjal")]
ARR = "Left to right: " + ", ".join(f"{at[i]} ({veg[at[i]]})" for i in range(1, 8))
sid = stimulus("puzzle", "Seven persons in a row, with favourite vegetables",
               "Seven persons Bhavik, Dhwani, Garv, Ipsita, Mayank, Sarthak and Tamanna sit in a straight row, all "
               "facing north. Each of them likes a different vegetable among Beans, Brinjal, Cabbage, Carrot, Okra, "
               "Peas and Spinach. (Facing north, a person's right is towards the east end of the row.)", conds,
               "Step 1: Number the seats 1 to 7 from the left. Ipsita = 4, Dhwani = 6, Mayank = 7.\n"
               "Step 2: The Carrot-lover sits at seat 3 and is Bhavik.\n"
               "Step 3: Garv is at an end; seat 7 is Mayank's, so Garv = 1. Seats 2 and 5 remain for Sarthak and "
               "Tamanna; Sarthak cannot sit next to Garv, so Sarthak = 5 and Tamanna = 2.\n"
               "Step 4: Okra is immediately right of Garv: Tamanna. Ipsita Spinach, Mayank Brinjal.\n"
               "Step 5: Beans, Cabbage and Peas remain for Garv (1), Sarthak (5) and Dhwani (6). Beans is immediately "
               "left of Cabbage, so Sarthak Beans, Dhwani Cabbage and Garv Peas.\n\n"
               + table(["Seat", "Person", "Vegetable"], [(i, at[i], veg[at[i]]) for i in range(1, 8)]))
ans = next(p for p in P if veg[p] == "Cabbage")
assert ans == "Dhwani"
puzzle_q(sid, LIN, SGL, "Basic", "Who likes Cabbage?", ans, ["Sarthak", "Garv", "Mayank"],
         "Placing the last attributes with an adjacency clue",
         "After Spinach, Carrot, Okra and Brinjal are fixed, Beans, Cabbage and Peas remain for seats 1, 5 and 6. The "
         "only adjacent pair is 5–6, so Sarthak likes Beans and Dhwani Cabbage.",
         [ARR, "Free: Beans, Cabbage, Peas for seats 1, 5, 6", "Beans immediately left of Cabbage ⇒ seats 5, 6"],
         why_others_wrong="Sarthak likes Beans, Garv Peas and Mayank Brinjal.", seconds=45)
b_ = next(p for p in P if veg[p] == "Brinjal")
ans = at[L1[b_] - 3]
assert ans == "Ipsita"
puzzle_q(sid, LIN, SGL, "Basic", "Who sits third to the left of the person who likes Brinjal?", ans,
         ["Sarthak", "Bhavik", "Dhwani"], "Facing north: the left is towards the west",
         "Mayank likes Brinjal and sits at seat 7. Three seats to his left is seat 4: Ipsita.",
         [ARR, "Brinjal: Mayank (seat 7)", "7 − 3 = seat 4 ⇒ Ipsita"],
         why_others_wrong="Sarthak is second to his left, Bhavik fourth and Dhwani immediately to his left.", seconds=40)
beans = next(p for p in P if veg[p] == "Beans")
cnt = abs(L1["Garv"] - L1[beans]) - 1
assert cnt == 3
puzzle_q(sid, LIN, SGL, "Basic", "How many persons sit between Garv and the person who likes Beans?", num_word(cnt),
         ["Two", "Four", "Five"], "Count the seats strictly between two persons",
         "Garv is at seat 1 and Sarthak (Beans) at seat 5. Tamanna, Bhavik and Ipsita sit between them: three persons.",
         [ARR, "Garv 1, Beans = Sarthak 5", "Between: seats 2, 3, 4 ⇒ three"], natural=by_num, seconds=40)
stm = [("Tamanna – Okra", veg["Tamanna"] == "Okra"), ("Garv – Beans", veg["Garv"] == "Beans"),
       ("Bhavik – Spinach", veg["Bhavik"] == "Spinach"), ("Dhwani – Peas", veg["Dhwani"] == "Peas")]
t, f = one_true(stm)
puzzle_q(sid, LIN, SGL, "Basic", "Which of the following person – vegetable pairs is correct?", t, f,
         "Reading an attribute off the final arrangement", "From the table: " + ARR + ".", [ARR], seconds=40)

# ---- L2 Basic set: two rows of three facing each other. Row 1 faces south (its right is west), Row 2 faces
#      north (its right is east). Seat r*10 + c, c = 1..3 from west to east; (1, c) faces (2, c).
P = ["Kuhu", "Lakshay", "Nivedita", "Pranit", "Sanya", "Vishal"]
SEATS = [r * 10 + c for r in (1, 2) for c in range(1, 4)]
row_, col = lambda s: s // 10, lambda s: s % 10
RT = lambda s, k: s - k if row_(s) == 1 else s + k
opp = lambda s: s + 10 if row_(s) == 1 else s - 10
conds = [
    ("Pranit sits in the middle seat of the row that faces south.", ("Pranit",), lambda p: p == 12),
    ("Lakshay faces Pranit.", ("Lakshay", "Pranit"), lambda l, p: l == opp(p)),
    ("Sanya sits immediately to the left of Pranit.", ("Sanya", "Pranit"), lambda s, p: s == RT(p, -1)),
    ("Vishal sits immediately to the left of Lakshay.", ("Vishal", "Lakshay"), lambda v, l: v == RT(l, -1)),
    ("Nivedita faces Sanya.", ("Nivedita", "Sanya"), lambda n, s: n == opp(s)),
]
L2 = unique(P, {p: SEATS for p in P}, conds, [P])
at = {v: k for k, v in L2.items()}
assert [at[s] for s in SEATS] == ["Kuhu", "Pranit", "Sanya", "Vishal", "Lakshay", "Nivedita"]
ARR = ("Row 1 (facing south), west to east: " + ", ".join(at[10 + c] for c in range(1, 4)) +
       "; Row 2 (facing north), west to east: " + ", ".join(at[20 + c] for c in range(1, 4)))
sid = stimulus("puzzle", "Six persons in two short facing rows",
               "Six persons Kuhu, Lakshay, Nivedita, Pranit, Sanya and Vishal sit in two parallel rows of three seats "
               "each. The persons in Row 1 face south and the persons in Row 2 face north, so each person faces exactly "
               "one person of the other row. (Facing south, the right is towards the west; facing north, the right is "
               "towards the east.)", conds,
               "Number the seats 1 to 3 from west to east in both rows.\n"
               "Step 1: Pranit = Row 1 seat 2; Lakshay faces him: Row 2 seat 2.\n"
               "Step 2: Pranit faces south, so his left is east: Sanya = Row 1 seat 3. Lakshay faces north, so his left "
               "is west: Vishal = Row 2 seat 1.\n"
               "Step 3: Nivedita faces Sanya: Row 2 seat 3. Kuhu takes the last seat, Row 1 seat 1.\n\n"
               + table(["Seat", "Row 1 (facing south)", "Row 2 (facing north)"],
                       [(c, at[10 + c], at[20 + c]) for c in range(1, 4)]))
ans = at[opp(L2["Kuhu"])]
assert ans == "Vishal"
puzzle_q(sid, LIN, DBL, "Basic", "Who faces Kuhu?", ans, ["Lakshay", "Nivedita", "Sanya"],
         "Facing persons share the same seat number", "Kuhu is at Row 1 seat 1; facing her is Row 2 seat 1: Vishal.",
         [ARR, "Kuhu: Row 1 seat 1 ⇒ faces Row 2 seat 1 = Vishal"],
         why_others_wrong="Lakshay faces Pranit, Nivedita faces Sanya, and Sanya is in Kuhu's own row.", seconds=40)
ans = at[RT(L2["Vishal"], 2)]
assert ans == "Nivedita"
puzzle_q(sid, LIN, DBL, "Basic", "Who sits second to the right of Vishal?", ans, ["Lakshay", "Kuhu", "Sanya"],
         "Facing north: the right is east",
         "Vishal sits at Row 2 seat 1 and faces north, so his right is towards the east: Lakshay (seat 2), then "
         "Nivedita (seat 3).", [ARR, "Vishal faces north ⇒ right = east", "Seat 1 + 2 = seat 3 ⇒ Nivedita"],
         why_others_wrong="Lakshay is immediately to his right; Kuhu faces him; Sanya is in the other row.", seconds=40)
facer = at[opp(L2["Lakshay"])]
ans = at[RT(L2[facer], -1)]
assert (facer, ans) == ("Pranit", "Sanya")
puzzle_q(sid, LIN, DBL, "Basic", "Who sits immediately to the left of the person who faces Lakshay?", ans,
         ["Kuhu", "Nivedita", "Vishal"], "Facing south: the left is east",
         "Pranit faces Lakshay. Pranit faces south, so his left is towards the east: Row 1 seat 3, Sanya.",
         [ARR, "Person facing Lakshay = Pranit (Row 1 seat 2)", "Facing south ⇒ left = east ⇒ seat 3 = Sanya"],
         why_others_wrong="Kuhu is immediately to Pranit's right (west); Nivedita and Vishal are in Row 2.", seconds=45)
stm = [("Nivedita sits at an extreme end of Row 2", col(L2["Nivedita"]) in (1, 3)),
       ("Kuhu faces Lakshay", L2["Kuhu"] == opp(L2["Lakshay"])),
       ("Sanya sits in the same row as Vishal", row_(L2["Sanya"]) == row_(L2["Vishal"])),
       ("Pranit sits at an extreme end of Row 1", col(L2["Pranit"]) in (1, 3))]
t, f = one_true(stm)
puzzle_q(sid, LIN, DBL, "Basic", "Which of the following statements is true?", t, f,
         "Checking each statement against the arrangement",
         "Nivedita is at Row 2 seat 3, an end seat. Kuhu faces Vishal, Sanya is in Row 1 while Vishal is in Row 2, and "
         "Pranit is in the middle of Row 1.", [ARR], seconds=45)

# ---- L3 Intermediate (standalone): a row of unknown length
V = ["n", "Ketan", "Lipika", "Mohini"]
conds = [("Ketan sits ninth from the left end.", ("Ketan",), lambda k: k == 9),
         ("Lipika sits to the right of Ketan, and exactly as many persons sit between Ketan and Lipika as sit to the "
          "left of Ketan.", ("Ketan", "Lipika"), lambda k, l: l > k and l - k - 1 == k - 1),
         ("Mohini sits fourth to the right of Lipika and is seventh from the right end.", ("n", "Mohini", "Lipika"),
          lambda n, m, l: m == l + 4 and n - m + 1 == 7)]
sols = solve(V, {"n": range(3, 60)} | {p: range(1, 60) for p in V[1:]},
             [(vs, fn) for _, vs, fn in conds] + [(("n", "Mohini"), lambda n, m: m <= n)], [V[1:]])
assert len(sols) == 1 and sols[0]["n"] == 28
n_ = sols[0]["n"]
mcq(LIN, UNK, "Intermediate",
    "Some persons sit in a straight row, all facing north. The number of persons is not given.\n" + bullets(conds)
    + "\n\nHow many persons sit in the row?", str(n_), ["27", "29", "26"], "Turning a 'between' count into a position",
    "Eight persons sit to the left of Ketan (9th), so eight sit between Ketan and Lipika: Lipika is 9 + 8 + 1 = 18th. "
    "Mohini is 18 + 4 = 22nd from the left and 7th from the right, so the row has 22 + 7 − 1 = 28 persons.",
    ["Left of Ketan: 8 ⇒ 8 persons between Ketan and Lipika", "Lipika = 9 + 9 = 18th", "Mohini = 22nd",
     "Total = 22 + 7 − 1 = 28"],
    why_others_wrong="27 places Lipika 17th (eight seats instead of eight persons between); 29 forgets to subtract "
                     "Mohini once; 26 subtracts her twice.", natural=int, seconds=60, verified_by=BRUTE)

# ---- L4 Intermediate (standalone): seven persons, mixed facing (seats 1..7 from the west)
P = ["Anahita", "Bodhan", "Devyani", "Eknoor", "Gurdeep", "Haimanti", "Yug"]
F_ = ["f" + p for p in P]
VV = [x for p in P for x in (p, "f" + p)]
RS = lambda s, f, k: s + k if f == "N" else s - k
conds = [
    ("Devyani sits in the middle seat and faces south.", ("Devyani", "fDevyani"), lambda d, f: d == 4 and f == "S"),
    ("Yug sits immediately to the right of Devyani, and Bodhan sits immediately to her left.",
     ("Yug", "Bodhan", "Devyani", "fDevyani"), lambda y, b, d, f: y == RS(d, f, 1) and b == RS(d, f, -1)),
    ("Haimanti sits third to the right of Yug.", ("Haimanti", "Yug", "fYug"), lambda h, y, f: h == RS(y, f, 3)),
    ("Bodhan faces the same direction as Yug.", ("fBodhan", "fYug"), lambda a, b: a == b),
    ("Anahita sits immediately to the left of Yug, and Gurdeep sits second to the left of Yug.",
     ("Anahita", "Gurdeep", "Yug", "fYug"), lambda a, g, y, f: a == RS(y, f, -1) and g == RS(y, f, -2)),
    ("Eknoor faces south, and Anahita faces the direction opposite to Yug's.", ("fEknoor", "fAnahita", "fYug"),
     lambda e, a, y: e == "S" and a != y),
    ("Exactly three persons face south.", tuple(F_), lambda *f: f.count("S") == 3),
]
L4 = unique(VV, {p: range(1, 8) for p in P} | {f: "NS" for f in F_}, conds, [P])
at = {L4[p]: p for p in P}
fc = {p: L4["f" + p] for p in P}
FN = {"N": "north", "S": "south"}
assert [(at[i], fc[at[i]]) for i in range(1, 8)] == [
    ("Gurdeep", "N"), ("Anahita", "S"), ("Yug", "N"), ("Devyani", "S"), ("Bodhan", "N"), ("Haimanti", "N"),
    ("Eknoor", "S")]
ans = at[RS(L4["Eknoor"], fc["Eknoor"], 2)]
assert ans == "Bodhan"
mcq(LIN, SGL, "Intermediate",
    "Seven persons Anahita, Bodhan, Devyani, Eknoor, Gurdeep, Haimanti and Yug sit in a straight row. Some of them face "
    "north and the others face south. (Facing north, the right is east; facing south, the right is west.)\n"
    + bullets(conds) + "\n\nWho sits second to the right of Eknoor?", ans, ["Haimanti", "Devyani", "Yug"],
    "Fix each person's facing before reading 'right'",
    "Number the seats 1 to 7 from the west. Devyani = 4 facing south (right = west), so Yug = 3 and Bodhan = 5. "
    "Haimanti is third to Yug's right: if Yug faced south that would be seat 0, so Yug faces north and Haimanti = 6; "
    "Bodhan also faces north. Anahita (immediately left of Yug) = 2 and Gurdeep = 1, so Eknoor = 7. Eknoor, Devyani "
    "and Anahita (opposite to Yug) face south — already three — so Gurdeep and Haimanti face north. Eknoor faces south, "
    "so his right is west: seat 6 (Haimanti), then seat 5 (Bodhan).",
    ["Devyani 4 (S) ⇒ Yug 3, Bodhan 5", "Haimanti = Yug + 3 needs Yug facing north ⇒ Haimanti 6",
     "Anahita 2, Gurdeep 1, Eknoor 7", "South: Devyani, Anahita, Eknoor (three) ⇒ others north",
     "Eknoor (7) faces south ⇒ second to his right = seat 5 = Bodhan"],
    why_others_wrong="Haimanti is immediately to Eknoor's right; Devyani is third to his right; Yug is fourth.",
    seconds=90, verified_by=BRUTE)

# ---- L5 Intermediate (standalone): eight persons facing north, then two persons interchange seats
P = ["Raunak", "Shivangi", "Tarak", "Urmi", "Vatsal", "Waseem", "Xenia", "Zubair"]
conds = [("Raunak sits fourth from the left end.", ("Raunak",), lambda r: r == 4),
         ("Only two persons sit to the right of Shivangi.", ("Shivangi",), lambda s: s == 6),
         ("Xenia sits exactly midway between Raunak and Shivangi.", ("Xenia", "Raunak", "Shivangi"),
          lambda x, r, s: 2 * x == r + s),
         ("Vatsal sits second to the right of Shivangi, and Waseem is an immediate neighbour of Vatsal.",
          ("Vatsal", "Waseem", "Shivangi"), lambda v, w, s: v == s + 2 and abs(w - v) == 1),
         ("Zubair is an immediate neighbour of Raunak.", ("Zubair", "Raunak"), lambda z, r: abs(z - r) == 1),
         ("Tarak is not an immediate neighbour of Zubair.", ("Tarak", "Zubair"), lambda t, z: abs(t - z) != 1)]
L5 = unique(P, {p: range(1, 9) for p in P}, conds, [P])
at = {v: k for k, v in L5.items()}
assert [at[i] for i in range(1, 9)] == ["Tarak", "Urmi", "Zubair", "Raunak", "Xenia", "Shivangi", "Waseem", "Vatsal"]
new = dict(L5)
new["Zubair"], new["Vatsal"] = L5["Vatsal"], L5["Zubair"]
cnt = abs(new["Zubair"] - new["Xenia"]) - 1
assert cnt == 2
mcq(LIN, SGL, "Intermediate",
    "Eight persons Raunak, Shivangi, Tarak, Urmi, Vatsal, Waseem, Xenia and Zubair sit in a straight row, all facing "
    "north.\n" + bullets(conds) + "\n\nIf Zubair and Vatsal interchange their seats, how many persons will then sit "
    "between Zubair and Xenia?", num_word(cnt), ["One", "Three", "Four"], "Fix the row, then apply the interchange",
    "Raunak = 4 and Shivangi = 6, so Xenia (midway) = 5. Vatsal = 8 and Waseem = 7. Zubair is next to Raunak: seat 3 "
    "(seat 5 is taken). Tarak cannot sit next to Zubair, so Tarak = 1 and Urmi = 2. After the interchange Zubair is at "
    "seat 8 and Xenia at seat 5, with Shivangi and Waseem between them: two persons.",
    ["Raunak 4, Shivangi 6 ⇒ Xenia 5", "Vatsal 8, Waseem 7", "Zubair 3; Tarak 1, Urmi 2",
     "Interchange: Zubair 8, Vatsal 3", "Between 5 and 8: seats 6, 7 ⇒ two"],
    why_others_wrong="One is the count before the interchange; Three and Four count one or both of the end persons.",
    natural=by_num, seconds=75, verified_by=BRUTE)

# ---- L6 Advanced set: two rows of five seats facing each other, eight persons, one vacant seat in each row.
#      Row 1 faces south (right = west = lower column), Row 2 faces north (right = east). Seat r*10 + c.
P = ["Bhagya", "Darshit", "Hritik", "Jhilmil", "Kalindi", "Nirmay", "Rudra", "Tejasvi"]
SEATS = [r * 10 + c for r in (1, 2) for c in range(1, 6)]
vac = lambda v, r: [s for s in SEATS if row_(s) == r and s not in v]
conds = [
    ("Kalindi faces south and sits in the middle seat of her row; Nirmay faces Kalindi.", ("Kalindi", "Nirmay"),
     lambda k, n: k == 13 and n == opp(k)),
    ("Bhagya sits immediately to the left of Kalindi, and the seat facing Bhagya is vacant.", tuple(P),
     lambda *v: v[0] == RT(v[4], -1) and opp(v[0]) not in v),
    ("Darshit sits second to the left of the vacant seat in his row.", tuple(P),
     lambda *v: len(vac(v, 1)) == 1 and len(vac(v, 2)) == 1 and RT(vac(v, row_(v[1]))[0], -2) == v[1]),
    ("Hritik sits third to the right of Bhagya.", ("Hritik", "Bhagya"), lambda h, b: h == RT(b, 3)),
    ("Rudra sits at an extreme end of a row.", ("Rudra",), lambda r: col(r) in (1, 5)),
    ("Jhilmil faces north and faces Rudra.", ("Jhilmil", "Rudra"), lambda j, r: row_(j) == 2 and j == opp(r)),
]
sols = solve(P, {p: SEATS for p in P}, [(vs, fn) for _, vs, fn in conds], [P])
sols = [s_ for s_ in sols if all(len(vac(list(s_.values()), r)) == 1 for r in (1, 2))]
assert len(sols) == 1, sols
L6 = sols[0]
at = {v: k for k, v in L6.items()}
assert [at.get(s) for s in SEATS] == ["Hritik", None, "Kalindi", "Bhagya", "Rudra",
                                      "Tejasvi", "Darshit", "Nirmay", None, "Jhilmil"]
cellr = lambda s: at.get(s, "vacant")
ARR = ("Row 1 (facing south), west to east: " + ", ".join(cellr(10 + c) for c in range(1, 6)) +
       "; Row 2 (facing north), west to east: " + ", ".join(cellr(20 + c) for c in range(1, 6)))
sid = stimulus("puzzle", "Eight persons on ten facing seats, one vacant seat per row",
               "Ten seats are arranged in two parallel rows of five, numbered 1 to 5 from west to east in each row. "
               "The persons in Row 1 face south and those in Row 2 face north, so seat k of Row 1 faces seat k of "
               "Row 2. Eight persons Bhagya, Darshit, Hritik, Jhilmil, Kalindi, Nirmay, Rudra and Tejasvi sit on eight "
               "of the seats, and exactly one seat in each row is vacant. (Facing south, the right is west; facing "
               "north, the right is east. Vacant seats are counted as seats.)", conds,
               "Step 1: Kalindi = Row 1 seat 3 (facing south, so her right is west and her left east); Nirmay = "
               "Row 2 seat 3.\n"
               "Step 2: Bhagya is immediately to Kalindi's left: Row 1 seat 4, and the seat facing him, Row 2 seat 4, is "
               "vacant. Hritik is third to Bhagya's right (west): Row 1 seat 1.\n"
               "Step 3: Jhilmil is in Row 2 and faces Rudra, so Rudra is in Row 1, at an end: seat 5 (seat 1 is "
               "Hritik's). Jhilmil = Row 2 seat 5.\n"
               "Step 4: Row 2 already has its vacant seat (4), so Tejasvi and Darshit fill Row 2 seats 1 and 2 and Row 1 "
               "seat 2 is vacant. Darshit is second to the left of his row's vacant seat: in Row 2 (facing north, left = "
               "west) that is seat 2. (In Row 1 the seat second to the left of vacant seat 2 would be Bhagya's seat 4.) "
               "So Darshit = Row 2 seat 2 and Tejasvi = Row 2 seat 1.\n\n"
               + table(["Seat", "Row 1 (facing south)", "Row 2 (facing north)"],
                       [(c, cellr(10 + c), cellr(20 + c)) for c in range(1, 6)]))
ans = at[opp(next(s_ for s_ in SEATS if row_(s_) == 1 and s_ not in at))]
assert ans == "Darshit"
puzzle_q(sid, LIN, DBL, "Advanced", "Who faces the vacant seat of Row 1?", ans, ["Tejasvi", "Nirmay", "Bhagya"],
         "Pin the two vacant seats first",
         "Row 2 seat 4 is vacant (it faces Bhagya), so Row 2 cannot hold another vacancy; Row 1 seat 2 is the other "
         "vacant seat, and Row 2 seat 2 is Darshit's.", [ARR, "Vacant: Row 1 seat 2 and Row 2 seat 4",
                                                         "Row 1 seat 2 faces Row 2 seat 2 = Darshit"],
         why_others_wrong="Tejasvi faces Hritik, Nirmay faces Kalindi, and Bhagya faces the vacant seat of Row 2.",
         seconds=90)
ans = at[RT(L6["Nirmay"], 2)]
assert ans == "Jhilmil"
puzzle_q(sid, LIN, DBL, "Advanced", "Who sits in the second seat to the right of Nirmay?", ans,
         ["Darshit", "Tejasvi", "Rudra"], "Vacant seats are counted as seats",
         "Nirmay (Row 2 seat 3) faces north, so his right is east: seat 4 (vacant), then seat 5 (Jhilmil).",
         [ARR, "Nirmay faces north ⇒ right = east", "Seat 3 + 2 = seat 5 ⇒ Jhilmil"],
         why_others_wrong="Darshit and Tejasvi are to his left; Rudra is in the other row.", seconds=80)
btw = [at[s_] for s_ in range(L6["Hritik"] + 1, L6["Bhagya"]) if s_ in at]
assert btw == ["Kalindi"]
puzzle_q(sid, LIN, DBL, "Advanced", "How many persons sit between Hritik and Bhagya?", num_word(len(btw)),
         ["Two", "None", "Three"], "Count persons, not seats",
         "Hritik is at Row 1 seat 1 and Bhagya at seat 4. Seats 2 and 3 lie between them; seat 2 is vacant, so only "
         "Kalindi sits between them.", [ARR, "Seats between 1 and 4: 2 (vacant), 3 (Kalindi) ⇒ one person"],
         why_others_wrong="Two counts the vacant seat as a person; None and Three miscount the seats.", natural=by_num,
         seconds=80)
ends = (at[21], at[25])
assert ends == ("Tejasvi", "Jhilmil")
puzzle_q(sid, LIN, DBL, "Advanced", "Which two persons sit at the two extreme ends of Row 2?", "Tejasvi and Jhilmil",
         ["Darshit and Jhilmil", "Hritik and Rudra", "Tejasvi and Nirmay"], "Ends of the north-facing row",
         "Row 2 from west to east: Tejasvi, Darshit, Nirmay, vacant, Jhilmil. The end seats 1 and 5 hold Tejasvi and "
         "Jhilmil.", [ARR], why_others_wrong="Hritik and Rudra are the ends of Row 1; Darshit and Nirmay sit in middle "
                                             "seats of Row 2.", seconds=75)
stm = [("Rudra faces Jhilmil", L6["Jhilmil"] == opp(L6["Rudra"])),
       ("Tejasvi sits immediately to the right of Darshit", L6["Tejasvi"] == RT(L6["Darshit"], 1)),
       ("Hritik faces a vacant seat", opp(L6["Hritik"]) not in at),
       ("Bhagya sits second to the right of Rudra", L6["Bhagya"] == RT(L6["Rudra"], 2))]
t, f = one_true(stm)
puzzle_q(sid, LIN, DBL, "Advanced", "Which of the following statements is true?", t, f,
         "Checking each statement against the arrangement",
         "Rudra (Row 1 seat 5) and Jhilmil (Row 2 seat 5) face each other. Tejasvi is to Darshit's left (west), Hritik "
         "faces Tejasvi (not a vacant seat), and Rudra faces south, so Bhagya (seat 4) is immediately to his right and "
         "Kalindi (seat 3) second to his right.", [ARR], seconds=80)

# ================================================================================================ CIRCULAR SEATING
CIR = "Circular Seating Arrangement"
CEN, INOUT, SQR = "Facing centre", "Facing inside and outside", "Square and rectangular tables"
cq = lambda sid_, sub, diff: (lambda text, correct, wrongs, concept, expl, steps, **kw: puzzle_q(
    sid_, CIR, sub, diff, text, correct, wrongs, concept, expl, steps, **kw))

# ---- C1 Basic set: eight persons facing the centre (seats 0..7 anticlockwise; right = +1); Aadhya fixed at 0
P = ["Aadhya", "Bhrigu", "Cauvery", "Jagrav", "Lohith", "Mahika", "Ranveer", "Sukriti"]
N = 8
conds = [("Mahika sits opposite Aadhya.", ("Mahika", "Aadhya"), lambda m, a: m == (a + 4) % N),
         ("Lohith sits immediately to the right of Aadhya, and Sukriti sits second to the right of Aadhya.",
          ("Lohith", "Sukriti", "Aadhya"), lambda l, s, a: l == (a + 1) % N and s == (a + 2) % N),
         ("Bhrigu sits immediately to the left of Mahika.", ("Bhrigu", "Mahika"), lambda b, m: b == (m - 1) % N),
         ("Cauvery sits second to the left of Aadhya.", ("Cauvery", "Aadhya"), lambda c, a: c == (a - 2) % N),
         ("Jagrav is not an immediate neighbour of Aadhya.", ("Jagrav", "Aadhya"),
          lambda j, a: (j - a) % N not in (1, N - 1))]
C1 = unique(P, {"Aadhya": [0]} | {p: range(N) for p in P if p != "Aadhya"}, conds, [P])
at = {v: k for k, v in C1.items()}
assert [at[i] for i in range(N)] == ["Aadhya", "Lohith", "Sukriti", "Bhrigu", "Mahika", "Jagrav", "Cauvery", "Ranveer"]
ARR = "Anticlockwise from Aadhya (each person's right is the next seat anticlockwise): " + ", ".join(
    at[i] for i in range(N))
sid = stimulus("puzzle", "Eight persons around a round table",
               "Eight persons Aadhya, Bhrigu, Cauvery, Jagrav, Lohith, Mahika, Ranveer and Sukriti sit around a "
               "circular table, equally spaced and all facing the centre. (Facing the centre, a person's right is "
               "anticlockwise.)", conds,
               "Put Aadhya at seat 0 and number the seats anticlockwise. Mahika = 4. Lohith = 1, Sukriti = 2. Bhrigu "
               "(immediately left of Mahika) = 3. Cauvery (second to Aadhya's left) = 6. Seats 5 and 7 remain for "
               "Jagrav and Ranveer; seat 7 is next to Aadhya, so Jagrav = 5 and Ranveer = 7.\n\n" + ARR)
Q = cq(sid, CEN, "Basic")
ans = at[(C1["Cauvery"] - 3) % N]
assert ans == "Bhrigu"
Q("Who sits third to the left of Cauvery?", ans, ["Mahika", "Sukriti", "Jagrav"], "Facing the centre: left = clockwise",
  "Cauvery is at seat 6; moving clockwise: Jagrav (5), Mahika (4), Bhrigu (3).",
  [ARR, "6 − 3 = seat 3 ⇒ Bhrigu"], why_others_wrong="Jagrav and Mahika are first and second to her left; Sukriti is "
                                                     "fourth.", seconds=40)
cnt = (C1["Jagrav"] - C1["Lohith"]) % N - 1
assert cnt == 3
Q("How many persons sit between Lohith and Jagrav when counted to the right of Lohith?", num_word(cnt),
  ["Two", "Four", "Five"], "Count in one direction only",
  "Lohith is at seat 1; going to his right (anticlockwise): Sukriti (2), Bhrigu (3), Mahika (4), then Jagrav (5). "
  "Three persons sit between them.", [ARR, "Seats 2, 3, 4 lie between ⇒ three"],
  why_others_wrong="Two and Four are off by one; Five counts Lohith and Jagrav themselves.",
  natural=by_num, seconds=40)
ans = at[(C1["Sukriti"] + 4) % N]
assert ans == "Cauvery"
Q("Who sits opposite Sukriti?", ans, ["Ranveer", "Jagrav", "Mahika"], "Opposite = four seats away in a circle of eight",
  "Sukriti is at seat 2; the seat opposite is 2 + 4 = 6: Cauvery.", [ARR, "2 + 4 = seat 6 ⇒ Cauvery"],
  why_others_wrong="Ranveer is opposite Bhrigu, Jagrav opposite Lohith and Mahika opposite Aadhya.", seconds=35)

# ---- C2 Intermediate set: ten persons facing the centre (right = +1); Agastya fixed at 0
P = ["Agastya", "Binal", "Chanchal", "Dhairya", "Ipshita", "Kanishk", "Nandan", "Pavani", "Shaurya", "Vanshika"]
N = 10
nb = lambda a, b: (a - b) % N in (1, N - 1)
conds = [("Nandan sits opposite Agastya.", ("Nandan", "Agastya"), lambda n, a: n == (a + 5) % N),
         ("Dhairya sits second to the right of Agastya.", ("Dhairya", "Agastya"), lambda d, a: d == (a + 2) % N),
         ("Only one person sits between Dhairya and Binal when counted to the right of Dhairya, and that person is "
          "Shaurya.", ("Binal", "Shaurya", "Dhairya"), lambda b, s, d: b == (d + 2) % N and s == (d + 1) % N),
         ("Chanchal sits third to the right of Nandan.", ("Chanchal", "Nandan"), lambda c, n: c == (n + 3) % N),
         ("Vanshika is an immediate neighbour of Nandan.", ("Vanshika", "Nandan"), lambda v, n: nb(v, n)),
         ("Kanishk sits immediately to the left of Chanchal.", ("Kanishk", "Chanchal"), lambda k, c: k == (c - 1) % N),
         ("Ipshita sits immediately to the left of Agastya.", ("Ipshita", "Agastya"), lambda i, a: i == (a - 1) % N)]
C2 = unique(P, {"Agastya": [0]} | {p: range(N) for p in P if p != "Agastya"}, conds, [P])
at = {v: k for k, v in C2.items()}
assert [at[i] for i in range(N)] == ["Agastya", "Pavani", "Dhairya", "Shaurya", "Binal", "Nandan", "Vanshika",
                                     "Kanishk", "Chanchal", "Ipshita"]
ARR = "Anticlockwise from Agastya: " + ", ".join(at[i] for i in range(N))
sid = stimulus("puzzle", "Ten persons around a round table",
               "Ten persons Agastya, Binal, Chanchal, Dhairya, Ipshita, Kanishk, Nandan, Pavani, Shaurya and Vanshika "
               "sit around a circular table, equally spaced and all facing the centre. (Facing the centre, a person's "
               "right is anticlockwise.)", conds,
               "Put Agastya at seat 0 and number the seats 0 to 9 anticlockwise. Nandan = 5. Dhairya = 2, Shaurya = 3, "
               "Binal = 4. Chanchal = 5 + 3 = 8 and Kanishk = 7. Nandan's neighbours are seats 4 (Binal) and 6, so "
               "Vanshika = 6. Ipshita = 9, and Pavani takes the last seat, 1.\n\n" + ARR)
Q = cq(sid, CEN, "Intermediate")
ans = at[(C2["Kanishk"] - 4) % N]
assert ans == "Shaurya"
Q("Who sits fourth to the left of Kanishk?", ans, ["Binal", "Dhairya", "Nandan"], "Left of a centre-facing person = "
  "clockwise", "Kanishk is at seat 7; four seats clockwise: Vanshika (6), Nandan (5), Binal (4), Shaurya (3).",
  [ARR, "7 − 4 = seat 3 ⇒ Shaurya"], why_others_wrong="Nandan is second, Binal third and Dhairya fifth to his left.",
  seconds=55)
ans = at[(C2["Shaurya"] + 5) % N]
assert ans == "Chanchal"
Q("Who sits opposite Shaurya?", ans, ["Kanishk", "Ipshita", "Vanshika"], "Opposite = five seats away in a circle of "
  "ten", "Shaurya is at seat 3; opposite is seat 8: Chanchal.", [ARR, "3 + 5 = 8 ⇒ Chanchal"],
  why_others_wrong="Kanishk is opposite Dhairya, Ipshita opposite Binal and Vanshika opposite Pavani.", seconds=50)
cnt = (C2["Ipshita"] - C2["Binal"]) % N - 1
assert cnt == 4
Q("How many persons sit between Ipshita and Binal when counted to the left of Ipshita?", num_word(cnt),
  ["Three", "Five", "Six"], "Count in the stated direction",
  "Ipshita is at seat 9; to her left (clockwise) come Chanchal (8), Kanishk (7), Vanshika (6) and Nandan (5), then "
  "Binal (4). Four persons sit between them.", [ARR, "Seats 8, 7, 6, 5 ⇒ four"],
  why_others_wrong="Three and Five are off by one; Six counts Ipshita and Binal themselves.",
  natural=by_num, seconds=55)
mid = at[(C2["Kanishk"] + C2["Nandan"]) // 2]
assert mid == "Vanshika"
Q("Who sits exactly between Kanishk and Nandan?", mid, ["Chanchal", "Binal", "Pavani"],
  "One seat separates two persons two places apart",
  "Kanishk (7) and Nandan (5) are two seats apart; seat 6 between them is Vanshika's.", [ARR, "Seat 6 ⇒ Vanshika"],
  why_others_wrong="Chanchal and Binal are the outer neighbours of Kanishk and Nandan; Pavani sits across the table.",
  seconds=50)

# ---- C3 Intermediate set: square table; corners (even seats) face outside, middles (odd seats) face the centre.
#      Seats 0..7 anticlockwise. Facing the centre: right = +1; facing outside: right = −1.
P = ["Avni", "Chirantan", "Gulabo", "Jaiveer", "Lavleen", "Prithvi", "Tanuja", "Yashpal"]
N = 8
RTs = lambda s, k: (s + k) % N if s % 2 else (s - k) % N
conds = [("Avni sits at a corner of the table.", ("Avni",), lambda a: a % 2 == 0),
         ("Prithvi sits immediately to the left of Avni, and Yashpal sits opposite Avni.",
          ("Prithvi", "Yashpal", "Avni"), lambda p, y, a: p == RTs(a, -1) and y == (a + 4) % N),
         ("Gulabo sits second to the right of Prithvi.", ("Gulabo", "Prithvi"), lambda g, p: g == RTs(p, 2)),
         ("Tanuja sits immediately to the left of Gulabo.", ("Tanuja", "Gulabo"), lambda t, g: t == RTs(g, -1)),
         ("Chirantan sits immediately to the left of Yashpal.", ("Chirantan", "Yashpal"),
          lambda c, y: c == RTs(y, -1)),
         ("Jaiveer sits at the middle of a side.", ("Jaiveer",), lambda j: j % 2 == 1)]
C3 = unique(P, {"Avni": [0]} | {p: range(N) for p in P if p != "Avni"}, conds, [P])
at = {v: k for k, v in C3.items()}
assert [at[i] for i in range(N)] == ["Avni", "Prithvi", "Tanuja", "Gulabo", "Yashpal", "Chirantan", "Lavleen",
                                     "Jaiveer"]
KIND = lambda i: "corner, facing outside" if i % 2 == 0 else "side, facing the centre"
ARR = "Anticlockwise from Avni: " + ", ".join(f"{at[i]} ({KIND(i)})" for i in range(N))
sid = stimulus("puzzle", "Square table: corners facing out, sides facing in",
               "Eight persons Avni, Chirantan, Gulabo, Jaiveer, Lavleen, Prithvi, Tanuja and Yashpal sit around a square "
               "table. Four of them sit at the four corners and face outside (away from the centre); the other four "
               "sit at the middle of the four sides and face the centre. (Facing the centre, the right is "
               "anticlockwise; facing outside, the right is clockwise.)", conds,
               "Number the seats 0 to 7 anticlockwise with Avni's corner as 0; corners are the even seats.\n"
               "Step 1: Avni faces outside, so her left is anticlockwise: Prithvi = 1. Yashpal = 4.\n"
               "Step 2: Prithvi faces the centre, so his right is anticlockwise: Gulabo = 3. Gulabo faces the centre, so "
               "her left is clockwise: Tanuja = 2.\n"
               "Step 3: Yashpal (corner, facing outside) has his left anticlockwise: Chirantan = 5.\n"
               "Step 4: Seats 6 (corner) and 7 (side) remain; Jaiveer sits at a side: Jaiveer = 7, Lavleen = 6.\n\n"
               + ARR)
Q = cq(sid, SQR, "Intermediate")
ans = at[RTs(C3["Lavleen"], 2)]
assert ans == "Yashpal"
Q("Who sits second to the right of Lavleen?", ans, ["Avni", "Chirantan", "Jaiveer"],
  "A corner person faces outside, so the right is clockwise",
  "Lavleen sits at corner seat 6 and faces outside, so her right is clockwise: Chirantan (5), then Yashpal (4).",
  [ARR, "Lavleen faces outside ⇒ right = clockwise", "6 − 2 = seat 4 ⇒ Yashpal"],
  why_others_wrong="Chirantan is immediately to her right; Jaiveer is immediately to her left and Avni second to her "
                   "left.", seconds=60)
ans = at[(C3["Gulabo"] + 4) % N]
assert ans == "Jaiveer"
Q("Who sits opposite Gulabo?", ans, ["Lavleen", "Chirantan", "Prithvi"], "Opposite seats differ by four",
  "Gulabo sits at seat 3 (middle of a side); opposite is seat 7: Jaiveer.", [ARR, "3 + 4 = 7 ⇒ Jaiveer"],
  why_others_wrong="Lavleen is opposite Tanuja, Chirantan opposite Prithvi, and Prithvi sits on the next side.",
  seconds=50)
corners = sorted(at[i] for i in range(0, N, 2) if at[i] != "Avni")
assert corners == ["Lavleen", "Tanuja", "Yashpal"]
Q("Apart from Avni, which three persons sit at the corners of the table?", "Lavleen, Tanuja and Yashpal",
  ["Gulabo, Tanuja and Yashpal", "Chirantan, Lavleen and Yashpal", "Jaiveer, Lavleen and Tanuja"],
  "Corners alternate with side seats",
  "The corners are seats 0, 2, 4 and 6: Avni, Tanuja, Yashpal and Lavleen.", [ARR],
  why_others_wrong="Gulabo, Chirantan and Jaiveer sit at the middle of sides and face the centre.", seconds=55)

# ---- C4 Advanced set: eight chairs, seven persons, one vacant chair, mixed facing; Abhimanyu fixed at 0
P = ["Abhimanyu", "Chitrangada", "Devraj", "Gauhar", "Malti", "Parikshit", "Satyam"]
N = 8
F_ = ["f" + p for p in P]
VV = [x for p in P for x in (p, "f" + p)]
RF = lambda s, f, k: (s + k) % N if f == "C" else (s - k) % N
conds = [
    ("Abhimanyu faces the centre, and the vacant chair is second to his right.", tuple(P) + ("fAbhimanyu",),
     lambda *v: v[-1] == "C" and RF(v[0], "C", 2) not in v[:-1]),
    ("Satyam sits opposite Abhimanyu.", ("Satyam", "Abhimanyu"), lambda s, a: s == (a + 4) % N),
    ("Devraj sits between the vacant chair and Satyam, next to both.", ("Devraj", "Satyam", "Abhimanyu"),
     lambda d, s, a: d == (s - 1) % N and (a + 2) % N == (d - 1) % N),
    ("Gauhar sits immediately to the left of Satyam, and Parikshit sits immediately to the right of Gauhar.",
     ("Gauhar", "Satyam", "fSatyam", "Parikshit", "fGauhar"),
     lambda g, s, fs, p, fg: g == RF(s, fs, -1) and p == RF(g, fg, 1)),
    ("Devraj sits second to the left of Malti.", ("Devraj", "Malti", "fMalti"), lambda d, m, f: d == RF(m, f, -2)),
    ("Parikshit faces the same direction as Abhimanyu, and Chitrangada faces the direction opposite to Parikshit's.",
     ("fParikshit", "fAbhimanyu", "fChitrangada"), lambda p, a, c: p == a and c != p),
    ("Exactly three persons face outside.", tuple(F_), lambda *f: f.count("O") == 3),
]
C4 = unique(VV, {"Abhimanyu": [0]} | {p: range(N) for p in P if p != "Abhimanyu"} | {f: "CO" for f in F_}, conds, [P])
at = {C4[p]: p for p in P}
fc = {p: C4["f" + p] for p in P}
FCN = {"C": "facing the centre", "O": "facing outside"}
assert [(at.get(i), fc.get(at.get(i))) for i in range(N)] == [
    ("Abhimanyu", "C"), ("Malti", "O"), (None, None), ("Devraj", "C"), ("Satyam", "O"), ("Gauhar", "C"),
    ("Parikshit", "C"), ("Chitrangada", "O")]
ARR = "Anticlockwise from Abhimanyu: " + ", ".join(
    f"{at[i]} ({FCN[fc[at[i]]]})" if i in at else "vacant chair" for i in range(N))
sid = stimulus("puzzle", "Seven persons, one empty chair, facing in or out",
               "Eight chairs are placed around a circular table, equally spaced. Seven persons Abhimanyu, Chitrangada, "
               "Devraj, Gauhar, Malti, Parikshit and Satyam sit on seven of them; one chair is vacant. Some of the "
               "persons face the centre and the others face outside. (Facing the centre, the right is anticlockwise; "
               "facing outside, the right is clockwise.) Positions such as 'second to the right' count chairs, "
               "including the vacant one.", conds,
               "Put Abhimanyu at chair 0 and number the chairs anticlockwise.\n"
               "Step 1: Abhimanyu faces the centre, so chair 2 is vacant. Satyam = 4, and Devraj (between the vacant "
               "chair and Satyam) = 3.\n"
               "Step 2: If Satyam faced the centre, his left (clockwise) would be chair 3, Devraj's; so Satyam faces "
               "outside and Gauhar = 5. If Gauhar faced outside, his right would be chair 4 (Satyam); so Gauhar faces "
               "the centre and Parikshit = 6. Chairs 1 and 7 remain.\n"
               "Step 3: Devraj is second to Malti's left. From chair 1 facing outside (left = anticlockwise) that is "
               "chair 3 — it fits; from chair 7 either way it is chair 1 or chair 5 — neither is Devraj's. So Malti = 1 "
               "and faces outside, and Chitrangada = 7.\n"
               "Step 4: Parikshit faces the centre like Abhimanyu, so Chitrangada faces outside. Outside: Satyam, "
               "Malti, Chitrangada — three — so Devraj faces the centre.\n\n" + ARR)
Q = cq(sid, INOUT, "Advanced")
ans = at[RF(C4["Chitrangada"], fc["Chitrangada"], 3)]
assert ans == "Satyam"
Q("Who sits third to the right of Chitrangada?", ans, ["Gauhar", "Abhimanyu", "Devraj"],
  "Facing outside: the right is clockwise",
  "Chitrangada (chair 7) faces outside, so her right is clockwise: Parikshit (6), Gauhar (5), Satyam (4).",
  [ARR, "7 − 3 = chair 4 ⇒ Satyam"], why_others_wrong="Gauhar is second to her right; Abhimanyu and Devraj lie to her "
                                                      "left.", seconds=90)
cnt = sum(1 for p in P if fc[p] == "C")
assert cnt == 4
Q("How many persons face the centre?", num_word(cnt), ["Three", "Five", "Two"], "Decide each facing from a clue",
  "Abhimanyu, Gauhar, Parikshit and Devraj face the centre; Satyam, Malti and Chitrangada face outside.",
  [ARR, "Outside: Satyam, Malti, Chitrangada (exactly three)", "Centre: the other four"], natural=by_num, seconds=85)
ans = at[(2 + 4) % N]
assert ans == "Parikshit"
Q("Who sits opposite the vacant chair?", ans, ["Gauhar", "Chitrangada", "Satyam"], "Opposite = four chairs away",
  "The vacant chair is chair 2; opposite it is chair 6: Parikshit.", [ARR, "2 + 4 = 6 ⇒ Parikshit"],
  why_others_wrong="Gauhar is opposite Malti, Chitrangada opposite Devraj and Satyam opposite Abhimanyu.", seconds=80)

# ---- C5 Advanced set: six persons facing the centre with their runs; Inder fixed at 0
P = ["Hrishikesh", "Inder", "Jasmit", "Kaveri", "Lalitesh", "Nayantara"]
RUNS = [12, 18, 25, 31, 40, 47]
N = 6
R_ = ["r" + p for p in P]
VV = P + R_
IXV = {v: i for i, v in enumerate(VV)}
seat_r = lambda v, r: next(v[IXV[p]] for p in P if v[IXV["r" + p]] == r)
run_at = lambda v, s: next(v[IXV["r" + p]] for p in P if v[IXV[p]] == s)
conds = [
    ("The person who scored 47 runs sits opposite the person who scored 12 runs.", tuple(VV),
     lambda *v: seat_r(v, 47) == (seat_r(v, 12) + 3) % N),
    ("Inder scored 31 runs and sits immediately to the left of Kaveri, who scored the fewest runs.",
     ("Inder", "Kaveri", "rInder", "rKaveri"), lambda i, k, ri, rk: i == (k - 1) % N and ri == 31 and rk == 12),
    ("Hrishikesh sits opposite Inder.", ("Hrishikesh", "Inder"), lambda h, i: h == (i + 3) % N),
    ("The runs of Hrishikesh's two immediate neighbours add up to 87.", tuple(VV),
     lambda *v: run_at(v, (v[IXV["Hrishikesh"]] + 1) % N) + run_at(v, (v[IXV["Hrishikesh"]] - 1) % N) == 87),
    ("Jasmit scored more runs than Nayantara, and Lalitesh scored fewer runs than Hrishikesh.",
     ("rJasmit", "rNayantara", "rLalitesh", "rHrishikesh"), lambda j, n, l, h: j > n and l < h),
]
C5 = unique(VV, {"Inder": [0]} | {p: range(N) for p in P if p != "Inder"} | {r: RUNS for r in R_}, conds, [P, R_])
at = {C5[p]: p for p in P}
rn = {p: C5["r" + p] for p in P}
assert [(at[i], rn[at[i]]) for i in range(N)] == [("Inder", 31), ("Kaveri", 12), ("Nayantara", 40),
                                                  ("Hrishikesh", 25), ("Jasmit", 47), ("Lalitesh", 18)]
ARR = "Anticlockwise from Inder: " + ", ".join(f"{at[i]} ({rn[at[i]]})" for i in range(N))
sid = stimulus("puzzle", "Six cricketers around a table, with their runs",
               "Six persons Hrishikesh, Inder, Jasmit, Kaveri, Lalitesh and Nayantara sit around a circular table, "
               "equally spaced and all facing the centre. In a match each of them scored a different number of runs "
               "among 12, 18, 25, 31, 40 and 47. (Facing the centre, a person's right is anticlockwise.)", conds,
               "Put Inder at seat 0 and number the seats anticlockwise.\n"
               "Step 1: Inder is immediately to Kaveri's left (clockwise of her), so Kaveri = 1, with 12 runs; Inder has "
               "31. Hrishikesh = 3.\n"
               "Step 2: The 47-scorer sits opposite Kaveri: seat 4.\n"
               "Step 3: Hrishikesh's neighbours are seats 2 and 4. Seat 4 has 47, so seat 2 has 87 − 47 = 40.\n"
               "Step 4: Jasmit, Lalitesh and Nayantara take seats 2, 4 and 5. Lalitesh scored fewer than Hrishikesh, "
               "and Hrishikesh cannot have 40 or 47 (they are at seats 2 and 4), so Lalitesh cannot hold 40 or 47 either: "
               "Lalitesh = seat 5. Jasmit > Nayantara gives Jasmit 47 (seat 4) and Nayantara 40 (seat 2). Hrishikesh and "
               "Lalitesh share 18 and 25; Lalitesh has fewer: Lalitesh 18, Hrishikesh 25.\n\n"
               + table(["Seat", "Person", "Runs"], [(i, at[i], rn[at[i]]) for i in range(N)]))
Q = cq(sid, CEN, "Advanced")
ans = rn[at[(C5["Lalitesh"] + 1) % N]] + rn[at[(C5["Lalitesh"] - 1) % N]]
assert ans == 78
Q("What is the total of the runs scored by the two immediate neighbours of Lalitesh?", str(ans), ["71", "65", "87"],
  "Numbers read off a circular arrangement",
  "Lalitesh sits at seat 5, between Jasmit (seat 4, 47 runs) and Inder (seat 0, 31 runs): 47 + 31 = 78.",
  [ARR, "Neighbours of seat 5: seats 4 and 0", "47 + 31 = 78"],
  why_others_wrong="71 uses Nayantara's 40 for Jasmit's 47; 65 uses Hrishikesh's 25 and Nayantara's 40; 87 is the total "
                   "for Hrishikesh's neighbours.", natural=int, seconds=110)
p25 = next(p for p in P if rn[p] == 25)
ans = at[(C5[p25] - 2) % N]
assert ans == "Kaveri"
Q("Who sits second to the left of the person who scored 25 runs?", ans, ["Inder", "Nayantara", "Jasmit"],
  "Facing the centre: left = clockwise",
  "Hrishikesh scored 25 and sits at seat 3. Moving clockwise: Nayantara (2), then Kaveri (1).",
  [ARR, "25 runs: Hrishikesh (seat 3)", "3 − 2 = seat 1 ⇒ Kaveri"],
  why_others_wrong="Nayantara is immediately to his left; Jasmit is immediately to his right; Inder sits opposite.",
  seconds=95)
opp_n = at[(C5["Nayantara"] + 3) % N]
cnt = sum(1 for p in P if rn[p] > rn[opp_n])
assert opp_n == "Lalitesh" and cnt == 4
Q("How many persons scored more runs than the person sitting opposite Nayantara?", num_word(cnt),
  ["Three", "Five", "Two"], "Identify the person, then compare values",
  "Opposite Nayantara (seat 2) is Lalitesh (seat 5), who scored 18. Only Kaveri (12) scored fewer, so four persons — "
  "Inder, Nayantara, Hrishikesh and Jasmit — scored more.", [ARR, "Opposite seat 2 = seat 5 = Lalitesh (18)",
                                                              "More than 18: 31, 40, 25, 47 ⇒ four"],
  natural=by_num, seconds=95)

# ================================================================================================ FLOOR PUZZLES
FLR = "Floor-Based Puzzles"
FF, FA = "Floor and flat", "Floor with attribute"
fq = lambda sid_, sub, diff: (lambda text, correct, wrongs, concept, expl, steps, **kw: puzzle_q(
    sid_, FLR, sub, diff, text, correct, wrongs, concept, expl, steps, **kw))

# ---- F1 Basic set: six floors with favourite sweets (floor 1 = lowermost)
P = ["Ayush", "Charulata", "Dakshesh", "Hemangi", "Kiranmayi", "Sohil"]
SW = ["Barfi", "Halwa", "Jalebi", "Laddoo", "Peda", "Rasgulla"]
S_ = ["s" + p for p in P]
VV = P + S_
IXV = {v: i for i, v in enumerate(VV)}
fl_of = lambda v, x: next(v[IXV[p]] for p in P if v[IXV["s" + p]] == x)
conds = [
    ("Ayush lives on floor 3 and likes Halwa.", ("Ayush", "sAyush"), lambda a, s: a == 3 and s == "Halwa"),
    ("Only one person lives between Ayush and Dakshesh, and Dakshesh lives above Ayush.", ("Dakshesh", "Ayush"),
     lambda d, a: d == a + 2),
    ("Charulata lives immediately above Dakshesh and likes Laddoo.", ("Charulata", "Dakshesh", "sCharulata"),
     lambda c, d, s: c == d + 1 and s == "Laddoo"),
    ("Kiranmayi lives immediately above Ayush.", ("Kiranmayi", "Ayush"), lambda k, a: k == a + 1),
    ("Hemangi lives on an even-numbered floor.", ("Hemangi",), lambda h: h % 2 == 0),
    ("The person who likes Peda lives on the lowermost floor, and the person who likes Jalebi lives immediately below "
     "Ayush.", tuple(VV), lambda *v: fl_of(v, "Peda") == 1 and fl_of(v, "Jalebi") == v[IXV["Ayush"]] - 1),
    ("The person who likes Rasgulla lives immediately above the person who likes Barfi.", tuple(VV),
     lambda *v: fl_of(v, "Rasgulla") == fl_of(v, "Barfi") + 1),
]
F1 = unique(VV, {p: range(1, 7) for p in P} | {s: SW for s in S_}, conds, [P, S_])
at = {F1[p]: p for p in P}
sw = {p: F1["s" + p] for p in P}
assert [(at[i], sw[at[i]]) for i in range(1, 7)] == [("Sohil", "Peda"), ("Hemangi", "Jalebi"), ("Ayush", "Halwa"),
                                                     ("Kiranmayi", "Barfi"), ("Dakshesh", "Rasgulla"),
                                                     ("Charulata", "Laddoo")]
ARR = "Bottom to top: " + ", ".join(f"floor {i} {at[i]} ({sw[at[i]]})" for i in range(1, 7))
sid = stimulus("puzzle", "Six floors and six favourite sweets",
               "Six persons Ayush, Charulata, Dakshesh, Hemangi, Kiranmayi and Sohil live on the six floors of a "
               "building, one on each floor. Floor 1 is the lowermost and floor 6 the topmost. Each of them likes a "
               "different sweet among Barfi, Halwa, Jalebi, Laddoo, Peda and Rasgulla.", conds,
               "Step 1: Ayush = 3, Dakshesh = 5, Charulata = 6, Kiranmayi = 4.\n"
               "Step 2: Floors 1 and 2 remain; Hemangi is on an even floor: Hemangi = 2, Sohil = 1.\n"
               "Step 3: Peda is on floor 1 (Sohil); Jalebi on floor 2 (Hemangi). Barfi and Rasgulla remain for floors 4 "
               "and 5; Rasgulla is above Barfi: Kiranmayi Barfi, Dakshesh Rasgulla.\n\n"
               + table(["Floor", "Person", "Sweet"], [(i, at[i], sw[at[i]]) for i in range(6, 0, -1)]))
Q = fq(sid, FA, "Basic")
ans = next(p for p in P if sw[p] == "Rasgulla")
assert ans == "Dakshesh"
Q("Who likes Rasgulla?", ans, ["Kiranmayi", "Charulata", "Hemangi"], "Adjacency of two attributes",
  "Barfi and Rasgulla are left for floors 4 and 5, and Rasgulla is immediately above Barfi, so Dakshesh (floor 5) likes "
  "Rasgulla.", [ARR], why_others_wrong="Kiranmayi likes Barfi, Charulata Laddoo and Hemangi Jalebi.", seconds=45)
cnt = abs(F1["Sohil"] - F1["Kiranmayi"]) - 1
assert cnt == 2
Q("How many persons live between Sohil and Kiranmayi?", num_word(cnt), ["One", "Three", "None"],
  "Count the floors strictly between", "Sohil is on floor 1 and Kiranmayi on floor 4; Hemangi and Ayush live between "
  "them.", [ARR, "Floors 2 and 3 ⇒ two persons"], natural=by_num, seconds=40)
ans = sw[at[F1["Hemangi"] + 1]]
assert ans == "Halwa"
Q("Which sweet does the person living immediately above Hemangi like?", ans, ["Barfi", "Peda", "Jalebi"],
  "Read the floor above, then its attribute", "Hemangi is on floor 2; floor 3 is Ayush's, and he likes Halwa.",
  [ARR, "Floor 3 = Ayush ⇒ Halwa"], why_others_wrong="Barfi is on floor 4, Peda on floor 1 and Jalebi is Hemangi's own.",
  seconds=40)

# ---- F2 Intermediate set: seven floors and monthly rents
P = ["Anvay", "Brijesh", "Dhruvika", "Gunjita", "Jasraj", "Moksha", "Neelesh"]
RENT = [8, 9, 11, 12, 14, 15, 17]  # thousand rupees
R_ = ["r" + p for p in P]
VV = P + R_
IXV = {v: i for i, v in enumerate(VV)}
fl_r = lambda v, r: next(v[IXV[p]] for p in P if v[IXV["r" + p]] == r)
conds = [
    ("Moksha lives on floor 4 and pays ₹14,000.", ("Moksha", "rMoksha"), lambda m, r: m == 4 and r == 14),
    ("The person who pays the highest rent lives two floors below Moksha.", tuple(VV),
     lambda *v: fl_r(v, 17) == v[IXV["Moksha"]] - 2),
    ("Jasraj lives immediately above Moksha and pays the lowest rent.", ("Jasraj", "Moksha", "rJasraj"),
     lambda j, m, r: j == m + 1 and r == 8),
    ("Anvay lives immediately below Moksha, and his rent is ₹1,000 more than Jasraj's.",
     ("Anvay", "Moksha", "rAnvay", "rJasraj"), lambda a, m, ra, rj: a == m - 1 and ra == rj + 1),
    ("Dhruvika lives on the topmost floor, and the rents of Dhruvika and Gunjita add up to ₹23,000.",
     ("Dhruvika", "rDhruvika", "rGunjita"), lambda d, rd, rg: d == 7 and rd + rg == 23),
    ("Brijesh pays ₹1,000 more than Moksha, and Gunjita lives below Brijesh.",
     ("rBrijesh", "rMoksha", "Gunjita", "Brijesh"), lambda rb, rm, g, b: rb == rm + 1 and g < b),
    ("Gunjita pays more than Dhruvika.", ("rGunjita", "rDhruvika"), lambda g, d: g > d),
]
F2 = unique(VV, {p: range(1, 8) for p in P} | {r: RENT for r in R_}, conds, [P, R_])
at = {F2[p]: p for p in P}
rt = {p: F2["r" + p] for p in P}
assert [(at[i], rt[at[i]]) for i in range(1, 8)] == [("Gunjita", 12), ("Neelesh", 17), ("Anvay", 9), ("Moksha", 14),
                                                     ("Jasraj", 8), ("Brijesh", 15), ("Dhruvika", 11)]
rs = lambda k: f"₹{k},000"
ARR = "Bottom to top: " + ", ".join(f"floor {i} {at[i]} ({rs(rt[at[i]])})" for i in range(1, 8))
sid = stimulus("puzzle", "Seven floors and seven monthly rents",
               "Seven persons Anvay, Brijesh, Dhruvika, Gunjita, Jasraj, Moksha and Neelesh live on the seven floors of a "
               "building, one on each floor (floor 1 is the lowermost, floor 7 the topmost). Each pays a different "
               "monthly rent among ₹8,000, ₹9,000, ₹11,000, ₹12,000, ₹14,000, ₹15,000 and ₹17,000.", conds,
               "Step 1: Moksha = 4 (₹14,000). Jasraj = 5 (₹8,000, the lowest). Anvay = 3 (₹9,000). The ₹17,000 payer "
               "is on floor 2. Dhruvika = 7.\n"
               "Step 2: Brijesh pays ₹15,000, so he is not on floor 2. Floors 1, 2 and 6 remain for Brijesh, Gunjita "
               "and Neelesh; Gunjita lives below Brijesh, so Brijesh cannot be on floor 1 — Brijesh = 6.\n"
               "Step 3: Rents left: ₹11,000, ₹12,000 and ₹17,000 for Dhruvika, Gunjita and Neelesh. Dhruvika + Gunjita "
               "= ₹23,000 = 11 + 12, so Neelesh pays ₹17,000 and lives on floor 2; Gunjita = 1. Gunjita pays more than "
               "Dhruvika: Gunjita ₹12,000, Dhruvika ₹11,000.\n\n"
               + table(["Floor", "Person", "Rent"], [(i, at[i], rs(rt[at[i]])) for i in range(7, 0, -1)]))
Q = fq(sid, FA, "Intermediate")
tot = rt[at[6]] + rt[at[7]]
assert tot == 26
Q("What is the total monthly rent paid by the persons on floors 6 and 7?", rs(tot), [rs(29), rs(23), rs(25)],
  "Combine positions with values", "Floor 6 is Brijesh (₹15,000) and floor 7 is Dhruvika (₹11,000): ₹26,000.",
  [ARR, "15 + 11 = 26 thousand"], why_others_wrong="₹29,000 uses Neelesh's rent; ₹23,000 is Dhruvika plus Gunjita; "
                                                   "₹25,000 uses ₹14,000 for floor 6.",
  natural=lambda t: int(t[1:].replace(",", "")), seconds=60)
ans = next(p for p in P if rt[p] == 12)
assert ans == "Gunjita"
Q("Who pays ₹12,000 a month?", ans, ["Dhruvika", "Neelesh", "Brijesh"], "Split a sum between two persons",
  "Dhruvika and Gunjita together pay ₹23,000, which can only be ₹11,000 + ₹12,000; Gunjita pays more, so she pays "
  "₹12,000.", [ARR], why_others_wrong="Dhruvika pays ₹11,000, Neelesh ₹17,000 and Brijesh ₹15,000.", seconds=60)
cnt = sum(1 for p in P if F2[p] < F2["Moksha"] and rt[p] > rt["Anvay"])
assert cnt == 2
Q("How many persons who live below Moksha pay more rent than Anvay?", num_word(cnt), ["One", "Three", "None"],
  "Filter by floor, then by value",
  "Below Moksha (floor 4) live Anvay (₹9,000), Neelesh (₹17,000) and Gunjita (₹12,000). Neelesh and Gunjita pay more "
  "than Anvay: two persons.", [ARR, "Floors 1–3: Gunjita 12, Neelesh 17, Anvay 9", "More than 9: two"],
  natural=by_num, seconds=60)

# ---- F3 Advanced set: nine floors numbered FROM THE TOP, seven persons, two vacant floors, professions
P = ["Amarjeet", "Bhuvanesh", "Chinmayee", "Durgesh", "Pankti", "Ritwik", "Shalaka"]
JOB = ["Actor", "Baker", "Coach", "Dentist", "Jeweller", "Nurse", "Plumber"]
J_ = ["j" + p for p in P]
VV = P + J_
IXV = {v: i for i, v in enumerate(VV)}
fl_j = lambda v, j: next(v[IXV[p]] for p in P if v[IXV["j" + p]] == j)
conds = [
    ("Durgesh lives on floor 5 and is a Plumber.", ("Durgesh", "jDurgesh"), lambda d, j: d == 5 and j == "Plumber"),
    ("The Baker lives immediately above Durgesh, and the floor immediately below Durgesh is vacant.", tuple(VV),
     lambda *v: fl_j(v, "Baker") == v[IXV["Durgesh"]] - 1 and v[IXV["Durgesh"]] + 1 not in v[:7]),
    ("Bhuvanesh lives on the lowermost floor, and Chinmayee lives immediately above him.", ("Bhuvanesh", "Chinmayee"),
     lambda b, c: b == 9 and c == 8),
    ("Pankti is a Dentist and lives immediately above Chinmayee.", ("Pankti", "jPankti", "Chinmayee"),
     lambda p, j, c: p == c - 1 and j == "Dentist"),
    ("Amarjeet lives three floors above Pankti.", ("Amarjeet", "Pankti"), lambda a, p: a == p - 3),
    ("Exactly one floor lies between Ritwik and Shalaka, and Ritwik lives above Shalaka.", ("Ritwik", "Shalaka"),
     lambda r, s: s == r + 2),
    ("The Nurse lives immediately above the Baker.", tuple(VV), lambda *v: fl_j(v, "Nurse") == fl_j(v, "Baker") - 1),
    ("Ritwik is neither the Actor nor the Jeweller, and the Jeweller lives below the Actor.", tuple(VV),
     lambda *v: v[IXV["jRitwik"]] not in ("Actor", "Jeweller") and fl_j(v, "Jeweller") > fl_j(v, "Actor")),
]
F3 = unique(VV, {p: range(1, 10) for p in P} | {j: JOB for j in J_}, conds, [P, J_])
at = {F3[p]: p for p in P}
jb = {p: F3["j" + p] for p in P}
assert [(at.get(i), jb.get(at.get(i))) for i in range(1, 10)] == [
    ("Ritwik", "Coach"), (None, None), ("Shalaka", "Nurse"), ("Amarjeet", "Baker"), ("Durgesh", "Plumber"),
    (None, None), ("Pankti", "Dentist"), ("Chinmayee", "Actor"), ("Bhuvanesh", "Jeweller")]
ARR = "Top to bottom: " + ", ".join(f"floor {i} {at[i]} ({jb[at[i]]})" if i in at else f"floor {i} vacant"
                                    for i in range(1, 10))
sid = stimulus("puzzle", "Nine floors numbered from the top, two vacant",
               "A building has nine floors. The floors are numbered from the top: floor 1 is the topmost floor and "
               "floor 9 the lowermost. Seven persons Amarjeet, Bhuvanesh, Chinmayee, Durgesh, Pankti, Ritwik and "
               "Shalaka live in it, one person per floor, so two floors are vacant. Each person has a different "
               "profession among Actor, Baker, Coach, Dentist, Jeweller, Nurse and Plumber.", conds,
               "Remember: a smaller floor number is higher up.\n"
               "Step 1: Durgesh = 5 (Plumber); floor 6 is vacant; the Baker is on floor 4.\n"
               "Step 2: Bhuvanesh = 9, Chinmayee = 8, Pankti = 7 (Dentist). Amarjeet = 7 − 3 = 4, so Amarjeet is the "
               "Baker.\n"
               "Step 3: Floors 1, 2 and 3 remain for Ritwik and Shalaka, with one floor between them and Ritwik higher: "
               "Ritwik = 1, Shalaka = 3, floor 2 vacant.\n"
               "Step 4: The Nurse is immediately above the Baker (floor 4): Shalaka. Actor, Coach and Jeweller remain "
               "for Ritwik, Chinmayee and Bhuvanesh; Ritwik is the Coach. The Jeweller is below the Actor: Bhuvanesh "
               "(9) Jeweller, Chinmayee (8) Actor.\n\n"
               + table(["Floor (from top)", "Person", "Profession"],
                       [(i, at.get(i, "vacant"), jb.get(at.get(i), "—")) for i in range(1, 10)]))
Q = fq(sid, FA, "Advanced")
vac_ = [i for i in range(1, 10) if i not in at]
assert vac_ == [2, 6]
Q("Which two floors are vacant?", "Floors 2 and 6", ["Floors 6 and 8", "Floors 2 and 4", "Floors 1 and 6"],
  "Floors numbered from the top", "Floor 6 is vacant by a direct clue. Ritwik and Shalaka must use two of floors 1–3 "
  "with one floor between them, so they take 1 and 3 and floor 2 is vacant.", [ARR], seconds=100)
nurse = next(p for p in P if jb[p] == "Nurse")
ans = at[F3[nurse] + 2]
assert ans == "Durgesh"
Q("Who lives two floors below the Nurse?", ans, ["Ritwik", "Amarjeet", "Pankti"],
  "With floors numbered from the top, 'below' means a larger number",
  "The Nurse is Shalaka on floor 3. Two floors below is floor 5: Durgesh.",
  [ARR, "Nurse = Shalaka (floor 3)", "3 + 2 = floor 5 ⇒ Durgesh"],
  why_others_wrong="Ritwik is two floors above her; Amarjeet is immediately below her; Pankti is four floors below.",
  seconds=95)
coach = next(p for p in P if jb[p] == "Coach")
dent = next(p for p in P if jb[p] == "Dentist")
cnt = sum(1 for i in range(F3[coach] + 1, F3[dent]) if i in at)
assert cnt == 3
Q("How many persons live between the Coach and the Dentist?", num_word(cnt), ["Five", "Four", "Two"],
  "Count persons, not floors", "The Coach (Ritwik) is on floor 1 and the Dentist (Pankti) on floor 7. Floors 2 to 6 lie "
  "between them; floors 2 and 6 are vacant, so three persons (Shalaka, Amarjeet, Durgesh) live between them.",
  [ARR, "Floors 2–6 between; 2 and 6 vacant ⇒ three"], why_others_wrong="Five counts the vacant floors as persons; "
                                                                        "Four counts one of them.", natural=by_num,
  seconds=95)

# ================================================================================================ BOX PUZZLES
BOX = "Box-Based Puzzles"
STK, BWC = "Stacked boxes", "Boxes with weights or colours"

# ---- X1 Basic set: seven boxes in one stack (position 1 = bottom)
B = ["B", "E", "G", "J", "N", "S", "W"]
conds = [("Box W is kept exactly in the middle of the stack.", ("W",), lambda w: w == 4),
         ("Only two boxes are kept between box W and box G, and box G is above box W.", ("G", "W"),
          lambda g, w: g == w + 3),
         ("Box B is kept immediately above box W.", ("B", "W"), lambda b, w: b == w + 1),
         ("Box J is kept at the bottom of the stack.", ("J",), lambda j: j == 1),
         ("Box E is kept immediately above box S.", ("E", "S"), lambda e, s: e == s + 1)]
X1 = unique(B, {b: range(1, 8) for b in B}, conds, [B])
at = {v: k for k, v in X1.items()}
assert [at[i] for i in range(1, 8)] == ["J", "S", "E", "W", "B", "N", "G"]
ARR = "Bottom to top: " + ", ".join(at[i] for i in range(1, 8))
sid = stimulus("puzzle", "Seven boxes in one stack",
               "Seven boxes B, E, G, J, N, S and W are kept one above another in a single stack. Position 1 is the "
               "bottom and position 7 the top.", conds,
               "W = 4, G = 7, B = 5, J = 1. Positions 2, 3 and 6 remain for E, N and S. E is immediately above S, so "
               "they take 2 and 3 (S = 2, E = 3), and N = 6.\n\n" + ARR)
Q = lambda text, correct, wrongs, concept, expl, steps, **kw: puzzle_q(sid, BOX, STK, "Basic", text, correct, wrongs,
                                                                       concept, expl, steps, **kw)
ans = at[X1["N"] - 1]
assert ans == "B"
Q("Which box is kept immediately below box N?", ans, ["G", "W", "E"], "Fill the last gap of the stack",
  "N is the only box left for position 6, so the box below it is at position 5: B.", [ARR],
  why_others_wrong="G is above N; W and E are lower down.", seconds=40)
cnt = X1["B"] - X1["J"] - 1
assert cnt == 3
Q("How many boxes are kept between box J and box B?", num_word(cnt), ["Two", "Four", "Five"],
  "Count positions strictly between", "J is at 1 and B at 5; S, E and W lie between them.", [ARR], natural=by_num,
  seconds=35)
ans = at[6]
Q("Which box is kept second from the top?", ans, ["G", "B", "E"], "Second from the top of seven = position 6",
  "Position 7 is G (top); position 6 is N.", [ARR], why_others_wrong="G is at the top; B is third from the top; E is "
                                                                     "fifth.", seconds=35)

# ---- X2 Basic (standalone): six boxes in one stack
B = ["A", "D", "F", "K", "Q", "U"]
conds = [("Box K is kept third from the bottom.", ("K",), lambda k: k == 3),
         ("Box Q is kept immediately above box K.", ("Q", "K"), lambda q, k: q == k + 1),
         ("Box A is kept at the top.", ("A",), lambda a: a == 6),
         ("Box D is kept immediately above box F.", ("D", "F"), lambda d, f: d == f + 1)]
X2 = unique(B, {b: range(1, 7) for b in B}, conds, [B])
at = {v: k for k, v in X2.items()}
assert [at[i] for i in range(1, 7)] == ["F", "D", "K", "Q", "U", "A"]
mcq(BOX, STK, "Basic", "Six boxes A, D, F, K, Q and U are kept one above another in a single stack. Position 1 is the "
    "bottom and position 6 the top.\n" + bullets(conds) + "\n\nWhich box is kept immediately below box A?", at[5],
    ["Q", "D", "K"], "Use the free pair of adjacent positions",
    "K = 3, Q = 4, A = 6. Positions 1, 2 and 5 remain; D must be immediately above F, so F = 1 and D = 2, leaving U at "
    "5 — immediately below A.", ["K 3, Q 4, A 6", "Free: 1, 2, 5; D on F ⇒ F 1, D 2", "U 5 ⇒ below A"],
    why_others_wrong="Q is at 4 (two below A); D and K are lower still.", seconds=40, verified_by=BRUTE)

# ---- X3 Basic (standalone): five coloured boxes in one stack
B = ["H", "L", "M", "R", "T"]
CO = ["Blue", "Green", "Red", "White", "Yellow"]
K_ = ["c" + b for b in B]
VV = B + K_
IXV = {v: i for i, v in enumerate(VV)}
pos_c = lambda v, c: next(v[IXV[b]] for b in B if v[IXV["c" + b]] == c)
conds = [("Box H is kept in the middle of the stack and is Yellow.", ("H", "cH"), lambda h, c: h == 3 and c == "Yellow"),
         ("The Green box is at the top, and box R is kept immediately below the Green box.", tuple(VV),
          lambda *v: pos_c(v, "Green") == 5 and v[IXV["R"]] == 4),
         ("The White box is at the bottom.", tuple(VV), lambda *v: pos_c(v, "White") == 1),
         ("Box M is kept immediately below box T.", ("M", "T"), lambda m, t: m == t - 1),
         ("Box T is not Blue.", ("cT",), lambda c: c != "Blue")]
X3 = unique(VV, {b: range(1, 6) for b in B} | {k: CO for k in K_}, conds, [B, K_])
assert (X3["M"], X3["T"], X3["L"], X3["cT"], X3["cR"]) == (1, 2, 5, "Red", "Blue")
mcq(BOX, BWC, "Basic", "Five boxes H, L, M, R and T are kept one above another in a single stack (position 1 is the "
    "bottom). Each box is of a different colour among Blue, Green, Red, White and Yellow.\n" + bullets(conds) +
    "\n\nWhat is the colour of box R?", X3["cR"], ["Red", "Green", "White"], "Positions first, then colours",
    "H = 3 (Yellow) and R = 4. M is immediately below T, and the only free adjacent pair is 1–2, so M = 1, T = 2 and L = 5. L (top) is Green "
    "and M (bottom) is White. Blue and Red remain for T and R; T is not Blue, so T is Red and R is Blue.",
    ["H 3, R 4; M 1, T 2; L 5", "Top L = Green; bottom M = White", "T ≠ Blue ⇒ T Red, R Blue"],
    why_others_wrong="Red is T's colour, Green L's and White M's.", seconds=50, verified_by=BRUTE)

# ---- X4 Intermediate (standalone): eight boxes; equal counts above and below
B = ["C", "F", "I", "K", "O", "P", "V", "Z"]
conds = [("Exactly three boxes are kept below box P.", ("P",), lambda p: p == 4),
         ("Only two boxes are kept between box Z and box V, and box V is above box Z.", ("Z", "V"),
          lambda z, v: v == z + 3),
         ("As many boxes are kept above box V as below box Z.", ("Z", "V"), lambda z, v: 8 - v == z - 1),
         ("Box C is kept immediately above box P.", ("C", "P"), lambda c, p: c == p + 1),
         ("Box F is at the top, and box I is kept immediately below box F.", ("F", "I"), lambda f, i: f == 8 and i == 7),
         ("Box K is kept immediately below box Z.", ("K", "Z"), lambda k, z: k == z - 1)]
X4 = unique(B, {b: range(1, 9) for b in B} | {"Z": range(1, 9)}, conds, [B])
at = {v: k for k, v in X4.items()}
assert [at[i] for i in range(1, 9)] == ["O", "K", "Z", "P", "C", "V", "I", "F"]
cnt = X4["I"] - X4["K"] - 1
assert cnt == 4
mcq(BOX, STK, "Intermediate", "Eight boxes C, F, I, K, O, P, V and Z are kept one above another in a single stack "
    "(position 1 is the bottom, 8 the top).\n" + bullets(conds) + "\n\nHow many boxes are kept between box K and box "
    "I?", num_word(cnt), ["Three", "Five", "Two"], "Turn two count clues into equations",
    "P = 4 and C = 5; F = 8 and I = 7. V = Z + 3, and the boxes above V (8 − V) equal the boxes below Z (Z − 1): "
    "8 − Z − 3 = Z − 1, so Z = 3 and V = 6. K = 2 and O = 1. Between K (2) and I (7) lie Z, P, C and V: four boxes.",
    ["P 4, C 5, F 8, I 7", "8 − (Z + 3) = Z − 1 ⇒ Z = 3, V = 6", "K 2, O 1", "Between 2 and 7: four"],
    why_others_wrong="Three and Five are off by one; Two counts only the boxes between Z and V.", natural=by_num,
    seconds=70, verified_by=BRUTE)

# ---- X5 Intermediate (standalone): five boxes with weights
B = ["G", "L", "R", "U", "Y"]
WT = [10, 15, 20, 25, 30]
W_ = ["w" + b for b in B]
VV = B + W_
IXV = {v: i for i, v in enumerate(VV)}
pos_w = lambda v, w: next(v[IXV[b]] for b in B if v[IXV["w" + b]] == w)
conds = [("The heaviest box is kept in the middle of the stack, and the lightest box immediately below it.", tuple(VV),
          lambda *v: pos_w(v, 30) == 3 and pos_w(v, 10) == 2),
         ("Box R is at the bottom and weighs 5 kg less than the heaviest box.", ("R", "wR"),
          lambda r, w: r == 1 and w == 25),
         ("Box L is at the top and weighs 20 kg.", ("L", "wL"), lambda l, w: l == 5 and w == 20),
         ("Box U weighs 5 kg more than box Y.", ("wU", "wY"), lambda u, y: u == y + 5)]
X5 = unique(VV, {b: range(1, 6) for b in B} | {w: WT for w in W_}, conds, [B, W_])
at = {X5[b]: b for b in B}
assert [(at[i], X5["w" + at[i]]) for i in range(1, 6)] == [("R", 25), ("Y", 10), ("G", 30), ("U", 15), ("L", 20)]
tot = X5["w" + at[X5["G"] - 1]] + X5["w" + at[X5["G"] + 1]]
assert tot == 25
mcq(BOX, BWC, "Intermediate", "Five boxes G, L, R, U and Y are kept one above another in a single stack (position 1 "
    "is the bottom). Their weights are 10, 15, 20, 25 and 30 kg, one weight per box.\n" + bullets(conds) +
    "\n\nWhat is the total weight of the two boxes kept immediately above and immediately below box G?", f"{tot} kg",
    ["35 kg", "45 kg", "30 kg"], "Weights fix the positions",
    "R (25 kg) is at the bottom and L (20 kg) at the top. Weights left: 10, 15, 30 for G, U and Y; U = Y + 5 forces "
    "Y = 10 and U = 15, so G = 30 is the heaviest, in the middle (3). The lightest, Y, is at 2 and U at 4. The boxes "
    "next to G weigh 10 + 15 = 25 kg.",
    ["R 1 (25), L 5 (20)", "U = Y + 5 with 10, 15, 30 left ⇒ Y 10, U 15, G 30", "G 3, Y 2, U 4", "10 + 15 = 25 kg"],
    why_others_wrong="35 kg adds R and Y; 45 kg adds R and L; 30 kg is G's own weight.",
    natural=lambda t: int(t.split()[0]), seconds=70, verified_by=BRUTE)

# ---- X6 Advanced set: ten boxes in two stacks of five (Left and Right), side by side
B = ["B", "D", "F", "H", "K", "M", "P", "R", "T", "W"]
SP = [(s, l) for s in "LR" for l in range(1, 6)]
oth = lambda p: ("R" if p[0] == "L" else "L", p[1])
conds = [("Box T is at level 3 of the left stack, and box F is directly to the right of box T (at the same level of "
          "the other stack).", ("T", "F"), lambda t, f: t == ("L", 3) and f == ("R", 3)),
         ("Box P is kept immediately above box F, and box H is at the top of the stack that contains box P.",
          ("P", "F", "H"), lambda p, f, h: p == (f[0], f[1] + 1) and h == (p[0], 5)),
         ("Box B is at the same level as box P, in the other stack.", ("B", "P"), lambda b, p: b == oth(p)),
         ("Box K is at the bottom of the stack that does not contain box H.", ("K", "H"),
          lambda k, h: k == (oth(h)[0], 1)),
         ("Boxes B and D are in the same stack, and as many boxes are kept above box B as below box D.", ("B", "D"),
          lambda b, d: b[0] == d[0] and 5 - b[1] == d[1] - 1),
         ("Box W is kept immediately above box M, and box R is not in the stack that contains box W.",
          ("W", "M", "R"), lambda w, m, r: w == (m[0], m[1] + 1) and r[0] != w[0])]
X6 = unique(B, {b: SP for b in B}, conds, [B])
at = {v: k for k, v in X6.items()}
assert [at[("L", l)] for l in range(1, 6)] == ["K", "D", "T", "B", "R"]
assert [at[("R", l)] for l in range(1, 6)] == ["M", "W", "F", "P", "H"]
ARR = ("Left stack, bottom to top: " + ", ".join(at[("L", l)] for l in range(1, 6)) +
       "; Right stack, bottom to top: " + ", ".join(at[("R", l)] for l in range(1, 6)))
sid = stimulus("puzzle", "Ten boxes in two side-by-side stacks",
               "Ten boxes B, D, F, H, K, M, P, R, T and W are kept in two stacks, Left and Right, standing side by side, "
               "with five boxes in each stack. Level 1 is the bottom of a stack and level 5 its top. A box is 'directly "
               "to the right' of another when it is at the same level of the Right stack.", conds,
               "Step 1: T = Left 3, F = Right 3, P = Right 4, H = Right 5. B is at level 4 of the Left stack.\n"
               "Step 2: K is at the bottom of the stack without H: Left 1.\n"
               "Step 3: D is in B's stack (Left). One box is above B (level 5), so one box is below D: D = Left 2.\n"
               "Step 4: Left 5, Right 1 and Right 2 remain for M, R and W. W is immediately above M, so they take "
               "Right 1 and Right 2 (M = Right 1, W = Right 2); R is in the other stack: Left 5.\n\n"
               + table(["Level", "Left stack", "Right stack"], [(l, at[("L", l)], at[("R", l)]) for l in range(5, 0, -1)]))
Q = lambda text, correct, wrongs, concept, expl, steps, **kw: puzzle_q(sid, BOX, STK, "Advanced", text, correct, wrongs,
                                                                       concept, expl, steps, **kw)
ans = at[oth(X6["M"])]
assert ans == "K"
Q("Which box is at the same level as box M, in the other stack?", ans, ["D", "W", "T"],
  "Same level across two stacks", "M is at level 1 of the Right stack; level 1 of the Left stack holds K.", [ARR],
  why_others_wrong="D is at level 2 (beside W); W is above M in the same stack; T is at level 3.", seconds=80)
cnt = X6["P"][1] - 1
assert cnt == 3
Q("How many boxes are kept below box P in its stack?", num_word(cnt), ["Two", "Four", "One"],
  "Count within one stack only", "P is at level 4 of the Right stack, above F, W and M: three boxes.", [ARR],
  natural=by_num, seconds=75)
ans = at[("L", 5)]
assert ans == "R"
Q("Which box is at the top of the Left stack?", ans, ["B", "H", "W"], "Use the 'not in the same stack' clue last",
  "M, R and W fill Left 5, Right 1 and Right 2. W sits directly on M, which is possible only in the Right stack; R is "
  "kept out of W's stack, so R takes Left 5.", [ARR],
  why_others_wrong="B is at Left 4; H is at the top of the Right stack; W is at Right 2.", seconds=85)
stm = [("Box D is directly to the left of box W", X6["W"] == oth(X6["D"]) and X6["D"][0] == "L"),
       ("Box B is directly to the left of box F", X6["F"] == oth(X6["B"])),
       ("Box K is kept immediately below box T", X6["K"] == (X6["T"][0], X6["T"][1] - 1)),
       ("Box H is at the same level as box B", X6["H"][1] == X6["B"][1])]
t, f = one_true(stm)
Q("Which of the following statements is true?", t, f, "Check each statement against both stacks",
  "D (Left 2) and W (Right 2) are at the same level, so D is directly to the left of W. B is beside P, not F; D, not "
  "K, is immediately below T; H is at level 5 and B at level 4.", [ARR], seconds=85)

# ---- X7 Advanced set: eight coloured boxes in one stack
B = ["C", "E", "H", "L", "O", "S", "V", "Y"]
CO = ["Brown", "Cream", "Golden", "Grey", "Navy", "Olive", "Peach", "Silver"]
K_ = ["c" + b for b in B]
VV = B + K_
IXV = {v: i for i, v in enumerate(VV)}
pos_c = lambda v, c: next(v[IXV[b]] for b in B if v[IXV["c" + b]] == c)
conds = [
    ("Box C is kept fourth from the bottom.", ("C",), lambda c: c == 4),
    ("Only two boxes are kept between box C and the Cream box, and the Cream box is above C.", tuple(VV),
     lambda *v: pos_c(v, "Cream") == v[IXV["C"]] + 3),
    ("Box L is kept immediately above box V, which is not Grey.", ("L", "V", "cV"),
     lambda l, v, c: l == v + 1 and c != "Grey"),
    ("Box S is at the bottom and is Navy.", ("S", "cS"), lambda s, c: s == 1 and c == "Navy"),
    ("The Olive box is kept immediately above the Golden box, and box Y is Golden.", tuple(VV),
     lambda *v: pos_c(v, "Olive") == pos_c(v, "Golden") + 1 and v[IXV["cY"]] == "Golden"),
    ("Box O is kept immediately above box C, and box E is kept immediately below box V.", ("O", "C", "E", "V"),
     lambda o, c, e, v: o == c + 1 and e == v - 1),
    ("Box L is Brown, box H is Peach, and box O is not Grey.", ("cL", "cH", "cO"),
     lambda l, h, o: l == "Brown" and h == "Peach" and o != "Grey"),
]
X7 = unique(VV, {b: range(1, 9) for b in B} | {k: CO for k in K_}, conds, [B, K_])
at = {X7[b]: b for b in B}
co = {b: X7["c" + b] for b in B}
assert [(at[i], co[at[i]]) for i in range(1, 9)] == [
    ("S", "Navy"), ("H", "Peach"), ("Y", "Golden"), ("C", "Olive"), ("O", "Silver"), ("E", "Grey"), ("V", "Cream"),
    ("L", "Brown")]
ARR = "Bottom to top: " + ", ".join(f"{i} {at[i]} ({co[at[i]]})" for i in range(1, 9))
sid = stimulus("puzzle", "Eight boxes in eight colours",
               "Eight boxes C, E, H, L, O, S, V and Y are kept one above another in a single stack (position 1 is the "
               "bottom and 8 the top). Each box is of a different colour among Brown, Cream, Golden, Grey, Navy, "
               "Olive, Peach and Silver.", conds,
               "Step 1: C = 4; the Cream box is at 7; O = 5; S = 1 (Navy).\n"
               "Step 2: L is immediately above V and E immediately below V, so E, V, L occupy three consecutive "
               "positions among the free ones (2, 3, 6, 7, 8): only 6, 7, 8 work. E = 6, V = 7 (Cream), L = 8 (Brown).\n"
               "Step 3: H and Y take 2 and 3. The Olive box is immediately above the Golden box Y. If Y were at 2, "
               "position 3 would be Olive, but H at 3 is Peach; so Y = 3 and H = 2, and C (position 4) is Olive.\n"
               "Step 4: Grey and Silver remain for O and E; O is not Grey, so O is Silver and E is Grey.\n\n"
               + table(["Position", "Box", "Colour"], [(i, at[i], co[at[i]]) for i in range(8, 0, -1)]))
Q = lambda text, correct, wrongs, concept, expl, steps, **kw: puzzle_q(sid, BOX, BWC, "Advanced", text, correct, wrongs,
                                                                       concept, expl, steps, **kw)
ans = co[at[X7["O"] - 1]]
assert ans == "Olive"
Q("What is the colour of the box kept immediately below box O?", ans, ["Golden", "Grey", "Silver"],
  "Locate the box, then its colour", "O is at position 5; position 4 is C, which is Olive (directly above the Golden "
  "box Y).", [ARR], why_others_wrong="Golden is Y's (position 3), Grey is E's (above O), Silver is O's own colour.",
  seconds=90)
cnt = abs(pos_c([X7[v] for v in VV], "Grey") - pos_c([X7[v] for v in VV], "Navy")) - 1
assert cnt == 4
Q("Counting only the boxes placed strictly between them, how many boxes separate the Navy box from the Grey box?", num_word(cnt), ["Three", "Five", "Six"],
  "Count positions strictly between", "Navy is S at position 1 and Grey is E at position 6; four boxes (H, Y, C, O) lie "
  "between them.", [ARR], natural=by_num, seconds=85)
ans = at[X7["L"] - 2]
assert ans == "E"
Q("Which box is kept two places below the Brown box?", ans, ["V", "O", "C"], "Brown = L at the top",
  "L (Brown) is at position 8; two places below is position 6: E.", [ARR, "8 − 2 = 6 ⇒ E"],
  why_others_wrong="V is immediately below L; O and C are three and four places below.", seconds=80)
stm = [("Box H is kept immediately above the Golden box", X7["H"] == X7["Y"] + 1),
       ("The Silver box is kept immediately above box C", co[at[X7["C"] + 1]] == "Silver"),
       ("Box V is Grey", co["V"] == "Grey"),
       ("Three boxes are kept above the Cream box", 8 - X7["V"] == 3)]
t, f = one_true(stm)
Q("Which of the following statements is true?", t, f, "Check each statement against the final stack",
  "O, directly above C, is Silver. H is below the Golden box Y; V is Cream; only one box (L) is above the Cream box.",
  [ARR], seconds=90)

# ================================================================================================ MONTH / DATE / YEAR
MB, DB, YB = "Month-based", "Date-based", "Year-based"
WD = lambda y, m, d_: dt.date(y, m, d_).strftime("%A")

# ---- M1 Basic (standalone): five trips in five given months
P = ["Darshana", "Govinda", "Kunjal", "Prakhar", "Sumedha"]
MS = [1, 4, 7, 10, 12]
conds = [("Kunjal travels in the only one of these months that has 30 days.", ("Kunjal",),
          lambda k: MDAYS[k] == 30),
         ("Prakhar travels in the next of these months after Kunjal's.", ("Prakhar", "Kunjal"),
          lambda p, k: MS.index(p) == MS.index(k) + 1),
         ("Sumedha travels in the last of these months.", ("Sumedha",), lambda s: s == 12),
         ("Govinda does not travel in January.", ("Govinda",), lambda g: g != 1)]
M1 = unique(P, {p: MS for p in P}, conds, [P])
assert (M1["Kunjal"], M1["Prakhar"], M1["Govinda"], M1["Darshana"]) == (4, 7, 10, 1)
ans = next(p for p in P if M1[p] == 10)
mcq(MON, MB, "Basic", "Five friends Darshana, Govinda, Kunjal, Prakhar and Sumedha each take one trip in the same "
    "year, in five different months among January, April, July, October and December.\n" + bullets(conds) +
    "\n\nWho travels in October?", ans, ["Prakhar", "Darshana", "Sumedha"], "Month lengths fix the first person",
    "Of January, April, July, October and December, only April has 30 days: Kunjal. The next listed month is July: "
    "Prakhar. Sumedha takes December. January and October remain; Govinda is not in January, so Govinda travels in "
    "October and Darshana in January.",
    ["30-day month among the five: April ⇒ Kunjal", "Next month in the list: July ⇒ Prakhar", "December ⇒ Sumedha",
     "Govinda ≠ January ⇒ Govinda October"],
    why_others_wrong="Prakhar travels in July, Darshana in January and Sumedha in December.", seconds=45,
    verified_by=BRUTE)

# ---- M2 Basic (standalone): four visits on four dates of June 2026 (1 June 2026 is a Monday)
assert WD(2026, 6, 1) == "Monday"
P = ["Hansa", "Lokesh", "Ruchika", "Tanmay"]
DTS = [5, 9, 14, 22]
conds = [("Ruchika visits on the earliest of the four dates.", ("Ruchika",), lambda r: r == 5),
         ("Hansa visits on the 14th.", ("Hansa",), lambda h: h == 14),
         ("Tanmay visits after Lokesh.", ("Tanmay", "Lokesh"), lambda t, l: t > l)]
M2 = unique(P, {p: DTS for p in P}, conds, [P])
ans = WD(2026, 6, M2["Lokesh"])
assert M2["Lokesh"] == 9 and ans == "Tuesday"
mcq(MON, DB, "Basic", "Four persons Hansa, Lokesh, Ruchika and Tanmay each visit a museum once in June 2026, on four "
    "different dates among the 5th, 9th, 14th and 22nd. 1 June 2026 is a Monday.\n" + bullets(conds) +
    "\n\nOn which day of the week does Lokesh visit?", ans, ["Monday", "Wednesday", "Sunday"],
    "Dates seven days apart fall on the same weekday",
    "Ruchika takes the 5th and Hansa the 14th, leaving the 9th and the 22nd; Tanmay is after Lokesh, so Lokesh visits on "
    "the 9th. 1 June is a Monday, so 8 June is also a Monday and 9 June a Tuesday.",
    ["Ruchika 5th, Hansa 14th", "Lokesh before Tanmay ⇒ Lokesh 9th, Tanmay 22nd", "1 June Monday ⇒ 8 June Monday ⇒ "
     "9 June Tuesday"], why_others_wrong="Monday is the 8th; Wednesday is the 10th; Sunday is the 7th.", seconds=45,
    verified_by=BRUTE)

# ---- M3 Intermediate set: six meetings in six given months, with cities
P = ["Aruna", "Bhaskar", "Gauravi", "Jitesh", "Madhulika", "Sameer"]
CT = ["Ajmer", "Bareilly", "Hubli", "Jorhat", "Nashik", "Rourkela"]
MS = [2, 3, 5, 7, 8, 11]
C_ = ["c" + p for p in P]
VV = P + C_
IXV = {v: i for i, v in enumerate(VV)}
m_c = lambda v, c: next(v[IXV[p]] for p in P if v[IXV["c" + p]] == c)
ix = MS.index
conds = [
    ("Gauravi's meeting is in a month that has 31 days, and it is held in Jorhat.", ("Gauravi", "cGauravi"),
     lambda g, c: MDAYS[g] == 31 and c == "Jorhat"),
    ("Exactly two of the meetings are held between Gauravi's and Jitesh's, and Jitesh's is earlier.",
     ("Gauravi", "Jitesh"), lambda g, j: ix(g) - ix(j) == 3),
    ("Madhulika's meeting is the last of the six.", ("Madhulika",), lambda m: m == 11),
    ("Bhaskar's meeting is the next one after Gauravi's, and it is held in Rourkela.",
     ("Bhaskar", "Gauravi", "cBhaskar"), lambda b, g, c: ix(b) == ix(g) + 1 and c == "Rourkela"),
    ("Aruna's meeting is earlier than Sameer's.", ("Aruna", "Sameer"), lambda a, s: a < s),
    ("The Hubli meeting is in the shortest of the six months, and the Ajmer meeting is the one just before "
     "Gauravi's.", tuple(VV), lambda *v: m_c(v, "Hubli") == 2 and ix(m_c(v, "Ajmer")) == ix(v[IXV["Gauravi"]]) - 1),
    ("The Nashik meeting is in a month that has 31 days.", tuple(VV), lambda *v: MDAYS[m_c(v, "Nashik")] == 31),
]
M3 = unique(VV, {p: MS for p in P} | {c: CT for c in C_}, conds, [P, C_])
mo = {p: M3[p] for p in P}
ct = {p: M3["c" + p] for p in P}
ORD = sorted(P, key=mo.get)
assert [(p, MNAME[mo[p]], ct[p]) for p in ORD] == [
    ("Jitesh", "February", "Hubli"), ("Aruna", "March", "Nashik"), ("Sameer", "May", "Ajmer"),
    ("Gauravi", "July", "Jorhat"), ("Bhaskar", "August", "Rourkela"), ("Madhulika", "November", "Bareilly")]
ARR = "; ".join(f"{MNAME[mo[p]]}: {p} ({ct[p]})" for p in ORD)
sid = stimulus("puzzle", "Six meetings in six months, with cities",
               "Six persons Aruna, Bhaskar, Gauravi, Jitesh, Madhulika and Sameer each attend one meeting in the same "
               "non-leap year. The meetings are held in six different months — February, March, May, July, August and "
               "November — and in six different cities among Ajmer, Bareilly, Hubli, Jorhat, Nashik and Rourkela. "
               "'Between' and 'next' refer to the order of these six meetings.", conds,
               "Step 1: Gauravi's month has 31 days: March, May, July or August. Jitesh is three meetings earlier, so "
               "Gauravi is in July (Jitesh February) or August (Jitesh March).\n"
               "Step 2: Bhaskar is the next meeting after Gauravi's. If Gauravi were in August, Bhaskar would be in "
               "November, which is Madhulika's. So Gauravi = July, Jitesh = February, Bhaskar = August.\n"
               "Step 3: Aruna and Sameer take March and May; Aruna is earlier: Aruna March, Sameer May.\n"
               "Step 4: Hubli is in February (Jitesh); Ajmer is just before July: May (Sameer). Bareilly and Nashik "
               "remain for March and November; Nashik is in a 31-day month: Aruna Nashik, Madhulika Bareilly.\n\n"
               + table(["Month", "Person", "City"], [(MNAME[mo[p]], p, ct[p]) for p in ORD]))
Q = lambda text, correct, wrongs, concept, expl, steps, **kw: puzzle_q(sid, MON, MB, "Intermediate", text, correct,
                                                                       wrongs, concept, expl, steps, **kw)
ans = next(p for p in P if ct[p] == "Ajmer")
assert ans == "Sameer"
Q("Whose meeting is held in Ajmer?", ans, ["Aruna", "Jitesh", "Bhaskar"], "Order clue for a city",
  "The Ajmer meeting is the one just before Gauravi's July meeting, i.e. in May, which is Sameer's.", [ARR],
  why_others_wrong="Aruna is in Nashik, Jitesh in Hubli and Bhaskar in Rourkela.", seconds=60)
ans = MNAME[next(mo[p] for p in P if ct[p] == "Bareilly")]
assert ans == "November"
Q("In which month is the Bareilly meeting held?", ans, ["March", "August", "May"], "Elimination of the last two cities",
  "Bareilly and Nashik remain for Aruna (March) and Madhulika (November). November has 30 days, so Nashik goes to March "
  "and Bareilly to November.", [ARR], why_others_wrong="March is Nashik, August Rourkela and May Ajmer.", seconds=60)
cnt = ix(mo["Madhulika"]) - ix(mo["Aruna"]) - 1
assert cnt == 3
Q("How many meetings are held between Aruna's meeting and Madhulika's meeting?", num_word(cnt), ["Two", "Four", "Five"],
  "Count meetings, not calendar months", "Between March (Aruna) and November (Madhulika) come the May, July and August "
  "meetings: three. (The calendar months that have no meeting are not counted.)", [ARR], natural=by_num, seconds=60)
stm = [("Gauravi – July – Jorhat", mo["Gauravi"] == 7 and ct["Gauravi"] == "Jorhat"),
       ("Jitesh – March – Hubli", mo["Jitesh"] == 3 and ct["Jitesh"] == "Hubli"),
       ("Sameer – May – Nashik", mo["Sameer"] == 5 and ct["Sameer"] == "Nashik"),
       ("Bhaskar – November – Rourkela", mo["Bhaskar"] == 11 and ct["Bhaskar"] == "Rourkela")]
t, f = one_true(stm)
Q("Which of the following person – month – city combinations is correct?", t, f, "Read both attributes off the table",
  ARR + ".", [ARR], seconds=60)

# ---- M4 Intermediate set: eight appointments on the Tuesdays and Fridays of October 2026 (1 October is a Thursday)
assert WD(2026, 10, 1) == "Thursday"
SL = [k for k in range(1, 32) if dt.date(2026, 10, k).weekday() in (1, 4)]
assert SL == [2, 6, 9, 13, 16, 20, 23, 27, 30]
wd = lambda k: WD(2026, 10, k)
P = ["Chandrima", "Dheeraj", "Farhana", "Jugnu", "Kshitij", "Mahua", "Prachi", "Rishabh"]
nth = lambda k: sum(1 for x in SL if x <= k and wd(x) == wd(k))
between = lambda v, a, b: sum(1 for x in v if min(a, b) < x < max(a, b))
conds = [
    ("Chandrima's appointment is on the third Friday of the month.", ("Chandrima",),
     lambda c: wd(c) == "Friday" and nth(c) == 3),
    ("Only two persons have appointments between Chandrima's and Dheeraj's, and Dheeraj's is later.", tuple(P),
     lambda *v: v[1] > v[0] and between(v, v[0], v[1]) == 2),
    ("Mahua's appointment is on the last of the nine possible dates.", ("Mahua",), lambda m: m == 30),
    ("No appointment is fixed on the second Friday of the month.", tuple(P), lambda *v: 9 not in v),
    ("Farhana's appointment is on the possible date immediately before Chandrima's.", ("Farhana", "Chandrima"),
     lambda f, c: SL.index(f) == SL.index(c) - 1),
    ("Kshitij's appointment is on the first Tuesday, and Prachi's is earlier than Kshitij's.", ("Kshitij", "Prachi"),
     lambda k, p: wd(k) == "Tuesday" and nth(k) == 1 and p < k),
    ("Jugnu's appointment is on a Tuesday.", ("Jugnu",), lambda j: wd(j) == "Tuesday"),
]
M4 = unique(P, {p: SL for p in P}, conds, [P])
at = {v: k for k, v in M4.items()}
assert [at.get(k) for k in SL] == ["Prachi", "Kshitij", None, "Farhana", "Chandrima", "Jugnu", "Rishabh", "Dheeraj",
                                   "Mahua"]
ARR = "; ".join(f"{k} Oct ({wd(k)[:3]}): {at.get(k, 'no appointment')}" for k in SL)
sid = stimulus("puzzle", "Appointments on the Tuesdays and Fridays of October 2026",
               "A bank's loan officer meets customers only on Tuesdays and Fridays. Eight customers Chandrima, Dheeraj, "
               "Farhana, Jugnu, Kshitij, Mahua, Prachi and Rishabh each have one appointment with her in October 2026, "
               "on eight different dates; one of the possible dates has no appointment. 1 October 2026 is a Thursday.",
               conds,
               "Step 1: 1 October is a Thursday, so the Fridays are 2, 9, 16, 23, 30 and the Tuesdays 6, 13, 20, 27: "
               "nine possible dates.\n"
               "Step 2: Chandrima = 16 (third Friday); the 9th has no appointment; Mahua = 30; Farhana = 13 (the "
               "possible date just before the 16th). Kshitij = 6 (first Tuesday), so Prachi = 2.\n"
               "Step 3: The 20th, 23rd and 27th remain for Dheeraj, Jugnu and Rishabh. Two persons sit between "
               "Chandrima and Dheeraj, so Dheeraj = 27. Jugnu is on a Tuesday: 20; Rishabh = 23.\n\n"
               + table(["Date", "Day", "Customer"], [(f"{k} Oct", wd(k), at.get(k, "—")) for k in SL]))
Q = lambda text, correct, wrongs, concept, expl, steps, **kw: puzzle_q(sid, MON, DB, "Intermediate", text, correct,
                                                                       wrongs, concept, expl, steps, **kw)
ans = f"{M4['Rishabh']} October"
assert ans == "23 October"
Q("On which date is Rishabh's appointment?", ans, ["20 October", "27 October", "9 October"],
  "Weekdays from the first date of the month", "After the fixed dates, the 20th, 23rd and 27th remain. Dheeraj must be "
  "on the 27th (two persons between him and Chandrima) and Jugnu on the Tuesday 20th, so Rishabh is on Friday the 23rd.",
  [ARR], why_others_wrong="The 20th is Jugnu's, the 27th Dheeraj's, and the 9th has no appointment.", seconds=75)
cnt = sum(1 for p in P if wd(M4[p]) == "Friday")
assert cnt == 4
Q("How many of the eight appointments fall on a Friday?", num_word(cnt), ["Five", "Three", "Six"],
  "One Friday is empty", "Fridays: 2 (Prachi), 9 (none), 16 (Chandrima), 23 (Rishabh), 30 (Mahua) — four appointments.",
  [ARR], why_others_wrong="Five counts the empty 9th; Three and Six miscount.", natural=by_num, seconds=70)
ans = at[M4["Farhana"] + 7]
assert ans == "Jugnu"
Q("Whose appointment is exactly one week after Farhana's?", ans, ["Chandrima", "Rishabh", "Dheeraj"],
  "One week later = same weekday, date + 7", "Farhana is on Tuesday 13 October; one week later is Tuesday 20 October: "
  "Jugnu.", [ARR, "13 + 7 = 20 ⇒ Jugnu"], why_others_wrong="Chandrima is three days after Farhana, Rishabh ten days "
                                                          "and Dheeraj two weeks.", seconds=70)
gap = M4["Dheeraj"] - M4["Kshitij"]
assert gap == 21
Q("How many days after Kshitij's appointment is Dheeraj's appointment?", str(gap), ["14", "18", "24"],
  "Difference of dates in the same month", "Kshitij is on the 6th and Dheeraj on the 27th: 27 − 6 = 21 days (exactly "
  "three weeks, both Tuesdays).", [ARR], natural=int, seconds=70)

# ---- M5 Advanced (standalone): birth years from age relations (ages = 2026 − birth year)
P = ["Kanak", "Nimesh", "Ojasvini", "Rudrani", "Sushant"]
YRS = [1990, 1994, 2000, 2008, 2010]
age = lambda y: 2026 - y
conds = [("Kanak is exactly twice as old as Sushant.", ("Kanak", "Sushant"), lambda k, s: age(k) == 2 * age(s)),
         ("Rudrani is exactly 10 years older than Ojasvini.", ("Rudrani", "Ojasvini"),
          lambda r, o: age(r) == age(o) + 10),
         ("Nimesh is older than Rudrani.", ("Nimesh", "Rudrani"), lambda n, r: n < r)]
M5 = unique(P, {p: YRS for p in P}, conds, [P])
assert {p: age(M5[p]) for p in P} == {"Kanak": 36, "Nimesh": 32, "Ojasvini": 16, "Rudrani": 26, "Sushant": 18}
ans = age(M5["Nimesh"]) + 4 + age(M5["Ojasvini"]) + 4
assert ans == 56
mcq(MON, YB, "Advanced", "Five persons Kanak, Nimesh, Ojasvini, Rudrani and Sushant were born in five different years "
    "among 1990, 1994, 2000, 2008 and 2010. Ages are counted in completed years on their birthdays in 2026, so the "
    "ages in 2026 are 36, 32, 26, 18 and 16 in some order.\n" + bullets(conds) + "\n\nWhat will be the sum of the ages "
    "of Nimesh and Ojasvini on their birthdays in 2030?", str(ans), ["48", "52", "60"], "Pairs of ages that fit a ratio "
    "and a difference",
    "Ages: 36, 32, 26, 18, 16. 'Twice as old' fits 36 = 2 × 18 or 32 = 2 × 16; '10 years older' fits 36 − 26 or 26 − 16. "
    "If Kanak 32 and Sushant 16, the 10-year pair must be Rudrani 36 and Ojasvini 26, leaving Nimesh 18 — younger than "
    "Rudrani, which breaks the third clue. So Kanak 36, Sushant 18, Rudrani 26, Ojasvini 16 and Nimesh 32. In 2030 "
    "Nimesh will be 36 and Ojasvini 20: 56.",
    ["Twice: (36, 18) or (32, 16); ten apart: (36, 26) or (26, 16)", "Case Kanak 32: Rudrani 36, Nimesh 18 < Rudrani ✗",
     "Case Kanak 36: Rudrani 26, Ojasvini 16, Nimesh 32 ✓", "2030: 32 + 4 = 36 and 16 + 4 = 20 ⇒ 56"],
    why_others_wrong="48 is their sum in 2026; 52 adds four years only once; 60 uses Kanak's age for Nimesh's.",
    natural=int, seconds=110, verified_by=BRUTE)

# ---- M6 Advanced (standalone): dates across February and March 2027 (non-leap year)
assert WD(2027, 2, 1) == "Monday" and MDAYS[2] == 28
base = dt.date(2027, 2, 23)
jay = base
bip = jay + dt.timedelta(days=7)
vri = bip + dt.timedelta(days=13)
aan = jay - dt.timedelta(days=12)
kus = aan + dt.timedelta(days=45)
assert (bip, vri, aan, kus) == (dt.date(2027, 3, 2), dt.date(2027, 3, 15), dt.date(2027, 2, 11), dt.date(2027, 3, 28))
ans = f"28 March, {kus.strftime('%A')}"
assert ans == "28 March, Sunday"
mcq(MON, DB, "Advanced", "Five persons Aanchal, Bipin, Jayati, Kushagra and Vrishti each have one appointment in "
    "February or March 2027. 2027 is not a leap year, and 1 February 2027 is a Monday.\n"
    "- Jayati's appointment is on 23 February.\n- Bipin's appointment is exactly 7 days after Jayati's.\n"
    "- Vrishti's appointment is 13 days after Bipin's.\n- Aanchal's appointment is 12 days before Jayati's.\n"
    "- Kushagra's appointment is 45 days after Aanchal's.\n\nOn which date and day of the week is Kushagra's "
    "appointment?", ans, ["29 March, Monday", "27 March, Saturday", "25 March, Thursday"],
    "Carry dates across a 28-day February",
    "Aanchal = 23 − 12 = 11 February. Forty-five days later: 17 days take her to 28 February, and 28 more days give 28 "
    "March. 1 March 2027 is a Monday (February has exactly four weeks), so 29 March is a Monday and 28 March a Sunday.",
    ["Aanchal: 11 February", "11 Feb + 17 days = 28 Feb; + 28 days = 28 March", "1 Feb Monday ⇒ 1 Mar Monday (28 days)",
     "28 March = 29 March − 1 ⇒ Sunday"],
    why_others_wrong="29 March treats February as a 29-day month; 27 March and 25 March miscount the days carried "
                     "over into March.", seconds=100, verified_by=RECOMP)

# ================================================================================================ PUZZLES (OTHER)
OTH = "Puzzles (Other)"
sav = {"Shreyas": 4800}
sav["Purvi"] = sav["Shreyas"] + 1200
sav["Mitesh"] = sav["Purvi"] - 2500
sav["Tilak"] = (sav["Mitesh"] + sav["Shreyas"]) // 2
sav["Raghavi"] = 2 * sav["Mitesh"]
ORD = sorted(sav, key=sav.get, reverse=True)
assert ORD == ["Raghavi", "Purvi", "Shreyas", "Tilak", "Mitesh"]
ans = sav[ORD[1]] - sav[ORD[3]]
assert ans == 1850
rp = lambda k: f"₹{k:,}"
mcq(OTH, "Comparison and ordering", "Intermediate",
    "Six friends Mitesh, Purvi, Raghavi, Shreyas, Tilak and Yamika saved different amounts last month.\n"
    "- Shreyas saved ₹4,800, and Purvi saved ₹1,200 more than Shreyas.\n- Mitesh saved ₹2,500 less than Purvi.\n"
    "- Tilak's savings are exactly midway between Mitesh's and Shreyas's.\n- Raghavi saved twice as much as Mitesh.\n"
    "- Yamika saved less than each of the other five.\n\nBy how much do the savings of the second highest saver exceed "
    "those of the fourth highest saver?", rp(ans), [rp(1200), rp(2500), rp(2850)], "Fix every value, then rank",
    "Purvi = 4,800 + 1,200 = 6,000; Mitesh = 6,000 − 2,500 = 3,500; Tilak = (3,500 + 4,800) ÷ 2 = 4,150; Raghavi = "
    "7,000. Order: Raghavi 7,000, Purvi 6,000, Shreyas 4,800, Tilak 4,150, Mitesh 3,500, Yamika. Second (Purvi) − "
    "fourth (Tilak) = 1,850.",
    ["Purvi 6,000; Mitesh 3,500; Tilak 4,150; Raghavi 7,000", "Order: Raghavi > Purvi > Shreyas > Tilak > Mitesh > "
     "Yamika", "6,000 − 4,150 = ₹1,850"],
    why_others_wrong="₹1,200 compares Purvi with Shreyas (third); ₹2,500 compares Purvi with Mitesh (fifth); ₹2,850 "
                     "compares Raghavi with Tilak.", natural=lambda t: int(t[1:].replace(",", "")), seconds=75,
    verified_by=RECOMP)

# ================================================================================================ SYLLOGISM
TWO, FEW, POSS = "Two-statement", "Only a few / Only", "Possibility cases"


def N(*pairs):  # redefined: the seating sections reuse the name N for a seat count
    return {s_: (s_, p_) for s_, p_ in pairs}


# ---- Basic
syl_q("Basic", TWO, N(("kettle", "kettles"), ("pan", "pans"), ("pot", "pots")),
      [("some", "kettle", "pan"), ("all", "pan", "pot")],
      [("some", "pot", "kettle"), ("all", "kettle", "pot")], ONLY_I,
      "Some + All = Some",
      "The kettles that are pans are also pots, so some pots are kettles (I). Kettles outside pans may not be pots, so "
      "'All kettles are pots' is not certain (II).",
      ["Kettle ∩ pan ⊂ pots ⇒ some pots are kettles: I follows", "Kettles outside pans are free ⇒ II not certain"],
      seconds=35)
syl_q("Basic", TWO, N(("anchor", "anchors"), ("oar", "oars"), ("sail", "sails")),
      [("no", "anchor", "oar"), ("some", "oar", "sail")],
      [("somenot", "sail", "anchor"), ("no", "sail", "anchor")], ONLY_I,
      "No + Some (reversed) = Some not",
      "The sails that are oars cannot be anchors, so some sails are not anchors (I). The other sails may be anchors, so "
      "'No sail is an anchor' is not certain (II).",
      ["Sail ∩ oar is non-empty and outside anchors ⇒ I follows", "Sails outside oars may be anchors ⇒ II not certain"],
      seconds=35)
syl_q("Basic", TWO, N(("tent", "tents"), ("hut", "huts"), ("cabin", "cabins")),
      [("all", "tent", "hut"), ("no", "hut", "cabin")],
      [("some", "hut", "tent"), ("somenot", "cabin", "tent")], BOTH,
      "All + No: conversion and exclusion",
      "Every tent is a hut and tents exist, so some huts are tents (I). No cabin is a hut, and every tent is a hut, so "
      "no cabin is a tent; in particular, some cabins are not tents (II).",
      ["All tents are huts ⇒ Some huts are tents: I", "Cabins ∩ huts = ∅ and tents ⊂ huts ⇒ cabins are not tents: II"],
      seconds=35)
syl_q("Basic", TWO, N(("clock", "clocks"), ("watch", "watches"), ("timer", "timers")),
      [("some", "clock", "watch"), ("some", "watch", "timer")],
      [("some", "clock", "timer"), ("no", "clock", "timer")], EITHER,
      "Some + Some gives no definite link; test the complementary pair",
      "Nothing links clocks to timers, so neither conclusion is certain alone. But 'Some clocks are timers' and 'No "
      "clock is a timer' are about the same two terms and exactly one of them must be true: either I or II follows.",
      ["Some + Some ⇒ no definite clock–timer relation", "I and II form a complementary pair",
       "⇒ Either I or II follows"],
      why="'Either' takes the place of 'Both' (four-option rule); 'Neither' ignores the complementary pair.", seconds=35)
syl_q("Basic", TWO, N(("racket", "rackets"), ("bat", "bats"), ("net", "nets")),
      [("all", "racket", "bat"), ("all", "bat", "net")],
      [("all", "net", "racket"), ("some", "net", "bat")], ONLY_II,
      "All + All = All, but it does not reverse",
      "Bats lie inside nets, so some nets are bats (II). Nets may contain much more than rackets, so 'All nets are "
      "rackets' is not certain (I).", ["Rackets ⊂ bats ⊂ nets", "Some nets are bats: II follows",
                                        "All nets are rackets reverses the chain ⇒ I fails"], seconds=30)
syl_q("Basic", TWO, N(("badge", "badges"), ("medal", "medals"), ("trophy", "trophies")),
      [("no", "badge", "medal"), ("all", "trophy", "medal")],
      [("no", "trophy", "badge"), ("somenot", "medal", "badge")], BOTH,
      "All + No (in reverse order) = No",
      "Every trophy is a medal and no medal is a badge, so no trophy is a badge (I). Medals exist and none of them is a "
      "badge, so some medals are not badges (II).",
      ["Trophies ⊂ medals; medals ∩ badges = ∅ ⇒ I", "Medals exist and are all outside badges ⇒ II"], seconds=35)
syl_q("Basic", TWO, N(("bucket", "buckets"), ("tub", "tubs"), ("basin", "basins")),
      [("somenot", "bucket", "tub"), ("all", "tub", "basin")],
      [("some", "bucket", "basin"), ("some", "basin", "tub")], ONLY_II,
      "'Some not' gives nothing about the third term",
      "Tubs exist and all are basins, so some basins are tubs (II). The buckets that are not tubs may or may not be "
      "basins, and no bucket need be a tub at all, so I is not certain.",
      ["All tubs are basins ⇒ Some basins are tubs: II", "Buckets need not touch basins ⇒ I not certain"], seconds=35)
# ---- Intermediate
syl_q("Intermediate", FEW, N(("map", "maps"), ("chart", "charts"), ("graph", "graphs")),
      [("onlyfew", "map", "chart"), ("all", "chart", "graph")],
      [("some", "graph", "map"), ("somenot", "map", "chart")], BOTH,
      "'Only a few A are B' = some A are B + some A are not B",
      "Some maps are charts and every chart is a graph, so some graphs are maps (I). 'Only a few' also states directly "
      "that some maps are not charts (II).",
      ["Map ∩ chart ⊂ graphs ⇒ I", "Only a few ⇒ some maps are not charts ⇒ II"], seconds=45)
syl_q("Intermediate", FEW, N(("poem", "poems"), ("song", "songs"), ("essay", "essays")),
      [("onlyfew", "poem", "song"), ("no", "song", "essay")],
      [("poss_all", "poem", "essay"), ("somenot", "essay", "song")], ONLY_II,
      "A possibility fails when some members are definitely excluded",
      "Some poems are songs, and no song is an essay, so those poems can never be essays: 'all poems being essays' is "
      "impossible (I). Essays exist and none is a song, so some essays are not songs (II).",
      ["Poem ∩ song is non-empty and outside essays ⇒ I impossible", "No song is an essay ⇒ II follows"], seconds=45)
syl_q("Intermediate", POSS, N(("zebra", "zebras"), ("giraffe", "giraffes"), ("rhino", "rhinos")),
      [("all", "zebra", "giraffe"), ("some", "giraffe", "rhino")],
      [("poss_all", "rhino", "zebra"), ("poss_some", "zebra", "rhino")], BOTH,
      "Possibilities that no statement blocks",
      "Rhinos could all lie inside zebras (which are inside giraffes); that still gives 'some giraffes are rhinos', so I "
      "is possible. Some zebras being rhinos is also allowed (II).",
      ["Rhinos ⊂ zebras ⊂ giraffes satisfies both statements ⇒ I possible", "Zebra ∩ rhino is not forbidden ⇒ II "
       "possible"], seconds=45)
syl_q("Intermediate", FEW, N(("spider", "spiders"), ("ant", "ants"), ("bee", "bees")),
      [("only", "spider", "ant"), ("some", "ant", "bee")],
      [("some", "bee", "spider"), ("somenot", "spider", "ant")], ONLY_I,
      "'Only spiders are ants' = All ants are spiders",
      "Every ant is a spider, so the bees that are ants are spiders: some bees are spiders (I). Spiders and ants may be "
      "exactly the same group, so 'some spiders are not ants' is not certain (II).",
      ["Only spiders are ants ⇒ ants ⊂ spiders", "Ant ∩ bee ⊂ spiders ⇒ I", "Spiders may equal ants ⇒ II not certain"],
      why="Reading 'Only spiders are ants' as 'All spiders are ants' would wrongly make II false for a different reason "
          "and could hide why I holds.", seconds=50)
syl_q("Intermediate", POSS, N(("drill", "drills"), ("saw", "saws"), ("chisel", "chisels")),
      [("no", "drill", "saw"), ("some", "saw", "chisel")],
      [("poss_all", "chisel", "drill"), ("somenot", "chisel", "drill")], ONLY_II,
      "Members that are definitely excluded block 'all'",
      "Some chisels are saws, and no saw is a drill, so those chisels are not drills (II) and all chisels can never be "
      "drills (I is impossible).", ["Chisel ∩ saw is non-empty and outside drills", "⇒ II follows; I impossible"],
      seconds=45)
syl_q("Intermediate", TWO, N(("helmet", "helmets"), ("visor", "visors"), ("mask", "masks"), ("goggle", "goggles")),
      [("some", "helmet", "visor"), ("all", "visor", "mask"), ("no", "mask", "goggle")],
      [("somenot", "helmet", "goggle"), ("some", "mask", "helmet")], BOTH,
      "A chain of three statements",
      "The helmets that are visors are masks (so some masks are helmets, II), and masks are never goggles, so those "
      "helmets are not goggles (I).", ["Helmet ∩ visor ⊂ masks ⇒ II", "Masks ∩ goggles = ∅ ⇒ those helmets are not "
                                                                       "goggles ⇒ I"], seconds=50)
syl_q("Intermediate", FEW, N(("pillar", "pillars"), ("arch", "arches"), ("dome", "domes")),
      [("onlyfew", "pillar", "arch"), ("onlyfew", "arch", "dome")],
      [("some", "pillar", "arch"), ("poss_all", "arch", "dome")], ONLY_I,
      "'Only a few' rules out 'all'",
      "'Only a few pillars are arches' includes 'some pillars are arches' (I). 'Only a few arches are domes' means some "
      "arches are not domes, so all arches being domes is impossible (II).",
      ["Only a few pillars are arches ⇒ some are ⇒ I", "Some arches are not domes ⇒ II impossible"], seconds=45)
syl_q("Intermediate", POSS, N(("wagon", "wagons"), ("sledge", "sledges"), ("buggy", "buggies")),
      [("all", "wagon", "sledge"), ("no", "sledge", "buggy")],
      [("poss_some", "buggy", "wagon"), ("poss_all", "sledge", "wagon")], ONLY_II,
      "Subset of an excluded set is excluded too",
      "Wagons lie inside sledges and sledges never meet buggies, so no buggy can be a wagon (I impossible). Sledges and "
      "wagons may be the same group, so all sledges being wagons is possible (II).",
      ["Wagons ⊂ sledges; sledges ∩ buggies = ∅ ⇒ I impossible", "Wagons = sledges is allowed ⇒ II possible"],
      seconds=45)
syl_q("Intermediate", TWO, N(("pebble", "pebbles"), ("boulder", "boulders"), ("crystal", "crystals"),
                             ("fossil", "fossils")),
      [("some", "pebble", "boulder"), ("no", "boulder", "crystal"), ("all", "crystal", "fossil")],
      [("somenot", "fossil", "boulder"), ("somenot", "pebble", "crystal")], BOTH,
      "Two 'some not' results from one 'No' statement",
      "Crystals exist, are all fossils and are never boulders, so some fossils are not boulders (I). The pebbles that are "
      "boulders cannot be crystals, so some pebbles are not crystals (II).",
      ["Crystals ⊂ fossils, crystals ∩ boulders = ∅ ⇒ I", "Pebble ∩ boulder is outside crystals ⇒ II"], seconds=50)
syl_q("Intermediate", FEW, N(("carpet", "carpets"), ("rug", "rugs"), ("mat", "mats")),
      [("onlyfew", "carpet", "rug"), ("some", "rug", "mat")],
      [("some", "carpet", "mat"), ("no", "carpet", "mat")], EITHER,
      "No definite carpet–mat link; check the complementary pair",
      "Carpets and mats are linked only through rugs by 'some', so neither conclusion is certain alone. The two "
      "conclusions are 'Some' and 'No' about the same terms, so exactly one is true: either I or II follows.",
      ["Only a few + Some ⇒ no definite carpet–mat relation", "I and II are complementary ⇒ Either I or II"],
      why="'Either' replaces 'Both' (four-option rule).", seconds=45)
syl_q("Intermediate", POSS, N(("lemon", "lemons"), ("lime", "limes"), ("plum", "plums")),
      [("some", "lemon", "lime"), ("all", "lime", "plum")],
      [("poss_all", "plum", "lemon"), ("somenot", "plum", "lemon")], ONLY_I,
      "A possibility versus a definite 'some not'",
      "Plums could all be lemons (then limes are lemons too, and some lemons are limes still holds), so I is possible. "
      "For the same reason 'some plums are not lemons' is not certain (II).",
      ["Plums ⊂ lemons is consistent with both statements ⇒ I possible", "That same case makes II false ⇒ II not "
                                                                          "certain"], seconds=45)
# ---- Advanced
syl_q("Advanced", POSS, N(("jug", "jugs"), ("mug", "mugs"), ("tumbler", "tumblers"), ("keg", "kegs")),
      [("some", "jug", "mug"), ("onlyfew", "mug", "tumbler"), ("all", "tumbler", "keg")],
      [("some", "keg", "mug"), ("poss_all", "mug", "keg")], BOTH,
      "Room outside the 'only a few' part",
      "Some mugs are tumblers and every tumbler is a keg, so some kegs are mugs (I). The mugs that are not tumblers can "
      "still lie in the part of kegs outside tumblers, so all mugs being kegs is possible (II).",
      ["Mug ∩ tumbler ⊂ kegs ⇒ I", "Mugs outside tumblers may sit in kegs ⇒ II possible"], seconds=60)
syl_q("Advanced", POSS, N(("violet", "violets"), ("orchid", "orchids"), ("fern", "ferns"), ("cactus", "cacti")),
      [("all", "violet", "orchid"), ("no", "orchid", "fern"), ("some", "fern", "cactus")],
      [("somenot", "cactus", "violet"), ("poss_some", "fern", "violet")], ONLY_I,
      "An exclusion passed down to a subset",
      "The cacti that are ferns are not orchids, and every violet is an orchid, so those cacti are not violets (I). "
      "Violets lie inside orchids, which never meet ferns, so no fern can be a violet (II impossible).",
      ["Cactus ∩ fern is outside orchids ⊃ violets ⇒ I", "Violets ⊂ orchids, orchids ∩ ferns = ∅ ⇒ II impossible"],
      seconds=60)
syl_q("Advanced", FEW, N(("crate", "crates"), ("sack", "sacks"), ("bin", "bins"), ("tray", "trays")),
      [("no", "crate", "sack"), ("onlyfew", "sack", "bin"), ("all", "bin", "tray")],
      [("somenot", "tray", "crate"), ("no", "tray", "crate")], ONLY_I,
      "A definite 'some not' and an unsupported 'no'",
      "Some sacks are bins, so some trays are sacks; those trays are not crates (no crate is a sack): some trays are not "
      "crates (I). Crates may still be trays (for example, crates that are bins), so II is not certain.",
      ["Sack ∩ bin ⊂ trays and outside crates ⇒ I", "Crates can be trays outside sacks ⇒ II not certain"], seconds=60)
syl_q("Advanced", FEW, N(("stick", "sticks"), ("cane", "canes"), ("wand", "wands"), ("staff", "staffs")),
      [("only", "stick", "cane"), ("some", "cane", "wand"), ("no", "wand", "staff")],
      [("somenot", "stick", "staff"), ("poss_all", "cane", "staff")], ONLY_I,
      "'Only sticks are canes' = All canes are sticks",
      "Every cane is a stick; the canes that are wands are sticks and are not staffs, so some sticks are not staffs (I). "
      "Those same canes can never be staffs, so all canes being staffs is impossible (II).",
      ["Canes ⊂ sticks; cane ∩ wand is outside staffs ⇒ I", "Some canes are definitely not staffs ⇒ II impossible"],
      seconds=65)
syl_q("Advanced", FEW, N(("quill", "quills"), ("ink", "inks"), ("paper", "papers"), ("scroll", "scrolls")),
      [("some", "quill", "ink"), ("all", "ink", "paper"), ("onlyfew", "paper", "scroll")],
      [("some", "quill", "scroll"), ("poss_all", "ink", "scroll")], ONLY_II,
      "'Only a few' blocks 'all' only for its own subject",
      "Quills reach scrolls only through papers, and the paper–scroll overlap may avoid the quills, so I is not certain. "
      "'Only a few papers are scrolls' needs some papers outside scrolls, but those can be papers that are not inks, so "
      "all inks being scrolls is possible (II).",
      ["Quill ∩ ink ⊂ papers; papers ∩ scrolls may miss them ⇒ I not certain",
       "Inks ⊂ scrolls with other papers outside scrolls ⇒ II possible"], seconds=65)
syl_q("Advanced", FEW, N(("compass", "compasses"), ("sextant", "sextants"), ("telescope", "telescopes"),
                         ("binocular", "binoculars")),
      [("no", "compass", "sextant"), ("all", "telescope", "sextant"), ("onlyfew", "telescope", "binocular")],
      [("somenot", "binocular", "compass"), ("no", "telescope", "compass")], BOTH,
      "Exclusion carried down to subsets",
      "Every telescope is a sextant and no sextant is a compass, so no telescope is a compass (II). Some telescopes are "
      "binoculars; those binoculars are telescopes and hence not compasses (I).",
      ["Telescopes ⊂ sextants, sextants ∩ compasses = ∅ ⇒ II", "Binocular ∩ telescope is outside compasses ⇒ I"],
      seconds=60)
syl_q("Advanced", TWO, N(("meadow", "meadows"), ("field", "fields"), ("farm", "farms"), ("orchard", "orchards")),
      [("some", "meadow", "field"), ("somenot", "field", "farm"), ("all", "farm", "orchard")],
      [("somenot", "meadow", "farm"), ("some", "orchard", "field")], NEITHER,
      "'Some not' in the middle breaks the chain",
      "All meadows could be farms (the fields that are not farms may lie outside meadows), so I is not certain. Farms "
      "are orchards, but the fields may all lie outside farms and orchards, so II is not certain either.",
      ["Meadows ⊂ farms is possible ⇒ I not certain", "Fields may avoid orchards ⇒ II not certain"], seconds=60)
syl_q("Advanced", FEW, N(("cottage", "cottages"), ("villa", "villas"), ("mansion", "mansions"), ("castle", "castles")),
      [("onlyfew", "cottage", "villa"), ("all", "villa", "mansion"), ("no", "mansion", "castle")],
      [("somenot", "mansion", "cottage"), ("all", "mansion", "cottage")], EITHER,
      "A complementary pair on the same two terms",
      "Mansions contain the villas, some of which are cottages; whether every mansion is a cottage is open, so neither "
      "conclusion is certain alone. 'Some mansions are not cottages' and 'All mansions are cottages' cannot both be "
      "false, and cannot both be true: either I or II follows.",
      ["No statement fixes mansions inside or outside cottages", "I and II are complementary ⇒ Either I or II"],
      why="'Either' replaces 'Both' (four-option rule); 'Neither' ignores the complementary pair.", seconds=65)

# ================================================================================================ INEQUALITY
DIRECT, CODED = "Direct inequality", "Coded inequality"
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


def chain_text(chain, conc):
    return "Statement: " + chain, [chain], [parse_chain(c)[0] for c in conc], conc


# ---- Basic
s, ch, cc, ct = chain_text("P < Y ≤ N = H > C ≥ W", ["Y < C", "H > W"])
s = ("Six quantities are related as shown in the single chain P < Y ≤ N = H > C ≥ W. Assuming the chain to be "
     "true, decide which of the two conclusions below is/are definitely true.")
ineq_q3("Basic", DIRECT, s, ch, cc, ct, ONLY_II,
        "Y and C lie on opposite sides of the turn at H (Y ≤ N = H > C), so Y < C is not certain. H > C ≥ W gives "
        "H > W.", ["I: Y ≤ N = H > C: reversal at H → no relation", "II: H > C ≥ W → H > W, true"], seconds=30)
s, ch, cc, ct = chain_text("D ≥ G = M ≥ S < B ≤ J", ["D ≥ S", "J > M"])
s = ("Given relation: D ≥ G = M ≥ S < B ≤ J (every sign in it holds). Using only this relation, test the "
     "two conclusions that follow.")
ineq_q3("Basic", DIRECT, s, ch, cc, ct, ONLY_I,
        "D ≥ G = M ≥ S gives D ≥ S. M and J lie on opposite sides of the turn at S (M ≥ S < B), so J > M is not "
        "certain.", ["I: D ≥ G = M ≥ S → D ≥ S, true", "II: M ≥ S < B ≤ J: reversal at S → no relation"], seconds=30)

# ---- Intermediate: direct, several statements
s, ch, cc, ct = ("Statement: F > K; K ≥ R; T < R; T = V; W ≥ F", ["F > K", "K ≥ R", "T < R", "T = V", "W ≥ F"],
                 [("K", ">", "R"), ("K", "=", "R")], ["K > R", "K = R"])
ineq_q3("Intermediate", DIRECT, s, ch, cc, ct, EITHER,
        "Combined: W ≥ F > K ≥ R > T = V. Only K ≥ R is known, so K > R and K = R are each uncertain, but one of them "
        "must hold: either I or II is true.",
        ["Chain: W ≥ F > K ≥ R > T = V", "K ≥ R ⇒ (K > R) or (K = R)", "Either I or II"],
        why="'Either' replaces 'Both' (four-option rule).", concept="Complementary pair from a '≥' sign", seconds=50)
s, ch, cc, ct = ("Statement: A ≤ M; M < X; X ≥ J; J > Q; Q = E", ["A ≤ M", "M < X", "X ≥ J", "J > Q", "Q = E"],
                 [("A", "<", "J"), ("M", ">", "E")], ["A < J", "M > E"])
ineq_q3("Intermediate", DIRECT, s, ch, cc, ct, NEITHER,
        "Combined: A ≤ M < X ≥ J > Q = E. Both conclusions compare a term left of X with a term right of X, and the "
        "direction turns at X, so neither can be established.",
        ["Chain: A ≤ M < X ≥ J > Q = E", "I: A … X ≥ J: reversal at X → no relation",
         "II: M < X ≥ … E: reversal at X → no relation"], seconds=50)
s, ch, cc, ct = ("Statement: H ≥ C; C = U; U > B; B ≥ Y; N > H", ["H ≥ C", "C = U", "U > B", "B ≥ Y", "N > H"],
                 [("N", ">", "Y"), ("H", ">", "B")], ["N > Y", "H > B"])
ineq_q3("Intermediate", DIRECT, s, ch, cc, ct, BOTH,
        "Combined: N > H ≥ C = U > B ≥ Y. From N to Y every sign points the same way with strict signs on the path, "
        "so N > Y. H ≥ C = U > B gives H > B.",
        ["Chain: N > H ≥ C = U > B ≥ Y", "I: N > Y, true", "II: H > B, true"], seconds=50)
s, ch, cc, ct = ("Statement: Z < O; O ≤ G; G = D; D > K; K ≥ S", ["Z < O", "O ≤ G", "G = D", "D > K", "K ≥ S"],
                 [("Z", "<", "K"), ("S", "<", "D")], ["Z < K", "S < D"])
ineq_q3("Intermediate", DIRECT, s, ch, cc, ct, ONLY_II,
        "Combined: Z < O ≤ G = D > K ≥ S. Z and K are on opposite sides of the turn at D, so Z < K is not certain. "
        "D > K ≥ S gives S < D.",
        ["Chain: Z < O ≤ G = D > K ≥ S", "I: reversal at D → no relation", "II: D > K ≥ S → S < D, true"], seconds=50)

# ---- Intermediate: coded set
CODE_P = {"∂": ">", "∇": "<", "∫": "=", "∑": "≥", "∏": "≤"}
CODE_P_TXT = ("In the questions of this set, the symbols ∂, ∇, ∫, ∑ and ∏ are used with these meanings:\n"
              "'A ∂ B' means 'A is greater than B'; 'A ∇ B' means 'A is smaller than B'; 'A ∫ B' means 'A is equal "
              "to B'; 'A ∑ B' means 'A is either greater than or equal to B'; 'A ∏ B' means 'A is either smaller than "
              "or equal to B'.\nAssuming the statements to be true, find which of the conclusions I and II is/are "
              "definitely true.")
SID_P = stimulus("passage", "Five calculus-style inequality symbols", CODE_P_TXT, None,
                 "Decode: ∂ means >, ∇ means <, ∫ means =, ∑ means ≥ and ∏ means ≤. Rewrite every statement with the "
                 "ordinary signs, join them into one chain, and test each conclusion along the chain.")
CCP = "Decoding symbols, then reading the chain"


def coded_p(stmts, concs):
    return ("Statements: " + ", ".join(stmts), [decode(x, CODE_P) for x in stmts],
            [parse_chain(decode(c, CODE_P))[0] for c in concs], concs)


s, ch, cc, ct = coded_p(["L ∑ P", "P ∂ G", "G ∫ F", "F ∏ X"], ["L ∂ F", "X ∂ P"])
ineq_q3("Intermediate", CODED, s, ch, cc, ct, ONLY_I,
        "Decoded: L ≥ P > G = F ≤ X. L > F follows (I). X and P lie on opposite sides of the turn at F, so X > P is not "
        "certain (II).", ["Decode: L ≥ P, P > G, G = F, F ≤ X", "Chain: L ≥ P > G = F ≤ X", "I: L > F, true",
                          "II: X > P: reversal at F → not certain"], concept=CCP, stimulus=SID_P, seconds=55)
s, ch, cc, ct = coded_p(["B ∇ N", "N ∫ T", "T ∑ K", "K ∂ U"], ["T ∂ U", "U ∇ N"])
ineq_q3("Intermediate", CODED, s, ch, cc, ct, BOTH,
        "Decoded: B < N = T ≥ K > U. T ≥ K > U gives T > U (I), and U < K ≤ T = N gives U < N (II).",
        ["Decode: B < N, N = T, T ≥ K, K > U", "Chain: B < N = T ≥ K > U", "I: T > U, true", "II: U < N, true"],
        concept=CCP, stimulus=SID_P, seconds=55)
s, ch, cc, ct = coded_p(["E ∏ R", "R ∇ H", "H ∑ O", "O ∫ I"], ["E ∇ I", "I ∂ R"])
ineq_q3("Intermediate", CODED, s, ch, cc, ct, NEITHER,
        "Decoded: E ≤ R < H ≥ O = I. Both conclusions compare a term left of H with a term right of H, across the turn "
        "at H, so neither is certain.",
        ["Decode: E ≤ R, R < H, H ≥ O, O = I", "Chain: E ≤ R < H ≥ O = I", "I: E < I: reversal at H",
         "II: I > R: reversal at H"], concept=CCP, stimulus=SID_P, seconds=55)
s, ch, cc, ct = coded_p(["S ∑ A", "A ∫ V", "V ∑ M", "M ∂ Q"], ["S ∂ M", "S ∫ M"])
ineq_q3("Intermediate", CODED, s, ch, cc, ct, EITHER,
        "Decoded: S ≥ A = V ≥ M > Q. Only S ≥ M is known, so S > M and S = M are each uncertain, but one of them must "
        "be true: either I or II.",
        ["Decode: S ≥ A, A = V, V ≥ M, M > Q", "S ≥ A = V ≥ M ⇒ S ≥ M", "S > M or S = M ⇒ Either I or II"],
        why="'Either' replaces 'Both' (four-option rule).", concept=CCP, stimulus=SID_P, seconds=55)
s, ch, cc, ct = coded_p(["G ∂ H", "J ∑ H", "J ∏ K", "L ∇ K"], ["G ∂ K", "K ∑ H"])
ineq_q3("Intermediate", CODED, s, ch, cc, ct, ONLY_II,
        "Decoded: G > H ≤ J ≤ K > L. G and K lie on opposite sides of the turn at H, so G > K is not certain. "
        "H ≤ J ≤ K gives K ≥ H (II).",
        ["Decode: G > H, J ≥ H, J ≤ K, L < K", "Chain: G > H ≤ J ≤ K > L", "I: reversal at H → not certain",
         "II: K ≥ H, true"], concept=CCP, stimulus=SID_P, seconds=55)

# ---- Advanced
s, ch, cc, ct = ("Statement: J ≥ W; W > E; E ≥ Y; P = Y; P ≥ C; D > J",
                 ["J ≥ W", "W > E", "E ≥ Y", "P = Y", "P ≥ C", "D > J"], [("D", ">", "C"), ("E", ">", "C")],
                 ["D > C", "E > C"])
ineq_q("Advanced", DIRECT, s, ch, cc, ct, ONLY_I,
        "Combined: D > J ≥ W > E ≥ Y = P ≥ C. From D to C every sign points the same way and there is a strict sign, "
        "so D > C (I). From E to C the signs are only ≥, = and ≥, so E ≥ C — E > C is not certain (II).",
        ["Rewrite as one chain: D > J ≥ W > E ≥ Y = P ≥ C", "I: strict signs on the path ⇒ D > C, true",
         "II: E ≥ Y = P ≥ C has no strict sign ⇒ only E ≥ C"],
        why="A path made only of ≥ and = never proves a strict '>'.", concept="Combining six statements into one chain",
        seconds=70)
CH = ["K < M ≤ A", "A = Z", "Z > T ≥ O"]
OPTS = [("K", "<", "Z"), ("M", ">", "T"), ("O", "<", "M"), ("T", "<", "K")]
rels = [r for c in CH for r in parse_chain(c)]
vs = sorted({x for a_, _, b_ in rels for x in (a_, b_)})
sats = [dict(zip(vs, vals)) for vals in itertools.product(range(len(vs) + 2), repeat=len(vs))
        if all(REL[o](dict(zip(vs, vals))[a_], dict(zip(vs, vals))[b_]) for a_, o, b_ in rels)]
always = [c for c in OPTS if all(REL[c[1]](v[c[0]], v[c[2]]) for v in sats)]
assert always == [OPTS[0]]
mcq(INQ, DIRECT, "Advanced",
    "Statement: K < M ≤ A; A = Z; Z > T ≥ O\n\nWhich of the following conclusions is definitely true?",
    " ".join(OPTS[0]), [" ".join(c) for c in OPTS[1:]], "Definitely true = holds in every case the chain allows",
    "Combined: K < M ≤ A = Z > T ≥ O. K < M ≤ A = Z gives K < Z in every case. M, K and T, O lie on opposite sides of "
    "the turn at Z, so M > T, O < M and T < K can each be true or false.",
    ["Chain: K < M ≤ A = Z > T ≥ O", "K < Z: same direction with a strict sign ⇒ definitely true",
     "M > T, O < M, T < K: compare across the turn at Z ⇒ not determined"],
    why_others_wrong="Each of the other three relations crosses the turn at Z, so it may or may not hold.", seconds=70,
    verified_by=EXHAUST)

# ================================================================================================ BLOOD RELATIONS
DRB, CDB, FPZ = "Direct relation", "Coded blood relation", "Family puzzle"
F = Family().add("Oh", "M").add("O", "F").marry("Oh", "O").add("N", "F", "Oh", "O").add("P", "M", "Oh", "O")
F.add("M", "M").marry("M", "N")
ans = F.rel("M", "P")
assert ans == "brother-in-law"
mcq(BLD, DRB, "Basic", "M is the husband of N. N is the only daughter of O. P is the son of O. How is M related to P?",
    cap(ans), ["Brother", "Father-in-law", "Uncle"], "A sister's husband is a brother-in-law",
    "N and P are both children of O, so N is P's sister. M is N's husband, so M is P's brother-in-law.",
    ["N (daughter of O) and P (son of O) are siblings", "M = husband of P's sister ⇒ brother-in-law"],
    why_others_wrong="M shares no parent with P; he is in P's generation, so he is neither P's father-in-law nor his "
                     "uncle.", seconds=30, verified_by=RECOMP)
CODE_R = {"◇": "father", "○": "daughter", "△": "brother", "▽": "wife"}
F = Family().add("Nf", "M").add("Nm", "F").marry("Nf", "Nm").add("M", "F", "Nf", "Nm").add("L", "M", "Nf", "Nm")
F.add("K", "F").marry("K", "L")
F.check(coded_facts("K ▽ L △ M", CODE_R) + [("M", "daughter", "Nm")])
ans = F.rel("K", "Nm")
assert ans == "daughter-in-law" and F.rel("K", "Nf") == "daughter-in-law"
mcq(BLD, CDB, "Intermediate",
    "In a certain code:\n'A ◇ B' means 'A is the father of B';\n'A ○ B' means 'A is the daughter of B';\n'A △ B' means "
    "'A is the brother of B';\n'A ▽ B' means 'A is the wife of B'.\n\nIf 'K ▽ L △ M ○ N', how is K related to N?",
    cap(ans), ["Daughter", "Sister-in-law", "Mother"], "Decode left to right and track generations",
    "K is L's wife. L is M's brother, and M is N's daughter, so L is N's son. K, the wife of N's son, is N's "
    "daughter-in-law (whether N is the father or the mother).",
    ["K ▽ L: K is L's wife", "L △ M and M ○ N: L is a child (son) of N", "Wife of one's son ⇒ daughter-in-law"],
    why_others_wrong="Daughter is M's relation to N; K is M's sister-in-law, not N's; Mother puts K a generation too "
                     "high.", seconds=55, verified_by=RECOMP)
F = Family().add("Devendra", "M").add("Kamini", "F").marry("Devendra", "Kamini")
F.add("Lalit", "M", "Devendra", "Kamini").add("Mohini", "F", "Devendra", "Kamini")
F.add("Neha", "F").marry("Lalit", "Neha").add("Ojas", "M", "Lalit", "Neha")
F.add("Prem", "M").marry("Mohini", "Prem").add("Riya", "F", "Prem", "Mohini")
F.check([("Neha", "daughter-in-law", "Kamini"), ("Ojas", "son", "Neha"), ("Mohini", "daughter", "Devendra")])
ans = F.rel("Prem", "Ojas")
assert ans == "uncle" and F.rel("Riya", "Ojas") == "cousin"
mcq(BLD, FPZ, "Advanced",
    "Kamini has exactly two children, one son and one daughter. Neha is Kamini's daughter-in-law, and Ojas is Neha's "
    "son. Devendra is Kamini's husband. Riya's mother is Devendra's only daughter, and Prem is the husband of Riya's "
    "mother. Each person mentioned has only one spouse. How is Prem related to Ojas?",
    "Uncle (husband of his father's sister)", ["Father", "Brother-in-law", "Grandfather"],
    "Identify each spouse first, then the generations",
    "Neha is Kamini's daughter-in-law, so she is the wife of Kamini's only son; Ojas's father is therefore Kamini's son. "
    "Devendra's only daughter is Kamini's daughter (Devendra is Kamini's husband), i.e. the sister of Ojas's father. "
    "Prem is her husband, so Prem is the husband of Ojas's paternal aunt: his uncle.",
    ["Daughter-in-law of Kamini ⇒ wife of Kamini's only son ⇒ Ojas's father = Kamini's son",
     "Riya's mother = Kamini's daughter = sister of Ojas's father", "Prem = her husband ⇒ Ojas's uncle"],
    why_others_wrong="Prem is Riya's father, not Ojas's; he is the brother-in-law of Ojas's father, not of Ojas; he is "
                     "in the parents' generation, not the grandparents'.", seconds=80, verified_by=RECOMP)

# ================================================================================================ DIRECTION SENSE
DD, PP, SH_ = "Distance and direction", "Point-to-point", "Shadow-based"
x, y = walk("W", [(None, 9), ("R", 12), ("R", 4)])
assert (x, y) == (-5, 12)
mcq(DIR, DD, "Basic",
    "Kavya walks 9 m towards the west. She then turns right and walks 12 m, and then turns right again and walks 4 m. "
    "How far is she now from her starting point, and in which direction?", f"{dist(x, y)} m, {compass(x, y)}",
    ["13 m, North-East", "15 m, North-West", "12 m, North"], "Net displacement",
    "Right from west is north, and right from north is east. She ends 9 − 4 = 5 m west and 12 m north of the start: "
    "√(25 + 144) = 13 m, towards the north-west.",
    ["9 m west → (−9, 0)", "Right = north; 12 m → (−9, 12)", "Right = east; 4 m → (−5, 12)", "√(5² + 12²) = 13 m, NW"],
    why_others_wrong="North-East forgets that she is still 5 m west; 15 m uses 9 and 12 as the legs; 12 m, North ignores "
                     "the west part.", seconds=40, verified_by=RECOMP)
Pp = (0, 0)
Qp = (Pp[0] + 7, Pp[1])
Rp = (Qp[0], Qp[1] + 7)
Sp = (Rp[0] - 3, Rp[1])
assert Sp == (4, 7)
mcq(DIR, PP, "Basic",
    "Point Q is 7 m east of point P. Point R is 7 m north of point Q. Point S is 3 m west of point R. In which direction "
    "is point S with respect to point P?", compass(*Sp), ["North-West", "North", "East"], "Place every point on a grid",
    "Take P at (0, 0). Q = (7, 0), R = (7, 7) and S = (4, 7). S is 4 m east and 7 m north of P: north-east.",
    ["P (0, 0) → Q (7, 0) → R (7, 7) → S (4, 7)", "S − P = (+4, +7) ⇒ North-East"],
    why_others_wrong="North-West would need S to be west of P; North and East ignore one of the two components.",
    seconds=40, verified_by=RECOMP)
face = "W"
face2 = turn(face, "L")
assert NAME[face2] == "South"
mcq(DIR, SH_, "Basic",
    "Soon after sunrise, Mehul stood in an open field with his back to the sun. He then turned 90° anticlockwise. Which "
    "direction is he facing now?", NAME[face2], ["North", "East", "West"], "The morning sun is in the east",
    "After sunrise the sun is in the east. With his back to the sun, Mehul faces west. A 90° anticlockwise turn (a left "
    "turn) from west gives south.", ["Morning sun in the east ⇒ back to the sun = facing west",
                                      "Anticlockwise 90° from west ⇒ south"],
    why_others_wrong="North is a clockwise turn from west; East would mean facing the sun; West ignores the turn.",
    seconds=35, verified_by=RECOMP)
ANG = {"N": 0, "NE": 45, "E": 90, "SE": 135, "S": 180, "SW": 225, "W": 270, "NW": 315}
ANAME = {"N": "North", "NE": "North-East", "E": "East", "SE": "South-East", "S": "South", "SW": "South-West",
         "W": "West", "NW": "North-West"}
fin = (ANG["SW"] - 135 + 270) % 360
ans = ANAME[next(k for k, v in ANG.items() if v == fin)]
assert ans == "North"
mcq(DIR, DD, "Basic", "A boy is facing south-west. He turns 135° anticlockwise and then 270° clockwise. Which direction "
    "is he facing now?", ans, ["South", "East", "North-West"], "Net turn = clockwise − anticlockwise",
    "Net turn: 270° clockwise − 135° anticlockwise = 135° clockwise. South-west is 225°; 225° + 135° = 360°: north.",
    ["Net: 135° clockwise", "225° + 135° = 360° = North"],
    why_others_wrong="South turns the net amount the wrong way; East stops after the first turn; North-West adds only "
                     "90°.", seconds=40, verified_by=RECOMP)
x, y = walk("N", [(None, 20), ("R", 21)])
assert dist(x, y) == "29"
mcq(DIR, DD, "Basic", "A car travels 20 km towards the north, then turns right and travels 21 km. How far is the car "
    "from its starting point, and in which direction?", f"{dist(x, y)} km, {compass(x, y)}",
    ["41 km, North-East", "29 km, North-West", "21 km, East"], "A 20-21-29 right triangle",
    "Right from north is east. The car is 21 km east and 20 km north of the start: √(400 + 441) = √841 = 29 km, "
    "towards the north-east.", ["North 20 → (0, 20)", "Right = east 21 → (21, 20)", "√(20² + 21²) = 29 km, NE"],
    why_others_wrong="41 km adds the legs; North-West takes the turn as a left turn; 21 km, East ignores the north leg.",
    seconds=40, verified_by=RECOMP)
ira = walk("N", [(None, 6), ("R", 8)])
jai = walk("S", [(None, 6), ("L", 8)])
assert ira == (8, 6) and jai == (8, -6)
dx, dy = ira[0] - jai[0], ira[1] - jai[1]
mcq(DIR, PP, "Intermediate",
    "Ira and Jai start from the same point. Ira walks 6 km north, turns right and walks 8 km. Jai walks 6 km south, "
    "turns left and walks 8 km. How far apart are they now, and in which direction is Ira from Jai?",
    f"{dist(dx, dy)} km, {compass(dx, dy)}", ["16 km, North-East", "12 km, South", "20 km, North"],
    "Put both end points on one grid",
    "Ira: north 6, then right (east) 8 ⇒ (8, 6). Jai: south 6, then left (from south, left is east) 8 ⇒ (8, −6). Both are "
    "8 km east of the start, so Ira is exactly 12 km north of Jai.",
    ["Ira (8, 6)", "Jai: facing south, left = east ⇒ (8, −6)", "Difference (0, 12) ⇒ 12 km, North"],
    why_others_wrong="16 km, North-East takes Jai's left as west; 12 km, South is Jai's direction from Ira; 20 km adds "
                     "all the legs.", seconds=60, verified_by=RECOMP)

# ---- Advanced set: coded directions between seven points
CODE_D = {"α": (6, 0), "β": (0, 8), "γ": (-6, 0), "δ": (0, -8)}
PT = {"L": (0, 0)}
for a_, op_, b_ in [("K", "α", "L"), ("M", "β", "K"), ("N", "γ", "M"), ("O", "δ", "L"), ("T", "γ", "O")]:
    PT[a_] = (PT[b_][0] + CODE_D[op_][0], PT[b_][1] + CODE_D[op_][1])
assert PT == {"L": (0, 0), "K": (6, 0), "M": (6, 8), "N": (0, 8), "O": (0, -8), "T": (-6, -8)}
ARR = "Coordinates (east, north) in metres with L at (0, 0): " + ", ".join(f"{k} {v}" for k, v in PT.items())
sid = stimulus("puzzle", "Coded directions between six points",
               "In a certain code:\n'P α Q' means 'P is 6 m to the east of Q';\n'P β Q' means 'P is 8 m to the north "
               "of Q';\n'P γ Q' means 'P is 6 m to the west of Q';\n'P δ Q' means 'P is 8 m to the south of Q'.\n\n"
               "The following are true: K α L, M β K, N γ M, O δ L, T γ O.", None,
               "Put L at (0, 0), with east and north positive.\nK α L: K = (6, 0). M β K: M = (6, 8). N γ M: N = (0, 8). "
               "O δ L: O = (0, −8). T γ O: T = (−6, −8).")
DQ = lambda sub, text, correct, wrongs, concept, expl, steps, **kw: mcq(
    DIR, sub, "Advanced", text, correct, wrongs, concept, expl, steps, stimulus=sid, verified_by=RECOMP, **kw)
dx, dy = PT["M"]
DQ(PP, "What is the straight-line distance between L and M, and in which direction is M from L?",
   f"{dist(dx, dy)} m, {compass(dx, dy)}", ["14 m, North-East", "10 m, North-West", "8 m, North"],
   "Decode, then use a 6-8-10 triangle", "M is 6 m east and 8 m north of L: √(36 + 64) = 10 m, north-east.",
   [ARR, "M − L = (6, 8)", "√(6² + 8²) = 10 m, North-East"],
   why_others_wrong="14 m adds the legs; North-West mistakes α for west; 8 m, North ignores the east part.", seconds=75)
dx, dy = PT["T"][0] - PT["M"][0], PT["T"][1] - PT["M"][1]
DQ(PP, "How far is point T from point M, and in which direction is T from M?", f"{dist(dx, dy)} m, {compass(dx, dy)}",
   ["20 m, North-East", "28 m, South-West", "16 m, South"], "Difference of two decoded positions",
   "T = (−6, −8) and M = (6, 8). T is 12 m west and 16 m south of M: √(144 + 256) = 20 m, towards the south-west.",
   [ARR, "T − M = (−12, −16)", "√(12² + 16²) = 20 m, South-West"],
   why_others_wrong="North-East is M's direction from T; 28 m adds the legs; 16 m, South ignores the west part.",
   seconds=80)
mid_ = ((PT["N"][0] + PT["O"][0]) / 2, (PT["N"][1] + PT["O"][1]) / 2)
ans = next(k for k, v in PT.items() if v == mid_)
assert ans == "L"
DQ(PP, "Which point lies exactly midway between N and O?", ans, ["K", "M", "T"], "Midpoint of two points",
   "N = (0, 8) and O = (0, −8) lie on one north–south line; their midpoint is (0, 0), which is L.", [ARR],
   why_others_wrong="K, M and T are 6 m east or west of that line.", seconds=70)
# ---- Advanced (standalone)
x, y = (4 + 5, 0)
x, y = x, y + 12
assert (x, y) == (9, 12)
mcq(DIR, SH_, "Advanced",
    "At about 7 am on a clear day, the shadow of a vertical pole P ends at point Q, 4 m from the foot of the pole. Ravi "
    "starts at Q, walks straight to the pole, continues 5 m in the same direction beyond it, then turns left and walks "
    "12 m. How far is Ravi from Q now, and in which direction?", f"{dist(x, y)} m, {compass(x, y)}",
    ["13 m, North-East", "15 m, South-East", "21 m, North-East"], "Morning shadows point west",
    "At 7 am the sun is in the east, so the shadow points west: Q is 4 m west of the pole. Walking from Q to the pole "
    "and 5 m beyond means walking east 9 m. A left turn from east is north, 12 m. Ravi is 9 m east and 12 m north of "
    "Q: √(81 + 144) = 15 m, north-east.",
    ["Morning: sun east ⇒ shadow west ⇒ Q is 4 m west of P", "Q → P → 5 m beyond = 9 m east",
     "Left of east = north: 12 m", "√(9² + 12²) = 15 m, North-East"],
    why_others_wrong="13 m measures from the pole instead of from Q; South-East takes the left turn as south; 21 m adds "
                     "the legs.", seconds=90, verified_by=RECOMP)
x, y = walk("S", [(None, 5), ("L", 9), ("R", 7), ("R", 21), ("L", 4)])
assert (x, y) == (-12, -16)
mcq(DIR, DD, "Advanced",
    "A delivery rider starts from the depot and rides 5 km towards the south. She turns left and rides 9 km, turns "
    "right and rides 7 km, turns right again and rides 21 km, and finally turns left and rides 4 km. How far is she "
    "from the depot, and in which direction?", f"{dist(x, y)} km, {compass(x, y)}",
    ["20 km, South-East", "28 km, South-West", "16 km, South"], "Track the facing after every turn",
    "Left from south is east (9 km); right from east is south (7 km); right from south is west (21 km); left from west "
    "is south (4 km). Net: east 9 − 21 = 12 km west; south 5 + 7 + 4 = 16 km. √(144 + 256) = 20 km, south-west.",
    ["S 5 → (0, −5)", "Left ⇒ E 9 → (9, −5)", "Right ⇒ S 7 → (9, −12)", "Right ⇒ W 21 → (−12, −12)",
     "Left ⇒ S 4 → (−12, −16)", "√(12² + 16²) = 20 km, South-West"],
    why_others_wrong="South-East ignores that the 21 km west leg overshoots; 28 km adds the legs; 16 km, South drops the "
                     "west part.", seconds=110, verified_by=RECOMP)

# ================================================================================================ CODING-DECODING
LC, SW, NC = "Letter coding", "Sentence/word coding", "Number coding"
VOW = set("AEIOU")


def letter_rules():
    R = {}
    opp_ = lambda w: "".join(AL[26 - pos(c)] for c in w)
    half = lambda w: w[len(w) // 2:] + w[:len(w) // 2]
    halfrev = lambda w: w[:len(w) // 2][::-1] + w[len(w) // 2:][::-1]
    pairswap = lambda w: "".join(w[i + 1] + w[i] for i in range(0, len(w) - 1, 2)) + (w[-1] if len(w) % 2 else "")
    oddeven = lambda w: w[0::2] + w[1::2]
    for k in range(-6, 7):
        for nm, f_ in (("id", lambda w: w), ("rev", lambda w: w[::-1]), ("opp", opp_), ("half", half),
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
        R[f"opp+posL{sgn}"] = lambda w, s=sgn: "".join(shift(c, s * (i + 1)) for i, c in enumerate(opp_(w)))
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

# ---- Basic set: sentence coding
SS = [(["river", "flows", "fast"], ["mo", "ki", "ra"]), (["fast", "boats", "sail"], ["ki", "pu", "zo"]),
      (["boats", "cross", "river"], ["zo", "ra", "te"])]
sid = stimulus("passage", "Three coded sentences about a river",
               "In a certain code language:\n'river flows fast' is written as 'mo ki ra',\n'fast boats sail' is written "
               "as 'ki pu zo', and\n'boats cross river' is written as 'zo ra te'.\n(The codes of the words in a sentence "
               "may be in any order.)", None,
               "Each shared word takes the code its two sentences share: river = ra (sentences 1 and 3), fast = ki "
               "(1 and 2), boats = zo (2 and 3). The leftover code in each sentence belongs to its only unshared word: "
               "flows = mo, sail = pu, cross = te.")
CQ = lambda sub, diff, text, correct, wrongs, concept, expl, steps, **kw: mcq(
    COD, sub, diff, text, correct, wrongs, concept, expl, steps, stimulus=sid, verified_by=RECOMP, **kw)
assert sentence_solve(SS, "flows") == {"mo"}
CQ(SW, "Basic", "What is the code for 'flows'?", "mo", ["ki", "ra", "te"], "Remove the codes of the shared words",
   "In sentence 1, river = ra (shared with sentence 3) and fast = ki (shared with sentence 2), so flows = mo.",
   ["river = ra; fast = ki", "Leftover in 'mo ki ra' ⇒ flows = mo"],
   why_others_wrong="ki is 'fast', ra is 'river' and te is 'cross'.", seconds=40)
assert sentence_solve(SS, "pu") == {"sail"}
CQ(SW, "Basic", "Which word is coded as 'pu'?", "sail", ["boats", "fast", "cross"], "The unshared code of a sentence",
   "Sentence 2 is 'fast boats sail' = 'ki pu zo'. fast = ki and boats = zo, so pu = sail.",
   ["fast = ki (1 & 2); boats = zo (2 & 3)", "pu ⇒ sail"], why_others_wrong="boats = zo, fast = ki, cross = te.",
   seconds=40)
assert sentence_solve(SS, "river") == {"ra"} and sentence_solve(SS, "cross") == {"te"}
CQ(SW, "Basic", "What is the code for 'cross river'?", "te ra", ["zo te", "ra mo", "te ki"], "Two codes at once",
   "river = ra (common to sentences 1 and 3). In sentence 3, boats = zo, so cross = te. 'cross river' = 'te ra' (in "
   "any order).", ["river = ra", "boats = zo ⇒ cross = te"],
   why_others_wrong="zo is 'boats', mo is 'flows' and ki is 'fast'.", seconds=45)
# ---- Basic standalone
psw = lambda w: "".join(w[i + 1] + w[i] for i in range(0, len(w) - 1, 2)) + (w[-1] if len(w) % 2 else "")
assert psw("PENCIL") == "EPCNLI"
ans = inferred([("PENCIL", "EPCNLI")], "MARKET", psw("MARKET"))
assert ans == "AMKRTE"
mcq(COD, LC, "Basic", "In a certain code, PENCIL is written as EPCNLI. How is MARKET written in that code?", ans,
    ["TEKRAM", "AMRKTE", "MAKRET"], "Letters swapped in pairs",
    "PENCIL → (PE)(NC)(IL) → EP CN LI: each pair of letters is interchanged. MARKET → (MA)(RK)(ET) → AM KR TE = AMKRTE.",
    ["Pairs: PE→EP, NC→CN, IL→LI", f"MARKET: MA→AM, RK→KR, ET→TE ⇒ {ans}"],
    why_others_wrong="TEKRAM reverses the word; AMRKTE does not swap the middle pair; MAKRET swaps only the middle pair.",
    seconds=35, verified_by=RECOMP)
ans = inferred([("ROAD", "WTFI")], "PATH", shift("PATH", 5))
assert ans == "UFYM"
mcq(COD, LC, "Basic", "In a certain code language, ROAD is written as WTFI. How is PATH written in that code language?",
    ans, ["UFZM", "KVOC", "UEYM"], "Every letter moves the same number of places",
    "R→W, O→T, A→F, D→I: every letter moves 5 places forward. P→U, A→F, T→Y, H→M: UFYM.",
    ["R +5 = W, O +5 = T, A +5 = F, D +5 = I", "PATH +5 ⇒ UFYM"],
    why_others_wrong="UFZM moves T six places; KVOC moves every letter back; UEYM moves A only four places.",
    seconds=35, verified_by=RECOMP)
rs_ = lambda w: sum(27 - pos(c) for c in w)
assert rs_("FAN") == 60 and rs_("BOX") == 40
ans = inferred([("FAN", 60), ("BOX", 40)], "COT", rs_("COT"), NRULES)
assert ans == 43
mcq(COD, NC, "Basic", "In a certain code, FAN is written as 60 and BOX is written as 40. How is COT written in that "
    "code?", str(ans), ["38", "47", "45"], "Reverse alphabetical positions (A = 26, …, Z = 1)",
    "Counting from Z = 1 to A = 26: F 21 + A 26 + N 13 = 60; B 25 + O 12 + X 3 = 40. COT: C 24 + O 12 + T 7 = 43.",
    ["Reverse positions: F 21, A 26, N 13 ⇒ 60 ✓", "B 25, O 12, X 3 ⇒ 40 ✓", "C 24 + O 12 + T 7 = 43"],
    why_others_wrong="38 is the ordinary sum of positions (3 + 15 + 20); 47 and 45 miscount one letter's reverse "
                     "position.", natural=int, seconds=45, verified_by=RECOMP)
dc = lambda w: "".join(str(pos(c)) for c in w)
assert dc("BED") == "254"
ans = dc("FACE")
assert ans == "6135"
mcq(COD, NC, "Basic", "In a certain code, BED is written as 254 and HAD as 814. How is FACE written in that code?", ans,
    ["6153", "7135", "6134"], "Each letter becomes its alphabetical position",
    "B = 2, E = 5, D = 4 gives 254; H = 8, A = 1, D = 4 gives 814. F = 6, A = 1, C = 3, E = 5: 6135.",
    ["Letters → positions: BED 2-5-4, HAD 8-1-4", "FACE → 6-1-3-5"],
    why_others_wrong="6153 swaps C and E; 7135 takes F as 7; 6134 takes E as 4.", seconds=35, verified_by=RECOMP)

# ---- Intermediate set: letter-to-symbol code with conditions
TAB = {"A": "4", "B": "%", "C": "7", "D": "@", "E": "9", "H": "#", "K": "2", "M": "$", "N": "5", "O": "8", "R": "&",
       "S": "3", "T": "©", "U": "6"}


def enc(w):
    c = [TAB[ch] for ch in w]
    v0, v1 = w[0] in VOW, w[-1] in VOW
    if v0 and not v1:
        c[0], c[-1] = c[-1], c[0]
    elif v0 and v1:
        c[0] = c[-1] = TAB[w[1]]
    elif not v0 and v1:
        c[-1] = "★"
    return "".join(c)


plain = lambda w: "".join(TAB[ch] for ch in w)
sid = stimulus("data_table", "Letter codes with three conditions",
               "Each letter is coded as shown below, subject to the conditions that follow.\n\n"
               + table(["Letter"] + list(TAB), ["Code"] + list(TAB.values())) +
               "\n\nConditions:\n(i) If the first letter is a vowel and the last letter is a consonant, the codes of the "
               "first and the last letters are interchanged.\n(ii) If both the first and the last letters are vowels, "
               "both are coded as the code of the second letter.\n(iii) If the first letter is a consonant and the last "
               "letter is a vowel, the last letter is coded as ★.\nIf no condition applies, every letter is coded as in "
               "the table.", None,
               "Check the first and last letters of the word, apply at most one condition, and code the remaining "
               "letters from the table.")
for w_, e_ in (("OMEN", "5$98"), ("AROMA", "&&8$&"), ("DUSK", "@632"), ("TUBE", "©6%★")):
    assert enc(w_) == e_, (w_, enc(w_))
CQ(LC, "Intermediate", "What is the code for 'OMEN'?", enc("OMEN"), [plain("OMEN"), "$598", "5$9★"],
   "Condition (i): vowel first, consonant last",
   "O is a vowel and N a consonant, so condition (i) applies: the codes of O (8) and N (5) are interchanged. "
   "O M E N → 5 $ 9 8.", ["Table: O 8, M $, E 9, N 5", "Condition (i) ⇒ swap first and last codes ⇒ 5$98"],
   why_others_wrong="8$95 ignores the condition; $598 swaps the wrong letters; 5$9★ mixes conditions (i) and (iii).",
   seconds=60)
CQ(LC, "Intermediate", "What is the code for 'AROMA'?", enc("AROMA"), [plain("AROMA"), "4&8$4"[::-1], "★&8$★"],
   "Condition (ii): vowels at both ends",
   "A is a vowel at both ends, so both A's take the code of the second letter, R (&): & & 8 $ &.",
   ["Second letter R = &", "First and last letters → & ⇒ &&8$&"],
   why_others_wrong="4&8$4 ignores the condition; 4$8&4 reverses the word; ★&8$★ wrongly applies the ★ rule.",
   seconds=60)
CQ(LC, "Intermediate", "What is the code for 'DUSK'?", enc("DUSK"), ["263@", "@63★", "#632"],
   "No condition applies to consonants at both ends",
   "D and K are both consonants, so none of the conditions applies: D @, U 6, S 3, K 2 ⇒ @632.",
   ["First D, last K: both consonants", "Plain table codes ⇒ @632"],
   why_others_wrong="263@ wrongly applies condition (i); @63★ wrongly applies (iii); #632 uses the code of H for D.",
   seconds=55)
CQ(LC, "Intermediate", "What is the code for 'TUBE'?", enc("TUBE"), [plain("TUBE"), "★6%©", "6©%9"],
   "Condition (iii): consonant first, vowel last",
   "T is a consonant and E a vowel, so condition (iii) applies: the last letter is coded as ★. T U B E → © 6 % ★.",
   ["Table: T ©, U 6, B %, E 9", "Condition (iii) ⇒ last code ★ ⇒ ©6%★"],
   why_others_wrong="©6%9 ignores the condition; ★6%© puts ★ first and moves ©; 6©%9 rearranges the codes.",
   seconds=55)

# ---- Intermediate set: four coded sentences with one ambiguous pair
SS = [(["save", "water", "daily"], ["ka", "lo", "mi"]), (["water", "the", "plants", "daily"], ["mi", "ne", "lo", "su"]),
      (["plants", "need", "sunlight"], ["su", "ra", "tu"]), (["need", "to", "save"], ["ra", "ka", "vo"])]
sid = stimulus("passage", "Four coded sentences about plants",
               "In a certain code language:\n'save water daily' is written as 'ka lo mi',\n'water the plants daily' is "
               "written as 'mi ne lo su',\n'plants need sunlight' is written as 'su ra tu', and\n'need to save' is "
               "written as 'ra ka vo'.\n(The codes of the words in a sentence may be in any order.)", None,
               "plants = su (sentences 2 and 3); need = ra (3 and 4); save = ka (1 and 4). Then sunlight = tu and to = vo. "
               "'water' and 'daily' always appear together, so they share 'lo' and 'mi' in some order; the remaining "
               "code of sentence 2, ne, is 'the'.")
assert sentence_solve(SS, "sunlight") == {"tu"}
CQ(SW, "Intermediate", "What is the code for 'sunlight'?", "tu", ["su", "ra", "vo"], "Strip the shared codes",
   "plants = su (shared by sentences 2 and 3) and need = ra (shared by sentences 3 and 4), so in 'su ra tu' sunlight = "
   "tu.", ["plants = su; need = ra", "sunlight = tu"], why_others_wrong="su is 'plants', ra 'need' and vo 'to'.",
   seconds=55)
assert sentence_solve(SS, "vo") == {"to"}
CQ(SW, "Intermediate", "Which word is coded as 'vo'?", "to", ["need", "save", "the"], "Leftover code of a sentence",
   "Sentence 4 'need to save' = 'ra ka vo'. need = ra and save = ka (shared with sentence 1), so vo = to.",
   ["need = ra; save = ka", "vo ⇒ to"], why_others_wrong="need = ra, save = ka and the = ne.", seconds=55)
assert sentence_solve(SS, "lo") == {"water", "daily"}
CQ(SW, "Intermediate", "Which word does the code 'lo' stand for?", "Either 'water' or 'daily'",
   ["'water' only", "'daily' only", "'the'"], "When two words always appear together",
   "'water' and 'daily' occur together in sentences 1 and 2 and nowhere else, so their codes 'lo' and 'mi' cannot be "
   "told apart: 'lo' is either 'water' or 'daily'.", ["water, daily appear only in sentences 1 and 2",
                                                       "Their codes lo, mi cannot be separated"],
   why_others_wrong="Choosing one of the two words assumes information the sentences do not give; 'the' is ne.",
   seconds=60)
# ---- Intermediate standalone
hr1 = LRULES["halfrev+1"]
assert hr1("CASTLE") == "TBDFMU"
ans = inferred([("CASTLE", "TBDFMU")], "BRIDGE", hr1("BRIDGE"))
assert ans == "JSCFHE"
mcq(COD, LC, "Intermediate", "In a certain code, CASTLE is written as TBDFMU. How is BRIDGE written in that code?", ans,
    ["IRBEGD", "CSJEHF", "JSCHFE"], "Reverse each half, then move every letter one step forward",
    "CASTLE → halves CAS | TLE → reversed SAC | ELT → each letter +1: TBD | FMU. BRIDGE → BRI | DGE → IRB | EGD → +1: "
    f"JSC | FHE = {ans}.", ["CAS → SAC → TBD; TLE → ELT → FMU", "BRI → IRB → JSC; DGE → EGD → FHE"],
    why_others_wrong="IRBEGD stops before the +1 step; CSJEHF adds 1 without reversing the halves; JSCHFE reverses the "
                     "second half wrongly.", seconds=60, verified_by=RECOMP)
DR2 = {}
for k_ in range(-9, 10):
    for nm_, f_ in (("id", lambda n: n), ("rev", lambda n: n[::-1]), ("pairswap", lambda n: n[1] + n[0] + n[3] + n[2]),
                    ("halfswap", lambda n: n[2:] + n[:2]), ("ends", lambda n: n[3] + n[1:3] + n[0])):
        DR2[f"{nm_}{k_}"] = lambda n, f_=f_, k_=k_: "".join(str((int(d) + k_) % 10) for d in f_(n))
        DR2[f"{k_}-{nm_}"] = lambda n, f_=f_, k_=k_: "".join(str((k_ - int(d)) % 10) for d in f_(n))
r2 = DR2["rev2"]
assert r2("4716") == "8396" and r2("2053") == "5724"
ans = inferred([("4716", "8396"), ("2053", "5724")], "6481", r2("6481"), DR2)
assert ans == "3068"
mcq(COD, NC, "Intermediate", "In a certain code, 4716 is written as 8396 and 2053 is written as 5724. How is 6481 "
    "written in that code?", ans, ["8603", "1846", "3069"], "Add 2 to each digit, then reverse",
    "4716: +2 to every digit → 6938, reversed → 8396. 2053 → 4275 → 5724. 6481 → 8603 → 3068.",
    ["Check: 4716 → 6938 → 8396; 2053 → 4275 → 5724", "6481 + 2 each → 8603", f"Reverse → {ans}"],
    why_others_wrong="8603 skips the reversal; 1846 only reverses; 3069 adds 3 to the last digit.", seconds=60,
    verified_by=RECOMP)
vc = LRULES["vc1,-1"]
assert vc("PLANT") == "OKBMS" and vc("CREDIT") == "BQFCJS"
ans = inferred([("PLANT", "OKBMS"), ("CREDIT", "BQFCJS")], "MOBILE", vc("MOBILE"))
assert ans == "LPAJKF"
mcq(COD, LC, "Intermediate", "In a certain code, PLANT is written as OKBMS and CREDIT is written as BQFCJS. How is "
    "MOBILE written in that code?", ans, ["NPCJMF", "LNAHKD", "LPAJKD"], "Vowels and consonants move differently",
    "In PLANT the consonants move one step back (P→O, L→K, N→M, T→S) and the vowel A moves one step forward (A→B); "
    "CREDIT confirms it (E→F, I→J). MOBILE: M→L, O→P, B→A, I→J, L→K, E→F = LPAJKF.",
    ["Consonants −1, vowels +1", "M L, O P, B A, I J, L K, E F"],
    why_others_wrong="NPCJMF moves every letter forward; LNAHKD moves every letter back; LPAJKD moves the final E back "
                     "instead of forward.", seconds=60, verified_by=RECOMP)
# ---- Advanced
pl = LRULES["posL1"]
assert pl("BANK") == "CCQO" and pl("SHIP") == "TJLT"
ans = inferred([("BANK", "CCQO"), ("SHIP", "TJLT")], "WORLD", pl("WORLD"))
assert ans == "XQUPI"
mcq(COD, LC, "Advanced", "In a certain code, BANK is written as CCQO and SHIP is written as TJLT. How is WORLD written "
    "in that code?", ans, ["XQUPH", "XPSMH", "YQUPI"], "Shift by the letter's place in the word",
    "Each letter moves forward by its position in the word: B+1 = C, A+2 = C, N+3 = Q, K+4 = O. SHIP: S+1 T, H+2 J, I+3 "
    "L, P+4 T. WORLD: W+1 X, O+2 Q, R+3 U, L+4 P, D+5 I = XQUPI.",
    ["Shifts +1, +2, +3, +4 (+5 for a 5th letter)", "Check BANK → CCQO, SHIP → TJLT", f"WORLD → {ans}"],
    why_others_wrong="XQUPH moves the 5th letter by 4; XPSMH moves every letter by 1; YQUPI moves the first letter by 2.",
    seconds=75, verified_by=RECOMP)
wc_ = lambda w: shift(w[0].upper(), 1) + str(len(w))
EX = [("safe money transfer", "T4 N5 U8"), ("quick loan", "R5 M4")]
assert all(" ".join(wc_(x) for x in s_.split()) == c_ for s_, c_ in EX)
ALT = {"next-first+len": wc_, "first+len": lambda w: w[0].upper() + str(len(w)),
       "next-first+vowels": lambda w: shift(w[0].upper(), 1) + str(sum(c in "aeiou" for c in w)),
       "next-last+len": lambda w: shift(w[-1].upper(), 1) + str(len(w)),
       "prev-first+len": lambda w: shift(w[0].upper(), -1) + str(len(w)),
       "next-first+len+1": lambda w: shift(w[0].upper(), 1) + str(len(w) + 1)}
fits = {k: " ".join(f_(x) for x in "fast online payment".split()) for k, f_ in ALT.items()
        if all(" ".join(f_(x) for x in s_.split()) == c_ for s_, c_ in EX)}
assert set(fits.values()) == {"G4 P6 Q7"}
mcq(COD, SW, "Advanced", "In a certain code language, each word is coded by a rule, and the codes are written in the "
    "same order as the words. 'safe money transfer' is written as 'T4 N5 U8', and 'quick loan' is written as 'R5 M4'. "
    "How is 'fast online payment' written in that code language?", "G4 P6 Q7",
    ["F4 O6 P7", "G4 P6 Q8", "G4 P5 Q7"], "Code = letter after the first letter + number of letters",
    "safe → S+1 = T and 4 letters: T4; money → N5; transfer → U8; quick → R5; loan → M4. fast → G4, online → P6, "
    "payment → Q7.", ["Letter part: the letter after the word's first letter", "Number part: length of the word",
                      "fast G4, online P6, payment Q7"],
    why_others_wrong="F4 O6 P7 does not shift the first letter; G4 P6 Q8 miscounts 'payment' (7 letters); G4 P5 Q7 "
                     "miscounts 'online' (6 letters).", seconds=70, verified_by=RECOMP)

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


SR = "Q 7 % D E 3 & 8 K # U 1 J @ 5 X Z 6 $ A".split()
assert len(SR) == 20
i6 = len(SR) - 6
ans = SR[i6 - 4]
assert SR[i6] == "5" and ans == "U"
mcq(ALN, PB, "Basic", series_intro(" ".join(SR)) + "\n\nWhich element is 4th to the left of the 6th element from the "
    "right end?", ans, near(SR, i6 - 4), "Convert a right-end position, then move left",
    f"The 6th element from the right is the {i6 + 1}th from the left ({SR[i6]}). Four places to its left is the "
    f"{i6 - 3}th element: {ans}.", [f"6th from the right = 20 − 6 + 1 = {i6 + 1}th from the left = {SR[i6]}",
                                     f"{i6 + 1} − 4 = {i6 - 3}th ⇒ {ans}"], seconds=40, verified_by=RECOMP)
SR = "5 T @ 2 K 9 # B 4 E & 6 W % 1 R 8 £ M 3 U".split()
hits = [w for w in windows(SR) if is_d(w[1]) and is_s(w[0]) and is_l(w[2])]
a, w = count_opts(len(hits))
mcq(ALN, SN, "Intermediate", series_intro(" ".join(SR)) + "\n\nHow many numbers in the arrangement are immediately "
    "preceded by a symbol and immediately followed by a letter?", a, w, "Both neighbours must match",
    "Numbers with both neighbours: " + "; ".join(f"{SR[i - 1]} {SR[i]} {SR[i + 1]}" for i in range(1, len(SR) - 1)
                                                if is_d(SR[i])) + ". Symbol before and letter after: "
    + (", ".join(" ".join(h) for h in hits) or "none") + f" — {len(hits)}.",
    ["Check each number's left and right neighbour", "Matches: " + (", ".join(" ".join(h) for h in hits) or "none")],
    natural=by_num, seconds=60, verified_by=RECOMP)
SR = "H 6 © Y 2 A ¥ 9 L O 4 # S 7 I @ 1 N £ 8 F 3 E".split()
nos = [t for t in SR if not is_s(t)]
nw = nos[:8][::-1] + nos[8:]
ans = nw[9 - 1 + 5]
mcq(ALN, PB, "Advanced", series_intro(" ".join(SR)) + "\n\nIf all the symbols are removed and then the first eight "
    "of the remaining elements are written in reverse order, which element will be 5th to the right of the 9th element "
    "from the left end?", ans, near(nw, 13), "Delete, rearrange a block, then count",
    "Without symbols: " + " ".join(nos) + ". Reversing the first eight gives " + " ".join(nw) + f". The 9th element is "
    f"{nw[8]}; five places to its right is the 14th: {ans}.",
    ["Remove " + ", ".join(t for t in SR if is_s(t)), "Reverse the first eight: " + " ".join(nw),
     f"9th = {nw[8]}; 9 + 5 = 14th ⇒ {ans}"], seconds=80, verified_by=RECOMP)

# ================================================================================================ ALPHABET TEST
ABT = "Alphabet Test"
LP, WF, PRS = "Letter position", "Word formation", "Pairs of letters"
ans = AL[20 - 8 - 1]
assert ans == "L"
mcq(ABT, LP, "Basic", "Which letter is 8th to the left of the 20th letter from the left end of the English alphabet?",
    ans, ["K", "M", "B"], "Positions in the alphabet", "The 20th letter is T. Eight places to its left is the 12th "
    "letter: L.", ["20th = T", "20 − 8 = 12th ⇒ L"], why_others_wrong="K (11th) and M (13th) are one place off; B "
                                                                       "counts 8 places right of T from the other end.",
    seconds=30, verified_by=RECOMP)
ans = AL[(pos("G") + pos("S")) // 2 - 1]
assert ans == "M"
mcq(ABT, LP, "Basic", "Which letter of the English alphabet lies exactly midway between G and S?", ans,
    ["L", "N", "K"], "Midpoint of two positions", "G is 7th and S is 19th; (7 + 19) ÷ 2 = 13th: M.",
    ["G = 7, S = 19", "(7 + 19) ÷ 2 = 13 ⇒ M"], why_others_wrong="L and N are one place either side; K is 11th.",
    seconds=30, verified_by=RECOMP)
WDS = ["CARPET", "CARROT", "CARTON", "CARBON", "CARGO"]
srt = sorted(WDS)
assert srt == ["CARBON", "CARGO", "CARPET", "CARROT", "CARTON"]
mcq(ABT, WF, "Basic", "If the words CARPET, CARROT, CARTON, CARBON and CARGO are arranged in the order in which they "
    "appear in an English dictionary, which word will be fourth?", srt[3], ["CARPET", "CARTON", "CARGO"],
    "Compare the first letter that differs", "All five start with CAR; the 4th letters are P, R, T, B, G. In order: B, "
    "G, P, R, T, so the fourth word is CARROT.", ["Common prefix CAR", "4th letters: B < G < P < R < T",
                                                 "Order: " + ", ".join(srt)],
    why_others_wrong="CARPET is third, CARTON fifth and CARGO second.", seconds=35, verified_by=RECOMP)
wd = "WORLD"
pr = letter_pairs(wd)
a, w = count_opts(len(pr))
mcq(ABT, PRS, "Basic", f"How many pairs of letters are there in the word '{wd}' each of which has as many letters "
    "between them in the word as in the English alphabet (counting both forward and backward)?", a, w,
    "Compare the gap in the word with the gap in the alphabet",
    "Pairs found: " + (", ".join(f"{x}{y}" for x, y in pr) or "none") + f" — {len(pr)} in all.",
    ["Alphabet positions: " + ", ".join(f"{c} {pos(c)}" for c in wd),
     "A pair qualifies when |word gap| = |alphabet gap|"], natural=by_num, seconds=50, verified_by=RECOMP)
SRC = "COMMUNICATION"
can = lambda wd_: all(wd_.count(c) <= SRC.count(c) for c in set(wd_))
OPTS = ["CAUTION", "MONITOR", "NOTICE", "COMMAND"]
assert [can(x) for x in OPTS] == [True, False, False, False]
mcq(ABT, WF, "Basic", "Which of the following words can be formed using the letters of the word 'COMMUNICATION', each "
    "letter used no more often than it appears in it?", OPTS[0], OPTS[1:], "Check every letter against the source",
    "COMMUNICATION has C×2, O×2, M×2, U, N×2, I×2, A and T. CAUTION needs C, A, U, T, I, O, N — all available. MONITOR "
    "needs an R, NOTICE an E and COMMAND a D, none of which occur.",
    ["Available: A1 C2 I2 M2 N2 O2 T1 U1", "CAUTION ✓", "MONITOR (R), NOTICE (E), COMMAND (D) ✗"], seconds=45,
    verified_by=RECOMP)
# ---- Advanced
kept = [c for i, c in enumerate(AL) if (i + 1) % 4 != 0][::-1]
ans = kept[8]
mcq(ABT, LP, "Advanced", "If every letter in a position of the English alphabet that is a multiple of 4 (D, H, L, …) is "
    "removed and the remaining letters are written in reverse order, which letter will be 9th from the left end?", ans,
    [kept[7], kept[9], AL[26 - 9]], "Remove, reverse, then count",
    "Removed: D, H, L, P, T, X. Remaining in reverse order: " + " ".join(kept) + f". The 9th from the left is {ans}.",
    ["Remove positions 4, 8, …, 24", "Reverse: " + " ".join(kept), f"9th ⇒ {ans}"],
    why_others_wrong=f"{kept[7]} and {kept[9]} are 8th and 10th; {AL[26 - 9]} is the 9th letter of the full reversed "
                     "alphabet, ignoring the removal.", seconds=70, verified_by=RECOMP)
wd = "STRENGTH"
pr = letter_pairs(wd)
a, w = count_opts(len(pr))
mcq(ABT, PRS, "Advanced", f"In the word '{wd}', how many pairs of letters have the same number of letters between "
    "them in the word as between them in the English alphabet? Count a pair whether its letters appear in alphabetical "
    "or reverse order.", a, w, "Compare the gap in the word with the gap in the alphabet",
    "Pairs found: " + (", ".join(f"{x}{y}" for x, y in pr) or "none") + f" — {len(pr)} in all.",
    ["Alphabet positions: " + ", ".join(f"{c} {pos(c)}" for c in wd),
     "A pair qualifies when |word gap| = |alphabet gap|"], natural=by_num, seconds=80, verified_by=RECOMP)
wd = "PERFORMANCE"
nl = sorted(shift(c, -2) for c in wd)
ans = nl[-5]
wr_ = sorted(set(nl) - {ans}, key=lambda c: (abs(pos(c) - pos(ans)), c))[:3]
mcq(ABT, LP, "Advanced", f"Each letter of the word '{wd}' is replaced by the letter two places before it in the English "
    "alphabet, and the new letters are then arranged in alphabetical order from left to right. Which letter will be 5th "
    "from the right end?", ans, wr_,
    "Transform, sort, then count from the right",
    "−2 on each letter: " + " ".join(shift(c, -2) for c in wd) + ". Sorted: " + " ".join(nl) + f". The 5th from the right "
    f"is {ans}.", ["Shift each letter back by 2", "Sort: " + " ".join(nl), f"5th from the right ⇒ {ans}"],
    why_others_wrong="The other letters sit at different places in the sorted list (or do not occur in it).",
    seconds=80, verified_by=RECOMP)
wd = "HORIZONTAL"
hit = [wd[i] for i in range(1, len(wd) - 1) if wd[i - 1] in VOW and wd[i + 1] in VOW]
a, w = count_opts(len(hit))
mcq(ABT, LP, "Advanced", f"In the word '{wd}', how many letters have a vowel immediately on both sides of them?", a, w,
    "Check both neighbours of every inner letter",
    f"Letters of {wd} with a vowel on each side: " + (", ".join(f"{wd[i - 1]}{wd[i]}{wd[i + 1]}" for i in
                                                               range(1, len(wd) - 1)
                                                               if wd[i - 1] in VOW and wd[i + 1] in VOW) or "none")
    + f" — {len(hit)}.", ["Vowels: " + ", ".join(c for c in wd if c in VOW), "Check each inner letter's neighbours"],
    natural=by_num, seconds=60, verified_by=RECOMP)
l4, r5 = 4, 26 - 5 + 1
assert (l4 + r5) % 2 == 0
ans = AL[(l4 + r5) // 2 + 3 - 1]
assert ans == "P"
mcq(ABT, LP, "Advanced", "Which letter is 3rd to the right of the letter that lies exactly midway between the 4th letter "
    "from the left end and the 5th letter from the right end of the English alphabet?", ans, ["M", "O", "Q"],
    "Convert both positions to the left end first",
    "The 4th letter from the left is D (4). The 5th from the right is the 22nd from the left, V. Midway: (4 + 22) ÷ 2 = "
    "13th, M. Three places to its right is the 16th letter: P.",
    ["4th from the left = D (4)", "5th from the right = 26 − 5 + 1 = 22nd = V", "Midway = 13th = M", "13 + 3 = 16 ⇒ P"],
    why_others_wrong="M is the midpoint itself; O and Q are 2 and 4 places to its right.", seconds=70,
    verified_by=RECOMP)

# ================================================================================================ NUMBER SERIES (REASONING)
NSR = "Number Series (Reasoning)"
NDO, TDN = "Number-based digit operations", "Three-digit number questions"
NUMS = [517, 284, 936, 461, 708, 359]
sid = stimulus("data_table", "Six three-digit numbers",
               "Study the following six three-digit numbers and answer the questions.\n\n" +
               "   ".join(map(str, NUMS)), None, "Read each operation carefully and apply it to every number.")
NQ = lambda text, correct, wrongs, concept, expl, steps, **kw: mcq(
    NSR, TDN, "Intermediate", text, correct, wrongs, concept, expl, steps, stimulus=sid, verified_by=RECOMP, **kw)
rv = {n: int(str(n)[::-1]) for n in NUMS}
best = max(NUMS, key=rv.get)
assert best == 359 and rv[best] == 953
NQ("If the digits of each number are reversed, which original number gives the largest new number?", str(best),
   ["936", "708", "517"], "Reverse, then compare",
   "Reversed: " + ", ".join(f"{n} → {rv[n]}" for n in NUMS) + ". The largest is 953, from 359.",
   ["Reversed values listed", "Largest 953 ⇐ 359"],
   why_others_wrong="936 → 639, 708 → 807 and 517 → 715 are all smaller than 953.", seconds=55)
op = lambda n: n + 100 if n % 2 else n - 1
new = {n: op(n) for n in NUMS}
cnt = sum(1 for n in NUMS if new[n] % 3 == 0)
a, w = count_opts(cnt)
NQ("If 1 is added to the first digit of every odd number and 1 is subtracted from the last digit of every even number, "
   "how many of the new numbers will be divisible by 3?", a, w, "Apply the right operation to each number",
   "New numbers: " + ", ".join(f"{n} → {new[n]}" for n in NUMS) + ". Divisible by 3 (digit sum a multiple of 3): "
   + (", ".join(str(new[n]) for n in NUMS if new[n] % 3 == 0) or "none") + f" — {cnt}.",
   ["Odd: 517, 461, 359 (+100); even: 284, 936, 708 (−1)", "Test each digit sum"], natural=by_num, seconds=65)
s_ = sorted(NUMS)
ans = s_[-2] - s_[2]
assert (s_[-2], s_[2], ans) == (708, 461, 247)
NQ("What is the difference between the second largest number and the third smallest number?", str(ans),
   ["475", "349", "191"], "Sort first", "In ascending order: " + ", ".join(map(str, s_)) + ". Second largest 708, third "
   "smallest 461: 708 − 461 = 247.", ["Sorted: " + ", ".join(map(str, s_)), "708 − 461 = 247"],
   why_others_wrong="475 uses the largest number (936 − 461); 349 uses the second smallest (708 − 359); 191 uses the "
                    "third largest (708 − 517).", natural=int, seconds=55)


def rowop(a, b):
    if a % 2 and not b % 2:
        return a + b
    if not a % 2 and b % 2:
        return a - b
    if a % 2 and b % 2:
        return a * b
    assert a % b == 0
    return a // b


ROWS = [(15, 8, 3), (36, 4, 7), (28, 5, 6)]
res = [rowop(rowop(a, b), c) for a, b, c in ROWS]
assert res == [69, 63, 29]
RULES = ("(i) If an odd number is followed by an even number, they are added.\n(ii) If an even number is followed by an "
         "odd number, the odd number is subtracted from the even number.\n(iii) If an odd number is followed by an odd "
         "number, they are multiplied.\n(iv) If an even number is followed by an even number, the first is divided by "
         "the second.")
sid = stimulus("data_table", "Three rows of numbers with operation rules",
               "Each row below has three numbers. Work from left to right: apply the rule that fits the first two "
               "numbers, then apply the rule that fits that result and the third number. The final value is the row's "
               "result.\n\n" + RULES + "\n\nRow 1: 15   8   3\nRow 2: 36   4   7\nRow 3: 28   5   6", None,
               "Row 1: 15 (odd), 8 (even) → 23; 23, 3 (both odd) → 69.\nRow 2: 36, 4 (both even) → 9; 9, 7 (both odd) "
               "→ 63.\nRow 3: 28 (even), 5 (odd) → 23; 23 (odd), 6 (even) → 29.")
NQ = lambda text, correct, wrongs, concept, expl, steps, **kw: mcq(
    NSR, NDO, "Intermediate", text, correct, wrongs, concept, expl, steps, stimulus=sid, verified_by=RECOMP, **kw)
NQ("What is the result of Row 1?", str(res[0]), ["26", "120", "23"], "Apply the rules left to right",
   "15 is odd and 8 even, so add: 23. 23 and 3 are both odd, so multiply: 69.", ["15 + 8 = 23", "23 × 3 = 69"],
   why_others_wrong="26 adds 3 instead of multiplying; 120 multiplies 15 by 8; 23 stops after the first step.",
   natural=int, seconds=50)
NQ("What is the difference between the results of Row 1 and Row 2?", str(res[0] - res[1]), ["9", "40", "12"],
   "Compute both rows", "Row 1 = 69. Row 2: 36 ÷ 4 = 9, then 9 × 7 = 63. 69 − 63 = 6.",
   ["Row 1 = 69", "Row 2: 36 ÷ 4 = 9; 9 × 7 = 63", "69 − 63 = 6"],
   why_others_wrong="9 is Row 2's first step; 40 compares Row 1 with Row 3; 12 uses 57 for Row 2.", natural=int,
   seconds=60)
NQ("What is the sum of the results of Row 2 and Row 3?", str(res[1] + res[2]), ["86", "98", "132"],
   "Rule (ii) subtracts the odd number", "Row 2 = 63. Row 3: 28 − 5 = 23, then 23 + 6 = 29. 63 + 29 = 92.",
   ["Row 2 = 63", "Row 3: 28 − 5 = 23; 23 + 6 = 29", "63 + 29 = 92"],
   why_others_wrong="86 uses 23 for Row 3; 98 adds 5 instead of subtracting it in Row 3; 132 uses Row 1 for Row 2.",
   natural=int, seconds=60)

# ================================================================================================ RANKING
RNK = "Ranking and Order"
aman, bina = 14, 14 + 6
tot = bina + 17 - 1
assert tot == 36
mcq(RNK, "Position in a row", "Intermediate", "In a row of students facing north, Aman is 14th from the left end. "
    "Bina sits sixth to the right of Aman and is 17th from the right end. How many students are there in the row?",
    str(tot), ["37", "35", "31"], "Both-end positions of one person give the total",
    f"Bina is 14 + 6 = 20th from the left and 17th from the right, so the row has 20 + 17 − 1 = {tot} students.",
    ["Bina = 14 + 6 = 20th from the left", f"Total = 20 + 17 − 1 = {tot}"],
    why_others_wrong="37 forgets to subtract Bina once; 35 places Bina 19th; 31 adds Aman's position to Bina's "
                     "right-end position.", natural=int, seconds=45, verified_by=RECOMP)

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
            final = sorted(items, key=key) if side == "left" else sorted(items, key=key)[::-1]
            assert tf is None and cur == final, ("a step changes nothing", cur)
            break
        cur = new
        steps.append(cur[:])
    return steps


line = lambda s: " ".join(map(str, s))
step_txt = lambda st: [f"Step {ROMAN[i]}: {line(s_)}" for i, s_ in enumerate(st)]

# ---- Basic set: smallest number to the right end each step (final line in descending order)
INP = [48, 13, 76, 54, 29, 37, 91]
st = run_machine(INP, key=lambda n: n, side="right")
assert st[-1] == sorted(INP, reverse=True)
sid = stimulus("passage", "Machine: smallest number to the right end",
               "A number arrangement machine rearranges a line of numbers step by step. In each step it takes the "
               "smallest number among those not yet arranged and places it at the right end, immediately to the left "
               "of the numbers already arranged there (in Step I, at the extreme right). The other numbers keep their "
               "order. The machine stops when all the numbers are arranged.\n\nInput: " + line(INP), None,
               "Numbers from smallest: 13, 29, 37, 48, 54, 76, 91.\n\n" + "\n".join(step_txt(st)))
IQ = lambda text, correct, wrongs, concept, expl, steps, **kw: mcq(
    IOT, NR, "Basic", text, correct, wrongs, concept, expl, steps, stimulus=sid, verified_by=RECOMP, **kw)
IQ("Which of the following is Step II?", line(st[1]), [line(st[0]), line(st[2]), line(INP[::-1])],
   "One number per step", " ".join(f"{t}." for t in step_txt(st[:2])), step_txt(st[:2]),
   why_others_wrong="The other lines are Step I, Step III and the input reversed.", seconds=45)
IQ("How many steps does the machine take to complete the arrangement?", num_word(len(st)),
   [num_word(len(st) - 1), num_word(len(st) + 1), num_word(len(st) - 2)], "The last step may arrange two numbers",
   " ".join(f"{t}." for t in step_txt(st)) + f" After Step {ROMAN[len(st) - 1]} the line is in descending order.",
   step_txt(st), natural=by_num, seconds=50)
s3 = st[2]
IQ("In Step III, which number is 2nd from the left end?", str(s3[1]), [str(x) for x in near(s3, 1)],
   "Read the step, then count", f"Step III: {line(s3)}. The 2nd from the left is {s3[1]}.", [f"Step III: {line(s3)}"],
   seconds=45)
fin = st[-1]
IQ("In the last step, which number is 4th from the right end?", str(fin[-4]), [str(x) for x in near(fin, len(fin) - 4)],
   "Final line = descending order", f"Last step: {line(fin)}. The 4th from the right is {fin[-4]}.",
   [f"Last step: {line(fin)}"], seconds=40)

# ---- Intermediate set: first word alphabetically → first letter moved to the end → right end
INP = "plum grape kiwi apple mango lime".split()
rot = lambda w: w[1:] + w[0]
st = run_machine(INP, key=lambda w: w, side="right", tf=rot)
sid = stimulus("passage", "Machine: words rotated and moved to the right",
               "A word arrangement machine rearranges a line of words step by step. In each step it takes, among the "
               "words not yet arranged, the word that comes first in alphabetical order, moves its first letter to the "
               "end of the word (for example, 'pear' becomes 'earp'), and places the new word at the right end, "
               "immediately to the left of the words already arranged there. The other words keep their order. The "
               "machine stops when every word has been arranged.\n\nInput: " + line(INP), None,
               "Alphabetical order of the input words: apple, grape, kiwi, lime, mango, plum.\n\n" + "\n".join(
                   step_txt(st)))
IQ = lambda text, correct, wrongs, concept, expl, steps, **kw: mcq(
    IOT, WR, "Intermediate", text, correct, wrongs, concept, expl, steps, stimulus=sid, verified_by=RECOMP, **kw)
assert len(st) == 6
IQ("Which of the following is Step III?", line(st[2]), [line(st[1]), line(st[3]), line(st[2][::-1])],
   "Selection plus transformation", " ".join(f"{t}." for t in step_txt(st[:3])), step_txt(st[:3]),
   why_others_wrong="The first two wrong lines are Steps II and IV; the last is Step III written backwards.",
   seconds=70)
tgt = "angom"
first = next(i for i, s_ in enumerate(st) if tgt in s_)
IQ(f"The rotated form '{tgt}' is produced in which step of the machine?", f"Step {ROMAN[first]}",
   [f"Step {ROMAN[i]}" for i in range(6) if i != first][:3], "Order of selection",
   "mango is the fifth word in alphabetical order, so it is taken (and becomes 'angom') in Step V.", step_txt(st),
   natural=lambda t: ROMAN.index(t.split()[1]), seconds=60)
fin = st[-1]
IQ("In the last step, which word is 3rd from the left end?", fin[2], [x for x in near(fin, 2)],
   "The first word chosen ends at the far right", f"Last step: {line(fin)}. The 3rd from the left is {fin[2]}.",
   [f"Last step: {line(fin)}"], seconds=60)

# ---- Advanced set: mixed machine with transformations on both sides
INP = ["comet", 47, "orbit", 82, "nova", 36, "lunar", 91, "star", 55]
dprod = lambda n: (n // 10) * (n % 10)
dsum = lambda n: n // 10 + n % 10
assert len({dprod(n) for n in INP if isinstance(n, int)}) == 5


def mixed(items):
    cur, steps, ln, lw = list(items), [], 0, 0
    rest_n = [x for x in items if isinstance(x, int)]
    rest_w = [x for x in items if isinstance(x, str)]
    left, right = [], []
    while rest_n or rest_w:
        if rest_n:
            n = min(rest_n, key=dprod)
            rest_n.remove(n)
            left.append(dsum(n))
        if rest_w:
            w = max(rest_w)
            rest_w.remove(w)
            right.insert(0, w[::-1])
        mid = [x for x in items if x in rest_n or x in rest_w]
        new = left + mid + right
        assert new != cur
        cur = new
        steps.append(cur[:])
    return steps


st = mixed(INP)
assert len(st) == 5
sid = stimulus("passage", "Machine: digit products and reversed words",
               "A word and number arrangement machine rearranges a line step by step. In each step it makes two moves: "
               "(1) among the numbers not yet arranged, it takes the one whose two digits have the smallest product, "
               "replaces it by the sum of its digits and places the result at the left end, immediately to the right of "
               "the results already placed there; (2) among the words not yet arranged, it takes the one that comes "
               "last in alphabetical order, writes it backwards and places it at the right end, immediately to the left "
               "of the words already placed there. All other elements keep their order. The machine stops when every "
               "element has been arranged.\n\nInput: " + line(INP), None,
               "Digit products: " + ", ".join(f"{n} → {dprod(n)}" for n in INP if isinstance(n, int)) +
               ", so the numbers are taken in the order 91, 82, 36, 55, 47 and become 10, 10, 9, 10, 11. Words from "
               "last to first alphabetically: star, orbit, nova, lunar, comet.\n\n" + "\n".join(step_txt(st)))
IQ = lambda text, correct, wrongs, concept, expl, steps, **kw: mcq(
    IOT, MM, "Advanced", text, correct, wrongs, concept, expl, steps, stimulus=sid, verified_by=RECOMP, **kw)
IQ("Which of the following is Step III?", line(st[2]), [line(st[1]), line(st[3]),
                                                       line(st[2][:3] + [x for x in INP if x in st[2][3:-3]] +
                                                            ["nova", "orbit", "star"])],
   "Two moves with transformations in each step", " ".join(f"{t}." for t in step_txt(st[:3])), step_txt(st[:3]),
   why_others_wrong="The first two wrong lines are Steps II and IV; the last forgets to reverse the arranged words.",
   seconds=100)
ans = sum(x for x in st[-1] if isinstance(x, int))
IQ("What is the sum of all the numbers in the last step?", str(ans), [str(sum(x for x in INP if isinstance(x, int))),
                                                                    str(ans - 1), str(ans + 10)],
   "Every number is replaced by its digit sum", f"Last step: {line(st[-1])}. Sum: {ans}.",
   [f"Last step: {line(st[-1])}", "Digit sums: 91 → 10, 82 → 10, 36 → 9, 55 → 10, 47 → 11"], natural=int,
   seconds=90)
s2 = st[1]
ix_ = s2.index("nova")
ans = s2[ix_ + 3]
IQ("In Step II, which element is 3rd to the right of 'nova'?", str(ans), [str(x) for x in near(s2, ix_ + 3)],
   "Read the step, then count", f"Step II: {line(s2)}. Three places to the right of 'nova' is {ans}.",
   [f"Step II: {line(s2)}"], seconds=85)
first = next(i for i, s_ in enumerate(st) if "ranul" in s_)
IQ("At which step is the reversed word 'ranul' first placed on the right side of the line?", f"Step {ROMAN[first]}",
   [f"Step {ROMAN[i]}" for i in range(5) if i != first][:3], "Order of the word moves",
   "lunar is the fourth word from the end of the alphabet among the five, so it is reversed to 'ranul' in Step IV.",
   step_txt(st), natural=lambda t: ROMAN.index(t.split()[1]), seconds=80)
pos9 = st[-1].index(9) + 1
IQ("In the last step, what is the position of '9' from the left end?", ORDN(pos9),
   [ORDN(k) for k in (pos9 - 1, pos9 + 1, pos9 + 2)], "Results are placed left to right in the order chosen",
   f"Last step: {line(st[-1])}. 36 is the third number chosen, so its digit sum 9 is in the {ORDN(pos9)} place.",
   [f"Last step: {line(st[-1])}"], natural=lambda t: int(t[:-2]), seconds=80)

# ================================================================================================ DATA SUFFICIENCY
TS, THS = "Two-statement", "Three-statement"


def ds_opts(ans):
    keys = "ABNT" if ans == "N" else "ABET" if ans == "E" else "ABNT" if ans in "ABT" else None
    assert ans in keys
    return [DS2[k] for k in keys]


models = [{"d": d} for d in range(1, 32)]
got = ds2(models, lambda m: m["d"] % 2 == 0 and m["d"] > 26, lambda m: m["d"] % 7 == 0, lambda m: m["d"])
assert got == "T"
fixed(DSF, TS, "Basic", DS_HEAD + "Question: On which date in March was Rohan born?\n\nI. Rohan was born on an even "
      "date after 26 March.\nII. Rohan was born on a date that is a multiple of 7.", ds_opts("T"), DS2["T"],
      "Test each statement alone, then together",
      "I allows 28 or 30 March; II allows 7, 14, 21 or 28 March. Only 28 March satisfies both.",
      ["I alone: 28 or 30 ⇒ not sufficient", "II alone: 7, 14, 21, 28 ⇒ not sufficient", "Together: 28 March"],
      seconds=40, verified_by=ENUM)
P = list("PQRST")
models = [dict(zip(P, p)) for p in itertools.permutations(range(1, 6))]
got = ds2(models, lambda m: m["Q"] == 3 and m["R"] == 4, lambda m: m["S"] == 2 and m["T"] > m["R"],
          lambda m: next(k for k in P if m[k] == 5))
assert got == "T"
fixed(DSF, TS, "Intermediate", DS_HEAD + "Question: Five persons P, Q, R, S and T live on the five floors of a "
      "building, one on each floor (floor 1 is the lowermost). Who lives on floor 5?\n\nI. Q lives on floor 3, and R "
      "lives immediately above Q.\nII. S lives on floor 2, and T lives on a floor above R.", ds_opts("T"), DS2["T"],
      "Combine floor clues", "I fixes Q (3) and R (4), but floor 5 could be P, S or T. II alone does not fix R. Together, "
      "T is above R (4), so T is on floor 5.",
      ["I alone: floor 5 open ⇒ not sufficient", "II alone: R unknown ⇒ not sufficient", "Together: T above floor 4 ⇒ T"],
      seconds=55, verified_by=ENUM)
P = list("ABCDEF")
models = [dict(zip(P, (0,) + p)) for p in itertools.permutations(range(1, 6))]
got = ds2(models, lambda m: m["B"] == (m["A"] + 1) % 6 and m["C"] == (m["B"] + 2) % 6,
          lambda m: (m["D"] - m["E"]) % 6 == 3 and (m["F"] - m["A"]) % 6 not in (1, 5),
          lambda m: next(k for k in P if m[k] == (m["A"] + 3) % 6))
assert got == "A"
fixed(DSF, TS, "Intermediate", DS_HEAD + "Question: Six friends A, B, C, D, E and F sit around a circular table, "
      "equally spaced and all facing the centre. Who sits opposite A?\n\nI. B sits immediately to the right of A, and C "
      "sits second to the right of B.\nII. D sits opposite E, and F is not an immediate neighbour of A.", ds_opts("A"),
      DS2["A"], "Opposite = three places away in a circle of six",
      "I: B is one place and C three places to A's right, so C sits opposite A — sufficient. II: D and E face each other "
      "and F is not next to A, but A's opposite could be F, or one of D and E — not sufficient.",
      ["I: C = A + 3 ⇒ opposite A", "II: several seatings remain"], seconds=60, verified_by=ENUM)


def code_models(sents):
    words = sorted({w for ws, _ in sents for w in ws})
    codes = sorted({c for _, cs in sents for c in cs})
    return [dict(zip(words, p)) for p in itertools.permutations(codes)
            if all({dict(zip(words, p))[w] for w in ws} == set(cs) for ws, cs in sents)]


S1 = [(["gold", "bond"], ["xi", "ra"]), (["bond", "yield"], ["ra", "lu"])]
S2 = [(["gold", "price"], ["xi", "mo"]), (["price", "rise"], ["mo", "te"])]
assert {m["gold"] for m in code_models(S1)} == {"xi"} and {m["gold"] for m in code_models(S2)} == {"xi"}
fixed(DSF, TS, "Intermediate", DS_HEAD + "Question: In a certain code language, what is the code for 'gold'?\n\n"
      "I. 'gold bond' is written as 'xi ra', and 'bond yield' is written as 'ra lu'.\nII. 'gold price' is written as "
      "'xi mo', and 'price rise' is written as 'mo te'.", ds_opts("E"), DS2["E"],
      "Each statement on its own", "I: bond = ra (common code), so gold = xi. II: price = mo (common code), so gold = "
      "xi. Each statement alone answers the question.", ["I: bond = ra ⇒ gold = xi", "II: price = mo ⇒ gold = xi"],
      seconds=55, verified_by=ENUM)
models = [{"n": n, "m": m, "k": k} for n in range(20, 80) for m in range(1, n + 1) for k in range(1, n + 1) if m != k]
got = ds2(models, lambda x: x["m"] == 9, lambda x: x["k"] == x["m"] + 6 and x["n"] - x["k"] + 1 == 30,
          lambda x: x["n"])
assert got == "T"
fixed(DSF, TS, "Intermediate", DS_HEAD + "Question: How many students are there in the class?\n\nI. Meera is 9th "
      "from the top.\nII. Meera is 6 ranks above Kunal, and Kunal is 30th from the bottom.", ds_opts("T"), DS2["T"],
      "One person's rank from both ends gives the total",
      "I alone gives only Meera's rank from the top. II alone links Meera and Kunal but gives no rank from the top. "
      "Together, Kunal is 9 + 6 = 15th from the top and 30th from the bottom: 15 + 30 − 1 = 44 students.",
      ["I alone ⇒ not sufficient", "II alone ⇒ not sufficient", "Together: Kunal 15th from top, 30th from bottom ⇒ 44"],
      seconds=60, verified_by=ENUM)
models = [{"r": r, "s": s} for r in range(1, 100) for s in range(1, 100)]
got = ds2(models, lambda m: m["r"] == m["s"] + 5, lambda m: m["s"] % 7 == 0, lambda m: m["r"])
assert got == "N"
fixed(DSF, TS, "Intermediate", DS_HEAD + "Question: What is Ravi's present age?\n\nI. Ravi is 5 years older than "
      "Sunil.\nII. Sunil's present age is a multiple of 7.", ds_opts("N"), DS2["N"],
      "A relation plus a family of values is still not a single value",
      "I links the two ages; II allows Sunil to be 7, 14, 21, … Together Ravi could be 12, 19, 26, … — no single "
      "answer.", ["I alone ⇒ not sufficient", "II alone ⇒ not sufficient", "Together: Ravi = 12, 19, 26, … ⇒ still "
                                                                              "not sufficient"],
      seconds=45, verified_by=ENUM)
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
models = [{"d": d} for d in range(7)]
got = ds2(models, lambda m: m["d"] in (2, 4), lambda m: m["d"] == 2, lambda m: m["d"])
assert got == "B"
fixed(DSF, TS, "Intermediate", DS_HEAD + "Question: On which day of the week did Gita visit the bank?\n\nI. Gita "
      "visited the bank on the day after Tuesday or on the day before Saturday.\nII. Gita visited the bank three days "
      "after Sunday.", ds_opts("B"), DS2["B"], "Test each statement alone",
      "I allows Wednesday or Friday — not sufficient. II: three days after Sunday is Wednesday — sufficient.",
      ["I: Wednesday or Friday ⇒ not sufficient", "II: Sunday + 3 = Wednesday ⇒ sufficient"], seconds=45,
      verified_by=ENUM)
# ---- Advanced: three statements
P = list("PQRST")
models = [dict(zip(P, p)) for p in itertools.permutations(range(5))]  # larger = taller
fns = [lambda m: m["P"] > m["Q"] and m["P"] > m["R"], lambda m: m["S"] > m["T"],
       lambda m: m["Q"] > m["R"] > m["T"] and m["P"] > m["T"]]
got = ds3(models, fns, lambda m: min(P, key=m.get))
assert got == "II+III"
fixed(DSF, THS, "Advanced", DS3_HEAD + "Question: Among P, Q, R, S and T, each of a different height, who is the "
      "shortest?\n\nI. P is taller than both Q and R.\nII. S is taller than T.\nIII. Q is taller than R, R is taller "
      "than T, and P is taller than T.", [DS3[k_] for k_ in ("I+II", "II+III", "ALL", "NONE")], DS3["II+III"],
      "Three-statement data sufficiency: test every pair",
      "III puts T below P, Q and R; II puts T below S. So II + III make T the shortest. I + II leaves R, Q or T as the "
      "shortest. I + III fixes P, Q, R above T but says nothing about S. No statement alone is enough.",
      ["II + III: T below P, Q, R and S ⇒ T shortest", "I + II and I + III: S or T/R undecided"], seconds=75,
      verified_by=ENUM)
models = [{"m": m, "s": s, "r": r} for m in range(1, 41) for s in range(1, 41) for r in range(1, 41)
          if len({m, s, r}) == 3]
fns = [lambda x: x["m"] == x["s"] + 5, lambda x: 40 - x["s"] + 1 == 18, lambda x: x["r"] == x["s"] - 3]
got = ds3(models, fns, lambda x: x["m"])
assert got == "I+II"
fixed(DSF, THS, "Advanced", DS3_HEAD + "Question: What is Mohan's rank from the top in a class of 40 students?\n\n"
      "I. Mohan is 5 ranks below Sohan.\nII. Sohan is 18th from the bottom.\nIII. Rohan is 3 ranks above Sohan.",
      [DS3[k_] for k_ in ("I+II", "I+III", "ALL", "NONE")], DS3["I+II"], "Find the statement that only distracts",
      "I + II: Sohan is 40 − 18 + 1 = 23rd from the top, so Mohan is 28th — sufficient. III only links Rohan to Sohan, "
      "and no statement gives Rohan's rank, so I + III and II + III cannot fix Mohan. Statement III is not needed.",
      ["I + II: Sohan 23rd ⇒ Mohan 28th", "I + III and II + III: not sufficient"], seconds=75, verified_by=ENUM)

# ================================================================================================ VERBAL REASONING
# Hand-written items. Each was solved by the author; BLIND_OK (set at the end of this section) lists the items that a
# separate, fresh solver answered blind (from a key-free dump) with the same key. Only those carry
# ai:independent-check; the rest keep ai:self-recheck.
VERBAL_IDS = []
ASM = "Statement and Assumptions"
AOPT = ["Only assumption I is implicit", "Only assumption II is implicit", "Neither I nor II is implicit",
        "Both I and II are implicit"]
A_I, A_II, A_N, A_B = AOPT
A_HEAD = ("Read the statement and the two assumptions. An assumption is something supposed or taken for granted by "
          "the person making the statement. Decide which of the assumptions is/are implicit in the statement.\n\n")


def asm(diff, statement, a1, a2, answer, explanation, steps, why, seconds=45):
    q_ = fixed(ASM, "Implicit assumptions", diff, A_HEAD + f"Statement: {statement}\n\nAssumptions:\nI. {a1}\nII. {a2}",
               AOPT, answer, "Implicit assumption: what the speaker must take for granted", explanation, steps,
               why_others_wrong=why, seconds=seconds)
    VERBAL_IDS.append(q_["question_id"])


asm("Intermediate", "A school has decided to send an SMS to a student's parents on every day the student is absent.",
    "The parents of the students can receive SMS messages.",
    "Students are absent from school only when they are ill.", A_I,
    "Sending absence alerts by SMS makes sense only if the parents can receive such messages (I). The plan says nothing "
    "about why students are absent; it does not need absences to be caused only by illness (II).",
    ["Alerts by SMS ⇒ parents can receive SMS: I implicit", "Reason for absence is irrelevant to the plan ⇒ II not "
                                                             "implicit"],
    "Only II and Both accept a claim about the cause of absence that the plan does not rely on; Neither ignores the "
    "premise of the SMS plan.", seconds=40)

# ================================================================================================ STATEMENT-CONCLUSION
SCN = "Statement and Conclusions"
SC_HEAD = ("Read the statement and the two conclusions. Assume everything in the statement to be true, and decide "
           "which conclusion(s) logically follow from it.\n\n")
VC, INF = "Valid conclusions", "Inferences"


def scq(diff, sub, statement, c1, c2, answer, explanation, steps, why, seconds=45):
    q_ = fixed(SCN, sub, diff, SC_HEAD + f"Statement: {statement}\n\nConclusions:\nI. {c1}\nII. {c2}",
               conclusion_options(answer), answer, "A conclusion must follow from the statement alone", explanation,
               steps, why_others_wrong=why, seconds=seconds)
    VERBAL_IDS.append(q_["question_id"])


scq("Basic", VC, "Every passenger on the 7:40 am ferry today carried a life jacket. Ritu travelled on the 7:40 am "
    "ferry today.", "Ritu carried a life jacket today.", "Ritu travels on the 7:40 am ferry every day.", ONLY_I,
    "Ritu was one of the passengers on that ferry today, and every such passenger carried a life jacket, so I follows. "
    "Nothing is said about her travel on other days, so II does not follow.",
    ["Every passenger on that ferry today had a life jacket; Ritu was one ⇒ I", "Other days are not mentioned ⇒ II "
                                                                               "does not follow"],
    "Only II and Both rely on information about other days that is not given.", seconds=30)
scq("Basic", INF, "The town library is open from 9 am to 5 pm on every weekday (Monday to Friday) and is closed on "
    "Sundays.", "A visitor who arrives at the library at 6 pm on a Wednesday will find it closed.",
    "The library is open on Saturdays.", ONLY_I,
    "Wednesday is a weekday, and on weekdays the library is open only from 9 am to 5 pm, so at 6 pm it is closed (I). "
    "The statement gives no information about Saturdays, so II does not follow.",
    ["Weekday hours end at 5 pm ⇒ closed at 6 pm on Wednesday: I", "Saturday is not covered ⇒ II does not follow"],
    "Only II and Both assume something about Saturdays; Neither ignores the stated weekday hours.", seconds=35)
scq("Basic", INF, "A box contains only red pens and blue pens. It has 12 red pens, and the number of blue pens in it is "
    "twice the number of red pens.", "The box has 24 blue pens.", "The box has 36 pens in all.", BOTH,
    "Blue pens = 2 × 12 = 24 (I). Since the box holds only red and blue pens, the total is 12 + 24 = 36 (II).",
    ["Blue = 2 × 12 = 24 ⇒ I", "Only two colours ⇒ total = 12 + 24 = 36 ⇒ II"],
    "Each 'Only' option drops one of two direct calculations.", seconds=35)
scq("Basic", INF, "The sales of a garment shop doubled in December compared with November.",
    "The shop reduced its prices in December.", "The shop's profit doubled in December.", NEITHER,
    "The statement gives only the change in sales. The reason (a price cut, a festival, new stock) is not given, so I "
    "does not follow; profit depends on costs and prices, which are not given, so II does not follow.",
    ["Cause of the rise is not stated ⇒ I does not follow", "Sales ≠ profit ⇒ II does not follow"],
    "The other options accept a cause or a profit figure that the statement does not supply.", seconds=35)
scq("Basic", VC, "All the employees of the branch attended the training session on Saturday. Meena did not attend the "
    "training session on Saturday.", "Meena was on leave on Saturday.", "Meena is not an employee of the branch.",
    ONLY_II,
    "If Meena were an employee of the branch she would have attended, since all of them did; she did not, so she is not "
    "an employee of the branch (II). Why she did not attend is not stated, so I does not follow.",
    ["All employees attended; Meena did not ⇒ Meena is not an employee: II", "No reason is given for her absence ⇒ I "
                                                                              "does not follow"],
    "Only I and Both guess a reason; Neither misses the direct contrapositive.", seconds=35)
scq("Advanced", INF, "A tank holds 1,200 litres when full. It is now one-quarter full, and water is being pumped into it "
    "at a steady 50 litres per minute, with nothing flowing out.", "The tank will be full in 18 minutes.",
    "The tank will be at least half full within 5 minutes.", ONLY_I,
    "The tank now holds 1,200 ÷ 4 = 300 litres and needs 900 more; at 50 litres a minute that takes 18 minutes (I). "
    "After 5 minutes it holds 300 + 250 = 550 litres, less than half (600), so II is false.",
    ["Now: 300 L; needed: 900 L ⇒ 900 ÷ 50 = 18 min ⇒ I", "After 5 min: 550 L < 600 L ⇒ II false"],
    "Only II and Both accept a figure the arithmetic rules out; Neither ignores the direct calculation.", seconds=60)
scq("Advanced", VC, "In a housing society, no flat on the ground floor has a balcony, and every flat that has a balcony "
    "has two bedrooms. Flat 104 of the society has a balcony.", "Flat 104 is not on the ground floor.",
    "Flat 104 has two bedrooms.", BOTH,
    "A ground-floor flat never has a balcony; flat 104 has one, so it is not on the ground floor (I). Every flat with a "
    "balcony has two bedrooms, so flat 104 has two bedrooms (II).",
    ["No ground-floor flat has a balcony; 104 has one ⇒ not on the ground floor: I",
     "Balcony ⇒ two bedrooms ⇒ II"], "Each 'Only' option drops one of two valid deductions.", seconds=55)
scq("Advanced", VC, "Every train that runs from Station X to Station Y stops at Station Z. Train 12 does not stop at "
    "Station Z.", "Train 12 does not stop at Station Y.", "Train 12 does not run from Station X to Station Y.", ONLY_II,
    "If Train 12 ran from X to Y it would stop at Z; it does not stop at Z, so it does not run from X to Y (II). It may "
    "still stop at Y on some other route, so I does not follow.",
    ["X→Y trains all stop at Z; Train 12 skips Z ⇒ not an X→Y train: II", "It may reach Y from elsewhere ⇒ I does not "
                                                                         "follow"],
    "Only I and Both turn 'not an X–Y train' into 'never stops at Y'.", seconds=55)
scq("Advanced", INF, "The results of the examination will be declared either on 10 June or on 15 June, depending on "
    "when the evaluation of the answer sheets is completed.", "The results will be declared on 10 June.",
    "The evaluation of the answer sheets will be completed by 9 June.", NEITHER,
    "The statement leaves both dates open, so I is not certain. It does not say when evaluation will finish, so II is "
    "not certain either; and the two conclusions are not a complementary pair (II is not the same as 'results on "
    "15 June'), so 'either' does not apply.",
    ["Two possible dates ⇒ I uncertain", "Completion date not given ⇒ II uncertain",
     "I and II are not exact opposites ⇒ not an 'either' case"],
    "Only I, Only II and Either each treat one open possibility as settled.", seconds=55)

# ================================================================================================ CAUSE AND EFFECT
CAE = "Cause and Effect"
CE = {"A": "Statement I is the cause and statement II is its effect",
      "B": "Statement II is the cause and statement I is its effect",
      "C": "Both the statements I and II are independent causes",
      "D": "Both the statements I and II are effects of independent causes",
      "E": "Both the statements I and II are effects of some common cause"}
CE_HEAD = ("Below are two statements, I and II. They may be independent causes, effects of independent causes or of "
           "a common cause, or one may be the effect of the other. Decide the relationship.\n\n")
IND, COM = "Independent causes", "Common cause"


def ceq(sub, s1, s2, answer, explanation, steps, why, seconds=45):
    keys = [k_ for k_ in "ABCDE" if k_ != "C"]
    q_ = fixed(CAE, sub, "Intermediate", CE_HEAD + f"I. {s1}\nII. {s2}", [CE[k_] for k_ in keys], CE[answer],
               "Cause and effect: look for a direct link, a shared trigger, or none", explanation, steps,
               why_others_wrong=why, seconds=seconds)
    VERBAL_IDS.append(q_["question_id"])


ceq(IND, "A landslide on Monday morning blocked the only road leading to the hill village.",
    "Trucks carrying vegetables could not reach the hill village on Monday.", "A",
    "With its only road blocked, no truck could reach the village that day. I explains II directly.",
    ["I: the only road is blocked", "II: supply trucks cannot reach the village the same day",
     "Blocked road → no truck access ⇒ I is the cause"],
    "Trucks failing to arrive cannot cause a landslide, so B is impossible; no third event is needed.", seconds=40)
ceq(IND, "The municipal corporation closed the city's main swimming pool to the public for a month.",
    "Inspectors found deep cracks in the walls of the city's main swimming pool.", "B",
    "Cracks in the pool's walls make it unsafe, and closing the pool for repairs is the natural response. II is the "
    "cause and I its effect.", ["II: structural cracks found", "I: pool closed for a month",
                                "Unsafe structure → closure ⇒ II is the cause"],
    "Closing a pool does not create cracks, so A is impossible.", seconds=40)
ceq(COM, "Sales of sweaters and blankets in the hill town rose sharply this week.",
    "Schools in the hill town moved their morning start time one hour later this week.", "E",
    "Buying sweaters does not make schools change their timings, and later school timings do not make people buy "
    "woollens. Both are standard responses to one event — a sharp drop in temperature (a cold wave) in the town this "
    "week.", ["No direct link between the two", "Both are typical responses to the same cold spell",
              "⇒ effects of a common cause"],
    "Effects of independent causes would need two unrelated reasons that happened in the same town in the same week; "
    "one cold wave explains both.", seconds=45)
ceq(IND, "The state government raised the salaries of its employees by 8%.",
    "A private airline started new flights between two cities of the state.", "D",
    "A salary revision results from the government's pay decisions; new flights result from an airline's business "
    "plans. Neither explains the other, and no single event explains both.",
    ["I: outcome of a government pay decision", "II: outcome of an airline's business decision",
     "No link and no shared trigger ⇒ effects of independent causes"],
    "A common cause would need one event behind both a pay rise and an airline's route plan; nothing suggests one.",
    seconds=40)
ceq(IND, "The bank's central server stopped working for six hours on Friday.",
    "Customers of the bank could not use its mobile banking app for six hours on Friday.", "A",
    "A mobile banking app depends on the bank's server; while the server is down, the app cannot work. I explains II, "
    "and the durations match.", ["I: server down for six hours", "II: app unusable for the same six hours",
                                 "App depends on the server ⇒ I is the cause"],
    "Customers being unable to use the app cannot bring the server down, so B fails; the server failure fully explains "
    "the outage, so no separate common cause is needed.", seconds=45)
ceq(IND, "The railway has added four extra coaches to the Pune–Nagpur express.",
    "The Pune–Nagpur express has had long waiting lists every day for the past three months.", "B",
    "Long, persistent waiting lists show that demand exceeds the seats available; adding coaches is the railway's "
    "response. II is the cause and I its effect.",
    ["II: demand has exceeded seats for three months", "I: extra coaches added", "Excess demand → more coaches"],
    "Adding coaches now cannot have caused waiting lists over the past three months, so A is impossible.", seconds=40)

# ================================================================================================ CRITICAL REASONING
CRT = "Critical Reasoning"
SW_, CA_, INFP = "Strengthen and weaken", "Course of action", "Inference from a passage"


def crq(diff, sub, text, correct, wrongs, concept, explanation, steps, why, seconds=60):
    q_ = mcq(CRT, sub, diff, text, correct, wrongs, concept, explanation, steps, why_others_wrong=why, seconds=seconds)
    VERBAL_IDS.append(q_["question_id"])


crq("Basic", CA_, "Statement: Residents of a colony complain that the streetlights on their main road have not worked "
    "for two weeks, and two thefts have taken place on that road at night during this time.\n\nWhich of the following "
    "is the most appropriate course of action?",
    "Repair the streetlights quickly and increase police patrolling on the road at night",
    ["Ask the residents not to leave their homes after dark", "Remove the streetlights from the road",
     "Shift the residents of the colony to another area"], "A course of action should remove the stated problem",
    "The problems are dark streets and night-time thefts. Fixing the lights and adding patrols address both directly.",
    ["Problem: no streetlights; thefts at night", "Remedy: repair lights; more patrols"],
    "Confining residents indoors or moving them away is impractical; removing the lights makes things worse.",
    seconds=30)
crq("Advanced", SW_, "Argument: The city's ban on plastic bags in shops has reduced the amount of plastic waste the "
    "city produces, because the number of plastic bags reaching the city landfill fell by 40% in the six months after "
    "the ban.\n\nWhich of the following, if true, most seriously weakens the argument?",
    "During the same six months, a new recycling unit began collecting most plastic waste directly from homes, so much "
    "less plastic of every kind reached the landfill",
    ["Many shopkeepers supported the ban when it was announced", "Cloth bags cost more than plastic bags",
     "The ban was widely reported in the city's newspapers"],
    "Weaken: the measured fall may come from a change in where waste goes, not from less waste",
    "The evidence is the count of bags at the landfill. If a new unit diverted plastic away from the landfill, the "
    "count would fall even if the city produced as much plastic waste as before, so the evidence no longer supports "
    "the conclusion.",
    ["Evidence: fewer bags at the landfill", "Conclusion: less plastic waste produced",
     "Weakener: plastic diverted to recycling ⇒ landfill count no longer measures waste produced"],
    "Shopkeepers' support, the price of cloth bags and press coverage say nothing about how much plastic waste the city "
    "produces.", seconds=75)

# Blind check (2026-11-06): a fresh solver answered all 18 items from a key-free dump and matched every key.
# BANK_REAS_000999 was then replaced by a clearer common-cause scenario and re-answered blind by a second fresh
# solver, who matched the key again.
BLIND_OK = {f"BANK_REAS_{n:06d}" for n in range(987, 1005)}
assert BLIND_OK == set(VERBAL_IDS)

# ================================================================================================ WRITE
plan = json.loads((ROOT / "batches" / "plans" / "BATCH_005_plan.json").read_text(encoding="utf-8"))
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
assert BLIND_OK <= set(VERBAL_IDS)
for x in QUESTIONS:
    if x["question_id"] in BLIND_OK:
        x["verification"]["verified_by"] = list(HAND)
print(f"{len(QUESTIONS)} questions, {len(STIMULI)} stimuli, keys {dict(sorted(KEYCOUNT.items()))}, "
      f"blind-matched {len(BLIND_OK)}/{len(VERBAL_IDS)}")
if "--dump-verbal" in sys.argv:  # key-free dump of the hand-written items for the blind solver
    VERBAL = {"Statement and Assumptions", "Statement and Conclusions", "Cause and Effect", "Critical Reasoning"}
    out_ = [{"id": x["question_id"], "text": x["question_text"], "options": x["options"]} for x in QUESTIONS
            if x["topic"] in VERBAL]
    Path(sys.argv[sys.argv.index("--dump-verbal") + 1]).write_text(json.dumps(out_, indent=1, ensure_ascii=False),
                                                                   encoding="utf-8")
    print("dumped", len(out_))
if CHECK_QUOTA:
    assert len(QUESTIONS) == splan["total"] == 200
    assert QUESTIONS[0]["question_id"] == splan["question_ids"][0]
    assert QUESTIONS[-1]["question_id"] == splan["question_ids"][1]
    assert max(KEYCOUNT.values()) - min(KEYCOUNT.values()) <= 12, KEYCOUNT
    doc = {
        "schema_version": "1.0",
        "batch_id": "BATCH_005",
        "created_at": TODAY,
        "notes": ("Reasoning Ability part of BATCH_005: 200 original questions (60 Basic, 80 Intermediate, 60 "
                  "Advanced) built by tools/batch_005/reasoning.py. New puzzle structures and noun sets. Puzzles are "
                  "brute-forced for a unique arrangement; syllogisms are checked over every Venn-region model; "
                  "inequalities over all integer assignments; data sufficiency by enumerating models for each "
                  "statement subset; blood relations, directions, coding (inferred rules checked against "
                  "alternative simple rules), series, alphabet, number operations, ranking and input-output are "
                  "recomputed in code. Verbal-reasoning items are hand-written and were re-answered blind by a "
                  "separate solver. All questions await human review."),
        "stimuli": STIMULI,
        "questions": QUESTIONS,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {OUT}")
