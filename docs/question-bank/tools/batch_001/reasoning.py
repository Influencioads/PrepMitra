"""Builds batches/parts/BATCH_001_REAS.json: the 200 Reasoning Ability questions of BATCH_001.

Every computable answer is derived here before the file is written:
- puzzles and seating: the conditions are written once as (text, variables, test) triples; the text goes into the
  stimulus and the test into an exhaustive backtracking search that must return exactly one arrangement. Every
  answer is then read off that arrangement;
- syllogisms: checked over every Venn-region model; inequalities: exhaustive integer assignments;
- blood relations, directions, ranking, series, alphabet, number, coding and input-output: recomputed in code;
- data sufficiency: each statement checked alone and together by enumeration.
Verbal-reasoning items (assumptions, conclusions, cause-effect, critical reasoning) are hand-written and double-checked.
If any assertion fails, nothing is written.

    python tools/batch_001/reasoning.py        (run from docs/question-bank)
"""

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
OUT = ROOT / "batches" / "parts" / "BATCH_001_REAS.json"
TODAY = "2026-11-05"
RA = "Reasoning Ability"
LETTERS = "ABCD"
BRUTE = ("script:brute-force-unique", "ai:author-solve")
RECOMP = ("script:recompute", "ai:author-solve")
VENN = ("script:all-venn-models", "ai:author-solve")
EXHAUST = ("script:exhaustive-integers", "ai:author-solve")
HAND = ("ai:author-solve", "ai:independent-check")
OPT4 = ["Only conclusion I follows", "Only conclusion II follows", "Neither conclusion I nor II follows",
        "Both conclusions I and II follow"]
EITHER = "Either conclusion I or II follows"

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


