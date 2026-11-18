"""Builder for batches/parts/BATCH_008_PHY_p2.json (package PHY_008_p2 of BATCH_008).

Physics, 125 original questions, NEET_PHY_001876..NEET_PHY_002000: Current Electricity, Magnetic Effects of Current
and Magnetism, Electromagnetic Induction and Alternating Currents, Electromagnetic Waves, Optics, Dual Nature of
Matter and Radiation, Atoms and Nuclei, Electronic Devices, Experimental Skills.

Every numerical answer is recomputed below with an assert next to its question; multi-statement, assertion-reason
and statement-pair keys are derived from truth tables; the plan quota, format mix and answer-key balance are
asserted before anything is written. If any assert fails, nothing is written.

    python tools/batch_008/PHY_008_p2.py        (run from docs/neet-bank)
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
PLAN = ROOT / "batches" / "plans" / "BATCH_008_plan.json"
OUT = ROOT / "batches" / "parts" / "BATCH_008_PHY_p2.json"
PACKAGE = "PHY_008_p2"
FIRST_ID = 1876
COUNT = 125

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
dims = (1, 2, 4)
res = [F(l, a * b) for l, a, b in ((dims[0], dims[1], dims[2]), (dims[1], dims[0], dims[2]), (dims[2], dims[0], dims[1]))]
assert max(res) / min(res) == 16 and F(4, 1) ** 3 == 64
q(CE, "Resistivity and temperature", "Basic", "numerical",
  "A rectangular block of a metal measures 1 cm × 2 cm × 4 cm. Its resistance is measured between each pair of "
  "opposite faces in turn, the current being spread uniformly over the two faces used. The ratio of the largest of "
  "these three resistances to the smallest is:",
  *opt("16", ["4", "64", "1/16"], "A"),
  "R = ρl/A: the resistance is largest for the longest current path through the smallest cross-section",
  "The resistivity is fixed by the material. Between the 1 cm × 2 cm faces the current path is 4 cm long through an "
  "area of 2 cm²; between the 2 cm × 4 cm faces the path is 1 cm long through 8 cm².",
  ["R_max ∝ l/A = 4/2 = 2 (in cm⁻¹)", "R_min ∝ 1/8", "R_max/R_min = 2 ÷ (1/8) = 16"],
  shortcut="Ratio = (l_max/l_min) × (A_max/A_min) = 4 × 4 = 16.",
  why="4 uses only the ratio of the lengths (or only the ratio of the face areas); both change together. 64 cubes "
      "the length ratio. 1/16 is the smallest-to-largest ratio, inverted.",
  ncert=CEC + "Ohm's law; resistivity (R = ρl/A)", seconds=45, rc=True)

E_kwh = F(2) * 3 * 30
assert E_kwh == 180 and F(2) * 3 == 6 and F(2) * 30 == 60 and 2000 * 3 * 30 == 180000
q(CE, "Drift velocity and Ohm's law", "Basic", "numerical",
  "An electric heater rated 2.0 kW is used for 3 hours every day. The electrical energy it consumes in 30 days is:",
  *opt("180 kWh", ["6.0 kWh", "60 kWh", "1.8 × 10⁵ kWh"], "B"),
  "Electrical energy = power × time; 1 kWh is the energy used by a 1 kW appliance in 1 hour",
  "The heater uses 2.0 kW for 3 h each day, i.e. 6 kWh a day, for 30 days.",
  ["Energy per day = 2.0 kW × 3 h = 6.0 kWh", "Energy in 30 days = 6.0 × 30 = 180 kWh"],
  why="6.0 kWh is the energy for a single day. 60 kWh leaves out the 3 hours a day. 1.8 × 10⁵ kWh puts the power "
      "in watts (2000 W) but keeps the unit kWh.",
  ncert=CEC + "electrical energy, power", seconds=30, rc=True)

q(CE, "Cells, emf and internal resistance", "Basic", "direct",
  "A cell is supplying a steady current to an external resistor. Inside the cell (through its electrolyte), the "
  "conventional current flows:",
  *opt("from the negative terminal to the positive terminal",
       ["from the positive terminal to the negative terminal",
        "in neither direction, because current flows only in the external circuit",
        "from the positive terminal to the negative terminal, but only if the internal resistance is negligible"], "C"),
  "A cell is a source of emf: inside it, charges are driven against the electrostatic field",
  "In a steady circuit the current is the same all round the closed loop. In the external resistor the conventional "
  "current goes from the positive terminal to the negative terminal, so to complete the loop it must go from the "
  "negative terminal to the positive terminal inside the cell. The chemical action of the cell does the work of "
  "moving the charges this way, against the electrostatic field.",
  ["Steady current: same current all round the closed loop",
   "Outside: positive terminal → resistor → negative terminal",
   "Inside the cell: negative terminal → positive terminal"],
  why="The positive-to-negative direction holds only in the external circuit (or inside a cell that is being "
      "charged). Current does flow through the cell, which is part of the closed loop. The internal resistance does "
      "not decide the direction of the current inside the cell.",
  ncert=CEC + "cells, emf, internal resistance", seconds=30)

drops = [-5, +12, -3]
x_DA = -sum(drops)
assert x_DA == -4 and abs(sum(drops)) == 4 and sum(abs(d) for d in drops) == 20
q(CE, "Kirchhoff's laws", "Basic", "numerical",
  "In a closed loop ABCDA of a circuit carrying steady currents, the potential falls by 5 V from A to B (across a "
  "resistor), rises by 12 V from B to C (across a cell) and falls by 3 V from C to D (across another resistor). The "
  "change in potential from D back to A is:",
  *opt("a fall of 4 V", ["a rise of 4 V", "a fall of 20 V", "zero"], "D"),
  "Kirchhoff's loop rule: the algebraic sum of the changes in potential round any closed loop is zero",
  "Going once round the loop brings us back to the starting point, so all the changes of potential must add up to "
  "zero: −5 + 12 − 3 + ΔV_DA = 0.",
  ["−5 V + 12 V − 3 V = +4 V from A to D", "ΔV_DA = −4 V, i.e. a fall of 4 V"],
  why="A rise of 4 V has the sign wrong: the potential has already risen by 4 V from A to D, so it must fall by 4 V "
      "on the way back. 20 V adds the magnitudes of the three changes and ignores their signs. Zero would hold only "
      "if the first three changes already summed to zero.",
  ncert=CEC + "Kirchhoff's rules", seconds=35, rc=True)

R_side = F(16, 4)
R_adj = R_side * 3 * R_side / (R_side + 3 * R_side)
assert R_adj == 3 and R_side == 4 and 3 * R_side == 12
q(CE, "Combination of resistors", "Basic", "numerical",
  "A uniform wire of resistance 16 Ω is bent into the shape of a square, its two ends being joined. The resistance "
  "between two adjacent corners of the square is:",
  *opt("3 Ω", ["4 Ω", "12 Ω", "16 Ω"], "A"),
  "Parallel combination of the two paths between the chosen points",
  "Each side has a resistance of 16/4 = 4 Ω. Between two adjacent corners there are two paths in parallel: one side "
  "(4 Ω) and the other three sides in series (12 Ω).",
  ["Each side = 4 Ω", "Paths: 4 Ω and 12 Ω in parallel", "R = (4 × 12)/(4 + 12) = 3 Ω"],
  why="4 Ω takes only the single side and ignores the parallel path round the other three sides. 12 Ω takes only "
      "the longer path. 16 Ω is the resistance of the whole straight wire.",
  ncert=CEC + "combination of resistors - series and parallel", seconds=40, rc=True)

q(CE, "Drift velocity and Ohm's law", "Basic", "statement_pair",
  sp("For a metallic conductor, the potential difference across it is proportional to the current through it only "
     "so long as its temperature and other physical conditions remain unchanged.",
     "When a uniform wire is cut into two equal halves, the resistivity of the material of each half is half that "
     "of the original wire."),
  SP, sp_key(True, False),
  "Ohm's law and the difference between resistance and resistivity",
  "Statement I is true: Ohm's law, V = IR with R constant, holds for a metal only when its temperature (and other "
  "physical conditions) do not change; heating the conductor changes its resistance. Statement II is false: "
  "resistivity is a property of the material at a given temperature and does not depend on the dimensions of the "
  "wire. Cutting the wire halves its resistance, not its resistivity.",
  ["I: R constant only at fixed temperature → true", "II: ρ depends on material and temperature, not size → false"],
  why="Statement II confuses resistivity with resistance, which is the quantity that halves.",
  ncert=CEC + "Ohm's law; resistivity of various materials", seconds=35)

# ---- Intermediate
n_e = F(9000) / F(60, 1000) * F(6) * 10 ** 23
v_d = F(72, 10) / (n_e * F(16, 10) * F(1, 10 ** 19) * F(1, 10 ** 6))
assert n_e == 9 * 10 ** 28 and v_d == F(5, 10000)
assert F(72, 10) / (n_e / 1000 * F(16, 10 ** 20) * F(1, 10 ** 6)) == F(1, 2)
assert F(72, 10) / (2 * n_e * F(16, 10 ** 20) * F(1, 10 ** 6)) == F(25, 100000)
close(float(F(72, 10) / (F(9000) * F(6) * 10 ** 23 * F(16, 10 ** 20) * F(1, 10 ** 6))), 8.33e-3, 1e-3)
q(CE, "Drift velocity and Ohm's law", "Intermediate", "numerical",
  "A metal has one free electron per atom. Its density is 9.0 × 10³ kg m⁻³ and its molar mass is 60 g mol⁻¹. A wire "
  "of this metal, of cross-sectional area 1.0 mm², carries a steady current of 7.2 A. Taking Avogadro's number as "
  "6.0 × 10²³ mol⁻¹ and e = 1.6 × 10⁻¹⁹ C, the drift speed of the free electrons is:",
  *opt("0.50 mm/s", ["0.50 m/s", "0.25 mm/s", "8.3 mm/s"], "B"),
  "Number density of free electrons from density and molar mass; I = neAv_d",
  "One cubic metre of the metal has a mass of 9.0 × 10³ kg = 150 mol, i.e. 150 × 6.0 × 10²³ = 9.0 × 10²⁸ atoms, "
  "and so 9.0 × 10²⁸ free electrons. The drift speed then follows from I = neAv_d.",
  ["n = (ρ/M)N_A = (9.0 × 10³/0.060) × 6.0 × 10²³ = 9.0 × 10²⁸ m⁻³",
   "neA = 9.0 × 10²⁸ × 1.6 × 10⁻¹⁹ × 1.0 × 10⁻⁶ = 1.44 × 10⁴ C m⁻¹",
   "v_d = 7.2/(1.44 × 10⁴) = 5.0 × 10⁻⁴ m/s = 0.50 mm/s"],
  why="0.50 m/s uses the molar mass as 60 kg mol⁻¹ (grams not converted), making n 1000 times too small. 0.25 mm/s "
      "assumes two free electrons per atom. 8.3 mm/s multiplies the density by N_A without dividing by the molar "
      "mass.",
  ncert=CEC + "drift of electrons and the origin of resistivity", seconds=90, rc=True)

aP, aQ = F(4, 1000), F(2, 1000)
t_eq = (12 - 10) / (10 * aP - 12 * aQ)
assert t_eq == 125
assert F(2) / (10 * aP) == 50 and F(2) / (10 * (aP - aQ)) == 100
close(float(F(2) / (12 * (aP - aQ))), 83.3, 1e-3)
q(CE, "Resistivity and temperature", "Intermediate", "numerical",
  "Wire P has a resistance of 10 Ω at 0 °C and a temperature coefficient of resistance of 4.0 × 10⁻³ °C⁻¹. Wire Q "
  "has a resistance of 12 Ω at 0 °C and a temperature coefficient of resistance of 2.0 × 10⁻³ °C⁻¹. Both "
  "coefficients are referred to 0 °C and may be taken as constant. The temperature at which the two wires have equal "
  "resistances is:",
  *opt("125 °C", ["50 °C", "100 °C", "83 °C"], "D"),
  "R_t = R₀(1 + αt) for each wire",
  "Wire P starts with the smaller resistance but its resistance rises faster. Equate the two expressions and solve "
  "for t.",
  ["10(1 + 0.004t) = 12(1 + 0.002t)", "10 + 0.040t = 12 + 0.024t", "0.016t = 2 → t = 125 °C"],
  why="50 °C lets only P's resistance change (10(1 + 0.004t) = 12). 100 °C and 83 °C multiply the difference of the "
      "two coefficients by a single base resistance (10 Ω or 12 Ω), instead of using 10α_P − 12α_Q.",
  ncert=CEC + "temperature dependence of resistivity", seconds=75, rc=True)

V_m, I_m, RA = F(5), F(1, 2), F(1, 2)
R_true = V_m / I_m - RA
assert R_true == F(19, 2) and V_m / I_m == 10 and V_m / I_m + RA == F(21, 2) and V_m / I_m - I_m * RA == F(39, 4)
q(CE, "Drift velocity and Ohm's law", "Intermediate", "numerical",
  "To measure an unknown resistance R, it is connected in series with an ammeter of resistance 0.50 Ω, and a "
  "voltmeter is connected across the series combination of R and the ammeter. The voltmeter reads 5.0 V and the "
  "ammeter reads 0.50 A. The value of R is:",
  *opt("9.5 Ω", ["10 Ω", "10.5 Ω", "9.75 Ω"], "C"),
  "Ohm's law applied to the part of the circuit across which the voltmeter is connected",
  "The voltmeter measures the potential difference across R and the ammeter together, and the ammeter reading is "
  "the current through both. So V/I is the total resistance R + R_A.",
  ["V/I = 5.0/0.50 = 10 Ω = R + R_A", "R = 10 − 0.50 = 9.5 Ω"],
  why="10 Ω ignores the resistance of the ammeter, which is inside the voltmeter's connections. 10.5 Ω adds the "
      "ammeter resistance instead of subtracting it. 9.75 Ω subtracts the ammeter's potential drop (0.25 V) as if it "
      "were a resistance in ohms.",
  ncert=CEC + "Ohm's law", seconds=60, rc=True)

eps4 = 12
r4 = math.sqrt(2 * 8)
assert r4 == 4
P2 = (F(eps4) / (2 + 4)) ** 2 * 2
P8 = (F(eps4) / (8 + 4)) ** 2 * 8
assert P2 == P8 == 8 and F(eps4 ** 2, 4 * 4) == 9 and (F(eps4) / (2 + 6)) ** 2 * 2 == F(9, 2)
q(CE, "Cells, emf and internal resistance", "Intermediate", "numerical",
  "A battery of emf 12 V delivers exactly the same power to an external resistor of 2 Ω as to an external resistor of "
  "8 Ω (each connected alone across it). The internal resistance of the battery and the power delivered in either "
  "case are, respectively:",
  *opt("4 Ω and 8 W", ["5 Ω and 8 W", "4 Ω and 9 W", "6 Ω and 4.5 W"], "A"),
  "Power in the external resistor P = ε²R/(R + r)²",
  "Equating the power for R₁ = 2 Ω and R₂ = 8 Ω gives R₁(R₂ + r)² = R₂(R₁ + r)², which simplifies to r² = R₁R₂.",
  ["2(8 + r)² = 8(2 + r)² → (8 + r) = 2(2 + r) → r = 4 Ω", "With 2 Ω: I = 12/6 = 2 A, P = 4 × 2 = 8 W",
   "With 8 Ω: I = 12/12 = 1 A, P = 1 × 8 = 8 W"],
  shortcut="Equal power in R₁ and R₂ means r = √(R₁R₂).",
  why="5 Ω is the arithmetic mean of 2 Ω and 8 Ω; the condition gives the geometric mean. 9 W is the maximum "
      "power ε²/4r, delivered only when R = r = 4 Ω, not in these two cases. 6 Ω (the difference 8 − 2) does not "
      "make the two powers equal.",
  ncert=CEC + "cells, emf, internal resistance; electrical energy, power", seconds=90, rc=True)

def pratio(x):
    return F((1 + x) ** 2, x)
assert pratio(F(2)) == F(9, 2) and pratio(F(1)) == 4 and pratio(F(3)) == F(16, 3) and pratio(F(9, 2)) != F(9, 2)
q(CE, "Combination of resistors", "Intermediate", "numerical",
  "Two resistors are connected first in series and then in parallel across the same ideal battery. The total power "
  "drawn from the battery in the parallel arrangement is 4.5 times that drawn in the series arrangement. The ratio "
  "of the larger resistance to the smaller resistance is:",
  *opt("2", ["4.5", "1", "3"], "B"),
  "For a fixed voltage, P = V²/R_eq, so P_parallel/P_series = R_series/R_parallel",
  "Let the resistances be R and xR. Then R_series = R(1 + x) and R_parallel = Rx/(1 + x), so the power ratio is "
  "(1 + x)²/x.",
  ["(1 + x)²/x = 4.5 → x² + 2x + 1 = 4.5x", "2x² − 5x + 2 = 0 → x = 2 or x = 1/2",
   "Ratio of larger to smaller = 2"],
  why="4.5 takes the power ratio itself as the resistance ratio. A ratio of 1 (equal resistors) gives a power ratio "
      "of 4, and a ratio of 3 gives 16/3 ≈ 5.3, not 4.5.",
  ncert=CEC + "combination of resistors - series and parallel; electrical energy, power", seconds=90, rc=True)

Q_heat = 1 * 4200 * 80
t_k = F(Q_heat) / (F(8, 10) * 1000)
assert t_k == 420 and t_k / 60 == 7 and F(Q_heat, 1000) / 60 == F(28, 5)
close(float(Q_heat * F(8, 10) / 1000 / 60), 4.48, 1e-3)
assert F(1 * 4200 * 100) / 800 / 60 == F(35, 4)
q(CE, "Drift velocity and Ohm's law", "Intermediate", "numerical",
  "An electric kettle draws a power of 1.0 kW from the mains. It heats 1.0 kg of water from 20 °C to 100 °C, and "
  "80% of the electrical energy it draws goes into heating the water. Taking the specific heat capacity of water as "
  "4200 J kg⁻¹ K⁻¹, the time taken is:",
  *opt("7.0 min", ["5.6 min", "4.5 min", "8.75 min"], "D"),
  "Electrical energy = Pt; only the useful fraction of it heats the water",
  "Heat needed by the water = mcΔT. The kettle supplies 1000 J each second, of which only 800 J reaches the water.",
  ["Heat needed = 1.0 × 4200 × 80 = 3.36 × 10⁵ J", "Useful power = 0.80 × 1000 = 800 W",
   "t = 3.36 × 10⁵/800 = 420 s = 7.0 min"],
  why="5.6 min ignores the 80% efficiency. 4.5 min multiplies by 0.80 instead of dividing by it. 8.75 min takes the temperature rise as 100 °C instead of "
      "80 °C.",
  ncert=CEC + "electrical energy, power", seconds=70, rc=True)

q(CE, "Drift velocity and Ohm's law", "Intermediate", "assertion_reason",
  ar("When a constant potential difference is applied across a metal wire, the current in it settles at a steady "
     "value, even though the electric field accelerates each free electron between collisions.",
     "Collisions with the ions of the metal keep randomising the velocities of the electrons, so the average "
     "velocity they acquire in the field, the drift velocity eEτ/m, does not keep growing with time."),
  AR, ar_key(True, True, True),
  "Drift velocity: acceleration between collisions, randomisation at collisions",
  "Between collisions each electron is accelerated by the field, but after a collision its velocity is random "
  "again. Averaged over all electrons, the velocity gained is the acceleration eE/m times the average time τ since "
  "the last collision, which is a constant. A constant drift velocity means a constant current I = neAv_d. R gives "
  "exactly this reason, so it explains A.",
  ["A: steady current for a fixed potential difference → true",
   "R: collisions randomise velocities; v_d = eEτ/m is constant → true",
   "R explains why the current does not keep increasing → A"],
  why="Both statements are true, and the constant drift velocity of R is the reason why the current in A is steady.",
  ncert=CEC + "drift of electrons and the origin of resistivity", seconds=50)

q(CE, "Cells, emf and internal resistance", "Intermediate", "match_list",
  ml("A cell of emf ε and internal resistance r is connected across an external resistor R. Match each quantity in "
     "List-I with its expression in List-II.",
     ["Current in the circuit", "Potential difference across the terminals of the cell",
      "Power delivered to the external resistor",
      "Fraction of the power generated by the cell that is delivered to the external resistor"],
     ["εR/(R + r)", "R/(R + r)", "ε/(R + r)", "ε²R/(R + r)²"]),
  *mlo("A-III, B-I, C-IV, D-II", ["A-III, B-II, C-IV, D-I", "A-I, B-III, C-IV, D-II", "A-III, B-I, C-II, D-IV"],
       "C"),
  "Cell with internal resistance: I = ε/(R + r), V = IR, P = I²R",
  "The current is ε/(R + r). The terminal potential difference is V = ε − Ir = IR = εR/(R + r). The power in R is "
  "I²R = ε²R/(R + r)². The cell generates power εI, of which I²R reaches R, so the fraction is IR/ε = R/(R + r).",
  ["I = ε/(R + r) → A-III", "V = IR = εR/(R + r) → B-I", "P_R = ε²R/(R + r)² → C-IV", "Fraction = R/(R + r) → D-II"],
  why="The code with B-II, D-I interchanges the terminal voltage (which carries ε) and the dimensionless fraction. "
      "A-I, B-III interchanges the current and the terminal voltage. C-II, D-IV gives a dimensionless ratio as a "
      "power.",
  ncert=CEC + "cells, emf, internal resistance; electrical energy, power", seconds=60)

# ---- Advanced
eps_c, r_c, R_c = F(3, 2), F(1, 2), F(1, 2)
# three cells normal, one reversed, all in parallel across R_c: node equation for terminal voltage V
V_p = (3 * eps_c / r_c - eps_c / r_c) / (4 / r_c + 1 / R_c)
I_p = V_p / R_c
assert V_p == F(3, 5) and I_p == F(6, 5)
assert eps_c / (r_c / 4 + R_c) == F(12, 5) and eps_c / (r_c / 3 + R_c) == F(9, 4)
assert (eps_c / 2) / (r_c + R_c) == F(3, 4)
q(CE, "Cells, emf and internal resistance", "Advanced", "numerical",
  "Four identical cells, each of emf 1.5 V and internal resistance 0.5 Ω, are meant to be connected in parallel "
  "(all positive terminals joined together and all negative terminals joined together), but one of them is "
  "connected the wrong way round. A 0.5 Ω resistor is connected across the two common terminals. The current "
  "through the resistor is:",
  *opt("1.2 A", ["2.4 A", "0.75 A", "2.25 A"], "D"),
  "Kirchhoff's junction rule at the common terminal (or the equivalent cell of a parallel group)",
  "Let V be the potential of the common positive line relative to the common negative line. Each correctly "
  "connected cell sends (1.5 − V)/0.5 into the line; the reversed cell sends (−1.5 − V)/0.5; together these must "
  "equal the current V/0.5 through the resistor.",
  ["3(1.5 − V) + (−1.5 − V) = V", "3.0 = 5V → V = 0.6 V", "I = 0.6/0.5 = 1.2 A"],
  shortcut="Equivalent cell: emf = (1.5 + 1.5 + 1.5 − 1.5)/4 = 0.75 V, internal resistance 0.5/4 = 0.125 Ω; "
           "I = 0.75/0.625 = 1.2 A.",
  why="2.4 A takes all four cells as correctly connected. 0.75 A uses the right equivalent emf but the internal "
      "resistance of one cell (0.5 Ω) instead of r/4. 2.25 A simply leaves the reversed cell out of the circuit.",
  ncert=CEC + "cells in series and in parallel", seconds=120, rc=True)


def two_node(E1, r1, Ra, R, Rb, E2, r2):
    """Node potentials V_A, V_B: G-A cell E1 (r1, + at A); A-G resistor Ra; A-B resistor R; B-G resistor Rb;
    B-G cell E2 (r2, + at B)."""
    a11, a12, b1 = F(1, r1) + F(1, Ra) + F(1, R), -F(1, R), F(E1, r1)
    a21, a22, b2 = -F(1, R), F(1, R) + F(1, Rb) + F(1, r2), F(E2, r2)
    d = a11 * a22 - a12 * a21
    return (b1 * a22 - a12 * b2) / d, (a11 * b2 - a21 * b1) / d


VA, VB = two_node(12, 1, 4, 2, 2, 4, 1)
assert (VA, VB) == (8, 4)
I_cell2 = (4 - VB) / 1
I_cell1, I_AB = (12 - VA) / 1, (VA - VB) / 2
assert I_cell2 == 0 and I_cell1 == 4 and I_AB == 2
VA2, VB2 = two_node(12, 1, 4, 2, 2, -4, 1)   # 4 V cell reversed
assert (-4 - VB2) / 1 != 0
q(CE, "Kirchhoff's laws", "Advanced", "numerical",
  "In a circuit, points A and B are connected to a common return line G as follows. Between G and A: a cell of emf "
  "12 V and internal resistance 1 Ω, its positive terminal towards A. Between A and G: a 4 Ω resistor. Between A and "
  "B: a 2 Ω resistor. Between B and G: a 2 Ω resistor and, in parallel with it, a cell of emf 4 V and internal "
  "resistance 1 Ω, its positive terminal towards B. The current through the 4 V cell is:",
  *opt("zero", ["2 A, into its positive terminal", "4 A, out of its positive terminal", "1 A, into its positive terminal"],
       "B"),
  "Kirchhoff's rules (junction rule at A and B) for a network with two cells",
  "Take G as 0 V and let the potentials of A and B be V_A and V_B. The junction rule at A and at B gives two "
  "equations. Solving them, the potential of B comes out equal to 4 V, the emf of the second cell, so no current "
  "flows through that cell.",
  ["At A: (12 − V_A)/1 = V_A/4 + (V_A − V_B)/2", "At B: (V_A − V_B)/2 + (4 − V_B)/1 = V_B/2",
   "Solving: V_A = 8 V, V_B = 4 V", "Current in 4 V cell = (4 − V_B)/1 = 0",
   "Check: 4 A from the 12 V cell = 2 A (4 Ω) + 2 A (A to B); 2 A from A to B all goes through the 2 Ω to G"],
  why="2 A is the current through the 2 Ω resistor between A and B (and through the 2 Ω between B and G), not through "
      "the cell. 4 A is the current through the 12 V cell. 1 A would need the potential of B to be 3 V or 5 V, "
      "which does not satisfy the junction rule at B.",
  ncert=CEC + "Kirchhoff's rules", seconds=150, rc=True)

R1v = R2v = 1000
I_R2 = F(12 - 4, R2v)
I_R1 = F(4, R1v)
RV = F(4) / (I_R2 - I_R1)
assert RV == 1000 and F(4) / I_R2 == 500 and F(12) / I_R1 == 3000 and F(8) / I_R1 == 2000
q(CE, "Combination of resistors", "Advanced", "numerical",
  "Two 1.0 kΩ resistors R₁ and R₂ are connected in series across an ideal 12 V battery. A voltmeter connected across "
  "R₁ reads 4.0 V. The resistance of the voltmeter is:",
  *opt("1.0 kΩ", ["0.50 kΩ", "2.0 kΩ", "3.0 kΩ"], "A"),
  "A voltmeter of finite resistance in parallel with a resistor; series current shared at the junction",
  "With the voltmeter connected, the p.d. across R₂ is 12 − 4 = 8 V, so the current through R₂ (and from the battery) "
  "is 8 mA. Only 4.0/1000 = 4 mA of this goes through R₁; the remaining 4 mA goes through the voltmeter, which has "
  "4.0 V across it.",
  ["Current through R₂ = 8.0 V/1.0 kΩ = 8.0 mA", "Current through R₁ = 4.0 V/1.0 kΩ = 4.0 mA",
   "Voltmeter current = 8.0 − 4.0 = 4.0 mA → R_V = 4.0 V/4.0 mA = 1.0 kΩ"],
  why="0.50 kΩ (4 V/8 mA) is the resistance of R₁ and the voltmeter in parallel, not of the voltmeter alone. 2.0 kΩ "
      "divides the 8 V across R₂ by the voltmeter current. 3.0 kΩ divides the battery emf by the voltmeter current.",
  ncert=CEC + "combination of resistors - series and parallel; Kirchhoff's rules", seconds=110, rc=True)

q(CE, "Wheatstone and metre bridge", "Advanced", "statement_pair",
  sp("A Wheatstone bridge with unequal resistances P and Q in one branch (P/Q = R/S) remains balanced if P and Q "
     "alone are interchanged.",
     "The balance condition of a Wheatstone bridge is obtained by applying Kirchhoff's loop rule to two loops, "
     "together with the condition that no current flows through the galvanometer."),
  SP, sp_key(False, True),
  "Wheatstone bridge: balance condition and its derivation",
  "Statement I is false: after the interchange the ratio in that branch becomes Q/P, which differs from R/S unless "
  "P = Q, so the galvanometer deflects. Statement II is true: with I_g = 0, the loop rule applied to the loop "
  "containing P, the galvanometer and R, and to the loop containing Q, the galvanometer and S, gives I₁P = I₂R and "
  "I₁Q = I₂S, whose ratio is P/Q = R/S.",
  ["I: Q/P ≠ R/S when P ≠ Q → false", "II: loop rule + I_g = 0 gives P/Q = R/S → true"],
  why="Interchanging P with Q inverts their ratio; a balanced bridge stays balanced under such a swap only in the "
      "special case P = Q.",
  ncert=CEC + "Wheatstone bridge", seconds=50)

q(CE, "Cells, emf and internal resistance", "Advanced", "assertion_reason",
  ar("By connecting more and more identical cells in parallel across a fixed external resistor, the current through "
     "the resistor can be made as large as we please.",
     "The internal resistance of n identical cells, each of internal resistance r, connected in parallel is r/n."),
  AR, ar_key(False, True),
  "Parallel grouping of cells: emf unchanged, internal resistance divided by n",
  "For n identical cells in parallel the emf stays ε and the internal resistance is r/n, so the current is "
  "I = ε/(R + r/n). As n grows, r/n tends to zero and I approaches ε/R, but never exceeds it. So the current is "
  "limited and A is false. R is true.",
  ["R: r_eq = r/n → true", "I = ε/(R + r/n) → ε/R as n → ∞", "A: the current cannot exceed ε/R → false"],
  why="Adding cells in parallel never raises the emf, so the current is bounded by ε/R; A is false while R is a "
      "correct statement.",
  ncert=CEC + "cells in series and in parallel", seconds=50)

Rb100 = F(220 ** 2, 100)
Rb25 = F(220 ** 2, 25)
Ib = F(440) / (Rb100 + Rb25)
assert Rb100 == 484 and Rb25 == 1936 and Rb25 / Rb100 == 4
close(float(Ib), 0.18, 0.02)
assert Ib * Rb25 == 352 and Ib * Rb100 == 88
close(float(Ib ** 2 * Rb100), 16.0, 1e-3)
assert Ib ** 2 * Rb25 > Ib ** 2 * Rb100
truth = {"a": True, "b": True, "c": True, "d": False, "e": True}
q(CE, "Combination of resistors", "Advanced", "multi_statement",
  ms("Two bulbs, rated 100 W, 220 V and 25 W, 220 V, are connected in series across a 440 V supply. Treat the "
     "resistance of each bulb as constant, equal to the value implied by its rating. Which of the following "
     "statements are correct?",
     ["The resistance of the 25 W bulb is four times that of the 100 W bulb.",
      "The current in the circuit is about 0.18 A.",
      "The potential difference across the 25 W bulb is about 352 V, well above its rated voltage.",
      "The 100 W bulb dissipates more power than the 25 W bulb.",
      "The power dissipated in the 100 W bulb is about 16 W."]),
  *mso(truth, "abce", ["abd", "bce", "acde"], "B"),
  "Rated values give R = V²/P; in series the same current flows and the voltage divides in the ratio of resistances",
  "R(100 W) = 220²/100 = 484 Ω and R(25 W) = 220²/25 = 1936 Ω. In series across 440 V the current is "
  "440/2420 ≈ 0.18 A. The voltage divides as 1 : 4, so 88 V across the 100 W bulb and 352 V across the 25 W bulb, "
  "which is likely to fuse. In series the larger resistance dissipates more power, so the 25 W bulb dissipates more.",
  ["R₁₀₀ = 484 Ω, R₂₅ = 1936 Ω → (a) true", "I = 440/2420 ≈ 0.18 A → (b) true",
   "V₂₅ = 0.1818 × 1936 = 352 V → (c) true", "P = I²R: larger in the 1936 Ω bulb → (d) false",
   "P₁₀₀ = 0.1818² × 484 ≈ 16 W → (e) true"],
  why="(d) is false: with the same current in both, P = I²R is four times larger in the 25 W bulb (about 64 W "
      "against 16 W). The other codes either include (d) or leave out the true statement (a).",
  ncert=CEC + "combination of resistors - series and parallel; electrical energy, power", seconds=120, rc=True)


# ================================================================ Magnetic Effects of Current and Magnetism (B6 I8 A6)
MC = NC + "'Moving Charges and Magnetism', "
MM = NC + "'Magnetism and Matter', "
MU0 = 4 * math.pi * 1e-7

# ---- Basic
assert F(1, 2) / 2 == F(1, 4) and F(1, 2) == F(1, 2)
q(MAG, "Force on charges and conductors", "Basic", "numerical",
  "A charged particle moves in a circle of radius r at right angles to a uniform magnetic field. If its speed is "
  "halved and the magnetic field is doubled (the particle still moving at right angles to the field), the radius of "
  "its circular path becomes:",
  *opt("r/4", ["4r", "r", "r/2"], "B"),
  "Radius of the circular path r = mv/(qB)",
  "The magnetic force qvB provides the centripetal force mv²/r, so r = mv/(qB): directly proportional to the speed "
  "and inversely proportional to the field.",
  ["r ∝ v/B", "New radius = r × (1/2) ÷ 2 = r/4"],
  why="4r inverts the dependence on both v and B. r assumes the two changes cancel, but both make the radius "
      "smaller. r/2 applies only one of the two changes.",
  ncert=MC + "motion in a magnetic field", seconds=30, rc=True)

I_w, L_w, B_vec = 2.0, 0.50, (3e-3, 4e-3, 0.0)
Lv = (L_w, 0.0, 0.0)
Fz = I_w * (Lv[0] * B_vec[1] - Lv[1] * B_vec[0])
close(Fz, 4.0e-3)
close(I_w * L_w * math.hypot(3e-3, 4e-3), 5.0e-3)
close(I_w * L_w * 3e-3, 3.0e-3)
q(MAG, "Force on charges and conductors", "Basic", "numerical",
  "A straight wire 0.50 m long lies along the x-axis and carries a current of 2.0 A in the +x direction. It is in a "
  "uniform magnetic field B = (3.0 î + 4.0 ĵ) mT. The magnetic force on the wire is:",
  *opt("4.0 × 10⁻³ N, along +z", ["5.0 × 10⁻³ N, along +z", "3.0 × 10⁻³ N, along +z", "4.0 × 10⁻³ N, along −z"],
       "C"),
  "Force on a straight current-carrying conductor F = I(l × B)",
  "Only the component of B perpendicular to the wire exerts a force. The x-component of B is along the wire and "
  "gives î × î = 0; the y-component gives î × ĵ = k̂.",
  ["F = I l î × (3.0 î + 4.0 ĵ) × 10⁻³ T", "= 2.0 × 0.50 × 4.0 × 10⁻³ (î × ĵ) N", "= 4.0 × 10⁻³ N along +z (k̂)"],
  why="5.0 × 10⁻³ N uses the full magnitude of B (5.0 mT), including the component parallel to the wire. "
      "3.0 × 10⁻³ N uses the parallel component, which gives no force. The −z direction comes from taking B × l "
      "instead of l × B.",
  ncert=MC + "magnetic force on a current-carrying conductor", seconds=50, rc=True)

assert F(3, 2) == F(3) / 2 and F(3) * 2 == 6 and F(3) / 4 == F(3, 4) and F(2, 3) == 1 / F(3, 2)
q(MAG, "Biot-Savart law", "Basic", "numerical",
  "The magnetic field at the centre of a circular loop carrying a steady current is B. The loop is replaced by "
  "another single circular loop of twice the radius, carrying three times the current. The magnetic field at its "
  "centre is:",
  *opt("3B/2", ["6B", "3B/4", "2B/3"], "D"),
  "Field at the centre of a circular loop B = µ₀I/(2R)",
  "The field at the centre is proportional to the current and inversely proportional to the radius.",
  ["B ∝ I/R", "B' = B × 3/2 = 3B/2"],
  why="6B multiplies by the factor for the radius instead of dividing by it. 3B/4 treats the field as falling off "
      "as 1/R². 2B/3 inverts the result.",
  ncert=MC + "magnetic field on the axis of a circular current loop", seconds=30, rc=True)

v_up, B_north = (0, 0, 1), (0, 1, 0)
cross = (v_up[1] * B_north[2] - v_up[2] * B_north[1], v_up[2] * B_north[0] - v_up[0] * B_north[2],
         v_up[0] * B_north[1] - v_up[1] * B_north[0])
force_dir = tuple(-c for c in cross)   # electron: negative charge
assert force_dir == (1, 0, 0)          # x = east, y = north, z = up
q(MAG, "Force on charges and conductors", "Basic", "direct",
  "An electron moves vertically upwards through a region where a uniform horizontal magnetic field points towards "
  "the north. The magnetic force on the electron at that instant points:",
  *opt("towards the east", ["towards the west", "towards the north", "vertically downwards"], "A"),
  "Magnetic force F = q(v × B); the charge of the electron is negative",
  "Take east, north and up as a right-handed set of axes (east × north = up). Then up × north = west, so for a "
  "positive charge the force would be towards the west. The electron's charge is negative, which reverses the force.",
  ["v × B = (up) × (north) = west", "q = −e reverses it: F towards the east"],
  why="West is the direction for a positive charge. The force cannot be along the field (north), and it must be "
      "perpendicular to the velocity, so it cannot be vertical.",
  ncert=MC + "magnetic force", seconds=40)

q(MAG, "Force on charges and conductors", "Basic", "statement_pair",
  sp("The magnitude of a magnetic field is 1 tesla if a charge of 1 C moving at 1 m/s at right angles to the field "
     "experiences a force of 1 N.",
     "A smaller unit of magnetic field, the gauss, equal to 10⁻⁴ T, is also often used."),
  SP, sp_key(True, True),
  "Unit of magnetic field: the tesla, from F = qvB sin θ, and the gauss",
  "From F = qvB sin θ with θ = 90°, B = F/(qv), so 1 T = 1 N/(1 C × 1 m/s) = 1 N s C⁻¹ m⁻¹, which is Statement I. "
  "The tesla is a rather large unit; NCERT notes that the non-SI unit gauss, 1 G = 10⁻⁴ T, is also often used, "
  "which is Statement II.",
  ["I: B = F/(qv sin 90°) → 1 T = 1 N s C⁻¹ m⁻¹ → true", "II: 1 gauss = 10⁻⁴ T → true"],
  why="Both statements are correct, so options saying either is false are wrong.",
  ncert=MC + "magnetic force (unit of magnetic field)", seconds=35)

q(MAG, "Torque on loop and galvanometer", "Basic", "match_list",
  ml("Match each device or definition in List-I with the physical effect on which it is based (List-II).",
     ["Moving-coil galvanometer", "Velocity selector", "SI definition of the ampere (based on force between currents)",
      "A long current-carrying solenoid used as a magnet"],
     ["Force between two parallel current-carrying conductors", "Torque on a current loop in a magnetic field",
      "Electric and magnetic forces on a moving charge balancing each other",
      "Its field outside, at large distances, is the same as that of a bar magnet (a magnetic dipole)"]),
  *mlo("A-II, B-III, C-I, D-IV", ["A-I, B-III, C-II, D-IV", "A-II, B-IV, C-I, D-III", "A-III, B-II, C-I, D-IV"],
       "D"),
  "Applications of the magnetic force and torque",
  "The coil of a moving-coil galvanometer turns because of the torque NIAB on a current loop. In a velocity "
  "selector, qE and qvB are equal and opposite for particles of speed E/B. The ampere was defined through the force "
  "per unit length between two parallel currents. A solenoid's external field is that of a magnetic dipole, like a "
  "bar magnet.",
  ["Galvanometer → torque on loop (II)", "Velocity selector → qE = qvB (III)",
   "Ampere → force between parallel currents (I)", "Solenoid → equivalent bar magnet (IV)"],
  why="A-I interchanges the galvanometer and the ampere definition. B-IV, D-III interchanges the velocity selector "
      "and the solenoid. A-III, B-II interchanges the galvanometer and the velocity selector.",
  ncert=MC + "moving coil galvanometer; motion in combined electric and magnetic fields; force between two "
             "parallel currents; " + MM + "the bar magnet", seconds=50)

# ---- Intermediate
G_s, S1, I1r = F(90), F(10), F(10)
Ig = I1r * S1 / (G_s + S1)
I2r = Ig * (G_s + F(5)) / F(5)
assert Ig == 1 and I2r == 19 and Ig * G_s / F(5) == 18
q(MAG, "Torque on loop and galvanometer", "Intermediate", "numerical",
  "A galvanometer of resistance 90 Ω, shunted by a 10 Ω resistor, works as an ammeter of range 0–10 mA. If the "
  "10 Ω shunt is replaced by a 5 Ω shunt, the range of the ammeter becomes:",
  *opt("0–19 mA", ["0–20 mA", "0–5 mA", "0–18 mA"], "B"),
  "Shunt: the galvanometer and the shunt share the current in the inverse ratio of their resistances",
  "First find the full-scale current I_g of the galvanometer from the original arrangement, then the new total "
  "current for which the galvanometer current is again I_g.",
  ["10 mA divides as 10 : 90 between G and S → I_g = 10 × 10/100 = 1 mA",
   "New range: I = I_g(G + S)/S = 1 × (90 + 5)/5 = 19 mA"],
  why="0–20 mA assumes that halving the shunt doubles the range. 0–5 mA moves the range the wrong way: a smaller "
      "shunt takes more current, so the range increases. 0–18 mA counts only the shunt current I_gG/S and leaves "
      "out the 1 mA through the galvanometer.",
  ncert=MC + "moving coil galvanometer (conversion into an ammeter)", seconds=75, rc=True)

r_ratio = F(1) / F(2)          # r = p/(qB), same p and B: r_alpha/r_p = q_p/q_alpha
T_ratio = F(4) / F(2)          # T = 2 pi m/(qB)
assert r_ratio == F(1, 2) and T_ratio == 2
q(MAG, "Force on charges and conductors", "Intermediate", "numerical",
  "A proton and an alpha particle enter the same uniform magnetic field with momenta of equal magnitude, each moving "
  "at right angles to the field. Taking the mass of the alpha particle as 4 times and its charge as 2 times those of "
  "the proton, the ratio of the radii of their paths (r_α : r_p) and the ratio of their periods of revolution "
  "(T_α : T_p) are, respectively:",
  *opt("1 : 2 and 2 : 1", ["1 : 2 and 1 : 1", "2 : 1 and 2 : 1", "2 : 1 and 1 : 2"], "C"),
  "r = p/(qB) and T = 2πm/(qB)",
  "With the same momentum in the same field, the radius depends only on the charge. The period depends on m/q, "
  "which is twice as large for the alpha particle.",
  ["r_α/r_p = q_p/q_α = 1/2", "T_α/T_p = (m_α/q_α)/(m_p/q_p) = (4/2)/1 = 2"],
  why="1 : 1 for the periods forgets that T depends on m/q, which differs for the two particles. 2 : 1 for the radii "
      "uses r ∝ m/q, which holds for equal speeds, not equal momenta. The last option inverts both ratios.",
  ncert=MC + "motion in a magnetic field", seconds=70, rc=True)

F_L = 0.50 * 2.0 * math.hypot(0.03, 0.04)
close(F_L, 0.050)
close(0.50 * 2.0 * 0.07, 0.070)
close(0.50 * 2.0 * 0.01, 0.010)
q(MAG, "Force on charges and conductors", "Intermediate", "numerical",
  "A wire bent into an L-shape, with arms of 3.0 cm and 4.0 cm at right angles to each other, carries a current of "
  "2.0 A. It lies in a plane perpendicular to a uniform magnetic field of 0.50 T. The magnitude of the net magnetic "
  "force on the wire is:",
  *opt("0.050 N", ["0.070 N", "0.010 N", "zero"], "A"),
  "Force on a bent wire in a uniform field equals the force on a straight wire joining its ends",
  "The forces on the two arms, BIl₁ and BIl₂, are perpendicular to each other because the arms are perpendicular. "
  "Their resultant is BI√(l₁² + l₂²), the force on a straight wire of length 5.0 cm joining the two ends.",
  ["F₁ = 0.50 × 2.0 × 0.03 = 0.030 N; F₂ = 0.50 × 2.0 × 0.04 = 0.040 N, at right angles",
   "F = √(0.030² + 0.040²) = 0.050 N"],
  shortcut="In a uniform field, F = BI × (straight-line distance between the ends) = 0.50 × 2.0 × 0.05 N.",
  why="0.070 N adds the two forces as if they were in the same direction. 0.010 N subtracts them. Zero would hold "
      "only for a closed loop, whose ends coincide.",
  ncert=MC + "magnetic force on a current-carrying conductor", seconds=60, rc=True)

n_layer = 5 * 400 / 0.50
B_sol = MU0 * n_layer * 3.0
close(B_sol, 1.5e-2, 0.01)
close(MU0 * 400 / 0.50 * 3.0, 3.0e-3, 0.01)
close(MU0 * 2000 * 3.0, 7.5e-3, 0.01)
close(MU0 * 40 * 3.0, 1.5e-4, 0.01)
q(MAG, "Ampere's law", "Intermediate", "numerical",
  "A long solenoid is 50 cm long and is wound in 5 layers, each layer having 400 turns spread evenly along its "
  "length. It carries a current of 3.0 A. Taking µ₀ = 4π × 10⁻⁷ T m A⁻¹, the magnetic field well inside the "
  "solenoid, near its middle, is about:",
  *opt("1.5 × 10⁻² T", ["3.0 × 10⁻³ T", "7.5 × 10⁻³ T", "1.5 × 10⁻⁴ T"], "D"),
  "Field inside a long solenoid B = µ₀nI, with n the total number of turns per unit length",
  "Every layer carries the same current round the same axis, so all 5 × 400 = 2000 turns count. Spread over 0.50 m "
  "they give n = 4000 turns per metre.",
  ["n = 2000/0.50 = 4000 m⁻¹", "B = 4π × 10⁻⁷ × 4000 × 3.0 ≈ 1.5 × 10⁻² T"],
  why="3.0 × 10⁻³ T counts only one layer. 7.5 × 10⁻³ T uses the total number of turns (2000) as if it were the "
      "number per metre, ignoring the 0.50 m length. 1.5 × 10⁻⁴ T uses turns per centimetre (40 cm⁻¹) without "
      "converting to turns per metre.",
  ncert=MC + "the solenoid", seconds=60, rc=True)

q(MAG, "Force on charges and conductors", "Intermediate", "assertion_reason",
  ar("In a region with uniform electric and magnetic fields perpendicular to each other, charged particles moving "
     "perpendicular to both fields with speed E/B pass through undeflected, whatever their charge and mass.",
     "For a particle moving faster than E/B in this region, the electric force on it is larger than the magnetic "
     "force."),
  AR, ar_key(True, False),
  "Velocity selector: qE = qvB",
  "For the right direction of motion, the electric force qE and the magnetic force qvB act in opposite directions. "
  "They balance when v = E/B; q cancels from both sides and m does not appear, so A is true. For v > E/B the "
  "magnetic force qvB exceeds qE, so the particle is deflected in the direction of the magnetic force. R reverses "
  "this and is false.",
  ["Balance: qE = qvB → v = E/B, independent of q and m → A true",
   "For v > E/B: qvB > qE → magnetic force is larger → R false"],
  why="R is false, so the options that call both statements true are wrong; A is true, so the option calling A "
      "false is wrong.",
  ncert=MC + "motion in combined electric and magnetic fields (velocity selector)", seconds=50)

q(MAG, "Magnetic dipole and bar magnet", "Intermediate", "assertion_reason",
  ar("The SI unit of magnetic dipole moment, A m², can also be written as J T⁻¹.",
     "The potential energy of a magnetic dipole of moment m in a uniform magnetic field B is U = −m·B."),
  AR, ar_key(True, True, True),
  "Units of magnetic moment from the energy of a dipole in a field",
  "Since U = −mB cos θ, the moment m has the unit of energy divided by magnetic field, J T⁻¹. Checking: "
  "1 T = 1 N A⁻¹ m⁻¹, so J T⁻¹ = (N m)/(N A⁻¹ m⁻¹) = A m². Both statements are true and R is the relation that "
  "gives the unit in A.",
  ["U = −mB cos θ → [m] = [U]/[B] = J T⁻¹", "J T⁻¹ = N m/(N A⁻¹ m⁻¹) = A m² → A true", "R true and explains A"],
  why="Both statements are true, and the unit J T⁻¹ follows directly from the energy expression in R.",
  ncert=MM + "the bar magnet (magnetic dipole in a uniform field)", seconds=50)

truth = {"a": True, "b": True, "c": True, "d": False, "e": False}
q(MAG, "Biot-Savart law", "Intermediate", "multi_statement",
  ms("The Biot–Savart law for the magnetic field of a current element is compared with Coulomb's law for the "
     "electric field of a point charge. Which of the following statements are correct?",
     ["The magnetic field of a current element depends on the angle between the element and the line joining it to "
      "the field point, while the electric field of a point charge has no such angular dependence.",
      "Both fields obey the principle of superposition.",
      "The source of the electrostatic field (charge) is a scalar, while the source of the magnetic field (I dl) is "
      "a vector.",
      "The magnetic field due to a current element at a point does not depend on the distance of the point from "
      "the element.",
      "The magnetic field due to a current element falls off as the inverse cube of the distance."]),
  *mso(truth, "abc", ["ab", "acd", "bce"], "B"),
  "Biot–Savart law: dB = (µ₀/4π) I dl × r̂/r²",
  "NCERT compares the two laws. Both fields are long range, falling as 1/r², and both obey superposition. The "
  "electrostatic field is produced by a scalar source, the charge q, but the magnetic field by a vector source, "
  "I dl. The Biot–Savart field contains sin θ, the angle between dl and r, while the Coulomb field has no such "
  "factor.",
  ["(a) sin θ factor only in Biot–Savart → true", "(b) superposition holds for both → true",
   "(c) q scalar, I dl vector → true", "(d) the field falls as 1/r² → false", "(e) it is 1/r², not 1/r³ → false"],
  why="The field of a current element depends on distance as 1/r², so (d) and (e) are both false; every option "
      "containing either of them, or leaving out (c), is wrong.",
  ncert=MC + "magnetic field due to a current element, Biot-Savart law", seconds=60)

circ = MU0 * 2 * 5
close(circ, 1.26e-5, 1e-2)
close(MU0 * 5, 6.3e-6, 1e-2)
close(2e-7 * 10, 2.0e-6)
q(MAG, "Ampere's law", "Intermediate", "numerical",
  "A long straight wire carries a steady current of 5.0 A. A closed path winds twice round the wire (like two turns "
  "of a coil) before closing on itself, always going round in the same sense. Taking µ₀ = 4π × 10⁻⁷ T m A⁻¹, the "
  "magnitude of ∮B·dl along this path is about:",
  *opt("1.3 × 10⁻⁵ T m", ["6.3 × 10⁻⁶ T m", "zero", "2.0 × 10⁻⁶ T m"], "C"),
  "Ampere's circuital law ∮B·dl = µ₀I_enclosed, the current being counted each time the path goes round it",
  "Each complete turn round the wire contributes µ₀I to the line integral (the integral of B dl over one circle of "
  "radius r is B × 2πr = µ₀I, and the same holds for any shape of path going once round). Going round twice in the "
  "same sense doubles the result.",
  ["One turn round the wire: µ₀I", "Two turns: 2µ₀I = 2 × 4π × 10⁻⁷ × 5.0 ≈ 1.3 × 10⁻⁵ T m"],
  why="6.3 × 10⁻⁶ T m counts the current only once. Zero would apply to a path that does not encircle the wire. "
      "2.0 × 10⁻⁶ T m uses µ₀/2π in place of µ₀.",
  ncert=MC + "Ampere's circuital law", seconds=50, rc=True)

# ---- Advanced
mB = 0.40 * 0.25
sin_t = 0.050 / mB
U1, U2 = -mB * math.cos(math.asin(sin_t)), -mB * math.cos(math.pi - math.asin(sin_t))
close(U1, -0.0866, 1e-3)
close(U2, 0.0866, 1e-3)
q(MAG, "Magnetic dipole and bar magnet", "Advanced", "numerical",
  "A magnetic dipole of moment 0.40 A m² is held in a uniform magnetic field of 0.25 T. The torque acting on it has "
  "a magnitude of 0.050 N m. The potential energy of the dipole (taken as −m·B) could be:",
  *opt("−0.087 J or +0.087 J", ["−0.087 J only", "−0.050 J or +0.050 J", "+0.087 J only"], "D"),
  "Torque τ = mB sin θ and potential energy U = −mB cos θ",
  "The torque fixes sin θ but not θ itself: both θ = 30° and θ = 150° give sin θ = 0.5. These two orientations have "
  "potential energies of opposite sign.",
  ["mB = 0.40 × 0.25 = 0.10 J", "sin θ = 0.050/0.10 = 0.5 → θ = 30° or 150°",
   "U = −0.10 cos 30° = −0.087 J, or U = −0.10 cos 150° = +0.087 J"],
  why="−0.087 J only and +0.087 J only each miss one of the two angles allowed by sin θ = 0.5. ±0.050 J takes the "
      "magnitude of the energy equal to the magnitude of the torque.",
  ncert=MM + "the bar magnet (magnetic dipole in a uniform magnetic field)", seconds=90, rc=True)

lam_g = 5.0e-4 * 10
h_float = 2e-7 * 50 * 25 / lam_g
close(h_float, 0.050)
close(1e-7 * 50 * 25 / lam_g, 0.025)
close(4e-7 * 50 * 25 / lam_g, 0.10)
q(MAG, "Force on charges and conductors", "Advanced", "numerical",
  "A long horizontal wire, fixed in position, carries a steady current of 50 A. A second long, straight, horizontal "
  "wire, parallel to it and directly above it, has a mass of 5.0 × 10⁻⁴ kg per metre and carries a current of 25 A. "
  "Taking µ₀ = 4π × 10⁻⁷ T m A⁻¹ and g = 10 m/s², the upper wire can float in equilibrium (supported only by the "
  "magnetic force) at a height above the lower wire of:",
  *opt("5.0 cm, with the two currents in opposite directions",
       ["5.0 cm, with the two currents in the same direction", "2.5 cm, with the two currents in opposite directions",
        "10 cm, with the two currents in opposite directions"], "B"),
  "Force per unit length between parallel currents f = µ₀I₁I₂/(2πd); antiparallel currents repel",
  "The magnetic force on the upper wire must be upward, i.e. repulsive, so the currents must be in opposite "
  "directions. Its magnitude per metre must equal the weight per metre.",
  ["Weight per metre = 5.0 × 10⁻⁴ × 10 = 5.0 × 10⁻³ N/m",
   "µ₀I₁I₂/(2πd) = 2 × 10⁻⁷ × 50 × 25/d = 2.5 × 10⁻⁴/d N/m", "2.5 × 10⁻⁴/d = 5.0 × 10⁻³ → d = 0.050 m = 5.0 cm"],
  why="Currents in the same direction attract, pulling the upper wire down, so it cannot float. 2.5 cm uses "
      "µ₀/4π (10⁻⁷) in place of µ₀/2π. 10 cm uses µ₀/π (4 × 10⁻⁷) in place of µ₀/2π.",
  ncert=MC + "force between two parallel currents", seconds=110, rc=True)

Gm, Igm = F(100), F(1, 1000)
S_sh = Igm * Gm / (1 - Igm)
R_am = Gm * S_sh / (Gm + S_sh)
R_ser = F(10) / 1 - R_am
assert R_am == F(1, 10) and R_ser == F(99, 10)
assert F(10) / Igm - Gm == 9900
q(MAG, "Torque on loop and galvanometer", "Advanced", "numerical",
  "A galvanometer of resistance 100 Ω gives full-scale deflection for a current of 1.0 mA. It is first converted into "
  "an ammeter of range 0–1.0 A by a suitable shunt. This ammeter (galvanometer with its shunt) is then to be used as "
  "a voltmeter of range 0–10 V. The resistance that must be connected in series with the ammeter is:",
  *opt("9.9 Ω", ["10 Ω", "9.9 kΩ", "10.1 Ω"], "A"),
  "Galvanometer conversions: shunt for an ammeter, series resistance for a voltmeter",
  "The ammeter reaches full scale at 1.0 A. Its own resistance is that of G and the shunt in parallel. To read "
  "10 V at full scale, the total resistance must be 10 V/1.0 A = 10 Ω.",
  ["Shunt: S = I_gG/(I − I_g) = (0.001 × 100)/0.999 ≈ 0.1001 Ω",
   "Ammeter resistance = GS/(G + S) = 0.10 Ω",
   "Total resistance needed = 10/1.0 = 10 Ω → series resistance = 10 − 0.10 = 9.9 Ω"],
  why="10 Ω forgets the 0.10 Ω resistance of the ammeter itself. 9.9 kΩ uses the bare galvanometer's full-scale "
      "current (1.0 mA), which no longer applies once the shunt is fitted. 10.1 Ω adds the ammeter resistance "
      "instead of subtracting it.",
  ncert=MC + "moving coil galvanometer (conversion into ammeter and voltmeter)", seconds=120, rc=True)

enc = {"A": 4, "B": 4 - 6, "C": -6 + 2, "D": 4 - 6 + 2}
assert enc == {"A": 4, "B": -2, "C": -4, "D": 0}
q(MAG, "Ampere's law", "Advanced", "match_list",
  ml("Three long straight wires P, Q and S are perpendicular to the plane of the page. P carries a current 4I out of "
     "the page, Q carries 6I into the page and S carries 2I out of the page. Each closed path in List-I lies in the "
     "plane of the page and is traversed anticlockwise as seen by the reader. Match each path with the value of "
     "∮B·dl along it (List-II).",
     ["A path enclosing P only", "A path enclosing P and Q only", "A path enclosing Q and S only",
      "A path enclosing P, Q and S"],
     ["−4µ₀I", "zero", "+4µ₀I", "−2µ₀I"]),
  *mlo("A-III, B-IV, C-I, D-II", ["A-III, B-I, C-IV, D-II", "A-I, B-IV, C-III, D-II", "A-III, B-IV, C-II, D-I"],
       "C"),
  "Ampere's circuital law with the right-hand sign rule for enclosed currents",
  "For an anticlockwise path (seen by the reader), the right-hand rule makes a current out of the page positive and "
  "a current into the page negative. ∮B·dl is µ₀ times the algebraic sum of the enclosed currents; wires outside "
  "the path contribute nothing.",
  ["P only: +4I → +4µ₀I (III)", "P and Q: 4I − 6I = −2I → −2µ₀I (IV)", "Q and S: −6I + 2I = −4I → −4µ₀I (I)",
   "P, Q and S: 4I − 6I + 2I = 0 → zero (II)"],
  why="B-I, C-IV interchanges the values for the two two-wire paths. A-I takes the current out of the page as "
      "negative. C-II, D-I interchanges the three-wire path (net current zero) with the Q-and-S path.",
  ncert=MC + "Ampere's circuital law", seconds=80)

q(MAG, "Force on charges and conductors", "Advanced", "statement_pair",
  sp("An electron and a proton with equal kinetic energies move at right angles to the same uniform magnetic field. "
     "The radius of the electron's circular path is smaller than that of the proton's.",
     "In this situation, the magnetic forces on the electron and on the proton have equal magnitudes."),
  SP, sp_key(True, False),
  "r = mv/(qB) = √(2mK)/(qB); F = qvB",
  "For equal kinetic energy K and equal charge magnitude, r = √(2mK)/(eB) is proportional to √m, so the much "
  "lighter electron moves in the smaller circle: Statement I is true. The electron's speed, √(2K/m), is larger by "
  "the factor √(m_p/m_e) ≈ 43, so the force evB on it is larger: Statement II is false.",
  ["r ∝ √m for equal K and |q| → electron's r smaller → I true",
   "v ∝ 1/√m → v_e > v_p → F = evB larger for the electron → II false"],
  why="Statement II would be true for equal speeds, not equal kinetic energies.",
  ncert=MC + "motion in a magnetic field", seconds=60)

f_len = 2e-7 * 5 * 10 / 0.10
B_mid = 2e-7 * 10 / 0.05 - 2e-7 * 5 / 0.05
x_null = F(10) / 3
close(f_len, 1.0e-4)
close(B_mid, 2.0e-5)
assert F(5) / x_null == F(10) / (10 - x_null)
truth = {"a": True, "b": True, "c": True, "d": True, "e": False}
q(MAG, "Ampere's law", "Advanced", "multi_statement",
  ms("Two long, straight, parallel wires, 10 cm apart in air, carry steady currents of 5.0 A and 10 A in the same "
     "direction. Taking µ₀ = 4π × 10⁻⁷ T m A⁻¹, which of the following statements are correct?",
     ["The force per unit length on each wire is 1.0 × 10⁻⁴ N/m.",
      "The wires attract each other.",
      "The magnitude of the magnetic field at the point midway between the wires is 2.0 × 10⁻⁵ T.",
      "In the plane of the wires, the resultant magnetic field is zero at a point between the wires, about 3.3 cm "
      "from the 5.0 A wire.",
      "The 10 A wire experiences a force twice as large as the force on the 5.0 A wire."]),
  *mso(truth, "abcd", ["abc", "abde", "bcd"], "D"),
  "Field of a long straight wire B = µ₀I/(2πr); force per unit length µ₀I₁I₂/(2πd)",
  "The force per unit length is µ₀I₁I₂/(2πd), the same on both wires (Newton's third law), and attractive for "
  "currents in the same direction. Between the wires the two fields are opposite, so the field at the midpoint is "
  "the difference of the two, and the null point lies nearer the smaller current.",
  ["(a) 2 × 10⁻⁷ × 5 × 10/0.10 = 1.0 × 10⁻⁴ N/m → true", "(b) like currents attract → true",
   "(c) 2 × 10⁻⁷ × (10 − 5)/0.05 = 2.0 × 10⁻⁵ T → true",
   "(d) 5/x = 10/(10 − x) → x = 10/3 ≈ 3.3 cm from the 5 A wire → true",
   "(e) the forces are equal and opposite → false"],
  why="(e) is false because the two wires exert equal and opposite forces on each other. The codes with (e), or "
      "without (a) or (d), are therefore wrong.",
  ncert=MC + "magnetic field due to a long straight wire; force between two parallel currents", seconds=120, rc=True)


# ================================================================ Electromagnetic Induction and AC (B5 I6 A5)
EC = NC + "'Electromagnetic Induction', "
ACC = NC + "'Alternating Current', "

# ---- Basic
emf_rev = 50 * 2 * 0.5 * 0.02 / 0.1
close(emf_rev, 10.0)
close(50 * 0.5 * 0.02 / 0.1, 5.0)
q(EMI, "Faraday's and Lenz's laws", "Basic", "numerical",
  "A coil of 50 turns, each of area 0.020 m², lies with its plane perpendicular to a uniform magnetic field of "
  "0.50 T. The direction of the field is reversed (its magnitude staying 0.50 T) in 0.10 s. The magnitude of the "
  "average emf induced in the coil is:",
  *opt("10 V", ["5.0 V", "zero", "20 V"], "A"),
  "Faraday's law: average emf = NΔΦ/Δt",
  "The flux through each turn changes from +BA to −BA, a change of 2BA, not BA.",
  ["ΔΦ per turn = 2BA = 2 × 0.50 × 0.020 = 0.020 Wb", "ε = NΔΦ/Δt = 50 × 0.020/0.10 = 10 V"],
  why="5.0 V takes the change of flux as BA, as if the field had only been switched off. Zero assumes the flux is "
      "unchanged because the magnitude of the field is the same. 20 V counts the change as 4BA.",
  ncert=EC + "Faraday's law of induction", seconds=40, rc=True)

f_x = 31.4 / (2 * math.pi * 0.1)
close(f_x, 50.0, 1e-3)
close(31.4 / 0.1, 314)
close(31.4 / (math.pi * 0.1), 100, 1e-3)
close(31.4 / (4 * math.pi * 0.1), 25, 1e-3)
q(EMI, "AC: rms, reactance and impedance", "Basic", "numerical",
  "The reactance of an ideal inductor of inductance 0.10 H is 31.4 Ω at a certain frequency of the AC source. That "
  "frequency is about:",
  *opt("50 Hz", ["314 Hz", "100 Hz", "25 Hz"], "B"),
  "Inductive reactance X_L = ωL = 2πfL",
  "Solve X_L = 2πfL for f.",
  ["f = X_L/(2πL) = 31.4/(2 × 3.14 × 0.10) = 50 Hz"],
  why="314 Hz is the angular frequency ω = X_L/L (in rad/s), not the frequency. 100 Hz leaves out the factor 2. "
      "25 Hz uses 4π in place of 2π.",
  ncert=ACC + "AC voltage applied to an inductor", seconds=30, rc=True)

q(EMI, "Faraday's and Lenz's laws", "Basic", "direct",
  "A long straight wire lies in the plane of the page and carries a current directed towards the top of the page. "
  "A rectangular conducting loop lies in the same plane, to the right of the wire. The current in the wire is "
  "increasing. As seen by a reader looking at the page, the current induced in the loop is:",
  *opt("anticlockwise", ["clockwise", "zero, because the loop does not move", "clockwise in the side nearer the wire "
                                                                              "only"], "C"),
  "Lenz's law: the induced current opposes the change of flux that produces it",
  "By the right-hand rule, the field of the upward current is into the page at points to the right of the wire. "
  "As the current grows, the inward flux through the loop increases. The induced current must produce an outward "
  "field inside the loop, which requires an anticlockwise current.",
  ["Field of wire on its right: into the page", "Inward flux increasing",
   "Induced field must be out of the page → anticlockwise current"],
  why="Clockwise would add to the increasing inward flux, against Lenz's law. A changing flux induces an emf even in "
      "a stationary loop. The current in a single closed loop is the same all round it; it cannot flow in one side "
      "only.",
  ncert=EC + "Lenz's law and conservation of energy", seconds=45)

q(EMI, "Faraday's and Lenz's laws", "Basic", "statement_pair",
  sp("For a given rate of change of magnetic flux through each turn, the emf induced in a closely wound coil is "
     "proportional to its number of turns.",
     "Lenz's law gives the magnitude of the induced emf, while Faraday's law gives only its direction."),
  SP, sp_key(True, False),
  "Faraday's law ε = −N dΦ/dt; Lenz's law fixes the direction (the minus sign)",
  "Statement I is true: the emfs of the N turns add, ε = −N dΦ_B/dt. Statement II reverses the roles: Faraday's law "
  "gives the magnitude of the emf, and Lenz's law tells us its polarity (the induced current opposes the change in "
  "flux).",
  ["I: ε = N dΦ/dt → proportional to N → true", "II: the roles are reversed → false"],
  why="Statement II is false because Lenz's law is about the direction, not the magnitude, of the induced emf.",
  ncert=EC + "Faraday's law of induction; Lenz's law", seconds=35)

L_self = F(20) * F(2, 100) / (6 - 2)
assert L_self == F(1, 10) and F(20) * F(2, 100) / 6 != L_self and F(20) * F(2, 100) / 2 == F(1, 5)
assert 1 / L_self == 10
q(EMI, "Self and mutual inductance", "Basic", "numerical",
  "When the current in a coil rises steadily from 2.0 A to 6.0 A in 0.020 s, a self-induced emf of 20 V appears "
  "across it. The self-inductance of the coil is:",
  *opt("0.10 H", ["0.20 H", "10 H", "0.067 H"], "D"),
  "Self-induced emf ε = L dI/dt",
  "The current changes by 6.0 − 2.0 = 4.0 A in 0.020 s, i.e. at 200 A/s.",
  ["dI/dt = 4.0/0.020 = 200 A/s", "L = ε/(dI/dt) = 20/200 = 0.10 H"],
  why="0.20 H uses the initial current (2.0 A) instead of the change in current. 10 H inverts the ratio. 0.067 H "
      "uses the final current (6.0 A) instead of the change.",
  ncert=EC + "self-inductance", seconds=35, rc=True)

# ---- Intermediate
q_slide = F(5, 10) * F(4, 10) * 1 / 2
assert q_slide == F(1, 10) and F(5, 10) * F(4, 10) == F(1, 5) and F(1, 5) * 2 == F(2, 5)
q(EMI, "Faraday's and Lenz's laws", "Intermediate", "numerical",
  "A metal rod slides along two parallel conducting rails 0.40 m apart, which are joined at one end through a "
  "2.0 Ω resistor; the rod and rails have negligible resistance. A uniform magnetic field of 0.50 T acts at right "
  "angles to the plane of the rails. The rod is moved (not necessarily at constant speed) through a distance of "
  "1.0 m along the rails. The total charge that flows through the resistor is:",
  *opt("0.10 C", ["0.20 C", "0.40 C", "It cannot be found without knowing the speed of the rod"], "B"),
  "Charge driven round a circuit by induction: q = ΔΦ/R, independent of how fast the flux changes",
  "At each instant I = ε/R = (1/R) dΦ/dt, so the total charge is q = ∫I dt = ΔΦ/R. The flux changes by B × (area "
  "swept by the rod) = BLd, however fast or slowly the rod moves.",
  ["ΔΦ = BLd = 0.50 × 0.40 × 1.0 = 0.20 Wb", "q = ΔΦ/R = 0.20/2.0 = 0.10 C"],
  why="0.20 C is the change of flux in webers, not divided by the resistance. 0.40 C multiplies by R instead of "
      "dividing. The speed is not needed, because the charge depends only on the total change of flux.",
  ncert=EC + "Faraday's law of induction; motional electromotive force", seconds=70, rc=True)

P_avg = 0.5 * 100 * 5 * math.cos(math.pi / 3)
close(P_avg, 125)
close(100 * 5 * math.cos(math.pi / 3), 250)
close(0.5 * 100 * 5 * math.cos(math.pi / 6), 216.5)
q(EMI, "LCR resonance and power", "Intermediate", "numerical",
  "In an AC circuit, the voltage applied and the current drawn are v = 100 sin(ωt) volt and "
  "i = 5.0 sin(ωt − π/3) ampere. The average power consumed by the circuit is:",
  *opt("125 W", ["250 W", "500 W", "217 W"], "D"),
  "Average power P = V_rms I_rms cos φ = ½V₀I₀ cos φ",
  "The current lags the voltage by φ = π/3, so the power factor is cos 60° = 0.5. The rms values are the peak "
  "values divided by √2, so V_rms I_rms = ½V₀I₀.",
  ["½V₀I₀ = ½ × 100 × 5.0 = 250 W", "P = 250 × cos 60° = 125 W"],
  why="250 W uses the peak values without the factor ½ (or forgets the power factor). 500 W multiplies the peak "
      "values directly. 217 W uses cos 30° instead of cos 60°.",
  ncert=ACC + "power in AC circuit: the power factor", seconds=50, rc=True)

e_inst = 100 * 0.1 * 0.1 * 100 * math.sin(rad(30))
close(e_inst, 50)
close(100 * 0.1 * 0.1 * 100 * math.cos(rad(30)), 86.6, 1e-3)
q(EMI, "AC generator and transformer", "Intermediate", "numerical",
  "The coil of an AC generator has 100 turns, each of area 0.10 m², and rotates at 100 rad/s about an axis "
  "perpendicular to a uniform magnetic field of 0.10 T. At t = 0 the plane of the coil is perpendicular to the "
  "field. The magnitude of the emf induced in the coil at the instant when it has turned through 30° from this "
  "position is:",
  *opt("50 V", ["87 V", "100 V", "zero"], "A"),
  "Emf of an AC generator ε = NBAω sin ωt, with ωt measured from the position of maximum flux",
  "With the plane perpendicular to B at t = 0, the flux is Φ = NBA cos ωt and the emf is NBAω sin ωt. The peak emf "
  "is NBAω = 100 × 0.10 × 0.10 × 100 = 100 V.",
  ["ε₀ = NBAω = 100 V", "ε = ε₀ sin 30° = 50 V"],
  why="87 V uses cos 30°, which would apply if the angle were measured from the position where the plane is "
      "parallel to the field. 100 V is the peak emf, reached only when the plane is parallel to the field. Zero is "
      "the emf at t = 0, when the flux is maximum.",
  ncert=EC + "AC generator", seconds=60, rc=True)

q(EMI, "AC: rms, reactance and impedance", "Intermediate", "assertion_reason",
  ar("The rms value of a sinusoidal alternating current is larger than its peak value.",
     "For a sinusoidal current of peak value i_m, the rms value is i_m/√2."),
  AR, ar_key(False, True),
  "rms (effective) value of a sinusoidal current",
  "R is the standard result I = i_m/√2 ≈ 0.707 i_m. It shows that the rms value is smaller than the peak value, so "
  "A is false.",
  ["R: I_rms = i_m/√2 → true", "Since √2 > 1, I_rms < i_m → A false"],
  why="A contradicts R: dividing by √2 makes the rms value about 0.71 of the peak value.",
  ncert=ACC + "AC voltage applied to a resistor (rms or effective current)", seconds=30)

q(EMI, "AC: rms, reactance and impedance", "Intermediate", "match_list",
  ml("Match each quantity in List-I with the way it depends on the frequency of the AC source (List-II).",
     ["Resistance of an ideal resistor", "Reactance of an ideal inductor", "Reactance of an ideal capacitor",
      "Impedance of a series LCR circuit"],
     ["Inversely proportional to the frequency", "Independent of the frequency",
      "Least at the resonant frequency", "Directly proportional to the frequency"]),
  *mlo("A-II, B-IV, C-I, D-III", ["A-II, B-I, C-IV, D-III", "A-III, B-IV, C-I, D-II", "A-IV, B-II, C-I, D-III"],
       "B"),
  "X_L = ωL, X_C = 1/(ωC), Z = √[R² + (X_C − X_L)²]",
  "A resistance does not depend on frequency. X_L = 2πfL grows in proportion to f, and X_C = 1/(2πfC) falls as 1/f. "
  "The impedance of a series LCR circuit is least, equal to R, at the resonant frequency where X_L = X_C.",
  ["R → independent (II)", "X_L ∝ f (IV)", "X_C ∝ 1/f (I)", "Z minimum at resonance (III)"],
  why="B-I, C-IV interchanges the inductor and the capacitor. A-III, D-II interchanges the resistor and the LCR "
      "circuit. A-IV, B-II interchanges the resistor and the inductor.",
  ncert=ACC + "AC voltage applied to an inductor; to a capacitor; series LCR circuit", seconds=45)

Zrl = math.hypot(60, 80)
I_rl = 100 / Zrl
truth = {"a": abs(I_rl - 1) < 1e-12, "b": abs(60 / Zrl - 0.8) < 1e-9, "c": abs(I_rl ** 2 * 60 - 60) < 1e-9,
         "d": abs(I_rl * 60 + I_rl * 80 - 100) < 1e-9, "e": True}
assert truth == {"a": True, "b": False, "c": True, "d": False, "e": True}
assert abs(math.atan2(80, 60) - math.atan(4 / 3)) < 1e-12
q(EMI, "AC: rms, reactance and impedance", "Intermediate", "multi_statement",
  ms("A 60 Ω resistor and an ideal inductor of reactance 80 Ω are connected in series to a 100 V (rms) AC supply. "
     "Which of the following statements are correct?",
     ["The rms current in the circuit is 1.0 A.",
      "The power factor of the circuit is 0.80.",
      "The average power drawn from the supply is 60 W.",
      "The rms voltages across the resistor and across the inductor add up to 100 V.",
      "The current lags behind the supply voltage by the angle tan⁻¹(4/3)."]),
  *mso(truth, "ace", ["abc", "acd", "bde"], "A"),
  "Series RL circuit: Z = √(R² + X_L²), cos φ = R/Z, tan φ = X_L/R",
  "Z = √(60² + 80²) = 100 Ω, so I = 1.0 A. The power factor is R/Z = 0.60 and the power is I²R = 60 W. The rms "
  "voltages are 60 V and 80 V; they are 90° out of phase, so they add as phasors (√(60² + 80²) = 100 V), not "
  "arithmetically. The current lags by φ with tan φ = 80/60 = 4/3.",
  ["(a) I = 100/100 = 1.0 A → true", "(b) cos φ = 60/100 = 0.60 → false", "(c) P = 1² × 60 = 60 W → true",
   "(d) 60 V + 80 V = 140 V ≠ 100 V → false", "(e) tan φ = 4/3, current lags → true"],
  why="(b) gives sin φ (0.80) instead of cos φ (0.60). (d) adds the rms voltages arithmetically, ignoring their 90° "
      "phase difference.",
  ncert=ACC + "series LCR circuit; power in AC circuit: the power factor", seconds=90, rc=True)

# ---- Advanced
I_line1, I_line2 = 1e6 / 1e4, 1e6 / 1e5
loss1, loss2 = I_line1 ** 2 * 5, I_line2 ** 2 * 5
close(loss1, 5.0e4)
close(loss2, 5.0e2)
close(0.5 * loss1, 2.5e4)
close(loss1 / 10, 5.0e3)
q(EMI, "AC generator and transformer", "Advanced", "numerical",
  "A power of 1.0 MW is to be sent to a town through transmission lines of total resistance 5.0 Ω. The losses in "
  "the lines are calculated first for transmission at 10 kV (rms) and then for transmission at 100 kV (rms), the "
  "voltage being raised by a step-up transformer at the power station. Treating the load as drawing current in "
  "phase with the voltage, the power lost in the lines in the two cases is, respectively:",
  *opt("50 kW and 0.50 kW", ["50 kW and 5.0 kW", "25 kW and 0.25 kW", "20 MW and 2.0 GW"], "C"),
  "Line loss I²R with I = P/V: raising the voltage lowers the current and the loss as 1/V²",
  "For a fixed power transmitted, the line current is P/V. The loss in the lines is I²R, so a tenfold rise in "
  "voltage reduces the current tenfold and the loss a hundredfold.",
  ["At 10 kV: I = 10⁶/10⁴ = 100 A; loss = 100² × 5.0 = 5.0 × 10⁴ W = 50 kW (5% of the power)",
   "At 100 kV: I = 10 A; loss = 10² × 5.0 = 500 W = 0.50 kW"],
  why="50 kW and 5.0 kW takes the loss as falling in proportion to 1/V instead of 1/V². 25 kW and 0.25 kW puts a "
      "needless factor ½ in, as if the rms current were half the value P/V. 20 MW and 2.0 GW uses V²/R with the "
      "transmission voltage, which is not the voltage across the lines.",
  ncert=ACC + "transformers (transmission of electrical energy)", seconds=100, rc=True)

e0g = 100 * 0.20 * 0.050 * 100
P_g = e0g ** 2 / (2 * 50)
tau_g = P_g / 100
close(e0g, 100)
close(P_g, 100)
close(tau_g, 1.0)
close(e0g ** 2 / 50 / 100, 2.0)
close(P_g / 100 ** 2, 0.010)
q(EMI, "AC generator and transformer", "Advanced", "numerical",
  "The coil of an AC generator has 100 turns, each of area 0.050 m², and rotates at a constant angular speed of "
  "100 rad/s about an axis perpendicular to a uniform magnetic field of 0.20 T. Its ends are connected to a 50 Ω "
  "resistor; the coil's own resistance and all friction are negligible. The average torque that must be applied to "
  "keep the coil rotating at this speed is:",
  *opt("1.0 N m", ["2.0 N m", "100 N m", "0.010 N m"], "A"),
  "Energy conservation: mechanical power supplied = electrical power dissipated; P = τω",
  "The peak emf is NBAω. The average power in the resistor is ε₀²/(2R). This power must be supplied by the applied "
  "torque, whose average value is P/ω.",
  ["ε₀ = 100 × 0.20 × 0.050 × 100 = 100 V", "P_avg = ε₀²/(2R) = 100²/(2 × 50) = 100 W",
   "τ_avg = P/ω = 100/100 = 1.0 N m"],
  why="2.0 N m uses ε₀²/R, forgetting that the average of sin² over a cycle is ½. 100 N m gives the power in watts as "
      "if it were the torque. 0.010 N m divides the power by ω².",
  ncert=EC + "AC generator; " + ACC + "power in AC circuit", seconds=120, rc=True)

M_loops = MU0 * math.pi * 0.010 ** 2 / (2 * 0.20)
close(M_loops, 9.9e-10, 5e-3)
close(MU0 * math.pi * 0.010 ** 2 / 0.20, 2.0e-9, 0.02)
close(MU0 * math.pi * 0.010 ** 2 / (4 * 0.20), 4.9e-10, 0.01)
close(MU0 * 0.010 ** 2 / (2 * 0.20), 3.1e-10, 0.02)
q(EMI, "Self and mutual inductance", "Advanced", "numerical",
  "A small single-turn circular loop of radius 1.0 cm is placed at the centre of a large single-turn circular loop "
  "of radius 20 cm, the two loops being coplanar and concentric. Treating the magnetic field of the large loop as "
  "uniform over the small loop, and taking µ₀ = 4π × 10⁻⁷ T m A⁻¹, the mutual inductance of the pair is about:",
  *opt("9.9 × 10⁻¹⁰ H", ["2.0 × 10⁻⁹ H", "4.9 × 10⁻¹⁰ H", "3.1 × 10⁻¹⁰ H"], "D"),
  "Mutual inductance M = Φ₂/I₁; field at the centre of a loop B = µ₀I/(2R)",
  "A current I₁ in the large loop gives a field µ₀I₁/(2R) at its centre, which is nearly uniform over the small "
  "loop. The flux through the small loop is this field times its area πr².",
  ["Φ₂ = [µ₀I₁/(2R)] × πr²", "M = µ₀πr²/(2R) = 4π × 10⁻⁷ × π × (0.010)²/(2 × 0.20)",
   "M = π² × 10⁻¹⁰ ≈ 9.9 × 10⁻¹⁰ H"],
  why="2.0 × 10⁻⁹ H uses µ₀I/R for the field at the centre (factor 2 missing). 4.9 × 10⁻¹⁰ H uses µ₀I/(4R). "
      "3.1 × 10⁻¹⁰ H takes the area of the small loop as r² instead of πr².",
  ncert=EC + "mutual inductance", seconds=110, rc=True)

L_fac = F(2) ** 2 * F(1, 2) ** 2 / 2
assert L_fac == F(1, 2) and F(2) ** 2 / 2 == 2 and F(2) ** 2 * F(1, 2) ** 2 == 1 and F(2) * F(1, 2) ** 2 / 2 == F(1, 4)
q(EMI, "Self and mutual inductance", "Advanced", "numerical",
  "A long air-cored solenoid has self-inductance L. It is rewound so that its total number of turns is doubled, its "
  "length is doubled and its radius is halved (it stays long compared with its radius). Its new self-inductance is:",
  *opt("L/2", ["2L", "L", "L/4"], "A"),
  "Self-inductance of a long solenoid L = µ₀n²Al = µ₀N²πr²/l",
  "Write L in terms of the total number of turns N: with n = N/l, L = µ₀(N/l)²(πr²)l = µ₀N²πr²/l.",
  ["L ∝ N²r²/l", "New L = L × 2² × (1/2)² ÷ 2 = L/2"],
  why="2L ignores the change of radius. L ignores the change of length. L/4 takes L as proportional to N instead "
      "of N².",
  ncert=EC + "self-inductance (long solenoid)", seconds=70, rc=True)

q(EMI, "Self and mutual inductance", "Advanced", "match_list",
  ml("Match each quantity in List-I with its expression in List-II. (n, n₁, n₂ = turns per unit length; A = area of "
     "cross-section; l = length; r₁ = radius of the inner solenoid; B = magnetic field in vacuum.)",
     ["Self-inductance of a long solenoid", "Mutual inductance of two long coaxial solenoids of length l",
      "Magnetic energy stored in an inductor L carrying current I", "Magnetic energy per unit volume of a field B"],
     ["B²/(2µ₀)", "µ₀n²Al", "½LI²", "µ₀n₁n₂πr₁²l"]),
  *mlo("A-II, B-IV, C-III, D-I", ["A-IV, B-II, C-III, D-I", "A-II, B-IV, C-I, D-III", "A-III, B-IV, C-II, D-I"],
       "C"),
  "Inductance of solenoids and magnetic energy",
  "For a long solenoid, Φ per turn = µ₀nIA and N = nl, so L = µ₀n²Al. For coaxial solenoids, the field µ₀n₂I₂ of "
  "the outer one links the n₁l turns of the inner one over area πr₁², giving M = µ₀n₁n₂πr₁²l. The work done "
  "against the self-induced emf in building up a current I is ½LI². Dividing ½LI² for a solenoid by its volume Al "
  "gives the energy density B²/(2µ₀).",
  ["Solenoid L → II", "Coaxial M → IV", "Energy in inductor → III", "Energy density → I"],
  why="A-IV, B-II interchanges self- and mutual inductance. C-I, D-III interchanges the total energy and the energy "
      "per unit volume. A-III, C-II interchanges the inductance and the energy.",
  ncert=EC + "inductance (self-inductance and mutual inductance)", seconds=60)


# ================================================================ Electromagnetic Waves (B2 I2 A2)
WC = NC + "'Electromagnetic Waves', "

q(EMW, "EM spectrum and uses", "Basic", "direct",
  "According to NCERT, the radiation focused through a laser in LASIK (laser-assisted in situ keratomileusis) eye "
  "surgery belongs to the:",
  *opt("ultraviolet region", ["infrared region", "microwave region", "gamma-ray region"], "B"),
  "Uses of different parts of the electromagnetic spectrum",
  "NCERT notes that ultraviolet radiation can be focused into very narrow beams for high-precision applications "
  "such as LASIK eye surgery.",
  ["UV can be focused into very narrow beams → used in LASIK"],
  why="Infrared is used in remote switches and physical therapy, microwaves in radar and ovens, and gamma rays to "
      "destroy cancer cells; none of these is the radiation NCERT names for LASIK.",
  ncert=WC + "electromagnetic spectrum (ultraviolet rays)", seconds=25)

lam_radio = 3e8 / 1.5e6
close(lam_radio, 200)
q(EMW, "EM wave properties", "Basic", "numerical",
  "A radio station broadcasts at a frequency of 1.5 MHz. Taking the speed of electromagnetic waves in air as "
  "3.0 × 10⁸ m/s, the wavelength of the waves is:",
  *opt("200 m", ["0.20 m", "4.5 × 10¹⁴ m", "2.0 × 10⁵ m"], "B"),
  "c = fλ for electromagnetic waves",
  "All electromagnetic waves travel at c in vacuum (and very nearly in air), so λ = c/f.",
  ["λ = c/f = 3.0 × 10⁸/(1.5 × 10⁶) = 200 m"],
  why="0.20 m treats 1.5 MHz as 1.5 GHz. 4.5 × 10¹⁴ m multiplies c by f. 2.0 × 10⁵ m takes MHz as kHz.",
  ncert=WC + "electromagnetic waves (speed c = fλ)", seconds=25, rc=True)

E_vec, B_dir = (0, 0, 1), (1, 0, 0)
prop = (E_vec[1] * B_dir[2] - E_vec[2] * B_dir[1], E_vec[2] * B_dir[0] - E_vec[0] * B_dir[2],
        E_vec[0] * B_dir[1] - E_vec[1] * B_dir[0])
assert prop == (0, 1, 0)
close(30 / 3e8, 1.0e-7)
q(EMW, "EM wave properties", "Intermediate", "numerical",
  "At a certain point and instant, the electric field of a plane electromagnetic wave travelling in vacuum has a "
  "magnitude of 30 V/m and points along +z, while its magnetic field points along +x. Taking c = 3.0 × 10⁸ m/s, the "
  "magnitude of the magnetic field and the direction of propagation of the wave are:",
  *opt("1.0 × 10⁻⁷ T; along +y", ["1.0 × 10⁻⁷ T; along −y", "9.0 × 10⁹ T; along +y", "1.0 × 10⁻⁷ T; along +z"],
       "C"),
  "In a plane EM wave B₀ = E₀/c, and the wave travels along E × B",
  "E, B and the direction of propagation are mutually perpendicular, and the propagation is along E × B. "
  "Here ẑ × x̂ = ŷ.",
  ["B = E/c = 30/(3.0 × 10⁸) = 1.0 × 10⁻⁷ T", "Direction of propagation: E × B = ẑ × x̂ = +ŷ"],
  why="−y comes from taking B × E instead of E × B. 9.0 × 10⁹ T multiplies E by c. The wave cannot travel along +z, "
      "the direction of its own electric field, because the wave is transverse.",
  ncert=WC + "electromagnetic waves (nature of electromagnetic waves)", seconds=50, rc=True)

q(EMW, "EM spectrum and uses", "Intermediate", "statement_pair",
  sp("Gamma rays are used in medicine to destroy cancer cells.",
     "Visible light occupies the wavelength range from about 100 nm to 400 nm."),
  SP, sp_key(True, False),
  "Uses and wavelength ranges of parts of the electromagnetic spectrum",
  "Statement I is true: NCERT lists the destruction of cancer cells as a medical use of gamma rays. Statement II is "
  "false: visible light extends from about 400 nm to about 700 nm; wavelengths shorter than about 400 nm are "
  "ultraviolet.",
  ["I: gamma rays destroy cancer cells → true", "II: visible ≈ 400–700 nm → false"],
  why="The range in Statement II belongs to the ultraviolet, not to visible light.",
  ncert=WC + "electromagnetic spectrum", seconds=35)

q(EMW, "Displacement current", "Advanced", "assertion_reason",
  ar("While a capacitor is being charged, there is a magnetic field in the gap between its plates, although no "
     "charge flows across the gap.",
     "A changing electric flux produces a magnetic field in the same way as a conduction current does; Maxwell "
     "called the term ε₀ dΦ_E/dt the displacement current."),
  AR, ar_key(True, True, True),
  "Ampere–Maxwell law: ∮B·dl = µ₀(i_c + ε₀ dΦ_E/dt)",
  "No conduction current crosses the gap, but the electric field between the plates grows as the capacitor "
  "charges, so the electric flux through the gap changes. By the Ampere–Maxwell law this displacement current is "
  "a source of magnetic field, just like a conduction current, which is why there is a magnetic field in the gap. "
  "R is the reason for A.",
  ["A: magnetic field exists in the gap → true", "R: dΦ_E/dt term acts as a source of B → true",
   "The changing flux in the gap is what produces that field → R explains A"],
  why="Both are true and the displacement current of R is precisely the source of the field described in A.",
  ncert=WC + "displacement current", seconds=50)

c0 = 3e8
bands = {"A": c0 / 100e6, "B": c0 / 10e9, "C": c0 / 6e14, "D": c0 / 3e18}
close(bands["A"], 3.0)
close(bands["B"], 0.03)
close(bands["C"], 5.0e-7)
close(bands["D"], 1.0e-10)
assert bands["A"] > 0.1 and 1e-3 < bands["B"] < 0.1 and 400e-9 < bands["C"] < 700e-9 and 1e-13 < bands["D"] < 1e-8
q(EMW, "EM spectrum and uses", "Advanced", "match_list",
  ml("Match each electromagnetic wave in List-I, given by its frequency, with the part of the spectrum to which it "
     "belongs (List-II). Take c = 3 × 10⁸ m/s and use the wavelength ranges given in NCERT.",
     ["100 MHz", "10 GHz", "6 × 10¹⁴ Hz", "3 × 10¹⁸ Hz"],
     ["Visible light", "X-rays", "Radio waves", "Microwaves"]),
  *mlo("A-III, B-IV, C-I, D-II", ["A-IV, B-III, C-I, D-II", "A-III, B-IV, C-II, D-I", "A-IV, B-I, C-III, D-II"],
       "D"),
  "λ = c/f, then compare with the wavelength ranges of the spectrum",
  "Convert each frequency to a wavelength: 100 MHz → 3 m (radio, > 0.1 m); 10 GHz → 3 cm (microwaves, 0.1 m to "
  "1 mm); 6 × 10¹⁴ Hz → 500 nm (visible, about 400–700 nm); 3 × 10¹⁸ Hz → 0.1 nm (X-rays, about 10 nm to "
  "10⁻⁴ nm).",
  ["100 MHz → 3 m → radio (III)", "10 GHz → 3 cm → microwave (IV)", "6 × 10¹⁴ Hz → 500 nm → visible (I)",
   "3 × 10¹⁸ Hz → 0.1 nm → X-rays (II)"],
  why="A-IV, B-III interchanges radio waves and microwaves (the higher frequency is the microwave). C-II, D-I "
      "interchanges visible light and X-rays. A-IV, B-I, C-III scrambles the order of increasing frequency.",
  ncert=WC + "electromagnetic spectrum", seconds=70, rc=True)


# ================================================================ Optics (B7 I8 A7)
RO = NC + "'Ray Optics and Optical Instruments', "
WO = NC + "'Wave Optics', "

# ---- Basic
assert F(400, 2) / F(2) == 100 and F(400) / 2 == 200
q(OPT, "Optical instruments", "Basic", "numerical",
  "A reflecting telescope has a concave objective mirror of radius of curvature 4.0 m and an eyepiece of focal "
  "length 2.0 cm. Its magnifying power in normal adjustment is:",
  *opt("100", ["200", "50", "0.01"], "B"),
  "Magnifying power of a telescope in normal adjustment m = f_o/f_e; for a mirror f = R/2",
  "The objective mirror has focal length R/2 = 2.0 m = 200 cm. The magnifying power is f_o/f_e.",
  ["f_o = 4.0/2 = 2.0 m = 200 cm", "m = 200/2.0 = 100"],
  why="200 uses the radius of curvature as the focal length. 50 halves the result twice. 0.01 is f_e/f_o, the ratio "
      "inverted.",
  ncert=RO + "optical instruments (telescope)", seconds=35, rc=True)

t_glass = 1.5 * 3.0e-3 / 3e8
close(t_glass, 1.5e-11)
close(3.0e-3 / 3e8, 1.0e-11)
close(1.5 ** 2 * 3.0e-3 / 3e8, 2.25e-11)
close(3.0e-3 / (1.5 * 3e8), 6.7e-12, 1e-2)
q(OPT, "Refraction and lenses", "Basic", "numerical",
  "Light falls normally on a glass plate 3.0 mm thick, of refractive index 1.5. Taking the speed of light in vacuum "
  "as 3.0 × 10⁸ m/s, the time taken by the light to cross the plate is:",
  *opt("1.5 × 10⁻¹¹ s", ["1.0 × 10⁻¹¹ s", "2.25 × 10⁻¹¹ s", "6.7 × 10⁻¹² s"], "D"),
  "Speed of light in a medium v = c/n",
  "In the glass the light travels at c/n = 2.0 × 10⁸ m/s, so it takes longer than in vacuum to cover the same "
  "thickness.",
  ["v = 3.0 × 10⁸/1.5 = 2.0 × 10⁸ m/s", "t = 3.0 × 10⁻³/(2.0 × 10⁸) = 1.5 × 10⁻¹¹ s"],
  why="1.0 × 10⁻¹¹ s uses the speed in vacuum. 2.25 × 10⁻¹¹ s multiplies by n twice. 6.7 × 10⁻¹² s uses nc instead "
      "of c/n, as if light were faster in glass.",
  ncert=RO + "refraction", seconds=30, rc=True)

q(OPT, "Huygens' principle and interference", "Basic", "direct",
  "In Huygens' construction, each point of a wavefront is a source of secondary wavelets, but only the forward "
  "envelope of the wavelets is taken as the new wavefront. NCERT justifies ignoring the backward wave by:",
  *opt("assuming that the amplitude of the secondary wavelets is maximum in the forward direction and zero in the "
       "backward direction",
       ["the fact that light cannot travel backwards in any medium",
        "assuming that the secondary wavelets travel faster in the forward direction",
        "the destructive interference of the backward wavelets with the incident wave, which Huygens proved"], "A"),
  "Huygens' principle and its ad hoc assumption about the backwave",
  "NCERT notes that a backwave is not observed, and that Huygens explained its absence by assuming the amplitude of "
  "the secondary wavelets to be maximum in the forward direction and zero in the backward direction. This is an ad "
  "hoc assumption that gives the right result; the backwave is properly removed only by a more rigorous wave "
  "theory.",
  ["Backwave not observed", "Huygens: amplitude of secondary wavelets zero in the backward direction (ad hoc)"],
  why="Light can of course travel in any direction (reflection sends it back). The wavelets travel at the same "
      "speed in all directions in a uniform medium. Huygens gave no interference proof; the assumption is ad hoc.",
  ncert=WO + "Huygens principle", seconds=40)

phi = 3 * math.pi
path = phi / (2 * math.pi)
close(path, 1.5)
assert math.isclose(math.cos(phi / 2) ** 2, 0, abs_tol=1e-12)
q(OPT, "Huygens' principle and interference", "Basic", "numerical",
  "Two coherent light waves of the same wavelength λ and equal intensity, coming from in-phase sources, meet at a "
  "point with a phase difference of 3π. The path difference between them and the nature of the point are:",
  *opt("3λ/2; a dark point (zero intensity)", ["3λ; a bright point", "3λ/2; a bright point",
                                             "3λ/4; a point of intensity half the maximum"], "C"),
  "Phase difference φ = (2π/λ) × path difference; intensity I = 4I₀ cos²(φ/2)",
  "A phase difference of 2π corresponds to a path difference of λ, so 3π corresponds to 3λ/2, an odd multiple of "
  "λ/2. The waves are in opposite phase and, having equal intensities, cancel completely.",
  ["Δx = (λ/2π) × 3π = 3λ/2", "I = 4I₀ cos²(3π/2) = 0 → dark"],
  why="3λ uses Δx = φλ/π. An odd multiple of λ/2 gives destructive, not constructive, interference. 3λ/4 halves the "
      "path difference again.",
  ncert=WO + "coherent and incoherent addition of waves; interference", seconds=35, rc=True)

i_pm = 30
dev = 180 - 2 * i_pm
assert dev == 120
q(OPT, "Mirrors", "Basic", "numerical",
  "A ray of light falls on a plane mirror at an angle of incidence of 30°. The angle through which the ray is "
  "deviated from its original direction by the reflection is:",
  *opt("120°", ["60°", "30°", "150°"], "B"),
  "Law of reflection; deviation by a plane mirror δ = 180° − 2i",
  "The angle of reflection equals the angle of incidence, 30°. The incident and reflected rays make an angle of "
  "2i = 60° with each other measured through the normal, so the reflected ray is turned through 180° − 60° from the "
  "original direction of travel.",
  ["Angle between incident and reflected rays (through the normal) = 2i = 60°", "Deviation = 180° − 60° = 120°"],
  why="60° is the angle between the incident and reflected rays, not the deviation. 30° is the angle of reflection. "
      "150° uses 180° − i.",
  ncert=RO + "reflection of light by spherical mirrors (laws of reflection)", seconds=35, rc=True)

speeds = {n: 3e8 / n for n in (1.5, 4 / 3, 2.0, 1.25)}
close(speeds[1.5], 2.0e8)
close(speeds[4 / 3], 2.25e8)
close(speeds[2.0], 1.5e8)
close(speeds[1.25], 2.4e8)
q(OPT, "Refraction and lenses", "Basic", "match_list",
  ml("Match the refractive index of each transparent medium in List-I with the speed of light in it (List-II). "
     "Take the speed of light in vacuum as 3.0 × 10⁸ m/s.",
     ["1.5", "4/3", "2.0", "1.25"],
     ["1.5 × 10⁸ m/s", "2.4 × 10⁸ m/s", "2.0 × 10⁸ m/s", "2.25 × 10⁸ m/s"]),
  *mlo("A-III, B-IV, C-I, D-II", ["A-IV, B-III, C-I, D-II", "A-III, B-IV, C-II, D-I", "A-I, B-IV, C-III, D-II"],
       "D"),
  "Absolute refractive index n = c/v",
  "The speed in each medium is c/n: the larger the refractive index, the smaller the speed.",
  ["3.0/1.5 = 2.0 → III", "3.0 × 3/4 = 2.25 → IV", "3.0/2.0 = 1.5 → I", "3.0/1.25 = 2.4 → II"],
  why="A-IV, B-III interchanges the values for 1.5 and 4/3. C-II, D-I interchanges those for 2.0 and 1.25. A-I, "
      "C-III gives the medium of index 2.0 a larger speed than that of index 1.5.",
  ncert=RO + "refraction", seconds=50, rc=True)

f_men = 1 / (0.5 * (1 / 20 - 1 / 30))
close(f_men, 120)
close(1 / (0.5 * (1 / 20 + 1 / 30)), 24)
close(1 / (1 / 20 - 1 / 30), 60)
q(OPT, "Refraction and lenses", "Basic", "numerical",
  "A thin glass lens (refractive index 1.5) has one convex surface of radius of curvature 20 cm and one concave "
  "surface of radius of curvature 30 cm, the centres of curvature of both surfaces lying on the same side of the "
  "lens (a converging meniscus). Its focal length in air is:",
  *opt("120 cm", ["24 cm", "60 cm", "−120 cm"], "C"),
  "Lens maker's formula 1/f = (n − 1)(1/R₁ − 1/R₂) with the Cartesian sign convention",
  "With light going left to right and both centres of curvature on the right, R₁ = +20 cm and R₂ = +30 cm.",
  ["1/f = 0.5 × (1/20 − 1/30) = 0.5 × 1/60 = 1/120", "f = +120 cm (converging)"],
  why="24 cm treats the lens as biconvex (adds 1/20 and 1/30). 60 cm leaves out the factor (n − 1) = 0.5. −120 cm "
      "has the sign wrong: the more strongly curved surface is the convex one, so the lens converges.",
  ncert=RO + "refraction by a lens (lens maker's formula)", seconds=50, rc=True)

# ---- Intermediate
assert math.isqrt(9 * 4) == 6
q(OPT, "Refraction and lenses", "Intermediate", "numerical",
  "An object and a screen are fixed a certain distance apart, and a convex lens placed between them forms a sharp "
  "image on the screen at two different positions of the lens. The heights of the two images are 9.0 cm and 4.0 cm. "
  "The height of the object is:",
  *opt("6.0 cm", ["6.5 cm", "5.0 cm", "2.25 cm"], "A"),
  "Conjugate positions: the object and image distances interchange, so m₁m₂ = 1",
  "In the two positions u and v are interchanged, so the magnifications are v/u and u/v, whose product is 1. Hence "
  "h₁h₂ = h², the object height being the geometric mean of the image heights.",
  ["m₁ = h₁/h, m₂ = h₂/h, m₁m₂ = 1", "h = √(h₁h₂) = √(9.0 × 4.0) = 6.0 cm"],
  why="6.5 cm is the arithmetic mean of the image heights. 5.0 cm is their difference. 2.25 cm is their ratio.",
  ncert=RO + "refraction by a lens; magnification", seconds=50, rc=True)

v_o = 20 - 5
u_o = 1 / (1 / v_o - 1 / 1.0)
close(-u_o, 15 / 14)
close(-1 / (1 / 20 - 1), 20 / 19)
q(OPT, "Optical instruments", "Intermediate", "numerical",
  "A compound microscope has an objective of focal length 1.0 cm and an eyepiece of focal length 5.0 cm, placed "
  "20 cm apart. It is adjusted so that the final image is at infinity. The distance of the object from the "
  "objective is about:",
  *opt("1.07 cm", ["1.05 cm", "1.25 cm", "1.00 cm"], "B"),
  "For the final image at infinity, the intermediate image lies at the focus of the eyepiece",
  "The image formed by the objective must be 5.0 cm in front of the eyepiece, i.e. 20 − 5 = 15 cm from the "
  "objective. The lens formula for the objective then gives the object distance.",
  ["v_o = 20 − 5.0 = 15 cm", "1/u = 1/v − 1/f = 1/15 − 1/1.0 = −14/15", "|u| = 15/14 ≈ 1.07 cm"],
  why="1.05 cm takes the image of the objective at the eyepiece itself (v = 20 cm). 1.25 cm takes v = 5.0 cm. "
      "1.00 cm puts the object at the focus, which would send the intermediate image to infinity.",
  ncert=RO + "optical instruments (compound microscope)", seconds=75, rc=True)

iB_int = deg(math.atan(1 / math.sqrt(2)))
close(iB_int, 35.3, 2e-3)
close(deg(math.atan(math.sqrt(2))), 54.7, 2e-3)
q(OPT, "Polarisation", "Intermediate", "numerical",
  "Unpolarised light travelling inside a block of glass of refractive index √2 falls on the plane surface between "
  "the glass and air. The angle of incidence (inside the glass) for which the light reflected back into the glass "
  "is completely plane polarised is about:",
  *opt("35.3°", ["54.7°", "45°", "No such angle exists, because light going from glass into air cannot be "
                                 "polarised by reflection"], "D"),
  "Brewster's law tan i_B = n₂/n₁, for light going from medium 1 into medium 2",
  "Here the light is incident from the glass (n₁ = √2) on air (n₂ = 1), so tan i_B = 1/√2. This angle is smaller "
  "than the critical angle (45°), so a refracted ray exists, perpendicular to the reflected ray.",
  ["tan i_B = n_air/n_glass = 1/√2", "i_B = tan⁻¹(0.707) ≈ 35.3°"],
  why="54.7° (tan⁻¹ √2) is the Brewster angle for light incident from air on the glass. 45° is the critical angle, "
      "at which there is no refracted ray. Brewster's law applies whichever side the light comes from.",
  ncert=WO + "polarisation by reflection (Brewster's law)", seconds=60, rc=True)

u_par = -10 * 1.0 / (1.5 - 1.0)
close(u_par, -20)
close(10 * 1.5 / 0.5, 30)
close(10 * 0.5 / 1.0, 5.0)
q(OPT, "Refraction and lenses", "Intermediate", "numerical",
  "A long glass rod (refractive index 1.5) has one end ground to a convex hemispherical surface of radius of "
  "curvature 10 cm. A point object in air lies on the axis of the rod. For the light from it to travel inside the "
  "rod as a parallel beam (along the axis), the distance of the object from the pole of the curved surface must be:",
  *opt("20 cm", ["10 cm", "30 cm", "5.0 cm"], "B"),
  "Refraction at a spherical surface: n₂/v − n₁/u = (n₂ − n₁)/R",
  "A parallel beam inside the rod means the image is at infinity, so n₂/v = 0. With light travelling from air "
  "into glass, R = +10 cm.",
  ["0 − 1.0/u = (1.5 − 1.0)/10", "u = −10/0.5 = −20 cm", "The object is 20 cm in front of the surface"],
  why="10 cm puts the object at the centre of curvature. 30 cm is the second focal length, n₂R/(n₂ − n₁), where "
      "an incident parallel beam would focus inside the glass. 5.0 cm inverts the ratio, taking u = R(n₂ − n₁)/n₁.",
  ncert=RO + "refraction at spherical surfaces", seconds=70, rc=True)

q(OPT, "Polarisation", "Intermediate", "direct",
  "Unpolarised light falls on a glass surface at Brewster's angle. The reflected light is:",
  *opt("plane polarised, with its electric field vibrating perpendicular to the plane of incidence",
       ["plane polarised, with its electric field vibrating in the plane of incidence",
        "unpolarised, because reflection does not polarise light",
        "plane polarised, with its electric field along the direction of the reflected ray"], "C"),
  "Polarisation by reflection",
  "At Brewster's angle the reflected and refracted rays are perpendicular. The component of the electric field "
  "lying in the plane of incidence would have to vibrate along the reflected ray, which is not possible for a "
  "transverse wave, so it is absent from the reflected light. Only the component perpendicular to the plane of "
  "incidence is reflected.",
  ["Reflected ⊥ refracted at i_B", "In-plane component cannot be radiated along the reflected direction",
   "Reflected light: E ⊥ plane of incidence"],
  why="The in-plane component is the one missing from the reflected light. Reflection does polarise light. A light "
      "wave is transverse, so its electric field is never along its direction of travel.",
  ncert=WO + "polarisation by reflection", seconds=40)

truth = {"a": True, "b": True, "c": True, "d": False, "e": False}
q(OPT, "Refraction and lenses", "Intermediate", "multi_statement",
  ms("A small coin lies at the bottom of a beaker of water, and a parallel-sided glass slab is used in a separate "
     "experiment. Considering viewing along (or very near) the normal, which of the following statements are "
     "correct?",
     ["The apparent depth of the coin equals its real depth divided by the refractive index of water.",
      "For the same real depth, the coin would appear to be raised more if the liquid had a larger refractive "
      "index.",
      "A glass slab of thickness t and refractive index n placed over a mark makes the mark appear raised by "
      "t(1 − 1/n).",
      "The apparent shift produced by the slab depends on how far the mark is below the slab.",
      "The coin appears to be deeper than it really is."]),
  *mso(truth, "abc", ["ab", "abd", "ace"], "D"),
  "Real and apparent depth for near-normal viewing",
  "For near-normal viewing, apparent depth = real depth/n, so the coin appears raised by h(1 − 1/n), more for "
  "larger n. A slab of thickness t produces a normal shift t(1 − 1/n), which does not depend on the distance of the "
  "object below the slab. Since n > 1 the coin appears shallower, not deeper.",
  ["(a) h' = h/n → true", "(b) raise h(1 − 1/n) grows with n → true", "(c) slab shift t(1 − 1/n) → true",
   "(d) shift independent of distance → false", "(e) appears shallower → false"],
  why="(d) is false because the slab shift depends only on t and n. (e) is false because water makes the coin "
      "appear raised. Codes containing either, or missing (c), are wrong.",
  ncert=RO + "refraction (real and apparent depth)", seconds=60)

q(OPT, "Refraction and lenses", "Intermediate", "statement_pair",
  sp("The relation n₂/v − n₁/u = (n₂ − n₁)/R for refraction at a single spherical surface holds for paraxial rays "
     "(rays close to the axis and making small angles with it).",
     "Putting R → ∞ in this relation, for a plane surface, gives the image of an object in water seen from air "
     "along the normal at a depth equal to the real depth divided by the refractive index of water."),
  SP, sp_key(True, True),
  "Refraction at a spherical surface and its plane-surface limit",
  "Statement I is true: NCERT derives the relation using small-angle approximations, valid for paraxial rays. "
  "Statement II is true: with R → ∞, n₂/v = n₁/u. For an object in water (n₁ = 4/3) at depth h viewed from air "
  "(n₂ = 1), v = u/n₁ in magnitude, i.e. apparent depth = h/n.",
  ["I: small-angle (paraxial) derivation → true", "II: 1/v = (4/3)/u → |v| = h/(4/3) → true"],
  why="Both statements are correct, so every option calling either false is wrong.",
  ncert=RO + "refraction at spherical surfaces", seconds=50)

sinC = {"A": F(1) / F(3, 2), "B": F(1) / F(4, 3), "C": F(4, 3) / F(3, 2), "D": F(1, 2)}
assert sinC == {"A": F(2, 3), "B": F(3, 4), "C": F(8, 9), "D": F(1, 2)}
q(OPT, "Total internal reflection", "Intermediate", "match_list",
  ml("Light travels from the first medium into the second in each case of List-I. Match each case with the sine of "
     "the critical angle (List-II). Refractive indices: glass 1.5, water 4/3, medium X 2.0, air 1.",
     ["Glass to air", "Water to air", "Glass to water", "Medium X to air"],
     ["8/9", "1/2", "2/3", "3/4"]),
  *mlo("A-III, B-IV, C-I, D-II", ["A-IV, B-III, C-I, D-II", "A-III, B-IV, C-II, D-I", "A-I, B-IV, C-III, D-II"],
       "B"),
  "Critical angle: sin C = n_rarer/n_denser",
  "Total internal reflection needs light to go from the denser to the rarer medium, and sin C is the ratio of the "
  "smaller refractive index to the larger.",
  ["Glass → air: 1/1.5 = 2/3 (III)", "Water → air: 3/4 (IV)", "Glass → water: (4/3)/(3/2) = 8/9 (I)",
   "X → air: 1/2 (II)"],
  why="A-IV, B-III interchanges glass and water. C-II, D-I interchanges the glass–water pair and medium X. A-I, C-III "
      "interchanges glass–air with glass–water: against water the critical angle is larger, not smaller.",
  ncert=RO + "total internal reflection", seconds=55, rc=True)

# ---- Advanced
r1_gr = 60 - 45
sin_i = math.sqrt(2) * 0.259
close(sin_i, 0.366, 2e-3)
close(deg(math.asin(sin_i)), 21.5, 3e-3)
close(deg(math.asin(math.sqrt(2) * math.sin(rad(30)))), 45)
q(OPT, "Prism", "Advanced", "numerical",
  "A prism of refracting angle 60° is made of glass of refractive index √2. The least angle of incidence on the "
  "first face for which a ray can emerge from the second face (instead of being totally internally reflected there) "
  "is about (take sin 15° = 0.259 and sin⁻¹ 0.366 ≈ 21.5°):",
  *opt("21.5°", ["45°", "15°", "30°"], "C"),
  "Prism: r₁ + r₂ = A; emergence requires r₂ ≤ critical angle",
  "The ray just emerges (grazing the second face) when r₂ equals the critical angle C, with sin C = 1/√2, "
  "C = 45°. Then r₁ = 60° − 45° = 15°. For any smaller angle of incidence, r₁ is smaller, r₂ exceeds 45° and the "
  "ray is totally reflected.",
  ["sin C = 1/√2 → C = 45°", "r₁ = A − C = 15°", "sin i = √2 × sin 15° = 1.414 × 0.259 = 0.366 → i ≈ 21.5°"],
  why="45° is the angle of incidence for minimum deviation (r₁ = r₂ = 30°). 15° is the angle of refraction r₁, not "
      "the angle of incidence. 30° is A/2.",
  ncert=RO + "refraction through a prism; total internal reflection", seconds=120, rc=True)

v_o2 = 1 / (1 / 1.0 - 1 / 1.1)
u_e2 = 25 * 5 / (25 + 5)
close(v_o2, 11.0)
close(v_o2 + u_e2, 15.17, 1e-3)
close(v_o2 + 5, 16)
q(OPT, "Optical instruments", "Advanced", "numerical",
  "A compound microscope has an objective of focal length 1.0 cm and an eyepiece of focal length 5.0 cm. An object "
  "is placed 1.1 cm in front of the objective, and the final image is formed at the least distance of distinct "
  "vision, 25 cm from the eyepiece. The distance between the objective and the eyepiece is about:",
  *opt("15.2 cm", ["16.0 cm", "36.0 cm", "11.0 cm"], "D"),
  "Compound microscope: objective forms a real image, which acts as the object for the eyepiece",
  "The objective's image distance follows from the lens formula. The eyepiece must then be placed so that this "
  "image lies at the object distance that gives a virtual image 25 cm away.",
  ["Objective: 1/v = 1/1.0 − 1/1.1 → v = 11 cm", "Eyepiece: 1/u_e = 1/5 + 1/25 = 6/25 → u_e ≈ 4.17 cm",
   "Separation = 11 + 4.17 ≈ 15.2 cm"],
  why="16.0 cm puts the intermediate image at the focus of the eyepiece, which gives a final image at infinity. "
      "36.0 cm adds the 25 cm final image distance. 11.0 cm leaves out the eyepiece's object distance.",
  ncert=RO + "optical instruments (compound microscope)", seconds=120, rc=True)

d_l = 2.6e-6 / 600e-9
n_max = math.floor(d_l)
assert n_max == 4 and 2 * n_max + 1 == 9
q(OPT, "Huygens' principle and interference", "Advanced", "numerical",
  "In a two-slit interference experiment the slits are 2.6 µm apart and are illuminated by light of wavelength "
  "600 nm. A screen surrounds the slits far away, so that waves leaving the slits at any angle θ up to 90° on either "
  "side of the central direction can be observed. Using the path difference d sin θ, the total number of bright "
  "fringes (including the central one) is:",
  *opt("9", ["4", "8", "5"], "B"),
  "Bright fringes: d sin θ = nλ, with |sin θ| < 1",
  "The order n of a bright fringe must satisfy |n| = d sin θ/λ < d/λ = 2.6/0.60 ≈ 4.3. So n can be 0, ±1, ±2, "
  "±3 and ±4.",
  ["d/λ = 2.6 × 10⁻⁶/(6.0 × 10⁻⁷) ≈ 4.33", "Largest order n = 4", "Total = 2 × 4 + 1 = 9"],
  why="4 counts the orders on one side only, without the central fringe. 8 leaves out the central fringe. 5 counts "
      "one side together with the central fringe.",
  ncert=WO + "interference of light waves and Young's experiment", seconds=90, rc=True)

iB_15 = deg(math.atan(1.5))
close(iB_15, 56.3, 1e-3)
truth = {"a": True, "b": True, "c": True, "d": True, "e": False}
q(OPT, "Polarisation", "Advanced", "multi_statement",
  ms("Unpolarised light in air falls on a flat glass surface (refractive index 1.5) at Brewster's angle. Which of "
     "the following statements are correct?",
     ["The angle of incidence is tan⁻¹(1.5), about 56°.",
      "The reflected light is completely plane polarised.",
      "The refracted (transmitted) light is only partially polarised.",
      "If the reflected light is viewed through a polaroid that is slowly rotated, its intensity falls to zero at "
      "one orientation of the polaroid in each half-turn.",
      "Brewster's angle has the same value for all transparent media."]),
  *mso(truth, "abcd", ["abc", "abde", "bcd"], "A"),
  "Brewster's law tan i_B = n and polarisation by reflection",
  "At i_B = tan⁻¹ n the reflected light contains only the component perpendicular to the plane of incidence, so it "
  "is completely polarised. The transmitted light carries all the in-plane component and part of the "
  "perpendicular one, so it is only partially polarised. A polaroid whose pass axis is perpendicular to the "
  "vibration of the reflected light blocks it completely (twice per full turn). Brewster's angle depends on n, so "
  "it differs from medium to medium.",
  ["(a) tan⁻¹ 1.5 ≈ 56.3° → true", "(b) completely polarised → true", "(c) partially polarised → true",
   "(d) Malus: I = I₀cos²θ → zero when θ = 90° → true", "(e) depends on n → false"],
  why="(e) is false, since tan i_B = n differs between media; the codes containing (e) or missing (a) or (d) are "
      "wrong.",
  ncert=WO + "polarisation (polarisation by reflection; Malus's law)", seconds=90)

q(OPT, "Huygens' principle and interference", "Advanced", "assertion_reason",
  ar("For a thin convex lens forming a real image of a point object, light travelling along the axis (through the "
     "thick middle of the lens) and light travelling through the thin edge of the lens take the same time to go "
     "from the object to the image.",
     "Light travels more slowly in glass than in air; the ray through the edge goes a longer path in air, which "
     "makes up exactly for the extra thickness of glass crossed by the axial ray."),
  AR, ar_key(True, True, True),
  "Wave picture of a lens: equal travel times from a point object to its image",
  "NCERT notes that the total time taken from a point on the object to the corresponding point on the image is the "
  "same along any ray. The axial ray has the shortest geometric path but crosses the most glass, where light is "
  "slower. The edge ray crosses little glass but covers a longer path in air. The two effects balance, so all parts "
  "of the wave reach the image in phase. R gives exactly this balance, so it explains A.",
  ["A: equal times along all rays from object to image → true",
   "R: slower in glass at the centre, longer air path at the edge → true",
   "The balance in R is why the times are equal → R explains A"],
  why="Both statements are true and R is the reason for A, so the options that reject either statement or the "
      "explanation are wrong.",
  ncert=WO + "refraction and reflection of plane waves using Huygens principle (refraction by a lens)", seconds=60)

R_b = 4.0
v1 = 1.5 * R_b / 0.5
u2 = v1 - 2 * R_b
v2 = 1 / (0.5 / R_b + 1.5 / u2)
close(v1, 12.0)
close(u2, 4.0)
close(v2, 2.0)
q(OPT, "Refraction and lenses", "Advanced", "numerical",
  "A solid glass sphere of radius 4.0 cm and refractive index 1.5 is placed in air. A parallel beam of light falls "
  "on it along a diameter. Considering paraxial rays, the beam is brought to a focus:",
  *opt("2.0 cm beyond the far surface of the sphere", ["4.0 cm beyond the far surface of the sphere",
                                                     "6.0 cm beyond the far surface of the sphere",
                                                     "exactly at the far surface of the sphere"], "B"),
  "Refraction at two spherical surfaces in succession: n₂/v − n₁/u = (n₂ − n₁)/R",
  "The first surface alone would focus the beam 3R = 12 cm inside, i.e. 4.0 cm beyond the far surface. This "
  "converging beam meets the second surface, where it is refracted again and focused closer.",
  ["Surface 1 (air → glass, R = +4): 1.5/v₁ = 0.5/4 → v₁ = 12 cm",
   "This point is 12 − 8 = 4.0 cm beyond surface 2 (a virtual object, u₂ = +4 cm)",
   "Surface 2 (glass → air, R = −4): 1/v₂ − 1.5/4 = (1 − 1.5)/(−4) → 1/v₂ = 0.5 → v₂ = 2.0 cm"],
  why="4.0 cm stops after the first refraction. 6.0 cm is the distance of the focus from the centre, not from the "
      "far surface. A focus at the far surface would need a refractive index of 2.",
  ncert=RO + "refraction at spherical surfaces", seconds=150, rc=True)

q(OPT, "Diffraction", "Advanced", "statement_pair",
  sp("In the single-slit pattern, at the angle where a sin θ = 3λ/2 the slit can be divided into three equal parts; "
     "the contributions of two of them cancel and the third gives a secondary maximum.",
     "If the slit is made wider, all else unchanged, the secondary maxima move away from the centre of the pattern."),
  SP, sp_key(True, False),
  "Single-slit diffraction: dividing the slit into parts",
  "Statement I is NCERT's argument for the first secondary maximum at θ ≈ 3λ/(2a): two thirds of the slit cancel "
  "pairwise, and the remaining third contributes. Statement II is false: the angles θ ≈ (n + ½)λ/a decrease when a "
  "increases, so the maxima move closer to the centre.",
  ["I: three-part argument → true", "II: θ ∝ 1/a → wider slit, maxima closer → false"],
  why="Statement II has the dependence on slit width reversed.",
  ncert=WO + "diffraction (the single slit)", seconds=50)


# ================================================================ Dual Nature of Matter and Radiation (B2 I3 A2)
DC = NC + "'Dual Nature of Radiation and Matter', "

n_pe = 3.2e-6 / 1.6e-19
close(n_pe, 2.0e13)
close(3.2e-6 * 1.6e-19, 5.1e-25, 1e-2)
q(DUAL, "Photoelectric effect", "Basic", "numerical",
  "In a photoelectric experiment, the saturation photocurrent is 3.2 µA. Taking e = 1.6 × 10⁻¹⁹ C, the number of "
  "photoelectrons reaching the collector per second is:",
  *opt("2.0 × 10¹³", ["2.0 × 10¹⁹", "5.1 × 10⁻²⁵", "2.0 × 10¹⁰"], "A"),
  "Current = charge per second = (number of electrons per second) × e",
  "At saturation all the emitted photoelectrons reach the collector, and each carries charge e.",
  ["n = I/e = 3.2 × 10⁻⁶/(1.6 × 10⁻¹⁹) = 2.0 × 10¹³ per second"],
  why="2.0 × 10¹⁹ ignores the micro prefix. 5.1 × 10⁻²⁵ multiplies the current by e instead of "
      "dividing. 2.0 × 10¹⁰ reads µA as nA.",
  ncert=DC + "experimental study of photoelectric effect", seconds=25, rc=True)

q(DUAL, "Einstein's equation", "Basic", "direct",
  "Planck's constant h appears in Einstein's photoelectric equation K_max = hν − φ₀. The SI unit of h, J s, is the "
  "same as the SI unit of:",
  *opt("angular momentum", ["linear momentum", "power", "energy"], "B"),
  "Units of Planck's constant from E = hν",
  "h = E/ν has unit J/s⁻¹ = J s = kg m² s⁻¹. Angular momentum mvr also has unit kg m s⁻¹ × m = kg m² s⁻¹.",
  ["[h] = J s = kg m² s⁻¹", "[L] = kg m² s⁻¹ → same"],
  why="Linear momentum has unit kg m s⁻¹. Power is J s⁻¹, not J s. Energy is J.",
  ncert=DC + "Einstein's photoelectric equation: energy quantum of radiation", seconds=25)

lam_x = 1240 / 12400
V_e = (1.227 / lam_x) ** 2
close(lam_x, 0.1)
close(V_e, 150.6, 1e-3)
close(1.227 / lam_x, 12.27, 1e-3)
close((1.227 / 1.0) ** 2, 1.51, 3e-3)
q(DUAL, "de Broglie wavelength", "Intermediate", "numerical",
  "An electron, starting from rest, is accelerated through a potential difference V so that its de Broglie "
  "wavelength equals the wavelength of an X-ray photon of energy 12.4 keV. Taking hc = 1240 eV nm and, for an "
  "electron accelerated from rest through V volts, λ = 1.227/√V nm, the value of V is about:",
  *opt("151 V", ["12.3 V", "12.4 kV", "1.51 V"], "C"),
  "Photon: λ = hc/E; electron: λ = 1.227/√V nm",
  "First find the photon's wavelength, then the accelerating voltage that gives the electron the same wavelength.",
  ["λ_photon = 1240/12 400 = 0.100 nm", "√V = 1.227/0.100 = 12.27", "V = 12.27² ≈ 151 V"],
  why="12.3 V forgets to square 1.227/λ. 12.4 kV assumes the electron must have the same energy as the photon; "
      "equal wavelengths do not mean equal energies. 1.51 V takes the wavelength as 1.0 nm.",
  ncert=DC + "wave nature of matter", seconds=70, rc=True)

q(DUAL, "Photoelectric effect", "Intermediate", "assertion_reason",
  ar("Light of a certain intensity in the red part of the spectrum fails to eject photoelectrons from a given metal, "
     "but violet light of the same intensity may eject them.",
     "Photons of violet light carry less energy than photons of red light."),
  AR, ar_key(True, False),
  "Threshold frequency: emission depends on the energy hν of each photon, not on intensity",
  "Violet light has a higher frequency than red light, so each violet photon carries more energy (E = hν). If the "
  "red photon energy is below the work function and the violet photon energy is above it, only violet light ejects "
  "electrons, whatever the intensity. A is true; R has the comparison reversed and is false.",
  ["ν_violet > ν_red → E_violet > E_red", "A true (threshold depends on frequency)", "R false"],
  why="R is false, so the options calling both statements true cannot be right; A is a correct statement.",
  ncert=DC + "photoelectric effect and wave theory of light; Einstein's photoelectric equation", seconds=40)

E_ph = 1240 / 248
K_m = E_ph - 3.0
lam0 = 1240 / 3.0
close(E_ph, 5.0)
close(K_m, 2.0)
close(lam0, 413, 1e-3)
truth = {"a": True, "b": True, "c": True, "d": False, "e": True}
q(DUAL, "Einstein's equation", "Intermediate", "multi_statement",
  ms("Monochromatic light of wavelength 248 nm falls on a metal surface of work function 3.0 eV. Taking "
     "hc = 1240 eV nm, which of the following statements are correct?",
     ["The maximum kinetic energy of the photoelectrons is 2.0 eV.",
      "The stopping potential is 2.0 V.",
      "The threshold wavelength of the metal is about 413 nm.",
      "Doubling the intensity of the light doubles the stopping potential.",
      "Some photoelectrons are emitted with kinetic energies smaller than 2.0 eV."]),
  *mso(truth, "abce", ["abc", "abde", "bce"], "D"),
  "Einstein's equation K_max = hν − φ₀ = eV₀",
  "Each photon carries 1240/248 = 5.0 eV. The fastest electrons leave with 5.0 − 3.0 = 2.0 eV, so V₀ = 2.0 V. The "
  "threshold wavelength is hc/φ₀ = 413 nm. The stopping potential depends on frequency, not intensity. Electrons "
  "from below the surface lose some energy on the way out, so a spread of energies up to K_max is emitted.",
  ["(a) 5.0 − 3.0 = 2.0 eV → true", "(b) V₀ = K_max/e = 2.0 V → true", "(c) 1240/3.0 ≈ 413 nm → true",
   "(d) V₀ independent of intensity → false", "(e) energies range from 0 to K_max → true"],
  why="Only (d) is false. The codes that include (d), or leave out (a) or (e), are wrong.",
  ncert=DC + "experimental study of photoelectric effect; Einstein's photoelectric equation", seconds=80, rc=True)

nu_min = (2.5 + 2.0) / 4.14e-15
close(nu_min, 1.09e15, 3e-3)
close(2.5 / 4.14e-15, 6.0e14, 1e-2)
close(0.5 / 4.14e-15, 1.2e14, 1e-2)
close(2.0 / 4.14e-15, 4.8e14, 1e-2)
q(DUAL, "Einstein's equation", "Advanced", "numerical",
  "The emitter of a photocell has a work function of 2.5 eV. The collector is held at a potential of −2.0 V "
  "relative to the emitter. Taking h = 4.14 × 10⁻¹⁵ eV s, the minimum frequency of the incident light for which "
  "any photoelectrons can reach the collector is about:",
  *opt("1.09 × 10¹⁵ Hz", ["6.0 × 10¹⁴ Hz", "1.2 × 10¹⁴ Hz", "4.8 × 10¹⁴ Hz"], "D"),
  "Einstein's equation with a retarding potential: an electron reaches the collector only if K_max ≥ eV",
  "The fastest photoelectrons must have at least 2.0 eV of kinetic energy to climb the 2.0 V retarding potential. "
  "So each photon must supply the work function plus 2.0 eV.",
  ["hν_min = φ₀ + eV = 2.5 + 2.0 = 4.5 eV", "ν_min = 4.5/(4.14 × 10⁻¹⁵) ≈ 1.09 × 10¹⁵ Hz"],
  why="6.0 × 10¹⁴ Hz is the threshold frequency of the emitter; electrons emitted at that frequency have no energy "
      "left to overcome the retarding potential. 1.2 × 10¹⁴ Hz subtracts the 2.0 eV instead of adding it. "
      "4.8 × 10¹⁴ Hz uses only the 2.0 eV and ignores the work function.",
  ncert=DC + "experimental study of photoelectric effect (effect of potential); Einstein's photoelectric equation",
  seconds=90, rc=True)

assert F(-1, 2) * F(-1, 100) == F(1, 200) * 1
q(DUAL, "de Broglie wavelength", "Advanced", "numerical",
  "The kinetic energy of a non-relativistic particle is increased slightly, and its de Broglie wavelength is found "
  "to decrease by 0.50%. The percentage increase in its kinetic energy is about:",
  *opt("1.0%", ["0.50%", "0.25%", "2.0%"], "B"),
  "λ = h/√(2mK), so λ ∝ K^(−1/2) and, for small changes, Δλ/λ = −½ ΔK/K",
  "Taking logarithms and differentiating, the fractional change of λ is minus one half the fractional change of K.",
  ["Δλ/λ = −½ (ΔK/K)", "−0.50% = −½ (ΔK/K) → ΔK/K = +1.0%"],
  why="0.50% assumes λ ∝ 1/K. 0.25% halves instead of doubling. 2.0% uses λ ∝ K^(−1/4).",
  ncert=DC + "wave nature of matter", seconds=70, rc=True)


# ================================================================ Atoms and Nuclei (B3 I5 A3)
AT = NC + "'Atoms', "
NU = NC + "'Nuclei', "

lam_La = 1240 / 10.2
close(lam_La, 121.6, 1e-3)
q(AN, "Bohr model and hydrogen spectrum", "Basic", "numerical",
  "A hydrogen atom emits a photon of energy 10.2 eV. Taking hc = 1240 eV nm, the wavelength of this photon and the "
  "region of the spectrum in which it lies are:",
  *opt("about 122 nm, in the ultraviolet", ["about 122 nm, in the visible region", "about 656 nm, in the visible region",
                                          "about 12.2 nm, in the X-ray region"], "A"),
  "λ = hc/E; the visible region is about 400–700 nm",
  "λ = 1240/10.2 nm. This is the first line of the Lyman series (n = 2 → n = 1), which lies in the ultraviolet.",
  ["λ = 1240/10.2 ≈ 122 nm", "122 nm < 400 nm → ultraviolet"],
  why="122 nm is well below the visible range. 656 nm is the first Balmer line (1.89 eV). 12.2 nm misplaces the "
      "decimal point.",
  ncert=AT + "line spectra of the hydrogen atom", seconds=30, rc=True)

q(AN, "Fission and fusion", "Basic", "direct",
  "Fusion of light nuclei, such as the fusion of hydrogen nuclei in the Sun, needs an extremely high temperature "
  "(of the order of 10⁷ K or more) mainly because:",
  *opt("the nuclei must have enough kinetic energy to overcome their mutual Coulomb repulsion and come within the "
       "range of the nuclear force",
       ["the nuclear force between light nuclei is repulsive at ordinary temperatures",
        "the binding energy per nucleon of the product is smaller than that of the reacting nuclei",
        "neutrons must first be produced by the heat to start a chain reaction"], "C"),
  "Thermonuclear fusion",
  "All nuclei are positively charged and repel each other. To fuse, they must approach within a few femtometres, "
  "where the short-range attractive nuclear force acts. Only at very high temperatures do enough nuclei have the "
  "kinetic energy to overcome the Coulomb barrier; hence the name thermonuclear fusion.",
  ["Coulomb barrier between positive nuclei", "High temperature → high kinetic energies → nuclei get close enough"],
  why="The nuclear force is attractive at the relevant distances; it is the Coulomb force that opposes fusion. In "
      "energy-releasing fusion the product has a larger binding energy per nucleon. Fusion is not a neutron-driven "
      "chain reaction.",
  ncert=NU + "nuclear energy (nuclear fusion - energy generation in stars)", seconds=40)

q(AN, "Nuclear size and mass defect", "Basic", "statement_pair",
  sp("The mass of a neutron is slightly larger than the mass of a proton.",
     "The nucleus of the ordinary hydrogen atom, ¹₁H, contains no neutron."),
  SP, sp_key(True, True),
  "Composition of nuclei; masses of the proton and neutron",
  "Statement I is true: NCERT gives m_n = 1.00866 u and m_p = 1.00727 u. Statement II is true: ¹₁H has A = 1 and "
  "Z = 1, so its nucleus is a single proton and N = A − Z = 0.",
  ["I: 1.00866 u > 1.00727 u → true", "II: N = 1 − 1 = 0 → true"],
  why="Both statements are correct, so the options calling either false are wrong.",
  ncert=NU + "atomic masses and composition of nucleus", seconds=30)

E_Li = 13.6 * 9 * (1 - F(1, 4))
close(float(E_Li), 91.8)
close(13.6 * 3 * 0.75, 30.6)
close(13.6 * 9, 122.4)
q(AN, "Bohr model and hydrogen spectrum", "Intermediate", "numerical",
  "In the Bohr model the energy levels of a hydrogen-like ion of atomic number Z are E_n = −13.6 Z²/n² eV. The "
  "energy of the photon emitted when a doubly ionised lithium ion (Li²⁺, Z = 3) makes the transition n = 2 → n = 1 "
  "is:",
  *opt("91.8 eV", ["10.2 eV", "30.6 eV", "122.4 eV"], "D"),
  "Bohr energy levels of hydrogen-like ions scale as Z²",
  "The photon energy is E₂ − E₁ = 13.6 Z²(1 − 1/4) eV, which for Z = 3 is nine times the hydrogen value of 10.2 eV.",
  ["E₂ − E₁ = 13.6 × 9 × (1 − 1/4)", "= 122.4 × 0.75 = 91.8 eV"],
  why="10.2 eV is the hydrogen value (Z = 1). 30.6 eV scales by Z instead of Z². 122.4 eV is the ionisation energy "
      "of Li²⁺ from its ground state, not the 2 → 1 photon energy.",
  ncert=AT + "Bohr model of the hydrogen atom (energy levels)", seconds=45, rc=True)

dm_he = 2 * 1.007825 + 2 * 1.008665 - 4.002603
BE_he = dm_he * 931.5
close(BE_he, 28.3, 1e-3)
close(BE_he / 4, 7.07, 1e-3)
close((2 * 1.007276 + 2 * 1.008665 - 4.002603) * 931.5 / 4, 6.82, 1e-3)
close(BE_he / 2, 14.1, 5e-3)
q(AN, "Binding energy", "Intermediate", "numerical",
  "Given the atomic masses m(¹H) = 1.007825 u and m(⁴He) = 4.002603 u, the neutron mass 1.008665 u and "
  "1 u = 931.5 MeV/c², the binding energy per nucleon of the ⁴He nucleus is about:",
  *opt("7.07 MeV", ["28.3 MeV", "14.1 MeV", "6.82 MeV"], "B"),
  "Mass defect Δm = [Zm(¹H) + Nm_n] − m(atom); E_b = Δm c²",
  "Using atomic masses for both ¹H and ⁴He makes the electron masses cancel. ⁴He has 2 protons and 2 neutrons.",
  ["Δm = 2(1.007825) + 2(1.008665) − 4.002603 = 0.030377 u", "E_b = 0.030377 × 931.5 ≈ 28.3 MeV",
   "E_b/A = 28.3/4 ≈ 7.07 MeV"],
  why="28.3 MeV is the total binding energy, not the value per nucleon. 14.1 MeV divides by the number of protons "
      "only. 6.82 MeV uses the bare proton mass (1.007276 u) with the atomic mass of helium, so the two electron "
      "masses are not balanced.",
  ncert=NU + "mass-energy and nuclear binding energy", seconds=90, rc=True)

n_r = math.sqrt(2.12 / 0.53)
close(n_r, 2.0)
close(-13.6 / n_r ** 2, -3.4)
q(AN, "Bohr model and hydrogen spectrum", "Intermediate", "numerical",
  "In the Bohr model of the hydrogen atom, the radius of the nth orbit is 0.53 n² Å and the energy is −13.6/n² eV. "
  "An electron moving in an orbit of radius 2.12 Å has a total energy of:",
  *opt("−3.4 eV", ["−0.85 eV", "−1.51 eV", "−6.8 eV"], "C"),
  "r_n ∝ n² and E_n ∝ −1/n²",
  "First find n from the radius, then the energy.",
  ["n² = 2.12/0.53 = 4 → n = 2", "E₂ = −13.6/4 = −3.4 eV"],
  why="−0.85 eV takes n = 4 (the ratio of radii) instead of n² = 4. −1.51 eV is the energy for n = 3. −6.8 eV is "
      "the potential energy in the n = 2 orbit, twice the total energy.",
  ncert=AT + "Bohr model of the hydrogen atom", seconds=45, rc=True)

q(AN, "Rutherford scattering", "Intermediate", "assertion_reason",
  ar("In analysing the alpha-particle scattering experiment, the gold nucleus can be treated as remaining "
     "stationary throughout the collision.",
     "A gold nucleus is about 50 times heavier than an alpha particle."),
  AR, ar_key(True, True, True),
  "Alpha-particle trajectory: heavy target nucleus",
  "NCERT notes that since the gold nucleus is about 50 times heavier than an alpha particle, it is reasonable to "
  "assume that it remains stationary during the scattering. R gives exactly the reason that justifies A.",
  ["m(Au)/m(α) ≈ 197/4 ≈ 50", "A much heavier target barely recoils → treated as stationary", "R explains A"],
  why="Both are true and the large mass ratio is the reason the recoil of the nucleus can be neglected.",
  ncert=AT + "alpha-particle scattering and Rutherford's nuclear model of atom", seconds=40)

q(AN, "Bohr model and hydrogen spectrum", "Intermediate", "match_list",
  ml("For the electron of a hydrogen atom in the n = 2 orbit of the Bohr model (E_n = −13.6/n² eV), match each "
     "quantity in List-I with its value in List-II.",
     ["Total energy", "Kinetic energy", "Potential energy", "Orbital angular momentum"],
     ["h/π", "−6.8 eV", "+3.4 eV", "−3.4 eV"]),
  *mlo("A-IV, B-III, C-II, D-I", ["A-III, B-IV, C-II, D-I", "A-IV, B-II, C-III, D-I", "A-II, B-III, C-IV, D-I"],
       "D"),
  "Bohr model: K = −E, U = 2E, L = nh/2π",
  "E₂ = −13.6/4 = −3.4 eV. For an inverse-square attraction the kinetic energy is −E = +3.4 eV and the potential "
  "energy is 2E = −6.8 eV. The angular momentum is nh/(2π) = 2h/(2π) = h/π.",
  ["E = −3.4 eV (IV)", "K = +3.4 eV (III)", "U = −6.8 eV (II)", "L = h/π (I)"],
  why="A-III, B-IV interchanges total and kinetic energy (signs swapped). B-II, C-III gives a negative kinetic "
      "energy. A-II, C-IV interchanges total and potential energy.",
  ncert=AT + "Bohr model of the hydrogen atom", seconds=55)

# de Broglie wavelength in nth orbit: lambda_n = 2 pi r_n / n, proportional to n
n_db = 4
assert (0.53 * n_db ** 2 * 2 * math.pi / n_db) / (0.53 * 2 * math.pi) == 4
close(-13.6 / n_db ** 2, -0.85)
q(AN, "Bohr model and hydrogen spectrum", "Advanced", "numerical",
  "In the Bohr model of the hydrogen atom (r_n ∝ n², E_n = −13.6/n² eV), the de Broglie wavelength of the electron "
  "in a certain orbit is four times its value in the ground-state orbit. The total energy of the electron in this "
  "orbit is:",
  *opt("−0.85 eV", ["−3.4 eV", "+0.85 eV", "−13.6 eV"], "B"),
  "de Broglie's interpretation of Bohr's condition: 2πr_n = nλ_n",
  "λ_n = 2πr_n/n. Since r_n ∝ n², λ_n ∝ n (equivalently, λ = h/mv with v ∝ 1/n). A wavelength four times the "
  "ground-state value means n = 4.",
  ["λ_n = 2πr_n/n ∝ n²/n = n", "λ_n = 4λ₁ → n = 4", "E₄ = −13.6/16 = −0.85 eV"],
  why="−3.4 eV takes λ ∝ n², giving n = 2. +0.85 eV has the wrong sign; a bound electron has negative total "
      "energy. −13.6 eV is the ground-state energy, as if λ did not depend on n.",
  ncert=AT + "de Broglie's explanation of Bohr's second postulate of quantisation", seconds=80, rc=True)

K_light = 170 * F(140, 236)
close(float(K_light), 100.8, 1e-3)
close(float(170 * F(96, 236)), 69.2, 1e-3)
close(float(170 * F(96, 140)), 116.6, 1e-3)
q(AN, "Fission and fusion", "Advanced", "numerical",
  "A nucleus of mass number 236, at rest, splits into two fragments of mass numbers 140 and 96 (no neutrons are "
  "emitted in this simplified case). The fragments share a total kinetic energy of 170 MeV. Taking the masses of "
  "the fragments as proportional to their mass numbers, the kinetic energy of the lighter fragment is about:",
  *opt("101 MeV", ["69 MeV", "85 MeV", "117 MeV"], "D"),
  "Conservation of momentum in a two-body break-up: equal and opposite momenta, K = p²/2m ∝ 1/m",
  "The fragments fly apart with equal and opposite momenta, so their kinetic energies are in the inverse ratio of "
  "their masses. The lighter fragment takes the larger share.",
  ["K_light/K_heavy = 140/96", "K_light = 170 × 140/236 ≈ 101 MeV", "K_heavy = 170 × 96/236 ≈ 69 MeV"],
  why="69 MeV is the share of the heavier fragment. 85 MeV divides the energy equally. 117 MeV multiplies 170 MeV by "
      "the mass ratio 96/140 instead of by the fraction 140/236.",
  ncert=NU + "nuclear energy (nuclear fission)", seconds=90, rc=True)

truth = {"a": True, "b": True, "c": True, "d": False, "e": False}
q(AN, "Binding energy", "Advanced", "multi_statement",
  ms("Which of the following statements about the nuclear force, as described in NCERT, are correct?",
     ["It is much stronger than the Coulomb force acting between charges, so it can overcome the repulsion "
      "between protons inside a nucleus.",
      "It falls rapidly to zero as the distance between two nucleons becomes more than a few femtometres.",
      "The nuclear force between neutron and neutron, proton and neutron, and proton and proton is approximately "
      "the same.",
      "It is attractive at all separations, however small.",
      "It acts between electrons and nucleons, binding the electrons to the nucleus."]),
  *mso(truth, "abc", ["ab", "abd", "bce"], "C"),
  "Properties of the nuclear force",
  "NCERT lists: the nuclear force is much stronger than the Coulomb force; it is short-ranged, falling rapidly to "
  "zero beyond a few femtometres (which leads to saturation); it is nearly the same for n–n, n–p and p–p; and it is "
  "attractive for separations above about 0.8 fm but becomes strongly repulsive at smaller separations. Electrons "
  "are bound to the nucleus by the electrostatic force.",
  ["(a) much stronger than Coulomb → true", "(b) short range → true", "(c) charge independent → true",
   "(d) repulsive below about 0.8 fm → false", "(e) electrons are held by electrostatic attraction → false"],
  why="(d) misses the strong repulsion at very short distances, and (e) wrongly brings electrons into the nuclear "
      "force. Codes with (d) or (e), or missing (c), are wrong.",
  ncert=NU + "nuclear force", seconds=60)


# ================================================================ Electronic Devices (B5 I6 A5)
SD = NC + "'Semiconductor Electronics: Materials, Devices and Simple Circuits', "
LOGIC = "NMC syllabus, Electronic Devices: logic gates (OR, AND, NOT, NAND and NOR)"

# ---- Basic
P_sc = 0.02 * 0.02 * 1000 * 0.15
close(P_sc, 0.060)
close(0.02 * 0.02 * 1000, 0.40)
close(0.2 * 0.2 * 1000 * 0.15 / 10, 0.60)
q(ED, "LED, photodiode and solar cell", "Basic", "numerical",
  "A solar cell measuring 2.0 cm × 2.0 cm receives sunlight of intensity 1000 W m⁻² falling normally on it, and "
  "converts 15% of the incident light energy into electrical energy. The electrical power it delivers is:",
  *opt("60 mW", ["400 mW", "6.0 mW", "600 mW"], "A"),
  "Incident power = intensity × area; electrical output = efficiency × incident power",
  "The area is 4.0 cm² = 4.0 × 10⁻⁴ m², so the incident power is 0.40 W, of which 15% is converted.",
  ["Area = 0.020 × 0.020 = 4.0 × 10⁻⁴ m²", "Incident power = 1000 × 4.0 × 10⁻⁴ = 0.40 W",
   "Output = 0.15 × 0.40 = 0.060 W = 60 mW"],
  why="400 mW is the incident power, without the 15% efficiency. 6.0 mW and 600 mW convert 4.0 cm² to m² wrongly "
      "(by a factor of 10 either way).",
  ncert=SD + "solar cell", seconds=35, rc=True)

ni_ge = 2.4e19
close(2 * ni_ge, 4.8e19)
q(ED, "Semiconductors", "Basic", "numerical",
  "In a sample of pure (intrinsic) germanium at a certain temperature, the intrinsic carrier concentration is "
  "2.4 × 10¹⁹ m⁻³. The total number of mobile charge carriers (free electrons and holes together) per cubic metre "
  "is:",
  *opt("4.8 × 10¹⁹", ["2.4 × 10¹⁹", "1.2 × 10¹⁹", "5.8 × 10³⁸"], "B"),
  "Intrinsic semiconductor: n_e = n_h = n_i",
  "Each broken covalent bond releases one free electron and leaves one hole, so in a pure semiconductor the "
  "electron and hole concentrations are both equal to n_i.",
  ["n_e = n_h = 2.4 × 10¹⁹ m⁻³", "Total = 2 × 2.4 × 10¹⁹ = 4.8 × 10¹⁹ m⁻³"],
  why="2.4 × 10¹⁹ counts only the electrons (or only the holes). 1.2 × 10¹⁹ splits n_i between the two kinds of "
      "carrier. 5.8 × 10³⁸ is n_i², the product n_e n_h, not a number of carriers.",
  ncert=SD + "intrinsic semiconductor", seconds=30, rc=True)

q(ED, "Semiconductors", "Basic", "direct",
  "Silicon is doped with boron, a trivalent impurity. After a boron atom has accepted an electron from a "
  "neighbouring silicon atom to complete its fourth covalent bond, the boron atom in the crystal becomes:",
  *opt("an immobile negative ion", ["a mobile negative charge carrier", "an immobile positive ion",
                                    "a neutral atom that takes no further part"], "D"),
  "Acceptor impurities in a p-type semiconductor",
  "The boron atom has only three valence electrons. When it takes an electron from a neighbouring bond to complete "
  "its fourth bond, it acquires one extra electron and becomes a negative ion, fixed in the crystal lattice. The "
  "hole left behind in the neighbouring bond is the mobile carrier.",
  ["B has 3 valence electrons", "Accepts one electron → net charge −e", "Ion is fixed in the lattice (immobile)"],
  why="The ion is part of the lattice and cannot move; the mobile carrier is the hole. A positive ion is what a "
      "donor (pentavalent) atom becomes. The accepted electron leaves the atom charged, not neutral.",
  ncert=SD + "extrinsic semiconductor (p-type semiconductor)", seconds=35)

q(ED, "p-n junction diode and rectifier", "Basic", "match_list",
  ml("Match each part of a simple rectifier power supply working from the AC mains (List-I) with its function "
     "(List-II).",
     ["Step-down transformer", "Junction diode", "Capacitor connected across the load", "Load resistor"],
     ["The output voltage is taken across it", "Lowers the AC mains voltage to the required value",
      "Allows current to flow in one direction only", "Smooths the pulsating output by reducing the ripple"]),
  *mlo("A-II, B-III, C-IV, D-I", ["A-III, B-II, C-IV, D-I", "A-II, B-III, C-I, D-IV", "A-II, B-IV, C-III, D-I"],
       "C"),
  "Junction diode as a rectifier, with a capacitor filter",
  "The transformer supplies the required (lower) AC voltage. The diode conducts only when forward biased, so the "
  "current through the load is unidirectional. A capacitor across the load charges to the peak and discharges "
  "slowly between peaks, reducing the ripple. The rectified output is taken across the load resistor.",
  ["Transformer → II", "Diode → III", "Capacitor filter → IV", "Load resistor → I"],
  why="A-III, B-II interchanges the transformer and the diode. C-I, D-IV interchanges the capacitor and the load. "
      "B-IV, C-III interchanges the diode and the capacitor.",
  ncert=SD + "application of junction diode as a rectifier", seconds=45)

truth = {"a": True, "b": True, "c": True, "d": False, "e": False}
q(ED, "LED, photodiode and solar cell", "Basic", "multi_statement",
  ms("Which of the following statements about solar cells, as described in NCERT, are correct?",
     ["Si, GaAs, CdTe and CuInSe₂ are among the materials used to make solar cells.",
      "Solar cells are used to power electronic devices in satellites and space vehicles.",
      "Solar cells are also used as the power supply in some calculators.",
      "A solar cell converts electrical energy into light energy.",
      "A solar cell has to be connected to an external battery in reverse bias to work."]),
  *mso(truth, "abc", ["ab", "abd", "bce"], "A"),
  "Solar cell: a p-n junction that generates an emf when light falls on it",
  "NCERT lists Si (Eg ≈ 1.1 eV), GaAs (≈ 1.43 eV), CdTe (≈ 1.45 eV) and CuInSe₂ (≈ 1.04 eV) as commonly used "
  "materials, and mentions their use in satellites, space vehicles and some calculators. A solar cell converts "
  "light into electrical energy, without any external bias.",
  ["(a), (b), (c) → NCERT statements → true", "(d) it is the reverse (light → electricity) → false",
   "(e) no external bias is applied → false"],
  why="(d) describes an LED, not a solar cell, and (e) contradicts the working of a solar cell, which itself "
      "supplies power.",
  ncert=SD + "solar cell", seconds=45)

# ---- Intermediate
R_static = 0.70 / 10e-3
r_dyn = (0.72 - 0.70) / (15e-3 - 10e-3)
close(R_static, 70)
close(r_dyn, 4.0)
close(0.72 / 15e-3, 48)
close(0.70 / 15e-3, 46.7, 1e-3)
q(ED, "p-n junction diode and rectifier", "Intermediate", "numerical",
  "On the forward characteristic of a junction diode, the current is 10 mA at a forward voltage of 0.70 V and "
  "15 mA at 0.72 V. The static (d.c.) resistance V/I of the diode at 0.70 V, and its dynamic resistance in this "
  "region, are respectively:",
  *opt("70 Ω and 4.0 Ω", ["4.0 Ω and 70 Ω", "70 Ω and 48 Ω", "47 Ω and 4.0 Ω"], "B"),
  "Static resistance V/I at a point; dynamic resistance ΔV/ΔI over a small range",
  "The static resistance uses the values at one point of the characteristic. The dynamic resistance uses the "
  "small changes between the two points; because the forward characteristic is steep, it is much smaller.",
  ["Static: 0.70/0.010 = 70 Ω", "Dynamic: (0.72 − 0.70)/(0.015 − 0.010) = 0.02/0.005 = 4.0 Ω"],
  why="4.0 Ω and 70 Ω interchanges the two. 48 Ω is the static resistance at 0.72 V, not the dynamic resistance. "
      "47 Ω divides 0.70 V by the wrong current (15 mA).",
  ncert=SD + "semiconductor diode (V-I characteristics; dynamic resistance)", seconds=50, rc=True)

V_load_pk = 10 * 980 / (980 + 20)
close(V_load_pk, 9.8)
close(10 * 20 / 1000, 0.2)
q(ED, "p-n junction diode and rectifier", "Intermediate", "numerical",
  "A half-wave rectifier consists of a single junction diode in series with a 980 Ω load resistor, connected to an "
  "AC source of peak voltage 10 V and negligible internal resistance. Model the diode as having a constant forward "
  "resistance of 20 Ω (and no threshold voltage) and an infinite reverse resistance. The peak voltage across the "
  "load is:",
  *opt("9.8 V", ["10 V", "0.20 V", "9.3 V"], "D"),
  "In forward bias the diode's resistance is in series with the load, forming a potential divider",
  "During the conducting half-cycle the peak current is 10 V/(980 + 20) Ω = 10 mA, and the load takes its share "
  "of the voltage.",
  ["I_peak = 10/1000 = 10 mA", "V_load,peak = 10 mA × 980 Ω = 9.8 V"],
  why="10 V ignores the forward resistance of the diode. 0.20 V is the peak drop across the diode itself. 9.3 V "
      "subtracts a 0.7 V threshold, which this model of the diode does not include.",
  ncert=SD + "application of junction diode as a rectifier", seconds=50, rc=True)


def g_and(a, b): return a & b
def g_or(a, b): return a | b
def g_not(a): return 1 - a
def g_nand(a, b): return 1 - (a & b)
def g_nor(a, b): return 1 - (a | b)


INPUTS = [(0, 0), (0, 1), (1, 0), (1, 1)]
assert [g_or(g_and(a, b), g_and(a, g_not(b))) for a, b in INPUTS] == [a for a, b in INPUTS]
q(ED, "Logic gates", "Intermediate", "direct",
  "Inputs A and B are fed to an AND gate. Input A and the output of a NOT gate (whose input is B) are fed to a second "
  "AND gate. The outputs of the two AND gates are fed to an OR gate, whose output is Y. Then:",
  *opt("Y = A, whatever the value of B", ["Y = B, whatever the value of A", "Y = A + B (an OR gate)",
                                         "Y = 1 for every combination of inputs"], "A"),
  "Truth table of a combination of gates",
  "Y = A·B + A·B̄. When A = 0 both AND outputs are 0, so Y = 0. When A = 1 exactly one of B and B̄ is 1, so one AND "
  "output is 1 and Y = 1. Hence Y always equals A.",
  ["(0,0) → 0 + 0 = 0", "(0,1) → 0 + 0 = 0", "(1,0) → 0 + 1 = 1", "(1,1) → 1 + 0 = 1", "Y = 0, 0, 1, 1 = A"],
  why="Y = B fails for (1, 0), where Y = 1. An OR gate would give 1 for (0, 1), but here Y = 0. Y is 0 whenever "
      "A = 0, so it is not always 1.",
  ncert=LOGIC, seconds=50)

q(ED, "Semiconductors", "Intermediate", "assertion_reason",
  ar("When a p-n junction is forward biased, the concentration of electrons on the p-side near the junction "
     "becomes much larger than in the unbiased junction.",
     "When a p-n junction is forward biased, the height of the potential barrier increases."),
  AR, ar_key(True, False),
  "Forward bias: lowered barrier and minority carrier injection",
  "In forward bias the applied voltage opposes the built-in potential, so the effective barrier is lowered. "
  "Electrons from the n-side then cross into the p-side, where they are minority carriers; this minority carrier "
  "injection greatly raises the electron concentration on the p-side near the junction. A is true. R is false: "
  "the barrier height decreases in forward bias and increases in reverse bias.",
  ["A: minority carrier injection under forward bias → true", "R: barrier decreases, not increases → false"],
  why="R states the reverse-bias behaviour; under forward bias the barrier is lowered.",
  ncert=SD + "semiconductor diode (p-n junction diode under forward bias)", seconds=45)

q(ED, "p-n junction diode and rectifier", "Intermediate", "statement_pair",
  sp("An ideal diode offers zero resistance when forward biased and infinite resistance when reverse biased.",
     "In a half-wave rectifier, current flows through the load during the half-cycle in which the diode is reverse "
     "biased."),
  SP, sp_key(True, False),
  "Ideal diode; working of a half-wave rectifier",
  "Statement I is the definition of an ideal diode. Statement II is false: the diode conducts, and the load "
  "carries current, during the half-cycle in which the diode is forward biased; in the other half-cycle the diode "
  "is reverse biased and the current is (nearly) zero.",
  ["I: ideal diode → true", "II: conduction occurs in forward bias → false"],
  why="Statement II interchanges the conducting and non-conducting half-cycles.",
  ncert=SD + "application of junction diode as a rectifier", seconds=35)

truth = {"a": True, "b": True, "c": True, "d": False, "e": False}
q(ED, "p-n junction diode and rectifier", "Intermediate", "multi_statement",
  ms("A capacitor is connected across the load resistor of a half-wave rectifier working from 50 Hz AC mains. Which "
     "of the following statements are correct?",
     ["The capacitor charges up to (nearly) the peak value of the rectified voltage.",
      "When the rectified voltage falls below the capacitor voltage, the capacitor discharges through the load.",
      "If the load draws only a small current (large load resistance), the output voltage stays close to the peak "
      "value.",
      "With the capacitor connected, the output is a perfectly steady DC voltage with no ripple at all.",
      "The fundamental frequency of the ripple in the output is 100 Hz."]),
  *mso(truth, "abc", ["ab", "abd", "ace"], "B"),
  "Capacitor filter for a rectifier",
  "On the rising part of each half-cycle the diode conducts and charges the capacitor to the peak voltage. When the "
  "input falls, the diode is reverse biased and the capacitor discharges through the load, so the output falls "
  "only slowly. A large load resistance (small current) keeps the fall small, so the output stays near the peak. "
  "Some ripple always remains. A half-wave rectifier gives one output pulse per input cycle, so the ripple "
  "frequency is 50 Hz.",
  ["(a) charges to peak → true", "(b) discharges through the load between peaks → true",
   "(c) small load current → output close to peak → true", "(d) some ripple remains → false",
   "(e) half-wave ripple is at 50 Hz → false"],
  why="(d) overstates the filter's effect, and (e) gives the full-wave ripple frequency. Codes containing either are "
      "wrong, as is the code without (c).",
  ncert=SD + "application of junction diode as a rectifier (filter)", seconds=60)

# ---- Advanced
theta_on = deg(math.asin(0.7 / 1.4))
frac = (180 - 2 * theta_on) / 360
close(theta_on, 30)
close(frac, 1 / 3)
q(ED, "p-n junction diode and rectifier", "Advanced", "numerical",
  "A half-wave rectifier uses a silicon diode in series with a load resistor. Treat the diode as non-conducting "
  "below a forward voltage of 0.70 V and as having a constant drop of 0.70 V when it conducts. The AC input is "
  "sinusoidal with a peak value of 1.4 V. The fraction of each complete cycle during which current flows through "
  "the load is:",
  *opt("1/3", ["1/2", "1/6", "2/3"], "D"),
  "A diode with a threshold conducts only while the input exceeds the threshold voltage",
  "Current flows only while 1.4 sin ωt > 0.70, i.e. sin ωt > 0.5, which holds from ωt = 30° to 150° in the positive "
  "half-cycle: 120° out of 360°.",
  ["sin ωt > 0.70/1.4 = 0.5", "Conduction from 30° to 150° → 120°", "Fraction = 120°/360° = 1/3"],
  why="1/2 is the fraction for an ideal diode (no threshold). 1/6 takes the conduction as 60°. 2/3 compares 120° "
      "with a half-cycle (180°) instead of a full cycle.",
  ncert=SD + "semiconductor diode (V-I characteristics); application of junction diode as a rectifier",
  seconds=100, rc=True)

V_M = (F(9) / 1 + F(7, 10) / 1) / (F(1) + F(1, 2) + F(1))
I_d = (V_M - F(7, 10)) / 1
close(float(I_d), 3.18, 1e-3)
close((9 - 0.7) / 2, 4.15)
V_M0 = F(9) / (F(1) + F(1, 2) + F(1))
close(float(V_M0), 3.6)
q(ED, "p-n junction diode and rectifier", "Advanced", "numerical",
  "A 9.0 V battery of negligible internal resistance is connected through a 1.0 kΩ resistor to a point M. From M, "
  "a 2.0 kΩ resistor goes to the negative terminal of the battery, and a second path, consisting of a forward-biased "
  "silicon diode in series with a 1.0 kΩ resistor, also goes to the negative terminal. Treat the diode as having a "
  "constant drop of 0.70 V when it conducts. The current through the diode is about:",
  *opt("3.2 mA", ["4.2 mA", "3.6 mA", "8.3 mA"], "A"),
  "Kirchhoff's junction rule at M, with the diode replaced by a 0.70 V drop",
  "Let V be the potential of M. The current from the battery, (9.0 − V)/1.0 kΩ, splits between the 2.0 kΩ resistor, "
  "V/2.0 kΩ, and the diode path, (V − 0.70)/1.0 kΩ.",
  ["(9.0 − V)/1 = V/2 + (V − 0.70)/1 (in mA, with V in volts)", "9.7 = 2.5V → V = 3.88 V",
   "I_diode = (3.88 − 0.70)/1.0 ≈ 3.2 mA"],
  why="4.2 mA ignores the 2.0 kΩ branch, sending the whole current through the diode. 3.6 mA treats the diode as "
      "ideal (no 0.70 V drop). 8.3 mA leaves out the 1.0 kΩ series resistor between the battery and M.",
  ncert=SD + "semiconductor diode (forward bias)", seconds=120, rc=True)

circA = [g_nand(g_nand(a, b), a) for a, b in INPUTS]
circB = [g_nor(g_nor(a, b), a) for a, b in INPUTS]
circC = [g_or(a, g_nor(a, b)) for a, b in INPUTS]
circD = [g_nor(g_nand(a, b), b) for a, b in INPUTS]
assert circA == [1, 1, 0, 1] and circB == [0, 1, 0, 0] and circC == [1, 0, 1, 1] and circD == [0, 0, 0, 0]
q(ED, "Logic gates", "Advanced", "match_list",
  ml("Each circuit in List-I has inputs A and B. Match it with its outputs in List-II, listed for the inputs "
     "(A, B) = (0, 0), (0, 1), (1, 0), (1, 1) in that order.",
     ["A and B are fed to a NAND gate; its output and A are fed to a second NAND gate",
      "A and B are fed to a NOR gate; its output and A are fed to a second NOR gate",
      "A and B are fed to a NOR gate; its output and A are fed to an OR gate",
      "A and B are fed to a NAND gate; its output and B are fed to a NOR gate"],
     ["0, 0, 0, 0", "1, 0, 1, 1", "0, 1, 0, 0", "1, 1, 0, 1"]),
  *mlo("A-IV, B-III, C-II, D-I", ["A-II, B-III, C-IV, D-I", "A-IV, B-I, C-II, D-III", "A-III, B-IV, C-II, D-I"],
       "D"),
  "Truth tables of combinations of NAND, NOR and OR gates",
  "Work through each input combination. (A) X = NAND(A, B) = 1, 1, 1, 0; Y = NAND(X, A) = 1, 1, 0, 1. "
  "(B) X = NOR(A, B) = 1, 0, 0, 0; Y = NOR(X, A) = 0, 1, 0, 0. (C) Y = A OR X = 1, 0, 1, 1. "
  "(D) Y = NOR(X, B) with X = 1, 1, 1, 0: the NOR inputs are (1,0), (1,1), (1,0), (0,1), so Y = 0 always.",
  ["A → 1, 1, 0, 1 (IV)", "B → 0, 1, 0, 0 (III)", "C → 1, 0, 1, 1 (II)", "D → 0, 0, 0, 0 (I)"],
  why="A-II, C-IV interchanges the outputs of the NAND–NAND and NOR–OR circuits. B-I, D-III interchanges the NOR–NOR circuit with the NAND–NOR circuit. "
      "A-III, B-IV interchanges the first two circuits.",
  ncert=LOGIC, seconds=120, rc=True)

X_n = [g_nor(a, b) for a, b in INPUTS]
Y_n = [g_nand(x, a) for x, (a, b) in zip(X_n, INPUTS)]
Y_and = [g_and(x, a) for x, (a, b) in zip(X_n, INPUTS)]
Y_nor = [g_nor(x, a) for x, (a, b) in zip(X_n, INPUTS)]
truth = {"a": X_n == [1, 0, 0, 0], "b": Y_n == [1, 1, 1, 1], "c": Y_n == [0, 1, 1, 1], "d": Y_and == [0, 0, 0, 0],
         "e": Y_nor == [0, 1, 0, 0]}
assert truth == {"a": True, "b": True, "c": False, "d": True, "e": True}
q(ED, "Logic gates", "Advanced", "multi_statement",
  ms("Inputs A and B are fed to a NOR gate, whose output is X. X and A are then fed to a NAND gate, whose output is "
     "Y. Which of the following statements are correct?",
     ["X = 1 only when A = 0 and B = 0.",
      "Y = 1 for every combination of the inputs.",
      "The circuit as a whole behaves as an OR gate.",
      "If the NAND gate is replaced by an AND gate, the output becomes 0 for every combination of the inputs.",
      "If the NAND gate is replaced by a NOR gate, the output is 1 only when A = 0 and B = 1."]),
  *mso(truth, "abde", ["abd", "acde", "bde"], "B"),
  "Truth tables of combinations of gates",
  "X = NOR(A, B) = 1, 0, 0, 0 for (0,0), (0,1), (1,0), (1,1). X and A are never both 1 (X = 1 only when A = 0), so "
  "NAND(X, A) = 1 always and AND(X, A) = 0 always. NOR(X, A) is 1 only when X = 0 and A = 0, i.e. for (0, 1).",
  ["(a) X = 1, 0, 0, 0 → true", "(b) Y = 1, 1, 1, 1 → true", "(c) an OR gate gives 0 for (0,0), but Y = 1 → false",
   "(d) AND(X, A) = 0, 0, 0, 0 → true", "(e) NOR(X, A) = 0, 1, 0, 0 → true"],
  why="Only (c) is false: Y is 1 even when both inputs are 0. The codes with (c), or without (a) or (e), are wrong.",
  ncert=LOGIC, seconds=110, rc=True)

I_R = (10 - 6) / 100
I_L = 6 / 300
I_Z = I_R - I_L
close(I_R, 0.040)
close(I_Z, 0.020)
close(6 * I_Z, 0.12)
truth = {"a": True, "b": True, "c": abs(6 * I_Z - 0.24) < 1e-9, "d": True, "e": False}
assert truth == {"a": True, "b": True, "c": False, "d": True, "e": False}
q(ED, "Zener diode", "Advanced", "multi_statement",
  ms("A Zener diode of breakdown voltage 6.0 V is connected through a 100 Ω series resistor to a 10 V DC supply, and "
     "a 300 Ω load is connected across the Zener diode, which is in its breakdown region. Taking the voltage across "
     "the Zener diode as constant at 6.0 V, which of the following statements are correct?",
     ["The current through the series resistor is 40 mA.",
      "The current through the Zener diode is 20 mA.",
      "The power dissipated in the Zener diode is 0.24 W.",
      "If the load is disconnected, the current through the Zener diode becomes 40 mA.",
      "If the supply is raised to 12 V, the voltage across the load rises to 7.2 V."]),
  *mso(truth, "abd", ["ab", "abc", "bde"], "A"),
  "Zener voltage regulator: I_R = (V_in − V_Z)/R = I_Z + I_L",
  "The series resistor has 10 − 6 = 4.0 V across it, so it carries 40 mA. The load takes 6.0/300 = 20 mA, leaving "
  "20 mA for the Zener. Its power is 6.0 × 0.020 = 0.12 W. Without the load, all 40 mA goes through the Zener. As "
  "long as the Zener stays in breakdown, the load voltage stays at 6.0 V.",
  ["(a) 4.0 V/100 Ω = 40 mA → true", "(b) 40 − 20 = 20 mA → true", "(c) 6.0 × 0.020 = 0.12 W, not 0.24 W → false",
   "(d) no load: I_Z = 40 mA → true", "(e) load voltage stays 6.0 V → false"],
  why="(c) uses the 40 mA series current instead of the 20 mA Zener current, and (e) forgets that the Zener holds "
      "the load voltage at 6.0 V.",
  ncert=SD + "Zener diode (Zener diode as a voltage regulator)", seconds=110, rc=True)


# ================================================================ Experimental Skills (B2 I3 A2)
LAB = "NMC syllabus, Experimental Skills: "

rho_w = 3.0 * 0.10e-6 / 0.50
close(rho_w, 6.0e-7)
close(3.0 * 0.10e-6 * 0.50, 1.5e-7)
close(3.0 * 0.10 / 0.50, 0.60)
q(EXP, "Electrical experiments", "Basic", "numerical",
  "In the experiment to find the resistance of a given wire using Ohm's law, the graph of potential difference "
  "(y-axis) against current (x-axis) is a straight line through the origin with a slope of 3.0 Ω. The length of the "
  "wire between the connections is 50 cm and its cross-sectional area is 0.10 mm². The resistivity of its material "
  "is:",
  *opt("6.0 × 10⁻⁷ Ω m", ["1.5 × 10⁻⁷ Ω m", "3.0 × 10⁻⁷ Ω m", "0.60 Ω m"], "B"),
  "Slope of the V–I graph = R; ρ = RA/l",
  "The slope of V against I is the resistance of the wire, 3.0 Ω. The resistivity follows from R = ρl/A.",
  ["R = 3.0 Ω", "ρ = RA/l = 3.0 × 0.10 × 10⁻⁶/0.50 = 6.0 × 10⁻⁷ Ω m"],
  why="1.5 × 10⁻⁷ Ω m multiplies by the length instead of dividing. 3.0 × 10⁻⁷ Ω m ignores the length. 0.60 Ω m "
      "leaves the area in mm².",
  ncert=LAB + "resistance of a given wire using Ohm's law", seconds=40, rc=True)

q(EXP, "Thermal and fluid experiments", "Basic", "direct",
  "In the capillary-rise experiment, water rises to a certain height in a clean glass capillary tube. A little "
  "detergent is then dissolved in the water, the tube and temperature being unchanged. The height of the water "
  "column in the tube:",
  *opt("decreases, because the detergent lowers the surface tension of water",
       ["increases, because the detergent raises the surface tension of water",
        "stays the same, because the capillary rise depends only on the radius of the tube",
        "increases, because the detergent makes the water denser"], "D"),
  "Capillary rise h = 2S cos θ/(rρg); effect of detergents on surface tension",
  "Detergents reduce the surface tension of water. With S smaller (and the density nearly unchanged), the height "
  "h = 2S cos θ/(rρg) is smaller, so the water column is shorter.",
  ["Detergent lowers S", "h ∝ S → h decreases"],
  why="Detergents lower, not raise, the surface tension. The rise depends on the surface tension as well as on the "
      "radius. A small amount of detergent does not appreciably change the density, and a denser liquid would in "
      "any case rise less, not more.",
  ncert=LAB + "surface tension of water by capillary rise and effect of detergents", seconds=30)

ratio_vt = F(7800 - 1200, 2700 - 1200)
assert ratio_vt == F(22, 5)
close(7800 / 2700, 2.89, 1e-3)
q(EXP, "Thermal and fluid experiments", "Intermediate", "numerical",
  "In the terminal-velocity experiment, a steel ball (density 7800 kg m⁻³) and an aluminium ball (density "
  "2700 kg m⁻³) of the same radius are dropped in turn through the same viscous liquid of density 1200 kg m⁻³. "
  "Assuming Stokes' law holds for both, the ratio of the terminal velocity of the steel ball to that of the "
  "aluminium ball is:",
  *opt("4.4", ["2.9", "1/4.4", "6.5"], "C"),
  "Terminal velocity v = 2r²(ρ − σ)g/(9η)",
  "For balls of the same radius in the same liquid, the terminal velocity is proportional to the difference "
  "between the density of the ball and that of the liquid (weight minus buoyancy).",
  ["v ∝ (ρ − σ)", "Ratio = (7800 − 1200)/(2700 − 1200) = 6600/1500 = 4.4"],
  why="2.9 is the ratio of the densities of the balls, ignoring the buoyancy of the liquid. 1/4.4 inverts the "
      "ratio. 6.5 divides the density of steel by that of the liquid.",
  ncert=LAB + "coefficient of viscosity of a given viscous liquid by measuring terminal velocity", seconds=50,
  rc=True)

n_pr = 0.755 / math.sin(rad(30))
close(n_pr, 1.51)
close(math.sin(rad(60)) / 0.755, 1.15, 1e-2)
close(math.sin(rad(38)) / math.sin(rad(30)), 1.23, 1e-2)
q(EXP, "Optics experiments", "Intermediate", "numerical",
  "From the i–δ graph plotted for a triangular glass prism of refracting angle 60°, a student finds the minimum "
  "deviation to be 38°. Taking sin 49° = 0.755, the refractive index of the glass is about:",
  *opt("1.51", ["0.755", "1.15", "1.23"], "B"),
  "Prism formula n = sin[(A + δ_m)/2]/sin(A/2)",
  "At minimum deviation the angle of incidence is (A + δ_m)/2 = 49° and the angle of refraction inside the prism "
  "is A/2 = 30°.",
  ["(A + δ_m)/2 = (60° + 38°)/2 = 49°", "n = sin 49°/sin 30° = 0.755/0.5 ≈ 1.51"],
  why="0.755 forgets to divide by sin 30°. 1.15 inverts the formula, using sin 60°/sin 49°. 1.23 uses sin δ_m/sin "
      "(A/2), with the deviation alone in place of (A + δ_m)/2.",
  ncert=LAB + "plot of angle of deviation vs angle of incidence for a triangular prism; " + RO +
        "refraction through a prism", seconds=55, rc=True)

q(EXP, "Electrical experiments", "Intermediate", "assertion_reason",
  ar("In the experiment to draw the reverse-bias characteristic of a Zener diode, a resistor is connected in series "
     "with the Zener diode.",
     "Beyond the breakdown voltage, the reverse current of a Zener diode rises very sharply for a negligible change "
     "in voltage, so without a series resistor the current could become large enough to damage the diode."),
  AR, ar_key(True, True, True),
  "Zener characteristic: protection by a current-limiting resistor",
  "Once breakdown is reached, the voltage across the Zener hardly changes while the current can grow very large. A "
  "series resistor takes up the extra voltage and limits the current, protecting the diode and letting the "
  "breakdown region be traced safely. R gives exactly this reason.",
  ["A: series (current-limiting) resistor used → true", "R: sharp rise of current at breakdown → true",
   "The resistor is needed precisely because of this sharp rise → A"],
  why="Both statements are true and R is the reason for using the resistor.",
  ncert=LAB + "characteristic curves of a Zener diode and finding reverse breakdown voltage", seconds=45)

m_obj = F(40 * 25, 20)
m_app = F(40 * 20, 20)
dens = m_obj / (m_obj - m_app)
assert m_obj == 50 and m_app == 40 and dens == 5
assert m_app / (m_obj - m_app) == 4 and m_obj / m_app == F(5, 4)
q(EXP, "Mechanics experiments", "Advanced", "numerical",
  "A uniform metre scale is balanced on a knife edge at its 50.0 cm mark. A small solid object is hung from the "
  "30.0 cm mark, and the scale balances again (knife edge still at 50.0 cm) when a 40 g mass is hung from the "
  "75.0 cm mark. The object is then completely immersed in water (density 1.0 g cm⁻³), still hanging from the "
  "30.0 cm mark, and balance is restored by moving the 40 g mass to the 70.0 cm mark. The density of the material of "
  "the object is:",
  *opt("5.0 g cm⁻³", ["4.0 g cm⁻³", "1.25 g cm⁻³", "0.20 g cm⁻³"], "D"),
  "Principle of moments; loss of weight in water equals the weight of water displaced (Archimedes' principle)",
  "The scale's own weight acts at the knife edge and has no moment. In air: m × 20 cm = 40 g × 25 cm. In water the "
  "object's apparent mass m' satisfies m' × 20 cm = 40 g × 20 cm. The loss of mass, m − m', is the mass of water "
  "displaced, which fixes the volume.",
  ["In air: m = 40 × 25/20 = 50 g", "In water: m' = 40 × 20/20 = 40 g",
   "Water displaced = 10 g → volume = 10 cm³", "Density = 50/10 = 5.0 g cm⁻³"],
  why="4.0 g cm⁻³ divides the apparent mass in water (40 g) by the volume. 1.25 g cm⁻³ is the ratio of the mass in "
      "air to the apparent mass in water. 0.20 g cm⁻³ inverts the correct ratio.",
  ncert=LAB + "mass of a given object using a metre scale by the principle of moments", seconds=120, rc=True)

q(EXP, "Electrical experiments", "Advanced", "statement_pair",
  sp("In the experiment on the dissipation of energy of a simple pendulum, the square of the amplitude is plotted "
     "against time because the energy of oscillation is proportional to the square of the amplitude.",
     "To find the reverse breakdown voltage of a Zener diode, the diode is connected in forward bias and the "
     "voltage at which the current starts to rise sharply is noted."),
  SP, sp_key(True, False),
  "Laboratory experiments: damped pendulum; Zener characteristic",
  "Statement I is true: the energy of a pendulum oscillating with small amplitude A is proportional to A², so a "
  "graph of A² against time shows how the energy is dissipated. Statement II is false: the breakdown voltage is "
  "found from the reverse-bias characteristic; in forward bias a Zener diode behaves like an ordinary diode, "
  "conducting beyond about 0.7 V.",
  ["I: E ∝ A² → true", "II: breakdown is a reverse-bias effect → false"],
  why="Statement II confuses the forward threshold voltage with the reverse breakdown voltage.",
  ncert=LAB + "simple pendulum - dissipation of energy by plotting a graph between square of amplitude and time; "
              "characteristic curves of a Zener diode", seconds=45)
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
    doc = {"schema_version": "1.0", "batch_id": "BATCH_008", "created_at": TODAY,
           "notes": "Package PHY_008_p2: 125 original Physics questions (Current Electricity to Experimental Skills), "
                    "NEET_PHY_001876..002000. Numerical answers recomputed by tools/batch_008/PHY_008_p2.py.",
           "stimuli": [], "questions": QS}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {OUT}: {len(QS)} questions")
    print("difficulty", dict(Counter(x["difficulty"] for x in QS)))
    print("formats", dict(fmts))
    print("keys", dict(sorted(keys.items())))


if __name__ == "__main__":
    main()
