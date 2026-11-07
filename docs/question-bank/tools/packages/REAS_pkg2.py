"""Builds the Reasoning Ability topic package 2 (Month and Date-Based Puzzles, Puzzles (Other), Syllogism,
Inequality) for BATCH_007 to BATCH_010: batches/parts/frag/BATCH_<NNN>_REAS_pkg2.json.

Method (helpers copied from tools/batch_005/reasoning.py, which cannot be imported without rebuilding batch 5):
- puzzles: every condition is written once as (text, variables, test); the text goes into the stimulus or the
  question and the test into an exhaustive backtracking search that must return exactly one arrangement. Every
  answer is read off that arrangement (script:brute-force-unique) or recomputed with datetime (script:recompute);
- syllogisms: every conclusion is checked over every Venn-region model of up to four sets (script:all-venn-models);
- inequalities: exhaustive search over all integer assignments with values 0..k-1 (k = number of letters), which
  realises every weak order, cross-checked with a wider range 0..k+2 (script:exhaustive-integers).
Repeat guard: syllogism nouns must not occur in any earlier REAS file (sample, parts, batch-6 builder) and each noun
is used once in the package; single-chain inequality sign patterns must be new.
The package plan (batches/plans/packages/REAS_pkg2.json) is asserted per batch: quota per topic and difficulty, ID
range and first stimulus ID. If any assertion fails, nothing is written.

    python tools/packages/REAS_pkg2.py        (run from docs/question-bank)
"""

import datetime as dt
import glob
import itertools
import json
import re
import sys
from collections import Counter
from pathlib import Path

TOOLS = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(TOOLS))
from qbank import default_mappings  # noqa: E402

ROOT = TOOLS.parent
PLAN = json.loads((ROOT / "batches" / "plans" / "packages" / "REAS_pkg2.json").read_text(encoding="utf-8"))
TODAY = "2026-11-05"
RA = "Reasoning Ability"
LETTERS = "ABCD"
BRUTE = ("script:brute-force-unique", "ai:author-solve")
RECOMP = ("script:recompute", "ai:author-solve")
VENN = ("script:all-venn-models", "ai:author-solve")
EXHAUST = ("script:exhaustive-integers", "ai:author-solve")
OPT4 = ["Only conclusion I follows", "Only conclusion II follows", "Neither conclusion I nor II follows",
        "Both conclusions I and II follow"]
EITHER = "Either conclusion I or II follows"
ONLY_I, ONLY_II, NEITHER, BOTH = OPT4
MON, OTH, SYL, INQ = "Month and Date-Based Puzzles", "Puzzles (Other)", "Syllogism", "Inequality"
MB, DB, YB = "Month-based", "Date-based", "Year-based"
DSG, CMP, DAY = "Designation", "Comparison and ordering", "Day-based"
TWO, FEW, POSS = "Two-statement", "Only a few / Only", "Possibility cases"
DIRECT, CODED = "Direct inequality", "Coded inequality"

# ------------------------------------------------------------------------------------------------ batch context
QUESTIONS, STIMULI, KEYCOUNT = [], [], Counter()
FIRST_Q = FIRST_STIM = 0
CUR = None
DONE = {}


def begin(nnn):
    global QUESTIONS, STIMULI, KEYCOUNT, FIRST_Q, FIRST_STIM, CUR
    CUR = PLAN["batches"][nnn]
    QUESTIONS, STIMULI, KEYCOUNT = [], [], Counter()
    FIRST_Q = int(CUR["question_ids"][0].split("_")[-1])
    FIRST_STIM = int(CUR["stimulus_id_start"].split("_")[-1])


def finish(nnn, notes, draft=False):
    b = PLAN["batches"][nnn]
    want = Counter({(t["topic"], d): n for t in b["topics"] for d, n in t["quota"].items() if n})
    got = Counter((x["topic"], x["difficulty"]) for x in QUESTIONS)
    subs = {t["topic"]: set(t["subtopics"]) for t in b["topics"]}
    if draft:
        print(nnn, "gaps:", {k: (want[k], got[k]) for k in set(want) | set(got) if want[k] != got[k]}, KEYCOUNT)
    else:
        assert got == want, (nnn, {k: (want[k], got[k]) for k in set(want) | set(got) if want[k] != got[k]})
    assert all(x["subtopic"] in subs[x["topic"]] for x in QUESTIONS)
    ids = [x["question_id"] for x in QUESTIONS]
    if not draft:
        assert len(ids) == b["count"] and ids[0] == b["question_ids"][0] and ids[-1] == b["question_ids"][1], ids[:1]
        assert STIMULI and STIMULI[0]["stimulus_id"] == b["stimulus_id_start"]
        n = len(QUESTIONS)
        assert all(0.18 * n <= KEYCOUNT[k] <= 0.32 * n for k in LETTERS), (nnn, KEYCOUNT)
    sets = Counter(x["stimulus_id"] for x in QUESTIONS if "stimulus_id" in x)
    assert all(3 <= sets[s["stimulus_id"]] <= 6 for s in STIMULI), (nnn, sets)
    for s in STIMULI:  # one difficulty and one topic per set
        mem = [x for x in QUESTIONS if x.get("stimulus_id") == s["stimulus_id"]]
        assert len({(x["topic"], x["difficulty"]) for x in mem}) == 1, s["stimulus_id"]
    DONE[nnn] = {"schema_version": "1.0", "batch_id": b["batch_id"], "created_at": TODAY, "notes": notes,
                 "stimuli": list(STIMULI), "questions": list(QUESTIONS)}


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


def cons_of(conds):
    """A condition is (text, vars, test) or (text, [(vars, test), ...]) when its test splits into parts."""
    out = []
    for c in conds:
        out.extend([(c[1], c[2])] if len(c) == 3 else c[1])
    return out


def each(P, make):
    """Per-person parts of a condition: make(p) -> (vars, test)."""
    return [make(p) for p in P]


def all_sols(variables, domains, conds, distinct_groups=()):
    return solve(variables, domains, cons_of(conds), distinct_groups)


def unique(variables, domains, conds, distinct_groups=()):
    sols = solve(variables, domains, cons_of(conds), distinct_groups)
    assert len(sols) == 1, f"{len(sols)} solutions: {sols[:3]}"
    return sols[0]


def place(correct, wrongs, natural=None):
    """Returns (options, key). natural=None: the correct option goes to the least-used key so far in this batch;
    natural=callable: all four options are sorted by it and the key falls where it falls."""
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
num_word = lambda n: WORDS[n]
by_num = lambda t: WORDS.index(t) if t in WORDS else float(t.split()[0])


def q(topic, subtopic, difficulty, text, options, answer, concept, explanation, steps, shortcut=None,
      why_others_wrong=None, seconds=60, stimulus=None, verified_by=("ai:author-solve", "ai:self-recheck"),
      tags=None):
    assert answer in LETTERS and len(options) == 4 and len(set(options)) == 4, (text, options)
    assert why_others_wrong, text[:80]
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
    assert correct_text in options
    return q(topic, subtopic, difficulty, text, options, LETTERS[options.index(correct_text)], concept, explanation,
             steps, **kw)


def conclusion_options(answer, base=OPT4, either=EITHER):
    """Four-option rule: Only I, Only II, Neither, Both; when the answer is 'Either I or II' it replaces 'Both'
    (impossible for two complementary conclusions) and 'Neither' stays."""
    return base[:3] + [either] if answer == either else list(base)


def stimulus(kind, title, intro, conds, solution):
    sid = f"STIM_REAS_{FIRST_STIM + len(STIMULI):06d}"
    body = intro + "\n\n" + bullets(conds) if conds else intro
    STIMULI.append({"stimulus_id": sid, "type": kind, "title": title, "content": body, "solution": solution})
    return sid


def one_true(statements):
    good = [t for t, ok in statements if ok]
    assert len(good) == 1 and len(statements) == 4, statements
    return good[0], [t for t, ok in statements if not ok]


def one_false(statements):
    bad = [t for t, ok in statements if not ok]
    assert len(bad) == 1 and len(statements) == 4, statements
    return bad[0], [t for t, ok in statements if ok]


def bullets(conds):
    return "\n".join(f"- {c[0]}" for c in conds)


def puzzle_q(sid, topic, sub, diff, text, correct, wrongs, concept, explanation, steps, natural=None, seconds=60,
             verified_by=BRUTE, **kw):
    return mcq(topic, sub, diff, text, correct, wrongs, concept, explanation, steps, natural=natural,
               seconds=seconds, stimulus=sid, verified_by=verified_by, **kw)


ORDN = lambda k: f"{k}{'th' if 10 <= k % 100 <= 20 else {1: 'st', 2: 'nd', 3: 'rd'}.get(k % 10, 'th')}"
MNAME = ["", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
         "November", "December"]
MDAYS = {m: (dt.date(2026 + (m == 12), m % 12 + 1, 1) - dt.date(2026, m, 1)).days for m in range(1, 13)}
assert MDAYS[2] == 28 and MDAYS[4] == 30 and MDAYS[12] == 31
WD = lambda y, m, d_: dt.date(y, m, d_).strftime("%A")
isleap = lambda y: y % 4 == 0 and (y % 100 != 0 or y % 400 == 0)

# ------------------------------------------------------------------------------------------------ repeat guard data
EARLIER_FILES = ["batches/BATCH_000_sample.json"] + sorted(glob.glob(str(ROOT / "batches/parts/BATCH_*_REAS.json")))
EARLIER = [q_ for f in EARLIER_FILES for q_ in json.loads((ROOT / f).read_text(encoding="utf-8"))["questions"]]
_SYL_WORDS = set()
for _q in EARLIER:
    if _q["topic"] == SYL:
        _SYL_WORDS |= set(re.findall(r"[a-z]+", _q["question_text"].split("Statements", 1)[-1]))
_b6 = TOOLS / "batch_006" / "reasoning.py"
if _b6.exists():
    _src = _b6.read_text(encoding="utf-8")
    _i = _src.find("= SYLLOGISM")
    _SYL_WORDS |= set(re.findall(r'"([a-z]+)"', _src[_i:_src.find("= INEQUALITY", _i)]))
USED_NOUNS = set()
SIGNS = "<>≤≥="


def signs_of(chain):
    return "".join(t for t in chain.split() if t in SIGNS)


EARLIER_CHAINS = set()
for _q in EARLIER:
    if _q["topic"] == INQ:
        for m in re.finditer(r"(?:[A-Z] [<>≤≥=] ){4,}[A-Z]", _q["question_text"]):
            EARLIER_CHAINS.add(signs_of(m.group(0)))
MY_CHAINS = set()


def new_chain(chain):
    s = signs_of(chain)
    assert s not in EARLIER_CHAINS and s not in MY_CHAINS, ("repeated chain pattern", chain)
    MY_CHAINS.add(s)


# ------------------------------------------------------------------------------------------------ syllogism engine
def article(w):
    return ("an " if w[0] in "aeiou" else "a ") + w


def syl_text(form, a, b, nouns):
    sa, pa = nouns[a]
    sb, pb = nouns[b]
    return {
        "all": f"All {pa} are {pb}.", "no": f"No {sa} is {article(sb)}.", "some": f"Some {pa} are {pb}.",
        "somenot": f"Some {pa} are not {pb}.", "onlyfew": f"Only a few {pa} are {pb}.",
        "only": f"Only {pa} are {pb}.", "atleast": f"At least some {pa} are {pb}.",
        "poss_all": f"All {pa} being {pb} is a possibility.", "poss_some": f"Some {pa} being {pb} is a possibility.",
        "poss_no": f"No {sa} being {article(sb)} is a possibility.",
        "poss_somenot": f"Some {pa} not being {pb} is a possibility.",
        "never_all": f"All {pa} can never be {pb}.",
    }[form]


def syl_models(terms, statements):
    """Every Venn-region model of up to four non-empty sets (2^(2^k - 1) region subsets) that satisfies the
    statements. Returns (models, holds) where holds[form](model, a, b) tests a categorical form."""
    terms = list(terms)
    k = len(terms)
    assert 2 <= k <= 4
    regions = list(itertools.product((0, 1), repeat=k))[1:]
    ix = {t: i for i, t in enumerate(terms)}
    mask = lambda pred: sum(1 << j for j, r in enumerate(regions) if pred(r))
    AB = {(a, b): mask(lambda r, a=a, b=b: r[ix[a]] and r[ix[b]]) for a in terms for b in terms if a != b}
    AnB = {(a, b): mask(lambda r, a=a, b=b: r[ix[a]] and not r[ix[b]]) for a in terms for b in terms if a != b}
    holds = {
        "all": lambda m, a, b: m & AnB[a, b] == 0, "no": lambda m, a, b: m & AB[a, b] == 0,
        "some": lambda m, a, b: m & AB[a, b] != 0, "atleast": lambda m, a, b: m & AB[a, b] != 0,
        "somenot": lambda m, a, b: m & AnB[a, b] != 0,
        "onlyfew": lambda m, a, b: m & AB[a, b] != 0 and m & AnB[a, b] != 0,
        "only": lambda m, a, b: m & AnB[b, a] == 0,
    }
    nonempty = [mask(lambda r, t=t: r[ix[t]]) for t in terms]
    models = [m for m in range(1 << len(regions))
              if all(m & ne for ne in nonempty) and all(holds[f](m, a, b) for f, a, b in statements)]
    assert models, statements
    return models, holds


POSS_BASE = {"poss_all": "all", "poss_some": "some", "poss_no": "no", "poss_somenot": "somenot"}


def syl_follows(models, holds, c):
    f, a, b = c
    if f in POSS_BASE:
        return any(holds[POSS_BASE[f]](m, a, b) for m in models)
    if f == "never_all":
        return all(not holds["all"](m, a, b) for m in models)
    return all(holds[f](m, a, b) for m in models)


def syl_verdict(nouns, statements, conclusions):
    models, holds = syl_models(nouns, statements)
    f1, f2 = (syl_follows(models, holds, c) for c in conclusions)
    c1, c2 = conclusions
    either = ({c1[1], c1[2]} == {c2[1], c2[2]} and not f1 and not f2
              and not any(c[0] in POSS_BASE or c[0] == "never_all" for c in conclusions)
              and all(holds[c1[0]](m, c1[1], c1[2]) or holds[c2[0]](m, c2[1], c2[2]) for m in models))
    return EITHER if either else BOTH if f1 and f2 else ONLY_I if f1 else ONLY_II if f2 else NEITHER


def register_nouns(nouns):
    for s_, p_ in nouns.values():
        for w in (s_, p_):
            assert w not in _SYL_WORDS, ("noun used in an earlier batch", w)
        assert s_ not in USED_NOUNS, ("noun reused inside the package", s_)
        USED_NOUNS.add(s_)


def N(*pairs):
    return {p_[0]: p_ for p_ in pairs}


SYL_INTRO = ""
SYL_TAIL = "\n\nTake the statements as true. Which conclusion(s) follow?"
SYL_WHY = {
    ONLY_I: "Conclusion II is not forced by the statements (some valid diagram breaks it), so 'Both' and 'Only II' "
            "are wrong; I holds in every diagram, so 'Neither' is wrong.",
    ONLY_II: "Conclusion I is not forced by the statements (some valid diagram breaks it), so 'Both' and 'Only I' "
             "are wrong; II holds in every diagram, so 'Neither' is wrong.",
    NEITHER: "Each conclusion fails in at least one valid diagram, so 'Only I', 'Only II' and 'Both' are wrong.",
    BOTH: "Each conclusion holds in every valid diagram, so choosing only one of them, or neither, is wrong.",
    EITHER: "Neither conclusion is certain alone, so 'Only I' and 'Only II' are wrong; but in every diagram one of "
            "the two holds, so 'Neither' is wrong. ('Either' replaces 'Both' under the four-option rule.)",
}
SYL_CONCEPT = {TWO: "Two-statement syllogism (Venn diagram method)", FEW: "'Only a few' and 'Only' statements",
               POSS: "Possibility conclusions in syllogism"}


def syl_q(diff, sub, nouns, statements, conclusions, expected, explanation, steps, concept=None, shortcut=None,
          seconds=None):
    register_nouns(nouns)
    got = syl_verdict(nouns, statements, conclusions)
    assert got == expected, (statements, conclusions, got, expected)
    text = ("Statements:\n" + "\n".join(syl_text(f, a, b, nouns) for f, a, b in statements) +
            "\n\nConclusions:\nI. " + syl_text(*conclusions[0], nouns) + "\nII. " + syl_text(*conclusions[1], nouns))
    secs = seconds or {"Basic": 35, "Intermediate": 45, "Advanced": 60}[diff] + 10 * (len(statements) - 2)
    return fixed(SYL, sub, diff, text + SYL_TAIL, conclusion_options(expected), expected,
                 concept or SYL_CONCEPT[sub], explanation, steps, shortcut=shortcut,
                 why_others_wrong=SYL_WHY[expected], seconds=secs, verified_by=VENN)


def syl_pick(diff, sub, nouns, statements, candidates, explanation, steps, why, concept=None, seconds=None):
    """Four candidate conclusions; exactly one follows definitely."""
    register_nouns(nouns)
    models, holds = syl_models(nouns, statements)
    marks = [(syl_text(*c, nouns), syl_follows(models, holds, c)) for c in candidates]
    good, bad = one_true(marks)
    text = ("Statements:\n" + "\n".join(syl_text(f, a, b, nouns) for f, a, b in statements) +
            "\n\nTaking the statements to be true even if they seem to be at variance with commonly known facts, "
            "which one of the following conclusions definitely follows?")
    secs = seconds or {"Basic": 40, "Intermediate": 55, "Advanced": 70}[diff] + 10 * (len(statements) - 2)
    return mcq(SYL, sub, diff, text, good, bad, concept or SYL_CONCEPT[sub], explanation, steps,
               why_others_wrong=why, seconds=secs, verified_by=VENN)


def syl_reverse(diff, sub, nouns, conclusions, sets, explanation, steps, why, seconds=80):
    """Reverse syllogism: four sets of statements; exactly one makes both conclusions follow definitely."""
    register_nouns(nouns)
    marks = []
    for st in sets:
        models, holds = syl_models(nouns, st)
        ok = all(syl_follows(models, holds, c) for c in conclusions)
        marks.append((" ".join(syl_text(f, a, b, nouns) for f, a, b in st), ok))
    good, bad = one_true(marks)
    text = ("Conclusions:\nI. " + syl_text(*conclusions[0], nouns) + "\nII. " + syl_text(*conclusions[1], nouns) +
            "\n\nWhich one of the following sets of statements, taken to be true, makes both conclusions I and II "
            "definitely follow?")
    return mcq(SYL, sub, diff, text, good, bad, "Reverse syllogism: testing candidate statement sets", explanation,
               steps, why_others_wrong=why, seconds=seconds, verified_by=VENN)


# ------------------------------------------------------------------------------------------------ inequality engine
REL = {">": lambda a, b: a > b, "<": lambda a, b: a < b, "≥": lambda a, b: a >= b, "≤": lambda a, b: a <= b,
       "=": lambda a, b: a == b}


def parse_chain(s):
    """'P ≥ Q > R' -> [('P','≥','Q'), ('Q','>','R')]."""
    tok = s.split()
    assert len(tok) % 2 == 1 and all(tok[i] in REL for i in range(1, len(tok), 2)), s
    return [(tok[i], tok[i + 1], tok[i + 2]) for i in range(0, len(tok) - 2, 2)]


def ineq_models(chains, extra_vars=(), widen=0):
    """All integer assignments (values 0..k-1+widen) satisfying every relation, by exhaustive backtracking."""
    rels = [r for c in chains for r in parse_chain(c)]
    vs = sorted({x for a, _, b in rels for x in (a, b)} | set(extra_vars))
    dom = range(len(vs) + widen)
    cons = [((a, b), REL[o]) for a, o, b in rels]
    sols = solve(vs, {v: dom for v in vs}, cons)
    assert sols, chains
    return sols


def ineq_follows(chains, concl, widen=0):
    """True when every model satisfies the relation(s) of concl (a chain string)."""
    rels = parse_chain(concl)
    ms = ineq_models(chains, {x for a, _, b in rels for x in (a, b)}, widen)
    return all(REL[o](m[a], m[b]) for m in ms for a, o, b in rels)


def ineq_possible(chains, concl, widen=0):
    rels = parse_chain(concl)
    ms = ineq_models(chains, {x for a, _, b in rels for x in (a, b)}, widen)
    return any(all(REL[o](m[a], m[b]) for a, o, b in rels) for m in ms)


def ineq_verdict(chains, c1, c2):
    res = []
    for widen in (0, 3):  # cross-check: the verdict must not change with a wider value range
        f1, f2 = ineq_follows(chains, c1, widen), ineq_follows(chains, c2, widen)
        (a1, o1, b1), (a2, o2, b2) = parse_chain(c1)[0], parse_chain(c2)[0]
        either = False
        if {a1, b1} == {a2, b2} and not f1 and not f2:
            ms = ineq_models(chains, {a1, b1}, widen)
            either = all(REL[o1](m[a1], m[b1]) or REL[o2](m[a2], m[b2]) for m in ms)
        res.append(EITHER if either else BOTH if f1 and f2 else ONLY_I if f1 else ONLY_II if f2 else NEITHER)
    assert res[0] == res[1], res
    return res[0]


IO4 = {ONLY_I: "Only I is true", ONLY_II: "Only II is true", NEITHER: "Neither I nor II is true",
       BOTH: "Both I and II are true", EITHER: "Either I or II is true"}
INQ_WHY = {
    ONLY_I: "II is not definitely true (a valid ordering breaks it), so 'Only II' and 'Both' are wrong; I always "
            "holds, so 'Neither' is wrong.",
    ONLY_II: "I is not definitely true (a valid ordering breaks it), so 'Only I' and 'Both' are wrong; II always "
             "holds, so 'Neither' is wrong.",
    NEITHER: "Each conclusion fails for some ordering that satisfies the statements, so the other three are wrong.",
    BOTH: "Each conclusion holds for every ordering that satisfies the statements, so picking one, or neither, is "
          "wrong.",
    EITHER: "Neither conclusion is certain alone, but one of them must hold, so 'Neither' is wrong. ('Either' "
            "replaces 'Both' under the four-option rule.)",
}


def ineq_q(diff, sub, statement_text, chains, concs, expected, explanation, steps, shortcut=None, seconds=None,
           concept=None, stimulus=None, shown=None):
    """chains: decoded ordinary chains; concs: two decoded conclusions; shown: conclusions as printed (coded)."""
    got = ineq_verdict(chains, *concs)
    assert got == expected, (chains, concs, got, expected)
    shown = shown or concs
    text = statement_text + "\n\nConclusions:\nI. " + shown[0] + "\nII. " + shown[1]
    secs = seconds or {"Basic": 30, "Intermediate": 50, "Advanced": 70}[diff]
    return fixed(INQ, sub, diff, text, [IO4[x] for x in conclusion_options(expected)], IO4[expected],
                 concept or ("Reading a combined inequality chain" if sub == DIRECT else
                             "Decoding symbols, then reading the chain"),
                 explanation, steps, shortcut=shortcut, why_others_wrong=INQ_WHY[expected], seconds=secs,
                 verified_by=EXHAUST, stimulus=stimulus)


def chain_q(diff, chain, concs, expected, explanation, steps, lead=None, **kw):
    """Direct single-chain item; the sign pattern must be new."""
    new_chain(chain)
    text = (lead + "\n\n" if lead else "") + "Statement: " + chain
    return ineq_q(diff, DIRECT, text, [chain], concs, expected, explanation, steps, **kw)


def multi_q(diff, stmts, concs, expected, explanation, steps, **kw):
    """Direct item with several separate statements."""
    return ineq_q(diff, DIRECT, "Statements: " + "; ".join(stmts), stmts, concs, expected, explanation, steps, **kw)


def decode(s, code):
    return " ".join(code.get(t, t) for t in s.split())


def coded_q(diff, code, sid, stmts, concs, expected, explanation, steps, **kw):
    text = "Statements: " + ", ".join(stmts)
    return ineq_q(diff, CODED, text, [decode(x, code) for x in stmts], [decode(c, code) for c in concs], expected,
                  explanation, steps, stimulus=sid, shown=concs, **kw)


COMBO = {(1, 0, 0): "Only I is true", (0, 1, 0): "Only II is true", (0, 0, 1): "Only III is true",
         (1, 1, 0): "Only I and II are true", (1, 0, 1): "Only I and III are true",
         (0, 1, 1): "Only II and III are true", (1, 1, 1): "All I, II and III are true",
         (0, 0, 0): "None of I, II and III is true"}


def three_q(diff, sub, statement_text, chains, concs, wrong_combos, explanation, steps, why, shown=None,
            seconds=None, stimulus=None, concept=None):
    """Three conclusions; the options are the correct truth pattern and three wrong patterns."""
    pats = [tuple(int(ineq_follows(chains, c, widen)) for c in concs) for widen in (0, 3)]
    assert pats[0] == pats[1]
    good = COMBO[pats[0]]
    wrongs = [COMBO[w] for w in wrong_combos]
    assert good not in wrongs
    shown = shown or concs
    text = (statement_text + "\n\nConclusions:\nI. " + shown[0] + "\nII. " + shown[1] + "\nIII. " + shown[2] +
            "\n\nWhich of the conclusions is/are definitely true?")
    return mcq(INQ, sub, diff, text, good, wrongs, concept or "Three conclusions tested against one chain",
               explanation, steps, why_others_wrong=why, seconds=seconds or 75, verified_by=EXHAUST,
               stimulus=stimulus)


def expr_q(diff, text, candidates, pred, explanation, steps, why, seconds=70, concept=None):
    """Four candidate expressions (chains); exactly one satisfies pred(chain) -> bool."""
    for c in candidates:
        parse_chain(c)
    good, bad = one_true([(c, pred(c)) for c in candidates])
    return mcq(INQ, DIRECT, diff, text, good, bad, concept or "Testing candidate expressions", explanation, steps,
               why_others_wrong=why, seconds=seconds, verified_by=EXHAUST)


def never(rel):
    """pred: rel (e.g. 'G > T') is definitely false, i.e. no ordering satisfying the chain makes it true;
    checked with two value ranges."""
    def f(chain):
        r = [not ineq_possible([chain], rel, w) for w in (0, 3)]
        assert r[0] == r[1]
        return r[0]
    return f


def always(rel):
    def f(chain):
        r = [ineq_follows([chain], rel, w) for w in (0, 3)]
        assert r[0] == r[1]
        return r[0]
    return f


# ================================================================================================ BATCH_007
begin("007")

# ---------------------------------------------------------------- syllogism (B2 I8 A5)
syl_q("Basic", TWO, N(("heron", "herons"), ("stork", "storks"), ("egret", "egrets")),
      [("all", "heron", "stork"), ("no", "stork", "egret")],
      [("no", "heron", "egret"), ("some", "egret", "heron")], ONLY_I,
      "Every heron lies inside the storks, and the storks lie completely outside the egrets, so no heron can be an "
      "egret: I follows. Because no heron is an egret, 'Some egrets are herons' is impossible: II does not follow.",
      ["All herons are storks + No stork is an egret ⇒ No heron is an egret (All + No = No)",
       "I follows; II contradicts I, so it does not follow"])
syl_q("Basic", TWO, N(("tractor", "tractors"), ("scooter", "scooters"), ("jeep", "jeeps")),
      [("some", "tractor", "scooter"), ("some", "scooter", "jeep")],
      [("some", "tractor", "jeep"), ("no", "tractor", "jeep")], EITHER,
      "Two 'Some' statements give no definite link between tractors and jeeps, so neither conclusion is certain on its "
      "own. But I and II are about the same pair and between them cover every case (either some tractors are jeeps or "
      "none is), so exactly one of them must be true: either I or II follows.",
      ["Some + Some ⇒ no definite conclusion", "I and II: 'Some A are B' and 'No A is B' form a complementary pair",
       "Either I or II follows"])
