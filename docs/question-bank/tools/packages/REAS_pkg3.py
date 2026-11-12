"""Builds the four fragment files of Reasoning package 3 (Blood Relations, Direction Sense, Coding and Decoding,
Alphanumeric Series, Alphabet Test, Number Series (Reasoning)) for batches 7-10:
batches/parts/frag/BATCH_00k_REAS_pkg3.json, following batches/plans/packages/REAS_pkg3.json.

Helpers (family tree, walk/compass, letter-rule library, sentence-code solver, option placement) are copied from
tools/batch_005/reasoning.py. Every answer is recomputed in code:
- blood relations: an explicit family tree checks every stated fact and names the asked relation;
- directions: coordinates (east, north) from the stated moves;
- coding: an inferred rule must be the only answer given by every rule of the alternative-rule library that fits
  the examples; sentence codes are solved by enumerating every word->code bijection; stated rules are applied in code;
- alphanumeric series, alphabet test and number questions: recomputed from the arrangement / word / numbers.
The script asserts each batch's quota (topic x difficulty), its ID range and its first stimulus ID before writing;
if any assertion fails, nothing is written. --draft prints quota gaps instead of asserting them.
--dump <file> writes a key-free dump for the blind solver.

    python tools/packages/REAS_pkg3.py        (run from docs/question-bank)
"""

import itertools
import json
import math
import string
import sys
from collections import Counter
from pathlib import Path

TOOLS = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(TOOLS))
from qbank import default_mappings  # noqa: E402

ROOT = TOOLS.parent
PKG = json.loads((ROOT / "batches" / "plans" / "packages" / "REAS_pkg3.json").read_text(encoding="utf-8"))
TODAY = "2026-11-05"
RA = "Reasoning Ability"
LETTERS = "ABCD"
RECOMP = ("script:recompute", "ai:author-solve")
SELF = ("ai:author-solve", "ai:self-recheck")

# ---- per-batch state: begin(k) switches the globals that q(), place() and stimulus() use
STATE = {}
QUESTIONS, STIMULI, KEYCOUNT = [], [], Counter()
FIRST_Q = FIRST_STIM = 0


def begin(k):
    global QUESTIONS, STIMULI, KEYCOUNT, FIRST_Q, FIRST_STIM
    b = PKG["batches"][k]
    STATE[k] = {"questions": [], "stimuli": [], "keys": Counter()}
    QUESTIONS, STIMULI, KEYCOUNT = STATE[k]["questions"], STATE[k]["stimuli"], STATE[k]["keys"]
    FIRST_Q = int(b["question_ids"][0][-6:])
    FIRST_STIM = int(b["stimulus_id_start"][-6:])


# ------------------------------------------------------------------------------------------------ generic helpers (copied from tools/batch_005/reasoning.py)
def place(correct, wrongs, natural=None):
    """Returns (options, key). natural=None: put the correct option on the least-used key so far (keeps A-D balanced);
    natural=callable: sort all four options by it (numbers stay in order) and let the key fall where it falls."""
    wrongs = list(wrongs)
    assert len(wrongs) == 3 and correct not in wrongs and len(set(wrongs)) == 3, (correct, wrongs)
    if natural:
        opts = sorted([correct] + wrongs, key=natural)
    else:
        # least-used key so far (keeps A-D balanced); ties broken by a seeded random choice so the keys do not
        # follow a visible A, B, C, D cycle
        low = min(KEYCOUNT[L] for L in LETTERS)
        k = __import__("random").Random(FIRST_Q * 7 + len(QUESTIONS)).choice(
            [L for L in LETTERS if KEYCOUNT[L] <= low + 1])
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



BLD = "Blood Relations"
DIR = "Direction Sense"

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


# ------------------------------------------------------------------------------------------------ package helpers
DRB, CDB, FPZ = "Direct relation", "Coded blood relation", "Family puzzle"
DD, PP, SH_ = "Distance and direction", "Point-to-point", "Shadow-based"
LC, SW, NC = "Letter coding", "Sentence/word coding", "Number coding"
ABT = "Alphabet Test"
LP, WF, PRS = "Letter position", "Word formation", "Pairs of letters"
NSR = "Number Series (Reasoning)"
NDO, TDN = "Number-based digit operations", "Three-digit number questions"
ANG = {"N": 0, "NE": 45, "E": 90, "SE": 135, "S": 180, "SW": 225, "W": 270, "NW": 315}
ANAME = {"N": "North", "NE": "North-East", "E": "East", "SE": "South-East", "S": "South", "SW": "South-West",
         "W": "West", "NW": "North-West"}
DEG = {v: ANAME[k] for k, v in ANG.items()}
DVEC = {0: (0, 1), 45: (1, 1), 90: (1, 0), 135: (1, -1), 180: (0, -1), 225: (-1, -1), 270: (-1, 0), 315: (-1, 1)}
SIDE = {"L": "left", "R": "right"}


def walk_trace(start, moves, unit):
    """Step texts for walk(): the facing after each turn and the running position (east, north)."""
    f, x, y, out = start, 0, 0, []
    for t, d in moves:
        if t:
            nf = turn(f, t)
            head = f"Turn {SIDE[t]} from {NAME[f].lower()} ⇒ {NAME[nf].lower()}"
            f = nf
        else:
            head = f"Start {NAME[f].lower()}"
        x, y = x + VEC[f][0] * d, y + VEC[f][1] * d
        out.append(f"{head}: {d} {unit} → ({x}, {y})")
    assert (x, y) == walk(start, moves)
    return out


def walk_deg(start, moves):
    """moves: (clockwise turn in degrees, k); headings stay multiples of 45°; a diagonal leg of k moves k east/west and
    k north/south (length k√2). Returns the final (x, y) and the step texts."""
    h, x, y, out = ANG[start], 0, 0, []
    for t, k in moves:
        h = (h + t) % 360
        dx, dy = DVEC[h]
        x, y = x + dx * k, y + dy * k
        out.append(f"Heading {DEG[h].lower()}, {k}{'√2' if h % 90 else ''} → ({x}, {y})")
    return (x, y), out


def dd_wrongs(x, y, unit, total, back=False):
    """Three wrong 'distance, direction' options with the slip each one makes. back=True asks for the direction of
    the start from the end point."""
    sx, sy = (-x, -y) if back else (x, y)
    c = f"{dist(x, y)} {unit}, {compass(sx, sy)}"
    cands = []
    if sx:
        cands.append((f"{dist(x, y)} {unit}, {compass(-sx, sy)}", "mixes up east and west"))
    cands.append((f"{dist(x, y)} {unit}, {compass(-sx, -sy)}",
                  "gives the end point's direction from the start" if back else
                  "gives the direction of the start from the end point"))
    if sx and sy:
        cands.append((f"{abs(x) + abs(y)} {unit}, {compass(sx, sy)}", "adds the two components instead of using "
                                                                       "Pythagoras"))
    cands.append((f"{total} {unit}, {compass(sx, sy)}", "adds every leg travelled"))
    if sy:
        cands.append((f"{dist(x, y)} {unit}, {compass(sx, -sy)}", "mixes up north and south"))
    out, why = [], []
    for o, r in cands:
        if o != c and o not in out:
            out.append(o)
            why.append(f"'{o}' {r}")
    return c, out[:3], "; ".join(why[:3]) + "."


def kind(t):
    return "number" if is_d(t) else "letter" if is_l(t) else "symbol"


def fmt(seq):
    return " ".join(seq)


def ordn(k):
    return f"{k}{'th' if 10 <= k % 100 <= 20 else {1: 'st', 2: 'nd', 3: 'rd'}.get(k % 10, 'th')}"


def near_l(c, k=3):
    """Wrong letter options: letters next to c in the alphabet."""
    out = []
    for d in (1, -1, 2, -2, 3):
        p = pos(c) + d
        if 1 <= p <= 26:
            out.append(AL[p - 1])
    return out[:k]


DR2 = {}
for k_ in range(-9, 10):
    for nm_, f_ in (("id", lambda n: n), ("rev", lambda n: n[::-1]), ("pairswap", lambda n: n[1] + n[0] + n[3] + n[2]),
                    ("halfswap", lambda n: n[2:] + n[:2]), ("ends", lambda n: n[3] + n[1:3] + n[0])):
        DR2[f"{nm_}{k_}"] = lambda n, f_=f_, k_=k_: "".join(str((int(d) + k_) % 10) for d in f_(n))
        DR2[f"{k_}-{nm_}"] = lambda n, f_=f_, k_=k_: "".join(str((k_ - int(d)) % 10) for d in f_(n))
        DR2[f"{nm_}alt{k_}"] = lambda n, f_=f_, k_=k_: "".join(
            str((int(d) + (k_ if i % 2 == 0 else -k_)) % 10) for i, d in enumerate(f_(n)))


def decoded(examples, code, options, correct, rules=LRULES):
    """Decoding check: every library rule that fits the examples maps the correct option, and no other option, to
    the given code."""
    fits = [f_ for f_ in rules.values() if all(f_(a) == b for a, b in examples)]
    assert fits
    for f_ in fits:
        assert [o for o in options if f_(o) == code] == [correct], (examples, code)
    return correct


def collinear(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0]) == 0


# question IDs a separate fresh solver answered blind from a key-free dump and matched (compared by option text;
# option order was reshuffled afterwards, question texts and option sets unchanged): all Blood Relations and
# Direction Sense items
BLIND_OK = {
    "BANK_REAS_001300", "BANK_REAS_001301", "BANK_REAS_001302", "BANK_REAS_001303", "BANK_REAS_001304",
    "BANK_REAS_001305", "BANK_REAS_001306", "BANK_REAS_001307", "BANK_REAS_001308", "BANK_REAS_001309",
    "BANK_REAS_001310", "BANK_REAS_001311", "BANK_REAS_001312", "BANK_REAS_001313", "BANK_REAS_001314",
    "BANK_REAS_001315", "BANK_REAS_001316", "BANK_REAS_001317", "BANK_REAS_001318", "BANK_REAS_001319",
    "BANK_REAS_001320", "BANK_REAS_001321", "BANK_REAS_001322", "BANK_REAS_001323", "BANK_REAS_001507",
    "BANK_REAS_001508", "BANK_REAS_001509", "BANK_REAS_001510", "BANK_REAS_001511", "BANK_REAS_001512",
    "BANK_REAS_001513", "BANK_REAS_001514", "BANK_REAS_001515", "BANK_REAS_001516", "BANK_REAS_001517",
    "BANK_REAS_001518", "BANK_REAS_001519", "BANK_REAS_001520", "BANK_REAS_001521", "BANK_REAS_001522",
    "BANK_REAS_001523", "BANK_REAS_001524", "BANK_REAS_001706", "BANK_REAS_001707", "BANK_REAS_001708",
    "BANK_REAS_001709", "BANK_REAS_001710", "BANK_REAS_001711", "BANK_REAS_001712", "BANK_REAS_001713",
    "BANK_REAS_001714", "BANK_REAS_001715", "BANK_REAS_001716", "BANK_REAS_001717", "BANK_REAS_001718",
    "BANK_REAS_001719", "BANK_REAS_001720", "BANK_REAS_001900", "BANK_REAS_001901", "BANK_REAS_001902",
    "BANK_REAS_001903", "BANK_REAS_001904", "BANK_REAS_001905", "BANK_REAS_001906", "BANK_REAS_001907",
    "BANK_REAS_001908", "BANK_REAS_001909", "BANK_REAS_001910", "BANK_REAS_001911", "BANK_REAS_001912",
    "BANK_REAS_001913", "BANK_REAS_001914", "BANK_REAS_001915", "BANK_REAS_001916", "BANK_REAS_001917",
    "BANK_REAS_001918", "BANK_REAS_001919", "BANK_REAS_001920", "BANK_REAS_001921", "BANK_REAS_001922",
    "BANK_REAS_001923", "BANK_REAS_001924"
}


def sentence_solve(sentences, ask):
    """Faster equivalent of the batch-5 solver: a word can take a code only if both occur in exactly the same
    sentences (any other choice breaks some sentence's code set); a bijection exists when every such membership
    class has as many words as codes. Returns the set of codes 'ask' (a word) can take, or the words a code can be."""
    words = sorted({w for ws, _ in sentences for w in ws})
    codes = sorted({c for _, cs in sentences for c in cs})
    assert len(words) == len(codes) and all(len(ws) == len(cs) == len(set(cs)) for ws, cs in sentences)
    sig_w = {w: tuple(w in ws for ws, _ in sentences) for w in words}
    sig_c = {c: tuple(c in cs for _, cs in sentences) for c in codes}
    for s in set(sig_w.values()) | set(sig_c.values()):
        assert sum(v == s for v in sig_w.values()) == sum(v == s for v in sig_c.values()), "no consistent coding"
    if ask in sig_w:
        return {c for c in codes if sig_c[c] == sig_w[ask]}
    return {w for w in words if sig_w[w] == sig_c[ask]}


# ================================================================================================ BATCH 007
begin("007")
# ---------------------------------------------------------------- Blood relations: Basic (standalone)
F = Family().add("Vinod", "M").add("Vw", "F").marry("Vinod", "Vw").add("Hemant", "M", "Vinod", "Vw")
F.add("Gm", "F", "Vinod", "Vw").add("Gf", "M").marry("Gf", "Gm").add("Gauri", "F", "Gf", "Gm")
F.check([("Gm", "sister", "Hemant"), ("Gm", "mother", "Gauri"), ("Vinod", "father", "Hemant")])
ans = F.rel("Vinod", "Gauri")
assert ans == "grandfather"
mcq(BLD, DRB, "Basic", "Gauri's mother is the only sister of Hemant. Hemant's father is Vinod. How is Vinod related to "
    "Gauri?", cap(ans), ["Father", "Uncle", "Father-in-law"], "A mother's father is a grandfather",
    "Gauri's mother is Hemant's sister, so she is also Vinod's daughter. Vinod is therefore the father of Gauri's "
    "mother: Gauri's (maternal) grandfather.",
    ["Gauri's mother = Hemant's sister ⇒ Vinod's daughter", "Father of one's mother ⇒ grandfather"],
    why_others_wrong="Father and Uncle put Vinod one generation too low; Father-in-law would need Gauri to be married to "
                     "Vinod's son.", seconds=30, verified_by=RECOMP)
F = Family().add("Mp", "M").add("Mm", "F").marry("Mp", "Mm").add("Manoj", "M", "Mp", "Mm")
F.add("Nikhil", "M", "Mp", "Mm").add("Lalita", "F").marry("Manoj", "Lalita").add("Ketan", "M", "Manoj", "Lalita")
F.check([("Nikhil", "brother", "Manoj"), ("Lalita", "wife", "Manoj"), ("Ketan", "son", "Lalita")])
ans = F.rel("Ketan", "Nikhil")
assert ans == "nephew"
mcq(BLD, DRB, "Basic", "Nikhil is the only brother of Manoj. Lalita is Manoj's wife, and Ketan is Lalita's son. How is "
    "Ketan related to Nikhil?", cap(ans), ["Son", "Brother", "Cousin"], "A brother's son is a nephew",
    "Ketan is the son of Lalita and her husband Manoj. Manoj is Nikhil's brother, so Ketan is the son of Nikhil's "
    "brother: Nikhil's nephew.", ["Ketan = son of Manoj (Lalita's husband)", "Son of one's brother ⇒ nephew"],
    why_others_wrong="Ketan's father is Manoj, not Nikhil; Ketan is a generation below Nikhil, so he is neither his "
                     "brother nor his cousin.", seconds=30, verified_by=RECOMP)
F = Family().add("C", "M").add("D", "F").marry("C", "D").add("B", "M", "C", "D").add("Bw", "F").marry("B", "Bw")
F.add("A", "M", "B", "Bw")
F.check([("B", "son", "C"), ("D", "wife", "C")])
F2 = Family().add("C", "M").add("D", "F").marry("C", "D").add("B", "M", "C", "D").add("Bw", "F").marry("B", "Bw")
F2.add("A", "F", "B", "Bw")
ans = F.rel("D", "A")
assert ans == F2.rel("D", "A") == "grandmother"
mcq(BLD, DRB, "Basic", "A is the child of B. B is the only son of C, and D is C's wife. How is D related to A?",
    cap(ans), ["Mother", "Aunt", "Mother-in-law"], "The wife of a grandfather is a grandmother",
    "B is the son of C and his wife D, so D is B's mother. A is B's child, so D is A's grandmother (whether A is a boy "
    "or a girl).", ["D = mother of B", "A = child of B ⇒ D is A's grandmother"],
    why_others_wrong="Mother is D's relation to B; Aunt would need D to be a sister of A's parent; Mother-in-law would "
                     "need A to be married to D's child.", seconds=30, verified_by=RECOMP)
F = Family().add("Tf", "M").add("Usha", "F").marry("Tf", "Usha").add("Tara", "F", "Tf", "Usha")
F.add("Sb", "M", "Tf", "Usha").add("Simran", "F").marry("Sb", "Simran")
F.check([("Sb", "brother", "Tara"), ("Usha", "mother", "Tara")])
ans = F.rel("Simran", "Usha")
assert ans == "daughter-in-law"
mcq(BLD, DRB, "Basic", "Simran's husband is the brother of Tara. Tara's mother is Usha. How is Simran related to Usha?",
    cap(ans), ["Daughter", "Sister-in-law", "Niece"], "A son's wife is a daughter-in-law",
    "Simran's husband is Tara's brother, so he is also Usha's son. Simran, the wife of Usha's son, is Usha's "
    "daughter-in-law.", ["Simran's husband = Tara's brother = Usha's son", "Son's wife ⇒ daughter-in-law"],
    why_others_wrong="Simran is not Usha's own child; she is Tara's sister-in-law, not Usha's; a niece is a sibling's "
                     "daughter.", seconds=30, verified_by=RECOMP)
F = Family().add("Mohit", "M").add("Deepa", "F").marry("Mohit", "Deepa").add("Arjun", "M", "Mohit", "Deepa")
F.add("Kavita", "F").marry("Arjun", "Kavita")
F.check([("Arjun", "son", "Deepa"), ("Mohit", "husband", "Deepa")])
ans = F.rel("Mohit", "Kavita")
assert ans == "father-in-law"
mcq(BLD, DRB, "Basic", "Deepa's son Arjun is married to Kavita. Mohit is Deepa's husband. How is Mohit related to "
    "Kavita?", cap(ans), ["Father", "Brother-in-law", "Grandfather"], "A husband's father is a father-in-law",
    "Arjun is the son of Deepa and her husband Mohit. Kavita is Arjun's wife, so Mohit is her husband's father: her "
    "father-in-law.", ["Mohit = Arjun's father", "Father of one's husband ⇒ father-in-law"],
    why_others_wrong="Kavita is not Mohit's own child; a brother-in-law would be in Kavita's generation; Grandfather "
                     "skips a generation.", seconds=30, verified_by=RECOMP)

# ---------------------------------------------------------------- Blood relations: Intermediate set (digit codes)
CODE_D7 = {"1": "father", "2": "daughter", "3": "wife", "4": "brother", "5": "mother"}
CODE_D7_TXT = ("In a certain code:\n'P 1 Q' means 'P is the father of Q';\n'P 2 Q' means 'P is the daughter of Q';\n"
               "'P 3 Q' means 'P is the wife of Q';\n'P 4 Q' means 'P is the brother of Q';\n'P 5 Q' means 'P is the "
               "mother of Q'.\n\nUse only the relations that each expression states.")
sid = stimulus("passage", "Digit codes for relations", CODE_D7_TXT, None,
               "Decode each expression pair by pair from the left, draw the small tree, and read the asked relation "
               "off it. A child of a married person is taken to be the child of the couple.")
BQ = lambda sub, text, correct, wrongs, concept, expl, steps, **kw: mcq(
    BLD, sub, "Intermediate", text, correct, wrongs, concept, expl, steps, stimulus=sid, verified_by=RECOMP, **kw)
F = Family().add("O", "M").add("N", "F").marry("N", "O").add("M", "F", "O", "N").add("L", "M", "O", "N")
F.check(coded_facts("L 4 M 2 N 3 O", CODE_D7))
ans = F.rel("L", "O")
assert ans == "son"
BQ(CDB, "If 'L 4 M 2 N 3 O', how is L related to O?", cap(ans), ["Brother-in-law", "Nephew", "Grandson"],
   "Decode pair by pair", "L is M's brother; M is N's daughter, so L is also N's son; N is O's wife, so L is O's son.",
   ["L 4 M: L is M's brother", "M 2 N: M is N's daughter ⇒ L is N's son", "N 3 O: N is O's wife ⇒ L is O's son"],
   why_others_wrong="Brother-in-law and Nephew would need L to be outside O's own children; Grandson skips a "
                    "generation.", seconds=50)
st_ = []
for hg in ("M", "F"):
    F = Family().add("Ef", "M").add("E", "F").marry("Ef", "E").add("F_", "M", "Ef", "E").add("G", "M", "Ef", "E")
    F.add("Gw", "F").marry("G", "Gw").add("H", hg, "G", "Gw")
    F.check(coded_facts("E 5 F_ 4 G 1 H", CODE_D7))
    st_.append((F.rel("E", "H"), F.rel("F_", "H"), F.rel("H", "E"), F.rel("G", "F_")))
assert st_[0][0] == st_[1][0] == "grandmother" and {st_[0][2], st_[1][2]} == {"grandson", "granddaughter"}
assert st_[0][1] == "uncle" and st_[0][3] == "brother"
ans = st_[0][1]
BQ(CDB, "If 'E 5 F 4 G 1 H', how is F related to H?", cap(ans), ["Father", "Brother", "Cousin"],
   "A father's brother is an uncle",
   "E is F's mother; F is G's brother, so F and G are both E's children; G is H's father. F, the brother of H's "
   "father, is H's uncle (whether H is a boy or a girl).", ["E 5 F, F 4 G: F and G are siblings",
                                                             "G 1 H: G is H's father ⇒ F is H's uncle"],
   why_others_wrong="H's father is G; F is a generation above H, so neither H's brother nor cousin.", seconds=55)
# 'U ? V 2 W' - which code makes U definitely W's husband? V is W's daughter.
# code 1: U is V's father. V has one father, so W (V's parent) must be V's mother and U, W's husband.
# code 5: U is V's mother, so W is V's father and U is W's wife. Codes 3 (wife of V) and 4 (brother of V) say nothing.
for c_ in "1345":
    makes_husband = []
    for wg in ("M", "F"):  # W's gender is not given; try both
        if c_ == "1":
            ok_ = wg == "F"  # W = father would give V two fathers
            if ok_:
                F = Family().add("U", "M").add("W", "F").marry("U", "W").add("V", "F", "U", "W")
                F.check(coded_facts("U 1 V 2 W", CODE_D7))
                makes_husband.append(F.rel("U", "W") == "husband")
        elif c_ == "5":
            ok_ = wg == "M"
            if ok_:
                F = Family().add("U", "F").add("W", "M").marry("U", "W").add("V", "F", "W", "U")
                F.check(coded_facts("U 5 V 2 W", CODE_D7))
                makes_husband.append(F.rel("U", "W") == "husband")
        else:
            makes_husband.append(False)  # U is V's wife / brother: no link to W as a spouse is stated
    assert all(makes_husband) == (c_ == "1"), c_
BQ(CDB, "In the expression 'U ? V 2 W', which code should replace ? so that U is definitely the husband of W?", "1",
   ["3", "4", "5"], "Fix V's parents first",
   "V is W's daughter. With '1', U is V's father; V has only one father, so W must be V's mother and U, the father of "
   "her daughter, is W's husband. With '5', U would be V's mother (W's wife, not husband); with '3' or '4' U is V's "
   "wife or brother, which says nothing about U being W's husband.",
   ["V 2 W: V is W's daughter", "U 1 V: U is V's father ⇒ W is V's mother ⇒ U is W's husband",
    "Test 3, 4, 5: none makes U W's husband"],
   why_others_wrong="'3' makes U V's wife, '4' V's brother and '5' V's mother — none makes U the husband of W.",
   seconds=60)

# ---------------------------------------------------------------- Blood relations: Advanced set (family of eight)
F = Family().add("Anand", "M").add("Bharati", "F").marry("Anand", "Bharati")
for c_, g_ in (("Chinmay", "M"), ("Damini", "F"), ("Gopal", "M")):
    F.add(c_, g_, "Anand", "Bharati")
F.add("Fatima", "F").marry("Chinmay", "Fatima").add("Hema", "F").marry("Gopal", "Hema")
F.add("Ekansh", "M", "Gopal", "Hema")
# every clue holds in this tree ...
assert F.children("Anand") == {"Chinmay", "Damini", "Gopal"} and [c for c in F.children("Anand") if F.g[c] == "F"] == ["Damini"]
assert "Damini" not in F.sp and {g for a in F.children("Anand") for g in F.children(a)} == {"Ekansh"}
assert F.rel("Fatima", "Ekansh") == "aunt" and F.rel("Gopal", "Ekansh") == "father" and F.rel("Chinmay", "Anand") == "son"
# ... and the tree is the only one: Ekansh's father must be a son of Anand (Damini, the only daughter, is unmarried);
# the sons are the two remaining males Chinmay and Gopal; Gopal is not Ekansh's uncle, so he is the father (Hema's
# husband) and Fatima, the wife of one of Ekansh's uncles, is Chinmay's wife.
FAM_TXT = ("A family has eight members: Anand, Bharati, Chinmay, Damini, Ekansh, Fatima, Gopal and Hema. There are "
           "exactly three married couples, and every married person's spouse is a member of the family. Anand is "
           "male.")
FAM_C = [("Anand and Bharati are married to each other and have exactly three children, of whom only one is a "
          "daughter.", (), None),
         ("Damini is the daughter of Bharati and is unmarried.", (), None),
         ("Ekansh, a boy, is the only grandchild of Anand, and Hema is Ekansh's mother.", (), None),
         ("Chinmay is a son of Anand.", (), None),
         ("Fatima is the wife of one of Ekansh's uncles.", (), None),
         ("Gopal is not an uncle of Ekansh.", (), None)]
sid = stimulus("puzzle", "A family of eight with three couples", FAM_TXT, FAM_C,
               "Anand's children are Damini and two sons. Ekansh's mother Hema must be married to a son of Anand "
               "(Damini is unmarried). The only males left are Chinmay, Ekansh and Gopal, and Ekansh is a grandchild, "
               "so Anand's sons are Chinmay and Gopal. Gopal is not Ekansh's uncle, so he is Ekansh's father and "
               "Hema's husband; Fatima is then Chinmay's wife.\nTree: Anand + Bharati → Chinmay (+ Fatima), Damini, "
               "Gopal (+ Hema) → Ekansh.")
TREE7 = "Anand + Bharati → Chinmay (+ Fatima), Damini, Gopal (+ Hema) → Ekansh"
AQ = lambda text, correct, wrongs, concept, expl, steps, **kw: mcq(
    BLD, FPZ, "Advanced", text, correct, wrongs, concept, expl, steps, stimulus=sid, verified_by=RECOMP, **kw)
ans = F.rel("Fatima", "Ekansh")
AQ("How is Fatima related to Ekansh?", cap(ans), ["Mother", "Sister", "Grandmother"], "Fix both couples first",
   "Ekansh's father is Gopal, and Chinmay is Gopal's brother. Fatima is Chinmay's wife, so she is the wife of "
   "Ekansh's paternal uncle: his aunt.", [TREE7, "Fatima = wife of Chinmay = wife of Ekansh's uncle ⇒ aunt"],
   why_others_wrong="Ekansh's mother is Hema; Fatima is a generation above Ekansh, so she is not his sister; his "
                    "grandmother is Bharati.", seconds=90)
ans = F.rel("Chinmay", "Hema")
assert ans == "brother-in-law"
AQ("How is Chinmay related to Hema?", cap(ans), ["Husband", "Father-in-law", "Brother"],
   "Husband's brother = brother-in-law",
   "Hema is Gopal's wife, and Chinmay is Gopal's brother, so Chinmay is Hema's husband's brother: her "
   "brother-in-law.", [TREE7, "Hema's husband Gopal; Chinmay = Gopal's brother"],
   why_others_wrong="Hema's husband is Gopal; Anand is her father-in-law; Chinmay is not Hema's own brother.",
   seconds=80)
ans = next(m for m in F.parents("Ekansh") if F.g[m] == "M")
assert ans == "Gopal" and F.rel("Damini", "Gopal") == "sister"
AQ("Who is Ekansh's father?", ans, ["Chinmay", "Anand", "Cannot be determined"], "Use the 'not an uncle' clue",
   "Ekansh's father is a son of Anand, i.e. Chinmay or Gopal. The other son would be Ekansh's uncle, and Gopal is "
   "not his uncle, so Gopal is the father.", ["Ekansh's father ∈ {Chinmay, Gopal}", "Gopal is not an uncle ⇒ Gopal "
                                                                                  "is the father"],
   why_others_wrong="Chinmay is Ekansh's uncle (Fatima's husband); Anand is his grandfather; the last clue settles "
                    "it, so it can be determined.", seconds=80)
