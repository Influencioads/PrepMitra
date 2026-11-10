"""Builds batches/parts/BATCH_002_REAS.json: the 200 Reasoning Ability questions of BATCH_002.

Same method and helpers as tools/batch_001/reasoning.py, with new puzzle structures and new conditions:
- puzzles and seating: the conditions are written once as (text, variables, test) triples; the text goes into the
  stimulus (or the question) and the test into an exhaustive backtracking search that must return exactly one
  arrangement. Every answer is then read off that arrangement;
- syllogisms: checked over every Venn-region model; inequalities: exhaustive integer assignments;
- blood relations (explicit family tree), directions, coding, series, alphabet, number, ranking and input-output:
  recomputed in code; data sufficiency: each statement subset checked by enumerating models.
Verbal-reasoning items (conclusions, cause-effect, critical reasoning) are hand-written and re-checked.
If any assertion fails, nothing is written.

    python tools/batch_002/reasoning.py        (run from docs/question-bank)
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
OUT = ROOT / "batches" / "parts" / "BATCH_002_REAS.json"
TODAY = "2026-11-05"
RA = "Reasoning Ability"
LETTERS = "ABCD"
FIRST_Q, FIRST_STIM = 205, 2001
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


# ================================================================================================ LINEAR SEATING
LIN = "Linear Seating Arrangement"

# ---- L1 Basic: seven persons, one row, all facing SOUTH (seats 1..7 from west to east; right = west)
P = ["Aman", "Bhoomi", "Chirayu", "Dhara", "Eklavya", "Gunjan", "Hitesh"]
RS_ = lambda p, k: p - k  # k-th to the right of a south-facing person (negative k = to the left)
conds = [
    ("Hitesh sits at one of the extreme ends of the row.", ("Hitesh",), lambda h: h in (1, 7)),
    ("Only two persons sit between Hitesh and Aman.", ("Hitesh", "Aman"), lambda h, a: abs(h - a) == 3),
    ("Gunjan sits immediately to the right of Aman.", ("Gunjan", "Aman"), lambda g, a: g == RS_(a, 1)),
    ("Dhara sits third to the left of Gunjan.", ("Dhara", "Gunjan"), lambda d, g: d == RS_(g, -3)),
    ("Chirayu is an immediate neighbour of Hitesh.", ("Chirayu", "Hitesh"), lambda c, h: abs(c - h) == 1),
    ("Bhoomi sits immediately to the left of Aman.", ("Bhoomi", "Aman"), lambda b, a: b == RS_(a, -1)),
]
L1 = unique(P, {p: range(1, 8) for p in P}, conds, [P])
at = {v: k for k, v in L1.items()}
assert [at[i] for i in range(1, 8)] == ["Hitesh", "Chirayu", "Gunjan", "Aman", "Bhoomi", "Dhara", "Eklavya"]
ARR = "West to east: " + ", ".join(at[i] for i in range(1, 8)) + " (all facing south)"
sid = stimulus("puzzle", "Seven persons in a row facing south",
               "Seven persons Aman, Bhoomi, Chirayu, Dhara, Eklavya, Gunjan and Hitesh sit in a straight row, all "
               "facing south. (For a person facing south, the right is towards the west and the left is towards the "
               "east.)", conds,
               "Hitesh is at an end and Aman is three seats from him. Gunjan is immediately to Aman's right (west) and "
               "Dhara third to Gunjan's left (east), so Dhara is two seats east of Aman. If Hitesh were at the east "
               "end (seat 7 from the west), Aman = 4, Gunjan = 3 and Dhara = 6, and Chirayu, Hitesh's neighbour, would "
               "need seat 6: rejected. So Hitesh is at the west end (seat 1), Aman = 4, Gunjan = 3, Dhara = 6, "
               "Chirayu = 2, Bhoomi (immediately to Aman's left, i.e. east) = 5 and Eklavya = 7.\n\n"
               + table(["Seat (west to east)", "Person"], [(i, at[i]) for i in range(1, 8)]))
ans = at[RS_(L1["Bhoomi"], -2)]
assert ans == "Eklavya" and at[RS_(L1["Bhoomi"], 2)] == "Gunjan"
puzzle_q(sid, LIN, "Single row, facing north/south", "Basic", "Who sits second to the left of Bhoomi?", ans,
         ["Gunjan", "Dhara", "Aman"], "Facing south: the left is towards the east",
         f"Bhoomi sits at seat 5 (from the west) facing south, so her left is towards the east. Second to her left is "
         f"seat 7: {ans}.",
         ["Hitesh at the east end fails (Chirayu would need Dhara's seat), so Hitesh is at the west end", ARR,
          f"Bhoomi = seat 5; left = east; seat 5 + 2 = 7 = {ans}"],
         why_others_wrong="Gunjan is second to Bhoomi's right (counting westwards); Dhara is immediately to her "
                          "left; Aman is immediately to her right.", seconds=50)
gap = abs(L1["Chirayu"] - L1["Dhara"]) - 1
assert gap == 3
puzzle_q(sid, LIN, "Single row, facing north/south", "Basic", "How many persons sit between Chirayu and Dhara?",
         num_word(gap), ["Two", "Four", "One"], "Counting seats between two persons",
         f"Chirayu is at seat {L1['Chirayu']} and Dhara at seat {L1['Dhara']}, so Gunjan, Aman and Bhoomi sit between "
         f"them: {gap}.", [ARR, f"Seats strictly between {L1['Chirayu']} and {L1['Dhara']}: 3, 4, 5"],
         natural=by_num, seconds=45)
stm = [
    ("Aman sits exactly in the middle of the row", L1["Aman"] == 4),
    ("Eklavya sits immediately to the right of Dhara", RS_(L1["Dhara"], 1) == L1["Eklavya"]),
    ("Chirayu sits second to the left of Hitesh", RS_(L1["Hitesh"], -2) == L1["Chirayu"]),
    ("Gunjan is an immediate neighbour of Bhoomi", abs(L1["Gunjan"] - L1["Bhoomi"]) == 1),
]
t, f = one_true(stm)
puzzle_q(sid, LIN, "Single row, facing north/south", "Basic", "Which of the following statements is true?", t, f,
         "Checking statements against the final arrangement",
         "Aman sits at seat 4 of 7, with three persons on each side, so he is exactly in the middle.",
         [ARR, "Aman: seat 4 of 7, three persons on either side: true",
          "Immediately to Dhara's right (west) is Bhoomi, not Eklavya: false",
          "Second to Hitesh's left (east) is Gunjan, not Chirayu: false",
          "Aman sits between Gunjan (3) and Bhoomi (5): false"], seconds=50)

# ---- L2 Basic: nine seats in a row facing north, six persons, three seats vacant
P = ["Jignesh", "Kritika", "Manan", "Nupur", "Parth", "Rachna"]
IX = {p: i for i, p in enumerate(P)}
conds = [
    ("Kritika sits at the extreme left end of the row.", ("Kritika",), lambda k: k == 1),
    ("Exactly one seat lies between Kritika and Parth, and that seat is vacant.", tuple(P),
     lambda *v: abs(v[IX["Kritika"]] - v[IX["Parth"]]) == 2 and (v[IX["Kritika"]] + v[IX["Parth"]]) // 2 not in v),
    ("Manan sits immediately to the right of Parth.", ("Manan", "Parth"), lambda m, p: m == p + 1),
    ("Jignesh sits third to the right of Nupur.", ("Jignesh", "Nupur"), lambda j, n: j == n + 3),
    ("Rachna sits second to the left of Jignesh.", ("Rachna", "Jignesh"), lambda r, j: r == j - 2),
    ("The seat immediately to the right of Rachna is vacant.", tuple(P),
     lambda *v: v[IX["Rachna"]] + 1 <= 9 and v[IX["Rachna"]] + 1 not in v),
    ("Neither of the two end seats of the row is vacant.", tuple(P), lambda *v: 1 in v and 9 in v),
]
L2 = unique(P, {p: range(1, 10) for p in P}, conds, [P])
at = {v: k for k, v in L2.items()}
row = [at.get(i, "vacant") for i in range(1, 10)]
assert row == ["Kritika", "vacant", "Parth", "Manan", "vacant", "Nupur", "Rachna", "vacant", "Jignesh"]
ARR = "Seats 1 to 9 from the left: " + ", ".join(row)
sid = stimulus("puzzle", "Six persons in a row of nine seats",
               "A row has nine seats, numbered 1 to 9 from the left end. Six persons Jignesh, Kritika, Manan, Nupur, "
               "Parth and Rachna sit in six of the seats, all facing north; the other three seats are vacant.", conds,
               "Kritika = 1, seat 2 is vacant, Parth = 3 and Manan = 4. Rachna is second to the left of Jignesh and "
               "Jignesh third to the right of Nupur, so Nupur, Rachna and Jignesh sit at n, n + 1 and n + 3. Seat 9 "
               "must be occupied, and only these three persons are left, so Jignesh = 9, Rachna = 7 and Nupur = 6. "
               "Seat 8 (to Rachna's right) and seat 5 are vacant.\n\n"
               + table(["Seat", "Occupant"], [(i, row[i - 1]) for i in range(1, 10)]))
rightof = sum(1 for p in P if L2[p] > L2["Manan"])
assert rightof == 3
puzzle_q(sid, LIN, "Single row, facing north/south", "Basic", "How many persons sit to the right of Manan?",
         num_word(rightof), ["Two", "Four", "Five"], "Counting persons, not seats",
         "Manan is at seat 4. To his right are seats 5 to 9, of which 5 and 8 are vacant; Nupur, Rachna and Jignesh "
         "sit there: three persons.", [ARR, "Occupied seats to the right of seat 4: 6, 7, 9"], natural=by_num,
         why_others_wrong="Five counts the seats, not the persons.", seconds=45)
vac = [i for i in range(1, 10) if i not in at]
VAC = lambda a, b, c: f"Seats {a}, {b} and {c}"
puzzle_q(sid, LIN, "Single row, facing north/south", "Basic", "Which seats are vacant?", VAC(*vac),
         [VAC(2, 5, 7), VAC(3, 5, 8), VAC(2, 6, 8)], "Placing the vacant seats",
         "Seat 2 is fixed as vacant by the Kritika–Parth condition. Jignesh must take seat 9, which puts Rachna at 7 "
         "and Nupur at 6; seats 5 and 8 remain empty.", [ARR], seconds=45)
nb = [at[s] for s in (L2["Nupur"] - 1, L2["Nupur"] + 1) if s in at]
assert nb == ["Rachna"]
puzzle_q(sid, LIN, "Single row, facing north/south", "Basic", "Who sits in a seat adjacent to Nupur's seat?", nb[0],
         ["Manan", "Jignesh", "Parth"], "Adjacent seats when some seats are vacant",
         "Nupur is at seat 6. Seat 5 is vacant and seat 7 is Rachna's, so Rachna is the only person beside her.",
         [ARR, "Seat 5: vacant; seat 7: Rachna"],
         why_others_wrong="Manan is at seat 4, separated from Nupur by the vacant seat 5; Jignesh is at seat 9.",
         seconds=40)

# ---- L3, L4 Intermediate (standalone): unknown number of persons
sols = [n for n in range(1, 60) if 12 <= n and 8 <= n and abs(12 - (n - 8 + 1)) - 1 == 3 and (n - 8 + 1) != 12]
assert sols == [15, 23]
mcq(LIN, "Unknown number of persons", "Intermediate",
    "Some persons sit in a row, all facing north. Ritu sits 12th from the left end and Sohail sits 8th from the right "
    "end. Exactly three persons sit between Ritu and Sohail. What is the minimum possible number of persons in the "
    "row?", str(min(sols)), ["19", "23", "17"], "Two cases: the two persons may or may not 'cross' each other",
    "Sohail is either to the right of Ritu or to her left. Right: Sohail is 16th from the left and 8th from the right, "
    "so the row has 16 + 8 − 1 = 23 persons. Left: Sohail is 12 − 4 = 8th from the left and 8th from the right, so the "
    "row has 8 + 8 − 1 = 15 persons. The minimum is 15.",
    ["Case 1, Sohail to the right of Ritu: Sohail = 12 + 4 = 16th from the left → total 16 + 8 − 1 = 23",
     "Case 2, Sohail to the left of Ritu: Sohail = 12 − 4 = 8th from the left → total 8 + 8 − 1 = 15",
     "Check case 2: Ritu at 12 of 15 is 4th from the right, and seats 9–11 lie between them: valid",
     "Minimum = 15"],
    why_others_wrong="23 is the maximum (the non-crossing case); 19 and 17 come from adding ranks without the "
                     "between-count.", natural=int, seconds=60, verified_by=RECOMP)
sols = []
for n in range(3, 60):
    for ni in range(1, n + 1):
        m = 4
        o = ni + 3  # facing south: left = east (higher seat number from the west)
        if ni != m and abs(ni - m) - 1 == 5 and 1 <= o <= n and n - o == 1 and len({m, ni, o}) == 3:
            sols.append((n, ni, o))
assert sols == [(14, 10, 13)]
n_, ni_, o_ = sols[0]
ans = n_ - 4
assert ans == 10
mcq(LIN, "Unknown number of persons", "Intermediate",
    "Some persons sit in a row, all facing south. Mohan sits fourth from the west end of the row. Exactly five "
    "persons sit between Mohan and Nisha. Ojas sits third to the left of Nisha, and only one person sits between "
    "Ojas and the east end of the row. How many persons sit to the left of Mohan?", str(ans), ["3", "9", "11"],
    "Facing south: the left is towards the east",
    "Count seats from the west end. Mohan = 4. Nisha is six seats away: 4 + 6 = 10 (4 − 6 is impossible). Facing "
    "south, Ojas's seat three to Nisha's left is to the east: 13. One person sits between Ojas and the east end, so "
    "the row has 14 persons. Mohan's left is towards the east, where seats 5 to 14 hold 10 persons.",
    ["Mohan = 4th from the west", "Nisha = 4 + 6 = 10 (five persons between)",
     "Ojas = 10 + 3 = 13 (left of a south-facing person = east)", "One person between Ojas and the east end ⇒ 14 persons",
     "Persons to Mohan's left (east of seat 4) = 14 − 4 = 10"],
    why_others_wrong="3 counts the persons to Mohan's west, which is his right; 9 and 11 are off-by-one counts.",
    natural=int, seconds=70, verified_by=RECOMP)

# ---- L5 Advanced: unknown number of persons in a row facing north
P = ["Aarti", "Bharat", "Chhavi", "Dinesh", "Eshita", "Faisal", "Girija", "Hemant"]
V = ["n", "Dinesh", "Eshita", "Faisal", "Aarti", "Bharat", "Hemant", "Girija", "Chhavi"]
conds = [
    ("Dinesh sits sixth from the left end of the row.", ("Dinesh",), lambda d: d == 6),
    ("Only two persons sit between Dinesh and Eshita.", ("Dinesh", "Eshita"), lambda d, e: abs(d - e) == 3),
    ("Faisal sits fourth to the left of Eshita.", ("Faisal", "Eshita"), lambda f_, e: f_ == e - 4),
    ("Aarti sits second to the left of Faisal.", ("Aarti", "Faisal"), lambda a, f_: a == f_ - 2),
    ("Bharat sits third to the right of Eshita.", ("Bharat", "Eshita"), lambda b, e: b == e + 3),
    ("As many persons sit between Aarti and Bharat as between Bharat and Hemant.", ("Aarti", "Bharat", "Hemant"),
     lambda a, b, h: abs(a - b) == abs(b - h)),
    ("Hemant sits at one of the extreme ends of the row.", ("n", "Hemant"), lambda n, h: h in (1, n)),
    ("Girija sits exactly in the middle of the row.", ("n", "Girija"), lambda n, g: n % 2 == 1 and g == (n + 1) // 2),
    ("Only five persons sit between Girija and Chhavi.", ("Girija", "Chhavi"), lambda g, c: abs(g - c) == 6),
]
cfull = conds + [("(every named seat lies within the row)", tuple(V), lambda n, *v: max(v) <= n)]
L5 = unique(V, {"n": range(8, 61)} | {p: range(1, 61) for p in P}, cfull, [P])
N5 = L5["n"]
assert N5 == 21 and [L5[p] for p in P] == [3, 12, 17, 6, 9, 5, 11, 21]
ARR = f"{N5} persons; from the left: " + ", ".join(f"{p} {L5[p]}" for p in sorted(P, key=L5.get))
sid = stimulus("puzzle", "A row of unknown length",
               "Some persons sit in a straight row, all facing north. The number of persons in the row is not given. "
               "Aarti, Bharat, Chhavi, Dinesh, Eshita, Faisal, Girija and Hemant are among them.", conds,
               "Count positions from the left end. Dinesh = 6, so Eshita = 3 or 9. Faisal is four places to Eshita's "
               "left, which is impossible from 3, so Eshita = 9, Faisal = 5, Aarti = 3 and Bharat = 12. Eight persons "
               "sit between Aarti and Bharat, so Hemant is nine places from Bharat: 3 (Aarti's seat) or 21. Hence "
               "Hemant = 21, and as he is at an end, the row has 21 persons. The middle of 21 is 11 (Girija). Chhavi "
               "is six places from Girija: 5 (Faisal's seat) or 17, so Chhavi = 17.\n\n"
               + table(["Position from the left", "Person"], [(L5[p], p) for p in sorted(P, key=L5.get)])
               + "\n\nAll other positions are held by persons whose names are not given.")
puzzle_q(sid, LIN, "Unknown number of persons", "Advanced", "How many persons sit in the row?", str(N5),
         ["19", "23", "20"], "Fixing the row length from an end condition",
         "Hemant must be nine places from Bharat (12), at 21, and he sits at an end, so the row has 21 persons.",
         ["Eshita = 9 (Eshita = 3 leaves no seat for Faisal)", "Faisal = 5, Aarti = 3, Bharat = 12",
          "Between Aarti and Bharat: 8 persons ⇒ Hemant = 12 + 9 = 21", "Hemant at an end ⇒ 21 persons"],
         natural=int, seconds=90)
gap = L5["Girija"] - L5["Aarti"] - 1
assert gap == 7
puzzle_q(sid, LIN, "Unknown number of persons", "Advanced", "How many persons sit between Aarti and Girija?",
         str(gap), ["6", "8", "9"], "Positions of named persons in a longer row",
         f"Aarti is 3rd and Girija 11th from the left, so {gap} persons (positions 4 to 10) sit between them.",
         [ARR, f"11 − 3 − 1 = {gap}"], natural=int, seconds=75)
fr = N5 - L5["Chhavi"] + 1
assert fr == 5
ORDN = lambda k: f"{k}{'th' if 10 <= k % 100 <= 20 else {1: 'st', 2: 'nd', 3: 'rd'}.get(k % 10, 'th')}"
puzzle_q(sid, LIN, "Unknown number of persons", "Advanced",
         "What is Chhavi's position from the right end of the row?", ORDN(fr), ["4th", "6th", "17th"],
         "Converting a left-end position to a right-end position",
         f"Chhavi is 17th from the left in a row of {N5}, so she is {N5} − 17 + 1 = {fr}th from the right.",
         [ARR, "Chhavi = 11 ± 6 → 17 (5 is Faisal's)", f"From the right: 21 − 17 + 1 = {fr}"],
         why_others_wrong="17th is her position from the left end.", natural=lambda t: int(t[:-2]), seconds=75)
stm = [
    ("Bharat sits immediately to the right of Girija", L5["Bharat"] == L5["Girija"] + 1),
    ("Eshita sits exactly in the middle of the row", L5["Eshita"] == (N5 + 1) // 2),
    ("Faisal sits third to the left of Dinesh", L5["Faisal"] == L5["Dinesh"] - 3),
    ("Exactly ten persons sit between Bharat and Hemant", L5["Hemant"] - L5["Bharat"] - 1 == 10),
]
t, f = one_true(stm)
puzzle_q(sid, LIN, "Unknown number of persons", "Advanced", "Which of the following statements is true?", t, f,
         "Checking statements in a row of unknown length",
         "Girija is 11th and Bharat 12th from the left, so Bharat is immediately to Girija's right.",
         [ARR, "Girija 11, Bharat 12: true", "The middle is 11 (Girija), not Eshita (9): false",
          "Third to the left of Dinesh (6) is position 3, Aarti: false",
          "Between Bharat (12) and Hemant (21): 8 persons, not 10: false"], seconds=80)

# ---- L6 Advanced: two rows of five, BOTH facing north (Row 1 in front, Row 2 directly behind)
P = ["Aditya", "Bela", "Chetna", "Darshan", "Esha", "Gopal", "Indu", "Jatin", "Kirti", "Lalit"]
SEATS = [r * 10 + c for r in (1, 2) for c in range(1, 6)]
rw, cl = (lambda s: s // 10), (lambda s: s % 10)
RN = lambda s, k: s + k if 1 <= cl(s) + k <= 5 else None  # everyone faces north: right = east
conds = [
    ("Aditya sits in the middle of one of the rows.", ("Aditya",), lambda a: cl(a) == 3),
    ("The person who sits directly in front of Aditya sits immediately to the right of Indu.", ("Aditya", "Indu"),
     lambda a, i: rw(a) == 2 and RN(i, 1) == a - 10),
    ("Chetna sits directly behind Kirti.", ("Chetna", "Kirti"), lambda c, k: c == k + 10),
    ("Kirti is an immediate neighbour of Darshan.", ("Kirti", "Darshan"),
     lambda k, d: rw(k) == rw(d) and abs(k - d) == 1),
    ("Gopal and Bela sit at the two extreme ends of the same row.", ("Gopal", "Bela"),
     lambda g, b: rw(g) == rw(b) and {cl(g), cl(b)} == {1, 5}),
    ("Lalit sits immediately to the right of Chetna.", ("Lalit", "Chetna"), lambda l, c: RN(c, 1) == l),
    ("Esha sits second to the left of Chetna.", ("Esha", "Chetna"), lambda e, c: RN(c, -2) == e),
    ("Jatin does not sit directly behind Gopal.", ("Jatin", "Gopal"), lambda j, g: j != g + 10),
]
L6 = unique(P, {p: SEATS for p in P}, conds, [P])
at = {v: k for k, v in L6.items()}
assert [at[s] for s in SEATS] == ["Bela", "Indu", "Darshan", "Kirti", "Gopal",
                                  "Jatin", "Esha", "Aditya", "Chetna", "Lalit"]
ARR = ("Row 1 (front), west to east: " + ", ".join(at[10 + c] for c in range(1, 6)) +
       "; Row 2 (behind), west to east: " + ", ".join(at[20 + c] for c in range(1, 6)))
sid = stimulus("puzzle", "Two rows facing the same way",
               "Ten persons Aditya, Bela, Chetna, Darshan, Esha, Gopal, Indu, Jatin, Kirti and Lalit sit in two "
               "parallel rows of five seats each. All of them face north. Row 1 is in front (to the north) and Row 2 "
               "is directly behind it, so each person in Row 2 sits directly behind one person of Row 1. Who sits in "
               "which row is not given.", conds,
               "Someone sits in front of Aditya, so Aditya is in the middle of Row 2, and the person in front of him "
               "(Row 1, seat 3) is immediately to the right of Indu: Indu is at Row 1, seat 2. Chetna sits behind "
               "Kirti, so Kirti is in Row 1 and Chetna in Row 2. Chetna has Lalit on her right and Esha second to her "
               "left, so Chetna is at seat 3 or 4 of Row 2; seat 3 is Aditya's, so Chetna = Row 2 seat 4, Esha = seat "
               "2, Lalit = seat 5, and Kirti = Row 1 seat 4. Darshan is next to Kirti: Row 1 seat 3 or 5. Gopal and "
               "Bela must be at both ends of one row; Row 2 already has Lalit at an end, so they take Row 1 seats 1 "
               "and 5, which puts Darshan at Row 1 seat 3. Jatin takes Row 2 seat 1; he is not behind Gopal, so Bela "
               "= Row 1 seat 1 and Gopal = Row 1 seat 5.\n\n"
               + table(["Seat (west to east)", "Row 1 (front)", "Row 2 (behind)"],
                       [(c, at[10 + c], at[20 + c]) for c in range(1, 6)]))
ans = at[L6["Darshan"] + 10]
assert ans == "Aditya"
puzzle_q(sid, LIN, "Double row", "Advanced", "Who sits directly behind Darshan?", ans, ["Chetna", "Esha", "Indu"],
         "Front and behind in two rows facing the same direction",
         "Darshan is at seat 3 of Row 1, and the person at seat 3 of Row 2 is Aditya.",
         ["Aditya = Row 2 seat 3; Indu = Row 1 seat 2", "Chetna = Row 2 seat 4 with Esha (2) and Lalit (5)",
          "Gopal and Bela take the Row 1 ends, so Darshan = Row 1 seat 3", ARR],
         why_others_wrong="Chetna sits behind Kirti and Esha behind Indu; Indu sits in Row 1.", seconds=90)
front_l = at[L6["Lalit"] - 10]
ans = at[RN(L6[front_l], -1)]
assert front_l == "Gopal" and ans == "Kirti"
puzzle_q(sid, LIN, "Double row", "Advanced",
         "Who sits immediately to the left of the person who sits directly in front of Lalit?", ans,
         ["Gopal", "Darshan", "Chetna"], "Chaining two relations",
         "Lalit is at Row 2 seat 5, so Gopal (Row 1 seat 5) is directly in front of him. Everyone faces north, so "
         "Gopal's left is seat 4 of Row 1: Kirti.", [ARR, "In front of Lalit: Gopal", "Immediately left of Gopal: Kirti"],
         why_others_wrong="Gopal himself is the person in front of Lalit; Darshan is second to Gopal's left; Chetna is "
                          "immediately to Lalit's left.", seconds=80)
gap = abs(cl(L6["Indu"]) - cl(L6["Gopal"])) - 1
assert gap == 2 and rw(L6["Indu"]) == rw(L6["Gopal"])
puzzle_q(sid, LIN, "Double row", "Advanced", "How many persons sit between Indu and Gopal?", num_word(gap),
         ["One", "Three", "None"], "Counting within one row",
         "Indu and Gopal both sit in Row 1, at seats 2 and 5, so Darshan and Kirti sit between them.", [ARR],
         natural=by_num, seconds=60)
stm = [
    ("Jatin sits directly behind Bela", L6["Jatin"] == L6["Bela"] + 10),
    ("Esha sits directly behind Darshan", L6["Esha"] == L6["Darshan"] + 10),
    ("Kirti sits at an extreme end of Row 1", cl(L6["Kirti"]) in (1, 5)),
    ("Aditya sits immediately to the right of Chetna", RN(L6["Chetna"], 1) == L6["Aditya"]),
]
t, f = one_true(stm)
puzzle_q(sid, LIN, "Double row", "Advanced", "Which of the following statements is true?", t, f,
         "Checking statements in a two-row arrangement",
         "Bela is at Row 1 seat 1 and Jatin at Row 2 seat 1, so Jatin sits directly behind Bela.",
         [ARR, "Jatin (Row 2, seat 1) is behind Bela (Row 1, seat 1): true",
          "Behind Darshan (seat 3) is Aditya, not Esha: false", "Kirti is at seat 4 of Row 1, not an end: false",
          "Immediately to Chetna's right is Lalit; Aditya is on her left: false"], seconds=75)

# ================================================================================================ CIRCULAR SEATING
CIR = "Circular Seating Arrangement"

# ---- C1 Basic (standalone): five persons facing the centre (seats 0..4 anticlockwise; right = +1)
P = ["Arnav", "Bhakti", "Chinmay", "Damini", "Farida"]
N = 5
conds = [("Bhakti sits second to the right of Arnav.", ("Bhakti", "Arnav"), lambda b, a: b == (a + 2) % N),
         ("Chinmay sits immediately to the left of Arnav.", ("Chinmay", "Arnav"), lambda c, a: c == (a - 1) % N),
         ("Damini is an immediate neighbour of Chinmay.", ("Damini", "Chinmay"),
          lambda d, c: (d - c) % N in (1, N - 1))]
C1 = unique(P, {p: range(N) for p in P} | {"Arnav": [0]}, conds, [P])
at = {v: k for k, v in C1.items()}
ans = at[(C1["Damini"] - 2) % N]
assert [at[i] for i in range(N)] == ["Arnav", "Farida", "Bhakti", "Damini", "Chinmay"] and ans == "Farida"
mcq(CIR, "Facing centre", "Basic",
    "Five friends Arnav, Bhakti, Chinmay, Damini and Farida sit around a circular table, equally spaced and all "
    "facing the centre. " + " ".join(t for t, _, _ in conds) + "\n\nWho sits second to the left of Damini?", ans,
    ["Chinmay", "Arnav", "Bhakti"], "Facing the centre: right is anticlockwise, left is clockwise",
    "Going to the right (anticlockwise) from Arnav the order is Arnav, Farida, Bhakti, Damini, Chinmay. Damini's left "
    "is clockwise: Bhakti, then Farida.",
    ["Fix Arnav; Bhakti is two seats to his right, Chinmay one seat to his left",
     "The only empty seat next to Chinmay is between Bhakti and Chinmay: Damini",
     "Farida takes the last seat, between Arnav and Bhakti",
     "Clockwise from Damini: Bhakti, Farida"],
    why_others_wrong="Chinmay is immediately to Damini's right and Arnav second to her right; Bhakti is immediately "
                     "to her left.", seconds=45, verified_by=BRUTE)

# ---- C2 Basic (standalone): rectangular table, one person at each shorter side, two on each longer side
P = ["Gauri", "Harsh", "Ilesh", "Jaya", "Kanak", "Lata"]
N = 6
SHORT = {0, 3}  # seats 0..5 anticlockwise; seats 0 and 3 are the shorter sides; 1-2 and 4-5 are the longer sides
side = lambda s: "S" if s in SHORT else ("L1" if s in (1, 2) else "L2")
conds = [("Gauri sits at one of the shorter sides of the table.", ("Gauri",), lambda g: g in SHORT),
         ("Harsh sits at the other shorter side.", ("Harsh", "Gauri"), lambda h, g: h in SHORT and h != g),
         ("Ilesh sits immediately to the right of Harsh.", ("Ilesh", "Harsh"), lambda i, h: i == (h + 1) % N),
         ("Jaya sits second to the left of Ilesh.", ("Jaya", "Ilesh"), lambda j, i: j == (i - 2) % N),
         ("Kanak sits immediately to the left of Gauri.", ("Kanak", "Gauri"), lambda k, g: k == (g - 1) % N)]
C2 = unique(P, {p: range(N) for p in P} | {"Gauri": [0]}, conds, [P])  # the two shorter sides are symmetric
at = {v: k for k, v in C2.items()}
mate = [p for p in P if p != "Jaya" and side(C2[p]) == side(C2["Jaya"])]
assert [at[i] for i in range(N)] == ["Gauri", "Lata", "Jaya", "Harsh", "Ilesh", "Kanak"] and mate == ["Lata"]
mcq(CIR, "Square and rectangular tables", "Basic",
    "Six persons Gauri, Harsh, Ilesh, Jaya, Kanak and Lata sit around a rectangular table, all facing the centre. One "
    "person sits at each of the two shorter sides and two persons sit at each of the two longer sides. "
    + " ".join(t for t, _, _ in conds) + "\n\nWho sits at the same longer side of the table as Jaya?", mate[0],
    ["Kanak", "Ilesh", "Harsh"], "Rectangular table: seats in order around the table",
    "Going to the right (anticlockwise) from Gauri: Gauri (shorter side), two seats on one longer side, Harsh (other "
    "shorter side), two seats on the other longer side. Ilesh is the first seat after Harsh, Jaya is two seats to "
    "Ilesh's left (just before Harsh), Kanak is just before Gauri, and Lata takes the seat after Gauri. Jaya and Lata "
    "share a longer side.",
    ["Seats to the right of Gauri: [long side A: s1, s2], Harsh, [long side B: s4, s5]",
     "Ilesh = s4 (immediately right of Harsh); Jaya = second to Ilesh's left = s2",
     "Kanak = immediately left of Gauri = s5; Lata = s1", "Long side A: Lata and Jaya"],
    why_others_wrong="Kanak and Ilesh share the other longer side; Harsh sits at a shorter side.", seconds=50,
    verified_by=BRUTE)

# ---- C3 Intermediate: eight chairs around a circle, seven persons, one chair vacant, all facing the centre
P = ["Mahi", "Nirav", "Oshin", "Prakash", "Qadir", "Rupa", "Sagar"]
N = 8
IX = {p: i for i, p in enumerate(P)}
VACANT = lambda v: next(s for s in range(N) if s not in v)
conds = [
    ("Mahi sits opposite Nirav.", ("Mahi", "Nirav"), lambda m, n: n == (m + 4) % N),
    ("The vacant chair is second to the right of Mahi.", tuple(P), lambda *v: VACANT(v) == (v[IX["Mahi"]] + 2) % N),
    ("Sagar sits immediately to the left of Nirav.", ("Sagar", "Nirav"), lambda s, n: s == (n - 1) % N),
    ("Oshin sits second to the right of Sagar.", ("Oshin", "Sagar"), lambda o, s: o == (s + 2) % N),
    ("Prakash sits immediately to the left of Mahi.", ("Prakash", "Mahi"), lambda p, m: p == (m - 1) % N),
    ("Qadir does not sit next to the vacant chair.", tuple(P),
     lambda *v: (v[IX["Qadir"]] - VACANT(v)) % N not in (1, N - 1)),
]
C3 = unique(P, {p: range(N) for p in P} | {"Mahi": [0]}, conds, [P])
at = {v: k for k, v in C3.items()}
VC = VACANT(list(C3.values()))
seat = lambda s: at.get(s % N, "the vacant chair")
assert [seat(i) for i in range(N)] == ["Mahi", "Rupa", "the vacant chair", "Sagar", "Nirav", "Oshin", "Qadir",
                                       "Prakash"]
ARR = "Going right (anticlockwise) from Mahi: " + ", ".join(seat(i) for i in range(N))
sid = stimulus("puzzle", "Seven persons and a vacant chair",
               "Eight chairs are placed around a circular table, equally spaced. Seven persons Mahi, Nirav, Oshin, "
               "Prakash, Qadir, Rupa and Sagar sit on seven of them, all facing the centre; one chair is vacant. "
               "Positions such as 'second to the right' are counted by chairs, including the vacant chair.", conds,
               "Fix Mahi. Nirav is opposite her (four chairs away), the vacant chair is second to her right and "
               "Prakash immediately to her left. Sagar is immediately to Nirav's left, i.e. between the vacant chair "
               "and Nirav, and Oshin is second to Sagar's right, i.e. immediately to Nirav's right. The two chairs "
               "left are the one between Mahi and the vacant chair and the one between Oshin and Prakash. Qadir "
               "cannot sit next to the vacant chair, so Qadir sits between Oshin and Prakash and Rupa between Mahi "
               "and the vacant chair.\n\n"
               + table(["Chair (anticlockwise from Mahi)", "Occupant"], [(i, seat(i)) for i in range(N)]))
ans = seat(VC + 4)
assert ans == "Qadir"
puzzle_q(sid, CIR, "Facing centre", "Intermediate", "Who sits opposite the vacant chair?", ans,
         ["Rupa", "Prakash", "Oshin"], "Opposite chairs in an eight-chair circle",
         "The vacant chair is second to Mahi's right; four chairs further on is the chair between Oshin and Prakash, "
         "which is Qadir's.", [ARR, f"Opposite the vacant chair: {ans}"],
         why_others_wrong="Rupa sits next to the vacant chair; Prakash is opposite Sagar and Oshin opposite Rupa.",
         seconds=70)
ans = seat(C3["Oshin"] - 3)
assert ans == "the vacant chair"
ans = seat(C3["Oshin"] - 2)
assert ans == "Sagar"
puzzle_q(sid, CIR, "Facing centre", "Intermediate", "Who sits second to the left of Oshin?", ans,
         ["Nirav", "Qadir", "Prakash"], "Facing the centre: the left is clockwise",
         "Oshin faces the centre, so her left is clockwise: Nirav, then Sagar.", [ARR, "Clockwise from Oshin: Nirav, Sagar"],
         why_others_wrong="Nirav is immediately to her left; Qadir is immediately to her right and Prakash second to "
                          "her right.", seconds=60)
k = next(k for k in range(1, N) if seat(C3["Rupa"] + k) == "Nirav")
between = [seat(C3["Rupa"] + i) for i in range(1, k)]
cnt = sum(1 for x in between if x in P)
assert between == ["the vacant chair", "Sagar"] and cnt == 1
puzzle_q(sid, CIR, "Facing centre", "Intermediate",
         "How many persons sit between Rupa and Nirav when counted to the right of Rupa?", num_word(cnt),
         ["Two", "Three", "None"], "Counting persons, not chairs",
         "To Rupa's right (anticlockwise) come the vacant chair, Sagar and then Nirav. Only one person, Sagar, sits "
         "between them.", [ARR, "Right of Rupa: vacant chair, Sagar, Nirav"],
         why_others_wrong="Two counts the vacant chair as a person.", natural=by_num, seconds=60)
stm = [
    ("Prakash sits opposite Sagar", C3["Prakash"] == (C3["Sagar"] + 4) % N),
    ("Rupa sits immediately to the left of Mahi", C3["Rupa"] == (C3["Mahi"] - 1) % N),
    ("Oshin sits next to the vacant chair", (C3["Oshin"] - VC) % N in (1, N - 1)),
    ("Qadir sits third to the right of Nirav", C3["Qadir"] == (C3["Nirav"] + 3) % N),
]
t, f = one_true(stm)
puzzle_q(sid, CIR, "Facing centre", "Intermediate", "Which of the following statements is true?", t, f,
         "Checking statements against the circle", "Prakash is at chair 7 and Sagar at chair 3 (counting "
         "anticlockwise from Mahi at 0), four chairs apart: they sit opposite each other.",
         [ARR, "Prakash (7) and Sagar (3) are four chairs apart: true",
          "Rupa is immediately to Mahi's right, not her left (Prakash is on her left): false",
          "Oshin's neighbours are Nirav and Qadir: false",
          "Third to Nirav's right is Prakash; Qadir is second to his right: false"], seconds=60)

# ---- C4 Intermediate: seven persons around a circle, some facing the centre (I) and some outside (O)
P = ["Anirudh", "Bindiya", "Chandra", "Deepak", "Eshani", "Firdaus", "Gagan"]
N = 7
RC = lambda s, f, k: (s + (k if f == "I" else -k)) % N
adj = lambda a, b: (a - b) % N in (1, N - 1)
conds = [
    ("Anirudh faces the centre, and Chandra sits second to the right of Anirudh.", ("Anirudh", "fAnirudh", "Chandra"),
     lambda a, f_, c: f_ == "I" and c == RC(a, f_, 2)),
    ("Gagan sits between Anirudh and Chandra and faces outside.", ("Gagan", "fGagan", "Anirudh", "Chandra"),
     lambda g, fg, a, c: fg == "O" and adj(g, a) and adj(g, c)),
    ("Firdaus is an immediate neighbour of Anirudh.", ("Firdaus", "Anirudh"), adj),
    ("Bindiya sits second to the right of Firdaus.", ("Firdaus", "fFirdaus", "Bindiya"),
     lambda f_, ff, b: b == RC(f_, ff, 2)),
    ("Deepak sits immediately to the right of Bindiya.", ("Bindiya", "fBindiya", "Deepak"),
     lambda b, fb, d: d == RC(b, fb, 1)),
    ("Chandra sits immediately to the right of Eshani.", ("Eshani", "fEshani", "Chandra"),
     lambda e, fe, c: c == RC(e, fe, 1)),
    ("Exactly three persons face outside.", tuple("f" + p for p in P), lambda *f_: f_.count("O") == 3),
    ("Deepak and Chandra face the same direction.", ("fDeepak", "fChandra"), lambda a, b: a == b),
]
order = [x for p in P for x in (p, "f" + p)]
dom = {p: range(N) for p in P} | {"f" + p: "IO" for p in P} | {"Anirudh": [0]}
C4 = unique(order, dom, conds, [P])
at = {C4[p]: p for p in P}
fc = {p: C4["f" + p] for p in P}
rt = lambda p, k: at[RC(C4[p], fc[p], k)]
FCN = {"I": "centre", "O": "outside"}
assert [(at[i], fc[at[i]]) for i in range(N)] == [("Anirudh", "I"), ("Gagan", "O"), ("Chandra", "I"), ("Eshani", "O"),
                                                  ("Bindiya", "I"), ("Deepak", "I"), ("Firdaus", "O")]
ARR = "Anticlockwise from Anirudh: " + ", ".join(f"{at[i]} ({FCN[fc[at[i]]]})" for i in range(N))
sid = stimulus("puzzle", "Seven persons around a circle, facing in or out",
               "Seven persons Anirudh, Bindiya, Chandra, Deepak, Eshani, Firdaus and Gagan sit around a circular "
               "table, equally spaced. Some of them face the centre and the others face outside. (For a person facing "
               "the centre the right is anticlockwise; for a person facing outside the right is clockwise.)", conds,
               "Fix Anirudh (facing the centre). Chandra is two seats anticlockwise from him and Gagan (facing "
               "outside) sits between them; Firdaus takes the seat on Anirudh's other side. If Firdaus faced the "
               "centre, second to his right would be Gagan's seat, so Firdaus faces outside and Bindiya sits two seats "
               "clockwise from him. The two seats left lie on either side of Bindiya. Chandra is immediately to "
               "Eshani's right, so Eshani is Chandra's neighbour (the seat between Chandra and Bindiya) and, to have "
               "Chandra on her right, faces outside. Deepak takes the seat between Bindiya and Firdaus; being "
               "immediately to Bindiya's right, he makes Bindiya face the centre. Gagan, Firdaus and Eshani are the "
               "three facing outside, so Chandra and Deepak face the centre.\n\n"
               + table(["Anticlockwise from Anirudh", "Person", "Faces"], [(i, at[i], FCN[fc[at[i]]]) for i in range(N)]))
ans = rt("Deepak", -2)
assert ans == "Eshani" and rt("Deepak", 2) == "Anirudh"
puzzle_q(sid, CIR, "Facing inside and outside", "Intermediate", "Who sits second to the left of Deepak?", ans,
         ["Anirudh", "Bindiya", "Firdaus"], "Facing the centre: the left is clockwise",
         "Deepak faces the centre, so his left is clockwise: Bindiya, then Eshani.",
         ["Firdaus must face outside (otherwise Bindiya would land on Gagan's seat)", ARR,
          "Clockwise from Deepak: Bindiya, Eshani"],
         why_others_wrong="Anirudh is second to Deepak's right; Bindiya is immediately to his left and Firdaus "
                          "immediately to his right.", seconds=70)
out = [p for p in P if fc[p] == "O"]
assert out == ["Eshani", "Firdaus", "Gagan"]
puzzle_q(sid, CIR, "Facing inside and outside", "Intermediate", "Which three persons face outside?",
         "Eshani, Firdaus and Gagan", ["Bindiya, Firdaus and Gagan", "Chandra, Eshani and Gagan",
                                       "Deepak, Eshani and Firdaus"], "Fixing facing directions from 'right' clues",
         "Gagan faces outside (given). Firdaus must face outside for Bindiya to fit, and Eshani must face outside for "
         "Chandra to be on her right. That makes three, so everyone else faces the centre.", [ARR], seconds=60)
rel = next(f"{['Immediately', 'Second', 'Third'][k - 1]} to the {side_}"
           for k in (1, 2, 3) for side_, sg in (("left", -1), ("right", 1)) if rt("Firdaus", sg * k) == "Gagan")
assert rel == "Second to the left"
puzzle_q(sid, CIR, "Facing inside and outside", "Intermediate",
         "What is the position of Gagan with respect to Firdaus?", rel,
         ["Second to the right", "Third to the right", "Immediately to the left"],
         "Relative position for an outside-facing person",
         "Firdaus faces outside, so his left is anticlockwise: Anirudh, then Gagan. Gagan is second to his left.",
         [ARR, "Firdaus faces outside → left = anticlockwise", "Anticlockwise from Firdaus: Anirudh, Gagan"],
         why_others_wrong="'Second to the right' is what you get by treating Firdaus as facing the centre.", seconds=65)
ans = rt("Chandra", 3)
assert ans == "Deepak" and rt("Chandra", -3) == "Firdaus"
puzzle_q(sid, CIR, "Facing inside and outside", "Intermediate", "Who sits third to the right of Chandra?", ans,
         ["Firdaus", "Bindiya", "Eshani"], "Counting to the right of a centre-facing person",
         "Chandra faces the centre, so her right is anticlockwise: Eshani, Bindiya, Deepak.",
         [ARR, "Anticlockwise from Chandra: Eshani, Bindiya, Deepak"],
         why_others_wrong="Firdaus is third to her left; Bindiya second and Eshani first to her right.", seconds=55)

# ---- C5 Advanced: two concentric circles; inner circle faces outside, outer circle faces the centre
P = ["Harini", "Ibrahim", "Juhi", "Kishore", "Leena", "Mridul", "Nayan", "Oindrila"]
SEATS = [0, 1, 2, 3, 10, 11, 12, 13]  # k = outer seat k (faces the centre); 10 + k = inner seat k (faces outside)
inner = lambda s: s >= 10
face_ = lambda s: s - 10 if inner(s) else s + 10  # outer seat k and inner seat k face each other
RCC = lambda s, k: (10 + (s - 10 - k) % 4) if inner(s) else (s + k) % 4  # k-th to the right in one's own circle
conds = [
    ("Harini sits in the outer circle and faces Nayan.", ("Harini", "Nayan"),
     lambda h, n: not inner(h) and n == face_(h)),
    ("Mridul sits second to the right of Harini.", ("Mridul", "Harini"), lambda m, h: m == RCC(h, 2)),
    ("Leena faces Mridul.", ("Leena", "Mridul"), lambda l, m: l == face_(m)),
    ("Juhi sits immediately to the right of Leena.", ("Juhi", "Leena"), lambda j, l: j == RCC(l, 1)),
    ("Kishore faces Juhi.", ("Kishore", "Juhi"), lambda k, j: k == face_(j)),
    ("Ibrahim is an immediate neighbour of Nayan.", ("Ibrahim", "Nayan"),
     lambda i, n: inner(i) == inner(n) and i in (RCC(n, 1), RCC(n, -1))),
]
C5 = unique(P, {p: SEATS for p in P} | {"Harini": [0]}, conds, [P])
at = {v: k for k, v in C5.items()}
assert [at[s] for s in SEATS] == ["Harini", "Kishore", "Mridul", "Oindrila", "Nayan", "Juhi", "Leena", "Ibrahim"]
ARR = ("Outer circle (anticlockwise): " + ", ".join(at[k] for k in range(4)) +
       "; inner circle, in the same order: " + ", ".join(at[10 + k] for k in range(4)) +
       " (each inner person faces the outer person listed in the same place)")
sid = stimulus("puzzle", "Two concentric circles",
               "Eight persons Harini, Ibrahim, Juhi, Kishore, Leena, Mridul, Nayan and Oindrila sit around two "
               "concentric circular tables, four at each, equally spaced. The persons at the inner table face "
               "outside, and those at the outer table face the centre, so every inner person faces exactly one outer "
               "person. Positions such as 'to the right' are counted among the persons of one's own circle.", conds,
               "Harini is in the outer circle facing Nayan (inner). Facing the centre, Harini's right is "
               "anticlockwise, so Mridul is the outer seat opposite Harini, and Leena (inner) faces Mridul. Leena "
               "faces outside, so her right is clockwise; the inner seat immediately clockwise of Leena is Juhi's, "
               "and Kishore is the outer person facing Juhi, i.e. immediately to Harini's right. Ibrahim must sit "
               "beside Nayan in the inner circle; the only free inner seat is the one opposite Juhi, so Ibrahim sits "
               "there, and Oindrila takes the last outer seat, facing Ibrahim.\n\n"
               + table(["Place (anticlockwise)", "Outer circle (faces centre)", "Inner circle (faces outside)"],
                       [(k + 1, at[k], at[10 + k]) for k in range(4)]))
ans = at[face_(C5["Oindrila"])]
assert ans == "Ibrahim"
puzzle_q(sid, CIR, "Facing inside and outside", "Advanced", "Who faces Oindrila?", ans, ["Juhi", "Leena", "Nayan"],
         "Concentric circles: pair each outer seat with the inner seat in front of it",
         "Oindrila takes the only outer seat left, and the inner person in front of that seat is Ibrahim.",
         ["Harini faces Nayan; Mridul (second to Harini's right) faces Leena",
          "Juhi is immediately to Leena's right (clockwise, as Leena faces outside); Kishore faces Juhi",
          "Ibrahim, Nayan's neighbour, takes the last inner seat; Oindrila faces him", ARR],
         why_others_wrong="Juhi faces Kishore, Leena faces Mridul and Nayan faces Harini.", seconds=100)
ans = at[RCC(C5[at[face_(C5["Kishore"])]], -1)]
assert at[face_(C5["Kishore"])] == "Juhi" and ans == "Leena"
puzzle_q(sid, CIR, "Facing inside and outside", "Advanced",
         "Who sits immediately to the left of the person who faces Kishore?", ans,
         ["Nayan", "Ibrahim", "Mridul"], "Inner circle faces outside: its left is anticlockwise",
         "Juhi faces Kishore. Juhi faces outside, so her left is anticlockwise in the inner circle: Leena.",
         [ARR, "Person facing Kishore: Juhi", "Juhi's left (anticlockwise): Leena"],
         why_others_wrong="Nayan is immediately to Juhi's right; Ibrahim sits opposite her in the inner circle; Mridul "
                          "is in the outer circle.", seconds=90)
stm = [
    ("Kishore sits immediately to the right of Harini", C5["Kishore"] == RCC(C5["Harini"], 1)),
    ("Juhi faces Mridul", face_(C5["Juhi"]) == C5["Mridul"]),
    ("Ibrahim sits second to the right of Nayan", C5["Ibrahim"] == RCC(C5["Nayan"], 2)),
    ("Mridul faces Ibrahim", face_(C5["Mridul"]) == C5["Ibrahim"]),
]
t, f = one_true(stm)
puzzle_q(sid, CIR, "Facing inside and outside", "Advanced", "Which of the following statements is true?", t, f,
         "Checking statements across two circles",
         "Harini faces the centre, so her right is anticlockwise, and the next outer seat anticlockwise is Kishore's.",
         [ARR, "Kishore is immediately to Harini's right: true", "Juhi faces Kishore, not Mridul: false",
          "Second to Nayan's right (clockwise in the inner circle) is Leena: false",
          "Mridul faces Leena: false"], seconds=90)

# ================================================================================================ FLOOR PUZZLES
FLR = "Floor-Based Puzzles"

# ---- F1 Basic (standalone): five floors
P = ["Aisha", "Balraj", "Chitra", "Dev", "Elina"]
conds = [("Chitra lives on an even-numbered floor.", ("Chitra",), lambda c: c % 2 == 0),
         ("Only one person lives between Chitra and Aisha.", ("Chitra", "Aisha"), lambda c, a: abs(c - a) == 2),
         ("Balraj lives immediately above Chitra.", ("Balraj", "Chitra"), lambda b, c: b == c + 1),
         ("Dev lives on a floor below Aisha's floor.", ("Dev", "Aisha"), lambda d, a: d < a),
         ("Elina does not live on the topmost floor.", ("Elina",), lambda e: e != 5)]
F1 = unique(P, {p: range(1, 6) for p in P}, conds, [P])
at = {v: k for k, v in F1.items()}
ans = at[F1["Chitra"] - 1]
assert [at[i] for i in range(1, 6)] == ["Dev", "Aisha", "Elina", "Chitra", "Balraj"] and ans == "Elina"
mcq(FLR, "Floor and flat", "Basic",
    "Five persons Aisha, Balraj, Chitra, Dev and Elina live on the five floors of a building, one on each floor. The "
    "lowermost floor is numbered 1 and the topmost floor 5.\n" + bullets(conds) +
    "\n\nWho lives on the floor immediately below Chitra?", ans, ["Aisha", "Balraj", "Dev"],
    "Floor puzzle: test the cases of the most restricted person",
    "Chitra is on floor 2 or 4. If she were on 2, Balraj would be on 3, Aisha on 4, Dev on 1 and Elina on the top "
    "floor, which is not allowed. So Chitra is on 4, Balraj on 5, Aisha on 2, Dev on 1 and Elina on 3. Elina lives "
    "immediately below Chitra.",
    ["Case Chitra = 2: Balraj 3, Aisha 4, Dev 1 → Elina 5 (top): rejected",
     "Case Chitra = 4: Balraj 5, Aisha 2 (6 does not exist), Dev 1, Elina 3",
     "Floor 3 (below Chitra): Elina"],
    why_others_wrong="Balraj lives above Chitra; Aisha and Dev are on floors 2 and 1.", seconds=50, verified_by=BRUTE)

# ---- F2 Basic (standalone): four floors with a favourite drink
P = ["Garima", "Hamid", "Ishani", "Jeevan"]
DR = ["Coffee", "Juice", "Milk", "Tea"]
conds = [("The person who likes Coffee lives on the topmost floor.", ("Coffee",), lambda c: c == 4),
         ("Garima lives immediately below the person who likes Coffee.", ("Garima", "Coffee"),
          lambda g, c: g == c - 1),
         ("Ishani lives on a floor above Jeevan's floor.", ("Ishani", "Jeevan"), lambda i, j: i > j),
         ("Hamid lives on a floor below Jeevan's floor.", ("Hamid", "Jeevan"), lambda h, j: h < j),
         ("The person who likes Tea lives immediately above the person who likes Milk.", ("Tea", "Milk"),
          lambda t_, m: t_ == m + 1),
         ("Jeevan does not like Milk.", ("Jeevan", "Milk"), lambda j, m: j != m)]
F2 = unique(P + DR, {x: range(1, 5) for x in P + DR}, conds, [P, DR])
drink = {p: next(d for d in DR if F2[d] == F2[p]) for p in P}
assert drink == {"Garima": "Juice", "Hamid": "Milk", "Ishani": "Coffee", "Jeevan": "Tea"}
mcq(FLR, "Floor with attribute", "Basic",
    "Four persons Garima, Hamid, Ishani and Jeevan live on the four floors of a building, one on each floor (floor 1 "
    "is the lowermost). Each of them likes a different drink among Coffee, Juice, Milk and Tea.\n" + bullets(conds) +
    "\n\nWhich drink does Garima like?", drink["Garima"], ["Tea", "Milk", "Coffee"], "Floor plus one attribute",
    "Coffee is on floor 4 and Garima on floor 3. Ishani is above Jeevan and Jeevan above Hamid, so Ishani = 4, "
    "Jeevan = 2 and Hamid = 1. Tea is immediately above Milk: floors 2–1 or 3–2. If Tea were on 3, Milk would be on "
    "2 (Jeevan), which is not allowed. So Tea = 2 (Jeevan), Milk = 1 (Hamid) and Juice = 3 (Garima).",
    ["Coffee = floor 4, Garima = floor 3", "Hamid < Jeevan < Ishani ⇒ Hamid 1, Jeevan 2, Ishani 4",
     "Tea–Milk on (3, 2) would give Jeevan Milk: rejected ⇒ Tea 2, Milk 1", "Garima (floor 3) likes Juice"],
    why_others_wrong="Tea is Jeevan's, Milk Hamid's and Coffee Ishani's.", seconds=50, verified_by=BRUTE)

# ---- F3 Intermediate: three floors with three flats each (West, Middle, East)
P = ["Ankur", "Barkha", "Charan", "Disha", "Emon", "Falak", "Gaurang", "Heer", "Imtiaz"]
FL9 = [f * 10 + c for f in (1, 2, 3) for c in (1, 2, 3)]
fl, col = (lambda s: s // 10), (lambda s: s % 10)
CN = {1: "West", 2: "Middle", 3: "East"}
conds = [
    ("Imtiaz lives in a Middle flat, but not on the topmost floor.", ("Imtiaz",), lambda i: col(i) == 2 and fl(i) != 3),
    ("Ankur lives in the flat directly above Imtiaz's flat.", ("Ankur", "Imtiaz"), lambda a, i: a == i + 10),
    ("Emon lives in the flat directly below Imtiaz's flat.", ("Emon", "Imtiaz"), lambda e, i: e == i - 10),
    ("Barkha lives in an East flat on the same floor as Imtiaz.", ("Barkha", "Imtiaz"),
     lambda b, i: col(b) == 3 and fl(b) == fl(i)),
    ("Disha lives in the flat directly above Barkha's flat.", ("Disha", "Barkha"), lambda d, b: d == b + 10),
    ("Heer lives in the flat directly above Charan's flat, and both live in West flats.", ("Heer", "Charan"),
     lambda h, c: h == c + 10 and col(c) == 1),
    ("Falak lives in a West flat, on the same floor as Gaurang.", ("Falak", "Gaurang"),
     lambda f_, g: col(f_) == 1 and fl(f_) == fl(g)),
]
F3 = unique(P, {p: FL9 for p in P}, conds, [P])
at = {v: k for k, v in F3.items()}
assert [at[s] for s in FL9] == ["Falak", "Emon", "Gaurang", "Charan", "Imtiaz", "Barkha", "Heer", "Ankur", "Disha"]
ARR = "; ".join(f"Floor {x}: " + ", ".join(f"{CN[c]} {at[x * 10 + c]}" for c in (1, 2, 3)) for x in (3, 2, 1))
sid = stimulus("puzzle", "Nine flats on three floors",
               "Nine persons Ankur, Barkha, Charan, Disha, Emon, Falak, Gaurang, Heer and Imtiaz live in a three-storey "
               "building, one in each flat. Floor 1 is the lowermost and floor 3 the topmost. Each floor has three "
               "flats in a line from west to east: West, Middle and East. Each flat is directly above the flat of the "
               "same name on the floor below.", conds,
               "Imtiaz has a flat above him (Ankur) and a flat below him (Emon), so Imtiaz must be in 2-Middle, Ankur "
               "in 3-Middle and Emon in 1-Middle. Barkha is in 2-East and Disha above her in 3-East. The West flats "
               "of all three floors and 1-East are left. Heer is directly above Charan in the West column, so they "
               "take 3-West/2-West or 2-West/1-West, and Falak takes the remaining West flat. Falak shares a floor "
               "with Gaurang, and the only non-West flat left is 1-East, so Falak = 1-West, Gaurang = 1-East, Charan "
               "= 2-West and Heer = 3-West.\n\n"
               + table(["Floor", "West", "Middle", "East"], [(x,) + tuple(at[x * 10 + c] for c in (1, 2, 3))
                                                            for x in (3, 2, 1)]))
ans = at[F3["Heer"] - 10]
assert ans == "Charan"
FQ = lambda text, correct, wrongs, concept, expl, steps, **kw: puzzle_q(
    sid, FLR, "Floor and flat", "Intermediate", text, correct, wrongs, concept, expl, steps, **kw)
FQ("Who lives in the flat directly below Heer's flat?", ans, ["Falak", "Imtiaz", "Ankur"],
   "Directly below = same column, one floor lower",
   "Heer lives in 3-West; directly below it is 2-West, Charan's flat.",
   ["Imtiaz has flats above and below him ⇒ 2-Middle", "Barkha 2-East, Disha 3-East, Ankur 3-Middle, Emon 1-Middle",
    "Falak shares a floor with Gaurang ⇒ floor 1 (only 1-East is free outside the West column)", ARR],
   why_others_wrong="Falak is two floors below Heer; Imtiaz is diagonally below her; Ankur is beside her.",
   seconds=75)
ans = at[F3["Imtiaz"] - 1]
assert ans == "Charan"
cnt = sum(1 for p in P if fl(F3[p]) > fl(F3["Gaurang"]) and col(F3[p]) == 3)
assert cnt == 2
FQ("How many persons live in East flats on floors above Gaurang's floor?", num_word(cnt), ["One", "Three", "None"],
   "Counting by column and floor", "Gaurang lives on floor 1. The East flats above are 2-East (Barkha) and 3-East "
   "(Disha): two persons.", [ARR], natural=by_num, seconds=60)
FQ("Who lives in the flat immediately to the west of Barkha's flat?", at[F3["Barkha"] - 1],
   ["Charan", "Disha", "Gaurang"], "Neighbours on the same floor",
   "Barkha lives in 2-East; the flat immediately to its west is 2-Middle, Imtiaz's.", [ARR],
   why_others_wrong="Charan is two flats west of Barkha; Disha is above her; Gaurang is on floor 1.", seconds=55)
assert at[F3["Barkha"] - 1] == "Imtiaz"
same = [p for p in P if p != "Emon" and fl(F3[p]) == fl(F3["Emon"])]
FQ("Which two persons live on the same floor as Emon?", " and ".join(sorted(same)),
   ["Charan and Barkha", "Falak and Heer", "Gaurang and Imtiaz"], "Grouping by floor",
   "Emon lives in 1-Middle; the other flats of floor 1 belong to Falak (West) and Gaurang (East).", [ARR],
   seconds=55)
assert sorted(same) == ["Falak", "Gaurang"]
stm = [
    ("Ankur lives directly above Imtiaz", F3["Ankur"] == F3["Imtiaz"] + 10),
    ("Heer lives on the same floor as Barkha", fl(F3["Heer"]) == fl(F3["Barkha"])),
    ("Disha lives in a Middle flat", col(F3["Disha"]) == 2),
    ("Charan lives on the lowermost floor", fl(F3["Charan"]) == 1),
]
t, f = one_true(stm)
FQ("Which of the following statements is true?", t, f, "Checking statements against the grid",
   "Ankur lives in 3-Middle, directly above Imtiaz's 2-Middle.",
   [ARR, "Ankur 3-Middle above Imtiaz 2-Middle: true", "Heer is on floor 3, Barkha on floor 2: false",
    "Disha lives in 3-East: false", "Charan lives on floor 2: false"], seconds=60)

# ---- F4 Intermediate: six floors, each person with a different age
P = ["Jayesh", "Kesar", "Lohit", "Madhu", "Nitin", "Pranali"]
AGES = [24, 27, 31, 35, 38, 42]
AV = [f"a{x}" for x in AGES]
conds = [
    ("The person aged 42 lives on floor 2.", ("a42",), lambda a: a == 2),
    ("Jayesh lives two floors above the person aged 42.", ("Jayesh", "a42"), lambda j, a: j == a + 2),
    ("Pranali lives immediately above Jayesh.", ("Pranali", "Jayesh"), lambda p, j: p == j + 1),
    ("The youngest person lives immediately below Jayesh.", ("a24", "Jayesh"), lambda y, j: y == j - 1),
    ("Jayesh is older than both the persons living above him.", ("Jayesh", "a24", "a27", "a31", "a35", "a38", "a42"),
     lambda j, *a: all(AGES[i] < next(AGES[k] for k in range(6) if a[k] == j) for i in range(6) if a[i] > j)),
    ("Lohit lives on the topmost floor and is older than Pranali.", ("Lohit", "Pranali", *AV),
     lambda l, p, *a: l == 6 and next(AGES[k] for k in range(6) if a[k] == l) >
     next(AGES[k] for k in range(6) if a[k] == p)),
    ("Madhu is 11 years younger than Kesar.", ("Madhu", "Kesar", *AV),
     lambda m, k, *a: next(AGES[i] for i in range(6) if a[i] == m) + 11 == next(AGES[i] for i in range(6) if a[i] == k)),
    ("Nitin lives above Madhu.", ("Nitin", "Madhu"), lambda n, m: n > m),
]
F4 = unique(AV + P, {x: range(1, 7) for x in AV + P}, conds, [P, AV])
age = {p: next(AGES[i] for i in range(6) if F4[AV[i]] == F4[p]) for p in P}
at = {F4[p]: p for p in P}
assert [(at[i], age[at[i]]) for i in range(1, 7)] == [("Madhu", 31), ("Kesar", 42), ("Nitin", 24), ("Jayesh", 38),
                                                      ("Pranali", 27), ("Lohit", 35)]
ARR = "Floor 1 to 6: " + ", ".join(f"{at[i]} ({age[at[i]]})" for i in range(1, 7))
sid = stimulus("puzzle", "Six floors and six ages",
               "Six persons Jayesh, Kesar, Lohit, Madhu, Nitin and Pranali live on the six floors of a building, one "
               "on each floor (floor 1 is the lowermost). Their ages, in years, are 24, 27, 31, 35, 38 and 42, one "
               "age each.", conds,
               "The 42-year-old is on floor 2, Jayesh on 4, Pranali on 5 and the 24-year-old on 3; Lohit is on 6. So "
               "Kesar, Madhu and Nitin share floors 1, 2 and 3, where floor 2 holds age 42 and floor 3 age 24. Ages 11 "
               "apart are 24–35, 27–38 and 31–42. Madhu 24 (floor 3) is impossible because Nitin must live above "
               "Madhu; Madhu 27 with Kesar 38 is impossible because only floor 1 has an age other than 42 and 24. So "
               "Kesar is 42 (floor 2) and Madhu 31 on floor 1, leaving floor 3 (24) for Nitin. Floors 4, 5 and 6 "
               "share 27, 35 and 38 with Jayesh older than Lohit and Pranali, and Lohit older than Pranali: Jayesh "
               "38, Lohit 35, Pranali 27.\n\n"
               + table(["Floor", "Person", "Age"], [(i, at[i], age[at[i]]) for i in range(6, 0, -1)]))
GQ = lambda text, correct, wrongs, concept, expl, steps, **kw: puzzle_q(
    sid, FLR, "Floor with attribute", "Intermediate", text, correct, wrongs, concept, expl, steps, **kw)
GQ("How old is the person who lives on floor 5?", f"{age[at[5]]} years", ["35 years", "24 years", "38 years"],
   "Ordering ages under 'older than' conditions",
   "Floors 4, 5 and 6 hold Jayesh, Pranali and Lohit with ages 27, 35 and 38, and Jayesh > Lohit > Pranali, so "
   "Pranali (floor 5) is 27.", ["42 → floor 2, Jayesh 4, Pranali 5, the 24-year-old 3, Lohit 6",
                                "Madhu 31 (floor 1) and Kesar 42 (floor 2); the other 11-year pairs do not fit", ARR],
   natural=lambda t: int(t.split()[0]), seconds=80)
assert age[at[5]] == 27
s16 = age[at[1]] + age[at[6]]
GQ("What is the sum of the ages of the persons on the lowermost and topmost floors?", f"{s16} years",
   ["69 years", "59 years", "73 years"], "Reading two attributes off the solved grid",
   f"Floor 1 is Madhu (31) and floor 6 Lohit (35): {s16} years.", [ARR, f"31 + 35 = {s16}"],
   natural=lambda t: int(t.split()[0]), seconds=70)
assert s16 == 66
older = sum(1 for p in P if age[p] > age["Madhu"])
GQ("How many persons are older than Madhu?", num_word(older), ["Two", "Four", "Five"], "Comparing ages",
   "Madhu is 31; Kesar (42), Jayesh (38) and Lohit (35) are older: three persons.", [ARR], natural=by_num, seconds=55)
assert older == 3
stm = [
    ("Nitin is the youngest of the six", age["Nitin"] == 24),
    ("Kesar lives immediately below Jayesh", F4["Kesar"] == F4["Jayesh"] - 1),
    ("Lohit is the oldest of the six", age["Lohit"] == 42),
    ("Pranali lives on an even-numbered floor", F4["Pranali"] % 2 == 0),
]
t, f = one_true(stm)
GQ("Which of the following statements is true?", t, f, "Checking statements against floors and ages",
   "Nitin lives on floor 3, which holds the youngest person (24).",
   [ARR, "Nitin, floor 3, age 24: true", "Below Jayesh (4) is Nitin, not Kesar: false",
    "The oldest (42) is Kesar: false", "Pranali lives on floor 5: false"], seconds=60)

# ---- F5 Advanced: five floors, two flats per floor (A west, B east), eight persons, two flats vacant
P = ["Ritesh", "Sneh", "Tulika", "Umang", "Varsha", "Wahid", "Yashvi", "Zoravar"]
FL10 = [f * 10 + c for f in range(1, 6) for c in (1, 2)]
FLN = {1: "A", 2: "B"}
IX = {p: i for i, p in enumerate(P)}
conds = [
    ("Tulika lives in flat B of an odd-numbered floor, and flat A of her floor is vacant.", tuple(P),
     lambda *v: col(v[IX["Tulika"]]) == 2 and fl(v[IX["Tulika"]]) % 2 == 1 and v[IX["Tulika"]] - 1 not in v),
    ("Ritesh lives directly above Tulika.", ("Ritesh", "Tulika"), lambda r, t_: r == t_ + 10),
    ("Umang lives on the same floor as Ritesh.", ("Umang", "Ritesh"), lambda u, r: fl(u) == fl(r)),
    ("Yashvi lives directly above Umang.", ("Yashvi", "Umang"), lambda y, u: y == u + 10),
    ("The flat directly above Ritesh's flat is vacant.", tuple(P),
     lambda *v: v[IX["Ritesh"]] + 10 <= 52 and v[IX["Ritesh"]] + 10 not in v),
    ("Sneh lives in flat B, two floors below Ritesh.", ("Sneh", "Ritesh"), lambda s, r: s == r - 20),
    ("Varsha lives in flat A on a floor below Zoravar's floor.", ("Varsha", "Zoravar"),
     lambda va, z: col(va) == 1 and fl(va) < fl(z)),
    ("Wahid lives on the lowermost floor.", ("Wahid",), lambda w: fl(w) == 1),
]
F5 = unique(P, {p: FL10 for p in P}, conds, [P])
at = {v: k for k, v in F5.items()}
cell = lambda s: at.get(s, "vacant")
assert [cell(s) for s in FL10] == ["Varsha", "Wahid", "Zoravar", "Sneh", "vacant", "Tulika", "Umang", "Ritesh",
                                   "Yashvi", "vacant"]
ARR = "; ".join(f"Floor {x}: A {cell(x * 10 + 1)}, B {cell(x * 10 + 2)}" for x in range(5, 0, -1))
sid = stimulus("puzzle", "Eight persons in ten flats",
               "A five-storey building has two flats on each floor: flat A to the west and flat B to the east, with "
               "each flat A directly above the flat A of the floor below (and likewise for B). Floor 1 is the "
               "lowermost. Eight persons Ritesh, Sneh, Tulika, Umang, Varsha, Wahid, Yashvi and Zoravar live in eight "
               "of the flats, one in each; two flats are vacant.", conds,
               "Tulika is in flat B of floor 1, 3 or 5. Floor 5 leaves no flat above her for Ritesh. Floor 1 puts "
               "Ritesh in 2-B, and Sneh would have to live two floors below floor 2: impossible. So Tulika = 3-B (3-A "
               "vacant), Ritesh = 4-B, 5-B vacant, Umang = 4-A, Yashvi = 5-A and Sneh = 2-B. That uses both vacant "
               "flats, so 1-A, 1-B and 2-A are occupied by Varsha, Wahid and Zoravar. Wahid is on floor 1; Varsha is "
               "in a flat A below Zoravar, so Varsha = 1-A, Zoravar = 2-A and Wahid = 1-B.\n\n"
               + table(["Floor", "Flat A (west)", "Flat B (east)"],
                       [(x, cell(x * 10 + 1), cell(x * 10 + 2)) for x in range(5, 0, -1)]))
HQ = lambda text, correct, wrongs, concept, expl, steps, **kw: puzzle_q(
    sid, FLR, "Floor and flat", "Advanced", text, correct, wrongs, concept, expl, steps, **kw)
ans = at[F5["Yashvi"] - 10]
assert ans == "Umang"
HQ("Who lives in the flat directly below Yashvi's flat?", ans, ["Ritesh", "Tulika", "Zoravar"],
   "Flats with vacancies: test the floor options for the anchor person",
   "Yashvi lives in 5-A, directly above Umang in 4-A.",
   ["Tulika = 5-B leaves no flat above for Ritesh; Tulika = 1-B leaves no flat two floors below Ritesh for Sneh",
    "So Tulika = 3-B, Ritesh = 4-B, Umang = 4-A, Yashvi = 5-A", ARR],
   why_others_wrong="Ritesh is diagonally below Yashvi (4-B); Tulika is in 3-B; Zoravar is in 2-A.", seconds=100)
nb_ = sum(1 for p in P if col(F5[p]) == 2)
assert nb_ == 4
HQ("How many persons live in B flats?", num_word(nb_), ["Three", "Five", "Two"], "Counting a column",
   "B flats: 1-B Wahid, 2-B Sneh, 3-B Tulika, 4-B Ritesh; 5-B is vacant. Four persons.", [ARR], natural=by_num,
   seconds=70)
stm = [
    ("Zoravar lives directly below a vacant flat", F5["Zoravar"] + 10 not in at),
    ("Sneh lives on the same floor as Varsha", fl(F5["Sneh"]) == fl(F5["Varsha"])),
    ("Both the vacant flats are on the same floor", len({fl(s) for s in FL10 if s not in at}) == 1),
    ("Wahid lives directly below Tulika", F5["Wahid"] == F5["Tulika"] - 10),
]
t, f = one_true(stm)
HQ("Which of the following statements is true?", t, f, "Checking statements that involve vacant flats",
   "Zoravar lives in 2-A, and the flat directly above, 3-A, is vacant.",
   [ARR, "Above 2-A is 3-A, vacant: true", "Sneh is on floor 2, Varsha on floor 1: false",
    "The vacant flats are 3-A and 5-B, on different floors: false",
    "Directly below Tulika (3-B) is Sneh (2-B), not Wahid: false"], seconds=80)

# ================================================================================================ BOX PUZZLES
BOX = "Box-Based Puzzles"

# ---- B1 Basic: two stacks of three boxes each (level 1 = bottom)
P = ["D", "F", "H", "J", "L", "N"]
ST = [s * 10 + lv for s in (1, 2) for lv in (1, 2, 3)]  # 1x = stack X, 2x = stack Y
sk, lv = (lambda s: s // 10), (lambda s: s % 10)
SKN = {1: "X", 2: "Y"}
conds = [
    ("Box J is in stack X.", ("J",), lambda j: sk(j) == 1),
    ("Box D is placed directly above box J.", ("D", "J"), lambda d, j: d == j + 1),
    ("Box H is at the top of the stack that does not contain box D.", ("H", "D"),
     lambda h, d: lv(h) == 3 and sk(h) != sk(d)),
    ("Box L is at the same level as box D, but in the other stack.", ("L", "D"),
     lambda l, d: lv(l) == lv(d) and sk(l) != sk(d)),
    ("Box F is placed below box L in the same stack.", ("F", "L"), lambda f_, l: sk(f_) == sk(l) and lv(f_) < lv(l)),
    ("Box N is not at the bottom of either stack.", ("N",), lambda n: lv(n) != 1),
]
B1 = unique(P, {p: ST for p in P}, conds, [P])
at = {v: k for k, v in B1.items()}
assert [at[s] for s in ST] == ["J", "D", "N", "F", "L", "H"]
ARR = ("Stack X, bottom to top: " + ", ".join(at[10 + i] for i in (1, 2, 3)) +
       "; Stack Y, bottom to top: " + ", ".join(at[20 + i] for i in (1, 2, 3)))
sid = stimulus("puzzle", "Six boxes in two stacks",
               "Six boxes D, F, H, J, L and N are kept in two stacks, X (on the left) and Y (on the right), with "
               "three boxes in each stack. Level 1 is the bottom of a stack and level 3 its top.", conds,
               "Box J is in stack X with D directly above it, so J and D are at levels 1–2 or 2–3 of stack X. L sits "
               "at D's level in stack Y, and H is at the top of stack Y. If D were at level 3, L would also be at "
               "level 3 of Y, which is H's place. So J = X1, D = X2 and L = Y2. F is below L: Y1. N takes the "
               "remaining place, X3 (not a bottom place).\n\n"
               + table(["Level", "Stack X", "Stack Y"], [(i, at[10 + i], at[20 + i]) for i in (3, 2, 1)]))
BQ = lambda text, correct, wrongs, concept, expl, steps, **kw: puzzle_q(
    sid, BOX, "Stacked boxes", "Basic", text, correct, wrongs, concept, expl, steps, **kw)
BQ("Which box is placed directly above box F?", at[B1["F"] + 1], ["H", "D", "N"], "Two stacks: work level by level",
   "F is at the bottom of stack Y, and directly above it is L.",
   ["D at level 3 would put L on H's place, so D = X2 and J = X1", "L = Y2, F = Y1, H = Y3, N = X3", ARR],
   why_others_wrong="H is two places above F; D and N are in stack X.", seconds=50)
assert at[B1["F"] + 1] == "L"
BQ("Which box is at the top of stack X?", at[13], ["H", "D", "L"], "Filling the last place",
   "Stack X holds J (bottom) and D (middle); the only box left, N, goes on top.", [ARR],
   why_others_wrong="H is at the top of stack Y.", seconds=45)
assert at[13] == "N"
BQ("Which box is at the same level as box N?", at[23], ["D", "L", "F"], "Comparing levels across stacks",
   "N is at level 3 of stack X; level 3 of stack Y is H.", [ARR], seconds=40)
above = 3 - lv(B1["J"])
BQ("How many boxes are placed above box J in its stack?", num_word(above), ["One", "Three", "None"],
   "Counting within one stack", "J is at the bottom of stack X, with D and N above it: two boxes.", [ARR],
   natural=by_num, seconds=40)
assert above == 2

# ---- B2 Intermediate: seven stacked boxes with different weights
P = ["B", "C", "E", "G", "I", "K", "M"]
WT = [10, 14, 17, 21, 25, 28, 32]
WV = [f"w{x}" for x in WT]
wof = lambda p, v: next(WT[i] for i in range(7) if v[i] == p)
conds = [
    ("Box G is the heaviest box and is placed third from the bottom.", ("G", "w32"), lambda g, w: g == 3 and w == g),
    ("Only two boxes are placed between box G and the lightest box.", ("G", "w10"), lambda g, w: abs(g - w) == 3),
    ("Box I is placed immediately above the lightest box and weighs 17 kg.", ("I", "w10", "w17"),
     lambda i, w, w17: i == w + 1 and w17 == i),
    ("Box K is placed at the bottom of the stack and weighs twice as much as box C.", ("K", "C", *WV),
     lambda k, c, *v: k == 1 and wof(k, v) == 2 * wof(c, v)),
    ("Box C is placed immediately above box K.", ("C", "K"), lambda c, k: c == k + 1),
    ("Box E is placed immediately above box M, and E is heavier than M.", ("E", "M", *WV),
     lambda e, m, *v: e == m + 1 and wof(e, v) > wof(m, v)),
]
B2 = unique(["G", "w32", "w10", "I", "w17", "K", "C", "B", "E", "M"] + [w for w in WV if w not in ("w32", "w10", "w17")],
            {x: range(1, 8) for x in P + WV}, conds, [P, WV])
at = {B2[p]: p for p in P}
wt = {p: wof(B2[p], [B2[w] for w in WV]) for p in P}
assert [(at[i], wt[at[i]]) for i in range(1, 8)] == [("K", 28), ("C", 14), ("G", 32), ("M", 21), ("E", 25),
                                                     ("B", 10), ("I", 17)]
ARR = "Bottom to top: " + ", ".join(f"{at[i]} ({wt[at[i]]} kg)" for i in range(1, 8))
sid = stimulus("puzzle", "Seven boxes and their weights",
               "Seven boxes B, C, E, G, I, K and M are placed one above another in a single stack. Their weights are "
               "10 kg, 14 kg, 17 kg, 21 kg, 25 kg, 28 kg and 32 kg, one weight per box.", conds,
               "G (32 kg) is third from the bottom, so the lightest box is three places from it: sixth from the "
               "bottom. I (17 kg) is seventh. K is at the bottom and C second. Among the weights left (10, 14, 21, 25, "
               "28) the only pair where one is twice the other is 14 and 28, so K = 28 kg and C = 14 kg. E sits "
               "immediately above M, so they take places 4 and 5 (if they took 5 and 6, E would be the lightest, yet "
               "heavier than M). B takes place 6 and is the lightest (10 kg). E is heavier than M: E = 25, M = 21.\n\n"
               + table(["Place from the bottom", "Box", "Weight"], [(i, at[i], f"{wt[at[i]]} kg")
                                                                     for i in range(7, 0, -1)]))
WQ = lambda text, correct, wrongs, concept, expl, steps, **kw: puzzle_q(
    sid, BOX, "Boxes with weights or colours", "Intermediate", text, correct, wrongs, concept, expl, steps, **kw)
WQ("What is the weight of the box placed immediately below box G?", f"{wt[at[B2['G'] - 1]]} kg",
   ["28 kg", "21 kg", "10 kg"], "Placing weights with a ratio condition",
   "Below G (third from the bottom) is C, the second box, which weighs 14 kg.",
   ["Lightest = 3 places from G = sixth; I (17 kg) = seventh", "K bottom, C second; 14 and 28 are the only "
    "double pair left ⇒ C 14, K 28", ARR], natural=lambda t: int(t.split()[0]), seconds=75)
assert wt[at[B2["G"] - 1]] == 14
hv = sum(1 for p in P if wt[p] > wt["E"])
WQ("How many boxes are heavier than box E?", num_word(hv), ["One", "Three", "Four"], "Comparing weights",
   "E weighs 25 kg; only G (32 kg) and K (28 kg) are heavier.", [ARR], natural=by_num, seconds=55)
assert hv == 2
s_ = wt[at[1]] + wt[at[7]]
WQ("What is the combined weight of the top box and the bottom box?", f"{s_} kg", ["38 kg", "49 kg", "42 kg"],
   "Reading weights at the two ends", f"Top: I (17 kg); bottom: K (28 kg). Total {s_} kg.", [ARR],
   natural=lambda t: int(t.split()[0]), seconds=55)
assert s_ == 45
WQ("Which box is placed second from the top?", at[6], ["E", "M", "I"], "Positions counted from the top",
   "The stack has seven boxes, so second from the top is sixth from the bottom: B, the lightest box.", [ARR],
   why_others_wrong="I is at the top; E and M are fifth and fourth from the bottom.", seconds=50)
assert at[6] == "B"

# ---- B3 Advanced: a stack with an unknown number of boxes
P = ["R", "S", "T", "U", "V", "W", "X", "Y"]
V = ["n", "T", "W", "V", "R", "S", "U", "X", "Y"]
conds = [
    ("Box T is placed fifth from the bottom.", ("T",), lambda t_: t_ == 5),
    ("Only three boxes are placed between box T and box W.", ("T", "W"), lambda t_, w: abs(t_ - w) == 4),
    ("Box V is placed immediately below box W.", ("V", "W"), lambda v, w: v == w - 1),
    ("As many boxes are placed above box W as below box T.", ("n", "W", "T"), lambda n, w, t_: n - w == t_ - 1),
    ("Box R is placed exactly in the middle of the stack.", ("n", "R"), lambda n, r: n % 2 == 1 and r == (n + 1) // 2),
    ("Only two boxes are placed between box R and box S, and S is placed above V.", ("R", "S", "V"),
     lambda r, s, v: abs(r - s) == 3 and s > v),
    ("Only one box is placed between box U and box S, and U is not at the top of the stack.", ("n", "U", "S"),
     lambda n, u, s: abs(u - s) == 2 and u != n),
    ("Box X is at the top of the stack, and box Y is placed second from the bottom.", ("n", "X", "Y"),
     lambda n, x, y: x == n and y == 2),
]
B3 = unique(V, {"n": range(8, 41)} | {p: range(1, 41) for p in P},
            conds + [("(within the stack)", tuple(V), lambda n, *v: max(v) <= n)], [P])
NB = B3["n"]
assert NB == 13 and [B3[p] for p in P] == [7, 10, 5, 12, 8, 9, 13, 2]
ARR = f"{NB} boxes; from the bottom: " + ", ".join(f"{p} {B3[p]}" for p in sorted(P, key=B3.get))
sid = stimulus("puzzle", "A stack of unknown size",
               "Some boxes are placed one above another in a single stack. The number of boxes is not given. Boxes R, "
               "S, T, U, V, W, X and Y are among them; the other boxes are unnamed.", conds,
               "Number places from the bottom. T = 5, so W = 9 or 1; V is immediately below W, so W = 9 and V = 8. "
               "Four boxes are below T, so four are above W: the stack has 9 + 4 = 13 boxes. R is in the middle, "
               "7th. S is three places from R (4 or 10) and above V (8), so S = 10. U is two places from S (8 or 12); "
               "8 is V's place, so U = 12, which is not the top. X = 13 and Y = 2.\n\n"
               + table(["Place from the bottom", "Box"], [(B3[p], p) for p in sorted(P, key=B3.get, reverse=True)])
               + "\n\nThe other places hold unnamed boxes.")
XQ = lambda text, correct, wrongs, concept, expl, steps, **kw: puzzle_q(
    sid, BOX, "Stacked boxes", "Advanced", text, correct, wrongs, concept, expl, steps, **kw)
XQ("How many boxes are there in the stack?", str(NB), ["12", "14", "15"], "Fixing the stack size",
   "W must be 9th (V is directly below it), and there are four boxes below T, hence four above W: 9 + 4 = 13.",
   ["T = 5; W = 5 ± 4 → 9 (1 leaves no place for V)", "Below T: 4 boxes ⇒ above W: 4 boxes", "Total = 13"],
   natural=int, seconds=90)
gap = B3["R"] - B3["Y"] - 1
XQ("How many boxes are placed between box Y and box R?", str(gap), ["3", "5", "6"], "Counting with unnamed boxes",
   f"Y is 2nd and R 7th from the bottom, so {gap} boxes lie between them.", [ARR], natural=int, seconds=70)
assert gap == 4
ft = NB - B3["S"] + 1
XQ("What is the position of box S from the top of the stack?", ORDN(ft), ["3rd", "5th", "10th"],
   "Converting a bottom position to a top position", f"S is 10th from the bottom of 13 boxes: 13 − 10 + 1 = {ft}th "
   "from the top.", [ARR, "S = 10 (4 would be below V)", f"From the top: {ft}"],
   why_others_wrong="10th is S's place from the bottom.", natural=lambda t: int(t[:-2]), seconds=70)
assert ft == 4
gap = B3["U"] - B3["V"] - 1
above_w = next(p for p in P if B3[p] == B3["W"] + 1)
assert above_w == "S" and gap == 3
XQ("Which box is placed immediately above box W?", above_w, ["U", "V", "X"], "Reading a neighbour in the stack",
   "W is 9th from the bottom and S is 10th, so S sits immediately above W.", [ARR],
   why_others_wrong="V is immediately below W; U is 12th and X 13th (the top).", seconds=60)
stm = [
    ("Box R is placed immediately above box T", B3["R"] == B3["T"] + 1),
    ("Box U is placed immediately below box X", B3["U"] == B3["X"] - 1),
    ("Box W is placed immediately above box S", B3["W"] == B3["S"] + 1),
    ("Exactly five boxes are placed above box W", B3["n"] - B3["W"] == 5),
]
t, f = one_true(stm)
XQ("Which of the following statements is true?", t, f, "Checking statements in a stack of unknown size",
   "U is 12th and X 13th (the top), so U is immediately below X.",
   [ARR, "U (12) is immediately below X (13): true", "R is 7th and T 5th, with an unnamed box between: false",
    "W (9) is below S (10), not above it: false", "Above W (9) there are 13 − 9 = 4 boxes, not 5: false"],
   seconds=70)

# ================================================================================================ MONTH / DATE / YEAR
MON = "Month and Date-Based Puzzles"
MNAME = ["", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
         "November", "December"]
MDAYS = {m: (dt.date(2026 + (m == 12), m % 12 + 1, 1) - dt.date(2026, m, 1)).days for m in range(1, 13)}
assert MDAYS[2] == 28 and MDAYS[4] == 30 and MDAYS[12] == 31

# ---- M1 Basic: seven trainings, one in each month from March to September
P = ["Akhil", "Bhargavi", "Chetas", "Dipti", "Ehsan", "Firoza", "Gautam"]
conds = [
    ("Akhil's training is in a month that has 31 days.", ("Akhil",), lambda a: MDAYS[a] == 31),
    ("Chetas's training is in a month after Akhil's, and only one person's training is between theirs.",
     ("Chetas", "Akhil"), lambda c, a: c == a + 2),
    ("Firoza's training is in the month immediately before Chetas's.", ("Firoza", "Chetas"), lambda f_, c: f_ == c - 1),
    ("Bhargavi's training is in the month immediately after Chetas's.", ("Bhargavi", "Chetas"),
     lambda b, c: b == c + 1),
    ("Ehsan's training is in a month that has 30 days, after Bhargavi's.", ("Ehsan", "Bhargavi"),
     lambda e, b: MDAYS[e] == 30 and e > b),
    ("Gautam's training is in a month that has 30 days.", ("Gautam",), lambda g: MDAYS[g] == 30),
    ("Dipti's training is in a month before Gautam's.", ("Dipti", "Gautam"), lambda d, g: d < g),
]
M1 = unique(P, {p: range(3, 10) for p in P}, conds, [P])
at = {v: k for k, v in M1.items()}
assert [at[m] for m in range(3, 10)] == ["Dipti", "Gautam", "Akhil", "Firoza", "Chetas", "Bhargavi", "Ehsan"]
ARR = "March to September: " + ", ".join(at[m] for m in range(3, 10))
sid = stimulus("puzzle", "Seven trainings from March to September",
               "Seven employees Akhil, Bhargavi, Chetas, Dipti, Ehsan, Firoza and Gautam attend a training "
               "programme, one in each month from March to September of the same year.", conds,
               "Akhil, Firoza, Chetas and Bhargavi take four consecutive months, with Akhil's month having 31 days, "
               "and Ehsan comes later in a 30-day month. Akhil in July or August leaves no room. Akhil in March gives "
               "Firoza April, Chetas May, Bhargavi June and Ehsan September; Dipti and Gautam would take July and "
               "August, but Gautam's month must have 30 days: rejected. So Akhil = May, Firoza = June, Chetas = July, "
               "Bhargavi = August, Ehsan = September, and Gautam (30 days, after Dipti) = April, Dipti = March.\n\n"
               + table(["Month", "Employee"], [(MNAME[m], at[m]) for m in range(3, 10)]))
MQ = lambda text, correct, wrongs, concept, expl, steps, **kw: puzzle_q(
    sid, MON, "Month-based", "Basic", text, correct, wrongs, concept, expl, steps, **kw)
ans = at[M1["Gautam"] + 1]
MQ("Whose training is in the month immediately after Gautam's?", ans, ["Dipti", "Firoza", "Chetas"],
   "Month puzzle: use the number of days in each month",
   "Gautam's training is in April, and May belongs to Akhil.",
   ["Akhil = March fails (Gautam would need a 31-day month)", ARR, "After April: May = Akhil"],
   why_others_wrong="Dipti is in March (before Gautam); Firoza and Chetas are in June and July.", seconds=55)
assert ans == "Akhil"
gap = M1["Firoza"] - M1["Dipti"] - 1
MQ("How many persons have their training between Dipti's and Firoza's?", num_word(gap), ["One", "Three", "Four"],
   "Counting months between", "Dipti is in March and Firoza in June; Gautam (April) and Akhil (May) come between.",
   [ARR], natural=by_num, seconds=45)
assert gap == 2
thirty = [at[m] for m in range(3, 10) if MDAYS[m] == 30]
MQ("Whose trainings are in months that have 30 days?", ", ".join(thirty[:-1]) + " and " + thirty[-1],
   ["Gautam, Chetas and Ehsan", "Dipti, Firoza and Ehsan", "Gautam, Firoza and Bhargavi"],
   "Months with 30 days: April, June, September (and November)",
   "Between March and September the 30-day months are April, June and September: Gautam, Firoza and Ehsan.", [ARR],
   seconds=45)
assert thirty == ["Gautam", "Firoza", "Ehsan"]

# ---- M2 Basic: six visits on six dates of the same month
P = ["Harshad", "Ishita", "Jairaj", "Kalyani", "Lavesh", "Meghna"]
DT = [3, 8, 12, 17, 23, 28]
conds = [
    ("Ishita visits on an odd-numbered date after the 12th.", ("Ishita",), lambda i: DT[i] % 2 == 1 and DT[i] > 12),
    ("Only one person visits between Ishita and Jairaj.", ("Ishita", "Jairaj"), lambda i, j: abs(i - j) == 2),
    ("Lavesh visits on the date immediately after Ishita's (no one visits between them).", ("Lavesh", "Ishita"),
     lambda l, i: l == i + 1),
    ("Harshad visits on an even-numbered date, before Meghna.", ("Harshad", "Meghna"),
     lambda h, m: DT[h] % 2 == 0 and h < m),
    ("Kalyani visits before Harshad.", ("Kalyani", "Harshad"), lambda k, h: k < h),
    ("Meghna visits on a date that is a multiple of 4, and before Jairaj.", ("Meghna", "Jairaj"),
     lambda m, j: DT[m] % 4 == 0 and m < j),
]
M2 = unique(P, {p: range(6) for p in P}, conds, [P])
at = {v: k for k, v in M2.items()}
assert [at[i] for i in range(6)] == ["Kalyani", "Harshad", "Meghna", "Ishita", "Lavesh", "Jairaj"]
ARR = "In date order: " + ", ".join(f"{DT[i]} July – {at[i]}" for i in range(6))
sid = stimulus("puzzle", "Six visits on six dates of July",
               "Six persons Harshad, Ishita, Jairaj, Kalyani, Lavesh and Meghna visit a bank branch on six different "
               "dates of July: the 3rd, 8th, 12th, 17th, 23rd and 28th. Each person visits once.", conds,
               "Ishita visits on the 17th or the 23rd, with Lavesh on the next date of the list. If Ishita = 23rd, "
               "Lavesh = 28th and Jairaj = 12th; Meghna must be before Jairaj on a multiple of 4, i.e. the 8th, and "
               "Harshad before her on an even date: impossible (only the 3rd is earlier). So Ishita = 17th and Lavesh "
               "= 23rd, and Jairaj, two dates away from Ishita, is on the 8th or the 28th. Meghna (a multiple of 4) "
               "must come before Jairaj, which rules out the 8th, so Jairaj = 28th. Kalyani, Harshad and Meghna take "
               "the 3rd, 8th and 12th in that order (Kalyani before Harshad before Meghna).\n\n" + table(["Date (July)", "Person"], [(DT[i], at[i]) for i in range(6)]))
DQ = lambda text, correct, wrongs, concept, expl, steps, **kw: puzzle_q(
    sid, MON, "Date-based", "Basic", text, correct, wrongs, concept, expl, steps, **kw)
DQ("Who visits on 12 July?", at[2], ["Harshad", "Jairaj", "Kalyani"], "Date puzzle: eliminate cases",
   "Ishita must be on the 17th, Lavesh on the 23rd; Kalyani, Harshad and Meghna take the 3rd, 8th and 12th in that "
   "order, so Meghna visits on the 12th.",
   ["Ishita = 23rd leaves no even date before Meghna (8th) for Harshad: rejected",
    "Ishita 17th, Lavesh 23rd, Jairaj 28th", ARR], seconds=50)
assert at[2] == "Meghna"
gap = M2["Lavesh"] - M2["Harshad"] - 1
DQ("How many persons visit between Harshad and Lavesh?", num_word(gap), ["One", "Three", "None"],
   "Counting visits between two dates", "Harshad visits on the 8th and Lavesh on the 23rd; Meghna (12th) and Ishita "
   "(17th) visit in between.", [ARR], natural=by_num, seconds=45)
assert gap == 2
DQ("On which date does Lavesh visit?", f"{DT[M2['Lavesh']]} July", ["17 July", "28 July", "12 July"],
   "Reading the date", "Lavesh visits on the date right after Ishita's (17th): the 23rd.", [ARR],
   natural=lambda t: int(t.split()[0]), seconds=40)
assert DT[M2["Lavesh"]] == 23

# ---- M3 Intermediate: six persons born in six of the twelve months
P = ["Neeraj", "Ovi", "Pramod", "Ruchi", "Sumit", "Tanisha"]
conds = [
    ("Neeraj was born in a month that has 30 days.", ("Neeraj",), lambda n: MDAYS[n] == 30),
    ("Tanisha was born in the month immediately after Neeraj's month.", ("Tanisha", "Neeraj"),
     lambda t_, n: t_ == n + 1),
    ("Pramod was born after Tanisha, and exactly two months lie between their months.", ("Pramod", "Tanisha"),
     lambda p, t_: p == t_ + 3),
    ("Ovi was born after Pramod, and exactly one month lies between their months.", ("Ovi", "Pramod"),
     lambda o, p: o == p + 2),
    ("Sumit was born in a month that has 31 days, after Ovi's month.", ("Sumit", "Ovi"),
     lambda s, o: MDAYS[s] == 31 and s > o),
    ("Ruchi was born in the shortest month of the year.", ("Ruchi",), lambda r: r == 2),
]
M3 = unique(["Neeraj", "Tanisha", "Pramod", "Ovi", "Sumit", "Ruchi"], {p: range(1, 13) for p in P}, conds, [P])
at = {v: k for k, v in M3.items()}
assert [(m, at[m]) for m in sorted(at)] == [(2, "Ruchi"), (4, "Neeraj"), (5, "Tanisha"), (8, "Pramod"), (10, "Ovi"),
                                            (12, "Sumit")]
ARR = "; ".join(f"{MNAME[m]}: {at.get(m, '—')}" for m in range(1, 13))
sid = stimulus("puzzle", "Six birthdays in twelve months",
               "Six friends Neeraj, Ovi, Pramod, Ruchi, Sumit and Tanisha were born in six different months of the "
               "same year (not a leap year). In each of the other six months none of them was born.", conds,
               "Neeraj's month has 30 days: April, June, September or November. Tanisha is the next month, Pramod "
               "three months after Tanisha and Ovi two months after Pramod. From September or November the chain "
               "runs past December. From June: Tanisha July, Pramod October, Ovi December, and Sumit (31 days, after "
               "Ovi) has no month left. So Neeraj = April, Tanisha = May, Pramod = August, Ovi = October and Sumit = "
               "December (the only 31-day month after October). Ruchi = February.\n\n"
               + table(["Month", "Born"], [(MNAME[m], at.get(m, "—")) for m in range(1, 13)]))
YQ = lambda text, correct, wrongs, concept, expl, steps, **kw: puzzle_q(
    sid, MON, "Month-based", "Intermediate", text, correct, wrongs, concept, expl, steps, **kw)
YQ("Who was born in October?", at[10], ["Pramod", "Sumit", "Tanisha"], "Testing each possible starting month",
   "Neeraj = June leaves no 31-day month after Ovi (December) for Sumit, so Neeraj = April and the chain gives Ovi "
   "October.", ["Neeraj ∈ {April, June, September, November}", "September/November: chain runs past December",
                "June: Ovi = December, no month for Sumit", ARR], seconds=75)
assert at[10] == "Ovi"
empty = 12 - len(P)
cnt = sum(1 for m in range(M3["Neeraj"] + 1, M3["Sumit"]) if m not in at)
YQ("In how many months between Neeraj's month and Sumit's month was none of the six born?", num_word(cnt),
   ["Three", "Five", "Six"], "Counting empty months in a range",
   "Between April and December lie May to November (7 months). Tanisha (May), Pramod (August) and Ovi (October) "
   "were born in three of them, so four are empty: June, July, September and November.", [ARR], natural=by_num,
   seconds=65)
assert cnt == 4
gap = sum(1 for p in P if M3["Ruchi"] < M3[p] < M3["Pramod"])
YQ("How many of the six were born after Ruchi but before Pramod?", num_word(gap), ["One", "Three", "Four"],
   "Ordering birthdays", "Ruchi is February and Pramod August; Neeraj (April) and Tanisha (May) fall between.", [ARR],
   natural=by_num, seconds=55)
assert gap == 2
stm = [
    ("Exactly one month lies between Ruchi's and Neeraj's months", M3["Neeraj"] - M3["Ruchi"] == 2),
    ("Sumit was born in November", M3["Sumit"] == 11),
    ("Tanisha was born in a month with 30 days", MDAYS[M3["Tanisha"]] == 30),
    ("Pramod was born in the month immediately before Ovi's", M3["Ovi"] == M3["Pramod"] + 1),
]
t, f = one_true(stm)
YQ("Which of the following statements is true?", t, f, "Checking statements against the calendar",
   "Ruchi (February) and Neeraj (April) have only March between them.",
   [ARR, "February and April: one month (March) between: true", "Sumit was born in December: false",
    "May has 31 days: false", "September lies between August and October: false"], seconds=60)

# ---- M4 Intermediate: joining years and departments
P = ["Vasudha", "Waqar", "Yamuna", "Zeeshan", "Aniket", "Bhumika"]
YR = [2013, 2015, 2018, 2019, 2022, 2024]
DP = ["Audit", "Credit", "HR", "IT", "Retail", "Treasury"]
conds = [
    ("Vasudha joined in an even-numbered year and works in Credit.", ("Vasudha", "Credit"),
     lambda v, c: YR[v] % 2 == 0 and v == c),
    ("The person who works in HR joined exactly one year after Vasudha.", ("HR", "Vasudha"),
     lambda h, v: YR[h] == YR[v] + 1),
    ("Zeeshan works in HR.", ("Zeeshan", "HR"), lambda z, h: z == h),
    ("Aniket joined exactly nine years after Bhumika.", ("Aniket", "Bhumika"), lambda a, b: YR[a] == YR[b] + 9),
    ("The person who works in Treasury joined most recently.", ("Treasury",), lambda t_: t_ == 5),
    ("Yamuna joined after Zeeshan but before Aniket.", ("Yamuna", "Zeeshan", "Aniket"), lambda y, z, a: z < y < a),
    ("The person who works in Audit joined earliest.", ("Audit",), lambda a: a == 0),
    ("Bhumika does not work in Retail.", ("Bhumika", "Retail"), lambda b, r: b != r),
]
M4 = unique(P + DP, {x: range(6) for x in P + DP}, conds, [P, DP])
dept = {p: next(d for d in DP if M4[d] == M4[p]) for p in P}
yr = {p: YR[M4[p]] for p in P}
assert yr == {"Vasudha": 2018, "Waqar": 2013, "Yamuna": 2022, "Zeeshan": 2019, "Aniket": 2024, "Bhumika": 2015}
assert dept == {"Vasudha": "Credit", "Waqar": "Audit", "Yamuna": "Retail", "Zeeshan": "HR", "Aniket": "Treasury",
                "Bhumika": "IT"}
order_ = sorted(P, key=yr.get)
ARR = "; ".join(f"{yr[p]}: {p} ({dept[p]})" for p in order_)
sid = stimulus("puzzle", "Six officers and their joining years",
               "Six officers Vasudha, Waqar, Yamuna, Zeeshan, Aniket and Bhumika joined a bank in six different years "
               "among 2013, 2015, 2018, 2019, 2022 and 2024. Each works in a different department among Audit, Credit, "
               "HR, IT, Retail and Treasury.", conds,
               "The only two listed years one year apart are 2018 and 2019, so Vasudha (even year, Credit) joined in "
               "2018 and Zeeshan (HR) in 2019. Nine-year gaps: 2013–2022 and 2015–2024. If Bhumika = 2013 and Aniket "
               "= 2022, Yamuna must join after 2019 and before 2022, which no listed year allows. So Bhumika = 2015, "
               "Aniket = 2024 (Treasury, the latest year), Yamuna = 2022 and Waqar = 2013 (Audit, the earliest). IT "
               "and Retail remain for Bhumika and Yamuna; Bhumika is not in Retail, so Bhumika = IT and Yamuna = "
               "Retail.\n\n" + table(["Year", "Officer", "Department"], [(yr[p], p, dept[p]) for p in order_]))
JQ = lambda text, correct, wrongs, concept, expl, steps, **kw: puzzle_q(
    sid, MON, "Year-based", "Intermediate", text, correct, wrongs, concept, expl, steps, **kw)
JQ("Who works in IT?", "Bhumika", ["Yamuna", "Waqar", "Aniket"], "Year gaps that fit only one pair",
   "Bhumika joined in 2015; of IT and Retail, the two departments left for her and Yamuna, she cannot take Retail.",
   ["2018–2019 is the only one-year gap ⇒ Vasudha 2018, Zeeshan 2019",
    "Bhumika 2013 / Aniket 2022 leaves no year for Yamuna ⇒ Bhumika 2015, Aniket 2024", ARR], seconds=80)
JQ("In which year did Yamuna join?", str(yr["Yamuna"]), ["2019", "2015", "2024"], "Between two fixed years",
   "Yamuna joined after Zeeshan (2019) and before Aniket (2024); the only listed year in between is 2022.", [ARR],
   natural=int, seconds=60)
d_ = yr["Zeeshan"] - yr["Waqar"]
JQ("How many years after Waqar did Zeeshan join?", f"{d_} years", ["4 years", "5 years", "9 years"],
   "Year arithmetic", f"Waqar joined in 2013 and Zeeshan in 2019: {d_} years later.", [ARR],
   natural=lambda t: int(t.split()[0]), seconds=55)
assert d_ == 6
stm = [
    ("The officer in Treasury joined nine years after the officer in IT", yr["Aniket"] - yr["Bhumika"] == 9),
    ("Waqar works in Retail", dept["Waqar"] == "Retail"),
    ("The officer in Credit joined after the officer in HR", yr["Vasudha"] > yr["Zeeshan"]),
    ("Yamuna joined in an odd-numbered year", yr["Yamuna"] % 2 == 1),
]
t, f = one_true(stm)
JQ("Which of the following statements is true?", t, f, "Linking two attributes through the year",
   "Treasury is Aniket (2024) and IT is Bhumika (2015): nine years apart.",
   [ARR, "Aniket (Treasury) 2024 − Bhumika (IT) 2015 = 9: true", "Waqar works in Audit: false",
    "Credit (2018) joined before HR (2019): false", "Yamuna joined in 2022: false"], seconds=65)

# ---- M5, M6 Advanced (standalone): calendar dates and birth years
APR = {d_: dt.date(2026, 4, d_) for d_ in range(1, 31)}
TF = [d_ for d_ in APR if APR[d_].weekday() in (3, 4)]  # Thursdays and Fridays of April 2026
week = lambda d_: APR[d_].isocalendar()[1]
assert APR[1].strftime("%A") == "Wednesday" and TF == [2, 3, 9, 10, 16, 17, 23, 24, 30]
P = ["Nitya", "Omkar", "Pihu", "Rehan", "Sia"]
conds = [
    ("Every appointment is on a Thursday or a Friday, and no two appointments fall in the same Monday-to-Sunday "
     "week.", tuple(P), lambda *v: len({week(x) for x in v}) == 5),
    ("Nitya's appointment is on a date that is a perfect square.", ("Nitya",), lambda n: n in (1, 4, 9, 16, 25)),
    ("Omkar's appointment is exactly 15 days after Nitya's.", ("Omkar", "Nitya"), lambda o, n: o == n + 15),
    ("Pihu's appointment is on a Friday, earlier than Nitya's.", ("Pihu", "Nitya"),
     lambda p, n: APR[p].weekday() == 4 and p < n),
    ("Rehan's appointment is on an odd-numbered date.", ("Rehan",), lambda r: r % 2 == 1),
]
M5 = unique(["Nitya", "Omkar", "Pihu", "Rehan", "Sia"], {p: TF for p in P}, conds, [P])
assert M5 == {"Nitya": 9, "Omkar": 24, "Pihu": 3, "Rehan": 17, "Sia": 30}
mcq(MON, "Date-based", "Advanced",
    "Five persons Nitya, Omkar, Pihu, Rehan and Sia each have one appointment at a bank in April 2026, on five "
    "different dates. 1 April 2026 is a Wednesday.\n" + bullets(conds) + "\n\nOn which date is Sia's appointment?",
    "30 April", ["23 April", "16 April", "24 April"], "Calendar puzzle: list the allowed dates first",
    "With 1 April a Wednesday, the Thursdays and Fridays are 2, 3, 9, 10, 16, 17, 23, 24 and 30 April, in five weeks: "
    "(2, 3), (9, 10), (16, 17), (23, 24) and (30). Each person takes a different week. Nitya's date is a perfect "
    "square: 9 or 16; 15 days later gives 24 (a Friday) or 31 (not in April), so Nitya = 9 and Omkar = 24. Pihu's "
    "Friday is before the 9th: the 3rd. The weeks left are (16, 17) and (30); Rehan's date is odd, so Rehan = 17 and "
    "Sia = 30 April.",
    ["Thursdays/Fridays: 2, 3 | 9, 10 | 16, 17 | 23, 24 | 30 (one week each)",
     "Nitya ∈ {9, 16}; Omkar = Nitya + 15 must be in April and a Thursday/Friday ⇒ Nitya 9, Omkar 24",
     "Pihu: a Friday before the 9th ⇒ 3", "Remaining weeks (16, 17) and (30): Rehan odd ⇒ 17", "Sia = 30 April"],
    why_others_wrong="23 April is in Omkar's week; 16 April is in Rehan's week; 24 April is Omkar's date.",
    natural=lambda t: int(t.split()[0]), seconds=120, verified_by=BRUTE)
P = ["Kavin", "Lipika", "Mayur", "Nalini"]
leap = lambda y: y % 4 == 0 and (y % 100 != 0 or y % 400 == 0)
YRS = range(1985, 2006)
conds = [
    ("In 2026, Kavin's age in completed years is a perfect square.", ("Kavin",),
     lambda k: round((2026 - k) ** 0.5) ** 2 == 2026 - k),
    ("Lipika was born exactly 12 years before Kavin.", ("Lipika", "Kavin"), lambda l, k: l == k - 12),
    ("Mayur was born in a leap year, after Lipika but before Kavin.", ("Mayur", "Lipika", "Kavin"),
     lambda m, l, k: leap(m) and l < m < k),
    ("Nalini is older than Lipika, and the digits of Nalini's birth year add up to 25.", ("Nalini", "Lipika"),
     lambda n, l: n < l and sum(map(int, str(n))) == 25),
    ("In 2026, Mayur's age in completed years is a multiple of 10.", ("Mayur",), lambda m: (2026 - m) % 10 == 0),
]
M6 = unique(["Kavin", "Lipika", "Mayur", "Nalini"], {p: YRS for p in P}, conds, [P])
assert M6 == {"Kavin": 2001, "Lipika": 1989, "Mayur": 1996, "Nalini": 1987}
d_ = M6["Mayur"] - M6["Nalini"]
mcq(MON, "Year-based", "Advanced",
    "Four friends Kavin, Lipika, Mayur and Nalini were born in four different years from 1985 to 2005. Ages are "
    "counted in completed years on their birthdays in 2026.\n" + bullets(conds) +
    "\n\nHow many years older than Mayur is Nalini?", f"{d_} years", ["7 years", "11 years", "13 years"],
    "Year puzzle: perfect squares, leap years and digit sums",
    "Kavin's 2026 age must be a perfect square: 25 (born 2001) or 36 (born 1990). Lipika is 12 years older, born 1989 "
    "or 1978; 1978 is outside the range, so Kavin = 2001 and Lipika = 1989. Mayur was born in a leap year between "
    "1989 and 2001 (1992, 1996 or 2000) and is 34, 30 or 26 in 2026; only 30 is a multiple of 10, so Mayur = 1996. "
    "Nalini was born between 1985 and 1988 with digit sum 25: 1987. 1996 − 1987 = 9 years.",
    ["Kavin: age 25 (2001) or 36 (1990)", "Lipika = Kavin − 12 ⇒ 1989 (1978 is out of range) ⇒ Kavin 2001",
     "Mayur: leap year in 1990–2000 ⇒ 1992/1996/2000; age 30 ⇒ 1996",
     "Nalini: 1985–1988 with digit sum 25 ⇒ 1987 (1+9+8+7)", "Difference: 1996 − 1987 = 9"],
    why_others_wrong="7 years is Mayur − Lipika; 11 and 13 come from taking Mayur as 1998 or 2000.",
    natural=lambda t: int(t.split()[0]), seconds=120, verified_by=BRUTE)
assert d_ == 9 and M6["Mayur"] - M6["Lipika"] == 7

# ================================================================================================ PUZZLES (OTHER)
OTH = "Puzzles (Other)"
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
P = ["Ujjwal", "Vrinda", "Wamika", "Xavier", "Yusuf", "Ziva"]
IX = {p: i for i, p in enumerate(P)}
conds = [("Xavier visits on Wednesday.", ("Xavier",), lambda x: x == 2),
         ("Vrinda visits two days after Xavier.", ("Vrinda", "Xavier"), lambda v, x: v == x + 2),
         ("Nobody visits on the day immediately after Vrinda's day.", tuple(P),
          lambda *v: v[IX["Vrinda"]] + 1 < 7 and v[IX["Vrinda"]] + 1 not in v),
         ("Ziva visits on the day immediately before Xavier.", ("Ziva", "Xavier"), lambda z, x: z == x - 1),
         ("Yusuf visits on a day after Ujjwal and after Wamika.", ("Yusuf", "Ujjwal", "Wamika"),
          lambda y, u, w: y > u and y > w),
         ("Wamika does not visit on Monday.", ("Wamika",), lambda w: w != 0)]
O1 = unique(P, {p: range(7) for p in P}, conds, [P])
at = {v: k for k, v in O1.items()}
assert [at.get(i, "-") for i in range(7)] == ["Ujjwal", "Ziva", "Xavier", "Wamika", "Vrinda", "-", "Yusuf"]
mcq(OTH, "Day-based", "Basic",
    "Six persons Ujjwal, Vrinda, Wamika, Xavier, Yusuf and Ziva visit a library on six different days of the same "
    "week (Monday to Sunday), one person per day; on the remaining day nobody visits.\n" + bullets(conds) +
    "\n\nWho visits on Sunday?", at[6], ["Wamika", "Ujjwal", "Vrinda"], "Day puzzle with one empty day",
    "Xavier = Wednesday, Vrinda = Friday, Saturday is empty and Ziva = Tuesday. Monday, Thursday and Sunday remain "
    "for Ujjwal, Wamika and Yusuf. Yusuf comes after both others, so he takes Sunday; Wamika cannot take Monday, so "
    "Wamika = Thursday and Ujjwal = Monday.",
    ["Xavier Wed → Vrinda Fri → Saturday empty", "Ziva Tue", "Free: Mon, Thu, Sun for Ujjwal, Wamika, Yusuf",
     "Yusuf after both ⇒ Sunday; Wamika not Monday ⇒ Thursday; Ujjwal Monday"],
    why_others_wrong="Wamika visits on Thursday, Ujjwal on Monday and Vrinda on Friday.", seconds=45,
    verified_by=BRUTE)

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

# ================================================================================================ SYLLOGISM
TWO, FEW, POSS = "Two-statement", "Only a few / Only", "Possibility cases"
# ---- Basic (two statements)
syl_q("Basic", TWO, N(("cup", "cups"), ("plate", "plates"), ("bowl", "bowls")),
      [("all", "cup", "plate"), ("no", "plate", "bowl")],
      [("no", "cup", "bowl"), ("some", "bowl", "cup")], ONLY_I,
      "All + No = No (first term to third term)",
      "Every cup is a plate and no plate is a bowl, so no cup can be a bowl (I follows). II says the opposite of I, "
      "so it cannot follow.",
      ["All cups ⊂ plates; plates and bowls do not overlap", "So cups and bowls do not overlap: I follows",
       "II (Some bowls are cups) contradicts I: does not follow"],
      shortcut="All + No ⇒ No between the end terms.", seconds=30)
syl_q("Basic", TWO, N(("rose", "roses"), ("lily", "lilies"), ("tulip", "tulips")),
      [("some", "rose", "lily"), ("all", "lily", "tulip")],
      [("all", "rose", "tulip"), ("some", "tulip", "rose")], ONLY_II,
      "Some + All = Some",
      "The roses that are lilies are also tulips, so some roses are tulips, i.e. some tulips are roses (II). Nothing "
      "is said about the roses that are not lilies, so 'All roses are tulips' is not certain (I).",
      ["Some roses are lilies + All lilies are tulips ⇒ Some roses are tulips", "Conversion ⇒ Some tulips are roses: "
       "II follows", "Roses outside lilies may not be tulips: I does not follow"],
      shortcut="Some + All ⇒ Some (and it converts).", seconds=35)
syl_q("Basic", TWO, N(("pilot", "pilots"), ("captain", "captains"), ("sailor", "sailors")),
      [("no", "pilot", "captain"), ("some", "captain", "sailor")],
      [("some", "pilot", "sailor"), ("somenot", "sailor", "pilot")], ONLY_II,
      "No + Some = Some not (in the reverse direction)",
      "The sailors that are captains cannot be pilots, so some sailors are not pilots (II). Sailors outside the "
      "captain group may or may not be pilots, so I is not certain.",
      ["Some captains are sailors ⇒ Some sailors are captains", "No captain is a pilot ⇒ those sailors are not "
       "pilots: II follows", "No statement links pilots to sailors directly: I does not follow"],
      shortcut="No + Some ⇒ 'Some (third) are not (first)'.", seconds=35)
syl_q("Basic", TWO, N(("kite", "kites"), ("balloon", "balloons"), ("toy", "toys")),
      [("all", "kite", "balloon"), ("all", "kite", "toy")],
      [("some", "balloon", "toy"), ("some", "toy", "balloon")], BOTH,
      "Two 'All' statements with a common subject",
      "Kites exist and every kite is both a balloon and a toy, so the kites form a common part of balloons and toys. "
      "Hence some balloons are toys and some toys are balloons.",
      ["All kites are balloons and all kites are toys", "Kites lie in both sets ⇒ Some balloons are toys: I follows",
       "Conversion of I ⇒ Some toys are balloons: II follows"], seconds=30)
syl_q("Basic", TWO, N(("stamp", "stamps"), ("letter", "letters"), ("parcel", "parcels")),
      [("somenot", "stamp", "letter"), ("all", "letter", "parcel")],
      [("somenot", "stamp", "parcel"), ("all", "parcel", "letter")], NEITHER,
      "'Some not' gives no definite conclusion here",
      "The stamps that are not letters may still be parcels (parcels extend beyond letters), so I is not certain. "
      "'All letters are parcels' cannot be reversed into 'All parcels are letters', so II does not follow.",
      ["Some stamps lie outside letters; that part can still be inside parcels: I not definite",
       "All letters are parcels does not convert to All parcels are letters: II does not follow"], seconds=35)
syl_q("Basic", TWO, N(("hill", "hills"), ("rock", "rocks"), ("stone", "stones")),
      [("some", "hill", "rock"), ("somenot", "rock", "stone")],
      [("some", "hill", "stone"), ("no", "hill", "stone")], EITHER,
      "Complementary pair: 'Some' and 'No' on the same two terms",
      "Neither conclusion is certain: the hills that are rocks may or may not lie in the non-stone part of rocks. But "
      "either some hill is a stone or no hill is a stone; one of the two must be true. So either I or II follows.",
      ["Some + Some-not gives no definite hill–stone relation", "I alone is not certain; II alone is not certain",
       "I and II are a 'Some' / 'No' pair on the same terms: exactly one is true", "So either I or II follows"],
      why="'Either' takes the place of 'Both' (four-option rule); Both is impossible for contradictory conclusions.",
      seconds=40)
syl_q("Basic", TWO, N(("shirt", "shirts"), ("jacket", "jackets"), ("coat", "coats")),
      [("all", "shirt", "jacket"), ("somenot", "coat", "jacket")],
      [("somenot", "coat", "shirt"), ("somenot", "shirt", "coat")], ONLY_I,
      "Some-not through an 'All' statement",
      "The coats that are not jackets cannot be shirts, because every shirt is a jacket. So some coats are not shirts "
      "(I). The shirts may well all be coats, so II is not certain.",
      ["All shirts ⊂ jackets", "Coats outside jackets are outside shirts ⇒ Some coats are not shirts: I follows",
       "All shirts could lie in the coat part of jackets: II does not follow"], seconds=40)
# ---- Intermediate (only a few / only)
syl_q("Intermediate", FEW, N(("clerk", "clerks"), ("officer", "officers"), ("manager", "managers")),
      [("only", "clerk", "officer"), ("some", "officer", "manager")],
      [("some", "clerk", "manager"), ("poss_all", "manager", "clerk")], BOTH,
      "'Only A are B' means All B are A",
      "'Only clerks are officers' means every officer is a clerk. The officers that are managers are therefore "
      "clerks, so some clerks are managers (I). Managers are not kept away from clerks anywhere, so all managers "
      "being clerks is possible (II).",
      ["Only clerks are officers ⇒ All officers are clerks", "Some officers are managers ⇒ those are clerks ⇒ Some "
       "clerks are managers: I follows", "No statement separates managers from clerks ⇒ II is possible: follows"],
      why="Reading 'Only clerks are officers' as 'All clerks are officers' loses conclusion I.", seconds=50)
syl_q("Intermediate", FEW, N(("violin", "violins"), ("guitar", "guitars"), ("drum", "drums")),
      [("onlyfew", "violin", "guitar"), ("all", "drum", "guitar")],
      [("somenot", "violin", "drum"), ("some", "drum", "violin")], ONLY_I,
      "'Only a few A are B' = some A are B and some A are not B",
      "Some violins are not guitars, and every drum is a guitar, so those violins are not drums (I). The drums may lie "
      "in the part of guitars that has no violins, so II is not certain.",
      ["Only a few violins are guitars ⇒ some violins lie outside guitars", "Drums ⊂ guitars ⇒ violins outside "
       "guitars are not drums: I follows", "Drums need not overlap the violin part of guitars: II does not follow"],
      seconds=50)
# ---- Advanced (three statements, four terms)
syl_q("Advanced", POSS, N(("brick", "bricks"), ("tile", "tiles"), ("slab", "slabs"), ("block", "blocks")),
      [("some", "brick", "tile"), ("onlyfew", "tile", "slab"), ("all", "slab", "block")],
      [("some", "tile", "block"), ("poss_all", "brick", "block")], BOTH,
      "Definite chain plus an unrestricted possibility",
      "Some tiles are slabs and all slabs are blocks, so some tiles are blocks (I). No statement keeps any brick out "
      "of blocks, so all bricks being blocks is possible (II).",
      ["Only a few tiles are slabs ⇒ some tiles are slabs", "Some tiles are slabs + All slabs are blocks ⇒ Some tiles "
       "are blocks: I follows", "Bricks are never separated from blocks ⇒ all bricks being blocks is possible: II "
       "follows"], seconds=60)
syl_q("Advanced", FEW, N(("lion", "lions"), ("tiger", "tigers"), ("leopard", "leopards"), ("cheetah", "cheetahs")),
      [("no", "lion", "tiger"), ("only", "tiger", "leopard"), ("some", "leopard", "cheetah")],
      [("no", "lion", "leopard"), ("poss_all", "cheetah", "lion")], ONLY_I,
      "'Only tigers are leopards' puts every leopard inside tigers",
      "All leopards are tigers and no lion is a tiger, so no lion is a leopard (I). The cheetahs that are leopards "
      "are tigers, which can never be lions, so all cheetahs can never be lions (II fails).",
      ["Only tigers are leopards ⇒ All leopards are tigers", "No lion is a tiger ⇒ No lion is a leopard: I follows",
       "Some cheetahs are leopards (⊂ tigers) ⇒ those cheetahs are not lions ⇒ II is impossible"], seconds=65)
syl_q("Advanced", POSS, N(("ship", "ships"), ("boat", "boats"), ("yacht", "yachts"), ("raft", "rafts")),
      [("all", "ship", "boat"), ("somenot", "boat", "yacht"), ("no", "yacht", "raft")],
      [("poss_some", "ship", "raft"), ("somenot", "boat", "raft")], ONLY_I,
      "Possibility: look only for a statement that forbids it",
      "Ships are restricted only to boats; rafts are kept away only from yachts. The non-yacht part of boats can hold "
      "ships and rafts together, so some ships being rafts is possible (I). Every boat could be a raft (none of them "
      "would then be a yacht, which the statements allow), so 'Some boats are not rafts' is not certain (II).",
      ["Some ships being rafts: nothing forbids it ⇒ possible: I follows",
       "All boats could lie in rafts (outside yachts), consistent with every statement ⇒ II not definite"],
      seconds=65)
syl_q("Advanced", FEW, N(("shoe", "shoes"), ("sandal", "sandals"), ("boot", "boots"), ("slipper", "slippers")),
      [("onlyfew", "shoe", "sandal"), ("some", "sandal", "boot"), ("no", "boot", "slipper")],
      [("somenot", "shoe", "slipper"), ("somenot", "sandal", "slipper")], ONLY_II,
      "Only the definite chain survives",
      "The sandals that are boots cannot be slippers, so some sandals are not slippers (II). The shoes may avoid boots "
      "entirely, and every shoe could then be a slipper, so I is not certain.",
      ["Some sandals are boots + No boot is a slipper ⇒ Some sandals are not slippers: II follows",
       "Shoe–boot overlap is not certain, so no shoe is forced out of slippers: I does not follow"], seconds=65)
syl_q("Advanced", POSS, N(("city", "cities"), ("town", "towns"), ("village", "villages"), ("hamlet", "hamlets")),
      [("onlyfew", "city", "town"), ("all", "town", "village"), ("only", "village", "hamlet")],
      [("poss_all", "hamlet", "town"), ("some", "city", "village")], BOTH,
      "'Only villages are hamlets' = All hamlets are villages",
      "All hamlets are villages and all towns are villages; nothing stops every hamlet from lying in the town part, so "
      "I is possible. Some cities are towns and all towns are villages, so some cities are villages (II).",
      ["Only villages are hamlets ⇒ All hamlets are villages", "Hamlets and towns both lie inside villages; no "
       "statement separates them ⇒ All hamlets being towns is possible: I follows",
       "Some cities are towns + All towns are villages ⇒ Some cities are villages: II follows"], seconds=65)
syl_q("Advanced", FEW, N(("shell", "shells"), ("pearl", "pearls"), ("bead", "beads"), ("gem", "gems")),
      [("some", "shell", "pearl"), ("no", "pearl", "bead"), ("onlyfew", "bead", "gem")],
      [("some", "shell", "gem"), ("no", "shell", "gem")], EITHER,
      "Either–or across a 'No' statement",
      "Shells are linked only to pearls, and pearls only to 'not beads'; gems can lie inside or outside beads. So a "
      "shell–gem overlap is possible but not certain, and so is no overlap. One of 'Some shells are gems' and 'No "
      "shell is a gem' must be true: either I or II follows.",
      ["Some shells are pearls; no pearl is a bead; some beads are gems and some are not",
       "Gems outside beads may or may not include shells ⇒ neither I nor II is certain",
       "I and II are a 'Some' / 'No' pair on shells and gems ⇒ Either I or II follows"],
      why="'Either' takes the place of 'Both' (four-option rule).", seconds=65)
syl_q("Advanced", POSS, N(("poet", "poets"), ("writer", "writers"), ("editor", "editors"), ("critic", "critics")),
      [("no", "poet", "writer"), ("some", "writer", "editor"), ("all", "editor", "critic")],
      [("some", "poet", "critic"), ("all", "critic", "writer")], NEITHER,
      "No + Some + All: only 'Some critics are not poets' is definite",
      "Poets are kept away only from writers; critics extend beyond editors, so poets may or may not be critics (I not "
      "certain). 'All editors are critics' does not make every critic a writer (II not certain).",
      ["Definite: Some writers are editors ⇒ some writers are critics; those critics are not poets",
       "I: a poet–critic overlap is possible but not certain: does not follow",
       "II: critics may lie outside writers: does not follow", "I and II are on different pairs: not an 'either' case"],
      seconds=60)

# ================================================================================================ INEQUALITY
DIRECT, CODED = "Direct inequality", "Coded inequality"
# ---- Basic: direct
s, ch, cc, ct = direct(["R ≥ S > T = U ≤ V < W"], ["R > U", "W > T"])
ineq_q("Basic", DIRECT, s, ch, cc, ct, BOTH,
       "R ≥ S > T = U gives R > U. T = U ≤ V < W gives W > T. Both follow.",
       ["I: R ≥ S > T = U: same direction with one strict sign → R > U, true",
        "II: T = U ≤ V < W → W > T, true"], seconds=30)
s, ch, cc, ct = direct(["D < E ≤ F > G ≥ H = I"], ["D < F", "I < E"])
ineq_q("Basic", DIRECT, s, ch, cc, ct, ONLY_I,
       "D < E ≤ F gives D < F. Between E and I the chain turns at F (E ≤ F > G), so I and E cannot be compared.",
       ["I: D < E ≤ F → D < F, true", "II: E ≤ F > G ≥ H = I: the direction reverses at F → no relation"],
       seconds=30)
s, ch, cc, ct = direct(["K = L > M ≥ N < O ≤ P"], ["K ≥ O", "P > N"])
ineq_q("Basic", DIRECT, s, ch, cc, ct, ONLY_II,
       "K and O are separated by a reversal at N (M ≥ N < O), so K ≥ O is not certain. N < O ≤ P gives P > N.",
       ["I: K = L > M ≥ N < O: reverses at N → no relation", "II: N < O ≤ P → P > N, true"], seconds=30)
s, ch, cc, ct = direct(["X ≤ Y < Z = A ≥ B > C"], ["Y > B", "X ≥ C"])
ineq_q("Basic", DIRECT, s, ch, cc, ct, NEITHER,
       "Both comparisons pass through Z = A, where the direction reverses (Y < Z = A ≥ B), so neither can be "
       "established.", ["I: Y < Z = A ≥ B: reversal → no relation", "II: X ≤ Y < Z = A ≥ B > C: reversal → no relation"],
       seconds=30)
s, ch, cc, ct = direct(["Y < T ≥ U ≥ V = W < X ≤ Z"], ["T > W", "T = W"])
ineq_q("Basic", DIRECT, s, ch, cc, ct, EITHER,
       "Y < T ≥ U ≥ V = W < X ≤ Z: from T to W, T ≥ U ≥ V = W gives T ≥ W: T is either greater than or equal to W, and neither alone is certain. Together the "
       "two conclusions cover T ≥ W exactly, so either I or II follows.",
       ["T ≥ U ≥ V = W → T ≥ W (no strict sign on the path)", "I (T > W) alone: not certain; II (T = W) alone: not "
        "certain", "I or II together = T ≥ W: Either I or II follows"],
       why="'Either' takes the place of 'Both' (four-option rule); T > W and T = W cannot both hold.", seconds=35)

# ---- Intermediate: coded and combined
CODE_A = {"@": ">", "#": "<", "$": "=", "%": "≥", "&": "≤"}
CODE_A_TXT = ("In the following question, the symbols @, #, $, % and & are used with these meanings:\n"
              "'P @ Q' means 'P is greater than Q'; 'P # Q' means 'P is smaller than Q'; 'P $ Q' means 'P is equal "
              "to Q'; 'P % Q' means 'P is either greater than or equal to Q'; 'P & Q' means 'P is either smaller "
              "than or equal to Q'.\nAssuming the statements to be true, find which of the conclusions I and II "
              "is/are definitely true.")
s, ch, cc, ct = coded(CODE_A_TXT, CODE_A, ["M @ N", "N % O", "O $ P", "Q & P"], ["O @ Q", "O $ Q"])
ineq_q("Intermediate", CODED, s, ch, cc, ct, EITHER,
       "Decoded: M > N ≥ O = P ≥ Q, so O ≥ Q. O > Q and O = Q are each uncertain, but one of them must hold: either I "
       "or II follows.",
       ["Decode: @ → >, % → ≥, $ → =, & → ≤", "M > N ≥ O = P and Q ≤ P → O = P ≥ Q",
        "I: O > Q and II: O = Q together make O ≥ Q: Either"],
       why="'Either' replaces 'Both' (four-option rule).", concept="Decoding symbols; the either-or case", seconds=50)
s, ch, cc, ct = coded(CODE_A_TXT, CODE_A, ["A # B", "B & C", "D @ C", "E % D"], ["E @ A", "B # D"])
ineq_q("Intermediate", CODED, s, ch, cc, ct, BOTH,
       "Decoded: A < B ≤ C < D ≤ E. So E > A and B < D: both follow.",
       ["Decode: A < B, B ≤ C, D > C, E ≥ D", "Chain: A < B ≤ C < D ≤ E", "I: E @ A means E > A: true",
        "II: B # D means B < D: B ≤ C < D → true"], concept="Decoding symbols, then reading the chain", seconds=50)
CODE_B = {"÷": ">", "×": "≤", "+": "≥", "−": "<", "★": "="}
CODE_B_TXT = ("In the following question, 'A ÷ B' means 'A is greater than B', 'A × B' means 'A is not greater "
              "than B', 'A + B' means 'A is not smaller than B', 'A − B' means 'A is smaller than B', and 'A ★ B' "
              "means 'A is equal to B'.\nAssuming the statements to be true, find which of the conclusions I and II "
              "is/are definitely true.")
s, ch, cc, ct = coded(CODE_B_TXT, CODE_B, ["G ÷ H", "H + J", "J ★ K", "L × K"], ["G ÷ L", "L − H"])
ineq_q("Intermediate", CODED, s, ch, cc, ct, ONLY_I,
       "Decoded: G > H ≥ J = K ≥ L. So G > L (I follows), but H ≥ L only, so L < H is not certain.",
       ["Decode: G > H, H ≥ J, J = K, L ≤ K", "Chain: G > H ≥ J = K ≥ L", "I: G > L: true",
        "II: L < H: only L ≤ H is certain (equality possible): not definite"],
       concept="Decoding symbols, then reading the chain", seconds=50)
s, ch, cc, ct = coded(CODE_B_TXT, CODE_B, ["R − S", "S ★ T", "T + U", "V ÷ U"], ["V ÷ R", "U × S"])
ineq_q("Intermediate", CODED, s, ch, cc, ct, ONLY_II,
       "Decoded: R < S = T ≥ U < V. V and R are linked only through U, where the direction reverses, so V > R is not "
       "certain. T ≥ U with S = T gives U ≤ S.",
       ["Decode: R < S, S = T, T ≥ U, V > U", "Chain: R < S = T ≥ U < V", "I: V > R: reversal at U → no relation",
        "II: U ≤ S: S = T ≥ U → true"], concept="Decoding symbols, then reading the chain", seconds=55)
s, ch, cc, ct = direct(["F ≥ G", "H < G", "J = H", "K ≥ F", "L > K", "M ≤ J"], ["K > J", "F > K"])
ineq_q("Intermediate", DIRECT, s, ch, cc, ct, ONLY_I,
       "Combined: L > K ≥ F ≥ G > H = J ≥ M. So K > J. F > K contradicts K ≥ F.",
       ["Combine: L > K ≥ F ≥ G > H = J ≥ M", "I: K > J (one strict sign, no reversal): true", "II: F > K: false (K ≥ F)"],
       concept="Combining several statements into one chain", seconds=45)
s, ch, cc, ct = direct(["R < S", "T ≥ S", "U ≤ S", "V = U", "W > T", "Q ≤ R"], ["R < V", "T > V"])
ineq_q("Intermediate", DIRECT, s, ch, cc, ct, NEITHER,
       "R and V are both below S along different branches, so they cannot be compared. T ≥ S ≥ U = V gives only "
       "T ≥ V, so T > V is not certain.",
       ["Chains: Q ≤ R < S ≤ T < W and V = U ≤ S", "I: R and V are both on the lower side of S: no relation",
        "II: T ≥ S ≥ U = V → T ≥ V only (all could be equal): not definite"],
       concept="Combining several statements into one chain", seconds=50)
s, ch, cc, ct = direct(["W = X", "X ≥ Y", "Z < Y", "V > W"], ["V > Y", "Z < X"])
ineq_q("Intermediate", DIRECT, s, ch, cc, ct, BOTH,
       "Combined: V > W = X ≥ Y > Z. So V > Y and X > Z: both follow.",
       ["Combine: V > W = X ≥ Y > Z", "I: V > W = X ≥ Y → V > Y: true", "II: X ≥ Y > Z → Z < X: true"],
       concept="Combining several statements into one chain", seconds=45)
s, ch, cc, ct = direct(["C > D ≥ E", "F < E", "G ≤ F", "H > C"], ["G = E", "H > G"])
ineq_q("Intermediate", DIRECT, s, ch, cc, ct, ONLY_II,
       "Combined: H > C > D ≥ E > F ≥ G. So G < E (I is false) and H > G (II follows).",
       ["Combine: H > C > D ≥ E > F ≥ G", "I: G = E? E > F ≥ G → E > G: false", "II: H > G: true"],
       concept="Combining several statements into one chain", seconds=45)
CANDS = {"M < N ≤ O = R ≤ P < Q": None, "M ≤ N = O ≥ R < P ≤ Q": None, "R > O ≥ N > M ≥ P = Q": None,
         "Q > P ≥ O = N ≥ M ≥ R": None}
for e in CANDS:
    f1, f2, _ = ineq_eval([e], [("M", "<", "Q"), ("R", "≥", "O")])
    CANDS[e] = f1 and f2
good = [e for e, ok in CANDS.items() if ok]
assert good == ["M < N ≤ O = R ≤ P < Q"]
mcq(INQ, DIRECT, "Intermediate",
    "In which of the following expressions are both 'M < Q' and 'R ≥ O' definitely true?", good[0],
    [e for e in CANDS if e != good[0]], "Testing each expression against two conclusions",
    "In M < N ≤ O = R ≤ P < Q the signs from M to Q all point the same way (with strict signs), so M < Q; and O = R "
    "gives R ≥ O. Each other expression fails at least one conclusion.",
    ["M < N ≤ O = R ≤ P < Q: M < Q true; R = O so R ≥ O true",
     "M ≤ N = O ≥ R < P ≤ Q: reverses at O and R → M < Q not certain; R ≤ O",
     "R > O ≥ N > M ≥ P = Q: M ≥ Q, so M < Q is false",
     "Q > P ≥ O = N ≥ M ≥ R: M < Q true, but R ≤ O, so R ≥ O is not certain"],
    seconds=60, verified_by=EXHAUST)
BL = {}
for sym in [">", "≥", "=", "<", "≤"]:
    f1, f2, _ = ineq_eval(["P ≥ Q {} R > S".format(sym)], [("P", "≥", "R"), ("R", "≥", "Q")])
    BL[sym] = f1 and f2
assert [k for k, v in BL.items() if v] == ["="]
mcq(INQ, DIRECT, "Intermediate",
    "Which symbol should be placed in the blank in the expression 'P ≥ Q __ R > S' so that both 'P ≥ R' and "
    "'R ≥ Q' are definitely true?", "=", [">", "≥", "≤"], "Choosing a sign for two required relations",
    "With '=', Q = R, so P ≥ Q = R gives P ≥ R, and R = Q gives R ≥ Q. With '>' or '≥', R ≤ Q, so R ≥ Q is not "
    "certain; with '≤', the direction reverses at Q and P cannot be compared with R.",
    ["'=': P ≥ Q = R → P ≥ R; R = Q → R ≥ Q: both hold",
     "'>' or '≥': Q > R or Q ≥ R → R ≥ Q fails (not certain)",
     "'≤': P ≥ Q ≤ R → no relation between P and R"],
    seconds=50, verified_by=EXHAUST)
# ---- Advanced
CODE_C = {"δ": "<", "β": ">", "λ": "≤", "μ": "≥", "θ": "="}
CODE_C_TXT = ("In the following question, 'A δ B' means 'A is neither greater than nor equal to B'; 'A β B' means "
              "'A is neither smaller than nor equal to B'; 'A λ B' means 'A is not greater than B'; 'A μ B' means "
              "'A is not smaller than B'; 'A θ B' means 'A is neither greater than nor smaller than B'.\nAssuming the "
              "statements to be true, find which of the conclusions I and II is/are definitely true.")
s, ch, cc, ct = coded(CODE_C_TXT, CODE_C, ["J μ K", "K β L", "M λ L", "M θ N", "O δ N"], ["L β N", "L θ N"])
ineq_q("Advanced", CODED, s, ch, cc, ct, EITHER,
       "Decoded: J ≥ K > L ≥ M = N > O. So L ≥ N: L > N and L = N are each uncertain, but one must be true. Either I "
       "or II follows.",
       ["Decode: δ → <, β → >, λ → ≤, μ → ≥, θ → =", "J ≥ K, K > L, M ≤ L, M = N, O < N",
        "Chain: J ≥ K > L ≥ M = N > O ⇒ L ≥ N", "I (L > N) or II (L = N): Either"],
       why="'Either' replaces 'Both' (four-option rule).", concept="Negative-worded codes; the either-or case",
       seconds=75)
s, ch, cc, ct = direct(["U ≥ V", "W < V", "X ≤ W", "Y > U", "Z = X", "V ≥ T"], ["Y > Z", "T > Z"])
ineq_q("Advanced", DIRECT, s, ch, cc, ct, ONLY_I,
       "Combined: Y > U ≥ V > W ≥ X = Z, with T ≤ V on a separate branch. So Y > Z. T and Z are both below V along "
       "different branches, so they cannot be compared.",
       ["Rewrite: Y > U, U ≥ V, V > W, W ≥ X, X = Z, T ≤ V", "Chain: Y > U ≥ V > W ≥ X = Z",
        "I: Y > Z: true", "II: T ≤ V and Z < V: both below V → no relation"],
       concept="Combining six statements into one chain", seconds=70)

# ================================================================================================ BLOOD RELATIONS
F = Family().add("Gf", "M").add("Gm", "F").marry("Gf", "Gm").add("Fa", "M", "Gf", "Gm").add("Mo", "F")
F.marry("Fa", "Mo").add("Kiran", "M", "Fa", "Mo").add("Girl", "F", "Fa", "Mo")
assert [c for c in F.children("Gf") if F.g[c] == "M"] == ["Fa"]
ans = F.rel("Girl", "Kiran")
assert ans == "sister"
mcq(BLD, "Direct relation", "Basic",
    "Pointing to a girl in a photograph, Kiran said, \"She is the daughter of the only son of my father's father.\" "
    "How is the girl related to Kiran?", cap(ans), ["Cousin", "Niece", "Daughter"],
    "Collapsing 'the only son of my father's father'",
    "Kiran's father's father has only one son, and Kiran's father is a son of his, so that only son is Kiran's own "
    "father. The girl is the daughter of Kiran's father: Kiran's sister.",
    ["My father's father = Kiran's paternal grandfather", "His only son = Kiran's father",
     "Daughter of Kiran's father = Kiran's sister"],
    why_others_wrong="Cousin would need the 'only son' to be a different man (an uncle), which 'only' rules out.",
    seconds=30, verified_by=RECOMP)
CODE_BR = {"%": "daughter", "*": "wife", "$": "brother", "#": "mother"}
F = Family().add("G1", "M").add("G2", "F").marry("G1", "G2").add("R", "M", "G1", "G2").add("S", "F", "G1", "G2")
F.add("Q", "F").marry("Q", "R").add("P", "F", "R", "Q").add("Sx", "M").marry("S", "Sx").add("T", "M", "Sx", "S")
expr = "P % Q * R $ S # T"
F.check(coded_facts(expr, CODE_BR))
ans = F.rel("T", "P")
assert ans == "cousin"
mcq(BLD, "Coded blood relation", "Intermediate",
    "In a certain code:\n'A % B' means 'A is the daughter of B';\n'A * B' means 'A is the wife of B';\n'A $ B' means "
    "'A is the brother of B';\n'A # B' means 'A is the mother of B'.\n\nIf 'P % Q * R $ S # T', how is T related to "
    "P?", cap(ans), ["Sister", "Niece", "Aunt"], "Decoding a chain that crosses to a sibling's family",
    "P is the daughter of Q, and Q is the wife of R, so R is P's father. R is the brother of S, so S is P's aunt. S is "
    "the mother of T, so T is the child of P's father's sister: P's cousin.",
    ["P % Q: P is Q's daughter", "Q * R: Q is R's wife ⇒ R is P's father", "R $ S: R is S's brother ⇒ S is P's aunt",
     "S # T: S is T's mother ⇒ T is P's cousin"],
    why_others_wrong="Sister would need T to share P's parents; niece is T's relation to R; aunt is S's relation to P.",
    seconds=50, verified_by=RECOMP)
F = Family().add("Arvind", "M").add("Bimla", "F").marry("Arvind", "Bimla")
F.add("Chetan", "M", "Arvind", "Bimla").add("Deepti", "F", "Arvind", "Bimla")
F.add("Harleen", "F").marry("Chetan", "Harleen").add("Eshaan", "M", "Chetan", "Harleen")
F.add("Girish", "M").marry("Deepti", "Girish").add("Falguni", "F", "Girish", "Deepti")
facts = [("Falguni", "daughter", "Girish"), ("Harleen", "daughter-in-law", "Arvind"),
         ("Deepti", "sister-in-law", "Harleen"), ("Girish", "son-in-law", "Bimla"), ("Chetan", "father", "Eshaan")]
F.check(facts)
assert [x for c in F.children("Bimla") for x in F.children(c) if F.g[x] == "M"] == ["Eshaan"]
ans = F.rel("Girish", "Eshaan")
assert ans == "uncle"
mcq(BLD, "Family puzzle", "Advanced",
    "A family of three generations has eight members: Arvind, Bimla, Chetan, Deepti, Eshaan, Falguni, Girish and "
    "Harleen. Arvind, Chetan, Eshaan and Girish are male; the others are female. There are three married couples.\n"
    "- Eshaan is the only grandson of Bimla.\n- Falguni is the daughter of Girish.\n- Harleen is the daughter-in-law "
    "of Arvind.\n- Deepti is the sister-in-law of Harleen.\n- Girish is the son-in-law of Bimla.\n- Chetan is the "
    "father of Eshaan.\n- Arvind and Bimla are married to each other and have only two children.\n\n"
    "How is Girish related to Eshaan?", cap(ans), ["Father-in-law", "Brother-in-law", "Grandfather"],
    "Building a three-generation tree from in-law clues",
    "Arvind and Bimla have two children: Harleen is married to their son and Girish to their daughter. Chetan, a "
    "male, is Eshaan's father and must be the son (Girish is the son-in-law), so Chetan's wife is Harleen. Deepti, "
    "female and Harleen's sister-in-law, is the daughter, married to Girish; Falguni is their daughter. Girish is the "
    "husband of Eshaan's father's sister: Eshaan's uncle.",
    ["Generation 1: Arvind + Bimla, two children: one son (husband of Harleen), one daughter (wife of Girish)",
     "Chetan (male, father of Eshaan) = the son, married to Harleen", "Deepti (female) = the daughter, married to "
     "Girish; Falguni = their daughter", "Girish = husband of Eshaan's paternal aunt ⇒ uncle"],
    why_others_wrong="Brother-in-law is Girish's relation to Chetan; father-in-law and grandfather belong to "
                     "generation 1.", seconds=90, verified_by=RECOMP)

# ================================================================================================ DIRECTION SENSE
# ---- Basic
x, y = walk("W", [(None, 15), ("R", 8)])
assert (x, y) == (-15, 8)
mcq(DIR, "Distance and direction", "Basic",
    "Meena walks 15 m towards the west. She then turns right and walks 8 m. How far is she from her starting point, "
    "and in which direction?", f"{dist(x, y)} m, {compass(x, y)}",
    ["23 m, North-West", "17 m, North-East", "7 m, North"], "Displacement with an 8-15-17 triangle",
    "Turning right from west means facing north. She is 15 m west and 8 m north of the start: √(225 + 64) = 17 m, "
    "towards the north-west.",
    ["15 m west → (−15, 0)", "Right from west = north; 8 m → (−15, 8)", "√(15² + 8²) = 17 m; west and north → "
     "North-West"], why_others_wrong="23 m adds the two legs; North-East reverses the east–west direction.",
    seconds=35, verified_by=RECOMP)
pts = {"Q": (0, 0)}
pts["P"] = (0, 6)
pts["R"] = (-6, 0)
pts["S"] = (-6, -6)
dx, dy = pts["P"][0] - pts["S"][0], pts["P"][1] - pts["S"][1]
assert compass(dx, dy) == "North-East"
mcq(DIR, "Point-to-point", "Basic",
    "Point P is 6 m north of point Q. Point R is 6 m west of point Q. Point S is 6 m south of point R. In which "
    "direction is point P with respect to point S?", compass(dx, dy), ["North-West", "South-East", "North"],
    "Placing points on a grid", "With Q at (0, 0): P = (0, 6), R = (−6, 0), S = (−6, −6). From S to P is 6 m east "
    "and 12 m north, so P is to the north-east of S.",
    ["Q (0, 0), P (0, 6), R (−6, 0), S (−6, −6)", "P − S = (6, 12): east and north ⇒ North-East"],
    why_others_wrong="South-East and North-West mix up the signs; North ignores the 6 m east component.", seconds=40,
    verified_by=RECOMP)
face = [f for f in CW if CW[(CW.index(f) + 2) % 4] == "E"]
assert face == ["W"]
mcq(DIR, "Shadow-based", "Basic",
    "One evening before sunset, Ravi was standing in an open field. His shadow fell exactly behind him. Which direction "
    "was he facing?", NAME[face[0]], ["East", "North", "South"], "Shadows in the evening",
    "In the evening the sun is in the west, so shadows fall towards the east. The shadow is behind Ravi, so his back "
    "is to the east and he faces west (towards the sun).",
    ["Evening sun → west; shadow → east", "Shadow behind him ⇒ his back faces east", "So he faces West"],
    why_others_wrong="East is where the shadow points, not where he faces.", seconds=30, verified_by=RECOMP)
ang = (90 + 90 + 180 - 45) % 360
assert ang == 315
mcq(DIR, "Distance and direction", "Basic",
    "A girl is facing east. She turns 90° clockwise, then 180° clockwise, and then 45° anticlockwise. Which direction "
    "is she facing now?", "North-West", ["North-East", "South-West", "West"], "Net rotation",
    "Measure directions clockwise from north: east = 90°. 90 + 90 = 180° (south), + 180 = 360° (north), − 45 = 315°, "
    "which is north-west.",
    ["East = 90°", "+90° → 180° (south)", "+180° → 0° (north)", "−45° → 315° (north-west)"],
    shortcut="Net turn = 90 + 180 − 45 = 225° clockwise; east + 225° = 315° = north-west.", seconds=35,
    verified_by=RECOMP)
x, y = walk("N", [(None, 5), ("R", 3), ("R", 5)])
assert (x, y) == (3, 0)
mcq(DIR, "Distance and direction", "Basic",
    "Asha starts from her house and walks 5 km north. She turns right and walks 3 km, then turns right again and "
    "walks 5 km. How far is she from her house, and in which direction?", f"{dist(x, y)} km, {compass(x, y)}",
    ["3 km, West", "5 km, East", "13 km, South"], "Legs that cancel out",
    "The 5 km north and 5 km south cancel; only the 3 km east remains. She is 3 km east of her house.",
    ["5 km north → (0, 5)", "Right (east) 3 km → (3, 5)", "Right (south) 5 km → (3, 0)", "3 km, East"],
    why_others_wrong="13 km adds every leg; West reverses the direction of the 3 km leg.", seconds=35,
    verified_by=RECOMP)
pts = {"Y": (0, 0), "X": (12, 0)}
pts["Z"] = (12, -9)
dx, dy = pts["Z"]
assert dist(dx, dy) == "15"
mcq(DIR, "Point-to-point", "Basic",
    "Village X is 12 km east of village Y. Village Z is 9 km south of village X. What is the shortest distance "
    "between villages Y and Z?", f"{dist(dx, dy)} km", ["21 km", "12 km", "18 km"], "Pythagoras on a 9-12-15 triangle",
    "Y, X and Z form a right angle at X: YZ = √(12² + 9²) = √225 = 15 km.",
    ["Y (0, 0), X (12, 0), Z (12, −9)", "YZ = √(144 + 81) = 15 km"],
    why_others_wrong="21 km is the path through X, not the shortest distance.",
    natural=lambda t: int(t.split()[0]), seconds=30, verified_by=RECOMP)
# ---- Intermediate
a_ = walk("N", [(None, 7), ("R", 4)])
b_ = walk("S", [(None, 5), ("R", 1)])
dx, dy = a_[0] - b_[0], a_[1] - b_[1]
assert a_ == (4, 7) and b_ == (-1, -5) and (dx, dy) == (5, 12)
mcq(DIR, "Distance and direction", "Intermediate",
    "Ankit and Bunty start from the same point. Ankit walks 7 km north, turns right and walks 4 km. Bunty walks 5 km "
    "south, turns right and walks 1 km. How far apart are they now, and in which direction is Ankit with respect to "
    "Bunty?", f"{dist(dx, dy)} km, {compass(dx, dy)}", ["13 km, South-West", "17 km, North-East", "12 km, North"],
    "Two walkers: subtract the final positions",
    "Ankit ends at (4, 7). Bunty, turning right while facing south, faces west and ends at (−1, −5). Ankit − Bunty = "
    "(5, 12): 13 km, towards the north-east.",
    ["Ankit: 7 north → (0, 7); right = east, 4 → (4, 7)", "Bunty: 5 south → (0, −5); right of south = west, 1 → (−1, −5)",
     "Difference (5, 12) → √(25 + 144) = 13 km; north and east → North-East"],
    why_others_wrong="South-West is Bunty's direction from Ankit; 17 km adds the legs (12 + 5).", seconds=60,
    verified_by=RECOMP)
x_face = [f for f in CW if turn(f, "L") == "W"]
y_face = [CW[(CW.index(f) + 2) % 4] for f in x_face]
assert x_face == ["N"] and y_face == ["S"]
mcq(DIR, "Shadow-based", "Intermediate",
    "One morning after sunrise, Ishaan and Yatin were standing back to back. Ishaan's shadow fell exactly to his left. "
    "Which direction was Yatin facing?", NAME[y_face[0]], ["North", "East", "West"],
    "Morning shadows with two observers",
    "In the morning the sun is in the east, so shadows fall to the west. Ishaan's left points west, so Ishaan faces "
    "north. Standing back to back, Yatin faces the opposite way: south.",
    ["Morning sun → east; shadow → west", "Ishaan's left = west ⇒ Ishaan faces north",
     "Back to back ⇒ Yatin faces south"], why_others_wrong="North is Ishaan's direction, not Yatin's.", seconds=45,
    verified_by=RECOMP)
pts = {"Q": (0, 0), "P": (10, 0)}
pts["R"] = ((pts["P"][0] + pts["Q"][0]) / 2, 0)
pts["S"] = (pts["R"][0], 12)
dx, dy = pts["S"][0] - pts["Q"][0], pts["S"][1] - pts["Q"][1]
assert (dx, dy) == (5, 12)
mcq(DIR, "Point-to-point", "Intermediate",
    "Point P is 10 m east of point Q. Point R is the midpoint of the line joining P and Q. Point S is 12 m north of "
    "point R. How far is point S from point Q, and in which direction?", f"{dist(int(dx), dy)} m, {compass(dx, dy)}",
    ["13 m, North-West", "15.6 m, North-East", "12 m, North"], "Midpoints on a grid",
    "With Q at (0, 0), P = (10, 0), so R = (5, 0) and S = (5, 12). S is 5 m east and 12 m north of Q: 13 m, towards "
    "the north-east.",
    ["Q (0, 0), P (10, 0) → midpoint R (5, 0)", "S = R + 12 m north = (5, 12)", "QS = √(25 + 144) = 13 m; North-East"],
    why_others_wrong="North-West reverses the east component; 12 m ignores it.", seconds=55, verified_by=RECOMP)
# ---- Advanced
STEP = {"★": (5, 0), "◆": (0, -3), "▲": (-8, 0), "●": (0, 9)}
pts = {"K": (0, 0)}
for a, s_, b in [("J", "★", "K"), ("L", "●", "J"), ("M", "▲", "L"), ("N", "◆", "M")]:
    pts[a] = (pts[b][0] + STEP[s_][0], pts[b][1] + STEP[s_][1])
dx, dy = pts["N"][0] - pts["K"][0], pts["N"][1] - pts["K"][1]
assert pts["N"] == (-3, 6) and dist(dx, dy) == "3√5"
mcq(DIR, "Point-to-point", "Advanced",
    "In a certain code:\n'A ★ B' means 'A is 5 m east of B';\n'A ◆ B' means 'A is 3 m south of B';\n'A ▲ B' means "
    "'A is 8 m west of B';\n'A ● B' means 'A is 9 m north of B'.\n\nIf 'J ★ K', 'L ● J', 'M ▲ L' and 'N ◆ M', what is "
    "the shortest distance between N and K, and in which direction is N with respect to K?",
    f"{dist(dx, dy)} m, {compass(dx, dy)}", ["3√5 m, South-East", "9 m, North-West", "√41 m, North-West"],
    "Coded directions converted to coordinates",
    "With K at (0, 0): J = (5, 0), L = (5, 9), M = (−3, 9), N = (−3, 6). N is 3 m west and 6 m north of K: √45 = "
    "3√5 m, towards the north-west.",
    ["K (0, 0); J ★ K → J (5, 0); L ● J → L (5, 9)", "M ▲ L → M (−3, 9); N ◆ M → N (−3, 6)",
     "N − K = (−3, 6) → √(9 + 36) = 3√5 m; west and north → North-West"],
    why_others_wrong="South-East is K's direction from N; √41 m uses the wrong north–south gap (5 m).", seconds=75,
    verified_by=RECOMP)
assert dist(-4, 5) == "√41"
PT = {"B": (0, 0), "A": (-6, 0), "C": (0, 8), "D": (5, 8), "E": (5, 4), "F": (-6, 4), "G": (-6, 8)}
chain = [("A", "B", 6, "west"), ("C", "B", 8, "north"), ("D", "C", 5, "east"), ("E", "D", 4, "south"),
         ("F", "E", 11, "west"), ("G", "F", 4, "north")]
U = {"north": (0, 1), "south": (0, -1), "east": (1, 0), "west": (-1, 0)}
for a, b, d_, w_ in chain:
    assert PT[a] == (PT[b][0] + U[w_][0] * d_, PT[b][1] + U[w_][1] * d_)
sid = stimulus("puzzle", "Seven points on a plane",
               "Study the following information about seven points A, B, C, D, E, F and G on a flat ground.",
               [(f"Point {a} is {d_} m {w_} of point {b}.", (), None) for a, b, d_, w_ in chain],
               "Take B as (0, 0), with east as +x and north as +y: "
               + ", ".join(f"{p} = ({PT[p][0]}, {PT[p][1]})" for p in "ABCDEFG") + ".")
DQ2 = lambda text, correct, wrongs, concept, expl, steps, **kw: mcq(
    DIR, "Point-to-point", "Advanced", text, correct, wrongs, concept, expl, steps, stimulus=sid,
    verified_by=RECOMP, **kw)
GRID = "B (0, 0), A (−6, 0), C (0, 8), D (5, 8), E (5, 4), F (−6, 4), G (−6, 8)"
dx, dy = PT["D"][0] - PT["A"][0], PT["D"][1] - PT["A"][1]
DQ2("In which direction is point D with respect to point A?", compass(dx, dy), ["South-West", "North", "East"],
    "Coordinates of a chain of points", f"D − A = ({dx}, {dy}): east and north, so D is to the north-east of A.",
    [GRID, f"D − A = ({dx}, {dy}) → North-East"], seconds=70)
assert compass(dx, dy) == "North-East"
dac = dist(PT["C"][0] - PT["A"][0], PT["C"][1] - PT["A"][1])
DQ2("What is the shortest distance between points A and C?", f"{dac} m", ["14 m", "8 m", "12 m"],
    "Pythagoras on a 6-8-10 triangle", "A is 6 m west of B and C is 8 m north of B, so AC = √(36 + 64) = 10 m.",
    [GRID, "AC = √(6² + 8²) = 10 m"], why_others_wrong="14 m is the path through B.",
    natural=lambda t: int(t.split()[0]), seconds=60)
assert dac == "10"
on = [p for p in "BCDE" if PT[p][0] == PT["A"][0] and 0 < PT[p][1] < PT["G"][1]] + \
     [p for p in "F" if PT[p][0] == PT["A"][0] and PT["A"][1] < PT[p][1] < PT["G"][1]]
assert on == ["F"]
DQ2("Which point lies on the straight line segment joining A and G?", on[0], ["B", "E", "C"],
    "Points with the same x-coordinate lie on one north–south line",
    "A = (−6, 0) and G = (−6, 8) lie on the same north–south line. F = (−6, 4) is on that line between them.",
    [GRID, "Only F has x = −6 and 0 < y < 8"],
    why_others_wrong="B and E are east of the line; C is 6 m east of G.", seconds=65)
x, y = walk("N", [(None, 20), ("R", 15), ("R", 27), ("L", 9)])
assert (x, y) == (24, -7)
mcq(DIR, "Distance and direction", "Advanced",
    "Starting from point S, a car travels 20 km north, turns right and travels 15 km, turns right again and travels "
    "27 km, and then turns left and travels 9 km. How far is the car from S, and in which direction?",
    f"{dist(x, y)} km, {compass(x, y)}", ["25 km, North-East", "31 km, South-East", "24 km, East"],
    "Net displacement with a 7-24-25 triangle",
    "Net east: 15 + 9 = 24 km (turning left while facing south means facing east). Net south: 27 − 20 = 7 km. "
    "Distance = √(24² + 7²) = 25 km, towards the south-east.",
    ["20 km north → (0, 20)", "Right (east) 15 → (15, 20)", "Right (south) 27 → (15, −7)",
     "Left of south = east, 9 → (24, −7)", "√(576 + 49) = 25 km; east and south → South-East"],
    why_others_wrong="North-East forgets that the car ends 7 km south of S; 31 km adds the components.", seconds=80,
    verified_by=RECOMP)

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


# ================================================================================================ CODING-DECODING
LC, SW, NC = "Letter coding", "Sentence/word coding", "Number coding"
# ---- Basic
alt = lambda w: "".join(AL[(pos(c) - 1 + (1 if i % 2 == 0 else -1)) % 26] for i, c in enumerate(w))
assert alt("PLANET") == "QKBMFS"
ans = alt("SILVER")
assert ans == "THMUFQ"
mcq(COD, LC, "Basic", "In a certain code language, PLANET is written as QKBMFS. How is SILVER written in that code "
    "language?", ans, ["TJMWFS", "RHKUDQ", "THMUFS"], "Alternating forward and backward shifts",
    "PLANET → QKBMFS: P+1, L−1, A+1, N−1, E+1, T−1. The letters in odd places move one step forward and those in even "
    "places one step back. SILVER: S+1 = T, I−1 = H, L+1 = M, V−1 = U, E+1 = F, R−1 = Q.",
    ["Check: P→Q (+1), L→K (−1), A→B (+1), N→M (−1), E→F (+1), T→S (−1)",
     "SILVER: S→T, I→H, L→M, V→U, E→F, R→Q", f"Code: {ans}"],
    why_others_wrong="TJMWFS shifts every letter forward; RHKUDQ shifts every letter back; THMUFS gets the last "
                     "letter wrong.", seconds=35, verified_by=RECOMP)

# ---- Intermediate: sentence-coding set
SENTS = [(["gold", "price", "rises", "today"], ["mo", "ki", "ta", "ru"]),
         (["silver", "price", "falls", "today"], ["ki", "ne", "zo", "ru"]),
         (["demand", "rises", "for", "gold"], ["ta", "pa", "mo", "lu"]),
         (["silver", "demand", "is", "high"], ["zo", "pa", "vi", "sa"])]
SPAIRS = [("gold price rises today", "mo ki ta ru"), ("silver price falls today", "ki ne zo ru"),
          ("demand rises for gold", "ta pa mo lu"), ("silver demand is high", "zo pa vi sa")]
for (ws, cs), (wt_, ct_) in zip(SENTS, SPAIRS):
    assert ws == wt_.split() and cs == ct_.split()
sid = stimulus("passage", "Four coded sentences about metal prices",
               "In a certain code language:\n" + "\n".join(f"'{w}' is written as '{c}'" for w, c in SPAIRS) +
               "\n\n(The codes of the words in a sentence may appear in any order.)", None,
               "silver = zo (sentences 2 and 4); demand = pa (sentences 3 and 4); price and today share {ki, ru} "
               "(sentences 1 and 2) and cannot be told apart; gold and rises share {mo, ta} (sentences 1 and 3) and "
               "cannot be told apart. Then falls = ne (sentence 2), for = lu (sentence 3), and is and high share "
               "{vi, sa}.")
CQ = lambda text, correct, wrongs, concept, expl, steps, **kw: mcq(
    COD, SW, "Intermediate", text, correct, wrongs, concept, expl, steps, stimulus=sid, verified_by=RECOMP, **kw)
got = sentence_solve(SENTS, "falls")
assert got == {"ne"}
CQ("What is the code for 'falls'?", "ne", ["zo", "ki", "ru"], "Eliminating shared words",
   "Sentence 2 is 'silver price falls today'. silver = zo (common to sentences 2 and 4), and price and today take ki "
   "and ru (common to sentences 1 and 2). The code left is ne.",
   ["Sentences 2 & 4: silver = zo", "Sentences 1 & 2: {price, today} = {ki, ru}", "Sentence 2: falls = ne"],
   seconds=50)
assert sentence_solve(SENTS, "demand") == {"pa"}
CQ("What is the code for 'demand'?", "pa", ["ta", "mo", "zo"], "Common word, common code",
   "'demand' appears in sentences 3 and 4, and the only code common to both is pa.",
   ["Sentence 3 codes: ta pa mo lu; sentence 4 codes: zo pa vi sa", "Common code: pa ⇒ demand = pa"], seconds=40)
assert sentence_solve(SENTS, "lu") == {"for"}
CQ("Which word is coded as 'lu'?", "for", ["rises", "gold", "demand"], "Decoding a code back to a word",
   "Sentence 3 is 'demand rises for gold' = 'ta pa mo lu'. demand = pa, and gold and rises take mo and ta (shared "
   "with sentence 1). So lu = for.",
   ["demand = pa (sentences 3 & 4)", "{gold, rises} = {mo, ta} (sentences 1 & 3)", "Remaining: for = lu"],
   seconds=45)
assert sentence_solve(SENTS, "gold") == {"mo", "ta"}
CQ("What is the code for 'gold'?", "Cannot be determined", ["mo", "ta", "ki"], "When two words always appear together",
   "gold and rises appear together in sentences 1 and 3 and never apart, so they share the codes mo and ta in some "
   "order. The code for gold cannot be fixed.",
   ["Sentences 1 & 3 share {gold, rises} and {mo, ta}", "No sentence contains one without the other",
    "So gold = mo or ta: cannot be determined"],
   why_others_wrong="mo and ta are each possible but neither is certain; ki belongs to price or today.", seconds=50)

# ---- Intermediate: standalone
pair_swap = lambda w: "".join(w[i + 1] + w[i] for i in range(0, len(w) - 1, 2)) + (w[-1] if len(w) % 2 else "")
code_ps = lambda w: shift(pair_swap(w), 1)
assert code_ps("MOTHER") == "PNIUSF"
ans = code_ps("SECOND")
assert ans == "FTPDEO"
mcq(COD, LC, "Intermediate", "In a certain code, MOTHER is written as PNIUSF. How is SECOND written in that code?",
    ans, ["TFDPOE", "FTPDOE", "RDBNMC"], "Swap each pair of letters, then shift forward",
    "MOTHER → split into pairs MO | TH | ER → swap each pair → OM HT RE → move each letter one step forward → PN IU SF. "
    f"SECOND → SE | CO | ND → ES OC DN → FT PD EO = {ans}.",
    ["Check: MOTHER → OMHTRE → +1 → PNIUSF", "SECOND → ESOCDN", f"+1 → {ans}"],
    why_others_wrong="TFDPOE shifts without swapping; FTPDOE swaps only two pairs correctly; RDBNMC shifts backwards.",
    seconds=50, verified_by=RECOMP)
oe = lambda w: shift(w[0::2] + w[1::2], 1)
assert oe("MARKET") == "NSFBLU"
ans = oe("PLANET")
assert ans == "QBFMOU"
mcq(COD, LC, "Intermediate", "In a certain code, MARKET is written as NSFBLU. How is PLANET written in that code?",
    ans, ["QMBOFU", "PAELNT", "QBFOMU"], "Odd-place letters first, then even-place letters, then +1",
    "MARKET: letters in odd places (M, R, E) are written first, then those in even places (A, K, T): MREAKT; each "
    "letter then moves one step forward: NSFBLU. PLANET → P, A, E then L, N, T → PAELNT → QBFMOU.",
    ["MARKET → MRE + AKT → +1 → NSF BLU (matches)", "PLANET → PAE + LNT = PAELNT", f"+1 → {ans}"],
    why_others_wrong="QMBOFU shifts without rearranging; PAELNT rearranges without shifting; QBFOMU swaps two "
                     "letters.", seconds=55, verified_by=RECOMP)
pc = lambda w: pos(w[0]) * pos(w[-1]) + len(w)
assert pc("CAKE") == 19 and pc("BOOK") == 26
ans = pc("DESK")
assert ans == 48
mcq(COD, NC, "Intermediate", "In a certain code, CAKE is written as 19 and BOOK is written as 26. How is DESK "
    "written in that code?", str(ans), ["44", "52", "26"], "Product of end-letter positions plus word length",
    "CAKE: C (3) × E (5) = 15, plus 4 letters = 19. BOOK: B (2) × K (11) = 22, plus 4 = 26. DESK: D (4) × K (11) = "
    f"44, plus 4 = {ans}.",
    ["CAKE: 3 × 5 + 4 = 19 (matches)", "BOOK: 2 × 11 + 4 = 26 (matches)", f"DESK: 4 × 11 + 4 = {ans}"],
    why_others_wrong="44 forgets to add the number of letters; 52 adds twice the number of letters; 26 is the "
                     "code of BOOK.", natural=int, seconds=55, verified_by=RECOMP)
sm = lambda w: sum(pos(c) for c in w) * len(w)
assert sm("ACE") == 27 and sm("BED") == 33
ans = sm("FACE")
assert ans == 60
mcq(COD, NC, "Intermediate", "In a certain code, ACE is written as 27 and BED as 33. How is FACE written in that "
    "code?", str(ans), ["15", "45", "75"], "Sum of positions multiplied by the number of letters",
    "ACE: (1 + 3 + 5) × 3 = 27. BED: (2 + 5 + 4) × 3 = 33. FACE: (6 + 1 + 3 + 5) × 4 = 15 × 4 = 60.",
    ["ACE: 9 × 3 = 27; BED: 11 × 3 = 33 (both match)", "FACE: 6 + 1 + 3 + 5 = 15", f"15 × 4 = {ans}"],
    why_others_wrong="15 is only the sum; 45 multiplies by 3 instead of the number of letters; 75 multiplies by 5.",
    natural=int, seconds=55, verified_by=RECOMP)
SUB = {"sky": "sea", "sea": "land", "land": "tree", "tree": "river", "river": "cloud"}
ans = SUB["sea"]
assert ans == "land"
mcq(COD, SW, "Intermediate",
    "If 'sky' is called 'sea', 'sea' is called 'land', 'land' is called 'tree', 'tree' is called 'river' and 'river' is "
    "called 'cloud', then where do fish live?", cap(ans), ["Sea", "River", "Cloud"],
    "Word substitution: answer with the new name of the real thing",
    "Fish live in the sea, and in this language the sea is called 'land'.",
    ["Real answer: fish live in the sea", "'sea' is called 'land'", "Answer: land"],
    why_others_wrong="'Sea' is the real word, not its code; 'River' is the code for tree; 'Cloud' is the code for "
                     "river.", seconds=30, verified_by=RECOMP)

# ---- Advanced: digit-symbol coding set
DTAB = {"1": "K", "2": "@", "3": "P", "4": "#", "5": "R", "6": "%", "7": "T", "8": "&", "9": "M", "0": "*"}


def num_code(n):
    c = [DTAB[d] for d in n]
    f, l = int(n[0]), int(n[-1])
    if f % 2 == 1 and l % 2 == 0:
        c[0] = c[-1] = DTAB[n[-1]]
    elif f % 2 == 0 and l % 2 == 0:
        c[0], c[-1] = c[-1], c[0]
    elif f % 2 == 0 and l % 2 == 1:
        c[0], c[-1] = "X", "Y"
    else:
        c[2] = "$"
    return "".join(c)


raw = lambda n: "".join(DTAB[d] for d in n)
DTXT = ("Study the digit codes and the conditions below.\n\n| Digit | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 0 |\n"
        "|---|---|---|---|---|---|---|---|---|---|---|\n| Code | " + " | ".join(DTAB[d] for d in "1234567890") +
        " |\n\nConditions (apply only the one that fits):\n(i) If the first digit is odd and the last digit is even, "
        "both are coded as the code of the last digit.\n(ii) If both the first and the last digits are even, their "
        "codes are interchanged.\n(iii) If the first digit is even and the last digit is odd, the first is coded as X "
        "and the last as Y.\n(iv) If both the first and the last digits are odd, the third digit is coded as $.\n\n"
        "Each question gives a five-digit number; choose its code.")
sid = stimulus("passage", "Digit codes with conditions", DTXT, None,
               "Find the parity of the first and last digits, apply the one matching condition, and code every other "
               "digit from the table.")
NQ = lambda num, correct, wrongs, expl, steps, **kw: mcq(
    COD, NC, "Advanced", f"What is the code for {num}?", correct, wrongs, "Table coding with conditions on the end "
    "digits", expl, steps, stimulus=sid, verified_by=RECOMP, **kw)
n = "47392"
ans = num_code(n)
assert ans == "@TPM#" and raw(n) == "#TPM@"
NQ(n, ans, [raw(n), "#TP$@", "XTPMY"],
   "4 and 2 are both even, so condition (ii) interchanges the codes of the end digits: 4 → # and 2 → @ swap places. "
   "The middle digits 7, 3, 9 are T, P, M.",
   ["First digit 4 (even), last digit 2 (even): condition (ii)", "Raw codes: # T P M @", f"Interchange ends: {ans}"],
   why_others_wrong="#TPM@ ignores the condition; #TP$@ applies (iv); XTPMY applies (iii).", seconds=60)
n = "58164"
ans = num_code(n)
assert ans == "#&K%#"
NQ(n, ans, [raw(n), "R&K%R", "#&K%R"],
   "5 is odd and 4 is even, so condition (i) codes both end digits as the code of 4 (#). The middle digits 8, 1, 6 "
   "are &, K, %.",
   ["First 5 (odd), last 4 (even): condition (i)", "Both ends → # (code of 4)", f"Code: {ans}"],
   why_others_wrong="R&K%# is the raw code; R&K%R uses the first digit's code; #&K%R swaps the ends instead.",
   seconds=60)
n = "82735"
ans = num_code(n)
assert ans == "X@TPY"
NQ(n, ans, [raw(n), "R@TP&", "&@$PR"],
   "8 is even and 5 is odd, so condition (iii) applies: the first digit becomes X and the last Y. The middle digits "
   "2, 7, 3 are @, T, P.",
   ["First 8 (even), last 5 (odd): condition (iii)", "Middle: 2 → @, 7 → T, 3 → P", f"Code: {ans}"],
   why_others_wrong="&@TPR is the raw code; R@TP& interchanges the ends (condition ii); &@$PR applies (iv).",
   seconds=60)
n = "39517"
ans = num_code(n)
assert ans == "PM$KT"
NQ(n, ans, [raw(n), "TMRKP", "XMRKY"],
   "3 and 7 are both odd, so condition (iv) applies: only the third digit (5) changes, to $. The code is P M $ K T.",
   ["First 3 (odd), last 7 (odd): condition (iv)", "Third digit 5 → $", f"Code: {ans}"],
   why_others_wrong="PMRKT is the raw code; TMRKP interchanges the ends; XMRKY applies condition (iii).", seconds=55)

# ---- Advanced: standalone
def oddeven(w):
    t = "".join(AL[(pos(c) - 1 + (2 if i % 2 == 0 else -3)) % 26] for i, c in enumerate(w))
    h = len(t) // 2
    return t[h:] + t[:h]


assert oddeven("GARDEN") == "AGKIXT"
ans = oddeven("SILVER")
assert ans == "SGOUFN"
mcq(COD, LC, "Advanced",
    "In a certain code, GARDEN is written as AGKIXT. The letters in odd places (1st, 3rd, 5th) are moved two places "
    "forward in the alphabet, the letters in even places are moved three places back, and then the two halves of the "
    "result are interchanged. How is SILVER written in that code?", ans, ["UFNSGO", "SGONFU", "UFTSGO"],
    "Position-dependent shifts followed by a half swap",
    "SILVER: S+2 = U, I−3 = F, L+2 = N, V−3 = S, E+2 = G, R−3 = O → UFNSGO. Interchanging the halves (UFN | SGO) gives "
    f"{ans}.",
    ["Check GARDEN: G+2 I, A−3 X, R+2 T, D−3 A, E+2 G, N−3 K → IXT AGK → AGKIXT (matches)",
     "SILVER → U F N S G O", f"Swap halves → {ans}"],
    why_others_wrong="UFNSGO skips the half swap; SGONFU reverses the second half; UFTSGO mis-shifts L.", seconds=75,
    verified_by=RECOMP)
VW = set("AEIOU")
cv = lambda w: sum(pos(c) for c in w if c not in VW) - sum(pos(c) for c in w if c in VW)
assert cv("BANK") == 26 and cv("LOAN") == 10
ALT_RULES = {"sum of all positions": lambda w: sum(pos(c) for c in w),
             "consonant sum": lambda w: sum(pos(c) for c in w if c not in VW),
             "vowels minus consonants": lambda w: -cv(w)}
assert all(f_("BANK") != 26 or f_("LOAN") != 10 for f_ in ALT_RULES.values())
ans = cv("CREDIT")
assert ans == 31
mcq(COD, NC, "Advanced",
    "In a certain code, BANK is written as 26 and LOAN is written as 10. Using the same rule, how is CREDIT written?",
    str(ans), ["59", "45", "14"], "Consonant total minus vowel total",
    "BANK: consonants B (2) + N (14) + K (11) = 27, vowel A (1); 27 − 1 = 26. LOAN: L (12) + N (14) = 26, vowels "
    "O (15) + A (1) = 16; 26 − 16 = 10. CREDIT: consonants C 3 + R 18 + D 4 + T 20 = 45; vowels E 5 + I 9 = 14; "
    f"45 − 14 = {ans}.",
    ["BANK: 27 − 1 = 26 ✓; LOAN: 26 − 16 = 10 ✓", "CREDIT consonants: 3 + 18 + 4 + 20 = 45",
     "CREDIT vowels: 5 + 9 = 14", f"45 − 14 = {ans}"],
    why_others_wrong="59 adds all six positions; 45 is the consonant total alone; 14 is the vowel total.",
    natural=int, seconds=80, verified_by=RECOMP)
assert sum(pos(c) for c in "CREDIT") == 59
SENTS = [(["fund", "flow", "is", "strong"], ["ve", "ko", "ri", "ta"]),
         (["strong", "rupee", "flow"], ["ta", "mu", "ko"]),
         (["rupee", "is", "weak"], ["mu", "ri", "zi"]),
         (["weak", "fund", "outlook"], ["zi", "ve", "pa"])]
assert sentence_solve(SENTS, "fund") == {"ve"} and sentence_solve(SENTS, "outlook") == {"pa"}
assert sentence_solve(SENTS, "strong") == {"ta", "ko"} and sentence_solve(SENTS, "is") == {"ri"}
mcq(COD, SW, "Advanced",
    "In a certain code language:\n'fund flow is strong' is written as 've ko ri ta',\n'strong rupee flow' is written "
    "as 'ta mu ko',\n'rupee is weak' is written as 'mu ri zi', and\n'weak fund outlook' is written as 'zi ve pa'.\n"
    "(The codes of the words in a sentence may appear in any order.)\n\nWhat is the code for 'fund is'?", "ve ri",
    ["ve ko", "ri zi", "ta ri"], "Chained elimination across four sentences",
    "{strong, flow} = {ta, ko} (sentences 1 and 2), so rupee = mu (sentence 2). Then from sentence 3, rupee = mu "
    "leaves {is, weak} = {ri, zi}; weak also appears in sentence 4, whose codes include zi but not ri, so weak = zi "
    "and is = ri. From sentence 1 the code left for fund is ve.",
    ["Sentences 1 & 2: {strong, flow} = {ta, ko} ⇒ rupee = mu", "Sentences 3 & 4 share weak and zi ⇒ weak = zi",
     "Sentence 3: is = ri", "Sentence 1: fund = ve", "fund is = ve ri"],
    why_others_wrong="ko belongs to strong or flow; zi is weak; ta belongs to strong or flow.", seconds=90,
    verified_by=RECOMP)

# ================================================================================================ ALPHANUMERIC SERIES
ALN = "Alphanumeric Series"
SR = "K 7 @ B 3 E # 9 M U 4 $ R 2 % A 8 T & 6 Q".split()
assert len(SR) == 21
a_, b_ = 7, len(SR) - 5 + 1
mid = (a_ + b_) // 2
ans = SR[mid - 1]
assert (a_, b_, mid) == (7, 17, 12) and ans == "$"
mcq(ALN, "Position-based", "Intermediate", series_intro(" ".join(SR)) +
    "\n\nWhich element is exactly midway between the 7th element from the left end and the 5th element from the right "
    "end?", ans, ["4", "R", "U"], "Converting a right-end position before finding the midpoint",
    f"The series has 21 elements, so the 5th from the right is the 17th from the left. Midway between positions 7 "
    f"and 17 is position 12: {ans}.",
    ["Total elements = 21", "5th from the right = 21 − 5 + 1 = 17th from the left",
     "Midpoint of 7 and 17 = 12", f"12th element = {ans}"],
    why_others_wrong="4 and R are the 11th and 13th elements (off by one); U is the 10th.", seconds=60,
    verified_by=RECOMP)
assert (SR[10], SR[12], SR[9]) == ("4", "R", "U")
SR = "5 G @ 3 K 8 E # 2 W 7 $ L 4 I 9 % P 6 & N 1 Y".split()
hits = [int(SR[i]) for i in range(len(SR) - 1) if is_d(SR[i]) and is_l(SR[i + 1]) and SR[i + 1] not in "AEIOU"]
total = sum(hits)
assert hits == [5, 3, 2, 1] and total == 11
mcq(ALN, "Symbol and number series", "Advanced", series_intro(" ".join(SR)) +
    "\n\nWhat is the sum of all the numbers in the arrangement each of which is immediately followed by a consonant?",
    str(total), ["15", "21", "17"], "Scanning number–consonant pairs and adding",
    "Numbers immediately followed by a consonant: " + "; ".join(
        f"{SR[i]} {SR[i + 1]}" for i in range(len(SR) - 1) if is_d(SR[i]) and is_l(SR[i + 1])
        and SR[i + 1] not in "AEIOU") + f". Their sum is {' + '.join(map(str, hits))} = {total}.",
    ["Check each number and the element after it", "Discard those followed by a vowel (8 E, 4 I) or a symbol "
     "(7 $, 9 %, 6 &)", "Qualifying: " + ", ".join(map(str, hits)), f"Sum = {total}"],
    natural=int, seconds=75, verified_by=RECOMP)

# ================================================================================================ ALPHABET TEST
ABT = "Alphabet Test"
ans = AL[(26 - 12 + 1) + 5 - 1]
assert ans == "T"
mcq(ABT, "Letter position", "Basic", "Which letter is 5th to the right of the 12th letter from the right end of the "
    "English alphabet?", ans, ["J", "U", "S"], "Converting a right-end position",
    "The 12th letter from the right is the (27 − 12) = 15th from the left, O. Five places to its right is the 20th "
    f"letter: {ans}.", ["12th from the right = 15th from the left = O", "15 + 5 = 20", f"20th letter = {ans}"],
    why_others_wrong="J is 5th to the left of O; U and S are off by one.", seconds=30, verified_by=RECOMP)
CANDW = ["PARENT", "MASTER", "PRINTED", "TRAMPLE"]
canform = lambda w, src: not (Counter(w) - Counter(src))
okw = [w for w in CANDW if canform(w, "DEPARTMENT")]
assert okw == ["PARENT"]
mcq(ABT, "Word formation", "Basic", "Which of the following words can be formed using the letters of the word "
    "'DEPARTMENT' (each letter used no more often than it appears in DEPARTMENT)?", okw[0],
    [w for w in CANDW if w != okw[0]], "Checking letters against the source word",
    "DEPARTMENT has D, E, E, P, A, R, T, T, M, N. PARENT uses P, A, R, E, N, T, all available.",
    ["PARENT: P, A, R, E, N, T — all present", "MASTER needs S (absent)", "PRINTED needs I (absent)",
     "TRAMPLE needs L (absent)"], seconds=35, verified_by=RECOMP)
W = "MOBILE"
pr = letter_pairs(W)
a, w = count_opts(len(pr))
mcq(ABT, "Pairs of letters", "Basic", f"How many pairs of letters are there in the word '{W}' each of which has as "
    "many letters between them in the word as in the English alphabet (counting both forward and backward)?", a, w,
    "Comparing word gaps with alphabet gaps",
    "Pairs found: " + (", ".join(f"{x}{y}" for x, y in pr) or "none") + f". Total {len(pr)}.",
    ["Positions: " + ", ".join(f"{ch} = {pos(ch)}" for ch in W),
     "For each pair, compare the gap in the word with the gap in the alphabet",
     "Matching pairs: " + (", ".join(f"{x}–{y}" for x, y in pr) or "none")], natural=by_num, seconds=45,
    verified_by=RECOMP)
btw = 26 - 9 + 1 - 6 - 1
assert btw == 11
mcq(ABT, "Letter position", "Basic", "How many letters are there between the 6th letter from the left end and the "
    "9th letter from the right end of the English alphabet?", str(btw), ["10", "12", "13"],
    "Counting letters between two positions",
    "The 6th letter from the left is F (6). The 9th from the right is the 18th from the left, R. Between positions 6 "
    f"and 18 there are 18 − 6 − 1 = {btw} letters.", ["6th from left = F", "9th from right = 27 − 9 = 18th = R",
                                                      f"Between: {btw}"], natural=int, seconds=30, verified_by=RECOMP)
W = "GRAPHIC"
newl = [AL[pos(c) - 2] if c in VW else AL[pos(c) % 26] for c in W]
rep = sorted(k for k, v in Counter(newl).items() if v > 1)
assert newl == list("HSZQIHD") and rep == ["H"]
mcq(ABT, "Letter position", "Intermediate",
    "In the word 'GRAPHIC', each consonant is replaced by the letter immediately after it in the English alphabet and "
    "each vowel by the letter immediately before it. How many letters appear more than once in the new letter group?",
    num_word(len(rep)), ["None", "Two", "Three"], "Transform, then look for repeats",
    "G→H, R→S, A→Z, P→Q, H→I, I→H, C→D gives H S Z Q I H D. Only H appears twice.",
    ["Consonants +1: G→H, R→S, P→Q, H→I, C→D", "Vowels −1: A→Z, I→H", "New group: HSZQIHD", "Repeated: H only"],
    why_others_wrong="'None' misses that H (from G) and H (from I) coincide.", natural=by_num, seconds=50,
    verified_by=RECOMP)
W = "BACKGROUND"
pr = letter_pairs(W)
a, w = count_opts(len(pr))
mcq(ABT, "Pairs of letters", "Advanced", f"How many pairs of letters are there in the word '{W}' each of which has "
    "as many letters between them in the word as in the English alphabet (counting both forward and backward)?",
    a, w, "Exhaustive pair checking in a ten-letter word",
    "Pairs found: " + (", ".join(f"{x}{y}" for x, y in pr) or "none") + f". Total {len(pr)}.",
    ["Positions: " + ", ".join(f"{ch} = {pos(ch)}" for ch in W),
     "Check every pair (i, j): |alphabet gap| must equal j − i",
     "Matching pairs: " + (", ".join(f"{x}–{y}" for x, y in pr) or "none")], natural=by_num, seconds=80,
    verified_by=RECOMP)
W = "NUMERICAL"
srt = sorted(W)
same = [W[i] for i in range(len(W)) if srt[i] == W[i]]
a, w = count_opts(len(same))
mcq(ABT, "Letter position", "Advanced", f"If the letters of the word '{W}' are arranged in alphabetical order from "
    "left to right, how many letters will remain in the same position as in the original word?", a, w,
    "Sorting a word and comparing positions",
    f"Original: {' '.join(W)}; sorted: {' '.join(srt)}. Letters in the same place: " + (", ".join(same) or "none") +
    f". Total {len(same)}.", [f"Sorted: {''.join(srt)}", "Compare place by place",
                              "Unchanged: " + (", ".join(same) or "none")], natural=by_num, seconds=70,
    verified_by=RECOMP)
W = "COMPUTERS"
newl = [AL[pos(c) % 26] if i % 2 == 0 else AL[pos(c) - 2] for i, c in enumerate(W)]
rs = sorted(newl, reverse=True)
ans = rs[3]
mcq(ABT, "Letter position", "Advanced",
    f"In the word '{W}', each letter in an odd place (1st, 3rd, …) is replaced by the next letter of the English "
    "alphabet and each letter in an even place by the previous letter. The new letters are then arranged in reverse "
    "alphabetical order (Z to A) from left to right. Which letter will be 4th from the left?", ans,
    [x for x in ["T", "Q", "D", "S", "N", "R"] if x != ans][:3], "Transform, sort in reverse, count",
    f"New letters: {' '.join(newl)}. In reverse alphabetical order: {' '.join(rs)}. The 4th from the left is {ans}.",
    ["Odd places +1, even places −1: " + " ".join(f"{c}→{n}" for c, n in zip(W, newl)),
     "Reverse order: " + " ".join(rs), f"4th from the left: {ans}"], seconds=80, verified_by=RECOMP)
CANDW = ["CASINO", "OASIS", "ACTION", "STATION"]
bad = [w for w in CANDW if not canform(w, "ASSOCIATION")]
assert bad == ["STATION"]
mcq(ABT, "Word formation", "Advanced", "Which of the following words CANNOT be formed using the letters of the word "
    "'ASSOCIATION' (each letter used no more often than it appears in ASSOCIATION)?", bad[0],
    [w for w in CANDW if w != bad[0]], "Letter counts matter, not just letters",
    "ASSOCIATION has A×2, S×2, O×2, I×2, C, T and N. STATION needs T twice, but there is only one T.",
    ["Letter counts: A2 S2 O2 I2 C1 T1 N1", "CASINO, OASIS, ACTION: all within these counts",
     "STATION: S, T, A, T, I, O, N → two Ts needed: cannot be formed"], seconds=60, verified_by=RECOMP)
HALF = AL[:13][::-1] + AL[13:]
ans = HALF[(26 - 17 + 1) + 7 - 1]
mcq(ABT, "Letter position", "Advanced",
    "If the first half of the English alphabet (A to M) is written in reverse order and the second half (N to Z) is "
    "left as it is, which letter will be 7th to the right of the 17th letter from the right end?", ans,
    [x for x in [AL[16], HALF[9], HALF[15]] if x != ans][:3] + ([] if len({AL[16], HALF[9], HALF[15]} - {ans}) == 3
                                                                else ["W"]),
    "Positions in a partly reversed alphabet",
    f"The new sequence is {' '.join(HALF)}. The 17th from the right is the 10th from the left ({HALF[9]}); 7 places "
    f"to its right is the 17th from the left: {ans}.",
    ["New order: " + "".join(HALF), "17th from the right = 26 − 17 + 1 = 10th from the left = " + HALF[9],
     f"10 + 7 = 17th from the left = {ans}"], seconds=70, verified_by=RECOMP)

# ================================================================================================ NUMBER-BASED
NUM = "Number Series (Reasoning)"
NS = [586, 293, 741, 958, 324]
NSTXT = "Study the following five three-digit numbers and answer the questions.\n\n" + "   ".join(map(str, NS))
sid = stimulus("data_table", "Five three-digit numbers", NSTXT, None,
               "Digits of each number: " + "; ".join(f"{n}: {' '.join(str(n))}" for n in NS) + ".")
NQ5 = lambda sub, text, correct, wrongs, concept, expl, steps, **kw: mcq(
    NUM, sub, "Intermediate", text, correct, wrongs, concept, expl, steps, stimulus=sid, verified_by=RECOMP, **kw)
rev = {n: int(str(n)[::-1]) for n in NS}
r_sorted = sorted(NS, key=rev.get, reverse=True)
ans = r_sorted[1]
NQ5("Three-digit number questions", "If the digits of each number are reversed, which original number gives the "
    "second largest new number?", str(ans), [str(x) for x in NS if x != ans][:3], "Reversing digits, then ordering",
    "Reversed: " + ", ".join(f"{n} → {rev[n]}" for n in NS) + f". In descending order: "
    + ", ".join(str(rev[n]) for n in r_sorted) + f". The second largest, {rev[ans]}, comes from {ans}.",
    ["Reverse each: " + ", ".join(f"{n}→{rev[n]}" for n in NS), "Order: " + " > ".join(str(rev[n]) for n in r_sorted)],
    seconds=50)
mid_sub = {n: n - 10 for n in NS}
allodd = [n for n in NS if all(int(d) % 2 for d in str(mid_sub[n]))]
a, w = count_opts(len(allodd))
NQ5("Number-based digit operations", "If 1 is subtracted from the middle digit of each number, how many of the new "
    "numbers will have all three digits odd?", a, w, "Digit operation, then a property check",
    "New numbers: " + ", ".join(str(mid_sub[n]) for n in NS) + ". All digits odd: " +
    (", ".join(str(mid_sub[n]) for n in allodd) or "none") + f". Count {len(allodd)}.",
    ["Subtract 10 from each number (middle digit − 1)", "New: " + ", ".join(str(mid_sub[n]) for n in NS),
     "All-odd: " + (", ".join(str(mid_sub[n]) for n in allodd) or "none")], natural=by_num, seconds=50)
asc = sorted(NS)
ans = sum(map(int, str(asc[1])))
NQ5("Three-digit number questions", "If the numbers are arranged in ascending order, what is the sum of the digits "
    "of the second number from the left?", str(ans), [str(x) for x in (ans - 1, ans + 2, ans + 4)],
    "Ordering, then digit sum", f"Ascending: {', '.join(map(str, asc))}. The second is {asc[1]}; digit sum "
    f"{' + '.join(str(asc[1]))} = {ans}.", ["Ascending: " + ", ".join(map(str, asc)), f"Second: {asc[1]}",
                                           f"Digit sum: {ans}"], natural=int, seconds=45)
hi, lo = max(NS), min(NS)
ans = int(str(hi)[0]) * int(str(lo)[-1])
NQ5("Number-based digit operations", "What is the product of the first digit of the highest number and the last "
    "digit of the lowest number?", str(ans), [str(x) for x in sorted({27, 36, 18, 45, 24} - {ans})[:3]],
    "Identifying extremes, then operating on digits",
    f"Highest = {hi} (first digit {str(hi)[0]}); lowest = {lo} (last digit {str(lo)[-1]}); product = {ans}.",
    [f"Highest: {hi}", f"Lowest: {lo}", f"{str(hi)[0]} × {str(lo)[-1]} = {ans}"], natural=int, seconds=40)
sw12 = {n: int(str(n)[1] + str(n)[0] + str(n)[2]) for n in NS}
big = [n for n in NS if sw12[n] > 500]
a, w = count_opts(len(big))
NQ5("Number-based digit operations", "If the first and second digits of each number are interchanged, how many of the "
    "new numbers will be greater than 500?", a, w, "Digit interchange and comparison",
    "New numbers: " + ", ".join(f"{n} → {sw12[n]}" for n in NS) + ". Greater than 500: " +
    (", ".join(str(sw12[n]) for n in big) or "none") + f". Count {len(big)}.",
    ["Interchange 1st and 2nd digits: " + ", ".join(f"{n}→{sw12[n]}" for n in NS),
     "Compare each with 500"], natural=by_num, seconds=45)

# ================================================================================================ RANKING
RNK = "Ranking and Order"
n_, r_ = 40, 14
s_ = r_ + 9
ans = n_ - s_ + 1
assert ans == 18
mcq(RNK, "Position in a row", "Intermediate",
    "In a row of 40 children facing north, Rohan is 14th from the left end. Sameer sits ninth to the right of Rohan. "
    "What is Sameer's position from the right end?", ORDN(ans), ["17th", "19th", "23rd"],
    "Moving along the row, then converting ends",
    f"Sameer is 14 + 9 = 23rd from the left, so from the right he is 40 − 23 + 1 = {ans}th.",
    ["Sameer from the left = 14 + 9 = 23", f"From the right = 40 − 23 + 1 = {ans}"],
    why_others_wrong="23rd is his position from the left; 17th and 19th are off-by-one conversions.",
    natural=lambda t: int(t[:-2]), seconds=40, verified_by=RECOMP)

# ================================================================================================ INPUT-OUTPUT
IOT = "Input and Output"
ROMAN = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII"]


def len_machine(words):
    """Each step: the shortest unarranged word (ties: alphabetically first) moves to the immediate right of the words
    already arranged at the left. Every step must change the line."""
    cur, steps = list(words), []
    for k in range(len(cur) - 1):
        rest = cur[k:]
        nxt = sorted(rest, key=lambda w: (len(w), w))[0]
        new = cur[:k] + [nxt] + [x for x in rest if x != nxt]
        assert new != cur, k
        cur = new
        steps.append(cur[:])
    assert cur == sorted(words, key=lambda w: (len(w), w))
    return steps


INP = "planet ox cradle mint sun bridge eagle".split()
st = len_machine(INP)
assert len(st) == 6
ALLST = [f"Step {ROMAN[i]}: " + " ".join(s_) for i, s_ in enumerate(st)]
sid = stimulus("input_output", "Machine: shortest word to the left",
               "A word arrangement machine rearranges a line of words step by step. In each step it takes the word "
               "with the fewest letters among the words not yet arranged (if two such words have the same number of "
               "letters, the one that comes first in alphabetical order) and places it immediately to the right of "
               "the words already arranged (in Step I, at the extreme left). The other words keep their order. The "
               "machine stops when all the words are arranged.\n\nInput: " + " ".join(INP), None,
               "Steps for the given input:\n\n" + "\n".join(ALLST))
IQ = lambda text, correct, wrongs, expl, steps_, **kw: mcq(
    IOT, "Word rearrangement", "Basic", text, correct, wrongs, "Simulating a selection machine by word length", expl,
    steps_, stimulus=sid, verified_by=RECOMP, **kw)
e = st[2]
ans = e[e.index("mint") + 2]
assert ans == "cradle"
IQ("In Step III, which word is second to the right of 'mint'?", ans, ["planet", "bridge", "eagle"],
   f"Step III is '{' '.join(e)}'. Two places to the right of 'mint' is '{ans}'.", ALLST[:3], seconds=50)
k = next(i for i, s_ in enumerate(st) if s_[s_.index("mint") + 1] == "eagle") + 1
assert k == 4
IQ("In which step does 'eagle' appear immediately to the right of 'mint' for the first time?", f"Step {ROMAN[k - 1]}",
   ["Step III", "Step V", "Step VI"], "eagle (5 letters) is the fourth word picked, after ox, sun and mint, so it "
   "lands next to mint in Step IV.", ALLST[:4], natural=lambda t: ROMAN.index(t.split()[1]), seconds=50)
p_ = st[1].index("planet") + 1
IQ("What is the position of 'planet' from the left end in Step II?", ORDN(p_), ["2nd", "4th", "6th"],
   f"Step II is '{' '.join(st[1])}'; planet is {ORDN(p_)} from the left.", ALLST[:2],
   natural=lambda t: int(t[:-2]), seconds=45)
assert p_ == 3


def right_machine(nums):
    """Each step: the largest unarranged number moves to the immediate left of the numbers already arranged at the
    right end. Every step must change the line."""
    cur, steps, n = list(nums), [], len(nums)
    for k in range(n - 1):
        rest = cur[:n - k]
        nxt = max(rest)
        new = [x for x in rest if x != nxt] + [nxt] + cur[n - k:]
        assert new != cur, k
        cur = new
        steps.append(cur[:])
    assert cur == sorted(nums)
    return steps


INP = [38, 91, 24, 67, 45, 82, 13]
st = right_machine(INP)
assert len(st) == 6
ALLST = [f"Step {ROMAN[i]}: " + " ".join(map(str, s_)) for i, s_ in enumerate(st)]
sid = stimulus("input_output", "Machine: largest number to the right",
               "A number arrangement machine rearranges a line of numbers step by step. In each step it takes the "
               "largest number among those not yet arranged and places it immediately to the left of the numbers "
               "already arranged at the right end (in Step I, at the extreme right). The other numbers keep their "
               "order. The machine stops when all the numbers are arranged.\n\nInput: " + " ".join(map(str, INP)),
               None, "Steps for the given input:\n\n" + "\n".join(ALLST))
JQ2 = lambda text, correct, wrongs, expl, steps_, **kw: mcq(
    IOT, "Number rearrangement", "Basic", text, correct, wrongs, "Simulating a descending selection to the right",
    expl, steps_, stimulus=sid, verified_by=RECOMP, **kw)
ans = st[2][2]
assert ans == 45
JQ2("Which number is 3rd from the left end in Step III?", str(ans), ["67", "13", "24"],
    f"Step III is '{' '.join(map(str, st[2]))}'; its 3rd number from the left is {ans}.", ALLST[:3], seconds=45)
target = [38, 24, 13, 45, 67, 82, 91]
k = st.index(target) + 1
assert k == 4
JQ2("In which step does the arrangement read '38 24 13 45 67 82 91'?", f"Step {ROMAN[k - 1]}",
    ["Step III", "Step V", "Step VI"], "Numbers are fixed from the right in the order 91, 82, 67, 45. The line with "
    "45 just placed is Step IV.", ALLST[:5], natural=lambda t: ROMAN.index(t.split()[1]), seconds=50)
JQ2("How many steps does the machine take to arrange the given input?", str(len(st)), ["5", "7", "4"],
    "Seven numbers need six placements; the last number falls into place on its own. The input is fully arranged at "
    "Step VI, and no step is wasted because each step moves a number.", ALLST, natural=int, seconds=45)

# ---- Intermediate (standalone)


def pair_machine(items):
    words = [x for x in items if not x.isdigit()]
    nums = [x for x in items if x.isdigit()]
    wo = sorted(words, key=lambda w: (len(w), w))
    no = sorted(nums, key=int, reverse=True)
    cur, block, steps = list(items), [], []
    for w_, n_ in zip(wo, no):
        block += [w_, n_]
        cur = block + [x for x in items if x not in block]
        steps.append(cur[:])
    return steps


INP = "lake 16 ore 81 bank 57 fig 34".split()
st = pair_machine(INP)
ans = " ".join(st[1])
assert ans == "fig 81 ore 57 lake 16 bank 34"
mcq(IOT, "Mixed machine", "Intermediate",
    "A machine rearranges a line of words and numbers step by step. In each step it takes the word with the fewest "
    "letters among the words not yet arranged (ties broken alphabetically) together with the largest number not yet "
    "arranged, and places that word and then that number immediately to the right of the elements already arranged "
    "(in Step I, at the extreme left). The other elements keep their order.\n\nInput: " + " ".join(INP) +
    "\n\nWhich of the following is Step II?", ans,
    ["fig 81 bank 57 ore 34 lake 16", "ore 81 fig 57 lake 16 bank 34", "fig 81 ore 57 bank 34 lake 16"],
    "Word–number pairs placed at the left",
    "Words by length: fig and ore (3 letters, fig first), then bank and lake (4 letters). Numbers in descending "
    "order: 81, 57, 34, 16. Step I places 'fig 81'; Step II places 'ore 57'. The rest keep their order: lake 16 bank 34.",
    [f"Step {ROMAN[i]}: " + " ".join(s_) for i, s_ in enumerate(st[:2])],
    why_others_wrong="'fig 81 ore 57 bank 34 lake 16' is Step III; the other two use the wrong order of words.",
    seconds=70, verified_by=RECOMP)
dsum = lambda n: sum(map(int, str(n)))


def dsum_machine(nums):
    cur, steps = list(nums), []
    for k in range(len(cur)):
        rest = cur[k:]
        nxt = max(rest, key=dsum)
        new = cur[:k] + [nxt] + [x for x in rest if x != nxt]
        if new == cur:
            continue
        cur = new
        steps.append(cur[:])
    return steps


INP = [91, 58, 27, 66, 34, 79]
assert len({dsum(n) for n in INP}) == len(INP)
st = dsum_machine(INP)
assert len(st) == 3 and st[-1] == sorted(INP, key=dsum, reverse=True)
ans = st[1][3]
assert ans == 27
mcq(IOT, "Number rearrangement", "Intermediate",
    "A machine rearranges numbers step by step. In each step it takes, among the numbers not yet arranged, the one "
    "with the largest sum of digits and places it immediately to the right of the numbers already arranged (in Step "
    "I, at the extreme left). The other numbers keep their order, and the machine stops as soon as the numbers stand "
    "in descending order of digit sum.\n\nInput: " + " ".join(map(str, INP)) +
    "\n\nWhich number is 4th from the left end in Step II?", str(ans), ["91", "66", "34"],
    "Ordering by digit sum", "Digit sums: " + ", ".join(f"{n} → {dsum(n)}" for n in INP) +
    f". Step I: {' '.join(map(str, st[0]))}. Step II: {' '.join(map(str, st[1]))}. The 4th number is {ans}.",
    [f"Step {ROMAN[i]}: " + " ".join(map(str, s_)) for i, s_ in enumerate(st)],
    why_others_wrong="91 is 3rd and 66 5th in Step II; 34 is at the right end.", seconds=70, verified_by=RECOMP)

# ---- Advanced: word-number machine with transformations


def adv_machine(items):
    words = sorted(x for x in items if not x.isdigit())
    nums = sorted((int(x) for x in items if x.isdigit()), reverse=True)
    block, rest, steps = [], list(items), []
    for w_, n_ in zip(words, nums):
        rest.remove(w_)
        rest.remove(str(n_))
        block += [w_[:-1], str(n_ - len(w_))]
        steps.append(block + rest)
    return steps


INP = "mango 47 ink 92 slate 35 bold 68 crane 13".split()
st = adv_machine(INP)
assert len(st) == 5 and st[-1] == "bol 88 cran 63 in 44 mang 30 slat 8".split()
ALLST = [f"Step {ROMAN[i]}: " + " ".join(s_) for i, s_ in enumerate(st)]
sid = stimulus("input_output", "Machine: words lose a letter, numbers lose the word length",
               "A word and number arrangement machine rearranges a line step by step. In each step it takes the word "
               "that comes first in alphabetical order among the words not yet arranged and the largest number not "
               "yet arranged. The word is written without its last letter, and the number is reduced by the number "
               "of letters in that word (counted before the letter is removed). The shortened word and then the "
               "reduced number are placed immediately to the right of the elements already arranged (in Step I, at "
               "the extreme left). All other elements keep their order. The machine stops when every element has "
               "been arranged.\n\nInput: " + " ".join(INP), None,
               "Steps for the given input:\n\n" + "\n".join(ALLST))
AQ = lambda text, correct, wrongs, expl, steps_, **kw: mcq(
    IOT, "Mixed machine", "Advanced", text, correct, wrongs, "Two transformations per step", expl, steps_,
    stimulus=sid, verified_by=RECOMP, **kw)
AQ("How many steps does the machine take for the given input?", str(len(st)), ["4", "6", "10"],
   "Five words and five numbers are arranged one pair per step, so five steps are needed (Step V is the last).",
   ALLST, natural=int, seconds=75)
e = st[2]
ans = e[e.index("in") + 3]
assert ans == "slate"
AQ("In Step III, which element is 3rd to the right of 'in'?", ans, ["44", "35", "mango"],
   f"Step III is '{' '.join(e)}'. To the right of 'in' come 44, mango and then slate, the 3rd.",
   ALLST[:3], why_others_wrong="44 is 1st and mango 2nd to the right of 'in'; 35 is 4th.", seconds=80)
total = sum(int(x) for x in st[-1] if x.isdigit())
assert total == 233
AQ("What is the sum of all the numbers in the last step?", str(total), ["255", "210", "243"],
   "The last step is 'bol 88 cran 63 in 44 mang 30 slat 8': 88 + 63 + 44 + 30 + 8 = 233.",
   [ALLST[-1], "Each number = original − letters of its paired word: 92−4, 68−5, 47−3, 35−5, 13−5"],
   why_others_wrong="255 is the sum of the original numbers; 210 and 243 subtract the wrong word lengths.",
   natural=int, seconds=80)
assert sum(int(x) for x in INP if x.isdigit()) == 255
e = st[1]
gap = abs(e.index("cran") - e.index("35")) - 1
assert gap == 5
AQ("In Step II, how many elements are there between 'cran' and '35'?", num_word(gap), ["Four", "Six", "Three"],
   f"Step II is '{' '.join(e)}'. Between 'cran' (3rd) and '35' (9th) lie 63, mango, 47, ink and slate: five.",
   ALLST[:2], natural=by_num, seconds=75)

# ================================================================================================ DATA SUFFICIENCY
def ds2_q(diff, question, st1, st2, models, f1, f2, answer, expected, drop, explanation, steps, seconds=50):
    got = ds2(models, f1, f2, answer)
    assert got == expected, (question, got)
    keys = [k for k in "ABENT" if k != drop]
    assert expected in keys and len(keys) == 4
    opts = [DS2[k] for k in keys]
    return fixed(DSF, "Two-statement", diff, DS_HEAD + f"Question: {question}\n\nI. {st1}\nII. {st2}", opts,
                 DS2[expected], "Data sufficiency: test each statement alone, then together", explanation, steps,
                 seconds=seconds, verified_by=ENUM)


# ---- Basic
months = [{"m": m} for m in range(1, 13)]
ds2_q("Basic", "In which month was Rahul born?", "Rahul was born in a month after March but before May.",
      "Rahul was born in a month that has 30 days and comes before June.", months,
      lambda d: 3 < d["m"] < 5, lambda d: MDAYS[d["m"]] == 30 and d["m"] < 6, lambda d: d["m"], "E", "N",
      "I leaves only April. II: the 30-day months before June are only April. Each statement alone answers it.",
      ["I: after March and before May → April: sufficient", "II: 30-day months are April, June, September, November; "
       "before June → April: sufficient", "Either statement alone is sufficient"], seconds=40)
grid = range(-6, 7)
pts_models = [{"A": (ax, ay), "C": (cx, cy)} for ax in grid for ay in grid for cx in grid for cy in grid
              if (ax, ay) != (0, 0)]
ds2_q("Basic", "In which direction is point A with respect to point B?",
      "A is 5 m north of point C, and C is 5 m west of B.", "A is to the north of C.", pts_models,
      lambda d: d["C"] == (-5, 0) and d["A"] == (-5, 5), lambda d: d["A"][0] == d["C"][0] and d["A"][1] > d["C"][1],
      lambda d: compass(*d["A"]), "A", "T",
      "From I, C = (−5, 0) and A = (−5, 5) with B at the origin, so A is north-west of B. II gives no link to B.",
      ["I: B (0, 0) → C (−5, 0) → A (−5, 5): North-West: sufficient", "II: says nothing about B: not sufficient",
       "I alone is sufficient"], seconds=40)
five = list("ABCDE")
models = [dict(zip(five, p)) for p in itertools.permutations(range(1, 6))]
ds2_q("Basic", "Five persons A, B, C, D and E sit in a row, all facing north. Who sits exactly in the middle of the "
      "row?", "A sits at the extreme left end, and B sits third to the right of A.",
      "D sits at the extreme right end, and C sits second to the left of D.", models,
      lambda m: m["A"] == 1 and m["B"] == 4, lambda m: m["D"] == 5 and m["C"] == 3,
      lambda m: next(p for p in five if m[p] == 3), "B", "E",
      "I places A (1) and B (4); seat 3 could be C, D or E. II places D at 5 and C at 3, the middle seat.",
      ["I: A = 1, B = 4 → middle (seat 3) not fixed: not sufficient", "II: D = 5, C = 3 → C is in the middle: "
       "sufficient", "II alone is sufficient"], seconds=45)
# ---- Intermediate
d1 = [(["sun", "is", "hot"], ["ka", "lo", "mi"]), (["hot", "tea"], ["mi", "pu"])]
d2 = [(["sun", "rises", "early"], ["ka", "zo", "ve"]), (["early", "bird"], ["ve", "ru"])]
r1, r2, r12 = sentence_solve(d1, "sun"), sentence_solve(d2, "sun"), sentence_solve(d1 + d2, "sun")
assert (r1, r2, r12) == ({"ka", "lo"}, {"ka", "zo"}, {"ka"})
fixed(DSF, "Two-statement", "Intermediate",
      DS_HEAD + "Question: In a certain code language, what is the code for 'sun'?\n\n"
      "I. 'sun is hot' is written as 'ka lo mi', and 'hot tea' is written as 'mi pu'.\n"
      "II. 'sun rises early' is written as 'ka zo ve', and 'early bird' is written as 've ru'.",
      [DS2[k] for k in "ABNT"], DS2["T"], "Data sufficiency with sentence coding",
      "I: hot = mi, so sun is ka or lo. II: early = ve, so sun is ka or zo. Together, the only code common to both "
      "possibilities is ka.",
      ["I: hot = mi ⇒ {sun, is} = {ka, lo}: not sufficient", "II: early = ve ⇒ {sun, rises} = {ka, zo}: not "
       "sufficient", "I + II: sun ∈ {ka, lo} ∩ {ka, zo} = {ka}: sufficient", "Both statements together are necessary"],
      seconds=60, verified_by=ENUM)
four = list("PQRS")
models = [dict(zip(four, p)) for p in itertools.permutations(range(4))]  # larger = older
ds2_q("Intermediate", "Among P, Q, R and S, each of a different age, who is the youngest?",
      "Q is younger than each of P, R and S.", "R is older than S.", models,
      lambda m: all(m["Q"] < m[x] for x in "PRS"), lambda m: m["R"] > m["S"],
      lambda m: min(four, key=m.get), "A", "E",
      "I directly makes Q the youngest. II compares only R and S, so the youngest could be P, Q or S.",
      ["I: Q < P, R, S ⇒ Q is the youngest: sufficient", "II: R > S only: not sufficient", "I alone is sufficient"],
      seconds=40)
six = list("ABCDEF")
models = []
for perm in itertools.permutations(range(1, 6)):
    m = dict(zip(six[1:], perm))
    m["A"] = 0
    models.append(m)
ds2_q("Intermediate", "Six persons A, B, C, D, E and F sit around a circular table, equally spaced and facing the "
      "centre. Who sits opposite A?", "B sits second to the right of A, and C sits immediately to the left of B.",
      "D sits second to the left of C, and E is not an immediate neighbour of B.", models,
      lambda m: m["B"] == 2 and m["C"] == 1,
      lambda m: m["D"] == (m["C"] - 2) % 6 and (m["E"] - m["B"]) % 6 not in (1, 5),
      lambda m: next(p for p in six if m[p] == 3), "T", "E",
      "Number seats 0–5 to A's right (opposite A = seat 3). I: B = 2, C = 1; seats 3, 4, 5 are open. II alone fixes "
      "nothing about A. Together: D = 1 − 2 = seat 5; E is not next to B (seat 2), so E = 4 and F = 3, opposite A.",
      ["I: B = 2, C = 1; D, E, F in seats 3–5: not sufficient", "II: D, C, E, B relative to each other only: not "
       "sufficient", "I + II: D = 5, E ≠ 3 (next to B) ⇒ E = 4, F = 3 ⇒ F is opposite A",
       "Both statements together are necessary"], seconds=70)
models = [dict(zip(five, p)) for p in itertools.permutations(range(1, 6))]  # floors 1..5
ds2_q("Intermediate", "Five persons A, B, C, D and E live on the five floors of a building, one on each floor "
      "(floor 1 is the lowermost). Who lives on the topmost floor?",
      "Only E lives above D, and D lives immediately above B.", "C lives on an odd-numbered floor below A.", models,
      lambda m: m["E"] == 5 and m["D"] == 4 and m["B"] == 3, lambda m: m["C"] % 2 == 1 and m["C"] < m["A"],
      lambda m: next(p for p in five if m[p] == 5), "A", "T",
      "'Only E lives above D' means D is on floor 4 and E on floor 5, so I answers the question. II leaves the top "
      "floor open.", ["I: only one person above D ⇒ D = 4, E = 5 (top): sufficient",
                      "II: C odd and below A ⇒ many placements: not sufficient", "I alone is sufficient"], seconds=45)
models = [{"n": n, "r": r, "s": s} for n in range(10, 61) for r in range(1, n + 1) for s in range(1, n + 1) if r != s]
ds2_q("Intermediate", "What is Ravi's rank from the bottom in his class?",
      "Ravi is 12th from the top in a class of 40 students.",
      "Sita is five ranks below Ravi and 24th from the bottom.", models,
      lambda d: d["r"] == 12 and d["n"] == 40, lambda d: d["s"] == d["r"] + 5 and d["n"] - d["s"] + 1 == 24,
      lambda d: d["n"] - d["r"] + 1, "E", "N",
      "I: 40 − 12 + 1 = 29th from the bottom. II: Sita is 24th from the bottom and five ranks below Ravi, so Ravi is "
      "24 + 5 = 29th from the bottom. Each statement alone is sufficient.",
      ["I: rank from bottom = 40 − 12 + 1 = 29: sufficient",
       "II: Ravi is five places above Sita ⇒ 24 + 5 = 29th from the bottom: sufficient",
       "Either statement alone is sufficient"], seconds=50)
week_models = [{"m": a, "t": b} for a in range(7) for b in range(7) if a != b]
ds2_q("Intermediate", "On which day of the week did Meera visit the bank?",
      "Meera did not visit on Monday, Wednesday, Saturday or Sunday.",
      "Meera visited two days after Tina, and Tina visited on a day after Monday but before Wednesday.", week_models,
      lambda d: d["m"] not in (0, 2, 5, 6), lambda d: d["m"] == d["t"] + 2 and 0 < d["t"] < 2,
      lambda d: d["m"], "B", "E",
      "I leaves Tuesday, Thursday and Friday. II: Tina visited on Tuesday, so Meera visited on Thursday.",
      ["I: Tuesday, Thursday or Friday: not sufficient", "II: Tina = Tuesday ⇒ Meera = Thursday: sufficient",
       "II alone is sufficient"], seconds=45)
models = [dict(zip(five, p)) for p in itertools.permutations(range(1, 6))]
ds2_q("Intermediate", "Five persons A, B, C, D and E sit in a row facing north. Who sits at the extreme right end?",
      "B sits immediately to the right of A, and C sits at the extreme left end.",
      "D is not an immediate neighbour of C, and E sits second from the left end.", models,
      lambda m: m["B"] == m["A"] + 1 and m["C"] == 1, lambda m: abs(m["D"] - m["C"]) != 1 and m["E"] == 2,
      lambda m: next(p for p in five if m[p] == 5), "N", "E",
      "Together: C = 1 and E = 2; A–B take two adjacent seats among 3, 4, 5 and D the remaining one. A–B at 3–4 puts D "
      "at 5; A–B at 4–5 puts D at 3. D at 3 is not next to C (seat 1), so both cases are allowed: the right end is D "
      "or B. Even together the statements are not sufficient.",
      ["I: C = 1, A–B adjacent: many placements", "II: E = 2, D not next to C: many placements",
       "I + II: (C, E, A, B, D) or (C, E, D, A, B): right end D or B", "Not sufficient even together"], seconds=70)
# ---- Advanced: three statements
DS3_HEAD = ("The question below is followed by three statements, I, II and III. Decide which of the statements "
            "are sufficient to answer the question.\n\n")
models = [dict(zip(five, p)) for p in itertools.permutations(range(1, 6))]  # stack places from the bottom
fns = [lambda m: m["C"] == m["A"] + 1, lambda m: m["B"] == 1 and m["D"] == 2, lambda m: abs(m["E"] - m["D"]) != 1]
got = ds3(models, fns, lambda m: next(p for p in five if m[p] == 5))
assert got == "ALL"
keys = ["I+II", "II+III", "ALL", "NONE"]
fixed(DSF, "Three-statement", "Advanced",
      DS3_HEAD + "Question: Five boxes A, B, C, D and E are placed one above another in a single stack. Which box is "
      "at the top?\n\nI. Box C is placed immediately above box A.\nII. Box B is at the bottom, and box D is placed "
      "immediately above B.\nIII. Box E is not placed adjacent to box D.", [DS3[k] for k in keys], DS3["ALL"],
      "Three-statement data sufficiency: test every pair before using all three",
      "I + II: B = 1, D = 2, and the A–C pair with E fill places 3–5 in two ways (top C or top E). II + III: E is at 4 "
      "or 5, but A and C are free. I + III: many placements. With all three, E must be at 5 (at 4 the A–C pair cannot "
      "fit), so E is at the top.",
      ["I + II: (A3, C4, E5) or (E3, A4, C5): not sufficient", "II + III: B1, D2, E at 4 or 5; A, C free: not "
       "sufficient", "I + III: B, D free: not sufficient",
       "All three: B1, D2, E ∈ {4, 5}; E = 4 splits places 3 and 5, breaking the A–C pair ⇒ E = 5 (top)",
       "All three statements are necessary"], seconds=80, verified_by=ENUM)

# ================================================================================================ VERBAL REASONING
# Hand-written items. Each was solved by the author, then re-answered without looking at the key, checking every
# option against the standard rules: a conclusion must follow from the statement alone (no outside facts, no
# predictions, no generalising from a sample); cause-effect needs a direct link, a shared trigger, or none; a course of
# action must be practical and aimed at the stated problem; a strengthener/weakener must bear on the stated causal link.
SCN = "Statement and Conclusions"
SC_HEAD = ("Read the statement and the two conclusions. Assume everything in the statement to be true, and decide "
           "which conclusion(s) logically follow from it.\n\n")


def scq(diff, sub, statement, c1, c2, answer, explanation, steps, why, seconds=45):
    return fixed(SCN, sub, diff, SC_HEAD + f"Statement: {statement}\n\nConclusions:\nI. {c1}\nII. {c2}", OPT4, answer,
                 "A conclusion must follow from the statement alone", explanation, steps, why_others_wrong=why,
                 seconds=seconds, verified_by=HAND)


VC, INF = "Valid conclusions", "Inferences"
# ---- Basic
scq("Basic", VC, "All employees of the branch must complete the cyber-security training by Friday. Ravi is an "
    "employee of the branch.", "Ravi must complete the cyber-security training by Friday.",
    "Ravi has not yet completed the cyber-security training.", ONLY_I,
    "The rule covers every employee of the branch and Ravi is one, so I follows. Nothing says whether Ravi has "
    "already finished the training, so II does not follow.",
    ["Rule: every employee of the branch → training by Friday", "Ravi is an employee ⇒ I follows",
     "Whether he has already done it is not stated ⇒ II does not follow"],
    "Both and Only II assume a fact (Ravi has not finished) that the statement never gives; Neither ignores the "
    "direct application of the rule.", seconds=30)
scq("Basic", VC, "A train leaves Pune at 6:00 am and reaches Mumbai at 9:30 am the same day. It makes no stop on the "
    "way.", "The train takes three and a half hours to travel from Pune to Mumbai.",
    "The train does not stop at any station between Pune and Mumbai.", BOTH,
    "6:00 am to 9:30 am is three and a half hours, so I follows. 'It makes no stop on the way' says exactly what II "
    "says, so II follows too.",
    ["9:30 − 6:00 = 3 h 30 min ⇒ I follows", "'No stop on the way' ⇒ II follows"],
    "Only I or Only II leaves out one of two direct restatements; Neither ignores both.", seconds=30)
scq("Basic", VC, "Some members of the city cricket club also play chess.",
    "All chess players in the city are members of the cricket club.",
    "No member of the cricket club plays tennis.", NEITHER,
    "The statement only says that the cricket club and chess players overlap. It says nothing about all chess "
    "players (I fails) and nothing about tennis (II fails).",
    ["'Some members play chess' gives an overlap only", "I turns 'some' into 'all' the other way: does not follow",
     "II brings in tennis, which is never mentioned: does not follow"],
    "Only I reverses and widens the 'some' statement; Only II and Both rely on information not in the statement.",
    seconds=30)
scq("Basic", VC, "Only candidates who hold a graduation degree can apply for the post of Probationary Officer. Suresh "
    "has applied for the post.", "Suresh will be selected as a Probationary Officer.",
    "Suresh holds a graduation degree.", ONLY_II,
    "Applying is open only to graduates, and Suresh has applied, so he holds a degree (II). Applying does not mean "
    "being selected (I fails).",
    ["Rule: can apply ⇒ graduate", "Suresh applied ⇒ he is a graduate: II follows",
     "Selection depends on the recruitment process, not on applying: I does not follow"],
    "Only I and Both confuse applying with being selected; Neither ignores the eligibility rule.", seconds=35)
scq("Basic", INF, "The number of visitors to the city museum rose from 12,000 in January to 18,000 in February.",
    "The museum had more visitors in February than in January.",
    "The museum reduced its ticket price in February.", ONLY_I,
    "18,000 is more than 12,000, so I follows. The statement gives no reason for the rise; a price cut is only one "
    "possible explanation (II fails).",
    ["18,000 > 12,000 ⇒ I follows", "No cause is given; II guesses one ⇒ does not follow"],
    "Both and Only II supply a cause that the statement does not mention.", seconds=30)
# ---- Advanced
scq("Advanced", VC, "In a company, every manager has at least five years of work experience. Some employees with at "
    "least five years of work experience work in the sales department. Anil is a manager in the company.",
    "Anil has at least five years of work experience.", "Anil works in the sales department.", ONLY_I,
    "Anil is a manager, and every manager has at least five years of experience, so I follows. Only some experienced "
    "employees are in sales, and nothing places Anil among them, so II does not follow.",
    ["Every manager ⇒ ≥ 5 years; Anil is a manager ⇒ I follows",
     "Some ≥ 5-year employees are in sales: Anil may or may not be one ⇒ II does not follow"],
    "Both treats 'some experienced employees are in sales' as if it covered Anil.", seconds=50)
scq("Advanced", INF, "Over the past year, the total number of bank accounts in a district rose by 40%, while the "
    "district's adult population stayed the same.",
    "The number of bank accounts per adult in the district is higher now than a year ago.",
    "Every adult in the district now has a bank account.", ONLY_I,
    "More accounts for the same number of adults means more accounts per adult, so I follows. Some adults may hold "
    "several accounts while others hold none, so II does not follow.",
    ["Accounts ×1.4, adults unchanged ⇒ accounts per adult ×1.4: I follows",
     "Total accounts say nothing about how they are spread over adults: II does not follow"],
    "Both and Only II assume every adult is covered; a rise in totals can come from people opening second accounts.",
    seconds=55)
scq("Advanced", VC, "The state has made it mandatory for every new building with a built-up area above 500 square "
    "metres to install a rainwater-harvesting system. A newly built office building of 800 square metres in the state "
    "has no such system.", "The rule is not being enforced anywhere in the state.",
    "The new office building does not comply with the rule.", ONLY_II,
    "The building is new and above 500 square metres, so the rule applies; without the system it does not comply "
    "(II). One building's failure does not show that the rule is ignored everywhere (I fails).",
    ["Rule applies: new building, 800 > 500 square metres", "No system ⇒ non-compliance: II follows",
     "A single case cannot establish that enforcement fails everywhere: I does not follow"],
    "Only I and Both generalise from one building to the whole state.", seconds=55)
scq("Advanced", INF, "Tomato prices in the city doubled in July after heavy rain damaged the crop in the neighbouring "
    "districts.", "Tomato prices in the city will fall in August.",
    "Tomatoes sold in the city come only from the neighbouring districts.", NEITHER,
    "I is a prediction about August that the statement does not support. The rain-hit districts clearly supply "
    "some of the city's tomatoes, but 'only' goes beyond what is stated (II fails).",
    ["I: a forecast; nothing in the statement fixes August prices: does not follow",
     "II: the statement shows the neighbouring districts matter, not that they are the sole source: does not follow"],
    "Only II is the trap: the price jump suggests the districts are an important source, not the only one.",
    seconds=50)
scq("Advanced", VC, "All five members of the audit team are chartered accountants. Exactly two of the five also hold "
    "an MBA. Priya is a member of the audit team and does not hold an MBA.", "Priya is a chartered accountant.",
    "Three members of the audit team do not hold an MBA.", BOTH,
    "Every member is a chartered accountant, and Priya is a member, so I follows. Exactly two of five hold an MBA, so "
    "the other three do not, so II follows.",
    ["All members are CAs; Priya is a member ⇒ I follows", "5 − 2 = 3 members without an MBA ⇒ II follows"],
    "Only I misses the arithmetic in 'exactly two of the five'; Only II misses the direct application to Priya.",
    seconds=50)

# ================================================================================================ CAUSE AND EFFECT
CAE = "Cause and Effect"
CE = {"A": "Statement I is the cause and statement II is its effect",
      "B": "Statement II is the cause and statement I is its effect",
      "C": "Both the statements I and II are independent causes",
      "D": "Both the statements I and II are effects of independent causes",
      "E": "Both the statements I and II are effects of some common cause"}
CE_HEAD = ("Below are two statements, I and II. They may be independent causes, effects of independent causes or of "
           "a common cause, or one may be the effect of the other. Decide the relationship.\n\n")


def ceq(sub, s1, s2, answer, drop, explanation, steps, why, seconds=45):
    keys = [k for k in "ABCDE" if k != drop]
    assert answer in keys and len(keys) == 4
    return fixed(CAE, sub, "Intermediate", CE_HEAD + f"I. {s1}\nII. {s2}", [CE[k] for k in keys], CE[answer],
                 "Cause and effect: look for a direct link, a shared trigger, or none", explanation, steps,
                 why_others_wrong=why, seconds=seconds, verified_by=HAND)


ceq("Independent causes", "The state government announced a 50% cut in bus fares for students from 1 June.",
    "The number of students travelling by state buses rose sharply in June.", "A", "C",
    "Cheaper fares make the bus more attractive to students, and the rise came in the month the cut began. I "
    "explains II, so I is the cause and II its effect.",
    ["I (fare cut from 1 June) comes first", "Lower fares → more student passengers in June: I explains II",
     "So I is the cause, II the effect"],
    "II cannot cause I (the cut was announced before the rise); a common cause or independent causes would ignore "
    "the direct link.", seconds=40)
ceq("Independent causes", "Several flights at the city airport were cancelled on Tuesday morning.",
    "Dense fog reduced visibility at the city airport to under 50 metres on Tuesday morning.", "B", "C",
    "Very low visibility makes take-offs and landings unsafe, which leads airlines to cancel flights. II explains I, "
    "so II is the cause and I its effect.",
    ["II: fog, visibility under 50 m", "I: cancellations the same morning", "Fog → unsafe flying → cancellations: "
     "II is the cause"],
    "Cancelled flights cannot create fog, so A is impossible; E would need a third event behind both, but the fog "
    "itself explains the cancellations.", seconds=40)
ceq("Common cause", "All the hotels in the hill town reported full occupancy last weekend.",
    "Traffic jams stretched for several kilometres on the road to the hill town last weekend.", "E", "C",
    "Full hotels do not cause traffic on the approach road, and the jams do not fill hotels. Both are what a single "
    "event, a surge of tourists (for example over a long holiday weekend), would produce. So both are effects of a "
    "common cause.",
    ["No direct causal link either way", "Both are typical results of one trigger: a rush of visitors",
     "So both are effects of a common cause"],
    "Effects of independent causes would need two unrelated reasons that happened to coincide on the same weekend; "
    "one tourist rush explains both more simply.", seconds=50)
ceq("Independent causes", "The retail price of onions in the city has risen by 30% this month.",
    "The city's municipal corporation has raised property tax rates for the coming year.", "D", "C",
    "Each statement is an outcome: onion prices respond to supply and crop conditions, and the tax rise to the "
    "corporation's budget needs. Neither explains the other, and no single event explains both. They are effects of "
    "independent causes.",
    ["I is an effect of market supply conditions", "II is an effect of the corporation's revenue decisions",
     "No link and no shared trigger ⇒ effects of independent causes"],
    "A common cause would need one event driving both a vegetable price and a civic tax decision; nothing suggests "
    "one.", seconds=50)
ceq("Independent causes", "The school has decided to keep its playground open to local children on Sundays.",
    "Parents in the locality complained that their children had no safe place to play on weekends.", "B", "D",
    "The parents' complaint (II) is the problem; opening the playground on Sundays (I) is the school's response to "
    "it. II is the cause and I its effect.",
    ["II reports a need: no safe place to play on weekends", "I meets that need directly",
     "So II is the cause and I the effect"],
    "I cannot cause II (the decision would end the complaint, not create it); treating them as unrelated ignores the "
    "obvious response.", seconds=45)
ceq("Common cause", "Many residents of the coastal district were moved to relief camps on Thursday.",
    "All schools in the coastal district remained closed from Thursday to Saturday.", "E", "C",
    "Moving residents does not close schools, and closing schools does not move residents. Both are standard "
    "precautions taken together after one trigger, such as a cyclone warning for the coast. So both are effects of "
    "a common cause.",
    ["No direct link between evacuation and school closure", "Both match the response to one emergency warning",
     "So both are effects of a common cause"],
    "A is tempting (schools are sometimes used as relief camps), but even then the closure would follow from the "
    "same emergency, not from the evacuation itself.", seconds=50)

# ================================================================================================ CRITICAL REASONING
CRT = "Critical Reasoning"


def crq(diff, sub, text, correct, wrongs, concept, explanation, steps, why, seconds=60):
    return mcq(CRT, sub, diff, text, correct, wrongs, concept, explanation, steps, why_others_wrong=why,
               seconds=seconds, verified_by=HAND)


crq("Basic", "Course of action", "Statement: On the first working day of every month, when pensions are credited, "
    "many pensioners wait for over an hour at a bank branch.\n\nWhich of the following is the most appropriate course "
    "of action for the bank?",
    "Open extra counters and issue tokens to pensioners on the first few working days of every month",
    ["Stop crediting pensions on the first working day of the month",
     "Ask pensioners to visit the branch only once a year",
     "Keep the branch closed on the first working day of every month"],
    "A course of action should solve the stated problem practically",
    "The problem is a predictable rush on known days. Extra counters and tokens on those days cut the waiting time "
    "directly without harming anyone.",
    ["Problem: long waits on pension days", "Cause: many pensioners come on the same days",
     "Remedy: more service capacity on exactly those days"],
    "Delaying pensions or closing the branch hurts the pensioners; asking them to come once a year is impractical "
    "and does not reduce the queue on the busy days.", seconds=35)
crq("Intermediate", "Inference from a passage", "A survey of 500 customers of a bank found that 70% of the customers "
    "who use the bank's mobile app visited a branch at least once last month, while 90% of the customers who do not "
    "use the app visited a branch at least once last month.\n\nWhich of the following can be inferred from the "
    "survey?",
    "Among the surveyed customers, app users were less likely than non-users to have visited a branch last month",
    ["Using the mobile app makes customers stop visiting branches",
     "Most of the 500 surveyed customers use the mobile app",
     "The bank should close some of its branches"],
    "Inference: state only what the figures show",
    "70% of app users versus 90% of non-users visited a branch, so within the survey app users were less likely to "
    "visit. That is a direct reading of the figures.",
    ["App users: 70% visited; non-users: 90% visited", "70% < 90% ⇒ app users less likely to visit (within the survey)",
     "No causal claim, split of users or recommendation can be drawn"],
    "The survey shows an association, not that the app causes fewer visits (and 70% still visited); the split "
    "between users and non-users is never given; closing branches is a recommendation, not an inference.",
    seconds=60)
crq("Advanced", "Strengthen and weaken", "Argument: Six months after the city began charging cars a fee to enter the "
    "central business district during peak hours, the average speed of traffic in the district rose by 20%. So the "
    "entry fee has reduced congestion in the district.\n\nWhich of the following, if true, most seriously weakens the "
    "argument?",
    "During the same six months, a new ring road opened that lets vehicles crossing the city bypass the central "
    "business district altogether",
    ["The number of metro passengers travelling to the district rose during the six months",
     "Many drivers complained that the entry fee is too high",
     "The fee applies only during peak hours on working days"],
    "Weakening a causal claim: offer another cause for the same effect",
    "The argument credits the fee for faster traffic. If a new ring road took through-traffic out of the district in "
    "the same period, the faster speeds may be due to the road, not the fee, so the conclusion is undermined.",
    ["Conclusion: fee → faster traffic", "A weakener supplies an alternative explanation for the same result",
     "A new bypass road in the same period is such an explanation"],
    "More metro passengers fits the argument (drivers switching to the metro); complaints about the price do not "
    "touch the effect on traffic; the peak-hour limit only describes the fee.", seconds=75)

# ================================================================================================ WRITE
plan = json.loads((ROOT / "batches" / "plans" / "BATCH_002_plan.json").read_text(encoding="utf-8"))
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
for st_ in STIMULI:
    n_ = sum(1 for x in QUESTIONS if x.get("stimulus_id") == st_["stimulus_id"])
    assert 3 <= n_ <= 5, (st_["stimulus_id"], n_)
    assert len({x["difficulty"] for x in QUESTIONS if x.get("stimulus_id") == st_["stimulus_id"]}) == 1
assert STIMULI[0]["stimulus_id"] == splan["stimulus_id_start"]
print(f"{len(QUESTIONS)} questions, {len(STIMULI)} stimuli, keys {dict(sorted(KEYCOUNT.items()))}")
if CHECK_QUOTA:
    assert len(QUESTIONS) == splan["total"] == 200
    assert QUESTIONS[0]["question_id"] == splan["question_ids"][0]
    assert QUESTIONS[-1]["question_id"] == splan["question_ids"][1]
    doc = {
        "schema_version": "1.0",
        "batch_id": "BATCH_002",
        "created_at": TODAY,
        "notes": ("Reasoning Ability part of BATCH_002: 200 original questions (60 Basic, 80 Intermediate, 60 "
                  "Advanced) built by tools/batch_002/reasoning.py. New puzzle structures (vacant seats, unknown row "
                  "length, two rows facing the same way, concentric circles, rectangular table, flats with vacancies, "
                  "two stacks, unknown stack size, box weights, numeric ages on floors, calendar dates, joining "
                  "years). Puzzles are brute-forced for a unique arrangement; syllogisms are checked over every "
                  "Venn-region model; inequalities over all integer assignments; data sufficiency by enumerating "
                  "models for each statement subset; blood relations, directions, coding, series, alphabet, ranking "
                  "and input-output are recomputed in code. Verbal-reasoning items are hand-written and re-checked. "
                  "All questions await human review."),
        "stimuli": STIMULI,
        "questions": QUESTIONS,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {OUT}")
