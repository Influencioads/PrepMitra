"""Builds the Reasoning Ability topic package 4 (batches/plans/packages/REAS_pkg4.json): Ranking and Order, Input and
Output, Data Sufficiency, Statement and Assumptions, Statement and Conclusions, Cause and Effect and Critical
Reasoning for BATCH_007 to BATCH_010. Writes one fragment per batch to batches/parts/frag/BATCH_<NNN>_REAS_pkg4.json.

Method (helpers copied from tools/batch_005/reasoning.py, whose module runs its whole build on import):
- ranking: positions recomputed in code; comparison puzzles brute-forced for a unique order;
- input-output: every machine is simulated step by step and every answer is read off the simulated steps;
- data sufficiency: each statement subset is checked by enumerating models (script:enumerate-models);
- verbal items (assumptions, conclusions, cause and effect, critical reasoning) are hand-written; they carry
  ai:independent-check only after a separate, fresh solver answered them blind (key-free dump) and matched the key.
If any assertion fails, nothing is written. --draft prints quota gaps instead of asserting them;
--dump-blind <path> writes the key-free dump for the blind solver.

    python tools/packages/REAS_pkg4.py        (run from docs/question-bank)
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
PKG = json.loads((ROOT / "batches" / "plans" / "packages" / "REAS_pkg4.json").read_text(encoding="utf-8"))
TODAY = "2026-11-05"
RA = "Reasoning Ability"
LETTERS = "ABCD"
RECOMP = ("script:recompute", "ai:author-solve")
BRUTE = ("script:brute-force-unique", "ai:author-solve")
ENUM = ("script:enumerate-models", "ai:author-solve")
HAND = ("ai:author-solve", "ai:independent-check")  # only after a blind match by a fresh solver
SELF = ("ai:author-solve", "ai:self-recheck")

B = {}  # batch -> {"Q": [...], "S": [...], "K": Counter()}
CUR = None
VERBAL_IDS = []


def batch(b):
    global CUR
    CUR = b
    B.setdefault(b, {"Q": [], "S": [], "K": Counter()})


def QS():
    return B[CUR]["Q"]


# ------------------------------------------------------------------------------------------------ generic helpers
def solve(variables, domains, constraints, distinct_groups=()):
    """Exhaustive backtracking search; returns every assignment that satisfies all constraints."""
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
    wrongs = list(wrongs)
    assert len(wrongs) == 3 and correct not in wrongs and len(set(wrongs)) == 3, (correct, wrongs)
    if natural:
        opts = sorted([correct] + wrongs, key=natural)
    else:
        n, kc = len(QS()), B[CUR]["K"]
        k = min(LETTERS, key=lambda L: (kc[L], (LETTERS.index(L) - n) % 4))
        opts = wrongs[:]
        opts.insert(LETTERS.index(k), correct)
    return opts, LETTERS[opts.index(correct)]


WORDS = ["None", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Eleven", "Twelve",
         "Thirteen", "Fourteen", "Fifteen"]
num_word = lambda n: WORDS[n]
by_num = lambda t: WORDS.index(t) if t in WORDS else float(t.split()[0])
ORDN = lambda k: f"{k}{'th' if 10 <= k % 100 <= 20 else {1: 'st', 2: 'nd', 3: 'rd'}.get(k % 10, 'th')}"
ord_key = lambda t: int(t[:-2])


def q(topic, subtopic, difficulty, text, options, answer, concept, explanation, steps, shortcut=None,
      why_others_wrong=None, seconds=60, stimulus=None, verified_by=SELF, tags=None):
    assert answer in LETTERS and len(options) == 4 and len(set(options)) == 4, (text, options)
    first = int(PKG["batches"][CUR]["question_ids"][0].split("_")[-1])
    out = {
        "question_id": f"BANK_REAS_{first + len(QS()):06d}",
        "exam_mappings": default_mappings(RA, difficulty),
        "subject": RA, "topic": topic, "subtopic": subtopic, "difficulty": difficulty,
        "question_type": "MCQ", "language": "en",
    }
    if stimulus:
        pos = sum(1 for x in QS() if x.get("stimulus_id") == stimulus) + 1
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
    QS().append(out)
    B[CUR]["K"][answer] += 1
    return out


def mcq(topic, subtopic, difficulty, text, correct, wrongs, concept, explanation, steps, natural=None, **kw):
    opts, key = place(correct, wrongs, natural)
    return q(topic, subtopic, difficulty, text, opts, key, concept, explanation, steps, **kw)


def fixed(topic, subtopic, difficulty, text, options, correct_text, concept, explanation, steps, **kw):
    assert correct_text in options
    return q(topic, subtopic, difficulty, text, options, LETTERS[options.index(correct_text)], concept, explanation,
             steps, **kw)


def stimulus(kind, title, content, solution):
    start = int(PKG["batches"][CUR]["stimulus_id_start"].split("_")[-1])
    sid = f"STIM_REAS_{start + len(B[CUR]['S']):06d}"
    B[CUR]["S"].append({"stimulus_id": sid, "type": kind, "title": title, "content": content, "solution": solution})
    return sid


def bullets(conds):
    return "\n".join(f"- {t}" for t, _, _ in conds)


def near(seq, i, k=3):
    """Wrong options: distinct elements near position i (0-based) other than seq[i]."""
    out = []
    for d in (1, -1, 2, -2, 3, -3, 4, -4, 5, -5):
        j = i + d
        if 0 <= j < len(seq) and seq[j] != seq[i] and seq[j] not in out:
            out.append(seq[j])
    return out[:k]


# ------------------------------------------------------------------------------------------------ data sufficiency
DSF = "Data Sufficiency"
TS, THS = "Two-statement", "Three-statement"
DS2 = {"A": "Statement I alone is sufficient, but statement II alone is not sufficient",
       "B": "Statement II alone is sufficient, but statement I alone is not sufficient",
       "E": "Either statement I alone or statement II alone is sufficient",
       "N": "Statements I and II together are not sufficient",
       "T": "Both statements I and II together are necessary"}
DS_HEAD = ("The question below is followed by two statements, I and II. Decide whether the data in the statements are "
           "sufficient to answer the question.\n\n")
DS3 = {"I+II": "Only statements I and II together are sufficient",
       "II+III": "Only statements II and III together are sufficient",
       "I+III": "Only statements I and III together are sufficient",
       "ALL": "All three statements I, II and III together are necessary",
       "NONE": "Even all three statements together are not sufficient",
       "ANY2": "Any two of the three statements together are sufficient"}
DS3_HEAD = ("The question below is followed by three statements, I, II and III. Decide which of the statements "
            "are sufficient to answer the question.\n\n")


def sufficient(models, stmt_fns, subset, answer):
    vals = {answer(m) for m in models if all(stmt_fns[i](m) for i in subset)}
    assert vals, subset
    return len(vals) == 1


def ds2(models, s1, s2, answer):
    a, b = sufficient(models, [s1, s2], [0], answer), sufficient(models, [s1, s2], [1], answer)
    t = sufficient(models, [s1, s2], [0, 1], answer)
    return "E" if a and b else "A" if a else "B" if b else "T" if t else "N"


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


def ds_q(diff, text, models, s1, s2, answer, expected, concept, expl, steps, seconds=50, why=None):
    got = ds2(models, s1, s2, answer)
    assert got == expected, (text[:70], got)
    keys = "ABET" if expected == "E" else "ABNT"
    return fixed(DSF, TS, diff, DS_HEAD + text, [DS2[k] for k in keys], DS2[expected], concept, expl, steps,
                 why_others_wrong=why, seconds=seconds, verified_by=ENUM)


def ds3_q(diff, text, models, fns, answer, expected, opt_keys, concept, expl, steps, seconds=75, why=None):
    got = ds3(models, fns, answer)
    assert got == expected and expected in opt_keys and len(opt_keys) == 4, (text[:70], got)
    return fixed(DSF, THS, diff, DS3_HEAD + text, [DS3[k] for k in opt_keys], DS3[expected], concept, expl, steps,
                 why_others_wrong=why, seconds=seconds, verified_by=ENUM)


# ------------------------------------------------------------------------------------------------ input-output
IOT = "Input and Output"
WR, NR, MM = "Word rearrangement", "Number rearrangement", "Mixed machine"
ROMAN = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X"]
line = lambda s: " ".join(map(str, s))
step_txt = lambda st: [f"Step {ROMAN[i]}: {line(s_)}" for i, s_ in enumerate(st)]
step_key = lambda t: ROMAN.index(t.split()[1])
steps_join = lambda st: " ".join(f"{t}." for t in step_txt(st))


def run_select(items, key, side="left", tf=None):
    """Each step takes the unarranged item with the smallest key, transforms it (tf), and places it next to the items
    already arranged at the left end (side='left') or the right end (side='right'). Without a transformation, a step
    that would not change the line ends the machine (the line is already final)."""
    cur, rest, done, steps = list(items), list(items), [], []
    while rest:
        nxt = min(rest, key=key)
        rest.remove(nxt)
        new_item = tf(nxt) if tf else nxt
        done = done + [new_item] if side == "left" else [new_item] + done
        new = done + rest if side == "left" else rest + done
        if new == cur:
            assert tf is None
            final = sorted(items, key=key) if side == "left" else sorted(items, key=key)[::-1]
            assert cur == final, ("a step changes nothing", cur)
            break
        cur = new
        steps.append(cur[:])
    return steps


# ------------------------------------------------------------------------------------------------ verbal helpers
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


SCN = "Statement and Conclusions"
VC, INF = "Valid conclusions", "Inferences"
OPT4 = ["Only conclusion I follows", "Only conclusion II follows", "Neither conclusion I nor II follows",
        "Both conclusions I and II follow"]
ONLY_I, ONLY_II, NEITHER, BOTH = OPT4
EITHER = "Either conclusion I or II follows"
SC_HEAD = ("Read the statement and the two conclusions. Assume everything in the statement to be true, and decide "
           "which conclusion(s) logically follow from it.\n\n")


def scq(diff, sub, statement, c1, c2, answer, explanation, steps, why, seconds=45):
    opts = [ONLY_I, ONLY_II, NEITHER, EITHER] if answer == EITHER else OPT4
    q_ = fixed(SCN, sub, diff, SC_HEAD + f"Statement: {statement}\n\nConclusions:\nI. {c1}\nII. {c2}", opts, answer,
               "A conclusion must follow from the statement alone", explanation, steps, why_others_wrong=why,
               seconds=seconds)
    VERBAL_IDS.append(q_["question_id"])


CAE = "Cause and Effect"
CE = {"A": "Statement I is the cause and statement II is its effect",
      "B": "Statement II is the cause and statement I is its effect",
      "D": "Both the statements I and II are effects of independent causes",
      "E": "Both the statements I and II are effects of some common cause"}
CE_HEAD = ("Below are two statements, I and II. They may be independent causes, effects of independent causes or of "
           "a common cause, or one may be the effect of the other. Decide the relationship.\n\n")
IND, COM = "Independent causes", "Common cause"


def ceq(diff, s1, s2, answer, explanation, steps, why, seconds=45):
    sub = COM if answer == "E" else IND
    q_ = fixed(CAE, sub, diff, CE_HEAD + f"I. {s1}\nII. {s2}", [CE[k] for k in "ABDE"], CE[answer],
               "Cause and effect: look for a direct link, a shared trigger, or none", explanation, steps,
               why_others_wrong=why, seconds=seconds)
    VERBAL_IDS.append(q_["question_id"])


CRT = "Critical Reasoning"
SW_, CA_, INFP = "Strengthen and weaken", "Course of action", "Inference from a passage"


def crq(diff, sub, text, correct, wrongs, concept, explanation, steps, why, seconds=60):
    q_ = mcq(CRT, sub, diff, text, correct, wrongs, concept, explanation, steps, why_others_wrong=why, seconds=seconds)
    VERBAL_IDS.append(q_["question_id"])


RNK = "Ranking and Order"
POSR, CHW = "Position in a row", "Comparison of heights/weights"


# ################################################################################################ BATCH_007
batch("007")
# ================================================================================================ RANKING (B5, A5)
# ---- Basic
n_, h_, i_ = 36, 25, 22
i_left = n_ - i_ + 1
ans = h_ - i_left - 1
assert (i_left, ans) == (15, 9)
mcq(RNK, POSR, "Basic", "In a row of 36 students facing north, Harsh is 25th from the left end and Ishaan is 22nd from "
    "the right end. Ishaan sits to the left of Harsh. How many students sit between Harsh and Ishaan?", str(ans),
    ["11", "10", "8"], "Convert both positions to the same end",
    f"Ishaan is 36 − 22 + 1 = {i_left}th from the left. Harsh is 25th from the left, so the students between them are "
    f"those in places 16 to 24: 25 − 15 − 1 = {ans}.",
    [f"Ishaan from the left = 36 − 22 + 1 = {i_left}", f"Between = 25 − 15 − 1 = {ans}"],
    why_others_wrong="11 is 25 + 22 − 36, the overlap that still counts Harsh and Ishaan; 10 forgets to subtract one; "
                     "8 subtracts one too many.", natural=int, seconds=40, verified_by=RECOMP)

P5 = ["P", "Q", "R", "S", "T"]
conds = [("Parcel Q is heavier than parcel R but lighter than parcel T.", ("Q", "R", "T"), lambda q_, r, t: r < q_ < t),
         ("Parcel P is lighter than parcel R.", ("P", "R"), lambda p, r: p < r),
         ("Parcel S is heavier than parcel T.", ("S", "T"), lambda s, t: t < s)]
W5 = unique(P5, {p: range(1, 6) for p in P5}, conds, [P5])  # 1 = lightest
ans = next(p for p in P5 if W5[p] == 2)
assert ans == "R"
mcq(RNK, CHW, "Basic", "Five parcels P, Q, R, S and T have different weights.\n" + bullets(conds) +
    "\n\nWhich parcel is the second lightest?", ans, ["Q", "P", "T"], "Join the comparisons into one chain",
    "T > Q > R and R > P give T > Q > R > P; S is heavier than T. Order from the heaviest: S, T, Q, R, P. The second "
    "lightest is R.", ["T > Q > R > P", "S > T", "Order: S, T, Q, R, P"],
    why_others_wrong="P is the lightest; Q is third from the lightest; T is the second heaviest.", seconds=40,
    verified_by=BRUTE)

L_ = 0
M = {"Lata": L_, "Komal": L_ + 8}
M["Mira"] = M["Komal"] - 5
M["Nalini"] = M["Mira"] + 2
order = sorted(M, key=M.get, reverse=True)
assert order == ["Komal", "Nalini", "Mira", "Lata"]
mcq(RNK, CHW, "Basic", "In a test, Komal scored 8 marks more than Lata. Mira scored 5 marks less than Komal, and "
    "Nalini scored 2 marks more than Mira. Who scored the second highest marks among the four?", "Nalini",
    ["Mira", "Komal", "Lata"], "Express every score in terms of one person's score",
    "Take Lata's score as L. Komal = L + 8, Mira = L + 3, Nalini = L + 5. Order: Komal, Nalini, Mira, Lata. The second "
    "highest is Nalini.", ["Komal = L + 8", "Mira = L + 3", "Nalini = L + 5", "Order: Komal > Nalini > Mira > Lata"],
    why_others_wrong="Komal is the highest, Mira third and Lata the lowest.", seconds=45, verified_by=RECOMP)

mid = (29 + 1) // 2
lina = mid - 6
ans = 29 - lina + 1
assert (mid, lina, ans) == (15, 9, 21)
mcq(RNK, POSR, "Basic", "Twenty-nine children sit in a row facing north. Kabir sits exactly in the middle of the row. "
    "Lina sits sixth to the left of Kabir. What is Lina's position from the right end of the row?", ORDN(ans),
    ["9th", "20th", "22nd"], "Middle of an odd row = (n + 1) ÷ 2",
    f"Kabir is (29 + 1) ÷ 2 = 15th from the left. Lina is six places to his left: 15 − 6 = 9th from the left, so she "
    f"is 29 − 9 + 1 = {ans}st from the right.",
    ["Kabir = 15th from the left", "Lina = 9th from the left", f"From the right: 29 − 9 + 1 = {ans}"],
    why_others_wrong="9th is her place from the left; 20th and 22nd come from dropping or doubling the + 1.",
    natural=ord_key, seconds=40, verified_by=RECOMP)

R6 = ["U", "V", "W", "X", "Y", "Z"]
conds = [("Rope U is longer than rope V but shorter than rope W.", ("U", "V", "W"), lambda u, v, w: v < u < w),
         ("Rope X is shorter than rope V.", ("X", "V"), lambda x, v: x < v),
         ("Rope Y is the longest.", tuple(R6), lambda *v: v[4] == 6),
         ("Rope Z is longer than rope W.", ("Z", "W"), lambda z, w: w < z)]
L6 = unique(R6, {p: range(1, 7) for p in R6}, conds, [R6])
ans = sum(1 for p in R6 if L6[p] < L6["U"])
assert ans == 2
mcq(RNK, CHW, "Basic", "Six ropes U, V, W, X, Y and Z have different lengths.\n" + bullets(conds) +
    "\n\nHow many ropes are shorter than rope U?", num_word(ans), ["One", "Three", "Four"],
    "Build the chain from the longest", "Y is the longest and Z > W > U > V > X, so the order is Y, Z, W, U, V, X. "
    "Two ropes (V and X) are shorter than U.", ["W > U > V > X", "Z > W; Y longest", "Order: Y, Z, W, U, V, X"],
    why_others_wrong="One counts only V; Three and Four count ropes longer than U or include U itself.",
    natural=by_num, seconds=40, verified_by=BRUTE)

# ---- Advanced: weight set (stimulus)
P7 = ["Abha", "Bimal", "Charu", "Dhruv", "Ekta", "Farhan", "Gopi"]
conds = [("Only two persons are heavier than Abha.", tuple(P7), lambda *v: sum(1 for x in v if x > v[0]) == 2),
         ("Dhruv is heavier than Farhan but lighter than Charu.", ("Dhruv", "Farhan", "Charu"),
          lambda d, f, c: f < d < c),
         ("Exactly two persons have weights between those of Charu and Ekta.", ("Charu", "Ekta"),
          lambda c, e: abs(c - e) == 3),
         ("Charu is heavier than Ekta.", ("Charu", "Ekta"), lambda c, e: e < c),
         ("Gopi is lighter than Farhan.", ("Gopi", "Farhan"), lambda g, f: g < f),
         ("Bimal is heavier than Dhruv, but Bimal is not the heaviest.", ("Bimal", "Dhruv"),
          lambda b, d: d < b < 7)]
W7 = unique(P7, {p: range(1, 8) for p in P7}, conds, [P7])  # 1 = lightest
ORD7 = sorted(P7, key=W7.get, reverse=True)
assert ORD7 == ["Charu", "Bimal", "Abha", "Ekta", "Dhruv", "Farhan", "Gopi"]
sid = stimulus("puzzle", "Seven persons and their weights",
               "Seven persons Abha, Bimal, Charu, Dhruv, Ekta, Farhan and Gopi have different weights.\n\n"
               + bullets(conds),
               "Abha is the 3rd heaviest. Gopi < Farhan < Dhruv < Charu, so Charu is at least 4th from the bottom, and "
               "Ekta is exactly three places below Charu. If Charu were 4th from the bottom, Ekta would be the lightest, "
               "but Gopi, Farhan and Dhruv must fill the three places below Charu. If Charu were 2nd heaviest, Ekta "
               "would be 5th heaviest, Dhruv 4th heaviest, and Bimal (heavier than Dhruv, not the heaviest) would have "
               "no place. So Charu is the heaviest, Ekta 4th, Bimal 2nd, and Dhruv, Farhan, Gopi follow. Heaviest to "
               "lightest: "
               + ", ".join(ORD7) + ".")
RQ = lambda text, correct, wrongs, concept, expl, steps, **kw: mcq(RNK, CHW, "Advanced", text, correct, wrongs, concept,
                                                                    expl, steps, stimulus=sid, verified_by=BRUTE, **kw)
RQ("Who is the second heaviest?", ORD7[1], ["Abha", "Charu", "Ekta"], "Fix the extremes first",
   "Order from the heaviest: " + ", ".join(ORD7) + ". The second heaviest is Bimal.", ["Order: " + " > ".join(ORD7)],
   why_others_wrong="Charu is the heaviest, Abha third and Ekta fourth.", seconds=100)
ans = sum(1 for p in P7 if W7[p] < W7["Ekta"])
assert ans == 3
RQ("How many persons are lighter than Ekta?", num_word(ans), ["Two", "Four", "One"], "Count below a fixed place",
   "Ekta is 4th from the top of seven, so Dhruv, Farhan and Gopi (three persons) are lighter than her.",
   ["Ekta = 4th heaviest", "Below her: Dhruv, Farhan, Gopi"], natural=by_num,
   why_others_wrong="Two leaves out Gopi; Four counts Ekta herself; One counts only Gopi's neighbour.", seconds=60)
ans = 51 + 4 * (W7["Bimal"] - W7["Farhan"])
assert ans == 67
RQ("The weights are whole numbers of kilograms, and each person is exactly 4 kg heavier than the next lighter person. "
   "If Farhan weighs 51 kg, how much does Bimal weigh?", f"{ans} kg", ["63 kg", "71 kg", "59 kg"],
   "Equal gaps: weight difference = number of places × gap",
   f"Farhan is 6th and Bimal 2nd from the top, four places apart, so Bimal weighs 51 + 4 × 4 = {ans} kg.",
   ["Farhan: 6th heaviest; Bimal: 2nd heaviest", "Gap: 4 places × 4 kg = 16 kg", f"Bimal = 51 + 16 = {ans} kg"],
   natural=lambda t: int(t.split()[0]), why_others_wrong="63 kg counts three gaps, 71 kg five, and 59 kg two.",
   seconds=90)

# ---- Advanced standalone: could-be total
cand = set()
for N in range(8, 60):
    o_, p_ = 7, N - 6
    if p_ != o_ and abs(o_ - p_) - 1 == 4:
        cand.add(N)
assert cand == {8, 18}
mcq(RNK, POSR, "Advanced", "Some persons sit in a row facing north. Ojas is 7th from the left end and Pia is 7th from "
    "the right end. Exactly four persons sit between Ojas and Pia. Which of the following could be the number of "
    "persons in the row?", "8", ["16", "17", "19"], "Two cases: the two persons may or may not cross",
    "If Pia is to the right of Ojas, the row has 7 + 4 + 7 = 18 persons. If Pia is to the left of Ojas, Pia is 2nd and "
    "Ojas 7th from the left with four persons between them, so the row has 8 persons. Only 8 is among the options.",
    ["No crossing: 7 + 4 + 7 = 18", "Crossing: N − 6 = 2 ⇒ N = 8", "Possible totals: 8 or 18"],
    why_others_wrong="16, 17 and 19 do not leave exactly four persons between them in either arrangement.",
    natural=int, seconds=80, verified_by=RECOMP)

# ---- Advanced standalone: minimum persons
sols = []
for N in range(10, 60):
    ravi, sunil, tara = 6, 10, N - 9
    if tara >= 1 and abs(tara - sunil) - 1 == 3 and tara not in (ravi, sunil):
        sols.append(N)
assert min(sols) == 23 and sols == [23]
mcq(RNK, POSR, "Advanced", "Some persons sit in a row facing north. Ravi is 6th from the left end, and Sunil sits "
    "fourth to the right of Ravi. Tara is 10th from the right end, and exactly three persons sit between Sunil and "
    "Tara. What is the minimum possible number of persons in the row?", "23", ["15", "22", "24"],
    "Check each case against the seats already taken",
    "Sunil is 10th from the left. Tara is either 14th or 6th from the left. The 6th seat is Ravi's, so Tara is 14th "
    "from the left and 10th from the right: 14 + 10 − 1 = 23 persons. This is the only possible number, so it is also "
    "the minimum.", ["Sunil = 6 + 4 = 10th from the left", "Tara = 14th or 6th; 6th is Ravi's ⇒ 14th",
                     "Total = 14 + 10 − 1 = 23"],
    why_others_wrong="15 puts Tara in Ravi's seat; 22 and 24 come from dropping or doubling the − 1.", natural=int,
    seconds=90, verified_by=RECOMP)

# ================================================================================================ INPUT-OUTPUT (B2, I7, A3)
# ---- Basic standalone: smallest units digit to the left
INP = [46, 81, 93, 70, 25, 58]
st = run_select(INP, key=lambda n: (n % 10, n), side="left")
assert len(st) == 4 and st[2] == [70, 81, 93, 46, 25, 58]
mcq(IOT, NR, "Basic",
    "A number arrangement machine rearranges a line of numbers step by step. In each step it takes, among the numbers "
    "not yet arranged, the one with the smallest units digit and places it immediately to the right of the numbers "
    "already arranged at the left end (in Step I, at the extreme left). The other numbers keep their order. A step "
    "that would not change the line is not counted.\n\nInput: " + line(INP) + "\n\nWhich of the following is Step III?",
    line(st[2]), [line(st[1]), line(st[3]), line(sorted(INP))], "Order by the units digit, not by the number",
    "Units digits: 46 → 6, 81 → 1, 93 → 3, 70 → 0, 25 → 5, 58 → 8, so the order is 70, 81, 93, 25, 46, 58. "
    + steps_join(st[:3]), step_txt(st[:3]),
    why_others_wrong="The first two wrong lines are Steps II and IV; the last orders the numbers by their value.",
    seconds=50, verified_by=RECOMP)

# ---- Basic standalone: symmetric interchange machine
INP = "lotus maple cedar birch aspen olive tulip neem".split()
st, cur = [], INP[:]
for k in range(4):
    cur = cur[:]
    cur[k], cur[7 - k] = cur[7 - k], cur[k]
    st.append(cur)
assert st[-1] == INP[::-1]
ans = st[1][6]
assert ans == "maple"
mcq(IOT, WR, "Basic",
    "A word machine rearranges a line of eight words step by step. In Step I it interchanges the 1st and the 8th words "
    "(counted from the left), in Step II the 2nd and the 7th words, in Step III the 3rd and the 6th words, and in Step "
    "IV the 4th and the 5th words. Then it stops.\n\nInput: " + line(INP) +
    "\n\nWhich word is 7th from the left end in Step II?", ans, ["tulip", "olive", "lotus"],
    "Each step changes only two places", steps_join(st[:2]) + " The 7th word from the left is maple.", step_txt(st[:2]),
    why_others_wrong="tulip is 7th in the input and in Step I; olive is 6th; lotus is 8th after Step I.", seconds=45,
    verified_by=RECOMP)

# ---- Intermediate set A (4): most consonants to the right end
INP = "glints planet aroma stream oasis branch idea".split()
cons = lambda w: sum(1 for c in w if c not in "aeiou")
assert all("y" not in w for w in INP)
st = run_select(INP, key=lambda w: (-cons(w), w), side="right")
assert len(st) == 6 and st[-1] == ["idea", "oasis", "aroma", "stream", "planet", "glints", "branch"]
sid = stimulus("passage", "Machine: most consonants to the right end",
               "A word arrangement machine rearranges a line of words step by step. In each step it takes, among the "
               "words not yet arranged, the word with the most consonants (letters other than a, e, i, o and u); if "
               "two such words have the same number of consonants, it takes the one that comes first in alphabetical "
               "order. It places that word at the right end, immediately to the left of the words already arranged "
               "there (in Step I, at the extreme right). The other words keep their order. The machine stops when the "
               "arrangement is complete.\n\nInput: " + line(INP),
               "Consonants: planet 4, stream 4, oasis 2, branch 5, idea 1, glints 5, aroma 2. Order of selection: "
               "branch, glints, planet, stream, aroma, oasis, idea.\n\n" + "\n".join(step_txt(st)))
IQ = lambda text, correct, wrongs, concept, expl, steps, **kw: mcq(
    IOT, WR, "Intermediate", text, correct, wrongs, concept, expl, steps, stimulus=sid, verified_by=RECOMP, **kw)
IQ("Which of the following is Step III?", line(st[2]), [line(st[1]), line(st[3]), line(st[2][::-1])],
   "Count consonants, break ties alphabetically", steps_join(st[:3]), step_txt(st[:3]),
   why_others_wrong="The first two wrong lines are Steps II and IV; the last is Step III written backwards.",
   seconds=75)
s4 = st[3]
ans = s4[s4.index("stream") - 2]
assert ans == "oasis" and s4[:5] == ["aroma", "oasis", "idea", "stream", "planet"]
IQ("In Step IV, which word is second to the left of 'stream'?", ans,
   ["aroma", "idea", "planet"], "Read the step, then count",
   f"Step IV: {line(s4)}. Two places to the left of 'stream' is '{ans}'.", [f"Step IV: {line(s4)}"], seconds=60)
assert next(i for i, s_ in enumerate(st) if s_[0] == "idea") == len(st) - 1
IQ("Counting only the steps that change the line, after how many steps does 'idea' end up at the extreme left with every word in its final place?", num_word(len(st)),
   [num_word(len(st) + 1), num_word(len(st) - 1), num_word(len(st) - 2)], "The last word needs no step of its own",
   steps_join(st) + " After Step VI only 'idea' is left, and it is already at the left end.", step_txt(st),
   natural=by_num, seconds=70)
first = next(i for i, s_ in enumerate(st) if s_.index("oasis") + 1 == s_.index("aroma"))
IQ("In which step does 'oasis' first stand immediately to the left of 'aroma'?", f"Step {ROMAN[first]}",
   [f"Step {ROMAN[i]}" for i in range(6) if i != first][:3], "Track two words through the steps",
   steps_join(st[:first + 1]), step_txt(st[:first + 1]), natural=step_key, seconds=70)

# ---- Intermediate set B (3): smallest reversed value to the left, written reversed
INP = [62, 38, 81, 47, 15, 93]
rev = lambda n: int(str(n)[::-1])
st = run_select(INP, key=rev, side="left", tf=rev)
assert len(st) == 6
assert not set(rev(n) for n in INP) & set(INP)
sid = stimulus("passage", "Machine: numbers read backwards",
               "A number arrangement machine rearranges a line of two-digit numbers step by step. In each step it takes, "
               "among the numbers not yet arranged, the one whose value is the smallest when its digits are read in "
               "reverse order, writes it with its digits reversed, and places it immediately to the right of the "
               "numbers already arranged at the left end (in Step I, at the extreme left). The other numbers keep "
               "their order. The machine stops when every number has been arranged.\n\nInput: " + line(INP),
               "Reversed values: 62 → 26, 38 → 83, 81 → 18, 47 → 74, 15 → 51, 93 → 39. Order of selection: 81, 62, "
               "93, 15, 47, 38.\n\n" + "\n".join(step_txt(st)))
IQ = lambda text, correct, wrongs, concept, expl, steps, **kw: mcq(
    IOT, NR, "Intermediate", text, correct, wrongs, concept, expl, steps, stimulus=sid, verified_by=RECOMP, **kw)
IQ("Which of the following is Step III?", line(st[2]),
   [line(st[1]), line(st[3]), line([81, 62, 93] + [x for x in INP if x not in (81, 62, 93)])],
   "Select by the reversed value, then write it reversed", steps_join(st[:3]), step_txt(st[:3]),
   why_others_wrong="The first two wrong lines are Steps II and IV; the last forgets to reverse the arranged numbers.",
   seconds=75)
s4 = st[3]
ans = s4[0] + s4[-1]
IQ("In Step IV, what is the sum of the numbers at the two ends of the line?", str(ans),
   [str(s4[0] + s4[-2]), str(81 + s4[-1]), str(s4[1] + s4[-1])], "Read the step, then add",
   f"Step IV: {line(s4)}. Ends: {s4[0]} and {s4[-1]}; sum = {ans}.", [f"Step IV: {line(s4)}"], natural=int,
   seconds=70)
fin = st[-1]
ans = fin[-3]
IQ("In the last step, which number is 3rd from the right end?", str(ans), [str(x) for x in near(fin, len(fin) - 3)],
   "The last step lists the reversed numbers in order of selection", f"Last step: {line(fin)}. The 3rd from the right "
   f"is {ans}.", [f"Last step: {line(fin)}"], seconds=60)

# ---- Advanced set (3): fewest vowels left (first two letters swapped); largest units digit right (+ units digit)
INP = ["garden", 37, "kite", 54, "brush", 89, "apron", 62, "stick", 45]
vow = lambda w: sum(1 for c in w if c in "aeiou")
sw2 = lambda w: w[1] + w[0] + w[2:]


def mixed007(items):
    ws, ns = [x for x in items if isinstance(x, str)], [x for x in items if isinstance(x, int)]
    left, right, steps, cur = [], [], [], list(items)
    while ws or ns:
        if ws:
            w = min(ws, key=lambda w_: (vow(w_), w_))
            ws.remove(w)
            left.append(sw2(w))
        if ns:
            n = max(ns, key=lambda n_: n_ % 10)
            ns.remove(n)
            right.insert(0, n + n % 10)
        mid = [x for x in items if x in ws or x in ns]
        new = left + mid + right
        assert new != cur
        cur = new
        steps.append(cur)
    return steps


assert len({n % 10 for n in INP if isinstance(n, int)}) == 5
st = mixed007(INP)
assert len(st) == 5
sid = stimulus("passage", "Machine: swapped letters and units-digit numbers",
               "A word and number arrangement machine rearranges a line step by step. In each step it makes two moves: "
               "(1) among the words not yet arranged, it takes the word with the fewest vowels (a, e, i, o, u; if two "
               "words have the same number of vowels, the one that comes first in alphabetical order), interchanges "
               "its first two letters, and places it at the left end, immediately to the right of the words already "
               "placed there; (2) among the numbers not yet arranged, it takes the one with the largest units digit, "
               "adds its units digit to it, and places the result at the right end, immediately to the left of the "
               "numbers already placed there. All other elements keep their order. The machine stops when every "
               "element has been arranged.\n\nInput: " + line(INP),
               "Words: brush (1 vowel), stick (1), then apron, garden, kite (2 each) → rbush, tsick, paron, agrden, "
               "ikte. Numbers by units digit: 89, 37, 45, 54, 62 → 98, 44, 50, 58, 64.\n\n" + "\n".join(step_txt(st)))
IQ = lambda text, correct, wrongs, concept, expl, steps, **kw: mcq(
    IOT, MM, "Advanced", text, correct, wrongs, concept, expl, steps, stimulus=sid, verified_by=RECOMP, **kw)
IQ("Which of the following is Step III?", line(st[2]),
   [line(st[1]), line(st[3]), line(["brush", "stick", "apron"] + st[2][3:])],
   "Two moves, each with a transformation", steps_join(st[:3]), step_txt(st[:3]),
   why_others_wrong="The first two wrong lines are Steps II and IV; the last forgets to interchange the letters.",
   seconds=110)
ans = sum(x for x in st[-1] if isinstance(x, int))
IQ("What is the sum of all the numbers in the last step?", str(ans),
   [str(sum(x for x in INP if isinstance(x, int))), str(ans - 9), str(ans + 10)],
   "Each number grows by its own units digit",
   f"Last step: {line(st[-1])}. Sum = 98 + 44 + 50 + 58 + 64 = {ans}.", [f"Last step: {line(st[-1])}"], natural=int,
   seconds=90)
s2 = st[1]
ans = s2[-4]
IQ("In Step II, which element is 4th from the right end?", str(ans), [str(x) for x in near(s2, len(s2) - 4)],
   "Read the step, then count", f"Step II: {line(s2)}. The 4th from the right is {ans}.", [f"Step II: {line(s2)}"],
   seconds=85)

# ================================================================================================ DATA SUFFICIENCY (B1, I2)
V4 = ["M", "N", "P", "K"]
models = [dict(zip(V4, p)) for p in itertools.product(range(1, 6), repeat=4)]
ds_q("Basic", "Question: Is M greater than K?\n\nI. M ≥ N > P.\nII. P ≥ K.", models,
     lambda m: m["M"] >= m["N"] > m["P"], lambda m: m["P"] >= m["K"], lambda m: m["M"] > m["K"], "T",
     "A yes/no question is answered when every allowed case gives the same answer",
     "I says nothing about K, and II says nothing about M. Together, M ≥ N > P ≥ K, so M > K: the answer is 'yes'.",
     ["I alone: K unknown ⇒ not sufficient", "II alone: M unknown ⇒ not sufficient", "Together: M ≥ N > P ≥ K ⇒ M > K"],
     seconds=40, why="The 'alone' options use one statement only; 'together not sufficient' ignores that the chain closes when both are combined.")
models = [{"dep": d, "dur": u} for d in range(8 * 60, 10 * 60) for u in range(10, 90)]
hm = lambda t: f"{t // 60}:{t % 60:02d} am"
ds_q("Intermediate", "Question: At what time did Neeraj reach his office?\n\nI. Neeraj left home at 8:40 am, and "
     "his journey to the office took 35 minutes.\nII. Neeraj reached his office 25 minutes before his 9:40 am meeting.",
     models, lambda m: m["dep"] == 8 * 60 + 40 and m["dur"] == 35, lambda m: m["dep"] + m["dur"] == 9 * 60 + 15,
     lambda m: m["dep"] + m["dur"], "E", "Each statement on its own",
     "I: 8:40 am + 35 minutes = 9:15 am. II: 9:40 am − 25 minutes = 9:15 am. Each statement alone gives the time.",
     ["I: 8:40 + 0:35 = 9:15 ⇒ sufficient", "II: 9:40 − 0:25 = 9:15 ⇒ sufficient"], seconds=45,
     why="Each 'alone' option ignores that the other statement also works; 'both together necessary' wrongly needs both.")
P8 = list("PQRSTUVW")
models = [dict(zip(P8, (0,) + p)) for p in itertools.permutations(range(1, 8))]  # right of a seat = +1
ds_q("Intermediate", "Question: Eight friends P, Q, R, S, T, U, V and W sit around a circular table, equally spaced "
     "and all facing the centre. Who sits second to the right of P?\n\nI. R sits immediately to the left of P, and T "
     "sits third to the right of R.\nII. U sits opposite P, and V is an immediate neighbour of U.", models,
     lambda m: m["R"] == 7 and m["T"] == (m["R"] + 3) % 8, lambda m: m["U"] == 4 and (m["V"] - 4) % 8 in (1, 7),
     lambda m: next(k for k in P8 if m[k] == 2), "A", "Count places from a fixed person",
     "I: R is one place to P's left, so three places to R's right is two places to P's right — T. Sufficient. II fixes "
     "U opposite P and V next to U, but the seat two places to P's right could still be Q, R, S, T or W — not "
     "sufficient.", ["I: R = P − 1, T = R + 3 = P + 2 ⇒ T", "II: seat P + 2 not fixed"], seconds=70,
     why="II alone leaves the seat open, and I alone already answers, so neither 'together' option is right.")

# ================================================================================================ ASSUMPTIONS (B4, I1, A5)
asm("Basic", "Notice at the entrance of a museum: \"Flash photography is not allowed inside the galleries.\"",
    "Flash photography can harm the exhibits or disturb other visitors in the galleries.",
    "Visitors to the museum do not carry cameras or mobile phones.", A_I,
    "A ban on flash photography is issued only because the museum sees some harm in it, to the exhibits or to other "
    "visitors (I). If visitors carried no cameras or phones, the notice would be pointless, so II is not assumed.",
    ["Ban on flash ⇒ flash is seen as harmful: I implicit", "Notice expects cameras to be carried ⇒ II not implicit"],
    "Only II and Both accept II, which goes against the purpose of the notice; Neither ignores the reason for a ban.",
    seconds=35)
asm("Basic", "A bakery has put up a board: \"Fresh bread available from 7 am every day.\"",
    "Some people want to buy fresh bread early in the morning.",
    "The bakery will be able to have fresh bread ready by 7 am every day.", A_B,
    "The bakery advertises early bread because it expects buyers at that hour (I), and it would not promise bread "
    "from 7 am every day unless it expects to have bread ready by then (II).",
    ["Advertising an early hour ⇒ demand expected: I", "Promise of bread by 7 am ⇒ able to bake in time: II"],
    "Each 'Only' option drops one of two things the promise rests on; Neither ignores both.", seconds=35)
asm("Basic", "A shop has put up a sign: \"Goods once sold will not be taken back.\"",
    "Every customer of the shop wants to return the goods he or she buys.",
    "The goods sold in the shop are of poor quality.", A_N,
    "The sign only states the shop's return policy. It does not take for granted that every customer wants to return "
    "goods ('every' is too strong), and it says nothing about the quality of the goods.",
    ["'Every customer' is an extreme claim ⇒ I not implicit", "Quality is not mentioned ⇒ II not implicit"],
    "Only I, Only II and Both accept a claim the sign does not need.", seconds=35)
asm("Basic", "Instruction printed on an admit card: \"Carry a valid photo identity card. Candidates without one will "
    "not be allowed into the examination hall.\"",
    "Every candidate already has a passport.",
    "Some candidates may come to the examination hall without a valid photo identity card.", A_II,
    "The warning is printed because the examining body expects that some candidates might forget or not have a valid "
    "identity card (II). Many kinds of photo identity card are valid; nothing suggests that every candidate has a "
    "passport (I).", ["Warning ⇒ some may come without an ID: II", "Passport for every candidate is not needed ⇒ I not "
                                                                   "implicit"],
    "Only I and Both accept the passport claim; Neither misses the reason for the warning.", seconds=35)
asm("Intermediate", "\"The bank will waive the processing fee on all home loans sanctioned during the festival "
    "month,\" said the bank's chairman.",
    "The waiver will attract more home-loan borrowers to the bank during the festival month.",
    "The bank charges no other fee on home loans.", A_I,
    "A fee waiver for a limited period is meant to draw more borrowers in that period, so I is implicit. Whether the "
    "bank charges other fees has nothing to do with the waiver, so II is not implicit.",
    ["Purpose of a limited-period waiver ⇒ more borrowers: I", "Other fees are irrelevant ⇒ II not implicit"],
    "Only II and Both accept an irrelevant claim; Neither ignores the purpose of the offer.", seconds=40)
asm("Advanced", "A university's notice: \"Apply for the merit scholarship before 15 July. Applications received "
    "after 15 July will not be considered.\"",
    "The university expects to receive applications for the merit scholarship.",
    "Every application received before 15 July will be accepted for the scholarship.", A_I,
    "A notice inviting applications is issued only if applications are expected (I). The notice says late "
    "applications will not be considered; it does not follow that every timely application will be accepted. Being "
    "considered is not the same as being granted the scholarship, so II is not implicit.",
    ["Inviting applications ⇒ applications expected: I", "'Not considered if late' does not mean 'accepted if on "
                                                          "time' ⇒ II not implicit"],
    "Only II and Both confuse 'considered' with 'accepted'; Neither ignores why the notice was issued.", seconds=55)
asm("Advanced", "\"To cut paper use, the office will print all internal documents on both sides of the sheet from "
    "Monday,\" said the office manager.",
    "The office's printers can print on both sides of a sheet, or can be made to do so.",
    "Printing on both sides of a sheet uses fewer sheets than printing on one side.", A_B,
    "The plan can work only if the printers can print on both sides (I), and it cuts paper use only if double-sided "
    "printing needs fewer sheets (II). Both are taken for granted.",
    ["Plan must be practicable ⇒ I", "Plan must serve its purpose ⇒ II"],
    "Each 'Only' option drops one of two things the plan rests on.", seconds=50)
asm("Advanced", "\"The city's new metro line will open to the public on 1 March,\" announced the metro corporation.",
    "Once the line opens, all the buses on the same route will run empty.",
    "The new line will carry more passengers than any other metro line in the city.", A_N,
    "The announcement only gives an opening date. It does not need buses to lose every passenger (I is extreme), or "
    "the new line to carry more passengers than every other line (II).",
    ["Opening date only ⇒ no claim about buses: I not implicit", "No comparison with other lines ⇒ II not implicit"],
    "Each of the other options accepts a sweeping prediction that the announcement does not depend on.", seconds=45)
asm("Advanced", "The government has made it compulsory for every new two-wheeler sold in the country to be fitted "
    "with an anti-lock braking system.",
    "Two-wheelers without an anti-lock braking system will stop being used on the roads at once.",
    "Anti-lock braking systems make two-wheelers safer to ride.", A_II,
    "A safety device is made compulsory only if it is believed to improve safety (II). The rule covers only new "
    "two-wheelers, so it does not assume that older two-wheelers without the system will vanish from the roads at "
    "once (I).", ["Compulsory fitting ⇒ the device is believed to help: II", "Rule is for new vehicles only ⇒ I not "
                                                                            "implicit"],
    "Only I and Both read the rule as applying to existing vehicles; Neither ignores why the device is required.",
    seconds=50)
asm("Advanced", "A hospital has started an SMS service that tells each patient in the outpatient queue when his or her "
    "turn is about 15 minutes away.",
    "Patients waiting in the outpatient queue have phones that can receive SMS messages.",
    "Some patients would rather spend part of their waiting time away from the queue area.", A_B,
    "An SMS alert is useful only if the patients can receive SMS messages (I). The point of telling a patient that the "
    "turn is 15 minutes away is to let him or her wait elsewhere and come back in time (II).",
    ["Service works only if SMS can be received ⇒ I", "Purpose: patients need not wait in the queue area ⇒ II"],
    "Each 'Only' option drops one of two things the service depends on.", seconds=55)

# ================================================================================================ CONCLUSIONS (I6)
scq("Intermediate", VC, "Every member of the city chess club has a national rating. No member of the city chess club "
    "is under 10 years of age. Arnav is 9 years old.", "Arnav is not a member of the city chess club.",
    "Arnav does not have a national rating.", ONLY_I,
    "No member is under 10, and Arnav is 9, so he is not a member (I). The statement says that every member has a "
    "rating, not that only members have ratings, so Arnav may or may not have one (II does not follow).",
    ["No member under 10; Arnav is 9 ⇒ not a member: I", "'Every member has a rating' does not mean 'only members do' "
                                                         "⇒ II does not follow"],
    "Only II and Both reverse 'every member has a rating'; Neither misses the direct age rule.", seconds=50)
scq("Intermediate", INF, "A cinema hall has 240 seats. For the 6 pm show, exactly 180 tickets were sold, one ticket "
    "for each seat, and no seat was sold twice.", "At least 60 seats were unsold for the 6 pm show.",
    "75% of the seats were sold for the 6 pm show.", BOTH,
    "Unsold seats = 240 − 180 = 60, so 'at least 60' is true (I). 180 ÷ 240 = 0.75 = 75% (II).",
    ["Unsold = 240 − 180 = 60 ⇒ I", "Sold share = 180 ÷ 240 = 75% ⇒ II"],
    "Each 'Only' option drops one of two direct calculations; Neither ignores both.", seconds=45)
scq("Intermediate", INF, "The price of a kilogram of rice at a shop rose from ₹50 to ₹60 this month.",
    "The price of rice at the shop rose by 20% this month.", "Rice was in short supply this month.", ONLY_I,
    "The rise is ₹10 on ₹50, that is 20% (I). The statement gives no reason for the rise; a shortage is one possible "
    "reason among many, so II does not follow.", ["(60 − 50) ÷ 50 = 20% ⇒ I", "Cause of the rise not stated ⇒ II does "
                                                                              "not follow"],
    "Only II and Both assume a cause; Neither ignores the direct calculation.", seconds=40)
scq("Intermediate", VC, "Some of the trains that leave the city's central station run at night. Every night train "
    "from the central station has sleeper coaches.",
    "Every train that leaves the central station has sleeper coaches.",
    "Some trains that leave the central station have sleeper coaches.", ONLY_II,
    "The night trains are some of the station's trains, and each of them has sleeper coaches, so some trains from the "
    "station have sleeper coaches (II). Nothing is said about the trains that do not run at night, so I does not "
    "follow.", ["Some trains are night trains; all night trains have sleepers ⇒ II", "Day trains not covered ⇒ I does "
                                                                                       "not follow"],
    "Only I and Both extend a fact about night trains to every train; Neither misses the 'some' conclusion.",
    seconds=45)
scq("Intermediate", INF, "The seats in an auditorium are numbered from 1 to 300. Rahul's seat number is a multiple of "
    "7 and is greater than 290.", "Rahul's seat number is 294.", "Rahul's seat number is an even number.", BOTH,
    "The multiples of 7 between 291 and 300 are only 294 (287 is too small and 301 is beyond 300). So Rahul's seat is "
    "294 (I), which is even (II).", ["Multiples of 7 in 291–300: only 294 ⇒ I", "294 is even ⇒ II"],
    "Each 'Only' option drops a conclusion that follows from the single possible seat number.", seconds=50)
scq("Intermediate", VC, "Ramesh's car is older than Suresh's car, and Suresh's car is older than Dinesh's car.",
    "Dinesh's car is the costliest of the three.", "Ramesh bought his car before Suresh bought his.", NEITHER,
    "The statement compares only the ages of the cars. Price is not mentioned (I does not follow), and an older car "
    "can be bought later, for example second-hand, so the order of purchase is not given (II does not follow).",
    ["Age of a car says nothing about its price ⇒ I does not follow", "Age of a car ≠ date of purchase ⇒ II does not "
                                                                      "follow"],
    "Each other option treats the cars' ages as if they gave their prices or purchase dates.", seconds=45)

# ================================================================================================ CRITICAL REASONING (B4, I3, A4)
crq("Basic", CA_, "Statement: Over the past month, several children in a residential colony have been bitten by stray "
    "dogs in the colony's park.\n\nWhich of the following is the most appropriate course of action?",
    "Ask the municipal body to catch the stray dogs, vaccinate them and move them to an animal shelter",
    ["Close the colony's park permanently", "Ask the children to carry sticks to the park",
     "Cut down all the trees in the park"], "A course of action should remove the stated problem safely",
    "The problem is stray dogs biting children. Getting the authorities to catch, vaccinate and shelter the dogs "
    "removes the danger and protects both children and animals.",
    ["Problem: stray dogs biting children", "Remedy: authorities catch, vaccinate and shelter the dogs"],
    "Closing the park punishes residents; sticks may provoke more attacks; cutting trees has nothing to do with dogs.",
    seconds=30)
t_c = 7 * 60 + 40
school = t_c + 3 * 6
assert school == 7 * 60 + 58
crq("Basic", INFP, "Passage: A school bus picks up students at five stops in the order A, B, C, D and E, and then "
    "goes to the school. It reaches stop C at 7:40 am. It takes exactly 6 minutes to go from any stop to the next, "
    "and also 6 minutes from stop E to the school. It does not wait at any stop.\n\nWhich of the following can be "
    "inferred from the passage?", "The bus reaches the school at 7:58 am",
    ["The bus leaves stop A at 7:30 am", "The bus carries the same number of students every day",
     "Classes at the school begin at 8:00 am"], "An inference must follow from the given facts alone",
    "From C (7:40 am) the bus needs three more 6-minute legs: C to D, D to E and E to the school, so it arrives at "
    "7:58 am.", ["C 7:40 → D 7:46 → E 7:52 → school 7:58"],
    "The bus leaves A at 7:28 am, not 7:30; the number of students and the school's starting time are not given.",
    seconds=45)
crq("Basic", SW_, "Claim: Installing a drinking-water cooler in the school playground will make students drink more "
    "water during the games period.\n\nWhich of the following, if true, most strengthens the claim?",
    "At present, students who want water during the games period must walk back to the main building, and most of "
    "them do not do so", ["The water cooler will cost the school ₹20,000",
                          "Students play football and cricket during the games period",
                          "Some students bring water bottles from home"],
    "Strengthen: show that the distance to water is what stops students from drinking",
    "If students drink little now because the water is far away, a cooler in the playground removes that obstacle, "
    "so they are likely to drink more.", ["Claim: cooler ⇒ more drinking", "Strengthener: distance is the obstacle now"],
    "The cost and the games played are irrelevant; students who bring bottles already have water, which, if "
    "anything, weakens the claim.", seconds=40)
crq("Basic", CA_, "Statement: There is no pedestrian crossing on the busy road outside a city hospital, and patients' "
    "relatives often run across the road between moving vehicles.\n\nWhich of the following is the most appropriate "
    "course of action?", "Mark a pedestrian crossing with a signal near the hospital gate and post a traffic warden "
                         "there at busy hours",
    ["Shift the hospital to another part of the city", "Stop patients' relatives from visiting the hospital",
     "Close the road to all vehicles permanently"], "Practical remedy for the stated danger",
    "The danger is pedestrians crossing a busy road with no safe crossing. A signalled crossing with a warden lets "
    "people cross safely without disrupting the hospital or the road.",
    ["Problem: no safe place to cross", "Remedy: signalled crossing + warden"],
    "Moving the hospital, banning visitors and closing the road are extreme and impractical.", seconds=30)
crq("Intermediate", SW_, "Argument: A company introduced flexible office hours in January. In January–March, employee "
    "absence was 15% lower than in October–December of the previous year. So the flexible hours reduced absence.\n\n"
    "Which of the following, if true, most seriously weakens the argument?",
    "In each of the past five years, absence at the company in January–March was about 15% lower than in the "
    "October–December quarter before it, because of the festival and flu season in October–December",
    ["Most employees said they liked the flexible office hours", "The company has about 400 employees",
     "A rival company introduced flexible office hours last year"],
    "Weaken: show that the fall would have happened anyway",
    "If absence always falls by about 15% from October–December to January–March, the fall this year is the usual "
    "seasonal pattern and does not show that flexible hours made a difference.",
    ["Evidence: 15% fall after the change", "Weakener: the same fall happens every year ⇒ no effect shown"],
    "Employees liking the hours does not show lower absence; the company's size and a rival's policy are irrelevant.",
    seconds=70)
crq("Intermediate", INFP, "Passage: Among the four branches of a bank in a town, the Station Road branch has more "
    "customers than the Market branch, and the Market branch has more customers than the Hospital Road branch. The "
    "Lake View branch has fewer customers than the Hospital Road branch.\n\nWhich of the following can be inferred "
    "from the passage?", "The Station Road branch has more customers than the Lake View branch",
    ["The Market branch has the most customers of the four", "The Lake View branch has the most deposits of the four",
     "The Hospital Road branch has fewer customers than the Lake View branch"],
    "Chain the comparisons", "Station Road > Market > Hospital Road > Lake View, so Station Road has more customers "
    "than Lake View.", ["Station Road > Market > Hospital Road", "Hospital Road > Lake View",
                        "⇒ Station Road > Lake View"],
    "Station Road, not Market, has the most customers; deposits are not mentioned; Lake View has fewer customers than "
    "Hospital Road, not more.", seconds=45)
crq("Intermediate", CA_, "Statement: Every year, tomato prices in a district crash in the same two months because "
    "the whole harvest reaches the market at once, and many farmers sell at a loss.\n\nWhich of the following is the "
    "most appropriate course of action?",
    "Help farmers' groups sign supply contracts, fixed before the season, with tomato-processing units that make "
    "puree and ketchup", ["Ban tomato farming in the district", "Ask farmers to destroy part of their harvest every "
                                                                "year", "Bring tomatoes from other states into the "
                                                                        "district's markets"],
    "Address the glut without harming farmers",
    "Prices crash because too many tomatoes reach the market at once. Contracts with processing units give farmers a "
    "fixed outlet and price for part of the crop, so less of it floods the market.",
    ["Problem: glut at harvest time", "Remedy: assured outlet through processing contracts"],
    "A ban is extreme; destroying crops wastes produce and income; importing tomatoes worsens the glut.", seconds=60)
crq("Advanced", SW_, "Argument: Residents of Ward 7 visit the city's government hospital less often than residents of "
    "any other ward. So the people of Ward 7 are the healthiest in the city.\n\nWhich of the following, if true, most "
    "seriously weakens the argument?",
    "Ward 7 is the farthest ward from the government hospital, and most of its residents are treated at a large "
    "private clinic inside the ward", ["Ward 7 has more parks than any other ward",
                                       "The government hospital has added 100 beds this year",
                                       "Residents of Ward 7 visit the hospital mainly for check-ups"],
    "Weaken: give another reason for fewer hospital visits",
    "If Ward 7's residents go to a nearby private clinic instead of the distant government hospital, they may fall ill "
    "as often as anyone else; the low number of hospital visits does not show better health.",
    ["Evidence: fewer visits to one hospital", "Weakener: they are treated elsewhere ⇒ visits do not measure health"],
    "More parks would, if anything, support the argument; hospital beds and the purpose of visits do not explain why "
    "Ward 7's visits are fewer.", seconds=75)
crq("Advanced", SW_, "Argument: The city plans to replace its diesel buses with electric buses, claiming that this "
    "will reduce the amount of fine dust in the city's air.\n\nWhich of the following, if true, most strengthens the "
    "claim?", "Studies of the city's air show that exhaust from diesel buses is a major source of the fine dust along "
              "the main bus routes", ["Electric buses cost more to buy than diesel buses",
                                      "Electric buses are quieter than diesel buses",
                                      "Many cities abroad have started using electric buses"],
    "Strengthen: link the thing removed to the problem",
    "Electric buses produce no exhaust. If diesel-bus exhaust is a major source of the fine dust, removing it should "
    "reduce the dust.", ["Claim: electric buses ⇒ less fine dust", "Strengthener: diesel exhaust is a major source"],
    "Cost and noise do not bear on dust; what other cities do says nothing about this city's air.", seconds=60)
crq("Advanced", INFP, "Passage: In a bank's recruitment drive, a candidate is shortlisted only if he or she clears "
    "both the written test and the group discussion. All 200 candidates took both. 120 cleared the written test and "
    "90 cleared the group discussion.\n\nWhich of the following must be true?",
    "At most 90 candidates were shortlisted", ["Exactly 90 candidates were shortlisted",
                                               "At least 100 candidates cleared neither stage",
                                               "Exactly 10 candidates cleared both stages"],
    "'Only if' gives a necessary condition, not a sufficient one",
    "A shortlisted candidate must have cleared both stages, and at most 90 candidates (those who cleared the group "
    "discussion) can have cleared both. So at most 90 were shortlisted. At least 120 + 90 − 200 = 10 cleared both, but "
    "clearing both does not guarantee shortlisting ('only if'), so even 'at least 10 shortlisted' is not certain.",
    ["Shortlisted ⊆ cleared both ⊆ cleared the group discussion (90) ⇒ at most 90",
     "Cleared both ≥ 10, but 'only if' ⇒ shortlisting not guaranteed"],
    "Exactly 90 treats clearing both stages as enough for shortlisting; at least 120 candidates cleared some stage, so "
    "at most 80 cleared neither; the number who cleared both is at least 10, not exactly 10.", seconds=90)
crq("Advanced", CA_, "Statement: An inspection found that many fire extinguishers in the city's shopping malls had "
    "passed their expiry dates, and the staff of several malls did not know how to use them.\n\nWhich of the "
    "following is the most appropriate course of action?",
    "Order the malls to replace expired extinguishers within a fixed time and train their staff, and check compliance "
    "through surprise inspections", ["Close all the shopping malls in the city",
                                     "Remove the fire extinguishers from the malls",
                                     "Ask shoppers to carry their own fire extinguishers"],
    "Fix both problems found and make sure the fix lasts",
    "The inspection found two problems — expired equipment and untrained staff. Replacing the equipment, training the "
    "staff and checking by surprise inspections addresses both and keeps the malls open.",
    ["Problems: expired extinguishers; untrained staff", "Remedy: replace, train, inspect"],
    "Closing every mall is extreme; removing extinguishers increases the danger; shoppers cannot be expected to carry "
    "extinguishers.", seconds=50)


# ################################################################################################ BATCH_008
batch("008")
# ================================================================================================ INPUT-OUTPUT (B5, I1, A6)
# ---- Basic set (5): odd numbers first (ascending), then even numbers (ascending), each to the left
INP = [42, 17, 68, 33, 91, 24, 55]
st = run_select(INP, key=lambda n: (n % 2 == 0, n), side="left")
assert len(st) == 5 and st[-1] == [17, 33, 55, 91, 24, 42, 68]
sid = stimulus("passage", "Machine: odd numbers first",
               "A number arrangement machine rearranges a line of numbers step by step. In each step it takes, among "
               "the numbers not yet arranged, the smallest odd number and places it immediately to the right of the "
               "numbers already arranged at the left end (in Step I, at the extreme left). When no odd number is left, "
               "it takes the smallest even number in the same way. The other numbers keep their order. A step that "
               "would not change the line is not counted, and the machine stops when the arrangement is complete."
               "\n\nInput: " + line(INP),
               "Order of selection: 17, 33, 55, 91 (odd), then 24, 42, 68 (even).\n\n" + "\n".join(step_txt(st)))
IQ = lambda text, correct, wrongs, concept, expl, steps, **kw: mcq(
    IOT, NR, "Basic", text, correct, wrongs, concept, expl, steps, stimulus=sid, verified_by=RECOMP, **kw)
IQ("Which of the following is Step II?", line(st[1]), [line(st[0]), line(st[2]), line(sorted(INP))],
   "Odd numbers are arranged before even numbers", steps_join(st[:2]), step_txt(st[:2]),
   why_others_wrong="The first two wrong lines are Steps I and III; the last puts all the numbers in plain ascending "
                    "order.", seconds=45)
IQ("The machine stops once the seven numbers stand in their final order. How many steps does it need for this input?", num_word(len(st)),
   [num_word(len(st) + 1), num_word(len(st) + 2), num_word(len(st) - 1)], "Stop when the line is final",
   steps_join(st) + " After Step V, 42 and 68 are already in their places, so no further step is needed.",
   step_txt(st), natural=by_num, seconds=50)
s3 = st[2]
ans = s3[-4]
IQ("In Step III, which number is 4th from the right end?", str(ans), [str(x) for x in near(s3, len(s3) - 4)],
   "Read the step, then count", f"Step III: {line(s3)}. The 4th from the right is {ans}.", [f"Step III: {line(s3)}"],
   seconds=40)
first = next(i for i, s_ in enumerate(st) if s_.index(91) == s_.index(55) + 1)
IQ("In which step does 91 first stand immediately to the right of 55?", f"Step {ROMAN[first]}",
   [f"Step {ROMAN[i]}" for i in range(5) if i != first][:3], "Track two numbers through the steps",
   steps_join(st[:first + 1]), step_txt(st[:first + 1]), natural=step_key, seconds=50)
pos = st[-1].index(24) + 1
IQ("In the last step, what is the position of 24 from the left end?", ORDN(pos),
   [ORDN(k) for k in (pos - 1, pos + 1, 3)], "The first even number follows all the odd numbers",
   f"Last step: {line(st[-1])}. There are four odd numbers, so 24 is {ORDN(pos)} from the left.",
   [f"Last step: {line(st[-1])}"], natural=ord_key, seconds=40)

# ---- Intermediate standalone: first letter latest in the alphabet; first letter replaced by the previous letter
INP = "tide hall rope moss vane cork".split()
prev1 = lambda w: chr(ord(w[0]) - 1) + w[1:]
st = run_select(INP, key=lambda w: -ord(w[0]), side="left", tf=prev1)
assert [w for w in st[-1]] == ["uane", "side", "qope", "loss", "gall", "bork"]
mcq(IOT, WR, "Intermediate",
    "A word machine rearranges a line of words step by step. In each step it takes, among the words not yet arranged, "
    "the word whose first letter comes latest in the alphabet, replaces that first letter by the letter just before it "
    "in the alphabet (for example, 'nest' becomes 'mest'), and places the new word immediately to the right of the "
    "words already arranged at the left end (in Step I, at the extreme left). The other words keep their order.\n\n"
    "Input: " + line(INP) + "\n\nWhich of the following is Step IV?", line(st[3]),
    [line(st[2]), line(st[4]), line(["vane", "tide", "rope", "moss", "hall", "cork"])],
    "Selection by the first letter, then a one-letter change", steps_join(st[:4]), step_txt(st[:4]),
    why_others_wrong="The first two wrong lines are Steps III and V; the last forgets to change the first letters.",
    seconds=75, verified_by=RECOMP)

# ---- Advanced set A (3): word-number pairs to the right end
INP = ["violet", 28, "amber", 73, "coral", 46, "indigo", 15, "olive", 59]


def pairs008(items):
    ws, ns = sorted(x for x in items if isinstance(x, str)), sorted(x for x in items if isinstance(x, int))
    done, steps, cur = [], [], list(items)
    for w, n in zip(ws, ns):
        done = [w, n + len(w)] + done
        mid = [x for x in items if x not in ws[:ws.index(w) + 1] and x not in ns[:ns.index(n) + 1]]
        new = mid + done
        assert new != cur
        cur = new
        steps.append(cur)
    return steps


st = pairs008(INP)
assert len(st) == 5 and st[-1] == ["violet", 79, "olive", 64, "indigo", 52, "coral", 33, "amber", 20]
sid = stimulus("passage", "Machine: word-number pairs to the right",
               "A word and number arrangement machine rearranges a line step by step. In each step it takes the word "
               "that comes first in alphabetical order among the words not yet arranged and the smallest number among "
               "the numbers not yet arranged. It adds the number of letters in that word to that number, and places "
               "the word followed by the new number at the right end, immediately to the left of the pairs already "
               "placed there (in Step I, at the extreme right). All other elements keep their order. The machine "
               "stops when every element has been arranged.\n\nInput: " + line(INP),
               "Pairs in order: amber + 15 → 20, coral + 28 → 33, indigo + 46 → 52, olive + 59 → 64, violet + 73 → "
               "79.\n\n" + "\n".join(step_txt(st)))
IQ = lambda text, correct, wrongs, concept, expl, steps, **kw: mcq(
    IOT, MM, "Advanced", text, correct, wrongs, concept, expl, steps, stimulus=sid, verified_by=RECOMP, **kw)
IQ("Which of the following is Step III?", line(st[2]),
   [line(st[1]), line(st[3]), line([x for x in st[2] if x not in (52, 33, 20)][:4] + ["indigo", 46, "coral", 28,
                                                                                         "amber", 15])],
   "Pairs with a transformed number", steps_join(st[:3]), step_txt(st[:3]),
   why_others_wrong="The first two wrong lines are Steps II and IV; the last forgets to add the word lengths.",
   seconds=110)
s2 = st[1]
ans = s2[s2.index("amber") - 3]
IQ("In Step II, which element is 3rd to the left of 'amber'?", str(ans),
   [str(x) for x in near(s2, s2.index("amber") - 3) if x != "amber"][:3], "Read the step, then count",
   f"Step II: {line(s2)}. Three places to the left of 'amber' is {ans}.", [f"Step II: {line(s2)}"], seconds=80)
ans = sum(x for x in st[-1] if isinstance(x, int))
IQ("What is the sum of all the numbers in the last step?", str(ans),
   [str(sum(x for x in INP if isinstance(x, int))), str(ans - 6), str(ans + 5)], "Each number gains its word's length",
   f"Last step: {line(st[-1])}. Sum = 79 + 64 + 52 + 33 + 20 = {ans}.", [f"Last step: {line(st[-1])}"], natural=int,
   seconds=85)

# ---- Advanced set B (3): three-digit numbers by the middle digit; first and last digits interchanged
INP = [482, 731, 965, 254, 619, 873]
swap13 = lambda n: int(str(n)[2] + str(n)[1] + str(n)[0])
st = run_select(INP, key=lambda n: (n // 10) % 10, side="left", tf=swap13)
assert len(st) == 6 and not set(map(swap13, INP)) & set(INP)
sid = stimulus("passage", "Machine: middle digits and swapped ends",
               "A number arrangement machine rearranges a line of three-digit numbers step by step. In each step it "
               "takes, among the numbers not yet arranged, the one with the smallest middle (tens) digit, interchanges "
               "its first and last digits, and places the new number immediately to the right of the numbers already "
               "arranged at the left end (in Step I, at the extreme left). The other numbers keep their order. The "
               "machine stops when every number has been arranged.\n\nInput: " + line(INP),
               "Middle digits: 482 → 8, 731 → 3, 965 → 6, 254 → 5, 619 → 1, 873 → 7. Order of selection: 619, 731, "
               "254, 965, 873, 482 → 916, 137, 452, 569, 378, 284.\n\n" + "\n".join(step_txt(st)))
IQ = lambda text, correct, wrongs, concept, expl, steps, **kw: mcq(
    IOT, NR, "Advanced", text, correct, wrongs, concept, expl, steps, stimulus=sid, verified_by=RECOMP, **kw)
IQ("Which of the following is Step II?", line(st[1]),
   [line(st[0]), line(st[2]), line([619, 731] + [x for x in INP if x not in (619, 731)])],
   "Select by the middle digit, then swap the end digits", steps_join(st[:2]), step_txt(st[:2]),
   why_others_wrong="The first two wrong lines are Steps I and III; the last forgets to interchange the digits.",
   seconds=80)
s4 = st[3]
ans = abs(s4[1] - s4[-2])
IQ("In Step IV, what is the difference between the 2nd number from the left and the 2nd number from the right?",
   str(ans), [str(abs(s4[0] - s4[-1])), str(abs(s4[1] - s4[-1])), str(abs(s4[2] - s4[-2]))],
   "Read the step, then subtract", f"Step IV: {line(s4)}. 2nd from the left = {s4[1]}, 2nd from the right = "
                                   f"{s4[-2]}; difference = {ans}.", [f"Step IV: {line(s4)}"], natural=int,
   seconds=90)
ans = sum(1 for x in st[-1] if x % 2)
assert ans == 2
IQ("In the last step, how many of the six three-digit numbers are odd?", num_word(ans), ["Three", "Four", "One"],
   "Swapping the end digits can change a number from odd to even",
   f"Last step: {line(st[-1])}. Only 137 and 569 are odd, so there are two odd numbers (the input had four).",
   [f"Last step: {line(st[-1])}", "Odd: 137, 569"], natural=by_num,
   why_others_wrong="Four counts the odd numbers of the input; Three and One miscount the new numbers.", seconds=80)

# ================================================================================================ DATA SUFFICIENCY (B2, I7, A3)
models = [{"a": a, "b": b} for a in range(0, 601) for b in range(0, 601)]
ds_q("Basic", "Question: How much money does Asha have?\n\nI. Asha and Bela together have ₹500.\nII. Asha has ₹100 "
     "more than Bela.", models, lambda m: m["a"] + m["b"] == 500, lambda m: m["a"] == m["b"] + 100, lambda m: m["a"],
     "T", "Two unknowns need two independent facts",
     "I alone allows many splits of ₹500, and II alone gives only the difference. Together: A + B = 500 and A − B = "
     "100, so A = ₹300.", ["I alone ⇒ not sufficient", "II alone ⇒ not sufficient", "Together: 2A = 600 ⇒ A = ₹300"],
     seconds=45, why="Each 'alone' option relies on one equation in two unknowns; 'together not sufficient' ignores that the two equations fix A.")
models = [{"x": x} for x in range(0, 200)]
ds_q("Basic", "Question: Is the whole number x even?\n\nI. x + 3 is odd.\nII. 5x is even.", models,
     lambda m: (m["x"] + 3) % 2 == 1, lambda m: (5 * m["x"]) % 2 == 0, lambda m: m["x"] % 2 == 0, "E",
     "Each statement on its own",
     "I: odd − 3 is even, so x is even — sufficient. II: 5 is odd, so 5x is even only when x is even — sufficient. "
     "Each statement alone answers 'yes'.", ["I: x = odd − 3 ⇒ even", "II: odd × x even ⇒ x even"], seconds=40,
     why="Each 'alone' option overlooks that the other statement also settles the question; 'both together necessary' needs both when one is enough.")
AL = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
enc = lambda w, s: "".join(AL[(AL.index(c) + s) % 26] for c in w)
models = [{"s": s} for s in range(1, 26)]
ds_q("Intermediate", "Question: In a certain code, every letter of a word is replaced by the letter a fixed number of "
     "places after it in the alphabet (the same number for every letter, counting on from A after Z). What is the code "
     "for 'MAP'?\n\nI. The fixed number of places is an odd number less than 6.\nII. 'GO' is written as 'JR'.", models,
     lambda m: m["s"] in (1, 3, 5), lambda m: enc("GO", m["s"]) == "JR", lambda m: enc("MAP", m["s"]), "B",
     "A shift code is fixed once the shift is known",
     "I allows a shift of 1, 3 or 5 — not sufficient. II: G → J and O → R are shifts of 3, so 'MAP' is 'PDS' — "
     "sufficient.", ["I: shift 1, 3 or 5 ⇒ not sufficient", "II: G → J = +3 ⇒ MAP → PDS"], seconds=55,
     why="'I alone' trusts a statement that leaves three shifts; the 'together' options ignore that II alone fixes the shift.")
assert enc("MAP", 3) == "PDS"
models = [{"a": a, "b": b, "c": c} for a in range(1, 60) for b in range(1, 60) for c in range(1, 60)]
ds_q("Intermediate", "Question: How many years older than Chetan is Amit?\n\nI. Amit is 6 years older than Bhanu.\n"
     "II. Chetan is younger than Bhanu.", models, lambda m: m["a"] == m["b"] + 6, lambda m: m["c"] < m["b"],
     lambda m: m["a"] - m["c"], "N", "An inequality cannot fix a difference",
     "I gives Amit − Bhanu = 6. II says only that Chetan is younger than Bhanu, not by how much. So Amit − Chetan is "
     "more than 6, but could be 7, 8, 9, … — not fixed even with both statements.",
     ["I: A − B = 6", "II: C < B, gap unknown", "Together: A − C > 6 but not fixed ⇒ not sufficient"], seconds=50,
     why="The 'alone' options use one statement; 'both together necessary' treats 'younger' as if it gave the size of the gap.")
Q5 = list("JKLMN")
models = [dict(zip(Q5, p)) for p in itertools.permutations(range(1, 6))]  # 1 = front
ds_q("Intermediate", "Question: Five persons J, K, L, M and N stand in a queue, one behind another. Who stands at the "
     "back of the queue?\n\nI. K is third from the front, and J stands immediately behind K.\nII. M stands somewhere "
     "in front of L, and N stands somewhere in front of M.", models,
     lambda m: m["K"] == 3 and m["J"] == 4, lambda m: m["N"] < m["M"] < m["L"],
     lambda m: next(k for k in Q5 if m[k] == 5), "T", "Fill the free places using the order",
     "I leaves places 1, 2 and 5 for L, M and N in any order — not sufficient. II gives N before M before L, but not "
     "their places — not sufficient. Together, N, M and L take places 1, 2 and 5 in that order, so L is at the back.",
     ["I: K = 3, J = 4; places 1, 2, 5 open", "II: N ahead of M ahead of L", "Together: N 1, M 2, L 5 ⇒ L"],
     seconds=60, why="Each statement alone leaves more than one person for the last place; 'together not "
                     "sufficient' ignores that the order fills the three free places uniquely.")
SUB = ["Maths", "Physics", "Chemistry", "Biology", "English"]
models = [dict(zip(SUB, p)) for p in itertools.permutations(range(1, 6))]
ds_q("Intermediate", "Question: Five subjects — Maths, Physics, Chemistry, Biology and English — are taught in five "
     "periods (1 to 5) on Monday, one subject per period. Which subject is taught in period 4?\n\nI. Biology is taught "
     "in period 2, and Physics is taught in the period immediately after Maths.\nII. Chemistry, Biology and English "
     "are taught in periods 1, 2 and 3 in some order, and Physics is taught in the period immediately after Maths.",
     models, lambda m: m["Biology"] == 2 and m["Physics"] == m["Maths"] + 1,
     lambda m: {m["Chemistry"], m["Biology"], m["English"]} == {1, 2, 3} and m["Physics"] == m["Maths"] + 1,
     lambda m: next(k for k in SUB if m[k] == 4), "B", "Test each statement alone",
     "I: with Biology in period 2, Maths and Physics can be in periods 3–4 or 4–5, so period 4 has Physics or Maths — "
     "not sufficient. II: periods 4 and 5 are left for Maths and Physics, and Physics comes right after Maths, so "
     "Maths is in period 4 — sufficient.",
     ["I: Maths–Physics in 3–4 or 4–5 ⇒ not sufficient", "II: periods 4, 5 = Maths, Physics ⇒ Maths"],
     seconds=55, why="'I alone' trusts a statement that leaves two subjects for period 4; the 'together' options "
                     "ignore that II alone is enough.")
isprime = lambda n: n > 1 and all(n % d for d in range(2, int(n ** 0.5) + 1))
models = [{"n": n} for n in range(10, 100)]
ds_q("Intermediate", "Question: Ravi's roll number is a two-digit number. What is it?\n\nI. It is a prime number, its "
     "digits add up to 10, and its tens digit is greater than its units digit.\nII. Its units digit is 3.", models,
     lambda m: isprime(m["n"]) and m["n"] // 10 + m["n"] % 10 == 10 and m["n"] // 10 > m["n"] % 10,
     lambda m: m["n"] % 10 == 3, lambda m: m["n"], "A", "List the numbers each statement allows",
     "I: the two-digit numbers whose digits add up to 10 and whose tens digit is larger are 64, 73, 82 and 91; "
     "of these only 73 is prime — sufficient. II allows 13, 23, …, 93 — not sufficient.",
     ["I: 64, 73, 82, 91 ⇒ only 73 is prime", "II: nine numbers end in 3 ⇒ not sufficient"], seconds=60,
     why="'II alone' trusts a statement that allows nine numbers; the 'together' options add a statement that is not needed.")
models = [{"g": g, "h": h, "n": n} for n in range(20, 61) for g in range(1, n + 1) for h in range(1, n + 1) if g != h]
ds_q("Intermediate", "Question: In a class with no tied ranks, how many students rank between Gauri and Hema?\n\n"
     "I. Gauri is 8th from the top, and Hema is 15th from the top.\nII. There are 40 students in the class, and Hema "
     "is 26th from the bottom.", models, lambda m: m["g"] == 8 and m["h"] == 15,
     lambda m: m["n"] == 40 and m["n"] - m["h"] + 1 == 26, lambda m: abs(m["g"] - m["h"]) - 1, "A",
     "Ranks between two persons need both ranks from the same end",
     "I: 15 − 8 − 1 = 6 students rank between them — sufficient. II gives only Hema's rank (15th from the top) and "
     "nothing about Gauri — not sufficient.", ["I: 15 − 8 − 1 = 6 ⇒ sufficient", "II: Gauri unknown ⇒ not sufficient"],
     seconds=50, why="'II alone' trusts a statement that never mentions Gauri; the 'together' options add a statement that is not needed.")
models = [{"p": p, "q": q_, "r": r} for p in range(1, 40) for q_ in range(1, 40) for r in range(1, 40)]
ds_q("Intermediate", "Question: What is the weight of box R?\n\nI. Boxes P and Q together weigh 30 kg, and boxes P, Q "
     "and R together weigh 48 kg.\nII. Box Q weighs 12 kg, and box R weighs 6 kg more than box Q.", models,
     lambda m: m["p"] + m["q"] == 30 and m["p"] + m["q"] + m["r"] == 48, lambda m: m["q"] == 12 and m["r"] == 18,
     lambda m: m["r"], "E", "Each statement on its own",
     "I: R = 48 − 30 = 18 kg — sufficient. II: R = 12 + 6 = 18 kg — sufficient.",
     ["I: R = 48 − 30 = 18 kg", "II: R = 12 + 6 = 18 kg"], seconds=45,
     why="Each 'alone' option ignores that the other statement also gives R; 'both together necessary' needs both when either works.")

# ---- Advanced: three statements
V4 = list("ABCD")
models = [dict(zip(V4, p)) for p in itertools.product(range(1, 6), repeat=4)]
ds3_q("Advanced", "Question: Is A greater than D?\n\nI. A ≥ B.\nII. B > C.\nIII. C ≥ D.", models,
      [lambda m: m["A"] >= m["B"], lambda m: m["B"] > m["C"], lambda m: m["C"] >= m["D"]],
      lambda m: m["A"] > m["D"], "ALL", ("I+II", "II+III", "NONE", "ALL"), "A chain needs every link",
      "All three give A ≥ B > C ≥ D, so A > D: 'yes'. Any two statements leave a gap in the chain: I + II says nothing "
      "about D, II + III says nothing about A, and I + III does not connect B with C. So all three are needed.",
      ["I + II + III: A ≥ B > C ≥ D ⇒ A > D", "Any pair leaves A or D unconnected"], seconds=60,
      why="Each pair misses one link of the chain, and with all three the answer is fixed, so 'not sufficient' is "
          "wrong.")
models = [{"x": x, "y": y} for x in range(-30, 31) for y in range(-30, 31)]
ds3_q("Advanced", "Question: What is the value of x + y?\n\nI. x − y = 4.\nII. xy = 21.\nIII. x and y are both "
      "positive integers.", models,
      [lambda m: m["x"] - m["y"] == 4, lambda m: m["x"] * m["y"] == 21, lambda m: m["x"] > 0 and m["y"] > 0],
      lambda m: m["x"] + m["y"], "ALL", ("I+II", "I+III", "ALL", "NONE"), "Watch for negative solutions",
      "I + II: x = 7, y = 3 or x = −3, y = −7, so x + y = 10 or −10 — not sufficient. II + III: (1, 21), (3, 7), "
      "(7, 3), (21, 1) give sums 22 or 10. I + III: infinitely many pairs. All three: x = 7, y = 3, so x + y = 10.",
      ["I + II: (7, 3) or (−3, −7)", "II + III: sums 22 or 10", "All three: x + y = 10"], seconds=90,
      why="I + II forgets the negative pair; I + III gives a whole family; with all three the sum is fixed.")
OW = ["Arun", "Bina", "Chirag", "Dev"]
COL = ["red", "blue", "green", "white"]
models = [dict(zip(OW, p)) for p in itertools.permutations(COL)]
ds3_q("Advanced", "Question: Arun, Bina, Chirag and Dev each own one car, and the four cars are red, blue, green and "
      "white, one of each colour. What is the colour of Arun's car?\n\nI. Bina's car is not blue.\nII. Chirag's car "
      "is white.\nIII. Dev's car is blue, and Bina's car is not green.", models,
      [lambda m: m["Bina"] != "blue", lambda m: m["Chirag"] == "white",
       lambda m: m["Dev"] == "blue" and m["Bina"] != "green"],
      lambda m: m["Arun"], "II+III", ("I+II", "II+III", "ALL", "NONE"), "Pair the statements and test each pair",
      "II + III: Chirag white, Dev blue, Bina not green ⇒ Bina red, so Arun green — sufficient. I + II: Chirag white, "
      "Bina red or green, Arun could be red, blue or green. I + III: Dev blue, Bina red or white, Arun could be red, "
      "green or white. No single statement is enough.",
      ["II + III: Chirag white, Dev blue, Bina red ⇒ Arun green", "I + II and I + III leave Arun open"], seconds=80,
      why="I + II leaves several colours for Arun; II + III already fixes it, so all three are not necessary.")

# ================================================================================================ ASSUMPTIONS (I1)
asm("Intermediate", "The municipal corporation has asked every restaurant in the city to display its food-hygiene "
    "rating at the entrance.",
    "Customers may use the hygiene rating when deciding where to eat.",
    "Every restaurant in the city has the highest hygiene rating.", A_I,
    "Ratings are displayed at the entrance so that customers can see them before choosing a restaurant, so I is "
    "implicit. If every restaurant had the top rating, displaying it would tell customers nothing; II is not assumed "
    "and goes against the purpose of the order.",
    ["Display at the entrance ⇒ customers can use it to choose: I", "Ratings must differ to be useful ⇒ II not "
                                                                    "implicit"],
    "Only II and Both accept a claim that makes the display pointless; Neither ignores why it is displayed.",
    seconds=40)

# ================================================================================================ CONCLUSIONS (B4, I1, A5)
scq("Basic", INF, "Meena's birthday is on 12 August. Today is 5 August of the same year.",
    "Meena's birthday is 7 days from today.", "Meena's birthday has already passed this year.", ONLY_I,
    "From 5 August to 12 August is 12 − 5 = 7 days, so I follows. The birthday is still a week away, so it has not "
    "passed; II is false.", ["12 − 5 = 7 days ahead ⇒ I", "Birthday is still to come ⇒ II false"],
    "Only II and Both accept a conclusion the dates contradict; Neither ignores the simple count.", seconds=30)
scq("Basic", VC, "Rita is taller than Sita, and Sita is taller than Gita.", "Rita is taller than Gita.",
    "Gita is the shortest of the three.", BOTH,
    "Rita > Sita > Gita, so Rita is taller than Gita (I), and Gita is shorter than both the others, so she is the "
    "shortest of the three (II).", ["Rita > Sita > Gita", "⇒ Rita > Gita: I", "⇒ Gita shortest: II"],
    "Each 'Only' option drops one of two direct consequences of the same chain.", seconds=30)
scq("Basic", INF, "A shop offered a 10% discount on all shirts last Sunday.",
    "The shop sold more shirts last Sunday than on the Saturday before it.",
    "The shop had no trousers for sale last Sunday.", NEITHER,
    "The statement tells us only about the discount. It gives no sales figures for either day (I does not follow), "
    "and a discount on shirts says nothing about whether trousers were on sale (II does not follow).",
    ["No sales figures ⇒ I does not follow", "Shirts only mentioned ⇒ nothing about trousers ⇒ II does not follow"],
    "Each other option accepts an outcome or a fact that the statement does not give.", seconds=30)
scq("Basic", INF, "The train to Jaipur left the station on time at 4:15 pm. Ravi reached the station at 4:25 pm.",
    "Ravi will travel to Jaipur by bus.", "Ravi could not board that train at the station.", ONLY_II,
    "The train had left ten minutes before Ravi reached the station, so he could not board it there (II). How he will "
    "travel now, or whether he was going to Jaipur at all, is not stated, so I does not follow.",
    ["Train left 4:15; Ravi arrived 4:25 ⇒ could not board it: II", "His further plans are unknown ⇒ I does not "
                                                                     "follow"],
    "Only I and Both guess Ravi's next step; Neither misses the direct timing.", seconds=30)
scq("Intermediate", INF, "On Monday, every one of the 40 passenger seats on a school bus was occupied by a student, "
    "and 5 more students travelled standing. Apart from the driver, there was no one else on the bus.",
    "The bus carries more than 40 students every day.", "45 students travelled on the bus on Monday.", ONLY_II,
    "On Monday, 40 seated and 5 standing students travelled: 45 in all (II). The statement is about Monday only, so "
    "nothing follows about other days (I).", ["Monday: 40 + 5 = 45 students ⇒ II", "Other days are not described ⇒ I "
                                                                                   "does not follow"],
    "Only I and Both turn a single day into a daily pattern; Neither ignores the direct count.", seconds=40)
scq("Advanced", VC, "In a company, only employees who have completed five years of service are eligible for the "
    "long-service award, and every eligible employee who has no disciplinary record receives it. Leela has completed "
    "seven years of service and has no disciplinary record.", "Leela receives the long-service award.",
    "Every employee who receives the long-service award has completed five years of service.", ONLY_II,
    "'Only employees with five years of service are eligible' makes five years necessary for eligibility, not "
    "enough for it; other conditions may apply. So we cannot say that Leela is eligible, and I does not follow. Every "
    "award-winner must be eligible, and every eligible employee has five years of service, so II follows.",
    ["'Only X are eligible' ⇒ eligible ⇒ X (not X ⇒ eligible)", "Leela's eligibility not established ⇒ I does not "
                                                                  "follow", "Award ⇒ eligible ⇒ five years ⇒ II"],
    "Only I and Both read 'only those with five years' as 'all those with five years'; Neither misses that every "
    "award-winner must be eligible.", seconds=75)
c_, w_ = next((c, 50 - c) for c in range(51) if 2 * c - (50 - c) == 73)
assert (c_, w_) == (41, 9)
scq("Advanced", INF, "A test has 50 questions. Each correct answer earns 2 marks, each wrong answer costs 1 mark, and "
    "an unanswered question earns nothing. Tarun answered all 50 questions and scored 73 marks.",
    "Tarun answered 41 questions correctly.", "Tarun got more than 10 questions wrong.", ONLY_I,
    "If c answers are correct, 50 − c are wrong: 2c − (50 − c) = 73, so 3c = 123 and c = 41 (I). Then 9 answers "
    "were wrong, which is not more than 10, so II is false.",
    ["2c − (50 − c) = 73 ⇒ c = 41: I", "Wrong = 9 ⇒ II false"],
    "Only II and Both accept a count the arithmetic rules out; Neither ignores the direct calculation.", seconds=75)
assert 5 * 4 * 1 + 5 * 4 * 2 == 60 and 40 > 60 / 2
scq("Advanced", INF, "A building has 10 floors with 4 flats on each floor. Every flat on floors 1 to 5 has exactly "
    "one balcony, and every flat on floors 6 to 10 has exactly two balconies.",
    "The flats of the building have 60 balconies in all.",
    "More than half of the flats' balconies are on floors 6 to 10.", BOTH,
    "Floors 1–5: 5 × 4 × 1 = 20 balconies; floors 6–10: 5 × 4 × 2 = 40 balconies. Total 60 (I), and 40 of the 60 "
    "are on floors 6 to 10, which is more than half (II).",
    ["Floors 1–5: 20; floors 6–10: 40", "Total 60 ⇒ I", "40 > 30 ⇒ II"],
    "Each 'Only' option drops one of two direct calculations.", seconds=60)
scq("Advanced", INF, "The average monthly salary of the 10 employees of a firm is ₹30,000.",
    "At least one employee of the firm earns ₹30,000 or more a month.",
    "Every employee of the firm earns at least ₹25,000 a month.", ONLY_I,
    "If every employee earned less than ₹30,000, the average would also be less than ₹30,000. So at least one earns "
    "₹30,000 or more (I). An average says nothing about the lowest salary — one employee could earn ₹10,000 while "
    "others earn more — so II does not follow.",
    ["Not everyone can be below the average ⇒ I", "The minimum is not fixed by the average ⇒ II does not follow"],
    "Only II and Both treat the average as a floor; Neither misses that some value must reach the average.",
    seconds=60)
scq("Advanced", INF, "This year, the number of cars sold by a company fell by 10%, while the number of two-wheelers "
    "it sold rose by 10%.", "The total number of vehicles the company sold this year was the same as last year.",
    "The company sold more two-wheelers than cars this year.", NEITHER,
    "Percentage changes depend on last year's numbers, which are not given. If the company sold more cars than "
    "two-wheelers last year, the total fell; if fewer, it rose — so I does not follow. Whether two-wheelers now "
    "outnumber cars also depends on the starting numbers, so II does not follow.",
    ["Equal percentages on unequal bases ⇒ totals unknown ⇒ I does not follow",
     "Last year's numbers unknown ⇒ II does not follow"],
    "Each other option treats equal percentage changes as if the bases were known.", seconds=60)

# ================================================================================================ CAUSE AND EFFECT (I5)
ceq("Intermediate", "The college raised the fees for its hostel by 40% this year.",
    "Many students of the college moved out of the hostel this year into cheaper shared flats nearby.", "A",
    "A steep rise in hostel fees makes the hostel costlier than shared flats, so students move out to save money. "
    "I explains II.", ["I: hostel fees up 40%", "II: students move to cheaper flats", "I → II"],
    "Students moving out cannot have caused a fee rise announced for the year, so B fails; one statement explains "
    "the other, so neither independent nor common causes fit.", seconds=40)
ceq("Intermediate", "A new metro station opened next to the Sector 18 market last month.",
    "The number of shoppers visiting the Sector 18 market rose sharply this month.", "A",
    "A metro station next to the market makes it much easier for people to reach it, so more shoppers come. The "
    "station (I) came first and explains the rise (II).", ["I: easier access to the market", "II: more shoppers",
                                                          "I → II"],
    "More shoppers this month cannot have caused a station that opened last month (B); no third event is needed.",
    seconds=40)
ceq("Intermediate", "The company recalled 20,000 of its new pressure cookers from the market.",
    "Tests found that the safety valve of the company's new pressure cooker could fail under high pressure.", "B",
    "A product is recalled when it is found to be unsafe. The faulty safety valve (II) is the reason for the recall "
    "(I).", ["II: faulty valve found", "I: cookers recalled", "II → I"],
    "A recall does not create a fault in a valve, so A fails; the fault directly explains the recall.", seconds=40)
ceq("Intermediate", "The price of gold in the country rose to a record high this week.",
    "The city's municipal corporation began a drive to clear encroachments from footpaths this week.", "D",
    "Gold prices depend on world markets and demand for gold; clearing footpaths is a civic decision. Neither explains "
    "the other, and no single event explains both.",
    ["I: market-driven price rise", "II: civic drive", "No link, no shared trigger"],
    "A or B would need gold prices and footpath drives to affect each other; E would need one event behind both.",
    seconds=40)
ceq("Intermediate", "Petrol pumps across the state ran out of fuel this week because fuel tankers did not reach them.",
    "Deliveries of cooking-gas cylinders across the state were badly delayed this week because the trucks carrying "
    "them did not run.", "E",
    "Empty petrol pumps do not delay gas cylinders, and delayed cylinders do not empty petrol pumps. Both are what one "
    "event would produce — for example, a statewide strike by the tanker and truck operators who carry fuel and gas.",
    ["I and II: both depend on fuel transport", "Shared trigger: disruption of fuel transport (e.g., a strike)"],
    "A and B would need one shortage to cause the other; D would need two unrelated reasons in the same week, while "
    "one transport disruption explains both.", seconds=50)

# ================================================================================================ CRITICAL REASONING (B1, I8, A1)
crq("Basic", CA_, "Statement: Every evening, vegetable vendors in a town market throw their unsold and rotting "
    "vegetables on the road, and the heaps attract stray cattle that block traffic.\n\nWhich of the following is the "
    "most appropriate course of action?",
    "Place covered waste bins in the market, collect the market's waste every evening, and fine vendors who dump "
    "waste on the road", ["Close the vegetable market permanently", "Ban the sale of vegetables in the town",
                          "Ask the traffic police to stop vehicles from using the market road"],
    "Remove the cause with a practical, enforceable step",
    "The problem starts with waste dumped on the road. Bins, daily collection and fines stop the dumping, which "
    "removes the heaps, the cattle and the traffic blocks.",
    ["Cause: dumping of waste on the road", "Remedy: bins + daily collection + fines"],
    "Closing the market or banning vegetable sales is extreme; stopping traffic leaves the waste where it is.",
    seconds=30)
crq("Intermediate", SW_, "Argument: An online poll on a bank's website found that 85% of the people who responded "
    "prefer mobile banking to visiting a branch. So the bank can close most of its rural branches without "
    "inconveniencing its customers.\n\nWhich of the following, if true, most seriously weakens the argument?",
    "Most of the bank's rural customers do not use the internet, and very few of them took part in the online poll",
    ["The poll received more than 10,000 responses", "Running a rural branch costs the bank less than running a city "
                                                     "branch", "Some city customers also visit branches"],
    "Weaken: show that the sample does not represent the people affected",
    "The decision affects rural customers, but the poll mostly reached internet users. If rural customers hardly took "
    "part and mostly do not use the internet, the poll says nothing about their needs.",
    ["Evidence: online poll", "Affected group: rural customers", "Weakener: they were missing from the poll"],
    "A large number of responses does not fix a biased sample; branch costs and city customers' habits do not show "
    "how rural customers would be affected.", seconds=70)
crq("Intermediate", SW_, "Argument: The city should set up more public charging points for electric cars, because "
    "the lack of charging points is what is holding back the purchase of electric cars in the city.\n\nWhich of the "
    "following, if true, most strengthens the argument?",
    "In a survey, most car buyers in the city who had considered an electric car said they did not buy one because "
    "they had nowhere to charge it", ["Electric cars are cheaper to run than petrol cars",
                                      "The city has more than five lakh registered cars",
                                      "Charging points can be installed in parking lots"],
    "Strengthen: confirm the cause the argument names",
    "The argument says the shortage of charging points is the obstacle. The survey shows that buyers who considered "
    "electric cars were put off for exactly that reason.",
    ["Claim: lack of charging points blocks purchases", "Strengthener: buyers say so in a survey"],
    "Running costs and the number of cars do not show what stops buyers; that charging points can be installed shows "
    "the plan is possible, not that it would help.", seconds=65)
b_ = next(b for b in range(151) if 300 * b + 200 * (150 - b) == 38000)
assert b_ == 80 and 200 * (150 - b_) == 14000
crq("Intermediate", INFP, "Passage: A theatre sells balcony tickets at ₹300 each and stall tickets at ₹200 each. On "
    "Saturday it sold 150 tickets in all and collected ₹38,000 from them.\n\nWhich of the following can be inferred "
    "from the passage?", "The theatre sold 80 balcony tickets on Saturday",
    ["The theatre sold 70 balcony tickets on Saturday", "The theatre sold more stall tickets than balcony tickets on "
                                                        "Saturday", "The theatre collected ₹16,000 from stall tickets "
                                                                    "on Saturday"],
    "Two conditions fix two unknowns",
    "If b balcony tickets were sold, 300b + 200(150 − b) = 38,000, so 100b = 8,000 and b = 80. Then 70 stall tickets "
    "were sold, bringing in ₹14,000.", ["300b + 200(150 − b) = 38,000", "b = 80; stall = 70; stall income ₹14,000"],
    "70 is the number of stall tickets; stall tickets (70) were fewer than balcony tickets (80); stall income was "
    "₹14,000, not ₹16,000.", seconds=75)
crq("Intermediate", CA_, "Statement: After a new highway opened near a district hospital, the number of patients in "
    "its emergency ward has doubled, and many of them wait for hours before a doctor sees them.\n\nWhich of the "
    "following is the most appropriate course of action?",
    "Add doctors and beds to the emergency ward and set up a trauma-care unit to treat highway accident cases",
    ["Close the new highway", "Refuse to treat patients from other districts",
     "Reduce the working hours of the emergency ward"], "Match capacity to the new demand",
    "Demand has doubled, mainly from the highway. More doctors and beds, plus a trauma unit, add the capacity the "
    "ward now needs.", ["Problem: demand doubled, long waits", "Remedy: more staff, beds and a trauma unit"],
    "Closing the highway is impractical; refusing patients and cutting hours make the problem worse.", seconds=50)
crq("Intermediate", SW_, "Argument: Shops on Gandhi Road that put up bright LED signboards last year reported higher "
    "sales this year than the shops on the road that did not. So bright signboards increase a shop's sales.\n\n"
    "Which of the following, if true, most seriously weakens the argument?",
    "The shops that put up LED signboards were the same shops that also enlarged their premises and stocked more goods "
    "last year", ["LED signboards use less electricity than older signboards",
                  "Some shops on Gandhi Road stay open until 10 pm",
                  "Gandhi Road is one of the busiest roads in the town"],
    "Weaken: point to another difference between the two groups",
    "If the shops with new signboards also expanded and added stock, their higher sales could come from the "
    "expansion, not the signboards.", ["Evidence: signboard shops sold more", "Weakener: those shops also expanded ⇒ "
                                                                             "another cause"],
    "Electricity use, opening hours of some shops and the road's traffic apply to both groups and do not explain the "
    "difference.", seconds=65)
assert 5 * 4 // 2 * 2 == 20
crq("Intermediate", INFP, "Passage: In a quiz tournament, each of five teams played every other team exactly once. "
    "Each match had a winner and a loser; the winner got 2 points and the loser 0.\n\nWhich of the following must be "
    "true?", "The five teams together got 20 points",
    ["Each team won exactly two matches", "At least one team won all its matches",
     "The five teams together got 10 points"], "Count matches first",
    "Five teams playing each other once make 5 × 4 ÷ 2 = 10 matches, and each match gives out exactly 2 points, so "
    "the teams together got 20 points.", ["Matches = 5C2 = 10", "Points = 10 × 2 = 20"],
    "The results of individual teams are not given, so 'two wins each' and 'one unbeaten team' need not be true; 10 "
    "is the number of matches, not points.", seconds=60)
crq("Intermediate", SW_, "Argument: The city's decision to make the first hour of parking free in the old market area "
    "will bring more shoppers to the old market.\n\nWhich of the following, if true, most strengthens the argument?",
    "Shopkeepers in the old market say that many of their former customers now shop at the new mall mainly because "
    "parking there is free", ["The old market has more than 200 shops",
                              "Parking charges in the city were last revised five years ago",
                              "Some shoppers in the old market come on foot"],
    "Strengthen: show that parking cost is what keeps shoppers away",
    "If shoppers left the old market mainly because they had to pay for parking, free parking removes that reason "
    "and is likely to bring some of them back.",
    ["Claim: free parking ⇒ more shoppers", "Strengthener: paid parking is why shoppers left"],
    "The number of shops and when charges were last revised do not link parking to shoppers; shoppers on foot are "
    "unaffected by parking.", seconds=60)
crq("Intermediate", CA_, "Statement: A bank has found that many people who took small business loans under a "
    "government scheme did not know that the loans had to be repaid, and defaults on these loans are rising.\n\nWhich "
    "of the following is the most appropriate course of action?",
    "Explain the repayment terms clearly to every borrower when the loan is given, and send reminders before each "
    "instalment falls due", ["Stop giving loans under the scheme", "Write off all the loans given under the scheme",
                             "Take legal action against every borrower at once"],
    "Remove the misunderstanding that causes the problem",
    "Defaults are rising because borrowers did not know they had to repay. Clear explanation at the start and "
    "reminders later remove that gap without ending the scheme.",
    ["Cause: borrowers unaware of repayment", "Remedy: explain terms + reminders"],
    "Stopping the scheme or writing off loans is extreme; suing every borrower punishes people for a "
    "misunderstanding that the bank can correct.", seconds=55)
crq("Advanced", SW_, "Argument: Since the city introduced a ₹2,000 fine for driving without a seat belt, the number "
    "of drivers caught without a seat belt has fallen by 60%. So many more drivers in the city now wear seat belts."
    "\n\nWhich of the following, if true, most seriously weakens the argument?",
    "During the same period, the traffic police cut the number of seat-belt checkpoints in the city by about "
    "two-thirds", ["The fine for not wearing a helmet was also raised during the same period",
                   "Most new cars warn drivers who have not fastened their seat belts",
                   "Many drivers support the higher fine"],
    "Weaken: show that the measure itself changed",
    "The number of drivers caught depends on how many checks are made. If checkpoints fell by two-thirds, far fewer "
    "drivers would be caught even if just as many drove without seat belts.",
    ["Evidence: fewer drivers caught", "Weakener: far fewer checks ⇒ catches no longer measure behaviour"],
    "The helmet fine concerns two-wheelers; seat-belt warnings in new cars would, if anything, support the argument; "
    "drivers' support for the fine does not show what they do.", seconds=75)


# ################################################################################################ BATCH_009
batch("009")
# ================================================================================================ RANKING (B1, I6)
f_ = next(f for f in range(40) if f + 2 * f + 1 == 31)
ans = 2 * f_ + 1
assert (f_, ans) == (10, 21)
mcq(RNK, POSR, "Basic", "Thirty-one people stand in a queue. Mohan has twice as many people behind him as in front "
    "of him. What is Mohan's position from the back of the queue?", ORDN(ans), ["11th", "20th", "22nd"],
    "People in front + Mohan + people behind = total",
    f"If f people are in front of Mohan, 2f are behind him: f + 1 + 2f = 31, so f = 10. Twenty people are behind him, "
    f"so he is {ans}st from the back.", ["f + 1 + 2f = 31 ⇒ f = 10", "Behind = 20 ⇒ 21st from the back"],
    why_others_wrong="11th is his place from the front; 20th forgets to count Mohan himself; 22nd adds one too many.",
    natural=ord_key, seconds=45, verified_by=RECOMP)

# ---- Intermediate set (3): six trees
T6 = ["P", "Q", "R", "S", "T", "U"]
conds = [("Tree R is taller than exactly four of the other trees.", tuple(T6),
          lambda *v: sum(1 for x in v if x < v[2]) == 4),
         ("Tree Q is taller than tree T but shorter than tree U.", ("Q", "T", "U"), lambda q_, t, u: t < q_ < u),
         ("Tree P is shorter than tree T.", ("P", "T"), lambda p, t: p < t),
         ("Exactly one tree is taller than tree S and shorter than tree R.", ("S", "R"), lambda s, r: r - s == 2)]
H6 = unique(T6, {p: range(1, 7) for p in T6}, conds, [T6])  # 1 = shortest
ORD6 = sorted(T6, key=H6.get, reverse=True)
assert ORD6 == ["U", "R", "Q", "S", "T", "P"]
sid = stimulus("puzzle", "Six trees and their heights",
               "Six trees P, Q, R, S, T and U in a garden have different heights.\n\n" + bullets(conds),
               "R is the 2nd tallest. U > Q > T > P, so U is the tallest. S is two places below R, that is, 4th "
               "tallest; Q, T and P fill the 3rd, 5th and 6th places in that order. Tallest to shortest: "
               + ", ".join(ORD6) + ".")
RQ = lambda text, correct, wrongs, concept, expl, steps, **kw: mcq(RNK, CHW, "Intermediate", text, correct, wrongs,
                                                                    concept, expl, steps, stimulus=sid,
                                                                    verified_by=BRUTE, **kw)
RQ("Which tree is the third tallest?", ORD6[2], ["R", "S", "U"], "Fix the extremes, then the gaps",
   "Order from the tallest: " + ", ".join(ORD6) + ". The third tallest is Q.", ["Order: " + " > ".join(ORD6)],
   why_others_wrong="U is the tallest, R second and S fourth.", seconds=75)
ans = sum(1 for p in T6 if H6[p] > H6["S"])
assert ans == 3
RQ("How many trees are taller than tree S?", num_word(ans), ["Two", "Four", "One"], "Count above a fixed place",
   "S is 4th tallest, so U, R and Q — three trees — are taller than S.", ["S = 4th tallest", "Above: U, R, Q"],
   natural=by_num, why_others_wrong="Two leaves out U; Four counts S itself; One counts only R.", seconds=50)
HT = dict(zip(sorted(T6, key=H6.get), [4, 6, 7, 9, 12, 15]))
ans = HT["T"] + HT["Q"]
assert ans == 15
RQ("The heights of the six trees are 4 m, 6 m, 7 m, 9 m, 12 m and 15 m. What is the combined height of trees T and "
   "Q?", f"{ans} m", ["13 m", "16 m", "19 m"], "Match the sorted heights to the sorted order",
   "From the shortest: P 4 m, T 6 m, S 7 m, Q 9 m, R 12 m, U 15 m. T + Q = 6 + 9 = 15 m.",
   ["Shortest to tallest: P, T, S, Q, R, U", "T = 6 m, Q = 9 m"], natural=lambda t: int(t.split()[0]),
   why_others_wrong="13 m takes S for T; 16 m takes S for Q; 19 m takes R for Q.", seconds=70)

# ---- Intermediate standalone (3)
girls = [p for p in range(1, 41) if p % 4 == 0]
naresh = 40 - 14 + 1
ans = sum(1 for p in girls if p < naresh)
assert naresh == 27 and naresh % 4 and ans == 6
mcq(RNK, POSR, "Intermediate", "Forty students sit in a row facing north. Counting from the left end, every fourth "
    "student (the 4th, 8th, 12th and so on) is a girl, and all the others are boys. Naresh is 14th from the right end. "
    "How many girls sit to the left of Naresh?", num_word(ans), ["Seven", "Five", "Four"],
    "Convert to one end, then count the multiples",
    f"Naresh is 40 − 14 + 1 = {naresh}th from the left. The girls to his left are in places 4, 8, …, 24: six girls.",
    [f"Naresh = {naresh}th from the left", "Girls at 4, 8, 12, 16, 20, 24 ⇒ 6"],
    why_others_wrong="Seven counts place 28, which is to Naresh's right; Five misses one multiple; Four counts the "
                     "girls to his right (28, 32, 36, 40).", natural=by_num, seconds=60, verified_by=RECOMP)
komal_left, total = 7, 21
ans = (total - komal_left) - (komal_left - 1)
assert ans == 8
mcq(RNK, POSR, "Intermediate", "Twenty-one girls stand in a row facing north. Komal is 7th from the left end. How "
    "many girls must leave the row from its right end so that Komal stands exactly in the middle of the row?",
    num_word(ans), ["Seven", "Six", "Fourteen"], "In the middle ⇒ equal numbers on both sides",
    f"Komal has 6 girls to her left and 21 − 7 = 14 to her right. To be in the middle she needs 6 on the right, so "
    f"14 − 6 = {ans} girls must leave.", ["Left of Komal: 6", "Right of Komal: 14", f"Leave: 14 − 6 = {ans}"],
    why_others_wrong="Seven and Six are her place and the girls on her left; Fourteen is the number on her right.",
    natural=by_num, seconds=50, verified_by=RECOMP)
ans = 50 - 18 + 1
assert ans == 33
mcq(RNK, POSR, "Intermediate", "In a class of 50 students with no tied ranks, every student's rank in English is "
    "exactly the reverse of his or her rank in Maths: the student ranked 1st in Maths is ranked last in English, the "
    "student ranked 2nd in Maths is second-last in English, and so on. Tanu ranks 18th in Maths. What is her rank in "
    "English?", ORDN(ans), ["32nd", "18th", "34th"], "A reversed list = the same list counted from the other end",
    f"Reversing the order turns a rank r into 50 − r + 1. Tanu's English rank is 50 − 18 + 1 = {ans}rd.",
    [f"English rank = 50 − 18 + 1 = {ans}"],
    why_others_wrong="32nd forgets the + 1; 18th ignores the reversal; 34th adds 1 twice.", natural=ord_key,
    seconds=50, verified_by=RECOMP)

# ================================================================================================ DATA SUFFICIENCY (B5, I1, A6)
models = [{"p": p, "c": c} for p in range(1, 51) for c in range(1, 51)]
ds_q("Basic", "Question: What is the price of one pen?\n\nI. Three pens and two pencils together cost ₹50.\nII. One "
     "pen and one pencil together cost ₹20.", models, lambda m: 3 * m["p"] + 2 * m["c"] == 50,
     lambda m: m["p"] + m["c"] == 20, lambda m: m["p"], "T", "Two prices need two independent facts",
     "I allows several pairs (for example pen ₹10 and pencil ₹10, or pen ₹14 and pencil ₹4); II allows many splits of "
     "₹20. Together: 3p + 2c = 50 and 2p + 2c = 40, so p = ₹10.",
     ["I alone ⇒ not sufficient", "II alone ⇒ not sufficient", "Together: (3p + 2c) − 2(p + c) = 10 ⇒ p = ₹10"],
     seconds=50, why="Each 'alone' option uses one equation in two unknowns; 'together not sufficient' ignores that "
                     "the two equations fix the price.")
models = [{"dep": d, "dur": u} for d in range(9 * 60, 13 * 60) for u in range(60, 300, 5)]
ds_q("Basic", "Question: At what time did the train leave Station X?\n\nI. The train reached Station Y at 2:40 pm.\n"
     "II. The train was scheduled to leave Station X at 10:40 am, and it left 45 minutes late.", models,
     lambda m: m["dep"] + m["dur"] == 14 * 60 + 40, lambda m: m["dep"] == 10 * 60 + 40 + 45, lambda m: m["dep"], "B",
     "Test each statement alone",
     "I gives only the arrival time; without the journey time the departure is unknown — not sufficient. II: 10:40 am "
     "+ 45 minutes = 11:25 am — sufficient.", ["I: journey time unknown ⇒ not sufficient", "II: 10:40 + 0:45 = 11:25"],
     seconds=40, why="'I alone' needs the journey time, which is not given; the 'together' options ignore that II "
                     "alone answers.")
K4 = ["Dev", "Eshan", "Farah", "Gita"]
models = [dict(zip(K4, p)) for p in itertools.permutations(range(1, 5))]  # larger = older
ds_q("Basic", "Question: Dev, Eshan, Farah and Gita are four children of different ages. Is Dev the eldest of the "
     "four?\n\nI. Dev is older than Eshan, and Eshan is older than both Farah and Gita.\nII. Gita is the youngest of "
     "the four.", models, lambda m: m["Dev"] > m["Eshan"] > max(m["Farah"], m["Gita"]),
     lambda m: m["Gita"] == 1, lambda m: m["Dev"] == 4, "A", "A yes/no question is settled if every case agrees",
     "I: Dev > Eshan > Farah and Gita, so Dev is older than all three — 'yes'. II says nothing about Dev's place "
     "among the other three — not sufficient.", ["I: Dev > Eshan > Farah, Gita ⇒ yes", "II: only Gita placed ⇒ not "
                                                                                       "sufficient"],
     seconds=40, why="'II alone' places only Gita; the 'together' options add a statement that is not needed.")
F4 = ["Kunal", "Lata", "Mohit", "Neha"]
models = [dict(zip(F4, p)) for p in itertools.permutations(range(1, 5))]  # floor 1 = lowermost
ds_q("Basic", "Question: Kunal, Lata, Mohit and Neha live on the four floors of a building, one on each floor (floor "
     "1 is the lowermost). On which floor does Kunal live?\n\nI. Exactly one person lives above Kunal.\nII. Neha lives on "
     "the topmost floor, and Kunal lives immediately below Neha.", models,
     lambda m: sum(1 for k in F4 if m[k] > m["Kunal"]) == 1,
     lambda m: m["Neha"] == 4 and m["Kunal"] == 3, lambda m: m["Kunal"], "E", "Each statement on its own",
     "I: exactly one person lives above Kunal, so he is on floor 3. II: Neha is on floor 4 and Kunal just below her, "
     "on floor 3. Each statement alone gives floor 3.", ["I: one person above ⇒ floor 3", "II: below floor 4 ⇒ floor 3"],
     seconds=40, why="Each 'alone' option misses that the other statement also fixes the floor; 'both together "
                     "necessary' needs both when either works.")
models = [{"t": t, "p": p} for t in range(1, 61) for p in range(0, 61) if p <= t]
ds_q("Basic", "Question: How many students of Class 8B passed the test?\n\nI. 40 students of Class 8B took the test, "
     "and 60% of them passed.\nII. 40 students of Class 8B took the test, and 16 of them failed.", models,
     lambda m: m["t"] == 40 and m["p"] * 100 == 60 * m["t"], lambda m: m["t"] == 40 and m["t"] - m["p"] == 16,
     lambda m: m["p"], "E", "Each statement on its own",
     "I: 60% of 40 = 24 passed. II: 40 − 16 = 24 passed. Each statement alone gives the answer.",
     ["I: 0.6 × 40 = 24", "II: 40 − 16 = 24"], seconds=35,
     why="Each 'alone' option misses that the other statement also works; 'both together necessary' needs both when "
         "either is enough.")
S4 = ["Kavi", "Leena", "Mona", "Neel"]
models = [dict(zip(S4, (0,) + p)) for p in itertools.permutations(range(1, 4))]  # right of a seat = +1
ds_q("Intermediate", "Question: Kavi, Leena, Mona and Neel sit at a square table, one on each side, all facing the "
     "centre. Who sits opposite Kavi?\n\nI. Leena sits immediately to the right of Kavi.\nII. Mona sits immediately "
     "to the left of Kavi.", models, lambda m: m["Leena"] == 1, lambda m: m["Mona"] == 3,
     lambda m: next(k for k in S4 if m[k] == 2), "T", "Four seats: right, left and opposite",
     "I fixes only Kavi's right; Mona and Neel could take either of the other two seats — not sufficient. II fixes "
     "only Kavi's left; Leena and Neel could take either remaining seat — not sufficient. Together, the right and left "
     "seats are Leena and Mona, so Neel sits opposite Kavi.",
     ["I: right = Leena; opposite = Mona or Neel", "II: left = Mona; opposite = Leena or Neel",
      "Together: opposite = Neel"], seconds=50,
     why="Each statement alone leaves two people for the opposite seat; 'together not sufficient' ignores that the two "
         "fixed neighbours leave only Neel.")

# ---- Advanced: three statements
models = [{"n": n} for n in range(1, 200)]
ds3_q("Advanced", "Question: What is the value of the positive integer n?\n\nI. n is a factor of 36.\nII. n is a "
      "multiple of 4.\nIII. n is greater than 10.", models,
      [lambda m: 36 % m["n"] == 0, lambda m: m["n"] % 4 == 0, lambda m: m["n"] > 10],
      lambda m: m["n"], "NONE", ("I+II", "I+III", "ALL", "NONE"), "Check whether even all three fix the answer",
      "Factors of 36: 1, 2, 3, 4, 6, 9, 12, 18, 36. With II they are 4, 12 and 36; with III as well, 12 and 36 remain. "
      "Even all three statements leave two values, so they are not sufficient.",
      ["I + II: 4, 12, 36", "I + III: 12, 18, 36", "All three: 12 or 36 ⇒ not sufficient"], seconds=75,
      why="Every pair leaves several values, and even all three leave 12 and 36.")
models = [{"s": s, "d": d} for s in range(12 * 60, 18 * 60, 5) for d in range(30, 241, 5)]
ds3_q("Advanced", "Question: At what time did the meeting begin?\n\nI. The meeting lasted 90 minutes.\nII. The "
      "meeting ended at 4:15 pm.\nIII. Tea was served exactly halfway through the meeting, at 3:30 pm.", models,
      [lambda m: m["d"] == 90, lambda m: m["s"] + m["d"] == 16 * 60 + 15, lambda m: 2 * m["s"] + m["d"] == 2 * 210 + 2 * 12 * 60],
      lambda m: m["s"], "ANY2", ("I+II", "II+III", "ANY2", "ALL"), "Two of start, end, length and midpoint fix the rest",
      "I + II: 4:15 pm − 90 min = 2:45 pm. I + III: 3:30 pm − 45 min = 2:45 pm. II + III: the midpoint 3:30 pm is 45 "
      "minutes before the end, so the meeting lasted 90 minutes and began at 2:45 pm. Any two statements are enough; "
      "none alone is.", ["I + II: 4:15 − 1:30 = 2:45", "I + III: 3:30 − 0:45 = 2:45", "II + III: 3:30 − 0:45 = 2:45"],
      seconds=80, why="Each listed pair works, so no single pair is the only sufficient one, and all three are not "
                      "needed.")
models = [{"p": p, "q": q_, "r": r} for p in range(1, 80) for q_ in range(1, 80) for r in range(1, 80)]
ds3_q("Advanced", "Question: What is the weight of box Q?\n\nI. Boxes P and Q together weigh 50 kg.\nII. Boxes Q "
      "and R together weigh 60 kg.\nIII. Boxes P and R together weigh 70 kg.", models,
      [lambda m: m["p"] + m["q"] == 50, lambda m: m["q"] + m["r"] == 60, lambda m: m["p"] + m["r"] == 70],
      lambda m: m["q"], "ALL", ("I+II", "II+III", "ALL", "NONE"), "Three unknowns need three equations",
      "Any two statements give two equations in three unknowns — not sufficient. All three: P + Q + R = (50 + 60 + "
      "70) ÷ 2 = 90, so Q = 90 − 70 = 20 kg.", ["Any pair: two equations, three unknowns", "All: total 90 ⇒ Q = 20 kg"],
      seconds=80, why="Each pair leaves one weight free; with all three the weight of Q is fixed, so 'not sufficient' "
                      "is wrong.")
models = [{"a": a, "b": b} for a in range(1, 100) for b in range(1, 100)]
ds3_q("Advanced", "Question: What is Anil's present age?\n\nI. Anil is twice as old as Bimal.\nII. Bimal is younger "
      "than 15.\nIII. Five years ago, Anil was three times as old as Bimal was then.", models,
      [lambda m: m["a"] == 2 * m["b"], lambda m: m["b"] < 15, lambda m: m["a"] - 5 == 3 * (m["b"] - 5)],
      lambda m: m["a"], "I+III", ("I+II", "I+III", "II+III", "ALL"), "Two independent equations fix two ages",
      "I + III: A = 2B and A − 5 = 3(B − 5), so 2B − 5 = 3B − 15, B = 10 and A = 20 — sufficient. I + II allows "
      "B = 1 to 14, so A is not fixed. II + III: A = 3B − 10 with B < 15 still allows several ages. No statement alone "
      "is enough.", ["I + III: 2B − 5 = 3B − 15 ⇒ B = 10, A = 20", "I + II and II + III: several ages"], seconds=80,
      why="I + II and II + III leave many ages; II is not needed once I and III are used.")
R5 = list("PQRST")
models = [dict(zip(R5, p)) for p in itertools.permutations(range(1, 6))]  # 1 = left end, all facing north
ds3_q("Advanced", "Question: Five persons P, Q, R, S and T sit in a row, all facing north. Who sits second from the "
      "right end?\n\nI. R sits second to the right of P.\nII. Q and T sit at the two ends of the row.\nIII. S sits "
      "immediately to the left of R.", models,
      [lambda m: m["R"] == m["P"] + 2, lambda m: {m["Q"], m["T"]} == {1, 5}, lambda m: m["S"] == m["R"] - 1],
      lambda m: next(k for k in R5 if m[k] == 4), "I+II", ("I+II", "II+III", "ALL", "NONE"),
      "Pair the statements and test each pair",
      "I + II: P, R and the person between them fill places 2, 3 and 4, so P is 2nd and R is 4th — R is second from "
      "the right. II + III: S and R are next to each other in places 2–4, so the 4th place could be R or P. I + III "
      "puts P, S and R together but not where. No single statement is enough.",
      ["I + II: P 2nd, R 4th ⇒ R", "II + III: 4th = R or P", "I + III: block of three not fixed"], seconds=85,
      why="II + III leaves two people for the place; I + II already fixes it, so all three are not necessary.")
models = [{"two": a, "five": b} for a in range(0, 40) for b in range(0, 40)]
ds3_q("Advanced", "Question: Sapna has only ₹2 coins and ₹5 coins. How many ₹5 coins does she have?\n\nI. She has 20 "
      "coins in all.\nII. Her coins are worth ₹67 in all.\nIII. She has more ₹2 coins than ₹5 coins.", models,
      [lambda m: m["two"] + m["five"] == 20, lambda m: 2 * m["two"] + 5 * m["five"] == 67,
       lambda m: m["two"] > m["five"]],
      lambda m: m["five"], "I+II", ("I+II", "II+III", "ANY2", "NONE"), "Number and value of coins fix both counts",
      "I + II: t + f = 20 and 2t + 5f = 67 give 3f = 27, so f = 9 — sufficient. II + III allows (31, 1), (26, 3), "
      "(21, 5), (16, 7) and (11, 9) — not sufficient. I + III allows f = 0 to 9. No statement alone is enough.",
      ["I + II: 3f = 67 − 40 = 27 ⇒ f = 9", "II + III: five possibilities", "I + III: f = 0 to 9"], seconds=85,
      why="II + III and I + III leave several counts, so 'any two' is wrong; I + II fixes the count.")

# ================================================================================================ ASSUMPTIONS (I6, A1)
asm("Intermediate", "The state electricity board has asked consumers to pay their bills online to avoid the long "
    "queues at its offices.",
    "Many consumers are able to pay their bills online.",
    "Long queues form at the board's offices when consumers pay their bills there.", A_B,
    "Asking consumers to pay online makes sense only if many of them can (I), and the stated reason — avoiding long "
    "queues — takes for granted that paying at the offices causes such queues (II).",
    ["Advice must be practicable ⇒ I", "Stated purpose ⇒ queues exist at the offices ⇒ II"],
    "Each 'Only' option drops one of two things the advice rests on.", seconds=40)
asm("Intermediate", "Advertisement of a cricket academy: \"Learn from coaches who have played for the state team — "
    "join now!\"",
    "People who want to learn cricket value being coached by experienced players.",
    "Every student who joins the academy will go on to play for the state team.", A_I,
    "The advertisement highlights the coaches' playing record because it expects learners to value it (I). It makes "
    "no promise that every student will reach the state team, and nothing in it depends on that (II).",
    ["Selling point = coaches' experience ⇒ learners value it: I", "No promise of selection ⇒ II not implicit"],
    "Only II and Both accept a promise the advertisement never makes; Neither ignores its selling point.", seconds=40)
asm("Intermediate", "Notice near the lifts of an office building: \"In case of fire, do not use the lifts.\"",
    "Using a lift during a fire may be dangerous.",
    "There is another way, such as a staircase, to leave the building during a fire.", A_B,
    "People are told not to use the lifts in a fire only because lifts are considered unsafe then (I). Telling people "
    "not to use the lifts in an emergency takes for granted that they have another way out (II).",
    ["Ban on lifts ⇒ lifts seen as unsafe: I", "No lifts in an emergency ⇒ another exit exists: II"],
    "Each 'Only' option drops one of two things the notice needs.", seconds=40)
asm("Intermediate", "The principal announced, \"The school's annual sports day will be held on the first Saturday of "
    "December.\"",
    "It never rains in December.",
    "Every student of the school will win at least one prize on sports day.", A_N,
    "The announcement only fixes a date. It does not need December to be free of rain on every day ('never' is too "
    "strong), and it says nothing about prizes.",
    ["'Never rains' is an extreme claim ⇒ I not implicit", "Prizes are not mentioned ⇒ II not implicit"],
    "Each other option accepts a claim that the announcement does not rely on.", seconds=35)
asm("Intermediate", "A bank's message to its customers: \"Never share your card PIN with anyone, including people "
    "who say they are bank staff.\"",
    "The bank's staff regularly ask customers for their PINs.",
    "Some people may try to get customers' PINs by pretending to be bank staff.", A_II,
    "The warning about people who 'say they are bank staff' is given because fraudsters may pose as staff (II). The "
    "message implies that genuine staff do not ask for PINs, so I goes against it.",
    ["Warning about pretenders ⇒ II", "Bank says never share, even with staff ⇒ I contradicts the message"],
    "Only I and Both accept a claim the message contradicts; Neither misses the reason for the warning.", seconds=40)
asm("Intermediate", "A traffic-police advertisement: \"Renew your vehicle's pollution-under-control certificate before "
    "it expires, to avoid a fine.\"",
    "The traffic police check whether vehicles have valid pollution certificates.",
    "Most vehicles in the city cause heavy pollution.", A_I,
    "The threat of a fine is real only if the police check certificates (I). The advertisement is about keeping the "
    "certificate valid; it does not assume that most vehicles pollute heavily (II).",
    ["Fine for expiry ⇒ certificates are checked: I", "No claim about how much vehicles pollute ⇒ II not implicit"],
    "Only II and Both accept a sweeping claim; Neither ignores how the fine works.", seconds=40)
asm("Advanced", "The city has decided to fit every ambulance with a remote device that turns the traffic signals ahead "
    "of it green.",
    "Once the devices are fitted, ambulances will no longer need sirens.",
    "Delays at traffic signals slow ambulances down.", A_II,
    "The devices are meant to save time at signals, which assumes that signals now delay ambulances (II). Green "
    "signals do not clear the vehicles already on the road, so the plan does not assume that sirens become "
    "unnecessary (I).", ["Purpose: save time at signals ⇒ II", "Sirens still needed for traffic on the road ⇒ I not "
                                                                "implicit"],
    "Only I and Both read too much into the plan; Neither misses why the devices are fitted.", seconds=50)

# ================================================================================================ CONCLUSIONS (I1)
assert (10 * 60 + 45 + 150) == 13 * 60 + 15
scq("Intermediate", INF, "A meeting began at 10:45 am and lasted 2 hours 30 minutes without a break. Lunch at the "
    "office is served at 1:00 pm.", "The meeting ended at 1:15 pm.", "The meeting ended before lunch was served.",
    ONLY_I, "10:45 am + 2 hours 30 minutes = 1:15 pm (I). Lunch is served at 1:00 pm, which is before the meeting "
    "ended, so II is false.", ["10:45 + 2:30 = 13:15 = 1:15 pm ⇒ I", "1:15 pm is after 1:00 pm ⇒ II false"],
    "Only II and Both accept a timing the arithmetic rules out; Neither ignores the direct calculation.", seconds=40)

# ================================================================================================ CAUSE AND EFFECT (B4, A5)
ceq("Basic", "A power cut hit the whole town from 6 pm to 10 pm on Saturday.",
    "The town's only cinema hall, which has no power generator, cancelled its 7 pm show on Saturday.", "A",
    "A cinema with no generator cannot run a show without electricity, and the 7 pm show fell inside the power cut. "
    "I explains II.", ["I: no power 6–10 pm", "II: 7 pm show cancelled; no generator", "I → II"],
    "A cancelled show cannot cause a town-wide power cut (B); no outside event is needed to explain II.", seconds=35)
ceq("Basic", "The village panchayat installed solar-powered streetlights along all the village roads.",
    "The village roads were dark at night because there was no electricity connection for streetlights.", "B",
    "The roads had no lights for lack of an electricity connection, so the panchayat chose lights that need none. II "
    "is the reason for I.", ["II: roads dark; no power connection", "I: solar lights installed", "II → I"],
    "Installing lights cannot cause the earlier darkness (A); the two are directly linked.", seconds=35)
ceq("Basic", "A famous singer released her new album on Friday.",
    "The city's water department repaired a leaking pipeline on Friday.", "D",
    "An album release follows the singer's own plans; a pipeline repair follows a leak. Neither explains the other, "
    "and no single event lies behind both.", ["I: music industry decision", "II: civic repair", "No link"],
    "A or B would need the album and the repair to affect each other; E would need one shared reason.", seconds=30)
ceq("Basic", "Several matches of the city's open-air cricket tournament were called off this week.",
    "The lake in the city overflowed this week for the first time in ten years.", "E",
    "Called-off cricket matches cannot make a lake overflow, and an overflowing lake does not stop matches across the "
    "city. Both are typical results of one event — very heavy rain in the city this week.",
    ["I: outdoor matches called off", "II: lake overflows", "Shared trigger: very heavy rain"],
    "A or B would need one statement to produce the other; D would need two unrelated reasons, while heavy rain "
    "explains both.", seconds=40)
ceq("Advanced", "The government cut the import duty on edible oils from 20% to 5%.",
    "Retail prices of imported edible oils fell over the next few weeks.", "A",
    "A lower import duty lowers the landed cost of imported oils, and lower costs pass into lower retail prices over "
    "the following weeks. I explains II.", ["I: import duty cut", "II: retail prices of imported oils fall", "I → II"],
    "Falling prices that came after the duty cut cannot have caused it (B); the link is direct, so D and E do not "
    "fit.", seconds=50)
ceq("Advanced", "The bank has begun asking customers for a one-time code, in addition to their password, every time "
    "they log in to its net-banking website.",
    "Last month, many of the bank's customers lost money after their net-banking passwords were stolen.", "B",
    "When stolen passwords lead to losses, a bank adds a second check so that a password alone is no longer enough. "
    "II is the reason for I.", ["II: losses through stolen passwords", "I: extra login check added", "II → I"],
    "A new login check cannot cause losses that happened last month (A); the extra check answers that problem "
    "directly.", seconds=55)
ceq("Advanced", "The country's exports of rice rose by 12% this year.",
    "A state government opened 50 new primary health centres this year.", "D",
    "Rice exports depend on harvests and world demand; opening health centres is a state health-policy decision. "
    "Neither explains the other, and nothing suggests one event behind both.",
    ["I: trade outcome", "II: state health decision", "No link, no shared trigger"],
    "A or B would need exports and health centres to affect each other; E would need a common cause.", seconds=45)
ceq("Advanced", "The retail price of onions in the country's markets doubled in the first half of this month.",
    "In the second half of this month, the government banned the export of onions.", "A",
    "When onion prices at home shoot up, the government stops exports so that more onions stay in the domestic market "
    "and prices come down. I explains II. A ban on exports keeps more onions at home, which would lower prices, so it "
    "cannot be the cause of the rise.", ["I: domestic prices double", "II: export ban to keep onions at home", "I → II"],
    "B fails because an export ban increases supply at home and would push prices down, not up; the link is direct.",
    seconds=55)
ceq("Advanced", "Several banks raised the interest rates on their fixed deposits this week.",
    "Several banks raised the interest rates on their home loans this week.", "E",
    "Banks raise both deposit and loan rates together when their own cost of funds rises, as after an increase in "
    "the central bank's policy rate. Higher deposit rates do not by themselves explain higher loan rates (banks "
    "could absorb the cost), and higher loan rates do not explain higher deposit rates; both follow from the same "
    "change.", ["I and II: both are rate rises by banks", "Shared trigger: a rise in the policy rate / cost of funds"],
    "A or B would need one rate rise to cause the other; D would need two unrelated reasons, while one policy change "
    "explains both.", seconds=60)

# ================================================================================================ CRITICAL REASONING (B2, I7, A2)
import math
fee = 20 + 10 * math.ceil((200 - 60) / 60)
assert fee == 50
crq("Basic", INFP, "Passage: A parking lot charges ₹20 for the first hour and ₹10 for each additional hour or part of "
    "an hour. Rohit parked his car there from 9:00 am to 12:20 pm the same day.\n\nWhich of the following can be "
    "inferred from the passage?", "Rohit paid ₹50 for parking", ["Rohit paid ₹40 for parking",
                                                                "Rohit paid ₹45 for parking",
                                                                "Rohit paid ₹60 for parking"],
    "Part of an hour counts as a full hour",
    "Rohit parked for 3 hours 20 minutes: the first hour costs ₹20, and the remaining 2 hours 20 minutes count as "
    "three additional hours (₹30). Total ₹50.", ["Duration: 3 h 20 min", "₹20 + 3 × ₹10 = ₹50"],
    "₹40 ignores the part hour; ₹45 charges half for it; ₹60 charges an extra hour.", seconds=45)
crq("Basic", CA_, "Statement: Students of a college complain that the food in the college canteen is often stale, and "
    "several students fell ill last week after eating there.\n\nWhich of the following is the most appropriate course "
    "of action?", "Get the canteen inspected, require food to be cooked fresh every day, and act against the canteen "
                  "contractor if the standards are not met",
    ["Close the college for a week", "Ask the students to stop eating lunch", "Shorten the lunch break"],
    "Fix the source of the problem", "The problem is unsafe food from the canteen. Inspection, fresh-cooking rules and "
                                     "action against the contractor address it directly.",
    ["Problem: stale food, illness", "Remedy: inspect, set standards, enforce"],
    "Closing the college and skipping lunch are extreme; a shorter lunch break does nothing about the food.",
    seconds=30)
crq("Intermediate", SW_, "Argument: Families that own pets report lower stress than families that do not. So getting a "
    "pet reduces a family's stress.\n\nWhich of the following, if true, most seriously weakens the argument?",
    "Families that already have low stress and plenty of free time are much more likely to decide to get a pet",
    ["Dogs are the most popular pets in the country", "Pet food has become costlier in recent years",
     "Some pet-owning families have more than one pet"], "Weaken: the causation may run the other way",
    "If calm families with free time are the ones that get pets, low stress may be the reason for owning a pet rather "
    "than its result, so the comparison does not show that pets reduce stress.",
    ["Evidence: pet owners less stressed", "Weakener: low stress leads to pet ownership"],
    "The most popular pet, food prices and the number of pets do not explain why pet owners are less stressed.",
    seconds=60)
crq("Intermediate", SW_, "Argument: The town should replace its old water pipes, because the pipes are the main "
    "reason the town's tap water is often dirty.\n\nWhich of the following, if true, most strengthens the argument?",
    "Water samples taken at the town's treatment plant are clean, but samples of the same water taken from taps after "
    "it passes through the old pipes are often dirty",
    ["The old pipes were laid more than forty years ago", "New pipes will cost the town ₹12 crore",
     "Most towns in the state get their water from rivers"], "Strengthen: locate the problem in the pipes",
    "If the water leaves the plant clean and arrives dirty, it is being dirtied on the way — in the pipes — which "
    "supports replacing them.", ["Clean at the plant, dirty at the tap ⇒ pipes are the source"],
    "The pipes' age suggests but does not show the cause; cost and other towns' water sources are irrelevant.",
    seconds=60)
crq("Intermediate", INFP, "Passage: In an office, every employee in the Accounts team sits on the 3rd floor. Every "
    "employee who sits on the 3rd floor has a laptop. Some employees who have laptops work from home on Fridays."
    "\n\nWhich of the following must be true?", "Every member of the Accounts team has a laptop",
    ["Every employee who has a laptop sits on the 3rd floor", "Some members of the Accounts team work from home on "
                                                              "Fridays", "No one who sits on the 3rd floor works from "
                                                                         "home on Fridays"],
    "Chain 'every' statements in the forward direction only",
    "Accounts ⇒ 3rd floor ⇒ laptop, so every Accounts member has a laptop. The 'some' statement about laptop owners "
    "says nothing certain about the Accounts team or the 3rd floor.",
    ["Accounts ⊆ 3rd floor ⊆ laptop users", "'Some laptop users work from home' does not pass down the chain"],
    "The first wrong option reverses 'every 3rd-floor employee has a laptop'; the other two draw definite "
    "conclusions from a 'some' statement.", seconds=60)
crq("Intermediate", CA_, "Statement: Farmers in a district complain that they must carry their vegetables 40 km to "
    "the nearest wholesale market, and much of the produce spoils on the way.\n\nWhich of the following is the most "
    "appropriate course of action?",
    "Set up collection centres in the district with refrigerated transport to the wholesale market, or open a market "
    "yard within the district", ["Ask the farmers to grow fewer vegetables", "Close the wholesale market",
                                 "Ban the transport of vegetables out of the district"],
    "Shorten the distance or protect the produce on the way",
    "Spoilage comes from the long trip without proper transport. Local collection with refrigerated transport, or a "
    "market yard nearby, removes that loss.", ["Problem: distance + spoilage", "Remedy: local collection or market"],
    "Growing less cuts farmers' income; closing the market or banning transport makes selling impossible.",
    seconds=50)
crq("Intermediate", SW_, "Argument: Most people who were cheated in online-shopping frauds in the country last year "
    "were between 20 and 35 years old. So people aged 20 to 35 are more careless online than older people.\n\nWhich "
    "of the following, if true, most seriously weakens the argument?",
    "People aged 20 to 35 make up about 80% of all online shoppers in the country",
    ["Online-shopping frauds rose by 25% last year", "Many fraud victims did not report the fraud to the police",
     "People aged 20 to 35 shop online mostly on their phones"], "Weaken: compare with the size of each group",
    "If this age group makes up most online shoppers, it would account for most fraud victims even if its members "
    "were no more careless than anyone else. The raw share of victims does not show a higher rate of carelessness.",
    ["Evidence: most victims are 20–35", "Weakener: most shoppers are 20–35 ⇒ share of victims expected"],
    "A rise in frauds and unreported cases do not compare age groups; the device used does not show carelessness.",
    seconds=70)
packs = [(a, b) for a in range(10) for b in range(6) if 6 * a + 10 * b == 46]
assert packs == [(1, 4), (6, 1)]
crq("Intermediate", INFP, "Passage: A shop sells pens only in packs of 6 and packs of 10. Ankit bought exactly 46 pens "
    "from the shop.\n\nWhich of the following must be true?", "Ankit bought at least one pack of each size",
    ["Ankit bought 7 packs in all", "Ankit bought more packs of 6 than packs of 10",
     "Ankit bought exactly 4 packs of 10"], "List every possibility before choosing 'must'",
    "6a + 10b = 46 has only two whole-number solutions: one pack of 6 with four packs of 10, or six packs of 6 with one "
    "pack of 10. In both, he bought at least one pack of each size.",
    ["6a + 10b = 46 ⇒ (a, b) = (1, 4) or (6, 1)", "Both include each size"],
    "7 packs, more packs of 6, and exactly 4 packs of 10 are each true for only one of the two possibilities.",
    seconds=70)
crq("Intermediate", CA_, "Statement: Many senior citizens in a city do not claim the pension they are entitled to, "
    "because the application form is long and must be submitted in person at a single office in the city.\n\nWhich "
    "of the following is the most appropriate course of action?",
    "Shorten the form and let it be submitted online or at ward offices, with help desks for senior citizens",
    ["Stop the pension scheme for new applicants", "Raise the amount of the pension",
     "Pay the pension only to those who have already applied"], "Remove the barrier that keeps people out",
    "Eligible people are left out because applying is hard. A shorter form, more places to apply and help desks make "
    "it easy for them to claim.", ["Barrier: long form, one office", "Remedy: shorter form, online/ward submission, "
                                                                     "help desks"],
    "Stopping the scheme or limiting it to current applicants leaves the eligible out; a higher pension does not "
    "help people who cannot apply.", seconds=50)
crq("Advanced", SW_, "Argument: The state should make all its government offices paperless within one year, because "
    "this would save about ₹500 crore a year on paper and printing.\n\nWhich of the following, if true, most "
    "seriously weakens the argument?",
    "Most government offices in the state have no computers or internet connection, and equipping them would take "
    "at least five years", ["Paper is made from wood pulp", "Several private companies in the state are already "
                                                            "paperless", "The state spends more on salaries than on "
                                                                         "paper"],
    "Weaken: attack the plan's feasibility within the stated time",
    "The proposal is to go paperless within one year. If most offices lack the computers and connections needed and "
    "setting them up takes five years, the plan cannot be carried out on time, whatever its savings.",
    ["Proposal: paperless in one year", "Weakener: infrastructure needs five years ⇒ not feasible"],
    "The source of paper is irrelevant; private firms' success supports the idea; comparing salaries with paper "
    "costs does not deny the savings.", seconds=70)
leena, mohan = 0.04 * (25000 - 10000), 0.04 * (12000 - 10000)
assert (leena, mohan) == (600, 80) and leena / mohan == 7.5
crq("Advanced", INFP, "Passage: A bank pays interest on a savings account only on the part of the balance above "
    "₹10,000, at 4% a year. Leena kept ₹25,000 in her account for a full year and Mohan kept ₹12,000 in his for a "
    "full year; neither balance changed during the year.\n\nWhich of the following must be true?",
    "Leena earned more than seven times as much interest as Mohan",
    ["Leena earned ₹1,000 as interest", "Mohan earned ₹480 as interest",
     "Leena earned a little more than twice as much interest as Mohan"],
    "Apply the rate only to the part above the threshold",
    "Leena earns 4% of ₹15,000 = ₹600; Mohan earns 4% of ₹2,000 = ₹80. ₹600 is 7.5 times ₹80.",
    ["Leena: 0.04 × 15,000 = ₹600", "Mohan: 0.04 × 2,000 = ₹80", "600 ÷ 80 = 7.5"],
    "₹1,000 and ₹480 apply the rate to the whole balance; 'about twice' compares the balances, not the interest.",
    seconds=80)


# ################################################################################################ BATCH_010
batch("010")
# ================================================================================================ RANKING (B5, A4)
tia = 26 - 12 + 1
ans = tia - 1
assert (tia, ans) == (15, 14)
mcq(RNK, POSR, "Basic", "Twenty-six children sit in a row facing north. Tia is 12th from the right end. How many "
    "children sit to the left of Tia?", num_word(ans), ["Fifteen", "Eleven", "Thirteen"],
    "Children to the left = position from the left − 1",
    f"Tia is 26 − 12 + 1 = {tia}th from the left, so {ans} children sit to her left.",
    [f"Tia = 26 − 12 + 1 = {tia}th from the left", f"To her left: {tia} − 1 = {ans}"],
    why_others_wrong="Fifteen is her position from the left; Eleven counts the children to her right; Thirteen "
                     "subtracts one too many.", natural=by_num, seconds=35, verified_by=RECOMP)
S5 = ["Arya", "Bela", "Chhavi", "Dina", "Esha"]
conds = [("Arya scored more than Bela but less than Chhavi.", ("Arya", "Bela", "Chhavi"), lambda a, b, c: b < a < c),
         ("Dina scored less than Bela.", ("Dina", "Bela"), lambda d, b: d < b),
         ("Esha scored more than Chhavi.", ("Esha", "Chhavi"), lambda e, c: c < e)]
M5 = unique(S5, {p: range(1, 6) for p in S5}, conds, [S5])
ans = min(S5, key=M5.get)
assert ans == "Dina"
mcq(RNK, CHW, "Basic", "Five students Arya, Bela, Chhavi, Dina and Esha scored different marks in a test.\n"
    + bullets(conds) + "\n\nWho scored the lowest marks?", ans, ["Bela", "Arya", "Esha"], "Join the comparisons",
    "Esha > Chhavi > Arya > Bela > Dina. Dina scored the lowest.", ["Chhavi > Arya > Bela", "Bela > Dina",
                                                                  "Esha > Chhavi"],
    why_others_wrong="Bela is second lowest, Arya in the middle and Esha the highest.", seconds=35, verified_by=BRUTE)
B5_ = ["P", "Q", "R", "S", "T"]
conds = [("Box Q is heavier than only box R.", tuple(B5_), lambda *v: sum(1 for x in v if x < v[1]) == 1 and v[2] < v[1]),
         ("Box S is lighter than only box T.", tuple(B5_), lambda *v: sum(1 for x in v if x > v[3]) == 1 and v[4] > v[3])]
W5_ = unique(B5_, {p: range(1, 6) for p in B5_}, conds, [B5_])
ans = next(p for p in B5_ if W5_[p] == 3)
assert ans == "P"
mcq(RNK, CHW, "Basic", "Five boxes P, Q, R, S and T have different weights.\n" + bullets(conds) +
    "\n\nWhich box is exactly in the middle when the boxes are arranged by weight?", ans, ["Q", "S", "R"],
    "'Heavier than only one' = second lightest",
    "Q is heavier than R alone, so R is the lightest and Q second lightest. S is lighter than T alone, so T is the "
    "heaviest and S second heaviest. P is left for the middle place.",
    ["R lightest, Q 2nd lightest", "T heaviest, S 2nd heaviest", "Middle: P"],
    why_others_wrong="Q and S are the second lightest and second heaviest; R is the lightest.", seconds=40,
    verified_by=BRUTE)
left = [r for r in range(1, 26) if r % 2 == 0]
ans = len(left) - left.index(14)
assert (len(left), ans) == (12, 6)
mcq(RNK, POSR, "Basic", "Twenty-five students with roll numbers 1 to 25 sit in a row facing north, in order of roll "
    "number from the left end. All the students with odd roll numbers leave the row, and the others do not move "
    "relative to one another. What is the position of roll number 14 from the right end in the new row?", ORDN(ans),
    ["7th", "12th", "5th"], "Count only the students who remain",
    "The remaining students are roll numbers 2, 4, …, 24 — twelve students. Roll number 14 is 7th of them from the "
    "left, so it is 12 − 7 + 1 = 6th from the right.",
    ["Remaining: 2, 4, …, 24 (12 students)", "14 is 7th from the left", "From the right: 12 − 7 + 1 = 6th"],
    why_others_wrong="7th is its place from the left; 12th is the number of students left; 5th forgets the + 1.",
    natural=ord_key, seconds=50, verified_by=RECOMP)
ans = (18 - 4 + 1 - 3) * 25
assert ans == 300
mcq(RNK, POSR, "Basic", "Eighteen lamp posts stand in a straight row, 25 m apart from one another. What is the "
    "distance between the 3rd post from the left end and the 4th post from the right end?", f"{ans} m",
    ["325 m", "275 m", "350 m"], "Distance = number of gaps × gap length",
    "The 4th post from the right is 18 − 4 + 1 = 15th from the left. From the 3rd to the 15th post there are "
    f"15 − 3 = 12 gaps of 25 m: {ans} m.", ["4th from right = 15th from left", "Gaps = 15 − 3 = 12", "12 × 25 = 300 m"],
    why_others_wrong="325 m counts 13 gaps (posts, not spaces); 275 m counts 11; 350 m counts 14.",
    natural=lambda t: int(t.split()[0]), seconds=45, verified_by=RECOMP)

# ---- Advanced set (4): a row of unknown length
P4r = ["Arun", "Bela", "Chetan", "Dinesh"]
conds = [("Arun is 8th from the left end.", ("Arun",), lambda a: a == 8),
         ("Bela sits to the right of Arun, and exactly five persons sit between Arun and Bela.", ("Arun", "Bela"),
          lambda a, b: b - a == 6),
         ("Chetan sits third to the left of Bela.", ("Bela", "Chetan"), lambda b, c: c == b - 3),
         ("Exactly four persons sit between Chetan and Dinesh, and Dinesh sits to the right of Bela.",
          ("Bela", "Chetan", "Dinesh"), lambda b, c, d: abs(d - c) == 5 and d > b),
         ("Dinesh is 4th from the right end of the row.", ("Dinesh", "N"), lambda d, n: n - d + 1 == 4)]
ROW = unique(P4r + ["N"], {**{p: range(1, 41) for p in P4r}, "N": range(1, 41)}, conds, [P4r])
assert (ROW["Arun"], ROW["Bela"], ROW["Chetan"], ROW["Dinesh"], ROW["N"]) == (8, 14, 11, 16, 19)
sid = stimulus("puzzle", "A row of unknown length",
               "Some persons sit in a row, all facing north.\n\n" + bullets(conds),
               "From the left: Arun 8th, Bela 8 + 6 = 14th, Chetan 14 − 3 = 11th. Dinesh is five places from Chetan "
               "(6th or 16th) and to the right of Bela, so 16th; being 4th from the right, the row has 16 + 4 − 1 = 19 "
               "persons.")
RQ = lambda text, correct, wrongs, concept, expl, steps, **kw: mcq(RNK, POSR, "Advanced", text, correct, wrongs,
                                                                    concept, expl, steps, stimulus=sid,
                                                                    verified_by=BRUTE, **kw)
RQ("How many persons sit in the row?", str(ROW["N"]), ["18", "20", "22"], "Place everyone from the left end first",
   "Arun 8th, Bela 14th, Chetan 11th, Dinesh 16th from the left; Dinesh is 4th from the right, so the row has 16 + 4 − "
   "1 = 19 persons.", ["Arun 8, Bela 14, Chetan 11, Dinesh 16", "N = 16 + 4 − 1 = 19"], natural=int,
   why_others_wrong="18 and 20 drop or double the − 1; 22 places Dinesh on the wrong side of Chetan.", seconds=110)
ans = ROW["Dinesh"] - ROW["Arun"] - 1
RQ("How many persons sit between Arun and Dinesh?", num_word(ans), ["Six", "Eight", "Nine"], "Between = gap − 1",
   f"Arun is 8th and Dinesh 16th from the left: 16 − 8 − 1 = {ans} persons sit between them.",
   ["16 − 8 − 1 = 7"], natural=by_num, why_others_wrong="Eight forgets the − 1; Six subtracts one too many; Nine "
                                                        "counts both ends.", seconds=70)
ans = ROW["N"] - ROW["Chetan"] + 1
RQ("What is Chetan's position from the right end?", ORDN(ans), ["8th", "10th", "11th"],
   "Position from the other end = total − position + 1", f"Chetan is 11th from the left in a row of 19: 19 − 11 + 1 = "
                                                         f"{ans}th from the right.", ["19 − 11 + 1 = 9"],
   natural=ord_key, why_others_wrong="11th is his place from the left; 8th and 10th misuse the + 1.", seconds=70)
mid_ = (ROW["Arun"] + ROW["Dinesh"]) // 2
assert (ROW["Arun"] + ROW["Dinesh"]) % 2 == 0 and mid_ - 1 == ROW["Chetan"]
RQ("Esha sits exactly midway between Arun and Dinesh. Who sits immediately to the left of Esha?", "Chetan",
   ["Bela", "Arun", "Dinesh"], "Midway = average of the two positions",
   f"Arun is 8th and Dinesh 16th, so Esha is (8 + 16) ÷ 2 = {mid_}th from the left. The 11th place, immediately to "
   "her left, is Chetan's.", [f"Esha = (8 + 16) ÷ 2 = {mid_}th", "11th = Chetan"],
   why_others_wrong="Bela is two places to Esha's right; Arun and Dinesh are the two ends of the stretch.",
   seconds=80)

# ================================================================================================ INPUT-OUTPUT (B3, I7, A1)
# ---- Basic set (3): second letter in alphabetical order, to the right end
INP = "drum flute horn piano tabla veena guitar".split()
assert len({w[1] for w in INP}) == 7
st = run_select(INP, key=lambda w: w[1], side="right")
assert st[-1] == ["guitar", "drum", "horn", "flute", "piano", "veena", "tabla"]
sid = stimulus("passage", "Machine: second letters to the right",
               "A word arrangement machine rearranges a line of words step by step. In each step it takes, among the "
               "words not yet arranged, the word whose SECOND letter comes earliest in the alphabet, and places it at "
               "the right end, immediately to the left of the words already arranged there (in Step I, at the extreme "
               "right). The other words keep their order. A step that would not change the line is not counted, and "
               "the machine stops when the arrangement is complete.\n\nInput: " + line(INP),
               "Second letters: drum r, flute l, horn o, piano i, tabla a, veena e, guitar u. Order of selection: "
               "tabla, veena, piano, flute, horn, drum, guitar.\n\n" + "\n".join(step_txt(st)))
IQ = lambda text, correct, wrongs, concept, expl, steps, **kw: mcq(
    IOT, WR, "Basic", text, correct, wrongs, concept, expl, steps, stimulus=sid, verified_by=RECOMP, **kw)
IQ("Which of the following is Step II?", line(st[1]), [line(st[0]), line(st[2]), line(st[1][::-1])],
   "Look at the second letter, not the first", steps_join(st[:2]), step_txt(st[:2]),
   why_others_wrong="The first two wrong lines are Steps I and III; the last is Step II written backwards.", seconds=50)
assert next(i for i, s_ in enumerate(st) if s_[0] == "guitar") == len(st) - 1
IQ("Counting only the steps that change the line, after how many steps does 'guitar' first stand at the extreme left of the line?", num_word(len(st)),
   [num_word(len(st) + 1), num_word(len(st) - 1), num_word(len(st) + 2)], "Stop when the line is final",
   steps_join(st) + f" After Step {ROMAN[len(st) - 1]} the arrangement is complete.", step_txt(st), natural=by_num,
   seconds=55)
s3 = st[2]
ans = s3[2]
IQ("In Step III, which word is 3rd from the left end?", ans, [x for x in near(s3, 2)], "Read the step, then count",
   f"Step III: {line(s3)}. The 3rd word from the left is '{ans}'.", [f"Step III: {line(s3)}"], seconds=45)

# ---- Intermediate set A (4): every number changes in every step, then the line rotates
INP = [36, 15, 48, 27, 64, 9]


def tick(seq):
    new = [n + 3 if n % 2 else n // 2 for n in seq]
    return new[1:] + new[:1]


st, cur = [], INP
for _ in range(4):
    cur = tick(cur)
    st.append(cur)
sid = stimulus("passage", "Machine: halve or add three, then rotate",
               "A number machine changes a line of numbers step by step. In each step it first replaces every number: "
               "an odd number by that number plus 3, and an even number by half of it. It then moves the number at the "
               "left end of the line to the right end; the other numbers keep their order. The machine runs for four "
               "steps.\n\nInput: " + line(INP), "\n".join(step_txt(st)))
IQ = lambda text, correct, wrongs, concept, expl, steps, **kw: mcq(
    IOT, NR, "Intermediate", text, correct, wrongs, concept, expl, steps, stimulus=sid, verified_by=RECOMP, **kw)
no_rot = [n + 3 if n % 2 else n // 2 for n in [n + 3 if n % 2 else n // 2 for n in INP]]
IQ("Which of the following is Step II?", line(st[1]), [line(st[0]), line(st[2]), line(no_rot)],
   "Change every number, then rotate", steps_join(st[:2]), step_txt(st[:2]),
   why_others_wrong="The first two wrong lines are Steps I and III; the last applies the number rule twice but never "
                    "rotates the line.", seconds=75)
ans = sum(st[2])
IQ("What is the sum of the numbers in Step III?", str(ans), [str(sum(st[1])), str(sum(st[3])), str(ans + 3)],
   "Rotation does not change the sum", f"Step III: {line(st[2])}. Sum = {ans}.", step_txt(st[:3]), natural=int,
   seconds=75)
ans = sum(1 for n in st[3] if n % 2)
IQ("After the numbers are changed and rotated in Step IV, how many of them are odd?", num_word(ans),
   [num_word(k) for k in (ans - 1, ans + 1, ans + 2) if k >= 0][:3] if ans >= 1 else ["One", "Three", "Four"],
   "Check the parity after the last change", f"Step IV: {line(st[3])}. Odd numbers: "
                                             + ", ".join(str(n) for n in st[3] if n % 2) + f" — {num_word(ans).lower()}.",
   [f"Step IV: {line(st[3])}"], natural=by_num, seconds=70)
ans = st[3][1]
IQ("In Step IV, which number is 2nd from the left end?", str(ans), [str(x) for x in near(st[3], 1)],
   "Read the step, then count", f"Step IV: {line(st[3])}. The 2nd from the left is {ans}.", step_txt(st), seconds=70)

# ---- Intermediate set B (3): alternate moves — a word in odd steps, a number in even steps
INP = [81, "lime", "jade", 52, "mint", 37, "rose", 46]


def alt010(items):
    ws, ns = [x for x in items if isinstance(x, str)], [x for x in items if isinstance(x, int)]
    left, right, steps, cur, k = [], [], [], list(items), 0
    while ws or ns:
        if k % 2 == 0:
            w = max(ws)
            ws.remove(w)
            left.append(w)
        else:
            n = min(ns)
            ns.remove(n)
            right.insert(0, int(str(n)[::-1]))
        mid = [x for x in items if x in ws or x in ns]
        new = left + mid + right
        assert new != cur, ("no change", k)
        cur, k = new, k + 1
        steps.append(cur)
    return steps


st = alt010(INP)
assert len(st) == 8 and not {73, 64, 25, 18} & {81, 52, 37, 46}
sid = stimulus("passage", "Machine: words and numbers in turn",
               "A word and number arrangement machine rearranges a line step by step, moving one element per step. In "
               "Steps I, III, V, … it takes, among the words not yet arranged, the word that comes last in alphabetical "
               "order and places it at the left end, immediately to the right of the words already placed there. In "
               "Steps II, IV, VI, … it takes the smallest number not yet arranged, reverses its digits, and places the "
               "result at the right end, immediately to the left of the numbers already placed there. All other "
               "elements keep their order. The machine stops when every element has been arranged.\n\nInput: "
               + line(INP), "Words in order: rose, mint, lime, jade. Numbers in order: 37 → 73, 46 → 64, 52 → 25, "
                            "81 → 18.\n\n" + "\n".join(step_txt(st)))
IQ = lambda text, correct, wrongs, concept, expl, steps, **kw: mcq(
    IOT, MM, "Intermediate", text, correct, wrongs, concept, expl, steps, stimulus=sid, verified_by=RECOMP, **kw)
IQ("Which of the following is Step IV?", line(st[3]), [line(st[2]), line(st[4]),
                                                      line(st[3][:-2] + [46, 37])],
   "One element per step, words and numbers in turn", steps_join(st[:4]), step_txt(st[:4]),
   why_others_wrong="The first two wrong lines are Steps III and V; the last forgets to reverse the placed numbers.",
   seconds=80)
first = next(i for i, s_ in enumerate(st) if 25 in s_)
IQ("In which step is '25' placed on the right side of the line?", f"Step {ROMAN[first]}",
   [f"Step {ROMAN[i]}" for i in (first - 1, first + 1, first - 2)], "Numbers move only in even steps",
   "52 is the third smallest number, and numbers move in Steps II, IV and VI, so 52 becomes 25 in Step VI.",
   step_txt(st[:first + 1]), natural=step_key, seconds=70)
fin = st[-1]
ans = fin[-3]
IQ("In the last step, which element is 3rd from the right end?", str(ans), [str(x) for x in near(fin, len(fin) - 3)],
   "Numbers are stacked from the right in order of selection", f"Last step: {line(fin)}. The 3rd from the right is "
                                                                f"{ans}.", [f"Last step: {line(fin)}"], seconds=60)

# ---- Advanced standalone: remainders and quotients by 7; words in capitals
INP = ["pearl", 45, "coral", 30, "amber", 61, "topaz", 20]


def adv010(items):
    ws, ns = [x for x in items if isinstance(x, str)], [x for x in items if isinstance(x, int)]
    left, right, steps, cur = [], [], [], list(items)
    while ws or ns:
        if ns:
            n = min(ns, key=lambda v: (v % 7, v))
            ns.remove(n)
            left.append(n // 7)
        if ws:
            w = max(ws)
            ws.remove(w)
            right.insert(0, w.upper())
        mid = [x for x in items if x in ws or x in ns]
        new = left + mid + right
        assert new != cur
        cur = new
        steps.append(cur)
    return steps


assert len({n % 7 for n in INP if isinstance(n, int)}) == 4
st = adv010(INP)
s3 = st[2]
ans = sum(x for x in s3 if isinstance(x, int))
assert len(st) == 4
mcq(IOT, MM, "Advanced",
    "A word and number arrangement machine rearranges a line step by step. In each step it makes two moves: (1) among "
    "the numbers not yet arranged, it takes the one that leaves the smallest remainder when divided by 7, replaces it "
    "by the quotient of that division, and places the quotient at the left end, immediately to the right of the "
    "quotients already placed there; (2) among the words not yet arranged, it takes the one that comes last in "
    "alphabetical order, writes it in capital letters, and places it at the right end, immediately to the left of the "
    "words already placed there. All other elements keep their order.\n\nInput: " + line(INP) +
    "\n\nWhat is the sum of all the numbers in Step III?", str(ans),
    [str(sum(x for x in st[1] if isinstance(x, int))), str(sum(x for x in INP if isinstance(x, int)) // 7),
     str(ans + 3)],
    "Track which numbers are still unchanged in the step",
    "Remainders on division by 7: 30 → 2, 45 → 3, 61 → 5, 20 → 6, so the numbers are taken in the order 30, 45, 61, "
    "20 and become 4, 6, 8, 2. Words from last alphabetically: topaz, pearl, coral, amber. " + steps_join(st[:3]) + f" Sum of the numbers in Step III = {ans}.", step_txt(st[:3]),
    natural=int, seconds=110, verified_by=RECOMP)

# ================================================================================================ ASSUMPTIONS (B5, A5)
asm("Basic", "Notice in a public park: \"Keep the park clean. Use the dustbins.\"",
    "There are dustbins in the park.", "Some visitors may litter the park if they are not reminded.", A_B,
    "Visitors are told to use the dustbins, so the notice takes for granted that dustbins are there (I). A reminder "
    "to keep the park clean is put up only if littering is expected otherwise (II).",
    ["Instruction to use dustbins ⇒ dustbins exist: I", "Reminder ⇒ littering is possible: II"],
    "Each 'Only' option drops one of two things the notice rests on.", seconds=30)
asm("Basic", "Railway announcement: \"Book your tickets early — seats fill up fast during the holidays.\"",
    "Many people travel by train during the holidays.", "Train fares are lower during the holidays.", A_I,
    "Seats fill up fast only if many people travel then (I). The announcement says nothing about fares, so II is not "
    "implicit.", ["Seats fill fast ⇒ heavy holiday travel: I", "Fares not mentioned ⇒ II not implicit"],
    "Only II and Both accept a claim about fares; Neither ignores the reason given for booking early.", seconds=30)
asm("Basic", "Advertisement: \"Wanted: a driver who can also speak English, for a travel company.\"",
    "Every driver in the city speaks English.", "Some drivers are able to speak English.", A_II,
    "The company asks for an English-speaking driver because it expects some drivers to have that skill (II). If "
    "every driver spoke English, there would be no need to mention it, so I is not assumed.",
    ["Asking for a skill ⇒ some candidates have it: II", "Mentioning it ⇒ not everyone has it ⇒ I not implicit"],
    "Only I and Both accept a claim that would make the requirement pointless; Neither misses the basis of the "
    "advertisement.", seconds=35)
asm("Basic", "Notice from a school: \"The school will remain closed on Monday on account of the local festival.\"",
    "Every student of the school celebrates the festival.", "The school will remain closed on Tuesday too.", A_N,
    "A holiday for a local festival does not need every student to celebrate it ('every' is too strong), and the "
    "notice speaks only of Monday, so nothing is assumed about Tuesday.",
    ["'Every student' is an extreme claim ⇒ I not implicit", "Only Monday is mentioned ⇒ II not implicit"],
    "Each other option accepts a claim that the notice does not depend on.", seconds=30)
asm("Basic", "Road-safety poster: \"Wear a helmet — it can save your life.\"",
    "Wearing a helmet can reduce the risk of a fatal head injury in an accident.",
    "People who see the poster may follow its advice.", A_B,
    "The poster says a helmet can save a life, which assumes it reduces the risk of fatal injuries (I). A poster is "
    "put up only if people are expected to notice it and act on it (II).",
    ["Claim on the poster ⇒ helmets protect: I", "Purpose of a poster ⇒ people may act on it: II"],
    "Each 'Only' option drops one of two things every advisory poster rests on.", seconds=30)
asm("Advanced", "\"Every employee will get a bonus of one month's salary if the company's profit this year crosses "
    "₹100 crore,\" announced the company's chief executive.",
    "It is possible for the company's profit to cross ₹100 crore this year.",
    "Employees will not work at all unless they are promised a bonus.", A_I,
    "A conditional bonus is announced only if the condition can be met (I). The offer may be meant to encourage "
    "employees, but it does not assume that they would stop working altogether without it (II is extreme).",
    ["Promise tied to a target ⇒ the target is reachable: I", "'Not work at all' is an extreme claim ⇒ II not "
                                                                "implicit"],
    "Only II and Both accept an extreme claim; Neither ignores that the target must be reachable.", seconds=50)
asm("Advanced", "A bank has cut its home-loan interest rate by 0.25 percentage point to attract new borrowers.",
    "Some borrowers choose a lender partly on the basis of the interest rate it charges.",
    "Other banks will not cut their home-loan rates.", A_I,
    "A rate cut can attract borrowers only if borrowers care about the rate (I). The bank may expect rivals to "
    "follow; its move does not depend on their keeping their rates unchanged (II).",
    ["Rate cut to attract borrowers ⇒ borrowers compare rates: I", "Rivals' reaction is not part of the plan ⇒ II "
                                                                     "not implicit"],
    "Only II and Both assume something about other banks that the decision does not need; Neither ignores why a "
    "rate cut would attract anyone.", seconds=50)
asm("Advanced", "Order of the district collector: \"In view of the heavy-rain forecast for tomorrow, all schools in "
    "the district will remain closed tomorrow.\"",
    "The forecast of heavy rain for tomorrow will certainly come true.",
    "Heavy rain could make it unsafe for children to travel to and from school.", A_II,
    "Schools are closed because heavy rain could endanger children on their way (II). Acting on a forecast as a "
    "precaution does not require being certain that it will come true, so I ('certainly') is not assumed.",
    ["Closure for safety ⇒ rain can make travel unsafe: II", "Precaution, not certainty ⇒ I not implicit"],
    "Only I and Both treat a precaution as a certainty; Neither misses the safety reason for the closure.",
    seconds=55)
asm("Advanced", "The state government will give free bicycles to all girls who join Class 9 in government schools.",
    "Every girl in the state already owns a bicycle.",
    "Boys in government schools do not need to travel to school.", A_N,
    "If every girl already owned a bicycle, giving free bicycles would be pointless, so I goes against the scheme. "
    "The scheme is aimed at girls, but it does not assume that boys never need to travel to school (II).",
    ["I contradicts the purpose of the scheme", "Targeting girls does not imply boys need no transport ⇒ II not "
                                               "implicit"],
    "Each other option accepts a claim that contradicts the scheme or reads too much into its target group.",
    seconds=50)
asm("Advanced", "Notice from a company: \"Employees may work from home on Fridays, provided their work does not "
    "suffer.\"", "Employees will finish all their weekly work by Thursday.",
    "Some employees' work can be done from home.", A_II,
    "Allowing work from home makes sense only if at least some work can be done from home (II). The notice allows "
    "work on Fridays, from home; it does not assume that all the week's work is done by Thursday (I).",
    ["Permission to work from home ⇒ some work is possible from home: II", "Friday is still a working day ⇒ I not "
                                                                            "implicit"],
    "Only I and Both treat Friday as a day without work; Neither ignores what the permission needs.", seconds=50)

# ================================================================================================ CONCLUSIONS (I6, A1)
both_ = [b for b in range(6) if 3 + 3 - b == 5]
assert both_ == [1]
scq("Intermediate", VC, "Each of the five trainees in a batch passed at least one of two tests, Hindi and English. "
    "Exactly three of them passed the Hindi test, and exactly three passed the English test.",
    "At least one trainee passed both tests.", "Exactly one trainee passed both tests.", BOTH,
    "Passing counts add up to 3 + 3 = 6 for 5 trainees who each passed at least one test, so exactly 6 − 5 = 1 "
    "trainee was counted twice, that is, passed both. 'Exactly one' (II) and therefore 'at least one' (I) both "
    "follow.", ["3 + 3 − both = 5 ⇒ both = 1", "⇒ II, and hence I"],
    "Each 'Only' option drops one of two consequences of the same count.", seconds=55)
assert 4 * 5 == 20 and 12 * 60 // 5 == 144
scq("Intermediate", INF, "A clock gains exactly 5 minutes every hour. It was set to the correct time at 8:00 am "
    "today.", "When the correct time is 12:00 noon today, the clock shows 12:20 pm.",
    "The clock will show the correct time again later today.", ONLY_I,
    "In 4 hours the clock gains 4 × 5 = 20 minutes, so at noon it shows 12:20 pm (I). To show the correct time again "
    "it must gain a full 12 hours (720 minutes), which takes 720 ÷ 5 = 144 hours — not today (II is false).",
    ["Gain by noon: 4 × 5 = 20 min ⇒ I", "Gain needed: 720 min ⇒ 144 hours ⇒ II false"],
    "Only II and Both accept a conclusion the rate rules out; Neither ignores the direct calculation.", seconds=60)
scq("Intermediate", VC, "Bina is the only sister of Ankit's father.", "Bina is Ankit's aunt.",
    "Ankit's father has no brother.", ONLY_I,
    "The sister of one's father is one's aunt, so I follows. Being the only sister means Ankit's father has no other "
    "sister; it says nothing about brothers, so II does not follow.",
    ["Father's sister = aunt ⇒ I", "'Only sister' says nothing about brothers ⇒ II does not follow"],
    "Only II and Both read 'only sister' as 'only sibling'; Neither misses the direct relation.", seconds=40)
scq("Intermediate", INF, "The company's revenue this year was the highest in its history.",
    "The company made a profit this year.", "The company's revenue will be higher next year.", NEITHER,
    "Revenue is what the company earned from sales; profit also depends on its costs, which are not given, so I does "
    "not follow. A record this year says nothing certain about next year, so II does not follow.",
    ["Revenue ≠ profit ⇒ I does not follow", "No information about next year ⇒ II does not follow"],
    "Each other option treats record revenue as if it guaranteed profit or future growth.", seconds=40)
scq("Intermediate", INF, "A club has 60 members. 25 of them play tennis, and every member who plays tennis also "
    "swims. 20 members neither play tennis nor swim.", "More members of the club play tennis than swim.",
    "Exactly 15 members of the club swim but do not play tennis.", ONLY_II,
    "The 40 members who do something all swim (tennis players swim too, and the rest of the 40 must swim). So 40 "
    "swim, of whom 25 also play tennis: 40 − 25 = 15 swim without playing tennis (II). Since 40 swim and 25 play "
    "tennis, I is false.", ["Swimmers = 60 − 20 = 40", "Swim only = 40 − 25 = 15 ⇒ II", "40 > 25 ⇒ I false"],
    "Only I and Both reverse the comparison; Neither ignores the direct count.", seconds=60)
scq("Intermediate", INF, "The bus fare from a village to the town is ₹30 per passenger. An auto-rickshaw makes the "
    "same trip for ₹90, whether it carries one, two or three passengers.",
    "For three people travelling together, the auto-rickshaw costs the same as the bus.",
    "For two people travelling together, the bus is cheaper than the auto-rickshaw.", BOTH,
    "Three people pay 3 × ₹30 = ₹90 by bus, the same as the auto-rickshaw (I). Two people pay ₹60 by bus, less than "
    "₹90 (II).", ["3 × 30 = 90 = 90 ⇒ I", "2 × 30 = 60 < 90 ⇒ II"],
    "Each 'Only' option drops one of two direct comparisons.", seconds=40)
scq("Advanced", VC, "Some of the bank's branches open on Sundays. Every branch of the bank that opens on Sundays has "
    "a cash-deposit machine.", "Some of the bank's branches that have a cash-deposit machine open on Sundays.",
    "Every branch of the bank that has a cash-deposit machine opens on Sundays.", ONLY_I,
    "The branches that open on Sundays exist and all have cash-deposit machines, so some branches with machines open "
    "on Sundays (I). 'Every Sunday branch has a machine' cannot be reversed: branches with machines may also be "
    "closed on Sundays, so II does not follow.",
    ["Some branches open on Sundays; all of them have machines ⇒ I", "Converse of an 'every' statement ⇒ II does not "
                                                                       "follow"],
    "Only II and Both reverse the 'every' statement; Neither misses the 'some' conclusion.", seconds=55)

# ================================================================================================ CRITICAL REASONING (B4, I2, A7)
crq("Basic", SW_, "Claim: Keeping the school library open during the lunch break will increase the number of books "
    "that students borrow.\n\nWhich of the following, if true, most strengthens the claim?",
    "At present the library is open only during class hours, when most students cannot visit it",
    ["The library has more than 5,000 books", "The lunch break lasts 40 minutes",
     "Some students bring their own books to school"], "Strengthen: show that access is the obstacle now",
    "If students borrow few books because the library is open only when they are in class, opening it at lunch "
    "removes that obstacle, so more books are likely to be borrowed.",
    ["Claim: more opening time ⇒ more borrowing", "Strengthener: students cannot visit at present"],
    "The size of the collection and the length of the break do not show that students will come; students with "
    "their own books are, if anything, less likely to borrow.", seconds=35)
assert 300 * 10 // 4 == 750
crq("Basic", INFP, "Passage: A recipe that serves 4 people needs 300 g of rice. Neha is making the same recipe for 10 "
    "people, using rice in the same proportion.\n\nWhich of the following can be inferred?",
    "Neha needs 750 g of rice", ["Neha needs 600 g of rice", "Neha needs 1,200 g of rice",
                                 "Neha needs 3 kg of rice"], "Scale in proportion to the number of people",
    "Rice per person = 300 ÷ 4 = 75 g, so 10 people need 75 × 10 = 750 g.", ["300 ÷ 4 = 75 g per person",
                                                                           "75 × 10 = 750 g"],
    "600 g doubles the recipe; 1,200 g quadruples it; 3 kg multiplies by ten instead of by 10 ÷ 4.", seconds=35)
crq("Basic", CA_, "Statement: Several elderly residents of a housing society have slipped and fallen on the "
    "society's staircase, whose steps are worn smooth and have no handrail.\n\nWhich of the following is the most "
    "appropriate course of action?", "Fit handrails and anti-slip strips on the staircase",
    ["Ask the elderly residents to stay indoors", "Close the staircase permanently",
     "Stop visitors from using the staircase"], "Remove the cause of the falls",
    "The falls are caused by smooth steps with nothing to hold. Handrails and anti-slip strips fix both causes.",
    ["Cause: smooth steps, no handrail", "Remedy: anti-slip strips + handrails"],
    "Keeping residents indoors or closing the staircase is impractical; stopping visitors does not make the steps "
    "safer.", seconds=30)
crq("Basic", SW_, "Claim: A café's new menu is popular with its customers, because the café's sales rose by 40% in "
    "the first week after the new menu was introduced.\n\nWhich of the following, if true, most weakens the claim?",
    "During that first week, the café gave a 50% discount on every item to celebrate the new menu",
    ["The new menu has more vegetarian dishes than the old one", "The café is located near a college",
     "The café's owner designed the new menu herself"], "Weaken: give another reason for the rise",
    "A half-price offer in the same week could explain the jump in sales by itself, so the rise does not show that "
    "customers like the new menu.", ["Evidence: sales up 40% in week 1", "Weakener: 50% discount in the same week"],
    "The kind of dishes, the location and who designed the menu do not explain a sudden one-week rise.", seconds=35)
crq("Intermediate", CA_, "Statement: Many small traders in a town are losing sales because they accept only cash, "
    "while more and more customers want to pay digitally.\n\nWhich of the following is the most appropriate course "
    "of action?", "Help the traders open free QR-code payment accounts with their banks and show them how to use them",
    ["Ban digital payments in the town", "Ask customers to carry more cash",
     "Close the shops that accept only cash"], "Enable the traders rather than restrict the customers",
    "Traders lose sales because they cannot accept digital payments. Helping them start accepting such payments "
    "removes the problem.", ["Problem: cash-only traders lose customers", "Remedy: enable digital payments"],
    "Banning digital payments or telling customers to carry cash goes against what customers want; closing shops "
    "punishes the traders.", seconds=45)
fam = sum(0 if (a < 12 or a > 60) else 50 for a in (65, 38, 36, 12, 8))
assert fam == 150
crq("Intermediate", INFP, "Passage: A museum gives free entry to children under 12 years of age and to people over "
    "60. All other visitors pay ₹50 each. On Sunday, a family visited the museum: a grandmother aged 65, two parents "
    "aged 38 and 36, and two children aged 12 and 8.\n\nWhich of the following can be inferred?",
    "The family paid ₹150 in all for entry", ["The family paid ₹100 in all for entry",
                                             "The family paid ₹200 in all for entry",
                                             "The family paid ₹250 in all for entry"],
    "Apply each condition exactly",
    "The grandmother (over 60) and the 8-year-old (under 12) enter free. The two parents and the 12-year-old (who is "
    "not under 12) pay ₹50 each: ₹150.", ["Free: 65-year-old, 8-year-old", "Pay: 38, 36 and 12 ⇒ 3 × ₹50 = ₹150"],
    "₹100 treats the 12-year-old as under 12; ₹200 charges the grandmother or the younger child; ₹250 charges "
    "everyone.", seconds=50)
crq("Advanced", SW_, "Argument: Countries with more mobile phones per person have higher average incomes. So giving "
    "free mobile phones to families in the state's poorest districts will raise their incomes.\n\nWhich of the "
    "following, if true, most seriously weakens the argument?",
    "A trial last year that gave free phones to 10,000 families in two of the poorest districts found no change in "
    "their incomes after a year, compared with similar families who did not get phones",
    ["Mobile phones have become cheaper in recent years", "Most people in the poorest districts work in farming",
     "Several companies sell mobile phones in the state"], "Weaken: direct evidence against the predicted effect",
    "The argument predicts that free phones will raise incomes. A controlled trial in the same kind of districts found "
    "no effect, which directly undercuts the prediction drawn from a country-level link.",
    ["Prediction: free phones ⇒ higher incomes", "Weakener: trial shows no effect"],
    "Cheaper phones, the main occupation and the number of sellers do not show whether phones raise incomes.",
    seconds=70)
crq("Advanced", SW_, "Argument: The hospital's new rule that doctors must wash their hands before examining each "
    "patient is the reason infections among its patients fell by 30% this year.\n\nWhich of the following, if true, "
    "most strengthens the argument?",
    "The hospital made no other change this year in its cleaning, staffing or kinds of patients, and similar "
    "hospitals without the rule saw no fall in infections",
    ["Hand-washing takes doctors less than a minute", "The hospital has 400 beds",
     "Doctors at the hospital agreed with the new rule"], "Strengthen: rule out other explanations",
    "If nothing else changed at the hospital and comparable hospitals without the rule saw no fall, the new rule is "
    "the most likely reason for the drop in infections.",
    ["Claim: rule ⇒ fewer infections", "Strengthener: no other change; no fall elsewhere"],
    "The time hand-washing takes, the hospital's size and doctors' agreement do not link the rule to the fall.",
    seconds=70)
LEC = ["Economics", "History", "Law", "Maths", "Physics"]
sch = [dict(zip(LEC, p)) for p in itertools.permutations(range(1, 6))
       if p[3] == 3 and p[2] == p[1] + 1 and p[4] < p[0]]
assert len(sch) == 2 and all(m["Economics"] == m["Physics"] + 1 for m in sch)
assert not all(m["History"] == 1 for m in sch) and not all(m["Economics"] == 5 for m in sch)
assert not all(m["Law"] < m["Maths"] for m in sch)
crq("Advanced", INFP, "Passage: Five lectures — on Economics, History, Law, Maths and Physics — are held one after "
    "another on a day. Law is held immediately after History. Maths is the third lecture. Physics is held at some "
    "time before Economics.\n\nWhich of the following must be true?",
    "Physics is held immediately before Economics",
    ["History is the first lecture", "Economics is the last lecture", "Law is held before Maths"],
    "Find every arrangement, then pick what holds in all",
    "History–Law must take places 1–2 or 4–5 (Maths is 3rd). If they are 1–2, Physics and Economics are 4th and 5th; "
    "if they are 4–5, Physics and Economics are 1st and 2nd. In both cases Physics comes immediately before Economics.",
    ["Case 1: History, Law, Maths, Physics, Economics", "Case 2: Physics, Economics, Maths, History, Law",
     "Common to both: Physics just before Economics"],
    "Each of the other options holds in only one of the two possible orders.", seconds=90)
crq("Advanced", CA_, "Statement: A survey found that the city's buses run almost empty between 11 am and 4 pm but "
    "are badly overcrowded during the morning and evening peak hours.\n\nWhich of the following is the most "
    "appropriate course of action?",
    "Shift some buses from the afternoon schedule to the peak hours, and offer lower fares in the afternoon",
    ["Stop all bus services between 11 am and 4 pm", "Buy enough new buses to double the fleet at once",
     "Raise fares sharply during peak hours to keep people off the buses"],
    "Match supply to demand at low cost",
    "Buses are idle in the afternoon and short at peak hours. Moving buses to the peak hours uses the existing fleet "
    "better, and cheaper afternoon fares can draw some travellers away from the peaks.",
    ["Problem: mismatch between bus supply and demand", "Remedy: reschedule buses + off-peak fares"],
    "Stopping afternoon buses strands those who travel then; doubling the fleet is costly and leaves more empty "
    "buses; sharp peak fares penalise people who must travel at those hours.", seconds=70)
crq("Advanced", SW_, "Argument: Patients who choose Dr Mehta for knee surgery recover faster than the patients of the "
    "other knee surgeons at the hospital. So Dr Mehta is the hospital's best knee surgeon.\n\nWhich of the following, "
    "if true, most seriously weakens the argument?",
    "Dr Mehta operates mostly on young athletes with minor injuries, while the other surgeons treat most of the "
    "elderly patients with severe knee damage", ["Dr Mehta has worked at the hospital for ten years",
                                                 "The hospital has four knee surgeons",
                                                 "Dr Mehta's patients pay the same fees as other patients"],
    "Weaken: the groups being compared differ",
    "Young patients with minor injuries recover faster whoever operates on them. If Dr Mehta's patients are mostly "
    "such cases, their faster recovery does not show that he is the best surgeon.",
    ["Evidence: faster recovery of Dr Mehta's patients", "Weakener: his patients are easier cases"],
    "Years of service, the number of surgeons and fees do not explain the difference in recovery.", seconds=70)
avg = (20 * 60 + 30 * 70) / 50
assert avg == 66
crq("Advanced", INFP, "Passage: In a class, the average mark of the 20 boys is 60, and the average mark of the 30 "
    "girls is 70. There are no other students in the class.\n\nWhich of the following must be true?",
    "The average mark of the whole class is 66", ["The average mark of the whole class is 65",
                                                  "At least one girl scored more than 70",
                                                  "Every girl scored more than every boy"],
    "A combined average is weighted by group size",
    "Total marks = 20 × 60 + 30 × 70 = 1,200 + 2,100 = 3,300 for 50 students: average 66.",
    ["Total = 1,200 + 2,100 = 3,300", "Average = 3,300 ÷ 50 = 66"],
    "65 averages the two averages without weighting; every girl could have scored exactly 70; averages say nothing "
    "about every individual.", seconds=70)
crq("Advanced", CA_, "Statement: An audit found that the city's government hospitals often run out of essential "
    "medicines because each hospital places its own orders late and in small quantities.\n\nWhich of the following "
    "is the most appropriate course of action?",
    "Set up a central system that tracks every hospital's stock and places orders automatically before stocks run "
    "low", ["Stop giving free medicines at the hospitals", "Ask patients to bring their own medicines",
            "Order a five-year stock of every medicine at once"], "Fix the ordering process that causes the shortage",
    "Shortages come from late, small orders by each hospital. Central tracking with automatic reordering keeps stocks "
    "up without the waste of huge one-time purchases.",
    ["Cause: late, small orders", "Remedy: central tracking + automatic reordering"],
    "Stopping free medicines or shifting the burden to patients defeats the purpose of the hospitals; a five-year "
    "stock would expire and waste money.", seconds=60)


# ################################################################################################ BLIND CHECK + WRITE
# Blind check (2026-11-06): three fresh solvers answered all 111 hand-written items from a key-free dump. 105 matched
# with high confidence. Five items were then revised (BANK_REAS_001402, 001592, 001785, 001789, 001976: a wrong option
# that was also true, a cause-effect pair open to a direct link, missing timing, a borderline assumption) and a fourth
# fresh solver re-answered them blind, matching every key with high confidence. BANK_REAS_001583 matched the key but
# was flagged as a strict-reading trap ('only X are eligible'), so it keeps ai:self-recheck.
BLIND_OK = set(VERBAL_IDS) - {"BANK_REAS_001583"}

ALLQ = [x for b_ in B.values() for x in b_["Q"]]
if "--dump-blind" in sys.argv:  # key-free dump of every hand-written item for the blind solvers
    out_ = [{"id": x["question_id"], "text": x["question_text"], "options": x["options"]} for x in ALLQ
            if x["question_id"] in VERBAL_IDS]
    Path(sys.argv[sys.argv.index("--dump-blind") + 1]).write_text(json.dumps(out_, indent=1, ensure_ascii=False),
                                                                   encoding="utf-8")
    print("dumped", len(out_))

CHECK = "--draft" not in sys.argv
assert set(B) == set(PKG["batches"]), sorted(B)
for b_, spec in PKG["batches"].items():
    Q_, S_ = B[b_]["Q"], B[b_]["S"]
    have = Counter((x["topic"], x["difficulty"]) for x in Q_)
    for t in spec["topics"]:
        for d_, n_ in t["quota"].items():
            if CHECK:
                assert have[(t["topic"], d_)] == n_, (b_, t["topic"], d_, have[(t["topic"], d_)], n_)
            elif have[(t["topic"], d_)] != n_:
                print("quota", b_, t["topic"], d_, have[(t["topic"], d_)], "/", n_)
        assert all(x["subtopic"] in t["subtopics"] for x in Q_ if x["topic"] == t["topic"]), (b_, t["topic"])
    assert all(x["topic"] in {t["topic"] for t in spec["topics"]} for x in Q_), b_
    if CHECK:
        assert len(Q_) == spec["count"], (b_, len(Q_))
        assert Counter(x["difficulty"] for x in Q_) == Counter(spec["by_difficulty"]), b_
        assert Q_[0]["question_id"] == spec["question_ids"][0] and Q_[-1]["question_id"] == spec["question_ids"][1]
        assert max(B[b_]["K"].values()) - min(B[b_]["K"].values()) <= 4, (b_, B[b_]["K"])
    if S_:
        assert S_[0]["stimulus_id"] == spec["stimulus_id_start"], b_
    for st_ in S_:
        mem = [x for x in Q_ if x.get("stimulus_id") == st_["stimulus_id"]]
        assert 3 <= len(mem) <= 6, (st_["stimulus_id"], len(mem))
        assert len({x["difficulty"] for x in mem}) == 1 and len({x["topic"] for x in mem}) == 1, st_["stimulus_id"]
assert len(ALLQ) == PKG["total"] or not CHECK
assert BLIND_OK <= set(VERBAL_IDS)
for x in ALLQ:
    if x["question_id"] in BLIND_OK:
        x["verification"]["verified_by"] = list(HAND)
for b_ in sorted(B):
    print(b_, len(B[b_]["Q"]), "questions,", len(B[b_]["S"]), "stimuli, keys", dict(sorted(B[b_]["K"].items())))
print(f"verbal {len(VERBAL_IDS)}, blind-matched {len(BLIND_OK)}")
if CHECK:
    for b_, spec in PKG["batches"].items():
        doc = {
            "schema_version": "1.0",
            "batch_id": spec["batch_id"],
            "created_at": TODAY,
            "notes": (f"Reasoning Ability topic package 4 for {spec['batch_id']}: {spec['count']} original questions on "
                      "ranking, input-output, data sufficiency, assumptions, conclusions, cause and effect and critical "
                      "reasoning, built by tools/packages/REAS_pkg4.py. Ranking positions and input-output machines "
                      "are recomputed in code, comparison puzzles brute-forced for a unique order, and data "
                      "sufficiency checked by enumerating models for each statement subset. Verbal items are "
                      "hand-written and were re-answered blind by separate fresh solvers. All questions await human "
                      "review."),
            "stimuli": B[b_]["S"],
            "questions": B[b_]["Q"],
        }
        out = ROOT / spec["output"]
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print("wrote", out)
