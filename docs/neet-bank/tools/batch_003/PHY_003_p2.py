"""Builder for batches/parts/BATCH_003_PHY_p2.json (package PHY_003_p2 of BATCH_003).

Physics, 118 original questions, NEET_PHY_000633..NEET_PHY_000750: Current Electricity, Magnetic Effects of Current
and Magnetism, Electromagnetic Induction and Alternating Currents, Electromagnetic Waves, Optics, Dual Nature of
Matter and Radiation, Atoms and Nuclei, Electronic Devices, Experimental Skills.

Every numerical answer is recomputed below with an assert next to its question; multi-statement, assertion-reason
and statement-pair keys are derived from truth tables; the plan quota, format mix and answer-key balance are
asserted before anything is written. If any assert fails, nothing is written.

    python tools/batch_003/PHY_003_p2.py        (run from docs/neet-bank)
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
PLAN = ROOT / "batches" / "plans" / "BATCH_003_plan.json"
OUT = ROOT / "batches" / "parts" / "BATCH_003_PHY_p2.json"
PACKAGE = "PHY_003_p2"
FIRST_ID = 633
COUNT = 118

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
mu_e, V_w, L_w = 4.0e-3, 3.0, 2.0
close(mu_e * V_w / L_w, 6.0e-3)
close(mu_e * V_w, 1.2e-2)
close(mu_e * V_w * L_w, 2.4e-2)
close(mu_e / (V_w / L_w), 2.67e-3, 1e-2)
q(CE, "Drift velocity and Ohm's law", "Basic", "numerical",
  "The free electrons in a metal wire 2.0 m long have a mobility of 4.0 × 10⁻³ m² V⁻¹ s⁻¹. A potential difference "
  "of 3.0 V is maintained between the ends of the wire. The drift speed of the electrons is:",
  *opt("6.0 × 10⁻³ m/s", ["1.2 × 10⁻² m/s", "2.4 × 10⁻² m/s", "2.7 × 10⁻³ m/s"], "A"),
  "Mobility: µ = v_d/E, so v_d = µE with E = V/L",
  "Mobility is the drift speed per unit electric field. The field in a uniform wire is the potential difference "
  "divided by the length.",
  ["E = V/L = 3.0/2.0 = 1.5 V/m", "v_d = µE = 4.0 × 10⁻³ × 1.5 = 6.0 × 10⁻³ m/s"],
  why="1.2 × 10⁻² m/s multiplies µ by V instead of by E. 2.4 × 10⁻² m/s multiplies by the length instead of "
      "dividing. 2.7 × 10⁻³ m/s divides µ by E.",
  ncert=NC + "'Current Electricity', mobility", seconds=35, rc=True)

I_par = F(3, 2) / (F(14, 10) + F(4, 10) / 4)
assert I_par == 1
assert F(6) / (F(14, 10) + F(16, 10)) == 2
close(1.5 / 1.8, 0.83, 1e-2)
assert F(6) / (F(14, 10) + F(1, 10)) == 4
q(CE, "Cells, emf and internal resistance", "Basic", "numerical",
  "Four identical cells, each of emf 1.5 V and internal resistance 0.4 Ω, are connected in parallel (all positive "
  "terminals joined together). A 1.4 Ω resistor is connected across the combination. The current in the resistor "
  "is:",
  *opt("1.0 A", ["2.0 A", "0.83 A", "4.0 A"], "B"),
  "Identical cells in parallel: emf ε, internal resistance r/n",
  "Connecting identical cells in parallel does not raise the emf; it only divides the internal resistance by the "
  "number of cells.",
  ["ε_eq = 1.5 V, r_eq = 0.4/4 = 0.1 Ω", "I = ε_eq/(R + r_eq) = 1.5/(1.4 + 0.1) = 1.0 A"],
  why="2.0 A treats the cells as being in series (6 V, 1.6 Ω). 0.83 A uses the internal resistance of one cell "
      "(0.4 Ω) instead of 0.1 Ω. 4.0 A adds the emfs as in series but divides the internal resistance as in "
      "parallel.",
  ncert=NC + "'Current Electricity', cells in series and in parallel", seconds=40, rc=True)

R_ring = 12
assert (F(R_ring, 2) * F(R_ring, 2)) / (F(R_ring, 2) + F(R_ring, 2)) == 3
q(CE, "Combination of resistors", "Basic", "numerical",
  "A uniform wire of resistance 12 Ω is bent into a complete circle. The resistance between two diametrically "
  "opposite points of the circle is:",
  *opt("3 Ω", ["6 Ω", "12 Ω", "24 Ω"], "C"),
  "Two halves of the ring in parallel",
  "Between two diametrically opposite points, the ring is two semicircular wires, each of half the total "
  "resistance, joined in parallel.",
  ["Each semicircle: 12/2 = 6 Ω", "Parallel: 6 × 6/(6 + 6) = 3 Ω"],
  why="6 Ω counts only one semicircle. 12 Ω is the resistance of the straight wire. 24 Ω adds the two halves as if "
      "in series with the whole wire.",
  ncert=NC + "'Current Electricity', combination of resistors in series and parallel", seconds=30, rc=True)

P_tx, Rc, V_tx = 400e3, 5, 20e3
I_tx = P_tx / V_tx
assert I_tx == 20 and I_tx ** 2 * Rc == 2000
close(V_tx ** 2 / Rc, 80e6)
assert I_tx * Rc == 100 and (P_tx / 20) ** 2 * Rc == 2e9
q(CE, "Drift velocity and Ohm's law", "Basic", "numerical",
  "A power station delivers 400 kW to a distant town through transmission cables whose total resistance is 5 Ω. "
  "The power is transmitted at 20 kV. The power lost as heat in the cables is:",
  *opt("2 kW", ["80 MW", "100 W", "2000 MW"], "D"),
  "Power loss in connecting wires: P_loss = I²R_c with I = P/V",
  "The current in the cables is fixed by the power delivered and the transmission voltage; the heat produced in "
  "the cables depends on this current and on their resistance. The 20 kV is not the voltage across the cables.",
  ["I = P/V = 400 × 10³/(20 × 10³) = 20 A", "P_loss = I²R_c = 20² × 5 = 2000 W = 2 kW"],
  why="80 MW uses V²/R_c, treating the full 20 kV as if it were across the cables. 100 W is I × R_c, which is the "
      "voltage drop in the cables (100 V), not a power. 2000 MW forgets to convert 20 kV to volts (I = 20 000 A).",
  ncert=NC + "'Current Electricity', electrical energy and power (power loss in transmission)", seconds=45,
  rc=True)

q(CE, "Drift velocity and Ohm's law", "Basic", "direct",
  "A copper wire is at room temperature and no electric field is applied to it. The average velocity of all the "
  "free electrons in the wire is:",
  *opt("zero, because their thermal velocities are randomly directed",
       ["of the order of 10⁵ m/s, directed along the length of the wire",
        "of the order of 10⁻⁴ m/s, directed along the length of the wire",
        "equal to the speed of light in copper"], "B"),
  "Random thermal motion of free electrons",
  "Free electrons move with large thermal speeds, but their directions are random, so their velocities average to "
  "zero. Only when a field is applied does a small drift velocity get superposed on this random motion.",
  ["Thermal speeds are large but randomly directed", "Average of randomly directed velocities = 0",
   "With no field, there is no drift and no current"],
  why="10⁵ m/s is the order of the thermal speed of an individual electron, not the average velocity. 10⁻⁴ m/s "
      "is a typical drift speed, which exists only when a field is applied. The speed of light is unrelated.",
  ncert=NC + "'Current Electricity', drift of electrons and the origin of resistivity", seconds=25)

q(CE, "Drift velocity and Ohm's law", "Basic", "match_list",
  ml("Match each quantity in List-I with its expression in List-II for a metallic conductor (n = number density of "
     "free electrons, e = electronic charge, m = electron mass, τ = relaxation time, E = electric field, "
     "A = cross-sectional area, v_d = drift speed).",
     ["Magnitude of the drift velocity", "Current in the conductor", "Resistivity", "Conductivity"],
     ["ne²τ/m", "eEτ/m", "m/(ne²τ)", "neAv_d"]),
  *mlo("A-II, B-IV, C-III, D-I",
       ["A-II, B-IV, C-I, D-III", "A-IV, B-II, C-III, D-I", "A-III, B-IV, C-II, D-I"], "C"),
  "Drude picture of conduction",
  "An electron accelerates as eE/m between collisions, giving an average drift eEτ/m. The charge crossing a "
  "section per second is neAv_d. Substituting gives J = (ne²τ/m)E, so σ = ne²τ/m and ρ = 1/σ = m/(ne²τ).",
  ["v_d = eEτ/m → A-II", "I = neAv_d → B-IV", "ρ = m/(ne²τ) → C-III", "σ = ne²τ/m → D-I"],
  why="Swapping C and D confuses resistivity with its reciprocal. The other codes put a current or a drift "
      "speed against the wrong formula.",
  ncert=NC + "'Current Electricity', drift of electrons and the origin of resistivity", seconds=50)

I_op = F(6 - 2, 1 + 1 + 2)
assert I_op == 1 and 2 + I_op * 1 == 3 and 2 - I_op * 1 == 1 and 6 - I_op * 1 == 5
q(CE, "Cells, emf and internal resistance", "Intermediate", "numerical",
  "A cell of emf 6 V and internal resistance 1 Ω and a cell of emf 2 V and internal resistance 1 Ω are connected "
  "in a single loop with a 2 Ω resistor. The cells oppose each other: the positive terminal of one is joined to "
  "the positive terminal of the other. The potential difference across the terminals of the 2 V cell is:",
  *opt("3 V", ["1 V", "2 V", "5 V"], "D"),
  "A cell being charged: V = ε + Ir",
  "The net emf drives current in the direction set by the 6 V cell, so current is forced into the 2 V cell at its "
  "positive terminal; that cell is being charged and its terminal voltage exceeds its emf.",
  ["I = (6 − 2)/(1 + 1 + 2) = 1 A", "2 V cell is charged: V = ε + Ir = 2 + 1 × 1 = 3 V"],
  why="1 V uses V = ε − Ir, which applies to a cell that is discharging. 2 V ignores the drop across the internal "
      "resistance. 5 V is the terminal voltage of the 6 V cell.",
  ncert=NC + "'Current Electricity', cells, emf, internal resistance", seconds=60, rc=True)

# metre bridge: X/R = 40/60; (X + 5)/R = 50/50
R_mb = 5 / (1 - F(40, 60))
X_mb = F(40, 60) * R_mb
assert R_mb == 15 and X_mb == 10
assert X_mb / R_mb == F(40, 60) and (X_mb + 5) / R_mb == 1
X_wrong = 5 / (F(50, 40) - 1)
assert X_wrong == 20
q(CE, "Wheatstone and metre bridge", "Intermediate", "numerical",
  "In a metre bridge, a resistance X is in the left gap and a resistance R in the right gap, and the null point is "
  "40.0 cm from the left end of the wire. When a 5 Ω resistor is connected in series with X in the left gap (R "
  "unchanged), the null point moves to 50.0 cm from the left end. The value of X is:",
  *opt("10 Ω", ["15 Ω", "20 Ω", "5 Ω"], "B"),
  "Metre bridge balance: (left resistance)/(right resistance) = l/(100 − l)",
  "Write the balance condition for both positions of the null point and solve the two equations for X and R.",
  ["First balance: X/R = 40/60 = 2/3", "Second balance: (X + 5)/R = 50/50 = 1 → R = X + 5",
   "X = (2/3)(X + 5) → X/3 = 10/3 → X = 10 Ω (and R = 15 Ω)"],
  why="15 Ω is the value of R. 20 Ω comes from taking X/(X + 5) = 40/50, i.e. using the two balance lengths as "
      "if R were not needed. 5 Ω assumes X equals the added resistor.",
  ncert=NC + "'Current Electricity', meter bridge", seconds=75, rc=True)

R_cut = F(10, 5) / 5
assert R_cut == F(2, 5)
assert F(10, 5) == 2 and 10 * 5 == 50 and F(10, 125) == F(2, 25)
q(CE, "Combination of resistors", "Intermediate", "numerical",
  "A uniform wire of resistance 10 Ω is cut into five pieces of equal length, and the five pieces are then "
  "connected in parallel. The resistance of the combination is:",
  *opt("0.4 Ω", ["2 Ω", "50 Ω", "0.08 Ω"], "A"),
  "Cutting a wire divides its resistance; parallel combination of equal resistors",
  "Each piece has one-fifth of the length and hence one-fifth of the resistance. Five equal resistors in parallel "
  "have one-fifth of the resistance of one of them.",
  ["Each piece: 10/5 = 2 Ω", "Five 2 Ω pieces in parallel: 2/5 = 0.4 Ω (in general R/n²)"],
  why="2 Ω is the resistance of a single piece. 50 Ω multiplies by 5 instead of dividing. 0.08 Ω divides by 5 "
      "three times (R/n³).",
  ncert=NC + "'Current Electricity', combination of resistors", seconds=40, rc=True)

I_ab, R1_ab, E_ab, R2_ab = 2, 2, 3, 1
VA_minus_VB = I_ab * R1_ab - E_ab + I_ab * R2_ab
assert VA_minus_VB == 3
assert I_ab * R1_ab + E_ab + I_ab * R2_ab == 9 and I_ab * (R1_ab + R2_ab) == 6
q(CE, "Kirchhoff's laws", "Intermediate", "numerical",
  "In a part of a circuit, a steady current of 2 A flows from point A to point B through the following elements in "
  "series, in this order: a 2 Ω resistor, a cell of emf 3 V and negligible internal resistance whose positive "
  "terminal faces B, and a 1 Ω resistor. The potential difference V_A − V_B is:",
  *opt("3 V", ["9 V", "6 V", "−3 V"], "C"),
  "Potential changes along a branch (Kirchhoff's loop rule)",
  "Walk from A to B in the direction of the current. The potential falls by IR across each resistor and rises by ε "
  "on crossing the cell from its negative to its positive terminal.",
  ["V_A − 2 × 2 + 3 − 2 × 1 = V_B", "V_A − V_B = 4 − 3 + 2 = 3 V"],
  why="9 V treats the cell as a drop instead of a rise. 6 V ignores the cell. −3 V has the right size but the "
      "wrong sign: A is at the higher potential.",
  ncert=NC + "'Current Electricity', Kirchhoff's rules", seconds=60, rc=True)

q(CE, "Drift velocity and Ohm's law", "Intermediate", "assertion_reason",
  ar("When a switch is closed, a bulb several metres away lights up almost at once, although the drift speed of the "
     "free electrons in the connecting wires is only of the order of 1 mm/s.",
     "An electric field is set up throughout the circuit almost instantly, so the free electrons everywhere in the "
     "wires start drifting at practically the same time."),
  AR, ar_key(True, True, explains=True),
  "Establishment of current in a circuit",
  "The current in the filament does not wait for electrons from the switch to arrive. The electric field spreads "
  "through the wires at nearly the speed of light, and electrons already present in every part of the circuit "
  "begin to drift together. A is true and R correctly explains it.",
  ["Drift speed ~ 1 mm/s, yet the bulb lights at once → A true",
   "The field is established along the whole circuit almost instantly → R true",
   "Electrons in the filament start moving immediately because of the field → R explains A"],
  why="R is exactly the reason the bulb does not have to wait for electrons to travel from the switch, so B, C and "
      "D are wrong.",
  ncert=NC + "'Current Electricity', drift of electrons (worked example on drift speed)", seconds=45)

q(CE, "Drift velocity and Ohm's law", "Intermediate", "assertion_reason",
  ar("Doubling the potential difference across a metal wire kept at a constant temperature doubles its resistance.",
     "At constant temperature, the current through a metal wire is directly proportional to the potential "
     "difference across it."),
  AR, ar_key(False, True),
  "Ohm's law: resistance of an ohmic conductor",
  "For a metal at constant temperature, I ∝ V (Ohm's law, R is true). Doubling V therefore doubles I, and "
  "R = V/I stays the same. A is false.",
  ["I ∝ V at constant temperature → R true", "R = V/I unchanged when V and I both double → A false"],
  why="A is false, so options A, B and C (which need A to be true) are wrong.",
  ncert=NC + "'Current Electricity', Ohm's law", seconds=35)

q(CE, "Drift velocity and Ohm's law", "Intermediate", "statement_pair",
  sp("Electric current is a vector quantity, since it has a direction of flow.",
     "The relation J = σE, between the current density J and the electric field E, is an equivalent form of Ohm's "
     "law."),
  SP, sp_key(False, True),
  "Current as a scalar; Ohm's law in terms of J and E",
  "Current has a sense along a wire but does not add as a vector (currents meeting at a junction add "
  "algebraically), so it is a scalar; current density J is the vector. Writing V = IR for a small element of "
  "length l and area A gives E l = J A (ρl/A), i.e. E = ρJ or J = σE, which is Ohm's law in another form.",
  ["Currents add algebraically at a junction → scalar → Statement I false",
   "V = IR → El = (JA)(ρl/A) → J = σE → Statement II true"],
  why="Statement I is false and Statement II is true; every other combination is wrong.",
  ncert=NC + "'Current Electricity', electric current; Ohm's law", seconds=40)

mb_truth = {"a": True, "b": True, "c": True, "d": False, "e": False}
q(CE, "Wheatstone and metre bridge", "Intermediate", "multi_statement",
  ms("Which of the following statements about the metre bridge are correct?",
     ["It works on the principle of the Wheatstone bridge.",
      "The resistors and the wire are connected by thick metal strips whose resistance can be neglected.",
      "The position of the null point does not depend on the emf of the cell used.",
      "At the null point, the current through the galvanometer is maximum.",
      "The resistance per unit length of the bridge wire must be known to calculate the unknown resistance."]),
  *mso(mb_truth, "abc", ["abd", "ace", "bcd"], "A"),
  "Metre bridge: balance condition and construction",
  "The metre bridge is a Wheatstone bridge in which two arms are the two segments of a uniform wire. At balance "
  "no current flows through the galvanometer, and X/R = (resistance of l)/(resistance of 100 − l) = l/(100 − l), "
  "because the resistance per unit length cancels. The balance condition contains only resistances, so it does "
  "not depend on the cell's emf.",
  ["(a) True: Wheatstone principle", "(b) True: thick copper strips of negligible resistance",
   "(c) True: balance condition has no emf in it", "(d) False: galvanometer current is zero at the null point",
   "(e) False: resistance per unit length cancels in the ratio"],
  why="Every other option includes (d) or (e), which are false, or leaves out a true statement.",
  ncert=NC + "'Current Electricity', meter bridge", seconds=60)

# shorted bridge: B and D merged into node 2
v_sb = solve_network(3, [(0, 2, 1), (0, 2, 2), (2, 1, 2), (2, 1, 1)], {0: 6, 1: 0})
VM = v_sb[2]
I_P, I_Q = (6 - VM) / 1, VM / 2
I_R, I_S = (6 - VM) / 2, VM / 1
assert VM == 3 and I_P - I_Q == F(3, 2) and I_S - I_R == F(3, 2)
q(CE, "Kirchhoff's laws", "Advanced", "numerical",
  "Resistors P = 1 Ω and Q = 2 Ω are joined in series to form one branch, and R = 2 Ω and S = 1 Ω in series form a "
  "second branch. Both branches are connected across an ideal 6 V battery, with P and R joined to its positive "
  "terminal. The P–Q junction (point B) and the R–S junction (point D) are then joined by a wire of negligible "
  "resistance. The current in this wire is:",
  *opt("1.5 A, flowing from B to D", ["1.5 A, flowing from D to B", "zero", "3 A, flowing from B to D"], "B"),
  "Kirchhoff's junction and loop rules for an unbalanced bridge with a shorting wire",
  "The wire puts B and D at the same potential, so P and R are in parallel between the positive terminal and B/D, "
  "and Q and S are in parallel between B/D and the negative terminal. Find the common potential, then apply the "
  "junction rule at B.",
  ["P ∥ R = 2/3 Ω and Q ∥ S = 2/3 Ω, so B and D are at 3 V",
   "Current into B through P = 3/1 = 3 A; current out of B through Q = 3/2 = 1.5 A",
   "Junction rule at B: 3 − 1.5 = 1.5 A leaves B through the wire, towards D",
   "Check at D: 3/2 = 1.5 A in through R plus 1.5 A from the wire = 3 A out through S = 3/1 A"],
  why="'From D to B' gets the direction wrong. Zero would need P/Q = R/S (a balanced bridge), but 1/2 ≠ 2/1. "
      "3 A is the current in P, not the share that crosses the wire.",
  ncert=NC + "'Current Electricity', Kirchhoff's rules", seconds=110, rc=True)

X_rho = F(2) * 60 / 40
rho_w = float(X_rho) * math.pi * (0.40e-3) ** 2 / (4 * 0.500)
assert X_rho == 3
close(rho_w, 7.54e-7)
close(float(F(2) * 40 / 60) * math.pi * (0.40e-3) ** 2 / (4 * 0.5), 3.35e-7)
close(3 * math.pi * (0.40e-3) ** 2 / 0.5, 3.02e-6)
close(3 * (0.40e-3) ** 2 / 0.5, 9.6e-7)
q(CE, "Wheatstone and metre bridge", "Advanced", "numerical",
  "In a metre bridge, a wire of length 50.0 cm and diameter 0.40 mm is connected in the left gap and a standard "
  "resistance of 2.0 Ω in the right gap. The null point is 60.0 cm from the left end of the bridge wire. The "
  "resistivity of the material of the wire is about:",
  *opt("7.5 × 10⁻⁷ Ω m", ["3.4 × 10⁻⁷ Ω m", "3.0 × 10⁻⁶ Ω m", "9.6 × 10⁻⁷ Ω m"], "A"),
  "Metre bridge balance, then ρ = RA/L with A = πd²/4",
  "First find the resistance of the wire from the balance length, then convert it to resistivity using the "
  "wire's own length and cross-sectional area.",
  ["X/2.0 = 60/40 → X = 3.0 Ω", "A = πd²/4 = π(0.40 × 10⁻³)²/4 = 1.26 × 10⁻⁷ m²",
   "ρ = XA/L = 3.0 × 1.26 × 10⁻⁷/0.500 ≈ 7.5 × 10⁻⁷ Ω m"],
  why="3.4 × 10⁻⁷ Ω m inverts the bridge ratio (X = 4/3 Ω). 3.0 × 10⁻⁶ Ω m uses the diameter as the radius. "
      "9.6 × 10⁻⁷ Ω m takes the area as d², leaving out π/4.",
  ncert=NC + "'Current Electricity', meter bridge; resistivity", seconds=100, rc=True)

sols = [R for R in (F(1), F(4)) if (F(12) / (R + 2)) ** 2 * R == 16]
assert sols == [1, 4]
# R^2 - 5R + 4 = 0 has exactly these two roots
assert all(R * R - 5 * R + 4 == 0 for R in sols)
assert (F(12) / 11) ** 2 * 9 != 16 and (F(12) / 9) ** 2 * 7 != 16 and (F(12) / 4) ** 2 * 2 != 16
q(CE, "Cells, emf and internal resistance", "Advanced", "numerical",
  "A battery of emf 12 V and internal resistance 2 Ω is connected across an external resistor R. The power "
  "dissipated in R is 16 W. The value of R is:",
  *opt("either 1 Ω or 4 Ω", ["9 Ω", "7 Ω", "2 Ω"], "D"),
  "Power delivered to an external resistor: P = ε²R/(R + r)²",
  "Below the maximum power (which occurs at R = r), every value of power is delivered for two different load "
  "resistances, one smaller and one larger than r.",
  ["16 = 144R/(R + 2)² → (R + 2)² = 9R", "R² − 5R + 4 = 0 → (R − 1)(R − 4) = 0",
   "R = 1 Ω or 4 Ω (check: 1 Ω → I = 4 A, P = 16 W; 4 Ω → I = 2 A, P = 16 W)"],
  shortcut="Maximum power here is ε²/4r = 18 W at R = 2 Ω; 16 W is below it, so expect two roots whose product "
           "is r² = 4.",
  why="9 Ω uses P = ε²/R and ignores the internal resistance. 7 Ω subtracts r from that wrong value. 2 Ω is the "
      "load for maximum power (18 W), not 16 W.",
  ncert=NC + "'Current Electricity', cells, emf, internal resistance; electrical power", seconds=110, rc=True)

sq = [(0, 1, 4), (1, 2, 4), (2, 3, 4), (3, 0, 4), (0, 2, 4)]
assert equivalent_resistance(4, sq, 1, 3) == 4
assert equivalent_resistance(4, sq, 0, 2) == 2
v_sq = solve_network(4, sq, {1: 1, 3: 0})
assert v_sq[0] == v_sq[2]
q(CE, "Combination of resistors", "Advanced", "numerical",
  "Five resistors, each of 4 Ω, are connected to form a square ABCD (one resistor on each side) together with its "
  "diagonal AC. The equivalent resistance between the corners B and D is:",
  *opt("4 Ω", ["2 Ω", "8/3 Ω", "8 Ω"], "C"),
  "Symmetry: points at equal potential carry no current between them",
  "With the source across B and D, the network is symmetric about the line BD, so A and C are at the same "
  "potential and the diagonal AC carries no current. It can be removed.",
  ["V_A = V_C by symmetry → no current in AC",
   "Remaining: path B–A–D (8 Ω) in parallel with path B–C–D (8 Ω)", "R_BD = 8 × 8/(8 + 8) = 4 Ω"],
  why="2 Ω is the resistance between A and C (the ends of the diagonal), not between B and D. 8/3 Ω wrongly puts "
      "the diagonal in parallel with one 8 Ω path. 8 Ω counts only one path.",
  ncert=NC + "'Current Electricity', combination of resistors; Wheatstone bridge", seconds=80, rc=True)

eps, r = F(1), F(1)
series = lambda cells: (sum(c[0] for c in cells), sum(c[1] for c in cells))
parallel_same = lambda c, n: (c[0], c[1] / n)
cell = (eps, r)
mA = series([cell] * 4)
mB = parallel_same(cell, 4)
mC = parallel_same(series([cell] * 2), 2)
mD = series([parallel_same(cell, 3), cell])
assert mA == (4, 4) and mB == (1, F(1, 4)) and mC == (2, 1) and mD == (2, F(4, 3))
q(CE, "Cells, emf and internal resistance", "Advanced", "match_list",
  ml("Four identical cells, each of emf ε and internal resistance r, are grouped as described in List-I. Match "
     "each grouping with the emf and internal resistance of the combination in List-II.",
     ["All four in series", "All four in parallel",
      "Two pairs, each pair of two cells in series, the two pairs then joined in parallel",
      "Three cells in parallel, and this group joined in series with the fourth cell"],
     ["2ε and r", "4ε and 4r", "2ε and 4r/3", "ε and r/4"]),
  *mlo("A-II, B-IV, C-I, D-III",
       ["A-II, B-IV, C-III, D-I", "A-IV, B-II, C-I, D-III", "A-II, B-I, C-IV, D-III"], "B"),
  "Cells in series and in parallel",
  "In series, emfs and internal resistances add. Identical cells in parallel keep the emf of one cell and divide "
  "the internal resistance by their number.",
  ["Series of four: 4ε, 4r → A-II", "Parallel of four: ε, r/4 → B-IV",
   "Each pair: 2ε, 2r; two pairs in parallel: 2ε, r → C-I",
   "Three in parallel: ε, r/3; in series with one cell: 2ε, r/3 + r = 4r/3 → D-III"],
  why="The other codes swap the series and parallel results or give the two-pair grouping the internal "
      "resistance of the 3 + 1 grouping.",
  ncert=NC + "'Current Electricity', cells in series and in parallel", seconds=90, rc=True)

R1p, R2p, Vb = 6, 3, 12
assert Vb ** 2 * R1p / (R1p + R2p) ** 2 > Vb ** 2 * R2p / (R1p + R2p) ** 2  # (a) series: larger R hotter
assert Vb ** 2 / R2p > Vb ** 2 / R1p  # (b) parallel: smaller R hotter
assert Vb ** 2 / R1p + Vb ** 2 / R2p > Vb ** 2 / R1p  # (c)
assert Vb / (R1p + R2p) < Vb / R1p  # (d) false: series addition reduces current
assert F(Vb ** 2, 2 * R1p) == F(Vb ** 2, R1p) / 2  # (e) two identical bulbs together use half, not a quarter
pw_truth = {"a": True, "b": True, "c": True, "d": False, "e": False}
q(CE, "Combination of resistors", "Advanced", "multi_statement",
  ms("Resistors are connected across an ideal battery (no internal resistance) whose emf stays constant, and the "
     "resistances do not change with temperature. Which of the following statements are correct?",
     ["When two resistors R₁ > R₂ are in series across the battery, more heat is produced per second in R₁.",
      "When the same two resistors are in parallel across the battery, more heat is produced per second in R₂.",
      "Connecting one more resistor in parallel across the battery increases the total power drawn from it.",
      "Connecting one more resistor in series with a resistor already across the battery increases the current "
      "drawn from it.",
      "Two identical bulbs in series across the battery together consume one-fourth of the power that one bulb "
      "consumes when connected alone across it."]),
  *mso(pw_truth, "abc", ["abe", "bcd", "acd"], "C"),
  "Power in series and parallel combinations: P = I²R and P = V²/R",
  "In series the current is common, so P = I²R is larger for the larger resistance. In parallel the voltage is "
  "common, so P = V²/R is larger for the smaller resistance. Adding a parallel branch lowers the total "
  "resistance and raises the power V²/R_eq; adding a series resistor raises the total resistance and lowers "
  "the current.",
  ["(a) True: same I, P = I²R", "(b) True: same V, P = V²/R",
   "(c) True: R_eq falls, P = V²/R_eq rises", "(d) False: current falls",
   "(e) False: together they take V²/2R, i.e. half (each bulb alone takes one-fourth)"],
  why="Options with (d) or (e) include a false statement; the remaining option leaves out a true one.",
  ncert=NC + "'Current Electricity', combination of resistors; electrical power", seconds=90)


# ================================================================ Magnetic Effects of Current and Magnetism (B6 I7 A6)
MU0 = 4 * math.pi * 1e-7
B_sol = MU0 * (500 / 0.50) * 2
close(B_sol, 2.51e-3)
close(MU0 * 500 * 2, 1.26e-3)
close(MU0 * 500 * 2 * 0.50, 6.28e-4)
close(MU0 * 1 * 2, 2.51e-6)
q(MAG, "Ampere's law", "Basic", "numerical",
  "A long air-cored solenoid is 50 cm long and has 500 turns. It carries a current of 2.0 A. Taking "
  "µ₀ = 4π × 10⁻⁷ T m A⁻¹, the magnetic field well inside the solenoid, near its middle, is about:",
  *opt("2.5 × 10⁻³ T", ["1.3 × 10⁻³ T", "6.3 × 10⁻⁴ T", "2.5 × 10⁻⁶ T"], "B"),
  "Field inside a long solenoid: B = µ₀nI, n = turns per unit length",
  "Ampere's law applied to a rectangular loop half inside the solenoid gives a uniform field µ₀nI inside, where n "
  "is the number of turns per metre.",
  ["n = 500/0.50 = 1000 turns per metre", "B = µ₀nI = 4π × 10⁻⁷ × 1000 × 2.0 = 8π × 10⁻⁴ ≈ 2.5 × 10⁻³ T"],
  why="1.3 × 10⁻³ T uses the total number of turns N instead of n. 6.3 × 10⁻⁴ T multiplies by the length "
      "instead of dividing. 2.5 × 10⁻⁶ T takes n as 1 turn per millimetre but treats it as 1 per metre.",
  ncert=NC + "'Moving Charges and Magnetism', the solenoid", seconds=35, rc=True)

F_e = 1.6e-19 * 3e6 * 0.2 * math.sin(math.radians(30))
close(F_e, 4.8e-14)
close(1.6e-19 * 3e6 * 0.2, 9.6e-14)
close(1.6e-19 * 3e6 * 0.2 * math.cos(math.radians(30)), 8.3e-14, 1e-2)
q(MAG, "Force on charges and conductors", "Basic", "numerical",
  "An electron moves with a speed of 3.0 × 10⁶ m/s in a direction making an angle of 30° with a uniform magnetic "
  "field of 0.20 T. Taking e = 1.6 × 10⁻¹⁹ C, the magnitude of the magnetic force on the electron is:",
  *opt("4.8 × 10⁻¹⁴ N", ["9.6 × 10⁻¹⁴ N", "8.3 × 10⁻¹⁴ N", "zero"], "C"),
  "Magnetic force on a moving charge: F = qvB sin θ",
  "Only the component of velocity perpendicular to the field contributes to the magnetic force.",
  ["F = evB sin 30° = 1.6 × 10⁻¹⁹ × 3.0 × 10⁶ × 0.20 × 0.5", "F = 4.8 × 10⁻¹⁴ N"],
  why="9.6 × 10⁻¹⁴ N leaves out sin θ. 8.3 × 10⁻¹⁴ N uses cos 30°. Zero would be true only if the velocity were "
      "parallel or antiparallel to the field.",
  ncert=NC + "'Moving Charges and Magnetism', magnetic force", seconds=30, rc=True)

tau_m = 2.0 * 0.15 * math.sin(math.radians(30))
close(tau_m, 0.15)
close(2.0 * 0.15, 0.30)
close(2.0 * 0.15 * math.cos(math.radians(30)), 0.26, 1e-2)
q(MAG, "Magnetic dipole and bar magnet", "Basic", "numerical",
  "A bar magnet of magnetic moment 2.0 A m² is held in a uniform magnetic field of 0.15 T with its axis at 30° to "
  "the field. The magnitude of the torque acting on it is:",
  *opt("0.15 N m", ["0.30 N m", "0.26 N m", "zero, because the field is uniform"], "D"),
  "Torque on a magnetic dipole: τ = m × B, |τ| = mB sin θ",
  "A uniform field exerts no net force on a magnet but does exert a torque that tends to align m with B.",
  ["τ = mB sin θ = 2.0 × 0.15 × sin 30°", "τ = 0.30 × 0.5 = 0.15 N m"],
  why="0.30 N m leaves out sin θ. 0.26 N m uses cos 30°. A uniform field gives zero net force, not zero torque.",
  ncert=NC + "'Magnetism and Matter', the bar magnet: the dipole in a uniform magnetic field", seconds=30, rc=True)

m_coil = 100 * 0.40 * math.pi * 0.05 ** 2
close(m_coil, 0.314)
close(0.40 * math.pi * 0.05 ** 2, 3.14e-3)
close(100 * 0.40 * math.pi * 0.10 ** 2, 1.26)
close(100 * 0.40 * 2 * math.pi * 0.05, 12.6)
q(MAG, "Torque on loop and galvanometer", "Basic", "numerical",
  "A flat circular coil of 100 turns, each of radius 5.0 cm, carries a current of 0.40 A. The magnitude of its "
  "magnetic dipole moment is about:",
  *opt("0.31 A m²", ["3.1 × 10⁻³ A m²", "1.26 A m²", "12.6 A m²"], "A"),
  "Magnetic moment of a coil: m = NIA",
  "Each turn is a current loop of moment IA; the N turns add.",
  ["A = πr² = π(0.05)² = 7.85 × 10⁻³ m²", "m = NIA = 100 × 0.40 × 7.85 × 10⁻³ ≈ 0.31 A m²"],
  why="3.1 × 10⁻³ A m² leaves out the number of turns. 1.26 A m² uses 10 cm (the diameter) as the radius. "
      "12.6 A m² uses the circumference 2πr in place of the area.",
  ncert=NC + "'Moving Charges and Magnetism', the magnetic dipole moment of a current loop", seconds=35, rc=True)

q(MAG, "Magnetic dipole and bar magnet", "Basic", "direct",
  "The magnetic field lines of a bar magnet form closed loops. Inside the magnet, the field lines run:",
  *opt("from the south pole to the north pole",
       ["from the north pole to the south pole", "nowhere, because the magnetic field inside a magnet is zero",
        "radially outwards from the centre of the magnet"], "B"),
  "Magnetic field lines are continuous closed loops",
  "Outside the magnet the lines leave the north pole and enter the south pole. Since they form closed loops and do "
  "not start or end at the poles, inside the magnet they continue from the south pole to the north pole.",
  ["Outside: N → S", "Lines are closed loops → inside: S → N"],
  why="N to S describes the lines outside the magnet. The field inside is not zero. Radial lines would require "
      "a magnetic monopole at the centre.",
  ncert=NC + "'Magnetism and Matter', the magnetic field lines", seconds=25)

q(MAG, "Biot-Savart law", "Basic", "direct",
  "According to the Biot–Savart law, the magnetic field dB produced at a point P by a small current element I dl is "
  "zero when:",
  *opt("P lies on the line along which the current element points",
       ["the line joining the element to P is perpendicular to dl",
        "P is very close to the current element",
        "the current in the element is steady"], "C"),
  "Biot–Savart law: dB = (µ₀/4π) I dl × r/r³, magnitude ∝ sin θ",
  "The field of a current element is proportional to sin θ, where θ is the angle between dl and the displacement "
  "r to the point. On the line of the element θ = 0° or 180°, so dB = 0.",
  ["|dB| = (µ₀/4π) I dl sin θ/r²", "P on the line of dl → θ = 0 or 180° → dB = 0"],
  why="When r is perpendicular to dl, sin θ = 1 and the field is largest. Close to the element the field is "
      "large, not zero. A steady current does produce a field.",
  ncert=NC + "'Moving Charges and Magnetism', magnetic field due to a current element, Biot–Savart law",
  seconds=30)

k_t, N_g, A_g, B_g, I_g = 1.0e-4, 100, 2.0e-4, 0.50, 2e-3
phi_g = N_g * A_g * B_g * I_g / k_t
close(phi_g, 0.20)
close(N_g * 2.0e-2 * B_g * I_g / k_t, 20)
close(N_g * A_g * B_g / k_t * 1e-3, 0.10)
close(k_t / (N_g * A_g * B_g * I_g), 5.0)
q(MAG, "Torque on loop and galvanometer", "Intermediate", "numerical",
  "A moving-coil galvanometer has a coil of 100 turns, each of area 2.0 cm², in a radial magnetic field of "
  "0.50 T. The torsional constant of its spring is 1.0 × 10⁻⁴ N m rad⁻¹. The steady deflection of the coil for a "
  "current of 2.0 mA is:",
  *opt("0.20 rad", ["20 rad", "0.10 rad", "5.0 rad"], "A"),
  "Moving-coil galvanometer: kφ = NIAB",
  "In the radial field the deflecting torque NIAB is balanced by the restoring torque kφ of the spring, so the "
  "deflection is proportional to the current.",
  ["φ = NIAB/k", "A = 2.0 cm² = 2.0 × 10⁻⁴ m²",
   "φ = 100 × 2.0 × 10⁻³ × 2.0 × 10⁻⁴ × 0.50/(1.0 × 10⁻⁴) = 0.20 rad"],
  why="20 rad converts cm² to m² with 10⁻² instead of 10⁻⁴. 0.10 rad is the current sensitivity, the deflection "
      "per milliampere. 5.0 rad inverts the ratio (k/NIAB).",
  ncert=NC + "'Moving Charges and Magnetism', the moving coil galvanometer", seconds=55, rc=True)

r_ratio = 2 ** (1 / 3)
# axial: 2m/r1^3 = equatorial: m/r2^3 -> (r1/r2)^3 = 2
close(r_ratio ** 3, 2)
close(2 / r_ratio ** 3, 1 / 1 ** 3)
q(MAG, "Magnetic dipole and bar magnet", "Intermediate", "numerical",
  "A short bar magnet produces magnetic fields of equal magnitude at a point P₁ on its axis and at a point P₂ on "
  "its equatorial line (the perpendicular bisector of its axis). The ratio of the distances of P₁ and P₂ from the "
  "centre of the magnet, r₁ : r₂, is:",
  *opt("2^(1/3) : 1", ["2 : 1", "1 : 2^(1/3)", "√2 : 1"], "C"),
  "Fields of a short magnet: axial B = µ₀(2m)/(4πr³), equatorial B = µ₀m/(4πr³)",
  "At the same distance the axial field is twice the equatorial field, so the axial point must be farther away "
  "for the two to be equal; the fields fall as 1/r³.",
  ["2m/r₁³ = m/r₂³", "(r₁/r₂)³ = 2", "r₁ : r₂ = 2^(1/3) : 1 ≈ 1.26 : 1"],
  why="2 : 1 forgets the cube. 1 : 2^(1/3) puts the axial point nearer, which would make its field even larger. "
      "√2 : 1 treats the field as falling off as 1/r².",
  ncert=NC + "'Magnetism and Matter', the bar magnet as an equivalent solenoid", seconds=55, rc=True)

B_w = MU0 * 5 / (2 * math.pi * 0.10)
F_w = 1.6e-19 * 4e6 * B_w
close(B_w, 1e-5)
close(F_w, 6.4e-18)
close(1.6e-19 * 4e6 * MU0 * 5 / (math.pi * 0.10), 1.28e-17)
# direction: wire along +x, electron at +y moving +x; B at +y is +z; F = (-e) v x B
vx, Bz = (1, 0, 0), (0, 0, 1)
cross = (vx[1] * Bz[2] - vx[2] * Bz[1], vx[2] * Bz[0] - vx[0] * Bz[2], vx[0] * Bz[1] - vx[1] * Bz[0])
assert tuple(-c for c in cross) == (0, 1, 0)  # +y: away from the wire
q(MAG, "Force on charges and conductors", "Intermediate", "numerical",
  "A long straight wire carries a steady current of 5.0 A. An electron moves parallel to the wire, in the same "
  "direction as the current, at a distance of 10 cm from it, with a speed of 4.0 × 10⁶ m/s. Taking "
  "µ₀ = 4π × 10⁻⁷ T m A⁻¹ and e = 1.6 × 10⁻¹⁹ C, the magnetic force on the electron is:",
  *opt("6.4 × 10⁻¹⁸ N, directed away from the wire",
       ["6.4 × 10⁻¹⁸ N, directed towards the wire", "1.28 × 10⁻¹⁷ N, directed away from the wire", "zero"], "B"),
  "Field of a straight wire B = µ₀I/(2πd); force on a moving charge F = qv × B",
  "The field of the wire circles round it, so it is perpendicular to the electron's velocity. A positive charge "
  "moving along the current would be pulled towards the wire (like parallel currents); the negative electron is "
  "pushed away.",
  ["B = µ₀I/(2πd) = 2 × 10⁻⁷ × 5.0/0.10 = 1.0 × 10⁻⁵ T",
   "F = evB = 1.6 × 10⁻¹⁹ × 4.0 × 10⁶ × 1.0 × 10⁻⁵ = 6.4 × 10⁻¹⁸ N",
   "Electron moving along the current ≡ conventional current opposite to the wire's → repelled, away from wire"],
  why="'Towards the wire' is the direction for a positive charge. 1.28 × 10⁻¹⁷ N uses µ₀I/(πd), twice the field. "
      "Zero assumes the field is along the wire, but it circles the wire and is perpendicular to the velocity.",
  ncert=NC + "'Moving Charges and Magnetism', magnetic field of a straight wire; Lorentz force", seconds=70, rc=True)

Rw, Iw = 1.0, 1.0
B_in = MU0 * Iw * (Rw / 2) / (2 * math.pi * Rw ** 2)
B_out = MU0 * Iw / (2 * math.pi * 2 * Rw)
close(B_in / B_out, 1)
q(MAG, "Ampere's law", "Intermediate", "numerical",
  "A long straight cylindrical wire of radius R carries a steady current spread uniformly over its cross-section. "
  "The ratio of the magnetic field at a distance R/2 from its axis to the field at a distance 2R from its axis is:",
  *opt("1 : 1", ["1 : 4", "4 : 1", "1 : 2"], "D"),
  "Ampere's law inside and outside a long current-carrying cylinder",
  "Inside, a circular Amperian loop of radius r encloses the fraction r²/R² of the current, so B ∝ r. Outside, it "
  "encloses all of it, so B ∝ 1/r.",
  ["Inside: B(r) = µ₀Ir/(2πR²) → B(R/2) = µ₀I/(4πR)", "Outside: B(r) = µ₀I/(2πr) → B(2R) = µ₀I/(4πR)",
   "Ratio = 1 : 1"],
  why="1 : 4 and 4 : 1 use the 1/r law (or the r law) at both points. 1 : 2 uses B ∝ r inside but forgets that "
      "the field outside falls off with distance.",
  ncert=NC + "'Moving Charges and Magnetism', Ampere's circuital law", seconds=60, rc=True)

q(MAG, "Force on charges and conductors", "Intermediate", "statement_pair",
  sp("A charged particle at rest in a uniform magnetic field B experiences a magnetic force of magnitude qB.",
     "The magnetic force on a moving charged particle is directed along its velocity."),
  SP, sp_key(False, False),
  "Magnetic part of the Lorentz force: F = q(v × B)",
  "The magnetic force depends on the velocity: F = qvB sin θ, which is zero for v = 0. Because it is a cross "
  "product, the force is perpendicular to v (and to B), never along v.",
  ["v = 0 → F = 0 → Statement I false", "F = q(v × B) ⊥ v → Statement II false"],
  why="Both statements are false, so every other option is wrong.",
  ncert=NC + "'Moving Charges and Magnetism', magnetic force", seconds=35)

q(MAG, "Magnetic dipole and bar magnet", "Intermediate", "assertion_reason",
  ar("When a bar magnet is cut into two halves by a cut perpendicular to its length, each half is a complete magnet "
     "with a north pole and a south pole.",
     "Isolated magnetic north and south poles (magnetic monopoles) exist and can be separated by cutting a magnet."),
  AR, ar_key(True, False),
  "Magnetic poles always occur in pairs",
  "Cutting a bar magnet gives two smaller magnets, each with both poles, however many times it is cut. This is "
  "because isolated magnetic poles (monopoles) are not known to exist. A is true; R is false.",
  ["Each piece is a magnet with N and S → A true", "Monopoles do not exist → R false"],
  why="R is false, so options A, B and D are wrong.",
  ncert=NC + "'Magnetism and Matter', the bar magnet", seconds=30)

amp_truth = {"a": True, "b": True, "c": False, "d": True, "e": False}
q(MAG, "Ampere's law", "Intermediate", "multi_statement",
  ms("Which of the following statements are correct?",
     ["The magnetic field well inside a long solenoid is nearly uniform and parallel to its axis.",
      "The magnetic field at points in the open space outside an ideal toroid is zero.",
      "For a fixed number of turns per unit length and a fixed current, the field inside a long solenoid "
      "increases as the solenoid is made longer.",
      "Ampere's circuital law, ∮B·dl = µ₀I, holds for steady currents.",
      "Ampere's circuital law is valid only for circular closed paths."]),
  *mso(amp_truth, "abd", ["abc", "bde", "acd"], "B"),
  "Ampere's circuital law and its applications",
  "Ampere's law holds for any closed loop around steady currents; circles are chosen only when symmetry makes the "
  "integral easy. For a long solenoid B = µ₀nI depends only on n and I, not on the length. Outside an ideal "
  "toroid an Amperian loop encloses no net current, so the field there is zero.",
  ["(a) True", "(b) True: no net current enclosed outside", "(c) False: B = µ₀nI, independent of length",
   "(d) True: the law is for steady currents", "(e) False: any closed path"],
  why="The other options include (c) or (e), which are false, or leave out a true statement.",
  ncert=NC + "'Moving Charges and Magnetism', Ampere's circuital law; the solenoid; the toroid", seconds=55)

B_loop = MU0 / (2 * 1.0)
B_line = MU0 / (2 * math.pi * 1.0)
close(B_loop + B_line, (MU0 / 2) * (1 + 1 / math.pi))
q(MAG, "Biot-Savart law", "Advanced", "numerical",
  "A long, straight, insulated wire carrying a steady current I is bent, in one plane, so that it forms a single "
  "complete circular loop of radius R. The straight parts of the wire lie along one line that touches the loop at "
  "the point where the loop begins and ends, and the wire turns smoothly into the loop and out of it without any "
  "kink, so that the current continues along the straight line in its original direction. The magnitude of the "
  "magnetic field at the centre of the loop is:",
  *opt("(µ₀I/2R)(1 + 1/π)", ["(µ₀I/2R)(1 − 1/π)", "µ₀I/(2R)", "(µ₀I/2R)(1 + 2/π)"], "A"),
  "Superposition of the fields of a circular loop and a long straight wire",
  "The straight wire is effectively an infinitely long wire at distance R from the centre. Because the wire runs "
  "smoothly into the loop, the current at the point of contact has the same direction in the loop as in the "
  "straight part, so both produce fields at the centre in the same direction (perpendicular to the plane).",
  ["Loop: B₁ = µ₀I/(2R)", "Straight wire at distance R: B₂ = µ₀I/(2πR)",
   "Same direction → B = µ₀I/(2R) + µ₀I/(2πR) = (µ₀I/2R)(1 + 1/π)"],
  why="(1 − 1/π) assumes the two fields oppose, which would need the loop current to reverse direction at the "
      "contact point. µ₀I/(2R) ignores the straight wire. (1 + 2/π) uses µ₀I/(πR) for the straight wire.",
  ncert=NC + "'Moving Charges and Magnetism', field on the axis of a circular loop; Ampere's law (straight wire)",
  seconds=80, rc=True)

F_net = 2e-7 * 10 * 2 * 0.10 * (1 / 0.05 - 1 / 0.15)
close(F_net, 5.33e-6)
close(2e-7 * 10 * 2 * 0.10 * (1 / 0.05 + 1 / 0.15), 1.07e-5, 1e-2)
close(2e-7 * 10 * 2 * 0.10 / 0.05, 8.0e-6)
q(MAG, "Force on charges and conductors", "Advanced", "numerical",
  "A long straight wire carries a current of 10 A. A rectangular loop carrying a current of 2.0 A lies in the same "
  "plane, with its two 10 cm long sides parallel to the wire at distances of 5.0 cm and 15 cm from it. In the side "
  "nearer the wire, the loop current is in the same direction as the current in the wire. Taking "
  "µ₀ = 4π × 10⁻⁷ T m A⁻¹, the net magnetic force on the loop is:",
  *opt("5.3 × 10⁻⁶ N, towards the wire",
       ["5.3 × 10⁻⁶ N, away from the wire", "1.07 × 10⁻⁵ N, towards the wire", "8.0 × 10⁻⁶ N, towards the wire"],
       "C"),
  "Force between parallel currents: F = µ₀I₁I₂L/(2πd)",
  "The two sides perpendicular to the wire carry opposite currents at the same distances, so their forces cancel. "
  "The near side (current parallel to the wire's) is attracted; the far side (antiparallel) is repelled, but less "
  "strongly because it is farther away.",
  ["Near side: F₁ = 2 × 10⁻⁷ × 10 × 2.0 × 0.10/0.05 = 8.0 × 10⁻⁶ N, towards the wire",
   "Far side: F₂ = 2 × 10⁻⁷ × 10 × 2.0 × 0.10/0.15 = 2.67 × 10⁻⁶ N, away from the wire",
   "Net: 8.0 − 2.67 = 5.3 × 10⁻⁶ N, towards the wire"],
  why="'Away from the wire' reverses the net direction. 1.07 × 10⁻⁵ N adds the two forces although they are "
      "opposite. 8.0 × 10⁻⁶ N counts only the near side.",
  ncert=NC + "'Moving Charges and Magnetism', force between two parallel currents", seconds=90, rc=True)

B_ax = 1e-7 * 2 * 1.0 / 0.10 ** 3
B_eq = 1e-7 * 1.0 / 0.10 ** 3
close(B_ax, 2e-4)
close(B_eq, 1e-4)
close(math.hypot(B_ax, B_eq), 2.24e-4, 1e-2)
close(math.hypot(B_ax, B_ax), 2.83e-4, 1e-2)
q(MAG, "Magnetic dipole and bar magnet", "Advanced", "numerical",
  "Two identical short bar magnets, each of magnetic moment 1.0 A m², lie in a horizontal plane with their centres "
  "20 cm apart on a line XY. Magnet 1 lies along XY and magnet 2 is perpendicular to XY. Ignoring all other "
  "magnetic fields and taking µ₀/4π = 10⁻⁷ T m A⁻¹, the magnitude of the resultant magnetic field at the midpoint "
  "of the line joining their centres is about:",
  *opt("2.2 × 10⁻⁴ T", ["3.0 × 10⁻⁴ T", "1.0 × 10⁻⁴ T", "2.8 × 10⁻⁴ T"], "D"),
  "Axial and equatorial fields of a short magnet; vector addition",
  "The midpoint is 10 cm from each centre. It lies on the axis of magnet 1 and on the equatorial line of magnet 2. "
  "The axial field of magnet 1 is along XY; the equatorial field of magnet 2 is antiparallel to its own moment, "
  "i.e. perpendicular to XY. The two fields are at right angles.",
  ["Magnet 1 (axial): B₁ = 10⁻⁷ × 2 × 1.0/(0.10)³ = 2.0 × 10⁻⁴ T, along XY",
   "Magnet 2 (equatorial): B₂ = 10⁻⁷ × 1.0/(0.10)³ = 1.0 × 10⁻⁴ T, perpendicular to XY",
   "B = √(2.0² + 1.0²) × 10⁻⁴ = √5 × 10⁻⁴ ≈ 2.2 × 10⁻⁴ T"],
  why="3.0 × 10⁻⁴ T adds the magnitudes as if the fields were parallel. 1.0 × 10⁻⁴ T subtracts them. "
      "2.8 × 10⁻⁴ T treats the midpoint as an axial point of both magnets.",
  ncert=NC + "'Magnetism and Matter', the bar magnet as an equivalent solenoid", seconds=100, rc=True)

q(MAG, "Biot-Savart law", "Advanced", "statement_pair",
  sp("Like the electrostatic field of a point charge, the magnetic field of a current element is long-range and "
     "falls off as the inverse square of the distance from it.",
     "The electrostatic field of a point charge is along the line joining the charge to the field point, whereas "
     "the magnetic field of a current element is perpendicular to the plane containing the element and the line "
     "joining it to the field point."),
  SP, sp_key(True, True),
  "Comparison of the Biot–Savart law with Coulomb's law",
  "dB = (µ₀/4π) I dl × r/r³ has magnitude ∝ 1/r², like Coulomb's law, so both fields are long-range. The "
  "electrostatic field is radial, along r, but dB is along dl × r, perpendicular to the plane of dl and r. There "
  "is also an angle factor (sin θ) in the magnetic case.",
  ["Both ∝ 1/r² → Statement I true", "E along r; dB along dl × r → Statement II true"],
  why="Both statements are true, so every other option is wrong.",
  ncert=NC + "'Moving Charges and Magnetism', Biot–Savart law (comparison with Coulomb's law)", seconds=45)

qq, mm, BB, vv = 2.0, 3.0, 0.5, 4.0
rr = mm * vv / (qq * BB)
close(qq ** 2 * BB ** 2 * rr ** 2 / (2 * mm), 0.5 * mm * vv ** 2)
close(2 * math.pi * rr / vv, 2 * math.pi * mm / (qq * BB))
q(MAG, "Force on charges and conductors", "Advanced", "match_list",
  ml("A particle of charge q and mass m moves with speed v at right angles to a uniform magnetic field B, in a "
     "circle of radius r. Match each quantity in List-I with its expression in List-II.",
     ["Radius of the circle", "Time period of revolution", "Frequency of revolution", "Kinetic energy"],
     ["q²B²r²/(2m)", "2πm/(qB)", "mv/(qB)", "qB/(2πm)"]),
  *mlo("A-III, B-II, C-IV, D-I",
       ["A-III, B-IV, C-II, D-I", "A-I, B-II, C-IV, D-III", "A-III, B-II, C-I, D-IV"], "C"),
  "Circular motion of a charge in a magnetic field",
  "The magnetic force supplies the centripetal force: qvB = mv²/r, so r = mv/(qB). The period 2πr/v = 2πm/(qB) "
  "is independent of speed, and the frequency is its reciprocal. Using v = qBr/m in ½mv² gives the kinetic "
  "energy in terms of r.",
  ["qvB = mv²/r → r = mv/(qB) → A-III", "T = 2πr/v = 2πm/(qB) → B-II", "ν = 1/T = qB/(2πm) → C-IV",
   "v = qBr/m → K = ½mv² = q²B²r²/(2m) → D-I"],
  why="Swapping B and C confuses the period with the frequency. The other codes put the radius or the kinetic "
      "energy against the wrong expression.",
  ncert=NC + "'Moving Charges and Magnetism', motion in a magnetic field", seconds=70, rc=True)

loop_truth = {"a": True, "b": True, "c": True, "d": False, "e": False}
assert (math.pi * 2.0 ** 2) / (math.pi * 1.0 ** 2) == 4  # (d) doubling radius quadruples m
q(MAG, "Biot-Savart law", "Advanced", "multi_statement",
  ms("Which of the following statements about a plane circular loop of radius R carrying a steady current I are "
     "correct?",
     ["For a fixed current, the magnetic field at the centre of the loop is inversely proportional to R.",
      "At points on the axis far from the loop (distance x ≫ R), the field falls off as 1/x³.",
      "The loop behaves as a magnetic dipole of moment IA, where A is the area of the loop.",
      "Doubling the radius of the loop, with the current unchanged, doubles its magnetic moment.",
      "The magnetic field at the centre of the loop lies in the plane of the loop."]),
  *mso(loop_truth, "abc", ["abd", "bce", "acd"], "A"),
  "Field of a circular current loop; the loop as a magnetic dipole",
  "On the axis, B = µ₀IR²/[2(R² + x²)^(3/2)]. At the centre (x = 0) this is µ₀I/(2R) ∝ 1/R; for x ≫ R it becomes "
  "µ₀IR²/(2x³) = µ₀(2m)/(4πx³) with m = IπR², the field of a dipole. The field at the centre is along the axis, "
  "perpendicular to the plane of the loop.",
  ["(a) True: B = µ₀I/(2R)", "(b) True: B ≈ µ₀IR²/(2x³)", "(c) True: m = IA",
   "(d) False: A = πR² → m becomes 4 times", "(e) False: B at centre is perpendicular to the plane"],
  why="Every other option includes (d) or (e), which are false, or leaves out a true statement.",
  ncert=NC + "'Moving Charges and Magnetism', magnetic field on the axis of a circular current loop; the magnetic "
             "dipole", seconds=70)


# ================================================================ Electromagnetic Induction and AC (B4 I6 A4)
NL = 50 * 0.5 * 0.02 * math.sin(math.radians(60))
close(NL, 0.433)
close(50 * 0.5 * 0.02 * math.cos(math.radians(60)), 0.25)
close(50 * 0.5 * 0.02, 0.50)
close(0.5 * 0.02 * math.sin(math.radians(60)), 8.66e-3)
q(EMI, "Faraday's and Lenz's laws", "Basic", "numerical",
  "A flat coil of 50 turns, each of area 0.020 m², is placed in a uniform magnetic field of 0.50 T. The field "
  "makes an angle of 60° with the plane of the coil. The total magnetic flux linked with the coil is about:",
  *opt("0.43 Wb", ["0.25 Wb", "0.50 Wb", "8.7 × 10⁻³ Wb"], "C"),
  "Magnetic flux: Φ = BA cos θ, θ measured from the normal to the coil",
  "The angle in Φ = BA cos θ is between B and the area vector (the normal). A field at 60° to the plane is at "
  "30° to the normal. Flux linkage counts every turn.",
  ["Angle with the normal = 90° − 60° = 30°", "Flux per turn = 0.50 × 0.020 × cos 30° = 8.66 × 10⁻³ Wb",
   "Flux linkage = 50 × 8.66 × 10⁻³ ≈ 0.43 Wb"],
  why="0.25 Wb uses the 60° angle (with the plane) in cos θ. 0.50 Wb ignores the angle. 8.7 × 10⁻³ Wb is the flux "
      "through one turn only.",
  ncert=NC + "'Electromagnetic Induction', magnetic flux", seconds=40, rc=True)

XL2 = 2 * math.pi * 50 * (0.2 / math.pi)
close(XL2, 20)
close(220 / XL2, 11)
close(220 * math.sqrt(2) / XL2, 15.6, 1e-2)
close(220 / (XL2 * math.sqrt(2)), 7.8, 1e-2)
close(220 / (math.pi * 50 * 0.2 / math.pi), 22)
q(EMI, "AC: rms, reactance and impedance", "Basic", "numerical",
  "An ideal inductor of inductance (0.2/π) H is connected to a 220 V (rms), 50 Hz AC supply. The rms current in "
  "the circuit is:",
  *opt("11 A", ["15.6 A", "7.8 A", "22 A"], "A"),
  "Inductive reactance X_L = ωL = 2πfL; I_rms = V_rms/X_L",
  "A pure inductor limits the current through its reactance, which grows with frequency.",
  ["X_L = 2π × 50 × (0.2/π) = 20 Ω", "I_rms = 220/20 = 11 A"],
  why="15.6 A uses the peak voltage (220√2) with an rms answer. 7.8 A divides the rms value by √2 again. 22 A "
      "uses πfL (half the reactance).",
  ncert=NC + "'Alternating Current', AC voltage applied to an inductor", seconds=35, rc=True)

eps0 = 100 * 0.20 * 0.050 * (2 * math.pi * 50)
close(eps0, 314.16)
close(100 * 0.20 * 0.050 * 50, 50)
close(0.20 * 0.050 * 2 * math.pi * 50, 3.14)
close(eps0 / math.sqrt(2), 222, 1e-2)
q(EMI, "AC generator and transformer", "Basic", "numerical",
  "The coil of an AC generator has 100 turns, each of area 0.050 m², and rotates at 50 revolutions per second "
  "about an axis perpendicular to a uniform magnetic field of 0.20 T. The peak emf induced in the coil is about:",
  *opt("314 V", ["50 V", "3.14 V", "222 V"], "D"),
  "AC generator: ε = NBAω sin ωt, peak ε₀ = NBAω",
  "The flux through the rotating coil varies sinusoidally, and the peak emf is NBAω with ω = 2πν.",
  ["ω = 2π × 50 = 100π rad/s", "ε₀ = NBAω = 100 × 0.20 × 0.050 × 100π = 100π ≈ 314 V"],
  why="50 V uses ω = 50 rad/s (the revolutions per second) instead of 2πν. 3.14 V leaves out the number of turns. "
      "222 V is the rms value, not the peak.",
  ncert=NC + "'Electromagnetic Induction', AC generator", seconds=40, rc=True)

q(EMI, "Faraday's and Lenz's laws", "Basic", "direct",
  "A closed coil is placed near various sources. In which of the following situations is NO emf induced in the "
  "closed coil?",
  *opt("A neighbouring coil carries a steady current, and both coils are at rest",
       ["A bar magnet is moved towards the coil",
        "The steady current in a neighbouring coil is switched off",
        "The coil is rotated in a uniform magnetic field about an axis in its plane, perpendicular to the field"],
       "B"),
  "Faraday's law: an emf is induced only when the magnetic flux linked with the coil changes",
  "A steady current in a stationary neighbouring coil produces a constant flux through the coil, so no emf is "
  "induced. Moving a magnet, switching a current off and rotating the coil all change the flux.",
  ["Steady current + no motion → constant flux → no emf", "Every other case changes the flux → emf induced"],
  why="Each of the other situations changes the flux linked with the coil (by motion of the magnet, by change of "
      "current, or by change of orientation), so an emf is induced.",
  ncert=NC + "'Electromagnetic Induction', the experiments of Faraday and Henry", seconds=30)

R5, XC5, V5 = 30, 40, 200
Z5 = math.hypot(R5, XC5)
I5 = V5 / Z5
assert Z5 == 50 and I5 == 4 and I5 * R5 == 120 and I5 * XC5 == 160
close(200 * 3 / 7, 85.7, 1e-2)
assert 200 / 40 * 30 == 150 and 200 / 40 * 40 == 200
q(EMI, "AC: rms, reactance and impedance", "Intermediate", "numerical",
  "A 30 Ω resistor and a capacitor of reactance 40 Ω are connected in series to a 200 V (rms) AC supply. The rms "
  "voltages across the resistor and across the capacitor are, respectively:",
  *opt("120 V and 160 V", ["86 V and 114 V", "160 V and 120 V", "150 V and 200 V"], "B"),
  "Series RC circuit: Z = √(R² + X_C²); voltages add as phasors",
  "Find the current from the impedance; each element's rms voltage is the current times its own resistance or "
  "reactance. The two voltages are 90° out of phase, so they do not add up to 200 V arithmetically.",
  ["Z = √(30² + 40²) = 50 Ω, I = 200/50 = 4 A", "V_R = 4 × 30 = 120 V, V_C = 4 × 40 = 160 V",
   "Check: √(120² + 160²) = 200 V"],
  why="86 V and 114 V share 200 V in the ratio 3 : 4 as if the voltages added arithmetically. 160 V and 120 V are "
      "swapped. 150 V and 200 V take the current as 200/40 = 5 A, ignoring the resistor in the impedance.",
  ncert=NC + "'Alternating Current', series LCR circuit (phasor diagram)", seconds=60, rc=True)

P6 = 220 * 5.0 * math.cos(math.radians(60))
Iw6 = 5.0 * math.sin(math.radians(60))
close(P6, 550)
close(Iw6, 4.33)
close(220 * 5.0 * math.sin(math.radians(60)), 952.6, 1e-2)
q(EMI, "LCR resonance and power", "Intermediate", "numerical",
  "In an AC circuit, the rms voltage is 220 V and the rms current is 5.0 A, the current lagging behind the voltage "
  "by 60°. The average power consumed and the wattless component of the current are, respectively:",
  *opt("550 W and 4.3 A", ["550 W and 2.5 A", "950 W and 2.5 A", "1100 W and 4.3 A"], "C"),
  "Average power P = V_rms I_rms cos φ; wattless current I_rms sin φ",
  "Resolve the current into a component in phase with the voltage (I cos φ), which carries the power, and a "
  "component 90° out of phase (I sin φ), which consumes no average power: the wattless current.",
  ["P = 220 × 5.0 × cos 60° = 550 W", "Wattless current = 5.0 × sin 60° ≈ 4.3 A"],
  why="2.5 A is I cos φ, the power-carrying (wattful) component. 950 W uses sin φ for the power. 1100 W leaves "
      "out the power factor.",
  ncert=NC + "'Alternating Current', power in AC circuit: the power factor (wattless current)", seconds=55,
  rc=True)

VR7, VL7, VC7 = 40, 80, 50
V7 = math.hypot(VR7, VL7 - VC7)
assert V7 == 50
close(math.sqrt(VR7 ** 2 + VL7 ** 2 + VC7 ** 2), 102.5, 1e-2)
q(EMI, "AC: rms, reactance and impedance", "Intermediate", "numerical",
  "In a series LCR circuit connected to an AC source, the rms voltages across the resistor, the inductor and the "
  "capacitor are 40 V, 80 V and 50 V respectively. The rms voltage of the source is:",
  *opt("50 V", ["170 V", "70 V", "102 V"], "D"),
  "Phasor addition: V = √[V_R² + (V_L − V_C)²]",
  "V_L and V_C are opposite in phase, so they partly cancel; their difference is at 90° to V_R.",
  ["V_L − V_C = 80 − 50 = 30 V", "V = √(40² + 30²) = 50 V"],
  why="170 V adds the three voltages arithmetically. 70 V adds V_R to (V_L − V_C) arithmetically. 102 V adds the "
      "squares of all three, treating V_L and V_C as perpendicular.",
  ncert=NC + "'Alternating Current', series LCR circuit (phasor diagram)", seconds=50, rc=True)

q(EMI, "Self and mutual inductance", "Intermediate", "assertion_reason",
  ar("Self-inductance plays the role of inertia in an electric circuit; it is the electrical analogue of mass in "
     "mechanics.",
     "The self-induced emf in a coil opposes any change (growth or decay) of the current in it."),
  AR, ar_key(True, True, explains=True),
  "Self-induction and electrical inertia",
  "Mass resists a change of velocity; a coil's self-induced back emf, −L dI/dt, resists a change of current. "
  "Because self-inductance opposes changes of current just as mass opposes changes of motion, it is called the "
  "electrical inertia. R gives the reason for A.",
  ["Back emf ε = −L dI/dt opposes change of current → R true",
   "This opposition to change is what makes L analogous to mass → A true and explained by R"],
  why="R is the very property that makes the analogy hold, so B is wrong; both are true, so C and D are wrong.",
  ncert=NC + "'Electromagnetic Induction', self-inductance", seconds=40)

q(EMI, "AC: rms, reactance and impedance", "Intermediate", "statement_pair",
  sp("In a purely resistive AC circuit, the average power dissipated is V_rms × I_rms.",
     "An alternating current of peak value I₀ produces the same heating effect in a resistor as a steady current "
     "of value I₀."),
  SP, sp_key(True, False),
  "rms values and power in AC circuits",
  "For a resistor the current is in phase with the voltage, so P = V_rms I_rms (power factor 1). The steady "
  "current with the same heating effect is the rms value I₀/√2, not the peak value I₀.",
  ["Resistor: φ = 0, P = V_rms I_rms → Statement I true",
   "Average power = I₀²R/2 = (I₀/√2)²R → equivalent DC is I₀/√2 → Statement II false"],
  why="Statement I is true and Statement II is false; the other combinations are wrong.",
  ncert=NC + "'Alternating Current', AC voltage applied to a resistor", seconds=40)

q(EMI, "AC: rms, reactance and impedance", "Intermediate", "match_list",
  ml("Each circuit in List-I is connected to a sinusoidal AC source. Match it with the phase relation between the "
     "current and the source voltage in List-II.",
     ["A pure resistor", "A pure inductor", "A pure capacitor",
      "A resistor and a capacitor in series, with resistance R equal to the capacitive reactance X_C"],
     ["Current leads the voltage by π/4", "Current lags behind the voltage by π/2", "Current is in phase with the voltage",
      "Current leads the voltage by π/2"]),
  *mlo("A-III, B-II, C-IV, D-I",
       ["A-III, B-IV, C-II, D-I", "A-I, B-II, C-IV, D-III", "A-III, B-II, C-I, D-IV"], "B"),
  "Phase relations in AC circuits",
  "Current and voltage are in phase in a resistor. In an inductor the current lags by π/2; in a capacitor it leads "
  "by π/2. In a series RC circuit tan φ = X_C/R, with the current leading; for X_C = R, φ = π/4.",
  ["R: in phase → A-III", "L: lags by π/2 → B-II", "C: leads by π/2 → C-IV", "RC with X_C = R: tan φ = 1, "
   "leads by π/4 → D-I"],
  why="Swapping B and C reverses the inductor and capacitor. The other codes give the RC circuit a phase of 0 or "
      "π/2, which needs X_C = 0 or R = 0.",
  ncert=NC + "'Alternating Current', AC voltage applied to an inductor and to a capacitor", seconds=55)

vt = 0.020 * 10 * 2 / (0.5 ** 2 * 0.4 ** 2)
close(vt, 10)
close(0.020 * 10 * 2 / (0.5 * 0.4), 2)
close(0.020 * 10 / (0.5 ** 2 * 0.4 ** 2 * 2), 2.5)
close(0.020 * 10 * 2 / (0.5 ** 2 * 0.4), 4)
# at terminal speed: B I l = mg with I = Bvl/R
close(0.5 * (0.5 * vt * 0.4 / 2) * 0.4, 0.020 * 10)
q(EMI, "Faraday's and Lenz's laws", "Advanced", "numerical",
  "Two long vertical conducting rails, 0.40 m apart, are joined at the top by a 2.0 Ω resistor. A uniform "
  "horizontal magnetic field of 0.50 T is perpendicular to the plane of the rails. A horizontal conducting rod of "
  "mass 20 g slides down the rails without friction, always in contact with them. Neglecting all other "
  "resistances and taking g = 10 m/s², the terminal speed of the rod is:",
  *opt("10 m/s", ["2 m/s", "2.5 m/s", "4 m/s"], "B"),
  "Motional emf ε = Bvl; magnetic force on the induced current opposes the motion (Lenz's law)",
  "As the rod falls, the induced current I = Bvl/R experiences an upward force BIl = B²l²v/R that grows with "
  "speed. The rod stops accelerating when this force equals its weight.",
  ["B²l²v/R = mg", "v = mgR/(B²l²) = (0.020 × 10 × 2.0)/(0.25 × 0.16)", "v = 0.40/0.040 = 10 m/s"],
  why="2 m/s uses Bl instead of B²l². 2.5 m/s puts R in the denominator. 4 m/s squares B but not l.",
  ncert=NC + "'Electromagnetic Induction', motional electromotive force; energy consideration", seconds=90,
  rc=True)

R12 = 1.0
XL12 = R12 * math.tan(math.radians(45))
XC12 = R12 * math.tan(math.radians(45))
pf12 = R12 / math.hypot(R12, XL12 - XC12)
close(pf12, 1)
q(EMI, "LCR resonance and power", "Advanced", "numerical",
  "A resistor R, an inductor L and a capacitor C are available. When R and L alone are connected in series to an AC "
  "source of fixed frequency, the current lags the voltage by 45°. When R and C alone are connected in series to "
  "the same source, the current leads the voltage by 45°. When R, L and C are all connected in series to this "
  "source, the power factor of the circuit is:",
  *opt("1", ["1/√2", "1/2", "zero"], "A"),
  "Phase angle tan φ = (X_L − X_C)/R; power factor cos φ",
  "A 45° phase difference in the RL circuit means X_L = R; in the RC circuit, X_C = R. In the LCR circuit the two "
  "reactances cancel, so the circuit is at resonance.",
  ["RL: tan 45° = X_L/R → X_L = R", "RC: tan 45° = X_C/R → X_C = R",
   "LCR: Z = √[R² + (X_L − X_C)²] = R → cos φ = R/Z = 1"],
  why="1/√2 is the power factor of either two-element circuit, not of the full LCR circuit. 1/2 and zero do not "
      "follow from equal reactances; zero would need R = 0.",
  ncert=NC + "'Alternating Current', series LCR circuit; resonance; power factor", seconds=75, rc=True)

pf = lambda R_, XL_, XC_: R_ / math.hypot(R_, XL_ - XC_)
assert pf(0, 1, 0) == 0
close(pf(1, 0, 0), 1)
close(pf(1, 0, math.sqrt(3)), 0.5)
close(pf(1, 2, 1), 1 / math.sqrt(2))
q(EMI, "LCR resonance and power", "Advanced", "match_list",
  ml("Each circuit in List-I is connected to an AC source. Match it with its power factor in List-II.",
     ["A pure inductor", "A pure resistor",
      "A resistor R in series with a capacitor of reactance √3 R",
      "A series LCR circuit with X_L = 2R and X_C = R"],
     ["1/2", "zero", "1/√2", "1"]),
  *mlo("A-II, B-IV, C-I, D-III",
       ["A-IV, B-II, C-I, D-III", "A-II, B-IV, C-III, D-I", "A-II, B-I, C-IV, D-III"], "C"),
  "Power factor cos φ = R/Z",
  "Use Z = √[R² + (X_L − X_C)²] for each circuit. A pure reactance has R = 0 and power factor zero; a pure "
  "resistance has Z = R.",
  ["Inductor: R = 0 → cos φ = 0 → A-II", "Resistor: Z = R → 1 → B-IV",
   "RC: Z = √(R² + 3R²) = 2R → 1/2 → C-I", "LCR: X_L − X_C = R → Z = √2 R → 1/√2 → D-III"],
  why="Swapping A and B gives the inductor the power factor of a resistor. Swapping C and D, or B and C, "
      "mismatches the RC and LCR results.",
  ncert=NC + "'Alternating Current', power in AC circuit: the power factor", seconds=80, rc=True)

res_truth = {"a": True, "b": True, "c": False, "d": False, "e": True}
q(EMI, "LCR resonance and power", "Advanced", "multi_statement",
  ms("A series LCR circuit (R ≠ 0) is driven by an AC source of fixed rms voltage whose frequency can be varied. "
     "Which of the following statements are correct?",
     ["At resonance, the voltages across the inductor and the capacitor are equal in magnitude and opposite in "
      "phase.",
      "At resonance, the amplitude of the current is the largest.",
      "A series circuit containing only a resistor and an inductor (no capacitor) can also be brought to "
      "resonance by changing the frequency.",
      "The resonant frequency of the circuit depends on the resistance R.",
      "At resonance, the average power drawn from the source is V_rms²/R."]),
  *mso(res_truth, "abe", ["abd", "bce", "ade"], "D"),
  "Resonance in a series LCR circuit",
  "At ω₀ = 1/√(LC), X_L = X_C, so the voltages across L and C cancel, Z = R is a minimum and the current is a "
  "maximum. Resonance needs both L and C, since the reactances must cancel. ω₀ does not involve R. At resonance "
  "the power factor is 1, so P = V_rms I_rms = V_rms²/R.",
  ["(a) True", "(b) True: Z is least (= R)", "(c) False: needs both L and C",
   "(d) False: ω₀ = 1/√(LC)", "(e) True"],
  why="The other options include (c) or (d), which are false, or leave out a true statement.",
  ncert=NC + "'Alternating Current', series LCR circuit: resonance", seconds=60)


# ================================================================ Electromagnetic Waves (B1 I2 A1)
q(EMW, "EM spectrum and uses", "Basic", "direct",
  "The remote switches of household electronic systems such as TV sets work by sending out:",
  *opt("infrared waves", ["ultraviolet rays", "microwaves", "gamma rays"], "C"),
  "Uses of infrared radiation",
  "Infrared radiation is produced by light emitting diodes and is used in the remote switches of household "
  "electronic systems such as TV sets, video recorders and hi-fi systems.",
  ["Remote controls use IR LEDs → infrared"],
  why="Ultraviolet is used, for example, to kill germs; microwaves are used in radar and ovens; gamma rays come "
      "from nuclear reactions and are used in medicine. None of these is used in TV remote switches.",
  ncert=NC + "'Electromagnetic Waves', electromagnetic spectrum (infrared waves)", seconds=20)

v_med = 3e8 / math.sqrt(1 * 2.25)
lam_med = v_med / 5e14
close(v_med, 2e8)
close(lam_med, 400e-9)
close(3e8 / 5e14, 600e-9)
close(3e8 / 2.25 / 5e14, 267e-9, 1e-2)
close(3e8 * 1.5 / 5e14, 900e-9)
q(EMW, "EM wave properties", "Intermediate", "numerical",
  "An electromagnetic wave of frequency 5.0 × 10¹⁴ Hz travels through a non-magnetic medium (relative "
  "permeability 1) of relative permittivity 2.25. Its speed in the medium is v = c/√(µ_r ε_r), with "
  "c = 3 × 10⁸ m/s. The wavelength of the wave in the medium is:",
  *opt("400 nm", ["600 nm", "267 nm", "900 nm"], "A"),
  "Speed of an EM wave in a medium: v = 1/√(µε) = c/√(µ_r ε_r); λ = v/f",
  "The frequency is fixed by the source; in the medium the speed and hence the wavelength are reduced by the "
  "factor √(µ_r ε_r) = 1.5.",
  ["v = 3 × 10⁸/√2.25 = 2 × 10⁸ m/s", "λ = v/f = 2 × 10⁸/(5.0 × 10¹⁴) = 4.0 × 10⁻⁷ m = 400 nm"],
  why="600 nm is the wavelength in vacuum. 267 nm divides by ε_r instead of √ε_r. 900 nm multiplies by 1.5 "
      "instead of dividing.",
  ncert=NC + "'Electromagnetic Waves', electromagnetic waves (speed in a medium)", seconds=45, rc=True)

i_d = 8.85e-12 * 0.05 * 2.0e12
close(i_d, 0.885)
close(8.85e-12 * 2.0e12, 17.7)
close(8.85e-12 * 2.0e12 / 0.05, 354)
close(4 * math.pi * 1e-7 * 0.05 * 2.0e12, 1.26e5, 1e-2)
q(EMW, "Displacement current", "Intermediate", "numerical",
  "The electric field between the plates of a parallel-plate capacitor, each of area 0.050 m², is uniform and is "
  "increasing at the rate of 2.0 × 10¹² V m⁻¹ s⁻¹. Taking ε₀ = 8.85 × 10⁻¹² C² N⁻¹ m⁻², the displacement current "
  "between the plates is about:",
  *opt("0.89 A", ["17.7 A", "354 A", "1.3 × 10⁵ A"], "B"),
  "Displacement current: i_d = ε₀ dΦ_E/dt = ε₀ A dE/dt",
  "The changing electric flux between the plates acts as a source of magnetic field, just like a conduction "
  "current of value ε₀ dΦ_E/dt.",
  ["Φ_E = EA → dΦ_E/dt = A dE/dt = 0.050 × 2.0 × 10¹² = 1.0 × 10¹¹ V m s⁻¹",
   "i_d = ε₀ dΦ_E/dt = 8.85 × 10⁻¹² × 1.0 × 10¹¹ ≈ 0.89 A"],
  why="17.7 A leaves out the plate area. 354 A divides by the area instead of multiplying. 1.3 × 10⁵ A uses µ₀ in "
      "place of ε₀.",
  ncert=NC + "'Electromagnetic Waves', displacement current", seconds=45, rc=True)

q(EMW, "Displacement current", "Advanced", "statement_pair",
  sp("A displacement current exists in a region only when the electric flux through that region changes with "
     "time.",
     "While a capacitor is being charged, the displacement current between its plates is equal to the conduction "
     "current in the connecting wires."),
  SP, sp_key(True, True),
  "Maxwell's displacement current",
  "i_d = ε₀ dΦ_E/dt is zero for a steady electric field. During charging, the conduction current i brings charge "
  "Q to the plates, and the flux between them is Q/ε₀, so i_d = ε₀ d(Q/ε₀)/dt = dQ/dt = i: the total current "
  "(conduction plus displacement) is continuous.",
  ["i_d = ε₀ dΦ_E/dt → zero if Φ_E is constant → Statement I true",
   "Φ_E = Q/ε₀ → i_d = dQ/dt = i → Statement II true"],
  why="Both statements are true, so every other option is wrong.",
  ncert=NC + "'Electromagnetic Waves', displacement current", seconds=50)


# ================================================================ Optics (B6 I8 A6)
n1 = 1 / F(3, 5)
assert n1 == F(5, 3)
close(3e8 / float(n1), 1.8e8)
close(3e8 * float(n1), 5.0e8)
close(3e8 * 0.8, 2.4e8)
q(OPT, "Total internal reflection", "Basic", "numerical",
  "The critical angle C for light travelling from a transparent medium into air is such that sin C = 3/5. Taking "
  "the speed of light in air as 3 × 10⁸ m/s, the speed of light in the medium is:",
  *opt("1.8 × 10⁸ m/s", ["5.0 × 10⁸ m/s", "2.4 × 10⁸ m/s", "3.0 × 10⁸ m/s"], "B"),
  "Critical angle: sin C = 1/n; speed v = c/n",
  "The critical angle fixes the refractive index of the medium relative to air, and the refractive index fixes "
  "the speed of light in it.",
  ["n = 1/sin C = 5/3", "v = c/n = 3 × 10⁸ × 3/5 = 1.8 × 10⁸ m/s"],
  why="5.0 × 10⁸ m/s multiplies by n instead of dividing (and exceeds c). 2.4 × 10⁸ m/s uses cos C. "
      "3.0 × 10⁸ m/s assumes the speed does not change.",
  ncert=NC + "'Ray Optics and Optical Instruments', total internal reflection", seconds=35, rc=True)

f2, u2 = F(-10), F(-5)
v2 = 1 / (1 / f2 - 1 / u2)
assert v2 == 10 and -v2 / u2 == 2
assert 1 / (F(1, 10) + F(1, 5)) == F(10, 3)
q(OPT, "Mirrors", "Basic", "numerical",
  "An object is placed 5 cm in front of a concave mirror of focal length 10 cm. The image formed is:",
  *opt("10 cm behind the mirror, virtual, with magnification +2",
       ["10 cm in front of the mirror, real, with magnification −2",
        "3.3 cm behind the mirror, virtual, with magnification +0.67",
        "at infinity"], "D"),
  "Mirror equation 1/v + 1/u = 1/f with the Cartesian sign convention; m = −v/u",
  "An object inside the focus of a concave mirror gives a virtual, erect, magnified image behind the mirror.",
  ["u = −5 cm, f = −10 cm", "1/v = 1/f − 1/u = −1/10 + 1/5 = +1/10 → v = +10 cm (behind the mirror)",
   "m = −v/u = −10/(−5) = +2 (virtual, erect, twice the size)"],
  why="'10 cm in front, real' drops the sign of v. 3.3 cm comes from adding 1/10 and 1/5 (magnitudes without "
      "signs). 'At infinity' is the case of an object at the focus.",
  ncert=NC + "'Ray Optics and Optical Instruments', the mirror equation; magnification", seconds=40, rc=True)

f3 = 1 / F(-5, 2)
assert f3 == F(-2, 5)  # metres = -40 cm
q(OPT, "Refraction and lenses", "Basic", "numerical",
  "The power of a thin lens is −2.5 D. Its focal length and the type of lens are:",
  *opt("−40 cm; a concave (diverging) lens",
       ["−0.4 cm; a concave (diverging) lens", "+40 cm; a convex (converging) lens",
        "−4 cm; a concave (diverging) lens"], "A"),
  "Power of a lens: P = 1/f, with f in metres",
  "Power in dioptres is the reciprocal of the focal length in metres; a negative power means a diverging lens.",
  ["f = 1/P = 1/(−2.5) m = −0.4 m = −40 cm", "Negative focal length → concave (diverging) lens"],
  why="−0.4 cm leaves the answer in metres but labels it centimetres. +40 cm ignores the sign of the power. "
      "−4 cm divides 10 by 2.5.",
  ncert=NC + "'Ray Optics and Optical Instruments', power of a lens", seconds=25, rc=True)

r4 = math.degrees(math.asin(math.sin(math.radians(45)) / math.sqrt(2)))
close(r4, 30)
close(45 - r4, 15)
close(45 + r4, 75)
q(OPT, "Refraction and lenses", "Basic", "numerical",
  "A ray of light in air falls on the plane surface of a glass block of refractive index √2 at an angle of "
  "incidence of 45°. The angle through which the ray is deviated from its original direction on entering the "
  "glass is:",
  *opt("15°", ["30°", "45°", "75°"], "C"),
  "Snell's law: sin i = n sin r; deviation at one surface = i − r",
  "The ray bends towards the normal; the deviation is the angle between the incident and refracted directions.",
  ["sin r = sin 45°/√2 = (1/√2)/√2 = 1/2 → r = 30°", "Deviation = i − r = 45° − 30° = 15°"],
  why="30° is the angle of refraction, not the deviation. 45° is the angle of incidence. 75° adds i and r.",
  ncert=NC + "'Ray Optics and Optical Instruments', refraction", seconds=30, rc=True)

q(OPT, "Polarisation", "Basic", "direct",
  "Unpolarised light of intensity I₀ falls normally on a single polaroid, which is slowly rotated in its own "
  "plane. The intensity of the light transmitted by the polaroid:",
  *opt("remains constant at I₀/2",
       ["varies between I₀ and zero", "varies between I₀ and I₀/2", "becomes zero twice in every rotation"], "B"),
  "Unpolarised light and a polaroid",
  "In unpolarised light the direction of the electric field changes randomly, so every orientation of the pass "
  "axis transmits the same average intensity, half of the incident intensity.",
  ["Unpolarised: no preferred direction", "Any orientation transmits I₀/2 → no change on rotation"],
  why="Variation between I₀ and zero is what a second polaroid (analyser) shows when it is rotated in already "
      "polarised light; with unpolarised light the transmitted intensity never varies or becomes zero.",
  ncert=NC + "'Wave Optics', polarisation", seconds=25)

q(OPT, "Huygens' principle and interference", "Basic", "direct",
  "Light from a distant star reaches the Earth. A small portion of the wavefront arriving at a telescope can be "
  "taken to be:",
  *opt("plane", ["spherical and diverging", "cylindrical", "spherical and converging"], "D"),
  "Shapes of wavefronts",
  "A point source sends out spherical wavefronts. At a very large distance the radius of the sphere is huge, so a "
  "small portion of the wavefront is effectively a plane.",
  ["Point source → spherical wavefront", "Very far from the source, a small part of a large sphere ≈ plane"],
  why="A diverging spherical wavefront is seen close to a point source; a cylindrical one comes from a linear "
      "source (such as a slit); a converging spherical wavefront is produced, for example, by a convex lens.",
  ncert=NC + "'Wave Optics', Huygens principle", seconds=25)

n_g, R7, u7 = F(3, 2), F(10), F(-30)
v7 = n_g / ((n_g - 1) / R7 + 1 / u7)
assert v7 == 90
assert n_g / ((n_g - 1) / R7 + F(1, 30)) == 18
assert 1 / ((n_g - 1) / R7 + 1 / u7) == 60
assert n_g / (1 / u7) == -45
q(OPT, "Refraction and lenses", "Intermediate", "numerical",
  "A point object in air lies on the axis of a long glass rod (refractive index 1.5) whose end is ground to a "
  "convex hemispherical surface of radius of curvature 10 cm. The object is 30 cm from the pole of this surface. "
  "The image formed by refraction at the surface is:",
  *opt("90 cm from the pole, inside the glass (real)",
       ["18 cm from the pole, inside the glass (real)", "60 cm from the pole, inside the glass (real)",
        "45 cm from the pole, on the air side (virtual)"], "C"),
  "Refraction at a spherical surface: n₂/v − n₁/u = (n₂ − n₁)/R",
  "Light goes from air (n₁ = 1) into glass (n₂ = 1.5). With the Cartesian convention, u = −30 cm and R = +10 cm "
  "(centre of curvature inside the glass).",
  ["1.5/v − 1/(−30) = (1.5 − 1)/10", "1.5/v = 0.05 − 0.0333 = 0.0167", "v = +90 cm: real image inside the glass"],
  why="18 cm takes u = +30 cm. 60 cm drops n₂ from the term n₂/v. 45 cm (virtual) ignores the curvature, "
      "treating the surface as plane.",
  ncert=NC + "'Ray Optics and Optical Instruments', refraction at spherical surfaces", seconds=70, rc=True)

f8 = 1 / ((F(8, 5) - 1) * (F(-1, 30) - F(1, 30)))
assert f8 == -25
assert 1 / ((F(8, 5) - 1) * F(-1, 30)) == -50
close(1 / (1.6 * (-2 / 30)), -9.375)
q(OPT, "Refraction and lenses", "Intermediate", "numerical",
  "A thin biconcave lens is made of glass of refractive index 1.6, and both its surfaces have radius of curvature "
  "30 cm. Its focal length in air is:",
  *opt("−25 cm", ["−50 cm", "+25 cm", "−9.4 cm"], "A"),
  "Lens maker's formula: 1/f = (n − 1)(1/R₁ − 1/R₂)",
  "For a biconcave lens, with light going from left to right, the first surface has its centre of curvature on "
  "the incident side (R₁ = −30 cm) and the second on the far side (R₂ = +30 cm).",
  ["1/f = (1.6 − 1)(1/(−30) − 1/30) = 0.6 × (−2/30) = −0.04 cm⁻¹", "f = −25 cm (diverging)"],
  why="−50 cm counts only one curved surface. +25 cm ignores the signs of the radii, giving a converging lens. "
      "−9.4 cm uses n instead of (n − 1).",
  ncert=NC + "'Ray Optics and Optical Instruments', lens maker's formula", seconds=50, rc=True)

M9 = F(90, 5) * (1 + F(5, 25))
assert M9 == F(108, 5)
assert F(90, 5) == 18 and F(90, 5) + 1 == 19 and F(90, 5) * (1 - F(5, 25)) == F(72, 5)
q(OPT, "Optical instruments", "Intermediate", "numerical",
  "An astronomical telescope has an objective of focal length 90 cm and an eyepiece of focal length 5 cm. It is "
  "adjusted so that the final image is formed at the least distance of distinct vision, D = 25 cm. The magnifying "
  "power of the telescope is:",
  *opt("21.6", ["18", "19", "14.4"], "B"),
  "Telescope with the final image at the near point: M = (f_o/f_e)(1 + f_e/D)",
  "With the final image at D instead of at infinity, the eyepiece acts as a simple microscope with magnification "
  "(1 + f_e/D) on the angular size set by the objective.",
  ["f_o/f_e = 90/5 = 18", "M = 18 × (1 + 5/25) = 18 × 1.2 = 21.6"],
  why="18 is the magnifying power in normal adjustment (image at infinity). 19 adds 1 to f_o/f_e. 14.4 uses "
      "(1 − f_e/D).",
  ncert=NC + "'Ray Optics and Optical Instruments', optical instruments: telescope", seconds=50, rc=True)

N10 = F(10) * 600 / 400
assert N10 == 15
assert F(10) * 400 / 600 == F(20, 3) and F(10) * F(600, 400) ** 2 == F(45, 2)
q(OPT, "Huygens' principle and interference", "Intermediate", "numerical",
  "In a Young's double-slit experiment with light of wavelength 600 nm, a certain length of the screen contains "
  "exactly 10 fringe widths. If the light is replaced by light of wavelength 400 nm, all else unchanged, the number "
  "of fringe widths in the same length of the screen becomes:",
  *opt("15", ["6.7", "10", "22.5"], "D"),
  "Fringe width β = λD/d ∝ λ",
  "The fixed length equals N × β. Since β is proportional to λ, the number of fringes in that length is inversely "
  "proportional to λ.",
  ["N₁β₁ = N₂β₂ → N₂ = N₁λ₁/λ₂", "N₂ = 10 × 600/400 = 15"],
  why="6.7 uses N ∝ λ. 10 assumes the fringe width does not depend on wavelength. 22.5 squares the ratio of the "
      "wavelengths.",
  ncert=NC + "'Wave Optics', interference of light waves and Young's experiment", seconds=40, rc=True)

C_glass = math.degrees(math.asin(1 / 1.5))
assert C_glass < 45
q(OPT, "Total internal reflection", "Intermediate", "assertion_reason",
  ar("A right-angled isosceles glass prism (angles 90°, 45°, 45°) can be used to turn a beam of light through 90° "
     "or through 180° by total internal reflection.",
     "The critical angle for ordinary glass (refractive index about 1.5) is greater than 45°."),
  AR, ar_key(True, False),
  "Totally reflecting prisms",
  "In such a prism the light meets the hypotenuse (or the two short faces) at 45° inside the glass. For n = 1.5, "
  "sin C = 1/1.5, so C ≈ 41.8°, which is less than 45°; the light is therefore totally reflected. A is true; R "
  "is false.",
  ["C = sin⁻¹(1/1.5) ≈ 41.8° < 45° → R false", "Angle of incidence 45° > C → total reflection → A true"],
  why="R is false (if C were greater than 45°, these prisms would not work), so options A, B and D are wrong.",
  ncert=NC + "'Ray Optics and Optical Instruments', total internal reflection (prisms)", seconds=45)

q(OPT, "Mirrors", "Intermediate", "statement_pair",
  sp("The linear magnification produced by a plane mirror is −1.",
     "A convex mirror always forms a virtual, erect and diminished image of a real object."),
  SP, sp_key(False, True),
  "Images formed by plane and convex mirrors",
  "A plane mirror forms a virtual, erect image of the same size, so m = +1 (a negative magnification would mean an "
  "inverted image). For a convex mirror f > 0 and u < 0, so v is always positive (behind the mirror) and less than "
  "f, giving a virtual, erect, diminished image.",
  ["Plane mirror: erect, same size → m = +1 → Statement I false",
   "Convex mirror: 0 < v < f for every real object → virtual, erect, diminished → Statement II true"],
  why="Statement I is false and Statement II is true; every other combination is wrong.",
  ncert=NC + "'Ray Optics and Optical Instruments', reflection of light by spherical mirrors", seconds=40)

q(OPT, "Prism", "Intermediate", "match_list",
  ml("Match each quantity in List-I with its expression in List-II (n = refractive index, A = angle of the prism, "
     "D_m = angle of minimum deviation, R₁ and R₂ = radii of curvature, f = focal length in metres).",
     ["Refractive index of the material of a prism", "Deviation produced by a thin prism",
      "1/f for a thin lens in air (lens maker's formula)", "Power of a lens"],
     ["(n − 1)A", "1/f", "sin[(A + D_m)/2]/sin(A/2)", "(n − 1)(1/R₁ − 1/R₂)"]),
  *mlo("A-III, B-I, C-IV, D-II",
       ["A-I, B-III, C-IV, D-II", "A-III, B-IV, C-I, D-II", "A-III, B-I, C-II, D-IV"], "D"),
  "Prism and lens formulae",
  "At minimum deviation the ray passes symmetrically through the prism, giving n = sin[(A + D_m)/2]/sin(A/2). For "
  "small A this reduces to D = (n − 1)A. The lens maker's formula gives 1/f, and the power of a lens is 1/f in "
  "dioptres.",
  ["Prism at minimum deviation → A-III", "Thin prism → B-I", "Lens maker → C-IV", "Power → D-II"],
  why="Swapping A and B confuses the exact prism formula with its small-angle form. The other codes mismatch the "
      "lens maker's formula and the definition of power.",
  ncert=NC + "'Ray Optics and Optical Instruments', refraction through a prism; lens maker's formula; power",
  seconds=50)

hw_truth = {"a": True, "b": True, "c": False, "d": True, "e": False}
q(OPT, "Huygens' principle and interference", "Intermediate", "multi_statement",
  ms("Which of the following statements about wavefronts are correct?",
     ["The wavefront due to a point source at a finite distance is spherical.",
      "Rays are perpendicular to the wavefronts.",
      "According to the wave theory, light that bends towards the normal on refraction travels faster in the second "
      "medium.",
      "A thin convex lens converts an incident plane wavefront into a converging spherical wavefront.",
      "A plane wavefront reflected from a plane mirror becomes a spherical wavefront."]),
  *mso(hw_truth, "abd", ["abc", "bde", "acd"], "A"),
  "Huygens' principle: wavefronts and their propagation",
  "A point source gives spherical wavefronts and rays are normals to the wavefronts. Huygens' construction gives "
  "n₂/n₁ = v₁/v₂, so bending towards the normal (n₂ > n₁) means slower travel in the second medium. A convex "
  "lens converts a plane wave into a spherical wave converging to its focus; a plane mirror reflects a plane wave "
  "as a plane wave.",
  ["(a) True", "(b) True", "(c) False: v₂ < v₁ when the ray bends towards the normal", "(d) True",
   "(e) False: the reflected wavefront is plane"],
  why="The other options include (c) or (e), which are false, or leave out a true statement.",
  ncert=NC + "'Wave Optics', Huygens principle; refraction and reflection of plane waves", seconds=55)

v_a = F(10)
u_b = v_a - 5
v_b = 1 / (F(-1, 10) + 1 / u_b)
assert v_b == 10
assert 1 / (F(-1, 10) + 1 / -u_b) == F(-10, 3)
q(OPT, "Refraction and lenses", "Advanced", "numerical",
  "A parallel beam of light travelling along the common principal axis falls on a thin convex lens of focal length "
  "10 cm. A thin concave lens of focal length 10 cm is placed coaxially 5 cm behind the convex lens (on the side "
  "away from the incoming light). The final image is formed:",
  *opt("10 cm beyond the concave lens, real",
       ["3.3 cm before the concave lens (on the convex-lens side), virtual", "at infinity",
        "5 cm beyond the concave lens, real"], "A"),
  "Two-lens system: the image of the first lens is the object for the second",
  "The convex lens alone would focus the beam 10 cm behind it, i.e. 5 cm beyond the concave lens. The concave lens "
  "intercepts the converging beam, so that point is a virtual object for it.",
  ["Convex lens: image at +10 cm from it", "For the concave lens: u = +5 cm (virtual object), f = −10 cm",
   "1/v = 1/f + 1/u = −1/10 + 1/5 = +1/10 → v = +10 cm: real image 10 cm beyond the concave lens"],
  why="3.3 cm (virtual) treats the virtual object as a real object (u = −5 cm). 'At infinity' treats the lenses as "
      "if they were in contact (net power zero). '5 cm beyond' ignores the concave lens.",
  ncert=NC + "'Ray Optics and Optical Instruments', combination of thin lenses", seconds=90, rc=True)

sinC16 = 1 / 1.25
tanC16 = sinC16 / math.sqrt(1 - sinC16 ** 2)
close(60 * tanC16, 80)
close(60 * sinC16, 48)
close(60 / tanC16, 45)
close(60 * math.sqrt(1 - sinC16 ** 2), 36)
q(OPT, "Total internal reflection", "Advanced", "numerical",
  "A small bulb lies at the bottom of a tank filled to a depth of 60 cm with a transparent liquid of refractive "
  "index 1.25. Light from the bulb can emerge into the air above only through a circular patch of the liquid "
  "surface directly above the bulb. The radius of this patch is:",
  *opt("80 cm", ["48 cm", "45 cm", "36 cm"], "B"),
  "Total internal reflection: rays meeting the surface at more than the critical angle are trapped",
  "Light escapes only where the angle of incidence at the surface is less than C. The edge of the patch is where "
  "the ray from the bulb meets the surface exactly at C, so r = h tan C.",
  ["sin C = 1/1.25 = 0.8 → cos C = 0.6, tan C = 4/3", "r = h tan C = 60 × 4/3 = 80 cm"],
  why="48 cm uses h sin C. 45 cm uses h/tan C. 36 cm uses h cos C.",
  ncert=NC + "'Ray Optics and Optical Instruments', total internal reflection", seconds=70, rc=True)

lam1, lam2 = 600, 480
n_a, n_b = 4, 5
assert n_a * lam1 == n_b * lam2 == 2400
assert all(k * lam1 % lam2 for k in range(1, n_a))  # no smaller coincidence
y17 = n_a * lam1 * 1e-9 * 1.0 / 1e-3
close(y17, 2.4e-3)
close((lam1 + lam2) * 1e-9 / 1e-3, 1.08e-3)
q(OPT, "Huygens' principle and interference", "Advanced", "numerical",
  "In a Young's double-slit experiment, the slits are 1.0 mm apart and the screen is 1.0 m away. The slits are "
  "illuminated with light containing two wavelengths, 600 nm and 480 nm. The least distance from the central "
  "maximum at which a bright fringe of one wavelength falls exactly on a bright fringe of the other is:",
  *opt("2.4 mm", ["0.6 mm", "1.08 mm", "4.8 mm"], "C"),
  "Position of the nth bright fringe: y = nλD/d; coincidence when n₁λ₁ = n₂λ₂",
  "Bright fringes of the two wavelengths coincide where the same path difference is a whole number of each "
  "wavelength. The smallest such path difference (other than zero) is the least common multiple of 600 nm and "
  "480 nm.",
  ["n₁ × 600 = n₂ × 480 → n₁/n₂ = 4/5", "Smallest: n₁ = 4, n₂ = 5 → path difference 2400 nm",
   "y = 4 × 600 × 10⁻⁹ × 1.0/(1.0 × 10⁻³) = 2.4 × 10⁻³ m = 2.4 mm"],
  why="0.6 mm is only the first bright fringe of 600 nm light. 1.08 mm adds the two wavelengths. 4.8 mm is the "
      "second coincidence (n₁ = 8, n₂ = 10).",
  ncert=NC + "'Wave Optics', interference of light waves and Young's experiment", seconds=90, rc=True)

q(OPT, "Huygens' principle and interference", "Advanced", "assertion_reason",
  ar("When a plane wavefront passes through a thin prism, the emerging wavefront is a plane that is tilted with "
     "respect to the incident wavefront.",
     "The part of the wavefront that travels through the thicker portion of the prism is delayed more, because "
     "light travels more slowly in glass than in air."),
  AR, ar_key(True, True, explains=True),
  "Refraction of a plane wave by a prism (Huygens' construction)",
  "Different parts of the incident wavefront cross different thicknesses of glass. The part crossing the thick "
  "base spends longer in the slower medium and lags behind the part crossing near the apex, so the emerging "
  "wavefront is tilted (the light is deviated towards the base). R explains A.",
  ["Speed in glass < speed in air", "Greater thickness → greater delay → wavefront tilts → A true, explained by R"],
  why="R is the cause of the tilt described in A, so B is wrong; both are true, so C and D are wrong.",
  ncert=NC + "'Wave Optics', Huygens principle (refraction of a plane wave by a thin prism)", seconds=45)

q(OPT, "Diffraction", "Advanced", "statement_pair",
  sp("In the diffraction pattern of a single slit of width a, illuminated normally by light of wavelength λ, the "
     "angular width of the central maximum is 2λ/a.",
     "If the slit is illuminated with blue light instead of red light, all else unchanged, the central maximum "
     "becomes wider."),
  SP, sp_key(True, False),
  "Single-slit diffraction: width of the central maximum",
  "The first minima lie at θ = ±λ/a (small angles), so the central maximum spans an angle 2λ/a. Since the width is "
  "proportional to λ, the shorter wavelength of blue light gives a narrower central maximum.",
  ["First minima at ±λ/a → angular width 2λ/a → Statement I true",
   "λ_blue < λ_red → narrower central maximum → Statement II false"],
  why="Statement I is true and Statement II is false; the other combinations are wrong.",
  ncert=NC + "'Wave Optics', diffraction at a single slit", seconds=45)

C_ga = math.degrees(math.asin(1 / 1.5))
C_gw = math.degrees(math.asin((4 / 3) / 1.5))
assert C_gw > C_ga  # (e) false
assert math.degrees(math.asin(1 / 2.0)) < C_ga  # (c) false: higher n -> smaller C
tir_truth = {"a": True, "b": True, "c": False, "d": True, "e": False}
q(OPT, "Total internal reflection", "Advanced", "multi_statement",
  ms("Which of the following statements about total internal reflection are correct?",
     ["It can occur only when light travels from an optically denser medium towards an optically rarer medium.",
      "It occurs only when the angle of incidence exceeds the critical angle for the pair of media.",
      "For light going from different media into air, the critical angle is larger for a medium of larger "
      "refractive index.",
      "When total internal reflection occurs at a boundary, there is no refracted ray in the rarer medium.",
      "For a given glass, the critical angle at a glass–water boundary is smaller than at a glass–air boundary."]),
  *mso(tir_truth, "abd", ["abc", "bde", "ade"], "C"),
  "Conditions for total internal reflection; sin C = n_rarer/n_denser",
  "TIR needs denser-to-rarer travel and incidence beyond the critical angle; then all the light is reflected and "
  "no refracted ray exists. sin C = n_rarer/n_denser, so a larger n_denser gives a smaller C, and replacing air by "
  "water (n closer to that of glass) increases C.",
  ["(a) True", "(b) True", "(c) False: sin C = 1/n → larger n, smaller C", "(d) True",
   "(e) False: glass–water: sin C = 1.33/1.5 ≈ 0.89 (C ≈ 63°) > glass–air: sin C = 0.67 (C ≈ 42°)"],
  why="The other options include (c) or (e), which are false, or leave out a true statement.",
  ncert=NC + "'Ray Optics and Optical Instruments', total internal reflection", seconds=70)


# ================================================================ Dual Nature of Matter and Radiation (B3 I4 A3)
q(DUAL, "Photoelectric effect", "Basic", "direct",
  "Most metals emit photoelectrons only when ultraviolet light falls on them. Which of the following metals emit "
  "photoelectrons even when visible light falls on them?",
  *opt("Alkali metals such as sodium, potassium and caesium",
       ["Zinc, cadmium and magnesium", "All metals, provided the visible light is intense enough",
        "No metal; visible light can never eject photoelectrons"], "A"),
  "Threshold frequency depends on the metal",
  "Alkali metals (lithium, sodium, potassium, caesium, rubidium) have small work functions and respond even to "
  "visible light. Metals such as zinc, cadmium and magnesium respond only to ultraviolet light of short "
  "wavelength.",
  ["Low work function → threshold in the visible → alkali metals"],
  why="Zinc, cadmium and magnesium need ultraviolet light. Intensity cannot make up for a frequency below the "
      "threshold. Alkali metals do emit with visible light, so 'no metal' is wrong.",
  ncert=NC + "'Dual Nature of Radiation and Matter', photoelectric effect (Hallwachs' and Lenard's observations)",
  seconds=25)

p_ph = 6.6e-34 / 500e-9
close(p_ph, 1.32e-27)
close(6.6e-34 * 500e-9, 3.3e-40)
close(6.6e-34 / 500, 1.32e-36)
close(6.6e-34 * 3e8 / 500e-9, 3.96e-19)
q(DUAL, "Photoelectric effect", "Basic", "numerical",
  "Taking Planck's constant h = 6.6 × 10⁻³⁴ J s, the momentum of a photon of wavelength 500 nm is:",
  *opt("1.32 × 10⁻²⁷ kg m/s", ["3.3 × 10⁻⁴⁰ kg m/s", "1.32 × 10⁻³⁶ kg m/s", "3.96 × 10⁻¹⁹ kg m/s"], "C"),
  "Photon momentum: p = h/λ",
  "Every photon of wavelength λ carries momentum h/λ (and energy hc/λ).",
  ["λ = 500 nm = 5.00 × 10⁻⁷ m", "p = h/λ = 6.6 × 10⁻³⁴/(5.00 × 10⁻⁷) = 1.32 × 10⁻²⁷ kg m/s"],
  why="3.3 × 10⁻⁴⁰ multiplies h by λ. 1.32 × 10⁻³⁶ leaves λ in nanometres. 3.96 × 10⁻¹⁹ is the photon's energy "
      "in joules (hc/λ), not its momentum.",
  ncert=NC + "'Dual Nature of Radiation and Matter', particle nature of light: the photon", seconds=30, rc=True)

nu0 = 2.0 / 4.0e-15
close(nu0, 5.0e14)
close(4.0e-15 / 2.0, 2.0e-15)
close(4.0e-15 * 2.0, 8.0e-15)
q(DUAL, "Einstein's equation", "Basic", "numerical",
  "The work function of a metal is 2.0 eV. Taking Planck's constant as 4.0 × 10⁻¹⁵ eV s, the threshold frequency "
  "for photoelectric emission from this metal is:",
  *opt("5.0 × 10¹⁴ Hz", ["2.0 × 10⁻¹⁵ Hz", "8.0 × 10⁻¹⁵ Hz", "5.0 × 10¹⁵ Hz"], "D"),
  "Threshold frequency: hν₀ = φ₀",
  "At the threshold frequency, the photon energy just equals the work function, and the photoelectrons come out "
  "with zero kinetic energy.",
  ["ν₀ = φ₀/h = 2.0 eV/(4.0 × 10⁻¹⁵ eV s)", "ν₀ = 5.0 × 10¹⁴ Hz"],
  why="2.0 × 10⁻¹⁵ Hz divides h by φ₀. 8.0 × 10⁻¹⁵ Hz multiplies them. 5.0 × 10¹⁵ Hz is a slip of a power of ten.",
  ncert=NC + "'Dual Nature of Radiation and Matter', Einstein's photoelectric equation", seconds=30, rc=True)

v_max = math.sqrt(2 * 1.6e-19 * 1.8 / 9e-31)
close(v_max, 8.0e5)
close(math.sqrt(1.6e-19 * 1.8 / 9e-31), 5.66e5, 1e-2)
close(2 * 1.6e-19 * 1.8 / 9e-31, 6.4e11)
close(math.sqrt(1.6e-19 * 1.8 / (2 * 9e-31)), 4.0e5)
q(DUAL, "Einstein's equation", "Intermediate", "numerical",
  "The stopping potential for photoelectrons emitted from a metal surface is 1.8 V. Taking the electron's charge "
  "as 1.6 × 10⁻¹⁹ C and its mass as 9 × 10⁻³¹ kg, the maximum speed of the photoelectrons is:",
  *opt("8.0 × 10⁵ m/s", ["5.7 × 10⁵ m/s", "6.4 × 10¹¹ m/s", "4.0 × 10⁵ m/s"], "B"),
  "Stopping potential: eV₀ = K_max = ½mv_max²",
  "The stopping potential is just enough to stop the fastest photoelectrons, so eV₀ equals their maximum kinetic "
  "energy.",
  ["K_max = eV₀ = 1.6 × 10⁻¹⁹ × 1.8 = 2.88 × 10⁻¹⁹ J",
   "v_max = √(2K_max/m) = √(2 × 2.88 × 10⁻¹⁹/(9 × 10⁻³¹)) = √(6.4 × 10¹¹) = 8.0 × 10⁵ m/s"],
  why="5.7 × 10⁵ m/s leaves out the factor 2 in √(2K/m). 6.4 × 10¹¹ is v², not v. 4.0 × 10⁵ m/s puts the "
      "2 in the denominator, v = √(K/2m).",
  ncert=NC + "'Dual Nature of Radiation and Matter', experimental study of photoelectric effect (stopping "
             "potential)", seconds=50, rc=True)

K_A, K_B = 5.0 - 2.0, 5.0 - 4.0
close(math.sqrt(K_A / K_B), math.sqrt(3))
q(DUAL, "Einstein's equation", "Intermediate", "numerical",
  "Photons of energy 5.0 eV fall on two metal surfaces, P of work function 2.0 eV and Q of work function 4.0 eV. "
  "The ratio of the maximum speed of the photoelectrons from P to that from Q is:",
  *opt("√3 : 1", ["3 : 1", "1 : √3", "2 : 1"], "A"),
  "Einstein's equation K_max = hν − φ₀; v ∝ √K",
  "Find each maximum kinetic energy, then remember that speed goes as the square root of kinetic energy for the "
  "same particle.",
  ["K_P = 5.0 − 2.0 = 3.0 eV, K_Q = 5.0 − 4.0 = 1.0 eV", "v_P/v_Q = √(K_P/K_Q) = √3"],
  why="3 : 1 is the ratio of kinetic energies, not speeds. 1 : √3 inverts the ratio. 2 : 1 uses the inverse ratio "
      "of the work functions.",
  ncert=NC + "'Dual Nature of Radiation and Matter', Einstein's photoelectric equation", seconds=45, rc=True)

q(DUAL, "Photoelectric effect", "Intermediate", "assertion_reason",
  ar("Photoelectrons are emitted from a metal surface only if the energy of each incident photon is at least equal "
     "to the work function of the metal.",
     "The work functions of metals are of the order of a few electron volts."),
  AR, ar_key(True, True, explains=False),
  "Photon picture of the photoelectric effect; work function",
  "An electron absorbs one photon and must receive at least the work function to escape, so emission needs hν ≥ "
  "φ₀ (A is true). Work functions are indeed a few eV (for example about 2 eV for caesium and about 5 eV for "
  "platinum), so R is true. But the size of the work function does not explain why one photon must supply at "
  "least φ₀; that follows from the single-photon absorption process. R is not the explanation of A.",
  ["One photon is absorbed by one electron; escape needs energy ≥ φ₀ → A true",
   "φ₀ ~ few eV → R true", "R states a magnitude; it does not explain the condition in A → option B"],
  why="Option A would need R to give the reason for A, which it does not. Both statements are true, so C and D are "
      "wrong.",
  ncert=NC + "'Dual Nature of Radiation and Matter', electron emission; photoelectric effect", seconds=40)

q(DUAL, "de Broglie wavelength", "Intermediate", "match_list",
  ml("Match each case in List-I with its de Broglie wavelength (or wavelength) in List-II. (h = Planck's constant, "
     "c = speed of light.)",
     ["A particle of momentum p", "A particle of mass m and kinetic energy K",
      "A particle of mass m and charge q, accelerated from rest through a potential difference V",
      "A photon of energy E"],
     ["hc/E", "h/√(2mqV)", "h/p", "h/√(2mK)"]),
  *mlo("A-III, B-IV, C-II, D-I",
       ["A-III, B-II, C-IV, D-I", "A-I, B-IV, C-II, D-III", "A-III, B-IV, C-I, D-II"], "D"),
  "de Broglie relation λ = h/p",
  "For a particle, p = √(2mK); accelerating a charge q through V gives K = qV. For a photon, E = hc/λ.",
  ["λ = h/p → A-III", "p = √(2mK) → λ = h/√(2mK) → B-IV", "K = qV → λ = h/√(2mqV) → C-II",
   "E = hc/λ → λ = hc/E → D-I"],
  why="The other codes exchange the kinetic-energy and accelerating-voltage forms or give the photon a particle "
      "formula.",
  ncert=NC + "'Dual Nature of Radiation and Matter', wave nature of matter", seconds=50)

lam8 = 0.1227
K8 = (1.227 / lam8) ** 2
E8 = 1240 / lam8
close(K8, 100)
close(E8 / K8, 101.06, 1e-2)
q(DUAL, "de Broglie wavelength", "Advanced", "numerical",
  "An electron and a photon each have a wavelength of 0.1227 nm. Taking hc = 1240 eV nm and, for an electron of "
  "kinetic energy K (in eV), λ = 1.227/√K nm, the ratio of the energy of the photon to the kinetic energy of the "
  "electron is about:",
  *opt("101", ["1", "10", "1.0 × 10⁴"], "B"),
  "Photon energy E = hc/λ; electron kinetic energy from λ = h/√(2mK)",
  "The same wavelength means the same momentum, but energy depends on momentum differently: E = pc for a photon "
  "and K = p²/2m for the electron.",
  ["Electron: √K = 1.227/0.1227 = 10 → K = 100 eV", "Photon: E = 1240/0.1227 ≈ 1.01 × 10⁴ eV",
   "E/K ≈ 1.01 × 10⁴/100 ≈ 101"],
  why="1 assumes the same wavelength means the same energy (it means the same momentum). 10 is roughly the square "
      "root of the correct ratio. 1.0 × 10⁴ is the photon energy in eV, not the ratio.",
  ncert=NC + "'Dual Nature of Radiation and Matter', wave nature of matter; the photon", seconds=75, rc=True)

P9, c9 = 3.0, 3e8
lam9 = 600e-9
h9 = 6.6e-34
N9 = P9 / (h9 * c9 / lam9)
close(N9 * h9 / lam9, P9 / c9)
close(P9 / c9, 1.0e-8)
q(DUAL, "Photoelectric effect", "Advanced", "numerical",
  "A monochromatic beam of light of wavelength 600 nm and power 3.0 W falls normally on a surface that absorbs it "
  "completely. Treating the beam as a stream of photons, each of energy hc/λ and momentum h/λ, and taking "
  "c = 3 × 10⁸ m/s, the force exerted by the beam on the surface is:",
  *opt("1.0 × 10⁻⁸ N", ["2.0 × 10⁻⁸ N", "9.0 × 10⁸ N", "1.0 × 10⁸ N"], "D"),
  "Force = rate of transfer of momentum by the photons",
  "If N photons arrive per second, N(hc/λ) = P and the momentum delivered per second is N(h/λ) = P/c. The "
  "wavelength cancels.",
  ["N = P/(hc/λ)", "Force = N × h/λ = P/c", "F = 3.0/(3 × 10⁸) = 1.0 × 10⁻⁸ N"],
  why="2.0 × 10⁻⁸ N would apply to a perfectly reflecting surface, where each photon's momentum is reversed. "
      "9.0 × 10⁸ N multiplies P by c. 1.0 × 10⁸ N divides c by P.",
  ncert=NC + "'Dual Nature of Radiation and Matter', particle nature of light: the photon", seconds=60, rc=True)

wave_truth = {"a": True, "b": True, "c": True, "d": False, "e": False}
q(DUAL, "Photoelectric effect", "Advanced", "multi_statement",
  ms("Which of the following are predictions of the wave picture of light that DISAGREE with the observed features "
     "of the photoelectric effect?",
     ["The maximum kinetic energy of the emitted electrons should increase with the intensity of the light.",
      "Emission should occur at any frequency, provided the light is intense enough.",
      "For very dim light, there should be a noticeable time lag before emission begins.",
      "There should be a threshold frequency below which no emission occurs, however intense the light.",
      "The photocurrent should increase with the intensity of the light."]),
  *mso(wave_truth, "abc", ["abd", "bce", "acd"], "D"),
  "Failure of the wave picture to explain the photoelectric effect",
  "In the wave picture, energy arrives continuously and is spread over the wavefront, so a brighter beam should "
  "give faster electrons, any frequency should work if intense enough, and dim light should need time to "
  "accumulate energy. All three disagree with experiment. A threshold frequency is not a prediction of the wave "
  "picture (it is an observation the wave picture cannot explain), and a photocurrent rising with intensity is "
  "observed, so it is not a disagreement.",
  ["(a), (b), (c): wave predictions contradicted by experiment",
   "(d): not a wave prediction (observed fact)", "(e): agrees with observation"],
  why="Every other option includes (d) or (e), or leaves out one of the three conflicting predictions.",
  ncert=NC + "'Dual Nature of Radiation and Matter', photoelectric effect and wave theory of light", seconds=70)


# ================================================================ Atoms and Nuclei (B3 I5 A3)
E_1g = 1e-3 * (3e8) ** 2
close(E_1g, 9e13)
close(1 * (3e8) ** 2, 9e16)
close(1e-3 * 3e8, 3e5)
q(AN, "Nuclear size and mass defect", "Basic", "numerical",
  "Taking c = 3 × 10⁸ m/s, the energy equivalent of 1 g of matter is:",
  *opt("9 × 10¹³ J", ["9 × 10¹⁶ J", "3 × 10⁵ J", "9 × 10¹⁰ J"], "B"),
  "Mass–energy equivalence: E = mc²",
  "Einstein's relation gives the energy equivalent of any mass; the mass must be in kilograms.",
  ["m = 1 g = 1 × 10⁻³ kg", "E = mc² = 10⁻³ × (3 × 10⁸)² = 9 × 10¹³ J"],
  why="9 × 10¹⁶ J takes the mass as 1 kg. 3 × 10⁵ J uses mc instead of mc². 9 × 10¹⁰ J converts grams to "
      "kilograms with 10⁻⁶.",
  ncert=NC + "'Nuclei', mass–energy and nuclear binding energy", seconds=25, rc=True)

E_g = -13.6
assert -E_g == 13.6
close(2 * E_g, -27.2)
close(-E_g + 2 * E_g, E_g)
q(AN, "Bohr model and hydrogen spectrum", "Basic", "numerical",
  "In the Bohr model, the total energy of the electron in the ground state of the hydrogen atom is −13.6 eV. Its "
  "kinetic energy and potential energy in this state are, respectively:",
  *opt("+13.6 eV and −27.2 eV", ["−13.6 eV and −27.2 eV", "+27.2 eV and −40.8 eV", "+6.8 eV and −20.4 eV"], "C"),
  "Bohr orbit energies: K = −E, U = 2E",
  "For an electron held in a circular orbit by the Coulomb force, K = ke²/2r and U = −ke²/r, so U = −2K and "
  "E = K + U = −K.",
  ["K = −E = +13.6 eV", "U = 2E = −27.2 eV", "Check: K + U = −13.6 eV"],
  why="−13.6 eV for K gives a negative kinetic energy, which is impossible. +27.2 and −40.8 eV, and +6.8 and "
      "−20.4 eV, add up to −13.6 eV but do not satisfy U = −2K.",
  ncert=NC + "'Atoms', Bohr model of the hydrogen atom (energy of the electron)", seconds=35, rc=True)

q(AN, "Rutherford scattering", "Basic", "direct",
  "In the alpha-particle scattering experiment, a very small fraction of the alpha particles were deflected through "
  "more than 90°, some almost straight back. This observation led Rutherford to conclude that:",
  *opt("the positive charge and most of the mass of the atom are concentrated in a tiny central region",
       ["electrons are spread uniformly through a sphere of positive charge",
        "most of the space inside an atom is empty",
        "alpha particles are strongly attracted by the electrons of the atom"], "D"),
  "Rutherford's nuclear model",
  "Turning a fast, heavy alpha particle back needs a very large repulsive force, which is possible only if the "
  "positive charge (and most of the mass) is packed into a very small nucleus that the particle can approach "
  "closely.",
  ["Large-angle scattering → very strong repulsion", "→ positive charge and mass concentrated in a tiny nucleus"],
  why="A uniform sphere of positive charge (Thomson's model) cannot produce large deflections. 'Mostly empty "
      "space' is concluded from the undeflected particles, not the large-angle ones. Electrons are far too light to "
      "deflect alpha particles appreciably.",
  ncert=NC + "'Atoms', alpha-particle scattering and Rutherford's nuclear model of atom", seconds=30)

dL = (4 - 2) * 6.6e-34 / (2 * math.pi)
close(dL, 2.10e-34, 1e-2)
close(6.6e-34 / (2 * math.pi), 1.05e-34, 1e-2)
close(4 * 6.6e-34 / (2 * math.pi), 4.2e-34, 1e-2)
close(6 * 6.6e-34 / (2 * math.pi), 6.3e-34, 1e-2)
q(AN, "Bohr model and hydrogen spectrum", "Intermediate", "numerical",
  "In the Bohr model of the hydrogen atom, the electron jumps from the n = 4 orbit to the n = 2 orbit. Taking "
  "h = 6.6 × 10⁻³⁴ J s, the magnitude of the change in its orbital angular momentum is about:",
  *opt("2.1 × 10⁻³⁴ J s", ["1.05 × 10⁻³⁴ J s", "4.2 × 10⁻³⁴ J s", "6.3 × 10⁻³⁴ J s"], "A"),
  "Bohr's quantisation condition: L = nh/2π",
  "The angular momentum in the nth orbit is n times h/2π, so the change between two orbits is (n₁ − n₂)h/2π.",
  ["L₄ − L₂ = (4 − 2)h/2π = h/π", "h/π = 6.6 × 10⁻³⁴/3.14 ≈ 2.1 × 10⁻³⁴ J s"],
  why="1.05 × 10⁻³⁴ J s is a single unit h/2π. 4.2 × 10⁻³⁴ J s is the angular momentum in the n = 4 orbit, not the "
      "change. 6.3 × 10⁻³⁴ J s adds the quantum numbers (4 + 2) instead of subtracting.",
  ncert=NC + "'Atoms', Bohr model of the hydrogen atom (quantisation of angular momentum)", seconds=40, rc=True)

rho_n = 3 * 1.66e-27 / (4 * math.pi * (1.2e-15) ** 3)
close(rho_n, 2.29e17, 1e-2)
close(1.66e-27 / (1.2e-15) ** 3, 9.6e17, 1e-2)
close(3 * 1.66e-27 / (4 * math.pi * (2.4e-15) ** 3), 2.87e16, 1e-2)
close(3 * 1.66e-27 / (4 * math.pi * (1.2e-14) ** 3), 2.29e14, 1e-2)
q(AN, "Nuclear size and mass defect", "Intermediate", "numerical",
  "Taking the radius of a nucleus of mass number A as R = R₀A^(1/3) with R₀ = 1.2 fm, and the mass of a nucleon as "
  "1.66 × 10⁻²⁷ kg, the density of nuclear matter is about:",
  *opt("2.3 × 10¹⁷ kg/m³", ["9.6 × 10¹⁷ kg/m³", "2.9 × 10¹⁶ kg/m³", "2.3 × 10¹⁴ kg/m³"], "D"),
  "Nuclear density: mass A × m_N divided by volume (4/3)πR₀³A",
  "Both the mass and the volume of a nucleus are proportional to A, so A cancels and the density is the same for "
  "all nuclei.",
  ["ρ = A m_N/[(4/3)π R₀³ A] = 3m_N/(4πR₀³)", "R₀³ = (1.2 × 10⁻¹⁵)³ = 1.73 × 10⁻⁴⁵ m³",
   "ρ = 3 × 1.66 × 10⁻²⁷/(4π × 1.73 × 10⁻⁴⁵) ≈ 2.3 × 10¹⁷ kg/m³"],
  why="9.6 × 10¹⁷ takes the volume as R₀³, leaving out 4π/3. 2.9 × 10¹⁶ uses 2R₀ (a diameter) as the radius. "
      "2.3 × 10¹⁴ takes 1 fm as 10⁻¹⁴ m.",
  ncert=NC + "'Nuclei', size of the nucleus", seconds=60, rc=True)

q(AN, "Bohr model and hydrogen spectrum", "Intermediate", "assertion_reason",
  ar("The Bohr model cannot be extended even to two-electron atoms such as helium.",
     "In the Bohr model of the hydrogen atom, the radius of the nth orbit is proportional to n²."),
  AR, ar_key(True, True, explains=False),
  "Limitations of the Bohr model",
  "The Bohr model applies to hydrogenic (one-electron) atoms; in a two-electron atom each electron interacts with "
  "the other electron as well as with the nucleus, which the model cannot handle (A true). The orbit radius "
  "r_n ∝ n² is a correct result of the model (R true), but it says nothing about why the model fails for "
  "many-electron atoms.",
  ["Bohr model fails for He (electron–electron interaction) → A true", "r_n ∝ n² → R true",
   "R is a property of hydrogen orbits, unrelated to the failure → option B"],
  why="R does not give the reason for A, so option A is wrong; both are true, so C and D are wrong.",
  ncert=NC + "'Atoms', Bohr model of the hydrogen atom (limitations)", seconds=40)

assert 1.008665 != 1.007276
q(AN, "Binding energy", "Intermediate", "statement_pair",
  sp("The mass of a stable nucleus is less than the total mass of its protons and neutrons taken separately.",
     "The mass of a free neutron is exactly equal to the mass of a proton."),
  SP, sp_key(True, False),
  "Mass defect and nucleon masses",
  "Energy (the binding energy) must be supplied to separate a nucleus into free nucleons, so the nucleus is "
  "lighter than its separated nucleons by ΔM = E_b/c². The neutron is slightly heavier than the proton "
  "(1.00866 u against 1.00727 u).",
  ["Mass defect ΔM > 0 for a bound nucleus → Statement I true", "m_n ≈ 1.00866 u > m_p ≈ 1.00727 u → Statement II false"],
  why="Statement I is true and Statement II is false; the other combinations are wrong.",
  ncert=NC + "'Nuclei', atomic masses and composition of nucleus; mass–energy and nuclear binding energy",
  seconds=40)

Zs = (1, 2, 3)
r_Z = [1 / Z for Z in Zs]
v_Z = [Z for Z in Zs]
T_Z = [2 * math.pi * r / v for r, v in zip(r_Z, v_Z)]
for Z, T in zip(Zs, T_Z):
    close(T, 2 * math.pi / Z ** 2)
q(AN, "Bohr model and hydrogen spectrum", "Intermediate", "match_list",
  ml("For a hydrogen-like ion of atomic number Z in a given orbit n of the Bohr model, match each quantity in "
     "List-I with the way it depends on Z in List-II.",
     ["Radius of the orbit", "Speed of the electron", "Magnitude of the total energy",
      "Time period of revolution of the electron"],
     ["Z", "Z²", "1/Z²", "1/Z"]),
  *mlo("A-IV, B-I, C-II, D-III",
       ["A-IV, B-I, C-III, D-II", "A-I, B-IV, C-II, D-III", "A-IV, B-II, C-I, D-III"], "D"),
  "Bohr model for hydrogen-like ions: r ∝ n²/Z, v ∝ Z/n, E ∝ Z²/n²",
  "A nucleus of charge Ze pulls the electron in more strongly: the orbit shrinks as 1/Z and the speed grows as Z. "
  "The energy goes as Z², and the period 2πr/v goes as (1/Z)/Z = 1/Z².",
  ["r ∝ 1/Z → A-IV", "v ∝ Z → B-I", "|E| ∝ Z² → C-II", "T = 2πr/v ∝ 1/Z² → D-III"],
  why="Swapping C and D gives the energy and the period each other's dependence. The other codes swap the radius "
      "and the speed.",
  ncert=NC + "'Atoms', Bohr model of the hydrogen atom", seconds=60, rc=True)

n_top = next(n for n in range(2, 10) if abs(13.6 * (1 - 1 / n ** 2) - 12.75) < 1e-9)
assert n_top == 4 and n_top * (n_top - 1) // 2 == 6
q(AN, "Bohr model and hydrogen spectrum", "Advanced", "numerical",
  "Hydrogen atoms in the ground state are excited by monochromatic radiation whose photons each have energy "
  "12.75 eV. Using E_n = −13.6/n² eV, the number of different wavelengths that can be present in the emission "
  "spectrum as the atoms return to the ground state is:",
  *opt("6", ["3", "4", "10"], "B"),
  "Excitation by photon absorption; number of spectral lines from level n: n(n − 1)/2",
  "A photon is absorbed only if its energy matches a level difference exactly. Find the level reached, then count "
  "every possible downward transition, including those through intermediate levels.",
  ["E₄ − E₁ = 13.6(1 − 1/16) = 12.75 eV → atoms reach n = 4",
   "Lines: 4→3, 4→2, 4→1, 3→2, 3→1, 2→1 = 4 × 3/2 = 6"],
  why="3 counts only the direct jumps from n = 4. 4 is the quantum number reached, not the number of lines. 10 "
      "would apply to atoms raised to n = 5.",
  ncert=NC + "'Atoms', the line spectra of the hydrogen atom", seconds=70, rc=True)

E_f = 200 * 1.6e-13
N_f = 200e6 / E_f
close(N_f, 6.25e18)
close(200e6 / (200 * 1.6e-19), 6.25e24)
close(200e3 / E_f, 6.25e15)
q(AN, "Fission and fusion", "Advanced", "numerical",
  "A nuclear reactor produces thermal power at the rate of 200 MW. Each fission of a ²³⁵U nucleus releases "
  "200 MeV of energy. Taking 1 MeV = 1.6 × 10⁻¹³ J, the number of fissions taking place per second is:",
  *opt("6.25 × 10¹⁸", ["1.0 × 10⁶", "6.25 × 10²⁴", "6.25 × 10¹⁵"], "A"),
  "Rate of fission = power/(energy per fission)",
  "Convert the energy per fission to joules, then divide the power (joules per second) by it.",
  ["Energy per fission = 200 × 1.6 × 10⁻¹³ = 3.2 × 10⁻¹¹ J", "N = 200 × 10⁶/(3.2 × 10⁻¹¹) = 6.25 × 10¹⁸ per second"],
  why="1.0 × 10⁶ divides 200 MW by 200 MeV without converting units. 6.25 × 10²⁴ converts MeV as if it were eV. "
      "6.25 × 10¹⁵ takes 200 MW as 200 kW.",
  ncert=NC + "'Nuclei', nuclear energy: fission", seconds=50, rc=True)

ruth_truth = {"a": True, "b": True, "c": False, "d": True, "e": False}
q(AN, "Rutherford scattering", "Advanced", "multi_statement",
  ms("Which of the following statements are correct?",
     ["According to classical electromagnetic theory, an electron revolving round the nucleus in Rutherford's "
      "model should radiate energy and spiral into the nucleus.",
      "Rutherford's model, combined with classical theory, would predict a continuous emission spectrum rather "
      "than a line spectrum.",
      "In the Bohr model, the frequency of the photon emitted in a transition equals the frequency of revolution of "
      "the electron in its initial orbit.",
      "An alpha particle aimed head-on at a nucleus (zero impact parameter) rebounds back along its path.",
      "The larger the impact parameter of an alpha particle, the larger the angle through which it is scattered."]),
  *mso(ruth_truth, "abd", ["abc", "bde", "ade"], "C"),
  "Rutherford's nuclear model, its classical difficulty, and the Bohr frequency condition",
  "An accelerating (revolving) charge radiates classically; the orbit would shrink and the frequency of the "
  "emitted radiation would change continuously, giving a continuous spectrum. In the Bohr model the photon's "
  "frequency is fixed by the energy difference, hν = E_i − E_f, not by the orbital frequency. In scattering, a "
  "head-on alpha particle rebounds (θ ≈ 180°), while a larger impact parameter means a smaller deflection.",
  ["(a) True", "(b) True", "(c) False: hν = E_i − E_f", "(d) True: θ ≈ π for b = 0",
   "(e) False: larger b → smaller scattering angle"],
  why="The other options include (c) or (e), which are false, or leave out a true statement.",
  ncert=NC + "'Atoms', alpha-particle trajectory (impact parameter); Bohr model of the hydrogen atom",
  seconds=70)


# ================================================================ Electronic Devices (B4 I5 A4)
V0b = 0.7
assert round(V0b - 0.4, 10) == 0.3 and round(V0b + 0.4, 10) == 1.1
q(ED, "p-n junction diode and rectifier", "Basic", "numerical",
  "The barrier potential of a silicon p-n junction is 0.7 V. The effective height of the potential barrier when "
  "the junction is forward biased by 0.4 V, and when it is reverse biased by 0.4 V, is respectively:",
  *opt("0.3 V and 1.1 V", ["1.1 V and 0.3 V", "0.7 V and 0.7 V", "0.3 V and 0.3 V"], "B"),
  "Effect of bias on the barrier: forward V₀ − V, reverse V₀ + V",
  "In forward bias the applied voltage opposes the built-in potential and lowers the barrier; in reverse bias it "
  "adds to it and raises the barrier.",
  ["Forward: 0.7 − 0.4 = 0.3 V", "Reverse: 0.7 + 0.4 = 1.1 V"],
  why="1.1 V and 0.3 V swaps the two cases. 0.7 V and 0.7 V assumes bias does not change the barrier. 0.3 V and "
      "0.3 V subtracts in both cases.",
  ncert=NC + "'Semiconductor Electronics', p-n junction diode under forward and reverse bias", seconds=30, rc=True)

Iz = 0.45 / 9
close(Iz, 0.050)
close(9 / 0.45, 20)
close(0.45 * 9, 4.05)
q(ED, "Zener diode", "Basic", "numerical",
  "A Zener diode has a breakdown voltage of 9.0 V and a maximum power rating of 0.45 W. The largest current it can "
  "safely carry in the breakdown region is:",
  *opt("50 mA", ["20 mA", "4.05 A", "5 mA"], "C"),
  "Power in the Zener: P = V_Z I_Z",
  "In breakdown the voltage across the Zener stays at V_Z, so the current is limited by the power it can "
  "dissipate.",
  ["I_max = P_max/V_Z = 0.45/9.0 = 0.050 A = 50 mA"],
  why="20 mA comes from V/P = 20, read as milliamperes. 4.05 A multiplies P by V. 5 mA is a slip of a power of ten.",
  ncert=NC + "'Semiconductor Electronics', Zener diode", seconds=30, rc=True)

q(ED, "Semiconductors", "Basic", "direct",
  "Which one of the following is a compound semiconductor?",
  *opt("Gallium arsenide (GaAs)", ["Silicon", "Germanium", "Copper"], "D"),
  "Elemental and compound semiconductors",
  "Silicon and germanium are elemental semiconductors. Compound semiconductors are formed from two or more "
  "elements, for example GaAs, CdS, CdSe and InP. Copper is a metal (conductor).",
  ["Si, Ge: elemental", "GaAs: compound of gallium and arsenic", "Cu: conductor"],
  why="Silicon and germanium are elemental semiconductors, and copper is a metal.",
  ncert=NC + "'Semiconductor Electronics', classification of metals, conductors and semiconductors", seconds=20)

nand = lambda a, b: int(not (a and b))
nor = lambda a, b: int(not (a or b))
pairs = [(0, 0), (0, 1), (1, 0), (1, 1)]
assert all(nand(a, a) == int(not a) for a in (0, 1))
assert all(nand(nand(a, b), nand(a, b)) == (a & b) for a, b in pairs)
assert all(nand(nand(a, a), nand(b, b)) == (a | b) for a, b in pairs)
assert [nor(a, b) for a, b in pairs] == [1, 0, 0, 0]
q(ED, "Logic gates", "Basic", "statement_pair",
  sp("The NAND gate is called a universal gate because the basic gates OR, AND and NOT can all be built using NAND "
     "gates alone.",
     "The output of a two-input NOR gate is 1 only when both its inputs are 0."),
  SP, sp_key(True, True),
  "NAND as a universal gate; NOR truth table",
  "A NAND gate with its inputs joined is a NOT gate; NAND followed by such a NOT gives AND; NOT on each input "
  "followed by NAND gives OR. NOR = NOT(A + B), which is 1 only for A = B = 0.",
  ["NAND realises NOT, AND and OR → Statement I true", "NOR outputs 1, 0, 0, 0 for 00, 01, 10, 11 → Statement II true"],
  why="Both statements are true, so every other option is wrong.", seconds=35, rc=True)

r_d = (0.72 - 0.70) / (20e-3 - 10e-3)
close(r_d, 2)
close(0.70 / 10e-3, 70)
close(0.72 / 20e-3, 36)
q(ED, "p-n junction diode and rectifier", "Intermediate", "numerical",
  "On the forward characteristic of a junction diode, the current is 10 mA at a forward voltage of 0.70 V and "
  "20 mA at 0.72 V. The dynamic resistance of the diode in this region is:",
  *opt("2 Ω", ["70 Ω", "36 Ω", "0.5 Ω"], "A"),
  "Dynamic resistance: r_d = ΔV/ΔI",
  "The diode's I–V characteristic is not linear, so its resistance is defined for small changes about the "
  "operating point as the ratio of the change in voltage to the change in current.",
  ["ΔV = 0.72 − 0.70 = 0.02 V, ΔI = 20 − 10 = 10 mA", "r_d = 0.02/0.010 = 2 Ω"],
  why="70 Ω and 36 Ω are the static ratios V/I at the two points. 0.5 Ω inverts the ratio (ΔI/ΔV).",
  ncert=NC + "'Semiconductor Electronics', p-n junction diode: V–I characteristics (dynamic resistance)",
  seconds=40, rc=True)

Vs_peak = 220 / 10 * math.sqrt(2)
close(Vs_peak, 31.1, 1e-2)
close(220 * math.sqrt(2), 311, 1e-2)
close(22 / math.sqrt(2), 15.6, 1e-2)
q(ED, "p-n junction diode and rectifier", "Intermediate", "numerical",
  "The primary of a step-down transformer with turns ratio N_p : N_s = 10 : 1 is connected to the 220 V (rms), "
  "50 Hz mains. The secondary feeds a half-wave rectifier consisting of an ideal diode in series with a load "
  "resistor. The peak voltage across the load is about:",
  *opt("31 V", ["22 V", "311 V", "15.6 V"], "C"),
  "Transformer ratio, then peak = √2 × rms; an ideal diode passes the positive peak unchanged",
  "The transformer reduces the rms voltage in the turns ratio. The half-wave rectifier passes alternate half "
  "cycles, so the load sees the full positive peak of the secondary voltage.",
  ["V_s(rms) = 220/10 = 22 V", "Peak = 22√2 ≈ 31 V"],
  why="22 V is the rms value, not the peak. 311 V ignores the transformer. 15.6 V divides by √2 instead of "
      "multiplying.",
  ncert=NC + "'Semiconductor Electronics', application of junction diode as a rectifier", seconds=45, rc=True)

ni, Nd = 1.5e16, 1e22
assert ni ** 2 / Nd < ni
q(ED, "Semiconductors", "Intermediate", "assertion_reason",
  ar("At a given temperature, an n-type semiconductor contains more holes than the intrinsic semiconductor of the "
     "same material.",
     "In thermal equilibrium, the electron and hole concentrations in a semiconductor satisfy n_e n_h = n_i²."),
  AR, ar_key(False, True),
  "Mass-action law in doped semiconductors",
  "Doping with donors raises n_e far above n_i. Because n_e n_h = n_i² (R true), n_h = n_i²/n_e falls below n_i: "
  "the many electrons recombine with holes. So an n-type sample has fewer holes than the intrinsic one, and A is "
  "false.",
  ["n_e n_h = n_i² → R true", "n_e ≫ n_i → n_h = n_i²/n_e ≪ n_i → A false"],
  why="A is false, so options A, B and C (which need A to be true) are wrong.",
  ncert=NC + "'Semiconductor Electronics', extrinsic semiconductor", seconds=40, rc=True)

q(ED, "Semiconductors", "Intermediate", "match_list",
  ml("Match each quantity in List-I with its approximate value in List-II.",
     ["Energy band gap of carbon (diamond)", "Energy band gap of silicon", "Energy band gap of germanium",
      "Threshold (cut-in) voltage of a germanium junction diode"],
     ["about 0.2 V", "about 5.4 eV", "about 0.7 eV", "about 1.1 eV"]),
  *mlo("A-II, B-IV, C-III, D-I",
       ["A-II, B-III, C-IV, D-I", "A-IV, B-II, C-III, D-I", "A-II, B-IV, C-I, D-III"], "D"),
  "Band gaps of C, Si and Ge; cut-in voltage of a Ge diode",
  "Diamond has a large gap (about 5.4 eV) and is an insulator; silicon (about 1.1 eV) and germanium (about "
  "0.7 eV) are semiconductors. The forward current of a germanium diode rises sharply beyond about 0.2 V (about "
  "0.7 V for silicon).",
  ["C: 5.4 eV → A-II", "Si: 1.1 eV → B-IV", "Ge: 0.7 eV → C-III", "Ge diode cut-in: 0.2 V → D-I"],
  why="Swapping B and C reverses the band gaps of silicon and germanium. The other codes give diamond a "
      "semiconductor's gap or mix up the band gap of germanium with its diode's cut-in voltage.",
  ncert=NC + "'Semiconductor Electronics', classification on the basis of energy bands; diode V–I characteristics",
  seconds=45)

hole_truth = {"a": True, "b": True, "c": True, "d": False, "e": False}
q(ED, "Semiconductors", "Intermediate", "multi_statement",
  ms("Which of the following statements about electrons and holes in a pure (intrinsic) semiconductor are correct?",
     ["A hole is a vacancy left in a covalent bond, and it behaves as a positive charge carrier.",
      "Electron–hole pairs are produced by thermal energy breaking covalent bonds.",
      "The motion of a hole under an applied field actually results from bound electrons jumping from one covalent "
      "bond into a neighbouring vacancy.",
      "Holes are free positively charged particles, of the same mass as protons, released from the nuclei.",
      "In thermal equilibrium, electrons and holes never recombine."]),
  *mso(hole_truth, "abc", ["abd", "bce", "ace"], "A"),
  "Intrinsic semiconductors: holes, generation and recombination",
  "Thermal energy frees some electrons from covalent bonds, leaving vacancies (holes) with an effective positive "
  "charge. A hole moves when a bound electron from a neighbouring bond fills it, leaving a new vacancy. In "
  "equilibrium, the rate of generation equals the rate of recombination of electrons and holes.",
  ["(a) True", "(b) True", "(c) True", "(d) False: a hole is not a particle from the nucleus",
   "(e) False: recombination goes on and balances generation"],
  why="The other options include (d) or (e), which are false, or leave out a true statement.",
  ncert=NC + "'Semiconductor Electronics', intrinsic semiconductor", seconds=55)

Vz, Rs, RL = 6.0, 500, 1200
Vmin = Vz + (Vz / RL) * Rs
close(Vmin, 8.5)
close(Vz * (1 + RL / Rs), 20.4)
close((Vz / RL) * Rs, 2.5)
q(ED, "Zener diode", "Advanced", "numerical",
  "A Zener diode of breakdown voltage 6.0 V is used as a voltage regulator: a 500 Ω series resistor connects it to "
  "a variable DC input, and a 1.2 kΩ load is connected across the Zener. Treating the Zener as drawing current only "
  "when the voltage across it would otherwise exceed 6.0 V, the minimum input voltage for which the load voltage "
  "stays at 6.0 V is:",
  *opt("8.5 V", ["6.0 V", "20.4 V", "2.5 V"], "D"),
  "Zener regulator: at the edge of regulation the Zener current is zero and the load takes all the current",
  "At the minimum input, the Zener just reaches breakdown: the series resistor and the load form a voltage divider "
  "that puts exactly 6.0 V across the load.",
  ["Load current at 6.0 V: I_L = 6.0/1200 = 5.0 mA", "Drop across 500 Ω = 5.0 mA × 500 = 2.5 V",
   "V_in(min) = 6.0 + 2.5 = 8.5 V"],
  why="6.0 V ignores the drop across the series resistor. 20.4 V inverts the divider ratio (6.0 × (1 + R_L/R_s)). "
      "2.5 V is only the drop across the series resistor.",
  ncert=NC + "'Semiconductor Electronics', Zener diode as voltage regulator", seconds=80, rc=True)

and_ = lambda a, b: a & b
Y11 = [nor(and_(a, b), a) for a, b in pairs]
assert Y11 == [int(not a) for a, b in pairs]
assert Y11 != [int(not b) for a, b in pairs] and Y11 != [nand(a, b) for a, b in pairs]
assert Y11 != [a | b for a, b in pairs]
q(ED, "Logic gates", "Advanced", "direct",
  "Inputs A and B are fed to an AND gate. The output of the AND gate and the input A are then fed to a NOR gate, "
  "whose output is Y. The output Y is equal to:",
  *opt("Ā (NOT A)", ["B̄ (NOT B)", "NOT(A · B)", "A + B"], "B"),
  "Truth table of a combination of gates",
  "Y = NOT(A·B + A). Whenever A = 1 the NOR has an input 1, so Y = 0; when A = 0 both NOR inputs are 0, so Y = 1. "
  "Hence Y = Ā, whatever B is.",
  ["(A, B) = (0, 0): A·B = 0, NOR(0, 0) = 1", "(0, 1): NOR(0, 0) = 1", "(1, 0): NOR(0, 1) = 0",
   "(1, 1): NOR(1, 1) = 0 → Y = 1, 1, 0, 0 = Ā"],
  why="B̄ would give 1, 0, 1, 0. NAND gives 1, 1, 1, 0 (it differs at A = 1, B = 0). A + B gives 0, 1, 1, 1.",
  seconds=60, rc=True)

q(ED, "Zener diode", "Advanced", "statement_pair",
  sp("Zener breakdown occurs when the Zener diode is forward biased beyond about 0.7 V.",
     "In the breakdown region, a large change in the current through a Zener diode produces a large change in the "
     "voltage across it."),
  SP, sp_key(False, False),
  "Zener breakdown and regulation",
  "Breakdown happens under reverse bias: at the Zener voltage the strong field in the very thin depletion region "
  "pulls electrons out of their bonds and the reverse current rises sharply. In this region the voltage stays "
  "almost constant over a large range of current, which is why the Zener diode is used as a regulator.",
  ["Breakdown is a reverse-bias effect → Statement I false",
   "Large ΔI gives very small ΔV in breakdown → Statement II false"],
  why="Both statements are false, so every other option is wrong.",
  ncert=NC + "'Semiconductor Electronics', Zener diode", seconds=40)

iv_truth = {"a": True, "b": True, "c": False, "d": False, "e": True}
q(ED, "p-n junction diode and rectifier", "Advanced", "multi_statement",
  ms("Which of the following statements about the V–I characteristics of a p-n junction diode are correct?",
     ["Beyond the threshold voltage, the forward current increases very rapidly with a small increase of voltage.",
      "Under reverse bias below breakdown, the current is very small (of the order of µA) and nearly independent of "
      "the reverse voltage.",
      "In forward bias, the dynamic resistance of the diode is larger at larger currents.",
      "At forward voltages below the threshold voltage, the forward current is very large.",
      "For a silicon diode, the threshold voltage is about 0.7 V."]),
  *mso(iv_truth, "abe", ["abc", "bde", "ace"], "C"),
  "Forward and reverse characteristics of a junction diode",
  "Below the threshold the forward current is negligible; above it the current rises steeply, so ΔV/ΔI (the "
  "dynamic resistance) becomes smaller at larger currents. The reverse current is a small minority-carrier current "
  "that hardly changes with voltage until breakdown. The threshold is about 0.7 V for silicon (about 0.2 V for "
  "germanium).",
  ["(a) True", "(b) True", "(c) False: steeper curve → smaller r_d at large current",
   "(d) False: the current is negligible below threshold", "(e) True"],
  why="The other options include (c) or (d), which are false, or leave out a true statement.",
  ncert=NC + "'Semiconductor Electronics', p-n junction diode: V–I characteristics", seconds=60)


# ================================================================ Experimental Skills (B2 I3 A2)
LC_v = 0.5 - 19 * 0.5 / 20
close(LC_v, 0.025)
close(0.5 / 19, 0.0263, 1e-2)
q(EXP, "Vernier calipers and screw gauge", "Basic", "numerical",
  "The main scale of a vernier calipers is graduated in divisions of 0.5 mm, and 20 divisions of the vernier scale "
  "coincide with 19 divisions of the main scale. The least count of the instrument is:",
  *opt("0.025 mm", ["0.05 mm", "0.026 mm", "0.5 mm"], "A"),
  "Least count = 1 MSD − 1 VSD",
  "The least count is the difference between one main-scale division and one vernier-scale division.",
  ["1 VSD = (19/20) × 0.5 mm = 0.475 mm", "LC = 0.5 − 0.475 = 0.025 mm"],
  why="0.05 mm takes a main-scale division as 1 mm. 0.026 mm divides 0.5 mm by 19 instead of 20. 0.5 mm is one "
      "main-scale division.",
  seconds=35, rc=True)

m_u = F(60) * (80 - 50) / (50 - 10)
assert m_u == 45
assert F(60) * 40 / 30 == 80 and F(60) * 10 / 80 == F(15, 2)
q(EXP, "Mechanics experiments", "Basic", "numerical",
  "A uniform metre scale balances horizontally on a knife edge placed at its 50.0 cm mark. When an unknown mass is "
  "hung at the 10.0 cm mark and a 60 g mass at the 80.0 cm mark, the scale again balances on the knife edge at the "
  "50.0 cm mark. The unknown mass is:",
  *opt("45 g", ["80 g", "60 g", "7.5 g"], "C"),
  "Principle of moments about the knife edge",
  "The scale's own weight acts at the 50 cm mark, on the knife edge, so it has no moment. The moments of the two "
  "hanging masses about the knife edge must be equal.",
  ["Arms: unknown 50 − 10 = 40 cm, known 80 − 50 = 30 cm", "m × 40 = 60 × 30 → m = 45 g"],
  why="80 g interchanges the arms. 60 g assumes equal arms. 7.5 g uses the scale readings 10 and 80 as the arms.",
  ncert="Class 11 Physics, 'System of Particles and Rotational Motion', principle of moments", seconds=40, rc=True)

R3, S3 = F(2100), F(100)
G3 = R3 * S3 / (R3 - S3)
assert G3 == 105
# check: galvanometer current halves when the shunt is added
I_no = 1 / (R3 + G3)
I_tot = 1 / (R3 + G3 * S3 / (G3 + S3))
assert I_tot * S3 / (G3 + S3) == I_no / 2
close(float(R3 * S3 / (R3 + S3)), 95.45, 1e-3)
q(EXP, "Electrical experiments", "Intermediate", "numerical",
  "In the half-deflection method for finding the resistance G of a galvanometer, the galvanometer, a resistance "
  "R = 2100 Ω and a cell of negligible internal resistance are in series, and the galvanometer shows a deflection "
  "θ. When a shunt S = 100 Ω is connected across the galvanometer, with R unchanged, the deflection falls to θ/2. "
  "The resistance of the galvanometer is:",
  *opt("105 Ω", ["100 Ω", "95.5 Ω", "2000 Ω"], "B"),
  "Half-deflection method: G = RS/(R − S)",
  "Write the galvanometer current with and without the shunt, and set the second equal to half of the first.",
  ["Without shunt: I_g = E/(R + G)",
   "With shunt: I_g′ = [E/(R + GS/(G + S))] × S/(G + S) = ES/[R(G + S) + GS]",
   "I_g′ = I_g/2 → G(R − S) = RS → G = 2100 × 100/2000 = 105 Ω"],
  why="100 Ω takes G = S, which holds only when R ≫ G. 95.5 Ω uses RS/(R + S). 2000 Ω is R − S.",
  seconds=75, rc=True)

q(EXP, "Electrical experiments", "Intermediate", "statement_pair",
  sp("In the experiment to verify Ohm's law, the ammeter is connected in series with the resistor and the voltmeter "
     "in parallel with it.",
     "On the reverse-bias characteristic of a Zener diode, the breakdown voltage is read as the reverse voltage at "
     "which the reverse current increases sharply."),
  SP, sp_key(True, True),
  "Connection of meters; Zener characteristic",
  "An ammeter must carry the current through the resistor, so it goes in series; a voltmeter must have the same "
  "potential difference across it as the resistor, so it goes in parallel. On a Zener's reverse characteristic the "
  "current stays tiny until the breakdown voltage, where it rises steeply at almost constant voltage.",
  ["Ammeter in series, voltmeter in parallel → Statement I true",
   "Breakdown voltage = knee of the reverse characteristic → Statement II true"],
  why="Both statements are true, so every other option is wrong.", seconds=35)

q(EXP, "Electrical experiments", "Intermediate", "match_list",
  ml("A student tests each component in List-I by connecting it, in series with a low-voltage DC source and a "
     "current-indicating meter, first one way round and then the other. Match each component with the observation "
     "in List-II.",
     ["Resistor", "Junction diode", "Light emitting diode", "Capacitor (initially uncharged)"],
     ["A brief current that dies away to zero; no steady current either way round",
      "A steady current in one direction only, and the component glows",
      "The same steady current both ways round",
      "A steady current in one direction only, and the component does not glow"]),
  *mlo("A-III, B-IV, C-II, D-I",
       ["A-III, B-II, C-IV, D-I", "A-I, B-IV, C-II, D-III", "A-III, B-IV, C-I, D-II"], "A"),
  "Identifying a resistor, a diode, an LED and a capacitor",
  "A resistor conducts equally in both directions. A diode conducts in one direction only; an LED also conducts "
  "one way only but emits light. A capacitor allows only a momentary charging current and then blocks steady DC.",
  ["Resistor: same current both ways → A-III", "Diode: one way, no light → B-IV", "LED: one way, glows → C-II",
   "Capacitor: momentary current only → D-I"],
  why="Swapping B and C confuses the diode with the LED. The other codes give the capacitor or the resistor a "
      "steady one-way current.",
  seconds=45)

f6, l1, l2 = 500, 0.160, 0.500
lam6 = 2 * (l2 - l1)
close(f6 * lam6, 340)
close((l2 - 3 * l1) / 2, 0.010)
close(l2 - 3 * l1, 0.020)
close(4 * f6 * l1, 320)
close(f6 * (l2 - l1), 170)
q(EXP, "Mechanics experiments", "Advanced", "numerical",
  "In a resonance-tube experiment with a tuning fork of frequency 500 Hz, the first and second resonances occur at "
  "air-column lengths of 16.0 cm and 50.0 cm. The speed of sound in air and the end correction of the tube are, "
  "respectively:",
  *opt("340 m/s and 1.0 cm", ["340 m/s and 2.0 cm", "170 m/s and 1.0 cm", "320 m/s and 0 cm"], "D"),
  "Closed pipe with end correction e: l₁ + e = λ/4, l₂ + e = 3λ/4",
  "Subtracting the two resonance conditions removes the end correction and gives λ/2; putting λ back into the "
  "first condition gives e.",
  ["l₂ − l₁ = λ/2 → λ = 2 × 34.0 = 68.0 cm", "v = fλ = 500 × 0.680 = 340 m/s",
   "e = λ/4 − l₁ = 17.0 − 16.0 = 1.0 cm (equivalently e = (l₂ − 3l₁)/2)"],
  why="2.0 cm forgets to halve (l₂ − 3l₁). 170 m/s takes λ = l₂ − l₁. 320 m/s uses v = 4fl₁, ignoring the end "
      "correction.",
  ncert="Class 11 Physics, 'Waves', standing waves in a pipe closed at one end", seconds=80, rc=True)

q(EXP, "Optics experiments", "Advanced", "assertion_reason",
  ar("In the u–v method for finding the focal length of a concave mirror, the image needle is adjusted until there "
     "is maximum parallax between it and the image of the object needle.",
     "When there is no parallax between two objects, they are at the same distance from the eye."),
  AR, ar_key(False, True),
  "Removal of parallax to locate an image",
  "Two objects at different distances appear to move relative to each other when the eye is moved sideways "
  "(parallax). When they are at the same place there is no relative movement (R true). The image needle is "
  "therefore adjusted until there is NO parallax with the image, which places it exactly at the image; A is "
  "false.",
  ["No parallax ⇔ same position → R true", "Image needle set for no parallax, not maximum → A false"],
  why="A is false, so options A, B and C (which need A to be true) are wrong.", seconds=40)


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
    assert all(28 <= keys[k] <= 31 for k in LETTERS), keys
    texts = [x["question_text"] for x in QS]
    assert len(set(texts)) == len(texts)
    doc = {"schema_version": "1.0", "batch_id": "BATCH_003", "created_at": TODAY,
           "notes": "Package PHY_003_p2: 118 original Physics questions (Current Electricity to Experimental Skills), "
                    "NEET_PHY_000633..000750. Numerical answers recomputed by tools/batch_003/PHY_003_p2.py.",
           "stimuli": [], "questions": QS}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {OUT}: {len(QS)} questions")
    print("difficulty", dict(Counter(x["difficulty"] for x in QS)))
    print("formats", dict(fmts))
    print("keys", dict(sorted(keys.items())))


if __name__ == "__main__":
    main()
