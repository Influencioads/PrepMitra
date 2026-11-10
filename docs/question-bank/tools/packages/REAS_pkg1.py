"""Builds the Reasoning Ability topic package 1 (Linear Seating, Circular Seating, Floor-Based Puzzles, Box-Based
Puzzles) for batches 7-10: batches/parts/frag/BATCH_00{7,8,9}_REAS_pkg1.json and BATCH_010_REAS_pkg1.json.

Method (same as tools/batch_005/reasoning.py, whose solve/unique/place/q helpers are reused):
- every puzzle is written once as (text, variables, test) triples; the text goes into the stimulus (or into the
  question for a standalone puzzle) and the test into an exhaustive backtracking search over every assignment;
  the search must return exactly one arrangement (for circles, one person's seat is fixed to remove rotations);
- every person and every attribute value is a variable whose value is a position, so attribute clues are simple
  equalities and the search stays exhaustive yet fast;
- every answer is read off the unique arrangement in code and asserted; wrong options are checked to be different
  from the answer, and "which is true / false" items assert that exactly one option has the required truth value.
If any assertion fails, nothing is written. --draft prints quota gaps instead of asserting them.

    python tools/packages/REAS_pkg1.py        (run from docs/question-bank)
"""

import itertools
import json
import sys
from collections import Counter
from pathlib import Path

TOOLS = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(TOOLS))
from qbank import default_mappings  # noqa: E402

ROOT = TOOLS.parent
PKG = json.loads((ROOT / "batches" / "plans" / "packages" / "REAS_pkg1.json").read_text(encoding="utf-8"))
TODAY = "2026-11-05"
RA = "Reasoning Ability"
LETTERS = "ABCD"
BRUTE = ("script:brute-force-unique", "ai:author-solve")
HAND = ("script:brute-force-unique", "ai:author-solve", "ai:independent-check")
LIN, CIR, FLR, BOX = ("Linear Seating Arrangement", "Circular Seating Arrangement", "Floor-Based Puzzles",
                      "Box-Based Puzzles")
SGL, DBL, UNK = "Single row, facing north/south", "Double row", "Unknown number of persons"
CEN, INOUT, SQR = "Facing centre", "Facing inside and outside", "Square and rectangular tables"
FF, FA = "Floor and flat", "Floor with attribute"
STK, BWC = "Stacked boxes", "Boxes with weights or colours"

BATCH = {}  # "007" -> {"questions": [...], "stimuli": [...], "keys": Counter(), "first_q": int, "first_s": int}
CUR = None


def begin(key):
    global CUR
    p = PKG["batches"][key]
    BATCH[key] = {"questions": [], "stimuli": [], "keys": Counter(), "first_q": int(p["question_ids"][0][-6:]),
                  "first_s": int(p["stimulus_id_start"][-6:]), "plan": p}
    CUR = BATCH[key]


# ------------------------------------------------------------------------------------------------ search
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


def unique(variables, domains, conds, distinct_groups=(), extra=()):
    """conds: (text, vars, test) triples; extra: (vars, test) pairs that are implicit in the set-up (not printed)."""
    import time
    t0 = time.time()
    sols = solve(variables, domains, [(vs, fn) for _, vs, fn in conds] + list(extra), distinct_groups)
    if time.time() - t0 > 2:
        print(f"  slow search {time.time() - t0:.1f}s: {conds[0][0][:60]}", file=sys.stderr)
    assert len(sols) == 1, f"{len(sols)} solutions: {sols[:3]}"
    return sols[0]


def needed(variables, domains, conds, distinct_groups=(), extra=()):
    """Asserts that every printed condition is needed: dropping any one of them leaves more than one arrangement."""
    for i in range(len(conds)):
        rest = conds[:i] + conds[i + 1:]
        n = len(solve(variables, domains, [(vs, fn) for _, vs, fn in rest] + list(extra), distinct_groups))
        assert n > 1, f"condition not needed: {conds[i][0]}"


# ------------------------------------------------------------------------------------------------ options
def place(correct, wrongs, natural=None):
    """Returns (options, key). natural=None: put the correct option on the least-used key so far in this batch (keeps
    A-D balanced); natural=callable: sort all four options by it and let the key fall where it falls."""
    wrongs = list(wrongs)
    assert len(wrongs) == 3 and correct not in wrongs and len(set(wrongs)) == 3, (correct, wrongs)
    if natural:
        opts = sorted([correct] + wrongs, key=natural)
    else:
        n = len(CUR["questions"])
        k = min(LETTERS, key=lambda L: (CUR["keys"][L], (LETTERS.index(L) - n) % 4))
        opts = wrongs[:]
        opts.insert(LETTERS.index(k), correct)
    return opts, LETTERS[opts.index(correct)]


WORDS = ["None", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Eleven", "Twelve"]


def nw(n):
    return WORDS[n]


by_num = lambda t: WORDS.index(t) if t in WORDS else float(t.split()[0])


def q(topic, subtopic, difficulty, text, options, answer, concept, explanation, steps, shortcut=None,
      why_others_wrong=None, seconds=60, stimulus=None, verified_by=BRUTE):
    assert answer in LETTERS and len(options) == 4 and len(set(options)) == 4, (text, options)
    qs = CUR["questions"]
    out = {
        "question_id": f"BANK_REAS_{CUR['first_q'] + len(qs):06d}",
        "exam_mappings": default_mappings(RA, difficulty),
        "subject": RA, "topic": topic, "subtopic": subtopic, "difficulty": difficulty,
        "question_type": "MCQ", "language": "en",
    }
    if stimulus:
        pos = sum(1 for x in qs if x.get("stimulus_id") == stimulus) + 1
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
    qs.append(out)
    CUR["keys"][answer] += 1
    return out


def table(header, rows):
    return "| " + " | ".join(header) + " |\n|" + "---|" * len(header) + "\n" + "\n".join(
        "| " + " | ".join(str(c) for c in r) + " |" for r in rows)


def bullets(conds):
    return "\n".join(f"- {t}" for t, _, _ in conds)


def one_true(statements):
    """statements: list of (text, bool). Exactly one must be true; returns (true_text, [false_texts])."""
    good = [t for t, ok in statements if ok]
    assert len(good) == 1 and len(statements) == 4, statements
    return good[0], [t for t, ok in statements if not ok]


def one_false(statements):
    bad = [t for t, ok in statements if not ok]
    assert len(bad) == 1 and len(statements) == 4, statements
    return bad[0], [t for t, ok in statements if ok]


def odd_one(groups):
    """groups: list of (text, fits_rule). Exactly one group breaks the stated rule; returns (odd, others)."""
    return one_false(groups)


# ------------------------------------------------------------------------------------------------ set context
class Ctx:
    topic = sub = diff = sid = arr = None


C = Ctx()


def puzzle(topic, sub, diff, title, intro, conds, solution, arr, kind="puzzle"):
    """Starts a question set: stores the stimulus and the context the following ask() calls use."""
    sid = f"STIM_REAS_{CUR['first_s'] + len(CUR['stimuli']):06d}"
    body = intro + "\n\n" + bullets(conds)
    CUR["stimuli"].append({"stimulus_id": sid, "type": kind, "title": title, "content": body, "solution": solution})
    C.topic, C.sub, C.diff, C.sid, C.arr = topic, sub, diff, sid, arr
    return sid


def ask(text, correct, wrongs, concept, explanation, steps=(), why=None, natural=None, sec=45, shortcut=None):
    """One question of the current set; the final arrangement is always the first step."""
    opts, key = place(correct, wrongs, natural)
    return q(C.topic, C.sub, C.diff, text, opts, key, concept, explanation, [C.arr, *steps], shortcut=shortcut,
             why_others_wrong=why, seconds=sec, stimulus=C.sid)


def alone(topic, sub, diff, intro, conds, question, correct, wrongs, concept, explanation, steps, why=None,
          natural=None, sec=75, shortcut=None):
    """A standalone puzzle: the conditions are printed in the question itself."""
    opts, key = place(correct, wrongs, natural)
    text = intro + "\n" + bullets(conds) + "\n\n" + question
    return q(topic, sub, diff, text, opts, key, concept, explanation, steps, shortcut=shortcut,
             why_others_wrong=why, seconds=sec)


def inv(sol, names):
    """position -> name for the given names."""
    return {sol[n]: n for n in names}


def pick(pool, avoid, prefer=(), k=3):
    """k distinct wrong options: the preferred ones first, then the rest of the pool in order."""
    out = []
    for x in list(prefer) + list(pool):
        if x not in avoid and x not in out:
            out.append(x)
    assert len(out) >= k, (pool, avoid)
    return out[:k]


def nums(ans, cands):
    """Numeric word options: the answer plus three other counts, sorted naturally."""
    return nw(ans), [nw(c) for c in cands if c != ans][:3]


ORD = lambda k: f"{k}{'th' if 10 <= k % 100 <= 20 else {1: 'st', 2: 'nd', 3: 'rd'}.get(k % 10, 'th')}"


def target_key():
    n = len(CUR["questions"])
    return LETTERS.index(min(LETTERS, key=lambda L: (CUR["keys"][L], (LETTERS.index(L) - n) % 4)))


def bal(ans, fmt=nw, step=1, lo=0, hi=99):
    """Four evenly spaced numeric options containing ans, shifted so that (in natural order) the answer lands on the
    least-used key; returns (correct_text, wrong_texts) to pass with natural=key_of(fmt)."""
    k = target_key()
    start = ans - k * step
    start = max(lo, min(start, hi - 3 * step))
    vals = [start + i * step for i in range(4)]
    assert ans in vals
    return fmt(ans), [fmt(v) for v in vals if v != ans]


ordn = lambda t: int(t[:-2])


def link(items, attrs, values):
    """Channels a per-item value variable (attrs[i] holds the value of items[i], whose variable is a position) to
    per-value position variables '@<value>' (the position of the item holding that value). Returns (vars, extra)."""
    kv = [f"@{v}" for v in values]
    extra = [((it, a, k), lambda p, w, q, v=v: (p == q) == (w == v))
             for it, a in zip(items, attrs) for v, k in zip(values, kv)]
    return kv, extra


# ################################################################################################ BATCH 007
begin("007")

# ---- 7L1 Basic set (6): seven persons facing SOUTH, each from a different city. Seats 1..7 from the west end.
#      Facing south: right = west (seat - k), left = east (seat + k).
P = ["Abhiraj", "Charvi", "Hriday", "Kesha", "Navya", "Rishit", "Tanmay"]
CT = ["Agra", "Bhopal", "Indore", "Kochi", "Madurai", "Patna", "Surat"]
V = P + CT
conds = [
    ("Abhiraj sits exactly in the middle of the row.", ("Abhiraj",), lambda a: a == 4),
    ("Charvi sits second to the left of Abhiraj.", ("Charvi", "Abhiraj"), lambda c, a: c == a + 2),
    ("The person from Bhopal sits immediately to the left of Charvi.", ("Bhopal", "Charvi"), lambda b, c: b == c + 1),
    ("Navya sits immediately to the right of Abhiraj.", ("Navya", "Abhiraj"), lambda n, a: n == a - 1),
    ("Kesha sits at one of the extreme ends of the row, but she is not from Bhopal.", ("Kesha", "Bhopal"),
     lambda k, b: k in (1, 7) and k != b),
    ("Tanmay sits immediately to the left of Abhiraj.", ("Tanmay", "Abhiraj"), lambda t, a: t == a + 1),
    ("Rishit is not from Bhopal.", ("Rishit", "Bhopal"), lambda r, b: r != b),
    ("The person from Surat sits at the extreme right end of the row.", ("Surat",), lambda s: s == 1),
    ("Navya is from Kochi, and the person from Patna sits immediately to the left of Navya.",
     ("Navya", "Kochi", "Patna"), lambda n, k, p: n == k and p == n + 1),
    ("Only one person sits between the persons from Agra and Kochi.", ("Agra", "Kochi"),
     lambda a, k: abs(a - k) == 2),
    ("Charvi is not from Indore.", ("Charvi", "Indore"), lambda c, i: c != i),
]
S = unique(V, {v: range(1, 8) for v in V}, conds, [P, CT])
at, city = inv(S, P), {S[c]: c for c in CT}
cof = {p: city[S[p]] for p in P}
assert [(at[i], city[i]) for i in range(1, 8)] == [
    ("Kesha", "Surat"), ("Rishit", "Indore"), ("Navya", "Kochi"), ("Abhiraj", "Patna"), ("Tanmay", "Agra"),
    ("Charvi", "Madurai"), ("Hriday", "Bhopal")]
ARR = "West to east: " + ", ".join(f"{at[i]} ({city[i]})" for i in range(1, 8)) + "; all face south"
puzzle(LIN, SGL, "Basic", "Seven persons facing south, with home cities",
       "Seven persons Abhiraj, Charvi, Hriday, Kesha, Navya, Rishit and Tanmay sit in a straight row, all facing "
       "south. Each of them is from a different city among Agra, Bhopal, Indore, Kochi, Madurai, Patna and Surat. "
       "(For a person facing south, the right is towards the west and the left is towards the east.)", conds,
       "Number the seats 1 to 7 from the west end. Facing south, 'to the right' means a lower seat number and 'to the "
       "left' a higher one.\n"
       "Step 1: Abhiraj = 4. Charvi is second to his left: 6. Navya is immediately to his right: 3, and Tanmay "
       "immediately to his left: 5.\n"
       "Step 2: Bhopal is immediately to Charvi's left: seat 7. Kesha is at an end but not from Bhopal, so Kesha = 1.\n"
       "Step 3: Seats 2 and 7 remain for Hriday and Rishit. Rishit is not from Bhopal (seat 7), so Rishit = 2 and "
       "Hriday = 7 (Bhopal).\n"
       "Step 4: The extreme right end is the west end, seat 1: Kesha is from Surat. Navya (3) is from Kochi, and Patna "
       "is immediately to her left, seat 4: Abhiraj.\n"
       "Step 5: Agra is two seats from Kochi (3): seat 1 or 5; seat 1 is Surat, so Agra = 5 (Tanmay). Indore and "
       "Madurai remain for Rishit and Charvi; Charvi is not from Indore, so Charvi is from Madurai and Rishit from "
       "Indore.\n\n" + table(["Seat (from west)", "Person", "City"], [(i, at[i], city[i]) for i in range(1, 8)]), ARR)
ans = at[S["Agra"]]
assert ans == "Tanmay"
ask("Who is from Agra?", ans, ["Rishit", "Charvi", "Abhiraj"], "Placing an attribute with a 'between' clue",
    "Agra must be two seats away from Kochi (seat 3), i.e. seat 1 or 5. Seat 1 is Surat, so Agra is seat 5: Tanmay.",
    ["Kochi = seat 3 ⇒ Agra = seat 1 or 5", "Seat 1 = Surat ⇒ Agra = seat 5 = Tanmay"],
    why="Rishit is from Indore, Charvi from Madurai and Abhiraj from Patna.", sec=40)
ans = at[S["Charvi"] - 3]
assert ans == "Navya"
ask("Who sits third to the right of Charvi?", ans, ["Kesha", "Rishit", "Hriday"], "Facing south: the right is west",
    "Charvi sits at seat 6 and faces south, so her right is towards the west: seats 5, 4, 3. Third to her right is "
    "seat 3, Navya.", ["Charvi = seat 6, facing south ⇒ right = west", "6 − 3 = seat 3 ⇒ Navya"],
    why="Rishit is fourth and Kesha fifth to her right; Hriday is immediately to her left.", sec=40)
n_ = abs(S["Kesha"] - S["Madurai"]) - 1
assert n_ == 4
c_, w_ = bal(n_)
ask("How many persons sit between Kesha and the person from Madurai?", c_, w_,
    "Counting the seats strictly between two persons",
    "Kesha is at seat 1 and the person from Madurai (Charvi) at seat 6, so seats 2 to 5 lie between them: four "
    "persons.", ["Kesha = seat 1; Madurai = Charvi = seat 6", "Between: seats 2, 3, 4, 5 ⇒ four"], natural=by_num,
    sec=40)
ans = cof["Rishit"]
assert ans == "Indore"
ask("Which city is Rishit from?", ans, ["Madurai", "Agra", "Surat"], "The last two attributes are settled by a "
    "negative clue", "After Surat, Kochi, Patna, Bhopal and Agra are placed, Indore and Madurai remain for Rishit and "
    "Charvi. Charvi is not from Indore, so Rishit is.", ["Left: Indore, Madurai for Rishit, Charvi",
                                                          "Charvi is not from Indore ⇒ Rishit = Indore"],
    why="Madurai is Charvi's city, Agra Tanmay's and Surat Kesha's.", sec=40)
ans = at[7]
assert ans == "Hriday"
ask("Who sits at the extreme left end of the row?", ans, ["Kesha", "Charvi", "Rishit"],
    "Facing south, the left end of the row is its east end",
    "All persons face south, so their left is towards the east. The extreme left end is seat 7: Hriday.",
    ["Facing south ⇒ left end = east end = seat 7", "Seat 7 = Hriday"],
    why="Kesha sits at the other (right, west) end; Charvi and Rishit are not at an end.", sec=35)
t, f = one_true([("Tanmay sits immediately to the right of Charvi", S["Tanmay"] == S["Charvi"] - 1),
                 ("Hriday sits second to the left of Navya", S["Hriday"] == S["Navya"] + 2),
                 ("The person from Patna sits at an extreme end", S["Patna"] in (1, 7)),
                 ("Only two persons sit between Rishit and Abhiraj", abs(S["Rishit"] - S["Abhiraj"]) == 3)])
assert t == "Tanmay sits immediately to the right of Charvi"
ask("Which of the following statements is true?", t, f, "Checking each statement against the arrangement",
    "Charvi sits at seat 6 facing south, so her right is towards the west; seat 5 (Tanmay) is immediately to her "
    "right. The other statements fail.",
    ["Charvi = 6, facing south ⇒ immediately right = seat 5 = Tanmay ✓",
     "Navya = 3 ⇒ second to her left (east) = seat 5 = Tanmay, not Hriday ✗",
     "Patna = Abhiraj = seat 4, the middle ✗", "Rishit 2, Abhiraj 4 ⇒ only one person between ✗"],
    why="Second to Navya's left is Tanmay, Patna is in the middle seat, and only one person (Navya) sits between "
        "Rishit and Abhiraj.", sec=50)

# ---- 7L2 Intermediate set (4): eight persons, mixed facing, each learning a different language.
#      Seats 1..8 from the west. Facing north: right = east (+k); facing south: right = west (−k).
P = ["Advait", "Bhairavi", "Dhruv", "Gargee", "Jivesh", "Kalyani", "Paras", "Sumedha"]
LG = ["Bengali", "French", "German", "Japanese", "Korean", "Russian", "Spanish", "Tamil"]
F = ["f" + p for p in P]
RT = lambda s, f, k: s + k if f == "N" else s - k
V = ["Sumedha", "fSumedha", "Dhruv", "Kalyani", "fKalyani", "Paras", "fParas", "Bhairavi", "fBhairavi", "Jivesh",
     "fJivesh", "fDhruv", "Advait", "Gargee", "fGargee", "fAdvait"] + LG
conds = [
    ("Sumedha learns German. She sits fourth from the west end of the row and faces north.",
     ("Sumedha", "fSumedha", "German"), lambda s, f, g: s == 4 and f == "N" and g == s),
    ("Dhruv sits third to the right of Sumedha.", ("Dhruv", "Sumedha", "fSumedha"),
     lambda d, s, f: d == RT(s, f, 3)),
    ("Kalyani sits at one of the extreme ends of the row, and Dhruv sits immediately to her right.",
     ("Kalyani", "fKalyani", "Dhruv"), lambda k, f, d: k in (1, 8) and d == RT(k, f, 1)),
    ("Paras sits at the other extreme end and faces the same direction as Kalyani.",
     ("Kalyani", "fKalyani", "Paras", "fParas"), lambda k, fk, p, fp: p == 9 - k and fp == fk),
    ("Bhairavi sits second to the right of Kalyani.", ("Bhairavi", "Kalyani", "fKalyani"),
     lambda b, k, f: b == RT(k, f, 2)),
    ("Both persons sitting immediately next to Bhairavi face north, but Bhairavi does not.",
     ("Bhairavi", "fBhairavi", "Jivesh", "fJivesh", "Dhruv", "fDhruv"),
     lambda b, fb, j, fj, d, fd: fb == "S" and all(fx == "N" for x, fx in ((j, fj), (d, fd)) if abs(x - b) == 1)
     and sum(abs(x - b) == 1 for x in (j, d)) == 2),
    ("Jivesh sits immediately to the right of Sumedha.", ("Jivesh", "Sumedha", "fSumedha"),
     lambda j, s, f: j == RT(s, f, 1)),
    ("Advait sits second to the left of Jivesh.", ("Advait", "Jivesh", "fJivesh"), lambda a, j, f: a == RT(j, f, -2)),
    ("Gargee faces the same direction as Sumedha.", ("fGargee", "fSumedha"), lambda g, s: g == s),
    ("Exactly four persons face north.", tuple(F), lambda *fs: fs.count("N") == 4),
    ("Bhairavi learns Bengali. The person who learns Russian sits at an extreme end, and only one person sits "
     "between the Russian learner and Bhairavi.", ("Bhairavi", "Bengali", "Russian"),
     lambda b, be, r: be == b and r in (1, 8) and abs(r - b) == 2),
    ("The Spanish learner sits immediately to the right of the German learner.",
     ("Spanish", "German", "Sumedha", "fSumedha"), lambda sp, g, s, f: sp == RT(g, f, 1)),
    ("Dhruv learns Japanese, and the French learner sits at an extreme end of the row.",
     ("Dhruv", "Japanese", "French"), lambda d, j, fr: d == j and fr in (1, 8)),
    ("The Korean learner faces south.", ("Korean", *P, *F),
     lambda ko, *pf: all(f_ == "S" for x, f_ in zip(pf[:8], pf[8:]) if x == ko)),
]
dom = {p: range(1, 9) for p in P} | {f: "NS" for f in F} | {g: range(1, 9) for g in LG}
S = unique(V, dom, conds, [P, LG])
at, lang = inv(S, P), inv(S, LG)
fc = {p: S["f" + p] for p in P}
FN = {"N": "north", "S": "south"}
assert [(at[i], fc[at[i]], lang[i]) for i in range(1, 9)] == [
    ("Paras", "S", "French"), ("Gargee", "N", "Tamil"), ("Advait", "S", "Korean"), ("Sumedha", "N", "German"),
    ("Jivesh", "N", "Spanish"), ("Bhairavi", "S", "Bengali"), ("Dhruv", "N", "Japanese"),
    ("Kalyani", "S", "Russian")]
ARR = "West to east: " + ", ".join(f"{at[i]} ({FN[fc[at[i]]]}, {lang[i]})" for i in range(1, 9))
puzzle(LIN, SGL, "Intermediate", "Eight persons facing north or south, with languages",
       "Eight persons Advait, Bhairavi, Dhruv, Gargee, Jivesh, Kalyani, Paras and Sumedha sit in a straight row. Some "
       "of them face north and the others face south. Each of them is learning a different language among Bengali, "
       "French, German, Japanese, Korean, Russian, Spanish and Tamil. (For a person facing north, the right is "
       "towards the east; for a person facing south, the right is towards the west.)", conds,
       "Number the seats 1 to 8 from the west end.\n"
       "Step 1: Sumedha = 4, facing north, German. Dhruv is third to her right (east): 7.\n"
       "Step 2: Dhruv is immediately to the right of Kalyani, who is at an end. Kalyani = 8 facing south (her right is "
       "west, seat 7) works; Kalyani = 1 cannot have seat 7 next to her. Paras = 1, facing south.\n"
       "Step 3: Bhairavi is second to Kalyani's right: 8 − 2 = 6. Her neighbours (5 and 7) face north and she faces "
       "south, so Dhruv faces north.\n"
       "Step 4: Jivesh is immediately to Sumedha's right: 5 (so he faces north). Jivesh faces north, so his left is "
       "west: Advait = 5 − 2 = 3, and Gargee takes seat 2.\n"
       "Step 5: Gargee faces north like Sumedha. North-facing so far: Sumedha, Dhruv, Jivesh, Gargee = four, so "
       "Advait faces south.\n"
       "Step 6: Russian is at an end two seats from Bhairavi (6): seat 8, Kalyani. Spanish is immediately right of "
       "German (seat 4, facing north): seat 5, Jivesh. Dhruv learns Japanese; French is at an end: seat 1, Paras.\n"
       "Step 7: Korean and Tamil remain for Gargee (north) and Advait (south). The Korean learner faces south: Advait "
       "learns Korean and Gargee Tamil.\n\n"
       + table(["Seat (from west)", "Person", "Faces", "Language"],
               [(i, at[i], FN[fc[at[i]]], lang[i]) for i in range(1, 9)]), ARR)
ans = at[RT(S["Bhairavi"], fc["Bhairavi"], -2)]
assert ans == "Kalyani"
ask("Who sits second to the left of Bhairavi?", ans, ["Jivesh", "Sumedha", "Dhruv"],
    "A south-facing person's left is towards the east",
    "Bhairavi sits at seat 6 and faces south, so her left is towards the east: seat 7 (Dhruv), then seat 8 (Kalyani).",
    ["Bhairavi = seat 6, facing south ⇒ left = east", "6 + 2 = seat 8 ⇒ Kalyani"],
    why="Sumedha is second to her right (west); Dhruv is immediately to her left; Jivesh is immediately to her right.",
    sec=50)
ans = lang[RT(S["Advait"], fc["Advait"], 1)]
assert ans == "Tamil"
ask("Which language does the person sitting immediately to the right of Advait learn?", ans,
    ["German", "French", "Korean"], "Find the facing direction first, then the neighbour",
    "Advait sits at seat 3 and faces south, so his right is towards the west: seat 2, Gargee, who learns Tamil.",
    ["Advait = seat 3, facing south ⇒ right = west", "Seat 2 = Gargee ⇒ Tamil"],
    why="German is the language of the person on Advait's left (Sumedha); French is Paras's (two seats away); Korean "
        "is Advait's own language.", sec=50)
n_ = abs(S["French"] - S["Spanish"]) - 1
assert n_ == 3
c_, w_ = bal(n_)
ask("How many persons sit between the French learner and the Spanish learner?", c_, w_,
    "Count the seats strictly between two persons",
    "The French learner (Paras) is at seat 1 and the Spanish learner (Jivesh) at seat 5, so Gargee, Advait and "
    "Sumedha sit between them.", ["French = seat 1, Spanish = seat 5", "Between: seats 2, 3, 4 ⇒ three"],
    natural=by_num, sec=45)
t, f = one_true([("Dhruv and Gargee face the same direction", fc["Dhruv"] == fc["Gargee"]),
                 ("Advait sits immediately to the right of Sumedha", S["Advait"] == RT(S["Sumedha"], "N", 1)),
                 ("The Japanese learner sits second to the right of the Bengali learner",
                  S["Japanese"] == RT(S["Bengali"], fc[at[S["Bengali"]]], 2)),
                 ("Exactly three persons face south", list(fc.values()).count("S") == 3)])
assert t == "Dhruv and Gargee face the same direction"
ask("Which of the following statements is true?", t, f, "Checking each statement against the arrangement",
    "Dhruv and Gargee both face north, so the first statement is true; each of the others fails.",
    ["Dhruv north, Gargee north ⇒ same direction ✓",
     "Sumedha (seat 4) faces north ⇒ immediately to her right (east) is seat 5 = Jivesh, not Advait ✗",
     "Bengali = Bhairavi (seat 6, facing south) ⇒ second to her right (west) is seat 4 = Sumedha (German) ✗",
     "South-facing: Paras, Advait, Bhairavi, Kalyani = four, not three ✗"],
    why="Jivesh, not Advait, is immediately right of Sumedha; second to Bhairavi's right is the German learner; four "
        "persons face south.", sec=55)


# ---- 7L3 Intermediate set (4): a south-facing row of unknown length. Seats are counted from the WEST end, which is
#      the right end for persons facing south (right = west = −k, left = east = +k); n = number of persons.
V = ["Ranjana", "Shailesh", "Uditi", "Varenya", "Ojasvi", "n", "Pratyush"]
conds = [
    ("Ranjana sits fifth from the right end of the row.", ("Ranjana",), lambda r: r == 5),
    ("Shailesh sits sixth to the left of Ranjana.", ("Shailesh", "Ranjana"), lambda s, r: s == r + 6),
    ("Only three persons sit between Shailesh and Uditi, and Uditi sits to the left of Shailesh.",
     ("Uditi", "Shailesh"), lambda u, s: u == s + 4),
    ("Varenya sits exactly midway between Ranjana and Uditi.", ("Varenya", "Ranjana", "Uditi"),
     lambda v, r, u: 2 * v == r + u),
    ("Ojasvi sits second to the right of Varenya.", ("Ojasvi", "Varenya"), lambda o, v: o == v - 2),
    ("Pratyush sits at the extreme left end of the row, and as many persons sit between Uditi and Pratyush as sit "
     "between Ranjana and Ojasvi.", ("Pratyush", "n", "Uditi", "Ranjana", "Ojasvi"),
     lambda p, n, u, r, o: p == n and p - u - 1 == abs(o - r) - 1),
]
NAMED = [v for v in V if v != "n"]
S = unique(V, {v: range(1, 41) for v in V}, conds, [NAMED], extra=[(("n", *NAMED), lambda n, *xs: max(xs) <= n)])
n_ = S["n"]
assert (n_, S["Shailesh"], S["Uditi"], S["Varenya"], S["Ojasvi"]) == (18, 11, 15, 10, 8)
ARR = (f"Counting from the right (west) end: Ranjana 5th, Ojasvi 8th, Varenya 10th, Shailesh 11th, Uditi 15th, "
       f"Pratyush {n_}th (the left end); {n_} persons in all")
puzzle(LIN, UNK, "Intermediate", "A south-facing row of unknown length",
       "Some persons sit in a straight row, all facing south. (For a person facing south, the right is towards the "
       "west and the left is towards the east.) The number of persons in the row is not given. Ojasvi, Pratyush, "
       "Ranjana, Shailesh, Uditi and Varenya are among them.", conds,
       "Count positions from the right end of the row (the west end, since everyone faces south). Moving 'to the left' "
       "of someone increases this count.\n"
       "Step 1: Ranjana = 5th from the right. Shailesh is sixth to her left: 5 + 6 = 11th.\n"
       "Step 2: Three persons sit between Shailesh and Uditi, Uditi on his left: 11 + 4 = 15th.\n"
       "Step 3: Varenya is midway between 5th and 15th: 10th. Ojasvi is second to Varenya's right: 10 − 2 = 8th.\n"
       "Step 4: Between Ranjana (5th) and Ojasvi (8th) sit two persons, so two persons sit between Uditi (15th) and "
       "Pratyush, who is at the left end: Pratyush = 15 + 3 = 18th from the right. The row has 18 persons.\n\n"
       + table(["Person", "From the right end", "From the left end"],
               [(p, ORD(S[p]), ORD(n_ - S[p] + 1)) for p in sorted(NAMED, key=lambda x: S[x])]), ARR)
ask("How many persons sit in the row?", str(n_), ["17", "19", "20"], "Turning 'between' counts into positions",
    "Uditi is 15th from the right. Two persons sit between Uditi and Pratyush (as between Ranjana, 5th, and Ojasvi, "
    "8th), so Pratyush, at the left end, is 18th from the right: 18 persons.",
    ["Ranjana 5th ⇒ Shailesh 11th ⇒ Uditi 15th", "Varenya 10th ⇒ Ojasvi 8th ⇒ two persons between Ranjana and Ojasvi",
     "Pratyush = 15 + 2 + 1 = 18th from the right = the left end ⇒ 18 persons"],
    why="17 leaves out Pratyush himself; 19 and 20 add seats that no clue allows.", natural=int, sec=75)
ans = n_ - S["Shailesh"] + 1
assert ans == 8
ask("What is Shailesh's position from the left end of the row?", ORD(ans), ["7th", "9th", "11th"],
    "Position from one end = total − position from the other end + 1",
    "Shailesh is 11th from the right in a row of 18, so he is 18 − 11 + 1 = 8th from the left end.",
    ["Shailesh = 11th from the right", "From the left: 18 − 11 + 1 = 8th"],
    why="11th is his position from the right end; 7th forgets the +1 and 9th adds one too many.",
    natural=lambda t: int(t[:-2]), sec=50)
n2 = S["Uditi"] - S["Ojasvi"] - 1
assert n2 == 6
c_, w_ = bal(n2)
ask("How many persons sit between Ojasvi and Uditi?", c_, w_, "Persons between = difference of positions − 1",
    "Ojasvi is 8th and Uditi 15th from the right, so 15 − 8 − 1 = 6 persons sit between them.",
    ["Ojasvi 8th, Uditi 15th (both from the right)", "15 − 8 − 1 = 6"], natural=by_num, sec=50)
ans = S["Pratyush"]
ask("If Ojasvi and Pratyush interchange their seats, what will be Ojasvi's position from the right end?",
    ORD(ans), ["8th", "17th", "11th"], "After an interchange each person takes the other's position",
    "Pratyush sits at the left end, 18th from the right. After the interchange Ojasvi takes his seat: 18th from the "
    "right end.", ["Pratyush = 18th from the right (the left end)", "Ojasvi moves there ⇒ 18th"],
    why="8th is Ojasvi's original position; 17th and 11th are not Pratyush's seat.", natural=lambda t: int(t[:-2]),
    sec=45)

# ---- 7LA1 Advanced (standalone): eight players of four clubs, the gap between club-mates growing by one per club.
#      Seats 1..8 from the west, all facing north (right = east).
P = ["Bhavin", "Chandni", "Dipali", "Faiz", "Hiral", "Imran", "Juhi", "Kunal"]
CLUB = {"Chess": 1, "Hockey": 2, "Kabaddi": 3, "Tennis": 4}
CV = [c + i for c in CLUB for i in "12"]
same = lambda a, b, xs: any({a, b} == {xs[i], xs[i + 1]} for i in range(0, 8, 2))
conds = [
    ("Exactly one person sits between the two Chess players, exactly two persons sit between the two Hockey players, "
     "exactly three between the two Kabaddi players and exactly four between the two Tennis players.", tuple(CV),
     lambda *xs: all(xs[2 * i] < xs[2 * i + 1] and xs[2 * i + 1] - xs[2 * i] == g + 1
                     for i, g in enumerate(CLUB.values()))),
    ("A Tennis player sits at the extreme left end of the row.", ("Tennis1",), lambda t: t == 1),
    ("Chandni sits at the extreme right end of the row.", ("Chandni",), lambda c: c == 8),
    ("Faiz and Kunal belong to the same club.", ("Faiz", "Kunal", *CV), lambda f, k, *xs: same(f, k, xs)),
    ("Imran sits second to the right of Bhavin, and Hiral sits immediately to the left of Imran.",
     ("Imran", "Bhavin", "Hiral"), lambda i, b, h: i == b + 2 and h == i - 1),
    ("Dipali and Imran belong to the same club.", ("Dipali", "Imran", *CV), lambda d, i, *xs: same(d, i, xs)),
    ("Juhi sits at one of the extreme ends of the row, and Faiz sits somewhere to the left of Kunal.",
     ("Juhi", "Faiz", "Kunal"), lambda j, f, k: j in (1, 8) and f < k),
]
S = unique(CV + P, {v: range(1, 9) for v in CV + P}, conds, [CV, P])
at = inv(S, P)
club = {S[v]: v[:-1] for v in CV}
assert [(at[i], club[i]) for i in range(1, 9)] == [
    ("Juhi", "Tennis"), ("Faiz", "Chess"), ("Dipali", "Kabaddi"), ("Kunal", "Chess"), ("Bhavin", "Hockey"),
    ("Hiral", "Tennis"), ("Imran", "Kabaddi"), ("Chandni", "Hockey")]
mate = next(p for p in P if p != "Hiral" and club[S[p]] == club[S["Hiral"]])
assert mate == "Juhi"
alone(LIN, SGL, "Advanced",
      "Eight persons Bhavin, Chandni, Dipali, Faiz, Hiral, Imran, Juhi and Kunal sit in a straight row, all facing "
      "north. Two of them belong to each of four clubs: Chess, Hockey, Kabaddi and Tennis.", conds,
      "Who is the other member of Hiral's club?", mate, ["Chandni", "Bhavin", "Faiz"],
      "Fix the club pattern first, then place the names",
      "With a Tennis player at seat 1 and four persons between the Tennis pair, Tennis = seats 1 and 6. The only way to "
      "fit the other gaps in the free seats is Kabaddi 3 & 7, Chess 2 & 4 and Hockey 5 & 8. Placing the names puts "
      "Hiral at seat 6 (Tennis), so her club-mate is Juhi at seat 1.",
      ["Tennis: seats 1 and 6 (four persons between)",
       "Kabaddi needs a gap of 4 seats among 2, 3, 4, 5, 7, 8: only 3 & 7 (2 & 6 and 4 & 8 clash with Tennis or leave "
       "no room for Hockey) ⇒ free 2, 4, 5, 8",
       "Chess (gap 2) = 2 & 4; Hockey (gap 3) = 5 & 8",
       "Chandni = 8. Bhavin, Hiral, Imran sit in three consecutive seats from west to east",
       "Juhi is at an end, so Juhi = 1. Imran's club-mate is Dipali: trio 2-3-4 needs Dipali at 2 ✗, trio 3-4-5 needs "
       "her at 8 ✗, trio 4-5-6 needs her at 1 ✗ (Juhi), trio 5-6-7 gives Imran = 7 (Kabaddi), Dipali = 3 ✓",
       "Faiz and Kunal take 2 and 4 (both Chess), Faiz to the left: Faiz = 2, Kunal = 4",
       "Hiral = seat 6 (Tennis) ⇒ the other Tennis player is Juhi (seat 1)"],
      why="Chandni and Bhavin play Hockey; Faiz plays Chess.", sec=150)

# ---- 7LA2 Advanced (standalone): facing fixed by the half of the row — seats 1-4 face north, seats 5-8 face south.
P = ["Ishika", "Jairaj", "Kriti", "Nakul", "Pihu", "Ritvik", "Sanvi", "Yashas"]
fac = lambda s: "N" if s <= 4 else "S"
R2 = lambda s, k: s + k if fac(s) == "N" else s - k
conds = [
    ("Ritvik sits at one of the extreme ends of the row, and Kriti sits immediately to his right.",
     ("Ritvik", "Kriti"), lambda r, k: r in (1, 8) and k == R2(r, 1)),
    ("Ishika sits immediately to the right of Yashas, and Jairaj sits third to the right of Yashas.",
     ("Ishika", "Jairaj", "Yashas"), lambda i, j, y: i == R2(y, 1) and j == R2(y, 3)),
    ("Sanvi sits immediately to the left of Jairaj.", ("Sanvi", "Jairaj"), lambda s, j: s == R2(j, -1)),
    ("Yashas does not sit at an extreme end of the row, but Nakul does.", ("Yashas", "Nakul"),
     lambda y, n: y not in (1, 8) and n in (1, 8)),
    ("Pihu faces north, but Yashas faces south.", ("Pihu", "Yashas"), lambda p, y: fac(p) == "N" and fac(y) == "S"),
]
S = unique(P, {p: range(1, 9) for p in P}, conds, [P])
at = inv(S, P)
assert [at[i] for i in range(1, 9)] == ["Nakul", "Sanvi", "Jairaj", "Pihu", "Ishika", "Yashas", "Kriti", "Ritvik"]
lp = at[R2(S["Pihu"], -1)]
n_ = abs(S[lp] - S["Nakul"]) - 1
assert (lp, n_) == ("Jairaj", 1)
c_, w_ = bal(n_)
alone(LIN, SGL, "Advanced",
      "Eight persons Ishika, Jairaj, Kriti, Nakul, Pihu, Ritvik, Sanvi and Yashas sit in a straight row of eight seats, "
      "numbered 1 to 8 from the west end. The persons in seats 1 to 4 face north and those in seats 5 to 8 face south. "
      "(Facing north, the right is towards the east; facing south, the right is towards the west.)",
      conds, "How many persons sit between Nakul and the person who sits immediately to the left of Pihu?", c_, w_,
      "When the facing depends on the seat, check which half each person sits in before moving right or left",
      "Yashas faces south, so he is in seat 5, 6 or 7, and Ishika and Jairaj are one and three seats west of him. "
      "Only Yashas = 6 works, giving (west to east) Nakul, Sanvi, Jairaj, Pihu, Ishika, Yashas, Kriti, Ritvik. Pihu "
      "(seat 4) faces north, so her left is west: seat 3, Jairaj. Between Nakul (1) and Jairaj (3) sits one person.",
      ["Yashas faces south ⇒ seat 5, 6 or 7; Ishika = Yashas − 1, Jairaj = Yashas − 3",
       "Yashas 5 ⇒ Jairaj 2 (north) ⇒ Sanvi 1, leaving only seat 8 for both Ritvik and Nakul ✗",
       "Yashas 7 ⇒ Ishika 6, Jairaj 4 ⇒ Sanvi 3; Ritvik 8 needs Kriti 7 ✗, Ritvik 1 ⇒ Kriti 2, Nakul 8, Pihu 5 faces "
       "south ✗",
       "Yashas 6 ⇒ Ishika 5, Jairaj 3 ⇒ Sanvi 2; Ritvik 1 needs Kriti 2 ✗ ⇒ Ritvik 8, Kriti 7, Nakul 1, Pihu 4 ✓",
       "Pihu (4, north) ⇒ left = west = seat 3 = Jairaj", "Between Nakul (1) and Jairaj (3): Sanvi ⇒ one"],
      why="Any other count comes from taking Pihu's left as east or from a case that breaks the clues.",
      natural=by_num, sec=150)


# ================================================================================================ circular helpers
# Seats 0..n−1 anticlockwise. Facing the centre, the right is anticlockwise (+1); facing outside, it is clockwise (−1).
def CR(s, f, k, n):
    return (s + k) % n if f == "C" else (s - k) % n


FCN = {"C": "facing the centre", "O": "facing outside"}

# ---- 7CB1 Basic (standalone): five persons at the corners of a pentagonal table, facing the centre.
P = ["Aniket", "Bhumika", "Chaitra", "Daman", "Eshwar"]
conds = [
    ("Chaitra sits immediately to the right of Aniket.", ("Chaitra", "Aniket"), lambda c, a: c == CR(a, "C", 1, 5)),
    ("Bhumika sits second to the left of Aniket.", ("Bhumika", "Aniket"), lambda b, a: b == CR(a, "C", -2, 5)),
    ("Daman does not sit next to Chaitra.", ("Daman", "Chaitra"), lambda d, c: (d - c) % 5 not in (1, 4)),
]
S = unique(P, {"Aniket": [0]} | {p: range(5) for p in P[1:]}, conds, [P])
at = inv(S, P)
assert [at[i] for i in range(5)] == ["Aniket", "Chaitra", "Eshwar", "Bhumika", "Daman"]
nb = {at[(S["Eshwar"] - 1) % 5], at[(S["Eshwar"] + 1) % 5]}
assert nb == {"Chaitra", "Bhumika"}
alone(CIR, CEN, "Basic",
      "Five friends Aniket, Bhumika, Chaitra, Daman and Eshwar sit at the five corners of a pentagonal table, one at "
      "each corner, all facing the centre. (Facing the centre, a person's right is the next seat anticlockwise.)",
      conds, "Who are the immediate neighbours of Eshwar?", "Chaitra and Bhumika",
      ["Aniket and Daman", "Chaitra and Daman", "Bhumika and Aniket"], "Fix one person and place the rest around him",
      "Going anticlockwise from Aniket: Chaitra (his immediate right), then two seats remain before Bhumika, who is "
      "second to Aniket's left. Daman cannot sit next to Chaitra, so the order is Aniket, Chaitra, Eshwar, Bhumika, "
      "Daman. Eshwar sits between Chaitra and Bhumika.",
      ["Seats anticlockwise from Aniket: 0 Aniket", "Chaitra = immediate right = seat 1",
       "Bhumika = second to the left (two seats clockwise) = seat 3", "Seats 2 and 4 remain; seat 2 touches Chaitra ⇒ "
       "Daman = 4, Eshwar = 2", "Eshwar's neighbours: Chaitra (1) and Bhumika (3)"],
      why="Aniket's neighbours are Chaitra and Daman; Daman sits between Bhumika and Aniket.", sec=45)

# ---- 7CB2 Basic (standalone): six persons at a hexagonal table, all facing OUTSIDE (right = clockwise = −1).
P = ["Kamakshi", "Manohar", "Neha", "Omprakash", "Prakriti", "Rajat"]
conds = [
    ("Manohar sits exactly opposite Kamakshi.", ("Manohar", "Kamakshi"), lambda m, k: m == (k + 3) % 6),
    ("Neha sits immediately to the right of Kamakshi.", ("Neha", "Kamakshi"), lambda n, k: n == CR(k, "O", 1, 6)),
    ("Rajat sits second to the left of Neha.", ("Rajat", "Neha"), lambda r, n: r == CR(n, "O", -2, 6)),
    ("Prakriti sits immediately to the left of Rajat.", ("Prakriti", "Rajat"), lambda p, r: p == CR(r, "O", -1, 6)),
]
S = unique(P, {"Kamakshi": [0]} | {p: range(6) for p in P[1:]}, conds, [P])
at = inv(S, P)
assert [at[i] for i in range(6)] == ["Kamakshi", "Rajat", "Prakriti", "Manohar", "Omprakash", "Neha"]
ans = at[CR(S["Omprakash"], "O", 2, 6)]
assert ans == "Prakriti"
alone(CIR, CEN, "Basic",
      "Six persons Kamakshi, Manohar, Neha, Omprakash, Prakriti and Rajat sit around a hexagonal table, one at each "
      "side, all facing away from the centre. (Facing outside, a person's right is the next seat clockwise.)", conds,
      "Who sits second to the right of Omprakash?", ans, ["Neha", "Rajat", "Manohar"],
      "Facing outside reverses right and left compared with facing the centre",
      "Number the seats 0 to 5 anticlockwise from Kamakshi. Manohar = 3 (opposite). Neha is to Kamakshi's right, "
      "i.e. clockwise: seat 5. Rajat is second to Neha's left (anticlockwise): seat 1, and Prakriti is immediately to "
      "Rajat's left: seat 2. Omprakash takes seat 4. Two seats to his right (clockwise) is seat 2: Prakriti.",
      ["Kamakshi 0, Manohar 3", "Facing outside: right = clockwise ⇒ Neha = 5",
       "Left = anticlockwise ⇒ Rajat = 5 + 2 = 1, Prakriti = 2", "Omprakash = 4",
       "Second to his right: 4 → 3 → 2 ⇒ Prakriti"],
      why="Neha is second to his left, Rajat third to his right, and Manohar immediately to his right.", sec=50)

# ---- 7CI1 Intermediate (standalone): eight persons, neighbours always face opposite ways.
P = ["Ambika", "Bhushan", "Champa", "Devesh", "Gaurika", "Harbhajan", "Indrajit", "Jyoti"]
fe = lambda s: "C" if s % 2 == 0 else "O"  # Ambika (seat 0) faces the centre, so even seats face the centre
conds = [
    ("Ambika faces the centre, and Harbhajan sits exactly opposite her.", ("Harbhajan",), lambda h: h == 4),
    ("Bhushan sits immediately to the left of Harbhajan.", ("Bhushan", "Harbhajan"),
     lambda b, h: b == CR(h, fe(h), -1, 8)),
    ("Jyoti sits immediately to the right of Bhushan.", ("Jyoti", "Bhushan"), lambda j, b: j == CR(b, fe(b), 1, 8)),
    ("Indrajit faces the centre.", ("Indrajit",), lambda i: fe(i) == "C"),
    ("Devesh is an immediate neighbour of Ambika.", ("Devesh",), lambda d: d in (1, 7)),
    ("Gaurika sits second to the left of Champa.", ("Gaurika", "Champa"), lambda g, c: g == CR(c, fe(c), -2, 8)),
]
S = unique(P, {"Ambika": [0]} | {p: range(8) for p in P[1:]}, conds, [P])
at = inv(S, P)
assert [at[i] for i in range(8)] == ["Ambika", "Devesh", "Jyoti", "Bhushan", "Harbhajan", "Champa", "Indrajit",
                                     "Gaurika"]
ans = at[CR(S["Indrajit"], "C", 3, 8)]
assert ans == "Devesh"
alone(CIR, INOUT, "Intermediate",
      "Eight persons Ambika, Bhushan, Champa, Devesh, Gaurika, Harbhajan, Indrajit and Jyoti sit around a circular "
      "table, equally spaced. Some face the centre and the others face outside, and of any two persons sitting next to "
      "each other, one faces the centre and the other faces outside. (Facing the centre, the right is anticlockwise; "
      "facing outside, it is clockwise.)", conds, "Who sits third to the right of Indrajit?", ans,
      ["Gaurika", "Champa", "Ambika"], "With alternate facing, every second seat faces the same way",
      "Number the seats 0 to 7 anticlockwise from Ambika. Ambika faces the centre, so even seats face the centre and "
      "odd seats face outside. Harbhajan = 4 (centre); his left is clockwise: Bhushan = 3 (outside). Bhushan's right "
      "is clockwise: Jyoti = 2. Indrajit faces the centre: the only even seat left is 6. Devesh, Champa and Gaurika "
      "take 1, 5 and 7; Gaurika is second to the left (anticlockwise) of an outside-facing Champa, which works only "
      "for Champa = 5, Gaurika = 7, leaving Devesh = 1, next to Ambika. Indrajit (6) faces the centre: three seats "
      "anticlockwise is seat 1, Devesh.",
      ["Even seats face the centre, odd seats outside", "Harbhajan 4 ⇒ Bhushan 3 ⇒ Jyoti 2", "Indrajit = 6",
       "Champa 5, Gaurika 7, Devesh 1", "Third to Indrajit's right: 6 → 7 → 0 → 1 ⇒ Devesh"],
      why="Gaurika is immediately to Indrajit's right, Ambika second to his right, and Champa immediately to his left.",
      sec=90)

# ---- 7CI2 Intermediate (standalone): a rectangular table with ten seats — one at each shorter side, four along each
#      longer side — all facing the centre. Seats 0..9 anticlockwise: 0 = one shorter side, 1–4 one longer side,
#      5 = the other shorter side, 6–9 the other longer side; seat s on a longer side faces seat 10 − s.
P = ["Anup", "Bhanu", "Deepika", "Gyan", "Hiten", "Ira", "Kanchan", "Mihir", "Nirmala", "Purab"]
opp10 = lambda s: (s + 5) % 10 if s in (0, 5) else 10 - s
R10 = lambda s, k: (s + k) % 10
conds = [
    ("Ira and Gyan sit at the two shorter sides.", ("Gyan",), lambda g: g == 5),
    ("Mihir sits second to the right of Ira.", ("Mihir", "Ira"), lambda m, i: m == R10(i, 2)),
    ("Purab sits directly opposite Mihir.", ("Purab", "Mihir"), lambda p, m: p == opp10(m)),
    ("Deepika sits fourth to the left of Purab.", ("Deepika", "Purab"), lambda d, p: d == R10(p, -4)),
    ("Kanchan sits immediately between Mihir and Deepika.", ("Kanchan", "Mihir", "Deepika"),
     lambda k, m, d: {R10(k, 1), R10(k, -1)} == {m, d}),
    ("Hiten sits immediately to the left of Ira.", ("Hiten", "Ira"), lambda h, i: h == R10(i, -1)),
    ("Nirmala sits immediately to the right of Gyan.", ("Nirmala", "Gyan"), lambda n, g: n == R10(g, 1)),
    ("Bhanu does not sit next to Ira.", ("Bhanu", "Ira"), lambda b, i: abs(b - i) not in (1, 9)),
]
S = unique(P, {"Ira": [0]} | {p: range(10) for p in P if p != "Ira"}, conds, [P])
at = inv(S, P)
assert [at[i] for i in range(10)] == ["Ira", "Anup", "Mihir", "Kanchan", "Deepika", "Gyan", "Nirmala", "Bhanu",
                                      "Purab", "Hiten"]
ans = at[opp10(S["Anup"])]
assert ans == "Hiten"
alone(CIR, SQR, "Intermediate",
      "Ten persons Anup, Bhanu, Deepika, Gyan, Hiten, Ira, Kanchan, Mihir, Nirmala and Purab sit around a rectangular "
      "table, all facing the centre. One person sits at each of the two shorter sides and four persons sit along each "
      "of the two longer sides, so that each person on a longer side sits directly opposite a person on the other "
      "longer side. (Facing the centre, the right is anticlockwise.)", conds, "Who sits directly opposite Anup?", ans,
      ["Bhanu", "Nirmala", "Purab"], "Number the seats round the table and pair the long-side seats",
      "Start at Ira's shorter side and number the seats 0 to 9 anticlockwise; Gyan is at seat 5. Seats 1–4 form one "
      "longer side and 9–6 the other, so seat s faces seat 10 − s. Mihir = 2, Purab opposite = 8, Deepika four seats "
      "clockwise from Purab = 4, Kanchan between them = 3, Hiten = 9 and Nirmala = 6. Bhanu cannot sit next to Ira, "
      "so Bhanu = 7 and Anup = 1. Seat 1 faces seat 9: Hiten.",
      ["Ira 0, Gyan 5; seat s faces 10 − s", "Mihir 2 ⇒ Purab 8 ⇒ Deepika 4 ⇒ Kanchan 3",
       "Hiten 9 (Ira's left), Nirmala 6 (Gyan's right)", "Seats 1, 7 for Anup, Bhanu; Bhanu not next to Ira ⇒ Anup 1",
       "Opposite seat 1 = seat 9 ⇒ Hiten"],
      why="Bhanu faces Kanchan, Nirmala faces Deepika, and Purab faces Mihir.", sec=90)

# ---- 7CA1 Advanced (standalone): a pentagonal table with ten seats — five at the corners facing outside and five at
#      the middle of the sides facing the centre. Seats 0..9 anticlockwise, even = corner, odd = side; Aditi at 0.
P = ["Aditi", "Bipin", "Dhanush", "Gautam", "Hansraj", "Jasmeet", "Laboni", "Murali", "Neelima", "Sameer"]
pf = lambda s: "O" if s % 2 == 0 else "C"
conds = [
    ("Aditi sits at a corner, and Murali sits immediately to her left.", ("Murali", "Aditi"),
     lambda m, a: m == CR(a, pf(a), -1, 10)),
    ("Neelima sits second to the right of Murali.", ("Neelima", "Murali"), lambda n, m: n == CR(m, pf(m), 2, 10)),
    ("Gautam sits immediately to the left of Neelima.", ("Gautam", "Neelima"), lambda g, n: g == CR(n, pf(n), -1, 10)),
    ("Sameer sits second to the right of Neelima, and Bipin sits immediately to the left of Sameer.",
     ("Sameer", "Neelima", "Bipin"), lambda s, n, b: s == CR(n, pf(n), 2, 10) and b == CR(s, pf(s), -1, 10)),
    ("Hansraj sits immediately between Aditi and Laboni.", ("Hansraj", "Aditi", "Laboni"),
     lambda h, a, l: {(h + 1) % 10, (h - 1) % 10} == {a, l}),
    ("Dhanush faces the centre.", ("Dhanush",), lambda d: pf(d) == "C"),
]
S = unique(P, {"Aditi": [0]} | {p: range(10) for p in P[1:]}, conds, [P])
at = inv(S, P)
assert [at[i] for i in range(10)] == ["Aditi", "Murali", "Gautam", "Neelima", "Bipin", "Sameer", "Jasmeet", "Dhanush",
                                      "Laboni", "Hansraj"]
ans = at[CR(S["Laboni"], "O", 3, 10)]
assert ans == "Sameer"
alone(CIR, INOUT, "Advanced",
      "Ten persons Aditi, Bipin, Dhanush, Gautam, Hansraj, Jasmeet, Laboni, Murali, Neelima and Sameer sit around a "
      "table shaped like a regular pentagon. Five of them sit at the five corners and face away from the centre; the "
      "other five sit at the middle of the five sides and face the centre. Corner and side seats alternate around the "
      "table. (Facing the centre, the right is anticlockwise; facing outside, it is clockwise.)", conds,
      "Who sits third to the right of Laboni?", ans, ["Jasmeet", "Dhanush", "Hansraj"],
      "Corner persons face outside, side persons face the centre: read each clue with the speaker's own facing",
      "Number the seats 0 to 9 anticlockwise from Aditi (corner); even seats are corners (outside), odd seats sides "
      "(centre). Murali, to Aditi's left (anticlockwise), is at 1. Neelima is second to Murali's right "
      "(anticlockwise): 3. Gautam, to Neelima's left (clockwise): 2. Sameer, second to Neelima's right: 5, and Bipin, "
      "to Sameer's left: 4. Hansraj sits between Aditi and Laboni: seat 1 is taken, so Hansraj = 9 and Laboni = 8. "
      "Dhanush faces the centre: 7, and Jasmeet 6. Laboni (8) faces outside, so her right is clockwise: 7, 6, 5 — "
      "third to her right is Sameer.",
      ["Even seats: corners, facing outside (right = clockwise); odd seats: sides, facing the centre (right = "
       "anticlockwise)", "Aditi 0 ⇒ Murali 1 ⇒ Neelima 3 ⇒ Gautam 2", "Sameer 5 ⇒ Bipin 4",
       "Hansraj between Aditi and Laboni ⇒ Hansraj 9, Laboni 8", "Dhanush 7 (side), Jasmeet 6",
       "Laboni 8, facing outside ⇒ right = clockwise: 7, 6, 5 ⇒ Sameer"],
      why="Dhanush is immediately and Jasmeet second to her right; Hansraj is immediately to her left.", sec=120)


# ================================================================================================ floor helpers
def floors_table(n, cols, rows_fn, header):
    """Top floor first, as the floors appear in a building."""
    return table(header, [rows_fn(f) for f in range(n, 0, -1)])


# ---- 7F1 Basic set (4): six floors, favourite colours (floor 1 = lowermost)
P = ["Kavin", "Lajja", "Mrinalini", "Nimit", "Pooja", "Suhas"]
CO = ["Blue", "Green", "Orange", "Pink", "Purple", "Yellow"]
conds = [
    ("Kavin lives on floor 3.", ("Kavin",), lambda k: k == 3),
    ("Only one person lives between Kavin and Lajja, and Lajja lives above Kavin.", ("Lajja", "Kavin"),
     lambda l, k: l == k + 2),
    ("Mrinalini lives immediately above Lajja.", ("Mrinalini", "Lajja"), lambda m, l: m == l + 1),
    ("The person who likes Green lives immediately below Lajja.", ("Green", "Lajja"), lambda g, l: g == l - 1),
    ("Suhas lives above Pooja, and Nimit does not live on an even-numbered floor.", ("Suhas", "Pooja", "Nimit"),
     lambda s, p, n: s > p and n % 2 == 1),
    ("The person who likes Pink lives on the topmost floor.", ("Pink",), lambda p: p == 6),
    ("The person who likes Purple lives immediately below the person who likes Green.", ("Purple", "Green"),
     lambda p, g: p == g - 1),
    ("Pooja likes Blue.", ("Pooja", "Blue"), lambda p, b: p == b),
    ("The person who likes Yellow lives on an odd-numbered floor below Kavin.", ("Yellow", "Kavin"),
     lambda y, k: y % 2 == 1 and y < k),
]
S = unique(P + CO, {v: range(1, 7) for v in P + CO}, conds, [P, CO])
at, col = inv(S, P), inv(S, CO)
cof = {p: col[S[p]] for p in P}
assert [(at[i], col[i]) for i in range(1, 7)] == [("Nimit", "Yellow"), ("Pooja", "Blue"), ("Kavin", "Purple"),
                                                    ("Suhas", "Green"), ("Lajja", "Orange"), ("Mrinalini", "Pink")]
ARR = "Bottom to top: " + ", ".join(f"floor {i} {at[i]} ({col[i]})" for i in range(1, 7))
puzzle(FLR, FA, "Basic", "Six floors and six favourite colours",
       "Six persons Kavin, Lajja, Mrinalini, Nimit, Pooja and Suhas live on the six floors of a building, one on each "
       "floor. Floor 1 is the lowermost and floor 6 the topmost. Each of them likes a different colour among Blue, "
       "Green, Orange, Pink, Purple and Yellow.", conds,
       "Step 1: Kavin = 3, Lajja = 5, Mrinalini = 6.\n"
       "Step 2: Floors 1, 2 and 4 remain for Nimit, Pooja and Suhas. Nimit is on an odd floor: 1. Suhas is above Pooja: "
       "Pooja = 2, Suhas = 4.\n"
       "Step 3: Green is immediately below Lajja: floor 4 (Suhas). Purple is immediately below Green: floor 3 (Kavin). "
       "Pink is on floor 6 (Mrinalini). Pooja likes Blue.\n"
       "Step 4: Yellow is on an odd floor below Kavin: floor 1 (Nimit). Orange is left for Lajja.\n\n"
       + floors_table(6, None, lambda f: (f, at[f], col[f]), ["Floor", "Person", "Colour"]), ARR)
ans = at[S["Green"]]
assert ans == "Suhas"
ask("Who likes Green?", ans, ["Kavin", "Pooja", "Lajja"], "Placing an attribute relative to a fixed person",
    "Lajja lives on floor 5, so the person immediately below her, on floor 4, likes Green: Suhas.",
    ["Lajja = 5 ⇒ Green = floor 4", "Floor 4 = Suhas"],
    why="Kavin likes Purple, Pooja Blue and Lajja Orange.", sec=40)
ans = cof["Lajja"]
assert ans == "Orange"
ask("Which colour does Lajja like?", ans, ["Pink", "Yellow", "Green"], "The last colour by elimination",
    "Pink, Green, Purple, Blue and Yellow go to Mrinalini, Suhas, Kavin, Pooja and Nimit, so Lajja likes Orange.",
    ["Pink 6, Green 4, Purple 3, Blue 2 (Pooja), Yellow 1", "Left for Lajja: Orange"],
    why="Pink is Mrinalini's, Yellow Nimit's and Green Suhas's colour.", sec=40)
n_ = abs(S["Pooja"] - S["Mrinalini"]) - 1
assert n_ == 3
c_, w_ = bal(n_)
ask("How many persons live between Pooja and Mrinalini?", c_, w_, "Floors strictly between two persons",
    "Pooja is on floor 2 and Mrinalini on floor 6, so floors 3, 4 and 5 lie between them: three persons.",
    ["Pooja 2, Mrinalini 6", "Between: 3, 4, 5 ⇒ three"], natural=by_num, sec=40)
ans = at[S["Purple"] + 1]
assert ans == "Suhas"
ask("Who lives immediately above the person who likes Purple?", ans, ["Nimit", "Lajja", "Pooja"],
    "Locate the attribute, then move one floor",
    "Purple is liked by Kavin on floor 3. Floor 4, immediately above, is Suhas's.",
    ["Purple = Kavin = floor 3", "Floor 4 = Suhas"],
    why="Pooja lives immediately below Kavin; Lajja is two floors above him; Nimit is on floor 1.", sec=40)

# ---- 7F2 Basic set (4): eight floors, no attribute
P = ["Akhil", "Bansi", "Chinu", "Darpan", "Eela", "Falgun", "Gopi", "Himani"]
conds = [
    ("Darpan lives on the topmost floor.", ("Darpan",), lambda d: d == 8),
    ("Exactly three persons live between Darpan and Eela.", ("Eela", "Darpan"), lambda e, d: abs(e - d) == 4),
    ("Chinu lives immediately above Eela, and Gopi lives immediately below Eela.", ("Chinu", "Gopi", "Eela"),
     lambda c, g, e: c == e + 1 and g == e - 1),
    ("Akhil lives on an even-numbered floor below Eela.", ("Akhil", "Eela"), lambda a, e: a % 2 == 0 and a < e),
    ("Bansi lives two floors above Chinu.", ("Bansi", "Chinu"), lambda b, c: b == c + 2),
    ("Himani lives above Falgun.", ("Himani", "Falgun"), lambda h, f: h > f),
]
S = unique(P, {p: range(1, 9) for p in P}, conds, [P])
at = inv(S, P)
assert [at[i] for i in range(1, 9)] == ["Falgun", "Akhil", "Gopi", "Eela", "Chinu", "Himani", "Bansi", "Darpan"]
ARR = "Bottom to top: " + ", ".join(f"{i} {at[i]}" for i in range(1, 9))
puzzle(FLR, FF, "Basic", "Eight persons on eight floors",
       "Eight persons Akhil, Bansi, Chinu, Darpan, Eela, Falgun, Gopi and Himani live on the eight floors of a "
       "building, one on each floor. Floor 1 is the lowermost and floor 8 the topmost.", conds,
       "Step 1: Darpan = 8. Three persons live between Darpan and Eela: Eela = 4.\n"
       "Step 2: Chinu = 5 and Gopi = 3. Bansi is two floors above Chinu: 7.\n"
       "Step 3: Akhil is on an even floor below 4: floor 2.\n"
       "Step 4: Floors 1 and 6 remain for Falgun and Himani; Himani is above Falgun: Himani = 6, Falgun = 1.\n\n"
       + floors_table(8, None, lambda f: (f, at[f]), ["Floor", "Person"]), ARR)
ans = at[S["Bansi"] - 1]
assert ans == "Himani"
ask("Who lives immediately below Bansi?", ans, ["Chinu", "Darpan", "Eela"], "Reading a neighbour off the floors",
    "Bansi lives on floor 7; floor 6 is Himani's.", ["Bansi = 7", "Floor 6 = Himani"],
    why="Chinu is two floors below Bansi, Darpan is above him, and Eela is on floor 4.", sec=35)
n_ = abs(S["Akhil"] - S["Chinu"]) - 1
c_, w_ = bal(n_)
ask("How many persons live between Akhil and Chinu?", c_, w_, "Floors strictly between two persons",
    f"Akhil is on floor 2 and Chinu on floor 5, so Gopi (3) and Eela (4) live between them.",
    ["Akhil 2, Chinu 5", "Between: 3, 4 ⇒ two"], natural=by_num, sec=40)
ans = at[1]
assert ans == "Falgun"
ask("Who lives on the lowermost floor?", ans, ["Akhil", "Himani", "Gopi"], "The last pair is settled by an 'above' "
    "clue", "After the others are placed, floors 1 and 6 remain for Falgun and Himani. Himani lives above Falgun, so "
    "Falgun is on floor 1.", ["Free floors: 1 and 6", "Himani above Falgun ⇒ Falgun = 1"],
    why="Akhil is on floor 2, Himani on 6 and Gopi on 3.", sec=40)
t, f = one_true([("Gopi lives immediately above Akhil", S["Gopi"] == S["Akhil"] + 1),
                 ("Eela lives exactly in the middle of Darpan and Falgun", 2 * S["Eela"] == S["Darpan"] + S["Falgun"]),
                 ("Himani lives on an odd-numbered floor", S["Himani"] % 2 == 1),
                 ("Three persons live between Bansi and Eela", abs(S["Bansi"] - S["Eela"]) == 4)])
ask("Which of the following statements is true?", t, f, "Checking each statement against the floors",
    "Gopi (floor 3) lives immediately above Akhil (floor 2).",
    ["Gopi 3, Akhil 2 ✓", "Darpan 8 and Falgun 1: the middle would be 4.5, not Eela's floor 4 ✗",
     "Himani lives on floor 6, an even floor ✗", "Bansi 7, Eela 4 ⇒ only Chinu and Himani (two persons) between ✗"],
    why="Eela is not midway between floors 8 and 1, Himani's floor is even, and only two persons live between Bansi and "
        "Eela.", sec=45)


# ---- 7F3 Intermediate set (3): seven floors, family sizes with arithmetic clues. Variables: floor of each person and
#      family size ("m" + name) of each person.
P = ["Jairam", "Kumud", "Madhav", "Oorja", "Pawan", "Rachit", "Shruti"]
M = ["m" + p for p in P]
V = ["Shruti", "Pawan", "mPawan", "mShruti", "Madhav", "mMadhav", "Jairam", "mJairam", "Oorja", "Kumud", "Rachit",
     "mOorja", "mRachit", "mKumud"]
conds = [
    ("Shruti lives on floor 4, and Pawan lives immediately below her. Shruti's family has twice as many members as "
     "Pawan's.", ("Shruti", "Pawan", "mPawan", "mShruti"), lambda s, p, mp, ms: s == 4 and p == 3 and ms == 2 * mp),
    ("Madhav lives on the topmost floor, and his family has one member more than Pawan's.",
     ("Madhav", "mMadhav", "mPawan"), lambda m, mm, mp: m == 7 and mm == mp + 1),
    ("Only one person lives between Madhav and Jairam, and Jairam's family is the smallest of all.",
     ("Madhav", "Jairam", "mJairam"), lambda m, j, mj: abs(m - j) == 2 and mj == 2),
    ("Oorja lives immediately below Madhav. Her family has as many members as Jairam's and Rachit's families "
     "together.", ("Oorja", "Madhav", "mOorja", "mJairam", "mRachit"),
     lambda o, m, mo, mj, mr: o == m - 1 and mo == mj + mr),
    ("Kumud lives above Rachit.", ("Kumud", "Rachit"), lambda k, r: k > r),
    ("The family on floor 2 is the largest of all.", (*P, *M), lambda *x: x[7 + x[:7].index(2)] == 8),
]
dom = {p: range(1, 8) for p in P} | {m: range(2, 9) for m in M}
S = unique(V, dom, conds, [P, M])
at = inv(S, P)
mem = {p: S["m" + p] for p in P}
assert [(at[i], mem[at[i]]) for i in range(1, 8)] == [("Rachit", 5), ("Kumud", 8), ("Pawan", 3), ("Shruti", 6),
                                                       ("Jairam", 2), ("Oorja", 7), ("Madhav", 4)]
ARR = "Bottom to top: " + ", ".join(f"{i} {at[i]} ({mem[at[i]]})" for i in range(1, 8)) + " (family members)"
puzzle(FLR, FA, "Intermediate", "Seven floors and seven family sizes",
       "Seven persons Jairam, Kumud, Madhav, Oorja, Pawan, Rachit and Shruti live on the seven floors of a building, one "
       "on each floor (floor 1 is the lowermost, floor 7 the topmost). Their families have 2, 3, 4, 5, 6, 7 and 8 "
       "members, a different number for each person.", conds,
       "Step 1: Shruti = 4, Pawan = 3, Madhav = 7, Oorja = 6. Jairam is two floors from Madhav: 5. Kumud and Rachit take "
       "floors 2 and 1; Kumud is above Rachit, so Kumud = 2, Rachit = 1.\n"
       "Step 2: Jairam's family is the smallest: 2. Kumud (floor 2) has the largest family: 8.\n"
       "Step 3: Shruti = 2 × Pawan and Madhav = Pawan + 1. From 3, 4, 5, 6, 7 the only doubling pair is 3 and 6, so "
       "Pawan = 3, Shruti = 6, Madhav = 4.\n"
       "Step 4: 5 and 7 remain for Oorja and Rachit, and Oorja = 2 + Rachit: Rachit = 5, Oorja = 7.\n\n"
       + floors_table(7, None, lambda f: (f, at[f], mem[at[f]]), ["Floor", "Person", "Family members"]), ARR)
tot = mem[at[1]] + mem[at[2]]
assert tot == 13
c_, w_ = bal(tot, fmt=str, lo=10)
ask("What is the total number of family members of the persons living on floors 1 and 2?", c_, w_,
    "Settle both families before adding", "Floor 2 is Kumud (largest family, 8) and floor 1 is Rachit (5): 8 + 5 = 13.",
    ["Kumud (floor 2) = 8", "Rachit (floor 1) = 7 − 2 = 5", "8 + 5 = 13"], natural=int, sec=60)
ans = at[S[next(p for p in P if mem[p] == 7)] + 1]
assert ans == "Madhav"
ask("Who lives immediately above the person whose family has 7 members?", ans, ["Jairam", "Oorja", "Shruti"],
    "Use the sum clue to find the 7-member family",
    "Oorja's family equals Jairam's (2) plus Rachit's; with 5 and 7 left, Rachit = 5 and Oorja = 7. Oorja is on floor "
    "6, so Madhav (floor 7) lives immediately above her.",
    ["5 and 7 left for Oorja and Rachit; Oorja = 2 + Rachit ⇒ Oorja = 7", "Oorja = floor 6 ⇒ floor 7 = Madhav"],
    why="Jairam lives immediately below Oorja; Oorja is the 7-member family herself; Shruti is on floor 4.", sec=60)
five = next(p for p in P if mem[p] == 5)
n_ = 7 - S[five]
assert n_ == 6
c_, w_ = bal(n_)
ask("How many persons live above the person whose family has 5 members?", c_, w_,
    "Find the person, then count the floors above", "The 5-member family is Rachit's, on floor 1, so all six others "
    "live above him.", ["5 members = Rachit = floor 1", "Floors 2–7 ⇒ six persons above"], natural=by_num, sec=55)

# ---- 7F4 Advanced set (5): eight floors, each person with a profession and a home city
P = ["Amolika", "Bhargav", "Chandan", "Damayanti", "Girish", "Hamida", "Jignesh", "Kalpesh"]
PR = ["Architect", "Banker", "Chef", "Dentist", "Engineer", "Lawyer", "Pilot", "Teacher"]
CT = ["Gaya", "Jaipur", "Kanpur", "Mysuru", "Nagpur", "Pune", "Ranchi", "Shimla"]
conds = [
    ("The Architect lives on the lowermost floor, and exactly three persons live between the Architect and the "
     "Lawyer.", ("Architect", "Lawyer"), lambda a, l: a == 1 and l == 5),
    ("The person from Jaipur lives immediately below the Lawyer.", ("Jaipur", "Lawyer"), lambda j, l: j == l - 1),
    ("Girish lives on the topmost floor and is the Pilot. The Pilot lives two floors above the Chef.",
     ("Girish", "Pilot", "Chef"), lambda g, p, c: g == 8 and p == g and c == p - 2),
    ("Hamida lives immediately below Girish, and the Dentist is from Shimla.", ("Hamida", "Girish", "Dentist", "Shimla"),
     lambda h, g, d, s: h == g - 1 and d == s),
    ("Kalpesh lives immediately below Damayanti, and Damayanti lives on an odd-numbered floor.",
     ("Kalpesh", "Damayanti"), lambda k, d: k == d - 1 and d % 2 == 1),
    ("The Engineer lives on an odd-numbered floor, immediately below the Teacher.", ("Engineer", "Teacher"),
     lambda e, t: e % 2 == 1 and t == e + 1),
    ("Chandan lives immediately above the Architect and is from Kanpur.", ("Chandan", "Architect", "Kanpur"),
     lambda c, a, k: c == a + 1 and k == c),
    ("Amolika is from Mysuru, and the person from Gaya lives somewhere below her.", ("Amolika", "Mysuru", "Gaya"),
     lambda a, m, g: a == m and g < a),
    ("The person from Pune lives above the person from Shimla, and the person from Nagpur lives on an even-numbered "
     "floor.", ("Pune", "Shimla", "Nagpur"), lambda p, s, n: p > s and n % 2 == 0),
    ("Bhargav is not the Architect.", ("Bhargav", "Architect"), lambda b, a: b != a),
]
V = PR + ["Girish", "Hamida", "Damayanti", "Kalpesh", "Chandan", "Amolika", "Bhargav", "Jignesh"] + CT
S = unique(V, {v: range(1, 9) for v in V}, conds, [P, PR, CT])
at, pro, cit = inv(S, P), inv(S, PR), inv(S, CT)
assert [(at[i], pro[i], cit[i]) for i in range(1, 9)] == [
    ("Jignesh", "Architect", "Gaya"), ("Chandan", "Banker", "Kanpur"), ("Amolika", "Engineer", "Mysuru"),
    ("Kalpesh", "Teacher", "Jaipur"), ("Damayanti", "Lawyer", "Ranchi"), ("Bhargav", "Chef", "Nagpur"),
    ("Hamida", "Dentist", "Shimla"), ("Girish", "Pilot", "Pune")]
ARR = "Bottom to top: " + ", ".join(f"{i} {at[i]} ({pro[i]}, {cit[i]})" for i in range(1, 9))
puzzle(FLR, FA, "Advanced", "Eight floors, eight professions and eight home cities",
       "Eight persons Amolika, Bhargav, Chandan, Damayanti, Girish, Hamida, Jignesh and Kalpesh live on the eight floors "
       "of a building, one on each floor (floor 1 is the lowermost, floor 8 the topmost). Each has a different "
       "profession among Architect, Banker, Chef, Dentist, Engineer, Lawyer, Pilot and Teacher, and each is from a "
       "different city among Gaya, Jaipur, Kanpur, Mysuru, Nagpur, Pune, Ranchi and Shimla.", conds,
       "Step 1: Architect = 1, Lawyer = 5, Jaipur = 4. Girish = 8 and is the Pilot, so the Chef is on floor 6. "
       "Hamida = 7. Chandan = 2 (above the Architect), from Kanpur.\n"
       "Step 2: Damayanti is on an odd floor with Kalpesh immediately below. Floor 1 has nothing below, floor 3 would "
       "need Kalpesh on Chandan's floor 2, and floor 7 is Hamida's, so Damayanti = 5 (Lawyer) and Kalpesh = 4 "
       "(Jaipur).\n"
       "Step 3: The Engineer is on an odd floor immediately below the Teacher: floor 1 is the Architect and floor 7 "
       "would need the Teacher on the Pilot's floor 8, so Engineer = 3 and Teacher = 4 (Kalpesh).\n"
       "Step 4: Banker and Dentist remain for floors 2 and 7. The Dentist is from Shimla, but floor 2 is Kanpur, so "
       "Dentist = 7 (Hamida, Shimla) and Banker = 2 (Chandan). Pune is above Shimla: floor 8.\n"
       "Step 5: Amolika, Bhargav and Jignesh take floors 1, 3 and 6; Gaya, Mysuru, Nagpur and Ranchi go to floors 1, 3, "
       "5 and 6. Nagpur is on an even floor: 6. Amolika is from Mysuru with Gaya below her, so she is not on 1 or 6: "
       "Amolika = 3 (Mysuru), Gaya = 1 and Ranchi = 5. Bhargav is not the Architect: Bhargav = 6, Jignesh = 1.\n\n"
       + floors_table(8, None, lambda f: (f, at[f], pro[f], cit[f]), ["Floor", "Person", "Profession", "City"]), ARR)
ans = at[S["Chef"]]
assert ans == "Bhargav"
ask("Who is the Chef?", ans, ["Hamida", "Amolika", "Jignesh"], "The Pilot's floor fixes the Chef's floor",
    "Girish, the Pilot, lives on floor 8, so the Chef lives on floor 6. Of the three persons left for floors 1, 3 and "
    "6, Amolika must be on floor 3 and Bhargav, who is not the Architect, takes floor 6.",
    ["Pilot = 8 ⇒ Chef = 6", "Amolika = 3 (Mysuru, Gaya below her)", "Bhargav not the Architect ⇒ Bhargav = 6"],
    why="Hamida is the Dentist, Amolika the Engineer and Jignesh the Architect.", sec=75)
ans = cit[S["Lawyer"]]
assert ans == "Ranchi"
ask("Which city is the Lawyer from?", ans, ["Jaipur", "Nagpur", "Mysuru"], "Cities fill in after the professions",
    "The Lawyer lives on floor 5. Once Kanpur (2), Jaipur (4), Shimla (7), Pune (8), Nagpur (6), Mysuru (3) and Gaya "
    "(1) are placed, Ranchi is left for floor 5.",
    ["Lawyer = floor 5 (Damayanti)", "Nagpur 6 (even), Mysuru 3, Gaya 1 ⇒ Ranchi 5"],
    why="Jaipur is the Teacher's city (floor 4), Nagpur the Chef's and Mysuru the Engineer's.", sec=75)
n_ = abs(S["Engineer"] - S["Shimla"]) - 1
assert n_ == 3
c_, w_ = bal(n_)
ask("How many persons live between the Engineer and the person from Shimla?", c_, w_,
    "Locate both through their own clues, then count",
    "The Engineer lives on floor 3 and the person from Shimla (the Dentist) on floor 7, so floors 4, 5 and 6 lie "
    "between them: three persons.", ["Engineer = 3", "Shimla = Dentist = 7", "Between: 4, 5, 6 ⇒ three"],
    natural=by_num, sec=70)
ans = at[S["Teacher"] - 1]
assert ans == "Amolika"
ask("Who lives immediately below the Teacher?", ans, ["Chandan", "Damayanti", "Jignesh"],
    "The Engineer is immediately below the Teacher",
    "The Teacher (Kalpesh) lives on floor 4 and the Engineer immediately below on floor 3. Floor 3 is Amolika's.",
    ["Teacher = floor 4", "Floor 3 = Engineer = Amolika"],
    why="Chandan lives on floor 2, Damayanti immediately above the Teacher, and Jignesh on floor 1.", sec=70)
combos = [(p, pro[S[p]], cit[S[p]]) for p in P]
t, f = one_true([("Chandan – Banker – Kanpur", ("Chandan", "Banker", "Kanpur") in combos),
                 ("Hamida – Dentist – Pune", ("Hamida", "Dentist", "Pune") in combos),
                 ("Jignesh – Architect – Mysuru", ("Jignesh", "Architect", "Mysuru") in combos),
                 ("Kalpesh – Engineer – Jaipur", ("Kalpesh", "Engineer", "Jaipur") in combos)])
ask("Which of the following person – profession – city combinations is correct?", t, f,
    "Check all three parts of each combination", "Chandan lives on floor 2, is the Banker and is from Kanpur.",
    ["Chandan: floor 2, Banker, Kanpur ✓", "Hamida is from Shimla, not Pune ✗", "Jignesh is from Gaya ✗",
     "Kalpesh is the Teacher ✗"], why="Each of the other combinations has one wrong part.", sec=70)


# ================================================================================================ BOXES, batch 007
# ---- 7BB1 Basic (standalone): six boxes, positions counted from the TOP (1 = top, 6 = bottom)
B = ["A", "F", "J", "M", "R", "X"]
conds = [
    ("Box X is kept fourth from the top.", ("X",), lambda x: x == 4),
    ("Only one box is kept between Box X and Box R, and Box R is kept above Box X.", ("R", "X"),
     lambda r, x: r == x - 2),
    ("Box M is kept at the bottom of the stack, and Box F is kept immediately above Box M.", ("M", "F"),
     lambda m, f: m == 6 and f == 5),
    ("Box J is kept above Box A.", ("J", "A"), lambda j, a: j < a),
]
S = unique(B, {b: range(1, 7) for b in B}, conds, [B])
at = inv(S, B)
assert [at[i] for i in range(1, 7)] == ["J", "R", "A", "X", "F", "M"]
ans = at[S["R"] + 1]
alone(BOX, STK, "Basic",
      "Six boxes A, F, J, M, R and X are kept one above another in a single stack. The positions are counted from the "
      "top: position 1 is the top of the stack and position 6 the bottom.", conds,
      f"Which box is kept immediately below Box R?", "Box " + ans, ["Box X", "Box J", "Box F"],
      "When positions are counted from the top, 'below' means a larger position number",
      "X = 4th from the top and R is two places above it: 2nd. M = 6th and F = 5th. Positions 1 and 3 remain for J and "
      "A; J is above A, so J = 1st and A = 3rd. Immediately below R (2nd) is the 3rd box: A.",
      ["X = 4, R = 2, M = 6, F = 5 (from the top)", "J above A ⇒ J = 1, A = 3", "Below R (2) ⇒ position 3 = A"],
      why="X is two places below R, J is immediately above R, and F is near the bottom.", sec=45)

# ---- 7BB2 Basic (standalone): six boxes holding different numbers of pens (1 = bottom)
B = ["B", "D", "H", "L", "P", "T"]
PN = ["p" + b for b in B]
conds = [
    ("Box B is kept third from the bottom and contains the most pens.", ("B", "pB"), lambda b, p: b == 3 and p == 9),
    ("Box D is kept two places above Box B.", ("D", "B"), lambda d, b: d == b + 2),
    ("Box P is kept immediately above Box B.", ("P", "B"), lambda p, b: p == b + 1),
    ("Box L is kept at the top and contains 6 pens.", ("L", "pL"), lambda l, p: l == 6 and p == 6),
    ("Box H is kept below Box T.", ("H", "T"), lambda h, t: h < t),
    ("The box with 4 pens is kept immediately below Box B.", (*B, *PN),
     lambda *x: x[6 + x[:6].index(x[0] - 1)] == 4 if x[0] - 1 in x[:6] else False),
    ("Box D contains three pens more than Box P.", ("pD", "pP"), lambda d, p: d == p + 3),
]
S = unique(B + PN, {b: range(1, 7) for b in B} | {p: range(4, 10) for p in PN}, conds, [B, PN])
at = inv(S, B)
pens = {b: S["p" + b] for b in B}
assert [(at[i], pens[at[i]]) for i in range(1, 7)] == [("H", 7), ("T", 4), ("B", 9), ("P", 5), ("D", 8), ("L", 6)]
c_, w_ = bal(pens["H"], fmt=str, lo=4, hi=9)
alone(BOX, BWC, "Basic",
      "Six boxes B, D, H, L, P and T are kept one above another in a single stack (position 1 is the bottom and 6 the "
      "top). The boxes contain 4, 5, 6, 7, 8 and 9 pens, a different number in each box.", conds,
      "How many pens does Box H contain?", c_, w_, "Place the boxes first, then the counts",
      "B = 3, D = 5, P = 4, L = 6. Positions 1 and 2 remain for H and T, and H is below T: H = 1, T = 2. The box "
      "immediately below B is T, so T has 4 pens. B has 9 and L has 6, leaving 5, 7 and 8 for D, H and P. D = P + 3 "
      "fits only 8 and 5, so H has 7 pens.",
      ["Positions: H 1, T 2, B 3, P 4, D 5, L 6", "B 9, L 6, T (below B) 4", "Left 5, 7, 8; D = P + 3 ⇒ D 8, P 5",
       "H = 7"], why="5 is in Box P, 8 in Box D and 6 in Box L.", natural=int, sec=60)

# ---- 7BI1 Intermediate set (4): seven boxes, each with a weight and a colour (1 = bottom)
B = ["C", "G", "K", "N", "Q", "U", "Z"]
W = ["w" + b for b in B]
CL = ["Black", "Brown", "Cream", "Gold", "Maroon", "Silver", "Violet"]
WT = [12, 15, 18, 22, 26, 30, 35]
wat = lambda pos_w, p: next(w for b, w in pos_w if b == p)  # weight of the box at position p
conds = [
    ("Box C is kept exactly in the middle of the stack, and Box Q is kept immediately above Box C.", ("C", "Q"),
     lambda c, q: c == 4 and q == 5),
    ("Box N is kept at the top. It is 4 kg heavier than Box C.", ("N", "wN", "wC"), lambda n, wn, wc: n == 7 and
     wn == wc + 4),
    ("Exactly three boxes are kept between Box N and Box Z.", ("Z", "N"), lambda z, n: abs(z - n) == 4),
    ("Box Z is the heaviest box, and its colour is Gold.", ("wZ", "Z", "Gold"), lambda w, z, g: w == 35 and g == z),
    ("Box K is kept immediately below Box Z and is the lightest box.", ("K", "Z", "wK"),
     lambda k, z, w: k == z - 1 and w == 12),
    ("Box U is kept below Box G.", ("U", "G"), lambda u, g: u < g),
    ("Box Q is twice as heavy as Box G.", ("wQ", "wG"), lambda q, g: q == 2 * g),
    ("The Silver box is kept at the bottom, and it weighs 26 kg.", ("Silver", *B, *W),
     lambda s, *x: s == 1 and x[7 + x[:7].index(1)] == 26),
    ("The Black box is the lightest box.", ("Black", "K"), lambda b, k: b == k),
    ("The Violet box is kept immediately between the Gold box and the Brown box.", ("Violet", "Gold", "Brown"),
     lambda v, g, b: min(g, b) < v < max(g, b) and abs(g - b) == 2),
    ("The Cream box is lighter than the Maroon box.", ("Cream", "Maroon", *B, *W),
     lambda c, m, *x: x[7 + x[:7].index(c)] < x[7 + x[:7].index(m)]),
]
V = ["C", "Q", "N", "Z", "K", "U", "G"] + W + CL
S = unique(V, {b: range(1, 8) for b in B} | {w: WT for w in W} | {c: range(1, 8) for c in CL}, conds, [B, W, CL])
at, colr = inv(S, B), inv(S, CL)
wt = {b: S["w" + b] for b in B}
assert [(at[i], wt[at[i]], colr[i]) for i in range(1, 8)] == [
    ("U", 26, "Silver"), ("K", 12, "Black"), ("Z", 35, "Gold"), ("C", 18, "Violet"), ("Q", 30, "Brown"),
    ("G", 15, "Cream"), ("N", 22, "Maroon")]
ARR = "Bottom to top: " + ", ".join(f"{i} {at[i]} ({wt[at[i]]} kg, {colr[i]})" for i in range(1, 8))
puzzle(BOX, BWC, "Intermediate", "Seven boxes with weights and colours",
       "Seven boxes C, G, K, N, Q, U and Z are kept one above another in a single stack (position 1 is the bottom and 7 "
       "the top). Their weights are 12, 15, 18, 22, 26, 30 and 35 kg, and their colours are Black, Brown, Cream, Gold, "
       "Maroon, Silver and Violet, one weight and one colour per box.", conds,
       "Step 1: C = 4, Q = 5, N = 7. Three boxes lie between N and Z: Z = 3 (Gold, 35 kg). K = 2 (12 kg, so Black).\n"
       "Step 2: Positions 1 and 6 remain for U and G; U is below G: U = 1, G = 6. The Silver box is at the bottom and "
       "weighs 26 kg: U.\n"
       "Step 3: Weights left: 15, 18, 22, 30 for C, G, N, Q. N = C + 4 gives 18 and 22; Q = 2 × G gives 15 and 30. So "
       "C = 18, N = 22, G = 15, Q = 30.\n"
       "Step 4: Violet lies between Gold (3) and Brown with one box between them, so Brown = 5 (Q) and Violet = 4 (C). "
       "Cream and Maroon remain for G (15 kg) and N (22 kg); Cream is lighter: G Cream, N Maroon.\n\n"
       + table(["Position", "Box", "Weight (kg)", "Colour"],
               [(i, at[i], wt[at[i]], colr[i]) for i in range(7, 0, -1)]), ARR)
c_, w_ = bal(wt["Q"], fmt=lambda v: f"{v} kg", step=WT[1] - WT[0], lo=12)
ask("What is the weight of Box Q?", c_, w_, "Pair the remaining weights with the two weight clues",
    "After 35 (Z), 12 (K) and 26 (U), the weights 15, 18, 22 and 30 remain. N = C + 4 needs 18 and 22, so Q = 2 × G "
    "takes 15 and 30: Q weighs 30 kg.", ["Free: 15, 18, 22, 30", "N = C + 4 ⇒ 22 and 18", "Q = 2 × G ⇒ 30 and 15"],
    natural=lambda t: int(t.split()[0]), sec=60)
ans = colr[S["G"]]
assert ans == "Cream"
ask("What is the colour of Box G?", ans, ["Maroon", "Brown", "Violet"], "Use the weight comparison for the last pair",
    "Cream and Maroon remain for G (15 kg) and N (22 kg). The Cream box is the lighter of the two, so G is Cream.",
    ["Cream, Maroon left for G, N", "G 15 kg < N 22 kg ⇒ G = Cream"],
    why="Maroon is Box N's colour, Brown Box Q's and Violet Box C's.", sec=55)
n_ = abs(S["Black"] - S["Brown"]) - 1
assert n_ == 2
c_, w_ = bal(n_)
ask("How many boxes are kept between the Black box and the Brown box?", c_, w_, "Count positions strictly between",
    "The Black box (K) is at position 2 and the Brown box (Q) at position 5, so Z and C lie between them.",
    ["Black = K = 2, Brown = Q = 5", "Between: 3, 4 ⇒ two"], natural=by_num, sec=50)
tot = wt[at[S["Violet"] + 1]] + wt[at[S["Violet"] - 1]]
assert tot == 65
c_, w_ = bal(tot, fmt=lambda v: f"{v} kg", step=5, lo=50)
ask("What is the total weight of the boxes kept immediately above and immediately below the Violet box?", c_, w_,
    "Find the Violet box, then add its two neighbours",
    "The Violet box is C (position 4). Immediately above is Q (30 kg) and immediately below is Z (35 kg): 65 kg.",
    ["Violet = C = position 4", "Above: Q 30 kg; below: Z 35 kg", "30 + 35 = 65 kg"],
    natural=lambda t: int(t.split()[0]), sec=60)

# ---- 7BI2 Intermediate set (3): nine boxes in a 3 × 3 rack. Compartment = 10 × shelf + column, shelf 1 = bottom,
#      column 1 = left (as seen from the front).
B = ["D", "E", "G", "I", "M", "O", "R", "U", "W"]
CELLS = [10 * r + c for r in (1, 2, 3) for c in (1, 2, 3)]
conds = [
    ("Box U is kept in the centre compartment of the rack (middle shelf, middle column).", ("U",), lambda u: u == 22),
    ("Box M is kept directly below Box U.", ("M", "U"), lambda m, u: m == u - 10),
    ("Box E is kept immediately to the right of Box M, on the same shelf.", ("E", "M"), lambda e, m: e == m + 1),
    ("Box I is kept directly above Box E.", ("I", "E"), lambda i, e: i == e + 10),
    ("Box G is kept immediately to the left of Box O, on the same shelf.", ("G", "O"),
     lambda g, o: o == g + 1 and g % 10 in (1, 2)),
    ("Box D is kept directly below Box W.", ("D", "W"), lambda d, w: d == w - 10),
    ("Box R is kept on the bottom shelf.", ("R",), lambda r: r // 10 == 1),
]
S = unique(B, {b: CELLS for b in B}, conds, [B])
at = inv(S, B)
SH, CO_ = {3: "Top", 2: "Middle", 1: "Bottom"}, {1: "Left", 2: "Middle", 3: "Right"}
assert [[at[10 * r + c] for c in (1, 2, 3)] for r in (3, 2, 1)] == [["W", "G", "O"], ["D", "U", "I"],
                                                                     ["R", "M", "E"]]
ARR = "Rack (front view): " + "; ".join(
    f"{SH[r]} shelf: " + ", ".join(at[10 * r + c] for c in (1, 2, 3)) + " (left to right)" for r in (3, 2, 1))
puzzle(BOX, STK, "Intermediate", "Nine boxes in a three-by-three rack",
       "A rack has three shelves (top, middle and bottom), and each shelf has three compartments (left, middle and "
       "right, as seen from the front). Nine boxes D, E, G, I, M, O, R, U and W are kept in the rack, one in each "
       "compartment. 'Directly above/below' means in the same column on the next shelf.", conds,
       "Step 1: U = middle shelf, middle. M is directly below: bottom, middle. E is to M's right: bottom, right. I is "
       "directly above E: middle, right.\n"
       "Step 2: Free compartments: bottom-left, middle-left and the whole top shelf. R is on the bottom shelf: "
       "bottom-left.\n"
       "Step 3: D is directly below W, and only the left column has two free compartments one above the other "
       "(middle-left and top-left): D = middle-left, W = top-left.\n"
       "Step 4: G and O take the top-middle and top-right compartments, G on the left.\n\n"
       + table(["Shelf", "Left", "Middle", "Right"], [(SH[r], *[at[10 * r + c] for c in (1, 2, 3)]) for r in (3, 2, 1)]),
       ARR)
ans = at[S["D"] + 10]
assert ans == "W"
ask("Which box is kept directly above Box D?", "Box " + ans, ["Box R", "Box U", "Box G"],
    "Only one column still has two free compartments stacked together",
    "After U, M, E, I and R are placed, the left column has the middle and top compartments free, one above the "
    "other, so D (below) and W (above) go there.", ["Free pair in one column: middle-left and top-left",
                                                    "D middle-left ⇒ W top-left, directly above D"],
    why="R is directly below D, U is to D's right, and G is diagonally above D.", sec=50)
ans = at[33]
assert ans == "O"
ask("Which box is kept in the right compartment of the top shelf?", "Box " + ans, ["Box G", "Box I", "Box W"],
    "Fill the last shelf with the left-right clue",
    "Only the top-middle and top-right compartments remain for G and O, and G is immediately to the left of O, so O "
    "is in the top-right compartment.", ["Top shelf: W, _, _", "G immediately left of O ⇒ G middle, O right"],
    why="G is top-middle, W top-left, and I is on the middle shelf.", sec=50)
t, f = one_true([("U and M", {S["U"] % 10, S["M"] % 10} == {S["G"] % 10}),
                 ("D and R", {S["D"] % 10, S["R"] % 10} == {S["G"] % 10}),
                 ("I and E", {S["I"] % 10, S["E"] % 10} == {S["G"] % 10}),
                 ("O and I", {S["O"] % 10, S["I"] % 10} == {S["G"] % 10})])
ask("Which two boxes are kept in the same column as Box G?", t, f, "A column runs through all three shelves",
    "G is in the middle compartment of the top shelf, so its column also holds U (middle shelf) and M (bottom shelf).",
    ["G: top shelf, middle column", "Middle column below G: U, then M"],
    why="D and R are in the left column; I, E and O are in the right column.", sec=45)


# ---- 7BA1 Advanced set (6): eight boxes with weights, clues built on sums of weights (1 = bottom)
B = ["F", "J", "K", "P", "S", "T", "V", "Y"]
W = ["w" + b for b in B]
WT = [6, 9, 11, 14, 17, 20, 23, 27]
wpos = lambda x, p: x[8 + x[:8].index(p)]  # weight of the box at position p, from (*B positions, *W weights)
conds = [
    ("Box S is kept fifth from the bottom.", ("S",), lambda s: s == 5),
    ("The heaviest box is kept two places below Box S, and the lightest box is kept immediately below Box S.",
     ("S", "@27", "@6"), lambda s, h, l: h == s - 2 and l == s - 1),
    ("Exactly three boxes are kept between Box P and the heaviest box, and Box P is kept above it.",
     ("P", "@27"), lambda p, h: p == h + 4),
    ("Box K is kept between Box S and Box P.", ("K", "S", "P"), lambda k, s, p: min(s, p) < k < max(s, p)),
    ("Box V is kept at the top, and its weight equals the combined weight of Box F and Box P.",
     ("V", "wV", "wF", "wP"), lambda v, wv, wf, wp: v == 8 and wv == wf + wp),
    ("Box K weighs as much as Box S and Box J together.", ("wK", "wS", "wJ"), lambda k, s, j: k == s + j),
    ("Box J is kept immediately above Box T, and Box T is lighter than Box Y.", ("J", "T", "wT", "wY"),
     lambda j, t, wt_, wy: j == t + 1 and wt_ < wy),
    ("The two bottom boxes together weigh 29 kg.", tuple(f"@{v}" for v in WT),
     lambda *ks: sum(v for v, k in zip(WT, ks) if k in (1, 2)) == 29),
    ("Box P is lighter than Box V but heavier than Box J.", ("wP", "wV", "wJ"), lambda p, v, j: j < p < v),
]
KV, LINK = link(B, W, WT)
V = ["S", "@27", "@6", "P", "K", "V", "J", "T", "F", "Y", "wS", "wJ", "wK", "wF", "wP", "wV", "wT", "wY"]
V += [k for k in KV if k not in V]
S = unique(V, {b: range(1, 9) for b in B} | {w: WT for w in W} | {k: range(1, 9) for k in KV}, conds, [B, W, KV],
           extra=LINK)
at = inv(S, B)
wt = {b: S["w" + b] for b in B}
assert [(at[i], wt[at[i]]) for i in range(1, 9)] == [("T", 20), ("J", 9), ("Y", 27), ("F", 6), ("S", 14), ("K", 23),
                                                     ("P", 11), ("V", 17)]
ARR = "Bottom to top: " + ", ".join(f"{i} {at[i]} ({wt[at[i]]} kg)" for i in range(1, 9))
puzzle(BOX, BWC, "Advanced", "Eight boxes and the sums of their weights",
       "Eight boxes F, J, K, P, S, T, V and Y are kept one above another in a single stack (position 1 is the bottom "
       "and 8 the top). Their weights are 6, 9, 11, 14, 17, 20, 23 and 27 kg, one weight per box.", conds,
       "Step 1: S = 5. The heaviest box (27 kg) is at 3 and the lightest (6 kg) at 4. P is four places above the "
       "heaviest: P = 7. K lies between S and P: K = 6. V = 8. F, J, T and Y take positions 1 to 4.\n"
       "Step 2: 9, 11, 14, 17, 20 and 23 kg are left for positions 1, 2, 5, 6, 7 and 8. The two bottom boxes weigh 29 "
       "kg together: only 9 + 20 works, so positions 1 and 2 hold 9 and 20 kg, and S, K, P, V share 11, 14, 17, 23.\n"
       "Step 3: K = S + J, where J is one of the bottom four (9, 20, 27 or 6 kg). The possibilities are 14 + 9 = 23 or "
       "11 + 6 = 17 or 17 + 6 = 23. V = F + P with P lighter than V uses the other two weights: (a) S 14, J 9, K 23 ⇒ "
       "V 17, P 11, F 6; (b) S 11, J 6, K 17 ⇒ V 23, P 14, F 9; (c) S 17, J 6, K 23 ⇒ V 14, P 11, F 3 ✗.\n"
       "Step 4: In (b) J (6 kg) is at 4, so T is at 3 with 27 kg and Y would be lighter than T ✗. So (a): F = 4 (6 "
       "kg); J (9 kg) is in the bottom pair and is immediately above T: T = 1 (20 kg), J = 2, and Y = 3 (27 kg). P (11) "
       "is heavier than J (9) and lighter than V (17), as required.\n\n"
       + table(["Position", "Box", "Weight (kg)"], [(i, at[i], wt[at[i]]) for i in range(8, 0, -1)]), ARR)
ans = max(B, key=wt.get)
assert ans == "Y"
ask("Which box is the heaviest?", "Box " + ans, ["Box T", "Box K", "Box V"], "Eliminate the weight cases one by one",
    "The heaviest box sits at position 3. Of the two cases that fit the sums, the one with T at 3 makes Y lighter "
    "than T, which is not allowed, so Y is at 3 and weighs 27 kg.",
    ["Heaviest at position 3", "Case with T at 3 ⇒ Y lighter than T ✗", "Y = position 3 = 27 kg"],
    why="T weighs 20 kg, K 23 kg and V 17 kg.", sec=90)
c_, w_ = bal(wt["K"], fmt=lambda v: f"{v} kg", step=3, lo=11)
ask("What is the weight of Box K?", c_, w_, "K = S + J",
    "In the only valid case S weighs 14 kg and J 9 kg, so K weighs 14 + 9 = 23 kg.",
    ["Valid case: S 14, J 9", "K = 14 + 9 = 23 kg"], natural=lambda t: int(t.split()[0]), sec=90)
n_ = abs(S["J"] - S["V"]) - 1
assert n_ == 5
c_, w_ = bal(n_)
ask("How many boxes are kept between Box J and Box V?", c_, w_, "Count the positions strictly between",
    "J is at position 2 and V at 8, so positions 3 to 7 lie between them: five boxes.",
    ["J = 2, V = 8", "Between: 3, 4, 5, 6, 7 ⇒ five"], natural=by_num, sec=75)
tot = sum(wt[at[i]] for i in range(S["K"] + 1, 9))
assert tot == 28
c_, w_ = bal(tot, fmt=lambda v: f"{v} kg", step=3, lo=20)
ask("What is the total weight of the boxes kept above Box K?", c_, w_, "Add every box above the given one",
    "K is at position 6; above it are P (11 kg) and V (17 kg): 28 kg.", ["Above K: P (7), V (8)", "11 + 17 = 28 kg"],
    natural=lambda t: int(t.split()[0]), sec=75)
ans = at[S[next(b for b in B if wt[b] == 14)] - 1]
assert ans == "F"
ask("Which box is kept immediately below the box that weighs 14 kg?", "Box " + ans, ["Box Y", "Box K", "Box J"],
    "Find the 14 kg box first", "Box S weighs 14 kg and sits at position 5. Immediately below it, at 4, is Box F, the "
    "lightest box.", ["14 kg = S (position 5)", "Position 4 = F"],
    why="Y is two places below S, K is immediately above S, and J is at position 2.", sec=75)
t, f = one_true([("Box T weighs 20 kg", wt["T"] == 20),
                 ("Box P weighs exactly as much as Box J and Box F together", wt["P"] == wt["J"] + wt["F"]),
                 ("Box V is the second heaviest box", sorted(WT)[-2] == wt["V"]),
                 ("Box T is kept immediately below Box Y", S["T"] == S["Y"] - 1)])
ask("Which of the following statements is true?", t, f, "Checking each statement against the final stack",
    "Box T, at the bottom, weighs 20 kg, so the first statement is true.",
    ["T = 20 kg ✓", "J + F = 9 + 6 = 15 kg, but P = 11 kg ✗", "Second heaviest = 23 kg (K), V = 17 kg ✗",
     "T is at 1 and Y at 3, so J lies between them ✗"],
    why="P is not the sum of J and F, K (not V) is the second heaviest, and J sits between T and Y.", sec=80)


# ################################################################################################ BATCH 008
begin("008")

# ---- 8L1 Basic set (5): eight bank officers in a row facing north, each in a different department
P = ["Anmol", "Bishakha", "Dolly", "Gagandeep", "Hrithik", "Inaaya", "Kirtan", "Mehr"]
DP = ["Accounts", "Audit", "Credit", "Forex", "HR", "IT", "Legal", "Treasury"]
conds = [
    ("Inaaya sits fourth from the left end of the row and works in Credit.", ("Inaaya", "Credit"),
     lambda i, c: i == 4 and c == i),
    ("Bishakha sits second to the right of Inaaya and works in HR.", ("Bishakha", "Inaaya", "HR"),
     lambda b, i, h: b == i + 2 and h == b),
    ("The person who works in Accounts sits immediately to the right of Bishakha.", ("Accounts", "Bishakha"),
     lambda a, b: a == b + 1),
    ("Gagandeep sits at the extreme right end and works in Treasury.", ("Gagandeep", "Treasury"),
     lambda g, t: g == 8 and t == 8),
    ("Dolly sits at an extreme end of the row, and Anmol sits immediately to the left of Inaaya.",
     ("Dolly", "Anmol", "Inaaya"), lambda d, a, i: d in (1, 8) and a == i - 1),
    ("Mehr sits immediately to the left of Bishakha, and Kirtan is not an immediate neighbour of Bishakha.",
     ("Mehr", "Kirtan", "Bishakha"), lambda m, k, b: m == b - 1 and abs(k - b) != 1),
    ("The person who works in IT sits second to the left of the person who works in Accounts.", ("IT", "Accounts"),
     lambda i, a: i == a - 2),
    ("The person in Forex sits immediately to the right of the person in Legal, and Anmol does not work in Forex.",
     ("Forex", "Legal", "Anmol"), lambda f, l, a: f == l + 1 and a != f),
]
S = unique(P + DP, {v: range(1, 9) for v in P + DP}, conds, [P, DP])
at, dep = inv(S, P), inv(S, DP)
dof = {p: dep[S[p]] for p in P}
assert [(at[i], dep[i]) for i in range(1, 9)] == [
    ("Dolly", "Legal"), ("Kirtan", "Forex"), ("Anmol", "Audit"), ("Inaaya", "Credit"), ("Mehr", "IT"),
    ("Bishakha", "HR"), ("Hrithik", "Accounts"), ("Gagandeep", "Treasury")]
ARR = "Left to right: " + ", ".join(f"{at[i]} ({dep[i]})" for i in range(1, 9))
puzzle(LIN, SGL, "Basic", "Eight bank officers in a row, with departments",
       "Eight officers of a bank, Anmol, Bishakha, Dolly, Gagandeep, Hrithik, Inaaya, Kirtan and Mehr, sit in a "
       "straight row, all facing north. Each works in a different department among Accounts, Audit, Credit, Forex, HR, "
       "IT, Legal and Treasury. (Facing north, a person's right is towards the east end of the row.)", conds,
       "Number the seats 1 to 8 from the left (west) end.\n"
       "Step 1: Inaaya = 4 (Credit), Bishakha = 6 (HR), Accounts = 7, Gagandeep = 8 (Treasury).\n"
       "Step 2: Dolly is at an end; seat 8 is taken, so Dolly = 1. Anmol = 3, Mehr = 5.\n"
       "Step 3: Seats 2 and 7 remain for Hrithik and Kirtan. Kirtan cannot sit next to Bishakha (6), so Kirtan = 2 and "
       "Hrithik = 7 (Accounts).\n"
       "Step 4: IT is two seats left of Accounts: seat 5, Mehr. Audit, Forex and Legal remain for seats 1, 2 and 3; "
       "Forex is immediately right of Legal, and Anmol (3) is not in Forex, so Legal = 1 (Dolly), Forex = 2 (Kirtan) "
       "and Audit = 3 (Anmol).\n\n" + table(["Seat", "Person", "Department"], [(i, at[i], dep[i]) for i in range(1, 9)]),
       ARR)
ans = at[S["IT"]]
assert ans == "Mehr"
ask("Who works in IT?", ans, ["Hrithik", "Anmol", "Kirtan"], "Locate a department relative to another",
    "Accounts is at seat 7 (immediately right of Bishakha), so IT is two seats to the left: seat 5, Mehr.",
    ["Accounts = seat 7", "IT = 7 − 2 = seat 5 = Mehr"],
    why="Hrithik works in Accounts, Anmol in Audit and Kirtan in Forex.", sec=40)
ans = dof["Kirtan"]
assert ans == "Forex"
ask("In which department does Kirtan work?", ans, ["Legal", "Audit", "Accounts"],
    "Settle the last three departments with the adjacency clue",
    "Audit, Forex and Legal remain for seats 1, 2 and 3. Forex is immediately right of Legal, so Legal–Forex is 1–2 "
    "or 2–3; Anmol (3) is not in Forex, so Legal = 1 and Forex = 2, Kirtan's seat.",
    ["Free: Audit, Forex, Legal for seats 1–3", "Forex right of Legal; seat 3 ≠ Forex ⇒ Forex = 2 = Kirtan"],
    why="Legal is Dolly's department, Audit Anmol's and Accounts Hrithik's.", sec=45)
n_ = abs(S["Anmol"] - S["Treasury"]) - 1
assert n_ == 4
c_, w_ = bal(n_)
ask("How many persons sit between Anmol and the person who works in Treasury?", c_, w_,
    "Count the seats strictly between", "Anmol is at seat 3 and the Treasury officer (Gagandeep) at seat 8, so seats 4 "
    "to 7 lie between them: four persons.", ["Anmol 3, Treasury = Gagandeep 8", "Between: 4, 5, 6, 7 ⇒ four"],
    natural=by_num, sec=40)
ans = at[S["Kirtan"] + 2]
assert ans == "Inaaya"
ask("Who sits second to the right of Kirtan?", ans, ["Anmol", "Dolly", "Mehr"], "Facing north: the right is east",
    "Kirtan is at seat 2; two seats to the east is seat 4, Inaaya.", ["Kirtan = 2", "2 + 2 = seat 4 ⇒ Inaaya"],
    why="Anmol is immediately to his right, Dolly to his left, and Mehr third to his right.", sec=35)
t, f = one_true([("Hrithik works in Accounts", dof["Hrithik"] == "Accounts"),
                 ("Dolly works in Audit", dof["Dolly"] == "Audit"),
                 ("Mehr sits at an extreme end of the row", S["Mehr"] in (1, 8)),
                 ("Bishakha sits immediately to the right of Inaaya", S["Bishakha"] == S["Inaaya"] + 1)])
ask("Which of the following statements is true?", t, f, "Checking each statement against the arrangement",
    "Hrithik sits at seat 7, immediately right of Bishakha, which is the Accounts seat.",
    ["Hrithik = seat 7 = Accounts ✓", "Dolly works in Legal ✗", "Mehr is at seat 5 ✗",
     "Bishakha is second, not first, to Inaaya's right ✗"], why="Each of the other statements contradicts the table.",
    sec=40)

# ---- 8L2 Intermediate set (4): a north-facing row of unknown length with an interchange (seats from the left end)
V = ["Harshit", "Tejas", "n", "Vrinda", "Yamuna"]
conds = [
    ("Harshit sits tenth from the left end of the row, and Tejas sits somewhere to his right.", ("Harshit", "Tejas"),
     lambda h, t: h == 10 and t > h),
    ("If Harshit and Tejas interchange their seats, Harshit becomes seventeenth from the left end and Tejas becomes "
     "fourteenth from the right end.", ("Harshit", "Tejas", "n"), lambda h, t, n: t == 17 and n - h + 1 == 14),
    ("Vrinda sits exactly in the middle of the row.", ("Vrinda", "n"), lambda v, n: n % 2 == 1 and v == (n + 1) // 2),
    ("Yamuna sits second to the left of the seat that Tejas occupies before the interchange.", ("Yamuna", "Tejas"),
     lambda y, t: y == t - 2),
]
NAMED = [v for v in V if v != "n"]
S = unique(V, {v: range(1, 41) for v in V}, conds, [NAMED], extra=[(("n", *NAMED), lambda n, *xs: max(xs) <= n)])
n_ = S["n"]
assert (n_, S["Tejas"], S["Vrinda"], S["Yamuna"]) == (23, 17, 12, 15)
ARR = (f"From the left end (before the interchange): Harshit 10th, Vrinda 12th, Yamuna 15th, Tejas 17th; {n_} persons "
       f"in all")
puzzle(LIN, UNK, "Intermediate", "A row of unknown length and an interchange",
       "Some persons sit in a straight row, all facing north. The number of persons in the row is not given. Harshit, "
       "Tejas, Vrinda and Yamuna are among them.", conds,
       "Step 1: After the interchange Harshit takes Tejas's seat and becomes 17th from the left, so Tejas sits 17th "
       "from the left.\n"
       "Step 2: Tejas takes Harshit's seat (10th from the left) and becomes 14th from the right, so the row has "
       "10 + 14 − 1 = 23 persons.\n"
       "Step 3: Vrinda is in the middle: (23 + 1) ÷ 2 = 12th from the left. Yamuna is second to the left of 17th: "
       "15th from the left.\n\n"
       + table(["Person", "From the left (before)", "From the right (before)"],
               [(p, ORD(S[p]), ORD(n_ - S[p] + 1)) for p in sorted(NAMED, key=lambda x: S[x])]), ARR)
c_, w_ = bal(n_, fmt=str, lo=20)
ask("How many persons sit in the row?", c_, w_, "An interchange swaps the two seats, not the counts",
    "Tejas, in Harshit's seat (10th from the left), is 14th from the right: 10 + 14 − 1 = 23.",
    ["Harshit's seat: 10th from the left = 14th from the right", "Total = 10 + 14 − 1 = 23"], natural=int, sec=60)
n2 = S["Tejas"] - S["Harshit"] - 1
assert n2 == 6
c_, w_ = bal(n2)
ask("How many persons sit between Harshit and Tejas?", c_, w_, "Persons between = difference of positions − 1",
    "Harshit is 10th and Tejas 17th from the left: 17 − 10 − 1 = 6 persons sit between them.",
    ["Harshit 10th, Tejas 17th (from the left)", "17 − 10 − 1 = 6"], natural=by_num, sec=50)
ans = n_ - S["Vrinda"] + 1
assert ans == 12
c_, w_ = bal(ans, fmt=ORD, lo=1)
ask("What is Vrinda's position from the right end of the row?", c_, w_, "The middle seat is the same from both ends",
    "With 23 persons, the middle seat is 12th from either end, so Vrinda is 12th from the right.",
    ["n = 23 (odd) ⇒ middle = 12th", "12th from both ends"], natural=ordn, sec=45)
n3 = abs(S["Tejas"] - S["Yamuna"]) - 1
assert n3 == 1
c_, w_ = bal(n3)
ask("After the interchange, how many persons sit between Harshit and Yamuna?", c_, w_,
    "After the interchange Harshit sits in Tejas's old seat",
    "After the interchange Harshit is 17th from the left and Yamuna is 15th, so only the 16th person sits between "
    "them.", ["Harshit (after) = 17th", "Yamuna = 15th", "Between: the 16th ⇒ one"], natural=by_num, sec=50)

# ---- 8L3 Advanced set (6): nine persons in three teams, all facing north; no two team-mates sit side by side
P = ["Aaradhya", "Bodhi", "Chinmayi", "Divit", "Eshna", "Falguni", "Hridya", "Ivaan", "Jaanvi"]
T = ["t" + p for p in P]
TN = {"R": "Red", "B": "Blue", "G": "Green"}
conds = [
    ("Jaanvi sits exactly in the middle of the row, and Falguni sits immediately to her left.",
     ("Jaanvi", "Falguni"), lambda j, f: j == 5 and f == 4),
    ("Ivaan sits third to the right of Falguni, and they are in the same team.",
     ("Ivaan", "Falguni", "tIvaan", "tFalguni"), lambda i, f, ti, tf: i == f + 3 and ti == tf),
    ("Divit sits at the extreme left end, and Eshna sits at the extreme right end.", ("Divit", "Eshna"),
     lambda d, e: d == 1 and e == 9),
    ("Aaradhya sits third to the left of Eshna, and Chinmayi sits immediately to the left of Eshna.",
     ("Aaradhya", "Chinmayi", "Eshna"), lambda a, c, e: a == e - 3 and c == e - 1),
    ("Hridya sits to the left of Bodhi.", ("Hridya", "Bodhi"), lambda h, b: h < b),
    ("No two members of the same team sit next to each other.", (*P, *T),
     lambda *x: all(x[9 + x[:9].index(s)] != x[9 + x[:9].index(s + 1)] for s in range(1, 9))),
    ("Divit is in the Red team, and Aaradhya is in the Blue team.", ("tDivit", "tAaradhya"),
     lambda d, a: d == "R" and a == "B"),
    ("Jaanvi and Chinmayi are in the same team, and so are Hridya and Eshna.",
     ("tJaanvi", "tChinmayi", "tHridya", "tEshna"), lambda j, c, h, e: j == c and h == e),
]
V = ["Jaanvi", "Falguni", "Ivaan", "Divit", "Eshna", "Aaradhya", "Chinmayi", "Hridya", "Bodhi"] + T
S = unique(V, {p: range(1, 10) for p in P} | {t: "RBG" for t in T}, conds, [P],
           extra=[(tuple(T), lambda *ts: all(ts.count(c) == 3 for c in "RBG"))])
at = inv(S, P)
tm = {p: S["t" + p] for p in P}
assert [(at[i], tm[at[i]]) for i in range(1, 10)] == [
    ("Divit", "R"), ("Hridya", "B"), ("Bodhi", "G"), ("Falguni", "R"), ("Jaanvi", "G"), ("Aaradhya", "B"),
    ("Ivaan", "R"), ("Chinmayi", "G"), ("Eshna", "B")]
ARR = "Left to right: " + ", ".join(f"{at[i]} ({TN[tm[at[i]]]})" for i in range(1, 10))
puzzle(LIN, SGL, "Advanced", "Nine persons from three teams in one row",
       "Nine persons Aaradhya, Bodhi, Chinmayi, Divit, Eshna, Falguni, Hridya, Ivaan and Jaanvi sit in a straight row, "
       "all facing north. Each belongs to one of three teams, Red, Blue and Green, and each team has exactly three "
       "members among them. (Facing north, the right is towards the east.)", conds,
       "Number the seats 1 to 9 from the left end.\n"
       "Step 1: Jaanvi = 5, Falguni = 4, Ivaan = 7, Divit = 1, Eshna = 9, Aaradhya = 6, Chinmayi = 8.\n"
       "Step 2: Seats 2 and 3 remain for Hridya and Bodhi; Hridya is to the left: Hridya = 2, Bodhi = 3.\n"
       "Step 3: Divit is Red and Aaradhya Blue. Jaanvi (5) and Ivaan (7) both sit next to Aaradhya, so neither is "
       "Blue, and so their team-mates Chinmayi and Falguni are not Blue either. Falguni sits next to Jaanvi, so the "
       "pair Falguni–Ivaan and the pair Jaanvi–Chinmayi take Red and Green in some order.\n"
       "Step 4: If Falguni and Ivaan were Green, Jaanvi, Chinmayi and Divit would fill Red; Hridya and Eshna could "
       "not both join Green (it would have four), so they would be Blue and Bodhi Green — but Bodhi (3) sits next to "
       "Falguni (4) ✗. So Falguni and Ivaan are Red (Red is now full) and Jaanvi and Chinmayi are Green.\n"
       "Step 5: Hridya and Eshna share a team; Red is full and Green has room for only one more, so both are Blue "
       "with Aaradhya, and Bodhi is the third Green member. No two neighbours share a team.\n\n"
       + table(["Seat", "Person", "Team"], [(i, at[i], TN[tm[at[i]]]) for i in range(1, 10)]), ARR)
ans = TN[tm["Bodhi"]]
assert ans == "Green"
ask("Which team does Bodhi belong to?", ans, ["Red", "Blue", "Cannot be determined"],
    "Count team sizes after fixing the forced memberships",
    "Red is Divit, Falguni and Ivaan; Blue is Aaradhya, Hridya and Eshna; so Bodhi completes Green with Jaanvi and "
    "Chinmayi.", ["Red: Divit, Falguni, Ivaan (full)", "Blue: Aaradhya + Hridya, Eshna (full)", "Bodhi ⇒ Green"],
    why="Red and Blue already have three members each, and every team is fixed, so the team can be determined.",
    sec=80)
ans = at[S["Hridya"] + 2]
assert ans == "Falguni"
ask("Who sits second to the right of Hridya?", ans, ["Bodhi", "Jaanvi", "Divit"], "Facing north: the right is east",
    "Hridya is at seat 2; two seats to the east is seat 4, Falguni.", ["Hridya = 2", "2 + 2 = 4 ⇒ Falguni"],
    why="Bodhi is immediately to her right, Jaanvi third to her right, and Divit to her left.", sec=60)
n_ = sum(1 for p in P if tm[p] == "B" and S[p] > S["Jaanvi"])
assert n_ == 2
c_, w_ = bal(n_)
ask("How many members of the Blue team sit to the right of Jaanvi?", c_, w_, "Read team and position together",
    "Blue members: Hridya (2), Aaradhya (6) and Eshna (9). Jaanvi is at seat 5, so Aaradhya and Eshna sit to her "
    "right.", ["Blue: Hridya 2, Aaradhya 6, Eshna 9", "Right of seat 5: 6 and 9 ⇒ two"], natural=by_num, sec=70)
gg = [p for p in P if 1 < S[p] < 9 and tm[at[S[p] - 1]] == "G" and tm[at[S[p] + 1]] == "G"]
assert gg == ["Falguni"]
ask("Who among the following sits between two members of the Green team?", "Falguni",
    ["Aaradhya", "Hridya", "Ivaan"], "Check both neighbours' teams",
    "Falguni (seat 4) has Bodhi (3, Green) and Jaanvi (5, Green) on either side.",
    ["Falguni: neighbours Bodhi (Green) and Jaanvi (Green) ✓", "Aaradhya: Jaanvi (Green), Ivaan (Red) ✗",
     "Hridya: Divit (Red), Bodhi (Green) ✗", "Ivaan: Aaradhya (Blue), Chinmayi (Green) ✗"],
    why="Each of the others has at least one neighbour who is not in the Green team.", sec=70)
ans = at[S["Chinmayi"] - 3]
assert ans == "Jaanvi"
ask("Who sits third to the left of Chinmayi?", ans, ["Aaradhya", "Falguni", "Ivaan"], "Facing north: the left is west",
    "Chinmayi is at seat 8; three seats to the west is seat 5, Jaanvi.", ["Chinmayi = 8", "8 − 3 = 5 ⇒ Jaanvi"],
    why="Aaradhya is second, Ivaan first and Falguni fourth to her left.", sec=60)
t, f = one_true([("Hridya and Eshna are in the Blue team", tm["Hridya"] == tm["Eshna"] == "B"),
                 ("Bodhi and Ivaan are in the same team", tm["Bodhi"] == tm["Ivaan"]),
                 ("Exactly three Red team members sit to the left of Jaanvi", sum(
                     1 for p in P if tm[p] == "R" and S[p] < S["Jaanvi"]) == 3),
                 ("Chinmayi is in the Blue team", tm["Chinmayi"] == "B")])
ask("Which of the following statements is true?", t, f, "Checking each statement against the teams",
    "Blue is Aaradhya, Hridya and Eshna, so the first statement is true.",
    ["Hridya, Eshna: Blue ✓", "Bodhi Green, Ivaan Red ✗",
     "Red members left of Jaanvi: Divit and Falguni only (Ivaan is to her right) ✗", "Chinmayi is Green ✗"],
    why="Bodhi and Ivaan are in different teams, only two Red members sit left of Jaanvi, and Chinmayi is Green.",
    sec=70)


# ---- 8C1 Basic set (6): seven persons facing the centre, each likes a different cuisine (Ayaan fixed at seat 0)
P = ["Ayaan", "Gunika", "Madhur", "Parul", "Rehaan", "Sarika", "Tanvir"]
CU = ["Bengali", "Chinese", "Gujarati", "Italian", "Mexican", "Punjabi", "Thai"]
R7 = lambda s, k: (s + k) % 7
conds = [
    ("Parul sits immediately to the right of Ayaan, and Gunika sits third to the right of Ayaan.",
     ("Parul", "Gunika", "Ayaan"), lambda p, g, a: p == R7(a, 1) and g == R7(a, 3)),
    ("Madhur sits second to the left of Ayaan.", ("Madhur", "Ayaan"), lambda m, a: m == R7(a, -2)),
    ("Tanvir sits immediately between Parul and Gunika.", ("Tanvir", "Parul", "Gunika"),
     lambda t, p, g: {R7(t, 1), R7(t, -1)} == {p, g}),
    ("Rehaan is an immediate neighbour of Ayaan.", ("Rehaan", "Ayaan"), lambda r, a: r in (R7(a, 1), R7(a, -1))),
    ("Ayaan likes Punjabi food, and the person who likes Thai food sits immediately to his right.",
     ("Ayaan", "Punjabi", "Thai"), lambda a, p, t: p == a and t == R7(a, 1)),
    ("Gunika likes Bengali food, and the person who likes Chinese food sits immediately to her right.",
     ("Gunika", "Bengali", "Chinese"), lambda g, b, c: b == g and c == R7(g, 1)),
    ("The person who likes Mexican food sits immediately to the left of Ayaan.", ("Mexican", "Ayaan"),
     lambda m, a: m == R7(a, -1)),
    ("Madhur does not like Italian food.", ("Madhur", "Italian"), lambda m, i: m != i),
]
S = unique(P + CU, {"Ayaan": [0]} | {v: range(7) for v in P[1:] + CU}, conds, [P, CU])
at, cui = inv(S, P), inv(S, CU)
cof = {p: cui[S[p]] for p in P}
assert [(at[i], cui[i]) for i in range(7)] == [
    ("Ayaan", "Punjabi"), ("Parul", "Thai"), ("Tanvir", "Italian"), ("Gunika", "Bengali"), ("Sarika", "Chinese"),
    ("Madhur", "Gujarati"), ("Rehaan", "Mexican")]
ARR = "Anticlockwise from Ayaan (each person's right is the next seat anticlockwise): " + ", ".join(
    f"{at[i]} ({cui[i]})" for i in range(7))
puzzle(CIR, CEN, "Basic", "Seven persons around a round table, with favourite cuisines",
       "Seven persons Ayaan, Gunika, Madhur, Parul, Rehaan, Sarika and Tanvir sit around a circular table, equally "
       "spaced and all facing the centre. Each likes a different cuisine among Bengali, Chinese, Gujarati, Italian, "
       "Mexican, Punjabi and Thai. (Facing the centre, a person's right is anticlockwise and the left is clockwise.)",
       conds,
       "Number the seats 0 to 6 anticlockwise starting from Ayaan.\n"
       "Step 1: Parul = 1 and Gunika = 3 (right = anticlockwise). Madhur is second to Ayaan's left (clockwise): 5.\n"
       "Step 2: Tanvir sits between Parul (1) and Gunika (3): seat 2. Rehaan is next to Ayaan: seat 6 (seat 1 is "
       "Parul's). Sarika takes seat 4.\n"
       "Step 3: Ayaan likes Punjabi; Thai is on his right: Parul. Gunika likes Bengali; Chinese is on her right: "
       "Sarika (4). Mexican is on Ayaan's left: Rehaan (6).\n"
       "Step 4: Gujarati and Italian remain for Tanvir and Madhur; Madhur does not like Italian, so Madhur likes "
       "Gujarati and Tanvir Italian.\n\n" + table(["Seat (anticlockwise)", "Person", "Cuisine"],
                                                   [(i, at[i], cui[i]) for i in range(7)]), ARR)
ans = at[S["Chinese"]]
assert ans == "Sarika"
ask("Who likes Chinese food?", ans, ["Tanvir", "Madhur", "Rehaan"], "An attribute placed beside a fixed person",
    "Gunika sits at seat 3; the person immediately to her right (anticlockwise) is at seat 4: Sarika.",
    ["Gunika = seat 3", "Her right = seat 4 = Sarika ⇒ Chinese"],
    why="Tanvir likes Italian, Madhur Gujarati and Rehaan Mexican.", sec=40)
ans = at[R7(S["Tanvir"], -3)]
assert ans == "Rehaan"
ask("Who sits third to the left of Tanvir?", ans, ["Madhur", "Ayaan", "Sarika"], "Facing the centre: left = clockwise",
    "Tanvir is at seat 2. Moving clockwise: seat 1 (Parul), seat 0 (Ayaan), seat 6 (Rehaan).",
    ["Tanvir = seat 2", "Clockwise 3 seats: 1, 0, 6 ⇒ Rehaan"],
    why="Ayaan is second to his left, Sarika second to his right, and Madhur third to his right.", sec=45)
ans = cof["Madhur"]
assert ans == "Gujarati"
ask("Which cuisine does Madhur like?", ans, ["Italian", "Mexican", "Thai"], "The last pair by a negative clue",
    "Gujarati and Italian are the two cuisines left for Tanvir and Madhur, and Madhur does not like Italian.",
    ["Left: Gujarati, Italian for Tanvir and Madhur", "Madhur ≠ Italian ⇒ Gujarati"],
    why="Italian is Tanvir's, Mexican Rehaan's and Thai Parul's cuisine.", sec=40)
n_ = (S["Sarika"] - S["Ayaan"]) % 7 - 1
assert n_ == 3
c_, w_ = bal(n_)
ask("How many persons sit between Ayaan and Sarika when counted from Ayaan's right?", c_, w_,
    "Counting from a person's right means going anticlockwise when facing the centre",
    "From Ayaan (0) anticlockwise: Parul (1), Tanvir (2), Gunika (3), then Sarika (4). Three persons sit between.",
    ["Ayaan 0 → Sarika 4 anticlockwise", "Between: seats 1, 2, 3 ⇒ three"], natural=by_num, sec=45)
it = at[S["Italian"]]
nb = {at[R7(S[it], 1)], at[R7(S[it], -1)]}
assert nb == {"Parul", "Gunika"}
ask("Who are the immediate neighbours of the person who likes Italian food?", "Parul and Gunika",
    ["Ayaan and Parul", "Gunika and Sarika", "Madhur and Rehaan"], "Find the person first, then both neighbours",
    "Tanvir likes Italian and sits at seat 2, between Parul (1) and Gunika (3).",
    ["Italian = Tanvir = seat 2", "Neighbours: seats 1 and 3 ⇒ Parul and Gunika"],
    why="Ayaan sits next to Parul but not next to Tanvir; Sarika is Gunika's other neighbour; Madhur and Rehaan sit "
        "across the table.", sec=45)
t, f = one_true([("Sarika sits second to the left of Rehaan", S["Sarika"] == R7(S["Rehaan"], -2)),
                 ("Parul likes Italian food", cof["Parul"] == "Italian"),
                 ("Madhur sits immediately to the right of Gunika", S["Madhur"] == R7(S["Gunika"], 1)),
                 ("Ayaan sits immediately between Rehaan and Madhur", {R7(0, 1), R7(0, -1)} == {S["Rehaan"], S["Madhur"]})])
ask("Which of the following statements is true?", t, f, "Checking each statement against the arrangement",
    "Rehaan is at seat 6; his left is clockwise: seat 5 (Madhur), then seat 4 (Sarika). So Sarika is second to his "
    "left.", ["Rehaan 6 ⇒ clockwise 5, 4 ⇒ Sarika ✓", "Parul likes Thai ✗",
              "Gunika's right (seat 4) is Sarika, not Madhur ✗", "Ayaan's neighbours are Rehaan and Parul ✗"],
    why="Parul likes Thai, Sarika is on Gunika's right, and Ayaan sits between Rehaan and Parul.", sec=50)


# ---- 8C2 Intermediate set (4): rectangular table, three seats along each longer side and one at each shorter side.
#      Seats 0..7 anticlockwise: 0 and 4 = shorter sides; 1–3 and 5–7 = longer sides, seat s facing seat 8 − s.
#      The middle seat of each longer side (2 and 6) faces outside; everyone else faces the centre.
P = ["Kshitij", "Mahua", "Nikunj", "Prerak", "Rumi", "Sudhir", "Tvisha", "Urmila"]
rf = lambda s: "O" if s in (2, 6) else "C"
opp8 = lambda s: 8 - s
conds = [
    ("Kshitij and Prerak sit at the two shorter sides of the table.", ("Prerak",), lambda p: p == 4),
    ("Rumi sits immediately to the right of Kshitij.", ("Rumi", "Kshitij"), lambda r, k: r == CR(k, rf(k), 1, 8)),
    ("Mahua sits second to the right of Prerak.", ("Mahua", "Prerak"), lambda m, p: m == CR(p, rf(p), 2, 8)),
    ("Urmila sits directly opposite Mahua.", ("Urmila", "Mahua"), lambda u, m: u == opp8(m)),
    ("Nikunj sits immediately to the left of Urmila.", ("Nikunj", "Urmila"), lambda n, u: n == CR(u, rf(u), -1, 8)),
    ("Sudhir does not sit next to Prerak.", ("Sudhir", "Prerak"), lambda s, p: abs(s - p) not in (1, 7)),
]
S = unique(P, {"Kshitij": [0]} | {p: range(8) for p in P[1:]}, conds, [P])
at = inv(S, P)
assert [at[i] for i in range(8)] == ["Kshitij", "Rumi", "Urmila", "Nikunj", "Prerak", "Tvisha", "Mahua", "Sudhir"]
SEATN = {0: "shorter side, facing the centre", 4: "shorter side, facing the centre",
         2: "middle of a longer side, facing outside", 6: "middle of a longer side, facing outside"}
SN = lambda i: SEATN.get(i, "longer side, facing the centre")
ARR = "Anticlockwise from Kshitij: " + ", ".join(f"{at[i]} ({SN(i)})" for i in range(8))
puzzle(CIR, SQR, "Intermediate", "Rectangular table: middle seats of the longer sides face outside",
       "Eight persons Kshitij, Mahua, Nikunj, Prerak, Rumi, Sudhir, Tvisha and Urmila sit around a rectangular table. "
       "Three persons sit along each longer side and one person at each shorter side. The person in the middle seat of "
       "each longer side faces away from the centre; the other six face the centre. Each person on a longer side sits "
       "directly opposite a person on the other longer side. (Facing the centre, the right is anticlockwise; facing "
       "outside, it is clockwise.)", conds,
       "Number the seats 0 to 7 anticlockwise, starting with Kshitij at one shorter side; Prerak is at the other "
       "shorter side, seat 4. Seats 1–3 and 5–7 are the longer sides (2 and 6 are their middle seats, facing outside), "
       "and seat s faces seat 8 − s.\n"
       "Step 1: Kshitij faces the centre, so his right is anticlockwise: Rumi = 1.\n"
       "Step 2: Prerak also faces the centre: Mahua = 4 + 2 = 6 (a middle seat, facing outside). Urmila is opposite "
       "Mahua: seat 2, also facing outside.\n"
       "Step 3: Urmila faces outside, so her left is anticlockwise: Nikunj = 3.\n"
       "Step 4: Seats 5 and 7 remain for Sudhir and Tvisha; seat 5 is next to Prerak, so Sudhir = 7, Tvisha = 5.\n\n"
       + table(["Seat", "Person", "Position"], [(i, at[i], SN(i)) for i in range(8)]), ARR)
ans = at[opp8(S["Nikunj"])]
assert ans == "Tvisha"
ask("Who sits directly opposite Nikunj?", ans, ["Mahua", "Sudhir", "Prerak"], "Pair the seats across the longer sides",
    "Nikunj is at seat 3, which faces seat 5: Tvisha.", ["Nikunj = 3", "Opposite = 8 − 3 = 5 ⇒ Tvisha"],
    why="Mahua faces Urmila, Sudhir faces Rumi, and Prerak sits at a shorter side.", sec=55)
ans = at[CR(S["Prerak"], "C", -3, 8)]
assert ans == "Rumi"
ask("Who sits third to the left of Prerak?", ans, ["Tvisha", "Mahua", "Urmila"],
    "Prerak faces the centre, so his left is clockwise",
    "Prerak (seat 4) faces the centre; clockwise: seat 3 (Nikunj), seat 2 (Urmila), seat 1 (Rumi).",
    ["Prerak faces the centre ⇒ left = clockwise", "4 → 3 → 2 → 1 ⇒ Rumi"],
    why="Tvisha and Mahua are to his right; Urmila is second to his left.", sec=55)
ans = at[CR(S["Kshitij"], "C", -1, 8)]
assert ans == "Sudhir"
ask("Who sits immediately to the left of Kshitij?", ans, ["Rumi", "Tvisha", "Urmila"],
    "Facing the centre: left = clockwise", "Kshitij faces the centre, so his left is clockwise: seat 7, Sudhir.",
    ["Kshitij (0) faces the centre ⇒ left = clockwise", "Seat 7 = Sudhir"],
    why="Rumi is immediately to his right; Tvisha and Urmila are not his neighbours.", sec=50)
n_ = (S["Mahua"] - S["Rumi"]) % 8 - 1
assert n_ == 4
c_, w_ = bal(n_)
ask("How many persons sit between Rumi and Mahua, counting from Rumi's right?", c_, w_,
    "Rumi faces the centre, so her right is anticlockwise",
    "From Rumi (1) anticlockwise: Urmila (2), Nikunj (3), Prerak (4), Tvisha (5), then Mahua (6). Four persons sit "
    "between them.", ["Rumi faces the centre ⇒ count anticlockwise", "Seats 2, 3, 4, 5 ⇒ four"], natural=by_num,
    sec=55)

# ---- 8C3 Intermediate set (4): two concentric tables — three persons at the inner table facing outside, six at the
#      outer table facing the centre. Outer seats o0..o5 anticlockwise; inner seats at the angles of o0, o2, o4, so the
#      inner person at angle k faces the outer person at o_k. Positions are angles 0..5 (inner: 0, 2, 4).
INNER, OUTER = ["Abeer", "Kajol", "Navin"], ["Deeksha", "Faiyaz", "Hamsini", "Ishant", "Lakshit", "Ojal"]
conds = [
    ("Abeer, Kajol and Navin sit at the inner table; Abeer faces Hamsini.", ("Hamsini", "Abeer"),
     lambda h, a: h == a),
    ("Kajol sits immediately to the left of Abeer.", ("Kajol", "Abeer"), lambda k, a: k == (a + 2) % 6),
    ("Faiyaz faces Kajol, and Deeksha sits immediately to the right of Faiyaz.", ("Faiyaz", "Kajol", "Deeksha"),
     lambda f, k, d: f == k and d == (f + 1) % 6),
    ("Ishant sits immediately to the left of Hamsini.", ("Ishant", "Hamsini"), lambda i, h: i == (h - 1) % 6),
    ("Lakshit sits second to the right of Faiyaz.", ("Lakshit", "Faiyaz"), lambda l, f: l == (f + 2) % 6),
]
dom = {"Abeer": [0], "Kajol": [2, 4], "Navin": [2, 4]} | {o: range(6) for o in OUTER}
S = unique(["Abeer", "Kajol", "Navin", *OUTER], dom, conds, [INNER, OUTER])
inn, out = inv(S, INNER), inv(S, OUTER)
assert [inn[k] for k in (0, 2, 4)] == ["Abeer", "Kajol", "Navin"]
assert [out[k] for k in range(6)] == ["Hamsini", "Ojal", "Faiyaz", "Deeksha", "Lakshit", "Ishant"]
ARR = ("Outer table, anticlockwise: " + ", ".join(out[k] for k in range(6)) + "; inner table: Abeer faces Hamsini, "
       "Kajol faces Faiyaz, Navin faces Lakshit")
puzzle(CIR, INOUT, "Intermediate", "Three at an inner table, six at an outer table",
       "Nine persons sit around two concentric circular tables. Three of them sit at the smaller inner table, equally "
       "spaced and facing outside; the other six sit at the outer table, equally spaced and facing the centre. Each "
       "person at the inner table directly faces one person at the outer table, and between any two such outer persons "
       "there is exactly one other outer person. The nine persons are Abeer, Deeksha, Faiyaz, Hamsini, Ishant, Kajol, "
       "Lakshit, Navin and Ojal. (Facing the centre, the right is anticlockwise; facing outside, it is clockwise.)",
       conds,
       "Number the outer seats 0 to 5 anticlockwise from Hamsini, the person Abeer faces. The inner persons face outer "
       "seats 0, 2 and 4.\n"
       "Step 1: Abeer faces outside, so his left is anticlockwise: Kajol is at the next inner seat anticlockwise and "
       "faces outer seat 2. Navin faces outer seat 4.\n"
       "Step 2: Faiyaz faces Kajol: outer seat 2. Deeksha, to Faiyaz's right (anticlockwise): 3. Lakshit, second to "
       "Faiyaz's right: 4, so Lakshit faces Navin.\n"
       "Step 3: Ishant is to Hamsini's left (clockwise): seat 5. Ojal takes seat 1.\n\n"
       + table(["Outer seat", "Outer person", "Faced by (inner)"],
               [(k, out[k], inn.get(k, "–")) for k in range(6)]), ARR)
ans = out[(S["Ojal"] + 1) % 6]
assert ans == "Faiyaz"
ask("Who sits immediately to the right of Ojal?", ans, ["Hamsini", "Deeksha", "Kajol"],
    "Outer persons face the centre: right = anticlockwise",
    "Ojal is at outer seat 1; the next seat anticlockwise, seat 2, is Faiyaz's.",
    ["Ojal = outer 1", "Right (anticlockwise) = outer 2 = Faiyaz"],
    why="Hamsini is to Ojal's left; Deeksha is second to Ojal's right; Kajol sits at the inner table.", sec=55)
mid = out[1]
assert mid == "Ojal"
ask("Who sits at the outer table between the two persons who face Abeer and Kajol?", mid,
    ["Ishant", "Deeksha", "Lakshit"], "The outer persons facing inner persons are one seat apart",
    "Hamsini (outer 0) faces Abeer and Faiyaz (outer 2) faces Kajol; the outer seat between them, seat 1, is Ojal's.",
    ["Abeer ↔ Hamsini (0), Kajol ↔ Faiyaz (2)", "Between 0 and 2 ⇒ outer 1 = Ojal"],
    why="Ishant sits beside Hamsini on the other side; Deeksha and Lakshit sit beyond Faiyaz.", sec=55)
ans = out[(S["Lakshit"] + 2) % 6]
assert ans == "Hamsini"
ask("Who sits second to the right of Lakshit?", ans, ["Deeksha", "Ojal", "Faiyaz"],
    "Count anticlockwise at the outer table", "Lakshit is at outer seat 4; moving anticlockwise: Ishant (5), Hamsini "
    "(0).", ["Lakshit = outer 4", "4 → 5 → 0 ⇒ Hamsini"],
    why="Deeksha is immediately to his left, Ojal third to his right and Faiyaz second to his left.", sec=55)
ans = inn[(S["Navin"] - 2) % 6]
assert ans == "Kajol"
ask("Who sits immediately to the right of Navin?", ans, ["Abeer", "Lakshit", "Deeksha"],
    "Inner persons face outside: right = clockwise",
    "Navin faces outside, so his right is clockwise. The next inner seat clockwise from Navin's (the one facing outer "
    "seat 4) is the one facing outer seat 2: Kajol.",
    ["Navin faces outer 4, Kajol outer 2, Abeer outer 0", "Clockwise from Navin ⇒ Kajol"],
    why="Abeer is immediately to Navin's left; Lakshit is the outer person Navin faces; Deeksha is at the outer table.",
    sec=60)

# ---- 8CA1 Advanced (standalone): eight persons facing the centre, with interchanges (Basant fixed at seat 0)
P = ["Basant", "Charmi", "Girik", "Himanshi", "Jeet", "Kumkum", "Mayur", "Noyonika"]
R8 = lambda s, k: (s + k) % 8
conds = [
    ("Girik sits opposite Basant, and Charmi sits second to the right of Basant.", ("Girik", "Charmi"),
     lambda g, c: g == 4 and c == 2),
    ("Himanshi sits second to the right of Girik.", ("Himanshi", "Girik"), lambda h, g: h == R8(g, 2)),
    ("If Charmi and Himanshi interchange their seats, Himanshi will sit immediately to the left of Jeet.",
     ("Jeet", "Charmi"), lambda j, c: c == R8(j, -1)),
    ("If Mayur and Kumkum interchange their seats, Kumkum will sit immediately to the right of Basant.",
     ("Mayur",), lambda m: m == 1),
    ("Noyonika does not sit next to Basant.", ("Noyonika",), lambda n: n not in (1, 7)),
]
S = unique(P, {"Basant": [0]} | {p: range(8) for p in P[1:]}, conds, [P])
at = inv(S, P)
assert [at[i] for i in range(8)] == ["Basant", "Mayur", "Charmi", "Jeet", "Girik", "Noyonika", "Himanshi", "Kumkum"]
ans = at[R8(S["Jeet"], -3)]
assert ans == "Basant"
alone(CIR, CEN, "Advanced",
      "Eight persons Basant, Charmi, Girik, Himanshi, Jeet, Kumkum, Mayur and Noyonika sit around a circular table, "
      "equally spaced and all facing the centre. (Facing the centre, the right is anticlockwise.) The statements about "
      "interchanges describe what would happen; nobody actually moves.", conds,
      "In the actual arrangement, who sits third to the left of Jeet?", ans, ["Kumkum", "Mayur", "Noyonika"],
      "A hypothetical interchange tells you where the moved person's new seat is",
      "Seats 0 to 7 anticlockwise from Basant: Girik 4, Charmi 2, Himanshi 6. After a Charmi–Himanshi swap Himanshi "
      "would be at seat 2, immediately left of Jeet, so Jeet = 3. After a Mayur–Kumkum swap Kumkum would be at "
      "Basant's right (seat 1), so Mayur = 1. Noyonika is not next to Basant: 5, and Kumkum = 7. Third to Jeet's left "
      "(clockwise from 3) is seat 0: Basant.",
      ["Girik 4, Charmi 2, Himanshi 6", "Swap 1: Himanshi would take seat 2 = Jeet's left ⇒ Jeet = 3",
       "Swap 2: Kumkum would take Mayur's seat = Basant's right ⇒ Mayur = 1",
       "Noyonika ∉ {1, 7} ⇒ Noyonika 5, Kumkum 7", "Jeet 3 ⇒ clockwise 2, 1, 0 ⇒ Basant"],
      why="Kumkum is fourth to Jeet's left, Mayur second to his left, and Noyonika second to his right.", sec=120)

# ---- 8CA2 Advanced (standalone): four pairs of twins, each pair sitting directly opposite (Akash fixed at seat 0)
P = ["Akash", "Chandana", "Hiralal", "Ilavati", "Kaustubh", "Moushumi", "Rakesh", "Swati"]
conds = [
    ("Ilavati sits immediately to the right of Akash, and Rakesh sits second to the right of Akash.",
     ("Ilavati", "Rakesh"), lambda i, r: i == 1 and r == 2),
    ("Hiralal sits immediately to the left of Akash, and Moushumi sits third to the right of Akash.",
     ("Hiralal", "Moushumi"), lambda h, m: h == 7 and m == 3),
    ("Kaustubh is not Rakesh's twin.", ("Kaustubh", "Rakesh"), lambda k, r: k != R8(r, 4)),
    ("Chandana sits immediately to the right of Swati.", ("Chandana", "Swati"), lambda c, s: c == R8(s, 1)),
]
S = unique(P, {"Akash": [0]} | {p: range(8) for p in P[1:]}, conds, [P])
at = inv(S, P)
assert [at[i] for i in range(8)] == ["Akash", "Ilavati", "Rakesh", "Moushumi", "Kaustubh", "Swati", "Chandana",
                                     "Hiralal"]
ans = at[R8(S["Ilavati"], 4)]
assert ans == "Swati"
alone(CIR, CEN, "Advanced",
      "Eight persons Akash, Chandana, Hiralal, Ilavati, Kaustubh, Moushumi, Rakesh and Swati sit around a circular "
      "table, equally spaced and all facing the centre. They are four pairs of twins, and each person sits directly "
      "opposite his or her twin. (Facing the centre, the right is anticlockwise.)", conds,
      "Who is Ilavati's twin?", ans, ["Chandana", "Kaustubh", "Moushumi"],
      "Twins sit opposite, so a person's seat fixes the twin's seat",
      "Seats 0 to 7 anticlockwise from Akash: Ilavati 1, Rakesh 2, Moushumi 3, Hiralal 7. Kaustubh, Swati and "
      "Chandana take 4, 5 and 6. Seat 6 is opposite Rakesh, and Kaustubh is not Rakesh's twin, so Kaustubh is at 4 or "
      "5; Chandana is immediately right (anticlockwise) of Swati, which needs two adjacent free seats: with Kaustubh "
      "at 4, Swati = 5 and Chandana = 6; with Kaustubh at 5 no pair is left. Ilavati (1) is opposite seat 5: Swati.",
      ["Fixed: Akash 0, Ilavati 1, Rakesh 2, Moushumi 3, Hiralal 7",
       "Free 4, 5, 6; Rakesh's twin sits at 6 ⇒ Kaustubh ≠ 6",
       "Swati–Chandana need adjacent seats (Chandana anticlockwise of Swati) ⇒ Swati 5, Chandana 6, Kaustubh 4",
       "Ilavati (1) ↔ seat 5 ⇒ Swati"],
      why="Chandana is Rakesh's twin, Kaustubh is Akash's and Moushumi is Hiralal's.", sec=110)


# ---- 8F1 Basic set (3): five floors, each person owns a different vehicle
P = ["Amrit", "Dimpy", "Hari", "Kanak", "Sohan"]
VH = ["Bicycle", "Bike", "Car", "Scooter", "Van"]
conds = [
    ("Sohan lives exactly in the middle floor of the building and owns the Car.", ("Sohan", "Car"),
     lambda s, c: s == 3 and c == 3),
    ("Amrit lives immediately above Sohan, and Kanak lives somewhere above Amrit.", ("Amrit", "Kanak", "Sohan"),
     lambda a, k, s: a == s + 1 and k > a),
    ("Dimpy lives on an even-numbered floor.", ("Dimpy",), lambda d: d % 2 == 0),
    ("The person who owns the Van lives on the lowermost floor.", ("Van",), lambda v: v == 1),
    ("The person who owns the Scooter lives immediately above the person who owns the Bicycle.",
     ("Scooter", "Bicycle"), lambda s, b: s == b + 1),
]
S = unique(P + VH, {v: range(1, 6) for v in P + VH}, conds, [P, VH])
at, veh = inv(S, P), inv(S, VH)
vof = {p: veh[S[p]] for p in P}
assert [(at[i], veh[i]) for i in range(1, 6)] == [("Hari", "Van"), ("Dimpy", "Bike"), ("Sohan", "Car"),
                                                    ("Amrit", "Bicycle"), ("Kanak", "Scooter")]
ARR = "Bottom to top: " + ", ".join(f"floor {i} {at[i]} ({veh[i]})" for i in range(1, 6))
puzzle(FLR, FA, "Basic", "Five floors and five vehicles",
       "Five persons Amrit, Dimpy, Hari, Kanak and Sohan live on the five floors of a building, one on each floor "
       "(floor 1 is the lowermost, floor 5 the topmost). Each owns a different vehicle among a Bicycle, a Bike, a Car, "
       "a Scooter and a Van.", conds,
       "Step 1: Sohan = 3 (Car), Amrit = 4, Kanak = 5.\n"
       "Step 2: Dimpy is on an even floor: 2 (floor 4 is Amrit's). Hari = 1, so Hari owns the Van.\n"
       "Step 3: Bicycle, Bike and Scooter remain for floors 2, 4 and 5. The Scooter is immediately above the Bicycle: "
       "floors 4 and 5 (floor 3 is the Car). So Amrit has the Bicycle, Kanak the Scooter and Dimpy the Bike.\n\n"
       + floors_table(5, None, lambda f: (f, at[f], veh[f]), ["Floor", "Person", "Vehicle"]), ARR)
ans = at[S["Scooter"]]
assert ans == "Kanak"
ask("Who owns the Scooter?", ans, ["Amrit", "Dimpy", "Sohan"], "An adjacency clue between two attributes",
    "The Scooter must be immediately above the Bicycle; the only free adjacent pair is floors 4–5, so the Scooter is "
    "on floor 5: Kanak.", ["Free floors for Bicycle/Bike/Scooter: 2, 4, 5", "Scooter above Bicycle ⇒ 5 above 4",
                           "Floor 5 = Kanak"],
    why="Amrit owns the Bicycle, Dimpy the Bike and Sohan the Car.", sec=40)
ans = vof["Dimpy"]
assert ans == "Bike"
ask("Which vehicle does Dimpy own?", ans, ["Bicycle", "Van", "Scooter"], "The last vehicle by elimination",
    "Van (floor 1), Car (3), Bicycle (4) and Scooter (5) are placed, so Dimpy on floor 2 owns the Bike.",
    ["Placed: Van 1, Car 3, Bicycle 4, Scooter 5", "Floor 2 = Dimpy ⇒ Bike"],
    why="The Bicycle is Amrit's, the Van Hari's and the Scooter Kanak's.", sec=40)
n_ = abs(S["Hari"] - S["Bicycle"]) - 1
assert n_ == 2
c_, w_ = bal(n_)
ask("How many persons live between Hari and the person who owns the Bicycle?", c_, w_,
    "Count floors strictly between", "Hari is on floor 1 and the Bicycle owner (Amrit) on floor 4, so Dimpy and "
    "Sohan live between them.", ["Hari 1, Bicycle = Amrit 4", "Between: 2, 3 ⇒ two"], natural=by_num, sec=40)

# ---- 8FI1 Intermediate (standalone): six floors, three families of two; exactly two floors separate the two members
#      of every family
P = ["Anil", "Bela", "Charu", "Dev", "Uma", "Vikas"]
FAM = {"Anil": "Sen", "Bela": "Sen", "Charu": "Das", "Dev": "Das", "Uma": "Rao", "Vikas": "Rao"}
conds = [
    ("Exactly two floors lie between the two members of each family.", tuple(P),
     lambda *x: all(abs(x[i] - x[j]) == 3 for i in range(6) for j in range(i + 1, 6) if FAM[P[i]] == FAM[P[j]])),
    ("Charu lives on the topmost floor, and Bela on the lowermost floor.", ("Charu", "Bela"),
     lambda c, b: c == 6 and b == 1),
    ("Uma lives immediately above Anil.", ("Uma", "Anil"), lambda u, a: u == a + 1),
]
S = unique(P, {p: range(1, 7) for p in P}, conds, [P])
at = inv(S, P)
assert [at[i] for i in range(1, 7)] == ["Bela", "Vikas", "Dev", "Anil", "Uma", "Charu"]
ans = at[2]
alone(FLR, FF, "Intermediate",
      "Six persons live on the six floors of a building, one on each floor (floor 1 is the lowermost, floor 6 the "
      "topmost). They belong to three families of two: Anil and Bela are the Sens, Charu and Dev are the Dases, and "
      "Uma and Vikas are the Raos.", conds, "Who lives on floor 2?", ans, ["Dev", "Anil", "Uma"],
      "A fixed gap between family members pairs the floors",
      "With two floors between family members, the family pairs must occupy floors 1–4, 2–5 and 3–6. Charu is on 6, "
      "so Dev is on 3. Bela is on 1, so Anil is on 4. Uma is immediately above Anil: floor 5, so Vikas is on floor 2.",
      ["Gap of two floors ⇒ pairs 1–4, 2–5, 3–6", "Charu 6 ⇒ Dev 3; Bela 1 ⇒ Anil 4",
       "Uma = 5 ⇒ Vikas = 2"],
      why="Dev lives on floor 3, Anil on 4 and Uma on 5.", sec=70)

# ---- 8FI2 Intermediate (standalone): seven floors, five persons, two vacant floors
P = ["Gul", "Jas", "Ketki", "Lalan", "Mona"]
conds = [
    ("Jas lives on the topmost floor, and Lalan lives immediately below Jas.", ("Jas", "Lalan"),
     lambda j, l: j == 7 and l == 6),
    ("Exactly two floors lie between Jas and Gul.", ("Gul", "Jas"), lambda g, j: abs(g - j) == 3),
    ("Mona lives immediately below Gul.", ("Mona", "Gul"), lambda m, g: m == g - 1),
    ("Ketki lives on an odd-numbered floor.", ("Ketki",), lambda k: k % 2 == 1),
    ("The two vacant floors are not next to each other.", tuple(P),
     lambda *x: all(f in x or f + 1 in x for f in range(1, 7))),
]
S = unique(P, {p: range(1, 8) for p in P}, conds, [P])
at = inv(S, P)
vac = [f for f in range(1, 8) if f not in at]
assert vac == [2, 5] and S["Ketki"] == 1 and S["Gul"] == 4
n_ = sum(1 for f in vac if f < S["Gul"])
assert n_ == 1
c_, w_ = bal(n_)
alone(FLR, FF, "Intermediate",
      "A building has seven floors, numbered 1 (lowermost) to 7 (topmost). Five persons Gul, Jas, Ketki, Lalan and "
      "Mona live in it, one person per floor, so two floors are vacant.", conds,
      "How many vacant floors are there below Gul?", c_, w_, "Place the persons, then read the gaps",
      "Jas = 7, Lalan = 6, Gul = 4, Mona = 3. Floors 1, 2 and 5 remain for Ketki and the two vacant floors. Ketki is "
      "on an odd floor (1 or 5); if Ketki were on 5, floors 1 and 2 would both be vacant and next to each other. So "
      "Ketki = 1 and floors 2 and 5 are vacant. One vacant floor (2) is below Gul.",
      ["Jas 7, Lalan 6, Gul 4, Mona 3", "Left: 1, 2, 5 for Ketki + two vacancies",
       "Ketki 5 ⇒ 1, 2 vacant and adjacent ✗ ⇒ Ketki 1", "Vacant: 2 and 5 ⇒ one below Gul"],
      natural=by_num, sec=75)

# ---- 8FA1 Advanced (standalone): a building of unknown height with vacant floors
P = ["Ojaswini", "Prithu", "Quresh", "Rekha", "Sunil", "Tanu"]
conds = [
    ("Ojaswini lives on floor 3, and Rekha lives immediately above her.", ("Ojaswini", "Rekha"),
     lambda o, r: o == 3 and r == 4),
    ("Exactly three floors lie between Ojaswini and Prithu, and Prithu lives above her.", ("Prithu", "Ojaswini"),
     lambda p, o: p == o + 4),
    ("Quresh lives on the topmost floor, and the number of floors above Prithu equals the number of floors below "
     "Ojaswini.", ("Quresh", "n", "Prithu", "Ojaswini"), lambda q, n, p, o: q == n and n - p == o - 1),
    ("Sunil lives immediately below Quresh, and Tanu lives on the lowermost floor.", ("Sunil", "Quresh", "Tanu"),
     lambda s, q, t: s == q - 1 and t == 1),
]
V = ["Ojaswini", "Rekha", "Prithu", "n", "Quresh", "Sunil", "Tanu"]
S = unique(V, {v: range(1, 21) for v in V}, conds, [P], extra=[(("n", *P), lambda n, *xs: max(xs) <= n)])
n_ = S["n"]
vac = [f for f in range(1, n_ + 1) if f not in {S[p] for p in P}]
assert n_ == 9 and vac == [2, 5, 6]
k_ = sum(1 for f in vac if S["Rekha"] < f < S["Prithu"])
assert k_ == 2
c_, w_ = bal(k_)
alone(FLR, FF, "Advanced",
      "Six persons Ojaswini, Prithu, Quresh, Rekha, Sunil and Tanu live in a building whose number of floors is not "
      "given. Floor 1 is the lowermost. No floor has more than one person, and every floor not named for a person "
      "below is vacant.", conds, "How many vacant floors lie between Rekha and Prithu?", c_, w_,
      "Find the height of the building from the 'equal number of floors' clue",
      "Ojaswini = 3, Rekha = 4, Prithu = 3 + 4 = 7. Two floors lie below Ojaswini, so two lie above Prithu: the "
      "building has 9 floors and Quresh = 9, Sunil = 8, Tanu = 1. The vacant floors are 2, 5 and 6, and two of them "
      "(5 and 6) lie between Rekha (4) and Prithu (7).",
      ["Ojaswini 3, Rekha 4, Prithu 7", "Floors below Ojaswini = 2 ⇒ floors above Prithu = 2 ⇒ 9 floors",
       "Quresh 9, Sunil 8, Tanu 1 ⇒ vacant 2, 5, 6", "Between 4 and 7: 5, 6 ⇒ two vacant"],
      natural=by_num, sec=100)

# ---- 8FA2 Advanced (standalone): six floors with a North and a South flat on each; nine residents, three vacant
#      flats. Flat = 10 × floor + (1 for North, 2 for South); each North flat is directly above the North flat below.
P = ["Arpita", "Bhaskar", "Damini", "Eshaan", "Gopika", "Indu", "Jayesh", "Meghna", "Pranav"]
FL = [10 * f + s for f in range(1, 7) for s in (1, 2)]
other = lambda c: c + 1 if c % 10 == 1 else c - 1
conds = [
    ("Arpita lives in the North flat of floor 4, and Pranav lives in the other flat on her floor.",
     ("Arpita", "Pranav"), lambda a, p: a == 41 and p == other(a)),
    ("Indu lives directly above Pranav, and Gopika lives directly below Arpita.", ("Indu", "Gopika", "Pranav", "Arpita"),
     lambda i, g, p, a: i == p + 10 and g == a - 10),
    ("Jayesh lives in a North flat on the topmost floor; the other flat on his floor and the flat directly below his "
     "are both vacant.", tuple(P),
     lambda *x: x[6] == 61 and other(61) not in x and 51 not in x),
    ("Eshaan lives in the South flat of the lowermost floor, and Bhaskar lives directly above Eshaan.",
     ("Eshaan", "Bhaskar"), lambda e, b: e == 12 and b == 22),
    ("Damini lives directly below Meghna.", ("Damini", "Meghna"), lambda d, m: d == m - 10),
]
S = unique(["Arpita", "Pranav", "Indu", "Gopika", "Eshaan", "Bhaskar", "Damini", "Meghna", "Jayesh"],
           {p: FL for p in P}, conds, [P])
at = inv(S, P)
assert {p: S[p] for p in P} == {"Arpita": 41, "Bhaskar": 22, "Damini": 11, "Eshaan": 12, "Gopika": 31, "Indu": 52,
                                "Jayesh": 61, "Meghna": 21, "Pranav": 42}
n_ = sum(1 for p in P if S[p] % 10 == 2)
assert n_ == 4
c_, w_ = bal(n_)
alone(FLR, FF, "Advanced",
      "A building has six floors, numbered 1 (lowermost) to 6 (topmost). Each floor has two flats, North and South; "
      "each North flat is directly above the North flat of the floor below, and likewise for the South flats. Nine "
      "persons Arpita, Bhaskar, Damini, Eshaan, Gopika, Indu, Jayesh, Meghna and Pranav live in the building, one per "
      "flat, so three flats are vacant.", conds, "How many persons live in South flats?", c_, w_,
      "Track the vacant flats as carefully as the occupied ones",
      "Arpita = 4 North, Pranav = 4 South, Indu = 5 South, Gopika = 3 North. Jayesh = 6 North, with 6 South and 5 "
      "North vacant. Eshaan = 1 South, Bhaskar = 2 South. Free flats: 1 North, 2 North and 3 South; Damini is "
      "directly below Meghna, which only 1 North / 2 North allow, so 3 South is the third vacant flat. South-flat "
      "residents: Eshaan, Bhaskar, Pranav and Indu — four.",
      ["4N Arpita, 4S Pranav, 5S Indu, 3N Gopika", "6N Jayesh; 6S and 5N vacant", "1S Eshaan, 2S Bhaskar",
       "Damini below Meghna ⇒ 1N Damini, 2N Meghna; 3S vacant", "South: 1S, 2S, 4S, 5S ⇒ four"],
      natural=by_num, sec=110)


# ---- 8B1 Basic set (4): seven gift boxes in a stack (1 = bottom)
B = ["B", "D", "F", "H", "K", "M", "P"]
GF = ["Clock", "Lamp", "Mug", "Pen set", "Scarf", "Toy", "Watch"]
conds = [
    ("Box P is kept exactly in the middle of the stack, and Box B is kept immediately below Box P.", ("P", "B"),
     lambda p, b: p == 4 and b == 3),
    ("Only one box is kept between Box P and Box D, and Box D is kept above Box P.", ("D", "P"),
     lambda d, p: d == p + 2),
    ("Box M is kept at the top of the stack.", ("M",), lambda m: m == 7),
    ("Box H contains the Watch, and it is kept immediately below Box D.", ("H", "Watch", "D"),
     lambda h, w, d: h == w and h == d - 1),
    ("Box F is kept below Box K, and Box B contains the Clock.", ("F", "K", "B", "Clock"),
     lambda f, k, b, c: f < k and c == b),
    ("The box containing the Toy is kept immediately above the box containing the Mug, and below the box containing "
     "the Watch.", ("Toy", "Mug", "Watch"), lambda t, m, w: t == m + 1 and t < w),
    ("The box containing the Scarf is kept two places above the box containing the Lamp.", ("Scarf", "Lamp"),
     lambda s, l: s == l + 2),
]
S = unique(B + GF, {v: range(1, 8) for v in B + GF}, conds, [B, GF])
at, gift = inv(S, B), inv(S, GF)
gof = {b: gift[S[b]] for b in B}
assert [(at[i], gift[i]) for i in range(1, 8)] == [("F", "Mug"), ("K", "Toy"), ("B", "Clock"), ("P", "Lamp"),
                                                    ("H", "Watch"), ("D", "Scarf"), ("M", "Pen set")]
ARR = "Bottom to top: " + ", ".join(f"{i} {at[i]} ({gift[i]})" for i in range(1, 8))
puzzle(BOX, STK, "Basic", "Seven gift boxes in a stack",
       "Seven boxes B, D, F, H, K, M and P are kept one above another in a single stack (position 1 is the bottom and 7 "
       "the top). Each box contains a different gift among a Clock, a Lamp, a Mug, a Pen set, a Scarf, a Toy and a "
       "Watch.", conds,
       "Step 1: P = 4, B = 3, D = 6, M = 7, H = 5 (Watch).\n"
       "Step 2: Positions 1 and 2 remain for F and K; F is below K: F = 1, K = 2. B holds the Clock.\n"
       "Step 3: Lamp, Mug, Pen set, Scarf and Toy remain for positions 1, 2, 4, 6 and 7. The Toy is immediately above "
       "the Mug and below the Watch (5): positions 1–2, so F has the Mug and K the Toy.\n"
       "Step 4: The Scarf is two places above the Lamp: positions 4 and 6, so P has the Lamp, D the Scarf and M the Pen "
       "set.\n\n" + table(["Position", "Box", "Gift"], [(i, at[i], gift[i]) for i in range(7, 0, -1)]), ARR)
ans = at[S["Toy"]]
assert ans == "K"
ask("Which box contains the Toy?", "Box " + ans, ["Box F", "Box P", "Box M"], "An adjacency clue between two gifts",
    "The Toy must sit immediately above the Mug and below the Watch (position 5). The free adjacent pairs are 1–2 and "
    "6–7, and only 1–2 is below the Watch, so the Toy is at position 2: Box K.",
    ["Free adjacent pairs among 1, 2, 4, 6, 7: 1–2 and 6–7", "Toy below Watch (5) ⇒ 1–2", "Toy = position 2 = K"],
    why="F holds the Mug, P the Lamp and M the Pen set.", sec=40)
ans = gof["M"]
assert ans == "Pen set"
ask("What does Box M contain?", ans, ["Scarf", "Lamp", "Watch"], "The last gift by elimination",
    "Lamp and Scarf take positions 4 and 6, so the Pen set is left for M at the top.",
    ["Scarf two above Lamp ⇒ 4 and 6", "Left for position 7 (M): Pen set"],
    why="The Scarf is in D, the Lamp in P and the Watch in H.", sec=40)
n_ = abs(S["F"] - S["Watch"]) - 1
assert n_ == 3
c_, w_ = bal(n_)
ask("How many boxes are kept between Box F and the box containing the Watch?", c_, w_, "Count positions between",
    "F is at position 1 and the Watch (H) at 5, so K, B and P lie between them.",
    ["F 1, Watch = H 5", "Between: 2, 3, 4 ⇒ three"], natural=by_num, sec=40)
ans = at[S["Clock"] + 1]
assert ans == "P"
ask("Which box is kept immediately above the box containing the Clock?", "Box " + ans, ["Box H", "Box K", "Box D"],
    "Find the gift's box, then move one place", "The Clock is in B at position 3; position 4 is Box P.",
    ["Clock = B = 3", "Position 4 = P"], why="K is below B, and H and D are two and three places above it.", sec=40)

# ---- 8B2 Basic set (4): seven coloured boxes in a single line on a shelf (1 = left end, as seen from the front)
B = ["Q", "R", "T", "V", "W", "X", "Y"]
CL = ["Beige", "Blue", "Grey", "Lemon", "Olive", "Peach", "Teal"]
conds = [
    ("Box T is placed exactly in the middle of the line, and Box R is placed immediately to the right of Box T.",
     ("T", "R"), lambda t, r: t == 4 and r == 5),
    ("Box Q is placed second to the left of Box T, and Box Y is placed immediately to the right of Box Q.",
     ("Q", "Y", "T"), lambda q, y, t: q == t - 2 and y == q + 1),
    ("Box W is placed at the extreme left end, and Box V at the extreme right end.", ("W", "V"),
     lambda w, v: w == 1 and v == 7),
    ("Box T is Blue, and the Peach box is placed immediately to the left of the Blue box.", ("T", "Blue", "Peach"),
     lambda t, b, p: b == t and p == b - 1),
    ("The Teal box is at the left end and the Beige box at the right end.", ("Teal", "Beige"),
     lambda t, b: t == 1 and b == 7),
    ("The Grey box is placed between the Teal box and the Peach box.", ("Grey", "Teal", "Peach"),
     lambda g, t, p: min(t, p) < g < max(t, p)),
    ("The Olive box is placed immediately to the right of the Blue box.", ("Olive", "Blue"), lambda o, b: o == b + 1),
]
S = unique(B + CL, {v: range(1, 8) for v in B + CL}, conds, [B, CL])
at, colr = inv(S, B), inv(S, CL)
cofb = {b: colr[S[b]] for b in B}
assert [(at[i], colr[i]) for i in range(1, 8)] == [("W", "Teal"), ("Q", "Grey"), ("Y", "Peach"), ("T", "Blue"),
                                                    ("R", "Olive"), ("X", "Lemon"), ("V", "Beige")]
ARR = "Left to right: " + ", ".join(f"{at[i]} ({colr[i]})" for i in range(1, 8))
puzzle(BOX, BWC, "Basic", "Seven coloured boxes in a line on a shelf",
       "Seven boxes Q, R, T, V, W, X and Y are placed side by side in a single line on a shelf. Left and right are as "
       "seen by a person facing the shelf. Each box is of a different colour among Beige, Blue, Grey, Lemon, Olive, "
       "Peach and Teal.", conds,
       "Number the places 1 to 7 from the left.\n"
       "Step 1: T = 4, R = 5, Q = 2, Y = 3, W = 1, V = 7, so X = 6.\n"
       "Step 2: T is Blue; Peach is immediately left of it: Y. Teal = 1 (W), Beige = 7 (V).\n"
       "Step 3: Grey lies between Teal (1) and Peach (3): place 2, Q. Olive is immediately right of Blue: R. Lemon is "
       "left for X.\n\n" + table(["Place (from left)", "Box", "Colour"], [(i, at[i], colr[i]) for i in range(1, 8)]),
       ARR)
ans = cofb["X"]
assert ans == "Lemon"
ask("What is the colour of Box X?", ans, ["Olive", "Beige", "Peach"], "The last colour by elimination",
    "Teal, Grey, Peach, Blue, Olive and Beige go to W, Q, Y, T, R and V, so X is Lemon.",
    ["Placed: Teal W, Grey Q, Peach Y, Blue T, Olive R, Beige V", "X ⇒ Lemon"],
    why="Olive is R's colour, Beige V's and Peach Y's.", sec=40)
ans = at[S["Grey"]]
assert ans == "Q"
ask("Which box is Grey?", "Box " + ans, ["Box Y", "Box W", "Box X"], "'Between' with both ends fixed",
    "Teal is at place 1 and Peach at place 3, so the Grey box is at place 2: Box Q.",
    ["Teal 1, Peach 3 ⇒ Grey = 2", "Place 2 = Q"], why="Y is Peach, W is Teal and X is Lemon.", sec=40)
n_ = abs(S["W"] - S["Olive"]) - 1
assert n_ == 3
c_, w_ = bal(n_)
ask("How many boxes are placed between Box W and the Olive box?", c_, w_, "Count the places strictly between",
    "W is at place 1 and the Olive box (R) at place 5, so Q, Y and T lie between them.",
    ["W 1, Olive = R 5", "Between: 2, 3, 4 ⇒ three"], natural=by_num, sec=40)
ans = at[S["Y"] + 2]
assert ans == "R"
ask("Which box is placed second to the right of Box Y?", "Box " + ans, ["Box T", "Box X", "Box Q"],
    "Right is as seen from the front", "Y is at place 3; two places to the right is place 5: Box R.",
    ["Y = 3", "3 + 2 = 5 ⇒ R"], why="T is immediately right of Y, X is third to its right and Q is to its left.",
    sec=40)

# ---- 8B3 Intermediate set (3): nine boxes in three stacks of different heights — Left (2 boxes), Middle (3) and
#      Right (4). Cell = 10 × stack + level (stack 1 = Left, 2 = Middle, 3 = Right; level 1 = bottom).
B = ["B", "C", "F", "J", "L", "N", "R", "U", "Z"]
CELLS = [11, 12, 21, 22, 23, 31, 32, 33, 34]
TOP = {1: 12, 2: 23, 3: 34}
conds = [
    ("Box L is at the top of the tallest stack, and Box R is directly below Box L.", ("L", "R"),
     lambda l, r: l == 34 and r == 33),
    ("Box U is directly below Box R. Box B is in the middle stack, at the same level as Box U.", ("U", "R", "B"),
     lambda u, r, b: u == r - 1 and b == 20 + u % 10),
    ("Box N is directly above Box B.", ("N", "B"), lambda n, b: n == b + 1),
    ("Box C is at the top of a stack, and Box J is directly below Box C.", ("C", "J"),
     lambda c, j: c in TOP.values() and j == c - 1),
    ("Box Z is not in the same stack as Box L.", ("Z", "L"), lambda z, l: z // 10 != l // 10),
]
S = unique(B, {b: CELLS for b in B}, conds, [B])
at = inv(S, B)
SN = {1: "Left", 2: "Middle", 3: "Right"}
assert {b: S[b] for b in B} == {"J": 11, "C": 12, "Z": 21, "B": 22, "N": 23, "F": 31, "U": 32, "R": 33, "L": 34}
ARR = "; ".join(f"{SN[s]} stack (bottom to top): " + ", ".join(at[10 * s + l] for l in range(1, {1: 3, 2: 4, 3: 5}[s]))
                for s in (1, 2, 3))
puzzle(BOX, STK, "Intermediate", "Nine boxes in three stacks of different heights",
       "Nine boxes B, C, F, J, L, N, R, U and Z are kept in three stacks standing side by side: the Left stack has two "
       "boxes, the Middle stack three and the Right stack four. Level 1 is the bottom of every stack; 'directly "
       "above/below' means in the same stack, one level higher/lower.", conds,
       "Step 1: The tallest stack is the Right one: L = Right 4, R = Right 3, U = Right 2.\n"
       "Step 2: B is in the Middle stack at U's level: Middle 2. N is directly above B: Middle 3, the top of that "
       "stack.\n"
       "Step 3: C is at the top of a stack with J directly below it. Right and Middle tops are taken, so C = Left 2 and "
       "J = Left 1.\n"
       "Step 4: Middle 1 and Right 1 remain for F and Z. Z is not in L's (Right) stack: Z = Middle 1, F = Right 1.\n\n"
       + table(["Level", "Left", "Middle", "Right"],
               [(l, at.get(10 + l, "–"), at.get(20 + l, "–"), at[30 + l]) for l in range(4, 0, -1)]), ARR)
ans = at[S["N"] - 1]
assert ans == "B"
ask("Which box is kept directly below Box N?", "Box " + ans, ["Box Z", "Box U", "Box C"],
    "'Directly below' stays in the same stack", "N is at Middle level 3; directly below it, Middle level 2, is B.",
    ["N = Middle 3", "Middle 2 = B"], why="Z is two levels below N; U and C are in other stacks.", sec=50)
n_ = 4 - S["U"] % 10
assert n_ == 2
c_, w_ = bal(n_)
ask("Counting only the Right stack, how many boxes sit higher than Box U?", c_, w_, "Count only within the same stack",
    "U is at level 2 of the four-box Right stack; R and L are above it.", ["U = Right 2", "Above: R (3), L (4) ⇒ two"],
    natural=by_num, sec=50)
ans = at[31]
assert ans == "F"
ask("Which box is at the bottom of the Right stack?", "Box " + ans, ["Box Z", "Box J", "Box U"],
    "Use the last negative clue", "Middle 1 and Right 1 remain for F and Z; Z is not in the Right stack (L's), so F is "
    "at the bottom of the Right stack.", ["Free: Middle 1, Right 1", "Z not with L ⇒ F = Right 1"],
    why="Z is at the bottom of the Middle stack, J at the bottom of the Left stack, and U at Right 2.", sec=50)

# ---- 8B4 Advanced set (4): two stacks of four boxes; in each stack every box is lighter than the box below it.
#      Cell = 10 × stack + level (stack 1 = A, 2 = B; level 1 = bottom). Cell weights are variables "c<cell>".
B = ["D", "E", "G", "H", "K", "M", "P", "T"]
WT = [5, 7, 9, 12, 15, 18, 21, 24]
CELLS = [11, 12, 13, 14, 21, 22, 23, 24]
CW = ["c" + str(c) for c in CELLS]
wof = lambda pos, cws: cws[CELLS.index(pos)]  # weight of the box in cell pos
conds = [
    ("Box T is the heaviest box and is in stack A.", ("T", *CW), lambda t, *cw: t // 10 == 1 and wof(t, cw) == 24),
    ("Box K is at the top of stack B and weighs 7 kg.", ("K", *CW), lambda k, *cw: k == 24 and wof(k, cw) == 7),
    ("Box M is the lightest box.", ("M", *CW), lambda m, *cw: wof(m, cw) == 5),
    ("Box H is at the bottom of stack B and weighs 3 kg less than Box T.", ("H", "T", *CW),
     lambda h, t, *cw: h == 21 and wof(h, cw) == wof(t, cw) - 3),
    ("Box G is kept directly below Box D.", ("G", "D"), lambda g, d: d == g + 1),
    ("Box P weighs twice as much as Box E.", ("P", "E", *CW), lambda p, e, *cw: wof(p, cw) == 2 * wof(e, cw)),
    ("Box G is in the same stack as Box T.", ("G", "T"), lambda g, t: g // 10 == t // 10),
]
order = [((10 * s + l, 10 * s + l + 1)) for s in (1, 2) for l in (1, 2, 3)]
extra = [(("c" + str(a), "c" + str(b_)), lambda x, y: x > y) for a, b_ in order]
S = unique(CW + B, {c: WT for c in CW} | {b: CELLS for b in B}, conds, [CW, B], extra=extra)
at = inv(S, B)
wt = {b: S["c" + str(S[b])] for b in B}
assert [(at[c], wt[at[c]]) for c in CELLS] == [("T", 24), ("G", 15), ("D", 12), ("M", 5), ("H", 21), ("P", 18),
                                               ("E", 9), ("K", 7)]
ARR = ("Stack A (bottom to top): " + ", ".join(f"{at[10 + l]} {wt[at[10 + l]]} kg" for l in range(1, 5)) +
       "; Stack B: " + ", ".join(f"{at[20 + l]} {wt[at[20 + l]]} kg" for l in range(1, 5)))
puzzle(BOX, BWC, "Advanced", "Two stacks, lighter boxes always on top",
       "Eight boxes D, E, G, H, K, M, P and T are kept in two stacks, A and B, with four boxes in each stack (level 1 is "
       "the bottom of a stack). Their weights are 5, 7, 9, 12, 15, 18, 21 and 24 kg, one weight per box. In each stack, "
       "every box is lighter than the box directly below it.", conds,
       "Step 1: Every stack gets lighter upwards, so the heaviest box is at the bottom of its stack: T = A1 (24 kg). "
       "K = B4 (7 kg). H = B1 with 24 − 3 = 21 kg.\n"
       "Step 2: The lightest box M (5 kg) must be at the top of a stack; B4 is K, so M = A4.\n"
       "Step 3: D, E, G and P take A2, A3, B2 and B3 with 9, 12, 15 and 18 kg. P = 2 × E, so P = 18 and E = 9; G and D "
       "share 12 and 15.\n"
       "Step 4: G is directly below D and in T's stack, so G and D are in stack A (G = A2, D = A3) and P, E are in "
       "stack B. In each stack the lower box is heavier: G = 15, D = 12, P = B2 (18), E = B3 (9).\n\n"
       + table(["Level", "Stack A", "Stack B"],
               [(l, f"{at[10 + l]} ({wt[at[10 + l]]} kg)", f"{at[20 + l]} ({wt[at[20 + l]]} kg)")
                for l in range(4, 0, -1)]), ARR)
c_, w_ = bal(wt["D"], fmt=lambda v: f"{v} kg", step=3, lo=6)
ask("What is the weight of Box D?", c_, w_, "Lower boxes are heavier",
    "G and D share 12 and 15 kg, and G is directly below D, so G is heavier: D weighs 12 kg.",
    ["P 18, E 9 (P = 2 × E) ⇒ G, D share 12, 15", "G below D ⇒ D = 12 kg"], natural=lambda t: int(t.split()[0]),
    sec=80)
ans = at[S["H"] + 1]
assert ans == "P"
ask("Which box is kept directly above Box H?", "Box " + ans, ["Box E", "Box G", "Box K"],
    "Place stack B from its two fixed ends", "H is at B1 and K at B4. P and E share B2 and B3, and P (18 kg) is heavier "
    "than E (9 kg), so P is directly above H.", ["B1 H, B4 K", "P 18 > E 9 ⇒ P = B2"],
    why="E is at B3, G is in stack A, and K is at the top of stack B.", sec=80)
tot = sum(wt[at[10 + l]] for l in range(1, 5))
assert tot == 56
c_, w_ = bal(tot, fmt=lambda v: f"{v} kg", step=3, lo=40)
ask("What is the total weight of the boxes in stack A?", c_, w_, "Add the four weights of one stack",
    "Stack A holds T (24), G (15), D (12) and M (5): 24 + 15 + 12 + 5 = 56 kg.",
    ["Stack A: T 24, G 15, D 12, M 5", "Sum = 56 kg"], natural=lambda t: int(t.split()[0]), sec=80)
n_ = sum(1 for b in B if wt[b] > wt["P"])
assert n_ == 2
c_, w_ = bal(n_)
ask("How many boxes are heavier than Box P?", c_, w_, "Compare across both stacks",
    "P weighs 18 kg; only T (24 kg) and H (21 kg) are heavier.", ["P = 18 kg", "Heavier: T 24, H 21 ⇒ two"],
    natural=by_num, sec=70)


# ################################################################################################ BATCH 009
begin("009")

# ---- 9LB Basic (standalone): five persons facing south
P = ["Ganga", "Hemu", "Indra", "Jolly", "Kamal"]
conds = [
    ("Ganga sits exactly in the middle of the row, and Indra sits immediately to her left.", ("Ganga", "Indra"),
     lambda g, i: g == 3 and i == g + 1),
    ("Hemu sits at an extreme end of the row, next to Indra.", ("Hemu", "Indra"),
     lambda h, i: h in (1, 5) and abs(h - i) == 1),
    ("Jolly does not sit next to Ganga.", ("Jolly", "Ganga"), lambda j, g: abs(j - g) != 1),
]
S = unique(P, {p: range(1, 6) for p in P}, conds, [P])
at = inv(S, P)
assert [at[i] for i in range(1, 6)] == ["Jolly", "Kamal", "Ganga", "Indra", "Hemu"]
alone(LIN, SGL, "Basic",
      "Five persons Ganga, Hemu, Indra, Jolly and Kamal sit in a straight row, all facing south. (For a person facing "
      "south, the right is towards the west and the left is towards the east.)", conds,
      "Who sits at the extreme right end of the row?", at[1], ["Hemu", "Kamal", "Indra"],
      "Facing south, the right end of the row is its west end",
      "Number the seats 1 to 5 from the west. Ganga = 3; her left is east, so Indra = 4, and Hemu, at an end next to "
      "Indra, = 5. Jolly cannot sit next to Ganga, so Jolly = 1 and Kamal = 2. The right end (west end) is seat 1: "
      "Jolly.",
      ["Ganga 3, Indra 4 (left = east), Hemu 5", "Jolly not next to Ganga ⇒ Jolly 1, Kamal 2",
       "Right end = west end = seat 1 ⇒ Jolly"],
      why="Hemu is at the left (east) end; Kamal and Indra are not at an end.", sec=50)

# ---- 9LI1 Intermediate set (5): two rows of four seats, ALL facing south; Row 1 is in front, Row 2 directly behind.
#      Cell = 10 × row + column, columns 1..4 from the west. Facing south: right = west (lower column).
P = ["Aalok", "Binita", "Chakshu", "Dhanvi", "Ehsaan", "Fenil", "Gauransh", "Hetal"]
CELLS = [10 * r + c for r in (1, 2) for c in range(1, 5)]
conds = [
    ("Aalok sits in the front row, second from the right end of that row.", ("Aalok",), lambda a: a == 12),
    ("Gauransh sits directly behind Aalok, and Chakshu sits immediately to the left of Gauransh.",
     ("Gauransh", "Aalok", "Chakshu"), lambda g, a, c: g == a + 10 and c == g + 1),
    ("Dhanvi sits second to the left of Aalok, and Ehsaan sits directly behind Dhanvi.", ("Dhanvi", "Aalok", "Ehsaan"),
     lambda d, a, e: d == a + 2 and e == d + 10),
    ("Hetal sits in the front row at one of its ends.", ("Hetal",), lambda h: h in (11, 14)),
    ("Binita does not sit in the front row.", ("Binita",), lambda b: b // 10 == 2),
]
S = unique(P, {p: CELLS for p in P}, conds, [P])
at = inv(S, P)
assert [[at[10 * r + c] for c in range(1, 5)] for r in (1, 2)] == [["Hetal", "Aalok", "Fenil", "Dhanvi"],
                                                                    ["Binita", "Gauransh", "Chakshu", "Ehsaan"]]
ARR = ("West to east — Row 1 (front): " + ", ".join(at[10 + c] for c in range(1, 5)) + "; Row 2 (behind): " +
       ", ".join(at[20 + c] for c in range(1, 5)) + "; everyone faces south")
puzzle(LIN, DBL, "Intermediate", "Two rows facing south, one behind the other",
       "Eight persons Aalok, Binita, Chakshu, Dhanvi, Ehsaan, Fenil, Gauransh and Hetal sit in two rows of four seats "
       "each. Everyone faces south. Row 1 is the front row; Row 2 is directly behind it, so each person in Row 2 sits "
       "directly behind one person in Row 1. (Facing south, the right is towards the west and the left towards the "
       "east.)", conds,
       "Number the columns 1 to 4 from the west. Facing south, the right end of a row is its west end.\n"
       "Step 1: Aalok = Row 1, column 2. Gauransh = Row 2, column 2; Chakshu, to his left (east): Row 2, column 3.\n"
       "Step 2: Dhanvi is second to Aalok's left: Row 1, column 4; Ehsaan behind her: Row 2, column 4.\n"
       "Step 3: Free seats: Row 1 columns 1 and 3, Row 2 column 1. Hetal is at an end of the front row: column 1. "
       "Binita is not in the front row: Row 2, column 1. Fenil = Row 1, column 3.\n\n"
       + table(["Column (from west)", "Row 1 (front)", "Row 2 (behind)"],
               [(c, at[10 + c], at[20 + c]) for c in range(1, 5)]), ARR)
ans = at[S["Fenil"] + 10]
assert ans == "Chakshu"
ask("Who sits directly behind Fenil?", ans, ["Gauransh", "Ehsaan", "Binita"], "Same column, next row",
    "Fenil is in Row 1, column 3; directly behind is Row 2, column 3: Chakshu.",
    ["Fenil = Row 1, col 3", "Behind = Row 2, col 3 = Chakshu"],
    why="Gauransh is behind Aalok, Ehsaan behind Dhanvi and Binita behind Hetal.", sec=50)
ans = at[S["Chakshu"] - 1]
assert ans == "Gauransh"
ask("Who sits immediately to the right of Chakshu?", ans, ["Ehsaan", "Fenil", "Binita"],
    "Facing south: right = west", "Chakshu is in Row 2, column 3, facing south; his right is west: column 2, Gauransh.",
    ["Chakshu = Row 2, col 3", "Right = west ⇒ col 2 = Gauransh"],
    why="Ehsaan is to his left, Fenil in front of him, and Binita second to his right.", sec=50)
ans = at[21]
assert ans == "Binita"
ask("Who sits at the right end of the back row?", ans, ["Ehsaan", "Hetal", "Gauransh"],
    "The right end for south-facing persons is the west end", "In Row 2 the west end is column 1: Binita.",
    ["Facing south ⇒ right end = west end", "Row 2, col 1 = Binita"],
    why="Ehsaan is at the left (east) end of the back row; Hetal is in the front row; Gauransh is not at an end.",
    sec=45)
n_ = abs(S["Hetal"] - S["Dhanvi"]) - 1
assert n_ == 2
c_, w_ = bal(n_)
ask("How many persons sit between Hetal and Dhanvi in the front row?", c_, w_, "Count seats strictly between",
    "Hetal is at column 1 and Dhanvi at column 4 of the front row, so Aalok and Fenil sit between them.",
    ["Hetal col 1, Dhanvi col 4", "Between: Aalok, Fenil ⇒ two"], natural=by_num, sec=45)
ans = at[S["Binita"] - 10]
assert ans == "Hetal"
ask("Who sits directly in front of Binita?", ans, ["Aalok", "Fenil", "Gauransh"], "In front = same column, Row 1",
    "Binita is in Row 2, column 1; directly in front is Row 1, column 1: Hetal.",
    ["Binita = Row 2, col 1", "Front = Row 1, col 1 = Hetal"],
    why="Aalok is in front of Gauransh, Fenil in front of Chakshu, and Gauransh sits beside Binita.", sec=45)

# ---- 9LI2 Intermediate set (4): seven players facing north, each wearing a different jersey number
P = ["Kuldeep", "Lipsa", "Murari", "Nandan", "Paridhi", "Ruchika", "Somnath"]
J = ["j" + p for p in P]
NUMS = [7, 9, 10, 14, 18, 21, 23]
conds = [
    ("Lipsa sits exactly in the middle of the row and wears the smallest number.", ("Lipsa", "jLipsa"),
     lambda l, j: l == 4 and j == 7),
    ("The person wearing 23 sits at the extreme left end of the row.", (*P, *J),
     lambda *x: x[7 + x[:7].index(1)] == 23),
    ("Kuldeep sits immediately to the right of Lipsa, and his number is twice Murari's.",
     ("Kuldeep", "Lipsa", "jKuldeep", "jMurari"), lambda k, l, jk, jm: k == l + 1 and jk == 2 * jm),
    ("Nandan sits at the extreme right end, and his number is three times Lipsa's.", ("Nandan", "jNandan", "jLipsa"),
     lambda n, jn, jl: n == 7 and jn == 3 * jl),
    ("Ruchika sits immediately to the left of Nandan, and Somnath sits second to the left of Kuldeep.",
     ("Ruchika", "Nandan", "Somnath", "Kuldeep"), lambda r, n, s, k: r == n - 1 and s == k - 2),
    ("Murari does not sit at an end of the row.", ("Murari",), lambda m: m not in (1, 7)),
    ("Somnath's number is greater than Ruchika's.", ("jSomnath", "jRuchika"), lambda s, r: s > r),
]
V = ["Lipsa", "Kuldeep", "Nandan", "Ruchika", "Somnath", "Murari", "Paridhi"] + J
S = unique(V, {p: range(1, 8) for p in P} | {j: NUMS for j in J}, conds, [P, J])
at = inv(S, P)
jn = {p: S["j" + p] for p in P}
assert [(at[i], jn[at[i]]) for i in range(1, 8)] == [
    ("Paridhi", 23), ("Murari", 9), ("Somnath", 14), ("Lipsa", 7), ("Kuldeep", 18), ("Ruchika", 10), ("Nandan", 21)]
ARR = "Left to right: " + ", ".join(f"{at[i]} ({jn[at[i]]})" for i in range(1, 8))
puzzle(LIN, SGL, "Intermediate", "Seven players in a row, with jersey numbers",
       "Seven players Kuldeep, Lipsa, Murari, Nandan, Paridhi, Ruchika and Somnath sit in a straight row, all facing "
       "north. Their jersey numbers are 7, 9, 10, 14, 18, 21 and 23, a different number for each player. (Facing "
       "north, the right is towards the east.)", conds,
       "Number the seats 1 to 7 from the left.\n"
       "Step 1: Lipsa = 4 (number 7). Kuldeep = 5, Nandan = 7 with 3 × 7 = 21, Ruchika = 6, Somnath = 3.\n"
       "Step 2: Seats 1 and 2 remain for Murari and Paridhi; Murari is not at an end: Murari = 2, Paridhi = 1. The "
       "number 23 is at the left end: Paridhi.\n"
       "Step 3: 9, 10, 14 and 18 remain for Murari, Somnath, Kuldeep and Ruchika. Kuldeep = 2 × Murari: 18 and 9. "
       "Somnath's number is greater than Ruchika's: Somnath 14, Ruchika 10.\n\n"
       + table(["Seat", "Player", "Number"], [(i, at[i], jn[at[i]]) for i in range(1, 8)]), ARR)
c_, w_ = bal(jn["Somnath"], fmt=str, step=2, lo=8)
ask("What is Somnath's jersey number?", c_, w_,
    "Use the doubling clue before the comparison",
    "Kuldeep = 2 × Murari leaves only 18 and 9 for them; of 10 and 14, the larger goes to Somnath.",
    ["Left: 9, 10, 14, 18", "Kuldeep 18, Murari 9", "Somnath > Ruchika ⇒ Somnath 14"], natural=int, sec=60)
ans = next(p for p in P if jn[p] == 10)
assert ans == "Ruchika"
ask("Who wears number 10?", ans, ["Murari", "Somnath", "Paridhi"], "The last pair by comparison",
    "10 and 14 remain for Somnath and Ruchika, and Somnath's is greater, so Ruchika wears 10.",
    ["10, 14 for Somnath and Ruchika", "Somnath > Ruchika ⇒ Ruchika 10"],
    why="Murari wears 9, Somnath 14 and Paridhi 23.", sec=55)
tot = jn[at[S["Lipsa"] - 1]] + jn[at[S["Lipsa"] + 1]]
assert tot == 32
c_, w_ = bal(tot, fmt=str, step=2, lo=26)
ask("What is the sum of the jersey numbers of Lipsa's two immediate neighbours?", c_, w_,
    "Identify both neighbours, then add", "Lipsa's neighbours are Somnath (14) and Kuldeep (18): 14 + 18 = 32.",
    ["Neighbours: Somnath (3), Kuldeep (5)", "14 + 18 = 32"], natural=int, sec=60)
ans = at[S[next(p for p in P if jn[p] == 9)] + 2]
assert ans == "Lipsa"
ask("Who sits second to the right of the player wearing 9?", ans, ["Somnath", "Kuldeep", "Paridhi"],
    "Locate the number first", "Number 9 is Murari's, at seat 2. Two seats to the right is seat 4: Lipsa.",
    ["9 = Murari (seat 2)", "2 + 2 = 4 ⇒ Lipsa"],
    why="Somnath is immediately to his right, Kuldeep third to his right, and Paridhi to his left.", sec=55)

# ---- 9LA Advanced (standalone): a row of unknown length; the side is settled by the size limit
V = ["Xavier", "Yogini", "n", "Waman"]
conds = [
    ("Xavier sits twelfth from the left end, and Yogini sits ninth from the right end.", ("Xavier", "Yogini", "n"),
     lambda x, y, n: x == 12 and n - y + 1 == 9),
    ("Exactly five persons sit between Xavier and Yogini.", ("Xavier", "Yogini"), lambda x, y: abs(x - y) == 6),
    ("The row has fewer than twenty persons.", ("n",), lambda n: n < 20),
    ("Waman sits third to the right of Yogini.", ("Waman", "Yogini"), lambda w, y: w == y + 3),
]
NAMED = ["Xavier", "Yogini", "Waman"]
S = unique(V, {v: range(1, 41) for v in V}, conds, [NAMED], extra=[(("n", *NAMED), lambda n, *xs: max(xs) <= n)])
assert (S["n"], S["Yogini"], S["Waman"]) == (14, 6, 9)
n_ = S["Xavier"] - S["Waman"] - 1
assert n_ == 2
c_, w_ = bal(n_)
alone(LIN, UNK, "Advanced",
      "Some persons sit in a straight row, all facing north. The number of persons is not given; Waman, Xavier and "
      "Yogini are among them.", conds, "How many persons sit between Waman and Xavier?", c_, w_,
      "Test both sides for the second person and keep the case the size limit allows",
      "If Yogini sat to the right of Xavier she would be 12 + 6 = 18th from the left and the row would have "
      "18 + 9 − 1 = 26 persons — more than allowed. So Yogini is 12 − 6 = 6th from the left and the row has "
      "6 + 9 − 1 = 14 persons. Waman is 6 + 3 = 9th from the left, so the 10th and 11th persons sit between Waman and "
      "Xavier (12th).",
      ["Yogini right of Xavier ⇒ 18th ⇒ 26 persons ✗ (fewer than 20)", "Yogini = 6th from left ⇒ n = 14",
       "Waman = 9th", "Between 9th and 12th: 10th, 11th ⇒ two"], natural=by_num, sec=100)


# ---- 9C1 Basic set (5): six persons facing the centre, each wearing a different coloured cap (Daya fixed at 0)
P = ["Daya", "Kirpal", "Nutan", "Pinki", "Ramesh", "Sonu"]
CP = ["Black", "Green", "Orange", "Red", "White", "Yellow"]
R6 = lambda s, k: (s + k) % 6
conds = [
    ("Kirpal sits opposite Daya, and Sonu sits immediately to the left of Kirpal.", ("Kirpal", "Sonu", "Daya"),
     lambda k, s, d: k == R6(d, 3) and s == R6(k, -1)),
    ("Nutan sits immediately between Daya and Sonu.", ("Nutan", "Daya", "Sonu"), lambda n, d, s: {R6(n, 1), R6(n, -1)} == {d, s}),
    ("Pinki sits immediately to the left of Daya.", ("Pinki", "Daya"), lambda p, d: p == R6(d, -1)),
    ("Daya wears the Red cap, and the person wearing the Green cap sits opposite her.", ("Daya", "Red", "Green"),
     lambda d, r, g: r == d and g == R6(d, 3)),
    ("The person wearing the White cap sits immediately to the right of Daya.", ("White", "Daya"),
     lambda w, d: w == R6(d, 1)),
    ("The person wearing the Black cap sits second to the left of Ramesh.", ("Black", "Ramesh"),
     lambda b, r: b == R6(r, -2)),
    ("Pinki does not wear the Yellow cap.", ("Pinki", "Yellow"), lambda p, y: p != y),
]
S = unique(P + CP, {"Daya": [0]} | {v: range(6) for v in P[1:] + CP}, conds, [P, CP])
at, cap = inv(S, P), inv(S, CP)
cof = {p: cap[S[p]] for p in P}
assert [(at[i], cap[i]) for i in range(6)] == [("Daya", "Red"), ("Nutan", "White"), ("Sonu", "Black"),
                                               ("Kirpal", "Green"), ("Ramesh", "Yellow"), ("Pinki", "Orange")]
ARR = "Anticlockwise from Daya: " + ", ".join(f"{at[i]} ({cap[i]})" for i in range(6))
puzzle(CIR, CEN, "Basic", "Six persons around a round table, with coloured caps",
       "Six persons Daya, Kirpal, Nutan, Pinki, Ramesh and Sonu sit around a circular table, equally spaced and all "
       "facing the centre. Each wears a cap of a different colour among Black, Green, Orange, Red, White and Yellow. "
       "(Facing the centre, a person's right is anticlockwise and the left clockwise.)", conds,
       "Number the seats 0 to 5 anticlockwise from Daya.\n"
       "Step 1: Kirpal = 3 (opposite). Sonu, to Kirpal's left (clockwise): 2. Nutan sits between Daya and Sonu: 1. "
       "Pinki, to Daya's left: 5. Ramesh = 4.\n"
       "Step 2: Daya Red, Kirpal (opposite) Green, Nutan (Daya's right) White. Black is second to Ramesh's left "
       "(clockwise from 4): seat 2, Sonu.\n"
       "Step 3: Orange and Yellow remain for Ramesh and Pinki; Pinki does not wear Yellow: Pinki Orange, Ramesh "
       "Yellow.\n\n" + table(["Seat (anticlockwise)", "Person", "Cap"], [(i, at[i], cap[i]) for i in range(6)]), ARR)
ans = at[S["Black"]]
assert ans == "Sonu"
ask("Who wears the Black cap?", ans, ["Nutan", "Ramesh", "Pinki"], "Facing the centre: left = clockwise",
    "Ramesh is at seat 4; two seats clockwise is seat 2: Sonu.", ["Ramesh = 4", "Second to his left: 3, 2 ⇒ Sonu"],
    why="Nutan wears White, Ramesh Yellow and Pinki Orange.", sec=40)
ans = cof["Ramesh"]
assert ans == "Yellow"
ask("Which cap does Ramesh wear?", ans, ["Orange", "White", "Green"], "The last pair by a negative clue",
    "Orange and Yellow remain for Ramesh and Pinki; Pinki does not wear Yellow, so Ramesh does.",
    ["Left: Orange, Yellow", "Pinki ≠ Yellow ⇒ Ramesh Yellow"],
    why="Orange is Pinki's, White Nutan's and Green Kirpal's.", sec=40)
ans = at[R6(S["Kirpal"], 2)]
assert ans == "Pinki"
ask("Who sits second to the right of Kirpal?", ans, ["Ramesh", "Daya", "Sonu"], "Right = anticlockwise",
    "Kirpal is at seat 3; anticlockwise: seat 4 (Ramesh), seat 5 (Pinki).", ["Kirpal = 3", "3 → 4 → 5 ⇒ Pinki"],
    why="Ramesh is immediately to his right, Daya opposite him, and Sonu immediately to his left.", sec=40)
ans = at[R6(S["White"], 3)]
assert ans == "Ramesh"
ask("Who sits opposite the person wearing the White cap?", ans, ["Pinki", "Kirpal", "Sonu"],
    "Opposite = three seats away at a six-seat table", "Nutan wears White and sits at seat 1; seat 4 is opposite: "
    "Ramesh.", ["White = Nutan = 1", "Opposite = 4 ⇒ Ramesh"],
    why="Pinki is opposite Sonu, and Kirpal is opposite Daya.", sec=40)
t, f = one_true([("Nutan sits immediately to the right of Sonu", S["Nutan"] == R6(S["Sonu"], 1)),
                 ("Pinki wears the Green cap", cof["Pinki"] == "Green"),
                 ("Ramesh sits immediately between Kirpal and Pinki", {R6(S["Ramesh"], 1), R6(S["Ramesh"], -1)} ==
                  {S["Kirpal"], S["Pinki"]}),
                 ("Daya sits opposite Sonu", S["Sonu"] == R6(S["Daya"], 3))])
ask("Which of the following statements is true?", t, f, "Checking each statement against the arrangement",
    "Ramesh (seat 4) has Kirpal (3) and Pinki (5) on either side.",
    ["Sonu (2): right = anticlockwise = seat 3 = Kirpal, not Nutan ✗", "Pinki wears Orange ✗",
     "Ramesh between Kirpal and Pinki ✓", "Daya is opposite Kirpal ✗"],
    why="Nutan is on Sonu's left, Pinki wears Orange, and Daya sits opposite Kirpal.", sec=45)


# ---- 9C2 Intermediate set (4): eight persons facing the centre, with ages (Akhilesh fixed at 0)
P = ["Akhilesh", "Bhagwati", "Deepti", "Gurmeet", "Jasoda", "Kamlesh", "Neetu", "Sahil"]
A = ["a" + p for p in P]
AG = [21, 24, 27, 30, 33, 36, 39, 42]
conds = [
    ("Sahil sits opposite Akhilesh and is the oldest of all.", ("Sahil", "aSahil"), lambda s, a: s == 4 and a == 42),
    ("Neetu is the youngest of all and sits immediately to the right of Akhilesh.", ("Neetu", "aNeetu"),
     lambda n, a: n == 1 and a == 21),
    ("Gurmeet sits second to the left of Sahil and is 18 years older than Neetu.",
     ("Gurmeet", "Sahil", "aGurmeet", "aNeetu"), lambda g, s, ag, an: g == R8(s, -2) and ag == an + 18),
    ("Deepti sits immediately to the right of Sahil and is 3 years older than Neetu.",
     ("Deepti", "Sahil", "aDeepti", "aNeetu"), lambda d, s, ad, an: d == R8(s, 1) and ad == an + 3),
    ("Kamlesh sits opposite Gurmeet, and Jasoda sits immediately between Gurmeet and Sahil.",
     ("Kamlesh", "Gurmeet", "Jasoda", "Sahil"),
     lambda k, g, j, s: k == R8(g, 4) and {R8(j, 1), R8(j, -1)} == {g, s}),
    ("Akhilesh is older than Bhagwati but younger than Kamlesh.", ("aAkhilesh", "aBhagwati", "aKamlesh"),
     lambda a, b, k: b < a < k),
    ("Jasoda is 3 years younger than Bhagwati.", ("aJasoda", "aBhagwati"), lambda j, b: j == b - 3),
]
V = ["Sahil", "Neetu", "Gurmeet", "Deepti", "Kamlesh", "Jasoda", "Bhagwati"] + A
S = unique(["Akhilesh"] + V, {"Akhilesh": [0]} | {p: range(8) for p in P[1:]} | {a: AG for a in A}, conds, [P, A])
at = inv(S, P)
age = {p: S["a" + p] for p in P}
assert [(at[i], age[at[i]]) for i in range(8)] == [
    ("Akhilesh", 33), ("Neetu", 21), ("Gurmeet", 39), ("Jasoda", 27), ("Sahil", 42), ("Deepti", 24), ("Kamlesh", 36),
    ("Bhagwati", 30)]
ARR = "Anticlockwise from Akhilesh: " + ", ".join(f"{at[i]} ({age[at[i]]})" for i in range(8))
puzzle(CIR, CEN, "Intermediate", "Eight persons around a round table, with ages",
       "Eight persons Akhilesh, Bhagwati, Deepti, Gurmeet, Jasoda, Kamlesh, Neetu and Sahil sit around a circular "
       "table, equally spaced and all facing the centre. Their ages are 21, 24, 27, 30, 33, 36, 39 and 42 years, one "
       "age each. (Facing the centre, the right is anticlockwise.)", conds,
       "Number the seats 0 to 7 anticlockwise from Akhilesh.\n"
       "Step 1: Sahil = 4 (42). Neetu = 1 (21). Gurmeet, second to Sahil's left (clockwise): 2, aged 21 + 18 = 39. "
       "Deepti, to Sahil's right: 5, aged 24.\n"
       "Step 2: Kamlesh is opposite Gurmeet: 6. Jasoda sits between Gurmeet (2) and Sahil (4): 3. Bhagwati = 7.\n"
       "Step 3: 27, 30, 33 and 36 remain for Akhilesh, Bhagwati, Jasoda and Kamlesh. Jasoda = Bhagwati − 3 and "
       "Bhagwati < Akhilesh < Kamlesh: Jasoda 27, Bhagwati 30, Akhilesh 33, Kamlesh 36 (Jasoda 30, Bhagwati 33 would "
       "leave Akhilesh younger than Bhagwati).\n\n"
       + table(["Seat", "Person", "Age"], [(i, at[i], age[at[i]]) for i in range(8)]), ARR)
c_, w_ = bal(age["Kamlesh"], fmt=str, step=3, lo=21)
ask("How old is Kamlesh?", c_, w_, "Order the four remaining ages with the two comparison clues",
    "Of 27, 30, 33 and 36, Jasoda and Bhagwati must be 3 apart and Bhagwati < Akhilesh < Kamlesh. Only Jasoda 27, "
    "Bhagwati 30, Akhilesh 33, Kamlesh 36 works.", ["Left: 27, 30, 33, 36", "Jasoda = Bhagwati − 3",
                                                     "Bhagwati < Akhilesh < Kamlesh ⇒ Kamlesh 36"],
    natural=int, sec=60)
ans = at[R8(S["Sahil"], -1)]
assert ans == "Jasoda"
ask("Who sits immediately to the left of the oldest person?", ans, ["Deepti", "Gurmeet", "Kamlesh"],
    "Left = clockwise", "The oldest is Sahil (seat 4); clockwise next is seat 3: Jasoda.",
    ["Oldest = Sahil = 4", "Left = 3 ⇒ Jasoda"],
    why="Deepti is to Sahil's right, Gurmeet second to his left, and Kamlesh second to his right.", sec=55)
d_ = age["Sahil"] - age["Akhilesh"]
assert d_ == 9
c_, w_ = bal(d_, fmt=lambda v: f"{v} years", step=3, lo=3)
ask("What is the difference between the age of Akhilesh and the age of the person sitting opposite him?", c_, w_, "Find both ages first",
    "Sahil is 42 and Akhilesh is 33: the difference is 9 years.", ["Sahil 42, Akhilesh 33", "42 − 33 = 9"],
    natural=lambda t: int(t.split()[0]), sec=55)
ans = sorted(P, key=age.get)[1]
assert ans == "Deepti"
ask("Who is the second youngest?", ans, ["Jasoda", "Neetu", "Bhagwati"], "Rank by age",
    "Neetu is 21 (youngest) and Deepti 24, the next age.", ["Neetu 21", "Deepti 24 ⇒ second youngest"],
    why="Neetu is the youngest; Jasoda (27) and Bhagwati (30) come after Deepti.", sec=50)

# ---- 9CA Advanced set (6): eight persons facing the centre, seated by rank — the person ranked next always sits
#      third to the right of the previous one. Seat of rank r = 3(r − 1) mod 8 (rank 1 at seat 0 removes rotations).
P = ["Aanya", "Balwant", "Darshana", "Gitesh", "Himmat", "Kesar", "Prachi", "Shivam"]
RK = ["r" + p for p in P]
conds = [
    ("Prachi sits second to the left of Himmat, and Shivam sits immediately to the right of Prachi.",
     ("Prachi", "Himmat", "Shivam"), lambda p, h, s: p == R8(h, -2) and s == R8(p, 1)),
    ("Gitesh sits opposite Kesar, and Aanya sits immediately to the left of Kesar.", ("Gitesh", "Kesar", "Aanya"),
     lambda g, k, a: g == R8(k, 4) and a == R8(k, -1)),
    ("Balwant is ranked last, and Kesar is ranked below Darshana.", ("rBalwant", "rKesar", "rDarshana"),
     lambda b, k, d: b == 8 and k > d),
]
LINKR = [((p, "r" + p), lambda s, r: s == 3 * (r - 1) % 8) for p in P]
S = unique(RK + P, {r: range(1, 9) for r in RK} | {p: range(8) for p in P}, conds, [RK, P], extra=LINKR)
at = inv(S, P)
rk = {p: S["r" + p] for p in P}
assert [(at[i], rk[at[i]]) for i in range(8)] == [
    ("Prachi", 1), ("Shivam", 4), ("Himmat", 7), ("Gitesh", 2), ("Darshana", 5), ("Balwant", 8), ("Aanya", 3),
    ("Kesar", 6)]
ARR = "Anticlockwise from the top-ranked person: " + ", ".join(f"{at[i]} (rank {rk[at[i]]})" for i in range(8))
puzzle(CIR, CEN, "Advanced", "Eight persons seated in order of rank",
       "Eight persons Aanya, Balwant, Darshana, Gitesh, Himmat, Kesar, Prachi and Shivam sit around a circular table, "
       "equally spaced and all facing the centre. They were ranked 1 to 8 in a test (rank 1 is the highest), and they "
       "are seated so that the person with each next rank (2 after 1, 3 after 2, and so on up to 8) sits third to the "
       "right of the person with the previous rank. (Facing the centre, the right is anticlockwise.)", conds,
       "Number the seats 0 to 7 anticlockwise from the rank-1 person. Moving three seats right each time, the ranks "
       "1 to 8 sit at seats 0, 3, 6, 1, 4, 7, 2, 5. So seat 0 = rank 1, 1 = rank 4, 2 = rank 7, 3 = rank 2, 4 = rank 5, "
       "5 = rank 8, 6 = rank 3, 7 = rank 6.\n"
       "Step 1: Balwant (rank 8) = seat 5. Prachi, Shivam and Himmat sit in three consecutive seats p, p + 1, p + 2; "
       "Kesar, Aanya and Gitesh satisfy Aanya = Kesar − 1 and Gitesh = Kesar + 4.\n"
       "Step 2: Avoiding seat 5, the only fits are (a) Prachi 0, Shivam 1, Himmat 2, Gitesh 3, Aanya 6, Kesar 7, "
       "Darshana 4, or (b) Prachi 1, Shivam 2, Himmat 3, Kesar 0, Aanya 7, Gitesh 4, Darshana 6.\n"
       "Step 3: In (b) Kesar would be ranked 1, above Darshana (rank 3) ✗. So (a): Prachi 1, Gitesh 2, Aanya 3, Shivam 4, "
       "Darshana 5, Kesar 6, Himmat 7, Balwant 8.\n\n"
       + table(["Seat", "Person", "Rank"], [(i, at[i], rk[at[i]]) for i in range(8)]), ARR)
ans = next(p for p in P if rk[p] == 3)
assert ans == "Aanya"
ask("Who is ranked third?", ans, ["Shivam", "Gitesh", "Darshana"], "Ranks follow a fixed step round the table",
    "Rank 3 sits at seat 6 (three seats right of rank 2 at seat 3): Aanya.", ["Rank seats: 1→0, 2→3, 3→6",
                                                                              "Seat 6 = Aanya"],
    why="Gitesh is 2nd, Shivam 4th and Darshana 5th.", sec=90)
ans = at[R8(S["Gitesh"], 2)]
assert ans == "Balwant"
ask("Who sits second to the right of the person ranked second?", ans, ["Darshana", "Aanya", "Himmat"],
    "Right = anticlockwise", "Gitesh (rank 2) is at seat 3; anticlockwise: Darshana (4), Balwant (5).",
    ["Rank 2 = Gitesh, seat 3", "3 → 4 → 5 ⇒ Balwant"],
    why="Darshana is immediately to his right, Aanya third to his right and Himmat to his left.", sec=80)
c_, w_ = bal(rk["Himmat"], fmt=ORD, lo=1, hi=8)
ask("What is Himmat's rank?", c_, w_, "Read the rank of the seat", "Himmat sits at seat 2, which holds rank 7.",
    ["Seat 2 ↔ rank 7 (0, 3, 6, 1, 4, 7, 2 ⇒ the 7th rank lands on seat 2)"], natural=ordn, sec=80)
n_ = (S["Balwant"] - S["Prachi"]) % 8 - 1
assert n_ == 4
c_, w_ = bal(n_)
ask("How many persons sit between Prachi and Balwant, counting from Prachi's right?", c_, w_,
    "Count anticlockwise from Prachi", "Prachi is at 0 and Balwant at 5: seats 1, 2, 3, 4 lie between.",
    ["Prachi 0 → Balwant 5 anticlockwise", "Seats 1–4 ⇒ four"], natural=by_num, sec=80)
ans = at[R8(S["Prachi"], 4)]
assert ans == "Darshana"
ask("Who sits opposite the person ranked first?", ans, ["Shivam", "Kesar", "Gitesh"], "Opposite = four seats away",
    "Prachi (rank 1) is at seat 0; seat 4 is Darshana's.", ["Rank 1 = Prachi, seat 0", "Opposite = seat 4 = Darshana"],
    why="Shivam and Kesar are Prachi's neighbours; Gitesh is three seats to her right.", sec=75)
t, f = one_true([("Shivam is ranked fourth", rk["Shivam"] == 4), ("Gitesh sits next to Prachi",
                                                                 abs(S["Gitesh"] - S["Prachi"]) in (1, 7)),
                 ("Kesar is ranked fifth", rk["Kesar"] == 5),
                 ("Aanya sits immediately to the right of Kesar", S["Aanya"] == R8(S["Kesar"], 1))])
ask("Which of the following statements is true?", t, f, "Checking each statement against the table",
    "Shivam sits at seat 1, which holds rank 4.", ["Shivam = seat 1 = rank 4 ✓", "Gitesh (3) is not next to Prachi (0) ✗",
                                                   "Kesar is ranked 6th ✗",
                                                   "Kesar's right (seat 0) is Prachi; Aanya is on his left ✗"],
    why="Gitesh sits three seats from Prachi, Kesar is 6th, and Aanya is on Kesar's left.", sec=80)


# ---- 9F1 Basic set (6): seven floors and favourite fruits
P = ["Bunty", "Chikki", "Golu", "Jugnu", "Minku", "Pappu", "Tinku"]
FR = ["Apple", "Banana", "Grapes", "Guava", "Mango", "Orange", "Papaya"]
conds = [
    ("Minku lives on floor 4 and likes Orange.", ("Minku", "Orange"), lambda m, o: m == 4 and o == 4),
    ("Chikki lives immediately above Minku, and Bunty lives immediately below Minku.", ("Chikki", "Bunty", "Minku"),
     lambda c, b, m: c == m + 1 and b == m - 1),
    ("Pappu lives on the topmost floor, and Jugnu lives between Chikki and Pappu.", ("Pappu", "Jugnu", "Chikki"),
     lambda p, j, c: p == 7 and c < j < p),
    ("Golu lives below Tinku.", ("Golu", "Tinku"), lambda g, t: g < t),
    ("The person who likes Mango lives immediately below the person who likes Orange, and the person who likes "
     "Grapes lives two floors above the Mango lover.", ("Mango", "Orange", "Grapes"),
     lambda m, o, g: m == o - 1 and g == m + 2),
    ("The person on the topmost floor likes Papaya, and Golu likes Guava.", ("Papaya", "Golu", "Guava"),
     lambda p, g, gu: p == 7 and gu == g),
    ("Tinku does not like Banana.", ("Tinku", "Banana"), lambda t, b: t != b),
]
S = unique(P + FR, {v: range(1, 8) for v in P + FR}, conds, [P, FR])
at, fru = inv(S, P), inv(S, FR)
fof = {p: fru[S[p]] for p in P}
assert [(at[i], fru[i]) for i in range(1, 8)] == [
    ("Golu", "Guava"), ("Tinku", "Apple"), ("Bunty", "Mango"), ("Minku", "Orange"), ("Chikki", "Grapes"),
    ("Jugnu", "Banana"), ("Pappu", "Papaya")]
ARR = "Bottom to top: " + ", ".join(f"floor {i} {at[i]} ({fru[i]})" for i in range(1, 8))
puzzle(FLR, FA, "Basic", "Seven floors and seven fruits",
       "Seven persons Bunty, Chikki, Golu, Jugnu, Minku, Pappu and Tinku live on the seven floors of a building, one on "
       "each floor (floor 1 is the lowermost, floor 7 the topmost). Each likes a different fruit among Apple, Banana, "
       "Grapes, Guava, Mango, Orange and Papaya.", conds,
       "Step 1: Minku = 4 (Orange), Chikki = 5, Bunty = 3, Pappu = 7, Jugnu = 6 (between 5 and 7).\n"
       "Step 2: Floors 1 and 2 remain for Golu and Tinku; Golu is below: Golu = 1, Tinku = 2.\n"
       "Step 3: Mango is immediately below Orange: floor 3 (Bunty). Grapes is two floors above Mango: floor 5 (Chikki). "
       "Papaya: floor 7 (Pappu). Golu: Guava.\n"
       "Step 4: Apple and Banana remain for Tinku (2) and Jugnu (6); Tinku does not like Banana: Tinku Apple, Jugnu "
       "Banana.\n\n" + floors_table(7, None, lambda f: (f, at[f], fru[f]), ["Floor", "Person", "Fruit"]), ARR)
ans = at[S["Grapes"]]
assert ans == "Chikki"
ask("Who likes Grapes?", ans, ["Jugnu", "Bunty", "Tinku"], "Chain two attribute clues",
    "Orange is on floor 4, so Mango is on 3 and Grapes on 5: Chikki.", ["Orange 4 ⇒ Mango 3 ⇒ Grapes 5",
                                                                       "Floor 5 = Chikki"],
    why="Jugnu likes Banana, Bunty Mango and Tinku Apple.", sec=40)
ans = fof["Tinku"]
assert ans == "Apple"
ask("Which fruit does Tinku like?", ans, ["Banana", "Guava", "Mango"], "The last pair by a negative clue",
    "Apple and Banana are left for Tinku and Jugnu; Tinku does not like Banana.",
    ["Left: Apple, Banana", "Tinku ≠ Banana ⇒ Apple"], why="Banana is Jugnu's, Guava Golu's and Mango Bunty's.",
    sec=40)
n_ = abs(S["Golu"] - S["Mango"]) - 1
assert n_ == 1
c_, w_ = bal(n_)
ask("How many persons live between Golu and the person who likes Mango?", c_, w_, "Floors strictly between",
    "Golu is on floor 1 and the Mango lover (Bunty) on floor 3; only Tinku lives between them.",
    ["Golu 1, Mango = Bunty 3", "Between: floor 2 ⇒ one"], natural=by_num, sec=40)
ans = at[S["Banana"] + 1]
assert ans == "Pappu"
ask("Who lives immediately above the person who likes Banana?", ans, ["Chikki", "Minku", "Jugnu"],
    "Find the fruit, then move up", "Banana is Jugnu's, on floor 6; floor 7 is Pappu's.",
    ["Banana = Jugnu = 6", "Floor 7 = Pappu"], why="Chikki lives immediately below Jugnu; Jugnu is the Banana lover.",
    sec=40)
ans = at[2]
assert ans == "Tinku"
ask("Who lives on floor 2?", ans, ["Golu", "Bunty", "Jugnu"], "The last pair of persons by an 'above' clue",
    "Floors 1 and 2 remain for Golu and Tinku, and Golu lives below Tinku, so Tinku is on floor 2.",
    ["Free: 1, 2", "Golu below Tinku ⇒ Tinku 2"], why="Golu is on floor 1, Bunty on 3 and Jugnu on 6.", sec=35)
t, f = one_true([("Bunty likes Orange", fof["Bunty"] == "Orange"),
                 ("Jugnu lives immediately above Chikki", S["Jugnu"] == S["Chikki"] + 1),
                 ("Two persons live between Golu and Chikki", abs(S["Golu"] - S["Chikki"]) - 1 == 2),
                 ("Pappu likes Banana", fof["Pappu"] == "Banana")])
ask("Which of the following statements is true?", t, f, "Checking each statement against the floors",
    "Jugnu (6) lives immediately above Chikki (5).",
    ["Bunty likes Mango ✗", "Jugnu 6, Chikki 5 ✓", "Golu 1, Chikki 5 ⇒ three persons between, not two ✗",
     "Pappu likes Papaya ✗"], why="Bunty likes Mango, three persons live between Golu and Chikki, and Pappu likes "
                                  "Papaya.", sec=45)


# ---- 9FI1 Intermediate set (5): five floors with a West and an East flat on each; ten residents.
#      Flat = 10 × floor + (1 West, 2 East).
P = ["Ajit", "Bimla", "Chaman", "Dharmesh", "Ekam", "Firoza", "Gaurangi", "Hardik", "Ishita", "Jaggi"]
FL = [10 * f + s for f in range(1, 6) for s in (1, 2)]
conds = [
    ("Ajit lives in the West flat of floor 3, and Gaurangi lives in the other flat on his floor.",
     ("Ajit", "Gaurangi"), lambda a, g: a == 31 and g == 32),
    ("Jaggi lives directly above Gaurangi, and Bimla lives directly above Jaggi.", ("Jaggi", "Gaurangi", "Bimla"),
     lambda j, g, b: j == g + 10 and b == j + 10),
    ("Hardik lives on the topmost floor, and Ekam lives directly below Hardik.", ("Hardik", "Ekam"),
     lambda h, e: h // 10 == 5 and e == h - 10),
    ("Chaman lives in an East flat on a floor below Ajit's.", ("Chaman", "Ajit"),
     lambda c, a: c % 10 == 2 and c // 10 < a // 10),
    ("Ishita lives on the lowermost floor, and Firoza lives directly above Dharmesh.", ("Ishita", "Firoza", "Dharmesh"),
     lambda i, f, d: i // 10 == 1 and f == d + 10),
]
S = unique(P, {p: FL for p in P}, conds, [P])
at = inv(S, P)
assert [[at[10 * f + s] for s in (1, 2)] for f in range(5, 0, -1)] == [
    ["Hardik", "Bimla"], ["Ekam", "Jaggi"], ["Ajit", "Gaurangi"], ["Firoza", "Chaman"], ["Dharmesh", "Ishita"]]
ARR = "Top to bottom (West, East): " + "; ".join(f"floor {f}: {at[10 * f + 1]}, {at[10 * f + 2]}"
                                                 for f in range(5, 0, -1))
puzzle(FLR, FF, "Intermediate", "Ten residents in a five-storey building with two flats per floor",
       "Ten persons Ajit, Bimla, Chaman, Dharmesh, Ekam, Firoza, Gaurangi, Hardik, Ishita and Jaggi live in a "
       "five-storey building (floor 1 is the lowermost). Each floor has two flats, West and East; each West flat is "
       "directly above the West flat of the floor below, and likewise for the East flats. One person lives in each "
       "flat.", conds,
       "Step 1: Ajit = 3 West, Gaurangi = 3 East, Jaggi = 4 East, Bimla = 5 East.\n"
       "Step 2: Hardik is on floor 5; the East flat is Bimla's, so Hardik = 5 West and Ekam = 4 West.\n"
       "Step 3: Chaman is in an East flat below floor 3: 1 East or 2 East. Firoza is directly above Dharmesh: the "
       "free stacked pairs are 1–2 West and 1–2 East, and the East pair would leave no East flat for Chaman, so "
       "Dharmesh = 1 West, Firoza = 2 West.\n"
       "Step 4: Ishita is on floor 1: 1 East. Chaman = 2 East.\n\n"
       + table(["Floor", "West", "East"], [(f, at[10 * f + 1], at[10 * f + 2]) for f in range(5, 0, -1)]), ARR)
ans = at[S["Chaman"] - 10]
assert ans == "Ishita"
ask("Who lives directly below Chaman?", ans, ["Dharmesh", "Gaurangi", "Firoza"], "Directly below = same side",
    "Chaman lives in 2 East; directly below is 1 East: Ishita.", ["Chaman = 2 East", "1 East = Ishita"],
    why="Dharmesh is diagonally below, Gaurangi above, and Firoza beside Chaman.", sec=50)
ans = at[S["Ekam"] + 1]
assert ans == "Jaggi"
ask("Who lives in the other flat on Ekam's floor?", ans, ["Bimla", "Ajit", "Hardik"], "Same floor, other side",
    "Ekam lives in 4 West; 4 East is Jaggi's.", ["Ekam = 4 West", "4 East = Jaggi"],
    why="Bimla and Hardik are on floor 5, Ajit on floor 3.", sec=45)
ans = at[S["Firoza"] + 10]
assert ans == "Ajit"
ask("Who lives directly above Firoza?", ans, ["Ekam", "Gaurangi", "Chaman"], "Directly above = same side",
    "Firoza is in 2 West; directly above is 3 West: Ajit.", ["Firoza = 2 West", "3 West = Ajit"],
    why="Ekam is two floors above her, Gaurangi diagonally above, and Chaman beside her.", sec=45)
n_ = sum(1 for p in P if S[p] % 10 == 2 and S[p] > S["Chaman"])
assert n_ == 3
c_, w_ = bal(n_)
ask("How many persons live in East flats above Chaman?", c_, w_, "Count one column only",
    "Above 2 East are Gaurangi (3 East), Jaggi (4 East) and Bimla (5 East).", ["East column above 2: 3, 4, 5 ⇒ three"],
    natural=by_num, sec=45)
ans = at[21]
assert ans == "Firoza"
ask("Who lives in the West flat of floor 2?", ans, ["Dharmesh", "Chaman", "Ishita"],
    "The only stacked free pair settles Firoza and Dharmesh",
    "Floors 1 and 2 are left. Firoza and Dharmesh need one column (West or East), but Chaman needs an East flat "
    "there, so they take the West column: Firoza (above) = 2 West.",
    ["Free: 1W, 1E, 2W, 2E; Chaman needs 1E or 2E", "Firoza–Dharmesh column = West ⇒ Firoza 2 West"],
    why="Dharmesh is in 1 West, Chaman in 2 East and Ishita in 1 East.", sec=50)

# ---- 9FI2 Intermediate set (4): six floors, each person with a pet and a drink
P = ["Lakhan", "Mili", "Nirja", "Omi", "Rasika", "Taran"]
PT = ["Cat", "Dog", "Fish", "Hamster", "Parrot", "Rabbit"]
DR = ["Coffee", "Juice", "Lassi", "Milk", "Soup", "Tea"]
conds = [
    ("Lakhan lives on an even-numbered floor and owns the Cat.", ("Lakhan", "Cat"), lambda l, c: l % 2 == 0 and c == l),
    ("The Fish owner lives immediately below the Cat owner.", ("Fish", "Cat"), lambda f, c: f == c - 1),
    ("Nirja lives on the topmost floor and drinks Lassi.", ("Nirja", "Lassi"), lambda n, l: n == 6 and l == 6),
    ("Omi lives somewhere between Lakhan and Nirja.", ("Omi", "Lakhan", "Nirja"), lambda o, l, n: l < o < n),
    ("The Rabbit owner drinks Juice and lives immediately below the Lassi drinker.", ("Rabbit", "Juice", "Lassi"),
     lambda r, j, l: r == j and r == l - 1),
    ("Taran lives on the lowermost floor and drinks Tea; Mili lives immediately above Taran and owns the Dog.",
     ("Taran", "Tea", "Mili", "Dog"), lambda t, te, m, d: t == 1 and te == 1 and m == 2 and d == 2),
    ("Rasika drinks Coffee.", ("Rasika", "Coffee"), lambda r, c: r == c),
    ("The Hamster owner lives above the Parrot owner, and the Milk drinker lives above the Soup drinker.",
     ("Hamster", "Parrot", "Milk", "Soup"), lambda h, p, m, s: h > p and m > s),
]
V = P + PT + DR
S = unique(V, {v: range(1, 7) for v in V}, conds, [P, PT, DR])
at, pet, drk = inv(S, P), inv(S, PT), inv(S, DR)
assert [(at[i], pet[i], drk[i]) for i in range(1, 7)] == [
    ("Taran", "Parrot", "Tea"), ("Mili", "Dog", "Soup"), ("Rasika", "Fish", "Coffee"), ("Lakhan", "Cat", "Milk"),
    ("Omi", "Rabbit", "Juice"), ("Nirja", "Hamster", "Lassi")]
ARR = "Bottom to top: " + ", ".join(f"{i} {at[i]} ({pet[i]}, {drk[i]})" for i in range(1, 7))
puzzle(FLR, FA, "Intermediate", "Six floors, six pets and six drinks",
       "Six persons Lakhan, Mili, Nirja, Omi, Rasika and Taran live on the six floors of a building, one on each floor "
       "(floor 1 is the lowermost). Each owns a different pet among a Cat, a Dog, a Fish, a Hamster, a Parrot and a "
       "Rabbit, and each drinks a different one of Coffee, Juice, Lassi, Milk, Soup and Tea.", conds,
       "Step 1: Nirja = 6 (Lassi). Taran = 1 (Tea), Mili = 2 (Dog).\n"
       "Step 2: The Rabbit owner, who drinks Juice, is on floor 5. Lakhan (Cat) is on an even floor: 4 (2 is Mili's), "
       "so the Fish is on floor 3.\n"
       "Step 3: Omi lives between Lakhan (4) and Nirja (6): 5, so Omi owns the Rabbit and drinks Juice. Rasika = 3 "
       "(Fish) and drinks Coffee.\n"
       "Step 4: Hamster and Parrot remain for Nirja (6) and Taran (1); the Hamster is higher: Nirja Hamster, Taran "
       "Parrot. Milk and Soup remain for Lakhan (4) and Mili (2); Milk is higher: Lakhan Milk, Mili Soup.\n\n"
       + floors_table(6, None, lambda f: (f, at[f], pet[f], drk[f]), ["Floor", "Person", "Pet", "Drink"]), ARR)
ans = at[S["Fish"]]
assert ans == "Rasika"
ask("Who owns the Fish?", ans, ["Omi", "Mili", "Lakhan"], "The Cat fixes the Fish",
    "Lakhan (Cat) must be on floor 4, so the Fish is on floor 3: Rasika.", ["Lakhan = 4", "Fish = 3 = Rasika"],
    why="Omi owns the Rabbit, Mili the Dog and Lakhan the Cat.", sec=55)
ans = drk[S["Lakhan"]]
assert ans == "Milk"
ask("What does Lakhan drink?", ans, ["Soup", "Coffee", "Juice"], "A comparison clue for the last pair",
    "Milk and Soup remain for Lakhan (4) and Mili (2); the Milk drinker lives higher, so Lakhan drinks Milk.",
    ["Left: Milk, Soup for floors 4 and 2", "Milk above Soup ⇒ Lakhan Milk"],
    why="Soup is Mili's drink, Coffee Rasika's and Juice Omi's.", sec=55)
ans = at[S["Soup"]]
assert ans == "Mili"
ask("Who drinks Soup?", ans, ["Taran", "Lakhan", "Rasika"], "Same step as the Milk drinker",
    "Soup goes to the lower of floors 2 and 4: Mili.", ["Milk above Soup", "Soup = floor 2 = Mili"],
    why="Taran drinks Tea, Lakhan Milk and Rasika Coffee.", sec=50)
ans = pet[S["Taran"]]
assert ans == "Parrot"
ask("Which pet does Taran own?", ans, ["Hamster", "Rabbit", "Dog"], "The Hamster is above the Parrot",
    "Hamster and Parrot remain for Nirja (6) and Taran (1); the Hamster owner lives higher, so Taran owns the Parrot.",
    ["Left: Hamster, Parrot for floors 6 and 1", "Hamster above Parrot ⇒ Taran Parrot"],
    why="Nirja owns the Hamster, Omi the Rabbit and Mili the Dog.", sec=50)

# ---- 9FA1 Advanced (standalone): six residents of a nine-floor building whose floor numbers are linked by arithmetic
P = ["Arush", "Bindu", "Chiku", "Devi", "Eshu", "Faru"]
conds = [
    ("Eshu lives on the topmost floor, and Eshu's floor number is the square of Devi's.", ("Eshu", "Devi"),
     lambda e, d: e == 9 and e == d * d),
    ("Chiku's floor number is twice Devi's, and Bindu's floor number is twice Arush's.",
     ("Chiku", "Devi", "Bindu", "Arush"), lambda c, d, b, a: c == 2 * d and b == 2 * a),
    ("Arush lives immediately above Devi, and Faru lives on the lowermost floor.", ("Arush", "Devi", "Faru"),
     lambda a, d, f: a == d + 1 and f == 1),
]
S = unique(P, {p: range(1, 10) for p in P}, conds, [P])
vac = [f for f in range(1, 10) if f not in S.values()]
assert {p: S[p] for p in P} == {"Arush": 4, "Bindu": 8, "Chiku": 6, "Devi": 3, "Eshu": 9, "Faru": 1}
assert vac == [2, 5, 7]
n_ = sum(1 for f in vac if S["Arush"] < f < S["Bindu"])
assert n_ == 2
c_, w_ = bal(n_)
alone(FLR, FF, "Advanced",
      "A building has nine floors, numbered 1 (lowermost) to 9 (topmost). Six persons Arush, Bindu, Chiku, Devi, Eshu "
      "and Faru live in it, one person per floor; the other three floors are vacant.", conds,
      "How many vacant floors lie between Arush and Bindu?", c_, w_, "Turn each arithmetic clue into a floor number",
      "Eshu = 9 = Devi², so Devi = 3. Then Chiku = 6, Arush = 4 and Bindu = 8; Faru = 1. The vacant floors are 2, 5 "
      "and 7. Between Arush (4) and Bindu (8) lie floors 5, 6 and 7, of which 5 and 7 are vacant.",
      ["Eshu 9 = Devi² ⇒ Devi 3", "Chiku = 6, Arush = 4, Bindu = 8, Faru = 1", "Vacant: 2, 5, 7",
       "Between 4 and 8: 5 (vacant), 6 (Chiku), 7 (vacant) ⇒ two"], natural=by_num, sec=90)

# ---- 9FA2 Advanced (standalone): six floors, a sum clue and case elimination
P = ["Hina", "Ivan", "Jojo", "Lalli", "Moti", "Nanu"]
conds = [
    ("The sum of the floor numbers of Hina and Nanu is 7.", ("Hina", "Nanu"), lambda h, n: h + n == 7),
    ("Ivan lives two floors above Hina, and Lalli lives somewhere above Ivan.", ("Ivan", "Hina", "Lalli"),
     lambda i, h, l: i == h + 2 and l > i),
    ("Jojo lives on an even-numbered floor below Hina.", ("Jojo", "Hina"), lambda j, h: j % 2 == 0 and j < h),
    ("Moti lives on an odd-numbered floor.", ("Moti",), lambda m: m % 2 == 1),
]
S = unique(P, {p: range(1, 7) for p in P}, conds, [P])
at = inv(S, P)
assert [at[i] for i in range(1, 7)] == ["Moti", "Jojo", "Hina", "Nanu", "Ivan", "Lalli"]
ans = at[S["Hina"] - 1]
alone(FLR, FF, "Advanced",
      "Six persons Hina, Ivan, Jojo, Lalli, Moti and Nanu live on the six floors of a building, one on each floor. "
      "Floor 1 is the lowermost and floor 6 the topmost.", conds, "Who lives immediately below Hina?", ans,
      ["Moti", "Nanu", "Ivan"], "List the cases for the sum clue and eliminate",
      "Lalli is above Ivan, who is two above Hina, so Hina ≤ 3. Hina = 1 leaves no floor below for Jojo; Hina = 2 "
      "leaves only floor 1 below, which is odd. So Hina = 3, Nanu = 4, Ivan = 5, Lalli = 6, Jojo = 2 and Moti = 1. "
      "Jojo lives immediately below Hina.",
      ["Lalli > Ivan = Hina + 2 ⇒ Hina ≤ 3", "Hina 1 ✗ (Jojo needs an even floor below); Hina 2 ✗ (only floor 1 "
       "below)", "Hina 3 ⇒ Nanu 4, Ivan 5, Lalli 6, Jojo 2, Moti 1", "Below Hina ⇒ Jojo"],
      why="Moti is on floor 1, Nanu immediately above Hina, and Ivan two floors above her.", sec=90)


# ---- 9BB1 Basic (standalone): five boxes in a stack (1 = bottom)
B = ["G", "K", "P", "S", "W"]
conds = [
    ("Box G is kept exactly in the middle of the stack, and Box P is kept at the top.", ("G", "P"),
     lambda g, p: g == 3 and p == 5),
    ("Box S is kept immediately below Box P.", ("S", "P"), lambda s, p: s == p - 1),
    ("Only one box is kept between Box K and Box G.", ("K", "G"), lambda k, g: abs(k - g) == 2),
]
S = unique(B, {b: range(1, 6) for b in B}, conds, [B])
at = inv(S, B)
assert [at[i] for i in range(1, 6)] == ["K", "W", "G", "S", "P"]
alone(BOX, STK, "Basic",
      "Five boxes G, K, P, S and W are kept one above another in a single stack. Position 1 is the bottom and position "
      "5 the top.", conds, "Which box is kept immediately above Box W?", "Box " + at[S["W"] + 1],
      ["Box S", "Box K", "Box P"], "Fill the fixed positions first",
      "G = 3, P = 5, S = 4. K is two places from G: 1 or 5; 5 is P's, so K = 1. W takes position 2, and the box "
      "immediately above it is G.", ["G 3, P 5, S 4", "K = 1 (5 taken)", "W = 2 ⇒ above it: G"],
      why="S is two places above W, K is below W, and P is at the top.", sec=40)

# ---- 9BB2 Basic (standalone): six coloured boxes in a stack (1 = bottom)
B = ["C", "F", "I", "L", "O", "U"]
CL = ["Blue", "Brown", "Green", "Pink", "Red", "White"]
conds = [
    ("Box F is Red and is kept fourth from the bottom.", ("F", "Red"), lambda f, r: f == 4 and r == 4),
    ("Box L is kept immediately above Box F and is Green.", ("L", "F", "Green"), lambda l, f, g: l == f + 1 and g == l),
    ("Box I, kept at the top, is Brown.", ("I", "Brown"), lambda i, b: i == 6 and b == 6),
    ("Box C is Blue and is kept immediately below Box U.", ("C", "U", "Blue"), lambda c, u, b: c == u - 1 and b == c),
    ("The Pink box is kept at the bottom of the stack.", ("Pink",), lambda p: p == 1),
]
S = unique(B + CL, {v: range(1, 7) for v in B + CL}, conds, [B, CL])
at, colr = inv(S, B), inv(S, CL)
ans = colr[S["U"]]
assert [at[i] for i in range(1, 7)] == ["O", "C", "U", "F", "L", "I"] and ans == "White"
alone(BOX, BWC, "Basic",
      "Six boxes C, F, I, L, O and U are kept one above another in a single stack (position 1 is the bottom and 6 the "
      "top). Each box is of a different colour among Blue, Brown, Green, Pink, Red and White.", conds,
      "What is the colour of Box U?", ans, ["Pink", "Blue", "Green"], "Place the boxes, then the leftover colours",
      "F = 4 (Red), L = 5 (Green), I = 6 (Brown). Positions 1, 2 and 3 remain for C, O and U, with C immediately "
      "below U: C = 2, U = 3 or C = 1, U = 2. The bottom box is Pink, but C is Blue, so C is not at the bottom: C = 2, "
      "U = 3, O = 1 (Pink). The only colour left is White, for U.",
      ["F 4 Red, L 5 Green, I 6 Brown", "C below U; C (Blue) cannot be the Pink bottom box ⇒ C 2, U 3, O 1",
       "Left colour: White ⇒ U"], why="Pink is O's colour, Blue C's and Green L's.", sec=55)

# ---- 9BA1 Advanced (standalone): nine boxes in three colours, three of each; no two boxes of one colour touch
B = ["B", "D", "G", "J", "M", "Q", "S", "V", "X"]
CC = [f"c{i}" for i in range(1, 10)]  # colour at position i
col = lambda pos, cs: cs[pos - 1]
conds = [
    ("Box J is kept exactly in the middle of the stack and is Green; Box B is kept immediately above J and is Blue.",
     ("J", "B", *CC), lambda j, b, *cs: j == 5 and col(j, cs) == "G" and b == 6 and col(b, cs) == "U"),
    ("Box M is kept at the bottom and is Red.", ("M", *CC), lambda m, *cs: m == 1 and col(m, cs) == "R"),
    ("Exactly two boxes are kept between any two Red boxes that have no other Red box between them.", tuple(CC),
     lambda *cs: (lambda r: all(b - a == 3 for a, b in zip(r, r[1:])))([i + 1 for i in range(9) if cs[i] == "R"])),
    ("Box Q and Box S are both Red, and Q is kept above S.", ("Q", "S", *CC),
     lambda q, s, *cs: q > s and col(q, cs) == col(s, cs) == "R"),
    ("Box G is kept at the top, and the box immediately below G is Green.", ("G", *CC),
     lambda g, *cs: g == 9 and col(8, cs) == "G"),
    ("No two boxes of the same colour are kept one immediately above the other.", tuple(CC),
     lambda *cs: all(cs[i] != cs[i + 1] for i in range(8))),
    ("Box D is kept between Box X and Box S, and Box X is of the same colour as Box B.", ("D", "X", "S", "B", *CC),
     lambda d, x, s, b, *cs: min(x, s) < d < max(x, s) and col(x, cs) == col(b, cs)),
]
S = unique(CC + B, {c: "RUG" for c in CC} | {b: range(1, 10) for b in B}, conds, [B],
           extra=[(tuple(CC), lambda *cs: all(cs.count(c) == 3 for c in "RUG"))])
at = inv(S, B)
kol = {b: S[f"c{S[b]}"] for b in B}
assert [(at[i], kol[at[i]]) for i in range(1, 10)] == [
    ("M", "R"), ("X", "U"), ("D", "G"), ("S", "R"), ("J", "G"), ("B", "U"), ("Q", "R"), ("V", "G"), ("G", "U")]
n_ = sum(1 for b in B if kol[b] == "G" and S[b] < S["Q"])
assert n_ == 2
c_, w_ = bal(n_)
alone(BOX, BWC, "Advanced",
      "Nine boxes B, D, G, J, M, Q, S, V and X are kept one above another in a single stack (position 1 is the bottom "
      "and 9 the top). Three of them are Red, three Blue and three Green.", conds,
      "How many Green boxes are kept below Box Q?", c_, w_, "Fix the Red pattern first",
      "J = 5 (Green), B = 6 (Blue), M = 1 (Red). Red boxes are three apart starting at 1: Red at 1, 4 and 7. Q and S "
      "are Red with Q above, so S = 4 and Q = 7. G = 9, and position 8 is Green. D lies between X and S; the free "
      "positions are 2, 3 and 8, so X = 2, D = 3, V = 8. X has B's colour (Blue). D (3) sits between Blue X and Red S, "
      "and Blue and Green are each one short: D is Green, and G (above Green V) is Blue. Green boxes: D (3), J (5), "
      "V (8); two of them are below Q (7).",
      ["J 5 Green, B 6 Blue, M 1 Red", "Red at 1, 4, 7 ⇒ S 4, Q 7", "G 9; position 8 Green",
       "D between X and S with free 2, 3, 8 ⇒ X 2, D 3, V 8", "X Blue (as B); G Blue (above Green 8); D Green",
       "Green: 3, 5, 8 ⇒ below Q (7): two"], natural=by_num, sec=120)


# ################################################################################################ BATCH 010
begin("010")

# ---- 10LB1 Basic (standalone): six persons facing north
P = ["Abha", "Babli", "Chhotu", "Dabbu", "Eva", "Fanny"]
conds = [
    ("Only two persons sit to the right of Abha.", ("Abha",), lambda a: a == 4),
    ("Dabbu sits at the extreme right end, and Chhotu sits between Abha and Dabbu.", ("Dabbu", "Chhotu", "Abha"),
     lambda d, c, a: d == 6 and a < c < d),
    ("Eva sits at the extreme left end, and Fanny sits immediately to the left of Abha.", ("Eva", "Fanny", "Abha"),
     lambda e, f, a: e == 1 and f == a - 1),
]
S = unique(P, {p: range(1, 7) for p in P}, conds, [P])
at = inv(S, P)
assert [at[i] for i in range(1, 7)] == ["Eva", "Babli", "Fanny", "Abha", "Chhotu", "Dabbu"]
alone(LIN, SGL, "Basic",
      "Six persons Abha, Babli, Chhotu, Dabbu, Eva and Fanny sit in a straight row, all facing north. (Facing north, "
      "the right is towards the east.)", conds, "Who sits second to the left of Abha?", at[S["Abha"] - 2],
      ["Fanny", "Eva", "Chhotu"], "'Only two persons to the right' fixes a seat",
      "With six seats and two persons to her right, Abha is in seat 4. Dabbu = 6, Chhotu = 5, Eva = 1, Fanny = 3, and "
      "Babli takes seat 2 — second to Abha's left.",
      ["Abha = 4 (two persons to her right)", "Dabbu 6, Chhotu 5, Eva 1, Fanny 3", "Babli = 2 = second to Abha's left"],
      why="Fanny is immediately to her left, Eva third to her left, and Chhotu to her right.", sec=45)

# ---- 10LB2 Basic (standalone): seven persons facing north
P = ["Karan", "Lekha", "Megha", "Nikki", "Pari", "Raju", "Sunny"]
conds = [
    ("Megha sits fourth from the left end, and Raju sits second to the right of Megha.", ("Megha", "Raju"),
     lambda m, r: m == 4 and r == m + 2),
    ("Karan sits at the extreme left end and Sunny at the extreme right end.", ("Karan", "Sunny"),
     lambda k, s: k == 1 and s == 7),
    ("Pari sits immediately to the left of Megha.", ("Pari", "Megha"), lambda p, m: p == m - 1),
    ("Lekha sits to the right of Nikki.", ("Lekha", "Nikki"), lambda l, n: l > n),
]
S = unique(P, {p: range(1, 8) for p in P}, conds, [P])
at = inv(S, P)
assert [at[i] for i in range(1, 8)] == ["Karan", "Nikki", "Pari", "Megha", "Lekha", "Raju", "Sunny"]
n_ = S["Lekha"] - S["Karan"] - 1
assert n_ == 3
c_, w_ = bal(n_)
alone(LIN, SGL, "Basic",
      "Seven persons Karan, Lekha, Megha, Nikki, Pari, Raju and Sunny sit in a straight row, all facing north. "
      "(Facing north, the right is towards the east.)", conds, "How many persons sit between Karan and Lekha?", c_, w_,
      "Place the fixed seats, then the last pair",
      "Megha = 4, Raju = 6, Karan = 1, Sunny = 7, Pari = 3. Seats 2 and 5 remain for Nikki and Lekha; Lekha is to the "
      "right: Lekha = 5. Between seats 1 and 5 sit Nikki, Pari and Megha: three persons.",
      ["Megha 4, Raju 6, Karan 1, Sunny 7, Pari 3", "Nikki 2, Lekha 5", "Between 1 and 5 ⇒ three"],
      natural=by_num, sec=45)

# ---- 10LI1 Intermediate set (4): two facing rows of six. Row 1 faces south (right = west), Row 2 faces north
#      (right = east). Cell = 10 × row + column, columns 1..6 from the west; cell 1c faces cell 2c.
P = ["Arya", "Bhola", "Chanda", "Dhiren", "Gulab", "Hasan", "Kapil", "Lalit", "Mohan", "Nayan", "Ravi", "Tulsi"]
CELLS = [10 * r + c for r in (1, 2) for c in range(1, 7)]
RR = lambda s, k: s - k if s // 10 == 1 else s + k
fc = lambda s: s + 10 if s // 10 == 1 else s - 10
conds = [
    ("Mohan sits in Row 1, third from the east end of that row.", ("Mohan",), lambda m: m == 14),
    ("Hasan faces Mohan, and Bhola sits immediately to the right of Hasan.", ("Hasan", "Mohan", "Bhola"),
     lambda h, m, b: h == fc(m) and b == RR(h, 1)),
    ("Tulsi sits immediately to the right of Mohan, and Dhiren faces Tulsi.", ("Tulsi", "Mohan", "Dhiren"),
     lambda t, m, d: t == RR(m, 1) and d == fc(t)),
    ("Ravi sits second to the left of Mohan, and Gulab sits between Mohan and Ravi.", ("Ravi", "Mohan", "Gulab"),
     lambda r, m, g: r == RR(m, -2) and min(m, r) < g < max(m, r)),
    ("Lalit faces Ravi, and Chanda sits at one end of Row 2.", ("Lalit", "Ravi", "Chanda"),
     lambda l, r, c: l == fc(r) and c in (21, 26)),
    ("Nayan faces Arya, who sits in the row that faces south.", ("Nayan", "Arya"),
     lambda n, a: n == fc(a) and a // 10 == 1),
]
V = ["Mohan", "Hasan", "Bhola", "Tulsi", "Dhiren", "Ravi", "Gulab", "Lalit", "Chanda", "Nayan", "Arya", "Kapil"]
S = unique(V, {p: CELLS for p in P}, conds, [P])
at = inv(S, P)
assert [[at[10 * r + c] for c in range(1, 7)] for r in (1, 2)] == [
    ["Kapil", "Arya", "Tulsi", "Mohan", "Gulab", "Ravi"], ["Chanda", "Nayan", "Dhiren", "Hasan", "Bhola", "Lalit"]]
ARR = ("West to east — Row 1 (facing south): " + ", ".join(at[10 + c] for c in range(1, 7)) +
       "; Row 2 (facing north): " + ", ".join(at[20 + c] for c in range(1, 7)))
puzzle(LIN, DBL, "Intermediate", "Twelve persons in two facing rows of six",
       "Twelve persons Arya, Bhola, Chanda, Dhiren, Gulab, Hasan, Kapil, Lalit, Mohan, Nayan, Ravi and Tulsi sit in two "
       "parallel rows of six seats each. The persons in Row 1 face south and those in Row 2 face north, so each person "
       "faces exactly one person of the other row. (Facing south, the right is towards the west; facing north, the "
       "right is towards the east.)", conds,
       "Number the columns 1 to 6 from the west in both rows.\n"
       "Step 1: Mohan = Row 1, column 4. Hasan faces him: Row 2, column 4; Bhola, to Hasan's right (east): Row 2, "
       "column 5.\n"
       "Step 2: Tulsi, to Mohan's right (west): Row 1, column 3; Dhiren faces her: Row 2, column 3.\n"
       "Step 3: Ravi, second to Mohan's left (east): Row 1, column 6; Gulab between them: column 5. Lalit faces Ravi: "
       "Row 2, column 6, so Chanda is at the other end: Row 2, column 1.\n"
       "Step 4: Free seats: Row 1 columns 1 and 2, Row 2 column 2. Nayan faces Arya, so they take the facing pair "
       "Row 2 column 2 and Row 1 column 2; Arya is in the south-facing Row 1, so Nayan is in Row 2, and Kapil gets Row 1, column 1.\n\n"
       + table(["Column", "Row 1 (facing south)", "Row 2 (facing north)"],
               [(c, at[10 + c], at[20 + c]) for c in range(1, 7)]), ARR)
ans = at[fc(S["Kapil"])]
assert ans == "Chanda"
ask("Who faces Kapil?", ans, ["Nayan", "Lalit", "Dhiren"], "Facing persons share a column",
    "Kapil is in Row 1, column 1; facing him is Row 2, column 1: Chanda.", ["Kapil = Row 1, col 1", "Faces Row 2, col 1"],
    why="Nayan faces Arya, Lalit faces Ravi and Dhiren faces Tulsi.", sec=55)
ans = at[RR(S["Nayan"], 2)]
assert ans == "Hasan"
ask("Who sits second to the right of Nayan?", ans, ["Chanda", "Bhola", "Dhiren"], "Row 2 faces north: right = east",
    "Nayan is in Row 2, column 2; two seats east is column 4: Hasan.", ["Nayan = Row 2, col 2", "2 + 2 = col 4 ⇒ Hasan"],
    why="Dhiren is immediately to his right, Bhola third to his right, and Chanda to his left.", sec=55)
ans = at[RR(S["Gulab"], -1)]
assert ans == "Ravi"
ask("Who sits immediately to the left of Gulab?", ans, ["Mohan", "Bhola", "Lalit"], "Row 1 faces south: left = east",
    "Gulab is in Row 1, column 5, facing south; his left is east: column 6, Ravi.",
    ["Gulab = Row 1, col 5", "Left = east ⇒ col 6 = Ravi"],
    why="Mohan is to his right; Bhola faces him; Lalit is in the other row.", sec=55)
n_ = abs(S["Arya"] - S["Ravi"]) - 1
assert n_ == 3
c_, w_ = bal(n_)
ask("How many persons sit between Arya and Ravi?", c_, w_, "Count within one row",
    "Arya is in Row 1, column 2 and Ravi in Row 1, column 6: Tulsi, Mohan and Gulab sit between them.",
    ["Arya col 2, Ravi col 6 (Row 1)", "Between: cols 3, 4, 5 ⇒ three"], natural=by_num, sec=50)

# ---- 10LI2 Intermediate set (4): ten seats in a row, seven persons, three vacant seats; all face north
P = ["Anvi", "Bhim", "Chiru", "Dolu", "Esha", "Fuzail", "Gita"]
conds = [
    ("Anvi sits on seat 6, and Chiru sits immediately to the right of Anvi.", ("Anvi", "Chiru"),
     lambda a, c: a == 6 and c == 7),
    ("Bhim sits at the extreme left end, and Dolu at the extreme right end.", ("Bhim", "Dolu"),
     lambda b, d: b == 1 and d == 10),
    ("Fuzail sits immediately to the left of Dolu.", ("Fuzail", "Dolu"), lambda f, d: f == d - 1),
    ("Esha and Gita sit in adjacent seats, Esha to the left of Gita, and exactly one seat lies between Bhim and Esha.",
     ("Esha", "Gita", "Bhim"), lambda e, g, b: g == e + 1 and e == b + 2),
]
S = unique(P, {p: range(1, 11) for p in P}, conds, [P])
at = inv(S, P)
vac = [s for s in range(1, 11) if s not in at]
assert vac == [2, 5, 8] and [at.get(s) for s in (1, 3, 4, 6, 7, 9, 10)] == ["Bhim", "Esha", "Gita", "Anvi", "Chiru",
                                                                             "Fuzail", "Dolu"]
ARR = "Seats 1 to 10 from the left: " + ", ".join(at.get(s, "vacant") for s in range(1, 11))
puzzle(LIN, SGL, "Intermediate", "Ten seats, seven persons",
       "Ten seats are placed in a straight row and numbered 1 to 10 from the left end. Seven persons Anvi, Bhim, Chiru, "
       "Dolu, Esha, Fuzail and Gita sit on seven of them, all facing north; the other three seats are vacant. "
       "Positions such as 'second to the right' count seats, including vacant ones.", conds,
       "Step 1: Anvi = 6, Chiru = 7, Bhim = 1, Dolu = 10, Fuzail = 9.\n"
       "Step 2: One seat lies between Bhim (1) and Esha: Esha = 3, and Gita, immediately to her right, = 4.\n"
       "Step 3: The vacant seats are 2, 5 and 8.\n\n"
       + table(["Seat", "Person"], [(s, at.get(s, "vacant")) for s in range(1, 11)]), ARR)
n_ = sum(1 for v in vac if S["Bhim"] < v < S["Anvi"])
assert n_ == 2
c_, w_ = bal(n_)
ask("How many vacant seats lie between Bhim and Anvi?", c_, w_, "Mark the vacant seats after placing everyone",
    "Bhim is on seat 1 and Anvi on seat 6; seats 2 and 5 between them are vacant.",
    ["Vacant: 2, 5, 8", "Between 1 and 6: 2 and 5 ⇒ two"], natural=by_num, sec=55)
ans = at[S["Fuzail"] - 3]
assert ans == "Anvi"
ask("Who sits third to the left of Fuzail?", ans, ["Chiru", "Gita", "Dolu"], "Count seats, including vacant ones",
    "Fuzail is on seat 9; three seats to the left is seat 6: Anvi.", ["Fuzail = 9", "9 − 3 = seat 6 ⇒ Anvi"],
    why="Chiru is second to his left (seat 8 is vacant, seat 7 is Chiru's); Gita is further left; Dolu is to his "
        "right.", sec=55)
t, f = one_true([("Seat 5", 5 in vac), ("Seat 4", 4 in vac), ("Seat 7", 7 in vac), ("Seat 3", 3 in vac)])
ask("Which of the following seats is vacant?", t, f, "Place all seven persons first",
    "The persons occupy seats 1, 3, 4, 6, 7, 9 and 10, so seats 2, 5 and 8 are vacant.",
    ["Occupied: 1, 3, 4, 6, 7, 9, 10", "Vacant: 2, 5, 8 ⇒ seat 5"],
    why="Gita is on seat 4, Chiru on 7 and Esha on 3.", sec=50)
n2 = sum(1 for p in P if S[p] > S["Gita"])
assert n2 == 4
c_, w_ = bal(n2)
ask("How many persons sit to the right of Gita?", c_, w_, "Count persons, not seats",
    "Gita is on seat 4; to her right sit Anvi (6), Chiru (7), Fuzail (9) and Dolu (10).",
    ["Gita = 4", "Persons on 6, 7, 9, 10 ⇒ four"], natural=by_num, sec=50)

# ---- 10LA Advanced set (3): eight persons facing north, ranked by height (1 = tallest)
P = ["Hiran", "Ishu", "Kuku", "Lado", "Mitu", "Nanki", "Pammi", "Rinku"]
H = ["h" + p for p in P]
conds = [
    ("Lado and Pammi sit at the two ends of the row, Lado at the left end.", ("Lado", "Pammi"),
     lambda l, p: l == 1 and p == 8),
    ("The tallest person sits immediately to the right of Lado, and the shortest person sits immediately to the "
     "right of the tallest person.", (*P, *H),
     lambda *x: x[8 + x[:8].index(2)] == 1 and x[8 + x[:8].index(3)] == 8),
    ("Nanki is the second tallest and sits second to the right of the tallest person.", ("Nanki", "hNanki"),
     lambda n, h: n == 4 and h == 2),
    ("Hiran sits second to the right of Nanki and is shorter than only Kuku and Nanki.", ("Hiran", "Nanki", "hHiran"),
     lambda hi, n, h: hi == n + 2 and h == 3),
    ("Kuku is taller than Nanki.", ("hKuku", "hNanki"), lambda k, n: k < n),
    ("Ishu sits immediately to the left of Hiran, and Rinku immediately to the right of Hiran.",
     ("Ishu", "Rinku", "Hiran"), lambda i, r, h: i == h - 1 and r == h + 1),
    ("Ishu is shorter than everyone except the shortest person; Rinku is taller than Lado, and Lado is taller than "
     "Pammi.", ("hIshu", "hRinku", "hLado", "hPammi"), lambda i, r, l, p: i == 7 and r < l < p),
]
V = ["Lado", "Pammi", "Nanki", "Hiran", "Ishu", "Rinku", "Kuku", "Mitu"] + H
S = unique(V, {p: range(1, 9) for p in P} | {h: range(1, 9) for h in H}, conds, [P, H])
at = inv(S, P)
hr = {p: S["h" + p] for p in P}
assert [(at[i], hr[at[i]]) for i in range(1, 9)] == [
    ("Lado", 5), ("Kuku", 1), ("Mitu", 8), ("Nanki", 2), ("Ishu", 7), ("Hiran", 3), ("Rinku", 4), ("Pammi", 6)]
ARR = "Left to right (height rank, 1 = tallest): " + ", ".join(f"{at[i]} ({hr[at[i]]})" for i in range(1, 9))
puzzle(LIN, SGL, "Advanced", "Eight persons in a row, ranked by height",
       "Eight persons Hiran, Ishu, Kuku, Lado, Mitu, Nanki, Pammi and Rinku sit in a straight row, all facing north. No "
       "two of them are of the same height. (Facing north, the right is towards the east.)", conds,
       "Number the seats 1 to 8 from the left.\n"
       "Step 1: Lado = 1, Pammi = 8. The tallest person is on seat 2 and the shortest on seat 3. Nanki (2nd tallest) "
       "= 4, Hiran (3rd tallest) = 6, Ishu = 5, Rinku = 7.\n"
       "Step 2: Kuku and Mitu take seats 2 and 3. Kuku is taller than Nanki, the second tallest, so Kuku is the "
       "tallest (seat 2) and Mitu the shortest (seat 3).\n"
       "Step 3: Ranks 4 to 7 remain for Ishu, Rinku, Lado and Pammi. Ishu is 7th; Rinku > Lado > Pammi in height: "
       "Rinku 4th, Lado 5th, Pammi 6th.\n\n"
       + table(["Seat", "Person", "Height rank"], [(i, at[i], hr[at[i]]) for i in range(1, 9)]), ARR)
ans = next(p for p in P if hr[p] == 4)
assert ans == "Rinku"
ask("Who is the fourth tallest?", ans, ["Lado", "Ishu", "Hiran"], "Order the last four with the comparison chain",
    "Kuku, Nanki and Hiran are the three tallest. Of the rest, Ishu is 7th and Rinku is taller than Lado, who is "
    "taller than Pammi, so Rinku is 4th.", ["Top three: Kuku, Nanki, Hiran", "Ishu 7th, Mitu 8th",
                                            "Rinku > Lado > Pammi ⇒ Rinku 4th"],
    why="Lado is 5th, Ishu 7th and Hiran 3rd.", sec=90)
cnt = sum(1 for s in range(2, 8) if hr[at[s]] < hr[at[s - 1]] and hr[at[s]] < hr[at[s + 1]])
assert cnt == 3
c_, w_ = bal(cnt)
ask("Among the persons who have two neighbours, how many are taller than both of their neighbours?", c_, w_,
    "Compare each person with both neighbours",
    "Kuku (taller than Lado and Mitu), Nanki (taller than Mitu and Ishu) and Hiran (taller than Ishu and Rinku) "
    "qualify; nobody else does.", ["Kuku 1 vs 5, 8 ✓", "Nanki 2 vs 8, 7 ✓", "Hiran 3 vs 7, 4 ✓",
                                    "Mitu, Ishu, Rinku ✗"], natural=by_num, sec=90)
ans = at[S[next(p for p in P if hr[p] == 7)] - 1]
assert ans == "Nanki"
ask("Who sits immediately to the left of the second shortest person?", ans, ["Hiran", "Mitu", "Kuku"],
    "Find the person by rank, then move left", "Ishu is the second shortest and sits on seat 5; seat 4, to the left, "
    "is Nanki's.", ["Second shortest = Ishu (seat 5)", "Seat 4 = Nanki"],
    why="Hiran is to Ishu's right; Mitu and Kuku are further left.", sec=80)


# ---- 10CB Basic (standalone): six persons facing the centre (Tina fixed at 0)
P = ["Tina", "Umesh", "Vimla", "Waris", "Yusuf", "Zarna"]
conds = [
    ("Umesh sits immediately to the right of Tina, and Yusuf sits opposite Umesh.", ("Umesh", "Yusuf"),
     lambda u, y: u == 1 and y == R6(u, 3)),
    ("Vimla sits second to the left of Yusuf.", ("Vimla", "Yusuf"), lambda v, y: v == R6(y, -2)),
    ("Zarna does not sit next to Tina.", ("Zarna",), lambda z: z not in (1, 5)),
]
S = unique(P, {"Tina": [0]} | {p: range(6) for p in P[1:]}, conds, [P])
at = inv(S, P)
assert [at[i] for i in range(6)] == ["Tina", "Umesh", "Vimla", "Zarna", "Yusuf", "Waris"]
alone(CIR, CEN, "Basic",
      "Six friends Tina, Umesh, Vimla, Waris, Yusuf and Zarna sit around a circular table, equally spaced and all "
      "facing the centre. (Facing the centre, the right is anticlockwise and the left clockwise.)", conds,
      "Who sits immediately to the left of Tina?", at[5], ["Umesh", "Zarna", "Yusuf"],
      "Fix one person and go round",
      "Seats 0 to 5 anticlockwise from Tina: Umesh = 1, Yusuf (opposite) = 4, Vimla (second to Yusuf's left, "
      "clockwise) = 2. Seats 3 and 5 remain; seat 5 is next to Tina, so Zarna = 3 and Waris = 5. Tina's left "
      "(clockwise) neighbour is seat 5: Waris.",
      ["Tina 0, Umesh 1, Yusuf 4, Vimla 2", "Zarna not next to Tina ⇒ Zarna 3, Waris 5", "Left of Tina = seat 5 ⇒ Waris"],
      why="Umesh is on Tina's right; Zarna and Yusuf are not her neighbours.", sec=45)

# ---- 10CI1 Intermediate set (5): ten chairs, eight persons, two vacant chairs; all face the centre (Ajay at 0)
P = ["Ajay", "Bimal", "Disha", "Fateh", "Jassi", "Lucky", "Rupal", "Ujjal"]
R10 = lambda s, k: (s + k) % 10
conds = [
    ("Jassi sits opposite Ajay, and Bimal sits immediately to the left of Jassi.", ("Jassi", "Bimal"),
     lambda j, b: j == 5 and b == R10(j, -1)),
    ("Rupal sits immediately to the right of Ajay. Fateh sits second to the right of Rupal, and the chair between "
     "Rupal and Fateh is vacant.", ("Rupal", "Fateh", *[p for p in P if p not in ("Rupal", "Fateh")]),
     lambda r, f, *o: r == 1 and f == R10(r, 2) and R10(r, 1) not in o),
    ("Lucky sits immediately to the left of Ajay, and Disha sits immediately to the left of Lucky.",
     ("Lucky", "Disha"), lambda l, d: l == 9 and d == 8),
    ("Ujjal sits immediately to the right of Jassi.", ("Ujjal", "Jassi"), lambda u, j: u == R10(j, 1)),
    ("The two vacant chairs are exactly opposite each other.", tuple(P),
     lambda *x: (lambda v: len(v) == 2 and R10(v[0], 5) == v[1])([c for c in range(10) if c not in x])),
]
S = unique(["Ajay", "Jassi", "Bimal", "Lucky", "Disha", "Ujjal", "Rupal", "Fateh"],
           {"Ajay": [0]} | {p: range(10) for p in P[1:]}, conds, [P])
at = inv(S, P)
vac = [c for c in range(10) if c not in at]
assert vac == [2, 7] and [at.get(i) for i in (0, 1, 3, 4, 5, 6, 8, 9)] == [
    "Ajay", "Rupal", "Fateh", "Bimal", "Jassi", "Ujjal", "Disha", "Lucky"]
ARR = "Chairs anticlockwise from Ajay: " + ", ".join(at.get(i, "vacant") for i in range(10))
puzzle(CIR, CEN, "Intermediate", "Ten chairs, eight persons",
       "Ten chairs are placed around a circular table, equally spaced. Eight persons Ajay, Bimal, Disha, Fateh, Jassi, "
       "Lucky, Rupal and Ujjal sit on eight of them, all facing the centre; two chairs are vacant. Positions such as "
       "'second to the right' count chairs, including vacant ones. (Facing the centre, the right is anticlockwise.)",
       conds,
       "Number the chairs 0 to 9 anticlockwise from Ajay.\n"
       "Step 1: Jassi = 5 (opposite), Bimal = 4 (Jassi's left, clockwise), Ujjal = 6.\n"
       "Step 2: Rupal = 1, chair 2 is vacant, Fateh = 3.\n"
       "Step 3: Lucky = 9, Disha = 8. The only chair left is 7, which is vacant — and it is exactly opposite chair 2, "
       "as required.\n\n" + table(["Chair", "Person"], [(i, at.get(i, "vacant")) for i in range(10)]), ARR)
ans = at[R10(S["Rupal"], 5)]
assert ans == "Ujjal"
ask("Who sits opposite Rupal?", ans, ["Jassi", "Bimal", "Disha"], "Opposite = five chairs away",
    "Rupal is on chair 1; chair 6 is opposite: Ujjal.", ["Rupal = 1", "1 + 5 = 6 ⇒ Ujjal"],
    why="Jassi is opposite Ajay, Bimal is opposite Lucky, and Disha is opposite Fateh.", sec=50)
ans = at[R10(S["Fateh"], -2)]
assert ans == "Rupal"
ask("Who sits second to the left of Fateh?", ans, ["Ajay", "Bimal", "Lucky"], "Count the vacant chair as well",
    "Fateh is on chair 3; his left is clockwise: chair 2 (vacant), then chair 1, Rupal.",
    ["Fateh = 3", "Clockwise: 2 (vacant), 1 ⇒ Rupal"],
    why="Ajay is third to his left, Bimal is to his right, and Lucky is further clockwise.", sec=55)
n_ = sum(1 for c in range(1, S["Bimal"]) if c in at)
assert n_ == 2
c_, w_ = bal(n_)
ask("How many persons sit between Ajay and Bimal, counting from Ajay's right?", c_, w_,
    "Count persons, skipping vacant chairs", "From Ajay (0) anticlockwise: Rupal (1), vacant (2), Fateh (3), then "
    "Bimal (4). Two persons sit between them.", ["Chairs 1, 2, 3 lie between", "Chair 2 is vacant ⇒ two persons"],
    natural=by_num, sec=55)
ans = at[R10(7, 1)]
assert ans == "Disha"
ask("Who sits immediately to the right of the vacant chair that is next to Ujjal?", ans, ["Lucky", "Jassi", "Fateh"],
    "A vacant chair has a 'right' as seen by a person facing the centre from it",
    "The vacant chair next to Ujjal is chair 7. Facing the centre from it, the right is anticlockwise: chair 8, "
    "Disha.", ["Vacant chairs: 2 and 7; chair 7 is next to Ujjal (6)", "Chair 8 ⇒ Disha"],
    why="Lucky is two chairs from it, Jassi is next to Ujjal on the other side, and Fateh is beside the other vacant "
        "chair.", sec=60)
t, f = one_true([("Bimal sits opposite Lucky", R10(S["Bimal"], 5) == S["Lucky"]),
                 ("Disha sits immediately to the right of Ujjal", S["Disha"] == R10(S["Ujjal"], 1)),
                 ("Fateh sits opposite Jassi", R10(S["Fateh"], 5) == S["Jassi"]),
                 ("Both vacant chairs are next to Rupal", all(abs(v - S["Rupal"]) in (1, 9) for v in vac))])
ask("Which of the following statements is true?", t, f, "Checking each statement against the arrangement",
    "Bimal is on chair 4 and Lucky on chair 9: 4 + 5 = 9, so they sit opposite each other.",
    ["Bimal 4 ↔ 9 Lucky ✓", "Ujjal's right is chair 7, which is vacant ✗", "Fateh 3 ↔ 8 Disha ✗",
     "Only chair 2 is next to Rupal; chair 7 is not ✗"],
    why="A vacant chair is to Ujjal's right, Fateh faces Disha, and only one vacant chair touches Rupal.", sec=55)

# ---- 10CI2 Intermediate set (4): seven persons, some facing the centre and some outside (Rohit at 0)
P = ["Rohit", "Saloni", "Tanuj", "Urvi", "Vedika", "Xena", "Yuvi"]
F7 = ["f" + p for p in P]
C7 = lambda s, f, k: CR(s, f, k, 7)
conds = [
    ("Rohit faces the centre, and Urvi sits immediately to his right.", ("fRohit", "Urvi"),
     lambda f, u: f == "C" and u == C7(0, f, 1)),
    ("Urvi faces outside, and Yuvi sits immediately to Urvi's left.", ("fUrvi", "Yuvi", "Urvi"),
     lambda f, y, u: f == "O" and y == C7(u, f, -1)),
    ("Saloni sits immediately to the right of Yuvi, and the two of them face opposite directions.",
     ("Saloni", "Yuvi", "fYuvi", "fSaloni"), lambda s, y, fy, fs: s == C7(y, fy, 1) and fy != fs),
    ("Vedika sits immediately to the left of Rohit and faces the same direction as Rohit.",
     ("Vedika", "fVedika", "fRohit"), lambda v, fv, fr: v == C7(0, fr, -1) and fv == fr),
    ("Tanuj sits immediately to the left of Vedika.", ("Tanuj", "Vedika", "fVedika"),
     lambda t, v, f: t == C7(v, f, -1)),
    ("Xena faces the centre, Xena and Tanuj face opposite directions, and Yuvi faces the same direction as Xena.",
     ("fXena", "fTanuj", "fYuvi"), lambda x, t, y: x == "C" and t != x and y == x),
]
V = ["fRohit", "Urvi", "fUrvi", "Yuvi", "fYuvi", "Saloni", "fSaloni", "Vedika", "fVedika", "Tanuj", "fXena", "fTanuj",
     "Xena"]
S = unique(V, {"Xena": range(7)} | {p: range(1, 7) for p in P if p != "Rohit"} | {f: "CO" for f in F7},
           conds, [[p for p in P if p != "Rohit"]], extra=[(("Xena",), lambda x: x != 0)])
S["Rohit"] = 0
at = inv(S, P)
fc7 = {p: S["f" + p] for p in P}
assert [(at[i], fc7[at[i]]) for i in range(7)] == [
    ("Rohit", "C"), ("Urvi", "O"), ("Yuvi", "C"), ("Saloni", "O"), ("Xena", "C"), ("Tanuj", "O"), ("Vedika", "C")]
ARR = "Anticlockwise from Rohit: " + ", ".join(f"{at[i]} ({FCN[fc7[at[i]]]})" for i in range(7))
puzzle(CIR, INOUT, "Intermediate", "Seven persons facing in or out",
       "Seven persons Rohit, Saloni, Tanuj, Urvi, Vedika, Xena and Yuvi sit around a circular table, equally spaced. "
       "Some of them face the centre and the others face outside. (Facing the centre, the right is anticlockwise; "
       "facing outside, it is clockwise.)", conds,
       "Number the seats 0 to 6 anticlockwise from Rohit.\n"
       "Step 1: Rohit faces the centre: Urvi = 1. Urvi faces outside, so her left is anticlockwise: Yuvi = 2.\n"
       "Step 2: Vedika, on Rohit's left (clockwise), = 6 and faces the centre. Tanuj, on Vedika's left, = 5.\n"
       "Step 3: Xena faces the centre; Yuvi faces the same way (centre), Tanuj the other way (outside). Saloni faces "
       "opposite to Yuvi (outside) and sits on Yuvi's right (anticlockwise): 3. Xena takes seat 4.\n\n"
       + table(["Seat", "Person", "Facing"], [(i, at[i], FCN[fc7[at[i]]]) for i in range(7)]), ARR)
ans = at[C7(S["Saloni"], "O", 2)]
assert ans == "Urvi"
ask("Who sits second to the right of Saloni?", ans, ["Xena", "Tanuj", "Rohit"], "Saloni faces outside",
    "Saloni (seat 3) faces outside, so her right is clockwise: seat 2 (Yuvi), then seat 1 (Urvi).",
    ["Saloni = 3, faces outside ⇒ right = clockwise", "3 → 2 → 1 ⇒ Urvi"],
    why="Xena and Tanuj are on her left; Rohit is third to her right.", sec=60)
ans = at[C7(S["Tanuj"], "O", -1)]
assert ans == "Vedika"
ask("Who sits immediately to the left of Tanuj?", ans, ["Xena", "Rohit", "Saloni"], "Tanuj faces outside",
    "Tanuj (seat 5) faces outside, so his left is anticlockwise: seat 6, Vedika.",
    ["Tanuj = 5, faces outside ⇒ left = anticlockwise", "Seat 6 = Vedika"],
    why="Xena is on his right; Rohit and Saloni are not his neighbours.", sec=55)
n_ = list(fc7.values()).count("O")
assert n_ == 3
c_, w_ = bal(n_)
ask("How many persons face outside?", c_, w_, "Collect every facing clue",
    "Urvi, Saloni and Tanuj face outside; Rohit, Yuvi, Xena and Vedika face the centre.",
    ["Outside: Urvi, Saloni, Tanuj", "Centre: Rohit, Yuvi, Xena, Vedika"], natural=by_num, sec=55)
ans = at[C7(S["Urvi"], "O", 3)]
assert ans == "Tanuj"
ask("Who sits third to the right of Urvi?", ans, ["Vedika", "Xena", "Yuvi"], "Urvi faces outside",
    "Urvi (seat 1) faces outside, so her right is clockwise: seat 0 (Rohit), 6 (Vedika), 5 (Tanuj).",
    ["Urvi = 1 ⇒ clockwise 0, 6, 5", "Third = Tanuj"],
    why="Vedika is second to her right, Yuvi is to her left, and Xena is further anticlockwise.", sec=60)

# ---- 10CA Advanced (standalone): eight persons; every centre-facing person sits opposite an outside-facing person
P = ["Ambar", "Chitti", "Dhruva", "Garima", "Hoshang", "Jalaj", "Mukta", "Navami"]
F8 = ["f" + p for p in P]
conds = [
    ("Ambar faces the centre, and Dhruva sits opposite Ambar.", ("fAmbar", "Dhruva"),
     lambda f, d: f == "C" and d == 4),
    ("Garima faces outside and sits immediately to the right of Ambar.", ("fGarima", "Garima", "fAmbar"),
     lambda fg, g, fa: fg == "O" and g == CR(0, fa, 1, 8)),
    ("Jalaj sits immediately to the left of Garima, and Mukta sits opposite Garima.", ("Jalaj", "Garima", "fGarima",
                                                                                        "Mukta"),
     lambda j, g, fg, m: j == CR(g, fg, -1, 8) and m == R8(g, 4)),
    ("Hoshang sits second to the left of Dhruva, and Chitti sits immediately to the left of Ambar.",
     ("Hoshang", "Dhruva", "fDhruva", "Chitti", "fAmbar"),
     lambda h, d, fd, c, fa: h == CR(d, fd, -2, 8) and c == CR(0, fa, -1, 8)),
    ("Chitti faces outside, and Jalaj and Navami face the same direction.", ("fChitti", "fJalaj", "fNavami"),
     lambda c, j, n: c == "O" and j == n),
]
OPP = (tuple(P) + tuple(F8), lambda *x: all(x[8 + i] != x[8 + x[:8].index(R8(x[i], 4))] for i in range(8)))
S = unique(["Ambar"] + F8 + ["Dhruva", "Garima", "Jalaj", "Mukta", "Hoshang", "Chitti", "Navami"],
           {"Ambar": [0]} | {p: range(8) for p in P[1:]} | {f: "CO" for f in F8}, conds, [P], extra=[OPP])
at = inv(S, P)
fc8 = {p: S["f" + p] for p in P}
assert [(at[i], fc8[at[i]]) for i in range(8)] == [
    ("Ambar", "C"), ("Garima", "O"), ("Jalaj", "C"), ("Navami", "C"), ("Dhruva", "O"), ("Mukta", "C"),
    ("Hoshang", "O"), ("Chitti", "O")]
ans = at[CR(S["Navami"], "C", 2, 8)]
assert ans == "Mukta"
alone(CIR, INOUT, "Advanced",
      "Eight persons Ambar, Chitti, Dhruva, Garima, Hoshang, Jalaj, Mukta and Navami sit around a circular table, "
      "equally spaced. Some face the centre and the others face outside, and every person sits exactly opposite a "
      "person who faces the other way. (Facing the centre, the right is anticlockwise; facing outside, it is "
      "clockwise.)", conds, "Who sits second to the right of Navami?", ans, ["Hoshang", "Dhruva", "Garima"],
      "Opposite persons face opposite ways — use this to fix facings",
      "Seats 0 to 7 anticlockwise from Ambar (centre): Dhruva 4 faces outside (opposite Ambar). Garima (outside) = 1, "
      "so Mukta (opposite) = 5 faces the centre. Garima's left is anticlockwise: Jalaj = 2. Dhruva faces outside, so "
      "his left is anticlockwise: Hoshang = 6. Chitti, on Ambar's left (clockwise), = 7 and faces outside, so Navami "
      "(3, opposite Chitti) faces the centre, and Jalaj faces the centre like Navami (and Hoshang, opposite Jalaj, "
      "faces outside). Navami faces the centre, so second to her right (anticlockwise) is seat 5: Mukta.",
      ["Ambar 0 (C), Dhruva 4 (O)", "Garima 1 (O) ⇒ Mukta 5 (C); Jalaj 2", "Hoshang 6, Chitti 7 (O), Navami 3",
       "Chitti O ⇒ Navami C ⇒ Jalaj C ⇒ Hoshang O", "Navami (3, centre) ⇒ anticlockwise 4, 5 ⇒ Mukta"],
      why="Dhruva is immediately to her right; Hoshang third to her right; Garima is to her left.", sec=120)


# ---- 10F1 Basic set (5): six floors and six hobbies
P = ["Bablu", "Chameli", "Dinu", "Ganesh", "Heena", "Jagan"]
HB = ["Dancing", "Painting", "Reading", "Singing", "Swimming", "Writing"]
conds = [
    ("Chameli lives on floor 4, Bablu immediately above her and Jagan immediately below her.",
     ("Chameli", "Bablu", "Jagan"), lambda c, b, j: c == 4 and b == 5 and j == 3),
    ("Dinu lives on the topmost floor, and Heena lives below Ganesh.", ("Dinu", "Heena", "Ganesh"),
     lambda d, h, g: d == 6 and h < g),
    ("The person who likes Painting lives on an even-numbered floor between Jagan and Bablu.",
     ("Painting", "Jagan", "Bablu"), lambda p, j, b: p % 2 == 0 and j < p < b),
    ("The person on the topmost floor likes Singing, and the person on floor 1 likes Reading.",
     ("Singing", "Reading"), lambda s, r: s == 6 and r == 1),
    ("The person who likes Dancing lives immediately below the person who likes Painting.", ("Dancing", "Painting"),
     lambda d, p: d == p - 1),
    ("Bablu does not like Swimming.", ("Bablu", "Swimming"), lambda b, s: b != s),
]
S = unique(P + HB, {v: range(1, 7) for v in P + HB}, conds, [P, HB])
at, hob = inv(S, P), inv(S, HB)
hof = {p: hob[S[p]] for p in P}
assert [(at[i], hob[i]) for i in range(1, 7)] == [("Heena", "Reading"), ("Ganesh", "Swimming"), ("Jagan", "Dancing"),
                                                    ("Chameli", "Painting"), ("Bablu", "Writing"), ("Dinu", "Singing")]
ARR = "Bottom to top: " + ", ".join(f"floor {i} {at[i]} ({hob[i]})" for i in range(1, 7))
puzzle(FLR, FA, "Basic", "Six floors and six hobbies",
       "Six persons Bablu, Chameli, Dinu, Ganesh, Heena and Jagan live on the six floors of a building, one on each "
       "floor (floor 1 is the lowermost, floor 6 the topmost). Each has a different hobby among Dancing, Painting, "
       "Reading, Singing, Swimming and Writing.", conds,
       "Step 1: Chameli = 4, Bablu = 5, Jagan = 3, Dinu = 6. Floors 1 and 2 remain; Heena is below Ganesh: Heena = 1, "
       "Ganesh = 2.\n"
       "Step 2: Painting is on an even floor between 3 and 5: floor 4 (Chameli). Dancing is immediately below: floor "
       "3 (Jagan). Singing: floor 6 (Dinu). Reading: floor 1 (Heena).\n"
       "Step 3: Swimming and Writing remain for Ganesh and Bablu; Bablu does not swim: Bablu Writing, Ganesh "
       "Swimming.\n\n" + floors_table(6, None, lambda f: (f, at[f], hob[f]), ["Floor", "Person", "Hobby"]), ARR)
ans = at[S["Writing"]]
assert ans == "Bablu"
ask("Who likes Writing?", ans, ["Ganesh", "Chameli", "Dinu"], "The last pair by a negative clue",
    "Swimming and Writing remain for Ganesh and Bablu, and Bablu does not like Swimming, so he likes Writing.",
    ["Left: Swimming, Writing", "Bablu ≠ Swimming ⇒ Writing"],
    why="Ganesh likes Swimming, Chameli Painting and Dinu Singing.", sec=40)
ans = hof["Ganesh"]
assert ans == "Swimming"
ask("What is Ganesh's hobby?", ans, ["Writing", "Reading", "Dancing"], "Same step, the other person",
    "Of Swimming and Writing, Bablu takes Writing, so Ganesh likes Swimming.", ["Bablu = Writing ⇒ Ganesh = Swimming"],
    why="Writing is Bablu's, Reading Heena's and Dancing Jagan's hobby.", sec=40)
n_ = abs(S["Heena"] - S["Dancing"]) - 1
assert n_ == 1
c_, w_ = bal(n_)
ask("How many persons live between Heena and the person who likes Dancing?", c_, w_, "Floors strictly between",
    "Heena is on floor 1 and the Dancing lover (Jagan) on floor 3; only Ganesh lives between them.",
    ["Heena 1, Dancing = Jagan 3", "Between: floor 2 ⇒ one"], natural=by_num, sec=40)
ans = at[S["Reading"]]
assert ans == "Heena"
ask("Who likes Reading?", ans, ["Ganesh", "Jagan", "Dinu"], "Floor 1 is settled by the 'below' clue",
    "Reading is liked by the person on floor 1. Heena lives below Ganesh, so Heena is on floor 1.",
    ["Reading = floor 1", "Heena below Ganesh ⇒ Heena = 1"],
    why="Ganesh is on floor 2, Jagan on 3 and Dinu on 6.", sec=40)
t, f = one_true([("Chameli likes Dancing", hof["Chameli"] == "Dancing"),
                 ("Dinu lives immediately above the person who likes Writing", S["Dinu"] == S["Writing"] + 1),
                 ("Jagan lives on an even-numbered floor", S["Jagan"] % 2 == 0),
                 ("Heena lives immediately below Jagan", S["Heena"] == S["Jagan"] - 1)])
ask("Which of the following statements is true?", t, f, "Checking each statement against the floors",
    "The Writing lover (Bablu) is on floor 5, and Dinu lives on floor 6, immediately above him.",
    ["Chameli likes Painting ✗", "Writing = Bablu (5), Dinu 6 ✓", "Jagan is on floor 3 ✗",
     "Heena is on floor 1 and Jagan on 3 ✗"],
    why="Chameli paints, Jagan's floor is odd, and Ganesh lives between Heena and Jagan.", sec=45)

# ---- 10FI Intermediate set (4): four floors, two persons on each floor, each with a favourite colour
P = ["Arif", "Chinki", "Gudiya", "Hanif", "Lalu", "Mamta", "Pintu", "Sweety"]
CO8 = ["Amber", "Coral", "Indigo", "Lilac", "Mint", "Navy", "Rose", "Tan"]
conds = [
    ("Gudiya lives on floor 3 and likes Rose.", ("Gudiya", "Rose"), lambda g, r: g == 3 and r == "Gudiya"),
    ("Arif lives on the floor immediately above Gudiya's and likes Mint.", ("Arif", "Gudiya", "Mint"),
     lambda a, g, m: a == g + 1 and m == "Arif"),
    ("Hanif lives on an even-numbered floor below Gudiya.", ("Hanif", "Gudiya"), lambda h, g: h % 2 == 0 and h < g),
    ("Chinki and Mamta live on the same floor.", ("Chinki", "Mamta"), lambda c, m: c == m),
    ("Sweety lives above Lalu, and Pintu lives on the floor immediately below Lalu's.", ("Sweety", "Lalu", "Pintu"),
     lambda s, l, p: s > l and p == l - 1),
    ("The person who likes Navy lives on the topmost floor. Hanif likes Amber and Pintu likes Lilac.",
     ("Navy", "Amber", "Lilac", *P), lambda n, a, li, *x: x[P.index(n)] == 4 and a == "Hanif" and li == "Pintu"),
    ("The person who likes Tan lives on floor 3, and Chinki does not like Indigo.", ("Tan", "Indigo", *P),
     lambda t, i, *x: x[P.index(t)] == 3 and i != "Chinki"),
]
dom = {p: range(1, 5) for p in P} | {c: P for c in CO8}
S = unique(P + CO8, dom, conds, [CO8], extra=[(tuple(P), lambda *x: all(x.count(f) == 2 for f in range(1, 5)))])
cof = {S[c]: c for c in CO8}
fl = {p: S[p] for p in P}
assert {f: sorted(p for p in P if fl[p] == f) for f in range(1, 5)} == {
    1: ["Chinki", "Mamta"], 2: ["Hanif", "Pintu"], 3: ["Gudiya", "Lalu"], 4: ["Arif", "Sweety"]}
assert cof == {"Gudiya": "Rose", "Arif": "Mint", "Sweety": "Navy", "Hanif": "Amber", "Pintu": "Lilac",
               "Chinki": "Coral", "Mamta": "Indigo", "Lalu": "Tan"}
ARR = "Top to bottom: " + "; ".join(
    f"floor {f}: " + ", ".join(f"{p} ({cof[p]})" for p in P if fl[p] == f) for f in range(4, 0, -1))
puzzle(FLR, FA, "Intermediate", "Two persons on each of four floors, with colours",
       "Eight persons Arif, Chinki, Gudiya, Hanif, Lalu, Mamta, Pintu and Sweety live in a four-storey building, two "
       "persons on each floor (floor 1 is the lowermost, floor 4 the topmost). Each likes a different colour among "
       "Amber, Coral, Indigo, Lilac, Mint, Navy, Rose and Tan.", conds,
       "Step 1: Gudiya = 3 (Rose), Arif = 4 (Mint), Hanif = 2 (Amber).\n"
       "Step 2: Chinki and Mamta share a floor; floors 2, 3 and 4 each have only one free place, so they live on "
       "floor 1.\n"
       "Step 3: Lalu, Pintu and Sweety fill one place each on floors 2, 3 and 4. Pintu is immediately below Lalu and "
       "Sweety is above Lalu: Pintu = 2, Lalu = 3, Sweety = 4.\n"
       "Step 4: Navy is on floor 4; Arif likes Mint, so Sweety likes Navy. Pintu likes Lilac. Tan is on floor 3, where "
       "Gudiya likes Rose, so Lalu likes Tan. Coral and Indigo remain for Chinki and Mamta; Chinki does not like Indigo: Chinki Coral, Mamta Indigo.\n\n"
       + table(["Floor", "Persons (colour)"],
               [(f, ", ".join(f"{p} ({cof[p]})" for p in P if fl[p] == f)) for f in range(4, 0, -1)]), ARR)
ans = next(p for p in P if fl[p] == fl["Lalu"] and p != "Lalu")
assert ans == "Gudiya"
ask("Who lives on the same floor as Lalu?", ans, ["Sweety", "Pintu", "Arif"], "Fill the single free places in order",
    "Pintu is immediately below Lalu and Sweety above him, with one free place on each of floors 2, 3 and 4, so Lalu "
    "is on floor 3 with Gudiya.", ["Free: one place on 2, 3, 4", "Pintu 2, Lalu 3, Sweety 4", "Floor 3: Gudiya, Lalu"],
    why="Sweety and Arif are on floor 4; Pintu is on floor 2.", sec=55)
ans = cof["Sweety"]
assert ans == "Navy"
ask("Which colour does Sweety like?", ans, ["Mint", "Tan", "Lilac"], "Two persons share the top floor",
    "Navy belongs to someone on floor 4. Arif (floor 4) likes Mint, so Sweety, the other person there, likes Navy.",
    ["Floor 4: Arif, Sweety", "Arif = Mint ⇒ Sweety = Navy"],
    why="Mint is Arif's, Tan Lalu's and Lilac Pintu's colour.", sec=55)
ans = next(p for p in P if cof[p] == "Coral")
assert ans == "Chinki"
ask("Who likes Coral?", ans, ["Mamta", "Lalu", "Hanif"], "The last pair on floor 1",
    "Tan goes to Lalu (the only floor-3 person without a colour), so Coral and Indigo remain for Chinki and Mamta; Chinki does not like Indigo, so Chinki likes Coral.",
    ["Floor 1 colours: Coral, Indigo", "Chinki ≠ Indigo ⇒ Coral"],
    why="Mamta likes Indigo, Lalu Tan and Hanif Amber.", sec=55)
n_ = sum(1 for p in P if fl[p] > fl["Pintu"])
assert n_ == 4
c_, w_ = bal(n_)
ask("How many persons live above Pintu's floor?", c_, w_, "Two persons per floor",
    "Pintu lives on floor 2; floors 3 and 4 hold two persons each: four persons.",
    ["Pintu = floor 2", "Floors 3, 4 ⇒ 2 + 2 = four"], natural=by_num, sec=50)

# ---- 10FA Advanced set (6): a basement, a ground floor and floors 1-6 (levels 0-7), eight persons with professions
P = ["Abhi", "Barun", "Chaya", "Dilip", "Emily", "Feroz", "Gagan", "Harsha"]
PF = ["Actor", "Baker", "Cashier", "Doctor", "Editor", "Farmer", "Guard", "Nurse"]
LV = lambda v: "the basement" if v == 0 else "the ground floor" if v == 1 else f"floor {v - 1}"
conds = [
    ("Exactly three persons live above Emily, and Emily is the Actor.", ("Emily", "Actor"),
     lambda e, a: e == 4 and a == e),
    ("The Doctor lives two levels below Emily.", ("Doctor", "Emily"), lambda d, e: d == e - 2),
    ("Chaya lives on the ground floor, immediately above the Guard.", ("Chaya", "Guard"),
     lambda c, g: c == 1 and g == c - 1),
    ("Barun lives on the topmost floor, and Dilip lives two levels below Barun.", ("Barun", "Dilip"),
     lambda b, d: b == 7 and d == 5),
    ("Gagan lives between Dilip and Barun.", ("Gagan", "Dilip", "Barun"), lambda g, d, b: d < g < b),
    ("Feroz lives below Harsha, and Abhi lives immediately above Harsha.", ("Feroz", "Harsha", "Abhi"),
     lambda f, h, a: f < h and a == h + 1),
    ("The Nurse lives immediately above the Doctor.", ("Nurse", "Doctor"), lambda n, d: n == d + 1),
    ("The Cashier lives immediately below the Editor, and the Editor lives below the Farmer.",
     ("Cashier", "Editor", "Farmer"), lambda c, e, f: c == e - 1 and e < f),
]
S = unique(P + PF, {v: range(8) for v in P + PF}, conds, [P, PF])
at, prof = inv(S, P), inv(S, PF)
pof = {p: prof[S[p]] for p in P}
assert [(at[i], prof[i]) for i in range(8)] == [
    ("Feroz", "Guard"), ("Chaya", "Baker"), ("Harsha", "Doctor"), ("Abhi", "Nurse"), ("Emily", "Actor"),
    ("Dilip", "Cashier"), ("Gagan", "Editor"), ("Barun", "Farmer")]
ARR = "Lowest to highest: " + ", ".join(f"{LV(i)} {at[i]} ({prof[i]})" for i in range(8))
puzzle(FLR, FA, "Advanced", "A basement, a ground floor and six floors",
       "A building has a basement, a ground floor and six floors above the ground floor (floors 1 to 6, floor 6 being "
       "the topmost). Eight persons Abhi, Barun, Chaya, Dilip, Emily, Feroz, Gagan and Harsha live in it, one on each "
       "of these eight levels. Each has a different profession among Actor, Baker, Cashier, Doctor, Editor, Farmer, "
       "Guard and Nurse. 'Level' means any of the eight (basement, ground floor or floor 1-6).", conds,
       "List the levels from the bottom: basement, ground, 1, 2, 3, 4, 5, 6.\n"
       "Step 1: Three persons live above Emily, so Emily is on floor 3 (the Actor). The Doctor is two levels lower: "
       "floor 1.\n"
       "Step 2: Chaya = ground floor; the Guard is in the basement. Barun = floor 6, Dilip = floor 4, Gagan = floor 5.\n"
       "Step 3: Feroz, Harsha and Abhi take the basement, floor 1 and floor 2. Abhi is immediately above Harsha and "
       "Feroz below Harsha: Feroz = basement (Guard), Harsha = floor 1 (Doctor), Abhi = floor 2.\n"
       "Step 4: The Nurse is immediately above the Doctor: Abhi. Baker, Cashier, Editor and Farmer remain for Chaya "
       "(ground), Dilip (4), Gagan (5) and Barun (6). Cashier is immediately below Editor, and Editor is below Farmer: "
       "Cashier 4 (Dilip), Editor 5 (Gagan), Farmer 6 (Barun). Chaya is the Baker.\n\n"
       + table(["Level", "Person", "Profession"], [(LV(i), at[i], prof[i]) for i in range(7, -1, -1)]), ARR)
ans = at[S["Cashier"]]
assert ans == "Dilip"
ask("Who is the Cashier?", ans, ["Gagan", "Chaya", "Barun"], "Chain the Cashier–Editor–Farmer clues",
    "Of floors 4, 5, 6 and the ground floor, only 4–5 lets the Cashier sit immediately below the Editor with the "
    "Farmer above: Dilip (floor 4) is the Cashier.",
    ["Free professions: Baker, Cashier, Editor, Farmer for ground, 4, 5, 6", "Cashier 4, Editor 5, Farmer 6"],
    why="Gagan is the Editor, Chaya the Baker and Barun the Farmer.", sec=90)
ans = pof["Chaya"]
assert ans == "Baker"
ask("What is Chaya's profession?", ans, ["Guard", "Cashier", "Nurse"], "The leftover profession",
    "Cashier, Editor and Farmer go to floors 4, 5 and 6, so the Baker is left for Chaya on the ground floor.",
    ["Cashier 4, Editor 5, Farmer 6", "Ground floor = Chaya ⇒ Baker"],
    why="The Guard is Feroz, the Cashier Dilip and the Nurse Abhi.", sec=85)
n_ = abs(S["Guard"] - S["Actor"]) - 1
assert n_ == 3
c_, w_ = bal(n_)
ask("How many persons live between the Guard and the Actor?", c_, w_, "Count levels, including the ground floor",
    "The Guard (Feroz) is in the basement and the Actor (Emily) on floor 3. Chaya (ground), Harsha (1) and Abhi (2) "
    "live between them.", ["Guard = basement, Actor = floor 3", "Between: ground, 1, 2 ⇒ three"], natural=by_num,
    sec=85)
ans = at[S["Nurse"] + 1]
assert ans == "Emily"
ask("Who lives immediately above the Nurse?", ans, ["Harsha", "Dilip", "Gagan"], "Find the Nurse first",
    "The Nurse (Abhi) lives on floor 2; floor 3 is Emily's.", ["Nurse = Abhi = floor 2", "Floor 3 = Emily"],
    why="Harsha is below the Nurse; Dilip and Gagan live higher up.", sec=80)
t, f = one_true([("Floor 1", S["Doctor"] == 2), ("The ground floor", S["Doctor"] == 1), ("Floor 2", S["Doctor"] == 3),
                 ("The basement", S["Doctor"] == 0)])
ask("On which level does the Doctor live?", t, f, "Count levels from Emily",
    "Emily is on floor 3 and the Doctor two levels below: floor 1.", ["Emily = floor 3", "Two levels down ⇒ floor 1"],
    why="The ground floor is Chaya's, floor 2 the Nurse's, and the basement the Guard's.", sec=75)
t, f = one_true([("Gagan is the Editor", pof["Gagan"] == "Editor"), ("Harsha lives on the ground floor", S["Harsha"] == 1),
                 ("Three persons live above Dilip", 7 - S["Dilip"] == 3),
                 ("Abhi is the Doctor", pof["Abhi"] == "Doctor")])
ask("Which of the following statements is true?", t, f, "Checking each statement against the building",
    "Gagan (floor 5) is the Editor.", ["Gagan = Editor ✓", "Harsha is on floor 1 ✗",
                                       "Above Dilip (floor 4): only Gagan and Barun ✗", "Abhi is the Nurse ✗"],
    why="Harsha lives on floor 1, only two persons live above Dilip, and Abhi is the Nurse.", sec=80)


# ---- 10B1 Basic set (6): eight coloured boxes in a stack (1 = bottom)
B = ["A", "C", "E", "H", "K", "N", "R", "W"]
CL = ["Aqua", "Black", "Cyan", "Gold", "Ivory", "Lime", "Plum", "Rust"]
conds = [
    ("Box A is kept fourth from the bottom and is Black; Box N is kept immediately above Box A.", ("A", "Black", "N"),
     lambda a, b, n: a == 4 and b == 4 and n == 5),
    ("Box K is kept at the top, and Box H is kept immediately below Box K.", ("K", "H"), lambda k, h: k == 8 and h == 7),
    ("Box C is kept between Box N and Box H, and Box R is kept at the bottom.", ("C", "N", "H", "R"),
     lambda c, n, h, r: n < c < h and r == 1),
    ("Box W is kept above Box E.", ("W", "E"), lambda w, e: w > e),
    ("The Ivory box is kept immediately above the Black box, and the top box is Cyan.", ("Ivory", "Black", "Cyan"),
     lambda i, b, c: i == b + 1 and c == 8),
    ("The Gold box is kept two places below the Black box, and the Plum box is kept between the Gold and Black boxes.",
     ("Gold", "Black", "Plum"), lambda g, b, p: g == b - 2 and g < p < b),
    ("The Rust box is kept immediately below the Cyan box, and the bottom box is not Aqua.", ("Rust", "Cyan", "Aqua"),
     lambda r, c, a: r == c - 1 and a != 1),
]
S = unique(B + CL, {v: range(1, 9) for v in B + CL}, conds, [B, CL])
at, colr = inv(S, B), inv(S, CL)
cofb = {b: colr[S[b]] for b in B}
assert [(at[i], colr[i]) for i in range(1, 9)] == [
    ("R", "Lime"), ("E", "Gold"), ("W", "Plum"), ("A", "Black"), ("N", "Ivory"), ("C", "Aqua"), ("H", "Rust"),
    ("K", "Cyan")]
ARR = "Bottom to top: " + ", ".join(f"{i} {at[i]} ({colr[i]})" for i in range(1, 9))
puzzle(BOX, BWC, "Basic", "Eight coloured boxes in a stack",
       "Eight boxes A, C, E, H, K, N, R and W are kept one above another in a single stack (position 1 is the bottom "
       "and 8 the top). Each box is of a different colour among Aqua, Black, Cyan, Gold, Ivory, Lime, Plum and Rust.",
       conds,
       "Step 1: A = 4 (Black), N = 5, K = 8, H = 7, C = 6, R = 1.\n"
       "Step 2: Positions 2 and 3 remain for E and W; W is above E: E = 2, W = 3.\n"
       "Step 3: Ivory = 5 (N), Cyan = 8 (K), Gold = 2 (E), Plum = 3 (W), Rust = 7 (H).\n"
       "Step 4: Aqua and Lime remain for R (1) and C (6); the bottom box is not Aqua: R Lime, C Aqua.\n\n"
       + table(["Position", "Box", "Colour"], [(i, at[i], colr[i]) for i in range(8, 0, -1)]), ARR)
ans = cofb["W"]
assert ans == "Plum"
ask("What is the colour of Box W?", ans, ["Gold", "Ivory", "Lime"], "'Between' two fixed colours",
    "Gold is at 2 and Black at 4, so Plum is at 3: Box W.", ["Gold 2, Black 4 ⇒ Plum 3", "Position 3 = W"],
    why="Gold is E's colour, Ivory N's and Lime R's.", sec=40)
ans = at[S["Ivory"]]
assert ans == "N"
ask("Which box is Ivory?", "Box " + ans, ["Box C", "Box A", "Box W"], "Ivory sits on the Black box",
    "The Black box (A) is at 4, so Ivory is at 5: Box N.", ["Black = A = 4", "Ivory = 5 = N"],
    why="C is Aqua, A is Black and W is Plum.", sec=35)
n_ = abs(S["E"] - S["Rust"]) - 1
assert n_ == 4
c_, w_ = bal(n_)
ask("How many boxes are kept between Box E and the Rust box?", c_, w_, "Count positions strictly between",
    "E is at 2 and the Rust box (H) at 7, so W, A, N and C lie between them.",
    ["E 2, Rust = H 7", "Between: 3, 4, 5, 6 ⇒ four"], natural=by_num, sec=40)
ans = at[S["Gold"] + 1]
assert ans == "W"
ask("Which box is kept immediately above the Gold box?", "Box " + ans, ["Box A", "Box R", "Box N"],
    "Find the Gold box first", "The Gold box (E) is at 2; position 3 is Box W.", ["Gold = E = 2", "Position 3 = W"],
    why="A is two places above the Gold box, R below it, and N three places above it.", sec=40)
ans = cofb["R"]
assert ans == "Lime"
ask("What is the colour of Box R?", ans, ["Aqua", "Rust", "Gold"], "The last pair by a negative clue",
    "Aqua and Lime remain for R (bottom) and C; the bottom box is not Aqua, so R is Lime.",
    ["Left: Aqua, Lime for R and C", "Bottom ≠ Aqua ⇒ R Lime"], why="Aqua is C's colour, Rust H's and Gold E's.",
    sec=40)
t, f = one_true([("Box C is Aqua", cofb["C"] == "Aqua"), ("Box H is Cyan", cofb["H"] == "Cyan"),
                 ("Box E is kept immediately below Box A", S["E"] == S["A"] - 1),
                 ("Four boxes are kept above Box N", 8 - S["N"] == 4)])
ask("Which of the following statements is true?", t, f, "Checking each statement against the stack",
    "Box C (position 6) is Aqua.", ["C = Aqua ✓", "H is Rust ✗", "E is two places below A (W between) ✗",
                                    "Above N (5): C, H, K = three, not four ✗"],
    why="H is Rust, W sits between E and A, and only three boxes are above N.", sec=45)

# ---- 10BI1 Intermediate set (4): eight boxes on two shelves of four (cell = 10 × shelf + place; shelf 1 = lower,
#      place 1 = left as seen from the front)
B = ["B", "D", "F", "H", "J", "L", "N", "P"]
CELLS = [10 * r + c for r in (1, 2) for c in range(1, 5)]
conds = [
    ("Box J is on the upper shelf, third from the left, and Box F is directly below Box J.", ("J", "F"),
     lambda j, f: j == 23 and f == 13),
    ("Box L is immediately to the right of Box F, and Box B is directly above Box L.", ("L", "F", "B"),
     lambda l, f, b: l == f + 1 and b == l + 10),
    ("Box H is at the left end of the lower shelf, and Box P is on the lower shelf.", ("H", "P"),
     lambda h, p: h == 11 and p // 10 == 1),
    ("Box D is directly above Box P.", ("D", "P"), lambda d, p: d == p + 10),
]
S = unique(B, {b: CELLS for b in B}, conds, [B])
at = inv(S, B)
assert [[at[10 * r + c] for c in range(1, 5)] for r in (2, 1)] == [["N", "D", "J", "B"], ["H", "P", "F", "L"]]
ARR = ("Upper shelf, left to right: " + ", ".join(at[20 + c] for c in range(1, 5)) + "; lower shelf: " +
       ", ".join(at[10 + c] for c in range(1, 5)))
puzzle(BOX, STK, "Intermediate", "Eight boxes on two shelves",
       "Eight boxes B, D, F, H, J, L, N and P are placed on two shelves, upper and lower, four boxes on each shelf in a "
       "line. Each box on the upper shelf is directly above one box on the lower shelf. Left and right are as seen from "
       "the front.", conds,
       "Number the places 1 to 4 from the left on each shelf.\n"
       "Step 1: J = upper 3, F = lower 3, L = lower 4, B = upper 4.\n"
       "Step 2: H = lower 1. P is on the lower shelf: the only free place there is 2. D is directly above P: upper 2.\n"
       "Step 3: N takes the last place, upper 1.\n\n"
       + table(["Shelf", "1", "2", "3", "4"], [("Upper", *[at[20 + c] for c in range(1, 5)]),
                                                ("Lower", *[at[10 + c] for c in range(1, 5)])]), ARR)
ans = at[S["H"] + 10]
assert ans == "N"
ask("Which box is directly above Box H?", "Box " + ans, ["Box D", "Box P", "Box J"], "Same place, upper shelf",
    "H is at lower 1; upper 1 holds N, the last box placed.", ["H = lower 1", "Upper 1 = N"],
    why="D is above P, J above F, and P is beside H.", sec=50)
ans = at[S["D"] + 1]
assert ans == "J"
ask("Which box is placed immediately to the right of Box D?", "Box " + ans, ["Box N", "Box B", "Box F"],
    "Same shelf, next place", "D is at upper 2; upper 3 is J.", ["D = upper 2", "Upper 3 = J"],
    why="N is to D's left, B is two places to its right, and F is on the lower shelf.", sec=45)
t, f = one_true([("B and L", {S["B"], S["L"]} == {24, 14}), ("J and F", {S["J"], S["F"]} == {24, 14}),
                 ("N and H", {S["N"], S["H"]} == {24, 14}), ("D and P", {S["D"], S["P"]} == {24, 14})])
ask("Which two boxes are at the right ends of the two shelves?", t, f, "Right end = place 4 on each shelf",
    "Upper 4 is B and lower 4 is L.", ["Upper 4 = B", "Lower 4 = L"],
    why="J and F are at place 3, N and H at the left ends, and D and P at place 2.", sec=45)
n_ = abs(S["N"] - S["B"]) - 1
assert n_ == 2
c_, w_ = bal(n_)
ask("How many boxes are placed between Box N and Box B on the upper shelf?", c_, w_, "Count places between",
    "N is at upper 1 and B at upper 4; D and J lie between them.", ["N = 1, B = 4 (upper)", "Between: D, J ⇒ two"],
    natural=by_num, sec=45)

# ---- 10BI2 Intermediate set (4): seven boxes of three sizes; no box is ever placed directly on a smaller box
B = ["C", "G", "M", "Q", "T", "V", "Y"]
Z = ["z" + b for b in B]
RANK = {"L": 3, "M": 2, "S": 1}
SZ = {"L": "Large", "M": "Medium", "S": "Small"}
conds = [
    ("No box is kept directly on top of a box smaller than itself.", (*B, *Z),
     lambda *x: all(RANK[x[7 + x[:7].index(p + 1)]] <= RANK[x[7 + x[:7].index(p)]] for p in range(1, 7))),
    ("Box Y is Medium, and Box C is kept immediately below Box Y.", ("Y", "zY", "C"),
     lambda y, z, c: z == "M" and c == y - 1),
    ("Box M is kept at the top, and Box T is Small.", ("M", "zT"), lambda m, z: m == 7 and z == "S"),
    ("Box G is kept immediately below Box T.", ("G", "T"), lambda g, t: g == t - 1),
    ("Box V is kept below Box Q.", ("V", "Q"), lambda v, q: v < q),
]
S = unique(B + Z, {b: range(1, 8) for b in B} | {z: "LMS" for z in Z}, conds, [B],
           extra=[(tuple(Z), lambda *zs: zs.count("L") == 3 and zs.count("M") == 2 and zs.count("S") == 2)])
at = inv(S, B)
sz = {b: S["z" + b] for b in B}
assert [(at[i], sz[at[i]]) for i in range(1, 8)] == [("V", "L"), ("Q", "L"), ("C", "L"), ("Y", "M"), ("G", "M"),
                                                     ("T", "S"), ("M", "S")]
ARR = "Bottom to top: " + ", ".join(f"{i} {at[i]} ({SZ[sz[at[i]]]})" for i in range(1, 8))
puzzle(BOX, STK, "Intermediate", "Seven boxes of three sizes",
       "Seven boxes C, G, M, Q, T, V and Y are kept one above another in a single stack (position 1 is the bottom). "
       "Three boxes are Large, two Medium and two Small.", conds,
       "Step 1: No box sits on a smaller box, so sizes never increase going up: positions 1–3 are Large, 4–5 Medium "
       "and 6–7 Small.\n"
       "Step 2: M = 7 (Small). T is Small: T = 6, and G, immediately below T, = 5 (Medium).\n"
       "Step 3: Y is Medium: the only Medium place left is 4, so Y = 4 and C = 3 (Large).\n"
       "Step 4: V and Q take 1 and 2 with V below: V = 1, Q = 2.\n\n"
       + table(["Position", "Box", "Size"], [(i, at[i], SZ[sz[at[i]]]) for i in range(7, 0, -1)]), ARR)
ans = max((b for b in B if sz[b] == "L"), key=S.get)
assert ans == "C"
ask("Which is the topmost Large box?", "Box " + ans, ["Box Q", "Box Y", "Box V"], "Sizes fall into blocks",
    "Large boxes fill positions 1–3; position 3 is C, kept immediately below the Medium box Y.",
    ["Large = 1, 2, 3", "Position 3 = C"], why="Q and V are lower Large boxes; Y is Medium.", sec=55)
n_ = sum(1 for b in B if sz[b] == "M" and S[b] > S["C"])
assert n_ == 2
c_, w_ = bal(n_)
ask("How many Medium boxes are kept above Box C?", c_, w_, "The size blocks are ordered",
    "Both Medium boxes, Y (4) and G (5), are above C (3).", ["Medium: Y 4, G 5", "Both above C ⇒ two"],
    natural=by_num, sec=50)
ans = at[S["G"] - 1]
assert ans == "Y"
ask("Which box is kept directly below Box G?", "Box " + ans, ["Box C", "Box T", "Box Q"], "Read the stack",
    "G is at 5; position 4 is Y.", ["G = 5", "Position 4 = Y"], why="C is two places below G, T above it, and Q at 2.",
    sec=45)
ans = SZ[sz["Q"]]
assert ans == "Large"
ask("What is the size of Box Q?", ans, ["Medium", "Small", "Cannot be determined"], "Positions fix sizes",
    "Q is at position 2, inside the Large block (1–3).", ["Q = 2", "Positions 1–3 are Large"],
    why="The size of every position is fixed by the rule, so Q's size can be determined.", sec=45)

# ---- 10BA1 Advanced (standalone): a stack of unknown size
V = ["n", "R", "S", "T"]
conds = [
    ("Box R is kept sixth from the top, and Box S is kept fourth from the bottom.", ("n", "R", "S"),
     lambda n, r, s: n - r + 1 == 6 and s == 4),
    ("Exactly two boxes are kept between Box R and Box S.", ("R", "S"), lambda r, s: abs(r - s) == 3),
    ("The stack has more than eight boxes, and Box T is kept immediately above Box R.", ("n", "T", "R"),
     lambda n, t, r: n > 8 and t == r + 1),
]
S = unique(V, {v: range(1, 31) for v in V}, conds, [["R", "S", "T"]],
           extra=[(("n", "R", "S", "T"), lambda n, *xs: max(xs) <= n)])
assert (S["n"], S["R"], S["T"]) == (12, 7, 8)
n_ = S["n"] - S["T"]
assert n_ == 4
c_, w_ = bal(n_)
alone(BOX, STK, "Advanced",
      "Some boxes are kept one above another in a single stack. The number of boxes is not given; R, S and T are "
      "three of them.", conds, "How many boxes are kept above Box T?", c_, w_,
      "Test both orders of R and S; keep the one the size condition allows",
      "S is 4th from the bottom. If R were below S it would be 1st from the bottom and also 6th from the top, giving "
      "only 6 boxes — not more than eight. So R is 4 + 3 = 7th from the bottom, and the stack has 7 + 6 − 1 = 12 "
      "boxes. T is 8th from the bottom, so 12 − 8 = 4 boxes are above it.",
      ["R below S ⇒ R 1st from bottom ⇒ 6 boxes ✗", "R above S ⇒ R 7th from bottom ⇒ n = 12",
       "T = 8th ⇒ above it: 12 − 8 = 4"], natural=by_num, sec=90)

# ---- 10BA2 Advanced (standalone): six boxes with weights and sum clues (1 = bottom)
B = ["D", "F", "L", "P", "U", "Z"]
W = ["w" + b for b in B]
WT = [5, 10, 15, 20, 25, 30]
conds = [
    ("Box Z is the heaviest box, and the boxes kept above Z weigh 40 kg in all.", ("Z", "wZ", *B, *W),
     lambda z, wz, *x: wz == 30 and sum(x[6 + i] for i in range(6) if x[i] > z) == 40),
    ("Box D is the lightest box and is kept immediately above Box Z.", ("D", "wD", "Z"),
     lambda d, wd, z: wd == 5 and d == z + 1),
    ("The two boxes kept below Box Z weigh 35 kg in all.", ("Z", *B, *W),
     lambda z, *x: z == 3 and sum(x[6 + i] for i in range(6) if x[i] < z) == 35),
    ("Box U is at the top, and Box P is kept immediately below Box U.", ("U", "P"), lambda u, p: u == 6 and p == 5),
    ("Box F is kept below Box L.", ("F", "L"), lambda f, l: f < l),
    ("Box U is lighter than Box P but heavier than Box L.", ("wU", "wP", "wL"), lambda u, p, l: l < u < p),
]
S = unique(B + W, {b: range(1, 7) for b in B} | {w: WT for w in W}, conds, [B, W])
wt = {b: S["w" + b] for b in B}
assert [(b, S[b], wt[b]) for b in sorted(B, key=S.get)] == [("F", 1, 25), ("L", 2, 10), ("Z", 3, 30), ("D", 4, 5),
                                                             ("P", 5, 20), ("U", 6, 15)]
c_, w_ = bal(wt["F"], fmt=lambda v: f"{v} kg", step=5, lo=5)
alone(BOX, BWC, "Advanced",
      "Six boxes D, F, L, P, U and Z are kept one above another in a single stack (position 1 is the bottom and 6 the "
      "top). Their weights are 5, 10, 15, 20, 25 and 30 kg, one weight per box.", conds,
      "What is the weight of Box F?", c_, w_, "Split the total weight around the heaviest box",
      "The weights total 105 kg. Z (30 kg) has 40 kg above it and 35 kg below it, and exactly two boxes below it, so "
      "Z = 3. D (5 kg) = 4, U = 6, P = 5, and F, L take 1, 2 with F below. The two bottom boxes weigh 35 kg: 10 + 25 or "
      "15 + 20. P and U weigh 40 − 5 = 35 kg: the other pair. U is lighter than P and heavier than L. If F, L are 10 "
      "and 25, then P, U are 20 and 15, and L must be 10 (lighter than U): F = 25. If F, L were 15 and 20, U would be "
      "10 and could not be heavier than L. So F weighs 25 kg.",
      ["Total 105 = 30 + 40 (above Z) + 35 (below Z) ⇒ Z = 3", "D 4, P 5, U 6, F 1, L 2",
       "F + L = 35 and P + U = 35: {10, 25} and {15, 20} in some order",
       "L < U < P ⇒ P 20, U 15, L 10 ⇒ F 25"], natural=lambda t: int(t.split()[0]), sec=120)


# ================================================================================================ WRITE
# Blind check: question IDs a fresh solver answered from a key-free dump and matched (filled in after the check).
# Blind check (2026-11-07): two fresh solvers answered 108 questions from a key-free dump (every standalone and the
# first two questions of every set) and matched all 108 keys. Afterwards, 'between' was reworded to 'immediately
# between' in five sets and one stem was reworded; those 22 questions are left out, so 97 IDs carry the tag.
BLIND_OK = {f"BANK_REAS_{n:06d}" for n in [1205, 1206, 1211, 1212, 1215, 1216, 1219, 1220, 1221, 1222, 1223, 1226, 1227, 1230, 1231, 1234, 1235, 1237, 1238, 1242, 1243, 1248, 1249, 1251, 1252, 1404, 1405, 1409, 1410, 1413, 1414, 1425, 1426, 1429, 1430, 1433, 1434, 1435, 1436, 1438, 1439, 1440, 1441, 1442, 1443, 1446, 1447, 1450, 1453, 1454, 1603, 1604, 1605, 1609, 1610, 1613, 1623, 1624, 1629, 1630, 1635, 1636, 1640, 1641, 1644, 1645, 1646, 1647, 1648, 1802, 1803, 1804, 1805, 1808, 1809, 1812, 1813, 1815, 1816, 1817, 1821, 1822, 1825, 1826, 1827, 1831, 1832, 1835, 1836, 1841, 1842, 1847, 1848, 1851, 1852, 1855, 1856]}
CHECK = "--draft" not in sys.argv
problems = []
for key, b in BATCH.items():
    p, qs, ss = b["plan"], b["questions"], b["stimuli"]
    have = Counter((x["topic"], x["difficulty"]) for x in qs)
    for t in p["topics"]:
        for d_, n_ in t["quota"].items():
            if have[(t["topic"], d_)] != n_:
                problems.append(f"{key} quota {t['topic']} {d_}: {have[(t['topic'], d_)]} / {n_}")
        assert all(x["subtopic"] in t["subtopics"] for x in qs if x["topic"] == t["topic"]), t["topic"]
    assert all(x["topic"] in {t["topic"] for t in p["topics"]} for x in qs)
    for st_ in ss:
        n_ = sum(1 for x in qs if x.get("stimulus_id") == st_["stimulus_id"])
        assert 3 <= n_ <= 6, (st_["stimulus_id"], n_)
        assert len({(x["topic"], x["difficulty"]) for x in qs if x.get("stimulus_id") == st_["stimulus_id"]}) == 1
    if ss:
        assert ss[0]["stimulus_id"] == p["stimulus_id_start"], (ss[0]["stimulus_id"], p["stimulus_id_start"])
    if len(qs) != p["count"]:
        problems.append(f"{key} count {len(qs)} / {p['count']}")
    elif qs:
        assert qs[0]["question_id"] == p["question_ids"][0] and qs[-1]["question_id"] == p["question_ids"][1]
    for x in qs:
        if x["question_id"] in BLIND_OK:
            x["verification"]["verified_by"] = list(HAND)
    print(f"BATCH_{key}: {len(qs)} questions, {len(ss)} stimuli, keys {dict(sorted(b['keys'].items()))}, "
          f"blind-matched {sum(x['question_id'] in BLIND_OK for x in qs)}")
for x in problems:
    print("  ", x)
if "--dump" in sys.argv:  # key-free dump for the blind solver
    out_ = []
    for b in BATCH.values():
        st = {s["stimulus_id"]: s for s in b["stimuli"]}
        for x in b["questions"]:
            out_.append({"id": x["question_id"], "puzzle": st[x["stimulus_id"]]["content"] if x.get("stimulus_id")
                         else None, "question": x["question_text"],
                         "options": {o["key"]: o["text"] for o in x["options"]}})
    Path(sys.argv[sys.argv.index("--dump") + 1]).write_text(json.dumps(out_, indent=1, ensure_ascii=False),
                                                            encoding="utf-8")
    print("dumped", len(out_))
PARTIAL = "--partial" in sys.argv  # development only: write the batches that are already complete
if CHECK or PARTIAL:
    if not PARTIAL:
        assert not problems, problems
        assert set(BATCH) == set(PKG["batches"])
    for key, b in BATCH.items():
        if PARTIAL and any(x.startswith(key + " ") for x in problems):
            continue
        assert max(b["keys"].values()) - min(b["keys"].values()) <= 4, (key, b["keys"])
        doc = {
            "schema_version": "1.0",
            "batch_id": f"BATCH_{key}",
            "created_at": TODAY,
            "notes": (f"Reasoning Ability topic package 1 (Linear Seating, Circular Seating, Floor-Based and Box-Based "
                      f"Puzzles) of BATCH_{key}: {len(b['questions'])} original questions built by "
                      "tools/packages/REAS_pkg1.py. New puzzle structures (checked against every earlier REAS part "
                      "file). Every puzzle is brute-forced to exactly one arrangement and every answer is read off it "
                      "in code. All questions await human review."),
            "stimuli": b["stimuli"],
            "questions": b["questions"],
        }
        out = ROOT / b["plan"]["output"]
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"wrote {out}")
