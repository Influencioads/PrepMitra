"""Builder for batches/parts/BATCH_007_PHY_p2.json (package PHY_007_p2 of BATCH_007).

Physics, 121 original questions, NEET_PHY_001630..NEET_PHY_001750: Current Electricity, Magnetic Effects of Current
and Magnetism, Electromagnetic Induction and Alternating Currents, Electromagnetic Waves, Optics, Dual Nature of
Matter and Radiation, Atoms and Nuclei, Electronic Devices, Experimental Skills.

Every numerical answer is recomputed below with an assert next to its question; multi-statement, assertion-reason
and statement-pair keys are derived from truth tables; the plan quota, format mix and answer-key balance are
asserted before anything is written. If any assert fails, nothing is written.

    python tools/batch_007/PHY_007_p2.py        (run from docs/neet-bank)
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
PLAN = ROOT / "batches" / "plans" / "BATCH_007_plan.json"
OUT = ROOT / "batches" / "parts" / "BATCH_007_PHY_p2.json"
PACKAGE = "PHY_007_p2"
FIRST_ID = 1630
COUNT = 121

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
rad, deg = math.radians, math.degrees


# ================================================================ Current Electricity (B6 I8 A6)
CEC = NC + "'Current Electricity', "

# ---- Basic
eps_g, isc_g = 2.0, 4.0
r_g = eps_g / isc_g
close(r_g, 0.5)
close(isc_g / eps_g, 2.0)
close(eps_g * isc_g, 8.0)
q(CE, "Cells, emf and internal resistance", "Basic", "numerical",
  "For a cell, the graph of the potential difference V across its terminals (y-axis) against the current I drawn "
  "from it (x-axis) is a straight line that cuts the V-axis at 2.0 V and the I-axis at 4.0 A. The internal "
  "resistance of the cell is:",
  *opt("0.5 Ω", ["2.0 Ω", "8.0 Ω", "4.0 Ω"], "A"),
  "Terminal voltage V = ε − Ir: a straight line with intercept ε on the V-axis and slope −r",
  "At I = 0 the terminal voltage equals the emf, so ε = 2.0 V. The line reaches V = 0 when the terminals are "
  "short-circuited, at I = ε/r = 4.0 A. The internal resistance is the magnitude of the slope.",
  ["V = ε − Ir → V-intercept = ε = 2.0 V", "V = 0 at I = ε/r = 4.0 A", "r = 2.0/4.0 = 0.5 Ω"],
  shortcut="r = (V-intercept)/(I-intercept).",
  why="2.0 Ω inverts the ratio (I-intercept/V-intercept). 8.0 Ω multiplies the two intercepts. 4.0 Ω reads the "
      "current intercept as if it were the resistance.",
  ncert=CEC + "cells, emf, internal resistance", seconds=35, rc=True)

I_s = 10 / (2 + 3)
H3 = I_s ** 2 * 3 * 60
assert I_s == 2 and H3 == 720
assert I_s ** 2 * 5 * 60 == 1200 and I_s ** 2 * 2 * 60 == 480 and round(10 ** 2 / 3 * 60) == 2000
q(CE, "Combination of resistors", "Basic", "numerical",
  "A 2 Ω resistor and a 3 Ω resistor are connected in series across an ideal 10 V battery. The heat produced in "
  "the 3 Ω resistor in one minute is:",
  *opt("720 J", ["1200 J", "480 J", "2000 J"], "B"),
  "Joule heating H = I²Rt, with the series current fixed by the total resistance",
  "The same current flows through both resistors: I = 10/(2 + 3) = 2 A. The heat produced in the 3 Ω resistor in "
  "60 s is I²Rt.",
  ["I = 10/5 = 2 A", "H = I²Rt = 2² × 3 × 60 = 720 J"],
  why="1200 J is the heat produced in both resistors together. 480 J is the heat in the 2 Ω resistor. 2000 J puts "
      "the full 10 V across the 3 Ω resistor.",
  ncert=CEC + "electrical energy, power; combination of resistors - series and parallel", seconds=35, rc=True)

I_w = F(6, 10 + 5)
V30 = I_w * F(10) * F(30, 100)
assert I_w == F(2, 5) and V30 == F(6, 5)
assert F(6) * F(30, 100) == F(9, 5) and I_w * 10 == 4 and I_w * 5 == 2
q(CE, "Drift velocity and Ohm's law", "Basic", "numerical",
  "A uniform wire AB, 100 cm long and of resistance 10 Ω, is connected in series with a 5 Ω resistor across an "
  "ideal 6 V battery. The potential difference between two points of the wire that are 30 cm apart is:",
  *opt("1.2 V", ["1.8 V", "4.0 V", "2.0 V"], "C"),
  "Ohm's law; a uniform wire has the same resistance per unit length everywhere",
  "The current is fixed by the total resistance of the circuit. A 30 cm length of the uniform wire has 30% of its "
  "resistance, and the potential difference across it is the current times that resistance.",
  ["I = 6/(10 + 5) = 0.4 A", "Resistance of 30 cm = 10 × 30/100 = 3 Ω", "V = 0.4 × 3 = 1.2 V"],
  why="1.8 V ignores the 5 Ω resistor and puts all 6 V across the wire. 4.0 V is the potential difference across "
      "the whole wire. 2.0 V is the potential difference across the 5 Ω resistor.",
  ncert=CEC + "Ohm's law", seconds=40, rc=True)

I_out = 4 + 3 - 2
assert I_out == 5 and 4 + 3 + 2 == 9 and 4 - 3 == 1
q(CE, "Kirchhoff's laws", "Basic", "numerical",
  "Four wires meet at a junction in a circuit carrying steady currents. Currents of 4 A and 3 A flow into the "
  "junction through two of the wires, and a current of 2 A flows out of it through the third wire. The current in "
  "the fourth wire is:",
  *opt("5 A, flowing out of the junction", ["9 A, flowing out of the junction", "1 A, flowing into the junction",
                                             "5 A, flowing into the junction"], "D"),
  "Kirchhoff's junction rule: total current in = total current out",
  "With steady currents no charge piles up at the junction, so the currents flowing in must equal the currents "
  "flowing out.",
  ["In: 4 + 3 = 7 A", "Out so far: 2 A", "Fourth wire: 7 − 2 = 5 A, flowing out"],
  why="9 A adds every current regardless of direction. 1 A subtracts the two incoming currents. 5 A into the "
      "junction has the right size but would make the incoming total 12 A against 2 A out.",
  ncert=CEC + "Kirchhoff's rules", seconds=25, rc=True)

P_, Q_, R_, S_ = 10, 20, 15, 30
assert F(P_, Q_) == F(R_, S_)
assert F(2 * P_, Q_) != F(R_, 2 * S_) and F(2 * P_, 2 * Q_) == F(R_, S_)
q(CE, "Wheatstone and metre bridge", "Basic", "direct",
  "In a Wheatstone bridge, resistors P and Q are in series in one branch and R and S in series in the other; both "
  "branches are connected across a cell, and a galvanometer joins the P–Q junction to the R–S junction. The bridge "
  "is balanced (P/Q = R/S). Which one of the following changes, made on its own, will make the galvanometer show a "
  "deflection?",
  *opt("Doubling both P and S", ["Replacing the cell by one of twice the emf",
                                 "Replacing the galvanometer by one of higher resistance",
                                 "Doubling both P and Q"], "C"),
  "Balance condition of the Wheatstone bridge: P/Q = R/S",
  "The balance condition involves only the ratios of the four resistances; it contains neither the emf of the cell "
  "nor the resistance of the galvanometer. Doubling P and S makes the left ratio 2P/Q and the right ratio R/(2S), "
  "so P/Q is now four times R/S and the bridge is unbalanced.",
  ["Balance needs P/Q = R/S only", "Double P and S: 2P/Q ≠ R/2S → deflection",
   "Double P and Q: 2P/2Q = P/Q → still balanced"],
  why="The cell's emf and the galvanometer's resistance do not appear in the balance condition, so changing them "
      "keeps the null. Doubling P and Q leaves the ratio P/Q unchanged.",
  ncert=CEC + "Wheatstone bridge", seconds=40)

q(CE, "Resistivity and temperature", "Basic", "direct",
  "The SI unit of resistivity, Ω m, expressed in terms of the SI base units (kg, m, s, A), is:",
  *opt("kg m³ s⁻³ A⁻²", ["kg m² s⁻³ A⁻²", "kg m s⁻³ A⁻²", "kg⁻¹ m⁻³ s³ A²"], "D"),
  "ρ = RA/l, and 1 Ω = 1 V/A",
  "1 V = 1 J/C = kg m² s⁻² /(A s) = kg m² s⁻³ A⁻¹, so 1 Ω = 1 V/A = kg m² s⁻³ A⁻². Multiplying by a metre gives "
  "the unit of resistivity.",
  ["1 Ω = kg m² s⁻³ A⁻²", "1 Ω m = kg m³ s⁻³ A⁻²"],
  why="kg m² s⁻³ A⁻² is the ohm itself (resistance, not resistivity). kg m s⁻³ A⁻² divides the ohm by a metre "
      "instead of multiplying. kg⁻¹ m⁻³ s³ A² is the unit of conductivity, the reciprocal of resistivity.",
  ncert=CEC + "Ohm's law (resistivity)", seconds=40)

# ---- Intermediate
R50, R100 = F(5), F(6)
slope = (R100 - R50) / 50
R0 = R50 - 50 * slope
alpha0 = slope / R0
assert R0 == 4 and alpha0 == F(5, 1000)
assert slope / R50 == F(4, 1000) and slope / R100 == F(1, 300)
close(5 * 273 / 323, 4.2, 0.01)
close(1 / 273, 3.7e-3, 0.02)
q(CE, "Resistivity and temperature", "Intermediate", "numerical",
  "The resistance of a metal wire is 5.0 Ω at 50 °C and 6.0 Ω at 100 °C. Assuming that its resistance varies "
  "linearly with temperature, its resistance at 0 °C and its temperature coefficient of resistance referred to "
  "0 °C are, respectively:",
  *opt("4.0 Ω and 5.0 × 10⁻³ °C⁻¹", ["4.0 Ω and 4.0 × 10⁻³ °C⁻¹", "4.2 Ω and 3.7 × 10⁻³ °C⁻¹",
                                     "4.0 Ω and 3.3 × 10⁻³ °C⁻¹"], "B"),
  "R_T = R₀(1 + αT): a straight line whose slope is αR₀",
  "The resistance rises by 1.0 Ω for 50 °C, i.e. 0.02 Ω per °C. Extrapolating back 50 °C from 5.0 Ω gives R₀. "
  "Since the slope equals αR₀, α (referred to 0 °C) is the slope divided by R₀.",
  ["Slope = (6.0 − 5.0)/50 = 0.02 Ω °C⁻¹", "R₀ = 5.0 − 50 × 0.02 = 4.0 Ω", "α = 0.02/4.0 = 5.0 × 10⁻³ °C⁻¹"],
  why="4.0 × 10⁻³ °C⁻¹ divides the slope by the resistance at 50 °C, and 3.3 × 10⁻³ °C⁻¹ by the resistance at "
      "100 °C, instead of by R₀. 4.2 Ω and 3.7 × 10⁻³ °C⁻¹ wrongly take the resistance as proportional to the "
      "absolute temperature.",
  ncert=CEC + "temperature dependence of resistivity", seconds=70, rc=True)

tiny = F(1, 10 ** 9)
R_short = equivalent_resistance(4, [(0, 1, 6), (1, 2, 6), (2, 3, 6), (0, 2, tiny), (1, 3, tiny)], 0, 3)
close(float(R_short), 2.0, 1e-6)
q(CE, "Combination of resistors", "Intermediate", "numerical",
  "Three 6 Ω resistors are connected in series between points A and B, in the order A–P (first resistor), P–Q "
  "(second resistor) and Q–B (third resistor). A wire of negligible resistance then joins A to Q, and another wire "
  "of negligible resistance joins P to B. The equivalent resistance between A and B is:",
  *opt("2 Ω", ["18 Ω", "6 Ω", "zero"], "A"),
  "Points joined by a wire of negligible resistance are at the same potential and can be merged",
  "Because of the wires, A and Q are one node and P and B are another. Then the first resistor (A–P) runs from "
  "node A to node B, the second (P–Q) from node B to node A and the third (Q–B) from node A to node B: all three "
  "resistors are connected between A and B, i.e. in parallel.",
  ["A ≡ Q and P ≡ B", "Each 6 Ω resistor is connected between A and B", "R = 6/3 = 2 Ω"],
  why="18 Ω ignores the two wires. 6 Ω keeps only one resistor between A and B. Zero assumes A and B are shorted, but "
      "A and B are still joined only through resistors.",
  ncert=CEC + "combination of resistors - series and parallel", seconds=60, rc=True)

eps_m, R_m = 12, 3
r_m = R_m
Pmax = F(eps_m ** 2, 4 * r_m)
assert Pmax == 12
assert F(eps_m ** 2, 2 * r_m) == 24 and F(eps_m ** 2, r_m) == 48 and F(eps_m ** 2, 4 * F(3, 2)) == 24
q(CE, "Cells, emf and internal resistance", "Intermediate", "numerical",
  "A battery of emf 12 V delivers the greatest possible power to an external resistor when the resistance of that "
  "resistor is 3 Ω. The internal resistance of the battery and the greatest power it can deliver to an external "
  "resistor are, respectively:",
  *opt("3 Ω and 12 W", ["3 Ω and 24 W", "3 Ω and 48 W", "1.5 Ω and 24 W"], "B"),
  "Maximum power transfer: the power in the external resistor is greatest when R = r, and then equals ε²/4r",
  "P = ε²R/(R + r)² is greatest when R = r, so r = 3 Ω. The current is then ε/2r = 2 A and the power in the "
  "external resistor is I²R.",
  ["Maximum when R = r → r = 3 Ω", "I = 12/(3 + 3) = 2 A", "P = I²R = 4 × 3 = 12 W (= ε²/4r)"],
  why="24 W is the total power generated by the battery (εI), half of which is lost in the internal resistance. "
      "48 W is ε²/r, the power that would be generated on short circuit. 1.5 Ω and 24 W wrongly take r as half "
      "of R.",
  ncert=CEC + "cells, emf, internal resistance", seconds=60, rc=True)

rhoA, rhoB = 2.0e-8, 1.0e-6
close(rhoB / rhoA, 50)
close(rhoA / rhoB, 0.02)
close(math.sqrt(rhoB / rhoA), 7.07, 1e-3)
q(CE, "Drift velocity and Ohm's law", "Intermediate", "numerical",
  "A wire of metal A (resistivity 2.0 × 10⁻⁸ Ω m) is joined end to end with a wire of alloy B (resistivity "
  "1.0 × 10⁻⁶ Ω m) of the same cross-sectional area, and a steady current flows through the two wires in series. "
  "The ratio of the magnitude of the electric field inside wire B to that inside wire A is:",
  *opt("50", ["1", "0.02", "7.1"], "D"),
  "Microscopic form of Ohm's law: E = ρj",
  "The current and the cross-sectional area are the same for both wires, so the current density j is the same. The "
  "electric field needed to drive that current density is proportional to the resistivity.",
  ["j = I/A, same in both wires", "E = ρj → E_B/E_A = ρ_B/ρ_A", "= (1.0 × 10⁻⁶)/(2.0 × 10⁻⁸) = 50"],
  why="1 assumes that the same current means the same field. 0.02 inverts the ratio. 7.1 takes a square root that "
      "has no place in E = ρj.",
  ncert=CEC + "Ohm's law (j = σE)", seconds=50, rc=True)

q(CE, "Combination of resistors", "Intermediate", "assertion_reason",
  ar("The coil of an electric heater is cut to half its length, and the remaining half is connected across the same "
     "mains supply. Neglecting any change of resistance with temperature, the heater now draws twice the power.",
     "The power drawn by a resistor across a fixed potential difference is V²/R, and halving the length of a "
     "uniform coil halves its resistance."),
  AR, ar_key(True, True, True),
  "Power P = V²/R at a fixed potential difference; R ∝ length",
  "Half the length of the same wire has half the resistance. With the same mains voltage, P = V²/R doubles. R states "
  "exactly these two facts, so it explains A.",
  ["R' = R/2 (R ∝ l)", "P' = V²/R' = 2V²/R = 2P", "R explains A"],
  why="Both statements are true and together they give the doubling, so R is the correct explanation of A.",
  ncert=CEC + "electrical energy, power", seconds=40)

q(CE, "Kirchhoff's laws", "Intermediate", "statement_pair",
  sp("Kirchhoff's junction rule holds for steady currents because no charge accumulates at a junction.",
     "Kirchhoff's loop rule can be applied only to closed loops that contain at least one cell."),
  SP, sp_key(True, False),
  "Basis of Kirchhoff's rules",
  "The junction rule expresses conservation of charge: in the steady state charge does not pile up at a junction, "
  "so the current in equals the current out (Statement I true). The loop rule says the algebraic sum of the changes "
  "in potential round any closed loop is zero, because the electrostatic potential is single-valued; it applies to "
  "every closed loop, whether or not the loop contains a cell (Statement II false).",
  ["Junction rule: charge conservation, no accumulation → I true",
   "Loop rule: valid for any closed loop → II false"],
  why="A loop made only of resistors also obeys the loop rule (the sum of the IR terms is zero), so Statement II is "
      "false.",
  ncert=CEC + "Kirchhoff's rules", seconds=40)

I_A = F(1) / (F(2) / 1)          # length doubled
I_B = F(1) / (F(1) / 4)          # diameter doubled → area ×4
I_C = F(1) / (F(2) / 4)          # both doubled
I_D = F(1) / (F(2) / F(1, 2))    # stretched: length ×2, area ×1/2
assert (I_A, I_B, I_C, I_D) == (F(1, 2), 4, 2, F(1, 4))
q(CE, "Resistivity and temperature", "Intermediate", "match_list",
  ml("A uniform metal wire is connected across a fixed potential difference, and its temperature stays the same. "
     "Each change in List-I is made to the original wire (or the wire is replaced by another wire of the same "
     "material). Match each change with its effect on the current in List-II.",
     ["The length is doubled, the cross-sectional area being unchanged",
      "The diameter is doubled, the length being unchanged",
      "Both the length and the diameter are doubled",
      "The wire is stretched uniformly to twice its length (its volume being unchanged)"],
     ["Becomes half", "Becomes four times", "Becomes twice", "Becomes one-fourth"]),
  *mlo("A-I, B-II, C-III, D-IV", ["A-I, B-III, C-II, D-IV", "A-III, B-II, C-I, D-IV", "A-I, B-II, C-IV, D-III"],
       "A"),
  "R = ρl/A with ρ fixed; I = V/R at a fixed potential difference",
  "The current is inversely proportional to R, i.e. proportional to A/l. Doubling the diameter makes the area four "
  "times. Stretching to twice the length at constant volume halves the area, so R becomes four times.",
  ["A: l × 2 → R × 2 → I/2", "B: d × 2 → A × 4 → R/4 → I × 4", "C: l × 2, A × 4 → R/2 → I × 2",
   "D: l × 2, A/2 → R × 4 → I/4"],
  why="A-I, B-III, ... treats the area as proportional to the diameter instead of its square. A-III, B-II, ... "
      "makes the current proportional to the length. A-I, B-II, C-IV, D-III interchanges the last two cases.",
  ncert=CEC + "Ohm's law (resistivity)", seconds=60, rc=True)

Rp_ = F(3 * 6, 3 + 6)
Req_ = Rp_ + 2
I_tot = F(12) / Req_
Vp_ = I_tot * Rp_
assert Req_ == 4 and I_tot == 3 and Vp_ == 6
truth_ce = {"a": Req_ == 4, "b": Vp_ / 3 == 1, "c": I_tot * 2 == 6, "d": Vp_ ** 2 / 6 == 6, "e": 12 * I_tot == 24}
q(CE, "Combination of resistors", "Intermediate", "multi_statement",
  ms("A 3 Ω resistor and a 6 Ω resistor are connected in parallel, and this combination is connected in series with "
     "a 2 Ω resistor across an ideal 12 V battery. Which of the following statements are correct?",
     ["The equivalent resistance of the circuit is 4 Ω.",
      "The current in the 3 Ω resistor is 1 A.",
      "The potential difference across the 2 Ω resistor is 6 V.",
      "The power dissipated in the 6 Ω resistor is 6 W.",
      "The power supplied by the battery is 24 W."]),
  *mso(truth_ce, "acd", ["abc", "acde", "cd"], "B"),
  "Series–parallel reduction, current division and power",
  "3 Ω ∥ 6 Ω = 2 Ω, so the total is 4 Ω (a true) and the battery current is 3 A. The 2 Ω resistor takes 6 V (c "
  "true), leaving 6 V across the parallel pair: 2 A in the 3 Ω resistor (b false) and 1 A in the 6 Ω resistor, "
  "which dissipates 6²/6 = 6 W (d true). The battery supplies 12 × 3 = 36 W (e false).",
  ["R = 2 + 2 = 4 Ω; I = 3 A", "V(2 Ω) = 6 V; V(parallel) = 6 V", "I(3 Ω) = 2 A; P(6 Ω) = 6 W",
   "P(battery) = 36 W"],
  why="Options containing (b) or (e) include a false statement; (c) and (d) only leaves out the true statement (a).",
  ncert=CEC + "combination of resistors - series and parallel", seconds=75, rc=True)

# ---- Advanced
V_load = lambda RL: F(10) * (F(50) * RL / (50 + RL)) / (50 + F(50) * RL / (50 + RL))
assert V_load(F(100)) == 4
assert F(50) * 100 / 150 == F(100, 3)
assert V_load(F(200)) != 4 and F(10) * (F(50) * 200 / 250) / 100 == 4   # forgetting the upper half
q(CE, "Combination of resistors", "Advanced", "numerical",
  "A rheostat of total resistance 100 Ω is used as a potential divider: its two ends are connected across an ideal "
  "10 V battery and its sliding contact is set exactly at the middle of its length. A load resistor R_L is "
  "connected between the sliding contact and the negative end of the rheostat (i.e. across the lower half). The "
  "potential difference across R_L is found to be 4.0 V. The value of R_L is:",
  *opt("100 Ω", ["33.3 Ω", "200 Ω", "20 Ω"], "C"),
  "Loaded potential divider: the load is in parallel with the lower part of the divider",
  "The lower 50 Ω of the rheostat in parallel with R_L forms R_p, which is in series with the upper 50 Ω. The 10 V "
  "divides in the ratio R_p : 50, and R_p must take 4.0 V.",
  ["4.0 = 10 × R_p/(R_p + 50) → R_p = 33.3 Ω", "50R_L/(50 + R_L) = 100/3 → 150R_L = 5000 + 100R_L",
   "R_L = 100 Ω"],
  why="33.3 Ω is the parallel combination R_p, not the load itself. 200 Ω divides the voltage in proportion to the "
      "whole 100 Ω rheostat, forgetting that the upper half is in series. 20 Ω comes from inverting the "
      "parallel-combination formula wrongly.",
  ncert=CEC + "combination of resistors - series and parallel", seconds=110, rc=True)

n_cu, e_ch, I_d = 8.0e28, 1.6e-19, 3.2
v1 = I_d / (n_cu * e_ch * 1.0e-6)
v2 = I_d / (n_cu * e_ch * 2.0e-6)
t_dr = 0.45 / v1 + 0.45 / v2
close(v1, 2.5e-4)
close(t_dr / 3600, 1.5)
close(0.9 / v1 / 3600, 1.0)
close(0.9 / v2 / 3600, 2.0)
close(0.9 / ((v1 + v2) / 2) / 3600, 4 / 3)
q(CE, "Drift velocity and Ohm's law", "Advanced", "numerical",
  "A copper wire 0.90 m long consists of two parts of equal length: the first 0.45 m has a cross-sectional area of "
  "1.0 mm² and the remaining 0.45 m an area of 2.0 mm². It carries a steady current of 3.2 A. Taking the number "
  "density of free electrons in copper as 8.0 × 10²⁸ m⁻³ and e = 1.6 × 10⁻¹⁹ C, the time taken by an electron to "
  "drift from one end of the wire to the other is:",
  *opt("1.5 h", ["1.0 h", "2.0 h", "1.33 h"], "B"),
  "Drift speed v_d = I/(neA); the same current flows through both parts",
  "The drift speed is larger in the thinner part. The total drift time is the sum of the times spent in the two "
  "parts, each found from its own drift speed.",
  ["Thin part: v₁ = 3.2/(8.0 × 10²⁸ × 1.6 × 10⁻¹⁹ × 1.0 × 10⁻⁶) = 2.5 × 10⁻⁴ m/s → t₁ = 0.45/v₁ = 1800 s",
   "Thick part: v₂ = 1.25 × 10⁻⁴ m/s → t₂ = 3600 s", "t = 5400 s = 1.5 h"],
  why="1.0 h uses the drift speed of the thinner part for the whole wire, and 2.0 h that of the thicker part. "
      "1.33 h divides the length by the average of the two drift speeds, which is not the correct average for "
      "equal distances.",
  ncert=CEC + "drift of electrons and the origin of resistivity", seconds=110, rc=True)

edges_k4 = [(0, 1, 2), (0, 2, 2), (0, 3, 2), (1, 2, 2), (1, 3, 2), (2, 3, 1)]
assert equivalent_resistance(4, edges_k4, 0, 1) == 1
v_k4 = solve_network(4, edges_k4, {0: 1, 1: 0})
assert v_k4[2] == v_k4[3]
assert F(2) / 3 == F(2, 3) and F(2 * 4, 2 + 4) == F(4, 3)
q(CE, "Combination of resistors", "Advanced", "numerical",
  "Four points A, B, C and D are each joined to every other point by a separate resistor (six resistors in all, "
  "insulated where they cross). The resistors joining A–B, A–C, A–D, B–C and B–D are each 2 Ω, and the resistor "
  "joining C–D is 1 Ω. The equivalent resistance between A and B is:",
  *opt("1 Ω", ["2 Ω", "4/3 Ω", "2/3 Ω"], "A"),
  "Symmetry: points at the same potential carry no current between them",
  "With a potential difference between A and B, C and D are placed identically (each joined to A and to B by 2 Ω), "
  "so they are at the same potential and the C–D resistor carries no current, whatever its value. The network is "
  "then the direct 2 Ω resistor in parallel with two 4 Ω paths (A–C–B and A–D–B).",
  ["V_C = V_D → no current in C–D", "Paths: 2 Ω, 4 Ω, 4 Ω in parallel", "1/R = 1/2 + 1/4 + 1/4 = 1 → R = 1 Ω"],
  why="2 Ω keeps only the direct A–B resistor. 4/3 Ω leaves out one of the two 4 Ω paths. 2/3 Ω treats each "
      "two-resistor path as a single 2 Ω resistor.",
  ncert=CEC + "combination of resistors - series and parallel", seconds=90, rc=True)

Vc, Vd, I_cd = F(16, 10), F(12, 10), F(2)
eps_c = (Vc + Vd) / 2
r_c = (Vc - Vd) / (2 * I_cd)
assert eps_c == F(14, 10) and r_c == F(1, 10)
assert (Vc - Vd) / I_cd == F(2, 10)
q(CE, "Cells, emf and internal resistance", "Advanced", "numerical",
  "When a cell is being charged by a current of 2.0 A, the potential difference across its terminals is 1.6 V. "
  "When the same cell is discharging and supplies a current of 2.0 A to an external circuit, the potential "
  "difference across its terminals is 1.2 V. The emf and internal resistance of the cell are, respectively:",
  *opt("1.4 V and 0.1 Ω", ["1.4 V and 0.2 Ω", "1.6 V and 0.2 Ω", "1.2 V and 0.1 Ω"], "C"),
  "Terminal voltage: V = ε + Ir while charging, V = ε − Ir while discharging",
  "While charging, the current is driven into the positive terminal against the emf, so the terminal voltage "
  "exceeds ε by Ir. While discharging it falls short of ε by Ir. Adding and subtracting the two equations gives ε "
  "and r.",
  ["ε + 2r = 1.6 and ε − 2r = 1.2", "Adding: 2ε = 2.8 → ε = 1.4 V", "Subtracting: 4r = 0.4 → r = 0.1 Ω"],
  why="1.4 V and 0.2 Ω divides the difference of the two voltages by 2.0 A instead of by 4.0 A. 1.6 V and 1.2 V "
      "take one of the terminal voltages as the emf.",
  ncert=CEC + "cells, emf, internal resistance", seconds=80, rc=True)

q(CE, "Kirchhoff's laws", "Advanced", "assertion_reason",
  ar("In a single series circuit of a cell and several resistors, the current is largest in the resistor nearest "
     "the positive terminal of the cell and becomes smaller in each later resistor, because charge is used up as "
     "it flows.",
     "In a series circuit carrying a steady current, the current is the same at every cross-section, because charge "
     "is conserved and does not accumulate anywhere in the circuit."),
  AR, ar_key(False, True),
  "Steady current and conservation of charge",
  "Charge is not consumed in a resistor; it is energy that is converted into heat. In the steady state no charge "
  "accumulates anywhere, so the same current flows through every element of a series circuit (A false, R true).",
  ["Charge is conserved; energy, not charge, is used up in resistors", "Same current in all series elements",
   "A false, R true"],
  why="A is the common misconception that current is 'used up'. R is the correct statement, so the options that "
      "call A true are wrong.",
  ncert=CEC + "electric current; Kirchhoff's rules", seconds=40)

eX, eY, rX, rY = 6, 4, 1, 1
I_loop = F(eX - eY, rX + rY)
V_term = eX - I_loop * rX
heat = I_loop ** 2 * (rX + rY)
truth_cells = {"a": I_loop == 1, "b": V_term == 5, "c": False, "d": heat == 2, "e": eX * I_loop == 4}
assert eY + I_loop * rY == V_term   # Y is charged: current enters its positive terminal
q(CE, "Cells, emf and internal resistance", "Advanced", "multi_statement",
  ms("A cell X (emf 6 V, internal resistance 1 Ω) and a cell Y (emf 4 V, internal resistance 1 Ω) are connected "
     "in parallel, positive terminal to positive terminal and negative terminal to negative terminal. Nothing else "
     "is connected to them. Which of the following statements are correct?",
     ["A current of 1 A flows round the loop formed by the two cells.",
      "The potential difference between the common positive and common negative terminals is 5 V.",
      "The current flows out of the positive terminal of Y.",
      "Heat is produced in the two cells at a total rate of 2 W.",
      "Cell X converts chemical energy into electrical energy at the rate of 4 W."]),
  *mso(truth_cells, "abd", ["ab", "abde", "bcd"], "D"),
  "Loop rule for two opposing emfs; charging of the weaker cell",
  "Round the loop the emfs oppose each other: I = (6 − 4)/(1 + 1) = 1 A (a true). The common terminal voltage is "
  "6 − 1 × 1 = 5 V = 4 + 1 × 1 (b true). Since 5 V exceeds Y's emf, the current is driven into Y's positive "
  "terminal and Y is being charged (c false). Heat in the internal resistances is 1² × 1 + 1² × 1 = 2 W (d true). X "
  "converts chemical energy at ε_X I = 6 W, of which 4 W is stored in Y and 2 W is heat (e false).",
  ["I = 2/2 = 1 A", "V = 6 − 1 = 5 V", "Current enters Y at + → Y charged", "Heat = 2 W; ε_X I = 6 W"],
  why="Options containing (c) or (e) include a false statement; (a) and (b) only leaves out the true statement (d).",
  ncert=CEC + "cells, emf, internal resistance; Kirchhoff's rules", seconds=100, rc=True)


# ================================================================ Magnetic Effects of Current and Magnetism (B6 I8 A6)
MC = NC + "'Moving Charges and Magnetism', "
MM = NC + "'Magnetism and Matter', "
MU0 = 4 * math.pi * 1e-7

# ---- Basic
assert F(2, 3) * 1 == F(2 * 1, 3)          # B ∝ I/r: (2I)/(3d) → 2B/3
assert F(2, 9) != F(2, 3) and F(3, 2) != F(2, 3)
q(MAG, "Biot-Savart law", "Basic", "numerical",
  "The magnetic field at a distance d from a long straight wire carrying a steady current I is B. If the current is "
  "doubled, the magnetic field at a distance 3d from the wire is:",
  *opt("2B/3", ["6B", "2B/9", "3B/2"], "A"),
  "Field of a long straight wire: B = µ₀I/(2πr), i.e. B ∝ I/r",
  "The field is directly proportional to the current and inversely proportional to the distance from the wire.",
  ["B' = B × (2I/I) × (d/3d)", "B' = 2B/3"],
  why="6B multiplies by the distance ratio instead of dividing. 2B/9 treats the field as falling off as 1/r². 3B/2 "
      "inverts the result.",
  ncert=MC + "magnetic field due to a long straight current-carrying wire", seconds=30, rc=True)

S_sh, frac = F(2), F(1, 10)
G_sh = S_sh * (1 - frac) / frac
assert G_sh == 18
assert S_sh * frac / (1 - frac) == F(2, 9) and S_sh / frac == 20 and S_sh * F(9, 10) == F(9, 5)
q(MAG, "Torque on loop and galvanometer", "Basic", "numerical",
  "A shunt of 2 Ω is connected across a galvanometer, and it is found that only 10% of the main current now passes "
  "through the galvanometer. The resistance of the galvanometer is:",
  *opt("18 Ω", ["0.22 Ω", "20 Ω", "1.8 Ω"], "B"),
  "Galvanometer and shunt are in parallel: the currents divide inversely as the resistances",
  "The potential difference across the galvanometer equals that across the shunt. 10% of the current flows through "
  "G and 90% through S.",
  ["I_g G = (I − I_g) S", "0.1I × G = 0.9I × 2", "G = 18 Ω"],
  why="0.22 Ω inverts the current ratio (it would make the galvanometer carry 90%). 20 Ω divides S by 0.1 without "
      "using the 90% through the shunt. 1.8 Ω multiplies S by 0.9 instead of by 9.",
  ncert=MC + "moving coil galvanometer", seconds=40, rc=True)

m_loop = 0.02 * 5
tau0 = m_loop * 0.3 * math.sin(0)
assert tau0 == 0
close(m_loop * 0.3, 0.03)
close(m_loop * 0.3 / 2, 0.015)
close(m_loop * 0.3 * math.sqrt(3) / 2, 0.026, 1e-2)
q(MAG, "Torque on loop and galvanometer", "Basic", "numerical",
  "A plane circular loop of area 0.02 m² carries a steady current of 5 A. It is placed in a uniform magnetic field "
  "of 0.3 T with its plane perpendicular to the field. The magnitude of the torque on the loop is:",
  *opt("zero", ["0.03 N m", "0.015 N m", "0.026 N m"], "C"),
  "Torque on a current loop: τ = m × B, of magnitude mB sin θ (θ = angle between m and B)",
  "The magnetic moment of a plane loop is perpendicular to its plane. With the plane perpendicular to B, the moment "
  "is parallel (or antiparallel) to B, so θ = 0 (or 180°) and the torque is zero.",
  ["m = IA = 5 × 0.02 = 0.1 A m², along the normal to the loop", "Plane ⊥ B → m ∥ B → sin θ = 0",
   "τ = 0"],
  why="0.03 N m is the maximum torque mB, which acts when the plane of the loop is parallel to the field. 0.015 N m "
      "and 0.026 N m correspond to angles of 30° and 60° between m and B.",
  ncert=MC + "torque on current loop, magnetic dipole", seconds=30, rc=True)

q(MAG, "Ampere's law", "Basic", "direct",
  "Ampere's circuital law, ∮B·dl = µ₀I, holds for any closed path in a region of steady currents. It is, however, "
  "practically useful for calculating the magnetic field only when:",
  *opt("the current distribution is symmetric enough that a closed path can be chosen along which the field is "
       "tangential and of constant magnitude (or zero)",
       ["the current changes with time", "the closed path chosen is a circle",
        "the closed path chosen encloses no current"], "D"),
  "Ampere's circuital law and its use for symmetric current distributions",
  "The law always relates the line integral of B round a closed path to the current enclosed. To get B itself out "
  "of the integral, the path must be one on which B is tangential with a constant magnitude (as for a long straight "
  "wire, a solenoid or a toroid), so that ∮B·dl reduces to B × (length of the path).",
  ["∮B·dl = µ₀I_enclosed holds always (steady currents)", "B can be taken out of the integral only on a "
   "symmetric path", "So the law is useful when there is high symmetry"],
  why="The law in this form is for steady currents, not time-varying ones. The path need not be a circle (a "
      "rectangle is used for the solenoid). A path enclosing no current gives ∮B·dl = 0, which by itself does not "
      "give B.",
  ncert=MC + "Ampere's circuital law", seconds=35)

q(MAG, "Magnetic dipole and bar magnet", "Basic", "statement_pair",
  sp("A current-carrying solenoid behaves like a bar magnet; the end at which the current is seen to flow "
     "anticlockwise, when viewed from outside facing that end, acts as its north pole.",
     "The magnetic field lines of a bar magnet and those of a current-carrying solenoid form continuous closed "
     "loops."),
  SP, sp_key(True, True),
  "Bar magnet as an equivalent solenoid",
  "By the right-hand rule, an anticlockwise current seen from one end produces a field pointing out of that end, "
  "towards the viewer, so field lines emerge there: it is a north pole (Statement I true). Magnetic field lines "
  "never begin or end; for both the bar magnet and the solenoid they run outside from N to S and inside from S to "
  "N, forming closed loops (Statement II true).",
  ["Anticlockwise current facing the viewer → field towards the viewer → N pole", "Field lines are closed loops"],
  why="Both statements are correct, so options calling either of them false are wrong.",
  ncert=MM + "the bar magnet; bar magnet as an equivalent solenoid", seconds=35)

cross = lambda a, b: (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])
X_, Y_, Z_ = (1, 0, 0), (0, 1, 0), (0, 0, 1)
assert cross(X_, Y_) == Z_ and cross(Y_, Z_) == X_ and cross(Z_, X_) == Y_ and cross(X_, Z_) == (0, -1, 0)
q(MAG, "Force on charges and conductors", "Basic", "match_list",
  ml("A positively charged particle moves through a uniform magnetic field. Its velocity and the field are along the "
     "directions given in List-I. Match each case with the direction of the magnetic force on the particle in "
     "List-II.",
     ["Velocity along +x, field along +y", "Velocity along +y, field along +z", "Velocity along +z, field along +x",
      "Velocity along +x, field along +z"],
     ["Along +x", "Along +y", "Along +z", "Along −y"]),
  *mlo("A-III, B-I, C-II, D-IV", ["A-III, B-II, C-I, D-IV", "A-IV, B-I, C-II, D-III", "A-III, B-I, C-IV, D-II"],
       "D"),
  "Magnetic force F = q(v × B)",
  "For a positive charge the force is along v × B. Using x̂ × ŷ = ẑ, ŷ × ẑ = x̂, ẑ × x̂ = ŷ and x̂ × ẑ = −ŷ gives the "
  "four directions.",
  ["A: x̂ × ŷ = ẑ", "B: ŷ × ẑ = x̂", "C: ẑ × x̂ = ŷ", "D: x̂ × ẑ = −ŷ"],
  why="The other codes take B × v instead of v × B for some cases, which reverses the force, or interchange the "
      "results of two cases.",
  ncert=MC + "magnetic force", seconds=50, rc=True)

# ---- Intermediate
x_null = F(2 * 20, 6 - 2)
assert x_null == 10 and F(2, x_null) == F(6, x_null + 20)
assert F(2 * 20, 2 + 6) == 5            # the same-direction (between the wires) answer
q(MAG, "Biot-Savart law", "Intermediate", "numerical",
  "Two long straight parallel wires P and Q, 20 cm apart, carry steady currents of 2 A and 6 A respectively, in "
  "opposite directions. In the plane containing the two wires, the resultant magnetic field due to them is zero at "
  "a line that is:",
  *opt("10 cm from P, on the side of P away from Q", ["5 cm from P, between the wires",
                                                       "10 cm from Q, on the side of Q away from P",
                                                       "nowhere; no such line exists in that plane"], "B"),
  "Superposition of the fields of two long straight wires (B = µ₀I/2πr)",
  "For opposite currents, the two fields point the same way at every point between the wires, so they can cancel "
  "only outside. The point must be nearer the smaller current so that its field can match the larger current's "
  "field from farther away.",
  ["Outside, beyond P, distance x from P: 2/x = 6/(x + 20)", "6x = 2x + 40 → x = 10 cm"],
  why="5 cm from P between the wires is the answer for currents in the same direction. A point beyond Q is nearer "
      "the larger current, so the fields cannot cancel there. A null line does exist, outside the wires on P's "
      "side.",
  ncert=MC + "magnetic field due to a long straight current-carrying wire", seconds=70, rc=True)

R_c, B_c = 0.10, 2 * math.pi * 1e-5
I_c = 2 * R_c * B_c / MU0
m_c = I_c * math.pi * R_c ** 2
close(I_c, 10)
close(m_c, 0.314, 1e-3)
close((4 * R_c * B_c / MU0) * math.pi * R_c ** 2, 0.628, 1e-3)
close((R_c * B_c / MU0) * math.pi * R_c ** 2, 0.157, 1e-3)
close(I_c * R_c ** 2, 0.10)
q(MAG, "Biot-Savart law", "Intermediate", "numerical",
  "A single circular loop of wire of radius 10 cm carries a steady current, and the magnetic field at its centre is "
  "2π × 10⁻⁵ T. Taking µ₀ = 4π × 10⁻⁷ T m A⁻¹, the magnetic dipole moment of the loop is about:",
  *opt("0.31 A m²", ["0.63 A m²", "0.16 A m²", "0.10 A m²"], "C"),
  "B at the centre = µ₀I/2R; magnetic moment m = IA",
  "First find the current from the field at the centre, then multiply it by the area of the loop.",
  ["I = 2RB/µ₀ = (2 × 0.10 × 2π × 10⁻⁵)/(4π × 10⁻⁷) = 10 A", "m = I πR² = 10 × π × 0.01 ≈ 0.31 A m²"],
  why="0.63 A m² uses µ₀I/4R (the field of a semicircle), which doubles the current. 0.16 A m² uses µ₀I/R, which "
      "halves it. 0.10 A m² leaves out π from the area.",
  ncert=MC + "magnetic field on the axis of a circular current loop; the magnetic dipole moment", seconds=60,
  rc=True)

B_one = MU0 * 10 / (2 * math.pi * 0.10)
close(B_one, 2e-5)
v1_ = (-math.sqrt(3) / 2, 0.5)
v2_ = (-math.sqrt(3) / 2, -0.5)
res = math.hypot(v1_[0] + v2_[0], v1_[1] + v2_[1]) * B_one
close(res, 3.46e-5, 2e-3)
close(math.hypot(v1_[0] - v2_[0], v1_[1] - v2_[1]) * B_one, 2e-5)
q(MAG, "Biot-Savart law", "Intermediate", "numerical",
  "Two long straight parallel wires, 10 cm apart, each carry a steady current of 10 A in the same direction. "
  "Taking µ₀ = 4π × 10⁻⁷ T m A⁻¹, the magnitude of the resultant magnetic field at a point that is 10 cm from each "
  "wire (so that the point and the two wires form an equilateral triangle in a plane perpendicular to the wires) "
  "is about:",
  *opt("3.5 × 10⁻⁵ T", ["4.0 × 10⁻⁵ T", "2.0 × 10⁻⁵ T", "zero"], "D"),
  "Vector superposition of the fields of two long straight wires",
  "Each wire produces 2 × 10⁻⁵ T at the point, perpendicular to the line joining that wire to the point. The two "
  "lines are at 60° to each other, and for currents in the same direction the two field vectors are also at 60°, "
  "giving a resultant of 2B cos 30° = √3 B.",
  ["Each field: B = µ₀I/(2πd) = (2 × 10⁻⁷ × 10)/0.10 = 2 × 10⁻⁵ T", "Angle between the two fields = 60°",
   "B_net = √3 × 2 × 10⁻⁵ ≈ 3.5 × 10⁻⁵ T"],
  why="4.0 × 10⁻⁵ T adds the magnitudes as if the fields were parallel. 2.0 × 10⁻⁵ T is the result for currents in "
      "opposite directions (fields at 120°). The fields do not cancel at this point.",
  ncert=MC + "magnetic field due to a long straight current-carrying wire", seconds=80, rc=True)

f_near = MU0 * 10 * 10 / (2 * math.pi * 0.10)
f_far = MU0 * 10 * 10 / (2 * math.pi * 0.20)
close(f_near + f_far, 3e-4)
close(2 * f_near, 4e-4)
close(f_near, 2e-4)
q(MAG, "Force on charges and conductors", "Intermediate", "numerical",
  "Three long straight parallel wires lie in one plane, equally spaced 10 cm apart, and each carries a steady "
  "current of 10 A in the same direction. Taking µ₀ = 4π × 10⁻⁷ T m A⁻¹, the magnitude of the net magnetic force "
  "per unit length on one of the outer wires is:",
  *opt("3 × 10⁻⁴ N/m", ["4 × 10⁻⁴ N/m", "2 × 10⁻⁴ N/m", "zero"], "A"),
  "Force per unit length between parallel currents: f = µ₀I₁I₂/(2πd), attractive for currents in the same "
  "direction",
  "An outer wire is attracted by the middle wire (10 cm away) and by the other outer wire (20 cm away). Both forces "
  "point towards the other wires, so they add.",
  ["From the middle wire: 2 × 10⁻⁷ × 100/0.10 = 2 × 10⁻⁴ N/m",
   "From the far wire: 2 × 10⁻⁷ × 100/0.20 = 1 × 10⁻⁴ N/m", "Net = 3 × 10⁻⁴ N/m, towards the middle"],
  why="4 × 10⁻⁴ N/m places the far wire at 10 cm. 2 × 10⁻⁴ N/m leaves out the far wire. Zero is the net force on "
      "the middle wire, not on an outer one.",
  ncert=MC + "magnetic force between two parallel currents, the ampere", seconds=60, rc=True)

close(math.sqrt(2 * 2) / math.sqrt(2), math.sqrt(2))   # r = √(2mK)/(qB) ∝ √K
q(MAG, "Force on charges and conductors", "Intermediate", "direct",
  "A charged particle moves in a circle at right angles to a uniform magnetic field. If its kinetic energy is "
  "doubled, the field being unchanged, then:",
  *opt("the radius becomes √2 times and the time period of revolution is unchanged",
       ["the radius doubles and the time period of revolution is unchanged",
        "the radius becomes √2 times and the time period becomes 1/√2 times",
        "the radius is unchanged and the time period is halved"], "B"),
  "r = mv/(qB) = √(2mK)/(qB); T = 2πm/(qB)",
  "Doubling the kinetic energy makes the speed √2 times. The radius is proportional to the speed, so it becomes √2 "
  "times. The period does not depend on the speed at all.",
  ["K × 2 → v × √2", "r ∝ v → r × √2", "T = 2πm/qB → unchanged"],
  why="The radius is proportional to the speed (√K), not to K. The period depends only on m, q and B, so it does not "
      "change.",
  ncert=MC + "motion in a magnetic field", seconds=40)

q(MAG, "Force on charges and conductors", "Intermediate", "assertion_reason",
  ar("When a steady current is passed through a loosely wound, flexible long solenoid, the solenoid tends to "
     "contract along its length.",
     "Adjacent turns of the solenoid carry currents in the same direction, and parallel currents in the same "
     "direction attract each other."),
  AR, ar_key(True, True, True),
  "Force between parallel currents",
  "Neighbouring turns of a solenoid are side by side and their currents flow the same way round. Parallel currents "
  "in the same direction attract, so the turns pull towards one another and the solenoid shortens. R explains A.",
  ["Adjacent turns: currents in the same direction", "Same-direction currents attract",
   "Turns pull together → contraction"],
  why="Both statements are true and the attraction between neighbouring turns is the cause of the contraction, so R "
      "is the correct explanation of A.",
  ncert=MC + "magnetic force between two parallel currents, the ampere", seconds=40)

truth_tube = {"a": True, "b": True, "c": False, "d": True, "e": False}
q(MAG, "Ampere's law", "Intermediate", "multi_statement",
  ms("A long, straight, thin-walled hollow metal tube of radius R carries a steady current I along its length, the "
     "current being spread uniformly round its circumference. Which of the following statements are correct?",
     ["The magnetic field is zero at every point in the hollow space inside the tube.",
      "At a distance r (r > R) from the axis, the magnitude of the field is µ₀I/(2πr).",
      "If the current in the tube is doubled, the field inside the hollow space becomes non-zero.",
      "Outside the tube, the magnetic field lines are circles centred on the axis of the tube.",
      "At a fixed distance r (r > R) from the axis, the field depends on the radius R of the tube."]),
  *mso(truth_tube, "abd", ["ab", "abde", "bcd"], "C"),
  "Ampere's circuital law with a circular Amperian loop coaxial with the tube",
  "A circular loop of radius r < R inside the hollow space encloses no current, so B × 2πr = 0 and B = 0 for any "
  "current (a true, c false). A loop of radius r > R encloses the whole current I, so B = µ₀I/(2πr), the same as "
  "for a thin wire on the axis and independent of R (b true, e false). By symmetry the field lines outside are "
  "circles centred on the axis (d true).",
  ["r < R: I_enclosed = 0 → B = 0", "r > R: B × 2πr = µ₀I → B = µ₀I/2πr", "Field lines: coaxial circles"],
  why="Options containing (c) or (e) include a false statement; (a) and (b) only leaves out the true statement (d).",
  ncert=MC + "Ampere's circuital law", seconds=70)

q(MAG, "Magnetic dipole and bar magnet", "Intermediate", "statement_pair",
  sp("At large distances, the magnetic field lines of a bar magnet have the same pattern as the electric field lines "
     "of an electric dipole.",
     "Like the electric field lines of an electric dipole, the magnetic field lines of a bar magnet begin on its "
     "north pole and end on its south pole."),
  SP, sp_key(True, False),
  "Bar magnet as a magnetic dipole; magnetic field lines form closed loops",
  "Far from a bar magnet, its field has the same form as the field of an electric dipole, with m in place of p "
  "and µ₀/4π in place of 1/4πε₀ (Statement I true). But magnetic field lines do not begin or end anywhere: they "
  "pass through the magnet from S to N and form continuous closed loops, unlike electric field lines, which begin "
  "on positive charges and end on negative charges (Statement II false).",
  ["Far field of a bar magnet ≅ dipole field → I true", "Magnetic field lines are closed loops → II false"],
  why="Statement II describes electric field lines; magnetic field lines continue inside the magnet, so it is false.",
  ncert=MM + "the bar magnet (the electrostatic analog; magnetic field lines)", seconds=40)

# ---- Advanced
a_h, b_h, I_h, r_h = 0.02, 0.04, 6.0, 0.03
I_enc = I_h * (r_h ** 2 - a_h ** 2) / (b_h ** 2 - a_h ** 2)
B_h = MU0 * I_enc / (2 * math.pi * r_h)
close(I_enc, 2.5)
close(B_h, 1.67e-5, 3e-3)
close(MU0 * I_h / (2 * math.pi * r_h), 4.0e-5)
close(MU0 * (I_h * (r_h - a_h) / (b_h - a_h)) / (2 * math.pi * r_h), 2.0e-5)
q(MAG, "Ampere's law", "Advanced", "numerical",
  "A long straight hollow cylindrical conductor has an inner radius of 2.0 cm and an outer radius of 4.0 cm. It "
  "carries a steady current of 6.0 A along its length, spread uniformly over the cross-section of its wall. Taking "
  "µ₀ = 4π × 10⁻⁷ T m A⁻¹, the magnitude of the magnetic field at a distance of 3.0 cm from its axis is about:",
  *opt("1.7 × 10⁻⁵ T", ["4.0 × 10⁻⁵ T", "2.0 × 10⁻⁵ T", "zero"], "B"),
  "Ampere's circuital law: B × 2πr = µ₀ × (current enclosed by the circle of radius r)",
  "The current density is uniform over the annular cross-section, so the current enclosed by a circle of radius r "
  "is in proportion to the area of the wall inside that circle: (r² − a²)/(b² − a²) of the total.",
  ["I_enc = 6.0 × (3² − 2²)/(4² − 2²) = 6.0 × 5/12 = 2.5 A",
   "B = µ₀I_enc/(2πr) = (2 × 10⁻⁷ × 2.5)/0.03 ≈ 1.7 × 10⁻⁵ T"],
  why="4.0 × 10⁻⁵ T uses the whole 6.0 A. 2.0 × 10⁻⁵ T takes the enclosed current in proportion to (r − a)/(b − a) "
      "instead of the areas. Zero would be correct only in the hollow region (r < 2.0 cm).",
  ncert=MC + "Ampere's circuital law", seconds=100, rc=True)

m_r, g_, th, B_r, L_r = 0.10, 10, 45, 0.50, 0.50
I_r = m_r * g_ * math.tan(rad(th)) / (B_r * L_r)
close(I_r, 4.0)
close(m_r * g_ * math.sin(rad(th)) / (B_r * L_r), 2.83, 1e-3)
close(m_r * g_ / (B_r * L_r * math.cos(rad(th))), 5.66, 1e-3)
q(MAG, "Force on charges and conductors", "Advanced", "numerical",
  "Two parallel conducting rails, 0.50 m apart, lie on a smooth plane inclined at 45° to the horizontal, running "
  "straight down the slope. A metal rod of mass 0.10 kg rests across the rails, horizontal and perpendicular to "
  "them. A uniform vertical magnetic field of 0.50 T acts in the region. Taking g = 10 m/s², the current that must "
  "be passed through the rod, in the proper direction, to keep it at rest is:",
  *opt("4.0 A", ["2.8 A", "5.7 A", "zero, because a vertical field cannot push the rod along the slope"], "C"),
  "Force on a current-carrying rod F = BIL; equilibrium on a smooth incline",
  "The rod is horizontal and the field vertical, so the magnetic force BIL is horizontal and perpendicular to the "
  "rod. Its component up the slope is BIL cos 45°, which must balance the component of the weight down the slope, "
  "mg sin 45°.",
  ["BIL cos θ = mg sin θ", "I = mg tan θ/(BL) = (0.10 × 10 × 1)/(0.50 × 0.50)", "I = 4.0 A"],
  why="2.8 A balances mg sin θ with the whole of BIL, as if the magnetic force acted along the slope. 5.7 A balances "
      "BIL cos θ against the whole weight. A horizontal force does have a component along the slope, so zero is "
      "wrong.",
  ncert=MC + "magnetic force on a current-carrying conductor", seconds=100, rc=True)

Ig = (F(5, 2) - 1) / (400 - 100)
G_ = 1 / Ig - 100
assert Ig == F(1, 200) and G_ == 100
assert 1 / Ig == 200 and F(1, 100) == F(1, 100) and 1 / F(5, 2 * 400) - 100 == 60
q(MAG, "Torque on loop and galvanometer", "Advanced", "numerical",
  "A galvanometer in series with a 100 Ω resistor gives full-scale deflection when a potential difference of 1.0 V "
  "is applied across the combination. With a 400 Ω resistor in place of the 100 Ω resistor, full-scale deflection "
  "needs 2.5 V. The resistance of the galvanometer and its full-scale current are, respectively:",
  *opt("100 Ω and 5 mA", ["200 Ω and 5 mA", "100 Ω and 10 mA", "60 Ω and 6.25 mA"], "D"),
  "Galvanometer as a voltmeter: V = I_g(G + R)",
  "The same full-scale current I_g flows in both cases. Subtracting the two equations eliminates G.",
  ["I_g(G + 100) = 1.0 and I_g(G + 400) = 2.5", "Subtract: 300 I_g = 1.5 → I_g = 5 mA",
   "G + 100 = 1.0/0.005 = 200 → G = 100 Ω"],
  why="200 Ω is G + 100, the total resistance in the first case. 10 mA divides 1.0 V by the 100 Ω resistor alone. "
      "60 Ω and 6.25 mA take I_g as 2.5 V/400 Ω, ignoring the galvanometer's own resistance.",
  ncert=MC + "moving coil galvanometer", seconds=90, rc=True)

m_p, q_p, v_p, B_p = 1.6e-27, 1.6e-19, 2e6, 0.5
r_p = m_p * v_p / (q_p * B_p)
t90 = (math.pi / 2) * m_p / (q_p * B_p)
close(r_p, 0.04)
close(t90, math.pi * 1e-8)
close(math.sqrt(2) * r_p, 0.0566, 1e-3)
close(math.pi * r_p / 2, 0.0628, 1e-3)
q(MAG, "Force on charges and conductors", "Advanced", "numerical",
  "A proton (mass 1.6 × 10⁻²⁷ kg, charge 1.6 × 10⁻¹⁹ C) moving with a speed of 2.0 × 10⁶ m/s enters a region of "
  "uniform magnetic field of 0.50 T, its velocity being perpendicular to the field. The time it takes for its "
  "direction of motion to turn through 90°, and the magnitude of its displacement during this time, are:",
  *opt("π × 10⁻⁸ s and 5.7 cm", ["π × 10⁻⁸ s and 6.3 cm", "2π × 10⁻⁸ s and 5.7 cm", "4π × 10⁻⁸ s and 8.0 cm"],
       "A"),
  "Circular motion in a magnetic field: r = mv/(qB), angular speed ω = qB/m",
  "The velocity turns at the constant rate ω = qB/m, so turning through π/2 takes a quarter of the period. In that "
  "time the proton moves along a quarter circle, and its displacement is the chord joining the ends of the quarter "
  "circle, √2 r.",
  ["r = (1.6 × 10⁻²⁷ × 2 × 10⁶)/(1.6 × 10⁻¹⁹ × 0.5) = 0.04 m = 4 cm",
   "t = (π/2)(m/qB) = (π/2) × 2 × 10⁻⁸ = π × 10⁻⁸ s", "Displacement = √2 × 4 cm ≈ 5.7 cm"],
  why="6.3 cm is the length of the quarter-circle arc (distance travelled), not the displacement. 2π × 10⁻⁸ s is "
      "half a period. 4π × 10⁻⁸ s and 8.0 cm are the full period and the diameter.",
  ncert=MC + "motion in a magnetic field", seconds=100, rc=True)

q(MAG, "Torque on loop and galvanometer", "Advanced", "assertion_reason",
  ar("Using a spring of smaller torsional constant k in a moving-coil galvanometer increases its current sensitivity "
     "but decreases its voltage sensitivity.",
     "Both the current sensitivity (NAB/k) and the voltage sensitivity (NAB/kR) of a moving-coil galvanometer are "
     "inversely proportional to k."),
  AR, ar_key(False, True),
  "Current sensitivity φ/I = NAB/k; voltage sensitivity φ/V = NAB/(kR)",
  "Making k smaller increases both sensitivities, because both contain k in the denominator and the coil's "
  "resistance R is not changed by changing the spring. A is therefore false, while R is a correct statement.",
  ["Current sensitivity ∝ 1/k → increases", "Voltage sensitivity ∝ 1/(kR), R unchanged → increases",
   "A false, R true"],
  why="A confuses the spring with the number of turns: increasing N raises R as well, which is why it does not "
      "raise the voltage sensitivity. Changing k leaves R unchanged, so both sensitivities rise.",
  ncert=MC + "moving coil galvanometer", seconds=50)

kq = F(1)
assert (2 * kq, kq, 2 * kq / 8, kq / 8) == (2, 1, F(1, 4), F(1, 8))
q(MAG, "Magnetic dipole and bar magnet", "Advanced", "match_list",
  ml("A short bar magnet of magnetic moment m is placed with its centre at the origin. Writing k = µ₀/4π and "
     "ignoring all other magnetic fields, match each point in List-I with the magnitude of the field there in "
     "List-II.",
     ["On the axis of the magnet, at a distance r from its centre",
      "On the equatorial line (perpendicular bisector of the axis), at a distance r from the centre",
      "On the axis of the magnet, at a distance 2r from its centre",
      "On the equatorial line, at a distance 2r from the centre"],
     ["km/r³", "2km/r³", "km/(8r³)", "km/(4r³)"]),
  *mlo("A-II, B-I, C-IV, D-III", ["A-I, B-II, C-III, D-IV", "A-II, B-I, C-III, D-IV", "A-II, B-IV, C-I, D-III"],
       "B"),
  "Field of a short magnet: axial 2km/r³, equatorial km/r³ (both ∝ 1/r³)",
  "At equal distances the axial field is twice the equatorial field. Doubling the distance divides each by 2³ = 8.",
  ["A: 2km/r³", "B: km/r³", "C: 2km/(2r)³ = km/(4r³)", "D: km/(2r)³ = km/(8r³)"],
  why="A-I, B-II, C-III, D-IV interchanges the axial and equatorial fields. A-II, B-I, C-III, D-IV forgets the "
      "factor 2 of the axial field at 2r and so interchanges the two values at 2r. A-II, B-IV, C-I, D-III mixes up "
      "the fields at r and at 2r on the equatorial line.",
  ncert=MM + "the bar magnet (field of a magnetic dipole)", seconds=60, rc=True)


# ================================================================ EMI and AC (B4 I6 A4)
EC = NC + "'Electromagnetic Induction', "
ACC = NC + "'Alternating Current', "

# ---- Basic
phi = lambda t: 3 * t ** 2 - 4 * t          # mWb
dphi = lambda t: 6 * t - 4                  # mWb/s = mV
assert dphi(2) == 8 and phi(2) == 4 and 6 * 2 == 12 and phi(2) / 2 == 2
q(EMI, "Faraday's and Lenz's laws", "Basic", "numerical",
  "The magnetic flux linked with a single-turn closed loop varies with time as Φ = (3t² − 4t) mWb, where t is in "
  "seconds. The magnitude of the emf induced in the loop at t = 2 s is:",
  *opt("8 mV", ["4 mV", "12 mV", "2 mV"], "A"),
  "Faraday's law: ε = −dΦ/dt",
  "The induced emf depends on the rate of change of the flux at that instant, not on the flux itself.",
  ["dΦ/dt = (6t − 4) mWb/s", "At t = 2 s: 6 × 2 − 4 = 8 mWb/s", "|ε| = 8 mV"],
  why="4 mV is the value of the flux at t = 2 s, not its rate of change. 12 mV differentiates only the 3t² term. "
      "2 mV divides the flux by the time.",
  ncert=EC + "Faraday's law of induction", seconds=35, rc=True)

B_x, r_x, drdt = 0.5, 0.10, 0.002
emf_x = B_x * 2 * math.pi * r_x * drdt
close(emf_x, 6.28e-4, 1e-3)
close(B_x * math.pi * r_x * drdt, 3.14e-4, 1e-3)
close(B_x * r_x * drdt, 1.0e-4)
close(B_x * 4 * math.pi * r_x * drdt, 1.26e-3, 3e-3)
q(EMI, "Faraday's and Lenz's laws", "Basic", "numerical",
  "A flexible circular conducting loop lies with its plane perpendicular to a uniform magnetic field of 0.50 T. Its "
  "radius is increasing at a steady rate of 2.0 mm/s. The magnitude of the emf induced in the loop at the instant "
  "when its radius is 10 cm is about:",
  *opt("0.63 mV", ["0.31 mV", "0.10 mV", "1.3 mV"], "B"),
  "Faraday's law with a changing area: ε = B dA/dt",
  "The field is constant, so the flux changes only because the area πr² changes. dA/dt = 2πr (dr/dt).",
  ["dA/dt = 2πr dr/dt = 2π × 0.10 × 0.002 = 1.26 × 10⁻³ m²/s", "ε = B dA/dt = 0.50 × 1.26 × 10⁻³ ≈ 6.3 × 10⁻⁴ V"],
  why="0.31 mV takes dA/dt as πr dr/dt (dropping the factor 2 of the derivative of r²). 0.10 mV leaves out 2π. 1.3 mV "
      "doubles the correct value.",
  ncert=EC + "Faraday's law of induction", seconds=45, rc=True)

q(EMI, "Faraday's and Lenz's laws", "Basic", "statement_pair",
  sp("For a given rate of change of magnetic flux through a closed coil, the induced emf does not depend on the "
     "resistance of the coil, but the induced current does.",
     "An emf is induced by a changing magnetic flux only if the loop through which the flux changes is made of a "
     "conducting material."),
  SP, sp_key(True, False),
  "Faraday's law gives the emf; the current follows from Ohm's law",
  "The induced emf equals the rate of change of flux linkage, whatever the coil is made of; the current is this emf "
  "divided by the resistance (Statement I true). The emf is induced round any closed path through which the flux "
  "changes; a conducting loop is needed only for a current to flow (Statement II false).",
  ["ε = −N dΦ/dt: independent of R", "I = ε/R: depends on R", "Emf exists even without a conductor"],
  why="Statement II confuses the emf with the current: a non-conducting ring has the same emf but no current.",
  ncert=EC + "Faraday's law of induction", seconds=40)

q(EMI, "Faraday's and Lenz's laws", "Basic", "direct",
  "The magnetic flux through a closed coil of fixed resistance increases steadily (linearly) with time from zero. "
  "While the flux is increasing, the current induced in the coil:",
  *opt("is constant and non-zero",
       ["increases linearly with time", "is zero, because the flux starts from zero",
        "decreases steadily to zero"], "D"),
  "Faraday's law: the emf depends on the rate of change of flux",
  "A flux that rises linearly has a constant rate of change, so the induced emf is constant, and with a fixed "
  "resistance so is the current.",
  ["Φ = kt → dΦ/dt = k (constant)", "ε = −k → I = ε/R = constant"],
  why="The current follows the rate of change of the flux, not the flux itself, so it neither grows with the flux "
      "nor is zero when the flux starts from zero. A constant rate gives no decrease.",
  ncert=EC + "Faraday's law of induction", seconds=25)

# ---- Intermediate
B_rod, w_rod, l_rod = 0.5, 20, 0.4
half = B_rod * w_rod * (l_rod / 2) ** 2 / 2
close(half, 0.2)
assert half - half == 0
close(B_rod * w_rod * l_rod ** 2 / 2, 0.8)
q(EMI, "Faraday's and Lenz's laws", "Intermediate", "numerical",
  "A metal rod 0.4 m long rotates with an angular speed of 20 rad/s about an axis passing through its midpoint and "
  "perpendicular to the rod. A uniform magnetic field of 0.5 T acts parallel to the axis of rotation. The potential "
  "difference between the two ends of the rod is:",
  *opt("zero", ["0.8 V", "0.2 V", "0.4 V"], "B"),
  "Motional emf of a rotating rod: ε = ½Bωl² between the axis and the end of a length l",
  "Each half of the rod (length 0.2 m) has an emf ½Bω(0.2)² = 0.2 V between the midpoint and its outer end. Both "
  "outer ends are at the same potential relative to the midpoint (both higher, or both lower), so the potential "
  "difference between the two ends is zero.",
  ["Each half: ½ × 0.5 × 20 × 0.2² = 0.2 V, midpoint to end", "Both ends are 0.2 V from the midpoint in the same "
   "sense", "V(end 1) − V(end 2) = 0"],
  why="0.8 V is the emf for rotation about one end. 0.2 V is the potential difference between the midpoint and "
      "either end. 0.4 V adds the two halves as if they were in series.",
  ncert=EC + "motional electromotive force", seconds=50, rc=True)

R_pf, X_pf = 4, 3
pf1 = R_pf / math.hypot(R_pf, X_pf)
pf2 = R_pf / math.hypot(R_pf, 2 * X_pf)
close(pf1, 0.8)
close(pf2, 0.555, 2e-3)
close(R_pf / math.hypot(R_pf, X_pf / 2), 0.936, 2e-3)
q(EMI, "LCR resonance and power", "Intermediate", "numerical",
  "A resistor and an inductor are connected in series to an AC source. At a source frequency of 50 Hz the power "
  "factor of the circuit is 0.80. If the frequency is changed to 100 Hz, the components and the source voltage "
  "being unchanged, the power factor becomes about:",
  *opt("0.55", ["0.40", "0.94", "0.80"], "D"),
  "Power factor of an LR circuit: cos φ = R/√(R² + X_L²), with X_L = ωL ∝ f",
  "A power factor of 0.80 means R : X_L = 4 : 3 at 50 Hz. Doubling the frequency doubles X_L but leaves R "
  "unchanged.",
  ["At 50 Hz: R = 4k, X_L = 3k (so that cos φ = 4/5)", "At 100 Hz: X_L = 6k",
   "cos φ = 4/√(16 + 36) = 4/7.21 ≈ 0.55"],
  why="0.40 halves the power factor, as if it were inversely proportional to the frequency. 0.94 halves X_L, as for "
      "a capacitor. 0.80 assumes the power factor does not depend on frequency.",
  ncert=ACC + "LCR series circuit (impedance, phase); power in AC circuit: the power factor", seconds=70, rc=True)

M_, I0_, w_ = 0.10, 2.0, 100 * math.pi
e_pk = M_ * I0_ * w_
close(e_pk, 62.8, 1e-3)
close(e_pk / math.sqrt(2), 44.4, 1e-3)
q(EMI, "Self and mutual inductance", "Intermediate", "numerical",
  "The mutual inductance of a pair of coils is 0.10 H. The current in the first coil varies as i₁ = 2.0 sin(100πt) "
  "A, with t in seconds. The peak value of the emf induced in the second coil is about:",
  *opt("62.8 V", ["0.20 V", "20 V", "44.4 V"], "A"),
  "Mutual induction: ε₂ = −M di₁/dt",
  "Differentiating i₁ = I₀ sin ωt gives I₀ω cos ωt, so the induced emf oscillates with peak value MI₀ω.",
  ["di₁/dt = 2.0 × 100π cos(100πt)", "ε₀ = MI₀ω = 0.10 × 2.0 × 100π", "ε₀ ≈ 62.8 V"],
  why="0.20 V is MI₀, without the factor ω. 20 V uses ω = 100 instead of 100π rad/s. 44.4 V is the rms value of "
      "the emf, not its peak.",
  ncert=EC + "inductance (mutual inductance)", seconds=50, rc=True)

q(EMI, "AC generator and transformer", "Intermediate", "assertion_reason",
  ar("When the load connected to the secondary of an ideal transformer draws a larger current, the current drawn by "
     "the primary from the supply also increases.",
     "An ideal transformer is 100% efficient only when no load is connected to its secondary."),
  AR, ar_key(True, False),
  "Ideal transformer: output power = input power, V_s I_s = V_p I_p",
  "For an ideal transformer the input power equals the output power at every load, and the voltages are fixed by "
  "the supply and the turns ratio. A larger secondary current therefore means a larger primary current, "
  "I_p = (V_s/V_p) I_s (A true). An ideal transformer has no losses at any load, so R is false.",
  ["V_p I_p = V_s I_s", "V_p, V_s fixed → I_p ∝ I_s", "Ideal: 100% efficient at every load → R false"],
  why="R is false: 'ideal' means no losses whatever the load. So the options that call R true are wrong.",
  ncert=ACC + "transformers", seconds=40)

q(EMI, "AC generator and transformer", "Intermediate", "statement_pair",
  sp("In an AC generator, the ends of the rotating coil are connected to the external circuit through slip rings "
     "and brushes.",
     "The frequency of the alternating emf produced by an AC generator does not depend on the number of turns in its "
     "coil."),
  SP, sp_key(True, True),
  "AC generator: ε = NBAω sin ωt",
  "The coil turns continuously, so its ends are connected to rotating slip rings on which fixed carbon brushes "
  "press, connecting the coil to the outside circuit (Statement I true). The emf varies as sin ωt, where ω is the "
  "angular speed of rotation; the number of turns N affects only the amplitude NBAω (Statement II true).",
  ["Slip rings + brushes connect the rotating coil → I true", "Frequency = ω/2π; N changes only the peak emf → "
   "II true"],
  why="Both statements are correct, so options calling either of them false are wrong.",
  ncert=EC + "AC generator", seconds=35)

q(EMI, "Self and mutual inductance", "Intermediate", "match_list",
  ml("Match each physical quantity in List-I with an equivalent form of its SI unit in List-II.",
     ["Inductance", "Magnetic flux", "Reactance", "Capacitance"],
     ["V s", "V s A⁻¹", "A s V⁻¹", "V A⁻¹"]),
  *mlo("A-II, B-I, C-IV, D-III", ["A-I, B-II, C-IV, D-III", "A-II, B-I, C-III, D-IV", "A-IV, B-I, C-II, D-III"],
       "B"),
  "Units from defining relations: ε = −dΦ/dt, ε = −L dI/dt, X = V/I, C = Q/V",
  "From ε = −dΦ/dt, flux has the unit of emf × time, V s (the weber). From ε = −L dI/dt, inductance has the unit "
  "V s A⁻¹ (the henry). A reactance is a ratio of voltage to current, V A⁻¹ (ohm). Capacitance is charge per unit "
  "voltage, A s V⁻¹ (farad).",
  ["Φ: V s", "L: V s A⁻¹", "X: V A⁻¹", "C: A s V⁻¹"],
  why="A-I, B-II, ... interchanges the units of inductance and flux. A-II, B-I, C-III, D-IV interchanges reactance and "
      "capacitance. A-IV, ... gives inductance the unit of resistance.",
  ncert=EC + "inductance; " + "Faraday's law of induction", seconds=50)

# ---- Advanced
B_l, L_l, v_l, R_l = 0.5, 0.10, 2.0, 0.5
emf_l = B_l * L_l * v_l
I_l = emf_l / R_l
F_l = B_l * I_l * L_l
W_l = F_l * L_l
close(emf_l, 0.1)
close(F_l, 0.01)
close(W_l, 1.0e-3)
q(EMI, "Faraday's and Lenz's laws", "Advanced", "numerical",
  "A square conducting loop of side 10 cm and resistance 0.50 Ω lies in a plane perpendicular to a uniform magnetic "
  "field of 0.50 T, which fills the region on one side of a straight boundary. Initially the loop is entirely "
  "inside the field with one side lying along the boundary. It is pulled out of the field, perpendicular to the "
  "boundary, at a constant speed of 2.0 m/s. The work that must be done to pull it completely out of the field is:",
  *opt("1.0 mJ", ["zero, because the speed is constant", "2.0 mJ", "0.5 mJ"], "C"),
  "Motional emf ε = BLv; opposing force BIL; work = force × distance (equal to the heat produced)",
  "While the loop is leaving, only the side still in the field cuts field lines, so ε = BLv. The induced current "
  "produces a force BIL opposing the motion, and an equal external force is needed to keep the speed constant over "
  "a distance equal to the side L.",
  ["ε = 0.5 × 0.10 × 2.0 = 0.10 V; I = 0.10/0.50 = 0.20 A", "F = BIL = 0.5 × 0.20 × 0.10 = 0.010 N",
   "W = F × L = 0.010 × 0.10 = 1.0 × 10⁻³ J"],
  why="At constant speed the applied force balances the magnetic drag, it is not zero, so work is done (and appears "
      "as heat). 2.0 mJ takes the emf as 2BLv, as if two sides cut the field. 0.5 mJ uses half the force, as if the "
      "force grew from zero.",
  ncert=EC + "motional electromotive force", seconds=100, rc=True)

V_src, V_C = 100, 240
V_coil = math.hypot(V_src, V_C)
close(V_coil, 260)
assert V_src + V_C == 340 and V_C - V_src == 140
q(EMI, "LCR resonance and power", "Advanced", "numerical",
  "A coil (having both resistance and inductance) is connected in series with a capacitor across an AC source of "
  "rms voltage 100 V, and the frequency is adjusted to resonance. An AC voltmeter connected across the capacitor "
  "then reads 240 V. The reading of the voltmeter when it is connected across the coil is:",
  *opt("260 V", ["240 V", "340 V", "140 V"], "D"),
  "Series resonance: V_L = V_C, and the source voltage appears across the resistance; phasor addition",
  "At resonance the inductive and capacitive voltages cancel, so the whole 100 V of the source is across the coil's "
  "resistance. The coil's inductive voltage equals the capacitor voltage, 240 V, and it is 90° ahead of the "
  "resistive voltage, so the two add as phasors.",
  ["At resonance: V_R = V_source = 100 V, V_L = V_C = 240 V", "V_coil = √(V_R² + V_L²) = √(100² + 240²)",
   "V_coil = 260 V"],
  why="240 V ignores the coil's resistance. 340 V adds the two voltages arithmetically, and 140 V subtracts them, "
      "ignoring the 90° phase difference.",
  ncert=ACC + "series LCR circuit (resonance)", seconds=90, rc=True)

n_s, N_c, r_s, r_c = 2000, 100, 0.02, 0.05
M_sol = MU0 * n_s * N_c * math.pi * r_s ** 2
close(M_sol, 3.16e-4, 2e-3)
close(MU0 * n_s * N_c * math.pi * r_c ** 2, 1.97e-3, 3e-3)
close(MU0 * n_s * N_c * r_s ** 2, 1.0e-4, 6e-3)
q(EMI, "Self and mutual inductance", "Advanced", "numerical",
  "A long solenoid of radius 2.0 cm has 2000 turns per metre. A coil of 100 turns and radius 5.0 cm is placed "
  "around the middle of the solenoid, coaxial with it. Taking µ₀ = 4π × 10⁻⁷ T m A⁻¹, the mutual inductance of the "
  "solenoid and the coil is about:",
  *opt("0.32 mH", ["2.0 mH", "0.10 mH", "zero, because the coil lies outside the solenoid, where the field is zero"],
       "A"),
  "Mutual inductance M = N₂Φ₂/I₁, with the flux of the long solenoid confined to its own cross-section",
  "A current I in the solenoid produces B = µ₀nI inside it and practically zero field outside. The flux through "
  "each turn of the larger coil is therefore B × (area of the solenoid), not B × (area of the coil). The coil "
  "surrounds the solenoid, so all of this flux links it.",
  ["Flux per turn = µ₀nI × πr_s²", "M = N µ₀ n π r_s² = 100 × 4π × 10⁻⁷ × 2000 × π × (0.02)²",
   "M ≈ 3.2 × 10⁻⁴ H = 0.32 mH"],
  why="2.0 mH uses the area of the coil, but there is no field between the solenoid and the coil. 0.10 mH leaves π "
      "out of the area. The coil does lie in the field-free region, but it encircles the solenoid's flux, so the "
      "flux linkage is not zero.",
  ncert=EC + "inductance (mutual inductance)", seconds=100, rc=True)

truth_rail = {"a": True, "b": True, "c": False, "d": True, "e": False}
Bz, lz, vz, Rz = 1.0, 1.0, 1.0, 1.0
P_heat = lambda B, v: (B * lz * v) ** 2 / Rz
F_ext = lambda B, v: B ** 2 * lz ** 2 * v / Rz
assert P_heat(Bz, 2 * vz) == 4 * P_heat(Bz, vz) and F_ext(2 * Bz, vz) == 4 * F_ext(Bz, vz)
assert F_ext(Bz, vz) * vz == P_heat(Bz, vz)
q(EMI, "Faraday's and Lenz's laws", "Advanced", "multi_statement",
  ms("A conducting rod slides with a constant velocity v along two parallel, frictionless conducting rails that are "
     "joined at one end through a resistor R. A uniform magnetic field B acts perpendicular to the plane of the "
     "rails. An external agent keeps the velocity constant; the rod and rails have negligible resistance. Which of "
     "the following statements are correct?",
     ["The mechanical power supplied by the external agent equals the rate at which heat is produced in R.",
      "The magnetic force on the rod due to the induced current opposes its motion.",
      "If the resistor is removed so that the circuit is open, the emf between the ends of the rod becomes zero.",
      "Doubling the speed of the rod makes the rate of heating in R four times as large.",
      "Doubling the magnetic field doubles the external force needed to keep the speed constant."]),
  *mso(truth_rail, "abd", ["ab", "abde", "bcd"], "B"),
  "Motional emf ε = Blv; energy conservation and Lenz's law",
  "The induced current I = Blv/R gives a force F = BIl = B²l²v/R opposing the motion (b true, Lenz's law), so the "
  "agent supplies power Fv = B²l²v²/R, equal to I²R (a true). The heating rate ∝ v² (d true) and the force ∝ B² "
  "(e false: it becomes four times). The emf Blv exists across the moving rod whether or not a current flows (c "
  "false).",
  ["I = Blv/R; F = B²l²v/R", "Fv = I²R", "P ∝ v²; F ∝ B²", "Open circuit: emf Blv, current zero"],
  why="Options containing (c) or (e) include a false statement; (a) and (b) only leaves out the true statement (d).",
  ncert=EC + "motional electromotive force; Lenz's law and conservation of energy", seconds=80, rc=True)


# ================================================================ Electromagnetic Waves (B1 I2 A1)
WC = NC + "'Electromagnetic Waves', "

q(EMW, "EM spectrum and uses", "Basic", "direct",
  "Visible sunlight absorbed by the Earth's surface is re-radiated, and part of this re-radiated energy is trapped "
  "by greenhouse gases such as carbon dioxide, keeping the Earth warm (the greenhouse effect). The radiation "
  "re-emitted by the Earth's surface is mainly:",
  *opt("infrared radiation", ["ultraviolet radiation", "X-rays", "microwaves"], "C"),
  "Infrared waves and the greenhouse effect",
  "The Earth's surface, being much cooler than the Sun, re-radiates the absorbed energy at longer wavelengths, in "
  "the infrared. Greenhouse gases absorb this infrared radiation and so keep the Earth warm.",
  ["Absorbed: mainly visible light", "Re-emitted by the cooler surface: longer wavelengths → infrared",
   "Trapped by greenhouse gases"],
  why="Ultraviolet and X-rays have shorter wavelengths than visible light; a cool surface does not emit them. "
      "Microwaves are not the radiation by which the warm surface mainly re-radiates.",
  ncert=WC + "electromagnetic spectrum (infrared waves)", seconds=25)

k_q = 2.0e-6
i_d = 2 * k_q * 3.0
close(i_d, 12e-6)
close(k_q * 9, 18e-6)
close(k_q * 9 / 3, 6e-6)
q(EMW, "Displacement current", "Intermediate", "numerical",
  "While a parallel-plate capacitor is being charged, the charge on its positive plate varies with time as "
  "q = (2.0 × 10⁻⁶ C s⁻²) t². The displacement current in the region between the plates at t = 3.0 s is:",
  *opt("12 µA", ["18 µA", "6 µA", "zero, because no charge crosses the gap between the plates"], "A"),
  "Displacement current i_d = ε₀ dΦ_E/dt, which equals the conduction current dq/dt in the leads",
  "Between the plates the electric flux is q/ε₀, so ε₀ dΦ_E/dt = dq/dt: the displacement current between the plates "
  "equals the rate at which charge is building up on the plates.",
  ["i_d = dq/dt = 2 × 2.0 × 10⁻⁶ × t", "At t = 3.0 s: i_d = 1.2 × 10⁻⁵ A = 12 µA"],
  why="18 µA is the numerical value of the charge (18 µC) at t = 3.0 s, not its rate of change. 6 µA is the average "
      "current q/t over the first 3 s. No charge crosses the gap, but the changing electric field gives a "
      "displacement current equal to the conduction current.",
  ncert=WC + "displacement current", seconds=50, rc=True)

q(EMW, "EM wave properties", "Intermediate", "assertion_reason",
  ar("In a plane electromagnetic wave travelling through vacuum, the oscillating electric and magnetic fields at any "
     "point reach their maximum values at the same instant.",
     "Electromagnetic waves are transverse: the electric and magnetic fields are perpendicular to the direction of "
     "propagation of the wave."),
  AR, ar_key(True, True, False),
  "Plane EM wave: E_x = E₀ sin(kz − ωt), B_y = B₀ sin(kz − ωt)",
  "In a plane wave in vacuum, E and B vary with the same phase (kz − ωt), so they are in phase and have their "
  "maxima together, with E₀ = cB₀ (A true). The fields are also perpendicular to the direction of propagation (R "
  "true). But being transverse is a statement about directions; it does not say anything about the relative phase "
  "of E and B, so R does not explain A.",
  ["Same phase (kz − ωt) for E and B → A true", "E, B ⊥ direction of propagation → R true",
   "Direction (R) ≠ phase (A) → R not the explanation"],
  why="Both statements are true, but the transverse nature of the wave concerns the directions of the fields, not "
      "the instants at which they peak, so R is not the explanation of A.",
  ncert=WC + "electromagnetic waves (nature of electromagnetic waves)", seconds=45)

E0_, B0_, f_ = 30.0, 1.5e-7, 5.0e14
v_m = E0_ / B0_
n_m = 3e8 / v_m
lam_m = v_m / f_
close(v_m, 2e8)
close(n_m, 1.5)
close(lam_m, 400e-9)
close(3e8 / f_, 600e-9)
close(3e8 / f_ * n_m, 900e-9)
q(EMW, "EM wave properties", "Advanced", "numerical",
  "A plane electromagnetic wave of frequency 5.0 × 10¹⁴ Hz travels through a transparent, non-magnetic medium. The "
  "amplitudes of its electric and magnetic fields are 30 V/m and 1.5 × 10⁻⁷ T. Taking c = 3 × 10⁸ m/s, the "
  "refractive index of the medium and the wavelength of the wave in the medium are, respectively:",
  *opt("1.5 and 400 nm", ["1.5 and 600 nm", "0.67 and 400 nm", "1.5 and 900 nm"], "D"),
  "In a medium, E₀/B₀ = v (the wave speed in the medium); n = c/v; λ = v/f",
  "The ratio of the field amplitudes gives the speed of the wave in the medium. The refractive index is c/v, and "
  "the wavelength in the medium is v/f (the frequency is the same as in vacuum).",
  ["v = E₀/B₀ = 30/(1.5 × 10⁻⁷) = 2.0 × 10⁸ m/s", "n = 3 × 10⁸/2 × 10⁸ = 1.5",
   "λ = v/f = 2.0 × 10⁸/5.0 × 10¹⁴ = 4.0 × 10⁻⁷ m = 400 nm"],
  why="600 nm is the wavelength in vacuum (c/f). 0.67 is v/c, the reciprocal of the refractive index. 900 nm "
      "multiplies the vacuum wavelength by n instead of dividing.",
  ncert=WC + "electromagnetic waves", seconds=70, rc=True)


# ================================================================ Optics (B7 I9 A7)
RO = NC + "'Ray Optics and Optical Instruments', "
WO = NC + "'Wave Optics', "

# ---- Basic
n1 = math.sqrt(1.5)
r1 = deg(math.asin(math.sin(rad(60)) / n1))
close(r1, 45)
close(180 - 60 - r1, 75)
q(OPT, "Refraction and lenses", "Basic", "numerical",
  "A ray of light in air falls at an angle of incidence of 60° on the plane surface of a transparent medium of "
  "refractive index √(3/2) (about 1.22). Part of the light is reflected and part is refracted. The angle between "
  "the reflected ray and the refracted ray is:",
  *opt("75°", ["105°", "15°", "90°"], "A"),
  "Law of reflection and Snell's law",
  "The reflected ray makes 60° with the normal on the air side. Snell's law gives the angle of refraction. The two "
  "rays lie on opposite sides of the surface, so the angle between them is 180° − (angle of reflection + angle of "
  "refraction).",
  ["sin r = sin 60°/√(3/2) = (√3/2)(√2/√3) = 1/√2 → r = 45°", "Angle between the rays = 180° − 60° − 45° = 75°"],
  why="105° adds the two angles made with the normal. 15° is the deviation of the refracted ray (i − r). 90° would "
      "be correct only at the polarising (Brewster) angle, which here is not 60°.",
  ncert=RO + "refraction", seconds=50, rc=True)

v_glass = 3e8 * math.sin(rad(30)) / math.sin(rad(60))
close(v_glass, 1.73e8, 2e-3)
close(3e8 * math.sin(rad(60)) / math.sin(rad(30)), 5.2e8, 2e-3)
close(3e8 * math.cos(rad(30)), 2.6e8, 2e-3)
q(OPT, "Huygens' principle and interference", "Basic", "numerical",
  "A plane wavefront of light travelling in air (speed 3.0 × 10⁸ m/s) meets the plane surface of a glass block. "
  "The incident wavefront makes an angle of 60° with the surface, and the refracted wavefront inside the glass "
  "makes an angle of 30° with the surface. The speed of light in the glass is about:",
  *opt("1.7 × 10⁸ m/s", ["5.2 × 10⁸ m/s", "1.5 × 10⁸ m/s", "2.6 × 10⁸ m/s"], "B"),
  "Refraction of a plane wave by Huygens' construction: sin i/sin r = v₁/v₂",
  "The angle between a wavefront and the surface equals the angle between the corresponding ray and the normal, so "
  "i = 60° and r = 30°. In the time the incident wavefront moves a distance v₁t in air, the secondary wavelet in "
  "glass grows to radius v₂t, which gives sin i/sin r = v₁/v₂.",
  ["i = 60°, r = 30°", "v₂ = v₁ sin r/sin i = 3.0 × 10⁸ × 0.5/0.866", "v₂ ≈ 1.7 × 10⁸ m/s"],
  why="5.2 × 10⁸ m/s inverts the ratio and exceeds the speed of light in vacuum. 1.5 × 10⁸ m/s uses the ratio of the "
      "angles (30°/60°) instead of their sines. 2.6 × 10⁸ m/s multiplies by cos 30° instead of using the sine "
      "ratio.",
  ncert=WO + "refraction and reflection of plane waves using Huygens principle", seconds=50, rc=True)

beta0 = F(1, 2)
beta1 = beta0 * 2 / F(1, 2)
assert beta1 == 2
q(OPT, "Huygens' principle and interference", "Basic", "numerical",
  "In Young's double-slit experiment the fringe width is 0.5 mm. If the separation between the slits is halved and "
  "the distance between the slits and the screen is doubled, the wavelength being unchanged, the new fringe width "
  "is:",
  *opt("2.0 mm", ["0.5 mm", "1.0 mm", "0.125 mm"], "C"),
  "Fringe width β = λD/d",
  "The fringe width is proportional to D and inversely proportional to d. Doubling D doubles β, and halving d "
  "doubles it again.",
  ["β' = β × (D'/D) × (d/d')", "β' = 0.5 × 2 × 2 = 2.0 mm"],
  why="0.5 mm assumes the two changes cancel. 1.0 mm applies only one of the two changes. 0.125 mm takes β as "
      "proportional to d and inversely proportional to D.",
  ncert=WO + "interference of light waves and Young's experiment", seconds=30, rc=True)

lam0, ng, t_g = 600e-9, 1.5, 1.0e-3
N_w = t_g / (lam0 / ng)
close(N_w, 2500)
close(t_g / lam0, 1667, 1e-3)
close(t_g / (lam0 * ng), 1111, 1e-3)
q(OPT, "Refraction and lenses", "Basic", "numerical",
  "Light of wavelength 600 nm in vacuum passes normally through a glass plate 1.0 mm thick, of refractive index "
  "1.5. The number of wavelengths of the light contained in the thickness of the plate is:",
  *opt("2500", ["1667", "1111", "3750"], "D"),
  "On entering a medium of refractive index n, the frequency is unchanged and the wavelength becomes λ₀/n",
  "Inside the glass the wavelength is 600/1.5 = 400 nm. The number of wavelengths in the plate is its thickness "
  "divided by this wavelength.",
  ["λ (glass) = 600/1.5 = 400 nm", "N = 1.0 × 10⁻³/(4.0 × 10⁻⁷) = 2500"],
  why="1667 uses the vacuum wavelength. 1111 multiplies the wavelength by n instead of dividing. 3750 multiplies "
      "the correct number by n once more.",
  ncert=RO + "refraction", seconds=40, rc=True)

q(OPT, "Huygens' principle and interference", "Basic", "direct",
  "A plane wavefront travelling along the principal axis falls on a concave mirror of small aperture. The "
  "reflected wavefront is:",
  *opt("spherical, converging to the focus of the mirror",
       ["plane, travelling back along the axis", "spherical, diverging from a point behind the mirror",
        "cylindrical, converging to a line through the pole"], "A"),
  "Wavefronts and rays: rays are normal to wavefronts",
  "A concave mirror reflects rays parallel to its axis so that they converge to its focus. The surfaces normal to "
  "these converging rays are spheres centred on the focus, shrinking as they approach it: a converging spherical "
  "wavefront.",
  ["Parallel rays → reflected towards F", "Wavefront ⊥ rays → spherical, centred on F, converging"],
  why="A plane mirror would return a plane wavefront. A diverging spherical wavefront from a point behind the mirror "
      "is produced by a convex mirror. A spherical mirror does not produce a cylindrical wavefront.",
  ncert=WO + "Huygens principle (wavefronts)", seconds=30)

q(OPT, "Refraction and lenses", "Basic", "statement_pair",
  sp("The power of a lens is measured in dioptres, a lens of focal length 1 m having a power of 1 D.",
     "A converging (convex) lens has a negative power."),
  SP, sp_key(True, False),
  "Power of a lens P = 1/f (f in metres)",
  "P = 1/f, so 1 D = 1 m⁻¹ and a lens of focal length 1 m has a power of 1 D (Statement I true). A converging lens "
  "has a positive focal length and hence a positive power; a diverging lens has a negative power (Statement II "
  "false).",
  ["1 D = 1 m⁻¹ → I true", "Convex: f > 0 → P > 0 → II false"],
  why="Statement II reverses the sign convention: it is the diverging lens whose power is negative.",
  ncert=RO + "power of a lens", seconds=25)

q(OPT, "Optical instruments", "Basic", "match_list",
  ml("Match each lens or instrument in List-I with the position of the object it uses, as described in List-II.",
     ["Simple microscope forming its final image at the near point (object position relative to the lens)",
      "Objective of a compound microscope (object position)",
      "Objective of an astronomical telescope (object position)",
      "Eyepiece of an astronomical telescope in normal adjustment (position of the intermediate image)"],
     ["Just beyond the focus of the lens", "Between the focus and the lens", "Practically at infinity",
      "Exactly at the focus of the lens"]),
  *mlo("A-II, B-I, C-III, D-IV", ["A-I, B-II, C-III, D-IV", "A-II, B-IV, C-III, D-I", "A-II, B-I, C-IV, D-III"],
       "B"),
  "Image formation in the simple microscope, compound microscope and telescope",
  "A simple microscope needs a virtual, magnified image, so the object is inside the focal length. The objective of "
  "a compound microscope forms a real, magnified image, so the object is placed just beyond its focus. A telescope "
  "views distant objects. In normal adjustment the final image is at infinity, so the intermediate image lies at "
  "the focus of the eyepiece.",
  ["A: object within f → II", "B: object just beyond f_o → I", "C: object at infinity → III",
   "D: intermediate image at f_e → IV"],
  why="A-I, B-II, ... interchanges the simple microscope and the objective of the compound microscope. A-II, B-IV, "
      "... puts the microscope object exactly at the focus, where the image would be at infinity. A-II, B-I, C-IV, "
      "D-III interchanges the telescope's object and intermediate image.",
  ncert=RO + "optical instruments", seconds=50)

# ---- Intermediate
f_two = 10
u_real = -F(3, 2) * f_two          # m = f/(u + f) = -2
u_virt = -F(1, 2) * f_two          # m = +2
assert F(f_two) / (u_real + f_two) == -2 and F(f_two) / (u_virt + f_two) == 2
assert u_virt - u_real == 10
q(OPT, "Refraction and lenses", "Intermediate", "numerical",
  "A thin convex lens forms an image twice the size of an object (magnification of magnitude 2) for two different "
  "positions of the object on its axis, one giving a real image and the other a virtual image. These two object "
  "positions are 10 cm apart. The focal length of the lens is:",
  *opt("10 cm", ["20 cm", "5 cm", "15 cm"], "C"),
  "Thin lens magnification m = v/u = f/(u + f) (Cartesian signs)",
  "For a real image m = −2 and for a virtual image m = +2. Using m = f/(u + f) gives the two object distances in "
  "terms of f, and their difference is f.",
  ["m = −2: u + f = −f/2 → u = −1.5f", "m = +2: u + f = f/2 → u = −0.5f",
   "Difference = 1.5f − 0.5f = f = 10 cm"],
  why="20 cm and 5 cm take the separation of the two positions as half or twice the focal length. 15 cm is the "
      "object distance for the real image, not the focal length.",
  ncert=RO + "thin lens formula; magnification", seconds=80, rc=True)

uu = [x / 10 for x in range(151, 2000)]
min_sep = min(u + u * 15 / (u - 15) for u in uu)
close(min_sep, 60, 1e-3)
q(OPT, "Refraction and lenses", "Intermediate", "numerical",
  "A thin convex lens of focal length 15 cm forms a real image of a real object. The least possible distance "
  "between the object and its real image is:",
  *opt("60 cm", ["30 cm", "15 cm", "45 cm"], "D"),
  "For a real image by a convex lens, object–image distance D = u + v is least (= 4f) when u = v = 2f",
  "With the object at 2f the real image is at 2f on the other side, and moving the object either nearer to F or "
  "farther away only increases the total distance. So the least separation is 4f.",
  ["D = u + v with 1/u + 1/v = 1/f (magnitudes)", "D is least at u = v = 2f", "D_min = 4f = 60 cm"],
  why="30 cm is 2f, the distance of the object (or image) from the lens in that position. 15 cm is f itself. 45 cm "
      "has no basis: the separation never falls below 4f.",
  ncert=RO + "thin lens formula", seconds=50, rc=True)

thB = 60
n_B = math.tan(rad(thB))
C_B = deg(math.asin(1 / n_B))
close(n_B, math.sqrt(3))
close(C_B, 35.26, 1e-3)
close(deg(math.acos(1 / n_B)), 54.7, 1e-3)
q(OPT, "Polarisation", "Intermediate", "numerical",
  "When unpolarised light in air falls on the plane surface of a transparent medium at an angle of incidence of "
  "60°, the reflected light is completely plane polarised. The critical angle for light going from this medium "
  "into air is about:",
  *opt("35°, i.e. sin⁻¹(1/√3)", ["30°", "60°", "55°, i.e. cos⁻¹(1/√3)"], "A"),
  "Brewster's law tan i_B = n; critical angle sin C = 1/n",
  "The angle of incidence for completely polarised reflection is the Brewster angle, so the refractive index is "
  "tan 60° = √3. The critical angle then follows from sin C = 1/n.",
  ["n = tan 60° = √3", "sin C = 1/√3 ≈ 0.577", "C ≈ 35°"],
  why="30° takes the critical angle as 90° minus the Brewster angle. 60° takes it equal to the Brewster angle. 55° "
      "uses cos C = 1/n instead of sin C = 1/n.",
  ncert=WO + "polarisation (Brewster's law)", seconds=60, rc=True)

d_y = F(1, 1)                       # mm
a_y = 2 * d_y / 10                 # 2λD/a = 10 λD/d
assert a_y == F(1, 5)
assert d_y / 10 == F(1, 10) and 2 * d_y / 5 == F(2, 5)
q(OPT, "Diffraction", "Intermediate", "numerical",
  "In a Young's double-slit experiment the separation between the centres of the two slits is 1.0 mm. Each slit has "
  "a finite width a, and the single-slit diffraction pattern of each slit, observed on the same screen with the same "
  "light, has a central maximum (between its first minima on either side) that contains exactly 10 interference "
  "fringe widths. The width a of each slit is:",
  *opt("0.2 mm", ["0.1 mm", "0.4 mm", "5 mm"], "B"),
  "Linear width of the single-slit central maximum = 2λD/a; fringe width of the double slit = λD/d",
  "Setting the width of the central maximum equal to 10 fringe widths, λ and D cancel.",
  ["2λD/a = 10 λD/d", "a = 2d/10 = d/5", "a = 1.0/5 = 0.2 mm"],
  why="0.1 mm takes the width of the central maximum as λD/a (half its true value). 0.4 mm fits only 5 fringe widths "
      "into the central maximum. 5 mm inverts the ratio.",
  ncert=WO + "diffraction (the single slit); interference of light waves and Young's experiment", seconds=70,
  rc=True)

P_c = F(1, 20) - F(1, 30)
f_c = 1 / P_c
v_c = 1 / (P_c + F(1, -30))
assert f_c == 60 and v_c == -60
assert 1 / (F(1, 20) + F(1, 30) - F(1, 30)) == 20
q(OPT, "Refraction and lenses", "Intermediate", "numerical",
  "A thin convex lens of focal length 20 cm is placed in contact with a thin concave lens of focal length 30 cm. A "
  "small object is placed on the common axis, 30 cm in front of the combination. The image formed is:",
  *opt("60 cm from the lenses, on the same side as the object (virtual)",
       ["60 cm from the lenses, on the other side (real)", "20 cm from the lenses, on the other side (real)",
        "30 cm from the lenses, on the same side as the object (virtual)"], "C"),
  "Thin lenses in contact: 1/F = 1/f₁ + 1/f₂; thin lens formula 1/v − 1/u = 1/F",
  "The combination has 1/F = 1/20 − 1/30 = 1/60, a converging lens of focal length 60 cm. The object at 30 cm is "
  "inside this focal length, so the image is virtual.",
  ["1/F = 1/20 − 1/30 → F = +60 cm", "1/v = 1/F + 1/u = 1/60 − 1/30 = −1/60", "v = −60 cm: virtual, on the "
   "object's side"],
  why="60 cm on the other side is a sign error in the lens formula. 20 cm on the other side treats the concave lens "
      "as converging (F = 12 cm). 30 cm on the object's side has no basis in the lens formula.",
  ncert=RO + "combination of thin lenses in contact", seconds=70, rc=True)

f_cm = 20
vv = [1 / (1 / f_cm - 1 / -u) for u in (1000, 100, 40, 20, 5)]   # u negative, f positive for convex mirror
assert all(0 < a < f_cm for a in vv) and vv == sorted(vv, reverse=True)
mm_ = [vv[i] / u for i, u in enumerate((1000, 100, 40, 20, 5))]
assert all(0 < a < 1 for a in mm_) and mm_ == sorted(mm_)
q(OPT, "Mirrors", "Intermediate", "direct",
  "A real object is moved along the principal axis of a convex mirror from a very large distance up to the pole of "
  "the mirror. During this motion, the image:",
  *opt("moves from the focus towards the pole and grows in size, though it always stays smaller than the object",
       ["moves from the pole towards the focus and shrinks in size",
        "moves from the focus out to infinity, becoming larger than the object",
        "stays at the focus, only its size increasing"], "D"),
  "Image formation by a convex mirror (mirror equation with f > 0)",
  "For a distant object the image is a point-sized image at the focus behind the mirror. As the object approaches, "
  "1/v = 1/f − 1/u gives a virtual image between the focus and the pole that moves towards the pole, and the "
  "magnification v/u grows towards +1 but never reaches it for a real object at a finite distance.",
  ["u → −∞: v = f, m → 0", "As u → 0: v → 0 (towards the pole), m → 1", "Always 0 < m < 1"],
  why="The image moves towards the pole, not away from it, and grows rather than shrinks. A convex mirror never "
      "forms a magnified image of a real object or an image at infinity. The image does not stay at the focus.",
  ncert=RO + "reflection of light by spherical mirrors", seconds=45)

q(OPT, "Huygens' principle and interference", "Intermediate", "assertion_reason",
  ar("When Young's double-slit experiment is performed with white light, the central fringe is white, while the "
     "fringes on either side of it are coloured.",
     "Light waves are transverse waves."),
  AR, ar_key(True, True, False),
  "Fringe width depends on wavelength (β = λD/d)",
  "At the centre the path difference is zero for every wavelength, so all colours give a maximum there and the "
  "central fringe is white. Elsewhere the positions of maxima depend on λ, so different colours separate and the "
  "fringes are coloured (A true). Light is indeed a transverse wave (R true), but this is shown by polarisation and "
  "has nothing to do with the colours of the fringes.",
  ["Zero path difference for all λ → white centre", "β ∝ λ → colours separate → coloured fringes",
   "Transverse nature is unrelated → R not the explanation"],
  why="Both statements are true, but the colouring comes from the dependence of the fringe positions on wavelength, "
      "not from the transverse nature of light.",
  ncert=WO + "interference of light waves and Young's experiment", seconds=40)

truth_coh = {"a": True, "b": True, "c": True, "d": False, "e": False}
q(OPT, "Huygens' principle and interference", "Intermediate", "multi_statement",
  ms("Which of the following statements about interference and Young's double-slit experiment are correct?",
     ["Two sources are coherent if the phase difference between the waves they send out stays constant in time.",
      "In Young's experiment, the two slits illuminated by light from a single source slit act as coherent sources.",
      "The fringe width does not depend on the intensity of the light used.",
      "When the two slits are equidistant from the source slit, the central fringe is dark.",
      "Dark fringes are formed at points where the waves from the two slits arrive in phase."]),
  *mso(truth_coh, "abc", ["ab", "abcd", "bce"], "A"),
  "Coherence and the conditions for constructive and destructive interference",
  "Coherent sources keep a constant phase difference (a true). Young obtained such sources by letting the light from "
  "one slit fall on two slits, so that any phase change in the source affects both equally (b true). β = λD/d does "
  "not involve the intensity (c true). With the slits equidistant from the source slit, the waves reach the centre "
  "of the screen with zero path difference, giving a bright central fringe (d false). Dark fringes are where the "
  "waves arrive in opposite phase (e false).",
  ["(a), (b), (c) true", "(d) false: zero path difference at the centre → bright", "(e) false: dark ↔ opposite "
   "phase"],
  why="Options containing (d) or (e) include a false statement; (a) and (b) only leaves out the true statement (c).",
  ncert=WO + "coherent and incoherent addition of waves; interference of light waves and Young's experiment",
  seconds=60)

q(OPT, "Refraction and lenses", "Intermediate", "statement_pair",
  sp("The power of a combination of thin lenses placed in contact is the algebraic sum of the powers of the "
     "individual lenses.",
     "When several lenses are used in combination, the total magnification produced is the product of the "
     "magnifications produced by the individual lenses."),
  SP, sp_key(True, True),
  "Combination of thin lenses in contact",
  "For thin lenses in contact, 1/F = 1/f₁ + 1/f₂ + ..., so P = P₁ + P₂ + ... (Statement I true). The image formed "
  "by the first lens acts as the object for the second, so the sizes multiply: m = m₁m₂m₃... (Statement II true).",
  ["P = P₁ + P₂ + ... → I true", "m = m₁ × m₂ × ... → II true"],
  why="Both statements are correct, so options calling either of them false are wrong.",
  ncert=RO + "combination of thin lenses in contact", seconds=30)

# ---- Advanced
def emerges_adjacent(n):
    """True if some ray entering one face of a cube can leave through an adjacent face."""
    for k in range(1, 900):
        i = rad(k / 10)
        r = math.asin(math.sin(i) / n)
        if math.sin(rad(90) - r) < 1 / n:
            return True
    return False
assert emerges_adjacent(1.40) and not emerges_adjacent(1.42) and not emerges_adjacent(1.5)
q(OPT, "Total internal reflection", "Advanced", "numerical",
  "Light enters a transparent cube, placed in air, through one of its faces. The least refractive index of the "
  "material of the cube for which no ray that enters through that face, whatever its angle of incidence, can come "
  "out through an adjacent face (a face perpendicular to the first) is:",
  *opt("√2", ["√3", "1.5", "2"], "B"),
  "Refraction at the first face followed by total internal reflection at a perpendicular face",
  "A ray refracted at angle r into the cube meets the adjacent face at an angle of incidence 90° − r. The worst case "
  "is grazing incidence on the first face, when r is largest (sin r = 1/n). Total internal reflection at the "
  "adjacent face for this ray needs sin(90° − r) = cos r ≥ 1/n.",
  ["Largest r: sin r = 1/n", "Need cos r ≥ 1/n → 1 − 1/n² ≥ 1/n²", "n² ≥ 2 → n ≥ √2"],
  why="√3, 1.5 and 2 all satisfy the condition, but the question asks for the least value, which is √2.",
  ncert=RO + "total internal reflection", seconds=110, rc=True)

n_w, h_fish, h_bird = F(4, 3), 12, 18
app = h_fish + n_w * h_bird
assert app == 36 and h_fish + F(h_bird) / n_w == F(51, 2) and n_w * h_fish + n_w * h_bird == 40
q(OPT, "Refraction and lenses", "Advanced", "numerical",
  "A fish is 12 cm below the surface of still water (refractive index 4/3), and a bird is 18 cm above the surface, "
  "vertically above the fish. Using the near-normal (paraxial) approximation for refraction at a plane surface, the "
  "distance of the bird from the fish, as it appears to the fish looking straight up, is:",
  *opt("36 cm", ["30 cm", "25.5 cm", "40 cm"], "C"),
  "Refraction at a plane surface: for near-normal viewing, apparent distance = (n of observer's medium/n of "
  "object's medium) × real distance from the surface",
  "The fish sees the bird through the water surface. Light from the bird travels from air into water, so for an "
  "observer in water the bird appears farther from the surface by the factor 4/3. The fish's own distance from the "
  "surface is real and unchanged.",
  ["Apparent height of the bird above the surface = (4/3) × 18 = 24 cm", "Apparent distance = 12 + 24 = 36 cm"],
  why="30 cm is the real distance. 25.5 cm divides the bird's height by n, which is what the bird would see for the "
      "fish's depth, not what the fish sees. 40 cm also scales the fish's own distance from the surface.",
  ncert=RO + "refraction (real and apparent depth)", seconds=80, rc=True)

I1, I2 = 1, 4
I_p = I1 + I2 + 2 * math.sqrt(I1 * I2) * math.cos(rad(60))
I_mx = (math.sqrt(I1) + math.sqrt(I2)) ** 2
close(I_p / I_mx, 7 / 9)
close(math.cos(rad(30)) ** 2, 3 / 4)
close((I1 + I2) / I_mx, 5 / 9)
q(OPT, "Huygens' principle and interference", "Advanced", "numerical",
  "In an interference experiment, two coherent waves reach a point on the screen with intensities I and 4I. At a "
  "point where the phase difference between them is π/3, the intensity, expressed as a fraction of the maximum "
  "intensity I_max in the pattern, is:",
  *opt("7I_max/9", ["3I_max/4", "5I_max/9", "I_max/9"], "A"),
  "Resultant intensity of two coherent waves: I = I₁ + I₂ + 2√(I₁I₂) cos φ",
  "The maximum occurs where cos φ = 1: I_max = (√I + √(4I))² = 9I. At φ = π/3, the interference term is "
  "2 × 2I × ½ = 2I.",
  ["I_max = (1 + 2)² I = 9I", "I(π/3) = I + 4I + 2 × 2I × cos 60° = 7I", "I/I_max = 7/9"],
  why="3I_max/4 uses cos²(φ/2), which holds only for two waves of equal intensity. 5I_max/9 drops the interference "
      "term, as if the waves were incoherent. I_max/9 is the minimum intensity (φ = π).",
  ncert=WO + "coherent and incoherent addition of waves", seconds=80, rc=True)

d_s, dbeta, dD = 1.0e-3, 0.30e-3, 0.50
lam_s = d_s * dbeta / dD
close(lam_s, 600e-9)
close(d_s * dbeta / 1.0, 300e-9)
close(2 * lam_s, 1200e-9)
q(OPT, "Huygens' principle and interference", "Advanced", "numerical",
  "In a Young's double-slit experiment the slits are 1.0 mm apart. When the screen is moved 50 cm closer to the "
  "slits, the fringe width decreases by 0.30 mm. The wavelength of the light used is:",
  *opt("600 nm", ["300 nm", "1200 nm", "60 nm"], "B"),
  "Fringe width β = λD/d is proportional to D, so Δβ = λΔD/d",
  "Only D changes. The change in fringe width is therefore λ/d times the change in D, so the original value of D is "
  "not needed.",
  ["Δβ = λ ΔD/d", "λ = d Δβ/ΔD = (1.0 × 10⁻³ × 0.30 × 10⁻³)/0.50", "λ = 6.0 × 10⁻⁷ m = 600 nm"],
  why="300 nm divides by 1.0 m instead of 0.50 m. 1200 nm multiplies by the factor 2 instead of dividing. 60 nm is a "
      "power-of-ten slip in converting millimetres.",
  ncert=WO + "interference of light waves and Young's experiment", seconds=70, rc=True)

q(OPT, "Total internal reflection", "Advanced", "assertion_reason",
  ar("A ray of light entering one face of a glass slab with parallel faces, placed in air, can be totally internally "
     "reflected at the opposite face if its angle of incidence at the first face is made large enough.",
     "Total internal reflection can occur only when light travels from an optically denser medium towards an "
     "optically rarer medium."),
  AR, ar_key(False, True),
  "Refraction through a parallel slab; condition for total internal reflection",
  "At the first face sin i = n sin r. The faces are parallel, so the ray meets the second face at the same angle r, "
  "with n sin r = sin i ≤ 1. Hence the angle at the second face never exceeds the critical angle (sin r ≤ 1/n), and "
  "the ray always emerges, parallel to its original direction (A false). R correctly states one of the conditions "
  "for total internal reflection.",
  ["Angle at the second face = r", "n sin r = sin i ≤ 1 → r ≤ C", "No total internal reflection → A false; R true"],
  why="A is false, so the options calling it true are wrong. Glass to air is denser to rarer, as R requires, but the "
      "geometry of a parallel slab never lets the angle at the second face exceed the critical angle.",
  ncert=RO + "total internal reflection", seconds=60)

assert 1 / (F(1, -20) - F(1, -30)) == -60           # concave mirror f = −20: v = −60 (in front, real)
assert 1 / (F(1, 20) - F(1, -30)) == 12             # convex mirror f = +20: v = +12 (behind, virtual)
assert 1 / (F(1, 20) + F(1, -30)) == 60             # convex lens f = +20: v = +60 (other side, real)
assert 1 / (F(1, -20) + F(1, -30)) == -12           # concave lens f = −20: v = −12 (object side, virtual)
q(OPT, "Mirrors", "Advanced", "match_list",
  ml("A small real object is placed 30 cm from each of the optical elements in List-I, on its principal axis. Each "
     "element has a focal length of magnitude 20 cm. Match each element with the image it forms (List-II).",
     ["Concave mirror", "Convex mirror", "Convex lens", "Concave lens"],
     ["Real, 60 cm from the element, on the same side as the object",
      "Virtual, 12 cm from the element, on the side opposite to the object",
      "Real, 60 cm from the element, on the side opposite to the object",
      "Virtual, 12 cm from the element, on the same side as the object"]),
  *mlo("A-I, B-II, C-III, D-IV", ["A-III, B-IV, C-I, D-II", "A-I, B-IV, C-III, D-II", "A-III, B-II, C-I, D-IV"],
       "C"),
  "Mirror formula 1/v + 1/u = 1/f and lens formula 1/v − 1/u = 1/f with Cartesian signs",
  "A mirror sends light back, so a real image forms on the object's side and a virtual image behind it. A lens lets "
  "light through, so a real image forms on the far side and a virtual image on the object's side.",
  ["Concave mirror (f = −20, u = −30): v = −60 cm → real, object side",
   "Convex mirror (f = +20): v = +12 cm → virtual, behind the mirror",
   "Convex lens (f = +20): v = +60 cm → real, far side", "Concave lens (f = −20): v = −12 cm → virtual, object side"],
  why="The other codes give the right distances but put the real or virtual images on the wrong side, mixing up "
      "how mirrors and lenses send light.",
  ncert=RO + "reflection by spherical mirrors; refraction by a lens", seconds=90, rc=True)

truth_huy = {"a": True, "b": True, "c": True, "d": False, "e": False}
q(OPT, "Huygens' principle and interference", "Advanced", "multi_statement",
  ms("Which of the following conclusions are obtained correctly from Huygens' principle applied to plane waves?",
     ["For refraction, sin i/sin r = v₁/v₂, where v₁ and v₂ are the speeds of light in the two media.",
      "For reflection at a plane surface, the angle of reflection equals the angle of incidence.",
      "On refraction the frequency is unchanged, and the wavelength in each medium is proportional to the speed of "
      "light in it.",
      "When light passes from a rarer to a denser medium, the refracted wavefront travels faster than the incident "
      "wavefront.",
      "Secondary wavelets in any medium spread out with the speed of light in vacuum."]),
  *mso(truth_huy, "abc", ["ab", "abcd", "ace"], "D"),
  "Huygens' construction for reflection and refraction of a plane wavefront",
  "During the time τ that the incident wavefront takes to sweep across the surface, the secondary wavelets in medium "
  "2 grow to radius v₂τ, which gives sin i/sin r = v₁/v₂ (a true) and, for reflection, equal angles (b true). The "
  "frequency is fixed by the source, so λ = v/ν ∝ v (c true). Bending towards the normal (rarer to denser) means "
  "v₂ < v₁: the wave is slower in the denser medium (d false). The wavelets in a medium spread with the speed of "
  "light in that medium (e false).",
  ["(a), (b), (c) true", "(d) false: slower in the denser medium", "(e) false: wavelets move at v of the medium"],
  why="Options containing (d) or (e) include a false statement; (a) and (b) only leaves out the true statement (c).",
  ncert=WO + "refraction and reflection of plane waves using Huygens principle", seconds=70)


# ================================================================ Dual Nature of Matter and Radiation (B2 I3 A2)
DC = NC + "'Dual Nature of Radiation and Matter', "

# ---- Basic
lamA = 600
lamB = lamA / 2          # φ = hc/λ₀, φ_B = 2φ_A
assert lamB == 300 and lamA * 2 == 1200
close(lamA / math.sqrt(2), 424, 1e-3)
q(DUAL, "Einstein's equation", "Basic", "numerical",
  "The threshold wavelength for photoelectric emission from metal A is 600 nm. Metal B has a work function twice "
  "that of metal A. The threshold wavelength for metal B is:",
  *opt("300 nm", ["1200 nm", "600 nm", "424 nm"], "D"),
  "Work function φ₀ = hν₀ = hc/λ₀",
  "The threshold wavelength is inversely proportional to the work function, so doubling the work function halves "
  "the threshold wavelength.",
  ["λ₀ = hc/φ₀ ∝ 1/φ₀", "λ₀(B) = 600/2 = 300 nm"],
  why="1200 nm makes λ₀ proportional to φ₀. 600 nm assumes the threshold wavelength is the same for all metals. "
      "424 nm divides by √2 instead of 2.",
  ncert=DC + "photoelectric effect; Einstein's photoelectric equation", seconds=30, rc=True)

T1_, T2_ = 300, 1200
ratio_lam = math.sqrt(T1_ / T2_)
close(ratio_lam, 0.5)
close(math.sqrt(27 / 927), 1 / 5.86, 2e-3)
q(DUAL, "de Broglie wavelength", "Basic", "numerical",
  "The de Broglie wavelength of helium atoms in a gas, calculated with their rms speed (so that λ = h/√(3mkT)), is "
  "λ at 27 °C. At 927 °C it becomes:",
  *opt("λ/2", ["λ/5.9", "λ/4", "2λ"], "C"),
  "de Broglie wavelength λ = h/p with p = √(3mkT) for thermal motion, so λ ∝ 1/√T (T in kelvin)",
  "The temperatures must be converted to kelvin: 27 °C = 300 K and 927 °C = 1200 K. The absolute temperature "
  "becomes four times, so the wavelength is halved.",
  ["T: 300 K → 1200 K (× 4)", "λ ∝ 1/√T → λ' = λ/√4 = λ/2"],
  why="λ/5.9 uses the Celsius temperatures. λ/4 takes λ as inversely proportional to T instead of √T. 2λ makes the "
      "wavelength grow with temperature, though the atoms move faster.",
  ncert=DC + "wave nature of matter", seconds=40, rc=True)

# ---- Intermediate
slope_v, nu0 = 4.0e-15, 4.0e14
V0_g = slope_v * (9.0e14 - nu0)
phi_g = slope_v * nu0              # in eV, since slope = h/e
close(V0_g, 2.0)
close(phi_g, 1.6)
close(slope_v * 9.0e14, 3.6)
q(DUAL, "Einstein's equation", "Intermediate", "numerical",
  "For a certain metal, the graph of the stopping potential V₀ (y-axis) against the frequency ν of the incident "
  "light (x-axis) is a straight line that cuts the frequency axis at 4.0 × 10¹⁴ Hz and has a slope of "
  "4.0 × 10⁻¹⁵ V s. The stopping potential for light of frequency 9.0 × 10¹⁴ Hz, and the work function of the "
  "metal, are respectively:",
  *opt("2.0 V and 1.6 eV", ["3.6 V and 1.6 eV", "2.0 V and 3.6 eV", "1.6 V and 2.0 eV"], "A"),
  "Einstein's equation in the form V₀ = (h/e)ν − φ₀/e: slope h/e, frequency intercept ν₀ = φ₀/h",
  "The line passes through (ν₀, 0) with slope h/e, so V₀ = (h/e)(ν − ν₀). The work function in electron volts is "
  "(h/e)ν₀, i.e. the slope times the threshold frequency.",
  ["V₀ = 4.0 × 10⁻¹⁵ × (9.0 − 4.0) × 10¹⁴ = 2.0 V", "φ₀/e = (h/e)ν₀ = 4.0 × 10⁻¹⁵ × 4.0 × 10¹⁴ = 1.6 V → "
   "φ₀ = 1.6 eV"],
  why="3.6 V multiplies the slope by ν instead of (ν − ν₀), as if the line passed through the origin. 3.6 eV is the "
      "photon energy at 9.0 × 10¹⁴ Hz, not the work function. 1.6 V and 2.0 eV interchange the two results.",
  ncert=DC + "Einstein's photoelectric equation: energy quantum of radiation", seconds=60, rc=True)

phi_m = 2.1
E300, E400 = 1240 / 300, 1240 / 400
V0_mix = E300 - phi_m
close(V0_mix, 2.03, 3e-3)
close(E400 - phi_m, 1.0)
q(DUAL, "Einstein's equation", "Intermediate", "numerical",
  "Light containing only two wavelengths, 400 nm and 300 nm, falls on a metal surface whose work function is "
  "2.1 eV. Taking hc = 1240 eV nm, the stopping potential for the photoelectrons is about:",
  *opt("2.0 V", ["1.0 V", "1.5 V", "3.0 V"], "B"),
  "Einstein's photoelectric equation K_max = hν − φ₀; the stopping potential stops the fastest electrons",
  "To stop the photocurrent completely, the collector must turn back even the fastest photoelectrons, which are "
  "those ejected by the shorter wavelength (higher photon energy).",
  ["Photon energies: 1240/300 = 4.13 eV and 1240/400 = 3.10 eV", "Fastest electrons: K_max = 4.13 − 2.1 = 2.03 eV",
   "Stopping potential ≈ 2.0 V"],
  why="1.0 V is enough to stop only the electrons ejected by the 400 nm light. 1.5 V averages the two stopping "
      "potentials. 3.0 V adds the 1.0 V and 2.0 V values, but each electron absorbs a single photon.",
  ncert=DC + "Einstein's photoelectric equation: energy quantum of radiation", seconds=60, rc=True)

q(DUAL, "Photoelectric effect", "Intermediate", "statement_pair",
  sp("When monochromatic light ejects photoelectrons from a metal, the emitted electrons have kinetic energies "
     "ranging from zero up to a maximum value.",
     "The maximum kinetic energy of the photoelectrons equals the whole energy hν of the incident photon."),
  SP, sp_key(True, False),
  "Einstein's photoelectric equation K_max = hν − φ₀",
  "Each photon gives its energy hν to one electron. An electron must spend at least the work function φ₀ (more if "
  "it comes from deeper inside or loses energy on the way) to escape, so the emitted electrons have kinetic "
  "energies from zero up to K_max (Statement I true). Even the fastest electrons have spent φ₀, so "
  "K_max = hν − φ₀, less than hν (Statement II false).",
  ["Energy needed to escape ≥ φ₀ → K from 0 to K_max → I true", "K_max = hν − φ₀ < hν → II false"],
  why="Statement II leaves out the work function, which every photoelectron must spend to leave the metal.",
  ncert=DC + "Einstein's photoelectric equation: energy quantum of radiation", seconds=35)

# ---- Advanced
E_ph = (2 * F(7, 2) - 2)          # E − 2.0 = 2(E − 3.5) → E = 5.0
assert E_ph == 5 and E_ph - 2 == 2 * (E_ph - F(7, 2))
q(DUAL, "Einstein's equation", "Advanced", "numerical",
  "Photons of the same energy fall on two metals: metal A of work function 2.0 eV and metal B of work function "
  "3.5 eV. The maximum kinetic energy of the photoelectrons from A is twice that of the photoelectrons from B. The "
  "energy of each photon is:",
  *opt("5.0 eV", ["1.5 eV", "5.5 eV", "7.0 eV"], "A"),
  "Einstein's photoelectric equation K_max = E − φ₀ for each metal",
  "Write K_max for each metal with the same photon energy E and use the given ratio.",
  ["K_A = E − 2.0, K_B = E − 3.5", "E − 2.0 = 2(E − 3.5) → E = 7.0 − 2.0 = 5.0 eV",
   "Check: K_A = 3.0 eV, K_B = 1.5 eV"],
  why="1.5 eV is the difference of the work functions (it is K_B, not E). 5.5 eV adds the two work functions. "
      "7.0 eV is twice the work function of B.",
  ncert=DC + "Einstein's photoelectric equation: energy quantum of radiation", seconds=70, rc=True)

m_e_, m_al = F(1), F(7294)               # alpha mass ≈ 7294 electron masses; any m_al > m_e works
p_same = F(1)
K_e, K_al = p_same ** 2 / (2 * m_e_), p_same ** 2 / (2 * m_al)
V_e, V_al = K_e / 1, K_al / 2             # charges e and 2e
truth_db = {"a": True, "b": K_e > K_al, "c": p_same / m_e_ > p_same / m_al, "d": K_e == K_al, "e": V_e < V_al}
q(DUAL, "de Broglie wavelength", "Advanced", "multi_statement",
  ms("An electron and an alpha particle, both moving much slower than light, have the same de Broglie wavelength. "
     "Which of the following statements are correct?",
     ["They have momenta of equal magnitude.",
      "The electron has the larger kinetic energy.",
      "The electron has the larger speed.",
      "They have equal kinetic energies.",
      "If each was accelerated from rest through a potential difference, the electron was accelerated through the "
      "smaller potential difference."]),
  *mso(truth_db, "abc", ["ac", "abcd", "abe"], "D"),
  "λ = h/p; K = p²/2m; for acceleration from rest qV = K",
  "Equal wavelengths mean equal momenta (a true). With the same p, the lighter electron has the larger speed p/m (c "
  "true) and the larger kinetic energy p²/2m (b true, d false). The electron's kinetic energy is thousands of times "
  "that of the alpha particle while its charge is only half as large, so it needed a much larger accelerating "
  "potential difference, V = K/q (e false).",
  ["p = h/λ: equal", "v = p/m, K = p²/2m: larger for the electron", "V = K/q: V_e = p²/2m_e e ≫ V_α = p²/(2m_α × 2e)"],
  why="Options containing (d) or (e) include a false statement; (a) and (c) only leaves out the true statement (b).",
  ncert=DC + "wave nature of matter", seconds=70, rc=True)


# ================================================================ Atoms and Nuclei (B3 I5 A4)
AC_ = NC + "'Atoms', "
NU = NC + "'Nuclei', "

# ---- Basic
dm = 900e6 / (3e8) ** 2
close(dm, 1.0e-8)
close(900e6 / 3e8, 3.0)
q(AN, "Nuclear size and mass defect", "Basic", "numerical",
  "A nuclear power station produces energy at the rate of 900 MW. Taking c = 3 × 10⁸ m/s, the mass converted into "
  "energy every second is:",
  *opt("1.0 × 10⁻⁸ kg", ["3.0 kg", "1.0 × 10⁻¹¹ kg", "1.0 × 10⁻⁵ kg"], "B"),
  "Mass–energy equivalence E = mc²",
  "In one second 9 × 10⁸ J of energy is produced; the corresponding mass is E/c².",
  ["E (per second) = 9.0 × 10⁸ J", "m = E/c² = 9.0 × 10⁸/(9 × 10¹⁶) = 1.0 × 10⁻⁸ kg"],
  why="3.0 kg divides by c instead of c². 1.0 × 10⁻¹¹ kg and 1.0 × 10⁻⁵ kg come from taking 1 MW as 10³ W or "
      "10⁹ W.",
  ncert=NU + "mass-energy and nuclear binding energy", seconds=30, rc=True)

R_ryd = 1.1e7
lam_P = 1 / (R_ryd * (1 / 9 - 1 / 16))
close(lam_P, 1.87e-6, 1e-3)
close(1 / (R_ryd * (1 / 4 - 1 / 9)), 6.55e-7, 2e-3)
close(9 / R_ryd, 8.2e-7, 3e-3)
q(AN, "Bohr model and hydrogen spectrum", "Basic", "numerical",
  "The wavelengths of the hydrogen spectrum are given by 1/λ = R(1/n_f² − 1/n_i²). Taking R = 1.1 × 10⁷ m⁻¹, the "
  "wavelength of the first line of the Paschen series (n_i = 4 → n_f = 3) and the region of the spectrum in which it "
  "lies are:",
  *opt("about 1.87 µm, in the infrared", ["about 656 nm, in the visible region", "about 0.82 µm, in the infrared",
                                          "about 1.87 µm, in the ultraviolet"], "D"),
  "Rydberg formula for the hydrogen spectrum; Paschen series ends on n = 3",
  "Substitute n_f = 3 and n_i = 4 for the first (longest-wavelength) line of the Paschen series.",
  ["1/λ = R(1/9 − 1/16) = 7R/144", "λ = 144/(7 × 1.1 × 10⁷) ≈ 1.87 × 10⁻⁶ m", "Longer than 700 nm → infrared"],
  why="656 nm is the first Balmer line (3 → 2). 0.82 µm is the series limit of the Paschen series (∞ → 3), not its "
      "first line. 1.87 µm is longer than visible wavelengths, so it lies in the infrared, not the ultraviolet.",
  ncert=AC_ + "line spectra of the hydrogen atom", seconds=50, rc=True)

lv = [-13.6 / n ** 2 for n in range(1, 8)]
gaps = [lv[i + 1] - lv[i] for i in range(6)]
assert all(gaps[i] > gaps[i + 1] for i in range(5))
q(AN, "Bohr model and hydrogen spectrum", "Basic", "direct",
  "In the energy level diagram of the hydrogen atom (E_n = −13.6/n² eV), as the principal quantum number n "
  "increases, the energy difference between successive levels:",
  *opt("decreases, the levels crowding closer together as E approaches zero",
       ["increases steadily", "stays the same, 10.2 eV for every pair of successive levels",
        "first increases and then decreases"], "B"),
  "Energy levels of hydrogen: E_n ∝ −1/n²",
  "The gaps between successive levels are 10.2 eV (1 → 2), 1.89 eV (2 → 3), 0.66 eV (3 → 4) and so on, getting "
  "smaller and smaller. The levels crowd together just below E = 0, the ionisation limit.",
  ["E₂ − E₁ = 10.2 eV, E₃ − E₂ = 1.89 eV, E₄ − E₃ = 0.66 eV", "Gaps shrink → levels crowd towards E = 0"],
  why="The gaps shrink rather than grow or stay constant; 10.2 eV is only the gap between n = 1 and n = 2.",
  ncert=AC_ + "the Bohr model of the hydrogen atom (energy levels)", seconds=30)

# ---- Intermediate
ratio_short = F(1, 1) / F(9, 1)        # λ_short ∝ n_f²
assert ratio_short == F(1, 9)
q(AN, "Bohr model and hydrogen spectrum", "Intermediate", "numerical",
  "Using 1/λ = R(1/n_f² − 1/n_i²) for hydrogen, the ratio of the shortest wavelength of the Lyman series to the "
  "shortest wavelength of the Paschen series is:",
  *opt("1 : 9", ["9 : 1", "1 : 3", "1 : 4"], "D"),
  "Shortest wavelength of a series: transition from n_i = ∞, so 1/λ = R/n_f²",
  "The series limit of each series corresponds to n_i → ∞, so λ_short = n_f²/R: 1/R for Lyman (n_f = 1) and 9/R "
  "for Paschen (n_f = 3).",
  ["Lyman: λ = 1/R", "Paschen: λ = 9/R", "Ratio = 1 : 9"],
  why="9 : 1 inverts the ratio. 1 : 3 takes λ as proportional to n_f instead of n_f². 1 : 4 uses the Balmer series "
      "(n_f = 2) instead of Paschen.",
  ncert=AC_ + "line spectra of the hydrogen atom", seconds=45, rc=True)

Q_f = 234 * F(84, 10) - 235 * F(76, 10)
close(float(Q_f), 179.6, 1e-3)
close(236 * 8.4 - 235 * 7.6, 196.4, 1e-3)
close(235 * 0.8, 188)
assert 54 + 38 == 92 and 140 + 94 + 2 == 236
q(AN, "Fission and fusion", "Intermediate", "numerical",
  "In one mode of fission, ²³⁵U absorbs a slow neutron and splits as ²³⁵₉₂U + ¹₀n → ¹⁴⁰₅₄Xe + ⁹⁴₃₈Sr + 2 ¹₀n. Take "
  "the binding energy per nucleon as 7.6 MeV for ²³⁵U and 8.4 MeV for each of the two fission fragments (a free "
  "neutron has no binding energy). The energy released in this fission is about:",
  *opt("180 MeV", ["196 MeV", "188 MeV", "1966 MeV"], "C"),
  "Energy released = (total binding energy of products) − (total binding energy of reactants)",
  "Only the nucleons bound in nuclei contribute binding energy. The fragments contain 140 + 94 = 234 nucleons; the "
  "two neutrons released are free, as is the neutron absorbed.",
  ["Reactants: 235 × 7.6 = 1786 MeV", "Products: 234 × 8.4 = 1965.6 MeV", "Q = 1965.6 − 1786 ≈ 180 MeV"],
  why="196 MeV counts all 236 nucleons, including the free neutrons, as bound at 8.4 MeV. 188 MeV multiplies the "
      "difference in binding energy per nucleon (0.8 MeV) by 235, ignoring that the numbers of bound nucleons "
      "differ. 1966 MeV is the total binding energy of the fragments, not the energy released.",
  ncert=NU + "nuclear energy (fission)", seconds=80, rc=True)

r1_b, v1_b = 0.53e-10, 2.2e6
T1_b = 2 * math.pi * r1_b / v1_b
close(T1_b, 1.51e-16, 3e-3)
close(r1_b / v1_b, 2.4e-17, 4e-3)
close(math.pi * r1_b / v1_b, 7.6e-17, 6e-3)
close(4 * math.pi * r1_b / v1_b, 3.03e-16, 3e-3)
q(AN, "Bohr model and hydrogen spectrum", "Intermediate", "numerical",
  "In the ground state of the hydrogen atom in the Bohr model, the electron moves in a circle of radius "
  "0.53 × 10⁻¹⁰ m with a speed of 2.2 × 10⁶ m/s. The time it takes to complete one revolution is about:",
  *opt("1.5 × 10⁻¹⁶ s", ["2.4 × 10⁻¹⁷ s", "7.6 × 10⁻¹⁷ s", "3.0 × 10⁻¹⁶ s"], "A"),
  "Uniform circular motion: T = 2πr/v",
  "The period is the circumference of the orbit divided by the speed of the electron.",
  ["T = 2π × 0.53 × 10⁻¹⁰/(2.2 × 10⁶)", "T ≈ 1.5 × 10⁻¹⁶ s"],
  why="2.4 × 10⁻¹⁷ s is r/v, without the factor 2π. 7.6 × 10⁻¹⁷ s is the time for half a revolution (πr/v). "
      "3.0 × 10⁻¹⁶ s uses 2π times the diameter.",
  ncert=AC_ + "the Bohr model of the hydrogen atom", seconds=40, rc=True)

q(AN, "Fission and fusion", "Intermediate", "assertion_reason",
  ar("In a fusion reaction that releases energy, the total mass of the products is greater than the total mass of "
     "the reacting nuclei.",
     "Fusion of very light nuclei releases energy because the binding energy per nucleon of the product nucleus is "
     "greater than that of the reacting nuclei."),
  AR, ar_key(False, True),
  "Energy released in a nuclear reaction = (mass of reactants − mass of products) c²",
  "When two light nuclei fuse into a more tightly bound nucleus, the binding energy increases; the extra binding "
  "energy is released, and by E = mc² the products have less mass than the reactants (A false). R correctly gives "
  "the reason why fusion of light nuclei releases energy.",
  ["Energy released → Δm = (m_reactants − m_products) > 0", "Products lighter → A false",
   "Larger binding energy per nucleon of the product → R true"],
  why="A reverses the mass change: a reaction that releases energy always has products of smaller total mass.",
  ncert=NU + "nuclear energy (fusion); mass-energy and nuclear binding energy", seconds=40)

q(AN, "Bohr model and hydrogen spectrum", "Intermediate", "statement_pair",
  sp("The total energy of the electron in any Bohr orbit of the hydrogen atom is negative, which means that the "
     "electron is bound to the nucleus.",
     "As the principal quantum number n of the orbit increases, the total energy of the electron becomes more "
     "negative."),
  SP, sp_key(True, False),
  "Energy of the electron in the Bohr model: E_n = −13.6/n² eV",
  "A negative total energy means that energy must be supplied to free the electron: it is bound (Statement I true). "
  "As n increases, E_n = −13.6/n² eV rises towards zero (−13.6, −3.4, −1.51 eV, ...), i.e. becomes less negative "
  "(Statement II false).",
  ["E < 0 → bound state → I true", "E_n = −13.6/n²: larger n → closer to 0 → II false"],
  why="Statement II reverses the trend: the outer orbits have higher (less negative) energies, which is why energy "
      "must be absorbed to raise the electron to them.",
  ncert=AC_ + "the Bohr model of the hydrogen atom", seconds=30)

# ---- Advanced
per_fus = 17.6 / 5
per_fis = 200 / 236
close(per_fus / per_fis, 4.15, 3e-3)
close(17.6 / 200, 0.088, 1e-3)
close(200 / 17.6, 11.36, 1e-3)
q(AN, "Fission and fusion", "Advanced", "numerical",
  "The fusion reaction ²₁H + ³₁H → ⁴₂He + ¹₀n releases 17.6 MeV, and the fission of a ²³⁵U nucleus after it absorbs "
  "a neutron releases about 200 MeV. Comparing the energy released per nucleon of the reacting particles "
  "(including the neutron absorbed in fission), the ratio of the value for this fusion reaction to that for "
  "fission is about:",
  *opt("4", ["0.09", "11", "1"], "B"),
  "Energy per nucleon of reactants = energy released/number of nucleons taking part",
  "The fusion reaction involves only 2 + 3 = 5 nucleons, while the fission involves 235 + 1 = 236 nucleons. Per "
  "nucleon, fusion releases several times more energy, although each fission event releases far more energy in "
  "total.",
  ["Fusion: 17.6/5 ≈ 3.5 MeV per nucleon", "Fission: 200/236 ≈ 0.85 MeV per nucleon", "Ratio ≈ 3.5/0.85 ≈ 4"],
  why="0.09 and 11 compare the energies per reaction (17.6/200 and 200/17.6), not per nucleon. 1 assumes both "
      "processes release the same energy per nucleon.",
  ncert=NU + "nuclear energy (fission and fusion)", seconds=70, rc=True)

Bn = lambda n: F(1, n) / F(n ** 2) ** 2         # B ∝ I/r, I ∝ v/r ∝ (1/n)/n²  → B ∝ v/r² = (1/n)/n⁴
assert Bn(1) / Bn(2) == 32
assert F(8) == (F(1) / 1) / (F(1, 2) / 4) and F(16) == F(2) ** 4
q(AN, "Bohr model and hydrogen spectrum", "Advanced", "numerical",
  "In the Bohr model of the hydrogen atom, the radius of the nth orbit is proportional to n² and the speed of the "
  "electron in it is proportional to 1/n. The revolving electron is equivalent to a circular current loop. The ratio "
  "of the magnetic field produced at the nucleus by the electron in the n = 1 orbit to that produced by the electron "
  "in the n = 2 orbit is:",
  *opt("32 : 1", ["8 : 1", "16 : 1", "1 : 32"], "D"),
  "Equivalent current I = e/T = ev/(2πr); field at the centre of a loop B = µ₀I/(2r)",
  "Combine the two relations: B = µ₀ev/(4πr²). With v ∝ 1/n and r ∝ n², B ∝ (1/n)/n⁴ = 1/n⁵.",
  ["I = ev/2πr ∝ (1/n)/n² = 1/n³", "B = µ₀I/2r ∝ (1/n³)/n² = 1/n⁵", "B₁/B₂ = 2⁵ = 32"],
  why="8 : 1 is the ratio of the equivalent currents only, forgetting that the radius also changes in B = µ₀I/2r. "
      "16 : 1 takes B ∝ 1/n⁴. 1 : 32 inverts the ratio.",
  ncert=AC_ + "the Bohr model of the hydrogen atom", seconds=90, rc=True)

A_ = 8
assert (F(A_) ** 1, round(A_ ** (1 / 3)), round(A_ ** (2 / 3))) == (8, 2, 4)
q(AN, "Nuclear size and mass defect", "Advanced", "match_list",
  ml("The radius of a nucleus of mass number A is R = R₀A^(1/3). Match each property of the nucleus in List-I with "
     "the way it depends on A in List-II.",
     ["Radius of the nucleus", "Volume of the nucleus", "Density of nuclear matter",
      "Surface area of the nucleus"],
     ["Proportional to A", "Proportional to A^(1/3)", "Proportional to A^(2/3)", "Independent of A"]),
  *mlo("A-II, B-I, C-IV, D-III", ["A-II, B-III, C-IV, D-I", "A-I, B-II, C-IV, D-III", "A-II, B-I, C-III, D-IV"],
       "C"),
  "R = R₀A^(1/3); volume ∝ R³; density = mass/volume with mass ∝ A",
  "The volume (4/3)πR³ is proportional to A. The mass is also proportional to A, so the density is the same for all "
  "nuclei. The surface area 4πR² is proportional to A^(2/3).",
  ["R ∝ A^(1/3)", "V ∝ R³ ∝ A", "ρ ∝ A/A → independent", "S ∝ R² ∝ A^(2/3)"],
  why="A-II, B-III, ... interchanges the volume and the surface area. A-I, B-II, ... interchanges the radius and the "
      "volume. A-II, B-I, C-III, D-IV interchanges the density and the surface area.",
  ncert=NU + "size of the nucleus", seconds=50, rc=True)

Z_he, n_he = 2, 2
E_he = F(-136, 10) * Z_he ** 2 / n_he ** 2
r_he = F(53, 100) * n_he ** 2 / Z_he
v_rat = F(Z_he, n_he)
truth_he = {"a": E_he == F(-136, 10), "b": r_he == F(106, 100), "c": v_rat == 1, "d": n_he == 1,
            "e": F(136, 10) * Z_he ** 2 * (1 - F(1, 4)) == F(102, 10)}
q(AN, "Bohr model and hydrogen spectrum", "Advanced", "multi_statement",
  ms("A singly ionised helium ion (He⁺, Z = 2) has its electron in the n = 2 orbit. In the Bohr model "
     "(E_n = −13.6 Z²/n² eV, r_n = 0.53 n²/Z Å, v_n ∝ Z/n), which of the following statements are correct?",
     ["The total energy of the electron is −13.6 eV.",
      "The radius of the orbit is about 1.06 Å.",
      "The speed of the electron equals the speed of the electron in the ground state of the hydrogen atom.",
      "The orbital angular momentum of the electron is h/2π.",
      "In a transition to the n = 1 orbit, the ion emits a photon of energy 10.2 eV."]),
  *mso(truth_he, "abc", ["ab", "abce", "bcd"], "A"),
  "Bohr model for hydrogen-like ions",
  "E₂ = −13.6 × 4/4 = −13.6 eV (a true). r₂ = 0.53 × 4/2 = 1.06 Å (b true). v ∝ Z/n = 2/2 = 1, the same as for "
  "hydrogen with n = 1 (c true). The angular momentum is nh/2π = 2h/2π = h/π (d false). E₂ − E₁ = −13.6 − (−54.4) "
  "= 40.8 eV, four times the hydrogen value of 10.2 eV (e false).",
  ["E₂ = −13.6 eV; r₂ = 1.06 Å; v = v(H, n = 1)", "L = 2(h/2π)", "ΔE(2 → 1) = 40.8 eV"],
  why="Options containing (d) or (e) include a false statement; (a) and (b) only leaves out the true statement (c).",
  ncert=AC_ + "the Bohr model of the hydrogen atom", seconds=80, rc=True)


# ================================================================ Electronic Devices (B4 I6 A4)
SD = NC + "'Semiconductor Electronics: Materials, Devices and Simple Circuits', "
GATES = lambda f: tuple(int(f(a, b)) for a, b in ((0, 0), (0, 1), (1, 0), (1, 1)))

# ---- Basic
I_dd = (F(37, 10) - F(7, 10)) / F(15, 10)     # mA (kΩ)
assert I_dd == 2
assert F(7, 10) * I_dd == F(14, 10) and F(3) * I_dd == 6 and F(37, 10) * I_dd == F(74, 10)
close(0.7 * 3.7 / 1.5, 1.73, 3e-3)
q(ED, "p-n junction diode and rectifier", "Basic", "numerical",
  "A silicon diode is connected in series with a 1.5 kΩ resistor across a 3.7 V DC supply so that it is forward "
  "biased. Treating the diode as having a constant forward voltage drop of 0.7 V when it conducts, the power "
  "dissipated in the diode is:",
  *opt("1.4 mW", ["6.0 mW", "7.4 mW", "1.7 mW"], "D"),
  "Diode with a constant forward drop: I = (V − 0.7)/R; power in the diode = 0.7 V × I",
  "The resistor takes the supply voltage minus the diode's drop, which fixes the current. The diode dissipates its "
  "voltage drop times this current.",
  ["I = (3.7 − 0.7)/1.5 kΩ = 2.0 mA", "P = 0.7 × 2.0 mA = 1.4 mW"],
  why="6.0 mW is the power in the resistor and 7.4 mW the total power from the supply. 1.7 mW uses a current that "
      "ignores the diode's 0.7 V drop (3.7/1.5 kΩ).",
  ncert=SD + "p-n junction diode under forward bias", seconds=35, rc=True)

q(ED, "Semiconductors", "Basic", "direct",
  "Silicon is doped with a trivalent impurity such as boron. In the energy band diagram of this p-type "
  "semiconductor, the acceptor energy level lies:",
  *opt("slightly above the top of the valence band",
       ["slightly below the bottom of the conduction band", "exactly in the middle of the band gap",
        "inside the conduction band"], "B"),
  "Energy bands of extrinsic semiconductors",
  "An acceptor atom readily accepts an electron from a neighbouring bond, leaving a hole. Very little energy is "
  "needed for this, so the acceptor level lies just above the top of the valence band.",
  ["Acceptor: accepts an electron from the valence band easily", "→ level just above E_V"],
  why="Slightly below the conduction band is the donor level of an n-type semiconductor. The acceptor level is not "
      "at mid-gap and does not lie inside either band.",
  ncert=SD + "extrinsic semiconductor (p-type)", seconds=25)

q(ED, "p-n junction diode and rectifier", "Basic", "statement_pair",
  sp("A p-n junction is forward biased when its p-side is connected to the positive terminal of a battery and its "
     "n-side to the negative terminal.",
     "When a p-n junction is reverse biased, its depletion region becomes wider."),
  SP, sp_key(True, True),
  "Forward and reverse bias of a p-n junction",
  "Forward bias means the external voltage opposes the built-in barrier: p-side to the positive terminal (Statement "
  "I true). In reverse bias the applied voltage adds to the barrier and pulls the majority carriers away from the "
  "junction, so the depletion region widens (Statement II true).",
  ["p → +, n → − : forward bias → I true", "Reverse bias: barrier V₀ + V, depletion region wider → II true"],
  why="Both statements are correct, so options calling either of them false are wrong.",
  ncert=SD + "p-n junction diode under forward bias; under reverse bias", seconds=25)

q(ED, "Semiconductors", "Basic", "match_list",
  ml("Match each item in List-I with the correct description in List-II.",
     ["Energy band structure of a metal", "Energy band gap of an insulator", "Energy band gap of a semiconductor",
      "Electrical behaviour of pure silicon at 0 K"],
     ["The conduction band is partly filled, or overlaps the valence band", "Greater than 3 eV", "Less than 3 eV",
      "It behaves as an insulator"]),
  *mlo("A-I, B-II, C-III, D-IV", ["A-I, B-III, C-II, D-IV", "A-IV, B-II, C-III, D-I", "A-I, B-II, C-IV, D-III"],
       "C"),
  "Classification of solids on the basis of energy bands",
  "In metals the conduction band is partly filled or overlaps the valence band, so electrons can move freely. "
  "Insulators have a large gap, Eg > 3 eV; semiconductors a small gap, Eg < 3 eV. At 0 K a pure semiconductor has "
  "its valence band full and conduction band empty, so it behaves as an insulator.",
  ["Metal → I", "Insulator → II", "Semiconductor → III", "Pure Si at 0 K → IV"],
  why="A-I, B-III, ... interchanges the band gaps of insulators and semiconductors. A-IV, ... calls a metal an "
      "insulator. A-I, B-II, C-IV, D-III mixes up the band gap of a semiconductor with the behaviour of pure "
      "silicon at 0 K.",
  ncert=SD + "classification of metals, conductors and semiconductors (on the basis of energy bands)", seconds=45)

# ---- Intermediate
Vp_hw = 12 * math.sqrt(2) - 0.7
close(Vp_hw, 16.27, 1e-3)
close(12 - 0.7, 11.3)
close(12 * math.sqrt(2), 16.97, 1e-3)
close(12 * math.sqrt(2) - 1.4, 15.57, 1e-3)
q(ED, "p-n junction diode and rectifier", "Intermediate", "numerical",
  "The secondary of a transformer gives an alternating voltage of 12 V (rms). It feeds a half-wave rectifier made of "
  "a single silicon diode in series with a load resistor. Treating the diode as having a constant forward drop of "
  "0.7 V when it conducts, the peak voltage across the load is about:",
  *opt("16.3 V", ["11.3 V", "17.0 V", "15.6 V"], "D"),
  "Peak value V₀ = √2 V_rms; the conducting diode takes away its forward drop",
  "The load receives the peak of the secondary voltage minus the diode's forward drop during the conducting half "
  "cycle.",
  ["V₀ = √2 × 12 ≈ 16.97 V", "Peak across load ≈ 16.97 − 0.7 ≈ 16.3 V"],
  why="11.3 V subtracts the drop from the rms value instead of the peak. 17.0 V ignores the diode's drop. 15.6 V "
      "subtracts two diode drops, though only one diode conducts.",
  ncert=SD + "application of junction diode as a rectifier", seconds=50, rc=True)

Iz = lambda Vin: (F(Vin) - 5) / 100 - F(5, 500)
assert Iz(10) == F(40, 1000) and Iz(12) == F(60, 1000) and Iz(12) - Iz(10) == F(20, 1000)
assert F(2, 500) == F(4, 1000)
q(ED, "Zener diode", "Intermediate", "numerical",
  "A Zener diode of breakdown voltage 5.0 V is connected through a 100 Ω series resistor to a DC supply, and a "
  "500 Ω load resistor is connected across the Zener diode. When the supply voltage is raised from 10 V to 12 V, "
  "the Zener diode remaining in breakdown, the current through the Zener diode:",
  *opt("increases by 20 mA", ["increases by 4 mA", "remains unchanged", "increases by 3.3 mA"], "B"),
  "Zener regulator: load voltage fixed at V_Z, so the load current is fixed; extra series current goes through the "
  "Zener",
  "The load voltage stays at 5.0 V, so the load current stays at 5.0/500 = 10 mA. The series resistor carries "
  "(V_in − 5.0)/100, which rises by 2 V/100 Ω = 20 mA, and all of this increase flows through the Zener diode.",
  ["At 10 V: I_s = 50 mA, I_L = 10 mA, I_Z = 40 mA", "At 12 V: I_s = 70 mA, I_L = 10 mA, I_Z = 60 mA",
   "Increase = 20 mA"],
  why="4 mA divides the 2 V change by the load resistance, but the load voltage does not change. The Zener current "
      "does change, because the series current changes. 3.3 mA divides the 2 V change by 600 Ω, treating the "
      "resistors as if they were in series without the Zener diode.",
  ncert=SD + "Zener diode as a voltage regulator", seconds=70, rc=True)

V_node = max(5, 3)
I_R = F(V_node, 1)           # mA through 1 kΩ
assert I_R == 5 and 3 - V_node < 0       # diode from the 3 V battery is reverse biased
q(ED, "p-n junction diode and rectifier", "Intermediate", "numerical",
  "Two ideal batteries, of 5 V and 3 V, have their negative terminals earthed. The positive terminal of each is "
  "connected to the anode of its own ideal diode, and the cathodes of the two diodes are joined at a point P. P is "
  "connected to earth through a 1 kΩ resistor. The current through the resistor and the current through the diode "
  "connected to the 3 V battery are, respectively:",
  *opt("5 mA and zero", ["8 mA and 3 mA", "4 mA and 2 mA", "3 mA and 3 mA"], "A"),
  "Ideal diode: conducts with zero drop when forward biased, no current when reverse biased",
  "If the diode from the 5 V battery conducts, P is at 5 V. The diode from the 3 V battery then has its cathode at "
  "5 V and its anode at 3 V, so it is reverse biased and carries no current. All the current comes from the 5 V "
  "battery.",
  ["P at 5 V (via the conducting diode)", "3 V diode: anode 3 V < cathode 5 V → off", "I = 5 V/1 kΩ = 5 mA"],
  why="8 mA and 3 mA assume both diodes conduct and their currents add. 4 mA and 2 mA put P at the average of the "
      "two emfs. 3 mA and 3 mA let the lower voltage set the potential of P.",
  ncert=SD + "p-n junction diode under forward bias; under reverse bias", seconds=70, rc=True)

lam_gaas = 1240 / 1.4
assert 850 < lam_gaas < 900 and lam_gaas > 700
q(ED, "LED, photodiode and solar cell", "Intermediate", "assertion_reason",
  ar("A light emitting diode made of gallium arsenide (GaAs), whose band gap is about 1.4 eV, emits infrared rather "
     "than visible light.",
     "The energy of the photons emitted by an LED is about equal to the band gap of its semiconductor, and photons "
     "of energy 1.4 eV have a wavelength of about 890 nm, longer than the wavelengths of visible light."),
  AR, ar_key(True, True, True),
  "LED: emitted photon energy ≈ band gap Eg; λ = hc/Eg",
  "In an LED, electrons recombining with holes across the band gap emit photons of energy close to Eg. For "
  "Eg ≈ 1.4 eV, λ ≈ 1240/1.4 ≈ 890 nm, beyond the red end of the visible spectrum (about 700 nm), so GaAs is used "
  "for infrared LEDs. R gives exactly this reason.",
  ["hν ≈ Eg = 1.4 eV", "λ = 1240/1.4 ≈ 890 nm > 700 nm → infrared", "R explains A"],
  why="Both statements are true and the photon energy fixed by the band gap is the reason the light is infrared, so "
      "R is the correct explanation of A.",
  ncert=SD + "optoelectronic junction devices (light emitting diode)", seconds=45)

AND_ = lambda a, b: a & b
OR_ = lambda a, b: a | b
NAND_ = lambda a, b: 1 - (a & b)
NOR_ = lambda a, b: 1 - (a | b)
assert GATES(lambda a, b: 1 - AND_(a, b)) == GATES(NAND_)
assert GATES(lambda a, b: OR_(a, a)) == GATES(lambda a, b: a)        # OR with joined inputs is a buffer, not NOT
q(ED, "Logic gates", "Intermediate", "statement_pair",
  sp("An AND gate followed by a NOT gate behaves as a NAND gate.",
     "A two-input OR gate with both its inputs joined together behaves as a NOT gate."),
  SP, sp_key(True, False),
  "Truth tables of the basic gates",
  "Inverting the output of an AND gate gives NOT(A·B), which is the NAND function (Statement I true). With both "
  "inputs of an OR gate joined, the output is A + A = A: the input is passed on unchanged, not inverted (Statement "
  "II false). It is a NAND or NOR gate with joined inputs that acts as a NOT gate.",
  ["NOT(A·B) = NAND → I true", "A + A = A (not Ā) → II false"],
  why="Statement II confuses the OR gate with the NOR gate; joining the inputs of an OR gate gives no inversion.",
  seconds=35, rc=True)

cand = {"a": NAND_, "b": NOR_, "c": OR_, "d": AND_, "e": lambda a, b: 1 - OR_(a, b)}
truth_g = {k: (f(0, 0) == 1 and f(1, 1) == 0) for k, f in cand.items()}
q(ED, "Logic gates", "Intermediate", "multi_statement",
  ms("A two-input logic gate (or combination of gates) gives an output of 1 when both inputs are 0, and an output of "
     "0 when both inputs are 1. Which of the following could it be?",
     ["A NAND gate", "A NOR gate", "An OR gate", "An AND gate", "An OR gate followed by a NOT gate"]),
  *mso(truth_g, "abe", ["ab", "abde", "ae"], "D"),
  "Truth tables of OR, AND, NAND and NOR",
  "NAND gives 1 for (0, 0) and 0 for (1, 1) (a true). NOR also gives 1 for (0, 0) and 0 for (1, 1) (b true), and an "
  "OR gate followed by a NOT gate is a NOR gate (e true). OR gives 0 for (0, 0) (c false), and AND gives 1 for "
  "(1, 1) (d false).",
  ["NAND: (0,0) → 1, (1,1) → 0 ✓", "NOR (= OR + NOT): (0,0) → 1, (1,1) → 0 ✓", "OR: (0,0) → 0 ✗; AND: (1,1) → 1 ✗"],
  why="Options containing (c) or (d) include a gate that fails one of the two conditions; (a) and (b) only, or (a) "
      "and (e) only, leave out a gate that satisfies both.",
  seconds=50, rc=True)

# ---- Advanced
edges_d = [(1, 2, 2), (2, 0, 4), (1, 2, 4), (2, 0, 2)]           # B and D merged into node 2 (diode conducting)
v_d = solve_network(3, edges_d, {0: 0, 1: 12})
assert v_d[2] == 6
I_diode = (12 - v_d[2]) / 2 - v_d[2] / 4                           # mA, from B to D
assert I_diode == F(3, 2)
vB_open, vD_open = F(12) * 4 / 6, F(12) * 2 / 6
assert vB_open == 8 and vD_open == 4 and (vB_open - vD_open) / 2 == 2
q(ED, "p-n junction diode and rectifier", "Advanced", "numerical",
  "An ideal 12 V battery is connected across two branches in parallel. Branch 1 has a 2 kΩ resistor (joined to the "
  "positive terminal) and a 4 kΩ resistor in series, meeting at point B. Branch 2 has a 4 kΩ resistor (joined to "
  "the positive terminal) and a 2 kΩ resistor in series, meeting at point D. An ideal diode is connected with its "
  "anode at B and its cathode at D. The current through the diode is:",
  *opt("1.5 mA, from B to D", ["zero, because the diode is reverse biased", "2.0 mA, from B to D",
                               "3.0 mA, from B to D"], "C"),
  "Ideal diode as a closed switch when forward biased; Kirchhoff's rules",
  "Without the diode, B would be at 12 × 4/6 = 8 V and D at 12 × 2/6 = 4 V, so the diode is forward biased and "
  "conducts, joining B and D. Then the two upper resistors (2 kΩ and 4 kΩ) are in parallel, and so are the two "
  "lower ones (4 kΩ and 2 kΩ), each pair being 4/3 kΩ, so the joined point is at 6 V. The diode current is the "
  "current arriving at B through the 2 kΩ resistor minus that leaving B through the 4 kΩ resistor.",
  ["Open: V_B = 8 V > V_D = 4 V → diode conducts", "B ≡ D at 6 V",
   "I(2 kΩ, top of branch 1) = 6/2 = 3.0 mA; I(4 kΩ, bottom of branch 1) = 6/4 = 1.5 mA",
   "Diode current = 3.0 − 1.5 = 1.5 mA, from B to D"],
  why="The diode is forward biased (B is at the higher potential), so zero is wrong. 2.0 mA divides the open-circuit "
      "4 V difference by 2 kΩ. 3.0 mA is the current in the upper resistor of branch 1, part of which continues "
      "through the 4 kΩ resistor below B.",
  ncert=SD + "p-n junction diode under forward bias", seconds=120, rc=True)

P_led = 2.0 * 20e-3
E_led = (1240 / 620) * 1.6e-19
N_ph = 0.10 * P_led / E_led
close(N_ph, 1.25e16)
close(P_led / E_led, 1.25e17)
close(0.01 * P_led / E_led, 1.25e15)
q(ED, "LED, photodiode and solar cell", "Advanced", "numerical",
  "An LED operates with a forward voltage of 2.0 V and a current of 20 mA, and emits light of wavelength 620 nm. "
  "10% of the electrical power supplied to it is converted into this light. Taking hc = 1240 eV nm and "
  "1 eV = 1.6 × 10⁻¹⁹ J, the number of photons it emits per second is about:",
  *opt("1.25 × 10¹⁶", ["1.25 × 10¹⁷", "1.25 × 10¹⁵", "2.5 × 10¹⁶"], "B"),
  "Photon emission rate = optical power/(energy per photon), with E = hc/λ",
  "The electrical power is VI. Only 10% of it emerges as light. Dividing the light power by the energy of one "
  "photon gives the number of photons per second.",
  ["Electrical power = 2.0 × 0.020 = 40 mW; light = 4.0 mW", "E = 1240/620 = 2.0 eV = 3.2 × 10⁻¹⁹ J",
   "N = 4.0 × 10⁻³/3.2 × 10⁻¹⁹ = 1.25 × 10¹⁶ s⁻¹"],
  why="1.25 × 10¹⁷ assumes all the electrical power becomes light. 1.25 × 10¹⁵ takes the efficiency as 1%. "
      "2.5 × 10¹⁶ uses half the correct photon energy.",
  ncert=SD + "optoelectronic junction devices (light emitting diode)", seconds=80, rc=True)

c1 = GATES(lambda a, b: (1 - a) & b)
c2 = GATES(lambda a, b: a & (1 - b))
c3 = GATES(lambda a, b: (1 - a) | b)
c4 = GATES(lambda a, b: (1 - a) & (1 - b))
assert (c1, c2, c3, c4) == ((0, 1, 0, 0), (0, 0, 1, 0), (1, 1, 0, 1), (1, 0, 0, 0))
q(ED, "Logic gates", "Advanced", "match_list",
  ml("Each circuit in List-I has inputs A and B. Match it with its outputs in List-II, listed for the inputs "
     "(A, B) = (0, 0), (0, 1), (1, 0), (1, 1) in that order.",
     ["A is passed through a NOT gate, and its output and B are fed to an AND gate",
      "B is passed through a NOT gate, and A and its output are fed to an AND gate",
      "A is passed through a NOT gate, and its output and B are fed to an OR gate",
      "A and B are each passed through a NOT gate, and the two outputs are fed to an AND gate"],
     ["0, 1, 0, 0", "0, 0, 1, 0", "1, 1, 0, 1", "1, 0, 0, 0"]),
  *mlo("A-I, B-II, C-III, D-IV", ["A-II, B-I, C-III, D-IV", "A-I, B-II, C-IV, D-III", "A-II, B-I, C-IV, D-III"],
       "D"),
  "Truth tables of combinations of NOT, AND and OR gates",
  "Work out each Boolean expression for the four input pairs: Ā·B is 1 only for (0, 1); A·B̄ only for (1, 0); "
  "Ā + B is 0 only for (1, 0); Ā·B̄ is 1 only for (0, 0) (it is the NOR function).",
  ["A: Ā·B → 0, 1, 0, 0", "B: A·B̄ → 0, 0, 1, 0", "C: Ā + B → 1, 1, 0, 1", "D: Ā·B̄ → 1, 0, 0, 0"],
  why="The other codes interchange the first two circuits (inverting the wrong input) or the last two (confusing the "
      "OR and AND combinations).",
  seconds=80, rc=True)

X_n = GATES(NAND_)
Y_n = tuple(1 - (x & x) for x in X_n)
assert Y_n == GATES(AND_)
truth_nand = {"a": Y_n == GATES(AND_), "b": X_n[1] == 1, "c": Y_n[2] == 0, "d": Y_n == GATES(OR_),
              "e": X_n == GATES(AND_)}
q(ED, "Logic gates", "Advanced", "multi_statement",
  ms("Inputs A and B are fed to a NAND gate, whose output is X. X is fed to both inputs of a second NAND gate, whose "
     "output is Y. Which of the following statements are correct?",
     ["Y = A·B, i.e. the circuit as a whole behaves as an AND gate.",
      "X = 1 when A = 0 and B = 1.",
      "Y = 0 when A = 1 and B = 0.",
      "The circuit as a whole behaves as an OR gate.",
      "If the second gate is removed and X is taken as the output, the circuit behaves as an AND gate."]),
  *mso(truth_nand, "abc", ["ab", "abce", "bcd"], "A"),
  "NAND as a universal gate: a NAND with joined inputs is a NOT gate",
  "X = NOT(A·B). The second NAND has both inputs equal to X, so Y = NOT(X·X) = NOT X = A·B: an AND gate (a true, d "
  "false). For (0, 1), A·B = 0 so X = 1 (b true). For (1, 0), Y = A·B = 0 (c true). X alone is the NAND function, "
  "not AND (e false).",
  ["X = NOT(A·B)", "Y = NOT X = A·B → AND", "Check (0,1): X = 1; (1,0): Y = 0"],
  why="Options containing (d) or (e) include a false statement; (a) and (b) only leaves out the true statement (c).",
  seconds=60, rc=True)


# ================================================================ Experimental Skills (B2 I3 A2)
LAB = "NMC syllabus, Experimental Skills: "

# ---- Basic
lc_sg = F(5, 10) / 50
reading = 4 + F(1, 2) + 18 * lc_sg
assert lc_sg == F(1, 100) and reading == F(468, 100)
assert 4 + 18 * lc_sg == F(418, 100) and 4 + F(1, 2) + 18 * F(5, 1000) == F(459, 100) and 4 + 18 * F(2, 100) == F(436, 100)
q(EXP, "Vernier calipers and screw gauge", "Basic", "numerical",
  "A screw gauge has a pitch of 0.5 mm and 50 divisions on its circular scale, and has no zero error. While a wire "
  "is held between the studs, the 4 mm mark of the main (linear) scale is visible and so is the 0.5 mm mark just "
  "beyond it; the 18th division of the circular scale is on the reference line. The diameter of the wire is:",
  *opt("4.68 mm", ["4.18 mm", "4.59 mm", "4.36 mm"], "B"),
  "Screw gauge reading = main scale reading + (circular scale division × least count); least count = pitch/number "
  "of circular divisions",
  "The least count is 0.5 mm/50 = 0.01 mm. Since the half-millimetre mark beyond 4 mm is also uncovered, the main "
  "scale reading is 4.5 mm.",
  ["Least count = 0.5/50 = 0.01 mm", "MSR = 4.5 mm; CSR = 18 × 0.01 = 0.18 mm", "Diameter = 4.68 mm"],
  why="4.18 mm misses the visible half-millimetre mark. 4.59 mm takes the least count as 0.005 mm. 4.36 mm misses "
      "the half-millimetre mark and takes the least count as 0.02 mm.",
  ncert=LAB + "screw gauge", seconds=40, rc=True)

q(EXP, "Thermal and fluid experiments", "Basic", "direct",
  "In the resonance-tube experiment to find the speed of sound in air, an end correction has to be added to the "
  "length of the air column because:",
  *opt("the antinode at the open end of the tube is formed slightly outside (above) the open end",
       ["the node at the water surface is formed slightly below the water surface",
        "the speed of sound in the tube is greater than in the open air",
        "the tuning fork is held slightly above the open end of the tube"], "D"),
  "Resonance in a tube closed at one end; end correction e ≈ 0.3d",
  "The water surface is a rigid closed end, so the node forms right at it. At the open end, the air just outside "
  "also takes part in the vibration, so the displacement antinode lies a little beyond the end of the tube. The "
  "effective length of the vibrating column is therefore l + e.",
  ["Closed end (water surface): node exactly at the surface", "Open end: antinode slightly outside → l_eff = l + e"],
  why="The node is at the water surface itself, not below it. The speed of sound is the same inside and outside the "
      "tube. The position of the fork does not create the correction.",
  ncert=LAB + "speed of sound in air at room temperature using a resonance tube", seconds=30)

# ---- Intermediate
h_cap = 3.0
l_cap = h_cap / math.cos(rad(60))
close(l_cap, 6.0)
close(h_cap * math.cos(rad(60)), 1.5)
close(h_cap / math.sin(rad(60)), 3.46, 2e-3)
q(EXP, "Thermal and fluid experiments", "Intermediate", "numerical",
  "In the capillary-rise experiment, water rises to a vertical height of 3.0 cm in a long, clean capillary tube held "
  "vertical. If the same tube is instead held inclined at 60° to the vertical, the length of the water column in "
  "the tube becomes:",
  *opt("6.0 cm", ["3.0 cm", "1.5 cm", "3.5 cm"], "C"),
  "Capillary rise h = 2S cos θ/(rρg) fixes the vertical height of the column",
  "The vertical height to which the water rises depends only on the surface tension, contact angle, radius and "
  "density, not on the tilt of the tube. In the tilted tube the column must be longer to reach the same vertical "
  "height: l cos 60° = h.",
  ["Vertical height stays h = 3.0 cm", "l = h/cos 60° = 3.0/0.5 = 6.0 cm"],
  why="3.0 cm assumes the length stays the same, which would give a smaller vertical height. 1.5 cm multiplies by "
      "cos 60° instead of dividing. 3.5 cm divides by sin 60°, measuring the angle from the wrong reference line.",
  ncert=LAB + "surface tension of water by capillary rise", seconds=45, rc=True)

f_rt, l1_rt, d_rt = 500, 0.158, 0.040
e_rt = 0.3 * d_rt
v_rt = 4 * f_rt * (l1_rt + e_rt)
close(v_rt, 340)
close(4 * f_rt * l1_rt, 316)
close(4 * f_rt * (l1_rt + 0.6 * d_rt), 364)
close(2 * f_rt * (l1_rt + e_rt), 170)
q(EXP, "Thermal and fluid experiments", "Intermediate", "numerical",
  "In a resonance-tube experiment with a tuning fork of frequency 500 Hz, the first resonance is obtained when the "
  "air column is 15.8 cm long. The internal diameter of the tube is 4.0 cm, and the end correction may be taken as "
  "0.3 times the diameter. The speed of sound in air is:",
  *opt("340 m/s", ["316 m/s", "364 m/s", "170 m/s"], "D"),
  "First resonance of a tube closed at one end: l₁ + e = λ/4",
  "Add the end correction to the measured length to get a quarter wavelength, then use v = fλ.",
  ["e = 0.3 × 4.0 = 1.2 cm", "λ/4 = 15.8 + 1.2 = 17.0 cm → λ = 68.0 cm", "v = 500 × 0.680 = 340 m/s"],
  why="316 m/s leaves out the end correction. 364 m/s takes the end correction as 0.6 times the diameter instead of "
      "0.6 times the radius. 170 m/s treats the first resonance length as λ/2.",
  ncert=LAB + "speed of sound in air at room temperature using a resonance tube", seconds=60, rc=True)

q(EXP, "Mechanics experiments", "Intermediate", "assertion_reason",
  ar("In the experiment to find the coefficient of viscosity of a liquid from the terminal velocity of a falling "
     "steel ball, the ball should be dropped along the axis of a wide jar, well away from its walls.",
     "Stokes' law, F = 6πηrv, applies to a sphere moving through a liquid that extends far on all sides; near the "
     "walls of the jar the motion of the ball is affected and the law no longer holds."),
  AR, ar_key(True, True, True),
  "Conditions for Stokes' law in the terminal-velocity experiment",
  "The terminal velocity is used with Stokes' law, which assumes the liquid extends far around the ball. Close to "
  "the walls, the liquid cannot flow freely round the ball, which slows it and gives a wrong value of η. That is why "
  "the ball is dropped along the axis of a wide jar: R explains A.",
  ["Stokes' law assumes a liquid extending far around the sphere", "Walls disturb the flow → wrong η",
   "So the ball is dropped along the axis → R explains A"],
  why="Both statements are true and the validity of Stokes' law is the very reason for the precaution, so R is the "
      "correct explanation of A.",
  ncert=LAB + "coefficient of viscosity of a liquid by measuring the terminal velocity of a spherical body",
  seconds=40)

# ---- Advanced
heat_lost = F(2, 10) * 400 * (100 - 40)
heat_cal = F(10, 1000) * 4200 * (40 - 20)
c_liq = (heat_lost - heat_cal) / (F(1, 10) * 20)
assert heat_lost == 4800 and heat_cal == 840 and c_liq == 1980
assert heat_lost / (F(1, 10) * 20) == 2400
assert (F(2, 10) * 400 * 80 - heat_cal) / 2 == 2780
close(float(heat_lost / (F(11, 100) * 20)), 2182, 1e-3)
q(EXP, "Thermal and fluid experiments", "Advanced", "numerical",
  "To find the specific heat capacity of a liquid by the method of mixtures, a 200 g copper block at 100 °C "
  "(specific heat capacity of copper 400 J kg⁻¹ K⁻¹) is dropped into 100 g of the liquid at 20 °C, contained in a "
  "calorimeter whose water equivalent is 10 g. The final steady temperature is 40 °C. Taking the specific heat "
  "capacity of water as 4200 J kg⁻¹ K⁻¹ and neglecting heat losses to the surroundings, the specific heat capacity "
  "of the liquid is:",
  *opt("1980 J kg⁻¹ K⁻¹", ["2400 J kg⁻¹ K⁻¹", "2780 J kg⁻¹ K⁻¹", "2180 J kg⁻¹ K⁻¹"], "B"),
  "Principle of calorimetry: heat lost by the hot body = heat gained by the liquid and the calorimeter",
  "The copper cools from 100 °C to 40 °C. The heat it gives out warms both the liquid and the calorimeter (treated "
  "as 10 g of water) from 20 °C to 40 °C.",
  ["Heat lost by copper = 0.200 × 400 × 60 = 4800 J", "Heat gained by calorimeter = 0.010 × 4200 × 20 = 840 J",
   "Liquid: 0.100 × c × 20 = 4800 − 840 = 3960 J → c = 1980 J kg⁻¹ K⁻¹"],
  why="2400 J kg⁻¹ K⁻¹ ignores the heat taken by the calorimeter. 2780 J kg⁻¹ K⁻¹ takes the copper's fall in "
      "temperature as 80 °C (100 − 20) instead of 60 °C. 2180 J kg⁻¹ K⁻¹ adds the 10 g water equivalent to the "
      "mass of the liquid, as if the calorimeter had the liquid's specific heat.",
  ncert=LAB + "specific heat capacity of a given liquid by the method of mixtures", seconds=110, rc=True)

q(EXP, "Electrical experiments", "Advanced", "match_list",
  ml("Match each graph obtained in a laboratory experiment (List-I) with the description of its shape (List-II).",
     ["Reverse-bias characteristic of a Zener diode (reverse current against reverse voltage)",
      "Forward-bias characteristic of a p-n junction diode (current against voltage)",
      "Angle of deviation against angle of incidence for a triangular glass prism",
      "Image distance against object distance (magnitudes) for a convex lens forming real images"],
     ["A curve that falls to a minimum and then rises again",
      "Current nearly zero until a particular reverse voltage, beyond which it rises very sharply at almost "
      "constant voltage",
      "Current negligible up to a threshold voltage, then rising steeply and non-linearly",
      "A curve that approaches the lines u = f and v = f asymptotically (a rectangular hyperbola)"]),
  *mlo("A-II, B-III, C-I, D-IV", ["A-III, B-II, C-I, D-IV", "A-II, B-III, C-IV, D-I", "A-III, B-II, C-IV, D-I"],
       "C"),
  "Shapes of characteristic and experimental graphs",
  "A Zener diode in reverse bias carries almost no current until its breakdown voltage, where the current rises "
  "sharply at nearly constant voltage. A junction diode in forward bias conducts appreciably only beyond the "
  "threshold (knee) voltage. The prism's deviation falls to a minimum and then rises. For a convex lens, "
  "(u − f)(v − f) = f², a rectangular hyperbola with asymptotes u = f and v = f.",
  ["Zener reverse → II", "Diode forward → III", "Prism i–δ → I", "Lens u–v → IV"],
  why="A-III, B-II, ... interchanges the Zener reverse and diode forward characteristics. The codes with C-IV, D-I "
      "interchange the prism and lens graphs.",
  ncert=LAB + "characteristic curves of a p-n junction diode and a Zener diode; i–δ curve of a prism; focal length "
              "of a convex lens", seconds=60)


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
    assert all(28 <= keys[k] <= 32 for k in LETTERS), keys
    texts = [x["question_text"] for x in QS]
    assert len(set(texts)) == len(texts)
    doc = {"schema_version": "1.0", "batch_id": "BATCH_007", "created_at": TODAY,
           "notes": "Package PHY_007_p2: 121 original Physics questions (Current Electricity to Experimental Skills), "
                    "NEET_PHY_001630..001750. Numerical answers recomputed by tools/batch_007/PHY_007_p2.py.",
           "stimuli": [], "questions": QS}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {OUT}: {len(QS)} questions")
    print("difficulty", dict(Counter(x["difficulty"] for x in QS)))
    print("formats", dict(fmts))
    print("keys", dict(sorted(keys.items())))


if __name__ == "__main__":
    main()
