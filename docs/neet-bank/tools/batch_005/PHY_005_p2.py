"""Builder for batches/parts/BATCH_005_PHY_p2.json (package PHY_005_p2 of BATCH_005).

Physics, 123 original questions, NEET_PHY_001128..NEET_PHY_001250: Current Electricity, Magnetic Effects of Current
and Magnetism, Electromagnetic Induction and Alternating Currents, Electromagnetic Waves, Optics, Dual Nature of
Matter and Radiation, Atoms and Nuclei, Electronic Devices, Experimental Skills.

Every numerical answer is recomputed below with an assert next to its question; multi-statement, assertion-reason
and statement-pair keys are derived from truth tables; the plan quota, format mix and answer-key balance are
asserted before anything is written. If any assert fails, nothing is written.

    python tools/batch_005/PHY_005_p2.py        (run from docs/neet-bank)
"""

import json
import math
import sys
from collections import Counter
from fractions import Fraction as F
from pathlib import Path

TOOLS = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(TOOLS))
from qbank import ASSERTION_REASON, STATEMENT_PAIR, default_mappings  # noqa: E402

ROOT = TOOLS.parent
TODAY = "2026-11-16"
LETTERS = "ABCD"
PLAN = ROOT / "batches" / "plans" / "BATCH_005_plan.json"
OUT = ROOT / "batches" / "parts" / "BATCH_005_PHY_p2.json"
PACKAGE = "PHY_005_p2"
FIRST_ID = 1128
COUNT = 123

CE = "Current Electricity"
MAG = "Magnetic Effects of Current and Magnetism"
EMI = "Electromagnetic Induction and Alternating Currents"
EMW = "Electromagnetic Waves"
OPT = "Optics"
DUAL = "Dual Nature of Matter and Radiation"
AN = "Atoms and Nuclei"
ED = "Electronic Devices"
EXP = "Experimental Skills"

AR, SP = ASSERTION_REASON, STATEMENT_PAIR
QS = []


def q(topic, subtopic, difficulty, fmt, text, options, answer, concept, explanation, steps, shortcut=None,
      why=None, ncert=None, seconds=60, rc=False):
    """Appends one question. rc=True only when the answer is recomputed by an assert in this file."""
    assert answer in LETTERS and len(options) == 4 and len(set(options)) == 4, text[:60]
    if fmt == "numerical":
        assert rc, f"numerical question without recompute: {text[:60]}"
    if fmt == "assertion_reason":
        assert options == AR
    if fmt == "statement_pair":
        assert options == SP
    verified_by = (["script:recompute"] if rc else []) + ["ai:author-solve", "ai:self-recheck"]
    QS.append({
        "question_id": None, "exam_mappings": default_mappings("Physics"), "subject": "Physics", "topic": topic,
        "subtopic": subtopic, "difficulty": difficulty, "question_type": "MCQ", "format": fmt, "language": "en",
        "question_text": text,
        "options": [{"key": LETTERS[i], "text": t} for i, t in enumerate(options)],
        "correct_answer": answer,
        "solution": {"concept": concept, "explanation": explanation, "steps": steps, "shortcut": shortcut,
                     "why_others_wrong": why, "ncert_reference": ncert,
                     "final_answer": f"Option {answer}: {options[LETTERS.index(answer)]}"},
        "suggested_time_seconds": seconds,
        "source": {"source_type": "Original", "source_name": "PrepMitra", "source_url": None,
                   "original_exam_year": None, "license_note": None},
        "verification": {"answer_verified": True, "solution_verified": True, "review_status": "Pending Human Review",
                         "verified_by": verified_by, "verified_at": TODAY},
    })


def opt(correct, wrong, at):
    """(options, answer) with the correct text at position `at`."""
    assert len(wrong) == 3 and correct not in wrong
    opts = list(wrong)
    opts.insert(LETTERS.index(at), correct)
    return opts, at


def match_options(correct: dict, wrong: list, at: str) -> list:
    """Option texts for a match-the-list question with the correct code at position `at` (as in the sample)."""
    code = lambda m: ", ".join(f"{k}-{m[k]}" for k in "ABCD")
    for m in [correct, *wrong]:
        assert sorted(m) == list("ABCD") and sorted(m.values()) == sorted(["I", "II", "III", "IV"])
    opts = [code(w) for w in wrong]
    opts.insert(LETTERS.index(at), code(correct))
    assert len(set(opts)) == 4
    return opts


def mcode(s):
    """'A-II, B-IV, C-I, D-III' -> dict, so match-list options can be written compactly."""
    return dict(p.split("-") for p in s.split(", "))


def mlo(correct, wrong, at):
    """(options, answer) for a match-list question."""
    return match_options(mcode(correct), [mcode(w) for w in wrong], at), at


def close(a, b, rel=6e-3):
    assert math.isclose(a, b, rel_tol=rel), (a, b)


def solve_network(n, edges, fixed):
    """Node potentials of a resistor network (exact fractions). edges: (a, b, R); fixed: {node: potential}."""
    free = [i for i in range(n) if i not in fixed]
    idx = {node: k for k, node in enumerate(free)}
    m = len(free)
    A = [[F(0)] * (m + 1) for _ in range(m)]
    for a, b, r in edges:
        g = F(1) / F(r)
        for x, y in ((a, b), (b, a)):
            if x in idx:
                A[idx[x]][idx[x]] += g
                if y in idx:
                    A[idx[x]][idx[y]] -= g
                else:
                    A[idx[x]][m] += g * F(fixed[y])
    for c in range(m):
        p = next(r for r in range(c, m) if A[r][c] != 0)
        A[c], A[p] = A[p], A[c]
        for r in range(m):
            if r != c and A[r][c] != 0:
                f = A[r][c] / A[c][c]
                A[r] = [x - f * y for x, y in zip(A[r], A[c])]
    v = dict(fixed)
    for node, k in idx.items():
        v[node] = A[k][m] / A[k][k]
    return {k: F(x) for k, x in v.items()}


def equivalent_resistance(n, edges, a, b):
    """Resistance between nodes a and b: hold a at 1 V, b at 0 V and find the current drawn."""
    v = solve_network(n, edges, {a: 1, b: 0})
    current = sum((v[x] - v[y]) / F(r) for x, y, r in edges if x == a) + \
        sum((v[y] - v[x]) / F(r) for x, y, r in edges if y == a)
    return 1 / current


def ms_check(truth, correct_set, option_sets):
    """Multi-statement guard: the keyed set is exactly the true statements and appears once among the options."""
    assert {k for k, t in truth.items() if t} == set(correct_set), (truth, correct_set)
    assert sum(1 for s in option_sets if set(s) == set(correct_set)) == 1


def ms_text(s):
    parts = [f"({x})" for x in s]
    return (", ".join(parts[:-1]) + " and " + parts[-1] if len(parts) > 1 else parts[0]) + " only"


def mso(truth, correct, wrong, at):
    """(options, answer) for a multi-statement question; asserts the key matches the truth table."""
    ms_check(truth, correct, [correct, *wrong])
    return opt(ms_text(correct), [ms_text(w) for w in wrong], at)


AR_STEM = "Given below are two statements: one is labelled Assertion (A) and the other is labelled Reason (R).\n\n"
AR_END = "\n\nChoose the correct answer from the options given below:"
SP_STEM = "Given below are two statements:\n\n"
SP_END = "\n\nIn the light of the above statements, choose the correct answer from the options given below:"
ML_END = "\n\nChoose the correct answer from the options given below:"
MS_END = "\n\nChoose the correct answer from the options given below:"


def ar(a, r):
    return f"{AR_STEM}Assertion (A): {a}\nReason (R): {r}{AR_END}"


def sp(s1, s2):
    return f"{SP_STEM}Statement I: {s1}\nStatement II: {s2}{SP_END}"


def ml(head, left, right):
    l1 = "\n".join(f"{k}. {v}" for k, v in zip("ABCD", left))
    l2 = "\n".join(f"{k}. {v}" for k, v in zip(["I", "II", "III", "IV"], right))
    return f"{head}\n\nList-I:\n{l1}\n\nList-II:\n{l2}{ML_END}"


def ms(head, items):
    body = "\n".join(f"({k}) {v}" for k, v in zip("abcde", items))
    return f"{head}\n\n{body}{MS_END}"


def ar_key(a_true, r_true, explains=None):
    """Key of an assertion-reason question from the truth of A and R."""
    if a_true and r_true:
        assert explains is not None
        return "A" if explains else "B"
    if a_true:
        return "C"
    assert r_true, "A and R both false is not one of the fixed options"
    return "D"


def sp_key(s1, s2):
    return {(True, True): "A", (False, False): "B", (True, False): "C", (False, True): "D"}[(s1, s2)]




NC = "Class 12 Physics, "


# ================================================================ Current Electricity (B6 I8 A6)
CEC = NC + "'Current Electricity', "

# ---- Basic
I_c1, A_c1 = 5.0, 2.5e-6
close(I_c1 / A_c1, 2.0e6)
close(A_c1 / I_c1, 5.0e-7)
close(I_c1 / 2.5, 2.0)
close(I_c1 / 2.5e-3, 2.0e3)
q(CE, "Drift velocity and Ohm's law", "Basic", "numerical",
  "A steady current of 5.0 A flows through a wire of uniform cross-sectional area 2.5 mm². The magnitude of the "
  "current density in the wire is:",
  *opt("2.0 × 10⁶ A m⁻²", ["2.0 A m⁻²", "5.0 × 10⁻⁷ A m⁻²", "2.0 × 10³ A m⁻²"], "C"),
  "Current density j = I/A",
  "Current density is the current per unit area of cross-section normal to the current. The area must be in m²: "
  "2.5 mm² = 2.5 × 10⁻⁶ m².",
  ["A = 2.5 mm² = 2.5 × 10⁻⁶ m²", "j = I/A = 5.0/(2.5 × 10⁻⁶) = 2.0 × 10⁶ A m⁻²"],
  why="2.0 A m⁻² leaves the area in mm². 5.0 × 10⁻⁷ A m⁻² divides the area by the current. 2.0 × 10³ A m⁻² converts "
      "mm² to m² with 10⁻³ instead of 10⁻⁶.",
  ncert=CEC + "Ohm's law (current density)", seconds=30, rc=True)

alpha_c2 = 5e-3
T_c2 = 0.5 / alpha_c2
assert T_c2 == 100
close(1.5 / alpha_c2, 300)
close(1 / alpha_c2, 200)
q(CE, "Resistivity and temperature", "Basic", "numerical",
  "The temperature coefficient of resistance of a metal, referred to 0 °C, is 5 × 10⁻³ °C⁻¹ and may be taken as "
  "constant. A wire of this metal has resistance R₀ at 0 °C. The temperature at which its resistance becomes 1.5 R₀ is:",
  *opt("100 °C", ["300 °C", "200 °C", "50 °C"], "A"),
  "R_T = R₀[1 + α(T − T₀)]",
  "The resistance rises by the fraction αΔT. For a 50% rise, αΔT = 0.5.",
  ["1.5 R₀ = R₀(1 + αT) → αT = 0.5", "T = 0.5/(5 × 10⁻³) = 100 °C"],
  why="300 °C uses αT = 1.5 (the whole ratio instead of the increase). 200 °C is the temperature at which the "
      "resistance doubles. 50 °C halves the correct value.",
  ncert=CEC + "temperature dependence of resistivity", seconds=35, rc=True)

eps_c3, R_c3, I_c3 = 2.0, 9.0, 0.2
r_c3 = eps_c3 / I_c3 - R_c3
close(r_c3, 1.0)
close(eps_c3 - I_c3 * R_c3, 0.2)
close((eps_c3 - I_c3 * R_c3) * I_c3, 0.04)
q(CE, "Cells, emf and internal resistance", "Basic", "numerical",
  "A cell of emf 2.0 V is connected across a 9.0 Ω resistor, and a current of 0.20 A flows in the circuit. The "
  "internal resistance of the cell is:",
  *opt("1.0 Ω", ["10 Ω", "0.20 Ω", "0.04 Ω"], "D"),
  "Circuit equation for a cell with internal resistance: I = ε/(R + r)",
  "The total resistance of the circuit is ε/I; the internal resistance is what remains after subtracting the "
  "external resistance.",
  ["R + r = ε/I = 2.0/0.20 = 10 Ω", "r = 10 − 9.0 = 1.0 Ω"],
  why="10 Ω is the total resistance R + r. 0.20 Ω takes the lost voltage (0.2 V) as the resistance. 0.04 Ω "
      "multiplies the lost voltage by the current instead of dividing.",
  ncert=CEC + "cells, emf, internal resistance", seconds=35, rc=True)

V_c4 = 6.0
I_c4 = sum(V_c4 / r for r in (2, 3, 6))
assert I_c4 == 6.0
close(V_c4 / 11, 0.545, 2e-3)
q(CE, "Combination of resistors", "Basic", "numerical",
  "Three resistors of 2 Ω, 3 Ω and 6 Ω are connected in parallel across an ideal 6 V battery. The total current "
  "drawn from the battery is:",
  *opt("6 A", ["0.55 A", "1 A", "11 A"], "B"),
  "Parallel resistors: the same p.d. across each; currents add",
  "Each resistor has the full 6 V across it, so the currents are 3 A, 2 A and 1 A. Equivalently, 1/R = 1/2 + 1/3 + "
  "1/6 = 1, so R = 1 Ω and I = 6 A.",
  ["I = 6/2 + 6/3 + 6/6 = 3 + 2 + 1 = 6 A", "Check: R_p = 1 Ω → I = 6/1 = 6 A"],
  why="0.55 A treats the resistors as in series (11 Ω). 1 A is the current in the 6 Ω resistor alone. 11 A adds "
      "the resistances and multiplies instead of dividing.",
  ncert=CEC + "combination of resistors - series and parallel", seconds=30, rc=True)

q(CE, "Resistivity and temperature", "Basic", "direct",
  "The resistivity of an intrinsic semiconductor such as silicon decreases as its temperature rises. The main "
  "reason is that, with a rise in temperature:",
  *opt("the number density of free charge carriers increases, more than making up for any decrease in the "
       "relaxation time",
       ["the relaxation time of the charge carriers increases sharply",
        "the charge carriers become heavier and so move more steadily",
        "the band gap of the semiconductor increases"], "C"),
  "ρ = m/(ne²τ): resistivity depends on both n and τ",
  "In metals n is practically fixed and τ falls with temperature, so ρ rises. In semiconductors n rises steeply with "
  "temperature, and this more than compensates for any fall in τ, so ρ falls.",
  ["ρ = m/(ne²τ)", "Semiconductor: n increases rapidly with T → ρ decreases"],
  why="The relaxation time decreases (not increases) with temperature. The mass of the carriers does not change. A "
      "larger band gap would reduce, not increase, the number of carriers.",
  ncert=CEC + "temperature dependence of resistivity", seconds=30)

q(CE, "Drift velocity and Ohm's law", "Basic", "statement_pair",
  sp("In a metal wire carrying a current, the drift speed of the free electrons (of the order of mm/s) is very much "
     "smaller than their random thermal speeds at room temperature (of the order of 10⁵ m/s).",
     "For a given electric field in a metal, the drift speed of the free electrons is directly proportional to "
     "their relaxation time."),
  SP, sp_key(True, True),
  "Drift velocity v_d = eEτ/m superposed on random thermal motion",
  "Free electrons move randomly with speeds of about 10⁵ m/s; the field only adds a tiny average drift of about "
  "1 mm/s (Statement I true). From v_d = eEτ/m, v_d ∝ τ for a given E (Statement II true).",
  ["Thermal speeds ~10⁵ m/s ≫ drift speed ~10⁻³ m/s → I true", "v_d = (eτ/m)E → v_d ∝ τ → II true"],
  why="Both statements are NCERT results, so options with either statement false are wrong.",
  ncert=CEC + "drift of electrons and the origin of resistivity", seconds=35)

# ---- Intermediate
VA, VB, VD = 10, 4, 0
v = solve_network(4, [(0, 3, 2), (1, 3, 4), (2, 3, 4)], {0: VA, 1: VB, 2: VD})
assert v[3] == 6
close((VA + VB + VD) / 3, 4.667, 1e-3)
assert F(VA * 2 + VB * 4 + VD * 4, 10) == F(18, 5)
q(CE, "Kirchhoff's laws", "Intermediate", "numerical",
  "A junction C in a circuit is connected to three points A, B and D by resistors of 2 Ω (C to A), 4 Ω (C to B) and "
  "4 Ω (C to D). Nothing else is connected to C. The potentials of A, B and D are held at 10 V, 4 V and 0 V "
  "respectively. The potential of C is:",
  *opt("6 V", ["4.67 V", "3.6 V", "5 V"], "B"),
  "Kirchhoff's junction rule applied to a node",
  "No charge accumulates at C, so the currents into C from A, B and D add to zero: Σ(V_X − V_C)/R_X = 0.",
  ["(10 − V)/2 + (4 − V)/4 + (0 − V)/4 = 0", "Multiply by 4: 20 − 2V + 4 − V − V = 0 → 4V = 24 → V = 6 V"],
  shortcut="V_C = Σ(V_X/R_X)/Σ(1/R_X) = (5 + 1 + 0)/(0.5 + 0.25 + 0.25) = 6 V.",
  why="4.67 V is the plain average of the three potentials, ignoring the resistances. 3.6 V weights each potential "
      "by its resistance instead of its conductance. 5 V has no basis in the junction rule.",
  ncert=CEC + "Kirchhoff's rules", seconds=60, rc=True)

small_c, shift_c = 8, 20
l1 = (100 - shift_c) / 2
large_c = small_c * (100 - l1) / l1
assert l1 == 40 and large_c == 12
assert small_c * 100 / 25 == 32 and small_c * (50 / 40) == 10 and small_c * (60 / 40) ** 2 == 18
q(CE, "Wheatstone and metre bridge", "Intermediate", "numerical",
  "Two resistors are placed in the two gaps of a metre bridge and the null point is found. When the two resistors "
  "are interchanged, the null point shifts along the wire by 20.0 cm. If the smaller resistance is 8 Ω, the larger "
  "resistance is:",
  *opt("12 Ω", ["32 Ω", "10 Ω", "18 Ω"], "A"),
  "Metre bridge balance R₁/R₂ = l/(100 − l); interchanging the resistors makes the null point 100 − l",
  "On interchanging, the null point moves from l to 100 − l, so the shift is 100 − 2l. A shift of 20 cm gives "
  "l = 40 cm for the smaller resistance's gap.",
  ["100 − 2l = 20 → l = 40 cm", "R_large/R_small = 60/40 = 3/2", "R_large = 8 × 1.5 = 12 Ω"],
  why="32 Ω takes the 20 cm shift itself as the balancing length (ratio 80 : 20). 10 Ω uses the ratio 50 : 40. "
      "18 Ω squares the correct ratio.",
  ncert=CEC + "Wheatstone bridge (metre bridge)", seconds=70, rc=True)

R0_c5 = 4.0
ratio = 1.1 ** 2
close((ratio - 1) * 100, 21.0)
close((1.1 ** 3 - 1) * 100, 33.1)
q(CE, "Resistivity and temperature", "Intermediate", "numerical",
  "A uniform metal wire of resistance 4.0 Ω is stretched so that its length increases by 10%. Its volume, "
  "resistivity and temperature do not change. The percentage increase in its resistance is:",
  *opt("21%", ["10%", "20%", "33.1%"], "D"),
  "R = ρl/A with constant volume: A = V/l, so R = ρl²/V ∝ l²",
  "When the volume is fixed, stretching the wire also reduces its area in the same ratio, so the resistance grows as "
  "the square of the length.",
  ["R ∝ l²", "R'/R = (1.10)² = 1.21", "Increase = 21%"],
  shortcut="For small stretches the increase is about 2 × 10% = 20%, but the exact value is 21%.",
  why="10% ignores the reduction in area. 20% is only the small-change approximation (2 × 10%). 33.1% uses R ∝ l³.",
  ncert=CEC + "resistivity of various materials", seconds=45, rc=True)

eA, rA, eB, rB, R_ch = 10.0, 1.0, 6.0, 1.0, 2.0
I_ch = (eA - eB) / (rA + rB + R_ch)
assert I_ch == 1.0
assert eB * I_ch == 6.0 and (eB + I_ch * rB) * I_ch == 7.0 and I_ch ** 2 * (rA + rB + R_ch) == 4.0
q(CE, "Cells, emf and internal resistance", "Intermediate", "numerical",
  "A battery X (emf 10 V, internal resistance 1 Ω) is used to charge a battery Y (emf 6 V, internal resistance "
  "1 Ω). The positive terminal of X is joined to the positive terminal of Y through a 2 Ω resistor, and the negative "
  "terminals are joined by a wire of negligible resistance. The rate at which electrical energy is converted into "
  "chemical energy in battery Y is:",
  *opt("6 W", ["7 W", "10 W", "4 W"], "A"),
  "Power stored in a battery being charged = ε × I; heat in its internal resistance is extra",
  "The emfs oppose each other in the loop, so the net emf is 10 − 6 = 4 V and the current is 4/(1 + 1 + 2) = 1 A. "
  "The part of the power that is stored chemically in Y is ε_Y × I; the I²r in Y is wasted as heat.",
  ["I = (10 − 6)/(1 + 1 + 2) = 1 A", "Power stored = ε_Y I = 6 × 1 = 6 W"],
  why="7 W is the total power delivered to Y, including the 1 W heat in its internal resistance. 10 W is the power "
      "generated by X. 4 W is the total heat produced in the circuit.",
  ncert=CEC + "cells, emf, internal resistance", seconds=75, rc=True)