fem = sorted(p for p, g_ in F.g.items() if g_ == "F")
a, w = count_opts(len(fem))
assert len(fem) == 4
AQ("How many female members are there in the family?", a, w, "Read each member's gender off the tree",
   "Bharati (wife of Anand), Damini (a daughter), Fatima (a wife) and Hema (a mother) are female; Anand, Chinmay, "
   "Gopal and Ekansh are male. Four females.", [TREE7, "Females: " + ", ".join(fem)], natural=by_num,
   why_others_wrong="Every member's gender follows from the clues: Chinmay and Gopal are Anand's sons and Ekansh is "
                    "a boy.", seconds=70)

# ---------------------------------------------------------------- Blood relations: Advanced (standalone)
CODE_S7 = {"◆": "parent", "●": "sister", "■": "husband", "▲": "son"}
res_ = set()
for ug in ("M", "F"):
    F = Family().add("Tp", "M").add("Tm", "F").marry("Tp", "Tm").add("T", "F", "Tp", "Tm").add("U", ug, "Tp", "Tm")
    F.add("S", "M").marry("S", "T").add("R", "M", "S", "T").add("Us", "F" if ug == "M" else "M").marry("U", "Us")
    F.add("V", "F", "U", "Us") if ug == "M" else F.add("V", "F", "Us", "U")
    assert F.rel("R", "S") == "son" and F.rel("S", "T") == "husband" and F.rel("T", "U") == "sister"
    assert "U" in F.parents("V")
    res_.add(F.rel("V", "R"))
assert res_ == {"cousin"}
mcq(BLD, CDB, "Advanced",
    "In a certain code:\n'P ◆ Q' means 'P is a parent of Q';\n'P ● Q' means 'P is the sister of Q';\n'P ■ Q' means 'P "
    "is the husband of Q';\n'P ▲ Q' means 'P is the son of Q'.\n\nIf 'R ▲ S ■ T ● U ◆ V', how is V related to R?",
    "Cousin", ["Nephew", "Brother", "Uncle"], "A parent's sibling's child is a cousin",
    "R is S's son; S is T's husband, so T is R's mother; T is U's sister, so U is R's maternal uncle or aunt; U is "
    "V's parent, so V is the child of R's mother's sibling: R's cousin (whatever the genders of U and V).",
    ["R ▲ S ■ T: R is the son of S and T", "T ● U: U is a sibling of R's mother", "U ◆ V: V is U's child ⇒ cousin"],
    why_others_wrong="Nephew would put V a generation below R; Brother needs the same parents; Uncle a generation "
                     "above.", seconds=75, verified_by=RECOMP)
F = Family().add("Rf", "M").add("Rm", "F").marry("Rf", "Rm").add("G", "M", "Rf", "Rm").add("Rekha", "F", "Rf", "Rm")
F.add("Gw", "F").marry("G", "Gw").add("Nf", "M", "G", "Gw").add("Nm", "F").marry("Nf", "Nm")
F.add("Nitin", "M", "Nf", "Nm")
assert F.rel("G", "Nm") == "father-in-law" and [c for c in F.children("Rf") if F.g[c] == "M"] == ["G"]
assert "Rekha" in F.siblings("G") and F.rel("G", "Nitin") == "grandfather" and F.rel("Rekha", "Nitin") is None
mcq(BLD, DRB, "Advanced",
    "Rekha said to Nitin, \"Your mother's father-in-law is the only son of my father.\" How is Rekha related to "
    "Nitin?", "Grand-aunt (sister of his paternal grandfather)", ["Aunt", "Grandmother", "Mother-in-law"],
    "Collapse the phrase step by step",
    "Nitin's mother's father-in-law is the father of Nitin's father: Nitin's paternal grandfather. He is the only son "
    "of Rekha's father, so he is Rekha's brother. Rekha is therefore the sister of Nitin's grandfather: his "
    "grand-aunt.", ["Mother's father-in-law = father's father = grandfather",
                    "Only son of Rekha's father = Rekha's brother", "Grandfather's sister ⇒ grand-aunt"],
    why_others_wrong="Aunt would be the sister of Nitin's father; Grandmother would be the grandfather's wife, not "
                     "his sister; Mother-in-law has no basis.", seconds=75, verified_by=RECOMP)

# ---------------------------------------------------------------- Direction: Basic
ren = (ANG["E"] - ANG["S"]) % 360
assert (ANG["N"] + ren) % 360 == ANG["W"] and (ANG["E"] + ren) % 360 == ANG["N"]
ans = DEG[(ANG["W"] + ren) % 360]
assert ans == "South"
mcq(DIR, DD, "Basic", "In a certain system, every direction is renamed in the same way: south is called east, east is "
    "called north and north is called west. What is west called in that system?", ans, ["North", "East", "West"],
    "Renaming = turning every direction by the same angle",
    "South → east is a 90° anticlockwise turn, and so are east → north and north → west. Turning west 90° "
    "anticlockwise gives south.", ["Each name is 90° anticlockwise of the true direction",
                                   "West turned 90° anticlockwise ⇒ South"],
    why_others_wrong="North turns west the other way; East reverses it; West would mean no renaming at all.",
    seconds=35, verified_by=RECOMP)
MV = [(None, 14), ("L", 9), ("L", 6), ("L", 3)]
x, y = walk("E", MV)
assert (x, y) == (8, 6)
c, w, why = dd_wrongs(x, y, "km", 32)
mcq(DIR, DD, "Basic", "Harsh drives 14 km towards the east. He turns left and drives 9 km, turns left again and drives "
    "6 km, and then turns left once more and drives 3 km. How far is he now from his starting point, and in which "
    "direction?", c, w, "Net east and net north displacement",
    "He ends 14 − 6 = 8 km east and 9 − 3 = 6 km north of the start: √(64 + 36) = 10 km, north-east.",
    walk_trace("E", MV, "km") + ["√(8² + 6²) = 10 km, North-East"], why_others_wrong=why, seconds=40,
    verified_by=RECOMP)

# ---------------------------------------------------------------- Direction: Intermediate set (town map)
PT = {"M": (0, 0)}
PT["T"] = (0, 12)
PT["S"] = (PT["T"][0] + 5, PT["T"][1])
PT["H"] = (-5, 0)
PT["P"] = (PT["T"][0], PT["T"][1] - 6)
PT["L"] = (PT["H"][0] + 1, PT["H"][1])
NM7 = {"M": "market", "T": "temple", "S": "school", "H": "hospital", "P": "post office", "L": "library"}
sid = stimulus("puzzle", "Six places in a small town",
               "Six places in a small town are located as follows.", [
                   ("The temple is 12 km north of the market.", (), None),
                   ("The school is 5 km east of the temple.", (), None),
                   ("The hospital is 5 km west of the market.", (), None),
                   ("The post office is 6 km south of the temple.", (), None),
                   ("The library is 1 km east of the hospital.", (), None)],
               "Put the market at (0, 0), east and north positive: temple (0, 12), school (5, 12), hospital (−5, 0), "
               "post office (0, 6), library (−4, 0).")
MAP7 = "Market (0, 0), temple (0, 12), school (5, 12), hospital (−5, 0), post office (0, 6), library (−4, 0)"
DQ = lambda sub, text, correct, wrongs, concept, expl, steps, **kw: mcq(
    DIR, sub, "Intermediate", text, correct, wrongs, concept, expl, steps, stimulus=sid, verified_by=RECOMP, **kw)
dx, dy = PT["S"]
c, w, why = dd_wrongs(dx, dy, "km", 17)
assert c == "13 km, North-East"
DQ(PP, "How far is the school from the market, and in which direction?", c, w, "A 5-12-13 triangle",
   "The school is 5 km east and 12 km north of the market: √(25 + 144) = 13 km, north-east.",
   [MAP7, "School − market = (5, 12)", "√(5² + 12²) = 13 km, North-East"], why_others_wrong=why, seconds=60)
on_line = [k for k in PT if k not in "HS" and collinear(PT["H"], PT["S"], PT[k])
           and min(PT["H"][0], PT["S"][0]) <= PT[k][0] <= max(PT["H"][0], PT["S"][0])]
assert on_line == ["P"]
DQ(PP, "Which place lies on the straight road joining the hospital and the school?", "Post office",
   ["Library", "Market", "Temple"], "Midpoint test",
   "The hospital is at (−5, 0) and the school at (5, 12). The midpoint of this segment is (0, 6), exactly where the "
   "post office is. The library and the market lie on the line y = 0 and the temple at (0, 12), none of them on the "
   "segment.", [MAP7, "Midpoint of hospital and school = (0, 6) = post office"],
   why_others_wrong="The library (−4, 0), the market (0, 0) and the temple (0, 12) are off the hospital–school line.",
   seconds=70)
dx, dy = PT["S"][0] - PT["L"][0], PT["S"][1] - PT["L"][1]
c, w, why = dd_wrongs(dx, dy, "km", 21)
assert c == "15 km, North-East"
DQ(PP, "What is the straight-line distance between the library and the school, and in which direction is the school "
   "from the library?", c, w, "Difference of two positions",
   "Library (−4, 0), school (5, 12): the school is 9 km east and 12 km north of the library, √(81 + 144) = 15 km, "
   "north-east.", [MAP7, "School − library = (9, 12)", "√(9² + 12²) = 15 km, North-East"], why_others_wrong=why,
   seconds=70)
dx, dy = PT["H"][0] - PT["T"][0], PT["H"][1] - PT["T"][1]
ans = compass(dx, dy)
assert ans == "South-West"
DQ(PP, "In which direction is the hospital with respect to the temple?", ans, ["North-East", "South-East", "West"],
   "Signs of the two components",
   "Hospital (−5, 0) minus temple (0, 12) = (−5, −12): west and south, so the hospital is south-west of the temple.",
   [MAP7, "Hospital − temple = (−5, −12) ⇒ South-West"],
   why_others_wrong="North-East is the temple's direction from the hospital; South-East takes the hospital as east of "
                    "the market; West ignores the 12 km north–south gap.", seconds=55)

# ---------------------------------------------------------------- Direction: Intermediate (standalone)
right_of = {"N": "E", "E": "S", "S": "W", "W": "N"}
shadow = right_of["S"]
sun = {"E": "W", "W": "E"}[shadow]
assert shadow == "W" and sun == "E"
mcq(DIR, SH_, "Intermediate", "Tina was standing in an open field facing south, and her shadow fell exactly to her "
    "right. At what time of the day was this most likely?", "In the morning, after sunrise",
    ["In the evening, before sunset", "At noon", "The time cannot be judged from a shadow"],
    "A shadow points away from the sun",
    "Facing south, her right is west, so the shadow pointed west. A shadow points away from the sun, so the sun was in "
    "the east: it was morning.", ["Facing south ⇒ right = west", "Shadow west ⇒ sun east ⇒ morning"],
    why_others_wrong="In the evening the sun is in the west and the shadow would fall to her left; at noon the shadow "
                     "is very short and points north (in India), not west; the side of the shadow does tell the time "
                     "of day.", seconds=45, verified_by=RECOMP)
MV = [(None, 10), ("R", 5), ("R", 4), ("L", 3)]
x, y = walk("N", MV)
assert (x, y) == (8, 6)
c, w, why = dd_wrongs(x, y, "m", 22, back=True)
assert c == "10 m, South-West"
mcq(DIR, DD, "Intermediate", "Vivaan walks 10 m towards the north. He turns right and walks 5 m, turns right again and "
    "walks 4 m, and then turns left and walks 3 m. How far must he walk now, and in which direction, to go straight "
    "back to his starting point?", c, w, "The way back is the opposite of the displacement",
    "He ends 8 m east and 6 m north of the start, 10 m away. To return he must walk 10 m towards the south-west.",
    walk_trace("N", MV, "m") + ["Displacement (8, 6): 10 m north-east of the start", "Way back: 10 m, South-West"],
    why_others_wrong=why, seconds=60, verified_by=RECOMP)
a_ = (ANG["E"] + 135) % 360
b_ = (ANG["W"] - 135) % 360
gap = min(abs(a_ - b_), 360 - abs(a_ - b_))
assert (DEG[a_], DEG[b_], gap) == ("South-West", "South-East", 90)
mcq(DIR, DD, "Intermediate", "Kabir and Laila stand back to back, Kabir facing east. Kabir then turns 135° clockwise, "
    "and Laila turns 135° anticlockwise. What is the smaller angle between the directions they now face?", "90°",
    ["45°", "135°", "180°"], "Find each new facing, then compare",
    "Kabir: east + 135° clockwise = south-west. Laila faces west (back to back with Kabir); west − 135° = south-east. "
    "South-west and south-east are 90° apart.", ["Kabir: E (90°) + 135° = 225° (SW)", "Laila: W (270°) − 135° = 135° "
                                                                                       "(SE)", "|225° − 135°| = 90°"],
    why_others_wrong="45° and 135° come from turning one of them the wrong way; 180° assumes they still face "
                     "opposite ways.", seconds=55, verified_by=RECOMP)

# ---------------------------------------------------------------- Direction: Advanced (standalone)
(x, y), tr_ = walk_deg("N", [(0, 9), (45, 4), (135, 25), (90, 9)])
assert (x, y) == (-5, -12)
c, w, why = dd_wrongs(x, y, "km", 43)
mcq(DIR, DD, "Advanced", "A drone takes off from point O and flies 9 km towards the north. It then turns 45° clockwise "
    "and flies 4√2 km, turns 135° clockwise and flies 25 km, and finally turns 90° clockwise and flies 9 km. How far "
    "is the drone from O, and in which direction?", c, w, "A diagonal leg of k√2 moves k along each axis",
    "North 9 → (0, 9). A 45° clockwise turn points it north-east; 4√2 km moves it 4 km east and 4 km north → (4, 13). "
    "Another 135° clockwise makes it face south: 25 km → (4, −12). A 90° clockwise turn makes it face west: 9 km → "
    "(−5, −12). Distance √(25 + 144) = 13 km, south-west.",
    tr_ + ["√(5² + 12²) = 13 km, South-West"],
    why_others_wrong=why, seconds=110, verified_by=RECOMP)

# ---------------------------------------------------------------- Coding: Basic
ans = inferred([("PRINT", "MOFKQ")], "GLOBE", shift("GLOBE", -3))
assert ans == "DILYB"
mcq(COD, LC, "Basic", "In a certain code language, PRINT is written as MOFKQ. How is GLOBE written in that code "
    "language?", ans, ["JORGH", "DILYC", "DJLYB"], "Every letter moves back by the same number of places",
    "P→M, R→O, I→F, N→K, T→Q: every letter moves 3 places back. G→D, L→I, O→L, B→Y (B, A, Z, Y), E→B: DILYB.",
    ["P −3 = M, R −3 = O, I −3 = F, N −3 = K, T −3 = Q", "GLOBE −3 ⇒ DILYB"],
    why_others_wrong="JORGH moves every letter forward; DILYC moves E back only 2 places; DJLYB moves L back only 2.",
    seconds=35, verified_by=RECOMP)
spl = lambda w: sum(pos(c) for c in w) + len(w)
ans = inferred([("BAT", 26), ("FUN", 44)], "RICE", spl("RICE"), NRULES)
assert ans == 39
mcq(COD, NC, "Basic", "In a certain code, BAT is written as 26 and FUN is written as 44. How is RICE written in that "
    "code?", str(ans), ["35", "43", "40"], "Sum of positions plus the number of letters",
    "BAT: 2 + 1 + 20 = 23, plus 3 letters = 26. FUN: 6 + 21 + 14 = 41, plus 3 = 44. RICE: 18 + 9 + 3 + 5 = 35, plus 4 "
    "letters = 39.", ["BAT: 23 + 3 = 26 ✓; FUN: 41 + 3 = 44 ✓", "RICE: 35 + 4 = 39"],
    why_others_wrong="35 leaves out the number of letters; 43 adds 8 (twice the length); 40 adds 5.", natural=int,
    seconds=45, verified_by=RECOMP)

# ---------------------------------------------------------------- Coding: Intermediate set (train sentences)
SS = [(["train", "leaves", "early", "today"], ["ve", "ko", "ra", "mi"]),
      (["today", "platform", "is", "crowded"], ["tu", "mi", "ne", "sa"]),
      (["night", "train", "arrives", "today"], ["le", "zo", "mi", "ra"]),
      (["platform", "leaves", "at", "night"], ["pu", "sa", "zo", "ko"])]
sid = stimulus("passage", "Four coded sentences about a train",
               "In a certain code language:\n" + "\n".join(f"'{' '.join(a_)}' is written as '{' '.join(b_)}'"
                                                           for a_, b_ in SS) +
               "\n(The codes of the words in a sentence may be in any order.)", None,
               "today = mi (sentences 1, 2 and 3); train = ra (1 and 3); leaves = ko (1 and 4); platform = sa (2 and "
               "4); night = zo (3 and 4). Leftovers: early = ve, arrives = le, at = pu. 'is' and 'crowded' appear only "
               "in sentence 2, so they share 'tu' and 'ne' in some order.")
CQ = lambda sub, text, correct, wrongs, concept, expl, steps, **kw: mcq(
    COD, sub, "Intermediate", text, correct, wrongs, concept, expl, steps, stimulus=sid, verified_by=RECOMP, **kw)
assert sentence_solve(SS, "early") == {"ve"}
CQ(SW, "What is the code for 'early'?", "ve", ["ko", "ra", "mi"], "Remove the codes of the shared words",
   "In sentence 1, today = mi (in sentences 1, 2, 3), train = ra (1 and 3) and leaves = ko (1 and 4). The leftover "
   "code ve is 'early'.", ["today = mi; train = ra; leaves = ko", "early = ve"],
   why_others_wrong="ko is 'leaves', ra is 'train' and mi is 'today'.", seconds=60)
assert sentence_solve(SS, "pu") == {"at"}
CQ(SW, "Which word is coded as 'pu'?", "at", ["platform", "leaves", "night"], "Leftover code of a sentence",
   "Sentence 4 is 'platform leaves at night' = 'pu sa zo ko'. platform = sa (shared with sentence 2), leaves = ko "
   "(shared with 1) and night = zo (shared with 3), so pu = at.", ["platform = sa; leaves = ko; night = zo",
                                                                 "pu ⇒ at"],
   why_others_wrong="platform = sa, leaves = ko and night = zo.", seconds=60)
assert sentence_solve(SS, "night") == {"zo"} and sentence_solve(SS, "train") == {"ra"}
CQ(SW, "What is the code for 'night train'?", "zo ra", ["le ra", "zo mi", "pu ra"], "Two codes, each from a shared "
                                                                                     "pair of sentences",
   "night is in sentences 3 and 4, whose only common code is zo. train is in sentences 1 and 3, whose common codes "
   "are ra and mi; mi is 'today' (also in sentence 2), so train = ra. 'night train' = 'zo ra'.",
   ["night = zo (3 ∩ 4)", "train = ra (1 ∩ 3, minus today's mi)"],
   why_others_wrong="le is 'arrives', mi is 'today' and pu is 'at'.", seconds=60)
undet = [w_ for w_ in ["crowded", "early", "at", "arrives"] if len(sentence_solve(SS, w_)) > 1]
assert undet == ["crowded"] and sentence_solve(SS, "crowded") == {"tu", "ne"}
CQ(SW, "For which of the following words can the code NOT be found with certainty?", "crowded",
   ["early", "at", "arrives"], "Words that occur only together cannot be separated",
   "'is' and 'crowded' occur only in sentence 2. After today = mi and platform = sa are removed, they are left with "
   "'tu' and 'ne' in an unknown order. early (ve), at (pu) and arrives (le) are each the single leftover of a "
   "sentence.", ["Sentence 2 leftovers: tu, ne for 'is', 'crowded'", "early = ve, at = pu, arrives = le are fixed"],
   why_others_wrong="early, at and arrives each have a fixed code.", seconds=65)

# ---------------------------------------------------------------- Coding: Intermediate (standalone)
hm = LRULES["half+-1"]
assert hm("MARKET") == "JDSLZQ" and hm("SILVER") == "UDQRHK"
ans = inferred([("MARKET", "JDSLZQ"), ("SILVER", "UDQRHK")], "CORNER", hm("CORNER"))
assert ans == "MDQBNQ"
mcq(COD, LC, "Intermediate", "In a certain code, MARKET is written as JDSLZQ and SILVER is written as UDQRHK. How is "
    "CORNER written in that code?", ans, ["BNQMDQ", "ODSDPS", "MDQBNR"], "Swap the halves, then move each letter",
    "MARKET → halves MAR | KET → swapped KETMAR → each letter one place back: JDSLZQ. SILVER → VERSIL → UDQRHK. "
    "CORNER → NERCOR → MDQBNQ.", ["Swap halves: CORNER → NERCOR", "Each letter −1 ⇒ MDQBNQ"],
    why_others_wrong="BNQMDQ shifts without swapping the halves; ODSDPS moves the letters forward; MDQBNR leaves the "
                     "last R unshifted.", seconds=60, verified_by=RECOMP)
r_ = DR2["pairswap3"]
assert r_("5821") == "1845" and r_("7406") == "7093"
ans = inferred([("5821", "1845"), ("7406", "7093")], "3958", r_("3958"), DR2)
assert ans == "2618"
mcq(COD, NC, "Intermediate", "In a certain code, 5821 is written as 1845 and 7406 is written as 7093. How is 3958 "
    "written in that code?", ans, ["6281", "9385", "2617"], "Swap digits in pairs, then add 3",
    "5821: swap the 1st–2nd and 3rd–4th digits → 8512, then add 3 to each digit (keeping only the units digit) → "
    "1845. 7406 → 4760 → 7093. 3958 → 9385 → 2618.",
    ["Check: 5821 → 8512 → 1845; 7406 → 4760 → 7093", "3958 → 9385", "+3 each (9+3 = 12 → 2) ⇒ 2618"],
    why_others_wrong="6281 adds 3 without swapping; 9385 swaps without adding; 2617 adds only 2 to the last digit.",
    seconds=65, verified_by=RECOMP)
alt_ = LRULES["alt2,-2"]
assert alt_("PEARL") == "RCCPN" and alt_("BRANCH") == "DPCLEF"
OPTS = ["BRANCH", "BRUNCH", "BLANCH", "BREACH"]
ans = decoded([("PEARL", "RCCPN")], "DPCLEF", OPTS, "BRANCH")
mcq(COD, LC, "Intermediate", "In a certain code, PEARL is written as RCCPN. Which word is written as DPCLEF in that "
    "code?", ans, OPTS[1:], "Undo the rule letter by letter",
    "PEARL → RCCPN: the 1st, 3rd and 5th letters move 2 places forward (P→R, A→C, L→N) and the 2nd and 4th move 2 "
    "places back (E→C, R→P). To decode, reverse it: D−2 = B, P+2 = R, C−2 = A, L+2 = N, E−2 = C, F+2 = H: BRANCH.",
    ["Rule: odd places +2, even places −2", "Decode DPCLEF: odd −2, even +2 ⇒ B R A N C H"],
    why_others_wrong="BRUNCH would be coded DPWLEF, BLANCH as DJCLEF and BREACH as DPGYEF.", seconds=70,
    verified_by=RECOMP)
assert [alt_(w_) for w_ in OPTS[1:]] == ["DPWLEF", "DJCLEF", "DPGYEF"]

# ---------------------------------------------------------------- Coding: Advanced
rp = LRULES["rev+posL1"]
assert rp("COIN") == "OKRG" and rp("LAMP") == "QODP"
ans = inferred([("COIN", "OKRG"), ("LAMP", "QODP")], "STORE", rp("STORE"))
assert ans == "FTRXX"
mcq(COD, LC, "Advanced", "In a certain code, COIN is written as OKRG and LAMP is written as QODP. How is STORE "
    "written in that code?", ans, ["TVRVJ", "FSPUT", "FTRXW"], "Reverse, then shift by place",
    "COIN reversed is NIOC; then the 1st letter moves 1 place forward, the 2nd 2 places, the 3rd 3 and the 4th 4: "
    "O K R G. LAMP → PMAL → Q O D P. STORE → EROTS → E+1 F, R+2 T, O+3 R, T+4 X, S+5 X = FTRXX.",
    ["Reverse the word", "Shift the k-th letter k places forward", "STORE → EROTS → FTRXX"],
    why_others_wrong="TVRVJ shifts without reversing; FSPUT moves every letter only one place; FTRXW moves the 5th "
                     "letter only 4 places.", seconds=80, verified_by=RECOMP)
wl = NRULES["weighted-left"]
assert wl("DOG") == 55 and wl("BEE") == 27
ans = inferred([("DOG", 55), ("BEE", 27)], "LION", wl("LION"), NRULES)
assert ans == 131
mcq(COD, NC, "Advanced", "In a certain code, DOG is written as 55 and BEE is written as 27. How is LION written in "
    "that code?", str(ans), ["50", "119", "137"], "Each position is multiplied by the letter's place in the word",
    "DOG: 4 × 1 + 15 × 2 + 7 × 3 = 4 + 30 + 21 = 55. BEE: 2 × 1 + 5 × 2 + 5 × 3 = 27. LION: 12 × 1 + 9 × 2 + 15 × 3 + "
    "14 × 4 = 12 + 18 + 45 + 56 = 131.", ["Weights 1, 2, 3, … from the left", "LION = 12 + 18 + 45 + 56 = 131"],
    why_others_wrong="50 is the plain sum of positions; 119 counts the weights from the right; 137 uses 15 for I.",
    natural=int, seconds=80, verified_by=RECOMP)

# ---------------------------------------------------------------- Alphanumeric series: Basic set
SR = "G 4 & P 7 U © 3 M L 8 % E 2 F 6 # W 9 A T 5".split()
assert len(SR) == 22
sid = stimulus("data_table", "Arrangement of 22 elements beginning with G", series_intro(fmt(SR)), None,
               "Number the elements 1 to 22 from the left; the k-th element from the right is the (23 − k)-th from "
               "the left.")
AQ = lambda sub, text, correct, wrongs, concept, expl, steps, **kw: mcq(
    ALN, sub, "Basic", text, correct, wrongs, concept, expl, steps, stimulus=sid, verified_by=RECOMP, **kw)
i_ = 4 - 1 + 6
ans = SR[i_]
AQ(PB, "Which element is 6th to the right of the 4th element from the left end?", ans, near(SR, i_),
   "Add when moving right", f"The 4th element is {SR[3]}. Six places to its right is the 10th element: {ans}.",
   [f"4th = {SR[3]}", f"4 + 6 = 10th ⇒ {ans}"], seconds=35)
hits = [(SR[i], SR[i + 1]) for i in range(len(SR) - 1) if is_l(SR[i]) and is_d(SR[i + 1])]
a, w = count_opts(len(hits))
AQ(SN, "How many letters in the arrangement are immediately followed by a number?", a, w,
   "Look at the right neighbour of every letter",
   "Letter–number pairs: " + ", ".join(f"{x_} {y_}" for x_, y_ in hits) + f" — {len(hits)} in all.",
   ["Scan each letter's right neighbour", "Pairs: " + ", ".join(f"{x_}{y_}" for x_, y_ in hits)], natural=by_num,
   seconds=45)
rv = SR[::-1]
ans = rv[7]
AQ(PB, "If the whole arrangement is written in reverse order, which element will be 8th from the left end?", ans,
   near(rv, 7), "Reversing turns left-end positions into right-end positions",
   f"After reversal, the 8th from the left is the 8th from the right of the original arrangement, i.e. the "
   f"{23 - 8}th from the left: {ans}.", ["8th from the left after reversal = 8th from the right before",
                                         f"22 − 8 + 1 = 15th ⇒ {ans}"], seconds=40)
odd_ = [i for i in range(len(SR)) if is_d(SR[i]) and int(SR[i]) % 2]
hits = [(SR[i], SR[i + 1]) for i in odd_ if i + 1 < len(SR) and is_l(SR[i + 1])]
a, w = count_opts(len(hits))
assert len(hits) == 3
AQ(SN, "How many odd numbers in the arrangement are immediately followed by a letter?", a, w,
   "Check the right neighbour of every odd number",
   "Odd numbers and their right neighbours: " + ", ".join(f"{SR[i]} {SR[i + 1] if i + 1 < len(SR) else '(end)'}"
                                                          for i in odd_) +
   ". Followed by a letter: " + ", ".join(f"{x_} {y_}" for x_, y_ in hits) + f" — {len(hits)}.",
   ["Odd numbers: " + ", ".join(SR[i] for i in odd_), "Keep those with a letter on the right (5 is the last element)"],
   natural=by_num, seconds=45)
