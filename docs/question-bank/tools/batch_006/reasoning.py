"""Builds batches/parts/BATCH_006_REAS.json: the 200 Reasoning Ability questions of BATCH_006.

Same method and helpers as tools/batch_005/reasoning.py, with new puzzle structures, noun sets and scenarios:
- puzzles and seating: the conditions are written once as (text, variables, test) triples; the text goes into the
  stimulus (or the question) and the test into an exhaustive backtracking search that must return exactly one
  arrangement. Every answer is then read off that arrangement;
- syllogisms: checked over every Venn-region model; inequalities: exhaustive integer assignments;
- blood relations (explicit family tree), directions, coding (inferred rules are checked against a library of
  alternative simple rules), series, alphabet, number operations, ranking and input-output: recomputed in code;
  data sufficiency: each statement subset checked by enumerating models.
Verbal-reasoning items (assumptions, conclusions, cause and effect, critical reasoning) are hand-written; they carry
ai:independent-check only after a separate, fresh solver answered them blind and matched the key.
If any assertion fails, nothing is written. --draft prints quota gaps instead of asserting them;
--dump-verbal <path> writes a key-free dump of the verbal items for the blind solver.

    python tools/batch_006/reasoning.py        (run from docs/question-bank)
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
OUT = ROOT / "batches" / "parts" / "BATCH_006_REAS.json"
TODAY = "2026-11-05"
RA = "Reasoning Ability"
LETTERS = "ABCD"
FIRST_Q, FIRST_STIM = 1005, 6001
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
    # exhaustive backtracking over all integer assignments in range(dom) (same set as a full product, pruned early)
    sats = solve(vs, {x: range(dom) for x in vs}, [((a, b), (lambda x, y, o=o: REL[o](x, y))) for a, o, b in rels])
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

# ---- L1 Basic (standalone): a queue of six persons at a counter (position 1 = front)
P = ["Darpana", "Jishnu", "Kalyan", "Mrinalini", "Sohan", "Tvisha"]
conds = [("Kalyan stands third from the front of the queue.", ("Kalyan",), lambda k: k == 3),
         ("Only one person stands between Kalyan and Tvisha, and Tvisha stands behind Kalyan.", ("Kalyan", "Tvisha"),
          lambda k, t: t == k + 2),
         ("Jishnu stands immediately in front of Tvisha.", ("Jishnu", "Tvisha"), lambda j, t: j == t - 1),
         ("Darpana stands immediately in front of Kalyan.", ("Darpana", "Kalyan"), lambda d, k: d == k - 1),
         ("Sohan does not stand at the front of the queue.", ("Sohan",), lambda s: s != 1)]
Q1 = unique(P, {p: range(1, 7) for p in P}, conds, [P])
at = {v: k for k, v in Q1.items()}
assert [at[i] for i in range(1, 7)] == ["Mrinalini", "Darpana", "Kalyan", "Jishnu", "Tvisha", "Sohan"]
cnt = abs(Q1["Mrinalini"] - Q1["Jishnu"]) - 1
assert cnt == 2
mcq(LIN, SGL, "Basic",
    "Six persons Darpana, Jishnu, Kalyan, Mrinalini, Sohan and Tvisha stand in a single queue at a ticket counter, one "
    "behind another, all facing the counter.\n" + bullets(conds) +
    "\n\nHow many persons stand between Mrinalini and Jishnu?", num_word(cnt), ["One", "Three", "Four"],
    "A queue is a row: count positions from the front",
    "Kalyan is 3rd and Tvisha 5th; Jishnu is 4th and Darpana 2nd. Positions 1 and 6 remain for Mrinalini and Sohan; "
    "Sohan is not at the front, so Mrinalini is 1st and Sohan 6th. Between Mrinalini (1st) and Jishnu (4th) stand "
    "Darpana and Kalyan: two persons.",
    ["Kalyan 3, Tvisha 5, Jishnu 4, Darpana 2", "Sohan not 1st ⇒ Mrinalini 1, Sohan 6",
     "Between 1 and 4: positions 2, 3 ⇒ two"],
    why_others_wrong="One and Three miscount the positions between 1st and 4th; Four counts Mrinalini and Jishnu too.",
    natural=by_num, seconds=40, verified_by=BRUTE)

# ---- L2 Basic (standalone): five persons facing south, each owning a vehicle (seats 1..5 from the west)
P = ["Gautami", "Hriday", "Ojasvi", "Pulkit", "Upasana"]
VH = ["Bicycle", "Car", "Jeep", "Scooter", "Tractor"]
F_ = ["v" + p for p in P]
VV = P + F_
IXV = {v: i for i, v in enumerate(VV)}
own = lambda v, x: next(v[IXV[p]] for p in P if v[IXV["v" + p]] == x)
conds = [("Ojasvi sits at the west end of the row.", ("Ojasvi",), lambda o: o == 1),
         ("Upasana sits second to the left of Ojasvi and owns the Jeep.", ("Upasana", "Ojasvi", "vUpasana"),
          lambda u, o, v: u == o + 2 and v == "Jeep"),
         ("Hriday sits immediately to the right of Upasana.", ("Hriday", "Upasana"), lambda h, u: h == u - 1),
         ("Pulkit owns the Car and sits at an extreme end of the row.", ("Pulkit", "vPulkit"),
          lambda p, v: p in (1, 5) and v == "Car"),
         ("The person who owns the Scooter sits immediately to the left of the person who owns the Tractor.",
          tuple(VV), lambda *v: own(v, "Scooter") == own(v, "Tractor") + 1)]
Q2 = unique(VV, {p: range(1, 6) for p in P} | {f: VH for f in F_}, conds, [P, F_])
assert [(p, Q2[p], Q2["v" + p]) for p in sorted(P, key=Q2.get)] == [
    ("Ojasvi", 1, "Tractor"), ("Hriday", 2, "Scooter"), ("Upasana", 3, "Jeep"), ("Gautami", 4, "Bicycle"),
    ("Pulkit", 5, "Car")]
ans = next(p for p in P if Q2["v" + p] == "Bicycle")
assert ans == "Gautami"
mcq(LIN, SGL, "Basic",
    "Five persons Gautami, Hriday, Ojasvi, Pulkit and Upasana sit in a straight row, all facing south. Each owns a "
    "different vehicle among Bicycle, Car, Jeep, Scooter and Tractor. (Facing south, a person's right is towards the "
    "west and the left towards the east.)\n" + bullets(conds) + "\n\nWho owns the Bicycle?", ans,
    ["Hriday", "Ojasvi", "Upasana"], "Facing south reverses left and right",
    "Number the seats 1 to 5 from the west. Ojasvi = 1. Facing south, the left is east, so Upasana (Jeep) = 3, and "
    "Hriday, immediately to her right (west), = 2. Pulkit (Car) is at an end: seat 5, so Gautami = 4. The Scooter owner "
    "is immediately to the left (east) of the Tractor owner; among seats 1, 2 and 4 the only adjacent pair is 1–2, so "
    "the Tractor owner is Ojasvi (1) and the Scooter owner Hriday (2), leaving the Bicycle for Gautami.",
    ["Ojasvi 1; Upasana 3 (Jeep); Hriday 2", "Pulkit 5 (Car) ⇒ Gautami 4",
     "Scooter immediately east of Tractor ⇒ Ojasvi Tractor, Hriday Scooter", "Gautami ⇒ Bicycle"],
    why_others_wrong="Hriday owns the Scooter, Ojasvi the Tractor and Upasana the Jeep.", seconds=50,
    verified_by=BRUTE)

# ---- L3 Intermediate (standalone): eight persons, immediate neighbours always face opposite directions
P = ["Arundhati", "Bikram", "Damayanti", "Ganesh", "Kartikeya", "Niharika", "Shreyas", "Vaidehi"]
fac = lambda f1, s: f1 if s % 2 == 1 else ("S" if f1 == "N" else "N")  # f1 = facing of seat 1; facing alternates
RS = lambda s, f, k: s + k if f == "N" else s - k
conds = [
    ("Ganesh sits third from the west end and faces south.", ("Ganesh", "f1"), lambda g, f: g == 3 and fac(f, g) == "S"),
    ("Niharika sits second to the right of Ganesh.", ("Niharika", "Ganesh", "f1"),
     lambda n, g, f: n == RS(g, fac(f, g), 2)),
    ("Shreyas sits third to the left of Niharika.", ("Shreyas", "Niharika", "f1"),
     lambda s, n, f: s == RS(n, fac(f, n), -3)),
    ("Vaidehi sits at an extreme end of the row and faces north.", ("Vaidehi", "f1"),
     lambda v, f: v in (1, 8) and fac(f, v) == "N"),
    ("Bikram sits immediately to the left of Vaidehi.", ("Bikram", "Vaidehi", "f1"),
     lambda b, v, f: b == RS(v, fac(f, v), -1)),
    ("Kartikeya is not an immediate neighbour of Shreyas.", ("Kartikeya", "Shreyas"), lambda k, s: abs(k - s) != 1),
    ("Arundhati faces the same direction as Ganesh, and Damayanti sits somewhere to the east of Arundhati.",
     ("Damayanti", "Arundhati", "f1"), lambda d, a, f: d > a and fac(f, a) == "S"),
]
L3 = unique(P + ["f1"], {p: range(1, 9) for p in P} | {"f1": "NS"}, conds, [P])
at = {L3[p]: p for p in P}
assert [at[i] for i in range(1, 9)] == ["Niharika", "Kartikeya", "Ganesh", "Shreyas", "Arundhati", "Damayanti",
                                        "Bikram", "Vaidehi"] and L3["f1"] == "S"
ans = at[RS(L3["Arundhati"], fac("S", L3["Arundhati"]), -2)]
assert ans == "Bikram"
mcq(LIN, SGL, "Intermediate",
    "Eight persons Arundhati, Bikram, Damayanti, Ganesh, Kartikeya, Niharika, Shreyas and Vaidehi sit in a straight row. "
    "Some face north and the others face south, and any two immediate neighbours face opposite directions. (Facing "
    "north, the right is east; facing south, the right is west.)\n" + bullets(conds) +
    "\n\nWho sits second to the left of Arundhati?", ans, ["Ganesh", "Damayanti", "Vaidehi"],
    "Alternating facing: one person's facing fixes everyone's",
    "Number the seats 1 to 8 from the west. Ganesh (seat 3) faces south, so every odd seat faces south and every even "
    "seat north. Niharika is second to Ganesh's right (west): seat 1, facing south; Shreyas is third to her left (east): "
    "seat 4. Vaidehi faces north from an end, so she is at seat 8; Bikram, immediately to her left (west), is at 7. "
    "Seats 2, 5 and 6 remain. Arundhati faces south, so she is at 5; Kartikeya cannot sit next to Shreyas, so he is at "
    "2, and Damayanti at 6 (east of Arundhati). Arundhati faces south, so her left is east: seat 6, then seat 7 — Bikram.",
    ["Ganesh 3 (S) ⇒ odd seats face south, even seats north", "Niharika 1, Shreyas 4",
     "Vaidehi 8 (N), Bikram 7", "Arundhati 5 (odd), Kartikeya 2, Damayanti 6",
     "Arundhati faces south ⇒ left = east ⇒ seat 7 = Bikram"],
    why_others_wrong="Ganesh is second to her right (west); Damayanti is immediately to her left; Vaidehi is third to "
                     "her left.", seconds=90, verified_by=BRUTE)

# ---- L4 Intermediate (standalone): a south-facing row of unknown length
V = ["n", "Mitali", "Pranay"]
conds = [("Mitali sits eighth from the east end of the row.", ("n", "Mitali"), lambda n, m: n - m + 1 == 8),
         ("Pranay sits fifth to the right of Mitali.", ("Pranay", "Mitali"), lambda p, m: p == m - 5),
         ("Exactly as many persons sit to the right of Pranay as sit between Pranay and Mitali.", ("Pranay", "Mitali"),
          lambda p, m: p - 1 == m - p - 1)]
sols = solve(V, {"n": range(2, 80), "Mitali": range(1, 80), "Pranay": range(1, 80)},
             [(vs, fn) for _, vs, fn in conds] + [(("n", "Pranay"), lambda n, p: p <= n)], [V[1:]])
assert len(sols) == 1 and sols[0] == {"n": 17, "Mitali": 10, "Pranay": 5}
mid = (17 + 1) // 2
cnt = abs(mid - sols[0]["Pranay"]) - 1
assert cnt == 3
mcq(LIN, UNK, "Intermediate",
    "Some persons sit in a straight row, all facing south. The number of persons is not given. (Facing south, a "
    "person's right is towards the west.)\n" + bullets(conds) +
    "\n\nIf Sushant sits exactly in the middle of the row, how many persons sit between Sushant and Pranay?",
    num_word(cnt), ["Two", "Four", "Five"], "Facing south: 'to the right' means towards the west end",
    "Count positions from the west end. Pranay is five places west of Mitali, so four persons sit between them; "
    "therefore four persons sit to Pranay's right (west), making Pranay 5th from the west and Mitali 10th from the "
    "west. Mitali is 8th from the east, so the row has 10 + 8 − 1 = 17 persons and the middle seat is the 9th. Between "
    "the 5th (Pranay) and 9th (Sushant) sit three persons.",
    ["Between Pranay and Mitali: 4 ⇒ 4 persons west of Pranay ⇒ Pranay 5th from west",
     "Mitali = 5 + 5 = 10th from west", "Total = 10 + 8 − 1 = 17 ⇒ middle = 9th", "Between 5th and 9th: three"],
    why_others_wrong="Two and Four come from an off-by-one count of the total or of the middle seat; Five results from "
                     "taking 'right' as east for a south-facing row.", natural=by_num, seconds=75, verified_by=BRUTE)

# ---- L5 Advanced (standalone): nine persons in a 3 x 3 block of seats, all facing north
P = ["Bhairavi", "Chetak", "Dhanush", "Hamsini", "Jahnavi", "Kshama", "Pratyush", "Ruhani", "Yatindra"]
CELLS = [(r, c) for r in (1, 2, 3) for c in (1, 2, 3)]  # r = 1 front row ... 3 back row; c = 1 west ... 3 east
conds = [("Kshama sits in the middle seat of the middle row.", ("Kshama",), lambda k: k == (2, 2)),
         ("Pratyush sits directly behind Kshama.", ("Pratyush", "Kshama"), lambda p, k: p == (k[0] + 1, k[1])),
         ("Ruhani sits immediately to the left of Pratyush.", ("Ruhani", "Pratyush"),
          lambda r, p: r == (p[0], p[1] - 1)),
         ("Chetak sits at one end of the front row, and Bhairavi sits directly behind Chetak.", ("Chetak", "Bhairavi"),
          lambda c, b: c[0] == 1 and c[1] in (1, 3) and b == (2, c[1])),
         ("Hamsini sits in the same column as Ruhani but not in the same row as Bhairavi.",
          ("Hamsini", "Ruhani", "Bhairavi"), lambda h, r, b: h[1] == r[1] and h[0] != b[0]),
         ("Dhanush sits in the front row.", ("Dhanush",), lambda d: d[0] == 1),
         ("Yatindra does not sit in the same column as Chetak.", ("Yatindra", "Chetak"), lambda y, c: y[1] != c[1])]
L5 = unique(P, {p: CELLS for p in P}, conds, [P])
at = {v: k for k, v in L5.items()}
assert [[at[(r, c)] for c in (1, 2, 3)] for r in (1, 2, 3)] == [
    ["Hamsini", "Dhanush", "Chetak"], ["Yatindra", "Kshama", "Bhairavi"], ["Ruhani", "Pratyush", "Jahnavi"]]
lj = at[(L5["Jahnavi"][0], L5["Jahnavi"][1] - 1)]
ans = at[(L5[lj][0] - 1, L5[lj][1])]
assert (lj, ans) == ("Pratyush", "Kshama")
mcq(LIN, DBL, "Advanced",
    "Nine students Bhairavi, Chetak, Dhanush, Hamsini, Jahnavi, Kshama, Pratyush, Ruhani and Yatindra sit in a hall in "
    "three rows of three seats each — a front row, a middle row and a back row — all facing north towards the stage. "
    "The seats of each row are directly behind the seats of the row in front. (Facing north, a person's right is east; "
    "'directly behind' means in the same column, one row further back.)\n" + bullets(conds) +
    "\n\nWho sits directly in front of the person who sits immediately to the left of Jahnavi?", ans,
    ["Bhairavi", "Dhanush", "Yatindra"], "Rows and columns: fix the grid one column at a time",
    "Kshama is in the centre seat; Pratyush is behind her (back row, middle) and Ruhani to his left (back row, west). "
    "Hamsini is in Ruhani's column (west) but not in Bhairavi's row. Bhairavi sits in the middle row (directly behind "
    "Chetak, who is in the front row), so Hamsini takes the front-row west seat. Chetak is then at the east end of the "
    "front row and Bhairavi behind him (middle row, east). Dhanush takes the front-row middle seat. Yatindra cannot be "
    "in Chetak's (east) column, so he sits in the middle row, west, and Jahnavi in the back row, east. Immediately to "
    "Jahnavi's left is Pratyush, and directly in front of Pratyush is Kshama.",
    ["Kshama (middle, centre); Pratyush (back, centre); Ruhani (back, west)",
     "Bhairavi is in the middle row ⇒ Hamsini (front, west)", "Chetak (front, east), Bhairavi (middle, east)",
     "Dhanush (front, centre); Yatindra (middle, west); Jahnavi (back, east)",
     "Left of Jahnavi = Pratyush ⇒ in front of him = Kshama"],
    why_others_wrong="Bhairavi sits directly in front of Jahnavi herself; Dhanush is two rows in front of Pratyush; "
                     "Yatindra is in front of Ruhani.", seconds=120, verified_by=BRUTE)

# ================================================================================================ CIRCULAR SEATING
CIR = "Circular Seating Arrangement"
CEN, INOUT, SQR = "Facing centre", "Facing inside and outside", "Square and rectangular tables"
cq = lambda sid_, sub, diff: (lambda text, correct, wrongs, concept, expl, steps, **kw: puzzle_q(
    sid_, CIR, sub, diff, text, correct, wrongs, concept, expl, steps, **kw))

# ---- C1 Basic set: six persons facing the centre with favourite games (seats 0..5 anticlockwise; right = +1)
P = ["Anupama", "Bhushan", "Gulzar", "Madhavi", "Rajat", "Tanvir"]
GM = ["Carrom", "Checkers", "Chess", "Ludo", "Pachisi", "Scrabble"]
G_ = ["g" + p for p in P]
VV = P + G_
IXV = {v: i for i, v in enumerate(VV)}
N6 = 6
likes = lambda v, x: next(v[IXV[p]] for p in P if v[IXV["g" + p]] == x)
conds = [
    ("Rajat sits second to the right of Anupama.", ("Rajat", "Anupama"), lambda r, a: r == (a + 2) % N6),
    ("Madhavi sits immediately to the left of Rajat.", ("Madhavi", "Rajat"), lambda m, r: m == (r - 1) % N6),
    ("The person who likes Chess sits opposite Anupama, and that person is Gulzar.", ("Gulzar", "gGulzar", "Anupama"),
     lambda g, c, a: g == (a + 3) % N6 and c == "Chess"),
    ("Tanvir is not an immediate neighbour of Gulzar.", ("Tanvir", "Gulzar"),
     lambda t, g: (t - g) % N6 not in (1, N6 - 1)),
    ("The person who likes Carrom sits immediately to the right of Gulzar.", tuple(VV),
     lambda *v: likes(v, "Carrom") == (v[IXV["Gulzar"]] + 1) % N6),
    ("Anupama likes Ludo and Rajat likes Scrabble.", ("gAnupama", "gRajat"),
     lambda a, r: a == "Ludo" and r == "Scrabble"),
    ("Madhavi does not like Pachisi.", ("gMadhavi",), lambda m: m != "Pachisi"),
]
C1 = unique(VV, {"Anupama": [0]} | {p: range(N6) for p in P[1:]} | {g: GM for g in G_}, conds, [P, G_])
at = {C1[p]: p for p in P}
gm = {p: C1["g" + p] for p in P}
assert [(at[i], gm[at[i]]) for i in range(N6)] == [
    ("Anupama", "Ludo"), ("Madhavi", "Checkers"), ("Rajat", "Scrabble"), ("Gulzar", "Chess"), ("Bhushan", "Carrom"),
    ("Tanvir", "Pachisi")]
ARR = "Anticlockwise from Anupama: " + ", ".join(f"{at[i]} ({gm[at[i]]})" for i in range(N6))
sid = stimulus("puzzle", "Six friends at a round table, with favourite games",
               "Six friends Anupama, Bhushan, Gulzar, Madhavi, Rajat and Tanvir sit around a circular table, equally "
               "spaced and all facing the centre. Each likes a different game among Carrom, Checkers, Chess, Ludo, "
               "Pachisi and Scrabble. (Facing the centre, a person's right is the next seat anticlockwise.)", conds,
               "Step 1: Put Anupama at seat 0 and number the seats anticlockwise. Rajat = 2, Madhavi = 1 (immediately "
               "to Rajat's left), Gulzar (Chess) = 3, opposite Anupama.\n"
               "Step 2: Seats 4 and 5 remain for Bhushan and Tanvir. Seat 4 is next to Gulzar, so Tanvir = 5 and "
               "Bhushan = 4.\n"
               "Step 3: Carrom is immediately to Gulzar's right: seat 4, Bhushan. Anupama Ludo, Rajat Scrabble; "
               "Checkers and Pachisi remain for Madhavi and Tanvir, and Madhavi does not like Pachisi, so Madhavi "
               "Checkers and Tanvir Pachisi.\n\n"
               + table(["Seat (anticlockwise)", "Person", "Game"], [(i, at[i], gm[at[i]]) for i in range(N6)]))
Q = cq(sid, CEN, "Basic")
ans = next(p for p in P if gm[p] == "Pachisi")
assert ans == "Tanvir"
Q("Who likes Pachisi?", ans, ["Madhavi", "Bhushan", "Gulzar"], "Elimination on the last two attributes",
  "After Ludo, Scrabble, Chess and Carrom are placed, Checkers and Pachisi remain for Madhavi and Tanvir; Madhavi "
  "does not like Pachisi, so Tanvir does.", [ARR, "Left: Checkers, Pachisi for Madhavi, Tanvir", "Madhavi ≠ Pachisi ⇒ "
                                                                                                 "Tanvir"],
  why_others_wrong="Madhavi likes Checkers, Bhushan Carrom and Gulzar Chess.", seconds=45)
ans = at[(C1["Madhavi"] + 3) % N6]
assert ans == "Bhushan"
Q("Who sits opposite Madhavi?", ans, ["Gulzar", "Tanvir", "Rajat"], "Opposite = three seats away in a circle of six",
  "Madhavi is at seat 1; the seat opposite is 1 + 3 = 4, Bhushan's.", [ARR, "Madhavi 1 ⇒ opposite seat 4 = Bhushan"],
  why_others_wrong="Gulzar sits opposite Anupama, Tanvir opposite Rajat, and Rajat is Madhavi's neighbour.",
  seconds=40)
cr = next(p for p in P if gm[p] == "Carrom")
ans = at[(C1[cr] - 2) % N6]
assert (cr, ans) == ("Bhushan", "Rajat")
Q("Who sits second to the left of the person who likes Carrom?", ans, ["Tanvir", "Anupama", "Gulzar"],
  "Facing the centre: the left is clockwise",
  "Bhushan likes Carrom and sits at seat 4. Facing the centre, his left is clockwise: seat 3 (Gulzar), then seat 2 "
  "(Rajat).", [ARR, "Carrom: Bhushan (seat 4)", "Left = clockwise ⇒ 4 − 2 = seat 2 = Rajat"],
  why_others_wrong="Gulzar is immediately to his left; Tanvir is immediately to his right and Anupama second to his "
                   "right.", seconds=45)
stm = [("Madhavi likes Checkers and sits immediately to the right of Anupama",
        gm["Madhavi"] == "Checkers" and C1["Madhavi"] == (C1["Anupama"] + 1) % N6),
       ("Tanvir likes Carrom and sits opposite Rajat", gm["Tanvir"] == "Carrom"),
       ("Gulzar likes Ludo and sits opposite Anupama", gm["Gulzar"] == "Ludo"),
       ("Bhushan likes Scrabble and sits next to Anupama", gm["Bhushan"] == "Scrabble")]
t, f = one_true(stm)
Q("Which of the following statements is true?", t, f, "Check both parts of each statement",
  "Madhavi (seat 1, Checkers) is the next seat anticlockwise from Anupama, i.e. immediately to her right. Tanvir "
  "likes Pachisi, Gulzar Chess and Bhushan Carrom, so the other statements fail on the game.", [ARR], seconds=50)

# ---- C2 Basic set: four men and four women sit alternately, all facing the centre (seats 0..7; right = +1)
MEN = ["Jaiwant", "Mahesh", "Prabal", "Sudhir"]
WOM = ["Kalpita", "Rupali", "Swati", "Vaishali"]
P = MEN + WOM
N8 = 8
nb = lambda a, b: (a - b) % N8 in (1, N8 - 1)
conds = [
    ("Men and women sit alternately.", tuple(P), lambda *v: all(v[i] % 2 == 0 for i in range(4))
     and all(v[i] % 2 == 1 for i in range(4, 8))),
    ("Sudhir sits opposite Jaiwant.", ("Sudhir", "Jaiwant"), lambda s, j: s == (j + 4) % N8),
    ("Swati sits immediately to the right of Sudhir.", ("Swati", "Sudhir"), lambda w, s: w == (s + 1) % N8),
    ("Rupali sits second to the left of Swati.", ("Rupali", "Swati"), lambda r, w: r == (w - 2) % N8),
    ("Prabal sits immediately to the left of Rupali.", ("Prabal", "Rupali"), lambda p, r: p == (r - 1) % N8),
    ("Vaishali is an immediate neighbour of both Mahesh and Jaiwant.", ("Vaishali", "Mahesh", "Jaiwant"),
     lambda v, m, j: nb(v, m) and nb(v, j)),
]
C2 = unique(P, {"Jaiwant": [0]} | {p: range(N8) for p in P[1:]}, conds, [P])
at = {C2[p]: p for p in P}
assert [at[i] for i in range(N8)] == ["Jaiwant", "Kalpita", "Prabal", "Rupali", "Sudhir", "Swati", "Mahesh",
                                      "Vaishali"]
ARR = "Anticlockwise from Jaiwant: " + ", ".join(at[i] for i in range(N8))
sid = stimulus("puzzle", "Four men and four women seated alternately",
               "Eight persons sit around a circular table, equally spaced and all facing the centre. Four of them — "
               "Jaiwant, Mahesh, Prabal and Sudhir — are men, and the other four — Kalpita, Rupali, Swati and Vaishali — "
               "are women. (Facing the centre, a person's right is the next seat anticlockwise.)", conds,
               "Step 1: Put Jaiwant at seat 0 and number the seats anticlockwise. Men take the even seats and women the "
               "odd seats.\n"
               "Step 2: Sudhir = 4 (opposite Jaiwant); Swati = 5 (to his right); Rupali = 3 (second to Swati's left); "
               "Prabal = 2 (immediately to Rupali's left). Mahesh takes the last man's seat, 6.\n"
               "Step 3: Vaishali neighbours both Mahesh (6) and Jaiwant (0): seat 7. Kalpita = 1.\n\n"
               + table(["Seat (anticlockwise)", "Person"], [(i, at[i]) for i in range(N8)]))
Q = cq(sid, CEN, "Basic")
ans = at[(C2["Rupali"] + 4) % N8]
assert ans == "Vaishali"
Q("Who sits opposite Rupali?", ans, ["Kalpita", "Swati", "Mahesh"], "Opposite = four seats away in a circle of eight",
  "Rupali is at seat 3; opposite her is seat 7, Vaishali.", [ARR, "Rupali 3 ⇒ opposite 7 = Vaishali"],
  why_others_wrong="Kalpita sits opposite Swati; Swati is two seats from Rupali; Mahesh is a man and men sit opposite "
                   "men.", seconds=40)
ans = at[(C2["Prabal"] - 2) % N8]
assert ans == "Jaiwant"
Q("Who sits second to the left of Prabal?", ans, ["Rupali", "Sudhir", "Kalpita"],
  "Facing the centre: the left is clockwise",
  "Prabal is at seat 2. His left is clockwise: seat 1 (Kalpita), then seat 0 (Jaiwant).",
  [ARR, "Prabal 2 ⇒ 2 − 2 = seat 0 = Jaiwant"],
  why_others_wrong="Kalpita is immediately to his left; Rupali is immediately to his right and Sudhir second to his "
                   "right.", seconds=40)
cnt = (C2["Swati"] - C2["Kalpita"]) % N8 - 1
assert cnt == 3
Q("How many persons sit between Kalpita and Swati when counted from the right of Kalpita?", num_word(cnt),
  ["Two", "Four", "Five"], "Count in the stated direction only",
  "Kalpita is at seat 1. Her right is anticlockwise: seats 2 (Prabal), 3 (Rupali), 4 (Sudhir), then Swati at 5. Three "
  "persons sit between them on that side.", [ARR, "Right of Kalpita: 2, 3, 4, then Swati at 5 ⇒ three"],
  why_others_wrong="Three persons also sit between them on the other side (Jaiwant, Vaishali, Mahesh); Two, Four and "
                   "Five miscount the seats.", natural=by_num, seconds=45)
stm = [("Mahesh sits immediately to the left of Vaishali", C2["Mahesh"] == (C2["Vaishali"] - 1) % N8),
       ("Kalpita sits opposite Sudhir", C2["Kalpita"] == (C2["Sudhir"] + 4) % N8),
       ("Prabal sits immediately to the right of Rupali", C2["Prabal"] == (C2["Rupali"] + 1) % N8),
       ("Swati and Rupali are immediate neighbours", nb(C2["Swati"], C2["Rupali"]))]
t, f = one_true(stm)
Q("Which of the following statements is true?", t, f, "Checking each statement against the arrangement",
  "Vaishali is at seat 7; immediately to her left (clockwise) is seat 6, Mahesh. Kalpita sits opposite Swati, Prabal "
  "is to Rupali's left, and Sudhir sits between Rupali and Swati.", [ARR], seconds=45)

# ---- C3 Intermediate set: rectangular table; long-side seats face the centre, the two end seats face outside.
#      Seats 0..5 anticlockwise from the west end: 0 W end, 1 south-west, 2 south-east, 3 E end, 4 north-east,
#      5 north-west. Facing the centre: right = +1; facing outside: right = −1.
P = ["Hiranya", "Jasmeet", "Keshava", "Lopamudra", "Nakul", "Revati"]
ENDS = {0, 3}
RR = lambda s, k: (s + k) % 6 if s not in ENDS else (s - k) % 6
ACROSS = {0: 3, 3: 0, 1: 5, 5: 1, 2: 4, 4: 2}
SEATNAME = {0: "west end", 1: "south side, west seat", 2: "south side, east seat", 3: "east end",
            4: "north side, east seat", 5: "north side, west seat"}
conds = [
    ("Nakul sits at the west end of the table.", ("Nakul",), lambda n: n == 0),
    ("Revati sits immediately to the right of Nakul.", ("Revati", "Nakul"), lambda r, n: r == RR(n, 1)),
    ("Keshava sits directly across the table from Revati.", ("Keshava", "Revati"), lambda k, r: k == ACROSS[r]),
    ("Jasmeet sits second to the right of Keshava.", ("Jasmeet", "Keshava"), lambda j, k: j == RR(k, 2)),
    ("Lopamudra sits immediately to the left of Jasmeet.", ("Lopamudra", "Jasmeet"), lambda l, j: l == RR(j, -1)),
]
C3 = unique(P, {p: range(6) for p in P}, conds, [P])
at = {C3[p]: p for p in P}
assert [at[i] for i in range(6)] == ["Nakul", "Keshava", "Hiranya", "Jasmeet", "Lopamudra", "Revati"]
ARR = "; ".join(f"{SEATNAME[i]}: {at[i]}" for i in range(6))
sid = stimulus("puzzle", "A rectangular table with outward-facing end seats",
               "Six persons Hiranya, Jasmeet, Keshava, Lopamudra, Nakul and Revati sit around a rectangular table. The "
               "longer sides of the table are to the north and south, and each has two seats; the shorter sides are to "
               "the west and east, and each has one seat. The four persons on the longer sides face the centre of the "
               "table, while the two persons at the shorter (end) sides face away from the table. Seats on the north "
               "side are directly across from the seats on the south side, and the west-end seat is directly across "
               "from the east-end seat. (Facing the centre, a person's right is the next seat anticlockwise; facing "
               "outside, it is the next seat clockwise.)", conds,
               "Going anticlockwise from the west end the seats are: west end, south-west, south-east, east end, "
               "north-east, north-west.\n"
               "Step 1: Nakul (west end) faces outside, so his right is clockwise: Revati = north-west.\n"
               "Step 2: Keshava is across from Revati: south-west. He faces the centre, so his right is anticlockwise: "
               "south-east, then the east end — Jasmeet.\n"
               "Step 3: Jasmeet faces outside, so her left is anticlockwise: Lopamudra = north-east. Hiranya takes the "
               "last seat, south-east.\n\n"
               + table(["Seat", "Person", "Facing"], [(SEATNAME[i], at[i], "outside" if i in ENDS else "centre")
                                                      for i in range(6)]))
Q = cq(sid, SQR, "Intermediate")
ans = at[ACROSS[C3["Hiranya"]]]
assert ans == "Lopamudra"
Q("Who sits directly across the table from Hiranya?", ans, ["Revati", "Keshava", "Jasmeet"],
  "Across the table: same position on the opposite long side",
  "Hiranya sits at the south-east seat; across from it is the north-east seat, Lopamudra's.",
  [ARR, "Hiranya: south-east ⇒ across = north-east = Lopamudra"],
  why_others_wrong="Revati is across from Keshava; Keshava sits beside Hiranya; Jasmeet sits at the east end.",
  seconds=60)
ans = at[RR(C3["Nakul"], -2)]
assert ans == "Hiranya"
Q("Who sits second to the left of Nakul?", ans, ["Lopamudra", "Revati", "Keshava"],
  "An outward-facing person's left is anticlockwise",
  "Nakul faces away from the table, so his left is the anticlockwise direction: south-west (Keshava), then south-east "
  "(Hiranya).", [ARR, "Nakul faces outside ⇒ left = anticlockwise", "West end → south-west → south-east = Hiranya"],
  why_others_wrong="Keshava is immediately to his left; Revati is immediately to his right and Lopamudra second to his "
                   "right. Lopamudra would be the answer if Nakul were taken to face the centre.", seconds=60)
stm = [("Lopamudra sits immediately to the left of Revati", C3["Lopamudra"] == RR(C3["Revati"], -1)),
       ("Jasmeet sits immediately to the right of Lopamudra", C3["Jasmeet"] == RR(C3["Lopamudra"], 1)),
       ("Revati and Keshava sit on the same longer side", C3["Revati"] in (4, 5) and C3["Keshava"] in (4, 5)),
       ("Hiranya sits at an end of the table", C3["Hiranya"] in ENDS)]
t, f = one_true(stm)
Q("Which of the following statements is true?", t, f, "Mixed facing: check each person's own right and left",
  "Revati (north-west) faces the centre, so her left is clockwise: the north-east seat, Lopamudra's — true. "
  "Lopamudra's right is anticlockwise, which is Revati, not Jasmeet; Revati is on the north side and Keshava on the "
  "south side; Hiranya is on the south side, not at an end.", [ARR], seconds=70)

# ---- C4 Advanced set: square table with three chairs on each side (12 chairs), ten persons, two vacant chairs.
#      Chairs 0..11 anticlockwise; side = chair // 3; the middle chair of a side has chair % 3 == 1. Facing the
#      centre: right = +1. Anvita is fixed at chair 1 (rotations by a whole side are symmetries).
P = ["Anvita", "Bhargav", "Chaitra", "Haridas", "Indumati", "Kumud", "Laxman", "Mandakini", "Nachiket", "Parimal"]
side = lambda s: s // 3
midc = lambda s: s % 3 == 1
R12 = lambda s, k: (s + k) % 12
vacc = lambda v: [s for s in range(12) if s not in v]
IXP = {p: i for i, p in enumerate(P)}
conds = [
    ("Anvita sits in the middle chair of a side, and Kumud sits directly opposite her (in the middle chair of the "
     "opposite side).", ("Anvita", "Kumud"), lambda a, k: midc(a) and k == R12(a, 6)),
    ("Laxman sits third to the right of Kumud.", ("Laxman", "Kumud"), lambda l, k: l == R12(k, 3)),
    ("Chaitra sits second to the right of Anvita, and Nachiket sits immediately to the right of Anvita.",
     ("Chaitra", "Nachiket", "Anvita"), lambda c, n, a: c == R12(a, 2) and n == R12(a, 1)),
    ("The two vacant chairs are on the same side of the table; it is neither Anvita's side nor Kumud's side.",
     tuple(P), lambda *v: len({side(s) for s in vacc(v)}) == 1
     and side(vacc(v)[0]) not in (side(v[IXP["Anvita"]]), side(v[IXP["Kumud"]]))),
    ("Bhargav sits immediately to the left of a vacant chair.", tuple(P),
     lambda *v: any(v[IXP["Bhargav"]] == R12(s, -1) for s in vacc(v))),
    ("Haridas sits on the same side as Kumud, but not in the middle chair, and Mandakini sits immediately to the "
     "left of Haridas.", ("Haridas", "Kumud", "Mandakini"),
     lambda h, k, m: side(h) == side(k) and not midc(h) and m == R12(h, -1)),
    ("Indumati sits in the middle chair of a side.", ("Indumati",), lambda i: midc(i)),
]
C4 = unique(P, {"Anvita": [1]} | {p: range(12) for p in P[1:]}, conds, [P])
at = {C4[p]: p for p in P}
cell = lambda s: at.get(s, "vacant")
assert [cell(i) for i in range(12)] == ["Parimal", "Anvita", "Nachiket", "Chaitra", "Indumati", "Mandakini",
                                        "Haridas", "Kumud", "Bhargav", "vacant", "Laxman", "vacant"]
ARR = "Anticlockwise, side by side: " + " | ".join(", ".join(cell(3 * s_ + j) for j in range(3)) for s_ in range(4))
sid = stimulus("puzzle", "Twelve chairs around a square table, two vacant",
               "A square table has three chairs along each side — one at each end of the side and one in the middle — "
               "so there are twelve chairs, equally spaced around the table. Going round the table, the last chair of "
               "one side is next to the first chair of the next side. Ten persons Anvita, Bhargav, Chaitra, Haridas, "
               "Indumati, Kumud, Laxman, Mandakini, Nachiket and Parimal sit on ten of the chairs, all facing the "
               "centre, and two chairs are vacant. (Facing the centre, a person's right is the next chair "
               "anticlockwise. Vacant chairs are counted as chairs.)", conds,
               "Number the chairs 0 to 11 anticlockwise so that Anvita is in chair 1, the middle of side A (chairs "
               "0–2); side B has chairs 3–5, side C 6–8 and side D 9–11.\n"
               "Step 1: Kumud = 7 (middle of side C). Laxman = 7 + 3 = 10. Nachiket = 2, Chaitra = 3.\n"
               "Step 2: The vacant chairs share a side other than A and C. On side B, chair 3 is Chaitra's, so the "
               "vacant chairs would be 4 and 5; then Bhargav would have to be in chair 3 or 4 — impossible. So the "
               "vacant chairs are on side D: 9 and 11 (Laxman has 10), and Bhargav = 8 (immediately to the left of "
               "chair 9).\n"
               "Step 3: Haridas is on side C but not in the middle; chair 8 is Bhargav's, so Haridas = 6 and Mandakini "
               "= 5. Indumati takes the middle chair 4, and Parimal the last chair, 0.\n\n"
               + table(["Side", "Chairs (anticlockwise)"],
                       [("ABCD"[s_], ", ".join(cell(3 * s_ + j) for j in range(3))) for s_ in range(4)]))
Q = cq(sid, SQR, "Advanced")
btw = [cell(R12(C4["Bhargav"], k)) for k in range(1, (C4["Parimal"] - C4["Bhargav"]) % 12)]
cnt = sum(1 for x in btw if x != "vacant")
assert btw == ["vacant", "Laxman", "vacant"] and cnt == 1
Q("How many persons sit between Bhargav and Parimal when counted from the right of Bhargav?", num_word(cnt),
  ["Two", "Three", "None"], "Count persons, not chairs",
  "From Bhargav (chair 8) going to his right (anticlockwise): chair 9 vacant, chair 10 Laxman, chair 11 vacant, then "
  "Parimal (chair 0). Only Laxman sits between them.",
  [ARR, "Chairs 9, 10, 11 between them; 9 and 11 vacant", "Persons between: Laxman ⇒ one"],
  why_others_wrong="Three counts the chairs; Two counts one vacant chair as a person; None overlooks Laxman.",
  natural=by_num, seconds=75)
mates = sorted(at[s_] for s_ in range(12) if s_ in at and side(s_) == side(C4["Indumati"]) and at[s_] != "Indumati")
assert mates == ["Chaitra", "Mandakini"]
Q("Which two persons sit on the same side of the table as Indumati?", "Chaitra and Mandakini",
  ["Nachiket and Chaitra", "Mandakini and Haridas", "Laxman and Bhargav"], "Group the chairs side by side",
  "Indumati sits in chair 4, the middle of side B (chairs 3–5). Chairs 3 and 5 hold Chaitra and Mandakini.",
  [ARR, "Side B: Chaitra, Indumati, Mandakini"],
  why_others_wrong="Nachiket is on side A; Haridas is on side C; Laxman is on side D and Bhargav on side C.",
  seconds=70)
ans = cell(R12(C4["Chaitra"], -2))
assert ans == "Anvita"
Q("Who sits second to the left of Chaitra?", ans, ["Nachiket", "Mandakini", "Indumati"],
  "Facing the centre: the left is clockwise",
  "Chaitra is in chair 3. Her left is clockwise: chair 2 (Nachiket), then chair 1 (Anvita).",
  [ARR, "Chaitra 3 ⇒ 3 − 2 = chair 1 = Anvita"],
  why_others_wrong="Nachiket is immediately to her left; Indumati and Mandakini are to her right.", seconds=60)
ans = cell(R12(C4["Indumati"], 6))
assert ans == "Laxman"
Q("Who sits directly opposite Indumati?", ans, ["Kumud", "Parimal", "Bhargav"],
  "Middle chairs of opposite sides face each other",
  "Indumati is in the middle chair of side B; directly opposite is the middle chair of side D, chair 10: Laxman.",
  [ARR, "Middle of B (4) ↔ middle of D (10) = Laxman"],
  why_others_wrong="Kumud sits opposite Anvita; Parimal and Bhargav sit at ends of sides, not in middle chairs.",
  seconds=60)
stm = [("A vacant chair is immediately to the left of Parimal", cell(R12(C4["Parimal"], -1)) == "vacant"),
       ("Haridas sits immediately to the right of Bhargav", C4["Haridas"] == R12(C4["Bhargav"], 1)),
       ("Nachiket and Chaitra sit on the same side of the table", side(C4["Nachiket"]) == side(C4["Chaitra"])),
       ("Mandakini sits in the middle chair of a side", midc(C4["Mandakini"]))]
t, f = one_true(stm)
Q("Which of the following statements is true?", t, f, "Corner neighbours are on different sides",
  "Parimal is in chair 0; his left (clockwise) is chair 11, which is vacant — true. Immediately to Bhargav's right is "
  "the vacant chair 9; Nachiket (chair 2) and Chaitra (chair 3) are neighbours across a corner, on sides A and B; "
  "Mandakini is in chair 5, an end chair.", [ARR], seconds=75)

# ================================================================================================ FLOOR PUZZLES
FLR = "Floor-Based Puzzles"
FF, FA = "Floor and flat", "Floor with attribute"
fq = lambda sid_, sub, diff: (lambda text, correct, wrongs, concept, expl, steps, **kw: puzzle_q(
    sid_, FLR, sub, diff, text, correct, wrongs, concept, expl, steps, **kw))

# ---- F1 Basic set: six floors with curtain colours (floor 1 = lowermost)
P = ["Bhanu", "Chandana", "Girish", "Purab", "Ujjwal", "Vasanti"]
CO = ["Beige", "Maroon", "Mauve", "Teal", "Turquoise", "Violet"]
C_ = ["c" + p for p in P]
VV = P + C_
IXV = {v: i for i, v in enumerate(VV)}
flr = lambda v, x: next(v[IXV[p]] for p in P if v[IXV["c" + p]] == x)
conds = [
    ("Purab lives on floor 4, and Chandana lives immediately below Purab.", ("Purab", "Chandana"),
     lambda p, c: p == 4 and c == p - 1),
    ("Vasanti lives on the topmost floor.", ("Vasanti",), lambda v: v == 6),
    ("Only one person lives between Bhanu and Chandana.", ("Bhanu", "Chandana"), lambda b, c: abs(b - c) == 2),
    ("Girish lives on an odd-numbered floor.", ("Girish",), lambda g: g % 2 == 1),
    ("Ujjwal lives on a floor below Bhanu's floor.", ("Ujjwal", "Bhanu"), lambda u, b: u < b),
    ("Bhanu has Teal curtains, and the person with Maroon curtains lives immediately above him.", tuple(VV),
     lambda *v: v[IXV["cBhanu"]] == "Teal" and flr(v, "Maroon") == v[IXV["Bhanu"]] + 1),
    ("Girish has Beige curtains, and the person with Mauve curtains lives immediately above Girish.", tuple(VV),
     lambda *v: v[IXV["cGirish"]] == "Beige" and flr(v, "Mauve") == v[IXV["Girish"]] + 1),
    ("Chandana has neither Violet nor Mauve curtains.", ("cChandana",), lambda c: c not in ("Violet", "Mauve")),
]
F1 = unique(VV, {p: range(1, 7) for p in P} | {c: CO for c in C_}, conds, [P, C_])
at = {F1[p]: p for p in P}
cu = {p: F1["c" + p] for p in P}
assert [(at[i], cu[at[i]]) for i in range(1, 7)] == [
    ("Girish", "Beige"), ("Ujjwal", "Mauve"), ("Chandana", "Turquoise"), ("Purab", "Violet"), ("Bhanu", "Teal"),
    ("Vasanti", "Maroon")]
ARR = "Bottom to top: " + ", ".join(f"floor {i} {at[i]} ({cu[at[i]]})" for i in range(1, 7))
sid = stimulus("puzzle", "Six floors and six curtain colours",
               "Six persons Bhanu, Chandana, Girish, Purab, Ujjwal and Vasanti live on the six floors of a building, "
               "one on each floor. Floor 1 is the lowermost and floor 6 the topmost. Each has curtains of a different "
               "colour among Beige, Maroon, Mauve, Teal, Turquoise and Violet.", conds,
               "Step 1: Purab = 4, Chandana = 3, Vasanti = 6. Bhanu is two floors from Chandana: floor 1 or 5.\n"
               "Step 2: Ujjwal lives below Bhanu, so Bhanu cannot be on floor 1: Bhanu = 5. Floors 1 and 2 remain for "
               "Girish and Ujjwal; Girish is on an odd floor, so Girish = 1 and Ujjwal = 2.\n"
               "Step 3: Bhanu Teal ⇒ Maroon on floor 6 (Vasanti). Girish Beige ⇒ Mauve on floor 2 (Ujjwal). Turquoise "
               "and Violet remain for Chandana and Purab; Chandana is not Violet, so Chandana Turquoise and Purab "
               "Violet.\n\n" + table(["Floor", "Person", "Curtains"], [(i, at[i], cu[at[i]]) for i in range(6, 0, -1)]))
Q = fq(sid, FA, "Basic")
ans = next(p for p in P if cu[p] == "Violet")
assert ans == "Purab"
Q("Who has Violet curtains?", ans, ["Chandana", "Ujjwal", "Vasanti"], "Fix the floors first, then the colours",
  "Teal (Bhanu), Maroon (Vasanti), Beige (Girish) and Mauve (Ujjwal) are fixed by the clues. Turquoise and Violet "
  "remain for Chandana and Purab; Chandana is not Violet, so Purab has Violet curtains.",
  [ARR, "Left: Turquoise, Violet for Chandana, Purab", "Chandana ≠ Violet ⇒ Purab"],
  why_others_wrong="Chandana has Turquoise, Ujjwal Mauve and Vasanti Maroon curtains.", seconds=45)
cnt = abs(F1["Ujjwal"] - F1["Vasanti"]) - 1
assert cnt == 3
Q("How many persons live between Ujjwal and Vasanti?", num_word(cnt), ["Two", "Four", "One"],
  "Count the floors strictly between two persons",
  "Ujjwal lives on floor 2 and Vasanti on floor 6. Floors 3, 4 and 5 (Chandana, Purab, Bhanu) lie between them.",
  [ARR, "Between floors 2 and 6: 3, 4, 5 ⇒ three"], natural=by_num, seconds=40)
stm = [("Floor 3 – Chandana – Turquoise", at[3] == "Chandana" and cu["Chandana"] == "Turquoise"),
       ("Floor 2 – Girish – Beige", at[2] == "Girish"),
       ("Floor 5 – Bhanu – Maroon", cu["Bhanu"] == "Maroon"),
       ("Floor 1 – Ujjwal – Mauve", at[1] == "Ujjwal")]
t, f = one_true(stm)
Q("Which of the following floor – person – curtain combinations is correct?", t, f,
  "Check all three parts of each combination", "From the table: " + ARR + ".", [ARR],
  why_others_wrong="Girish is on floor 1 (not 2), Bhanu has Teal curtains, and Ujjwal is on floor 2.", seconds=45)

# ---- F2 Intermediate set: seven floors and the number of potted plants each person keeps
P = ["Abhijit", "Deepali", "Faiyaz", "Kamakshi", "Leeladhar", "Ojaswini", "Rishi"]
PL = [4, 6, 7, 9, 12, 15, 18]
N_ = ["n" + p for p in P]
VV = P + N_
IXV = {v: i for i, v in enumerate(VV)}
flr = lambda v, x: next(v[IXV[p]] for p in P if v[IXV["n" + p]] == x)
num_on = lambda v, f: next(v[IXV["n" + p]] for p in P if v[IXV[p]] == f)
conds = [
    ("The person who keeps 18 plants lives on floor 5, and Kamakshi lives two floors below that person.", tuple(VV),
     lambda *v: flr(v, 18) == 5 and v[IXV["Kamakshi"]] == 3),
    ("Kamakshi keeps exactly half as many plants as the person who lives immediately above her.", tuple(VV),
     lambda *v: 2 * v[IXV["nKamakshi"]] == num_on(v, v[IXV["Kamakshi"]] + 1)),
    ("The person who keeps 15 plants lives immediately below Kamakshi.", tuple(VV),
     lambda *v: flr(v, 15) == v[IXV["Kamakshi"]] - 1),
    ("Rishi lives on the topmost floor and keeps fewer plants than Kamakshi.", ("Rishi", "nRishi", "nKamakshi"),
     lambda r, nr, nk: r == 7 and nr < nk),
    ("Only two persons live between Rishi and Faiyaz.", ("Rishi", "Faiyaz"), lambda r, f: abs(r - f) == 3),
    ("Abhijit lives on a floor above Faiyaz's floor and keeps the second-smallest number of plants.",
     ("Abhijit", "Faiyaz", "nAbhijit"), lambda a, f, n: a > f and n == 7),
    ("Deepali keeps an odd number of plants, and Leeladhar keeps fewer plants than Deepali.",
     ("nDeepali", "nLeeladhar"), lambda d, l: d % 2 == 1 and l < d),
]
F2 = unique(VV, {p: range(1, 8) for p in P} | {n: PL for n in N_}, conds, [P, N_])
at = {F2[p]: p for p in P}
pl = {p: F2["n" + p] for p in P}
assert [(at[i], pl[at[i]]) for i in range(1, 8)] == [
    ("Leeladhar", 9), ("Deepali", 15), ("Kamakshi", 6), ("Faiyaz", 12), ("Ojaswini", 18), ("Abhijit", 7),
    ("Rishi", 4)]
ARR = "Bottom to top: " + ", ".join(f"floor {i} {at[i]} ({pl[at[i]]})" for i in range(1, 8))
sid = stimulus("puzzle", "Seven floors and their potted plants",
               "Seven persons Abhijit, Deepali, Faiyaz, Kamakshi, Leeladhar, Ojaswini and Rishi live on the seven "
               "floors of a building, one on each floor (floor 1 is the lowermost, floor 7 the topmost). Each keeps a "
               "different number of potted plants among 4, 6, 7, 9, 12, 15 and 18.", conds,
               "Step 1: 18 plants on floor 5; Kamakshi = 3; 15 plants on floor 2.\n"
               "Step 2: Kamakshi's count doubled must be on floor 4. Possible pairs from the list: 6 and 12, or 9 and "
               "18 — but 18 is on floor 5, so Kamakshi keeps 6 and floor 4 has 12.\n"
               "Step 3: Rishi = 7 with fewer than 6 plants: 4. Faiyaz is three floors below Rishi: floor 4 (12 "
               "plants).\n"
               "Step 4: Abhijit is above Faiyaz with 7 plants; floor 5 has 18, so Abhijit = 6. Floor 1 then has 9 "
               "plants.\n"
               "Step 5: Deepali, Leeladhar and Ojaswini take floors 1 (9), 2 (15) and 5 (18). Deepali's count is odd "
               "(9 or 15) and Leeladhar has fewer than Deepali: if Deepali had 9, nobody left would have fewer, so "
               "Deepali = floor 2 (15), Leeladhar = floor 1 (9) and Ojaswini = floor 5 (18).\n\n"
               + table(["Floor", "Person", "Plants"], [(i, at[i], pl[at[i]]) for i in range(7, 0, -1)]))
Q = fq(sid, FA, "Intermediate")
Q("How many plants does Ojaswini keep?", str(pl["Ojaswini"]), ["15", "12", "9"],
  "Resolve the last three persons by the 'fewer than' clue",
  "Floors 1, 2 and 5 hold 9, 15 and 18 plants. Deepali must have an odd count and someone (Leeladhar) must have fewer, "
  "so Deepali has 15 and Leeladhar 9; Ojaswini, on floor 5, keeps 18.",
  [ARR, "Deepali 15, Leeladhar 9 ⇒ Ojaswini 18"], natural=int, seconds=75)
ans = at[F2[next(p for p in P if pl[p] == 9)] + 1]
assert ans == "Deepali"
Q("Who lives immediately above the person who keeps 9 plants?", ans, ["Kamakshi", "Leeladhar", "Faiyaz"],
  "Chain the clues from the fixed floors",
  "Leeladhar keeps 9 plants and lives on floor 1; Deepali lives on floor 2.",
  [ARR, "9 plants: Leeladhar (floor 1) ⇒ floor 2 = Deepali"],
  why_others_wrong="Kamakshi is two floors above Leeladhar; Leeladhar is the 9-plant person himself; Faiyaz lives on "
                   "floor 4.", seconds=70)
tot = sum(pl[at[i]] for i in (6, 7))
assert tot == 11
Q("What is the total number of plants kept by the persons on the two topmost floors?", str(tot), ["13", "22", "16"],
  "Read the counts off the two top floors",
  "Floor 7 (Rishi) has 4 plants and floor 6 (Abhijit) 7 plants: 4 + 7 = 11.", [ARR, "4 + 7 = 11"],
  why_others_wrong="13 adds Rishi's 4 to 9; 22 adds Abhijit's 7 to 15; 16 adds 4 to 12.", natural=int, seconds=65)
cnt = abs(F2["Deepali"] - F2["Abhijit"]) - 1
assert cnt == 3
Q("How many persons live between Deepali and Abhijit?", num_word(cnt), ["Two", "Four", "One"],
  "Count the floors strictly between two persons",
  "Deepali is on floor 2 and Abhijit on floor 6; Kamakshi, Faiyaz and Ojaswini live between them.",
  [ARR, "Between floors 2 and 6 ⇒ three persons"], natural=by_num, seconds=60)

# ---- F3 Intermediate set: seven floors and three professions with repeats
P = ["Gobind", "Harleen", "Jayanti", "Madhur", "Nirupama", "Oorja", "Shailesh"]
J_ = ["j" + p for p in P]
VV = P + J_
IXV = {v: i for i, v in enumerate(VV)}
job_on = lambda v, f: next(v[IXV["j" + p]] for p in P if v[IXV[p]] == f)
conds = [
    ("Three of them are Doctors, two are Lawyers and two are Teachers.", tuple(J_),
     lambda *j: j.count("Doctor") == 3 and j.count("Lawyer") == 2 and j.count("Teacher") == 2),
    ("No two persons of the same profession live on adjacent floors.", tuple(VV),
     lambda *v: all(job_on(v, f) != job_on(v, f + 1) for f in range(1, 7))),
    ("Madhur is a Teacher and lives on floor 4.", ("Madhur", "jMadhur"), lambda m, j: m == 4 and j == "Teacher"),
    ("Oorja is a Doctor and lives on the topmost floor.", ("Oorja", "jOorja"), lambda o, j: o == 7 and j == "Doctor"),
    ("Harleen lives immediately below Madhur and is not a Doctor.", ("Harleen", "Madhur", "jHarleen"),
     lambda h, m, j: h == m - 1 and j != "Doctor"),
    ("Gobind lives on floor 1 and has the same profession as Oorja.", ("Gobind", "jGobind", "jOorja"),
     lambda g, j, o: g == 1 and j == o),
    ("Jayanti is a Lawyer.", ("jJayanti",), lambda j: j == "Lawyer"),
    ("Shailesh lives on a floor below Nirupama's floor.", ("Shailesh", "Nirupama"), lambda s, n: s < n),
]
F3 = unique(VV, {p: range(1, 8) for p in P} | {j: ["Doctor", "Lawyer", "Teacher"] for j in J_}, conds, [P])
at = {F3[p]: p for p in P}
jb = {p: F3["j" + p] for p in P}
assert [(at[i], jb[at[i]]) for i in range(1, 8)] == [
    ("Gobind", "Doctor"), ("Shailesh", "Teacher"), ("Harleen", "Lawyer"), ("Madhur", "Teacher"),
    ("Nirupama", "Doctor"), ("Jayanti", "Lawyer"), ("Oorja", "Doctor")]
ARR = "Bottom to top: " + ", ".join(f"floor {i} {at[i]} ({jb[at[i]]})" for i in range(1, 8))
sid = stimulus("puzzle", "Seven floors, three professions, no two alike adjacent",
               "Seven persons Gobind, Harleen, Jayanti, Madhur, Nirupama, Oorja and Shailesh live on the seven floors "
               "of a building, one on each floor (floor 1 is the lowermost, floor 7 the topmost). Each of them is a "
               "Doctor, a Lawyer or a Teacher.", conds,
               "Step 1: Madhur (Teacher) = 4, Oorja (Doctor) = 7, Gobind (Doctor) = 1, Harleen = 3. Harleen is not a "
               "Doctor, and as Madhur's neighbour cannot be a Teacher: Harleen is a Lawyer.\n"
               "Step 2: Floor 2 lies between a Doctor (1) and a Lawyer (3), so it is a Teacher. The professions left "
               "are one Doctor and one Lawyer for floors 5 and 6; floor 6 is next to Oorja (Doctor), so floor 6 is the "
               "Lawyer and floor 5 the Doctor.\n"
               "Step 3: Jayanti is a Lawyer, so she is on floor 6. Shailesh is below Nirupama, so Shailesh = 2 "
               "(Teacher) and Nirupama = 5 (Doctor).\n\n"
               + table(["Floor", "Person", "Profession"], [(i, at[i], jb[at[i]]) for i in range(7, 0, -1)]))
Q = fq(sid, FA, "Intermediate")
ans = next(p for p in P if jb[p] == "Teacher" and p != "Madhur")
assert ans == "Shailesh"
Q("Apart from Madhur, who is a Teacher?", ans, ["Harleen", "Nirupama", "Jayanti"],
  "A floor squeezed between two different professions takes the third",
  "Floor 2 lies between Gobind (Doctor, floor 1) and Harleen (Lawyer, floor 3), so its resident must be a Teacher. "
  "Shailesh lives below Nirupama, and the only floors left are 2 and 5, so Shailesh is on floor 2.",
  [ARR, "Floor 2 between Doctor and Lawyer ⇒ Teacher", "Shailesh below Nirupama ⇒ Shailesh = 2"],
  why_others_wrong="Harleen and Jayanti are Lawyers; Nirupama is a Doctor.", seconds=75)
cnt = sum(1 for p in P if jb[p] == "Doctor" and F3[p] > F3["Harleen"])
assert cnt == 2
Q("How many Doctors live above Harleen?", num_word(cnt), ["One", "Three", "None"],
  "Read professions above a fixed floor",
  "Above Harleen (floor 3) live Madhur (Teacher), Nirupama (Doctor), Jayanti (Lawyer) and Oorja (Doctor): two "
  "Doctors.", [ARR, "Floors 4–7: Teacher, Doctor, Lawyer, Doctor ⇒ two"],
  why_others_wrong="Three counts Gobind too, but he lives below Harleen.", natural=by_num, seconds=65)
stm = [("Jayanti lives immediately below Oorja", F3["Jayanti"] == F3["Oorja"] - 1),
       ("Nirupama and Gobind have different professions", jb["Nirupama"] != jb["Gobind"]),
       ("Shailesh lives immediately above Harleen", F3["Shailesh"] == F3["Harleen"] + 1),
       ("Both Lawyers live below Madhur", sum(1 for p in P if jb[p] == "Lawyer" and F3[p] < 4) == 2)]
t, f = one_true(stm)
Q("Which of the following statements is true?", t, f, "Checking each statement against the arrangement",
  "Jayanti (floor 6) lives immediately below Oorja (floor 7) — true. Nirupama and Gobind are both Doctors; Shailesh "
  "lives below Harleen, not above; and only one Lawyer (Harleen) lives below Madhur — Jayanti lives above him.",
  [ARR], seconds=65)

# ---- F4 Advanced set: four floors with three flats each (West, Middle, East), nine persons, three vacant flats
P = ["Ajeet", "Bansi", "Champa", "Dilip", "Fulmani", "Gokul", "Hemangini", "Indraneel", "Jagjit"]
FL = [(f, c) for f in range(1, 5) for c in range(3)]  # c: 0 West, 1 Middle, 2 East
CN = ["West", "Middle", "East"]
IXP = {p: i for i, p in enumerate(P)}
vf = lambda v: [x for x in FL if x not in v]
conds = [
    ("Exactly three flats are vacant, and no two vacant flats are on the same floor.", tuple(P),
     lambda *v: len({x[0] for x in vf(v)}) == 3),
    ("Gokul lives in the Middle flat of floor 3, and the flat directly below his flat is vacant.", tuple(P),
     lambda *v: v[IXP["Gokul"]] == (3, 1) and (2, 1) not in v),
    ("Ajeet lives directly above Gokul, and the East flat of Ajeet's floor is vacant.", tuple(P),
     lambda *v: v[IXP["Ajeet"]] == (4, 1) and (4, 2) not in v),
    ("Bansi lives in a West flat on an even-numbered floor, and Dilip lives on the same floor as Bansi.",
     ("Bansi", "Dilip"), lambda b, d: b[1] == 0 and b[0] % 2 == 0 and d[0] == b[0]),
    ("Hemangini lives directly below Bansi, and Fulmani lives directly above Bansi.", ("Hemangini", "Fulmani", "Bansi"),
     lambda h, f, b: h == (b[0] - 1, b[1]) and f == (b[0] + 1, b[1])),
    ("Champa lives directly above Dilip.", ("Champa", "Dilip"), lambda c, d: c == (d[0] + 1, d[1])),
    ("Jagjit lives on the same floor as Hemangini, in the East flat.", ("Jagjit", "Hemangini"),
     lambda j, h: j == (h[0], 2)),
]
F4 = unique(P, {p: FL for p in P}, conds, [P])
at = {v: k for k, v in F4.items()}
cell = lambda x: at.get(x, "vacant")
assert [[cell((f, c)) for c in range(3)] for f in range(4, 0, -1)] == [
    ["Indraneel", "Ajeet", "vacant"], ["Fulmani", "Gokul", "Champa"], ["Bansi", "vacant", "Dilip"],
    ["Hemangini", "vacant", "Jagjit"]]
ARR = "Top to bottom (West, Middle, East): " + " | ".join(
    f"floor {f}: " + ", ".join(cell((f, c)) for c in range(3)) for f in range(4, 0, -1))
sid = stimulus("puzzle", "Four floors with three flats each, three vacant",
               "A four-storey building (floor 1 is the lowermost, floor 4 the topmost) has three flats on each floor: "
               "West, Middle and East. Each flat is directly above the flat of the same name on the floor below. Nine "
               "persons Ajeet, Bansi, Champa, Dilip, Fulmani, Gokul, Hemangini, Indraneel and Jagjit live in nine of "
               "the twelve flats, one person per flat, and the other three flats are vacant.", conds,
               "Step 1: Gokul = 3-Middle, 2-Middle vacant; Ajeet = 4-Middle, 4-East vacant. Floors 2 and 4 now have "
               "their vacant flat, so the third vacant flat is on floor 1 or 3.\n"
               "Step 2: Bansi is in a West flat on floor 2 or 4. If Bansi were in 4-West, Fulmani would have to be "
               "above floor 4 — impossible. So Bansi = 2-West, Hemangini = 1-West, Fulmani = 3-West. Dilip is on "
               "floor 2: 2-East (2-Middle is vacant). Champa = 3-East, above Dilip.\n"
               "Step 3: Jagjit = 1-East. Floor 3 is now full, so the third vacant flat is on floor 1: 1-Middle. "
               "Indraneel takes the last flat, 4-West.\n\n"
               + table(["Floor", "West", "Middle", "East"],
                       [(f,) + tuple(cell((f, c)) for c in range(3)) for f in range(4, 0, -1)]))
Q = fq(sid, FF, "Advanced")
full = [f for f in range(1, 5) if all((f, c) in at for c in range(3))]
assert full == [3]
Q("Which floor has no vacant flat?", "Floor 3", ["Floor 1", "Floor 2", "Floor 4"],
  "Track the one-vacancy-per-floor rule",
  "Floors 2 and 4 get their vacant flats from the clues about Gokul and Ajeet. Fulmani, Gokul and Champa then fill "
  "floor 3, so the remaining vacant flat must be on floor 1 (its Middle flat).",
  [ARR, "Vacant: 4-East, 2-Middle, 1-Middle", "Floor 3 full: Fulmani, Gokul, Champa"],
  why_others_wrong="Floor 1 has its Middle flat vacant, floor 2 its Middle flat and floor 4 its East flat.",
  seconds=120)
ans = cell((F4["Indraneel"][0] - 1, F4["Indraneel"][1]))
assert ans == "Fulmani"
Q("Who lives directly below Indraneel?", ans, ["Gokul", "Bansi", "Champa"], "Same flat name, one floor down",
  "Indraneel lives in 4-West; directly below is 3-West, Fulmani's flat.", [ARR, "4-West ⇒ 3-West = Fulmani"],
  why_others_wrong="Gokul is below Ajeet; Bansi is two floors below Indraneel; Champa is in an East flat.",
  seconds=100)
stm = [("Jagjit lives directly below Dilip", F4["Jagjit"] == (F4["Dilip"][0] - 1, F4["Dilip"][1])),
       ("Hemangini lives in a Middle flat", F4["Hemangini"][1] == 1),
       ("Champa and Ajeet live on the same floor", F4["Champa"][0] == F4["Ajeet"][0]),
       ("The flat directly above Fulmani's flat is vacant", (F4["Fulmani"][0] + 1, 0) not in at)]
t, f = one_true(stm)
Q("Which of the following statements is true?", t, f, "Checking each statement against the arrangement",
  "Dilip is in 2-East and Jagjit in 1-East, directly below him — true. Hemangini lives in a West flat; Champa is on "
  "floor 3 and Ajeet on floor 4; the flat above Fulmani (4-West) is Indraneel's.", [ARR], seconds=100)

# ---- F5 Advanced set: ten floors, seven persons, three vacant floors
P = ["Ketki", "Murari", "Navneet", "Padmini", "Rehaan", "Sevanti", "Trilok"]
vfl = lambda v: [f for f in range(1, 11) if f not in v]
IXP = {p: i for i, p in enumerate(P)}
conds = [
    ("The lowermost and topmost floors are both occupied.", tuple(P), lambda *v: 1 in v and 10 in v),
    ("Trilok lives on floor 7, and Murari lives immediately below Trilok.", ("Trilok", "Murari"),
     lambda t, m: t == 7 and m == 6),
    ("Ketki lives below Trilok; of the floors between Ketki and Trilok, exactly two are vacant and exactly one is "
     "occupied.", tuple(P), lambda *v: v[0] < v[6] and v[6] - v[0] - 1 == 3
     and sum(1 for f in range(v[0] + 1, v[6]) if f not in v) == 2),
    ("Sevanti lives on an odd-numbered floor below Ketki's floor.", ("Sevanti", "Ketki"),
     lambda s, k: s % 2 == 1 and s < k),
    ("Padmini lives immediately above Trilok.", ("Padmini", "Trilok"), lambda p, t: p == t + 1),
    ("Only one person lives above Navneet.", tuple(P), lambda *v: sum(1 for x in v if x > v[IXP["Navneet"]]) == 1),
]
F5 = unique(P, {p: range(1, 11) for p in P}, conds, [P])
at = {v: k for k, v in F5.items()}
assert [at.get(f, "vacant") for f in range(1, 11)] == [
    "Sevanti", "vacant", "Ketki", "vacant", "vacant", "Murari", "Trilok", "Padmini", "Navneet", "Rehaan"]
ARR = "Bottom to top: " + ", ".join(f"{f} {at.get(f, 'vacant')}" for f in range(1, 11))
sid = stimulus("puzzle", "Ten floors, seven residents, three vacant floors",
               "A building has ten floors, numbered 1 (lowermost) to 10 (topmost). Seven persons Ketki, Murari, "
               "Navneet, Padmini, Rehaan, Sevanti and Trilok live in it, one person per floor, so exactly three floors "
               "are vacant.", conds,
               "Step 1: Trilok = 7, Murari = 6, Padmini = 8.\n"
               "Step 2: Between Ketki and Trilok there are exactly three floors (two vacant, one occupied), so Ketki = "
               "3. Murari (6) is the occupied one, so floors 4 and 5 are vacant.\n"
               "Step 3: Sevanti is on an odd floor below 3: floor 1. That leaves one more vacant floor among 2, 9 and "
               "10, with Navneet and Rehaan to place; floor 10 is occupied.\n"
               "Step 4: Only one person lives above Navneet. If Navneet were on floor 2, many would be above him; so "
               "Navneet = 9, Rehaan = 10, and floor 2 is vacant.\n\n"
               + table(["Floor", "Resident"], [(f, at.get(f, "vacant")) for f in range(10, 0, -1)]))
Q = fq(sid, FF, "Advanced")
cnt = sum(1 for f in range(F5["Sevanti"] + 1, F5["Murari"]) if f not in at)
assert cnt == 3
Q("How many vacant floors are there between Sevanti and Murari?", num_word(cnt), ["Two", "One", "Four"],
  "Settle the last vacant floor before counting",
  "Sevanti is on floor 1 and Murari on floor 6. Floors 2, 4 and 5 are vacant and floor 3 is Ketki's, so three vacant "
  "floors lie between them.", [ARR, "Between 1 and 6: 2 (vacant), 3 (Ketki), 4, 5 (vacant) ⇒ three"],
  why_others_wrong="Two misses the vacant floor 2, which is fixed only after placing Navneet; One and Four miscount.",
  natural=by_num, seconds=120)
cnt2 = sum(1 for p in P if F5[p] > F5["Murari"])
assert cnt2 == 4
Q("How many persons live above Murari?", num_word(cnt2), ["Three", "Five", "Two"], "Count occupied floors only",
  "Above Murari (floor 6) live Trilok (7), Padmini (8), Navneet (9) and Rehaan (10): four persons.",
  [ARR, "Floors 7–10 all occupied ⇒ four"], why_others_wrong="Three leaves out Rehaan on the topmost floor; Five and "
                                                              "Two miscount.", natural=by_num, seconds=100)
stm = [("Navneet lives immediately above Padmini", F5["Navneet"] == F5["Padmini"] + 1),
       ("Ketki lives immediately above Sevanti", F5["Ketki"] == F5["Sevanti"] + 1),
       ("Floor 5 is occupied", 5 in at),
       ("Rehaan lives on floor 9", F5["Rehaan"] == 9)]
t, f = one_true(stm)
Q("Which of the following statements is true?", t, f, "Checking each statement against the arrangement",
  "Navneet (floor 9) lives immediately above Padmini (floor 8) — true. Floor 2, between Sevanti (1) and Ketki "
  "(3), is vacant; floor 5 is vacant; and Rehaan lives on floor 10.", [ARR], seconds=100)

# ================================================================================================ BOX PUZZLES
BOX = "Box-Based Puzzles"
STK, BWC = "Stacked boxes", "Boxes with weights or colours"

# ---- X1 Basic (standalone): six boxes, positions read from the top
B = ["E", "H", "M", "P", "S", "X"]
conds = [("Box M is kept fourth from the top.", ("M",), lambda m: 7 - m == 4),
         ("Box S is kept immediately above box M.", ("S", "M"), lambda s, m: s == m + 1),
         ("Only two boxes are kept between box S and box X.", ("S", "X"), lambda s, x: abs(s - x) == 3),
         ("Box E is kept at the top.", ("E",), lambda e: e == 6),
         ("Box H is kept somewhere below box P.", ("H", "P"), lambda h, p: h < p)]
X1 = unique(B, {b: range(1, 7) for b in B}, conds, [B])
at = {v: k for k, v in X1.items()}
assert [at[i] for i in range(1, 7)] == ["X", "H", "M", "S", "P", "E"]
ans = at[X1["P"] - 1]
assert ans == "S"
mcq(BOX, STK, "Basic",
    "Six boxes E, H, M, P, S and X are kept one above another in a single stack.\n" + bullets(conds) +
    "\n\nWhich box is kept immediately below box P?", "Box " + ans, ["Box M", "Box E", "Box H"],
    "Convert 'from the top' into a position from the bottom",
    "With six boxes, fourth from the top is third from the bottom: M = 3, so S = 4. Two boxes between S and X puts X "
    "at position 1 (position 7 does not exist). E = 6. Positions 2 and 5 remain; H is below P, so H = 2 and P = 5. "
    "Immediately below P (5) is S (4).",
    ["M: 4th from top = 3rd from bottom", "S = 4, X = 1, E = 6", "H below P ⇒ H = 2, P = 5", "Below P ⇒ S"],
    why_others_wrong="M is two places below P; E is immediately above P; H is at position 2.", seconds=45,
    verified_by=BRUTE)

# ---- X2 Intermediate (standalone): six boxes with weights linked by arithmetic
B = ["F", "J", "N", "R", "V", "Z"]
WT = [8, 12, 16, 20, 24, 30]
W_ = ["w" + b for b in B]
VV = B + W_
IXV = {v: i for i, v in enumerate(VV)}
won = lambda v, p_: next(v[IXV["w" + b]] for b in B if v[IXV[b]] == p_)
conds = [("Box R is the heaviest box and is kept immediately above box F.", ("R", "wR", "F"),
          lambda r, w, f: w == 30 and r == f + 1),
         ("Box F weighs exactly half as much as the box kept at the bottom.", tuple(VV),
          lambda *v: 2 * v[IXV["wF"]] == won(v, 1)),
         ("Box J is the lightest box and is kept immediately above box R.", ("J", "wJ", "R"),
          lambda j, w, r: w == 8 and j == r + 1),
         ("Only one box is kept between box J and box N.", ("J", "N"), lambda j, n: abs(j - n) == 2),
         ("Box V weighs 20 kg and is not at the top.", ("V", "wV"), lambda v_, w: w == 20 and v_ != 6),
         ("The box at the top weighs 4 kg less than box V.", tuple(VV), lambda *v: won(v, 6) == v[IXV["wV"]] - 4)]
X2 = unique(VV, {b: range(1, 7) for b in B} | {w: WT for w in W_}, conds, [B, W_])
at = {X2[b]: b for b in B}
assert [(at[i], X2["w" + at[i]]) for i in range(1, 7)] == [("Z", 24), ("F", 12), ("R", 30), ("J", 8), ("V", 20),
                                                           ("N", 16)]
tot = sum(X2["w" + at[i]] for i in range(X2["J"] + 1, 7))
assert tot == 36
mcq(BOX, BWC, "Intermediate",
    "Six boxes F, J, N, R, V and Z are kept one above another in a single stack (position 1 is the bottom, 6 the top). "
    "Their weights are 8, 12, 16, 20, 24 and 30 kg, one weight per box.\n" + bullets(conds) +
    "\n\nWhat is the total weight of the boxes kept above box J?", f"{tot} kg", ["44 kg", "50 kg", "28 kg"],
    "Stack positions and weights together",
    "The top box weighs 20 − 4 = 16 kg. F weighs half as much as the bottom box; J is the 8-kg box, so F = 12 kg and "
    "the bottom box weighs 24 kg (F itself is not at the bottom). F, R (30 kg) and J (8 kg) are consecutive from the "
    "bottom up. J cannot be at 6 (the top box weighs 16 kg), and if F were at 3, J would be at 5 and N, two places from "
    "J, would need position 3 or 7 — impossible. So F = 2, R = 3, J = 4, and N = 6 (16 kg). V (20 kg) = 5, and Z is "
    "the 24-kg box at the bottom. Above J: V (20) + N (16) = 36 kg.",
    ["Top box = 16 kg; V = 20 kg below the top", "F = 12 with 24 kg at the bottom ⇒ F 2, R 3, J 4, Z 1 (24)",
     "N = 6 (16 kg), V = 5", "Above J: 20 + 16 = 36 kg"],
    why_others_wrong="44 kg adds R instead of N; 50 kg adds R and V; 28 kg adds J's own weight to V.",
    natural=lambda t: int(t.split()[0]), seconds=100, verified_by=BRUTE)

# ---- X3 Advanced (standalone): eight boxes, four wooden and four plastic, no two wooden boxes adjacent
B = ["B", "C", "G", "K", "L", "Q", "T", "Y"]
M_ = ["m" + b for b in B]
VV = B + M_
IXV = {v: i for i, v in enumerate(VV)}
mat = lambda v, p_: next(v[IXV["m" + b]] for b in B if v[IXV[b]] == p_)
conds = [("Exactly four of the boxes are wooden and the other four are plastic.", tuple(M_),
          lambda *m: m.count("W") == 4),
         ("No two wooden boxes are kept one directly on top of the other.", tuple(VV),
          lambda *v: all(not (mat(v, p_) == "W" and mat(v, p_ + 1) == "W") for p_ in range(1, 8))),
         ("Box K is wooden and is kept fifth from the top.", ("K", "mK"), lambda k, m: 9 - k == 5 and m == "W"),
         ("Box Q is kept immediately below box K.", ("Q", "K"), lambda q, k: q == k - 1),
         ("Box L is plastic and is kept at the bottom.", ("L", "mL"), lambda l, m: l == 1 and m == "P"),
         ("Only two boxes are kept between box T and box Q, and box T is above box Q.", ("T", "Q"),
          lambda t, q: t == q + 3),
         ("Box Y is kept immediately above box T.", ("Y", "T"), lambda y, t: y == t + 1),
         ("Box G is wooden and is kept somewhere below box C.", ("G", "mG", "C"), lambda g, m, c: m == "W" and g < c),
         ("Box C is plastic.", ("mC",), lambda m: m == "P")]
X3 = unique(VV, {b: range(1, 9) for b in B} | {m: "WP" for m in M_}, conds, [B])
at = {X3[b]: b for b in B}
MATN = {"W": "wooden", "P": "plastic"}
assert [(at[i], X3["m" + at[i]]) for i in range(1, 9)] == [
    ("L", "P"), ("G", "W"), ("Q", "P"), ("K", "W"), ("C", "P"), ("T", "W"), ("Y", "P"), ("B", "W")]
top = at[8]
mcq(BOX, STK, "Advanced",
    "Eight boxes B, C, G, K, L, Q, T and Y are kept one above another in a single stack (position 1 is the bottom, "
    "8 the top). Each box is either wooden or plastic.\n" + bullets(conds) +
    "\n\nWhich box is kept at the top, and what is it made of?", f"Box {top}, wooden",
    ["Box Y, plastic", "Box B, plastic", "Box T, wooden"], "Alternation rules fix the materials",
    "K is fifth from the top, i.e. position 4 (wooden); Q = 3, T = 6, Y = 7, L = 1 (plastic). B, C and G take "
    "positions 2, 5 and 8. G is wooden: position 5 would sit on wooden K, so G = 2, which forces Q (3) to be plastic. "
    "C is above G and plastic, so C is at 5 or 8. Position 5 sits on wooden K, so it must be plastic anyway; the "
    "wooden boxes so far are G and K, and two more are needed among positions 6, 7 and 8 without two in a row — that "
    "means 6 and 8 are wooden and 7 plastic. So T (6) is wooden, C = 5 (plastic) and B = 8 (wooden).",
    ["K = 4 (wooden), Q = 3, T = 6, Y = 7, L = 1", "G wooden cannot be at 5 ⇒ G = 2, Q plastic",
     "Two more wooden among 6, 7, 8 with none adjacent ⇒ 6 and 8 wooden", "C plastic ⇒ C = 5, B = 8 (wooden)"],
    why_others_wrong="Y is at position 7 (plastic) just below the top; B is wooden, not plastic; T is wooden but at "
                     "position 6.", seconds=150, verified_by=BRUTE)

# ---- X4 Advanced (standalone): seven coloured boxes; the top three are then moved one by one to a new stack
B = ["A", "D", "H", "M", "O", "U", "W"]
CO = ["Amber", "Coral", "Cyan", "Indigo", "Lemon", "Lilac", "Rust"]
C_ = ["c" + b for b in B]
VV = B + C_
IXV = {v: i for i, v in enumerate(VV)}
pc = lambda v, x: next(v[IXV[b]] for b in B if v[IXV["c" + b]] == x)
conds = [("Box A is kept exactly in the middle of the stack and is Cyan.", ("A", "cA"),
          lambda a, c: a == 4 and c == "Cyan"),
         ("The Lilac box is kept at the top.", tuple(VV), lambda *v: pc(v, "Lilac") == 7),
         ("Box U is kept immediately above box A, and only one box is kept between box U and box M.",
          ("U", "A", "M"), lambda u, a, m: u == a + 1 and abs(u - m) == 2),
         ("Box M is kept somewhere above box D, and box D is Amber.", ("M", "D", "cD"),
          lambda m, d, c: m > d and c == "Amber"),
         ("Box H is kept immediately below the Lemon box.", tuple(VV), lambda *v: v[IXV["H"]] == pc(v, "Lemon") - 1),
         ("Box O is Indigo and is kept at the bottom.", ("O", "cO"), lambda o, c: o == 1 and c == "Indigo"),
         ("Box W is kept somewhere above box H.", ("W", "H"), lambda w, h: w > h),
         ("Box U is not Coral.", ("cU",), lambda c: c != "Coral")]
X4 = unique(VV, {b: range(1, 8) for b in B} | {c: CO for c in C_}, conds, [B, C_])
at = {X4[b]: b for b in B}
assert [(at[i], X4["c" + at[i]]) for i in range(1, 8)] == [
    ("O", "Indigo"), ("H", "Coral"), ("W", "Lemon"), ("A", "Cyan"), ("U", "Rust"), ("D", "Amber"), ("M", "Lilac")]
new_stack = [at[7], at[6], at[5]]  # first box removed goes to the bottom of the new stack
amber = next(b for b in B if X4["c" + b] == "Amber")
ans = new_stack[new_stack.index(amber) + 1]
assert new_stack == ["M", "D", "U"] and ans == "U"
mcq(BOX, BWC, "Advanced",
    "Seven boxes A, D, H, M, O, U and W are kept one above another in a single stack (position 1 is the bottom, 7 the "
    "top). Each is of a different colour among Amber, Coral, Cyan, Indigo, Lemon, Lilac and Rust.\n" + bullets(conds) +
    "\n\nThe three topmost boxes are now taken off one at a time, always from the top of the stack, and placed one on "
    "top of another to form a new stack beside it (the first box taken off is at the bottom of the new stack). Which "
    "box is then kept immediately above the Amber box?", "Box " + ans, ["Box M", "Box A", "Box W"],
    "Moving boxes one at a time reverses their order",
    "A (Cyan) = 4, O (Indigo) = 1, U = 5, and M is two places from U: 3 or 7. M is above D, and D must be somewhere "
    "below M; if M were 3, D would be at 2, H and W would take 6 and 7 with H = 6, and the Lemon box would have to be "
    "at 7 — but the top box is Lilac. So M = 7 (Lilac) and D = 6 (Amber). H and W take 2 and 3 with W above H: H = 2, W = 3 (Lemon). U is not "
    "Coral, so U is Rust and H Coral. Stack: O, H, W, A, U, D, M. Taking M, then D, then U off the top builds a new "
    "stack M (bottom), D, U (top). Immediately above D (Amber) is U.",
    ["A 4, O 1, U 5; M 7 (Lilac), D 6 (Amber)", "H 2 (Coral), W 3 (Lemon), U Rust",
     "Moved one by one: M, D, U ⇒ new stack bottom→top M, D, U", "Above D ⇒ U"],
    why_others_wrong="M was above D in the original stack but is below it in the new one; A and W stay in the "
                     "original stack.", seconds=150, verified_by=BRUTE)

# ================================================================================================ MONTH / DATE / YEAR
MB, DB, YB = "Month-based", "Date-based", "Year-based"
WD = lambda y, m, d_: dt.date(y, m, d_).strftime("%A")
mq = lambda sid_, sub, diff: (lambda text, correct, wrongs, concept, expl, steps, **kw: puzzle_q(
    sid_, MON, sub, diff, text, correct, wrongs, concept, expl, steps, **kw))

# ---- M1 Basic set: six saplings planted in six months from June to November, one tree each
P = ["Anokhi", "Girdhar", "Kanishka", "Maitreyi", "Pankaj", "Suhani"]
TR = ["Ashoka", "Banyan", "Jamun", "Mango", "Neem", "Peepal"]
T_ = ["t" + p for p in P]
VV = P + T_
IXV = {v: i for i, v in enumerate(VV)}
mon_of = lambda v, x: next(v[IXV[p]] for p in P if v[IXV["t" + p]] == x)
conds = [
    ("Kanishka plants in the last of the six months, and she plants the Ashoka.", ("Kanishka", "tKanishka"),
     lambda k, t: k == 11 and t == "Ashoka"),
    ("Girdhar plants in a month that has 30 days.", ("Girdhar",), lambda g: MDAYS[g] == 30),
    ("Pankaj plants before Girdhar, and only two persons plant between them.", ("Pankaj", "Girdhar"),
     lambda p, g: g - p == 3),
    ("The Neem sapling is planted in June.", tuple(VV), lambda *v: mon_of(v, "Neem") == 6),
    ("Anokhi plants in the month immediately after Pankaj's month, and she plants the Mango.",
     ("Anokhi", "Pankaj", "tAnokhi"), lambda a, p, t: a == p + 1 and t == "Mango"),
    ("Maitreyi plants in a month after Suhani's month.", ("Maitreyi", "Suhani"), lambda m, s: m > s),
    ("The Banyan is planted in the month immediately before the Ashoka.", tuple(VV),
     lambda *v: mon_of(v, "Banyan") == mon_of(v, "Ashoka") - 1),
    ("Suhani does not plant the Peepal.", ("tSuhani",), lambda t: t != "Peepal"),
]
M1 = unique(VV, {p: range(6, 12) for p in P} | {t: TR for t in T_}, conds, [P, T_])
mo = {p: M1[p] for p in P}
tr = {p: M1["t" + p] for p in P}
ORD = sorted(P, key=mo.get)
assert [(MNAME[mo[p]], p, tr[p]) for p in ORD] == [
    ("June", "Pankaj", "Neem"), ("July", "Anokhi", "Mango"), ("August", "Suhani", "Jamun"),
    ("September", "Girdhar", "Peepal"), ("October", "Maitreyi", "Banyan"), ("November", "Kanishka", "Ashoka")]
ARR = "; ".join(f"{MNAME[mo[p]]}: {p} ({tr[p]})" for p in ORD)
sid = stimulus("puzzle", "Six saplings planted from June to November",
               "Six persons Anokhi, Girdhar, Kanishka, Maitreyi, Pankaj and Suhani each plant one sapling in the same "
               "year, one person in each month from June to November. Each plants a different tree among Ashoka, "
               "Banyan, Jamun, Mango, Neem and Peepal.", conds,
               "Step 1: Kanishka = November (Ashoka). Girdhar's month has 30 days: June, September or November; Pankaj "
               "is three months before him, so Girdhar = September and Pankaj = June (Neem).\n"
               "Step 2: Anokhi = July (Mango). August and October remain for Suhani and Maitreyi; Maitreyi is later, so "
               "Suhani = August and Maitreyi = October.\n"
               "Step 3: Banyan is immediately before Ashoka (November): October, Maitreyi. Jamun and Peepal remain for "
               "Suhani and Girdhar; Suhani is not Peepal, so Suhani Jamun and Girdhar Peepal.\n\n"
               + table(["Month", "Person", "Tree"], [(MNAME[mo[p]], p, tr[p]) for p in ORD]))
Q = mq(sid, MB, "Basic")
ans = next(p for p in P if tr[p] == "Jamun")
assert ans == "Suhani"
Q("Who plants the Jamun sapling?", ans, ["Girdhar", "Maitreyi", "Anokhi"], "Elimination on the last two trees",
  "Neem, Mango, Banyan and Ashoka are fixed; Jamun and Peepal remain for Suhani and Girdhar, and Suhani does not "
  "plant the Peepal.", [ARR, "Suhani ≠ Peepal ⇒ Suhani Jamun"],
  why_others_wrong="Girdhar plants the Peepal, Maitreyi the Banyan and Anokhi the Mango.", seconds=45)
Q("In which month does Maitreyi plant her sapling?", MNAME[mo["Maitreyi"]], ["August", "September", "November"],
  "Order clue between two persons", "August and October are left for Suhani and Maitreyi, and Maitreyi plants later: "
                                    "October.", [ARR, "Suhani August, Maitreyi October"],
  why_others_wrong="August is Suhani's month, September Girdhar's and November Kanishka's.", seconds=40)
cnt = abs(mo["Anokhi"] - mo["Maitreyi"]) - 1
assert cnt == 2
Q("How many persons plant between Anokhi and Maitreyi?", num_word(cnt), ["One", "Three", "None"],
  "Count the months strictly between", "Anokhi plants in July and Maitreyi in October; Suhani (August) and Girdhar "
                                       "(September) plant between them.", [ARR, "Between July and October: two"],
  natural=by_num, seconds=40)
ans = next(tr[p] for p in P if mo[p] == 9)
assert ans == "Peepal"
Q("Which sapling is planted in September?", ans, ["Jamun", "Banyan", "Neem"], "Read the tree for a month",
  "Girdhar plants in September, and he plants the Peepal.", [ARR, "September: Girdhar ⇒ Peepal"],
  why_others_wrong="Jamun is planted in August, Banyan in October and Neem in June.", seconds=40)
stm = [("July – Anokhi – Mango", mo["Anokhi"] == 7 and tr["Anokhi"] == "Mango"),
       ("June – Pankaj – Peepal", tr["Pankaj"] == "Peepal"),
       ("October – Suhani – Banyan", mo["Suhani"] == 10),
       ("November – Girdhar – Ashoka", mo["Girdhar"] == 11)]
t, f = one_true(stm)
Q("Which of the following month – person – tree combinations is correct?", t, f, "Check all three parts",
  "From the table: " + ARR + ".", [ARR],
  why_others_wrong="Pankaj plants the Neem; October is Maitreyi's month; November is Kanishka's.", seconds=45)

# ---- M2 Intermediate (standalone): five birthday months and month lengths
P = ["Ambar", "Keertana", "Nishant", "Saloni", "Varad"]
conds = [("Of the five, only Saloni was born in a month that has fewer than 30 days.", tuple(P),
          lambda *v: MDAYS[v[3]] < 30 and all(MDAYS[x] >= 30 for i, x in enumerate(v) if i != 3)),
         ("Varad was born in the month immediately after Saloni's month.", ("Varad", "Saloni"),
          lambda v_, s: v_ == s + 1),
         ("Exactly three months come between Varad's month and Keertana's month, and Keertana was born after Varad.",
          ("Keertana", "Varad"), lambda k, v_: k - v_ == 4),
         ("Ambar was born in a month that has 31 days and comes between Varad's and Keertana's months.",
          ("Ambar", "Varad", "Keertana"), lambda a, v_, k: MDAYS[a] == 31 and v_ < a < k),
         ("Nishant was born four months after Keertana.", ("Nishant", "Keertana"), lambda n, k: n == k + 4)]
M2 = unique(P, {p: range(1, 13) for p in P}, conds, [P])
assert {p: MNAME[M2[p]] for p in P} == {"Ambar": "May", "Keertana": "July", "Nishant": "November",
                                        "Saloni": "February", "Varad": "March"}
cnt = sum(1 for p in P if MDAYS[M2[p]] == 31)
assert cnt == 3
mcq(MON, MB, "Intermediate",
    "Five friends Ambar, Keertana, Nishant, Saloni and Varad were born in five different months of the same year "
    "(not a leap year).\n" + bullets(conds) + "\n\nHow many of the five were born in a month that has 31 days?",
    num_word(cnt), ["Two", "Four", "One"], "Month lengths: 30 days hath September, April, June and November",
    "Only February has fewer than 30 days, so Saloni = February and Varad = March. Keertana is four months after Varad: "
    "July. Ambar's month lies between March and July and has 31 days: May (April and June have 30). Nishant is four "
    "months after July: November. The 31-day months among these are March, May and July — Varad, Ambar and Keertana: "
    "three persons.",
    ["Saloni February ⇒ Varad March", "Keertana July", "Ambar: between March and July with 31 days ⇒ May",
     "Nishant November (30 days)", "31-day months: March, May, July ⇒ three"],
    why_others_wrong="Two leaves out one of March, May and July; Four counts November, which has 30 days; One counts "
                     "only July.", natural=by_num, seconds=75, verified_by=BRUTE)

# ---- M3 Intermediate (standalone): bill payments on the Wednesdays and Saturdays of September 2026
assert WD(2026, 9, 1) == "Tuesday"
SLS = [k for k in range(1, 31) if dt.date(2026, 9, k).weekday() in (2, 5)]
assert SLS == [2, 5, 9, 12, 16, 19, 23, 26, 30]
wd3 = lambda k: dt.date(2026, 9, k).strftime("%A")
P = ["Hari", "Jaya", "Kamal", "Lekha", "Mridul"]
conds = [("Hari pays on the second Saturday of the month.", ("Hari",), lambda h: h == 12),
         ("Jaya pays exactly 11 days after Hari.", ("Jaya", "Hari"), lambda j, h: j == h + 11),
         ("Kamal pays on a Wednesday before Hari, and exactly one of the five pays before Kamal.", tuple(P),
          lambda *v: wd3(v[2]) == "Wednesday" and v[2] < v[0] and sum(1 for x in v if x < v[2]) == 1),
         ("Lekha pays exactly one week before or exactly one week after Kamal.", ("Lekha", "Kamal"),
          lambda l, k: abs(l - k) == 7),
         ("Mridul pays on a Saturday after Jaya.", ("Mridul", "Jaya"), lambda m, j: wd3(m) == "Saturday" and m > j)]
M3 = unique(P, {p: SLS for p in P}, conds, [P])
assert M3 == {"Hari": 12, "Jaya": 23, "Kamal": 9, "Lekha": 2, "Mridul": 26}
mcq(MON, DB, "Intermediate",
    "A cooperative society accepts bill payments only on Wednesdays and Saturdays. Five members Hari, Jaya, Kamal, "
    "Lekha and Mridul each pay once in September 2026, on five different dates. 1 September 2026 is a Tuesday.\n"
    + bullets(conds) + "\n\nOn which date does Lekha pay?", "2 September", ["16 September", "5 September",
                                                                          "19 September"],
    "List the allowed dates first, then place each person",
    "The Wednesdays are 2, 9, 16, 23 and 30 September and the Saturdays 5, 12, 19 and 26. Hari = 12 (second Saturday); "
    "Jaya = 23 (a Wednesday). Kamal pays on a Wednesday before the 12th: the 2nd or the 9th. Exactly one person pays "
    "before Kamal; Hari, Jaya and Mridul (a Saturday after the 23rd: the 26th) all pay later, so that person must be "
    "Lekha. Then Kamal cannot be on the 2nd, so Kamal = 9 and Lekha, one week away and earlier, = 2 September.",
    ["Allowed: Wed 2, 9, 16, 23, 30; Sat 5, 12, 19, 26", "Hari 12, Jaya 23, Mridul 26",
     "Kamal Wed before 12 with exactly one person before him ⇒ Kamal 9, Lekha before him",
     "Lekha = 9 − 7 = 2 September"],
    why_others_wrong="16 September is one week after Kamal, but then nobody would pay before Kamal; 5 and 19 "
                     "September are Saturdays not a week away from Kamal.", seconds=90, verified_by=BRUTE)

# ---- M4 Advanced set: birth years and birth months; ages in completed years as on 1 June 2026
P = ["Avantika", "Dinkar", "Gurpreet", "Mallika", "Naresh", "Shobhit"]
YRS = [1981, 1986, 1992, 1995, 1999, 2004]
MS6 = [1, 3, 5, 7, 9, 11]
Y_ = ["y" + p for p in P]
M_ = ["m" + p for p in P]
VV = P + [x for p in P for x in ("y" + p, "m" + p)]
IXV = {v: i for i, v in enumerate(VV)}
age = lambda y, m: 2026 - y - (1 if m > 6 else 0)  # completed years on 1 June 2026 (no birthday falls in June)
who_y = lambda v, y: next(p for p in P if v[IXV["y" + p]] == y)
conds = [
    ("The person born in 1992 was born in March.", tuple(VV),
     lambda *v: v[IXV["m" + who_y(v, 1992)]] == 3),
    ("Gurpreet is the youngest of the six and was born in January.", ("yGurpreet", "mGurpreet"),
     lambda y, m: y == 2004 and m == 1),
    ("Dinkar is the oldest of the six.", ("yDinkar",), lambda y: y == 1981),
    ("As on 1 June 2026, Mallika is 30 years old and Avantika is 34 years old (in completed years).",
     ("yMallika", "mMallika", "yAvantika", "mAvantika"),
     lambda ym, mm, ya, ma: age(ym, mm) == 30 and age(ya, ma) == 34),
    ("Naresh was born in May, and he is younger than Mallika.", ("mNaresh", "yNaresh", "yMallika"),
     lambda m, y, ym: m == 5 and y > ym),
    ("Shobhit was born in July, in a year before Avantika's year.", ("mShobhit", "yShobhit", "yAvantika"),
     lambda m, y, ya: m == 7 and y < ya),
    ("Mallika was born in the latest of the six months.", ("mMallika",), lambda m: m == 11),
]
M4 = unique(VV, {p: [0] for p in P} | {f"y{p}": YRS for p in P} | {f"m{p}": MS6 for p in P}, conds,
            [Y_, M_])
yr = {p: M4["y" + p] for p in P}
mn = {p: M4["m" + p] for p in P}
ag = {p: age(yr[p], mn[p]) for p in P}
ORD = sorted(P, key=yr.get)
assert [(p, yr[p], MNAME[mn[p]], ag[p]) for p in ORD] == [
    ("Dinkar", 1981, "September", 44), ("Shobhit", 1986, "July", 39), ("Avantika", 1992, "March", 34),
    ("Mallika", 1995, "November", 30), ("Naresh", 1999, "May", 27), ("Gurpreet", 2004, "January", 22)]
ARR = "; ".join(f"{p}: {MNAME[mn[p]]} {yr[p]} (age {ag[p]})" for p in ORD)
sid = stimulus("puzzle", "Six birth years, six birth months, ages on 1 June 2026",
               "Six persons Avantika, Dinkar, Gurpreet, Mallika, Naresh and Shobhit were born in six different years "
               "among 1981, 1986, 1992, 1995, 1999 and 2004, and in six different months among January, March, May, "
               "July, September and November (one year and one month each). Ages are counted in completed years as on "
               "1 June 2026: a person whose birthday month is later in the year than June has not yet had a 2026 "
               "birthday on that date.", conds,
               "Step 1: Gurpreet = January 2004 (youngest); Dinkar = 1981 (oldest).\n"
               "Step 2: Avantika is 34 on 1 June 2026: born in 1992 with a birthday by June, or in 1991 with a later "
               "birthday — 1991 is not in the list, so Avantika = 1992, and the 1992-born person was born in March: "
               "Avantika = March 1992.\n"
               "Step 3: Mallika is 30: 1996 with an early birthday (not in the list) or 1995 with a birthday after "
               "June. So Mallika = 1995, and she has the latest month, November.\n"
               "Step 4: Shobhit = July, in a year before 1992: 1986 (1981 is Dinkar's). Naresh = May, younger than "
               "Mallika: 1999. Dinkar takes the last month, September.\n\n"
               + table(["Person", "Year", "Month", "Age on 1 June 2026"],
                       [(p, yr[p], MNAME[mn[p]], ag[p]) for p in ORD]))
Q = mq(sid, YB, "Advanced")
Q("As on 1 June 2026, what is Dinkar's age in completed years?", str(ag["Dinkar"]), ["45", "43", "46"],
  "A September birthday has not yet come by 1 June",
  "Dinkar was born in September 1981. On 1 June 2026 his 2026 birthday has not yet come, so he is 2026 − 1981 − 1 = 44 "
  "years old.", [ARR, "Dinkar: September 1981", "2026 − 1981 = 45, minus 1 (birthday after June) ⇒ 44"],
  why_others_wrong="45 ignores that his birthday comes after 1 June; 43 and 46 are off by one more year.", natural=int,
  seconds=120)
ans = next(p for p in P if yr[p] == 1986)
assert ans == "Shobhit"
Q("Who was born in 1986?", ans, ["Avantika", "Naresh", "Dinkar"], "A 'before' clue with two years excluded",
  "Shobhit's year is before Avantika's (1992), so it is 1981 or 1986; 1981 is Dinkar's, so Shobhit was born in 1986.",
  [ARR, "Shobhit before 1992 and not 1981 ⇒ 1986"],
  why_others_wrong="Avantika was born in 1992, Naresh in 1999 and Dinkar in 1981.", seconds=100)
cnt = sum(1 for p in P if mn[p] <= 5)
assert cnt == 3
Q("How many of the six had already had their 2026 birthday on 1 June 2026?", num_word(cnt), ["Two", "Four", "Six"],
  "Only the January, March and May birthdays fall before June",
  "Birthdays in January (Gurpreet), March (Avantika) and May (Naresh) come before 1 June; July, September and "
  "November do not. Three persons.", [ARR, "Before June: January, March, May ⇒ three"],
  why_others_wrong="Two, Four and Six miscount the months that come before June.", natural=by_num, seconds=100)
diff = ag["Mallika"] - ag["Naresh"]
assert diff == 3 and yr["Naresh"] - yr["Mallika"] == 4
Q("As on 1 June 2026, by how many completed years is Mallika older than Naresh?", str(diff), ["4", "5", "2"],
  "The birth-year gap and the age gap need not match",
  "Naresh (May 1999) is 27, since his birthday has passed; Mallika (November 1995) is 30, since hers has not. "
  "30 − 27 = 3, although their birth years are four apart.",
  [ARR, "Naresh 2026 − 1999 = 27", "Mallika 2026 − 1995 − 1 = 30", "30 − 27 = 3"],
  why_others_wrong="4 is the gap between the birth years; 5 and 2 come from mixing up which birthday has passed.",
  natural=int, seconds=110)
stm = [("Avantika – March – 1992", mn["Avantika"] == 3 and yr["Avantika"] == 1992),
       ("Naresh – May – 1995", yr["Naresh"] == 1995),
       ("Dinkar – November – 1981", mn["Dinkar"] == 11),
       ("Shobhit – July – 1981", yr["Shobhit"] == 1981)]
t, f = one_true(stm)
Q("Which of the following person – month – year combinations is correct?", t, f, "Check all three parts",
  "From the table: " + ARR + ".", [ARR],
  why_others_wrong="Naresh was born in 1999, Dinkar in September, and Shobhit in 1986.", seconds=90)

# ---- M5 Advanced set: six visits on the weekend dates of August 2026 (1 August 2026 is a Saturday)
assert WD(2026, 8, 1) == "Saturday"
WK = [k for k in range(1, 32) if dt.date(2026, 8, k).weekday() in (5, 6)]
assert WK == [1, 2, 8, 9, 15, 16, 22, 23, 29, 30]
wdA = lambda k: dt.date(2026, 8, k).strftime("%A")
wkno = lambda k: (k - 1) // 7  # weekend index: 1–2 → 0, 8–9 → 1, ...
P = ["Aparna", "Gajendra", "Kaushiki", "Manohar", "Riddhima", "Tejpal"]
conds = [
    ("Kaushiki visits on the third Saturday of the month, and Gajendra visits on the day after Kaushiki.",
     ("Kaushiki", "Gajendra"), lambda k, g: k == 15 and g == k + 1),
    ("Riddhima visits on the last Saturday of the month.", ("Riddhima",), lambda r: r == 29),
    ("Tejpal visits exactly one week after Gajendra.", ("Tejpal", "Gajendra"), lambda t, g: t == g + 7),
    ("Aparna visits exactly two weeks before Kaushiki.", ("Aparna", "Kaushiki"), lambda a, k: a == k - 14),
    ("Manohar visits on a Sunday before Kaushiki, but not on the same weekend as Aparna.",
     ("Manohar", "Kaushiki", "Aparna"), lambda m, k, a: wdA(m) == "Sunday" and m < k and wkno(m) != wkno(a)),
]
M5 = unique(P, {p: WK for p in P}, conds, [P])
assert M5 == {"Aparna": 1, "Gajendra": 16, "Kaushiki": 15, "Manohar": 9, "Riddhima": 29, "Tejpal": 23}
ORD = sorted(P, key=M5.get)
ARR = "; ".join(f"{M5[p]} Aug ({wdA(M5[p])[:3]}): {p}" for p in ORD)
sid = stimulus("puzzle", "Six visits on the weekends of August 2026",
               "A heritage museum is open to visitors only on Saturdays and Sundays. Six persons Aparna, Gajendra, "
               "Kaushiki, Manohar, Riddhima and Tejpal each visit it once in August 2026, on six different dates. "
               "1 August 2026 is a Saturday.", conds,
               "Step 1: The Saturdays are 1, 8, 15, 22 and 29 August and the Sundays 2, 9, 16, 23 and 30 August.\n"
               "Step 2: Kaushiki = 15 (third Saturday), Gajendra = 16, Tejpal = 23, Riddhima = 29 (last Saturday), "
               "Aparna = 15 − 14 = 1.\n"
               "Step 3: Manohar visits on a Sunday before the 15th: the 2nd or the 9th. The 2nd is on Aparna's weekend "
               "(1–2 August), so Manohar = 9.\n\n"
               + table(["Date", "Day", "Visitor"], [(f"{M5[p]} August", wdA(M5[p]), p) for p in ORD]))
Q = mq(sid, DB, "Advanced")
cnt = sum(1 for p in P if wdA(M5[p]) == "Sunday")
assert cnt == 3
Q("How many of the six visit on a Sunday?", num_word(cnt), ["Two", "Four", "One"], "Weekday of each fixed date",
  "Manohar (9th), Gajendra (16th) and Tejpal (23rd) visit on Sundays; Aparna, Kaushiki and Riddhima visit on "
  "Saturdays.", [ARR, "Sundays: 9, 16, 23 ⇒ three"], natural=by_num, seconds=90)
ans = next(p for p in P if M5[p] == M5["Manohar"] + 20)
assert ans == "Riddhima"
Q("Who visits exactly 20 days after Manohar?", ans, ["Tejpal", "Gajendra", "Kaushiki"],
  "Fix the last open person before doing date arithmetic",
  "Manohar visits on 9 August (the 2nd is ruled out because it is Aparna's weekend). 9 + 20 = 29 August: Riddhima.",
  [ARR, "Manohar = 9", "9 + 20 = 29 ⇒ Riddhima"],
  why_others_wrong="Tejpal visits 14 days after Manohar, Gajendra 7 days and Kaushiki 6 days after him. Taking "
                   "Manohar on the 2nd would point to 22 August, when nobody visits.", seconds=100)
stm = [("Tejpal visits on 23 August, a Sunday", M5["Tejpal"] == 23 and wdA(23) == "Sunday"),
       ("Aparna and Manohar visit on the same weekend", wkno(M5["Aparna"]) == wkno(M5["Manohar"])),
       ("Gajendra visits on a Saturday", wdA(M5["Gajendra"]) == "Saturday"),
       ("Exactly three persons visit before Kaushiki", sum(1 for p in P if M5[p] < M5["Kaushiki"]) == 3)]
t, f = one_true(stm)
Q("Which of the following statements is true?", t, f, "Checking each statement against the dates",
  "Tejpal visits one week after Gajendra (16th): 23 August, a Sunday — true. Aparna (1st) and Manohar (9th) visit on "
  "different weekends; Gajendra visits on a Sunday; and only two persons — Aparna and Manohar — visit before "
  "Kaushiki.", [ARR], seconds=100)

# ================================================================================================ PUZZLES (OTHER)
OTH = "Puzzles (Other)"
DSG, CMP, DAY = "Designation", "Comparison and ordering", "Day-based"

# ---- O1 Basic (standalone): five pencils of different lengths
PC = ["A", "B", "C", "D", "E"]
conds = [("Pencil B is longer than pencil D but shorter than pencil A.", ("B", "D", "A"), lambda b, d, a: d < b < a),
         ("Pencil E is shorter than pencil D.", ("E", "D"), lambda e, d: e < d),
         ("Pencil C is longer than pencil A.", ("C", "A"), lambda c, a: c > a)]
O1 = unique(PC, {p: range(1, 6) for p in PC}, conds, [PC])  # 5 = longest
ans = next(p for p in PC if O1[p] == 3)
assert ans == "B"
mcq(OTH, CMP, "Basic",
    "Five pencils A, B, C, D and E have different lengths.\n" + bullets(conds) + "\n\nWhich pencil is the third "
    "longest?", "Pencil " + ans, ["Pencil A", "Pencil D", "Pencil C"], "Build one chain from the comparisons",
    "B is between D and A: A > B > D. E is shorter than D, and C is longer than A. So C > A > B > D > E, and the third "
    "longest is B.", ["A > B > D", "D > E; C > A", "C > A > B > D > E ⇒ third = B"],
    why_others_wrong="A is the second longest, D the fourth and C the longest.", seconds=35, verified_by=BRUTE)

# ---- O2 Intermediate set: eight meetings in the morning and afternoon slots of Monday to Thursday
P = ["Aalok", "Bhupesh", "Daya", "Hemraj", "Kanika", "Mohsin", "Rewa", "Tarini"]
DN = ["Monday", "Tuesday", "Wednesday", "Thursday"]
dayof = lambda s: DN[(s - 1) // 2]
slot = lambda s: "morning" if s % 2 == 1 else "afternoon"
conds = [("Hemraj's meeting is on Wednesday afternoon.", ("Hemraj",), lambda h: h == 6),
         ("Aalok meets before Hemraj, and only one meeting is held between their meetings.", ("Aalok", "Hemraj"),
          lambda a, h: h - a == 2),
         ("Kanika meets on the same day as Aalok.", ("Kanika", "Aalok"), lambda k, a: dayof(k) == dayof(a)),
         ("Mohsin's meeting is the last of the week, and Bhupesh meets on the same day as Mohsin.",
          ("Mohsin", "Bhupesh"), lambda m, b: m == 8 and dayof(b) == dayof(m)),
         ("Tarini meets in a morning slot on a day after Kanika's day.", ("Tarini", "Kanika"),
          lambda t, k: slot(t) == "morning" and dayof(t) != dayof(k) and t > k),
         ("Rewa meets in an afternoon slot.", ("Rewa",), lambda r: slot(r) == "afternoon")]
O2 = unique(P, {p: range(1, 9) for p in P}, conds, [P])
at = {v: k for k, v in O2.items()}
assert [at[i] for i in range(1, 9)] == ["Daya", "Rewa", "Kanika", "Aalok", "Tarini", "Hemraj", "Bhupesh", "Mohsin"]
ARR = "; ".join(f"{dayof(i)} {slot(i)}: {at[i]}" for i in range(1, 9))
sid = stimulus("puzzle", "Eight meetings in morning and afternoon slots",
               "A branch manager holds two meetings a day — one in the morning and one in the afternoon — from Monday "
               "to Thursday of a week, so there are eight meeting slots. Eight customers Aalok, Bhupesh, Daya, Hemraj, "
               "Kanika, Mohsin, Rewa and Tarini each have one meeting, in different slots. (Monday morning is the first "
               "slot and Thursday afternoon the last; slots are counted in this order.)", conds,
               "Number the slots 1 (Monday morning) to 8 (Thursday afternoon).\n"
               "Step 1: Hemraj = 6 (Wednesday afternoon). Aalok = 4 (Tuesday afternoon), so Kanika = 3 (Tuesday "
               "morning).\n"
               "Step 2: Mohsin = 8 and Bhupesh = 7 (Thursday morning).\n"
               "Step 3: Tarini has a morning slot on a day after Tuesday: Wednesday morning (5), as Thursday morning "
               "is taken.\n"
               "Step 4: Slots 1 and 2 remain; Rewa takes the afternoon slot (2) and Daya slot 1.\n\n"
               + table(["Day", "Morning", "Afternoon"], [(DN[d], at[2 * d + 1], at[2 * d + 2]) for d in range(4)]))
Q = lambda text, correct, wrongs, concept, expl, steps, **kw: puzzle_q(sid, OTH, DAY, "Intermediate", text, correct,
                                                                       wrongs, concept, expl, steps, **kw)
Q("Who meets the manager on Monday morning?", at[1], ["Rewa", "Kanika", "Tarini"], "The last open slots go last",
  "Slots 3 to 8 are fixed by the clues about Hemraj, Aalok, Kanika, Mohsin, Bhupesh and Tarini. Rewa needs an "
  "afternoon slot, so she takes Monday afternoon and Daya Monday morning.",
  [ARR, "Open: Monday morning and afternoon", "Rewa afternoon ⇒ Daya morning"],
  why_others_wrong="Rewa meets on Monday afternoon, Kanika on Tuesday morning and Tarini on Wednesday morning.",
  seconds=60)
ans = at[O2["Tarini"] + 1]
assert ans == "Hemraj"
Q("Whose meeting comes immediately after Tarini's?", ans, ["Aalok", "Bhupesh", "Mohsin"],
  "Consecutive slots run morning → afternoon → next morning",
  "Tarini meets on Wednesday morning; the next slot is Wednesday afternoon, Hemraj's.",
  [ARR, "Wednesday morning → Wednesday afternoon = Hemraj"],
  why_others_wrong="Aalok's meeting is just before Tarini's; Bhupesh and Mohsin meet on Thursday.", seconds=55)
cnt = O2["Tarini"] - O2["Rewa"] - 1
assert cnt == 2
Q("How many meetings are held between Rewa's meeting and Tarini's meeting?", num_word(cnt), ["One", "Three", "Four"],
  "Count slots, not days", "Rewa has slot 2 and Tarini slot 5; slots 3 and 4 (Kanika and Aalok) lie between them.",
  [ARR, "Slots 3, 4 between 2 and 5 ⇒ two"],
  why_others_wrong="One counts the day (Tuesday) instead of its two slots; Three and Four include an end slot.",
  natural=by_num, seconds=55)
Q("When does Bhupesh meet the manager?", f"{dayof(O2['Bhupesh'])} {slot(O2['Bhupesh'])}",
  ["Thursday afternoon", "Wednesday morning", "Tuesday afternoon"], "Same day as the last slot",
  "Mohsin has the last slot, Thursday afternoon; Bhupesh meets on the same day, so he has Thursday morning.",
  [ARR, "Mohsin: Thursday afternoon ⇒ Bhupesh: Thursday morning"],
  why_others_wrong="Thursday afternoon is Mohsin's slot, Wednesday morning Tarini's and Tuesday afternoon Aalok's.",
  seconds=50)

# ---- O3 Intermediate set: six employees, designations and joining years
P = ["Ashwath", "Deeksha", "Faraaz", "Ishika", "Tushita", "Yashwant"]
POSTS = ["Zonal Head", "Regional Head", "Branch Head", "Sales Manager", "Agent Supervisor", "Agent Trainee"]
YRS = [2009, 2012, 2014, 2017, 2020, 2023]
VV = P + ["y" + p for p in P]
IXV = {v: i for i, v in enumerate(VV)}
conds = [("Ishika is senior to all the others, and the person who joined in 2009 is immediately junior to her.",
          tuple(VV), lambda *v: v[IXV["Ishika"]] == 0 and next(p for p in P if v[IXV["y" + p]] == 2009)
          == next(p for p in P if v[IXV[p]] == 1)),
         ("Faraaz joined the earliest of all.", ("yFaraaz",), lambda y: y == 2009),
         ("Deeksha is the most junior, and she joined six years after Ashwath.", ("Deeksha", "yDeeksha", "yAshwath"),
          lambda d, yd, ya: d == 5 and yd == ya + 6),
         ("Ashwath is immediately senior to Tushita, who joined in the latest year.", ("Ashwath", "Tushita",
                                                                                      "yTushita"),
          lambda a, t, y: t == a + 1 and y == 2023),
         ("Yashwant joined in 2017, five years after Ishika, and he is senior to Ashwath.",
          ("yYashwant", "yIshika", "Yashwant", "Ashwath"), lambda yy, yi, y_, a: yy == 2017 and yi == 2012 and y_ < a)]
O3 = unique(VV, {p: range(6) for p in P} | {"y" + p: YRS for p in P}, conds, [P, ["y" + p for p in P]])
post = {p: POSTS[O3[p]] for p in P}
yr = {p: O3["y" + p] for p in P}
ORD = sorted(P, key=O3.get)
assert [(p, post[p], yr[p]) for p in ORD] == [
    ("Ishika", "Zonal Head", 2012), ("Faraaz", "Regional Head", 2009), ("Yashwant", "Branch Head", 2017),
    ("Ashwath", "Sales Manager", 2014), ("Tushita", "Agent Supervisor", 2023), ("Deeksha", "Agent Trainee", 2020)]
ARR = "; ".join(f"{post[p]}: {p} ({yr[p]})" for p in ORD)
sid = stimulus("puzzle", "Six insurance employees: posts and joining years",
               "Six employees Ashwath, Deeksha, Faraaz, Ishika, Tushita and Yashwant of an insurance company hold six "
               "different posts. In decreasing order of seniority the posts are: Zonal Head, Regional Head, Branch "
               "Head, Sales Manager, Agent Supervisor and Agent Trainee. Each joined the company in a different year "
               "among 2009, 2012, 2014, 2017, 2020 and 2023. Seniority of post does not depend on the year of "
               "joining.", conds,
               "Step 1: Ishika = Zonal Head. Faraaz joined in 2009, so he is immediately junior to her: Regional Head. "
               "Deeksha = Agent Trainee.\n"
               "Step 2: Tushita joined in 2023, Yashwant in 2017 and Ishika in 2012. The years left are 2014 and 2020 "
               "for Ashwath and Deeksha, six years apart: Ashwath 2014, Deeksha 2020.\n"
               "Step 3: Branch Head, Sales Manager and Agent Supervisor remain for Ashwath, Tushita and Yashwant, with "
               "Ashwath immediately above Tushita and Yashwant above Ashwath: Yashwant Branch Head, Ashwath Sales "
               "Manager, Tushita Agent Supervisor.\n\n"
               + table(["Post", "Employee", "Joined"], [(post[p], p, yr[p]) for p in ORD]))
Q = lambda text, correct, wrongs, concept, expl, steps, **kw: puzzle_q(sid, OTH, DSG, "Intermediate", text, correct,
                                                                       wrongs, concept, expl, steps, **kw)
ans = next(p for p in P if post[p] == "Branch Head")
assert ans == "Yashwant"
Q("Who is the Branch Head?", ans, ["Ashwath", "Tushita", "Faraaz"], "Place the linked pair, then the free person",
  "Ashwath and Tushita hold two consecutive posts among Branch Head, Sales Manager and Agent Supervisor, and Yashwant "
  "is senior to Ashwath, so Yashwant takes Branch Head.", [ARR, "Yashwant above the pair Ashwath–Tushita ⇒ Branch Head"],
  why_others_wrong="Ashwath is the Sales Manager, Tushita the Agent Supervisor and Faraaz the Regional Head.",
  seconds=70)
p14 = next(p for p in P if yr[p] == 2014)
assert (p14, post[p14]) == ("Ashwath", "Sales Manager")
Q("Who joined in 2014, and what is that person's post?", "Ashwath – Sales Manager",
  ["Deeksha – Agent Trainee", "Ashwath – Branch Head", "Ishika – Zonal Head"], "Year gap fixes the last two years",
  "2014 and 2020 are the only years left for Ashwath and Deeksha, and Deeksha joined six years after Ashwath, so "
  "Ashwath joined in 2014. He is the Sales Manager.", [ARR, "Ashwath 2014, Deeksha 2020", "Ashwath = Sales Manager"],
  why_others_wrong="Deeksha joined in 2020 and Ishika in 2012; Ashwath is not the Branch Head (Yashwant is).",
  seconds=70)
cnt = sum(1 for p in P if O3[p] > O3[next(q_ for q_ in P if yr[q_] == 2017)])
assert cnt == 3
Q("How many employees are junior to the employee who joined in 2017?", num_word(cnt), ["Two", "Four", "One"],
  "Find the person, then count the posts below",
  "Yashwant joined in 2017 and is the Branch Head; the Sales Manager, Agent Supervisor and Agent Trainee — three "
  "employees — are junior to him.", [ARR, "2017: Yashwant (Branch Head) ⇒ three posts below"],
  natural=by_num, seconds=60)

# ---- O4 Advanced (standalone): six runners and their finishing times
P = ["Gaurang", "Hima", "Kuldeep", "Ritika", "Saumya", "Vipul"]
TT = range(45, 80)
rank = lambda v, x: sum(1 for y in v if y < x) + 1
conds = [("Gaurang finished in 58 seconds, and exactly two runners finished before him.", tuple(P),
          lambda *v: v[0] == 58 and rank(v, v[0]) == 3),
         ("Hima finished 4 seconds after Gaurang, and exactly one runner finished between Gaurang and Hima.",
          tuple(P), lambda *v: v[1] == v[0] + 4 and sum(1 for y in v if v[0] < y < v[1]) == 1),
         ("Ritika won the race in 51 seconds, and Vipul finished 3 seconds after Ritika.", ("Ritika", "Vipul"),
          lambda r, v_: r == 51 and v_ == 54),
         ("The average of Kuldeep's and Hima's times is 61 seconds.", ("Kuldeep", "Hima"),
          lambda k, h: k + h == 122),
         ("Saumya finished last, 7 seconds after Kuldeep.", tuple(P),
          lambda *v: v[4] == v[2] + 7 and rank(v, v[4]) == 6)]
# hidden pruning constraints, each implied by the stated conditions (they only speed up the exhaustive search)
IMPLIED = [(("Gaurang",), lambda g: g == 58), (("Hima", "Gaurang"), lambda h, g: h == g + 4),
           (("Saumya", "Kuldeep"), lambda s_, k: s_ == k + 7)]
sols = solve(["Gaurang", "Hima", "Kuldeep", "Saumya", "Ritika", "Vipul"], {p: TT for p in P},
             IMPLIED + [(vs, fn) for _, vs, fn in conds], [P])
assert len(sols) == 1
O4 = sols[0]
assert O4 == {"Gaurang": 58, "Hima": 62, "Kuldeep": 60, "Ritika": 51, "Saumya": 67, "Vipul": 54}
gap = O4["Saumya"] - O4["Vipul"]
assert gap == 13
mcq(OTH, CMP, "Advanced",
    "Six runners Gaurang, Hima, Kuldeep, Ritika, Saumya and Vipul ran a race and finished at different times, "
    "measured in whole seconds (a smaller time means an earlier finish).\n" + bullets(conds) +
    "\n\nBy how many seconds did Saumya finish after the runner who came second?", f"{gap} seconds",
    ["9 seconds", "16 seconds", "7 seconds"], "Turn ranks and differences into times",
    "Ritika won in 51 s and Vipul took 54 s; since exactly two runners beat Gaurang (58 s), they are Ritika and Vipul, "
    "so Vipul came second. Hima took 62 s, so Kuldeep, from the average, took 2 × 61 − 62 = 60 s — he is the one "
    "runner between Gaurang and Hima. Saumya took 60 + 7 = 67 s and finished last. Saumya finished 67 − 54 = 13 s "
    "after Vipul.",
    ["Before Gaurang: Ritika (51), Vipul (54) ⇒ Vipul second", "Hima = 62; Kuldeep = 122 − 62 = 60",
     "Saumya = 67 (last)", "67 − 54 = 13 s"],
    why_others_wrong="9 seconds compares Saumya with Gaurang; 16 seconds compares her with the winner; 7 seconds "
                     "compares her with Kuldeep.", natural=lambda t: int(t.split()[0]), seconds=100,
    verified_by=BRUTE)

# ================================================================================================ SYLLOGISM
TWO, OAF, POS = "Two-statement", "Only a few / Only", "Possibility cases"


def N(*pairs):  # redefined: the seating sections reuse names freely
    return {s: (s, p) for s, p in pairs}


# ---- Basic
syl_q("Basic", TWO, N(("kiosk", "kiosks"), ("stall", "stalls"), ("booth", "booths")),
      [("all", "kiosk", "stall"), ("some", "stall", "booth")],
      [("some", "stall", "kiosk"), ("all", "booth", "stall")], ONLY_I, "'All A are B' gives 'Some B are A'",
      "Every kiosk is a stall, and kiosks exist, so some stalls are kiosks (I). 'Some stalls are booths' says nothing "
      "about booths that are not stalls, so II does not follow.",
      ["All kiosks are stalls ⇒ some stalls are kiosks: I", "Some stalls are booths ⇏ all booths are stalls: II fails"],
      why="Only II and Both read 'some' as 'all'; Neither misses the converse of an 'All' statement.", seconds=30)
syl_q("Basic", TWO, N(("harbour", "harbours"), ("dock", "docks"), ("pier", "piers")),
      [("no", "harbour", "dock"), ("all", "pier", "dock")],
      [("no", "pier", "harbour"), ("somenot", "dock", "harbour")], BOTH, "An 'All' inside a 'No'",
      "Every pier is a dock and no dock is a harbour, so no pier is a harbour (I). The piers are docks that are not "
      "harbours, so some docks are not harbours (II).",
      ["Piers ⊂ docks; docks ∩ harbours = ∅ ⇒ no pier is a harbour: I",
       "Piers are docks outside harbours ⇒ some docks are not harbours: II"],
      why="Each 'Only' option drops one of two definite conclusions.", seconds=35)
syl_q("Basic", POS, N(("comet", "comets"), ("meteor", "meteors"), ("planet", "planets")),
      [("some", "comet", "meteor"), ("no", "meteor", "planet")],
      [("poss_all", "comet", "planet"), ("poss_some", "planet", "comet")], ONLY_II,
      "A possibility fails only if it contradicts a statement",
      "Some comets are meteors, and no meteor is a planet, so at least those comets are not planets: 'all comets are "
      "planets' contradicts the statements (I fails). Comets that are not meteors may be planets, so II is possible.",
      ["Comet-meteors can never be planets ⇒ I impossible", "Other comets may be planets ⇒ II possible"],
      why="Only I and Both ignore the comets that are meteors; Neither treats an open overlap as ruled out.",
      seconds=35)

# ---- Intermediate
syl_q("Intermediate", OAF, N(("glacier", "glaciers"), ("valley", "valleys"), ("canyon", "canyons")),
      [("onlyfew", "glacier", "valley"), ("all", "valley", "canyon")],
      [("some", "canyon", "glacier"), ("poss_all", "glacier", "canyon")], BOTH,
      "'Only a few A are B' = some A are B and some A are not B",
      "Some glaciers are valleys and every valley is a canyon, so some canyons are glaciers (I). The glaciers that are "
      "not valleys may still be canyons, so all glaciers being canyons is possible (II).",
      ["Some glaciers are valleys ⊂ canyons ⇒ I", "Non-valley glaciers can lie inside canyons ⇒ II possible"],
      why="'Only a few' forbids all glaciers being valleys, not all glaciers being canyons, so II is not ruled out.",
      seconds=45)
syl_q("Intermediate", TWO, N(("sitar", "sitars"), ("tabla", "tablas"), ("veena", "veenas"),
                             ("harmonium", "harmoniums")),
      [("some", "sitar", "tabla"), ("all", "tabla", "veena"), ("no", "veena", "harmonium")],
      [("some", "sitar", "harmonium"), ("no", "sitar", "harmonium")], EITHER,
      "Complementary pair: 'Some A are B' and 'No A is B'",
      "The sitars that are tablas are veenas and so not harmoniums, but nothing is said about the other sitars. Neither "
      "conclusion is certain on its own; yet exactly one of 'Some sitars are harmoniums' and 'No sitar is a harmonium' "
      "must be true, so either I or II follows.",
      ["I uncertain; II uncertain", "Same subject and predicate, one 'some', one 'no' ⇒ complementary pair",
       "⇒ Either I or II follows"],
      why="Only I and Only II pick one side without support; Neither ignores that the pair covers every case.",
      seconds=50)
syl_q("Intermediate", OAF, N(("turbine", "turbines"), ("engine", "engines"), ("pump", "pumps")),
      [("only", "turbine", "engine"), ("some", "engine", "pump")],
      [("some", "pump", "turbine"), ("all", "turbine", "engine")], ONLY_I,
      "'Only A are B' means every B is an A",
      "'Only turbines are engines' means every engine is a turbine. Some engines are pumps, so those pumps are turbines: "
      "some pumps are turbines (I). It does not mean every turbine is an engine, so II does not follow.",
      ["Only turbines are engines ⇒ all engines are turbines", "Some engines are pumps ⇒ some pumps are turbines: I",
       "Turbines need not all be engines ⇒ II fails"],
      why="Only II and Both reverse the direction of 'Only'.", seconds=45)
syl_q("Intermediate", POS, N(("parrot", "parrots"), ("owl", "owls"), ("swan", "swans"), ("kestrel", "kestrels")),
      [("all", "parrot", "owl"), ("some", "owl", "swan"), ("no", "swan", "kestrel")],
      [("poss_some", "parrot", "swan"), ("poss_all", "owl", "kestrel")], ONLY_I,
      "Test each possibility against every statement",
      "Parrots are owls and some owls are swans; nothing stops some parrots from being among those swans, so I is "
      "possible. Some owls are swans, and no swan is a kestrel, so not every owl can be a kestrel: II is impossible.",
      ["Parrot–swan overlap not forbidden ⇒ I possible", "Owl-swans can never be kestrels ⇒ II impossible"],
      why="Only II and Both overlook the owls that are swans; Neither treats an allowed overlap as ruled out.",
      seconds=50)
syl_q("Intermediate", OAF, N(("sari", "saris"), ("shawl", "shawls"), ("turban", "turbans")),
      [("onlyfew", "sari", "shawl"), ("no", "shawl", "turban")],
      [("somenot", "sari", "turban"), ("poss_some", "turban", "sari")], BOTH,
      "'Only a few' gives a definite 'some'",
      "Some saris are shawls, and no shawl is a turban, so those saris are not turbans: some saris are not turbans (I). "
      "The saris that are not shawls may be turbans, so II is possible.",
      ["Sari-shawls are never turbans ⇒ I", "Non-shawl saris may be turbans ⇒ II possible"],
      why="Each 'Only' option drops one valid conclusion; Neither misses both.", seconds=45)

# ---- Advanced
syl_q("Advanced", TWO, N(("bridge", "bridges"), ("tunnel", "tunnels"), ("road", "roads"), ("lane", "lanes")),
      [("some", "bridge", "tunnel"), ("all", "tunnel", "road"), ("onlyfew", "road", "lane")],
      [("no", "bridge", "road"), ("some", "lane", "bridge")], NEITHER,
      "Separate what is false from what is merely uncertain",
      "Some bridges are tunnels and all tunnels are roads, so some bridges are roads: I ('No bridge is a road') is "
      "false. Only a few roads are lanes, but nothing connects those lanes with bridges, so II is uncertain. I and II "
      "have different subject–predicate pairs, so no 'either' case arises.",
      ["Some bridges are roads ⇒ I is false", "Lanes may or may not include bridges ⇒ II uncertain",
       "Different term pairs ⇒ not complementary ⇒ Neither"],
      why="Only I accepts a statement that contradicts the given ones; Only II and Both treat a possibility as certain.",
      seconds=60)
syl_q("Advanced", OAF, N(("diary", "diaries"), ("ledger", "ledgers"), ("register", "registers"),
                         ("planner", "planners")),
      [("only", "diary", "ledger"), ("onlyfew", "ledger", "register"), ("no", "register", "planner")],
      [("somenot", "diary", "planner"), ("poss_all", "ledger", "planner")], ONLY_I,
      "Chain 'Only' and 'Only a few' before testing a possibility",
      "Every ledger is a diary ('Only diaries are ledgers'). Some ledgers are registers, and no register is a planner, so "
      "those ledgers — which are diaries — are not planners: some diaries are not planners (I). The same ledger-"
      "registers can never be planners, so all ledgers being planners is impossible (II fails).",
      ["Only diaries are ledgers ⇒ ledgers ⊂ diaries", "Some ledgers are registers (not planners)",
       "⇒ some diaries are not planners: I", "Ledger-registers block 'all ledgers are planners' ⇒ II fails"],
      why="Only II and Both ignore the ledgers that are registers; Neither misses the chain that gives I.", seconds=60)

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
    # cross-check with a wider value range: the verdict must not change
    k = len({x for c in chains for r in parse_chain(c) for x in (r[0], r[2])})
    assert ineq_eval(chains, conclusions, dom=k + 2) == (f1, f2, either)
    text = (statement_text + "\n\nConclusions:\nI. " + concl_text[0] + "\nII. " + concl_text[1])
    return fixed(INQ, sub, diff, text, [IO4[x] for x in conclusion_options(expected)], IO4[expected], concept,
                 explanation, steps, shortcut=shortcut, why_others_wrong=why, seconds=seconds, verified_by=EXHAUST,
                 stimulus=stimulus)


def chain_text(chain, conc):
    return "Statement: " + chain, [chain], [parse_chain(c)[0] for c in conc], conc


def models_of(chains, extra=()):
    rels = [r for c in chains for r in parse_chain(c)] + list(extra)
    vs = sorted({x for a_, _, b_ in rels for x in (a_, b_)})
    out = solve(vs, {x: range(len(vs)) for x in vs}, [((a_, b_), (lambda x, y, o=o: REL[o](x, y))) for a_, o, b_ in rels])
    assert out
    return out


def status(chains, rel, extra=()):
    """'T' if rel holds in every model of the chains, 'F' if in none, 'U' otherwise."""
    a_, o, b_ = rel
    hits = [REL[o](v[a_], v[b_]) for v in models_of(chains, extra)]
    return "T" if all(hits) else "F" if not any(hits) else "U"


# ---- Basic: single chains
B_ITEMS = [
    ("A > B ≥ C = D < E ≤ F", ["A > D", "F > C"], BOTH,
     "A > B ≥ C = D gives A > D (I). F ≥ E > D = C gives F > C (II).",
     ["I: A > B ≥ C = D ⇒ A > D, true", "II: F ≥ E > D = C ⇒ F > C, true"]),
    ("M ≤ N < O = P ≥ Q > R", ["M < P", "N > Q"], ONLY_I,
     "M ≤ N < O = P gives M < P (I). N and Q lie on opposite sides of the turn at O = P (N < O = P ≥ Q), so N > Q is "
     "not certain (II).", ["I: M ≤ N < O = P ⇒ M < P, true", "II: N < … ≥ Q: reversal ⇒ no relation"]),
    ("G < H ≤ J = K > L ≥ M", ["G < L", "M < J"], ONLY_II,
     "G and L lie on opposite sides of the turn at J = K, so G < L is not certain (I). M ≤ L < K = J gives M < J (II).",
     ["I: G < … K > L: reversal ⇒ no relation", "II: M ≤ L < K = J ⇒ M < J, true"]),
    ("P ≥ Q > R < S = T ≤ U", ["P > S", "U > Q"], NEITHER,
     "Both conclusions compare a term on the left of R with a term on its right. The chain turns at R (Q > R < S), so "
     "neither relation is certain.", ["I: P … R < S: reversal at R", "II: U … R < … Q: reversal at R"]),
    ("C ≤ D = E ≥ F > G", ["C < E", "C = E"], EITHER,
     "C ≤ D = E gives only C ≤ E. Each of C < E and C = E is uncertain on its own, but one of them must hold: either "
     "I or II is true.", ["C ≤ D = E ⇒ C ≤ E", "C < E or C = E ⇒ Either"]),
    ("B < C ≤ D > E = F ≥ G", ["B ≥ D", "G < D"], ONLY_II,
     "B < C ≤ D gives B < D, so B ≥ D is false (I). G ≤ F = E < D gives G < D (II).",
     ["I: B < D ⇒ B ≥ D false", "II: G ≤ F = E < D ⇒ G < D, true"]),
    ("H > I ≥ J ≤ K < L = M", ["H > J", "M > J"], BOTH,
     "H > I ≥ J gives H > J (I). M = L > K ≥ J gives M > J (II).",
     ["I: H > I ≥ J ⇒ H > J, true", "II: M = L > K ≥ J ⇒ M > J, true"]),
]
B_LEADS = ["Six quantities in a warehouse ledger satisfy the relation {c}. Taking it as true, test the two conclusions.",
           "A teacher writes the chain {c} on the board and asks which conclusions are definitely true.",
           "Given: {c}. Every sign in this relation holds.",
           "The following comparison of six values is known to be correct: {c}.",
           "Five values are linked as {c}. Decide which of the conclusions must hold.",
           "Accept the relation {c} as true and check each conclusion against it.",
           "Statement (one continuous chain): {c}"]
for n_b, (chain, conc, exp, expl, steps) in enumerate(B_ITEMS):
    s, ch, cc, ct = chain_text(chain, conc)
    s = B_LEADS[n_b].format(c=chain)
    ineq_q("Basic", DIRECT, s, ch, cc, ct, exp, expl, steps,
           why="'Either' replaces 'Both' when the two conclusions split one '≤'/'≥' sign." if exp == EITHER else
           "A relation holds only if every sign from one term to the other points the same way; one strict sign "
           "makes it strict.", seconds=30)

# ---- Intermediate: direct, several statements
I_ITEMS = [
    (["R ≥ S", "S > T", "U ≤ T", "U = V", "W > R"], ["W > U", "V < S"], BOTH,
     "Combined: W > R ≥ S > T ≥ U = V. W > U (I) and V < S (II) both follow along one direction.",
     ["Chain: W > R ≥ S > T ≥ U = V", "I: W > U, true", "II: V = U ≤ T < S ⇒ V < S, true"]),
    (["A < B", "B ≥ C", "D > C", "D ≤ E", "F = E"], ["A < E", "F > C"], ONLY_II,
     "Combined: A < B ≥ C < D ≤ E = F. A and E lie on opposite sides of the turn at B and C, so A < E is not certain. "
     "F = E ≥ D > C gives F > C.", ["Chain: A < B ≥ C < D ≤ E = F", "I: crosses the turns ⇒ not certain",
                                    "II: F = E ≥ D > C ⇒ F > C, true"]),
    (["K ≤ L", "L = M", "M > N", "O ≥ N", "O < P"], ["K > N", "P > M"], NEITHER,
     "Combined: K ≤ L = M > N ≤ O < P. K and N, and P and M, are compared across the turn at N (M > N ≤ O), so "
     "neither conclusion is certain.", ["Chain: K ≤ L = M > N ≤ O < P", "I: K … M > N: reversal",
                                       "II: P > O ≥ N < M: reversal"]),
    (["X ≥ Y", "Y = Z", "Z ≥ Q", "Q > R"], ["X > Q", "X = Q"], EITHER,
     "Combined: X ≥ Y = Z ≥ Q > R. Only X ≥ Q is known, so each of X > Q and X = Q is uncertain, but one must hold.",
     ["Chain: X ≥ Y = Z ≥ Q > R", "X ≥ Q ⇒ X > Q or X = Q", "Either I or II"]),
    (["D > E", "E ≥ F", "G < F", "G ≥ H", "J = H"], ["D > J", "G > J"], ONLY_I,
     "Combined: D > E ≥ F > G ≥ H = J. D > J follows (I). G ≥ H = J gives only G ≥ J, so G > J is not certain (II).",
     ["Chain: D > E ≥ F > G ≥ H = J", "I: D > J, true", "II: G ≥ J only ⇒ G > J not certain"]),
]
I_LEADS = ["Five separate statements are given: {c}. Combine them and test the conclusions.",
           "Statements (all true): {c}",
           "The following relations hold among six quantities: {c}. Which conclusions are definitely true?",
           "Treat these four statements as facts: {c}.",
           "From the data {c}, decide which of the two conclusions follow."]
for n_i, (chains, conc, exp, expl, steps) in enumerate(I_ITEMS):
    s = I_LEADS[n_i].format(c="; ".join(chains))
    ineq_q("Intermediate", DIRECT, s, chains, [parse_chain(c)[0] for c in conc], conc, exp, expl, steps,
           why="'Either' replaces 'Both' (four-option rule)." if exp == EITHER else
           "Join the statements into one chain first; a turn in direction between two terms leaves them unrelated.",
           seconds=50)

# ---- Intermediate: coded set with word codes
CODE_W = {"zu": ">", "mi": "<", "ro": "=", "te": "≥", "fa": "≤"}
CODE_W_TXT = ("In the questions of this set, the words zu, mi, ro, te and fa are used between two letters with these "
              "meanings:\n'A zu B' means 'A is neither smaller than nor equal to B'; 'A mi B' means 'A is neither "
              "greater than nor equal to B'; 'A ro B' means 'A is neither greater than nor smaller than B'; 'A te B' "
              "means 'A is not smaller than B'; 'A fa B' means 'A is not greater than B'.\nAssuming the statements to "
              "be true, find which of the conclusions I and II is/are definitely true.")
SID_W = stimulus("passage", "Five two-letter code words for comparisons", CODE_W_TXT, None,
                 "Decode: zu means >, mi means <, ro means =, te means ≥ and fa means ≤ ('not smaller than' allows "
                 "greater or equal; 'not greater than' allows smaller or equal). Rewrite each statement with ordinary "
                 "signs, join them into one chain, and test each conclusion along the chain.")
CCW = "Decoding word codes, then reading the chain"


def coded_w(stmts, concs):
    return ("Statements: " + ", ".join(stmts), [decode(x, CODE_W) for x in stmts],
            [parse_chain(decode(c, CODE_W))[0] for c in concs], concs)


W_ITEMS = [
    (["P te Q", "Q zu R", "R ro S", "T fa S"], ["P zu S", "T mi Q"], BOTH,
     "Decoded: P ≥ Q > R = S ≥ T. P > S (I) and T < Q (II) both hold.",
     ["Decode: P ≥ Q, Q > R, R = S, T ≤ S", "Chain: P ≥ Q > R = S ≥ T", "I: P > S, true", "II: T < Q, true"]),
    (["A mi B", "B fa C", "C zu D", "E te D"], ["A mi C", "E zu B"], ONLY_I,
     "Decoded: A < B ≤ C > D ≤ E. A < C (I). E and B lie across the turn at C and D, so E > B is not certain (II).",
     ["Decode: A < B, B ≤ C, C > D, E ≥ D", "Chain: A < B ≤ C > D ≤ E", "I: A < C, true", "II: reversal ⇒ not "
                                                                                        "certain"]),
    (["G ro H", "H te J", "J mi K", "L zu K"], ["G mi K", "L zu J"], ONLY_II,
     "Decoded: G = H ≥ J < K < L. G and K lie on opposite sides of the turn at J, so G < K is not certain (I). "
     "L > K > J gives L > J (II).", ["Decode: G = H, H ≥ J, J < K, L > K", "Chain: G = H ≥ J < K < L",
                                     "I: reversal at J", "II: L > K > J ⇒ L > J, true"]),
    (["M fa N", "N zu O", "O te P", "P ro Q"], ["M te O", "Q zu M"], NEITHER,
     "Decoded: M ≤ N > O ≥ P = Q. Both conclusions compare M with a term on the other side of the turn at N, so "
     "neither is certain.", ["Decode: M ≤ N, N > O, O ≥ P, P = Q", "Chain: M ≤ N > O ≥ P = Q",
                             "I and II: reversal at N ⇒ not certain"]),
    (["R te S", "S ro T", "T te U", "V mi U"], ["R zu U", "R ro U"], EITHER,
     "Decoded: R ≥ S = T ≥ U > V. Only R ≥ U is known, so R > U and R = U are each uncertain, but one must hold.",
     ["Decode: R ≥ S, S = T, T ≥ U, V < U", "R ≥ U ⇒ R > U or R = U", "Either I or II"]),
    (["W zu X", "X fa Y", "Y ro Z", "Z mi E"], ["E zu X", "W zu Y"], ONLY_I,
     "Decoded: W > X ≤ Y = Z < E. E > Z = Y ≥ X gives E > X (I). W and Y lie on opposite sides of the turn at X, so "
     "W > Y is not certain (II).", ["Decode: W > X, X ≤ Y, Y = Z, Z < E", "Chain: W > X ≤ Y = Z < E",
                                    "I: E > X, true", "II: reversal at X"]),
]
for stmts, concs, exp, expl, steps in W_ITEMS:
    s, ch, cc, ct = coded_w(stmts, concs)
    ineq_q("Intermediate", CODED, s, ch, cc, ct, exp, expl, steps, concept=CCW, stimulus=SID_W, seconds=55,
           why="'Either' replaces 'Both' (four-option rule)." if exp == EITHER else
           "Decode first; 'not smaller than' is ≥, not >.")

# ---- Advanced
# A1: seven statements, two conclusions
s = "Statement: Q ≥ W; W = E; E > R; T ≤ R; T > Y; U ≥ Q; I < Y"
ch = ["Q ≥ W", "W = E", "E > R", "T ≤ R", "T > Y", "U ≥ Q", "I < Y"]
ineq_q("Advanced", DIRECT, s, ch, [("U", ">", "I"), ("Q", ">", "R")], ["U > I", "Q > R"], BOTH,
       "Combined: U ≥ Q ≥ W = E > R ≥ T > Y > I. U > I (I) and Q > R (II) both lie along one direction with a strict "
       "sign on each path.", ["Chain: U ≥ Q ≥ W = E > R ≥ T > Y > I", "I: U > I, true", "II: Q ≥ W = E > R ⇒ Q > R, "
                                                                                       "true"],
       why="Neither 'Only' option survives: both paths contain a strict '>'.", seconds=75,
       concept="Combining seven statements into one chain")
# A2: how many of four conclusions are definitely true
CH = ["B ≥ N", "N > M", "M = K", "K ≤ J", "J < H", "B < L"]
CON = [("L", ">", "M"), ("H", ">", "M"), ("B", ">", "K"), ("J", "≥", "N")]
st = [status(CH, c) for c in CON]
assert st == ["T", "T", "T", "U"]
cnt = st.count("T")
mcq(INQ, DIRECT, "Advanced",
    "Statement: B ≥ N; N > M; M = K; K ≤ J; J < H; B < L\n\nConclusions:\nI. L > M\nII. H > M\nIII. B > K\nIV. J ≥ N"
    "\n\nHow many of the conclusions I, II, III and IV are definitely true?", num_word(cnt), ["Two", "Four", "One"],
    "Test each conclusion along the joined chain",
    "Combined: L > B ≥ N > M = K ≤ J < H. L > M (I) and B > K (III) follow along the left part; H > J ≥ K = M gives "
    "H > M (II). J and N lie on opposite sides of the turn at M = K, so J ≥ N is not certain (IV). Three conclusions "
    "are definitely true.",
    ["Chain: L > B ≥ N > M = K ≤ J < H", "I: L > M ✓; III: B > K ✓", "II: H > J ≥ K = M ⇒ H > M ✓",
     "IV: N > M = K ≤ J ⇒ J vs N unknown ✗", "Count = 3"],
    why_others_wrong="Four accepts IV, which crosses the turn at M = K; Two and One miss II or III.", natural=by_num,
    seconds=90, verified_by=EXHAUST)
# A3: which conclusion is definitely false
CH = ["P < Q ≤ R", "R = S", "S ≥ T > U"]
OPTS = [("U", "≥", "R"), ("P", "≥", "U"), ("T", "<", "Q"), ("Q", ">", "U")]
st = [status(CH, c) for c in OPTS]
assert st == ["F", "U", "U", "U"]
mcq(INQ, DIRECT, "Advanced",
    "Statement: P < Q ≤ R; R = S; S ≥ T > U\n\nWhich of the following is definitely FALSE?", " ".join(OPTS[0]),
    [" ".join(c) for c in OPTS[1:]], "Definitely false = contradicted by every case the chain allows",
    "Combined: P < Q ≤ R = S ≥ T > U. Reading from R down to U: R = S ≥ T > U, so R > U always, and 'U ≥ R' can never "
    "be true. P ≥ U, T < Q and Q > U all compare terms across the turn at R = S, so each may be true or false.",
    ["Chain: P < Q ≤ R = S ≥ T > U", "R = S ≥ T > U ⇒ R > U always ⇒ U ≥ R definitely false",
     "P vs U, T vs Q, Q vs U: across the turn ⇒ undetermined"],
    why_others_wrong="Each of the other three relations crosses the turn at R = S, so it is possible but not certain "
                     "— and therefore not definitely false.", seconds=80, verified_by=EXHAUST)
# A4: fill two blanks so that both conclusions are definitely true
EXPR = "G _ H ≥ J _ K = L"
CANDS = [(">", "≥"), ("≥", "<"), ("=", ">"), ("<", "≥")]
NEED = [("G", ">", "J"), ("L", "≤", "J")]
ok = []
for a_, b_ in CANDS:
    chain = f"G {a_} H ≥ J {b_} K = L"
    ok.append(all(status([chain], n_) == "T" for n_ in NEED))
assert ok == [True, False, False, False]
mcq(INQ, DIRECT, "Advanced",
    f"Which pair of signs, filled in order in the blanks of the expression '{EXPR}', makes both 'G > J' and "
    "'L ≤ J' definitely true?", "> and ≥", ["≥ and <", "= and >", "< and ≥"],
    "Fill the blanks, then test both conclusions",
    "G > J needs every sign from G to J to point the same way with at least one strict sign: the first blank must be "
    "'>' (with '≥' after H). L ≤ J needs J ≥ K = L, so the second blank must be '≥', '>' or '='. Only '> and ≥' meets "
    "both: G > H ≥ J ≥ K = L. With '≥ and <', G ≥ J only and J < L; with '= and >', G ≥ J only; with '< and ≥', G and J "
    "are unrelated.",
    ["G > J ⇒ first blank '>'", "L ≤ J ⇒ second blank '≥', '>' or '='", "Only option: > and ≥"],
    why_others_wrong="'≥ and <' and '= and >' leave G ≥ J without a strict sign; '< and ≥' reverses the direction "
                     "between G and H.", seconds=80, verified_by=EXHAUST)
# A5: three conclusions
CH = ["V > W ≥ X", "X = Y", "Y < Z ≤ A"]
CON = [("V", ">", "Y"), ("A", ">", "X"), ("W", "≥", "Z")]
st = [status(CH, c) for c in CON]
assert st == ["T", "T", "U"]
OPT3 = ["Only I and II are true", "Only I and III are true", "Only II and III are true", "All I, II and III are true"]
fixed(INQ, DIRECT, "Advanced", "Statement: V > W ≥ X; X = Y; Y < Z ≤ A\n\nConclusions:\nI. V > Y\nII. A > X\nIII. W ≥ Z",
      OPT3, OPT3[0], "Three conclusions: test each along the chain",
      "Combined: V > W ≥ X = Y < Z ≤ A. V > Y (I) and A ≥ Z > Y = X, i.e. A > X (II), follow. W and Z lie on opposite "
      "sides of the turn at X = Y, so W ≥ Z is not certain (III).",
      ["Chain: V > W ≥ X = Y < Z ≤ A", "I: V > Y ✓", "II: A ≥ Z > Y = X ⇒ A > X ✓", "III: across the turn ✗"],
      why_others_wrong="Every other option includes III, which compares W and Z across the turn at X = Y.", seconds=80,
      verified_by=EXHAUST)
# A6: which added statement makes a conclusion definitely true
CH = ["C ≥ D", "D > E", "F ≤ E"]
TARGET = ("G", ">", "F")
ADD = [("G", "≥", "D"), ("G", "=", "F"), ("G", ">", "C"), ("G", "<", "E")]
st = [status(CH, TARGET, extra=[a_]) for a_ in ADD]
assert st == ["T", "F", "T", "U"]
# 'G > C' also works, so keep only one working option among the four shown
ADD = [("G", "≥", "D"), ("G", "=", "F"), ("G", "≤", "C"), ("G", "<", "E")]
st = [status(CH, TARGET, extra=[a_]) for a_ in ADD]
assert st == ["T", "F", "U", "U"]
mcq(INQ, DIRECT, "Advanced",
    "Statement: C ≥ D; D > E; F ≤ E\n\nWhich of the following statements, if added to the given statements, makes "
    "'G > F' definitely true?", " ".join(ADD[0]), [" ".join(a_) for a_ in ADD[1:]],
    "The added link must join G to the chain on the correct side",
    "Combined: C ≥ D > E ≥ F. Adding G ≥ D gives G ≥ D > E ≥ F, so G > F. G = F makes G > F false; G ≤ C and G < E "
    "place G above or below a term without fixing its position relative to F.",
    ["Chain: C ≥ D > E ≥ F", "G ≥ D ⇒ G ≥ D > E ≥ F ⇒ G > F ✓", "G = F ⇒ G > F false",
     "G ≤ C, G < E ⇒ G could be below or above F"],
    why_others_wrong="G = F contradicts the conclusion; with G ≤ C or G < E, G may still be less than F.", seconds=80,
    verified_by=EXHAUST)
# A7: coded (word codes reused as a standalone with its own key)
s = ("Here 'A zu B' means 'A is neither smaller than nor equal to B', 'A mi B' means 'A is neither greater than nor "
     "equal to B', 'A ro B' means 'A is neither greater than nor smaller than B', 'A te B' means 'A is not smaller "
     "than B' and 'A fa B' means 'A is not greater than B'.\n\nStatements: H te K, K ro N, N zu Q, R fa Q, R zu S, "
     "T te H")
ch = [decode(x, CODE_W) for x in ["H te K", "K ro N", "N zu Q", "R fa Q", "R zu S", "T te H"]]
ineq_q("Advanced", CODED, s, ch, [("T", ">", "R"), ("S", "<", "K")], ["T zu R", "S mi K"], BOTH,
       "Decoded: T ≥ H ≥ K = N > Q ≥ R > S. T > R (I) and S < K (II) both follow along one direction.",
       ["Decode: H ≥ K, K = N, N > Q, R ≤ Q, R > S, T ≥ H", "Chain: T ≥ H ≥ K = N > Q ≥ R > S", "I: T > R ✓",
        "II: S < R ≤ Q < N = K ⇒ S < K ✓"], concept=CCW, seconds=80,
       why="Each 'Only' option drops one conclusion that follows along the chain.")
# A8: Either at the end of a long chain
s = "Statement: A ≤ B; B = C; C ≤ D; E > D; F < A; G ≥ E"
ch = ["A ≤ B", "B = C", "C ≤ D", "E > D", "F < A", "G ≥ E"]
ineq_q("Advanced", DIRECT, s, ch, [("D", ">", "A"), ("D", "=", "A")], ["D > A", "D = A"], EITHER,
       "Combined: F < A ≤ B = C ≤ D < E ≤ G. Only D ≥ A is known, so D > A and D = A are each uncertain, but exactly "
       "one of them must be true.", ["Chain: F < A ≤ B = C ≤ D < E ≤ G", "A ≤ D ⇒ D > A or D = A", "Either I or II"],
       why="'Either' replaces 'Both' (four-option rule); neither 'Only' option is certain.", seconds=75,
       concept="Complementary pair along a weak chain")
# A9: coded, neither
s = ("Here 'A zu B' means 'A is neither smaller than nor equal to B', 'A mi B' means 'A is neither greater than nor "
     "equal to B', 'A ro B' means 'A is neither greater than nor smaller than B', 'A te B' means 'A is not smaller "
     "than B' and 'A fa B' means 'A is not greater than B'.\n\nStatements: J mi K, K te L, L ro M, M mi N, O fa N, "
     "O zu P")
ch = [decode(x, CODE_W) for x in ["J mi K", "K te L", "L ro M", "M mi N", "O fa N", "O zu P"]]
ineq_q("Advanced", CODED, s, ch, [("J", "<", "N"), ("P", "<", "L")], ["J mi N", "P mi L"], NEITHER,
       "Decoded: J < K ≥ L = M < N ≥ O > P. J and N lie across the turn at K (J < K ≥ L), and P and L lie across the "
       "turn at N (M < N ≥ O), so neither conclusion is certain.",
       ["Decode: J < K, K ≥ L, L = M, M < N, O ≤ N, O > P", "Chain: J < K ≥ L = M < N ≥ O > P",
        "I: reversal at K", "II: reversal at N"], concept=CCW, seconds=80,
       why="Both conclusions cross a turn in the chain.")

# ================================================================================================ BLOOD RELATIONS
DRB, CDB, FPZ = "Direct relation", "Coded blood relation", "Family puzzle"

# ---- Basic
F = Family().add("GF", "M").add("GM", "F").marry("GF", "GM").add("Kf", "M", "GF", "GM")
F.add("Km", "F").marry("Kf", "Km").add("Karan", "M", "Kf", "Km").add("Girl", "F", "Kf", "Km")
assert [c for c in F.children("GM") if F.g[c] == "M"] == ["Kf"]  # the only son of Karan's father's mother
ans = F.rel("Girl", "Karan")
assert ans == "sister"
mcq(BLD, DRB, "Basic",
    "Pointing to a girl, Karan said, \"She is the daughter of the only son of my father's mother.\" How is the girl "
    "related to Karan?", cap(ans), ["Cousin", "Niece", "Aunt"], "Collapse the phrase from the inside out",
    "Karan's father's mother is his paternal grandmother. Her only son must be Karan's father. The girl is the "
    "daughter of Karan's father, so she is Karan's sister.",
    ["Father's mother = paternal grandmother", "Her only son = Karan's father", "Daughter of Karan's father ⇒ sister"],
    why_others_wrong="A cousin would be the child of the father's sibling, but the grandmother has no other son; niece "
                     "and aunt put the girl in the wrong generation.", seconds=30, verified_by=RECOMP)
F = Family().add("Zh", "M").add("Z", "F").marry("Zh", "Z").add("X", "M", "Zh", "Z").add("W", "F", "Zh", "Z")
F.add("Xw", "F").marry("X", "Xw").add("Y", "M", "X", "Xw")
F.check([("X", "father", "Y"), ("Z", "mother", "X")])
ans = F.rel("W", "Y")
assert ans == "aunt"
mcq(BLD, DRB, "Basic",
    "X is the father of Y. Z is the mother of X. W is the only daughter of Z. How is W related to Y?", cap(ans),
    ["Mother", "Sister", "Grandmother"], "Father's sister = aunt",
    "Z is X's mother, and W is Z's daughter, so W is X's sister. X is Y's father, so W is Y's father's sister: Y's aunt.",
    ["Z = mother of X; W = daughter of Z ⇒ W is X's sister", "X = father of Y ⇒ W = Y's paternal aunt"],
    why_others_wrong="Y's mother is X's wife, not his sister; W is a generation above Y, so not a sister; Z, not W, is "
                     "Y's grandmother.", seconds=30, verified_by=RECOMP)

# ---- Intermediate coded set
CODE_B = {"lo": "mother", "pa": "brother", "ki": "husband", "su": "daughter", "ne": "sister"}
CODE_B_TXT = ("In a certain code language:\n'A lo B' means 'A is the mother of B';\n'A pa B' means 'A is the brother "
              "of B';\n'A ki B' means 'A is the husband of B';\n'A su B' means 'A is the daughter of B';\n'A ne B' "
              "means 'A is the sister of B'.\nIn every expression, a married couple's children are the children of "
              "both spouses.")
sid = stimulus("passage", "Two-letter code words for relations", CODE_B_TXT, None,
               "Decode each expression pair by pair from left to right, draw the small family tree it describes, and "
               "then read the asked relation off the tree. Genders come from the words used: mother, daughter and "
               "sister are female; brother and husband are male.")
BQ = lambda sub, text, correct, wrongs, concept, expl, steps, **kw: mcq(
    BLD, sub, "Intermediate", text, correct, wrongs, concept, expl, steps, stimulus=sid, verified_by=RECOMP, **kw)
# Q1: M ki N lo O pa P
F = Family().add("M", "M").add("N", "F").marry("M", "N").add("O", "M", "M", "N").add("P", "F", "M", "N")
F.check(coded_facts("M ki N", CODE_B) + coded_facts("N lo O", CODE_B) + coded_facts("O pa P", CODE_B))
F2_ = Family().add("M", "M").add("N", "F").marry("M", "N").add("O", "M", "M", "N").add("P", "M", "M", "N")
assert F.rel("M", "P") == F2_.rel("M", "P") == "father"  # P's gender is not given; the answer does not depend on it
BQ(CDB, "If 'M ki N lo O pa P', how is M related to P?", "Father", ["Brother", "Husband", "Uncle"],
   "Decode pair by pair", "M is N's husband; N is O's mother; O is P's brother, so O and P are children of N — and of "
                          "her husband M. M is P's father.",
   ["M ki N: M is N's husband", "N lo O and O pa P: O and P are N's children", "Children of the couple ⇒ M is the "
                                                                                "father of P"],
   why_others_wrong="Brother is O's relation to P; Husband is M's relation to N; Uncle would need M to be a sibling of "
                    "P's parent.", seconds=50)
# Q2: A su B ne C ki D
F = Family().add("Bp", "M").add("Bm", "F").marry("Bp", "Bm").add("B", "F", "Bp", "Bm").add("C", "M", "Bp", "Bm")
F.add("D", "F").marry("C", "D").add("Bh", "M").marry("B", "Bh").add("A", "F", "Bh", "B")
F.check(coded_facts("A su B", CODE_B) + coded_facts("B ne C", CODE_B) + coded_facts("C ki D", CODE_B))
ans = F.rel("D", "A")
assert ans == "aunt"
BQ(CDB, "If 'A su B ne C ki D', how is D related to A?", "Aunt", ["Mother", "Sister-in-law", "Cousin"],
   "A parent's brother's wife is an aunt",
   "A is B's daughter; B is C's sister; C is D's husband. So C is A's maternal uncle, and D, his wife, is A's aunt.",
   ["A su B: A is B's daughter", "B ne C: C is B's brother ⇒ A's uncle", "C ki D: D is C's wife ⇒ A's aunt"],
   why_others_wrong="B, not D, is A's mother; D is B's sister-in-law, not A's; a cousin is in A's own generation.",
   seconds=55)
# Q3: which expression means J is the grandmother of K
EXPRS = ["J lo L ki M lo K", "J su L lo K", "J ne L lo K", "J lo L pa K"]
F = Family().add("Jh", "M").add("J", "F").marry("Jh", "J").add("L", "M", "Jh", "J").add("M", "F").marry("L", "M")
F.add("K", "M", "L", "M")
F.check(coded_facts("J lo L", CODE_B) + coded_facts("L ki M", CODE_B) + coded_facts("M lo K", CODE_B))
assert F.rel("J", "K") == "grandmother"
G1 = Family().add("L", "F").add("J", "F", None, "L").add("K", "M", None, "L")  # J su L lo K
G2 = Family().add("P0", "F").add("J", "F", None, "P0").add("L", "F", None, "P0").add("K", "M", None, "L")  # J ne L lo K
G3 = Family().add("J", "F").add("L", "M", None, "J").add("K", "M", None, "J")  # J lo L pa K
assert (G1.rel("J", "K"), G2.rel("J", "K"), G3.rel("J", "K")) == ("sister", "aunt", "mother")
BQ(CDB, "Which of the following expressions means that J is the grandmother of K?", EXPRS[0], EXPRS[1:],
   "Test each option: two generations must separate J and K",
   "In 'J lo L ki M lo K', J is L's mother, L is M's husband and M is K's mother; so L is K's father and J, L's "
   "mother, is K's grandmother. In the other options J is K's sister ('J su L lo K'), aunt ('J ne L lo K') or mother "
   "('J lo L pa K').",
   ["J lo L ki M lo K: J → L (son) → K (L is K's father) ⇒ grandmother ✓", "J su L lo K ⇒ J is K's sister",
    "J ne L lo K ⇒ J is K's aunt", "J lo L pa K ⇒ J is K's mother"],
   why_others_wrong="Each of the other expressions puts J zero or one generation above K.", seconds=70)
# Q4: E pa F su G ki H
F = Family().add("G", "M").add("H", "F").marry("G", "H").add("E", "M", "G", "H").add("F", "F", "G", "H")
F.check(coded_facts("E pa F", CODE_B) + coded_facts("F su G", CODE_B) + coded_facts("G ki H", CODE_B))
ans = F.rel("H", "E")
assert ans == "mother"
BQ(CDB, "If 'E pa F su G ki H', how is H related to E?", "Mother", ["Sister", "Wife", "Grandmother"],
   "The husband's wife is the children's mother",
   "E is F's brother; F is G's daughter, so E is G's son; G is H's husband, so H is E's mother.",
   ["E pa F, F su G ⇒ E and F are G's children", "G ki H ⇒ H is G's wife", "⇒ H is E's mother"],
   why_others_wrong="F, not H, is E's sister; H is G's wife, not E's; grandmother is one generation too high.",
   seconds=50)

# ---- Intermediate standalone
F = Family().add("Rohan", "M").add("Shanta", "F").marry("Rohan", "Shanta")
F.add("Tushar", "M", "Rohan", "Shanta").add("Pari", "F", "Rohan", "Shanta")
F.add("Uma", "F").marry("Tushar", "Uma").add("Om", "M", "Tushar", "Uma")
F.check([("Shanta", "mother", "Tushar"), ("Shanta", "mother-in-law", "Uma"), ("Tushar", "father", "Om"),
         ("Pari", "sister", "Tushar")])
ans = F.rel("Pari", "Uma")
assert ans == "sister-in-law"
mcq(BLD, FPZ, "Intermediate",
    "A family has six members: Om, Pari, Rohan, Shanta, Tushar and Uma, with two married couples.\n- Shanta is the "
    "mother of Tushar and the mother-in-law of Uma.\n- Om is the only grandchild of Shanta, and Om's father is "
    "Tushar.\n- Pari is the only sister of Tushar.\n- Rohan is married to Shanta.\n\nHow is Pari related to Uma?",
    cap(ans), ["Sister", "Mother-in-law", "Daughter"], "Husband's sister = sister-in-law",
    "Shanta is Uma's mother-in-law and Tushar's mother; the two couples are Rohan–Shanta and Tushar–Uma, so Uma is "
    "Tushar's wife. Pari is Tushar's sister, i.e. Uma's husband's sister: her sister-in-law.",
    ["Couples: Rohan–Shanta, Tushar–Uma", "Pari = Tushar's sister", "Husband's sister ⇒ sister-in-law"],
    why_others_wrong="Pari shares no parent with Uma; Shanta, not Pari, is Uma's mother-in-law; Pari is in Uma's "
                     "generation, not the next.", seconds=55, verified_by=RECOMP)
F = Family().add("Gf", "M").add("Gm", "F").marry("Gf", "Gm").add("Man", "M", "Gf", "Gm")
F.add("Nm", "F", "Gf", "Gm").add("Nf", "M").marry("Nf", "Nm").add("Nandini", "F", "Nf", "Nm")
assert [c for c in F.children("Gm") if F.g[c] == "F"] == ["Nm"]
ans = F.rel("Man", "Nandini")
assert ans == "uncle"
mcq(BLD, DRB, "Intermediate",
    "Pointing to a man, Nandini said, \"His mother's only daughter is my mother.\" How is the man related to Nandini?",
    "Maternal uncle", ["Father", "Brother", "Paternal uncle"], "Identify the shared parent first",
    "The man's mother's only daughter is the man's sister (his mother has no other daughter). That sister is Nandini's "
    "mother, so the man is her mother's brother: her maternal uncle.",
    ["His mother's only daughter = his sister", "His sister = Nandini's mother", "Mother's brother ⇒ maternal uncle"],
    why_others_wrong="Nandini's father is her mother's husband, not her brother; the man is a generation above "
                     "Nandini; a paternal uncle is the father's brother.", seconds=40, verified_by=RECOMP)
F = Family().add("Lh", "M").add("Leela", "F").marry("Lh", "Leela").add("Ritu", "F", "Lh", "Leela")
F.add("Vikram", "M").marry("Vikram", "Ritu").add("Aarav", "M", "Vikram", "Ritu").add("Bina", "F").marry("Aarav", "Bina")
F.check([("Vikram", "son-in-law", "Leela"), ("Aarav", "son", "Ritu")])
ans = F.rel("Bina", "Vikram")
assert ans == "daughter-in-law"
mcq(BLD, FPZ, "Intermediate",
    "Vikram is the son-in-law of Leela, who has only one child, Ritu. Vikram and Ritu have only one child, Aarav, and "
    "Bina is Aarav's wife. How is Bina related to Vikram?", cap(ans), ["Daughter", "Sister-in-law", "Granddaughter"],
    "Son-in-law of a mother of one = husband of that child",
    "Leela has only one child, Ritu, so her son-in-law Vikram is Ritu's husband. Aarav is their son, and Bina, Aarav's "
    "wife, is the wife of Vikram's son: his daughter-in-law.",
    ["Leela's only child Ritu ⇒ Vikram is Ritu's husband", "Aarav = son of Vikram and Ritu",
     "Wife of one's son ⇒ daughter-in-law"],
    why_others_wrong="Bina is married into the family, so she is not Vikram's daughter; sister-in-law would put her in "
                     "Vikram's generation; granddaughter puts her two generations below.", seconds=50,
    verified_by=RECOMP)

# ---- Advanced: coded, with one gender left open
CODE_A = {"$": "son", "%": "wife", "@": "sister", "#": "father", "&": "mother"}
F_variants = []
for og in ("M", "F"):
    F = Family().add("Kh", "M").add("K", "F").marry("Kh", "K").add("L", "F", "Kh", "K").add("M", "F", "Kh", "K")
    F.add("O", og).add("Osp", "F" if og == "M" else "M")
    if og == "M":
        F.marry("O", "Osp").add("N", "M", "O", "Osp")
    else:
        F.marry("Osp", "O").add("N", "M", "Osp", "O")
    F.marry("N", "M")
    F.check(coded_facts("K & L", CODE_A) + coded_facts("L @ M", CODE_A) + coded_facts("M % N", CODE_A)
            + coded_facts("N $ O", CODE_A))
    F_variants.append((F.rel("O", "M"), F.rel("K", "N")))
assert F_variants == [("father-in-law", "mother-in-law"), ("mother-in-law", "mother-in-law")]
mcq(BLD, CDB, "Advanced",
    "In a certain code:\n'A $ B' means 'A is the son of B';\n'A % B' means 'A is the wife of B';\n'A @ B' means 'A is "
    "the sister of B';\n'A # B' means 'A is the father of B';\n'A & B' means 'A is the mother of B'.\n\nIf "
    "'K & L @ M % N $ O', which of the following is definitely true?",
    "K is the mother-in-law of N", ["O is the father-in-law of M", "L is the wife of N", "K is the mother of O"],
    "Separate what the code fixes from what it leaves open",
    "K is the mother of L; L is the sister of M, so K is also M's mother; M is N's wife, so K is N's mother-in-law — "
    "certain. N is the son of O, so O is M's father-in-law or mother-in-law; O's gender is not given, so 'father-in-law' "
    "is not definite. L is N's sister-in-law, not his wife, and K is not O's mother.",
    ["K & L, L @ M ⇒ K is M's mother", "M % N ⇒ K is N's mother-in-law (definite)",
     "N $ O ⇒ O is a parent of N; O's gender unknown ⇒ 'father-in-law' not definite"],
    why_others_wrong="'O is the father-in-law of M' fails if O is N's mother; L is N's sister-in-law; K and O are "
                     "parents of the couple, not mother and child.", seconds=90, verified_by=RECOMP)

# ================================================================================================ DIRECTION SENSE
DD, PP, SH_ = "Distance and direction", "Point-to-point", "Shadow-based"
x, y = walk("E", [(None, 5), ("L", 3), ("L", 9), ("L", 3)])
assert (x, y) == (-4, 0)
mcq(DIR, DD, "Basic",
    "Anjali cycles 5 km towards the east. She turns left and cycles 3 km, turns left again and cycles 9 km, and then "
    "turns left once more and cycles 3 km. How far is she from her starting point, and in which direction?",
    "4 km West", ["4 km East", "14 km West", "3 km North"], "Track east–west and north–south separately",
    "East–west: 5 km east, then 9 km west ⇒ 4 km west. North–south: 3 km north (first left from east), then 3 km south "
    "(third left) ⇒ 0. She is 4 km west of the start.",
    ["Facing east → left = north → left = west → left = south", "East–west: +5 − 9 = −4", "North–south: +3 − 3 = 0",
     "⇒ 4 km West"],
    why_others_wrong="4 km East reverses the net east–west movement; 14 km adds the two east–west legs; 3 km North "
                     "forgets the final 3 km south.", seconds=40, verified_by=RECOMP)
ANG = {"N": 0, "NE": 45, "E": 90, "SE": 135, "S": 180, "SW": 225, "W": 270, "NW": 315}
ANAME = {"N": "North", "NE": "North-East", "E": "East", "SE": "South-East", "S": "South", "SW": "South-West",
         "W": "West", "NW": "North-West"}
shadow = "W"  # morning: the sun is in the east, so shadows fall towards the west
face = next(k for k in "NESW" if CW[(CW.index(k) + 1) % 4] == shadow)  # her right points to the shadow
after = next(k for k, a in ANG.items() if a == (ANG[face] + 135) % 360)
assert (face, after) == ("S", "NW")
mcq(DIR, SH_, "Intermediate",
    "Early one morning, soon after sunrise, Meera stands in an open field and notices that her shadow falls exactly to "
    "her right. She then turns 135° clockwise. In which direction is she facing now?", ANAME[after],
    ["South-West", "North-East", "South-East"], "Morning shadows point west",
    "In the morning the sun is in the east, so shadows fall to the west. Her shadow is to her right, so her right hand "
    "points west and she is facing south. Turning 135° clockwise from south (180°) gives 315°, which is north-west.",
    ["Morning sun in the east ⇒ shadow to the west", "Right = west ⇒ facing south",
     "South (180°) + 135° clockwise = 315° ⇒ North-West"],
    why_others_wrong="South-West turns only 45°; North-East turns 135° anticlockwise; South-East assumes she first faced "
                     "north.", seconds=55, verified_by=RECOMP)
PTS = {"A": (0, 0)}
PTS["B"] = (PTS["A"][0] + 10, PTS["A"][1])
PTS["C"] = (PTS["B"][0], PTS["B"][1] + 6)
PTS["D"] = (PTS["C"][0] - 4, PTS["C"][1])
PTS["E"] = (PTS["D"][0], PTS["D"][1] - 11)
PTS["F"] = (PTS["E"][0] + 6, PTS["E"][1])
dx, dy = PTS["F"][0] - PTS["A"][0], PTS["F"][1] - PTS["A"][1]
assert (dx, dy) == (12, -5) and dist(dx, dy) == "13" and compass(dx, dy) == "South-East"
mcq(DIR, PP, "Advanced",
    "Point B is 10 m east of point A. Point C is 6 m north of point B. Point D is 4 m west of point C. Point E is 11 m "
    "south of point D. Point F is 6 m east of point E. What is the shortest distance between A and F, and in which "
    "direction is F with respect to A?", "13 m, South-East", ["13 m, North-East", "17 m, South-East", "12 m, East"],
    "Reduce the route to net east and net north displacements",
    "Take A as the origin. B (10, 0), C (10, 6), D (6, 6), E (6, −5), F (12, −5). F is 12 m east and 5 m south of A, "
    "so AF = √(12² + 5²) = √169 = 13 m, towards the south-east.",
    ["Coordinates: B (10, 0), C (10, 6), D (6, 6), E (6, −5), F (12, −5)", "Net: 12 m east, 5 m south",
     "AF = √(144 + 25) = 13 m, South-East"],
    why_others_wrong="North-East ignores that E is 11 m south of a point only 6 m north of the line AB; 17 m adds the "
                     "net legs instead of using Pythagoras; 12 m East ignores the 5 m southward offset.", seconds=75,
    verified_by=RECOMP)
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

NRULES["last-letter-shift"] = lambda w: pos(w[-1]) * len(w)
NRULES["first+last"] = lambda w: pos(w[0]) + pos(w[-1])

# ---- Basic set: sentence coding with one unresolved pair
SS = [(["clean", "the", "city"], ["ka", "mo", "ri"]), (["the", "city", "sleeps"], ["mo", "ri", "ze"]),
      (["city", "lights", "glow"], ["ri", "pu", "lo"])]
sid = stimulus("passage", "Three coded sentences about a city",
               "In a certain code language:\n'clean the city' is written as 'ka mo ri',\n'the city sleeps' is written "
               "as 'mo ri ze', and\n'city lights glow' is written as 'ri pu lo'.\n(The codes of the words in a "
               "sentence may be in any order.)", None,
               "'city' is the only word in all three sentences, and 'ri' the only code in all three: city = ri. "
               "Sentences 1 and 2 share 'the city' and the codes 'mo ri', so the = mo. The leftovers give clean = ka "
               "and sleeps = ze. In sentence 3, 'lights' and 'glow' share the codes 'pu' and 'lo', and nothing tells "
               "which is which.")
CQ = lambda sub, diff, text, correct, wrongs, concept, expl, steps, **kw: mcq(
    COD, sub, diff, text, correct, wrongs, concept, expl, steps, stimulus=sid, verified_by=RECOMP, **kw)
assert sentence_solve(SS, "clean") == {"ka"}
CQ(SW, "Basic", "What is the code for 'clean'?", "ka", ["mo", "ri", "ze"], "Strip away the shared words' codes",
   "city = ri (in all three sentences) and the = mo (shared by sentences 1 and 2). The remaining code of sentence 1 is "
   "ka, so clean = ka.", ["city = ri", "the = mo", "clean = ka"],
   why_others_wrong="mo is 'the', ri is 'city' and ze is 'sleeps'.", seconds=40)
assert sentence_solve(SS, "mo") == {"the"}
CQ(SW, "Basic", "Which word is coded as 'mo'?", "the", ["city", "clean", "sleeps"],
   "Two shared words: settle one of them from a third sentence",
   "Sentences 1 and 2 share 'the' and 'city', and the codes 'mo' and 'ri'. Sentence 3 contains 'city' and 'ri' but not "
   "'the' or 'mo', so city = ri and the = mo.", ["Shared by 1 and 2: the, city ↔ mo, ri", "Sentence 3: city = ri",
                                                 "⇒ the = mo"],
   why_others_wrong="city = ri, clean = ka, sleeps = ze.", seconds=45)
assert sentence_solve(SS, "glow") == {"pu", "lo"}
CQ(SW, "Basic", "Which of the following can be the code for 'glow'?", "lo", ["ri", "ze", "ka"],
   "When two words share two codes, either assignment is possible",
   "In 'city lights glow' = 'ri pu lo', city = ri, so 'lights' and 'glow' take 'pu' and 'lo' in some order. 'lo' is "
   "one of the two possible codes for 'glow'; the others belong to city, sleeps and clean.",
   ["city = ri", "lights, glow ↔ pu, lo (order unknown)", "Among the options only 'lo' is possible"],
   why_others_wrong="ri is 'city', ze is 'sleeps' and ka is 'clean'.", seconds=45)

# ---- Basic standalone
rv1 = lambda w: shift(w[::-1], 1)
ans = inferred([("FLOWER", rv1("FLOWER"))], "GARDEN", rv1("GARDEN"))
assert rv1("FLOWER") == "SFXPMG" and ans == "OFESBH"
mcq(COD, LC, "Basic", "In a certain code, FLOWER is written as SFXPMG. How is GARDEN written in that code?", ans,
    ["HBSEFO", "OFESBG", "NDCRZF"], "Reverse the word, then shift each letter",
    "FLOWER reversed is REWOLF; moving each letter one place forward gives SFXPMG. GARDEN reversed is NEDRAG; one place "
    "forward: OFESBH.", ["FLOWER → REWOLF → +1 → SFXPMG ✓", "GARDEN → NEDRAG → +1 → OFESBH"],
    why_others_wrong="HBSEFO shifts without reversing; OFESBG leaves the last letter unshifted; NDCRZF shifts backward.",
    seconds=40, verified_by=RECOMP)
ep = NRULES["ends-product"]
assert ep("CAT") == 60 and ep("DOG") == 28
ans = inferred([("CAT", 60), ("DOG", 28)], "LAMP", ep("LAMP"), NRULES)
assert ans == 192
mcq(COD, NC, "Basic", "In a certain code, CAT is written as 60 and DOG is written as 28. How is LAMP written in that "
    "code?", str(ans), ["42", "28", "180"], "Only the end letters matter",
    "CAT: C = 3 and T = 20, 3 × 20 = 60. DOG: D = 4 and G = 7, 4 × 7 = 28. LAMP: L = 12 and P = 16, 12 × 16 = 192.",
    ["Code = position of first letter × position of last letter", "CAT 3 × 20 = 60 ✓; DOG 4 × 7 = 28 ✓",
     "LAMP 12 × 16 = 192"],
    why_others_wrong="42 is the sum of all four positions; 28 is the sum of the end positions; 180 multiplies L by O.",
    natural=int, seconds=45, verified_by=RECOMP)

# ---- Intermediate standalone
vc = LRULES["vc2,-1"]
assert vc("PAINT") == "OCKMS"
ans = inferred([("PAINT", "OCKMS")], "SUGAR", vc("SUGAR"))
assert ans == "RWFCQ"
mcq(COD, LC, "Intermediate", "In a certain code, PAINT is written as OCKMS. How is SUGAR written in that code?", ans,
    ["RWFCS", "TSHYS", "RVFBQ"], "Vowels and consonants follow different rules",
    "In PAINT the vowels A and I move two places forward (C, K) and the consonants P, N and T move one place back (O, M, "
    "S). SUGAR: S → R, U → W, G → F, A → C, R → Q, giving RWFCQ.",
    ["Vowels +2: A→C, I→K", "Consonants −1: P→O, N→M, T→S", "SUGAR → R W F C Q"],
    why_others_wrong="RWFCS moves the last R forward; TSHYS reverses both rules; RVFBQ moves the vowels only one place.",
    seconds=60, verified_by=RECOMP)
wc2 = lambda w: w[-1].upper() + str(len(w)) + w[0].upper()
EX = [("green leaf", "N5G F4L"), ("quiet room", "T5Q M4R")]
assert all(" ".join(wc2(x) for x in s_.split()) == c_ for s_, c_ in EX)
ALT = {"last+len+first": wc2, "first+len+last": lambda w: w[0].upper() + str(len(w)) + w[-1].upper(),
       "last+vowels+first": lambda w: w[-1].upper() + str(sum(c in "aeiou" for c in w)) + w[0].upper(),
       "last+len-1+first": lambda w: w[-1].upper() + str(len(w) - 1) + w[0].upper(),
       "second-last+len+first": lambda w: w[-2].upper() + str(len(w)) + w[0].upper()}
fits = {k: " ".join(f_(x) for x in "deep ocean water".split()) for k, f_ in ALT.items()
        if all(" ".join(f_(x) for x in s_.split()) == c_ for s_, c_ in EX)}
assert set(fits.values()) == {"P4D N5O R5W"}
mcq(COD, SW, "Intermediate", "In a certain code language, each word is coded by the same rule, and the codes are "
    "written in the same order as the words. 'green leaf' is written as 'N5G F4L', and 'quiet room' is written as "
    "'T5Q M4R'. How is 'deep ocean water' written in that code language?", "P4D N5O R5W",
    ["D4P O5N W5R", "P4D N5O R4W", "P2D N3O R2W"], "Code = last letter + length + first letter",
    "green → last letter N, 5 letters, first letter G: N5G. leaf → F4L; quiet → T5Q; room → M4R. deep → P4D, ocean → "
    "N5O, water → R5W.", ["Pattern: last letter, number of letters, first letter", "deep P4D, ocean N5O, water R5W"],
    why_others_wrong="D4P O5N W5R puts the first letter first; P4D N5O R4W miscounts 'water'; P2D N3O R2W counts the "
                     "vowels instead of the letters.", seconds=60, verified_by=RECOMP)

# ---- Advanced set: two-step letter code
STEPS_TXT = ("In a certain code language, every word is coded in two steps.\nStep 1: Each letter in an odd position of "
             "the word (1st, 3rd, 5th, …) is replaced by the letter two places after it in the English alphabet, and "
             "each letter in an even position (2nd, 4th, …) by the letter one place before it. The alphabet wraps "
             "round (Y → A, Z → B, A → Z).\nStep 2: If the word begins with a vowel, the letters obtained in step 1 "
             "are written in reverse order; otherwise they are kept in the same order.")


def code2(w):
    s1 = "".join(shift(c, 2 if i % 2 == 0 else -1) for i, c in enumerate(w))
    return s1[::-1] if w[0] in VOW else s1


assert code2("MONEY") == "ONPDA" and code2("ASSET") == "VDURC" and code2("BONUS") == "DNPTU"
sid = stimulus("passage", "A two-step code: position shifts, then reversal for vowel-initial words", STEPS_TXT, None,
               "Work letter by letter: +2 for the 1st, 3rd, 5th, … letters and −1 for the 2nd, 4th, … letters, "
               "wrapping round the alphabet. Then reverse the result only if the original word starts with A, E, I, O "
               "or U. To decode, undo step 2 first (reverse if the word might start with a vowel) and then shift "
               "back.")
AQ = lambda text, correct, wrongs, concept, expl, steps, **kw: mcq(
    COD, LC, "Advanced", text, correct, wrongs, concept, expl, steps, stimulus=sid, verified_by=RECOMP, **kw)
AQ("What is the code for 'MONEY'?", code2("MONEY"), ["ONPDW", "ADPNO", "OPPFA"], "Watch the wrap-round at the end",
   "M +2 = O, O −1 = N, N +2 = P, E −1 = D, Y +2 = A (Y → Z → A). MONEY begins with a consonant, so the order is kept: "
   "ONPDA.", ["Odd positions +2: M→O, N→P, Y→A", "Even positions −1: O→N, E→D", "Starts with M ⇒ no reversal ⇒ ONPDA"],
   why_others_wrong="ONPDW moves Y back instead of forward; ADPNO reverses a word that starts with a consonant; OPPFA "
                    "moves every letter forward.", seconds=75)
AQ("What is the code for 'ASSET'?", code2("ASSET"), ["CRUDV", "VDURE", "CTUFV"], "Step 2 applies to vowel-initial words",
   "Step 1: A +2 = C, S −1 = R, S +2 = U, E −1 = D, T +2 = V, giving CRUDV. ASSET begins with a vowel, so step 2 "
   "reverses it: VDURC.", ["Step 1: C R U D V", "Starts with A ⇒ reverse ⇒ VDURC"],
   why_others_wrong="CRUDV stops after step 1; VDURE leaves the A unshifted; CTUFV moves every letter forward.",
   seconds=75)
CANDS = ["BONUS", "BOATS", "BINGO", "BASIS"]
codes_ = {w: code2(w) for w in CANDS}
assert [w for w in CANDS if codes_[w] == "DNPTU"] == ["BONUS"]
AQ("Which word is coded as 'DNPTU'?", "BONUS", CANDS[1:], "Decode by reversing the two steps",
   "DNPTU begins with D; if the word started with a vowel the code would be reversed. Undoing step 1 from the left: "
   "D −2 = B, N +1 = O, P −2 = N, T +1 = U, U −2 = S: BONUS, which begins with a consonant, so no reversal was "
   "applied — consistent.", ["Undo step 1: −2 on odd positions, +1 on even positions", "DNPTU → B O N U S",
                             "BONUS starts with a consonant ⇒ no reversal ⇒ consistent"],
   why_others_wrong=f"BOATS is coded {codes_['BOATS']}, BINGO {codes_['BINGO']} and BASIS {codes_['BASIS']}.",
   seconds=80)
c_eq = code2("EQUITY")
ans = c_eq[-3]
assert c_eq == "XVHWPG" and ans == "W"
AQ("In the code for 'EQUITY', which letter is third from the right end?", ans, ["H", "P", "V"],
   "Apply both steps before counting positions",
   "Step 1: E→G, Q→P, U→W, I→H, T→V, Y→X, giving GPWHVX. EQUITY begins with a vowel, so the code is XVHWPG. From the "
   "right: G, P, W — the third letter is W.", ["Step 1: G P W H V X", "Starts with E ⇒ reverse ⇒ XVHWPG",
                                                 "Third from the right ⇒ W"],
   why_others_wrong="H is third from the right before the reversal; P is second from the right; V is second from the "
                    "left.", seconds=80)

# ---- Advanced standalone: number coding
cv = NRULES["consonants-vowels"]
assert cv("LOAN") == 10 and cv("CASH") == 29
ans = inferred([("LOAN", 10), ("CASH", 29)], "SAVE", cv("SAVE"), NRULES)
assert ans == 35
mcq(COD, NC, "Advanced", "In a certain code, LOAN is written as 10 and CASH is written as 29. How is SAVE written in "
    "that code?", str(ans), ["47", "41", "45"], "Consonants add, vowels subtract",
    "Using alphabetical positions, the consonants are added and the vowels subtracted. LOAN: L 12 − O 15 − A 1 + N 14 = "
    "10. CASH: C 3 − A 1 + S 19 + H 8 = 29. SAVE: S 19 − A 1 + V 22 − E 5 = 35.",
    ["LOAN: 12 − 15 − 1 + 14 = 10 ✓", "CASH: 3 − 1 + 19 + 8 = 29 ✓", "SAVE: 19 − 1 + 22 − 5 = 35"],
    why_others_wrong="47 adds all four positions; 41 adds the consonants only; 45 adds E instead of "
                     "subtracting it.", natural=int, seconds=80, verified_by=RECOMP)

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


# ---- Basic (standalone)
SR = "M 4 # R 7 K @ 2 E 9 $ T 5 W & 3 B % 8 H".split()
assert len(SR) == 20
i11 = len(SR) - 11
ans = SR[i11 + 5]
assert SR[i11] == "9" and ans == "&"
mcq(ALN, PB, "Basic", series_intro(" ".join(SR)) + "\n\nWhich element is 5th to the right of the 11th element from the "
    "right end?", ans, near(SR, i11 + 5), "Convert a right-end position, then move right",
    f"The 11th element from the right is the {i11 + 1}th from the left (9). Five places to its right is the "
    f"{i11 + 6}th element from the left: {ans}.", [f"11th from the right = 20 − 11 + 1 = {i11 + 1}th from the left = 9",
                                                   f"{i11 + 1} + 5 = {i11 + 6}th ⇒ {ans}"],
    why_others_wrong="The other options are the elements one or two places away from the correct position.",
    seconds=40, verified_by=RECOMP)
SR = "6 F ★ 3 J A 8 © N 1 S Y £ 5 O 2 G ¥ 4 V".split()
assert len(SR) == 20
nw = SR[:10][::-1] + SR[10:]
ans = nw[3]
assert ans == "8"
mcq(ALN, PB, "Basic", series_intro(" ".join(SR)) + "\n\nIf the first ten elements of the arrangement are written in "
    "reverse order, which element will be 4th from the left end?", ans, near(nw, 3), "Reverse a block, then count",
    "The first ten elements are " + " ".join(SR[:10]) + "; reversed they read " + " ".join(SR[:10][::-1]) + f". The 4th "
    f"from the left is {ans} (it was the 7th element from the left, since 10 − 4 + 1 = 7).",
    ["Reversed block: " + " ".join(SR[:10][::-1]), "4th from the left ⇒ original 7th ⇒ " + ans],
    why_others_wrong="The other options are the neighbours of the 4th position in the reversed block.", seconds=40,
    verified_by=RECOMP)

# ---- Intermediate set 1: symbols and numbers
SR1 = "D 3 * K 8 L ! 6 P 2 U # 7 Q ◆ A 4 Z 9 @ G 1 Y ^".split()
assert len(SR1) == 24
sid = stimulus("data_table", "Arrangement of 24 elements ending in a symbol", series_intro(" ".join(SR1)), None,
               "Number the elements 1 to 24 from the left. For neighbour questions, check each element's left and "
               "right neighbours; for position questions, convert right-end positions with (25 − k).")
AQ = lambda sub, text, correct, wrongs, concept, expl, steps, **kw: mcq(
    ALN, sub, "Intermediate", text, correct, wrongs, concept, expl, steps, stimulus=sid, verified_by=RECOMP, **kw)
hits = [(SR1[i - 1], SR1[i]) for i in range(1, len(SR1)) if is_s(SR1[i]) and is_d(SR1[i - 1])]
assert hits == [("3", "*"), ("9", "@")]
a, w = count_opts(len(hits))
AQ(SN, "Count the symbols whose left-hand neighbour is a number. How many such symbols are there?", a, w,
   "Look at the left neighbour of every symbol",
   "The symbols and their left neighbours: " + ", ".join(f"{SR1[i - 1]} {SR1[i]}" for i in range(1, len(SR1))
                                                        if is_s(SR1[i])) + ". Only 3 * and 9 @ have a number before "
   "the symbol: two.", ["Symbols: * ! # ◆ @ ^", "Preceded by a number: 3 *, 9 @ ⇒ two"], natural=by_num, seconds=50)
hits = [(SR1[i], SR1[i + 1]) for i in range(len(SR1) - 1) if is_d(SR1[i]) and CONS(SR1[i + 1])]
tot = sum(int(a_) for a_, _ in hits)
assert tot == 26
AQ(SN, "What is the sum of the numbers in the arrangement that are immediately followed by a consonant?", str(tot),
   ["22", "28", "35"], "Filter by the right neighbour, then add",
   "Numbers followed by a consonant: " + ", ".join(f"{a_} {b_}" for a_, b_ in hits) + f". Sum: "
   + " + ".join(a_ for a_, _ in hits) + f" = {tot}. (2 is followed by the vowel U, 3 and 9 by symbols.)",
   ["Numbers followed by a consonant: 8, 6, 7, 4, 1", f"8 + 6 + 7 + 4 + 1 = {tot}"],
   why_others_wrong="22 leaves out 4; 28 also adds 2, which is followed by the vowel U; 35 also adds 9, which is "
                    "followed by a symbol.", natural=int, seconds=60)
a3, b3 = 2, len(SR1) - 6
ans = SR1[(a3 + b3) // 2]
assert (SR1[a3], SR1[b3], ans) == ("*", "9", "U")
AQ(PB, "Take the stretch of the arrangement that runs from the 3rd element from the left end to the 6th element from "
   "the right end. Which element sits at the exact centre of that stretch?", ans, near(SR1, (a3 + b3) // 2), "Midway = average of the two positions",
   "The 3rd from the left is * (position 3). The 6th from the right is position 24 − 6 + 1 = 19 (9). Midway: "
   f"(3 + 19) ÷ 2 = 11th: {ans}.", ["3rd from the left = position 3 (*)", "6th from the right = position 19 (9)",
                                    f"(3 + 19) ÷ 2 = 11 ⇒ {ans}"], seconds=55)
g = [x for i in range(0, 24, 4) for x in SR1[i:i + 4][::-1]]
ans = g[-10]
assert ans == "Q"
AQ(PB, "If the elements are taken in groups of four from the left (D 3 * K, 8 L ! 6, and so on) and the order of the "
   "elements within each group is reversed, which element will be 10th from the right end?", ans, near(g, 24 - 10),
   "Reverse within groups; positions of whole groups do not change",
   "New arrangement: " + " ".join(g) + f". The 10th from the right is the 15th from the left: {ans}.",
   ["Groups reversed: " + " | ".join(" ".join(g[i:i + 4]) for i in range(0, 24, 4)),
    f"10th from the right = 24 − 10 + 1 = 15th from the left ⇒ {ans}"], seconds=65)

# ---- Intermediate set 2: positions after deleting the numbers
SR2 = "7 B & N 2 O 5 % H J 8 ▲ E 3 T # 9 C I 6 $ W 4 X".split()
assert len(SR2) == 24
sid = stimulus("data_table", "Arrangement of 24 elements starting with a number", series_intro(" ".join(SR2)), None,
               "Number the elements 1 to 24 from the left. When elements are removed, renumber the remaining ones "
               "before counting.")
AQ = lambda sub, text, correct, wrongs, concept, expl, steps, **kw: mcq(
    ALN, sub, "Intermediate", text, correct, wrongs, concept, expl, steps, stimulus=sid, verified_by=RECOMP, **kw)
nn = [t for t in SR2 if not is_d(t)]
ans = nn[14 - 6]
assert (nn[14], ans) == ("W", "E")
AQ(PB, "If all the numbers are removed from the arrangement, which element will be 6th to the left of the 15th element "
   "from the left end?", ans, near(nn, 8), "Delete first, then count",
   "Without numbers: " + " ".join(nn) + f". The 15th element is {nn[14]}; six places to its left is the 9th: {ans}.",
   ["Remove 7, 2, 5, 8, 3, 9, 6, 4", "Remaining: " + " ".join(nn), f"15th = {nn[14]}; 15 − 6 = 9th ⇒ {ans}"],
   seconds=60)
vows = [i for i, t in enumerate(SR2) if t in VOW]
nums = [i for i, t in enumerate(SR2) if is_d(t)]
lo_, hi_ = sorted((vows[1], nums[-2]))
btw = [SR2[k] for k in range(lo_ + 1, hi_) if is_l(SR2[k])]
assert (SR2[vows[1]], SR2[nums[-2]], btw) == ("E", "6", ["T", "C", "I"])
a, w = count_opts(len(btw))
AQ(SN, "How many letters are there between the second vowel from the left end and the second number from the right "
   "end?", a, w, "Locate both reference elements first",
   "Vowels from the left: O (6th), E (13th), … — the second is E. Numbers from the right: 4 (23rd), 6 (20th), … — the "
   "second is 6. Between E (13th) and 6 (20th) lie 3, T, #, 9, C, I; the letters among them are T, C and I: three.",
   ["Second vowel from the left: E (13th)", "Second number from the right: 6 (20th)",
    "Between them: 3 T # 9 C I ⇒ letters T, C, I ⇒ three"], natural=by_num, seconds=65)
LT = sorted(t for t in SR2 if is_l(t))
it_ = iter(LT)
sorted_arr = [next(it_) if is_l(t) else t for t in SR2]
ans = sorted_arr[8]
assert ans == "H"
AQ(PB, "If only the letters of the arrangement are rearranged in alphabetical order from left to right, occupying the "
   "same places that letters occupy now (numbers and symbols stay where they are), which element will be 9th from the "
   "left end?", ans, near(sorted_arr, 8), "Only the letters move",
   "The letters in alphabetical order are " + ", ".join(LT) + ". Filling the letter places from the left: "
   + " ".join(sorted_arr) + f". The 9th element is {ans}.",
   ["Letter places: 2, 4, 6, 9, 10, 13, 15, 18, 19, 22, 24", "Alphabetical letters: " + " ".join(LT),
    f"Place 9 is the 4th letter place ⇒ {LT[3]}"], seconds=75)
assert LT[3] == ans

# ---- Advanced (standalone)
SR = "K 2 E @ 9 P # U 6 R £ 3 A L 8 © T 5 I ¥ D 7 W 4".split()
assert len(SR) == 24
step1 = [shift(t, 1) if is_l(t) else t for t in SR]
step2 = [t for i, t in enumerate(step1) if (i + 1) % 2 == 1]
ans = step2[-4]
assert ans == "U"
mcq(ALN, PB, "Advanced", series_intro(" ".join(SR)) + "\n\nIf every letter in the arrangement is replaced by the "
    "letter that comes immediately after it in the English alphabet, and then every element in an even-numbered "
    "position (2nd, 4th, 6th, …) is removed, which element will be 4th from the right end?", ans, near(step2, len(step2) - 4),
    "Replace, delete by original positions, then count",
    "After replacing letters: " + " ".join(step1) + ". Keeping only the 1st, 3rd, 5th, … elements: " + " ".join(step2)
    + f". The 4th from the right is {ans}.",
    ["Letters +1: " + " ".join(step1), "Keep odd positions: " + " ".join(step2), f"4th from the right ⇒ {ans}"],
    why_others_wrong="The other options are its neighbours in the final arrangement.", seconds=90, verified_by=RECOMP)
SR3 = "K 2 # E @ 9 P 6 # U R 3 £ A L 8 © T 5 I ¥ D 7 W 4".split()
assert len(SR3) == 25
hits = [i for i in range(1, len(SR3) - 1) if is_d(SR3[i]) and CONS(SR3[i - 1]) and is_s(SR3[i + 1])]
val = sum(int(SR3[i]) for i in hits) * len(hits)
assert [SR3[i] for i in hits] == ["2", "6", "3", "8"] and val == 76
mcq(ALN, SN, "Advanced", series_intro(" ".join(SR3)) + "\n\nEach number that is immediately preceded by a consonant "
    "and immediately followed by a symbol is selected. What is the sum of the selected numbers multiplied by the "
    "number of numbers selected?", str(val), ["57", "95", "68"], "Two-sided neighbour test, then compute",
    "Numbers with their neighbours: " + ", ".join(f"{SR3[i - 1]} {SR3[i]} {SR3[i + 1]}" for i in range(1, len(SR3) - 1)
                                                  if is_d(SR3[i])) + ". Consonant before and symbol after: K 2 #, "
    "P 6 #, R 3 £ and L 8 © — four numbers (9 has a symbol before it, 5 a vowel after it, 7 a letter after it, and 4 "
    "has no right neighbour). Sum 2 + 6 + 3 + 8 = 19; 19 × 4 = 76.",
    ["Selected: 2, 6, 3, 8 (four numbers)", "Sum = 19", "19 × 4 = 76"],
    why_others_wrong="57 multiplies 19 by 3 instead of 4; 95 multiplies by 5; 68 leaves out 2 (17 × 4).",
    natural=int, seconds=90, verified_by=RECOMP)

# ================================================================================================ ALPHABET TEST
ABT = "Alphabet Test"
LP, WF, PRS = "Letter position", "Word formation", "Pairs of letters"
NEWAL = [c for c in AL if c not in VOW] + ["A", "E", "I", "O", "U"]
p3, p10 = 3, 26 - 10 + 1
mid = NEWAL[(p3 + p10) // 2 - 1]
ans = NEWAL[NEWAL.index(mid) - 4]
assert (NEWAL[p3 - 1], NEWAL[p10 - 1], mid, ans) == ("D", "V", "M", "H")
mcq(ABT, LP, "Advanced",
    "The five vowels are taken out of the English alphabet and written, in the order A, E, I, O, U, after Z; the 21 "
    "consonants keep their original order before them. In this new sequence, which letter is 4th to the left of the "
    "letter that lies exactly midway between the 3rd letter from the left end and the 10th letter from the right end?",
    ans, ["G", "J", "F"], "Rebuild the sequence before counting",
    "New sequence: " + " ".join(NEWAL) + ". The 3rd from the left is D (position 3); the 10th from the right is "
    "position 26 − 10 + 1 = 17, V. Midway: (3 + 17) ÷ 2 = 10th, M. Four places to the left of M is the 6th letter, H.",
    ["New order: consonants B…Z, then A E I O U", "3rd from left = D (3); 10th from right = V (17)",
     "Midway = 10th = M", "10 − 4 = 6th ⇒ H"],
    why_others_wrong="G and J are one place off; F is the answer in the ordinary alphabet's counting of the new "
                     "sequence's 4th letter.", seconds=90, verified_by=RECOMP)

# ================================================================================================ NUMBER SERIES (REASONING)
NSR = "Number Series (Reasoning)"
NDO, TDN = "Number-based digit operations", "Three-digit number questions"
dg = lambda n: [int(c) for c in str(n)]

# ---- Basic set: five three-digit numbers
NUMS = [642, 389, 715, 926, 453]
sid = stimulus("data_table", "Five three-digit numbers (set B)",
               "Study the following five three-digit numbers and answer the questions.\n\n" + "   ".join(map(str, NUMS)),
               None, "Apply each operation to every number before comparing.")
NQ = lambda text, correct, wrongs, concept, expl, steps, **kw: mcq(
    NSR, TDN, "Basic", text, correct, wrongs, concept, expl, steps, stimulus=sid, verified_by=RECOMP, **kw)
sw = {n: int(str(n)[::-1]) for n in NUMS}  # three digits: interchanging first and last = reversing
best = max(NUMS, key=sw.get)
assert best == 389 and sw[best] == 983
NQ("If the first and the last digits of each number are interchanged, which original number becomes the largest?",
   str(best), ["926", "715", "642"], "Interchange, then compare",
   "New numbers: " + ", ".join(f"{n} → {sw[n]}" for n in NUMS) + ". The largest is 983, from 389.",
   ["Interchanged values listed", "Largest 983 ⇐ 389"],
   why_others_wrong="926 → 629, 715 → 517 and 642 → 246 are all smaller than 983.", seconds=40)
s_ = sorted(NUMS)
ans = sum(dg(s_[-2]))
assert (s_[-2], ans) == (715, 13)
NQ("What is the sum of the digits of the second largest number?", str(ans), ["17", "12", "18"], "Sort, then add digits",
   "In ascending order: " + ", ".join(map(str, s_)) + ". The second largest is 715: 7 + 1 + 5 = 13.",
   ["Second largest = 715", "7 + 1 + 5 = 13"],
   why_others_wrong="17 is the digit sum of 926 (the largest); 12 is that of 453; 18 is that of 642.", natural=int,
   seconds=35)
cnt = sum(1 for n in NUMS if dg(n)[1] > dg(n)[0] and dg(n)[1] > dg(n)[2])
assert cnt == 1
a, w = count_opts(cnt)
NQ("In how many numbers is the middle digit greater than both the first digit and the last digit?", a, w,
   "Compare the middle digit with both ends",
   "642: 4 < 6. 389: 8 < 9. 715: 1 is smallest. 926: 2 < 9. 453: 5 > 4 and 5 > 3 ✓. Only one number.",
   ["Check each number's middle digit", "Only 453 qualifies"], natural=by_num, seconds=40)
new = {n: int("".join(str(d - 1) for d in dg(n))) for n in NUMS}
cnt = sum(1 for n in NUMS if new[n] % 2 == 0)
assert cnt == 3
a, w = count_opts(cnt)
NQ("If 1 is subtracted from each digit of every number, how many of the new numbers will be even?", a, w,
   "Only the last digit decides evenness",
   "New numbers: " + ", ".join(f"{n} → {new[n]}" for n in NUMS) + ". Even: 278, 604, 342 — three.",
   ["Last digits after −1: 1, 8, 4, 5, 2", "Even: three"], natural=by_num, seconds=40)
ans = dg(s_[0])[0] * dg(s_[0])[2]
assert ans == 27
NQ("What is the product of the first and the last digits of the smallest number?", str(ans), ["24", "72", "12"],
   "Find the smallest number first", "The smallest number is 389; 3 × 9 = 27.", ["Smallest = 389", "3 × 9 = 27"],
   why_others_wrong="24 multiplies the first two digits (3 × 8); 72 the last two (8 × 9); 12 uses 453 (4 × 3).",
   natural=int, seconds=35)

# ---- Advanced set: five four-digit numbers
NUMS4 = [7316, 4859, 2694, 9147, 5382]
sid = stimulus("data_table", "Five four-digit numbers (set B)",
               "Study the following five four-digit numbers and answer the questions.\n\n"
               + "   ".join(map(str, NUMS4)), None,
               "Apply each operation to every number, write the new numbers down, and only then compare or count.")
NQ = lambda text, correct, wrongs, concept, expl, steps, **kw: mcq(
    NSR, NDO, "Advanced", text, correct, wrongs, concept, expl, steps, stimulus=sid, verified_by=RECOMP, **kw)
asc = {n: int("".join(sorted(str(n)))) for n in NUMS4}
order = sorted(NUMS4, key=asc.get, reverse=True)
assert order[2] == 5382
NQ("If the digits of each number are arranged in ascending order within the number, which original number will give "
   "the third largest new number?", str(order[2]), ["2694", "4859", "9147"], "Rearrange digits, then rank",
   "New numbers: " + ", ".join(f"{n} → {asc[n]:04d}" for n in NUMS4) + ". In descending order: "
   + ", ".join(f"{asc[n]}" for n in order) + ". The third largest, 2358, comes from 5382.",
   ["Ascending digits: " + ", ".join(f"{asc[n]}" for n in NUMS4), "Descending: " + ", ".join(f"{asc[n]}" for n in order),
    "Third ⇒ 2358 ⇐ 5382"],
   why_others_wrong="2694 gives the second largest (2469); 4859 the largest (4589); 9147 the fourth (1479).",
   seconds=75)
sw24 = {n: int(str(n)[0] + str(n)[3] + str(n)[2] + str(n)[1]) for n in NUMS4}
o2 = sorted(sw24.values(), reverse=True)
ans = o2[1] - o2[3]
assert o2 == [9741, 7613, 5283, 4958, 2496] and ans == 2655
NQ("If the second and the fourth digits of each number are interchanged and the new numbers are arranged in "
   "descending order, what is the difference between the second and the fourth numbers of that order?", str(ans),
   ["2330", "4458", "2462"], "Interchange, sort, subtract",
   "New numbers: " + ", ".join(f"{n} → {sw24[n]}" for n in NUMS4) + ". Descending: " + ", ".join(map(str, o2))
   + f". Second − fourth = 7613 − 4958 = {ans}.",
   ["Interchanged: " + ", ".join(map(str, sw24.values())), "Descending: " + ", ".join(map(str, o2)),
    "7613 − 4958 = 2655"],
   why_others_wrong="2330 subtracts the third from the second (7613 − 5283); 4458 subtracts the third from the first "
                    "(9741 − 5283); 2462 subtracts the fifth from the fourth (4958 − 2496).", natural=int, seconds=90)
cnt = sum(1 for n in NUMS4 if sum(dg(n)[:2]) > sum(dg(n)[2:]))
assert cnt == 1
a, w = count_opts(cnt)
NQ("In how many numbers is the sum of the first two digits greater than the sum of the last two digits?", a, w,
   "Split each number into two halves",
   "7316: 10 vs 7 ✓; 4859: 12 vs 14; 2694: 8 vs 13; 9147: 10 vs 11; 5382: 8 vs 10. Only one number.",
   ["Compare (d1 + d2) with (d3 + d4) for each", "Only 7316 qualifies"], natural=by_num, seconds=70)
tf = lambda n: int("".join(str(d - 1) if d % 2 else str(d + 1) for d in dg(n)))
new = {n: tf(n) for n in NUMS4}
assert all(len(str(v)) == 4 for v in new.values())
cnt = sum(1 for n in NUMS4 if new[n] % 3 == 0)
assert cnt == 2
a, w = count_opts(cnt)
NQ("If 1 is subtracted from every odd digit and 1 is added to every even digit of each number, how many of the new numbers will be divisible by 3?", a, w, "Digit-sum test for 3",
   "New numbers: " + ", ".join(f"{n} → {new[n]}" for n in NUMS4) + ". Digit sums: "
   + ", ".join(f"{new[n]} → {sum(dg(new[n]))}" for n in NUMS4) + ". Divisible by 3: "
   + ", ".join(str(new[n]) for n in NUMS4 if new[n] % 3 == 0) + " — two.",
   ["Odd digits −1, even digits +1", "Digit sum a multiple of 3 ⇒ divisible by 3", "Count = two"],
   natural=by_num, seconds=90)

# ================================================================================================ RANKING
RNK = "Ranking and Order"
POSR, CHW = "Position in a row", "Comparison of heights/weights"
farid = 12 + 9
ans = 38 - farid + 1
assert ans == 18
mcq(RNK, POSR, "Intermediate", "In a row of 38 students facing north, Esha is 12th from the left end. Farid sits 9th "
    "to the right of Esha. What is Farid's position from the right end?", f"{ORDN(ans)}", ["17th", "19th", "27th"],
    "Position from the other end = total − position + 1",
    "Farid is 12 + 9 = 21st from the left. From the right he is 38 − 21 + 1 = 18th.",
    ["Farid = 12 + 9 = 21st from the left", "38 − 21 + 1 = 18th from the right"],
    why_others_wrong="17th forgets the +1; 19th counts Esha's seat twice; 27th is 38 − 12 + 1, Esha's own position "
                     "from the right.", natural=lambda t: int(t[:-2]), seconds=40, verified_by=RECOMP)
H = {"Amit": 165}
H["Chirag"] = H["Amit"] - 4
H["Bina"] = H["Chirag"] + 8
H["Dev"] = H["Bina"] + 3
order = sorted(H, key=H.get, reverse=True)
assert order == ["Dev", "Bina", "Amit", "Chirag"]
mcq(RNK, CHW, "Intermediate", "Five friends Amit, Bina, Chirag, Dev and Esha have different heights. Amit is 165 cm "
    "tall. Chirag is 4 cm shorter than Amit, and Bina is 8 cm taller than Chirag. Dev is 3 cm taller than Bina, and "
    "Esha is shorter than Chirag. Who is the second tallest?", "Bina", ["Amit", "Dev", "Chirag"],
    "Convert every clue into a height",
    "Chirag = 161 cm, Bina = 169 cm, Dev = 172 cm, Amit = 165 cm, and Esha is below 161 cm. Order: Dev, Bina, Amit, "
    "Chirag, Esha — the second tallest is Bina.",
    ["Chirag 161, Bina 169, Dev 172, Amit 165, Esha < 161", "Dev > Bina > Amit > Chirag > Esha"],
    why_others_wrong="Amit is third, Dev the tallest and Chirag fourth.", seconds=50, verified_by=RECOMP)
P6 = ["Kiran", "Lalit", "Mohan", "Neha", "Omi", "Pari"]
conds = [("Kiran is heavier than only Lalit.", tuple(P6), lambda *v: sum(1 for x in v if x < v[0]) == 1
          and v[1] < v[0]),
         ("Mohan is lighter than Neha but heavier than Omi.", ("Mohan", "Neha", "Omi"), lambda m, n, o: o < m < n),
         ("Neha is not the heaviest.", tuple(P6), lambda *v: v[3] != max(v))]
R6 = unique(P6, {p: range(1, 7) for p in P6}, conds, [P6])  # larger = heavier
ans = next(p for p in P6 if R6[p] == 4)
assert ans == "Mohan"
mcq(RNK, CHW, "Intermediate", "Six persons Kiran, Lalit, Mohan, Neha, Omi and Pari have different weights.\n"
    + bullets(conds) + "\n\nWho is the third heaviest?", ans, ["Neha", "Omi", "Pari"], "Fix the extremes first",
    "Kiran is heavier than only Lalit, so Lalit is the lightest and Kiran fifth. Neha > Mohan > Omi, and Neha is not "
    "the heaviest, so Pari is the heaviest. Order: Pari, Neha, Mohan, Omi, Kiran, Lalit — Mohan is third.",
    ["Lalit 6th, Kiran 5th", "Neha > Mohan > Omi and Neha not 1st ⇒ Pari 1st", "Pari, Neha, Mohan, Omi, Kiran, Lalit"],
    why_others_wrong="Neha is second, Omi fourth and Pari the heaviest.", seconds=55, verified_by=BRUTE)
tot = 16 + 25 - 1 + 3
assert tot == 43
mcq(RNK, POSR, "Intermediate", "In a class, Rahul is 16th from the top and 25th from the bottom in the merit list. "
    "Three students of the class were absent from the examination and were not ranked. How many students are there "
    "in the class?", str(tot), ["40", "44", "41"], "Ranked students + unranked students",
    "Ranked students = 16 + 25 − 1 = 40. Adding the three unranked students gives 43.",
    ["Ranked = 16 + 25 − 1 = 40", "Class = 40 + 3 = 43"],
    why_others_wrong="40 forgets the absent students; 44 forgets to subtract Rahul once; 41 adds 1 instead of 3.",
    natural=int, seconds=40, verified_by=RECOMP)
tara = 11 + 8
ans = 31 - tara
assert ans == 12
mcq(RNK, POSR, "Intermediate", "In a row of 31 persons facing north, Sapna is 11th from the left end and Tara sits 8th "
    "to the right of Sapna. How many persons sit between Tara and the right end of the row (not counting Tara)?",
    num_word(ans), ["Eleven", "Thirteen", "Ten"], "Persons to one side = total − position",
    "Tara is 11 + 8 = 19th from the left, so 31 − 19 = 12 persons sit to her right.",
    ["Tara = 19th from the left", "To her right: 31 − 19 = 12"],
    why_others_wrong="Eleven subtracts one too many; Thirteen counts Tara; Ten miscounts Tara's position.",
    natural=by_num, seconds=40, verified_by=RECOMP)
P5 = ["Uma", "Varun", "Wafa", "Xavi", "Yogi"]
conds = [("Varun is taller than Uma but shorter than Wafa.", ("Varun", "Uma", "Wafa"), lambda v, u, w: u < v < w),
         ("Xavi is shorter than Uma.", ("Xavi", "Uma"), lambda x, u: x < u),
         ("Yogi is taller than Varun but shorter than Wafa.", ("Yogi", "Varun", "Wafa"), lambda y, v, w: v < y < w)]
R5 = unique(P5, {p: range(1, 6) for p in P5}, conds, [P5])
order = sorted(P5, key=R5.get, reverse=True)
assert order == ["Wafa", "Yogi", "Varun", "Uma", "Xavi"]
mcq(RNK, CHW, "Intermediate", "Five friends Uma, Varun, Wafa, Xavi and Yogi have different heights.\n" + bullets(conds)
    + "\n\nWho is exactly in the middle when they are arranged by height?", "Varun", ["Yogi", "Uma", "Wafa"],
    "Merge the chains", "Wafa > Varun > Uma > Xavi, and Yogi is between Varun and Wafa: Wafa, Yogi, Varun, Uma, Xavi. "
    "The middle (3rd) is Varun.", ["Wafa > Varun > Uma > Xavi", "Wafa > Yogi > Varun", "Middle = Varun"],
    why_others_wrong="Yogi is second, Uma fourth and Wafa the tallest.", seconds=45, verified_by=BRUTE)
# Advanced: interchange
a_new = 18
tot = a_new + 13 - 1
ans = tot - a_new
assert (tot, ans) == (30, 12)
mcq(RNK, POSR, "Advanced", "In a row of persons facing north, Arif is 9th from the left end and Bela is 13th from the "
    "right end. When Arif and Bela interchange their places, Arif becomes 18th from the left end. How many persons "
    "then sit to the right of Bela?", "Twenty-one", ["Twenty", "Twelve", "Twenty-two"],
    "After an interchange, each takes the other's old position",
    "After the interchange Arif is at Bela's old place: 18th from the left and 13th from the right, so the row has "
    "18 + 13 − 1 = 30 persons. Bela moves to Arif's old place, 9th from the left, so 30 − 9 = 21 persons sit to her "
    "right.", ["Bela's old place = 18th from left = 13th from right ⇒ total 30", "Bela now 9th from the left",
               "To her right: 30 − 9 = 21"],
    why_others_wrong="Twenty uses 29 persons; Twelve is the count to Arif's right after the interchange; Twenty-two "
                     "counts Bela herself.", seconds=70, verified_by=RECOMP)
assert 30 - 9 == 21

# ================================================================================================ INPUT-OUTPUT
WR, NR, MM = "Word rearrangement", "Number rearrangement", "Mixed machine"
line = lambda s: " ".join(map(str, s))
step_txt = lambda st: [f"Step {ROMAN[i]}: {line(s_)}" for i, s_ in enumerate(st)]


def run_left(items, key):
    """Each step moves the unarranged item with the smallest key to the left end, just right of the arranged ones.
    A step that would leave the line unchanged is still listed only if it changes the line."""
    cur, done, rest, steps = list(items), [], list(items), []
    while rest:
        nxt = min(rest, key=key)
        rest.remove(nxt)
        done.append(nxt)
        new = done + rest
        if new != cur:
            steps.append(new[:])
            cur = new
    return steps


# ---- Basic (standalone): largest number to the left each step
INP = [34, 81, 17, 56, 92, 43]
st = run_left(INP, key=lambda n: -n)
assert st[-1] == sorted(INP, reverse=True) and len(st) == 4
mcq(IOT, NR, "Basic",
    "A number arrangement machine rearranges a line of numbers step by step. In each step it takes the largest number "
    "among those not yet arranged and places it immediately to the right of the numbers already arranged at the left "
    "end (in Step I, at the extreme left). The other numbers keep their order. A step that would not change the line "
    "is skipped.\n\nInput: " + line(INP) + "\n\nWhich of the following is Step II?", line(st[1]),
    [line(st[0]), line(st[2]), line([92, 81, 56, 43, 34, 17][::-1])], "One number per step",
    " ".join(f"{t}." for t in step_txt(st[:2])), step_txt(st[:2]),
    why_others_wrong="The other lines are Step I, Step III and the final line reversed.", seconds=45,
    verified_by=RECOMP)

# ---- Intermediate (standalone): longest word to the left, ties broken alphabetically
INP = "plum orange fig banana kiwi grape".split()
key = lambda w: (-len(w), w)
st = run_left(INP, key)
ans = st[2][2]
assert st[2] == ["banana", "orange", "grape", "plum", "fig", "kiwi"] and ans == "grape"
mcq(IOT, WR, "Intermediate",
    "A word arrangement machine rearranges a line of words step by step. In each step it takes the longest word among "
    "those not yet arranged (if two words are equally long, the one that comes first in a dictionary) and places it "
    "immediately to the right of the words already arranged at the left end. The other words keep their order.\n\n"
    "Input: " + line(INP) + "\n\nIn Step III, which word is 3rd from the left end?", ans, ["plum", "orange", "kiwi"],
    "Length first, then dictionary order",
    "Step I: banana (6 letters, before orange) → " + line(st[0]) + ". Step II: orange → " + line(st[1]) + ". Step III: "
    "grape (5 letters) → " + line(st[2]) + ". The 3rd word from the left is grape.", step_txt(st[:3]),
    why_others_wrong="plum is 4th in Step III; orange is 2nd; kiwi is last.", seconds=70, verified_by=RECOMP)

# ---- Intermediate (standalone): mixed machine
INP = ["melon", 27, "apple", 64, "cherry", 15, "date", 48]


def mixed6(items):
    """Each step: (1) the alphabetically first unarranged word goes to the left end, after the words already placed
    there; (2) the smallest unarranged number goes to the right end, before the numbers already placed there, and 5 is
    added to it."""
    words_done, nums_done, rest, steps = [], [], list(items), []
    while rest:
        ws = [x for x in rest if isinstance(x, str)]
        ns = [x for x in rest if isinstance(x, int)]
        if ws:
            w_ = min(ws)
            rest.remove(w_)
            words_done.append(w_)
        if ns:
            n_ = min(ns)
            rest.remove(n_)
            nums_done.insert(0, n_ + 5)
        steps.append(words_done + rest + nums_done)
    return steps


st = mixed6(INP)
assert st[1] == ["apple", "cherry", "melon", 64, "date", 48, 32, 20]
assert st[-1] == ["apple", "cherry", "date", "melon", 69, 53, 32, 20]
ans = st[1][-3]
assert ans == 48
mcq(IOT, MM, "Intermediate",
    "A word and number arrangement machine rearranges a line step by step. In each step it makes two moves: (1) among "
    "the words not yet arranged, it takes the one that comes first in a dictionary and places it at the left end, just "
    "after the words already arranged there; (2) among the numbers not yet arranged, it takes the smallest, adds 5 to "
    "it, and places the result at the right end, just before the numbers already arranged there. Everything else keeps "
    "its order.\n\nInput: " + line(INP) + "\n\nIn Step II, which element is 3rd from the right end?", str(ans),
    ["32", "64", "20"], "Track both moves in each step",
    "Step I: apple to the left; 15 + 5 = 20 to the right → " + line(st[0]) + ". Step II: cherry to the left; 27 + 5 = 32 "
    "to the right → " + line(st[1]) + ". From the right: 20, 32, 48 — the 3rd is 48.", step_txt(st[:2]),
    why_others_wrong="32 is 2nd from the right and 20 1st; 64 is 4th from the right.", natural=int, seconds=80,
    verified_by=RECOMP)

# ================================================================================================ DATA SUFFICIENCY
TS, THS = "Two-statement", "Three-statement"


def ds_opts(ans):
    keys = "ABET" if ans == "E" else "ABNT"
    assert ans in keys
    return [DS2[k] for k in keys]


def ds_q(diff, sub, text, models, s1, s2, answer, expected, concept, expl, steps, seconds=50):
    got = ds2(models, s1, s2, answer)
    assert got == expected, (text, got)
    return fixed(DSF, sub, diff, DS_HEAD + text, ds_opts(expected), DS2[expected], concept, expl, steps,
                 seconds=seconds, verified_by=ENUM)


DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
# Basic
models = [{"d1": d} for d in range(7)]  # weekday index (Monday = 0) of 1 August
d15 = lambda m: (m["d1"] + 14) % 7
ds_q("Basic", TS, "Question: On which day of the week was 15 August of a certain year?\n\nI. 10 August of that year was "
     "a Monday.\nII. 1 August of that year was a Saturday.", models, lambda m: (m["d1"] + 9) % 7 == 0,
     lambda m: m["d1"] == 5, d15, "E", "Each statement on its own",
     "I: 15 August is five days after Monday 10 August: Saturday. II: 15 August is exactly two weeks after Saturday "
     "1 August: Saturday. Each statement alone gives the day.",
     ["I: Monday + 5 ⇒ Saturday ⇒ sufficient", "II: Saturday + 14 ⇒ Saturday ⇒ sufficient"], seconds=45)

P4 = list("PQRS")
models = [dict(zip(P4, p)) for p in itertools.permutations(range(4))]  # larger = heavier
ds_q("Basic", TS, "Question: Among four boxes P, Q, R and S, each of a different weight, which is the heaviest?\n\n"
     "I. P is heavier than both Q and R, and S is lighter than R.\nII. Q is heavier than S only.", models,
     lambda m: m["P"] > m["Q"] and m["P"] > m["R"] and m["S"] < m["R"],
     lambda m: sum(1 for k in P4 if m[k] < m["Q"]) == 1 and m["S"] < m["Q"], lambda m: max(P4, key=m.get), "A",
     "Test each statement alone",
     "I: P is above Q and R, and S is below R, so P is above all three — sufficient. II places Q second from the "
     "bottom with S below it, but P or R could be the heaviest — not sufficient.",
     ["I: P > Q, P > R > S ⇒ P heaviest ⇒ sufficient", "II: only S below Q ⇒ P or R heaviest ⇒ not sufficient"],
     seconds=45)
# Kiran's brothers: Kiran's gender is not stated
models = []
for kg in "MF":
    for others in itertools.product("MF", repeat=3):  # up to three siblings (mother has 2 to 4 children)
        for n in range(0, 4):
            sib = list(others[:n])
            models.append({"kg": kg, "children": n + 1, "sis": sib.count("F"), "bro": sib.count("M")})
ds_q("Basic", TS, "Question: How many brothers does Kiran have?\n\nI. Kiran's mother has exactly four children, and "
     "all of them have the same father.\nII. Kiran has exactly two sisters.", models, lambda m: m["children"] == 4,
     lambda m: m["sis"] == 2, lambda m: m["bro"], "T", "Siblings = children − 1, whatever Kiran's gender",
     "I gives Kiran three siblings but not how many are boys. II gives two sisters but not the total. Together: three "
     "siblings, two of them sisters, so Kiran has exactly one brother — whether Kiran is a boy or a girl.",
     ["I: 3 siblings, genders unknown ⇒ not sufficient", "II: total unknown ⇒ not sufficient",
      "Together: 3 − 2 = 1 brother"], seconds=50)
models = [{"m": m} for m in range(1, 13)]
ds_q("Basic", TS, "Question: In which month was Rohit born?\n\nI. Rohit was born in a month that has 31 days and comes "
     "immediately after a month that has 30 days.\nII. Rohit was born in the month immediately before November.",
     models, lambda x: MDAYS[x["m"]] == 31 and MDAYS[(x["m"] - 2) % 12 + 1] == 30, lambda x: x["m"] == 10,
     lambda x: x["m"], "B", "Test each statement alone",
     "I fits May, July, October and December — not sufficient. II: the month before November is October — "
     "sufficient.", ["I: May, July, October, December ⇒ not sufficient", "II: October ⇒ sufficient"], seconds=45)
# Intermediate
models = [{"s": s, "t": t} for s in range(1, 80) for t in range(1, 80)]
ds_q("Intermediate", TS, "Question: What is Sahil's present age?\n\nI. Sahil is 4 years older than Tia, and the sum of "
     "their present ages is 30 years.\nII. Five years ago, Tia's age was two-thirds of Sahil's age at that time.", models,
     lambda m: m["s"] == m["t"] + 4 and m["s"] + m["t"] == 30, lambda m: 3 * (m["t"] - 5) == 2 * (m["s"] - 5),
     lambda m: m["s"], "A", "Two equations fix two unknowns; one equation does not",
     "I: S − T = 4 and S + T = 30 give S = 17 — sufficient. II: 3(T − 5) = 2(S − 5) is one equation in two "
     "unknowns (e.g. S = 11, T = 9 or S = 17, T = 13) — not sufficient.",
     ["I: S = (30 + 4) ÷ 2 = 17 ⇒ sufficient", "II: one equation, many solutions ⇒ not sufficient"], seconds=60)
models = [{"d": d} for d in range(7)]
ds_q("Intermediate", TS, "Question: On which day of a certain week (Monday to Sunday) did Meera visit the bank?\n\n"
     "I. Meera visited the bank on a day after Tuesday but before Friday.\nII. Meera did not visit on a Wednesday or on "
     "a weekend (Saturday or Sunday).", models, lambda m: 1 < m["d"] < 4, lambda m: m["d"] not in (2, 5, 6),
     lambda m: m["d"], "T", "Intersect the two lists",
     "I: Wednesday or Thursday. II: Monday, Tuesday, Thursday or Friday. Together only Thursday remains.",
     ["I: Wednesday, Thursday ⇒ not sufficient", "II: Monday, Tuesday, Thursday, Friday ⇒ not sufficient",
      "Together: Thursday"], seconds=55)
models = [{"n": n, "o": o} for n in range(1, 51) for o in range(1, 51) if n != o]
ds_q("Intermediate", TS, "Question: In a class of 50 students with no ties, what is Nikhil's rank from the bottom?\n\n"
     "I. Nikhil is 7 ranks below Omkar, who is 20th from the top.\nII. Exactly 23 students rank below Nikhil.", models,
     lambda m: m["o"] == 20 and m["n"] == 27, lambda m: 50 - m["n"] == 23, lambda m: 50 - m["n"] + 1, "E",
     "Each statement on its own",
     "I: Nikhil is 27th from the top, so 50 − 27 + 1 = 24th from the bottom. II: 23 students below him makes him 24th "
     "from the bottom. Each statement alone is enough.",
     ["I: 27th from top ⇒ 24th from bottom", "II: 23 below ⇒ 24th from bottom"], seconds=55)

# ---- Advanced: three statements
DS3H = lambda keys: [DS3[k_] for k_ in keys]
# A1: two-digit number
models = [{"n": n} for n in range(10, 100)]
fns = [lambda m: sum(dg(m["n"])) == 9, lambda m: m["n"] > 50, lambda m: dg(m["n"])[0] == 2 * dg(m["n"])[1]]
got = ds3(models, fns, lambda m: m["n"])
assert got == "I+III"
fixed(DSF, THS, "Advanced", DS3_HEAD + "Question: What is the two-digit number N?\n\nI. The sum of the digits of N is 9."
      "\nII. N is greater than 50.\nIII. The tens digit of N is twice its units digit.",
      DS3H(("I+II", "I+III", "ALL", "NONE")), DS3["I+III"], "Find the smallest sufficient pair",
      "I + III: t + u = 9 and t = 2u give u = 3, t = 6: N = 63 — sufficient. I + II allows 54, 63, 72, 81, 90; II + III "
      "allows 63 and 84. No single statement is enough.",
      ["I + III ⇒ 63 ⇒ sufficient", "I + II ⇒ 54, 63, 72, 81, 90", "II + III ⇒ 63, 84"], seconds=75, verified_by=ENUM)
# A2: floors
P5 = list("ABCDE")
models = [dict(zip(P5, p)) for p in itertools.permutations(range(1, 6))]
fns = [lambda m: m["A"] == m["B"] + 2, lambda m: m["C"] == 5 and m["D"] < m["E"], lambda m: m["B"] == 1]
got = ds3(models, fns, lambda m: next(k for k in P5 if m[k] == 3))
assert got == "I+III"
fixed(DSF, THS, "Advanced", DS3_HEAD + "Question: Five persons A, B, C, D and E live on the five floors of a building, "
      "one on each floor (floor 1 is the lowermost). Who lives on floor 3?\n\nI. A lives two floors above B.\nII. C "
      "lives on the topmost floor, and D lives below E.\nIII. B lives on the lowermost floor.",
      DS3H(("I+II", "I+III", "II+III", "NONE")), DS3["I+III"], "Pair the statements and test each pair",
      "I + III: B = 1, so A = 3 — sufficient. I + II: B and A could be 1 and 3 or 2 and 4, so floor 3 could be A or "
      "D/E. II + III: C = 5, B = 1, and A, D, E fill 2–4 in more than one way. No statement alone is enough.",
      ["I + III ⇒ A = 3", "I + II and II + III leave several arrangements"], seconds=80, verified_by=ENUM)
# A3: direction
models = [{"dx": dx, "dy": dy} for dx in range(-12, 13) for dy in range(-12, 13) if (dx, dy) != (0, 0)]
fns = [lambda m: m["dy"] == 5, lambda m: m["dx"] == -12 or m["dx"] == 12,
       lambda m: m["dx"] * m["dx"] + m["dy"] * m["dy"] == 169 and m["dx"] < 0]
got = ds3(models, fns, lambda m: compass(m["dx"], m["dy"]))
assert got == "I+III", got
fixed(DSF, THS, "Advanced", DS3_HEAD + "Question: In which direction is point P from point Q?\n\nI. P is 5 m to the "
      "north of the east–west line through Q.\nII. P is 12 m from the north–south line through Q.\nIII. The straight-"
      "line distance PQ is 13 m, and P lies to the west of Q.",
      DS3H(("I+II", "I+III", "ANY2", "NONE")), DS3["I+III"], "Direction needs the sign of both displacements",
      "I fixes 'north' (5 m) and III fixes 'west'; together P is north-west of Q — sufficient. II gives only the size of "
      "the east–west gap, so I + II leaves north-east or north-west. II + III: P is 12 m west and, from 13 m, 5 m north "
      "or south — not sufficient. No statement alone is enough.",
      ["I: north component; III: west, |PQ| = 13", "I + III ⇒ North-West", "I + II: east or west unknown",
       "II + III: north or south unknown"], seconds=85, verified_by=ENUM)
# A4: circular seating, who sits opposite A
P6c = list("ABCDEF")
models = [dict(zip(P6c, (0,) + p)) for p in itertools.permutations(range(1, 6))]
fns = [lambda m: m["B"] == 1 and m["C"] == (m["E"] + 2) % 6, lambda m: (m["D"] - m["E"]) % 6 == 1,
       lambda m: m["F"] in (2, 4)]
got = ds3(models, fns, lambda m: next(k for k in P6c if m[k] == 3))
assert got == "I+III", got
fixed(DSF, THS, "Advanced", DS3_HEAD + "Question: Six friends A, B, C, D, E and F sit around a circular table, equally "
      "spaced and facing the centre. Who sits opposite A?\n\nI. B sits immediately to the right of A, and C sits second "
      "to the right of E.\nII. D sits immediately to the right of E.\nIII. F sits second to the right or second to the "
      "left of A.", DS3H(("I+II", "I+III", "ALL", "NONE")), DS3["I+III"], "Test every pair before using all three",
      "Number the seats 0–5 to the right (anticlockwise) from A = 0. I + III: B = 1 and F = 2 or 4. If F = 2, E and C "
      "(two apart) must be 3 and 5, leaving D = 4; if F = 4, E and C must again be 3 and 5, leaving D = 2. Either way E "
      "is at seat 3, opposite A — sufficient. I + II: E, D, C take three consecutive seats among 2–5, so E is at 2 or "
      "3 — not fixed. II + III do not place B or C. No single statement is enough.",
      ["I + III: F 2 ⇒ E 3, D 4, C 5; F 4 ⇒ E 3, C 5, D 2 ⇒ E opposite A", "I + II: E at 2 or 3 ⇒ not sufficient",
       "II + III: not sufficient"], seconds=90, verified_by=ENUM)
# A5: box stack
B5_ = list("JKLMN")
models = [dict(zip(B5_, p)) for p in itertools.permutations(range(1, 6))]
fns = [lambda m: m["K"] == m["J"] + 1, lambda m: m["L"] == 5 or m["L"] == 1, lambda m: m["M"] < m["N"]]
got = ds3(models, fns, lambda m: next(k for k in B5_ if m[k] == 5))
assert got == "NONE", got
fixed(DSF, THS, "Advanced", DS3_HEAD + "Question: Five boxes J, K, L, M and N are kept one above another in a single "
      "stack (position 1 is the bottom). Which box is at the top?\n\nI. Box K is kept immediately above box J.\nII. "
      "Box L is kept either at the top or at the bottom.\nIII. Box M is kept somewhere below box N.",
      DS3H(("I+II", "II+III", "ALL", "NONE")), DS3["NONE"], "Check whether even all three fix the answer",
      "With all three statements, L could be at the top (for example J, K, M, N, L from the bottom) or at the bottom "
      "(for example L, M, J, K, N, with N on top, or L, J, K, M, N). The top box is not fixed, so even all three "
      "statements together are not sufficient.",
      ["All three: L top ⇒ top = L", "All three: L bottom ⇒ top = N or K", "⇒ not sufficient"], seconds=85,
      verified_by=ENUM)

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


asm("Intermediate", "A bank has decided to send monthly account statements to its customers by e-mail instead of by "
    "post from the next quarter.",
    "Most of the bank's customers can receive and read e-mail.",
    "The postal department has stopped delivering letters.", A_I,
    "Switching statements to e-mail makes sense only if customers can receive e-mail (I). The decision does not "
    "depend on the post having stopped working; banks move to e-mail for cost and speed, so II is not assumed.",
    ["E-mail statements ⇒ customers can receive e-mail: I implicit", "No need for the post to have stopped: II not "
                                                                     "implicit"],
    "Only II and Both accept a claim the decision does not rely on; Neither ignores the basis of the change.")
asm("Intermediate", "Notice at a petrol pump: \"Switch off your mobile phone while your vehicle is being refuelled.\"",
    "Using a mobile phone during refuelling is considered a safety risk.",
    "People who come to the petrol pump will read and follow the notice.", A_B,
    "A safety instruction is issued only if the activity is seen as risky (I), and a notice is put up only if the "
    "authority expects people to read and act on it (II).",
    ["Instruction ⇒ phone use seen as risky: I", "Notice displayed ⇒ expected to be read and obeyed: II"],
    "Each 'Only' option drops one of two assumptions every such notice rests on.")
asm("Intermediate", "The state government has decided to train 5,000 village youth as solar-panel technicians this "
    "year.",
    "There will be work for trained solar-panel technicians.",
    "Village youth are not interested in any other kind of work.", A_I,
    "Training people for a trade is sensible only if there will be work for them (I). The plan says nothing about "
    "other kinds of work, and it does not require village youth to reject every other job (II).",
    ["Training for a trade ⇒ demand for the trade expected: I", "Other jobs are irrelevant to the plan: II not "
                                                                "implicit"],
    "Only II and Both read an extreme claim into the plan; Neither ignores why the training is offered.")
asm("Intermediate", "Advertisement of a language institute: \"Learn to speak English fluently in 30 days — or get "
    "your full fee back.\"",
    "Some people want to learn to speak English.",
    "Every person who joins the course will speak English fluently within 30 days.", A_I,
    "An institute advertises a course only if it expects some people to want it (I). The refund offer itself shows "
    "that the institute does not take for granted that every learner will succeed, so II is not implicit.",
    ["Advertising a course ⇒ demand exists: I", "Refund promise ⇒ success for all is not assumed: II not implicit"],
    "Only II and Both treat a promise of refunds as a guarantee of success; Neither ignores the purpose of an "
    "advertisement.")
asm("Intermediate", "The city traffic police will install cameras at 50 busy junctions to fine drivers who jump red "
    "lights.",
    "Some drivers jump red lights at these junctions.",
    "The cameras will be able to identify the vehicles that jump red lights.", A_B,
    "The plan is aimed at drivers who jump red lights, so it takes for granted that this happens at these junctions "
    "(I); fining them through cameras works only if the cameras can identify the vehicles (II).",
    ["Target behaviour exists: I", "Fines through cameras ⇒ vehicles can be identified: II"],
    "Each 'Only' option drops one of the two things the plan needs.")
asm("Intermediate", "A bank has extended the last date for paying the annual locker rent from 31 March to 30 April.",
    "All the locker holders had already paid the rent by 31 March.",
    "The bank will extend the last date again after 30 April.", A_N,
    "Extending a deadline makes sense only if some holders had not yet paid, so I goes against the statement. Nothing "
    "in a single extension implies a further one, so II is not implicit either.",
    ["Extension ⇒ some had not paid ⇒ I contradicts the statement", "A further extension is not implied ⇒ II not "
                                                                       "implicit"],
    "I is the opposite of what the extension suggests, and II is a guess about the future; so neither is implicit.")

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


assert 120 - 75 == 45 and 75 / 120 > 0.6
scq("Intermediate", INF, "A hostel has 120 students. Every student has opted for exactly one of two meal plans, "
    "vegetarian or non-vegetarian, and 75 students have opted for the vegetarian plan.",
    "45 students have opted for the non-vegetarian plan.",
    "More than 60% of the students have opted for the vegetarian plan.", BOTH,
    "Each student has exactly one plan, so 120 − 75 = 45 chose the non-vegetarian plan (I). 75 ÷ 120 = 62.5%, which "
    "is more than 60% (II).", ["120 − 75 = 45 ⇒ I", "75 ÷ 120 = 62.5% > 60% ⇒ II"],
    "Each 'Only' option drops one of two direct calculations; Neither ignores both.", seconds=45)

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


def ceq(diff, sub, s1, s2, answer, explanation, steps, why, seconds=45):
    keys = [k_ for k_ in "ABCDE" if k_ != "C"]
    q_ = fixed(CAE, sub, diff, CE_HEAD + f"I. {s1}\nII. {s2}", [CE[k_] for k_ in keys], CE[answer],
               "Cause and effect: look for a direct link, a shared trigger, or none", explanation, steps,
               why_others_wrong=why, seconds=seconds)
    VERBAL_IDS.append(q_["question_id"])


ceq("Basic", IND, "A water pipeline running under the market road burst early on Tuesday morning.",
    "The market road was under knee-deep water for several hours on Tuesday.", "A",
    "Water escaping from a burst pipeline under the road floods the road. I directly explains II, and the timing "
    "matches.", ["I: pipeline under the road bursts", "II: the same road floods the same day", "I → II"],
    "A flooded road cannot burst a pipeline, so B is impossible; no third event is needed.", seconds=35)
ceq("Basic", IND, "The college library extended its closing time from 6 pm to 10 pm for the examination month.",
    "Students had asked the college for a quiet place to study in the evenings during the examination month, since "
    "their hostels have no study rooms.", "B",
    "The students' request for an evening study place is the reason the library stays open later. II is the cause and "
    "I its effect.", ["II: demand for an evening study place", "I: library opens till 10 pm", "II → I"],
    "Longer library hours cannot create a request that was made because the hostels lack study rooms, so A fails.",
    seconds=40)
ceq("Basic", COM, "Schools in the district changed their timings this week so that classes end before 11 am.",
    "Hospitals in the district set up special wards for heatstroke patients this week.", "E",
    "Earlier school closing does not make hospitals open heatstroke wards, and heatstroke wards do not change school "
    "timings. Both are typical responses to one event — a severe heatwave in the district this week.",
    ["No direct link between the two", "Both are standard responses to extreme heat", "⇒ effects of a common cause"],
    "Effects of independent causes would need two unrelated reasons in the same week; one heatwave explains both.",
    seconds=40)
ceq("Basic", IND, "The municipal corporation repainted all the zebra crossings in the city.",
    "A private bank launched a new credit card for college students.", "D",
    "Repainting road markings follows from the corporation's road-safety work; a new card follows from a bank's "
    "business plans. Neither explains the other, and no single event explains both.",
    ["I: outcome of civic road maintenance", "II: outcome of a bank's product decision", "⇒ independent causes"],
    "A common cause would need one event behind both a civic road job and a bank's product launch; nothing suggests "
    "one.", seconds=35)
ceq("Advanced", IND, "The central bank sharply lowered, with immediate effect, the maximum amount that any one bank may "
    "lend to a single borrower.",
    "Several large companies that had been borrowing heavily from a single bank began spreading their borrowing "
    "across many banks.", "A",
    "Once one bank may lend a large borrower only a smaller amount, a company that needs the same total credit must go "
    "to several banks. The new limit (I) directly explains the companies' change (II).",
    ["I: a lower single-borrower limit for each bank", "II: big borrowers split loans across banks",
     "Limit forces the split ⇒ I is the cause"],
    "Companies spreading their loans cannot have caused a regulator's limit that took effect immediately before it, "
    "so B fails; no outside event is needed.", seconds=60)
ceq("Advanced", IND, "The state's sugar mills ended their cane-crushing season a month earlier than usual this year.",
    "Sugarcane output in the state fell by a third this year because of a severe drought.", "B",
    "Mills crush the cane that farmers supply; with a third less cane, they run out of cane and close the season early. "
    "The drought-hit output (II) explains the early end (I).",
    ["II: one-third less cane, caused by drought", "I: mills stop crushing a month early", "Less cane → shorter "
                                                                                              "season ⇒ II is the cause"],
    "An early end to crushing cannot reduce the cane grown in a drought year, so A fails; the drought is already part "
    "of II, so no separate common cause is needed.", seconds=60)
ceq("Advanced", COM, "Banks in the state reported a sharp rise in withdrawals of cash in the week before Diwali.",
    "Shops in the state's markets reported record sales of clothes and sweets in the week before Diwali.", "E",
    "People withdraw cash and shop heavily for the same reason — festival buying before Diwali. Cash withdrawals do "
    "not by themselves create sales (people could withdraw and not spend), and shop sales do not cause withdrawals; "
    "both follow from the festival season.",
    ["No direct cause: withdrawals ≠ purchases", "Both are typical of pre-festival spending",
     "⇒ effects of a common cause"],
    "A or B would need one statement to produce the other; D would need two unrelated reasons, though both are tied "
    "to the same festival week.", seconds=60)
ceq("Advanced", IND, "The city's metro rail recorded its highest-ever daily ridership on Monday.",
    "A television channel recorded its highest-ever viewership for a cooking show on Monday night.", "D",
    "Metro ridership depends on travel needs in the city; a cooking show's ratings depend on the programme and its "
    "audience across the country. Sharing a date does not link them, and no single event is suggested behind both.",
    ["I: result of travel demand on Monday", "II: result of a TV programme's appeal", "Same day ≠ same cause ⇒ D"],
    "A or B would need metro travel to drive TV viewing or vice versa; E would need one event behind both, and none "
    "is indicated.", seconds=55)

# ================================================================================================ CRITICAL REASONING
CRT = "Critical Reasoning"
SW_, CA_, INFP = "Strengthen and weaken", "Course of action", "Inference from a passage"


def crq(diff, sub, text, correct, wrongs, concept, explanation, steps, why, seconds=60):
    q_ = mcq(CRT, sub, diff, text, correct, wrongs, concept, explanation, steps, why_others_wrong=why, seconds=seconds)
    VERBAL_IDS.append(q_["question_id"])


# ---- Basic
crq("Basic", CA_, "Statement: Customers of a bank branch complain that the branch's only drinking-water cooler has not "
    "worked for a month, and elderly customers who wait for long periods have no water to drink.\n\nWhich of the "
    "following is the most appropriate course of action?",
    "The branch should get the water cooler repaired or replaced without delay",
    ["The branch should ask customers not to visit on weekdays", "The branch should stop elderly customers from "
                                                                  "waiting inside", "The branch should remove the "
                                                                                    "water cooler permanently"],
    "A course of action should remove the stated problem directly",
    "The problem is a broken cooler; repairing or replacing it solves it directly and quickly.",
    ["Problem: no working water cooler", "Remedy: repair or replace it"],
    "Restricting visits or waiting is impractical and unfair, and removing the cooler makes things worse.", seconds=30)
crq("Basic", CA_, "Statement: A survey found that many primary-school students in a town carry schoolbags weighing "
    "almost a third of their own body weight, and several complain of back pain.\n\nWhich of the following is the most "
    "appropriate course of action?",
    "Schools should set a daily timetable so that students carry only the books needed that day, and provide lockers "
    "for the rest",
    ["Schools should stop giving any books to primary students", "Parents should carry the bags for their children "
                                                                   "every day", "Students with back pain should "
                                                                                 "be asked to stay at home"],
    "Practical, targeted remedy", "Carrying only the day's books and keeping the rest in lockers lightens the bags "
                                  "directly, without harming studies.",
    ["Cause: too many books carried daily", "Remedy: day-wise books + lockers"],
    "Removing books harms learning; parents carrying bags or children staying home do not address the cause.",
    seconds=35)
crq("Basic", INFP, "Passage: The town's only bridge across the river will be closed for repairs from 1 March to "
    "15 March. During this period a ferry will carry people across the river every 30 minutes from 6 am to 9 pm. "
    "There is no other way to cross the river near the town.\n\nWhich of the following can be inferred from the "
    "passage?",
    "During the closure, a person in the town who needs to cross the river at 11 pm will not be able to do so",
    ["The ferry will continue to run after the bridge reopens", "The repairs will be completed before 15 March",
     "Most people in the town cross the river every day"], "An inference must follow from the passage alone",
    "Between 1 and 15 March the bridge is closed, the ferry runs only from 6 am to 9 pm, and there is no other way to "
    "cross. So at 11 pm nobody can cross.",
    ["Bridge closed; ferry 6 am–9 pm; no other crossing", "11 pm is outside ferry hours ⇒ cannot cross"],
    "The passage says nothing about the ferry after the closure, early completion, or how many people cross daily.",
    seconds=40)
crq("Basic", SW_, "Argument: Building speed breakers near the school gate will reduce accidents involving students.\n\n"
    "Which of the following, if true, most strengthens the argument?",
    "Most accidents near the school gate in the past year involved vehicles moving at high speed",
    ["The school gate is painted in bright colours", "Speed breakers are cheap to build",
     "Some students come to school by bus"], "Strengthen: show that the remedy targets the actual cause",
    "Speed breakers slow vehicles. If the accidents near the gate were mostly caused by fast vehicles, slowing them "
    "should reduce accidents.", ["Remedy: slower vehicles", "Strengthener: accidents were speed-related"],
    "The gate's colour, the cost of speed breakers and how some students travel do not show that slowing traffic "
    "will cut accidents.", seconds=35)
crq("Basic", INFP, "Passage: Every bus on route 7 stops at the district hospital. The 8:15 am bus from the bus stand "
    "runs on route 7.\n\nWhich of the following can be inferred from the passage?",
    "The 8:15 am bus stops at the district hospital",
    ["Every bus that stops at the district hospital runs on route 7", "The 8:15 am bus is always crowded",
     "No bus on any other route stops at the district hospital"], "Apply a general rule to a member of the group",
    "All route-7 buses stop at the hospital, and the 8:15 am bus is a route-7 bus, so it stops at the hospital.",
    ["All route 7 buses → hospital", "8:15 am bus ∈ route 7 ⇒ stops at hospital"],
    "The passage does not say that only route-7 buses stop there, and says nothing about crowding.", seconds=30)
crq("Basic", CA_, "Statement: In a village, many wells have dried up because groundwater is being pumped out faster "
    "than rainwater can refill it.\n\nWhich of the following is the most appropriate course of action?",
    "Encourage rainwater harvesting and regulate the digging of new borewells in the village",
    ["Dig all the existing wells deeper", "Ask the villagers to leave the village", "Ban the use of water for all "
                                                                                     "farming"],
    "Address both sides of the imbalance",
    "The wells dry because withdrawal exceeds recharge. Rainwater harvesting adds recharge and regulating borewells "
    "limits withdrawal, so both sides of the imbalance are addressed.",
    ["Cause: pumping > recharge", "Remedy: more recharge, controlled pumping"],
    "Deeper wells speed up depletion; moving villagers away or banning all farming is impractical and extreme.",
    seconds=35)
# ---- Intermediate
assert 5 / 3000 > 40 / 40000
crq("Intermediate", SW_, "Argument: The new online examination portal is more reliable than the old one, because "
    "complaints about the portal crashing on exam day fell from 40 last year to 5 this year.\n\nWhich of the "
    "following, if true, most seriously weakens the argument?",
    "About 40,000 candidates used the portal last year, but only about 3,000 used it this year",
    ["The new portal has a more attractive design", "The new portal was built by a well-known company",
     "Some candidates did not know how to file a complaint"], "Weaken: compare rates, not raw counts",
    "40 complaints from 40,000 users is 0.1%; 5 from 3,000 users is about 0.17%. The complaint rate actually rose, so "
    "the fall in the number of complaints does not show greater reliability.",
    ["Last year: 40 ÷ 40,000 = 0.1%", "This year: 5 ÷ 3,000 ≈ 0.17%", "Rate rose ⇒ evidence fails"],
    "Design and the builder's reputation say nothing about crashes; not knowing how to complain applies to both "
    "years and does not explain the change.", seconds=70)
crq("Intermediate", SW_, "Argument: Giving free city-bus passes to senior citizens will reduce the number of private "
    "cars on the city's roads.\n\nWhich of the following, if true, most strengthens the argument?",
    "A survey found that most senior citizens now travel in private cars driven by family members, and most of them "
    "said they would switch to buses if travel were free",
    ["Bus drivers in the city are well trained", "Many senior citizens enjoy walking in parks",
     "The city plans to buy more buses next year"], "Strengthen: show that the target group will change behaviour",
    "The argument needs senior citizens who now use cars to switch to buses. The survey shows that they now use cars "
    "and would switch if the bus were free.", ["Link needed: car users switch to buses", "Survey supplies both parts"],
    "Driver training, walking habits and future bus purchases do not show that car trips will be replaced.",
    seconds=60)
assert (1200 - 300) // 3 == 300
crq("Intermediate", INFP, "Passage: A bank branch has 1,200 savings accounts, of which 300 are dormant. Exactly one-"
    "third of the active (non-dormant) accounts have a debit card linked to them.\n\nWhich of the following can be "
    "inferred from the passage?",
    "Exactly 300 active accounts have a debit card linked to them",
    ["Exactly 400 accounts have a debit card linked to them", "No dormant account has a debit card linked to it",
     "At most 300 accounts in the branch have a debit card linked to them"], "Compute only what the data fix",
    "Active accounts = 1,200 − 300 = 900; one-third of them is 300. The passage is silent about cards on dormant "
    "accounts, so totals for all accounts cannot be fixed.",
    ["Active = 900", "900 ÷ 3 = 300 active accounts with cards", "Dormant accounts' cards unknown"],
    "400 takes one-third of all 1,200 accounts; the other two options make claims about dormant accounts, which the "
    "passage does not cover.", seconds=60)
crq("Intermediate", CA_, "Statement: An inspection found that a government hospital ran short of oxygen cylinders "
    "several times this year because the supplier stopped deliveries after its bills remained unpaid for months.\n\n"
    "Which of the following is the most appropriate course of action?",
    "Clear the supplier's pending bills, pay future bills on a fixed schedule, and monitor the cylinder stock "
    "regularly",
    ["Stop admitting patients who may need oxygen", "Blacklist the supplier for stopping deliveries",
     "Ask patients' families to bring their own cylinders"], "Remove the root cause and prevent a repeat",
    "Deliveries stopped because of unpaid bills. Paying the dues restores supply, a payment schedule prevents a repeat, "
    "and stock monitoring catches shortages early.", ["Cause: unpaid bills", "Remedy: pay, schedule, monitor"],
    "Refusing patients or burdening families is harmful; blacklisting the supplier punishes it for the hospital's own "
    "failure to pay and does not secure supply.", seconds=60)
assert 60 * 1 / (80 - 60) == 3
crq("Intermediate", INFP, "Passage: Train A leaves a station at 7:00 am and runs at a steady 60 km/h. Train B leaves "
    "the same station at 8:00 am on a parallel track in the same direction and runs at a steady 80 km/h. Neither "
    "train stops.\n\nWhich of the following can be inferred from the passage?", "Train B draws level with train A at "
                                                                               "11:00 am",
    ["Train B draws level with train A at 10:00 am", "Train B never catches up with train A",
     "Train B draws level with train A at 12:00 noon"], "Head start ÷ relative speed",
    "At 8:00 am train A is 60 km ahead. B gains 80 − 60 = 20 km every hour, so it closes the gap in 60 ÷ 20 = 3 hours: "
    "at 11:00 am.", ["Head start = 60 km", "Relative speed = 20 km/h", "60 ÷ 20 = 3 h after 8:00 ⇒ 11:00 am"],
    "10:00 am uses a 2-hour catch-up; noon adds an extra hour; B is faster, so it must catch up.", seconds=60)
crq("Intermediate", SW_, "Argument: Pupils who eat breakfast at home score higher in tests than pupils who do not. "
    "So the school's new free-breakfast scheme will raise the test scores of the pupils who now skip breakfast.\n\n"
    "Which of the following, if true, most seriously weakens the argument?",
    "In this school, the pupils who eat breakfast at home come mostly from families that also pay for private "
    "tuition, while those who skip breakfast mostly do not get tuition",
    ["The free breakfast will include fruit and milk", "Some teachers also eat breakfast at school",
     "The scheme will be paid for by a local trust"], "Weaken: offer another explanation for the correlation",
    "If breakfast-eaters also get private tuition, their higher scores may come from tuition rather than from "
    "breakfast. Then giving breakfast alone need not raise the others' scores.",
    ["Evidence: breakfast-eaters score higher", "Alternative cause: tuition", "⇒ breakfast may not be what helps"],
    "The menu, teachers' meals and the source of funding do not touch the link between breakfast and scores.",
    seconds=70)
crq("Intermediate", SW_, "Argument: A company says that its new four-day work week has made its staff more "
    "productive, because the company's weekly output has stayed the same although working hours fell by a fifth.\n\n"
    "Which of the following, if true, most strengthens the argument?",
    "The company measured weekly output in the same way before and after the change, and it did not add staff or "
    "machines during that period",
    ["Most employees said they liked the four-day week", "Other companies in the city still work five days a week",
     "The company's office is close to a metro station"], "Strengthen: rule out other explanations for steady output",
    "Same output from fewer hours means more output per hour only if nothing else changed. Ruling out new staff, new "
    "machines and a change in how output is measured supports the claim.",
    ["Claim: output per hour rose", "Strengthener: no other change could explain steady output"],
    "Liking the new week, other firms' schedules and the office's location do not bear on output per hour.",
    seconds=65)
# ---- Advanced
crq("Advanced", SW_, "Argument: District X has more road accidents every year than any other district of the state. "
    "This shows that drivers in District X are the most careless in the state.\n\nWhich of the following, if true, "
    "most seriously weakens the argument?",
    "District X has by far the most vehicles and the longest road network in the state, and its accidents per 10,000 "
    "vehicles are below the state average",
    ["District X has the state's largest bus depot", "Most accidents in District X happen at night",
     "District X's traffic police were given new uniforms last year"], "Weaken: totals versus rates",
    "A larger number of accidents may simply reflect far more vehicles and roads. If the accident rate per vehicle is "
    "below the state average, X's drivers are, if anything, less accident-prone than average.",
    ["Evidence: highest total accidents", "Weakener: highest exposure, below-average rate",
     "⇒ totals do not show carelessness"],
    "A bus depot, night-time accidents and new uniforms do not compare the care taken by drivers across districts.",
    seconds=80)
r0, r1 = 1.0, 0.9 / 1.1
assert r1 < r0 and abs(1 - r1 / r0 - 0.10) > 0.05
crq("Advanced", INFP, "Passage: A bank's gross NPA ratio is its gross non-performing assets divided by its total loans. "
    "Over the last year, Bank Y's gross non-performing assets fell by 10%, while its total loans grew by 10%.\n\n"
    "Which of the following must be true?", "Bank Y's gross NPA ratio fell during the year",
    ["Bank Y's gross NPA ratio fell by exactly 10%", "Bank Y's net profit rose during the year",
     "Bank Y wrote off some of its bad loans during the year"], "Ratio = numerator ÷ denominator",
    "The numerator was multiplied by 0.9 and the denominator by 1.1, so the ratio became 0.9 ÷ 1.1 ≈ 0.82 of its old "
    "value — a fall of about 18%. It certainly fell, but not by exactly 10%. Profit and write-offs are not covered.",
    ["New ratio = old × 0.9 ÷ 1.1 ≈ 0.82 × old", "⇒ the ratio fell (by about 18%)",
     "Profit and write-offs: no information"],
    "'Exactly 10%' ignores the growth in loans; profit and write-offs are not given in the passage.", seconds=80)

# Blind check (2026-11-06): a separate, fresh solver answered all 30 items from a key-free dump (--dump-verbal) and
# matched every key. No item was changed afterwards.
BLIND_OK = {f"BANK_REAS_{n:06d}" for n in range(1175, 1205)}
assert BLIND_OK == set(VERBAL_IDS)
# ================================================================================================ WRITE
plan = json.loads((ROOT / "batches" / "plans" / "BATCH_006_plan.json").read_text(encoding="utf-8"))
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
        "batch_id": "BATCH_006",
        "created_at": TODAY,
        "notes": ("Reasoning Ability part of BATCH_006: 200 original questions (60 Basic, 80 Intermediate, 60 "
                  "Advanced) built by tools/batch_006/reasoning.py. New puzzle structures and noun sets. Puzzles are "
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
