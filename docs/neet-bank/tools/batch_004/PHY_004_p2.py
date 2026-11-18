"""Builder for batches/parts/BATCH_004_PHY_p2.json (package PHY_004_p2 of BATCH_004).

Physics, 120 original questions, NEET_PHY_000881..NEET_PHY_001000: Current Electricity, Magnetic Effects of Current
and Magnetism, Electromagnetic Induction and Alternating Currents, Electromagnetic Waves, Optics, Dual Nature of
Matter and Radiation, Atoms and Nuclei, Electronic Devices, Experimental Skills.

Every numerical answer is recomputed below with an assert next to its question; multi-statement, assertion-reason
and statement-pair keys are derived from truth tables; the plan quota, format mix and answer-key balance are
asserted before anything is written. If any assert fails, nothing is written.

    python tools/batch_004/PHY_004_p2.py        (run from docs/neet-bank)
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
PLAN = ROOT / "batches" / "plans" / "BATCH_004_plan.json"
OUT = ROOT / "batches" / "parts" / "BATCH_004_PHY_p2.json"
PACKAGE = "PHY_004_p2"
FIRST_ID = 881
COUNT = 120

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


# ================================================================ Current Electricity (B5 I7 A5)
CEC = NC + "'Current Electricity', "

# ---- Basic
I_b1, e_ch = 1.6, 1.6e-19
close(I_b1 / e_ch, 1.0e19)
close(I_b1 * e_ch, 2.56e-19)
close(1 / e_ch, 6.25e18)
q(CE, "Drift velocity and Ohm's law", "Basic", "numerical",
  "A steady current of 1.6 A flows through a metal wire. Taking the magnitude of the electronic charge as "
  "1.6 × 10⁻¹⁹ C, the number of free electrons crossing any cross-section of the wire per second is:",
  *opt("1.0 × 10¹⁹", ["2.56 × 10⁻¹⁹", "6.25 × 10¹⁸", "1.0 × 10¹⁸"], "B"),
  "Current as rate of flow of charge: I = (number per second) × e",
  "The charge crossing a section per second is the current. Each electron carries charge e, so the number of "
  "electrons per second is I/e.",
  ["n = I/e = 1.6/(1.6 × 10⁻¹⁹)", "n = 1.0 × 10¹⁹ electrons per second"],
  why="2.56 × 10⁻¹⁹ multiplies I by e instead of dividing. 6.25 × 10¹⁸ is the number per second for 1 A, not 1.6 A. "
      "1.0 × 10¹⁸ is a slip in the power of ten.",
  ncert=CEC + "electric current", seconds=30, rc=True)

Rs_b3, Rp_b3 = 50, 2
n_b3 = round(math.sqrt(Rs_b3 / Rp_b3))
R_b3 = Rs_b3 / n_b3
assert n_b3 == 5 and R_b3 == 10 and R_b3 / n_b3 == Rp_b3
q(CE, "Combination of resistors", "Basic", "numerical",
  "A number of identical resistors give an equivalent resistance of 50 Ω when all of them are connected in series "
  "and 2 Ω when all of them are connected in parallel. The number of resistors and the resistance of each are:",
  *opt("5 resistors of 10 Ω each", ["25 resistors of 2 Ω each", "10 resistors of 5 Ω each",
                                    "5 resistors of 50 Ω each"], "C"),
  "n identical resistors R: series nR, parallel R/n",
  "Dividing the series value by the parallel value removes R and gives n²; then R follows from nR.",
  ["nR = 50 and R/n = 2", "(nR)/(R/n) = n² = 25 → n = 5", "R = 50/5 = 10 Ω (check: 10/5 = 2 Ω)"],
  shortcut="n = √(R_series/R_parallel).",
  why="25 resistors takes n = R_s/R_p instead of its square root. 10 resistors of 5 Ω swaps n and R (series would "
      "then be 50 Ω but parallel 0.5 Ω). 5 resistors of 50 Ω puts the series total on each resistor.",
  ncert=CEC + "combination of resistors - series and parallel", seconds=45, rc=True)

eps_b4, r_b4, I_b4 = 12.0, 0.5, 4.0
close(eps_b4 + I_b4 * r_b4, 14.0)
close(eps_b4 - I_b4 * r_b4, 10.0)
q(CE, "Cells, emf and internal resistance", "Basic", "numerical",
  "A battery of emf 12 V and internal resistance 0.5 Ω is being charged by an external DC source, and a charging "
  "current of 4 A flows into its positive terminal. The potential difference across the terminals of the battery "
  "during charging is:",
  *opt("14 V", ["10 V", "12 V", "16 V"], "D"),
  "Terminal voltage while charging: V = ε + Ir",
  "While charging, current is driven into the positive terminal against the emf, so the external source must "
  "supply the emf and also the drop across the internal resistance.",
  ["V = ε + Ir = 12 + 4 × 0.5", "V = 14 V"],
  why="10 V uses ε − Ir, which applies when the battery is discharging. 12 V ignores the internal resistance. 16 V "
      "adds the current (4) instead of the drop Ir (2 V).",
  ncert=CEC + "cells, emf, internal resistance", seconds=35, rc=True)

q(CE, "Drift velocity and Ohm's law", "Basic", "direct",
  "When a potential difference is applied across a metal wire, the drift velocity of its free electrons is directed:",
  *opt("opposite to the direction of the electric field in the wire",
       ["along the direction of the electric field in the wire", "perpendicular to the electric field in the wire",
        "in no particular direction, since the electrons move randomly"], "A"),
  "Force on an electron in an electric field: F = −eE",
  "Each free electron is accelerated by the force −eE between collisions, so the average (drift) velocity it "
  "acquires is v_d = −eEτ/m, i.e. opposite to E. The conventional current is along E.",
  ["Electron charge is negative → force −eE", "v_d = −(eτ/m)E → opposite to E"],
  why="Along E is the direction of conventional current, not of electron drift. Perpendicular has no basis. The "
      "thermal velocities are random, but the drift superposed on them has a definite direction.",
  ncert=CEC + "drift of electrons and the origin of resistivity", seconds=25)

q(CE, "Drift velocity and Ohm's law", "Basic", "statement_pair",
  sp("The power dissipated in a resistor connected across a fixed potential difference V is directly proportional "
     "to its resistance.",
     "The commercial unit of electrical energy, 1 kilowatt-hour, is equal to 3.6 × 10⁶ J."),
  SP, sp_key(False, True),
  "Electrical power P = V²/R; kilowatt-hour",
  "For a fixed V, P = V²/R, so the power is inversely proportional to R (Statement I false). 1 kWh = 1000 W × "
  "3600 s = 3.6 × 10⁶ J (Statement II true).",
  ["Fixed V: P = V²/R ∝ 1/R → Statement I false", "1 kWh = 10³ × 3600 J = 3.6 × 10⁶ J → Statement II true"],
  why="P ∝ R holds for a fixed current (P = I²R), not for a fixed potential difference; so options with Statement I "
      "true are wrong, and Statement II is true.",
  ncert=CEC + "electrical energy, power", seconds=35)

# ---- Intermediate
m_e9, n_i1, rho_i1 = 9.0e-31, 6.25e28, 2.25e-8
tau_i1 = m_e9 / (n_i1 * e_ch ** 2 * rho_i1)
close(tau_i1, 2.5e-14)
close(m_e9 / (n_i1 * e_ch * rho_i1), 4.0e-33)
close(n_i1 * e_ch ** 2 * rho_i1 / m_e9, 4.0e13)
q(CE, "Drift velocity and Ohm's law", "Intermediate", "numerical",
  "A metal has 6.25 × 10²⁸ free electrons per m³ and a resistivity of 2.25 × 10⁻⁸ Ω m. Taking the electron mass "
  "as 9.0 × 10⁻³¹ kg and e = 1.6 × 10⁻¹⁹ C, the average relaxation time of the free electrons is:",
  *opt("2.5 × 10⁻¹⁴ s", ["4.0 × 10⁻³³ s", "4.0 × 10¹³ s", "1.25 × 10⁻¹⁴ s"], "A"),
  "Resistivity in terms of relaxation time: ρ = m/(ne²τ)",
  "The free-electron model gives ρ = m/(ne²τ). Rearranging gives τ = m/(ne²ρ).",
  ["ne²ρ = 6.25 × 10²⁸ × (1.6 × 10⁻¹⁹)² × 2.25 × 10⁻⁸ = 3.6 × 10⁻¹⁷",
   "τ = 9.0 × 10⁻³¹ / 3.6 × 10⁻¹⁷ = 2.5 × 10⁻¹⁴ s"],
  why="4.0 × 10⁻³³ s uses e instead of e². 4.0 × 10¹³ s inverts the expression. 1.25 × 10⁻¹⁴ s halves the correct "
      "value (an extra factor of 2).",
  ncert=CEC + "drift of electrons and the origin of resistivity", seconds=60, rc=True)

E_i2, R4_i2, e3_i2 = 12.0, 4.0, 3.0
I_i2 = e3_i2 / R4_i2
R_i2 = E_i2 / I_i2 - R4_i2
close(R_i2, 12.0)
close(E_i2 / I_i2, 16.0)
q(CE, "Kirchhoff's laws", "Intermediate", "numerical",
  "A cell of emf 12 V and negligible internal resistance is connected in series with a resistor R and a 4 Ω "
  "resistor. A second cell, of emf 3 V and negligible internal resistance, is connected in series with a "
  "galvanometer, and this branch is connected across the 4 Ω resistor, the positive terminal of the 3 V cell being "
  "joined to the end of the 4 Ω resistor that is at the higher potential. The galvanometer shows no deflection. "
  "The value of R is:",
  *opt("12 Ω", ["16 Ω", "4/3 Ω", "9 Ω"], "B"),
  "Loop rule for a branch carrying no current",
  "With no current in the galvanometer branch, the loop rule round that branch and the 4 Ω resistor gives: "
  "p.d. across 4 Ω = 3 V. The main loop then carries a current 3/4 A, which fixes R.",
  ["No current in the 3 V branch → I × 4 = 3 → I = 0.75 A",
   "Main loop: 12 = I(R + 4) → R + 4 = 16 → R = 12 Ω"],
  why="16 Ω is the total resistance of the main loop, not R. 4/3 Ω inverts the ratio of the voltages (9 V across R, "
      "3 V across 4 Ω). 9 Ω divides the 9 V across R by 1 A instead of 0.75 A.",
  ncert=CEC + "Kirchhoff's rules", seconds=75, rc=True)

P_i3, Q_i3, R_i3, S_i3 = 10, 30, 20, 90
S_need = F(R_i3 * Q_i3, P_i3)
X_i3 = S_i3 * S_need / (S_i3 - S_need)
assert S_need == 60 and X_i3 == 180
par = lambda a, b: F(a * b, a + b)
assert par(90, 30) != 60 and par(90, 60) != 60 and 90 + 30 != 60
q(CE, "Wheatstone and metre bridge", "Intermediate", "numerical",
  "In a Wheatstone bridge, P = 10 Ω and Q = 30 Ω are in series between points A and C, meeting at B, and R = 20 Ω "
  "and S = 90 Ω are in series between A and C, meeting at D (P and R are joined at A). A cell is connected between "
  "A and C and a galvanometer between B and D. To balance the bridge without changing P, Q or R, a resistor should "
  "be connected to S as follows:",
  *opt("180 Ω in parallel with S", ["30 Ω in parallel with S", "60 Ω in parallel with S", "30 Ω in series with S"],
       "D"),
  "Balance condition P/Q = R/S; parallel combination to reduce a resistance",
  "Balance needs S_eff = RQ/P = 20 × 30/10 = 60 Ω. Since 90 Ω is too large, a resistor X must be put in parallel "
  "with S: 90X/(90 + X) = 60.",
  ["Required S_eff = RQ/P = 60 Ω", "90X/(90 + X) = 60 → 90X = 5400 + 60X → X = 180 Ω"],
  why="30 Ω in parallel gives 22.5 Ω and 60 Ω in parallel gives 36 Ω, not 60 Ω. A resistor in series can only "
      "increase S above 90 Ω.",
  ncert=CEC + "Wheatstone bridge", seconds=70, rc=True)

P0, V0_i7, V1_i7 = 1000, 220, 200
drop = 1 - (V1_i7 / V0_i7) ** 2
close(drop, 0.1736, 1e-3)
close(1 - V1_i7 / V0_i7, 0.0909, 1e-3)
close((V0_i7 / V1_i7) ** 2 - 1, 0.21, 1e-2)
q(CE, "Drift velocity and Ohm's law", "Intermediate", "numerical",
  "An electric heater is rated 1000 W, 220 V. If the supply voltage falls to 200 V, the power drawn by the heater "
  "falls by about (assume its resistance stays the same):",
  *opt("17%", ["9%", "83%", "21%"], "C"),
  "P = V²/R for a fixed resistance",
  "With R fixed, P ∝ V², so the new power is (200/220)² of the rated power.",
  ["P'/P = (200/220)² = 0.826", "Fall = 1 − 0.826 = 0.174 ≈ 17% (P' ≈ 826 W)"],
  why="9% assumes P ∝ V. 83% is the fraction of power that remains, not the fall. 21% is (220/200)² − 1, the "
      "increase computed the wrong way round.",
  ncert=CEC + "electrical energy, power", seconds=50, rc=True)

q(CE, "Cells, emf and internal resistance", "Intermediate", "statement_pair",
  sp("Two cells of emfs ε₁ and ε₂ and internal resistances r₁ and r₂, connected in parallel (positive terminal to "
     "positive terminal), are equivalent to a single cell of emf (ε₁r₂ + ε₂r₁)/(r₁ + r₂).",
     "The internal resistance of this parallel combination is r₁ + r₂."),
  SP, sp_key(True, False),
  "Cells in parallel",
  "For two cells in parallel, the equivalent emf is (ε₁r₂ + ε₂r₁)/(r₁ + r₂) (Statement I true) and the equivalent "
  "internal resistance is r₁r₂/(r₁ + r₂), like two resistors in parallel (Statement II false). r₁ + r₂ is the "
  "internal resistance of the series combination.",
  ["ε_eq = (ε₁r₂ + ε₂r₁)/(r₁ + r₂) → Statement I true", "r_eq = r₁r₂/(r₁ + r₂), not r₁ + r₂ → Statement II false"],
  why="Statement II gives the series result, so options with Statement II true are wrong; Statement I is the "
      "standard result, so options with it false are wrong.",
  ncert=CEC + "cells in series and in parallel", seconds=45)

q(CE, "Resistivity and temperature", "Intermediate", "match_list",
  ml("A uniform metal wire is stretched until its length is doubled. Its volume, resistivity and temperature do not "
     "change. Match each quantity in List-I with its change in List-II.",
     ["Resistance of the wire", "Resistivity of the material", "Cross-sectional area of the wire",
      "Current density, for the same current through the wire"],
     ["Unchanged", "Becomes 4 times", "Becomes half", "Becomes twice"]),
  *mlo("A-II, B-I, C-III, D-IV",
       ["A-IV, B-I, C-III, D-II", "A-II, B-IV, C-III, D-I", "A-II, B-I, C-IV, D-III"], "B"),
  "R = ρl/A with constant volume; resistivity is a material property; J = I/A",
  "Constant volume means A halves when l doubles. Then R = ρl/A becomes 2 × 2 = 4 times. Resistivity depends only "
  "on the material and temperature, so it is unchanged. For the same current, J = I/A doubles.",
  ["Al = constant → A' = A/2 → C-III", "R' = ρ(2l)/(A/2) = 4R → A-II", "ρ unchanged → B-I", "J' = I/(A/2) = 2J → D-IV"],
  why="A-IV takes R ∝ l only and forgets that A also halves. B-IV treats resistivity as if it changed with shape. "
      "C-IV makes the area double instead of halve.",
  ncert=CEC + "resistivity of various materials", seconds=50)

ms_ce1 = {"a": True, "b": True, "c": True, "d": False, "e": True}
q(CE, "Combination of resistors", "Intermediate", "multi_statement",
  ms("Which of the following statements about combinations of resistors are correct?",
     ["In a parallel combination, the current through each resistor is inversely proportional to its resistance.",
      "The equivalent resistance of a parallel combination is less than the smallest of the individual resistances.",
      "The equivalent resistance of a series combination is greater than the largest of the individual "
      "resistances.",
      "Connecting one more resistor in parallel with an existing parallel combination increases its equivalent "
      "resistance.",
      "In a series combination, the potential difference across each resistor is proportional to its resistance."]),
  *mso(ms_ce1, "abce", ["abc", "bcde", "ade"], "D"),
  "Series and parallel combinations",
  "In parallel all resistors have the same V, so I = V/R ∝ 1/R, and 1/R_eq = Σ1/R is larger than any single 1/R, "
  "making R_eq smaller than the smallest R. Adding a branch adds to 1/R_eq, so R_eq decreases. In series the same "
  "current flows, so V = IR ∝ R and R_eq = ΣR exceeds the largest R.",
  ["(a) V same → I ∝ 1/R: true", "(b) 1/R_eq > 1/R_min → R_eq < R_min: true", "(c) R_eq = ΣR > R_max: true",
   "(d) adding a parallel branch lowers R_eq: false", "(e) I same → V ∝ R: true"],
  why="(a), (b) and (c) only leaves out the true statement (e). The other two options include (d), which is false, "
      "or leave out true statements.",
  ncert=CEC + "combination of resistors - series and parallel", seconds=60)

# ---- Advanced
n_a1, e_a1, r_a1 = 4, 1.5, 0.5
R_a1 = r_a1  # n e/(R + n r) = e/(R + r/n)  →  R = r
I_ser = n_a1 * e_a1 / (R_a1 + n_a1 * r_a1)
I_par = e_a1 / (R_a1 + r_a1 / n_a1)
close(I_ser, 2.4)
close(I_par, 2.4)
close(n_a1 * e_a1 / (n_a1 * r_a1), 3.0)
close(e_a1 / (R_a1 + n_a1 * r_a1), 0.6)
q(CE, "Cells, emf and internal resistance", "Advanced", "numerical",
  "Four identical cells, each of emf 1.5 V and internal resistance 0.5 Ω, are used to send a current through an "
  "external resistor R. The current in R is found to be the same whether the four cells are all connected in series "
  "or all connected in parallel. The current in R is:",
  *opt("2.4 A", ["3.0 A", "0.6 A", "1.2 A"], "C"),
  "Series: nε/(R + nr); parallel: ε/(R + r/n)",
  "Equating the two currents fixes R; then either expression gives the current.",
  ["nε/(R + nr) = ε/(R + r/n) → n(R + r/n) = R + nr → (n − 1)R = (n − 1)r → R = r = 0.5 Ω",
   "Series: I = 6/(0.5 + 2) = 2.4 A", "Parallel check: I = 1.5/(0.5 + 0.125) = 2.4 A"],
  shortcut="The two groupings give equal currents exactly when R equals the internal resistance of one cell.",
  why="3.0 A takes R = 0 in the series formula. 0.6 A uses the emf of one cell with the internal resistance of all "
      "four in series. 1.2 A halves the correct value.",
  ncert=CEC + "cells in series and in parallel", seconds=90, rc=True)

edges_a2 = [(0, 2, 2), (2, 1, 4), (0, 3, 3), (3, 1, 6), (2, 3, 5)]
Req_a2 = equivalent_resistance(4, edges_a2, 0, 1)
assert Req_a2 == F(18, 5)
assert solve_network(4, edges_a2, {0: 1, 1: 0})[2] == solve_network(4, edges_a2, {0: 1, 1: 0})[3]
assert par(Req_a2, 5) < 3 and 2 + 4 + 3 + 6 + 5 == 20
q(CE, "Wheatstone and metre bridge", "Advanced", "numerical",
  "Five resistors are connected between points A and B as follows: 2 Ω from A to C, 4 Ω from C to B, 3 Ω from A to "
  "D, 6 Ω from D to B, and 5 Ω between C and D. The equivalent resistance between A and B is:",
  *opt("3.6 Ω", ["2.1 Ω", "5.0 Ω", "20 Ω"], "B"),
  "Balanced Wheatstone bridge: the middle resistor carries no current",
  "The four outer resistors form a Wheatstone bridge with ratio 2/4 = 3/6, so C and D are at the same potential "
  "whatever voltage is applied between A and B. The 5 Ω resistor carries no current and can be removed.",
  ["2/4 = 3/6 → balanced → no current in 5 Ω", "Path ACB = 6 Ω, path ADB = 9 Ω",
   "R_AB = 6 × 9/(6 + 9) = 3.6 Ω"],
  shortcut="Check P/Q = R/S first; if it holds, drop the bridging resistor.",
  why="2.1 Ω treats the 5 Ω resistor as if it were connected in parallel across A and B. 5.0 Ω is just the bridging "
      "resistor. 20 Ω adds all five resistors in series.",
  ncert=CEC + "Wheatstone bridge", seconds=60, rc=True)

t1_a3, t2_a3 = 10, 15
t_par = F(t1_a3 * t2_a3, t1_a3 + t2_a3)
assert t_par == 6 and t1_a3 + t2_a3 == 25
q(CE, "Combination of resistors", "Advanced", "numerical",
  "Two heater coils, each connected separately across the same mains supply, boil a given quantity of water in "
  "10 minutes and 15 minutes respectively. If the two coils are connected in parallel across the same supply, the "
  "time taken to boil the same quantity of water is (neglect heat losses and any change of resistance):",
  *opt("6 minutes", ["25 minutes", "12.5 minutes", "5 minutes"], "D"),
  "Heat H = (V²/R)t at fixed V; parallel powers add",
  "The same heat H is needed each time. With V fixed, P = V²/R, so t = H/P ∝ R. In parallel the powers add: "
  "P = P₁ + P₂, so 1/t = 1/t₁ + 1/t₂.",
  ["1/t = 1/10 + 1/15 = 1/6", "t = 6 minutes"],
  shortcut="Parallel: t = t₁t₂/(t₁ + t₂); series: t = t₁ + t₂.",
  why="25 minutes is the time with the coils in series. 12.5 minutes is the average of the two times. 5 minutes "
      "would need the two times to be equal (10 and 10).",
  seconds=70, rc=True)

q(CE, "Combination of resistors", "Advanced", "assertion_reason",
  ar("A resistor R₁ is connected in series with a resistor R₂ across a battery. A voltmeter of finite resistance, "
     "connected across R₁, reads less than the potential difference that existed across R₁ before the voltmeter "
     "was connected.",
     "The voltmeter in parallel with R₁ lowers the resistance of that part of the circuit, so this part takes a "
     "smaller share of the battery voltage."),
  AR, ar_key(True, True, True),
  "Loading effect of a voltmeter; potential divider",
  "In a series circuit the voltage divides in proportion to the resistances. The voltmeter (resistance R_V) in "
  "parallel with R₁ makes that part R₁R_V/(R₁ + R_V) < R₁, while R₂ (and any internal resistance) is unchanged, so "
  "the share of the voltage across that part falls. This is exactly why the reading is low; an ideal voltmeter "
  "would need infinite resistance.",
  ["Parallel combination R₁ ∥ R_V < R₁", "Smaller fraction of the battery voltage across it → reading low (A true)",
   "R states this mechanism → R true and explains A"],
  why="R gives the actual cause of the lower reading, so option B is wrong; both statements are true, so options C "
      "and D are wrong.",
  seconds=60)

ms_ce2 = {"a": True, "b": True, "c": True, "d": True, "e": False}
q(CE, "Drift velocity and Ohm's law", "Advanced", "multi_statement",
  ms("A uniform metal wire is connected across an ideal battery of constant emf. It is replaced by a wire of the same "
     "material and the same length but twice the diameter, connected across the same battery. The temperature of "
     "the wire is the same in both cases. Which of the following statements are correct for the second wire, "
     "compared with the first?",
     ["The current through it is four times as large.",
      "The drift speed of its free electrons is the same.",
      "The electric field inside it is the same.",
      "The power dissipated in it is four times as large.",
      "The resistivity of its material is one-fourth as large."]),
  *mso(ms_ce2, "abcd", ["ad", "ace", "bcd"], "A"),
  "R = ρl/A; I = neAv_d; E = V/l; P = V²/R",
  "Doubling the diameter makes the area 4 times, so R becomes one-fourth and I = V/R becomes 4 times. The field "
  "E = V/l is unchanged because V and l are unchanged, so v_d = (eτ/m)E is unchanged (check: v_d = I/(neA) = "
  "4I/(ne·4A)). P = V²/R becomes 4 times. Resistivity depends on material and temperature only, so it is unchanged.",
  ["A → 4A, R → R/4, I → 4I: (a) true", "v_d = I/(neA) unchanged: (b) true", "E = V/l unchanged: (c) true",
   "P = V²/R → 4P: (d) true", "ρ unchanged: (e) false"],
  why="(a) and (d) only and (b), (c) and (d) only leave out true statements. (a), (c) and (e) only includes (e), "
      "which is false because resistivity does not depend on the dimensions.",
  ncert=CEC + "drift of electrons and the origin of resistivity", seconds=90)

# ================================================================ Magnetic Effects of Current and Magnetism (B5 I7 A5)
MCC = NC + "'Moving Charges and Magnetism', "
MMC = NC + "'Magnetism and Matter', "
MU0 = 4 * math.pi * 1e-7

# ---- Basic
q(MAG, "Force on charges and conductors", "Basic", "direct",
  "In the definition of the ampere based on the force between currents, one ampere is the steady current which, "
  "maintained in each of two very long, straight, parallel conductors of negligible cross-section placed 1 m apart "
  "in vacuum, produces on each conductor a force of:",
  *opt("2 × 10⁻⁷ N per metre of length", ["1 N per metre of length", "4π × 10⁻⁷ N per metre of length",
                                         "1 × 10⁻⁷ N per metre of length"], "A"),
  "Force between parallel currents: f = µ₀I₁I₂/(2πd)",
  "With I₁ = I₂ = 1 A and d = 1 m, f = (4π × 10⁻⁷ × 1 × 1)/(2π × 1) = 2 × 10⁻⁷ N per metre. This is the basis "
  "of the definition of the ampere given in the textbook.",
  ["f = µ₀I₁I₂/(2πd) = 2 × 10⁻⁷ × 1 × 1/1", "f = 2 × 10⁻⁷ N/m"],
  why="4π × 10⁻⁷ is µ₀ itself, forgetting the 2π in the denominator. 1 × 10⁻⁷ is µ₀/4π. 1 N/m has no basis.",
  ncert=MCC + "magnetic force between two parallel currents, the ampere", seconds=30)

Is_b2, G_b2 = 10.0, 20.0  # div per mA, ohm
Vs_b2 = Is_b2 / G_b2      # div per mV, since 1 mA × 1 Ω = 1 mV
close(Vs_b2, 0.5)
q(MAG, "Torque on loop and galvanometer", "Basic", "numerical",
  "A moving-coil galvanometer has a current sensitivity of 10 divisions per mA and a coil resistance of 20 Ω. Its "
  "voltage sensitivity is:",
  *opt("0.5 division per mV", ["200 divisions per mV", "2 divisions per mV", "0.05 division per mV"], "C"),
  "Voltage sensitivity = current sensitivity / G",
  "A potential difference V drives a current V/G through the coil, so the deflection per unit voltage is the "
  "deflection per unit current divided by G.",
  ["V_s = I_s/G = (10 div/mA)/(20 Ω)", "= 0.5 division per (mA × Ω) = 0.5 division per mV"],
  why="200 divisions per mV multiplies by G. 2 divisions per mV inverts the ratio (G/I_s). 0.05 division per mV is a "
      "slip of a factor of 10.",
  ncert=MCC + "moving coil galvanometer", seconds=35, rc=True)

m_b3, r_b3 = 0.5, 0.10
B_eq = 1e-7 * m_b3 / r_b3 ** 3
close(B_eq, 5e-5)
close(2 * B_eq, 1e-4)
close(1e-7 * m_b3 / r_b3 ** 2, 5e-6)
q(MAG, "Magnetic dipole and bar magnet", "Basic", "numerical",
  "A short bar magnet has a magnetic moment of 0.5 A m². Taking µ₀/4π = 10⁻⁷ T m A⁻¹ and ignoring all other "
  "magnetic fields, the magnitude of its magnetic field at a point on its equatorial line (the perpendicular "
  "bisector of its axis), 10 cm from its centre, is:",
  *opt("5 × 10⁻⁵ T", ["1 × 10⁻⁴ T", "5 × 10⁻⁶ T", "2.5 × 10⁻⁵ T"], "B"),
  "Equatorial field of a short magnet: B = µ₀m/(4πr³)",
  "On the equatorial line of a short dipole the field is (µ₀/4π)(m/r³), half of the axial field at the same "
  "distance.",
  ["B = 10⁻⁷ × 0.5/(0.10)³", "B = 5 × 10⁻⁸/10⁻³ = 5 × 10⁻⁵ T"],
  why="1 × 10⁻⁴ T is the axial value (2m/r³). 5 × 10⁻⁶ T divides by r² instead of r³. 2.5 × 10⁻⁵ T halves the "
      "equatorial value.",
  ncert=MMC + "the bar magnet", seconds=40, rc=True)

q(MAG, "Magnetic materials", "Basic", "direct",
  "Which one of the following substances is ferromagnetic at room temperature?",
  *opt("Nickel", ["Copper", "Aluminium", "Water"], "D"),
  "Classification of magnetic materials",
  "Iron, cobalt, nickel and gadolinium are the common ferromagnetic substances. Copper and water are diamagnetic; "
  "aluminium is paramagnetic.",
  ["Ferromagnetic examples: Fe, Co, Ni, Gd → nickel"],
  why="Copper and water are diamagnetic and aluminium is paramagnetic; none of them is ferromagnetic.",
  ncert=MMC + "ferromagnetism", seconds=20)

I1_b5, I2_b5, I3_b5 = 5, 2, 6
circ = MU0 * (I1_b5 - I2_b5)
close(circ, 3.77e-6, 1e-2)
close(MU0 * (I1_b5 + I2_b5), 8.8e-6, 1e-2)
close(MU0 * (I1_b5 - I2_b5 + I3_b5), 1.13e-5, 1e-2)
q(MAG, "Ampere's law", "Basic", "numerical",
  "Three long straight wires are perpendicular to the plane of a closed loop. Wire 1 carries 5 A out of the plane "
  "and wire 2 carries 2 A into the plane; both pass through the region enclosed by the loop. Wire 3 carries 6 A out "
  "of the plane and lies outside the loop. Taking µ₀ = 4π × 10⁻⁷ T m A⁻¹, the magnitude of the line integral of the "
  "magnetic field round the loop, ∮B·dl, is about:",
  *opt("3.8 × 10⁻⁶ T m", ["8.8 × 10⁻⁶ T m", "1.1 × 10⁻⁵ T m", "zero"], "A"),
  "Ampere's circuital law: ∮B·dl = µ₀I_enclosed (algebraic sum)",
  "Only currents that pass through the surface bounded by the loop count, with opposite directions taking opposite "
  "signs. Wire 3, outside the loop, contributes nothing to the line integral (though it does contribute to B at "
  "points of the loop).",
  ["I_enc = 5 − 2 = 3 A", "∮B·dl = 4π × 10⁻⁷ × 3 ≈ 3.8 × 10⁻⁶ T m"],
  why="8.8 × 10⁻⁶ T m adds 5 A and 2 A ignoring their directions. 1.1 × 10⁻⁵ T m also counts the 6 A wire outside "
      "the loop. Zero would need the enclosed currents to cancel.",
  ncert=MCC + "Ampere's circuital law", seconds=45, rc=True)

# ---- Intermediate
I_i1, d_i1 = 5.0, 0.10
B_each = 2e-7 * I_i1 / (d_i1 / 2)
close(2 * B_each, 4e-5)
close(2 * (2e-7 * I_i1 / d_i1), 2e-5)
close(2e-7 * I_i1 / d_i1, 1e-5)
q(MAG, "Biot-Savart law", "Intermediate", "numerical",
  "Two long straight parallel wires, 10 cm apart, carry currents of 5 A each in opposite directions. Taking "
  "µ₀ = 4π × 10⁻⁷ T m A⁻¹, the magnitude of the magnetic field at the point midway between the wires is:",
  *opt("4 × 10⁻⁵ T", ["zero", "2 × 10⁻⁵ T", "1 × 10⁻⁵ T"], "C"),
  "Field of a long wire B = µ₀I/(2πd); superposition",
  "Between two wires with opposite currents, the fields of the two wires point the same way (use the right-hand "
  "rule on each), so they add. Each wire is 5 cm from the midpoint.",
  ["Each: B = 2 × 10⁻⁷ × 5/0.05 = 2 × 10⁻⁵ T", "Same direction → B = 2 × 2 × 10⁻⁵ = 4 × 10⁻⁵ T"],
  why="Zero is the result for currents in the same direction. 2 × 10⁻⁵ T uses 10 cm instead of 5 cm for the "
      "distance. 1 × 10⁻⁵ T is one wire at 10 cm.",
  ncert=MCC + "Ampere's circuital law (field of a long straight wire)", seconds=50, rc=True)

lam_i2, g10, B_i2 = 0.050, 10.0, 0.5
I_lev = lam_i2 * g10 / B_i2
close(I_lev, 1.0)
close(lam_i2 / B_i2, 0.1)
close(B_i2 / lam_i2, 10)
close(lam_i2 * g10 * B_i2, 0.25)
q(MAG, "Force on charges and conductors", "Intermediate", "numerical",
  "A long horizontal straight wire has a mass of 50 g per metre of its length. It is held in mid-air, with no "
  "support, by a uniform horizontal magnetic field of 0.5 T at right angles to the wire. Taking g = 10 m/s², the "
  "current in the wire is:",
  *opt("1.0 A", ["0.1 A", "10 A", "0.25 A"], "D"),
  "Force on a current: F = BIl; balance with weight",
  "For the wire to float, the upward magnetic force on each metre must equal the weight of each metre: BI × 1 = "
  "(mass per metre) × g.",
  ["BI = λg → I = λg/B", "I = 0.050 × 10/0.5 = 1.0 A"],
  why="0.1 A leaves out g. 10 A divides B by the mass per metre (an inverted ratio). 0.25 A multiplies by B "
      "instead of dividing.",
  ncert=MCC + "magnetic force on a current-carrying conductor", seconds=45, rc=True)

mp, qe, r_i3, B_i3 = 1.6e-27, 1.6e-19, 0.10, 0.5
p_i3 = qe * B_i3 * r_i3
K_keV = p_i3 ** 2 / (2 * mp) / qe / 1e3
close(K_keV, 125)
close(2 * K_keV, 250)
q(MAG, "Force on charges and conductors", "Intermediate", "numerical",
  "A proton (mass 1.6 × 10⁻²⁷ kg, charge 1.6 × 10⁻¹⁹ C) moves in a circle of radius 10 cm at right angles to a "
  "uniform magnetic field of 0.5 T. Its kinetic energy is:",
  *opt("125 keV", ["250 keV", "62.5 keV", "12.5 keV"], "A"),
  "r = mv/(qB) → p = qBr; K = p²/(2m)",
  "The radius fixes the momentum: p = qBr. The kinetic energy follows from K = p²/2m and is converted to eV by "
  "dividing by e.",
  ["p = 1.6 × 10⁻¹⁹ × 0.5 × 0.10 = 8 × 10⁻²¹ kg m/s",
   "K = (8 × 10⁻²¹)²/(2 × 1.6 × 10⁻²⁷) = 2 × 10⁻¹⁴ J", "K = 2 × 10⁻¹⁴/1.6 × 10⁻¹⁹ eV = 1.25 × 10⁵ eV = 125 keV"],
  why="250 keV uses K = p²/m (no factor ½). 62.5 keV halves the answer again. 12.5 keV is a slip of a factor of 10.",
  ncert=MCC + "motion in a magnetic field", seconds=70, rc=True)

q(MAG, "Magnetic materials", "Intermediate", "statement_pair",
  sp("In an unmagnetised piece of ferromagnetic material, the domains are oriented at random, so that the net "
     "magnetisation of the piece is zero.",
     "When the piece is placed in an external magnetic field, the domains oriented along the field grow in size "
     "and the others tend to turn towards the field."),
  SP, sp_key(True, True),
  "Domain picture of ferromagnetism",
  "Each domain is magnetised to saturation, but in an unmagnetised sample the domain magnetisations point in random "
  "directions and cancel. An external field makes domains aligned with it grow and others rotate towards it, "
  "producing a large net magnetisation along the field.",
  ["Random domains → net M = 0 → Statement I true", "Field → aligned domains grow, others rotate → Statement II true"],
  why="Both statements are true, so every other option is wrong.",
  ncert=MMC + "ferromagnetism", seconds=35)

N_i5, A_i5, Ic_i5, B_i5 = 10, 0.01, 2.0, 0.5
m_i5 = N_i5 * Ic_i5 * A_i5
close(m_i5, 0.2)
close(m_i5 * B_i5, 0.1)
close(-m_i5 * B_i5, -0.1)
close(2 * m_i5 * B_i5, 0.2)
q(MAG, "Torque on loop and galvanometer", "Intermediate", "match_list",
  ml("A flat coil of 10 turns, each of area 0.01 m², carries a current of 2 A and is placed in a uniform magnetic "
     "field of 0.5 T. Match each quantity in List-I with its value in List-II.",
     ["Magnetic moment of the coil", "Torque on the coil when its magnetic moment is perpendicular to the field",
      "Potential energy of the coil when its magnetic moment is parallel to the field",
      "Work done by an external agent to turn the coil slowly from the parallel to the antiparallel position"],
     ["0.1 N m", "−0.1 J", "0.2 J", "0.2 A m²"]),
  *mlo("A-IV, B-I, C-II, D-III",
       ["A-IV, B-III, C-II, D-I", "A-IV, B-I, C-III, D-II", "A-III, B-I, C-II, D-IV"], "C"),
  "m = NIA; τ = mB sin θ; U = −mB cos θ; W = U_final − U_initial",
  "m = 10 × 2 × 0.01 = 0.2 A m². The torque is largest, mB = 0.1 N m, at θ = 90°. U = −mB = −0.1 J at θ = 0. "
  "Turning to θ = 180° raises U to +0.1 J, so the work needed is 0.2 J.",
  ["A: m = NIA = 0.2 A m² → IV", "B: τ = mB = 0.1 N m → I", "C: U = −mB = −0.1 J → II",
   "D: W = (+mB) − (−mB) = 2mB = 0.2 J → III"],
  why="B-III gives the torque the value 2mB. C-III with D-II gives the potential energy and the work each other's "
      "values. A-III gives the magnetic moment the unit of work.",
  ncert=MCC + "torque on current loop, magnetic dipole", seconds=60)

ms_mag1 = {"a": True, "b": True, "c": False, "d": True, "e": False}
q(MAG, "Force on charges and conductors", "Intermediate", "multi_statement",
  ms("Two long, straight, parallel wires carry steady currents. Which of the following statements are correct?",
     ["If the currents are in the same direction, the wires attract each other.",
      "If the currents are in opposite directions, the wires repel each other.",
      "The force per unit length between them is inversely proportional to the square of the distance between them.",
      "The forces the two wires exert on each other are equal in magnitude even when the currents are unequal.",
      "The wire carrying the larger current experiences the larger force."]),
  *mso(ms_mag1, "abd", ["abc", "ade", "bce"], "B"),
  "Force between parallel currents: f = µ₀I₁I₂/(2πd)",
  "Parallel currents attract and antiparallel currents repel. f = µ₀I₁I₂/(2πd) varies as 1/d, not 1/d². The "
  "expression is symmetric in I₁ and I₂, so each wire feels the same force (Newton's third law).",
  ["(a) like currents attract: true", "(b) unlike currents repel: true", "(c) f ∝ 1/d, not 1/d²: false",
   "(d) f = µ₀I₁I₂/(2πd) on each wire: true", "(e) contradicts (d): false"],
  why="Options with (c) or (e) are wrong: the force falls off as 1/d and is the same on both wires.",
  ncert=MCC + "magnetic force between two parallel currents, the ampere", seconds=45)

q(MAG, "Force on charges and conductors", "Intermediate", "assertion_reason",
  ar("A magnetic field can change the direction of motion of a charged particle but cannot change its speed.",
     "The magnetic force on a moving charged particle is always perpendicular to its velocity."),
  AR, ar_key(True, True, True),
  "Lorentz magnetic force F = q(v × B)",
  "Since F = q(v × B) is always perpendicular to v, it has no component along the velocity. It can only bend the "
  "path; the speed (and kinetic energy) stays the same. R is therefore the reason for A.",
  ["F ⊥ v always → R true", "No force component along v → speed unchanged, direction changes → A true and follows "
                            "from R"],
  why="R is exactly why the speed cannot change, so option B is wrong; both are true, so options C and D are wrong.",
  ncert=MCC + "magnetic force", seconds=35)

# ---- Advanced
v_a1, B_a1 = 1.0e6, 0.10
r_a1m = mp * v_a1 / (qe * B_a1)
t_a1 = math.pi * mp / (qe * B_a1)
close(r_a1m, 0.10)
close(2 * r_a1m, 0.20)
close(t_a1, math.pi * 1e-7)
q(MAG, "Force on charges and conductors", "Advanced", "numerical",
  "A uniform magnetic field of 0.10 T fills the whole region on one side of a plane boundary and is parallel to the "
  "boundary. A proton (mass 1.6 × 10⁻²⁷ kg, charge 1.6 × 10⁻¹⁹ C) enters the field region with a speed of "
  "1.0 × 10⁶ m/s, moving perpendicular to the boundary and perpendicular to the field. The distance between the "
  "points where it enters and leaves the field region, and the time it spends in the field, are:",
  *opt("0.20 m and π × 10⁻⁷ s", ["0.10 m and π × 10⁻⁷ s", "0.20 m and 2π × 10⁻⁷ s", "0.10 m and 2π × 10⁻⁷ s"], "B"),
  "Circular motion in B: r = mv/(qB), T = 2πm/(qB)",
  "Entering at right angles to the boundary, the proton describes a semicircle and leaves at right angles, a "
  "diameter away from the entry point, after half a period.",
  ["r = (1.6 × 10⁻²⁷ × 10⁶)/(1.6 × 10⁻¹⁹ × 0.10) = 0.10 m → separation 2r = 0.20 m",
   "t = T/2 = πm/(qB) = π × 1.6 × 10⁻²⁷/(1.6 × 10⁻²⁰) = π × 10⁻⁷ s"],
  why="0.10 m is the radius, not the diameter. 2π × 10⁻⁷ s is a full period; the proton completes only half a "
      "circle before leaving.",
  ncert=MCC + "motion in a magnetic field", seconds=90, rc=True)


def cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


# wire 1 along +x through origin, point P = (0.02, 0.02, 0): perpendicular vector from wire to P is +y
B1 = [2e-7 * 6 / 0.02 * c for c in cross((1, 0, 0), (0, 1, 0))]
# wire 2 along +y, perpendicular vector from wire to P is +x
B2 = [2e-7 * 2 / 0.02 * c for c in cross((0, 1, 0), (1, 0, 0))]
Bnet = [a + b for a, b in zip(B1, B2)]
close(Bnet[2], 4e-5)
assert Bnet[0] == 0 and Bnet[1] == 0
close(math.hypot(6e-5, 2e-5), 6.3e-5, 1e-2)
q(MAG, "Biot-Savart law", "Advanced", "numerical",
  "Two long, straight, insulated wires lie in the x-y plane, one along the x-axis carrying 6 A in the +x direction "
  "and the other along the y-axis carrying 2 A in the +y direction; they cross at the origin. Taking "
  "µ₀ = 4π × 10⁻⁷ T m A⁻¹, the magnetic field at the point (2 cm, 2 cm, 0) is:",
  *opt("4 × 10⁻⁵ T, along +z", ["8 × 10⁻⁵ T, along +z", "4 × 10⁻⁵ T, along −z", "6.3 × 10⁻⁵ T, in the x-y plane"],
       "C"),
  "B = µ₀I/(2πd) with direction from the right-hand rule; superposition",
  "Each wire is 2 cm from the point. The x-axis current (+x) produces a field along +z at a point on the +y side. "
  "The y-axis current (+y) produces a field along −z at a point on the +x side. The fields are along the same line "
  "but opposite, so they subtract.",
  ["Wire on x-axis: 2 × 10⁻⁷ × 6/0.02 = 6 × 10⁻⁵ T along +z",
   "Wire on y-axis: 2 × 10⁻⁷ × 2/0.02 = 2 × 10⁻⁵ T along −z", "Net: 4 × 10⁻⁵ T along +z"],
  why="8 × 10⁻⁵ T adds the two fields as if they were in the same direction. −z gives the direction of the weaker "
      "field. 6.3 × 10⁻⁵ T treats the fields as perpendicular vectors; both are actually perpendicular to the plane.",
  ncert=MCC + "Biot-Savart law", seconds=100, rc=True)

Lw, Iw = 1.0, 1.0
m_circle = Iw * math.pi * (Lw / (2 * math.pi)) ** 2
m_square = Iw * (Lw / 4) ** 2
close(m_circle / m_square, 4 / math.pi)
q(MAG, "Magnetic dipole and bar magnet", "Advanced", "numerical",
  "A wire of fixed length carries a fixed current. It is bent first into a single circular turn and then into a "
  "single square turn. The ratio of the magnetic moment of the circular turn to that of the square turn is:",
  *opt("4 : π", ["π : 4", "1 : 1", "2 : π"], "D"),
  "Magnetic moment of a current loop m = IA",
  "For the same length L, the circle has radius L/(2π) and area L²/(4π); the square has side L/4 and area L²/16. "
  "With the same current, the moments are in the ratio of the areas.",
  ["m_circle = I × L²/(4π)", "m_square = I × L²/16", "ratio = 16/(4π) = 4/π (≈ 1.27)"],
  shortcut="For a given perimeter the circle encloses the largest area, so the ratio must exceed 1.",
  why="π : 4 inverts the ratio and would make the square's moment larger. 1 : 1 ignores the different areas. 2 : π "
      "uses the wrong area for one shape.",
  ncert=MCC + "the magnetic dipole", seconds=75, rc=True)

q(MAG, "Force on charges and conductors", "Advanced", "assertion_reason",
  ar("If a charged particle passes through a region of space without any deflection, the magnetic field in that "
     "region must be zero.",
     "The magnetic force on a charged particle moving parallel to the magnetic field is zero."),
  AR, ar_key(False, True),
  "Conditions for zero magnetic force",
  "F = q(v × B) is zero when v is parallel or antiparallel to B, so a particle can cross a non-zero magnetic field "
  "undeflected (R true). Undeflected motion is also possible when an electric force balances the magnetic force, as "
  "in crossed fields. So no deflection does not mean B = 0 (A false).",
  ["v ∥ B → v × B = 0 → R true", "Undeflected motion possible with B ≠ 0 → A false"],
  why="A is false, so options A, B and C, which need A to be true, are wrong.",
  ncert=MCC + "magnetic force", seconds=45)

ms_mag2 = {"a": True, "b": True, "c": True, "d": True, "e": False}
q(MAG, "Force on charges and conductors", "Advanced", "multi_statement",
  ms("A proton and an electron enter the same uniform magnetic field with equal speeds, each moving at right angles "
     "to the field. Which of the following statements are correct?",
     ["The radius of the proton's circular path is larger than that of the electron's.",
      "The proton takes longer than the electron to complete one revolution.",
      "The proton and the electron go round their circles in opposite senses.",
      "The magnitudes of the magnetic forces on the proton and the electron are equal.",
      "The kinetic energy of each particle increases while it moves in the field."]),
  *mso(ms_mag2, "abcd", ["abc", "ace", "bcde"], "A"),
  "r = mv/(qB), T = 2πm/(qB), F = qvB; the magnetic force does no work",
  "Both have the same |q|, v and B. So F = |q|vB is the same for both. r and T are proportional to m, and the proton "
  "is about 1836 times heavier, so both are larger for the proton. Opposite charges are bent in opposite senses. "
  "The magnetic force is perpendicular to v, so kinetic energies stay constant.",
  ["(a) r ∝ m: true", "(b) T ∝ m: true", "(c) opposite charges → opposite senses: true",
   "(d) F = |q|vB same: true", "(e) no work done → KE constant: false"],
  why="(a), (b) and (c) only leaves out the true statement (d). The other options include (e), which is false.",
  ncert=MCC + "motion in a magnetic field", seconds=70)

# ================================================================ Electromagnetic Induction and AC (B4 I5 A4)
EIC = NC + "'Electromagnetic Induction', "
ACC = NC + "'Alternating Current', "

# ---- Basic
I0_b1, R_b1 = 2.0, 100.0
P_b1 = I0_b1 ** 2 * R_b1 / 2
close(P_b1, 200)
close(I0_b1 ** 2 * R_b1, 400)
close((I0_b1 / 2) ** 2 * R_b1, 100)
close(I0_b1 * R_b1 * I0_b1 / math.sqrt(2), 282.8, 1e-3)
q(EMI, "AC: rms, reactance and impedance", "Basic", "numerical",
  "An alternating current i = 2 sin ωt (in amperes) flows through a 100 Ω resistor. The average power dissipated "
  "in the resistor is:",
  *opt("200 W", ["400 W", "100 W", "283 W"], "B"),
  "Average power in a resistor: P = I_rms²R = I₀²R/2",
  "The average of sin²ωt over a cycle is ½, so the average power is half the peak power I₀²R.",
  ["I_rms = 2/√2 = √2 A", "P = I_rms²R = 2 × 100 = 200 W"],
  why="400 W is the peak power I₀²R. 100 W takes I_rms = I₀/2. 283 W multiplies the peak voltage by the rms "
      "current.",
  ncert=ACC + "AC voltage applied to a resistor", seconds=35, rc=True)

M_b2, dI_b2, dt_b2 = 0.5, 4.0, 0.02
close(M_b2 * dI_b2 / dt_b2, 100)
close(M_b2 * dI_b2, 2)
close(dI_b2 / (M_b2 * dt_b2), 400)
q(EMI, "Self and mutual inductance", "Basic", "numerical",
  "The mutual inductance of a pair of coils is 0.5 H. The current in one coil rises steadily from 0 to 4 A in "
  "0.02 s. The magnitude of the emf induced in the other coil is:",
  *opt("100 V", ["2 V", "50 V", "400 V"], "D"),
  "Mutual induction: ε₂ = M dI₁/dt",
  "The emf in the second coil equals the mutual inductance times the rate of change of current in the first.",
  ["dI₁/dt = 4/0.02 = 200 A/s", "ε = 0.5 × 200 = 100 V"],
  why="2 V is MΔI, leaving out the time. 50 V halves the answer. 400 V divides by M instead of multiplying.",
  ncert=EIC + "mutual inductance", seconds=30, rc=True)

q(EMI, "Faraday's and Lenz's laws", "Basic", "direct",
  "Which one of the following does NOT make use of eddy currents?",
  *opt("The heating element of an electric iron",
       ["Magnetic braking in some electric trains", "Electromagnetic damping in a galvanometer",
        "An induction furnace used to melt metals"], "C"),
  "Applications of eddy currents",
  "Magnetic braking, electromagnetic damping and induction furnaces all depend on currents induced in bulk metal by "
  "a changing magnetic flux. The heating element of an iron is heated by the current supplied to it through its "
  "terminals (Joule heating), not by induction.",
  ["Braking, damping, induction furnace → eddy currents", "Iron's element → ordinary Joule heating"],
  why="The other three are standard applications of eddy currents listed in the textbook.",
  ncert=EIC + "eddy currents", seconds=25)

q(EMI, "Faraday's and Lenz's laws", "Basic", "match_list",
  ml("Match each description in List-I with the law or phenomenon in List-II.",
     ["The rule that gives the direction of the induced current",
      "The law that gives the magnitude of the induced emf as the rate of change of magnetic flux linkage",
      "Emf induced in a coil by a change of current in the same coil",
      "Emf induced in a coil by a change of current in a neighbouring coil"],
     ["Mutual induction", "Lenz's law", "Self-induction", "Faraday's law of induction"]),
  *mlo("A-II, B-IV, C-III, D-I",
       ["A-IV, B-II, C-III, D-I", "A-II, B-IV, C-I, D-III", "A-IV, B-II, C-I, D-III"], "A"),
  "Faraday's law, Lenz's law, self- and mutual induction",
  "Faraday's law gives the magnitude ε = −dΦ/dt (with N turns, −N dΦ/dt); Lenz's law fixes the direction (the "
  "minus sign). A coil's own changing current induces an emf in it (self-induction); a neighbour's changing current "
  "induces one by mutual induction.",
  ["A: direction → Lenz's law (II)", "B: magnitude → Faraday's law (IV)", "C: same coil → self-induction (III)",
   "D: neighbouring coil → mutual induction (I)"],
  why="Codes with A-IV and B-II swap Faraday's and Lenz's laws. Codes with C-I and D-III swap self- and mutual "
      "induction.",
  ncert=EIC + "Faraday's law, Lenz's law, inductance", seconds=35)

# ---- Intermediate
N_i0, phi_i0, I_i0 = 500, 2e-4, 2.0
close(N_i0 * phi_i0 / I_i0, 0.05)
close(phi_i0 / I_i0, 1e-4)
close(N_i0 * phi_i0 * I_i0, 0.2)
close(N_i0 * phi_i0, 0.1)
q(EMI, "Self and mutual inductance", "Intermediate", "numerical",
  "A coil of 500 turns carries a steady current of 2.0 A, and the magnetic flux through each of its turns is "
  "2.0 × 10⁻⁴ Wb. The self-inductance of the coil is:",
  *opt("50 mH", ["0.1 mH", "200 mH", "100 mH"], "C"),
  "Self-inductance from flux linkage: NΦ = LI",
  "The total flux linked with the coil is N times the flux through one turn, and L is the flux linkage per unit "
  "current.",
  ["NΦ = 500 × 2.0 × 10⁻⁴ = 0.1 Wb", "L = NΦ/I = 0.1/2.0 = 0.05 H = 50 mH"],
  why="0.1 mH leaves out the number of turns. 200 mH multiplies the flux linkage by I instead of dividing. 100 mH is "
      "the flux linkage itself, forgetting to divide by I.",
  ncert=EIC + "self-inductance", seconds=40, rc=True)

Vp_i1, Ip_i1, eta_i1, Vs_i1 = 220, 5.0, 0.90, 330
Is_i1 = eta_i1 * Vp_i1 * Ip_i1 / Vs_i1
close(Is_i1, 3.0)
close(Vp_i1 * Ip_i1 / Vs_i1, 3.333, 1e-3)
close(0.9 * Is_i1, 2.7)
close(Ip_i1 * Vs_i1 / Vp_i1, 7.5)
q(EMI, "AC generator and transformer", "Intermediate", "numerical",
  "The primary coil of a transformer is connected to a 220 V AC supply and draws a current of 5.0 A. The secondary "
  "voltage is 330 V. If the efficiency of the transformer (output power/input power) is 90%, the current in the "
  "secondary is:",
  *opt("3.0 A", ["3.3 A", "2.7 A", "7.5 A"], "A"),
  "Power balance in a transformer with losses",
  "Input power = V_pI_p. Only 90% of it appears at the output, and the output power is V_sI_s.",
  ["P_in = 220 × 5.0 = 1100 W", "P_out = 0.90 × 1100 = 990 W", "I_s = 990/330 = 3.0 A"],
  why="3.3 A treats the transformer as ideal (100% efficient). 2.7 A applies the 90% twice. 7.5 A uses I_s/I_p = "
      "V_s/V_p, the inverse of the correct relation.",
  ncert=ACC + "transformers", seconds=50, rc=True)

e0_i2, f_i2 = 200, 50
q(EMI, "AC generator and transformer", "Intermediate", "numerical",
  "An AC generator produces an emf of peak value 200 V and frequency 50 Hz. If the speed of rotation of its coil is "
  "doubled, everything else being unchanged, the peak emf and the frequency become:",
  *opt("400 V and 100 Hz", ["200 V and 100 Hz", "400 V and 50 Hz", "800 V and 100 Hz"], "B"),
  "Generator emf ε = NBAω sin ωt",
  "Both the peak emf NBAω and the frequency ω/2π are proportional to the angular speed of the coil, so doubling the "
  "speed doubles both.",
  ["ε₀ = NBAω → 2ω gives 2ε₀ = 400 V", "f = ω/2π → 2f = 100 Hz"],
  why="200 V and 100 Hz forgets that the peak emf contains ω. 400 V and 50 Hz forgets that the frequency is set by "
      "the rotation. 800 V treats the peak emf as proportional to ω².",
  ncert=EIC + "AC generator", seconds=35, rc=True)
assert 2 * e0_i2 == 400 and 2 * f_i2 == 100

L_i3, t_i3 = 0.5, 4.0
i_t = lambda t: 3 * t ** 2
didt = 6 * t_i3
close(L_i3 * didt, 12)
close(L_i3 * i_t(t_i3), 24)
close(L_i3 * i_t(t_i3) / t_i3, 6)
close(L_i3 * 6, 3)
q(EMI, "Self and mutual inductance", "Intermediate", "numerical",
  "The current in a coil of self-inductance 0.5 H varies with time as i = 3t², where i is in amperes and t in "
  "seconds. The magnitude of the self-induced emf in the coil at t = 4 s is:",
  *opt("12 V", ["24 V", "6 V", "3 V"], "D"),
  "Self-induced emf ε = L di/dt",
  "The emf depends on the instantaneous rate of change of the current, found by differentiating i(t).",
  ["di/dt = 6t = 24 A/s at t = 4 s", "ε = 0.5 × 24 = 12 V"],
  why="24 V multiplies L by the current (48 A) instead of its rate of change. 6 V uses the average rate i/t. 3 V "
      "uses the coefficient 6 without the factor t.",
  ncert=EIC + "self-inductance", seconds=45, rc=True)

q(EMI, "Faraday's and Lenz's laws", "Intermediate", "statement_pair",
  sp("A metal plate swinging between the poles of a magnet is damped by eddy currents, and cutting slots in the "
     "plate reduces this damping.",
     "Induction furnaces use the heat produced by large eddy currents to melt metals."),
  SP, sp_key(True, True),
  "Eddy currents: damping and heating",
  "Eddy currents induced in the swinging plate oppose its motion (Lenz's law). Slots break up the paths available "
  "for the currents, so the currents and the damping are much smaller. In an induction furnace a high-frequency "
  "alternating field induces large eddy currents in the metal, whose Joule heating melts it.",
  ["Slots reduce the area for eddy currents → less damping → Statement I true",
   "Induction furnace → eddy-current heating → Statement II true"],
  why="Both statements are true, so every other option is wrong.",
  ncert=EIC + "eddy currents", seconds=35)

# ---- Advanced
Vdc, Idc, Vac, Iac, f_a1 = 100, 2.0, 100, 1.0, 50
R_a1c = Vdc / Idc
Z_a1 = Vac / Iac
XL_a1 = math.sqrt(Z_a1 ** 2 - R_a1c ** 2)
L_a1 = XL_a1 / (2 * math.pi * f_a1)
close(L_a1, 0.2757, 1e-3)
close(Z_a1 / (2 * math.pi * f_a1), 0.318, 1e-2)
close(R_a1c / (2 * math.pi * f_a1), 0.159, 1e-2)
close(XL_a1 / (50 * math.pi), 0.551, 1e-2)
q(EMI, "AC: rms, reactance and impedance", "Advanced", "numerical",
  "A coil draws a current of 2.0 A when connected to a 100 V DC supply, and a current of 1.0 A (rms) when connected "
  "to a 100 V (rms), 50 Hz AC supply. The self-inductance of the coil is about:",
  *opt("0.28 H", ["0.32 H", "0.16 H", "0.55 H"], "C"),
  "A coil = resistance R in series with inductance L; Z = √(R² + X_L²)",
  "On DC (steady current) the inductance plays no part, so the DC data give R. The AC data give the impedance; the "
  "inductive reactance is the remaining part, and L = X_L/(2πf).",
  ["R = 100/2.0 = 50 Ω", "Z = 100/1.0 = 100 Ω", "X_L = √(100² − 50²) = 86.6 Ω",
   "L = 86.6/(2π × 50) = 0.28 H"],
  why="0.32 H takes the whole impedance as the reactance. 0.16 H divides the resistance by ω. 0.55 H uses ω = 50π "
      "instead of 100π.",
  ncert=ACC + "series LCR circuit, impedance", seconds=100, rc=True)

Pb, Vb, Vs_a2, f_a2 = 50, 100, 200, 50
Rb = Vb ** 2 / Pb
Ib = Pb / Vb
VC = math.sqrt(Vs_a2 ** 2 - Vb ** 2)
C_a2 = Ib / (2 * math.pi * f_a2 * VC)
close(Rb, 200)
close(C_a2 * 1e6, 9.19, 1e-2)
close(Ib / (2 * math.pi * f_a2 * (Vs_a2 - Vb)) * 1e6, 15.9, 1e-2)
close(2 * C_a2 * 1e6, 18.4, 1e-2)
close(C_a2 / 2 * 1e6, 4.6, 1e-2)
q(EMI, "AC: rms, reactance and impedance", "Advanced", "numerical",
  "A bulb rated 50 W, 100 V is to be operated at its rated values from a 200 V (rms), 50 Hz AC supply by connecting "
  "a capacitor in series with it. Treating the bulb as a pure resistance, the capacitance needed is about:",
  *opt("9.2 µF", ["15.9 µF", "18.4 µF", "4.6 µF"], "A"),
  "Series RC circuit: V² = V_R² + V_C²; X_C = 1/(2πfC)",
  "At its rating the bulb takes I = P/V = 0.5 A with 100 V across it. In a series RC circuit the voltages across R "
  "and C are 90° out of phase, so they add as perpendicular phasors, not arithmetically.",
  ["I = 50/100 = 0.5 A", "V_C = √(200² − 100²) = 173 V", "X_C = 173/0.5 = 346 Ω",
   "C = 1/(2π × 50 × 346) = 9.2 × 10⁻⁶ F"],
  why="15.9 µF subtracts the voltages arithmetically (V_C = 100 V). 18.4 µF and 4.6 µF are off by a factor of 2 "
      "(using 2X_C or X_C/2).",
  ncert=ACC + "AC voltage applied to a capacitor; series circuits", seconds=110, rc=True)

ms_emi = {"a": True, "b": True, "c": True, "d": False, "e": True}
q(EMI, "AC: rms, reactance and impedance", "Advanced", "multi_statement",
  ms("An ideal capacitor is connected in a circuit. Which of the following statements are correct?",
     ["In the steady state it blocks a steady direct current but allows an alternating current to flow in the "
      "circuit.",
      "Its reactance decreases as the frequency of the AC source increases.",
      "The average power it consumes over a complete cycle of an AC source is zero.",
      "When it is connected alone across an AC source, the current lags behind the voltage by π/2.",
      "For a steady DC source (zero frequency), its reactance is infinite."]),
  *mso(ms_emi, "abce", ["abc", "bcd", "acde"], "B"),
  "Capacitor in AC: X_C = 1/(ωC); current leads by π/2",
  "X_C = 1/(ωC) falls as ω rises and becomes infinite at ω = 0, so DC is blocked once the capacitor is charged while "
  "AC keeps charging and discharging it. In a purely capacitive circuit the current leads the voltage by π/2, so "
  "the average power V_rmsI_rms cos 90° is zero.",
  ["(a) true", "(b) X_C ∝ 1/ω: true", "(c) cos φ = 0: true", "(d) current leads, not lags: false",
   "(e) ω = 0 → X_C → ∞: true"],
  why="(a), (b) and (c) only leaves out the true statement (e). The other options include (d), which is false.",
  ncert=ACC + "AC voltage applied to a capacitor", seconds=60)

q(EMI, "Faraday's and Lenz's laws", "Advanced", "assertion_reason",
  ar("If the magnetic flux through a closed coil is zero at some instant, the emf induced in the coil at that "
     "instant must also be zero.",
     "The induced emf depends on the rate of change of the magnetic flux, not on the value of the flux at that "
     "instant."),
  AR, ar_key(False, True),
  "Faraday's law ε = −dΦ/dt",
  "The emf is set by dΦ/dt. In an AC generator, the flux through the coil is zero when its plane is parallel to the "
  "field, yet that is exactly when the flux is changing fastest and the emf is maximum. So A is false and R is "
  "true.",
  ["ε = −N dΦ/dt → R true", "Φ = 0 with dΦ/dt ≠ 0 (coil plane parallel to B in a generator) → A false"],
  why="A is false, so options A, B and C, which need A to be true, are wrong.",
  ncert=EIC + "Faraday's law of induction", seconds=45)

# ================================================================ Electromagnetic Waves (B2 I2 A2)
EWC = NC + "'Electromagnetic Waves', "

q(EMW, "EM spectrum and uses", "Basic", "direct",
  "Which of the following lists parts of the electromagnetic spectrum in order of increasing frequency?",
  *opt("Radio waves, microwaves, infrared, ultraviolet",
       ["Microwaves, radio waves, ultraviolet, infrared", "Ultraviolet, infrared, microwaves, radio waves",
        "Radio waves, infrared, microwaves, ultraviolet"], "D"),
  "Order of the electromagnetic spectrum",
  "In order of decreasing wavelength (increasing frequency) the spectrum runs: radio waves, microwaves, infrared, "
  "visible, ultraviolet, X-rays, gamma rays.",
  ["Increasing frequency: radio < micro < IR < visible < UV < X < γ"],
  why="The first wrong option swaps radio waves with microwaves and UV with IR. The third is in decreasing order. "
      "The fourth puts infrared below microwaves.",
  ncert=EWC + "electromagnetic spectrum", seconds=25)

q(EMW, "EM spectrum and uses", "Basic", "assertion_reason",
  ar("Most of the ultraviolet radiation from the Sun is absorbed by the ozone layer in the atmosphere.",
     "Ultraviolet radiation has longer wavelengths than visible light."),
  AR, ar_key(True, False),
  "Ultraviolet rays",
  "The ozone layer high in the atmosphere absorbs most of the Sun's ultraviolet radiation, protecting us (A true). "
  "Ultraviolet lies beyond the violet end of the visible spectrum, so its wavelengths (about 400 nm down to "
  "about 1 nm) are shorter than those of visible light (R false).",
  ["Ozone absorbs most solar UV → A true", "UV wavelength < visible wavelength → R false"],
  why="R is false, so options A, B and D, which need R to be true, are wrong.",
  ncert=EWC + "electromagnetic spectrum - ultraviolet rays", seconds=30)

q(EMW, "EM spectrum and uses", "Intermediate", "match_list",
  ml("Match each part of the electromagnetic spectrum in List-I with a way in which it is produced (List-II).",
     ["Radio waves", "Infrared waves", "X-rays", "Gamma rays"],
     ["Emitted by atomic nuclei, for example in nuclear reactions",
      "Accelerated motion of charges in conducting wires",
      "Bombarding a metal target with high-energy electrons",
      "Hot bodies and molecules"]),
  *mlo("A-II, B-IV, C-III, D-I",
       ["A-II, B-III, C-IV, D-I", "A-IV, B-II, C-III, D-I", "A-II, B-IV, C-I, D-III"], "C"),
  "Sources of the different parts of the EM spectrum",
  "Radio waves are produced by accelerated charges in conducting wires (antennas). Infrared is emitted by hot "
  "bodies and molecules. X-rays are produced when high-energy electrons strike a metal target. Gamma rays come from "
  "atomic nuclei.",
  ["A → II", "B → IV", "C → III", "D → I"],
  why="Swapping III and IV gives infrared the X-ray tube. A-IV puts radio waves with hot bodies. C-I with D-III "
      "swaps the sources of X-rays and gamma rays.",
  ncert=EWC + "electromagnetic spectrum", seconds=40)

q(EMW, "EM wave properties", "Intermediate", "statement_pair",
  sp("A charge moving with a constant velocity radiates electromagnetic waves.",
     "A charge oscillating with some frequency produces electromagnetic waves of the same frequency."),
  SP, sp_key(False, True),
  "Sources of electromagnetic waves: accelerated charges",
  "A stationary charge produces only an electric field and a uniformly moving charge produces steady fields; "
  "neither radiates (Statement I false). An accelerated charge radiates, and an oscillating charge produces an "
  "electromagnetic wave whose frequency equals its frequency of oscillation (Statement II true).",
  ["Constant velocity → no radiation → Statement I false", "Oscillating charge → EM wave of the same frequency → "
                                                           "Statement II true"],
  why="Statement I is false, so options A and C are wrong; Statement II is true, so option B is wrong.",
  ncert=EWC + "sources of electromagnetic waves", seconds=35)

C_wa1, V0_wa1, w_wa1 = 10e-6, 100.0, 1000.0
id_max = C_wa1 * V0_wa1 * w_wa1
close(id_max, 1.0)
close(C_wa1 * V0_wa1, 1e-3)
close(id_max / math.sqrt(2), 0.707, 1e-2)
close(id_max / (2 * math.pi), 0.159, 1e-2)
q(EMW, "Displacement current", "Advanced", "numerical",
  "A 10 µF parallel-plate capacitor is connected to an AC source, and the potential difference between its plates "
  "is v = 100 sin(1000t), with v in volts and t in seconds. The maximum value of the displacement current between "
  "the plates is:",
  *opt("1.0 A", ["1.0 × 10⁻³ A", "0.71 A", "0.16 A"], "A"),
  "Displacement current i_d = ε₀ dΦ_E/dt = C dV/dt",
  "Between the plates Φ_E = q/ε₀ = CV/ε₀, so i_d = C dV/dt, equal to the conduction current in the wires.",
  ["dv/dt = 100 × 1000 cos(1000t)", "i_d = C dv/dt = 10 × 10⁻⁶ × 10⁵ cos(1000t) = 1.0 cos(1000t) A",
   "Maximum = 1.0 A"],
  why="1.0 × 10⁻³ A is CV₀, leaving out ω. 0.71 A is the rms value, not the maximum. 0.16 A divides by 2π, "
      "treating 1000 as a frequency in Hz instead of an angular frequency.",
  ncert=EWC + "displacement current", seconds=60, rc=True)

E0_wa2, k_wa2, c_light = 30.0, 2.0e7, 3.0e8
close(c_light * k_wa2, 6e15)
close(E0_wa2 / c_light, 1e-7)
close(k_wa2 / c_light, 0.0667, 1e-2)
close(E0_wa2 * c_light, 9e9)
# E along +y, propagation +z  →  B must satisfy E × B ∥ +z
assert cross((0, 1, 0), (-1, 0, 0)) == (0, 0, 1)
q(EMW, "EM wave properties", "Advanced", "numerical",
  "The electric field of a plane electromagnetic wave in vacuum is E = 30 sin(2.0 × 10⁷ z − ωt) ĵ V/m, with z in "
  "metres and t in seconds. Taking c = 3 × 10⁸ m/s, the angular frequency ω and the magnetic field of the wave are:",
  *opt("ω = 6 × 10¹⁵ rad/s; B has amplitude 1 × 10⁻⁷ T and oscillates along the x-axis",
       ["ω = 6 × 10¹⁵ rad/s; B has amplitude 1 × 10⁻⁷ T and oscillates along the z-axis",
        "ω = 6.7 × 10⁻² rad/s; B has amplitude 1 × 10⁻⁷ T and oscillates along the x-axis",
        "ω = 6 × 10¹⁵ rad/s; B has amplitude 9 × 10⁹ T and oscillates along the x-axis"], "B"),
  "Plane EM wave: ω = ck, B₀ = E₀/c, E ⊥ B ⊥ direction of propagation",
  "The phase (kz − ωt) shows the wave travels along +z with k = 2.0 × 10⁷ rad/m. In vacuum ω = ck and B₀ = E₀/c. "
  "B is perpendicular to both E (along y) and the direction of travel (z), so it lies along the x-axis; E × B "
  "must point along +z, so B is along −x when E is along +y.",
  ["ω = ck = 3 × 10⁸ × 2.0 × 10⁷ = 6 × 10¹⁵ rad/s", "B₀ = E₀/c = 30/(3 × 10⁸) = 1 × 10⁻⁷ T",
   "B ⊥ ĵ and ⊥ k̂ → along the x-axis"],
  why="B along the z-axis would be along the direction of propagation; EM waves are transverse. 6.7 × 10⁻² rad/s "
      "uses ω = k/c. 9 × 10⁹ T multiplies E₀ by c instead of dividing.",
  ncert=EWC + "electromagnetic waves", seconds=80, rc=True)

# ================================================================ Optics (B7 I9 A7)
ROC = NC + "'Ray Optics and Optical Instruments', "
WOC = NC + "'Wave Optics', "


def mirror_v(u, f):
    """Image distance from 1/v + 1/u = 1/f (Cartesian signs, distances in cm)."""
    return 1 / (F(1) / F(f) - F(1) / F(u))


# ---- Basic
assert mirror_v(-40, -20) == -40
q(OPT, "Mirrors", "Basic", "numerical",
  "A concave mirror forms a real, inverted image of the same size as the object when the object is placed 40 cm in "
  "front of the mirror. The focal length of the mirror is:",
  *opt("20 cm", ["40 cm", "10 cm", "80 cm"], "C"),
  "Image at the centre of curvature; f = R/2",
  "A concave mirror gives a real image of the same size only when the object is at the centre of curvature; the "
  "image is then also at C. So R = 40 cm and f = R/2.",
  ["Same-size real image → object at C → R = 40 cm", "f = R/2 = 20 cm",
   "Check: u = −40, f = −20 → 1/v = −1/20 + 1/40 → v = −40 cm, m = −1"],
  why="40 cm is the radius of curvature, not the focal length. 10 cm and 80 cm are off by further factors of 2.",
  ncert=ROC + "reflection of light by spherical mirrors", seconds=30, rc=True)

lam_o2, dx_o2 = 500e-9, 1.5e-6
assert round(dx_o2 / lam_o2, 9) == 3
q(OPT, "Huygens' principle and interference", "Basic", "numerical",
  "In a Young's double-slit experiment with light of wavelength 500 nm, the path difference between the waves "
  "reaching a point P on the screen from the two slits is 1.5 µm. The point P lies on:",
  *opt("the third bright fringe from the central bright fringe",
       ["the third dark fringe from the central bright fringe", "the sixth bright fringe from the central bright "
        "fringe", "the fourth dark fringe from the central bright fringe"], "D"),
  "Bright fringe: path difference = nλ",
  "Constructive interference occurs where the path difference is a whole number of wavelengths; n counts the bright "
  "fringes from the central one (n = 0).",
  ["Δ/λ = 1.5 × 10⁻⁶/(500 × 10⁻⁹) = 3", "Δ = 3λ → third bright fringe"],
  why="A dark fringe needs an odd number of half wavelengths, (n − ½)λ, but 1.5 µm is a whole number of wavelengths. "
      "'Sixth bright fringe' divides by λ/2 instead of λ.",
  ncert=WOC + "interference of light waves and Young's experiment", seconds=30, rc=True)

q(OPT, "Huygens' principle and interference", "Basic", "direct",
  "A wavefront is best described as:",
  *opt("a surface on which all points oscillate in the same phase (a surface of constant phase)",
       ["a surface on which the amplitude of the wave is zero", "the path along which the light energy travels",
        "the surface that separates two transparent media"], "A"),
  "Definition of a wavefront",
  "When a disturbance spreads from a source, the locus of points that oscillate in phase is a wavefront: a surface "
  "of constant phase. The energy travels along rays, which are perpendicular to the wavefronts.",
  ["Wavefront = locus of points in the same phase"],
  why="Zero-amplitude surfaces are not wavefronts. The path of energy is a ray, not a wavefront. A boundary between "
      "media is an interface.",
  ncert=WOC + "Huygens principle", seconds=20)

q(OPT, "Optical instruments", "Basic", "direct",
  "In a Cassegrain reflecting telescope, the light reflected by the concave primary (objective) mirror is reflected "
  "back through a hole in the primary mirror to the eyepiece by:",
  *opt("a convex secondary mirror", ["a plane mirror inclined at 45° to the axis", "a concave secondary mirror",
                                     "a convex lens placed at the focus of the primary"], "B"),
  "Reflecting telescopes: the Cassegrain arrangement",
  "In the Cassegrain design a convex secondary mirror reflects the converging light back through a hole in the "
  "primary mirror, so the image is formed behind the primary where the eyepiece and observer can be placed.",
  ["Cassegrain: concave primary + convex secondary, light through a hole in the primary"],
  why="A plane mirror at 45° sends the light sideways (the Newtonian arrangement), not back through the primary. The "
      "secondary of a Cassegrain telescope is convex, not concave, and it is a mirror, not a lens.",
  ncert=ROC + "optical instruments - telescope", seconds=25)

ng, nw = F(3, 2), F(4, 3)
assert ng / nw == F(9, 8) and nw / ng == F(8, 9) and ng - nw == F(1, 6)
q(OPT, "Refraction and lenses", "Basic", "numerical",
  "The refractive indices of glass and water with respect to air are 3/2 and 4/3 respectively. The refractive index "
  "of glass with respect to water is:",
  *opt("9/8", ["8/9", "1/6", "2"], "C"),
  "Relative refractive index n₂₁ = n₂/n₁",
  "The refractive index of medium 2 with respect to medium 1 is the ratio of their refractive indices (with "
  "respect to vacuum or air): n_gw = n_g/n_w.",
  ["n_gw = (3/2)/(4/3)", "n_gw = 9/8"],
  why="8/9 is the refractive index of water with respect to glass. 1/6 subtracts the indices. 2 multiplies them.",
  ncert=ROC + "refraction", seconds=25, rc=True)

f_o6, D_o6 = 5, 25
assert 1 + F(D_o6, f_o6) == 6 and F(D_o6, f_o6) == 5
q(OPT, "Optical instruments", "Basic", "numerical",
  "A simple microscope consists of a convex lens of focal length 5 cm. When the final image is formed at the least "
  "distance of distinct vision (25 cm), its magnifying power is:",
  *opt("6", ["5", "4", "0.2"], "B"),
  "Simple microscope with image at the near point: m = 1 + D/f",
  "With the image at the near point D, the angular magnification is 1 + D/f; with the image at infinity it is D/f.",
  ["m = 1 + 25/5 = 6"],
  why="5 is the magnifying power with the final image at infinity. 4 uses D/f − 1. 0.2 inverts D/f.",
  ncert=ROC + "optical instruments - the microscope", seconds=25, rc=True)

q(OPT, "Mirrors", "Basic", "statement_pair",
  sp("For a spherical mirror of small aperture, the focal length is half the radius of curvature.",
     "A concave mirror forms a virtual image of a real object only when the object lies between its focus and its "
     "pole."),
  SP, sp_key(True, True),
  "f = R/2; images formed by a concave mirror",
  "For paraxial rays a spherical mirror has f = R/2 (Statement I true). For a concave mirror, a real object beyond "
  "F gives a real image (at infinity when the object is at F); only an object between F and P gives a virtual, "
  "erect, magnified image (Statement II true).",
  ["f = R/2 → Statement I true", "Virtual image only for object between P and F → Statement II true"],
  why="Both statements are true, so every other option is wrong.",
  ncert=ROC + "reflection of light by spherical mirrors", seconds=30)

# ---- Intermediate
v_o8 = mirror_v(-10, -15)
assert v_o8 == 30 and -v_o8 / F(-10) == 3
assert mirror_v(-20, -15) == -60
q(OPT, "Mirrors", "Intermediate", "numerical",
  "A concave mirror of focal length 15 cm forms a virtual, erect image three times the size of an object placed in "
  "front of it. The distance of the object from the mirror is:",
  *opt("10 cm", ["20 cm", "5 cm", "45 cm"], "A"),
  "Mirror formula with magnification m = −v/u",
  "A virtual erect image has m = +3, so v = −3u (image behind the mirror). Substituting in the mirror formula gives "
  "u.",
  ["Let u = −x, v = +3x; f = −15", "1/(3x) − 1/x = −1/15 → −2/(3x) = −1/15 → x = 10 cm",
   "Check: u = −10 → v = +30 cm, m = −v/u = +3"],
  why="20 cm gives a real, inverted image of magnification −3 (v = −60 cm). 5 cm gives magnification 1.5. 45 cm "
      "multiplies the focal length by 3.",
  ncert=ROC + "mirror equation, magnification", seconds=60, rc=True)

R_o9, mu_o9 = 20, F(3, 2)  # equiconvex lens with f = 20 cm needs R = 2f(n−1) = 20 cm
f_bi = 1 / ((mu_o9 - 1) * (F(1, R_o9) + F(1, R_o9)))
f_half = 1 / ((mu_o9 - 1) * F(1, R_o9))
assert f_bi == 20 and f_half == 40
q(OPT, "Refraction and lenses", "Intermediate", "numerical",
  "A thin equiconvex lens has a focal length of 20 cm. It is cut into two identical halves by a plane perpendicular "
  "to its principal axis, passing through its optical centre, so that each half is a plano-convex lens. The focal "
  "length of each half is:",
  *opt("40 cm", ["20 cm", "10 cm", "80 cm"], "D"),
  "Lens maker's formula 1/f = (n − 1)(1/R₁ − 1/R₂)",
  "For the equiconvex lens both surfaces contribute equally: 1/f = (n − 1)(2/R). Each plano-convex half keeps only "
  "one curved surface (the other is plane, 1/R = 0), so its power is half.",
  ["Whole lens: 1/20 = (n − 1)(2/R)", "Half: 1/f' = (n − 1)(1/R) = 1/40 → f' = 40 cm"],
  shortcut="Two halves in contact rebuild the lens: P = P₁ + P₂ → each half has half the power.",
  why="20 cm would be the answer if the lens were cut along the principal axis (each half keeps both curved "
      "surfaces). 10 cm doubles the power instead of halving it. 80 cm halves it twice.",
  ncert=ROC + "refraction by a lens, lens maker's formula", seconds=60, rc=True)

lam_o10 = 650e-9
a_o10 = lam_o10 / math.sin(math.radians(30))
close(a_o10, 1.3e-6)
close(lam_o10, 0.65e-6)
close(2 * a_o10, 2.6e-6)
q(OPT, "Diffraction", "Intermediate", "numerical",
  "Light of wavelength 650 nm falls normally on a single slit. The first minimum of the diffraction pattern is "
  "observed at an angle of 30° from the central direction. The width of the slit is:",
  *opt("1.3 µm", ["0.65 µm", "2.6 µm", "0.33 µm"], "B"),
  "First minimum of single-slit diffraction: a sin θ = λ",
  "The first dark direction of a single slit satisfies a sin θ = λ. With θ = 30° the slit width is twice the "
  "wavelength.",
  ["a = λ/sin 30° = 650 nm/0.5", "a = 1300 nm = 1.3 µm"],
  why="0.65 µm takes a = λ (θ = 90°). 2.6 µm uses a sin θ = 2λ (the second minimum). 0.33 µm uses a sin θ = λ/2.",
  ncert=WOC + "diffraction - the single slit", seconds=45, rc=True)

f_o11, th_deg = 1.0, 0.5
d_img = f_o11 * math.radians(th_deg)
close(d_img, 8.73e-3, 1e-2)
close(2 * d_img, 17.5e-3, 1e-2)
close(d_img / 2, 4.4e-3, 1e-2)
q(OPT, "Mirrors", "Intermediate", "numerical",
  "A concave mirror of focal length 1.0 m forms an image of the Sun. The Sun's disc subtends an angle of 0.5° at the "
  "mirror. The diameter of the image of the Sun is about:",
  *opt("8.7 mm", ["17 mm", "4.4 mm", "0.50 m"], "C"),
  "Image of a distant object forms in the focal plane; size = f × angle (in radians)",
  "Rays from the two edges of the Sun's disc arrive as parallel beams inclined at 0.5°. Each beam focuses in the "
  "focal plane, so the image diameter is f times the angle in radians.",
  ["θ = 0.5° = 0.5 × π/180 = 8.73 × 10⁻³ rad", "d = fθ = 1.0 × 8.73 × 10⁻³ m ≈ 8.7 mm"],
  why="17 mm uses the radius of curvature (2 m) instead of f. 4.4 mm halves the angle. 0.50 m uses the angle in "
      "degrees instead of radians.",
  ncert=ROC + "reflection of light by spherical mirrors", seconds=60, rc=True)

n_core, n_clad = 1.60, 1.20
C_o12 = math.degrees(math.asin(n_clad / n_core))
close(C_o12, 48.6, 1e-2)
close(90 - C_o12, 41.4, 1e-2)
close(math.degrees(math.asin(1 / n_core)), 38.7, 1e-2)
close(math.degrees(math.asin(1 / n_clad)), 56.4, 1e-2)
q(OPT, "Total internal reflection", "Intermediate", "numerical",
  "In an optical fibre, the core has a refractive index of 1.60 and the cladding a refractive index of 1.20. The "
  "critical angle at the core–cladding boundary is about:",
  *opt("49°", ["41°", "39°", "56°"], "B"),
  "Critical angle between two media: sin C = n_rarer/n_denser",
  "Light inside the core meets the cladding; total internal reflection needs the angle of incidence to exceed C, "
  "where sin C = n_cladding/n_core.",
  ["sin C = 1.20/1.60 = 0.75", "C = sin⁻¹ 0.75 ≈ 48.6° ≈ 49°"],
  why="41° is 90° − C. 39° is the critical angle for a core–air boundary (sin C = 1/1.60). 56° is the critical "
      "angle for a cladding–air boundary (sin C = 1/1.20).",
  ncert=ROC + "total internal reflection - optical fibres", seconds=45, rc=True)

q(OPT, "Refraction and lenses", "Intermediate", "match_list",
  ml("A real object is placed on the principal axis of a thin lens of focal length f. Match the situation in List-I "
     "with the image in List-II.",
     ["Convex lens, object at a distance 2f from the lens",
      "Convex lens, object between the focus and the optical centre",
      "Convex lens, object very far away (practically at infinity)",
      "Concave lens, object at any distance"],
     ["Virtual, erect, magnified, on the same side as the object",
      "Virtual, erect, diminished, between the optical centre and the focus on the object side",
      "Real, inverted, same size, at 2f on the other side",
      "Real, inverted, highly diminished, at the focus"]),
  *mlo("A-III, B-I, C-IV, D-II",
       ["A-IV, B-I, C-III, D-II", "A-III, B-II, C-IV, D-I", "A-III, B-I, C-II, D-IV"], "D"),
  "Images formed by thin lenses (1/v − 1/u = 1/f)",
  "For a convex lens: object at 2f → image at 2f, same size, real, inverted; object within f → virtual, erect, "
  "magnified on the object side; object at infinity → point image at F. A concave lens always gives a virtual, "
  "erect, diminished image between the lens and its focus for a real object.",
  ["A → III", "B → I", "C → IV", "D → II"],
  why="A-IV/C-III swaps the 2f and infinity cases. B-II/D-I swaps the convex lens (magnified) with the concave lens "
      "(diminished). C-II/D-IV gives the concave lens a real image, which it cannot form for a real object.",
  ncert=ROC + "refraction by a lens", seconds=55)

ms_o14 = {"a": True, "b": True, "c": True, "d": False, "e": False}
q(OPT, "Prism", "Intermediate", "multi_statement",
  ms("A ray of light passes through an equilateral glass prism (angle A = 60°). Which of the following statements are correct?",
     ["At minimum deviation, the angles of refraction at the two faces are equal, each being A/2.",
      "At minimum deviation, the angle of incidence equals the angle of emergence.",
      "At minimum deviation, the refracted ray inside the prism is parallel to the base of the prism.",
      "The angle of minimum deviation does not depend on the refractive index of the prism material.",
      "For a given prism material, the angle of minimum deviation does not depend on the angle A of the prism."]),
  *mso(ms_o14, "abc", ["ab", "abcd", "bce"], "A"),
  "Refraction through a prism: r₁ + r₂ = A; δ = i + e − A; minimum deviation",
  "At minimum deviation the path is symmetric: i = e and r₁ = r₂ = A/2, so the ray inside travels parallel to the "
  "base. From n = sin[(A + D_m)/2]/sin(A/2), D_m depends both on n and on A.",
  ["(a) r₁ = r₂ = A/2: true", "(b) i = e: true", "(c) symmetric path → parallel to base: true",
   "(d) D_m depends on n: false", "(e) D_m depends on A: false"],
  why="(a) and (b) only leaves out the true statement (c). Options with (d) or (e) are wrong because D_m depends on "
      "both n and A.",
  ncert=ROC + "refraction through a prism", seconds=55)

q(OPT, "Refraction and lenses", "Intermediate", "assertion_reason",
  ar("A tank filled with water appears shallower than it really is when viewed from directly above.",
     "Light from the bottom bends away from the normal as it passes from water into air, so the rays reaching the "
     "eye appear to come from a point above the bottom."),
  AR, ar_key(True, True, True),
  "Apparent depth due to refraction",
  "Rays from a point on the bottom refract away from the normal at the water surface (water is denser than air). "
  "Traced back, the emerging rays meet at a point above the real one, so the bottom seems raised: apparent depth = "
  "real depth/n. R is the reason for A.",
  ["Water → air: ray bends away from the normal → R true", "Backward extensions meet above the bottom → A true, "
                                                           "explained by R"],
  why="R gives the mechanism of A, so option B is wrong; both statements are true, so options C and D are wrong.",
  ncert=ROC + "refraction", seconds=35)

crit = {"2": 2.0, "√2": math.sqrt(2), "1.25": 1.25, "2/√3": 2 / math.sqrt(3)}
angles = {k: math.degrees(math.asin(1 / v)) for k, v in crit.items()}
close(angles["2"], 30)
close(angles["√2"], 45)
close(angles["1.25"], 53.13, 1e-3)
close(angles["2/√3"], 60)
q(OPT, "Total internal reflection", "Intermediate", "match_list",
  ml("Light travels from each medium in List-I into air. Match the refractive index of the medium with the critical "
     "angle in List-II.",
     ["n = 2", "n = √2", "n = 1.25", "n = 2/√3"],
     ["45°", "60°", "30°", "about 53°"]),
  *mlo("A-III, B-I, C-IV, D-II",
       ["A-II, B-I, C-IV, D-III", "A-III, B-IV, C-I, D-II", "A-III, B-I, C-II, D-IV"], "B"),
  "sin C = 1/n for a medium–air boundary",
  "The critical angle is the angle of incidence in the denser medium for which the refracted ray grazes the surface: "
  "sin C = 1/n. A larger n gives a smaller C.",
  ["A: sin C = 1/2 → 30° (III)", "B: sin C = 1/√2 → 45° (I)", "C: sin C = 0.8 → 53° (IV)",
   "D: sin C = √3/2 → 60° (II)"],
  why="A-II/D-III uses cos C = 1/n. B-IV/C-I swaps the critical angles of n = √2 and n = 1.25. C-II/D-IV swaps "
      "those of n = 1.25 and n = 2/√3; in each case a larger index would get a larger critical angle.",
  ncert=ROC + "total internal reflection", seconds=45)

# ---- Advanced
A_o17, n_o17, i_o17 = 75.0, math.sqrt(2), 45.0
r1 = math.degrees(math.asin(math.sin(math.radians(i_o17)) / n_o17))
r2 = A_o17 - r1
s_e = n_o17 * math.sin(math.radians(r2))
close(r1, 30)
close(r2, 45)
close(s_e, 1.0)
e_o17 = 90.0
close(i_o17 + e_o17 - A_o17, 60)
close(math.degrees(math.asin(1 / n_o17)), r2)
q(OPT, "Prism", "Advanced", "numerical",
  "A ray of light is incident at 45° on one refracting face of a prism of angle 75°, made of glass of refractive "
  "index √2. Which statement correctly describes what happens at the second refracting face?",
  *opt("The ray emerges grazing along the second face, and the total deviation is 60°",
       ["The ray is totally reflected back into the prism at the second face, since the angle of incidence there "
        "exceeds the critical angle",
        "The ray emerges at 45° to the normal, and the total deviation is 15°",
        "The ray emerges grazing along the second face, and the total deviation is 135°"], "C"),
  "Prism relations r₁ + r₂ = A and δ = i + e − A; critical angle",
  "Snell's law at the first face gives r₁; then r₂ = A − r₁. Compare r₂ with the critical angle (sin C = 1/√2, "
  "C = 45°). Here r₂ equals C exactly, so the emergent ray grazes the surface (e = 90°).",
  ["sin r₁ = sin 45°/√2 = 1/2 → r₁ = 30°", "r₂ = 75° − 30° = 45° = C",
   "sin e = √2 sin 45° = 1 → e = 90° (grazing emergence)", "δ = i + e − A = 45° + 90° − 75° = 60°"],
  why="Total reflection would need r₂ to exceed 45°; it only equals it. Emergence at 45° wrongly takes e = r₂. A "
      "deviation of 135° forgets to subtract the prism angle.",
  ncert=ROC + "refraction through a prism", seconds=110, rc=True)

I0 = F(1)
I_out = I0 / 2 * F(3, 4) * F(1, 4)  # cos²30° = 3/4, cos²60° = 1/4
assert I_out == F(3, 32)
assert I0 * F(3, 4) * F(1, 4) == F(3, 16)
assert I0 / 2 * F(3, 4) * F(3, 4) == F(9, 32)
q(OPT, "Polarisation", "Advanced", "numerical",
  "Unpolarised light of intensity I₀ passes through three ideal polaroids P₁, P₂ and P₃ in that order. The pass "
  "axis of P₂ makes an angle of 30° with that of P₁, and the pass axis of P₃ is perpendicular to that of P₁. The "
  "intensity of the light emerging from P₃ is:",
  *opt("3I₀/32", ["zero", "3I₀/16", "9I₀/32"], "D"),
  "Polaroid halves unpolarised light; Malus's law I = I' cos²θ",
  "P₁ passes half of the unpolarised light. The plane-polarised light then passes P₂ (at 30°) and P₃, which is at "
  "90° − 30° = 60° to P₂, each time reduced by cos² of the angle between successive axes.",
  ["After P₁: I₀/2", "After P₂: (I₀/2) cos²30° = 3I₀/8", "After P₃: (3I₀/8) cos²60° = 3I₀/32"],
  why="Zero would be correct only without P₂ (P₁ and P₃ are crossed). 3I₀/16 forgets the factor ½ at P₁. 9I₀/32 "
      "uses 30° again for P₃ instead of 60°.",
  ncert=WOC + "polarisation", seconds=80, rc=True)

R_o20, n_o20 = 20, F(3, 2)
f_l = 1 / ((n_o20 - 1) * F(1, R_o20))
P_plane = 2 / f_l + 0             # plane face silvered: mirror power 0
P_curved = 2 / f_l + F(2, R_o20)  # curved face silvered: concave mirror of focal length R/2
assert f_l == 40 and 1 / P_plane == 20 and 1 / P_curved == F(20, 3)
q(OPT, "Refraction and lenses", "Advanced", "numerical",
  "A thin plano-convex lens of glass (refractive index 1.5) has a curved surface of radius of curvature 20 cm. Its "
  "plane surface is silvered, and light is incident on the curved surface. The system behaves as a concave mirror "
  "of focal length:",
  *opt("20 cm", ["40 cm", "6.7 cm", "10 cm"], "A"),
  "Silvered lens: P = 2P_lens + P_mirror",
  "Light passes through the lens, is reflected by the silvered surface and passes through the lens again, so the "
  "lens power counts twice. A plane mirror has zero power.",
  ["f_lens = R/(n − 1) = 20/0.5 = 40 cm", "P = 2/40 + 0 = 1/20 per cm", "Equivalent concave mirror: f = 20 cm"],
  why="40 cm is the focal length of the lens alone. 6.7 cm is the result when the curved surface is silvered "
      "(P = 2/40 + 2/20). 10 cm is R/2 of the curved surface used as a mirror alone.",
  seconds=90, rc=True)

q(OPT, "Optical instruments", "Advanced", "statement_pair",
  sp("The magnifying power of an astronomical telescope in normal adjustment can be increased by using an objective "
     "of smaller focal length, the eyepiece being unchanged.",
     "The magnifying power of a compound microscope increases if the focal length of its objective is increased, "
     "other things remaining unchanged."),
  SP, sp_key(False, False),
  "Magnifying powers: telescope f_o/f_e; microscope (L/f_o)(D/f_e)",
  "A telescope in normal adjustment has m = f_o/f_e, so a larger, not smaller, objective focal length increases m "
  "(Statement I false). A compound microscope has m ≈ (L/f_o)(D/f_e), so increasing f_o decreases m (Statement II "
  "false). The two instruments need opposite choices of objective.",
  ["Telescope m = f_o/f_e → smaller f_o reduces m → Statement I false",
   "Microscope m ∝ 1/f_o → larger f_o reduces m → Statement II false"],
  why="Both statements are false, so options A, C and D, which need at least one of them to be true, are wrong.",
  ncert=ROC + "optical instruments", seconds=45)

q(OPT, "Refraction and lenses", "Advanced", "assertion_reason",
  ar("If the lower half of a convex lens is covered with an opaque sheet, the lens still forms a complete image of "
     "an object, though the image is less bright.",
     "Rays from each point of the object pass through every part of the lens, and all of them are brought together "
     "at the image of that point."),
  AR, ar_key(True, True, True),
  "Image formation by a lens: every part of the lens forms the whole image",
  "Each object point sends rays to the whole lens surface, and all these rays converge at the corresponding image "
  "point. Covering half the lens removes half of the rays from every object point, so every image point still "
  "forms but receives less light. R is the reason for A.",
  ["Rays from every object point reach every part of the lens → R true",
   "Half the lens still forms every image point, with half the light → A true and explained by R"],
  why="R is the reason the full image survives, so option B is wrong; both statements are true, so options C and D "
      "are wrong.",
  ncert=ROC + "refraction by a lens", seconds=45)

ms_o22 = {"a": True, "b": True, "c": False, "d": True, "e": False}
q(OPT, "Huygens' principle and interference", "Advanced", "multi_statement",
  ms("In a Young's double-slit experiment with monochromatic light, the waves from the two slits reach the screen "
     "with equal intensities, each I₀. Which of the following statements are correct?",
     ["The maximum intensity on the screen is 4I₀.",
      "At a point where the phase difference between the two waves is π/2, the intensity is 2I₀.",
      "At a point where the path difference is λ/2, the intensity is 2I₀.",
      "If one slit is closed, the intensity at the position of the central bright fringe becomes I₀.",
      "The intensity averaged over many fringes is 4I₀."]),
  *mso(ms_o22, "abd", ["ab", "abde", "bcd"], "C"),
  "Resultant intensity I = 4I₀ cos²(φ/2)",
  "For two equal coherent waves, I = I₀ + I₀ + 2I₀ cos φ = 4I₀ cos²(φ/2). It is 4I₀ at φ = 0, 2I₀ at φ = π/2 and "
  "zero at φ = π (path difference λ/2). With one slit closed, only I₀ arrives. Energy is redistributed, so the "
  "average over many fringes is 2I₀, not 4I₀.",
  ["(a) φ = 0 → 4I₀: true", "(b) φ = π/2 → 4I₀ × ½ = 2I₀: true", "(c) Δ = λ/2 → φ = π → zero: false",
   "(d) one slit → I₀: true", "(e) average = 2I₀: false"],
  why="(a) and (b) only leaves out the true statement (d). The other options include (c) or (e), both false.",
  ncert=WOC + "interference of light waves and Young's experiment", seconds=75)

ms_o23 = {"a": True, "b": False, "c": True, "d": True, "e": False}
q(OPT, "Polarisation", "Advanced", "multi_statement",
  ms("Which of the following statements about polarisation and polaroids are correct?",
     ["A polaroid transmits only the component of the electric field of the light along its pass axis.",
      "Sound waves in air can be plane polarised by a suitable polariser.",
      "The light transmitted by a polaroid is plane polarised.",
      "When plane-polarised light falls on an ideal polaroid whose pass axis is parallel to the direction of "
      "vibration of its electric field, all the light is transmitted.",
      "Unpolarised light can be polarised by passing it through a polaroid, but never by reflection."]),
  *mso(ms_o23, "acd", ["ac", "abcd", "cde"], "B"),
  "Polaroids; transverse nature of light; polarisation by reflection",
  "A polaroid passes the E-component along its axis, so its output is plane polarised; if the incident light is "
  "already polarised along the axis, cos²0° = 1 and all of it passes. Only transverse waves can be polarised, so "
  "sound in air (longitudinal) cannot. Light can also be polarised by reflection (completely at Brewster's angle).",
  ["(a) true", "(b) sound in air is longitudinal → false", "(c) true", "(d) Malus: cos²0° = 1 → true",
   "(e) reflection also polarises → false"],
  why="(a) and (c) only leaves out the true statement (d). The other options include (b) or (e), both false.",
  ncert=WOC + "polarisation", seconds=60)

# ================================================================ Dual Nature of Matter and Radiation (B3 I4 A3)
DNC = NC + "'Dual Nature of Radiation and Matter', "
HC = 1240.0  # eV nm

# ---- Basic
E_d1, V_d1 = 4.2, 1.7
close(E_d1 - V_d1, 2.5)
close(E_d1 + V_d1, 5.9)
q(DUAL, "Einstein's equation", "Basic", "numerical",
  "Photons of energy 4.2 eV fall on a metal surface, and the stopping potential for the emitted photoelectrons is "
  "1.7 V. The work function of the metal is:",
  *opt("2.5 eV", ["5.9 eV", "1.7 eV", "4.2 eV"], "C"),
  "Einstein's photoelectric equation: hν = φ₀ + eV₀",
  "The stopping potential measures the maximum kinetic energy: K_max = eV₀. The rest of the photon energy is the "
  "work function.",
  ["K_max = eV₀ = 1.7 eV", "φ₀ = hν − K_max = 4.2 − 1.7 = 2.5 eV"],
  why="5.9 eV adds K_max to the photon energy. 1.7 eV is K_max, not the work function. 4.2 eV is the photon energy.",
  ncert=DNC + "Einstein's photoelectric equation", seconds=30, rc=True)

h_s, lam_d2 = 6.6e-34, 0.33e-9
close(h_s / lam_d2, 2.0e-24)
close(lam_d2 / h_s, 5.0e23)
q(DUAL, "de Broglie wavelength", "Basic", "numerical",
  "The de Broglie wavelength of a moving electron is 0.33 nm. Taking h = 6.6 × 10⁻³⁴ J s, the magnitude of its "
  "momentum is:",
  *opt("2.0 × 10⁻²⁴ kg m/s", ["5.0 × 10²³ kg m/s", "2.2 × 10⁻⁴³ kg m/s", "2.0 × 10⁻²⁵ kg m/s"], "A"),
  "de Broglie relation λ = h/p",
  "The momentum of the particle is Planck's constant divided by its de Broglie wavelength.",
  ["p = h/λ = 6.6 × 10⁻³⁴/(0.33 × 10⁻⁹)", "p = 2.0 × 10⁻²⁴ kg m/s"],
  why="5.0 × 10²³ inverts the relation (λ/h). 2.2 × 10⁻⁴³ multiplies h by λ. 2.0 × 10⁻²⁵ is a slip in the power of "
      "ten (0.33 nm = 3.3 × 10⁻¹⁰ m).",
  ncert=DNC + "wave nature of matter", seconds=30, rc=True)

q(DUAL, "Photoelectric effect", "Basic", "direct",
  "In his experiments of 1887 on electromagnetic waves, Hertz observed that the high-voltage sparks across the "
  "detector loop were enhanced when the emitter plate was illuminated by:",
  *opt("ultraviolet light from an arc lamp", ["infrared radiation from a heater", "radio waves from a second "
                                                                                 "spark gap",
                                              "red light from a filament lamp"], "B"),
  "Hertz's observations",
  "Hertz noticed that ultraviolet light falling on the emitter plate made it easier for sparks to pass: the light "
  "helped free charged particles (electrons) from the metal surface. This was the first observation of the "
  "photoelectric effect.",
  ["Hertz (1887): UV on emitter → sparks enhanced"],
  why="The textbook account names ultraviolet light from an arc lamp; infrared, radio waves and red light have too "
      "little energy per photon to free electrons from the metal used.",
  ncert=DNC + "photoelectric effect - Hertz's observations", seconds=25)

# ---- Intermediate
l1_d, l2_d = 400.0, 300.0
dV = HC / l2_d - HC / l1_d
close(dV, 1.033, 1e-3)
close(HC / l2_d, 4.13, 1e-2)
close(HC / (l1_d - l2_d), 12.4)
q(DUAL, "Einstein's equation", "Intermediate", "numerical",
  "Light of wavelength 400 nm falling on a metal surface ejects photoelectrons with a stopping potential V₁; light "
  "of wavelength 300 nm on the same surface gives a stopping potential V₂. Taking hc = 1240 eV nm, V₂ − V₁ is "
  "about:",
  *opt("1.03 V", ["4.13 V", "0.52 V", "12.4 V"], "D"),
  "eV₀ = hc/λ − φ₀; the work function cancels in the difference",
  "Writing Einstein's equation for both wavelengths and subtracting removes the unknown work function.",
  ["e(V₂ − V₁) = hc/300 − hc/400", "= 1240 × (1/300 − 1/400) = 1240/1200 eV", "V₂ − V₁ ≈ 1.03 V"],
  why="4.13 V is the energy of a 300 nm photon in eV, not a difference. 0.52 V halves the answer. 12.4 V divides hc "
      "by the difference of the wavelengths, which is not how energies combine.",
  ncert=DNC + "Einstein's photoelectric equation", seconds=60, rc=True)

ratio_d = math.sqrt(1836)
close(ratio_d, 42.85, 1e-3)
q(DUAL, "de Broglie wavelength", "Intermediate", "numerical",
  "An electron and a proton have the same kinetic energy (both moving much slower than light). Taking the mass of "
  "the proton as 1836 times that of the electron, the ratio of the de Broglie wavelength of the electron to that "
  "of the proton is about:",
  *opt("43", ["1836", "1/43", "1"], "A"),
  "λ = h/p = h/√(2mK)",
  "For equal kinetic energies, p = √(2mK) ∝ √m, so λ ∝ 1/√m. The lighter electron has the longer wavelength.",
  ["λ_e/λ_p = √(m_p/m_e)", "= √1836 ≈ 42.8 ≈ 43"],
  why="1836 is the mass ratio, not its square root (that would be the answer for equal speeds). 1/43 inverts the "
      "ratio. 1 would be the answer for equal momenta.",
  ncert=DNC + "wave nature of matter", seconds=45, rc=True)

q(DUAL, "Photoelectric effect", "Intermediate", "statement_pair",
  sp("In a photoelectric experiment, a photocurrent flows even when the collector is at zero potential with respect "
     "to the emitter.",
     "In the photoelectric effect, a photon gives only part of its energy to an electron and then continues with "
     "reduced energy."),
  SP, sp_key(True, False),
  "Photocurrent at zero collector potential; photon absorption",
  "Photoelectrons leave the emitter with kinetic energies from zero up to K_max, so many reach the collector even "
  "with no accelerating potential; a retarding potential is needed to stop them (Statement I true). In the "
  "photoelectric effect the photon is absorbed completely, giving all its energy hν to one electron (Statement II "
  "false).",
  ["Emitted electrons have kinetic energy → current at V = 0 → Statement I true",
   "Photon absorbed as a whole → Statement II false"],
  why="Statement II is false, so options A and D are wrong; Statement I is true, so option B is wrong.",
  ncert=DNC + "experimental study of photoelectric effect; photon picture", seconds=40)

ms_dual = {"a": True, "b": False, "c": True, "d": False, "e": True}
q(DUAL, "de Broglie wavelength", "Intermediate", "multi_statement",
  ms("Which of the following statements about de Broglie waves are correct?",
     ["The relation λ = h/p applies to every material particle in motion.",
      "For a fixed momentum, the de Broglie wavelength of a particle depends on its electric charge.",
      "The de Broglie wavelength of an electron accelerated from rest decreases as the accelerating potential "
      "difference is increased.",
      "An electron and a photon that have the same wavelength have the same energy.",
      "Two particles with equal momenta have equal de Broglie wavelengths, whatever their masses."]),
  *mso(ms_dual, "ace", ["ac", "acde", "bce"], "D"),
  "λ = h/p; electron: λ = h/√(2meV); photon E = pc",
  "λ depends only on momentum, so equal momenta give equal wavelengths and charge plays no part once p is fixed. A "
  "larger accelerating voltage gives a larger momentum and a shorter wavelength. A photon and an electron with the "
  "same λ have the same momentum, but the photon's energy pc is much larger than the electron's p²/2m.",
  ["(a) true", "(b) λ = h/p, charge does not enter: false", "(c) λ ∝ 1/√V: true",
   "(d) same p, but E_photon = pc ≫ p²/2m: false", "(e) true"],
  why="(a) and (c) only leaves out the true statement (e). The other options include (b) or (d), both false.",
  ncert=DNC + "wave nature of matter", seconds=60)

# ---- Advanced
m_al, q_al, V_al = 6.4e-27, 3.2e-19, 100.0
lam_al = h_s / math.sqrt(2 * m_al * q_al * V_al)
close(lam_al, 1.03e-12, 1e-2)
close(h_s / math.sqrt(2 * m_al * 1.6e-19 * V_al), 1.46e-12, 1e-2)
close(h_s / math.sqrt(2 * 1.6e-27 * 1.6e-19 * V_al), 2.92e-12, 1e-2)
close(h_s / math.sqrt(2 * m_al * 6.4e-19 * V_al), 7.3e-13, 1e-2)
q(DUAL, "de Broglie wavelength", "Advanced", "numerical",
  "An alpha particle (mass 6.4 × 10⁻²⁷ kg, charge 3.2 × 10⁻¹⁹ C), initially at rest, is accelerated through a "
  "potential difference of 100 V. Taking h = 6.6 × 10⁻³⁴ J s, its de Broglie wavelength is about:",
  *opt("1.0 × 10⁻¹² m", ["1.5 × 10⁻¹² m", "2.9 × 10⁻¹² m", "7.3 × 10⁻¹³ m"], "C"),
  "Charged particle accelerated through V: K = qV, λ = h/√(2mqV)",
  "The kinetic energy gained is qV, where q is the full charge of the alpha particle (2e). Then p = √(2mK) and "
  "λ = h/p.",
  ["K = qV = 3.2 × 10⁻¹⁹ × 100 = 3.2 × 10⁻¹⁷ J", "p = √(2 × 6.4 × 10⁻²⁷ × 3.2 × 10⁻¹⁷) = 6.4 × 10⁻²² kg m/s",
   "λ = 6.6 × 10⁻³⁴/6.4 × 10⁻²² ≈ 1.0 × 10⁻¹² m"],
  why="1.5 × 10⁻¹² m uses the charge e instead of 2e. 2.9 × 10⁻¹² m is the value for a proton. 7.3 × 10⁻¹³ m uses "
      "a charge of 4e.",
  ncert=DNC + "wave nature of matter", seconds=90, rc=True)

lam0, lam_a2 = 500.0, 250.0
K_a2 = HC / lam_a2 - HC / lam0
close(K_a2, 2.48)
close(HC / lam_a2, 4.96)
close(HC / lam_a2 + HC / lam0, 7.44)
close(K_a2 / 2, 1.24)
q(DUAL, "Einstein's equation", "Advanced", "numerical",
  "The threshold wavelength for photoelectric emission from a metal is 500 nm. Light of wavelength 250 nm falls on "
  "it. Taking hc = 1240 eV nm, the maximum kinetic energy of the emitted photoelectrons is:",
  *opt("2.48 eV", ["4.96 eV", "7.44 eV", "1.24 eV"], "B"),
  "Work function from the threshold wavelength: φ₀ = hc/λ₀; K_max = hc/λ − hc/λ₀",
  "At the threshold wavelength the photon energy just equals the work function. The excess energy of the shorter "
  "wavelength photon appears as K_max.",
  ["φ₀ = 1240/500 = 2.48 eV", "hν = 1240/250 = 4.96 eV", "K_max = 4.96 − 2.48 = 2.48 eV"],
  why="4.96 eV is the photon energy. 7.44 eV adds the work function instead of subtracting it. 1.24 eV halves the "
      "correct value.",
  ncert=DNC + "Einstein's photoelectric equation", seconds=60, rc=True)

q(DUAL, "Photoelectric effect", "Advanced", "assertion_reason",
  ar("In a photoelectric experiment with light of fixed frequency and intensity, making the collector more and more "
     "positive with respect to the emitter eventually stops increasing the photocurrent.",
     "At that stage all the photoelectrons emitted by the emitter are already reaching the collector."),
  AR, ar_key(True, True, True),
  "Saturation current",
  "The emitter releases a fixed number of electrons per second (set by the intensity). A positive collector "
  "potential draws more of them across until every emitted electron is collected; beyond that the current cannot "
  "grow, which is the saturation current. R gives the reason for A.",
  ["Fixed intensity → fixed emission rate", "All emitted electrons collected → current saturates → A true, R true "
                                            "and explains A"],
  why="R is exactly why the current saturates, so option B is wrong; both are true, so options C and D are wrong.",
  ncert=DNC + "effect of potential on photoelectric current", seconds=40)

# ================================================================ Atoms and Nuclei (B4 I5 A4)
ATC = NC + "'Atoms', "
NUC = NC + "'Nuclei', "

close((27 / 64) ** (1 / 3), 0.75)
close((27 / 64) ** (2 / 3), 9 / 16)
q(AN, "Nuclear size and mass defect", "Basic", "numerical",
  "Taking the radius of a nucleus of mass number A as R = R₀A^(1/3), the ratio of the radius of the ²⁷Al nucleus to "
  "that of the ⁶⁴Cu nucleus is:",
  *opt("3 : 4", ["27 : 64", "9 : 16", "4 : 3"], "D"),
  "Nuclear radius R ∝ A^(1/3)",
  "R₀ cancels in the ratio, leaving the cube root of the ratio of the mass numbers.",
  ["R_Al/R_Cu = (27/64)^(1/3) = 3/4"],
  why="27 : 64 is the ratio of the volumes (mass numbers). 9 : 16 is the ratio of the surface areas (A^(2/3)). 4 : 3 "
      "inverts the ratio.",
  ncert=NUC + "size of the nucleus", seconds=30, rc=True)

E_He2 = 13.6 * 2 ** 2 / 2 ** 2
close(E_He2, 13.6)
close(13.6 * 4, 54.4)
close(13.6 * 2 / 4, 6.8)
q(AN, "Bohr model and hydrogen spectrum", "Basic", "numerical",
  "In the Bohr model the energy levels of a hydrogen-like ion of atomic number Z are E_n = −13.6 Z²/n² eV. The "
  "energy needed to remove the electron from a He⁺ ion (Z = 2) that is in its first excited state (n = 2) is:",
  *opt("13.6 eV", ["54.4 eV", "3.4 eV", "6.8 eV"], "B"),
  "Ionisation from level n: energy = |E_n|",
  "Removing the electron takes it from E_n to zero, so the energy needed is |E_n| = 13.6 × 4/4 eV.",
  ["E₂(He⁺) = −13.6 × 2²/2² = −13.6 eV", "Energy needed = 13.6 eV"],
  why="54.4 eV is the ionisation energy from the ground state (n = 1). 3.4 eV uses Z = 1 (hydrogen). 6.8 eV uses Z "
      "instead of Z².",
  ncert=ATC + "Bohr model of the hydrogen atom", seconds=35, rc=True)

Z_u, A_u = 92, 238
assert A_u - Z_u == 146
q(AN, "Nuclear size and mass defect", "Basic", "direct",
  "The nucleus of ²³⁸₉₂U contains:",
  *opt("92 protons and 146 neutrons", ["92 protons and 238 neutrons", "146 protons and 92 neutrons",
                                       "238 protons and 92 neutrons"], "C"),
  "Composition of a nucleus: Z protons and N = A − Z neutrons",
  "In the symbol ᴬ_Z X, the subscript Z is the number of protons and the superscript A is the total number of "
  "nucleons, so N = A − Z.",
  ["Z = 92 protons", "N = 238 − 92 = 146 neutrons"],
  why="238 neutrons takes A as the neutron number. The other two options interchange the roles of Z and N or A.",
  ncert=NUC + "atomic masses and composition of nucleus", seconds=20)

q(AN, "Bohr model and hydrogen spectrum", "Basic", "match_list",
  ml("For the electron in the hydrogen atom in the Bohr model, match each quantity in List-I with the way it depends "
     "on the principal quantum number n (List-II).",
     ["Radius of the orbit", "Speed of the electron", "Magnitude of the total energy",
      "Orbital angular momentum"],
     ["n", "n²", "1/n", "1/n²"]),
  *mlo("A-II, B-III, C-IV, D-I",
       ["A-IV, B-III, C-II, D-I", "A-II, B-I, C-IV, D-III", "A-II, B-III, C-I, D-IV"], "A"),
  "Bohr model: r_n ∝ n², v_n ∝ 1/n, E_n ∝ −1/n², L = nh/2π",
  "Quantising L = nh/2π with the condition for circular orbits gives r_n = n²a₀ and v_n = v₁/n, and the energy "
  "E_n = −13.6/n² eV.",
  ["A → n² (II)", "B → 1/n (III)", "C → 1/n² (IV)", "D → n (I)"],
  why="A-IV/C-II swaps the radius and the energy. B-I/D-III swaps the speed and the angular momentum. C-I/D-IV gives "
      "the energy the dependence of L.",
  ncert=ATC + "Bohr model of the hydrogen atom", seconds=40)

# ---- Intermediate
n_ai1 = round(math.sqrt(13.6 / 1.51))
L_ai1 = n_ai1 * h_s / (2 * math.pi)
assert n_ai1 == 3
close(L_ai1, 3.15e-34, 1e-2)
close(h_s / (2 * math.pi), 1.05e-34, 1e-2)
close(9 * h_s / (2 * math.pi), 9.45e-34, 1e-2)
q(AN, "Bohr model and hydrogen spectrum", "Intermediate", "numerical",
  "In the Bohr model of the hydrogen atom (E_n = −13.6/n² eV), the electron is in an orbit where its total energy "
  "is −1.51 eV. Taking h = 6.6 × 10⁻³⁴ J s, its orbital angular momentum is about:",
  *opt("3.15 × 10⁻³⁴ J s", ["1.05 × 10⁻³⁴ J s", "9.45 × 10⁻³⁴ J s", "2.10 × 10⁻³⁴ J s"], "B"),
  "Identify n from E_n; then L = nh/2π",
  "The energy fixes the orbit number; Bohr's quantisation condition then gives the angular momentum.",
  ["n² = 13.6/1.51 ≈ 9 → n = 3", "L = 3h/2π = 3 × 6.6 × 10⁻³⁴/(2π) ≈ 3.15 × 10⁻³⁴ J s"],
  why="1.05 × 10⁻³⁴ J s is h/2π (n = 1). 9.45 × 10⁻³⁴ J s uses n = 9 (n² instead of n). 2.10 × 10⁻³⁴ J s uses n = 2.",
  ncert=ATC + "Bohr model of the hydrogen atom", seconds=50, rc=True)

T_ratio = F(1, 2) ** 3
assert T_ratio == F(1, 8)
q(AN, "Bohr model and hydrogen spectrum", "Intermediate", "numerical",
  "In the Bohr model of the hydrogen atom, the ratio of the time period of revolution of the electron in the "
  "ground state (n = 1) to that in the first excited state (n = 2) is:",
  *opt("1 : 8", ["1 : 4", "1 : 2", "8 : 1"], "C"),
  "T = 2πr/v with r ∝ n² and v ∝ 1/n → T ∝ n³",
  "The orbit grows as n² while the speed falls as 1/n, so the time for one revolution grows as n³.",
  ["T ∝ r/v ∝ n²/(1/n) = n³", "T₁ : T₂ = 1³ : 2³ = 1 : 8"],
  why="1 : 4 uses only r ∝ n². 1 : 2 uses only v ∝ 1/n. 8 : 1 inverts the ratio.",
  ncert=ATC + "Bohr model of the hydrogen atom", seconds=40, rc=True)

q(AN, "Fission and fusion", "Intermediate", "statement_pair",
  sp("In a nuclear reaction, the total rest mass of the particles before the reaction equals their total rest mass "
     "after it.",
     "In a nuclear reaction, the total number of nucleons before the reaction equals the total number after it."),
  SP, sp_key(False, True),
  "Conservation laws in nuclear reactions; mass–energy equivalence",
  "Energy released in fission or fusion comes from a decrease of rest mass, Q = (Δm)c², so rest mass is not "
  "conserved (Statement I false). The number of nucleons (protons + neutrons) is the same on both sides of a nuclear "
  "reaction (Statement II true).",
  ["Q = Δm c² ≠ 0 → rest mass changes → Statement I false", "Nucleon number conserved → Statement II true"],
  why="Statement I is false, so options A and C are wrong; Statement II is true, so option B is wrong.",
  ncert=NUC + "mass-energy and nuclear binding energy; nuclear energy", seconds=35)

ms_an = {"a": True, "b": True, "c": True, "d": False, "e": True}
q(AN, "Rutherford scattering", "Intermediate", "multi_statement",
  ms("Which of the following statements about the alpha-particle scattering experiment of Geiger and Marsden, and "
     "its interpretation by Rutherford, are correct?",
     ["A very thin gold foil was used as the target.",
      "The scattered alpha particles produced brief flashes of light (scintillations) on a screen, which were viewed "
      "through a microscope.",
      "The number of alpha particles scattered fell off rapidly as the angle of scattering increased.",
      "The results supported the model in which electrons are embedded in a uniform sphere of positive charge.",
      "The experiment showed that the nucleus is about 10⁻¹⁵ m to 10⁻¹⁴ m in size, very small compared with the "
      "atom."]),
  *mso(ms_an, "abce", ["abc", "acde", "bde"], "A"),
  "Geiger–Marsden experiment and the nuclear model",
  "Alpha particles were directed at a thin gold foil, and the scattered ones were counted by the scintillations "
  "they produced on a screen, viewed through a microscope. Most went nearly straight through and the number fell "
  "rapidly with the scattering angle, but a few were turned through large angles. This could not be explained by "
  "Thomson's model and led to a tiny nucleus of size about 10⁻¹⁵–10⁻¹⁴ m.",
  ["(a) true", "(b) true", "(c) true", "(d) the results ruled out Thomson's model: false", "(e) true"],
  why="(a), (b) and (c) only leaves out the true statement (e). The other options include (d), which is false.",
  ncert=ATC + "alpha-particle scattering and Rutherford's nuclear model of atom", seconds=50)

frac = 200 / (235 * 931.5) * 100
close(frac, 0.0914, 1e-2)
close(200 / 235, 0.851, 1e-2)
q(AN, "Fission and fusion", "Intermediate", "numerical",
  "The fission of one ²³⁵U nucleus releases about 200 MeV of energy. Taking the mass of the nucleus as 235 u and "
  "1 u = 931.5 MeV/c², the percentage of the mass of the nucleus that is converted into energy is about:",
  *opt("0.09%", ["0.85%", "9%", "0.009%"], "B"),
  "Mass–energy equivalence: the rest-mass energy of the nucleus is 235 × 931.5 MeV",
  "Express the mass of the nucleus as an energy and compare the energy released with it.",
  ["Rest-mass energy = 235 × 931.5 ≈ 2.19 × 10⁵ MeV", "Fraction = 200/(2.19 × 10⁵) ≈ 9.1 × 10⁻⁴ ≈ 0.09%"],
  why="0.85% divides 200 MeV by 235 and treats the result as a percentage (it is the energy per nucleon in MeV). 9% "
      "and 0.009% are slips by factors of 100 and 10.",
  ncert=NUC + "nuclear energy - fission", seconds=50, rc=True)

# ---- Advanced
v1_b, r1_b = 2.2e6, 0.53e-10
I_orb = qe * v1_b / (2 * math.pi * r1_b)
close(I_orb, 1.057e-3, 1e-2)
close(qe * v1_b / r1_b, 6.64e-3, 1e-2)
close(I_orb / 2, 0.53e-3, 1e-2)
close(qe * v1_b / (math.pi * r1_b), 2.11e-3, 1e-2)
q(AN, "Bohr model and hydrogen spectrum", "Advanced", "numerical",
  "In the ground state of the hydrogen atom in the Bohr model, the electron moves in a circle of radius "
  "0.53 × 10⁻¹⁰ m with a speed of 2.2 × 10⁶ m/s. Taking e = 1.6 × 10⁻¹⁹ C, the equivalent electric current due to "
  "the orbital motion of the electron is about:",
  *opt("1.06 mA", ["6.6 mA", "0.53 mA", "2.1 mA"], "D"),
  "Current of a revolving charge: I = e/T = ev/(2πr)",
  "The electron passes any point of its orbit once every period T = 2πr/v, carrying charge e each time, so the "
  "equivalent current is e/T.",
  ["T = 2πr/v = 2π × 0.53 × 10⁻¹⁰/2.2 × 10⁶ = 1.51 × 10⁻¹⁶ s", "I = e/T = 1.6 × 10⁻¹⁹/1.51 × 10⁻¹⁶ ≈ 1.06 × 10⁻³ A"],
  why="6.6 mA uses ev/r, leaving out 2π. 0.53 mA and 2.1 mA are off by a factor of 2 in the period.",
  ncert=ATC + "Bohr model of the hydrogen atom", seconds=70, rc=True)

Q_li = 8 * 7.07 - 7 * 5.60
close(Q_li, 17.36, 1e-3)
close(7.07 - 5.60, 1.47, 1e-2)
close(8 * 7.07 + 7 * 5.60, 95.76, 1e-3)
close(4 * 7.07 - 7 * 5.60, -10.92, 1e-3)
q(AN, "Binding energy", "Advanced", "numerical",
  "In the reaction ¹H + ⁷Li → ⁴He + ⁴He, the binding energy per nucleon is 5.60 MeV for ⁷Li and 7.07 MeV for ⁴He "
  "(the proton, a single nucleon, has no binding energy). The energy released in the reaction is about:",
  *opt("17.4 MeV", ["1.5 MeV", "95.8 MeV", "10.9 MeV"], "A"),
  "Q = (total binding energy of products) − (total binding energy of reactants)",
  "The energy released equals the increase in total binding energy. Multiply each binding energy per nucleon by "
  "the number of nucleons in that nucleus.",
  ["Products: 2 × 4 × 7.07 = 56.56 MeV", "Reactants: 7 × 5.60 + 0 = 39.20 MeV", "Q = 56.56 − 39.20 ≈ 17.4 MeV"],
  why="1.5 MeV subtracts the binding energies per nucleon without multiplying by the nucleon numbers. 95.8 MeV adds "
      "the binding energies. 10.9 MeV is the magnitude obtained by counting only one helium nucleus, which would "
      "even make the reaction absorb energy.",
  ncert=NUC + "mass-energy and nuclear binding energy", seconds=80, rc=True)

lmax = 1 / (F(1, 4) - F(1, 9))
lmin = 1 / F(1, 4)
assert lmax / lmin == F(9, 5)
assert (1 / (1 - F(1, 4))) / 1 == F(4, 3)
assert (1 / (F(1, 9) - F(1, 16))) / 9 == F(16, 7)
q(AN, "Bohr model and hydrogen spectrum", "Advanced", "numerical",
  "For the Balmer series of hydrogen, given by 1/λ = R(1/2² − 1/n²), n = 3, 4, 5, ..., the ratio of the longest "
  "wavelength to the shortest wavelength in the series is:",
  *opt("9 : 5", ["5 : 9", "4 : 3", "16 : 7"], "C"),
  "Longest wavelength: n = 3 → 2; shortest (series limit): n = ∞ → 2",
  "The longest wavelength comes from the smallest energy gap (3 → 2) and the shortest from the series limit "
  "(∞ → 2).",
  ["1/λ_max = R(1/4 − 1/9) = 5R/36", "1/λ_min = R(1/4) = R/4", "λ_max/λ_min = (36/5)/4 = 9/5"],
  why="5 : 9 inverts the ratio. 4 : 3 is the corresponding ratio for the Lyman series and 16 : 7 for the Paschen "
      "series.",
  ncert=ATC + "line spectra of the hydrogen atom", seconds=60, rc=True)

q(AN, "Bohr model and hydrogen spectrum", "Advanced", "assertion_reason",
  ar("The emission spectrum of hydrogen gas contains many lines, although each hydrogen atom has only one electron.",
     "In a sample of hydrogen, different atoms are excited to different energy levels and make different downward "
     "transitions, each transition emitting a photon of one particular wavelength."),
  AR, ar_key(True, True, True),
  "Origin of the many lines of the hydrogen spectrum",
  "One transition of one atom emits one photon of one wavelength. A sample contains a huge number of atoms; in a "
  "discharge they are raised to various levels and drop by various routes (e.g. 3 → 2, 3 → 1, 4 → 2, ...), so all "
  "the lines appear together. R is the reason for A.",
  ["One transition → one photon of one wavelength", "Many atoms, many different transitions → many lines → A true "
                                                    "and explained by R"],
  why="R explains why one-electron atoms give many lines, so option B is wrong; both are true, so options C and D "
      "are wrong.",
  ncert=ATC + "line spectra of the hydrogen atom", seconds=40)

# ================================================================ Electronic Devices (B4 I6 A4)
SEC = NC + "'Semiconductor Electronics: Materials, Devices and Simple Circuits', "

# ---- Basic
q(ED, "Semiconductors", "Basic", "direct",
  "On the basis of resistivity, solids are classified as metals, semiconductors and insulators. The resistivity of "
  "semiconductors typically lies in the range:",
  *opt("10⁻⁵ to 10⁶ Ω m", ["10⁻⁸ to 10⁻² Ω m", "10¹¹ to 10¹⁹ Ω m", "10⁻¹⁹ to 10⁻¹¹ Ω m"], "C"),
  "Classification of solids by resistivity",
  "Metals have resistivities of about 10⁻² to 10⁻⁸ Ω m, insulators about 10¹¹ to 10¹⁹ Ω m, and semiconductors lie "
  "in between, about 10⁻⁵ to 10⁶ Ω m.",
  ["Metals: 10⁻⁸–10⁻² Ω m", "Semiconductors: 10⁻⁵–10⁶ Ω m", "Insulators: 10¹¹–10¹⁹ Ω m"],
  why="10⁻⁸ to 10⁻² Ω m is the range for metals and 10¹¹ to 10¹⁹ Ω m for insulators. 10⁻¹⁹ to 10⁻¹¹ Ω m is lower "
      "than any real material.",
  ncert=SEC + "classification of metals, conductors and semiconductors", seconds=25)


def gate(name, a, b):
    return {"AND": a & b, "OR": a | b, "NAND": 1 - (a & b), "NOR": 1 - (a | b)}[name]


INPUTS = [(0, 0), (0, 1), (1, 0), (1, 1)]
q(ED, "LED, photodiode and solar cell", "Basic", "direct",
  "A solar cell works on the same basic principle as a photodiode. In its construction, the junction area of a "
  "solar cell is kept much larger than that of a photodiode because:",
  *opt("more solar radiation must fall on the junction so that more power can be generated",
       ["a larger junction area increases the band gap of the semiconductor",
        "a larger junction area allows the cell to be operated in reverse breakdown",
        "a larger junction area makes the cell emit light when current is passed through it"], "B"),
  "Solar cell: a large-area p-n junction for photovoltaic generation",
  "A solar cell, like a photodiode, generates electron–hole pairs by light near the junction, and the junction "
  "field separates them; but it is used without external bias to supply power. Its junction area is kept large so "
  "that a large amount of solar radiation is intercepted and more power is delivered.",
  ["Same principle as a photodiode (light → e–h pairs → separated by junction field)",
   "Large area → more incident radiation → more power"],
  why="The band gap is a property of the material, not of the junction area. A solar cell is not operated in "
      "breakdown. Light emission under forward current is the working of an LED.",
  ncert=SEC + "optoelectronic junction devices - solar cell", seconds=30)

Vin_e3, Vz_e3, R_e3 = 15.0, 6.0, 450.0
close((Vin_e3 - Vz_e3) / R_e3, 0.020)
close(Vin_e3 / R_e3, 0.0333, 1e-2)
close(Vz_e3 / R_e3, 0.0133, 1e-2)
close((Vin_e3 + Vz_e3) / R_e3, 0.0467, 1e-2)
q(ED, "Zener diode", "Basic", "numerical",
  "A Zener diode of breakdown voltage 6.0 V is connected in reverse bias, through a 450 Ω series resistor, to a "
  "15 V DC supply. No load is connected across the Zener diode, which is in its breakdown region. The current "
  "through the Zener diode is:",
  *opt("20 mA", ["33 mA", "13 mA", "47 mA"], "D"),
  "Zener in breakdown holds V_Z; the series resistor drops the rest",
  "In breakdown the Zener voltage stays at 6.0 V, so the series resistor has 15 − 6 = 9 V across it. With no load, "
  "all of the current through the resistor flows through the Zener diode.",
  ["V_R = 15 − 6.0 = 9.0 V", "I = 9.0/450 = 0.020 A = 20 mA"],
  why="33 mA puts the whole 15 V across the resistor. 13 mA uses the Zener voltage across the resistor. 47 mA adds "
      "the two voltages.",
  ncert=SEC + "Zener diode as a voltage regulator", seconds=35, rc=True)

q(ED, "Semiconductors", "Basic", "match_list",
  ml("Match each sample of silicon in List-I with the description of its charge carriers in List-II "
     "(n_e = number density of free electrons, n_h = number density of holes).",
     ["Pure silicon at 0 K", "Pure silicon at room temperature", "Silicon doped with arsenic",
      "Silicon doped with aluminium"],
     ["n_e = n_h, both non-zero", "n_h ≫ n_e", "No free charge carriers", "n_e ≫ n_h"]),
  *mlo("A-III, B-I, C-IV, D-II",
       ["A-I, B-III, C-IV, D-II", "A-III, B-I, C-II, D-IV", "A-I, B-III, C-II, D-IV"], "D"),
  "Intrinsic and extrinsic semiconductors",
  "At 0 K no covalent bonds are broken, so pure Si has no free carriers. At room temperature thermal energy creates "
  "electron–hole pairs, so n_e = n_h. Arsenic (pentavalent) donates electrons → n-type, n_e ≫ n_h. Aluminium "
  "(trivalent) accepts electrons, creating holes → p-type, n_h ≫ n_e.",
  ["A → III", "B → I", "C → IV (n-type)", "D → II (p-type)"],
  why="A-I/B-III swaps the 0 K and room-temperature cases. C-II/D-IV swaps the n-type and p-type dopants.",
  ncert=SEC + "intrinsic and extrinsic semiconductors", seconds=40)

# ---- Intermediate
Vsec_e5 = 24.0
close(Vsec_e5 / 2, 12.0)
close(Vsec_e5 / math.sqrt(2), 17.0, 1e-2)
q(ED, "p-n junction diode and rectifier", "Intermediate", "numerical",
  "In a centre-tap full-wave rectifier using ideal diodes, the peak voltage across the whole secondary winding of "
  "the transformer (from one end to the other) is 24 V. The peak voltage across the load resistor is:",
  *opt("12 V", ["24 V", "17 V", "6 V"], "C"),
  "Centre-tap rectifier: each diode uses half of the secondary",
  "The load is connected between the centre tap and the diodes. During each half-cycle only one half of the "
  "secondary drives current through the load, so the peak load voltage is the peak voltage of half the winding.",
  ["Each half of the secondary: 24/2 = 12 V peak", "Ideal diodes → load peak = 12 V"],
  why="24 V uses the whole secondary. 17 V is the rms value of a 24 V peak, which is not asked. 6 V halves the half "
      "winding again.",
  ncert=SEC + "application of junction diode as a rectifier", seconds=45, rc=True)

V_e6, R_e6, Vd = 5.0, 1200.0, 0.7
close((V_e6 - 2 * Vd) / R_e6, 3.0e-3)
close((V_e6 - Vd) / R_e6, 3.58e-3, 1e-2)
close(V_e6 / R_e6, 4.17e-3, 1e-2)
close((V_e6 - 3 * Vd) / R_e6, 2.42e-3, 1e-2)
q(ED, "p-n junction diode and rectifier", "Intermediate", "numerical",
  "Two silicon junction diodes are connected in series, both forward biased, with a 1.2 kΩ resistor across a 5.0 V "
  "DC supply. Treating each diode as having a constant forward voltage drop of 0.7 V when it conducts, the current "
  "in the circuit is:",
  *opt("3.0 mA", ["3.6 mA", "4.2 mA", "2.4 mA"], "B"),
  "Diode forward drop; loop rule",
  "Both diodes conduct, each taking 0.7 V. The rest of the supply voltage appears across the resistor.",
  ["V_R = 5.0 − 2 × 0.7 = 3.6 V", "I = 3.6/1200 = 3.0 × 10⁻³ A = 3.0 mA"],
  why="3.6 mA subtracts the drop of only one diode. 4.2 mA ignores both drops. 2.4 mA subtracts three drops.",
  ncert=SEC + "p-n junction diode under forward bias", seconds=40, rc=True)

V_e7, R1_e7, R2_e7 = 9.0, 1000.0, 2000.0
close(V_e7 / (R1_e7 + R2_e7), 3e-3)
close(V_e7 / R1_e7, 9e-3)
close(V_e7 / R2_e7, 4.5e-3)
q(ED, "p-n junction diode and rectifier", "Intermediate", "numerical",
  "An ideal 9 V battery is connected in series with a 1 kΩ resistor and a parallel combination of an ideal junction "
  "diode and a 2 kΩ resistor. The diode is connected so that it is reverse biased by the battery. The current drawn "
  "from the battery is:",
  *opt("3 mA", ["9 mA", "4.5 mA", "zero"], "D"),
  "Ideal diode: open circuit in reverse bias, short circuit in forward bias",
  "A reverse-biased ideal diode carries no current, so the parallel branch behaves as the 2 kΩ resistor alone, in "
  "series with 1 kΩ.",
  ["Diode reverse biased → open", "Total resistance = 1 + 2 = 3 kΩ", "I = 9/3000 = 3 × 10⁻³ A = 3 mA"],
  why="9 mA treats the diode as conducting, shorting out the 2 kΩ resistor. 4.5 mA ignores the 1 kΩ resistor. Zero "
      "forgets that current can still flow through the 2 kΩ resistor.",
  ncert=SEC + "p-n junction diode under reverse bias", seconds=45, rc=True)

q(ED, "LED, photodiode and solar cell", "Intermediate", "statement_pair",
  sp("Silicon, with a band gap of about 1.1 eV, is a suitable material for making light emitting diodes that emit "
     "visible light.",
     "The colour (wavelength) of the light emitted by an LED is decided by the band gap of the semiconductor it is "
     "made of."),
  SP, sp_key(False, True),
  "Light emitting diode: photon energy ≈ band gap",
  "In an LED, recombining electrons and holes emit photons of energy about E_g, so the band gap fixes the colour "
  "(Statement II true). Visible photons need about 1.8 eV to 3 eV, so the band gap must be at least about 1.8 eV; "
  "silicon's 1.1 eV is too small, and compound semiconductors such as GaAsP are used instead (Statement I false).",
  ["hν ≈ E_g → band gap sets the colour → Statement II true",
   "Visible light needs E_g ≳ 1.8 eV > 1.1 eV → Statement I false"],
  why="Statement I is false, so options A and C are wrong; Statement II is true, so option B is wrong.",
  ncert=SEC + "optoelectronic junction devices - light emitting diode", seconds=40)

tables = {g: ", ".join(str(gate(g, a, b)) for a, b in INPUTS) for g in ("AND", "OR", "NAND", "NOR")}
assert tables == {"AND": "0, 0, 0, 1", "OR": "0, 1, 1, 1", "NAND": "1, 1, 1, 0", "NOR": "1, 0, 0, 0"}
q(ED, "Logic gates", "Intermediate", "match_list",
  ml("Match each two-input gate in List-I with its outputs in List-II, listed for the inputs (A, B) = (0, 0), "
     "(0, 1), (1, 0), (1, 1) in that order.",
     ["AND", "OR", "NAND", "NOR"],
     [tables["NAND"], tables["AND"], tables["NOR"], tables["OR"]]),
  *mlo("A-II, B-IV, C-I, D-III",
       ["A-II, B-IV, C-III, D-I", "A-I, B-III, C-II, D-IV", "A-II, B-I, C-IV, D-III"], "B"),
  "Truth tables: AND = A·B, OR = A + B, NAND = NOT(A·B), NOR = NOT(A + B)",
  "AND is 1 only for (1,1); OR is 0 only for (0,0); NAND and NOR are the complements of AND and OR.",
  ["AND: 0, 0, 0, 1 → II", "OR: 0, 1, 1, 1 → IV", "NAND: 1, 1, 1, 0 → I", "NOR: 1, 0, 0, 0 → III"],
  why="C-III/D-I swaps NAND and NOR. A-I/B-III gives AND and OR the outputs of NAND and NOR. B-I/C-IV swaps OR and "
      "NAND.",
  ncert=SEC + "logic gates", seconds=45)

ms_ed1 = {"a": True, "b": True, "c": False, "d": False, "e": True}
q(ED, "p-n junction diode and rectifier", "Intermediate", "multi_statement",
  ms("Which of the following statements about rectifiers are correct?",
     ["A capacitor connected across the load of a rectifier reduces the ripple in the output voltage.",
      "With such a capacitor filter, a larger value of the product CR_L (capacitance × load resistance) gives a "
      "smoother output.",
      "The output of a half-wave rectifier without a filter is a steady DC voltage with no ripple.",
      "In a centre-tap full-wave rectifier, the current through the load flows in opposite directions during the "
      "two half-cycles of the input.",
      "A rectifier converts an alternating voltage into a unidirectional (pulsating) voltage."]),
  *mso(ms_ed1, "abe", ["ae", "abde", "bce"], "C"),
  "Rectification and capacitor filtering",
  "A rectifier passes current in one direction only, giving a pulsating, unidirectional output (not steady DC). A "
  "capacitor across the load charges at the peaks and discharges slowly through R_L between them; the larger the "
  "time constant CR_L, the less the voltage falls, so the smoother the output. In a full-wave rectifier the two "
  "diodes conduct alternately but both send current through the load in the same direction.",
  ["(a) true", "(b) larger CR_L → slower discharge → true", "(c) pulsating, not steady: false",
   "(d) same direction through the load: false", "(e) true"],
  why="(a) and (e) only leaves out the true statement (b). The other options include (c) or (d), both false.",
  ncert=SEC + "application of junction diode as a rectifier", seconds=55)

# ---- Advanced
Vz_e11, Vin_e11, RL_e11, Izmin = 10.0, 15.0, 1000.0, 5e-3
IL_e11 = Vz_e11 / RL_e11
Rmax = (Vin_e11 - Vz_e11) / (IL_e11 + Izmin)
close(Rmax, 333.3, 1e-3)
close((Vin_e11 - Vz_e11) / IL_e11, 500)
close((Vin_e11 - Vz_e11) / Izmin, 1000)
close((Vin_e11 - Vz_e11) / 20e-3, 250)
q(ED, "Zener diode", "Advanced", "numerical",
  "A Zener diode of breakdown voltage 10 V is used to keep the voltage across a 1.0 kΩ load at 10 V. It is "
  "connected in parallel with the load, and the combination is joined through a series resistor R to a 15 V DC "
  "supply. For proper regulation, the current through the Zener diode must not fall below 5 mA. The largest value "
  "of R that can be used is about:",
  *opt("333 Ω", ["500 Ω", "1000 Ω", "250 Ω"], "B"),
  "Zener regulator: I_R = I_L + I_Z; V_R = V_in − V_Z",
  "The load current is fixed by V_Z and R_L. The series resistor must carry the load current plus at least the "
  "minimum Zener current, with 15 − 10 = 5 V across it; a larger R would give a smaller current.",
  ["I_L = 10/1000 = 10 mA", "I_R(min) = 10 + 5 = 15 mA", "R_max = 5 V/15 mA ≈ 333 Ω"],
  why="500 Ω leaves no current for the Zener (it uses I_L alone). 1000 Ω leaves out the load current. 250 Ω uses "
      "20 mA, adding the minimum Zener current twice.",
  ncert=SEC + "Zener diode as a voltage regulator", seconds=80, rc=True)

V_e12, Vz_e12, Vd_e12, R_e12 = 12.0, 6.0, 0.7, 1000.0
close((V_e12 - Vz_e12 - Vd_e12) / R_e12, 5.3e-3)
close((V_e12 - Vz_e12) / R_e12, 6.0e-3)
close((V_e12 - Vz_e12 + Vd_e12) / R_e12, 6.7e-3)
close((V_e12 - Vd_e12) / R_e12, 11.3e-3)
q(ED, "Zener diode", "Advanced", "numerical",
  "A Zener diode of breakdown voltage 6.0 V and a silicon junction diode are connected in series with a 1.0 kΩ "
  "resistor across a 12 V DC supply. The Zener diode is reverse biased and in its breakdown region, and the silicon "
  "diode is forward biased with a constant drop of 0.7 V. The current in the circuit is:",
  *opt("5.3 mA", ["6.0 mA", "6.7 mA", "11.3 mA"], "C"),
  "Loop rule with a Zener in breakdown and a forward-biased diode",
  "The Zener in breakdown keeps 6.0 V across it and the silicon diode 0.7 V; the resistor takes the remainder of "
  "the 12 V.",
  ["V_R = 12 − 6.0 − 0.7 = 5.3 V", "I = 5.3/1000 = 5.3 mA"],
  why="6.0 mA ignores the drop across the silicon diode. 6.7 mA adds that drop instead of subtracting it. 11.3 mA "
      "ignores the Zener voltage, as if the Zener were forward biased with no drop.",
  ncert=SEC + "Zener diode", seconds=60, rc=True)

q(ED, "Semiconductors", "Advanced", "assertion_reason",
  ar("At room temperature, pure silicon is a much poorer conductor of electricity than copper.",
     "The number density of free charge carriers in pure silicon at room temperature (about 10¹⁶ m⁻³) is far "
     "smaller than the number density of free electrons in copper (about 10²⁹ m⁻³)."),
  AR, ar_key(True, True, True),
  "Carrier concentration and conductivity",
  "Conduction needs mobile charge carriers. In copper essentially every atom contributes a free electron "
  "(about 10²⁹ m⁻³), while in pure silicon only a tiny fraction of bonds is broken at room temperature (n_i about "
  "1.5 × 10¹⁶ m⁻³). This huge difference in carrier density is why silicon conducts so much worse. R explains A.",
  ["n(Cu) ~ 10²⁹ m⁻³ vs n_i(Si) ~ 10¹⁶ m⁻³ → R true", "Far fewer carriers → much higher resistivity → A true and "
                                                      "explained by R"],
  why="R gives the cause of A, so option B is wrong; both are true, so options C and D are wrong.",
  ncert=SEC + "intrinsic semiconductor", seconds=40)

ms_ed2 = {"a": True, "b": True, "c": True, "d": False, "e": False}
q(ED, "Zener diode", "Advanced", "multi_statement",
  ms("A Zener diode voltage regulator consists of a series resistor and a Zener diode, in reverse breakdown, "
     "connected in parallel with a fixed load resistor. The input voltage is increased slightly, the Zener diode "
     "remaining in breakdown. Which of the following statements are correct?",
     ["The current through the series resistor increases.",
      "The current through the Zener diode increases.",
      "The voltage across the load remains practically constant.",
      "The current through the load increases appreciably.",
      "The voltage across the series resistor remains unchanged."]),
  *mso(ms_ed2, "abc", ["ac", "abcd", "bce"], "B"),
  "Zener regulation: I_R = I_Z + I_L with V_Z constant",
  "In breakdown the Zener voltage, and hence the load voltage and load current, stay practically constant. The "
  "extra input voltage appears across the series resistor, so its voltage and current rise, and the extra current "
  "flows through the Zener diode.",
  ["V_L = V_Z constant → (c) true, (d) false", "V_R = V_in − V_Z rises → (e) false, (a) true",
   "I_Z = I_R − I_L rises → (b) true"],
  why="(a) and (c) only leaves out the true statement (b). The other options include (d) or (e), both false.",
  ncert=SEC + "Zener diode as a voltage regulator", seconds=60)

# ================================================================ Experimental Skills (B2 I3 A2)
I_x1, div_x1 = 60.0, 30
close(I_x1 / div_x1, 2.0)
q(EXP, "Electrical experiments", "Basic", "numerical",
  "In an experiment to find the figure of merit of a galvanometer, a current of 60 µA through it produces a steady "
  "deflection of 30 divisions. The figure of merit of the galvanometer is:",
  *opt("2 µA per division", ["0.5 µA per division", "60 µA per division", "1800 µA per division"], "D"),
  "Figure of merit = current per unit deflection",
  "The figure of merit is the current needed to produce a deflection of one division: k = I/θ.",
  ["k = 60 µA/30 divisions = 2 µA per division"],
  why="0.5 µA per division inverts the ratio (that is divisions per µA). 60 µA per division ignores the number of "
      "divisions. 1800 multiplies instead of dividing.",
  seconds=25, rc=True)

q(EXP, "Electrical experiments", "Basic", "direct",
  "While plotting the reverse-bias characteristic of a p-n junction diode, the reverse current is measured with a "
  "microammeter rather than a milliammeter because:",
  *opt("the reverse current is very small, of the order of microamperes",
       ["the reverse current is very large, beyond the range of a milliammeter",
        "a milliammeter cannot be connected in a reverse-biased circuit",
        "the reverse current flows only after breakdown"], "B"),
  "Reverse saturation current of a junction diode",
  "Under reverse bias only minority carriers cross the junction, so the current is tiny (µA range) and nearly "
  "constant until breakdown. A milliammeter would show practically no deflection.",
  ["Reverse current ~ µA → microammeter needed"],
  why="The reverse current is very small, not very large. Any ammeter can be connected in series in reverse bias. A "
      "small reverse current flows before breakdown too.",
  ncert=SEC + "p-n junction diode under reverse bias", seconds=25)

pitch_x3 = 2.0 / 4
lc_x3 = pitch_x3 / 100
close(lc_x3, 0.005)
close(3.5 + 27 * lc_x3, 3.635)
close(3.5 + 27 * 0.01, 3.77)
close(3.5 + 27 * 0.02, 4.04)
q(EXP, "Vernier calipers and screw gauge", "Intermediate", "numerical",
  "The screw of a screw gauge advances by 2.0 mm in 4 complete rotations, and its circular scale has 100 equal "
  "divisions. There is no zero error. While measuring the diameter of a wire, the main scale reading is 3.5 mm and "
  "the 27th division of the circular scale is on the reference line. The diameter of the wire is:",
  *opt("3.635 mm", ["3.770 mm", "4.040 mm", "3.527 mm"], "C"),
  "Pitch = distance per rotation; least count = pitch/number of circular divisions",
  "First find the pitch from the given advance, then the least count, then add the circular-scale contribution to "
  "the main scale reading.",
  ["Pitch = 2.0 mm/4 = 0.5 mm", "Least count = 0.5/100 = 0.005 mm",
   "Diameter = 3.5 + 27 × 0.005 = 3.5 + 0.135 = 3.635 mm"],
  why="3.770 mm takes the least count as 0.01 mm (pitch 1 mm). 4.040 mm takes the pitch as 2.0 mm. 3.527 mm takes "
      "the least count as 0.001 mm.",
  seconds=60, rc=True)

M_x4, g_x4, L_x4, d_x4, dl_x4 = 4.0, 10.0, 2.0, 1.0e-3, 0.5e-3
Y_x4 = M_x4 * g_x4 * L_x4 / (math.pi * (d_x4 / 2) ** 2 * dl_x4)
close(Y_x4, 2.04e11, 1e-2)
close(M_x4 * g_x4 * L_x4 / (math.pi * d_x4 ** 2 * dl_x4), 5.1e10, 1e-2)
close(M_x4 * g_x4 * L_x4 / (math.pi * (d_x4 / 4) ** 2 * dl_x4), 8.15e11, 1e-2)
close(M_x4 * g_x4 * L_x4 / (math.pi * (d_x4 / 2) ** 2 * 0.5), 2.04e8, 1e-2)
q(EXP, "Mechanics experiments", "Intermediate", "numerical",
  "In Searle's experiment, a load of 4.0 kg produces an extension of 0.50 mm in a wire of length 2.0 m and "
  "diameter 1.0 mm. Taking g = 10 m/s², the Young's modulus of the material of the wire is about:",
  *opt("2.0 × 10¹¹ N/m²", ["5.1 × 10¹⁰ N/m²", "8.2 × 10¹¹ N/m²", "2.0 × 10⁸ N/m²"], "D"),
  "Young's modulus Y = (F/A)/(Δl/L) = FL/(πr²Δl)",
  "The stretching force is the weight of the load. The area uses the radius, half of the measured diameter.",
  ["F = 4.0 × 10 = 40 N; r = 0.50 mm", "A = π(0.5 × 10⁻³)² = 7.85 × 10⁻⁷ m²",
   "Y = 40 × 2.0/(7.85 × 10⁻⁷ × 0.50 × 10⁻³) ≈ 2.0 × 10¹¹ N/m²"],
  why="5.1 × 10¹⁰ uses the diameter as the radius. 8.2 × 10¹¹ uses half the radius. 2.0 × 10⁸ leaves the extension "
      "in millimetres.",
  seconds=80, rc=True)

v1_x5, r_ratio = 2.0, 2
close(v1_x5 * r_ratio ** 2, 8.0)
q(EXP, "Thermal and fluid experiments", "Intermediate", "numerical",
  "In an experiment on viscosity, a steel ball of radius 1 mm falling through a viscous liquid attains a terminal "
  "velocity of 2 cm/s. Another steel ball of radius 2 mm, made of the same steel, falls through the same liquid. "
  "Assuming Stokes' law holds, its terminal velocity is:",
  *opt("8 cm/s", ["4 cm/s", "16 cm/s", "1 cm/s"], "B"),
  "Terminal velocity v = 2r²(ρ − σ)g/(9η) ∝ r²",
  "For the same materials and liquid, everything in the terminal-velocity formula is fixed except r², so doubling "
  "the radius makes v four times larger.",
  ["v ∝ r²", "v₂ = 2 × (2/1)² = 8 cm/s"],
  why="4 cm/s takes v ∝ r. 16 cm/s takes v ∝ r³ (the weight alone). 1 cm/s makes the larger ball slower.",
  ncert="Class 11 Physics, 'Mechanical Properties of Fluids', viscosity - Stokes' law", seconds=40, rc=True)

dL, L_x6, dT_tot, T_tot = 0.1, 100.0, 1.0, 200.0
err_g = (dL / L_x6 + 2 * dT_tot / T_tot) * 100
close(err_g, 1.1)
close((dL / L_x6 + dT_tot / T_tot) * 100, 0.6)
close((2 * dL / L_x6 + dT_tot / T_tot) * 100, 0.7)
q(EXP, "Mechanics experiments", "Advanced", "numerical",
  "In a simple pendulum experiment, the effective length is measured as 100.0 cm with an accuracy of 0.1 cm, and "
  "the time for 100 oscillations is measured as 200 s with a stop-watch of resolution 1 s. The maximum percentage "
  "error in the value of g obtained from g = 4π²L/T² is:",
  *opt("1.1%", ["0.6%", "0.7%", "1.0%"], "C"),
  "Error propagation: Δg/g = ΔL/L + 2ΔT/T",
  "The fractional error in the period equals that in the total time measured (T = t/100 → ΔT/T = Δt/t). Because T "
  "appears squared, its fractional error counts twice.",
  ["ΔL/L = 0.1/100 = 0.1%", "ΔT/T = 1/200 = 0.5%", "Δg/g = 0.1% + 2 × 0.5% = 1.1%"],
  why="0.6% forgets the factor 2 for T². 0.7% puts the factor 2 on L instead of T. 1.0% leaves out the error in L.",
  seconds=60, rc=True)

q(EXP, "Mechanics experiments", "Advanced", "match_list",
  ml("In each experiment of List-I, a straight-line graph is plotted. Match the experiment with the quantity "
     "obtained from the graph (List-II).",
     ["Simple pendulum: T² plotted against the effective length",
      "Verification of Ohm's law: potential difference plotted against current",
      "Searle's apparatus: extension plotted against the load",
      "Convex lens by the u–v method: 1/v plotted against 1/u (magnitudes)"],
     ["Focal length, from the intercepts on the axes", "Resistance, from the slope",
      "Acceleration due to gravity, from the slope", "Young's modulus, from the slope"]),
  *mlo("A-III, B-II, C-IV, D-I",
       ["A-IV, B-II, C-III, D-I", "A-III, B-I, C-IV, D-II", "A-I, B-II, C-IV, D-III"], "D"),
  "Using straight-line graphs in laboratory experiments",
  "T² = (4π²/g)L, so the slope gives g. V = RI, so the slope gives R. Extension = (L/AY) × weight, so the slope "
  "gives Y. For a convex lens with magnitudes, 1/v + 1/u = 1/f, so both intercepts equal 1/f.",
  ["A → g (III)", "B → R (II)", "C → Y (IV)", "D → f (I)"],
  why="A-IV/C-III swaps the pendulum and Searle's experiment. B-I/D-II swaps the lens and Ohm's law. A-I/D-III "
      "gives the lens graph the pendulum's quantity.",
  seconds=50)

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
    doc = {"schema_version": "1.0", "batch_id": "BATCH_004", "created_at": TODAY,
           "notes": "Package PHY_004_p2: 120 original Physics questions (Current Electricity to Experimental Skills), "
                    "NEET_PHY_000881..001000. Numerical answers recomputed by tools/batch_004/PHY_004_p2.py.",
           "stimuli": [], "questions": QS}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {OUT}: {len(QS)} questions")
    print("difficulty", dict(Counter(x["difficulty"] for x in QS)))
    print("formats", dict(fmts))
    print("keys", dict(sorted(keys.items())))


if __name__ == "__main__":
    main()