iu, iw = SR.index("U"), SR.index("W")
assert (iu + iw) % 2 == 0
ans = SR[(iu + iw) // 2]
AQ(PB, "Which element is exactly midway between U and W in the arrangement?", ans, near(SR, (iu + iw) // 2),
   "Midway = average of the two positions",
   f"U is {ordn(iu + 1)} and W is {ordn(iw + 1)} from the left; ({iu + 1} + {iw + 1}) ÷ 2 = {(iu + iw) // 2 + 1}: "
   f"{ans}.", [f"U = {iu + 1}, W = {iw + 1}", f"Midway = {(iu + iw) // 2 + 1}th ⇒ {ans}"], seconds=40)

# ---------------------------------------------------------------- Alphanumeric series: Intermediate (pattern series)
terms = []
p_ = 2
for d_ in (0, 3, 4, 5, 6):
    p_ += d_
    terms.append(f"{AL[p_ - 1]}{p_}")
ans = terms[-1]
assert terms == ["B2", "E5", "I9", "N14", "T20"]
mcq(ALN, SN, "Intermediate", "Which term should replace the question mark in the series?\n\nB2, E5, I9, N14, ?", ans,
    ["S19", "U21", "T21"], "Letter and number move together",
    "Each number is the alphabetical position of its letter, and the letters move forward by 3, 4, 5, … places: "
    "B(2) +3 → E(5) +4 → I(9) +5 → N(14). The next move is +6: N(14) → T(20). So the term is T20.",
    ["Numbers = positions of the letters", "Gaps: +3, +4, +5 ⇒ next +6", "14 + 6 = 20 = T ⇒ T20"],
    why_others_wrong="S19 adds only 5 again; U21 adds 7; T21 breaks the link between the letter and its position.",
    seconds=45, verified_by=RECOMP)

# ---------------------------------------------------------------- Alphanumeric series: Advanced set
SR = "7 K # 2 E R 9 @ D 4 U £ 6 H Q 1 $ I 8 B * 3 Z O 5 % N 6".split()
assert len(SR) == 28
sid = stimulus("data_table", "Arrangement of 28 elements beginning with 7", series_intro(fmt(SR)), None,
               "Number the elements 1 to 28 from the left (k-th from the right = (29 − k)-th from the left). Vowels: "
               "E, U, I, O. When elements are removed or moved, write out the new arrangement before counting.")
AQ = lambda sub, text, correct, wrongs, concept, expl, steps, **kw: mcq(
    ALN, sub, "Advanced", text, correct, wrongs, concept, expl, steps, stimulus=sid, verified_by=RECOMP, **kw)
nv = [t for t in SR if t not in VOW]
nw = nv[:9] + nv[9:20][::-1] + nv[20:]
ans = nw[-6]
AQ(PB, "If all the vowels are removed from the arrangement and then the 10th to the 20th elements (both inclusive) "
   "of the new arrangement are written in reverse order, which element will be 6th from the right end?", ans,
   near(nw, len(nw) - 6), "Delete, then reverse a block, then count",
   "Without vowels (" + str(len(nv)) + " elements): " + fmt(nv) + ". Reversing the 10th to 20th gives " + fmt(nw) +
   f". The 6th from the right is {ans}.",
   ["Remove E, U, I, O", "Reverse positions 10–20: " + fmt(nw), f"6th from the right ⇒ {ans}"], seconds=110)
hits = [i for i in range(1, len(SR) - 1) if CONS(SR[i]) and is_d(SR[i - 1]) and is_s(SR[i + 1])]
a, w = count_opts(len(hits))
AQ(SN, "In how many places in the arrangement do three consecutive elements follow the pattern 'number, consonant, symbol'?", a, w, "Both neighbours must match",
   "Consonants with a number on the left: " + ", ".join(f"{SR[i - 1]} {SR[i]} {SR[i + 1]}" for i in
                                                         range(1, len(SR) - 1) if CONS(SR[i]) and is_d(SR[i - 1])) +
   ". Of these, followed by a symbol: " + (", ".join(f"{SR[i - 1]} {SR[i]} {SR[i + 1]}" for i in hits) or "none") +
   f" — {len(hits)}.", ["Find consonants with a number on the left", "Keep those with a symbol on the right"],
   natural=by_num, seconds=80)
nums = [(SR[i], SR[i + 1]) for i in range(len(SR) - 1) if is_d(SR[i]) and SR[i + 1] in VOW]
tot = sum(int(x_) for x_, _ in nums)
assert len(nums) >= 2
AQ(SN, "What is the sum of all the numbers in the arrangement that are immediately followed by a vowel?", str(tot),
   [str(tot - 2), str(tot + 4), str(tot + 7)], "Filter by the right neighbour, then add",
   "Numbers followed by a vowel: " + ", ".join(f"{x_} {y_}" for x_, y_ in nums) + f". Sum = "
   + " + ".join(x_ for x_, _ in nums) + f" = {tot}.",
   ["Vowels and their left neighbours", "Add the numbers among them"],
   why_others_wrong="The other totals leave out one qualifying number or add a number that is followed by a "
                    "consonant or symbol.", natural=int, seconds=80)
vi = [i for i, t in enumerate(SR) if t in VOW]
j_ = vi[-2] + 3
ans = SR[j_]
AQ(PB, "Which element is 3rd to the right of the 2nd vowel from the right end?", ans, near(SR, j_),
   "Locate the reference element first",
   "Vowels from the right: " + ", ".join(f"{SR[i]} ({ordn(i + 1)})" for i in vi[::-1]) + f". The 2nd from the right "
   f"is {SR[vi[-2]]} ({ordn(vi[-2] + 1)}); three places to its right is the {ordn(j_ + 1)} element: {ans}.",
   [f"2nd vowel from the right = {SR[vi[-2]]}, {vi[-2] + 1}th from the left", f"{vi[-2] + 1} + 3 = {j_ + 1} ⇒ {ans}"],
   seconds=70)
ps = [x for i in range(0, len(SR), 2) for x in (SR[i + 1], SR[i])]
ans = ps[-11]
AQ(PB, "If the 1st and 2nd elements interchange their places, the 3rd and 4th interchange theirs, and so on to the "
   "end, which element will be 11th from the right end?", ans, near(ps, len(ps) - 11),
   "Swap in pairs, then count from the right",
   "After the pairwise swaps: " + fmt(ps) + f". The 11th from the right is the {len(ps) - 10}th from the left: {ans}.",
   ["Swap each pair: " + fmt(ps), f"11th from the right = {len(ps) - 10}th from the left ⇒ {ans}"], seconds=90)

# ---------------------------------------------------------------- Alphabet test: Intermediate set (one word)
wd = "CONSTABULARY"
sid = stimulus("passage", "Questions on the word CONSTABULARY",
               "Answer the questions on the basis of the word given below.\n\nC O N S T A B U L A R Y", None,
               "Write the alphabetical positions under the letters: C 3, O 15, N 14, S 19, T 20, A 1, B 2, U 21, "
               "L 12, A 1, R 18, Y 25.")
WQ = lambda sub, text, correct, wrongs, concept, expl, steps, **kw: mcq(
    ABT, sub, "Intermediate", text, correct, wrongs, concept, expl, steps, stimulus=sid, verified_by=RECOMP, **kw)
fh = [c for c in wd if pos(c) <= 13]
a, w = count_opts(len(fh))
WQ(LP, "How many letters of the word belong to the first half of the English alphabet (A to M)? Count every "
   "occurrence of a letter.", a, w, "A–M are positions 1 to 13",
   "Letters with positions 1 to 13: " + ", ".join(fh) + f" — {len(fh)} (A occurs twice).",
   ["Positions: " + ", ".join(f"{c} {pos(c)}" for c in wd), "Keep positions ≤ 13"], natural=by_num, seconds=50)
sw_ = sorted(wd)
ans = sw_[-5]
WQ(LP, "If the letters of the word are arranged in alphabetical order from left to right, which letter will be 5th "
   "from the right end?", ans, [sw_[-4], sw_[-6], sw_[-7]], "Sort, then count from the right",
   "Alphabetical order: " + fmt(sw_) + f". From the right: {', '.join(sw_[::-1][:5])} — the 5th is {ans}.",
   ["Sorted: " + fmt(sw_), f"5th from the right ⇒ {ans}"],
   why_others_wrong=f"{sw_[-4]}, {sw_[-6]} and {sw_[-7]} are 4th, 6th and 7th from the right.", seconds=55)
assert ans == "R" and len(set(sw_[-7:-3])) == 4
bl = "".join(wd[i:i + 4][::-1] for i in range(0, 12, 4))
ans = bl[4]
assert bl == "SNOCUBATYRAL" and ans == "U"
WQ(LP, "If the first four letters of the word are written in reverse order, then the next four in reverse order, and "
   "then the last four in reverse order, which letter will be 5th from the left end?", ans, ["T", "B", "C"],
   "Reverse each block of four", "CONS → SNOC, TABU → UBAT, LARY → YRAL: SNOCUBATYRAL. The 5th letter from the left is "
   "U.", ["Blocks: CONS | TABU | LARY", "Reversed: SNOC | UBAT | YRAL", "5th ⇒ U"],
   why_others_wrong="T is the 5th letter of the original word; B is 6th and C is 4th in the new arrangement.",
   seconds=50)
adj = [wd[i:i + 2] for i in range(len(wd) - 1) if abs(pos(wd[i]) - pos(wd[i + 1])) == 1]
a, w = count_opts(len(adj))
assert adj == ["ON", "ST", "AB"]
WQ(PRS, "How many pairs of letters stand next to each other in the word and are also next to each other in the "
   "English alphabet (in either order)?", a, w, "Check every adjacent pair",
   "Adjacent pairs that are consecutive in the alphabet: ON (O 15, N 14), ST (19, 20) and AB (1, 2) — three.",
   ["Adjacent pairs: " + ", ".join(wd[i:i + 2] for i in range(len(wd) - 1)), "Gap of exactly 1: ON, ST, AB"],
   natural=by_num, seconds=55)

# ---------------------------------------------------------------- Alphabet test: Intermediate (standalone)
grp = "".join(AL[i:i + 4][::-1] for i in range(0, 26, 4))
ans = grp[14]
assert grp.startswith("DCBAHGFE") and ans == "N"
mcq(ABT, LP, "Intermediate", "The English alphabet is divided into groups of four letters from the left (ABCD, EFGH, "
    "…, with YZ as the last group), and the letters within each group are written in reverse order. Which letter will "
    "then be 15th from the left end?", ans, ["O", "M", "P"], "Find the group, then the place inside it",
    "The 15th place falls in the 4th group (places 13–16), MNOP, which becomes PONM. Places 13, 14, 15 are P, O, N, so "
    "the 15th letter is N.", ["15 = 4 × 3 + 3 ⇒ 3rd place of the 4th group", "MNOP → PONM ⇒ 3rd = N"],
    why_others_wrong="O is the 15th letter of the normal alphabet; M and P are the other ends of the reversed group.",
    seconds=50, verified_by=RECOMP)
WDS = ["PLASTIC", "PLANET", "PLATFORM", "PLANTAIN", "PLAZA"]
srt = sorted(WDS)
assert srt == ["PLANET", "PLANTAIN", "PLASTIC", "PLATFORM", "PLAZA"]
mcq(ABT, WF, "Intermediate", "If the words PLASTIC, PLANET, PLATFORM, PLANTAIN and PLAZA are arranged in the order in "
    "which they appear in an English dictionary, which word will be in the middle?", srt[2],
    ["PLANTAIN", "PLATFORM", "PLANET"], "Compare letter by letter after the common part",
    "All start with PLA. The 4th letters are S, N, T, N, Z, so the order begins with the two N-words: PLANE-T vs "
    "PLANT-AIN differ at the 5th letter (E < T), so PLANET comes first, then PLANTAIN. Then PLASTIC (S), PLATFORM (T) "
    "and PLAZA (Z). The middle (3rd) word is PLASTIC.",
    ["Common prefix PLA", "4th letters: N, N, S, T, Z", "PLANET < PLANTAIN (E < T)", "Order: " + ", ".join(srt)],
    why_others_wrong="PLANTAIN is 2nd, PLATFORM 4th and PLANET 1st.", seconds=45, verified_by=RECOMP)


# ================================================================================================ BATCH 008
begin("008")
# ---------------------------------------------------------------- Blood relations
F = Family().add("Lakhan", "M").add("Mira", "F").marry("Lakhan", "Mira").add("Kamal", "M", "Lakhan", "Mira")
F.add("Kw", "F").marry("Kamal", "Kw").add("Jyoti", "F", "Kamal", "Kw")
F.check([("Jyoti", "daughter", "Kamal"), ("Lakhan", "father", "Kamal"), ("Mira", "wife", "Lakhan")])
ans = F.rel("Jyoti", "Mira")
assert ans == "granddaughter"
mcq(BLD, DRB, "Basic", "Jyoti is the only daughter of Kamal. Kamal's father is Lakhan, and Lakhan's wife is Mira. How is "
    "Jyoti related to Mira?", cap(ans), ["Daughter", "Niece", "Daughter-in-law"],
    "A son's daughter is a granddaughter",
    "Mira is Lakhan's wife, so she is Kamal's mother. Jyoti is Kamal's daughter, so she is Mira's granddaughter.",
    ["Mira = Kamal's mother", "Jyoti = Kamal's daughter ⇒ Mira's granddaughter"],
    why_others_wrong="Daughter skips a generation; Niece would need Jyoti's parent to be Mira's sibling; "
                     "Daughter-in-law would need Jyoti to be married to Mira's son.", seconds=30, verified_by=RECOMP)
res_ = set()
for dg in ("M", "F"):
    F = Family().add("Cp", "M").add("Cm", "F").marry("Cp", "Cm").add("C", "F", "Cp", "Cm").add("D", dg, "Cp", "Cm")
    F.add("B", "M").marry("B", "C").add("A", "M", "B", "C")
    assert F.rel("A", "B") == "son" and F.rel("B", "C") == "husband" and F.rel("C", "D") == "sister"
    res_.add(F.rel("D", "A"))
assert res_ == {"uncle", "aunt"}
mcq(BLD, CDB, "Intermediate",
    "In a certain code:\n'P # Q' means 'P is a child of Q';\n'P $ Q' means 'P is the sister of Q';\n'P @ Q' means 'P is "
    "the husband of Q'.\n\nIf 'A # B @ C $ D', how is D related to A?", "Cannot be determined",
    ["Maternal uncle", "Maternal aunt", "Cousin"], "Check whether every gender needed is given",
    "A is B's child and B is C's husband, so C is A's mother. C is D's sister, so D is a sibling of A's mother. D's "
    "gender is not given, so D may be A's maternal uncle or maternal aunt: the exact relation cannot be determined.",
    ["A # B, B @ C ⇒ C is A's mother", "C $ D ⇒ D is a sibling of A's mother", "D's gender unknown ⇒ uncle or aunt"],
    why_others_wrong="Uncle and Aunt each assume a gender the code never states; a cousin would be a child of D.",
    seconds=55, verified_by=RECOMP)
F = Family().add("Ojas", "M").add("Pallavi", "F").marry("Ojas", "Pallavi").add("Qadir", "M", "Ojas", "Pallavi")
F.add("Radha", "F", "Ojas", "Pallavi").add("Sameer", "M").marry("Radha", "Sameer")
bil = [p for p in F.g if F.rel(p, "Qadir") == "brother-in-law"]
assert bil == ["Sameer"] and "Qadir" not in F.sp
ans = F.rel("Sameer", "Pallavi")
assert ans == "son-in-law"
mcq(BLD, FPZ, "Intermediate", "Ojas and Pallavi are a married couple with exactly two children, Qadir and Radha. Qadir "
    "is unmarried. Sameer is Qadir's only brother-in-law. How is Sameer related to Pallavi?", cap(ans),
    ["Son", "Nephew", "Brother-in-law"], "An unmarried man's brother-in-law is his sister's husband",
    "Qadir is unmarried, so his brother-in-law can only be the husband of his sister. His only sibling is Radha, so "
    "Sameer is Radha's husband. The husband of Pallavi's daughter is Pallavi's son-in-law.",
    ["Qadir unmarried ⇒ brother-in-law = sister's husband", "Sameer = Radha's husband", "Daughter's husband ⇒ "
                                                                                       "son-in-law"],
    why_others_wrong="Pallavi's only son is Qadir; Sameer is not the child of Pallavi's sibling; he is Qadir's "
                     "brother-in-law, not Pallavi's.", seconds=55, verified_by=RECOMP)
F = Family().add("Lh", "M").add("Lata", "F").marry("Lh", "Lata").add("Mukul", "M", "Lh", "Lata")
F.add("Nandita", "F", "Lh", "Lata").add("Ruchi", "F").marry("Mukul", "Ruchi").add("Ishaan", "M", "Mukul", "Ruchi")
F.add("Om", "M").marry("Om", "Nandita").add("Parth", "M", "Om", "Nandita")
F.check([("Ruchi", "daughter-in-law", "Lata"), ("Ishaan", "son", "Ruchi"), ("Om", "son-in-law", "Lh"),
         ("Parth", "son", "Nandita")])
assert [c for c in F.children("Lata") if F.g[c] == "M"] == ["Mukul"]
ans = F.rel("Parth", "Ruchi")
assert ans == "nephew" and F.rel("Ishaan", "Parth") == "cousin"
mcq(BLD, FPZ, "Advanced", "Ruchi is the daughter-in-law of Lata, who has only one son. Nandita is Lata's only daughter. "
    "Om is the son-in-law of Lata's husband, and Parth is the son of Om and Nandita. Ishaan is Ruchi's son. Every "
    "person mentioned has only one spouse. How is Parth related to Ruchi?", cap(ans),
    ["Son", "Cousin", "Brother-in-law"], "Find both couples, then link through Lata's children",
    "Ruchi is the wife of Lata's only son. Om, the son-in-law of Lata's husband, is the husband of Lata's only "
    "daughter Nandita. Parth is Nandita's son, i.e. the son of Ruchi's husband's sister: Ruchi's nephew (and Ishaan's "
    "cousin).", ["Ruchi = wife of Lata's only son", "Nandita = Lata's only daughter = sister of Ruchi's husband",
                 "Parth = Nandita's son ⇒ Ruchi's nephew"],
    why_others_wrong="Ruchi's son is Ishaan; Parth is Ishaan's cousin, not Ruchi's; he is a generation below Ruchi, "
                     "so not her brother-in-law.", seconds=80, verified_by=RECOMP)

# ---------------------------------------------------------------- Direction: Basic set (benches in a park)
PT = {"A": (0, 0), "B": (0, 15)}
PT["C"] = (PT["B"][0] + 20, PT["B"][1])
PT["D"] = (PT["C"][0], PT["C"][1] - 15)
PT["E"] = (PT["D"][0] - 10, PT["D"][1])
sid = stimulus("puzzle", "Five benches in a park", "Five benches A, B, C, D and E stand in a park.", [
    ("Bench B is 15 m north of bench A.", (), None), ("Bench C is 20 m east of bench B.", (), None),
    ("Bench D is 15 m south of bench C.", (), None), ("Bench E is 10 m west of bench D.", (), None)],
    "Take A at (0, 0): B (0, 15), C (20, 15), D (20, 0), E (10, 0).")
MAP8 = "A (0, 0), B (0, 15), C (20, 15), D (20, 0), E (10, 0)"
DQ = lambda sub, text, correct, wrongs, concept, expl, steps, **kw: mcq(
    DIR, sub, "Basic", text, correct, wrongs, concept, expl, steps, stimulus=sid, verified_by=RECOMP, **kw)
c, w, why = dd_wrongs(*PT["C"], "m", 35)
assert c == "25 m, North-East"
DQ(PP, "What is the straight-line distance between benches A and C, and in which direction is C from A?", c, w,
   "A 15-20-25 triangle", "C is 20 m east and 15 m north of A: √(400 + 225) = 25 m, north-east.",
   [MAP8, "C − A = (20, 15)", "√(20² + 15²) = 25 m, North-East"], why_others_wrong=why, seconds=40)
ans = compass(PT["E"][0] - PT["B"][0], PT["E"][1] - PT["B"][1])
assert ans == "South-East"
DQ(PP, "In which direction is bench E with respect to bench B?", ans, ["North-West", "South-West", "East"],
   "Signs of the two components", "E (10, 0) − B (0, 15) = (10, −15): east and south, so E is south-east of B.",
   [MAP8, "E − B = (10, −15) ⇒ South-East"],
   why_others_wrong="North-West is B's direction from E; South-West takes E as west of A; East ignores the 15 m "
                    "north–south gap.", seconds=35)
dd_ = {k: dist(*v) for k, v in PT.items() if k != "A"}
ans = min(dd_, key=lambda k: PT[k][0] ** 2 + PT[k][1] ** 2)
assert ans == "E" and dd_ == {"B": "15", "C": "25", "D": "20", "E": "10"}
DQ(PP, "Which bench is nearest to bench A?", ans, ["B", "D", "C"], "Compare straight-line distances",
   "Distances from A: B 15 m, C 25 m, D 20 m, E 10 m. E is nearest.", [MAP8, "AB 15, AC 25, AD 20, AE 10"],
   why_others_wrong="B is 15 m, D 20 m and C 25 m from A.", seconds=40)

# ---------------------------------------------------------------- Direction: Basic (standalone)
sun_eve, shadow_eve = "W", "E"
mcq(DIR, SH_, "Basic", "One evening before sunset, Arjun walked straight towards his own shadow. In which direction was "
    "he walking?", NAME[shadow_eve], ["West", "North", "South"], "Evening sun is in the west",
    "Before sunset the sun is in the west, so shadows point east. Walking towards his shadow, Arjun was walking east.",
    ["Evening: sun in the west", "Shadow points away from the sun ⇒ east"],
    why_others_wrong="West is towards the sun; North and South are at right angles to the shadow.", seconds=30,
    verified_by=RECOMP)
MV = [(None, 9), ("L", 12)]
x, y = walk("S", MV)
assert (x, y) == (12, -9)
c, w, why = dd_wrongs(x, y, "km", 21)
mcq(DIR, DD, "Basic", "Pooja walks 9 km towards the south, then turns left and walks 12 km. How far is she from her "
    "starting point, and in which direction?", c, w, "Left of south is east",
    "Facing south, a left turn makes her face east. She ends 12 km east and 9 km south of the start: √(144 + 81) = "
    "15 km, south-east.", walk_trace("S", MV, "km") + ["√(12² + 9²) = 15 km, South-East"], why_others_wrong=why,
    seconds=35, verified_by=RECOMP)

# ---------------------------------------------------------------- Direction: Intermediate set (robot programs)


def run_prog(prog, start="N"):
    f, x, y = start, 0, 0
    for tok in prog.split():
        if tok == "R" or tok == "L":
            f = turn(f, tok)
        elif tok == "B":
            f = turn(turn(f, "R"), "R")
        else:
            d = int(tok[1:])
            x, y = x + VEC[f][0] * d, y + VEC[f][1] * d
    return x, y, f


sid = stimulus("passage", "A robot's movement instructions",
               "A robot always starts at point O facing north and follows a program of instructions from left to "
               "right:\nF n — move n metres forward in the direction it is facing;\nR — turn 90° to its right;\n"
               "L — turn 90° to its left;\nB — turn about (180°).\nTurns do not move the robot.", None,
               "Track the facing after every turn and the position (east, north) after every F.")
RQ = lambda sub, text, correct, wrongs, concept, expl, steps, **kw: mcq(
    DIR, sub, "Intermediate", text, correct, wrongs, concept, expl, steps, stimulus=sid, verified_by=RECOMP, **kw)
x, y, f = run_prog("F6 R F8 L F4 B F2")
assert (x, y) == (8, 8)
c, w, why = dd_wrongs(x, y, "m", 20)
RQ(DD, "Where is the robot, with respect to O, at the end of the program 'F6 R F8 L F4 B F2'?", c, w,
   "Equal east and north parts give a diagonal", "North 6 → (0, 6); right ⇒ east 8 → (8, 6); left ⇒ north 4 → (8, 10); "
   "about turn ⇒ south 2 → (8, 8). It is 8 m east and 8 m north of O: 8√2 m, north-east.",
   ["(0, 6) → (8, 6) → (8, 10) → (8, 8)", "√(8² + 8²) = 8√2 m, North-East"], why_others_wrong=why, seconds=60)
x, y, f = run_prog("F4 L F7 B F3 R R F2")
assert NAME[f] == "West"
RQ(DD, "Which direction is the robot facing at the end of the program 'F4 L F7 B F3 R R F2'?", NAME[f],
   ["North", "East", "South"], "Only the turns change the facing",
   "Facing: north → L ⇒ west → B ⇒ east → R ⇒ south → R ⇒ west. The moves do not change the facing, so it ends "
   "facing west.", ["N →L W →B E →R S →R W"],
   why_others_wrong="East is the facing before the last two right turns; South is after only one of them; North "
                    "ignores the about-turn.", seconds=55)
base_ = "F10 R F6 R F10 R"
x, y, f = run_prog(base_)
assert (x, y, f) == (6, 0, "W")
fits = [o for o in ("F6", "F10", "B F6", "L F6") if run_prog(base_ + " " + o)[:2] == (0, 0)]
assert fits == ["F6"]
RQ(PP, f"The program '{base_}' is to be completed with one more step so that the robot ends exactly at O. Which step "
   "should be added?", "F6", ["F10", "B F6", "L F6"], "Find the position and the facing first",
   "North 10 → (0, 10); right ⇒ east 6 → (6, 10); right ⇒ south 10 → (6, 0); right ⇒ facing west. O is 6 m to its "
   "west, so 'F6' brings it back.", ["Position (6, 0), facing west", "O is 6 m west ⇒ F6"],
   why_others_wrong="F10 overshoots by 4 m; 'B F6' moves it east, away from O; 'L F6' moves it south.", seconds=65)

# ---------------------------------------------------------------- Direction: Advanced set (diagonal relations)
PT = {"P": (0, 0)}
PT["Q"] = (PT["P"][0] + 4, PT["P"][1] + 4)
PT["R"] = (PT["Q"][0], PT["Q"][1] - 7)
PT["S"] = (PT["R"][0] - 8, PT["R"][1])
PT["T"] = (PT["S"][0], PT["S"][1] + 9)
PT["U"] = (PT["T"][0] + 4, PT["T"][1] - 4)
PT["V"] = (PT["P"][0], PT["P"][1] - 3)
assert PT == {"P": (0, 0), "Q": (4, 4), "R": (4, -3), "S": (-4, -3), "T": (-4, 6), "U": (0, 2), "V": (0, -3)}
sid = stimulus("puzzle", "Seven points with diagonal steps", "Seven points P, Q, R, S, T, U and V lie on flat ground.",
               [("Q is 4√2 m to the north-east of P.", (), None), ("R is 7 m to the south of Q.", (), None),
                ("S is 8 m to the west of R.", (), None), ("T is 9 m to the north of S.", (), None),
                ("U is 4√2 m to the south-east of T.", (), None), ("V is 3 m to the south of P.", (), None)],
               "A diagonal step of k√2 m moves k m along each axis. With P at (0, 0): Q (4, 4), R (4, −3), S (−4, −3), "
               "T (−4, 6), U (0, 2), V (0, −3).")
MAP8B = "P (0, 0), Q (4, 4), R (4, −3), S (−4, −3), T (−4, 6), U (0, 2), V (0, −3)"
AQ = lambda sub, text, correct, wrongs, concept, expl, steps, **kw: mcq(
    DIR, sub, "Advanced", text, correct, wrongs, concept, expl, steps, stimulus=sid, verified_by=RECOMP, **kw)
c, w, why = dd_wrongs(*PT["R"], "m", 4 + 4 + 7)
assert c == "5 m, South-East"
AQ(PP, "What is the straight-line distance between P and R, and in which direction is R from P?", c, w,
   "Convert the diagonal step first",
   "Q is 4 m east and 4 m north of P; R is 7 m south of Q, so R = (4, −3): 4 m east and 3 m south of P, 5 m away, "
   "south-east.", [MAP8B, "R − P = (4, −3)", "√(16 + 9) = 5 m, South-East"], why_others_wrong=why, seconds=80)
mid = ((PT["R"][0] + PT["S"][0]) / 2, (PT["R"][1] + PT["S"][1]) / 2)
ans = [k for k, v in PT.items() if v == mid]
assert ans == ["V"]
AQ(PP, "Which point lies exactly midway between R and S?", "V", ["P", "U", "T"], "Midpoint of a horizontal segment",
   "R (4, −3) and S (−4, −3) are on the same east–west line; their midpoint is (0, −3), which is V (3 m south of P).",
   [MAP8B, "Midpoint of R and S = (0, −3) = V"], why_others_wrong="P is 3 m north of that midpoint, U 5 m north, and "
                                                                   "T is far to the west.", seconds=75)
ans = compass(PT["T"][0] - PT["Q"][0], PT["T"][1] - PT["Q"][1])
assert ans == "North-West"
AQ(PP, "In which direction is T with respect to Q?", ans, ["South-West", "South-East", "West"],
   "Signs of the two components",
   "T (−4, 6) − Q (4, 4) = (−8, 2): 8 m west and 2 m north, so T is north-west of Q.",
   [MAP8B, "T − Q = (−8, +2) ⇒ North-West"],
   why_others_wrong="South-West misreads T as below Q; South-East is the direction of Q from T; West ignores the 2 m "
                    "north component.", seconds=75)
dx, dy = PT["U"][0] - PT["V"][0], PT["U"][1] - PT["V"][1]
assert (dx, dy) == (0, 5)
AQ(PP, "What is the shortest distance between U and V, and in which direction is U from V?", "5 m, North",
   ["5 m, South", "4√2 m, North-East", "9 m, North"], "Points on one north–south line",
   "U = T + (4, −4) = (0, 2), so U is 2 m north of P; V is 3 m south of P. Both lie on the north–south line through P, "
   "and U is 2 + 3 = 5 m north of V.", [MAP8B, "U − V = (0, 5) ⇒ 5 m, North"],
   why_others_wrong="5 m, South is V's direction from U; 4√2 m treats U as a diagonal step from V; 9 m adds T's "
                    "north step instead of U's position.", seconds=85)

# ---------------------------------------------------------------- Direction: Advanced (standalone)
(x, y), tr_ = walk_deg("E", [(135, 6), (-135, 14)])
assert (x, y) == (8, -6)
c, w, why = dd_wrongs(x, y, "m", 20)
mcq(DIR, SH_, "Advanced", "Just before sunset, Ravi stood facing his own shadow. He then turned 135° clockwise and "
    "walked 6√2 m, and then turned 135° anticlockwise and walked 14 m. How far is he now from where he stood, and in "
    "which direction?", c, w, "Fix the first facing from the shadow",
    "Before sunset the sun is in the west and the shadow points east, so Ravi faced east. 135° clockwise from east is "
    "south-west: 6√2 m moves him 6 m west and 6 m south → (−6, −6). 135° anticlockwise from south-west is east: 14 m "
    "→ (8, −6). He is 8 m east and 6 m south of the start: 10 m, south-east.",
    ["Facing the shadow at sunset ⇒ facing east"] + tr_ + ["√(8² + 6²) = 10 m, South-East"],
    why_others_wrong=why, seconds=100, verified_by=RECOMP)
Y_, X_ = (0, 0), (30, 0)
Z_ = (30, int(math.isqrt(50 ** 2 - 30 ** 2)))
W_ = ((Z_[0] + Y_[0]) / 2, (Z_[1] + Y_[1]) / 2)
dx, dy = W_[0] - X_[0], W_[1] - X_[1]
assert Z_ == (30, 40) and (dx, dy) == (-15, 20) and dist(-15, 20) == "25"
mcq(DIR, PP, "Advanced", "Town X is 30 km east of town Y. Town Z is due north of X and is 50 km from Y in a straight "
    "line. A car drives from Z straight towards Y and stops exactly halfway, at W. How far is W from X, and in which "
    "direction?", "25 km, North-West", ["25 km, North-East", "20 km, North-West", "35 km, North-West"],
    "Find Z first, then the midpoint",
    "Z is north of X with YZ = 50 and YX = 30, so XZ = √(50² − 30²) = 40 km: Z = (30, 40) with Y at (0, 0). The "
    "midpoint W of ZY is (15, 20). From X (30, 0), W is 15 km west and 20 km north: √(225 + 400) = 25 km, north-west.",
    ["XZ = √(2500 − 900) = 40 ⇒ Z (30, 40)", "W = midpoint of Z and Y = (15, 20)", "W − X = (−15, 20) ⇒ 25 km, "
                                                                                     "North-West"],
    why_others_wrong="North-East forgets that W is west of X; 20 km is only the north part; 35 km adds the two parts.",
    seconds=110, verified_by=RECOMP)

# ---------------------------------------------------------------- Coding: Basic
oe = LRULES["oddeven+0"]
assert oe("PLANET") == "PAELNT"
ans = inferred([("PLANET", "PAELNT")], "GARDEN", oe("GARDEN"))
assert ans == "GREADN"
mcq(COD, LC, "Basic", "In a certain code, PLANET is written as PAELNT. How is GARDEN written in that code?", ans,
    ["GAREDN", "NEDRAG", "AGDRNE"], "Odd places first, then even places",
    "PLANET: the letters in the 1st, 3rd and 5th places (P, A, E) are written first, followed by those in the 2nd, 4th "
    "and 6th places (L, N, T): PAELNT. GARDEN: G, R, E then A, D, N = GREADN.",
    ["Odd places: P A E; even places: L N T", "GARDEN ⇒ G R E + A D N"],
    why_others_wrong="GAREDN only swaps two middle letters; NEDRAG reverses the word; AGDRNE swaps neighbouring "
                     "letters.", seconds=35, verified_by=RECOMP)
pr_ = NRULES["product"]
assert pr_("BED") == 40 and pr_("DOG") == 420
ans = inferred([("BED", 40), ("DOG", 420)], "HEN", pr_("HEN"), NRULES)
assert ans == 560
mcq(COD, NC, "Basic", "In a certain code, BED is written as 40 and DOG is written as 420. How is HEN written in that "
    "code?", str(ans), ["27", "112", "520"], "Multiply the alphabetical positions",
    "BED: 2 × 5 × 4 = 40. DOG: 4 × 15 × 7 = 420. HEN: 8 × 5 × 14 = 560.",
    ["Check: 2 × 5 × 4 = 40; 4 × 15 × 7 = 420", "HEN: 8 × 5 × 14 = 560"],
    why_others_wrong="27 adds the positions; 112 multiplies only the first and last letters; 520 takes N as 13.",
    natural=int, seconds=40, verified_by=RECOMP)

# ---------------------------------------------------------------- Coding: Intermediate set (codes by number of vowels)
TAB8 = {"A": "6", "B": "#", "D": "3", "E": "9", "G": "%", "I": "1", "K": "&", "L": "4", "M": "@", "N": "7", "O": "2",
        "P": "$", "R": "8", "S": "©", "T": "5", "U": "★"}


def enc8(w):
    c = [TAB8[ch] for ch in w]
    nv_ = sum(ch in VOW for ch in w)
    if nv_ == 1:
        c = ["◎" if ch in VOW else x for ch, x in zip(w, c)]
    elif nv_ == 2:
        c[0], c[-1] = c[-1], c[0]
    elif nv_ >= 3:
        c = ["◇" if ch not in VOW and i + 1 < len(w) and w[i + 1] in VOW else c[i] for i, ch in enumerate(w)]
    return "".join(c)


plain8 = lambda w: "".join(TAB8[ch] for ch in w)
sid = stimulus("data_table", "Letter codes that depend on the number of vowels",
               "Each letter is coded as shown below, subject to the conditions that follow.\n\n"
               + table(["Letter"] + list(TAB8), ["Code"] + list(TAB8.values())) +
               "\n\nConditions (A, E, I, O and U are vowels):\n(i) If the word has exactly one vowel, that vowel is "
               "coded as ◎.\n(ii) If the word has exactly two vowels, the codes of its first and last letters are "
               "interchanged.\n(iii) If the word has three or more vowels, every consonant that is immediately "
               "followed by a vowel is coded as ◇.\nAll other letters are coded as in the table.", None,
               "Count the vowels of the word first; exactly one condition (or none, for a word without vowels) "
               "applies.")
CQ = lambda sub, text, correct, wrongs, concept, expl, steps, **kw: mcq(
    COD, sub, "Intermediate", text, correct, wrongs, concept, expl, steps, stimulus=sid, verified_by=RECOMP, **kw)
for w_, e_ in (("SPRINT", "©$8◎75"), ("MANGO", "267%@"), ("TOMATO", "◇2◇6◇2"), ("MINUTE", "◇1◇★◇9"),
               ("BOARD", "3268#")):
    assert enc8(w_) == e_, (w_, enc8(w_))
CQ(LC, "What is the code for 'SPRINT'?", enc8("SPRINT"), [plain8("SPRINT"), "5$8◎7©", "©$8◇75"],
   "One vowel: condition (i)", "SPRINT has one vowel (I), so only I is coded as ◎; the rest follow the table: S ©, "
   "P $, R 8, N 7, T 5 ⇒ ©$8◎75.", ["Vowels: I only ⇒ condition (i)", "S © P $ R 8 I ◎ N 7 T 5"],
   why_others_wrong="©$8175 ignores the condition; 5$8◎7© also swaps the end codes (condition (ii)); ©$8◇75 uses the "
                    "symbol of condition (iii).", seconds=55)
CQ(LC, "What is the code for 'MANGO'?", enc8("MANGO"), [plain8("MANGO"), "@◎7%◎", "2@7%6"],
   "Two vowels: condition (ii)", "MANGO has two vowels (A, O), so the codes of the first and last letters are "
   "interchanged: table codes @ 6 7 % 2 become 2 6 7 % @.", ["Vowels: A, O ⇒ condition (ii)",
                                                            "@67%2 → swap ends ⇒ 267%@"],
   why_others_wrong="@67%2 ignores the condition; @◎7%◎ applies condition (i); 2@7%6 swaps the wrong codes.",
   seconds=55)
CQ(LC, "What is the code for 'TOMATO'?", enc8("TOMATO"), [plain8("TOMATO"), "◇2◇6◇◇", "52@652"[::-1]],
   "Three vowels: condition (iii)", "TOMATO has three vowels (O, A, O). Each consonant followed by a vowel — T, M and "
   "T — becomes ◇; the vowels keep their codes (O 2, A 6): ◇2◇6◇2.",
   ["Vowels: O, A, O ⇒ condition (iii)", "T→◇, O 2, M→◇, A 6, T→◇, O 2"],
   why_others_wrong="52@652 ignores the condition; ◇2◇6◇◇ wrongly changes the last vowel; 256@25 reverses the plain "
                    "code.", seconds=60)
OPTS = ["MINUTE", "MINUET", "MANURE", "IMPUTE"]
codes_ = {o: enc8(o) for o in OPTS}
assert [o for o in OPTS if codes_[o] == "◇1◇★◇9"] == ["MINUTE"]
CQ(LC, "Which of the following words is coded as '◇1◇★◇9'?", "MINUTE", OPTS[1:], "Code every option",
   "MINUTE (3 vowels): M, N and T are each followed by a vowel ⇒ ◇1◇★◇9. MINUET → " + codes_["MINUET"] +
   ", MANURE → " + codes_["MANURE"] + ", IMPUTE → " + codes_["IMPUTE"] + ".",
   ["All four words have three vowels ⇒ condition (iii)", "Only MINUTE gives ◇1◇★◇9"],
   why_others_wrong="MINUET ends in T after a vowel, MANURE has A (6) as its 2nd letter, and IMPUTE starts with the "
                    "vowel I.", seconds=70)
CQ(LC, "What is the code for 'BOARD'?", enc8("BOARD"), [plain8("BOARD"), "#◎◎83", "3◇683"],
   "Two vowels: condition (ii)", "BOARD has two vowels (O, A), so the first and last codes are interchanged: table "
   "codes # 2 6 8 3 become 3 2 6 8 #.", ["Vowels: O, A ⇒ condition (ii)", "#2683 → swap ends ⇒ 3268#"],
   why_others_wrong="#2683 ignores the condition; #◎◎83 applies condition (i) to both vowels; 3◇683 mixes in "
                    "condition (iii).", seconds=55)

# ---------------------------------------------------------------- Coding: Intermediate set (grid code)
KEY = "PLANET"
GRID = list(KEY) + [c for c in AL if c not in KEY and c != "Z"]
assert len(GRID) == 25
RC = {c: f"{i // 5 + 1}{i % 5 + 1}" for i, c in enumerate(GRID)}
gcode = lambda w: " ".join(RC[c] for c in w)
rows_ = [[str(r + 1)] + GRID[r * 5:(r + 1) * 5] for r in range(5)]
sid = stimulus("data_table", "A 5 × 5 letter grid code",
               "In a certain code, each letter is written as a two-digit number: its row number followed by its column "
               "number in the grid below (Z is not used).\n\n" + table(["Row \\ Column", "1", "2", "3", "4", "5"],
                                                                        rows_), None,
               "Read the row first, then the column. For example, C is in row 2, column 3, so C = 23.")
GQ = lambda sub, text, correct, wrongs, concept, expl, steps, **kw: mcq(
    COD, sub, "Intermediate", text, correct, wrongs, concept, expl, steps, stimulus=sid, verified_by=RECOMP, **kw)
ans = gcode("WHITE")
assert ans == "53 32 33 21 15"
GQ(NC, "How is 'WHITE' written in this code?", ans, ["35 23 33 12 51", "53 32 33 21 51", "53 33 32 21 15"],
   "Row first, then column", "W is in row 5, column 3 (53); H row 3, column 2 (32); I 33; T row 2, column 1 (21); E "
   "row 1, column 5 (15).", ["W 53, H 32, I 33, T 21, E 15"],
   why_others_wrong="35 23 33 12 51 reads column before row; the third option reverses only E; the fourth swaps H and "
                    "I.", seconds=55)
OPTS = ["BOLD", "BALD", "BOND", "BOLT"]
assert [o for o in OPTS if gcode(o) == "22 42 12 24"] == ["BOLD"]
GQ(NC, "Which word is written as '22 42 12 24' in this code?", "BOLD", OPTS[1:], "Decode each pair",
   "22 = row 2, column 2 = B; 42 = O; 12 = L; 24 = D: BOLD.", ["22 B, 42 O, 12 L, 24 D"],
   why_others_wrong="BALD would be 22 13 12 24, BOND 22 42 14 24 and BOLT 22 42 12 21.", seconds=50)
assert [gcode(o) for o in OPTS[1:]] == ["22 13 12 24", "22 42 14 24", "22 42 12 21"]
tot = sum(int(d) for d in gcode("GRAPE").replace(" ", ""))
assert gcode("GRAPE") == "31 44 13 11 15" and tot == 24
GQ(NC, "What is the sum of all the digits in the code for 'GRAPE'?", str(tot), ["22", "26", "29"],
   "Code first, then add the digits", "G 31, R 44, A 13, P 11, E 15. Digit sum: 3 + 1 + 4 + 4 + 1 + 3 + 1 + 1 + 1 + 5 = "
   "24.", ["GRAPE ⇒ 31 44 13 11 15", "Sum of digits = 24"],
   why_others_wrong="22 drops a digit of R's code; 26 takes A as 33; 29 takes E as 55.", natural=int, seconds=60)

# ---------------------------------------------------------------- Coding: Intermediate (standalone)
ps1 = LRULES["pairswap+1"]
assert ps1("BANKER") == "BCLOSF" and ps1("TICKET") == "JULDUF"
ans = inferred([("BANKER", "BCLOSF"), ("TICKET", "JULDUF")], "MIRROR", ps1("MIRROR"))
assert ans == "JNSSSP"
mcq(COD, LC, "Intermediate", "In a certain code, BANKER is written as BCLOSF and TICKET is written as JULDUF. How is "
    "MIRROR written in that code?", ans, ["NJSSPS", "HLQQQN", "JNSSSQ"], "Swap neighbouring pairs, then shift",
    "BANKER → swap each pair: AB KN RE → each letter one place forward: BC LO SF. TICKET → IT KC TE → JU LD UF. MIRROR "
    "→ IM RR RO → JN SS SP.", ["Swap pairs: MI RR OR → IM RR RO", "+1 each ⇒ JNSSSP"],
    why_others_wrong="NJSSPS shifts without swapping; HLQQQN moves the letters back; JNSSSQ shifts the last letter "
                     "twice.", seconds=60, verified_by=RECOMP)

# ---------------------------------------------------------------- Coding: Advanced (mixed letters and digits)
RANK = {v: str(i + 1) for i, v in enumerate("AEIOU")}
VMAPS = {"rank": lambda c: RANK[c], "position": lambda c: str(pos(c)), "next": lambda c: shift(c, 1),
         "prev": lambda c: shift(c, -1), "same": lambda c: c, "position-mod-10": lambda c: str(pos(c) % 10)}
MIXED = {}
for vn, vf in VMAPS.items():
    for k_ in range(-6, 7):
        for rv_ in (False, True):
            MIXED[f"{vn},{k_},{rv_}"] = lambda w, vf=vf, k_=k_, rv_=rv_: "".join(
                vf(c) if c in VOW else shift(c, k_) for c in (w[::-1] if rv_ else w))
mx = MIXED["rank,-4,False"]
assert mx("PLANET") == "LH1J2P" and mx("CABIN") == "Y1X3J"
ans = inferred([("PLANET", "LH1J2P"), ("CABIN", "Y1X3J")], "MOUSE", mx("MOUSE"), MIXED)
assert ans == "I45O2"
mcq(COD, LC, "Advanced", "In a certain code, PLANET is written as LH1J2P and CABIN is written as Y1X3J. How is MOUSE "
    "written in that code?", ans, ["I1521O5", "I54O2", "Q45W2"], "Vowels and consonants follow different rules",
    "Consonants move 4 places back (P→L, L→H, N→J, T→P; C→Y, B→X, N→J). Vowels become their place among the vowels "
    "A 1, E 2, I 3, O 4, U 5 (A→1, E→2; A→1, I→3). MOUSE: M→I, O→4, U→5, S→O, E→2 = I45O2.",
    ["Consonants: −4", "Vowels: A1 E2 I3 O4 U5", "M I, O 4, U 5, S O, E 2"],
    why_others_wrong="I1521O5 uses alphabetical positions for the vowels; I54O2 swaps O and U; Q45W2 moves the "
                     "consonants forward.", seconds=85, verified_by=RECOMP)

# ---------------------------------------------------------------- Alphanumeric series: Basic (pattern)
terms = [f"{n * n}{AL[n * n - 1]}" for n in range(1, 6)]
assert terms == ["1A", "4D", "9I", "16P", "25Y"]
mcq(ALN, SN, "Basic", "Which term should replace the question mark in the series?\n\n1A, 4D, 9I, 16P, ?", terms[-1],
    ["25X", "24Y", "36Y"], "Squares and the letters at those places",
    "The numbers are 1², 2², 3², 4², so the next is 5² = 25. Each letter is the letter at that place in the alphabet "
    "(A 1, D 4, I 9, P 16), so the 25th letter Y goes with 25: 25Y.",
    ["Numbers: 1, 4, 9, 16 ⇒ 25", "Letter = 25th letter = Y"],
    why_others_wrong="25X takes the 24th letter; 24Y breaks the square pattern; 36Y skips a square.", seconds=35,
    verified_by=RECOMP)

# ---------------------------------------------------------------- Alphabet test: Basic (standalone)
r10 = 26 - 10 + 1
ans = AL[r10 - 6 - 1]
assert AL[r10 - 1] == "Q" and ans == "K"
mcq(ABT, LP, "Basic", "Which letter is 6th to the left of the 10th letter from the right end of the English alphabet?",
    ans, ["J", "L", "W"], "Convert the right-end position first",
    "The 10th letter from the right is the 26 − 10 + 1 = 17th from the left, Q. Six places to its left is the 11th "
    "letter: K.", ["10th from the right = 17th = Q", "17 − 6 = 11th ⇒ K"],
    why_others_wrong="J and L are one place off; W is 6 places to the right of Q.", seconds=30, verified_by=RECOMP)
a_, b_ = pos("H") + 4, pos("W") - 3
n_ = b_ - a_ - 1
assert (AL[a_ - 1], AL[b_ - 1], n_) == ("L", "T", 7)
mcq(ABT, LP, "Basic", "How many letters of the English alphabet are there between the letter that is 4th to the right "
    "of H and the letter that is 3rd to the left of W?", str(n_), ["6", "8", "9"], "Letters between = difference − 1",
    "4th to the right of H (8) is the 12th letter, L. 3rd to the left of W (23) is the 20th letter, T. Between L and T "
    "lie M, N, O, P, Q, R, S: 20 − 12 − 1 = 7 letters.", ["H + 4 = 12 = L; W − 3 = 20 = T", "20 − 12 − 1 = 7"],
    why_others_wrong="8 is the difference of the positions; 6 subtracts one too many; 9 counts both end letters.",
    natural=int, seconds=35, verified_by=RECOMP)
SRC = "PERSONALITY"
can = lambda wd_: all(wd_.count(c) <= SRC.count(c) for c in set(wd_))
OPTS = ["TERRAIN", "PAINTER", "SENATOR", "PLASTER"]
assert [can(x) for x in OPTS] == [False, True, True, True]
mcq(ABT, WF, "Basic", "Which of the following words CANNOT be formed using the letters of the word 'PERSONALITY', each "
    "letter used no more often than it appears in PERSONALITY?", OPTS[0], OPTS[1:],
    "Count repeated letters as well", "PERSONALITY has eleven different letters, each only once: P, E, R, S, O, N, A, "
    "L, I, T, Y. TERRAIN needs two R's, so it cannot be formed. PAINTER, SENATOR and PLASTER use each of their letters "
    "only once, and all of them are available.", ["Each letter of PERSONALITY occurs once", "TERRAIN needs R twice ✗"],
    why_others_wrong="PAINTER, SENATOR and PLASTER can all be formed.", seconds=45, verified_by=RECOMP)
wd = "HOSTEL"
pr = letter_pairs(wd)
a, w = count_opts(len(pr))
mcq(ABT, PRS, "Basic", f"Count the letter pairs in '{wd}' whose gap in the word (the number of letters between them) equals "
    "their gap in the English alphabet, in either direction. How many such pairs are there?", a, w,
    "Compare the gap in the word with the gap in the alphabet",
    "Pairs found: " + (", ".join(f"{x}{y}" for x, y in pr) or "none") + f" — {len(pr)} in all.",
    ["Alphabet positions: " + ", ".join(f"{c} {pos(c)}" for c in wd),
     "A pair qualifies when |word gap| = |alphabet gap|"], natural=by_num, seconds=45, verified_by=RECOMP)
WDS = ["RELIABLE", "RELATION", "RELEASE", "RELIEF"]
srt = sorted(WDS)
assert srt == ["RELATION", "RELEASE", "RELIABLE", "RELIEF"]
mcq(ABT, WF, "Basic", "If the words RELIABLE, RELATION, RELEASE and RELIEF are arranged in the order in which they appear "
    "in an English dictionary, which word will be third?", srt[2], ["RELATION", "RELEASE", "RELIEF"],
    "Compare the first letter that differs", "All begin with REL. The 4th letters are A (RELATION), E (RELEASE) and I "
    "(RELIABLE, RELIEF). Between RELIABLE and RELIEF the 5th letters are A and E, so RELIABLE comes first. Order: "
    "RELATION, RELEASE, RELIABLE, RELIEF.", ["4th letters: A < E < I", "RELIA- < RELIE-", "Order: " + ", ".join(srt)],
    why_others_wrong="RELATION is first, RELEASE second and RELIEF fourth.", seconds=35, verified_by=RECOMP)

# ---------------------------------------------------------------- Alphabet test: Advanced set (rearranged alphabet)
NEWA = list(AL[13:]) + list(AL[:13][::-1])
assert fmt(NEWA[:3]) == "N O P" and NEWA[13] == "M" and NEWA[-1] == "A"
sid = stimulus("passage", "An alphabet with its halves rearranged",
               "The English alphabet is rearranged as follows: the last thirteen letters (N to Z) are written first in "
               "their usual order, followed by the first thirteen letters (A to M) in reverse order.\n\n" + fmt(NEWA),
               None, "Number the new arrangement 1 to 26 from the left: N is 1st, Z 13th, M 14th and A 26th.")
XQ = lambda sub, text, correct, wrongs, concept, expl, steps, **kw: mcq(
    ABT, sub, "Advanced", text, correct, wrongs, concept, expl, steps, stimulus=sid, verified_by=RECOMP, **kw)
ans = NEWA[11 + 8]
XQ(LP, "In the new arrangement, which letter is 8th to the right of the 12th letter from the left end?", ans,
   near(NEWA, 19), "Count in the new arrangement, not the usual alphabet",
   f"The 12th letter is {NEWA[11]}. Eight places to its right is the 20th letter of the new arrangement: {ans}.",
   [f"12th = {NEWA[11]}", f"12 + 8 = 20th ⇒ {ans}"], seconds=60)
ig, is_ = NEWA.index("G"), NEWA.index("S")
nb = abs(ig - is_) - 1
assert nb == 13
XQ(LP, "In the new arrangement, how many letters are there between G and S?", str(nb), ["11", "12", "14"],
   "Use the new positions", f"S is {ordn(is_ + 1)} and G is {ordn(ig + 1)} in the new arrangement; letters between "
   f"them: {ig + 1} − {is_ + 1} − 1 = {nb}.", [f"S = {is_ + 1}th, G = {ig + 1}th", f"{ig + 1} − {is_ + 1} − 1 = {nb}"],
   why_others_wrong="11 counts the gap in the usual alphabet (S − G − 1); 12 and 14 miscount by one at an end.",
   natural=int, seconds=65)
iq, ic = NEWA.index("Q"), NEWA.index("C")
assert (iq + ic) % 2 == 0
ans = NEWA[(iq + ic) // 2]
XQ(LP, "In the new arrangement, which letter lies exactly midway between Q and C?", ans, near(NEWA, (iq + ic) // 2),
   "Midway = average of the two new positions",
   f"Q is {ordn(iq + 1)} and C is {ordn(ic + 1)}; ({iq + 1} + {ic + 1}) ÷ 2 = {(iq + ic) // 2 + 1}th: {ans}.",
   [f"Q = {iq + 1}, C = {ic + 1}", f"Midway = {(iq + ic) // 2 + 1}th ⇒ {ans}"], seconds=65)
rem = [c for i, c in enumerate(NEWA) if (i + 1) % 4 != 0]
ans = rem[-10]
XQ(LP, "If every 4th letter of the new arrangement (the 4th, 8th, 12th, … letters) is removed, which letter will be "
   "10th from the right end of what remains?", ans, near(rem, len(rem) - 10), "Remove first, then count",
   "Removed: " + ", ".join(NEWA[i] for i in range(3, 26, 4)) + ". Remaining (" + str(len(rem)) + " letters): " +
   fmt(rem) + f". The 10th from the right is {ans}.",
   ["Remove positions 4, 8, …, 24", "Remaining: " + fmt(rem), f"10th from the right ⇒ {ans}"], seconds=80)

# ---------------------------------------------------------------- Number questions: Intermediate set (three-digit)
NUMS = [473, 852, 619, 352, 725]
sid = stimulus("data_table", "Five three-digit numbers (set C)",
               "Study the following five three-digit numbers and answer the questions.\n\n" + "   ".join(map(str, NUMS)),
               None, "Write out the digits of each number before applying an operation.")
NQ = lambda sub, text, correct, wrongs, concept, expl, steps, **kw: mcq(
    NSR, sub, "Intermediate", text, correct, wrongs, concept, expl, steps, stimulus=sid, verified_by=RECOMP, **kw)
dg = lambda n: [int(c) for c in str(n)]
hits = [n for n in NUMS if dg(n)[0] + dg(n)[2] == dg(n)[1]]
a, w = count_opts(len(hits))
assert hits == [473, 352]
NQ(TDN, "In how many of the numbers is the sum of the first and the last digits equal to the middle digit?", a, w,
   "Test every number", "; ".join(f"{n}: {dg(n)[0]} + {dg(n)[2]} = {dg(n)[0] + dg(n)[2]} vs {dg(n)[1]}"
                                    for n in NUMS) + ". Equal for 473 and 352 — two numbers.",
   ["Check first + last = middle for each", "473 ✓, 352 ✓"], natural=by_num, seconds=50)
desc = {n: int("".join(sorted(str(n), reverse=True))) for n in NUMS}
order = sorted(NUMS, key=desc.get)
ans = order[2]
assert ans == 725
NQ(TDN, "If the digits within each number are arranged in descending order, and the new numbers are then arranged in "
   "ascending order, which original number will be in the middle?", str(ans), ["473", "852", "619"],
   "Rearrange digits, then rank", "New numbers: " + ", ".join(f"{n} → {desc[n]}" for n in NUMS) + ". Ascending: "
   + ", ".join(str(desc[n]) for n in order) + f". The middle one, {desc[ans]}, comes from {ans}.",
   ["Descending digits within each number", "Rank the new numbers", f"Middle ⇒ {desc[ans]} ⇐ {ans}"],
   why_others_wrong="473 gives 743 (2nd), 852 stays 852 (4th) and 619 gives 961 (5th).", seconds=65)
pd = lambda n: math.prod(dg(n))
ans = pd(max(NUMS)) - pd(min(NUMS))
assert (pd(852), pd(352), ans) == (80, 30, 50)
NQ(NDO, "What is the difference between the product of the digits of the largest number and the product of the digits "
   "of the smallest number?", str(ans), ["30", "54", "80"], "Find the extremes, then multiply digits",
   "Largest 852: 8 × 5 × 2 = 80. Smallest 352: 3 × 5 × 2 = 30. Difference 80 − 30 = 50.",
   ["Largest 852 → 80", "Smallest 352 → 30", "80 − 30 = 50"],
   why_others_wrong="30 and 80 are the two products themselves; 54 uses 473 (84) instead of 852.", natural=int,
   seconds=55)
assert pd(473) - 30 == 54

# ---------------------------------------------------------------- Number questions: Intermediate set (row rules)


def is_sq(n):
    return math.isqrt(n) ** 2 == n


def is_prime(n):
    return n > 1 and all(n % d for d in range(2, math.isqrt(n) + 1))


def step8(a, b):
    if is_sq(a):
        return math.isqrt(a) * b
    if is_prime(a):
        return a + 2 * b
    return a - b if b % 2 == 0 else a + b


ROWS = [(16, 5, 3), (7, 6, 4), (25, 3, 9)]
res = [step8(step8(a, b), c) for a, b, c in ROWS]
assert res == [23, 27, 24]
sid = stimulus("data_table", "Three rows of numbers with square and prime rules",
               "Each row has three numbers. Work from left to right: apply the first rule below that fits the first two "
               "numbers, then apply the first rule that fits that result and the third number. The final value is the "
               "row's result.\n\n(i) If the first number of the pair is a perfect square, the result is its square "
               "root multiplied by the second number.\n(ii) Otherwise, if the first number is a prime number, the "
               "result is the first number plus twice the second number.\n(iii) Otherwise, if the second number is "
               "even it is subtracted from the first; if it is odd it is added to the first.\n\nRow 1: 16   5   3\n"
               "Row 2: 7   6   4\nRow 3: 25   3   9", None,
               "Row 1: 16 is a square → 4 × 5 = 20; 20 is neither a square nor a prime and 3 is odd → 23.\n"
               "Row 2: 7 is prime → 7 + 12 = 19; 19 is prime → 19 + 8 = 27.\n"
               "Row 3: 25 is a square → 5 × 3 = 15; 15 is neither, 9 is odd → 24.")
NQ = lambda text, correct, wrongs, concept, expl, steps, **kw: mcq(
    NSR, NDO, "Intermediate", text, correct, wrongs, concept, expl, steps, stimulus=sid, verified_by=RECOMP, **kw)
NQ("What is the result of Row 2?", str(res[1]), ["19", "23", "15"], "Check the rules in order for each step",
   "7 is prime, so rule (ii): 7 + 2 × 6 = 19. 19 is also prime, so rule (ii) again: 19 + 2 × 4 = 27.",
   ["7 + 12 = 19", "19 + 8 = 27"],
   why_others_wrong="19 stops after the first step; 23 adds 4 instead of 8; 15 applies rule (iii) to 19.", natural=int,
   seconds=55)
assert step8(19, 4) == 27 and 19 - 4 == 15
NQ("What is the sum of the results of Row 1 and Row 3?", str(res[0] + res[2]), ["35", "50", "51"],
   "Rule (i) uses the square root", "Row 1: √16 × 5 = 20, then 20 + 3 = 23. Row 3: √25 × 3 = 15, then 15 + 9 = 24. "
   "23 + 24 = 47.", ["Row 1 = 23", "Row 3 = 24", "23 + 24 = 47"],
   why_others_wrong="35 adds only the first-step values (20 + 15); 50 adds Rows 1 and 2; 51 adds Rows 2 and 3.",
   natural=int, seconds=60)
assert (res[0] + res[1], res[1] + res[2]) == (50, 51)
new2 = step8(step8(7, 9), 4)
assert step8(7, 9) == 25 and new2 == 20
NQ("If the 6 in Row 2 is replaced by 9, what will be the result of Row 2?", str(new2), ["29", "33", "100"],
   "A new first-step result can change which rule applies next",
   "7 is prime: 7 + 2 × 9 = 25. Now 25 is a perfect square, so rule (i) applies: √25 × 4 = 20.",
   ["7 + 18 = 25", "25 is a square ⇒ 5 × 4 = 20"],
   why_others_wrong="29 adds 4 to 25 (rule iii) and 33 adds 2 × 4 (rule ii), both ignoring that 25 is a square; 100 "
                    "multiplies 25 by 4 without taking the square root.", natural=int, seconds=65)


# ================================================================================================ BATCH 009
begin("009")
# ---------------------------------------------------------------- Blood relations: Basic
F = Family().add("Gp", "M").add("Gm", "F").marry("Gp", "Gm").add("Bhavesh", "M", "Gp", "Gm").add("Am", "F", "Gp", "Gm")
F.add("Af", "M").marry("Af", "Am").add("Ananya", "F", "Af", "Am").add("Bw", "F").marry("Bhavesh", "Bw")
F.add("Chirag", "M", "Bhavesh", "Bw")
F.check([("Bhavesh", "brother", "Am"), ("Am", "mother", "Ananya"), ("Chirag", "son", "Bhavesh")])
ans = F.rel("Chirag", "Ananya")
assert ans == "cousin"
mcq(BLD, DRB, "Basic", "Ananya's mother has only one brother, Bhavesh. Chirag is Bhavesh's son. How is Chirag related "
    "to Ananya?", cap(ans), ["Brother", "Nephew", "Uncle"], "Children of siblings are cousins",
    "Bhavesh is the brother of Ananya's mother, i.e. Ananya's maternal uncle. His son Chirag is therefore Ananya's "
    "cousin.", ["Bhavesh = Ananya's maternal uncle", "Uncle's son ⇒ cousin"],
    why_others_wrong="Chirag and Ananya have different parents, so he is not her brother; he is in her generation, so "
                     "neither her nephew nor her uncle.", seconds=30, verified_by=RECOMP)

# ---------------------------------------------------------------- Blood relations: Intermediate set (coded)
CODE9 = {"∆": "mother", "∇": "son", "◊": "husband", "⊥": "sister", "∥": "brother"}
sid = stimulus("passage", "Five geometric codes for relations",
               "In a certain code:\n'P ∆ Q' means 'P is the mother of Q';\n'P ∇ Q' means 'P is the son of Q';\n'P ◊ Q' "
               "means 'P is the husband of Q';\n'P ⊥ Q' means 'P is the sister of Q';\n'P ∥ Q' means 'P is the brother "
               "of Q'.", None,
               "Decode pair by pair from the left. Two children of the same person are siblings; a child's two "
               "parents are a married couple.")
BQ = lambda sub, text, correct, wrongs, concept, expl, steps, **kw: mcq(
    BLD, sub, "Intermediate", text, correct, wrongs, concept, expl, steps, stimulus=sid, verified_by=RECOMP, **kw)
F = Family().add("D", "M").add("A", "F").marry("D", "A").add("B", "M", "D", "A").add("C", "M", "D", "A")
F.check(coded_facts("A ∆ B ∥ C ∇ D", CODE9))
ans = F.rel("D", "A")
assert ans == "husband"
BQ(CDB, "If 'A ∆ B ∥ C ∇ D', how is D related to A?", cap(ans), ["Son", "Father", "Brother"],
   "Two parents of one child are a couple",
   "A is B's mother; B is C's brother, so C is also A's child; C is D's son, so D is C's other parent. A is C's "
   "mother, so D is C's father and A's husband.", ["A ∆ B, B ∥ C ⇒ A is C's mother", "C ∇ D ⇒ D is C's parent",
                                                   "A mother, D parent ⇒ D is A's husband"],
   why_others_wrong="D is a parent of A's children, not A's child; nothing makes D A's father or brother.", seconds=55)
F = Family().add("R", "M").add("S", "F").marry("R", "S").add("P", "F", "R", "S").add("Q", "M", "R", "S")
F.check(coded_facts("P ⊥ Q ∇ R ◊ S", CODE9))
ans = F.rel("P", "S")
assert ans == "daughter"
BQ(CDB, "If 'P ⊥ Q ∇ R ◊ S', how is P related to S?", cap(ans), ["Sister", "Daughter-in-law", "Niece"],
   "A sister of one's son is one's daughter",
   "P is Q's sister; Q is R's son; R is S's husband, so S is Q's mother. P, Q's sister, is also S's daughter.",
   ["Q ∇ R, R ◊ S ⇒ Q is S's son", "P ⊥ Q ⇒ P is S's daughter"],
   why_others_wrong="P is Q's sister, not S's; P is S's own child, not a son's wife or a sibling's child.",
   seconds=55)
EXPRS = ["X ∆ Z ◊ W ∆ Y", "X ∆ Z ⊥ W ∆ Y", "X ⊥ Z ◊ W ∆ Y", "X ∆ Z ∥ W ∆ Y"]
F = Family().add("Xh", "M").add("X", "F").marry("Xh", "X").add("Z", "M", "Xh", "X").add("W", "F").marry("Z", "W")
F.add("Y", "M", "Z", "W")
F.check(coded_facts(EXPRS[0], CODE9))
assert F.rel("X", "Y") == "grandmother" and "Z" in F.parents("Y") and F.g["Z"] == "M"
# option 2: Z and W are sisters, so W (Y's mother) is X's daughter: maternal grandmother.
F2 = Family().add("Xh", "M").add("X", "F").marry("Xh", "X").add("Z", "F", "Xh", "X").add("W", "F", "Xh", "X")
F2.add("Wh", "M").marry("Wh", "W").add("Y", "M", "Wh", "W")
F2.check(coded_facts(EXPRS[1], CODE9))
assert F2.rel("X", "Y") == "grandmother" and not any(F2.g[p] == "M" and p in F2.children("X") for p in F2.parents("Y"))
# option 3: X is Z's sister, i.e. an aunt of Y. Option 4: Z is W's brother, so W is also X's child and is Y's mother.
F4 = Family().add("Xh", "M").add("X", "F").marry("Xh", "X").add("Z", "M", "Xh", "X").add("W", "F", "Xh", "X")
F4.add("Wh", "M").marry("Wh", "W").add("Y", "M", "Wh", "W")
F4.check(coded_facts(EXPRS[3], CODE9))
assert F4.rel("X", "Y") == "grandmother" and "Z" not in F4.parents("Y")
BQ(CDB, "Which of the following expressions shows that X is the paternal grandmother of Y (the mother of Y's "
   "father)?", EXPRS[0], EXPRS[1:], "Y's parent who is X's child must be male",
   "In 'X ∆ Z ◊ W ∆ Y', X is Z's mother, Z is W's husband and W is Y's mother, so Z (a man) is Y's father and X is "
   "his mother: Y's paternal grandmother. In the second and fourth expressions Y's mother W is X's daughter, so X is "
   "the maternal grandmother; in the third X is Z's sister, an aunt of Y.",
   ["Option 1: X → son Z → (Z's wife W) → Y ⇒ paternal", "Options 2 and 4: W, Y's mother, is X's daughter ⇒ maternal",
    "Option 3: X is Z's sister ⇒ aunt"],
   why_others_wrong="Two of them make X the mother of Y's mother, and one makes X an aunt.", seconds=75)
F = Family().add("H", "M").add("F_", "F").marry("H", "F_").add("Fp", "M").add("Fm", "F").marry("Fp", "Fm")
F.par["F_"] = ("Fp", "Fm")
F.add("E", "M", "Fp", "Fm").add("G", "M", "H", "F_")
F.check(coded_facts("E ∥ F_ ∆ G ∇ H", CODE9))
ans = F.rel("H", "E")
assert ans == "brother-in-law"
BQ(CDB, "If 'E ∥ F ∆ G ∇ H', how is H related to E?", cap(ans), ["Brother", "Father", "Nephew"],
   "The husband of one's sister", "E is F's brother; F is G's mother; G is H's son, so H is G's other parent — "
   "F's husband. H, the husband of E's sister F, is E's brother-in-law.",
   ["F ∆ G, G ∇ H ⇒ H is F's husband", "F is E's sister ⇒ H is E's brother-in-law"],
   why_others_wrong="H shares no parent with E; H is in E's generation, so neither his father nor his nephew.",
   seconds=60)

# ---------------------------------------------------------------- Blood relations: Intermediate set (family of six)
F = Family().add("Harsh", "M").add("Indira", "F").marry("Harsh", "Indira").add("Jatin", "M", "Harsh", "Indira")
F.add("Kirti", "F", "Harsh", "Indira").add("Lavanya", "F").marry("Jatin", "Lavanya")
F.add("Gunjan", "F", "Jatin", "Lavanya")
F.check([("Gunjan", "granddaughter", "Indira"), ("Lavanya", "daughter-in-law", "Harsh"),
         ("Kirti", "sister-in-law", "Lavanya"), ("Jatin", "father", "Gunjan"), ("Harsh", "husband", "Indira")])
assert "Kirti" not in F.sp
sid = stimulus("puzzle", "A family of six across three generations",
               "A family has six members — Gunjan, Harsh, Indira, Jatin, Kirti and Lavanya — across three generations, "
               "with exactly two married couples.",
               [("Harsh is married to Indira.", (), None), ("Gunjan is the only grandchild of Indira and is a girl.", (),
                                                             None),
                ("Lavanya is the daughter-in-law of Harsh.", (), None), ("Jatin is the father of Gunjan.", (), None),
                ("Kirti is unmarried and is the sister-in-law of Lavanya.", (), None)],
               "Lavanya, Harsh's daughter-in-law, is married to a son of Harsh; Jatin is Gunjan's father and Gunjan is "
               "Indira's grandchild, so Jatin is that son and Lavanya his wife. Kirti is unmarried, so as Lavanya's "
               "sister-in-law she must be her husband's sister: Harsh's daughter.\nTree: Harsh + Indira → Jatin "
               "(+ Lavanya) → Gunjan; Kirti.")
TREE9 = "Harsh + Indira → Jatin (+ Lavanya) → Gunjan; Kirti (unmarried daughter)"
FQ = lambda text, correct, wrongs, concept, expl, steps, **kw: mcq(
    BLD, FPZ, "Intermediate", text, correct, wrongs, concept, expl, steps, stimulus=sid, verified_by=RECOMP, **kw)
ans = F.rel("Kirti", "Gunjan")
assert ans == "aunt"
FQ("How is Kirti related to Gunjan?", cap(ans), ["Sister", "Mother", "Cousin"], "Father's sister = aunt",
   "Kirti is Jatin's sister and Jatin is Gunjan's father, so Kirti is Gunjan's paternal aunt.",
   [TREE9, "Kirti = sister of Gunjan's father ⇒ aunt"],
   why_others_wrong="Gunjan is the only grandchild, so she has no sister or cousin in the family; her mother is "
                    "Lavanya.", seconds=55)
ans = F.rel("Indira", "Lavanya")
assert ans == "mother-in-law"
FQ("How is Indira related to Lavanya?", cap(ans), ["Mother", "Sister-in-law", "Grandmother"],
   "Husband's mother = mother-in-law", "Lavanya is Jatin's wife, and Indira is Jatin's mother, so Indira is Lavanya's "
   "mother-in-law.", [TREE9, "Indira = mother of Lavanya's husband"],
   why_others_wrong="Lavanya is not Indira's own child; Indira is a generation above, so not a sister-in-law; she is "
                    "Gunjan's grandmother, not Lavanya's.", seconds=50)
ans = F.rel("Kirti", "Harsh")
assert ans == "daughter"
FQ("How is Kirti related to Harsh?", cap(ans), ["Daughter-in-law", "Sister", "Granddaughter"],
   "An unmarried sister-in-law is the husband's sister",
   "Kirti is unmarried, so she cannot be the wife of Lavanya's brother within the family; as Lavanya's sister-in-law "
   "she is the sister of Lavanya's husband Jatin, i.e. Harsh's daughter.",
   [TREE9, "Unmarried sister-in-law ⇒ husband's sister", "Jatin's sister ⇒ Harsh's daughter"],
   why_others_wrong="Harsh's daughter-in-law is Lavanya; Kirti is a generation below Harsh; his only grandchild is "
                    "Gunjan.", seconds=60)

# ---------------------------------------------------------------- Blood relations: Advanced set (family of eight)
F = Family().add("Bhola", "M").add("Charu", "F").marry("Bhola", "Charu").add("Divya", "F", "Bhola", "Charu")
F.add("Eshan", "M", "Bhola", "Charu").add("Faiz", "M").marry("Faiz", "Divya").add("Gita", "F").marry("Eshan", "Gita")
F.add("Hiten", "M", "Faiz", "Divya").add("Ira", "F", "Eshan", "Gita")
F.check([("Hiten", "grandson", "Charu"), ("Ira", "granddaughter", "Charu"), ("Hiten", "cousin", "Ira"),
         ("Faiz", "son-in-law", "Bhola"), ("Gita", "mother", "Ira"), ("Gita", "sister-in-law", "Divya"),
         ("Divya", "daughter", "Bhola"), ("Bhola", "husband", "Charu")])
assert [c for c in F.children("Charu") if F.g[c] == "M"] == ["Eshan"]
sid = stimulus("puzzle", "A family of eight with two cousins",
               "A family has eight members — Bhola, Charu, Divya, Eshan, Faiz, Gita, Hiten and Ira — across three "
               "generations, with three married couples. Every spouse is a member of the family.",
               [("Bhola is Charu's husband, and Eshan is their only son.", (), None),
                ("Divya is a daughter of Bhola.", (), None), ("Faiz is the son-in-law of Bhola.", (), None),
                ("Gita is the mother of Ira and the sister-in-law of Divya.", (), None),
                ("Hiten (a boy) and Ira (a girl) are the only grandchildren of Charu, and they are cousins.", (),
                 None)],
               "Faiz, Bhola's son-in-law, is married to Bhola's daughter Divya (the only daughter in the family). Gita "
               "is Divya's sister-in-law and not Faiz's wife, so she is Eshan's wife; Ira's mother is Gita, so Ira is "
               "Eshan's daughter. Hiten, the other grandchild and Ira's cousin, is the son of Divya and Faiz.\nTree: "
               "Bhola + Charu → Divya (+ Faiz) → Hiten; Eshan (+ Gita) → Ira.")
TREE9B = "Bhola + Charu → Divya (+ Faiz) → Hiten; Eshan (+ Gita) → Ira"
AQ = lambda text, correct, wrongs, concept, expl, steps, **kw: mcq(
    BLD, FPZ, "Advanced", text, correct, wrongs, concept, expl, steps, stimulus=sid, verified_by=RECOMP, **kw)
ans = F.rel("Faiz", "Ira")
assert ans == "uncle"
AQ("How is Faiz related to Ira?", cap(ans), ["Father", "Grandfather", "Brother-in-law"],
   "Husband of the father's sister", "Ira's father is Eshan, and Divya is Eshan's sister. Faiz is Divya's husband, so "
   "he is Ira's uncle (her paternal aunt's husband).", [TREE9B, "Faiz = husband of Ira's father's sister ⇒ uncle"],
   why_others_wrong="Ira's father is Eshan; her grandfather is Bhola; a brother-in-law would be in her own "
                    "generation.", seconds=85)
ans = F.rel("Hiten", "Eshan")
assert ans == "nephew"
AQ("How is Hiten related to Eshan?", cap(ans), ["Son", "Cousin", "Grandson"], "Sister's son = nephew",
   "Hiten is the son of Divya, and Divya is Eshan's sister, so Hiten is Eshan's nephew.",
   [TREE9B, "Hiten = son of Eshan's sister ⇒ nephew"],
   why_others_wrong="Eshan's child is Ira; Hiten is Ira's cousin, not Eshan's; Eshan is only one generation above "
                    "Hiten.", seconds=75)
PAIRS = [("Faiz", "Eshan"), ("Bhola", "Faiz"), ("Hiten", "Eshan"), ("Faiz", "Hiten")]
good = [p for p in PAIRS if F.rel(*p) == "brother-in-law"]
assert good == [("Faiz", "Eshan")]
AQ("Which of the following is a pair of brothers-in-law?", "Faiz and Eshan",
   ["Bhola and Faiz", "Hiten and Eshan", "Faiz and Hiten"], "Wife's brother = brother-in-law",
   "Faiz is married to Divya, and Eshan is Divya's brother, so Faiz and Eshan are brothers-in-law. Bhola is Faiz's "
   "father-in-law, Eshan is Hiten's uncle and Faiz is Hiten's father.",
   [TREE9B, "Faiz – Divya – Eshan: wife's brother ⇒ brothers-in-law"],
   why_others_wrong="Bhola and Faiz are father-in-law and son-in-law; Hiten is Eshan's nephew and Faiz's son.",
   seconds=80)

# ---------------------------------------------------------------- Direction
ren = (ANG["N"] - ANG["NE"]) % 360
assert (ANG["NW"] + ren) % 360 == ANG["W"]
ans = DEG[(ANG["S"] + ren) % 360]
assert ans == "South-East"
mcq(DIR, DD, "Basic", "In a certain system every direction is renamed in the same way: north-east is called north and "
    "north-west is called west. What is south called in that system?", ans, ["South-West", "North-East", "East"],
    "Renaming = turning every direction by the same angle",
    "North-east → north is a turn of 45° anticlockwise, and north-west → west is the same turn. Turning south 45° "
    "anticlockwise gives south-east.", ["Each name is 45° anticlockwise of the true direction",
                                        "South turned 45° anticlockwise ⇒ South-East"],
    why_others_wrong="South-West turns the other way; North-East and East are 180° and 90° away from south.",
    seconds=40, verified_by=RECOMP)
legs = [24, 24 // 2, 24 * 5 // 8]
MV = [(None, legs[0]), ("R", legs[1]), ("R", legs[2])]
x, y = walk("S", MV)
assert legs == [24, 12, 15] and (x, y) == (-12, -9)
c, w, why = dd_wrongs(x, y, "m", sum(legs))
mcq(DIR, DD, "Intermediate", "Nisha walks 24 m towards the south. She turns right and walks half that distance, and "
    "then turns right again and walks five-eighths of the first distance. How far is she now from her starting point, "
    "and in which direction?", c, w, "Work out each leg first",
    "Legs: 24 m, 12 m and 15 m. Right from south is west, and right from west is north. She ends 12 m west and 24 − 15 "
    "= 9 m south of the start: √(144 + 81) = 15 m, south-west.",
    ["Legs: 24, 24 ÷ 2 = 12, 24 × 5/8 = 15"] + walk_trace("S", MV, "m") + ["√(12² + 9²) = 15 m, South-West"],
    why_others_wrong=why, seconds=65, verified_by=RECOMP)
A_, B_ = (0, 0), (40, 0)
C_ = (40, 30)
D_ = (0, 30)
O_ = ((A_[0] + C_[0]) / 2, (A_[1] + C_[1]) / 2)
assert O_ == ((B_[0] + D_[0]) / 2, (B_[1] + D_[1]) / 2) == (20, 15)
c, w, why = dd_wrongs(20, 15, "m", 35)
mcq(DIR, PP, "Intermediate", "ABCD is a rectangular field. B is 40 m east of A, C is 30 m north of B, and D is 30 m north "
    "of A. A flag stands at the point where the diagonals AC and BD cross. How far is the flag from corner A, and in "
    "which direction?", c, w, "Diagonals of a rectangle bisect each other",
    "With A at (0, 0): B (40, 0), C (40, 30), D (0, 30). The diagonals meet at their common midpoint (20, 15), which is "
    "20 m east and 15 m north of A: √(400 + 225) = 25 m, north-east.",
    ["A (0, 0), C (40, 30)", "Crossing point = midpoint of AC = (20, 15)", "√(20² + 15²) = 25 m, North-East"],
    why_others_wrong=why, seconds=60, verified_by=RECOMP)
X1 = (0, 40 * 0.5)
X2 = (X1[0] + 60 * 0.5, X1[1])
Y1 = (0, -20 * 1)
dx, dy = X2[0] - Y1[0], X2[1] - Y1[1]
assert (dx, dy) == (30, 40)
c, w, why = dd_wrongs(30, 40, "km", 20 + 30 + 20)
mcq(DIR, DD, "Advanced", "At 9:00 am, car X leaves point O and drives north at 40 km/h. At 9:30 am it turns right and "
    "drives at 60 km/h until 10:00 am. Car Y leaves O at 9:00 am and drives south at 20 km/h until 10:00 am. At 10:00 "
    "am, how far is car X from car Y, and in which direction is X from Y?", c, w, "Distance = speed × time for each leg",
    "X: north 40 × ½ = 20 km, then east (right of north) 60 × ½ = 30 km ⇒ (30, 20). Y: south 20 × 1 = 20 km ⇒ (0, "
    "−20). X − Y = (30, 40): √(900 + 1600) = 50 km, north-east.",
    ["X: (0, 20) → (30, 20)", "Y: (0, −20)", "X − Y = (30, 40) ⇒ 50 km, North-East"], why_others_wrong=why,
    seconds=100, verified_by=RECOMP)

# ---------------------------------------------------------------- Coding: extra alternative rules (opposite letter
# combined with reversal) added to the batch-5 library for the inferred-rule checks below
opp = lambda w: "".join(AL[26 - pos(c)] for c in w)
LRULES2 = dict(LRULES)
for k_ in range(-6, 7):
    LRULES2[f"opprev+{k_}"] = lambda w, k_=k_: shift(opp(w[::-1]), k_)
    LRULES2[f"rev+opp+posL{k_}"] = lambda w, k_=k_: "".join(shift(c, k_ * (i + 1)) for i, c in enumerate(opp(w[::-1])))

# ---------------------------------------------------------------- Coding: Basic set (chain of two-word sentences)
SS = [(["green", "tea"], ["mi", "lo"]), (["tea", "time"], ["ru", "mi"]), (["time", "flies"], ["ka", "ru"]),
      (["green", "leaf"], ["lo", "se"])]
sid = stimulus("passage", "Four coded two-word phrases",
               "In a certain code language:\n" + "\n".join(f"'{' '.join(a_)}' is written as '{' '.join(b_)}'"
                                                           for a_, b_ in SS) +
               "\n(The codes of the words in a phrase may be in any order.)", None,
               "tea = mi (phrases 1 and 2), time = ru (2 and 3), green = lo (1 and 4). Then flies = ka and leaf = se.")
CQ = lambda sub, text, correct, wrongs, concept, expl, steps, **kw: mcq(
    COD, sub, "Basic", text, correct, wrongs, concept, expl, steps, stimulus=sid, verified_by=RECOMP, **kw)
assert sentence_solve(SS, "flies") == {"ka"}
CQ(SW, "What is the code for 'flies'?", "ka", ["ru", "mi", "se"], "Follow the chain of shared words",
   "'tea' is in phrases 1 and 2, so tea = mi. Then in phrase 2, time = ru, and in phrase 3, flies = ka.",
   ["tea = mi (1 ∩ 2)", "time = ru (2 ∩ 3)", "flies = ka"], why_others_wrong="ru is 'time', mi is 'tea' and se is "
                                                                             "'leaf'.", seconds=40)
assert sentence_solve(SS, "se") == {"leaf"}
CQ(SW, "Which word is coded as 'se'?", "leaf", ["green", "tea", "flies"], "Leftover code of a phrase",
   "'green' is in phrases 1 and 4, whose common code is lo. So in 'green leaf' = 'lo se', leaf = se.",
   ["green = lo (1 ∩ 4)", "se ⇒ leaf"], why_others_wrong="green = lo, tea = mi and flies = ka.", seconds=40)
assert sentence_solve(SS, "green") == {"lo"} and sentence_solve(SS, "time") == {"ru"}
CQ(SW, "What is the code for 'green time'?", "lo ru", ["mi ru", "lo ka", "se ru"], "Two codes from shared phrases",
   "green = lo (common to phrases 1 and 4) and time = ru (common to phrases 2 and 3): 'lo ru'.",
   ["green = lo", "time = ru"], why_others_wrong="mi is 'tea', ka is 'flies' and se is 'leaf'.", seconds=40)

# ---------------------------------------------------------------- Coding: Basic (standalone)
hr = LRULES["halfrev+0"]
assert hr("MOBILE") == "BOMELI"
ans = inferred([("MOBILE", "BOMELI")], "SILVER", hr("SILVER"))
assert ans == "LISREV"
mcq(COD, LC, "Basic", "In a certain code, MOBILE is written as BOMELI. How is SILVER written in that code?", ans,
    ["REVLIS", "ISLREV", "LISERV"], "Reverse each half of the word",
    "MOBILE → halves MOB | ILE → each half reversed: BOM | ELI. SILVER → SIL | VER → LIS | REV = LISREV.",
    ["Halves: SIL | VER", "Reverse each half ⇒ LIS | REV"],
    why_others_wrong="REVLIS reverses the whole word; ISLREV and LISERV reverse one half wrongly.", seconds=35,
    verified_by=RECOMP)
sl = NRULES["sum-len"]
assert sl("FACE") == 11 and sl("BEAD") == 8
ans = inferred([("FACE", 11), ("BEAD", 8)], "JADE", sl("JADE"), NRULES)
assert ans == 16
mcq(COD, NC, "Basic", "In a certain code, FACE is written as 11 and BEAD is written as 8. How is JADE written in that "
    "code?", str(ans), ["20", "24", "12"], "Sum of positions minus the number of letters",
    "FACE: 6 + 1 + 3 + 5 = 15, minus 4 letters = 11. BEAD: 2 + 5 + 1 + 4 = 12, minus 4 = 8. JADE: 10 + 1 + 4 + 5 = 20, "
    "minus 4 = 16.", ["FACE 15 − 4 = 11 ✓; BEAD 12 − 4 = 8 ✓", "JADE 20 − 4 = 16"],
    why_others_wrong="20 is the plain sum; 24 adds the length instead of subtracting it; 12 subtracts 8.",
    natural=int, seconds=40, verified_by=RECOMP)

# ---------------------------------------------------------------- Coding: Intermediate (standalone)
pr1 = LRULES["posR-1"]
assert pr1("CHAIR") == "XDXGQ" and pr1("TOWEL") == "OKTCK"
ans = inferred([("CHAIR", "XDXGQ"), ("TOWEL", "OKTCK")], "BENCH", pr1("BENCH"))
assert ans == "WAKAG" and LRULES["posL-1"]("BENCH") == "ACKYC"
mcq(COD, LC, "Intermediate", "In a certain code, CHAIR is written as XDXGQ and TOWEL is written as OKTCK. How is BENCH "
    "written in that code?", ans, ["ACKYC", "GAKAW", "WBKAG"], "Shift back by the place counted from the right",
    "Each letter moves back by its place counted from the right end: in CHAIR, C −5 = X, H −4 = D, A −3 = X, I −2 = G, "
    "R −1 = Q. TOWEL: T −5 O, O −4 K, W −3 T, E −2 C, L −1 K. BENCH: B −5 = W, E −4 = A, N −3 = K, C −2 = A, H −1 = G.",
    ["Shifts −5, −4, −3, −2, −1 from left to right", "BENCH ⇒ W A K A G"],
    why_others_wrong="ACKYC counts the places from the left; GAKAW reverses the answer; WBKAG moves E back only 3.",
    seconds=70, verified_by=RECOMP)
r9 = DR2["9-ends"]
assert r9("3816") == "3186" and r9("5207") == "2794"
ans = inferred([("3816", "3186"), ("5207", "2794")], "6439", r9("6439"), DR2)
assert ans == "0563"
mcq(COD, NC, "Intermediate", "In a certain code, 3816 is written as 3186 and 5207 is written as 2794. How is 6439 "
    "written in that code?", ans, ["3560", "9436", "0564"], "Swap the end digits, then subtract each digit from 9",
    "3816: interchange the first and last digits → 6813, then replace each digit d by 9 − d → 3186. 5207 → 7205 → "
    "2794. 6439 → 9436 → 0563.", ["Check: 3816 → 6813 → 3186; 5207 → 7205 → 2794", "6439 → 9436", "9 − each ⇒ 0563"],
    why_others_wrong="3560 skips the interchange; 9436 stops after it; 0564 miscomputes the last digit.", seconds=65,
    verified_by=RECOMP)
orv = LRULES2["opprev+0"]
assert orv("FIRE") == "VIRU" and orv("WATER") == "IVGZD"
ans = inferred([("FIRE", "VIRU"), ("WATER", "IVGZD")], "SMOKE", orv("SMOKE"), LRULES2)
assert ans == "VPLNH"
mcq(COD, LC, "Intermediate", "In a certain code, FIRE is written as VIRU and WATER is written as IVGZD. How is SMOKE "
    "written in that code?", ans, ["HNLPV", "EKOMS", "VPLNG"], "Opposite letters, written in reverse order",
    "Each letter is replaced by its opposite letter (A↔Z, B↔Y, …) and the result is written from right to left. FIRE → "
    "U R I V → VIRU. WATER → D Z G V I → IVGZD. SMOKE → H N L P V → VPLNH.",
    ["Opposite pairs: S↔H, M↔N, O↔L, K↔P, E↔V", "HNLPV reversed ⇒ VPLNH"],
    why_others_wrong="HNLPV forgets the reversal; EKOMS only reverses the word; VPLNG takes the opposite of S as G.",
    seconds=65, verified_by=RECOMP)

# ---------------------------------------------------------------- Coding: Advanced set (structure code)


def scode(w):
    return f"{len(w)}{''.join(sorted(c for c in w if c not in VOW))}{sum(c in VOW for c in w)}"


sid = stimulus("passage", "A code built from the letters of a word",
               "In a certain code, each word is written as three parts placed one after another:\n(1) the number of "
               "letters in the word;\n(2) the consonants of the word arranged in alphabetical order (a repeated "
               "consonant is written each time it occurs);\n(3) the number of vowels (A, E, I, O, U) in the word.\n"
               "For example, MARKET is written as 6KMRT2.", None,
               "Count the letters, sort the consonants, count the vowels; letters of the word that are vowels do not "
               "appear in part (2).")
assert scode("MARKET") == "6KMRT2"
SQ = lambda sub, text, correct, wrongs, concept, expl, steps, **kw: mcq(
    COD, sub, "Advanced", text, correct, wrongs, concept, expl, steps, stimulus=sid, verified_by=RECOMP, **kw)
ans = scode("PLANTS")
assert ans == "6LNPST1"
SQ(LC, "How is 'PLANTS' written in this code?", ans, ["6PLNTS1", "6LNPST2", "5LNPST1"], "Sort the consonants",
   "PLANTS has 6 letters; its consonants P, L, N, T, S in alphabetical order are L, N, P, S, T; it has one vowel (A): "
   "6LNPST1.", ["Letters: 6", "Consonants sorted: L N P S T", "Vowels: 1"],
   why_others_wrong="6PLNTS1 keeps the word order; 6LNPST2 counts two vowels; 5LNPST1 miscounts the letters.",
   seconds=70)
ans = scode("AUDIO")
assert ans == "5D4"
SQ(LC, "How is 'AUDIO' written in this code?", ans, ["5D3", "5AD4", "4D5"], "Vowels do not enter part (2)",
   "AUDIO has 5 letters, only one consonant (D) and four vowels (A, U, I, O): 5D4.",
   ["Letters: 5", "Consonants: D", "Vowels: A, U, I, O = 4"],
   why_others_wrong="5D3 misses a vowel; 5AD4 puts a vowel among the consonants; 4D5 swaps the two numbers.",
   seconds=65)
OPTS = ["STICKER", "TRICKED", "STROKES", "CRICKET"]
codes_ = {o: scode(o) for o in OPTS}
assert [o for o in OPTS if codes_[o] == "7CKRST2"] == ["STICKER"]
SQ(LC, "Which of the following words is written as '7CKRST2' in this code?", "STICKER", OPTS[1:],
   "Code every option", "STICKER: 7 letters; consonants S, T, C, K, R → C K R S T; vowels I, E = 2 ⇒ 7CKRST2. "
   f"TRICKED → {codes_['TRICKED']}, STROKES → {codes_['STROKES']}, CRICKET → {codes_['CRICKET']}.",
   ["All four have 7 letters and 2 vowels", "Only STICKER has the consonants C, K, R, S, T"],
   why_others_wrong="TRICKED has a D, STROKES two S's and CRICKET two C's among its consonants.", seconds=80)
WL = ["SECURE", "PLANET", "CANDLE", "ORANGE"]
hits = [w_ for w_ in WL if len(w_) == 2 * sum(c in VOW for c in w_)]
a, w = count_opts(len(hits))
assert hits == ["SECURE", "ORANGE"]
SQ(LC, "In how many of the words SECURE, PLANET, CANDLE and ORANGE will the number at the start of the code be exactly "
   "twice the number at the end?", a, w, "Only the letter count and the vowel count matter",
   "All four words have 6 letters, so the vowel count must be 3. SECURE (E, U, E) and ORANGE (O, A, E) have 3 vowels; "
   "PLANET and CANDLE have 2. Two words.", ["Start = 6 for all", "Vowels: SECURE 3, PLANET 2, CANDLE 2, ORANGE 3"],
   natural=by_num, seconds=70)

# ---------------------------------------------------------------- Coding: Advanced (standalone)
op1 = LRULES["opp+posL1"]
assert op1("GOLD") == "UNRA" and op1("MINT") == "OTPK"
ans = inferred([("GOLD", "UNRA"), ("MINT", "OTPK")], "SILVER", op1("SILVER"), LRULES2)
assert ans == "ITRIAO"
mcq(COD, LC, "Advanced", "In a certain code, GOLD is written as UNRA and MINT is written as OTPK. How is SILVER written "
    "in that code?", ans, ["HROEVI", "TKOZJX", "ITRIAP"], "Opposite letter, then shift by place",
    "Each letter is first replaced by its opposite letter (A↔Z): GOLD → T L O W. Then the 1st letter moves 1 place "
    "forward, the 2nd 2 places, and so on: U N R A. MINT → N R M G → O T P K. SILVER → H R O E V I → H+1 I, R+2 T, O+3 "
    "R, E+4 I, V+5 A, I+6 O = ITRIAO.", ["Opposites: SILVER → HROEVI", "Shifts +1 … +6 ⇒ ITRIAO"],
    why_others_wrong="HROEVI stops after the opposites; TKOZJX shifts without taking opposites; ITRIAP shifts the 6th "
                     "letter by 7.", seconds=90, verified_by=RECOMP)
DIGL = {}
for k_ in range(-3, 6):
    for rv_ in (False, True):
        DIGL[f"{k_},{rv_}"] = lambda n, k_=k_, rv_=rv_: "".join(AL[(int(d) + k_ - 1) % 26]
                                                               for d in (n[::-1] if rv_ else n))
dl = DIGL["2,True"]
assert dl("2735") == "GEID" and dl("6418") == "JCFH"
ans = inferred([("2735", "GEID"), ("6418", "JCFH")], "9504", dl("9504"), DIGL)
assert ans == "FBGK"
mcq(COD, NC, "Advanced", "In a certain code, 2735 is written as GEID and 6418 is written as JCFH. How is 9504 written "
    "in that code?", ans, ["KGBF", "EAFJ", "FBGJ"], "Reverse the digits, then turn each digit into a letter",
    "2735 reversed is 5372; each digit d becomes the (d + 2)-th letter: 5 → G, 3 → E, 7 → I, 2 → D: GEID. 6418 → 8146 "
    "→ J C F H. 9504 → 4059 → 4 → F, 0 → B, 5 → G, 9 → K: FBGK.",
    ["Reverse: 9504 → 4059", "Digit d → letter number d + 2", "4 F, 0 B, 5 G, 9 K"],
    why_others_wrong="KGBF skips the reversal; EAFJ uses the (d + 1)-th letter; FBGJ codes 9 as the 10th letter.",
    seconds=85, verified_by=RECOMP)
sx = NRULES["sum×len"]
assert sx("TEA") == 78 and sx("PIN") == 117
ans = inferred([("TEA", 78), ("PIN", 117)], "ROPE", sx("ROPE"), NRULES)
assert ans == 216
mcq(COD, NC, "Advanced", "In a certain code, TEA is written as 78 and PIN is written as 117. How is ROPE written in that "
    "code?", str(ans), ["54", "58", "220"], "Sum of positions multiplied by the number of letters",
    "TEA: (20 + 5 + 1) × 3 = 78. PIN: (16 + 9 + 14) × 3 = 117. ROPE: (18 + 15 + 16 + 5) × 4 = 54 × 4 = 216.",
    ["TEA 26 × 3 = 78 ✓; PIN 39 × 3 = 117 ✓", "ROPE 54 × 4 = 216"],
    why_others_wrong="54 is the plain sum; 58 adds the length instead of multiplying; 220 takes P as 17.", natural=int,
    seconds=75, verified_by=RECOMP)

# ---------------------------------------------------------------- Alphanumeric series: Basic
terms = [f"{AL[26 - 2 * i - 1]}{2 * i + 1}" for i in range(5)]
assert terms == ["Z1", "X3", "V5", "T7", "R9"]
mcq(ALN, SN, "Basic", "Which term should replace the question mark in the series?\n\nZ1, X3, V5, T7, ?", terms[-1],
    ["S9", "R8", "Q9"], "Two simple patterns side by side",
    "The letters go back two places each time (Z, X, V, T, R) and the numbers are the odd numbers 1, 3, 5, 7, 9. The "
    "next term is R9.", ["Letters −2: Z X V T ⇒ R", "Numbers +2: 1 3 5 7 ⇒ 9"],
    why_others_wrong="S9 moves the letter back only once; R8 breaks the odd-number pattern; Q9 moves the letter three "
                     "places.", seconds=30, verified_by=RECOMP)
SR = "D # 4 K @ E 7 M $ A 2 % O 9 P & U 3".split()
hits = [(SR[i], SR[i + 1]) for i in range(len(SR) - 1) if is_s(SR[i]) and SR[i + 1] in VOW]
a, w = count_opts(len(hits))
assert len(hits) == 4
mcq(ALN, SN, "Basic", series_intro(fmt(SR)) + "\n\nHow many symbols in the arrangement are immediately followed by a "
    "vowel?", a, w, "Look at the right neighbour of every symbol",
    "Symbols and their right neighbours: " + ", ".join(f"{SR[i]} {SR[i + 1]}" for i in range(len(SR) - 1)
                                                        if is_s(SR[i])) +
    ". Followed by a vowel: " + ", ".join(f"{x_} {y_}" for x_, y_ in hits) + f" — {len(hits)}.",
    ["Symbols: " + ", ".join(t for t in SR if is_s(t)), "Vowels: A, E, O, U"], natural=by_num, seconds=40,
    verified_by=RECOMP)

# ---------------------------------------------------------------- Alphanumeric series: Intermediate set A
SR = "B 5 @ H 2 J % 8 E K 3 © 6 N U # 9 W 1 * L 4 A $".split()
assert len(SR) == 24
sid = stimulus("data_table", "Arrangement of 24 elements beginning with B", series_intro(fmt(SR)), None,
               "Number the elements 1 to 24 from the left (k-th from the right = (25 − k)-th from the left). Vowels: "
               "E, U, A.")
AQ = lambda sub, text, correct, wrongs, concept, expl, steps, **kw: mcq(
    ALN, sub, "Intermediate", text, correct, wrongs, concept, expl, steps, stimulus=sid, verified_by=RECOMP, **kw)
hits = [i for i in range(1, len(SR) - 1) if is_s(SR[i]) and is_d(SR[i - 1]) and CONS(SR[i + 1])]
a, w = count_opts(len(hits))
AQ(SN, "Count the symbols that have a number as their left-hand neighbour and a consonant as their right-hand "
   "neighbour. How many such symbols are there?", a, w, "Both neighbours must match",
   "Each symbol with its neighbours: " + ", ".join(f"{SR[i - 1]} {SR[i]} {SR[i + 1] if i + 1 < len(SR) else '(end)'}"
                                                   for i in range(1, len(SR)) if is_s(SR[i])) +
   ". Number before and consonant after: " + (", ".join(f"{SR[i - 1]} {SR[i]} {SR[i + 1]}" for i in hits) or "none")
   + f" — {len(hits)}.", ["List every symbol with both neighbours", "Keep number–symbol–consonant"],
   natural=by_num, seconds=60)
j_ = len(SR) - 9 - 4
ans = SR[j_]
AQ(PB, "Which element is 4th to the left of the 9th element from the right end?", ans, near(SR, j_),
   "Convert a right-end position, then move left",
   f"The 9th from the right is the {len(SR) - 8}th from the left ({SR[len(SR) - 9]}). Four places to its left is the "
   f"{j_ + 1}th element: {ans}.", [f"9th from the right = 25 − 9 = 16th = {SR[len(SR) - 9]}", f"16 − 4 = 12th ⇒ {ans}"],
   seconds=50)
nums_i = [i for i, t in enumerate(SR) if is_d(t)]
sym_i = [i for i, t in enumerate(SR) if is_s(t)]
p1, p2 = nums_i[2], sym_i[-2]
assert (p1 + p2) % 2 == 0
ans = SR[(p1 + p2) // 2]
AQ(PB, "Which element is exactly midway between the 3rd number from the left end and the 2nd symbol from the right "
   "end?", ans, near(SR, (p1 + p2) // 2), "Locate both reference elements first",
   f"Numbers from the left: {', '.join(SR[i] for i in nums_i[:3])} — the 3rd is {SR[p1]} ({ordn(p1 + 1)}). Symbols "
   f"from the right: {', '.join(SR[i] for i in sym_i[::-1][:2])} — the 2nd is {SR[p2]} ({ordn(p2 + 1)}). Midway: "
   f"({p1 + 1} + {p2 + 1}) ÷ 2 = {(p1 + p2) // 2 + 1}th: {ans}.",
   [f"3rd number from the left = {SR[p1]} at {p1 + 1}", f"2nd symbol from the right = {SR[p2]} at {p2 + 1}",
    f"Midway = {(p1 + p2) // 2 + 1}th ⇒ {ans}"], seconds=70)
grp = lambda i: f"{SR[i]} {SR[i - 1]} {SR[i + 3]}"
GOOD = [grp(i) for i in (3, 9, 16)]
odd_i = 12
ODD = f"{SR[odd_i]} {SR[odd_i - 1]} {SR[odd_i + 2]}"
pattern_fits = lambda g: any(grp(i) == g for i in range(1, len(SR) - 3))
assert all(pattern_fits(g) for g in GOOD) and not pattern_fits(ODD) and len(set(GOOD + [ODD])) == 4
AQ(PB, "Three of the following four groups are formed in the same way on the basis of their positions in the "
   "arrangement. Which group does NOT belong to them?", ODD, GOOD, "Find the rule from the groups that agree",
   f"In '{GOOD[0]}', '{GOOD[1]}' and '{GOOD[2]}', the second element is immediately to the left of the first, and the "
   f"third element is 3rd to the right of the first. In '{ODD}', the third element is only 2nd to the right of "
   f"{SR[odd_i]} (the 3rd to its right is {SR[odd_i + 3]}).",
   ["Rule: X, the element just left of X, the element 3rd right of X", f"{ODD}: third element breaks the rule"],
   seconds=75)

# ---------------------------------------------------------------- Alphanumeric series: Intermediate set B
SR = "7 R £ T 3 9 G ¥ A 4 6 € Q 2 D I 8 5 Z ! M 1 E".split()
assert len(SR) == 23
sid = stimulus("data_table", "Arrangement of 23 elements beginning with 7", series_intro(fmt(SR)), None,
               "Number the elements 1 to 23 from the left. Vowels: A, I, E.")
AQ = lambda sub, text, correct, wrongs, concept, expl, steps, **kw: mcq(
    ALN, sub, "Intermediate", text, correct, wrongs, concept, expl, steps, stimulus=sid, verified_by=RECOMP, **kw)
nb = [i for i, t in enumerate(SR) if is_d(t) and ((i > 0 and is_d(SR[i - 1])) or (i + 1 < len(SR) and is_d(SR[i + 1])))]
a, w = count_opts(len(nb))
AQ(SN, "How many numbers in the arrangement have another number as at least one of their immediate neighbours?", a, w,
   "Look for runs of numbers", "Numbers standing next to another number: " + ", ".join(SR[i] for i in nb) +
   f" (in the pairs 3 9, 4 6 and 8 5) — {len(nb)} numbers.", ["Adjacent number pairs: 3 9, 4 6, 8 5",
                                                                "Each pair gives two numbers"], natural=by_num,
   seconds=55)
rv12 = SR[:12][::-1] + SR[12:]
ns_ = [t for t in rv12 if not is_s(t)]
ans = ns_[4]
AQ(PB, "If the first twelve elements are written in reverse order and then all the symbols are removed, which element "
   "will be 5th from the left end?", ans, near(ns_, 4), "Reverse first, then delete, then count",
   "Reversing the first twelve gives " + fmt(rv12) + ". Without symbols: " + fmt(ns_) + f". The 5th from the left is "
   f"{ans}.", ["Reverse elements 1–12", "Remove £, ¥, €, !", f"5th ⇒ {ans}"], seconds=70)
hits = [i for i in range(1, len(SR)) if SR[i] in VOW and is_s(SR[i - 1])]
a, w = count_opts(len(hits))
AQ(SN, "How many vowels in the arrangement are immediately preceded by a symbol?", a, w,
   "Check the left neighbour of every vowel",
   "Vowels with their left neighbours: " + ", ".join(f"{SR[i - 1]} {SR[i]}" for i in range(1, len(SR))
                                                     if SR[i] in VOW) + ". Preceded by a symbol: " +
   (", ".join(f"{SR[i - 1]} {SR[i]}" for i in hits) or "none") + f" — {len(hits)}.",
   ["Vowels: A, I, E", "Left neighbours: ¥, D, 1"], natural=by_num, seconds=50)

# ---------------------------------------------------------------- Alphanumeric series: Advanced (pattern)
pr_ = [2, 3, 5, 7, 11]
lp = [2]
for d_ in (2, 3, 4, 5):
    lp.append(lp[-1] + d_)
terms = [f"{p}{AL[l - 1]}{p * p}" for p, l in zip(pr_, lp)]
assert terms == ["2B4", "3D9", "5G25", "7K49", "11P121"]
mcq(ALN, SN, "Advanced", "Which term should replace the question mark in the series?\n\n2B4, 3D9, 5G25, 7K49, ?",
    terms[-1], ["11O121", "9P81", "11P111"], "Three patterns in one term",
    "First numbers: the primes 2, 3, 5, 7 ⇒ 11. Last numbers: their squares 4, 9, 25, 49 ⇒ 121. Letters: B, D, G, K "
    "move forward 2, 3, 4 places ⇒ next +5: K (11) + 5 = P (16). The term is 11P121.",
    ["Primes: 2, 3, 5, 7 ⇒ 11", "Squares ⇒ 121", "Letters +2, +3, +4 ⇒ +5: P"],
    why_others_wrong="11O121 moves the letter only 4 places; 9P81 takes 9, which is not prime; 11P111 breaks the "
                     "square pattern.", seconds=70, verified_by=RECOMP)

# ---------------------------------------------------------------- Alphabet test: Basic
wd = "MOTHER"
sw_ = sorted(wd)
ans = sw_[2]
assert fmt(sw_) == "E H M O R T" and ans == "M"
mcq(ABT, LP, "Basic", "If the letters of the word 'MOTHER' are arranged in alphabetical order from left to right, which "
    "letter will be 3rd from the left end?", ans, ["H", "O", "T"], "Sort the letters first",
    "In alphabetical order the letters are E, H, M, O, R, T. The 3rd from the left is M.", ["Sorted: E H M O R T",
                                                                                           "3rd ⇒ M"],
    why_others_wrong="H is 2nd and O 4th in the sorted order; T is the 3rd letter of MOTHER itself.", seconds=30,
    verified_by=RECOMP)

# ---------------------------------------------------------------- Number questions: Basic set (digit sequence)
DS = "4 7 2 9 3 8 5 1 6 3 9 2 7 4 8 1 5 3 6".split()
DI = [int(d) for d in DS]
sid = stimulus("data_table", "A sequence of nineteen digits",
               "Study the following sequence of digits and answer the questions.\n\n" + fmt(DS), None,
               "Number the digits 1 to 19 from the left; the k-th from the right is the (20 − k)-th from the left.")
NQ = lambda sub, text, correct, wrongs, concept, expl, steps, **kw: mcq(
    NSR, sub, "Basic", text, correct, wrongs, concept, expl, steps, stimulus=sid, verified_by=RECOMP, **kw)
hits = [i for i in range(1, len(DI)) if DI[i] == 3 and DI[i - 1] % 2]
a, w = count_opts(len(hits))
assert len(hits) == 2
NQ(NDO, "How many 3s in the sequence are immediately preceded by an odd digit?", a, w, "Check the left neighbour of "
                                                                                       "every 3",
   "The 3s and their left neighbours: " + ", ".join(f"{DI[i - 1]} 3" for i in range(1, len(DI)) if DI[i] == 3) +
   ". Odd left neighbour: 9 3 and 5 3 — two.", ["Find every 3", "Keep those with an odd digit on the left"],
   natural=by_num, seconds=40)
hits = [i for i in range(len(DI) - 1) if DI[i] % 2 == 0 and DI[i + 1] % 2]
a, w = count_opts(len(hits))
NQ(NDO, "How many even digits in the sequence are immediately followed by an odd digit?", a, w,
   "Check the right neighbour of every even digit",
   "Even digits followed by an odd digit: " + ", ".join(f"{DI[i]} {DI[i + 1]}" for i in hits) + f" — {len(hits)}.",
   ["Even digits: 4, 2, 8, 6, 2, 4, 8, 6", "Keep those with an odd digit on the right"], natural=by_num, seconds=50)
ans = DS[9 - 1 + 5]
NQ(NDO, "Which digit is 5th to the right of the 9th digit from the left end?", ans,
   [d for d in (DS[12], DS[14], DS[8], DS[3]) if d != ans][:3], "Add when moving right",
   f"The 9th digit is {DS[8]}. Five places to its right is the 14th digit: {ans}.", [f"9th = {DS[8]}",
                                                                                     f"9 + 5 = 14th ⇒ {ans}"],
   why_others_wrong="The other digits stand at the 13th, 15th or 9th place.", seconds=35)
tot = DI[3] + DI[-4]
assert (DI[3], DI[-4], tot) == (9, 1, 10) and (DI[-2], DI[-3], DI[-5]) == (3, 5, 8)
NQ(NDO, "What is the sum of the 4th digit from the left end and the 4th digit from the right end?", str(tot),
   ["12", "14", "17"], "Count from each end", "The 4th from the left is 9; the 4th from the right (16th from the left) "
                                               "is 1. 9 + 1 = 10.", ["4th from the left = 9", "4th from the right = 1",
                                                                      "9 + 1 = 10"],
   why_others_wrong="12, 14 and 17 pair the 9 with the 2nd (3), 3rd (5) and 5th (8) digit from the right instead of "
                    "the 4th.", natural=int, seconds=40)

# ---------------------------------------------------------------- Number questions: Advanced set (digit sequence)
DA = "3 6 4 9 1 8 2 5 7 3 6 1 4 9 2 8 1 6 5 3 7 2".split()
DJ = [int(d) for d in DA]
sid = stimulus("data_table", "A sequence of twenty-two digits",
               "Study the following sequence of digits and answer the questions.\n\n" + fmt(DA), None,
               "Number the digits 1 to 22 from the left. A two-digit number formed by adjacent digits is read from left "
               "to right.")
NQ = lambda sub, text, correct, wrongs, concept, expl, steps, **kw: mcq(
    NSR, sub, "Advanced", text, correct, wrongs, concept, expl, steps, stimulus=sid, verified_by=RECOMP, **kw)
SQS = {16, 25, 36, 49, 64, 81}
sq = [f"{DJ[i]}{DJ[i + 1]}" for i in range(len(DJ) - 1) if DJ[i] * 10 + DJ[i + 1] in SQS]
a, w = count_opts(len(sq))
NQ(NDO, "How many times do two adjacent digits, read from left to right, form a two-digit perfect square?", a, w,
   "Two-digit squares are 16, 25, 36, 49, 64 and 81",
   "Adjacent pairs that are squares: " + ", ".join(sq) + f" — {len(sq)}.",
   ["Squares to look for: 16, 25, 36, 49, 64, 81", "Scan each adjacent pair: " + ", ".join(sq)], natural=by_num,
   seconds=80)
mins = [i for i in range(1, len(DJ) - 1) if DJ[i] < DJ[i - 1] and DJ[i] < DJ[i + 1]]
a, w = count_opts(len(mins))
NQ(NDO, "How many digits in the sequence are smaller than both of their immediate neighbours?", a, w,
   "A digit with a larger digit on each side",
   "Such digits (with their neighbours): " + ", ".join(f"{DJ[i - 1]} {DJ[i]} {DJ[i + 1]}" for i in mins) +
   f" — {len(mins)}.", ["Check every inner digit against both neighbours"], natural=by_num, seconds=80)
NEWD = [9 - d if d % 2 else d for d in DJ]
picks = [NEWD[2], NEWD[7], NEWD[14]]
tot = sum(picks)
NQ(NDO, "If every odd digit in the sequence is replaced by (9 − that digit) and every even digit is left unchanged, what "
   "is the sum of the 3rd, 8th and 15th digits of the new sequence?", str(tot),
   [str(DJ[2] + DJ[7] + DJ[14]), str(tot + 2), str(tot - 3)], "Only odd digits change",
   f"Original 3rd, 8th and 15th digits: {DJ[2]}, {DJ[7]}, {DJ[14]}. Odd ones change to 9 − d: "
   + ", ".join(f"{DJ[i]} → {NEWD[i]}" for i in (2, 7, 14)) + f". Sum = {' + '.join(map(str, picks))} = {tot}.",
   [f"3rd {DJ[2]}, 8th {DJ[7]}, 15th {DJ[14]}", "Odd d → 9 − d", f"Sum = {tot}"],
   why_others_wrong=f"{DJ[2] + DJ[7] + DJ[14]} adds the original digits; the other two misapply the change to one "
                    "digit.", natural=int, seconds=80)
assert len({str(tot), str(DJ[2] + DJ[7] + DJ[14]), str(tot + 2), str(tot - 3)}) == 4
tri = [i for i in range(1, len(DJ) - 1) if DJ[i] == DJ[i - 1] + DJ[i + 1]]
a, w = count_opts(len(tri))
NQ(NDO, "In how many groups of three adjacent digits is the middle digit equal to the sum of the other two?", a, w,
   "Test every window of three", "Qualifying groups: " + (", ".join(f"{DJ[i - 1]} {DJ[i]} {DJ[i + 1]}" for i in tri)
                                                          or "none") + f" — {len(tri)}.",
   ["Slide a window of three digits", "Middle = left + right?"], natural=by_num, seconds=85)


# ================================================================================================ BATCH 010
begin("010")
# ---------------------------------------------------------------- Blood relations: Basic set (three codes)
CODE10 = {"%": "daughter", "&": "husband", "!": "father"}
sid = stimulus("passage", "Three symbol codes for relations",
               "In a certain code:\n'P % Q' means 'P is the daughter of Q';\n'P & Q' means 'P is the husband of Q';\n"
               "'P ! Q' means 'P is the father of Q'.", None,
               "Decode pair by pair from the left; the parents of a child are a married couple.")
BQ = lambda text, correct, wrongs, concept, expl, steps, **kw: mcq(
    BLD, CDB, "Basic", text, correct, wrongs, concept, expl, steps, stimulus=sid, verified_by=RECOMP, **kw)
F = Family().add("Y", "M").add("Z", "F").marry("Y", "Z").add("X", "F", "Y", "Z")
F.check(coded_facts("X % Y & Z", CODE10))
ans = F.rel("Z", "X")
assert ans == "mother"
BQ("If 'X % Y & Z', how is Z related to X?", cap(ans), ["Sister", "Grandmother", "Daughter"],
   "The wife of one's father is one's mother", "X is Y's daughter and Y is Z's husband, so Z is X's mother.",
   ["X % Y: X is Y's daughter", "Y & Z: Z is Y's wife ⇒ X's mother"],
   why_others_wrong="Z is a generation above X, so not her sister or daughter; nothing puts her two generations "
                    "above.", seconds=30)
F = Family().add("M", "M").add("Mw", "F").marry("M", "Mw").add("N", "M", "M", "Mw").add("O", "F").marry("N", "O")
F.check(coded_facts("M ! N & O", CODE10))
ans = F.rel("O", "M")
assert ans == "daughter-in-law"
BQ("If 'M ! N & O', how is O related to M?", cap(ans), ["Daughter", "Wife", "Sister"],
   "A son's wife is a daughter-in-law", "M is N's father and N is O's husband, so O is the wife of M's son: M's "
                                        "daughter-in-law.", ["M ! N: N is M's son (a husband is male)",
                                                             "N & O: O is N's wife ⇒ daughter-in-law"],
   why_others_wrong="O is married into the family, not M's own daughter; M's wife is N's mother; O is a generation "
                    "below M.", seconds=35)
F = Family().add("R", "M").add("T", "F").marry("R", "T").add("S", "F", "R", "T")
F.check(coded_facts("R ! S % T", CODE10))
ans = F.rel("T", "R")
assert ans == "wife"
BQ("If 'R ! S % T', how is T related to R?", cap(ans), ["Daughter", "Sister", "Mother"],
   "Two parents of one child", "R is S's father; S is T's daughter, so T is S's other parent, her mother. T is "
                               "therefore R's wife.", ["R ! S: R is S's father", "S % T: T is S's parent ⇒ mother",
                                                        "Father and mother of S ⇒ T is R's wife"],
   why_others_wrong="S is the daughter; T and R are S's two parents, so T is neither R's sister nor his mother.",
   seconds=35)

# ---------------------------------------------------------------- Blood relations: Basic (standalone)
F = Family().add("Uh", "M").add("Usha", "F").marry("Uh", "Usha").add("Vinay", "M", "Uh", "Usha")
F.add("Wamiqa", "F", "Uh", "Usha").add("Xavier", "M").marry("Xavier", "Wamiqa")
F.check([("Usha", "mother", "Vinay"), ("Vinay", "brother", "Wamiqa"), ("Xavier", "husband", "Wamiqa")])
ans = F.rel("Usha", "Xavier")
assert ans == "mother-in-law"
mcq(BLD, DRB, "Basic", "Usha is the mother of Vinay. Vinay is the brother of Wamiqa, and Xavier is Wamiqa's husband. "
    "How is Usha related to Xavier?", cap(ans), ["Mother", "Sister-in-law", "Aunt"], "Wife's mother = mother-in-law",
    "Vinay and Wamiqa are siblings, so Usha is Wamiqa's mother too. Xavier is Wamiqa's husband, so Usha is his "
    "mother-in-law.", ["Usha = mother of Vinay and Wamiqa", "Wife's mother ⇒ mother-in-law"],
    why_others_wrong="Xavier is not Usha's own son; she is a generation above him, so not his sister-in-law; an aunt "
                     "is a parent's sister.", seconds=30, verified_by=RECOMP)
F = Family().add("Eshwar", "M").add("Ew", "F").marry("Eshwar", "Ew").add("Deepak", "M", "Eshwar", "Ew")
F.add("Geeta", "F", "Eshwar", "Ew").add("Gh", "M").marry("Gh", "Geeta").add("Farida", "F", "Gh", "Geeta")
F.check([("Deepak", "son", "Eshwar"), ("Geeta", "sister", "Deepak"), ("Farida", "daughter", "Geeta")])
ans = F.rel("Deepak", "Farida")
assert ans == "uncle"
mcq(BLD, DRB, "Basic", "Deepak is the only son of Eshwar. Geeta is Deepak's sister, and Farida is Geeta's daughter. How "
    "is Deepak related to Farida?", cap(ans), ["Father", "Brother", "Grandfather"], "Mother's brother = uncle",
    "Deepak is the brother of Farida's mother Geeta, so he is Farida's (maternal) uncle.",
    ["Geeta = Farida's mother", "Deepak = Geeta's brother ⇒ uncle"],
    why_others_wrong="Farida's father is Geeta's husband; Deepak is a generation above Farida, so not her brother; "
                     "her grandfather is Eshwar.", seconds=30, verified_by=RECOMP)
F = Family().add("Hari", "M").add("Ila", "F").marry("Hari", "Ila").add("Jai", "M", "Hari", "Ila")
F.add("Kiya", "F").marry("Jai", "Kiya").add("Lina", "F", "Jai", "Kiya")
F.check([("Hari", "husband", "Ila"), ("Jai", "son", "Ila"), ("Kiya", "wife", "Jai"), ("Lina", "daughter", "Kiya")])
ans = F.rel("Hari", "Lina")
assert ans == "grandfather"
mcq(BLD, DRB, "Basic", "Hari is the husband of Ila. Ila's only son is Jai, and Jai's wife is Kiya. Lina is Kiya's "
    "daughter. How is Hari related to Lina?", cap(ans), ["Father", "Uncle", "Father-in-law"],
    "Father's father = grandfather", "Jai is the son of Hari and Ila, and Lina is the daughter of Jai and his wife "
                                     "Kiya. Hari is Lina's father's father: her grandfather.",
    ["Jai = Hari's son", "Lina = Jai's daughter ⇒ Hari is her grandfather"],
    why_others_wrong="Lina's father is Jai; Hari is two generations above her; he is Kiya's father-in-law, not "
                     "Lina's.", seconds=30, verified_by=RECOMP)

# ---------------------------------------------------------------- Blood relations: Intermediate (standalone)
F = Family().add("Kf", "M").add("Km", "F").marry("Kf", "Km").add("Kd", "M", "Kf", "Km").add("Ka", "F", "Kf", "Km")
F.add("Kdw", "F").marry("Kd", "Kdw").add("Kunal", "M", "Kd", "Kdw")
assert F.rel("Ka", "Kunal") == "aunt" and F.siblings("Kd") == {"Ka"}
F.add("Kah", "M").marry("Kah", "Ka").add("Cz", "M", "Kah", "Ka").add("Woman", "F").marry("Cz", "Woman")
assert F.rel("Ka", "Cz") == "mother" and F.rel("Cz", "Kunal") == "cousin" and F.sp["Woman"] == "Cz"
mcq(BLD, DRB, "Intermediate", "Looking at the photograph of a woman, Kunal said, \"Her husband's mother is the only "
    "sister of my father.\" How is the woman related to Kunal?", "Wife of his cousin",
    ["Sister", "Aunt", "Cousin"], "Collapse the phrase from the inside out",
    "The only sister of Kunal's father is Kunal's paternal aunt. Her son, the woman's husband, is Kunal's cousin, so "
    "the woman is the wife of Kunal's cousin.", ["Father's sister = Kunal's aunt", "Aunt's son = Kunal's cousin",
                                                  "The woman = cousin's wife"],
    why_others_wrong="She is not a child of Kunal's parents; the aunt is her mother-in-law, not her; she is related to "
                     "Kunal only by marriage, so not his own cousin.", seconds=55, verified_by=RECOMP)
CODEI = {"@": "brother", "#": "mother", "$": "daughter"}
F = Family().add("D", "M").add("B", "F").marry("D", "B").add("Bp", "M").add("Bm", "F").marry("Bp", "Bm")
F.par["B"] = ("Bp", "Bm")
F.add("A", "M", "Bp", "Bm").add("C", "F", "D", "B")
F.check(coded_facts("A @ B # C $ D", CODEI))
assert F.rel("A", "C") == "uncle" and F.rel("D", "B") == "husband" and F.g["C"] == "F" and F.rel("A", "D") != "son"
ans, wr_ = one_false([("A is the uncle of C", True), ("D is the husband of B", True), ("C is a girl", True),
                      ("A is the son of D", False)])
mcq(BLD, CDB, "Intermediate",
    "In a certain code:\n'P @ Q' means 'P is the brother of Q';\n'P # Q' means 'P is the mother of Q';\n'P $ Q' means "
    "'P is the daughter of Q'.\n\nIf 'A @ B # C $ D', which of the following is NOT true?", ans, wr_,
    "Decode, then test each statement",
    "A is B's brother; B is C's mother; C is D's daughter, so D is C's father and B's husband. So A is C's maternal "
    "uncle, D is B's husband and C is a girl — all true. A is B's brother, i.e. D's brother-in-law, not D's son.",
    ["A @ B, B # C ⇒ A is C's maternal uncle", "C $ D with B the mother ⇒ D is the father, B's husband",
     "A is D's brother-in-law ⇒ 'son of D' is false"],
    why_others_wrong="The other three statements follow directly from the code.", seconds=60, verified_by=RECOMP)
F = Family().add("Om", "M").add("Ow", "F").marry("Om", "Ow").add("Usha", "F", "Om", "Ow").add("Varun", "M", "Om", "Ow")
F.add("Uh", "M").marry("Uh", "Usha").add("Tia", "F", "Uh", "Usha").add("Wanda", "F").marry("Varun", "Wanda")
F.check([("Om", "grandfather", "Tia"), ("Usha", "mother", "Tia"), ("Varun", "brother", "Usha"),
         ("Om", "father", "Usha"), ("Wanda", "wife", "Varun")])
ans = F.rel("Wanda", "Tia")
assert ans == "aunt"
mcq(BLD, FPZ, "Intermediate", "Om is the father of Usha, and Tia is Usha's daughter. Usha's only sibling is Varun, and "
    "Wanda is Varun's wife. How is Wanda related to Tia?", cap(ans), ["Mother", "Sister-in-law", "Grandmother"],
    "Wife of the mother's brother", "Varun is the brother of Tia's mother Usha, i.e. Tia's maternal uncle. Wanda, his "
                                    "wife, is Tia's aunt.", ["Varun = Tia's maternal uncle", "Uncle's wife ⇒ aunt"],
    why_others_wrong="Tia's mother is Usha; Wanda is Usha's sister-in-law, not Tia's; Tia's grandmother is Om's wife.",
    seconds=50, verified_by=RECOMP)

# ---------------------------------------------------------------- Blood relations: Advanced set (coded family)
F = Family().add("Kartik", "M").add("Leela", "F").marry("Kartik", "Leela")
F.add("Mehul", "M", "Kartik", "Leela").add("Naina", "F", "Kartik", "Leela")
F.add("Ojasvi", "F").marry("Mehul", "Ojasvi").add("Pranav", "M", "Mehul", "Ojasvi")
F.add("Qasim", "M").marry("Qasim", "Naina").add("Riya", "F", "Qasim", "Naina")
STM = ["Kartik ⊗ Leela", "Leela ⊕ Mehul", "Mehul ⊖ Naina", "Ojasvi ⊗ Mehul", "Ojasvi ⊕ Pranav", "Qasim ⊗ Naina",
       "Qasim ⊕ Riya"]
for s_ in STM:
    a_, op_, b_ = s_.split()
    assert {"⊗": F.sp.get(a_) == b_, "⊕": a_ in F.parents(b_), "⊖": a_ in F.siblings(b_)}[op_], s_
sid = stimulus("puzzle", "A family described in three codes",
               "In a certain code, 'A ⊕ B' means 'A is a parent of B', 'A ⊗ B' means 'A is married to B' and 'A ⊖ B' "
               "means 'A and B are siblings'. Kartik, Mehul, Pranav and Qasim are male; Leela, Naina, Ojasvi and Riya "
               "are female. The following are true:\n\n" + "\n".join(f"- {s_}" for s_ in STM), None,
               "Leela, Kartik's wife, is a parent of Mehul, and Naina is Mehul's sibling, so both are children of "
               "Kartik and Leela. Ojasvi is Mehul's wife and Pranav's mother; Qasim is Naina's husband and Riya's "
               "parent.\nTree: Kartik + Leela → Mehul (+ Ojasvi) → Pranav; Naina (+ Qasim) → Riya.")
TREE10 = "Kartik + Leela → Mehul (+ Ojasvi) → Pranav; Naina (+ Qasim) → Riya"
AQ = lambda text, correct, wrongs, concept, expl, steps, **kw: mcq(
    BLD, FPZ, "Advanced", text, correct, wrongs, concept, expl, steps, stimulus=sid, verified_by=RECOMP, **kw)
ans = F.rel("Qasim", "Pranav")
assert ans == "uncle"
AQ("How is Qasim related to Pranav?", cap(ans), ["Father", "Cousin", "Grandfather"],
   "Husband of the father's sister", "Pranav's father Mehul is Naina's brother, and Qasim is Naina's husband, so Qasim "
                                     "is Pranav's uncle (paternal aunt's husband).",
   [TREE10, "Qasim = husband of Pranav's father's sister ⇒ uncle"],
   why_others_wrong="Pranav's father is Mehul; Qasim's child Riya is Pranav's cousin; his grandfather is Kartik.",
   seconds=85)
ans = F.rel("Leela", "Riya")
assert ans == "grandmother"
AQ("How is Leela related to Riya?", cap(ans), ["Mother", "Aunt", "Mother-in-law"], "Mother's mother",
   "Riya's mother is Naina (Qasim's wife), and Naina is Leela's daughter, so Leela is Riya's grandmother.",
   [TREE10, "Riya → Naina → Leela"],
   why_others_wrong="Riya's mother is Naina; Leela is two generations above Riya; she is Qasim's mother-in-law, not "
                    "Riya's.", seconds=80)
ans = F.rel("Ojasvi", "Naina")
assert ans == "sister-in-law"
AQ("How is Ojasvi related to Naina?", cap(ans), ["Sister", "Mother-in-law", "Cousin"],
   "Brother's wife = sister-in-law", "Ojasvi is married to Mehul, Naina's brother, so Ojasvi is Naina's "
                                     "sister-in-law.", [TREE10, "Ojasvi = wife of Naina's sibling"],
   why_others_wrong="Ojasvi has different parents from Naina; she is in Naina's generation, so not her mother-in-law; "
                    "cousins share grandparents.", seconds=80)

# ---------------------------------------------------------------- Blood relations: Advanced (standalone)
F = Family().add("Gf", "M").add("Gm", "F").marry("Gf", "Gm").add("Rf", "M", "Gf", "Gm").add("Aunt", "F", "Gf", "Gm")
F.add("Sahil", "M").marry("Sahil", "Aunt").add("Rm", "F").marry("Rf", "Rm").add("Rohan", "M", "Rf", "Rm")
assert F.rel("Sahil", "Gf") == "son-in-law" and F.siblings("Rf") == {"Aunt"}
ans = F.rel("Sahil", "Rohan")
assert ans == "uncle"
mcq(BLD, FPZ, "Advanced", "Sahil is the only son-in-law of Rohan's paternal grandfather. Rohan's father has exactly one "
    "sibling, and every person mentioned has only one spouse. How is Sahil related to Rohan?", "Uncle (husband of "
                                                                                                "his father's sister)",
    ["Father", "Brother-in-law", "Cousin"], "A son-in-law must be married to a daughter",
    "A son-in-law of Rohan's grandfather is married to one of the grandfather's daughters. The grandfather's children "
    "are Rohan's father and his only sibling, so that sibling is a daughter: Rohan's paternal aunt. Sahil is her "
    "husband, i.e. Rohan's uncle.", ["Son-in-law ⇒ husband of a daughter", "Only sibling of Rohan's father ⇒ that "
                                                                           "daughter", "Aunt's husband ⇒ uncle"],
    why_others_wrong="Rohan's father is a son of the grandfather, not a son-in-law; Sahil is a generation above Rohan, "
                     "so not his brother-in-law or cousin.", seconds=85, verified_by=RECOMP)
CODEA = {"©": "mother", "®": "brother", "™": "daughter"}
EX = ["P ™ Q ® S", "S ® Q © P", "P ® Q ™ S", "S © Q ® P"]
F = Family().add("Qf", "M").add("Qm", "F").marry("Qf", "Qm").add("Q", "M", "Qf", "Qm").add("S", "F", "Qf", "Qm")
F.add("Qw", "F").marry("Q", "Qw").add("P", "F", "Q", "Qw")
F.check(coded_facts(EX[0], CODEA))
assert F.rel("P", "S") == "niece"
F2 = Family().add("Qf", "M").add("Q", "F").marry("Qf", "Q").add("Pg", "M").add("Pm", "F").marry("Pg", "Pm")
F2.par["Q"] = ("Pg", "Pm")
F2.add("S", "M", "Pg", "Pm")
r2 = set()
for pg in ("M", "F"):
    F2.add("P", pg, "Qf", "Q")
    F2.check(coded_facts(EX[1], CODEA))
    r2.add(F2.rel("P", "S"))
assert r2 == {"nephew", "niece"}
F3 = Family().add("S", "M").add("Sw", "F").marry("S", "Sw").add("P", "M", "S", "Sw").add("Q", "F", "S", "Sw")
F3.check(coded_facts(EX[2], CODEA))
assert F3.rel("P", "S") == "son"
F4 = Family().add("Sh", "M").add("S", "F").marry("Sh", "S").add("Q", "M", "Sh", "S").add("P", "F", "Sh", "S")
F4.check(coded_facts(EX[3], CODEA))
assert F4.rel("S", "P") == "mother"
mcq(BLD, CDB, "Advanced",
    "In a certain code:\n'A © B' means 'A is the mother of B';\n'A ® B' means 'A is the brother of B';\n'A ™ B' means "
    "'A is the daughter of B'.\n\nWhich of the following expressions definitely means that P is the niece of S?",
    EX[0], EX[1:], "Test every option; the gender of P must be fixed",
    "In 'P ™ Q ® S', P is Q's daughter and Q is S's brother, so P is the daughter of S's brother: S's niece. In "
    "'S ® Q © P', S is the brother of P's mother, but P's gender is unknown (nephew or niece). 'P ® Q ™ S' makes P "
    "S's son, and 'S © Q ® P' makes S P's mother.",
    ["Option 1: daughter of S's brother ⇒ niece ✓", "Option 2: P's gender unknown", "Options 3 and 4: son / mother"],
    why_others_wrong="The second does not fix P's gender; the third and fourth give son and mother.", seconds=85,
    verified_by=RECOMP)

# ---------------------------------------------------------------- Direction: Basic
face = turn("E", "L")
assert NAME[face] == "North"
mcq(DIR, SH_, "Basic", "Early one morning, Kavya walked straight towards the sun. She then turned to her left and kept "
    "walking. In which direction was she walking then?", NAME[face], ["South", "West", "East"],
    "The morning sun is in the east", "Walking towards the morning sun means walking east. A left turn from east "
                                      "points north.", ["Towards the morning sun ⇒ east", "Left of east ⇒ north"],
    why_others_wrong="South is a right turn from east; West is away from the sun; East ignores the turn.", seconds=30,
    verified_by=RECOMP)

# ---------------------------------------------------------------- Direction: Intermediate set (taxi route)
PT = {"D": (0, 0)}
PT["A"] = (6, 0)
PT["B"] = (PT["A"][0], PT["A"][1] + 8)
PT["C"] = (PT["B"][0] - 12, PT["B"][1])
PT["E"] = (PT["C"][0], PT["C"][1] - 5)
PT["F"] = (PT["E"][0] + 10, PT["E"][1])
assert PT == {"D": (0, 0), "A": (6, 0), "B": (6, 8), "C": (-6, 8), "E": (-6, 3), "F": (4, 3)}
sid = stimulus("passage", "A taxi's route with five stops",
               "A taxi leaves its depot D and drives in straight lines: 6 km east to stop A, then 8 km north to stop B, "
               "then 12 km west to stop C, then 5 km south to stop E, and finally 10 km east to stop F, where it "
               "ends its trip.", None,
               "With D at (0, 0), east and north positive: A (6, 0), B (6, 8), C (−6, 8), E (−6, 3), F (4, 3).")
MAP10 = "D (0, 0), A (6, 0), B (6, 8), C (−6, 8), E (−6, 3), F (4, 3)"
TQ = lambda sub, text, correct, wrongs, concept, expl, steps, **kw: mcq(
    DIR, sub, "Intermediate", text, correct, wrongs, concept, expl, steps, stimulus=sid, verified_by=RECOMP, **kw)
c, w, why = dd_wrongs(*PT["B"], "km", 14)
TQ(PP, "What is the straight-line distance between the depot and stop B, and in which direction is B from the depot?",
   c, w, "A 6-8-10 triangle", "B is 6 km east and 8 km north of D: √(36 + 64) = 10 km, north-east.",
   [MAP10, "B − D = (6, 8) ⇒ 10 km, North-East"], why_others_wrong=why, seconds=50)
c, w, why = dd_wrongs(*PT["F"], "km", 41)
assert c == "5 km, North-East"
TQ(DD, "How far is the end point F from the depot in a straight line, and in which direction?", c, w,
   "Net displacement of the whole trip", "East: 6 − 12 + 10 = 4 km; north: 8 − 5 = 3 km. √(16 + 9) = 5 km, "
                                         "north-east.", [MAP10, "F = (4, 3) ⇒ 5 km, North-East"],
   why_others_wrong=why, seconds=60)
ans = compass(PT["C"][0] - PT["F"][0], PT["C"][1] - PT["F"][1])
assert ans == "North-West"
TQ(PP, "In which direction is stop C with respect to stop F?", ans, ["South-East", "North-East", "West"],
   "Signs of the two components", "C (−6, 8) − F (4, 3) = (−10, 5): west and north, so C is north-west of F.",
   [MAP10, "C − F = (−10, +5) ⇒ North-West"],
   why_others_wrong="South-East is F's direction from C; North-East misreads C as east of F; West ignores the 5 km "
                    "north component.", seconds=50)
d2 = {k: v[0] ** 2 + v[1] ** 2 for k, v in PT.items() if k != "D"}
ans = min(d2, key=d2.get)
assert ans == "F" and sorted(d2.values())[:2] == [25, 36]
TQ(PP, "Which stop is nearest to the depot in a straight line?", "F", ["A", "E", "B"], "Compare straight-line "
                                                                                       "distances",
   "Distances from D: A 6 km, B 10 km, C 10 km, E √45 ≈ 6.7 km, F 5 km. F is nearest.",
   [MAP10, "DA 6, DB 10, DC 10, DE √45, DF 5"], why_others_wrong="A is 6 km, E about 6.7 km and B 10 km away.",
   seconds=60)

# ---------------------------------------------------------------- Direction: Intermediate (standalone)
fin = (ANG["SE"] - 3 * 135) % 360
assert DEG[fin] == "East"
mcq(DIR, DD, "Intermediate", "A girl is facing south-east. She turns 135° anticlockwise three times in a row. Which "
    "direction is she facing now?", DEG[fin], ["North", "South-West", "South"], "Total turn = 3 × 135°",
    "Three turns of 135° make 405° anticlockwise, which is a full circle plus 45°. 45° anticlockwise from south-east is "
    "east.", ["3 × 135° = 405° = 360° + 45°", "SE (135°) − 45° = 90° = East"],
    why_others_wrong="North and South-West come from stopping after one or two turns; South turns the last 45° the other way.",
    seconds=55, verified_by=RECOMP)
assert DEG[(ANG["SE"] - 135) % 360] == "North" and DEG[(ANG["SE"] - 270) % 360] == "South-West" and DEG[(ANG["SE"] + 45) % 360] == "South"
mcq(DIR, SH_, "Intermediate", "At about 5 pm, Anil and Bhanu were walking straight towards each other on a road. Anil's "
    "shadow fell directly behind him. In which direction was Bhanu walking?", "East", ["West", "North", "South"],
    "Evening shadows point east", "At 5 pm the sun is in the west, so shadows point east. Anil's shadow was behind "
                                  "him, so Anil was walking west, towards the sun. Bhanu, walking towards Anil, was "
                                  "walking east.", ["Evening: shadow points east", "Shadow behind Anil ⇒ Anil walks "
                                                                                   "west", "Bhanu walks the opposite "
                                                                                           "way ⇒ east"],
    why_others_wrong="West is Anil's direction; North and South are at right angles to the road's direction.",
    seconds=50, verified_by=RECOMP)
MV = [(None, 7), ("R", 5), ("L", 4), ("R", 9), ("R", 11)]
x, y = walk("N", MV)
assert (x, y) == (14, 0)
mcq(DIR, DD, "Intermediate", "Sneha cycles 7 km towards the north, turns right and cycles 5 km, turns left and cycles "
    "4 km, turns right and cycles 9 km, and then turns right again and cycles 11 km. How far is she from her starting "
    "point, and in which direction?", "14 km, East", ["14 km, West", "36 km, East", "11 km, South"],
    "North and south legs may cancel", "North 7 + 4 = 11, then south 11: the north–south parts cancel. East 5 + 9 = 14 "
                                       "km. She is 14 km due east of the start.",
    walk_trace("N", MV, "km") + ["Net (14, 0) ⇒ 14 km, East"],
    why_others_wrong="West mixes up the right turns; 36 km adds every leg; 11 km, South is only the last leg.",
    seconds=65, verified_by=RECOMP)

# ---------------------------------------------------------------- Direction: Advanced set (midpoints)
PT = {"K": (0, 0), "J": (10, 0)}
PT["L"] = (PT["J"][0], PT["J"][1] + 10)
PT["M"] = ((PT["K"][0] + PT["L"][0]) / 2, (PT["K"][1] + PT["L"][1]) / 2)
PT["N"] = (PT["M"][0], PT["M"][1] - 5)
PT["O"] = (PT["M"][0] - 7, PT["M"][1])
assert PT == {"K": (0, 0), "J": (10, 0), "L": (10, 10), "M": (5, 5), "N": (5, 0), "O": (-2, 5)}
sid = stimulus("puzzle", "Six points with a midpoint", "Six points J, K, L, M, N and O lie on flat ground.",
               [("J is 10 m east of K.", (), None), ("L is 10 m north of J.", (), None),
                ("M is the midpoint of the straight line joining K and L.", (), None),
                ("N is 5 m south of M.", (), None), ("O is 7 m west of M.", (), None)],
               "With K at (0, 0): J (10, 0), L (10, 10), M (5, 5), N (5, 0), O (−2, 5).")
MAPA = "K (0, 0), J (10, 0), L (10, 10), M (5, 5), N (5, 0), O (−2, 5)"
XQ = lambda sub, text, correct, wrongs, concept, expl, steps, **kw: mcq(
    DIR, sub, "Advanced", text, correct, wrongs, concept, expl, steps, stimulus=sid, verified_by=RECOMP, **kw)
assert PT["N"] == ((PT["K"][0] + PT["J"][0]) / 2, 0)
XQ(PP, "Which point lies exactly midway between K and J?", "N", ["M", "O", "L"], "Drop M onto the line KJ",
   "M = (5, 5) is the midpoint of KL. N is 5 m south of M, i.e. (5, 0), which is exactly halfway along KJ from (0, 0) "
   "to (10, 0).", [MAPA, "Midpoint of KJ = (5, 0) = N"],
   why_others_wrong="M is 5 m north of KJ, O is 2 m west of K's north–south line, and L is 10 m north of J.",
   seconds=80)
XQ(PP, "What is the straight-line distance between K and M, and in which direction is M from K?", "5√2 m, North-East",
   ["5 m, North", "10 m, North-East", "5√2 m, South-West"], "Half of a diagonal",
   "M is the midpoint of KL, and L is 10 m east and 10 m north of K, so M is 5 m east and 5 m north of K: 5√2 m, "
   "north-east.", [MAPA, "M − K = (5, 5) ⇒ 5√2 m, North-East"],
   why_others_wrong="5 m, North ignores the east part; 10 m takes the full side length; South-West is K's direction "
                    "from M.", seconds=85)
assert dist(5, 5) == "5√2"
dx, dy = PT["L"][0] - PT["O"][0], PT["L"][1] - PT["O"][1]
assert (dx, dy) == (12, 5) and dist(dx, dy) == "13"
XQ(PP, "How far is L from O, and in which direction is L from O?", "13 m, North-East",
   ["13 m, South-West", "17 m, North-East", "12 m, East"], "A 5-12-13 triangle",
   "O = (−2, 5) and L = (10, 10): L is 12 m east and 5 m north of O, √(144 + 25) = 13 m, north-east.",
   [MAPA, "L − O = (12, 5) ⇒ 13 m, North-East"],
   why_others_wrong="South-West is O's direction from L; 17 m adds the two parts; 12 m, East ignores the north part.",
   seconds=90)

# ---------------------------------------------------------------- Coding: Basic
ans = inferred([("SALT", "WEPX")], "CORN", shift("CORN", 4))
assert ans == "GSVR"
mcq(COD, LC, "Basic", "In a certain code language, SALT is written as WEPX. How is CORN written in that code "
    "language?", ans, ["YKNJ", "GSVQ", "HTWS"], "Every letter moves forward by the same number of places",
    "S→W, A→E, L→P, T→X: every letter moves 4 places forward. C→G, O→S, R→V, N→R: GSVR.",
    ["S +4 = W, A +4 = E, L +4 = P, T +4 = X", "CORN +4 ⇒ GSVR"],
    why_others_wrong="YKNJ moves the letters back; GSVQ moves N only 3 places; HTWS moves every letter 5 places.",
    seconds=30, verified_by=RECOMP)
d1 = DR2["id1"]
assert d1("5274") == "6385" and d1("3916") == "4027"
ans = inferred([("5274", "6385"), ("3916", "4027")], "8093", d1("8093"), DR2)
assert ans == "9104"
mcq(COD, NC, "Basic", "In a certain code, 5274 is written as 6385 and 3916 is written as 4027. How is 8093 written in "
    "that code?", ans, ["7982", "9105", "3909"], "Add 1 to every digit (9 becomes 0)",
    "5274: each digit + 1 → 6385. 3916 → 4 0 2 7 (9 + 1 = 10, keep 0). 8093 → 9 1 0 4 = 9104.",
    ["Each digit +1, keeping only the units digit", "8093 ⇒ 9104"],
    why_others_wrong="7982 subtracts 1; 9105 adds 2 to the last digit; 3909 reverses the number and changes nothing "
                     "else.", seconds=35, verified_by=RECOMP)

# ---------------------------------------------------------------- Coding: Intermediate
rm2 = LRULES["rev+-2"]
assert rm2("LEMON") == "LMKCJ" and rm2("GRAPE") == "CNYPE"
ans = inferred([("LEMON", "LMKCJ"), ("GRAPE", "CNYPE")], "MELON", rm2("MELON"))
assert ans == "LMJCK"
mcq(COD, LC, "Intermediate", "In a certain code, LEMON is written as LMKCJ and GRAPE is written as CNYPE. How is MELON "
    "written in that code?", ans, ["KCJMLL"[:5], "PQNGO", "LMJCL"], "Reverse, then move each letter back",
    "LEMON reversed is NOMEL; each letter moved 2 places back: L M K C J. GRAPE → EPARG → C N Y P E. MELON → NOLEM → "
    "L M J C K.", ["Reverse: MELON → NOLEM", "Each letter −2 ⇒ LMJCK"],
    why_others_wrong="KCJML shifts without reversing; PQNGO moves the letters forward; LMJCL moves the last letter "
                     "back only once.", seconds=60, verified_by=RECOMP)
hs = DR2["halfswapalt2"]
assert hs("4815") == "3366" and hs("2967") == "8547"
ans = inferred([("4815", "3366"), ("2967", "8547")], "7302", hs("7302"), DR2)
assert ans == "2091"
mcq(COD, NC, "Intermediate", "In a certain code, 4815 is written as 3366 and 2967 is written as 8547. How is 7302 "
    "written in that code?", ans, ["9180", "0273", "2093"], "Swap the halves, then +2 and −2 alternately",
    "4815: the two halves are interchanged → 1548; then the 1st and 3rd digits get +2 and the 2nd and 4th get −2: 3 3 "
    "6 6. 2967 → 6729 → 8 5 4 7. 7302 → 0273 → 0+2 = 2, 2−2 = 0, 7+2 = 9, 3−2 = 1: 2091.",
    ["Swap halves: 7302 → 0273", "+2, −2, +2, −2 ⇒ 2091"],
    why_others_wrong="9180 applies the +2/−2 without swapping; 0273 only swaps; 2093 adds 2 to the last digit.",
    seconds=65, verified_by=RECOMP)

# ---------------------------------------------------------------- Coding: Advanced set (three-part word code)


def wcode(w):
    c = f"{w[-1]}{len(w)}{shift(w[0], 2)}"
    return c[::-1] if len(w) % 2 == 0 else c


sid = stimulus("passage", "A three-part code that depends on word length",
               "In a certain code, a word is written as: its last letter, then the number of letters in the word, "
               "then the letter that comes two places after its first letter in the English alphabet. If the word has "
               "an even number of letters, the whole code is then written in reverse order.\nFor example, TRAIN is "
               "written as N5V and HOME is written as J4E.", None,
               "Odd length: last letter + length + (first letter + 2). Even length: the same three parts, reversed.")
assert wcode("TRAIN") == "N5V" and wcode("HOME") == "J4E"
WQ = lambda text, correct, wrongs, concept, expl, steps, **kw: mcq(
    COD, LC, "Advanced", text, correct, wrongs, concept, expl, steps, stimulus=sid, verified_by=RECOMP, **kw)
ans = wcode("BRIDGE")
assert ans == "D6E"
WQ("How is 'BRIDGE' written in this code?", ans, ["E6D", "D6F", "E6B"], "Even length: reverse the code",
   "BRIDGE: last letter E, 6 letters, B + 2 = D, giving E6D. Six is even, so the code is reversed: D6E.",
   ["Parts: E, 6, D", "Even length ⇒ reverse ⇒ D6E"],
   why_others_wrong="E6D forgets the reversal; D6F reverses but shifts the wrong letter; E6B does not shift B.",
   seconds=70)
ans = wcode("STAMP")
assert ans == "P5U"
WQ("How is 'STAMP' written in this code?", ans, ["U5P", "P5T", "R5U"], "Odd length: no reversal",
   "STAMP: last letter P, 5 letters, S + 2 = U. Five is odd, so the code stays P5U.", ["Parts: P, 5, U",
                                                                                      "Odd length ⇒ P5U"],
   why_others_wrong="U5P reverses an odd-length code; P5T moves S only one place; R5U shifts the last letter.",
   seconds=65)
OPTS = ["PADLOCK", "SHAMROCK", "PARK", "PLUCK"]
cods = {o: wcode(o) for o in OPTS}
assert [o for o in OPTS if cods[o] == "K7R"] == ["PADLOCK"]
WQ("Which of the following words is written as 'K7R' in this code?", "PADLOCK", OPTS[1:], "Read the code back",
   "K7R is not reversed only if the word has an odd number of letters: 7 letters, ending in K, with first letter "
   "R − 2 = P. PADLOCK fits. " + f"SHAMROCK → {cods['SHAMROCK']}, PARK → {cods['PARK']}, PLUCK → {cods['PLUCK']}.",
   ["7 is odd ⇒ no reversal", "Last letter K, first letter P, 7 letters ⇒ PADLOCK"],
   why_others_wrong="SHAMROCK has 8 letters and starts with S; PARK has 4 letters (code reversed); PLUCK has 5.",
   seconds=80)

# ---------------------------------------------------------------- Alphanumeric series: Basic set
SR = "W 3 % H 8 A @ 5 K £ 1 F 7 I # 2 Y".split()
assert len(SR) == 17
sid = stimulus("data_table", "Arrangement of 17 elements beginning with W", series_intro(fmt(SR)), None,
               "Number the elements 1 to 17 from the left; the k-th from the right is the (18 − k)-th from the left.")
AQ = lambda sub, text, correct, wrongs, concept, expl, steps, **kw: mcq(
    ALN, sub, "Basic", text, correct, wrongs, concept, expl, steps, stimulus=sid, verified_by=RECOMP, **kw)
j_ = len(SR) - 6 - 3
ans = SR[j_]
AQ(PB, "Which element is 3rd to the left of the 6th element from the right end?", ans, near(SR, j_),
   "Convert a right-end position, then move left",
   f"The 6th from the right is the {len(SR) - 5}th from the left ({SR[len(SR) - 6]}). Three places to its left is the "
   f"{j_ + 1}th element: {ans}.", [f"6th from the right = 18 − 6 = 12th = {SR[len(SR) - 6]}",
                                   f"12 − 3 = 9th ⇒ {ans}"], seconds=35)
hits = [(SR[i], SR[i + 1]) for i in range(len(SR) - 1) if is_d(SR[i]) and is_l(SR[i + 1])]
a, w = count_opts(len(hits))
AQ(SN, "How many numbers in the arrangement are immediately followed by a letter?", a, w,
   "Look at the right neighbour of every number",
   "Numbers and their right neighbours: " + ", ".join(f"{SR[i]} {SR[i + 1]}" for i in range(len(SR) - 1)
                                                      if is_d(SR[i])) +
   ". Followed by a letter: " + ", ".join(f"{x_} {y_}" for x_, y_ in hits) + f" — {len(hits)}.",
   ["Numbers: " + ", ".join(t for t in SR if is_d(t)), "Keep those with a letter on the right"], natural=by_num,
   seconds=40)
nn = [t for t in SR if not is_d(t)]
ans = nn[6]
AQ(PB, "If all the numbers are removed from the arrangement, which element will be 7th from the left end?", ans,
   near(nn, 6), "Delete first, then count", "Without numbers: " + fmt(nn) + f". The 7th from the left is {ans}.",
   ["Remove " + ", ".join(t for t in SR if is_d(t)), f"7th ⇒ {ans}"], seconds=40)

# ---------------------------------------------------------------- Alphanumeric series: Basic (standalone)
terms = [f"{AL[3 * i - 1]}{3 * i}" for i in range(1, 6)]
assert terms == ["C3", "F6", "I9", "L12", "O15"]
mcq(ALN, SN, "Basic", "Which term should replace the question mark in the series?\n\nC3, F6, I9, L12, ?", terms[-1],
    ["O14", "N15", "P15"], "The number is the letter's position",
    "The letters move 3 places forward each time (C, F, I, L, O) and each number is its letter's position (3, 6, 9, "
    "12, 15). The next term is O15.", ["Letters +3: L ⇒ O", "O is the 15th letter ⇒ O15"],
    why_others_wrong="O14 and N15 break the link between the letter and its position; P15 moves the letter 4 places.",
    seconds=30, verified_by=RECOMP)
SR = "T % A 6 # E @ 9 U $ R I ¥ 4 O & B".split()
hits = [(SR[i], SR[i + 1]) for i in range(len(SR) - 1) if SR[i] in VOW and is_s(SR[i + 1])]
a, w = count_opts(len(hits))
mcq(ALN, SN, "Basic", series_intro(fmt(SR)) + "\n\nHow many vowels in the arrangement are immediately followed by a "
    "symbol?", a, w, "Look at the right neighbour of every vowel",
    "Vowels and their right neighbours: " + ", ".join(f"{SR[i]} {SR[i + 1]}" for i in range(len(SR) - 1)
                                                       if SR[i] in VOW) +
    ". Followed by a symbol: " + ", ".join(f"{x_} {y_}" for x_, y_ in hits) + f" — {len(hits)}.",
    ["Vowels: A, E, U, I, O", "Keep those with a symbol on the right"], natural=by_num, seconds=40,
    verified_by=RECOMP)

# ---------------------------------------------------------------- Alphanumeric series: Intermediate set
SR = "M 4 & D U 7 © S 2 E # K 9 V £ 3 A Z 6 % H O 8 $".split()
assert len(SR) == 24
sid = stimulus("data_table", "Arrangement of 24 elements beginning with M", series_intro(fmt(SR)), None,
               "Number the elements 1 to 24 from the left (k-th from the right = (25 − k)-th from the left). Vowels: "
               "U, E, A, O.")
AQ = lambda sub, text, correct, wrongs, concept, expl, steps, **kw: mcq(
    ALN, sub, "Intermediate", text, correct, wrongs, concept, expl, steps, stimulus=sid, verified_by=RECOMP, **kw)
nx = [shift(t, 1) if is_l(t) else t for t in SR]
vw = [t for t in nx if t in VOW]
a, w = count_opts(len(vw))
AQ(PB, "If every letter in the arrangement is replaced by the letter that comes immediately after it in the English "
   "alphabet, how many vowels will the new arrangement contain?", a, w, "Only letters just before a vowel become vowels",
   "A letter becomes a vowel only if it is D, H, N, T or Z (→ E, I, O, U, A). Letters of the arrangement: "
   + ", ".join(t for t in SR if is_l(t)) + ". Of these, " + ", ".join(t for t in SR if t in "DHNTZ") +
   f" become vowels — {len(vw)}.", ["Letters before vowels: D, H, N, T, Z", "Count them in the arrangement"],
   natural=by_num, seconds=60)
vi = [i for i, t in enumerate(SR) if t in VOW]
ni = [i for i, t in enumerate(SR) if is_d(t)]
p1, p2 = sorted((vi[1], ni[-3]))
syms = [SR[i] for i in range(p1 + 1, p2) if is_s(SR[i])]
a, w = count_opts(len(syms))
AQ(SN, "How many symbols are there between the 2nd vowel from the left end and the 3rd number from the right end?", a,
   w, "Locate both reference elements first",
   f"2nd vowel from the left: {SR[vi[1]]} ({ordn(vi[1] + 1)}). 3rd number from the right: {SR[ni[-3]]} "
   f"({ordn(ni[-3] + 1)}). Between them: " + fmt(SR[p1 + 1:p2]) + ". Symbols: " + (", ".join(syms) or "none") +
   f" — {len(syms)}.", [f"Vowel at {vi[1] + 1}, number at {ni[-3] + 1}", "Count the symbols in between"],
   natural=by_num, seconds=65)
j_ = (2 + 12) // 2 - 1 + 7
ans = SR[j_]
AQ(PB, "Which element is 7th to the right of the element that lies exactly midway between the 2nd and the 12th "
   "elements from the left end?", ans, near(SR, j_), "Midway = average of the positions",
   f"Midway between the 2nd and 12th is the (2 + 12) ÷ 2 = 7th element ({SR[6]}). Seven places to its right is the "
   f"14th element: {ans}.", ["(2 + 12) ÷ 2 = 7th", f"7 + 7 = 14th ⇒ {ans}"], seconds=50)

# ---------------------------------------------------------------- Alphanumeric series: Advanced set
SR = "5 Q @ E 8 J % 2 I N 7 # T 4 & O P 3 £ G A 9 ¥ L 6 K * U 1 R".split()
assert len(SR) == 30
sid = stimulus("data_table", "Arrangement of 30 elements beginning with 5", series_intro(fmt(SR)), None,
               "Number the elements 1 to 30 from the left (k-th from the right = (31 − k)-th from the left). Vowels: "
               "E, I, O, A, U. When elements are removed or regrouped, write out the new arrangement before counting.")
AQ = lambda sub, text, correct, wrongs, concept, expl, steps, **kw: mcq(
    ALN, sub, "Advanced", text, correct, wrongs, concept, expl, steps, stimulus=sid, verified_by=RECOMP, **kw)
ns_ = [t for t in SR if not is_s(t)]
nw = ns_[:12][::-1] + ns_[12:]
ans = nw[-7]
AQ(PB, "If all the symbols are removed and then the first twelve of the remaining elements are written in reverse "
   "order, which element will be 7th from the right end?", ans, near(nw, len(nw) - 7),
   "Delete, then reverse a block, then count",
   "Without symbols (" + str(len(ns_)) + " elements): " + fmt(ns_) + ". Reversing the first twelve: " + fmt(nw) +
   f". The 7th from the right is {ans}.", ["Remove the symbols", "Reverse the first twelve", f"7th from the right ⇒ "
                                                                                             f"{ans}"],
   seconds=100)
hits = [i for i in range(1, len(SR) - 1) if is_l(SR[i]) and is_s(SR[i - 1]) and is_d(SR[i + 1])
        and int(SR[i + 1]) % 2 == 0]
a, w = count_opts(len(hits))
AQ(SN, "How many letters in the arrangement are immediately preceded by a symbol and immediately followed by an even "
   "number?", a, w, "Both neighbours must match",
   "Letters with a symbol on the left: " + ", ".join(f"{SR[i - 1]} {SR[i]} {SR[i + 1]}" for i in range(1, len(SR) - 1)
                                                     if is_l(SR[i]) and is_s(SR[i - 1])) +
   ". Of these, followed by an even number: " + (", ".join(f"{SR[i - 1]} {SR[i]} {SR[i + 1]}" for i in hits) or "none")
   + f" — {len(hits)}.", ["Find letters with a symbol on the left", "Keep those with an even number on the right"],
   natural=by_num, seconds=80)
nc = [t for t in SR if not CONS(t)]
j_ = 4 + 4
ans = nc[j_]
AQ(PB, "If all the consonants are removed from the arrangement, which element will be 4th to the right of the 5th "
   "element from the left end?", ans, near(nc, j_), "Delete first, then count",
   "Without consonants: " + fmt(nc) + f". The 5th element is {nc[4]}; four places to its right is the 9th: {ans}.",
   ["Remove every consonant", f"5th = {nc[4]}", f"5 + 4 = 9th ⇒ {ans}"], seconds=80)
pre = [int(SR[i]) for i in range(1, len(SR)) if is_d(SR[i]) and SR[i - 1] in VOW]
fol = [int(SR[i]) for i in range(len(SR) - 1) if is_d(SR[i]) and SR[i + 1] in VOW]
ans = abs(sum(pre) - sum(fol))
AQ(SN, "What is the difference between the sum of the numbers that are immediately preceded by a vowel and the sum of "
   "the numbers that are immediately followed by a vowel?", str(ans),
   [str(sum(pre)), str(sum(fol)), str(sum(pre) + sum(fol))], "Two filters, two sums",
   "Preceded by a vowel: " + ", ".join(map(str, pre)) + f" (sum {sum(pre)}). Followed by a vowel: "
   + ", ".join(map(str, fol)) + f" (sum {sum(fol)}). Difference: {ans}.",
   ["Numbers with a vowel on the left", "Numbers with a vowel on the right", "Subtract the sums"],
   why_others_wrong="The other options are one of the two sums alone, or their total.", natural=int, seconds=90)
assert len({ans, sum(pre), sum(fol), sum(pre) + sum(fol)}) == 4
hits = [i for i in range(len(SR) - 2) if SR[i] in VOW and is_d(SR[i + 2])]
assert len(hits) == 2
a, w = count_opts(len(hits))
AQ(SN, "How many times does a number stand exactly two places to the right of a vowel (with one element in "
   "between)?", a, w, "Check the element two places to the right of every vowel",
   "Each vowel with the element two places to its right: " + ", ".join(f"{SR[i]} … {SR[i + 2]}" for i in
                                                                         range(len(SR) - 2) if SR[i] in VOW) +
   ". Numbers there: " + (", ".join(f"{SR[i]} {SR[i + 1]} {SR[i + 2]}" for i in hits) or "none") +
   f" — {len(hits)}.", ["Vowels: E, I, O, A, U", "Look two places to the right of each"], natural=by_num, seconds=80)

# ---------------------------------------------------------------- Alphabet test: Intermediate set (one word)
wd = "REPUBLICANS"
sid = stimulus("passage", "Questions on the word REPUBLICANS",
               "Answer the questions on the basis of the word given below.\n\nR E P U B L I C A N S", None,
               "Alphabetical positions: R 18, E 5, P 16, U 21, B 2, L 12, I 9, C 3, A 1, N 14, S 19.")
WQ = lambda sub, text, correct, wrongs, concept, expl, steps, **kw: mcq(
    ABT, sub, "Intermediate", text, correct, wrongs, concept, expl, steps, stimulus=sid, verified_by=RECOMP, **kw)
PRIMES = {2, 3, 5, 7, 11, 13, 17, 19, 23}
pl = [c for c in wd if pos(c) in PRIMES]
a, w = count_opts(len(pl))
WQ(LP, "How many letters of the word have a position in the English alphabet that is a prime number?", a, w,
   "Primes up to 26: 2, 3, 5, 7, 11, 13, 17, 19, 23",
   "Positions: " + ", ".join(f"{c} {pos(c)}" for c in wd) + ". Prime positions: " + ", ".join(f"{c} ({pos(c)})"
                                                                                               for c in pl) +
   f" — {len(pl)}.", ["Write each letter's position", "Keep the prime positions"], natural=by_num, seconds=60)
ans = wd[(1 + 9) // 2 - 1 + 3]
assert ans == "C"
WQ(LP, "Which letter is 3rd to the right of the letter that lies exactly midway between the 1st and 9th letters of the "
   "word?", ans, ["I", "A", "L"], "Midway = average of the positions",
   "Midway between the 1st and 9th letters is the 5th letter, B. Three places to its right is the 8th letter: C.",
   ["(1 + 9) ÷ 2 = 5th = B", "5 + 3 = 8th ⇒ C"],
   why_others_wrong="I is 7th and A 9th; L is only one place to the right of B.", seconds=50)
pr = letter_pairs(wd)
a, w = count_opts(len(pr))
WQ(PRS, "How many pairs of letters in the word have as many letters between them in the word as in the English "
   "alphabet (counting both forward and backward)?", a, w, "Compare the gap in the word with the gap in the alphabet",
   "Pairs found: " + (", ".join(f"{x}{y}" for x, y in pr) or "none") + f" — {len(pr)} in all.",
   ["Positions: " + ", ".join(f"{c} {pos(c)}" for c in wd), "A pair qualifies when |word gap| = |alphabet gap|"],
   natural=by_num, seconds=75)

# ---------------------------------------------------------------- Alphabet test: Intermediate (standalone)
ans = AL[pos("P") + (pos("K") - pos("D")) - 1]
assert ans == "W"
mcq(ABT, LP, "Intermediate", "Which letter is as many places to the right of P in the English alphabet as K is to the "
    "right of D?", ans, ["V", "X", "I"], "Find the gap, then apply it",
    "K (11) is 7 places to the right of D (4). Seven places to the right of P (16) is the 23rd letter: W.",
    ["K − D = 11 − 4 = 7", "16 + 7 = 23 ⇒ W"],
    why_others_wrong="V and X are 6 and 8 places from P; I is 7 places to the left of P.", seconds=45,
    verified_by=RECOMP)
WDS = ["MANAGE", "MANAGER", "MANAGING", "MANAGEMENT"]
srt = sorted(WDS)
assert srt == ["MANAGE", "MANAGEMENT", "MANAGER", "MANAGING"]
mcq(ABT, WF, "Intermediate", "If the words MANAGE, MANAGER, MANAGING and MANAGEMENT are arranged in the order in which "
    "they appear in an English dictionary, which word will be third?", srt[2], ["MANAGEMENT", "MANAGING", "MANAGE"],
    "A shorter word that is the start of a longer one comes first",
    "MANAGE comes first, being the beginning of the others. MANAGEMENT and MANAGER both start with MANAGE; their next "
    "letters are M and R, so MANAGEMENT comes before MANAGER. MANAGING (I after MANAG, and I > E) comes last. Third: "
    "MANAGER.", ["MANAGE < MANAGE-M… < MANAGE-R…", "MANAGI- comes after MANAGE-", "Order: " + ", ".join(srt)],
    why_others_wrong="MANAGEMENT is second, MANAGING fourth and MANAGE first.", seconds=45, verified_by=RECOMP)
cons = [c for c in AL if c not in VOW]
ans = cons[-12]
assert len(cons) == 21 and ans == "M"
mcq(ABT, LP, "Intermediate", "If all the vowels are removed from the English alphabet, which letter will be 12th from "
    "the right end of the remaining letters?", ans, ["L", "N", "O"], "21 consonants remain",
    "Without A, E, I, O, U, 21 letters remain. The 12th from the right is the 21 − 12 + 1 = 10th from the left: B C D F "
    "G H J K L M — M.", ["21 consonants", "12th from the right = 10th from the left", "10th consonant ⇒ M"],
    why_others_wrong="L and N are one place off; O is a vowel and has been removed.", seconds=50, verified_by=RECOMP)


# ================================================================================================ WRITE
DRAFT = "--draft" in sys.argv
problems = []
for k, b in PKG["batches"].items():
    if k not in STATE:
        problems.append(f"batch {k}: not built")
        continue
    qs, sts, keys = STATE[k]["questions"], STATE[k]["stimuli"], STATE[k]["keys"]
    have = Counter((x["topic"], x["difficulty"]) for x in qs)
    for t in b["topics"]:
        for d_, n_ in t["quota"].items():
            if have[(t["topic"], d_)] != n_:
                problems.append(f"batch {k}: {t['topic']} {d_} {have[(t['topic'], d_)]}/{n_}")
        assert all(x["subtopic"] in t["subtopics"] for x in qs if x["topic"] == t["topic"]), (k, t["topic"])
    assert all(x["topic"] in {t["topic"] for t in b["topics"]} for x in qs), k
    for st_ in sts:
        n_ = sum(1 for x in qs if x.get("stimulus_id") == st_["stimulus_id"])
        assert 3 <= n_ <= 6, (st_["stimulus_id"], n_)
        assert len({x["difficulty"] for x in qs if x.get("stimulus_id") == st_["stimulus_id"]}) == 1, st_["stimulus_id"]
        assert len({x["topic"] for x in qs if x.get("stimulus_id") == st_["stimulus_id"]}) == 1, st_["stimulus_id"]
    if sts:
        assert sts[0]["stimulus_id"] == b["stimulus_id_start"], (k, sts[0]["stimulus_id"])
    if len(qs) == b["count"]:
        assert qs[0]["question_id"] == b["question_ids"][0] and qs[-1]["question_id"] == b["question_ids"][1], k
    else:
        problems.append(f"batch {k}: {len(qs)}/{b['count']} questions")
    print(f"batch {k}: {len(qs)} questions, {len(sts)} stimuli, keys {dict(sorted(keys.items()))}")
for x in (x for k in STATE for x in STATE[k]["questions"]):
    if x["question_id"] in BLIND_OK:
        x["verification"]["verified_by"].append("ai:independent-check")
print(f"blind-matched {len(BLIND_OK)}")
if "--dump" in sys.argv:  # key-free dump for the blind solver
    sts_ = {s["stimulus_id"]: s for k in STATE for s in STATE[k]["stimuli"]}
    out_ = [{"id": x["question_id"], "stimulus": sts_[x["stimulus_id"]]["content"] if x.get("stimulus_id") else None,
             "text": x["question_text"], "options": {o["key"]: o["text"] for o in x["options"]}}
            for k in STATE for x in STATE[k]["questions"]]
    Path(sys.argv[sys.argv.index("--dump") + 1]).write_text(json.dumps(out_, indent=1, ensure_ascii=False),
                                                            encoding="utf-8")
    keys_ = {x["question_id"]: x["correct_answer"] for k in STATE for x in STATE[k]["questions"]}
    Path(sys.argv[sys.argv.index("--dump") + 1] + ".keys").write_text(json.dumps(keys_), encoding="utf-8")
    print("dumped", len(out_))
if problems:
    print("\n".join(problems))
    assert DRAFT, "quota problems (use --draft to inspect)"
else:
    for k, b in PKG["batches"].items():
        keys = STATE[k]["keys"]
        assert max(keys.values()) - min(keys.values()) <= 6, (k, keys)
        out = ROOT / b["output"]
        doc = {
            "schema_version": "1.0",
            "batch_id": b["batch_id"],
            "created_at": TODAY,
            "notes": (f"Reasoning Ability fragment of {b['batch_id']} from topic package REAS_pkg3 (Blood Relations, "
                      "Direction Sense, Coding and Decoding, Alphanumeric Series, Alphabet Test, Number Series "
                      f"(Reasoning)): {b['count']} original questions built by tools/packages/REAS_pkg3.py. Family "
                      "trees, coordinates, coding rules (inferred rules checked against a library of alternative "
                      "rules; sentence codes by enumerating every word-code bijection), series, alphabet and number "
                      "operations are recomputed in code. All questions await human review."),
            "stimuli": STATE[k]["stimuli"],
            "questions": STATE[k]["questions"],
        }
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"wrote {out}")