syl_q("Intermediate", FEW, N(("ladle", "ladles"), ("sieve", "sieves"), ("grater", "graters")),
      [("onlyfew", "ladle", "sieve"), ("all", "sieve", "grater")],
      [("all", "ladle", "grater"), ("some", "grater", "ladle")], ONLY_II,
      "'Only a few ladles are sieves' means some ladles are sieves and some are not. The ladles that are sieves are "
      "also graters, so some graters are ladles (II). The ladles outside the sieves may or may not be graters, so 'All "
      "ladles are graters' is not certain (I).",
      ["Ladle ∩ sieve ≠ ∅ and ⊂ graters ⇒ some graters are ladles: II follows",
       "Ladles outside sieves are unrestricted ⇒ I not certain"])
syl_q("Intermediate", FEW, N(("otter", "otters"), ("beaver", "beavers"), ("walrus", "walruses")),
      [("only", "beaver", "otter"), ("some", "walrus", "otter")],
      [("some", "beaver", "walrus"), ("poss_all", "otter", "walrus")], BOTH,
      "'Only beavers are otters' means every otter is a beaver. The walruses that are otters are therefore beavers, so "
      "some beavers are walruses (I). Nothing stops the walrus circle from covering the whole otter circle, so 'All "
      "otters being walruses' is possible (II).",
      ["Only beavers are otters ⇒ All otters are beavers", "Walrus ∩ otter ⊂ beavers ⇒ I follows",
       "Walruses may enclose all otters ⇒ II (possibility) follows"])
syl_q("Intermediate", POSS, N(("daisy", "daisies"), ("lotus", "lotuses"), ("marigold", "marigolds")),
      [("some", "daisy", "lotus"), ("no", "lotus", "marigold")],
      [("poss_all", "daisy", "marigold"), ("poss_some", "lotus", "marigold")], NEITHER,
      "Some daisies are lotuses, and no lotus can be a marigold, so those daisies can never be marigolds: 'All daisies "
      "being marigolds' is impossible (I fails). 'No lotus is a marigold' is definite, so 'Some lotuses being "
      "marigolds' is impossible too (II fails).",
      ["Daisy ∩ lotus is outside marigolds ⇒ all daisies can never be marigolds: I fails",
       "No lotus is a marigold (given) ⇒ II is impossible"])
syl_q("Intermediate", TWO, N(("cashier", "cashiers"), ("auditor", "auditors"), ("banker", "bankers"),
                              ("trader", "traders")),
      [("all", "cashier", "auditor"), ("some", "auditor", "banker"), ("no", "banker", "trader")],
      [("somenot", "auditor", "trader"), ("some", "cashier", "banker")], ONLY_I,
      "The auditors who are bankers can never be traders, so some auditors are not traders (I). The cashiers sit "
      "inside the auditors, but the bankers may overlap a part of the auditors that holds no cashier, so 'Some cashiers "
      "are bankers' is not certain (II).",
      ["Auditor ∩ banker ≠ ∅ and outside traders ⇒ I follows",
       "Cashiers need not touch the auditor–banker overlap ⇒ II not certain"])
syl_q("Intermediate", FEW, N(("sweater", "sweaters"), ("kurta", "kurtas"), ("muffler", "mufflers")),
      [("onlyfew", "sweater", "kurta"), ("onlyfew", "kurta", "muffler")],
      [("some", "sweater", "muffler"), ("somenot", "kurta", "muffler")], ONLY_II,
      "'Only a few kurtas are mufflers' directly says some kurtas are not mufflers (II). Sweaters and mufflers are "
      "linked only through kurtas by two particular statements, so 'Some sweaters are mufflers' is not certain (I).",
      ["Only a few kurtas are mufflers ⇒ some kurtas are mufflers AND some are not: II follows",
       "Two particular statements ⇒ no definite sweater–muffler link: I not certain"])
syl_q("Intermediate", POSS, N(("canoe", "canoes"), ("ferry", "ferries"), ("barge", "barges")),
      [("no", "canoe", "ferry"), ("all", "barge", "ferry")],
      [("poss_some", "canoe", "barge"), ("all", "ferry", "barge")], NEITHER,
      "Every barge is a ferry and no canoe is a ferry, so no canoe can be a barge: 'Some canoes being barges' is "
      "impossible (I). 'All ferries are barges' is a definite claim; the ferry circle may be larger than the barge "
      "circle, so it is not certain (II).",
      ["Barges ⊂ ferries, canoes outside ferries ⇒ no canoe is a barge ⇒ I impossible",
       "Ferries may extend beyond barges ⇒ II not certain"])
syl_q("Intermediate", FEW, N(("plier", "pliers"), ("spanner", "spanners"), ("wrench", "wrenches")),
      [("onlyfew", "plier", "spanner"), ("no", "spanner", "wrench")],
      [("somenot", "plier", "wrench"), ("somenot", "plier", "spanner")], BOTH,
      "'Only a few pliers are spanners' gives some pliers that are spanners and some that are not (II). The pliers "
      "that are spanners can never be wrenches, so some pliers are not wrenches (I).",
      ["Only a few ⇒ some pliers are not spanners: II follows",
       "Plier ∩ spanner ≠ ∅ and outside wrenches ⇒ some pliers are not wrenches: I follows"])
syl_pick("Intermediate", FEW, N(("buckle", "buckles"), ("strap", "straps"), ("zipper", "zippers")),
         [("only", "buckle", "strap"), ("some", "zipper", "strap")],
         [("some", "buckle", "zipper"), ("all", "zipper", "buckle"), ("no", "strap", "zipper"),
          ("all", "buckle", "strap")],
         "'Only buckles are straps' means every strap is a buckle. The zippers that are straps are therefore buckles, so "
         "some buckles are zippers.",
         ["Only buckles are straps ⇒ All straps are buckles", "Zipper ∩ strap ≠ ∅ and ⊂ buckles ⇒ Some buckles are "
          "zippers"],
         "'All zippers are buckles' is not certain (zippers outside straps are free); 'No strap is a zipper' "
         "contradicts the second statement; 'All buckles are straps' reverses the 'Only' statement, which is a common "
         "mistake.")
syl_q("Advanced", POSS, N(("canal", "canals"), ("creek", "creeks"), ("delta", "deltas"), ("fjord", "fjords")),
      [("some", "canal", "creek"), ("all", "creek", "delta"), ("no", "delta", "fjord")],
      [("poss_all", "canal", "fjord"), ("somenot", "canal", "fjord")], ONLY_II,
      "The canals that are creeks are deltas, and no delta is a fjord, so those canals are not fjords: 'Some canals "
      "are not fjords' is definite (II). For the same reason all canals can never be fjords, so the possibility in I "
      "fails.",
      ["Canal ∩ creek ⊂ deltas, which are outside fjords", "⇒ some canals are not fjords: II follows",
       "⇒ 'All canals are fjords' is impossible: I fails"])
syl_q("Advanced", POSS, N(("vulture", "vultures"), ("peacock", "peacocks"), ("kingfisher", "kingfishers"),
                          ("ibis", "ibises")),
      [("onlyfew", "vulture", "peacock"), ("all", "peacock", "kingfisher"), ("somenot", "ibis", "kingfisher")],
      [("all", "vulture", "kingfisher"), ("poss_all", "ibis", "peacock")], NEITHER,
      "The vultures that are not peacocks may lie outside the kingfishers, so 'All vultures are kingfishers' is not "
      "certain (I). Some ibises are outside the kingfishers, and every peacock is inside them, so those ibises can "
      "never be peacocks: 'All ibises being peacocks' is impossible (II).",
      ["Vultures outside peacocks are unrestricted ⇒ I not certain",
       "Ibises outside kingfishers cannot be peacocks (peacocks ⊂ kingfishers) ⇒ II impossible"])
syl_q("Advanced", POSS, N(("rocket", "rockets"), ("glider", "gliders"), ("drone", "drones"),
                          ("satellite", "satellites")),
      [("only", "rocket", "glider"), ("no", "rocket", "drone"), ("some", "satellite", "drone")],
      [("no", "glider", "drone"), ("poss_some", "satellite", "rocket")], BOTH,
      "'Only rockets are gliders' puts every glider inside the rockets; no rocket is a drone, so no glider is a drone "
      "(I). Some satellites are drones, but the other satellites are unrestricted and may overlap the rockets, so "
      "'Some satellites being rockets' is possible (II).",
      ["Only rockets are gliders ⇒ gliders ⊂ rockets", "Rockets ∩ drones = ∅ ⇒ No glider is a drone: I follows",
       "Satellites outside drones may meet rockets ⇒ II (possibility) follows"])
syl_q("Advanced", POSS, N(("vase", "vases"), ("urn", "urns"), ("pitcher", "pitchers"), ("goblet", "goblets")),
      [("all", "vase", "urn"), ("onlyfew", "urn", "pitcher"), ("no", "pitcher", "goblet")],
      [("somenot", "urn", "goblet"), ("poss_all", "urn", "goblet")], ONLY_I,
      "Some urns are pitchers, and no pitcher is a goblet, so those urns are not goblets: I follows. For the same "
      "reason all urns can never be goblets, so the possibility in II fails.",
      ["Urn ∩ pitcher ≠ ∅ and outside goblets", "⇒ some urns are not goblets: I follows",
       "⇒ all urns being goblets is impossible: II fails"])
syl_reverse("Advanced", POSS, N(("beacon", "beacons"), ("flare", "flares"), ("signal", "signals")),
            [("some", "flare", "beacon"), ("poss_all", "beacon", "signal")],
            [[("all", "beacon", "flare"), ("no", "flare", "signal")],
             [("some", "beacon", "flare"), ("all", "flare", "signal")],
             [("no", "beacon", "flare"), ("some", "flare", "signal")],
             [("all", "flare", "signal"), ("somenot", "beacon", "signal")]],
            "With 'Some beacons are flares. All flares are signals.', some flares are beacons (I), and the beacons not "
            "yet placed are free, so all of them may lie inside the signals (II).",
            ["Test each set for both conclusions", "Set 'Some beacons are flares; All flares are signals': I definite, "
             "II possible ⇒ both follow"],
            "'All beacons are flares. No flare is a signal.' makes every beacon a non-signal, so II fails. 'No beacon "
            "is a flare…' contradicts I. 'All flares are signals. Some beacons are not signals.' gives no definite "
            "flare–beacon overlap, so I fails (and II fails too).")

# ---------------------------------------------------------------- inequality (B3 I6 A2)
chain_q("Basic", "K ≥ T > B = R ≥ F < W", ["K > F", "W > B"], ONLY_I,
        "K ≥ T > B = R ≥ F gives K > F (one strict sign on the way). W and B are on opposite sides of the turn at F "
        "(R ≥ F < W), so W > B is not certain.",
        ["I: K ≥ T > B = R ≥ F ⇒ K > F, true", "II: B = R ≥ F < W: direction turns at F ⇒ no relation"])
chain_q("Basic", "D < Q = L ≥ Z > M ≤ H", ["D < Z", "H > Z"], NEITHER,
        "D < Q = L ≥ Z changes direction at L (rising, then falling), so D and Z are unrelated. Z > M ≤ H turns at M, "
        "so H and Z are unrelated too.",
        ["I: D < Q = L ≥ Z: turn at L ⇒ no relation", "II: Z > M ≤ H: turn at M ⇒ no relation"])
chain_q("Basic", "V = J ≤ S < N ≥ C > Y", ["J > C", "Y < N"], ONLY_II,
        "J ≤ S < N ≥ C: the chain turns at N, so J and C are unrelated. Y < C ≤ N gives Y < N.",
        ["I: J ≤ S < N ≥ C: turn at N ⇒ no relation", "II: N ≥ C > Y ⇒ Y < N, true"])

ARW = {"↑": ">", "↓": "<", "⇑": "≥", "⇓": "≤", "↔": "="}
ARW_TXT = ("In the questions of this set, arrows are used between two letters with these meanings:\n"
           "'A ↑ B' means 'A is greater than B'; 'A ↓ B' means 'A is smaller than B'; 'A ⇑ B' means 'A is not smaller "
           "than B'; 'A ⇓ B' means 'A is not greater than B'; 'A ↔ B' means 'A is equal to B'.\nAssuming the "
           "statements to be true, find which of the conclusions I and II is/are definitely true.")
sid = stimulus("passage", "Five arrow symbols for comparisons", ARW_TXT, None,
               "Decode: ↑ means >, ↓ means <, ⇑ means ≥ ('not smaller than'), ⇓ means ≤ ('not greater than') and ↔ "
               "means =. Rewrite every statement with ordinary signs, join them into one chain and test each "
               "conclusion along it.")
coded_q("Intermediate", ARW, sid, ["P ⇑ R", "R ↑ T", "T ↔ G", "G ⇓ M"], ["P ↑ G", "M ⇑ T"], BOTH,
        "Decoded: P ≥ R > T = G ≤ M. P ≥ R > T = G gives P > G (I). M ≥ G = T gives M ≥ T (II).",
        ["Decode: P ≥ R, R > T, T = G, G ≤ M", "Chain: P ≥ R > T = G ≤ M", "I: P > G, true", "II: M ≥ T, true"])
coded_q("Intermediate", ARW, sid, ["B ↓ H", "H ⇓ X", "X ↔ E", "E ↑ U"], ["H ↓ E", "H ↔ E"], EITHER,
        "Decoded: B < H ≤ X = E > U. Only H ≤ E is known, so neither H < E nor H = E is certain alone, but one of "
        "them must hold.",
        ["Decode: B < H, H ≤ X, X = E, E > U", "H ≤ X = E ⇒ H ≤ E", "I: H < E and II: H = E split '≤' ⇒ either"])
coded_q("Intermediate", ARW, sid, ["W ↑ F", "F ⇑ K", "Y ⇓ K", "Y ↑ A"], ["F ↑ Y", "A ⇑ K"], NEITHER,
        "Decoded: W > F ≥ K ≥ Y > A. F ≥ K ≥ Y gives only F ≥ Y, so F > Y is not certain (I). A < Y ≤ K gives A < K, "
        "so A ≥ K is false (II).",
        ["Decode: W > F, F ≥ K, Y ≤ K (K ≥ Y), Y > A", "Chain: W > F ≥ K ≥ Y > A",
         "I: F ≥ Y only ⇒ F > Y not certain", "II: A < K ⇒ A ≥ K false"])
coded_q("Intermediate", ARW, sid, ["J ↔ C", "C ⇓ V", "V ↓ N", "D ⇑ N"], ["J ↑ V", "D ↑ C"], ONLY_II,
        "Decoded: J = C ≤ V < N ≤ D. J = C ≤ V means J > V is false (I). D ≥ N > V ≥ C gives D > C (II).",
        ["Decode: J = C, C ≤ V, V < N, D ≥ N", "Chain: J = C ≤ V < N ≤ D", "I: J ≤ V ⇒ J > V false",
         "II: D ≥ N > V ≥ C ⇒ D > C, true"])
multi_q("Intermediate", ["G > S", "S ≥ Z", "Z = O", "O < I", "I ≤ T"], ["G > O", "T > S"], ONLY_I,
        "Combined: G > S ≥ Z = O < I ≤ T. G > S ≥ Z = O gives G > O (I). T and S lie on opposite sides of the turn at "
        "O, so T > S is not certain (II).",
        ["Chain: G > S ≥ Z = O < I ≤ T", "I: G > O, true", "II: S ≥ … O < … T: turn at O ⇒ no relation"])
multi_q("Intermediate", ["U ≤ E", "E < Q", "Q = W", "B ≥ W", "R < U"], ["B > U", "R < Q"], BOTH,
        "Combined: R < U ≤ E < Q = W ≤ B. Every sign from R to B points the same way, so B > U (I) and R < Q (II).",
        ["Chain: R < U ≤ E < Q = W ≤ B", "I: B ≥ W = Q > E ≥ U ⇒ B > U, true", "II: R < U ≤ E < Q ⇒ R < Q, true"])
multi_q("Advanced", ["H ≥ N", "N > P", "P ≤ Y", "Y = F", "F < L", "K ≥ H"], ["K > Y", "L > N"], NEITHER,
        "Combined: K ≥ H ≥ N > P ≤ Y = F < L. K and Y, and L and N, are compared across the turn at P (N > P ≤ Y), so "
        "neither relation is fixed.",
        ["Chain: K ≥ H ≥ N > P ≤ Y = F < L", "I: K … N > P ≤ Y: turn at P ⇒ no relation",
         "II: N > P ≤ … L: turn at P ⇒ no relation"], seconds=60)
three_q("Advanced", DIRECT, "Statements: A ≥ X; X = C; C > V; V ≥ O; M ≤ O; M < S",
        ["A ≥ X", "X = C", "C > V", "V ≥ O", "M ≤ O", "M < S"], ["A > O", "S > V", "V ≥ M"],
        [(1, 1, 1), (1, 0, 0), (0, 0, 1)],
        "Combined: A ≥ X = C > V ≥ O ≥ M < S. A > O follows (I). S and V are on opposite sides of the turn at M, so "
        "S > V is not certain (II). V ≥ O ≥ M gives V ≥ M (III).",
        ["Chain: A ≥ X = C > V ≥ O ≥ M < S", "I: A > O, true", "II: turn at M ⇒ not certain",
         "III: V ≥ O ≥ M ⇒ V ≥ M, true", "Only I and III"],
        "'All three' wrongly accepts II; 'Only I' misses III ('≥' conclusions are true when the chain gives ≥); "
        "'Only III' misses I.")

# ---------------------------------------------------------------- month and date puzzles (B2 I1 A2)
# MB1: leave months chosen by the length of the month's name
P = ["Bhoomi", "Chetan", "Dilnaz", "Ekansh", "Farida"]
MS = [2, 5, 6, 8, 12]
conds = [("Chetan's month has the shortest name of the five months.", ("Chetan",),
          lambda c: len(MNAME[c]) == min(len(MNAME[m]) for m in MS)),
         ("Farida's month is the next of these five months after Chetan's.", ("Farida", "Chetan"),
          lambda f, c: MS.index(f) == MS.index(c) + 1),
         ("Bhoomi's month has 28 days.", ("Bhoomi",), lambda b: MDAYS[b] == 28),
         ("Ekansh's month comes before Dilnaz's.", ("Ekansh", "Dilnaz"), lambda e, d: e < d)]
S_ = unique(P, {p: MS for p in P}, conds, [P])
assert (S_["Chetan"], S_["Farida"], S_["Bhoomi"], S_["Ekansh"], S_["Dilnaz"]) == (5, 6, 2, 8, 12)
mcq(MON, MB, "Basic", "Five colleagues Bhoomi, Chetan, Dilnaz, Ekansh and Farida each take a week's leave in 2027 "
    "(not a leap year), in five different months among February, May, June, August and December.\n" + bullets(conds) +
    "\n\nWho takes leave in August?", "Ekansh", ["Dilnaz", "Farida", "Chetan"], "Fix the months with a unique property "
    "first",
    "May has the shortest name (3 letters), so Chetan takes May; the next listed month, June, goes to Farida. Only "
    "February has 28 days: Bhoomi. August and December remain, and Ekansh is before Dilnaz, so Ekansh takes August.",
    ["Shortest name: May ⇒ Chetan", "Next listed month: June ⇒ Farida", "28 days: February ⇒ Bhoomi",
     "Ekansh before Dilnaz ⇒ Ekansh August, Dilnaz December"],
    why_others_wrong="Dilnaz takes December, Farida June and Chetan May.", seconds=40, verified_by=BRUTE)

# MB2: dates of a month described by number properties
P = ["Gopal", "Hetal", "Ira", "Jatin", "Kavya"]
DT = [6, 9, 15, 16, 28]
conds = [("Gopal's date is a perfect square greater than 10.", ("Gopal",), lambda g: g > 10 and int(g ** .5) ** 2 == g),
         ("Hetal's date is 12 days after Gopal's.", ("Hetal", "Gopal"), lambda h, g: h == g + 12),
         ("Ira's date is an odd number smaller than 10.", ("Ira",), lambda i: i % 2 == 1 and i < 10),
         ("Jatin's date is earlier than Kavya's.", ("Jatin", "Kavya"), lambda j, k: j < k)]
S_ = unique(P, {p: DT for p in P}, conds, [P])
nxt = sorted(DT)[sorted(DT).index(S_["Ira"]) + 1]
ans = next(p for p in P if S_[p] == nxt)
assert ans == "Kavya" and S_["Jatin"] == 6
mcq(MON, DB, "Basic", "Five persons Gopal, Hetal, Ira, Jatin and Kavya each book a cooking class in the same month, on "
    "five different dates among the 6th, 9th, 15th, 16th and 28th.\n" + bullets(conds) + "\n\nWhose class is on the "
    "date that comes immediately after Ira's?", ans, ["Jatin", "Gopal", "Hetal"], "Number properties of the dates",
    "Of the five dates, 9 and 16 are perfect squares and only 16 is greater than 10: Gopal. Hetal = 16 + 12 = 28. The "
    "odd dates below 10: only 9, so Ira has the 9th. Jatin and Kavya share the 6th and the 15th, and Jatin is earlier: "
    "Jatin 6th, Kavya 15th. The date right after the 9th is the 15th: Kavya.",
    ["Perfect square > 10: 16 ⇒ Gopal", "Hetal 28", "Odd and < 10: 9 ⇒ Ira", "Jatin 6, Kavya 15",
     "Next after 9th: 15th ⇒ Kavya"], why_others_wrong="Jatin has the 6th (before Ira), Gopal the 16th and Hetal the "
    "28th.", seconds=45, verified_by=BRUTE)

# MI1: birth years with two leap years
P = ["Nupur", "Om", "Pallavi", "Rakesh", "Sanya"]
YR = [2008, 2011, 2013, 2016, 2019]
conds = [("Nupur and Om were born in leap years, and Nupur is older than Om.", ("Nupur", "Om"),
          lambda n, o: isleap(n) and isleap(o) and n < o),
         ("Pallavi is exactly three years younger than Om.", ("Pallavi", "Om"), lambda p, o: p == o + 3),
         ("Rakesh is older than Sanya.", ("Rakesh", "Sanya"), lambda r, s: r < s)]
S_ = unique(P, {p: YR for p in P}, conds, [P])
ans = (2026 - S_["Rakesh"]) + (2026 - S_["Om"])
assert (S_["Rakesh"], S_["Om"], ans) == (2011, 2016, 25)
mcq(MON, YB, "Intermediate", "Five cousins Nupur, Om, Pallavi, Rakesh and Sanya were born in five different years among "
    "2008, 2011, 2013, 2016 and 2019. Ages are counted in completed years on their birthdays.\n" + bullets(conds) +
    "\n\nWhat is the sum of the ages of Rakesh and Om on their birthdays in 2026?", str(ans), ["23", "28", "26"],
    "Leap years are divisible by 4",
    "Among the five years only 2008 and 2016 are divisible by 4, so Nupur (older) was born in 2008 and Om in 2016. "
    "Pallavi = 2016 + 3 = 2019. Rakesh and Sanya share 2011 and 2013, Rakesh older: Rakesh 2011, Sanya 2013. In 2026 "
    "Rakesh is 15 and Om 10: 25.",
    ["Leap years: 2008, 2016 ⇒ Nupur 2008, Om 2016", "Pallavi 2019", "Rakesh 2011, Sanya 2013",
     "Ages in 2026: 15 + 10 = 25"],
    why_others_wrong="23 adds Sanya's age (13) to Om's; 28 adds Rakesh's and Sanya's; 26 uses Rakesh's age as 16.",
    natural=int, seconds=60, verified_by=BRUTE)

# MA1: events on the first day of five months of 2027 (1 January 2027 is a Friday)
assert WD(2027, 1, 1) == "Friday"
F1 = lambda m: WD(2027, m, 1)
P = ["Tanuj", "Urmila", "Vikrant", "Yashika", "Zubin"]
conds = [("Tanuj's event falls on a Sunday.", ("Tanuj",), lambda t: F1(t) == "Sunday"),
         ("Urmila's event falls on a Thursday in the first half of the year.", ("Urmila",),
          lambda u: F1(u) == "Thursday" and u <= 6),
         ("Vikrant's event falls on the same day of the week as Urmila's.", ("Vikrant", "Urmila"),
          lambda v, u: F1(v) == F1(u)),
         ("Yashika's event falls on a Monday, in a month that has 30 days.", ("Yashika",),
          lambda y: F1(y) == "Monday" and MDAYS[y] == 30),
         ("Zubin's event falls on a Wednesday and comes after Yashika's.", ("Zubin", "Yashika"),
          lambda z, y: F1(z) == "Wednesday" and z > y)]
S_ = unique(P, {p: range(1, 13) for p in P}, conds, [P])
assert {p: S_[p] for p in P} == {"Tanuj": 8, "Urmila": 4, "Vikrant": 7, "Yashika": 11, "Zubin": 12}
cnt = sum(MDAYS[S_[p]] == 31 for p in P)
assert cnt == 3
mcq(MON, MB, "Advanced", "Five persons Tanuj, Urmila, Vikrant, Yashika and Zubin each hold an event on the 1st of a "
    "different month of 2027. 1 January 2027 is a Friday, and 2027 is not a leap year.\n" + bullets(conds) +
    "\n\nHow many of the five events are held in a month that has 31 days?", num_word(cnt), ["Two", "Four", "One"],
    "Weekday of the 1st of each month (odd days)",
    "A month of 31 days moves the weekday on by 3, a 30-day month by 2 and February (28 days) by 0. From Friday 1 "
    "January the 1sts of 2027 fall on: Jan Fri, Feb Mon, Mar Mon, Apr Thu, May Sat, Jun Tue, Jul Thu, Aug Sun, Sep Wed, "
    "Oct Fri, Nov Mon, Dec Wed. Tanuj: the only Sunday, August. Urmila: Thursday in the first half, April; Vikrant: "
    "the other Thursday, July. Yashika: a Monday in a 30-day month — February and March fail, so November. Zubin: a "
    "Wednesday after November, December. The 31-day months are August, July and December: three events.",
    ["Shift: 31 days → +3, 30 days → +2, 28 days → 0", "1sts: Feb/Mar/Nov Mon, Apr/Jul Thu, Aug Sun, Sep/Dec Wed",
     "Tanuj Aug, Urmila Apr, Vikrant Jul, Yashika Nov, Zubin Dec", "31-day months: Aug, Jul, Dec ⇒ three"],
    why_others_wrong="Two or One leave out some of August, July and December; Four counts April or November, which "
                     "have 30 days.", natural=by_num, seconds=120, verified_by=BRUTE)

# MA2: a clinic that runs every 9th day from Sunday 3 January 2027
CL = [dt.date(2027, 1, 3) + dt.timedelta(days=9 * k) for k in range(10)]
assert CL[0].strftime("%A") == "Sunday" and CL[-1] == dt.date(2027, 3, 25)
P = ["Prerna", "Qadir", "Raunak", "Seema", "Tushar"]
day = lambda i: CL[i].strftime("%A")
conds = [("Prerna visits on the earliest clinic day that falls on a Saturday.", ("Prerna",),
          lambda p: day(p) == "Saturday" and all(day(j) != "Saturday" for j in range(p))),
         ("Qadir visits on a Friday in February.", ("Qadir",), lambda q_: day(q_) == "Friday" and CL[q_].month == 2),
         ("Raunak visits exactly four clinic days after Prerna.", ("Raunak", "Prerna"), lambda r, p: r == p + 4),
         ("Seema visits on a Tuesday in January.", ("Seema",), lambda s: day(s) == "Tuesday" and CL[s].month == 1),
         ("Tushar visits on the last clinic day in March.", ("Tushar",),
          lambda t: CL[t].month == 3 and all(CL[j].month != 3 for j in range(t + 1, len(CL))))]