q(CE, "Drift velocity and Ohm's law", "Intermediate", "assertion_reason",
  ar("A metal wire is connected across a battery that keeps a fixed potential difference between its ends. If the "
     "wire is heated, the drift speed of its free electrons increases.",
     "The drift speed of the free electrons in a metal is given by v_d = eEτ/m, where τ is the relaxation time."),
  AR, ar_key(False, True),
  "v_d = eEτ/m; τ decreases as the temperature of a metal rises",
  "With a fixed p.d. and length, E is unchanged. Heating the metal makes the electrons collide more often, so τ "
  "decreases and v_d decreases. A is false. R is the correct expression for the drift speed, so R is true.",
  ["E = V/L is fixed", "Heating → more frequent collisions → τ decreases", "v_d = eEτ/m decreases → A false; R true"],
  why="A is false because the drift speed falls, not rises; R is a correct NCERT relation.",
  ncert=CEC + "drift of electrons and the origin of resistivity", seconds=45)

q(CE, "Wheatstone and metre bridge", "Intermediate", "statement_pair",
  sp("If the cell and the galvanometer of a balanced Wheatstone bridge are interchanged, the bridge remains "
     "balanced.",
     "When a Wheatstone bridge is balanced, removing the galvanometer branch changes the current drawn from the cell."),
  SP, sp_key(True, False),
  "Balance condition of a Wheatstone bridge, P/Q = R/S",
  "With the cell and galvanometer interchanged, the galvanometer joins the other pair of corners and the balance "
  "condition becomes P/R = Q/S, which is the same as P/Q = R/S (Statement I true). At balance no current flows in "
  "the galvanometer, so removing it changes no current in the circuit (Statement II false).",
  ["Interchanged bridge: balance needs P/R = Q/S ⇔ P/Q = R/S → I true",
   "At balance I_g = 0 → removing the galvanometer leaves all currents unchanged → II false"],
  why="Statement II is false because the galvanometer branch carries no current at balance; Statement I is true, "
      "so the remaining options are wrong.",
  ncert=CEC + "Wheatstone bridge", seconds=50)

q(CE, "Cells, emf and internal resistance", "Intermediate", "match_list",
  ml("Two identical cells, each of emf ε and internal resistance r, and a resistor R are available. Match each "
     "arrangement in List-I with the current through R in List-II.",
     ["One cell alone connected across R",
      "Both cells in series (aiding each other), connected across R",
      "Both cells in parallel (positive terminal to positive terminal), connected across R",
      "Both cells in series but opposing each other (positive terminal joined to positive terminal), connected "
      "across R"],
     ["2ε/(2R + r)", "Zero", "ε/(R + r)", "2ε/(R + 2r)"]),
  *mlo("A-III, B-IV, C-I, D-II",
       ["A-III, B-I, C-IV, D-II", "A-I, B-IV, C-III, D-II", "A-III, B-IV, C-II, D-I"], "C"),
  "Equivalent emf and internal resistance of series and parallel cells",
  "Series aiding: emf 2ε, internal resistance 2r → 2ε/(R + 2r). Parallel: emf ε, internal resistance r/2 → "
  "ε/(R + r/2) = 2ε/(2R + r). Series opposing: net emf zero → no current.",
  ["A: ε/(R + r) → III", "B: 2ε/(R + 2r) → IV", "C: ε/(R + r/2) = 2ε/(2R + r) → I", "D: net emf 0 → II"],
  why="A-III, B-I, C-IV swaps the series and parallel expressions. A-I/C-III swaps one cell with the parallel pair. "
      "C-II/D-I gives the opposing pair a current and the parallel pair none.",
  ncert=CEC + "cells in series and in parallel", seconds=60)

q(CE, "Resistivity and temperature", "Intermediate", "multi_statement",
  ms("Which of the following statements about the resistivity of materials, as described in NCERT, are correct?",
     ["Metals have low resistivities, in the range of about 10⁻⁸ Ω m to 10⁻⁶ Ω m.",
      "Semiconductors have resistivities lower than those of metals.",
      "The resistivity of nichrome is much greater than that of copper.",
      "The temperature coefficient of resistivity of nichrome is much smaller than that of copper.",
      "Near room temperature, the resistivity of germanium increases as its temperature rises."]),
  *mso({"a": True, "b": False, "c": True, "d": True, "e": False}, "acd", ["abd", "cde", "ac"], "B"),
  "Resistivity of metals, alloys and semiconductors and its temperature dependence",
  "Metals: 10⁻⁸–10⁻⁶ Ω m (a true). Semiconductors lie between metals and insulators, so their resistivity is higher "
  "than that of metals (b false). Nichrome (about 100 × 10⁻⁸ Ω m) is far more resistive than copper "
  "(1.7 × 10⁻⁸ Ω m) (c true), and its temperature coefficient (about 1.7 × 10⁻⁴ °C⁻¹) is much smaller than "
  "copper's (about 3.9 × 10⁻³ °C⁻¹) (d true). Germanium is a semiconductor, so its resistivity falls as temperature "
  "rises (e false).",
  ["(a) true", "(b) false: semiconductors are more resistive than metals", "(c) true", "(d) true",
   "(e) false: negative temperature coefficient"],
  why="Options containing (b) or (e) include a false statement; (a) and (c) only leaves out the true statement (d).",
  ncert=CEC + "resistivity of various materials; temperature dependence of resistivity", seconds=60)

# ---- Advanced
e1, r1, e2, r2 = 2.0, 0.5, 1.5, 0.25
I_z = e1 / r1
R_z = (e1 + e2) / I_z - (r1 + r2)
close(R_z, 0.125)
close(e2 - I_z * r2, 0.5)
close((e1 + e2) / I_z, 0.875)
q(CE, "Cells, emf and internal resistance", "Advanced", "numerical",
  "Two cells, of emf 2.0 V (internal resistance 0.50 Ω) and emf 1.5 V (internal resistance 0.25 Ω), are connected "
  "in series, aiding each other, across an external resistor R. The value of R for which the potential difference "
  "across the terminals of the 2.0 V cell is zero is:",
  *opt("0.125 Ω", ["0.875 Ω", "0.25 Ω", "0.50 Ω"], "C"),
  "Terminal voltage V = ε − Ir; a cell's terminal p.d. is zero when Ir = ε",
  "The 2.0 V cell has zero terminal p.d. when the current through it is ε/r = 4 A. The series circuit must then "
  "carry 4 A, which fixes R.",
  ["V₁ = 0 → I = 2.0/0.50 = 4 A", "I = (2.0 + 1.5)/(0.50 + 0.25 + R) = 4", "0.75 + R = 0.875 → R = 0.125 Ω"],
  why="0.875 Ω is the total resistance of the circuit, not R. 0.25 Ω equates R to the internal resistance of the "
      "other cell. 0.50 Ω equates R to the internal resistance of the 2.0 V cell.",
  ncert=CEC + "cells, emf, internal resistance", seconds=90, rc=True)

V_m, I_m, RV = 4.8, 0.05, 2400.0
R_true = 1 / (I_m / V_m - 1 / RV)
close(R_true, 100.0)
close(V_m / I_m, 96.0)
close(1 / (I_m / V_m + 1 / RV), 92.3, 1e-3)
q(CE, "Combination of resistors", "Advanced", "numerical",
  "To measure a resistance R, a voltmeter of resistance 2400 Ω is connected directly across R, and an ammeter is "
  "connected in series with this combination. The voltmeter reads 4.8 V and the ammeter reads 0.050 A. The true "
  "value of R is:",
  *opt("100 Ω", ["96 Ω", "92.3 Ω", "2496 Ω"], "D"),
  "The ammeter current divides between R and the voltmeter in parallel",
  "The ammeter reads the total current through R and the voltmeter. The voltmeter itself takes 4.8/2400 = 2 mA, "
  "so the current through R is 50 − 2 = 48 mA.",
  ["Current in voltmeter = 4.8/2400 = 0.002 A", "Current in R = 0.050 − 0.002 = 0.048 A", "R = 4.8/0.048 = 100 Ω"],
  why="96 Ω is V/I, which ignores the current taken by the voltmeter. 92.3 Ω adds the voltmeter conductance instead "
      "of subtracting it. 2496 Ω treats the voltmeter as in series with R.",
  ncert=CEC + "combination of resistors - series and parallel", seconds=90, rc=True)

cube_edges = [(a, a ^ (1 << k), 12) for a in range(8) for k in range(3) if a < a ^ (1 << k)]
assert len(cube_edges) == 12
assert equivalent_resistance(8, cube_edges, 0, 1) == 7
assert equivalent_resistance(8, cube_edges, 0, 3) == 9
assert equivalent_resistance(8, cube_edges, 0, 7) == 10
q(CE, "Combination of resistors", "Advanced", "numerical",
  "Twelve identical resistors, each of 12 Ω, form the edges of a cube. The equivalent resistance between two "
  "adjacent corners of the cube (the two ends of one edge) is:",
  *opt("7 Ω", ["10 Ω", "9 Ω", "6 Ω"], "A"),
  "Symmetry and Kirchhoff's rules in a resistor network; for an edge of a cube R_eq = 7R/12",
  "Feed current I in at corner A and out at the adjacent corner B. By symmetry, the current divides so that the "
  "direct edge AB carries 7I/12. Hence V_AB = (7I/12)R and R_eq = 7R/12.",
  ["By symmetry, current in the direct edge AB = 7I/12", "V_AB = (7I/12) × 12 = 7I",
   "R_eq = V_AB/I = 7 Ω"],
  why="10 Ω (5R/6) is the resistance across a body diagonal. 9 Ω (3R/4) is the resistance across a face diagonal. "
      "6 Ω treats the edge as two equal paths in parallel.",
  seconds=120, rc=True)

q(CE, "Cells, emf and internal resistance", "Advanced", "assertion_reason",
  ar("A bulb is connected across a battery whose internal resistance is not negligible. When a second, identical "
     "bulb is connected in parallel with the first, the first bulb becomes dimmer.",
     "The potential difference across the terminals of a battery decreases as the current drawn from it increases, "
     "because V = ε − Ir."),
  AR, ar_key(True, True, True),
  "Terminal voltage V = ε − Ir",
  "Adding a bulb in parallel lowers the external resistance, so the battery delivers a larger current. A larger "
  "current means a larger drop Ir inside the battery, so the terminal p.d. (which is the p.d. across each bulb) "
  "falls and the first bulb dims. R states exactly this mechanism.",
  ["Second bulb in parallel → external resistance falls → I increases", "V = ε − Ir decreases",
   "P of first bulb = V²/R_bulb decreases → dimmer; R explains A"],
  why="Both statements are true and the fall in terminal voltage is precisely why the first bulb dims, so R is the "
      "correct explanation.",
  ncert=CEC + "cells, emf, internal resistance", seconds=60)

q(CE, "Cells, emf and internal resistance", "Advanced", "direct",
  "A cell of emf ε and internal resistance r is connected across an external resistor R. The efficiency of the cell "
  "is defined as the fraction of the power it generates that is delivered to R. The efficiency when the power "
  "delivered to R is maximum, and the efficiency when R = 3r, are respectively:",
  *opt("50% and 75%", ["100% and 75%", "50% and 25%", "75% and 50%"], "B"),
  "Efficiency η = I²R/[I²(R + r)] = R/(R + r); maximum power transfer at R = r",
  "The same current flows through R and r, so the fraction of power delivered to R is R/(R + r). Maximum power in R "
  "occurs at R = r, giving η = 1/2. For R = 3r, η = 3r/4r = 3/4.",
  ["η = R/(R + r)", "Maximum power: R = r → η = 50%", "R = 3r → η = 3/4 = 75%"],
  why="100% would need r = 0. 25% is r/(R + r), the fraction wasted inside the cell. 75% and 50% reverses the two "
      "cases.",
  ncert=CEC + "cells, emf, internal resistance", seconds=60)

q(CE, "Cells, emf and internal resistance", "Advanced", "multi_statement",
  ms("Two identical cells, each of emf ε and internal resistance r, can be connected either in series (aiding) or in "
     "parallel (positive terminal to positive terminal) across an external resistor R. A single cell alone gives a "
     "current ε/(R + r). Which of the following statements are correct?",
     ["If R is much larger than r, the series arrangement gives nearly twice the current of a single cell.",
      "If R is much smaller than r, the parallel arrangement gives nearly twice the current of a single cell.",
      "If R = r, the two arrangements give equal currents in R.",
      "In the parallel arrangement, the emf of the combination is 2ε.",
      "In the series arrangement, the internal resistance of the combination is r/2."]),
  *mso({"a": True, "b": True, "c": True, "d": False, "e": False}, "abc", ["ab", "bcd", "ace"], "D"),
  "Series: emf 2ε, internal resistance 2r; parallel: emf ε, internal resistance r/2",
  "Series current 2ε/(R + 2r) → 2ε/R when R ≫ r, twice the single-cell value ε/R (a true). Parallel current "
  "2ε/(2R + r) → 2ε/r when R ≪ r, twice ε/r (b true). With R = r both currents are 2ε/(3r) (c true). The emf of "
  "identical cells in parallel is ε, not 2ε (d false), and the series internal resistance is 2r, not r/2 (e false).",
  ["(a) 2ε/(R + 2r) ≈ 2ε/R → true", "(b) 2ε/(2R + r) ≈ 2ε/r → true", "(c) both = 2ε/3r → true",
   "(d) false", "(e) false"],
  why="Options with (d) or (e) contain a false statement, and (a) and (b) only misses the true statement (c).",
  ncert=CEC + "cells in series and in parallel", seconds=90)


# ================================================================ Magnetism (B6 I8 A6)
MC = NC + "'Moving Charges and Magnetism', "
MM = NC + "'Magnetism and Matter', "
mu0 = 4 * math.pi * 1e-7

# ---- Basic
dB = 1e-7 * 5 * 2e-3 * math.sin(math.radians(30)) / 0.10 ** 2
close(dB, 5e-8)
close(1e-7 * 5 * 2e-3 / 0.01, 1e-7)
close(1e-7 * 5 * 2e-3 * math.cos(math.radians(30)) / 0.01, 8.66e-8)
close(1e-7 * 5 * 2e-3 * 0.5 / 0.10, 5e-9)
q(MAG, "Biot-Savart law", "Basic", "numerical",
  "A small current element of length 2 mm carries a current of 5 A. Taking µ₀/4π = 10⁻⁷ T m A⁻¹, the magnitude of "
  "the magnetic field it produces at a point 10 cm away, the line joining the element to the point making an angle "
  "of 30° with the direction of the current, is:",
  *opt("5 × 10⁻⁸ T", ["1 × 10⁻⁷ T", "8.7 × 10⁻⁸ T", "5 × 10⁻⁹ T"], "B"),
  "Biot–Savart law: dB = (µ₀/4π) I dl sin θ / r²",
  "θ is the angle between the current element and the line joining it to the field point.",
  ["dB = 10⁻⁷ × 5 × (2 × 10⁻³) × sin 30° / (0.10)²", "= 10⁻⁷ × 5 × 2 × 10⁻³ × 0.5 / 0.01 = 5 × 10⁻⁸ T"],
  why="1 × 10⁻⁷ T leaves out sin θ. 8.7 × 10⁻⁸ T uses cos 30° instead of sin 30°. 5 × 10⁻⁹ T divides by r instead "
      "of r².",
  ncert=MC + "magnetic field due to a current element, Biot–Savart law", seconds=40, rc=True)

B_tor = mu0 * 500 * 1 / (2 * math.pi * 0.10)
close(B_tor, 1e-3)
close(mu0 * 500 / 0.10, 6.28e-3)
close(mu0 * 500 / (4 * 0.10), 1.57e-3)
q(MAG, "Ampere's law", "Basic", "numerical",
  "A toroid has 500 turns wound uniformly on a ring of mean radius 10 cm, and carries a current of 1.0 A. Taking "
  "µ₀ = 4π × 10⁻⁷ T m A⁻¹, the magnetic field inside the core of the toroid (within the windings, at the mean "
  "radius) is:",
  *opt("1.0 × 10⁻³ T", ["6.3 × 10⁻³ T", "1.6 × 10⁻³ T", "zero"], "D"),
  "Ampere's circuital law for a toroid: B = µ₀NI/(2πr)",
  "A circular Amperian loop of radius r inside the core links all N turns, each carrying I, so B(2πr) = µ₀NI.",
  ["B × 2πr = µ₀NI", "B = 4π × 10⁻⁷ × 500 × 1.0 / (2π × 0.10) = 1.0 × 10⁻³ T"],
  why="6.3 × 10⁻³ T leaves out the 2π in the circumference. 1.6 × 10⁻³ T uses 4r instead of 2πr. Zero is the field "
      "in the open space inside or outside the toroid, not within the windings.",
  ncert=MC + "the toroid", seconds=40, rc=True)

qch, vx, By = 2e-6, 3e4, 0.5
close(qch * vx * By, 0.03)
q(MAG, "Force on charges and conductors", "Basic", "numerical",
  "A particle of charge +2 µC moves with velocity 3 × 10⁴ m/s along the +x direction through a uniform magnetic "
  "field of 0.5 T along the +y direction. The magnetic force on the particle is:",
  *opt("0.03 N along +z", ["0.03 N along −z", "0.03 N along +y", "zero"], "A"),
  "Magnetic (Lorentz) force F = q(v × B)",
  "The force is perpendicular to both v and B. With v along x̂ and B along ŷ, x̂ × ŷ = ẑ, and the charge is positive.",
  ["|F| = qvB = 2 × 10⁻⁶ × 3 × 10⁴ × 0.5 = 0.03 N", "Direction: x̂ × ŷ = +ẑ"],
  why="−z is the direction for a negative charge (or for B × v). +y is along the field, but the magnetic force is "
      "always perpendicular to B. Zero would need v parallel to B.",
  ncert=MC + "magnetic force", seconds=35, rc=True)

q(MAG, "Biot-Savart law", "Basic", "direct",
  "A long straight vertical wire carries a steady current upwards. At a point a short distance due east of the wire, "
  "the magnetic field due to the current points:",
  *opt("towards the north", ["towards the south", "vertically upwards", "towards the east, away from the wire"], "A"),
  "Right-hand thumb rule for the field of a straight current",
  "Point the thumb of the right hand upwards along the current; the fingers curl anticlockwise as seen from above. "
  "At a point to the east of the wire, the anticlockwise circle is heading north.",
  ["Field lines: horizontal circles round the wire, anticlockwise seen from above",
   "Tangent at the east point of an anticlockwise circle points north"],
  why="South is the direction for a downward current. The field of a straight wire is perpendicular to the wire, so "
      "it cannot be vertical, and it is tangential to circles round the wire, not radial.",
  ncert=MC + "magnetic field on the axis of a straight wire / Ampere's circuital law", seconds=35)

q(MAG, "Torque on loop and galvanometer", "Basic", "direct",
  "A rigid plane loop of wire of any shape carries a steady current and is placed in a uniform magnetic field. The "
  "loop:",
  *opt("experiences zero net force, though it may experience a torque",
       ["experiences a net force along the field, but never a torque",
        "experiences a net force perpendicular to the field and no torque",
        "experiences neither a force nor a torque in any orientation"], "C"),
  "Force on a closed current loop in a uniform field; torque τ = m × B",
  "The force on the loop is I(∮dl) × B, and ∮dl = 0 for a closed loop, so the net force in a uniform field is zero. "
  "The forces on different parts can still form a couple, giving a torque m × B unless m is parallel or "
  "antiparallel to B.",
  ["F = I(∮dl) × B = 0", "τ = m × B ≠ 0 in general"],
  why="A net force on a current loop needs a non-uniform field. Saying it never feels a torque contradicts τ = m × B "
      "(e.g. the moving-coil galvanometer).",
  ncert=MC + "torque on current loop, magnetic dipole", seconds=30)

q(MAG, "Biot-Savart law", "Basic", "statement_pair",
  sp("The magnitude of the magnetic field due to a long straight wire carrying a steady current is inversely "
     "proportional to the distance from the wire.",
     "The magnetic field lines due to a long straight current-carrying wire are straight lines directed radially "
     "away from the wire."),
  SP, sp_key(True, False),
  "Field of a long straight wire: B = µ₀I/(2πr), along circles round the wire",
  "B = µ₀I/(2πr), so B ∝ 1/r (Statement I true). The field lines are concentric circles in planes perpendicular to "
  "the wire, not radial lines (Statement II false).",
  ["B = µ₀I/2πr → B ∝ 1/r → I true", "Field lines: concentric circles → II false"],
  why="Statement II describes the electric field of a line charge, not the magnetic field of a current.",
  ncert=MC + "Ampere's circuital law", seconds=30)

