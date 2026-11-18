"""Builder for batches/parts/BATCH_010_PHY_p2.json (package PHY_010_p2 of BATCH_010).

Physics, 134 original questions, NEET_PHY_002367..NEET_PHY_002500: Current Electricity, Magnetic Effects of Current
and Magnetism, Electromagnetic Induction and Alternating Currents, Electromagnetic Waves, Optics, Dual Nature of
Matter and Radiation, Atoms and Nuclei, Electronic Devices, Experimental Skills.

Every numerical answer is recomputed below with an assert next to its question; multi-statement, assertion-reason
and statement-pair keys are derived from truth tables; the plan quota, format mix and answer-key balance are
asserted before anything is written. If any assert fails, nothing is written.

    python tools/batch_010/PHY_010_p2.py        (run from docs/neet-bank)
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
PLAN = ROOT / "batches" / "plans" / "BATCH_010_plan.json"
OUT = ROOT / "batches" / "parts" / "BATCH_010_PHY_p2.json"
PACKAGE = "PHY_010_p2"
FIRST_ID = 2367
COUNT = 134

ES = "Electrostatics"
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
NC11 = "Class 11 Physics, "
rad, deg = math.radians, math.degrees
LAB = "NCERT Physics laboratory work (NMC experimental skills), "

# ================================================================ Current Electricity (B6 I8 A6)
CEC = NC + "'Current Electricity', "

# ---- Basic
mu_, m_e9, e_ = 4.0e-3, 9.0e-31, 1.6e-19
tau_ = mu_ * m_e9 / e_
close(tau_, 2.25e-14)
close(mu_ * e_ / m_e9, 7.1e8, 1e-2)
q(CE, "Drift velocity and Ohm's law", "Basic", "numerical",
  "The mobility of the free electrons in a metal is 4.0 × 10⁻³ m² V⁻¹ s⁻¹. Taking the electron mass as "
  "9.0 × 10⁻³¹ kg and e = 1.6 × 10⁻¹⁹ C, the average relaxation time of the free electrons is:",
  *opt("2.25 × 10⁻¹⁴ s", ["7.1 × 10⁸ s", "1.1 × 10⁻¹⁴ s", "4.5 × 10⁻¹⁴ s"], "D"),
  "Mobility μ = v_d/E = eτ/m, so τ = μm/e",
  "The drift speed acquired in a field E is eEτ/m, so the mobility (drift speed per unit field) is eτ/m. Solving "
  "for the relaxation time gives τ = μm/e.",
  ["τ = μm/e", "τ = (4.0 × 10⁻³ × 9.0 × 10⁻³¹)/(1.6 × 10⁻¹⁹)", "τ = 2.25 × 10⁻¹⁴ s"],
  why="7.1 × 10⁸ s comes from μe/m, the inverted relation (and its unit would be s⁻¹, not s). 1.1 × 10⁻¹⁴ s and "
      "4.5 × 10⁻¹⁴ s bring in a spurious factor of 1/2 or 2 in the relation μ = eτ/m.",
  ncert=CEC + "drift of electrons and the origin of resistivity; mobility", seconds=45, rc=True)

rho_t, L_t, r2_t, r1_t = 2.0e-8, 3.14, 3e-3, 1e-3
A_t = 3.14 * (r2_t ** 2 - r1_t ** 2)
R_t = rho_t * L_t / A_t
close(R_t, 2.5e-3)
close(rho_t * L_t / (3.14 * r2_t ** 2), 2.2e-3, 1e-2)
close(rho_t * L_t / (3.14 * (r2_t - r1_t) ** 2), 5.0e-3)
close(rho_t * L_t / (3.14 * r1_t ** 2), 2.0e-2)
q(CE, "Resistivity and temperature", "Basic", "numerical",
  "A metal tube 3.14 m long has an outer radius of 3 mm and an inner radius of 1 mm. The resistivity of the metal is "
  "2.0 × 10⁻⁸ Ω m. Taking π = 3.14, the resistance of the tube between its two ends (current flowing along its "
  "length) is:",
  *opt("2.5 × 10⁻³ Ω", ["2.2 × 10⁻³ Ω", "5.0 × 10⁻³ Ω", "2.0 × 10⁻² Ω"], "B"),
  "R = ρL/A, where A is the area of the conducting cross-section",
  "The current flows through the metal wall only, so the cross-sectional area is the ring between the two circles: "
  "A = π(r₂² − r₁²).",
  ["A = 3.14 × (9 − 1) × 10⁻⁶ m² = 2.512 × 10⁻⁵ m²",
   "R = ρL/A = (2.0 × 10⁻⁸ × 3.14)/(2.512 × 10⁻⁵)", "R = 2.5 × 10⁻³ Ω"],
  why="2.2 × 10⁻³ Ω uses the full disc of the outer radius, ignoring the hollow. 5.0 × 10⁻³ Ω uses π(r₂ − r₁)² "
      "instead of π(r₂² − r₁²). 2.0 × 10⁻² Ω uses the area of the inner circle, which carries no current.",
  ncert=CEC + "resistivity of various materials (R = ρl/A)", seconds=60, rc=True)

Rmax_ = F(2 + 3 + 6)
Rmin_ = 1 / (F(1, 2) + F(1, 3) + F(1, 6))
assert Rmin_ == 1 and Rmax_ / Rmin_ == 11 and Rmax_ / 2 == F(11, 2)
q(CE, "Combination of resistors", "Basic", "numerical",
  "Three resistors of 2 Ω, 3 Ω and 6 Ω are available. The ratio of the largest to the smallest equivalent "
  "resistance that can be obtained by connecting all three of them together is:",
  *opt("11", ["5.5", "6", "1/11"], "C"),
  "Series gives the largest and parallel the smallest equivalent resistance",
  "With all three used, the largest resistance is the series value and the smallest is the parallel value, which "
  "is less than the smallest single resistor.",
  ["Series: 2 + 3 + 6 = 11 Ω", "Parallel: 1/R = 1/2 + 1/3 + 1/6 = 1, so R = 1 Ω", "Ratio = 11/1 = 11"],
  why="5.5 takes the smallest resistance as 2 Ω, the smallest single resistor, but a parallel combination is less "
      "than its smallest member. 6 takes the largest resistance as the largest single resistor. 1/11 inverts the "
      "ratio asked for.",
  ncert=CEC + "combination of resistors - series and parallel", seconds=40, rc=True)

eps_, Isc_, Rl_ = F(3, 2), F(3), F(1)
r_ = eps_ / Isc_
I_ = eps_ / (Rl_ + r_)
assert r_ == F(1, 2) and I_ == 1 and I_ * Rl_ == 1
q(CE, "Cells, emf and internal resistance", "Basic", "numerical",
  "A cell of emf 1.5 V gives a current of 3.0 A when its terminals are joined by a thick wire of negligible "
  "resistance. When the same cell is connected across a 1.0 Ω resistor instead, the potential difference between "
  "its terminals is:",
  *opt("1.0 V", ["1.5 V", "0.5 V", "3.0 V"], "D"),
  "Short-circuit current ε/r gives the internal resistance; then V = ε − Ir",
  "On short circuit the whole emf drives current through the internal resistance alone: r = ε/I_sc. With the "
  "external resistor, I = ε/(R + r) and the terminal voltage is IR.",
  ["r = 1.5/3.0 = 0.5 Ω", "I = 1.5/(1.0 + 0.5) = 1.0 A", "V = IR = 1.0 × 1.0 = 1.0 V (= ε − Ir = 1.5 − 0.5)"],
  why="1.5 V is the emf, the terminal voltage only when no current is drawn. 0.5 V is the drop inside the cell, "
      "not across its terminals. 3.0 V multiplies the short-circuit current by the external resistance, but that "
      "current no longer flows once the resistor is connected.",
  ncert=CEC + "cells, emf, internal resistance", seconds=45, rc=True)

q(CE, "Drift velocity and Ohm's law", "Basic", "direct",
  "The dimensional formula of the electrical conductivity σ of a material (σ = 1/ρ, where ρ is its resistivity) is:",
  *opt("[M⁻¹ L⁻³ T³ A²]", ["[M L³ T⁻³ A⁻²]", "[M⁻¹ L⁻² T³ A²]", "[M⁻¹ L⁻¹ T³ A²]"], "B"),
  "Dimensions from R = V/I and ρ = RA/L",
  "Resistance R = V/I has dimensions [M L² T⁻³ A⁻²]. Resistivity ρ = RA/L adds one power of length: "
  "[M L³ T⁻³ A⁻²]. Conductivity is its reciprocal.",
  ["[V] = [M L² T⁻³ A⁻¹], so [R] = [M L² T⁻³ A⁻²]", "[ρ] = [R][L] = [M L³ T⁻³ A⁻²]",
   "[σ] = [ρ]⁻¹ = [M⁻¹ L⁻³ T³ A²]"],
  why="[M L³ T⁻³ A⁻²] is the resistivity itself. [M⁻¹ L⁻² T³ A²] is the conductance (1/R), which lacks the "
      "length factor. [M⁻¹ L⁻¹ T³ A²] has the wrong power of length.",
  ncert=CEC + "Ohm's law; resistivity and conductivity", seconds=50)

Q_, t_, Rh_ = 120, 60, 5
I_h = Q_ / t_
H_ = I_h ** 2 * Rh_ * t_
assert I_h == 2 and H_ == 1200 and Q_ ** 2 * Rh_ == 72000 and I_h ** 2 * Rh_ == 20
q(CE, "Drift velocity and Ohm's law", "Basic", "numerical",
  "A charge of 120 C flows at a steady rate through a 5 Ω resistor in 1 minute. The heat produced in the resistor "
  "is:",
  *opt("1200 J", ["72 kJ", "20 J", "600 J"], "C"),
  "Joule heating H = I²Rt with I = Q/t",
  "A steady flow of 120 C in 60 s is a current of 2 A. The heat produced is I²Rt (equivalently QV, with "
  "V = IR = 10 V).",
  ["I = 120/60 = 2 A", "H = I²Rt = 4 × 5 × 60 = 1200 J", "Check: H = QV = 120 × 10 = 1200 J"],
  why="72 kJ uses Q²R, which is not a heat (it leaves out the division by t). 20 J is I²R, the power in watts, "
      "not the heat in one minute. 600 J halves the correct value, as if the energy were ½QV (the energy stored in "
      "a capacitor), but a resistor carrying a steady current dissipates QV.",
  ncert=CEC + "electrical energy, power", seconds=40, rc=True)

# ---- Intermediate
Rring = F(36)
a1_, a2_ = Rring / 6, Rring * 5 / 6
Rab_ = a1_ * a2_ / (a1_ + a2_)
assert Rab_ == 5
q(CE, "Combination of resistors", "Intermediate", "numerical",
  "A uniform wire of resistance 36 Ω is bent into a complete circle. The resistance between two points on the "
  "circle whose radii make an angle of 60° with each other is:",
  *opt("5 Ω", ["6 Ω", "9 Ω", "30 Ω"], "A"),
  "The two arcs between the points are in parallel; arc resistance is proportional to arc length",
  "The 60° arc is 1/6 of the circle and the other arc is 5/6 of it. Current can go either way round, so the two "
  "arcs are in parallel.",
  ["Short arc: 36/6 = 6 Ω; long arc: 36 × 5/6 = 30 Ω", "R = (6 × 30)/(6 + 30) = 180/36 = 5 Ω"],
  why="6 Ω and 30 Ω are the two arcs taken alone; the other path is ignored. 9 Ω is the resistance between "
      "diametrically opposite points (two 18 Ω halves in parallel).",
  ncert=CEC + "combination of resistors", seconds=50, rc=True)

R20_, alpha_, V_, I_n = 50, 2.0e-4, 220, 4.0
Rhot_ = V_ / I_n
T_ = 20 + (Rhot_ / R20_ - 1) / alpha_
close(Rhot_, 55)
close(T_, 520)
close(20 + (Rhot_ - R20_) / Rhot_ / alpha_, 474.5, 1e-2)
close(20 + (Rhot_ / R20_) / alpha_, 5520)
q(CE, "Resistivity and temperature", "Intermediate", "numerical",
  "The heating coil of a toaster has a resistance of 50 Ω at 20 °C. When it is connected to a 220 V supply, the "
  "current settles at a steady value of 4.0 A. The temperature coefficient of resistance of its alloy is "
  "2.0 × 10⁻⁴ °C⁻¹ (constant, referred to 20 °C). The steady temperature of the coil is:",
  *opt("520 °C", ["500 °C", "about 475 °C", "5520 °C"], "B"),
  "R_T = R₂₀[1 + α(T − 20 °C)]; the hot resistance is V/I",
  "At the steady temperature the coil's resistance is 220 V/4.0 A = 55 Ω. The fractional rise in resistance, "
  "divided by α, gives the rise in temperature above 20 °C.",
  ["R_T = 220/4.0 = 55 Ω", "55 = 50[1 + 2.0 × 10⁻⁴ (T − 20)]", "T − 20 = 0.10/(2.0 × 10⁻⁴) = 500 °C",
   "T = 520 °C"],
  why="500 °C is only the rise in temperature; the coil started at 20 °C. 'About 475 °C' divides the change in "
      "resistance by the hot resistance (55 Ω) instead of the resistance at the reference temperature. 5520 °C "
      "uses R_T/R₂₀ in place of (R_T/R₂₀ − 1).",
  ncert=CEC + "temperature dependence of resistivity", seconds=75, rc=True)

r_p = F(1)
P_ = lambda R: R / (R + r_p) ** 2          # in units of ε²
ratio_ = P_(2 * r_p) / P_(r_p)
assert ratio_ == F(8, 9) and F(2, 3) == 2 * r_p / (2 * r_p + r_p)
q(CE, "Cells, emf and internal resistance", "Intermediate", "numerical",
  "A cell of emf ε and internal resistance r is connected across an external resistor R. The power delivered to "
  "the resistor when R = 2r, expressed as a fraction of the largest power the cell can deliver to any external "
  "resistor, is:",
  *opt("8/9", ["2/3", "1/2", "4/9"], "D"),
  "Power in the load P = ε²R/(R + r)²; it is greatest when R = r, where P_max = ε²/(4r)",
  "Write the load power for R = 2r and divide by the maximum value, which occurs at R = r.",
  ["P(2r) = ε² × 2r/(3r)² = 2ε²/(9r)", "P_max = P(r) = ε² r/(2r)² = ε²/(4r)", "P(2r)/P_max = (2/9) × 4 = 8/9"],
  why="2/3 is the efficiency R/(R + r) at R = 2r, the fraction of the cell's own output delivered to the load, not "
      "a comparison with the maximum. 1/2 is the efficiency at maximum power. 4/9 is (2/3)², a wrong way of "
      "scaling the power.",
  ncert=CEC + "cells, emf, internal resistance; electrical power", seconds=75, rc=True)

V_mb, l_mb = F(2), F(40)
VX_ = V_mb * l_mb / 100
assert VX_ == F(4, 5) and V_mb - VX_ == F(6, 5)
q(CE, "Wheatstone and metre bridge", "Intermediate", "numerical",
  "In a metre bridge, an ideal cell of emf 2.0 V is connected directly across the two ends of the 100 cm bridge "
  "wire, whose resistance is 4.0 Ω. An unknown resistance X is in the left gap and a known resistance in the right "
  "gap, and the null point is found 40.0 cm from the left end. At balance, the potential difference across X is:",
  *opt("0.80 V", ["1.20 V", "2.0 V", "1.6 V"], "A"),
  "At the null point the jockey and the X-R junction are at the same potential",
  "The cell maintains 2.0 V across the uniform wire, so the potential falls uniformly along it. The gap "
  "resistances X and R are connected between the same two ends as the wire. At balance the junction of X and R is "
  "at the same potential as the null point, so the drop across X equals the drop across the first 40.0 cm of wire.",
  ["Potential drop per cm of wire = 2.0 V/100 cm = 0.020 V/cm", "Drop across 40.0 cm = 0.80 V",
   "So the potential difference across X = 0.80 V (and across R it is 1.20 V)"],
  why="1.20 V is the drop across the right-hand 60 cm, i.e. across the known resistance. 2.0 V is the whole emf, "
      "shared between X and the known resistance. 1.6 V multiplies the wire's 4.0 Ω by 0.4 as if it were a current "
      "in amperes.",
  ncert=CEC + "Wheatstone bridge; metre bridge (balance condition)", seconds=70, rc=True)

q(CE, "Kirchhoff's laws", "Intermediate", "direct",
  "While solving a circuit with Kirchhoff's rules, a student assumes that the current in one branch flows from "
  "point P to point Q, and the equations give this current as −2 A. This result means that:",
  *opt("a current of 2 A flows in that branch from Q to P",
       ["the equations are inconsistent, so the circuit must be solved again with the opposite direction assumed",
        "a current of 2 A flows from P to Q, the negative sign showing only that the branch contains a cell",
        "no current flows in that branch, because a current cannot be negative"], "C"),
  "Assumed directions of currents in Kirchhoff's rules",
  "The direction of each unknown current may be assumed arbitrarily. If the solution comes out negative, the "
  "magnitude is still correct and the actual current flows opposite to the assumed direction; nothing needs to "
  "be solved again.",
  ["Assumed P → Q, result −2 A", "Magnitude 2 A, actual direction Q → P"],
  why="The equations are consistent; a negative value is a normal outcome of an arbitrary choice of direction. The "
      "sign has nothing to do with whether the branch contains a cell. A negative current is a current in the "
      "opposite direction, not zero.",
  ncert=CEC + "Kirchhoff's rules", seconds=40)

q(CE, "Cells, emf and internal resistance", "Intermediate", "statement_pair",
  sp("Two cells of emfs ε₁ and ε₂ (ε₁ > ε₂) and internal resistances r₁ and r₂ are connected in series, with the "
     "negative terminal of one joined to the negative terminal of the other. The internal resistance of the "
     "combination is r₁ + r₂.",
     "For the same connection, the emf of the combination is ε₁ − ε₂."),
  SP, sp_key(True, True),
  "Cells in series: emfs add algebraically, internal resistances always add",
  "Whichever way round the cells are joined, the current passes through both internal resistances one after the "
  "other, so r_eq = r₁ + r₂ (Statement I true). When like terminals are joined, the emfs act against each other "
  "and the net emf is ε₁ − ε₂ (Statement II true).",
  ["Statement I: series internal resistances add → true", "Statement II: opposing emfs subtract → true"],
  why="Reversing a cell changes the sign of its emf in the sum but not its internal resistance, so neither "
      "statement is false.",
  ncert=CEC + "cells in series and in parallel", seconds=50)

q(CE, "Drift velocity and Ohm's law", "Intermediate", "assertion_reason",
  ar("For a metal wire carrying a large current, the graph of the potential difference V across it (y-axis) "
     "against the current I (x-axis) bends upwards, its slope increasing as the current increases.",
     "A large current heats the wire, and the resistivity of a metal increases as its temperature rises."),
  AR, ar_key(True, True, True),
  "Ohm's law holds only at constant temperature; resistivity of metals rises with temperature",
  "The slope V/I of the graph is the resistance. A large current raises the temperature of the wire (Joule "
  "heating), the resistivity of the metal increases, and so the resistance, and with it the slope, increases. "
  "R is therefore the direct cause of A.",
  ["A: true (V–I graph curves away from the straight line)", "R: true (ρ of a metal increases with T)",
   "Rising resistance with heating is exactly why the slope increases → R explains A"],
  why="Both statements are true and the heating of the wire is the cause of the departure from the straight line, "
      "so the options saying R does not explain A, or that either statement is false, are wrong.",
  ncert=CEC + "limitations of Ohm's law; temperature dependence of resistivity", seconds=50)

q(CE, "Cells, emf and internal resistance", "Intermediate", "match_list",
  ml("A battery of emf 12 V and internal resistance 2 Ω is connected, in turn, to each external resistor listed in "
     "List-I. Match each resistor with the power dissipated in it (List-II).",
     ["2 Ω", "4 Ω", "10 Ω", "22 Ω"],
     ["10 W", "18 W", "5.5 W", "16 W"]),
  *mlo("A-II, B-IV, C-I, D-III", ["A-IV, B-II, C-I, D-III", "A-II, B-IV, C-III, D-I", "A-II, B-I, C-IV, D-III"],
       "B"),
  "Power in the load P = I²R with I = ε/(R + r)",
  "For each resistor find I = 12/(R + 2) and then P = I²R. The power is greatest (18 W) when R equals the "
  "internal resistance.",
  ["2 Ω: I = 3 A, P = 18 W", "4 Ω: I = 2 A, P = 16 W", "10 Ω: I = 1 A, P = 10 W", "22 Ω: I = 0.5 A, P = 5.5 W"],
  why="The other codes exchange 18 W and 16 W (forgetting that maximum power occurs at R = r) or 10 W and 5.5 W "
      "(as if power always rose with R).",
  ncert=CEC + "cells, emf, internal resistance; electrical power", seconds=90)
for R_, P_w in ((2, 18), (4, 16), (10, 10), (22, F(11, 2))):
    assert F(12, R_ + 2) ** 2 * R_ == P_w

# ---- Advanced
vb = solve_network(4, [(0, 1, 2), (1, 2, 4), (0, 3, 4), (3, 2, 2), (1, 3, 4)], {0: 6, 2: 0})
Ig_ = (vb[1] - vb[3]) / 4
assert vb[1] == F(18, 5) and vb[3] == F(12, 5) and Ig_ == F(3, 10)
v0 = solve_network(3, [(0, 1, 2), (1, 2, 4), (0, 1, 4), (1, 2, 2)], {0: 6, 2: 0})   # B and D merged (zero-resistance G)
assert (6 - v0[1]) / 2 - v0[1] / 4 == F(3, 4)
q(CE, "Wheatstone and metre bridge", "Advanced", "numerical",
  "In a Wheatstone bridge, P = 2 Ω joins A to B, Q = 4 Ω joins B to C, R = 4 Ω joins A to D and S = 2 Ω joins D "
  "to C. An ideal 6 V battery is connected with its positive terminal at A and its negative terminal at C, and a "
  "galvanometer of resistance 4 Ω is connected between B and D. The current through the galvanometer is:",
  *opt("0.30 A, from B to D", ["0.30 A, from D to B", "0.75 A, from B to D", "zero, because the bridge is balanced"],
       "D"),
  "Kirchhoff's junction rule at B and D (node potentials), with the galvanometer treated as a 4 Ω resistor",
  "P/Q = 1/2 but R/S = 2, so the bridge is not balanced. Take C as 0 V and A as 6 V and write the junction rule at "
  "B and at D, including the current through the galvanometer.",
  ["At B: (6 − V_B)/2 = V_B/4 + (V_B − V_D)/4 → 4V_B − V_D = 12",
   "At D: (6 − V_D)/4 = V_D/2 + (V_D − V_B)/4 → 4V_D − V_B = 6",
   "Solving: V_B = 3.6 V, V_D = 2.4 V", "I_G = (3.6 − 2.4)/4 = 0.30 A, from B (higher potential) to D"],
  why="'From D to B' reverses the direction: B is at the higher potential. 0.75 A is the galvanometer current if "
      "its resistance is ignored (B and D at the same potential). The bridge is not balanced, because "
      "P/Q ≠ R/S.",
  ncert=CEC + "Kirchhoff's rules; Wheatstone bridge", seconds=150, rc=True)

cube = [(a, b, 4) for a in range(8) for b in range(a + 1, 8) if bin(a ^ b).count("1") == 1]
assert len(cube) == 12
assert equivalent_resistance(8, cube, 0, 3) == 3
assert equivalent_resistance(8, cube, 0, 1) == F(7, 3) and equivalent_resistance(8, cube, 0, 7) == F(10, 3)
vc = solve_network(8, cube, {0: 1, 3: 0})
assert vc[1] == vc[2] == F(1, 2) and vc[4] == F(2, 3)
q(CE, "Combination of resistors", "Advanced", "numerical",
  "A wire-frame cube is built from twelve equal resistors of 4.0 Ω, one along each edge. A battery is connected "
  "between two corners A and C that lie diagonally opposite each other on one face (they are not joined by an "
  "edge and are not the ends of a body diagonal). The equivalent resistance of the frame between A and C is:",
  *opt("3.0 Ω", ["2.3 Ω", "3.3 Ω", "4.0 Ω"], "B"),
  "Symmetry of the network and Kirchhoff's junction rule",
  "Hold A at potential V and C at zero. Let B and D be the other two corners of the face ABCD, and A', B', C', D' "
  "the corners of the opposite face directly behind A, B, C, D. The mirror plane that swaps A and C (and V with 0) "
  "maps B, D, B' and D' onto themselves, so these four corners are all at V/2. Let A' be at potential x; then C' is "
  "at V − x. The junction rule at A' fixes x, and the current leaving A then gives the resistance.",
  ["Junction rule at A' (edge resistance r): (V − x) + 2(V/2 − x) = 0 → x = 2V/3",
   "Current leaving A: to B and D, 2 × (V/2)/r = V/r; to A', (V − 2V/3)/r = V/(3r)",
   "Total I = 4V/(3r) → R = 3r/4 = 3 × 4.0/4 = 3.0 Ω"],
  shortcut="For a cube of edge resistance r: adjacent corners 7r/12, face diagonal 3r/4, body diagonal 5r/6.",
  why="2.3 Ω (7r/12) is the resistance between the ends of one edge, and 3.3 Ω (5r/6) is between the ends of a body "
      "diagonal. 4.0 Ω (= r) keeps only the two two-edge paths round the face, in parallel, and ignores the rest of "
      "the cube.",
  ncert=CEC + "combination of resistors; Kirchhoff's rules", seconds=120, rc=True)

V_pq = (F(6, 1) + F(3, 1) + F(0)) / (F(1) + F(1) + F(1, 2))
I_res, I_3 = V_pq / 2, (V_pq - 3) / 1
assert V_pq == F(18, 5) and I_res == F(9, 5) and I_3 == F(3, 5)
q(CE, "Kirchhoff's laws", "Advanced", "numerical",
  "Three branches are connected in parallel between two points P and Q. Branch 1 is a cell of emf 6 V and internal "
  "resistance 1 Ω; branch 2 is a cell of emf 3 V and internal resistance 1 Ω; branch 3 is a 2 Ω resistor. Both "
  "cells have their positive terminals towards P. The current in the 2 Ω resistor, and the current in the 3 V "
  "cell, are:",
  *opt("1.8 A; 0.6 A, entering the positive terminal of the 3 V cell",
       ["1.8 A; 0.6 A, leaving the positive terminal of the 3 V cell", "2.0 A; zero in the 3 V cell",
        "3.0 A; 3.0 A, leaving the positive terminal of the 3 V cell"], "C"),
  "Kirchhoff's junction rule at P with V = V_P − V_Q as the unknown",
  "Let V be the potential of P above Q. The current leaving P through each cell branch is (V − ε)/r, and through "
  "the resistor it is V/2. Their sum must be zero.",
  ["(V − 6)/1 + (V − 3)/1 + V/2 = 0 → 2.5V = 9 → V = 3.6 V", "Current in the 2 Ω resistor = 3.6/2 = 1.8 A",
   "3 V cell: (3.6 − 3)/1 = 0.6 A flows from P into its positive terminal, so it is being charged",
   "6 V cell supplies (6 − 3.6)/1 = 2.4 A = 1.8 + 0.6 A ✓"],
  why="'Leaving the positive terminal' would mean the 3 V cell is discharging, but V_PQ = 3.6 V exceeds its emf, "
      "so it is being charged. '2.0 A; zero' ignores the 3 V cell and uses only the 6 V cell. '3.0 A' wrongly puts "
      "the two cells in series round one loop with the resistor.",
  ncert=CEC + "Kirchhoff's rules", seconds=150, rc=True)

truth = {"a": True, "b": True, "c": True, "d": True, "e": False}
Rb = F(1)
Ptot_before, Ptot_after = 1 / (Rb + Rb / 2), 1 / (2 * Rb)
PA0, PB0 = (1 / (F(3, 2))) ** 2, (1 / F(3, 2) / 2) ** 2
PA1, PB1 = F(1, 2) ** 2, F(1, 2) ** 2
assert PB0 == PA0 / 4 and PA1 < PA0 and PB1 > PB0 and 1 > PA0 and Ptot_after < Ptot_before
q(CE, "Combination of resistors", "Advanced", "multi_statement",
  ms("Three identical bulbs A, B and C are connected to an ideal battery: B and C are in parallel with each other, "
     "and this pair is in series with A. Treat the resistance of each bulb as constant. Which of the following "
     "statements are correct?",
     ["Bulb A glows the brightest of the three.",
      "Each of B and C dissipates one-quarter of the power dissipated in A.",
      "If the filament of C breaks, A becomes dimmer and B becomes brighter.",
      "If B is short-circuited by a wire of negligible resistance, C goes out and A becomes brighter.",
      "If the filament of C breaks, the total power drawn from the battery increases."]),
  *mso(truth, "abcd", ["abc", "ace", "bde"], "D"),
  "Series-parallel combination; P = I²R for equal resistances",
  "Let each bulb have resistance R and the battery voltage be V. Initially R_eq = 1.5R, so the current through A is "
  "I = V/(1.5R) and B and C carry I/2 each. A dissipates I²R and each of B, C dissipates (I/2)²R = I²R/4, so (a) "
  "and (b) are true. If C breaks, A and B are in series: the current V/(2R) is less than I, so A is dimmer, but B "
  "now carries V/(2R), more than I/2, so B is brighter (c true). Shorting B also shorts C (they are in parallel), "
  "and A gets the full battery voltage, so it becomes brighter (d true). When C breaks, R_eq rises from 1.5R to 2R, "
  "so the total power V²/R_eq decreases (e false).",
  ["(a) P_A = I²R is the largest → true", "(b) P_B = P_C = I²R/4 → true",
   "(c) I_A: V/1.5R → V/2R (dimmer); I_B: V/3R → V/2R (brighter) → true",
   "(d) A gets full V, power V²/R > (4/9)V²/R → true", "(e) R_eq increases, so total power decreases → false"],
  why="Options without (d) miss that shorting B also removes C from the circuit and puts the full voltage across A. "
      "Options with (e) forget that removing a parallel path increases the equivalent resistance and so reduces "
      "the total power.",
  ncert=CEC + "combination of resistors; electrical power", seconds=150)

truth = {"a": True, "b": True, "c": True, "d": False, "e": True}
q(CE, "Resistivity and temperature", "Advanced", "multi_statement",
  ms("A metal wire is connected across an ideal battery that keeps a fixed potential difference between its ends. "
     "The wire is then heated to a higher temperature, its dimensions remaining practically unchanged. Which of the "
     "following statements are correct?",
     ["The average relaxation time of the free electrons decreases.",
      "The resistivity of the metal increases.",
      "The drift speed of the free electrons decreases.",
      "The electric field inside the wire decreases.",
      "The power dissipated in the wire decreases."]),
  *mso(truth, "abce", ["abcd", "bcde", "ace"], "C"),
  "ρ = m/(ne²τ); v_d = eEτ/m; E = V/L; P = V²/R",
  "At a higher temperature the ions vibrate more and the electrons collide more often, so τ decreases (a true) and "
  "ρ = m/(ne²τ) increases (b true); n hardly changes in a metal. The field E = V/L is fixed by the battery and the "
  "length (d false), so the drift speed eEτ/m decreases with τ (c true). The resistance rises, so the power V²/R "
  "falls (e true).",
  ["(a) τ decreases → true", "(b) ρ ∝ 1/τ increases → true", "(c) v_d = eEτ/m with E fixed → decreases → true",
   "(d) E = V/L is unchanged → false", "(e) P = V²/R decreases → true"],
  why="Options containing (d) wrongly let the field change; it is fixed by the battery voltage and the length. "
      "The option without (b) misses the basic increase of resistivity with temperature.",
  ncert=CEC + "drift of electrons and the origin of resistivity; temperature dependence of resistivity",
  seconds=120)

q(CE, "Wheatstone and metre bridge", "Advanced", "assertion_reason",
  ar("In a Wheatstone bridge in which P/Q = R/S, the current in the galvanometer arm stays zero even if the "
     "galvanometer is replaced by a resistor of any value.",
     "When P/Q = R/S, the two ends of the galvanometer arm are at the same potential, so no current flows through "
     "a resistor of any value connected between them."),
  AR, ar_key(True, True, True),
  "Balance condition of the Wheatstone bridge",
  "With P/Q = R/S, the potential at the P-Q junction equals that at the R-S junction (each branch divides the "
  "battery voltage in the same ratio). A resistor (or galvanometer) joining two points at equal potential carries no "
  "current, whatever its resistance, and with no current in it the potentials stay equal. So the reason given is exactly "
  "why the assertion holds.",
  ["Potentials: V_B = V_D when P/Q = R/S", "ΔV = 0 across the arm → I = 0 for any resistance", "R explains A"],
  why="Both statements are true and the equality of potentials is the cause of zero current in the arm, so the "
      "options saying R is not the explanation, or that either statement is false, are wrong.",
  ncert=CEC + "Wheatstone bridge", seconds=60)

# ================================================================ Magnetic Effects of Current and Magnetism (B6 I8 A6)
MCM = NC + "'Moving Charges and Magnetism', "
MMM = NC + "'Magnetism and Matter', "
MU0 = 4 * math.pi * 1e-7

# ---- Basic
N_, I_c, A_c, B_c = 50, 2.0, 0.05 * 0.08, 0.5
tau_c = N_ * I_c * A_c * B_c * math.sin(rad(30))
close(tau_c, 0.10)
close(N_ * I_c * A_c * B_c * math.cos(rad(30)), 0.173, 1e-2)
q(MAG, "Torque on loop and galvanometer", "Basic", "numerical",
  "A rectangular coil of 50 turns, each measuring 5.0 cm × 8.0 cm, carries a current of 2.0 A. It is placed in a "
  "uniform magnetic field of 0.50 T so that the normal to the plane of the coil makes an angle of 30° with the "
  "field. The magnitude of the torque on the coil is:",
  *opt("0.10 N m", ["0.17 N m", "0.20 N m", "2.0 × 10⁻³ N m"], "A"),
  "Torque on a current loop τ = NIAB sin θ, θ being the angle between the normal (magnetic moment) and B",
  "The magnetic moment of the coil is NIA along its normal, and the torque is m × B, of magnitude NIAB sin θ with "
  "θ = 30°.",
  ["A = 0.05 × 0.08 = 4.0 × 10⁻³ m²", "m = NIA = 50 × 2.0 × 4.0 × 10⁻³ = 0.40 A m²",
   "τ = mB sin 30° = 0.40 × 0.50 × 0.5 = 0.10 N m"],
  why="0.17 N m uses cos 30°, which is correct only if 30° is the angle between the plane of the coil and the field. "
      "0.20 N m is the maximum torque (sin θ = 1). 2.0 × 10⁻³ N m leaves out the 50 turns.",
  ncert=MCM + "torque on current loop, magnetic dipole", seconds=50, rc=True)

d_w, I_s = 0.5e-3, 2.0
n_s = 1 / d_w
B_s = MU0 * n_s * I_s
close(n_s, 2000)
close(B_s, 5.03e-3)
close(MU0 * 1000 * I_s, 2.51e-3, 1e-2)
q(MAG, "Ampere's law", "Basic", "numerical",
  "A long solenoid is made by winding a single layer of insulated wire of diameter 0.50 mm on a long tube, with the "
  "turns touching one another. A current of 2.0 A flows through it. Taking μ₀ = 4π × 10⁻⁷ T m A⁻¹, the magnetic "
  "field well inside the solenoid is about:",
  *opt("5.0 × 10⁻³ T", ["2.5 × 10⁻³ T", "1.0 × 10⁻² T", "8.0 × 10⁻⁴ T"], "B"),
  "B = μ₀nI for a long solenoid; for close-wound turns n = 1/(wire diameter)",
  "With the turns touching, each turn occupies a length equal to the wire diameter, so the number of turns per "
  "metre is 1/(0.50 × 10⁻³ m) = 2000 m⁻¹.",
  ["n = 1/(0.50 × 10⁻³) = 2000 turns per metre", "B = μ₀nI = 4π × 10⁻⁷ × 2000 × 2.0", "B ≈ 5.0 × 10⁻³ T"],
  why="2.5 × 10⁻³ T takes 1000 turns per metre (treating 0.50 mm as the radius and doubling it). 1.0 × 10⁻² T "
      "takes 4000 turns per metre. 8.0 × 10⁻⁴ T divides by 2π as in the field of a straight wire.",
  ncert=MCM + "the solenoid", seconds=50, rc=True)

q(MAG, "Magnetic materials", "Basic", "direct",
  "When a superconducting material is cooled below its transition temperature in a magnetic field, the field lines "
  "are completely expelled from its interior and it behaves as a perfect diamagnet (χ = −1). This phenomenon is "
  "known as:",
  *opt("the Meissner effect", ["magnetic hysteresis", "the Curie point", "electromagnetic induction"], "C"),
  "Perfect diamagnetism of superconductors",
  "NCERT notes that the most exotic diamagnetic materials are superconductors, metals cooled to very low "
  "temperatures, which show perfect conductivity and perfect diamagnetism. The complete expulsion of the magnetic "
  "field from a superconductor is called the Meissner effect.",
  ["Superconductor: χ = −1, B inside = 0", "Name of the phenomenon: Meissner effect"],
  why="Hysteresis is the lag of magnetisation behind the applied field in ferromagnets. The Curie point is the "
      "temperature at which a ferromagnet becomes paramagnetic. Electromagnetic induction is the production of emf "
      "by a changing magnetic flux.",
  ncert=MMM + "magnetic properties of materials - diamagnetism", seconds=30)

n_m, I_m, chi_m = 1000, 2.0, 3.0e-4
H_m = n_m * I_m
M_m = chi_m * H_m
close(H_m, 2000)
close(M_m, 0.60)
close(MU0 * M_m, 7.54e-7, 1e-2)
q(MAG, "Magnetic materials", "Basic", "numerical",
  "A long solenoid with 1000 turns per metre carries a current of 2.0 A. Its core is filled with a material of "
  "magnetic susceptibility 3.0 × 10⁻⁴. The magnetisation of the core is:",
  *opt("0.60 A m⁻¹", ["2.0 × 10³ A m⁻¹", "6.7 × 10⁶ A m⁻¹", "7.5 × 10⁻⁷ A m⁻¹"], "D"),
  "Magnetic intensity H = nI; magnetisation M = χH",
  "Inside a long solenoid the magnetic intensity is H = nI, set by the winding alone. The magnetisation produced in "
  "a linear material is M = χH.",
  ["H = nI = 1000 × 2.0 = 2.0 × 10³ A m⁻¹", "M = χH = 3.0 × 10⁻⁴ × 2.0 × 10³ = 0.60 A m⁻¹"],
  why="2.0 × 10³ A m⁻¹ is H, not M. 6.7 × 10⁶ A m⁻¹ divides H by χ instead of multiplying. 7.5 × 10⁻⁷ is μ₀M, "
      "which is in tesla (the extra field due to the core), not the magnetisation.",
  ncert=MMM + "magnetisation and magnetic intensity", seconds=45, rc=True)

q(MAG, "Torque on loop and galvanometer", "Basic", "statement_pair",
  sp("An ammeter is connected in series with the part of a circuit whose current is to be measured, and a voltmeter "
     "is connected in parallel with the element across which the potential difference is to be measured.",
     "An ideal voltmeter has zero resistance."),
  SP, sp_key(True, False),
  "Use of ammeters and voltmeters made from galvanometers",
  "An ammeter must carry the current being measured, so it goes in series; a voltmeter must have the same potential "
  "difference as the element, so it goes in parallel (Statement I true). A voltmeter should draw as little current "
  "as possible, so an ideal voltmeter has infinite resistance, not zero (Statement II false).",
  ["Statement I: true", "Statement II: ideal voltmeter → infinite resistance → false"],
  why="A zero-resistance voltmeter in parallel would short-circuit the element, so Statement II cannot be true.",
  ncert=MCM + "moving coil galvanometer (conversion into ammeter and voltmeter)", seconds=35)

Vb_, Rr_, Ra_ = F(6), F(2), F(1, 2)
assert Vb_ / (Rr_ + Ra_) == F(12, 5) and Vb_ / Rr_ == 3 and Vb_ / Ra_ == 12
q(MAG, "Torque on loop and galvanometer", "Basic", "numerical",
  "A 2.0 Ω resistor is connected across an ideal 6.0 V battery. An ammeter of resistance 0.50 Ω is then connected "
  "in series with the resistor to measure the current. The reading of the ammeter is:",
  *opt("2.4 A", ["3.0 A", "12 A", "0.60 A"], "D"),
  "A real ammeter adds its own resistance in series and so reduces the current it measures",
  "Once the ammeter is in the circuit, the battery drives current through the resistor and the ammeter in series, "
  "so the current is 6.0/(2.0 + 0.50) A. This is less than the 3.0 A that flowed without the ammeter; that is why "
  "a good ammeter must have a very small resistance.",
  ["Total resistance = 2.0 + 0.50 = 2.5 Ω", "Reading I = 6.0/2.5 = 2.4 A"],
  why="3.0 A is the current before the ammeter was inserted. 12 A divides the emf by the ammeter's resistance "
      "alone. 0.60 A is the drop in current caused by the ammeter, not its reading.",
  ncert=MCM + "moving coil galvanometer (ammeter)", seconds=40, rc=True)

# ---- Intermediate
assert F(15, 10) == F(3, 2) and (F(15, 10)) ** 2 == F(9, 4)
q(MAG, "Ampere's law", "Intermediate", "numerical",
  "A toroid is wound uniformly on a ring-shaped core whose inner radius is 10 cm and outer radius is 15 cm. A steady "
  "current flows in the winding. Within the core, the ratio of the magnetic field at the inner edge (r = 10 cm) to "
  "that at the outer edge (r = 15 cm) is:",
  *opt("1.5", ["2.25", "0.67", "1"], "B"),
  "Ampere's law for a toroid: B × 2πr = μ₀NI, so B = μ₀NI/(2πr) inside the core",
  "A circular Amperian loop of radius r inside the core is threaded by all N turns, each carrying I. B is constant "
  "along the loop by symmetry, so B = μ₀NI/(2πr): the field varies inversely as r across the core.",
  ["B ∝ 1/r", "B(10 cm)/B(15 cm) = 15/10 = 1.5"],
  why="2.25 uses B ∝ 1/r². 0.67 inverts the ratio. 1 assumes the field is the same everywhere in the core, which "
      "holds only when the core is thin compared with its radius (the usual approximation B = μ₀nI).",
  ncert=MCM + "Ampere's circuital law; the toroid", seconds=50, rc=True)

m_r, mu_r, L_r, B_r = 0.20, 0.25, 0.50, 0.50
I_r = mu_r * m_r * 10 / (B_r * L_r)
close(I_r, 2.0)
close(m_r * 10 / (B_r * L_r), 8.0)
close(mu_r * 10 / (B_r * L_r), 10.0)
q(MAG, "Force on charges and conductors", "Intermediate", "numerical",
  "A metal rod of mass 0.20 kg rests at right angles across two horizontal parallel rails 0.50 m apart. The "
  "coefficient of static friction between the rod and the rails is 0.25. A uniform vertical magnetic field of "
  "0.50 T acts in the region. Taking g = 10 m/s², the least current that must be passed through the rod (via the "
  "rails) to make it just start sliding is:",
  *opt("2.0 A", ["8.0 A", "0.50 A", "10 A"], "C"),
  "Force on a current-carrying conductor F = BIL; limiting static friction μmg",
  "The vertical field and the horizontal rod are perpendicular, so the magnetic force BIL is horizontal, along the "
  "rails. The rod starts to slide when this force equals the limiting friction μN = μmg.",
  ["Limiting friction = 0.25 × 0.20 × 10 = 0.50 N", "BIL = 0.50 N → I = 0.50/(0.50 × 0.50) = 2.0 A"],
  why="8.0 A balances the weight mg instead of the friction μmg. 0.50 A is the friction force (in newtons) "
      "reported as a current. 10 A leaves the mass out of the friction force.",
  ncert=MCM + "magnetic force on a current-carrying conductor", seconds=60, rc=True)

B1_ = 2e-7 * 10 / 0.05
out_ = (-4 / 5, 3 / 5)                  # field of wire 1 (current out of page) at P, as a unit vector
into_ = (4 / 5, 3 / 5)                  # field of wire 2 (current into page) at P
res_ = math.hypot(out_[0] + into_[0], out_[1] + into_[1]) * B1_
same_ = math.hypot(out_[0] - 4 / 5, out_[1] - 3 / 5) * B1_
close(B1_, 4e-5)
close(res_, 4.8e-5)
close(same_, 6.4e-5)
q(MAG, "Biot-Savart law", "Intermediate", "numerical",
  "Two long straight parallel wires, 6.0 cm apart, carry steady currents of 10 A each in opposite directions. Point "
  "P lies on the perpendicular bisector of the line joining the wires, in the plane perpendicular to them, at a "
  "distance of 4.0 cm from the midpoint of that line (so P is 5.0 cm from each wire). Taking μ₀ = 4π × 10⁻⁷ "
  "T m A⁻¹, the magnitude of the resultant magnetic field at P is:",
  *opt("4.8 × 10⁻⁵ T", ["6.4 × 10⁻⁵ T", "8.0 × 10⁻⁵ T", "zero"], "D"),
  "Field of a long straight wire B = μ₀I/(2πr), perpendicular to the radius; vector addition",
  "Each wire produces B = μ₀I/(2πr) = 4.0 × 10⁻⁵ T at P, perpendicular to the line from that wire to P. With the "
  "currents opposite, the components parallel to the line joining the wires cancel and the components along the "
  "bisector add. Each field makes an angle θ with the bisector direction where cos θ = 3/5.",
  ["B from each wire = 2 × 10⁻⁷ × 10/0.05 = 4.0 × 10⁻⁵ T", "Resultant = 2B cos θ = 2 × 4.0 × 10⁻⁵ × (3/5)",
   "= 4.8 × 10⁻⁵ T (directed along the bisector)"],
  why="6.4 × 10⁻⁵ T (= 2B × 4/5) is the result for currents in the same direction. 8.0 × 10⁻⁵ T adds the two "
      "fields as if they were parallel. Zero would hold only for same-direction currents at the midpoint, not here.",
  ncert=MCM + "magnetic field due to a straight current-carrying wire", seconds=120, rc=True)

q(MAG, "Magnetic dipole and bar magnet", "Intermediate", "direct",
  "Two identical short bar magnets, each of magnetic moment m, are fixed with their centres at the same point and "
  "their axes at right angles to each other, forming a cross. The pair is equivalent to a single magnetic dipole of "
  "moment:",
  *opt("√2 m, directed at 45° to the axis of each magnet",
       ["2m, directed along the bisector of the angle between their axes", "zero, because the moments cancel",
        "m, directed along the axis of either magnet"], "A"),
  "Magnetic dipole moment is a vector; moments add vectorially",
  "The two moments have equal magnitude m and are perpendicular, so their vector sum has magnitude √(m² + m²) = √2 m "
  "and lies along the bisector, at 45° to each.",
  ["|m₁ + m₂| = √(m² + m²) = √2 m", "Direction: along the bisector, 45° to each axis"],
  why="2m adds the magnitudes as if the moments were parallel. Zero would need antiparallel moments. m ignores one "
      "of the two magnets.",
  ncert=MMM + "the bar magnet (magnetic dipole moment)", seconds=40)

q(MAG, "Torque on loop and galvanometer", "Intermediate", "assertion_reason",
  ar("To convert a given galvanometer into an ammeter of a larger range, a shunt of smaller resistance is needed.",
     "The shunt is connected in series with the galvanometer so that it takes most of the potential difference."),
  AR, ar_key(True, False),
  "Conversion of a galvanometer into an ammeter: shunt in parallel, I_g G = (I − I_g) S",
  "The shunt S is connected in parallel with the galvanometer, so that most of the current bypasses it. From "
  "I_g G = (I − I_g)S, S = I_g G/(I − I_g): a larger range I needs a smaller S. So A is true. R is false: a "
  "resistance in series with the galvanometer, taking most of the voltage, is how a voltmeter is made.",
  ["A: S = I_g G/(I − I_g) decreases as I increases → true", "R: the shunt is in parallel, not in series → false"],
  why="R describes the conversion into a voltmeter, so it is false here; options that treat R as true are wrong.",
  ncert=MCM + "moving coil galvanometer", seconds=45)

q(MAG, "Force on charges and conductors", "Intermediate", "statement_pair",
  sp("A proton and an electron move at right angles to the same uniform magnetic field with momenta of equal "
     "magnitude. They take equal times to complete one revolution.",
     "In this situation, the radii of their circular paths are equal."),
  SP, sp_key(False, True),
  "Circular motion in a magnetic field: r = mv/(qB) = p/(qB), T = 2πm/(qB)",
  "The radius r = p/(qB) depends only on the momentum and the charge, and the charges have equal magnitude, so equal "
  "momenta give equal radii (Statement II true). The period 2πm/(qB) depends on the mass; the electron is about "
  "1836 times lighter and goes round much faster (Statement I false).",
  ["r = p/(|q|B): equal p, equal |q| → equal r → II true", "T = 2πm/(|q|B): different m → different T → I false"],
  why="Statement I would be true only for particles of equal mass-to-charge ratio, which a proton and an electron "
      "are not.",
  ncert=MCM + "motion in a magnetic field", seconds=45)

mom = {"A": math.pi * 0.1 ** 2 * 2, "B": 5 * 0.1 ** 2 * 2, "C": 10 * 0.05 * 0.20 * 2, "D": 50 * math.pi * 0.02 ** 2 * 2}
close(mom["A"], 0.0628)
close(mom["B"], 0.10)
close(mom["C"], 0.20)
close(mom["D"], 0.1257)
q(MAG, "Magnetic dipole and bar magnet", "Intermediate", "match_list",
  ml("Each coil in List-I carries a current of 2.0 A. Match each coil with the magnitude of its magnetic dipole "
     "moment in List-II.",
     ["A single circular turn of radius 10 cm", "A square coil of 5 turns, side 10 cm",
      "A rectangular coil of 10 turns, 5.0 cm × 20 cm", "A circular coil of 50 turns, radius 2.0 cm"],
     ["0.20 A m²", "0.063 A m²", "0.13 A m²", "0.10 A m²"]),
  *mlo("A-II, B-IV, C-I, D-III", ["A-IV, B-II, C-I, D-III", "A-II, B-IV, C-III, D-I", "A-III, B-IV, C-I, D-II"],
       "B"),
  "Magnetic moment of a coil m = NIA",
  "Multiply the number of turns, the current and the area of one turn in each case.",
  ["A: 1 × 2.0 × π(0.10)² = 0.063 A m²", "B: 5 × 2.0 × (0.10)² = 0.10 A m²", "C: 10 × 2.0 × (0.05 × 0.20) = 0.20 A m²",
   "D: 50 × 2.0 × π(0.02)² = 0.13 A m²"],
  why="The other codes exchange the moments of coils A and B, or of C and D: the square coil has five turns, and "
      "the small circular coil gains from its 50 turns.",
  ncert=MCM + "the magnetic dipole moment of a current loop", seconds=90, rc=True)

q(MAG, "Force on charges and conductors", "Intermediate", "match_list",
  ml("Match each physical quantity in List-I with its SI unit expressed in SI base units (List-II).",
     ["Magnetic field B", "Magnetic flux", "Permeability of free space μ₀", "Magnetic dipole moment"],
     ["kg m² s⁻² A⁻¹", "A m²", "kg s⁻² A⁻¹", "kg m s⁻² A⁻²"]),
  *mlo("A-III, B-I, C-IV, D-II", ["A-I, B-III, C-IV, D-II", "A-III, B-I, C-II, D-IV", "A-IV, B-I, C-III, D-II"],
       "A"),
  "F = qvB (or F = BIl) defines the tesla; Φ = BA; B = μ₀I/(2πr); m = IA",
  "From F = BIl, 1 T = 1 N A⁻¹ m⁻¹ = kg s⁻² A⁻¹. Flux adds m²: kg m² s⁻² A⁻¹. From B = μ₀I/(2πr), μ₀ has the unit "
  "T m A⁻¹ = kg m s⁻² A⁻². The magnetic moment IA is A m².",
  ["B: N/(A m) = kg m s⁻²/(A m) = kg s⁻² A⁻¹", "Φ: T m² = kg m² s⁻² A⁻¹", "μ₀: T m A⁻¹ = kg m s⁻² A⁻²", "m: A m²"],
  why="The other codes exchange the field and the flux (which differ by m²), or the permeability and the dipole "
      "moment.",
  ncert=MCM + "magnetic force (unit of B); magnetic field due to a current element", seconds=75)

# ---- Advanced
mp_, qe_, v_p, B_p = 1.6e-27, 1.6e-19, 2.0e6, 0.50
r_p = mp_ * v_p / (qe_ * B_p)
chord_ = 2 * r_p * math.sin(rad(30))
close(r_p, 0.04)
close(chord_, 0.04)
close(2 * r_p * math.cos(rad(30)), 0.0693, 1e-2)
q(MAG, "Force on charges and conductors", "Advanced", "numerical",
  "A uniform magnetic field of 0.50 T fills the whole region on one side of a plane boundary and is parallel to "
  "that boundary. A proton (mass 1.6 × 10⁻²⁷ kg, charge 1.6 × 10⁻¹⁹ C) moving at 2.0 × 10⁶ m/s, perpendicular to "
  "the field, enters the field region with its velocity making an angle of 30° with the boundary. It moves along "
  "an arc and comes out again through the same boundary. The distance between the point where it enters and the "
  "point where it leaves is:",
  *opt("4.0 cm", ["6.9 cm", "8.0 cm", "2.0 cm"], "C"),
  "Circular motion r = mv/(qB); geometry of a chord: the angle between the tangent and the chord is half the arc",
  "Inside the field the proton moves on a circle of radius r = mv/(qB). The entry and exit points lie on the "
  "boundary, so they are the ends of a chord. The velocity (tangent) at entry makes 30° with this chord, so the "
  "chord length is 2r sin 30°, whichever way the proton curves.",
  ["r = (1.6 × 10⁻²⁷ × 2.0 × 10⁶)/(1.6 × 10⁻¹⁹ × 0.50) = 0.040 m", "Chord = 2r sin 30° = r = 4.0 cm"],
  why="6.9 cm uses 2r cos 30°, measuring the angle from the normal instead of from the boundary. 8.0 cm (= 2r) is "
      "the result for entry perpendicular to the boundary. 2.0 cm is r sin 30°, half the chord.",
  ncert=MCM + "motion in a magnetic field", seconds=120, rc=True)

k_s, g_s, B_k, L_k = 10.0, 10.0, 0.40, 0.50
dF = 2 * k_s * 0.010
I_k = dF / (B_k * L_k)
close(I_k, 1.0)
close(k_s * 0.010 / (B_k * L_k), 0.5)
close(2 * k_s * 0.030 / (B_k * L_k), 3.0)
close(2 * k_s * 0.020 / (B_k * L_k), 2.0)
q(MAG, "Force on charges and conductors", "Advanced", "numerical",
  "A horizontal metal rod 0.50 m long hangs from two identical light vertical springs, each of spring constant "
  "10 N/m, attached at its ends, in a uniform horizontal magnetic field of 0.40 T perpendicular to the rod. With no "
  "current in the rod, each spring is stretched by 2.0 cm. When a current is passed through the rod, each spring is "
  "stretched by 3.0 cm. The current in the rod is:",
  *opt("1.0 A", ["0.50 A", "3.0 A", "2.0 A"], "D"),
  "Force on a conductor F = BIL, added to the weight; two springs share the load",
  "Without current the two springs together balance the weight: 2k × 0.020 m = 0.40 N. With the current, the "
  "magnetic force BIL acts downward and the extra extension of 1.0 cm in each spring supplies the extra force.",
  ["Extra spring force = 2 × 10 × 0.010 = 0.20 N", "BIL = 0.20 N → I = 0.20/(0.40 × 0.50) = 1.0 A",
   "(The current flows in the direction for which BIL points downwards.)"],
  why="0.50 A uses only one spring. 3.0 A equates BIL to the whole spring force at 3.0 cm, which also includes the "
      "weight. 2.0 A equates BIL to the weight of the rod.",
  ncert=MCM + "magnetic force on a current-carrying conductor", seconds=100, rc=True)

v_h, th_h = 2.0e6, rad(30)
r_h = mp_ * v_h * math.sin(th_h) / (qe_ * B_p)
T_h = 2 * math.pi * mp_ / (qe_ * B_p)
pitch_h = v_h * math.cos(th_h) * T_h
close(r_h, 0.020)
close(T_h, 4 * math.pi * 1e-8)
close(pitch_h, 0.2177, 1e-2)
close(v_h * math.sin(th_h) * T_h, 0.1257, 1e-2)
truth = {"a": True, "b": True, "c": False, "d": True, "e": True}
q(MAG, "Force on charges and conductors", "Advanced", "multi_statement",
  ms("A proton (mass 1.6 × 10⁻²⁷ kg, charge 1.6 × 10⁻¹⁹ C) enters a uniform magnetic field of 0.50 T with a speed "
     "of 2.0 × 10⁶ m/s, its velocity making an angle of 30° with the field. Which of the following statements are "
     "correct?",
     ["The radius of its helical path is 2.0 cm.",
      "It takes 4π × 10⁻⁸ s (about 1.26 × 10⁻⁷ s) to complete one turn of the helix.",
      "The pitch of the helix is about 12.6 cm.",
      "Its kinetic energy remains constant.",
      "The component of its velocity along the field stays equal to about 1.73 × 10⁶ m/s."]),
  *mso(truth, "abde", ["abcd", "bcde", "ade"], "B"),
  "Helical motion: r = mv sin θ/(qB), T = 2πm/(qB), pitch = v cos θ × T",
  "Resolve the velocity into v cos θ along B (unaffected by the field) and v sin θ perpendicular to B (circular "
  "motion). r = m v sin θ/(qB) = 2.0 cm (a true). T = 2πm/(qB) = 4π × 10⁻⁸ s (b true). The pitch is the distance "
  "moved along B in one period: v cos θ × T ≈ 21.8 cm, not 12.6 cm (c false). The magnetic force does no work, so "
  "the kinetic energy is constant (d true), and v cos 30° ≈ 1.73 × 10⁶ m/s stays constant (e true).",
  ["(a) r = (1.6 × 10⁻²⁷ × 1.0 × 10⁶)/(0.80 × 10⁻¹⁹) = 0.020 m → true",
   "(b) T = 2π(1.6 × 10⁻²⁷)/(0.80 × 10⁻¹⁹) = 4π × 10⁻⁸ s → true",
   "(c) p = 1.73 × 10⁶ × 1.26 × 10⁻⁷ ≈ 0.218 m → false (12.6 cm uses v sin θ)",
   "(d) true; (e) true"],
  why="Options with (c) use the perpendicular component v sin θ to find the pitch; the pitch depends on the "
      "component along the field. Options leaving out (b) or (e) miss correct statements.",
  ncert=MCM + "motion in a magnetic field (helical motion)", seconds=150, rc=True)

q(MAG, "Ampere's law", "Advanced", "assertion_reason",
  ar("At every point outside a long straight wire of circular cross-section, carrying a steady current spread "
     "uniformly over its cross-section, the magnetic field is the same as it would be if the whole current flowed "
     "along the axis of the wire.",
     "A circular Amperian loop of radius r larger than the radius of the wire, coaxial with it, encloses the whole "
     "current I, and by symmetry the field is tangential to the loop with the same magnitude all round it, so "
     "B = μ₀I/(2πr)."),
  AR, ar_key(True, True, True),
  "Ampere's circuital law applied to a cylindrically symmetric current",
  "For r outside the wire, ∮B·dl = B × 2πr and the enclosed current is the whole of I, so B = μ₀I/(2πr), exactly "
  "the field of a thin wire carrying I along the axis. The reason gives precisely this argument, so it explains the "
  "assertion.",
  ["Outside: B(2πr) = μ₀I → B = μ₀I/(2πr)", "Same as a line current on the axis → A true; R true and explains A"],
  why="Both statements are true and R is the derivation of A, so the options saying R does not explain A, or that "
      "either statement is false, are wrong.",
  ncert=MCM + "Ampere's circuital law (field of a long straight wire)", seconds=60)

k_ = 1e-7
Bmid = 2 * (2 * k_ * 1.0 / 0.10 ** 3)
close(Bmid, 4.0e-4)
close(2 * (2 * k_ * 1.0 / 0.20 ** 3), 5.0e-5)
q(MAG, "Magnetic dipole and bar magnet", "Advanced", "numerical",
  "Two identical short bar magnets, each of magnetic moment 1.0 A m², lie along the same straight line with their "
  "centres 20 cm apart. Both magnetic moments point in the same direction along the line (the north pole of one "
  "faces the south pole of the other). Taking μ₀/4π = 10⁻⁷ T m A⁻¹ and ignoring all other magnetic fields, the "
  "magnitude of the magnetic field at the point midway between their centres is:",
  *opt("4.0 × 10⁻⁴ T", ["2.0 × 10⁻⁴ T", "zero", "5.0 × 10⁻⁵ T"], "B"),
  "Axial field of a short magnet B = (μ₀/4π)(2m/r³), directed along m on both sides of the magnet",
  "The midpoint is on the axis of each magnet, 10 cm from each. On the axis of a short dipole the field points "
  "along its moment whichever side of the magnet the point lies, so both fields point the same way and add.",
  ["Each: B = 10⁻⁷ × 2 × 1.0/(0.10)³ = 2.0 × 10⁻⁴ T", "Both along the common direction of the moments",
   "Total = 4.0 × 10⁻⁴ T"],
  why="2.0 × 10⁻⁴ T counts only one magnet. 'Zero' assumes that fields on opposite sides of the point cancel, but "
      "on the axis each field points along its own moment. 5.0 × 10⁻⁵ T uses the 20 cm separation instead of the "
      "10 cm distance from each centre.",
  ncert=MMM + "the bar magnet (field on the axis of a magnetic dipole)", seconds=90, rc=True)

r0_, v0_ = 0.53e-10, 2.2e6
I_orb = qe_ * v0_ / (2 * math.pi * r0_)
B_n = MU0 * I_orb / (2 * r0_)
close(B_n, 12.5, 1e-2)
close(MU0 * I_orb / (2 * math.pi * r0_), 3.99, 1e-2)
close(MU0 * (qe_ * v0_ / r0_) / (2 * r0_), 78.7, 1e-2)
q(MAG, "Biot-Savart law", "Advanced", "numerical",
  "In the Bohr model of the hydrogen atom, the electron (charge 1.6 × 10⁻¹⁹ C) moves round the nucleus in a circle "
  "of radius 0.53 × 10⁻¹⁰ m with a speed of 2.2 × 10⁶ m/s. Treating the revolving electron as a circular current "
  "loop and taking μ₀ = 4π × 10⁻⁷ T m A⁻¹, the magnetic field it produces at the nucleus is about:",
  *opt("12.5 T", ["4.0 T", "79 T", "6.3 T"], "D"),
  "Equivalent current I = e/T = ev/(2πr); field at the centre of a loop B = μ₀I/(2r)",
  "The electron passes any point of its orbit once per period T = 2πr/v, so the equivalent current is "
  "I = ev/(2πr). The nucleus is at the centre of this current loop.",
  ["I = (1.6 × 10⁻¹⁹ × 2.2 × 10⁶)/(2π × 0.53 × 10⁻¹⁰) ≈ 1.06 × 10⁻³ A",
   "B = μ₀I/(2r) = (4π × 10⁻⁷ × 1.06 × 10⁻³)/(2 × 0.53 × 10⁻¹⁰)", "B ≈ 12.5 T"],
  why="4.0 T uses μ₀I/(2πr), the field of a long straight wire. 79 T takes the current as ev/r, leaving out the 2π "
      "in the period. 6.3 T uses μ₀I/(4r), half the field at the centre of a full loop.",
  ncert=MCM + "magnetic field on the axis of a circular current loop (field at the centre)", seconds=120, rc=True)

# ================================================================ Electromagnetic Induction and AC (B5 I6 A5)
EMIC = NC + "'Electromagnetic Induction', "
ACC = NC + "'Alternating Current', "

# ---- Basic
u_B = 0.20 ** 2 / (2 * MU0)
close(u_B, 1.59e4, 1e-2)
close(0.20 / (2 * MU0), 7.96e4, 1e-2)
close(MU0 * 0.20 ** 2 / 2, 2.5e-8, 1e-2)
q(EMI, "Self and mutual inductance", "Basic", "numerical",
  "In a region of space, the magnetic field has a magnitude of 0.20 T. Taking μ₀ = 4π × 10⁻⁷ T m A⁻¹, the magnetic "
  "energy stored per unit volume of this region is about:",
  *opt("1.6 × 10⁴ J m⁻³", ["3.2 × 10⁴ J m⁻³", "8.0 × 10⁴ J m⁻³", "2.5 × 10⁻⁸ J m⁻³"], "A"),
  "Magnetic energy density u_B = B²/(2μ₀)",
  "NCERT obtains the energy stored in a solenoid as (1/2)LI² and rewrites it as B²/(2μ₀) per unit volume, a result "
  "that holds for any region of magnetic field in vacuum.",
  ["u_B = B²/(2μ₀) = (0.20)²/(2 × 4π × 10⁻⁷)", "= 0.040/(2.51 × 10⁻⁶) ≈ 1.6 × 10⁴ J m⁻³"],
  why="3.2 × 10⁴ J m⁻³ leaves out the factor 1/2. 8.0 × 10⁴ J m⁻³ uses B instead of B². 2.5 × 10⁻⁸ J m⁻³ "
      "multiplies by μ₀ instead of dividing.",
  ncert=EMIC + "self-inductance (magnetic energy density B²/2μ₀)", seconds=40, rc=True)

Ps_ = 10 * 22
assert Ps_ / 220 == 1 and Ps_ / 11 == 20 and 22 / 220 == 0.1
q(EMI, "AC generator and transformer", "Basic", "numerical",
  "An ideal step-down transformer is connected to the 220 V AC mains. Its secondary supplies 11 V to ten identical "
  "lamps connected in parallel, each rated 11 V, 22 W, all glowing normally. The current drawn from the mains by "
  "the primary is:",
  *opt("1.0 A", ["20 A", "0.10 A", "400 A"], "B"),
  "Ideal transformer: input power = output power, V_p I_p = V_s I_s",
  "The ten lamps together take 10 × 22 = 220 W from the secondary. An ideal transformer has no losses, so the "
  "primary draws the same 220 W from the 220 V mains.",
  ["Output power = 10 × 22 W = 220 W", "I_p = 220 W/220 V = 1.0 A", "(Secondary current = 220/11 = 20 A)"],
  why="20 A is the secondary current. 0.10 A is the primary current for a single lamp. 400 A steps the current up "
      "by the turns ratio instead of down; in a step-down transformer the primary current is the smaller one.",
  ncert=ACC + "transformers", seconds=45, rc=True)

e_rod = 0.50 * 0.50 * 4.0 * math.sin(rad(30))
close(e_rod, 0.50)
close(0.50 * 0.50 * 4.0 * math.cos(rad(30)), 0.866, 1e-2)
q(EMI, "Faraday's and Lenz's laws", "Basic", "numerical",
  "A straight metal rod 0.50 m long moves in a plane perpendicular to a uniform magnetic field of 0.50 T. Its "
  "velocity, of magnitude 4.0 m/s, makes an angle of 30° with the length of the rod. The emf induced between the "
  "ends of the rod is:",
  *opt("0.50 V", ["0.87 V", "1.0 V", "0.25 V"], "C"),
  "Motional emf = B l v⊥, where v⊥ is the component of velocity perpendicular to the rod (and to B)",
  "Only the velocity component perpendicular to the rod sweeps out area (cuts field lines); motion along the rod's "
  "own length produces no emf. That component is v sin 30°.",
  ["v⊥ = 4.0 × sin 30° = 2.0 m/s", "ε = B l v⊥ = 0.50 × 0.50 × 2.0 = 0.50 V"],
  why="0.87 V uses the component along the rod (v cos 30°), which produces no emf. 1.0 V treats the motion as "
      "perpendicular to the rod. 0.25 V halves the correct value without reason.",
  ncert=EMIC + "motional electromotive force", seconds=45, rc=True)

q(EMI, "LCR resonance and power", "Basic", "statement_pair",
  sp("At resonance, the impedance of a series LCR circuit is equal to its resistance R.",
     "At resonance, the current in a series LCR circuit is in phase with the applied voltage."),
  SP, sp_key(True, True),
  "Series resonance: X_L = X_C",
  "At resonance X_L = X_C, so Z = √(R² + (X_L − X_C)²) = R (Statement I true) and tan φ = (X_C − X_L)/R = 0, so the "
  "current and the voltage are in phase (Statement II true).",
  ["Z = R at resonance → true", "φ = 0 at resonance → true"],
  why="Both follow from X_L = X_C, so no option with a false statement is right.",
  ncert=ACC + "series LCR circuit; resonance", seconds=30)

q(EMI, "AC: rms, reactance and impedance", "Basic", "direct",
  "An AC voltmeter connected across the household mains reads 220 V. This reading is the:",
  *opt("rms value of the alternating voltage",
       ["peak value of the alternating voltage", "average value of the voltage over a complete cycle",
        "peak-to-peak value of the alternating voltage"], "D"),
  "AC meters are calibrated to read rms values",
  "NCERT notes that AC ammeters and voltmeters measure rms values, and that the household line voltage of 220 V is "
  "an rms value; the peak value is √2 × 220 ≈ 311 V.",
  ["Meter reading = V_rms = 220 V", "Peak value = 311 V"],
  why="The peak value of the mains is about 311 V, not 220 V. The average of a sinusoidal voltage over a complete "
      "cycle is zero. The peak-to-peak value is about 622 V.",
  ncert=ACC + "AC voltage applied to a resistor (rms values)", seconds=25)

# ---- Intermediate
emf0 = 50 * 0.010 * 0.20 * 100 * math.pi
close(emf0, 31.4, 1e-2)
close(0.010 * 0.20 * 100 * math.pi, 0.628, 1e-2)
q(EMI, "Faraday's and Lenz's laws", "Intermediate", "numerical",
  "A coil of 50 turns, each of area 0.010 m², is held with its plane perpendicular to a magnetic field that varies "
  "with time as B = 0.20 sin(100πt) tesla, t being in seconds. The peak value of the emf induced in the coil is "
  "about:",
  *opt("31.4 V", ["0.10 V", "0.63 V", "10 V"], "C"),
  "Faraday's law ε = −N dΦ/dt with Φ = BA",
  "The flux through each turn is Φ = AB₀ sin ωt, so ε = −NAB₀ω cos ωt, whose peak value is NAB₀ω with "
  "ω = 100π rad/s.",
  ["ε₀ = NAB₀ω = 50 × 0.010 × 0.20 × 100π", "= 0.10 × 100π ≈ 31.4 V"],
  why="0.10 V is the peak flux linkage NAB₀ (in Wb), not an emf. 0.63 V leaves out the 50 turns. 10 V drops the "
      "factor π from ω = 100π.",
  ncert=EMIC + "Faraday's law of induction", seconds=50, rc=True)

I_pf = 1000 / (250 * 0.8)
R_pf = 1000 / I_pf ** 2
close(I_pf, 5.0)
close(R_pf, 40)
close(1000 / (1000 / 250) ** 2, 62.5)
close(1000 / (1000 / (250 * 0.64)) ** 2, 25.6)
q(EMI, "LCR resonance and power", "Intermediate", "numerical",
  "An AC circuit connected to a 250 V (rms) supply draws an average power of 1.0 kW at a power factor of 0.80. The "
  "rms current in the circuit and the resistance of the circuit are:",
  *opt("5.0 A and 40 Ω", ["4.0 A and 62.5 Ω", "5.0 A and 50 Ω", "6.25 A and 25.6 Ω"], "D"),
  "Average power P = V_rms I_rms cos φ; the power is dissipated only in the resistance, P = I²_rms R",
  "Use P = VI cos φ to find the current, then P = I²R for the resistance (only the resistance absorbs average "
  "power).",
  ["I = P/(V cos φ) = 1000/(250 × 0.80) = 5.0 A", "R = P/I² = 1000/25 = 40 Ω",
   "(Impedance Z = V/I = 50 Ω, and R/Z = 0.80 ✓)"],
  why="4.0 A and 62.5 Ω ignore the power factor. 5.0 A and 50 Ω give the impedance V/I instead of the resistance. "
      "6.25 A and 25.6 Ω divide by the power factor twice.",
  ncert=ACC + "power in AC circuit: the power factor", seconds=70, rc=True)

C_t = 1 / (4 * 10 * (1e6) ** 2 * 1e-3)
close(C_t, 25e-12)
close(1 / ((1e6) ** 2 * 1e-3), 1e-9)
close(1 / (4 * (1e6) ** 2 * 1e-3), 250e-12)
q(EMI, "LCR resonance and power", "Intermediate", "numerical",
  "A tuning circuit consists of a coil of inductance 1.0 mH in series with a variable capacitor. To make the circuit "
  "resonate at a frequency of 1.0 MHz, the capacitance must be set to (take π² = 10):",
  *opt("25 pF", ["1.0 nF", "159 pF", "250 pF"], "A"),
  "Resonant frequency f₀ = 1/(2π√(LC)), so C = 1/(4π²f₀²L)",
  "Square the resonance condition and solve for C.",
  ["C = 1/(4π² f₀² L)", "= 1/(4 × 10 × (10⁶)² × 10⁻³) = 1/(4 × 10¹⁰)", "= 2.5 × 10⁻¹¹ F = 25 pF"],
  why="1.0 nF leaves out the factor 4π². 159 pF uses 2π in place of 4π². 250 pF drops the π² (takes it as 1).",
  ncert=ACC + "series LCR circuit; resonance", seconds=60, rc=True)

L_core = 100 * MU0 * 200 ** 2 * 1.0e-4 / 0.20
close(L_core, 2.51e-3, 1e-2)
close(MU0 * 200 ** 2 * 1.0e-4 / 0.20, 2.51e-5, 1e-2)
close(100 * MU0 * 200 * 1.0e-4 / 0.20, 1.26e-5, 1e-2)
close(100 * MU0 * 200 ** 2 * 1.0e-4, 5.03e-4, 1e-2)
q(EMI, "Self and mutual inductance", "Intermediate", "numerical",
  "A long solenoid 20 cm long has 200 turns, each of cross-sectional area 1.0 cm². Its core is filled with a "
  "material of relative permeability 100 (take it as constant). Taking μ₀ = 4π × 10⁻⁷ T m A⁻¹, the self-inductance "
  "of the solenoid is about:",
  *opt("2.5 mH", ["25 μH", "13 μH", "0.50 mH"], "B"),
  "Self-inductance of a long solenoid with a core L = μᵣμ₀N²A/l",
  "The flux linkage per unit current of a long solenoid is μ₀n²Al = μ₀N²A/l in vacuum; a core of relative "
  "permeability μᵣ multiplies it by μᵣ.",
  ["L = μᵣμ₀N²A/l = 100 × 4π × 10⁻⁷ × (200)² × 1.0 × 10⁻⁴/0.20", "≈ 2.5 × 10⁻³ H = 2.5 mH"],
  why="25 μH leaves out the core (μᵣ = 1). 13 μH uses N instead of N². 0.50 mH forgets to divide by the length.",
  ncert=EMIC + "inductance (self-inductance of a long solenoid)", seconds=70, rc=True)

q(EMI, "LCR resonance and power", "Intermediate", "statement_pair",
  sp("When a series LCR circuit is driven at a frequency above its resonant frequency, the current leads the applied "
     "voltage.",
     "Above the resonant frequency, the capacitive reactance of a series LCR circuit is greater than its inductive "
     "reactance."),
  SP, sp_key(False, False),
  "X_L = ωL grows and X_C = 1/(ωC) falls as ω increases",
  "At resonance X_L = X_C. Above resonance ω is larger, so X_L > X_C (Statement II false). The circuit is then "
  "inductive and the current lags behind the voltage (Statement I false).",
  ["Above ω₀: X_L > X_C → II false", "Inductive circuit → current lags → I false"],
  why="Both statements describe the circuit below resonance, where X_C > X_L and the current leads; above "
      "resonance both are reversed.",
  ncert=ACC + "series LCR circuit (phasor diagram)", seconds=45)

q(EMI, "Faraday's and Lenz's laws", "Intermediate", "match_list",
  ml("The magnetic flux Φ linked with a closed coil varies with time t as given in List-I (a, b, Φ₀ and ω are "
     "positive constants). Match each case with the behaviour of the emf induced in the coil (List-II).",
     ["Φ = at", "Φ = bt²", "Φ = Φ₀ sin ωt", "Φ = Φ₀ (constant)"],
     ["Zero at all times", "Constant and non-zero", "Proportional to the time t",
      "Sinusoidal, with its largest magnitude at the instants when the flux is zero"]),
  *mlo("A-II, B-III, C-IV, D-I", ["A-III, B-II, C-IV, D-I", "A-II, B-III, C-I, D-IV", "A-II, B-IV, C-III, D-I"],
       "C"),
  "Faraday's law ε = −dΦ/dt",
  "Differentiate each flux. Φ = at gives ε = −a (constant). Φ = bt² gives ε = −2bt (proportional to t). "
  "Φ = Φ₀ sin ωt gives ε = −Φ₀ω cos ωt, largest when sin ωt = 0, i.e. when the flux is zero. A constant flux "
  "induces no emf.",
  ["A: dΦ/dt = a → II", "B: dΦ/dt = 2bt → III", "C: dΦ/dt = Φ₀ω cos ωt → IV", "D: dΦ/dt = 0 → I"],
  why="The other codes confuse the flux with the emf: the emf depends on the rate of change of flux, not on its "
      "value, so a uniformly rising flux gives a constant emf and a steady flux gives none.",
  ncert=EMIC + "Faraday's law of induction", seconds=60)

# ---- Advanced
p_inst = 200 * 5 * math.sin(rad(90)) * math.sin(rad(90 - 60))
p_avg = 0.5 * 200 * 5 * math.cos(rad(60))
close(p_inst, 500)
close(p_avg, 250)
q(EMI, "AC: rms, reactance and impedance", "Advanced", "numerical",
  "In an AC circuit the applied voltage and the current are v = 200 sin ωt volt and i = 5.0 sin(ωt − π/3) ampere. "
  "The instantaneous power supplied to the circuit at the instant when ωt = π/2, and the average power over a "
  "complete cycle, are respectively:",
  *opt("500 W and 250 W", ["500 W and 500 W", "1000 W and 250 W", "866 W and 250 W"], "D"),
  "Instantaneous power p = vi; average power P = V_rms I_rms cos φ = ½V₀I₀ cos φ",
  "At ωt = π/2 the voltage is at its peak, 200 V, and the current is 5.0 sin(π/2 − π/3) = 5.0 sin(π/6) = 2.5 A. The "
  "average power uses the phase difference φ = π/3.",
  ["p = 200 × 2.5 = 500 W", "P = ½ × 200 × 5.0 × cos(π/3) = 250 W"],
  why="'500 W and 500 W' forgets the power factor in the average. 1000 W multiplies the two peak values, but the "
      "current is not at its peak at that instant. 866 W uses cos(π/6) instead of sin(π/6) for the current.",
  ncert=ACC + "power in AC circuit: the power factor", seconds=90, rc=True)

Fc, Rr2, Bv, lv = 0.50, 2.0, 0.50, 0.50
v_term = Fc * Rr2 / (Bv * lv) ** 2
close(v_term, 16)
close(Fc * Rr2 / (Bv * lv), 4.0)
q(EMI, "Faraday's and Lenz's laws", "Advanced", "numerical",
  "A metal rod lies across two smooth, horizontal, parallel conducting rails 0.50 m apart, which are joined at one "
  "end through a 2.0 Ω resistor; the rod and rails have negligible resistance. A uniform vertical magnetic field of "
  "0.50 T acts on the region. A constant horizontal force of 0.50 N, along the rails, is applied to the rod, which "
  "starts from rest. The speed that the rod finally attains is:",
  *opt("16 m/s", ["4.0 m/s", "8.0 m/s", "32 m/s"], "A"),
  "Motional emf Blv, current Blv/R, opposing force B²l²v/R; terminal speed when the forces balance",
  "As the rod speeds up, the induced current I = Blv/R grows and so does the opposing magnetic force BIl = B²l²v/R "
  "(Lenz's law). The rod stops accelerating when this force equals the applied force.",
  ["B²l²v/R = F", "v = FR/(B²l²) = (0.50 × 2.0)/(0.50 × 0.50)²", "v = 1.0/0.0625 = 16 m/s"],
  why="4.0 m/s uses Bl instead of B²l². 8.0 m/s and 32 m/s bring in a spurious factor of 1/2 or 2 in the balance of "
      "forces; at the terminal speed the applied force simply equals B²l²v/R.",
  ncert=EMIC + "motional electromotive force; energy consideration", seconds=100, rc=True)

Z_ = math.hypot(40, 60 - 30)
I_z = 250 / Z_
V_RL = I_z * math.hypot(40, 60)
close(Z_, 50)
close(V_RL, 360.6, 1e-2)
q(EMI, "AC: rms, reactance and impedance", "Advanced", "numerical",
  "A 40 Ω resistor, an inductor of reactance 60 Ω and a capacitor of reactance 30 Ω are connected in series to a "
  "250 V (rms) AC supply. The rms voltage across the resistor and inductor taken together (between the free end of "
  "the resistor and the far end of the inductor, the two being adjacent) is about:",
  *opt("361 V", ["500 V", "300 V", "250 V"], "B"),
  "Impedance Z = √(R² + (X_L − X_C)²); voltage across R and L together = I√(R² + X_L²)",
  "First find the current from the total impedance. The voltages across R and L are 90° out of phase, so across the "
  "pair the voltage is I√(R² + X_L²). It can exceed the supply voltage because the capacitor's voltage is in "
  "opposition to the inductor's.",
  ["Z = √(40² + 30²) = 50 Ω, I = 250/50 = 5.0 A", "V_R = 200 V, V_L = 300 V",
   "V_RL = √(200² + 300²) = 5.0 × √(40² + 60²) ≈ 361 V"],
  why="500 V adds V_R and V_L as numbers, ignoring the 90° phase difference. 300 V is the inductor's voltage alone. "
      "250 V assumes no part of a series circuit can have a voltage larger than the supply.",
  ncert=ACC + "series LCR circuit (phasor diagram)", seconds=100, rc=True)

truth = {"a": True, "b": True, "c": True, "d": False, "e": True}
q(EMI, "Faraday's and Lenz's laws", "Advanced", "multi_statement",
  ms("The north pole of a bar magnet is pushed towards a closed coil of wire along the coil's axis. Which of the "
     "following statements are correct?",
     ["The current induced in the coil makes the coil repel the approaching magnet.",
      "The work done by the agent against this repulsion appears as electrical energy in the coil, which is "
      "dissipated as heat in its resistance.",
      "If the coil is cut so that the circuit is open, an emf is still induced but no current flows, and the magnet "
      "no longer experiences an opposing force.",
      "Pushing the magnet in faster, through the same distance, increases the total charge that flows round the "
      "coil.",
      "Pushing the magnet in faster, through the same distance, increases the induced emf."]),
  *mso(truth, "abce", ["abcd", "ace", "bcde"], "C"),
  "Lenz's law and conservation of energy; induced charge q = NΔΦ/R",
  "By Lenz's law the near face of the coil becomes a north pole and repels the magnet (a true). The work done "
  "against this force is converted into electrical energy and then into heat (b true). An open coil still has the "
  "emf dΦ/dt but no current, so there is no magnetic force on the magnet from it (c true). The emf depends on the "
  "rate of change of flux, so it is larger for a faster push (e true), but the total charge q = NΔΦ/R depends only "
  "on the total change of flux, which is the same (d false).",
  ["(a) Lenz's law → true", "(b) energy conservation → true", "(c) emf without current → true",
   "(d) q = NΔΦ/R, independent of speed → false", "(e) ε = N dΦ/dt larger for faster motion → true"],
  why="Options containing (d) confuse the emf, which grows with speed, with the total charge, which does not. "
      "Options leaving out (b) or (e) miss correct statements.",
  ncert=EMIC + "Lenz's law and conservation of energy", seconds=120)

q(EMI, "Faraday's and Lenz's laws", "Advanced", "assertion_reason",
  ar("A bar magnet is released from rest above a fixed horizontal coil and falls along the coil's axis, right "
     "through it. The coil is connected to a voltmeter of very high resistance. The peak emf induced as the magnet "
     "leaves the coil is larger in magnitude than the peak emf induced as it enters.",
     "The magnet is moving faster as it leaves the coil, so the magnetic flux through the coil changes more "
     "rapidly then."),
  AR, ar_key(True, True, True),
  "Faraday's law: emf = rate of change of flux linkage",
  "The voltmeter draws almost no current, so there is practically no magnetic braking and the magnet keeps "
  "accelerating under gravity. As it leaves the coil it is faster than when it entered, the flux falls more quickly "
  "than it rose, and the peak emf is larger (and of opposite sign). The greater rate of change of flux is the direct "
  "cause.",
  ["A: true (larger, opposite-sign peak on leaving)", "R: true, and ε ∝ dΦ/dt makes it the reason"],
  why="Both statements are true and the faster change of flux is exactly why the exit peak is larger, so the other "
      "options are wrong.",
  ncert=EMIC + "Faraday's law of induction; Lenz's law", seconds=60)

# ================================================================ Electromagnetic Waves (B2 I2 A2)
EMWC = NC + "'Electromagnetic Waves', "
C0 = 3.0e8

q(EMW, "EM wave properties", "Basic", "assertion_reason",
  ar("Electromagnetic waves can travel through vacuum.",
     "Like sound waves, electromagnetic waves are vibrations of the particles of a material medium."),
  AR, ar_key(True, False),
  "Nature of electromagnetic waves",
  "In an electromagnetic wave the oscillating quantities are the electric and magnetic fields themselves, which "
  "sustain each other; no material medium is involved, so the waves travel through vacuum (A true). Sound, by "
  "contrast, needs a material medium; R wrongly describes electromagnetic waves as vibrations of particles (R "
  "false).",
  ["A: true (light reaches us from the Sun through space)", "R: false (oscillating E and B fields, no medium)"],
  why="Since R is false, it can neither be true nor explain A.",
  ncert=EMWC + "electromagnetic waves (nature of electromagnetic waves)", seconds=30)

U_p = 6.0
p_ref = 2 * U_p / C0
close(p_ref, 4.0e-8)
close(U_p / C0, 2.0e-8)
q(EMW, "EM wave properties", "Basic", "numerical",
  "A pulse of light carrying 6.0 J of energy falls normally on a perfectly reflecting mirror and is reflected back "
  "along its path. Taking c = 3.0 × 10⁸ m/s, the momentum delivered to the mirror is:",
  *opt("4.0 × 10⁻⁸ kg m/s", ["2.0 × 10⁻⁸ kg m/s", "1.8 × 10⁹ kg m/s", "zero"], "B"),
  "Electromagnetic waves carry momentum; light of energy U has momentum U/c",
  "The incident pulse carries momentum U/c towards the mirror. After reflection it carries U/c away from the "
  "mirror, so the change in the light's momentum, and hence the momentum given to the mirror, is 2U/c.",
  ["Momentum of the pulse = U/c = 6.0/(3.0 × 10⁸) = 2.0 × 10⁻⁸ kg m/s",
   "Reflection reverses it: Δp = 2U/c = 4.0 × 10⁻⁸ kg m/s"],
  why="2.0 × 10⁻⁸ kg m/s is the value for a perfectly absorbing surface. 1.8 × 10⁹ multiplies by c instead of "
      "dividing. 'Zero' forgets that reversing the light's momentum needs a push from the mirror.",
  ncert=EMWC + "electromagnetic waves (momentum and radiation pressure)", seconds=40, rc=True)

f_lc = 1 / (2 * math.pi * math.sqrt(1.0e-6 * 1.0e-12))
lam_lc = C0 / f_lc
close(lam_lc, 1.885, 1e-2)
close(C0 / (1 / math.sqrt(1e-18)), 0.30)
close(2 * math.pi * lam_lc, 11.8, 1e-2)
q(EMW, "EM spectrum and uses", "Intermediate", "numerical",
  "An oscillating LC circuit with L = 1.0 μH and C = 1.0 pF radiates electromagnetic waves at its natural "
  "frequency. Taking c = 3.0 × 10⁸ m/s, the wavelength of the radiation and the part of the spectrum to which it "
  "belongs are:",
  *opt("about 1.9 m; radio waves", ["about 0.30 m; microwaves", "about 1.9 mm; microwaves",
                                     "about 12 m; radio waves"], "A"),
  "An oscillating charge radiates at its own frequency; f = 1/(2π√(LC)); λ = c/f",
  "NCERT explains that an oscillating charge (as in an LC circuit used by Hertz) produces electromagnetic waves "
  "of the same frequency. Here f = 1/(2π√(LC)) and λ = c/f. Wavelengths longer than 0.1 m are radio waves.",
  ["√(LC) = √(10⁻⁶ × 10⁻¹²) = 10⁻⁹ s", "f = 1/(2π × 10⁻⁹) ≈ 1.59 × 10⁸ Hz",
   "λ = 3.0 × 10⁸/1.59 × 10⁸ ≈ 1.9 m → radio waves (λ > 0.1 m)"],
  why="0.30 m leaves out the 2π (and 0.30 m would still be a radio wavelength). 1.9 mm is a slip of 10³ in the "
      "wavelength. 12 m multiplies the correct wavelength by 2π.",
  ncert=EMWC + "electromagnetic waves (sources); electromagnetic spectrum", seconds=70, rc=True)

close(1 / math.sqrt(MU0 * 8.854e-12), 3.0e8, 1e-2)
q(EMW, "EM wave properties", "Intermediate", "match_list",
  ml("Match each quantity in List-I with its expression in List-II. (μ₀, ε₀ = permeability and permittivity of free "
     "space; μ, ε = those of a material medium; U = energy of light falling normally on a surface; Φ_E = electric "
     "flux.)",
     ["Speed of electromagnetic waves in vacuum", "Speed of electromagnetic waves in a material medium",
      "Momentum delivered to a perfectly reflecting surface by light of energy U",
      "Displacement current through a surface"],
     ["ε₀ dΦ_E/dt", "2U/c", "1/√(μ₀ε₀)", "1/√(με)"]),
  *mlo("A-III, B-IV, C-II, D-I", ["A-IV, B-III, C-II, D-I", "A-III, B-IV, C-I, D-II", "A-III, B-II, C-IV, D-I"],
       "D"),
  "Maxwell's results for electromagnetic waves; momentum of light; displacement current",
  "Maxwell's equations give the speed of electromagnetic waves as 1/√(μ₀ε₀) in vacuum (= c) and 1/√(με) in a "
  "medium. Light of energy U carries momentum U/c; on perfect reflection its momentum is reversed, so the surface "
  "receives 2U/c. Maxwell's displacement current is i_d = ε₀ dΦ_E/dt.",
  ["A → III", "B → IV", "C → II", "D → I"],
  why="The other codes exchange the vacuum and medium speeds, or the momentum and displacement-current "
      "expressions, or give the reflecting surface the absorbed-light value instead of 2U/c.",
  ncert=EMWC + "displacement current; electromagnetic waves (speed, momentum)", seconds=50)

q(EMW, "EM wave properties", "Advanced", "statement_pair",
  sp("When an electromagnetic wave passes from vacuum into a non-magnetic medium of relative permittivity 4, its "
     "wavelength in the medium is half its wavelength in vacuum.",
     "In that medium, the frequency of the wave is half its frequency in vacuum."),
  SP, sp_key(True, False),
  "Speed in a medium v = 1/√(με) = c/√(μᵣεᵣ); frequency is fixed by the source",
  "With μᵣ = 1 and εᵣ = 4, v = c/2. The frequency does not change on entering the medium, so λ = v/f becomes half "
  "of its vacuum value (Statement I true, Statement II false).",
  ["v = c/√4 = c/2", "f unchanged → λ halves → I true", "II says f halves → false"],
  why="It is the wavelength (and the speed) that changes in a medium; the frequency is set by the source.",
  ncert=EMWC + "electromagnetic waves (speed in a material medium)", seconds=45)

q(EMW, "EM wave properties", "Advanced", "direct",
  "A plane electromagnetic wave travels through vacuum in the −x direction. At a certain point and instant its "
  "magnetic field is along the +z direction. The electric field at that point and instant is along:",
  *opt("the −y direction", ["the +y direction", "the +x direction", "the −z direction"], "B"),
  "In a plane electromagnetic wave E, B and the direction of propagation form a right-handed set: E × B is along "
  "the direction of travel",
  "E must be perpendicular to both B (z) and the direction of travel (x), so it is along ±y. E × B must point along "
  "−x: (−ŷ) × ẑ = −x̂, while (+ŷ) × ẑ = +x̂.",
  ["E ⟂ x and E ⟂ z → E along ±y", "(−ŷ) × ẑ = −x̂ ✓ → E along −y"],
  why="+y gives E × B along +x, the wrong direction of travel. E cannot be along x (the direction of propagation) "
      "or along z (parallel or antiparallel to B), because the wave is transverse with E ⟂ B.",
  ncert=EMWC + "electromagnetic waves (transverse nature)", seconds=50)

# ================================================================ Optics (B7 I9 A7)
ROC = NC + "'Ray Optics and Optical Instruments', "
WOC = NC + "'Wave Optics', "


def lens_v(u, f):
    """Thin lens / Cartesian convention: 1/v − 1/u = 1/f."""
    return 1 / (1 / f + 1 / u)


def mirror_v(u, f):
    """Spherical mirror, Cartesian convention: 1/v + 1/u = 1/f."""
    return 1 / (1 / f - 1 / u)


# ---- Basic
r_wg = deg(math.asin((4 / 3) * 0.5 / 1.5))
close(r_wg, 26.4, 2e-3)
close(deg(math.asin(1.5 * 0.5 / (4 / 3))), 34.2, 2e-3)
close(deg(math.asin(0.5 / 1.5)), 19.5, 2e-3)
close(deg(math.asin(0.5 / (4 / 3))), 22.0, 2e-3)
q(OPT, "Refraction and lenses", "Basic", "numerical",
  "A ray of light travelling in water (refractive index 4/3) falls on the plane surface of a glass block "
  "(refractive index 1.5) immersed in the water, at an angle of incidence of 30°. The angle of refraction in the "
  "glass is about:",
  *opt("26.4°", ["34.2°", "19.5°", "22.0°"], "A"),
  "Snell's law n₁ sin i = n₂ sin r",
  "Use the refractive indices of the two media actually involved, water and glass.",
  ["(4/3) sin 30° = 1.5 sin r", "sin r = (4/3 × 0.5)/1.5 = 0.444", "r ≈ 26.4°"],
  why="34.2° puts the indices the wrong way round (the ray would then bend away from the normal entering a denser "
      "medium). 19.5° uses the refractive index of glass with respect to air, as if the ray came from air. 22.0° "
      "ignores the glass and treats it as refraction from air into water.",
  ncert=ROC + "refraction (Snell's law)", seconds=50, rc=True)

assert 10 * F(25, 5) == 50 and 10 * (1 + F(25, 5)) == 60
q(OPT, "Optical instruments", "Basic", "numerical",
  "In a compound microscope, the objective forms a real image 10 times as large as the object. The eyepiece has a "
  "focal length of 5.0 cm and the final image is formed at infinity. Taking the least distance of distinct vision "
  "as 25 cm, the magnifying power of the microscope is:",
  *opt("50", ["15", "60", "2"], "B"),
  "Magnifying power of a compound microscope m = m_o × m_e; eyepiece (image at infinity) m_e = D/f_e",
  "The eyepiece acts as a simple microscope viewing the objective's image; with the final image at infinity its "
  "angular magnification is D/f_e. The total magnifying power is the product of the two magnifications.",
  ["m_e = 25/5.0 = 5", "m = 10 × 5 = 50"],
  why="15 adds the magnifications instead of multiplying. 60 uses 1 + D/f_e, which applies when the final image is "
      "at the near point, not at infinity. 2 divides the objective's magnification by the focal length.",
  ncert=ROC + "optical instruments (compound microscope)", seconds=35, rc=True)

assert 2 * (20 + 5) == 50
q(OPT, "Mirrors", "Basic", "numerical",
  "An object stands 20 cm in front of a plane mirror. Keeping the object fixed, the mirror is moved 5.0 cm farther "
  "away from it, parallel to itself. The distance between the object and its image is now:",
  *opt("50 cm", ["45 cm", "30 cm", "40 cm"], "C"),
  "A plane mirror forms the image as far behind it as the object is in front",
  "After the move the object is 25 cm from the mirror, so the image is 25 cm behind it.",
  ["Object-mirror distance = 20 + 5.0 = 25 cm", "Object-image distance = 2 × 25 = 50 cm"],
  why="45 cm moves the image by only 5 cm; when the mirror moves 5 cm, the image moves 10 cm. 30 cm adds 10 cm to "
      "the object-mirror distance instead of to the object-image distance. 40 cm is the original separation.",
  ncert=ROC + "reflection of light by spherical mirrors (plane mirror as f → ∞)", seconds=30, rc=True)

q(OPT, "Huygens' principle and interference", "Basic", "direct",
  "A ray of light passing from air into water bends towards the normal, and measurements show that light travels "
  "more slowly in water than in air. Taken together, these two observations:",
  *opt("supported the wave picture of light, which predicts a smaller speed of light in the medium towards whose "
       "normal the ray bends on refraction",
       ["supported the corpuscular picture of light, which predicts a smaller speed of light in an optically "
        "denser medium",
        "showed that light travels with the same speed in all media",
        "showed that light waves are transverse"], "D"),
  "Wave and corpuscular explanations of refraction",
  "When light passes from air into water it bends towards the normal. Huygens' wave theory explains this only if "
  "the speed of light in water is less than in air (sin i/sin r = v₁/v₂). The corpuscular model explained the same "
  "bending by assuming a greater speed in the denser medium. The measured smaller speed in water "
  "therefore agrees with the wave picture and contradicts the corpuscular one.",
  ["Bending towards the normal: wave theory needs v₂ < v₁; corpuscular theory needs v₂ > v₁",
   "Measured v_water < v_air → wave theory supported"],
  why="The corpuscular model predicted a larger, not smaller, speed in the denser medium. The speed of light "
      "differs from medium to medium. Transverse nature is shown by polarisation, not by speed measurements.",
  ncert=WOC + "introduction; refraction of a plane wave", seconds=40)

q(OPT, "Refraction and lenses", "Basic", "statement_pair",
  sp("For two media 1 and 2, the refractive index of medium 1 with respect to medium 2 and that of medium 2 with "
     "respect to medium 1 satisfy n₁₂ × n₂₁ = 1.",
     "For three media 1, 2 and 3, n₃₂ = n₃₁ × n₂₁."),
  SP, sp_key(True, False),
  "Relative refractive index n₂₁ = n₂/n₁ = v₁/v₂",
  "n₁₂ = n₁/n₂ and n₂₁ = n₂/n₁, so their product is 1 (Statement I true). NCERT gives n₃₂ = n₃₁ × n₁₂: indeed "
  "n₃₁ × n₁₂ = (n₃/n₁)(n₁/n₂) = n₃/n₂. The product n₃₁ × n₂₁ = n₃n₂/n₁² is not n₃₂ (Statement II false).",
  ["I: (n₁/n₂)(n₂/n₁) = 1 → true", "II: n₃₂ = n₃₁ × n₁₂, not n₃₁ × n₂₁ → false"],
  why="Statement II uses n₂₁ where n₁₂ is needed; the two are reciprocals, so II is false and I is true.",
  ncert=ROC + "refraction", seconds=40)

q(OPT, "Total internal reflection", "Basic", "assertion_reason",
  ar("Total internal reflection cannot take place when light travels from water into glass.",
     "Glass is optically denser than water (it has a larger refractive index)."),
  AR, ar_key(True, True, True),
  "Conditions for total internal reflection",
  "Total internal reflection is possible only when light goes from an optically denser medium towards an optically "
  "rarer one (and the angle of incidence exceeds the critical angle). Going from water into glass, the light enters "
  "a denser medium and bends towards the normal, so there is no critical angle and total internal reflection cannot "
  "occur. R states exactly why.",
  ["A: true", "R: true (n_glass ≈ 1.5 > n_water ≈ 1.33)", "Denser → rarer is required; here it is rarer → denser → "
   "R explains A"],
  why="Both are true and the greater optical density of glass is precisely the reason, so the other options are "
      "wrong.",
  ncert=ROC + "total internal reflection", seconds=30)

f_o7, f_e7 = 1 / 0.5, 1 / 20
close(f_o7 / f_e7, 40)
q(OPT, "Optical instruments", "Basic", "numerical",
  "The objective of an astronomical telescope has a power of 0.50 D and its eyepiece has a power of 20 D. In normal "
  "adjustment (final image at infinity), the magnifying power of the telescope is:",
  *opt("40", ["1/40", "10", "205"], "D"),
  "Telescope in normal adjustment m = f_o/f_e; f = 1/P (f in metres)",
  "Convert powers to focal lengths: f_o = 1/0.50 = 2.0 m and f_e = 1/20 = 0.05 m. The magnifying power in normal "
  "adjustment is f_o/f_e, which equals P_e/P_o.",
  ["f_o = 200 cm, f_e = 5 cm", "m = 200/5 = 40 (= P_e/P_o = 20/0.50)"],
  why="1/40 inverts the ratio (P_o/P_e). 10 multiplies the two powers. 205 is the length of the telescope in "
      "centimetres (f_o + f_e), not its magnifying power.",
  ncert=ROC + "optical instruments (telescope); power of a lens", seconds=35, rc=True)

# ---- Intermediate
u8, v8 = 1.0, 4.0
f8 = 1 / (1 / u8 + 1 / v8)
close(f8, 0.80)
close(1 / (1 / 0.6 + 1 / 2.4), 0.48)
close(1 / (1 / u8 - 1 / v8), 1.333, 1e-2)
close(-mirror_v(-1.0, -0.8), 4.0)
q(OPT, "Mirrors", "Intermediate", "numerical",
  "A concave mirror forms, on a screen, a real image of a small lamp four times as large as the lamp. The screen is "
  "3.0 m from the lamp, and both lie on the principal axis in front of the mirror. The focal length of the mirror "
  "is:",
  *opt("0.80 m", ["1.6 m", "0.48 m", "1.33 m"], "B"),
  "Mirror equation 1/v + 1/u = 1/f with |v| = 4|u| and the screen beyond the lamp",
  "A real image four times the size lies four times as far from the mirror as the lamp. Both are in front of the "
  "mirror, so the lamp-screen separation is |v| − |u| = 3|u| = 3.0 m.",
  ["|u| = 1.0 m, |v| = 4.0 m", "1/f = 1/1.0 + 1/4.0 = 1.25 m⁻¹ (magnitudes, real image)", "f = 0.80 m"],
  why="1.6 m is the radius of curvature. 0.48 m takes |u| + |v| = 3.0 m, as if the lamp and screen were on "
      "opposite sides of the mirror. 1.33 m subtracts 1/v from 1/u, a sign slip in the mirror equation.",
  ncert=ROC + "reflection of light by spherical mirrors (mirror equation, magnification)", seconds=80, rc=True)

f9 = math.sqrt(5 * 80)
close(f9, 20)
close(lens_v(-(f9 + 5), f9), f9 + 80)
close(1 / (1 / 5 + 1 / 80), 4.7, 1e-2)
q(OPT, "Refraction and lenses", "Intermediate", "numerical",
  "A thin convex lens forms a real image of an object placed 5.0 cm beyond its first principal focus. The image is "
  "formed 80 cm beyond the second principal focus, on the other side of the lens. The focal length of the lens "
  "is:",
  *opt("20 cm", ["42.5 cm", "4.7 cm", "10 cm"], "C"),
  "Thin lens formula 1/v − 1/u = 1/f with distances measured from the lens",
  "Let the focal length be f. The object is at u = −(f + 5) cm and the image at v = +(f + 80) cm. Substitute in the "
  "lens formula and solve for f.",
  ["1/(f + 80) + 1/(f + 5) = 1/f", "f(2f + 85) = (f + 80)(f + 5) → 2f² + 85f = f² + 85f + 400",
   "f² = 400 → f = 20 cm (check: u = −25 cm gives v = +100 cm = f + 80 ✓)"],
  shortcut="Distances measured from the foci satisfy x₁x₂ = f²: f = √(5 × 80) = 20 cm.",
  why="42.5 cm averages the two given distances. 4.7 cm puts 5 cm and 80 cm into the lens formula as if they were "
      "measured from the lens. 10 cm is half the correct value.",
  ncert=ROC + "refraction by a lens (thin lens formula)", seconds=100, rc=True)

C_gw = deg(math.asin((4 / 3) / 1.5))
close(C_gw, 62.7, 2e-3)
assert C_gw > 45 > deg(math.asin(1 / 1.5))
q(OPT, "Total internal reflection", "Intermediate", "direct",
  "A right-angled isosceles glass prism (angles 90°, 45°, 45°; refractive index 1.5) turns a beam through 90° in air "
  "by total internal reflection at its hypotenuse face, the beam entering normally through one of the shorter "
  "faces. The prism is now placed in water (refractive index 4/3) and used in the same way. At the hypotenuse "
  "face, the beam:",
  *opt("is mainly refracted out into the water, because the critical angle for glass-water (about 63°) is more than "
       "45°",
       ["is still totally reflected, because 45° exceeds the critical angle of glass (about 42°)",
        "is still totally reflected, because total internal reflection does not depend on the surrounding medium",
        "passes into the water without any change of direction"], "A"),
  "Critical angle depends on both media: sin C = n_rarer/n_denser",
  "The beam meets the hypotenuse at 45°. For glass to air, sin C = 1/1.5 and C ≈ 42°, so 45° > C and the beam is "
  "totally reflected. For glass to water, sin C = (4/3)/1.5 = 0.889 and C ≈ 63°. Now 45° < C, so there is no total "
  "internal reflection; most of the light is refracted into the water (a little is reflected).",
  ["Glass-air: C ≈ 41.8° < 45° → TIR in air", "Glass-water: sin C = 0.889, C ≈ 62.7° > 45° → no TIR"],
  why="The 42° critical angle applies only to glass-air. The critical angle depends on the second medium too. At "
      "45° incidence the ray is not along the normal, so it is deviated on refraction.",
  ncert=ROC + "total internal reflection (prisms)", seconds=60)

hi = 1.0 * 100 / 10000
close(hi, 0.010)
close(0.05 * 100 / 10000, 5e-4)
q(OPT, "Optical instruments", "Intermediate", "numerical",
  "An astronomical telescope has an objective of focal length 100 cm and an eyepiece of focal length 5.0 cm. It is "
  "used to view a tower 100 m tall standing 10 km away. The height of the image of the tower formed by the "
  "objective is:",
  *opt("1.0 cm", ["0.050 cm", "20 cm", "0.10 cm"], "D"),
  "A distant object subtending angle α forms an image of height f_o × α in the focal plane of the objective",
  "The tower subtends a small angle α = 100 m/10 000 m = 0.010 rad at the objective. Its image is formed at the "
  "focal plane of the objective with height f_o α. The eyepiece plays no part in forming this image.",
  ["α = 100/10 000 = 0.010 rad", "h = f_o α = 100 cm × 0.010 = 1.0 cm"],
  why="0.050 cm uses the eyepiece focal length. 20 cm multiplies by the magnifying power f_o/f_e, but that applies "
      "to the angle subtended by the final image, not to the size of the objective's image. 0.10 cm slips a "
      "factor of 10 in converting 10 km.",
  ncert=ROC + "optical instruments (telescope)", seconds=60, rc=True)

P_air, P_wat = (1.5 - 1), (1.5 / (4 / 3) - 1)
assert P_wat < P_air
q(OPT, "Refraction and lenses", "Intermediate", "statement_pair",
  sp("A thin convex lens of glass (refractive index 1.5) has a smaller power when it is immersed in water "
     "(refractive index 4/3) than when it is in air.",
     "A small spherical air bubble inside water behaves as a diverging lens."),
  SP, sp_key(True, True),
  "Lens maker's formula with relative refractive index: 1/f = (n_rel − 1)(1/R₁ − 1/R₂)",
  "In air n_rel − 1 = 0.5; in water n_rel − 1 = 1.5/(4/3) − 1 = 0.125, so the power falls to a quarter (Statement "
  "I true). An air bubble is a 'biconvex lens' of a medium (air) rarer than its surroundings, so n_rel < 1 and its "
  "focal length is negative: it diverges light (Statement II true).",
  ["I: (n_rel − 1) falls from 0.5 to 0.125 → true", "II: convex shape with n_rel = 3/4 < 1 → diverging → true"],
  why="Both statements follow from the lens maker's formula with the refractive index taken relative to the "
      "surrounding medium.",
  ncert=ROC + "refraction by a lens (lens maker's formula)", seconds=45)

q(OPT, "Mirrors", "Intermediate", "assertion_reason",
  ar("A convex mirror can form a real image of a real object if the object is placed close enough to the mirror.",
     "In the Cartesian sign convention, the focal length of a convex mirror is positive."),
  AR, ar_key(False, True),
  "Images formed by a convex mirror",
  "For a real object (u negative) and a convex mirror (f positive), 1/v = 1/f − 1/u is always positive, so v is "
  "positive: the image is always virtual, erect, diminished and behind the mirror, wherever the object is. A is "
  "false. R is true: the focus of a convex mirror lies behind it, on the side opposite to the incident light.",
  ["A: 1/v = 1/f + 1/|u| > 0 → always virtual → false", "R: f measured behind the mirror → positive → true"],
  why="A is false for every object position, so the options that take A as true are wrong.",
  ncert=ROC + "reflection of light by spherical mirrors (sign convention; mirror equation)", seconds=45)

for th_, frac_ in ((60, F(1, 8)), (45, F(1, 4)), (30, F(3, 8))):
    close(0.5 * math.cos(rad(th_)) ** 2, float(frac_))
q(OPT, "Polarisation", "Intermediate", "match_list",
  ml("Unpolarised light of intensity I₀ falls on the arrangement of ideal polaroids described in List-I. Match each "
     "arrangement with the intensity of the light that finally emerges (List-II).",
     ["A single polaroid", "Two polaroids with their pass axes at 60° to each other",
      "Two polaroids with their pass axes at 45° to each other", "Two polaroids with their pass axes at 30° to each other"],
     ["I₀/4", "3I₀/8", "I₀/2", "I₀/8"]),
  *mlo("A-III, B-IV, C-I, D-II", ["A-III, B-II, C-I, D-IV", "A-I, B-IV, C-III, D-II", "A-III, B-IV, C-II, D-I"],
       "B"),
  "First polaroid halves unpolarised light; Malus's law I = I₁ cos² θ for the second",
  "Any single ideal polaroid transmits half the intensity of unpolarised light, whatever its orientation. The light "
  "leaving it is plane polarised, and a second polaroid at angle θ transmits the fraction cos² θ of it.",
  ["A: I₀/2", "B: (I₀/2) cos² 60° = I₀/8", "C: (I₀/2) cos² 45° = I₀/4", "D: (I₀/2) cos² 30° = 3I₀/8"],
  why="The other codes exchange the 60° and 30° cases (cos² 60° = 1/4 while cos² 30° = 3/4), or treat a single "
      "polaroid as passing a quarter of the light.",
  ncert=WOC + "polarisation (Malus's law)", seconds=60)

v_a = mirror_v(-18, -12)
v_c = mirror_v(-8, -12)
close(v_a, -36)
close(-v_a / -18, -2)
close(v_c, 24)
close(-v_c / -8, 3)
truth = {"a": True, "b": True, "c": True, "d": False, "e": False}
q(OPT, "Mirrors", "Intermediate", "multi_statement",
  ms("A small object is placed on the principal axis of a concave mirror of focal length 12 cm. Which of the "
     "following statements are correct?",
     ["With the object 18 cm from the mirror, the image is formed 36 cm in front of the mirror.",
      "With the object 18 cm from the mirror, the magnification is −2.",
      "With the object 8.0 cm from the mirror, the image is formed 24 cm behind the mirror.",
      "With the object 8.0 cm from the mirror, the image is smaller than the object.",
      "With the object 18 cm from the mirror, the image is virtual."]),
  *mso(truth, "abc", ["abce", "acd", "bcd"], "C"),
  "Mirror equation 1/v + 1/u = 1/f (Cartesian convention, f = −12 cm), m = −v/u",
  "Object at 18 cm (u = −18): 1/v = −1/12 + 1/18 = −1/36, so v = −36 cm, a real image in front of the mirror (a "
  "true, e false), with m = −v/u = −2 (b true). Object at 8.0 cm, between F and the pole (u = −8): "
  "1/v = −1/12 + 1/8 = 1/24, so v = +24 cm behind the mirror (c true) and m = −24/(−8) = +3, an enlarged virtual "
  "image (d false).",
  ["(a) v = −36 cm → true", "(b) m = −2 → true", "(c) v = +24 cm → true", "(d) m = +3 (enlarged) → false",
   "(e) v negative → real → false"],
  why="Options with (d) forget that an object between F and P gives an enlarged virtual image; options with (e) "
      "call the real image at 36 cm virtual.",
  ncert=ROC + "reflection of light by spherical mirrors", seconds=120, rc=True)

f16 = 30 * (1.5 - 1) / (1.6 - 1)
close(f16, 25)
close(30 * 1.5 / 1.6, 28.1, 1e-2)
close(30 * 1.6 / 1.5, 32)
q(OPT, "Refraction and lenses", "Intermediate", "numerical",
  "A thin equiconvex lens made of glass of refractive index 1.5 has a focal length of 30 cm in air. A lens of "
  "exactly the same shape is made from glass of refractive index 1.6. Its focal length in air is:",
  *opt("25 cm", ["36 cm", "28.1 cm", "32 cm"], "D"),
  "Lens maker's formula 1/f = (n − 1)(1/R₁ − 1/R₂): for the same surfaces f ∝ 1/(n − 1)",
  "The radii of curvature are the same, so only the factor (n − 1) changes, from 0.5 to 0.6.",
  ["f₂/f₁ = (n₁ − 1)/(n₂ − 1) = 0.5/0.6", "f₂ = 30 × 0.5/0.6 = 25 cm"],
  why="36 cm inverts the ratio of (n − 1) values. 28.1 cm and 32 cm scale the focal length by n instead of by "
      "(n − 1).",
  ncert=ROC + "refraction by a lens (lens maker's formula)", seconds=45, rc=True)

# ---- Advanced
pd = 5 * 600
assert pd / 5.5 == 3000 / 5.5 and abs(pd / 5.5 - 545.45) < 0.01
for lam_ in (500, 600, 3000 / 7):
    assert abs(pd / lam_ - round(pd / lam_)) < 1e-9          # these give bright fringes at P
q(OPT, "Huygens' principle and interference", "Advanced", "numerical",
  "In a Young's double-slit experiment with light of wavelength 600 nm, a point P on the screen is at the centre of "
  "the fifth bright fringe from the central bright fringe. Keeping everything else unchanged, the light is replaced "
  "by light of another wavelength. For which of the following wavelengths will P lie at the centre of a dark "
  "fringe?",
  *opt("about 545 nm", ["500 nm", "600 nm", "about 429 nm"], "B"),
  "Path difference fixed by the geometry: bright when Δ = nλ, dark when Δ = (n + ½)λ",
  "The path difference at P depends only on the positions of the slits and of P: Δ = 5 × 600 nm = 3000 nm. P is "
  "dark for a new wavelength λ if 3000 nm = (n + ½)λ for some whole number n.",
  ["Δ = 5 × 600 = 3000 nm", "Dark: λ = 3000/(n + ½); n = 5 gives λ ≈ 545 nm",
   "500 nm (Δ = 6λ), 600 nm (Δ = 5λ) and 3000/7 ≈ 429 nm (Δ = 7λ) all give bright fringes at P"],
  why="500 nm and about 429 nm make the path difference a whole number of wavelengths (6λ and 7λ), so P stays "
      "bright, as it does for 600 nm itself (5λ).",
  ncert=WOC + "interference of light waves and Young's experiment", seconds=120, rc=True)

n_min = int(2.5e-6 / 600e-9)
assert n_min == 4 and 2 * n_min == 8 and int(2 * 2.5e-6 / 600e-9) == 8
q(OPT, "Diffraction", "Advanced", "numerical",
  "Light of wavelength 600 nm falls normally on a single slit of width 2.5 μm. A screen surrounds the slit far "
  "away, so that light leaving the slit at any angle up to 90° on either side of the central direction can be "
  "observed. The total number of dark fringes (minima of intensity) in the diffraction pattern is:",
  *opt("8", ["4", "16", "9"], "C"),
  "Single-slit minima: a sin θ = nλ (n = ±1, ±2, ...), with |sin θ| ≤ 1",
  "Minima occur where a sin θ = nλ. Since sin θ cannot exceed 1, the order n can be at most a/λ = 2.5 μm/0.60 μm "
  "≈ 4.2, so n = 1, 2, 3 and 4 on each side.",
  ["n ≤ a/λ = 2.5/0.60 ≈ 4.17 → n = 1, 2, 3, 4", "4 minima on each side → 8 in all"],
  why="4 counts only one side of the central maximum. 16 uses a sin θ = nλ/2, the condition for interference "
      "between two halves, not for the minima of the whole slit. 9 counts the central maximum as a dark fringe.",
  ncert=WOC + "diffraction (the single slit)", seconds=90, rc=True)

dm_w = 2 * deg(math.asin((1.5 / (4 / 3)) * math.sin(rad(30)))) - 60
dm_a = 2 * deg(math.asin(1.5 * math.sin(rad(30)))) - 60
close(dm_w, 8.46, 1e-2)
close(dm_a, 37.2, 1e-2)
q(OPT, "Prism", "Advanced", "numerical",
  "An equilateral prism (refracting angle 60°) is made of glass of refractive index 1.5. It is completely immersed "
  "in water (refractive index 4/3). Using sin 34.2° ≈ 0.5625 and sin 48.6° ≈ 0.75, the angle of minimum deviation "
  "of the prism in water is about:",
  *opt("8.5°", ["37.2°", "68.5°", "34.2°"], "D"),
  "Prism formula with relative refractive index: n_rel = sin[(A + δ_m)/2]/sin(A/2)",
  "In water the bending at each face depends on the refractive index of glass relative to water, "
  "n_rel = 1.5/(4/3) = 1.125.",
  ["sin[(60° + δ_m)/2] = 1.125 × sin 30° = 0.5625", "(60° + δ_m)/2 = 34.2°", "δ_m = 68.4° − 60° ≈ 8.5°"],
  why="37.2° is the minimum deviation in air (using sin 48.6° = 0.75 with n = 1.5). 68.5° forgets to subtract the "
      "prism angle. 34.2° takes (A + δ_m)/2 itself as the deviation.",
  ncert=ROC + "refraction through a prism", seconds=110, rc=True)

avg_cos2 = sum(math.cos(2 * math.pi * k / 3600) ** 2 for k in range(3600)) / 3600
close(0.5 * avg_cos2, 0.25)
q(OPT, "Polarisation", "Advanced", "numerical",
  "Unpolarised light of intensity I₀ passes through a fixed ideal polaroid P₁ and then through a second ideal "
  "polaroid P₂, which is rotated steadily in its own plane. The intensity of the light emerging from P₂, averaged "
  "over one complete rotation of P₂, is:",
  *opt("I₀/4", ["I₀/2", "I₀/8", "zero"], "A"),
  "Malus's law I = I₁ cos² θ; the average of cos² θ over a full turn is 1/2",
  "P₁ passes I₀/2, plane polarised. As P₂ turns, the transmitted intensity is (I₀/2) cos² θ, varying between I₀/2 "
  "and zero. The average of cos² θ over a full rotation is 1/2.",
  ["After P₁: I₁ = I₀/2", "After P₂: I = (I₀/2) cos² θ", "Average = (I₀/2) × (1/2) = I₀/4"],
  why="I₀/2 is the maximum (θ = 0), not the average. I₀/8 is the value at θ = 60°. Zero is the minimum (θ = 90°).",
  ncert=WOC + "polarisation (Malus's law)", seconds=60, rc=True)

v1_ = 1.5 / (0.5 / 20)
v_w = (4 / 3) / ((4 / 3 - 1.5) / (-20) + 1.5 / v1_)
close(v1_, 60)
close(v_w, 40)
q(OPT, "Refraction and lenses", "Advanced", "numerical",
  "A thin equiconvex glass lens (refractive index 1.5), each face of radius of curvature 20 cm, forms the bottom of "
  "a tank: air is below the lens and water (refractive index 4/3) fills the tank above it. A parallel beam of light "
  "travels vertically upwards from below, along the axis of the lens. The beam is brought to a focus in the water "
  "at a distance from the lens of:",
  *opt("40 cm", ["20 cm", "80 cm", "26.7 cm"], "B"),
  "Refraction at a spherical surface: n₂/v − n₁/u = (n₂ − n₁)/R, applied at each face",
  "The two faces separate different media (air-glass and glass-water), so the ordinary thin-lens formula in air "
  "cannot be used. Apply the single-surface formula twice, taking the direction of the light as positive.",
  ["Face 1 (air → glass, R = +20 cm, u = ∞): 1.5/v₁ = 0.5/20 → v₁ = 60 cm",
   "Face 2 (glass → water, R = −20 cm, u = +60 cm): (4/3)/v − 1.5/60 = (4/3 − 1.5)/(−20) = 1/120",
   "(4/3)/v = 1/40 + 1/120 = 1/30 → v = 40 cm"],
  why="20 cm is the focal length with air on both sides. 80 cm is the focal length with water on both sides. "
      "26.7 cm simply multiplies the focal length in air by 4/3, which does not follow from the "
      "surface formula.",
  ncert=ROC + "refraction at spherical surfaces and by lenses", seconds=150, rc=True)

amp = {"A": (1 + 1) ** 2, "B": (1 + 0.5) ** 2, "C": (1 - 1) ** 2, "D": 1}
assert amp == {"A": 4, "B": 2.25, "C": 0, "D": 1}
q(OPT, "Huygens' principle and interference", "Advanced", "match_list",
  ml("In a Young's double-slit experiment with monochromatic light, each slit alone would produce an intensity I₀ at "
     "the central point O of the screen (equidistant from the slits). Match each arrangement in List-I with the "
     "intensity at O (List-II).",
     ["Both slits open, as described",
      "A filter placed over one slit reduces the intensity of the light from it to one-quarter, with no change of "
      "phase",
      "A thin transparent sheet over one slit (no absorption) adds an extra optical path of half a wavelength",
      "One slit is closed"],
     ["Zero", "I₀", "9I₀/4", "4I₀"]),
  *mlo("A-IV, B-III, C-I, D-II", ["A-IV, B-II, C-I, D-III", "A-III, B-IV, C-I, D-II", "A-IV, B-III, C-II, D-I"],
       "C"),
  "Superposition of amplitudes: I ∝ (a₁ + a₂)² for waves in phase, (a₁ − a₂)² for waves in antiphase",
  "Intensities add as squared amplitudes. With equal amplitudes a in phase at O: (2a)² → 4I₀. A quarter of the "
  "intensity means half the amplitude: (a + a/2)² → 9I₀/4. An extra half wavelength puts the waves in antiphase at "
  "O: (a − a)² = 0. With one slit closed there is no interference: I₀.",
  ["A: 4I₀", "B: (1 + ½)² I₀ = 9I₀/4", "C: (1 − 1)² I₀ = 0", "D: I₀"],
  why="The other codes add the filtered intensities directly (I₀ + I₀/4) instead of the amplitudes, or forget that "
      "a half-wavelength shift turns the central bright point dark.",
  ncert=WOC + "coherent and incoherent addition of waves; interference", seconds=90)

v2_ = lens_v(20 - 10, 10)
close(v2_, 5)
close(1 / (1 / 20 + 1 / 10), 6.667, 1e-2)
truth = {"a": True, "b": True, "c": True, "d": True, "e": False}
q(OPT, "Refraction and lenses", "Advanced", "multi_statement",
  ms("Two thin convex lenses L₁ (focal length 20 cm) and L₂ (focal length 10 cm) are placed coaxially 10 cm apart. A "
     "parallel beam of light travelling along the common axis falls on L₁. Which of the following statements are "
     "correct?",
     ["The beam is brought to a focus 5.0 cm beyond L₂.",
      "If the two lenses were placed in contact, the focal length of the combination would be about 6.7 cm.",
      "The beam comes to a focus closer to L₂ than the point where L₁ alone would focus it.",
      "If the separation of the lenses were made 30 cm, the beam would emerge from L₂ as a parallel beam.",
      "The power of the two lenses in contact is 5 D."]),
  *mso(truth, "abcd", ["abce", "acd", "bde"], "D"),
  "Two-lens system: the image by L₁ is the object for L₂; lenses in contact: P = P₁ + P₂",
  "L₁ alone focuses the beam 20 cm beyond it, i.e. 10 cm beyond L₂. For L₂ this is a virtual object at u = +10 cm: "
  "1/v = 1/10 + 1/10, so v = 5.0 cm (a true), which is closer than 10 cm (c true). In contact, "
  "1/f = 1/20 + 1/10 = 3/20, f ≈ 6.7 cm (b true), and P = 1/0.0667 m = 15 D, not 5 D (e false). With a "
  "separation of 30 cm the focus of L₁ coincides with the first focus of L₂, so the light leaves L₂ parallel "
  "(d true).",
  ["(a) 1/v − 1/(+10) = 1/10 → v = 5.0 cm → true", "(b) f = 20/3 ≈ 6.7 cm → true", "(c) 5 cm < 10 cm → true",
   "(d) 20 + 10 = 30 cm separation → parallel output → true", "(e) P = 5 D + 10 D = 15 D → false"],
  why="Options containing (e) subtract instead of adding the powers (or use one lens only). Options leaving out (a) "
      "or (d) miss correct results of the two-lens calculation.",
  ncert=ROC + "refraction by a lens (combination of thin lenses)", seconds=150, rc=True)

# ================================================================ Dual Nature of Matter and Radiation (B3 I4 A3)
DNC = NC + "'Dual Nature of Radiation and Matter', "
HC = 1240.0     # eV nm

# ---- Basic
lam_e = 6.6e-34 / (9.1e-31 * 1.0e6)
close(lam_e, 7.25e-10, 1e-2)
q(DUAL, "de Broglie wavelength", "Basic", "numerical",
  "An electron (mass 9.1 × 10⁻³¹ kg) moves with a speed of 1.0 × 10⁶ m/s. Taking h = 6.6 × 10⁻³⁴ J s, its de Broglie "
  "wavelength is about:",
  *opt("0.73 nm", ["0.36 nm", "7.3 nm", "4.1 × 10⁻⁴ nm"], "B"),
  "de Broglie relation λ = h/p = h/(mv)",
  "For a non-relativistic particle the momentum is mv, and the associated wavelength is h divided by it.",
  ["p = 9.1 × 10⁻³¹ × 1.0 × 10⁶ = 9.1 × 10⁻²⁵ kg m/s", "λ = 6.6 × 10⁻³⁴/9.1 × 10⁻²⁵ ≈ 7.3 × 10⁻¹⁰ m = 0.73 nm"],
  why="0.36 nm divides by 2mv. 7.3 nm is out by a factor of 10 in converting metres to nanometres. 4.1 × 10⁻⁴ nm "
      "uses the proton mass instead of the electron mass.",
  ncert=DNC + "wave nature of matter", seconds=40, rc=True)

E_300 = HC / 300
close(E_300, 4.13, 1e-2)
assert E_300 < 4.5
q(DUAL, "Photoelectric effect", "Basic", "numerical",
  "The work function of a metal surface is 4.5 eV. Ultraviolet light of wavelength 300 nm falls on it. Taking "
  "hc = 1240 eV nm, which statement is correct?",
  *opt("No photoelectrons are emitted, because each photon carries only about 4.1 eV",
       ["Photoelectrons are emitted with kinetic energies up to about 0.4 eV",
        "Photoelectrons are emitted if the light is made intense enough",
        "Photoelectrons are emitted with kinetic energies up to about 4.1 eV"], "C"),
  "Einstein's photoelectric equation: emission needs hν ≥ φ₀",
  "Each photon gives its energy to a single electron. A photon of 300 nm carries hc/λ = 1240/300 ≈ 4.13 eV, which "
  "is less than the 4.5 eV needed to free an electron, so no electron can escape, however many photons arrive.",
  ["E = 1240/300 ≈ 4.13 eV", "4.13 eV < φ₀ = 4.5 eV → no emission"],
  why="'Up to about 0.4 eV' subtracts the energies the wrong way round. Intensity only changes the number of "
      "photons, not the energy of each, so brighter light cannot cause emission. 'Up to 4.1 eV' ignores the work "
      "function altogether.",
  ncert=DNC + "Einstein's photoelectric equation: energy quantum of radiation", seconds=40, rc=True)

q(DUAL, "Einstein's equation", "Basic", "statement_pair",
  sp("If the frequency of the light falling on a photosensitive surface is doubled, the maximum kinetic energy of "
     "the emitted photoelectrons is also doubled.",
     "The stopping potential varies linearly with the frequency of the incident light (above the threshold "
     "frequency)."),
  SP, sp_key(False, True),
  "K_max = hν − φ₀ and eV₀ = hν − φ₀",
  "K_max is a linear function of ν with a negative intercept −φ₀, not proportional to ν. Doubling ν gives "
  "2hν − φ₀, which is more than twice hν − φ₀ (Statement I false). V₀ = (h/e)ν − φ₀/e is a straight line of slope "
  "h/e (Statement II true).",
  ["I: K' = 2hν − φ₀ ≠ 2(hν − φ₀) → false", "II: V₀ = (h/e)ν − φ₀/e → linear → true"],
  why="Statement I would hold only if the work function were zero; linear is not the same as proportional.",
  ncert=DNC + "Einstein's photoelectric equation", seconds=40)

# ---- Intermediate
q(DUAL, "Photoelectric effect", "Intermediate", "direct",
  "A small lamp, acting as a point source of monochromatic light, is placed 1.0 m from the emitter of a photocell "
  "and gives a measurable photocurrent. The lamp is then moved to a distance of 0.50 m, all else being unchanged. "
  "As a result:",
  *opt("the saturation photocurrent becomes about four times as large, and the stopping potential is unchanged",
       ["the saturation photocurrent doubles, and the stopping potential is unchanged",
        "both the saturation photocurrent and the stopping potential become about four times as large",
        "the saturation photocurrent is unchanged, and the stopping potential doubles"], "A"),
  "Photocurrent ∝ intensity; stopping potential depends only on frequency (and the metal)",
  "For a point source the intensity at the emitter varies as 1/r², so halving the distance makes it four times as "
  "large. Four times as many photons per second eject about four times as many electrons, so the saturation "
  "current becomes about four times. The energy of each photon (the frequency) is unchanged, so the maximum "
  "kinetic energy and the stopping potential do not change.",
  ["Intensity ∝ 1/r²: (1.0/0.50)² = 4", "Saturation current ∝ intensity → ×4", "V₀ depends on ν only → unchanged"],
  why="Doubling would follow from 1/r, not 1/r². The stopping potential does not depend on intensity, so options "
      "that change it are wrong.",
  ncert=DNC + "experimental study of photoelectric effect (effect of intensity)", seconds=45)

assert math.isclose(math.sqrt(4 / 1), 2) and math.isclose(math.sqrt(4 * 2 / (1 * 1)), 2 * math.sqrt(2))
q(DUAL, "de Broglie wavelength", "Intermediate", "numerical",
  "A proton and an alpha particle move with equal kinetic energies (both much slower than light). Taking the mass of "
  "the alpha particle as 4 times that of the proton, the ratio of the de Broglie wavelength of the proton to that "
  "of the alpha particle is:",
  *opt("2 : 1", ["1 : 2", "4 : 1", "2√2 : 1"], "B"),
  "λ = h/p = h/√(2mK)",
  "With equal kinetic energies, λ ∝ 1/√m. The lighter proton has the smaller momentum and so the longer "
  "wavelength.",
  ["λ_p/λ_α = √(m_α/m_p) = √4 = 2"],
  why="1 : 2 inverts the ratio. 4 : 1 uses λ ∝ 1/m, which holds for equal speeds, not equal energies. 2√2 : 1 is "
      "the ratio for particles accelerated through the same potential difference (which gives the alpha particle "
      "twice the energy).",
  ncert=DNC + "wave nature of matter", seconds=45, rc=True)

phi6 = HC / 400 - 1.0
lam0 = HC / phi6
close(phi6, 2.1)
close(lam0, 590.5, 1e-2)
close(HC / (HC / 400 + 1.0), 302.4, 1e-2)
q(DUAL, "Einstein's equation", "Intermediate", "numerical",
  "When light of wavelength 400 nm falls on a metal surface, the fastest photoelectrons have a kinetic energy of "
  "1.0 eV. Taking hc = 1240 eV nm, the threshold wavelength for this metal is about:",
  *opt("590 nm", ["400 nm", "1240 nm", "300 nm"], "C"),
  "K_max = hc/λ − φ₀; threshold wavelength λ₀ = hc/φ₀",
  "Find the photon energy, subtract the maximum kinetic energy to get the work function, then convert the work "
  "function to the threshold wavelength.",
  ["hc/λ = 1240/400 = 3.1 eV", "φ₀ = 3.1 − 1.0 = 2.1 eV", "λ₀ = 1240/2.1 ≈ 590 nm"],
  why="400 nm is the wavelength used, which gives emission with energy to spare, so the threshold is longer. "
      "1240 nm treats the 1.0 eV kinetic energy as the work function. 300 nm adds the kinetic energy to the photon "
      "energy instead of subtracting it.",
  ncert=DNC + "Einstein's photoelectric equation", seconds=60, rc=True)

q(DUAL, "de Broglie wavelength", "Intermediate", "assertion_reason",
  ar("A photon and an electron that have the same energy also have the same wavelength.",
     "For a photon as well as for an electron, the wavelength and the momentum are related by λ = h/p."),
  AR, ar_key(False, True),
  "Photon: p = E/c; electron: p = √(2mK)",
  "R is true: λ = h/p holds for both. But equal energies do not mean equal momenta. A photon of energy E has "
  "p = E/c, while an electron of kinetic energy E has p = √(2mE). For E of a few eV the electron's momentum is far "
  "larger, so its wavelength is far shorter (for example about 0.9 nm against about 620 nm at 2 eV). A is false.",
  ["R: λ = h/p for both → true", "A: p_photon = E/c ≠ p_electron = √(2mE) → different λ → false"],
  why="Equal energies give equal wavelengths only if the momenta are equal, which they are not; so A is false and "
      "R is true.",
  ncert=DNC + "wave nature of matter; particle nature of light: the photon", seconds=50)

# ---- Advanced
E_ph = math.sqrt(2 * 0.511e6 * 2.5)
close(E_ph, 1598, 1e-2)
close(math.sqrt(0.511e6 * 2.5), 1130, 1e-2)
q(DUAL, "de Broglie wavelength", "Advanced", "numerical",
  "A photon has the same momentum (and hence the same wavelength) as an electron of kinetic energy 2.5 eV. Taking "
  "the rest-mass energy of the electron, mc², as 0.511 MeV and √2.56 = 1.6, the energy of the photon is about:",
  *opt("1.6 keV", ["2.5 eV", "1.1 keV", "5.0 eV"], "A"),
  "Electron: p = √(2mK); photon: E = pc",
  "Equal momenta: E_photon = pc = c√(2mK) = √(2mc² K). Working in electron volts avoids converting units.",
  ["E = √(2 × 0.511 × 10⁶ eV × 2.5 eV) = √(2.555 × 10⁶) eV", "≈ 1.6 × 10³ eV = 1.6 keV"],
  why="2.5 eV assumes equal energies give equal momenta. 1.1 keV leaves out the factor 2 in p = √(2mK). 5.0 eV "
      "doubles the electron's energy, which has no basis.",
  ncert=DNC + "wave nature of matter; the photon", seconds=90, rc=True)

V0_, l0_ = 3.0 - 2.0, HC / 2.0
close(V0_, 1.0)
close(l0_, 620)
assert HC / 600 > 2.0
truth = {"a": True, "b": True, "c": True, "d": True, "e": False}
q(DUAL, "Photoelectric effect", "Advanced", "multi_statement",
  ms("Photons of energy 3.0 eV fall on the emitter of a photocell, whose work function is 2.0 eV. Take "
     "hc = 1240 eV nm. Which of the following statements are correct?",
     ["The stopping potential is 1.0 V.",
      "The threshold wavelength of the emitter is 620 nm.",
      "If the intensity of the light is doubled (same photon energy), the stopping potential is still 1.0 V.",
      "If the collector is held at +2.0 V relative to the emitter, the fastest electrons reach it with 3.0 eV of "
      "kinetic energy.",
      "Light of wavelength 600 nm would not eject any photoelectrons from this emitter."]),
  *mso(truth, "abcd", ["abce", "abc", "bcde"], "B"),
  "eV₀ = hν − φ₀; λ₀ = hc/φ₀; an accelerating potential adds eV to the kinetic energy",
  "K_max = 3.0 − 2.0 = 1.0 eV, so V₀ = 1.0 V (a true). λ₀ = 1240/2.0 = 620 nm (b true). Intensity does not affect "
  "V₀ (c true). An accelerating potential of 2.0 V adds 2.0 eV, so the fastest electrons arrive with 3.0 eV (d "
  "true). Light of 600 nm is shorter than the 620 nm threshold; its photons carry 1240/600 ≈ 2.07 eV > 2.0 eV, so "
  "it does eject electrons (e false).",
  ["(a) V₀ = 1.0 V → true", "(b) λ₀ = 620 nm → true", "(c) true", "(d) 1.0 + 2.0 = 3.0 eV → true",
   "(e) 600 nm < λ₀ → emission occurs → false"],
  why="Options containing (e) forget that any wavelength shorter than the threshold wavelength causes emission. "
      "Options leaving out (d) miss that the collector potential adds to the kinetic energy.",
  ncert=DNC + "photoelectric effect; Einstein's photoelectric equation", seconds=120, rc=True)

nu_ = F(1)
K1 = nu_ - F(1, 2)
assert F(3, 2) * nu_ - F(1, 2) == 2 * K1
q(DUAL, "Einstein's equation", "Advanced", "numerical",
  "When light of frequency ν falls on a metal, the maximum kinetic energy of the photoelectrons is K. When the "
  "frequency is increased by 50% (to 1.5ν), the maximum kinetic energy becomes 2K. The threshold frequency of the "
  "metal is:",
  *opt("ν/2", ["ν/4", "2ν/3", "ν/3"], "C"),
  "Einstein's equation K_max = h(ν − ν₀)",
  "Write the equation for both frequencies and eliminate K.",
  ["h(ν − ν₀) = K and h(1.5ν − ν₀) = 2K", "Subtract: 0.5hν = K", "hν − hν₀ = 0.5hν → ν₀ = ν/2"],
  why="ν/4, 2ν/3 and ν/3 come from algebraic slips; substituting any of them back does not double K when ν rises "
      "by 50% (for example ν₀ = ν/3 gives K = 2hν/3 and 7hν/6, a ratio of 7/4).",
  ncert=DNC + "Einstein's photoelectric equation", seconds=75, rc=True)


# ================================================================ Atoms and Nuclei (B4 I5 A4)
ATC = NC + "'Atoms', "
NUC = NC + "'Nuclei', "

# ---- Basic
q(AN, "Rutherford scattering", "Basic", "direct",
  "Which of the following conclusions could NOT be drawn from the alpha-particle scattering experiment of Geiger and "
  "Marsden by itself?",
  *opt("Electrons revolve round the nucleus only in certain stationary orbits, without radiating energy",
       ["Most of the space inside an atom is empty",
        "The positive charge and most of the mass of an atom are concentrated in a tiny central region",
        "The nucleus is very much smaller than the atom as a whole"], "A"),
  "Rutherford's nuclear model and Bohr's postulates",
  "The scattering results show that most alpha particles pass straight through (mostly empty space), that a few "
  "are deflected through large angles (a tiny, massive, positively charged nucleus) and give an estimate of the "
  "nuclear size. They say nothing about how the electrons move; stationary non-radiating orbits are Bohr's "
  "postulate, introduced later to explain the stability of atoms and the line spectrum of hydrogen.",
  ["Empty space, concentrated positive mass, small nucleus → from scattering",
   "Stationary orbits → Bohr's postulate, not from scattering"],
  why="The other three are exactly the conclusions Rutherford drew from the scattering data.",
  ncert=ATC + "alpha-particle scattering and Rutherford's nuclear model of atom; Bohr model", seconds=35)

assert [z ** 2 for z in (1, 2, 3)] == [1, 4, 9]
q(AN, "Bohr model and hydrogen spectrum", "Basic", "numerical",
  "According to the Bohr model, the ratio of the ionisation energies of the hydrogen atom (H), the singly ionised "
  "helium ion (He⁺) and the doubly ionised lithium ion (Li²⁺), each in its ground state, is:",
  *opt("1 : 4 : 9", ["1 : 2 : 3", "9 : 4 : 1", "1 : 8 : 27"], "B"),
  "Bohr energy of a hydrogen-like ion E_n = −13.6 Z²/n² eV",
  "In the ground state (n = 1) the ionisation energy is 13.6 Z² eV, so it is proportional to Z², with Z = 1, 2 and "
  "3.",
  ["13.6 × 1² : 13.6 × 2² : 13.6 × 3² = 1 : 4 : 9"],
  why="1 : 2 : 3 uses Z instead of Z². 9 : 4 : 1 inverts the ratio. 1 : 8 : 27 uses Z³.",
  ncert=ATC + "Bohr model of the hydrogen atom (hydrogen-like ions)", seconds=30, rc=True)

q(AN, "Fission and fusion", "Basic", "statement_pair",
  sp("The energy released in the fission of one ²³⁵U nucleus is of the order of 200 MeV.",
     "The binding energy per nucleon of the nuclei produced in the fission of ²³⁵U is greater than that of the "
     "uranium nucleus."),
  SP, sp_key(True, True),
  "Fission releases energy because the fragments are more tightly bound",
  "NCERT gives the energy released per fission of ²³⁵U as about 200 MeV (Statement I true). It arises because the "
  "binding energy per nucleon rises from about 7.6 MeV for uranium to about 8.5 MeV for the medium-mass fragments "
  "(Statement II true).",
  ["I: ~200 MeV per fission → true", "II: ~8.5 MeV vs ~7.6 MeV per nucleon → true"],
  why="Both statements are standard NCERT results, and the second explains the first.",
  ncert=NUC + "nuclear energy (fission)", seconds=35)

lam_He = 121.6 / 4
close(lam_He, 30.4)
q(AN, "Bohr model and hydrogen spectrum", "Basic", "numerical",
  "The wavelength of the photon emitted when a hydrogen atom makes the transition from n = 2 to n = 1 is 121.6 nm. "
  "In the Bohr model, the wavelength of the photon emitted in the same transition (n = 2 to n = 1) by a He⁺ ion is:",
  *opt("30.4 nm", ["60.8 nm", "486 nm", "13.5 nm"], "D"),
  "For hydrogen-like ions, transition energies scale as Z², so wavelengths scale as 1/Z²",
  "The energy levels of He⁺ (Z = 2) are 4 times those of hydrogen, so the same transition emits a photon of 4 times "
  "the energy and one-quarter the wavelength.",
  ["E(He⁺) = Z² × E(H) = 4 × E(H)", "λ(He⁺) = 121.6/4 = 30.4 nm"],
  why="60.8 nm divides by Z instead of Z². 486 nm multiplies by 4 instead of dividing. 13.5 nm divides by 9, as "
      "for Li²⁺.",
  ncert=ATC + "Bohr model (hydrogen-like ions); line spectra", seconds=35, rc=True)

# ---- Intermediate
balmer = [(ni, 2) for ni in range(3, 6)]
assert len(balmer) == 3 and 5 * 4 // 2 == 10
q(AN, "Bohr model and hydrogen spectrum", "Intermediate", "numerical",
  "A sample of hydrogen atoms is excited so that the atoms are in the n = 5 state. As they return to lower states by "
  "all possible transitions, the number of different lines of the Balmer series that can appear in the emission "
  "spectrum is:",
  *opt("3", ["10", "4", "6"], "D"),
  "Balmer lines are transitions ending on n = 2",
  "Every Balmer line ends on n = 2 and starts from a higher level. From the levels available (n = 3, 4 and 5) "
  "there are three such transitions: 5 → 2, 4 → 2 and 3 → 2.",
  ["Possible upper levels: 3, 4, 5", "Balmer lines: 5→2, 4→2, 3→2 → 3 lines"],
  why="10 is the total number of lines of all series from n = 5 (5 × 4/2). 4 counts the levels from 2 to 5 rather "
      "than the transitions ending on n = 2. 6 is the total for atoms starting from n = 4.",
  ncert=ATC + "line spectra of the hydrogen atom", seconds=40, rc=True)

E43 = 54.4 * (1 / 9 - 1 / 16)
close(E43, 2.644, 1e-2)
close(HC / E43, 469, 1e-2)
close(HC / (54.4 * (1 / 4 - 1 / 16)), 121.6, 1e-2)
close(HC / (54.4 * (1 / 4 - 1 / 9)), 164, 1e-2)
q(AN, "Bohr model and hydrogen spectrum", "Intermediate", "numerical",
  "He⁺ ions (Z = 2) are excited to the n = 4 state. In the Bohr model their energy levels are "
  "E_n = −54.4/n² eV. Taking hc = 1240 eV nm and the visible region as 400 nm to 700 nm, which transition gives a "
  "photon of visible light?",
  *opt("n = 4 → n = 3, about 469 nm", ["n = 4 → n = 2, about 122 nm", "n = 3 → n = 2, about 164 nm",
                                       "n = 2 → n = 1, about 30 nm"], "A"),
  "Photon energy = difference of levels; λ = hc/ΔE",
  "Compute the photon energies of the transitions from n = 4 and below. Only a photon of energy between about "
  "1.8 eV and 3.1 eV is visible.",
  ["4 → 3: ΔE = 54.4(1/9 − 1/16) ≈ 2.64 eV → λ ≈ 469 nm (visible)", "4 → 2: 10.2 eV → 122 nm (ultraviolet)",
   "3 → 2: 7.56 eV → 164 nm (ultraviolet)", "2 → 1: 40.8 eV → 30 nm (ultraviolet)"],
  why="The other three transitions are real but their photons (10.2 eV, 7.56 eV, 40.8 eV) lie far in the "
      "ultraviolet.",
  ncert=ATC + "Bohr model (hydrogen-like ions); line spectra", seconds=90, rc=True)

rr = 0.5 ** (1 / 3)
close(rr, 0.794, 1e-2)
q(AN, "Nuclear size and mass defect", "Intermediate", "numerical",
  "A nucleus of mass number A splits into two fragments of equal mass number. Using R = R₀A^(1/3) for each nucleus, "
  "the ratio of the radius of each fragment to the radius of the original nucleus is about:",
  *opt("0.79", ["0.50", "0.71", "0.63"], "B"),
  "Nuclear radius R ∝ A^(1/3) (constant nuclear density)",
  "Each fragment has mass number A/2, so its radius is R₀(A/2)^(1/3) = (1/2)^(1/3) times the original radius.",
  ["R_frag/R = (1/2)^(1/3) ≈ 0.79"],
  why="0.50 takes the radius proportional to A. 0.71 uses (1/2)^(1/2). 0.63 uses (1/2)^(2/3), the ratio of the "
      "surface areas, not the radii.",
  ncert=NUC + "size of the nucleus", seconds=40, rc=True)

nuc = {"Ar": (18, 40), "Ca": (20, 40), "Cl35": (17, 35), "Cl37": (17, 37), "C13": (6, 13), "N14": (7, 14),
       "Li": (3, 7), "C12": (6, 12)}
N_ = lambda k: nuc[k][1] - nuc[k][0]
assert nuc["Ar"][1] == nuc["Ca"][1] and nuc["Cl35"][0] == nuc["Cl37"][0] and N_("C13") == N_("N14") == 7
assert nuc["Li"][0] != nuc["C12"][0] and nuc["Li"][1] != nuc["C12"][1] and N_("Li") != N_("C12")
q(AN, "Nuclear size and mass defect", "Intermediate", "match_list",
  ml("Match each pair of nuclides in List-I with the relation between them (List-II).",
     ["⁴⁰₁₈Ar and ⁴⁰₂₀Ca", "³⁵₁₇Cl and ³⁷₁₇Cl", "¹³₆C and ¹⁴₇N", "⁷₃Li and ¹²₆C"],
     ["Isotones", "Isobars", "None of these relations", "Isotopes"]),
  *mlo("A-II, B-IV, C-I, D-III", ["A-IV, B-II, C-I, D-III", "A-II, B-IV, C-III, D-I", "A-I, B-IV, C-II, D-III"],
       "C"),
  "Isotopes: same Z; isobars: same A; isotones: same N = A − Z",
  "Compare Z, A and N = A − Z for each pair.",
  ["A: A = 40 for both (Z = 18, 20) → isobars", "B: Z = 17 for both (A = 35, 37) → isotopes",
   "C: N = 13 − 6 = 7 and 14 − 7 = 7 → isotones", "D: Z 3 vs 6, N 4 vs 6, A 7 vs 12 → none"],
  why="The other codes exchange isobars and isotopes (same A versus same Z) or miss that ¹³C and ¹⁴N have the same "
      "number of neutrons.",
  ncert=NUC + "atomic masses and composition of nucleus", seconds=60)

q(AN, "Bohr model and hydrogen spectrum", "Intermediate", "assertion_reason",
  ar("In the Bohr model, the radius of the ground-state orbit of the He⁺ ion is half the radius of the ground-state "
     "orbit of the hydrogen atom.",
     "In the Bohr model, the orbit radius of a hydrogen-like ion is proportional to n²/Z²."),
  AR, ar_key(True, False),
  "Bohr radius for a hydrogen-like ion r_n = (0.53 Å) n²/Z",
  "The Coulomb attraction is Z times stronger, and the quantisation condition gives r_n ∝ n²/Z. For He⁺ (Z = 2) "
  "in n = 1 the radius is half that of hydrogen (A true). R states n²/Z², which is the dependence of the energy "
  "(on Z²) confused with the radius; it would give a quarter, not a half (R false).",
  ["r ∝ n²/Z → r(He⁺)/r(H) = 1/2 → A true", "n²/Z² is wrong → R false"],
  why="Since R is false, it cannot be the explanation of A, and A itself is true.",
  ncert=ATC + "Bohr model of the hydrogen atom", seconds=45)

# ---- Advanced
lhs, rhs = 14.003074 + 4.002603, 16.999132 + 1.007825
Qv = (lhs - rhs) * 931.5
close(Qv, -1.192, 1e-2)
q(AN, "Nuclear size and mass defect", "Advanced", "numerical",
  "For the nuclear reaction ¹⁴₇N + ⁴₂He → ¹⁷₈O + ¹₁H, the atomic masses are ¹⁴N = 14.003074 u, ⁴He = 4.002603 u, "
  "¹⁷O = 16.999132 u and ¹H = 1.007825 u. Taking 1 u = 931.5 MeV/c², the Q-value of the reaction is about:",
  *opt("−1.19 MeV; the reaction absorbs energy", ["+1.19 MeV; the reaction releases energy",
                                                  "−1.28 MeV; the reaction absorbs energy",
                                                  "zero, because the number of nucleons is conserved"], "D"),
  "Q = (total initial mass − total final mass) c²",
  "Electron masses cancel because the atomic numbers balance (7 + 2 = 8 + 1). The products are heavier than the "
  "reactants, so Q is negative: kinetic energy must be supplied (by the alpha particle) for the reaction to occur.",
  ["Initial: 14.003074 + 4.002603 = 18.005677 u", "Final: 16.999132 + 1.007825 = 18.006957 u",
   "Δm = −0.001280 u → Q = −0.001280 × 931.5 ≈ −1.19 MeV"],
  why="+1.19 MeV gets the sign wrong: the mass increases, so energy is absorbed. −1.28 MeV converts the mass "
      "difference as if 1 u were 1000 MeV. Conservation of nucleon number does not make Q zero; Q comes from the "
      "change in mass (binding energy).",
  ncert=NUC + "mass-energy and nuclear binding energy", seconds=120, rc=True)

K_ion = 15.0 - 13.6
lam_ion = 1.227 / math.sqrt(K_ion)
close(lam_ion, 1.037, 1e-2)
close(1.227 / math.sqrt(15.0), 0.317, 1e-2)
close(1.227 / K_ion, 0.876, 1e-2)
q(AN, "Bohr model and hydrogen spectrum", "Advanced", "numerical",
  "A photon of energy 15.0 eV is absorbed by a hydrogen atom in its ground state (E₁ = −13.6 eV), and the electron "
  "is ejected. Neglecting the recoil of the proton and using λ = 1.227/√K nm for an electron of kinetic energy K "
  "(in eV), the de Broglie wavelength of the ejected electron is about:",
  *opt("1.04 nm", ["0.32 nm", "0.88 nm", "83 nm"], "B"),
  "Energy conservation: K = hν − (ionisation energy); de Broglie wavelength λ = h/√(2mK)",
  "13.6 eV of the photon's energy is used to free the electron from the ground state; the rest appears as the "
  "kinetic energy of the electron.",
  ["K = 15.0 − 13.6 = 1.4 eV", "λ = 1.227/√1.4 ≈ 1.227/1.18 ≈ 1.04 nm"],
  why="0.32 nm uses the whole 15.0 eV as kinetic energy. 0.88 nm divides by K instead of √K. 83 nm is the "
      "wavelength of the photon (1240/15), not of the electron.",
  ncert=ATC + "Bohr model (ionisation energy); " + "Class 12 Physics, 'Dual Nature of Radiation and Matter', wave "
              "nature of matter", seconds=90, rc=True)

ion = {"A": 13.6 / 4, "B": 13.6 * 4 / 4, "C": 13.6 * 9 / 4, "D": 13.6 * 4 / 9}
close(ion["A"], 3.4)
close(ion["B"], 13.6)
close(ion["C"], 30.6)
close(ion["D"], 6.04, 1e-2)
q(AN, "Bohr model and hydrogen spectrum", "Advanced", "match_list",
  ml("In the Bohr model, the energy levels of a hydrogen-like ion are E_n = −13.6 Z²/n² eV. Match each ion and state "
     "in List-I with the energy needed to remove its electron from that state (List-II).",
     ["Hydrogen atom, n = 2", "He⁺ ion, n = 2", "Li²⁺ ion, n = 2", "He⁺ ion, n = 3"],
     ["13.6 eV", "6.04 eV", "3.4 eV", "30.6 eV"]),
  *mlo("A-III, B-I, C-IV, D-II", ["A-I, B-III, C-IV, D-II", "A-III, B-I, C-II, D-IV", "A-III, B-IV, C-I, D-II"],
       "A"),
  "Ionisation energy from level n = 13.6 Z²/n² eV",
  "The energy needed to remove the electron from level n is |E_n| = 13.6 Z²/n² eV.",
  ["A: 13.6 × 1/4 = 3.4 eV", "B: 13.6 × 4/4 = 13.6 eV", "C: 13.6 × 9/4 = 30.6 eV", "D: 13.6 × 4/9 ≈ 6.04 eV"],
  why="The other codes exchange hydrogen's n = 2 value with He⁺'s, or the Li²⁺ and He⁺ (n = 3) values, by using Z "
      "instead of Z² or n instead of n².",
  ncert=ATC + "Bohr model (energy levels of hydrogen-like ions)", seconds=75, rc=True)

dm_DT = 17.6 / 931.5
close(dm_DT, 0.0189, 1e-2)
assert 17.6 / 5 > 200 / 236
truth = {"a": True, "b": True, "c": True, "d": False, "e": True}
q(AN, "Fission and fusion", "Advanced", "multi_statement",
  ms("Consider the reaction ²₁H + ³₁H → ⁴₂He + ¹₀n, which releases 17.6 MeV. Take 1 u = 931.5 MeV/c². Which of the "
     "following statements are correct?",
     ["It is a fusion reaction.",
      "The total number of nucleons is the same (five) on both sides.",
      "The total mass of the products is less than that of the reactants by about 0.019 u.",
      "The reaction takes place readily at room temperature, because the nuclear force between the nuclei is "
      "attractive.",
      "The energy released per nucleon of the reacting nuclei is greater than in the fission of a ²³⁵U nucleus "
      "(about 200 MeV per fission)."]),
  *mso(truth, "abce", ["abcd", "ace", "bcde"], "D"),
  "Fusion of light nuclei; mass-energy relation; Coulomb barrier",
  "Two light nuclei combine into a heavier one (a true); nucleon number is conserved, 2 + 3 = 4 + 1 (b true). The "
  "mass that disappears is 17.6/931.5 ≈ 0.019 u (c true). The nuclei are both positively charged; they must be "
  "brought within the very short range of the nuclear force against their Coulomb repulsion, which needs "
  "temperatures of the order of 10⁷ K or more, so the reaction does not occur at room temperature (d false). Per "
  "nucleon, fusion gives 17.6/5 ≈ 3.5 MeV, against about 200/236 ≈ 0.85 MeV for fission (e true).",
  ["(a) true", "(b) 5 = 5 → true", "(c) 17.6/931.5 ≈ 0.0189 u → true",
   "(d) Coulomb barrier needs very high temperature → false", "(e) 3.5 MeV > 0.85 MeV per nucleon → true"],
  why="Options with (d) ignore the Coulomb repulsion between the nuclei, which the short-range nuclear force cannot "
      "overcome at ordinary temperatures. Options leaving out (b) or (e) miss correct statements.",
  ncert=NUC + "nuclear energy (fusion - energy generation in stars)", seconds=120, rc=True)

# ================================================================ Electronic Devices (B5 I6 A5)
SEC = NC + "'Semiconductor Electronics: Materials, Devices and Simple Circuits', "
LOGIC = "NMC syllabus, logic gates (OR, AND, NOT, NAND and NOR)"
BITS = [(0, 0), (0, 1), (1, 0), (1, 1)]
NOT = lambda a: 1 - a
AND = lambda a, b: a & b
OR = lambda a, b: a | b
NOR = lambda a, b: NOT(OR(a, b))
NAND = lambda a, b: NOT(AND(a, b))

# ---- Basic
q(ED, "p-n junction diode and rectifier", "Basic", "numerical",
  "An ideal junction diode is connected in series with a 1.0 kΩ resistor across an ideal 5.0 V battery, the diode "
  "being reverse biased. The potential difference across the diode is:",
  *opt("5.0 V", ["zero", "0.7 V", "2.5 V"], "A"),
  "An ideal diode has infinite resistance in reverse bias",
  "A reverse-biased ideal diode lets no current flow. With zero current, there is no potential drop across the "
  "resistor (V = IR = 0), so the whole battery voltage appears across the diode.",
  ["I = 0 → V_R = 0", "V_diode = 5.0 − 0 = 5.0 V"],
  why="Zero would be the drop across an ideal diode in forward bias. 0.7 V is the forward drop of a real silicon "
      "diode. 2.5 V assumes the voltage is shared equally, as between two equal resistors.",
  ncert=SEC + "p-n junction diode under reverse bias; ideal diode", seconds=30, rc=True)
assert 5.0 - 0 * 1000 == 5.0

q(ED, "LED, photodiode and solar cell", "Basic", "direct",
  "An LED is to emit green light of wavelength about 540 nm. The photon energy of an LED is about equal to the band "
  "gap of its semiconductor. Taking hc = 1240 eV nm, which of the following semiconductors, identified by their "
  "band gaps, is suitable?",
  *opt("A semiconductor with a band gap of 2.3 eV",
       ["A semiconductor with a band gap of 1.1 eV", "A semiconductor with a band gap of 1.4 eV",
        "A semiconductor with a band gap of 3.1 eV"], "B"),
  "LED: emitted photon energy hc/λ ≈ E_g",
  "In an LED the light comes from electrons and holes recombining across the band gap, so each photon carries an "
  "energy close to E_g. The band gap needed is therefore hc/λ.",
  ["E_g ≈ 1240/540 ≈ 2.3 eV", "1.1 eV → about 1130 nm, 1.4 eV → about 890 nm (both infrared); 3.1 eV → 400 nm "
   "(violet)"],
  why="Band gaps of 1.1 eV and 1.4 eV give infrared photons, invisible to the eye. A band gap of 3.1 eV gives violet "
      "light near 400 nm, not green.",
  ncert=SEC + "optoelectronic junction devices (light emitting diode)", seconds=40)
close(HC / 540, 2.30, 1e-2)
close(HC / 3.1, 400)

q(ED, "LED, photodiode and solar cell", "Basic", "statement_pair",
  sp("A solar cell is a p-n junction that generates an emf when solar radiation falls on it.",
     "The three basic processes by which a solar cell generates an emf are the generation of electron-hole pairs by "
     "light, the separation of the electrons and holes by the junction field, and their collection at the "
     "electrodes."),
  SP, sp_key(True, True),
  "Working of a solar cell",
  "NCERT describes the solar cell as a p-n junction that generates emf when solar radiation falls on it, working on "
  "the same principle as the photodiode but without any external bias (Statement I true). It lists the three "
  "basic processes: generation, separation and collection (Statement II true).",
  ["Statement I: true", "Statement II: true (generation, separation, collection)"],
  why="Both statements are taken directly from NCERT's description of the solar cell.",
  ncert=SEC + "optoelectronic junction devices (solar cell)", seconds=30)

q(ED, "Semiconductors", "Basic", "assertion_reason",
  ar("At room temperature, the intrinsic carrier concentration of germanium is much larger than that of silicon.",
     "Germanium, like silicon, is an elemental semiconductor."),
  AR, ar_key(True, True, False),
  "Intrinsic carrier concentration depends on the band gap",
  "Germanium has a smaller band gap (about 0.7 eV) than silicon (about 1.1 eV), so at the same temperature many "
  "more electrons are thermally excited across the gap: A is true. R is also true, but both materials are "
  "elemental semiconductors, so being elemental cannot account for the difference between them. R is true but does "
  "not explain A.",
  ["A: true (smaller E_g → more electron-hole pairs)", "R: true (Ge and Si are both elemental)",
   "R names a property the two share, so it cannot explain a difference → B"],
  why="The reason for A is the smaller band gap of germanium, not the fact that it is elemental, so 'R is the "
      "correct explanation' is wrong; both statements are true, so C and D are wrong.",
  ncert=SEC + "classification of metals, conductors and semiconductors; intrinsic semiconductor", seconds=40)

q(ED, "p-n junction diode and rectifier", "Basic", "numerical",
  "An alternating voltage v = 20 sin(100πt) volt (t in seconds) is applied to a half-wave rectifier consisting of an "
  "ideal diode in series with a load resistor. The peak voltage across the load and the frequency of the rectified "
  "output are:",
  *opt("20 V and 50 Hz", ["14.1 V and 50 Hz", "20 V and 100 Hz", "10 V and 50 Hz"], "C"),
  "Half-wave rectifier: one output pulse per input cycle; ideal diode → no voltage lost",
  "The input has peak value 20 V and ω = 100π rad/s, i.e. f = 50 Hz. An ideal diode passes the positive half "
  "cycles unchanged, so the output peaks at 20 V and repeats once per input cycle.",
  ["V_peak = 20 V", "f = ω/2π = 100π/2π = 50 Hz", "Half-wave: output frequency = input frequency = 50 Hz"],
  why="14.1 V is the rms value of the input, not the peak of the output. 100 Hz is the output frequency of a "
      "full-wave rectifier. 10 V halves the peak, but the diode removes half of each cycle, not half of the "
      "amplitude.",
  ncert=SEC + "application of junction diode as a rectifier", seconds=40, rc=True)
assert 100 * math.pi / (2 * math.pi) == 50

# ---- Intermediate
n_ser, n_par = 12 / 0.50, 6.0 / 2.0
assert n_ser == 24 and n_par == 3 and n_ser * n_par == 72
q(ED, "LED, photodiode and solar cell", "Intermediate", "numerical",
  "Each solar cell of a certain type gives 0.50 V and 2.0 A at its operating point in sunlight. A panel is to supply "
  "12 V and 6.0 A at the same operating point. Arranging the cells in identical series strings connected in "
  "parallel, the least number of cells needed is:",
  *opt("72", ["24", "27", "3"], "D"),
  "Cells in series add voltages; identical strings in parallel add currents",
  "Each string must give 12 V, so it needs 12/0.50 = 24 cells in series and carries 2.0 A. To deliver 6.0 A, "
  "three such strings are joined in parallel.",
  ["Cells per string = 12/0.50 = 24", "Strings = 6.0/2.0 = 3", "Total = 24 × 3 = 72"],
  why="24 gives the right voltage but only 2.0 A. 27 adds the two numbers instead of multiplying. 3 gives the right "
      "current but only 0.50 V.",
  ncert=SEC + "optoelectronic junction devices (solar cell)", seconds=50, rc=True)

nD, ni = 1e22, 1e16
nh = ni ** 2 / nD
close(nh, 1e10)
close(nD / nh, 1e12)
q(ED, "Semiconductors", "Intermediate", "numerical",
  "Silicon with an intrinsic carrier concentration of 1.0 × 10¹⁶ m⁻³ is doped with 1.0 × 10²² m⁻³ donor atoms, all "
  "of which are ionised. In thermal equilibrium, the ratio of the concentration of majority carriers to that of "
  "minority carriers is about:",
  *opt("10¹²", ["10⁶", "10²²", "10⁻¹²"], "B"),
  "n_e ≈ N_D for n-type; mass-action law n_e n_h = n_i²",
  "The donors supply n_e ≈ 10²² m⁻³ electrons (majority carriers). The hole concentration is then fixed by "
  "n_e n_h = n_i².",
  ["n_e ≈ 1.0 × 10²² m⁻³", "n_h = (10¹⁶)²/10²² = 10¹⁰ m⁻³", "n_e/n_h = 10²²/10¹⁰ = 10¹²"],
  why="10⁶ compares the electrons with the intrinsic concentration instead of with the holes. 10²² is the electron "
      "concentration itself, not a ratio. 10⁻¹² inverts the ratio (minority to majority).",
  ncert=SEC + "extrinsic semiconductor", seconds=50, rc=True)

q(ED, "Semiconductors", "Intermediate", "assertion_reason",
  ar("At absolute zero, n-type silicon conducts electricity well, because its donor atoms supply free electrons.",
     "In n-type silicon, the donor energy level lies only a little (about 0.05 eV) below the bottom of the "
     "conduction band."),
  AR, ar_key(False, True),
  "Ionisation of donors needs (a little) thermal energy",
  "R is true: NCERT shows the donor level just below the conduction band, about 0.05 eV for silicon. But even this "
  "small energy must come from thermal agitation; at 0 K there is none, so the donor electrons stay bound and no "
  "electrons are in the conduction band. The semiconductor behaves as an insulator at 0 K, so A is false.",
  ["R: E_d ≈ 0.05 eV below E_c in Si → true", "A: at 0 K no thermal energy → donors not ionised → insulator → false"],
  why="A is false, so options that take it as true are wrong; at room temperature (kT ≈ 0.026 eV) most donors are "
      "ionised, but not at 0 K.",
  ncert=SEC + "extrinsic semiconductor (energy band diagram)", seconds=45)

exprs = {"A": lambda a, b: NOR(a, b), "B": lambda a, b: NAND(a, b), "C": lambda a, b: OR(a, AND(a, b)),
         "D": lambda a, b: NOT(OR(NOT(a), NOT(b)))}
targets = {"III": lambda a, b: AND(NOT(a), NOT(b)), "II": lambda a, b: OR(NOT(a), NOT(b)), "IV": lambda a, b: a,
           "I": lambda a, b: AND(a, b)}
for k, t in zip("ABCD", ["III", "II", "IV", "I"]):
    assert all(exprs[k](a, b) == targets[t](a, b) for a, b in BITS)
q(ED, "Logic gates", "Intermediate", "match_list",
  ml("Match each logic expression in List-I (inputs A and B) with the expression it is always equal to in List-II. "
     "(Check with truth tables if needed.)",
     ["NOT (A + B), the output of a NOR gate", "NOT (A · B), the output of a NAND gate",
      "A + (A · B)", "NOT ((NOT A) + (NOT B))"],
     ["A · B", "(NOT A) + (NOT B)", "(NOT A) · (NOT B)", "A"]),
  *mlo("A-III, B-II, C-IV, D-I", ["A-II, B-III, C-IV, D-I", "A-III, B-II, C-I, D-IV", "A-III, B-I, C-IV, D-II"],
       "C"),
  "Truth tables of OR, AND, NOT, NAND and NOR",
  "Write the outputs for (A, B) = (0, 0), (0, 1), (1, 0), (1, 1). NOR gives 1, 0, 0, 0, the same as "
  "(NOT A)·(NOT B). NAND gives 1, 1, 1, 0, the same as (NOT A) + (NOT B). A + A·B gives 0, 0, 1, 1, which is just A. "
  "NOT((NOT A) + (NOT B)) gives 0, 0, 0, 1, which is A·B.",
  ["A: 1,0,0,0 → III", "B: 1,1,1,0 → II", "C: 0,0,1,1 → IV", "D: 0,0,0,1 → I"],
  why="The other codes swap the NOR and NAND equivalents (the NOR output is 1 only for 0, 0; the NAND output is 0 "
      "only for 1, 1), or swap A + A·B (equal to A) with A·B.",
  ncert=LOGIC, seconds=90)

Vm_ = 12 * math.sqrt(2)
close(Vm_ / 1000, 0.017, 1e-2)
truth = {"a": True, "b": True, "c": False, "d": True, "e": False}
q(ED, "p-n junction diode and rectifier", "Intermediate", "multi_statement",
  ms("The secondary of a transformer gives 12 V (rms) at 50 Hz. It feeds a half-wave rectifier consisting of an ideal "
     "diode in series with a 1.0 kΩ load resistor. Which of the following statements are correct?",
     ["The peak current through the load is about 17 mA.",
      "The diode conducts during one half of each input cycle.",
      "The current pulses through the load occur at a frequency of 100 Hz.",
      "During the non-conducting half cycle, the reverse voltage across the diode reaches about 17 V.",
      "Doubling the load resistance doubles the frequency of the current pulses."]),
  *mso(truth, "abd", ["abcd", "bde", "acd"], "A"),
  "Half-wave rectification with an ideal diode; peak = √2 × rms",
  "The peak secondary voltage is 12√2 ≈ 17 V, so the peak load current is about 17 V/1.0 kΩ = 17 mA (a true). The "
  "diode conducts only when forward biased, i.e. during one half of each cycle (b true), so there is one pulse per "
  "cycle: 50 pulses per second, not 100 (c false). When the diode is off, no current flows and there is no drop "
  "across the load, so the full secondary voltage, up to about 17 V, appears across the diode (d true). The pulse "
  "frequency is set by the supply, not by the load (e false).",
  ["(a) 12√2/1000 ≈ 17 mA → true", "(b) true", "(c) 50 Hz, not 100 Hz → false", "(d) ≈ 17 V → true",
   "(e) frequency independent of R_L → false"],
  why="Options with (c) give the full-wave pulse frequency; options with (e) let the load change the frequency. "
      "The option without (a) misses the √2 relation between rms and peak values.",
  ncert=SEC + "application of junction diode as a rectifier", seconds=120, rc=True)

q(ED, "Zener diode", "Intermediate", "statement_pair",
  sp("Heavily doping both the p-side and the n-side of a p-n junction makes its depletion region thinner.",
     "Forward biasing a p-n junction decreases the diffusion current of majority carriers across it."),
  SP, sp_key(True, False),
  "Depletion width and doping; effect of forward bias on the barrier",
  "With heavy doping, the charge needed to set up the barrier is found within a short distance of the junction, so "
  "the depletion region is very thin; NCERT uses this to explain the Zener diode (Statement I true). Forward bias "
  "lowers the potential barrier, so many more majority carriers can diffuse across: the diffusion current "
  "increases greatly (Statement II false).",
  ["I: heavy doping → thin depletion layer (Zener diode) → true", "II: lower barrier → more diffusion → false"],
  why="Statement II reverses the effect of forward bias; it is under reverse bias that the diffusion current "
      "falls.",
  ncert=SEC + "p-n junction diode under forward bias; Zener diode", seconds=45)

# ---- Advanced
q(ED, "Semiconductors", "Advanced", "numerical",
  "A silicon crystal (intrinsic carrier concentration 1.5 × 10¹⁶ m⁻³) is doped with 1.0 × 10²¹ m⁻³ donor atoms and "
  "also with 1.0 × 10²¹ m⁻³ acceptor atoms, all of which are ionised. In thermal equilibrium, the electron and hole "
  "concentrations are:",
  *opt("both 1.5 × 10¹⁶ m⁻³", ["both 1.0 × 10²¹ m⁻³", "n_e = 2.0 × 10²¹ m⁻³ and n_h ≈ 1.1 × 10¹¹ m⁻³",
                               "both zero, because the electrons from the donors fill the acceptors"], "D"),
  "Charge neutrality n_e + N_A = n_h + N_D, together with n_e n_h = n_i²",
  "The electrons released by the donors are taken up by the equal number of acceptors, so the dopants compensate "
  "each other. Charge neutrality gives n_e = n_h, and the mass-action law then gives n_e = n_h = n_i: the crystal "
  "behaves like intrinsic silicon as far as carrier numbers are concerned.",
  ["n_e − n_h = N_D − N_A = 0", "n_e n_h = n_i² → n_e = n_h = n_i = 1.5 × 10¹⁶ m⁻³"],
  why="1.0 × 10²¹ m⁻³ for both ignores the recombination of donor electrons with acceptor holes. 2.0 × 10²¹ m⁻³ "
      "adds the two dopings as if both were donors. Zero ignores the thermally generated electron-hole pairs, "
      "which remain at the intrinsic level.",
  ncert=SEC + "intrinsic and extrinsic semiconductors (n_e n_h = n_i²)", seconds=90, rc=True)
assert F(15, 10) ** 2 == F(15, 10) * F(15, 10)

Is_, IL_ = (15 - 9) / 300, 9 / 1500
Iz_ = Is_ - IL_
close(Is_, 0.020)
close(IL_, 0.006)
close(Iz_, 0.014)
close(6 * Is_, 0.120)
q(ED, "Zener diode", "Advanced", "match_list",
  ml("A Zener diode of breakdown voltage 9.0 V is connected through a 300 Ω series resistor to a 15 V DC supply, and "
     "a 1.5 kΩ load resistor is connected across the Zener diode, which is in its breakdown region (take its "
     "voltage as constant). Match each quantity in List-I with its value in List-II.",
     ["Current through the series resistor", "Current through the load", "Current through the Zener diode",
      "Power dissipated in the series resistor"],
     ["6.0 mA", "120 mW", "20 mA", "14 mA"]),
  *mlo("A-III, B-I, C-IV, D-II", ["A-IV, B-I, C-III, D-II", "A-III, B-IV, C-I, D-II", "A-III, B-I, C-II, D-IV"],
       "B"),
  "Zener regulator: V_load = V_Z; I_series = (V_in − V_Z)/R_s; I_Z = I_series − I_load",
  "The Zener holds the load at 9.0 V. The series resistor drops the remaining 6.0 V and carries the total current, "
  "which divides between the load and the Zener.",
  ["I_s = (15 − 9.0)/300 = 20 mA", "I_L = 9.0/1500 = 6.0 mA", "I_Z = 20 − 6.0 = 14 mA",
   "P(series resistor) = 6.0 V × 20 mA = 120 mW"],
  why="The other codes exchange the series and Zener currents (the Zener carries only what the load does not take), "
      "or the load current with the Zener current.",
  ncert=SEC + "Zener diode (as a voltage regulator)", seconds=100, rc=True)

I_led = (5.0 - 2.0) / 150
I_ser = (12 - 5.0) / 100
close(I_led, 0.020)
close(I_ser, 0.070)
close(I_ser - I_led, 0.050)
q(ED, "Zener diode", "Advanced", "numerical",
  "A 12 V DC supply is connected through a 100 Ω resistor to a Zener diode of breakdown voltage 5.0 V, which is in "
  "its breakdown region. Connected across the Zener diode is a branch consisting of an LED in series with a 150 Ω "
  "resistor; the LED has a constant forward voltage of 2.0 V when it conducts. The current through the Zener diode "
  "is:",
  *opt("50 mA", ["70 mA", "20 mA", "90 mA"], "A"),
  "Zener regulator feeding a load; LED forward drop in series with its resistor",
  "The Zener fixes 5.0 V across the LED branch. The LED takes 2.0 V, leaving 3.0 V across its 150 Ω resistor. The "
  "100 Ω resistor drops 12 − 5.0 = 7.0 V and carries the total current, which divides between the LED branch and "
  "the Zener.",
  ["I_LED = (5.0 − 2.0)/150 = 20 mA", "I_total = (12 − 5.0)/100 = 70 mA", "I_Z = 70 − 20 = 50 mA"],
  why="70 mA is the total current in the 100 Ω resistor. 20 mA is the LED current. 90 mA adds the two instead of "
      "subtracting.",
  ncert=SEC + "Zener diode (as a voltage regulator); light emitting diode", seconds=100, rc=True)

def xnor_circ(a, b, last):
    return last(NOR(a, b), AND(a, b))
assert [xnor_circ(a, b, NOR) for a, b in BITS] == [0, 1, 1, 0]
assert [xnor_circ(a, b, OR) for a, b in BITS] == [1, 0, 0, 1]
truth = {"a": True, "b": True, "c": False, "d": True, "e": True}
q(ED, "Logic gates", "Advanced", "multi_statement",
  ms("Inputs A and B are fed both to a NOR gate (output X) and to an AND gate (output Y). X and Y are then fed to a "
     "second NOR gate, whose output is Z. Which of the following statements are correct?",
     ["Z = 0 when A = 0 and B = 0.",
      "Z = 1 when A = 1 and B = 0.",
      "Z = 1 when A = 1 and B = 1.",
      "Z = 1 when A = 0 and B = 1.",
      "If the second NOR gate is replaced by an OR gate, the new output is 1 only when A and B are equal."]),
  *mso(truth, "abde", ["abcd", "ade", "bcde"], "C"),
  "Truth tables of NOR, AND and OR",
  "For (0, 0): X = 1, Y = 0, so Z = NOR(1, 0) = 0 (a true). For (1, 0) and (0, 1): X = 0, Y = 0, so Z = 1 (b, d "
  "true). For (1, 1): X = 0, Y = 1, so Z = 0 (c false). With an OR gate in place of the second NOR, the output is "
  "OR(X, Y): 1 for (0, 0) and (1, 1), 0 otherwise, i.e. 1 only when A = B (e true).",
  ["(0,0): X=1, Y=0 → Z=0", "(0,1), (1,0): X=0, Y=0 → Z=1", "(1,1): X=0, Y=1 → Z=0",
   "OR(X, Y) = 1 for (0,0), (1,1) only"],
  why="Options with (c) forget that the AND output Y = 1 for (1, 1) makes the final NOR output 0. Options leaving "
      "out (b) or (e) miss correct rows of the truth table.",
  ncert=LOGIC, seconds=120)

lam_led = HC / 1.9
close(lam_led, 653, 1e-2)
assert HC / 500 > 1.9 > HC / 800
truth = {"a": True, "b": True, "c": True, "d": True, "e": False}
q(ED, "LED, photodiode and solar cell", "Advanced", "multi_statement",
  ms("A light-emitting diode is made of a semiconductor with a band gap of 1.9 eV. Take hc = 1240 eV nm. Which of the "
     "following statements are correct?",
     ["It emits red light of wavelength about 650 nm.",
      "It emits light only when it is forward biased.",
      "A photodiode made of the same semiconductor would respond to light of wavelength 500 nm.",
      "The light is emitted when electrons and holes recombine near the junction, the energy being released as "
      "photons.",
      "Increasing the forward current makes the LED emit light of a shorter wavelength."]),
  *mso(truth, "abcd", ["abce", "acd", "bcde"], "D"),
  "LED: photon energy ≈ band gap; photodiode responds when hν > E_g",
  "λ ≈ hc/E_g = 1240/1.9 ≈ 650 nm, red (a true). Under forward bias, electrons and holes are injected across the "
  "junction and recombine, releasing their energy as photons (b and d true). A photon of 500 nm carries "
  "1240/500 ≈ 2.5 eV, more than 1.9 eV, so it can create electron-hole pairs in a photodiode of this material (c "
  "true). A larger forward current increases the intensity of the light, not its photon energy; the colour is fixed "
  "by the band gap (e false).",
  ["(a) 1240/1.9 ≈ 653 nm → true", "(b) true", "(c) 2.48 eV > 1.9 eV → true", "(d) true",
   "(e) colour set by E_g → false"],
  why="Options with (e) confuse brightness with colour. Options leaving out (c) forget that photons with more "
      "energy than the band gap are also absorbed.",
  ncert=SEC + "optoelectronic junction devices (photodiode, light emitting diode)", seconds=120, rc=True)

# ================================================================ Experimental Skills (B3 I4 A3)

# ---- Basic
q(EXP, "Vernier calipers and screw gauge", "Basic", "direct",
  "The depth of a small beaker is to be measured with a vernier calipers. The part of the instrument used for this "
  "is:",
  *opt("the thin strip (depth rod) that slides out of the end of the main scale as the vernier is moved",
       ["the lower (main) jaws, placed against the outside of the beaker",
        "the upper jaws, placed against the inner walls of the beaker",
        "the circular scale, turned until the rod touches the bottom"], "C"),
  "Parts of a vernier calipers and their uses",
  "A vernier calipers has three measuring parts: the lower jaws for external dimensions (outer diameter), the "
  "upper jaws for internal dimensions (inner diameter), and a thin strip attached to the vernier, which projects "
  "from the end of the main scale and is used to measure depth. The end of the main scale rests on the rim and the "
  "strip is pushed down until it touches the bottom.",
  ["Outer size → lower jaws; inner size → upper jaws; depth → depth strip"],
  why="The lower jaws measure external dimensions and the upper jaws internal ones. A circular scale belongs to a "
      "screw gauge, not to a vernier calipers.",
  ncert=LAB + "vernier calipers - internal and external diameter and depth of a vessel", seconds=30)

W_eq = 200 * 420 / 4200
close(W_eq, 20)
q(EXP, "Thermal and fluid experiments", "Basic", "numerical",
  "A copper calorimeter of mass 200 g is used in a method-of-mixtures experiment. Taking the specific heat capacity "
  "of copper as 420 J kg⁻¹ K⁻¹ and that of water as 4200 J kg⁻¹ K⁻¹, the water equivalent of the calorimeter is:",
  *opt("20 g", ["200 g", "2.0 g", "2.0 kg"], "A"),
  "Water equivalent W = m s/s_w: the mass of water with the same heat capacity",
  "The calorimeter absorbs as much heat per kelvin as a mass W of water, where W s_w = m s.",
  ["W = 200 g × 420/4200 = 20 g"],
  why="200 g is the actual mass of the calorimeter, not its water equivalent. 2.0 g and 2.0 kg are out by a factor "
      "of 10 or 100 in the arithmetic of the ratio 420/4200 = 1/10.",
  ncert=LAB + "specific heat capacity by the method of mixtures", seconds=30, rc=True)

q(EXP, "Vernier calipers and screw gauge", "Basic", "statement_pair",
  sp("To reduce random error in measuring the diameter of a wire with a screw gauge, readings are taken at several "
     "places along the wire, in two mutually perpendicular directions at each place, and their mean is taken.",
     "The pitch of a screw gauge is the distance moved by its spindle (screw) in one complete rotation of the "
     "circular scale."),
  SP, sp_key(True, True),
  "Use of the screw gauge; pitch and least count",
  "A wire may not be perfectly uniform or perfectly round, so readings at different places and in two perpendicular "
  "directions are averaged (Statement I true). The pitch is the linear distance advanced per full turn; dividing it "
  "by the number of circular-scale divisions gives the least count (Statement II true).",
  ["Statement I: true (standard procedure)", "Statement II: true (definition of pitch)"],
  why="Both are correct descriptions of the screw gauge experiment.",
  ncert=LAB + "screw gauge - diameter of a given wire", seconds=30)

# ---- Intermediate
LC_v = F(1, 100)                          # cm
zero_err = -(10 - 7) * LC_v
obs = F(32, 10) + 4 * LC_v
assert zero_err == F(-3, 100) and obs - zero_err == F(327, 100)
q(EXP, "Vernier calipers and screw gauge", "Intermediate", "numerical",
  "A vernier calipers has a least count of 0.01 cm, its vernier scale having 10 divisions. With the jaws closed, the "
  "zero of the vernier scale lies to the left of the zero of the main scale, and the 7th vernier division coincides "
  "with a main-scale division. While measuring the diameter of a rod, the main-scale reading is 3.2 cm and the 4th "
  "vernier division coincides. The corrected diameter of the rod is:",
  *opt("3.27 cm", ["3.21 cm", "3.17 cm", "3.31 cm"], "B"),
  "Negative zero error = −(N − n) × LC when the vernier zero is to the left; corrected reading = observed − zero "
  "error",
  "With the vernier zero to the left of the main-scale zero, the instrument reads too little: the zero error is "
  "negative. If the nth of N vernier divisions coincides, the zero error is −(N − n) × LC.",
  ["Zero error = −(10 − 7) × 0.01 = −0.03 cm", "Observed reading = 3.2 + 4 × 0.01 = 3.24 cm",
   "Corrected = 3.24 − (−0.03) = 3.27 cm"],
  why="3.21 cm subtracts 0.03 cm, treating the error as positive. 3.17 cm and 3.31 cm take the zero error as "
      "−0.07 cm or +0.07 cm (7 × LC), as if it were read like a positive zero error.",
  ncert=LAB + "vernier calipers (zero error and zero correction)", seconds=75, rc=True)

g2 = 4 * math.pi ** 2 * (1.01 - 0.26) / (2.0 ** 2 - 1.0 ** 2)
close(g2, math.pi ** 2)
close(4 * math.pi ** 2 * 1.01 / 4.0, 9.97, 1e-2)
close(4 * math.pi ** 2 * 0.26 / 1.0, 10.26, 1e-2)
close(4 * math.pi ** 2 * 0.75 / 4.0, 7.40, 1e-2)
q(EXP, "Mechanics experiments", "Intermediate", "numerical",
  "In a simple pendulum experiment, the length of the string is measured from the point of suspension to the hook "
  "of the bob, the radius of the bob being unknown. With a string length of 101 cm the time period is 2.0 s, and "
  "with a string length of 26 cm it is 1.0 s. The value of g obtained from these readings is about:",
  *opt("9.87 m/s²", ["9.97 m/s²", "10.3 m/s²", "7.40 m/s²"], "C"),
  "T = 2π√(L_eff/g), with L_eff = L + x, where x (the unknown hook-to-centre distance) is the same in both "
  "readings",
  "Write T² = (4π²/g)(L + x) for both lengths and subtract: the unknown x cancels, leaving "
  "g = 4π²(L₁ − L₂)/(T₁² − T₂²).",
  ["L₁ − L₂ = 1.01 − 0.26 = 0.75 m", "T₁² − T₂² = 4.0 − 1.0 = 3.0 s²",
   "g = 4π² × 0.75/3.0 = π² ≈ 9.87 m/s²"],
  why="9.97 m/s² and 10.3 m/s² use one reading alone, ignoring the unknown distance from the hook to the centre of "
      "the bob. 7.40 m/s² divides by T₁² instead of by T₁² − T₂².",
  ncert=LAB + "simple pendulum (time period and effective length)", seconds=90, rc=True)

X1_, X2_ = F(6) * F(40, 60), F(6) * F(50, 50)
l_s = 100 * (X1_ + X2_) / (X1_ + X2_ + 6)
assert X1_ == 4 and X2_ == 6 and l_s == F(125, 2)
q(EXP, "Electrical experiments", "Intermediate", "numerical",
  "In a metre bridge experiment with a 6.0 Ω standard resistance in the right gap, the null point is 40.0 cm from "
  "the left end when a resistor X₁ is in the left gap, and 50.0 cm from the left end when a resistor X₂ is in the "
  "left gap instead. When X₁ and X₂ are connected in series in the left gap, the null point is expected at:",
  *opt("62.5 cm", ["90.0 cm", "45.0 cm", "37.5 cm"], "D"),
  "Metre bridge balance X/R = l/(100 − l); resistors in series add",
  "Find X₁ and X₂ from the first two balance points, add them for the series combination, and use the balance "
  "condition again to locate the new null point.",
  ["X₁ = 6.0 × 40/60 = 4.0 Ω; X₂ = 6.0 × 50/50 = 6.0 Ω", "Series: 10.0 Ω",
   "l/(100 − l) = 10/6 → l = 62.5 cm"],
  why="90.0 cm adds the two balancing lengths, but it is the resistances, not the lengths, that add. 45.0 cm "
      "averages the lengths. 37.5 cm is measured from the wrong end (100 − 62.5).",
  ncert=LAB + "metre bridge - verification of the laws of combination (series) of resistances", seconds=75, rc=True)

lcs = {"A": F(1, 10), "B": F(1, 2) / 50, "C": F(1) / 50, "D": F(1, 20)}
assert lcs == {"A": F(1, 10), "B": F(1, 100), "C": F(1, 50), "D": F(1, 20)}
q(EXP, "Vernier calipers and screw gauge", "Intermediate", "match_list",
  ml("Match each measuring instrument in List-I with its least count in List-II.",
     ["Vernier calipers in which 10 vernier divisions equal 9 main-scale divisions of 1 mm",
      "Screw gauge of pitch 0.5 mm with 50 divisions on its circular scale",
      "Screw gauge of pitch 1 mm with 50 divisions on its circular scale",
      "Vernier calipers in which 20 vernier divisions equal 19 main-scale divisions of 1 mm"],
     ["0.01 mm", "0.05 mm", "0.1 mm", "0.02 mm"]),
  *mlo("A-III, B-I, C-IV, D-II", ["A-II, B-I, C-IV, D-III", "A-III, B-IV, C-I, D-II", "A-III, B-I, C-II, D-IV"],
       "A"),
  "Vernier: LC = 1 MSD − 1 VSD; screw gauge: LC = pitch/number of circular-scale divisions",
  "For a vernier, N VSD = (N − 1) MSD gives LC = MSD/N. For a screw gauge, LC = pitch divided by the number of "
  "circular-scale divisions.",
  ["A: 1 mm/10 = 0.1 mm", "B: 0.5 mm/50 = 0.01 mm", "C: 1 mm/50 = 0.02 mm", "D: 1 mm/20 = 0.05 mm"],
  why="The other codes exchange the two verniers (0.1 mm and 0.05 mm) or the two screw gauges (0.01 mm and "
      "0.02 mm), which differ in N or in the pitch.",
  ncert=LAB + "vernier calipers and screw gauge (least count)", seconds=60, rc=True)

# ---- Advanced
r_z = (6.25 - 6.20) / (0.020 - 0.010)
close(r_z, 5.0)
close(6.20 / 0.010, 620)
q(EXP, "Electrical experiments", "Advanced", "numerical",
  "While drawing the reverse-bias characteristic of a Zener diode, a student finds that in the breakdown region the "
  "reverse voltage across the diode is 6.20 V when the reverse current is 10 mA, and 6.25 V when the current is "
  "20 mA. The resistance of the Zener diode in this region, found from the slope of the characteristic, is:",
  *opt("5.0 Ω", ["620 Ω", "312 Ω", "0.20 Ω"], "D"),
  "Dynamic resistance r = ΔV/ΔI from the characteristic curve",
  "In the breakdown region the voltage hardly changes while the current changes a lot; the dynamic resistance is "
  "the ratio of the small change in voltage to the change in current. Its small value is why the Zener diode "
  "regulates voltage well.",
  ["ΔV = 6.25 − 6.20 = 0.05 V", "ΔI = 20 − 10 = 10 mA = 0.010 A", "r = 0.05/0.010 = 5.0 Ω"],
  why="620 Ω and 312 Ω are the static ratios V/I at the two points, not the slope. 0.20 Ω inverts the ratio "
      "(ΔI/ΔV in A/V, i.e. a conductance in siemens).",
  ncert=LAB + "characteristic curves of a Zener diode and its reverse breakdown voltage", seconds=60, rc=True)

ratio_T = F(20, 10) * F(4, 10) / (F(30, 10) * F(5, 10))
assert ratio_T == F(8, 15)
q(EXP, "Thermal and fluid experiments", "Advanced", "numerical",
  "In the capillary-rise experiment, pure water rises 3.0 cm in a clean glass capillary tube of internal radius "
  "0.50 mm. A detergent solution, whose density may be taken equal to that of water, rises 2.0 cm in another clean "
  "capillary of internal radius 0.40 mm. Taking the angle of contact as zero in both cases, the ratio of the surface "
  "tension of the detergent solution to that of pure water is:",
  *opt("8/15", ["2/3", "5/6", "15/8"], "B"),
  "Capillary rise h = 2T/(rρg) for zero angle of contact, so T ∝ hr (same density)",
  "The detergent lowers the surface tension of water, which is the effect this experiment shows. Because the two "
  "tubes are different, both the height and the radius must be used: T = rhρg/2.",
  ["T ∝ h r", "T_det/T_water = (2.0 × 0.40)/(3.0 × 0.50) = 0.80/1.5 = 8/15"],
  why="2/3 compares the heights alone, ignoring the different radii. 5/6 multiplies the height ratio by r₁/r₂ "
      "instead of r₂/r₁ (as if h were proportional to r). 15/8 inverts the ratio; the detergent lowers the surface "
      "tension.",
  ncert=LAB + "surface tension of water by capillary rise and effect of detergents", seconds=90, rc=True)

truth = {"a": True, "b": True, "c": False, "d": True, "e": False}
q(EXP, "Thermal and fluid experiments", "Advanced", "multi_statement",
  ms("In the experiment to find the coefficient of viscosity of a liquid from the terminal velocity of a falling "
     "steel ball, which of the following statements are correct?",
     ["The ball reaches its terminal velocity when its weight is balanced by the upthrust and the viscous drag "
      "together.",
      "For balls of the same material falling through the same liquid, the terminal velocity is proportional to "
      "the square of the radius.",
      "The ball should be dropped close to the wall of the jar so that its fall can be watched clearly.",
      "If the temperature of the liquid rises, the terminal velocity of a given ball increases, because the "
      "viscosity of a liquid decreases with temperature.",
      "The terminal velocity does not depend on the density of the liquid."]),
  *mso(truth, "abd", ["abcd", "abde", "bde"], "C"),
  "Stokes' law: at terminal velocity (4/3)πr³(ρ − σ)g = 6πηrv, so v = 2r²(ρ − σ)g/(9η)",
  "At terminal velocity there is no acceleration: weight = upthrust + viscous force (a true). This gives "
  "v = 2r²(ρ − σ)g/(9η), so v ∝ r² for the same materials (b true) and v depends on the liquid's density σ (e "
  "false). The viscosity of liquids decreases as their temperature rises, so v increases (d true). Stokes' law "
  "holds for a ball moving through a liquid extending far on all sides, so the ball is dropped along the axis, away "
  "from the walls (c false).",
  ["(a) true", "(b) v ∝ r² → true", "(c) the walls disturb the flow → false", "(d) η falls with T → true",
   "(e) v ∝ (ρ − σ) → false"],
  why="Options with (c) contradict the precaution of keeping the ball away from the walls; options with (e) "
      "forget the upthrust term (ρ − σ).",
  ncert=LAB + "coefficient of viscosity by terminal velocity; " + NC11 + "'Mechanical Properties of Fluids', "
              "viscosity", seconds=120)


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
    assert all(31 <= keys[k] <= 37 for k in LETTERS), keys
    texts = [x["question_text"] for x in QS]
    assert len(set(texts)) == len(texts)
    doc = {"schema_version": "1.0", "batch_id": "BATCH_010", "created_at": TODAY,
           "notes": "Package PHY_010_p2: 134 original Physics questions (Current Electricity to Experimental Skills), "
                    "NEET_PHY_002367..002500. Numerical answers recomputed by tools/batch_010/PHY_010_p2.py.",
           "stimuli": [], "questions": QS}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {OUT}: {len(QS)} questions")
    print("difficulty", dict(Counter(x["difficulty"] for x in QS)))
    print("formats", dict(fmts))
    print("keys", dict(sorted(keys.items())))


if __name__ == "__main__":
    main()