def num_word(n):
    return ["None", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten"][n]


WORDS = ["None", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten"]
by_num = lambda t: WORDS.index(t) if t in WORDS else float(t.split()[0]) if t.split()[0].replace(".", "").isdigit() else 99


def q(topic, subtopic, difficulty, text, options, answer, concept, explanation, steps, shortcut=None,
      why_others_wrong=None, seconds=60, stimulus=None, verified_by=HAND, tags=None):
    assert answer in LETTERS and len(options) == 4 and len(set(options)) == 4, (text, options)
    out = {
        "question_id": None,
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
    out["question_id"] = f"BANK_REAS_{5 + len(QUESTIONS):06d}"
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
    """The four-option rule: Only I, Only II, Neither, Both; 'Either' replaces the least tempting wrong option."""
    if answer == EITHER:  # 'Both' is the least tempting wrong option when I and II are complementary
        return ["Only conclusion I follows", "Only conclusion II follows", "Neither conclusion I nor II follows",
                EITHER]
    return OPT4


def stimulus(kind, title, intro, conds, solution):
    sid = f"STIM_REAS_{2 + len(STIMULI):06d}"
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


ORD = {1: "immediately", 2: "second", 3: "third", 4: "fourth", 5: "fifth", 6: "sixth", 7: "seventh"}

# ================================================================================================ LINEAR SEATING
LIN = "Linear Seating Arrangement"

# ---- L1 Basic: six persons, one row, all facing north (positions 1..6 from the left end)
P = ["Anil", "Bina", "Chetan", "Divya", "Eshan", "Farah"]
conds = [
    ("Divya sits at one of the extreme ends of the row.", ("Divya",), lambda d: d in (1, 6)),
    ("Exactly two persons sit between Divya and Chetan.", ("Divya", "Chetan"), lambda d, c: abs(d - c) == 3),
    ("Bina sits immediately to the right of Chetan.", ("Bina", "Chetan"), lambda b, c: b == c + 1),
    ("Anil sits third to the left of Farah.", ("Anil", "Farah"), lambda a, f: a == f - 3),
    ("Farah does not sit at an extreme end of the row.", ("Farah",), lambda f: f not in (1, 6)),
]
L1 = unique(P, {p: range(1, 7) for p in P}, conds, [P])
row = sorted(P, key=L1.get)
assert row == ["Eshan", "Anil", "Chetan", "Bina", "Farah", "Divya"]
at = {v: k for k, v in L1.items()}
ARR = "Left to right: " + ", ".join(row)
sid = stimulus("puzzle", "Six friends in a row facing north",
               "Six friends Anil, Bina, Chetan, Divya, Eshan and Farah sit in a straight row, all facing north.",
               conds,
               "If Divya sits at the left end (1), Chetan is at 4 and Bina at 5; the only free pair three apart is "
               "(3, 6), so Farah would sit at the right end, which is not allowed. Hence Divya sits at the right end "
               "(6), Chetan at 3 and Bina at 4. Of the free seats 1, 2 and 5, only (2, 5) are three apart, so Anil "
               "is at 2 and Farah at 5, leaving seat 1 for Eshan.\n\n"
               + table(["Seat (from left)", "Person"], [(i, at[i]) for i in range(1, 7)]))
ans = at[L1["Chetan"] + 2]
puzzle_q(sid, LIN, "Single row, facing north/south", "Basic", "Who sits second to the right of Chetan?",
         ans, ["Anil", "Bina", "Divya"], "Linear arrangement: all facing north, so right means further east",
         f"With everyone facing north, the right of a person is towards seat 6. Chetan is at seat 3, so second to "
         f"his right is seat 5: {ans}.",
         ["Divya cannot be at the left end (it pushes Farah to an end), so Divya = 6, Chetan = 3, Bina = 4",
          "Anil and Farah must be three seats apart among seats 1, 2, 5: Anil = 2, Farah = 5; Eshan = 1",
          ARR, f"Second to the right of Chetan (3) is seat 5: {ans}"],
         why_others_wrong="Anil is immediately to Chetan's left (counting the wrong way); Bina is immediately to "
                          "his right; Divya is third to his right.", seconds=50)
assert ans == "Farah" and at[L1["Chetan"] - 1] == "Anil"
gap = abs(L1["Eshan"] - L1["Farah"]) - 1
puzzle_q(sid, LIN, "Single row, facing north/south", "Basic", "How many persons sit between Eshan and Farah?",
         num_word(gap), ["Two", "Four", "One"], "Counting seats between two persons",
         f"Eshan is at seat {L1['Eshan']} and Farah at seat {L1['Farah']}, so the persons in seats 2 to 4 (Anil, "
         f"Chetan and Bina) sit between them: {gap}.",
         [ARR, f"Eshan = {L1['Eshan']}, Farah = {L1['Farah']}",
          f"Seats strictly between: {L1['Farah'] - L1['Eshan'] - 1}"], natural=by_num, seconds=45)
puzzle_q(sid, LIN, "Single row, facing north/south", "Basic", "Who sits at the extreme left end of the row?",
         at[1], ["Divya", "Anil", "Chetan"], "Fixing the end positions",
         f"Divya is forced to the right end, so the left end is the only seat left after placing everyone else: "
         f"{at[1]}.", [ARR, f"Seat 1 (extreme left): {at[1]}"],
         why_others_wrong="Divya sits at the right end, not the left; Anil and Chetan are at seats 2 and 3.",
         seconds=45)
stm = [
    ("Bina sits exactly in the middle of Chetan and Farah", L1["Bina"] * 2 == L1["Chetan"] + L1["Farah"]),
    ("Eshan sits immediately to the left of Chetan", L1["Eshan"] == L1["Chetan"] - 1),
    ("Farah sits at the extreme right end", L1["Farah"] == 6),
    ("Two persons sit between Anil and Divya", abs(L1["Anil"] - L1["Divya"]) - 1 == 2),
]
t, f = one_true(stm)
puzzle_q(sid, LIN, "Single row, facing north/south", "Basic",
         "Which of the following statements is true according to the arrangement?", t, f,
         "Checking statements against the final arrangement",
         "Chetan (3), Bina (4) and Farah (5) sit in consecutive seats, so Bina is exactly in the middle of them.",
         [ARR, "Bina between Chetan (3) and Farah (5): true",
          "Immediately left of Chetan (3) is Anil (2), not Eshan: false",
          "The right end (6) is Divya: false",
          "Between Anil (2) and Divya (6) sit three persons: false"], seconds=50)

# ---- L2 Intermediate: eight persons, one row, some facing north and some south (seats 1..8 from west to east)
P = ["Gaurav", "Hema", "Ishaan", "Jaya", "Kunal", "Lata", "Mohit", "Nidhi"]
FP = ["f" + p for p in P]
R = lambda pos, face, k: pos + k * (1 if face == "N" else -1)  # k-th to the right; north-facing right = east
conds = [
    ("Kunal sits at one of the extreme ends of the row and faces south.", ("Kunal", "fKunal"),
     lambda k, f: k in (1, 8) and f == "S"),
    ("Exactly three persons sit between Kunal and Jaya.", ("Kunal", "Jaya"), lambda k, j: abs(k - j) == 4),
    ("Ishaan sits immediately to the left of Jaya.", ("Ishaan", "Jaya", "fJaya"),
     lambda i, j, f: R(j, f, -1) == i),
    ("Ishaan and Jaya face opposite directions.", ("fIshaan", "fJaya"), lambda a, b: a != b),
    ("Mohit is an immediate neighbour of Kunal and faces the same direction as Kunal.",
     ("Mohit", "fMohit", "Kunal", "fKunal"), lambda m, fm, k, fk: abs(m - k) == 1 and fm == fk),
    ("Hema sits immediately to the right of Nidhi.", ("Hema", "Nidhi", "fNidhi"), lambda h, n, f: R(n, f, 1) == h),
    ("Lata sits second to the right of Ishaan.", ("Lata", "Ishaan", "fIshaan"), lambda l, i, f: R(i, f, 2) == l),
    ("Only one person sits between Mohit and Hema.", ("Mohit", "Hema"), lambda m, h: abs(m - h) == 2),
    ("Hema faces north, and Nidhi faces the same direction as Hema.", ("fHema", "fNidhi"),
     lambda a, b: a == "N" and b == "N"),
    ("Gaurav and Lata face opposite directions.", ("fGaurav", "fLata"), lambda a, b: a != b),
    ("The two persons sitting at the extreme ends of the row face opposite directions.", tuple(P + FP),
     lambda *v: (lambda d: d["f" + min(P, key=d.get)] != d["f" + max(P, key=d.get)])(dict(zip(P + FP, v)))),
]
order = [x for p in P for x in (p, "f" + p)]
dom = {p: range(1, 9) for p in P} | {f: "NS" for f in FP}
L2 = unique(order, dom, conds, [P])
at = {L2[p]: p for p in P}
face = {p: L2["f" + p] for p in P}
FACE = {"N": "north", "S": "south"}
ARR = "West to east: " + ", ".join(f"{at[i]} ({face[at[i]]})" for i in range(1, 9))
assert [at[i] for i in range(1, 9)] == ["Kunal", "Mohit", "Nidhi", "Hema", "Jaya", "Ishaan", "Gaurav", "Lata"]
right = lambda p, k: at.get(R(L2[p], face[p], k))
sid = stimulus("puzzle", "Eight persons in a row facing north or south",
               "Eight persons Gaurav, Hema, Ishaan, Jaya, Kunal, Lata, Mohit and Nidhi sit in a straight row. Some of "
               "them face north and the others face south. (For a person facing north, the right is towards the "
               "east; for a person facing south, the right is towards the west.)", conds,
               "Kunal is at an end facing south, with Mohit beside him also facing south. Case 1, Kunal at the east "
               "end (seat 8): Mohit = 7, Jaya = 4 and Hema = 5. Nidhi faces north, so Hema (on her right) would put "
               "Nidhi at seat 4, which is Jaya's: rejected. Case 2, Kunal at the west end (seat 1): Mohit = 2, "
               "Jaya = 5, Hema = 4 and Nidhi = 3 (both facing north). Ishaan is immediately to Jaya's left: if Jaya "
               "faced north her left would be seat 4 (Hema), so Jaya faces south and Ishaan is at seat 6 facing north. "
               "Lata is second to Ishaan's right: seat 8. Gaurav takes seat 7. The ends face opposite ways, so Lata "
               "faces north and Gaurav (opposite to Lata) faces south.\n\n"
               + table(["Seat (west to east)", "Person", "Faces"],
                       [(i, at[i], FACE[face[at[i]]]) for i in range(1, 9)]))
ans = right("Jaya", -2)
puzzle_q(sid, LIN, "Single row, facing north/south", "Intermediate", "Who sits second to the left of Jaya?",
         ans, ["Nidhi", "Ishaan", "Lata"], "Mixed facing directions: left and right depend on the person's facing",
         f"Jaya is at seat {L2['Jaya']} facing south, so her left is towards the east. Second to her left is seat "
         f"{L2['Jaya'] + 2}: {ans}.",
         ["Kunal must be at the west end (the east-end case puts Nidhi on Jaya's seat)", ARR,
          f"Jaya faces south, so her left is eastward: seat {L2['Jaya']} + 2 = {L2['Jaya'] + 2}", f"Answer: {ans}"],
         why_others_wrong="Nidhi is second to the west of Jaya, which would be her left only if she faced north; "
                          "Ishaan is immediately to her left; Lata is third to her left.", seconds=70)
assert ans == "Gaurav" and right("Jaya", 2) == "Nidhi"
north = sum(1 for p in P if face[p] == "N")
puzzle_q(sid, LIN, "Single row, facing north/south", "Intermediate", "How many persons face north?",
         num_word(north), ["Three", "Five", "Six"], "Reading the facing directions from the solved row",
         f"Nidhi, Hema, Ishaan and Lata face north; the other four face south. So {north} persons face north.",
         [ARR, "North-facing: Nidhi, Hema, Ishaan, Lata"], natural=by_num, seconds=55)
d = L2["Gaurav"] - L2["Mohit"]  # Mohit faces south, so eastward is his left
assert face["Mohit"] == "S" and d == 5 and right("Mohit", -5) == "Gaurav"
puzzle_q(sid, LIN, "Single row, facing north/south", "Intermediate",
         "What is the position of Gaurav with respect to Mohit?", "Fifth to the left",
         ["Fifth to the right", "Fourth to the left", "Sixth to the right"],
         "Relative position for a south-facing person",
         "Mohit is at seat 2 facing south, so his left is towards the east. Gaurav is at seat 7, five seats east of "
         "Mohit: fifth to Mohit's left.",
         [ARR, "Mohit = seat 2, facing south (left = east)", "Gaurav = seat 7, i.e. 5 seats to the east",
          "So Gaurav is fifth to the left of Mohit"],
         why_others_wrong="'Fifth to the right' is what you get if you forget that Mohit faces south.", seconds=60)
puzzle_q(sid, LIN, "Single row, facing north/south", "Intermediate",
         "Which of the following pairs of persons sit at the two extreme ends of the row?",
         f"{at[1]} and {at[8]}", ["Kunal and Gaurav", "Mohit and Lata", "Kunal and Ishaan"],
         "Identifying end positions", f"Seat 1 is {at[1]} and seat 8 is {at[8]}.", [ARR], seconds=50)
ans = right("Nidhi", 3)
puzzle_q(sid, LIN, "Single row, facing north/south", "Intermediate", "Who sits third to the right of Nidhi?",
         ans, ["Mohit", "Jaya", "Gaurav"], "Counting to the right of a north-facing person",
         f"Nidhi is at seat 3 facing north, so her right is eastward: seat 3 + 3 = 6, which is {ans}.",
         [ARR, f"Nidhi = 3 (north) → third to the right = seat 6 = {ans}"],
         why_others_wrong="Jaya is second to Nidhi's right and Gaurav fourth; Mohit is on her left.", seconds=50)
assert ans == "Ishaan"

# ---- L3 Advanced: double row, ten persons, row membership unknown
P = ["Oviya", "Pranav", "Rekha", "Sahil", "Tanvi", "Uday", "Vimal", "Wasim", "Yamini", "Zoya"]
SEATS = [r * 10 + c for r in (1, 2) for c in range(1, 6)]
rw, cl = (lambda s: s // 10), (lambda s: s % 10)


def RR(s, k):  # k-th to the right; row 1 faces south (right = west), row 2 faces north (right = east)
    c = cl(s) + (k if rw(s) == 2 else -k)
    return rw(s) * 10 + c if 1 <= c <= 5 else None


opp = lambda s: (3 - rw(s)) * 10 + cl(s)
conds = [
    ("Sahil sits in the middle of the row that faces north.", ("Sahil",), lambda s: s == 23),
    ("The person who faces Sahil sits second to the right of Pranav.", ("Sahil", "Pranav"),
     lambda s, p: RR(p, 2) == opp(s)),
    ("Pranav sits at one of the extreme ends of a row.", ("Pranav",), lambda p: cl(p) in (1, 5)),
    ("Oviya faces the person who sits immediately to the right of Tanvi.", ("Oviya", "Tanvi"),
     lambda o, t: RR(t, 1) is not None and opp(RR(t, 1)) == o),
    ("Uday and Vimal sit in the same row with exactly one person between them.", ("Uday", "Vimal"),
     lambda u, v: rw(u) == rw(v) and abs(cl(u) - cl(v)) == 2),
    ("Zoya faces Vimal.", ("Zoya", "Vimal"), lambda z, v: opp(v) == z),
    ("Rekha faces Wasim.", ("Rekha", "Wasim"), lambda r, w: opp(r) == w),
    ("Yamini sits immediately to the right of Zoya.", ("Zoya", "Yamini"), lambda z, y: RR(z, 1) == y),
    ("Wasim is not an immediate neighbour of Sahil.", ("Wasim", "Sahil"),
     lambda w, s: not (rw(w) == rw(s) and abs(cl(w) - cl(s)) == 1)),
    ("Oviya sits in the same row as Sahil, and Wasim sits in the same row as Yamini.",
     ("Oviya", "Sahil", "Wasim", "Yamini"), lambda o, s, w, y: rw(o) == rw(s) and rw(w) == rw(y)),
]
L3 = unique(P, {p: SEATS for p in P}, conds, [P])
at = {v: k for k, v in L3.items()}
assert [at[s] for s in SEATS] == ["Rekha", "Uday", "Tanvi", "Vimal", "Pranav",
                                  "Wasim", "Oviya", "Sahil", "Zoya", "Yamini"]
ARR = ("Row 1 (facing south), west to east: " + ", ".join(at[10 + c] for c in range(1, 6)) +
       "; Row 2 (facing north), west to east: " + ", ".join(at[20 + c] for c in range(1, 6)))
sid = stimulus("puzzle", "Ten persons in two facing rows",
               "Ten persons Oviya, Pranav, Rekha, Sahil, Tanvi, Uday, Vimal, Wasim, Yamini and Zoya sit in two "
               "parallel rows of five seats each, with equal distance between neighbours. Row 1 is to the north and "
               "the persons in it face south; Row 2 is to the south and the persons in it face north. So every person "
               "faces exactly one person of the other row. Who sits in which row is not given.", conds,
               "Sahil is at seat 3 of Row 2, so the person facing him is at seat 3 of Row 1; that person is second "
               "to Pranav's right, so Pranav is in Row 1 at the east end (a south-facing person's right is west). "
               "Zoya faces Vimal, Yamini sits beside Zoya, Wasim shares Yamini's row and Rekha faces Wasim, so "
               "{Zoya, Yamini, Wasim} sit in one row and {Vimal, Uday, Rekha} in the other. If Zoya, Yamini and "
               "Wasim were in Row 1, Uday and Vimal would take Row 2 seats 2 and 4, Oviya would be forced to seat 1 "
               "(Tanvi at Row 1 seat 2), Zoya would have to face Vimal from seat 4 (seat 2 is Tanvi's), putting "
               "Yamini at seat 3 and Wasim at seat 1, and Rekha, facing Wasim, would need Oviya's seat: rejected. So Row 2 holds "
               "Sahil, Oviya, Zoya, Yamini and Wasim, and Row 1 holds Pranav, Tanvi, Uday, Vimal and Rekha. Testing "
               "Zoya–Yamini at seats 1–2 or 4–5 of Row 2 against the remaining conditions leaves only the "
               "arrangement below.\n\n"
               + table(["Seat (west to east)", "Row 1 (faces south)", "Row 2 (faces north)"],
                       [(c, at[10 + c], at[20 + c]) for c in range(1, 6)]))
puzzle_q(sid, LIN, "Double row", "Advanced", "Who faces the person who sits second to the left of Zoya?",
         at[opp(RR(L3["Zoya"], -2))],
         ["Vimal", "Tanvi", "Rekha"], "Double row: find the seat, then cross to the facing row",
         "Zoya sits at seat 4 of Row 2 facing north, so her left is towards the west. Second to her left is seat 2 "
         f"of Row 2 ({at[RR(L3['Zoya'], -2)]}), who faces seat 2 of Row 1: {at[opp(RR(L3['Zoya'], -2))]}.",
         ["Row membership: {Zoya, Yamini, Wasim} with Sahil and Oviya in Row 2; the rest in Row 1", ARR,
          f"Second to the left of Zoya (Row 2, seat 4, facing north) = Row 2 seat 2 = {at[RR(L3['Zoya'], -2)]}",
          f"The person facing Row 2 seat 2 is Row 1 seat 2 = {at[opp(RR(L3['Zoya'], -2))]}"],
         why_others_wrong="Vimal faces Zoya herself; Tanvi faces Sahil; Rekha faces Wasim.", seconds=90)
assert at[opp(RR(L3["Zoya"], -2))] == "Uday" and at[opp(L3["Zoya"])] == "Vimal"
puzzle_q(sid, LIN, "Double row", "Advanced", "Which two persons sit at the extreme ends of the row that faces south?",
         f"{at[11]} and {at[15]}", ["Wasim and Yamini", "Rekha and Vimal", "Uday and Pranav"],
         "Separating the two rows first", f"Row 1 faces south; its end seats are held by {at[11]} and {at[15]}.",
         [ARR], why_others_wrong="Wasim and Yamini are the ends of the north-facing row.", seconds=60)
gap = abs(cl(L3["Wasim"]) - cl(L3["Yamini"])) - 1
puzzle_q(sid, LIN, "Double row", "Advanced", "How many persons sit between Wasim and Yamini?", num_word(gap),
         ["One", "Two", "Four"], "Counting within one row",
         f"Wasim and Yamini both sit in Row 2, at seats 1 and 5, so Oviya, Sahil and Zoya sit between them: {gap}.",
         [ARR], natural=by_num, seconds=60)
stm = [
    ("Tanvi faces Sahil", opp(L3["Tanvi"]) == L3["Sahil"]),
    ("Pranav faces Zoya", opp(L3["Pranav"]) == L3["Zoya"]),
    ("Oviya sits immediately to the right of Sahil", RR(L3["Sahil"], 1) == L3["Oviya"]),
    ("Rekha sits immediately to the left of Uday", RR(L3["Uday"], -1) == L3["Rekha"]),
]
t, f = one_true(stm)
puzzle_q(sid, LIN, "Double row", "Advanced", "Which of the following statements is true?", t, f,
         "Checking statements in a double-row arrangement",
         "Tanvi is at seat 3 of Row 1 and Sahil at seat 3 of Row 2, so they face each other.",
         [ARR, "Tanvi (Row 1, seat 3) faces Sahil (Row 2, seat 3): true",
          "Pranav (Row 1, seat 5) faces Yamini, not Zoya: false",
          "Sahil faces north, so his right is seat 4 (Zoya), not Oviya: false",
          "Uday faces south, so his left is east (seat 3, Tanvi), not Rekha: false"], seconds=75)

# ================================================================================================ CIRCULAR SEATING
CIR = "Circular Seating Arrangement"

# ---- C1 Basic: six persons facing the centre. Seats numbered anticlockwise; a centre-facing person's right = +1
P = ["Kavya", "Lalit", "Meera", "Naveen", "Omkar", "Priya"]
N = 6
conds = [
    ("Meera sits immediately to the right of Kavya.", ("Meera", "Kavya"), lambda m, k: m == (k + 1) % N),
    ("Lalit sits opposite Kavya.", ("Lalit", "Kavya"), lambda l, k: l == (k + 3) % N),
    ("Naveen sits second to the right of Lalit.", ("Naveen", "Lalit"), lambda n, l: n == (l + 2) % N),
    ("Omkar is not an immediate neighbour of Naveen.", ("Omkar", "Naveen"),
     lambda o, n: (o - n) % N not in (1, N - 1)),
]
dom = {p: range(N) for p in P} | {"Kavya": [0]}  # fixing Kavya removes rotations
C1 = unique(P, dom, conds, [P])
at = {v: k for k, v in C1.items()}
cw = lambda p, k: at[(C1[p] + k) % N]  # k-th to the right (centre-facing)
ARR = "Going to the right (anticlockwise) from Kavya: " + ", ".join(at[i] for i in range(N))
assert [at[i] for i in range(N)] == ["Kavya", "Meera", "Omkar", "Lalit", "Priya", "Naveen"]
sid = stimulus("puzzle", "Six friends around a circular table",
               "Six friends Kavya, Lalit, Meera, Naveen, Omkar and Priya sit around a circular table, equally spaced, "
               "all facing the centre.", conds,
               "Place Kavya first. Meera is immediately to her right and Lalit opposite her. Naveen is second to "
               "Lalit's right, which is the seat immediately to Kavya's left. Two seats remain: the one between "
               "Meera and Lalit, and the one between Lalit and Naveen. Omkar cannot sit next to Naveen, so Omkar sits "
               "between Meera and Lalit and Priya between Lalit and Naveen.\n\n"
               + table(["Order to the right of Kavya", "Person"], [(i, at[i]) for i in range(N)]))
puzzle_q(sid, CIR, "Facing centre", "Basic", "Who sits opposite Meera?", cw("Meera", 3),
         ["Naveen", "Lalit", "Omkar"], "Circular arrangement facing the centre",
         f"In a six-seat circle the opposite seat is three places away. Three places from Meera is "
         f"{cw('Meera', 3)}.", [ARR, f"Opposite Meera: {cw('Meera', 3)}"],
         why_others_wrong="Lalit is opposite Kavya; Omkar is Meera's neighbour; Naveen is opposite Omkar.",
         seconds=45)
ans = cw("Omkar", -2)
puzzle_q(sid, CIR, "Facing centre", "Basic", "Who sits second to the left of Omkar?", ans,
         ["Priya", "Lalit", "Meera"], "Left of a centre-facing person is the clockwise direction",
         f"Going left (clockwise) from Omkar: Meera, then {ans}.", [ARR, f"Left of Omkar: Meera, then {ans}"],
         why_others_wrong="Priya is second to Omkar's right; Lalit and Meera are his immediate neighbours.",
         seconds=45)
assert ans == "Kavya" and cw("Omkar", 2) == "Priya"
puzzle_q(sid, CIR, "Facing centre", "Basic", "Who sits immediately to the left of Kavya?", cw("Kavya", -1),
         ["Meera", "Priya", "Lalit"], "Immediate neighbours in a circle",
         f"Meera is on Kavya's right; the seat on her left belongs to {cw('Kavya', -1)}.", [ARR], seconds=40)
cnt = next(k for k in range(1, N) if cw("Omkar", k) == "Naveen") - 1
puzzle_q(sid, CIR, "Facing centre", "Basic",
         "How many persons sit between Omkar and Naveen when counted to the right of Omkar?", num_word(cnt),
         ["One", "Three", "Four"], "Counting in one direction around a circle",
         f"Moving right from Omkar: Lalit, Priya, then Naveen. So {cnt} persons sit between them in that direction.",
         [ARR, "Right of Omkar: Lalit, Priya, Naveen"], natural=by_num, seconds=45)
assert cnt == 2

# ---- C2 Intermediate: eight persons, some facing the centre (I), some facing outside (O)
P = ["Aarav", "Bhavna", "Chirag", "Deepa", "Farhan", "Gita", "Harsh", "Isha"]
N = 8
RC = lambda s, f, k: (s + (k if f == "I" else -k)) % N
adj = lambda a, b: (a - b) % N in (1, N - 1)
conds = [
    ("Farhan sits opposite Aarav.", ("Farhan", "Aarav"), lambda f, a: f == (a + 4) % N),
    ("Aarav faces the centre, and Gita sits immediately to his right.", ("Aarav", "fAarav", "Gita"),
     lambda a, f, g: f == "I" and RC(a, f, 1) == g),
    ("Gita and Aarav face opposite directions.", ("fGita", "fAarav"), lambda a, b: a != b),
    ("Harsh sits third to the right of Isha.", ("Isha", "fIsha", "Harsh"), lambda i, f, h: RC(i, f, 3) == h),
    ("Harsh and Farhan face the same direction.", ("fHarsh", "fFarhan"), lambda a, b: a == b),
    ("Deepa is an immediate neighbour of Aarav.", ("Deepa", "Aarav"), adj),
    ("Chirag sits second to the right of Farhan.", ("Farhan", "fFarhan", "Chirag"),
     lambda f, ff, c: RC(f, ff, 2) == c),
    ("Bhavna is an immediate neighbour of both Farhan and Harsh.", ("Bhavna", "Farhan", "Harsh"),
     lambda b, f, h: adj(b, f) and adj(b, h)),
    ("Exactly three persons face outside.", tuple("f" + p for p in P), lambda *f: f.count("O") == 3),
    ("Isha faces the same direction as Aarav.", ("fIsha", "fAarav"), lambda a, b: a == b),
]
order = [x for p in P for x in (p, "f" + p)]
dom = {p: range(N) for p in P} | {"f" + p: "IO" for p in P} | {"Aarav": [0]}
C2 = unique(order, dom, conds, [P])
at = {C2[p]: p for p in P}
fc = {p: C2["f" + p] for p in P}
rt = lambda p, k: at[RC(C2[p], fc[p], k)]
FC = {"I": "centre", "O": "outside"}
ARR = "Anticlockwise from Aarav: " + ", ".join(f"{at[i]} ({FC[fc[at[i]]]})" for i in range(N))
assert [at[i] for i in range(N)] == ["Aarav", "Gita", "Chirag", "Isha", "Farhan", "Bhavna", "Harsh", "Deepa"]
sid = stimulus("puzzle", "Eight persons around a circle, facing in or out",
               "Eight persons Aarav, Bhavna, Chirag, Deepa, Farhan, Gita, Harsh and Isha sit around a circular "
               "table, equally spaced. Some of them face the centre and the others face outside. (For a person facing "
               "the centre, the right is anticlockwise; for a person facing outside, the right is clockwise.)", conds,
               "Fix Aarav (facing the centre). Farhan is opposite him, Gita is the next seat anticlockwise (facing "
               "outside) and Deepa takes the other seat beside Aarav. Bhavna sits between Farhan and Harsh: either "
               "(a) Bhavna and Harsh on Gita's side of Farhan, or (b) on Deepa's side. In (a) Harsh is next to "
               "Gita, Chirag must be two seats from Farhan on Deepa's side (so Farhan faces the centre), Isha takes "
               "the last seat, and Harsh being third to Isha's right forces Isha to face outside, contradicting "
               "'Isha faces the same way as Aarav'. In (b) Chirag is two seats from Farhan on Gita's side, so Farhan "
               "faces outside, and so does Harsh. Isha takes the seat between Chirag and Farhan; counting three to "
               "her right reaches Harsh only if she faces the centre. Gita, Farhan and Harsh are the three facing "
               "outside, so everyone else faces the centre.\n\n"
               + table(["Anticlockwise from Aarav", "Person", "Faces"],
                       [(i, at[i], FC[fc[at[i]]]) for i in range(N)]))
ans = rt("Deepa", -2)
puzzle_q(sid, CIR, "Facing inside and outside", "Intermediate", "Who sits second to the left of Deepa?", ans,
         ["Aarav", "Gita", "Farhan"], "Left of a centre-facing person is clockwise",
         f"Deepa faces the centre, so her left is clockwise: Harsh, then {ans}.",
         ["Case (a) (Bhavna between Farhan and Harsh on Gita's side) fails on Isha's direction", ARR,
          f"Deepa faces the centre; clockwise from her: Harsh, {ans}"],
         why_others_wrong="Gita is second to Deepa's right; Aarav is immediately to her right; Farhan is third to "
                          "her left.", seconds=75)
assert ans == "Bhavna"
k = next(k for k in range(1, N) if rt("Gita", k) == "Harsh")
puzzle_q(sid, CIR, "Facing inside and outside", "Intermediate",
         "How many persons sit between Gita and Harsh when counted to the right of Gita?", num_word(k - 1),
         ["One", "Three", "Four"], "Counting to the right of an outside-facing person",
         "Gita faces outside, so her right is clockwise: Aarav, Deepa, then Harsh. Two persons sit between them.",
         [ARR, "Gita faces outside → her right is clockwise", "Clockwise from Gita: Aarav, Deepa, Harsh"],
         natural=by_num, seconds=60)
assert k - 1 == 2
outside = [p for p in P if fc[p] == "O"]
puzzle_q(sid, CIR, "Facing inside and outside", "Intermediate", "Which of the following persons face outside?",
         ", ".join(outside[:-1]) + " and " + outside[-1],
         ["Farhan, Gita and Isha", "Gita, Harsh and Deepa", "Chirag, Farhan and Harsh"],
         "Facing directions", "Exactly three persons face outside: Farhan, Gita and Harsh.", [ARR], seconds=50)
assert outside == ["Farhan", "Gita", "Harsh"]
assert rt("Chirag", 1) == "Isha"
puzzle_q(sid, CIR, "Facing inside and outside", "Intermediate",
         "What is the position of Isha with respect to Chirag?", "Immediately to the right",
         ["Immediately to the left", "Second to the right", "Third to the left"],
         "Relative position", "Chirag faces the centre, so his right is anticlockwise, and the next seat "
         "anticlockwise from Chirag is Isha's.", [ARR], seconds=50)
puzzle_q(sid, CIR, "Facing inside and outside", "Intermediate", "Who sits opposite Isha?", at[(C2["Isha"] + 4) % N],
         ["Aarav", "Harsh", "Bhavna"], "Opposite seats in an eight-seat circle",
         f"Opposite means four seats away: {at[(C2['Isha'] + 4) % N]}.", [ARR], seconds=45)
assert at[(C2["Isha"] + 4) % N] == "Deepa"

# ---- C3 Advanced: square table, corners face the centre, middle-of-side seats face outside; plus home city
P = ["Jatin", "Komal", "Lokesh", "Manju", "Neel", "Pallavi", "Rohan", "Sneha"]
CT = ["Agra", "Bhopal", "Cochin", "Dehradun", "Indore", "Jaipur", "Kanpur", "Mysuru"]
N = 8
corner = lambda s: s % 2 == 0
RS = lambda s, k: (s + (k if corner(s) else -k)) % N
conds = [
    ("The person from Bhopal sits opposite Jatin.", ("Bhopal", "Jatin"), lambda b, j: b == (j + 4) % N),
    ("Lokesh sits second to the right of the person from Bhopal.", ("Lokesh", "Bhopal"),
     lambda l, b: RS(b, 2) == l),
    ("Sneha is from Agra.", ("Sneha", "Agra"), lambda s, a: s == a),
    ("Rohan faces the centre and sits immediately to the left of the person from Agra.", ("Rohan", "Agra"),
     lambda r, a: corner(r) and RS(a, -1) == r),
    ("Komal is from Jaipur and is an immediate neighbour of both Rohan and Manju.",
     ("Komal", "Jaipur", "Rohan", "Manju"), lambda k, j, r, m: k == j and adj(k, r) and adj(k, m)),
    ("Jatin sits second to the left of the person from Mysuru.", ("Mysuru", "Jatin"), lambda my, j: RS(my, -2) == j),
    ("Neel is from Kanpur and sits opposite Sneha.", ("Neel", "Kanpur", "Sneha"),
     lambda n, k, s: n == k and n == (s + 4) % N),
    ("The person from Cochin sits immediately to the right of the person from Dehradun.", ("Cochin", "Dehradun"),
     lambda c, d: RS(d, 1) == c),
    ("The persons from Dehradun and Indore both face the centre.", ("Dehradun", "Indore"),
     lambda d, i: corner(d) and corner(i)),
]
dom = {p: range(N) for p in P + CT} | {"Jatin": [0, 1]}  # rotations by two seats keep corners as corners
C3 = unique(P + CT, dom, conds, [P, CT])
at = {C3[p]: p for p in P}
city = {p: next(c for c in CT if C3[c] == C3[p]) for p in P}
ARR = "Anticlockwise from Jatin: " + ", ".join(
    f"{at[i]} ({city[at[i]]}, {'corner' if corner(i) else 'side'})" for i in range(N))
assert [(at[i], city[at[i]]) for i in range(N)] == [
    ("Jatin", "Indore"), ("Sneha", "Agra"), ("Rohan", "Mysuru"), ("Komal", "Jaipur"), ("Manju", "Bhopal"),
    ("Neel", "Kanpur"), ("Lokesh", "Dehradun"), ("Pallavi", "Cochin")]
sid = stimulus("puzzle", "Eight persons at a square table, with home cities",
               "Eight persons Jatin, Komal, Lokesh, Manju, Neel, Pallavi, Rohan and Sneha sit around a square table. "
               "Four of them sit at the four corners and face the centre; the other four sit at the middle of the "
               "four sides and face outside (away from the centre). Each of them is from a different city among "
               "Agra, Bhopal, Cochin, Dehradun, Indore, Jaipur, Kanpur and Mysuru.", conds,
               "Rohan faces the centre (a corner) and sits immediately to the left of Sneha (Agra). If Sneha were "
               "at a corner, her immediate left would be a side seat, so Sneha sits at a side, facing outside, with "
               "Rohan on the next corner to her left. Komal (Jaipur) sits on Rohan's other side, with Manju at the "
               "following corner. Neel (Kanpur) sits opposite Sneha, i.e. on the side after Manju. Jatin is second to "
               "the left of the Mysuru person and the Bhopal person sits opposite Jatin; together with Lokesh being "
               "second to the right of the Bhopal person, this places Jatin at the corner on Sneha's other side, "
               "Manju (Bhopal) opposite him, Lokesh at the last corner and Rohan from Mysuru. Pallavi takes the "
               "last side seat. Dehradun faces the centre and Cochin is immediately to its right, so Lokesh is from "
               "Dehradun and Pallavi from Cochin; Indore (a corner) goes to Jatin.\n\n"
               + table(["Anticlockwise from Jatin", "Person", "City", "Seat type"],
                       [(i, at[i], city[at[i]], "corner (faces centre)" if corner(i) else "side (faces outside)")
                        for i in range(N)]))
ans = at[RS(C3["Kanpur"], 2)]
puzzle_q(sid, CIR, "Square and rectangular tables", "Advanced",
         "Who sits second to the right of the person from Kanpur?", ans, ["Lokesh", "Manju", "Pallavi"],
         "Square table: side-seat persons face outside, so their right is clockwise",
         f"Neel (Kanpur) sits at the middle of a side and faces outside, so his right is clockwise: Manju, then "
         f"{ans}.", ["Sneha must be at a side seat with Rohan at the corner to her left", ARR,
                     f"Neel faces outside: clockwise from Neel → Manju, {ans}"],
         why_others_wrong="Pallavi is second to Neel's left; Lokesh is immediately to his left; Manju is "
                          "immediately to his right.", seconds=90)
assert ans == "Komal"
ans = city[at[RS(C3["Manju"], -1)]]
puzzle_q(sid, CIR, "Square and rectangular tables", "Advanced",
         "The person from which city sits immediately to the left of Manju?", ans, ["Kanpur", "Mysuru", "Bhopal"],
         "Corner seats face the centre, so the left is clockwise",
         f"Manju sits at a corner facing the centre; her immediate left is the clockwise seat, held by Komal, who is "
         f"from {ans}.", [ARR, f"Clockwise from Manju: Komal ({ans})"],
         why_others_wrong="Kanpur (Neel) is on Manju's right; Bhopal is Manju's own city; Mysuru is Rohan's.",
         seconds=75)
assert ans == "Jaipur"
sides = [at[i] for i in range(N) if not corner(i)]
puzzle_q(sid, CIR, "Square and rectangular tables", "Advanced",
         "Which of the following groups sit at the middle of the sides of the table?", ", ".join(sides[:3]) +
         " and " + sides[3], ["Sneha, Rohan, Neel and Pallavi", "Jatin, Komal, Neel and Pallavi",
                              "Sneha, Komal, Lokesh and Neel"], "Corner versus side seats",
         "The persons facing outside are at the middle of the sides: " + ", ".join(sides) + ".", [ARR], seconds=60)
stm = [
    ("Lokesh – Dehradun – corner", city["Lokesh"] == "Dehradun" and corner(C3["Lokesh"])),
    ("Pallavi – Dehradun – side", city["Pallavi"] == "Dehradun" and not corner(C3["Pallavi"])),
    ("Rohan – Indore – corner", city["Rohan"] == "Indore" and corner(C3["Rohan"])),
    ("Jatin – Mysuru – corner", city["Jatin"] == "Mysuru" and corner(C3["Jatin"])),
]
t, f = one_true(stm)
puzzle_q(sid, CIR, "Square and rectangular tables", "Advanced",
         "Which of the following person – city – seat combinations is correct?", t, f,
         "Matching two attributes to the final seating",
         "Lokesh sits at a corner and is from Dehradun; Pallavi (side) is from Cochin, Rohan from Mysuru and Jatin "
         "from Indore.", [ARR], seconds=70)

# ================================================================================================ FLOOR PUZZLES
FLR = "Floor-Based Puzzles"

# ---- F1 Basic: six persons, six floors (1 = lowermost)
P = ["Tara", "Usha", "Varun", "Wamiq", "Yogita", "Zubin"]
conds = [
    ("Tara lives on an odd-numbered floor.", ("Tara",), lambda t: t % 2 == 1),
    ("Only one person lives between Tara and Usha.", ("Tara", "Usha"), lambda t, u: abs(t - u) == 2),
    ("Wamiq lives immediately above Usha.", ("Wamiq", "Usha"), lambda w, u: w == u + 1),
    ("Zubin lives immediately above Tara, but below Usha.", ("Zubin", "Tara", "Usha"),
     lambda z, t, u: z == t + 1 and z < u),
    ("Varun lives on a floor below Yogita.", ("Varun", "Yogita"), lambda v, y: v < y),
    ("Yogita does not live on the topmost floor.", ("Yogita",), lambda y: y != 6),
]
F1 = unique(P, {p: range(1, 7) for p in P}, conds, [P])
at = {v: k for k, v in F1.items()}
assert [at[i] for i in range(1, 7)] == ["Varun", "Yogita", "Tara", "Zubin", "Usha", "Wamiq"]
ARR = "Floor 1 to 6: " + ", ".join(at[i] for i in range(1, 7))
sid = stimulus("puzzle", "Six persons on six floors",
               "Six persons Tara, Usha, Varun, Wamiq, Yogita and Zubin live on the six floors of a building, one on "
               "each floor. The lowermost floor is numbered 1 and the topmost floor is numbered 6.", conds,
               "Tara is on 1, 3 or 5 with Zubin immediately above her and Usha above Zubin. Tara = 1 gives Usha = 3, "
               "Wamiq = 4, Zubin = 2, leaving floors 5 and 6 for Varun and Yogita, so Yogita would be on the top "
               "floor: rejected. Tara = 5 puts Zubin on 6, above every possible Usha: rejected. So Tara = 3, Zubin = "
               "4, Usha = 5 (floor 1 would be below Zubin), Wamiq = 6, and Varun = 1, Yogita = 2.\n\n"
               + table(["Floor", "Person"], [(i, at[i]) for i in range(6, 0, -1)]))
puzzle_q(sid, FLR, "Floor and flat", "Basic", "Who lives on the topmost floor?", at[6], ["Usha", "Yogita", "Zubin"],
         "Floor puzzle: fix the most constrained person first",
         "Tara must be on floor 3, which places Usha on 5 and Wamiq immediately above her on floor 6.",
         ["Tara = 1 forces Yogita to the top floor; Tara = 5 puts Zubin above Usha: both rejected", ARR,
          f"Floor 6: {at[6]}"], seconds=50)
gap = abs(F1["Yogita"] - F1["Usha"]) - 1
puzzle_q(sid, FLR, "Floor and flat", "Basic", "How many persons live between Yogita and Usha?", num_word(gap),
         ["One", "Three", "Four"], "Counting floors between two persons",
         f"Yogita is on floor {F1['Yogita']} and Usha on floor {F1['Usha']}; Tara and Zubin live between them.",
         [ARR, f"Floors strictly between {F1['Yogita']} and {F1['Usha']}: 3 and 4"], natural=by_num, seconds=45)
puzzle_q(sid, FLR, "Floor and flat", "Basic", "Who lives immediately below Tara?", at[F1["Tara"] - 1],
         ["Varun", "Zubin", "Wamiq"], "Reading adjacent floors",
         f"Tara is on floor 3; floor 2 belongs to {at[F1['Tara'] - 1]}.", [ARR],
         why_others_wrong="Zubin is immediately above Tara, not below; Varun is on floor 1.", seconds=40)
stm = [("Zubin lives on floor 4", F1["Zubin"] == 4),
       ("Varun lives immediately below Tara", F1["Varun"] == F1["Tara"] - 1),
       ("Usha lives on an even-numbered floor", F1["Usha"] % 2 == 0),
       ("Wamiq lives immediately above Zubin", F1["Wamiq"] == F1["Zubin"] + 1)]
t, f = one_true(stm)
puzzle_q(sid, FLR, "Floor and flat", "Basic", "Which of the following statements is true?", t, f,
         "Checking statements against the arrangement", "Zubin lives on floor 4, immediately above Tara.",
         [ARR, "Varun is on 1, Tara on 3 (Yogita is between): false", "Usha is on 5 (odd): false",
          "Wamiq (6) is above Usha (5), not Zubin (4): false"], seconds=45)

# ---- F2 Intermediate: four floors x two flats (West/East)
P = ["Arjun", "Bindu", "Cyrus", "Daksh", "Ekta", "Firoz", "Gauri", "Hiten"]
SL = [f * 10 + w for f in range(1, 5) for w in (1, 2)]
fl, sd = (lambda s: s // 10), (lambda s: s % 10)
conds = [
    ("Daksh lives in a West flat on an odd-numbered floor, but not on the lowermost floor.", ("Daksh",),
     lambda d: sd(d) == 1 and fl(d) % 2 == 1 and fl(d) != 1),
    ("Bindu lives in the flat immediately above Hiten's flat.", ("Bindu", "Hiten"), lambda b, h: b == h + 10),
    ("Hiten and Daksh live on the same floor.", ("Hiten", "Daksh"), lambda h, d: fl(h) == fl(d)),
    ("Cyrus lives in an East flat, immediately below Ekta's flat.", ("Cyrus", "Ekta"),
     lambda c, e: sd(c) == 2 and c == e - 10),
    ("Arjun and Ekta live on the same floor.", ("Arjun", "Ekta"), lambda a, e: fl(a) == fl(e)),
    ("Firoz lives on a floor below Gauri's floor.", ("Firoz", "Gauri"), lambda f_, g: fl(f_) < fl(g)),
]
F2 = unique(P, {p: SL for p in P}, conds, [P])
at = {v: k for k, v in F2.items()}
assert [at[s] for s in SL] == ["Firoz", "Cyrus", "Arjun", "Ekta", "Daksh", "Hiten", "Gauri", "Bindu"]
ARR = "; ".join(f"Floor {x}: West {at[x * 10 + 1]}, East {at[x * 10 + 2]}" for x in range(4, 0, -1))
sid = stimulus("puzzle", "Eight persons in a four-storey building with two flats per floor",
               "Eight persons Arjun, Bindu, Cyrus, Daksh, Ekta, Firoz, Gauri and Hiten live in a four-storey building. "
               "The lowermost floor is 1 and the topmost is 4. Each floor has two flats, West and East; the West flat "
               "of a floor is directly above the West flat of the floor below it, and likewise for the East flats. "
               "Each person lives in a different flat.", conds,
               "Daksh is on floor 3, West flat. Hiten shares his floor, so Hiten is in 3-East and Bindu, directly "
               "above Hiten, is in 4-East. Ekta has Cyrus directly below her in an East flat; 4-East and 3-East are "
               "taken, so Ekta is in 2-East and Cyrus in 1-East. Arjun shares Ekta's floor: 2-West. Firoz and Gauri "
               "take 1-West and 4-West, and Firoz is lower, so Firoz = 1-West and Gauri = 4-West.\n\n"
               + table(["Floor", "West flat", "East flat"],
                       [(x, at[x * 10 + 1], at[x * 10 + 2]) for x in range(4, 0, -1)]))
puzzle_q(sid, FLR, "Floor and flat", "Intermediate", "Who lives in the flat immediately below Gauri's flat?",
         at[F2["Gauri"] - 10], ["Hiten", "Bindu", "Arjun"],
         "Floor and flat: 'immediately below' means the same side, one floor lower",
         f"Gauri lives in 4-West, so the flat immediately below is 3-West: {at[F2['Gauri'] - 10]}.",
         ["Daksh = 3-West → Hiten = 3-East → Bindu = 4-East", "Ekta = 2-East, Cyrus = 1-East, Arjun = 2-West",
          "Firoz = 1-West, Gauri = 4-West", ARR, f"Below 4-West is 3-West: {at[F2['Gauri'] - 10]}"],
         why_others_wrong="Hiten is diagonally below Gauri (3-East); Bindu shares her floor; Arjun is two floors "
                          "down.", seconds=70)
mate = lambda p: at[F2[p] + (1 if sd(F2[p]) == 1 else -1)]
puzzle_q(sid, FLR, "Floor and flat", "Intermediate", "Who lives on the same floor as Firoz?", mate("Firoz"),
         ["Arjun", "Ekta", "Gauri"], "Pairs on the same floor",
         f"Firoz lives in 1-West; the East flat of floor 1 belongs to {mate('Firoz')}.", [ARR], seconds=55)
assert mate("Firoz") == "Cyrus"
above = sum(1 for p in P if fl(F2[p]) > fl(F2["Arjun"]))
puzzle_q(sid, FLR, "Floor and flat", "Intermediate", "How many persons live on floors above Arjun's floor?",
         num_word(above), ["Two", "Three", "Five"], "Counting by floors, not flats",
         f"Arjun lives on floor 2. Floors 3 and 4 hold two persons each, so {above} persons live above his floor.",
         [ARR, "Floor 3: Daksh, Hiten; floor 4: Gauri, Bindu"], natural=by_num, seconds=50)

# ---- F3 Intermediate: seven floors with a sport each
P = ["Jai", "Kiran", "Leela", "Manav", "Nisha", "Ojas", "Puja"]
SP = ["Badminton", "Chess", "Cricket", "Hockey", "Kabaddi", "Tennis", "Volleyball"]
conds = [
    ("Jai lives on an odd-numbered floor above floor 3 and likes Kabaddi.", ("Jai", "Kabaddi"),
     lambda j, k: j % 2 == 1 and j > 3 and j == k),
    ("Only two persons live between Jai and the person who likes Hockey.", ("Jai", "Hockey"),
     lambda j, h: abs(j - h) == 3),
    ("Ojas likes Hockey, and the person who likes Tennis lives immediately above Ojas.", ("Ojas", "Hockey", "Tennis"),
     lambda o, h, t: o == h and t == o + 1),
    ("Manav likes Volleyball and lives below Leela.", ("Manav", "Volleyball", "Leela"),
     lambda m, v, l: m == v and m < l),
    ("Puja lives immediately below Jai and likes Cricket.", ("Puja", "Jai", "Cricket"),
     lambda p, j, c: p == j - 1 and p == c),
    ("The person who likes Chess lives on the lowermost floor.", ("Chess",), lambda c: c == 1),
    ("Leela does not like Tennis.", ("Leela", "Tennis"), lambda l, t: l != t),
    ("Kiran lives above Nisha, and Leela lives above Jai.", ("Kiran", "Nisha", "Leela", "Jai"),
     lambda k, n, l, j: k > n and l > j),
]
F3 = unique(P + SP, {x: range(1, 8) for x in P + SP}, conds, [P, SP])
at = {F3[p]: p for p in P}
sport = {p: next(s for s in SP if F3[s] == F3[p]) for p in P}
assert [(at[i], sport[at[i]]) for i in range(1, 8)] == [
    ("Nisha", "Chess"), ("Ojas", "Hockey"), ("Kiran", "Tennis"), ("Puja", "Cricket"), ("Jai", "Kabaddi"),
    ("Manav", "Volleyball"), ("Leela", "Badminton")]
ARR = "Floor 1 to 7: " + ", ".join(f"{at[i]} ({sport[at[i]]})" for i in range(1, 8))
sid = stimulus("puzzle", "Seven persons on seven floors with favourite sports",
               "Seven persons Jai, Kiran, Leela, Manav, Nisha, Ojas and Puja live on the seven floors of a building, "
               "one on each floor (floor 1 is the lowermost, floor 7 the topmost). Each likes a different sport among "
               "Badminton, Chess, Cricket, Hockey, Kabaddi, Tennis and Volleyball.", conds,
               "Jai is on 5 or 7; Leela lives above him, so Jai = 5 and Puja (Cricket) = 4. Hockey is three floors "
               "from Jai: floor 2 (8 does not exist), so Ojas = 2 and Tennis = 3. Chess is on floor 1. Floors 1, 3, 6 "
               "and 7 remain for Kiran, Leela, Manav and Nisha. Manav likes Volleyball, so he is not on 1 (Chess) or 3 "
               "(Tennis); with Leela above him, Manav = 6 and Leela = 7. Kiran is above Nisha: Nisha = 1 (Chess), "
               "Kiran = 3 (Tennis). Leela gets the remaining sport, Badminton.\n\n"
               + table(["Floor", "Person", "Sport"], [(i, at[i], sport[at[i]]) for i in range(7, 0, -1)]))
ans = at[F3["Cricket"] + 1]
puzzle_q(sid, FLR, "Floor with attribute", "Intermediate",
         "Who lives immediately above the person who likes Cricket?", ans, ["Ojas", "Manav", "Kiran"],
         "Floor puzzle with one attribute", f"Puja (Cricket) is on floor 4, and {ans} lives on floor 5.",
         ["Leela above Jai rules out Jai = 7, so Jai = 5, Puja = 4", ARR, f"Floor 5: {ans}"], seconds=60)
assert ans == "Jai"
puzzle_q(sid, FLR, "Floor with attribute", "Intermediate", "Which sport does Kiran like?", sport["Kiran"],
         ["Chess", "Badminton", "Volleyball"], "Linking persons to attributes",
         "Kiran must be above Nisha among floors 1 and 3, so Kiran is on floor 3, which is the Tennis floor "
         "(immediately above Ojas).", [ARR],
         why_others_wrong="Chess is Nisha's (floor 1), Badminton Leela's and Volleyball Manav's.", seconds=60)
gap = abs(F3["Nisha"] - F3["Manav"]) - 1
puzzle_q(sid, FLR, "Floor with attribute", "Intermediate", "How many persons live between Nisha and Manav?",
         num_word(gap), ["Three", "Five", "Two"], "Counting floors",
         f"Nisha is on 1 and Manav on 6: {gap} persons (floors 2 to 5) live between them.", [ARR], natural=by_num,
         seconds=50)

# ---- F4 Advanced: nine floors, eight persons (one floor vacant), favourite fruit
P = ["Raghav", "Simran", "Tushar", "Ujjwala", "Vedant", "Waheeda", "Yuvraj", "Zeenat"]
FR = ["Apple", "Banana", "Cherry", "Guava", "Kiwi", "Mango", "Orange", "Papaya"]
conds = [
    ("The vacant floor is an even-numbered floor above floor 4.", ("Vacant",), lambda v: v % 2 == 0 and v > 4),
    ("Tushar lives immediately below the vacant floor and likes Banana.", ("Tushar", "Vacant", "Banana"),
     lambda t, v, b: t == v - 1 and t == b),
    ("Exactly two floors lie between Tushar's floor and the floor of the person who likes Mango.",
     ("Tushar", "Mango"), lambda t, m: abs(t - m) == 3),
    ("Vedant likes Mango and lives below Tushar.", ("Vedant", "Mango", "Tushar"), lambda v, m, t: v == m and v < t),
    ("The person who likes Papaya lives immediately above Zeenat, who lives on an odd-numbered floor.",
     ("Papaya", "Zeenat"), lambda p, z: p == z + 1 and z % 2 == 1),
    ("Simran lives below Vedant.", ("Simran", "Vedant"), lambda s, v: s < v),
    ("Exactly one floor lies between Ujjwala's floor and Waheeda's floor.", ("Ujjwala", "Waheeda"),
     lambda u, w: abs(u - w) == 2),
    ("Ujjwala lives above the vacant floor, and Yuvraj lives immediately above Ujjwala.",
     ("Ujjwala", "Vacant", "Yuvraj"), lambda u, v, y: u > v and y == u + 1),
    ("Yuvraj likes Orange, and the person who likes Guava lives immediately below him.",
     ("Yuvraj", "Orange", "Guava"), lambda y, o, g: y == o and g == o - 1),
    ("The person who likes Cherry lives above the person who likes Guava.", ("Cherry", "Guava"), lambda c, g: c > g),
    ("The person who likes Kiwi lives below the person who likes Apple.", ("Kiwi", "Apple"), lambda k, a: k < a),
    ("Raghav lives above Simran, and the number of floors between Simran and Raghav is the same as the number of "
     "floors between Raghav and Ujjwala.", ("Simran", "Raghav", "Ujjwala"), lambda s, r, u: r > s and r - s == u - r),
]
F4 = unique(["Vacant"] + P + FR, {x: range(1, 10) for x in ["Vacant"] + P + FR}, conds,
            [["Vacant"] + P, ["Vacant"] + FR])
at = {F4[p]: p for p in P}
fruit = {p: next(x for x in FR if F4[x] == F4[p]) for p in P}
assert F4["Vacant"] == 6 and [(at[i], fruit[at[i]]) for i in range(1, 10) if i != 6] == [
    ("Simran", "Kiwi"), ("Vedant", "Mango"), ("Zeenat", "Apple"), ("Raghav", "Papaya"), ("Tushar", "Banana"),
    ("Ujjwala", "Guava"), ("Yuvraj", "Orange"), ("Waheeda", "Cherry")]
ARR = "Floor 1 to 9: " + ", ".join(f"{at[i]} ({fruit[at[i]]})" if i in at else "vacant" for i in range(1, 10))
sid = stimulus("puzzle", "Eight persons in a nine-storey building with one vacant floor",
               "A building has nine floors, numbered 1 (lowermost) to 9 (topmost). Eight persons Raghav, Simran, "
               "Tushar, Ujjwala, Vedant, Waheeda, Yuvraj and Zeenat live in it, one on each floor, so exactly one "
               "floor is vacant. Each person likes a different fruit among Apple, Banana, Cherry, Guava, Kiwi, Mango, "
               "Orange and Papaya.", conds,
               "The vacant floor is 6 or 8. If it were 8, Tushar = 7 and Ujjwala (above the vacant floor) = 9 would "
               "leave no floor for Yuvraj above her: so the vacant floor is 6 and Tushar (Banana) = 5. Mango is three "
               "floors from Tushar and below him: Vedant (Mango) = 2, so Simran = 1. Ujjwala is on 7 or 8 with Yuvraj "
               "above; Ujjwala = 8 would put Waheeda on 6 (vacant) or 10, so Ujjwala = 7, Yuvraj (Orange) = 8 and "
               "Waheeda = 9. Raghav is midway between Simran (1) and Ujjwala (7): floor 4. Zeenat takes the odd floor "
               "3, with Papaya (Raghav) above her. Guava is immediately below Orange: Ujjwala. Cherry is above Guava: "
               "Waheeda. Apple and Kiwi remain for Zeenat and Simran; Kiwi is lower, so Simran likes Kiwi and Zeenat "
               "Apple.\n\n" + table(["Floor", "Person", "Fruit"],
                                    [(i, at.get(i, "(vacant)"), fruit.get(at.get(i), "-")) for i in range(9, 0, -1)]))
ans = fruit[at[F4["Vacant"] + 1]]
puzzle_q(sid, FLR, "Floor with attribute", "Advanced",
         "Which fruit does the person living immediately above the vacant floor like?", ans,
         ["Banana", "Orange", "Cherry"], "Floor puzzle with a vacant floor and an attribute",
         f"The vacant floor is 6. Floor 7 is Ujjwala's, and she likes {ans} (it is immediately below Yuvraj's "
         "Orange).", ["Vacant = 8 leaves no room for Yuvraj above Ujjwala, so vacant = 6, Tushar = 5", ARR,
                      f"Floor 7: Ujjwala ({ans})"],
         why_others_wrong="Banana is Tushar's, immediately below the vacant floor; Orange is two floors above it.",
         seconds=90)
assert ans == "Guava"
between = sum(1 for p in P if F4["Vedant"] < F4[p] < F4["Ujjwala"])
puzzle_q(sid, FLR, "Floor with attribute", "Advanced", "How many persons live between Vedant and Ujjwala?",
         num_word(between), ["Four", "Two", "Five"], "Do not count the vacant floor as a person",
         f"Floors 3 to 6 lie between Vedant (2) and Ujjwala (7), but floor 6 is vacant, so only Zeenat, Raghav and "
         f"Tushar live between them: {between}.", [ARR], natural=by_num,
         why_others_wrong="Four counts the vacant floor as a person.", seconds=75)
puzzle_q(sid, FLR, "Floor with attribute", "Advanced", "Who likes Apple?",
         next(p for p in P if fruit[p] == "Apple"), ["Simran", "Raghav", "Waheeda"], "Final elimination step",
         "After every other fruit is fixed, Apple and Kiwi remain for Zeenat (3) and Simran (1). Kiwi is below "
         "Apple, so Zeenat likes Apple.", [ARR], seconds=75)
stm = [("1 – Simran – Kiwi", F4["Simran"] == 1 and fruit["Simran"] == "Kiwi"),
       ("3 – Zeenat – Kiwi", F4["Zeenat"] == 3 and fruit["Zeenat"] == "Kiwi"),
       ("7 – Ujjwala – Cherry", F4["Ujjwala"] == 7 and fruit["Ujjwala"] == "Cherry"),
       ("4 – Raghav – Apple", F4["Raghav"] == 4 and fruit["Raghav"] == "Apple")]
t, f = one_true(stm)
puzzle_q(sid, FLR, "Floor with attribute", "Advanced",
         "Which of the following floor – person – fruit combinations is correct?", t, f,
         "Matching two attributes", "Simran lives on floor 1 and likes Kiwi; the other combinations each have the "
         "right floor but the wrong fruit.", [ARR], seconds=70)

# ================================================================================================ BOX PUZZLES
BOX = "Box-Based Puzzles"

# ---- B1 Basic: six stacked boxes
P = list("PQRSTU")
conds = [
    ("Box R is kept immediately above box U.", ("R", "U"), lambda r, u: r == u + 1),
    ("Only one box is kept between box R and box T, and box T is above box R.", ("R", "T"), lambda r, t: t == r + 2),
    ("Box P is kept immediately above box S.", ("P", "S"), lambda p, s: p == s + 1),
    ("Box P is kept below box U.", ("P", "U"), lambda p, u: p < u),
    ("Box Q is not kept adjacent to box U.", ("Q", "U"), lambda q_, u: abs(q_ - u) != 1),
]
B1 = unique(P, {p: range(1, 7) for p in P}, conds, [P])
at = {v: k for k, v in B1.items()}
assert [at[i] for i in range(1, 7)] == list("SPURQT")
ARR = "Bottom to top: " + ", ".join(at[i] for i in range(1, 7))
sid = stimulus("puzzle", "Six boxes in a stack",
               "Six boxes P, Q, R, S, T and U are kept one above another in a single stack. Position 1 is the bottom "
               "and position 6 the top.", conds,
               "U, R and T follow the pattern U, R, (one box), T, so U is at 1, 2 or 3. P sits on S and below U, so "
               "S and P need two positions under U: U = 3, R = 4, T = 6, S = 1, P = 2. Q takes position 5.\n\n"
               + table(["Position", "Box"], [(i, at[i]) for i in range(6, 0, -1)]))
puzzle_q(sid, BOX, "Stacked boxes", "Basic", "Which box is kept at the top of the stack?", at[6], ["Q", "R", "U"],
         "Stacked boxes: chain the 'immediately above' conditions",
         "U, R and T form the block U–R–(gap)–T, and S and P must fit below U, so U = 3 and T = 6 (top).",
         ["S and P are below U, so U ≥ 3; U = 3 is the only fit", ARR], seconds=45)
gap = abs(B1["S"] - B1["Q"]) - 1
puzzle_q(sid, BOX, "Stacked boxes", "Basic", "How many boxes are kept between box S and box Q?", num_word(gap),
         ["Two", "Four", "One"], "Counting positions", "S is at 1 and Q at 5, so P, U and R are between them.",
         [ARR], natural=by_num, seconds=40)
puzzle_q(sid, BOX, "Stacked boxes", "Basic", "Which box is kept immediately below box R?", at[B1["R"] - 1],
         ["Q", "P", "T"], "Adjacent positions", "R is immediately above U, so U is immediately below R.", [ARR],
         seconds=35)
mid = at[(B1["P"] + B1["T"]) // 2]
assert (B1["P"] + B1["T"]) % 2 == 0
puzzle_q(sid, BOX, "Stacked boxes", "Basic", "Which box is kept exactly midway between box P and box T?", mid,
         ["U", "Q", "S"], "Midpoint of two positions", f"P is at 2 and T at 6; the midpoint is position 4: {mid}.",
         [ARR], seconds=45)

# ---- B2 Intermediate: seven boxes with colours
P = list("KLMNOPQ")
CO = ["Black", "Blue", "Green", "Pink", "Red", "White", "Yellow"]
conds = [
    ("The green box is kept exactly in the middle of the stack, and box P is green.", ("Green", "P"),
     lambda g, p: g == 4 and p == g),
    ("Box O is kept above box P, with exactly two boxes between them.", ("O", "P"), lambda o, p: o == p + 3),
    ("Box L is pink and is kept immediately below box O.", ("L", "Pink", "O"),
     lambda l, pk, o: l == pk and l == o - 1),
    ("The red box is kept immediately above box N.", ("Red", "N"), lambda r, n: r == n + 1),
    ("Box K is kept immediately below the green box and is not red.", ("K", "Green", "Red"),
     lambda k, g, r: k == g - 1 and k != r),
    ("Only one box is kept between box K and the white box.", ("K", "White"), lambda k, w: abs(k - w) == 2),
    ("The yellow box is kept immediately above the green box.", ("Yellow", "Green"), lambda y, g: y == g + 1),
    ("Box Q is kept below box M.", ("Q", "M"), lambda q_, m: q_ < m),
    ("The blue box is kept above the pink box.", ("Blue", "Pink"), lambda b, pk: b > pk),
]
B2 = unique(P + CO, {x: range(1, 8) for x in P + CO}, conds, [P, CO])
at = {B2[p]: p for p in P}
col = {p: next(c for c in CO if B2[c] == B2[p]) for p in P}
assert [(at[i], col[at[i]]) for i in range(1, 8)] == [("N", "White"), ("Q", "Red"), ("K", "Black"), ("P", "Green"),
                                                       ("M", "Yellow"), ("L", "Pink"), ("O", "Blue")]
ARR = "Bottom to top: " + ", ".join(f"{at[i]} ({col[at[i]]})" for i in range(1, 8))
sid = stimulus("puzzle", "Seven coloured boxes in a stack",
               "Seven boxes K, L, M, N, O, P and Q are kept one above another in a single stack (position 1 is the "
               "bottom, 7 the top). Each box is of a different colour among Black, Blue, Green, Pink, Red, White and "
               "Yellow.", conds,
               "P (green) is at 4, so O = 7, L (pink) = 6, K = 3 and yellow = 5. Blue is above pink, so O is blue. "
               "White is two away from K: position 1 or 5, and 5 is yellow, so white = 1. Positions 1, 2 and 5 remain "
               "for M, N and Q. Red is immediately above N: N = 1 gives red = 2 (N = 2 would make K red, N = 5 would "
               "make L red). So N is white and red is at 2. Q is below M, so Q = 2 (red) and M = 5 (yellow); K is "
               "black.\n\n" + table(["Position", "Box", "Colour"],
                                    [(i, at[i], col[at[i]]) for i in range(7, 0, -1)]))
puzzle_q(sid, BOX, "Boxes with weights or colours", "Intermediate", "What is the colour of box M?", col["M"],
         ["Red", "Blue", "Black"], "Box puzzle with colours",
         "M and Q share positions 2 and 5; Q is below M, so M is at 5, which is the yellow position (immediately "
         "above green).",
         ["P (green) = 4, O = 7, L (pink) = 6, K = 3, yellow = 5, O blue", "White = 1, N = 1, red = 2", ARR],
         seconds=70)
puzzle_q(sid, BOX, "Boxes with weights or colours", "Intermediate", "Which box is red?",
         next(p for p in P if col[p] == "Red"), ["N", "K", "M"], "Placing the red box",
         "Red is immediately above N. N must be at 1 (other choices make K or L red), so the red box is at 2, which "
         "is box Q.", [ARR], why_others_wrong="K is explicitly not red; N is white; M is yellow.", seconds=65)
gap = abs(B2["White"] - B2["Pink"]) - 1
puzzle_q(sid, BOX, "Boxes with weights or colours", "Intermediate",
         "How many boxes are kept between the white box and the pink box?", num_word(gap), ["Three", "Five", "Two"],
         "Counting positions", f"White is at 1 and pink at 6, so {gap} boxes are between them.", [ARR],
         natural=by_num, seconds=50)
puzzle_q(sid, BOX, "Boxes with weights or colours", "Intermediate",
         "Which box is kept immediately above the black box?", at[B2["Black"] + 1], ["M", "Q", "L"],
         "Adjacent positions", f"The black box is K at 3; position 4 holds {at[B2['Black'] + 1]}.", [ARR], seconds=45)
stm = [("Box Q is kept immediately above box N", B2["Q"] == B2["N"] + 1), ("Box M is blue", col["M"] == "Blue"),
       ("The pink box is at the top of the stack", B2["Pink"] == 7),
       ("Exactly two boxes are kept between box K and box O", abs(B2["K"] - B2["O"]) - 1 == 2)]
t, f = one_true(stm)
puzzle_q(sid, BOX, "Boxes with weights or colours", "Intermediate", "Which of the following statements is true?",
         t, f, "Verifying statements", "N is at 1 and Q at 2, so Q is immediately above N.",
         [ARR, "M is yellow: false", "Pink (L) is at 6; the top box O is blue: false",
          "K (3) and O (7) have three boxes between them: false"], seconds=55)

# ---- B3 Advanced: nine boxes with colours
P = list("ABCDEFGHI")
CO = ["Blue", "Brown", "Green", "Grey", "Indigo", "Orange", "Red", "Violet", "Yellow"]
conds = [
    ("Box A is kept immediately below the yellow box.", ("A", "Yellow"), lambda a, y: a == y - 1),
    ("Three boxes are kept between box A and box G.", ("A", "G"), lambda a, g: abs(a - g) == 4),
    ("Box G is blue, and box E is kept immediately above it.", ("G", "Blue", "E"),
     lambda g, b, e: g == b and e == g + 1),
    ("The orange box is kept above box I.", ("Orange", "I"), lambda o, i: o > i),
    ("The number of boxes above box I is the same as the number of boxes below it.", ("I",), lambda i: i == 5),
    ("Box D is green and is kept immediately above box I.", ("D", "Green", "I"),
     lambda d, g, i: d == g and d == i + 1),
    ("Only one box is kept between box D and box G.", ("D", "G"), lambda d, g: abs(d - g) == 2),
    ("The violet box is kept immediately below the blue box.", ("Violet", "Blue"), lambda v, b: v == b - 1),
    ("Box C is indigo and is kept above box F.", ("C", "Indigo", "F"), lambda c, ind, f_: c == ind and c > f_),
    ("Only one box is kept between box C and box A.", ("C", "A"), lambda c, a: abs(c - a) == 2),
    ("Box H is red, and the brown box is kept immediately above it.", ("H", "Red", "Brown"),
     lambda h, r, b: h == r and b == r + 1),
    ("The grey box is kept below the red box.", ("Grey", "Red"), lambda g, r: g < r),
]
B3 = unique(P + CO, {x: range(1, 10) for x in P + CO}, conds, [P, CO])
at = {B3[p]: p for p in P}
col = {p: next(c for c in CO if B3[c] == B3[p]) for p in P}
assert [(at[i], col[at[i]]) for i in range(1, 10)] == [
    ("F", "Grey"), ("C", "Indigo"), ("H", "Red"), ("A", "Brown"), ("I", "Yellow"), ("D", "Green"), ("B", "Violet"),
    ("G", "Blue"), ("E", "Orange")]
ARR = "Bottom to top: " + ", ".join(f"{at[i]} ({col[at[i]]})" for i in range(1, 10))
sid = stimulus("puzzle", "Nine coloured boxes in a stack",
               "Nine boxes A, B, C, D, E, F, G, H and I are kept one above another in a single stack (position 1 is "
               "the bottom, 9 the top). Each box is of a different colour among Blue, Brown, Green, Grey, Indigo, "
               "Orange, Red, Violet and Yellow.", conds,
               "I has four boxes above and four below: I = 5, so D (green) = 6. G is two from D: 4 or 8. If G = 4, A "
               "(four away) = 8 and E (above G) = 5 = I: rejected. So G (blue) = 8, E = 9, A = 4 and yellow = 5 (I). "
               "Violet = 7. C is two from A: 2 (6 is D), so C (indigo) = 2 and F (below C) = 1. B and H take 3 and 7; "
               "the brown box sits on red H, and 8 is blue, so H = 3 (red), A is brown and B = 7 (violet). Grey is "
               "below red: F. The last colour, orange, goes to E, which is above I as required.\n\n"
               + table(["Position", "Box", "Colour"], [(i, at[i], col[at[i]]) for i in range(9, 0, -1)]))
puzzle_q(sid, BOX, "Boxes with weights or colours", "Advanced", "Which box is kept immediately below the brown box?",
         at[B3["Brown"] - 1], ["C", "I", "F"], "Nine-box stack with colours",
         "The brown box is A at 4 (it sits on the red box H), so H is immediately below it.",
         ["I = 5, D = 6; G = 4 would put E on I's position, so G = 8, E = 9, A = 4", "C = 2, F = 1, H = 3, B = 7",
          ARR], seconds=90)
gap = abs(B3["Indigo"] - B3["Blue"]) - 1
puzzle_q(sid, BOX, "Boxes with weights or colours", "Advanced",
         "How many boxes are kept between the indigo box and the blue box?", num_word(gap), ["Four", "Six", "Three"],
         "Counting positions", f"Indigo (C) is at 2 and blue (G) at 8: {gap} boxes lie between them.", [ARR],
         natural=by_num, seconds=70)
puzzle_q(sid, BOX, "Boxes with weights or colours", "Advanced",
         "What is the colour of the box kept immediately above box D?", col[at[B3["D"] + 1]],
         ["Blue", "Yellow", "Brown"], "Colour lookup",
         "D is at 6; position 7 holds B, which is violet (immediately below the blue box).", [ARR], seconds=60)
stm = [("Box E is orange", col["E"] == "Orange"), ("Box F is at the bottom of the stack", B3["F"] == 1),
       ("The grey box is kept immediately below the indigo box", B3["Grey"] == B3["Indigo"] - 1),
       ("Box B is kept immediately above box G", B3["B"] == B3["G"] + 1)]
t, f = one_false(stm)
puzzle_q(sid, BOX, "Boxes with weights or colours", "Advanced", "Which of the following statements is NOT true?",
         t, f, "Finding the false statement", "B is at 7, immediately below G (8), not above it.",
         [ARR, "E is orange: true", "F is at 1: true", "Grey F (1) is immediately below indigo C (2): true"],
         seconds=60)

# ================================================================================================ MONTH / DATE / YEAR
MON = "Month and Date-Based Puzzles"
MONTHS = ["January", "February", "March", "April", "May", "June"]
DAYS_IN = {1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30}

# ---- M1 Basic
P = ["Aditi", "Bhuvan", "Charvi", "Dhruv", "Eshwar", "Falguni"]
conds = [
    ("Aditi was born in a month that has 31 days.", ("Aditi",), lambda a: DAYS_IN[a] == 31),
    ("Only one person was born between Aditi and Bhuvan.", ("Aditi", "Bhuvan"), lambda a, b: abs(a - b) == 2),
    ("Charvi was born in a month after Bhuvan's.", ("Charvi", "Bhuvan"), lambda c, b: c > b),
    ("Dhruv was born in a month before Falguni's.", ("Dhruv", "Falguni"), lambda d, f_: d < f_),
    ("Eshwar was born in a month that has 30 days.", ("Eshwar",), lambda e: DAYS_IN[e] == 30),
    ("Falguni was born in the month immediately before Aditi's.", ("Falguni", "Aditi"), lambda f_, a: f_ == a - 1),
]
M1 = unique(P, {p: range(1, 7) for p in P}, conds, [P])
at = {v: k for k, v in M1.items()}
assert [at[i] for i in range(1, 7)] == ["Dhruv", "Falguni", "Aditi", "Eshwar", "Bhuvan", "Charvi"]
ARR = "January to June: " + ", ".join(at[i] for i in range(1, 7))
sid = stimulus("puzzle", "Six birthdays from January to June",
               "Six persons Aditi, Bhuvan, Charvi, Dhruv, Eshwar and Falguni were born in six different months from "
               "January to June of the same (non-leap) year, one person in each month.", conds,
               "Aditi is in January, March or May. Falguni is immediately before her and Dhruv before Falguni, so "
               "Aditi cannot be in January. If Aditi were in May, Bhuvan would be in March, Charvi in June and "
               "Falguni in April, leaving no 30-day month (April or June) for Eshwar: rejected. So Aditi = March, "
               "Falguni = February, Dhruv = January, Bhuvan = May (January is taken), Charvi = June and Eshwar = "
               "April.\n\n" + table(["Month", "Person"], [(MONTHS[i - 1], at[i]) for i in range(1, 7)]))
puzzle_q(sid, MON, "Month-based", "Basic", "In which month was Charvi born?", MONTHS[M1["Charvi"] - 1],
         ["May", "April", "March"], "Month puzzle: test the 31-day options for Aditi",
         "Aditi = May fails (no 30-day month left for Eshwar), so Aditi = March, Bhuvan = May and Charvi, born after "
         "Bhuvan, = June.", ["Aditi ∈ {January, March, May}; January fails (Falguni and Dhruv must be earlier)",
                             "Aditi = May leaves no 30-day month for Eshwar", ARR], seconds=60)
gap = abs(M1["Dhruv"] - M1["Bhuvan"]) - 1
puzzle_q(sid, MON, "Month-based", "Basic", "How many persons were born between Dhruv and Bhuvan?", num_word(gap),
         ["Two", "Four", "One"], "Counting months",
         f"Dhruv (January) and Bhuvan (May): February, March and April lie between, so {gap} persons.", [ARR],
         natural=by_num, seconds=45)
puzzle_q(sid, MON, "Month-based", "Basic", "Who was born in the month immediately after Aditi's?",
         at[M1["Aditi"] + 1], ["Bhuvan", "Falguni", "Charvi"], "Adjacent months",
         f"Aditi was born in March; April belongs to {at[M1['Aditi'] + 1]}.", [ARR],
         why_others_wrong="Falguni is immediately before Aditi; Bhuvan is two months after her.", seconds=40)

# ---- M2 Intermediate: 4 months x 2 dates
P = ["Harini", "Imran", "Jyoti", "Karthik", "Madhav", "Naina", "Omar", "Parul"]
MN = {1: "March", 2: "June", 3: "September", 4: "December"}
mon = lambda s: (s + 1) // 2
day = lambda s: 24 if s % 2 == 0 else 9
D31 = {1: True, 2: False, 3: False, 4: True}
label = lambda s: f"{day(s)} {MN[mon(s)]}"
conds = [
    ("Harini's birthday is on the 24th of a month that has 30 days.", ("Harini",),
     lambda h: day(h) == 24 and not D31[mon(h)]),
    ("Only two persons have birthdays between Harini's and Madhav's.", ("Harini", "Madhav"),
     lambda h, m: abs(h - m) == 3),
    ("Madhav's birthday is in a month that has 31 days.", ("Madhav",), lambda m: D31[mon(m)]),
    ("Jyoti's birthday comes immediately after Madhav's.", ("Jyoti", "Madhav"), lambda j, m: j == m + 1),
    ("Imran and Parul have birthdays in the same month, Parul's before Imran's.", ("Imran", "Parul"),
     lambda i, p: mon(i) == mon(p) and p < i),
    ("Karthik's birthday is on the 24th and comes before Omar's.", ("Karthik", "Omar"),
     lambda k, o: day(k) == 24 and k < o),
    ("Naina's birthday is not in June.", ("Naina",), lambda n: mon(n) != 2),
]
M2 = unique(P, {p: range(1, 9) for p in P}, conds, [P])
at = {v: k for k, v in M2.items()}
assert [at[i] for i in range(1, 9)] == ["Naina", "Karthik", "Omar", "Harini", "Parul", "Imran", "Madhav", "Jyoti"]
ARR = "In date order: " + ", ".join(f"{label(i)} – {at[i]}" for i in range(1, 9))
sid = stimulus("puzzle", "Eight birthdays on the 9th and 24th of four months",
               "Eight persons Harini, Imran, Jyoti, Karthik, Madhav, Naina, Omar and Parul have their birthdays in "
               "the same year on different dates. Each birthday falls on either the 9th or the 24th of March, June, "
               "September or December, and no two persons share a date.", conds,
               "Harini is on 24 June or 24 September. Madhav is three dates away in a 31-day month: from 24 June that "
               "is 9 March or 9 December; from 24 September it would be 9 June or beyond 24 December, so Harini = "
               "24 June. If Madhav were 9 March (Jyoti 24 March), Imran and Parul would take September or December and "
               "Karthik the remaining 24th, leaving no later date for Omar: rejected. So Madhav = 9 December and "
               "Jyoti = 24 December. Imran and Parul need a month with both dates free: September (March would leave "
               "only 24 September for Karthik and nothing after it for Omar). So Parul = 9 September, Imran = "
               "24 September. Karthik takes 24 March; Naina is not in June, so Naina = 9 March and Omar = 9 June.\n\n"
               + table(["Date", "Person"], [(label(i), at[i]) for i in range(1, 9)]))
puzzle_q(sid, MON, "Date-based", "Intermediate", "Whose birthday is on 9 June?", at[3],
         ["Naina", "Karthik", "Parul"], "Month-and-date puzzle: eight ordered slots",
         "After Harini (24 June), Madhav (9 December), Jyoti, Parul and Imran are fixed, Karthik must be 24 March and "
         "Naina, barred from June, takes 9 March. So 9 June is Omar's.",
         ["Harini = 24 June (24 September has no valid Madhav)", "Madhav = 9 December, Jyoti = 24 December",
          "Parul = 9 September, Imran = 24 September", ARR], seconds=75)
assert at[3] == "Omar"
gap = abs(M2["Karthik"] - M2["Imran"]) - 1
puzzle_q(sid, MON, "Date-based", "Intermediate", "How many persons have birthdays between Karthik's and Imran's?",
         num_word(gap), ["Two", "Four", "Five"], "Counting dates",
         f"Karthik (24 March) and Imran (24 September): Omar, Harini and Parul lie between, so {gap}.", [ARR],
         natural=by_num, seconds=55)
puzzle_q(sid, MON, "Date-based", "Intermediate", "Whose birthday comes immediately before Parul's?",
         at[M2["Parul"] - 1], ["Omar", "Imran", "Madhav"], "Adjacent dates",
         f"Parul is on 9 September; the previous date in the list is 24 June: {at[M2['Parul'] - 1]}.", [ARR],
         seconds=50)
march = [at[i] for i in (1, 2)]
puzzle_q(sid, MON, "Date-based", "Intermediate", "Which two persons have their birthdays in March?",
         f"{march[0]} and {march[1]}", ["Madhav and Jyoti", "Karthik and Omar", "Naina and Omar"],
         "Month grouping", "9 March is Naina's and 24 March is Karthik's.", [ARR],
         why_others_wrong="Madhav and Jyoti are the December pair; Omar is in June.", seconds=55)
puzzle_q(sid, MON, "Date-based", "Intermediate", "On which date is Jyoti's birthday?", label(M2["Jyoti"]),
         ["9 December", "24 March", "24 September"], "Date lookup",
         "Jyoti comes immediately after Madhav (9 December), so her birthday is 24 December.", [ARR], seconds=45)

# ---- M3 Advanced: birth years and professions (ages as on 2026)
P = ["Ashwin", "Bharti", "Chandan", "Damini", "Ehsaan", "Fiza", "Gopal"]
YRS = [1968, 1974, 1979, 1985, 1990, 1997, 2003]
JB = ["Architect", "Banker", "Chef", "Doctor", "Engineer", "Farmer", "Lawyer"]
age = lambda y: 2026 - y
isprime = lambda n: n > 1 and all(n % d for d in range(2, int(n ** 0.5) + 1))
conds = [
    ("Damini's age is a prime number.", ("Damini",), lambda d: isprime(age(d))),
    ("The sum of the ages of Damini and Chandan is 70 years.", ("Damini", "Chandan"),
     lambda d, c: age(d) + age(c) == 70),
    ("Bharti is older than Fiza, and Fiza was born in an even-numbered year.", ("Bharti", "Fiza"),
     lambda b, f_: b < f_ and f_ % 2 == 0),
    ("Ehsaan was born in an odd-numbered year after 1990, and Chandan is younger than Ehsaan.",
     ("Ehsaan", "Chandan"), lambda e, c: e % 2 == 1 and e > 1990 and c > e),
    ("Ashwin is the Banker, and the Banker is exactly 5 years older than the Architect.",
     ("Ashwin", "Banker", "Architect"), lambda a, b, ar: a == b and age(b) - age(ar) == 5),
    ("The Doctor was born in the 1960s.", ("Doctor",), lambda d: 1960 <= d <= 1969),
    ("The Chef was born in an even-numbered year, and Gopal is not the Chef.", ("Chef", "Gopal"),
     lambda c, g: c % 2 == 0 and c != g),
    ("The Engineer's age is a prime number, and Ehsaan is not the Engineer.", ("Engineer", "Ehsaan"),
     lambda e, h: isprime(age(e)) and e != h),
    ("The Lawyer is exactly 6 years older than the Farmer.", ("Lawyer", "Farmer"),
     lambda l, f_: age(l) - age(f_) == 6),
    ("Damini is not the Architect, and Gopal is younger than Ashwin.", ("Damini", "Architect", "Gopal", "Ashwin"),
     lambda d, ar, g, a: d != ar and g > a),
]
M3 = unique(P + JB, {x: YRS for x in P + JB}, conds, [P, JB])
job = {p: next(j for j in JB if M3[j] == M3[p]) for p in P}
older = sorted(P, key=M3.get)
assert [(p, M3[p], job[p]) for p in older] == [
    ("Bharti", 1968, "Doctor"), ("Fiza", 1974, "Chef"), ("Damini", 1979, "Engineer"), ("Ashwin", 1985, "Banker"),
    ("Gopal", 1990, "Architect"), ("Ehsaan", 1997, "Lawyer"), ("Chandan", 2003, "Farmer")]
ARR = "; ".join(f"{p}: {M3[p]} (age {age(M3[p])}), {job[p]}" for p in older)
sid = stimulus("puzzle", "Seven persons: birth years and professions",
               "Seven persons Ashwin, Bharti, Chandan, Damini, Ehsaan, Fiza and Gopal were born in different years "
               "among 1968, 1974, 1979, 1985, 1990, 1997 and 2003. Each has a different profession among Architect, "
               "Banker, Chef, Doctor, Engineer, Farmer and Lawyer. Ages are calculated as on 2026 (2026 minus the "
               "birth year), so the possible ages are 58, 52, 47, 41, 36, 29 and 23.", conds,
               "Ehsaan is 1997 or 2003, and Chandan is younger, so Ehsaan = 1997 (29) and Chandan = 2003 (23). "
               "Damini's age is 70 − 23 = 47 (prime): 1979. The Banker–Architect gap of 5 years fits 52/47 or 41/36; "
               "47 is Damini, who is not the Architect, so the Banker is 41 (1985: Ashwin) and the Architect is 36 "
               "(1990). Gopal is younger than Ashwin, and only 1990 is still free after 1985, so Gopal is the "
               "Architect. Bharti and Fiza take 1968 and 1974; Bharti is older, so Bharti = 1968 (the Doctor) and Fiza "
               "= 1974. The Lawyer is 6 years older than the Farmer: 29 and 23, so Ehsaan is the Lawyer and Chandan "
               "the Farmer. The Engineer's age is prime: Damini (47). Fiza is the Chef (1974 is even).\n\n"
               + table(["Person", "Birth year", "Age in 2026", "Profession"],
                       [(p, M3[p], age(M3[p]), job[p]) for p in older]))
s = age(M3["Chef"]) + age(M3["Farmer"])
puzzle_q(sid, MON, "Year-based", "Advanced", "What is the sum of the ages of the Chef and the Farmer?",
         f"{s} years", ["70 years", "81 years", "64 years"], "Year-based puzzle: ages from birth years",
         f"The Chef is Fiza (1974, age 52) and the Farmer is Chandan (2003, age 23): 52 + 23 = {s} years.",
         ["Ehsaan = 1997, Chandan = 2003, Damini = 1979", "Banker (Ashwin) = 1985, Architect (Gopal) = 1990",
          "Bharti = 1968 (Doctor), Fiza = 1974 (Chef)", "Lawyer Ehsaan, Farmer Chandan, Engineer Damini", ARR],
         natural=by_num, why_others_wrong="70 is Damini + Chandan (Engineer + Farmer).", seconds=90)
assert s == 75
puzzle_q(sid, MON, "Year-based", "Advanced", "Who is the Engineer?", next(p for p in P if job[p] == "Engineer"),
         ["Fiza", "Ehsaan", "Gopal"], "Elimination with a numeric property",
         "Only Fiza (52) and Damini (47) remain for Chef and Engineer; the Engineer's age is prime, so Damini is the "
         "Engineer.", [ARR], seconds=75)
n = sum(1 for p in P if age(M3["Lawyer"]) < age(M3[p]) < age(M3["Doctor"]))
puzzle_q(sid, MON, "Year-based", "Advanced",
         "How many persons are older than the Lawyer but younger than the Doctor?", num_word(n),
         ["Three", "Five", "Two"], "Range counting",
         f"The Lawyer is 29 and the Doctor 58; ages 52, 47, 41 and 36 lie strictly between: {n} persons.", [ARR],
         natural=by_num, seconds=70)

# ================================================================================================ PUZZLES (OTHER)
OTH = "Puzzles (Other)"

# ---- O1 Basic (standalone): height order
P = ["Ravi", "Sanjay", "Tarun", "Uma", "Vani"]
conds = [("Sanjay is taller than Uma but shorter than Vani.", ("Sanjay", "Uma", "Vani"),
          lambda s_, u, v: u < s_ < v),
         ("Ravi is taller than Vani.", ("Ravi", "Vani"), lambda r, v: r > v),
         ("Tarun is shorter than Uma.", ("Tarun", "Uma"), lambda t, u: t < u)]
O1 = unique(P, {p: range(1, 6) for p in P}, conds, [P])  # 5 = tallest
tall = sorted(P, key=O1.get, reverse=True)
assert tall == ["Ravi", "Vani", "Sanjay", "Uma", "Tarun"]
mcq(OTH, "Comparison and ordering", "Basic",
    "Five friends Ravi, Sanjay, Tarun, Uma and Vani have different heights. " + " ".join(t for t, _, _ in conds) +
    "\n\nWho is the second tallest?", tall[1],
    ["Sanjay", "Ravi", "Uma"], "Combining comparisons into one chain",
    "Join the statements: Ravi > Vani > Sanjay > Uma > Tarun. The second tallest is Vani.",
    ["Vani > Sanjay > Uma (statement 1)", "Ravi > Vani (statement 2) → Ravi > Vani > Sanjay > Uma",
     "Uma > Tarun (statement 3) → Ravi > Vani > Sanjay > Uma > Tarun", "Second from the top: Vani"],
    shortcut="Only Ravi is above Vani, so Vani must be second.", seconds=35, verified_by=BRUTE)

# ---- O2 Basic (standalone): days of the week
P = ["Kabir", "Lina", "Mansi", "Nakul", "Ojasvi"]
conds = [("Mansi visits on Wednesday.", ("Mansi",), lambda m: m == 3),
         ("Lina visits on the day immediately after Kabir.", ("Lina", "Kabir"), lambda l, k: l == k + 1),
         ("Nakul visits on the day immediately before Mansi.", ("Nakul", "Mansi"), lambda n, m: n == m - 1),
         ("Ojasvi visits on a day before Kabir.", ("Ojasvi", "Kabir"), lambda o, k: o < k)]
O2 = unique(P, {p: range(1, 6) for p in P}, conds, [P])
at = {v: k for k, v in O2.items()}
assert [at[i] for i in range(1, 6)] == ["Ojasvi", "Nakul", "Mansi", "Kabir", "Lina"]
mcq(OTH, "Day-based", "Basic",
    "Five customers Kabir, Lina, Mansi, Nakul and Ojasvi visit a bank branch on five different days from Monday to "
    "Friday of the same week, one customer per day. " + " ".join(t for t, _, _ in conds) +
    "\n\nWho visits the branch on Friday?", at[5], ["Kabir", "Ojasvi", "Nakul"], "Day-based ordering",
    "Mansi = Wednesday and Nakul = Tuesday. Kabir and Lina need two consecutive free days with Ojasvi earlier: "
    "Thursday and Friday, leaving Monday for Ojasvi. So Lina visits on Friday.",
    ["Mansi = Wednesday, Nakul = Tuesday", "Free days: Monday, Thursday, Friday",
     "Kabir–Lina must be consecutive: Thursday–Friday", "Ojasvi = Monday (before Kabir)",
     "Order: Ojasvi, Nakul, Mansi, Kabir, Lina"], seconds=40, verified_by=BRUTE)

# ---- O3 Intermediate set: designations in a bank
P = ["Ira", "Jeet", "Kashvi", "Laksh", "Mihir", "Navya", "Pihu"]
POSTS = ["General Manager", "Deputy General Manager", "Assistant General Manager", "Chief Manager",
         "Senior Manager", "Manager", "Assistant Manager"]
conds = [
    ("Exactly two persons are senior to Pihu.", ("Pihu",), lambda p: p == 3),
    ("Jeet is junior to Pihu but senior to Navya.", ("Jeet", "Pihu", "Navya"), lambda j, p, n: p < j < n),
    ("Only one person is designated between Jeet and Kashvi.", ("Jeet", "Kashvi"), lambda j, k: abs(j - k) == 2),
    ("Laksh is junior to both Kashvi and Jeet.", ("Laksh", "Kashvi", "Jeet"), lambda l, k, j: l > k and l > j),
    ("Ira is immediately junior to Mihir.", ("Ira", "Mihir"), lambda i, m: i == m + 1),
    ("Navya is not the Manager.", ("Navya",), lambda n: n != 6),
]
O3 = unique(P, {p: range(1, 8) for p in P}, conds, [P])
at = {v: k for k, v in O3.items()}
assert [at[i] for i in range(1, 8)] == ["Mihir", "Ira", "Pihu", "Jeet", "Navya", "Kashvi", "Laksh"]
ARR = "Senior to junior: " + ", ".join(f"{at[i]} ({POSTS[i - 1]})" for i in range(1, 8))
sid = stimulus("puzzle", "Seven officers and seven designations",
               "Seven officers Ira, Jeet, Kashvi, Laksh, Mihir, Navya and Pihu of a bank hold seven different posts. "
               "In decreasing order of seniority the posts are: General Manager, Deputy General Manager, Assistant "
               "General Manager, Chief Manager, Senior Manager, Manager and Assistant Manager.", conds,
               "Pihu is third (Assistant General Manager). Jeet is fourth, fifth or sixth. Jeet fifth: Kashvi would be "
               "third (Pihu's) or seventh (leaving no junior post for Laksh): rejected. Jeet sixth: Navya and Laksh "
               "are both junior to him and only the seventh post is left: rejected. So Jeet is fourth (Chief "
               "Manager) and Kashvi is second or sixth. Kashvi second: nobody can take the first post (Mihir there "
               "would push Ira onto Kashvi's post): rejected. So Kashvi is sixth (Manager), Laksh seventh, Navya fifth "
               "(junior to Jeet, not the Manager), and Mihir and Ira take the first and second posts.\n\n"
               + table(["Seniority", "Post", "Officer"], [(i, POSTS[i - 1], at[i]) for i in range(1, 8)]))
puzzle_q(sid, OTH, "Designation", "Intermediate", "Who is the Senior Manager?", at[5], ["Kashvi", "Jeet", "Laksh"],
         "Designation puzzle: an ordered hierarchy",
         "Jeet must be the Chief Manager and Kashvi the Manager; Navya is junior to Jeet but not the Manager, and the "
         "Assistant Manager post goes to Laksh, so Navya is the Senior Manager.",
         ["Pihu = 3rd", "Jeet = 5th or 6th fails; Jeet = 4th", "Kashvi = 2nd leaves the 1st post empty; Kashvi = 6th",
          ARR], seconds=70)
assert at[5] == "Navya"
n = O3["Kashvi"] - 1
puzzle_q(sid, OTH, "Designation", "Intermediate", "How many persons are senior to Kashvi?", num_word(n),
         ["Four", "Three", "Six"], "Counting seniors",
         f"Kashvi is the Manager, sixth in seniority, so {n} persons are senior to her.", [ARR], natural=by_num,
         seconds=55)
puzzle_q(sid, OTH, "Designation", "Intermediate", "Which post does Ira hold?", POSTS[O3["Ira"] - 1],
         ["General Manager", "Assistant General Manager", "Chief Manager"], "Consecutive posts",
         "Mihir and Ira hold two consecutive posts with Mihir senior; the only consecutive pair left is first and "
         "second, so Ira is the Deputy General Manager.", [ARR], seconds=55)

# ---- O4 Advanced (standalone): week schedule with subjects
P = ["Pooja", "Qasim", "Rahul", "Sana", "Tejas", "Urvi", "Vinay"]
SU = ["Audit", "Credit", "Forex", "Insurance", "Loans", "Risk", "Treasury"]
conds = [
    ("Exactly three sessions are held after Pooja's session.", ("Pooja",), lambda p: p == 4),
    ("Urvi attends the Credit session on the day immediately after Pooja.", ("Urvi", "Credit", "Pooja"),
     lambda u, c, p: u == c and u == p + 1),
    ("Rahul attends on a day after Urvi, but not on Sunday.", ("Rahul", "Urvi"), lambda r, u: r > u and r != 7),
    ("Tejas attends on a weekend day and his subject is Insurance.", ("Tejas", "Insurance"),
     lambda t, i: t >= 6 and t == i),
    ("The Forex session is held on the day immediately before Sana's session.", ("Forex", "Sana"),
     lambda f_, s_: f_ == s_ - 1),
    ("Only one session is held between the Audit session and the Credit session.", ("Audit", "Credit"),
     lambda a, c: abs(a - c) == 2),
    ("The Treasury session is held on the day immediately after the Audit session.", ("Treasury", "Audit"),
     lambda t, a: t == a + 1),
    ("The Loans session is held after the Treasury session.", ("Loans", "Treasury"), lambda l, t: l > t),
    ("Qasim attends the Risk session, on a day before Vinay's.", ("Qasim", "Risk", "Vinay"),
     lambda q_, r, v: q_ == r and q_ < v),
]
O4 = unique(P + SU, {x: range(1, 8) for x in P + SU}, conds, [P, SU])
at = {O4[p]: p for p in P}
sub = {p: next(x for x in SU if O4[x] == O4[p]) for p in P}
assert [(at[i], sub[at[i]]) for i in range(1, 8)] == [
    ("Qasim", "Risk"), ("Vinay", "Forex"), ("Sana", "Audit"), ("Pooja", "Treasury"), ("Urvi", "Credit"),
    ("Rahul", "Loans"), ("Tejas", "Insurance")]
mcq(OTH, "Day-based", "Advanced",
    "Seven trainees Pooja, Qasim, Rahul, Sana, Tejas, Urvi and Vinay attend one training session each on the seven "
    "days of a week from Monday to Sunday, one trainee per day. Each session is on a different subject among Audit, "
    "Credit, Forex, Insurance, Loans, Risk and Treasury.\n" + "\n".join(f"- {t}" for t, _, _ in conds) +
    "\n\nWho attends on Tuesday, and on which subject?", f"{at[2]} – {sub[at[2]]}",
    ["Vinay – Audit", "Sana – Forex", "Qasim – Forex"], "Day-based puzzle with an attribute",
    "Pooja = Thursday, Urvi (Credit) = Friday. Audit is two days from Credit: Wednesday (Sunday would leave no day "
    "after it for Treasury). Treasury = Thursday (Pooja). Rahul is after Friday but not on Sunday, so Rahul = "
    "Saturday and Tejas (Insurance) = Sunday; Loans, after Treasury, is Saturday (Rahul). Monday to Wednesday remain "
    "for Qasim, Sana and Vinay; Forex is the day before Sana and Qasim (Risk) is before Vinay. The only fit is Qasim "
    "(Risk) Monday, Vinay (Forex) Tuesday, Sana (Audit) Wednesday.",
    ["Pooja = Thursday (three days after her); Urvi = Friday (Credit)",
     "Audit = Wednesday (Sunday fails: Treasury must follow Audit); Treasury = Thursday",
     "Rahul = Saturday (after Friday, not Sunday); Tejas = Sunday (Insurance); Loans = Saturday",
     "Sana on Monday has no Forex day before her; Sana on Tuesday needs Forex on Monday (Vinay, since Qasim has "
     "Risk), but then Qasim would be on Wednesday, which is Audit: rejected",
     "So Sana = Wednesday (Audit), Forex = Tuesday = Vinay, Qasim (Risk) = Monday",
     "Final: Mon Qasim (Risk), Tue Vinay (Forex), Wed Sana (Audit), Thu Pooja (Treasury), Fri Urvi (Credit), "
     "Sat Rahul (Loans), Sun Tejas (Insurance)"],
    why_others_wrong="Sana attends Audit on Wednesday; Qasim's subject is Risk (Monday).", seconds=150,
    verified_by=BRUTE)

# ---- O5 Advanced (standalone): heights with numeric bounds
P = ["Akash", "Bhumi", "Chaitanya", "Diya", "Emran", "Fatima", "Girish"]
conds = [("Bhumi is taller than Diya but shorter than Emran.", ("Bhumi", "Diya", "Emran"),
          lambda b, d, e: d < b < e),
         ("Only one person is taller than Fatima.", ("Fatima",), lambda f_: f_ == 6),
         ("Akash is taller than Emran, and Emran is shorter than Fatima.", ("Akash", "Emran", "Fatima"),
          lambda a, e, f_: a > e and e < f_),
         ("Girish is shorter than Diya but taller than Chaitanya.", ("Girish", "Diya", "Chaitanya"),
          lambda g, d, c: c < g < d)]
O5 = unique(P, {p: range(1, 8) for p in P}, conds, [P])  # 7 = tallest
tall = sorted(P, key=O5.get, reverse=True)
assert tall == ["Akash", "Fatima", "Emran", "Bhumi", "Diya", "Girish", "Chaitanya"]
HT = {"Emran": 171, "Diya": 160}
cands = ["158 cm", "165 cm", "172 cm", "176 cm"]
assert [c for c in cands if HT["Diya"] < int(c.split()[0]) < HT["Emran"]] == ["165 cm"]
mcq(OTH, "Comparison and ordering", "Advanced",
    "Seven persons Akash, Bhumi, Chaitanya, Diya, Emran, Fatima and Girish have different heights (in whole "
    "centimetres).\n" + "\n".join(f"- {t}" for t, _, _ in conds) +
    "\n- The tallest person is 182 cm tall and the shortest 150 cm.\n- Emran's height is 171 cm and Diya's is 160 cm."
    "\n\nWhich of the following could be Bhumi's height?", "165 cm", ["158 cm", "172 cm", "176 cm"],
    "Ordering plus numeric bounds",
    "The full order is Akash > Fatima > Emran > Bhumi > Diya > Girish > Chaitanya. Bhumi is between Diya (160) and "
    "Emran (171), so her height must be strictly between 160 and 171 cm: only 165 cm fits.",
    ["Akash > Emran and Fatima > Emran; only one person is above Fatima, so it must be Akash: Akash, Fatima, Emran",
     "Emran > Bhumi > Diya > Girish > Chaitanya",
     "Bhumi lies strictly between Diya (160) and Emran (171)",
     "158 < 160, while 172 and 176 exceed 171: impossible; 165 fits"],
    why_others_wrong="158 cm would make Bhumi shorter than Diya; 172 and 176 cm would make her taller than Emran.",
    seconds=100, verified_by=BRUTE)

# ================================================================================================ SYLLOGISM
SYL = "Syllogism"
ONLY_I, ONLY_II, NEITHER, BOTH = OPT4


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


# ---- Basic (two statements)
syl_q("Basic", "Two-statement", N(("pen", "pens"), ("pencil", "pencils"), ("eraser", "erasers")),
      [("all", "pen", "pencil"), ("some", "pencil", "eraser")],
      [("some", "pen", "eraser"), ("some", "eraser", "pencil")], ONLY_II,
      "All + Some gives no definite link between the end terms; 'some' converts",
      "The pencils that are erasers need not be pens, so I does not follow. 'Some pencils are erasers' converts to "
      "'Some erasers are pencils', so II follows.",
      ["All pens are pencils, Some pencils are erasers: the middle term 'pencils' is not fully covered in the "
       "'some' statement, so no pen–eraser link is certain", "I: not definite (pens may lie outside the eraser "
       "part of pencils)", "II: conversion of 'Some pencils are erasers' gives 'Some erasers are pencils': follows"],
      shortcut="All + Some = no conclusion between the end terms.",
      why="Only I is the classic trap: the 'some' part of pencils may not include any pen.", seconds=35)
syl_q("Basic", "Two-statement", N(("file", "files"), ("folder", "folders"), ("drawer", "drawers")),
      [("some", "file", "folder"), ("no", "folder", "drawer")],
      [("somenot", "file", "drawer"), ("no", "file", "drawer")], ONLY_I,
      "Some + No = Some not",
      "The files that are folders cannot be drawers, so some files are definitely not drawers (I follows). Other "
      "files may still be drawers, so 'No file is a drawer' is not certain.",
      ["Some files are folders; no folder is a drawer", "Those files that are folders are not drawers ⇒ Some files "
       "are not drawers: I follows", "Files outside 'folders' are unrestricted, so some files could be drawers: II "
       "does not follow"], shortcut="Some + No ⇒ Some-not (first term to third term).", seconds=35)
syl_q("Basic", "Two-statement", N(("coin", "coins"), ("note", "notes"), ("cheque", "cheques")),
      [("all", "coin", "note"), ("all", "note", "cheque")],
      [("all", "coin", "cheque"), ("some", "cheque", "coin")], BOTH,
      "All + All = All; 'All' implies 'Some' in reverse",
      "Coins lie inside notes, and notes inside cheques, so all coins are cheques (I). Since coins exist and all of "
      "them are cheques, some cheques are coins (II).",
      ["All coins ⊂ notes ⊂ cheques ⇒ All coins are cheques: I follows",
       "All coins are cheques ⇒ Some cheques are coins (conversion of 'All' gives 'Some'): II follows"],
      seconds=30)
syl_q("Basic", "Two-statement", N(("tree", "trees"), ("bush", "bushes"), ("shrub", "shrubs")),
      [("no", "tree", "bush"), ("all", "bush", "shrub")],
      [("no", "tree", "shrub"), ("some", "tree", "shrub")], EITHER,
      "Complementary pair: 'Some' and 'No' between the same two terms",
      "Neither conclusion is definite: trees are kept away only from bushes, and the shrubs outside 'bushes' may or "
      "may not include trees. But one of the two must be true, because either some tree is a shrub or none is. So "
      "either I or II follows.",
      ["No tree is a bush; all bushes are shrubs ⇒ only 'Some shrubs are not trees' is certain",
       "I (No tree is a shrub) is not certain; II (Some trees are shrubs) is not certain",
       "I and II are about the same pair (trees, shrubs) and form a 'No' / 'Some' pair: exactly one must be true",
       "So either I or II follows"],
      shortcut="Same subject and predicate, neither definite, one 'No' and one 'Some' ⇒ Either.",
      why="Under the four-option rule 'Either' replaces 'Both', which cannot be right here because I and II "
          "contradict each other.", seconds=40)
syl_q("Basic", "Two-statement", N(("car", "cars"), ("bus", "buses"), ("truck", "trucks")),
      [("some", "car", "bus"), ("some", "bus", "truck")],
      [("some", "car", "truck"), ("all", "truck", "bus")], NEITHER,
      "Some + Some = no conclusion",
      "Two 'some' statements never link the end terms, so I does not follow. 'Some buses are trucks' says nothing "
      "about all trucks, so II does not follow either.",
      ["Some cars are buses, some buses are trucks: the two 'some' parts of buses may not overlap",
       "I: not definite", "II: only some trucks are known to be buses: not definite"],
      shortcut="Some + Some ⇒ no definite conclusion between the end terms.", seconds=30)

# ---- Intermediate (only a few / possibility)
syl_q("Intermediate", "Only a few / Only", N(("lamp", "lamps"), ("bulb", "bulbs"), ("wire", "wires")),
      [("onlyfew", "lamp", "bulb"), ("all", "bulb", "wire")],
      [("some", "lamp", "wire"), ("all", "lamp", "bulb")], ONLY_I,
      "'Only a few A are B' = Some A are B and some A are not B",
      "Some lamps are bulbs and all bulbs are wires, so some lamps are wires (I follows). 'Only a few' also says "
      "some lamps are not bulbs, so 'All lamps are bulbs' is definitely false (II does not follow).",
      ["Only a few lamps are bulbs ⇒ Some lamps are bulbs AND some lamps are not bulbs",
       "Some lamps are bulbs + All bulbs are wires ⇒ Some lamps are wires: I follows",
       "II contradicts 'some lamps are not bulbs': does not follow"], seconds=40)
syl_q("Intermediate", "Only a few / Only", N(("river", "rivers"), ("lake", "lakes"), ("pond", "ponds")),
      [("all", "river", "lake"), ("onlyfew", "lake", "pond")],
      [("all", "river", "pond"), ("somenot", "lake", "pond")], ONLY_II,
      "Definite versus merely possible",
      "Rivers lie inside lakes, but nothing forces them into the pond part of lakes, so I is not definite. 'Only a "
      "few lakes are ponds' directly gives 'Some lakes are not ponds', so II follows.",
      ["Only a few lakes are ponds ⇒ some lakes are ponds and some are not: II follows",
       "Rivers may sit in the pond part, the non-pond part or both: 'All rivers are ponds' is only possible, not "
       "definite: I does not follow"],
      why="'All rivers being ponds is a possibility' would follow, but I states it as a fact.", seconds=40)
syl_q("Intermediate", "Possibility cases", N(("apple", "apples"), ("mango", "mangoes"), ("grape", "grapes"),
                                             ("cherry", "cherries")),
      [("some", "apple", "mango"), ("no", "mango", "grape"), ("onlyfew", "grape", "cherry")],
      [("somenot", "apple", "grape"), ("poss_some", "apple", "cherry")], BOTH,
      "Some + No = Some not; possibility needs only 'not forbidden'",
      "The apples that are mangoes cannot be grapes, so some apples are not grapes (I). No statement separates "
      "apples from cherries, so some apples being cherries is possible (II).",
      ["Some apples are mangoes + No mango is a grape ⇒ Some apples are not grapes: I follows",
       "Apples and cherries are never linked by a 'No' statement, so an overlap is allowed: II follows"],
      shortcut="For a possibility conclusion, look only for a statement that forbids it.", seconds=50)
syl_q("Intermediate", "Possibility cases", N(("desk", "desks"), ("table", "tables"), ("chair", "chairs")),
      [("onlyfew", "desk", "table"), ("no", "table", "chair")],
      [("somenot", "desk", "chair"), ("poss_all", "desk", "chair")], ONLY_I,
      "A possibility fails when it clashes with a definite fact",
      "Some desks are tables and no table is a chair, so those desks are not chairs (I follows). Because some desks "
      "are definitely not chairs, all desks can never be chairs (II does not follow).",
      ["Only a few desks are tables ⇒ some desks are tables", "Those desks are not chairs (No table is a chair) ⇒ "
       "Some desks are not chairs: I follows", "'All desks are chairs' would contradict I, so it is impossible: II "
       "does not follow"], seconds=45)
syl_q("Intermediate", "Only a few / Only", N(("phone", "phones"), ("tablet", "tablets"), ("laptop", "laptops"),
                                             ("screen", "screens")),
      [("some", "phone", "tablet"), ("onlyfew", "tablet", "laptop"), ("all", "laptop", "screen")],
      [("some", "phone", "laptop"), ("some", "screen", "tablet")], ONLY_II,
      "Chaining through 'only a few'",
      "The phones that are tablets may all lie in the non-laptop part of tablets, so I is not certain. Some tablets "
      "are laptops and all laptops are screens, so some tablets are screens, i.e. some screens are tablets (II).",
      ["Only a few tablets are laptops ⇒ some tablets are laptops", "Some tablets are laptops + All laptops are "
       "screens ⇒ Some tablets are screens ⇒ Some screens are tablets: II follows",
       "Some phones are tablets + Some tablets are laptops = Some + Some: I does not follow"], seconds=50)
syl_q("Intermediate", "Only a few / Only", N(("novel", "novels"), ("magazine", "magazines"),
                                             ("journal", "journals")),
      [("no", "novel", "magazine"), ("onlyfew", "magazine", "journal")],
      [("some", "novel", "journal"), ("all", "journal", "magazine")], NEITHER,
      "No definite link through a 'No' statement",
      "Novels are separated only from magazines; journals outside magazines may or may not include novels, so I is "
      "not definite. 'Only a few magazines are journals' does not say every journal is a magazine, so II is not "
      "definite either.",
      ["No + Some (in this order) gives no definite novel–journal relation: I does not follow",
       "Journals may exist outside magazines: II does not follow",
       "I and II are about different pairs, so 'either' cannot apply"], seconds=45)
syl_q("Intermediate", "Possibility cases", N(("doctor", "doctors"), ("nurse", "nurses"), ("surgeon", "surgeons"),
                                             ("intern", "interns")),
      [("all", "doctor", "nurse"), ("some", "nurse", "surgeon"), ("onlyfew", "surgeon", "intern")],
      [("some", "doctor", "intern"), ("no", "doctor", "surgeon")], NEITHER,
      "All + Some: no definite conclusion",
      "Doctors are inside nurses, but the nurses that are surgeons may not include any doctor, and neither may the "
      "interns: I is not definite. Equally, nothing stops a doctor from being a surgeon: II is not definite.",
      ["All doctors are nurses + Some nurses are surgeons = All + Some: no doctor–surgeon conclusion",
       "So no doctor–intern conclusion either: I does not follow", "II (No doctor is a surgeon) is not definite: "
       "does not follow", "I and II involve different pairs, so this is not an 'either' case"], seconds=50)

# ---- Advanced (possibility cases, four terms)
syl_q("Advanced", "Possibility cases", N(("bank", "banks"), ("vault", "vaults"), ("locker", "lockers"),
                                         ("safe", "safes")),
      [("onlyfew", "bank", "vault"), ("only", "vault", "locker"), ("no", "locker", "safe")],
      [("poss_all", "locker", "bank"), ("somenot", "vault", "safe")], BOTH,
      "'Only A are B' means All B are A",
      "'Only vaults are lockers' means all lockers are vaults. Lockers can sit in the bank part of vaults, so all "
      "lockers being banks is possible (I). Lockers exist, every locker is a vault and no locker is a safe, so some "
      "vaults are not safes (II).",
      ["Only vaults are lockers ⇒ All lockers are vaults", "I: lockers are restricted only to 'vaults' and away from "
       "'safes'; the bank part of vaults is allowed ⇒ possible: follows",
       "II: All lockers are vaults ⇒ Some vaults are lockers; No locker is a safe ⇒ Some vaults are not safes: "
       "follows"],
      why="Students who read 'Only vaults are lockers' as 'All vaults are lockers' reach the wrong diagram.",
      seconds=60)
syl_q("Advanced", "Possibility cases", N(("key", "keys"), ("lock", "locks"), ("chain", "chains"), ("ring", "rings")),
      [("all", "key", "lock"), ("onlyfew", "lock", "chain"), ("no", "chain", "ring")],
      [("somenot", "key", "chain"), ("poss_all", "ring", "lock")], ONLY_II,
      "Possibility through the unrestricted part of a set",
      "Keys may lie entirely in the chain part of locks, so 'Some keys are not chains' is not certain (I fails). "
      "Rings are barred only from chains; the non-chain part of locks can hold all rings, so II is possible.",
      ["All keys are locks; only a few locks are chains (some are, some are not)",
       "I: keys could all be chains (inside the chain part of locks): not definite",
       "II: rings must avoid chains only; locks that are not chains exist ⇒ all rings being locks is possible"],
      seconds=60)
syl_q("Advanced", "Only a few / Only", N(("coin", "coins"), ("token", "tokens"), ("chip", "chips"),
                                         ("card", "cards")),
      [("some", "coin", "token"), ("all", "token", "chip"), ("onlyfew", "chip", "card")],
      [("some", "coin", "chip"), ("poss_all", "chip", "card")], ONLY_I,
      "A possibility that contradicts 'only a few' fails",
      "Some coins are tokens and all tokens are chips, so some coins are chips (I). 'Only a few chips are cards' "
      "means some chips are not cards, so all chips can never be cards (II fails).",
      ["Some coins are tokens + All tokens are chips ⇒ Some coins are chips: I follows",
       "Only a few chips are cards ⇒ some chips are NOT cards ⇒ 'All chips are cards' is impossible: II does not "
       "follow"], seconds=50)
syl_q("Advanced", "Possibility cases", N(("metal", "metals"), ("alloy", "alloys"), ("rod", "rods"),
                                         ("wire", "wires")),
      [("onlyfew", "metal", "alloy"), ("all", "alloy", "rod"), ("no", "rod", "wire")],
      [("some", "metal", "wire"), ("poss_all", "wire", "alloy")], NEITHER,
      "Possibility blocked by a chain of 'All' and 'No'",
      "Metals that are not alloys are unrestricted, so a metal–wire overlap is possible but not certain (I fails). "
      "Every alloy is a rod and no rod is a wire, so no wire can ever be an alloy (II fails).",
      ["I: only the alloy part of metals is barred from wires; the rest may or may not be wires: not definite",
       "All alloys are rods + No rod is a wire ⇒ No alloy is a wire", "So 'All wires being alloys' is impossible: II "
       "does not follow"], seconds=60)
syl_q("Advanced", "Only a few / Only", N(("seed", "seeds"), ("plant", "plants"), ("tree", "trees"),
                                         ("flower", "flowers")),
      [("onlyfew", "seed", "plant"), ("all", "plant", "tree"), ("no", "tree", "flower")],
      [("some", "seed", "flower"), ("no", "seed", "flower")], EITHER,
      "Either–or with 'only a few'",
      "The seeds that are plants are trees and so are not flowers, but the seeds that are not plants are free: "
      "they may or may not be flowers. So neither I nor II is certain, yet one of them must hold. Either I or II "
      "follows.",
      ["Only a few seeds are plants ⇒ some seeds are plants (⊂ trees, not flowers) and some seeds are not plants",
       "Seeds outside plants can be flowers (I true) or not (II true)",
       "I and II are a 'Some' / 'No' pair on the same terms: Either I or II follows"],
      why="Under the four-option rule 'Either' replaces 'Both', which is impossible for contradictory conclusions.",
      seconds=55)

# ================================================================================================ INEQUALITY
INQ = "Inequality"
REL = {">": lambda a, b: a > b, "<": lambda a, b: a < b, "≥": lambda a, b: a >= b, "≤": lambda a, b: a <= b,
       "=": lambda a, b: a == b}


def parse_chain(s):
    """'P ≥ Q > R' -> [('P','≥','Q'), ('Q','>','R')]."""
    tok = s.split()
    return [(tok[i], tok[i + 1], tok[i + 2]) for i in range(0, len(tok) - 2, 2)]


def ineq_eval(chains, conclusions, dom=5):
    rels = [r for c in chains for r in parse_chain(c)]
    vs = sorted({x for a, _, b in rels for x in (a, b)} | {x for c in conclusions for x in (c[0], c[2])})
    res = []
    sats = []
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


# ---- Basic: direct
s, ch, cc, ct = direct(["M > N ≥ O = P < Q ≤ R"], ["M > P", "R > O"])
ineq_q("Basic", "Direct inequality", s, ch, cc, ct, BOTH,
       "M > N ≥ O = P gives M > P. O = P < Q ≤ R gives R > O. Both follow.",
       ["I: M > N ≥ O = P → the path has a strict '>' and no reversed sign: M > P, true",
        "II: O = P < Q ≤ R → R > O, true"], shortcut="Any path with one strict sign and no opposite sign gives a "
                                                     "strict result.", seconds=30)
s, ch, cc, ct = direct(["A ≤ B < C = D ≥ E > F"], ["C > A", "E < B"])
ineq_q("Basic", "Direct inequality", s, ch, cc, ct, ONLY_I,
       "A ≤ B < C gives C > A. Between B and E the signs change direction (B < C = D ≥ E), so no relation can be "
       "drawn between E and B.",
       ["I: A ≤ B < C → C > A, true", "II: B < C = D ≥ E: '<' and '≥' point in opposite directions → no relation, "
                                      "not definite"], seconds=30)
s, ch, cc, ct = direct(["G ≥ H = J > K ≤ L < M"], ["G > L", "M > K"])
ineq_q("Basic", "Direct inequality", s, ch, cc, ct, ONLY_II,
       "From G down to L the signs flip at K (J > K ≤ L), so G and L cannot be compared. K ≤ L < M gives M > K.",
       ["I: G ≥ H = J > K ≤ L: opposite signs around K → no relation", "II: K ≤ L < M → M > K, true"], seconds=30)
s, ch, cc, ct = direct(["S < T ≤ U = V > W ≥ X"], ["S < W", "X < T"])
ineq_q("Basic", "Direct inequality", s, ch, cc, ct, NEITHER,
       "Both comparisons pass through V, where the direction reverses (U = V > W), so neither S and W nor X and T "
       "can be compared.",
       ["I: S < T ≤ U = V > W: direction reverses at V → no relation", "II: X ≤ W < V = U ≥ T: reverses at U → no "
                                                                         "relation"], seconds=30)
s, ch, cc, ct = direct(["B ≥ C = D ≤ E < F"], ["E > C", "E = C"])
ineq_q("Basic", "Direct inequality", s, ch, cc, ct, EITHER,
       "C = D ≤ E gives E ≥ C: E is either greater than or equal to C, and neither alone is certain. Since I and II "
       "together cover '≥' exactly, either I or II follows.",
       ["C = D ≤ E → E ≥ C", "I (E > C) alone is not certain; II (E = C) alone is not certain",
        "Together they form E ≥ C, which is certain: Either I or II follows"],
       shortcut="When the derived sign is ≥ (or ≤) and the conclusions are the matching > and =, the answer is "
                "Either.", why="'Either' replaces 'Both' here (four-option rule), since E > C and E = C cannot both "
                               "be true.", seconds=35)

# ---- Intermediate: coded and combined
CODE1 = {"#": ">", "$": "≥", "&": "=", "%": "<", "@": "≤"}
CODE1_TXT = ("In the following question, the symbols #, $, &, % and @ are used with these meanings:\n"
             "'P # Q' means 'P is greater than Q'; 'P $ Q' means 'P is not smaller than Q'; 'P & Q' means 'P is "
             "equal to Q'; 'P % Q' means 'P is smaller than Q'; 'P @ Q' means 'P is not greater than Q'.\n"
             "Assuming the statements to be true, find which of the conclusions I and II is/are definitely true.")
decode = lambda s, code: " ".join(code.get(t, t) for t in s.split())


def coded(intro, code, stmts, concs):
    text = intro + "\n\nStatements: " + ", ".join(stmts)
    return text, [decode(x, code) for x in stmts], [parse_chain(decode(c, code))[0] for c in concs], concs


s, ch, cc, ct = coded(CODE1_TXT, CODE1, ["A # B", "B $ C", "C & D", "D @ E"], ["A # D", "E $ B"])
ineq_q("Intermediate", "Coded inequality", s, ch, cc, ct, ONLY_I,
       "Decoded: A > B ≥ C = D ≤ E. So A > D (I follows). Between E and B the direction reverses at D, so E ≥ B is "
       "not certain (II does not follow).",
       ["Decode: # → >, $ → ≥, & → =, @ → ≤", "Combined: A > B ≥ C = D ≤ E",
        "I: A # D means A > D: A > B ≥ C = D → true", "II: E $ B means E ≥ B: E ≥ D = C ≤ B → no relation"],
       concept="Decoding symbols, then reading the chain", seconds=50)
s, ch, cc, ct = direct(["P > Q ≥ R", "S < R ≤ T", "U = S"], ["P > U", "T > S"])
ineq_q("Intermediate", "Direct inequality", s, ch, cc, ct, BOTH,
       "Joining the statements: P > Q ≥ R > S = U and T ≥ R > S. So P > U and T > S: both follow.",
       ["Combine: P > Q ≥ R > S = U (S < R written as R > S)", "I: P > Q ≥ R > S = U → P > U, true",
        "II: T ≥ R > S → T > S, true"], concept="Combining several statements into one chain", seconds=45)
CODE2 = {"©": "<", "★": "=", "δ": "≤", "%": ">", "@": "≥"}
CODE2_TXT = ("In the following question, the symbols ©, ★, δ, % and @ are used with these meanings:\n"
             "'A © B' means 'A is smaller than B'; 'A ★ B' means 'A is equal to B'; 'A δ B' means 'A is either "
             "smaller than or equal to B'; 'A % B' means 'A is greater than B'; 'A @ B' means 'A is either greater "
             "than or equal to B'.\nAssuming the statements to be true, find which of the conclusions I and II "
             "is/are definitely true.")
s, ch, cc, ct = coded(CODE2_TXT, CODE2, ["J © K", "K ★ L", "L δ M", "N % L"], ["M % N", "N % J"])
ineq_q("Intermediate", "Coded inequality", s, ch, cc, ct, ONLY_II,
       "Decoded: J < K = L ≤ M and N > L. M and N are both above L but cannot be compared with each other (I fails). "
       "N > L = K > J gives N > J (II follows).",
       ["Decode: © → <, ★ → =, δ → ≤, % → >", "J < K = L ≤ M; N > L", "I: M > N? Both M and N are only known to be "
        "above L: no relation", "II: N > L = K > J → N > J, true"],
       concept="Decoding symbols, then reading the chain", seconds=55)
s, ch, cc, ct = coded(CODE1_TXT, CODE1, ["F $ G", "G & H", "H # I"], ["F # H", "F & H"])
ineq_q("Intermediate", "Coded inequality", s, ch, cc, ct, EITHER,
       "Decoded: F ≥ G = H > I, so F ≥ H. F > H and F = H are each uncertain, but one of them must be true: either I "
       "or II follows.",
       ["Decode: F ≥ G, G = H, H > I → F ≥ G = H > I", "F ≥ H: F > H (I) or F = H (II)",
        "Neither is certain alone; together they cover F ≥ H: Either"],
       why="'Either' replaces 'Both' (four-option rule): F > H and F = H cannot both hold.",
       concept="Decoding symbols; the either-or case", seconds=50)
s, ch, cc, ct = direct(["W ≤ X < Y", "Z > Y", "V ≥ X", "U = V"], ["U > W", "Z > V"])
ineq_q("Intermediate", "Direct inequality", s, ch, cc, ct, NEITHER,
       "U = V ≥ X ≥ W gives only U ≥ W, so U > W is not certain. Z > Y > X and V ≥ X do not compare Z with V.",
       ["Chains: W ≤ X < Y < Z, and U = V ≥ X", "I: U = V ≥ X ≥ W → U ≥ W only (equality possible): not definite",
        "II: Z and V are both above X, through different branches: no relation"],
       concept="Combining several statements into one chain", seconds=50)
CODE5 = {"Ω": "≤", "¥": "<", "€": "=", "∆": ">", "◘": "≥"}
CODE5_TXT = ("In the following question, 'A ¥ B' means 'A is less than B', 'A ∆ B' means 'A is more than B', 'A ◘ B' "
             "means 'A is at least B', 'A Ω B' means 'A is at most B', and 'A € B' means 'A and B are equal'.\n"
             "Assuming the statements to be true, find which of the conclusions I and II is/are definitely true.")
s, ch, cc, ct = coded(CODE5_TXT, CODE5, ["R Ω S", "S ¥ T", "T € U", "V ∆ U"], ["S ∆ V", "R ¥ U"])
ineq_q("Intermediate", "Coded inequality", s, ch, cc, ct, ONLY_II,
       "Decoded: R ≤ S < T = U < V. So S < V, which makes 'S > V' false (I fails), and R < U (II follows).",
       ["Decode: R Ω S → R ≤ S, S ¥ T → S < T, T € U → T = U, V ∆ U → V > U", "Chain: R ≤ S < T = U < V",
        "I: S ∆ V means S > V, but S < T = U < V: false",
        "II: R ≤ S < T = U → R < U, true"], concept="Decoding symbols, then reading the chain", seconds=55)

# ---- Advanced
CODE3 = {"◊": "<", "■": ">", "▲": "≤", "●": "≥", "✱": "="}
CODE3_TXT = ("In the following question, the symbols ◊, ■, ▲, ● and ✱ are used with these meanings:\n"
             "'A ◊ B' means 'A is neither greater than nor equal to B'; 'A ■ B' means 'A is neither smaller than nor "
             "equal to B'; 'A ▲ B' means 'A is not greater than B'; 'A ● B' means 'A is not smaller than B'; "
             "'A ✱ B' means 'A is neither greater than nor smaller than B'.\nAssuming the statements to be true, find "
             "which of the conclusions I and II is/are definitely true.")
s, ch, cc, ct = coded(CODE3_TXT, CODE3, ["M ● N", "N ✱ O", "O ■ P", "Q ▲ P", "Q ◊ R"], ["M ■ Q", "R ■ P"])
ineq_q("Advanced", "Coded inequality", s, ch, cc, ct, ONLY_I,
       "Decoded: M ≥ N = O > P ≥ Q < R. M > Q follows. R and P are both compared only with Q (R > Q, P ≥ Q), so they "
       "cannot be compared.",
       ["Decode: ◊ → <, ■ → >, ▲ → ≤, ● → ≥, ✱ → =", "M ≥ N = O > P, Q ≤ P, Q < R → M ≥ N = O > P ≥ Q < R",
        "I: M > Q: M ≥ N = O > P ≥ Q → true", "II: R > P: R > Q ≤ P → no relation"],
       concept="Negative-worded codes ('neither greater nor equal' = smaller)", seconds=70)
S_OPTS = {"≥, >, =, ≥": ["≥", ">", "=", "≥"], "≥, ≥, <, >": ["≥", "≥", "<", ">"], ">, ≥, ≤, >": [">", "≥", "≤", ">"],
          "=, >, <, =": ["=", ">", "<", "="]}
good = []
for label_, signs in S_OPTS.items():
    chain = "P {} Q {} R {} S {} T".format(*signs)
    f1, f2, _ = ineq_eval([chain], [("P", ">", "T"), ("S", "≥", "R")])
    if f1 and f2:
        good.append(label_)
assert good == ["≥, >, =, ≥"]
mcq(INQ, "Direct inequality", "Advanced",
    "Which of the following sets of symbols, filled in order in the blanks of the expression below, makes both "
    "'P > T' and 'S ≥ R' definitely true?\n\nP __ Q __ R __ S __ T", good[0],
    [k for k in S_OPTS if k != good[0]], "Building an expression that forces given conclusions",
    "With ≥, >, =, ≥ the expression is P ≥ Q > R = S ≥ T. The path from P to T contains a strict '>' and no reversed "
    "sign, so P > T; and R = S gives S ≥ R. Every other option fails at least one conclusion.",
    ["Option '≥, >, =, ≥': P ≥ Q > R = S ≥ T → P > T and S = R (so S ≥ R): both true",
     "Option '≥, ≥, <, >': P ≥ Q ≥ R < S > T → direction reverses at R and S: P > T fails",
     "Option '>, ≥, ≤, >': P > Q ≥ R ≤ S > T → reverses at R: P > T fails",
     "Option '=, >, <, =': P = Q > R < S = T → reverses at R: P > T fails"],
    shortcut="For P > T the four signs must all point the same way with at least one strict sign; only the first "
             "option has no reversal.", seconds=60, verified_by=EXHAUST)
s, ch, cc, ct = direct(["D > E ≥ F", "G ≤ F", "H = G", "I ≥ D"], ["I > H", "E ≥ H"])
ineq_q("Advanced", "Direct inequality", s, ch, cc, ct, BOTH,
       "Combined: I ≥ D > E ≥ F ≥ G = H. So I > H (the path contains D > E) and E ≥ H.",
       ["Combine: I ≥ D > E ≥ F ≥ G = H", "I: I ≥ D > E ≥ F ≥ G = H → I > H (one strict sign), true",
        "II: E ≥ F ≥ G = H → E ≥ H, true"], concept="Combining four statements into one chain", seconds=55)
CODE4 = {"⊕": "≤", "⊗": ">", "⊘": "=", "⊙": "≥", "⊖": "<"}
CODE4_TXT = ("In the following question, 'A ⊕ B' means 'A is not greater than B', 'A ⊗ B' means 'A is greater than "
             "B', 'A ⊘ B' means 'A is equal to B', 'A ⊙ B' means 'A is not smaller than B', and 'A ⊖ B' means 'A is "
             "smaller than B'.\nAssuming the statements to be true, find which of the conclusions I and II is/are "
             "definitely true.")
s, ch, cc, ct = coded(CODE4_TXT, CODE4, ["T ⊕ U", "U ⊗ V", "V ⊘ W", "X ⊙ U", "Y ⊖ W"], ["T ⊖ X", "Y ⊖ T"])
ineq_q("Advanced", "Coded inequality", s, ch, cc, ct, NEITHER,
       "Decoded: T ≤ U ≤ X, U > V = W > Y. T ≤ U ≤ X gives only T ≤ X, so T < X is not certain. Y and T are both "
       "below U but along different branches, so they cannot be compared.",
       ["Decode: T ≤ U, U > V, V = W, X ≥ U, Y < W", "T ≤ U ≤ X and U > V = W > Y",
        "I: T < X? Only T ≤ X is certain (T = U = X possible): not definite",
        "II: Y < T? T ≤ U and Y < W < U: both below U, no relation"],
       concept="Coded inequality with several branches", seconds=70)
s, ch, cc, ct = direct(["B ≥ C", "C > D", "E ≤ D", "F = E", "B ≤ G"], ["G > F", "D ≥ F"])
ineq_q("Advanced", "Direct inequality", s, ch, cc, ct, BOTH,
       "Combined: G ≥ B ≥ C > D ≥ E = F. The path from G to F contains the strict sign C > D, so G > F. D ≥ E = F "
       "gives D ≥ F. Both follow.",
       ["Rewrite each statement in one direction: G ≥ B, B ≥ C, C > D, D ≥ E, E = F",
        "Combined: G ≥ B ≥ C > D ≥ E = F", "I: G > F (one strict sign, no reversal): true",
        "II: D ≥ E = F → D ≥ F: true"],
       why="Students who stop at G ≥ B ≥ C often miss that C > D makes the G–F relation strict.",
       concept="Combining five statements into one chain", seconds=55)

# ================================================================================================ BLOOD RELATIONS
BLD = "Blood Relations"


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

# ---- Basic
F = Family().add("Kamini", "F").add("Neha", "F", mother="Kamini").add("Vikas", "M").marry("Neha", "Vikas")
F.add("Rohit", "M", father="Vikas", mother="Neha")
F.check([("Neha", "daughter", "Kamini"), ("Neha", "mother", "Rohit")])
assert [c for c in F.children("Kamini") if F.g[c] == "F"] == ["Neha"]
ans = F.rel("Neha", "Rohit")
mcq(BLD, "Direct relation", "Basic",
    "Pointing to a man, Neha said, \"His mother is the only daughter of my mother.\" How is Neha related to the man?",
    cap(ans), ["Sister", "Aunt", "Grandmother"], "Decoding a pointing statement from the speaker outward",
    "'The only daughter of my mother' is Neha herself (a woman speaking about her own mother's only daughter). So "
    "the man's mother is Neha.",
    ["Speaker: Neha (female)", "Only daughter of Neha's mother = Neha", "The man's mother = Neha",
     "So Neha is the man's mother"], shortcut="When a woman says 'only daughter of my mother', it is herself.",
    why_others_wrong="Sister or aunt would need the 'only daughter' to be someone other than Neha.", seconds=30,
    verified_by=RECOMP)
F = Family().add("D", "M").add("Dw", "F").marry("D", "Dw").add("C", "F", "D", "Dw").add("Cx", "M").marry("C", "Cx")
F.add("A", "M", "Cx", "C").add("B", "F", "Cx", "C")
F.check([("A", "brother", "B"), ("B", "daughter", "C"), ("D", "father", "C")])
ans = F.rel("A", "D")
mcq(BLD, "Direct relation", "Basic",
    "A is the brother of B. B is the daughter of C. D is the father of C. How is A related to D?", cap(ans),
    ["Son", "Nephew", "Son-in-law"], "Generation counting",
    "A and B are siblings, so A is also C's child. D is C's father, so A, a male one generation below C, is D's "
    "grandson.", ["A brother of B, B child of C ⇒ A is C's son", "D is C's father ⇒ D is two generations above A",
                  "A is male ⇒ grandson"], seconds=30, verified_by=RECOMP)
F = Family().add("Suresh", "M", "Gp", "Gm").add("Kamla", "F", "Gp", "Gm").add("Gp", "M").add("Gm", "F")
F.add("Mohan", "M").marry("Kamla", "Mohan").add("Usha", "F").marry("Suresh", "Usha")
F.add("Ravi", "M", "Suresh", "Usha")
F.check([("Suresh", "father", "Ravi"), ("Kamla", "sister", "Suresh"), ("Mohan", "husband", "Kamla")])
ans = F.rel("Mohan", "Ravi")
mcq(BLD, "Direct relation", "Basic",
    "Ravi's father is Suresh. Suresh's sister is Kamla, and Kamla's husband is Mohan. How is Mohan related to Ravi?",
    cap(ans), ["Father-in-law", "Brother-in-law", "Cousin"], "Paternal aunt's husband",
    "Kamla is Ravi's father's sister, i.e. his aunt; her husband Mohan is Ravi's uncle.",
    ["Suresh → father of Ravi", "Kamla → sister of Suresh → Ravi's aunt", "Mohan → husband of Kamla → Ravi's uncle"],
    seconds=30, verified_by=RECOMP)

# ---- Intermediate
CODE_B1 = {"+": "father", "−": "sister", "×": "wife", "÷": "son"}
F = Family().add("O", "M").add("N", "F").marry("O", "N").add("M", "M", "O", "N").add("P", "F", "O", "N")
F.add("Q", "M", "O", "N")
expr = "M ÷ N × O + P − Q"
F.check(coded_facts(expr, CODE_B1))
ans = F.rel("M", "Q")
mcq(BLD, "Coded blood relation", "Intermediate",
    "In a certain code:\n'P + Q' means 'P is the father of Q';\n'P − Q' means 'P is the sister of Q';\n'P × Q' means "
    "'P is the wife of Q';\n'P ÷ Q' means 'P is the son of Q'.\n\nIf 'M ÷ N × O + P − Q', how is M related to Q?",
    cap(ans), ["Son", "Father", "Nephew"], "Decoding a coded relation chain left to right",
    "M is the son of N, and N is the wife of O, so M is O's son. O is the father of P, and P is the sister of Q, so Q "
    "is also O's child. M and Q are children of the same parents, and M is male: M is Q's brother.",
    ["M ÷ N: M is the son of N", "N × O: N is the wife of O ⇒ M is the son of O and N",
     "O + P: O is the father of P; P − Q: P is the sister of Q ⇒ Q is also O's child",
     "M (male) and Q share parents ⇒ M is Q's brother"], seconds=50, verified_by=RECOMP)
F = Family().add("Gf", "M").add("Gm", "F").marry("Gf", "Gm").add("Fa", "M", "Gf", "Gm").add("Mo", "F")
F.marry("Fa", "Mo").add("Arun", "M", "Fa", "Mo").add("Aunt", "F", "Gf", "Gm").add("Cousin", "F", None, "Aunt")
F.add("Woman", "F").marry("Arun", "Woman")
grandsons = [x for c in F.children("Gf") for x in F.children(c) if F.g[x] == "M"]
assert grandsons == ["Arun"]
ans = F.rel("Woman", "Arun")
mcq(BLD, "Direct relation", "Intermediate",
    "Introducing a woman, Arun said, \"She is the wife of the only grandson of my father's father.\" How is the woman "
    "related to Arun?", cap(ans), ["Sister-in-law", "Cousin", "Daughter-in-law"],
    "Self-reference hidden in 'only grandson'",
    "Arun is a grandson of his own father's father. If that man has only one grandson, it must be Arun himself. So "
    "the woman is the wife of Arun.",
    ["My father's father = Arun's paternal grandfather", "His only grandson = Arun (Arun is male and is his grandson)",
     "Wife of that grandson = Arun's wife"],
    why_others_wrong="Sister-in-law would need the grandson to be Arun's brother, but the grandson is unique and Arun "
                     "is himself a grandson.", seconds=40, verified_by=RECOMP)
F = Family().add("Q", "M").add("S", "F").marry("Q", "S").add("P", "M", "Q", "S").add("U", "F", "Q", "S")
F.add("T", "F").marry("P", "T").add("R", "M", "P", "T")
facts = [("Q", "father-in-law", "T"), ("S", "grandmother", "R"), ("U", "sister", "P"), ("R", "son", "T"),
         ("Q", "husband", "S")]
F.check(facts)
ans = F.rel("U", "R")
mcq(BLD, "Family puzzle", "Intermediate",
    "There are six members P, Q, R, S, T and U in a family of three generations, with two married couples.\n"
    "- Q is the father-in-law of T.\n- S is the grandmother of R.\n- U is the sister of P.\n- R is the son of T.\n"
    "- Q is married to S, and P is the only son of Q.\n\nHow is U related to R?", cap(ans),
    ["Mother", "Sister", "Cousin"], "Building a three-generation family tree",
    "Q and S are the grandparents. P is their only son and is married to T (T is Q's daughter-in-law). R is the son of "
    "P and T. U is P's sister, so U is R's father's sister: his aunt.",
    ["Q is T's father-in-law and P is Q's only son ⇒ T is P's wife", "R is T's son ⇒ R is P's son; S (Q's wife) is "
     "R's grandmother", "U is P's sister ⇒ U is R's paternal aunt"], seconds=60, verified_by=RECOMP)
CODE_B2 = {"@": "mother", "#": "brother", "$": "husband", "&": "daughter"}
F = Family().add("M", "M").add("N", "F").marry("M", "N").add("K", "M", "M", "N").add("L", "F", "M", "N")
F.add("O", "F", "M", "N")
expr = "K # L & M $ N @ O"
F.check(coded_facts(expr, CODE_B2))
ans = F.rel("N", "K")
mcq(BLD, "Coded blood relation", "Intermediate",
    "In a certain code:\n'A @ B' means 'A is the mother of B';\n'A # B' means 'A is the brother of B';\n'A $ B' means "
    "'A is the husband of B';\n'A & B' means 'A is the daughter of B'.\n\nIn the expression 'K # L & M $ N @ O', how "
    "is N related to K?", cap(ans), ["Sister", "Aunt", "Grandmother"], "Coded relation chain",
    "K is L's brother and L is M's daughter, so K is M's son. M is N's husband, so N is K's mother.",
    ["K # L: K is the brother of L", "L & M: L is the daughter of M ⇒ K is M's son", "M $ N: M is the husband of N ⇒ "
     "N is the mother of K and L", "N @ O: N is O's mother (not needed for the question)"], seconds=45,
    verified_by=RECOMP)

# ---- Advanced
F = Family().add("Harsh", "M").add("Gita", "F").marry("Harsh", "Gita").add("Kunal", "M", "Harsh", "Gita")
F.add("Lata", "F", "Harsh", "Gita").add("Meena", "F").marry("Kunal", "Meena").add("Naresh", "M")
F.marry("Lata", "Naresh").add("Om", "M", "Kunal", "Meena").add("Pari", "F", "Naresh", "Lata")
facts = [("Om", "grandson", "Gita"), ("Meena", "daughter-in-law", "Harsh"), ("Pari", "niece", "Kunal"),
         ("Naresh", "son-in-law", "Gita"), ("Lata", "sister", "Kunal"), ("Harsh", "husband", "Gita"),
         ("Om", "son", "Meena")]
F.check(facts)
ans = F.rel("Om", "Lata")
mcq(BLD, "Family puzzle", "Advanced",
    "A family of three generations has eight members: Harsh, Gita, Kunal, Lata, Meena, Naresh, Om and Pari. There are "
    "three married couples, and each couple of the second generation has exactly one child.\n"
    "- Om is the grandson of Gita.\n- Meena is the daughter-in-law of Harsh.\n- Pari is the niece of Kunal.\n"
    "- Naresh is the son-in-law of Gita.\n- Lata is the sister of Kunal.\n- Harsh is the husband of Gita, and they "
    "have only two children.\n- Om is the son of Meena.\n\nHow is Om related to Lata?", cap(ans),
    ["Son", "Cousin", "Grandson"], "Eight-member family tree",
    "Harsh and Gita have two children, Kunal and Lata. Meena is Harsh's daughter-in-law, so she is Kunal's wife; Om "
    "is their son. Naresh is Gita's son-in-law, so he is Lata's husband, and Pari (Kunal's niece) is their daughter. "
    "Om is the son of Lata's brother: her nephew.",
    ["Generation 1: Harsh + Gita; children: Kunal, Lata", "Meena = Kunal's wife (daughter-in-law of Harsh); their son "
     "= Om", "Naresh = Lata's husband (son-in-law of Gita); their daughter = Pari (Kunal's niece)",
     "Om is the son of Lata's brother ⇒ nephew"],
    why_others_wrong="Cousin is Om's relation to Pari, not to Lata; grandson is his relation to Harsh and Gita.",
    seconds=90, verified_by=RECOMP)
CODE_B3 = {"★": "father", "●": "sister", "▲": "wife", "◆": "son", "■": "mother"}
F = Family().add("Kp", "M").add("K", "F").marry("Kp", "K").add("J", "F", "Kp", "K").add("G", "M").marry("G", "J")
F.add("H", "F", "G", "J").add("I", "M", "G", "J")
exprs = ["G ★ H ● I", "J ▲ G", "K ■ J", "I ◆ J"]
for e in exprs:
    F.check(coded_facts(e, CODE_B3))
ans = F.rel("I", "K")
mcq(BLD, "Coded blood relation", "Advanced",
    "In a certain code:\n'A ★ B' means 'A is the father of B';\n'A ● B' means 'A is the sister of B';\n'A ▲ B' means "
    "'A is the wife of B';\n'A ◆ B' means 'A is the son of B';\n'A ■ B' means 'A is the mother of B'.\n\nGiven that "
    "'G ★ H ● I', 'J ▲ G', 'K ■ J' and 'I ◆ J' are all true, how is I related to K?", cap(ans),
    ["Son", "Nephew", "Son-in-law"], "Combining several coded expressions",
    "G is the father of H and I (H is I's sister). J is G's wife and I is J's son, so J is I's mother. K is J's "
    "mother, so K is I's maternal grandmother and I, a male, is K's grandson.",
    ["G ★ H ● I: G is the father of H; H is the sister of I ⇒ G is I's father",
     "J ▲ G and I ◆ J: J is G's wife and I's mother; I is male", "K ■ J: K is J's mother",
     "So K is I's grandmother and I is K's grandson"], seconds=75, verified_by=RECOMP)
F = Family().add("Bhanu", "M").add("Chhaya", "F").marry("Bhanu", "Chhaya").add("Dev", "M", "Bhanu", "Chhaya")
F.add("Esha", "F", "Bhanu", "Chhaya").add("Farah", "F").marry("Dev", "Farah").add("Gagan", "M", "Dev", "Farah")
F.add("Hina", "F", "Dev", "Farah")
facts = [("Hina", "granddaughter", "Bhanu"), ("Farah", "mother", "Gagan"), ("Dev", "son", "Bhanu"),
         ("Gagan", "brother", "Hina"), ("Chhaya", "wife", "Bhanu"), ("Esha", "daughter", "Chhaya")]
F.check(facts)
assert [c for c in F.children("Chhaya") if F.g[c] == "F"] == ["Esha"]
mother_g = next(p for p in F.parents("Gagan") if F.g[p] == "F")
ans = F.rel("Esha", mother_g)
mcq(BLD, "Family puzzle", "Advanced",
    "In a family of seven members of three generations — Bhanu, Chhaya, Dev, Esha, Farah, Gagan and Hina — there are "
    "two married couples.\n- Hina is the granddaughter of Bhanu.\n- Farah is the mother of Gagan.\n- Esha is the "
    "only daughter of Chhaya.\n- Dev is the son of Bhanu, and Bhanu has only one son.\n- Gagan is the brother of "
    "Hina.\n- Chhaya is the wife of Bhanu.\n- Esha is unmarried.\n\nHow is Esha related to the mother of Gagan?",
    cap(ans), ["Daughter-in-law", "Aunt", "Sister"], "Relations through marriage",
    "Bhanu and Chhaya have two children, Dev and Esha. The grandchildren Gagan and Hina must be Dev's children (Esha is "
    "unmarried), so Farah is Dev's wife. Esha is the sister of Farah's husband: her sister-in-law.",
    ["Generation 1: Bhanu + Chhaya; children Dev (only son) and Esha (only daughter)",
     "Gagan and Hina are grandchildren of Bhanu; Esha is unmarried ⇒ they are Dev's children ⇒ Farah is Dev's wife",
     "Esha = sister of Farah's husband ⇒ sister-in-law"],
    why_others_wrong="Aunt is Esha's relation to Gagan and Hina, not to their mother.", seconds=80,
    verified_by=RECOMP)

# ================================================================================================ DIRECTION SENSE
DIR = "Direction Sense"
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


# ---- Basic
x, y = walk("N", [(None, 10), ("R", 6), ("R", 4)])
assert (x, y) == (6, 6)
mcq(DIR, "Distance and direction", "Basic",
    "Ravi walks 10 m towards the north. He then turns right and walks 6 m, and then turns right again and walks 4 m. "
    "How far is he now from his starting point, and in which direction?", f"{dist(x, y)} m, {compass(x, y)}",
    ["6√2 m, North-West", "8 m, North-East", "10 m, East"], "Net displacement with Pythagoras",
    "Net movement: 6 m east and 10 − 4 = 6 m north. Distance = √(6² + 6²) = 6√2 m (about 8.49 m), towards the "
    "north-east of the start.",
    ["Start (0, 0); 10 m north → (0, 10)", "Turn right (now facing east), 6 m → (6, 10)",
     "Turn right (now facing south), 4 m → (6, 6)", "Distance = √(36 + 36) = 6√2 m; x > 0 and y > 0 → North-East"],
    seconds=40, verified_by=RECOMP)
pts = {"B": (0, 0), "A": (-5, 0), "C": (0, 8)}
pts["D"] = (pts["C"][0] + 5, pts["C"][1])
dx, dy = pts["A"][0] - pts["D"][0], pts["A"][1] - pts["D"][1]
mcq(DIR, "Point-to-point", "Basic",
    "Point A is 5 m west of point B. Point C is 8 m north of point B. Point D is 5 m east of point C. In which "
    "direction is point A with respect to point D?", compass(dx, dy), ["North-West", "South-East", "West"],
    "Placing points on a grid",
    "Taking B as (0, 0): A = (−5, 0), C = (0, 8), D = (5, 8). From D to A the move is 10 m west and 8 m south, so A "
    "is to the south-west of D.",
    ["B = (0, 0), A = (−5, 0)", "C = (0, 8), D = (5, 8)", "A − D = (−10, −8): west and south ⇒ South-West"],
    seconds=40, verified_by=RECOMP)
# morning: sun in the east, so shadows fall to the west
face = [f for f in CW if turn(f, "R") == "W"]
assert face == ["S"]
mcq(DIR, "Shadow-based", "Basic",
    "One morning after sunrise, Neeraj was standing facing a pole. The shadow of the pole fell exactly to his right. "
    "Which direction was Neeraj facing?", NAME[face[0]], ["North", "East", "West"], "Shadows in the morning",
    "In the morning the sun is in the east, so shadows fall towards the west. The shadow is on Neeraj's right, so his "
    "right hand points west, which means he is facing south.",
    ["Morning sun → east; shadow → west", "Shadow on his right ⇒ his right = west",
     "Facing south, the right hand points west ⇒ he faces South"],
    shortcut="Morning: shadow west. Whatever side the shadow is on tells you where that hand points.", seconds=35,
    verified_by=RECOMP)

# ---- Intermediate
x, y = walk("E", [(None, 7), ("L", 9), ("R", 5), ("R", 4)])
assert (x, y) == (12, 5)
mcq(DIR, "Distance and direction", "Intermediate",
    "Starting from her house, Kiran drives 7 km towards the east. She then turns left and drives 9 km, turns right and "
    "drives 5 km, and finally turns right and drives 4 km. What is the shortest distance between her house and her "
    "present position?", f"{dist(x, y)} km", ["12 km", "17 km", "15 km"], "Net displacement with a 5-12-13 triple",
    "East: 7 + 5 = 12 km. North: 9 − 4 = 5 km. Shortest distance = √(12² + 5²) = 13 km.",
    ["7 km east → (7, 0)", "Left (north) 9 km → (7, 9)", "Right (east) 5 km → (12, 9)",
     "Right (south) 4 km → (12, 5)", "√(144 + 25) = √169 = 13 km"], natural=lambda t: float(t.split()[0]),
    seconds=50, verified_by=RECOMP)
pts = {"Q": (0, 0), "P": (0, -4)}
pts["R"] = (pts["P"][0] + 3, pts["P"][1])
pts["S"] = (pts["R"][0], pts["R"][1] + 7)
pts["T"] = (pts["S"][0] - 6, pts["S"][1])
dx, dy = pts["T"]
assert (dx, dy) == (-3, 3)
mcq(DIR, "Point-to-point", "Intermediate",
    "Point P is 4 m south of point Q. Point R is 3 m east of point P. Point S is 7 m north of point R. Point T is 6 m "
    "west of point S. How far is point T from point Q, and in which direction?", f"{dist(dx, dy)} m, {compass(dx, dy)}",
    ["3√2 m, North-East", "3 m, West", "5 m, North-West"], "Coordinates of a chain of points",
    "With Q at (0, 0): P = (0, −4), R = (3, −4), S = (3, 3), T = (−3, 3). T is 3 m west and 3 m north of Q: "
    "3√2 m to the north-west.",
    ["Q (0, 0) → P (0, −4) → R (3, −4) → S (3, 3) → T (−3, 3)", "T − Q = (−3, 3)", "Distance = √18 = 3√2 m; "
     "direction North-West"], seconds=55, verified_by=RECOMP)
# evening: sun in the west, shadows fall to the east. Asha's shadow falls to Bela's left.
bela = [f for f in CW if turn(f, "L") == "E"]
asha = [CW[(CW.index(f) + 2) % 4] for f in bela]
assert asha == ["N"]
mcq(DIR, "Shadow-based", "Intermediate",
    "One evening before sunset, Asha and Bela were standing facing each other. Asha's shadow fell exactly to Bela's "
    "left. Which direction was Asha facing?", NAME[asha[0]], ["South", "East", "West"],
    "Shadows in the evening, two observers",
    "In the evening the sun is in the west, so shadows fall to the east. Asha's shadow is on Bela's left, so Bela's "
    "left points east and Bela faces south. Asha faces Bela, so Asha faces north.",
    ["Evening sun → west; shadows → east", "Bela's left = east ⇒ Bela faces south",
     "Asha faces Bela ⇒ Asha faces north"],
    why_others_wrong="South is Bela's direction, not Asha's.", seconds=45, verified_by=RECOMP)
ang = (315 + 90 - 180 + 135) % 360
assert ang == 0
mcq(DIR, "Distance and direction", "Intermediate",
    "A man is facing north-west. He turns 90° clockwise, then 180° anticlockwise, and then 135° clockwise. Which "
    "direction is he facing now?", "North", ["South", "North-East", "West"], "Net rotation",
    "Measure directions clockwise from north: north-west = 315°. 315 + 90 − 180 + 135 = 360°, i.e. north.",
    ["North-west = 315°", "+90° → 45° (north-east)", "−180° → 225° (south-west)", "+135° → 360° = 0° (north)"],
    shortcut="Net turn = 90 − 180 + 135 = 45° clockwise; north-west turned 45° clockwise is north.", seconds=40,
    verified_by=RECOMP)

# ---- Advanced
step = {"#": (0, 3), "$": (4, 0), "@": (0, -3), "%": (-4, 0)}
pts = {"Q": (0, 0)}
for a, s_, b in [("P", "#", "Q"), ("R", "$", "Q"), ("S", "@", "R"), ("T", "%", "S")]:
    pts[a] = (pts[b][0] + step[s_][0], pts[b][1] + step[s_][1])
dx, dy = pts["R"][0] - pts["T"][0], pts["R"][1] - pts["T"][1]
assert (dx, dy) == (4, 3)
mcq(DIR, "Point-to-point", "Advanced",
    "In a certain code:\n'A # B' means 'A is 3 m north of B';\n'A $ B' means 'A is 4 m east of B';\n'A @ B' means "
    "'A is 3 m south of B';\n'A % B' means 'A is 4 m west of B'.\n\nIf 'P # Q', 'R $ Q', 'S @ R' and 'T % S', what is "
    "the shortest distance between R and T, and in which direction is R with respect to T?",
    f"{dist(dx, dy)} m, {compass(dx, dy)}", ["5 m, South-West", "7 m, North-East", "4 m, North"],
    "Coded directions converted to coordinates",
    "With Q at (0, 0): P = (0, 3), R = (4, 0), S = (4, −3), T = (0, −3). R − T = (4, 3), so R is 5 m from T, towards "
    "the north-east.",
    ["Q = (0, 0); P # Q → P = (0, 3); R $ Q → R = (4, 0)", "S @ R → S = (4, −3); T % S → T = (0, −3)",
     "R − T = (4, 3) → distance √(16 + 9) = 5 m; east and north of T → North-East"],
    why_others_wrong="South-West is T's direction from R (the reverse).", seconds=70, verified_by=RECOMP)
pts = {"K": (0, 0)}
for a, b, d, (ux, uy) in [("J", "K", 6, (1, 0)), ("L", "J", 8, (0, 1)), ("M", "L", 12, (-1, 0)),
                          ("N", "M", 8, (0, -1)), ("O", "N", 3, (1, 0)), ("P", "O", 4, (0, 1))]:
    pts[a] = (pts[b][0] + ux * d, pts[b][1] + uy * d)
dx, dy = pts["K"][0] - pts["P"][0], pts["K"][1] - pts["P"][1]
assert (dx, dy) == (3, -4)
mcq(DIR, "Point-to-point", "Advanced",
    "Point J is 6 m east of point K. Point L is 8 m north of point J. Point M is 12 m west of point L. Point N is 8 m "
    "south of point M. Point O is 3 m east of point N. Point P is 4 m north of point O. How far is point K from point "
    "P, and in which direction?", f"{dist(dx, dy)} m, {compass(dx, dy)}",
    ["5 m, North-West", "3 m, East", "7 m, South-East"], "Long chain of points on a grid",
    "With K at (0, 0): J = (6, 0), L = (6, 8), M = (−6, 8), N = (−6, 0), O = (−3, 0), P = (−3, 4). K − P = (3, −4): "
    "5 m to the south-east.",
    ["K (0, 0) → J (6, 0) → L (6, 8) → M (−6, 8)", "N (−6, 0) → O (−3, 0) → P (−3, 4)",
     "K − P = (3, −4) → √(9 + 16) = 5 m; east and south → South-East"],
    why_others_wrong="North-West is P's direction from K; 3 m is only the east–west gap.", seconds=75,
    verified_by=RECOMP)
r = walk("E", [(None, 10), ("L", 6), ("L", 4)])
sh = walk("W", [(None, 6), ("R", 15)])
dx, dy = sh[0] - r[0], sh[1] - r[1]
assert r == (6, 6) and sh == (-6, 15) and (dx, dy) == (-12, 9)
mcq(DIR, "Distance and direction", "Advanced",
    "Rohit and Sohan start from the same point X. Rohit walks 10 m east, turns left and walks 6 m, then turns left "
    "again and walks 4 m. Sohan walks 6 m west, then turns right and walks 15 m. What is the shortest distance between "
    "Rohit and Sohan now, and in which direction is Sohan with respect to Rohit?",
    f"{dist(dx, dy)} m, {compass(dx, dy)}", ["15 m, South-East", "21 m, North-West", "12 m, West"],
    "Two walkers: subtract final positions",
    "Rohit ends at (6, 6) and Sohan at (−6, 15). Sohan − Rohit = (−12, 9), so the distance is √(144 + 81) = 15 m and "
    "Sohan is to the north-west of Rohit.",
    ["Rohit: (10, 0) → left (north) 6 → (10, 6) → left (west) 4 → (6, 6)",
     "Sohan: west 6 → (−6, 0) → right (north) 15 → (−6, 15)",
     "Difference (−12, 9) → 15 m; west and north → North-West"],
    why_others_wrong="South-East is Rohit's direction from Sohan; 21 m adds the legs instead of using Pythagoras.",
    seconds=80, verified_by=RECOMP)

# ================================================================================================ CODING-DECODING
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


# ---- Basic
assert shift("MANGO", 1) == "NBOHP"
ans = shift("GRAPE", 1)
mcq(COD, "Letter coding", "Basic", "In a certain code language, MANGO is written as NBOHP. How is GRAPE written in "
    "that code language?", ans, ["HSBPF", "ISBQF", "HSCQF"], "Uniform forward shift",
    "Each letter of MANGO moves one place forward (M→N, A→B, N→O, G→H, O→P). Applying +1 to GRAPE gives "
    f"{ans}.", ["MANGO → NBOHP: every letter +1", "G→H, R→S, A→B, P→Q, E→F", f"GRAPE → {ans}"], seconds=30,
    verified_by=RECOMP)
wsum = lambda w: sum(pos(c) for c in w)
assert wsum("CAT") == 24
ans = wsum("DOG")
mcq(COD, "Number coding", "Basic", "If CAT is coded as 24, how will DOG be coded in the same code?", str(ans),
    ["25", "27", "28"], "Sum of alphabetical positions",
    "CAT = 3 + 1 + 20 = 24, so a word is coded as the sum of its letters' positions. DOG = 4 + 15 + 7 = 26.",
    ["C = 3, A = 1, T = 20 → 24 (matches)", "D = 4, O = 15, G = 7", f"Sum = {ans}"], natural=int, seconds=30,
    verified_by=RECOMP)
code3 = lambda w: shift(w, 1)[::-1]
assert code3("BRANCH") == "IDOBSC"
ans = code3("LOAN")
mcq(COD, "Letter coding", "Basic", "In a certain code, BRANCH is written as IDOBSC. How is LOAN written in that "
    "code?", ans, ["MPBO", "OBQM", "NBPM"], "Shift, then reverse",
    "Each letter of BRANCH is moved one place forward (CSBODI) and the result is written in reverse (IDOBSC). LOAN → "
    f"MPBO → reversed {ans}.", ["BRANCH +1 → CSBODI", "Reverse → IDOBSC (matches)", f"LOAN +1 → MPBO → reverse → {ans}"],
    why_others_wrong="MPBO forgets the reversal.", seconds=35, verified_by=RECOMP)
sents = [(["bank", "loan", "rate"], ["ka", "pi", "zo"]), (["loan", "is", "low"], ["zo", "mu", "re"]),
         (["rate", "is", "high"], ["pi", "mu", "tu"])]
got = sentence_solve(sents, "loan")
assert got == {"zo"}
mcq(COD, "Sentence/word coding", "Basic",
    "In a certain code language:\n'bank loan rate' is written as 'ka pi zo',\n'loan is low' is written as "
    "'zo mu re', and\n'rate is high' is written as 'pi mu tu'.\nWhat is the code for 'loan'?", "zo",
    ["pi", "mu", "ka"], "Common word ↔ common code",
    "'loan' appears in the first two sentences, and the only code common to them is 'zo'.",
    ["Sentences 1 and 2 share the word 'loan' and the code 'zo'", "So loan = zo",
     "(Also: rate = pi from sentences 1 and 3, is = mu from 2 and 3)"], seconds=35, verified_by=RECOMP)

# ---- Intermediate
sents = [(["save", "money", "now"], ["la", "ri", "ko"]), (["money", "grows", "fast"], ["ri", "tu", "pe"]),
         (["save", "time", "now"], ["ko", "sa", "la"]), (["time", "grows", "slowly"], ["sa", "pe", "mi"])]
got = sentence_solve(sents, "fast")
assert got == {"tu"}
mcq(COD, "Sentence/word coding", "Intermediate",
    "In a certain code language:\n'save money now' is written as 'la ri ko',\n'money grows fast' is written as "
    "'ri tu pe',\n'save time now' is written as 'ko sa la', and\n'time grows slowly' is written as 'sa pe mi'.\n"
    "What is the code for 'fast'?", "tu", ["pe", "ri", "mi"], "Elimination across several sentences",
    "money = ri (sentences 1 and 2), grows = pe (sentences 2 and 4). The remaining code of sentence 2, 'tu', must be "
    "'fast'.", ["Sentences 1 & 2: money = ri", "Sentences 2 & 4: grows = pe", "Sentence 2 = money grows fast = ri tu "
                "pe ⇒ fast = tu"], seconds=45, verified_by=RECOMP)
opp = lambda w: "".join(AL[26 - pos(c)] for c in w)
assert opp("LOCKER") == "OLXPVI"
ans = opp("SAFETY")
mcq(COD, "Letter coding", "Intermediate", "In a certain code, LOCKER is written as OLXPVI. How is SAFETY written "
    "in that code?", ans, ["HZVUGB", "HAUVGB", "GZUVHB"], "Opposite-letter (A↔Z) coding",
    "Each letter is replaced by its opposite in the alphabet (position p → 27 − p): L↔O, O↔L, C↔X, K↔P, E↔V, R↔I. "
    f"SAFETY → {ans}.", ["Check: L (12) → O (15), O (15) → L (12), C (3) → X (24)",
                         "S→H, A→Z, F→U, E→V, T→G, Y→B", f"SAFETY → {ans}"],
    shortcut="Opposite pairs to remember: A-Z, E-V, F-U, S-H, T-G, Y-B.", seconds=45, verified_by=RECOMP)
rpos = lambda w: " ".join(str(27 - pos(c)) for c in w)
assert rpos("PEARL") == "11 22 26 9 15"
ans = rpos("STONE")
mcq(COD, "Number coding", "Intermediate", "In a certain code, PEARL is written as '11 22 26 9 15'. How is STONE "
    "written in that code?", ans, ["19 20 15 14 5", "8 7 13 12 22", "7 8 12 13 22"], "Reverse alphabetical position",
    "Each letter is coded by its position counted from Z (27 − position): P (16) → 11, E (5) → 22, A (1) → 26. For "
    f"STONE: S → 8, T → 7, O → 12, N → 13, E → 22.", ["P = 16 → 27 − 16 = 11 (matches)", "S = 19 → 8; T = 20 → 7; "
                                                      "O = 15 → 12; N = 14 → 13; E = 5 → 22", f"STONE → {ans}"],
    why_others_wrong="'19 20 15 14 5' uses forward positions; the other two swap a pair of digits.", seconds=45,
    verified_by=RECOMP)


def halves(w):
    h = len(w) // 2
    return w[:h][::-1] + (w[h] if len(w) % 2 else "") + w[len(w) - h:][::-1]


assert halves("CHAPTER") == "AHCPRET"
ans = halves("DEPOSIT")
mcq(COD, "Letter coding", "Intermediate", "In a certain code, CHAPTER is written as AHCPRET. How is DEPOSIT written "
    "in that code?", ans, ["PEDOSIT", "DEPOTIS", "TISOPED"], "Reversing each half around the middle letter",
    "CHAPTER = CHA | P | TER; each three-letter half is reversed (AHC, RET) and the middle letter stays. DEPOSIT = "
    f"DEP | O | SIT → PED O TIS = {ans}.", ["CHA → AHC, P stays, TER → RET (matches)", "DEP → PED, O stays, SIT → TIS",
                                            f"DEPOSIT → {ans}"], seconds=40, verified_by=RECOMP)
sents = [(["credit", "card", "limit"], ["xo", "ve", "li"]), (["card", "fee", "waived"], ["ve", "ra", "qu"]),
         (["limit", "fee", "raised"], ["li", "ra", "ne"]), (["credit", "score", "raised"], ["xo", "ne", "su"])]
got = sentence_solve(sents, "ra")
assert got == {"fee"}
mcq(COD, "Sentence/word coding", "Intermediate",
    "In a certain code language:\n'credit card limit' is written as 'xo ve li',\n'card fee waived' is written as "
    "'ve ra qu',\n'limit fee raised' is written as 'li ra ne', and\n'credit score raised' is written as 'xo ne su'.\n"
    "What does the code 'ra' stand for?", "fee", ["waived", "raised", "limit"], "Decoding a code back to its word",
    "'ra' appears in sentences 2 and 3, and the only word common to those sentences is 'fee'.",
    ["Sentences 2 and 3 share the code 'ra' and the word 'fee'", "So ra = fee",
     "(Also: card = ve, limit = li, raised = ne, credit = xo)"], seconds=45, verified_by=RECOMP)

# ---- Advanced
TAB = {"A": "7", "D": "%", "E": "2", "G": "@", "K": "5", "M": "9", "P": "#", "R": "4", "T": "©", "U": "8"}
VOW = set("AEIOU")


def table_code(w):
    c = [TAB[x] for x in w]
    f, l = w[0], w[-1]
    if f in VOW and l not in VOW:
        c[0], c[-1] = c[-1], c[0]
    elif f not in VOW and l in VOW:
        c[0] = c[-1] = TAB[l]
    elif f not in VOW and l not in VOW:
        c[0] = c[-1] = "★"
    return "".join(c)


ans = table_code("PADKER")
assert ans == "★7%52★"
TAB_TXT = ("Study the letter codes and conditions below.\n\n| Letter | A | D | E | G | K | M | P | R | T | U |\n"
           "|---|---|---|---|---|---|---|---|---|---|---|\n| Code | 7 | % | 2 | @ | 5 | 9 | # | 4 | © | 8 |\n\n"
           "Conditions (apply only the first one that fits):\n(i) If the first letter is a vowel and the last letter "
           "is a consonant, the codes of the first and last letters are interchanged.\n(ii) If the first letter is a "
           "consonant and the last letter is a vowel, both are coded as the code of the vowel.\n(iii) If both the "
           "first and the last letters are consonants, both are coded as ★.\n\n")
mcq(COD, "Letter coding", "Advanced", TAB_TXT + "What is the code for the letter group PADKER?", ans,
    ["#7%524", "4%7%5#", "★7%5★2"], "Table coding with conditions",
    "PADKER begins with P and ends with R, both consonants, so condition (iii) applies: both end letters become ★, "
    "and the middle letters keep their table codes (A 7, D %, K 5, E 2).",
    ["First letter P (consonant), last letter R (consonant): condition (iii)", "Middle: A → 7, D → %, K → 5, E → 2",
     f"Code: ★ 7 % 5 2 ★ = {ans}"],
    why_others_wrong="'#7%524' ignores the conditions; '★7%5★2' places ★ on the wrong letter.", seconds=60,
    verified_by=RECOMP)
sents = [(["risk", "free", "bond", "yield"], ["ga", "lo", "mi", "tu"]), (["bond", "yield", "rises"], ["mi", "tu", "ve"]),
         (["free", "credit", "offer"], ["lo", "pa", "ke"]), (["credit", "risk", "rises"], ["pa", "ga", "ve"])]
assert sentence_solve(sents, "risk") == {"ga"} and sentence_solve(sents, "offer") == {"ke"}
assert sentence_solve(sents, "bond") == {"mi", "tu"}
mcq(COD, "Sentence/word coding", "Advanced",
    "In a certain code language:\n'risk free bond yield' is written as 'ga lo mi tu',\n'bond yield rises' is written "
    "as 'mi tu ve',\n'free credit offer' is written as 'lo pa ke', and\n'credit risk rises' is written as "
    "'pa ga ve'.\nWhat is the code for 'risk offer'?", "ga ke", ["ga lo", "ke pa", "mi ke"],
    "Multi-step elimination (codes may appear in any order)",
    "bond and yield take mi and tu (sentences 1 and 2), so rises = ve. free = lo (sentences 1 and 3), credit = pa "
    "(sentences 3 and 4), so risk = ga (the remaining code of sentence 4) and offer = ke (the remaining code of "
    "sentence 3). 'risk offer' = 'ga ke'.",
    ["Sentences 1 & 2: {bond, yield} = {mi, tu} ⇒ rises = ve", "Sentences 1 & 3: free = lo",
     "Sentences 3 & 4: credit = pa", "Sentence 4: credit pa, rises ve ⇒ risk = ga",
     "Sentence 3: free lo, credit pa ⇒ offer = ke", "risk offer = ga ke"],
    why_others_wrong="'mi ke' fails because mi belongs to bond or yield, which cannot be told apart.", seconds=75,
    verified_by=RECOMP)
VOWELS = set("AEIOU")
rule12 = lambda w: "".join(AL[(pos(c) + 1) % 26] if c in VOWELS else AL[pos(c) - 2] for c in w)[::-1]
assert rule12("BANK") == "JMCA"
ans = rule12("CLIENT")
mcq(COD, "Letter coding", "Advanced",
    "In a certain code, each vowel of a word is replaced by the letter two places after it in the English alphabet, "
    "each consonant by the letter immediately before it, and the resulting letters are then written in reverse "
    "order. For example, BANK is written as JMCA. How is CLIENT written in that code?", ans,
    ["BKKGMS", "SMGKKD", "SMGJKB"], "Separate rules for vowels and consonants, then reversal",
    "C→B, L→K, I→K, E→G, N→M, T→S gives BKKGMS; reversing gives SMGKKB.",
    ["Check BANK: B→A, A→C, N→M, K→J = ACMJ → reverse JMCA (matches)",
     "CLIENT: consonants −1 (C→B, L→K, N→M, T→S); vowels +2 (I→K, E→G)", "BKKGMS → reverse → SMGKKB"],
    why_others_wrong="BKKGMS skips the reversal; the other two mis-shift one letter.", seconds=70,
    verified_by=RECOMP)
dsum = lambda n: n if n < 10 else dsum(sum(int(c) for c in str(n)))
code13 = lambda w: "".join(str(dsum(pos(c))) for c in w)[::-1]
assert code13("KITE") == "5292"
ans = code13("MOTOR")
mcq(COD, "Number coding", "Advanced",
    "In a certain code, KITE is written as 5292: each letter is replaced by the digit sum of its alphabetical "
    "position (reduced to a single digit), and the digits are then written in reverse order. How is MOTOR written in "
    "that code?", ans, ["46269", "96246", "69264"], "Digit sums of positions, then reversal",
    "M = 13 → 4, O = 15 → 6, T = 20 → 2, O → 6, R = 18 → 9, giving 46269; reversed, 96264.",
    ["Check KITE: K 11 → 2, I 9, T 20 → 2, E 5 → 2925 → reverse 5292 (matches)",
     "MOTOR: 13 → 4, 15 → 6, 20 → 2, 15 → 6, 18 → 9 → 46269", "Reverse → 96264"],
    why_others_wrong="46269 skips the reversal.", seconds=60, verified_by=RECOMP)

# ================================================================================================ ALPHANUMERIC SERIES
ALN = "Alphanumeric Series"
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


# ---- Basic
SR = "R 4 # M 7 K @ 2 P E 9 $ T 3 & B 5 W".split()
ans = SR[9 - 1 + 6]
mcq(ALN, "Position-based", "Basic", series_intro(" ".join(SR)) +
    "\n\nWhich element is 6th to the right of the 9th element from the left end?", ans, ["3", "B", "T"],
    "Position arithmetic in a series",
    f"6th to the right of the 9th from the left is the (9 + 6) = 15th element from the left: {ans}.",
    ["9th from the left = P", "Counting 6 to the right: E, 9, $, T, 3, &", f"15th element = {ans}"],
    shortcut="Same direction: add the positions (9 + 6 = 15 from the left).", seconds=35, verified_by=RECOMP)
SR = "D 8 % L 3 Q © 6 A 1 ★ N 5 H 2 # Y 7".split()
c = sum(1 for i in range(1, len(SR)) if is_d(SR[i]) and is_l(SR[i - 1]))
a, w = count_opts(c)
mcq(ALN, "Symbol and number series", "Basic", series_intro(" ".join(SR)) +
    "\n\nHow many numbers in the arrangement are immediately preceded by a letter?", a, w,
    "Scanning adjacent pairs", "Look at every number and check the element just before it: "
    + ", ".join(f"{SR[i - 1]} {SR[i]}" for i in range(1, len(SR)) if is_d(SR[i]) and is_l(SR[i - 1])) +
    f". That is {c}.", ["List each number with the element before it",
                        "Keep the pairs where the earlier element is a letter",
                        "Pairs: " + "; ".join(f"{SR[i - 1]}{SR[i]}" for i in range(1, len(SR))
                                              if is_d(SR[i]) and is_l(SR[i - 1])), f"Count = {c}"],
    natural=by_num, seconds=40, verified_by=RECOMP)

# ---- Intermediate
SR = "H 3 % K 8 R © 1 A 6 # Z D 4 ★ U 9 M @ 2 F E 7 $ G".split()
hits = [x for x in windows(SR) if is_s(x[1]) and is_d(x[0]) and is_l(x[2])]
a, w = count_opts(len(hits))
mcq(ALN, "Symbol and number series", "Intermediate", series_intro(" ".join(SR)) +
    "\n\nHow many symbols in the arrangement are immediately preceded by a number and immediately followed by a "
    "letter?", a, w, "Number–symbol–letter triplets",
    "Qualifying triplets (number, symbol, letter): " + "; ".join(" ".join(x) for x in hits) + f". Total {len(hits)}.",
    ["Check every symbol: %, ©, #, ★, @, $", "Keep those with a number before and a letter after",
     "Found: " + ", ".join(" ".join(x) for x in hits)], natural=by_num, seconds=50, verified_by=RECOMP)
SR = "5 B @ T 9 E 2 # K M 6 & 1 R I ★ 8 S $ 3 L A 4 % W".split()
nos = [t for t in SR if not is_s(t)]
ans = nos[14 - 5 - 1]
mcq(ALN, "Position-based", "Intermediate", series_intro(" ".join(SR)) +
    "\n\nIf all the symbols are removed from the arrangement, which element will be 5th to the left of the 14th "
    "element from the left end?", ans, ["K", "W", "M"], "Rewriting the series before counting",
    f"Without symbols the series is: {' '.join(nos)}. 5th to the left of the 14th element is the (14 − 5) = 9th "
    f"element: {ans}.", ["Remove @, #, &, ★, $, %", "New series: " + " ".join(nos),
                         f"14 − 5 = 9th from the left = {ans}"],
    why_others_wrong="K is the 9th element of the original series (symbols not removed); W is 5th to the right of "
                     "the 14th; M is an off-by-one count.",
    seconds=55, verified_by=RECOMP)
SR = "J 7 E 4 @ U 2 Q # O 8 V I 1 & S 6 A $ 9 C ★ 5 G".split()
hits = [(SR[i], SR[i + 1]) for i in range(len(SR) - 1) if SR[i] in "AEIOU" and is_d(SR[i + 1])]
a, w = count_opts(len(hits))
mcq(ALN, "Symbol and number series", "Intermediate", series_intro(" ".join(SR)) +
    "\n\nHow many vowels in the arrangement are immediately followed by a number?", a, w, "Vowel–number pairs",
    "Vowels followed by a number: " + "; ".join(f"{v} {d}" for v, d in hits) + f". Total {len(hits)}.",
    ["Vowels present: E, U, O, I, A", "Check the element after each", "Qualifying: " +
     ", ".join(f"{v}{d}" for v, d in hits)], natural=by_num, seconds=45, verified_by=RECOMP)

# ---- Advanced
SR = "B 4 $ R 9 E K @ 2 W 6 # A M 1 % Y 8 I © T 3 F 5 ★ N".split()
new = SR[:13][::-1] + SR[13:]
ans = new[5 - 1 + 8]
mcq(ALN, "Position-based", "Advanced", series_intro(" ".join(SR)) +
    "\n\nIf the first thirteen elements of the arrangement are written in reverse order, which element will be 8th "
    "to the right of the 5th element from the left end?", ans, ["@", "R", "Y"], "Partial reversal, then counting",
    f"After reversing the first 13 elements the series begins {' '.join(new[:15])} … The 5th + 8 = 13th element is "
    f"{ans}.", ["First 13 reversed: " + " ".join(SR[:13][::-1]), "Rest unchanged: " + " ".join(SR[13:]),
                f"13th element of the new series = {ans}"],
    why_others_wrong=f"In the new series @, R and Y are the {new.index('@') + 1}th, {new.index('R') + 1}th and "
                     f"{new.index('Y') + 1}th elements, so they come from miscounting; without the reversal the 13th "
                     f"element would be {SR[12]}.", seconds=70, verified_by=RECOMP)
SR = "8 @ 3 G % 6 7 K # 2 4 © P 5 ★ 9 1 $ Q 6 & 3 D".split()
hits = [x for x in windows(SR) if is_d(x[1]) and int(x[1]) % 2 == 0 and is_s(x[0]) and is_d(x[2])
        and int(x[2]) % 2 == 1]
a, w = count_opts(len(hits))
mcq(ALN, "Symbol and number series", "Advanced", series_intro(" ".join(SR)) +
    "\n\nHow many even numbers in the arrangement are immediately preceded by a symbol and immediately followed by "
    "an odd number?", a, w, "Three-condition triplets",
    "Triplets (symbol, even number, odd number): " + ("; ".join(" ".join(x) for x in hits) or "none") +
    f". Total {len(hits)}.",
    ["Even numbers: 8, 6, 2, 4, 6", "Check the element before (symbol?) and after (odd number?)",
     "Qualifying: " + (", ".join(" ".join(x) for x in hits) or "none")], natural=by_num, seconds=60,
    verified_by=RECOMP)

# ================================================================================================ ALPHABET TEST
ABT = "Alphabet Test"


def letter_pairs(word):
    return [(word[i], word[j]) for i in range(len(word)) for j in range(i + 1, len(word))
            if abs(pos(word[j]) - pos(word[i])) == j - i]


ans = AL[15 + 7 - 1]
mcq(ABT, "Letter position", "Basic", "Which letter is 7th to the right of the 15th letter from the left end of the "
    "English alphabet?", ans, ["W", "H", "U"], "Position arithmetic in the alphabet",
    f"7th to the right of the 15th letter is the (15 + 7) = 22nd letter: {ans}.",
    ["15th letter = O", "15 + 7 = 22", f"22nd letter = {ans}"],
    shortcut="Remember E-J-O-T-Y = 5-10-15-20-25; 22 is two after T.", seconds=25, verified_by=RECOMP)
W = "GARDEN"
pr = letter_pairs(W)
a, w = count_opts(len(pr))
mcq(ABT, "Pairs of letters", "Basic", f"How many pairs of letters are there in the word '{W}' each of which has as "
    "many letters between them in the word as in the English alphabet (counting both forward and backward)?", a, w,
    "Comparing word gaps with alphabet gaps",
    "Pairs found: " + (", ".join(f"{x}{y}" for x, y in pr) or "none") + f". Total {len(pr)}.",
    [f"Positions: " + ", ".join(f"{ch} = {pos(ch)}" for ch in W),
     "For each pair, compare the gap in the word with the gap in the alphabet",
     "Matching pairs: " + (", ".join(f"{x}–{y}" for x, y in pr) or "none")], natural=by_num, seconds=45,
    verified_by=RECOMP)
REV = AL[::-1]
ans = REV[11 + 6 - 1]
mcq(ABT, "Letter position", "Intermediate", "If the English alphabet is written in reverse order (Z to A), which "
    "letter will be 6th to the right of the 11th letter from the left end?", ans, ["Q", "U", "K"],
    "Positions in a reversed alphabet",
    f"In the reversed alphabet the k-th letter from the left is the (27 − k)-th letter of the normal alphabet. "
    f"11 + 6 = 17th from the left → 27 − 17 = 10th normal letter: {ans}.",
    ["Reversed alphabet: Z Y X W V U T S R Q P O N M L K J …", "11th from left = P; 6 more to the right → 17th",
     f"17th from left in the reversed alphabet = {ans}"], why_others_wrong="Q is the result of using the normal "
                                                                           "alphabet (17th letter).",
    seconds=40, verified_by=RECOMP)
assert AL[17 - 1] == "Q"
W = "MAGNETIC"
chosen = sorted(W[i - 1] for i in (1, 2, 5, 6))
WORDS4 = ["MATE", "MEAT", "TEAM", "TAME"]  # common English words using exactly M, A, E, T
assert chosen == sorted("MATE") and all(sorted(x) == chosen for x in WORDS4)
mcq(ABT, "Word formation", "Intermediate",
    "If a meaningful English word is formed using the 1st, 2nd, 5th and 6th letters of the word 'MAGNETIC', each "
    "letter used exactly once, what is the first letter of that word? If no such word can be formed, choose 'No "
    "such word can be formed'; if more than one such word can be formed, choose 'More than one such word can be "
    "formed'.", "More than one such word can be formed", ["M", "T", "No such word can be formed"],
    "Picking letters by position, then forming words",
    "The letters are M, A, E and T. They form several words: MATE, MEAT, TEAM and TAME. So more than one word can "
    "be formed.", ["1st M, 2nd A, 5th E, 6th T", "Words: MATE, MEAT, TEAM, TAME", "More than one word"],
    why_others_wrong="M and T are first letters of some of the words, but there is no single word.", seconds=40,
    verified_by=HAND)
W = "TRANSPORT"
pr = letter_pairs(W)
a, w = count_opts(len(pr))
mcq(ABT, "Pairs of letters", "Advanced", f"How many pairs of letters are there in the word '{W}' each of which has "
    "as many letters between them in the word as in the English alphabet (counting both forward and backward)?",
    a, w, "Exhaustive pair checking in a longer word",
    "Pairs found: " + (", ".join(f"{x}{y}" for x, y in pr) or "none") + f". Total {len(pr)}.",
    [f"Positions: " + ", ".join(f"{ch} = {pos(ch)}" for ch in W),
     "Check every pair (i, j): |alphabet gap| must equal j − i",
     "Matching pairs: " + (", ".join(f"{x}–{y}" for x, y in pr) or "none")], natural=by_num, seconds=75,
    verified_by=RECOMP)
W = "EDUCATION"
conv = [AL[pos(ch)] if ch in VOWELS else AL[pos(ch) - 2] for ch in W]
srt = sorted(conv)
ans = srt[-3]
mcq(ABT, "Letter position", "Advanced",
    "In the word 'EDUCATION', each vowel is replaced by the letter immediately after it in the English alphabet and "
    "each consonant by the letter immediately before it. The new letters are then arranged in alphabetical order "
    "from left to right. Which letter will be 3rd from the right end?", ans, ["S", "J", "M"],
    "Transform, sort, then count from the right",
    f"The new letters are {' '.join(conv)}; in alphabetical order {' '.join(srt)}. The 3rd from the right is {ans}.",
    ["E→F, D→C, U→V, C→B, A→B, T→S, I→J, O→P, N→M", "New letters: " + " ".join(conv),
     "Sorted: " + " ".join(srt), f"3rd from the right: {ans}"], seconds=70, verified_by=RECOMP)

# ================================================================================================ NUMBER-BASED
NUM = "Number Series (Reasoning)"
NS = [742, 319, 865, 427, 583]
sw = {n: int(str(n)[::-1]) for n in NS}
ans = max(NS, key=sw.get)
mcq(NUM, "Three-digit number questions", "Basic",
    "Study the following five numbers:\n742   319   865   427   583\n\nIf the first and the third digits of each "
    "number are interchanged, which number will become the largest?", str(ans), ["865", "742", "583"],
    "Digit interchange", "After interchange: " + ", ".join(f"{n} → {sw[n]}" for n in NS) +
    f". The largest new number is {sw[ans]}, which comes from {ans}.",
    ["Swap first and third digits: " + ", ".join(f"{n}→{sw[n]}" for n in NS), f"Largest: {sw[ans]} (from {ans})"],
    why_others_wrong="865 is the largest before the interchange.", seconds=35, verified_by=RECOMP)
NS = [476, 813, 592, 368, 735]
nw = {n: (n // 100 + 1) * 100 + (n // 10 % 10) * 10 + (n % 10 - 1) for n in NS}
c = sum(1 for v in nw.values() if v % 3 == 0)
a, w = count_opts(c)
mcq(NUM, "Number-based digit operations", "Intermediate",
    "Study the following five numbers:\n476   813   592   368   735\n\nIf 1 is added to the first digit of each "
    "number and 1 is subtracted from its last digit, how many of the new numbers will be divisible by 3?", a, w,
    "Digit operations and the divisibility rule for 3",
    "New numbers: " + ", ".join(f"{nw[n]}" for n in NS) + ". A number is divisible by 3 when its digit sum is. "
    + "; ".join(f"{nw[n]}: {sum(map(int, str(nw[n])))}" for n in NS) + f". So {c} are divisible by 3.",
    ["New numbers: " + ", ".join(f"{n}→{nw[n]}" for n in NS),
     "Digit sums: " + ", ".join(str(sum(map(int, str(nw[n])))) for n in NS),
     f"Multiples of 3: {', '.join(str(nw[n]) for n in NS if nw[n] % 3 == 0)}"],
    shortcut="The operation does not change the digit sum (+1 and −1), so test the original numbers.",
    natural=by_num, seconds=45, verified_by=RECOMP)
assert all(sum(map(int, str(n))) == sum(map(int, str(nw[n]))) for n in NS)
NS = [518, 364, 927, 285, 619]
ds_ = {n: int("".join(sorted(str(n), reverse=True))) for n in NS}
vals = sorted(ds_.values(), reverse=True)
ans = vals[1] - vals[-1]
mcq(NUM, "Three-digit number questions", "Intermediate",
    "Study the following five numbers:\n518   364   927   285   619\n\nIf the digits within each number are "
    "arranged in descending order, what is the difference between the second highest and the lowest of the new "
    "numbers?", str(ans), ["329", "309", "321"], "Rearranging digits within numbers",
    "New numbers: " + ", ".join(f"{n} → {ds_[n]}" for n in NS) + f". Second highest = {vals[1]}, lowest = "
    f"{vals[-1]}; difference = {ans}.", ["Descending digits: " + ", ".join(f"{n}→{ds_[n]}" for n in NS),
                                        "Order: " + " > ".join(map(str, vals)), f"{vals[1]} − {vals[-1]} = {ans}"],
    natural=int, seconds=50, verified_by=RECOMP)
NS = [638, 471, 925, 362, 814]
sw = {n: int(str(n)[0] + str(n)[2] + str(n)[1]) for n in NS}
order = sorted(sw.values())
mid = order[2]
ans = int(str(mid)[0]) * int(str(mid)[2])
mcq(NUM, "Number-based digit operations", "Advanced",
    "Study the following five numbers:\n638   471   925   362   814\n\nIf the second and third digits of each number "
    "are interchanged and the new numbers are arranged in ascending order, what is the product of the first and last "
    "digits of the number in the middle?", str(ans), ["48", "28", "8"], "Interchange, sort, then operate",
    "After interchange: " + ", ".join(f"{n} → {sw[n]}" for n in NS) + f". Ascending: {', '.join(map(str, order))}. "
    f"The middle number is {mid}, and {str(mid)[0]} × {str(mid)[2]} = {ans}.",
    ["Interchange 2nd and 3rd digits: " + ", ".join(f"{n}→{sw[n]}" for n in NS),
     "Ascending: " + ", ".join(map(str, order)), f"Middle: {mid}; {str(mid)[0]} × {str(mid)[2]} = {ans}"],
    why_others_wrong="48 comes from the original middle number 638 (no interchange); 28 and 8 come from taking 417 "
                     "or 841 as the middle number.", natural=int, seconds=60, verified_by=RECOMP)

# ================================================================================================ RANKING
RNK = "Ranking and Order"
n_, meena, raju_r = 40, 14, 20
raju = n_ - raju_r + 1
gap = abs(raju - meena) - 1
mcq(RNK, "Position in a row", "Basic", "In a row of 40 students facing north, Meena is 14th from the left end and "
    "Raju is 20th from the right end. How many students sit between Meena and Raju?", str(gap), ["5", "7", "4"],
    "Converting a right-end rank to a left-end rank",
    f"Raju's position from the left = 40 − 20 + 1 = {raju}. Between positions 14 and {raju} there are {gap} students.",
    [f"Raju from left = 40 − 20 + 1 = {raju}", f"Between 14 and {raju}: {raju} − 14 − 1 = {gap}"],
    natural=int, seconds=35, verified_by=RECOMP)
tot = 9 + 32 - 1
mcq(RNK, "Position in a row", "Basic", "Arjun ranks 9th from the top and 32nd from the bottom in his class. How "
    "many students are there in the class?", str(tot), ["41", "39", "42"], "Total = rank from top + rank from bottom "
    "− 1", f"Arjun is counted in both ranks, so the class has 9 + 32 − 1 = {tot} students.",
    [f"9 + 32 − 1 = {tot}"], why_others_wrong="41 counts Arjun twice.", natural=int, seconds=25, verified_by=RECOMP)
b_front = 22
tot = b_front + 18 - 1
mcq(RNK, "Position in a row", "Intermediate", "In a queue, Amit is 12th from the front and Bala is 18th from the "
    "back. If they interchange their positions, Amit becomes 22nd from the front. How many people are there in the "
    "queue?", str(tot), ["40", "33", "38"], "Interchange of positions",
    f"After interchange Amit stands where Bala stood, so Bala's position was 22nd from the front and 18th from the "
    f"back. Total = 22 + 18 − 1 = {tot}.", ["Bala's place = 22nd from front (Amit's new place)",
                                             "Bala's place = 18th from back", f"Total = 22 + 18 − 1 = {tot}"],
    why_others_wrong="33 uses Amit's old position (12 + 22 − 1).", natural=int, seconds=40, verified_by=RECOMP)
P = list("PQRSTU")
conds = [("P is heavier than Q but lighter than U.", ("P", "Q", "U"), lambda p, q_, u: q_ < p < u),
         ("R is lighter than Q but heavier than T.", ("R", "Q", "T"), lambda r, q_, t: t < r < q_),
         ("S is the lightest.", tuple(P), lambda *v: v[3] == 1)]
RK = unique(P, {p: range(1, 7) for p in P}, conds, [P])
heavy = sorted(P, key=RK.get, reverse=True)
assert heavy == list("UPQRTS")
mcq(RNK, "Comparison of heights/weights", "Intermediate",
    "Six boxes P, Q, R, S, T and U have different weights. P is heavier than Q but lighter than U. R is lighter than "
    "Q but heavier than T. S is the lightest.\n\nWhich box is the third heaviest?", heavy[2], ["P", "R", "T"],
    "Merging two comparison chains", "U > P > Q and Q > R > T join into U > P > Q > R > T, with S lightest. The "
    "third heaviest is Q.", ["U > P > Q", "Q > R > T", "Combined: U > P > Q > R > T > S", "Third from the top: Q"],
    seconds=40, verified_by=BRUTE)
# Advanced: unknown row length
p_, q__ = 7, 7 + 5
r_ = q__ + 1
tot = r_ + 9 - 1
mid = (tot + 1) // 2
assert tot % 2 == 1
gap = abs(r_ - mid) - 1
mcq(RNK, "Position in a row", "Advanced",
    "Some persons sit in a row facing north. Pankaj is 7th from the left end. Qureshi sits 5th to the right of "
    "Pankaj. Rana sits immediately to the right of Qureshi and is 9th from the right end. Sumit sits exactly in the "
    "middle of the row. How many persons sit between Sumit and Rana?", num_word(gap), ["None", "Two", "Three"],
    "Unknown row length from overlapping ranks",
    f"Qureshi = 7 + 5 = 12th, Rana = 13th from the left. Rana is 9th from the right, so the row has 13 + 9 − 1 = "
    f"{tot} persons. The middle seat is {mid}th, and between seat {mid} and seat 13 there is {gap} person.",
    [f"Pankaj = 7, Qureshi = 12, Rana = 13 (from the left)", f"Total = 13 + 9 − 1 = {tot}",
     f"Middle of {tot} = {mid}th (Sumit)", f"Between {mid} and 13: {gap}"], natural=by_num, seconds=60,
    verified_by=RECOMP)
P = ["Nikhil", "Oorja", "Prem", "Ritika", "Shaan", "Trisha"]
conds = [("Prem is heavier than only two persons.", ("Prem",), lambda p: p == 3),
         ("Ritika is heavier than Prem but lighter than Shaan.", ("Ritika", "Prem", "Shaan"),
          lambda r, p, s_: p < r < s_),
         ("Nikhil is lighter than Oorja, and Oorja is heavier than Ritika.", ("Nikhil", "Oorja", "Ritika"),
          lambda n, o, r: n < o and o > r),
         ("Trisha is the lightest, and Oorja is not the heaviest.", ("Trisha", "Oorja"),
          lambda t, o: t == 1 and o != 6)]
RK6 = unique(P, {p: range(1, 7) for p in P}, conds, [P])
heavy = sorted(P, key=RK6.get, reverse=True)
assert heavy == ["Shaan", "Oorja", "Ritika", "Prem", "Nikhil", "Trisha"]
WT = {"Shaan": 82, "Trisha": 48, "Ritika": 67, "Nikhil": 55}
best = min(o + p for o in range(WT["Ritika"] + 1, WT["Shaan"]) for p in range(WT["Nikhil"] + 1, WT["Ritika"]))
assert best == 124
mcq(RNK, "Comparison of heights/weights", "Advanced",
    "Six persons Nikhil, Oorja, Prem, Ritika, Shaan and Trisha have different weights, each a whole number of "
    "kilograms.\n" + "\n".join(f"- {t}" for t, _, _ in conds) +
    "\n- The heaviest person weighs 82 kg and the lightest 48 kg.\n- Ritika weighs 67 kg and Nikhil 55 kg.\n\n"
    "What is the minimum possible combined weight of Oorja and Prem?", f"{best} kg", ["122 kg", "126 kg", "135 kg"],
    "Ordering, then the tightest integer bounds",
    "The order is Shaan > Oorja > Ritika > Prem > Nikhil > Trisha. Oorja must be above Ritika (67), so at least 68 "
    "kg; Prem must be above Nikhil (55), so at least 56 kg. Minimum total = 68 + 56 = 124 kg.",
    ["Prem has exactly two persons lighter: Trisha (lightest) and one more", "Ritika > Prem and Oorja > Ritika, "
     "Nikhil < Oorja: the only person who can be below Prem besides Trisha is Nikhil",
     "Ritika, Oorja and Shaan take the top three places with Ritika lowest; Oorja is not the heaviest, so Shaan is", "Order: Shaan 82 > Oorja > Ritika 67 > Prem > Nikhil 55 > Trisha 48",
     "Oorja ≥ 68, Prem ≥ 56 ⇒ minimum 124 kg"],
    why_others_wrong="122 kg uses 67 and 55 themselves, but weights are all different.",
    natural=lambda t: int(t.split()[0]), seconds=90, verified_by=BRUTE)

# ================================================================================================ INPUT-OUTPUT
IOT = "Input and Output"


def alpha_machine(words):
    steps, cur = [], list(words)
    for k in range(len(cur)):
        rest = cur[k:]
        nxt = min(rest)
        new = cur[:k] + [nxt] + [x for x in rest if x != nxt]
        if new == cur:
            break
        cur = new
        steps.append(cur[:])
    assert cur == sorted(words)
    return steps


inp = "sun bat ink cot apex dew".split()
st = alpha_machine(inp)
assert len(st) == 5 and all(st[i] != st[i + 1] for i in range(len(st) - 1))
target = "apex bat cot sun ink dew".split()
k = st.index(target) + 1
mcq(IOT, "Word rearrangement", "Basic",
    "A word arrangement machine rearranges a line of words step by step. In each step it takes the word that comes "
    "earliest in alphabetical order among the words not yet arranged and moves it to the immediate right of the words "
    "already arranged (in Step I, to the extreme left). The other words keep their order.\n\nInput: "
    + " ".join(inp) + "\n\nIn which step will the arrangement read 'apex bat cot sun ink dew'?",
    ["Step I", "Step II", "Step III", "Step IV", "Step V"][k - 1], ["Step II", "Step IV", "Step V"],
    "Simulating a one-word-per-step sorting machine",
    "Each step fixes the next word in alphabetical order at the left. After three steps apex, bat and cot are in "
    "place, giving 'apex bat cot sun ink dew'.",
    [f"Step {['I', 'II', 'III', 'IV', 'V'][i]}: " + " ".join(s_) for i, s_ in enumerate(st)],
    natural=lambda t: ["Step I", "Step II", "Step III", "Step IV", "Step V"].index(t), seconds=45,
    verified_by=RECOMP)
assert k == 3


def desc_machine(nums):
    steps, cur = [], list(nums)
    for k_ in range(len(cur)):
        rest = cur[k_:]
        nxt = max(rest)
        new = cur[:k_] + [nxt] + [x for x in rest if x != nxt]
        if new == cur:
            continue
        cur = new
        steps.append(cur[:])
    return steps


inp = [34, 89, 12, 57, 76, 41]
st = desc_machine(inp)
ans = st[2][-3]
mcq(IOT, "Number rearrangement", "Basic",
    "A number arrangement machine rearranges numbers step by step. In each step it takes the largest number among "
    "those not yet arranged and moves it to the immediate right of the numbers already arranged (in Step I, to the "
    "extreme left). The other numbers keep their order.\n\nInput: " + " ".join(map(str, inp)) +
    "\n\nWhich number is 3rd from the right end in Step III?", str(ans), ["41", "57", "12"],
    "Simulating a descending-order machine",
    f"Step I: {' '.join(map(str, st[0]))}; Step II: {' '.join(map(str, st[1]))}; Step III: "
    f"{' '.join(map(str, st[2]))}. The 3rd from the right in Step III is {ans}.",
    [f"Step {['I', 'II', 'III', 'IV', 'V', 'VI'][i]}: " + " ".join(map(str, s_)) for i, s_ in enumerate(st[:3])],
    seconds=45, verified_by=RECOMP)


def mixed_machine(items):
    """Step k: the smallest unarranged number goes to the extreme left; the alphabetically first unarranged word goes
    to the extreme right. Returns the list of steps."""
    cur, steps, done_n, done_w = list(items), [], [], []
    while True:
        nums = [x for x in cur if x.isdigit() and x not in done_n]
        wrds = [x for x in cur if not x.isdigit() and x not in done_w]
        if not nums and not wrds:
            break
        n_ = min(nums, key=int) if nums else None
        w_ = min(wrds) if wrds else None
        cur = [x for x in cur if x not in (n_, w_)]
        if n_:
            cur = [n_] + cur
            done_n.append(n_)
        if w_:
            cur = cur + [w_]
            done_w.append(w_)
        steps.append(cur[:])
    return steps


ILL = "train 46 ruby 13 echo 71 nest 28".split()
ill = mixed_machine(ILL)
roman = ["I", "II", "III", "IV", "V", "VI"]
INP = "lamp 52 opal 17 gate 64 kite 39 brick 85".split()
st = mixed_machine(INP)
assert len(st) == 5
sid = stimulus("input_output", "Machine: smallest number left, first word right",
               "A word and number arrangement machine, given an input line of words and numbers, rearranges it "
               "step by step. In each step, the smallest number not yet arranged is moved to the extreme left of "
               "the line, and the word that comes first in alphabetical order among the words not yet arranged is "
               "moved to the extreme right of the line. All other elements keep their order. The process stops when "
               "every element has been arranged.\n\nIllustration:\nInput: " + " ".join(ILL) + "\n" +
               "\n".join(f"Step {roman[i]}: " + " ".join(s_) for i, s_ in enumerate(ill)) +
               f"\n(Step {roman[len(ill) - 1]} is the last step.)\n\nInput for the questions: " + " ".join(INP),
               None,
               "Steps for the given input:\n\n" + "\n".join(f"Step {roman[i]}: " + " ".join(s_)
                                                            for i, s_ in enumerate(st)))
puzzle_io = lambda text, correct, wrongs, expl, steps_, **kw: mcq(
    IOT, "Mixed machine", "Intermediate", text, correct, wrongs, "Simulating a two-rule machine step by step", expl,
    steps_, stimulus=sid, verified_by=RECOMP, **kw)
ALLST = [f"Step {roman[i]}: " + " ".join(s_) for i, s_ in enumerate(st)]
puzzle_io("How many steps are needed to complete the arrangement of the given input?", f"{len(st)}",
          ["4", "6", "7"], f"There are five numbers and five words, and each step arranges one of each, so "
          f"{len(st)} steps are needed (Step V is the last).", ALLST, natural=int, seconds=60)
e = st[1]
ans = e[e.index("kite") + 3] if e.index("kite") + 3 < len(e) else None
puzzle_io("In Step II, which element is 3rd to the right of 'kite'?", ans,
          [x for x in ["opal", "gate", "64", "lamp"] if x != ans][:3],
          f"Step II is '{' '.join(e)}'. Counting three places to the right of 'kite' gives '{ans}'.",
          ALLST[:2], seconds=55)
last = st[-1]
ans = last[4] + " and " + last[5]
puzzle_io("In the last step, which two elements are 5th and 6th from the left end?", ans,
          ["39 and gate", "52 and kite", "17 and gate"],
          f"The last step is '{' '.join(last)}'. Its 5th and 6th elements are {last[4]} and {last[5]}.",
          [ALLST[-1]], seconds=50)


def adv_word_machine(words):
    """Each step: among unarranged words, the longest (ties: alphabetically first) moves to the right end of the
    arranged block at the left; its first letter is replaced by the next letter of the alphabet."""
    cur = list(words)
    steps = []
    arranged = 0
    pool = list(words)
    while pool:
        w_ = sorted(pool, key=lambda x: (-len(x), x))[0]
        pool.remove(w_)
        nw_ = AL[(pos(w_[0].upper())) % 26].lower() + w_[1:]
        idx = cur.index(w_, arranged)
        cur = cur[:arranged] + [nw_] + cur[arranged:idx] + cur[idx + 1:]
        arranged += 1
        steps.append(cur[:])
    return steps


INP = "mint orbit cask fern quilt pasture".split()
st = adv_word_machine(INP)
ans = st[3][4]
mcq(IOT, "Word rearrangement", "Advanced",
    "A machine rearranges words step by step. In each step it takes, among the words not yet arranged, the word with "
    "the most letters (if two words are equally long, the one that comes first in alphabetical order), changes its "
    "first letter to the next letter of the alphabet, and places it immediately to the right of the words already "
    "arranged (in Step I, at the extreme left). The other words keep their order.\n\nInput: " + " ".join(INP) +
    "\n\nWhich word will be 5th from the left end in Step IV?", ans, ["quilt", "fern", "nint"],
    "Selection by length, with a transformation",
    "Order of selection: pasture (7), orbit (5), quilt (5), cask (4), fern (4), mint (4) — ties broken "
    f"alphabetically. Step IV is '{' '.join(st[3])}', whose 5th word is {ans}.",
    [f"Step {roman[i]}: " + " ".join(s_) for i, s_ in enumerate(st)],
    why_others_wrong="quilt has already become 'ruilt' and moved left by Step III; 'nint' is mint after it is "
                     "picked, which happens only in Step VI.", seconds=90, verified_by=RECOMP)
assert st[3] == ["qasture", "prbit", "ruilt", "dask", "mint", "fern"] and ans == "mint"


def adv_num_machine(nums):
    """Each step: the largest unarranged number goes to the left block with its digits reversed; the smallest
    unarranged number goes to the right block with 5 added."""
    left, right, pool = [], [], list(nums)
    steps = []
    while pool:
        big = max(pool)
        pool.remove(big)
        left.append(int(str(big)[::-1]))
        if pool:
            small = min(pool)
            pool.remove(small)
            right.insert(0, small + 5)
        steps.append(left + [x for x in nums if x in pool] + right)
    return steps


INP = [47, 81, 26, 93, 58, 34]
st = adv_num_machine(INP)
ans = st[1][0] + st[1][-1]
mcq(IOT, "Number rearrangement", "Advanced",
    "A machine rearranges numbers step by step. In each step it takes the largest number not yet arranged, reverses "
    "its digits and places it immediately to the right of the numbers already placed at the left end (in Step I, at "
    "the extreme left). In the same step it takes the smallest number not yet arranged, adds 5 to it and places it "
    "immediately to the left of the numbers already placed at the right end (in Step I, at the extreme right). The "
    "remaining numbers keep their order in the middle.\n\nInput: " + " ".join(map(str, INP)) +
    "\n\nWhat is the sum of the two numbers at the extreme ends in Step II?", str(ans), ["78", "57", "49"],
    "Two transformations per step",
    f"Step I: {' '.join(map(str, st[0]))}. Step II: {' '.join(map(str, st[1]))}. Ends of Step II: {st[1][0]} and "
    f"{st[1][-1]}; sum = {ans}.",
    [f"Step {roman[i]}: " + " ".join(map(str, s_)) for i, s_ in enumerate(st)],
    shortcut="The left end never changes after Step I (39 from 93), and in Step II the right end is the second "
             "smallest number + 5 placed to the left of 31, so the extreme right stays 31.",
    natural=int, seconds=80, verified_by=RECOMP)

# ================================================================================================ DATA SUFFICIENCY
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


def ds2_q(diff, question, st1, st2, models, f1, f2, answer, expected, drop, explanation, steps, seconds=50):
    got = ds2(models, f1, f2, answer)
    assert got == expected, (question, got)
    keys = [k for k in "ABENT" if k != drop]
    assert expected in keys and len(keys) == 4
    opts = [DS2[k] for k in keys]
    return fixed(DSF, "Two-statement", diff, DS_HEAD + f"Question: {question}\n\nI. {st1}\nII. {st2}", opts,
                 DS2[expected], "Data sufficiency: test each statement alone, then together", explanation, steps,
                 seconds=seconds, verified_by=("script:enumerate-models", "ai:author-solve"))


people = list("PQRST")
models = [dict(zip(people, perm)) for perm in itertools.permutations(range(5))]  # larger = taller
ds2_q("Basic", "Among P, Q, R, S and T, each of a different height, who is the tallest?",
      "S is taller than P, and P is taller than both Q and R.", "T is shorter than Q.", models,
      lambda m: m["S"] > m["P"] > m["Q"] and m["P"] > m["R"], lambda m: m["T"] < m["Q"],
      lambda m: max(people, key=m.get), "T", "E",
      "I alone leaves T unplaced, so S or T could be the tallest. II alone says nothing about P, R or S. Together, T "
      "is below Q, which is below P and S, so S is the tallest.",
      ["I: S > P > Q, P > R; T unknown → tallest is S or T: not sufficient",
       "II: T < Q only: not sufficient", "I + II: S > P > Q > T and P > R → S is tallest: sufficient",
       "Both statements together are necessary"], seconds=45)
pts_models = [{"N": (0, 0), "M": (mx, my), "P": (px, py)} for mx in range(-4, 5) for my in range(-4, 5)
              for px in range(-4, 5) for py in range(-4, 5) if (mx, my) != (0, 0)]
ds2_q("Basic", "In which direction is village M with respect to village N?",
      "Village M is 4 km east of village P, and village P is 4 km south of village N.",
      "Village N is to the north-west of village M.", pts_models,
      lambda m: m["M"] == (m["P"][0] + 4, m["P"][1]) and m["P"] == (0, -4),
      lambda m: compass(-m["M"][0], -m["M"][1]) == "North-West",
      lambda m: compass(*m["M"]), "E", "N",
      "From I, M is 4 km east and 4 km south of N, i.e. south-east. From II, if N is north-west of M then M is "
      "south-east of N. Each statement alone answers the question.",
      ["I: N (0, 0) → P (0, −4) → M (4, −4): M is South-East of N: sufficient",
       "II: N is North-West of M ⇒ M is South-East of N: sufficient", "Either statement alone is sufficient"],
      seconds=40)
six = list("ABCDEF")
models = [dict(zip(six, perm)) for perm in itertools.permutations(range(1, 7))]
ds2_q("Intermediate", "Six persons A, B, C, D, E and F sit in a row facing north. Who sits at the extreme right "
      "end?", "C sits third from the left end, and exactly two persons sit between C and E.",
      "B sits immediately to the left of E, and F sits at the extreme left end.", models,
      lambda m: m["C"] == 3 and abs(m["C"] - m["E"]) == 3, lambda m: m["B"] == m["E"] - 1 and m["F"] == 1,
      lambda m: next(p for p in six if m[p] == 6), "A", "N",
      "From I, C is at seat 3 and E, three seats away, must be at seat 6 (seat 0 does not exist): E is at the right "
      "end. II fixes only F and the B–E pair, which can sit in several places.",
      ["I: C = 3; E = 3 ± 3 → E = 6 ⇒ E sits at the extreme right: sufficient",
       "II: F = 1; B–E adjacent anywhere from seats 2–3 to 5–6: not sufficient", "I alone is sufficient"],
      seconds=50)
dsents1 = [(["gold", "rate", "rise"], ["tu", "ka", "pa"]), (["rate", "cut", "now"], ["ka", "zi", "me"])]
dsents2 = [(["gold", "coin", "rise"], ["pa", "ro", "tu"]), (["coin", "now", "sale"], ["ro", "me", "lo"])]
r1 = sentence_solve(dsents1, "gold")
r2 = sentence_solve(dsents2, "gold")
r12 = sentence_solve(dsents1 + dsents2, "gold")
assert (len(r1), len(r2), len(r12)) == (2, 2, 2)
fixed(DSF, "Two-statement", "Intermediate",
      DS_HEAD + "Question: In a certain code language, what is the code for 'gold'?\n\n"
      "I. 'gold rate rise' is written as 'tu ka pa', and 'rate cut now' is written as 'ka zi me'.\n"
      "II. 'gold coin rise' is written as 'pa ro tu', and 'coin now sale' is written as 'ro me lo'.",
      [DS2[k] for k in "AENT"], DS2["N"], "Data sufficiency with sentence coding",
      "In every statement, and even when both are combined, 'gold' and 'rise' always appear together and share the "
      "codes 'tu' and 'pa'. Nothing separates them, so the code for 'gold' cannot be fixed.",
      ["I: gold and rise ↔ {tu, pa} (rate = ka): not sufficient", "II: gold and rise ↔ {pa, tu} (coin = ro): not "
       "sufficient", "I + II: gold and rise still appear only together with {tu, pa}: not sufficient",
       "Even together the statements are not sufficient"], seconds=55,
      verified_by=("script:enumerate-models", "ai:author-solve"))
DAYS7 = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
models = [{"mohan": a, "bro": b} for a in range(7) for b in range(7) if a != b]
ds2_q("Intermediate", "On which day of the week did Mohan visit the bank?",
      "Mohan did not visit the bank on a Saturday or a Sunday, and he visited after Wednesday.",
      "Mohan visited the bank on the day after his brother did, and his brother visited after Tuesday but before "
      "Thursday.", models, lambda m: m["mohan"] < 5 and m["mohan"] > 2,
      lambda m: m["mohan"] == m["bro"] + 1 and 1 < m["bro"] < 3, lambda m: m["mohan"], "B", "T",
      "I leaves Thursday and Friday open. From II, the brother visited on Wednesday, so Mohan visited on Thursday.",
      ["I: after Wednesday and not on a weekend → Thursday or Friday: not sufficient",
       "II: brother on Wednesday (after Tuesday, before Thursday) → Mohan on Thursday: sufficient",
       "II alone is sufficient"], seconds=45)

# ---- Advanced: three statements
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


DS3_HEAD = ("The question below is followed by three statements, I, II and III. Decide which of the statements are "
            "sufficient to answer the question.\n\n")
people = list("PQRST")
models = [dict(zip(people, perm)) for perm in itertools.permutations(range(5))]  # larger = older
fns = [lambda m: m["P"] > m["Q"] and m["P"] > m["R"], lambda m: m["S"] > m["P"], lambda m: m["T"] < m["Q"]]
got = ds3(models, fns, lambda m: max(people, key=m.get))
assert got == "ALL"
keys = ["I+II", "I+III", "ALL", "NONE"]
fixed(DSF, "Three-statement", "Advanced",
      DS3_HEAD + "Question: Among P, Q, R, S and T, each of a different age, who is the oldest?\n\nI. P is older than "
      "both Q and R.\nII. S is older than P.\nIII. T is younger than Q.", [DS3[k] for k in keys], DS3["ALL"],
      "Three-statement data sufficiency: test every pair before using all three",
      "No single statement or pair is enough: I + II leaves T unplaced; I + III leaves S unplaced; II + III leaves Q "
      "and R free. With all three, S > P > Q > T and P > R, so S is the oldest.",
      ["Any single statement: clearly insufficient", "I + II: S > P > Q, R; T could be older than S: not sufficient",
       "I + III: P > Q > T, P > R; S unknown: not sufficient", "II + III: S > P, Q > T; Q or R could be oldest: not "
       "sufficient", "I + II + III: S > P > Q > T and P > R ⇒ S oldest: all three are necessary"],
      seconds=75, verified_by=("script:enumerate-models", "ai:author-solve"))
six = list("ABCDEF")
models = []
for perm in itertools.permutations(range(1, 6)):
    m = dict(zip(six[1:], perm))
    m["A"] = 0
    models.append(m)
rt6 = lambda s_, k: (s_ + k) % 6  # all face the centre: right = anticlockwise = +1
nb6 = lambda a, b: (a - b) % 6 in (1, 5)
fns = [lambda m: m["C"] == rt6(m["A"], -2), lambda m: nb6(m["D"], m["C"]) and nb6(m["D"], m["F"]),
       lambda m: m["B"] == rt6(m["A"], 1)]
got = ds3(models, fns, lambda m: next(p for p in six if m[p] == 3))
assert got == "I+II"
keys = ["I+II", "II+III", "ALL", "ANY2"]
fixed(DSF, "Three-statement", "Advanced",
      DS3_HEAD + "Question: Six friends A, B, C, D, E and F sit around a circular table, equally spaced and facing "
      "the centre. Who sits opposite A?\n\nI. C sits second to the left of A.\nII. D is an immediate neighbour of "
      "both C and F.\nIII. B sits immediately to the right of A.", [DS3[k] for k in keys], DS3["I+II"],
      "Three-statement data sufficiency with a circular arrangement",
      "With I, C is two seats to A's left, which is next to the seat opposite A. II then needs D between C and F: D "
      "cannot sit on the side towards A (F would have to take A's seat), so D sits opposite A. So I and II together "
      "answer the question. III only places B next to A and does not complete any other combination.",
      ["Number the seats 0–5 to A's right (A = 0, opposite A = 3)", "I: C = 4. II alone: no fixed seat. III: B = 1",
       "I + II: D beside C → seat 3 or 5; D = 5 would need F at seat 0 (A's seat), so D = 3: sufficient",
       "I + III: C = 4, B = 1; seats 2, 3, 5 open for D, E, F: not sufficient",
       "II + III: B = 1 and a C–D–F block elsewhere: not sufficient", "Only I and II together are sufficient"],
      seconds=75, verified_by=("script:enumerate-models", "ai:author-solve"))

# ================================================================================================ VERBAL REASONING
# Hand-written items: each was solved by the author and re-checked independently against the standard rules
# (an assumption is what the statement maker must take for granted; a conclusion must follow from the statement
# alone; extreme or unrelated options fail).
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


asm("Basic", "A bank has announced that customers who register their mobile numbers with their accounts before 31 "
    "March will receive a free cheque book.",
    "Some customers would like a free cheque book enough to register their mobile numbers for it.",
    "All customers of the bank have already registered their mobile numbers.", A_I,
    "An incentive is offered only if the bank believes it will motivate at least some customers, so I is implicit. "
    "II contradicts the very purpose of the offer: if everyone had already registered, no incentive would be needed.",
    ["I: the offer makes sense only if a free cheque book attracts some customers: implicit",
     "II: if all had registered, the offer would be pointless: not implicit"],
    "Both or II fail because II goes against the reason for the announcement.", seconds=35)
asm("Basic", "Notice in a bank branch: \"Please collect a token from the token machine to avoid waiting in a long "
    "queue.\"", "Using the token machine reduces the time customers spend waiting in a queue.",
    "Customers visiting the branch can read and act on the notice.", A_B,
    "The notice promises less waiting through tokens, so I is assumed. Any written notice assumes its readers can "
    "read and follow it, so II is also assumed.",
    ["I: the notice links tokens with avoiding a long queue: implicit",
     "II: a notice is put up only if people are expected to read and act on it: implicit"],
    "Only I or Only II ignores one of the two things the notice takes for granted.", seconds=35)
asm("Intermediate", "The company has decided to shift its head office from Mumbai to Pune from next year.",
    "Pune offers a larger market for the company's products than Mumbai.",
    "All the employees working at the head office will move to Pune with it.", A_N,
    "A head office can move for many reasons, such as lower rent or better talent, so a bigger market in Pune is not "
    "taken for granted. The decision also does not depend on every employee moving; some may resign or be "
    "replaced.",
    ["I: the move could be for cost or other reasons; a larger market is not necessary: not implicit",
     "II: the company need not assume 100% of staff will relocate: not implicit"],
    "Only I reads a motive into the decision that the statement never needs.", seconds=45)
asm("Intermediate", "To reduce the cost of handling cash, a bank plans to install cash-recycler machines in its 200 "
    "busiest branches.", "Cash-recycler machines can lower the bank's cost of handling cash.",
    "The 200 busiest branches handle a significant amount of cash.", A_B,
    "The plan is meant to cut cash-handling cost, so the bank assumes the machines can do that (I). It picks the "
    "busiest branches because that is where enough cash is handled for the saving to matter (II).",
    ["I: the stated goal is cost reduction through the machines: implicit",
     "II: choosing the busiest branches for a cash-cost measure assumes they handle a lot of cash: implicit"],
    "Only I misses the reason for choosing these particular branches.", seconds=50)
asm("Advanced", "The regulator has directed all lenders to display the annualised interest rate, including all "
    "fees, prominently in every loan advertisement.",
    "Borrowers can compare loan offers better when the full annualised cost is shown prominently.",
    "Lenders have so far been charging interest above the legal limit.", A_I,
    "The directive is about disclosure: it assumes that showing the full cost helps borrowers compare offers (I). It "
    "does not assume that any lender broke an interest-rate limit (II); a disclosure rule would not fix that anyway.",
    ["I: the purpose of mandatory prominent disclosure is better comparison: implicit",
     "II: the directive concerns how costs are shown, not whether rates are illegal: not implicit"],
    "II is a tempting 'reason' for regulation, but the statement neither needs nor implies it.", seconds=55)
asm("Advanced", "\"Since our app now lets customers open a fixed deposit in three minutes, we expect deposits from "
    "young professionals to rise,\" said the bank's digital head.",
    "Young professionals have avoided opening fixed deposits only because the process was lengthy.",
    "Young professionals value speed and convenience when choosing financial products.", A_II,
    "The expectation rests on young professionals caring about speed and convenience (II). It does not need the "
    "lengthy process to have been the only reason they stayed away; 'only' makes I too strong.",
    ["II: expecting more deposits from a faster process assumes the target group values speed: implicit",
     "I: the speaker needs speed to be one factor, not the sole factor: 'only' makes it not implicit"],
    "Both fails because of the word 'only' in I.", seconds=55)

# ---- Statement and conclusions
SCN = "Statement and Conclusions"
SC_HEAD = ("Read the statement and the two conclusions. Assume everything in the statement to be true, and decide "
           "which conclusion(s) logically follow from it.\n\n")


def scq(diff, sub, statement, c1, c2, answer, explanation, steps, why, seconds=45):
    return fixed(SCN, sub, diff, SC_HEAD + f"Statement: {statement}\n\nConclusions:\nI. {c1}\nII. {c2}", OPT4, answer,
                 "A conclusion must follow from the statement alone", explanation, steps, why_others_wrong=why,
                 seconds=seconds, verified_by=HAND)


scq("Basic", "Valid conclusions", "All candidates who score at least 60% in the written test will be called for the "
    "interview. Rahul scored 72% in the written test.", "Rahul will be called for the interview.",
    "Rahul will be selected for the job.", ONLY_I,
    "Rahul meets the stated condition (72% ≥ 60%), so he will be called (I follows). Being called for an interview "
    "does not mean being selected (II does not follow).",
    ["Rule: score ≥ 60% ⇒ interview call", "Rahul 72% ⇒ interview call: I follows",
     "Selection depends on the interview, about which nothing is said: II does not follow"],
    "Both treats an interview call as selection.", seconds=35)
scq("Basic", "Valid conclusions", "Every savings account in Bank X earns 3% interest a year, and every fixed deposit "
    "in Bank X earns at least 6% a year.",
    "A fixed deposit in Bank X earns more interest in a year than a savings account in Bank X with the same amount.",
    "No fixed deposit in Bank X earns less than 6% a year.", BOTH,
    "For equal amounts, a rate of at least 6% always beats 3%, so I follows. II simply restates 'at least 6%', so "
    "it follows too.",
    ["I: FD rate ≥ 6% > 3% savings rate ⇒ more interest on the same amount: follows",
     "II: 'at least 6%' = 'never less than 6%': follows"],
    "Only II overlooks that equal amounts make the rate comparison decisive.", seconds=35)
scq("Intermediate", "Inferences", "The number of digital payment transactions in the country doubled last year, "
    "while the number of ATM cash withdrawals fell by 5%.", "People in the country have stopped using cash.",
    "The number of digital payment transactions will double again this year.", NEITHER,
    "ATM withdrawals fell by only 5%, so cash is clearly still used (I fails). Last year's growth says nothing "
    "certain about this year's (II is a prediction, not a conclusion).",
    ["I: a 5% fall in withdrawals means cash use continues: does not follow",
     "II: a future growth rate cannot be concluded from one past year: does not follow"],
    "Only I exaggerates a small fall into a complete stop.", seconds=45)
scq("Intermediate", "Inferences", "A survey of 2,000 small shop owners in five cities found that 64% of them accept "
    "payments through QR codes.",
    "Among the shop owners surveyed, those who accept QR-code payments outnumber those who do not.",
    "64% of all small shop owners in the country accept QR-code payments.", ONLY_I,
    "64% of the surveyed owners accept QR payments and 36% do not, so I follows. The survey covered five cities "
    "only; the figure cannot be extended to the whole country (II fails).",
    ["I: 64% versus 36% within the sample: follows",
     "II: a five-city sample does not establish a national percentage: does not follow"],
    "Both generalises a sample to the whole population.", seconds=45)
scq("Advanced", "Valid conclusions", "The state's tax collections in the first half of the year were higher than "
    "budgeted. Citing this, the state government has announced that it will meet this year's fiscal deficit target "
    "without cutting capital expenditure.",
    "The state government does not plan to cut capital expenditure in order to meet this year's fiscal deficit target.",
    "The state's tax collections for the full year will be higher than budgeted.", ONLY_I,
    "I restates the announced plan, so it follows. The statement covers only the first half of the year; the "
    "full-year collections may still fall short, so II does not follow.",
    ["I: 'without cutting capital expenditure' is the announced plan: follows",
     "II: first-half collections do not fix full-year collections: does not follow"],
    "Both extends a half-year fact to the whole year.", seconds=50)
scq("Advanced", "Valid conclusions", "In a city, every bank branch that opened after 2020 has a solar rooftop. None of "
    "the branches of Bank Y in the city has a solar rooftop.", "Bank Y has no branches in the city.",
    "No branch of Bank Y in the city opened after 2020.", ONLY_II,
    "If any Bank Y branch had opened after 2020, it would have a solar rooftop, but none does; so none opened after "
    "2020 (II). The statement refers to Bank Y's branches in the city, so it does not say they do not exist (I "
    "fails).",
    ["Rule: opened after 2020 ⇒ solar rooftop", "Bank Y branches: no solar rooftop ⇒ not opened after 2020 "
     "(contrapositive): II follows", "I is not implied: the statement speaks of Bank Y's branches in the city and "
     "gives no reason to think there are none: does not follow"],
    "Only I misreads 'none of the branches has a rooftop' as 'there are no branches'.", seconds=55)

# ---- Cause and effect
CAE = "Cause and Effect"
CE = {"A": "Statement I is the cause and statement II is its effect",
      "B": "Statement II is the cause and statement I is its effect",
      "C": "Both the statements I and II are independent causes",
      "D": "Both the statements I and II are effects of independent causes",
      "E": "Both the statements I and II are effects of some common cause"}
CE_HEAD = ("Below are two statements, I and II. They may be independent causes, effects of independent causes or of "
           "a common cause, or one may be the effect of the other. Decide the relationship.\n\n")


def ceq(diff, sub, s1, s2, answer, drop, explanation, steps, why, seconds=45):
    keys = [k for k in "ABCDE" if k != drop]
    return fixed(CAE, sub, diff, CE_HEAD + f"I. {s1}\nII. {s2}", [CE[k] for k in keys], CE[answer],
                 "Cause and effect: look for a direct link, a shared trigger, or none", explanation, steps,
                 why_others_wrong=why, seconds=seconds, verified_by=HAND)


ceq("Basic", "Independent causes", "Heavy unseasonal rain damaged the standing wheat crop in several districts of the "
    "state last week.", "Wheat prices in the wholesale markets of the state rose sharply this week.", "A", "C",
    "Crop damage reduces the expected supply of wheat, which pushes wholesale prices up. I came first and explains "
    "II, so I is the cause and II its effect.",
    ["I (crop damage) happened before II (price rise)", "Lower supply → higher prices: I explains II",
     "So I is the cause and II the effect"],
    "II cannot cause I: a price rise does not damage crops.", seconds=35)
ceq("Intermediate", "Common cause", "Most IT firms in the city asked their employees to work from home on Monday.",
    "All schools in the city remained closed on Monday.", "E", "C",
    "Neither event causes the other: offices do not shut schools, and school closures do not make firms switch to "
    "work from home. Both are typical responses to one trigger, such as a severe weather warning or a city-wide "
    "shutdown on that day. So both are effects of a common cause.",
    ["No direct link between I and II in either direction",
     "Both are same-day precautionary measures of the kind taken after a single city-wide trigger",
     "So both are effects of some common cause"],
    "Effects of independent causes would fit only if the two closures had unrelated triggers, which the identical "
    "timing and scope make unlikely.", seconds=50)
ceq("Intermediate", "Independent causes", "The bank has extended its branch working hours to 7 pm on weekdays.",
    "A survey by the bank showed that most of its salaried customers could not visit a branch before 5 pm.", "B", "C",
    "The survey finding (II) explains the decision to keep branches open later (I). II is the cause and I its "
    "effect.", ["II reports a problem: customers cannot come before 5 pm",
                "I is the bank's response: longer hours", "So II is the cause and I the effect"],
    "I cannot cause II: extending hours does not create the survey finding.", seconds=45)
ceq("Advanced", "Independent causes", "The central bank kept its policy interest rate unchanged at its latest "
    "meeting.", "Sales of air-conditioners rose sharply in the northern states this month.", "D", "C",
    "Each statement is an outcome: the rate decision follows from the central bank's view of inflation and growth, "
    "and the jump in air-conditioner sales from hot weather and seasonal demand. Neither explains the other, and no "
    "single event explains both. So they are effects of independent causes.",
    ["I is a decision (an effect of the monetary-policy assessment)",
     "II is a market outcome (an effect of seasonal heat and demand)",
     "No link between them and no shared trigger: effects of independent causes"],
    "A common cause would need one event driving both a policy decision and a seasonal sales rise; nothing points "
    "to one.", seconds=55)

# ---- Critical reasoning
CRT = "Critical Reasoning"


def crq(diff, sub, text, correct, wrongs, concept, explanation, steps, why, seconds=60):
    return mcq(CRT, sub, diff, text, correct, wrongs, concept, explanation, steps, why_others_wrong=why,
               seconds=seconds, verified_by=HAND)


crq("Basic", "Course of action", "Statement: Several customers of a bank branch have complained that its ATM often "
    "runs out of cash on weekends.\n\nWhich of the following is the most appropriate course of action for the bank?",
    "Schedule an additional cash refill for the ATM before every weekend",
    ["Shut down the ATM on weekends so that customers stop complaining",
     "Fine customers who withdraw cash from the ATM on weekends",
     "Transfer the branch manager to another branch immediately"],
    "A course of action should solve the stated problem practically",
    "The problem is a cash shortage on weekends; an extra refill before weekends removes it directly.",
    ["Identify the problem: the ATM runs dry on weekends", "Choose the action that fixes the cause: more cash "
     "before the weekend"],
    "Shutting the ATM or fining customers punishes users instead of solving the problem; transferring the manager "
    "does not put cash in the machine.", seconds=35)
crq("Basic", "Inference from a passage", "In a town, the number of two-wheeler loans sanctioned by banks in October "
    "was 30% higher than in September, while the number of two-wheeler loan applications was only 10% higher.\n\n"
    "Which of the following can be inferred from this information?",
    "A larger share of the applications was sanctioned in October than in September",
    ["Banks lowered their interest rates on two-wheeler loans in October",
     "Every application received in October was sanctioned",
     "More two-wheelers were sold in October than in any other month of the year"],
    "Inference must follow from the numbers given",
    "If sanctions grew by 30% and applications by only 10%, the ratio sanctions ÷ applications rose (1.3 ÷ 1.1 > 1). "
    "So a larger share of applications was approved in October.",
    ["Sanction ratio in October = 1.30 S ÷ 1.10 A = 1.18 × (S ÷ A)", "So the approval share rose by about 18%",
     "No other option is supported by the data"],
    "Interest rates and sales across the year are not mentioned; 'every application' is far stronger than the data.",
    seconds=45)
crq("Basic", "Strengthen and weaken", "A coaching institute claims that its students do better in the bank PO exam "
    "than other candidates because of its weekly mock tests.\n\nWhich of the following, if true, most weakens the "
    "institute's claim?",
    "The institute admits only students who have already scored highly in its own screening test",
    ["The institute's mock tests follow the latest exam pattern",
     "Some students of other institutes also clear the PO exam",
     "The institute has branches in ten cities"],
    "Weakening a causal claim: find another explanation for the result",
    "If the institute admits only students who were already strong, their better results may come from that "
    "selection rather than from the mock tests, which undercuts the claimed cause.",
    ["Claim: mock tests → better results", "A weakener offers another cause for the better results",
     "Pre-selecting strong students is such an alternative cause"],
    "Following the latest pattern supports the claim; other institutes' successes and the number of branches do not "
    "touch the cause of this institute's results.", seconds=45)
crq("Intermediate", "Strengthen and weaken", "Argument: The city should build a flyover at the Station Road junction, "
    "because it will reduce the time commuters spend waiting in traffic there.\n\nWhich of the following, if true, "
    "most strengthens the argument?",
    "A traffic study found that most vehicles at the junction go straight through it, which is the movement a "
    "flyover would carry",
    ["The flyover will take three years to build",
     "The city has already built two flyovers elsewhere",
     "Some shopkeepers near the junction oppose the flyover"],
    "Strengthening: show that the proposed means will produce the claimed effect",
    "A flyover only saves time for traffic that uses it. If most vehicles go straight through the junction, most of "
    "the traffic will bypass the signal, so waiting time falls: this supports the argument.",
    ["Claim: flyover → less waiting at the junction", "The claim depends on enough traffic using the flyover",
     "Most vehicles going straight confirms that dependence"],
    "Construction time and shopkeepers' views concern cost or opinion, not the time saved; flyovers elsewhere say "
    "nothing about this junction.", seconds=55)
crq("Intermediate", "Inference from a passage", "A bank's net profit equals its interest income plus other income, "
    "minus operating expenses, provisions for bad loans and tax. This year, Bank A's net profit rose by 20%, although "
    "its interest income, operating expenses and tax paid were all exactly the same as last year.\n\nWhich of the "
    "following must be true?",
    "Bank A's other income rose, or its provisions for bad loans fell, or both",
    ["Bank A gave out more loans this year than last year",
     "Bank A's provisions for bad loans fell this year",
     "Bank A's share price rose by 20% this year"],
    "Must-be-true inference from a definition",
    "Profit rose while interest income, expenses and tax were unchanged. The only remaining items in the definition "
    "are other income (added) and provisions (subtracted), so at least one of them must have moved in profit's "
    "favour. Either alone could explain the rise, so only the combined statement must be true.",
    ["Profit = interest income + other income − expenses − provisions − tax",
     "Unchanged: interest income, expenses, tax", "So other income rose and/or provisions fell"],
    "'Provisions fell' alone need not be true (other income could explain it); more loans would change interest "
    "income, which was unchanged; the share price is not linked to the definition.", seconds=60)
crq("Intermediate", "Course of action", "Statement: Many farmers in a district missed the deadline to enrol in the "
    "crop insurance scheme this season because they did not know about it.\n\nWhich of the following is the most "
    "appropriate course of action?",
    "Publicise the next enrolment deadline well in advance through village panchayats, SMS alerts and local banks",
    ["Discontinue the crop insurance scheme in the district",
     "Impose a penalty on farmers who miss the enrolment deadline",
     "Remove the enrolment deadline so that no date is ever announced"],
    "Course of action: address the cause, not the symptom",
    "The cause was lack of awareness, so spreading information through channels farmers use fixes it directly.",
    ["Cause: farmers were unaware of the deadline", "Remedy: inform them in time through reachable channels"],
    "Scrapping the scheme or penalising farmers harms the people it is meant to help; removing the deadline does not "
    "make farmers aware and makes the scheme unworkable.", seconds=45)
crq("Intermediate", "Strengthen and weaken", "Argument: Since the bank started charging a fee on branch cash deposits "
    "above ₹50,000, such deposits at its branches have fallen by 25%. So the fee has succeeded in moving customers to "
    "digital channels.\n\nWhich of the following, if true, most weakens the argument?",
    "Over the same period the bank's digital transactions did not increase, while many large depositors moved their "
    "accounts to a competing bank that charges no such fee",
    ["The fee was announced to all customers by SMS",
     "Digital transactions are cheaper for the bank to process than branch deposits",
     "The fee applies only to cash deposits above ₹50,000"],
    "Weakening: show the effect came from a different cause",
    "The argument assumes the fall in branch deposits means customers went digital. If digital use did not grow and "
    "depositors simply left for another bank, the fee drove customers away rather than towards digital channels.",
    ["Conclusion: fee → shift to digital", "Assumption: the missing deposits went to digital channels",
     "Evidence that they went to a competitor instead breaks the assumption"],
    "How the fee was announced, why digital is cheaper, and the fee threshold do not show where the deposits went.",
    seconds=60)
crq("Advanced", "Inference from a passage", "Passage: When a lender's cost of funds falls, it can cut its lending "
    "rates without hurting its margin. Over the last two quarters, the cost of funds of most small finance banks has "
    "fallen, yet their average lending rates have remained unchanged. In the same period, the share of their loans "
    "that turned bad has risen.\n\nWhich of the following can most reasonably be inferred from the passage?",
    "For most small finance banks, the gap between average lending rates and the cost of funds has widened over the "
    "two quarters",
    ["Small finance banks kept lending rates high on purpose to cover their rising bad loans",
     "Small finance banks will cut their lending rates in the next quarter",
     "Borrowers of small finance banks do not know that the banks' cost of funds has fallen"],
    "Inference: what the facts given directly imply",
    "Lending rates stayed the same while the cost of funds fell, so the difference between the two (the margin on "
    "lending) grew. This follows from the facts alone.",
    ["Margin on lending ≈ lending rate − cost of funds", "Lending rate unchanged, cost of funds down ⇒ margin up",
     "The other options add motives, predictions or knowledge not in the passage"],
    "The bad-loan motive is a plausible story but is not stated or implied; the next-quarter cut is a prediction; "
    "borrowers' awareness is never discussed.", seconds=75)
crq("Advanced", "Strengthen and weaken", "Argument: A state government says that waiving stamp duty on home "
    "purchases by first-time buyers will significantly increase home ownership among young families in the "
    "state.\n\nWhich of the following, if true, most seriously weakens the argument?",
    "Surveys show that the main obstacle for young families is the down payment, which is many times larger than "
    "the stamp duty that would be saved",
    ["Stamp duty is an important source of revenue for the state government",
     "Most first-time home buyers in the state are young families",
     "Several other states have also reduced stamp duty in the past"],
    "Weakening: show that the proposed means does not remove the real obstacle",
    "If the real barrier is the down payment, a stamp-duty waiver is too small to change young families' decisions, "
    "so home ownership will not rise significantly.",
    ["Claim: stamp-duty waiver → more home ownership among young families",
     "The claim assumes stamp duty is a significant barrier", "Evidence that the down payment is the main barrier "
     "(and far larger) attacks that assumption"],
    "Revenue loss is a cost argument, not about effectiveness; 'most buyers are young families' supports the "
    "argument; other states' actions say nothing about their results.", seconds=75)
crq("Advanced", "Course of action", "Statement: An internal audit found that several branches of a bank sanctioned "
    "loans without verifying the borrowers' income documents, and many of these loans have turned bad.\n\n"
    "Courses of action:\nI. The bank should make document verification a mandatory step in its loan software, so that "
    "a loan cannot be sanctioned without it.\nII. The bank should stop all lending until the audit is complete.\n"
    "III. The bank should investigate the officials responsible and try to recover the bad loans.\n\nWhich of the "
    "courses of action logically follow?", "Only I and III follow",
    ["Only I follows", "Only II and III follow", "All I, II and III follow"],
    "Evaluating several courses of action: practical, proportionate, aimed at the problem",
    "I prevents the lapse from recurring and III deals with the damage already done and with accountability. II is "
    "extreme: halting all lending punishes every borrower and branch for a process failure in some.",
    ["I: fixes the root cause (missing verification): follows",
     "II: a blanket stop is disproportionate and harms the business: does not follow",
     "III: addresses accountability and recovery: follows"],
    "Any option containing II fails because a complete lending halt is out of proportion to the problem; 'Only I' "
    "ignores the loans already lost.", seconds=70)

# ================================================================================================ WRITE
plan = json.loads((ROOT / "batches" / "plans" / "BATCH_001_plan.json").read_text(encoding="utf-8"))
splan = next(s_ for s_ in plan["subjects"] if s_["subject"] == RA)
have = Counter((x["topic"], x["difficulty"]) for x in QUESTIONS)
for t in splan["topics"]:
    for d_, n_ in t["quota"].items():
        assert have[(t["topic"], d_)] == n_, (t["topic"], d_, have[(t["topic"], d_)], n_)
    assert all(x["subtopic"] in t["subtopics"] for x in QUESTIONS if x["topic"] == t["topic"]), t["topic"]
assert len(QUESTIONS) == splan["total"] == 200
assert QUESTIONS[-1]["question_id"] == splan["question_ids"][1]
assert STIMULI[0]["stimulus_id"] == splan["stimulus_id_start"]
for st_ in STIMULI:
    n_ = sum(1 for x in QUESTIONS if x.get("stimulus_id") == st_["stimulus_id"])
    assert 3 <= n_ <= 5, (st_["stimulus_id"], n_)

doc = {
    "schema_version": "1.0",
    "batch_id": "BATCH_001",
    "created_at": TODAY,
    "notes": ("Reasoning Ability part of BATCH_001: 200 original questions (60 Basic, 80 Intermediate, 60 Advanced) "
              "built by tools/batch_001/reasoning.py. Puzzles and seating are brute-forced for a unique arrangement; "
              "syllogisms are checked over every Venn-region model; inequalities over all integer assignments; data "
              "sufficiency by enumerating models for each statement subset; blood relations, directions, coding, "
              "series, ranking and input-output are recomputed in code. Verbal-reasoning items (assumptions, "
              "conclusions, cause-effect, critical reasoning) are hand-written and independently re-checked. All "
              "questions await human review."),
    "stimuli": STIMULI,
    "questions": QUESTIONS,
}
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
print(f"wrote {OUT}: {len(QUESTIONS)} questions, {len(STIMULI)} stimuli, keys {dict(sorted(KEYCOUNT.items()))}")