# ---- Intermediate
B_q = mu0 * 10 / (8 * 0.05)
close(B_q, math.pi * 1e-5)
close(mu0 * 10 / (2 * 0.05), 4 * math.pi * 1e-5)
close(mu0 * 10 / (4 * 0.05), 2 * math.pi * 1e-5)
close(mu0 * 10 / (8 * math.pi * 0.05), 1e-5)
q(MAG, "Biot-Savart law", "Intermediate", "numerical",
  "A closed loop of wire consists of a quarter of a circle of radius 5 cm (centre O) together with the two straight "
  "radii joining the ends of the arc to O. A steady current of 10 A flows round the loop. Taking "
  "µ₀ = 4π × 10⁻⁷ T m A⁻¹, the magnitude of the magnetic field at O is:",
  *opt("π × 10⁻⁵ T", ["4π × 10⁻⁵ T", "2π × 10⁻⁵ T", "1 × 10⁻⁵ T"], "C"),
  "Field at the centre of an arc: B = (µ₀I/2R) × (θ/2π); straight segments pointing at O give no field there",
  "Each straight radius lies along a line through O, so for every element dl × r̂ = 0 and it contributes nothing. "
  "The quarter arc gives one quarter of the field at the centre of a full loop.",
  ["Radial segments: dl ∥ r → zero field at O", "Arc: B = ¼ × µ₀I/(2R) = µ₀I/(8R)",
   "B = 4π × 10⁻⁷ × 10 / (8 × 0.05) = π × 10⁻⁵ T"],
  why="4π × 10⁻⁵ T is the field of a complete loop. 2π × 10⁻⁵ T is that of a semicircle. 1 × 10⁻⁵ T has an extra "
      "factor π in the denominator.",
  ncert=MC + "magnetic field on the axis of a circular current loop (centre)", seconds=60, rc=True)

mass = {"p": (1, 1), "d": (2, 1), "a": (4, 2)}
rr = {k: math.sqrt(m) / qq for k, (m, qq) in mass.items()}
close(rr["d"] / rr["p"], math.sqrt(2))
close(rr["a"] / rr["p"], 1.0)
q(MAG, "Force on charges and conductors", "Intermediate", "numerical",
  "A proton, a deuteron and an alpha particle, all having the same kinetic energy, enter a uniform magnetic field "
  "moving at right angles to it. Taking the masses in the ratio 1 : 2 : 4 and the charges in the ratio 1 : 1 : 2, "
  "the ratio of the radii of their circular paths, r_p : r_d : r_α, is:",
  *opt("1 : √2 : 1", ["1 : 2 : 2", "1 : √2 : √2", "1 : 1 : 1"], "B"),
  "r = mv/(qB) = √(2mK)/(qB); for the same K, r ∝ √m/q",
  "Writing the momentum in terms of kinetic energy, p = √(2mK), so at equal K the radius depends on √m/q.",
  ["r ∝ √m/q", "Proton: √1/1 = 1; deuteron: √2/1 = √2; alpha: √4/2 = 1", "r_p : r_d : r_α = 1 : √2 : 1"],
  why="1 : 2 : 2 uses r ∝ m/q (equal speeds). 1 : √2 : √2 uses r ∝ √(m/q), which holds for equal accelerating "
      "potential differences, not equal kinetic energies. 1 : 1 : 1 ignores the masses.",
  ncert=MC + "motion in a magnetic field", seconds=60, rc=True)

B_coax = 2e-7 * 5 / 0.02
close(B_coax, 5e-5)
close(2e-7 * 5 / 0.05, 2e-5)
close(1e-7 * 5 / 0.02, 2.5e-5)
q(MAG, "Ampere's law", "Intermediate", "numerical",
  "A long coaxial cable consists of a thin central wire and a thin coaxial cylindrical sheath of radius 3 cm. The "
  "wire carries a steady current of 5 A along the axis, and the sheath carries 5 A back in the opposite direction. "
  "Taking µ₀ = 4π × 10⁻⁷ T m A⁻¹, the magnitudes of the magnetic field at distances of 2 cm and 5 cm from the axis "
  "are, respectively:",
  *opt("5 × 10⁻⁵ T and zero", ["5 × 10⁻⁵ T and 2 × 10⁻⁵ T", "zero and zero", "2.5 × 10⁻⁵ T and zero"], "A"),
  "Ampere's circuital law with circular Amperian loops: B(2πr) = µ₀I_enclosed",
  "At r = 2 cm the loop encloses only the central wire's 5 A. At r = 5 cm it encloses both currents, which cancel, "
  "so the net enclosed current and hence B (by symmetry) are zero.",
  ["r = 2 cm: B = µ₀I/(2πr) = 2 × 10⁻⁷ × 5/0.02 = 5 × 10⁻⁵ T", "r = 5 cm: I_enc = 5 − 5 = 0 → B = 0"],
  why="2 × 10⁻⁵ T at 5 cm ignores the return current in the sheath. Zero at 2 cm wrongly counts the sheath current "
      "inside a loop that does not enclose it. 2.5 × 10⁻⁵ T uses µ₀I/(4πr).",
  ncert=MC + "Ampere's circuital law", seconds=60, rc=True)

tau_c = 50 * 2 * math.pi * 0.10 ** 2 * 0.5 * math.sin(math.radians(30))
close(tau_c, math.pi / 4)
close(50 * 2 * math.pi * 0.01 * 0.5 * math.sin(math.radians(60)), 1.36, 2e-3)
close(50 * 2 * math.pi * 0.01 * 0.5, 1.571, 1e-3)
q(MAG, "Torque on loop and galvanometer", "Intermediate", "numerical",
  "A flat circular coil of 50 turns, each of radius 10 cm, carries a current of 2.0 A. It is placed in a uniform "
  "magnetic field of 0.50 T so that the plane of the coil makes an angle of 60° with the direction of the field. "
  "The magnitude of the torque on the coil is about:",
  *opt("0.79 N m", ["1.36 N m", "1.57 N m", "0.39 N m"], "D"),
  "τ = NIAB sin θ, θ being the angle between the magnetic moment (normal to the coil) and B",
  "The magnetic moment is along the normal to the coil. If the plane makes 60° with B, the normal makes 30° with B.",
  ["θ (normal to B) = 90° − 60° = 30°", "NIA = 50 × 2.0 × π(0.10)² = π A m²",
   "τ = π × 0.50 × sin 30° = π/4 ≈ 0.79 N m"],
  why="1.36 N m uses 60° as the angle between the moment and the field. 1.57 N m is the maximum torque (θ = 90°). "
      "0.39 N m halves the correct value.",
  ncert=MC + "torque on rectangular current loop in a uniform magnetic field", seconds=60, rc=True)

Ig = 4e-6 * 25
Rser = 2.0 / Ig - 50
close(Ig, 1e-4)
close(Rser, 19950)
q(MAG, "Torque on loop and galvanometer", "Intermediate", "numerical",
  "A moving-coil galvanometer has a coil resistance of 50 Ω and a figure of merit (current per division) of 4 µA per "
  "division, and its scale has 25 divisions on either side of zero. To convert it into a voltmeter of range 0–2 V, "
  "one should connect:",
  *opt("19 950 Ω in series", ["20 000 Ω in series", "19 950 Ω in parallel", "1 950 Ω in series"], "C"),
  "Full-scale current from the figure of merit; voltmeter: high resistance in series, I_g(G + R) = V",
  "Full-scale current I_g = 4 µA × 25 = 100 µA. For a full-scale reading at 2 V, the total resistance must be "
  "2/(100 × 10⁻⁶) = 20 000 Ω, of which 50 Ω is the coil itself.",
  ["I_g = 25 × 4 µA = 1.0 × 10⁻⁴ A", "G + R = 2/(1.0 × 10⁻⁴) = 20 000 Ω", "R = 20 000 − 50 = 19 950 Ω, in series"],
  why="20 000 Ω forgets to subtract the coil resistance. A resistance in parallel is a shunt, which converts the "
      "galvanometer into an ammeter. 1 950 Ω uses a full-scale current ten times too large.",
  ncert=MC + "the moving coil galvanometer", seconds=60, rc=True)

q(MAG, "Force on charges and conductors", "Intermediate", "assertion_reason",
  ar("A charged particle enters a uniform magnetic field with its velocity inclined to the field. The pitch of its "
     "helical path does not depend on the component of its velocity perpendicular to the field.",
     "The time taken by a charged particle to complete one revolution in a uniform magnetic field, 2πm/(qB), does "
     "not depend on its speed."),
  AR, ar_key(True, True, True),
  "Helical motion: pitch p = v∥ T with T = 2πm/(qB)",
  "The pitch is the distance moved along the field during one revolution, p = v∥ × T. Because T = 2πm/(qB) is the "
  "same whatever the perpendicular speed, p depends only on v∥. R gives exactly this reason.",
  ["p = v∥ T", "T = 2πm/(qB), independent of v⊥", "So p is independent of v⊥; R explains A"],
  why="Both are true, and the speed-independence of the period is what makes the pitch independent of v⊥.",
  ncert=MC + "motion in a magnetic field", seconds=50)

q(MAG, "Ampere's law", "Intermediate", "match_list",
  ml("A steady current I flows in each arrangement. Match the location in List-I with the magnitude of the magnetic "
     "field there in List-II (n = turns per unit length, N = total turns, r = distance from the axis or centre, "
     "R = radius of the wire).",
     ["Inside a long straight wire of radius R carrying current spread uniformly over its cross-section, at r < R",
      "Within the windings (core) of a toroid of N turns, at distance r from its centre",
      "Outside an ideal long solenoid, away from its ends",
      "Well inside an ideal long solenoid"],
     ["µ₀nI", "µ₀NI/(2πr)", "µ₀Ir/(2πR²)", "Zero (practically)"]),
  *mlo("A-III, B-II, C-IV, D-I",
       ["A-II, B-III, C-IV, D-I", "A-III, B-I, C-IV, D-II", "A-III, B-II, C-I, D-IV"], "A"),
  "Applications of Ampere's circuital law",
  "Inside the wire the enclosed current is I r²/R², so B = µ₀Ir/(2πR²). In the toroid core, B(2πr) = µ₀NI. Outside "
  "an ideal solenoid the field is practically zero; inside, B = µ₀nI.",
  ["A → µ₀Ir/(2πR²) (III)", "B → µ₀NI/(2πr) (II)", "C → zero (IV)", "D → µ₀nI (I)"],
  why="A-II/B-III swaps the wire and toroid expressions. B-I/D-II swaps the toroid and solenoid. C-I/D-IV puts the "
      "uniform field outside the solenoid instead of inside.",
  ncert=MC + "Ampere's circuital law; the solenoid; the toroid", seconds=60)

q(MAG, "Torque on loop and galvanometer", "Intermediate", "multi_statement",
  ms("A moving-coil galvanometer is converted into an ammeter or into a voltmeter. Which of the following statements "
     "are correct?",
     ["An ammeter is made by connecting a low resistance (shunt) in parallel with the galvanometer.",
      "A voltmeter is made by connecting a high resistance in series with the galvanometer.",
      "An ideal ammeter has infinite resistance.",
      "The resistance of an ammeter made in this way is less than the resistance of its shunt.",
      "Connecting a series resistance to make a voltmeter increases the current sensitivity of the galvanometer."]),
  *mso({"a": True, "b": True, "c": False, "d": True, "e": False}, "abd", ["ab", "abc", "bde"], "D"),
  "Galvanometer as ammeter and voltmeter",
  "A shunt in parallel diverts most of the current (a true); a large series resistance limits the current for a "
  "given voltage (b true). An ideal ammeter has zero resistance so as not to change the current (c false). The "
  "parallel combination of G and S is smaller than S (d true). The current sensitivity NAB/k depends only on the "
  "galvanometer itself; a series resistance does not change it (e false).",
  ["(a) true", "(b) true", "(c) false: ideal ammeter → zero resistance", "(d) true: GS/(G + S) < S",
   "(e) false: NAB/k unchanged"],
  why="Options with (c) or (e) contain a false statement, and (a) and (b) only leaves out the true statement (d).",
  ncert=MC + "the moving coil galvanometer", seconds=60)

# ---- Advanced
q_r, w_r, R_r = 10e-6, 100.0, 0.10
I_ring = q_r * w_r / (2 * math.pi)
m_ring = I_ring * math.pi * R_r ** 2
close(m_ring, 5e-6)
close(q_r * w_r * R_r ** 2, 1e-5)
close(q_r * w_r * R_r ** 2 / (2 * math.pi), 1.59e-6, 2e-3)
close(q_r * w_r * R_r / 2, 5e-5)
q(MAG, "Magnetic dipole and bar magnet", "Advanced", "numerical",
  "A thin non-conducting ring of radius 10 cm carries a charge of 10 µC spread uniformly along it. It rotates about "
  "its own axis (the line through its centre perpendicular to its plane) at an angular speed of 100 rad/s. The "
  "magnetic dipole moment of the rotating ring is:",
  *opt("5 × 10⁻⁶ A m²", ["1 × 10⁻⁵ A m²", "1.6 × 10⁻⁶ A m²", "5 × 10⁻⁵ A m²"], "A"),
  "A rotating charge is a current I = q/T = qω/2π; magnetic moment m = IA",
  "The whole charge passes any point of the ring once per revolution, so the equivalent current is q/T = qω/(2π). "
  "This current circulates round an area πR².",
  ["I = qω/(2π) = 10⁻⁵ × 100/(2π) = (5 × 10⁻⁴/π) A", "m = I πR² = qωR²/2",
   "m = 10⁻⁵ × 100 × 0.01/2 = 5 × 10⁻⁶ A m²"],
  why="1 × 10⁻⁵ A m² misses the factor ½ (uses I = qω/π). 1.6 × 10⁻⁶ A m² multiplies by R² but forgets the π of "
      "the area. 5 × 10⁻⁵ A m² uses R instead of R².",
  ncert=MC + "the magnetic dipole (current loop as a magnetic dipole)", seconds=80, rc=True)

Lr, mr, Br, Ir, g = 0.5, 0.1, 0.5, 2.0, 10
th = math.degrees(math.atan(Br * Ir * Lr / (mr * g)))
close(th, 26.57, 1e-3)
assert Br * Ir * Lr / (mr * g) == 0.5
q(MAG, "Force on charges and conductors", "Advanced", "numerical",
  "A horizontal metal rod 0.50 m long and of mass 0.10 kg hangs from two light, flexible vertical conducting leads "
  "attached to its ends. A uniform vertical magnetic field of 0.50 T acts in the region, and a current of 2.0 A is "
  "passed through the rod. Taking g = 10 m/s², the rod swings aside and comes to rest with the leads inclined to "
  "the vertical at an angle of:",
  *opt("tan⁻¹(0.5), about 27°", ["30°", "tan⁻¹(2), about 63°", "45°"], "C"),
  "Force on a current-carrying conductor F = BIL; equilibrium of three forces",
  "The field is vertical and the rod horizontal, so the magnetic force BIL is horizontal. In equilibrium the leads' "
  "tension balances the resultant of the weight (vertical) and the magnetic force (horizontal).",
  ["F = BIL = 0.50 × 2.0 × 0.50 = 0.50 N (horizontal)", "mg = 0.10 × 10 = 1.0 N",
   "tan θ = F/mg = 0.5 → θ ≈ 27°"],
  why="30° takes sin θ = 0.5 instead of tan θ. tan⁻¹(2) inverts the ratio (mg/F). 45° assumes the two forces are "
      "equal.",
  ncert=MC + "magnetic force on a current-carrying conductor", seconds=90, rc=True)

qp, vp, Ey, Bz = 1.6e-19, 2e5, 4e4, 0.1
Fy = qp * (Ey + (-vp * Bz))
close(Fy, 3.2e-15)
close(qp * (Ey + vp * Bz), 9.6e-15)
q(MAG, "Force on charges and conductors", "Advanced", "numerical",
  "A proton (charge 1.6 × 10⁻¹⁹ C) moves with velocity 2 × 10⁵ m/s along the +x direction through a region where "
  "there is a uniform electric field of 4 × 10⁴ V/m along +y and a uniform magnetic field of 0.1 T along +z. The "
  "net (Lorentz) force on the proton at that instant is:",
  *opt("3.2 × 10⁻¹⁵ N along +y", ["9.6 × 10⁻¹⁵ N along +y", "3.2 × 10⁻¹⁵ N along −y", "zero"], "B"),
  "Lorentz force F = q(E + v × B)",
  "The electric force qE is along +y. The magnetic force qv × B has x̂ × ẑ = −ŷ, so it is along −y. The two partly "
  "cancel; they would cancel completely only if v = E/B = 4 × 10⁵ m/s.",
  ["qE = 1.6 × 10⁻¹⁹ × 4 × 10⁴ = 6.4 × 10⁻¹⁵ N along +y",
   "qvB = 1.6 × 10⁻¹⁹ × 2 × 10⁵ × 0.1 = 3.2 × 10⁻¹⁵ N along −y (x̂ × ẑ = −ŷ)",
   "Net = 3.2 × 10⁻¹⁵ N along +y"],
  why="9.6 × 10⁻¹⁵ N takes the magnetic force along +y (wrong sign of x̂ × ẑ). −y reverses the larger, electric "
      "force. Zero assumes the fields balance, which needs v = E/B = 4 × 10⁵ m/s, not 2 × 10⁵ m/s.",
  ncert=MC + "magnetic force (Lorentz force)", seconds=80, rc=True)

q(MAG, "Force on charges and conductors", "Advanced", "assertion_reason",
  ar("Two identical charged particles move at right angles to the same uniform magnetic field, one with twice the "
     "speed of the other. The faster particle takes longer to complete one revolution.",
     "The radius of the circular path of a charged particle moving at right angles to a uniform magnetic field is "
     "proportional to its speed."),
  AR, ar_key(False, True),
  "r = mv/(qB); T = 2πr/v = 2πm/(qB)",
  "The faster particle moves in a circle of twice the radius but at twice the speed, so its period 2πm/(qB) is "
  "the same: A is false. R (r ∝ v) is true.",
  ["r = mv/(qB) ∝ v → R true", "T = 2πr/v = 2πm/(qB), independent of v → A false"],
  why="A is false because the period does not depend on speed; R is a true statement, so the key is 'A false, R true'.",
  ncert=MC + "motion in a magnetic field", seconds=45)

q(MAG, "Force on charges and conductors", "Advanced", "match_list",
  ml("A charged particle (weight negligible) moves in the field region described in List-I. Match each case with the "
     "path or motion in List-II.",
     ["Uniform electric field only; particle released from rest",
      "Uniform magnetic field only; velocity perpendicular to the field",
      "Uniform magnetic field only; velocity at an acute angle to the field",
      "Uniform electric and magnetic fields perpendicular to each other; velocity perpendicular to both and of "
      "magnitude E/B, in the direction for which the two forces are opposite"],
     ["Helix with its axis along the field", "Straight line with constant velocity",
      "Straight line with uniform acceleration", "Circle traversed at constant speed"]),
  *mlo("A-III, B-IV, C-I, D-II",
       ["A-IV, B-III, C-I, D-II", "A-III, B-I, C-IV, D-II", "A-II, B-IV, C-I, D-III"], "B"),
  "Motion of charges in electric and magnetic fields; velocity selector",
  "From rest in a uniform E, the constant force qE gives uniformly accelerated straight-line motion. A uniform B "
  "perpendicular to v gives uniform circular motion. With an acute angle, the parallel component is unaffected, so "
  "the path is a helix. In crossed fields with v = E/B the forces qE and qvB cancel, so the particle goes straight "
  "at constant velocity.",
  ["A → III", "B → IV", "C → I", "D → II"],
  why="A-IV/B-III swaps the electric-field and magnetic-field motions. B-I/C-IV swaps the circle and the helix. "
      "A-II/D-III swaps the uniformly accelerated and the undeflected motions.",
  ncert=MC + "motion in combined electric and magnetic fields (velocity selector)", seconds=60)

q(MAG, "Magnetic materials", "Advanced", "multi_statement",
  ms("Which of the following statements about magnetic materials are correct?",
     ["The individual atoms of a paramagnetic substance possess permanent magnetic dipole moments.",
      "In a weak field at room temperature, the atomic dipoles of a paramagnetic substance line up completely "
      "along the field.",
      "In a diamagnetic substance placed in a magnetic field, the electron orbits are modified so as to produce a "
      "net magnetic moment opposite to the field.",
      "A superconductor expels a magnetic field completely from its interior (the Meissner effect).",
      "The relative permeability of a superconductor is 1."]),
  *mso({"a": True, "b": False, "c": True, "d": True, "e": False}, "acd", ["ac", "abd", "cde"], "C"),
  "Microscopic picture of para- and diamagnetism; superconductors as perfect diamagnets",
  "Paramagnetic atoms have permanent dipole moments (a true), but thermal agitation keeps them largely random; only "
  "strong fields at low temperatures approach full alignment (b false). Diamagnetism arises from induced moments "
  "opposite to the field (c true). Superconductors are perfect diamagnets: the field is expelled (d true), χ = −1, "
  "so µ_r = 1 + χ = 0, not 1 (e false).",
  ["(a) true", "(b) false: thermal agitation prevents full alignment", "(c) true", "(d) true",
   "(e) false: µ_r = 0"],
  why="Options with (b) or (e) include a false statement, and (a) and (c) only misses the true statement (d).",
  ncert=MM + "magnetic properties of materials", seconds=70)


# ================================================================ EMI and AC (B4 I6 A4)
EC = NC + "'Electromagnetic Induction', "
ACC = NC + "'Alternating Current', "

# ---- Basic
emf_e1 = 0.05 * (0.4 - 0) / 0.02
I_e1 = emf_e1 / 2
close(emf_e1, 1.0)
close(I_e1, 0.5)
close(0.05 * 0.4 / 2, 0.01)
q(EMI, "Faraday's and Lenz's laws", "Basic", "numerical",
  "A single-turn conducting loop of area 0.05 m² and resistance 2 Ω lies with its plane perpendicular to a uniform "
  "magnetic field. The field is reduced uniformly from 0.4 T to zero in 0.02 s. The current induced in the loop "
  "during this time is:",
  *opt("0.5 A", ["1.0 A", "2.0 A", "0.01 A"], "B"),
  "Faraday's law ε = |ΔΦ|/Δt; Ohm's law I = ε/R",
  "The flux falls from BA to zero at a steady rate, so the emf is constant during the change.",
  ["ΔΦ = 0.4 × 0.05 = 0.02 Wb", "ε = 0.02/0.02 = 1.0 V", "I = ε/R = 1.0/2 = 0.5 A"],
  why="1.0 A takes the emf (in volts) as the current. 2.0 A multiplies the emf by R. 0.01 A divides the flux change "
      "by R but forgets to divide by the time.",
  ncert=EC + "Faraday's law of induction", seconds=40, rc=True)

