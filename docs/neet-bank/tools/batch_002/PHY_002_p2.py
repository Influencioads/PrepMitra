"""Builder for batches/parts/BATCH_002_PHY_p2.json (package PHY_002_p2 of BATCH_002).

Physics, 122 original questions, NEET_PHY_000379..NEET_PHY_000500: Current Electricity, Magnetic Effects of Current
and Magnetism, Electromagnetic Induction and Alternating Currents, Electromagnetic Waves, Optics, Dual Nature of
Matter and Radiation, Atoms and Nuclei, Electronic Devices, Experimental Skills.

Every numerical answer is recomputed below with an assert next to its question, and the plan quota, format mix and
answer-key balance are asserted before anything is written. If any assert fails, nothing is written.

    python tools/batch_002/PHY_002_p2.py        (run from docs/neet-bank)
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
PLAN = ROOT / "batches" / "plans" / "BATCH_002_plan.json"
OUT = ROOT / "batches" / "parts" / "BATCH_002_PHY_p2.json"
PACKAGE = "PHY_002_p2"
FIRST_ID = 379
COUNT = 122

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


def close(a, b, rel=1e-3):
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

# ================================================================ Current Electricity (B6 I7 A5)
rho, L_, A_ = 1.0e-6, 2.0, 0.5e-6
close(rho * L_ / A_, 4)
close(rho * L_ / 5e-6, 0.4)
close(rho / A_, 2)
close(rho * L_ / 0.5e-3, 4e-3)
q(CE, "Resistivity and temperature", "Basic", "numerical",
  "A wire of length 2 m and uniform cross-sectional area 0.5 mm² is made of an alloy of resistivity "
  "1.0 × 10⁻⁶ Ω m. Its resistance is:",
  *opt("4 Ω", ["0.4 Ω", "2 Ω", "4 × 10⁻³ Ω"], "A"),
  "Resistance from resistivity: R = ρL/A",
  "Resistance grows with length and falls with area; the material enters only through ρ.",
  ["A = 0.5 mm² = 0.5 × 10⁻⁶ m²", "R = ρL/A = (1.0 × 10⁻⁶ × 2)/(0.5 × 10⁻⁶) = 4 Ω"],
  why="0.4 Ω takes 0.5 mm² as 5 × 10⁻⁶ m². 2 Ω leaves out the length (ρ/A). 4 × 10⁻³ Ω converts mm² to m² with "
      "10⁻³ instead of 10⁻⁶.",
  ncert=NC + "'Current Electricity', resistivity of various materials", seconds=35, rc=True)

E_f, rho_cu = 0.034, 1.7e-8
close(E_f / rho_cu, 2.0e6)
close(rho_cu * E_f, 5.78e-10)
close(rho_cu / E_f, 5.0e-7)
close(E_f / 1.7e-6, 2.0e4)
q(CE, "Drift velocity and Ohm's law", "Basic", "numerical",
  "A uniform electric field of 0.034 V/m is maintained along a copper wire. The resistivity of copper is "
  "1.7 × 10⁻⁸ Ω m. The current density in the wire is:",
  *opt("2.0 × 10⁶ A/m²", ["5.8 × 10⁻¹⁰ A/m²", "5.0 × 10⁻⁷ A/m²", "2.0 × 10⁴ A/m²"], "B"),
  "Ohm's law in microscopic form: J = σE = E/ρ",
  "Current density is proportional to the local electric field; the constant of proportionality is the "
  "conductivity σ = 1/ρ.",
  ["J = E/ρ = 0.034/(1.7 × 10⁻⁸)", "= 2.0 × 10⁶ A/m²"],
  why="5.8 × 10⁻¹⁰ A/m² multiplies ρ and E. 5.0 × 10⁻⁷ A/m² divides ρ by E. 2.0 × 10⁴ A/m² uses "
      "1.7 × 10⁻⁶ (the value of ρ in Ω cm) as if it were in Ω m.",
  ncert=NC + "'Current Electricity', Ohm's law (J = σE)", seconds=35, rc=True)

P_par = 12 ** 2 / 6 + 12 ** 2 / 3
assert P_par == 72 and 12 ** 2 / 9 == 16 and 12 ** 2 / 6 == 24 and 12 ** 2 / 3 == 48
q(CE, "Combination of resistors", "Basic", "numerical",
  "A 6 Ω resistor and a 3 Ω resistor are connected in parallel across an ideal 12 V battery. The total power "
  "drawn from the battery is:",
  *opt("72 W", ["16 W", "24 W", "48 W"], "C"),
  "Power in a parallel combination: P = V²/R for each branch, and the branch powers add",
  "In parallel each resistor has the full 12 V across it, so each branch dissipates V²/R independently.",
  ["P(6 Ω) = 144/6 = 24 W, P(3 Ω) = 144/3 = 48 W", "Total = 72 W (equivalently V²/R_eq = 144/2)"],
  why="16 W treats the resistors as being in series (144/9). 24 W and 48 W count only one of the two branches.",
  ncert=NC + "'Current Electricity', electrical energy and power", seconds=35, rc=True)

q(CE, "Resistivity and temperature", "Basic", "direct",
  "A given metal wire is altered in each of the ways listed below, one at a time. Which change alters the "
  "resistivity of the wire?",
  *opt("Raising its temperature",
       ["Stretching it to twice its length at the same temperature",
        "Cutting it into two equal halves at the same temperature",
        "Passing a larger current through it while keeping its temperature fixed"], "D"),
  "Resistivity is a property of the material at a given temperature",
  "Resistance R = ρL/A depends on the shape of the wire, but resistivity ρ depends only on the material and its "
  "temperature. For a metal, ρ rises with temperature because the electrons collide more often.",
  ["Stretching or cutting changes L and A, so R changes, but ρ does not",
   "At fixed temperature ρ is independent of the current", "Raising the temperature changes ρ"],
  why="The first three options change the resistance (or nothing at all), not the resistivity of the metal.",
  ncert=NC + "'Current Electricity', temperature dependence of resistivity", seconds=25)

E_c, V_t, I_c = 1.5, 1.4, 2
close((E_c - V_t) / I_c, 0.05)
close(V_t / I_c, 0.7)
close(E_c / I_c, 0.75)
close((E_c - V_t) * I_c, 0.2)
q(CE, "Cells, emf and internal resistance", "Basic", "numerical",
  "The potential difference across the terminals of a cell is 1.5 V when no current is drawn from it, and falls "
  "to 1.4 V when it supplies a current of 2 A. The internal resistance of the cell is:",
  *opt("0.05 Ω", ["0.7 Ω", "0.75 Ω", "0.2 Ω"], "D"),
  "Terminal voltage of a discharging cell: V = ε − Ir",
  "The open-circuit terminal voltage equals the emf. The fall in terminal voltage when current flows is the drop "
  "across the internal resistance.",
  ["ε = 1.5 V (no current)", "Ir = ε − V = 1.5 − 1.4 = 0.1 V", "r = 0.1/2 = 0.05 Ω"],
  why="0.7 Ω is V/I, the external resistance. 0.75 Ω is ε/I, the total resistance of the circuit. 0.2 Ω multiplies "
      "the voltage drop by the current instead of dividing.",
  ncert=NC + "'Current Electricity', cells, emf, internal resistance", seconds=35, rc=True)

P_, Q_, R_b = 10, 20, 15
assert Q_ * R_b / P_ == 30 and P_ * R_b / Q_ == 7.5 and P_ + R_b == 25
close(P_ * Q_ / R_b, 13.33)
# the stated layout: two dividers across the same cell; null when the P-Q and R-S junctions are at equal potential
_S = Q_ * R_b / P_
assert abs(Q_ / (P_ + Q_) - _S / (R_b + _S)) < 1e-12
q(CE, "Wheatstone and metre bridge", "Basic", "numerical",
  "In a Wheatstone bridge, P = 10 Ω and Q = 20 Ω are in series in one branch, and R = 15 Ω and S are in series in "
  "the other branch. Both branches are connected across the same cell, with P and R joined at its positive "
  "terminal. The galvanometer is connected between the P–Q junction and the R–S junction. The value of S for "
  "which the galvanometer shows no deflection is:",
  *opt("30 Ω", ["7.5 Ω", "25 Ω", "13.3 Ω"], "B"),
  "Balance condition of a Wheatstone bridge: P/Q = R/S",
  "At balance no current flows through the galvanometer, so the ratios of resistances in the two arms on either "
  "side of it are equal.",
  ["P/Q = R/S → S = QR/P", "S = 20 × 15/10 = 30 Ω"],
  why="7.5 Ω uses P/Q = S/R. 25 Ω simply adds P and R. 13.3 Ω takes S = PQ/R.",
  ncert=NC + "'Current Electricity', Wheatstone bridge", seconds=30, rc=True)

VP = 12 - (12 / (4 + 2)) * 4
VQ = 12 - (12 / (3 + 6)) * 3
close(abs(VP - VQ), 4)
q(CE, "Kirchhoff's laws", "Intermediate", "numerical",
  "An ideal 12 V battery is connected across two branches in parallel. Branch 1 has a 4 Ω resistor followed by a "
  "2 Ω resistor; branch 2 has a 3 Ω resistor followed by a 6 Ω resistor. In each branch the first-named "
  "resistor is joined to the positive terminal. P is the junction of the 4 Ω and 2 Ω resistors and Q is the "
  "junction of the 3 Ω and 6 Ω resistors. The magnitude of the potential difference between P and Q is:",
  *opt("4 V", ["0 V", "8 V", "12 V"], "C"),
  "Potential along each branch of a circuit (Kirchhoff's loop rule)",
  "Each branch has the full 12 V across it. Find the potential of P and of Q above the negative terminal from the "
  "drops along each branch, then subtract.",
  ["Branch 1: I = 12/6 = 2 A; drop across 4 Ω = 8 V → V_P = 12 − 8 = 4 V",
   "Branch 2: I = 12/9 = 4/3 A; drop across 3 Ω = 4 V → V_Q = 12 − 4 = 8 V",
   "|V_P − V_Q| = 4 V (Q is at the higher potential)"],
  why="0 V assumes a balanced bridge, but 4/2 ≠ 3/6. 8 V is the potential of Q above the negative terminal, "
      "not the difference between P and Q. 12 V is the full battery voltage.",
  ncert=NC + "'Current Electricity', Kirchhoff's rules", seconds=75, rc=True)

R_A = F(1, 1 ** 2)
R_B = F(2, 2 ** 2)
assert (1 / R_A) / (1 / R_B) == F(1, 2)
q(CE, "Combination of resistors", "Intermediate", "numerical",
  "Wire X has length L and diameter d. Wire Y, made of the same material, has length 2L and diameter 2d. The two "
  "wires are connected in parallel across a battery. The ratio of the heat produced per second in X to that in Y "
  "is:",
  *opt("1 : 2", ["2 : 1", "1 : 1", "1 : 4"], "A"),
  "Resistance R = ρL/A with A ∝ d², and power in parallel P = V²/R",
  "First compare the resistances, then use the fact that both wires have the same voltage across them.",
  ["R ∝ L/d²: R_X ∝ L/d², R_Y ∝ 2L/(4d²) = (1/2)(L/d²) → R_X = 2R_Y",
   "In parallel, P = V²/R, so P_X/P_Y = R_Y/R_X = 1/2"],
  why="2 : 1 uses P = I²R as if the wires were in series. 1 : 1 assumes the doubled length cancels the doubled "
      "diameter (it does not, since area goes as d²). 1 : 4 ignores the doubled length of Y.",
  ncert=NC + "'Current Electricity', resistivity; electrical power", seconds=60, rc=True)

r_c = (F(9, 2) - 4) / (1 - F(1, 2))
E_c2 = 1 * (4 + r_c)
assert r_c == 1 and E_c2 == 5 and F(1, 2) * (9 + r_c) == E_c2
for e_, r_ in ((F(9, 2), F(1, 2)), (6, 2), (4, 0)):
    assert F(e_) / (4 + r_) == 1 and F(e_) / (9 + r_) != F(1, 2)
q(CE, "Cells, emf and internal resistance", "Intermediate", "numerical",
  "A cell sends a current of 1.0 A through an external resistance of 4 Ω, and a current of 0.5 A through an "
  "external resistance of 9 Ω. The emf and internal resistance of the cell are:",
  *opt("5 V and 1 Ω", ["4.5 V and 0.5 Ω", "6 V and 2 Ω", "4 V and 0 Ω"], "B"),
  "Circuit equation of a cell: ε = I(R + r)",
  "The emf and internal resistance are the same in both cases, so write ε = I(R + r) twice and solve the pair.",
  ["ε = 1.0 × (4 + r) and ε = 0.5 × (9 + r)", "4 + r = 4.5 + 0.5r → 0.5r = 0.5 → r = 1 Ω", "ε = 4 + 1 = 5 V"],
  shortcut="Check each option in both equations; only 5 V, 1 Ω gives 1.0 A with 4 Ω and 0.5 A with 9 Ω.",
  why="Each of the other pairs gives 1.0 A with 4 Ω but not 0.5 A with 9 Ω: 4.5/9.5 = 0.47 A, 6/11 = 0.55 A, "
      "4/9 = 0.44 A. They come from using only the first reading.",
  ncert=NC + "'Current Electricity', cells, emf, internal resistance", seconds=70, rc=True)

ratio0 = F(75, 25)
ratio1 = ratio0 / 2
l1 = 100 * ratio1 / (1 + ratio1)
assert ratio0 == 3 and l1 == 60
close(100 * 6 / 7, 85.71)
q(CE, "Wheatstone and metre bridge", "Intermediate", "numerical",
  "In a metre bridge, a resistance X is in the left gap and a standard resistance in the right gap; the null point "
  "is 75.0 cm from the left end. X is then shunted by connecting another resistor equal to X in parallel with it, "
  "the standard resistance being unchanged. The new null point is at a distance from the left end of:",
  *opt("60.0 cm", ["37.5 cm", "85.7 cm", "40.0 cm"], "D"),
  "Metre bridge balance: X/R = l/(100 − l)",
  "Find X/R from the first balance, halve X (two equal resistors in parallel), and find the new balance length.",
  ["First balance: X/R = 75/25 = 3", "After shunting: (X/2)/R = 1.5",
   "l/(100 − l) = 1.5 → l = 150 − 1.5l → l = 60.0 cm"],
  why="37.5 cm halves the balancing length instead of the resistance. 85.7 cm doubles the ratio (X/R = 6) instead "
      "of halving it. 40.0 cm is the correct balance measured from the right end.",
  ncert=NC + "'Current Electricity', Wheatstone bridge (metre bridge)", seconds=75, rc=True)

q(CE, "Kirchhoff's laws", "Intermediate", "assertion_reason",
  ar("Around any closed loop of a circuit, the algebraic sum of the changes in potential (across resistors and "
     "cells) is zero.",
     "The electrostatic force is conservative, so the net work it does on a charge taken once around a closed path "
     "and brought back to its starting point is zero."),
  AR, ar_key(True, True, True),
  "Kirchhoff's loop rule and its basis",
  "Potential is a single-valued function of position because the electrostatic field is conservative. A charge "
  "that goes round a loop and returns to its starting point is back at the same potential, so the changes in "
  "potential around the loop must add to zero. R is the reason for A.",
  ["A: Kirchhoff's loop rule → true", "R: zero work round a closed path for a conservative force → true",
   "Zero net work per unit charge = zero net change in potential → R explains A"],
  why="R is not a separate fact here; it is exactly why the loop rule holds, so option B is wrong. Both statements "
      "are true, so C and D are wrong.",
  ncert=NC + "'Current Electricity', Kirchhoff's rules", seconds=40)

q(CE, "Drift velocity and Ohm's law", "Intermediate", "statement_pair",
  sp("The mobility of conduction electrons, defined as the drift speed per unit electric field, equals eτ/m, where "
     "τ is the average time between collisions.",
     "In a metallic conductor at a fixed temperature, the drift speed of the electrons is directly proportional to "
     "the electric field in the conductor."),
  SP, sp_key(True, True),
  "Drift velocity, relaxation time and mobility",
  "An electron accelerated by eE/m for an average time τ acquires an average (drift) velocity v_d = eEτ/m. At a "
  "fixed temperature τ is fixed, so v_d ∝ E, and v_d/E = eτ/m is the mobility.",
  ["v_d = (eE/m)τ", "μ = v_d/E = eτ/m → Statement I true", "τ constant at fixed temperature → v_d ∝ E → Statement II true"],
  why="Both statements follow from v_d = eEτ/m, so any option calling either false is wrong.",
  ncert=NC + "'Current Electricity', drift of electrons and the origin of resistivity; mobility", seconds=40)

q(CE, "Combination of resistors", "Intermediate", "match_list",
  ml("Four identical resistors, each of resistance R, are connected in the ways described in List-I. Match each "
     "arrangement with its equivalent resistance in List-II.",
     ["All four in series", "All four in parallel",
      "Two in series, and this pair connected in parallel with the other two in series",
      "Three in parallel, and this group connected in series with the fourth"],
     ["R/4", "4R/3", "4R", "R"]),
  *mlo("A-III, B-I, C-IV, D-II",
       ["A-III, B-I, C-II, D-IV", "A-I, B-III, C-IV, D-II", "A-IV, B-I, C-III, D-II"], "C"),
  "Series and parallel combinations",
  "Series resistances add; for parallel resistances the reciprocals add.",
  ["A: R + R + R + R = 4R → III", "B: R/4 → I", "C: 2R ∥ 2R = R → IV", "D: R/3 + R = 4R/3 → II"],
  why="The other codes swap the two mixed arrangements or the series and parallel results.",
  ncert=NC + "'Current Electricity', combination of resistors (series and parallel)", seconds=60)

cube = [(0, 1, 6), (1, 2, 6), (2, 3, 6), (3, 0, 6), (4, 5, 6), (5, 6, 6), (6, 7, 6), (7, 4, 6),
        (0, 4, 6), (1, 5, 6), (2, 6, 6), (3, 7, 6)]
assert equivalent_resistance(8, cube, 0, 6) == 5
assert equivalent_resistance(8, cube, 0, 1) == F(7, 2)
assert equivalent_resistance(8, cube, 0, 2) == F(9, 2)
q(CE, "Combination of resistors", "Advanced", "numerical",
  "Twelve identical resistors, each of 6 Ω, form the edges of a cube. The equivalent resistance between two "
  "corners of the cube that are at opposite ends of a body diagonal is:",
  *opt("5 Ω", ["3.5 Ω", "4.5 Ω", "72 Ω"], "C"),
  "Equivalent resistance using symmetry (equipotential points)",
  "Feed current I in at one corner and take it out at the opposite corner. By symmetry it splits equally into the "
  "three edges at each end and into the six middle edges.",
  ["Entry corner: three edges, each carries I/3", "Middle: six edges, each carries I/6",
   "Exit corner: three edges, each carries I/3",
   "V = (I/3)R + (I/6)R + (I/3)R = (5/6)IR → R_eq = 5R/6 = 5 × 6/6 = 5 Ω"],
  why="3.5 Ω (7R/12) is the resistance between the ends of one edge. 4.5 Ω (3R/4) is the resistance across a face "
      "diagonal. 72 Ω puts all twelve resistors in series.",
  seconds=90, rc=True)

bridge = [(0, 1, 1), (1, 3, 2), (0, 2, 2), (2, 3, 1), (1, 2, 1)]
vb = solve_network(4, bridge, {0: 7, 3: 0})
assert vb[1] == 4 and vb[2] == 3 and (vb[1] - vb[2]) / 1 == 1
assert (7 - vb[1]) / 1 + (7 - vb[2]) / 2 == 5
q(CE, "Kirchhoff's laws", "Advanced", "numerical",
  "An ideal 7 V battery is connected between points A (positive) and C. Between A and C there are two paths: "
  "A to B through 1 Ω and then B to C through 2 Ω; and A to D through 2 Ω and then D to C through 1 Ω. Points B and "
  "D are joined by a 1 Ω resistor. The current in the resistor joining B and D is:",
  *opt("1 A, flowing from B to D", ["1 A, flowing from D to B", "zero, since the bridge is balanced",
                                    "5 A, flowing from B to D"], "A"),
  "Kirchhoff's rules (node potentials) for an unbalanced bridge",
  "Take C as zero potential and A at 7 V. Write the junction rule at B and at D for the unknown potentials, solve, "
  "and find the current from the potential difference across BD.",
  ["At B: (7 − V_B)/1 = V_B/2 + (V_B − V_D)/1 → 2.5V_B − V_D = 7",
   "At D: (7 − V_D)/2 = V_D/1 + (V_D − V_B)/1 → 2.5V_D − V_B = 3.5",
   "Solving: V_B = 4 V, V_D = 3 V", "I(BD) = (4 − 3)/1 = 1 A, from B (higher potential) to D"],
  why="The bridge is not balanced (1/2 ≠ 2/1), so the current is not zero. B is at the higher potential, so the "
      "current is not from D to B. 5 A is the total current drawn from the battery, not the current in BD.",
  ncert=NC + "'Current Electricity', Kirchhoff's rules; Wheatstone bridge", seconds=150, rc=True)

q(CE, "Drift velocity and Ohm's law", "Advanced", "statement_pair",
  sp("A wire whose cross-section is not uniform carries a steady current; the drift speed of its free electrons is "
     "greater in the thinner parts of the wire.",
     "In such a wire, the electric field inside the wire has the same magnitude at every cross-section."),
  SP, sp_key(True, False),
  "Steady current through a non-uniform conductor: I = neAv_d and J = σE",
  "In steady state the same current I passes every cross-section. With the same n everywhere, v_d = I/(neA) is "
  "larger where A is smaller. The current density J = I/A is also larger there, and since E = J/σ = ρJ, the "
  "field is larger in the thinner parts too.",
  ["Same I at every section (charge does not pile up)", "v_d = I/(neA) ∝ 1/A → larger where thinner → I true",
   "E = ρI/A ∝ 1/A → not the same everywhere → II false"],
  why="Statement II would hold only for a uniform wire. Statement I is true, so options calling it false are wrong.",
  ncert=NC + "'Current Electricity', drift of electrons; resistivity (J = σE)", seconds=60)

E_m, r_m = 6, 2
Rs = [F(x, 10) for x in range(1, 200)]
P = lambda R: F(E_m) ** 2 * R / (R + r_m) ** 2
best = max(Rs, key=P)
assert best == r_m and r_m / (r_m + r_m) == F(1, 2)
assert all(P(Rs[i]) > P(Rs[i + 1]) for i in range(19, len(Rs) - 1))
mt = {"a": True, "b": False, "c": True, "d": False, "e": True}
q(CE, "Cells, emf and internal resistance", "Advanced", "multi_statement",
  ms("A cell of emf ε and internal resistance r is connected across an external resistor whose resistance R can "
     "be varied from zero upwards. Which of the following statements are correct?",
     ["The current is largest when R = 0, and then equals ε/r.",
      "When R = r, the cell delivers 100% of the power it generates to the external resistor.",
      "The potential difference across the terminals of the cell increases as R is increased.",
      "As R is increased beyond r, the power dissipated in the external resistor keeps increasing.",
      "The power dissipated in the external resistor is greatest when R = r."]),
  *mso(mt, "ace", ["abe", "cd", "bcd"], "B"),
  "Current, terminal voltage and power for a cell with internal resistance",
  "I = ε/(R + r), V = IR = εR/(R + r) and P = ε²R/(R + r)². P is greatest when R = r, where the efficiency R/(R + r) "
  "is only 50%; beyond R = r the power falls again.",
  ["(a) R = 0 → I = ε/r, the largest value → true",
   "(b) efficiency = R/(R + r) = 1/2 at R = r → 50%, not 100% → false",
   "(c) V = ε/(1 + r/R) increases with R → true",
   "(d) P decreases for R > r → false", "(e) dP/dR = 0 at R = r → maximum → true"],
  why="Any option containing (b) or (d) is wrong, and any option missing one of (a), (c), (e) is incomplete.",
  ncert=NC + "'Current Electricity', cells, emf, internal resistance; electrical power", seconds=90, rc=True)

mt = {"a": True, "b": True, "c": True, "d": False, "e": False}
q(CE, "Drift velocity and Ohm's law", "Advanced", "multi_statement",
  ms("Which of the following statements about Ohm's law and its limitations are correct?",
     ["For a p-n junction diode, reversing the direction of an applied voltage of the same magnitude does not give "
      "a current of the same magnitude in the opposite direction.",
      "For a material such as GaAs, the same current can flow at more than one value of the applied voltage.",
      "At constant temperature, the graph of current against voltage for an ohmic conductor is a straight line "
      "through the origin.",
      "The resistance of an ohmic conductor kept at constant temperature changes with the current through it.",
      "A device whose current depends on the sign of the applied voltage obeys Ohm's law."]),
  *mso(mt, "abc", ["abd", "bce", "acde"], "D"),
  "Ohmic and non-ohmic behaviour",
  "Ohm's law (V ∝ I with constant R at fixed temperature) is not universal. NCERT lists three kinds of departure: "
  "V stops being proportional to I, the relation depends on the sign of V (as in a diode), and the relation is not "
  "unique (as in GaAs).",
  ["(a) diode: depends on sign of V → true", "(b) GaAs: V–I relation not unique → true",
   "(c) ohmic conductor: straight line through origin → true",
   "(d) ohmic means R constant at fixed temperature → false",
   "(e) a sign-dependent device is non-ohmic → false"],
  why="Options containing (d) or (e) include a false statement; they confuse the definition of an ohmic conductor.",
  ncert=NC + "'Current Electricity', limitations of Ohm's law", seconds=75)

# ================================================================ Magnetic Effects of Current and Magnetism (B6 I7 A6)
mu0 = 4 * math.pi * 1e-7
B_c = mu0 * 50 * 2 / (2 * 0.10)
close(B_c, 2 * math.pi * 1e-4)
close(mu0 * 50 * 2 / (4 * 0.10), math.pi * 1e-4)
close(mu0 * 50 * 2 / 0.10, 4 * math.pi * 1e-4)
close(mu0 * 2 / (2 * 0.10), 4 * math.pi * 1e-6)
q(MAG, "Biot-Savart law", "Basic", "numerical",
  "A flat circular coil of 50 turns and radius 10 cm carries a current of 2 A. Taking µ₀ = 4π × 10⁻⁷ T m A⁻¹, "
  "the magnetic field at the centre of the coil is:",
  *opt("2π × 10⁻⁴ T", ["π × 10⁻⁴ T", "4π × 10⁻⁴ T", "4π × 10⁻⁶ T"], "A"),
  "Field at the centre of a circular coil: B = µ₀NI/(2R)",
  "Each turn contributes µ₀I/(2R) at the centre (from the Biot-Savart law), and the N turns add.",
  ["B = µ₀NI/(2R) = (4π × 10⁻⁷ × 50 × 2)/(2 × 0.10)", "= (4π × 10⁻⁵)/0.2 = 2π × 10⁻⁴ T (about 6.3 × 10⁻⁴ T)"],
  why="π × 10⁻⁴ T uses µ₀NI/(4R), the result for a semicircle. 4π × 10⁻⁴ T drops the 2 in the denominator. "
      "4π × 10⁻⁶ T ignores the number of turns.",
  ncert=NC + "'Moving Charges and Magnetism', magnetic field on the axis of a circular current loop",
  seconds=35, rc=True)

F_w = 0.3 * 4 * 0.5 * math.sin(math.radians(30))
close(F_w, 0.30)
close(0.3 * 4 * 0.5 * math.cos(math.radians(30)), 0.52)
close(0.3 * 4 * 0.5, 0.60)
q(MAG, "Force on charges and conductors", "Basic", "numerical",
  "A straight wire 0.5 m long carries a current of 4 A in a uniform magnetic field of 0.3 T. The wire makes an "
  "angle of 30° with the direction of the field. The magnitude of the magnetic force on the wire is:",
  *opt("0.30 N", ["0.52 N", "0.60 N", "0.15 N"], "B"),
  "Force on a current-carrying conductor: F = BIL sin θ",
  "Only the component of the field perpendicular to the wire exerts a force on it.",
  ["F = BIL sin θ = 0.3 × 4 × 0.5 × sin 30°", "= 0.6 × 0.5 = 0.30 N"],
  why="0.52 N uses cos 30° instead of sin 30°. 0.60 N takes the wire to be perpendicular to the field. 0.15 N "
      "halves the answer a second time.",
  ncert=NC + "'Moving Charges and Magnetism', magnetic force on a current-carrying conductor", seconds=30, rc=True)

r_e = 9e-31 * 1.6e6 / (1.6e-19 * 9e-5)
close(r_e, 0.10)
close(2 * math.pi * r_e, 0.628)
q(MAG, "Force on charges and conductors", "Basic", "numerical",
  "An electron (mass 9 × 10⁻³¹ kg, charge magnitude 1.6 × 10⁻¹⁹ C) moves with a speed of 1.6 × 10⁶ m/s at right "
  "angles to a uniform magnetic field of 9 × 10⁻⁵ T. The radius of its circular path is:",
  *opt("10 cm", ["20 cm", "5 cm", "62.8 cm"], "C"),
  "Circular motion in a magnetic field: r = mv/(qB)",
  "The magnetic force qvB supplies the centripetal force mv²/r.",
  ["qvB = mv²/r → r = mv/(qB)", "r = (9 × 10⁻³¹ × 1.6 × 10⁶)/(1.6 × 10⁻¹⁹ × 9 × 10⁻⁵)",
   "= (1.44 × 10⁻²⁴)/(1.44 × 10⁻²³) = 0.10 m = 10 cm"],
  why="20 cm and 5 cm come from an extra factor of 2 in the numerator or the denominator. 62.8 cm is the "
      "circumference 2πr, not the radius.",
  ncert=NC + "'Moving Charges and Magnetism', motion in a magnetic field", seconds=40, rc=True)

q(MAG, "Ampere's law", "Basic", "direct",
  "According to Ampere's circuital law, the line integral of the magnetic field B around any closed path is equal "
  "to µ₀ times:",
  *opt("the net current passing through the surface bounded by the closed path",
       ["the total current in all conductors near the path, whether or not they pass through it",
        "the current per unit length of the path",
        "zero, whatever currents are present"], "B"),
  "Ampere's circuital law: ∮B·dl = µ₀I_enclosed",
  "Only currents that thread the closed loop (pass through a surface bounded by it) contribute to the line "
  "integral. Currents outside the loop change B at points on the loop but add nothing to the integral.",
  ["∮B·dl = µ₀ I_e, where I_e is the net current through the surface bounded by the loop"],
  why="Currents outside the loop do not count. 'Current per unit length' and 'zero always' do not state the law.",
  ncert=NC + "'Moving Charges and Magnetism', Ampere's circuital law", seconds=20)

q(MAG, "Magnetic materials", "Basic", "direct",
  "When a ferromagnetic material is heated above a certain temperature (its Curie temperature), it becomes:",
  *opt("paramagnetic", ["diamagnetic", "superconducting", "more strongly ferromagnetic"], "D"),
  "Temperature dependence of ferromagnetism",
  "Thermal agitation destroys the alignment of the atomic moments within domains. Above the Curie temperature the "
  "ferromagnetic property is lost and the material behaves as a paramagnet.",
  ["Ferromagnetism depends on temperature", "Above the Curie temperature T_c, the substance is paramagnetic"],
  why="The material does not become diamagnetic or superconducting, and heating weakens rather than strengthens "
      "ferromagnetism.",
  ncert=NC + "'Magnetism and Matter', ferromagnetism", seconds=20)

q(MAG, "Magnetic dipole and bar magnet", "Basic", "match_list",
  ml("Match each quantity in List-I with its expression in List-II. (m is a magnetic dipole moment and B a uniform "
     "magnetic field.)",
     ["Magnetic moment of a coil of N turns, each of area A, carrying current I",
      "Torque on a magnetic dipole m in a uniform field B",
      "Potential energy of a magnetic dipole m in a uniform field B",
      "Magnetic field at a far axial point, distance r from the centre of a short bar magnet"],
     ["m × B", "NIA", "µ₀(2m)/(4πr³)", "−m·B"]),
  *mlo("A-II, B-I, C-IV, D-III",
       ["A-II, B-IV, C-I, D-III", "A-I, B-II, C-IV, D-III", "A-II, B-I, C-III, D-IV"], "C"),
  "The current loop and the bar magnet as magnetic dipoles",
  "A current loop behaves as a dipole of moment m = NIA. In a uniform field a dipole feels a torque m × B and has "
  "potential energy −m·B. Far along its axis a short magnet produces B = µ₀(2m)/(4πr³).",
  ["A → NIA (II)", "B → m × B (I)", "C → −m·B (IV)", "D → µ₀(2m)/(4πr³) (III)"],
  why="The other codes swap torque with potential energy, or the moment with the torque, or the axial field with "
      "the potential energy.",
  ncert=NC + "'Moving Charges and Magnetism', the magnetic dipole moment of a current loop; 'Magnetism and "
             "Matter', the bar magnet", seconds=40)

q(MAG, "Ampere's law", "Intermediate", "assertion_reason",
  ar("For an ideal toroid with n turns per unit length carrying a current I, the magnetic field at a point in the "
     "open space enclosed by the toroid (not within its windings) is µ₀nI.",
     "A circular Amperian loop drawn through that open space, coaxial with the toroid, encloses no net current."),
  AR, ar_key(False, True),
  "Ampere's law applied to a toroid",
  "A loop in the open space inside the toroid does not pass through any winding, so the enclosed current is zero "
  "and B there is zero. The field µ₀nI exists only in the region enclosed by the windings (the core). A is false "
  "and R is true.",
  ["Loop in the open space: I_enclosed = 0 → B(2πr) = 0 → B = 0", "So A is false; R is true"],
  why="A is false, so options A, B and C (which all need A to be true) are wrong.",
  ncert=NC + "'Moving Charges and Magnetism', the solenoid and the toroid (Ampere's law)", seconds=45)

B0 = mu0 * 1 / (2 * 0.02 * math.pi)
close(B0, 1e-5)
close(math.hypot(B0, B0), math.sqrt(2) * 1e-5)
q(MAG, "Biot-Savart law", "Intermediate", "numerical",
  "Two identical circular coils, each of one turn and radius 2π cm, have a common centre and their planes are "
  "perpendicular to each other. Each carries a current of 1 A. Taking µ₀ = 4π × 10⁻⁷ T m A⁻¹, the magnitude of the "
  "resultant magnetic field at the common centre is:",
  *opt("√2 × 10⁻⁵ T", ["2 × 10⁻⁵ T", "zero", "1 × 10⁻⁵ T"], "C"),
  "Superposition of magnetic fields (vector addition)",
  "Each coil gives a field µ₀I/(2R) along its own axis. The two axes are perpendicular, so the fields add as "
  "perpendicular vectors.",
  ["B₁ = B₂ = µ₀I/(2R) = (4π × 10⁻⁷ × 1)/(2 × 2π × 10⁻²) = 1 × 10⁻⁵ T",
   "B = √(B₁² + B₂²) = √2 × 10⁻⁵ T"],
  why="2 × 10⁻⁵ T adds the fields as if they were parallel. Zero assumes they cancel. 1 × 10⁻⁵ T is the field of "
      "one coil only.",
  ncert=NC + "'Moving Charges and Magnetism', magnetic field on the axis of a circular current loop",
  seconds=50, rc=True)

F_semi = 0.2 * 5 * (2 * 0.10)
close(F_semi, 0.20)
close(0.2 * 5 * math.pi * 0.10, 0.314)
close(0.2 * 5 * 0.10, 0.10)
q(MAG, "Force on charges and conductors", "Intermediate", "numerical",
  "A wire bent into a semicircle of radius 10 cm carries a current of 5 A. It lies in a plane perpendicular to a "
  "uniform magnetic field of 0.2 T. The magnitude of the net magnetic force on the semicircular wire is:",
  *opt("0.20 N", ["0.31 N", "0.10 N", "zero"], "A"),
  "Force on a curved wire in a uniform field equals the force on the straight wire joining its ends",
  "In a uniform field, F = I(∫dl) × B, and ∫dl along any path is the straight vector from one end to the other. For "
  "a semicircle this is the diameter 2R, which is perpendicular to B.",
  ["Effective length = diameter = 2R = 0.20 m", "F = BI(2R) = 0.2 × 5 × 0.20 = 0.20 N"],
  why="0.31 N uses the arc length πR as if the arc were straight. 0.10 N uses R instead of 2R. Zero would be "
      "correct only for a closed loop.",
  ncert=NC + "'Moving Charges and Magnetism', magnetic force on a current-carrying conductor", seconds=60, rc=True)

T_p = 2 * math.pi * 1.6e-27 / (1.6e-19 * 0.5)
close(T_p, 4 * math.pi * 1e-8)
q(MAG, "Force on charges and conductors", "Intermediate", "numerical",
  "A proton (mass 1.6 × 10⁻²⁷ kg, charge 1.6 × 10⁻¹⁹ C) moves in a circle at right angles to a uniform magnetic "
  "field of 0.5 T with a speed of 2 × 10⁶ m/s. The time it takes to complete one revolution is:",
  *opt("4π × 10⁻⁸ s", ["2π × 10⁻⁸ s", "2 × 10⁻⁸ s", "8π × 10⁻⁸ s"], "D"),
  "Period of circular motion in a magnetic field: T = 2πm/(qB), independent of speed",
  "r = mv/(qB) grows in proportion to v, so the time 2πr/v does not depend on the speed. The speed in the stem is "
  "not needed.",
  ["T = 2πr/v = 2πm/(qB)", "= 2π × 1.6 × 10⁻²⁷/(1.6 × 10⁻¹⁹ × 0.5) = 2π × 2 × 10⁻⁸ = 4π × 10⁻⁸ s (≈ 0.13 µs)"],
  why="2π × 10⁻⁸ s is the time for half a revolution (πm/qB). 2 × 10⁻⁸ s leaves out the factor 2π. 8π × 10⁻⁸ s "
      "doubles the mass.",
  ncert=NC + "'Moving Charges and Magnetism', motion in a magnetic field", seconds=45, rc=True)

q(MAG, "Torque on loop and galvanometer", "Intermediate", "assertion_reason",
  ar("In a moving-coil galvanometer, the steady deflection of the coil is proportional to the current through it.",
     "The cylindrical pole pieces and the soft-iron core make the magnetic field radial, so the plane of the coil "
     "stays parallel to the field and the deflecting torque is NIAB in every position of the coil."),
  AR, ar_key(True, True, True),
  "Moving-coil galvanometer: radial field and linear scale",
  "In equilibrium the deflecting torque balances the spring's restoring torque: NIAB = kφ, so φ = (NAB/k)I. This "
  "linear relation needs the torque to be NIAB whatever the angle, which is exactly what the radial field ensures. "
  "R explains A.",
  ["Radial field → torque = NIAB (no sin θ factor)", "Equilibrium: NIAB = kφ → φ ∝ I"],
  why="Without a radial field the torque would vary as sin θ and the deflection would not be proportional to I, "
      "so R is the explanation, not an unrelated fact (B is wrong). Both are true (C, D wrong).",
  ncert=NC + "'Moving Charges and Magnetism', the moving coil galvanometer", seconds=45)

q(MAG, "Magnetic materials", "Intermediate", "statement_pair",
  sp("Diamagnetism is present in all substances, but in most paramagnetic and ferromagnetic substances it is "
     "masked by their much stronger paramagnetic or ferromagnetic behaviour.",
     "The relative permeability of a diamagnetic substance is slightly less than 1."),
  SP, sp_key(True, True),
  "Diamagnetism and relative permeability",
  "Diamagnetism arises from the orbital motion of electrons responding to an applied field, so every substance "
  "has it; it is weak and is usually swamped when the atoms have permanent moments. For a diamagnet χ is small and "
  "negative, so µr = 1 + χ is slightly less than 1.",
  ["Statement I: as stated in NCERT → true", "µr = 1 + χ with −1 < χ < 0 (small) → slightly below 1 → true"],
  why="Both statements are true, so every other option is wrong.",
  ncert=NC + "'Magnetism and Matter', diamagnetism", seconds=35)

q(MAG, "Biot-Savart law", "Intermediate", "match_list",
  ml("A steady current I flows in each configuration of List-I. Match the configuration with the magnitude of the "
     "magnetic field it produces at the stated point (List-II).",
     ["At the centre of a circular loop of radius R",
      "At a distance R from a very long straight wire",
      "Well inside a long solenoid having n turns per unit length",
      "On the axis of a circular loop of radius R, at a distance x from its centre"],
     ["µ₀nI", "µ₀I/(2πR)", "µ₀IR²/[2(R² + x²)^(3/2)]", "µ₀I/(2R)"]),
  *mlo("A-IV, B-II, C-I, D-III",
       ["A-II, B-IV, C-I, D-III", "A-IV, B-II, C-III, D-I", "A-III, B-II, C-I, D-IV"], "B"),
  "Standard magnetic field results",
  "These follow from the Biot-Savart law (loop, straight wire) and Ampere's law (solenoid).",
  ["Loop centre: µ₀I/(2R) → IV", "Straight wire: µ₀I/(2πR) → II", "Solenoid: µ₀nI → I",
   "Loop axis: µ₀IR²/[2(R² + x²)^(3/2)] → III (it reduces to IV at x = 0)"],
  why="The commonest slip is swapping µ₀I/(2R) and µ₀I/(2πR), which differ only by π.",
  ncert=NC + "'Moving Charges and Magnetism', Biot-Savart law applications; Ampere's circuital law", seconds=45)

ratio_ax = 1 / (1 + 3) ** 1.5   # R³/(R² + 3R²)^(3/2) with R = 1
close(ratio_ax, 1 / 8)
close(1 / (1 + 3), 1 / 4)
q(MAG, "Biot-Savart law", "Advanced", "numerical",
  "A circular loop of radius R carries a steady current. The ratio of the magnetic field at a point on its axis at a "
  "distance √3 R from its centre to the magnetic field at the centre of the loop is:",
  *opt("1/8", ["1/4", "1/2", "√3/8"], "B"),
  "Field on the axis of a circular loop: B(x) = µ₀IR²/[2(R² + x²)^(3/2)]",
  "Divide the axial field by the centre field µ₀I/(2R); everything except the geometry cancels.",
  ["B(x)/B(0) = R³/(R² + x²)^(3/2)", "With x² = 3R²: (R² + 3R²)^(3/2) = (4R²)^(3/2) = 8R³",
   "Ratio = R³/8R³ = 1/8"],
  why="1/4 forgets the power 3/2 and uses R²/(R² + x²). 1/2 treats the field as falling like 1/x. √3/8 keeps an "
      "extra factor of x/R.",
  ncert=NC + "'Moving Charges and Magnetism', magnetic field on the axis of a circular current loop",
  seconds=60, rc=True)

x_eq = F(2 * 30, 2 + 8)
assert x_eq == 6 and F(2, 6) == F(8, 30 - 6)
x_out = F(2 * 30, 8 - 2)
assert x_out == 10 and F(2, 10) == F(8, 30 + 10)
q(MAG, "Force on charges and conductors", "Advanced", "numerical",
  "Two long parallel wires P and Q, 30 cm apart, carry currents of 2 A and 8 A respectively in the same direction. "
  "A third long straight wire carrying a current is placed parallel to them, in their plane. It experiences no net "
  "magnetic force when it is placed:",
  *opt("between the wires, 6 cm from P",
       ["between the wires, 24 cm from P", "on the far side of P from Q, 10 cm from P",
        "midway between the wires"], "C"),
  "Force between parallel currents: F/L = µ₀I₁I₂/(2πd)",
  "The force on the third wire from each of P and Q is proportional to (that wire's current)/(distance). For no "
  "net force the two must be equal and opposite. With P and Q in the same direction, the two forces oppose only "
  "between the wires. The result does not depend on the current in the third wire.",
  ["Between the wires, at x from P: 2/x = 8/(30 − x)", "2(30 − x) = 8x → x = 6 cm from P (nearer the smaller current)"],
  why="24 cm from P puts the wire nearer the larger current (ratio inverted). 10 cm on the far side of P is where "
      "the forces would cancel if the currents were opposite. The midpoint would need equal currents.",
  ncert=NC + "'Moving Charges and Magnetism', force between two parallel currents", seconds=75, rc=True)

m_d, B_d = 0.5, 0.4
W_rot = m_d * B_d * (math.cos(math.radians(60)) - math.cos(math.radians(180)))
close(W_rot, 0.30)
close(m_d * B_d * (1 - math.cos(math.radians(60))), 0.10)
q(MAG, "Magnetic dipole and bar magnet", "Advanced", "numerical",
  "A current loop of magnetic moment 0.5 A m² is in a uniform magnetic field of 0.4 T, its moment making an angle "
  "of 60° with the field. The work that must be done by an external agent to turn it slowly until its moment is "
  "antiparallel to the field is:",
  *opt("0.30 J", ["0.10 J", "0.20 J", "0.40 J"], "D"),
  "Potential energy of a magnetic dipole: U = −mB cos θ; work done = U_final − U_initial",
  "Turning the dipole slowly, the external work equals the increase in potential energy.",
  ["U(60°) = −mB cos 60° = −0.2 × 0.5 = −0.10 J", "U(180°) = −mB cos 180° = +0.20 J",
   "W = 0.20 − (−0.10) = 0.30 J"],
  why="0.10 J is the work to turn from 0° to 60°. 0.20 J is just mB. 0.40 J (2mB) is the work to turn from 0° to "
      "180°, not from 60°.",
  ncert=NC + "'Magnetism and Matter', the dipole in a uniform magnetic field", seconds=70, rc=True)

theta_dev = math.degrees(math.asin(F(1, 2)))
close(theta_dev, 30)
close(math.degrees(math.acos(0.5)), 60)
close(math.degrees(math.atan(0.5)), 26.57)
q(MAG, "Force on charges and conductors", "Advanced", "numerical",
  "A proton moving at right angles to the boundary enters a region of uniform magnetic field directed "
  "perpendicular to its velocity. The field region has a width d along the proton's original direction of motion, "
  "and the radius of the proton's circular path inside the field is 2d. The angle through which the proton has "
  "been deflected when it leaves the field region is:",
  *opt("30°", ["60°", "26.6°", "90°"], "A"),
  "Circular arc of a charged particle crossing a field region",
  "Inside the field the proton moves on a circle of radius r whose centre lies on the boundary line through the "
  "entry point. After turning through angle θ its displacement along the original direction is r sin θ. It leaves "
  "when this equals d (possible because d < r).",
  ["r sin θ = d", "sin θ = d/r = d/(2d) = 1/2 → θ = 30°"],
  why="60° uses cos θ = d/r. 26.6° uses tan θ = d/r. 90° would need d = r; here d < r, so the proton leaves "
      "before turning through a quarter circle.",
  seconds=75, rc=True)

B_arcs = F(1, 4) - F(1, 8)
assert B_arcs == F(1, 8) and F(1, 4) + F(1, 8) == F(3, 8)
q(MAG, "Biot-Savart law", "Advanced", "numerical",
  "A closed wire loop consists of a semicircle of radius R and a semicircle of radius 2R with a common centre O, "
  "joined at their ends by two straight radial segments lying along a diameter. A steady current I flows round the "
  "loop. The magnitude of the magnetic field at O is:",
  *opt("µ₀I/(8R)", ["3µ₀I/(8R)", "µ₀I/(4R)", "zero"], "D"),
  "Field of a circular arc at its centre: B = (µ₀I/4πR) × (angle subtended); straight segments through O give zero",
  "Each semicircle gives µ₀I/(4r) at O. Going round the closed loop, the current flows in opposite senses (one "
  "clockwise, one anticlockwise about O) in the two arcs, so their fields at O are opposite. The radial segments "
  "point at O and contribute nothing.",
  ["Inner arc: µ₀I/(4R)", "Outer arc: µ₀I/(4 × 2R) = µ₀I/(8R), opposite in direction",
   "Net B = µ₀I/(4R) − µ₀I/(8R) = µ₀I/(8R), in the direction of the inner arc's field"],
  why="3µ₀I/(8R) adds the two fields although the current goes round O in opposite senses. µ₀I/(4R) counts only "
      "the inner arc. Zero would need equal radii.",
  ncert=NC + "'Moving Charges and Magnetism', magnetic field due to a current element, Biot-Savart law",
  seconds=90, rc=True)

mt = {"a": True, "b": True, "c": False, "d": False, "e": True}
q(MAG, "Magnetic materials", "Advanced", "multi_statement",
  ms("Which of the following statements about magnetic materials are correct?",
     ["The relative permeability of a ferromagnetic material is much greater than 1.",
      "When a diamagnetic material is placed in an external magnetic field, the field lines are pushed out of it "
      "and the field inside the material is reduced.",
      "In a ferromagnetic material, the magnetisation produced is opposite to the applied magnetic field.",
      "Copper and water are paramagnetic substances.",
      "Aluminium, sodium and calcium are paramagnetic substances."]),
  *mso(mt, "abe", ["acd", "bde", "abde"], "C"),
  "Classification of magnetic materials",
  "Ferromagnets: µr ≫ 1, magnetisation along the field. Diamagnets: field lines expelled, B inside reduced, χ < 0. "
  "NCERT lists copper, water, bismuth and lead among diamagnetic substances, and aluminium, sodium, calcium and "
  "oxygen (at STP) among paramagnetic ones.",
  ["(a) true", "(b) true", "(c) false: magnetisation is along the field (only a diamagnet opposes it)",
   "(d) false: copper and water are diamagnetic", "(e) true"],
  why="Options with (c) or (d) include a false statement; the remaining option leaves out (e) or another true "
      "statement.",
  ncert=NC + "'Magnetism and Matter', magnetic properties of materials", seconds=70)

# ================================================================ EMI and AC (B4 I6 A4)
L_s = 0.3
emf_s = L_s * (6 - 2) / 0.1
close(emf_s, 12)
close(L_s * 6 / 0.1, 18)
close(L_s * 8 / 0.1, 24)
close(L_s * 4, 1.2)
q(EMI, "Self and mutual inductance", "Basic", "numerical",
  "The current in a coil of self-inductance 0.3 H falls steadily from 6 A to 2 A in 0.1 s. The magnitude of the "
  "emf induced in the coil is:",
  *opt("12 V", ["18 V", "24 V", "1.2 V"], "B"),
  "Self-induced emf: ε = −L dI/dt",
  "A changing current changes the coil's own flux (NΦ = LI), which induces an emf opposing the change.",
  ["|dI/dt| = (6 − 2)/0.1 = 40 A/s", "|ε| = L|dI/dt| = 0.3 × 40 = 12 V"],
  why="18 V uses the initial current (6 A) instead of the change. 24 V adds the two currents. 1.2 V forgets to "
      "divide by the time.",
  ncert=NC + "'Electromagnetic Induction', self-inductance", seconds=30, rc=True)

C_ = 50e-6 / math.pi
Xc = 1 / (2 * math.pi * 50 * C_)
close(Xc, 200)
close(1 / (50 * C_), 400 * math.pi)
close(2 * math.pi * 50 * C_, 5e-3)
close(1 / (2 * math.pi * 50 * C_ * 1e-3), 2e5)
q(EMI, "AC: rms, reactance and impedance", "Basic", "numerical",
  "A capacitor of capacitance (50/π) µF is connected to a 50 Hz AC supply. Its capacitive reactance is:",
  *opt("200 Ω", ["400π Ω", "5 × 10⁻³ Ω", "2 × 10⁵ Ω"], "D"),
  "Capacitive reactance: X_C = 1/(ωC) = 1/(2πfC)",
  "A capacitor offers less opposition at higher frequency; its reactance falls as 1/f.",
  ["ωC = 2π × 50 × (50/π) × 10⁻⁶ = 5 × 10⁻³ S", "X_C = 1/(5 × 10⁻³) = 200 Ω"],
  why="400π Ω uses 1/(fC), leaving out 2π. 5 × 10⁻³ Ω is ωC, not its reciprocal. 2 × 10⁵ Ω reads the "
      "capacitance as (50/π) nF.",
  ncert=NC + "'Alternating Current', AC voltage applied to a capacitor", seconds=35, rc=True)

q(EMI, "Faraday's and Lenz's laws", "Basic", "direct",
  "The north pole of a bar magnet is moved towards one face of a closed circular coil. As seen from the side of "
  "the approaching magnet, the current induced in the coil flows:",
  *opt("anticlockwise, so that this face of the coil behaves as a north pole",
       ["clockwise, so that this face of the coil behaves as a south pole",
        "nowhere, because the coil is not connected to any battery",
        "clockwise, so that this face of the coil behaves as a north pole"], "A"),
  "Lenz's law",
  "The induced current opposes the change that causes it. The approaching north pole increases the flux, so the "
  "facing side of the coil becomes a north pole to repel it. A current that looks anticlockwise from that side "
  "makes that face a north pole.",
  ["Flux towards the coil increases → induced current must oppose the approach",
   "Facing side becomes N → current anticlockwise as seen by the magnet"],
  why="A south-pole face would attract the magnet and help the change, against Lenz's law. A closed coil needs no "
      "battery for an induced current. A clockwise current makes the facing side a south pole, not a north pole.",
  ncert=NC + "'Electromagnetic Induction', Lenz's law and conservation of energy", seconds=30)

q(EMI, "Faraday's and Lenz's laws", "Basic", "match_list",
  ml("Match each situation in List-I with the expression for the induced emf in List-II.",
     ["Emf in a coil of N turns linked by a changing magnetic flux Φ_B",
      "Emf across a rod of length l moving with speed v perpendicular to a uniform field B",
      "Peak emf of an AC generator with N turns of area A rotating at angular speed ω in field B",
      "Emf induced in coil 2 when the current I₁ in a neighbouring coil 1 changes"],
     ["NBAω", "−N dΦ_B/dt", "−M dI₁/dt", "Bvl"]),
  *mlo("A-II, B-IV, C-I, D-III",
       ["A-II, B-I, C-IV, D-III", "A-III, B-IV, C-I, D-II", "A-II, B-IV, C-III, D-I"], "C"),
  "Faraday's law and its applications",
  "All four follow from ε = −dΦ/dt applied to different set-ups.",
  ["A: Faraday's law for N turns → II", "B: motional emf → Bvl → IV",
   "C: ε = NBAω sin ωt, peak NBAω → I", "D: mutual induction, ε₂ = −M dI₁/dt → III"],
  why="The other codes swap the motional emf with the generator emf, or the mutual-induction emf with Faraday's law "
      "in general.",
  ncert=NC + "'Electromagnetic Induction', Faraday's law; motional emf; mutual inductance; 'Alternating "
             "Current' (AC generator)", seconds=40)

e_rod = 0.5 * 0.5 * 20 * 0.4 ** 2
close(e_rod, 0.8)
close(0.5 * 20 * 0.4 ** 2, 1.6)
close(0.5 * 20 * 0.4, 4.0)
q(EMI, "Faraday's and Lenz's laws", "Intermediate", "numerical",
  "A metal rod of length 0.4 m rotates with an angular speed of 20 rad/s about an axis through one end, "
  "perpendicular to the rod. A uniform magnetic field of 0.5 T is parallel to the axis of rotation. The emf "
  "induced between the ends of the rod is:",
  *opt("0.8 V", ["1.6 V", "4.0 V", "0.4 V"], "C"),
  "Motional emf in a rotating rod: ε = ½BωL²",
  "Different parts of the rod move with different speeds v = ωr. Adding the small emfs B(ωr)dr from r = 0 to L "
  "gives ½BωL² (equivalently, B × the average speed ωL/2 × L).",
  ["ε = ∫₀ᴸ Bωr dr = ½BωL²", "= ½ × 0.5 × 20 × 0.16 = 0.8 V"],
  shortcut="Use the speed of the midpoint: v_avg = ωL/2 = 4 m/s, so ε = B v_avg L = 0.5 × 4 × 0.4 = 0.8 V.",
  why="1.6 V leaves out the ½ (uses the speed of the free end for the whole rod). 4.0 V uses BωL, which is not "
      "even dimensionally an emf. 0.4 V puts in an extra factor ½.",
  ncert=NC + "'Electromagnetic Induction', motional electromotive force", seconds=50, rc=True)

L_sol = mu0 * 500 ** 2 * 1e-3 / 0.5
close(L_sol, 6.283e-4)
close(mu0 * 500 * 1e-3 / 0.5, 1.2566e-6)
close(mu0 * 500 ** 2 * 1e-2 / 0.5, 6.283e-3)
close(L_sol / 2, 3.14e-4)
q(EMI, "Self and mutual inductance", "Intermediate", "numerical",
  "An air-cored solenoid is 50 cm long, has 500 turns and a cross-sectional area of 10 cm². Taking "
  "µ₀ = 4π × 10⁻⁷ T m A⁻¹, its self-inductance is about:",
  *opt("0.63 mH", ["1.3 µH", "6.3 mH", "0.31 mH"], "A"),
  "Self-inductance of a long solenoid: L = µ₀N²A/l",
  "The field µ₀(N/l)I links all N turns of area A, so NΦ = µ₀N²AI/l and L = NΦ/I.",
  ["A = 10 cm² = 1 × 10⁻³ m²", "L = (4π × 10⁻⁷ × 500² × 1 × 10⁻³)/0.5",
   "= 4π × 10⁻⁷ × 500 = 6.28 × 10⁻⁴ H ≈ 0.63 mH"],
  why="1.3 µH uses N instead of N². 6.3 mH takes 10 cm² as 10⁻² m². 0.31 mH divides by 2l.",
  ncert=NC + "'Electromagnetic Induction', self-inductance", seconds=60, rc=True)

Z = math.hypot(40, 50 - 20)
close(Z, 50)
close(220 / Z, 4.4)
close(220 / (40 + 50 + 20), 2.0)
close(220 / 30, 7.33)
q(EMI, "AC: rms, reactance and impedance", "Intermediate", "numerical",
  "A series circuit of a 40 Ω resistor, an inductor of reactance 50 Ω and a capacitor of reactance 20 Ω is "
  "connected to a 220 V (rms) AC supply. The rms current and its phase relative to the supply voltage are:",
  *opt("4.4 A, lagging the voltage", ["4.4 A, leading the voltage", "2.0 A, lagging the voltage",
                                     "7.3 A, lagging the voltage"], "B"),
  "Impedance of a series LCR circuit: Z = √[R² + (X_L − X_C)²]",
  "The net reactance is X_L − X_C. Since it is positive (inductive), the current lags the voltage.",
  ["X_L − X_C = 50 − 20 = 30 Ω", "Z = √(40² + 30²) = 50 Ω", "I = 220/50 = 4.4 A",
   "X_L > X_C → circuit is inductive → current lags (tan φ = 30/40, φ ≈ 37°)"],
  why="'Leading' would need X_C > X_L. 2.0 A adds R, X_L and X_C arithmetically. 7.3 A uses only the net "
      "reactance and ignores R.",
  ncert=NC + "'Alternating Current', AC voltage applied to a series LCR circuit", seconds=60, rc=True)

I_res = 20 / 10
assert I_res == 2 and I_res * 100 == 200
q(EMI, "LCR resonance and power", "Intermediate", "numerical",
  "A series LCR circuit with R = 10 Ω is connected to an AC source of rms voltage 20 V whose frequency is set so "
  "that the circuit is in resonance; at this frequency the inductive reactance is 100 Ω. The rms voltage across "
  "the inductor is:",
  *opt("200 V", ["20 V", "zero", "10 V"], "D"),
  "Series resonance: X_L = X_C, Z = R; voltages across L and C are equal and opposite",
  "At resonance the impedance is just R, so the current is large; the voltage across L (and across C) is "
  "I·X_L, which can be many times the source voltage. The two cancel each other in the loop.",
  ["At resonance Z = R = 10 Ω → I = 20/10 = 2 A", "V_L = I X_L = 2 × 100 = 200 V (and V_C = 200 V, opposite in phase)"],
  why="20 V assumes no element can have more voltage than the source. Zero is the sum V_L + V_C, not V_L. 10 V "
      "halves the source voltage for no reason.",
  ncert=NC + "'Alternating Current', resonance", seconds=55, rc=True)

q(EMI, "LCR resonance and power", "Intermediate", "assertion_reason",
  ar("An ideal inductor connected to an AC source consumes no power on average over a complete cycle.",
     "In a purely inductive AC circuit, the current is in phase with the applied voltage."),
  AR, ar_key(True, False),
  "Power in a purely inductive circuit",
  "In a pure inductor the current lags the voltage by π/2, so the power factor cos φ = 0 and the average power "
  "V I cos φ = 0. Energy taken in one quarter cycle is returned in the next. A is true; R is false.",
  ["φ = π/2 for a pure inductor", "P_avg = V_rms I_rms cos(π/2) = 0 → A true",
   "Current lags by π/2, not in phase → R false"],
  why="R is false, so options A, B and D are wrong.",
  ncert=NC + "'Alternating Current', AC voltage applied to an inductor; power in AC circuit", seconds=40)

mt = {"a": True, "b": True, "c": False, "d": True, "e": False}
q(EMI, "Self and mutual inductance", "Intermediate", "multi_statement",
  ms("Which of the following statements about inductance are correct?",
     ["The self-inductance of a coil depends on its geometry and on the permeability of the medium inside it, not "
      "on the current through it.",
      "Inserting a soft-iron core into a coil increases its self-inductance.",
      "A self-induced emf always opposes the current in the coil.",
      "For a pair of coils, the mutual inductance of coil 1 with respect to coil 2 equals that of coil 2 with "
      "respect to coil 1.",
      "The SI unit of self-inductance is the tesla."]),
  *mso(mt, "abd", ["abc", "cde", "abde"], "B"),
  "Self and mutual inductance",
  "L = µ₀µr N²A/l depends on geometry and the core. The induced emf opposes the change in current (it can be along "
  "the current when the current is falling). M₁₂ = M₂₁. The unit of inductance is the henry.",
  ["(a) true", "(b) true: µr of iron ≫ 1", "(c) false: it opposes the change of current, not the current itself",
   "(d) true", "(e) false: henry (H = Wb/A)"],
  why="Options with (c) or (e) include a false statement.",
  ncert=NC + "'Electromagnetic Induction', inductance (mutual and self)", seconds=60)

Q_fl = 100 * (2 * 0.5 * 0.01) / 5
close(Q_fl, 0.2)
close(100 * 0.5 * 0.01 / 5, 0.1)
close(100 * 2 * 0.5 * 0.01, 1.0)
q(EMI, "Faraday's and Lenz's laws", "Advanced", "numerical",
  "A coil of 100 turns, each of area 100 cm², has a total resistance of 5 Ω and its ends are joined. It lies with "
  "its plane perpendicular to a uniform magnetic field of 0.5 T. It is then turned over through 180° about a "
  "diameter. The total charge that flows round the coil during the turn is:",
  *opt("0.2 C", ["0.1 C", "zero", "1.0 C"], "A"),
  "Charge induced by a flux change: Q = NΔΦ/R",
  "I = ε/R = −(N/R)dΦ/dt, so the charge Q = ∫I dt = NΔΦ/R depends only on the total change in flux, not on how "
  "fast the coil is turned. Turning over reverses the flux through each turn.",
  ["A = 100 cm² = 0.01 m²; Φ changes from +BA to −BA", "|ΔΦ| = 2BA = 2 × 0.5 × 0.01 = 0.01 Wb per turn",
   "Q = NΔΦ/R = 100 × 0.01/5 = 0.2 C"],
  why="0.1 C takes the flux change as BA, as for turning through 90°. Zero assumes the flux is the same because "
      "its magnitude is unchanged, but its sign reverses. 1.0 C forgets to divide by the resistance.",
  ncert=NC + "'Electromagnetic Induction', Faraday's law of induction", seconds=70, rc=True)

XL = 2 * math.pi * 50 * (1 / math.pi)
close(XL, 100)
C_need = 1 / (2 * math.pi * 50 * XL)
close(C_need, 100e-6 / math.pi)
close(200 ** 2 / 100, 400)
I_before = 200 / math.hypot(100, 100)
close(I_before ** 2 * 100, 200)
close(1 / (2 * math.pi * 50 * 50), 200e-6 / math.pi)
close(1 / (2 * math.pi * 50 * 200), 50e-6 / math.pi)
q(EMI, "LCR resonance and power", "Advanced", "numerical",
  "A 100 Ω resistor and an inductor of inductance (1/π) H are connected in series to a 200 V (rms), 50 Hz supply. "
  "A capacitor is to be added in series so that the power factor of the circuit becomes 1. The capacitance needed "
  "and the power then drawn from the supply are:",
  *opt("(100/π) µF and 400 W", ["(100/π) µF and 200 W", "(200/π) µF and 400 W", "(50/π) µF and 400 W"], "C"),
  "Power-factor correction: make X_C = X_L (series resonance); then P = V²/R",
  "A power factor of 1 means the net reactance is zero, so the capacitor must cancel the inductive reactance. The "
  "impedance then equals R.",
  ["X_L = 2πfL = 2π × 50 × (1/π) = 100 Ω", "X_C = 100 Ω → C = 1/(2πf X_C) = 1/(100π × 100) F = (100/π) µF",
   "P = V²/R = 200²/100 = 400 W"],
  why="200 W is the power before the capacitor is added (Z = 100√2 Ω, I = √2 A). (200/π) µF gives X_C = 50 Ω and "
      "(50/π) µF gives X_C = 200 Ω; neither cancels X_L.",
  ncert=NC + "'Alternating Current', resonance; power in AC circuit: the power factor", seconds=100, rc=True)

q(EMI, "AC generator and transformer", "Advanced", "statement_pair",
  sp("In an AC generator, the emf induced in the rotating coil is greatest at the instant when the plane of the coil "
     "is parallel to the magnetic field.",
     "The average value of a sinusoidal alternating current over one complete cycle is equal to its rms value."),
  SP, sp_key(True, False),
  "AC generator emf and average versus rms values",
  "With Φ = NBA cos ωt, the emf is NBAω sin ωt. It is largest when ωt = 90°, when the flux through the coil is zero, "
  "i.e. when the plane of the coil is parallel to B (the flux is then changing fastest). The average of a sinusoid "
  "over a full cycle is zero, while its rms value is I₀/√2.",
  ["ε = NBAω sin ωt; maximum when the coil's plane ∥ B → Statement I true",
   "Average over a cycle = 0 ≠ I₀/√2 → Statement II false"],
  why="Many students think the emf is greatest when the flux is greatest; it is the rate of change of flux that "
      "matters. Statement II is false, so options A and D are wrong.",
  ncert=NC + "'Electromagnetic Induction'/'Alternating Current', AC generator; rms value", seconds=50)

mt = {"a": True, "b": True, "c": True, "d": False, "e": False}
q(EMI, "LCR resonance and power", "Advanced", "multi_statement",
  ms("A series LCR circuit (with R ≠ 0) is driven by an AC source whose frequency is below the resonant frequency "
     "of the circuit. Which of the following statements are correct?",
     ["The capacitive reactance is greater than the inductive reactance.",
      "The current leads the applied voltage.",
      "The power factor of the circuit is less than 1.",
      "Increasing the capacitance, with L, R and the source frequency unchanged, takes the circuit further away "
      "from resonance.",
      "The impedance of the circuit is less than R."]),
  *mso(mt, "abc", ["abd", "cde", "bce"], "D"),
  "Behaviour of a series LCR circuit off resonance",
  "Below resonance, ω < 1/√(LC), so ωL < 1/(ωC): the circuit is capacitive and the current leads. The impedance "
  "√[R² + (X_C − X_L)²] exceeds R and cos φ = R/Z < 1. Increasing C lowers the resonant frequency 1/√(LC) "
  "towards the source frequency, bringing the circuit closer to resonance.",
  ["(a) ω < ω₀ → X_C > X_L → true", "(b) capacitive → current leads → true", "(c) Z > R → cos φ < 1 → true",
   "(d) larger C → smaller ω₀ → closer to ω → false", "(e) Z ≥ R always → false"],
  why="Options with (d) or (e) contain a false statement.",
  ncert=NC + "'Alternating Current', series LCR circuit; resonance", seconds=90)

# ================================================================ Electromagnetic Waves (B1 I2 A1)
q(EMW, "EM spectrum and uses", "Basic", "direct",
  "Special vacuum tubes called klystrons and magnetrons, and Gunn diodes, are used to produce:",
  *opt("microwaves", ["radio waves", "infrared waves", "X-rays"], "D"),
  "Production of the different parts of the electromagnetic spectrum",
  "NCERT notes that microwaves (used in radar and microwave ovens) are produced by klystrons, magnetrons and Gunn "
  "diodes. Radio waves come from accelerated charges in conducting wires (antennas), infrared from hot bodies, "
  "and X-rays from bombarding a metal target with high-energy electrons.",
  ["Klystron, magnetron, Gunn diode → microwaves"],
  why="The other radiations have different sources, listed in the explanation.",
  ncert=NC + "'Electromagnetic Waves', electromagnetic spectrum (microwaves)", seconds=20)

k_w, w_w = 200 * math.pi, 6 * math.pi * 1e10
close(2 * math.pi / k_w, 0.01)
close(w_w / k_w, 3e8)
close(w_w / (2 * math.pi), 3e10)
assert 1e-3 < 2 * math.pi / k_w < 0.1
q(EMW, "EM wave properties", "Intermediate", "numerical",
  "The electric field of an electromagnetic wave in vacuum is E_y = E₀ sin(200πx − 6π × 10¹⁰ t), with x in metres "
  "and t in seconds. The wavelength of the wave and the part of the spectrum it belongs to are:",
  *opt("1 cm; microwaves", ["0.5 cm; microwaves", "1 cm; infrared waves", "100 m; radio waves"], "B"),
  "Plane wave E = E₀ sin(kx − ωt): λ = 2π/k, f = ω/2π, v = ω/k",
  "Read k and ω from the phase. A check that ω/k = 3 × 10⁸ m/s confirms the wave is in vacuum.",
  ["k = 200π m⁻¹ → λ = 2π/k = 0.01 m = 1 cm", "ω = 6π × 10¹⁰ rad/s → f = 3 × 10¹⁰ Hz; ω/k = 3 × 10⁸ m/s ✓",
   "Microwaves span about 1 mm to 0.1 m → 1 cm is a microwave"],
  why="0.5 cm uses λ = π/k. 'Infrared' mis-places 1 cm; infrared lies between about 1 mm and 700 nm. 100 m reads "
      "k/(2π) = 100 as the wavelength.",
  ncert=NC + "'Electromagnetic Waves', electromagnetic waves; electromagnetic spectrum", seconds=60, rc=True)

q(EMW, "EM wave properties", "Intermediate", "assertion_reason",
  ar("An electromagnetic wave falling on a surface exerts a pressure on it.",
     "Electromagnetic waves carry energy but do not carry momentum."),
  AR, ar_key(True, False),
  "Momentum and radiation pressure of electromagnetic waves",
  "An electromagnetic wave carries momentum as well as energy: a wave delivering energy U to a surface that absorbs "
  "it completely delivers momentum U/c. The momentum delivered per second per unit area is the radiation pressure. "
  "A is true; R is false.",
  ["EM waves carry momentum p = U/c → R false", "Momentum transfer to the surface → force → pressure → A true"],
  why="R is false, so options A, B and D are wrong.",
  ncert=NC + "'Electromagnetic Waves', electromagnetic waves (momentum and radiation pressure)", seconds=35)

B_disp = mu0 * 2 * 0.05 / (2 * math.pi * 0.10 ** 2)
close(B_disp, 2e-6)
close(mu0 * 2 / (2 * math.pi * 0.05), 8e-6)
close(mu0 * 2 / (2 * math.pi * 0.10), 4e-6)
q(EMW, "Displacement current", "Advanced", "numerical",
  "A parallel-plate capacitor with circular plates of radius 10 cm is being charged by a steady current of 2 A. "
  "Neglecting edge effects and taking µ₀ = 4π × 10⁻⁷ T m A⁻¹, the magnitude of the magnetic field between the plates "
  "at a distance of 5 cm from their common axis is:",
  *opt("2 × 10⁻⁶ T", ["zero, since no conduction current flows between the plates", "8 × 10⁻⁶ T",
                      "4 × 10⁻⁶ T"], "D"),
  "Ampere-Maxwell law: ∮B·dl = µ₀(i_c + i_d); displacement current i_d = ε₀ dΦ_E/dt",
  "Between the plates the displacement current equals the charging current, spread uniformly over the plate area. "
  "A circular loop of radius r encloses the fraction r²/R² of it.",
  ["i_d (total) = 2 A; enclosed by loop of radius r: 2 × (5/10)² = 0.5 A",
   "B × 2πr = µ₀ × 0.5 → B = (4π × 10⁻⁷ × 0.5)/(2π × 0.05) = 2 × 10⁻⁶ T"],
  why="Zero ignores the displacement current. 8 × 10⁻⁶ T treats the full 2 A as enclosed within r = 5 cm. "
      "4 × 10⁻⁶ T is the field at the edge of the plates (r = 10 cm).",
  ncert=NC + "'Electromagnetic Waves', displacement current", seconds=90, rc=True)

# ================================================================ Optics (B7 I9 A7)
u_m, f_m = F(-20), F(20)
v_m = 1 / (1 / f_m - 1 / u_m)
assert v_m == 10 and -v_m / u_m == F(1, 2)
assert 1 / F(-20) - 1 / F(-20) == 0  # concave mirror, object at F: image at infinity
q(OPT, "Mirrors", "Basic", "numerical",
  "An object is placed 20 cm in front of a convex mirror of focal length 20 cm. The image is formed:",
  *opt("10 cm behind the mirror; magnification +0.5",
       ["at infinity", "20 cm behind the mirror; magnification +1",
        "10 cm in front of the mirror; magnification −0.5"], "B"),
  "Mirror equation 1/v + 1/u = 1/f with m = −v/u (Cartesian sign convention)",
  "For a convex mirror f is positive (focus behind the mirror) and a real object has negative u.",
  ["u = −20 cm, f = +20 cm", "1/v = 1/f − 1/u = 1/20 + 1/20 = 1/10 → v = +10 cm (behind the mirror)",
   "m = −v/u = −10/(−20) = +0.5: virtual, erect, half size"],
  why="'At infinity' is the answer for a concave mirror with the object at its focus. '20 cm behind, +1' treats "
      "the mirror as plane. '10 cm in front, −0.5' gets the size right but takes the image as real (sign slip).",
  ncert=NC + "'Ray Optics and Optical Instruments', the mirror equation", seconds=40, rc=True)

lam_g = 600 / 1.5
f_light = 3e8 / 600e-9
assert lam_g == 400
close(f_light, 5e14)
q(OPT, "Refraction and lenses", "Basic", "numerical",
  "Light of wavelength 600 nm in vacuum enters a glass block of refractive index 1.5. Taking c = 3 × 10⁸ m/s, the "
  "wavelength and the frequency of the light inside the glass are:",
  *opt("400 nm and 5.0 × 10¹⁴ Hz", ["900 nm and 5.0 × 10¹⁴ Hz", "400 nm and 3.3 × 10¹⁴ Hz",
                                     "600 nm and 7.5 × 10¹⁴ Hz"], "B"),
  "On refraction, frequency is unchanged; speed and wavelength are divided by n",
  "The frequency is fixed by the source. Since v = c/n and v = fλ, the wavelength in the medium is λ₀/n.",
  ["f = c/λ₀ = 3 × 10⁸/(600 × 10⁻⁹) = 5.0 × 10¹⁴ Hz (unchanged in glass)", "λ = λ₀/n = 600/1.5 = 400 nm"],
  why="900 nm multiplies by n instead of dividing. 3.3 × 10¹⁴ Hz wrongly reduces the frequency by n. 600 nm and "
      "7.5 × 10¹⁴ Hz keep the wavelength and change the frequency, the reverse of what happens.",
  ncert=NC + "'Ray Optics and Optical Instruments', refraction; 'Wave Optics', refraction of a plane wave",
  seconds=35, rc=True)

f_pc = F(20) / (F(3, 2) - 1)
assert f_pc == 40 and 1 / ((F(3, 2) - 1) * F(2, 20)) == 20
close(20 / 1.5, 13.33)
assert 20 * (F(3, 2) - 1) == 10
q(OPT, "Refraction and lenses", "Basic", "numerical",
  "A thin plano-convex lens is made of glass of refractive index 1.5, and the radius of curvature of its curved "
  "surface is 20 cm. Its focal length in air is:",
  *opt("40 cm", ["20 cm", "13.3 cm", "10 cm"], "C"),
  "Lens maker's formula: 1/f = (n − 1)(1/R₁ − 1/R₂)",
  "For the plane surface 1/R = 0, so only the curved surface contributes.",
  ["1/f = (1.5 − 1)(1/20 − 0) = 0.5/20 = 1/40", "f = 40 cm"],
  why="20 cm is the focal length of an equiconvex lens with both radii 20 cm. 13.3 cm uses n instead of (n − 1). "
      "10 cm multiplies R by (n − 1) instead of dividing.",
  ncert=NC + "'Ray Optics and Optical Instruments', refraction by a lens: lens maker's formula", seconds=30, rc=True)

q(OPT, "Total internal reflection", "Basic", "direct",
  "An optical fibre consists of a central core surrounded by a cladding. Light launched into the core is guided "
  "along the fibre, even round bends, because:",
  *opt("the refractive index of the core is greater than that of the cladding",
       ["the refractive index of the cladding is greater than that of the core",
        "the core and the cladding have the same refractive index",
        "the boundary between the core and the cladding is silvered like a mirror"], "A"),
  "Optical fibres and total internal reflection",
  "Total internal reflection needs light to go from a denser to a rarer medium at more than the critical angle. "
  "Making the core optically denser than the cladding lets light striking the core–cladding boundary at large "
  "angles be totally reflected again and again.",
  ["TIR requires n(core) > n(cladding)", "Rays meeting the boundary above the critical angle are trapped in the core"],
  why="A denser cladding or equal indices make TIR at the boundary impossible. The fibre is not silvered; "
      "reflection is total because of refraction physics, not a metal coating.",
  ncert=NC + "'Ray Optics and Optical Instruments', total internal reflection (optical fibres)", seconds=25)

q(OPT, "Huygens' principle and interference", "Basic", "direct",
  "According to Huygens' principle:",
  *opt("each point on a wavefront acts as a source of secondary wavelets, and the forward envelope of these wavelets "
       "gives the position of the wavefront at a later time",
       ["each point on a wavefront absorbs the light falling on it and re-emits it only in the backward direction",
        "only the centre of a wavefront acts as a source of new waves",
        "a wavefront is a surface on which the disturbance has different phases at different points"], "D"),
  "Huygens' construction of wavefronts",
  "A wavefront is a surface of constant phase. Every point on it acts as a source of secondary wavelets moving "
  "with the wave speed; the common tangent (envelope) to these wavelets in the forward direction is the new "
  "wavefront. Huygens assumed the backwave to be absent.",
  ["Wavefront: locus of points in the same phase", "New wavefront = forward envelope of secondary wavelets"],
  why="The backward-only and 'centre only' versions misstate the principle, and a wavefront is a surface of the "
      "same phase, not of different phases.",
  ncert=NC + "'Wave Optics', Huygens principle", seconds=25)

M_t, L_t = 100 / 5, 100 + 5
assert M_t == 20 and L_t == 105
q(OPT, "Optical instruments", "Basic", "numerical",
  "An astronomical telescope has an objective of focal length 100 cm and an eyepiece of focal length 5 cm. In "
  "normal adjustment (final image at infinity), the magnifying power and the distance between the two lenses are:",
  *opt("20 and 105 cm", ["20 and 95 cm", "0.05 and 105 cm", "500 and 105 cm"], "A"),
  "Telescope in normal adjustment: m = f_o/f_e, L = f_o + f_e",
  "The objective forms the image of a distant object at its focus; for a final image at infinity this point must "
  "also be the focus of the eyepiece.",
  ["m = f_o/f_e = 100/5 = 20", "L = f_o + f_e = 100 + 5 = 105 cm"],
  why="95 cm subtracts the focal lengths. 0.05 is f_e/f_o, the ratio upside down. 500 multiplies the focal lengths.",
  ncert=NC + "'Ray Optics and Optical Instruments', optical instruments: telescope", seconds=30, rc=True)

q(OPT, "Mirrors", "Basic", "match_list",
  ml("An object is placed on the principal axis of a concave mirror (C = centre of curvature, F = focus, P = pole). "
     "Match the position of the object (List-I) with the nature and position of the image (List-II).",
     ["Beyond C", "At F", "Between F and C", "Between P and F"],
     ["Virtual, erect, magnified, behind the mirror", "Real, inverted, highly magnified, at infinity",
      "Real, inverted, magnified, beyond C", "Real, inverted, diminished, between F and C"]),
  *mlo("A-IV, B-II, C-III, D-I",
       ["A-III, B-II, C-IV, D-I", "A-IV, B-I, C-III, D-II", "A-II, B-IV, C-III, D-I"], "C"),
  "Image formation by a concave mirror",
  "Use 1/v + 1/u = 1/f, or ray diagrams, for each object position.",
  ["Beyond C → image between F and C, real, inverted, diminished (IV)", "At F → image at infinity (II)",
   "Between F and C → image beyond C, real, inverted, magnified (III)",
   "Between P and F → virtual, erect, magnified, behind the mirror (I)"],
  why="The other codes swap the images for objects beyond C and between F and C (they are interchangeable by "
      "reversibility of light), or the images for objects at F and inside F.",
  ncert=NC + "'Ray Optics and Optical Instruments', reflection of light by spherical mirrors", seconds=45)

v_l = 1 / (F(1, 15) + F(1, -10))
assert v_l == -30 and v_l / F(-10) == 3
assert 1 / (F(1, 15) + F(1, 10)) == 6
q(OPT, "Refraction and lenses", "Intermediate", "numerical",
  "An object is placed 10 cm in front of a thin convex lens of focal length 15 cm. The image formed is:",
  *opt("30 cm from the lens on the same side as the object; virtual, erect and 3 times the size of the object",
       ["6 cm from the lens on the other side; real, inverted and 0.6 times the size of the object",
        "30 cm from the lens on the other side; real, inverted and 3 times the size of the object",
        "30 cm from the lens on the same side as the object; virtual, erect and 1/3 the size of the object"], "D"),
  "Thin lens formula 1/v − 1/u = 1/f and magnification m = v/u",
  "An object inside the focal length of a convex lens gives a virtual, erect, magnified image on the same side "
  "(the lens acts as a magnifier).",
  ["u = −10 cm, f = +15 cm", "1/v = 1/f + 1/u = 1/15 − 1/10 = −1/30 → v = −30 cm (same side as the object)",
   "m = v/u = (−30)/(−10) = +3 → virtual, erect, magnified 3 times"],
  why="'6 cm, other side' adds 1/15 and 1/10 (sign of u dropped). '30 cm on the other side, real' ignores the sign "
      "of v. '1/3 the size' takes m = u/v.",
  ncert=NC + "'Ray Optics and Optical Instruments', thin lens formula; magnification", seconds=50, rc=True)

A2_pr = (F(16, 10) - 1) * 5 / (F(3, 2) - 1)
assert A2_pr == 6 and (F(16, 10) - 1) * 5 == 3
close(0.5 * 5 / 0.6, 4.17)
close(5 * 1.6 / 1.5, 5.33)
q(OPT, "Prism", "Intermediate", "numerical",
  "A thin prism of refracting angle 5° made of glass of refractive index 1.6 is combined with a second thin prism "
  "of glass of refractive index 1.5, placed the other way round, so that a ray passing through both suffers no net "
  "deviation. The refracting angle of the second prism is:",
  *opt("6°", ["4.17°", "5.33°", "3°"], "B"),
  "Deviation by a thin prism: δ = (n − 1)A",
  "The inverted second prism deviates the ray the opposite way; for zero net deviation its deviation must equal "
  "that of the first.",
  ["δ₁ = (1.6 − 1) × 5° = 3°", "(1.5 − 1)A₂ = 3° → A₂ = 6°"],
  why="4.17° inverts the ratio of (n − 1) values. 5.33° uses the ratio of n instead of (n − 1). 3° is the "
      "deviation of the first prism, not the angle of the second.",
  ncert=NC + "'Ray Optics and Optical Instruments', refraction through a prism (thin prism)", seconds=50, rc=True)

beta = 600e-9 * 1 / 1e-3
close(beta, 0.6e-3)
close((5 - 1.5) * beta, 2.1e-3)
close((5 - 2.5) * beta, 1.5e-3)
close((5 - 2) * beta, 1.8e-3)
q(OPT, "Huygens' principle and interference", "Intermediate", "numerical",
  "In a Young's double-slit experiment the slits are 1 mm apart, the screen is 1 m away and light of wavelength "
  "600 nm is used. The distance between the second dark fringe and the fifth bright fringe, both on the same side of "
  "the central bright fringe, is:",
  *opt("2.1 mm", ["1.5 mm", "1.8 mm", "3.0 mm"], "C"),
  "Fringe positions in YDSE: bright y = nβ, dark y = (n − ½)β, with β = λD/d",
  "Count fringes in units of β from the central bright fringe. The first dark fringe is at β/2, the second at 3β/2.",
  ["β = λD/d = (600 × 10⁻⁹ × 1)/(1 × 10⁻³) = 0.6 mm", "Fifth bright: 5β = 3.0 mm; second dark: 1.5β = 0.9 mm",
   "Separation = 3.5β = 2.1 mm"],
  why="1.5 mm places the second dark fringe at 2.5β. 1.8 mm places it at 2β, as if it were a bright fringe. 3.0 mm "
      "is the distance of the fifth bright fringe from the centre.",
  ncert=NC + "'Wave Optics', interference of light waves and Young's experiment", seconds=70, rc=True)

iB = math.degrees(math.atan(math.sqrt(3)))
close(iB, 60)
r_B = math.degrees(math.asin(math.sin(math.radians(iB)) / math.sqrt(3)))
close(r_B, 30)
close(r_B, 90 - iB)
close(math.degrees(math.asin(1 / math.sqrt(3))), 35.26)
q(OPT, "Polarisation", "Intermediate", "numerical",
  "Unpolarised light falls on a plane glass surface (refractive index √3) at the angle of incidence for which the "
  "reflected light is completely plane polarised. The angle of refraction is:",
  *opt("30°", ["60°", "35.3°", "45°"], "D"),
  "Brewster's law: tan i_B = n",
  "At the Brewster angle the reflected light is completely polarised. Find i_B from tan i_B = n and then the "
  "refraction angle from Snell's law.",
  ["tan i_B = √3 → i_B = 60°", "sin r = sin 60°/√3 = (√3/2)/√3 = 1/2 → r = 30°",
   "Check: i_B + r = 90°"],
  why="60° is the angle of incidence, not of refraction. 35.3° is sin⁻¹(1/√3), the critical angle. 45° has no "
      "basis here.",
  ncert=NC + "'Wave Optics', polarisation by reflection", seconds=50, rc=True)

q(OPT, "Huygens' principle and interference", "Intermediate", "match_list",
  ml("For a Young's double-slit experiment (slit separation d, screen distance D, wavelength λ) and a single-slit "
     "diffraction experiment (slit width a), match List-I with List-II.",
     ["Fringe width in Young's experiment",
      "Distance of the nth bright fringe from the central bright fringe",
      "Path difference at the nth dark fringe (n = 1, 2, 3, ...)",
      "Angular position of the first minimum of the single-slit pattern (small angles)"],
     ["(n − ½)λ", "λ/a", "nλD/d", "λD/d"]),
  *mlo("A-IV, B-III, C-I, D-II",
       ["A-III, B-IV, C-I, D-II", "A-IV, B-III, C-II, D-I", "A-II, B-III, C-I, D-IV"], "A"),
  "Interference and diffraction formulae",
  "In YDSE, bright fringes are at y = nλD/d (path difference nλ) and dark fringes at path difference (n − ½)λ; the "
  "spacing is λD/d. For a single slit, the first minimum is at sin θ = λ/a.",
  ["A → λD/d (IV)", "B → nλD/d (III)", "C → (n − ½)λ (I)", "D → θ ≈ λ/a (II)"],
  why="The other codes swap the fringe width with the fringe position, or the dark-fringe condition with the "
      "single-slit minimum.",
  ncert=NC + "'Wave Optics', interference; diffraction at a single slit", seconds=45)

q(OPT, "Optical instruments", "Intermediate", "assertion_reason",
  ar("Objectives of large diameter are used in astronomical telescopes.",
     "A larger objective collects more light, so fainter objects can be seen, and it also gives a better resolving "
     "power."),
  AR, ar_key(True, True, True),
  "Light-gathering power and resolution of a telescope",
  "The light-gathering power depends on the area of the objective, and the ability to see two close objects "
  "separately (resolving power) also improves with the diameter of the objective. These two advantages are why "
  "large objectives are used. R explains A.",
  ["Light gathered ∝ (diameter)²", "Resolving power improves with diameter", "Both are reasons for large objectives"],
  why="R gives the very reasons for A, so B is wrong. Both statements are true, so C and D are wrong.",
  ncert=NC + "'Ray Optics and Optical Instruments', telescope", seconds=35)

q(OPT, "Mirrors", "Intermediate", "statement_pair",
  sp("The focal length of a spherical mirror changes when the mirror is immersed in water.",
     "A spherical mirror forms images free of chromatic aberration because its focal length does not depend on the "
     "wavelength of light."),
  SP, sp_key(False, True),
  "Focal length of a mirror: f = R/2",
  "A mirror works by reflection, and the law of reflection does not involve the refractive index of the medium or "
  "the wavelength. So f = R/2 is the same in water as in air, and the same for all colours, which is one advantage "
  "of reflecting telescopes.",
  ["f = R/2: depends only on the geometry → I false", "No dependence on λ → no chromatic aberration → II true"],
  why="Statement I is false (it would be true for a lens). Statement II is true, so B and C are wrong.",
  ncert=NC + "'Ray Optics and Optical Instruments', spherical mirrors; reflecting telescope", seconds=40)

mt = {"a": False, "b": True, "c": True, "d": False, "e": True}
q(OPT, "Optical instruments", "Intermediate", "multi_statement",
  ms("Which of the following statements about optical instruments are correct?",
     ["In an astronomical telescope, the focal length of the objective is smaller than that of the eyepiece.",
      "In a compound microscope, both the objective and the eyepiece are converging lenses.",
      "In a compound microscope, the objective forms a real, inverted and magnified image of the object.",
      "The final image formed by an astronomical refracting telescope is erect.",
      "In the normal adjustment of an astronomical telescope, the final image is formed at infinity."]),
  *mso(mt, "bce", ["abc", "cde", "abde"], "B"),
  "Compound microscope and astronomical telescope",
  "A telescope needs f_o ≫ f_e for large magnification (m = f_o/f_e), and its final image is inverted. In a "
  "microscope, two converging lenses are used; the objective forms a real, inverted, magnified intermediate image "
  "that the eyepiece magnifies further.",
  ["(a) false: f_o > f_e", "(b) true", "(c) true", "(d) false: the image is inverted", "(e) true"],
  why="Options containing (a) or (d) include a false statement.",
  ncert=NC + "'Ray Optics and Optical Instruments', optical instruments", seconds=55)

shift = 6 * (1 - F(2, 3))
assert shift == 2 and 6 / F(3, 2) == 4 and 6 * F(3, 2) == 9 and 6 * (F(3, 2) - 1) == 3
q(OPT, "Refraction and lenses", "Intermediate", "numerical",
  "A travelling microscope is focused on a mark on a table. A glass slab 6 cm thick, of refractive index 1.5, is "
  "then placed over the mark. To bring the mark back into focus, the microscope must be raised through:",
  *opt("2 cm", ["4 cm", "9 cm", "3 cm"], "B"),
  "Normal shift due to a slab: s = t(1 − 1/n)",
  "Seen through the slab, the mark appears raised by t(1 − 1/n), because the slab's thickness t appears as only t/n. "
  "The microscope must be raised by this apparent shift.",
  ["Apparent thickness of the slab = t/n = 6/1.5 = 4 cm", "Shift = t − t/n = 6 − 4 = 2 cm"],
  why="4 cm is the apparent thickness t/n, not the shift. 9 cm multiplies by n. 3 cm uses t(n − 1).",
  ncert=NC + "'Ray Optics and Optical Instruments', refraction (real and apparent depth)", seconds=45, rc=True)

u_r = F(80, 4)
v_r = 3 * u_r
f_r = 1 / (1 / v_r + 1 / u_r)
assert u_r + v_r == 80 and f_r == 15
q(OPT, "Refraction and lenses", "Advanced", "numerical",
  "A convex lens forms a real image, three times the size of the object, on a screen placed 80 cm from the object. "
  "The focal length of the lens is:",
  *opt("15 cm", ["60 cm", "20 cm", "30 cm"], "C"),
  "Lens formula with magnification for a real image: v = 3|u| and |u| + v = object–screen distance",
  "For a real image formed on a screen, object and image lie on opposite sides of the lens, so the distances add.",
  ["|u| + v = 80 and v = 3|u| → |u| = 20 cm, v = 60 cm", "1/f = 1/v − 1/u = 1/60 + 1/20 = 4/60 → f = 15 cm"],
  why="60 cm comes from treating the image as virtual (v − |u| = 80), which cannot be caught on a screen. 20 cm is "
      "the object distance. 30 cm takes f = v/2.",
  ncert=NC + "'Ray Optics and Optical Instruments', thin lens formula; magnification", seconds=70, rc=True)

phi = 2 * math.pi / 3
close(math.cos(phi / 2) ** 2, 0.25)
close(math.cos(math.pi / 6) ** 2, 0.75)
q(OPT, "Huygens' principle and interference", "Advanced", "numerical",
  "In a Young's double-slit experiment the two slits give waves of equal intensity, and the maximum intensity on "
  "the screen is I_max. At a point on the screen where the path difference between the two waves is λ/3, the "
  "intensity is:",
  *opt("I_max/4", ["3I_max/4", "I_max/2", "I_max/3"], "B"),
  "Resultant intensity of two coherent waves: I = 4I₀ cos²(φ/2), with φ = (2π/λ) × path difference",
  "With equal intensities I₀, the maximum is 4I₀, so I = I_max cos²(φ/2).",
  ["φ = (2π/λ)(λ/3) = 2π/3", "I = I_max cos²(π/3) = I_max × (1/2)² = I_max/4"],
  why="3I_max/4 uses φ = π/3 (cos²(π/6)), i.e. forgets the factor 2π. I_max/2 is the result for a path difference of "
      "λ/4. I_max/3 assumes the intensity falls in proportion to the path difference.",
  ncert=NC + "'Wave Optics', coherent and incoherent addition of waves", seconds=70, rc=True)

C_lim = 60 / 2
n_lim = 1 / math.sin(math.radians(C_lim))
close(n_lim, 2)
q(OPT, "Prism", "Advanced", "numerical",
  "A prism has a refracting angle of 60°. Light falls on one refracting face. For no light to emerge from the "
  "second refracting face, whatever the angle of incidence on the first face, the refractive index of the prism "
  "material must be at least:",
  *opt("2", ["√2", "1.5", "2/√3"], "D"),
  "Refraction through a prism: r₁ + r₂ = A, with r₁ at most equal to the critical angle C",
  "The largest possible r₁ (grazing incidence) is C, which makes r₂ = A − C as small as possible. If even this "
  "smallest r₂ is not less than C, every ray is totally reflected at the second face. So the condition is "
  "A − C ≥ C, i.e. A ≥ 2C.",
  ["r₂ = A − r₁ ≥ A − C", "No emergence for any i: A − C ≥ C → C ≤ A/2 = 30°", "n = 1/sin C ≥ 1/sin 30° = 2"],
  why="√2 corresponds to C = 45°, the limiting value for a 90° prism. 2/√3 corresponds to C = 60°, using A ≥ C "
      "instead of A ≥ 2C. 1.5 is just a typical value for glass.",
  ncert=NC + "'Ray Optics and Optical Instruments', refraction through a prism; total internal reflection",
  seconds=100, rc=True)

v_o = 25 - 5
u_o = 1 / (F(1, v_o) - F(1, 2))
assert u_o == F(-20, 9) and abs(v_o / u_o) == 9
assert abs(v_o / u_o) * 25 / 5 == 45
assert F(20 * 25, 2 * 5) == 50 and F(25 * 25, 2 * 5) == F(125, 2) and 9 * (1 + F(25, 5)) == 54
q(OPT, "Optical instruments", "Advanced", "numerical",
  "A compound microscope has an objective of focal length 2 cm and an eyepiece of focal length 5 cm, placed 25 cm "
  "apart. The microscope is adjusted so that the final image is at infinity. Taking the least distance of distinct "
  "vision as 25 cm, the magnifying power of the microscope is:",
  *opt("45", ["50", "62.5", "54"], "A"),
  "Compound microscope: m = m_o × m_e, with m_e = D/f_e for a final image at infinity",
  "For the final image at infinity, the objective's image must be at the focus of the eyepiece, which fixes v_o. "
  "The lens formula then gives u_o and the objective magnification.",
  ["v_o = 25 − 5 = 20 cm", "1/u_o = 1/20 − 1/2 = −9/20 → u_o = −20/9 cm", "m_o = v_o/u_o = −9 (magnitude 9)",
   "m_e = D/f_e = 25/5 = 5 → M = 9 × 5 = 45"],
  why="50 uses the approximation (L/f_o)(D/f_e) with L = 20 cm, and 62.5 the same with L = 25 cm; neither is exact "
      "here. 54 uses m_e = 1 + D/f_e, which applies when the final image is at the near point.",
  ncert=NC + "'Ray Optics and Optical Instruments', the compound microscope", seconds=110, rc=True)

q(OPT, "Diffraction", "Advanced", "assertion_reason",
  ar("Diffraction of light is easily observed around everyday objects such as doors and windows.",
     "Diffraction effects become noticeable when the size of the obstacle or aperture is comparable to the "
     "wavelength of the wave."),
  AR, ar_key(False, True),
  "When diffraction is noticeable",
  "The wavelength of visible light (about 0.4–0.7 µm) is tiny compared with doors and windows, so the bending of "
  "light round them is negligible and they cast sharp shadows. Diffraction of light becomes noticeable only with "
  "very small apertures or obstacles. A is false; R is true.",
  ["Door width ~ 1 m ≫ λ of light → negligible diffraction → A false", "R is the condition for marked diffraction → true"],
  why="A is false, so options A, B and C are wrong. (Sound, of wavelength ~ 1 m, does bend round doors — which is "
      "why A sounds plausible.)",
  ncert=NC + "'Wave Optics', diffraction", seconds=40)

q(OPT, "Diffraction", "Advanced", "statement_pair",
  sp("In an interference pattern, light energy is not destroyed at the dark fringes; it is redistributed, the "
     "intensity being greater than the sum of the separate intensities at the bright fringes.",
     "The first minimum of a single-slit diffraction pattern occurs where a sin θ = λ, which can be understood by "
     "dividing the slit into two halves whose corresponding points send waves with a path difference of λ/2."),
  SP, sp_key(True, True),
  "Energy in interference; the single-slit minimum",
  "With two equal coherent waves, the intensity varies between 0 and 4I₀, averaging 2I₀ = I₀ + I₀, so energy is "
  "conserved and only redistributed. For the single slit, at a sin θ = λ each point of the upper half pairs with a "
  "point of the lower half at a path difference λ/2, so the contributions cancel in pairs.",
  ["I ranges from 0 to 4I₀; average 2I₀ → Statement I true",
   "Halves of the slit cancel pairwise at a sin θ = λ → Statement II true"],
  why="Both statements are true, so every other option is wrong.",
  ncert=NC + "'Wave Optics', interference; diffraction at a single slit", seconds=50)

mt = {"a": True, "b": False, "c": True, "d": True, "e": False}
q(OPT, "Huygens' principle and interference", "Advanced", "multi_statement",
  ms("In a Young's double-slit experiment with monochromatic light, which of the following statements are correct?",
     ["The fringe width is directly proportional to the wavelength of the light used.",
      "If the two slits are illuminated by two sources of slightly different frequencies, a stationary fringe "
      "pattern is still obtained.",
      "Moving the screen farther from the slits does not change the angular separation of the fringes.",
      "The fringe width is inversely proportional to the separation of the slits.",
      "When the two slits give waves of equal intensity, the dark fringes are not completely dark."]),
  *mso(mt, "acd", ["abc", "bde", "acde"], "C"),
  "Young's double-slit experiment",
  "β = λD/d, so β ∝ λ and β ∝ 1/d; the angular separation β/D = λ/d does not depend on D. A stationary pattern "
  "needs coherent sources (a constant phase difference), which sources of different frequencies are not. With "
  "equal intensities, the minimum intensity is exactly zero.",
  ["(a) true", "(b) false: phase difference changes with time → pattern moves", "(c) true: angular width = λ/d",
   "(d) true", "(e) false: I_min = (√I₁ − √I₂)² = 0"],
  why="Options with (b) or (e) include a false statement.",
  ncert=NC + "'Wave Optics', interference of light waves and Young's experiment", seconds=70)

# ================================================================ Dual Nature of Matter and Radiation (B3 I4 A3)
lam0 = 1240 / 3.1
close(lam0, 400)
close(1240 * 3.1, 3844)
q(DUAL, "Photoelectric effect", "Basic", "numerical",
  "The work function of a metal is 3.1 eV. Taking hc = 1240 eV nm, the longest wavelength of light that can eject "
  "photoelectrons from it is:",
  *opt("400 nm", ["200 nm", "3844 nm", "4000 nm"], "D"),
  "Threshold wavelength: λ₀ = hc/φ₀",
  "Emission needs photon energy hc/λ ≥ φ₀, so the longest usable wavelength is the one with hc/λ = φ₀.",
  ["λ₀ = hc/φ₀ = 1240/3.1 = 400 nm"],
  why="200 nm halves the result for no reason. 3844 nm multiplies hc by φ₀ instead of dividing. 4000 nm is a "
      "power-of-ten slip (using 12400 eV nm, the value in eV Å, with nm).",
  ncert=NC + "'Dual Nature of Radiation and Matter', Einstein's photoelectric equation", seconds=30, rc=True)

h = 6.6e-34
lam_b = h / (6.6e-27 * 1e3)
close(lam_b, 1e-10)
close(h / 6.6e-27, 1e-7)
close(h / 6.6e-27 * 1e3, 1e-4)
close(6.6e-27 * 1e3 / h, 1e10)
q(DUAL, "de Broglie wavelength", "Basic", "numerical",
  "A particle of mass 6.6 × 10⁻²⁷ kg moves with a speed of 1.0 × 10³ m/s. Taking h = 6.6 × 10⁻³⁴ J s, its de "
  "Broglie wavelength is:",
  *opt("1.0 × 10⁻¹⁰ m", ["1.0 × 10⁻⁷ m", "1.0 × 10⁻⁴ m", "1.0 × 10¹⁰ m"], "A"),
  "de Broglie relation: λ = h/p = h/(mv)",
  "Every moving particle has an associated wavelength inversely proportional to its momentum.",
  ["p = mv = 6.6 × 10⁻²⁷ × 10³ = 6.6 × 10⁻²⁴ kg m/s", "λ = h/p = 6.6 × 10⁻³⁴/6.6 × 10⁻²⁴ = 1.0 × 10⁻¹⁰ m (1 Å)"],
  why="1.0 × 10⁻⁷ m leaves out the speed. 1.0 × 10⁻⁴ m multiplies h/m by v instead of dividing. 1.0 × 10¹⁰ m "
      "inverts the relation (p/h).",
  ncert=NC + "'Dual Nature of Radiation and Matter', wave nature of matter", seconds=30, rc=True)

q(DUAL, "Photoelectric effect", "Basic", "match_list",
  ml("Match each term of the photoelectric effect in List-I with its meaning in List-II.",
     ["Work function", "Threshold frequency", "Stopping potential", "Saturation current"],
     ["The photocurrent when all the emitted photoelectrons reach the collector",
      "The minimum energy an electron needs to escape from the metal surface",
      "The minimum frequency of the incident radiation for which photoelectrons are emitted",
      "The minimum negative potential of the collector, relative to the emitter, at which the photocurrent "
      "becomes zero"]),
  *mlo("A-II, B-III, C-IV, D-I",
       ["A-III, B-II, C-IV, D-I", "A-II, B-III, C-I, D-IV", "A-II, B-IV, C-III, D-I"], "B"),
  "Terms used in the photoelectric effect",
  "These are the standard NCERT definitions.",
  ["Work function φ₀ → II", "Threshold frequency ν₀ → III", "Stopping potential V₀ → IV", "Saturation current → I"],
  why="The other codes swap the work function with the threshold frequency, or the stopping potential with the "
      "saturation current.",
  ncert=NC + "'Dual Nature of Radiation and Matter', photoelectric effect; experimental study", seconds=40)

K1 = F(3, 2) - 1
K2 = 3 - 1
assert K2 / K1 == 4
q(DUAL, "Einstein's equation", "Intermediate", "numerical",
  "Light of frequency 1.5 times the threshold frequency of a metal falls on it. If the frequency of the light is "
  "doubled, the maximum kinetic energy of the photoelectrons becomes:",
  *opt("4 times its earlier value", ["2 times its earlier value", "√2 times its earlier value",
                                    "3 times its earlier value"], "B"),
  "Einstein's photoelectric equation: K_max = hν − hν₀",
  "K_max is a linear function of ν but not proportional to it, because of the work function term.",
  ["Before: K₁ = h(1.5ν₀) − hν₀ = 0.5hν₀", "After: K₂ = h(3ν₀) − hν₀ = 2hν₀", "K₂/K₁ = 2/0.5 = 4"],
  why="2 times assumes K_max ∝ ν. √2 times confuses K with speed. 3 times compares the new frequency with ν₀ "
      "instead of comparing the two kinetic energies.",
  ncert=NC + "'Dual Nature of Radiation and Matter', Einstein's photoelectric equation", seconds=50, rc=True)

E_ph = 4 * 1.6e-19
n_ph = 3.2e-3 / E_ph
close(n_ph, 5e15)
I_ph = 0.01 * n_ph * 1.6e-19
close(I_ph, 8e-6)
close(n_ph * 1.6e-19, 8e-4)
q(DUAL, "Photoelectric effect", "Intermediate", "numerical",
  "Monochromatic light whose photons each have energy 4.0 eV falls on a photosensitive surface with a power of "
  "3.2 mW. On average, one photoelectron is emitted for every 100 photons, and all emitted electrons are collected. "
  "Taking e = 1.6 × 10⁻¹⁹ C, the photocurrent is:",
  *opt("8 µA", ["0.8 mA", "80 µA", "0.8 µA"], "D"),
  "Photon flux = power/(energy per photon); photocurrent = (electrons per second) × e",
  "Each photon either ejects one electron or none, so the photocurrent is proportional to the number of photons "
  "arriving per second.",
  ["Energy per photon = 4.0 × 1.6 × 10⁻¹⁹ = 6.4 × 10⁻¹⁹ J",
   "Photons per second = 3.2 × 10⁻³/6.4 × 10⁻¹⁹ = 5 × 10¹⁵", "Electrons per second = 5 × 10¹³",
   "I = 5 × 10¹³ × 1.6 × 10⁻¹⁹ = 8 × 10⁻⁶ A = 8 µA"],
  why="0.8 mA assumes every photon ejects an electron. 80 µA uses 1 in 10. 0.8 µA uses 1 in 1000.",
  ncert=NC + "'Dual Nature of Radiation and Matter', photoelectric effect and the particle nature of light",
  seconds=70, rc=True)

q(DUAL, "Photoelectric effect", "Intermediate", "assertion_reason",
  ar("For light of a given frequency above the threshold, the maximum kinetic energy of the photoelectrons does not "
     "depend on the intensity of the light.",
     "Each photoelectron gets its energy from a single photon, and increasing the intensity increases the number of "
     "photons arriving per second without changing the energy of each photon."),
  AR, ar_key(True, True, True),
  "Photon picture of the photoelectric effect",
  "K_max = hν − φ₀ is set by the energy of one photon. More intense light of the same frequency means more photons "
  "per second, which raises the photocurrent but not the energy available to any one electron. R explains A.",
  ["One photon is absorbed by one electron", "Photon energy hν fixed by ν, not by intensity → K_max fixed"],
  why="R is the photon explanation of A, so B is wrong. Both statements are true, so C and D are wrong.",
  ncert=NC + "'Dual Nature of Radiation and Matter', effect of intensity of light on photocurrent; photon picture",
  seconds=40)

q(DUAL, "de Broglie wavelength", "Intermediate", "statement_pair",
  sp("The de Broglie wavelength of a moving macroscopic object, such as a thrown ball, is so small that its wave "
     "nature cannot be detected.",
     "When the speed of an electron (much less than the speed of light) is doubled, its de Broglie wavelength "
     "doubles."),
  SP, sp_key(True, False),
  "de Broglie wavelength λ = h/(mv)",
  "For a ball (m ~ 0.1 kg, v ~ 10 m/s), λ ~ 10⁻³⁴ m, far below anything measurable. λ is inversely proportional to "
  "the speed, so doubling the speed halves λ.",
  ["Large m → tiny λ → Statement I true", "λ ∝ 1/v → doubling v halves λ → Statement II false"],
  why="Statement II has the proportionality the wrong way round, so options A and D are wrong.",
  ncert=NC + "'Dual Nature of Radiation and Matter', wave nature of matter", seconds=35)

slope = (2.0 - 1.0) / (1.0e15 - 7.5e14)
h_m = 1.6e-19 * slope
nu0 = 7.5e14 - 1.0 / slope
close(slope, 4e-15)
close(h_m, 6.4e-34)
close(nu0, 5e14)
q(DUAL, "Einstein's equation", "Advanced", "numerical",
  "In a photoelectric experiment, the stopping potential is 1.0 V for light of frequency 7.5 × 10¹⁴ Hz and 2.0 V "
  "for light of frequency 1.0 × 10¹⁵ Hz. Taking e = 1.6 × 10⁻¹⁹ C, the value of Planck's constant obtained and the "
  "threshold frequency of the metal are:",
  *opt("6.4 × 10⁻³⁴ J s and 5.0 × 10¹⁴ Hz",
       ["4.0 × 10⁻¹⁵ J s and 5.0 × 10¹⁴ Hz", "6.4 × 10⁻³⁴ J s and 2.5 × 10¹⁴ Hz",
        "6.4 × 10⁻³⁴ J s and 7.5 × 10¹⁴ Hz"], "C"),
  "eV₀ = hν − hν₀: the V₀–ν graph is a straight line of slope h/e and intercept ν₀ on the frequency axis",
  "Two points on the line give the slope (h/e) and then the intercept.",
  ["Slope = ΔV₀/Δν = (2.0 − 1.0)/(1.0 × 10¹⁵ − 7.5 × 10¹⁴) = 4 × 10⁻¹⁵ V s",
   "h = e × slope = 1.6 × 10⁻¹⁹ × 4 × 10⁻¹⁵ = 6.4 × 10⁻³⁴ J s",
   "ν₀ = 7.5 × 10¹⁴ − 1.0/(4 × 10⁻¹⁵) = 7.5 × 10¹⁴ − 2.5 × 10¹⁴ = 5.0 × 10¹⁴ Hz"],
  why="4.0 × 10⁻¹⁵ J s is the slope h/e, not h. 2.5 × 10¹⁴ Hz is the frequency interval corresponding to 1 V, not "
      "the intercept. 7.5 × 10¹⁴ Hz is one of the given frequencies, at which V₀ is not zero.",
  ncert=NC + "'Dual Nature of Radiation and Matter', effect of frequency of incident radiation on stopping potential",
  seconds=100, rc=True)

K_e = 1240 / 200 - 2.2
close(K_e, 4.0)
close(1.227 / math.sqrt(K_e), 0.6135)
close(1.227 / math.sqrt(6.2), 0.4928)
close(1.227 / K_e, 0.307)
close(1.227 / math.sqrt(2.2), 0.827)
q(DUAL, "de Broglie wavelength", "Advanced", "numerical",
  "Ultraviolet light of wavelength 200 nm falls on a metal of work function 2.2 eV. Taking hc = 1240 eV nm and, for "
  "an electron of kinetic energy K (in eV), λ = 1.227/√K nm, the de Broglie wavelength of the fastest photoelectrons "
  "is about:",
  *opt("0.61 nm", ["0.49 nm", "0.31 nm", "0.83 nm"], "A"),
  "Einstein's equation followed by the de Broglie wavelength of an electron",
  "First find the maximum kinetic energy of the photoelectrons, then their de Broglie wavelength.",
  ["Photon energy = 1240/200 = 6.2 eV", "K_max = 6.2 − 2.2 = 4.0 eV", "λ = 1.227/√4.0 = 0.61 nm"],
  why="0.49 nm ignores the work function (uses K = 6.2 eV). 0.31 nm divides by K instead of √K. 0.83 nm uses the "
      "work function as the kinetic energy.",
  ncert=NC + "'Dual Nature of Radiation and Matter', Einstein's photoelectric equation; wave nature of matter",
  seconds=80, rc=True)

q(DUAL, "Photoelectric effect", "Advanced", "direct",
  "Which one of the following statements about photons is NOT correct?",
  *opt("In a collision between a photon and an electron, the number of photons is always conserved.",
       ["Photons are electrically neutral and are not deflected by electric or magnetic fields.",
        "A photon of frequency ν has energy hν and momentum hν/c.",
        "All photons of light of a given frequency have the same energy, whatever the intensity of the light."],
       "C"),
  "Photon picture of electromagnetic radiation",
  "In photon–particle collisions, total energy and total momentum are conserved, but the number of photons need not "
  "be: a photon may be absorbed or a new photon created. The other three statements are part of the photon picture.",
  ["Energy and momentum conserved in collisions", "Photon number NOT necessarily conserved (absorption, emission)"],
  why="The other three statements are correct, so they are not the answer to a 'NOT correct' question.",
  ncert=NC + "'Dual Nature of Radiation and Matter', particle nature of light: the photon", seconds=35)

# ================================================================ Atoms and Nuclei (B4 I5 A4)
E31 = 13.6 * (1 - F(1, 9))
close(E31, 12.09)
close(13.6 * (1 - 0.25), 10.2)
q(AN, "Bohr model and hydrogen spectrum", "Basic", "numerical",
  "Using E_n = −13.6/n² eV for the hydrogen atom, the energy of the photon emitted when the electron jumps from the "
  "n = 3 level to the n = 1 level is:",
  *opt("12.09 eV", ["1.51 eV", "10.2 eV", "13.6 eV"], "B"),
  "Bohr's frequency condition: hν = E_i − E_f",
  "The photon carries away the energy difference between the two levels.",
  ["E₃ = −13.6/9 = −1.51 eV, E₁ = −13.6 eV", "hν = −1.51 − (−13.6) = 12.09 eV"],
  why="1.51 eV is |E₃|, not the difference. 10.2 eV is for the n = 2 → 1 jump. 13.6 eV is the ionisation energy.",
  ncert=NC + "'Atoms', Bohr model of the hydrogen atom; energy levels", seconds=30, rc=True)

q(AN, "Bohr model and hydrogen spectrum", "Basic", "statement_pair",
  sp("The Balmer series of hydrogen lies entirely in the ultraviolet region.",
     "The lines of the Paschen series arise from transitions that end on the n = 2 level."),
  SP, sp_key(False, False),
  "Series of the hydrogen spectrum",
  "Balmer series lines end on n = 2; several of them (Hα, Hβ, ...) are in the visible region, with the series limit "
  "in the near ultraviolet. Paschen lines end on n = 3 and lie in the infrared.",
  ["Balmer: partly visible → Statement I false", "Paschen: ends on n = 3, not n = 2 → Statement II false"],
  why="Statement II describes the Balmer series, not the Paschen series. Statement I is false because the Balmer "
      "series is the visible series of hydrogen. So only option B fits.",
  ncert=NC + "'Atoms', atomic spectra; the line spectra of the hydrogen atom", seconds=30)

q(AN, "Binding energy", "Basic", "direct",
  "Which one of the following statements about the nuclear force between two nucleons is correct?",
  *opt("It becomes strongly repulsive when the nucleons are brought closer than about 0.8 fm.",
       ["It is a long-range force that falls off as the inverse square of the distance, like gravitation.",
        "It acts only between two protons.",
        "At a separation of about 1 fm it is weaker than the Coulomb force between two protons."], "C"),
  "Properties of the nuclear force",
  "The nuclear force is much stronger than the Coulomb force at nuclear distances, has a short range (a few fm), is "
  "nearly independent of charge (p–p, n–n and n–p alike), and is attractive beyond about 0.8 fm but strongly "
  "repulsive at smaller separations.",
  ["Attractive for r > 0.8 fm, repulsive for r < 0.8 fm"],
  why="It is short-ranged, not inverse-square; it acts between all pairs of nucleons; and at about 1 fm it is far "
      "stronger than the Coulomb force.",
  ncert=NC + "'Nuclei', nuclear force", seconds=25)

q(AN, "Nuclear size and mass defect", "Basic", "match_list",
  ml("Match each quantity in List-I with its approximate value in List-II.",
     ["Energy equivalent of 1 atomic mass unit",
      "R₀ in the nuclear radius formula R = R₀A^(1/3)",
      "Ionisation energy of a hydrogen atom in its ground state",
      "Radius of the first Bohr orbit of hydrogen"],
     ["13.6 eV", "931.5 MeV", "0.53 × 10⁻¹⁰ m", "1.2 × 10⁻¹⁵ m"]),
  *mlo("A-II, B-IV, C-I, D-III",
       ["A-II, B-III, C-I, D-IV", "A-I, B-IV, C-II, D-III", "A-IV, B-II, C-I, D-III"], "D"),
  "Order-of-magnitude constants of atomic and nuclear physics",
  "Atomic sizes are of order 10⁻¹⁰ m and atomic energies of order eV; nuclear sizes are of order 10⁻¹⁵ m and "
  "nuclear energies of order MeV.",
  ["1 u ↔ 931.5 MeV → II", "R₀ ≈ 1.2 fm → IV", "Hydrogen ionisation energy 13.6 eV → I",
   "Bohr radius 0.53 Å → III"],
  why="The other codes swap the atomic size (10⁻¹⁰ m) with the nuclear size constant (10⁻¹⁵ m), or the eV and MeV "
      "energies.",
  ncert=NC + "'Atoms', Bohr model; 'Nuclei', atomic masses; size of the nucleus", seconds=40)

dm_d = 1.007825 + 1.008665 - 2.014102
close(dm_d, 0.002388)
BE_d = dm_d * 931.5
close(BE_d, 2.224)
close(BE_d / 2, 1.112)
q(AN, "Binding energy", "Intermediate", "numerical",
  "Given the masses m(¹H) = 1.007825 u, m(neutron) = 1.008665 u and m(²H) = 2.014102 u (atomic masses), and "
  "1 u = 931.5 MeV/c², the binding energy of the deuteron is about:",
  *opt("2.22 MeV", ["1.11 MeV", "0.0024 MeV", "4.45 MeV"], "A"),
  "Binding energy = (mass defect) × c²",
  "Using atomic masses for ¹H and ²H is consistent: the electron masses cancel.",
  ["Δm = 1.007825 + 1.008665 − 2.014102 = 0.002388 u", "E_b = 0.002388 × 931.5 ≈ 2.22 MeV"],
  why="1.11 MeV is the binding energy per nucleon. 0.0024 MeV writes the mass defect in u as if it were MeV. "
      "4.45 MeV doubles the result.",
  ncert=NC + "'Nuclei', mass-energy and nuclear binding energy", seconds=50, rc=True)

v_ratio = F(3, 3)
assert v_ratio == 1
close(2.2e6 * 3, 6.6e6)
close(2.2e6 / 3, 7.3e5, rel=1e-2)
close(2.2e6 / 9, 2.4e5, rel=2e-2)
q(AN, "Bohr model and hydrogen spectrum", "Intermediate", "numerical",
  "In the Bohr model the speed of the electron in the ground state of hydrogen is 2.2 × 10⁶ m/s. The speed of the "
  "electron in the n = 3 orbit of a doubly ionised lithium ion (Li²⁺, Z = 3) is:",
  *opt("2.2 × 10⁶ m/s", ["6.6 × 10⁶ m/s", "7.3 × 10⁵ m/s", "2.4 × 10⁵ m/s"], "C"),
  "Bohr model for a hydrogen-like ion: v_n ∝ Z/n",
  "The electron's speed increases with nuclear charge and decreases with the orbit number: v_n = v₁(H) × Z/n.",
  ["v = 2.2 × 10⁶ × (Z/n) = 2.2 × 10⁶ × (3/3)", "= 2.2 × 10⁶ m/s, the same as in the ground state of hydrogen"],
  why="6.6 × 10⁶ m/s multiplies by Z but ignores n. 7.3 × 10⁵ m/s divides by n but ignores Z. 2.4 × 10⁵ m/s divides "
      "by n² (the energy dependence), not by n.",
  ncert=NC + "'Atoms', Bohr model of the hydrogen atom", seconds=45, rc=True)

R_H = 1.1e7
close(4 / R_H, 3.636e-7)
close(1 / R_H, 9.09e-8)
close(36 / (5 * R_H), 6.545e-7)
close(4 / (3 * R_H), 1.212e-7)
q(AN, "Bohr model and hydrogen spectrum", "Intermediate", "numerical",
  "Taking the Rydberg constant R = 1.1 × 10⁷ m⁻¹, the shortest wavelength in the Balmer series of hydrogen is about:",
  *opt("364 nm", ["91 nm", "655 nm", "121 nm"], "D"),
  "Balmer series: 1/λ = R(1/2² − 1/n²), n = 3, 4, 5, ...",
  "The shortest wavelength (series limit) corresponds to the largest energy gap, n → ∞.",
  ["1/λ_min = R(1/4 − 0) = R/4", "λ_min = 4/R = 4/(1.1 × 10⁷) m = 3.64 × 10⁻⁷ m ≈ 364 nm"],
  why="91 nm (1/R) is the Lyman series limit. 655 nm is the longest Balmer wavelength (n = 3 → 2). 121 nm is the "
      "first Lyman line.",
  ncert=NC + "'Atoms', the line spectra of the hydrogen atom", seconds=45, rc=True)

q(AN, "Bohr model and hydrogen spectrum", "Intermediate", "assertion_reason",
  ar("In the Bohr model, a hydrogen atom emits a photon only when its electron makes a transition from a higher "
     "energy orbit to a lower energy orbit.",
     "The energy of the photon emitted equals the difference between the energies of the initial and final states "
     "of the electron, hν = E_i − E_f."),
  AR, ar_key(True, True, True),
  "Bohr's third postulate (frequency condition)",
  "Electrons in stationary orbits do not radiate. Radiation occurs only in a transition, and the photon's energy "
  "must be the positive difference E_i − E_f; this is positive only for a jump to a lower level. R is why emission "
  "happens only in downward transitions.",
  ["hν = E_i − E_f > 0 only if E_i > E_f", "So emission accompanies a jump to a lower orbit"],
  why="R is the condition that makes A true, not an unrelated fact, so B is wrong. Both statements are true, so C "
      "and D are wrong.",
  ncert=NC + "'Atoms', Bohr model of the hydrogen atom (postulates)", seconds=40)

mt = {"a": True, "b": False, "c": True, "d": True, "e": False}
assert 14 - 6 == 16 - 8
q(AN, "Nuclear size and mass defect", "Intermediate", "multi_statement",
  ms("Which of the following statements are correct?",
     ["³₁H and ³₂He are isobars.",
      "The isotopes of an element have the same mass number.",
      "¹⁴₆C and ¹⁶₈O are isotones.",
      "One atomic mass unit is defined as 1/12 of the mass of an atom of ¹²C.",
      "The neutron was discovered by Rutherford."]),
  *mso(mt, "acd", ["abc", "bde", "acde"], "B"),
  "Composition of the nucleus; atomic mass unit",
  "Isotopes: same Z, different A. Isobars: same A. Isotones: same N = A − Z. The atomic mass unit is 1/12 of the "
  "mass of a ¹²C atom. The neutron was discovered by Chadwick (1932).",
  ["(a) both have A = 3 → isobars → true", "(b) isotopes have the same Z, different A → false",
   "(c) N = 14 − 6 = 8 and 16 − 8 = 8 → isotones → true", "(d) true", "(e) false: Chadwick"],
  why="Options with (b) or (e) include a false statement.",
  ncert=NC + "'Nuclei', atomic masses and composition of nucleus; discovery of neutron", seconds=55)

m_d2, m_he3, m_n = 2.014102, 3.016029, 1.008665
Q_dd = (2 * m_d2 - m_he3 - m_n) * 931.5
close(Q_dd, 3.27)
close(Q_dd / 2, 1.63, rel=5e-3)
close(Q_dd * 2, 6.54)
close((2 * m_d2 - m_he3 - m_n) * 1000, 3.51)
q(AN, "Fission and fusion", "Advanced", "numerical",
  "In the fusion reaction ²H + ²H → ³He + n, the masses are m(²H) = 2.014102 u, m(³He) = 3.016029 u and "
  "m(n) = 1.008665 u. Taking 1 u = 931.5 MeV/c², the energy released per reaction is about:",
  *opt("3.27 MeV", ["1.63 MeV", "6.54 MeV", "3.51 MeV"], "B"),
  "Q value of a nuclear reaction: Q = (mass of reactants − mass of products) × c²",
  "Energy is released because the products are lighter than the reactants.",
  ["Reactants: 2 × 2.014102 = 4.028204 u", "Products: 3.016029 + 1.008665 = 4.024694 u",
   "Δm = 0.003510 u → Q = 0.003510 × 931.5 ≈ 3.27 MeV"],
  why="1.63 MeV divides by two deuterons (energy per reacting nucleus). 6.54 MeV counts the energy twice. 3.51 MeV "
      "converts with 1 u = 1000 MeV.",
  ncert=NC + "'Nuclei', nuclear energy: nuclear fusion", seconds=70, rc=True)

lines = {(4, 2): 4 * (F(1, 4) - F(1, 16))}
assert lines[(4, 2)] == F(3, 4) == 1 - F(1, 4)
assert all(F(1, b ** 2) - F(1, a ** 2) != F(3, 4) for a, b in ((4, 2), (3, 2), (4, 1)))
q(AN, "Bohr model and hydrogen spectrum", "Advanced", "numerical",
  "In the Bohr model, the energy levels of a hydrogen-like ion are E_n = −13.6 Z²/n² eV. A photon emitted when a "
  "He⁺ ion (Z = 2) makes the transition n = 4 → n = 2 has the same wavelength as the photon emitted by a hydrogen "
  "atom in the transition:",
  *opt("n = 2 → n = 1", ["n = 4 → n = 2", "n = 3 → n = 2", "n = 4 → n = 1"], "D"),
  "Photon energy for a hydrogen-like ion: ΔE = 13.6 Z²(1/n_f² − 1/n_i²) eV",
  "Equal wavelengths mean equal photon energies. Compute the He⁺ energy and find the hydrogen transition with the "
  "same value.",
  ["He⁺: ΔE = 13.6 × 4 × (1/4 − 1/16) = 13.6 × 3/4 eV", "Hydrogen 2 → 1: ΔE = 13.6 × (1 − 1/4) = 13.6 × 3/4 eV ✓"],
  shortcut="Doubling both n and taking Z = 2 leaves Z²/n² unchanged, so He⁺ (4 → 2) matches H (2 → 1).",
  why="n = 4 → 2 in hydrogen gives 13.6 × 3/16 eV (Z² ignored). 3 → 2 gives 13.6 × 5/36 eV, and 4 → 1 gives "
      "13.6 × 15/16 eV.",
  ncert=NC + "'Atoms', Bohr model; the line spectra of the hydrogen atom", seconds=70, rc=True)

E_Li = 13.6 * 9
close(E_Li * (1 - F(1, 9)), 108.8)
close(E_Li * (1 - F(1, 4)), 91.8)
q(AN, "Bohr model and hydrogen spectrum", "Advanced", "numerical",
  "Using E_n = −13.6 Z²/n² eV, the minimum energy needed to raise a doubly ionised lithium ion (Li²⁺, Z = 3) from its "
  "ground state to its second excited state is:",
  *opt("108.8 eV", ["91.8 eV", "12.09 eV", "122.4 eV"], "C"),
  "Energy levels of a hydrogen-like ion; 'second excited state' means n = 3",
  "The ground state is n = 1, the first excited state n = 2 and the second excited state n = 3.",
  ["E₁ = −13.6 × 9 = −122.4 eV, E₃ = −122.4/9 = −13.6 eV", "ΔE = −13.6 − (−122.4) = 108.8 eV"],
  why="91.8 eV takes the second excited state as n = 2. 12.09 eV ignores Z (the hydrogen value). 122.4 eV is the "
      "ionisation energy of Li²⁺.",
  ncert=NC + "'Atoms', Bohr model of the hydrogen atom (energy levels)", seconds=60, rc=True)

mt = {"a": False, "b": True, "c": True, "d": False, "e": True}
q(AN, "Fission and fusion", "Advanced", "multi_statement",
  ms("Which of the following statements about nuclear binding energy, fission and fusion are correct?",
     ["Fusion of light nuclei takes place readily at low temperatures.",
      "The binding energy per nucleon is nearly constant for nuclei with mass numbers between about 30 and 170.",
      "The nearly constant binding energy per nucleon is explained by the short range of the nuclear force: a "
      "nucleon interacts mainly with its nearest neighbours (saturation).",
      "Present-day nuclear power reactors obtain their energy from controlled fusion.",
      "The fission of one ²³⁵U nucleus by a neutron releases energy of the order of 200 MeV."]),
  *mso(mt, "bce", ["abc", "cde", "bcde"], "A"),
  "Binding-energy curve, fission and fusion",
  "Fusion needs the nuclei to come within the range of the nuclear force against their Coulomb repulsion, which "
  "requires very high temperatures (thermonuclear fusion). Nuclear reactors run on controlled fission. The flat "
  "middle part of the binding-energy curve reflects the saturation of the short-range nuclear force.",
  ["(a) false: very high temperatures are needed", "(b) true", "(c) true",
   "(d) false: reactors use fission", "(e) true: about 200 MeV per fission"],
  why="Options with (a) or (d) include a false statement.",
  ncert=NC + "'Nuclei', mass-energy and nuclear binding energy; nuclear energy", seconds=60)

# ================================================================ Electronic Devices (B4 I6 A4)
q(ED, "Semiconductors", "Basic", "direct",
  "In the energy band diagram of an n-type silicon semiconductor (doped with a pentavalent impurity), the donor "
  "energy level lies:",
  *opt("slightly below the bottom of the conduction band",
       ["slightly above the top of the valence band", "in the middle of the band gap",
        "inside the conduction band"], "B"),
  "Energy bands of extrinsic semiconductors",
  "The fifth electron of a pentavalent dopant is only loosely bound. Its energy level E_D lies just below the "
  "conduction band, so a small amount of energy (about 0.01–0.05 eV) lifts it into the conduction band.",
  ["n-type: donor level E_D just below E_C", "p-type: acceptor level E_A just above E_V"],
  why="'Just above the valence band' is the acceptor level of a p-type semiconductor. The donor level is neither "
      "at mid-gap nor inside the conduction band.",
  ncert=NC + "'Semiconductor Electronics', extrinsic semiconductor", seconds=25)

lam_pd = 1240 / 2.5
close(lam_pd, 496)
close(1240 * 2.5, 3100)
q(ED, "LED, photodiode and solar cell", "Basic", "numerical",
  "A photodiode is made of a semiconductor with a band gap of 2.5 eV. Taking hc = 1240 eV nm, the longest "
  "wavelength of light it can detect is about:",
  *opt("496 nm", ["248 nm", "3100 nm", "4960 nm"], "D"),
  "Detection condition for a photodiode: hν ≥ E_g, i.e. λ ≤ hc/E_g",
  "Light is detected only if each photon can create an electron–hole pair, which needs at least the band-gap energy.",
  ["λ_max = hc/E_g = 1240/2.5 = 496 nm"],
  why="248 nm halves the result. 3100 nm multiplies hc by E_g instead of dividing. 4960 nm is a power-of-ten slip.",
  ncert=NC + "'Semiconductor Electronics', optoelectronic junction devices: photodiode", seconds=30, rc=True)

q(ED, "Logic gates", "Basic", "match_list",
  ml("Match each logic gate in List-I with its Boolean expression in List-II (inputs A and B).",
     ["OR", "AND", "NAND", "NOT (input A)"],
     ["Ā", "A + B", "NOT (A · B)", "A · B"]),
  *mlo("A-II, B-IV, C-III, D-I",
       ["A-IV, B-II, C-III, D-I", "A-II, B-III, C-IV, D-I", "A-II, B-IV, C-I, D-III"], "A"),
  "Basic logic gates",
  "OR gives A + B, AND gives A·B, NAND is AND followed by NOT, and NOT inverts its single input.",
  ["OR → A + B (II)", "AND → A·B (IV)", "NAND → NOT(A·B) (III)", "NOT → Ā (I)"],
  why="The other codes swap OR with AND, or AND with NAND.", seconds=30)

q(ED, "Semiconductors", "Basic", "statement_pair",
  sp("For a semiconductor, the energy band gap is greater than 3 eV.",
     "A pure (intrinsic) semiconductor behaves as an insulator at 0 K."),
  SP, sp_key(False, True),
  "Band gaps of insulators and semiconductors",
  "NCERT classifies materials with E_g > 3 eV as insulators and those with E_g < 3 eV as semiconductors (Si about "
  "1.1 eV, Ge about 0.7 eV). At 0 K no electron has the energy to cross the gap of an intrinsic semiconductor, so "
  "the conduction band is empty and it does not conduct.",
  ["E_g > 3 eV describes an insulator → Statement I false", "At 0 K, no carriers → insulator → Statement II true"],
  why="Statement I is false and Statement II true, so only option D fits.",
  ncert=NC + "'Semiconductor Electronics', classification of metals, conductors and semiconductors; intrinsic "
             "semiconductor", seconds=30)

I_d = (5 - 0.7) / 1000
close(I_d, 4.3e-3)
q(ED, "p-n junction diode and rectifier", "Intermediate", "numerical",
  "A silicon diode is connected in series with a 1 kΩ resistor across a 5 V DC supply so that the diode is forward "
  "biased. Treating the diode as having a constant forward voltage drop of 0.7 V when it conducts, the current in the "
  "circuit is:",
  *opt("4.3 mA", ["5.0 mA", "5.7 mA", "zero"], "A"),
  "Diode with a constant forward drop: I = (V − V_D)/R",
  "Once the diode conducts, its voltage stays at about 0.7 V; the rest of the supply voltage appears across the "
  "resistor.",
  ["Voltage across resistor = 5 − 0.7 = 4.3 V", "I = 4.3 V/1 kΩ = 4.3 mA"],
  why="5.0 mA ignores the diode drop. 5.7 mA adds the drop. Zero would be the answer for reverse bias.",
  ncert=NC + "'Semiconductor Electronics', p-n junction diode under forward bias", seconds=40, rc=True)

n_si = 5e28
close(n_si * 1e-6, 5e22)
q(ED, "Semiconductors", "Intermediate", "numerical",
  "Pure silicon contains 5 × 10²⁸ atoms per m³ and has an intrinsic carrier concentration of 1.5 × 10¹⁶ m⁻³. It is "
  "doped with arsenic at a concentration of 1 ppm (one arsenic atom per million silicon atoms). Assuming every "
  "arsenic atom donates one free electron, the concentration of free electrons is about:",
  *opt("5 × 10²² m⁻³", ["5 × 10²⁸ m⁻³", "5 × 10¹⁶ m⁻³", "1.5 × 10¹⁶ m⁻³"], "B"),
  "Doping: donor concentration N_D = (fraction) × (atoms per m³); n_e ≈ N_D ≫ n_i",
  "One part per million of 5 × 10²⁸ atoms is 5 × 10²² donor atoms per m³. This is a million times the intrinsic "
  "concentration, so the thermally generated electrons are negligible.",
  ["N_D = 10⁻⁶ × 5 × 10²⁸ = 5 × 10²² m⁻³", "n_e ≈ N_D = 5 × 10²² m⁻³ (n_i = 1.5 × 10¹⁶ m⁻³ is negligible)"],
  why="5 × 10²⁸ m⁻³ is the number of silicon atoms. 5 × 10¹⁶ m⁻³ uses one part per billion. 1.5 × 10¹⁶ m⁻³ is the "
      "intrinsic concentration, which doping greatly exceeds.",
  ncert=NC + "'Semiconductor Electronics', extrinsic semiconductor", seconds=45, rc=True)

NAND = lambda a, b: 1 - (a & b)
OR = lambda a, b: a | b
truth = [NAND(a, b) & OR(a, b) for a, b in ((0, 0), (0, 1), (1, 0), (1, 1))]
assert truth == [0, 1, 1, 0]
q(ED, "Logic gates", "Intermediate", "direct",
  "Inputs A and B are fed both to a NAND gate and to an OR gate, and the outputs of these two gates are fed to an "
  "AND gate, whose output is Y. For the inputs (A, B) = (0, 0), (0, 1), (1, 0), (1, 1), the outputs Y are, in order:",
  *opt("0, 1, 1, 0", ["1, 0, 0, 1", "0, 0, 0, 1", "0, 1, 1, 1"], "C"),
  "Truth tables of combined logic gates",
  "Work out the NAND and OR outputs for each input pair, then AND them.",
  ["NAND: 1, 1, 1, 0", "OR: 0, 1, 1, 1", "Y = NAND · OR: 0, 1, 1, 0"],
  why="1, 0, 0, 1 is the complement of the correct result. 0, 0, 0, 1 is the AND gate alone. 0, 1, 1, 1 is the OR "
      "gate alone.",
  seconds=60)

E_dep = 0.6 / 1e-6
close(E_dep, 6e5)
close(0.6 / 1e-3, 6e2)
q(ED, "p-n junction diode and rectifier", "Intermediate", "numerical",
  "The barrier potential of a p-n junction is 0.6 V and the width of its depletion region is 1 µm. Treating the "
  "field in the depletion region as uniform, its magnitude is:",
  *opt("6 × 10⁵ V/m", ["6 × 10⁻⁷ V/m", "1.7 × 10⁻⁶ V/m", "6 × 10² V/m"], "C"),
  "Uniform field: E = V/d",
  "The barrier potential is set up across the depletion region; dividing by its width gives the average field.",
  ["d = 1 µm = 1 × 10⁻⁶ m", "E = 0.6/(1 × 10⁻⁶) = 6 × 10⁵ V/m"],
  why="6 × 10⁻⁷ V/m multiplies V by d. 1.7 × 10⁻⁶ V/m is d/V. 6 × 10² V/m takes 1 µm as 10⁻³ m.",
  ncert=NC + "'Semiconductor Electronics', p-n junction formation", seconds=30, rc=True)

q(ED, "LED, photodiode and solar cell", "Intermediate", "assertion_reason",
  ar("The semiconductor used to make a light emitting diode that emits visible light must have a band gap of at "
     "least about 1.8 eV.",
     "Light emitting diodes have a long life and can be switched on and off very quickly."),
  AR, ar_key(True, True, False),
  "LED: band gap and advantages",
  "Visible light spans about 0.4–0.7 µm, i.e. photon energies of about 3 eV down to 1.8 eV. Since the photon "
  "energy is set by the band gap, a visible LED needs E_g of at least about 1.8 eV. R lists true advantages of LEDs "
  "over incandescent lamps (long life, fast on–off switching), but these have nothing to do with the band gap "
  "needed for visible emission.",
  ["A: λ ≤ 0.7 µm → hν ≥ 1.24/0.7 ≈ 1.8 eV → true", "R: true (NCERT lists these advantages)",
   "R does not explain A → option B"],
  why="Option A would need R to give the reason for the 1.8 eV requirement; it does not. Both statements are true, "
      "so C and D are wrong.",
  ncert=NC + "'Semiconductor Electronics', light emitting diode", seconds=40)

q(ED, "LED, photodiode and solar cell", "Intermediate", "statement_pair",
  sp("The I–V characteristic of a solar cell is drawn in the fourth quadrant of the coordinate axes because a solar "
     "cell does not draw current but supplies it to the load.",
     "Semiconductors with a band gap close to 1.5 eV are ideal materials for making solar cells."),
  SP, sp_key(True, True),
  "Solar cell characteristics and materials",
  "A solar cell is a source: under illumination it drives current through the load, so its I–V curve lies in the "
  "fourth quadrant. The solar spectrum peaks near 1.5 eV, so materials with E_g close to 1.5 eV (such as Si and "
  "GaAs) absorb a large part of it.",
  ["Supplies current → fourth quadrant → Statement I true", "E_g ≈ 1.5 eV matches the solar spectrum → Statement II true"],
  why="Both statements are true, so every other option is wrong.",
  ncert=NC + "'Semiconductor Electronics', solar cell", seconds=35)

V_s, R_s = 10, 1000
I_ge = (V_s - 0.3) / R_s
close(I_ge, 9.7e-3)
assert 0.3 < 0.7  # the silicon diode, with only 0.3 V across it, stays off
q(ED, "p-n junction diode and rectifier", "Advanced", "numerical",
  "A silicon diode and a germanium diode are connected in parallel, both forward biased, and the combination is "
  "connected in series with a 1 kΩ resistor across a 10 V DC supply. Model each diode as non-conducting below its "
  "cut-in voltage and as having a constant drop equal to that voltage when it conducts (0.7 V for silicon, 0.3 V for "
  "germanium). The current from the supply and the way it divides are:",
  *opt("9.7 mA, all of it through the germanium diode",
       ["9.3 mA, all of it through the silicon diode", "10 mA, shared equally by the two diodes",
        "4.85 mA through each diode"], "A"),
  "Diodes in parallel: the one with the lower cut-in voltage conducts first and clamps the voltage",
  "As the voltage across the pair rises, the germanium diode starts conducting at 0.3 V and holds the voltage "
  "there. The silicon diode then never reaches its 0.7 V cut-in voltage, so it carries no current.",
  ["Voltage across the parallel pair = 0.3 V (germanium conducts)", "Silicon: 0.3 V < 0.7 V → off",
   "I = (10 − 0.3)/1000 = 9.7 mA, all through germanium"],
  why="9.3 mA assumes the silicon diode conducts, but it cannot reach 0.7 V while the germanium diode holds 0.3 V. "
      "Equal sharing (and 4.85 mA each) assumes identical diodes. 10 mA also ignores the diode drop.",
  ncert=NC + "'Semiconductor Electronics', p-n junction diode; V-I characteristics", seconds=80, rc=True)

NOR = lambda a, b: 1 - (a | b)
NOT = lambda a: 1 - a
AND = lambda a, b: a & b
pairs = ((0, 0), (0, 1), (1, 0), (1, 1))
assert all(NOR(a, a) == NOT(a) for a in (0, 1))
assert all(NOT(NAND(a, b)) == AND(a, b) for a, b in pairs)
assert all(NOT(NOR(a, b)) == OR(a, b) for a, b in pairs)
assert all(OR(NOT(a), NOT(b)) == NAND(a, b) for a, b in pairs)
q(ED, "Logic gates", "Advanced", "match_list",
  ml("Match each combination of gates in List-I with the single gate it is equivalent to in List-II.",
     ["A NOR gate with both its inputs joined together", "A NAND gate followed by a NOT gate",
      "A NOR gate followed by a NOT gate",
      "Each of the inputs A and B passed through a NOT gate, and the two outputs fed to an OR gate"],
     ["AND", "OR", "NOT", "NAND"]),
  *mlo("A-III, B-I, C-II, D-IV",
       ["A-III, B-II, C-I, D-IV", "A-IV, B-I, C-II, D-III", "A-III, B-IV, C-II, D-I"], "D"),
  "Equivalent logic circuits",
  "Check each combination with a truth table (or Boolean algebra).",
  ["NOR(A, A) = NOT(A + A) = Ā → NOT (III)", "NOT(NAND) = A·B → AND (I)", "NOT(NOR) = A + B → OR (II)",
   "Ā + B̄ = NOT(A·B) → NAND (IV)"],
  why="The other codes swap AND and OR (B and C) or NAND with AND.", seconds=70)

mt = {"a": True, "b": False, "c": True, "d": True, "e": False}
q(ED, "p-n junction diode and rectifier", "Advanced", "multi_statement",
  ms("Which of the following statements about a p-n junction are correct?",
     ["During the formation of the junction, diffusion of majority carriers across it leaves behind immobile ions, "
      "forming the depletion region.",
      "The depletion region contains a large number of mobile charge carriers.",
      "In equilibrium with no bias, the diffusion current across the junction is equal and opposite to the drift "
      "current.",
      "Under reverse bias, the potential barrier across the junction increases.",
      "Under forward bias, the current is mainly due to the drift of minority carriers."]),
  *mso(mt, "acd", ["ab", "cde", "abcd"], "B"),
  "Formation and biasing of a p-n junction",
  "Diffusion of electrons and holes uncovers fixed donor and acceptor ions; this region is depleted of mobile "
  "carriers. The field of these ions drives a drift current that, in equilibrium, cancels the diffusion current. "
  "Reverse bias adds to the barrier (V₀ + V); forward bias lowers it, and the large forward current is due to "
  "diffusion of majority carriers.",
  ["(a) true", "(b) false: it is depleted of mobile carriers", "(c) true", "(d) true",
   "(e) false: forward current is mainly majority-carrier diffusion"],
  why="Options with (b) or (e) contain a false statement; 'abcd' also includes (b).",
  ncert=NC + "'Semiconductor Electronics', p-n junction; semiconductor diode", seconds=70)

mt = {"a": False, "b": True, "c": True, "d": False, "e": True}
q(ED, "LED, photodiode and solar cell", "Advanced", "multi_statement",
  ms("Which of the following statements about optoelectronic junction devices are correct?",
     ["Compared with incandescent lamps, LEDs need more power and have a shorter life.",
      "The current in a reverse-biased photodiode increases with the intensity of the light falling on it.",
      "An LED emits light when electrons and holes recombine near the junction under forward bias.",
      "A photodiode can detect light whose photon energy is less than the band gap of its semiconductor.",
      "The working of a solar cell involves generation of electron–hole pairs by light, their separation by the "
      "junction field, and their collection at the contacts."]),
  *mso(mt, "bce", ["abc", "cde", "bcde"], "D"),
  "LED, photodiode and solar cell",
  "LEDs work at low voltage and power and have long life. A photodiode under reverse bias gives a current "
  "proportional to the light intensity, but only for photons of energy above E_g. A solar cell works by "
  "generation, separation and collection of light-produced carriers.",
  ["(a) false", "(b) true", "(c) true", "(d) false: hν must exceed E_g", "(e) true"],
  why="Options with (a) or (d) contain a false statement.",
  ncert=NC + "'Semiconductor Electronics', optoelectronic junction devices", seconds=60)

# ================================================================ Experimental Skills (B2 I3 A2)
q(EXP, "Mechanics experiments", "Basic", "match_list",
  ml("Match each piece of apparatus or method in List-I with the quantity it is used to determine in List-II.",
     ["Searle's apparatus", "Travelling microscope (real and apparent thickness of a slab)",
      "Half-deflection method", "Metre scale balanced on a knife edge (principle of moments)"],
     ["Mass of a given body", "Young's modulus of the material of a wire", "Resistance of a galvanometer",
      "Refractive index of glass"]),
  *mlo("A-II, B-IV, C-III, D-I",
       ["A-IV, B-II, C-III, D-I", "A-II, B-IV, C-I, D-III", "A-III, B-IV, C-II, D-I"], "B"),
  "Experiments in the NEET practical list",
  "Searle's apparatus measures the extension of a wire under load (Young's modulus). A travelling microscope finds "
  "real and apparent thicknesses (n = real/apparent). The half-deflection method gives a galvanometer's "
  "resistance. A metre scale balanced on a knife edge uses moments to find an unknown mass.",
  ["A → II", "B → IV", "C → III", "D → I"],
  why="The other codes swap the elastic and optical experiments, or the electrical and mechanical ones.",
  seconds=40)

L_p = (98.5 + 3.0 / 2) / 100
T_p2 = 2 * math.pi * math.sqrt(L_p / math.pi ** 2)
close(T_p2, 2.00)
close(2 * math.sqrt(0.985), 1.985)
close(2 * math.sqrt(1.015), 2.015)
q(EXP, "Mechanics experiments", "Basic", "numerical",
  "In a simple pendulum experiment, the length of the string from the point of suspension to the top of the bob is "
  "98.5 cm and the diameter of the spherical bob is 3.0 cm. Taking g = π² m/s², the time period of the pendulum is:",
  *opt("2.00 s", ["1.98 s", "2.01 s", "1.00 s"], "C"),
  "Simple pendulum: T = 2π√(L/g), with L measured to the centre of the bob",
  "The effective length is the string length plus the radius of the bob.",
  ["L = 98.5 + 1.5 = 100.0 cm = 1.000 m", "T = 2π√(1/π²) = 2π/π = 2.00 s"],
  why="1.98 s uses the string length alone. 2.01 s adds the whole diameter instead of the radius. 1.00 s drops the "
      "factor 2 from 2π.",
  seconds=45, rc=True)

LC_v = 0.1
zero_err = 3 * LC_v
reading = 31 + 7 * LC_v
close(reading - zero_err, 31.4)
close(reading + zero_err, 32.0)
close(31 - 7 * LC_v + 0.0, 30.3)
q(EXP, "Vernier calipers and screw gauge", "Intermediate", "numerical",
  "A vernier calipers has 10 vernier divisions equal to 9 main-scale divisions of 1 mm each. With the jaws closed, the "
  "zero of the vernier is to the right of the main-scale zero and the 3rd vernier division coincides with a "
  "main-scale division. When a rod is held between the jaws, the main-scale reading is 3.1 cm and the 7th vernier "
  "division coincides. The corrected diameter of the rod is:",
  *opt("3.14 cm", ["3.20 cm", "3.17 cm", "3.03 cm"], "D"),
  "Vernier reading = MSR + (coinciding division × least count) − zero error",
  "A vernier zero to the right of the main zero means a positive zero error, which must be subtracted from every "
  "reading.",
  ["Least count = 1 MSD − 1 VSD = 1 mm − 0.9 mm = 0.1 mm", "Zero error = +3 × 0.1 = +0.3 mm",
   "Observed = 31 mm + 7 × 0.1 mm = 31.7 mm", "Corrected = 31.7 − 0.3 = 31.4 mm = 3.14 cm"],
  why="3.20 cm adds the zero error instead of subtracting it. 3.17 cm ignores the zero error. 3.03 cm subtracts "
      "the vernier reading from the main-scale reading.",
  seconds=70, rc=True)

s_metal = 0.20 * 4200 * (30 - 20) / (0.20 * (100 - 30))
assert s_metal == 600
assert 0.15 * 4200 * 10 / (0.20 * 70) == 450
assert 0.20 * 4200 * 10 / (0.20 * 80) == 525
close(0.10 * 4200 * 10 / (0.20 * 70), 300)
q(EXP, "Thermal and fluid experiments", "Intermediate", "numerical",
  "In a method-of-mixtures experiment, 200 g of a metal at 100 °C is dropped into 150 g of water at 20 °C contained "
  "in a calorimeter whose water equivalent is 50 g. The final steady temperature is 30 °C. Taking the specific heat "
  "of water as 4200 J kg⁻¹ K⁻¹ and neglecting heat losses, the specific heat of the metal is:",
  *opt("600 J kg⁻¹ K⁻¹", ["450 J kg⁻¹ K⁻¹", "525 J kg⁻¹ K⁻¹", "300 J kg⁻¹ K⁻¹"], "A"),
  "Principle of calorimetry: heat lost by the hot body = heat gained by the water and calorimeter",
  "The calorimeter absorbs heat as if it were 50 g of extra water, so the effective mass of water is 200 g.",
  ["Heat gained = (0.150 + 0.050) × 4200 × (30 − 20) = 8400 J", "Heat lost = 0.200 × s × (100 − 30) = 14s",
   "s = 8400/14 = 600 J kg⁻¹ K⁻¹"],
  why="450 J kg⁻¹ K⁻¹ ignores the calorimeter. 525 J kg⁻¹ K⁻¹ uses a fall of 80 K (to 20 °C) for the metal. "
      "300 J kg⁻¹ K⁻¹ subtracts the water equivalent instead of adding it.",
  seconds=80, rc=True)

q(EXP, "Vernier calipers and screw gauge", "Intermediate", "statement_pair",
  sp("The least count of a screw gauge is equal to its pitch divided by the number of divisions on its circular "
     "scale.",
     "Backlash error in a screw gauge is avoided by always turning the screw in the same direction while taking "
     "readings."),
  SP, sp_key(True, True),
  "Screw gauge: least count and backlash",
  "One full turn advances the spindle by the pitch, and one circular division by pitch/N, the least count. Wear in "
  "the threads lets the screw turn slightly without moving the spindle when the direction of turning is reversed "
  "(backlash); turning in one direction only avoids it.",
  ["LC = pitch/N → Statement I true", "Backlash appears on reversing; turn one way only → Statement II true"],
  why="Both statements are true, so every other option is wrong.", seconds=35)

T_st = 0.5e-3 * 0.03 * 1000 * 10 / 2
close(T_st, 0.075)
close(1.0e-3 * 0.03 * 1000 * 10 / 2, 0.15)
close(0.5e-3 * 0.3 * 1000 * 10 / 2, 0.75)
q(EXP, "Thermal and fluid experiments", "Advanced", "numerical",
  "In an experiment to measure the surface tension of water by capillary rise, water rises to a height of 3.0 cm in a "
  "clean glass capillary tube of internal diameter 1.0 mm. Taking the angle of contact as zero, the density of water "
  "as 1000 kg/m³ and g = 10 m/s², the surface tension of water is:",
  *opt("0.075 N/m", ["0.15 N/m", "0.0375 N/m", "0.75 N/m"], "B"),
  "Capillary rise: h = 2S cos θ/(rρg), so S = rhρg/(2 cos θ)",
  "Use the radius (half the internal diameter) and θ = 0 for clean glass and water.",
  ["r = 0.5 mm = 5 × 10⁻⁴ m, h = 0.030 m",
   "S = (5 × 10⁻⁴ × 0.030 × 1000 × 10)/2 = 0.15/2 = 0.075 N/m"],
  why="0.15 N/m uses the diameter as the radius. 0.0375 N/m divides by 4 instead of 2. 0.75 N/m takes 3.0 cm as "
      "0.3 m.",
  ncert="Class 11 Physics, 'Mechanical Properties of Fluids', capillary rise", seconds=60, rc=True)

q(EXP, "Mechanics experiments", "Advanced", "assertion_reason",
  ar("In the resonance-tube experiment, the speed of sound can be found from the first two resonance lengths l₁ and "
     "l₂ as v = 2f(l₂ − l₁), without knowing the end correction.",
     "For a tube closed at one end, the lengths of air column at successive resonances differ by λ/4."),
  AR, ar_key(True, False),
  "Resonance tube: eliminating the end correction",
  "With end correction e, the first two resonances satisfy l₁ + e = λ/4 and l₂ + e = 3λ/4. Subtracting removes e: "
  "l₂ − l₁ = λ/2, so v = fλ = 2f(l₂ − l₁). Successive resonance lengths therefore differ by λ/2, not λ/4. A is "
  "true; R is false.",
  ["l₁ + e = λ/4, l₂ + e = 3λ/4", "l₂ − l₁ = λ/2 → v = 2f(l₂ − l₁) → A true", "Difference is λ/2 → R false"],
  why="R is false (λ/4 is the length of the first resonance column including the end correction), so options A, "
      "B and D are wrong.",
  ncert="Class 11 Physics, 'Waves', standing waves in a pipe closed at one end", seconds=55)


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
    assert all(28 <= keys[k] <= 33 for k in LETTERS), keys
    texts = [x["question_text"] for x in QS]
    assert len(set(texts)) == len(texts)
    doc = {"schema_version": "1.0", "batch_id": "BATCH_002", "created_at": TODAY,
           "notes": "Package PHY_002_p2: 122 original Physics questions (Current Electricity to Experimental Skills), "
                    "NEET_PHY_000379..000500. Numerical answers recomputed by tools/batch_002/PHY_002_p2.py.",
           "stimuli": [], "questions": QS}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {OUT}: {len(QS)} questions")
    print("difficulty", dict(Counter(x["difficulty"] for x in QS)))
    print("formats", dict(fmts))
    print("keys", dict(sorted(keys.items())))


if __name__ == "__main__":
    main()
