"""Builder for batches/parts/BATCH_001_PHY_p2.json (package PHY_001_p2 of BATCH_001).

Physics, 115 original questions, NEET_PHY_000136..NEET_PHY_000250: Current Electricity, Magnetic Effects of Current
and Magnetism, Electromagnetic Induction and Alternating Currents, Electromagnetic Waves, Optics, Dual Nature of
Matter and Radiation, Atoms and Nuclei, Electronic Devices, Experimental Skills.

Every numerical answer is recomputed below with an assert next to its question, and the plan quota, format mix and
answer-key balance are asserted before anything is written. If any assert fails, nothing is written.

    python tools/batch_001/PHY_001_p2.py        (run from docs/neet-bank)
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
PLAN = ROOT / "batches" / "plans" / "BATCH_001_plan.json"
OUT = ROOT / "batches" / "parts" / "BATCH_001_PHY_p2.json"
PACKAGE = "PHY_001_p2"
FIRST_ID = 136

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


def close(a, b, rel=1e-3):
    assert math.isclose(a, b, rel_tol=rel), (a, b)


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


NC = "Class 12 Physics, "

# ================================================================ Current Electricity (B5 I7 A5)
n_e, area, cur, e = 5e28, 2e-6, 3.2, 1.6e-19
close(cur / (n_e * e * area), 2.0e-4)
close(cur / (n_e * e * 2e-3), 2.0e-7)
close(cur / (n_e * e * 1e-6), 4.0e-4)
q(CE, "Drift velocity and Ohm's law", "Basic", "numerical",
  "A copper wire of cross-sectional area 2 mm² carries a current of 3.2 A. The number density of free electrons in "
  "copper is 5 × 10²⁸ m⁻³ and e = 1.6 × 10⁻¹⁹ C. The drift speed of the electrons is:",
  *opt("2.0 × 10⁻⁴ m/s", ["2.0 × 10⁻⁷ m/s", "4.0 × 10⁻⁴ m/s", "1.0 × 10⁻⁴ m/s"], "C"),
  "Current in terms of drift velocity: I = n e A v_d",
  "The current is carried by n electrons per unit volume, each of charge e, drifting with speed v_d through area A.",
  ["A = 2 mm² = 2 × 10⁻⁶ m²",
   "v_d = I / (n e A) = 3.2 / (5 × 10²⁸ × 1.6 × 10⁻¹⁹ × 2 × 10⁻⁶)",
   "Denominator = 1.6 × 10⁴, so v_d = 3.2 / 16000 = 2.0 × 10⁻⁴ m/s (0.2 mm/s)"],
  why="2.0 × 10⁻⁷ m/s converts 2 mm² as 2 × 10⁻³ m². 4.0 × 10⁻⁴ m/s uses A = 1 mm². 1.0 × 10⁻⁴ m/s has an extra "
      "factor of 2 in the denominator.",
  seconds=50, rc=True)

R_par = F(3 * 6, 3 + 6)
assert R_par + 4 == 6 and 1 / (F(1, 3) + F(1, 6) + F(1, 4)) == F(4, 3) and F(9, 18) + 4 == F(9, 2)
q(CE, "Combination of resistors", "Basic", "numerical",
  "A 3 Ω resistor and a 6 Ω resistor are connected in parallel, and this combination is connected in series with "
  "a 4 Ω resistor. The equivalent resistance of the arrangement is:",
  *opt("6 Ω", ["13 Ω", "4/3 Ω", "4.5 Ω"], "A"),
  "Series and parallel combination of resistors",
  "Reduce the parallel pair first, then add the series resistor.",
  ["3 Ω ∥ 6 Ω = (3 × 6)/(3 + 6) = 2 Ω", "Total = 2 Ω + 4 Ω = 6 Ω"],
  why="13 Ω puts all three in series. 4/3 Ω puts all three in parallel. 4.5 Ω inverts the parallel formula, "
      "taking (3 + 6)/(3 × 6) = 0.5 Ω.",
  seconds=30, rc=True)

E_, r_, R_ = 12, 0.5, 5.5
I_ = E_ / (R_ + r_)
assert I_ == 2 and E_ - I_ * r_ == 11 and I_ * r_ == 1 and E_ + I_ * r_ == 13
q(CE, "Cells, emf and internal resistance", "Basic", "numerical",
  "A cell of emf 12 V and internal resistance 0.5 Ω is connected across an external resistance of 5.5 Ω. The "
  "potential difference across the terminals of the cell is:",
  *opt("11 V", ["12 V", "1 V", "13 V"], "D"),
  "Terminal voltage of a cell delivering current: V = ε − Ir",
  "Part of the emf is used to drive the current through the cell's own internal resistance.",
  ["I = ε/(R + r) = 12/(5.5 + 0.5) = 2 A", "V = ε − Ir = 12 − 2 × 0.5 = 11 V (also = IR = 2 × 5.5)"],
  why="12 V is the emf, the terminal voltage only on open circuit. 1 V is the drop inside the cell (Ir). 13 V is "
      "ε + Ir, which applies only while the cell is being charged.",
  seconds=40, rc=True)

q(CE, "Kirchhoff's laws", "Basic", "direct",
  "Kirchhoff's junction rule (the sum of currents entering a junction equals the sum of currents leaving it) is a "
  "consequence of the conservation of:",
  *opt("electric charge", ["energy", "linear momentum", "angular momentum"], "B"),
  "Basis of Kirchhoff's rules",
  "In steady state no charge piles up at a junction, so whatever charge flows in per second must flow out. The loop "
  "rule, in contrast, follows from the fact that the electrostatic force is conservative (energy).",
  ["Junction rule: ΣI_in = ΣI_out → no accumulation of charge → conservation of charge",
   "Loop rule: Σ(changes in potential) = 0 around a closed loop → conservation of energy"],
  why="Energy is the basis of the loop rule, not the junction rule. Momentum and angular momentum play no role in "
      "either rule.",
  ncert=NC + "'Current Electricity', Kirchhoff's rules", seconds=20)

R0, alpha = 10, 4e-3
close(R0 * (1 + alpha * 50), 12)
close(R0 * (1 + alpha * 70), 12.8)
q(CE, "Resistivity and temperature", "Basic", "numerical",
  "A metal wire has a resistance of 10 Ω at 20 °C. The temperature coefficient of resistance of the metal is "
  "4 × 10⁻³ °C⁻¹ (take it as constant, referred to 20 °C). Its resistance at 70 °C is:",
  *opt("12 Ω", ["12.8 Ω", "8 Ω", "10.2 Ω"], "C"),
  "Temperature dependence of resistance: R_T = R₀[1 + α(T − T₀)]",
  "For a metal the resistance rises almost linearly with temperature over a moderate range.",
  ["ΔT = 70 − 20 = 50 °C", "R = 10 [1 + 4 × 10⁻³ × 50] = 10 × 1.2 = 12 Ω"],
  why="12.8 Ω uses ΔT = 70 °C instead of 50 °C. 8 Ω subtracts the change, as if α were negative. 10.2 Ω adds "
      "αΔT = 0.2 directly in ohms instead of multiplying it by R₀.",
  seconds=40, rc=True)

R_wire = 5
assert R_wire * 4 * 4 == 80 and R_wire * 4 == 20 and R_wire * 4 * 16 == 320
q(CE, "Resistivity and temperature", "Intermediate", "numerical",
  "A uniform wire of resistance 5 Ω is drawn out (without any change in volume or resistivity) until its radius is "
  "half of its original value. The new resistance of the wire is:",
  *opt("80 Ω", ["20 Ω", "320 Ω", "1.25 Ω"], "A"),
  "R = ρl/A with constant volume",
  "When the radius halves, the area falls to one-fourth. Since the volume A·l is fixed, the length becomes four "
  "times. Both changes increase the resistance.",
  ["A₂ = A₁/4 (radius halved)", "Volume constant: l₂ = 4l₁",
   "R₂/R₁ = (l₂/l₁)(A₁/A₂) = 4 × 4 = 16", "R₂ = 16 × 5 = 80 Ω"],
  shortcut="At constant volume, R ∝ 1/r⁴. Halving r multiplies R by 2⁴ = 16.",
  why="20 Ω counts only one of the two effects (length or area). 320 Ω takes the area factor as 16 instead of 4. "
      "1.25 Ω divides by 4 instead of multiplying.",
  seconds=60, rc=True)

X = F(12) * F(40, 60)
assert X == 8 and F(12) * F(60, 40) == 18
q(CE, "Wheatstone and metre bridge", "Intermediate", "numerical",
  "In a metre bridge, an unknown resistance X is in the left gap and a 12 Ω resistance is in the right gap. The "
  "null point is found at 40.0 cm from the left end of the wire. The value of X is:",
  *opt("8 Ω", ["18 Ω", "4.8 Ω", "7.2 Ω"], "D"),
  "Balance condition of a metre bridge: X/R = l/(100 − l)",
  "The metre bridge is a Wheatstone bridge whose two ratio arms are the two segments of a uniform wire, so their "
  "resistances are proportional to their lengths.",
  ["Left segment l = 40 cm (on the side of X), right segment = 60 cm",
   "X/12 = 40/60", "X = 12 × 2/3 = 8 Ω"],
  why="18 Ω inverts the ratio of the lengths. 4.8 Ω and 7.2 Ω multiply 12 Ω by 0.4 and 0.6 of a metre, which is "
      "not the balance condition.",
  seconds=50, rc=True)

q(CE, "Combination of resistors", "Intermediate", "assertion_reason",
  ar("Two bulbs rated 60 W, 220 V and 100 W, 220 V are connected in series across a 220 V supply; the 60 W bulb "
     "glows brighter.",
     "In a series connection the same current flows through both bulbs, so the bulb of larger resistance dissipates "
     "more power (P = I²R)."),
  AR, "A",
  "Power in series combinations",
  "From P = V²/R at the rated voltage, the 60 W bulb has the larger resistance (R = 220²/60 ≈ 807 Ω against 484 Ω). "
  "In series the current is common, so P = I²R is larger for the 60 W bulb and it glows brighter. R is true and "
  "is exactly why A happens.",
  ["R(60 W) = 220²/60 ≈ 807 Ω, R(100 W) = 220²/100 = 484 Ω",
   "Series: same I, so P ∝ R → the 60 W bulb dissipates more → A true",
   "R states the reason: P = I²R with common current → correct explanation"],
  why="Option B would need R to be unrelated to A, but R is the very reason. Many students expect the 100 W bulb "
      "to be brighter, which is true only in parallel.",
  ncert=NC + "'Current Electricity', electrical energy and power", seconds=50)

E_net, r_net = (6 - 2) * 1.5, 6 * 0.5
assert E_net / (5 + r_net) == 0.75 and 9 / 8 == 1.125 and 7.5 / 8 == 0.9375 and E_net / 5 == 1.2
q(CE, "Cells, emf and internal resistance", "Intermediate", "numerical",
  "Six identical cells, each of emf 1.5 V and internal resistance 0.5 Ω, are meant to be connected in series "
  "across a 5 Ω resistor, but one cell is connected the wrong way round. The current in the 5 Ω resistor is:",
  *opt("0.75 A", ["1.125 A", "0.9375 A", "1.2 A"], "B"),
  "Cells in series with one reversed",
  "A reversed cell subtracts its emf, cancelling one correctly connected cell as well, so the net emf falls by "
  "2ε. Its internal resistance still adds to the circuit.",
  ["Net emf = (6 − 2) × 1.5 = 6 V", "Total internal resistance = 6 × 0.5 = 3 Ω",
   "I = 6/(5 + 3) = 0.75 A"],
  why="1.125 A ignores the reversal (9 V across 8 Ω). 0.9375 A removes only one cell's emf (7.5 V). 1.2 A ignores "
      "the internal resistances.",
  seconds=60, rc=True)

q(CE, "Cells, emf and internal resistance", "Intermediate", "multi_statement",
  ms("Which of the following statements about cells are correct?",
     ["The emf of a cell is the potential difference between its terminals when no current is drawn from it.",
      "While a cell is being charged by an external source, its terminal voltage is greater than its emf.",
      "When n identical cells are connected in parallel, the emf of the combination is n times the emf of one cell.",
      "When two cells are connected in series, the internal resistance of the combination is the sum of their "
      "internal resistances.",
      "The emf of a cell depends on the external resistance connected across it."]),
  *opt("(a), (b) and (d) only", ["(a), (c) and (d) only", "(b), (d) and (e) only", "(a), (b), (c) and (d) only"], "D"),
  "Emf, terminal voltage and combinations of cells",
  "Emf is a property of the cell (its electrodes and electrolyte); the terminal voltage differs from it by Ir, "
  "with the sign set by the direction of current through the cell.",
  ["(a) True: on open circuit V = ε",
   "(b) True: during charging current enters the positive terminal, V = ε + Ir",
   "(c) False: identical cells in parallel give emf ε (only the internal resistance becomes r/n)",
   "(d) True: r_eq = r₁ + r₂ in series",
   "(e) False: the emf does not depend on the external circuit; the terminal voltage does"],
  why="Any option containing (c) or (e) is wrong; any option leaving out (a), (b) or (d) is incomplete.",
  ncert=NC + "'Current Electricity', cells, emf and internal resistance; cells in series and in parallel",
  seconds=60)

q(CE, "Drift velocity and Ohm's law", "Intermediate", "statement_pair",
  sp("For a conductor carrying a fixed current, doubling its cross-sectional area doubles the drift speed of its "
     "free electrons.",
     "For a fixed potential difference across a conductor, doubling its length halves the drift speed of its free "
     "electrons."),
  SP, "D",
  "Drift speed: v_d = I/(neA) and v_d = eEτ/m",
  "At fixed current, v_d = I/(neA) ∝ 1/A, so doubling A halves v_d: Statement I is false. At fixed potential "
  "difference V, the field is E = V/l, and v_d = eEτ/m = eVτ/(ml) ∝ 1/l, so doubling l halves v_d: Statement II "
  "is true.",
  ["Fixed I: v_d ∝ 1/A → doubling A halves v_d → I false",
   "Fixed V: E = V/l, v_d = eτV/(ml) ∝ 1/l → doubling l halves v_d → II true"],
  why="Statement I reverses the dependence on area; it would be true only for v_d ∝ A, which is not the case.",
  ncert=NC + "'Current Electricity', drift of electrons and the origin of resistivity", seconds=50)

q(CE, "Drift velocity and Ohm's law", "Intermediate", "match_list",
  ml("Match List-I (physical quantity) with List-II (SI unit).",
     ["Resistivity", "Conductivity", "Mobility of charge carriers", "Current density"],
     ["A m⁻²", "Ω m", "m² V⁻¹ s⁻¹", "S m⁻¹"]),
  match_options({"A": "II", "B": "IV", "C": "III", "D": "I"},
                [{"A": "IV", "B": "II", "C": "III", "D": "I"}, {"A": "II", "B": "IV", "C": "I", "D": "III"},
                 {"A": "II", "B": "III", "C": "IV", "D": "I"}], "A"), "A",
  "Units from defining relations",
  "Write each quantity from its defining equation: ρ = RA/l, σ = 1/ρ, µ = v_d/E, j = I/A.",
  ["Resistivity ρ = RA/l → Ω m² / m = Ω m → II",
   "Conductivity σ = 1/ρ → Ω⁻¹ m⁻¹ = S m⁻¹ → IV",
   "Mobility µ = v_d/E → (m s⁻¹)/(V m⁻¹) = m² V⁻¹ s⁻¹ → III",
   "Current density j = I/A → A m⁻² → I"],
  why="The usual slip is swapping resistivity (Ω m) and conductivity (S m⁻¹), or giving mobility the unit of "
      "velocity.",
  ncert=NC + "'Current Electricity', resistivity, conductivity and mobility", seconds=45)

I_c = F(12, 1 + 2 + 3)
assert I_c == 2 and 4 * (I_c * 3) == 24 and 4 * F(12, 5) * 3 == F(144, 5) and 4 * (I_c * 2) == 16
q(CE, "Kirchhoff's laws", "Advanced", "numerical",
  "A battery of emf 12 V and internal resistance 1 Ω is connected in series with two resistors of 2 Ω and 3 Ω. A "
  "4 µF capacitor is connected directly across the 3 Ω resistor. In the steady state, the charge on the capacitor "
  "is:",
  *opt("24 µC", ["28.8 µC", "48 µC", "16 µC"], "B"),
  "Capacitor in a DC circuit in steady state",
  "Once the capacitor is fully charged no current flows through its branch, so the circuit current is set by the "
  "resistors alone. The capacitor then has the same potential difference as the resistor it is connected across.",
  ["Steady state: no current through the capacitor branch",
   "I = 12/(1 + 2 + 3) = 2 A",
   "V across 3 Ω = 2 × 3 = 6 V = V across the capacitor",
   "Q = CV = 4 µF × 6 V = 24 µC"],
  why="28.8 µC ignores the internal resistance (I = 2.4 A, V = 7.2 V). 48 µC puts the full emf across the "
      "capacitor. 16 µC uses the voltage across the 2 Ω resistor.",
  seconds=90, rc=True)

q(CE, "Wheatstone and metre bridge", "Advanced", "assertion_reason",
  ar("In a metre bridge experiment, the known resistance is chosen so that the null point lies near the middle of "
     "the wire.",
     "The balance condition of a Wheatstone bridge is P/Q = R/S, which does not involve the resistance of the "
     "galvanometer."),
  AR, "B",
  "Metre bridge practice and Wheatstone bridge balance",
  "A is true: a null point near the middle keeps the two lengths comparable, so the end resistances (at the "
  "copper strips) and the error in reading l have the least effect on the result. R is also true: at balance no "
  "current flows through the galvanometer, so its resistance does not appear. But R does not explain why the null "
  "point should be near the middle; that is about reducing percentage error and end error.",
  ["A true: null point near 50 cm minimises percentage error and end effects",
   "R true: balance P/Q = R/S is independent of the galvanometer resistance",
   "R is a property of balance, not the reason for choosing a mid-wire null point → option B"],
  why="Option A is the trap: both statements are correct facts about the bridge, but the galvanometer's "
      "resistance has nothing to do with where the null point should lie.",
  ncert=NC + "'Current Electricity', Wheatstone bridge", seconds=60)

a_c, a_m = -5e-4, 5e-3
R_m = 11 / (1 - a_m / a_c)
R_c = 11 - R_m
close(R_m, 1)
close(R_c, 10)
assert abs(R_c * a_c + R_m * a_m) < 1e-12
q(CE, "Resistivity and temperature", "Advanced", "numerical",
  "A carbon resistor (temperature coefficient of resistance −5 × 10⁻⁴ °C⁻¹) and a metal wire resistor (temperature "
  "coefficient +5 × 10⁻³ °C⁻¹) are connected in series. Their total resistance is 11 Ω and does not change, to "
  "first order, when the temperature changes slightly. The resistance of the carbon resistor is:",
  *opt("10 Ω", ["1 Ω", "5.5 Ω", "0.1 Ω"], "C"),
  "Combining positive and negative temperature coefficients",
  "In series the changes in resistance add: ΔR = (R_c α_c + R_m α_m) ΔT. For no net change this bracket must be "
  "zero.",
  ["R_c α_c + R_m α_m = 0 → R_c × 5 × 10⁻⁴ = R_m × 5 × 10⁻³ → R_c = 10 R_m",
   "R_c + R_m = 11 Ω → 11 R_m = 11 → R_m = 1 Ω",
   "R_c = 10 Ω"],
  why="1 Ω is the metal resistor, obtained by swapping the coefficients. 5.5 Ω splits the total equally, which "
      "would need equal and opposite coefficients. 0.1 Ω inverts the ratio of the coefficients and drops the total.",
  seconds=90, rc=True)

best = max(((n_s, 12 // n_s, F(n_s * 2, 3 + F(n_s * 1, 12 // n_s))) for n_s in (1, 2, 3, 4, 6, 12)),
           key=lambda t: t[2])
assert best == (6, 2, 2)
assert F(24, 15) == F(8, 5) and abs(float(F(2) / (3 + F(1, 12))) - 0.649) < 1e-3 and F(12, 3) == 4
q(CE, "Cells, emf and internal resistance", "Advanced", "numerical",
  "Twelve identical cells, each of emf 2 V and internal resistance 1 Ω, are to be arranged in a mixed grouping "
  "(equal rows in parallel, each row having the same number of cells in series) to send the largest possible "
  "current through an external resistance of 3 Ω. The largest current obtainable is:",
  *opt("2 A", ["1.6 A", "0.65 A", "4 A"], "A"),
  "Mixed grouping of cells: maximum current when the total internal resistance equals R",
  "With n cells in series in each of m rows (nm = 12), I = nε/(R + nr/m). The current is largest when nr/m = R.",
  ["Condition: n/m = 3 and nm = 12 → n = 6, m = 2",
   "Total emf = 6 × 2 = 12 V; internal resistance = 6 × 1/2 = 3 Ω",
   "I = 12/(3 + 3) = 2 A",
   "Check: all 12 in series gives 24/15 = 1.6 A; all in parallel gives 2/(3 + 1/12) ≈ 0.65 A"],
  why="1.6 A is all cells in series. 0.65 A is all cells in parallel. 4 A takes 12 V across 3 Ω and forgets the "
      "internal resistance of the grouping.",
  seconds=120, rc=True)

q(CE, "Resistivity and temperature", "Advanced", "multi_statement",
  ms("Which of the following statements about the temperature dependence of resistivity are correct?",
     ["In a metal, resistivity increases with temperature mainly because the average time between collisions of "
      "the electrons decreases.",
      "The resistivity of an intrinsic semiconductor decreases as its temperature rises.",
      "Alloys such as manganin and constantan are used in standard resistors because their resistivity changes "
      "very little with temperature.",
      "Every conductor obeys Ohm's law at all temperatures.",
      "The number density of free electrons in a metal increases greatly with temperature."]),
  *opt("(a), (b) and (c) only", ["(a), (c) and (e) only", "(b), (d) and (e) only", "(a), (b), (c) and (e) only"], "B"),
  "Why resistivity changes with temperature: ρ = m/(ne²τ)",
  "In metals n is nearly fixed and τ falls with temperature, so ρ rises. In semiconductors n rises sharply with "
  "temperature and outweighs the fall in τ, so ρ falls. Manganin and constantan have very weak temperature "
  "dependence. Ohm's law is not universal (diodes, semiconductors, materials with non-linear V–I graphs).",
  ["(a) True: τ decreases as ions vibrate more", "(b) True: n increases with temperature",
   "(c) True: used in wire-bound standard resistors", "(d) False: Ohm's law has limitations",
   "(e) False: in a metal n does not change appreciably with temperature"],
  why="Options with (e) take the semiconductor reason and apply it to metals; options with (d) treat Ohm's law "
      "as a universal law.",
  ncert=NC + "'Current Electricity', temperature dependence of resistivity; limitations of Ohm's law",
  seconds=75)


# ================================================================ Magnetism (B5 I7 A5)
MU0 = 4 * math.pi * 1e-7

q(MAG, "Biot-Savart law", "Basic", "direct",
  "A circular loop lies flat on a horizontal table. Seen from above, a steady current flows anticlockwise in it. "
  "The magnetic field at the centre of the loop is directed:",
  *opt("vertically upwards, out of the table", ["vertically downwards, into the table",
                                               "horizontally, in the plane of the loop", "nowhere; it is zero"], "C"),
  "Direction of the field of a circular loop: right-hand thumb rule",
  "Curl the fingers of the right hand along the current; the thumb gives the field at the centre. For an "
  "anticlockwise current seen from above, the thumb points up, towards the observer.",
  ["Every element of the loop gives dB at the centre along the same axis (Biot-Savart: dl × r̂)",
   "Anticlockwise current seen from above → field along the upward normal"],
  why="Downwards is the result for a clockwise current. The field at the centre is along the axis, not in the "
      "plane of the loop, and contributions of all elements add, so it is not zero.",
  ncert=NC + "'Moving Charges and Magnetism', magnetic field on the axis of a circular current loop", seconds=25)

B_w = MU0 * 10 / (2 * math.pi * 0.05)
close(B_w, 4e-5)
close(MU0 * 10 / (4 * math.pi * 0.05), 2e-5)
q(MAG, "Ampere's law", "Basic", "numerical",
  "A long straight wire carries a steady current of 10 A. Taking µ₀ = 4π × 10⁻⁷ T m A⁻¹, the magnitude of the "
  "magnetic field at a distance of 5 cm from the wire is:",
  *opt("4 × 10⁻⁵ T", ["2 × 10⁻⁵ T", "8 × 10⁻⁵ T", "4 × 10⁻⁷ T"], "D"),
  "Field of a long straight wire from Ampere's circuital law: B = µ₀I/(2πr)",
  "Take a circle of radius r around the wire as the Amperian loop. By symmetry B is constant on it and tangential, "
  "so B(2πr) = µ₀I.",
  ["B = µ₀I/(2πr) = (4π × 10⁻⁷ × 10)/(2π × 0.05)", "= (2 × 10⁻⁶)/0.05 = 4 × 10⁻⁵ T"],
  why="2 × 10⁻⁵ T uses 4πr in the denominator. 8 × 10⁻⁵ T drops the 2. 4 × 10⁻⁷ T leaves r in centimetres.",
  seconds=35, rc=True)

q(MAG, "Magnetic dipole and bar magnet", "Basic", "match_list",
  ml("Match List-I (physical quantity) with List-II (SI unit).",
     ["Magnetic dipole moment", "Magnetic field (B)", "Magnetic flux", "Permeability of free space (µ₀)"],
     ["Wb (T m²)", "T m A⁻¹", "A m²", "N A⁻¹ m⁻¹"]),
  match_options({"A": "III", "B": "IV", "C": "I", "D": "II"},
                [{"A": "I", "B": "IV", "C": "III", "D": "II"}, {"A": "III", "B": "II", "C": "I", "D": "IV"},
                 {"A": "IV", "B": "III", "C": "I", "D": "II"}], "B"), "B",
  "Units of magnetic quantities",
  "Use defining relations: m = IA, F = ILB (so B = F/(IL)), Φ = BA and B = µ₀I/(2πr).",
  ["Magnetic moment m = IA → A m² → III",
   "B = F/(IL) → N A⁻¹ m⁻¹ (= tesla) → IV",
   "Φ = BA → T m² = weber → I",
   "µ₀ = 2πrB/I → T m A⁻¹ → II"],
  why="The common mix-ups are B with flux (T against T m²) and magnetic moment with flux.",
  seconds=40)

q(MAG, "Magnetic materials", "Basic", "direct",
  "Which one of the following substances is diamagnetic?",
  *opt("Bismuth", ["Aluminium", "Iron", "Sodium"], "A"),
  "Classification of magnetic materials",
  "Diamagnetic substances have a small negative susceptibility and are weakly repelled by a magnet. Bismuth, copper, "
  "lead, silicon, water and sodium chloride are examples.",
  ["Bismuth: diamagnetic (χ small, negative)", "Aluminium and sodium: paramagnetic (χ small, positive)",
   "Iron: ferromagnetic (χ very large, positive)"],
  why="Aluminium and sodium are paramagnetic; iron is ferromagnetic.",
  ncert=NC + "'Magnetism and Matter', magnetic properties of materials", seconds=20)

m_coil = 20 * 2 * 0.1 ** 2
close(m_coil * 0.5, 0.2)
close(20 * 2 * 0.1 * 0.5, 2.0)
q(MAG, "Torque on loop and galvanometer", "Basic", "numerical",
  "A square coil of side 10 cm has 20 turns and carries a current of 2 A. It is placed in a uniform magnetic field "
  "of 0.5 T with the plane of the coil parallel to the field. The torque on the coil is:",
  *opt("0.2 N m", ["zero", "0.4 N m", "2.0 N m"], "B"),
  "Torque on a current loop: τ = NIAB sin θ, θ measured between the area vector and B",
  "When the plane of the coil is parallel to B, its area vector (normal) is perpendicular to B, so θ = 90° and the "
  "torque is maximum.",
  ["A = (0.1 m)² = 0.01 m²", "m = NIA = 20 × 2 × 0.01 = 0.4 A m²", "τ = mB sin 90° = 0.4 × 0.5 = 0.2 N m"],
  why="Zero takes θ as the angle between the plane and B; θ is measured from the normal. 0.4 N m is the magnetic "
      "moment, not the torque. 2.0 N m takes the area as 0.1 m².",
  seconds=40, rc=True)

f_wire = MU0 * 5 * 8 / (2 * math.pi * 0.04)
close(f_wire, 2e-4)
q(MAG, "Force on charges and conductors", "Intermediate", "numerical",
  "Two long parallel straight wires 4 cm apart carry currents of 5 A and 8 A in the same direction. Taking "
  "µ₀ = 4π × 10⁻⁷ T m A⁻¹, the force per unit length between the wires is:",
  *opt("2 × 10⁻⁴ N/m, attractive", ["2 × 10⁻⁴ N/m, repulsive", "1 × 10⁻⁴ N/m, attractive",
                                     "4 × 10⁻⁴ N/m, attractive"], "A"),
  "Force between parallel currents: F/L = µ₀I₁I₂/(2πd)",
  "Each wire sits in the field of the other. Currents in the same direction attract; opposite currents repel.",
  ["F/L = (4π × 10⁻⁷ × 5 × 8)/(2π × 0.04)", "= (2 × 10⁻⁷ × 40)/0.04 = 2 × 10⁻⁴ N/m",
   "Same direction → attractive"],
  why="Repulsive is the case for opposite currents. 1 × 10⁻⁴ N/m uses 4πd; 4 × 10⁻⁴ N/m drops the 2 in 2πd.",
  ncert=NC + "'Moving Charges and Magnetism', force between two parallel currents", seconds=45, rc=True)

r_ratio = math.sqrt((4 / 2) / (1 / 1))
close(r_ratio, math.sqrt(2))
q(MAG, "Force on charges and conductors", "Intermediate", "numerical",
  "A proton and an alpha particle, both starting from rest, are accelerated through the same potential difference "
  "and then enter a uniform magnetic field at right angles to it. The ratio of the radius of the alpha particle's "
  "circular path to that of the proton (r_α : r_p) is:",
  *opt("√2 : 1", ["2 : 1", "1 : 1", "1 : √2"], "C"),
  "Radius of a charged particle in a magnetic field: r = mv/(qB) = √(2mK)/(qB)",
  "After acceleration through V, K = qV, so the momentum is √(2mqV) and r = √(2mV/q)/B ∝ √(m/q).",
  ["r ∝ √(m/q)", "Alpha: m = 4m_p, q = 2e → m/q = 2(m_p/e)", "Proton: m/q = m_p/e",
   "r_α/r_p = √2"],
  why="2 : 1 is the ratio of m/q without the square root. 1 : 1 assumes equal momenta. 1 : √2 inverts the ratio.",
  seconds=75, rc=True)

S_sh = F(10, 1000) * 99 / (1 - F(10, 1000))
assert S_sh == 1 and F(10, 1000) * 99 / 1 == F(99, 100) and F(100, 1000) * 99 / (1 - F(100, 1000)) == 11
q(MAG, "Torque on loop and galvanometer", "Intermediate", "numerical",
  "A galvanometer of resistance 99 Ω gives full-scale deflection for a current of 10 mA. To convert it into an "
  "ammeter of range 0–1 A, one should connect:",
  *opt("1 Ω in parallel", ["0.99 Ω in parallel", "1 Ω in series", "11 Ω in parallel"], "D"),
  "Conversion of a galvanometer into an ammeter: low shunt in parallel",
  "At full scale, I_g flows through the galvanometer and the rest, I − I_g, through the shunt. Both have the same "
  "potential difference.",
  ["I_g G = (I − I_g) S", "S = I_g G/(I − I_g) = (0.01 × 99)/(1 − 0.01) = 0.99/0.99 = 1 Ω",
   "The shunt is connected in parallel with the galvanometer"],
  why="0.99 Ω divides by I instead of (I − I_g). A series resistor converts the galvanometer into a voltmeter, not "
      "an ammeter. 11 Ω takes I_g as 100 mA instead of 10 mA.",
  seconds=60, rc=True)

R_ser = F(10) / F(5, 1000) - 40
assert R_ser == 1960
q(MAG, "Torque on loop and galvanometer", "Intermediate", "numerical",
  "A galvanometer of resistance 40 Ω shows full-scale deflection for a current of 5 mA. To use it as a voltmeter of "
  "range 0–10 V, the resistance required and its connection are:",
  *opt("1960 Ω in series", ["2000 Ω in series", "2040 Ω in series", "1960 Ω in parallel"], "B"),
  "Conversion of a galvanometer into a voltmeter: high resistance in series",
  "At full scale, the whole 10 V appears across the galvanometer and the series resistance, with current I_g.",
  ["I_g (G + R) = V", "G + R = 10/0.005 = 2000 Ω", "R = 2000 − 40 = 1960 Ω, in series"],
  why="2000 Ω is the total resistance of the voltmeter, not the added resistance. 2040 Ω adds G instead of "
      "subtracting it. A parallel resistor would make an ammeter.",
  seconds=50, rc=True)

q(MAG, "Ampere's law", "Intermediate", "statement_pair",
  sp("For a fixed current and a fixed number of turns per unit length, the magnetic field inside a long solenoid "
     "increases with the radius of the solenoid.",
     "Inside a long straight cylindrical wire carrying a steady current spread uniformly over its cross-section, the "
     "magnetic field increases linearly with distance from the axis."),
  SP, "D",
  "Applications of Ampere's circuital law",
  "For a long solenoid, Ampere's law with a rectangular loop gives B = µ₀nI, which has no dependence on the radius: "
  "Statement I is false. Inside a uniform wire of radius a, a circular loop of radius r < a encloses current "
  "I r²/a², so B(2πr) = µ₀I r²/a² and B = µ₀Ir/(2πa²) ∝ r: Statement II is true.",
  ["Solenoid: B = µ₀nI, independent of radius → I false",
   "Inside the wire: I_enc = I r²/a² → B = µ₀Ir/(2πa²) ∝ r → II true"],
  why="Statement I confuses the solenoid with a single loop, whose central field does depend on radius.",
  ncert=NC + "'Moving Charges and Magnetism', Ampere's circuital law; the solenoid", seconds=60)

q(MAG, "Magnetic dipole and bar magnet", "Intermediate", "multi_statement",
  ms("Which of the following statements about a bar magnet are correct?",
     ["The magnetic field pattern of a bar magnet is similar to that of a current-carrying solenoid of the same "
      "shape.",
      "The potential energy of a bar magnet in a uniform magnetic field is minimum when its magnetic moment is "
      "parallel to the field.",
      "A bar magnet placed in a uniform magnetic field experiences no net force.",
      "At equal large distances, the field of a short bar magnet at an axial point is half the field at an "
      "equatorial point.",
      "The torque on a bar magnet in a uniform field is maximum when its magnetic moment is parallel to the field."]),
  *opt("(a), (b) and (c) only", ["(a), (c) and (d) only", "(b), (c) and (e) only", "(a), (b), (c) and (d) only"], "C"),
  "The bar magnet as an equivalent solenoid; dipole in a uniform field",
  "A bar magnet behaves like a solenoid with the same magnetic moment. In a uniform field the forces on its two ends "
  "cancel (no net force) but there is a torque τ = mB sin θ, and its energy is U = −mB cos θ.",
  ["(a) True: NCERT compares the bar magnet with an equivalent solenoid",
   "(b) True: U = −mB cos θ is least (−mB) at θ = 0°",
   "(c) True: equal and opposite forces on the poles in a uniform field",
   "(d) False: B_axial = 2µ₀m/(4πr³) is twice B_equatorial = µ₀m/(4πr³)",
   "(e) False: τ = mB sin θ is zero at θ = 0° and maximum at 90°"],
  why="(d) has the axial and equatorial fields the wrong way round. (e) confuses the position of minimum energy "
      "with that of maximum torque.",
  ncert=NC + "'Magnetism and Matter', the bar magnet; magnetic dipole in a uniform field", seconds=75)

q(MAG, "Magnetic materials", "Intermediate", "match_list",
  ml("Match List-I (type of material) with List-II (magnetic susceptibility χ).",
     ["Diamagnetic material", "Paramagnetic material", "Ferromagnetic material",
      "Superconductor (perfect diamagnet)"],
     ["χ = −1", "small and positive", "large and positive (χ ≫ 1)", "small and negative"]),
  match_options({"A": "IV", "B": "II", "C": "III", "D": "I"},
                [{"A": "I", "B": "II", "C": "III", "D": "IV"}, {"A": "IV", "B": "III", "C": "II", "D": "I"},
                 {"A": "II", "B": "IV", "C": "III", "D": "I"}], "D"), "D",
  "Susceptibility of magnetic materials",
  "χ measures how strongly a material is magnetised by a field. It is small and negative for diamagnets, small and "
  "positive for paramagnets, very large and positive for ferromagnets, and exactly −1 for a superconductor, which "
  "expels the field completely (Meissner effect).",
  ["Diamagnetic: −1 < χ < 0, small in magnitude → IV", "Paramagnetic: small, positive → II",
   "Ferromagnetic: χ ≫ 1 → III", "Superconductor: χ = −1, perfect diamagnet → I"],
  why="Taking a superconductor as merely 'small and negative' misses that it expels the field completely.",
  ncert=NC + "'Magnetism and Matter', magnetic properties of materials", seconds=40)

# hairpin: semicircle mu0 I/(4R) plus two semi-infinite wires each mu0 I/(4 pi R)
steps_n = 200000
semi_inf = sum(math.cos((k + 0.5) * (math.pi / 2) / steps_n) for k in range(steps_n)) * (math.pi / 2) / steps_n
close(semi_inf, 1.0, rel=1e-6)  # R * integral of dx/(x^2+R^2)^1.5 from 0 to inf (x = R tan t) = 1
B_hair = 1 / 4 + 2 * (semi_inf / (4 * math.pi))  # in units of mu0 I / R
close(B_hair, (1 / 4) * (1 + 2 / math.pi))
q(MAG, "Biot-Savart law", "Advanced", "numerical",
  "A long wire is bent into a hairpin shape: two long straight parallel portions joined by a semicircle of radius "
  "R. A current I flows through it. The magnetic field at the centre of the semicircle is:",
  *opt("(µ₀I/4R)(1 + 2/π)", ["µ₀I/4R", "(µ₀I/4R)(1 + 1/π)", "(µ₀I/4R)(1 − 2/π)"], "A"),
  "Biot-Savart law: semicircular arc plus semi-infinite straight wires",
  "The centre of the semicircle lies on the line through the ends of the two straight portions. Each straight "
  "portion is a semi-infinite wire ending at the foot of the perpendicular from the centre, and all three parts "
  "give fields in the same direction at the centre.",
  ["Semicircle: B₁ = µ₀I/(4R)",
   "Each semi-infinite wire: B = (µ₀I/4πR)(sin 90° + sin 0°) = µ₀I/(4πR)",
   "Two wires: µ₀I/(2πR) = (µ₀I/4R)(2/π), same direction as B₁",
   "Total: (µ₀I/4R)(1 + 2/π)"],
  why="µ₀I/4R ignores the straight portions. (1 + 1/π) counts only one straight wire. (1 − 2/π) takes the straight "
      "portions as opposing the arc; but the two wires lie on opposite sides of the centre and carry opposite "
      "currents, so both fields point the same way as the arc's.",
  seconds=120, rc=True)

theta = math.radians(60)
pitch_over_r = 2 * math.pi * math.cos(theta) / math.sin(theta)
close(pitch_over_r, 2 * math.pi / math.sqrt(3))
q(MAG, "Force on charges and conductors", "Advanced", "numerical",
  "A charged particle enters a uniform magnetic field with a velocity that makes an angle of 60° with the direction "
  "of the field. It moves along a helix. The ratio of the pitch of the helix to its radius is:",
  *opt("2π/√3", ["2π√3", "π/√3", "√3/(2π)"], "D"),
  "Helical motion: components of velocity along and across B",
  "The component v sin θ perpendicular to B gives circular motion of radius r = mv sin θ/(qB) and period "
  "T = 2πm/(qB). The component v cos θ along B carries the particle forward a distance p = (v cos θ)T in each turn.",
  ["r = mv sin θ/(qB)", "p = v cos θ × 2πm/(qB)", "p/r = 2π cos θ/sin θ = 2π cot 60° = 2π/√3"],
  why="2π√3 uses tan θ instead of cot θ (components swapped). π/√3 uses half a period. √3/(2π) is the ratio r/p.",
  seconds=90, rc=True)

v_sel = 3e4 / 0.02
r_p = 1.6e-27 * v_sel / (1.6e-19 * 0.02)
close(v_sel, 1.5e6)
close(r_p, 0.75)
close(1.6e-27 * v_sel / (1.6e-19 * 0.01), 1.5)
close(1 / r_p, 1.3333)
q(MAG, "Force on charges and conductors", "Advanced", "numerical",
  "Protons pass undeflected through a region with a uniform electric field of 3 × 10⁴ V/m and a uniform magnetic "
  "field of 0.02 T, perpendicular to each other and to the protons' velocity. The electric field is now switched "
  "off. Taking the proton mass as 1.6 × 10⁻²⁷ kg and its charge as 1.6 × 10⁻¹⁹ C, the radius of the circular path "
  "of the protons in the magnetic field is:",
  *opt("0.75 m", ["1.5 m", "0.375 m", "1.33 m"], "B"),
  "Velocity selector followed by circular motion in B",
  "Undeflected motion means qE = qvB, which fixes the speed. With E removed, the magnetic force alone provides the "
  "centripetal force.",
  ["qE = qvB → v = E/B = 3 × 10⁴/0.02 = 1.5 × 10⁶ m/s",
   "r = mv/(qB) = (1.6 × 10⁻²⁷ × 1.5 × 10⁶)/(1.6 × 10⁻¹⁹ × 0.02)",
   "= 2.4 × 10⁻²¹/3.2 × 10⁻²¹ = 0.75 m"],
  why="1.5 m takes B as 0.01 T in the last step. 0.375 m brings in a spurious factor of 1/2. 1.33 m is the inverse, "
      "qB/(mv).",
  seconds=90, rc=True)

q(MAG, "Torque on loop and galvanometer", "Advanced", "assertion_reason",
  ar("Increasing the number of turns of a moving-coil galvanometer always increases its voltage sensitivity.",
     "The current sensitivity of a moving-coil galvanometer is NAB/k, where k is the torsional constant of the "
     "spring."),
  AR, "D",
  "Current and voltage sensitivity of a moving-coil galvanometer",
  "Current sensitivity φ/I = NAB/k, so R is true. Voltage sensitivity φ/V = NAB/(kR_G). If N is doubled using "
  "the same kind of wire, the length of wire and hence R_G also double, so the voltage sensitivity stays the "
  "same. A is false.",
  ["At equilibrium NIAB = kφ → φ/I = NAB/k → R true",
   "φ/V = NAB/(kR_G); doubling N doubles R_G → φ/V unchanged → A false"],
  why="Increasing N raises current sensitivity, not necessarily voltage sensitivity; options A, B and C all accept "
      "A, which ignores the coil's resistance.",
  ncert=NC + "'Moving Charges and Magnetism', the moving coil galvanometer", seconds=60)

q(MAG, "Magnetic materials", "Advanced", "multi_statement",
  ms("Which of the following statements are correct?",
     ["Magnetic field lines of a bar magnet form continuous closed loops.",
      "The net magnetic flux through any closed surface is zero.",
      "Two magnetic field lines can intersect at a point where the field is strong.",
      "The susceptibility of a paramagnetic material decreases as its temperature rises.",
      "A diamagnetic substance placed in a non-uniform magnetic field moves from the weaker towards the stronger "
      "region of the field."]),
  *opt("(a), (b) and (d) only", ["(a), (b) and (e) only", "(b), (c) and (d) only", "(a), (b), (d) and (e) only"], "A"),
  "Field lines, Gauss's law for magnetism and magnetic materials",
  "Magnetic field lines have no beginning or end, so as many lines leave a closed surface as enter it. Lines cannot "
  "cross, because the field has one direction at each point. Paramagnetic susceptibility follows Curie's law, "
  "χ ∝ 1/T. Diamagnets are pushed from stronger to weaker field regions.",
  ["(a) True: lines are closed loops (continue inside the magnet)",
   "(b) True: Gauss's law for magnetism, Φ_B = 0 for any closed surface",
   "(c) False: two lines crossing would mean two directions of B at one point",
   "(d) True: Curie's law, χ = Cµ₀/T",
   "(e) False: a diamagnet moves from the stronger to the weaker region"],
  why="(e) describes a paramagnet, not a diamagnet. (c) is never true for field lines.",
  ncert=NC + "'Magnetism and Matter', magnetism and Gauss's law; magnetic properties of materials", seconds=75)

# ================================================================ EMI and AC (B4 I5 A4)
emf_f = 200 * (5e-3 - 1e-3) / 0.1
close(emf_f, 8)
close((5e-3 - 1e-3) / 0.1, 0.04)
close(200 * 6e-3 / 0.1, 12)
close(200 * 1e-3 / 0.1, 2)
q(EMI, "Faraday's and Lenz's laws", "Basic", "numerical",
  "The magnetic flux through each turn of a 200-turn coil decreases uniformly from 5 mWb to 1 mWb in 0.1 s. The "
  "magnitude of the average emf induced in the coil is:",
  *opt("8 V", ["0.04 V", "12 V", "2 V"], "C"),
  "Faraday's law: |ε| = N |ΔΦ|/Δt",
  "The emf depends on the rate of change of flux linkage, NΦ.",
  ["ΔΦ per turn = 5 − 1 = 4 mWb = 4 × 10⁻³ Wb", "|ε| = 200 × 4 × 10⁻³/0.1 = 8 V"],
  why="0.04 V leaves out the 200 turns. 12 V adds the initial and final fluxes. 2 V uses only the final flux.",
  seconds=35, rc=True)

V0_ac = 311
close(V0_ac / math.sqrt(2), 220, rel=2e-3)
close(100 * math.pi / (2 * math.pi), 50)
q(EMI, "AC: rms, reactance and impedance", "Basic", "numerical",
  "An alternating voltage is given by v = 311 sin(100πt) volt, with t in seconds. The rms voltage and the frequency "
  "of the supply are approximately:",
  *opt("220 V and 50 Hz", ["311 V and 50 Hz", "220 V and 100 Hz", "156 V and 50 Hz"], "A"),
  "rms value and frequency of a sinusoidal voltage",
  "Compare with v = V₀ sin ωt: V₀ = 311 V and ω = 100π rad/s.",
  ["V_rms = V₀/√2 = 311/1.414 ≈ 220 V", "f = ω/2π = 100π/2π = 50 Hz"],
  why="311 V is the peak value. 100 Hz takes ω/π instead of ω/2π. 156 V divides the peak by 2 instead of √2.",
  seconds=30, rc=True)

q(EMI, "Self and mutual inductance", "Basic", "direct",
  "The SI unit of inductance, the henry (H), is equivalent to:",
  *opt("Wb A⁻¹", ["Wb A", "V A⁻¹ s⁻¹", "T m² A"], "D"),
  "Definition of inductance: Φ = LI (flux linkage per unit current)",
  "Since NΦ = LI, L = NΦ/I, so 1 H = 1 Wb/A. Equivalently, from ε = L dI/dt, 1 H = 1 V s A⁻¹.",
  ["L = NΦ/I → H = Wb/A", "Check with ε = L dI/dt: H = V/(A s⁻¹) = V s A⁻¹ (not V A⁻¹ s⁻¹)"],
  why="Wb A and T m² A multiply by the current instead of dividing. V A⁻¹ s⁻¹ has the second in the wrong place.",
  seconds=25)

assert 220 * F(2500, 500) == 1100 and 5 * F(500, 2500) == 1
q(EMI, "AC generator and transformer", "Basic", "numerical",
  "An ideal transformer has 500 turns in the primary and 2500 turns in the secondary. The primary is connected to "
  "a 220 V AC supply and draws a current of 5 A. The secondary voltage and secondary current are:",
  *opt("1100 V and 1 A", ["1100 V and 25 A", "44 V and 25 A", "44 V and 1 A"], "B"),
  "Ideal transformer: V_s/V_p = N_s/N_p and V_p I_p = V_s I_s",
  "The voltage is stepped up in the ratio of turns; with no losses, power in = power out, so the current is stepped "
  "down by the same ratio.",
  ["V_s = 220 × 2500/500 = 1100 V", "I_s = V_p I_p/V_s = 220 × 5/1100 = 1 A"],
  why="25 A steps the current up along with the voltage, which would make output power 25 times the input. 44 V "
      "uses the turns ratio upside down.",
  seconds=35, rc=True)

B_r, L_r, v_r, R_r = 0.5, 0.5, 4, 2
emf_r = B_r * L_r * v_r
F_r = B_r * (emf_r / R_r) * L_r
close(F_r, 0.125)
close(B_r ** 2 * L_r * v_r / R_r, 0.25)
close(B_r ** 2 * L_r ** 2 * v_r / 4, 0.0625)
q(EMI, "Faraday's and Lenz's laws", "Intermediate", "numerical",
  "A metal rod of length 0.5 m slides on two parallel frictionless rails with a speed of 4 m/s, perpendicular to a "
  "uniform magnetic field of 0.5 T (the field is perpendicular to the plane of the rails). The rails are connected "
  "through a 2 Ω resistor; all other resistance is negligible. The external force needed to keep the rod moving at "
  "constant speed is:",
  *opt("0.125 N", ["0.25 N", "0.0625 N", "1.0 N"], "D"),
  "Motional emf and the magnetic force on the induced current",
  "The moving rod has emf Blv, which drives a current through the resistor. The field exerts a force BIl on this "
  "current that opposes the motion (Lenz's law); at constant speed the applied force must balance it.",
  ["ε = Blv = 0.5 × 0.5 × 4 = 1 V", "I = ε/R = 1/2 = 0.5 A",
   "F = BIl = 0.5 × 0.5 × 0.5 = 0.125 N (= B²l²v/R)"],
  why="0.25 N uses l instead of l² in B²l²v/R. 0.0625 N divides by 4 Ω instead of 2 Ω. 1.0 N is the emf in volts "
      "read as a force.",
  seconds=75, rc=True)

L_c = 0.2
close(0.5 * L_c * (4 ** 2 - 2 ** 2), 1.2)
close(0.5 * L_c * (4 - 2) ** 2, 0.4)
close(L_c * (4 ** 2 - 2 ** 2), 2.4)
close(0.5 * L_c * 4 ** 2, 1.6)
q(EMI, "Self and mutual inductance", "Intermediate", "numerical",
  "The current in a coil of self-inductance 0.2 H increases from 2 A to 4 A. The increase in the magnetic energy "
  "stored in the coil is:",
  *opt("1.2 J", ["0.4 J", "2.4 J", "1.6 J"], "A"),
  "Energy stored in an inductor: U = ½LI²",
  "The stored energy depends on the square of the current, so the change must be found as a difference of squares, "
  "not from the change in current.",
  ["U₁ = ½ × 0.2 × 2² = 0.4 J", "U₂ = ½ × 0.2 × 4² = 1.6 J", "ΔU = 1.6 − 0.4 = 1.2 J"],
  why="0.4 J uses (ΔI)² instead of the difference of the squares. 2.4 J drops the ½. 1.6 J is the final energy, not "
      "the increase.",
  seconds=45, rc=True)

w0 = 1 / math.sqrt(0.5 * 2e-6)
close(w0, 1000)
close(w0 / (2 * math.pi), 159.15)
close(200 / 40, 5)
q(EMI, "LCR resonance and power", "Intermediate", "numerical",
  "A series LCR circuit has L = 0.5 H, C = 2 µF and R = 40 Ω, and is connected to an AC source of rms voltage "
  "200 V whose frequency can be varied. The resonant angular frequency and the rms current at resonance are:",
  *opt("1000 rad/s and 5 A", ["159 rad/s and 5 A", "1000 rad/s and 3.5 A", "500 rad/s and 5 A"], "C"),
  "Series resonance: ω₀ = 1/√(LC), Z = R",
  "At resonance X_L = X_C, so the reactances cancel and the impedance is the resistance alone.",
  ["LC = 0.5 × 2 × 10⁻⁶ = 10⁻⁶ s²", "ω₀ = 1/√(10⁻⁶) = 1000 rad/s",
   "At resonance Z = R = 40 Ω, so I_rms = 200/40 = 5 A"],
  why="159 is the resonant frequency in hertz (ω₀/2π), not in rad/s. 3.5 A divides the rms current by √2 again. "
      "500 rad/s has a spurious factor of ½.",
  seconds=60, rc=True)

q(EMI, "Self and mutual inductance", "Intermediate", "statement_pair",
  sp("Lenz's law is a consequence of the principle of conservation of energy.",
     "The mutual inductance of two coils depends on the currents flowing in them."),
  SP, "C",
  "Lenz's law and mutual inductance",
  "If the induced current aided the change that produced it, the change would grow by itself and energy would be "
  "created; so Lenz's law follows from energy conservation (Statement I true). Mutual inductance depends only on "
  "the geometry of the coils (number of turns, size, separation, orientation) and the permeability of the medium, "
  "not on the currents (Statement II false).",
  ["Statement I: true (opposition to change is required by energy conservation)",
   "Statement II: false (M = µ₀n₁n₂πr₁²l for coaxial solenoids: geometry and medium only)"],
  why="Statement II mixes up M with the flux linkage MI, which does depend on current.",
  ncert=NC + "'Electromagnetic Induction', Lenz's law and conservation of energy; mutual inductance", seconds=45)

q(EMI, "AC: rms, reactance and impedance", "Intermediate", "match_list",
  ml("Match List-I with List-II for a series LCR circuit connected to an AC source of angular frequency ω.",
     ["Inductive reactance", "Capacitive reactance", "Resonant angular frequency", "Impedance at resonance"],
     ["1/√(LC)", "R", "ωL", "1/(ωC)"]),
  match_options({"A": "III", "B": "IV", "C": "I", "D": "II"},
                [{"A": "IV", "B": "III", "C": "I", "D": "II"}, {"A": "III", "B": "IV", "C": "II", "D": "I"},
                 {"A": "I", "B": "IV", "C": "III", "D": "II"}], "C"), "C",
  "Reactance, impedance and resonance",
  "X_L = ωL and X_C = 1/(ωC). Z = √(R² + (X_L − X_C)²); at resonance X_L = X_C, which gives ω₀ = 1/√(LC) and "
  "Z = R.",
  ["Inductive reactance X_L = ωL → III", "Capacitive reactance X_C = 1/(ωC) → IV",
   "Resonant angular frequency: ω₀L = 1/(ω₀C) → ω₀ = 1/√(LC) → I", "Impedance at resonance: Z = R → II"],
  why="Swapping X_L and X_C is the usual slip: an inductor's opposition grows with frequency, a capacitor's falls.",
  ncert=NC + "'Alternating Current', series LCR circuit; resonance", seconds=40)

Z_ = math.hypot(30, 80 - 40)
I_rms = 200 / Z_
close(Z_, 50)
close(I_rms ** 2 * 30, 480)
close(200 * I_rms, 800)
close(200 ** 2 / 30, 1333.3)
close(I_rms ** 2 * 40, 640)
q(EMI, "LCR resonance and power", "Advanced", "numerical",
  "A series circuit contains a 30 Ω resistor, an inductor of reactance 80 Ω and a capacitor of reactance 40 Ω, "
  "connected to a 200 V (rms) AC supply. The average power consumed in the circuit is:",
  *opt("480 W", ["800 W", "1333 W", "640 W"], "A"),
  "Power in an AC circuit: P = V_rms I_rms cos φ = I_rms² R",
  "Only the resistor consumes power on average; the inductor and capacitor store and return energy each cycle.",
  ["Z = √(30² + (80 − 40)²) = √(900 + 1600) = 50 Ω", "I_rms = 200/50 = 4 A", "cos φ = R/Z = 30/50 = 0.6",
   "P = V I cos φ = 200 × 4 × 0.6 = 480 W (= I²R = 16 × 30)"],
  why="800 W is the apparent power V_rms I_rms, ignoring the power factor. 1333 W is V²/R, taking the full supply "
      "voltage across the resistor. 640 W uses the net reactance (40 Ω) in place of R.",
  seconds=75, rc=True)

M_ = MU0 * 1000 * 200 * math.pi * 0.01 ** 2
e_m = M_ * 50
close(M_, 8 * math.pi ** 2 * 1e-6)
close(e_m, 3.948e-3)
close(MU0 * 1000 * 200 * math.pi * 0.02 ** 2 * 50, 15.79e-3)
close(MU0 * 100 * 200 * math.pi * 0.01 ** 2 * 50, 0.3948e-3)
close(MU0 * 1000 * 200 * 0.01 ** 2 * 50, 1.257e-3)
q(EMI, "Self and mutual inductance", "Advanced", "numerical",
  "A small coil of 200 turns and radius 1 cm is placed coaxially well inside a long solenoid that has 1000 turns per "
  "metre. The current in the long solenoid is increased at a steady rate of 50 A/s. Taking µ₀ = 4π × 10⁻⁷ T m A⁻¹, "
  "the emf induced in the small coil is about:",
  *opt("3.95 mV", ["15.8 mV", "0.395 mV", "1.26 mV"], "B"),
  "Mutual inductance of coaxial coils: M = µ₀ n N π r²",
  "The long solenoid's field µ₀nI is uniform inside it, so the flux linkage of the small coil is N(µ₀nI)(πr²), "
  "where r is the radius of the small coil.",
  ["M = µ₀nNπr² = 4π × 10⁻⁷ × 1000 × 200 × π × (0.01)²", "= 8π² × 10⁻⁶ H ≈ 7.9 × 10⁻⁵ H",
   "ε = M dI/dt = 8π² × 10⁻⁶ × 50 = 4π² × 10⁻⁴ V ≈ 3.95 × 10⁻³ V"],
  why="15.8 mV takes the diameter (2 cm) as the radius. 0.395 mV takes 100 turns per metre. 1.26 mV leaves out the π "
      "in the area πr².",
  seconds=120, rc=True)

q(EMI, "Faraday's and Lenz's laws", "Advanced", "assertion_reason",
  ar("A strong magnet dropped into a long vertical copper tube falls with an acceleration less than g.",
     "The current induced in the walls of the tube exerts a force on the magnet that aids its fall."),
  AR, "C",
  "Lenz's law applied to a falling magnet",
  "As the magnet falls, the flux through each ring of the tube changes, inducing currents in the copper (copper "
  "itself is not attracted by the magnet). By Lenz's law these currents oppose the cause, i.e. the relative motion, "
  "so they exert an upward force on the magnet. A is true; R is false because the force opposes the fall.",
  ["Changing flux through rings of the tube → induced currents", "Lenz's law: induced effect opposes the motion → "
   "upward force on the magnet", "Net downward force < mg → acceleration < g: A true; R false"],
  why="A force that aided the fall would increase the magnet's kinetic energy without any source of energy, which "
      "Lenz's law (energy conservation) forbids.",
  ncert=NC + "'Electromagnetic Induction', Lenz's law", seconds=50)

q(EMI, "AC generator and transformer", "Advanced", "multi_statement",
  ms("Which of the following statements about transformers are correct?",
     ["A transformer works on the principle of mutual induction.",
      "In an ideal step-up transformer, the current in the secondary coil is smaller than the current in the "
      "primary coil.",
      "A transformer can be used to step up a steady DC voltage.",
      "The core of a transformer is laminated to reduce energy loss due to eddy currents.",
      "In an ideal step-up transformer, the output power is greater than the input power."]),
  *opt("(a), (b) and (d) only", ["(a), (c) and (d) only", "(a), (b), (d) and (e) only", "(b), (c) and (e) only"], "D"),
  "Working and energy losses of a transformer",
  "An alternating current in the primary produces a changing flux that links the secondary (mutual induction). A "
  "steady DC gives no changing flux, so nothing is induced. In an ideal transformer V_pI_p = V_sI_s, so stepping "
  "voltage up steps current down and the power stays the same.",
  ["(a) True", "(b) True: V_s > V_p with V_pI_p = V_sI_s → I_s < I_p",
   "(c) False: constant flux induces no emf", "(d) True: laminations reduce eddy currents in the core",
   "(e) False: power out = power in for an ideal transformer"],
  why="(e) would violate energy conservation; (c) ignores that induction needs a changing flux.",
  ncert=NC + "'Alternating Current', transformers", seconds=60)

# ================================================================ Electromagnetic Waves (B1 I2 A1)
q(EMW, "EM spectrum and uses", "Basic", "match_list",
  ml("Match List-I (part of the electromagnetic spectrum) with List-II (a use).",
     ["Microwaves", "Infrared", "Ultraviolet", "X-rays"],
     ["Detecting fractures in bones", "Killing germs in water purifiers", "Radar systems used in aircraft "
      "navigation", "Lamps used in physical therapy"]),
  match_options({"A": "III", "B": "IV", "C": "II", "D": "I"},
                [{"A": "IV", "B": "III", "C": "II", "D": "I"}, {"A": "III", "B": "II", "C": "IV", "D": "I"},
                 {"A": "III", "B": "IV", "C": "I", "D": "II"}], "A"), "A",
  "Uses of different parts of the EM spectrum",
  "Each band is used where its interaction with matter is useful: microwaves for radar, infrared for heating "
  "(physical therapy), ultraviolet to kill germs, and X-rays because they pass through soft tissue but not bone.",
  ["Microwaves → radar for aircraft navigation → III", "Infrared → infrared lamps in physical therapy → IV",
   "Ultraviolet → UV lamps kill germs in water purifiers → II", "X-rays → medical diagnosis, e.g. fractures → I"],
  why="The likely slip is swapping infrared (heating) and ultraviolet (germicidal).",
  ncert=NC + "'Electromagnetic Waves', electromagnetic spectrum", seconds=35)

I_d = 2e-6 * 5e4
close(I_d, 0.1)
close(5e4 / 2e-6, 2.5e10)
q(EMW, "Displacement current", "Intermediate", "numerical",
  "A parallel-plate capacitor of capacitance 2 µF is being charged so that the potential difference between its "
  "plates increases at a rate of 5 × 10⁴ V/s. The displacement current in the region between the plates is:",
  *opt("0.1 A", ["zero", "2.5 × 10¹⁰ A", "0.05 A"], "B"),
  "Displacement current: i_d = ε₀ dΦ_E/dt",
  "Between the plates no charge flows, but the electric flux changes. For a parallel-plate capacitor "
  "ε₀ dΦ_E/dt = ε₀A dE/dt = (ε₀A/d) dV/dt = C dV/dt, which equals the conduction current in the leads.",
  ["i_d = C dV/dt", "= 2 × 10⁻⁶ × 5 × 10⁴ = 0.1 A"],
  why="Zero ignores Maxwell's displacement current. 2.5 × 10¹⁰ A divides dV/dt by C. 0.05 A brings in a spurious "
      "factor of ½.",
  ncert=NC + "'Electromagnetic Waves', displacement current", seconds=50, rc=True)

q(EMW, "EM wave properties", "Intermediate", "statement_pair",
  sp("In vacuum, electromagnetic waves of higher frequency travel faster than those of lower frequency.",
     "In an electromagnetic wave, the oscillating electric and magnetic fields are parallel to each other."),
  SP, "B",
  "Nature of electromagnetic waves",
  "All electromagnetic waves travel in vacuum with the same speed c = 1/√(µ₀ε₀), whatever their frequency, so "
  "Statement I is false. E and B are perpendicular to each other and to the direction of propagation, so Statement "
  "II is false.",
  ["Statement I: speed in vacuum = c for all frequencies → false",
   "Statement II: E ⊥ B ⊥ direction of propagation → false"],
  why="Dispersion (speed depending on frequency) happens in a material medium, not in vacuum.",
  ncert=NC + "'Electromagnetic Waves', electromagnetic waves", seconds=35)

B0_w = 6 / 3e8
close(B0_w, 2e-8)
cross = lambda a, b: (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])
assert cross((0, 1, 0), (0, 0, 1)) == (1, 0, 0) and cross((0, 1, 0), (0, 0, -1)) == (-1, 0, 0)
q(EMW, "EM wave properties", "Advanced", "numerical",
  "A plane electromagnetic wave travels in vacuum along the +x direction. At a certain point and instant its "
  "electric field is 6 V/m along the +y direction. Taking c = 3 × 10⁸ m/s, the magnetic field at that point and "
  "instant is:",
  *opt("2 × 10⁻⁸ T along +z", ["2 × 10⁻⁸ T along −z", "1.8 × 10⁹ T along +z", "2 × 10⁻⁸ T along +x"], "C"),
  "Relation between E and B in an EM wave: B = E/c, with E × B along the direction of propagation",
  "In an EM wave E and B are in phase, so B = E/c at every point and instant. The direction of E × B gives the "
  "direction of propagation, which fixes the direction of B.",
  ["|B| = E/c = 6/(3 × 10⁸) = 2 × 10⁻⁸ T", "E along +y, propagation along +x: ŷ × ẑ = x̂, so B is along +z"],
  why="−z would make E × B point along −x. 1.8 × 10⁹ T multiplies by c instead of dividing. B cannot be along x, "
      "the direction of travel: EM waves are transverse.",
  seconds=60, rc=True)

# ================================================================ Optics (B6 I9 A6)
def mirror_v(f, u):
    return 1 / (1 / f - 1 / u)


def lens_v(f, u):
    return 1 / (1 / f + 1 / u)


close(mirror_v(-15, -30), -30)
close(1 / (1 / -15 + 1 / -30), -10)  # sign slip: 1/v = 1/f + 1/u
q(OPT, "Mirrors", "Basic", "numerical",
  "An object is placed 30 cm in front of a concave mirror of focal length 15 cm. The image is formed:",
  *opt("30 cm in front of the mirror", ["10 cm in front of the mirror", "30 cm behind the mirror",
                                        "10 cm behind the mirror"], "B"),
  "Mirror equation: 1/v + 1/u = 1/f (Cartesian sign convention)",
  "With distances measured from the pole and negative in front of the mirror: u = −30 cm and f = −15 cm. The object "
  "is at the centre of curvature, so the image is also at the centre of curvature.",
  ["1/v = 1/f − 1/u = −1/15 + 1/30 = −1/30", "v = −30 cm → real image 30 cm in front of the mirror",
   "m = −v/u = −1: inverted and of the same size"],
  why="10 cm comes from writing 1/v = 1/f + 1/u (the lens-type sign slip). 'Behind the mirror' would be a virtual "
      "image, which a concave mirror forms only for objects inside the focus.",
  seconds=40, rc=True)

P_tot = F(100, 25) + F(100, -50)
assert P_tot == 2 and F(100, 25) + F(100, 50) == 6 and F(1, 25) - F(1, 50) == F(2, 100)
q(OPT, "Refraction and lenses", "Basic", "numerical",
  "A thin convex lens of focal length 25 cm is placed in contact with a thin concave lens of focal length 50 cm. The "
  "power of the combination is:",
  *opt("+2 D", ["+6 D", "−2 D", "+0.02 D"], "A"),
  "Power of thin lenses in contact: P = P₁ + P₂, with P = 1/f (f in metres)",
  "A convex lens has positive power and a concave lens negative power; powers of lenses in contact add.",
  ["P₁ = 1/0.25 m = +4 D", "P₂ = 1/(−0.50 m) = −2 D", "P = +4 − 2 = +2 D"],
  why="+6 D treats the concave lens as converging. −2 D gets the sign of the result wrong. +0.02 D uses focal "
      "lengths in centimetres.",
  seconds=35, rc=True)

q(OPT, "Total internal reflection", "Basic", "assertion_reason",
  ar("A cut diamond sparkles brilliantly because light entering it undergoes multiple total internal reflections "
     "before coming out.",
     "The critical angle for the diamond–air interface is very small (about 24.4°)."),
  AR, "A",
  "Total internal reflection in diamond",
  "Diamond has a large refractive index (about 2.42), so its critical angle is small, about 24.4°. Light that "
  "enters a suitably cut diamond strikes the inner faces at angles larger than this and is totally reflected many "
  "times, coming out only from a few directions. The small critical angle is the reason for the multiple "
  "reflections, so R explains A.",
  ["sin C = 1/n = 1/2.42 → C ≈ 24.4° (small)", "Most rays inside meet faces at more than 24.4° → repeated TIR",
   "Both true, and R is the reason for A"],
  why="R is not a separate fact here: without the small critical angle there would be no multiple total internal "
      "reflection.",
  ncert=NC + "'Ray Optics and Optical Instruments', total internal reflection", seconds=40)

q(OPT, "Polarisation", "Basic", "direct",
  "Which of the following phenomena shows that light waves are transverse?",
  *opt("Polarisation", ["Interference", "Diffraction", "Reflection"], "D"),
  "Polarisation as evidence of transverse waves",
  "Only a transverse wave has a direction of vibration perpendicular to its direction of travel that can be "
  "selected (polarised). Longitudinal waves such as sound cannot be polarised.",
  ["Interference and diffraction occur for all waves, transverse or longitudinal",
   "Reflection occurs for waves and particles alike", "Polarisation needs vibrations perpendicular to the "
   "direction of propagation → transverse"],
  why="Interference and diffraction prove wave nature, not the transverse character.",
  ncert=NC + "'Wave Optics', polarisation", seconds=20)

n_pr = math.sin(math.radians((60 + 30) / 2)) / math.sin(math.radians(60 / 2))
close(n_pr, math.sqrt(2))
close(math.sin(math.radians(60)) / math.sin(math.radians(30)), math.sqrt(3))
q(OPT, "Prism", "Basic", "numerical",
  "A prism of angle 60° produces an angle of minimum deviation of 30°. The refractive index of the material of the "
  "prism is:",
  *opt("√2", ["√3", "1.5", "1/√2"], "C"),
  "Prism formula at minimum deviation: n = sin[(A + δm)/2]/sin(A/2)",
  "At minimum deviation the ray passes symmetrically through the prism, with r = A/2 and i = (A + δm)/2.",
  ["(A + δm)/2 = (60° + 30°)/2 = 45°", "A/2 = 30°", "n = sin 45°/sin 30° = (1/√2)/(1/2) = √2"],
  why="√3 uses sin 60°/sin 30° (forgets to add δm and halve). 1/√2 inverts the ratio. 1.5 is only a typical value "
      "for glass.",
  seconds=40, rc=True)

q(OPT, "Optical instruments", "Basic", "match_list",
  ml("Match List-I (instrument and adjustment) with List-II (magnifying power). Here f, f_o and f_e are focal "
     "lengths, L is the tube length and D is the least distance of distinct vision.",
     ["Simple microscope, final image at the near point", "Simple microscope, final image at infinity",
      "Astronomical telescope in normal adjustment", "Compound microscope, final image at infinity"],
     ["f_o/f_e", "(L/f_o)(D/f_e)", "D/f", "1 + D/f"]),
  match_options({"A": "IV", "B": "III", "C": "I", "D": "II"},
                [{"A": "III", "B": "IV", "C": "I", "D": "II"}, {"A": "IV", "B": "III", "C": "II", "D": "I"},
                 {"A": "IV", "B": "I", "C": "III", "D": "II"}], "C"), "C",
  "Magnifying power of optical instruments",
  "A simple microscope gives 1 + D/f with the image at the near point and D/f with the image at infinity. A "
  "telescope in normal adjustment gives f_o/f_e. A compound microscope with the final image at infinity gives "
  "m_o × m_e = (L/f_o)(D/f_e).",
  ["Simple microscope, near point: m = 1 + D/f → IV", "Simple microscope, infinity: m = D/f → III",
   "Telescope, normal adjustment: m = f_o/f_e → I", "Compound microscope, infinity: m = (L/f_o)(D/f_e) → II"],
  why="The usual slip is swapping the two simple-microscope cases: the extra '1 +' appears only when the image is "
      "at the near point.",
  ncert=NC + "'Ray Optics and Optical Instruments', optical instruments", seconds=45)

app = F(20) / F(4, 3) + F(12) / F(3, 2)
assert app == 23 and F(32) * F(3, 4) == 24 and F(32) / F(3, 2) == F(64, 3)
q(OPT, "Refraction and lenses", "Intermediate", "numerical",
  "A tank contains a 20 cm deep layer of water (refractive index 4/3) with a 12 cm thick layer of oil (refractive "
  "index 1.5) floating on it. Viewed from directly above, the bottom of the tank appears to be at a depth below the "
  "top surface of the oil of:",
  *opt("23 cm", ["24 cm", "21.3 cm", "9 cm"], "B"),
  "Apparent depth for near-normal viewing: each layer contributes (real thickness)/n",
  "For viewing along the normal, a layer of thickness t and refractive index n appears to have thickness t/n. The "
  "apparent depths of successive layers add.",
  ["Water: 20/(4/3) = 15 cm", "Oil: 12/1.5 = 8 cm", "Apparent depth = 15 + 8 = 23 cm (real depth 32 cm)"],
  why="24 cm treats both layers as water. 21.3 cm treats both as oil. 9 cm is the apparent shift (32 − 23), not the "
      "apparent depth.",
  seconds=60, rc=True)

f_air = 1 / ((1.5 - 1) * (1 / 20 + 1 / 20))
f_water = 1 / ((1.5 / (4 / 3) - 1) * (1 / 20 + 1 / 20))
close(f_air, 20)
close(f_water, 80)
q(OPT, "Refraction and lenses", "Intermediate", "numerical",
  "A thin biconvex lens of glass (refractive index 1.5) has both radii of curvature equal to 20 cm. When it is "
  "completely immersed in water (refractive index 4/3), its focal length becomes:",
  *opt("80 cm", ["20 cm", "26.7 cm", "40 cm"], "A"),
  "Lens maker's formula with a surrounding medium: 1/f = (n_lens/n_medium − 1)(1/R₁ − 1/R₂)",
  "Bending at each surface depends on the refractive index of the glass relative to the medium around it. In water "
  "this relative index is much closer to 1, so the lens becomes much weaker.",
  ["In air: 1/f = (1.5 − 1)(1/20 + 1/20) = 0.5 × 0.1 → f = 20 cm",
   "Relative index in water: 1.5/(4/3) = 9/8", "In water: 1/f' = (9/8 − 1)(0.1) = 1/80 → f' = 80 cm"],
  shortcut="f'/f = (n − 1)/(n/n_w − 1) = 0.5/0.125 = 4.",
  why="20 cm is the focal length in air. 26.7 cm multiplies the air value by 4/3. 40 cm doubles it.",
  seconds=60, rc=True)

beta = 600e-9 * 1 / 0.5e-3
close(beta, 1.2e-3)
close(beta / (4 / 3), 0.9e-3)
close(beta * 4 / 3, 1.6e-3)
q(OPT, "Huygens' principle and interference", "Intermediate", "numerical",
  "In a Young's double-slit experiment, the slits are 0.5 mm apart, the screen is 1 m away and light of wavelength "
  "600 nm (in air) is used. If the entire apparatus is immersed in water of refractive index 4/3, the fringe width "
  "becomes:",
  *opt("0.9 mm", ["1.2 mm", "1.6 mm", "0.6 mm"], "D"),
  "Fringe width β = λD/d, with the wavelength in the medium",
  "In water the frequency is unchanged but the wavelength falls to λ/n, so the fringe width falls by the same "
  "factor.",
  ["In air: β = λD/d = (600 × 10⁻⁹ × 1)/(0.5 × 10⁻³) = 1.2 mm", "In water: λ' = λ/n, so β' = β/n",
   "β' = 1.2 × 3/4 = 0.9 mm"],
  why="1.2 mm is the fringe width in air. 1.6 mm multiplies by n instead of dividing. 0.6 mm halves the air value.",
  seconds=60, rc=True)

w_central = 2 * 500e-9 * 2 / 0.1e-3
close(w_central, 0.02)
q(OPT, "Diffraction", "Intermediate", "numerical",
  "Light of wavelength 500 nm falls normally on a single slit of width 0.1 mm. The diffraction pattern is observed "
  "on a screen 2 m away. The linear width of the central maximum is:",
  *opt("2 cm", ["1 cm", "4 cm", "0.5 cm"], "C"),
  "Single-slit diffraction: first minima at a sin θ = ±λ",
  "The central maximum extends between the first minima on either side, at angles ±λ/a for small angles.",
  ["First minimum: θ ≈ λ/a = 500 × 10⁻⁹/10⁻⁴ = 5 × 10⁻³ rad", "Distance of first minimum from centre = Dθ = 2 × "
   "5 × 10⁻³ = 1 cm", "Width of central maximum = 2Dλ/a = 2 cm"],
  why="1 cm is the distance from the centre to the first minimum (half-width). 4 cm doubles again. 0.5 cm uses "
      "the half-width with D = 1 m.",
  ncert=NC + "'Wave Optics', diffraction at a single slit", seconds=50, rc=True)

I_m = F(1, 2) * F(1, 4)
assert I_m == F(1, 8) and F(1, 2) * F(3, 4) == F(3, 8)
close(math.cos(math.radians(60)) ** 2, 0.25)
q(OPT, "Polarisation", "Intermediate", "numerical",
  "Unpolarised light of intensity I₀ passes through two polaroids whose pass axes are inclined at 60° to each "
  "other. The intensity of the light coming out of the second polaroid is:",
  *opt("I₀/8", ["I₀/4", "3I₀/8", "I₀/2"], "A"),
  "Malus' law: I = I₁ cos² θ",
  "The first polaroid passes half the intensity of unpolarised light, whatever its orientation. The second follows "
  "Malus' law with θ = 60°.",
  ["After the first polaroid: I₁ = I₀/2", "After the second: I₂ = (I₀/2) cos² 60° = (I₀/2)(1/4) = I₀/8"],
  why="I₀/4 applies cos² 60° to I₀ directly, forgetting the first halving. 3I₀/8 uses sin² 60°. I₀/2 stops after "
      "the first polaroid.",
  ncert=NC + "'Wave Optics', polarisation", seconds=40, rc=True)

q(OPT, "Polarisation", "Intermediate", "statement_pair",
  sp("When light is incident on a transparent medium at Brewster's angle, the reflected and refracted rays are "
     "perpendicular to each other.",
     "When unpolarised light is incident at Brewster's angle, the refracted light is completely plane polarised."),
  SP, "C",
  "Polarisation by reflection: Brewster's law, tan i_B = n",
  "At Brewster's angle the reflected ray is completely polarised and is perpendicular to the refracted ray "
  "(i_B + r = 90°), so Statement I is true. The refracted light is only partially polarised, because it still "
  "contains most of both components; Statement II is false.",
  ["tan i_B = n with Snell's law gives sin r = cos i_B → r + i_B = 90° → I true",
   "Only the reflected light is fully polarised; the transmitted light is partially polarised → II false"],
  why="Statement II attributes to the refracted beam what is true only of the reflected beam.",
  ncert=NC + "'Wave Optics', polarisation by reflection", seconds=45)

q(OPT, "Huygens' principle and interference", "Intermediate", "statement_pair",
  sp("In Young's double-slit experiment performed with white light, the central fringe is coloured.",
     "Two independent sodium lamps cannot act as coherent sources, because the phase difference between the light "
     "from them changes rapidly and randomly with time."),
  SP, "D",
  "Interference with white light; coherent sources",
  "At the centre the path difference is zero for every wavelength, so all colours interfere constructively and the "
  "central fringe is white (Statement I false). Light from independent sources has a phase difference that changes "
  "randomly in about 10⁻¹⁰ s, so the pattern averages out; they are incoherent (Statement II true).",
  ["Path difference zero at centre for all λ → bright for all colours → white → I false",
   "Independent sources: random phase changes → incoherent → II true"],
  why="The fringes on either side of the centre are coloured, which is where the idea of a coloured central "
      "fringe comes from.",
  ncert=NC + "'Wave Optics', coherent and incoherent addition of waves; interference", seconds=45)

q(OPT, "Huygens' principle and interference", "Intermediate", "match_list",
  ml("Match List-I (observation) with List-II (phenomenon mainly responsible).",
     ["Light guided along a bent optical fibre", "Bright and dark fringes in Young's double-slit experiment",
      "Light spreading into the geometrical shadow behind a narrow slit", "Polaroid sunglasses cutting down glare"],
     ["Diffraction", "Polarisation", "Total internal reflection", "Interference"]),
  match_options({"A": "III", "B": "IV", "C": "I", "D": "II"},
                [{"A": "IV", "B": "III", "C": "I", "D": "II"}, {"A": "III", "B": "I", "C": "IV", "D": "II"},
                 {"A": "III", "B": "IV", "C": "II", "D": "I"}], "D"), "D",
  "Identifying wave-optics and ray-optics phenomena",
  "Optical fibres trap light by repeated total internal reflection; Young's fringes come from superposition of two "
  "coherent waves; bending into the shadow is diffraction; polaroids block one plane of vibration.",
  ["Optical fibre → total internal reflection → III", "Young's fringes → interference → IV",
   "Spreading behind a slit → diffraction → I", "Polaroid sunglasses → polarisation → II"],
  why="Interference and diffraction are often swapped: two coherent sources give interference; bending at one "
      "narrow opening is diffraction.",
  seconds=35)

q(OPT, "Refraction and lenses", "Intermediate", "assertion_reason",
  ar("A convex lens made of glass of refractive index 1.5 converges light whatever medium it is placed in.",
     "The focal length of a lens depends on the refractive index of its material relative to the surrounding "
     "medium."),
  AR, "D",
  "Lens maker's formula with a surrounding medium",
  "By the lens maker's formula, 1/f = (n_lens/n_medium − 1)(1/R₁ − 1/R₂), so R is true. If the medium is optically "
  "denser than the glass (for example carbon disulphide, n ≈ 1.63), n_lens/n_medium < 1, f becomes negative and "
  "the biconvex lens diverges light. So A is false.",
  ["R true: 1/f depends on n_lens/n_medium", "In a medium with n > 1.5: (n_lens/n_medium − 1) < 0 → f < 0 → "
   "diverging → A false"],
  why="A is true only when the surrounding medium is optically rarer than the glass, as with air or water.",
  ncert=NC + "'Ray Optics and Optical Instruments', refraction by a lens: lens maker's formula", seconds=45)

D_s, d_s = 100, 20
f_disp = F(D_s ** 2 - d_s ** 2, 4 * D_s)
assert f_disp == 24 and F(D_s, 4) == 25 and F(D_s ** 2 + d_s ** 2, 4 * D_s) == 26
u1 = (D_s - d_s) / 2  # check: lens at 40 cm from object, image at 60 cm
close(1 / (1 / u1 + 1 / (D_s - u1)), 24)
q(OPT, "Refraction and lenses", "Advanced", "numerical",
  "An object and a screen are fixed 100 cm apart. A convex lens placed between them forms a sharp image on the "
  "screen at two positions of the lens that are 20 cm apart. The focal length of the lens is:",
  *opt("24 cm", ["25 cm", "26 cm", "20 cm"], "B"),
  "Displacement method: f = (D² − d²)/(4D)",
  "By the reversibility of light, the two positions are symmetric: in one, the object distance equals the image "
  "distance of the other. So u + v = D and v − u = d.",
  ["u + v = 100 and v − u = 20 → u = 40 cm, v = 60 cm",
   "1/f = 1/40 + 1/60 = 5/120 → f = 24 cm",
   "Same as (D² − d²)/(4D) = (10000 − 400)/400 = 24 cm"],
  why="25 cm is D/4, the largest focal length for which an image can be formed at all. 26 cm adds d² instead of "
      "subtracting it. 20 cm takes the displacement itself as f.",
  seconds=90, rc=True)

v_o = lens_v(1, -1.25)
close(v_o, 5)
m_o = v_o / 1.25
m_e = 1 + 25 / 5
close(m_o * m_e, 24)
close(m_o * 25 / 5, 20)
q(OPT, "Optical instruments", "Advanced", "numerical",
  "A compound microscope has an objective of focal length 1 cm and an eyepiece of focal length 5 cm. An object is "
  "placed 1.25 cm in front of the objective, and the final image is formed at the least distance of distinct "
  "vision, 25 cm. The magnitude of the magnifying power of the microscope is:",
  *opt("24", ["20", "30", "6"], "A"),
  "Compound microscope: m = m_o × m_e, with m_e = 1 + D/f_e for the final image at the near point",
  "The objective forms a real, magnified image; the eyepiece acts as a simple microscope on this image.",
  ["Objective: 1/v − 1/u = 1/f → 1/v = 1 + 1/(−1.25) = 0.2 → v = 5 cm",
   "m_o = v/u = 5/1.25 = 4 (in magnitude)", "m_e = 1 + D/f_e = 1 + 25/5 = 6", "M = 4 × 6 = 24"],
  why="20 uses m_e = D/f_e, which is for the final image at infinity. 30 takes m_o as v/f_o = 5. 6 is the eyepiece "
      "magnification alone.",
  seconds=120, rc=True)

r2 = math.radians(30)
e_ang = math.degrees(math.asin(math.sqrt(2) * math.sin(r2)))
close(e_ang, 45)
close(0 + e_ang - 30, 15)
close(30 * (math.sqrt(2) - 1), 12.43)
q(OPT, "Prism", "Advanced", "numerical",
  "A ray of light falls normally on one face of a prism of angle 30° made of glass of refractive index √2. The angle "
  "through which the ray is deviated by the prism is:",
  *opt("15°", ["45°", "12.4°", "30°"], "C"),
  "Refraction through a prism: r₁ + r₂ = A and δ = i + e − A",
  "At normal incidence the ray enters undeviated (i = r₁ = 0), so it meets the second face at r₂ = A = 30°.",
  ["i = 0, r₁ = 0 → r₂ = A − r₁ = 30°",
   "At the second face: sin e = n sin r₂ = √2 × ½ = 1/√2 → e = 45°", "δ = i + e − A = 0 + 45° − 30° = 15°"],
  why="45° is the angle of emergence, not the deviation. 12.4° uses the thin-prism formula δ = (n − 1)A, which is "
      "not valid for a 30° prism at normal incidence. 30° is the prism angle.",
  seconds=75, rc=True)

amp_ratio = math.sqrt(F(4, 9))
close(amp_ratio, 2 / 3)
ratio_max_min = ((1 + amp_ratio) / (1 - amp_ratio)) ** 2
close(ratio_max_min, 25)
assert F(9 + 4, 9 - 4) ** 2 == F(169, 25)
q(OPT, "Huygens' principle and interference", "Advanced", "numerical",
  "In a Young's double-slit experiment, the intensities of light from the two slits at the screen are in the ratio "
  "4 : 9. The ratio of the maximum to the minimum intensity in the interference pattern is:",
  *opt("25 : 1", ["169 : 25", "9 : 4", "5 : 1"], "D"),
  "Interference of waves of unequal amplitude: I_max ∝ (a₁ + a₂)², I_min ∝ (a₁ − a₂)²",
  "Intensity is proportional to the square of the amplitude, so first convert the intensity ratio to an "
  "amplitude ratio.",
  ["a₁ : a₂ = √4 : √9 = 2 : 3", "I_max/I_min = (2 + 3)²/(3 − 2)² = 25/1"],
  why="169 : 25 adds and subtracts the intensities instead of the amplitudes. 9 : 4 is just the ratio of the source "
      "intensities. 5 : 1 forgets to square the amplitude sums.",
  seconds=60, rc=True)

q(OPT, "Refraction and lenses", "Advanced", "multi_statement",
  ms("Which of the following statements about the refraction of light are correct?",
     ["When light passes from a denser to a rarer medium, the angle of refraction is greater than the angle of "
      "incidence.",
      "When light passes from air into glass, its wavelength decreases.",
      "When light passes from air into glass, its frequency decreases.",
      "Total internal reflection can occur when light travels from air into water.",
      "The speed of light in glass is less than its speed in air."]),
  *opt("(a), (b) and (e) only", ["(a), (c) and (e) only", "(b), (c) and (d) only", "(a), (b), (d) and (e) only"], "B"),
  "Refraction: Snell's law and what changes at a boundary",
  "Frequency is set by the source and does not change on refraction. In a denser medium the speed falls (v = c/n), "
  "so the wavelength λ = v/f falls too. Total internal reflection needs light going from a denser to a rarer "
  "medium.",
  ["(a) True: n₁ sin i = n₂ sin r with n₁ > n₂ gives r > i", "(b) True: λ_glass = λ_air/n",
   "(c) False: frequency is unchanged", "(d) False: TIR needs denser → rarer; air → water is rarer → denser",
   "(e) True: v = c/n"],
  why="(c) is the classic trap: the colour (frequency) of light does not change on entering glass. (d) reverses "
      "the condition for total internal reflection.",
  ncert=NC + "'Ray Optics and Optical Instruments', refraction; total internal reflection", seconds=60)

q(OPT, "Diffraction", "Advanced", "multi_statement",
  ms("Which of the following statements about diffraction at a single slit and about polaroids are correct?",
     ["The intensity of the secondary maxima decreases as their order increases.",
      "The first minimum of the pattern occurs at an angle θ given by a sin θ = λ/2, where a is the slit width.",
      "The central maximum is twice as wide as each secondary maximum.",
      "Increasing the width of the slit makes the central maximum wider.",
      "Polaroids can be used to control the intensity of light, for example in sunglasses and window panes."]),
  *opt("(a), (c) and (e) only", ["(a), (b) and (c) only", "(c), (d) and (e) only", "(a), (b), (c) and (e) only"], "A"),
  "Single-slit diffraction pattern; uses of polaroids",
  "The first minima are at a sin θ = ±λ, so the central maximum has angular width 2λ/a, twice that of the "
  "secondary maxima, and it narrows when the slit is widened. Secondary maxima get progressively weaker. A polaroid "
  "transmits only one plane of vibration, so turning it controls the transmitted intensity.",
  ["(a) True: secondary maxima fade with order", "(b) False: first minimum at a sin θ = λ",
   "(c) True: central width 2λ/a vs λ/a for the others", "(d) False: width ∝ 1/a",
   "(e) True: polaroids in sunglasses, window panes and photographic filters"],
  why="(b) uses the condition for a path difference of half a wavelength between the edges, which is not a "
      "minimum. (d) inverts the dependence on slit width.",
  ncert=NC + "'Wave Optics', diffraction at a single slit; polarisation", seconds=75)

# ================================================================ Dual Nature (B3 I4 A3)
HC = 1240  # eV nm
close(HC / 620, 2.0)
close(620 / HC, 0.5)
q(DUAL, "Einstein's equation", "Basic", "numerical",
  "The energy of a photon of wavelength 620 nm is (take hc = 1240 eV nm):",
  *opt("2 eV", ["0.5 eV", "20 eV", "0.2 eV"], "D"),
  "Photon energy E = hν = hc/λ",
  "With hc expressed in eV nm, dividing by the wavelength in nm gives the energy directly in eV.",
  ["E = hc/λ = 1240 eV nm / 620 nm = 2 eV"],
  why="0.5 eV inverts the formula (λ/hc). 20 eV and 0.2 eV are slips of a factor of 10 in the division.",
  seconds=25, rc=True)

lam_e = 1.227 / math.sqrt(100)
close(lam_e, 0.1227)
q(DUAL, "de Broglie wavelength", "Basic", "numerical",
  "An electron, initially at rest, is accelerated through a potential difference of 100 V. Using "
  "λ = 1.227/√V nm, its de Broglie wavelength is about:",
  *opt("0.123 nm", ["1.227 nm", "0.0123 nm", "12.27 nm"], "A"),
  "de Broglie wavelength of an electron accelerated through V volts",
  "The electron gains kinetic energy eV, so p = √(2meV) and λ = h/p = h/√(2meV) = 1.227/√V nm.",
  ["√V = √100 = 10", "λ = 1.227/10 = 0.1227 nm ≈ 0.123 nm"],
  why="1.227 nm forgets to divide by √V. 0.0123 nm divides by V instead of √V. 12.27 nm multiplies by √V.",
  ncert=NC + "'Dual Nature of Radiation and Matter', wave nature of matter", seconds=30, rc=True)

q(DUAL, "Photoelectric effect", "Basic", "direct",
  "In a photoelectric experiment, the intensity of the incident light is increased while its frequency (above the "
  "threshold) is kept the same. Which of the following increases?",
  *opt("The saturation photoelectric current", ["The maximum kinetic energy of the photoelectrons",
                                               "The stopping potential", "The threshold frequency of the metal"], "B"),
  "Effect of intensity on photoelectric emission",
  "Greater intensity at a fixed frequency means more photons per second, so more electrons are emitted per second "
  "and the saturation current rises. Each photon still has the same energy hν, so the maximum kinetic energy and "
  "the stopping potential do not change.",
  ["Number of photons per second ∝ intensity → saturation current ∝ intensity",
   "K_max = hν − φ₀: unchanged at fixed ν → stopping potential unchanged",
   "Threshold frequency depends only on the metal"],
  why="Maximum kinetic energy and stopping potential depend on frequency, not intensity. The threshold frequency "
      "is a property of the metal.",
  ncert=NC + "'Dual Nature of Radiation and Matter', effect of intensity of light on photocurrent", seconds=25)

K1 = HC / 310 - 2.0
close(K1, 2.0)
q(DUAL, "Einstein's equation", "Intermediate", "numerical",
  "Light of wavelength 310 nm falls on a metal surface whose work function is 2.0 eV. Taking hc = 1240 eV nm, the "
  "stopping potential is:",
  *opt("2 V", ["4 V", "6 V", "1 V"], "C"),
  "Einstein's photoelectric equation: eV₀ = hν − φ₀",
  "The stopping potential is the reverse potential that just stops the fastest photoelectrons, so eV₀ = K_max.",
  ["Photon energy = 1240/310 = 4 eV", "K_max = 4 − 2 = 2 eV", "V₀ = K_max/e = 2 V"],
  why="4 V uses the photon energy without subtracting the work function. 6 V adds the work function. 1 V halves "
      "K_max.",
  seconds=40, rc=True)

q(DUAL, "Photoelectric effect", "Intermediate", "statement_pair",
  sp("The threshold frequency for photoelectric emission is the same for all metals.",
     "The stopping potential depends on the work function of the metal but not on the frequency of the incident "
     "light."),
  SP, "B",
  "Threshold frequency and stopping potential",
  "The threshold frequency ν₀ = φ₀/h depends on the work function, which differs from metal to metal, so Statement I "
  "is false. From eV₀ = hν − φ₀, the stopping potential depends on both the frequency of light and the work "
  "function, so Statement II is false.",
  ["ν₀ = φ₀/h, different for different metals → I false",
   "V₀ = (h/e)ν − φ₀/e: increases linearly with ν → II false"],
  why="Statement II is half right: V₀ does depend on φ₀, but it also rises with frequency.",
  ncert=NC + "'Dual Nature of Radiation and Matter', effect of frequency of incident radiation on stopping "
            "potential", seconds=40)

ratio_db = math.sqrt((4 * 2) / (1 * 1))
close(ratio_db, 2 * math.sqrt(2))
q(DUAL, "de Broglie wavelength", "Intermediate", "numerical",
  "A proton and an alpha particle, both initially at rest, are accelerated through the same potential difference. "
  "The ratio of the de Broglie wavelength of the proton to that of the alpha particle (λ_p : λ_α) is:",
  *opt("2√2 : 1", ["2 : 1", "√2 : 1", "1 : 2√2"], "D"),
  "de Broglie wavelength after acceleration: λ = h/√(2mqV)",
  "Through the same V, each particle gains K = qV, so the momentum is √(2mqV) and λ ∝ 1/√(mq).",
  ["λ_p/λ_α = √(m_α q_α/(m_p q_p))", "= √(4 × 2) = √8 = 2√2"],
  why="2 : 1 is the answer for equal kinetic energies (charge ignored). √2 : 1 uses only the charge ratio. 1 : 2√2 "
      "inverts the ratio.",
  seconds=60, rc=True)

q(DUAL, "Photoelectric effect", "Intermediate", "assertion_reason",
  ar("Photoelectric emission begins practically instantaneously (within about 10⁻⁹ s) after light falls on the "
     "metal, even when the light is very dim.",
     "The energy of a photon is proportional to the intensity of the light."),
  AR, "C",
  "Photon picture of the photoelectric effect",
  "A is an experimental fact explained by the photon picture: a single photon gives all its energy hν to a single "
  "electron at once, so there is no time needed to accumulate energy. R is false: a photon's energy is hν and "
  "depends only on frequency; the intensity decides how many photons arrive per second.",
  ["A true: no observable time lag, even at low intensity", "R false: E = hν, independent of intensity"],
  why="Options A and B accept R, which mixes up photon energy with photon number.",
  ncert=NC + "'Dual Nature of Radiation and Matter', photoelectric effect; Einstein's photoelectric equation",
  seconds=40)

# hc/lam - W = 3 and hc/(2 lam) - W = 0.5
E_l = 2 * (3 - 0.5)
W_ = E_l - 3
close(E_l, 5)
close(W_, 2)
close(E_l / 2 - W_, 0.5)
close(HC / E_l, 248)
q(DUAL, "Einstein's equation", "Advanced", "numerical",
  "When a metal surface is illuminated with light of wavelength λ, the stopping potential is 3.0 V. When it is "
  "illuminated with light of wavelength 2λ, the stopping potential is 0.5 V. The work function of the metal is:",
  *opt("2.0 eV", ["2.5 eV", "5.0 eV", "0.5 eV"], "A"),
  "Einstein's photoelectric equation for two wavelengths",
  "Write eV₀ = hc/λ − φ₀ for both cases; doubling the wavelength halves the photon energy. Two equations give both "
  "the photon energy and the work function.",
  ["hc/λ − φ₀ = 3.0 eV … (1)", "hc/(2λ) − φ₀ = 0.5 eV … (2)",
   "(1) − (2): hc/(2λ) = 2.5 eV → hc/λ = 5.0 eV", "φ₀ = 5.0 − 3.0 = 2.0 eV (and λ = 1240/5 = 248 nm)"],
  why="2.5 eV is the photon energy at 2λ, 5.0 eV the photon energy at λ, and 0.5 eV the second stopping potential; "
      "none of them is the work function.",
  seconds=90, rc=True)

E_ph = 6.6e-34 * 3e8 / 660e-9
close(E_ph, 3e-19)
close(3e-3 / E_ph, 1e16)
close(3 / E_ph, 1e19)
close(3e-6 / E_ph, 1e13)
q(DUAL, "Photoelectric effect", "Advanced", "numerical",
  "A laser emits light of wavelength 660 nm with a power of 3 mW. Taking h = 6.6 × 10⁻³⁴ J s and c = 3 × 10⁸ m/s, "
  "the number of photons it emits per second is:",
  *opt("1 × 10¹⁶", ["1 × 10¹⁹", "1 × 10¹³", "3 × 10¹⁶"], "C"),
  "Photon flux: N = P/(hc/λ)",
  "The beam's power is the energy carried per second, and each photon carries hc/λ.",
  ["Energy per photon = hc/λ = (6.6 × 10⁻³⁴ × 3 × 10⁸)/(660 × 10⁻⁹) = 3 × 10⁻¹⁹ J",
   "N = P/E = 3 × 10⁻³/(3 × 10⁻¹⁹) = 1 × 10¹⁶ photons per second"],
  why="1 × 10¹⁹ takes 3 mW as 3 W. 1 × 10¹³ takes it as 3 µW. 3 × 10¹⁶ takes the photon energy as 1 × 10⁻¹⁹ J, "
      "dropping the factor 3 from c.",
  seconds=60, rc=True)

q(DUAL, "de Broglie wavelength", "Advanced", "multi_statement",
  ms("Which of the following statements are correct?",
     ["The maximum kinetic energy of photoelectrons increases linearly with the frequency of the incident light.",
      "The slope of the graph of stopping potential against frequency is h/e, the same for all metals.",
      "Below the threshold frequency, photoelectrons are emitted if the light is intense enough.",
      "A proton and an electron that have the same de Broglie wavelength have the same momentum.",
      "The de Broglie wavelength of a particle does not depend on its speed."]),
  *opt("(a), (b) and (d) only", ["(a), (c) and (d) only", "(b), (d) and (e) only", "(a), (b), (c) and (d) only"], "D"),
  "Photoelectric equation and de Broglie relation",
  "K_max = hν − φ₀ is a straight line in ν (not a proportionality), and eV₀ = hν − φ₀ gives a slope h/e for every "
  "metal. Below ν₀ no electron gets enough energy from one photon, however many photons arrive. λ = h/p, so equal "
  "λ means equal momentum, and λ changes with speed.",
  ["(a) True: K_max = hν − φ₀", "(b) True: V₀ = (h/e)ν − φ₀/e", "(c) False: no emission below ν₀ at any intensity",
   "(d) True: λ = h/p → same λ, same p", "(e) False: λ = h/(mv) falls as speed rises"],
  why="(c) is the classical-wave expectation that the photoelectric effect disproves. (e) ignores p = mv.",
  ncert=NC + "'Dual Nature of Radiation and Matter', Einstein's photoelectric equation; wave nature of matter",
  seconds=75)

# ================================================================ Atoms and Nuclei (B4 I5 A4)
E_n = lambda n, Z=1: -13.6 * Z ** 2 / n ** 2
close(-E_n(2), 3.4)
close(E_n(2) - E_n(1), 10.2)
q(AN, "Bohr model and hydrogen spectrum", "Basic", "numerical",
  "In the Bohr model, the energy of the hydrogen atom in its nth state is −13.6/n² eV. The energy needed to remove "
  "the electron from a hydrogen atom in its first excited state is:",
  *opt("3.4 eV", ["13.6 eV", "10.2 eV", "6.8 eV"], "B"),
  "Energy levels of hydrogen; ionisation from an excited state",
  "The first excited state is n = 2. Removing the electron means taking it to n = ∞, where its energy is zero.",
  ["E₂ = −13.6/4 = −3.4 eV", "Energy needed = 0 − (−3.4) = 3.4 eV"],
  why="13.6 eV is the ionisation energy from the ground state. 10.2 eV is the excitation energy from n = 1 to "
      "n = 2. 6.8 eV divides 13.6 by n instead of n².",
  seconds=30, rc=True)

R_nuc = 1.2 * 125 ** (1 / 3)
close(R_nuc, 6.0)
close(1.2 * 125 ** 0.5, 13.4, rel=2e-3)
q(AN, "Nuclear size and mass defect", "Basic", "numerical",
  "The radius of a nucleus of mass number A is R = R₀A^(1/3), with R₀ = 1.2 fm. The radius of a nucleus with "
  "A = 125 is:",
  *opt("6.0 fm", ["150 fm", "13.4 fm", "0.24 fm"], "A"),
  "Size of the nucleus: R = R₀A^(1/3)",
  "Nuclear volume is proportional to A, so the radius grows as the cube root of A.",
  ["125^(1/3) = 5", "R = 1.2 × 5 = 6.0 fm"],
  why="150 fm multiplies by A itself. 13.4 fm uses the square root of A. 0.24 fm divides R₀ by 5.",
  seconds=25, rc=True)

q(AN, "Rutherford scattering", "Basic", "direct",
  "In Rutherford's alpha-particle scattering experiment, most of the alpha particles passed through the gold foil "
  "without any appreciable deflection. This observation shows that:",
  *opt("most of the space inside an atom is empty",
       ["the positive charge of an atom is spread uniformly over the atom",
        "electrons revolve in fixed circular orbits",
        "the nucleus contains neutrons"], "D"),
  "Conclusions from alpha-particle scattering",
  "If the alpha particles meet nothing massive or highly charged on most paths, the atom must be mostly empty "
  "space. The rare large-angle deflections showed that the positive charge and most of the mass are concentrated "
  "in a tiny nucleus.",
  ["Most particles undeflected → most of the atom is empty space",
   "A few deflected by large angles → tiny, massive, positively charged nucleus"],
  why="A uniform spread of positive charge (Thomson's model) cannot produce the rare large-angle scattering. The "
      "experiment says nothing about electron orbits or neutrons.",
  ncert=NC + "'Atoms', alpha-particle scattering and Rutherford's nuclear model of atom", seconds=25)

close(0.02 * 931.5, 18.63)
q(AN, "Nuclear size and mass defect", "Basic", "numerical",
  "The mass defect of a certain nucleus is 0.02 u. Taking 1 u = 931.5 MeV/c², its binding energy is:",
  *opt("18.63 MeV", ["1.863 MeV", "186.3 MeV", "9.315 MeV"], "C"),
  "Mass–energy equivalence: E_b = Δm c²",
  "The binding energy is the energy equivalent of the mass defect.",
  ["E_b = 0.02 × 931.5 MeV = 18.63 MeV"],
  why="1.863 MeV and 186.3 MeV misplace the decimal point. 9.315 MeV halves the result.",
  seconds=25, rc=True)

ratio_l = (F(1, 4) - F(1, 9)) / (1 - F(1, 4))
assert ratio_l == F(5, 27)
q(AN, "Bohr model and hydrogen spectrum", "Intermediate", "numerical",
  "The ratio of the wavelength of the first line of the Lyman series to that of the first line of the Balmer "
  "series of hydrogen is:",
  *opt("5 : 27", ["27 : 5", "3 : 4", "4 : 9"], "A"),
  "Rydberg formula: 1/λ = R(1/n₁² − 1/n₂²)",
  "The first line of a series is the transition from the next higher level: 2 → 1 for Lyman and 3 → 2 for Balmer.",
  ["Lyman (2 → 1): 1/λ_L = R(1 − 1/4) = 3R/4", "Balmer (3 → 2): 1/λ_B = R(1/4 − 1/9) = 5R/36",
   "λ_L/λ_B = (5R/36)/(3R/4) = 20/108 = 5/27"],
  why="27 : 5 is the inverse ratio (energies, not wavelengths). 3 : 4 and 4 : 9 compare only parts of the two "
      "brackets.",
  seconds=60, rc=True)

r_He = 0.53 * 3 ** 2 / 2
close(r_He, 2.385)
close(0.53 * 9, 4.77)
close(0.53 * 3, 1.59)
close(0.53 * 3 / 2, 0.795)
q(AN, "Bohr model and hydrogen spectrum", "Intermediate", "numerical",
  "The radius of the first Bohr orbit of the hydrogen atom is 0.53 Å. The radius of the orbit with n = 3 in a "
  "singly ionised helium ion (He⁺, Z = 2) is:",
  *opt("2.385 Å", ["4.77 Å", "1.59 Å", "0.795 Å"], "D"),
  "Bohr radius for hydrogen-like ions: r_n = 0.53 n²/Z Å",
  "The radius grows as n² and shrinks as 1/Z because the larger nuclear charge pulls the electron closer.",
  ["r₃ = 0.53 × 3²/2", "= 0.53 × 4.5 = 2.385 Å"],
  why="4.77 Å ignores Z. 1.59 Å uses n instead of n² and ignores Z. 0.795 Å uses n/Z instead of n²/Z.",
  seconds=40, rc=True)

q(AN, "Bohr model and hydrogen spectrum", "Intermediate", "multi_statement",
  ms("Which of the following statements about the Bohr model of the hydrogen atom are correct?",
     ["The lines of the Lyman series lie in the ultraviolet region.",
      "In a stationary orbit, the angular momentum of the electron is an integral multiple of h/2π.",
      "The total energy of the electron in the nth orbit is −13.6/n² eV.",
      "The speed of the electron in its orbit increases as n increases.",
      "An electron in a stationary orbit radiates energy continuously."]),
  *opt("(a), (b) and (c) only", ["(a), (b) and (d) only", "(b), (c) and (e) only", "(a), (b), (c) and (d) only"], "B"),
  "Bohr's postulates and their consequences",
  "Bohr postulated that the electron moves in certain stationary orbits without radiating, with L = nh/2π. It "
  "radiates only when it jumps between orbits. In these orbits r ∝ n², v ∝ 1/n and E = −13.6/n² eV. Transitions to "
  "n = 1 (Lyman series) have the largest energies and lie in the ultraviolet.",
  ["(a) True: Lyman series in the ultraviolet", "(b) True: Bohr's quantisation condition",
   "(c) True: E_n = −13.6/n² eV", "(d) False: v_n ∝ 1/n, so speed falls as n rises",
   "(e) False: stationary orbits are non-radiating"],
  why="(e) is what classical physics predicts and Bohr's postulate denies. (d) reverses v ∝ 1/n.",
  ncert=NC + "'Atoms', Bohr model of the hydrogen atom; the line spectra of the hydrogen atom", seconds=60)

q(AN, "Nuclear size and mass defect", "Intermediate", "statement_pair",
  sp("The density of nuclear matter is nearly the same for all nuclei.",
     "The nuclear force between two nucleons is nearly independent of their charge and acts only over very short "
     "distances, of the order of a few femtometres."),
  SP, "A",
  "Nuclear density and the nuclear force",
  "Since R = R₀A^(1/3), the nuclear volume is proportional to A and so is the mass; the density is therefore nearly "
  "the same (about 2.3 × 10¹⁷ kg m⁻³) for all nuclei. The nuclear force is short-ranged and nearly the same for "
  "n–n, n–p and p–p pairs.",
  ["Volume ∝ R³ ∝ A and mass ∝ A → density independent of A → I true",
   "Nuclear force: short range, charge independent → II true"],
  why="Both statements are standard NCERT facts; neither is false.",
  ncert=NC + "'Nuclei', size of the nucleus; nuclear force", seconds=40)

q(AN, "Fission and fusion", "Intermediate", "match_list",
  ml("Match List-I with List-II.",
     ["Nuclear fission", "Nuclear fusion", "Mass defect",
      "Maximum binding energy per nucleon"],
     ["Nuclei near A = 56 (iron)", "Main source of the Sun's energy",
      "Basis of the energy produced in a nuclear reactor",
      "Difference between the total mass of the free nucleons and the mass of the nucleus"]),
  match_options({"A": "III", "B": "II", "C": "IV", "D": "I"},
                [{"A": "II", "B": "III", "C": "IV", "D": "I"}, {"A": "III", "B": "II", "C": "I", "D": "IV"},
                 {"A": "IV", "B": "II", "C": "III", "D": "I"}], "C"), "C",
  "Fission, fusion and binding energy",
  "Reactors use controlled fission of heavy nuclei. The Sun shines by fusing hydrogen into helium. The mass defect "
  "is the mass that disappears when nucleons bind. Binding energy per nucleon peaks (about 8.75 MeV) near A = 56.",
  ["Fission → nuclear reactor → III", "Fusion → energy of the Sun → II",
   "Mass defect → Σ(nucleon masses) − nuclear mass → IV", "Peak of B/A curve → A ≈ 56 → I"],
  why="Swapping fission and fusion is the usual slip: reactors use fission; stars use fusion.",
  ncert=NC + "'Nuclei', mass–energy and nuclear binding energy; nuclear energy", seconds=40)

Q_f = 2 * 120 * 8.5 - 240 * 7.6
close(Q_f, 216)
q(AN, "Binding energy", "Advanced", "numerical",
  "A nucleus of mass number 240, with a binding energy of 7.6 MeV per nucleon, splits into two nuclei of mass "
  "number 120 each, with a binding energy of 8.5 MeV per nucleon. The energy released in the process is:",
  *opt("216 MeV", ["108 MeV", "0.9 MeV", "432 MeV"], "B"),
  "Energy released = (total binding energy of products) − (total binding energy of the parent)",
  "Energy is released because the products are more tightly bound; the gain in binding energy appears as kinetic "
  "energy of the fragments.",
  ["B.E. of parent = 240 × 7.6 = 1824 MeV", "B.E. of products = 2 × 120 × 8.5 = 2040 MeV",
   "Q = 2040 − 1824 = 216 MeV"],
  shortcut="Total nucleon number is unchanged, so Q = 240 × (8.5 − 7.6) = 216 MeV.",
  why="108 MeV counts only one fragment. 0.9 MeV is the gain per nucleon. 432 MeV counts the gain twice.",
  seconds=60, rc=True)

d_min = 2 * 79 * 1.44 / 5
close(d_min, 45.5, rel=1e-3)
close(79 * 1.44 / 5, 22.75)
q(AN, "Rutherford scattering", "Advanced", "numerical",
  "An alpha particle with a kinetic energy of 5 MeV is directed head-on at a gold nucleus (Z = 79). Taking "
  "e²/(4πε₀) = 1.44 MeV fm, the distance of closest approach is about:",
  *opt("45.5 fm", ["22.8 fm", "91.0 fm", "4.55 fm"], "A"),
  "Distance of closest approach: K = (1/4πε₀)(2e)(Ze)/d",
  "In a head-on approach the alpha particle stops momentarily when all its kinetic energy has become electrostatic "
  "potential energy (the heavy gold nucleus is taken as fixed).",
  ["d = (1/4πε₀)(2Ze²)/K = 2 × 79 × 1.44 MeV fm / 5 MeV", "= 227.52/5 ≈ 45.5 fm"],
  why="22.8 fm takes the alpha particle's charge as e instead of 2e. 91.0 fm doubles once more. 4.55 fm is a "
      "decimal slip.",
  ncert=NC + "'Atoms', alpha-particle trajectory; distance of closest approach", seconds=60, rc=True)

E42 = E_n(4) - E_n(2)
close(E42, 2.55)
close(E42 - 2.0, 0.55)
close(E_n(4) - E_n(1) - 2.0, 10.75)
q(AN, "Bohr model and hydrogen spectrum", "Advanced", "numerical",
  "Photons emitted when hydrogen atoms make the transition from n = 4 to n = 2 fall on a metal of work function "
  "2.0 eV. Taking E_n = −13.6/n² eV, the maximum kinetic energy of the emitted photoelectrons is:",
  *opt("0.55 eV", ["2.55 eV", "10.75 eV", "0.85 eV"], "D"),
  "Hydrogen spectrum combined with Einstein's photoelectric equation",
  "The photon energy equals the difference of the two energy levels. Subtract the work function to get K_max.",
  ["E₄ = −13.6/16 = −0.85 eV, E₂ = −13.6/4 = −3.4 eV", "Photon energy = −0.85 − (−3.4) = 2.55 eV",
   "K_max = 2.55 − 2.0 = 0.55 eV"],
  why="2.55 eV forgets the work function. 10.75 eV uses the 4 → 1 transition (12.75 eV). 0.85 eV is the magnitude "
      "of the n = 4 energy, not a transition energy.",
  seconds=75, rc=True)

q(AN, "Binding energy", "Advanced", "assertion_reason",
  ar("Energy is released both in the fusion of very light nuclei and in the fission of very heavy nuclei.",
     "The binding energy per nucleon is smaller for very light nuclei and for very heavy nuclei than for nuclei of "
     "intermediate mass number."),
  AR, "A",
  "Binding energy curve and nuclear energy",
  "B/A is low for light nuclei, rises to about 8.75 MeV near A = 56 and falls to about 7.6 MeV at "
  "A = 238 (this is R, which is true). Fusing light nuclei or splitting a heavy nucleus gives products with higher "
  "B/A, that is, more tightly bound, and the extra binding energy is released (A, true). So R explains A.",
  ["R true: shape of the B/A versus A curve", "A true: fusion and fission both move towards higher B/A",
   "Higher B/A of the products is why energy is released → R explains A"],
  why="Option B is the trap: R is not merely related; the binding energy curve is exactly why both processes "
      "release energy.",
  ncert=NC + "'Nuclei', mass–energy and nuclear binding energy", seconds=60)

# ================================================================ Electronic Devices (B4 I5 A4)
q(ED, "Semiconductors", "Basic", "direct",
  "Which of the following impurities, when added in small amounts to pure silicon, makes it a p-type "
  "semiconductor?",
  *opt("Boron", ["Arsenic", "Phosphorus", "Antimony"], "C"),
  "Extrinsic semiconductors: acceptor (trivalent) impurities",
  "A trivalent atom such as boron, aluminium or indium has only three valence electrons, so one bond with "
  "neighbouring silicon atoms is incomplete. This creates a hole, making holes the majority carriers.",
  ["Trivalent dopant (B, Al, Ga, In) → acceptor → p-type",
   "Pentavalent dopant (As, P, Sb) → donor → n-type"],
  why="Arsenic, phosphorus and antimony are pentavalent donors, which make n-type silicon.",
  ncert=NC + "'Semiconductor Electronics: Materials, Devices and Simple Circuits', extrinsic semiconductor",
  seconds=20)

f_in = 50
assert 2 * f_in == 100
q(ED, "p-n junction diode and rectifier", "Basic", "numerical",
  "A full-wave rectifier is supplied with a 50 Hz AC input. The fundamental frequency of the ripple in its output "
  "is:",
  *opt("100 Hz", ["50 Hz", "25 Hz", "200 Hz"], "A"),
  "Output of a full-wave rectifier",
  "A full-wave rectifier sends current through the load in the same direction in both halves of each input cycle, "
  "so the output has two pulses per input cycle.",
  ["Input: 50 cycles per second", "Output: 2 pulses per input cycle → 100 pulses per second → 100 Hz"],
  why="50 Hz is the ripple frequency of a half-wave rectifier. 25 Hz halves instead of doubling. 200 Hz doubles "
      "twice.",
  ncert=NC + "'Semiconductor Electronics: Materials, Devices and Simple Circuits', application of junction diode "
            "as a rectifier", seconds=25, rc=True)

NAND = lambda a, b: int(not (a and b))
truth = {(a, b): NAND(a, b) for a in (0, 1) for b in (0, 1)}
assert [k for k, v in truth.items() if v == 0] == [(1, 1)]
q(ED, "Logic gates", "Basic", "direct",
  "A two-input logic gate gives an output 0 only when both its inputs are 1, and an output 1 for every other "
  "combination of inputs. The gate is:",
  *opt("NAND", ["AND", "NOR", "OR"], "B"),
  "Truth tables of basic logic gates",
  "Y = 0 only for A = B = 1 is the opposite of AND (which gives 1 only for A = B = 1). This is the NAND gate, "
  "Y = (A·B)'.",
  ["AND: Y = 1 only when A = B = 1", "NAND = NOT(AND): Y = 0 only when A = B = 1",
   "NOR: Y = 1 only when A = B = 0; OR: Y = 0 only when A = B = 0"],
  why="AND has the opposite outputs. NOR gives 1 only for both inputs 0. OR gives 0 only for both inputs 0.",
  seconds=25)

n_h = (1.5e16) ** 2 / 4.5e22
close(n_h, 5e9)
q(ED, "Semiconductors", "Basic", "numerical",
  "A silicon crystal has an intrinsic carrier concentration of 1.5 × 10¹⁶ m⁻³. It is doped so that the electron "
  "concentration becomes 4.5 × 10²² m⁻³. In thermal equilibrium, the hole concentration is:",
  *opt("5 × 10⁹ m⁻³", ["1.5 × 10¹⁶ m⁻³", "4.5 × 10²² m⁻³", "3.3 × 10⁻⁷ m⁻³"], "D"),
  "Mass-action law: n_e n_h = n_i²",
  "Doping raises one carrier concentration and, by recombination, lowers the other, keeping the product equal to "
  "n_i².",
  ["n_h = n_i²/n_e = (1.5 × 10¹⁶)²/(4.5 × 10²²)", "= 2.25 × 10³²/4.5 × 10²² = 5 × 10⁹ m⁻³"],
  why="1.5 × 10¹⁶ m⁻³ is the intrinsic value, which applies only before doping. 4.5 × 10²² m⁻³ assumes equal "
      "numbers of holes and electrons. 3.3 × 10⁻⁷ m⁻³ divides n_i by n_e without squaring.",
  ncert=NC + "'Semiconductor Electronics: Materials, Devices and Simple Circuits', extrinsic semiconductor",
  seconds=40, rc=True)

I_s = F(10 - 6, 200)
I_L = F(6, 1000)
assert I_s == F(20, 1000) and I_s - I_L == F(14, 1000)
q(ED, "Zener diode", "Intermediate", "numerical",
  "A Zener diode with a breakdown voltage of 6 V is used as a voltage regulator. It is connected through a 200 Ω "
  "series resistor to a 10 V DC supply, and a 1 kΩ load resistor is connected across the Zener diode. The current "
  "through the Zener diode is:",
  *opt("14 mA", ["20 mA", "6 mA", "26 mA"], "A"),
  "Zener regulator: current division between Zener and load",
  "In breakdown the Zener holds 6 V across itself and the load. The series resistor drops the rest of the supply "
  "voltage and carries the total current, which splits between the load and the Zener.",
  ["Voltage across series resistor = 10 − 6 = 4 V → I_s = 4/200 = 20 mA",
   "Load current = 6 V/1000 Ω = 6 mA", "Zener current = 20 − 6 = 14 mA"],
  why="20 mA is the current in the series resistor. 6 mA is the load current. 26 mA adds the load current instead "
      "of subtracting it.",
  ncert=NC + "'Semiconductor Electronics: Materials, Devices and Simple Circuits', Zener diode as a voltage "
            "regulator", seconds=60, rc=True)

AND_ = lambda a, b: int(a and b)
NOR = lambda a, b: int(not (a or b))
assert all(AND_(1 - a, 1 - b) == NOR(a, b) for a in (0, 1) for b in (0, 1))
q(ED, "Logic gates", "Intermediate", "direct",
  "Inputs A and B are each passed through a NOT gate, and the two outputs are fed to an AND gate. The circuit as a "
  "whole behaves as:",
  *opt("a NOR gate", ["a NAND gate", "an OR gate", "an AND gate"], "B"),
  "Combining gates; De Morgan's theorem",
  "The output is Y = A'·B'. By De Morgan's theorem A'·B' = (A + B)', which is the NOR function.",
  ["Truth table: A = 0, B = 0 → 1·1 = 1", "A = 0, B = 1 → 1·0 = 0", "A = 1, B = 0 → 0·1 = 0",
   "A = 1, B = 1 → 0·0 = 0", "Output 1 only for both inputs 0 → NOR"],
  why="NAND would be A' + B' (inverted inputs into an OR gate). OR and AND have different truth tables.",
  seconds=50)

q(ED, "p-n junction diode and rectifier", "Intermediate", "statement_pair",
  sp("When a p-n junction is forward biased, the width of its depletion region decreases.",
     "The small current in a reverse-biased p-n junction diode is due to the majority charge carriers."),
  SP, "C",
  "Biasing of a p-n junction",
  "Forward bias opposes the built-in potential, lowering the barrier and narrowing the depletion region "
  "(Statement I true). In reverse bias the barrier rises, majority carriers cannot cross, and the small current "
  "(of the order of µA) is due to minority carriers drifting across the junction (Statement II false).",
  ["Forward bias: barrier height and depletion width decrease → I true",
   "Reverse current: drift of minority carriers → II false"],
  why="Majority carriers produce the large forward current, not the small reverse current.",
  ncert=NC + "'Semiconductor Electronics: Materials, Devices and Simple Circuits', p-n junction under forward and "
            "reverse bias", seconds=40)

q(ED, "LED, photodiode and solar cell", "Intermediate", "assertion_reason",
  ar("A photodiode is operated under reverse bias.",
     "Under reverse bias, the fractional change in current caused by light is much larger than the fractional "
     "change under forward bias."),
  AR, "A",
  "Why a photodiode is reverse biased",
  "Light creates electron–hole pairs that add to the minority-carrier current. Under forward bias this extra "
  "current is tiny compared with the large majority-carrier current, so it is hard to detect. Under reverse bias the "
  "dark current is very small, so the same photocurrent is a large fraction of it. This is precisely why "
  "photodiodes are reverse biased.",
  ["A true: photodiodes are used in reverse bias",
   "R true: minority-carrier current is small, so light changes it by a large fraction",
   "R is the reason for A → option A"],
  why="Option B would require R to be unrelated to A, but R is the very reason given in NCERT.",
  ncert=NC + "'Semiconductor Electronics: Materials, Devices and Simple Circuits', optoelectronic junction "
            "devices: photodiode", seconds=45)

q(ED, "LED, photodiode and solar cell", "Intermediate", "match_list",
  ml("Match List-I (device) with List-II (how it is operated or used).",
     ["Light emitting diode", "Photodiode", "Solar cell", "Zener diode in a voltage regulator"],
     ["Reverse biased, used to detect optical signals", "Operated in the reverse breakdown region",
      "Forward biased, emits light", "No external bias; generates an emf when light falls on it"]),
  match_options({"A": "III", "B": "I", "C": "IV", "D": "II"},
                [{"A": "I", "B": "III", "C": "IV", "D": "II"}, {"A": "III", "B": "IV", "C": "I", "D": "II"},
                 {"A": "III", "B": "I", "C": "II", "D": "IV"}], "D"), "D",
  "Special-purpose p-n junction devices",
  "An LED emits light when electrons and holes recombine under forward bias. A photodiode is reverse biased to "
  "detect light. A solar cell needs no bias; light generates an emf. A Zener diode regulates voltage in its reverse "
  "breakdown region.",
  ["LED → forward biased, emits light → III", "Photodiode → reverse biased, detects light → I",
   "Solar cell → no external bias, generates emf → IV", "Zener regulator → reverse breakdown → II"],
  why="Swapping the photodiode and the solar cell is the usual slip: one is a detector that needs reverse bias, the "
      "other a source of emf with no bias.",
  ncert=NC + "'Semiconductor Electronics: Materials, Devices and Simple Circuits', special purpose p-n junction "
            "diodes", seconds=40)

I_net = F(6, 1 + 2)
assert I_net == 2
assert F(6, 1 + F(2 * 1, 2 + 1)) == F(18, 5) and F(6, 1 + 1) == 3 and F(6, 1 + 2 + 1) == F(3, 2)
q(ED, "p-n junction diode and rectifier", "Advanced", "numerical",
  "A 6 V battery of negligible internal resistance is connected in series with a 1 kΩ resistor to two parallel "
  "branches. Branch P contains an ideal diode that is forward biased by the battery, in series with a 2 kΩ "
  "resistor. Branch Q contains an ideal diode that is reverse biased by the battery, in series with a 1 kΩ "
  "resistor. The current drawn from the battery is:",
  *opt("2 mA", ["3.6 mA", "3 mA", "1.5 mA"], "C"),
  "Ideal diodes in DC circuits",
  "An ideal diode is a short circuit when forward biased and an open circuit when reverse biased. So branch Q "
  "carries no current and the circuit reduces to 1 kΩ and 2 kΩ in series.",
  ["Branch Q: reverse-biased diode → open → no current",
   "Branch P: forward-biased diode → short → 2 kΩ", "I = 6 V/(1 kΩ + 2 kΩ) = 2 mA"],
  why="3.6 mA lets both branches conduct (2 kΩ ∥ 1 kΩ in series with 1 kΩ). 3 mA lets only branch Q conduct. "
      "1.5 mA adds all three resistors in series.",
  seconds=75, rc=True)

R_led = F(9 - 2, F(20, 1000))
assert R_led == 350 and R_led * F(20, 1000) ** 2 == F(14, 100) and 2 * F(20, 1000) == F(4, 100)
assert F(9, F(20, 1000)) == 450
q(ED, "LED, photodiode and solar cell", "Advanced", "numerical",
  "An LED has a forward voltage of 2.0 V when it carries its rated current of 20 mA. It is to be run from a 9 V DC "
  "supply through a series resistor. The resistance needed and the power dissipated in that resistor are:",
  *opt("350 Ω and 0.14 W", ["450 Ω and 0.18 W", "350 Ω and 0.04 W", "100 Ω and 0.04 W"], "B"),
  "Series resistor for an LED: R = (V_supply − V_LED)/I",
  "The LED fixes its own forward voltage; the resistor must drop the remaining voltage at the rated current.",
  ["Voltage across resistor = 9 − 2 = 7 V", "R = 7 V/0.02 A = 350 Ω",
   "Power in resistor = I²R = (0.02)² × 350 = 0.14 W (= 7 V × 0.02 A)"],
  why="450 Ω and 0.18 W ignore the LED's forward voltage. 0.04 W is the power in the LED (2 V × 20 mA), not in the "
      "resistor. 100 Ω uses the LED's voltage instead of the resistor's.",
  seconds=75, rc=True)

q(ED, "Semiconductors", "Advanced", "multi_statement",
  ms("Which of the following statements about semiconductors are correct?",
     ["In an intrinsic semiconductor, the number density of free electrons equals that of holes.",
      "In a p-type semiconductor, holes are the minority carriers.",
      "Doping silicon with a trivalent impurity produces an n-type semiconductor.",
      "The energy band gap of silicon is larger than that of germanium.",
      "In an n-type semiconductor, electrons are the majority carriers, and the material as a whole is electrically "
      "neutral."]),
  *opt("(a), (d) and (e) only", ["(a), (b) and (d) only", "(a), (c), (d) and (e) only", "(b), (c) and (e) only"], "A"),
  "Intrinsic and extrinsic semiconductors",
  "In a pure crystal each thermally freed electron leaves one hole, so n_e = n_h. Trivalent dopants give holes "
  "(p-type), with holes as the majority carriers; pentavalent dopants give electrons (n-type). Doping adds neutral "
  "atoms, so a doped crystal stays neutral. The band gap is about 1.1 eV for Si and 0.7 eV for Ge.",
  ["(a) True: n_e = n_h = n_i", "(b) False: holes are the majority carriers in p-type",
   "(c) False: trivalent impurity → p-type", "(d) True: E_g(Si) ≈ 1.1 eV > E_g(Ge) ≈ 0.7 eV",
   "(e) True: majority electrons, but overall neutral"],
  why="A common misconception is that n-type material is negatively charged; it is neutral, because every donor "
      "electron leaves behind a positive donor ion.",
  ncert=NC + "'Semiconductor Electronics: Materials, Devices and Simple Circuits', intrinsic and extrinsic "
            "semiconductors", seconds=60)

q(ED, "Zener diode", "Advanced", "multi_statement",
  ms("Which of the following statements about rectifiers and the Zener diode are correct?",
     ["In a centre-tap full-wave rectifier, both diodes conduct at the same time.",
      "The output of a rectifier without a filter is a pulsating (fluctuating) DC voltage.",
      "A Zener diode is made by heavily doping both its p- and n-sides, which makes its depletion region very thin.",
      "In a half-wave rectifier, current flows through the load during only one half of each input cycle.",
      "A Zener voltage regulator keeps the output voltage nearly constant even when the input voltage changes."]),
  *opt("(b), (c), (d) and (e) only", ["(a), (b), (c) and (e) only", "(b), (d) and (e) only", "(a), (c) and (d) only"],
       "C"),
  "Rectifier action and Zener regulation",
  "In a centre-tap rectifier the two diodes conduct in alternate half-cycles. Without a filter, the output is "
  "unidirectional but pulsating. A Zener diode is heavily doped, so its depletion layer is thin and the field is "
  "strong enough for breakdown at a low, sharp voltage; in breakdown the voltage across it stays nearly constant "
  "over a wide range of current.",
  ["(a) False: the diodes conduct alternately", "(b) True: pulsating DC", "(c) True: heavy doping, thin "
   "depletion layer", "(d) True: half-wave rectifier passes one half-cycle", "(e) True: voltage regulation"],
  why="Options containing (a) are wrong; the option with only (b), (d) and (e) leaves out the true statement (c).",
  ncert=NC + "'Semiconductor Electronics: Materials, Devices and Simple Circuits', rectifier; Zener diode",
  seconds=60)

# ================================================================ Experimental Skills (B2 I3 A2)
LC_v = F(1, 1) - F(9, 10)  # mm
assert LC_v == F(1, 10)
assert F(24) + 6 * LC_v == F(246, 10)  # mm
q(EXP, "Vernier calipers and screw gauge", "Basic", "numerical",
  "In a vernier calipers, one main scale division is 1 mm and 10 vernier scale divisions coincide with 9 main scale "
  "divisions. While measuring the diameter of a rod (with no zero error), the main scale reading is 2.4 cm and the "
  "6th vernier division coincides with a main scale division. The diameter of the rod is:",
  *opt("2.46 cm", ["2.406 cm", "3.00 cm", "2.94 cm"], "B"),
  "Vernier calipers: least count = 1 MSD − 1 VSD; reading = MSR + (VSC × LC)",
  "The least count is the difference between one main-scale and one vernier-scale division.",
  ["1 VSD = 9/10 MSD = 0.9 mm → LC = 1 − 0.9 = 0.1 mm = 0.01 cm",
   "Reading = 2.4 cm + 6 × 0.01 cm = 2.46 cm"],
  why="2.406 cm takes the least count as 0.01 mm. 3.00 cm adds 6 mm instead of 6 × 0.1 mm. 2.94 cm adds "
      "6 × 0.9 mm, the length of 6 vernier divisions.",
  seconds=40, rc=True)

q(EXP, "Mechanics experiments", "Basic", "match_list",
  ml("Match List-I (laboratory set-up) with List-II (quantity it is used to determine).",
     ["Metre bridge", "Resonance tube", "Steel ball falling at terminal velocity through glycerine",
      "Capillary rise in a glass tube"],
     ["Surface tension of water", "Speed of sound in air", "Resistivity of the material of a wire",
      "Coefficient of viscosity of the liquid"]),
  match_options({"A": "III", "B": "II", "C": "IV", "D": "I"},
                [{"A": "II", "B": "III", "C": "IV", "D": "I"}, {"A": "III", "B": "II", "C": "I", "D": "IV"},
                 {"A": "III", "B": "IV", "C": "II", "D": "I"}], "A"), "A",
  "Standard NEET laboratory experiments",
  "Each set-up isolates one quantity: a metre bridge compares resistances, a resonance tube finds λ at a known "
  "frequency, terminal velocity in a viscous liquid gives η by Stokes' law, and capillary rise gives surface "
  "tension.",
  ["Metre bridge → unknown resistance → resistivity ρ = RA/l → III",
   "Resonance tube → resonating lengths → λ → v = fλ → II",
   "Terminal velocity → η = 2r²(ρ − σ)g/(9v) → IV", "Capillary rise h → S = hρgr/(2 cos θ) → I"],
  why="Mixing up the two fluid experiments (viscosity and surface tension) is the most likely slip.",
  seconds=35)

LC_s = F(5, 10) / 50  # mm
obs = F(35, 10) + 42 * LC_s
assert LC_s == F(1, 100) and obs == F(392, 100) and obs - F(3, 100) == F(389, 100)
assert F(35, 10) + 42 * F(5, 1000) - F(3, 100) == F(368, 100)
q(EXP, "Vernier calipers and screw gauge", "Intermediate", "numerical",
  "A screw gauge has a pitch of 0.5 mm and 50 divisions on its circular scale. With the studs closed it shows a "
  "positive zero error of +0.03 mm. While measuring the diameter of a wire, the main scale reading is 3.5 mm and the "
  "42nd circular division is on the reference line. The corrected diameter of the wire is:",
  *opt("3.89 mm", ["3.95 mm", "3.92 mm", "3.68 mm"], "D"),
  "Screw gauge: least count = pitch/number of circular divisions; true reading = observed reading − zero error",
  "A positive zero error means the gauge reads too much, so it is subtracted from every reading.",
  ["LC = 0.5 mm/50 = 0.01 mm", "Observed = 3.5 + 42 × 0.01 = 3.92 mm", "Corrected = 3.92 − (+0.03) = 3.89 mm"],
  why="3.95 mm adds the positive zero error instead of subtracting it. 3.92 mm ignores the zero error. 3.68 mm takes "
      "the least count as 0.005 mm.",
  seconds=60, rc=True)

q(EXP, "Mechanics experiments", "Intermediate", "assertion_reason",
  ar("In the simple pendulum experiment, the time for 20 or more oscillations is measured rather than the time for "
     "a single oscillation.",
     "Timing many oscillations reduces the least count of the stop-watch."),
  AR, "C",
  "Reducing percentage error in timing",
  "The least count of a stop-watch is fixed by its design (for example 0.1 s) and the reaction-time error at start "
  "and stop is about the same however long the timing is. Spreading this fixed error over 20 periods makes the "
  "error in one period, and the percentage error, 20 times smaller. So A is true and R is false.",
  ["A true: standard practice for the pendulum experiment",
   "R false: the least count does not change; the percentage error in T falls"],
  why="Options A and B accept R; the least count is a property of the instrument, not of the measurement.",
  seconds=40)

q(EXP, "Optics experiments", "Intermediate", "statement_pair",
  sp("In the u–v method for finding the focal length of a concave mirror, a graph of 1/v against 1/u (magnitudes) "
     "is a straight line that cuts both axes at 1/f.",
     "In the experiment to plot the i–δ curve of a prism, the angle of deviation first decreases and then increases "
     "as the angle of incidence is increased."),
  SP, "A",
  "Graphical methods in optics experiments",
  "For a real image formed by a concave mirror, 1/|v| + 1/|u| = 1/|f|, a straight line of slope −1 with both "
  "intercepts equal to 1/|f| (Statement I true). For a prism, δ falls to a minimum (δm) at one angle of incidence and "
  "rises again on either side (Statement II true).",
  ["1/|v| = −1/|u| + 1/|f| → straight line, intercepts 1/f on both axes → I true",
   "i–δ curve: δ decreases, reaches δm, then increases → II true"],
  why="Neither statement is false; a graph of v against u would be a hyperbola, which is perhaps why the first "
      "statement looks doubtful.",
  seconds=50)

pct = 2 * 1 + 2 + 0.5
close(pct, 4.5)
close(1 + 2 + 0.5, 3.5)
q(EXP, "Electrical experiments", "Advanced", "numerical",
  "In an experiment to find the resistivity of the material of a wire using ρ = πd²R/(4L), the percentage errors "
  "in measuring the diameter d, resistance R and length L are 1%, 2% and 0.5% respectively. The maximum percentage "
  "error in ρ is:",
  *opt("4.5%", ["3.5%", "2.5%", "5.0%"], "C"),
  "Propagation of errors: for ρ = k dᵃ Rᵇ L⁻ᶜ, Δρ/ρ = a(Δd/d) + b(ΔR/R) + c(ΔL/L)",
  "Relative errors add for products and quotients, each multiplied by the power of the quantity. Errors are always "
  "added, even for quantities in the denominator.",
  ["Δρ/ρ = 2(Δd/d) + ΔR/R + ΔL/L", "= 2 × 1% + 2% + 0.5% = 4.5%"],
  why="3.5% forgets the power 2 on d. 2.5% leaves out d altogether. 5.0% counts the error in L twice.",
  seconds=50, rc=True)

eta = 2 * (1e-3) ** 2 * (7800 - 1050) * 10 / (9 * 0.05)
close(eta, 0.3)
close(eta / 2, 0.15)
close(2 * (2e-3) ** 2 * 6750 * 10 / (9 * 0.05), 1.2)
close(2 * (1e-3) ** 2 * 7800 * 10 / (9 * 0.05), 0.3467)
q(EXP, "Thermal and fluid experiments", "Advanced", "numerical",
  "In an experiment, a steel ball of diameter 2 mm (density 7800 kg/m³) falls through glycerine (density "
  "1050 kg/m³) and reaches a terminal velocity of 5 cm/s. Taking g = 10 m/s², the coefficient of viscosity of "
  "glycerine is:",
  *opt("0.30 Pa s", ["0.15 Pa s", "1.2 Pa s", "0.35 Pa s"], "B"),
  "Stokes' law at terminal velocity: v_t = 2r²(ρ − σ)g/(9η)",
  "At terminal velocity the weight is balanced by buoyancy plus viscous drag, 6πηrv_t = (4/3)πr³(ρ − σ)g.",
  ["r = 1 mm = 1 × 10⁻³ m, ρ − σ = 7800 − 1050 = 6750 kg/m³",
   "η = 2r²(ρ − σ)g/(9v_t) = 2 × 10⁻⁶ × 6750 × 10/(9 × 0.05)", "= 0.135/0.45 = 0.30 Pa s"],
  why="0.15 Pa s drops the factor 2. 1.2 Pa s uses the diameter as the radius. 0.35 Pa s ignores buoyancy "
      "(uses ρ instead of ρ − σ).",
  seconds=90, rc=True)

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
    assert len(QS) == pkg["count"] == 115
    for x in QS:
        assert x["subtopic"] in subs[x["topic"]], (x["question_id"], x["subtopic"])
    # topics stay in plan order, so IDs are grouped by topic
    order = [x["topic"] for x in QS]
    assert order == sorted(order, key=pkg["topics"].index)
    fmts = Counter(x["format"] for x in QS)
    assert 0.53 <= fmts["numerical"] / len(QS) <= 0.58, fmts
    for f_ in ("direct", "assertion_reason", "statement_pair", "match_list", "multi_statement"):
        assert fmts[f_] >= 0.08 * len(QS), (f_, fmts)
    keys = Counter(x["correct_answer"] for x in QS)
    assert all(26 <= keys[k] <= 32 for k in LETTERS), keys
    texts = [x["question_text"] for x in QS]
    assert len(set(texts)) == len(texts)
    doc = {"schema_version": "1.0", "batch_id": "BATCH_001", "created_at": TODAY,
           "notes": "Package PHY_001_p2: 115 original Physics questions (Current Electricity to Experimental Skills), "
                    "NEET_PHY_000136..000250. Numerical answers recomputed by tools/batch_001/PHY_001_p2.py.",
           "stimuli": [], "questions": QS}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {OUT}: {len(QS)} questions")
    print("difficulty", dict(Counter(x["difficulty"] for x in QS)))
    print("formats", dict(fmts))
    print("keys", dict(sorted(keys.items())))


if __name__ == "__main__":
    main()