M_e2 = 4e-3 / 2
close(M_e2, 2e-3)
q(EMI, "Self and mutual inductance", "Basic", "numerical",
  "A steady current of 2.0 A in coil 1 produces a total magnetic flux linkage of 4.0 × 10⁻³ Wb with a nearby coil 2. "
  "The mutual inductance of the pair of coils is:",
  *opt("2.0 mH", ["8.0 mH", "4.0 mH", "500 H"], "D"),
  "Mutual inductance: N₂Φ₂ = M I₁",
  "The flux linkage of coil 2 is proportional to the current in coil 1; the constant of proportionality is M.",
  ["M = N₂Φ₂/I₁ = 4.0 × 10⁻³/2.0", "M = 2.0 × 10⁻³ H = 2.0 mH"],
  why="8.0 mH multiplies the flux linkage by the current. 4.0 mH ignores the current. 500 H divides the current by "
      "the flux linkage.",
  ncert=EC + "inductance - mutual inductance", seconds=30, rc=True)

q(EMI, "Faraday's and Lenz's laws", "Basic", "direct",
  "A rectangular conducting loop lies in the plane of the page, partly inside a region of uniform magnetic field "
  "directed into the page. The loop is pulled out of the field region at constant velocity. As seen by a reader "
  "looking at the page, the current induced in the loop while it is leaving the field is:",
  *opt("clockwise", ["anticlockwise", "zero, because the loop moves at constant velocity",
                     "clockwise in one half of the loop and anticlockwise in the other"], "A"),
  "Lenz's law: the induced current opposes the change in flux",
  "As the loop leaves the field, the flux into the page through it decreases. The induced current tries to maintain "
  "this flux, so it produces a field into the page inside the loop; by the right-hand rule, that is a clockwise "
  "current as seen by the reader.",
  ["Flux into the page decreases", "Induced field: into the page inside the loop", "Current: clockwise"],
  why="Anticlockwise would increase the decrease in flux, violating Lenz's law. Constant velocity still changes the "
      "flux, so there is an emf. A single loop carries one current all the way round.",
  ncert=EC + "Lenz's law and conservation of energy", seconds=35)

q(EMI, "AC generator and transformer", "Basic", "statement_pair",
  sp("For an ideal transformer, the ratio of the secondary voltage to the primary voltage equals the ratio of the "
     "number of turns in the secondary to that in the primary.",
     "The frequency of the alternating emf produced by an AC generator equals the number of rotations made by its "
     "coil per second."),
  SP, sp_key(True, True),
  "Transformer equation V_s/V_p = N_s/N_p; AC generator emf ε = NBAω sin ωt",
  "In an ideal transformer each turn has the same emf, so V_s/V_p = N_s/N_p (Statement I true). In a generator the "
  "emf goes through one complete cycle for each rotation of the coil, so ν = ω/2π is the number of rotations per "
  "second (Statement II true).",
  ["V_s/V_p = N_s/N_p → I true", "ε = ε₀ sin ωt, ω = 2πν → one cycle per rotation → II true"],
  why="Both statements are standard NCERT results, so the options calling either false are wrong.",
  ncert=EC + "AC generator; " + ACC + "transformers", seconds=35)

# ---- Intermediate
t_e = math.asin(100 / 200) / (100 * math.pi)
close(t_e, 1 / 600)
close(math.asin(math.sqrt(3) / 2) / (100 * math.pi), 1 / 300)
q(EMI, "AC: rms, reactance and impedance", "Intermediate", "numerical",
  "An alternating voltage is given by v = 200 sin(100πt), with v in volts and t in seconds. The least time after "
  "t = 0 at which the instantaneous voltage becomes 100 V is:",
  *opt("1/600 s", ["1/300 s", "1/200 s", "1/1200 s"], "C"),
  "Instantaneous value v = v₀ sin ωt",
  "Setting v = v₀/2 gives sin ωt = 1/2, whose smallest positive solution is ωt = π/6.",
  ["200 sin(100πt) = 100 → sin(100πt) = 1/2", "100πt = π/6 → t = 1/600 s"],
  why="1/300 s uses ωt = π/3 (where sin = √3/2). 1/200 s is the time to reach the peak (ωt = π/2). 1/1200 s uses "
      "ωt = π/12.",
  ncert=ACC + "AC voltage applied to a resistor", seconds=45, rc=True)

I_ss = 12 / (2 + 4)
U_ss = 0.5 * 0.2 * I_ss ** 2
close(U_ss, 0.4)
close(0.2 * I_ss ** 2, 0.8)
close(0.5 * 0.2 * (12 / 4) ** 2, 0.9)
q(EMI, "Self and mutual inductance", "Intermediate", "numerical",
  "An ideal inductor of inductance 0.20 H (no resistance) is connected in series with a 4 Ω resistor across a "
  "battery of emf 12 V and internal resistance 2 Ω. Long after the circuit is closed, the energy stored in the "
  "magnetic field of the inductor is:",
  *opt("0.4 J", ["0.8 J", "0.9 J", "zero"], "A"),
  "Steady DC: an ideal inductor has no p.d. across it; magnetic energy U = ½LI²",
  "Once the current is steady, dI/dt = 0, so the ideal inductor behaves as a plain wire and the current is fixed "
  "by the resistances. The inductor still stores energy ½LI² because a current flows through it.",
  ["Steady current I = 12/(4 + 2) = 2 A", "U = ½ × 0.20 × 2² = 0.4 J"],
  why="0.8 J forgets the factor ½. 0.9 J ignores the internal resistance (I = 3 A). Zero confuses the absence of a "
      "self-induced emf with the absence of stored energy.",
  ncert=EC + "inductance - self-inductance", seconds=60, rc=True)

Vs = 230 * 20
Is = Vs / 2300
Ip = Is * 20
assert Vs == 4600 and Is == 2 and Ip == 40
q(EMI, "AC generator and transformer", "Intermediate", "numerical",
  "An ideal step-up transformer has a turns ratio N_p : N_s = 1 : 20. Its primary is connected to a 230 V AC "
  "supply and its secondary to a 2300 Ω resistive load. The currents in the secondary and in the primary are, "
  "respectively:",
  *opt("2 A and 40 A", ["2 A and 0.1 A", "40 A and 2 A", "0.1 A and 2 A"], "B"),
  "V_s/V_p = N_s/N_p; ideal transformer: V_p I_p = V_s I_s",
  "The secondary voltage is 20 × 230 = 4600 V, which drives 2 A through the load. Since no power is lost, the "
  "primary current is 20 times the secondary current.",
  ["V_s = 230 × 20 = 4600 V", "I_s = 4600/2300 = 2 A", "I_p = I_s × (N_s/N_p) = 40 A"],
  why="0.1 A for the primary makes the current step up with the voltage (violating energy conservation). 40 A and "
      "2 A swaps the two currents. 0.1 A for the secondary uses 230 V across the load.",
  ncert=ACC + "transformers", seconds=60, rc=True)

f_eq = 50 * math.sqrt(100 / 25)
close(f_eq, 100)
q(EMI, "LCR resonance and power", "Intermediate", "numerical",
  "At a frequency of 50 Hz, a certain capacitor has a reactance of 100 Ω and a certain inductor has a reactance of "
  "25 Ω. If the two are connected in series with a resistor, the circuit will be in resonance at a frequency of:",
  *opt("100 Hz", ["200 Hz", "25 Hz", "12.5 Hz"], "A"),
  "X_L = ωL ∝ f, X_C = 1/(ωC) ∝ 1/f; resonance when X_L = X_C",
  "Raising the frequency by a factor k multiplies X_L by k and divides X_C by k. They become equal when "
  "25k = 100/k, i.e. k² = 4.",
  ["25k = 100/k → k² = 4 → k = 2", "f₀ = 2 × 50 = 100 Hz"],
  why="200 Hz takes k = 4 (forgetting the square root). 25 Hz lowers the frequency, which makes X_C even larger. "
      "12.5 Hz uses k = 1/4.",
  ncert=ACC + "series LCR circuit - resonance", seconds=60, rc=True)

q(EMI, "Self and mutual inductance", "Intermediate", "assertion_reason",
  ar("For a long air-cored solenoid of fixed length and cross-section, the self-inductance is proportional to the "
     "square of the number of turns per unit length.",
     "The self-induced emf in a coil always opposes the change in the current through it."),
  AR, ar_key(True, True, False),
  "L = µ₀n²Al for a long solenoid; Lenz's law for self-induction",
  "Doubling n doubles the field B = µ₀nI and also doubles the number of turns it links, so L = µ₀n²Al (A true). R "
  "is also true (Lenz's law), but it describes the direction of the self-induced emf, not why L depends on n²; it "
  "does not explain A.",
  ["Flux linkage NΦ = (nl)(µ₀nI)A → L = µ₀n²Al → A true", "R: Lenz's law → true",
   "R concerns the sign of the emf, not the n² dependence → not the explanation"],
  why="R is true but is about the direction of the induced emf; the n² dependence comes from n appearing both in the "
      "field and in the number of turns linked.",
  ncert=EC + "inductance - self-inductance", seconds=50)

q(EMI, "AC generator and transformer", "Intermediate", "match_list",
  ml("Match each source of energy loss in a practical transformer (List-I) with the way it is reduced (List-II), as "
     "described in NCERT.",
     ["Flux leakage", "Resistance of the windings", "Eddy currents in the iron core",
      "Hysteresis (repeated magnetisation and demagnetisation of the core)"],
     ["Using a laminated core", "Using a core material with a low hysteresis loss",
      "Winding the primary and secondary coils one over the other",
      "Using thick wire for windings carrying large currents"]),
  *mlo("A-III, B-IV, C-I, D-II",
       ["A-IV, B-III, C-I, D-II", "A-III, B-IV, C-II, D-I", "A-I, B-IV, C-III, D-II"], "D"),
  "Energy losses in transformers",
  "Leakage is reduced by winding the coils over each other so that they share the flux. Joule heating in the "
  "windings is reduced by thick (low-resistance) wire. Eddy currents are reduced by laminating the core. Hysteresis "
  "loss is reduced by choosing a core material with a low hysteresis loss.",
  ["A → III", "B → IV", "C → I", "D → II"],
  why="A-IV/B-III swaps leakage and winding resistance. C-II/D-I swaps the eddy-current and hysteresis remedies. "
      "A-I/C-III swaps leakage and eddy currents.",
  ncert=ACC + "transformers", seconds=50)

# ---- Advanced
R_l, X0 = 30.0, 20.0
Z2 = math.hypot(R_l, 2 * X0 - X0 / 2)
close(Z2, 30 * math.sqrt(2))
close(R_l + 2 * X0 - X0 / 2, 60)
close(math.hypot(R_l, 2 * X0 + X0 / 2), 58.3, 1e-3)
q(EMI, "LCR resonance and power", "Advanced", "numerical",
  "A series LCR circuit with R = 30 Ω is at resonance when driven at a frequency f₀; at this frequency the inductive "
  "and capacitive reactances are each 20 Ω. The source frequency is now changed to 2f₀, all components unchanged. "
  "The impedance of the circuit becomes:",
  *opt("30√2 Ω (about 42 Ω)", ["30 Ω", "60 Ω", "about 58 Ω"], "C"),
  "X_L ∝ f, X_C ∝ 1/f; Z = √[R² + (X_L − X_C)²]",
  "At 2f₀ the inductive reactance doubles to 40 Ω and the capacitive reactance halves to 10 Ω.",
  ["X_L = 40 Ω, X_C = 10 Ω", "Z = √(30² + 30²) = 30√2 ≈ 42 Ω"],
  why="30 Ω is the impedance at resonance. 60 Ω adds R and (X_L − X_C) arithmetically instead of in quadrature. "
      "About 58 Ω adds the two reactances instead of subtracting them.",
  ncert=ACC + "series LCR circuit", seconds=75, rc=True)

I_w, v_l, l_l, x1, a_l = 10.0, 5.0, 0.2, 0.1, 0.3
emf_l = 2e-7 * I_w * v_l * l_l * (1 / x1 - 1 / (x1 + a_l))
close(emf_l, 1.5e-5)
close(2e-7 * I_w * v_l * l_l / x1, 2e-5)
close(2e-7 * I_w * v_l * l_l * (1 / x1 + 1 / (x1 + a_l)), 2.5e-5)
close(2e-7 * I_w * v_l * l_l / (x1 + a_l), 5e-6)
q(EMI, "Faraday's and Lenz's laws", "Advanced", "numerical",
  "A long straight wire carries a steady current of 10 A. A rectangular conducting loop lies in the same plane, with "
  "two of its sides, each 0.20 m long, parallel to the wire; at a certain instant these sides are 0.10 m and 0.40 m "
  "from the wire. The loop moves directly away from the wire with a speed of 5.0 m/s. Taking "
  "µ₀/2π = 2 × 10⁻⁷ T m A⁻¹, the emf induced in the loop at this instant is:",
  *opt("15 µV", ["20 µV", "25 µV", "5 µV"], "A"),
  "Motional emf Blv in each side parallel to the wire; B = µ₀I/(2πx)",
  "The two sides perpendicular to the wire move along their own length and have no motional emf. The two parallel "
  "sides each have an emf Blv, but they are in opposite senses round the loop, so the net emf is the difference.",
  ["Near side: ε₁ = (µ₀I/2πx₁) l v = 2 × 10⁻⁷ × 10 × 0.20 × 5.0/0.10 = 20 µV",
   "Far side: ε₂ = 2 × 10⁻⁷ × 10 × 0.20 × 5.0/0.40 = 5 µV", "Net emf = 20 − 5 = 15 µV"],
  why="20 µV counts only the near side. 25 µV adds the two emfs although they oppose each other round the loop. "
      "5 µV counts only the far side.",
  ncert=EC + "motional electromotive force", seconds=100, rc=True)

q(EMI, "AC: rms, reactance and impedance", "Advanced", "statement_pair",
  sp("When an ideal inductor is connected to an AC source, the average power over a complete cycle is zero, although "
     "the instantaneous power is non-zero at most instants.",
     "When an ideal inductor is connected to an AC source, the instantaneous power delivered to it is positive at "
     "every instant."),
  SP, sp_key(True, False),
  "Power in a purely inductive circuit: p = vi with i lagging v by π/2",
  "With i lagging v by π/2, p = v₀i₀ sin ωt sin(ωt − π/2) = −½v₀i₀ sin 2ωt. It is non-zero except at isolated "
  "instants and averages to zero (Statement I true). It is negative for half the time, when the inductor returns "
  "its stored energy to the source (Statement II false).",
  ["p = −½v₀i₀ sin 2ωt", "Average over a cycle = 0 → I true", "p < 0 for half of each cycle → II false"],
  why="Statement II ignores the quarter-cycles in which the inductor gives back the energy stored in its field.",
  ncert=ACC + "AC voltage applied to an inductor", seconds=60)

q(EMI, "AC generator and transformer", "Advanced", "multi_statement",
  ms("The coil of an AC generator, having N turns each of area A, rotates with a constant angular speed ω in a "
     "uniform magnetic field B, about an axis perpendicular to the field. Which of the following statements are "
     "correct?",
     ["The magnetic flux through the coil is maximum at the instants when the induced emf is zero.",
      "The induced emf is given by ε = NBAω sin ωt, taking the coil's plane perpendicular to B at t = 0.",
      "Doubling the number of turns, everything else unchanged, doubles the peak emf.",
      "The frequency of the induced emf depends on the strength of the magnetic field.",
      "In hydroelectric generators, the coil is rotated by water falling from a height."]),
  *mso({"a": True, "b": True, "c": True, "d": False, "e": True}, "abce", ["abc", "abde", "bce"], "B"),
  "AC generator: Φ = NBA cos ωt, ε = NBAω sin ωt",
  "Φ = NBA cos ωt is maximum when sin ωt = 0, i.e. when ε = 0 (a true). ε = −dΦ/dt = NBAω sin ωt (b true). The peak "
  "emf NBAω is proportional to N (c true). The frequency is ω/2π, set by the rotation rate, not by B (d false). "
  "NCERT notes that in hydroelectric generators the falling water rotates the coil (e true).",
  ["(a) true: Φ max ↔ ε = 0", "(b) true", "(c) true: ε₀ = NBAω ∝ N", "(d) false: ν = ω/2π", "(e) true"],
  why="Options with (d) include a false statement; (a), (b) and (c) only and (b), (c) and (e) only each leave out a "
      "true statement.",
  ncert=EC + "AC generator", seconds=75)


# ================================================================ Electromagnetic Waves (B1 I2 A1)
WC = NC + "'Electromagnetic Waves', "

q(EMW, "EM spectrum and uses", "Basic", "direct",
  "Infrared waves are sometimes referred to as heat waves. According to NCERT, this is because:",
  *opt("water molecules present in most materials readily absorb infrared waves, which increases their thermal "
       "motion and so heats the material",
       ["infrared waves travel faster than visible light in vacuum",
        "infrared waves are produced only by bodies at very high temperatures, such as the Sun",
        "infrared waves carry electric charge that heats the material they fall on"], "D"),
  "Infrared radiation and its heating effect",
  "Many molecules, especially water, absorb infrared strongly. The absorbed energy increases their thermal motion, "
  "raising the temperature of the material.",
  ["Infrared is absorbed by water molecules", "Absorption increases thermal agitation → heating"],
  why="All electromagnetic waves travel at c in vacuum. Infrared is emitted by hot bodies and molecules generally, "
      "not only very hot ones. Electromagnetic waves carry no charge.",
  ncert=WC + "electromagnetic spectrum - infrared waves", seconds=30)

B0w, kw, ww = 2e-7, 0.5e3, 1.5e11
assert math.isclose(ww / kw, 3e8)
close(3e8 * B0w, 60)
q(EMW, "EM wave properties", "Intermediate", "numerical",
  "The magnetic field of a plane electromagnetic wave in vacuum is B_y = 2 × 10⁻⁷ sin(0.5 × 10³ x + 1.5 × 10¹¹ t) T, "
  "with x in metres and t in seconds. Taking c = 3 × 10⁸ m/s, the amplitude of the electric field of the wave and "
  "its direction of propagation are:",
  *opt("60 V/m; along −x", ["60 V/m; along +x", "6.7 × 10⁻¹⁶ V/m; along −x", "60 V/m; along +y"], "B"),
  "E₀ = cB₀; a wave sin(kx + ωt) travels towards −x",
  "The amplitudes are related by E₀ = cB₀. The phase kx + ωt stays constant if x decreases as t increases, so the "
  "wave travels along −x. (Check: ω/k = 1.5 × 10¹¹/0.5 × 10³ = 3 × 10⁸ m/s = c.)",
  ["E₀ = 3 × 10⁸ × 2 × 10⁻⁷ = 60 V/m", "Phase (kx + ωt) → propagation along −x"],
  why="+x is the direction for sin(kx − ωt). 6.7 × 10⁻¹⁶ V/m divides B₀ by c instead of multiplying. The wave "
      "cannot travel along y, the direction of its own magnetic field.",
  ncert=WC + "electromagnetic waves", seconds=60, rc=True)

Id_w = 8.85e-12 * 4e8
close(Id_w, 3.54e-3)
close(4e8 / 8.85e-12, 4.52e19, 1e-3)
q(EMW, "Displacement current", "Intermediate", "numerical",
  "While a capacitor is being charged, the electric flux through a surface between its plates increases at the rate "
  "of 4.0 × 10⁸ V m s⁻¹. Taking ε₀ = 8.85 × 10⁻¹² C² N⁻¹ m⁻², the displacement current through that surface is about:",
  *opt("3.5 mA", ["4.5 × 10¹⁹ A", "3.5 A", "zero, since no charge crosses the gap"], "A"),
  "Displacement current i_d = ε₀ dΦ_E/dt",
  "Maxwell's displacement current is ε₀ times the rate of change of electric flux. It exists even though no charge "
  "flows across the gap.",
  ["i_d = 8.85 × 10⁻¹² × 4.0 × 10⁸", "i_d ≈ 3.5 × 10⁻³ A = 3.5 mA"],
  why="4.5 × 10¹⁹ A divides by ε₀ instead of multiplying. 3.5 A is off by a factor of 1000. Zero ignores the "
      "displacement current, which is exactly what keeps the total current continuous.",
  ncert=WC + "displacement current", seconds=40, rc=True)

q(EMW, "EM spectrum and uses", "Advanced", "match_list",
  ml("Match each part of the electromagnetic spectrum in List-I with its approximate wavelength range in List-II, "
     "as given in NCERT.",
     ["Radio waves", "Microwaves", "Infrared", "Ultraviolet"],
     ["400 nm to 1 nm", "1 mm to 700 nm", "> 0.1 m", "0.1 m to 1 mm"]),
  *mlo("A-III, B-IV, C-II, D-I",
       ["A-IV, B-III, C-II, D-I", "A-III, B-IV, C-I, D-II", "A-III, B-II, C-IV, D-I"], "D"),
  "Wavelength ranges of the electromagnetic spectrum",
  "In order of decreasing wavelength: radio waves (> 0.1 m), microwaves (0.1 m to 1 mm), infrared (1 mm to 700 nm), "
  "visible light (700 nm to 400 nm), ultraviolet (400 nm to 1 nm), X-rays and gamma rays.",
  ["A → > 0.1 m (III)", "B → 0.1 m to 1 mm (IV)", "C → 1 mm to 700 nm (II)", "D → 400 nm to 1 nm (I)"],
  why="A-IV/B-III swaps radio waves and microwaves. C-I/D-II swaps infrared and ultraviolet across the visible band. "
      "B-II/C-IV swaps microwaves and infrared.",
  ncert=WC + "electromagnetic spectrum (Table 8.1)", seconds=50)