S_ = unique(P, {p: range(len(CL)) for p in P}, conds, [P])
td = CL[S_["Tushar"]]
ans = f"{td.day} March, {td.strftime('%A')}"
assert ans == "25 March, Thursday" and CL[S_["Raunak"]] == dt.date(2027, 3, 7)
mcq(MON, DB, "Advanced", "A free health clinic runs once every 9 days in 2027: its first day is Sunday, 3 January, the "
    "next is 12 January, and so on. Five persons Prerna, Qadir, Raunak, Seema and Tushar each visit on a different "
    "clinic day between January and March 2027 (2027 is not a leap year).\n" + bullets(conds) +
    "\n\nOn which date and day of the week does Tushar visit?", ans,
    ["25 March, Friday", "24 March, Wednesday", "16 March, Tuesday"], "A 9-day cycle moves the weekday on by 2",
    "Clinic days: 3, 12, 21, 30 January; 8, 17, 26 February; 7, 16, 25 March. Since 9 = 7 + 2, each clinic day falls two "
    "weekdays after the previous one: Sun, Tue, Thu, Sat, Mon, Wed, Fri, Sun, Tue, Thu. So the last clinic day in March, "
    "25 March, is a Thursday. (Prerna 30 Jan, Raunak 7 Mar, Seema 12 Jan and Qadir 26 Feb fit the other clues.)",
    ["Clinic days: Jan 3, 12, 21, 30; Feb 8, 17, 26; Mar 7, 16, 25", "Weekday +2 each time from Sunday",
     "10th clinic day (25 March): Sun→Tue→Thu→Sat→Mon→Wed→Fri→Sun→Tue→Thu"],
    why_others_wrong="25 March, Friday ignores the 2-day weekday step; 24 March, Wednesday miscounts February as 29 "
                     "days; 16 March is the second-last clinic day in March.", seconds=110, verified_by=BRUTE)

# ---------------------------------------------------------------- other puzzles (B5 I2 A5)
# OB1 Basic set: six morning runners and their distances
P = ["Amol", "Binita", "Chirag", "Deepti", "Eshan", "Gargi"]
conds = [("Deepti ran farther than Chirag but less than Gargi.", ("Deepti", "Chirag", "Gargi"),
          lambda d, c, g: c < d < g),
         ("Amol ran less than Chirag.", ("Amol", "Chirag"), lambda a, c: a < c),
         ("Eshan ran farther than Gargi.", ("Eshan", "Gargi"), lambda e, g: e > g),
         ("Binita ran farther than Amol but less than Chirag.", ("Binita", "Amol", "Chirag"),
          lambda b, a, c: a < b < c)]
S_ = unique(P, {p: range(1, 7) for p in P}, conds, [P])  # 6 = farthest
ORD = sorted(P, key=lambda p: -S_[p])
assert ORD == ["Eshan", "Gargi", "Deepti", "Chirag", "Binita", "Amol"]
sid = stimulus("puzzle", "Six morning runners and their distances",
               "Six friends Amol, Binita, Chirag, Deepti, Eshan and Gargi each ran a different distance on a Sunday "
               "morning.", conds,
               "Chirag < Deepti < Gargi < Eshan, and Amol < Binita < Chirag. Joined: Eshan > Gargi > Deepti > Chirag > "
               "Binita > Amol.")
ARR = "Order (farthest first): Eshan, Gargi, Deepti, Chirag, Binita, Amol"
puzzle_q(sid, OTH, CMP, "Basic", "Who ran the third longest distance?", "Deepti", ["Gargi", "Chirag", "Binita"],
         "Join the comparisons into one chain", "From the clues, Eshan > Gargi > Deepti > Chirag > Binita > Amol; the "
         "third is Deepti.", [ARR, "Third: Deepti"], why_others_wrong="Gargi is second, Chirag fourth and Binita "
         "fifth.", seconds=40)
puzzle_q(sid, OTH, CMP, "Basic", "How many of the friends ran less than Deepti?", "Three", ["Two", "Four", "One"],
         "Count below a position", "Chirag, Binita and Amol ran less than Deepti: three.", [ARR, "Below Deepti: "
         "Chirag, Binita, Amol ⇒ 3"], why_others_wrong="Two misses Amol or Binita; Four counts Deepti herself; One "
         "counts only Amol.", natural=by_num, seconds=30)
puzzle_q(sid, OTH, CMP, "Basic", "If the farthest runner covered 12 km and each runner covered exactly 1 km more than "
         "the next shorter runner, how far did Chirag run?", "9 km", ["8 km", "10 km", "7 km"],
         "Map ranks to values", "Eshan 12, Gargi 11, Deepti 10, Chirag 9 km.", [ARR, "12, 11, 10, 9 ⇒ Chirag 9 km"],
         why_others_wrong="10 km is Deepti's distance, 8 km Binita's and 7 km Amol's.", natural=by_num, seconds=40)

# OB2 Basic: five visits from Thursday to the following Monday
DN5 = ["Thursday", "Friday", "Saturday", "Sunday", "Monday"]
P = ["Harsh", "Ila", "Jai", "Kriti", "Lalit"]
conds = [("Kriti visits on Saturday.", ("Kriti",), lambda k: k == 2),
         ("Ila visits on the day immediately before Kriti.", ("Ila", "Kriti"), lambda i, k: i == k - 1),
         ("Jai visits on the last of the five days.", ("Jai",), lambda j: j == 4),
         ("Lalit visits on a later day than Harsh.", ("Lalit", "Harsh"), lambda l_, h: l_ > h)]
S_ = unique(P, {p: range(5) for p in P}, conds, [P])
assert DN5[S_["Lalit"]] == "Sunday"
mcq(OTH, DAY, "Basic", "Five persons Harsh, Ila, Jai, Kriti and Lalit visit a dental clinic on five consecutive days "
    "from Thursday to the following Monday, one person per day.\n" + bullets(conds) + "\n\nWho visits on Sunday?",
    "Lalit", ["Harsh", "Jai", "Ila"], "Days across a weekend",
    "Kriti is on Saturday and Ila on Friday. Jai takes the last day, Monday. Thursday and Sunday remain; Lalit is later "
    "than Harsh, so Harsh visits on Thursday and Lalit on Sunday.",
    ["Kriti Sat, Ila Fri, Jai Mon", "Thursday and Sunday left; Harsh before Lalit ⇒ Lalit Sunday"],
    why_others_wrong="Harsh visits on Thursday, Jai on Monday and Ila on Friday.", seconds=35, verified_by=BRUTE)

# OB3 Basic: four posts and one guest lecturer
POST = ["", "Principal", "Vice-Principal", "Head of Department", "Lecturer"]
P = ["Mehul", "Nisha", "Omkar", "Priti", "Rohan"]
conds = [("Mehul is a guest lecturer and holds none of the four posts.", ("Mehul",), lambda m: m == 0),
         ("Priti is the Vice-Principal.", ("Priti",), lambda p: p == 2),
         ("Rohan holds a post junior to Priti's post but senior to Omkar's.", ("Rohan", "Priti", "Omkar"),
          lambda r, p, o: p < r < o),
         ("Nisha is senior to Omkar.", ("Nisha", "Omkar"), lambda n, o: 0 < n < o)]
S_ = unique(P, {p: range(5) for p in P}, conds, [P])
assert POST[S_["Rohan"]] == "Head of Department" and S_["Nisha"] == 1
mcq(OTH, DSG, "Basic", "Five teachers Mehul, Nisha, Omkar, Priti and Rohan work in a college. Four of them hold the "
    "posts of Principal, Vice-Principal, Head of Department and Lecturer, one post each, in decreasing order of "
    "seniority.\n" + bullets(conds) + "\n\nWho is the Head of Department?", "Rohan", ["Omkar", "Nisha", "Mehul"],
    "Seniority order of posts",
    "Mehul holds no post. Priti is the Vice-Principal. Rohan is junior to Priti but senior to Omkar, so Rohan is the "
    "Head of Department and Omkar the Lecturer. That leaves Nisha as Principal (senior to Omkar, as required).",
    ["Mehul: no post; Priti: Vice-Principal", "Priti > Rohan > Omkar ⇒ Rohan HoD, Omkar Lecturer",
     "Nisha: Principal"], why_others_wrong="Omkar is the Lecturer, Nisha the Principal and Mehul holds no post.",
    seconds=40, verified_by=BRUTE)

# OI1 Intermediate: a round-robin with all win counts different
T5 = ["Amber", "Coral", "Ivory", "Jade", "Ruby"]
PAIRS = list(itertools.combinations(T5, 2))
ixT = {t: i for i, t in enumerate(T5)}


def rr_sols(conds_):
    out = []
    for res in itertools.product((0, 1), repeat=len(PAIRS)):  # 1 = first team of the pair wins
        beat = {(a, b) if r else (b, a) for (a, b), r in zip(PAIRS, res)}
        wins = {t: sum(1 for x, _ in beat if x == t) for t in T5}
        if len(set(wins.values())) == 5 and all(f(beat, wins) for _, f in conds_):
            out.append((beat, wins))
    return out


rconds = [("Jade won more matches than Ruby but fewer than Ivory.", lambda b, w: w["Ruby"] < w["Jade"] < w["Ivory"]),
          ("Amber beat Ivory.", lambda b, w: ("Amber", "Ivory") in b),
          ("Coral lost to Ruby.", lambda b, w: ("Ruby", "Coral") in b)]
RR = rr_sols(rconds)
assert len(RR) == 1 and RR[0][1] == {"Amber": 4, "Ivory": 3, "Jade": 2, "Ruby": 1, "Coral": 0}
mcq(OTH, CMP, "Intermediate", "Five teams Amber, Coral, Ivory, Jade and Ruby play a round-robin tournament: every team "
    "plays every other team exactly once, and every match has a winner (no draws). At the end, no two teams have won "
    "the same number of matches.\n" + bullets(rconds) + "\n\nHow many matches did Jade win?",
    "2", ["3", "1", "4"], "Distinct win counts in a round-robin",
    "There are 10 matches and each team plays 4. Five different win counts adding up to 10 must be 4, 3, 2, 1 and 0. "
    "Then the team with 4 wins beat everyone, the team with 3 beat all but the top team, and so on — a strict ladder. "
    "Ivory > Jade > Ruby in wins, Ruby beat Coral so Ruby is above Coral, and Amber beat Ivory so Amber is above Ivory. "
    "Ladder: Amber 4, Ivory 3, Jade 2, Ruby 1, Coral 0.",
    ["10 matches; distinct counts from 0–4 adding to 10 ⇒ 4, 3, 2, 1, 0", "Distinct counts ⇒ higher team beats lower",
     "Amber > Ivory > Jade > Ruby > Coral", "Jade: 2 wins"],
    why_others_wrong="3 is Ivory's count, 1 Ruby's and 4 Amber's.", natural=int, seconds=80, verified_by=BRUTE)

# OI2 Intermediate: six sessions on the Mondays, Wednesdays and Fridays of two weeks
SL = ["Monday of week 1", "Wednesday of week 1", "Friday of week 1", "Monday of week 2", "Wednesday of week 2",
      "Friday of week 2"]
P = ["Gauri", "Hemant", "Isha", "Jairaj", "Komal", "Lakshay"]
wk = lambda s: s // 3
conds = [("Isha's session is on the Wednesday of week 2.", ("Isha",), lambda i: i == 4),
         ("Exactly two sessions are held between Isha's session and Gauri's session.", ("Isha", "Gauri"),
          lambda i, g_: abs(i - g_) == 3),
         ("Komal's session is on a Friday.", ("Komal",), lambda k: k % 3 == 2),
         ("Hemant's session is in the same week as Komal's, and earlier.", ("Hemant", "Komal"),
          lambda h, k: wk(h) == wk(k) and h < k),
         ("Lakshay's session is the first of the six.", ("Lakshay",), lambda l_: l_ == 0)]
S_ = unique(P, {p: range(6) for p in P}, conds, [P])
assert S_["Jairaj"] == 2 and S_["Hemant"] == 3 and S_["Gauri"] == 1
mcq(OTH, DAY, "Intermediate", "Six trainers Gauri, Hemant, Isha, Jairaj, Komal and Lakshay each take one session in a "
    "two-week course. Sessions are held only on Monday, Wednesday and Friday of each week (six sessions in all), one "
    "trainer per session.\n" + bullets(conds) + "\n\nWhose session is on the Friday of week 1?", "Jairaj",
    ["Hemant", "Gauri", "Komal"], "Slots in order: Mon, Wed, Fri of week 1, then week 2",
    "Number the slots 1 to 6. Isha is slot 5; two sessions between Isha and Gauri puts Gauri in slot 2 (slot 8 does not "
    "exist). Lakshay is slot 1. Komal is on a Friday (slot 3 or 6) with Hemant earlier in the same week: slot 3 would "
    "need Hemant in slot 1 or 2, both taken, so Komal is slot 6 and Hemant slot 4 (slot 5 is Isha's). Jairaj takes the "
    "remaining slot 3, the Friday of week 1.",
    ["Slots 1–6; Isha 5, Gauri 2, Lakshay 1", "Komal Friday: slot 3 fails (Hemant has no room) ⇒ slot 6",
     "Hemant slot 4", "Jairaj slot 3 = Friday of week 1"],
    why_others_wrong="Hemant is on Monday of week 2, Gauri on Wednesday of week 1 and Komal on Friday of week 2.",
    seconds=70, verified_by=BRUTE)

# OA Advanced set: seven designations and the weekday of each officer's review
P = ["Ansh", "Bina", "Chhavi", "Darsh", "Eshita", "Faisal", "Gita"]
RK = ["", "General Manager", "Deputy General Manager", "Assistant General Manager", "Chief Manager",
      "Senior Manager", "Manager", "Officer"]