# ================================================================ Optics (B7 I8 A7)
RO = NC + "'Ray Optics and Optical Instruments', "
WO = NC + "'Wave Optics', "


def mirror_v(f, u):
    return 1 / (1 / f - 1 / u)


def lens_v(f, u):
    return 1 / (1 / f + 1 / u)


# ---- Basic
v_o1 = mirror_v(-20, -60)
m_o1 = -v_o1 / -60
close(v_o1, -30)
close(m_o1, -0.5)
close(3 * -mirror_v(-40, -60) / -60, -6)
q(OPT, "Mirrors", "Basic", "numerical",
  "An object 3.0 cm tall stands on the principal axis of a concave mirror of radius of curvature 40 cm, 60 cm in "
  "front of the mirror. The size and nature of the image are:",
  *opt("1.5 cm, inverted", ["1.5 cm, erect", "6.0 cm, inverted", "0.75 cm, inverted"], "C"),
  "f = R/2; mirror formula 1/v + 1/u = 1/f; m = −v/u",
  "With the Cartesian sign convention, f = −20 cm and u = −60 cm (object beyond C), so a real, inverted, diminished "
  "image forms between F and C.",
  ["f = −40/2 = −20 cm", "1/v = 1/f − 1/u = −1/20 + 1/60 = −1/30 → v = −30 cm",
   "m = −v/u = −(−30)/(−60) = −0.5 → h' = −1.5 cm (inverted)"],
  why="Erect contradicts the negative magnification of a real image. 6.0 cm takes f = R = 40 cm. 0.75 cm uses "
      "m = 1/4.",
  ncert=RO + "the mirror equation", seconds=45, rc=True)

v_o2 = lens_v(-15, -30)
close(v_o2, -10)
close(v_o2 / -30, 1 / 3)
close(lens_v(15, -30), 30)
q(OPT, "Refraction and lenses", "Basic", "numerical",
  "An object is placed 30 cm in front of a thin concave lens of focal length 15 cm. The image formed is:",
  *opt("10 cm from the lens on the same side as the object; virtual, erect and one-third the size of the object",
       ["30 cm from the lens on the other side; real, inverted and of the same size as the object",
        "10 cm from the lens on the other side; real, inverted and one-third the size of the object",
        "30 cm from the lens on the same side; virtual, erect and of the same size as the object"], "B"),
  "Thin lens formula 1/v − 1/u = 1/f; m = v/u",
  "For a concave lens f = −15 cm; with u = −30 cm, the image is virtual and on the object side, as always for a "
  "concave lens with a real object.",
  ["1/v = 1/f + 1/u = −1/15 − 1/30 = −1/10 → v = −10 cm", "m = v/u = (−10)/(−30) = +1/3"],
  why="30 cm on the other side, same size, is the result for a convex lens of focal length 15 cm. A concave lens "
      "cannot form a real image of a real object. 30 cm on the same side ignores the lens formula.",
  ncert=RO + "thin lens formula", seconds=40, rc=True)

close((1.5 - 1) * 4, 2.0)
close(1.5 * 4, 6.0)
close(4 / 1.5, 2.67, 2e-3)
q(OPT, "Prism", "Basic", "numerical",
  "A thin prism of refracting angle 4° is made of glass of refractive index 1.5. The deviation it produces in a ray "
  "of light passing through it (at near-normal incidence) is:",
  *opt("2°", ["6°", "2.7°", "1°"], "A"),
  "Deviation by a thin prism: δ = (n − 1)A",
  "For a thin prism and small angles, the minimum deviation reduces to δ = (n − 1)A.",
  ["δ = (1.5 − 1) × 4° = 2°"],
  why="6° uses nA instead of (n − 1)A. 2.7° divides A by n. 1° has an extra factor ½.",
  ncert=RO + "refraction through a prism", seconds=25, rc=True)

I_m = 8 * math.cos(math.radians(60)) ** 2
close(I_m, 2.0)
close(8 * math.cos(math.radians(60)), 4.0)
close(8 * math.sin(math.radians(60)) ** 2, 6.0)
q(OPT, "Polarisation", "Basic", "numerical",
  "Plane-polarised light of intensity 8.0 W m⁻² falls normally on an ideal polaroid whose pass axis makes an angle "
  "of 60° with the direction of vibration of the electric field of the light. The intensity of the transmitted "
  "light is:",
  *opt("2.0 W m⁻²", ["4.0 W m⁻²", "6.0 W m⁻²", "1.0 W m⁻²"], "D"),
  "Malus' law: I = I₀ cos² θ",
  "Only the component of E along the pass axis, E₀ cos θ, is transmitted; intensity goes as the square of the "
  "amplitude.",
  ["I = 8.0 × cos² 60° = 8.0 × ¼ = 2.0 W m⁻²"],
  why="4.0 W m⁻² uses cos θ instead of cos² θ. 6.0 W m⁻² uses sin² θ. 1.0 W m⁻² halves again, as if the incident "
      "light were unpolarised.",
  ncert=WO + "polarisation", seconds=30, rc=True)

q(OPT, "Polarisation", "Basic", "direct",
  "A polaroid consists of long-chain molecules aligned in a particular direction. When unpolarised light falls on "
  "it, according to NCERT:",
  *opt("the electric vectors along the direction of the aligned molecules are absorbed, so the pass axis is "
       "perpendicular to the molecules",
       ["the electric vectors perpendicular to the aligned molecules are absorbed, so the pass axis is along the "
        "molecules",
        "the light is reflected from the molecules, which polarises it",
        "all the electric vectors are transmitted, but their frequency is halved"], "C"),
  "Working of a polaroid",
  "The long-chain molecules absorb the component of the electric field parallel to their length. The component "
  "perpendicular to them is transmitted, so the pass axis is perpendicular to the aligned molecules.",
  ["Component along the molecules → absorbed", "Component perpendicular → transmitted (pass axis)"],
  why="The second option reverses absorption and transmission. A polaroid works by selective absorption, not "
      "reflection. Polarisation never changes the frequency of light.",
  ncert=WO + "polarisation", seconds=30)

q(OPT, "Mirrors", "Basic", "direct",
  "A convex mirror is preferred as a rear-view mirror in vehicles mainly because, for real objects behind the "
  "vehicle, it:",
  *opt("always forms an erect, diminished image and so gives a wider field of view",
       ["forms a real, inverted image that can be seen on a screen",
        "forms a magnified image of nearby vehicles",
        "forms an image at the same distance as the object, like a plane mirror"], "A"),
  "Image formation by a convex mirror",
  "A convex mirror forms a virtual, erect, diminished image of every real object, between the pole and the focus. "
  "Because the images are smaller, a much wider region behind the vehicle can be seen in a small mirror.",
  ["Convex mirror: virtual, erect, diminished images", "Diminished images → wide field of view"],
  why="A convex mirror never forms a real image of a real object. Its images are diminished, not magnified. Image "
      "distance equal to object distance describes a plane mirror.",
  ncert=RO + "reflection of light by spherical mirrors", seconds=25)

q(OPT, "Huygens' principle and interference", "Basic", "statement_pair",
  sp("When light from two independent (incoherent) sources, each producing intensity I₀ at a point, superposes "
     "there, the resultant intensity is 2I₀.",
     "With two such incoherent sources, a stationary pattern of bright and dark fringes is seen on a screen, with "
     "the intensity varying between 0 and 4I₀."),
  SP, sp_key(True, False),
  "Coherent and incoherent addition of light waves",
  "For incoherent sources the phase difference changes rapidly and randomly, so cos φ averages to zero and the "
  "intensities simply add: I = 2I₀ (Statement I true). For the same reason no stationary fringes are formed; the "
  "screen is uniformly illuminated (Statement II false).",
  ["I = I₁ + I₂ + 2√(I₁I₂)⟨cos φ⟩, ⟨cos φ⟩ = 0 → 2I₀ → I true", "No stable φ → no stationary fringes → II false"],
  why="Statement II describes coherent sources; with incoherent sources the intensity is uniform at 2I₀.",
  ncert=WO + "coherent and incoherent addition of waves", seconds=40)

# ---- Intermediate
ratio_l = (1.5 - 1) / (1.5 / 1.75 - 1)
close(20 * ratio_l, -70)
q(OPT, "Refraction and lenses", "Intermediate", "numerical",
  "A thin biconvex lens made of glass of refractive index 1.5 has a focal length of 20 cm in air. It is completely "
  "immersed in a transparent liquid of refractive index 1.75. Its focal length in the liquid is:",
  *opt("−70 cm (it behaves as a diverging lens)", ["+70 cm (still converging)", "−20 cm (diverging)", "+80 cm"],
       "B"),
  "Lens maker's formula with relative refractive index: 1/f = (n_g/n_m − 1)(1/R₁ − 1/R₂)",
  "The curvature factor is the same in air and in the liquid, so the focal lengths are in the inverse ratio of "
  "(n_g/n_m − 1). In a liquid denser than the glass, this factor is negative and the lens diverges.",
  ["In air: n_g − 1 = 0.5", "In liquid: 1.5/1.75 − 1 = −1/7",
   "f_liq = f_air × 0.5/(−1/7) = 20 × (−3.5) = −70 cm"],
  why="+70 cm ignores the change of sign: the liquid is optically denser than the glass. −20 cm just reverses the "
      "sign. +80 cm is the value for water (n = 4/3), which is less dense than the glass.",
  ncert=RO + "refraction at spherical surfaces and by lenses (lens-maker's formula)", seconds=60, rc=True)

i_p = math.degrees(math.asin(math.sqrt(3) * math.sin(math.radians(30))))
close(i_p, 60)
close(2 * i_p - 60, 60)
q(OPT, "Prism", "Intermediate", "numerical",
  "A ray of light passes through an equilateral glass prism (refracting angle 60°) of refractive index √3 in the "
  "position of minimum deviation. The angle of incidence on the first face and the angle of minimum deviation are, "
  "respectively:",
  *opt("60° and 60°", ["30° and 60°", "60° and 30°", "45° and 30°"], "C"),
  "At minimum deviation r₁ = r₂ = A/2, i = e, and D_m = 2i − A",
  "At minimum deviation the ray passes symmetrically, so each refraction angle inside is A/2 = 30°. Snell's law at "
  "the first face then gives i.",
  ["r = A/2 = 30°", "sin i = √3 sin 30° = √3/2 → i = 60°", "D_m = 2i − A = 120° − 60° = 60°"],
  why="30° is the angle of refraction inside the prism, not the angle of incidence. D_m = 30° uses D_m = i − A/2. "
      "45° would need n = √2.",
  ncert=RO + "refraction through a prism", seconds=55, rc=True)

m_t = 150 / 5
close(m_t * 0.5, 15)
q(OPT, "Optical instruments", "Intermediate", "numerical",
  "An astronomical telescope has an objective of focal length 150 cm and an eyepiece of focal length 5.0 cm, and is "
  "used in normal adjustment. The Moon subtends an angle of 0.5° at the unaided eye. The angle subtended at the eye "
  "by the final image of the Moon is about:",
  *opt("15°", ["0.017°", "0.5°", "7.5°"], "A"),
  "Angular magnification of a telescope in normal adjustment: m = f_o/f_e = β/α",
  "Magnifying power is defined as the ratio of the angle subtended by the final image to the angle subtended by the "
  "object at the unaided eye; for small angles, β = mα.",
  ["m = 150/5.0 = 30", "β = 30 × 0.5° = 15°"],
  why="0.017° divides the angle by m instead of multiplying. 0.5° ignores the magnification. 7.5° halves the "
      "magnification.",
  ncert=RO + "optical instruments - telescope", seconds=45, rc=True)

y_sec = 1.5 * 600e-9 * 1.5 / 0.3e-3
close(y_sec, 4.5e-3)
close(600e-9 * 1.5 / 0.3e-3, 3.0e-3)
close(2 * 600e-9 * 1.5 / 0.3e-3, 6.0e-3)
q(OPT, "Diffraction", "Intermediate", "numerical",
  "Light of wavelength 600 nm falls normally on a single slit of width 0.30 mm, and the diffraction pattern is "
  "observed on a screen 1.5 m away. Using the approximate condition for the secondary maxima, θ ≈ (n + ½)λ/a, the "
  "distance of the first secondary maximum from the centre of the pattern is about:",
  *opt("4.5 mm", ["3.0 mm", "6.0 mm", "2.25 mm"], "D"),
  "Single-slit pattern: minima at θ = nλ/a, secondary maxima approximately at θ = (n + ½)λ/a",
  "The first secondary maximum lies roughly midway between the first and second minima, at θ ≈ 3λ/(2a). On the "
  "screen, y = Dθ.",
  ["θ₁ ≈ 1.5λ/a = 1.5 × 600 × 10⁻⁹/0.30 × 10⁻³ = 3.0 × 10⁻³ rad", "y = Dθ = 1.5 × 3.0 × 10⁻³ = 4.5 mm"],
  why="3.0 mm is the position of the first minimum (λ/a). 6.0 mm is that of the second minimum (2λ/a). 2.25 mm "
      "uses λ/(2a).",
  ncert=WO + "diffraction - the single slit", seconds=60, rc=True)

q(OPT, "Huygens' principle and interference", "Intermediate", "assertion_reason",
  ar("In Young's double-slit experiment, the bright fringes near the centre of the pattern are equally spaced.",
     "In the diffraction pattern of a single slit, all the secondary maxima have the same intensity as the central "
     "maximum."),
  AR, ar_key(True, False),
  "Fringe positions in Young's experiment; intensity distribution in single-slit diffraction",
  "For small angles the nth bright fringe is at x = nλD/d, so successive fringes are a constant β = λD/d apart (A "
  "true). In single-slit diffraction the central maximum is much the brightest and the secondary maxima become "
  "weaker with increasing order (R false).",
  ["x_n = nλD/d → equal spacing β → A true", "Secondary maxima much weaker than the central one → R false"],
  why="R is false, so the options treating R as true are wrong; A is true.",
  ncert=WO + "interference of light waves and Young's experiment; diffraction", seconds=40)

q(OPT, "Huygens' principle and interference", "Intermediate", "match_list",
  ml("In a Young's double-slit experiment (with the slit separation, screen distance and wavelength initially fixed) "
     "and in a single-slit diffraction experiment, one change is made at a time, as in List-I. Match each change "
     "with its effect in List-II.",
     ["Young's experiment: the wavelength is changed from 600 nm to 400 nm (fringe width)",
      "Young's experiment: the distance of the screen from the slits is doubled (fringe width)",
      "Single slit: the slit width is doubled (linear width of the central maximum)",
      "Young's experiment: the whole apparatus is immersed in water of refractive index 4/3 (fringe width)"],
     ["Becomes 3/4 of its value", "Becomes half", "Becomes double", "Becomes 2/3 of its value"]),
  *mlo("A-IV, B-III, C-II, D-I",
       ["A-I, B-III, C-II, D-IV", "A-IV, B-II, C-III, D-I", "A-IV, B-III, C-I, D-II"], "C"),
  "Fringe width β = λD/d; central maximum width 2λD/a; λ in a medium = λ/n",
  "β ∝ λ: 400/600 = 2/3. β ∝ D: doubled. Central maximum ∝ 1/a: halved. In water the wavelength becomes λ/n = 3λ/4, "
  "so β becomes 3/4.",
  ["A → 2/3 (IV)", "B → double (III)", "C → half (II)", "D → 3/4 (I)"],
  why="A-I/D-IV swaps the wavelength and immersion effects. B-II/C-III inverts both dependences. C-I/D-II gives the "
      "slit-width change the water effect.",
  ncert=WO + "interference of light waves and Young's experiment; diffraction", seconds=60)

q(OPT, "Mirrors", "Intermediate", "multi_statement",
  ms("Using the Cartesian sign convention for spherical mirrors (distances measured from the pole, positive in the "
     "direction of the incident light), which of the following statements are correct?",
     ["The focal length of a concave mirror is negative.",
      "The magnification of a real image formed by a spherical mirror is negative.",
      "The mirror equation 1/v + 1/u = 1/f applies to both concave and convex mirrors.",
      "For a real object, the image distance for a convex mirror is positive.",
      "A convex mirror can form a real image of a real object."]),
  *mso({"a": True, "b": True, "c": True, "d": True, "e": False}, "abcd", ["abc", "bcde", "acd"], "A"),
  "Sign convention for spherical mirrors",
  "Light is incident from the left, so distances in front of the mirror are negative: a concave mirror's focus is "
  "in front (a true), and a real image is in front and inverted, giving m = −v/u < 0 (b true). The mirror equation "
  "holds for both kinds with signs (c true). A convex mirror's virtual image is behind the mirror, so v > 0 (d "
  "true); it never forms a real image of a real object (e false).",
  ["(a) true", "(b) true", "(c) true", "(d) true", "(e) false"],
  why="Options containing (e) include a false statement; the others leave out at least one true statement.",
  ncert=RO + "sign convention; the mirror equation", seconds=60)

q(OPT, "Optical instruments", "Intermediate", "statement_pair",
  sp("For a compound microscope with given objective and tube length, using an eyepiece of shorter focal length "
     "increases the magnifying power.",
     "For an astronomical telescope in normal adjustment, using an eyepiece of longer focal length, the objective "
     "being unchanged, increases the magnifying power."),
  SP, sp_key(True, False),
  "Microscope m ≈ (L/f_o)(D/f_e); telescope m = f_o/f_e",
  "In both instruments the eyepiece magnification is inversely proportional to f_e. A shorter f_e increases the "
  "microscope's magnifying power (Statement I true), and a longer f_e reduces the telescope's magnifying power "
  "f_o/f_e (Statement II false).",
  ["Microscope: m ∝ 1/f_e → I true", "Telescope: m = f_o/f_e → larger f_e gives smaller m → II false"],
  why="Statement II reverses the dependence on the eyepiece focal length.",
  ncert=RO + "optical instruments", seconds=40)

# ---- Advanced
v1 = lens_v(20, -30)
assert math.isclose(v1, 60)
u_m = v1 - 40
v_m = -u_m
pos = 40 + v_m
u2 = -(40 - pos)
assert math.isclose(pos, 20) and math.isclose(u2, -20)
assert abs(1 / 20 + 1 / u2) < 1e-12
q(OPT, "Refraction and lenses", "Advanced", "numerical",
  "A thin convex lens of focal length 20 cm has a plane mirror placed 40 cm behind it, perpendicular to its "
  "principal axis. A point object is on the axis 30 cm in front of the lens. After refraction through the lens, "
  "reflection at the mirror and refraction through the lens again, the final image is formed:",
  *opt("at infinity: the light emerges from the lens as a parallel beam",
       ["20 cm in front of the lens", "at the object itself, 30 cm in front of the lens",
        "60 cm behind the lens"], "D"),
  "Successive image formation; a converging beam on a plane mirror acts as a virtual object",
  "The lens alone would form an image 60 cm behind it, i.e. 20 cm behind the mirror. The mirror reflects the "
  "converging rays so that they meet 20 cm in front of the mirror, which is 20 cm from the lens. This point is at "
  "the focus of the lens, so the returning light emerges parallel.",
  ["Lens: 1/v = 1/20 − 1/30 = 1/60 → v = 60 cm", "Virtual object 20 cm behind the mirror → image 20 cm in front",
   "That point is 40 − 20 = 20 cm from the lens = f → emergent beam parallel"],
  why="20 cm in front of the lens forgets the second refraction. Returning to the object would need the mirror at "
      "the lens's image point (60 cm). 60 cm behind the lens ignores the mirror.",
  ncert=RO + "refraction by a lens; reflection by mirrors", seconds=120, rc=True)

v_b = 1 / ((1 - 1.5) / -10 + 1.5 / -5)
close(v_b, -4.0)
close(5 / 1.5, 3.33, 2e-3)
close(1 / ((1 - 1.5) / 10 + 1.5 / -5), -2.86, 2e-3)
q(OPT, "Refraction and lenses", "Advanced", "numerical",
  "A small air bubble is inside a solid glass sphere of radius 10 cm and refractive index 1.5, at a distance of 5 cm "
  "from the surface along a radius (i.e. halfway between the surface and the centre). Viewed from outside along "
  "that radius, from the side nearer the bubble, the bubble appears to be below the surface at a depth of:",
  *opt("4.0 cm", ["3.3 cm", "2.9 cm", "5.0 cm"], "B"),
  "Refraction at a spherical surface: n₂/v − n₁/u = (n₂ − n₁)/R",
  "Light goes from glass (n₁ = 1.5) to air (n₂ = 1). Taking the direction of the emerging light as positive, the "
  "object (bubble) is at u = −5 cm and the centre of curvature is on the glass side, so R = −10 cm.",
  ["1/v − 1.5/(−5) = (1 − 1.5)/(−10)", "1/v + 0.30 = 0.05 → 1/v = −0.25 → v = −4.0 cm",
   "The image is 4.0 cm inside the glass from the surface"],
  why="3.3 cm uses the plane-surface formula (real depth/n). 2.9 cm takes R with the wrong sign. 5.0 cm ignores "
      "refraction.",
  ncert=RO + "refraction at spherical surfaces", seconds=100, rc=True)