DN = ["", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
VV = [x for p in P for x in ("r" + p, "d" + p)]
rd = lambda p: ("r" + p, "d" + p)
conds = [
    ("The General Manager's review is on Thursday.", each(P, lambda p: (rd(p), lambda r, d: r != 1 or d == 4))),
    ("Darsh is the Assistant General Manager, and his review is on the day immediately after the Officer's review.",
     [(("rDarsh",), lambda r: r == 3)] + each([p for p in P if p != "Darsh"], lambda p: (
         rd(p) + ("dDarsh",), lambda r, d, dd: r != 7 or dd == d + 1))),
    ("Exactly two reviews are held between Bina's review and the General Manager's review, and Bina is junior to "
     "Darsh.", [(("rBina",), lambda r: r > 3)] + each(P, lambda p: (
         rd(p) + ("dBina",), lambda r, d, db: r != 1 or abs(db - d) == 3))),
    ("Faisal's review is on Sunday. Faisal is senior to Chhavi but junior to Eshita.",
     ("dFaisal", "rFaisal", "rChhavi", "rEshita"), lambda d, f, c, e: d == 7 and e < f < c),
    ("The Manager's review is on Monday.", each(P, lambda p: (rd(p), lambda r, d: r != 6 or d == 1))),
    ("Gita's review is on the day immediately before Ansh's review, and Gita is senior to Ansh.",
     ("dGita", "dAnsh", "rGita", "rAnsh"), lambda dg, da, rg, ra: da == dg + 1 and rg < ra),
    ("Exactly one review is held between Ansh's review and Faisal's review.", ("dAnsh", "dFaisal"),
     lambda a, f: abs(a - f) == 2),
    ("Ansh is senior to Eshita.", ("rAnsh", "rEshita"), lambda a, e: a < e),
    ("Chhavi's review is earlier in the week than Darsh's review.", ("dChhavi", "dDarsh"), lambda c, d: c < d),
]
S_ = unique(VV, {v: range(1, 8) for v in VV}, conds, [["r" + p for p in P], ["d" + p for p in P]])
R_ = {p: S_["r" + p] for p in P}
D_ = {p: S_["d" + p] for p in P}
assert R_ == {"Ansh": 2, "Bina": 6, "Chhavi": 7, "Darsh": 3, "Eshita": 4, "Faisal": 5, "Gita": 1}
assert D_ == {"Ansh": 5, "Bina": 1, "Chhavi": 2, "Darsh": 3, "Eshita": 6, "Faisal": 7, "Gita": 4}
sid = stimulus("puzzle", "Seven bank officers: designations and review days",
               "Seven officers Ansh, Bina, Chhavi, Darsh, Eshita, Faisal and Gita of a bank hold seven different "
               "designations. In decreasing order of seniority these are: General Manager, Deputy General Manager, "
               "Assistant General Manager, Chief Manager, Senior Manager, Manager and Officer. Each officer conducts a "
               "review on a different day of one week, from Monday to Sunday.", conds,
               "Bina is three days away from the General Manager's Thursday: Monday or Sunday; Faisal has Sunday, so "
               "Bina is on Monday and, as the Monday reviewer, is the Manager. One review between Ansh and Faisal "
               "(Sunday) puts Ansh on Friday and Gita on Thursday, so Gita is the General Manager. Tuesday, Wednesday "
               "and Saturday remain for Chhavi, Darsh and Eshita. Darsh comes the day after the Officer: Darsh on "
               "Saturday would make Ansh (Friday) the Officer, but Ansh is senior to Eshita; Darsh on Tuesday would "
               "make the Monday Manager the Officer. So Darsh is on Wednesday and the Officer on Tuesday; Chhavi is "
               "earlier than Darsh, so Chhavi is on Tuesday (Officer) and Eshita on Saturday. Ranks left 2, 4, 5: "
               "Ansh > Eshita > Faisal gives Ansh DGM, Eshita Chief Manager, Faisal Senior Manager.\n\n"
               "Mon Bina (Manager), Tue Chhavi (Officer), Wed Darsh (AGM), Thu Gita (GM), Fri Ansh (DGM), Sat Eshita "
               "(Chief Manager), Sun Faisal (Senior Manager).")
ARR = ("Mon Bina–Manager, Tue Chhavi–Officer, Wed Darsh–AGM, Thu Gita–GM, Fri Ansh–DGM, Sat Eshita–Chief Manager, "
       "Sun Faisal–Senior Manager")
who = lambda k: next(p for p in P if R_[p] == k)
puzzle_q(sid, OTH, DSG, "Advanced", "Who is the Chief Manager?", who(4), ["Faisal", "Ansh", "Bina"],
         "Link the day clues to the designation clues", "Eshita reviews on Saturday and is the Chief Manager.",
         [ARR, "Chief Manager: Eshita"], why_others_wrong="Faisal is the Senior Manager, Ansh the DGM and Bina the "
         "Manager.", seconds=150)
puzzle_q(sid, OTH, DAY, "Advanced", "On which day does the Deputy General Manager conduct the review?",
         DN[D_[who(2)]], ["Saturday", "Wednesday", "Thursday"], "Read the day of a designation",
         "The DGM is Ansh, whose review is on Friday.", [ARR, "DGM Ansh ⇒ Friday"],
         why_others_wrong="Saturday is the Chief Manager's day, Wednesday the AGM's and Thursday the GM's.", seconds=45)
gap = abs(D_[who(6)] - D_[who(5)]) - 1
assert gap == 5
puzzle_q(sid, OTH, DAY, "Advanced", "How many reviews are held between the Manager's review and the Senior Manager's "
         "review?", num_word(gap), ["Four", "Six", "Three"], "Count the days strictly between",
         "The Manager (Bina) reviews on Monday and the Senior Manager (Faisal) on Sunday; Tuesday to Saturday lie "
         "between: five reviews.", [ARR, "Monday … Sunday ⇒ 5 between"],
         why_others_wrong="Six counts one end; Four and Three miscount the days between Monday and Sunday.",
         natural=by_num, seconds=45)
good, bad = one_true([("Chhavi – Officer – Tuesday", R_["Chhavi"] == 7 and D_["Chhavi"] == 2),
                      ("Gita – Deputy General Manager – Thursday", R_["Gita"] == 2 and D_["Gita"] == 4),
                      ("Darsh – Assistant General Manager – Saturday", D_["Darsh"] == 6),
                      ("Faisal – Chief Manager – Sunday", R_["Faisal"] == 4)])
puzzle_q(sid, OTH, DSG, "Advanced", "Which of the following person – designation – day combinations is correct?",
         good, bad, "Check each part against the arrangement", "Chhavi is the Officer and reviews on Tuesday.",
         [ARR], why_others_wrong="Gita is the General Manager (not DGM); Darsh reviews on Wednesday; Faisal is the "
         "Senior Manager.", seconds=50)
nxt_ = next(p for p in P if D_[p] == D_[who(3)] + 1)
puzzle_q(sid, OTH, DAY, "Advanced", "Whose review is on the day immediately after the Assistant General Manager's "
         "review?", nxt_, ["Chhavi", "Ansh", "Eshita"], "Neighbour by day",
         "The AGM (Darsh) reviews on Wednesday; Thursday's review is Gita's.", [ARR, "Wednesday + 1 = Thursday ⇒ "
         "Gita"], why_others_wrong="Chhavi is the day before Darsh; Ansh is on Friday and Eshita on Saturday.",
         seconds=40)

finish("007", "Reasoning Ability topic package 2 for BATCH_007 (Month and Date-Based Puzzles, Puzzles (Other), "
       "Syllogism, Inequality): 43 original questions built by tools/packages/REAS_pkg2.py. Puzzles are brute-forced "
       "for a unique arrangement; syllogisms checked over every Venn-region model; inequalities over every integer "
       "ordering (with a wider-range cross-check).", draft="--draft" in sys.argv)


# ================================================================================================ BATCH_008
begin("008")

# ---------------------------------------------------------------- syllogism (B8 I4 A7)
syl_q("Basic", TWO, N(("sardine", "sardines"), ("prawn", "prawns"), ("lobster", "lobsters")),
      [("all", "sardine", "prawn"), ("some", "lobster", "sardine")],
      [("some", "lobster", "prawn"), ("all", "prawn", "sardine")], ONLY_I,
      "The lobsters that are sardines are inside the prawns, so some lobsters are prawns (I). 'All sardines are "
      "prawns' cannot be reversed into 'All prawns are sardines' (II).",
      ["Lobster ∩ sardine ≠ ∅ and sardines ⊂ prawns ⇒ some lobsters are prawns: I follows",
       "All A are B does not give All B are A ⇒ II not certain"])
syl_q("Basic", TWO, N(("fig", "figs"), ("peach", "peaches"), ("pear", "pears")),
      [("no", "fig", "peach"), ("all", "pear", "peach")],
      [("some", "fig", "pear"), ("no", "pear", "fig")], ONLY_II,
      "Every pear is a peach, and no peach is a fig, so no pear is a fig (II). That makes 'Some figs are pears' "
      "impossible (I).",
      ["All pears are peaches + No peach is a fig ⇒ No pear is a fig (All + No = No)", "II follows; I contradicts it"])
syl_q("Basic", TWO, N(("radish", "radishes"), ("turnip", "turnips"), ("cabbage", "cabbages")),
      [("some", "radish", "turnip"), ("no", "turnip", "cabbage")],
      [("some", "radish", "cabbage"), ("all", "cabbage", "turnip")], NEITHER,
      "Some + No gives only 'Some radishes are not cabbages'. Whether any radish is a cabbage is open, so I is not "
      "certain. 'No turnip is a cabbage' makes 'All cabbages are turnips' impossible (II).",
      ["Some radishes are turnips + No turnip is a cabbage ⇒ Some radishes are not cabbages (only this)",
       "I: not certain", "II: contradicts 'No turnip is a cabbage'"])
syl_q("Basic", TWO, N(("trumpet", "trumpets"), ("cymbal", "cymbals"), ("bugle", "bugles")),
      [("all", "trumpet", "cymbal"), ("all", "cymbal", "bugle")],
      [("all", "trumpet", "bugle"), ("some", "bugle", "trumpet")], BOTH,
      "Trumpets ⊂ cymbals ⊂ bugles, so all trumpets are bugles (I), and since there are trumpets, some bugles are "
      "trumpets (II).",
      ["All + All = All ⇒ All trumpets are bugles: I", "Conversion of I ⇒ Some bugles are trumpets: II"])
syl_q("Basic", TWO, N(("stapler", "staplers"), ("ruler", "rulers"), ("marker", "markers")),
      [("all", "stapler", "ruler"), ("some", "ruler", "marker")],
      [("some", "stapler", "marker"), ("no", "stapler", "marker")], EITHER,
      "The markers overlap the rulers, but not necessarily the part holding the staplers, so neither conclusion is "
      "certain. I and II are a complementary pair about staplers and markers: one of them must be true.",
      ["All + Some ⇒ no definite stapler–marker link", "'Some A are B' / 'No A is B' ⇒ complementary pair",
       "Either I or II follows"])
syl_q("Basic", TWO, N(("router", "routers"), ("modem", "modems"), ("printer", "printers")),
      [("no", "router", "modem"), ("some", "modem", "printer")],
      [("no", "router", "printer"), ("somenot", "printer", "router")], ONLY_II,
      "The printers that are modems can never be routers, so some printers are not routers (II). Printers outside the "
      "modems may be routers, so 'No router is a printer' is not certain (I).",
      ["Some printers are modems + No modem is a router ⇒ Some printers are not routers: II",
       "Printers outside modems are free ⇒ I not certain"])
syl_q("Basic", TWO, N(("lawyer", "lawyers"), ("judge", "judges"), ("tailor", "tailors")),
      [("all", "lawyer", "judge"), ("no", "tailor", "lawyer")],
      [("no", "tailor", "judge"), ("all", "judge", "lawyer")], NEITHER,
      "Tailors are outside the lawyers, but the judge circle is bigger than the lawyer circle, so tailors may still be "
      "judges: I is not certain. 'All lawyers are judges' does not reverse to 'All judges are lawyers' (II).",
      ["Tailors may overlap judges outside lawyers ⇒ I not certain", "All A are B ⇏ All B are A ⇒ II not certain"])
syl_pick("Basic", TWO, N(("temple", "temples"), ("fort", "forts"), ("palace", "palaces")),
         [("some", "temple", "fort"), ("no", "fort", "palace")],
         [("somenot", "temple", "palace"), ("no", "temple", "palace"), ("some", "palace", "temple"),
          ("all", "fort", "temple")],
         "The temples that are forts can never be palaces, so some temples are not palaces (Some + No = Some not).",
         ["Temple ∩ fort ≠ ∅", "Forts are outside palaces ⇒ Some temples are not palaces"],
         "'No temple is a palace' and 'Some palaces are temples' are each possible but not certain (temples outside "
         "the forts are free); 'All forts are temples' is not given.")
syl_q("Intermediate", FEW, N(("island", "islands"), ("desert", "deserts"), ("plateau", "plateaus")),
      [("onlyfew", "island", "desert"), ("all", "desert", "plateau")],
      [("some", "plateau", "island"), ("poss_no", "island", "plateau")], ONLY_I,
      "Some islands are deserts, and every desert is a plateau, so some plateaus are islands (I). Because that "
      "overlap must exist, 'No island being a plateau' is impossible (II).",
      ["Island ∩ desert ≠ ∅ and ⊂ plateaus ⇒ I follows", "Island ∩ plateau must be non-empty ⇒ II impossible"])
syl_q("Intermediate", FEW, N(("cliff", "cliffs"), ("cave", "caves"), ("beach", "beaches")),
      [("only", "cave", "cliff"), ("onlyfew", "beach", "cliff")],
      [("some", "cave", "beach"), ("somenot", "beach", "cliff")], BOTH,
      "'Only caves are cliffs' puts every cliff inside the caves. Some beaches are cliffs, hence caves, so some caves "
      "are beaches (I). 'Only a few beaches are cliffs' also says some beaches are not cliffs (II).",
      ["Only caves are cliffs ⇒ cliffs ⊂ caves", "Beach ∩ cliff ⊂ caves ⇒ I follows",
       "Only a few ⇒ some beaches are not cliffs: II follows"])
syl_q("Intermediate", POSS, N(("dune", "dunes"), ("lagoon", "lagoons"), ("volcano", "volcanoes")),
      [("all", "dune", "lagoon"), ("somenot", "volcano", "lagoon")],
      [("poss_all", "volcano", "dune"), ("some", "dune", "volcano")], NEITHER,
      "Some volcanoes lie outside the lagoons and so outside the dunes; hence all volcanoes can never be dunes (I "
      "fails). Dunes and volcanoes may or may not overlap, so 'Some dunes are volcanoes' is not certain (II).",
      ["Volcanoes outside lagoons are outside dunes ⇒ I impossible", "No forced dune–volcano overlap ⇒ II not certain"])
syl_q("Intermediate", TWO, N(("waterfall", "waterfalls"), ("stream", "streams"), ("bay", "bays"),
                              ("peak", "peaks")),
      [("some", "waterfall", "stream"), ("all", "stream", "bay"), ("no", "peak", "bay")],
      [("some", "peak", "waterfall"), ("somenot", "waterfall", "peak")], ONLY_II,
      "The waterfalls that are streams are bays, and no bay is a peak, so some waterfalls are not peaks (II). "
      "Waterfalls outside the streams may or may not be peaks, so I is not certain.",
      ["Waterfall ∩ stream ⊂ bays, which are outside peaks ⇒ II follows", "Other waterfalls are free ⇒ I not certain"])
syl_q("Advanced", POSS, N(("museum", "museums"), ("library", "libraries"), ("theatre", "theatres"),
                          ("stadium", "stadiums")),
      [("onlyfew", "museum", "library"), ("no", "library", "theatre"), ("all", "stadium", "theatre")],
      [("somenot", "museum", "stadium"), ("poss_some", "library", "stadium")], ONLY_I,
      "Some museums are libraries; libraries lie outside the theatres, and the stadiums lie inside the theatres, so "
      "those museums are not stadiums (I). For the same reason no library can ever be a stadium, so II is impossible.",
      ["Museum ∩ library ≠ ∅; libraries ∩ theatres = ∅; stadiums ⊂ theatres", "⇒ some museums are not stadiums: I",
       "⇒ libraries and stadiums never meet: II fails"])
syl_q("Advanced", FEW, N(("warehouse", "warehouses"), ("factory", "factories"), ("barn", "barns"),
                         ("shed", "sheds")),
      [("only", "factory", "warehouse"), ("some", "barn", "warehouse"), ("no", "shed", "factory")],
      [("poss_all", "barn", "shed"), ("somenot", "barn", "shed")], ONLY_II,
      "'Only factories are warehouses' puts every warehouse inside the factories. The barns that are warehouses are "
      "therefore factories, and no factory is a shed, so some barns are not sheds (II); all barns can never be sheds "
      "(I fails).",
      ["Warehouses ⊂ factories; factories ∩ sheds = ∅", "Barn ∩ warehouse ⊂ factories ⇒ not sheds",
       "⇒ II follows; I impossible"])
syl_q("Advanced", POSS, N(("potter", "potters"), ("baker", "bakers"), ("chef", "chefs"), ("plumber", "plumbers")),
      [("some", "potter", "baker"), ("onlyfew", "baker", "chef"), ("all", "chef", "plumber")],
      [("some", "potter", "chef"), ("poss_all", "baker", "chef")], NEITHER,
      "The potters that are bakers may all fall in the part of the bakers that is not chefs, so 'Some potters are "
      "chefs' is not certain (I). 'Only a few bakers are chefs' says some bakers are not chefs, so all bakers can never "
      "be chefs (II fails).",
      ["Potter ∩ baker may avoid chefs ⇒ I not certain", "Only a few ⇒ some bakers are not chefs ⇒ II impossible"])
syl_q("Advanced", POSS, N(("carpenter", "carpenters"), ("painter", "painters"), ("farmer", "farmers"),
                          ("umpire", "umpires")),
      [("all", "carpenter", "painter"), ("no", "painter", "farmer"), ("onlyfew", "umpire", "farmer")],
      [("no", "carpenter", "farmer"), ("poss_some", "umpire", "carpenter")], BOTH,
      "Carpenters ⊂ painters, and painters never meet farmers, so no carpenter is a farmer (I). Only a few umpires "
      "are farmers; the other umpires are unrestricted and may overlap the carpenters, so II is possible.",
      ["All + No = No ⇒ No carpenter is a farmer: I", "Umpires outside farmers are free ⇒ some may be carpenters: II"])
syl_q("Advanced", FEW, N(("juggler", "jugglers"), ("athlete", "athletes"), ("referee", "referees"),
                         ("sculptor", "sculptors")),
      [("only", "juggler", "athlete"), ("onlyfew", "referee", "athlete"), ("no", "sculptor", "juggler")],
      [("poss_all", "referee", "sculptor"), ("some", "juggler", "referee")], ONLY_II,
      "'Only jugglers are athletes' puts every athlete inside the jugglers. Some referees are athletes, so they are "
      "jugglers: some jugglers are referees (II). Those referees can never be sculptors (no sculptor is a juggler), "
      "so all referees being sculptors is impossible (I).",
      ["Athletes ⊂ jugglers", "Referee ∩ athlete ⊂ jugglers ⇒ II follows",
       "Jugglers ∩ sculptors = ∅ ⇒ some referees are never sculptors ⇒ I fails"])
syl_reverse("Advanced", POSS, N(("speaker", "speakers"), ("charger", "chargers"), ("cable", "cables")),
            [("somenot", "cable", "charger"), ("poss_all", "speaker", "cable")],
            [[("all", "speaker", "cable"), ("no", "cable", "charger")],
             [("some", "speaker", "cable"), ("all", "cable", "charger")],
             [("no", "speaker", "cable"), ("some", "cable", "charger")],
             [("onlyfew", "cable", "speaker"), ("all", "speaker", "charger")]],
            "With 'All speakers are cables. No cable is a charger.', no cable is a charger, so some cables are not "
            "chargers (I); and all speakers are cables, so II (a possibility) certainly holds.",
            ["Test each set", "Set 1: cables ∩ chargers = ∅ ⇒ I; speakers ⊂ cables ⇒ II"],
            "'Some speakers are cables. All cables are chargers.' makes I false; 'No speaker is a cable…' makes II "
            "impossible; 'Only a few cables are speakers. All speakers are chargers.' leaves the cables outside the "
            "speakers free to be chargers, so I is not certain.")
syl_q("Advanced", POSS, N(("battery", "batteries"), ("sensor", "sensors"), ("monitor", "monitors"),
                          ("scanner", "scanners")),
      [("no", "battery", "sensor"), ("some", "sensor", "monitor"), ("all", "monitor", "scanner")],
      [("poss_all", "battery", "scanner"), ("poss_all", "sensor", "battery")], ONLY_I,
      "Batteries are only kept away from sensors; the scanners include a large region outside the sensors, so all "
      "batteries may lie inside the scanners (I). 'No battery is a sensor' makes 'All sensors being batteries' "
      "impossible (II).",
      ["Batteries may sit in scanners outside sensors ⇒ I possible", "No battery is a sensor ⇒ II impossible"])

# ---------------------------------------------------------------- inequality (B2 I8 A5)
chain_q("Basic", "Q > Z ≥ E = N ≥ U > H", ["Q > N", "E > H"], BOTH,
        "All signs point the same way. Q > Z ≥ E = N gives Q > N (I), and E = N ≥ U > H gives E > H (II).",
        ["I: Q > Z ≥ E = N ⇒ Q > N, true", "II: E = N ≥ U > H ⇒ E > H, true"])
chain_q("Basic", "T ≤ C < X > O = A ≥ Y", ["T < A", "Y < C"], NEITHER,
        "Both conclusions compare a term left of X with a term right of X, and the chain turns at X (C < X > O), so no "
        "relation is fixed.",
        ["I: T ≤ C < X > O = A: turn at X ⇒ no relation", "II: Y ≤ A = O < X > C: turn at X ⇒ no relation"])

CLR = {"pink": ">", "blue": "<", "red": "≥", "grey": "≤", "green": "="}
CLR_TXT = ("In the questions of this set, colour words are used between two letters with these meanings:\n"
           "'A pink B' means 'A is greater than B'; 'A blue B' means 'A is smaller than B'; 'A red B' means 'A is "
           "either greater than or equal to B'; 'A grey B' means 'A is either smaller than or equal to B'; 'A green B' "
           "means 'A is equal to B'.\nAssuming the statements to be true, find which of the conclusions I and II "
           "is/are definitely true.")
sid = stimulus("passage", "Five colour words for comparisons", CLR_TXT, None,
               "Decode: pink means >, blue means <, red means ≥, grey means ≤ and green means =. Rewrite every "
               "statement with ordinary signs, join them into one chain and test each conclusion along it.")
coded_q("Intermediate", CLR, sid, ["M pink K", "K red F", "F green Z", "Z grey S"], ["M pink Z", "S pink K"], ONLY_I,
        "Decoded: M > K ≥ F = Z ≤ S. M > K ≥ F = Z gives M > Z (I). S and K are on opposite sides of the turn at Z, so "
        "S > K is not certain (II).",
        ["Decode: M > K, K ≥ F, F = Z, Z ≤ S", "Chain: M > K ≥ F = Z ≤ S", "I: M > Z, true",
         "II: K ≥ F = Z ≤ S: turn at Z ⇒ no relation"])
coded_q("Intermediate", CLR, sid, ["E blue R", "R grey N", "N pink L", "L green W"], ["E pink W", "E blue N"],
        ONLY_II,
        "Decoded: E < R ≤ N > L = W. E and W are on opposite sides of the turn at N, so E > W is not certain (I). "
        "E < R ≤ N gives E < N (II).",
        ["Decode: E < R, R ≤ N, N > L, L = W", "Chain: E < R ≤ N > L = W", "I: turn at N ⇒ no relation",
         "II: E < R ≤ N ⇒ E < N, true"])
coded_q("Intermediate", CLR, sid, ["G red B", "B green V", "V red Y", "Y pink H"], ["G pink V", "G green V"], EITHER,
        "Decoded: G ≥ B = V ≥ Y > H. Only G ≥ V is known; G > V and G = V are each uncertain, but one of them must "
        "hold.",
        ["Decode: G ≥ B, B = V, V ≥ Y, Y > H", "G ≥ B = V ⇒ G ≥ V", "I (G > V) and II (G = V) split '≥' ⇒ either"])
coded_q("Intermediate", CLR, sid, ["X grey T", "T blue D", "J pink D", "J red O"], ["X blue O", "O pink T"], NEITHER,
        "Decoded: X ≤ T < D < J ≥ O. O is compared with X and T across the turn at J (D < J ≥ O), so neither "
        "relation is fixed.",
        ["Decode: X ≤ T, T < D, J > D, J ≥ O", "Chain: X ≤ T < D < J ≥ O", "I and II cross the turn at J ⇒ "
         "no relation"])
multi_q("Intermediate", ["F ≤ L", "L < Y", "Y = C", "N ≥ C", "W < F"], ["N > F", "W < C"], BOTH,
        "Combined: W < F ≤ L < Y = C ≤ N. All signs point one way, with a strict sign on each path, so N > F (I) and "
        "W < C (II).",
        ["Chain: W < F ≤ L < Y = C ≤ N", "I: N ≥ C = Y > L ≥ F ⇒ N > F, true", "II: W < F ≤ L < Y = C ⇒ W < C, true"])
multi_q("Intermediate", ["R ≥ A", "A = I", "I > J", "P ≤ J", "P > V"], ["R > P", "V ≥ J"], ONLY_I,
        "Combined: R ≥ A = I > J ≥ P > V. R > P follows (I). J ≥ P > V gives J > V, so V ≥ J is false (II).",
        ["Chain: R ≥ A = I > J ≥ P > V", "I: R > P, true", "II: J > V ⇒ V ≥ J false"])
multi_q("Intermediate", ["K < Z", "Z ≥ O", "O > H", "H = B", "E ≥ K"], ["E < Z", "Z > B"], ONLY_II,
        "Combined: E ≥ K < Z ≥ O > H = B. E and Z are on opposite sides of the turn at K, so E < Z is not certain "
        "(I). Z ≥ O > H = B gives Z > B (II).",
        ["Chain: E ≥ K < Z ≥ O > H = B", "I: turn at K ⇒ no relation", "II: Z ≥ O > H = B ⇒ Z > B, true"])
multi_q("Intermediate", ["C > U", "U ≤ M", "M = Y", "Y < Q", "D ≤ C"], ["D > U", "Q > C"], NEITHER,
        "Combined: D ≤ C > U ≤ M = Y < Q. D ≤ C > U turns at C, and Q > … ≥ U < C turns at U, so neither conclusion "
        "is fixed.",
        ["Chain: D ≤ C > U ≤ M = Y < Q", "I: D ≤ C > U: turn at C ⇒ no relation",
         "II: C > U ≤ … < Q: turn at U ⇒ no relation"])
multi_q("Advanced", ["T ≥ K", "K > W", "W = E", "S ≤ E", "S > G", "H ≤ T", "H > B"], ["T > S", "B < K"], ONLY_I,
        "Combined: B < H ≤ T ≥ K > W = E ≥ S > G. T ≥ K > W = E ≥ S gives T > S (I). B < H ≤ T, then the chain turns "
        "at T (T ≥ K), so B and K are unrelated (II).",
        ["Chain: B < H ≤ T ≥ K > W = E ≥ S > G", "I: T > S, true", "II: B < H ≤ T ≥ K: turn at T ⇒ no relation"],
        seconds=75)
multi_q("Advanced", ["N < Y", "Y ≤ D", "D = U", "U < F", "F ≤ X", "R ≥ X"], ["R > Y", "N < X"], BOTH,
        "Combined: N < Y ≤ D = U < F ≤ X ≤ R. Every sign points one way and each path has a strict sign, so R > Y and "
        "N < X.",
        ["Chain: N < Y ≤ D = U < F ≤ X ≤ R", "I: R ≥ X ≥ F > U = D ≥ Y ⇒ R > Y, true",
         "II: N < Y ≤ … ≤ X ⇒ N < X, true"], seconds=65)
three_q("Advanced", DIRECT, "Statements: P > M; M ≥ J; J = A; A ≤ Q; Q < K; E ≥ P",
        ["P > M", "M ≥ J", "J = A", "A ≤ Q", "Q < K", "E ≥ P"], ["E > A", "K > J", "M ≥ Q"],
        [(1, 1, 1), (1, 0, 0), (0, 1, 0)],
        "Combined: E ≥ P > M ≥ J = A ≤ Q < K. E > A (I) and K > Q ≥ A = J, so K > J (II). M and Q are on opposite "
        "sides of the turn at A, so M ≥ Q is not certain (III).",
        ["Chain: E ≥ P > M ≥ J = A ≤ Q < K", "I: E > A, true", "II: K > Q ≥ A = J ⇒ K > J, true",
         "III: turn at A ⇒ not certain", "Only I and II"],
        "'All three' accepts III, which crosses a turn; 'Only I' and 'Only II' each miss a true conclusion.")
expr_q("Advanced", "In which of the following expressions is 'G > T' definitely false?",
       ["G ≤ L < R = T", "G ≥ L < R = T", "T ≥ L = R ≤ G", "G < L ≥ R > T"], never("G > T"),
       "In G ≤ L < R = T, G < T, so G > T can never hold. In each of the others G > T is possible for some values.",
       ["'Definitely false' ⇔ G ≤ T is forced", "G ≤ L < R = T ⇒ G < T ⇒ G > T false",
        "Others: the chain turns between G and T ⇒ G > T possible"],
       "G ≥ L < R = T, T ≥ L = R ≤ G and G < L ≥ R > T all turn between G and T, so G > T may or may not hold — it is "
       "not definitely false.", concept="'Definitely false' means the opposite relation is forced")
multi_q("Advanced", ["L ≥ Q", "Q < V", "V = I", "I ≥ R", "R > O", "M ≥ L"], ["M > O", "Q > R"], NEITHER,
        "Combined: M ≥ L ≥ Q < V = I ≥ R > O. M and O are separated by the turn at Q (Q < V); Q and R lie on either "
        "side of the turn at V = I. Neither conclusion is fixed.",
        ["Chain: M ≥ L ≥ Q < V = I ≥ R > O", "I: M … Q < V … O: turn at Q ⇒ no relation",
         "II: Q < V = I ≥ R: turn at V ⇒ no relation"], seconds=65)

# ---------------------------------------------------------------- month and date puzzles (B2 I7 A6)
# MB3 Basic: months that begin with the letter M
P = ["Vasu", "Wamiq", "Xena", "Yug", "Zara"]
MS = [1, 3, 5, 6, 7]
conds = [("Vasu's month and Wamiq's month both begin with the letter M, and Vasu's month comes first.",
          ("Vasu", "Wamiq"), lambda v, w: MNAME[v][0] == MNAME[w][0] == "M" and v < w),
         ("Xena's month has 30 days.", ("Xena",), lambda x: MDAYS[x] == 30),
         ("Yug's month is not January.", ("Yug",), lambda y: y != 1)]
S_ = unique(P, {p: MS for p in P}, conds, [P])
assert S_["Yug"] == 7 and S_["Zara"] == 1
mcq(MON, MB, "Basic", "Five friends Vasu, Wamiq, Xena, Yug and Zara each host a monthly book club meeting in a "
    "different month among January, March, May, June and July.\n" + bullets(conds) + "\n\nWho hosts the meeting in "
    "July?", "Yug", ["Zara", "Xena", "Wamiq"], "Use the month names and month lengths",
    "March and May are the only months here that begin with M, so Vasu hosts in March and Wamiq in May. June is the "
    "only 30-day month: Xena. January and July remain; Yug is not in January, so Yug hosts in July and Zara in "
    "January.", ["M-months: March (Vasu), May (Wamiq)", "30 days: June ⇒ Xena", "Yug ≠ January ⇒ Yug July"],
    why_others_wrong="Zara hosts in January, Xena in June and Wamiq in May.", seconds=35, verified_by=BRUTE)

# MB4 Basic: four meetings on the Sundays of November 2026 (1 November 2026 is a Sunday)
assert WD(2026, 11, 1) == "Sunday"
SUN = [d for d in range(1, 31) if WD(2026, 11, d) == "Sunday"]
assert SUN == [1, 8, 15, 22, 29]
P = ["Mohit", "Neel", "Ojas", "Parul"]
conds = [("Mohit's meeting is on the second Sunday of the month.", ("Mohit",), lambda m: m == SUN[1]),
         ("Neel's meeting is exactly two weeks after Mohit's.", ("Neel", "Mohit"), lambda n, m: n == m + 14),
         ("Ojas's meeting is on the last Sunday of the month.", ("Ojas",), lambda o: o == SUN[-1]),
         ("Parul's meeting is earlier than Mohit's.", ("Parul", "Mohit"), lambda p, m: p < m)]
S_ = unique(P, {p: SUN for p in P}, conds, [P])
free = [d for d in SUN if d not in S_.values()]
assert free == [15]
mcq(MON, DB, "Basic", "Four friends Mohit, Neel, Ojas and Parul each hold one meeting of their reading circle on a "
    "Sunday of November 2026, on four different Sundays. 1 November 2026 is a Sunday.\n" + bullets(conds) +
    "\n\nOn which Sunday of November is no meeting held?", "15 November", ["1 November", "22 November", "8 November"],
    "List the Sundays of the month first",
    "The Sundays are 1, 8, 15, 22 and 29 November. Mohit: 8th; Neel: 8 + 14 = 22nd; Ojas: 29th; Parul is earlier "
    "than Mohit: 1st. The Sunday left without a meeting is 15 November.",
    ["Sundays: 1, 8, 15, 22, 29", "Mohit 8, Neel 22, Ojas 29, Parul 1", "Free: 15 November"],
    why_others_wrong="1 November is Parul's, 22 November Neel's and 8 November Mohit's.", seconds=40,
    verified_by=BRUTE)

# MI2 Intermediate set: six exams on weekdays of March 2027 (1 March 2027 is a Monday)
assert WD(2027, 3, 1) == "Monday"
WDM = [d for d in range(1, 32) if dt.date(2027, 3, d).weekday() < 5]
wdn = lambda d: WD(2027, 3, d)
P = ["Chemistry", "Hindi", "Physics", "Sanskrit", "Statistics", "Zoology"]
conds = [("The Statistics exam is on the first Wednesday of the month.", ("Statistics",),
          lambda s: wdn(s) == "Wednesday" and s <= 7),
         ("The Physics exam is exactly 15 days after the Statistics exam.", ("Physics", "Statistics"),
          lambda p, s: p == s + 15),
         ("The Hindi exam is on the last Friday of the month.", ("Hindi",), lambda h: wdn(h) == "Friday" and h > 24),
         ("The Chemistry exam is on the same day of the week as the Physics exam, exactly one week earlier.",
          ("Chemistry", "Physics"), lambda c, p: c == p - 7),
         ("The Zoology exam is on the first Monday after the Chemistry exam.", ("Zoology", "Chemistry"),
          lambda z, c: wdn(z) == "Monday" and 0 < z - c <= 7),
         ("The Sanskrit exam is on a date that is a multiple of 10, before the Hindi exam.", ("Sanskrit", "Hindi"),
          lambda s, h: s % 10 == 0 and s < h)]
S_ = unique(P, {p: WDM for p in P}, conds, [P])
assert S_ == {"Chemistry": 11, "Hindi": 26, "Physics": 18, "Sanskrit": 10, "Statistics": 3, "Zoology": 15}
sid = stimulus("puzzle", "Six exams on the weekdays of March 2027",
               "Six exams — Chemistry, Hindi, Physics, Sanskrit, Statistics and Zoology — are held on six different "
               "dates in March 2027, one exam per date. No exam is held on a Saturday or a Sunday. 1 March 2027 is a "
               "Monday.", conds,
               "Mondays of March 2027: 1, 8, 15, 22, 29, so Wednesdays are 3, 10, 17, 24, 31 and Fridays 5, 12, 19, "
               "26. Statistics: first Wednesday, 3rd. Physics: 3 + 15 = 18th (Thursday). Hindi: last Friday, 26th. "
               "Chemistry: 18 − 7 = 11th (Thursday). Zoology: first Monday after the 11th, the 15th. Sanskrit: "
               "multiples of 10 are 10 (Wednesday), 20 (Saturday, no exams) and 30 (after Hindi), so the 10th.\n\n"
               "Order: Statistics 3 (Wed), Sanskrit 10 (Wed), Chemistry 11 (Thu), Zoology 15 (Mon), Physics 18 (Thu), "
               "Hindi 26 (Fri).")
ARR = "Statistics 3 Wed, Sanskrit 10 Wed, Chemistry 11 Thu, Zoology 15 Mon, Physics 18 Thu, Hindi 26 Fri"
btw = sum(1 for p in P if S_["Chemistry"] < S_[p] < S_["Hindi"])
assert btw == 2
puzzle_q(sid, MON, DB, "Intermediate", "How many exams are held between the Chemistry exam and the Hindi exam?",
         num_word(btw), ["Three", "One", "Four"], "Count strictly between two dates",
         "Chemistry is on the 11th and Hindi on the 26th; Zoology (15th) and Physics (18th) lie between: two.",
         [ARR, "Between 11 and 26: Zoology, Physics ⇒ 2"], why_others_wrong="Three counts one end; One misses Zoology "
         "or Physics; Four counts both ends.", natural=by_num, seconds=90)
puzzle_q(sid, MON, DB, "Intermediate", "On which day of the week is the Sanskrit exam held?", wdn(S_["Sanskrit"]),
         ["Saturday", "Tuesday", "Thursday"], "Weekday of a date from the 1st of the month",
         "The multiples of 10 are 10, 20 and 30; the 20th is a Saturday (no exams) and the 30th is after Hindi, so "
         "Sanskrit is on the 10th — a Wednesday (3rd + 7).", [ARR, "Sanskrit 10th = Wednesday"],
         why_others_wrong="Saturday is the 20th, which is not an exam day; Tuesday is the 30th, after Hindi; Thursday "
         "would be the 11th (Chemistry).", seconds=50)
gap = S_["Hindi"] - S_["Zoology"]
assert gap == 11
puzzle_q(sid, MON, DB, "Intermediate", "How many days after the Zoology exam is the Hindi exam held?", str(gap),
         ["8", "12", "15"], "Difference of dates in one month", "Zoology is on the 15th and Hindi on the 26th: 26 − 15 "
         "= 11 days.", [ARR, "26 − 15 = 11"], why_others_wrong="8 is the gap from Physics to Hindi; 12 and 15 come from "
         "wrong dates for Zoology (14th or 11th).", natural=int, seconds=45)
ans = next(p for p in P if S_[p] == 18)
puzzle_q(sid, MON, DB, "Intermediate", "Which exam is held on 18 March?", ans, ["Chemistry", "Zoology", "Hindi"],
         "Read the arrangement", "Physics is 15 days after Statistics (3rd): the 18th.", [ARR, "18 March: Physics"],
         why_others_wrong="Chemistry is on the 11th, Zoology on the 15th and Hindi on the 26th.", seconds=40)

# MI3 Intermediate set: seven book launches from April to October, three genres, no genre twice in a row
P = ["Amit", "Bhanu", "Charu", "Dhruva", "Esha", "Firdaus", "Gunjan"]
G3 = ["Poetry", "Fiction", "Travel"]
GV = ["g" + p for p in P]
VV = [x for p in P for x in (p, "g" + p)]
conds = [
    ("No two books launched in consecutive months are of the same genre.",
     [((a, "g" + a, b, "g" + b), lambda ma, ga, mb, gb: abs(ma - mb) != 1 or ga != gb)
      for a, b in itertools.combinations(P, 2)]),
    ("Three of the books are Poetry, two are Fiction and two are Travel.", tuple(GV),
     lambda *g: Counter(g) == Counter({"Poetry": 3, "Fiction": 2, "Travel": 2})),
    ("Charu's book, a Poetry book, is launched in July.", ("Charu", "gCharu"), lambda m, g: m == 7 and g == "Poetry"),
    ("Esha's book is launched in the month immediately before Charu's, and it is not a Fiction book.",
     ("Esha", "Charu", "gEsha"), lambda e, c, g: e == c - 1 and g != "Fiction"),
    ("Amit's book is launched in the first of the seven months and Gunjan's in the last, and neither of their books "
     "is Poetry.", ("Amit", "Gunjan", "gAmit", "gGunjan"),
     lambda a, g_, ga, gg: a == 4 and g_ == 10 and "Poetry" not in (ga, gg)),
    ("Firdaus's book is a Fiction book launched in a month that has 31 days.", ("Firdaus", "gFirdaus"),
     lambda f, g: g == "Fiction" and MDAYS[f] == 31),
    ("The two Fiction books are launched exactly four months apart.",
     [((a, "g" + a, b, "g" + b), lambda ma, ga, mb, gb: not (ga == gb == "Fiction") or abs(ma - mb) == 4)
      for a, b in itertools.combinations(P, 2)]),
    ("Bhanu's book is launched later than Dhruva's.", ("Bhanu", "Dhruva"), lambda b, d: b > d),
]
SS = all_sols(VV, {v: (range(4, 11) if v in P else G3) for v in VV}, conds, [P])
assert len(SS) == 1, len(SS)
S_ = SS[0]
assert ({p: S_[p] for p in P} == {"Amit": 4, "Dhruva": 5, "Esha": 6, "Charu": 7, "Firdaus": 8, "Bhanu": 9,
                                   "Gunjan": 10}
        and [S_["g" + p] for p in ["Amit", "Dhruva", "Esha", "Charu", "Firdaus", "Bhanu", "Gunjan"]] ==
        ["Fiction", "Poetry", "Travel", "Poetry", "Fiction", "Poetry", "Travel"])
sid = stimulus("puzzle", "Seven book launches from April to October, in three genres",
               "Seven authors Amit, Bhanu, Charu, Dhruva, Esha, Firdaus and Gunjan each launch one book in a different "
               "month from April to October of the same year. Each book belongs to one of three genres: Poetry, "
               "Fiction or Travel.", conds,
               "Charu: July, Poetry. Esha: June; her book is not Fiction, and it cannot be Poetry next to Charu's "
               "Poetry July, so it is Travel. Amit: April, Gunjan: October, neither Poetry. Two more Poetry books are "
               "needed among May, August and September (April and October are not Poetry); August touches Charu's "
               "Poetry July, so May and September are Poetry. Firdaus (Fiction, 31-day month: May or August) therefore "
               "takes August, and Dhruva and Bhanu take May and September — Bhanu later, so Dhruva May, Bhanu "
               "September. The second Fiction book must be four months from August: April (Amit), since October is "
               "only two months away. Gunjan's book is then Travel.\n\n"
               "Apr Amit (Fiction), May Dhruva (Poetry), Jun Esha (Travel), Jul Charu (Poetry), Aug Firdaus (Fiction), "
               "Sep Bhanu (Poetry), Oct Gunjan (Travel).")
ARR = ("Apr Amit–Fiction, May Dhruva–Poetry, Jun Esha–Travel, Jul Charu–Poetry, Aug Firdaus–Fiction, "
       "Sep Bhanu–Poetry, Oct Gunjan–Travel")
puzzle_q(sid, MON, MB, "Intermediate", "Whose book is launched in September?", "Bhanu", ["Dhruva", "Firdaus", "Gunjan"],
         "Combine the month clues with the genre counts", "Firdaus takes August, so Dhruva and Bhanu share May and "
         "September; Bhanu is later: September.", [ARR, "September: Bhanu"],
         why_others_wrong="Dhruva launches in May, Firdaus in August and Gunjan in October.", seconds=120)
puzzle_q(sid, MON, MB, "Intermediate", "Which genre is Gunjan's book?", S_["gGunjan"], ["Fiction", "Poetry",
         "Cannot be determined"], "Genre counts with a distance clue",
         "Firdaus's Fiction book is in August. The other Fiction book must be four months away: April is, October is "
         "not. So Amit's book is Fiction, and Gunjan's (not Poetry) is Travel.",
         [ARR, "Fiction: August and April ⇒ Amit", "Gunjan: Travel"], why_others_wrong="Fiction is Amit's genre (four "
         "months from August); Gunjan's book cannot be Poetry; the clues do fix the genre.", seconds=60)
cnt = sum(1 for p in P if S_["g" + p] == "Poetry" and S_[p] < 8)
assert cnt == 2
puzzle_q(sid, MON, MB, "Intermediate", "How many Poetry books are launched before August?", num_word(cnt),
         ["Three", "One", "None"], "Count with two attributes", "Poetry books: Dhruva (May), Charu (July) and Bhanu "
         "(September); two are before August.", [ARR, "May and July ⇒ 2"],
         why_others_wrong="Three counts Bhanu's September launch; One misses Dhruva's or Charu's; None ignores both.",
         natural=by_num, seconds=50)

# MA3 Advanced set: six bank branches and their opening years (ages counted in 2026)
P = ["Alwar", "Bidar", "Churu", "Dhule", "Etah", "Gonda"]
age = lambda y: 2026 - y
conds = [("In 2026, the Churu branch completes exactly 20 years.", ("Churu",), lambda c: age(c) == 20),
         ("In 2026, the Alwar branch is exactly twice as old as the Churu branch.", ("Alwar", "Churu"),
          lambda a, c: age(a) == 2 * age(c)),
         ("The Gonda branch opened seven years after the Churu branch.", ("Gonda", "Churu"), lambda g, c: g == c + 7),
         ("The Etah branch opened in a leap year, after the Churu branch but before the Gonda branch, and its age in "
          "2026 is a multiple of 7.", ("Etah", "Churu", "Gonda"),
          lambda e, c, g: isleap(e) and c < e < g and age(e) % 7 == 0),
         ("In 2026, the age of the Dhule branch equals the sum of the ages of the Gonda and Etah branches.",
          ("Dhule", "Gonda", "Etah"), lambda d, g, e: age(d) == age(g) + age(e)),
         ("The Bidar branch opened in the year in which the Alwar branch completed 10 years.", ("Bidar", "Alwar"),
          lambda b, a: b == a + 10)]
order = ["Churu", "Alwar", "Gonda", "Etah", "Dhule", "Bidar"]
S_ = unique(order, {p: range(1970, 2026) for p in order}, conds, [order])
assert S_ == {"Alwar": 1986, "Bidar": 1996, "Churu": 2006, "Dhule": 1999, "Etah": 2012, "Gonda": 2013}
sid = stimulus("puzzle", "Six bank branches and their opening years",
               "A bank opened six branches — Alwar, Bidar, Churu, Dhule, Etah and Gonda — in six different years. The "
               "age of a branch in a year is the number of years completed since it opened (a branch opened in 2006 is "
               "20 years old in 2026).", conds,
               "Churu: 2026 − 20 = 2006. Alwar: 40 years old, 1986. Gonda: 2013. Etah: a leap year after 2006 and "
               "before 2013 is 2008 or 2012; ages 18 and 14, and only 14 is a multiple of 7: 2012. Dhule: 13 + 14 = 27 "
               "years, 1999. Bidar: Alwar completed 10 years in 1996.\n\nOldest to newest: Alwar 1986, Bidar 1996, "
               "Dhule 1999, Churu 2006, Etah 2012, Gonda 2013.")
ARR = "Alwar 1986, Bidar 1996, Dhule 1999, Churu 2006, Etah 2012, Gonda 2013"
ans = next(p for p in P if age(S_[p]) == 30)
puzzle_q(sid, MON, YB, "Advanced", "Which branch completes 30 years in 2026?", ans, ["Dhule", "Alwar", "Churu"],
         "Age = 2026 − opening year", "2026 − 30 = 1996, the year Bidar opened.", [ARR, "1996 ⇒ Bidar"],
         why_others_wrong="Dhule is 27, Alwar 40 and Churu 20 years old in 2026.", seconds=150)
cnt = sum(isleap(S_[p]) for p in P)
assert cnt == 2
puzzle_q(sid, MON, YB, "Advanced", "How many of the six branches opened in a leap year?", num_word(cnt),
         ["One", "Three", "Four"], "Leap years are divisible by 4 (centuries by 400)",
         "Opening years: 1986, 1996, 1999, 2006, 2012, 2013. Divisible by 4: 1996 and 2012 — two.",
         [ARR, "1996 ✓, 2012 ✓, others ✗ ⇒ 2"], why_others_wrong="One forgets 1996 (Bidar); Three or Four count "
         "years such as 2006 or 1986 that are not divisible by 4.", natural=by_num, seconds=45)
yr = next(y for y in range(2026, 2100) if 2 * (y - S_["Gonda"]) == y - S_["Bidar"])
assert yr == 2030
puzzle_q(sid, MON, YB, "Advanced", "In which year will the Gonda branch be exactly half as old as the Bidar branch?",
         str(yr), ["2028", "2033", "2026"], "Age ratio with a constant gap",
         "Bidar is 2013 − 1996 = 17 years older than Gonda. Gonda is half as old as Bidar when Gonda's age equals that "
         "gap, 17: in 2013 + 17 = 2030 (Gonda 17, Bidar 34).",
         [ARR, "Gap = 17 years", "Half as old ⇔ Gonda's age = 17 ⇒ 2030"],
         why_others_wrong="2028 and 2033 give Gonda 15 and 20 years against Bidar's 32 and 37; in 2026 the ages are 13 "
         "and 30.", natural=int, seconds=75)
good, bad = one_true([("Dhule opened 13 years before Etah.", S_["Etah"] - S_["Dhule"] == 13),
                      ("Churu is the third oldest branch.", sorted(P, key=S_.get).index("Churu") == 2),
                      ("Alwar is 30 years older than Gonda.", S_["Gonda"] - S_["Alwar"] == 30),
                      ("Etah and Gonda opened in consecutive leap years.", False)])
puzzle_q(sid, MON, YB, "Advanced", "Which of the following statements is true?", good, bad,
         "Check each statement against the years", "Dhule opened in 1999 and Etah in 2012: 13 years apart.",
         [ARR, "2012 − 1999 = 13 ✓"], why_others_wrong="Churu is the fourth oldest (after Alwar, Bidar, Dhule); Alwar "
         "is 27 years older than Gonda; 2013 is not a leap year.", seconds=60)

# MA4 Advanced: a birthday on 29 February 2028
assert WD(2028, 1, 1) == "Saturday" and isleap(2028)
hb = dt.date(2028, 2, 29)
ib = hb + dt.timedelta(days=100)
ans = f"{ib.day} June, {ib.strftime('%A')}"
assert ans == "8 June, Thursday"
mcq(MON, DB, "Advanced", "Hiral was born on the only date that occurs in leap years alone, so she celebrates on that "
    "date in 2028. Her brother Inder's birthday in 2028 is exactly 100 days after Hiral's birthday. 1 January 2028 is "
    "a Saturday.\n\nOn which date and day of the week is Inder's birthday in 2028?", ans,
    ["7 June, Wednesday", "8 June, Wednesday", "9 June, Friday"], "Count days across months; use the leap day",
    "Hiral's birthday is 29 February. 1 January is a Saturday and 29 February is the 60th day of the year; 59 days "
    "later is 59 = 8 × 7 + 3 weekdays on: Saturday + 3 = Tuesday. Adding 100 days: March has 31 (to 31 March: 31 "
    "days), April 30 (61), May 31 (92), and 8 more days give 8 June. 100 = 14 × 7 + 2, so the weekday is Tuesday + 2 = "
    "Thursday.",
    ["29 Feb 2028: day 60; Saturday + 59 days ⇒ Tuesday", "29 Feb + 31 + 30 + 31 = 31 May (92 days); + 8 ⇒ 8 June",
     "100 = 14 weeks + 2 days ⇒ Thursday"],
    why_others_wrong="7 June miscounts the days by one; 8 June, Wednesday takes 100 days as 14 weeks + 1; 9 June, "
                     "Friday starts counting from 1 March.", seconds=110, verified_by=RECOMP)

# MA5 Advanced: months of 2026 with five Sundays or five Saturdays (1 January 2026 is a Thursday)
assert WD(2026, 1, 1) == "Thursday"
cntwd = lambda m, w: sum(1 for d in range(1, MDAYS[m] + 1) if WD(2026, m, d) == w)
P = ["Arnav", "Bulbul", "Chandan", "Damini", "Eklavya", "Falguni"]
conds = [("Bulbul's month has five Saturdays but only four Sundays.", ("Bulbul",),
          lambda b: cntwd(b, "Saturday") == 5 and cntwd(b, "Sunday") == 4),
         ("Damini's month has five Saturdays and five Sundays.", ("Damini",),
          lambda d: cntwd(d, "Saturday") == 5 and cntwd(d, "Sunday") == 5),
         ("Chandan's month has five Sundays.", ("Chandan",), lambda c: cntwd(c, "Sunday") == 5),
         ("Falguni's month begins on the same day of the week as Chandan's month.", ("Falguni", "Chandan"),
          lambda f, c: WD(2026, f, 1) == WD(2026, c, 1)),
         ("Arnav's month comes after Eklavya's month.", ("Arnav", "Eklavya"), lambda a, e: a > e)]
S_ = unique(P, {p: range(1, 7) for p in P}, conds, [P])
assert S_ == {"Arnav": 6, "Bulbul": 1, "Chandan": 3, "Damini": 5, "Eklavya": 4, "Falguni": 2}
ans = next(p for p in P if WD(2026, S_[p], 1) == "Wednesday")
assert ans == "Eklavya"
mcq(MON, MB, "Advanced", "Six volunteers Arnav, Bulbul, Chandan, Damini, Eklavya and Falguni each run a weekend camp "
    "in a different month from January to June 2026. 1 January 2026 is a Thursday, and 2026 is not a leap year.\n" +
    bullets(conds) + "\n\nWhose month begins on a Wednesday?", ans, ["Arnav", "Falguni", "Chandan"],
    "A month has five of a weekday only for the weekdays of its first (days − 28) days",
    "1sts of 2026: Jan Thu, Feb Sun, Mar Sun, Apr Wed, May Fri, Jun Mon. A 31-day month has five each of its first "
    "three weekdays, a 30-day month of its first two, and February only four of each. January (Thu, Fri, Sat): five "
    "Saturdays, four Sundays — Bulbul. May (Fri, Sat, Sun): five Saturdays and Sundays — Damini. March (Sun, Mon, Tue): "
    "five Sundays — Chandan. Falguni's month begins on a Sunday like March: February. April and June remain, Eklavya "
    "earlier: Eklavya April, Arnav June. April begins on a Wednesday: Eklavya.",
    ["1sts: Jan Thu, Feb Sun, Mar Sun, Apr Wed, May Fri, Jun Mon", "Five-of-a-kind days: Jan Thu–Sat, Mar Sun–Tue, "
     "Apr Wed–Thu, May Fri–Sun, Jun Mon–Tue", "Bulbul Jan, Damini May, Chandan Mar, Falguni Feb",
     "Eklavya Apr, Arnav Jun ⇒ Wednesday start: Eklavya"],
    why_others_wrong="Arnav's June begins on a Monday; Falguni's February and Chandan's March both begin on a Sunday.",
    seconds=130, verified_by=BRUTE)

# ---------------------------------------------------------------- other puzzles (A1)
P = ["Nandini", "Omesh", "Pari", "Qamar", "Riya", "Sahil"]
rk = lambda v, x: sum(1 for y in v if y > x)
ALL6 = tuple(P)
conds = [("Exactly two participants scored more than Pari, who scored 47.",
          [(("Pari",), lambda p: p == 47), (ALL6, lambda *v: rk(v, v[2]) == 2)]),
         ("Omesh scored 6 more than Riya and 4 less than Nandini.", ("Omesh", "Riya", "Nandini"),
          lambda o, r, n: o == r + 6 and n == o + 4),
         ("Qamar had the lowest score, 31, and the average of Qamar's and Riya's scores is 35.5.",
          [(("Qamar",), lambda q_: q_ == 31), (("Qamar", "Riya"), lambda q_, r: q_ + r == 71),
           (ALL6, lambda *v: min(v) == 31)]),
         ("The highest score was 55, and Sahil scored more than Nandini.",
          [(("Sahil", "Nandini"), lambda s, n: s > n), (ALL6, lambda *v: max(v) == 55)])]
SS = all_sols(["Qamar", "Riya", "Omesh", "Nandini", "Pari", "Sahil"], {p: range(31, 56) for p in P}, conds, [P])
assert len(SS) == 1 and SS[0] == {"Nandini": 50, "Omesh": 46, "Pari": 47, "Qamar": 31, "Riya": 40, "Sahil": 55}
S_ = SS[0]
ORD = sorted(P, key=lambda p: -S_[p])
assert ORD[3] == "Omesh"
mcq(OTH, CMP, "Advanced", "Six participants Nandini, Omesh, Pari, Qamar, Riya and Sahil took a quiz and got "
    "different scores (whole numbers).\n" + bullets(conds) + "\n\nWho has the fourth highest score?", "Omesh",
    ["Pari", "Riya", "Nandini"], "Fix the values from the numeric clues, then rank",
    "Qamar 31 and Riya + Qamar = 71 give Riya 40, so Omesh 46 and Nandini 50. Sahil beats Nandini and the top score "
    "is 55, so Sahil 55 (no one else can reach 55). Pari 47 with exactly Sahil and Nandini above her. Order: Sahil 55, "
    "Nandini 50, Pari 47, Omesh 46, Riya 40, Qamar 31. Fourth: Omesh.",
    ["Riya = 71 − 31 = 40; Omesh 46; Nandini 50", "Sahil > Nandini and max 55 ⇒ Sahil 55",
     "Order: Sahil, Nandini, Pari, Omesh, Riya, Qamar ⇒ fourth Omesh"],
    why_others_wrong="Pari is third, Riya fifth and Nandini second.", seconds=100, verified_by=BRUTE)

finish("008", "Reasoning Ability topic package 2 for BATCH_008 (Month and Date-Based Puzzles, Puzzles (Other), "
       "Syllogism, Inequality): 50 original questions built by tools/packages/REAS_pkg2.py. Puzzles are brute-forced "
       "for a unique arrangement or recomputed with datetime; syllogisms checked over every Venn-region model; "
       "inequalities over every integer ordering (with a wider-range cross-check).", draft="--draft" in sys.argv)


# ================================================================================================ BATCH_009
begin("009")

# ---------------------------------------------------------------- syllogism (B3 I4 A7)
syl_q("Basic", TWO, N(("monkey", "monkeys"), ("bear", "bears"), ("rabbit", "rabbits")),
      [("all", "monkey", "bear"), ("somenot", "rabbit", "bear")],
      [("some", "bear", "rabbit"), ("somenot", "rabbit", "monkey")], ONLY_II,
      "Some rabbits lie outside the bears; every monkey is inside the bears, so those rabbits are not monkeys (II). "
      "Whether any bear is a rabbit is open (I).",
      ["Rabbits outside bears are outside monkeys (monkeys ⊂ bears) ⇒ II follows",
       "Bears and rabbits need not overlap ⇒ I not certain"])
syl_q("Basic", TWO, N(("squirrel", "squirrels"), ("dolphin", "dolphins"), ("whale", "whales")),
      [("no", "squirrel", "dolphin"), ("all", "whale", "dolphin")],
      [("no", "whale", "squirrel"), ("somenot", "dolphin", "squirrel")], BOTH,
      "Whales ⊂ dolphins and dolphins never meet squirrels, so no whale is a squirrel (I). Since no dolphin is a "
      "squirrel and dolphins exist, some dolphins are not squirrels (II).",
      ["All whales are dolphins + No dolphin is a squirrel ⇒ No whale is a squirrel: I",
       "No dolphin is a squirrel ⇒ some dolphins are not squirrels: II"])
syl_q("Basic", TWO, N(("yak", "yaks"), ("goat", "goats"), ("donkey", "donkeys")),
      [("somenot", "yak", "goat"), ("all", "donkey", "goat")],
      [("some", "yak", "donkey"), ("no", "yak", "donkey")], EITHER,
      "The statements leave the yak–donkey relation open: yaks may or may not reach into the goats (where the donkeys "
      "are). So neither I nor II is certain, but they are a complementary pair: one must be true.",
      ["No definite yak–donkey relation", "'Some yaks are donkeys' / 'No yak is a donkey' ⇒ complementary pair",
       "Either I or II follows"])
syl_q("Intermediate", FEW, N(("biscuit", "biscuits"), ("muffin", "muffins"), ("samosa", "samosas")),
      [("only", "muffin", "biscuit"), ("no", "samosa", "muffin")],
      [("no", "biscuit", "samosa"), ("all", "muffin", "biscuit")], ONLY_I,
      "'Only muffins are biscuits' means every biscuit is a muffin. Muffins never meet samosas, so no biscuit is a "
      "samosa (I). The statement does not say every muffin is a biscuit (II) — that would be 'Only biscuits are "
      "muffins'.",
      ["Only muffins are biscuits ⇒ biscuits ⊂ muffins", "Muffins ∩ samosas = ∅ ⇒ I follows",
       "Muffins may extend beyond biscuits ⇒ II not certain"])
syl_q("Intermediate", FEW, N(("laddoo", "laddoos"), ("jalebi", "jalebis"), ("dosa", "dosas")),
      [("onlyfew", "laddoo", "jalebi"), ("onlyfew", "dosa", "jalebi")],
      [("some", "laddoo", "dosa"), ("all", "jalebi", "laddoo")], NEITHER,
      "Laddoos and dosas each overlap the jalebis only partly, and their overlaps may be different parts, so 'Some "
      "laddoos are dosas' is not certain (I). The jalebis meeting the dosas may lie outside the laddoos, so 'All "
      "jalebis are laddoos' is not certain either (II).",
      ["Two 'Only a few' statements with the middle term as predicate ⇒ no laddoo–dosa link",
       "Jalebi ∩ dosa may avoid laddoos ⇒ II not certain"])
syl_q("Intermediate", POSS, N(("pizza", "pizzas"), ("burger", "burgers"), ("noodle", "noodles")),
      [("all", "pizza", "burger"), ("onlyfew", "noodle", "burger")],
      [("poss_all", "noodle", "pizza"), ("poss_all", "burger", "noodle")], ONLY_II,
      "Some noodles are not burgers, and every pizza is a burger, so those noodles are not pizzas: all noodles can "
      "never be pizzas (I fails). The burgers may all lie inside the noodles — only a few noodles being burgers is "
      "still satisfied — so II is possible.",
      ["Noodles outside burgers are outside pizzas ⇒ I impossible",
       "Burgers ⊂ noodles keeps 'only a few noodles are burgers' true ⇒ II possible"])
syl_pick("Intermediate", POSS, N(("soup", "soups"), ("salad", "salads"), ("sandwich", "sandwiches")),
         [("no", "soup", "salad"), ("some", "salad", "sandwich")],
         [("poss_all", "sandwich", "soup"), ("poss_some", "soup", "sandwich"), ("poss_all", "salad", "soup"),
          ("some", "sandwich", "soup")],
         "The sandwiches outside the salads are unrestricted, so some of them may be soups: 'Some soups being "
         "sandwiches is a possibility' follows.",
         ["Soups only avoid salads", "Sandwiches outside salads may meet soups ⇒ possible"],
         "All sandwiches can never be soups (some sandwiches are salads); all salads being soups contradicts 'No soup "
         "is a salad'; 'Some sandwiches are soups' is possible but not definite.")
syl_q("Advanced", POSS, N(("lizard", "lizards"), ("snake", "snakes"), ("frog", "frogs"), ("turtle", "turtles")),
      [("all", "lizard", "snake"), ("some", "snake", "frog"), ("no", "frog", "turtle")],
      [("poss_all", "lizard", "frog"), ("somenot", "snake", "turtle")], BOTH,
      "The lizards may sit entirely inside the snake–frog overlap, so all lizards being frogs is possible (I). The "
      "snakes that are frogs can never be turtles, so some snakes are not turtles (II).",
      ["Lizards ⊂ snakes may fall inside snake ∩ frog ⇒ I possible",
       "Snake ∩ frog ≠ ∅ and outside turtles ⇒ II definite"])
syl_q("Advanced", POSS, N(("crab", "crabs"), ("snail", "snails"), ("moth", "moths"), ("beetle", "beetles")),
      [("onlyfew", "crab", "snail"), ("all", "snail", "moth"), ("no", "moth", "beetle")],
      [("somenot", "crab", "beetle"), ("poss_some", "beetle", "snail")], ONLY_I,
      "Some crabs are snails, snails ⊂ moths and moths never meet beetles, so those crabs are not beetles (I). For the "
      "same reason no snail can ever be a beetle, so II is impossible.",
      ["Crab ∩ snail ⊂ moths, outside beetles ⇒ I follows", "Snails ⊂ moths, moths ∩ beetles = ∅ ⇒ II impossible"])
syl_q("Advanced", POSS, N(("butterfly", "butterflies"), ("wasp", "wasps"), ("cricket", "crickets"),
                          ("hornet", "hornets")),
      [("some", "butterfly", "wasp"), ("no", "wasp", "cricket"), ("onlyfew", "cricket", "hornet")],
      [("poss_all", "hornet", "wasp"), ("no", "butterfly", "cricket")], NEITHER,
      "Some crickets are hornets, and no cricket is a wasp, so those hornets are not wasps: all hornets can never be "
      "wasps (I fails). Butterflies outside the wasps may be crickets, so 'No butterfly is a cricket' is not certain "
      "(II).",
      ["Hornet ∩ cricket ≠ ∅ and outside wasps ⇒ I impossible", "Butterflies outside wasps are free ⇒ II not certain"])
syl_q("Advanced", FEW, N(("vest", "vests"), ("skirt", "skirts"), ("cap", "caps"), ("hat", "hats")),
      [("only", "vest", "skirt"), ("onlyfew", "cap", "skirt"), ("no", "hat", "vest")],
      [("poss_all", "cap", "hat"), ("some", "vest", "cap")], ONLY_II,
      "'Only vests are skirts' puts every skirt inside the vests. Some caps are skirts, hence vests: some vests are "
      "caps (II). Those caps can never be hats (no hat is a vest), so all caps being hats is impossible (I).",
      ["Skirts ⊂ vests", "Cap ∩ skirt ⊂ vests ⇒ II follows", "Vests ∩ hats = ∅ ⇒ I impossible"])
syl_q("Advanced", TWO, N(("mitten", "mittens"), ("belt", "belts"), ("tie", "ties"), ("dhoti", "dhotis")),
      [("all", "mitten", "belt"), ("some", "belt", "tie"), ("no", "tie", "dhoti")],
      [("some", "mitten", "dhoti"), ("no", "mitten", "dhoti")], EITHER,
      "Mittens sit inside the belts, and dhotis are kept only out of the ties; the part of the belts outside the ties "
      "may or may not hold both mittens and dhotis. So neither conclusion is certain, but they form a complementary "
      "pair: one of them must be true.",
      ["No definite mitten–dhoti link", "I and II: 'Some A are B' / 'No A is B' ⇒ either"])
syl_q("Advanced", POSS, N(("bracelet", "bracelets"), ("anklet", "anklets"), ("earring", "earrings"),
                          ("necklace", "necklaces")),
      [("no", "bracelet", "anklet"), ("onlyfew", "anklet", "earring"), ("all", "earring", "necklace")],
      [("somenot", "necklace", "bracelet"), ("poss_all", "bracelet", "anklet")], ONLY_I,
      "Some anklets are earrings, hence necklaces, and no anklet is a bracelet: those necklaces are not bracelets "
      "(I). 'No bracelet is an anklet' makes 'All bracelets being anklets' impossible (II).",
      ["Anklet ∩ earring ⊂ necklaces, outside bracelets ⇒ I follows", "No bracelet is an anklet ⇒ II impossible"])
syl_q("Advanced", FEW, N(("bangle", "bangles"), ("brooch", "brooches"), ("locket", "lockets"),
                         ("pendant", "pendants")),
      [("only", "bangle", "brooch"), ("some", "locket", "brooch"), ("somenot", "pendant", "bangle")],
      [("poss_all", "pendant", "brooch"), ("all", "locket", "bangle")], NEITHER,
      "Some pendants are outside the bangles, and every brooch is inside the bangles ('Only bangles are brooches'), so "
      "all pendants can never be brooches (I fails). Lockets outside the brooches may be outside the bangles, so 'All "
      "lockets are bangles' is not certain (II).",
      ["Brooches ⊂ bangles; pendants outside bangles ⇒ I impossible", "Lockets outside brooches are free ⇒ II not "
       "certain"])

# ---------------------------------------------------------------- inequality (B8 I4 A7)
chain_q("Basic", "B ≤ R = E < Y ≥ P > L", ["B < Y", "L < E"], ONLY_I,
        "B ≤ R = E < Y gives B < Y (I). L < P ≤ Y and then the chain turns at Y (E < Y), so L and E are unrelated "
        "(II).", ["I: B ≤ R = E < Y ⇒ B < Y, true", "II: E < Y ≥ P > L: turn at Y ⇒ no relation"])
chain_q("Basic", "S > F ≥ A < C = O ≤ U", ["S > C", "U > A"], ONLY_II,
        "S > F ≥ A < C turns at A, so S and C are unrelated (I). U ≥ O = C > A gives U > A (II).",
        ["I: turn at A ⇒ no relation", "II: U ≥ O = C > A ⇒ U > A, true"])
chain_q("Basic", "Y ≥ M = G ≤ X < K > I", ["Y ≥ X", "I < X"], NEITHER,
        "Y ≥ M = G ≤ X turns at G, so Y and X are unrelated (I). X < K > I turns at K, so I and X are unrelated (II).",
        ["I: turn at G ⇒ no relation", "II: turn at K ⇒ no relation"])
chain_q("Basic", "N < W ≤ J ≤ H = D < Z", ["N < H", "Z > J"], BOTH,
        "Every sign points the same way. N < W ≤ J ≤ H gives N < H (I); Z > D = H ≥ J gives Z > J (II).",
        ["I: N < W ≤ J ≤ H ⇒ N < H, true", "II: Z > D = H ≥ J ⇒ Z > J, true"])

GRK = {"Γ": ">", "Λ": "<", "Ξ": "≥", "Π": "≤", "Ψ": "="}
GRK_TXT = ("In the questions of this set, the Greek capital letters Γ, Λ, Ξ, Π and Ψ are used with these meanings:\n"
           "'A Γ B' means 'A is greater than B'; 'A Λ B' means 'A is smaller than B'; 'A Ξ B' means 'A is either "
           "greater than or equal to B'; 'A Π B' means 'A is either smaller than or equal to B'; 'A Ψ B' means 'A is "
           "equal to B'.\nAssuming the statements to be true, find which of the conclusions I and II is/are definitely "
           "true.")
sid = stimulus("passage", "Five Greek capital letters for comparisons", GRK_TXT, None,
               "Decode: Γ means >, Λ means <, Ξ means ≥, Π means ≤ and Ψ means =. Rewrite the statements with ordinary "
               "signs, join them into a chain and test each conclusion.")
coded_q("Basic", GRK, sid, ["T Π K", "K Ψ B", "B Γ U"], ["T Λ B", "T Ψ B"], EITHER,
        "Decoded: T ≤ K = B > U, so T ≤ B. T < B and T = B are each uncertain, but one of them must hold.",
        ["Decode: T ≤ K, K = B, B > U", "T ≤ K = B ⇒ T ≤ B", "I (T < B) and II (T = B) split '≤' ⇒ either"],
        seconds=40)
coded_q("Basic", GRK, sid, ["R Ξ H", "H Γ M", "M Π D"], ["R Γ M", "D Γ H"], ONLY_I,
        "Decoded: R ≥ H > M ≤ D. R > M follows (I). D and H are on opposite sides of the turn at M, so D > H is not "
        "certain (II).", ["Decode: R ≥ H, H > M, M ≤ D", "I: R ≥ H > M ⇒ R > M, true", "II: turn at M ⇒ no relation"],
        seconds=40)
coded_q("Basic", GRK, sid, ["Z Λ Q", "Q Ψ C", "C Ξ F"], ["Z Λ F", "Q Ξ F"], ONLY_II,
        "Decoded: Z < Q = C ≥ F. Z and F lie on opposite sides of the turn at Q = C, so Z < F is not certain (I). "
        "Q = C ≥ F gives Q ≥ F (II).", ["Decode: Z < Q, Q = C, C ≥ F", "I: turn at C ⇒ no relation",
                                        "II: Q = C ≥ F ⇒ Q ≥ F, true"], seconds=40)
coded_q("Basic", GRK, sid, ["A Γ W", "W Ψ E", "E Λ V"], ["A Γ V", "W Γ V"], NEITHER,
        "Decoded: A > W = E < V. A and V lie on opposite sides of the turn at E, so A > V is not certain (I). "
        "W = E < V gives W < V, so W > V is false (II).",
        ["Decode: A > W, W = E, E < V", "I: A > W = E < V: turn at E ⇒ no relation", "II: W < V ⇒ W > V false"],
        seconds=40)
multi_q("Intermediate", ["P ≥ H", "H = X", "X > Y", "Y ≥ A", "C < A"], ["P > A", "C < X"], BOTH,
        "Combined: P ≥ H = X > Y ≥ A > C. All signs point one way with a strict sign on each path: P > A (I) and "
        "C < X (II).", ["Chain: P ≥ H = X > Y ≥ A > C", "I: P > A, true", "II: C < A ≤ Y < X ⇒ C < X, true"])
multi_q("Intermediate", ["M < E", "E ≤ O", "O = T", "T > J", "J ≥ U"], ["M < T", "U < E"], ONLY_I,
        "Combined: M < E ≤ O = T > J ≥ U. M < T follows (I). U and E are on opposite sides of the turn at T, so U < E "
        "is not certain (II).", ["Chain: M < E ≤ O = T > J ≥ U", "I: M < E ≤ O = T ⇒ M < T, true",
                                  "II: turn at T ⇒ no relation"])
multi_q("Intermediate", ["D ≥ K", "K < R", "R ≤ W", "W = Q", "L > D"], ["L > R", "Q > D"], NEITHER,
        "Combined: L > D ≥ K < R ≤ W = Q. Both conclusions compare a term left of K with a term right of K, and the "
        "chain turns at K (D ≥ K < R).", ["Chain: L > D ≥ K < R ≤ W = Q", "I and II cross the turn at K ⇒ no relation"])
multi_q("Intermediate", ["F = V", "V > N", "N ≥ B", "G ≥ B", "G < I"], ["F > G", "I > B"], ONLY_II,
        "Combined: F = V > N ≥ B ≤ G < I. F and G are on opposite sides of the turn at B, so F > G is not certain "
        "(I). I > G ≥ B gives I > B (II).", ["Chain: F = V > N ≥ B ≤ G < I", "I: turn at B ⇒ no relation",
                                              "II: I > G ≥ B ⇒ I > B, true"])

CHS = {"♔": ">", "♕": "≤", "♖": "=", "♗": "≥", "♘": "<"}
CHS_TXT = ("In the questions of this set, chess symbols are used between two letters with these meanings:\n"
           "'A ♔ B' means 'A is neither smaller than nor equal to B'; 'A ♕ B' means 'A is not greater than B'; 'A ♖ B' "
           "means 'A is neither greater than nor smaller than B'; 'A ♗ B' means 'A is not smaller than B'; 'A ♘ B' "
           "means 'A is neither greater than nor equal to B'.\nAssuming the statements to be true, find which of the "
           "conclusions I and II is/are definitely true.")
sid = stimulus("passage", "Five chess symbols defined by negations", CHS_TXT, None,
               "Translate each negation: 'neither smaller nor equal' = >, 'not greater' = ≤, 'neither greater nor "
               "smaller' = =, 'not smaller' = ≥, 'neither greater nor equal' = <. So ♔ is >, ♕ is ≤, ♖ is =, ♗ is ≥ "
               "and ♘ is <. Then join the statements into one chain.")
coded_q("Advanced", CHS, sid, ["J ♗ R", "R ♖ W", "W ♔ E", "S ♕ E", "S ♘ M"], ["J ♔ W", "J ♖ W"], EITHER,
        "Decoded: J ≥ R = W > E ≥ S < M. Only J ≥ W is known, so J > W and J = W are each uncertain, but one must "
        "hold.", ["Decode: J ≥ R, R = W, W > E, S ≤ E, S < M", "J ≥ R = W ⇒ J ≥ W",
                  "I (J > W) and II (J = W) split '≥' ⇒ either"], seconds=80)
coded_q("Advanced", CHS, sid, ["U ♘ N", "N ♕ T", "T ♖ I", "I ♘ O", "Y ♗ O"], ["U ♘ I", "Y ♔ N"], BOTH,
        "Decoded: U < N ≤ T = I < O ≤ Y. U < I (I) and Y ≥ O > I = T ≥ N gives Y > N (II).",
        ["Decode: U < N, N ≤ T, T = I, I < O, Y ≥ O", "Chain: U < N ≤ T = I < O ≤ Y", "I: U < I, true",
         "II: Y > N, true"], seconds=80)
coded_q("Advanced", CHS, sid, ["H ♔ L", "L ♗ F", "F ♘ D", "D ♖ P", "K ♗ D"], ["H ♔ D", "K ♗ L"], NEITHER,
        "Decoded: H > L ≥ F < D = P ≤ K. Both conclusions compare a term left of F with a term right of F, and the "
        "chain turns at F.", ["Decode: H > L, L ≥ F, F < D, D = P, K ≥ D", "Chain: H > L ≥ F < D = P ≤ K",
                              "I and II cross the turn at F ⇒ no relation"], seconds=80)
coded_q("Advanced", CHS, sid, ["C ♕ G", "G ♘ A", "A ♗ B", "B ♔ X", "X ♖ Z"], ["A ♔ Z", "C ♘ B"], ONLY_I,
        "Decoded: C ≤ G < A ≥ B > X = Z. A ≥ B > X = Z gives A > Z (I). C and B are on opposite sides of the turn at "
        "A, so C < B is not certain (II).", ["Decode: C ≤ G, G < A, A ≥ B, B > X, X = Z",
                                             "I: A > Z, true", "II: turn at A ⇒ no relation"], seconds=80)
multi_q("Advanced", ["Q ≥ E", "E > I", "I = H", "H ≤ V", "V < T", "W ≥ Q"], ["W > V", "T > I"], ONLY_II,
        "Combined: W ≥ Q ≥ E > I = H ≤ V < T. W and V are on opposite sides of the turn at H, so W > V is not certain "
        "(I). T > V ≥ H = I gives T > I (II).", ["Chain: W ≥ Q ≥ E > I = H ≤ V < T", "I: turn at H ⇒ no relation",
                                                  "II: T > V ≥ H = I ⇒ T > I, true"], seconds=65)
three_q("Advanced", DIRECT, "Statements: K < D; D ≤ P; P = Y; Y > G; G ≥ N; N > Z",
        ["K < D", "D ≤ P", "P = Y", "Y > G", "G ≥ N", "N > Z"], ["K < G", "P > N", "Z < P"],
        [(1, 1, 1), (0, 1, 0), (0, 0, 0)],
        "Combined: K < D ≤ P = Y > G ≥ N > Z. K and G lie on opposite sides of the turn at Y, so K < G is not certain "
        "(I). P = Y > G ≥ N gives P > N (II), and Z < N ≤ G < Y = P gives Z < P (III).",
        ["Chain: K < D ≤ P = Y > G ≥ N > Z", "I: turn at Y ⇒ not certain", "II: P > N, true", "III: Z < P, true",
         "Only II and III"],
        "'All three' accepts I, which crosses the turn at Y; 'Only II' misses III; 'None' misses both.")
expr_q("Advanced", "In which of the following expressions is 'M ≥ C' definitely true, but 'M > C' not definitely "
       "true?", ["M ≥ T = R ≥ C ≤ B", "M ≥ T > R = C < B", "M = T ≥ R ≤ C < B", "B ≤ M > T = R ≥ C"],
       lambda c: always("M ≥ C")(c) and not always("M > C")(c),
       "In M ≥ T = R ≥ C ≤ B, the path from M to C has only '≥' and '=' signs, so M ≥ C is certain but M = C is still "
       "possible — M > C is not certain.",
       ["Need: path M → C with no turn and no strict sign", "M ≥ T = R ≥ C: only ≥ and = ⇒ M ≥ C, not M > C"],
       "M ≥ T > R = C and B ≤ M > T = R ≥ C contain a strict sign, so M > C is definitely true as well; M = T ≥ R ≤ C "
       "turns at R, so even M ≥ C is not certain.",
       concept="'≥' certain but '>' not: the path must avoid every strict sign")

# ---------------------------------------------------------------- month and date puzzles (B8 I3 A4)
# MB set (Basic, 5 questions): six treks in six given months, read with the seasons
SEASON = {1: "Spring", 2: "Spring", 3: "Spring", 4: "Summer", 5: "Summer", 6: "Summer", 7: "Monsoon", 8: "Monsoon",
          9: "Monsoon", 10: "Winter", 11: "Winter", 12: "Winter"}
P = ["Aadi", "Bela", "Daksh", "Hema", "Ishan", "Kajal"]
MS = [1, 3, 4, 7, 10, 12]
conds = [("Hema treks in the only Summer month among the six.", ("Hema",), lambda h: SEASON[h] == "Summer"),
         ("Ishan treks in a Monsoon month.", ("Ishan",), lambda i: SEASON[i] == "Monsoon"),
         ("Kajal treks in the month that comes just before Hema's among the six months.", ("Kajal", "Hema"),
          lambda k, h: MS.index(k) == MS.index(h) - 1),
         ("Daksh and Bela both trek in Winter, and Bela's month is later.", ("Daksh", "Bela"),
          lambda d, b: SEASON[d] == SEASON[b] == "Winter" and d < b)]
S_ = unique(P, {p: MS for p in P}, conds, [P])
assert S_ == {"Aadi": 1, "Bela": 12, "Daksh": 10, "Hema": 4, "Ishan": 7, "Kajal": 3}
sid = stimulus("puzzle", "Six treks in six months, read by season",
               "Six friends Aadi, Bela, Daksh, Hema, Ishan and Kajal each go on one trek in the same year, in six "
               "different months among January, March, April, July, October and December. Take the seasons as: "
               "Spring = January to March, Summer = April to June, Monsoon = July to September, Winter = October to "
               "December.", conds,
               "Of the six months, only April is in Summer: Hema. Only July is in Monsoon: Ishan. The month before "
               "April in the list is March: Kajal. Winter months are October and December; Bela is later, so Daksh "
               "October and Bela December. Aadi takes the remaining month, January.\n\nJan Aadi, Mar Kajal, Apr Hema, "
               "Jul Ishan, Oct Daksh, Dec Bela.")
ARR = "Jan Aadi, Mar Kajal, Apr Hema, Jul Ishan, Oct Daksh, Dec Bela"
puzzle_q(sid, MON, MB, "Basic", "Who treks in January?", "Aadi", ["Kajal", "Daksh", "Bela"], "Seasons fix most months",
         "Every other month is taken by a clue, so Aadi gets January.", [ARR, "January: Aadi"],
         why_others_wrong="Kajal treks in March, Daksh in October and Bela in December.", seconds=60)
btw = sum(1 for p in P if S_["Kajal"] < S_[p] < S_["Bela"])
assert btw == 3
puzzle_q(sid, MON, MB, "Basic", "How many friends trek between Kajal and Bela?", num_word(btw), ["Two", "Four", "One"],
         "Count strictly between", "Kajal is in March and Bela in December; Hema, Ishan and Daksh lie between: three.",
         [ARR, "April, July, October ⇒ 3"], why_others_wrong="Two misses one of Hema, Ishan, Daksh; Four counts an "
         "end; One counts only Ishan.", natural=by_num, seconds=30)
puzzle_q(sid, MON, MB, "Basic", "In which month does Ishan trek?", MNAME[S_["Ishan"]], ["August", "October", "April"],
         "Season membership", "July is the only Monsoon month among the six.", [ARR, "Ishan: July"],
         why_others_wrong="August is not one of the six months; October is Daksh's and April Hema's.", seconds=25)
nx = MS[MS.index(S_["Ishan"]) + 1]
puzzle_q(sid, MON, MB, "Basic", "Who treks in the month that comes immediately after Ishan's among the six months?",
         next(p for p in P if S_[p] == nx), ["Bela", "Hema", "Aadi"], "Neighbour in the list of months",
         "After July comes October: Daksh.", [ARR, "October: Daksh"],
         why_others_wrong="Bela is in December, Hema in April (before July) and Aadi in January.", seconds=25)
cnt = sum(MDAYS[S_[p]] == 31 for p in P)
assert cnt == 5
puzzle_q(sid, MON, MB, "Basic", "How many of the friends trek in a month that has 31 days?", num_word(cnt),
         ["Four", "Six", "Three"], "Month lengths", "January, March, July, October and December have 31 days; only "
         "April has 30. So five friends.", [ARR, "31-day months: Jan, Mar, Jul, Oct, Dec ⇒ 5"],
         why_others_wrong="Four leaves out one 31-day month; Six counts April (30 days); Three counts only some.",
         natural=by_num, seconds=30)

# MB8 Basic: dates and weekdays inside one week
P = ["Leena", "Manas", "Nirav"]
mcq(MON, DB, "Basic", "In a certain month, the 14th is a Wednesday. Leena's birthday is on the 14th. Manas's birthday "
    "is three days after Leena's, and Nirav's birthday is on the Monday of the same week (the week runs from Monday to "
    "Sunday).\n\nOn which date is Nirav's birthday, and on which day of the week is Manas's birthday?",
    "12th; Saturday", ["13th; Saturday", "12th; Friday", "11th; Saturday"], "Count days forwards and backwards",
    "The Monday of the week that holds Wednesday the 14th is two days earlier: the 12th. Manas: 14 + 3 = 17th; "
    "Wednesday + 3 days = Saturday.",
    ["Wednesday 14 ⇒ Monday 12", "Manas: 17th = Wednesday + 3 = Saturday"],
    why_others_wrong="13th is a Tuesday; Friday is the 16th, only two days after Leena's; 11th is the Sunday of the "
                     "previous week.", seconds=30, verified_by=RECOMP)
assert (14 - 2, ["Wednesday", "Thursday", "Friday", "Saturday"][3]) == (12, "Saturday")

# MB9 Basic: four siblings born three years apart
P = ["Jugal", "Kirti", "Lakshmi", "Mohan"]
YR = [2001, 2004, 2007, 2010]
conds = [("Kirti is the eldest.", ("Kirti",), lambda k: k == 2001),
         ("Mohan is younger than Jugal but older than Lakshmi.", ("Mohan", "Jugal", "Lakshmi"),
          lambda m, j, l_: j < m < l_)]
S_ = unique(P, {p: YR for p in P}, conds, [P])
ans = 2026 - S_["Mohan"]
assert ans == 19
mcq(MON, YB, "Basic", "Four siblings Jugal, Kirti, Lakshmi and Mohan were born in 2001, 2004, 2007 and 2010, one in "
    "each year. Ages are counted in completed years on their birthdays.\n" + bullets(conds) + "\n\nHow old will Mohan "
    "be on his birthday in 2026?", str(ans), ["22", "16", "25"], "Order of birth years",
    "Kirti is the eldest: 2001. Jugal is older than Mohan, who is older than Lakshmi: Jugal 2004, Mohan 2007, Lakshmi "
    "2010. In 2026 Mohan turns 2026 − 2007 = 19.",
    ["Kirti 2001", "Jugal 2004, Mohan 2007, Lakshmi 2010", "2026 − 2007 = 19"],
    why_others_wrong="22 is Jugal's age, 16 Lakshmi's and 25 Kirti's.", natural=int, seconds=35, verified_by=BRUTE)

# MB10 Basic: four savings plans started months apart
P = ["Rina", "Sohan", "Tara", "Uday"]
conds = [("Rina starts in March.", ("Rina",), lambda r: r == 3),
         ("Sohan starts four months after Rina.", ("Sohan", "Rina"), lambda s, r: s == r + 4),
         ("Tara starts two months before Sohan.", ("Tara", "Sohan"), lambda t, s: t == s - 2),
         ("Uday starts in the month immediately after Tara's.", ("Uday", "Tara"), lambda u, t: u == t + 1)]
S_ = unique(P, {p: range(1, 13) for p in P}, conds, [P])
ans = next(p for p in P if S_[p] == 6)
assert ans == "Uday"
mcq(MON, MB, "Basic", "Four friends Rina, Sohan, Tara and Uday each start a monthly savings plan in a different month "
    "of the same year.\n" + bullets(conds) + "\n\nWho starts in June?", ans, ["Tara", "Sohan", "Rina"],
    "Chain of month gaps", "Rina: March. Sohan: March + 4 = July. Tara: July − 2 = May. Uday: May + 1 = June.",
    ["Rina Mar ⇒ Sohan Jul ⇒ Tara May ⇒ Uday Jun"],
    why_others_wrong="Tara starts in May, Sohan in July and Rina in March.", seconds=30, verified_by=BRUTE)

# MI4 Intermediate set: six appointments from Friday 25 September to Tuesday 6 October 2026
assert WD(2026, 9, 25) == "Friday"
DD = [dt.date(2026, 9, 25) + dt.timedelta(days=k) for k in range(12)]
P = ["Pranav", "Rukmini", "Sachin", "Tanvi", "Uttam", "Vidya"]
wdk = lambda k: DD[k].strftime("%A")
conds = [("Rukmini's appointment is on the last day of September.", ("Rukmini",),
          lambda r: DD[r] == dt.date(2026, 9, 30)),
         ("Pranav's appointment is exactly five days after Rukmini's.", ("Pranav", "Rukmini"), lambda p, r: p == r + 5),
         ("Tanvi's appointment is on the first Saturday of the period.", ("Tanvi",),
          lambda t: wdk(t) == "Saturday" and all(wdk(j) != "Saturday" for j in range(t))),
         ("Vidya's appointment is on a Friday in October.", ("Vidya",),
          lambda v: wdk(v) == "Friday" and DD[v].month == 10),
         ("Sachin's appointment is on the day after Vidya's.", ("Sachin", "Vidya"), lambda s, v: s == v + 1),
         ("Uttam's appointment is on a Monday, before Rukmini's.", ("Uttam", "Rukmini"),
          lambda u, r: wdk(u) == "Monday" and u < r)]
S_ = unique(P, {p: range(12) for p in P}, conds, [P])
DS = {p: DD[S_[p]] for p in P}
assert [DS[p].day for p in P] == [5, 30, 3, 26, 28, 2]
sid = stimulus("puzzle", "Six appointments across the end of September 2026",
               "Six persons Pranav, Rukmini, Sachin, Tanvi, Uttam and Vidya each have one appointment at a passport "
               "office on six different dates from Friday, 25 September 2026 to Tuesday, 6 October 2026 (September has "
               "30 days).", conds,
               "Days: Fri 25, Sat 26, Sun 27, Mon 28, Tue 29, Wed 30 September; Thu 1, Fri 2, Sat 3, Sun 4, Mon 5, Tue "
               "6 October. Rukmini 30 September; Pranav five days later, 5 October. Tanvi: first Saturday, 26 "
               "September. Vidya: the Friday in October, 2 October; Sachin 3 October. Uttam: a Monday before 30 "
               "September, 28 September.\n\nTanvi 26 Sep (Sat), Uttam 28 Sep (Mon), Rukmini 30 Sep (Wed), Vidya 2 Oct "
               "(Fri), Sachin 3 Oct (Sat), Pranav 5 Oct (Mon).")
ARR = "Tanvi 26 Sep Sat, Uttam 28 Sep Mon, Rukmini 30 Sep Wed, Vidya 2 Oct Fri, Sachin 3 Oct Sat, Pranav 5 Oct Mon"
cnt = sum(DS[p].month == 10 for p in P)
assert cnt == 3
puzzle_q(sid, MON, DB, "Intermediate", "How many of the six appointments are in October?", num_word(cnt),
         ["Two", "Four", "One"], "Carry dates over the month end", "Vidya (2 Oct), Sachin (3 Oct) and Pranav (5 Oct): "
         "three.", [ARR, "October: Vidya, Sachin, Pranav ⇒ 3"],
         why_others_wrong="Two misses Pranav, whose date crosses into October (30 Sep + 5 = 5 Oct); Four or One "
         "miscount.", natural=by_num, seconds=90)
gap = (DS["Pranav"] - DS["Tanvi"]).days
assert gap == 9
puzzle_q(sid, MON, DB, "Intermediate", "How many days after Tanvi's appointment is Pranav's appointment?", str(gap),
         ["10", "8", "11"], "Day count across a 30-day month", "26 September to 30 September is 4 days, and 5 more days "
         "reach 5 October: 9 days.", [ARR, "4 + 5 = 9"],
         why_others_wrong="10 treats September as a 31-day month; 8 and 11 miscount by a day or two.", natural=int,
         seconds=45)
puzzle_q(sid, MON, DB, "Intermediate", "On which day of the week is Rukmini's appointment?", DS["Rukmini"].strftime("%A"),
         ["Tuesday", "Thursday", "Monday"], "Weekday from a known date", "25 September is a Friday, so 30 September "
         "(five days later) is a Wednesday.", [ARR, "Fri 25 + 5 days ⇒ Wed 30"],
         why_others_wrong="Tuesday is 29 September, Thursday 1 October and Monday 28 September (Uttam).", seconds=35)

# MA6 Advanced set: retirement years (everyone retires in the year of the 60th birthday)
P = ["Gyan", "Hridya", "Kesar", "Lohit", "Mrinal", "Navya"]
ret = lambda b: b + 60
conds = [("Kesar retires in 2031.", ("Kesar",), lambda k: ret(k) == 2031),
         ("Lohit is seven years younger than Kesar.", ("Lohit", "Kesar"), lambda l_, k: l_ == k + 7),
         ("Gyan retires in 2026, and Navya is exactly ten years younger than Gyan.", ("Gyan", "Navya"),
          lambda g, n: ret(g) == 2026 and n == g + 10),
         ("Hridya was born in a leap year, after Kesar but before Lohit.", ("Hridya", "Kesar", "Lohit", "Navya"),
          lambda h, k, l_, n: isleap(h) and k < h < l_ and h != n),
         ("Mrinal is the youngest of the six, and Mrinal's age in 2026 is a perfect square.",
          [(("Mrinal",), lambda m: int((2026 - m) ** .5) ** 2 == 2026 - m),
           (tuple(P), lambda *v: v[4] == max(v))])]
order = ["Kesar", "Lohit", "Gyan", "Navya", "Hridya", "Mrinal"]
S_ = unique(order, {p: range(1960, 1996) for p in order}, conds, [order])
assert S_ == {"Gyan": 1966, "Hridya": 1972, "Kesar": 1971, "Lohit": 1978, "Mrinal": 1990, "Navya": 1976}
sid = stimulus("puzzle", "Six employees and their retirement years",
               "Six employees Gyan, Hridya, Kesar, Lohit, Mrinal and Navya of a bank were born in six different years "
               "between 1960 and 1995. Each employee retires in the year in which he or she turns 60.", conds,
               "Kesar: 2031 − 60 = 1971; Lohit 1978. Gyan: 2026 − 60 = 1966; Navya 1976. Hridya: a leap year after "
               "1971 and before 1978 — 1972 or 1976 — and 1976 is Navya's, so 1972. Mrinal is the youngest (after "
               "1978) and is a perfect-square age in 2026: 36 (born 1990) is the only one within 1979–1995 (25 would "
               "be 2001, 49 would be 1977).\n\nBirth / retirement: Gyan 1966/2026, Kesar 1971/2031, Hridya "
               "1972/2032, Navya 1976/2036, Lohit 1978/2038, Mrinal 1990/2050.")
ARR = "Gyan 1966/2026, Kesar 1971/2031, Hridya 1972/2032, Navya 1976/2036, Lohit 1978/2038, Mrinal 1990/2050"
ans = next(p for p in P if ret(S_[p]) == 2036)
puzzle_q(sid, MON, YB, "Advanced", "Who retires in 2036?", ans, ["Lohit", "Hridya", "Kesar"],
         "Retirement year = birth year + 60", "2036 − 60 = 1976: Navya (ten years younger than Gyan, born 1966).",
         [ARR, "1976 ⇒ Navya"], why_others_wrong="Lohit retires in 2038, Hridya in 2032 and Kesar in 2031.",
         seconds=150)
puzzle_q(sid, MON, YB, "Advanced", "In which year will Mrinal retire?", str(ret(S_["Mrinal"])),
         ["2045", "2051", "2038"], "Perfect-square age with a range", "Mrinal must be younger than Lohit (1978) and "
         "born by 1995: age in 2026 between 31 and 47. The only perfect square there is 36, so Mrinal was born in 1990 "
         "and retires in 2050.", [ARR, "Age 36 ⇒ 1990 ⇒ 2050"],
         why_others_wrong="2045 takes age 41; 2051 counts 61 years; 2038 is Lohit's retirement.", natural=int,
         seconds=60)
seq = sorted(P, key=lambda p: S_[p])
ans = seq[seq.index("Kesar") + 1]
assert ans == "Hridya"
puzzle_q(sid, MON, YB, "Advanced", "Who retires immediately after Kesar?", ans, ["Navya", "Lohit", "Gyan"],
         "Order of retirement = order of birth", "Kesar retires in 2031; the next retirement is Hridya's in 2032.",
         [ARR, "2031 Kesar ⇒ 2032 Hridya"], why_others_wrong="Navya retires in 2036 and Lohit in 2038, both later; "
         "Gyan retires first, in 2026.", seconds=45)
cnt = sum(isleap(S_[p]) for p in P)
assert cnt == 2
puzzle_q(sid, MON, YB, "Advanced", "How many of the six were born in a leap year?", num_word(cnt),
         ["One", "Three", "Four"], "Leap years are divisible by 4", "Birth years 1966, 1971, 1972, 1976, 1978, 1990; "
         "only 1972 and 1976 are divisible by 4: two.", [ARR, "1972 ✓, 1976 ✓ ⇒ 2"],
         why_others_wrong="One forgets Navya's 1976; Three or Four count years such as 1966 or 1990, which are not "
         "divisible by 4.", natural=by_num, seconds=45)

# ---------------------------------------------------------------- other puzzles (B1 I6 A2)
P = ["Ujala", "Vimal", "Waseem", "Xenia", "Yatin"]
conds = [("Ujala reached before Vimal but after Waseem.", ("Ujala", "Vimal", "Waseem"), lambda u, v, w: w < u < v),
         ("Yatin reached after Vimal.", ("Yatin", "Vimal"), lambda y, v: y > v),
         ("Xenia reached before Waseem.", ("Xenia", "Waseem"), lambda x, w: x < w)]
S_ = unique(P, {p: range(1, 6) for p in P}, conds, [P])
ans = next(p for p in P if S_[p] == 3)
assert ans == "Ujala"
mcq(OTH, CMP, "Basic", "Five colleagues Ujala, Vimal, Waseem, Xenia and Yatin reached the office at different times on "
    "Monday.\n" + bullets(conds) + "\n\nWho reached third?", ans, ["Waseem", "Vimal", "Xenia"], "One chain of 'before'",
    "Waseem < Ujala < Vimal < Yatin, and Xenia is before Waseem. Order: Xenia, Waseem, Ujala, Vimal, Yatin. Third: "
    "Ujala.", ["Xenia → Waseem → Ujala → Vimal → Yatin", "Third: Ujala"],
    why_others_wrong="Waseem is second, Vimal fourth and Xenia first.", seconds=35, verified_by=BRUTE)

# OI set (Intermediate, 4 questions): three departments, a Manager and an Executive in each, joining years
P = ["Aarav", "Bhakti", "Chaitali", "Devesh", "Eeshan", "Fiza"]
DEP = ["HR", "IT", "Sales"]
VV = [x for p in P for x in ("d" + p, "m" + p, "y" + p)]
DVS = tuple("d" + p for p in P) + tuple("m" + p for p in P)
conds = [
    ("Each department has exactly two of them: one Manager and one Executive, and in each department the Manager "
     "joined earlier than the Executive.",
     [(DVS, lambda *v: all(sum(1 for i in range(6) if v[i] == d) == 2 and
                           sum(v[6 + i] for i in range(6) if v[i] == d) == 1 for d in DEP))] +
     [(("d" + a, "m" + a, "y" + a, "d" + b, "m" + b, "y" + b),
       lambda da, ma, ya, db, mb, yb: not (da == db and ma == 1 and mb == 0) or ya < yb)
      for a in P for b in P if a != b]),
    ("Aarav, an Executive, joined last of the six.", ("yAarav", "mAarav"), lambda y, m: y == 2023 and m == 0),
    ("Devesh joined first of the six, and Bhakti works in the same department as Devesh.",
     ("yDevesh", "dDevesh", "dBhakti"), lambda y, d, b: y == 2018 and d == b),
    ("Fiza is a Manager and joined one year after Devesh.", ("mFiza", "yFiza"), lambda m, y: m == 1 and y == 2019),
    ("Chaitali works in Sales and joined in 2020.", ("dChaitali", "yChaitali"),
     lambda d, y: d == "Sales" and y == 2020),
    ("Eeshan joined in the year after Chaitali and works in the same department as her.",
     ("yEeshan", "dEeshan", "yChaitali", "dChaitali"), lambda y, d, yc, dc: y == yc + 1 and d == dc),
    ("Bhakti does not work in IT.", ("dBhakti",), lambda d: d != "IT"),
]
dom = {}
for p in P:
    dom |= {"d" + p: DEP, "m" + p: (0, 1), "y" + p: range(2018, 2024)}
S_ = unique(VV, dom, conds, [["y" + p for p in P]])
DP = {p: S_["d" + p] for p in P}
MG = {p: S_["m" + p] for p in P}
YJ = {p: S_["y" + p] for p in P}
assert DP == {"Aarav": "IT", "Bhakti": "HR", "Chaitali": "Sales", "Devesh": "HR", "Eeshan": "Sales", "Fiza": "IT"}
assert YJ == {"Aarav": 2023, "Bhakti": 2022, "Chaitali": 2020, "Devesh": 2018, "Eeshan": 2021, "Fiza": 2019}
sid = stimulus("puzzle", "Three departments, two posts each, six joining years",
               "Six employees Aarav, Bhakti, Chaitali, Devesh, Eeshan and Fiza work in three departments of a company "
               "— HR, IT and Sales. Each holds one of two posts, Manager or Executive, and each joined in a different "
               "year from 2018 to 2023.", conds,
               "Aarav joined in 2023 as an Executive; Devesh in 2018. Devesh joined before everyone, so he cannot be an "
               "Executive (his Manager would have joined earlier): Devesh is a Manager, and Bhakti, in his department, "
               "is its Executive. Fiza: Manager, 2019. Chaitali: Sales, 2020; Eeshan: Sales, 2021 — so Chaitali is the "
               "Sales Manager and Eeshan the Sales Executive. Sales is full, so Devesh and Bhakti are in HR or IT; "
               "Bhakti is not in IT, so both are in HR. Fiza then manages IT and Aarav is the IT Executive. Bhakti "
               "takes the remaining year, 2022.\n\nHR: Devesh (Manager, 2018), Bhakti (Executive, 2022); IT: Fiza "
               "(Manager, 2019), Aarav (Executive, 2023); Sales: Chaitali (Manager, 2020), Eeshan (Executive, 2021).")
ARR = ("HR: Devesh M 2018, Bhakti E 2022; IT: Fiza M 2019, Aarav E 2023; Sales: Chaitali M 2020, Eeshan E 2021")
puzzle_q(sid, OTH, DSG, "Intermediate", "Who is the Manager of the IT department?", "Fiza",
         ["Devesh", "Chaitali", "Aarav"], "Fill the departments one by one",
         "Sales has Chaitali and Eeshan; HR has Devesh and Bhakti; IT is left with Fiza (Manager) and Aarav.",
         [ARR, "IT Manager: Fiza"], why_others_wrong="Devesh manages HR, Chaitali manages Sales and Aarav is the IT "
         "Executive.", seconds=110)
puzzle_q(sid, OTH, DSG, "Intermediate", "In which year did Bhakti join?", str(YJ["Bhakti"]), ["2021", "2019", "2023"],
         "Remaining value", "2018 Devesh, 2019 Fiza, 2020 Chaitali, 2021 Eeshan, 2023 Aarav; Bhakti joined in 2022.",
         [ARR, "Bhakti: 2022"], why_others_wrong="2021 is Eeshan's year, 2019 Fiza's and 2023 Aarav's.", natural=int,
         seconds=40)
cnt = sum(1 for p in P if MG[p] == 0 and YJ[p] < 2023)
assert cnt == 2
puzzle_q(sid, OTH, DSG, "Intermediate", "How many Executives joined before 2023?", num_word(cnt),
         ["One", "Three", "None"], "Count with two attributes", "The Executives are Bhakti (2022), Aarav (2023) and "
         "Eeshan (2021); two joined before 2023.", [ARR, "Executives: Eeshan 2021, Bhakti 2022, Aarav 2023 ⇒ 2"],
         why_others_wrong="Three counts Aarav, who joined in 2023; One or None miss Eeshan or Bhakti.", natural=by_num,
         seconds=45)
good, bad = one_true([("Eeshan is the Sales Executive and joined in 2021.", DP["Eeshan"] == "Sales" and
                       MG["Eeshan"] == 0 and YJ["Eeshan"] == 2021),
                      ("Bhakti is the HR Manager.", MG["Bhakti"] == 1),
                      ("Fiza works in HR.", DP["Fiza"] == "HR"),
                      ("Chaitali joined after Eeshan.", YJ["Chaitali"] > YJ["Eeshan"])])
puzzle_q(sid, OTH, DSG, "Intermediate", "Which of the following statements is true?", good, bad,
         "Check each statement", "Eeshan joined in 2021, the year after Chaitali, as the Sales Executive.", [ARR],
         why_others_wrong="Bhakti is the HR Executive; Fiza works in IT; Chaitali joined before Eeshan.", seconds=45)

# OI5 Intermediate: seven shopping days from Wednesday to the next Tuesday
DN7 = ["Wednesday", "Thursday", "Friday", "Saturday", "Sunday", "Monday", "Tuesday"]
P = ["Gagan", "Heer", "Ikram", "Jaya", "Kanta", "Lucky", "Manav"]
conds = [("Exactly three persons shop between Heer and Kanta, and Heer shops before Kanta.", ("Heer", "Kanta"),
          lambda h, k: k - h == 4),
         ("Ikram shops on Saturday, and Jaya on the day immediately after Ikram.", ("Ikram", "Jaya"),
          lambda i, j: i == 3 and j == 4),
         ("Manav shops on the first of the seven days.", ("Manav",), lambda m: m == 0),
         ("Gagan shops later than Lucky.", ("Gagan", "Lucky"), lambda g_, l_: g_ > l_),
         ("Kanta does not shop on the last of the seven days.", ("Kanta",), lambda k: k != 6)]
S_ = unique(P, {p: range(7) for p in P}, conds, [P])
ans = next(p for p in P if DN7[S_[p]] == "Friday")
assert ans == "Lucky"
mcq(OTH, DAY, "Intermediate", "Seven persons Gagan, Heer, Ikram, Jaya, Kanta, Lucky and Manav each go grocery shopping "
    "on one of seven consecutive days, from a Wednesday to the following Tuesday, one person per day.\n" +
    bullets(conds) + "\n\nWho shops on Friday?", ans, ["Gagan", "Heer", "Kanta"], "A week that starts mid-week",
    "Days 1–7 are Wed, Thu, Fri, Sat, Sun, Mon, Tue. Manav Wed, Ikram Sat, Jaya Sun. Heer and Kanta are four days "
    "apart: (Thu, Mon) or (Fri, Tue); Kanta is not on Tuesday, so Heer Thu and Kanta Mon. Friday and Tuesday remain; "
    "Gagan is later than Lucky, so Lucky shops on Friday and Gagan on Tuesday.",
    ["Manav Wed, Ikram Sat, Jaya Sun", "Heer–Kanta 4 apart, Kanta ≠ Tue ⇒ Heer Thu, Kanta Mon",
     "Lucky Fri, Gagan Tue"], why_others_wrong="Gagan shops on Tuesday, Heer on Thursday and Kanta on Monday.",
    seconds=70, verified_by=BRUTE)

# OI6 Intermediate: six cyclists by speed
P = ["Ritesh", "Sonal", "Tara", "Umang", "Vipin", "Wahida"]
conds = [("Ritesh is faster than exactly two of the others.", tuple(P),
          lambda *v: sum(1 for x in v if x < v[0]) == 2),
         ("Sonal is faster than Ritesh.", ("Sonal", "Ritesh"), lambda s, r: s > r),
         ("Tara is slower than Umang but faster than Sonal.", ("Tara", "Umang", "Sonal"), lambda t, u, s: s < t < u),
         ("Vipin is not the slowest.", ("Vipin",), lambda v: v != 1)]
S_ = unique(P, {p: range(1, 7) for p in P}, conds, [P])  # 6 = fastest
ans = next(p for p in P if S_[p] == 2)
assert ans == "Vipin"
mcq(OTH, CMP, "Intermediate", "Six cyclists Ritesh, Sonal, Tara, Umang, Vipin and Wahida rode at different speeds in a "
    "race.\n" + bullets(conds) + "\n\nWho is the second slowest?", ans, ["Ritesh", "Wahida", "Sonal"],
    "Use 'exactly' counts to fix a position",
    "Umang > Tara > Sonal > Ritesh, and Ritesh is faster than exactly two cyclists — Vipin and Wahida, the only ones "
    "left. Vipin is not the slowest, so Wahida is last and Vipin second slowest.",
    ["Umang > Tara > Sonal > Ritesh", "Two below Ritesh: Vipin, Wahida", "Vipin not last ⇒ Vipin 5th (second "
     "slowest)"], why_others_wrong="Ritesh is the third slowest, Wahida the slowest and Sonal the fourth slowest.",
    seconds=60, verified_by=BRUTE)

# OA1 Advanced: seven visits from Monday to Sunday with counting clues
DNW = ["", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
P = ["Nikhil", "Pooja", "Rehana", "Sameer", "Tavleen", "Uday", "Vaani"]
conds = [("As many persons visit before Nikhil as visit after Pooja.", ("Nikhil", "Pooja"),
          lambda n, p: n - 1 == 7 - p),
         ("Exactly two persons visit between Nikhil and Rehana.", ("Nikhil", "Rehana"), lambda n, r: abs(n - r) == 3),
         ("Sameer visits on Thursday, and Rehana visits after Sameer.", ("Sameer", "Rehana"),
          lambda s, r: s == 4 and r > s),
         ("Tavleen visits after Uday, and exactly one person visits between Uday and Sameer.",
          ("Tavleen", "Uday", "Sameer"), lambda t, u, s: t > u and abs(u - s) == 2),
         ("Vaani visits before Nikhil.", ("Vaani", "Nikhil"), lambda v, n: v < n)]
S_ = unique(P, {p: range(1, 8) for p in P}, conds, [P])
assert S_ == {"Vaani": 1, "Uday": 2, "Nikhil": 3, "Sameer": 4, "Pooja": 5, "Rehana": 6, "Tavleen": 7}
ans = next(p for p in P if S_[p] == S_["Rehana"] - 1)
mcq(OTH, DAY, "Advanced", "Seven persons Nikhil, Pooja, Rehana, Sameer, Tavleen, Uday and Vaani each visit an art "
    "gallery on a different day of one week, from Monday to Sunday.\n" + bullets(conds) + "\n\nWho visits on the day "
    "immediately before Rehana?", ans, ["Sameer", "Tavleen", "Nikhil"], "Turn counting clues into positions",
    "Let Nikhil be day n and Pooja day p: n − 1 = 7 − p, so n + p = 8. Rehana is after Thursday (5, 6 or 7) and three "
    "days from Nikhil, so Nikhil is on day 2, 3 or 4; day 4 is Sameer's. Uday is two days from Sameer: day 2 or 6. "
    "Case Nikhil 2: Pooja 6, Rehana 5, Vaani 1, Uday must be 6 — taken by Pooja ✗. Case Nikhil 3: Pooja 5, Rehana 6, "
    "Uday 2 (day 6 is Rehana's), Tavleen after Uday and Vaani before Nikhil leave Vaani Monday and Tavleen Sunday. So: "
    "Mon Vaani, Tue Uday, Wed Nikhil, Thu Sameer, Fri Pooja, Sat Rehana, Sun Tavleen. The day before Rehana's is "
    "Pooja's.",
    ["Nikhil + Pooja = 8; Rehana ∈ {5, 6, 7} and |Nikhil − Rehana| = 3", "Nikhil 2 ⇒ Uday has no day ✗",
     "Nikhil 3 ⇒ Pooja 5, Rehana 6, Uday 2, Vaani 1, Tavleen 7", "Before Saturday (Rehana): Friday ⇒ Pooja"],
    why_others_wrong="Sameer is on Thursday, Tavleen on Sunday (after Rehana) and Nikhil on Wednesday.", seconds=120,
    verified_by=BRUTE)

# OA2 Advanced: ranks of five students in two tests
P = ["Ketan", "Lavi", "Mansi", "Neha", "Oindrila"]
VV = [x for p in P for x in ("a" + p, "b" + p)]
conds = [("No student has the same rank in both tests.", each(P, lambda p: (("a" + p, "b" + p),
                                                                            lambda a, b: a != b))),
         ("The student ranked 1st in Test 1 is ranked 3rd in Test 2.",
          each(P, lambda p: (("a" + p, "b" + p), lambda a, b: a != 1 or b == 3))),
         ("Lavi's rank in Test 2 is exactly two places better than in Test 1.", ("aLavi", "bLavi"),
          lambda a, b: b == a - 2),
         ("Oindrila is 2nd in Test 1 and last in Test 2.", ("aOindrila", "bOindrila"), lambda a, b: a == 2 and b == 5),
         ("Ketan's two ranks add up to 6.", ("aKetan", "bKetan"), lambda a, b: a + b == 6),
         ("Neha is ranked below Ketan in both tests.", ("aNeha", "aKetan", "bNeha", "bKetan"),
          lambda a, b, c, d: a > b and c > d)]
S_ = unique(VV, {v: range(1, 6) for v in VV}, conds, [["a" + p for p in P], ["b" + p for p in P]])
assert [(S_["a" + p], S_["b" + p]) for p in P] == [(4, 2), (3, 1), (1, 3), (5, 4), (2, 5)]
ans = next(p for p in P if S_["b" + p] == 4)
mcq(OTH, CMP, "Advanced", "Five students Ketan, Lavi, Mansi, Neha and Oindrila took two tests. In each test they got "
    "the ranks 1 to 5 (rank 1 is the best), with no ties.\n" + bullets(conds) + "\n\nWho is ranked 4th in Test 2?", ans,
    ["Ketan", "Mansi", "Lavi"], "Two rankings at once",
    "Oindrila: (2, 5). Ketan's ranks add to 6: (1, 5) and (2, 4) clash with Oindrila, (3, 3) repeats a rank, and "
    "(5, 1) leaves no room for Neha below Ketan in Test 1 — so Ketan is (4, 2). Neha is below Ketan in both: Test 1 "
    "rank 5, Test 2 rank 3 or 4. Lavi improves by two: Test 1 rank 3 → Test 2 rank 1 (rank 1 in Test 1 cannot "
    "improve). Mansi takes Test 1 rank 1 and so Test 2 rank 3, leaving Neha 4th in Test 2.",
    ["Oindrila (2, 5)", "Ketan (4, 2): the other sums fail", "Neha (5, ·); Lavi (3, 1)", "Mansi (1, 3) ⇒ Neha (5, 4)"],
    why_others_wrong="Ketan is 2nd in Test 2, Mansi 3rd and Lavi 1st.", seconds=120, verified_by=BRUTE)

finish("009", "Reasoning Ability topic package 2 for BATCH_009 (Month and Date-Based Puzzles, Puzzles (Other), "
       "Syllogism, Inequality): 57 original questions built by tools/packages/REAS_pkg2.py. Puzzles are brute-forced "
       "for a unique arrangement or recomputed with datetime; syllogisms checked over every Venn-region model; "
       "inequalities over every integer ordering (with a wider-range cross-check).", draft="--draft" in sys.argv)


# ================================================================================================ BATCH_010
begin("010")

# ---------------------------------------------------------------- syllogism (B5 I10 A2)
syl_q("Basic", TWO, N(("robin", "robins"), ("finch", "finches"), ("wren", "wrens")),
      [("all", "robin", "finch"), ("some", "wren", "robin")],
      [("some", "wren", "finch"), ("all", "finch", "wren")], ONLY_I,
      "The wrens that are robins are also finches, so some wrens are finches (I). Nothing says every finch is a wren "
      "(II).", ["Wren ∩ robin ≠ ∅ and robins ⊂ finches ⇒ I follows", "Finches outside wrens are possible ⇒ II not "
                "certain"])
syl_q("Basic", TWO, N(("magpie", "magpies"), ("cuckoo", "cuckoos"), ("oriole", "orioles")),
      [("some", "magpie", "cuckoo"), ("somenot", "cuckoo", "oriole")],
      [("some", "magpie", "oriole"), ("all", "oriole", "cuckoo")], NEITHER,
      "Two particular statements give no definite link: the magpies among the cuckoos may all lie in the part that is "
      "not orioles, so I is not certain; and orioles may lie outside the cuckoos, so II is not certain.",
      ["Some + Some not ⇒ no definite conclusion", "I and II both fail in some valid diagram"])
syl_q("Basic", TWO, N(("flamingo", "flamingos"), ("pelican", "pelicans"), ("toucan", "toucans")),
      [("some", "flamingo", "pelican"), ("all", "pelican", "toucan")],
      [("some", "toucan", "flamingo"), ("some", "flamingo", "toucan")], BOTH,
      "The flamingos that are pelicans are toucans, so some flamingos are toucans (II), which is the same as some "
      "toucans being flamingos (I).", ["Some + All = Some ⇒ Some flamingos are toucans: II",
                                       "Conversion ⇒ Some toucans are flamingos: I"])
syl_q("Basic", TWO, N(("invoice", "invoices"), ("voucher", "vouchers"), ("permit", "permits")),
      [("no", "invoice", "voucher"), ("all", "voucher", "permit")],
      [("no", "invoice", "permit"), ("somenot", "permit", "invoice")], ONLY_II,
      "The permits that are vouchers can never be invoices, so some permits are not invoices (II). Permits outside the "
      "vouchers may be invoices, so 'No invoice is a permit' is not certain (I).",
      ["Permit ∩ voucher ≠ ∅, outside invoices ⇒ II follows", "Invoices may meet permits outside vouchers ⇒ I not "
       "certain"])
syl_q("Basic", TWO, N(("deed", "deeds"), ("bond", "bonds"), ("licence", "licences")),
      [("some", "deed", "bond"), ("all", "licence", "bond")],
      [("some", "deed", "licence"), ("no", "deed", "licence")], EITHER,
      "Deeds and licences meet the bonds independently, so neither conclusion is certain. But 'Some deeds are "
      "licences' and 'No deed is a licence' cover every case between them, so one must be true.",
      ["No definite deed–licence link", "Complementary pair ⇒ either I or II follows"])
syl_q("Intermediate", FEW, N(("oven", "ovens"), ("toaster", "toasters"), ("grinder", "grinders")),
      [("onlyfew", "oven", "toaster"), ("no", "toaster", "grinder")],
      [("no", "oven", "grinder"), ("somenot", "oven", "grinder")], ONLY_II,
      "Some ovens are toasters and no toaster is a grinder, so those ovens are not grinders (II). The ovens outside "
      "the toasters may be grinders, so I is not certain.",
      ["Oven ∩ toaster ≠ ∅, outside grinders ⇒ II follows", "Ovens outside toasters are free ⇒ I not certain"])
syl_q("Intermediate", FEW, N(("mixer", "mixers"), ("blender", "blenders"), ("skillet", "skillets")),
      [("only", "mixer", "blender"), ("all", "skillet", "blender")],
      [("all", "skillet", "mixer"), ("all", "mixer", "skillet")], ONLY_I,
      "'Only mixers are blenders' puts every blender inside the mixers; skillets ⊂ blenders ⊂ mixers, so all "
      "skillets are mixers (I). The mixers may extend beyond the skillets (II).",
      ["Only mixers are blenders ⇒ blenders ⊂ mixers", "Skillets ⊂ blenders ⊂ mixers ⇒ I follows",
       "Reverse not given ⇒ II not certain"])
syl_q("Intermediate", POSS, N(("wicket", "wickets"), ("shuttle", "shuttles"), ("javelin", "javelins")),
      [("all", "wicket", "shuttle"), ("no", "javelin", "shuttle")],
      [("poss_some", "wicket", "javelin"), ("all", "shuttle", "wicket")], NEITHER,
      "Wickets ⊂ shuttles and javelins are outside the shuttles, so no wicket can be a javelin: I is impossible. 'All "
      "shuttles are wickets' reverses the first statement and is not certain (II).",
      ["Wickets ⊂ shuttles, javelins ∩ shuttles = ∅ ⇒ I impossible", "All A are B ⇏ All B are A ⇒ II not certain"])
syl_q("Intermediate", POSS, N(("discus", "discuses"), ("hurdle", "hurdles"), ("puck", "pucks")),
      [("some", "discus", "hurdle"), ("onlyfew", "hurdle", "puck")],
      [("poss_all", "discus", "puck"), ("poss_no", "discus", "puck")], BOTH,
      "Discuses and pucks are linked only through the hurdles, by two particular statements. All discuses may lie "
      "inside the pucks (I possible), or the discus–hurdle overlap may sit in the part of the hurdles that is not "
      "pucks, with no discus being a puck (II possible).",
      ["No definite discus–puck relation", "Both extreme cases fit the statements ⇒ both possibilities follow"])
syl_q("Intermediate", TWO, N(("envelope", "envelopes"), ("sticker", "stickers"), ("ribbon", "ribbons"),
                              ("binder", "binders")),
      [("all", "envelope", "sticker"), ("all", "sticker", "ribbon"), ("some", "binder", "envelope")],
      [("some", "binder", "ribbon"), ("all", "ribbon", "envelope")], ONLY_I,
      "Envelopes ⊂ stickers ⊂ ribbons, and some binders are envelopes, so those binders are ribbons (I). The ribbons "
      "may be far more than the envelopes (II).",
      ["Envelopes ⊂ stickers ⊂ ribbons", "Binder ∩ envelope ⊂ ribbons ⇒ I follows", "II reverses 'All' ⇒ not certain"])
syl_q("Intermediate", FEW, N(("architect", "architects"), ("dentist", "dentists"), ("cobbler", "cobblers")),
      [("only", "architect", "dentist"), ("onlyfew", "cobbler", "architect")],
      [("some", "cobbler", "dentist"), ("somenot", "cobbler", "dentist")], ONLY_II,
      "'Only architects are dentists' puts every dentist inside the architects. Some cobblers are not architects, so "
      "they are not dentists (II). The cobblers that are architects may or may not be dentists (I).",
      ["Dentists ⊂ architects", "Cobblers outside architects are outside dentists ⇒ II follows",
       "Cobbler ∩ architect may avoid dentists ⇒ I not certain"])
syl_q("Intermediate", FEW, N(("weaver", "weavers"), ("florist", "florists"), ("jeweller", "jewellers")),
      [("onlyfew", "weaver", "florist"), ("all", "jeweller", "florist")],
      [("some", "weaver", "jeweller"), ("all", "florist", "jeweller")], NEITHER,
      "The weavers who are florists may lie in the part of the florists that has no jewellers, so I is not certain. "
      "'All jewellers are florists' does not reverse (II).",
      ["Weaver ∩ florist may avoid jewellers ⇒ I not certain", "All A are B ⇏ All B are A ⇒ II not certain"])
syl_q("Intermediate", POSS, N(("mechanic", "mechanics"), ("electrician", "electricians"), ("librarian", "librarians")),
      [("no", "mechanic", "electrician"), ("some", "electrician", "librarian")],
      [("somenot", "librarian", "mechanic"), ("poss_all", "mechanic", "librarian")], BOTH,
      "The librarians who are electricians cannot be mechanics, so some librarians are not mechanics (I). The "
      "mechanics are only kept out of the electricians; they may all lie inside the librarians (II).",
      ["Librarian ∩ electrician ≠ ∅, outside mechanics ⇒ I definite", "Mechanics may sit in librarians outside "
       "electricians ⇒ II possible"])
syl_q("Intermediate", FEW, N(("van", "vans"), ("lorry", "lorries"), ("taxi", "taxis")),
      [("onlyfew", "van", "lorry"), ("onlyfew", "taxi", "lorry")],
      [("some", "van", "taxi"), ("no", "van", "taxi")], EITHER,
      "Vans and taxis each overlap the lorries only partly, so their own relation is open: neither I nor II is "
      "certain. They are a complementary pair, so one of them must be true.",
      ["No definite van–taxi relation", "'Some A are B' / 'No A is B' ⇒ either I or II"])
syl_pick("Intermediate", FEW, N(("ambulance", "ambulances"), ("tanker", "tankers"), ("sedan", "sedans")),
         [("only", "tanker", "ambulance"), ("no", "sedan", "tanker")],
         [("no", "ambulance", "sedan"), ("some", "tanker", "sedan"), ("all", "tanker", "ambulance"),
          ("some", "sedan", "ambulance")],
         "'Only tankers are ambulances' puts every ambulance inside the tankers; no sedan is a tanker, so no ambulance "
         "is a sedan.", ["Only tankers are ambulances ⇒ ambulances ⊂ tankers", "Tankers ∩ sedans = ∅ ⇒ No ambulance "
                         "is a sedan"],
         "'Some tankers are sedans' and 'Some sedans are ambulances' contradict the statements; 'All tankers are "
         "ambulances' reverses the 'Only' statement.")
syl_q("Advanced", POSS, N(("marsh", "marshes"), ("swamp", "swamps"), ("ridge", "ridges"), ("gorge", "gorges")),
      [("only", "ridge", "swamp"), ("some", "marsh", "swamp"), ("no", "gorge", "ridge")],
      [("somenot", "marsh", "gorge"), ("poss_all", "swamp", "gorge")], ONLY_I,
      "'Only ridges are swamps' puts every swamp inside the ridges, and no ridge is a gorge. The marshes that are "
      "swamps are therefore not gorges (I), and no swamp can ever be a gorge, so II is impossible.",
      ["Swamps ⊂ ridges, ridges ∩ gorges = ∅", "Marsh ∩ swamp ≠ ∅ ⇒ some marshes are not gorges: I",
       "Swamps never gorges ⇒ II fails"])
syl_q("Advanced", POSS, N(("oasis", "oases"), ("prairie", "prairies"), ("grove", "groves"), ("reef", "reefs")),
      [("some", "oasis", "prairie"), ("all", "prairie", "grove"), ("onlyfew", "reef", "grove")],
      [("poss_all", "reef", "prairie"), ("some", "oasis", "reef")], NEITHER,
      "Some reefs are not groves, and every prairie is a grove, so those reefs can never be prairies: I is impossible. "
      "Oases and reefs meet only through the groves, by particular statements, so II is not certain.",
      ["Reefs outside groves are outside prairies ⇒ I impossible", "No forced oasis–reef overlap ⇒ II not certain"])

# ---------------------------------------------------------------- inequality (B2 I4 A7)
chain_q("Basic", "H < D ≥ W = K > T ≥ Q", ["H < K", "W > Q"], ONLY_II,
        "H < D ≥ W turns at D, so H and K are unrelated (I). W = K > T ≥ Q gives W > Q (II).",
        ["I: turn at D ⇒ no relation", "II: W = K > T ≥ Q ⇒ W > Q, true"])
chain_q("Basic", "E = P ≥ G ≥ M < F ≤ J", ["E ≥ M", "J > G"], ONLY_I,
        "E = P ≥ G ≥ M gives E ≥ M (I). J ≥ F > M ≤ G turns at M, so J and G are unrelated (II).",
        ["I: E = P ≥ G ≥ M ⇒ E ≥ M, true", "II: turn at M ⇒ no relation"])

DIA = {"◆": ">", "◇": "≥", "▼": "<", "▽": "≤", "○": "="}
DIA_TXT = ("In the questions of this set, five shapes are used between two letters with these meanings:\n"
           "'A ◆ B' means 'A is greater than B'; 'A ◇ B' means 'A is either greater than or equal to B'; 'A ▼ B' means "
           "'A is smaller than B'; 'A ▽ B' means 'A is either smaller than or equal to B'; 'A ○ B' means 'A is equal "
           "to B'.\nAssuming the statements to be true, find which of the conclusions I and II is/are definitely "
           "true.")
sid = stimulus("passage", "Five filled and hollow shapes for comparisons", DIA_TXT, None,
               "Decode: ◆ means >, ◇ means ≥, ▼ means <, ▽ means ≤ and ○ means =. Rewrite the statements with ordinary "
               "signs, join them into a chain and test each conclusion.")
coded_q("Intermediate", DIA, sid, ["L ◆ R", "R ○ B", "B ▼ H", "H ◇ N"], ["L ◆ H", "N ◆ R"], NEITHER,
        "Decoded: L > R = B < H ≥ N. Both conclusions cross the turn at B (R = B < H), so neither is fixed.",
        ["Decode: L > R, R = B, B < H, H ≥ N", "Chain: L > R = B < H ≥ N", "I and II cross the turn at B ⇒ "
         "no relation"])
coded_q("Intermediate", DIA, sid, ["C ▽ Y", "Y ▼ U", "U ○ F", "F ◆ I"], ["C ▼ I", "U ◆ C"], ONLY_II,
        "Decoded: C ≤ Y < U = F > I. C and I are on opposite sides of the turn at U = F, so C < I is not certain (I). "
        "U > Y ≥ C gives U > C (II).", ["Decode: C ≤ Y, Y < U, U = F, F > I", "I: turn at F ⇒ no relation",
                                        "II: U > Y ≥ C ⇒ U > C, true"])
coded_q("Intermediate", DIA, sid, ["S ◇ A", "A ◆ O", "O ○ X", "X ◇ E"], ["S ◆ X", "A ◆ E"], BOTH,
        "Decoded: S ≥ A > O = X ≥ E. S > X (I) and A > E (II) both follow along one direction.",
        ["Decode: S ≥ A, A > O, O = X, X ≥ E", "I: S ≥ A > O = X ⇒ S > X, true", "II: A > O = X ≥ E ⇒ A > E, true"])
coded_q("Intermediate", DIA, sid, ["V ▼ G", "G ▽ T", "T ◆ P", "P ○ D"], ["V ▼ T", "D ▼ G"], ONLY_I,
        "Decoded: V < G ≤ T > P = D. V < T follows (I). D and G are on opposite sides of the turn at T, so D < G is "
        "not certain (II).", ["Decode: V < G, G ≤ T, T > P, P = D", "I: V < G ≤ T ⇒ V < T, true",
                              "II: turn at T ⇒ no relation"])
multi_q("Advanced", ["Z ≤ K", "K < B", "B ≥ W", "W > F", "F = A", "R ≥ Z"], ["R < B", "B > A"], ONLY_II,
        "Combined: R ≥ Z ≤ K < B ≥ W > F = A. R and B are on opposite sides of the turn at Z, so R < B is not certain "
        "(I). B ≥ W > F = A gives B > A (II).", ["Chain: R ≥ Z ≤ K < B ≥ W > F = A", "I: turn at Z ⇒ no relation",
                                                  "II: B > A, true"], seconds=65)
multi_q("Advanced", ["J > E", "E ≥ X", "X < L", "L = O", "O ≤ C", "M ≤ J"], ["M > X", "C > E"], NEITHER,
        "Combined: M ≤ J > E ≥ X < L = O ≤ C. M and X are separated by the turn at J (M ≤ J > E); C and E by the turn "
        "at X. Neither conclusion is fixed.", ["Chain: M ≤ J > E ≥ X < L = O ≤ C", "I: turn at J ⇒ no relation",
                                                "II: turn at X ⇒ no relation"], seconds=65)
multi_q("Advanced", ["G ≥ U", "U = Y", "Y > N", "N ≥ H", "H < D", "S < G"], ["G > H", "D > N"], ONLY_I,
        "Combined: S < G ≥ U = Y > N ≥ H < D. G ≥ U = Y > N ≥ H gives G > H (I). D and N are on opposite sides of the "
        "turn at H, so D > N is not certain (II).", ["Chain: S < G ≥ U = Y > N ≥ H < D", "I: G > H, true",
                                                      "II: turn at H ⇒ no relation"], seconds=65)
multi_q("Advanced", ["W ≤ O", "O < T", "T = R", "R ≤ K", "K < Q", "B ≤ W"], ["Q > O", "B < R"], BOTH,
        "Combined: B ≤ W ≤ O < T = R ≤ K < Q. Every sign points one way with a strict sign on each path: Q > O and "
        "B < R.", ["Chain: B ≤ W ≤ O < T = R ≤ K < Q", "I: Q > K ≥ R = T > O ⇒ Q > O, true",
                   "II: B ≤ W ≤ O < T = R ⇒ B < R, true"], seconds=65)
multi_q("Advanced", ["P ≥ F", "F = L", "L ≥ I", "I > C", "Y ≤ C"], ["P > L", "Y < F"], ONLY_II,
        "Combined: P ≥ F = L ≥ I > C ≥ Y. P ≥ F = L gives only P ≥ L, so P > L is not certain (I). Y ≤ C < I ≤ L = F "
        "gives Y < F (II).", ["Chain: P ≥ F = L ≥ I > C ≥ Y", "I: P ≥ L only ⇒ not certain",
                              "II: Y ≤ C < I ≤ L = F ⇒ Y < F, true"], seconds=60)
three_q("Advanced", DIRECT, "Statements: N ≥ X; X > Q; Q ≤ V; V = H; H < E; A ≤ N",
        ["N ≥ X", "X > Q", "Q ≤ V", "V = H", "H < E", "A ≤ N"], ["N > Q", "E > Q", "E > V"],
        [(1, 1, 0), (0, 1, 1), (1, 0, 1)],
        "Combined: A ≤ N ≥ X > Q ≤ V = H < E. N ≥ X > Q gives N > Q (I); E > H = V ≥ Q gives E > Q (II); E > H = V "
        "gives E > V (III). All three are true.",
        ["Chain: A ≤ N ≥ X > Q ≤ V = H < E", "I: N > Q, true", "II: E > Q, true", "III: E > V, true"],
        "Each of the other options drops one conclusion that does follow; none of I, II, III crosses the turn at Q.")
expr_q("Advanced", "In which of the following expressions is 'R > D' definitely true and 'R > K' definitely false?",
       ["K ≥ M = R > S ≥ D", "R > M ≥ D = S ≥ K", "K > M ≤ R > S ≥ D", "D < S = R ≥ M ≤ K"],
       lambda c: always("R > D")(c) and never("R > K")(c),
       "In K ≥ M = R > S ≥ D, R > S ≥ D gives R > D, and K ≥ M = R gives R ≤ K, so R > K can never hold.",
       ["Need R > D forced and R ≤ K forced", "K ≥ M = R ⇒ R ≤ K; R > S ≥ D ⇒ R > D"],
       "R > M ≥ D = S ≥ K makes R > K true; in K > M ≤ R > S ≥ D and D < S = R ≥ M ≤ K, R and K are separated by a "
       "turn at M, so R > K is possible rather than definitely false.",
       concept="Two requirements at once: one relation forced, another impossible")

# ---------------------------------------------------------------- month and date puzzles (B2 A1)
P = ["Arpita", "Bhola", "Chinmay", "Dimple", "Elvis"]
conds = [("Chinmay's birthday is in October.", ("Chinmay",), lambda c: c == 10),
         ("Bhola's birthday is in a 30-day month before Chinmay's.", ("Bhola", "Chinmay"),
          lambda b, c: MDAYS[b] == 30 and b < c),
         ("Dimple's birthday is three months after Arpita's.", ("Dimple", "Arpita"), lambda d, a: d == a + 3)]
S_ = unique(P, {p: range(8, 13) for p in P}, conds, [P])
assert S_ == {"Arpita": 8, "Bhola": 9, "Chinmay": 10, "Dimple": 11, "Elvis": 12}
mcq(MON, MB, "Basic", "Five friends Arpita, Bhola, Chinmay, Dimple and Elvis have their birthdays in five different "
    "months from August to December, one in each month.\n" + bullets(conds) + "\n\nWhose birthday is in November?",
    "Dimple", ["Elvis", "Arpita", "Bhola"], "Use the fixed month first",
    "Chinmay: October. Bhola: the 30-day month before October in the range is September. Dimple is three months after "
    "Arpita: of August, November and December, only August → November works. Elvis takes December. November: Dimple.",
    ["Chinmay Oct, Bhola Sep", "Arpita Aug ⇒ Dimple Nov", "Elvis Dec"],
    why_others_wrong="Elvis is in December, Arpita in August and Bhola in September.", seconds=35, verified_by=BRUTE)

pr = dt.date(2027, 1, 27) + dt.timedelta(days=9)
qr = pr + dt.timedelta(days=12)
assert (pr, qr) == (dt.date(2027, 2, 5), dt.date(2027, 2, 17))
mcq(MON, DB, "Basic", "Payal borrowed a library book on 27 January 2027 and returned it 9 days later. On the day Payal "
    "returned it, Qasim borrowed the same book and kept it for 12 days.\n\nOn which date did Qasim return the book?",
    "17 February 2027", ["16 February 2027", "18 February 2027", "14 February 2027"], "Adding days across a month end",
    "January has 31 days: 27 January + 4 days = 31 January, and 5 more days give 5 February (Payal's return). Qasim: "
    "5 February + 12 days = 17 February.", ["27 Jan + 9 = 5 Feb", "5 Feb + 12 = 17 Feb"],
    why_others_wrong="16 February and 18 February are one day off (counting 11 or 13 days for Qasim); 14 February "
                     "treats January as a 28-day month.",
    natural=lambda t: int(t.split()[0]), seconds=35, verified_by=RECOMP)

# MA7 Advanced: the next year with the same calendar as 2026
assert WD(2026, 1, 1) == "Thursday"
same = next(y for y in range(2027, 2100) if WD(y, 1, 1) == "Thursday" and not isleap(y))
assert same == 2037 and WD(2032, 1, 1) == "Thursday" and isleap(2032)
mcq(MON, YB, "Advanced", "1 January 2026 is a Thursday, and 2026 is not a leap year. Five friends each guess the next "
    "year after 2026 whose calendar is exactly the same as that of 2026 (every date falling on the same day of the "
    "week): Kavin says 2032, Leela says 2037, Mehr says 2043 and Nagesh says 2036.\n\nWhose guess is correct?",
    "Leela (2037)", ["Kavin (2032)", "Mehr (2043)", "Nagesh (2036)"], "Odd days: +1 for an ordinary year, +2 after a "
    "leap year",
    "A calendar repeats when 1 January falls on the same weekday and the year is of the same type (ordinary). Moving "
    "from one 1 January to the next adds 1 weekday after an ordinary year and 2 after a leap year: 2027 Fri, 2028 Sat "
    "(leap), 2029 Mon, 2030 Tue, 2031 Wed, 2032 Thu — but 2032 is a leap year, so its calendar differs after February. "
    "2033 Sat, 2034 Sun, 2035 Mon, 2036 Tue (leap), 2037 Thu, ordinary: 2037 repeats 2026.",
    ["1 Jan weekday: 2027 Fri, 2028 Sat, 2029 Mon, 2030 Tue, 2031 Wed, 2032 Thu (leap ✗)",
     "2033 Sat, 2034 Sun, 2035 Mon, 2036 Tue, 2037 Thu (ordinary ✓)"],
    why_others_wrong="2032 starts on a Thursday but is a leap year; 2043 also repeats 2026 but is not the next one; "
                     "2036 starts on a Tuesday.", seconds=90, verified_by=RECOMP)
assert WD(2043, 1, 1) == "Thursday" and not isleap(2043) and WD(2036, 1, 1) == "Tuesday"

# ---------------------------------------------------------------- other puzzles (B5 I1 A4)
P = ["Golu", "Hiya", "Jojo", "Kiku", "Lalli"]
conds = [("Hiya has more chocolates than Golu but fewer than Kiku.", ("Hiya", "Golu", "Kiku"),
          lambda h, g_, k: g_ < h < k),
         ("Jojo has fewer chocolates than Golu.", ("Jojo", "Golu"), lambda j, g_: j < g_),
         ("Lalli has more chocolates than Kiku.", ("Lalli", "Kiku"), lambda l_, k: l_ > k)]
S_ = unique(P, {p: range(1, 6) for p in P}, conds, [P])
assert sorted(P, key=lambda p: -S_[p]) == ["Lalli", "Kiku", "Hiya", "Golu", "Jojo"]
sid = stimulus("puzzle", "Five children and their chocolates",
               "Five children Golu, Hiya, Jojo, Kiku and Lalli have different numbers of chocolates.", conds,
               "Golu < Hiya < Kiku < Lalli, and Jojo < Golu. Order (most first): Lalli, Kiku, Hiya, Golu, Jojo.")
ARR = "Most to fewest: Lalli, Kiku, Hiya, Golu, Jojo"
puzzle_q(sid, OTH, CMP, "Basic", "Who has the most chocolates?", "Lalli", ["Kiku", "Hiya", "Golu"], "Top of the chain",
         "Lalli has more than Kiku, who has more than everyone else.", [ARR], why_others_wrong="Kiku is second, Hiya "
         "third and Golu fourth.", seconds=35)
puzzle_q(sid, OTH, CMP, "Basic", "Who is exactly in the middle of the order?", "Hiya", ["Golu", "Kiku", "Jojo"],
         "Middle of five = third", "Third of five: Hiya.", [ARR, "Third: Hiya"],
         why_others_wrong="Golu is fourth, Kiku second and Jojo fifth.", seconds=25)
puzzle_q(sid, OTH, CMP, "Basic", "How many children have fewer chocolates than Kiku?", "Three", ["Two", "Four", "One"],
         "Count below a position", "Hiya, Golu and Jojo: three.", [ARR, "Below Kiku: 3"],
         why_others_wrong="Two misses Jojo or Golu; Four includes Lalli, who has more; One counts only Hiya.",
         natural=by_num, seconds=25)

POSTS = ["", "Medical Superintendent", "Chief Medical Officer", "Senior Resident", "Junior Resident"]
P = ["Sunil", "Tanu", "Varsha", "Yusra"]
conds = [("Varsha is senior to Tanu but junior to Yusra.", ("Varsha", "Tanu", "Yusra"), lambda v, t, y: y < v < t),
         ("Sunil is not the Medical Superintendent.", ("Sunil",), lambda s: s != 1),
         ("Tanu is not the most junior.", ("Tanu",), lambda t: t != 4)]
S_ = unique(P, {p: range(1, 5) for p in P}, conds, [P])
ans = next(p for p in P if S_[p] == 3)
assert ans == "Tanu"
mcq(OTH, DSG, "Basic", "Four doctors Sunil, Tanu, Varsha and Yusra hold four posts in a hospital. In decreasing order "
    "of seniority the posts are: Medical Superintendent, Chief Medical Officer, Senior Resident and Junior Resident.\n" +
    bullets(conds) + "\n\nWho is the Senior Resident?", ans, ["Varsha", "Sunil", "Yusra"], "Seniority chain",
    "Yusra > Varsha > Tanu. Tanu is not the most junior, so Sunil is the Junior Resident and Tanu the Senior Resident; "
    "Varsha is the CMO and Yusra the Medical Superintendent (Sunil is not).",
    ["Yusra > Varsha > Tanu", "Tanu not last ⇒ Sunil Junior Resident", "Tanu Senior Resident"],
    why_others_wrong="Varsha is the CMO, Sunil the Junior Resident and Yusra the Medical Superintendent.", seconds=35,
    verified_by=BRUTE)

DN6 = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
P = ["Asha", "Babu", "Chand", "Dolly", "Elan", "Fatima"]
conds = [("Chand goes on Tuesday, and Babu on the day after Chand.", ("Chand", "Babu"),
          lambda c, b: c == 2 and b == 3),
         ("Asha goes on the first of the six days.", ("Asha",), lambda a: a == 0),
         ("Elan goes on Thursday.", ("Elan",), lambda e: e == 4),
         ("Fatima goes earlier in the week than Dolly.", ("Fatima", "Dolly"), lambda f, d: f < d)]
S_ = unique(P, {p: range(6) for p in P}, conds, [P])
ans = next(p for p in P if S_[p] == 5)
assert ans == "Dolly"
mcq(OTH, DAY, "Basic", "Six persons Asha, Babu, Chand, Dolly, Elan and Fatima each go to a swimming pool on one of six "
    "days from Sunday to Friday of the same week, one person per day.\n" + bullets(conds) + "\n\nWho goes on Friday?",
    ans, ["Fatima", "Elan", "Babu"], "Fill the fixed days first",
    "Asha Sunday, Chand Tuesday, Babu Wednesday, Elan Thursday. Monday and Friday remain; Fatima is earlier than "
    "Dolly, so Fatima Monday and Dolly Friday.", ["Asha Sun, Chand Tue, Babu Wed, Elan Thu",
                                                 "Fatima before Dolly ⇒ Fatima Mon, Dolly Fri"],
    why_others_wrong="Fatima goes on Monday, Elan on Thursday and Babu on Wednesday.", seconds=35, verified_by=BRUTE)

# OI Intermediate: four boxes compared on a balance
BX = ["P", "Q", "R", "S"]
bal = []
for w in itertools.permutations(range(1, 9), 4):
    P_, Q_, R_, S2 = w
    if P_ + Q_ == R_ + S2 and P_ + R_ > Q_ + S2 and P_ + S2 < Q_ + R_:
        bal.append(dict(zip(BX, w)))
assert bal and all(max(BX, key=m.get) == "R" for m in bal) and all(min(BX, key=m.get) == "S" for m in bal)
mcq(OTH, CMP, "Intermediate", "Four boxes P, Q, R and S have different weights. On a balance:\n"
    "- P and Q together exactly balance R and S together.\n- P and R together are heavier than Q and S together.\n"
    "- P and S together are lighter than Q and R together.\n\nWhich box is the heaviest?", "R", ["P", "Q", "S"],
    "Add and subtract the balance relations",
    "Write P + Q = R + S (1), P + R > Q + S (2), P + S < Q + R (3). (2) − (1): R − Q > Q − R, so R > Q. (1) + (3): "
    "2P + Q + S < 2R + Q + S, so R > P. From (1), R − P = Q − S, and R > P, so Q > S; also R > P and (2) + (1) give "
    "P > S. So R is heavier than P, Q and S.",
    ["(2) − (1) ⇒ R > Q", "(1) + (3) ⇒ R > P", "R > P > S (and Q > S) ⇒ R heaviest"],
    why_others_wrong="P and Q are each lighter than R; S is the lightest box.", seconds=90, verified_by=BRUTE)

# OA set (Advanced, 4 questions): six school posts and six subjects
P = ["Kamini", "Lokesh", "Madhav", "Naina", "Oorja", "Pratik"]
POSTS6 = ["", "Principal", "Vice-Principal", "Coordinator", "Senior Teacher", "Teacher", "Assistant Teacher"]
SUB = ["Maths", "Science", "English", "History", "Art", "Music"]
VV = [x for p in P for x in ("r" + p, "s" + p)]
rs = lambda p: ("r" + p, "s" + p)
conds = [
    ("The Maths teacher is senior to exactly four of the others.",
     each(P, lambda p: (rs(p), lambda r, s: s != "Maths" or r == 2))),
    ("The History teacher is the Principal.", each(P, lambda p: (rs(p), lambda r, s: s != "History" or r == 1))),
    ("Kamini is junior to the Maths teacher but senior to Pratik.",
     [(("rKamini", "rPratik"), lambda k, p: k < p)] +
     each(P, lambda p: (rs(p) + ("rKamini",), lambda r, s, k: s != "Maths" or r < k))),
    ("Lokesh is the most junior, and he teaches neither Music nor Art.", ("rLokesh", "sLokesh"),
     lambda r, s: r == 6 and s not in ("Music", "Art")),
    ("Pratik teaches Science, and Naina teaches Music and is junior to Pratik.",
     ("sPratik", "sNaina", "rNaina", "rPratik"), lambda sp, sn, rn, rp: sp == "Science" and sn == "Music" and rn > rp),
    ("Madhav is senior to Oorja.", ("rMadhav", "rOorja"), lambda m, o: m < o),
    ("The Art teacher is senior to the Science teacher.",
     [((("r" + a), "s" + a, "r" + b, "s" + b), lambda ra, sa, rb, sb: not (sa == "Art" and sb == "Science") or ra < rb)
      for a in P for b in P if a != b]),
]
S_ = unique(VV, {v: (range(1, 7) if v[0] == "r" else SUB) for v in VV}, conds,
            [["r" + p for p in P], ["s" + p for p in P]])
RK6 = {p: S_["r" + p] for p in P}
SB6 = {p: S_["s" + p] for p in P}
assert RK6 == {"Madhav": 1, "Oorja": 2, "Kamini": 3, "Pratik": 4, "Naina": 5, "Lokesh": 6}
assert SB6 == {"Madhav": "History", "Oorja": "Maths", "Kamini": "Art", "Pratik": "Science", "Naina": "Music",
               "Lokesh": "English"}
sid = stimulus("puzzle", "Six school posts and six subjects",
               "Six teachers Kamini, Lokesh, Madhav, Naina, Oorja and Pratik of a school hold six different posts. In "
               "decreasing order of seniority the posts are: Principal, Vice-Principal, Coordinator, Senior Teacher, "
               "Teacher and Assistant Teacher. Each teaches a different subject among Maths, Science, English, "
               "History, Art and Music.", conds,
               "The Maths teacher has four people below: Vice-Principal. The Principal teaches History. Lokesh is the "
               "Assistant Teacher (rank 6). Pratik teaches Science and Naina Music, Naina junior to Pratik; Kamini is "
               "junior to the Vice-Principal but senior to Pratik. So Kamini > Pratik > Naina > Lokesh fills ranks 3 "
               "to 6: Kamini Coordinator, Pratik Senior Teacher, Naina Teacher. Madhav and Oorja take ranks 1 and 2, "
               "Madhav senior: Madhav Principal (History), Oorja Vice-Principal (Maths). Lokesh teaches neither Music "
               "nor Art, so English; Kamini teaches Art (and is senior to the Science teacher, as required).\n\n"
               "Madhav Principal–History, Oorja VP–Maths, Kamini Coordinator–Art, Pratik Senior Teacher–Science, "
               "Naina Teacher–Music, Lokesh Assistant Teacher–English.")
ARR = ("Madhav Principal–History, Oorja VP–Maths, Kamini Coordinator–Art, Pratik Senior Teacher–Science, Naina "
       "Teacher–Music, Lokesh Asst Teacher–English")
puzzle_q(sid, OTH, DSG, "Advanced", "Who is the Coordinator?", "Kamini", ["Pratik", "Oorja", "Naina"],
         "Chain the seniority clues", "Kamini > Pratik > Naina > Lokesh occupy ranks 3–6, so Kamini is the "
         "Coordinator.", [ARR], why_others_wrong="Pratik is the Senior Teacher, Oorja the Vice-Principal and Naina "
         "the Teacher.", seconds=150)
puzzle_q(sid, OTH, DSG, "Advanced", "Which subject does Lokesh teach?", SB6["Lokesh"], ["Art", "Maths", "History"],
         "Eliminate subjects", "Maths (Oorja), History (Madhav), Science (Pratik) and Music (Naina) are taken; Lokesh "
         "does not teach Art, so English.", [ARR, "Lokesh: English"],
         why_others_wrong="Art is Kamini's subject, Maths Oorja's and History Madhav's.", seconds=45)
puzzle_q(sid, OTH, DSG, "Advanced", "Who teaches Maths?", "Oorja", ["Madhav", "Kamini", "Pratik"],
         "Rank of the Maths teacher", "The Maths teacher is the Vice-Principal; Madhav is senior to Oorja, so Madhav is "
         "the Principal and Oorja the Vice-Principal who teaches Maths.", [ARR, "VP = Oorja ⇒ Maths"],
         why_others_wrong="Madhav teaches History, Kamini Art and Pratik Science.", seconds=45)
good, bad = one_true([("Naina – Teacher – Music", RK6["Naina"] == 5 and SB6["Naina"] == "Music"),
                      ("Pratik – Coordinator – Science", RK6["Pratik"] == 3),
                      ("Madhav – Vice-Principal – History", RK6["Madhav"] == 2),
                      ("Kamini – Senior Teacher – Art", RK6["Kamini"] == 4)])
puzzle_q(sid, OTH, DSG, "Advanced", "Which of the following person – post – subject combinations is correct?", good,
         bad, "Check each part", "Naina is the Teacher and teaches Music.", [ARR],
         why_others_wrong="Pratik is the Senior Teacher, Madhav the Principal and Kamini the Coordinator.", seconds=50)

finish("010", "Reasoning Ability topic package 2 for BATCH_010 (Month and Date-Based Puzzles, Puzzles (Other), "
       "Syllogism, Inequality): 43 original questions built by tools/packages/REAS_pkg2.py. Puzzles are brute-forced "
       "for a unique arrangement or recomputed with datetime; syllogisms checked over every Venn-region model; "
       "inequalities over every integer ordering (with a wider-range cross-check).", draft="--draft" in sys.argv)

# ================================================================================================ write
if "--draft" not in sys.argv:
    assert sorted(DONE) == sorted(PLAN["batches"])
    assert sum(len(d["questions"]) for d in DONE.values()) == PLAN["total"]
    # 66 questions answered blind by a separate fresh solver (key-free dump, every third question per batch);
    # all 66 matched the key and were not changed afterwards.
    INDEP = {f"BANK_REAS_{n:06d}" for a, b in ((1257, 1299), (1457, 1506), (1649, 1705), (1857, 1899))
             for n in range(a, b + 1, 3)}
    assert len(INDEP) == 66
    for doc in DONE.values():
        for x in doc["questions"]:
            if x["question_id"] in INDEP:
                x["verification"]["verified_by"].append("ai:independent-check")
    for nnn, doc in DONE.items():
        out = ROOT / PLAN["batches"][nnn]["output"]
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print("wrote", out.relative_to(ROOT), len(doc["questions"]), "questions", dict(sorted(
            Counter(x["correct_answer"] for x in doc["questions"]).items())))