lam2 = 600 / 1.5
close(lam2, 400)
q(OPT, "Diffraction", "Advanced", "numerical",
  "A single slit is illuminated normally by light containing two wavelengths. The first minimum of the diffraction "
  "pattern of the 600 nm light falls at the same angle as the first secondary maximum of the other wavelength. "
  "Taking the secondary maxima at sin θ ≈ (n + ½)λ/a, the other wavelength is:",
  *opt("400 nm", ["900 nm", "300 nm", "600 nm"], "A"),
  "Single slit: first minimum a sin θ = λ; first secondary maximum a sin θ ≈ 3λ/2",
  "Equating the two path-difference conditions at the same angle: λ₁ = (3/2)λ₂.",
  ["a sin θ = λ₁ = 1.5 λ₂", "λ₂ = 600/1.5 = 400 nm"],
  why="900 nm multiplies by 1.5 instead of dividing. 300 nm uses the second minimum condition (2λ₂). 600 nm assumes "
      "the minimum and maximum coincide for the same wavelength.",
  ncert=WO + "diffraction - the single slit", seconds=60, rc=True)

v_obj = mirror_v(-20, -30)
mm = -v_obj / -30
close(v_obj, -60)
close(mm ** 2 * 2, 8)
q(OPT, "Mirrors", "Advanced", "numerical",
  "A small object lies on the principal axis of a concave mirror of focal length 20 cm, 30 cm in front of it, and "
  "moves along the axis towards the mirror at 2 cm/s. At this instant the image moves:",
  *opt("at 8 cm/s, away from the mirror", ["at 8 cm/s, towards the mirror", "at 4 cm/s, away from the mirror",
                                           "at 2 cm/s, towards the mirror"], "C"),
  "Differentiating the mirror equation: dv/dt = −(v²/u²) du/dt = −m² du/dt",
  "From 1/v + 1/u = 1/f, −(1/v²)dv/dt − (1/u²)du/dt = 0. The image speed is m² times the object speed, in the "
  "opposite sense along the axis. As the object moves from 30 cm towards F, the real image moves out towards "
  "infinity, away from the mirror.",
  ["v = −60 cm, m = −2", "|dv/dt| = m² |du/dt| = 4 × 2 = 8 cm/s",
   "u → F makes |v| increase → image moves away from the mirror"],
  why="Towards the mirror reverses the direction (the image recedes as the object approaches F). 4 cm/s uses |m| "
      "instead of m². 2 cm/s assumes the image moves like the object.",
  seconds=90, rc=True)

q(OPT, "Total internal reflection", "Advanced", "assertion_reason",
  ar("A ray of light falling normally on one refracting face of an equilateral glass prism of refractive index 1.5 "
     "emerges from the second refracting face.",
     "For a ray falling normally on the first face of a prism, the angle of incidence at the second refracting face "
     "is equal to the angle of the prism."),
  AR, ar_key(False, True),
  "Geometry of a prism: r₁ + r₂ = A; total internal reflection when the angle of incidence exceeds the critical angle",
  "Normal incidence means r₁ = 0, so r₂ = A = 60° (R true). The critical angle for n = 1.5 is sin⁻¹(2/3) ≈ 42°. "
  "Since 60° > 42°, the ray is totally internally reflected at the second face and does not emerge from it "
  "(A false).",
  ["r₁ = 0 → r₂ = A = 60° → R true", "sin C = 1/1.5 → C ≈ 41.8°", "60° > C → total internal reflection → A false"],
  why="A is false because the ray is totally reflected at the second face; R is a correct geometrical result.",
  ncert=RO + "total internal reflection; refraction through a prism", seconds=60)

lens_cases = {"A": -10, "B": -30, "C": -40, "D": -60}
vals = {k: lens_v(20, u) for k, u in lens_cases.items()}
close(vals["A"], -20)
close(vals["B"], 60)
close(vals["C"], 40)
close(vals["D"], 30)
q(OPT, "Refraction and lenses", "Advanced", "match_list",
  ml("A real object is placed on the principal axis of a thin convex lens of focal length 20 cm, at the distance "
     "from the lens given in List-I. Match each case with the image in List-II.",
     ["10 cm", "30 cm", "40 cm", "60 cm"],
     ["Real, 30 cm from the lens on the other side", "Real, 40 cm from the lens on the other side",
      "Virtual, 20 cm from the lens on the same side as the object", "Real, 60 cm from the lens on the other side"]),
  *mlo("A-III, B-IV, C-II, D-I",
       ["A-III, B-I, C-II, D-IV", "A-IV, B-III, C-II, D-I", "A-III, B-IV, C-I, D-II"], "B"),
  "Thin lens formula 1/v − 1/u = 1/f",
  "With f = +20 cm: u = −10 → v = −20 cm (virtual); u = −30 → v = +60 cm; u = −40 → v = +40 cm (at 2f); "
  "u = −60 → v = +30 cm.",
  ["A: 1/v = 1/20 − 1/10 → v = −20 cm (III)", "B: 1/v = 1/20 − 1/30 → v = 60 cm (IV)",
   "C: 1/v = 1/20 − 1/40 → v = 40 cm (II)", "D: 1/v = 1/20 − 1/60 → v = 30 cm (I)"],
  why="A-III, B-I, D-IV swaps the images for 30 cm and 60 cm (object and image distances are interchangeable, but "
      "not equal). A-IV/B-III makes the object inside f give a real image. C-I/D-II swaps the 2f case with the 60 cm "
      "case.",
  ncert=RO + "thin lens formula", seconds=90)

q(OPT, "Refraction and lenses", "Advanced", "multi_statement",
  ms("Which of the following statements about thin lenses are correct?",
     ["A thin equiconvex lens of glass of refractive index 1.5 has a focal length equal to the radius of curvature "
      "of its surfaces.",
      "A thin plano-convex lens of glass of refractive index 1.5 has a focal length equal to twice the radius of "
      "curvature of its curved surface.",
      "If such an equiconvex lens is immersed in a liquid of refractive index 1.5, it neither converges nor "
      "diverges light.",
      "A thin concave lens can form a real image of a real object.",
      "A thin convex lens forms a virtual image of a real object placed between its focus and its optical centre."]),
  *mso({"a": True, "b": True, "c": True, "d": False, "e": True}, "abce", ["abc", "abde", "bce"], "D"),
  "Lens maker's formula; image formation by thin lenses",
  "Equiconvex: 1/f = 0.5 × 2/R → f = R (a true). Plano-convex: 1/f = 0.5/R → f = 2R (b true). In a liquid of the "
  "same index, n_rel − 1 = 0, so the power is zero (c true). A concave lens always forms a virtual image of a real "
  "object (d false). An object inside the focus of a convex lens gives a virtual, erect, magnified image (e true).",
  ["(a) f = R", "(b) f = 2R", "(c) power = 0", "(d) false", "(e) true"],
  why="Options with (d) include a false statement; the other two options each leave out a true statement.",
  ncert=RO + "refraction by a lens; lens maker's formula", seconds=75)


# ================================================================ Dual Nature (B3 I4 A3)
DC = NC + "'Dual Nature of Radiation and Matter', "

# ---- Basic
E_d1 = 6.6e-34 * 5e14
close(E_d1, 3.3e-19)
close(6.6e-34 / 5e14, 1.32e-48)
q(DUAL, "Photoelectric effect", "Basic", "numerical",
  "Taking Planck's constant h = 6.6 × 10⁻³⁴ J s, the energy of a photon of frequency 5.0 × 10¹⁴ Hz is:",
  *opt("3.3 × 10⁻¹⁹ J", ["1.3 × 10⁻⁴⁸ J", "3.3 × 10⁻²⁰ J", "2.1 × 10⁻¹⁹ J"], "B"),
  "Photon energy E = hν",
  "Each photon of radiation of frequency ν carries energy hν.",
  ["E = hν = 6.6 × 10⁻³⁴ × 5.0 × 10¹⁴ = 3.3 × 10⁻¹⁹ J (about 2.1 eV)"],
  why="1.3 × 10⁻⁴⁸ J divides h by ν. 3.3 × 10⁻²⁰ J slips a power of ten. 2.1 × 10⁻¹⁹ J writes the energy in eV "
      "(2.1 eV) with the wrong unit.",
  ncert=DC + "photoelectric effect - Einstein's photoelectric equation", seconds=25, rc=True)

K_d2 = 4.14e-15 * (1.5e15 - 1.0e15)
close(K_d2, 2.07)
close(4.14e-15 * 1.5e15, 6.21)
close(4.14e-15 * 2.5e15, 10.35)
q(DUAL, "Einstein's equation", "Basic", "numerical",
  "The threshold frequency for photoelectric emission from a metal is 1.0 × 10¹⁵ Hz. Light of frequency "
  "1.5 × 10¹⁵ Hz falls on it. Taking h = 4.14 × 10⁻¹⁵ eV s, the maximum kinetic energy of the emitted "
  "photoelectrons is about:",
  *opt("2.07 eV", ["6.21 eV", "4.14 eV", "10.35 eV"], "A"),
  "Einstein's photoelectric equation: K_max = h(ν − ν₀)",
  "The work function is hν₀; the rest of the photon energy appears as the maximum kinetic energy.",
  ["K_max = 4.14 × 10⁻¹⁵ × (1.5 − 1.0) × 10¹⁵ = 4.14 × 0.5 = 2.07 eV"],
  why="6.21 eV is the whole photon energy hν. 4.14 eV is the work function hν₀. 10.35 eV adds the two frequencies.",
  ncert=DC + "Einstein's photoelectric equation", seconds=30, rc=True)

q(DUAL, "Photoelectric effect", "Basic", "direct",
  "According to the values of work function listed in NCERT, which one of the following metals has the HIGHEST "
  "work function?",
  *opt("Platinum", ["Caesium", "Sodium", "Copper"], "D"),
  "Work function of metals",
  "NCERT's table lists caesium about 2.14 eV, sodium about 2.75 eV, copper about 4.65 eV and platinum about 5.65 eV; "
  "platinum has the largest value of these.",
  ["Cs ≈ 2.14 eV < Na ≈ 2.75 eV < Cu ≈ 4.65 eV < Pt ≈ 5.65 eV"],
  why="Caesium has the lowest work function of the common metals (it emits even with visible light). Sodium and "
      "copper lie between caesium and platinum.",
  ncert=DC + "electron emission (Table: work functions of some metals)", seconds=25)

# ---- Intermediate
phiA = 4.0 - 1.5
K_B = 6.0 - 2 * phiA
assert K_B == 1.0
assert 6.0 - phiA == 3.5 and 6.0 - 1.5 == 4.5
q(DUAL, "Einstein's equation", "Intermediate", "numerical",
  "Photons of energy 4.0 eV eject photoelectrons of maximum kinetic energy 1.5 eV from metal A. Metal B has a work "
  "function twice that of metal A. When photons of energy 6.0 eV fall on metal B, the maximum kinetic energy of "
  "the photoelectrons is:",
  *opt("1.0 eV", ["3.5 eV", "4.5 eV", "No photoelectrons are emitted"], "C"),
  "Einstein's equation K_max = hν − φ₀",
  "First find the work function of A from the given data, double it for B, and then apply the equation again.",
  ["φ_A = 4.0 − 1.5 = 2.5 eV", "φ_B = 2 × 2.5 = 5.0 eV", "K_max (B) = 6.0 − 5.0 = 1.0 eV"],
  why="3.5 eV uses the work function of A for metal B. 4.5 eV subtracts the kinetic energy from A instead of a work "
      "function. 6.0 eV exceeds 5.0 eV, so emission does occur.",
  ncert=DC + "Einstein's photoelectric equation", seconds=50, rc=True)

q(DUAL, "de Broglie wavelength", "Intermediate", "numerical",
  "A nucleus at rest breaks up into two fragments whose masses are in the ratio 1 : 2, the fragments flying apart "
  "with speeds much smaller than that of light. The ratio of the de Broglie wavelengths of the two fragments is:",
  *opt("1 : 1", ["2 : 1", "1 : 2", "√2 : 1"], "D"),
  "Conservation of momentum; de Broglie wavelength λ = h/p",
  "The total momentum is zero before the break-up, so the two fragments have equal and opposite momenta. Since "
  "λ = h/p depends only on the magnitude of the momentum, the wavelengths are equal.",
  ["p₁ + p₂ = 0 → |p₁| = |p₂|", "λ₁/λ₂ = p₂/p₁ = 1"],
  why="2 : 1 and 1 : 2 make λ depend on mass alone (as if the speeds were equal). √2 : 1 assumes equal kinetic "
      "energies.",
  ncert=DC + "wave nature of matter", seconds=45, rc=True)
m_f1, m_f2 = 1, 2
v_f1 = F(2)  # any speed; momentum conservation fixes v_f2
v_f2 = m_f1 * v_f1 / m_f2
assert (m_f2 * v_f2) / (m_f1 * v_f1) == 1  # λ1/λ2 = p2/p1
assert F(m_f1 * 1, m_f2 * 1) != 1 and math.sqrt(m_f2 / m_f1) != 1

q(DUAL, "Photoelectric effect", "Intermediate", "statement_pair",
  sp("The work function of a metal does not depend on the nature of its surface.",
     "Electrons can be emitted from a metal surface by heating it suitably (thermionic emission) or by applying a "
     "very strong electric field (field emission)."),
  SP, sp_key(False, True),
  "Work function and modes of electron emission",
  "NCERT states that the work function depends on the properties of the metal and the nature of its surface, so "
  "Statement I is false. Thermionic emission, field emission and photoelectric emission are the three ways listed "
  "by NCERT of supplying the minimum energy for electron emission (Statement II true).",
  ["Work function depends on the metal and its surface → I false",
   "Thermionic and field emission are valid modes → II true"],
  why="Statement I is false (surface condition matters); Statement II is true.",
  ncert=DC + "electron emission", seconds=35)

q(DUAL, "Photoelectric effect", "Intermediate", "assertion_reason",
  ar("For light of a frequency above the threshold frequency, photoelectric emission from a metal stops when the "
     "intensity of the light is reduced below a certain minimum value.",
     "Photoelectric emission does not occur if the frequency of the incident light is below the threshold frequency, "
     "however intense the light may be."),
  AR, ar_key(False, True),
  "Dependence of photoelectric emission on intensity and frequency",
  "Above the threshold, each photon can eject an electron, so even very dim light causes emission; lowering the "
  "intensity only reduces the number of electrons emitted per second (A false). Below the threshold, no photon has "
  "enough energy, so there is no emission at any intensity (R true).",
  ["Above threshold: emission at any intensity; photocurrent ∝ intensity → A false",
   "Below threshold: no emission at any intensity → R true"],
  why="A is false (there is no minimum intensity), while R is a correct NCERT observation.",
  ncert=DC + "experimental study of photoelectric effect", seconds=40)

# ---- Advanced
K_r = (3.0 - 2.2) * 1.6e-19
p_r = math.sqrt(2 * 9e-31 * K_r)
r_r = p_r / (1.6e-19 * 1e-4)
close(r_r, 0.030)
close(math.sqrt(9e-31 * K_r) / (1.6e-19 * 1e-4), 0.0212, 2e-3)
close(math.sqrt(2 * 9e-31 * 3.0 * 1.6e-19) / (1.6e-19 * 1e-4), 0.0581, 2e-3)
q(DUAL, "Einstein's equation", "Advanced", "numerical",
  "Photons of energy 3.0 eV fall on a metal of work function 2.2 eV. The fastest photoelectrons enter a uniform "
  "magnetic field of 1.0 × 10⁻⁴ T moving at right angles to it. Taking the electron mass as 9.0 × 10⁻³¹ kg and "
  "e = 1.6 × 10⁻¹⁹ C, the radius of their circular path is:",
  *opt("3.0 cm", ["2.1 cm", "5.8 cm", "1.5 cm"], "B"),
  "K_max = hν − φ₀; radius in a magnetic field r = p/(eB) = √(2mK)/(eB)",
  "The maximum kinetic energy is 0.8 eV. Converting to joules gives the momentum, and the radius follows from "
  "r = p/(eB).",
  ["K = 0.8 eV = 1.28 × 10⁻¹⁹ J", "p = √(2 × 9.0 × 10⁻³¹ × 1.28 × 10⁻¹⁹) = 4.8 × 10⁻²⁵ kg m/s",
   "r = 4.8 × 10⁻²⁵/(1.6 × 10⁻¹⁹ × 1.0 × 10⁻⁴) = 0.030 m = 3.0 cm"],
  why="2.1 cm uses p = √(mK), missing the factor 2. 5.8 cm takes the whole photon energy as kinetic energy. 1.5 cm "
      "halves the radius.",
  ncert=DC + "Einstein's photoelectric equation; " + MC + "motion in a magnetic field", seconds=100, rc=True)

K_c = (4.5 - 2.0) - 1.0
close(K_c, 1.5)
q(DUAL, "Einstein's equation", "Advanced", "numerical",
  "Photons of energy 4.5 eV fall on the emitter of a photocell, whose work function is 2.0 eV. The collector is kept "
  "at a potential of −1.0 V with respect to the emitter. The maximum kinetic energy with which photoelectrons reach "
  "the collector is:",
  *opt("1.5 eV", ["3.5 eV", "2.5 eV", "zero, since the collector is negative"], "A"),
  "Einstein's equation; work done against a retarding potential",
  "Electrons leave the emitter with at most 2.5 eV. Moving to a collector 1.0 V lower in potential, each electron "
  "loses 1.0 eV of kinetic energy. Since 1.0 V is less than the stopping potential (2.5 V), the fastest electrons "
  "still arrive.",
  ["K_max at emitter = 4.5 − 2.0 = 2.5 eV", "Loss in retarding field = e × 1.0 V = 1.0 eV",
   "K at collector = 2.5 − 1.0 = 1.5 eV"],
  why="3.5 eV adds the energy of the retarding field instead of subtracting it. 2.5 eV ignores the retarding "
      "potential. The current becomes zero only when the retarding potential reaches the stopping potential, 2.5 V.",
  ncert=DC + "effect of potential on photoelectric current", seconds=60, rc=True)

q(DUAL, "Photoelectric effect", "Advanced", "multi_statement",
  ms("According to the photon picture of electromagnetic radiation, which of the following statements are correct?",
     ["Photons are electrically neutral and are not deflected by electric or magnetic fields.",
      "A photon of frequency ν has energy hν and momentum of magnitude hν/c.",
      "Increasing the intensity of light of a given wavelength increases the number of photons crossing unit area "
      "per unit time, not the energy of each photon.",
      "The energy of each photon in a beam increases when the intensity of the beam is increased.",
      "All photons travel with the same speed c in vacuum, whatever their frequency."]),
  *mso({"a": True, "b": True, "c": True, "d": False, "e": True}, "abce", ["abc", "acde", "bce"], "B"),
  "Particle nature of light: the photon",
  "Photons carry no charge (a true). E = hν and p = hν/c (b true). Intensity is set by the photon flux; the energy "
  "per photon depends only on frequency (c true, d false). Every photon moves at c in vacuum (e true).",
  ["(a) true", "(b) true", "(c) true", "(d) false: photon energy depends on ν only", "(e) true"],
  why="Options containing (d) include a false statement; the remaining options each leave out a true statement.",
  ncert=DC + "particle nature of light: the photon", seconds=60)


# ================================================================ Atoms and Nuclei (B4 I5 A3)
AC_ = NC + "'Atoms', "
NU = NC + "'Nuclei', "

# ---- Basic
BE_O = 0.1374 * 931.5
close(BE_O, 128.0, 1e-3)
close(BE_O / 16, 8.0, 1e-3)
close(BE_O / 8, 16.0, 1e-3)
q(AN, "Binding energy", "Basic", "numerical",
  "The mass defect of the ¹⁶₈O nucleus is 0.1374 u. Taking 1 u = 931.5 MeV/c², the binding energy per nucleon of "
  "¹⁶O is about:",
  *opt("8.0 MeV", ["128 MeV", "16 MeV", "0.0086 MeV"], "C"),
  "B.E. = Δm c²; binding energy per nucleon = B.E./A",
  "The total binding energy is the energy equivalent of the mass defect; dividing by the number of nucleons "
  "(A = 16) gives the binding energy per nucleon.",
  ["B.E. = 0.1374 × 931.5 ≈ 128 MeV", "B.E./A = 128/16 = 8.0 MeV"],
  why="128 MeV is the total binding energy. 16 MeV divides by Z = 8 instead of A = 16. 0.0086 MeV divides the mass "
      "defect by A without converting to energy.",
  ncert=NU + "mass-energy and nuclear binding energy", seconds=35, rc=True)

Q_fus = 0.0287 * 931.5
close(Q_fus, 26.7, 2e-3)
q(AN, "Fission and fusion", "Basic", "numerical",
  "In the series of fusion reactions by which four hydrogen nuclei (with two electrons) are converted into one "
  "helium nucleus in the Sun, the total mass that disappears is about 0.0287 u. Taking 1 u = 931.5 MeV/c², the "
  "energy released is about:",
  *opt("26.7 MeV", ["0.0287 MeV", "6.7 MeV", "2.67 × 10³ MeV"], "D"),
  "Energy released in fusion Q = Δm c²",
  "The disappearing mass appears as energy at 931.5 MeV per u.",
  ["Q = 0.0287 × 931.5 ≈ 26.7 MeV"],
  why="0.0287 MeV forgets to convert u to MeV. 6.7 MeV is the energy per nucleon (26.7/4), not per reaction. "
      "2.67 × 10³ MeV slips two powers of ten.",
  ncert=NU + "nuclear fusion - energy generation in stars", seconds=30, rc=True)

q(AN, "Bohr model and hydrogen spectrum", "Basic", "direct",
  "de Broglie's explanation of Bohr's quantisation of angular momentum states that, for an electron in a stationary "
  "orbit of radius r_n,",
  *opt("the circumference of the orbit contains a whole number of de Broglie wavelengths: 2πr_n = nλ",
       ["the radius of the orbit equals a whole number of de Broglie wavelengths: r_n = nλ",
        "the circumference of the orbit equals half a de Broglie wavelength",
        "the de Broglie wavelength of the electron is the same in every orbit"], "B"),
  "Electron as a standing wave on its orbit",
  "A stationary orbit is one in which the electron wave forms a standing wave, so the circumference must be an "
  "integral number of wavelengths. With λ = h/(mv), 2πr_n = nh/(mv) gives mvr_n = nh/2π, Bohr's condition.",
  ["2πr_n = nλ, λ = h/(mv_n)", "mv_n r_n = nh/2π"],
  why="r_n = nλ would give mvr = nh, not nh/2π. Half a wavelength cannot form a standing wave round a closed loop. "
      "The speed, and hence λ, differs from orbit to orbit.",
  ncert=AC_ + "de Broglie's explanation of Bohr's second postulate of quantisation", seconds=30)

q(AN, "Bohr model and hydrogen spectrum", "Basic", "statement_pair",
  sp("The Bohr model can be applied to hydrogen-like ions such as He⁺ and Li²⁺, which have a single electron.",
     "The Bohr model explains the relative intensities of the lines in the hydrogen spectrum."),
  SP, sp_key(True, False),
  "Scope and limitations of the Bohr model",
  "The model treats a single electron moving round a nucleus of charge Ze, so it applies to hydrogen-like ions "
  "(Statement I true). NCERT lists among its limitations that it cannot explain the relative intensities of the "
  "spectral lines (Statement II false).",
  ["Single electron + nucleus Ze → applies to He⁺, Li²⁺ → I true",
   "Relative intensities not explained → II false"],
  why="Statement II states the opposite of a limitation listed in NCERT.",
  ncert=AC_ + "Bohr model of the hydrogen atom (limitations)", seconds=30)


# ---- Intermediate
E_split = 28.3 - 2 * 2.22
close(E_split, 23.86, 1e-3)
close(28.3 - 2.22, 26.08, 1e-3)
close(28.3 + 2 * 2.22, 32.74, 1e-3)
q(AN, "Binding energy", "Intermediate", "numerical",
  "The binding energy of the ⁴₂He nucleus is 28.3 MeV and that of the deuteron (²₁H) is 2.22 MeV. The minimum "
  "energy needed to split a ⁴He nucleus into two deuterons is about:",
  *opt("23.9 MeV", ["26.1 MeV", "32.7 MeV", "28.3 MeV"], "B"),
  "Energy balance with binding energies: energy needed = B.E.(initial) − Σ B.E.(products)",
  "Splitting ⁴He completely would need 28.3 MeV, but forming two deuterons gives back their binding energy, "
  "2 × 2.22 MeV.",
  ["Energy needed = 28.3 − 2 × 2.22", "= 28.3 − 4.44 ≈ 23.9 MeV"],
  why="26.1 MeV subtracts the binding energy of only one deuteron. 32.7 MeV adds the deuterons' binding energy "
      "instead of subtracting it. 28.3 MeV is the energy to separate ⁴He into four free nucleons.",
  ncert=NU + "mass-energy and nuclear binding energy", seconds=50, rc=True)

E_he = 13.6 * 4 * (1 - 1 / 4)
close(E_he, 40.8)
close(E_he - 13.6, 27.2)
q(AN, "Bohr model and hydrogen spectrum", "Intermediate", "numerical",
  "In the Bohr model the energy levels of a hydrogen-like ion are E_n = −13.6 Z²/n² eV. A photon emitted when a He⁺ "
  "ion (Z = 2) makes the transition n = 2 → n = 1 is absorbed by a hydrogen atom in its ground state. The kinetic "
  "energy of the electron ejected from the hydrogen atom is:",
  *opt("27.2 eV", ["40.8 eV", "54.4 eV", "No electron is ejected, since the photon has only 10.2 eV"], "D"),
  "Photon energy hν = E_i − E_f; ionisation of hydrogen needs 13.6 eV",
  "The He⁺ photon has energy 13.6 × 4 × (1 − ¼) = 40.8 eV, much more than the 13.6 eV needed to ionise ground-state "
  "hydrogen; the excess is the kinetic energy of the ejected electron.",
  ["E(He⁺, 2 → 1) = 54.4 × (1 − 1/4) = 40.8 eV", "K = 40.8 − 13.6 = 27.2 eV"],
  why="40.8 eV forgets the ionisation energy of hydrogen. 54.4 eV is the ionisation energy of He⁺. 10.2 eV is the "
      "2 → 1 photon of hydrogen, not of He⁺ (it misses the Z² factor).",
  ncert=AC_ + "Bohr model of the hydrogen atom; energy levels", seconds=60, rc=True)

lev = {n: -13.6 / n ** 2 for n in range(1, 6)}
close(lev[4] - lev[2], 2.55)
close(lev[3] - lev[2], 1.889, 1e-3)
close(lev[4] - lev[3], 0.661, 1e-3)
close(lev[2] - lev[1], 10.2)
q(AN, "Bohr model and hydrogen spectrum", "Intermediate", "numerical",
  "A hydrogen atom emits a photon of energy 2.55 eV. Using E_n = −13.6/n² eV, the transition responsible is:",
  *opt("n = 4 → n = 2", ["n = 3 → n = 2", "n = 4 → n = 3", "n = 2 → n = 1"], "B"),
  "Photon energy equals the difference of two energy levels",
  "The levels are −13.6, −3.40, −1.51, −0.85 eV for n = 1 to 4. Only the pair n = 4 and n = 2 differ by 2.55 eV.",
  ["E₄ − E₂ = −0.85 − (−3.40) = 2.55 eV", "Other pairs: 3 → 2 = 1.89 eV, 4 → 3 = 0.66 eV, 2 → 1 = 10.2 eV"],
  why="3 → 2 gives 1.89 eV (Hα). 4 → 3 gives 0.66 eV. 2 → 1 gives 10.2 eV.",
  ncert=AC_ + "the line spectra of the hydrogen atom", seconds=50, rc=True)

q(AN, "Bohr model and hydrogen spectrum", "Intermediate", "assertion_reason",
  ar("In the Bohr model, the electron in a hydrogen atom can revolve round the nucleus in a stable orbit of any "
     "radius.",
     "In the Bohr model, the angular momentum of the electron in a stationary orbit is an integral multiple of "
     "h/2π."),
  AR, ar_key(False, True),
  "Bohr's postulates: quantised angular momentum leads to discrete orbits r_n ∝ n²",
  "Bohr allowed only those orbits for which mvr = nh/2π (R true). This restricts the radii to the discrete values "
  "r_n = n²a₀, so orbits of arbitrary radius are not allowed (A false).",
  ["mvr = nh/2π → R true", "r_n = n² × 0.53 Å only → A false"],
  why="A contradicts the very quantisation stated in R; R is true.",
  ncert=AC_ + "Bohr model of the hydrogen atom", seconds=35)

q(AN, "Bohr model and hydrogen spectrum", "Intermediate", "match_list",
  ml("Using E_n = −13.6/n² eV for the hydrogen atom, match each transition in List-I with the energy of the photon "
     "emitted in List-II.",
     ["n = 2 → n = 1", "n = 3 → n = 2", "n = 3 → n = 1", "n = ∞ → n = 1 (series limit of the Lyman series)"],
     ["12.09 eV", "1.89 eV", "13.6 eV", "10.2 eV"]),
  *mlo("A-IV, B-II, C-I, D-III",
       ["A-I, B-II, C-IV, D-III", "A-IV, B-II, C-III, D-I", "A-IV, B-I, C-II, D-III"], "B"),
  "Photon energy hν = E_i − E_f",
  "E₁ = −13.6, E₂ = −3.40, E₃ = −1.51 eV. The differences give the photon energies.",
  ["A: −3.40 − (−13.6) = 10.2 eV (IV)", "B: −1.51 − (−3.40) = 1.89 eV (II)",
   "C: −1.51 − (−13.6) = 12.09 eV (I)", "D: 0 − (−13.6) = 13.6 eV (III)"],
  why="A-I/C-IV swaps the 2 → 1 and 3 → 1 lines. C-III/D-I swaps 3 → 1 with the series limit. B-I/C-II swaps the "
      "Balmer and Lyman lines from n = 3.",
  ncert=AC_ + "the line spectra of the hydrogen atom", seconds=60)

# ---- Advanced
P_th, E_f = 320e6, 200 * 1.6e-13
rate = P_th / E_f
close(rate, 1e19)
mass_hr = rate * 3600 * 235 / 6.0e23
close(mass_hr, 14.1, 1e-3)
close(rate * 60 * 235 / 6.0e23, 0.235)
close(rate * 86400 * 235 / 6.0e23, 338.4, 1e-3)
q(AN, "Fission and fusion", "Advanced", "numerical",
  "A nuclear reactor generates thermal power at the rate of 320 MW by the fission of ²³⁵U, each fission releasing "
  "200 MeV. Taking 1 MeV = 1.6 × 10⁻¹³ J and Avogadro's number as 6.0 × 10²³ mol⁻¹, the mass of ²³⁵U consumed in "
  "one hour is about:",
  *opt("14 g", ["0.24 g", "340 g", "1.4 g"], "A"),
  "Fission rate = power/energy per fission; mass = (number of nuclei/N_A) × molar mass",
  "First find the number of fissions per second, then the number in one hour, and convert that number of ²³⁵U "
  "nuclei to grams using 235 g per mole.",
  ["Energy per fission = 200 × 1.6 × 10⁻¹³ = 3.2 × 10⁻¹¹ J", "Fissions per second = 320 × 10⁶/3.2 × 10⁻¹¹ = 10¹⁹",
   "In one hour: 3.6 × 10²² nuclei", "Mass = (3.6 × 10²²/6.0 × 10²³) × 235 g ≈ 14 g"],
  why="0.24 g is the mass consumed in one minute. 340 g is the mass consumed in a day. 1.4 g slips a power of ten.",
  ncert=NU + "nuclear energy - fission", seconds=100, rc=True)

Z_ion = round(math.sqrt(122.4 / 13.6))
assert Z_ion == 3
close(0.53 / Z_ion, 0.1767, 1e-3)
close(0.53 / Z_ion ** 2, 0.0589, 1e-3)
q(AN, "Bohr model and hydrogen spectrum", "Advanced", "numerical",
  "A hydrogen-like ion in its ground state has an ionisation energy of 122.4 eV. In the Bohr model, the energy "
  "levels are E_n = −13.6 Z²/n² eV and the orbit radii are r_n = (0.53 Å) n²/Z. The radius of the ground-state "
  "orbit of this ion is about:",
  *opt("0.18 Å", ["0.059 Å", "1.59 Å", "0.53 Å"], "C"),
  "Hydrogen-like ions: E ∝ Z², r ∝ 1/Z",
  "The ionisation energy from the ground state is 13.6 Z² eV, which gives Z. The radius then scales as 1/Z.",
  ["13.6 Z² = 122.4 → Z² = 9 → Z = 3 (Li²⁺)", "r₁ = 0.53/3 ≈ 0.18 Å"],
  why="0.059 Å divides by Z² instead of Z. 1.59 Å multiplies by Z. 0.53 Å is the hydrogen value, ignoring Z.",
  ncert=AC_ + "Bohr model of the hydrogen atom", seconds=60, rc=True)

r3, E3 = 0.53 * 9, -13.6 / 9
close(r3, 4.77)
close(E3, -1.511, 1e-3)
lines = {(a, b) for a in range(1, 4) for b in range(1, 4) if a > b}
assert len(lines) == 3
q(AN, "Bohr model and hydrogen spectrum", "Advanced", "multi_statement",
  ms("A hydrogen atom is in the state n = 3 of the Bohr model (E_n = −13.6/n² eV, r_n = 0.53 n² Å). Which of the "
     "following statements are correct?",
     ["Its total energy is about −1.51 eV.",
      "The radius of the electron's orbit is about 4.77 Å.",
      "In returning to the ground state, possibly in steps, it can emit photons of three different wavelengths.",
      "The longest wavelength it can emit belongs to the Balmer series.",
      "The angular momentum of the electron is h/π."]),
  *mso({"a": True, "b": True, "c": True, "d": True, "e": False}, "abcd", ["abc", "abde", "bcd"], "D"),
  "Energy, radius and angular momentum in the Bohr model; possible transitions",
  "E₃ = −13.6/9 ≈ −1.51 eV (a true). r₃ = 9 × 0.53 ≈ 4.77 Å (b true). Possible downward transitions: 3 → 1, 3 → 2 "
  "and 2 → 1, i.e. three wavelengths (c true). The smallest energy jump, 3 → 2 (1.89 eV), gives the longest "
  "wavelength and ends on n = 2, a Balmer line (d true). L = 3h/2π, not h/π (e false).",
  ["(a) true", "(b) true", "(c) true: 3 lines", "(d) true: 3 → 2 is Hα", "(e) false: L = 3h/2π"],
  why="Options containing (e) include a false statement; the others leave out at least one true statement.",
  ncert=AC_ + "Bohr model of the hydrogen atom; the line spectra of the hydrogen atom", seconds=80)


# ================================================================ Electronic Devices (B4 I6 A4)
SD = NC + "'Semiconductor Electronics: Materials, Devices and Simple Circuits', "

# ---- Basic
ni = math.sqrt(4e22 * 1e10)
close(ni, 2e16)
q(ED, "Semiconductors", "Basic", "numerical",
  "In a doped silicon sample at thermal equilibrium, the electron concentration is 4 × 10²² m⁻³ and the hole "
  "concentration is 1 × 10¹⁰ m⁻³. The intrinsic carrier concentration of silicon at this temperature is:",
  *opt("2 × 10¹⁶ m⁻³", ["4 × 10³² m⁻³", "4 × 10¹² m⁻³", "2 × 10³² m⁻³"], "B"),
  "Mass-action law: n_e n_h = n_i²",
  "In thermal equilibrium the product of the electron and hole concentrations equals the square of the intrinsic "
  "concentration, whatever the doping.",
  ["n_i² = 4 × 10²² × 1 × 10¹⁰ = 4 × 10³²", "n_i = 2 × 10¹⁶ m⁻³"],
  why="4 × 10³² m⁻³ is n_i², not n_i. 4 × 10¹² m⁻³ is the ratio n_e/n_h. 2 × 10³² m⁻³ halves the product instead of "
      "taking its square root.",
  ncert=SD + "extrinsic semiconductor", seconds=35, rc=True)

close(8.0 * 25e-3, 0.2)
q(ED, "Zener diode", "Basic", "numerical",
  "A Zener diode of breakdown voltage 8.0 V is operating in its breakdown region and carries a current of 25 mA. "
  "The power dissipated in the Zener diode is:",
  *opt("0.20 W", ["200 W", "0.32 W", "2.0 W"], "C"),
  "Power P = VI",
  "In breakdown, the voltage across the Zener is its breakdown voltage, so the power is V_Z I_Z.",
  ["P = 8.0 × 25 × 10⁻³ = 0.20 W"],
  why="200 W leaves the current in mA. 0.32 W divides V² by an assumed 200 Ω, which has no basis here. 2.0 W slips a "
      "power of ten.",
  ncert=SD + "Zener diode", seconds=25, rc=True)

q(ED, "Semiconductors", "Basic", "direct",
  "Silicon is doped with phosphorus (a pentavalent impurity). After each phosphorus atom has donated its fifth "
  "electron to the conduction band, the phosphorus atom in the crystal becomes:",
  *opt("an immobile positive ion",
       ["a mobile positive charge carrier, i.e. a hole", "an immobile negative ion", "a neutral atom that can move "
        "through the crystal"], "D"),
  "Donor impurities in n-type semiconductors",
  "Four of the five valence electrons of phosphorus form covalent bonds with neighbouring silicon atoms; the fifth "
  "is loosely bound and is easily freed. Having lost one electron, the donor atom is left as a positive ion, fixed in "
  "the crystal lattice.",
  ["Donor gives up its fifth electron", "Donor becomes a positive ion, bound in the lattice (immobile)"],
  why="A hole is a vacancy in a covalent bond, not an ionised donor. A negative ion forms from an acceptor (trivalent) "
      "impurity. The donor atom is part of the lattice and cannot move.",
  ncert=SD + "extrinsic semiconductor - n-type", seconds=30)

q(ED, "Semiconductors", "Basic", "match_list",
  ml("Match each term related to semiconductors in List-I with its description in List-II.",
     ["Doping", "Hole", "Depletion region", "Barrier potential"],
     ["The region near a p-n junction that has been emptied of mobile charge carriers",
      "A vacancy in a covalent bond, which behaves as a positive charge carrier",
      "The potential difference across a p-n junction that opposes further diffusion of majority carriers",
      "Adding a small, controlled amount of a suitable impurity to a pure semiconductor"]),
  *mlo("A-IV, B-II, C-I, D-III",
       ["A-II, B-IV, C-I, D-III", "A-IV, B-II, C-III, D-I", "A-IV, B-I, C-II, D-III"], "A"),
  "Basic terms of semiconductor physics",
  "Doping adds impurity atoms to change the conductivity. A hole is the vacancy left when an electron leaves a bond. "
  "Diffusion across a junction leaves a layer of fixed ions with no mobile carriers (depletion region), and the field "
  "of these ions sets up the barrier potential.",
  ["A → IV", "B → II", "C → I", "D → III"],
  why="A-II/B-IV swaps doping and hole. C-III/D-I swaps the depletion region and the barrier potential. B-I/C-II "
      "swaps the hole and the depletion region.",
  ncert=SD + "intrinsic and extrinsic semiconductors; p-n junction formation", seconds=40)

# ---- Intermediate
E_600 = 1240 / 600
close(E_600, 2.067, 1e-3)
gaps = {"1.8 eV": 1.8, "2.2 eV": 2.2, "2.5 eV": 2.5, "3.0 eV": 3.0}
assert [k for k, g in gaps.items() if g <= E_600] == ["1.8 eV"]
q(ED, "LED, photodiode and solar cell", "Intermediate", "numerical",
  "Four photodiodes are made of semiconductors with the band gaps listed below. Light of wavelength 600 nm falls on "
  "each. Taking hc = 1240 eV nm, the photodiode that will respond to this light is the one with a band gap of:",
  *opt("1.8 eV", ["2.2 eV", "2.5 eV", "3.0 eV"], "B"),
  "A photodiode responds only to photons with energy hν ≥ E_g",
  "Electron–hole pairs are generated only if each photon can lift an electron across the band gap.",
  ["Photon energy = 1240/600 ≈ 2.07 eV", "Only E_g = 1.8 eV is less than 2.07 eV"],
  why="Band gaps of 2.2 eV, 2.5 eV and 3.0 eV are all larger than the photon energy (2.07 eV), so no electron–hole "
      "pairs are produced in them.",
  ncert=SD + "optoelectronic junction devices - photodiode", seconds=40, rc=True)

I_loop = (9 - 3) / 2000
close(I_loop, 3e-3)
close((9 + 3) / 2000, 6e-3)
close(9 / 2000, 4.5e-3)
q(ED, "p-n junction diode and rectifier", "Intermediate", "numerical",
  "A 9 V battery and a 3 V battery (both ideal) are connected in a single series loop with a 2 kΩ resistor and an "
  "ideal junction diode. The batteries oppose each other (positive terminal of one joined to the positive terminal "
  "of the other), and the diode is connected so that it is forward biased by the net emf. The current in the loop "
  "is:",
  *opt("3 mA", ["6 mA", "4.5 mA", "zero"], "A"),
  "Ideal diode: zero resistance when forward biased; opposing emfs subtract",
  "The net emf is 9 − 3 = 6 V, in the direction of the 9 V battery. The diode conducts in that direction, so it acts "
  "as a plain wire and the 2 kΩ resistor alone limits the current.",
  ["Net emf = 9 − 3 = 6 V", "I = 6/2000 = 3 × 10⁻³ A = 3 mA"],
  why="6 mA adds the emfs, though they oppose each other. 4.5 mA ignores the 3 V battery. Zero would apply only if "
      "the diode were reverse biased by the net emf.",
  ncert=SD + "p-n junction diode under forward bias", seconds=50, rc=True)

q(ED, "Semiconductors", "Intermediate", "assertion_reason",
  ar("There are practically no mobile charge carriers in the depletion region of an unbiased p-n junction.",
     "The energy band gap of germanium is smaller than that of silicon."),
  AR, ar_key(True, True, False),
  "Depletion region; band gaps of Si and Ge",
  "Electrons and holes diffusing across the junction recombine, leaving behind only fixed donor and acceptor ions "
  "near the junction (A true). The band gap of Ge (about 0.7 eV) is smaller than that of Si (about 1.1 eV), so R is "
  "true, but it says nothing about why the depletion region lacks mobile carriers.",
  ["Diffusion + recombination → only immobile ions near the junction → A true",
   "E_g(Ge) ≈ 0.7 eV < E_g(Si) ≈ 1.1 eV → R true", "R is unrelated to A"],
  why="R is a true but unrelated property of the two materials, so it is not the explanation of A.",
  ncert=SD + "p-n junction formation; classification of metals, conductors and semiconductors", seconds=40)

q(ED, "LED, photodiode and solar cell", "Intermediate", "statement_pair",
  sp("The reverse breakdown voltages of light emitting diodes are very low, typically around 5 V.",
     "The light emitted by an LED is thermal radiation from its junction, which is heated by the current."),
  SP, sp_key(True, False),
  "Light emitting diode",
  "NCERT notes that LEDs have very low reverse breakdown voltages, typically about 5 V, so care is needed to avoid "
  "reverse voltages (Statement I true). The light comes from the recombination of electrons and holes near the "
  "junction under forward bias, the energy being released as photons; it is not thermal radiation (Statement II "
  "false).",
  ["LED reverse breakdown ≈ 5 V → I true", "Emission from electron–hole recombination → II false"],
  why="Statement II confuses an LED with an incandescent lamp.",
  ncert=SD + "optoelectronic junction devices - light emitting diode", seconds=35)

q(ED, "Logic gates", "Intermediate", "match_list",
  ml("Match each combination of logic gates in List-I with the single gate it is equivalent to in List-II.",
     ["A two-input NAND gate with both its inputs joined together",
      "Each of the inputs A and B passed through a NOT gate, and the two outputs fed to a NAND gate",
      "An OR gate followed by a NOT gate",
      "Each of the inputs A and B passed through a NOT gate, and the two outputs fed to a NOR gate"],
     ["OR", "AND", "NOT", "NOR"]),
  *mlo("A-III, B-I, C-IV, D-II",
       ["A-III, B-II, C-IV, D-I", "A-IV, B-I, C-III, D-II", "A-III, B-I, C-II, D-IV"], "D"),
  "Truth tables of NOT, NAND, NOR; inverting the inputs",
  "NAND with joined inputs gives NOT(A·A) = Ā. NAND of Ā and B̄ is NOT(Ā·B̄), which is 1 unless both A and B are 0, "
  "i.e. OR. OR followed by NOT is NOR. NOR of Ā and B̄ is 1 only when Ā = B̄ = 0, i.e. A = B = 1, which is AND.",
  ["A → NOT (III)", "B → OR (I)", "C → NOR (IV)", "D → AND (II)"],
  why="B-II/D-I swaps the inverted-input NAND and NOR. A-IV/C-III swaps the joined-input NAND and OR + NOT. "
      "C-II/D-IV gives OR + NOT the output of AND.",
  ncert="Logic gates (NMC syllabus: OR, AND, NOT, NAND and NOR)", seconds=60)

q(ED, "Zener diode", "Intermediate", "multi_statement",
  ms("Which of the following statements about the Zener diode are correct?",
     ["Under forward bias, a Zener diode behaves like an ordinary junction diode.",
      "Zener breakdown occurs because the very high electric field across the thin depletion layer pulls valence "
      "electrons out of the host atoms.",
      "In the breakdown region, the voltage across a Zener diode stays almost constant over a wide range of current.",
      "A Zener diode used as a voltage regulator is connected in forward bias.",
      "A Zener diode has lightly doped p- and n-regions."]),
  *mso({"a": True, "b": True, "c": True, "d": False, "e": False}, "abc", ["ac", "abcd", "bce"], "B"),
  "Zener diode: heavy doping, thin depletion layer, field-induced breakdown",
  "In forward bias the Zener conducts like any p-n diode (a true). Heavy doping gives a very thin depletion layer, so "
  "a few volts of reverse bias produce a field of about 5 × 10⁶ V/m, which pulls valence electrons free (b true). In "
  "breakdown the voltage is nearly constant while the current changes greatly (c true). As a regulator it is "
  "reverse biased (d false). Both sides are heavily, not lightly, doped (e false).",
  ["(a) true", "(b) true", "(c) true", "(d) false: reverse biased", "(e) false: heavily doped"],
  why="(a) and (c) only misses the true statement (b); options with (d) or (e) contain a false statement.",
  ncert="Zener diode (NMC syllabus: I-V characteristics and voltage regulator)", seconds=60)

# ---- Advanced
Is_z = (12 - 6) / 300
RLmin = 6 / Is_z
close(RLmin, 300)
close(12 / Is_z, 600)
close(6 / (12 / 300), 150)
q(ED, "Zener diode", "Advanced", "numerical",
  "A Zener diode of breakdown voltage 6.0 V is connected through a 300 Ω series resistor to a 12 V DC supply, and a "
  "load resistor R_L is connected across the Zener diode. Treating the Zener as drawing current only when the "
  "voltage across it would otherwise exceed 6.0 V, the smallest value of R_L for which the load voltage remains "
  "6.0 V is:",
  *opt("300 Ω", ["600 Ω", "150 Ω", "There is no lower limit; any load gives 6.0 V"], "C"),
  "Zener regulator: I_series = (V_in − V_Z)/R_s is shared by the Zener and the load",
  "While the Zener regulates, the series resistor has 12 − 6 = 6 V across it, so it carries 20 mA. The load can take "
  "at most all of this current (Zener current falling to zero), which fixes the smallest load resistance.",
  ["I_s = (12 − 6)/300 = 20 mA", "I_L ≤ 20 mA → R_L ≥ 6.0/0.020 = 300 Ω"],
  why="600 Ω divides the supply voltage, not the load voltage, by 20 mA. 150 Ω uses the supply voltage across the "
      "series resistor (40 mA). A very small load would draw so much current that the Zener leaves breakdown.",
  ncert="Zener diode as a voltage regulator (NMC syllabus)", seconds=80, rc=True)

K_p = 0.6 - (0.7 - 0.3)
close(K_p, 0.2)
q(ED, "p-n junction diode and rectifier", "Advanced", "numerical",
  "The barrier potential of an unbiased p-n junction is 0.70 V. The junction is now forward biased by 0.30 V. An "
  "electron in the n-region approaches the junction with a kinetic energy of 0.60 eV. Treating the effective barrier "
  "as the only obstacle, the kinetic energy with which it enters the p-region is:",
  *opt("0.20 eV", ["It cannot cross the junction", "0.90 eV", "0.60 eV"], "A"),
  "Forward bias lowers the barrier height to V₀ − V",
  "Forward bias opposes the built-in potential, so the effective barrier is 0.70 − 0.30 = 0.40 V. The electron "
  "loses 0.40 eV in climbing it.",
  ["Effective barrier = 0.70 − 0.30 = 0.40 V", "K = 0.60 − 0.40 = 0.20 eV"],
  why="'Cannot cross' uses the unbiased barrier of 0.70 V. 0.90 eV adds the bias voltage to the kinetic energy. "
      "0.60 eV ignores the barrier altogether.",
  ncert=SD + "semiconductor diode - p-n junction diode under forward bias", seconds=70, rc=True)

q(ED, "Semiconductors", "Advanced", "assertion_reason",
  ar("At room temperature, doping pure silicon with a donor impurity at a concentration of only one part per million "
     "increases its conductivity enormously.",
     "Each donor atom provides a free electron, and the donor concentration (about 10²² m⁻³) is millions of times "
     "larger than the intrinsic carrier concentration of silicon (about 10¹⁶ m⁻³)."),
  AR, ar_key(True, True, True),
  "Extrinsic semiconductors: carrier concentration set by doping",
  "Silicon has about 5 × 10²⁸ atoms per m³, so 1 ppm of donors gives about 5 × 10²² free electrons per m³, compared "
  "with an intrinsic concentration of about 1.5 × 10¹⁶ m⁻³. The number of carriers, and hence the conductivity, rises "
  "by a factor of about a million. R gives exactly this reason.",
  ["Donors: 5 × 10²⁸ × 10⁻⁶ = 5 × 10²² m⁻³", "n_i ≈ 1.5 × 10¹⁶ m⁻³", "Carrier number ↑ ~10⁶ times → conductivity ↑"],
  why="Both statements are true, and the huge increase in the number of free carriers is the reason for the rise in "
      "conductivity.",
  ncert=SD + "extrinsic semiconductor", seconds=50)

xnor = {(a, b): int((a & b) | (1 - (a | b))) for a in (0, 1) for b in (0, 1)}
assert xnor == {(0, 0): 1, (0, 1): 0, (1, 0): 0, (1, 1): 1}
orr = {(a, b): a | b for a in (0, 1) for b in (0, 1)}
assert orr != xnor
q(ED, "Logic gates", "Advanced", "multi_statement",
  ms("Inputs A and B are fed both to an AND gate and to a NOR gate, and the outputs of these two gates are fed to an "
     "OR gate, whose output is Y. Which of the following statements are correct?",
     ["Y = 1 when A = 0 and B = 0.", "Y = 0 when A = 0 and B = 1.", "Y = 1 when A = 1 and B = 1.",
      "Y = 1 when A = 1 and B = 0.",
      "The circuit is equivalent to a NOR gate followed by a NOT gate."]),
  *mso({"a": True, "b": True, "c": True, "d": False, "e": False}, "abc", ["ac", "abce", "bcd"], "D"),
  "Truth tables of AND, NOR and OR",
  "AND gives 1 only for (1, 1); NOR gives 1 only for (0, 0). Their OR is therefore 1 for (0, 0) and (1, 1) and 0 for "
  "(0, 1) and (1, 0): Y = 1 when the inputs are equal. A NOR followed by a NOT is an OR gate (0, 1, 1, 1), which is "
  "different.",
  ["AND: 0, 0, 0, 1; NOR: 1, 0, 0, 0 for (0,0), (0,1), (1,0), (1,1)", "Y = OR of these = 1, 0, 0, 1",
   "(a), (b), (c) true; (d) false; (e) false (NOR + NOT = OR: 0, 1, 1, 1)"],
  why="(a) and (c) only misses (b); options with (d) or (e) contain a false statement.",
  ncert="Logic gates (NMC syllabus: OR, AND, NOT, NAND and NOR)", seconds=80)


# ================================================================ Experimental Skills (B2 I3 A2)
LAB = "NMC syllabus, Experimental Skills: "

# ---- Basic
v_res = 4 * 480 * 0.175
close(v_res, 336)
close(2 * 480 * 0.175, 168)
q(EXP, "Mechanics experiments", "Basic", "numerical",
  "In a resonance-tube experiment with a tuning fork of frequency 480 Hz, the first resonance is obtained when the "
  "air column is 17.5 cm long. Neglecting the end correction, the speed of sound in air is:",
  *opt("336 m/s", ["168 m/s", "84 m/s", "672 m/s"], "B"),
  "First resonance of a tube closed at one end: l = λ/4",
  "At the first resonance the air column holds a quarter wavelength (node at the water surface, antinode at the open "
  "end), so λ = 4l and v = fλ.",
  ["λ = 4 × 0.175 = 0.70 m", "v = 480 × 0.70 = 336 m/s"],
  why="168 m/s uses λ = 2l (an open pipe). 84 m/s uses λ = l. 672 m/s uses λ = 8l.",
  ncert=LAB + "speed of sound in air at room temperature using a resonance tube", seconds=35, rc=True)

q(EXP, "Vernier calipers and screw gauge", "Basic", "statement_pair",
  sp("When the jaws of a vernier calipers are closed, if the zero of the vernier scale lies to the left of the zero "
     "of the main scale, the instrument has a negative zero error.",
     "The zero correction is equal in magnitude and opposite in sign to the zero error."),
  SP, sp_key(True, True),
  "Zero error and zero correction",
  "With the zero of the vernier to the left of the main-scale zero, every reading is too small, so the zero error is "
  "negative (Statement I true). The correction to be added is the zero error with its sign reversed: corrected "
  "reading = observed reading − zero error (Statement II true).",
  ["Vernier zero left of main zero → readings too small → negative zero error → I true",
   "Zero correction = −(zero error) → II true"],
  why="Both statements are correct, so the options calling either one false are wrong.",
  ncert=LAB + "vernier calipers", seconds=35)

# ---- Intermediate
LC_sg = F(1, 100)
zero_err = -3 * LC_sg
obs = 2 + 45 * LC_sg
corr = obs - zero_err
assert corr == F(248, 100)
assert obs + zero_err == F(242, 100)
q(EXP, "Vernier calipers and screw gauge", "Intermediate", "numerical",
  "A screw gauge has a pitch of 1 mm and 100 divisions on its circular scale. With the studs in contact, the zero of "
  "the circular scale is 3 divisions above the reference line (a negative zero error). When a metal sheet is placed "
  "between the studs, the main-scale reading is 2 mm and the 45th circular division is on the reference line. The "
  "corrected thickness of the sheet is:",
  *opt("2.48 mm", ["2.42 mm", "2.45 mm", "2.75 mm"], "C"),
  "Least count = pitch/number of divisions; corrected reading = observed reading − zero error",
  "The least count is 0.01 mm. A circular-scale zero above the reference line means the reading is short of zero by "
  "3 divisions: zero error = −0.03 mm. Subtracting a negative zero error adds 0.03 mm.",
  ["LC = 1 mm/100 = 0.01 mm", "Observed = 2 + 45 × 0.01 = 2.45 mm", "Zero error = −0.03 mm",
   "Corrected = 2.45 − (−0.03) = 2.48 mm"],
  why="2.42 mm subtracts 0.03 mm, treating the error as positive. 2.45 mm ignores the zero error. 2.75 mm adds 30 "
      "divisions instead of 3.",
  ncert=LAB + "screw gauge (thickness of a sheet)", seconds=60, rc=True)

R1, R2, R3 = 2.215, 2.715, 3.715
n_tm = (R3 - R1) / (R3 - R2)
close(n_tm, 1.5)
close((R2 - R1) / (R3 - R2), 0.5)
close((R3 - R1) / (R2 - R1), 3.0)
q(EXP, "Optics experiments", "Intermediate", "numerical",
  "To find the refractive index of a glass slab with a travelling microscope, the microscope is focused in turn on: "
  "(i) a mark on the table, reading 2.215 cm; (ii) the same mark seen through the slab placed over it, reading "
  "2.715 cm; (iii) chalk dust sprinkled on the top surface of the slab, reading 3.715 cm. The refractive index of "
  "the glass is:",
  *opt("1.50", ["0.50", "3.00", "1.33"], "B"),
  "n = real thickness/apparent thickness",
  "The real thickness is the distance from the mark to the top surface, R₃ − R₁. The apparent thickness is from the "
  "raised image of the mark to the top surface, R₃ − R₂.",
  ["Real thickness = 3.715 − 2.215 = 1.500 cm", "Apparent thickness = 3.715 − 2.715 = 1.000 cm",
   "n = 1.500/1.000 = 1.50"],
  why="0.50 is the normal shift divided by the apparent thickness. 3.00 divides the real thickness by the normal "
      "shift (R₂ − R₁). 1.33 is the refractive index of water, not obtained from these readings.",
  ncert=LAB + "refractive index of a glass slab using a travelling microscope", seconds=60, rc=True)

q(EXP, "Mechanics experiments", "Intermediate", "match_list",
  ml("Match each experiment in List-I with a precaution that NCERT-based laboratory practice requires for it "
     "(List-II).",
     ["Simple pendulum", "Coefficient of viscosity by terminal velocity",
      "Surface tension by capillary rise", "Young's modulus by Searle's apparatus"],
     ["Remove kinks from the wire by first hanging a dead load on it",
      "Start timing the ball only after it has fallen some distance through the liquid",
      "Keep the angular amplitude of the oscillations small",
      "Clean the capillary tube thoroughly and hold it vertical"]),
  *mlo("A-III, B-II, C-IV, D-I",
       ["A-II, B-III, C-IV, D-I", "A-III, B-II, C-I, D-IV", "A-III, B-IV, C-II, D-I"], "C"),
  "Precautions in laboratory experiments",
  "The pendulum formula assumes small oscillations. Stokes' law with v constant applies only after the ball reaches "
  "terminal velocity. Grease or tilt spoils the capillary rise. A dead load straightens the wire before extensions "
  "are measured.",
  ["A → III", "B → II", "C → IV", "D → I"],
  why="A-II/B-III swaps the pendulum and viscosity precautions. C-I/D-IV swaps the capillary and Searle's "
      "precautions. B-IV/C-II swaps the viscosity and capillary precautions.",
  ncert=LAB + "simple pendulum; viscosity; surface tension; Young's modulus", seconds=45)

# ---- Advanced
W = F(50 * (60 - 36), 36 - 20) - 50
assert W == 25
assert F(50 * 24, 16) == 75
q(EXP, "Thermal and fluid experiments", "Advanced", "numerical",
  "A calorimeter contains 50 g of water at 20 °C. Then 50 g of water at 60 °C is poured in, and after stirring the "
  "steady temperature is 36 °C. Neglecting heat losses to the surroundings, the water equivalent of the calorimeter "
  "(with its stirrer) is:",
  *opt("25 g", ["75 g", "50 g", "10 g"], "A"),
  "Principle of calorimetry: heat lost by hot water = heat gained by cold water + calorimeter",
  "The hot water cools by 24 °C. The cold water and the calorimeter (taken as W grams of water) both warm by 16 °C.",
  ["Heat lost = 50 × (60 − 36) = 1200 (in g °C, specific heat of water cancels)",
   "Heat gained = (50 + W) × (36 − 20) = 16(50 + W)", "16(50 + W) = 1200 → 50 + W = 75 → W = 25 g"],
  why="75 g is the total (water + calorimeter), not the calorimeter alone. 50 g assumes equal temperature changes "
      "for the cold side. 10 g has no basis in the heat balance.",
  ncert=LAB + "specific heat capacity by the method of mixtures", seconds=80, rc=True)

q(EXP, "Vernier calipers and screw gauge", "Advanced", "multi_statement",
  ms("Which of the following statements about vernier calipers and screw gauges are correct?",
     ["The least count of a vernier calipers equals one main-scale division minus one vernier-scale division.",
      "A positive zero error is subtracted from the observed reading to obtain the corrected reading.",
      "A screw gauge of pitch 1 mm with 100 divisions on its circular scale has a least count of 0.01 mm.",
      "If, with the studs of a screw gauge in contact, the zero of the circular scale lies below the reference line, "
      "the zero error is positive.",
      "For a vernier calipers with a negative zero error, the magnitude of the zero error is subtracted from the "
      "observed reading."]),
  *mso({"a": True, "b": True, "c": True, "d": True, "e": False}, "abcd", ["abc", "abde", "bcd"], "D"),
  "Least count and zero error of vernier calipers and screw gauge",
  "LC = 1 MSD − 1 VSD (a true). Corrected = observed − zero error, so a positive error is subtracted (b true). "
  "LC = pitch/divisions = 0.01 mm (c true). With the circular zero below the reference line, the screw reads a "
  "positive value when it should read zero (d true). With a negative zero error, subtracting a negative number "
  "means adding its magnitude (e false).",
  ["(a) true", "(b) true", "(c) true", "(d) true: positive zero error", "(e) false: the magnitude is added"],
  why="Options with (e) include a false statement; (a), (b) and (c) only and (b), (c) and (d) only each miss a true "
      "statement.",
  ncert=LAB + "vernier calipers; screw gauge", seconds=75)


# ================================================================ checks and output
def main():
    for i, x in enumerate(QS):
        x["question_id"] = f"NEET_PHY_{FIRST_ID + i:06d}"
    plan = json.loads(PLAN.read_text(encoding="utf-8"))
    subj = next(s for s in plan["subjects"] if any(p["package"] == PACKAGE for p in s["packages"]))
    pkg = next(p for p in subj["packages"] if p["package"] == PACKAGE)
    assert ROOT / pkg["output"] == OUT
    lo, hi = pkg["question_ids"]
    assert QS[0]["question_id"] == lo and QS[-1]["question_id"] == hi, (QS[0]["question_id"], QS[-1]["question_id"])
    quota = {(t["topic"], d): n for t in subj["topics"] if t["topic"] in pkg["topics"] for d, n in t["quota"].items()}
    subs = {t["topic"]: set(t["subtopics"]) for t in subj["topics"]}
    have = Counter((x["topic"], x["difficulty"]) for x in QS)
    assert have == Counter(quota), {k: (have.get(k), v) for k, v in quota.items() if have.get(k) != v}
    assert len(QS) == pkg["count"] == COUNT
    for x in QS:
        assert x["subtopic"] in subs[x["topic"]], (x["question_id"], x["subtopic"])
    order = [x["topic"] for x in QS]
    assert order == sorted(order, key=pkg["topics"].index)
    fmts = Counter(x["format"] for x in QS)
    assert 0.53 <= fmts["numerical"] / len(QS) <= 0.58, fmts
    for f_ in ("direct", "assertion_reason", "statement_pair", "match_list", "multi_statement"):
        assert fmts[f_] >= 0.08 * len(QS), (f_, fmts)
    keys = Counter(x["correct_answer"] for x in QS)
    assert all(29 <= keys[k] <= 33 for k in LETTERS), keys
    texts = [x["question_text"] for x in QS]
    assert len(set(texts)) == len(texts)
    doc = {"schema_version": "1.0", "batch_id": "BATCH_005", "created_at": TODAY,
           "notes": "Package PHY_005_p2: 123 original Physics questions (Current Electricity to Experimental Skills), "
                    "NEET_PHY_001128..001250. Numerical answers recomputed by tools/batch_005/PHY_005_p2.py.",
           "stimuli": [], "questions": QS}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {OUT}: {len(QS)} questions")
    print("difficulty", dict(Counter(x["difficulty"] for x in QS)))
    print("formats", dict(fmts))
    print("keys", dict(sorted(keys.items())))


if __name__ == "__main__":
    main()
