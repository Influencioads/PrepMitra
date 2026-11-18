"""Builder for batches/parts/BATCH_006_PHY_p2.json (package PHY_006_p2 of BATCH_006).

Physics, 119 original questions, NEET_PHY_001382..NEET_PHY_001500: Current Electricity, Magnetic Effects of Current
and Magnetism, Electromagnetic Induction and Alternating Currents, Electromagnetic Waves, Optics, Dual Nature of
Matter and Radiation, Atoms and Nuclei, Electronic Devices, Experimental Skills.

Every numerical answer is recomputed below with an assert next to its question; multi-statement, assertion-reason
and statement-pair keys are derived from truth tables; the plan quota, format mix and answer-key balance are
asserted before anything is written. If any assert fails, nothing is written.

    python tools/batch_006/PHY_006_p2.py        (run from docs/neet-bank)
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
PLAN = ROOT / "batches" / "plans" / "BATCH_006_plan.json"
OUT = ROOT / "batches" / "parts" / "BATCH_006_PHY_p2.json"
PACKAGE = "PHY_006_p2"
FIRST_ID = 1382
COUNT = 119

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
q_ce1 = 2 * 3 + 4 * 3 ** 2 / 2
assert q_ce1 == 24
assert (2 + 4 * 3) * 3 == 42 and 4 * 3 ** 2 == 36 and 2 * 3 == 6
q(CE, "Drift velocity and Ohm's law", "Basic", "numerical",
  "The current in a conductor varies with time as I = (2 + 4t) A, where t is in seconds. The charge that flows "
  "through any cross-section of the conductor between t = 0 and t = 3 s is:",
  *opt("24 C", ["42 C", "36 C", "6 C"], "A"),
  "Current is the rate of flow of charge: q = ∫I dt (area under the I–t graph)",
  "When the current changes with time, the charge is the area under the current–time graph, not the final current "
  "multiplied by the time.",
  ["q = ∫₀³ (2 + 4t) dt = [2t + 2t²]₀³", "q = 6 + 18 = 24 C"],
  shortcut="I rises linearly from 2 A to 14 A, so the average current is 8 A and q = 8 × 3 = 24 C.",
  why="42 C multiplies the final current (14 A) by the whole time. 36 C integrates 4t as 4t² instead of 2t² and "
      "leaves out the constant part. 6 C keeps only the constant 2 A part.",
  ncert=CEC + "electric current", seconds=40, rc=True)

R_tri = F(6 * 12, 6 + 12)
assert R_tri == 4
q(CE, "Combination of resistors", "Basic", "numerical",
  "Three resistors, each of 6 Ω, are connected to form a triangle. The equivalent resistance between any two corners "
  "of the triangle is:",
  *opt("4 Ω", ["18 Ω", "2 Ω", "3 Ω"], "B"),
  "Series and parallel combination",
  "Between two corners, one resistor connects them directly and the other two form a 12 Ω series path; these two "
  "paths are in parallel.",
  ["Direct path: 6 Ω; other path: 6 + 6 = 12 Ω", "R = (6 × 12)/(6 + 12) = 4 Ω"],
  why="18 Ω puts all three resistors in series. 2 Ω puts all three in parallel. 3 Ω takes the two paths as 6 Ω "
      "each.",
  ncert=CEC + "combination of resistors - series and parallel", seconds=30, rc=True)

q(CE, "Combination of resistors", "Basic", "statement_pair",
  sp("When resistors are connected in series across a battery, the same current flows through each of them.",
     "When resistors are connected in parallel across a battery, the potential difference across each resistor is "
     "inversely proportional to its resistance."),
  SP, sp_key(True, False),
  "Series: common current; parallel: common potential difference",
  "In a series connection there is only one path, so the current is the same in every resistor (Statement I true). "
  "In a parallel connection every resistor is connected between the same two points, so the potential difference "
  "is the same across each; it is the current that is inversely proportional to the resistance (Statement II "
  "false).",
  ["Series: I same in all → I true", "Parallel: V same across all; I ∝ 1/R → II false"],
  why="Statement II confuses the current (which divides inversely as R) with the potential difference (which is "
      "common to all the resistors).",
  ncert=CEC + "combination of resistors - series and parallel", seconds=30)

q(CE, "Resistivity and temperature", "Basic", "direct",
  "The current–voltage (I–V) graphs of the same metal wire, taken at two different temperatures T₁ and T₂, are "
  "straight lines through the origin, the line for T₁ being steeper (larger slope, I plotted against V) than the "
  "line for T₂. It follows that:",
  *opt("T₁ is lower than T₂, because the wire has a smaller resistance at T₁",
       ["T₁ is higher than T₂, because a steeper I–V line means a larger resistance",
        "T₁ is equal to T₂, because the slope of an I–V graph does not depend on temperature",
        "T₁ is higher than T₂, because the resistivity of a metal decreases as its temperature rises"], "D"),
  "Slope of the I–V graph = 1/R; the resistance of a metal increases with temperature",
  "For an I–V graph, the slope is I/V = 1/R. A steeper line means a smaller resistance. The resistance of a metal "
  "wire increases with temperature, so the smaller resistance belongs to the lower temperature.",
  ["Slope of I–V line = 1/R → line for T₁ has the smaller R", "R of a metal rises with temperature → T₁ < T₂"],
  why="A steeper I–V line means a smaller, not larger, resistance. The slope does depend on temperature because R "
      "does. The resistivity of a metal increases, not decreases, with temperature.",
  ncert=CEC + "temperature dependence of resistivity", seconds=35)

q(CE, "Kirchhoff's laws", "Basic", "statement_pair",
  sp("While applying Kirchhoff's loop rule, when a resistor R is traversed in the direction of the current I "
     "through it, the change in potential is −IR.",
     "While applying Kirchhoff's loop rule, when an ideal cell of emf ε is traversed from its negative terminal to "
     "its positive terminal, the change in potential is +ε."),
  SP, sp_key(True, True),
  "Sign conventions of the loop rule",
  "Current flows through a resistor from higher to lower potential, so going along the current the potential falls "
  "by IR (Statement I true). The positive terminal of a cell is at a potential ε higher than its negative terminal, "
  "so going from − to + the potential rises by ε (Statement II true).",
  ["Along the current in R: potential drops by IR → change −IR → I true",
   "Ideal cell, − to +: potential rises by ε → change +ε → II true"],
  why="Both sign conventions are correct, so the options that call either statement false are wrong.",
  ncert=CEC + "Kirchhoff's rules", seconds=30)

# ---- Intermediate
v_ce = solve_network(4, [(2, 1, 2), (3, 1, 2), (1, 0, 4)], {0: 0, 2: 12, 3: 6})
assert v_ce[1] == F(36, 5)
I_Y = (v_ce[1] - 6) / 2
assert I_Y == F(3, 5)          # positive: current flows from the common positive line INTO Y's positive terminal
assert v_ce[1] / 4 == F(9, 5) and F(6, 4) == F(3, 2)
q(CE, "Kirchhoff's laws", "Intermediate", "numerical",
  "Battery X (emf 12 V, internal resistance 2 Ω) and battery Y (emf 6 V, internal resistance 2 Ω) are connected in "
  "parallel, positive terminal to positive terminal and negative terminal to negative terminal, and a 4 Ω resistor "
  "is connected across the combination. The current through battery Y is:",
  *opt("0.6 A, flowing into its positive terminal (Y is being charged)",
       ["0.6 A, flowing out of its positive terminal",
        "1.5 A, flowing out of its positive terminal",
        "1.8 A, flowing out of its positive terminal"], "C"),
  "Kirchhoff's junction rule at the common positive terminal",
  "Let V be the potential of the common positive line (negative line at 0 V). The currents leaving the line through "
  "the two batteries' internal resistances and the 4 Ω resistor must add to zero.",
  ["(12 − V)/2 + (6 − V)/2 = V/4", "Multiply by 4: 24 − 2V + 12 − 2V = V → 5V = 36 → V = 7.2 V",
   "Current through Y = (7.2 − 6)/2 = 0.6 A, from the positive line into Y's positive terminal"],
  why="0.6 A out of the positive terminal has the right size but the wrong direction: the common terminal "
      "voltage (7.2 V) exceeds Y's emf, so Y is charged. 1.5 A treats Y as if it alone fed the 4 Ω resistor. 1.8 A "
      "is the current in the 4 Ω resistor.",
  ncert=CEC + "Kirchhoff's rules", seconds=90, rc=True)

R20, R120 = F(10), F(10) * 60 / 40
alpha_mb = (R120 - R20) / (R20 * 100)
assert R120 == 15 and alpha_mb == F(5, 1000)
assert F(15, 10) / 100 == F(15, 1000)
assert (R120 - R20) / (R120 * 100) == F(1, 300)
assert (F(10) * 60 / 50 - R20) / (R20 * 100) == F(2, 1000)
q(CE, "Wheatstone and metre bridge", "Intermediate", "numerical",
  "A coil of wire is placed in the left gap of a metre bridge and a standard 10.0 Ω resistor in the right gap. With "
  "the coil at 20 °C, the null point is 50.0 cm from the left end of the wire. The coil alone is then heated to "
  "120 °C (the standard resistor stays at 20 °C), and the null point moves to 60.0 cm from the left end. Taking the "
  "temperature coefficient of resistance of the coil's material as constant and referred to 20 °C, its value is:",
  *opt("5.0 × 10⁻³ °C⁻¹", ["1.5 × 10⁻² °C⁻¹", "3.3 × 10⁻³ °C⁻¹", "2.0 × 10⁻³ °C⁻¹"], "A"),
  "Metre bridge balance X/R = l/(100 − l) combined with R_T = R₂₀[1 + α(T − 20)]",
  "At 20 °C the null point is at the middle, so the coil has 10.0 Ω. At 120 °C the balance gives the hot "
  "resistance, and the fractional increase divided by the temperature rise is α.",
  ["At 20 °C: X = 10 × 50/50 = 10.0 Ω", "At 120 °C: X = 10 × 60/40 = 15.0 Ω",
   "α = (15 − 10)/(10 × 100) = 5.0 × 10⁻³ °C⁻¹"],
  why="1.5 × 10⁻² °C⁻¹ divides the ratio R_T/R₂₀ (not the fractional increase) by ΔT. 3.3 × 10⁻³ °C⁻¹ divides the "
      "increase by the hot resistance instead of the resistance at 20 °C. 2.0 × 10⁻³ °C⁻¹ uses 60/50 instead of "
      "60/40 for the balance ratio.",
  ncert=CEC + "Wheatstone bridge; temperature dependence of resistivity", seconds=90, rc=True)

nCu, nAl, ACu, AAl = 8.0, 6.0, 1.0, 2.0
ratio_vd = (nAl * AAl) / (nCu * ACu)
close(ratio_vd, 1.5)
close(1 / ratio_vd, 0.667, 1e-3)
close(nAl / nCu, 0.75)
q(CE, "Drift velocity and Ohm's law", "Intermediate", "numerical",
  "A copper wire of cross-sectional area 1.0 mm² is joined end to end with an aluminium wire of cross-sectional "
  "area 2.0 mm², and a steady current flows through the two wires in series. The number densities of free "
  "electrons are 8.0 × 10²⁸ m⁻³ in copper and 6.0 × 10²⁸ m⁻³ in aluminium. The ratio of the drift speed of the "
  "electrons in the copper wire to that in the aluminium wire is:",
  *opt("1.5", ["0.67", "2.0", "0.75"], "D"),
  "I = neAv_d with the same current in both wires",
  "In series the current is the same, so n A v_d is the same in both wires and v_d ∝ 1/(nA).",
  ["n_Cu A_Cu v_Cu = n_Al A_Al v_Al", "v_Cu/v_Al = (n_Al A_Al)/(n_Cu A_Cu) = (6.0 × 2.0)/(8.0 × 1.0) = 1.5"],
  why="0.67 inverts the ratio. 2.0 uses the areas alone and ignores the electron densities. 0.75 uses the electron "
      "densities alone and ignores the areas.",
  ncert=CEC + "drift of electrons and the origin of resistivity", seconds=50, rc=True)

q(CE, "Resistivity and temperature", "Intermediate", "assertion_reason",
  ar("The resistance of the tungsten filament of an electric bulb is much larger when the bulb is glowing than when "
     "it is cold.",
     "The resistivity of a metal increases as its temperature rises."),
  AR, ar_key(True, True, True),
  "Temperature dependence of the resistivity of metals",
  "A glowing filament is at a very high temperature (well above 2000 °C). Since the resistivity of a metal rises "
  "with temperature, the hot filament has a much higher resistance than the cold one. R gives exactly this reason.",
  ["Glowing filament → very high temperature", "ρ of a metal increases with T → R = ρl/A increases",
   "R explains A"],
  why="Both statements are true and the rise of resistivity with temperature is the cause of the larger hot "
      "resistance, so R correctly explains A.",
  ncert=CEC + "temperature dependence of resistivity", seconds=35)

I_c5 = F(12, 5 + 1)
assert I_c5 == 2 and 12 - I_c5 * 1 == 10 and I_c5 ** 2 * 5 == 20 and I_c5 ** 2 * 1 == 4 and F(12, 1) == 12
q(CE, "Cells, emf and internal resistance", "Intermediate", "multi_statement",
  ms("A cell of emf 12 V and internal resistance 1 Ω is connected across an external resistor of 5 Ω. Which of the "
     "following statements are correct?",
     ["The current in the circuit is 2 A.",
      "The potential difference between the terminals of the cell is 10 V.",
      "The power dissipated in the 5 Ω resistor is 24 W.",
      "The power dissipated inside the cell is 4 W.",
      "If the 5 Ω resistor is replaced by a wire of negligible resistance, the current becomes 6 A."]),
  *mso({"a": True, "b": True, "c": False, "d": True, "e": False}, "abd", ["abc", "bde", "ad"], "B"),
  "I = ε/(R + r), V = ε − Ir, P = I²R",
  "I = 12/(5 + 1) = 2 A (a true). V = 12 − 2 × 1 = 10 V (b true). Power in the 5 Ω resistor = 2² × 5 = 20 W, not "
  "24 W; 24 W is the total power εI (c false). Power inside the cell = 2² × 1 = 4 W (d true). With R = 0, the current "
  "is ε/r = 12 A, not 6 A (e false).",
  ["(a) I = 2 A → true", "(b) V = 10 V → true", "(c) 20 W, not 24 W → false", "(d) 4 W → true",
   "(e) short-circuit current 12 A → false"],
  why="Options containing (c) or (e) include a false statement; (a) and (d) only leaves out the true statement (b).",
  ncert=CEC + "cells, emf, internal resistance; electrical power", seconds=75)

q(CE, "Resistivity and temperature", "Intermediate", "match_list",
  ml("Match each material in List-I with its approximate resistivity at room temperature in List-II, as tabulated "
     "in NCERT.",
     ["Copper", "Nichrome", "Germanium", "Glass"],
     ["10¹⁰ to 10¹⁴ Ω m", "1.7 × 10⁻⁸ Ω m", "0.46 Ω m", "about 1.0 × 10⁻⁶ Ω m"]),
  *mlo("A-II, B-IV, C-III, D-I",
       ["A-IV, B-II, C-III, D-I", "A-II, B-III, C-IV, D-I", "A-II, B-IV, C-I, D-III"], "C"),
  "Resistivities of metals, alloys, semiconductors and insulators",
  "Metals such as copper have the lowest resistivities (about 10⁻⁸ Ω m). Alloys such as nichrome are about a "
  "hundred times more resistive (about 10⁻⁶ Ω m). Semiconductors such as germanium lie in between (0.46 Ω m), and "
  "insulators such as glass have enormous resistivities (10¹⁰–10¹⁴ Ω m).",
  ["Copper → 1.7 × 10⁻⁸ Ω m (II)", "Nichrome → ~10⁻⁶ Ω m (IV)", "Germanium → 0.46 Ω m (III)",
   "Glass → 10¹⁰–10¹⁴ Ω m (I)"],
  why="A-IV, B-II swaps the metal and the alloy. B-III, C-IV gives the alloy a semiconductor's resistivity. C-I, "
      "D-III swaps the semiconductor and the insulator.",
  ncert=CEC + "resistivity of various materials (table)", seconds=50)

P_ser = {r: F(12, 16) ** 2 * r for r in (4, 12)}
P_par = {r: F(12) ** 2 / r for r in (4, 12)}
assert P_ser == {4: F(9, 4), 12: F(27, 4)} and P_par == {4: 36, 12: 12}
q(CE, "Combination of resistors", "Intermediate", "match_list",
  ml("A 4 Ω resistor and a 12 Ω resistor are connected to an ideal 12 V battery, first in series with each other and "
     "then in parallel with each other. Match each case in List-I with the power dissipated in List-II.",
     ["Power in the 4 Ω resistor, series connection", "Power in the 12 Ω resistor, series connection",
      "Power in the 4 Ω resistor, parallel connection", "Power in the 12 Ω resistor, parallel connection"],
     ["12 W", "2.25 W", "36 W", "6.75 W"]),
  *mlo("A-II, B-IV, C-III, D-I",
       ["A-IV, B-II, C-III, D-I", "A-II, B-IV, C-I, D-III", "A-III, B-I, C-II, D-IV"], "A"),
  "Series: same current, P = I²R; parallel: same voltage, P = V²/R",
  "In series the current is 12/16 = 0.75 A in both, so the larger resistor takes more power. In parallel each "
  "resistor has the full 12 V, so the smaller resistor takes more power.",
  ["Series: I = 0.75 A → P₄ = 0.5625 × 4 = 2.25 W, P₁₂ = 0.5625 × 12 = 6.75 W",
   "Parallel: P₄ = 144/4 = 36 W, P₁₂ = 144/12 = 12 W"],
  why="A-IV, B-II gives the smaller resistor more power in series. C-I, D-III gives the larger resistor more power "
      "in parallel. A-III, B-I, C-II, D-IV swaps the series and parallel results.",
  ncert=CEC + "electrical power; combination of resistors", seconds=70, rc=True)

# ---- Advanced
x_lad = F(2)
for _ in range(60):
    x_lad = 2 + 2 * x_lad / (2 + x_lad)
close(float(x_lad), 1 + math.sqrt(5), 1e-9)
close(1 + math.sqrt(5), 3.236, 1e-3)
close(2 * (1 + math.sqrt(3)), 5.464, 1e-3)
q(CE, "Combination of resistors", "Advanced", "numerical",
  "An infinitely long ladder network is made of identical 2 Ω resistors. Each section of the ladder has one 2 Ω "
  "resistor along the upper line followed by one 2 Ω resistor connected across from the upper line to the lower "
  "line; the lower line has no resistance. The equivalent resistance between the two input terminals of the ladder "
  "is:",
  *opt("(1 + √5) Ω ≈ 3.2 Ω", ["2(1 + √3) Ω ≈ 5.5 Ω", "4 Ω", "infinite"], "B"),
  "Self-similarity of an infinite ladder: removing the first section leaves the same ladder",
  "Let the input resistance be x. The first series 2 Ω resistor is followed by the first rung (2 Ω) in parallel with "
  "the rest of the ladder, whose resistance is again x.",
  ["x = 2 + (2x)/(2 + x)", "x(2 + x) = 2(2 + x) + 2x → x² − 2x − 4 = 0",
   "x = 1 + √5 ≈ 3.24 Ω (positive root)"],
  why="2(1 + √3) Ω is the result for a ladder with a series resistor on both lines in every section. 4 Ω keeps only "
      "the first section (2 + 2). An infinite number of resistors does not give infinite resistance, because the "
      "later sections are in parallel with the rungs.",
  seconds=100, rc=True)

V1, R1m, V2, R2m = F(6, 5), 200, F(27, 20), 450
I1m, I2m = V1 / R1m, V2 / R2m
r_m = (V2 - V1) / (I1m - I2m)
eps_m = V1 + I1m * r_m
assert r_m == 50 and eps_m == F(3, 2)
assert (I1m - I2m) / (V2 - V1) == F(1, 50)
q(CE, "Cells, emf and internal resistance", "Advanced", "numerical",
  "A voltmeter of resistance 200 Ω, connected directly across the terminals of a cell, reads 1.20 V. When it is "
  "replaced by a voltmeter of resistance 450 Ω, the reading is 1.35 V. Nothing else is connected to the cell. The "
  "emf and the internal resistance of the cell are:",
  *opt("1.5 V and 50 Ω", ["1.35 V and zero", "1.2 V and 50 Ω", "1.5 V and 0.02 Ω"], "D"),
  "A voltmeter of finite resistance draws current, so it reads the terminal voltage V = ε − Ir",
  "Each voltmeter is the only load, so the current through the cell is the voltmeter reading divided by the "
  "voltmeter's resistance. Two readings give two equations for ε and r.",
  ["I₁ = 1.20/200 = 6.0 mA; I₂ = 1.35/450 = 3.0 mA", "ε = 1.20 + 0.006r = 1.35 + 0.003r",
   "0.003r = 0.15 → r = 50 Ω; ε = 1.20 + 0.30 = 1.5 V"],
  why="1.35 V and zero treats the 450 Ω voltmeter as ideal. 1.2 V and 50 Ω takes the first reading as the emf. "
      "1.5 V and 0.02 Ω inverts the ratio when finding r (ΔI/ΔV instead of ΔV/ΔI).",
  ncert=CEC + "cells, emf, internal resistance", seconds=110, rc=True)

k_J, R_w = 3.0e8, 1.0e-3
I_J = 2 * math.pi * k_J * R_w ** 3 / 3
close(I_J, 0.2 * math.pi)
close(I_J, 0.628, 1e-3)
close(k_J * R_w * math.pi * R_w ** 2, 0.942, 1e-3)
close(k_J * R_w / 2 * math.pi * R_w ** 2, 0.471, 1e-3)
close(2 * math.pi * k_J * R_w ** 3, 1.885, 1e-3)
q(CE, "Drift velocity and Ohm's law", "Advanced", "numerical",
  "The current density in a long straight wire of radius 1.0 mm is directed along the wire, and its magnitude "
  "increases linearly with the distance r from the axis: J = kr, with k = 3.0 × 10⁸ A m⁻³. The current in the wire "
  "is about:",
  *opt("0.63 A", ["0.94 A", "0.47 A", "1.9 A"], "C"),
  "Current is the flux of current density: I = ∫J dA",
  "Since J varies with r, divide the cross-section into thin rings of radius r and width dr (area 2πr dr) and add "
  "their currents.",
  ["dI = J × 2πr dr = 2πk r² dr", "I = 2πk ∫₀ᴿ r² dr = 2πkR³/3",
   "I = 2π × 3.0 × 10⁸ × (1.0 × 10⁻³)³/3 = 0.2π ≈ 0.63 A"],
  why="0.94 A multiplies the surface value kR by the whole area. 0.47 A uses the value of J at r = R/2 as the "
      "average. 1.9 A leaves out the factor 1/3 from the integration.",
  ncert=CEC + "electric current; current density", seconds=100, rc=True)

edges_wb = [(0, 1, 10), (1, 2, 20), (0, 3, 30), (3, 2, 60), (1, 3, 50)]
v_wb = solve_network(4, edges_wb, {0: 9, 2: 0})
assert v_wb[1] == v_wb[3] == 6
assert (9 - v_wb[1]) / 10 == F(3, 10) and v_wb[3] - 0 == 6
assert equivalent_resistance(4, edges_wb, 0, 2) == F(45, 2)
q(CE, "Wheatstone and metre bridge", "Advanced", "multi_statement",
  ms("In a Wheatstone bridge, P = 10 Ω (from A to B) and Q = 20 Ω (from B to C) form one arm, and R = 30 Ω (from A "
     "to D) and S = 60 Ω (from D to C) form the other. An ideal 9 V battery is connected between A (positive) and C, "
     "and a galvanometer between B and D. Which of the following statements are correct?",
     ["The bridge is balanced, and no current flows through the galvanometer.",
      "The current through P is 0.1 A.",
      "The potential difference across S is 6 V.",
      "The equivalent resistance of the network between A and C is 22.5 Ω.",
      "The potential of B is higher than that of D."]),
  *mso({"a": True, "b": False, "c": True, "d": True, "e": False}, "acd", ["ab", "cde", "abd"], "D"),
  "Balanced Wheatstone bridge: P/Q = R/S, no galvanometer current, V_B = V_D",
  "P/Q = 1/2 = R/S, so the bridge is balanced (a true) and B and D are at the same potential (e false). With no "
  "current in the galvanometer, the arms are simply two series pairs across 9 V: P–Q carries 9/30 = 0.3 A (b false) "
  "and R–S carries 9/90 = 0.1 A, so V_S = 0.1 × 60 = 6 V (c true). The equivalent resistance is 30 Ω in parallel "
  "with 90 Ω, i.e. 22.5 Ω (d true).",
  ["P/Q = R/S = 1/2 → balanced; V_B = V_D", "I(P–Q) = 9/30 = 0.3 A; I(R–S) = 9/90 = 0.1 A",
   "V_S = 0.1 × 60 = 6 V", "R_AC = (30 × 90)/120 = 22.5 Ω"],
  why="0.1 A is the current in the R–S arm, not in P, so (b) is false; at balance B and D are at equal potentials, so "
      "(e) is false. Every option except (a), (c) and (d) only includes one of these or leaves out a true statement.",
  ncert=CEC + "Wheatstone bridge", seconds=100)

v_par = solve_network(4, [(2, 1, 2), (3, 1, 1), (1, 0, 4)], {0: 0, 2: 6, 3: 4})
assert v_par[1] == 4 and (v_par[1] - 4) / 1 == 0
assert F(4, F(6 - 4, 2 + 1)) == 6
q(CE, "Cells, emf and internal resistance", "Advanced", "numerical",
  "Two cells, X (emf 6.0 V, internal resistance 2.0 Ω) and Y (emf 4.0 V, internal resistance 1.0 Ω), are connected "
  "in parallel, positive terminal to positive terminal, and the combination is connected across an external "
  "resistor R. The value of R for which no current flows through cell Y is:",
  *opt("4 Ω", ["2 Ω", "1 Ω", "6 Ω"], "A"),
  "A cell carries no current when the p.d. across it equals its emf",
  "If Y carries no current, the common terminal p.d. equals ε_Y = 4.0 V. Then X alone drives the current through "
  "R: (6 − 4)/2 = 1 A, and R = 4 V/1 A.",
  ["No current in Y → V = 4.0 V across R", "Current from X = (6.0 − 4.0)/2.0 = 1.0 A, all of it through R",
   "R = 4.0/1.0 = 4 Ω"],
  why="2 Ω takes the difference of the emfs (2 V) as the p.d. across R. 1 Ω simply equates R to the internal "
      "resistance of Y. 6 Ω uses the current that would circulate between the cells with R removed, "
      "(6 − 4)/(2 + 1) A, as the current in R.",
  ncert=CEC + "cells in series and in parallel", seconds=100, rc=True)


# ================================================================ Magnetism (B5 I7 A5)
MC = NC + "'Moving Charges and Magnetism', "
MM = NC + "'Magnetism and Matter', "
mu0 = 4 * math.pi * 1e-7

# ---- Basic
f_cyc = 1.6e-19 * 0.2 * math.pi / (2 * math.pi * 1.6e-27)
close(f_cyc, 1.0e7)
close(1.6e-19 * 0.2 * math.pi / 1.6e-27, 6.28e7, 1e-3)
close(1.6e-19 * 0.2 / (2 * math.pi * 1.6e-27), 3.18e6, 2e-3)
close(1.6e-19 * 0.2 * math.pi / (4 * math.pi * 1.6e-27), 5.0e6)
q(MAG, "Force on charges and conductors", "Basic", "numerical",
  "A proton (mass 1.6 × 10⁻²⁷ kg, charge 1.6 × 10⁻¹⁹ C) moves in a circle at right angles to a uniform magnetic "
  "field of 0.2π T (about 0.63 T). The number of revolutions it makes per second is:",
  *opt("1.0 × 10⁷", ["6.3 × 10⁷", "3.2 × 10⁶", "5.0 × 10⁶"], "B"),
  "Frequency of revolution in a magnetic field: ν = qB/(2πm), independent of speed",
  "The magnetic force qvB provides the centripetal force mv²/r, so the angular frequency is ω = qB/m and the number "
  "of revolutions per second is ω/2π. The speed of the proton is not needed.",
  ["ν = qB/(2πm)", "ν = (1.6 × 10⁻¹⁹ × 0.2π)/(2π × 1.6 × 10⁻²⁷) = 0.1 × 10⁸ = 1.0 × 10⁷ s⁻¹"],
  why="6.3 × 10⁷ is the angular frequency qB/m (in rad/s), not revolutions per second. 3.2 × 10⁶ drops the π in "
      "the field. 5.0 × 10⁶ divides by 4π instead of 2π.",
  ncert=MC + "motion in a magnetic field", seconds=40, rc=True)

R_ser = 15 / (3 / 1000) - 1000
assert round(R_ser) == 4000 and round(15 / (3 / 1000)) == 5000
q(MAG, "Torque on loop and galvanometer", "Basic", "numerical",
  "A voltmeter of resistance 1000 Ω has a range of 0–3 V. To use it to measure potential differences up to 15 V, one "
  "should connect:",
  *opt("4000 Ω in series with it", ["5000 Ω in series with it", "4000 Ω in parallel with it",
                                     "15 000 Ω in series with it"], "C"),
  "Range of a voltmeter = full-scale current × total resistance",
  "The full-scale current is 3 V/1000 Ω = 3 mA. To read 15 V at the same current, the total resistance must be "
  "15/0.003 = 5000 Ω, so an extra 4000 Ω is added in series.",
  ["I_fs = 3/1000 = 3 mA", "Total resistance for 15 V = 15/0.003 = 5000 Ω", "Series resistance = 5000 − 1000 = 4000 Ω"],
  why="5000 Ω is the total resistance needed, not the extra resistance. A resistance in parallel would lower the "
      "meter's resistance and draw more current, not extend a voltage range. 15 000 Ω multiplies the meter's "
      "resistance by the new range in volts.",
  ncert=MC + "the moving coil galvanometer (conversion into voltmeter)", seconds=35, rc=True)

# B at centre of loop radius a with current i is mu0 i/(2a); zero net field: i2/(2R*2) = I/(2R) -> i2 = 2I
assert F(1, 1) / 1 == F(2, 1) / 2
q(MAG, "Biot-Savart law", "Basic", "numerical",
  "Two circular loops of wire, of radii R and 2R, lie in the same plane and have a common centre O. The inner loop "
  "carries a steady current I. For the magnetic field at O to be zero, the current in the outer loop must be:",
  *opt("2I, circulating in the opposite sense", ["2I, circulating in the same sense",
                                                 "I/2, circulating in the opposite sense",
                                                 "4I, circulating in the opposite sense"], "D"),
  "Field at the centre of a circular loop: B = µ₀I/(2R), perpendicular to the plane",
  "Both fields at O are perpendicular to the common plane. They cancel only if they are equal in magnitude and the "
  "currents circulate in opposite senses.",
  ["µ₀I/(2R) = µ₀I′/(2 × 2R)", "I′ = 2I, in the opposite sense"],
  why="Currents in the same sense give fields in the same direction, which add. I/2 inverts the dependence on the "
      "radius. 4I takes B ∝ 1/R².",
  ncert=MC + "magnetic field on the axis of a circular current loop", seconds=35, rc=True)

# n turns from the same length: radius R/n, field = n * mu0 I/(2R/n) = n^2 * mu0 I/(2R)
assert all(n * n == n ** 2 for n in (2,)) and 2 ** 2 == 4
q(MAG, "Biot-Savart law", "Basic", "numerical",
  "A length of wire bent into a single circular turn carries a steady current, and the magnetic field at its centre "
  "is B. The same wire is unbent and rewound into a flat coil of two circular turns of equal radius, carrying the "
  "same current. The magnetic field at the centre of the coil is now:",
  *opt("4B", ["2B", "B/2", "B"], "A"),
  "B = µ₀NI/(2r) for a flat coil; with a fixed length of wire, r ∝ 1/N",
  "With two turns from the same length, each turn has half the radius. Doubling N and halving r each double the "
  "field.",
  ["2πR = 2 × 2πr → r = R/2", "B′ = µ₀(2)I/(2 × R/2) = 4 × µ₀I/(2R) = 4B"],
  why="2B doubles N but forgets that the radius halves. B/2 halves the radius in the wrong direction. B assumes the "
      "field depends only on the length of wire.",
  ncert=MC + "magnetic field on the axis of a circular current loop", seconds=35, rc=True)

q(MAG, "Magnetic materials", "Basic", "statement_pair",
  sp("Soft iron is a soft ferromagnetic material: its magnetisation disappears when the external magnetic field is "
     "removed.",
     "Alnico, an alloy of iron, aluminium, nickel, cobalt and copper, is a hard ferromagnetic material and is used "
     "to make permanent magnets."),
  SP, sp_key(True, True),
  "Hard and soft ferromagnetic materials",
  "NCERT describes soft ferromagnets, such as soft iron, as materials whose magnetisation disappears on removal of "
  "the external field (Statement I true), and hard ferromagnets, such as Alnico, as materials that retain their "
  "magnetisation and are used for permanent magnets (Statement II true).",
  ["Soft iron: magnetisation lost when field removed → I true", "Alnico: retains magnetisation → permanent magnets → "
   "II true"],
  why="Both statements are NCERT descriptions, so the options that call either of them false are wrong.",
  ncert=MM + "ferromagnetism (hard and soft ferromagnets)", seconds=30)

# ---- Intermediate
G, Ig = 100, F(1, 1000)
S1 = Ig * G / (1 - Ig)
S2 = Ig * G / (F(10, 1000) - Ig)
R1 = 1 / Ig - G
R2 = 10 / Ig - G
close(float(S1), 0.1, 2e-3)
close(float(S2), 11.1, 2e-3)
assert R1 == 900 and R2 == 9900
q(MAG, "Torque on loop and galvanometer", "Intermediate", "match_list",
  ml("A galvanometer of resistance 100 Ω gives full-scale deflection for a current of 1 mA. Match each instrument "
     "to be made from it (List-I) with the resistance needed and its connection (List-II).",
     ["Ammeter of range 0–1 A", "Ammeter of range 0–10 mA", "Voltmeter of range 0–1 V", "Voltmeter of range 0–10 V"],
     ["9900 Ω in series", "about 0.1 Ω in parallel", "900 Ω in series", "about 11.1 Ω in parallel"]),
  *mlo("A-II, B-IV, C-III, D-I",
       ["A-IV, B-II, C-III, D-I", "A-II, B-IV, C-I, D-III", "A-III, B-I, C-II, D-IV"], "D"),
  "Shunt S = I_gG/(I − I_g) in parallel for an ammeter; series R = V/I_g − G for a voltmeter",
  "For an ammeter, the shunt carries the excess current I − I_g at the same p.d. as the galvanometer. For a "
  "voltmeter, the total resistance must be V/I_g.",
  ["0–1 A: S = (0.001 × 100)/0.999 ≈ 0.1 Ω (parallel)", "0–10 mA: S = 0.1/0.009 ≈ 11.1 Ω (parallel)",
   "0–1 V: R = 1/0.001 − 100 = 900 Ω (series)", "0–10 V: R = 10/0.001 − 100 = 9900 Ω (series)"],
  why="A-IV, B-II gives the larger range the larger shunt, which is the wrong way round. C-I, D-III gives the larger "
      "voltage range the smaller series resistance. A-III, B-I, C-II, D-IV puts series resistances on the ammeters "
      "and shunts on the voltmeters.",
  ncert=MC + "the moving coil galvanometer (conversion into ammeter and voltmeter)", seconds=80, rc=True)

m_sol = 500 * 2.0 * 2.0e-4
close(m_sol, 0.2)
B_ax = 1e-7 * 2 * m_sol / 0.10 ** 3
close(B_ax, 4e-5)
close(1e-7 * m_sol / 0.10 ** 3, 2e-5)
close(1e-7 * 2 * m_sol / 0.10 ** 2, 4e-6)
q(MAG, "Magnetic dipole and bar magnet", "Intermediate", "numerical",
  "A short solenoid of 500 turns, each of cross-sectional area 2.0 × 10⁻⁴ m², carries a steady current of 2.0 A. Its "
  "length is very small compared with 10 cm, so it behaves like a short bar magnet. Taking µ₀/4π = 10⁻⁷ T m A⁻¹ and "
  "ignoring all other magnetic fields, the magnitude of the magnetic field on its axis, 10 cm from its centre, is:",
  *opt("4 × 10⁻⁵ T", ["2 × 10⁻⁵ T", "4 × 10⁻⁶ T", "8 × 10⁻⁵ T"], "B"),
  "A current-carrying solenoid is equivalent to a bar magnet of moment m = NIA; axial field of a short dipole "
  "B = (µ₀/4π)(2m/r³)",
  "First find the magnetic moment of the solenoid; then use the far-field formula for a point on the axis of a "
  "magnetic dipole.",
  ["m = NIA = 500 × 2.0 × 2.0 × 10⁻⁴ = 0.20 A m²", "B = 10⁻⁷ × 2 × 0.20/(0.10)³ = 4 × 10⁻⁵ T"],
  why="2 × 10⁻⁵ T is the equatorial-line value (no factor 2). 4 × 10⁻⁶ T uses 1/r² instead of 1/r³. 8 × 10⁻⁵ T "
      "doubles the axial value.",
  ncert=MM + "the bar magnet as an equivalent solenoid", seconds=60, rc=True)

M_ratio = (0.80 / 0.50) * (300 / 240)
close(M_ratio, 2.0)
close((0.80 / 0.50) * (240 / 300), 1.28)
q(MAG, "Magnetic materials", "Intermediate", "numerical",
  "A paramagnetic sample obeys Curie's law and is far from magnetic saturation. In an applied magnetic field of "
  "0.50 T at a temperature of 300 K, its magnetisation is M. The applied field is raised to 0.80 T and the sample "
  "is cooled to 240 K. Its magnetisation becomes:",
  *opt("2.0 M", ["1.28 M", "1.6 M", "1.25 M"], "C"),
  "Curie's law: χ = Cµ₀/T, so M = χH ∝ B₀/T",
  "The magnetisation is proportional to the applied field and, by Curie's law, inversely proportional to the "
  "absolute temperature.",
  ["M ∝ B₀/T", "M′/M = (0.80/0.50) × (300/240) = 1.6 × 1.25 = 2.0"],
  why="1.28 M multiplies by 240/300, as if M increased with temperature. 1.6 M ignores the change of temperature. "
      "1.25 M ignores the change of field.",
  ncert=MM + "paramagnetism (Curie's law)", seconds=50, rc=True)

q(MAG, "Torque on loop and galvanometer", "Intermediate", "assertion_reason",
  ar("A moving-coil galvanometer cannot be used as such (without any modification) to measure the current in a "
     "circuit.",
     "It gives full-scale deflection for a current of the order of microamperes, and since it must be connected in "
     "series, its resistance would change the current being measured."),
  AR, ar_key(True, True, True),
  "Why a galvanometer is converted before being used as an ammeter",
  "NCERT gives exactly these two reasons: the galvanometer is too sensitive (a few µA gives full-scale deflection), "
  "and being connected in series its resistance alters the very current it measures. Hence it is converted into an "
  "ammeter with a small shunt.",
  ["Very sensitive → overloaded by ordinary currents", "Series connection + large resistance → changes circuit "
   "current", "R explains A"],
  why="Both statements are true and R states the reasons why the galvanometer cannot be used directly, so R is the "
      "correct explanation.",
  ncert=MC + "the moving coil galvanometer", seconds=35)

q(MAG, "Magnetic dipole and bar magnet", "Intermediate", "statement_pair",
  sp("At points at equal large distances from a short bar magnet, the magnetic field on its axial line points along "
     "its magnetic moment, whereas the field on its equatorial line points opposite to its magnetic moment.",
     "The magnetic moment of a bar magnet is directed from its north pole to its south pole."),
  SP, sp_key(True, False),
  "Field of a magnetic dipole: B_axial = (µ₀/4π)(2m/r³), B_equatorial = −(µ₀/4π)(m/r³)",
  "On the axis the field is 2m/r³ along m; on the equatorial line it is m/r³ directed opposite to m (Statement I "
  "true). The magnetic moment of a bar magnet points from its south pole to its north pole (Statement II false).",
  ["Axial: along m; equatorial: opposite to m → I true", "m points S → N → II false"],
  why="Statement II reverses the direction of the magnetic moment; Statement I is the standard dipole result.",
  ncert=MM + "the bar magnet (field of a dipole)", seconds=40)

q(MAG, "Magnetic dipole and bar magnet", "Intermediate", "match_list",
  ml("A magnetic dipole of moment m is held in a uniform magnetic field B, with the angle between m and B as given in "
     "List-I. Match each case with the torque τ on the dipole and its potential energy U in List-II.",
     ["0°", "90°", "180°", "60°"],
     ["τ = mB, U = 0", "τ = 0, U = +mB (unstable equilibrium)", "τ = (√3/2)mB, U = −mB/2",
      "τ = 0, U = −mB (stable equilibrium)"]),
  *mlo("A-IV, B-I, C-II, D-III",
       ["A-II, B-I, C-IV, D-III", "A-IV, B-III, C-II, D-I", "A-I, B-IV, C-II, D-III"], "B"),
  "τ = mB sin θ; U = −mB cos θ",
  "The torque vanishes at 0° and 180°, but U is lowest (−mB) at 0°, which is stable, and highest (+mB) at 180°, "
  "which is unstable. At 90°, τ is maximum and U = 0. At 60°, τ = mB sin 60° and U = −mB cos 60°.",
  ["0°: τ = 0, U = −mB → IV", "90°: τ = mB, U = 0 → I", "180°: τ = 0, U = +mB → II",
   "60°: τ = (√3/2)mB, U = −mB/2 → III"],
  why="A-II, C-IV swaps the stable and unstable positions. B-III, D-I swaps the 90° and 60° cases. A-I, B-IV gives "
      "the parallel position the maximum torque.",
  ncert=MM + "the bar magnet (dipole in a uniform field)", seconds=60)

q(MAG, "Magnetic materials", "Intermediate", "multi_statement",
  ms("Which of the following statements about the examples of magnetic materials given in NCERT are correct?",
     ["Oxygen at STP is paramagnetic.",
      "Nitrogen at STP is diamagnetic.",
      "Cobalt is a ferromagnetic substance.",
      "Copper chloride is diamagnetic.",
      "Lead is paramagnetic."]),
  *mso({"a": True, "b": True, "c": True, "d": False, "e": False}, "abc", ["ab", "abcd", "bce"], "D"),
  "Examples of dia-, para- and ferromagnetic substances",
  "NCERT lists oxygen (at STP) and copper chloride among paramagnetic substances, nitrogen (at STP) and lead among "
  "diamagnetic substances, and iron, cobalt and nickel among ferromagnetic ones. So (a), (b) and (c) are true; "
  "copper chloride is paramagnetic (d false) and lead is diamagnetic (e false).",
  ["(a) true", "(b) true", "(c) true", "(d) false: copper chloride is paramagnetic",
   "(e) false: lead is diamagnetic"],
  why="Options containing (d) or (e) include a false statement; (a) and (b) only leaves out the true statement (c).",
  ncert=MM + "magnetic properties of materials (examples)", seconds=50)

# ---- Advanced
th1, th2 = math.pi / 2, 3 * math.pi / 2
I1a, I2a = th2 / (th1 + th2), th1 / (th1 + th2)
close(I1a, 0.75)
assert abs(I1a * th1 - I2a * th2) < 1e-12
close(0.5 * (th2 - th1) / (2 * math.pi) / 2, 1 / 8)
close(0.75 * (th1 / (2 * math.pi)) / 2, 3 / 32)
q(MAG, "Biot-Savart law", "Advanced", "numerical",
  "A uniform circular ring of wire of radius R has centre O. A steady current I enters the ring at point A and "
  "leaves it at point B, where the radii OA and OB are at right angles, so that the ring is divided into a "
  "quarter-circle arc and a three-quarter-circle arc in parallel. The lead wires are straight and lie along the "
  "lines OA and OB extended outwards. The magnitude of the magnetic field at O is:",
  *opt("zero", ["µ₀I/(8R)", "3µ₀I/(32R)", "µ₀I/(2R)"], "C"),
  "Field at the centre of an arc: B = (µ₀i/2R)(θ/2π); current divides inversely as the resistance (length) of the "
  "arcs",
  "The radial leads point at O and contribute nothing. The quarter arc carries 3I/4 and the three-quarter arc I/4 "
  "(currents inversely proportional to arc length). Their fields at O are in opposite directions, and the product "
  "i × θ is the same for both arcs, so they cancel.",
  ["i₁ = 3I/4 over θ₁ = π/2; i₂ = I/4 over θ₂ = 3π/2", "i₁θ₁ = 3πI/8 = i₂θ₂",
   "B₁ and B₂ are opposite and equal → B = 0"],
  why="µ₀I/(8R) assumes the current divides equally between the two arcs. 3µ₀I/(32R) counts only the quarter arc. "
      "µ₀I/(2R) treats the whole current as going round the complete ring.",
  ncert=MC + "magnetic field due to a current element, Biot–Savart law", seconds=110, rc=True)

em = 2 * 225 / ((1.0e-3) ** 2 * 0.05 ** 2)
close(em, 1.8e11)
close(225 / ((1.0e-3) ** 2 * 0.05 ** 2), 9.0e10)
close(2 * 225 / (1.0e-3 * 0.05 ** 2), 1.8e8)
close(2 * 225 / ((1.0e-3) ** 2 * 0.05), 9.0e9)
q(MAG, "Force on charges and conductors", "Advanced", "numerical",
  "Electrons, starting from rest, are accelerated through a potential difference of 225 V and then enter a uniform "
  "magnetic field of 1.0 mT, moving at right angles to it. They move in a circle of radius 5.0 cm. The value of the "
  "specific charge e/m of the electron obtained from these data is:",
  *opt("1.8 × 10¹¹ C/kg", ["9.0 × 10¹⁰ C/kg", "1.8 × 10⁸ C/kg", "9.0 × 10⁹ C/kg"], "D"),
  "eV = ½mv² and r = mv/(eB) combine to give e/m = 2V/(B²r²)",
  "The accelerating p.d. fixes the speed; the radius in the magnetic field fixes the momentum per unit charge. "
  "Eliminating v gives e/m.",
  ["v = √(2eV/m) and r = mv/(eB) → r² = 2mV/(eB²)", "e/m = 2V/(B²r²) = 2 × 225/[(10⁻³)² × (0.05)²]",
   "= 450/(2.5 × 10⁻⁹) = 1.8 × 10¹¹ C/kg"],
  why="9.0 × 10¹⁰ C/kg drops the factor 2 from ½mv². 1.8 × 10⁸ C/kg does not square B. 9.0 × 10⁹ C/kg does not "
      "square r.",
  ncert=MC + "motion in a magnetic field", seconds=100, rc=True)

cs1, cs2 = 40 * 2.0, 60 * 1.0
vs1, vs2 = cs1 / 20, cs2 / 30
assert F(int(cs1), int(cs2)) == F(4, 3) and vs1 / vs2 == 2
assert F(80 * 20, 60 * 30) == F(8, 9)
q(MAG, "Torque on loop and galvanometer", "Advanced", "numerical",
  "Two moving-coil galvanometers G₁ and G₂ have identical radial magnetic fields and identical springs (same "
  "torsional constant). G₁ has a coil of 40 turns, each of area 2.0 cm², and resistance 20 Ω; G₂ has a coil of 60 "
  "turns, each of area 1.0 cm², and resistance 30 Ω. The ratios of their current sensitivities and of their voltage "
  "sensitivities (G₁ : G₂) are, respectively:",
  *opt("4 : 3 and 2 : 1", ["4 : 3 and 8 : 9", "2 : 1 and 4 : 3", "3 : 4 and 1 : 2"], "B"),
  "Current sensitivity φ/I = NAB/k; voltage sensitivity φ/V = NAB/(kR)",
  "With the same B and k, the current sensitivity is proportional to NA, and the voltage sensitivity to NA/R.",
  ["NA: G₁ = 40 × 2.0 = 80, G₂ = 60 × 1.0 = 60 → 4 : 3",
   "NA/R: G₁ = 80/20 = 4, G₂ = 60/30 = 2 → 2 : 1"],
  why="4 : 3 and 8 : 9 multiplies by R instead of dividing for the voltage sensitivity. 2 : 1 and 4 : 3 swaps the two "
      "ratios. 3 : 4 and 1 : 2 inverts both.",
  ncert=MC + "the moving coil galvanometer (sensitivity)", seconds=80, rc=True)

B_in = mu0 * (1000 * 2.0 - 500 * 3.0)
B_bet = mu0 * 500 * 3.0
close(B_in, 6.28e-4, 1e-3)
close(B_bet, 1.885e-3, 1e-3)
close(mu0 * (1000 * 2.0 + 500 * 3.0), 4.40e-3, 2e-3)
close(mu0 * 1000 * 2.0, 2.51e-3, 2e-3)
q(MAG, "Ampere's law", "Advanced", "numerical",
  "Two long, ideal, coaxial solenoids are used. The inner one has 1000 turns per metre and carries 2.0 A; the outer "
  "one, of larger radius, has 500 turns per metre and carries 3.0 A, its current circulating in the opposite sense "
  "to that in the inner solenoid. Taking µ₀ = 4π × 10⁻⁷ T m A⁻¹, the magnitudes of the magnetic field well inside "
  "the inner solenoid and in the region between the two solenoids (away from the ends) are, respectively:",
  *opt("6.3 × 10⁻⁴ T and 1.9 × 10⁻³ T",
       ["4.4 × 10⁻³ T and 1.9 × 10⁻³ T", "6.3 × 10⁻⁴ T and 2.5 × 10⁻³ T", "6.3 × 10⁻⁴ T and zero"], "C"),
  "Field of a long ideal solenoid: µ₀nI inside, zero outside; superposition",
  "Inside the inner solenoid both solenoids contribute, and their fields are opposite. Between the solenoids, the "
  "point is outside the inner solenoid (zero field from it) but inside the outer one.",
  ["Inside inner: B = µ₀(n₁I₁ − n₂I₂) = 4π × 10⁻⁷ × (2000 − 1500) ≈ 6.3 × 10⁻⁴ T",
   "Between: B = µ₀n₂I₂ = 4π × 10⁻⁷ × 1500 ≈ 1.9 × 10⁻³ T"],
  why="4.4 × 10⁻³ T adds the two fields although the currents are in opposite senses. 2.5 × 10⁻³ T uses the inner "
      "solenoid's field in the region outside it. Zero ignores the outer solenoid, whose field fills the whole "
      "region within it.",
  ncert=MC + "the solenoid", seconds=100, rc=True)

q(MAG, "Torque on loop and galvanometer", "Advanced", "statement_pair",
  sp("A plane loop carrying a steady current, placed in a non-uniform magnetic field, can experience a net force.",
     "For a plane current loop in a uniform magnetic field, the torque depends on the shape of the loop, not merely "
     "on its current, its area and its orientation relative to the field."),
  SP, sp_key(True, False),
  "Net force on a current loop is zero only in a uniform field; τ = m × B with m = IA",
  "In a non-uniform field, the forces on different parts of the loop need not cancel, so a net force can act "
  "(Statement I true). In a uniform field the torque is m × B, and m = IA depends only on the current and the area "
  "(and the direction of the normal), not on the shape (Statement II false).",
  ["Non-uniform B: forces on opposite parts unequal → net force possible → I true",
   "Uniform B: τ = IA n̂ × B, shape-independent → II false"],
  why="Statement II is false because the magnetic moment of a plane loop is IA for any shape; Statement I is true, "
      "so the remaining options are wrong.",
  ncert=MC + "torque on current loop, magnetic dipole", seconds=50)


# ================================================================ EMI and AC (B4 I5 A4)
EC = NC + "'Electromagnetic Induction', "
ACC = NC + "'Alternating Current', "

# ---- Basic
emf_avg = 100 * 0.2 * 0.01 / 0.1
close(emf_avg, 2.0)
close(2 * emf_avg, 4.0)
close(0.2 * 0.01 / 0.1, 0.02)
q(EMI, "Faraday's and Lenz's laws", "Basic", "numerical",
  "A flat coil of 100 turns, each of area 0.01 m², is in a uniform magnetic field of 0.2 T with its plane "
  "perpendicular to the field. It is turned through 90°, about a diameter perpendicular to the field, in 0.1 s, so "
  "that its plane becomes parallel to the field. The magnitude of the average emf induced in the coil is:",
  *opt("2 V", ["4 V", "0.02 V", "zero, because the field does not change"], "D"),
  "Faraday's law: average emf = NΔΦ/Δt",
  "The flux through each turn falls from BA (plane perpendicular to B) to zero (plane parallel to B). An emf is "
  "induced because the flux changes, even though B itself is constant.",
  ["ΔΦ per turn = BA − 0 = 0.2 × 0.01 = 2 × 10⁻³ Wb", "ε_avg = NΔΦ/Δt = 100 × 2 × 10⁻³/0.1 = 2 V"],
  why="4 V takes the flux change as 2BA, which is the change for a 180° turn. 0.02 V leaves out the number of turns. "
      "Zero ignores that turning the coil changes the flux linked with it.",
  ncert=EC + "Faraday's law of induction", seconds=40, rc=True)

XC2 = 200 * 50 / 200
assert XC2 == 50 and 200 * 200 / 50 == 800 and 200 / math.sqrt(4) == 100
q(EMI, "AC: rms, reactance and impedance", "Basic", "numerical",
  "The reactance of a capacitor is 200 Ω when it is connected to a 50 Hz AC supply. Its reactance when it is "
  "connected to a 200 Hz AC supply is:",
  *opt("50 Ω", ["800 Ω", "100 Ω", "200 Ω"], "B"),
  "Capacitive reactance X_C = 1/(2πfC) ∝ 1/f",
  "The capacitance is unchanged, so the reactance is inversely proportional to the frequency. Raising the frequency "
  "four times reduces X_C to one quarter.",
  ["X_C ∝ 1/f", "X_C′ = 200 × (50/200) = 50 Ω"],
  why="800 Ω takes X_C ∝ f, which is the behaviour of an inductor. 100 Ω takes X_C ∝ 1/√f. 200 Ω assumes the "
      "reactance does not depend on frequency, which is true only of a resistor.",
  ncert=ACC + "AC voltage applied to a capacitor", seconds=30, rc=True)

q(EMI, "Faraday's and Lenz's laws", "Basic", "direct",
  "A light, closed, horizontal ring of a non-magnetic metal (such as copper) is dropped from rest so that it falls along the vertical axis of a "
  "fixed bar magnet whose axis is vertical, and passes right over and beyond it. Neglect air resistance. The "
  "acceleration of the ring, both while it is above the magnet and approaching it and after it has passed below the "
  "magnet and is moving away from it, is:",
  *opt("less than g in both stages",
       ["less than g while approaching, but greater than g while moving away",
        "equal to g throughout, since no battery is connected to the ring",
        "greater than g while approaching, because the magnet attracts the ring"], "A"),
  "Lenz's law: the induced current opposes the change (the relative motion) that produces it",
  "While the ring approaches, the flux through it increases and the induced current makes the ring repel the "
  "magnet. While it moves away, the flux decreases and the induced current makes the ring attract the magnet. In "
  "both stages the magnetic force on the ring is upward, opposing its motion, so its acceleration is less than g.",
  ["Approaching: flux increasing → repulsion → upward force", "Receding: flux decreasing → attraction → upward force",
   "a < g in both stages"],
  why="While moving away the induced current attracts the ring back towards the magnet (upward), so a > g is "
      "wrong. A battery is not needed: the changing flux itself drives a current. An uncharged, non-magnetic ring "
      "is not attracted by a magnet merely because it approaches it.",
  ncert=EC + "Lenz's law and conservation of energy", seconds=40)

q(EMI, "Self and mutual inductance", "Basic", "statement_pair",
  sp("The mutual inductance of two coils increases when both are wound on a common soft-iron core.",
     "The mutual inductance of two coils depends on their separation and on their relative orientation."),
  SP, sp_key(True, True),
  "Factors on which mutual inductance depends",
  "Mutual inductance depends on the geometry of the two coils, their separation and relative orientation, and on "
  "the permeability of the medium. A soft-iron core (very large relative permeability) increases the flux linked "
  "with the second coil for a given current in the first, so M increases (Statement I true). Moving the coils "
  "apart or turning one relative to the other changes the flux linkage and hence M (Statement II true).",
  ["Soft-iron core: µ_r ≫ 1 → larger flux linkage → larger M → I true",
   "Separation and orientation change the flux linkage → M changes → II true"],
  why="Both statements are true, so the options that call either of them false are wrong.",
  ncert=EC + "inductance (mutual inductance)", seconds=35)

# ---- Intermediate
R_l, XL_l, V_l = 100.0, 100.0, 200.0
I_res = V_l / R_l
Z_noC = math.hypot(R_l, XL_l)
I_noC = V_l / Z_noC
P_noC = I_noC ** 2 * R_l
close(I_res, 2.0)
close(I_noC, math.sqrt(2))
close(P_noC, 200.0)
close(V_l / (R_l + XL_l), 1.0)
close(V_l * I_noC, 282.8, 1e-3)
q(EMI, "LCR resonance and power", "Intermediate", "numerical",
  "A series LCR circuit with R = 100 Ω is connected to a 200 V (rms) AC source and is in resonance; at the source "
  "frequency the inductive and capacitive reactances are each 100 Ω. The capacitor is now short-circuited by a wire, "
  "everything else unchanged. The rms current and the average power drawn from the source become:",
  *opt("about 1.41 A and 200 W", ["2 A and 400 W", "1 A and 100 W", "about 1.41 A and 283 W"], "C"),
  "Z = √(R² + (X_L − X_C)²); average power P = I²R = V I cos φ",
  "At resonance the current was 200/100 = 2 A. With the capacitor shorted, the circuit is R and L only: "
  "Z = √(100² + 100²) = 100√2 Ω.",
  ["Z = 100√2 Ω → I = 200/(100√2) = √2 ≈ 1.41 A", "P = I²R = 2 × 100 = 200 W (cos φ = 1/√2)"],
  why="2 A and 400 W are the resonance values, before the change. 1 A and 100 W adds R and X_L arithmetically "
      "(200 Ω). 283 W multiplies V by I and ignores the power factor 1/√2.",
  ncert=ACC + "LCR series circuit; power in AC circuit", seconds=75, rc=True)

R_v, XL_v, XC_v, V_v = 60, 120, 40, 200
Z_v = math.hypot(R_v, XL_v - XC_v)
I_v = V_v / Z_v
vals = {"R": I_v * R_v, "L": I_v * XL_v, "C": I_v * XC_v, "LC": I_v * abs(XL_v - XC_v)}
close(Z_v, 100)
assert {k: round(v) for k, v in vals.items()} == {"R": 120, "L": 240, "C": 80, "LC": 160}
q(EMI, "AC: rms, reactance and impedance", "Intermediate", "match_list",
  ml("A resistor of 60 Ω, an inductor of reactance 120 Ω and a capacitor of reactance 40 Ω are connected in series "
     "to a 200 V (rms) AC supply. Match each pair of points in List-I with the rms voltage between them in List-II.",
     ["Across the resistor", "Across the inductor", "Across the capacitor",
      "Across the inductor and capacitor taken together"],
     ["160 V", "120 V", "80 V", "240 V"]),
  *mlo("A-II, B-IV, C-III, D-I",
       ["A-I, B-IV, C-III, D-II", "A-II, B-III, C-IV, D-I", "A-II, B-IV, C-I, D-III"], "D"),
  "Series AC circuit: same current; V_L and V_C are in antiphase, so V_LC = I|X_L − X_C|",
  "First find the impedance and the current; each voltage is I times the corresponding reactance or resistance. The "
  "voltages across L and C are opposite in phase, so across both together they subtract.",
  ["Z = √(60² + (120 − 40)²) = 100 Ω → I = 2 A", "V_R = 120 V, V_L = 240 V, V_C = 80 V",
   "V_LC = 2 × (120 − 40) = 160 V"],
  why="A-I, D-II swaps V_R and V_LC. B-III, C-IV swaps the inductor and the capacitor. C-I, D-III gives the "
      "capacitor the voltage of the L–C pair.",
  ncert=ACC + "LCR series circuit (phasor diagram)", seconds=80, rc=True)

omega_w = 120 * 2 * math.pi / 60
emf_w = 0.5 * 0.4 * omega_w * 0.5 ** 2
close(emf_w, 0.2 * math.pi)
close(8 * emf_w, 5.03, 1e-3)
close(0.4 * omega_w * 0.25, 1.257, 1e-3)
close(0.5 * 0.4 * 2 * 0.25, 0.10)
q(EMI, "Faraday's and Lenz's laws", "Intermediate", "numerical",
  "A metal wheel has 8 metal spokes, each 0.50 m long, joining its axle to its rim. It rotates at 120 revolutions "
  "per minute in a uniform magnetic field of 0.40 T directed parallel to its axle. The emf induced between the axle "
  "and the rim is about:",
  *opt("0.63 V", ["5.0 V", "1.26 V", "0.10 V"], "B"),
  "Emf across a rod rotating about one end in a perpendicular field: ε = ½Bωl²; identical spokes are in parallel",
  "Each spoke is a rod rotating about one end, with the axle end and the rim end common to all spokes. The spokes "
  "are therefore in parallel, so the emf between axle and rim is that of one spoke.",
  ["ω = 120 × 2π/60 = 4π rad/s", "ε = ½ × 0.40 × 4π × (0.50)² = 0.2π ≈ 0.63 V",
   "8 spokes in parallel → emf unchanged"],
  why="5.0 V adds the emfs of the 8 spokes as if they were in series. 1.26 V leaves out the factor ½. 0.10 V uses "
      "2 rev/s as if it were the angular speed in rad/s.",
  ncert=EC + "motional electromotive force", seconds=75, rc=True)

q(EMI, "AC: rms, reactance and impedance", "Intermediate", "assertion_reason",
  ar("A moving-coil (DC) ammeter connected in a circuit carrying a 50 Hz sinusoidal alternating current shows "
     "practically zero reading.",
     "The average value of a sinusoidal alternating current over a complete cycle is zero."),
  AR, ar_key(True, True, True),
  "Average and rms values of AC; why AC meters are based on the heating effect",
  "The deflecting torque on the coil of a moving-coil meter is proportional to the instantaneous current. With a "
  "50 Hz current this torque reverses a hundred times a second and averages to zero over each cycle, so the pointer "
  "stays practically at zero. R states the reason.",
  ["Torque ∝ i, which reverses every half cycle", "Average of i over a cycle = 0 → average torque = 0",
   "R explains A"],
  why="Both statements are true and the zero average value of the current over a cycle is exactly why a moving-coil "
      "meter reads zero; AC meters therefore use the heating effect (∝ i²) and read rms values.",
  ncert=ACC + "AC voltage applied to a resistor (rms value)", seconds=45)

q(EMI, "Faraday's and Lenz's laws", "Intermediate", "multi_statement",
  ms("A closed plane conducting loop is in a region of uniform magnetic field B. In which of the following cases is "
     "an emf induced in the loop?",
     ["The loop is moved without rotation, its whole area staying inside the uniform field.",
      "The loop is rotated about an axis that lies in its plane and is perpendicular to B.",
      "The loop, with its plane perpendicular to B, is squeezed so that its area decreases.",
      "The loop, with its plane perpendicular to B, is rotated in its own plane about an axis through its centre "
      "parallel to B.",
      "The magnitude of B is changed with time, the loop being held fixed with its plane perpendicular to B."]),
  *mso({"a": False, "b": True, "c": True, "d": False, "e": True}, "bce", ["bc", "abce", "cde"], "C"),
  "An emf is induced only when the magnetic flux BA cos θ through the loop changes",
  "Flux = BA cos θ. (a) B, A and θ are all unchanged → no emf. (b) θ changes → emf. (c) A changes → emf. (d) the "
  "loop turns in its own plane, so B, A and θ are unchanged → no emf. (e) B changes → emf.",
  ["(a) flux constant → no", "(b) θ changes → yes", "(c) A changes → yes", "(d) flux constant → no",
   "(e) B changes → yes"],
  why="Options containing (a) or (d) include a case of constant flux; (b) and (c) only leaves out case (e).",
  ncert=EC + "magnetic flux; Faraday's law of induction", seconds=60)

# ---- Advanced
R_a, V_a = 50.0, 200.0
P0 = V_a ** 2 / R_a
P_half = (V_a / math.hypot(R_a, R_a)) ** 2 * R_a
close(P0, 800)
close(P_half, 400)
close(P0 / math.sqrt(2), 565.7, 1e-3)
close((V_a / (2 * R_a)) ** 2 * R_a, 200)
close(V_a ** 2 / (2 * R_a), 400)
q(EMI, "LCR resonance and power", "Advanced", "numerical",
  "A series LCR circuit with R = 50 Ω is connected to a 200 V (rms) AC source whose frequency can be varied. The "
  "average power drawn from the source at the resonant frequency, and at a frequency for which X_L − X_C = 50 Ω, "
  "are, respectively:",
  *opt("800 W and 400 W", ["800 W and 566 W", "400 W and 200 W", "800 W and 200 W"], "D"),
  "Average power P = I²_rms R with I_rms = V_rms/Z",
  "At resonance Z = R. When the net reactance equals R, Z = R√2, so the current falls by √2 and the power, which "
  "goes as I², halves.",
  ["Resonance: P = V²/R = 200²/50 = 800 W", "X = R: Z = 50√2 Ω → I = 200/(50√2) = 2√2 A",
   "P = (2√2)² × 50 = 400 W"],
  why="800 W and 566 W divides the power, instead of the current, by √2. 400 W and 200 W treats 200 V as a peak "
      "value. 800 W and 200 W adds R and X arithmetically (Z = 100 Ω).",
  ncert=ACC + "power in AC circuit: the power factor", seconds=90, rc=True)

M_wl = 2e-7 * 0.10 * math.log(2)
close(M_wl, 1.386e-8, 1e-3)
close(2e-7 / 0.10 * 0.01, 2.0e-8)
close(2e-7 / 0.20 * 0.01, 1.0e-8)
close(1e-7 * 0.10 * math.log(2), 6.93e-9, 1e-3)
q(EMI, "Self and mutual inductance", "Advanced", "numerical",
  "A long straight wire lies in the plane of a square loop of side 10 cm. Two sides of the loop are parallel to the "
  "wire, the nearer one at a distance of 10 cm from it. Taking µ₀/2π = 2 × 10⁻⁷ T m A⁻¹, the mutual inductance of "
  "the wire and the loop is about (ln 2 = 0.693):",
  *opt("1.4 × 10⁻⁸ H", ["2.0 × 10⁻⁸ H", "1.0 × 10⁻⁸ H", "6.9 × 10⁻⁹ H"], "B"),
  "M = Φ/I, with the flux of B = µ₀I/(2πx) found by integrating over the loop",
  "The field of the wire varies as 1/x across the loop, so the flux is found by adding strips of width dx and "
  "length a parallel to the wire, from x = 10 cm to x = 20 cm.",
  ["Φ = ∫ (µ₀I/2πx) a dx from 0.10 to 0.20 m = (µ₀Ia/2π) ln 2",
   "M = Φ/I = 2 × 10⁻⁷ × 0.10 × 0.693 ≈ 1.4 × 10⁻⁸ H"],
  why="2.0 × 10⁻⁸ H takes the field at the nearer side as uniform over the loop. 1.0 × 10⁻⁸ H takes the field at "
      "the farther side as uniform. 6.9 × 10⁻⁹ H uses µ₀/4π in place of µ₀/2π.",
  ncert=EC + "inductance (mutual inductance)", seconds=110, rc=True)

e0_g = 50 * 0.5 * 0.02 * 100
close(e0_g, 50)
close(e0_g ** 2 / (2 * 25), 50)
close(e0_g ** 2 / 25, 100)
close(e0_g ** 2 / (4 * 25), 25)
close(e0_g / math.sqrt(2) * e0_g / 25, 70.7, 1e-3)
q(EMI, "AC generator and transformer", "Advanced", "numerical",
  "The coil of an AC generator has 50 turns, each of area 0.020 m², and rotates at an angular speed of 100 rad/s "
  "about an axis perpendicular to a uniform magnetic field of 0.50 T. The coil (of negligible resistance) is "
  "connected across a 25 Ω resistor. The average power dissipated in the resistor is:",
  *opt("50 W", ["100 W", "25 W", "71 W"], "C"),
  "Peak emf ε₀ = NBAω; average power in a resistor P = ε_rms²/R = ε₀²/(2R)",
  "The generator gives a sinusoidal emf of peak value NBAω. The average power uses the rms value, ε₀/√2.",
  ["ε₀ = 50 × 0.50 × 0.020 × 100 = 50 V", "ε_rms = 50/√2 V", "P = ε₀²/(2R) = 2500/50 = 50 W"],
  why="100 W uses the peak emf as if it were the rms value. 25 W divides by 4R. 71 W multiplies the rms emf by the "
      "peak current.",
  ncert=ACC + "AC generator; power in AC circuit", seconds=80, rc=True)

q(EMI, "Self and mutual inductance", "Advanced", "assertion_reason",
  ar("When the switch in a DC circuit containing a coil of large self-inductance is suddenly opened, a spark may jump "
     "across the switch contacts.",
     "The rapid decrease of the current induces a large emf in the coil, which opposes the decrease and tends to "
     "keep the current flowing."),
  AR, ar_key(True, True, True),
  "Self-induced emf ε = −L dI/dt",
  "Opening the switch makes the current fall almost to zero in a very short time, so dI/dt is very large and so is "
  "the self-induced emf L|dI/dt|. This emf acts to maintain the current, and it can be large enough to break down "
  "the air between the separating contacts, producing a spark. R explains A.",
  ["Switch opened → very large |dI/dt|", "ε = L|dI/dt| very large, opposing the fall of current",
   "Large emf across the gap → spark; R explains A"],
  why="Both statements are true and the large self-induced emf from the rapid fall of current is the cause of the "
      "spark, so R is the correct explanation of A.",
  ncert=EC + "inductance (self-inductance)", seconds=50)


# ================================================================ Electromagnetic Waves (B2 I2 A2)
WC = NC + "'Electromagnetic Waves', "

lam_mw = 3e8 / 2.45e9
close(lam_mw, 0.1224, 1e-3)
q(EMW, "EM spectrum and uses", "Basic", "numerical",
  "A microwave oven uses electromagnetic waves of frequency 2.45 GHz. Taking c = 3 × 10⁸ m/s, the wavelength of "
  "these waves in air is about:",
  *opt("12 cm", ["1.2 cm", "1.2 m", "7.4 × 10¹⁷ m"], "C"),
  "c = fλ for electromagnetic waves",
  "The wavelength is the speed of light divided by the frequency; 2.45 GHz = 2.45 × 10⁹ Hz.",
  ["λ = c/f = 3 × 10⁸/(2.45 × 10⁹)", "λ ≈ 0.122 m ≈ 12 cm"],
  why="1.2 cm and 1.2 m are off by a factor of ten in the power of ten. 7.4 × 10¹⁷ m multiplies c by f instead of "
      "dividing.",
  ncert=WC + "electromagnetic spectrum (microwaves)", seconds=30, rc=True)

q(EMW, "EM spectrum and uses", "Basic", "direct",
  "Welders wear special glass goggles, or face masks with glass windows, while welding. According to NCERT, these "
  "mainly protect their eyes from the large amount of:",
  *opt("ultraviolet radiation produced by the welding arc",
       ["X-rays produced by the welding arc", "microwaves produced by the welding arc",
        "radio waves produced by the welding arc"], "B"),
  "Ultraviolet rays: sources and hazards; ordinary glass absorbs UV",
  "Welding arcs emit a large amount of ultraviolet radiation, which can damage the eyes. Glass absorbs much of the "
  "UV, so welders use glass goggles or masks with glass windows.",
  ["Welding arc → strong UV emission", "Glass absorbs UV → protects the eyes"],
  why="Welding arcs are not significant sources of X-rays, microwaves or radio waves, and glass windows would not be "
      "the means of protection against them.",
  ncert=WC + "electromagnetic spectrum (ultraviolet rays)", seconds=25)

q(EMW, "EM spectrum and uses", "Intermediate", "multi_statement",
  ms("Which of the following statements about the electromagnetic spectrum, as given in NCERT, are correct?",
     ["The FM radio band extends from 88 MHz to 108 MHz.",
      "Some snakes can detect ultraviolet waves.",
      "Cellular phones use radio waves in the ultrahigh frequency (UHF) band to transmit voice communication.",
      "Television waves have lower frequencies than the waves of the AM radio band.",
      "Infrared detectors are used in Earth satellites, for example to observe the growth of crops."]),
  *mso({"a": True, "b": False, "c": True, "d": False, "e": True}, "ace", ["ac", "abce", "cde"], "D"),
  "Radio waves, microwaves, infrared and their uses",
  "FM: 88–108 MHz (a true). Snakes detect infrared, not ultraviolet; it is many insects whose 'visible' range "
  "extends into the ultraviolet (b false). Cellular phones use the UHF band (c true). TV waves (54–890 MHz) have "
  "higher frequencies than the AM band (530–1710 kHz) (d false). Infrared detectors are used in Earth "
  "satellites, for military purposes and to observe the growth of crops (e true).",
  ["(a) true", "(b) false: snakes detect infrared", "(c) true", "(d) false: TV frequencies are higher",
   "(e) true"],
  why="Options containing (b) or (d) include a false statement; (a) and (c) only leaves out the true statement (e).",
  ncert=WC + "electromagnetic spectrum", seconds=60)

B_out = 2e-7 * 1.0 / 0.08
close(B_out, 2.5e-6)
close(2e-7 * 1.0 * 0.08 / 0.04 ** 2, 1.0e-5)
close(2e-7 * 1.0 / 0.04, 5.0e-6)
q(EMW, "Displacement current", "Intermediate", "numerical",
  "A parallel-plate capacitor has circular plates of radius 4.0 cm and is being charged by a steady current of "
  "1.0 A. Neglect edge effects, so that the changing electric field is confined to the region between the plates. "
  "Taking µ₀ = 4π × 10⁻⁷ T m A⁻¹, the magnitude of the magnetic field at a point midway between the planes of the "
  "plates, 8.0 cm from their common axis (outside the edge of the plates), is:",
  *opt("2.5 × 10⁻⁶ T", ["1.0 × 10⁻⁵ T", "zero, since no conduction current flows there", "5.0 × 10⁻⁶ T"], "A"),
  "Ampere–Maxwell law: ∮B·dl = µ₀(i_c + i_d); between the plates i_d equals the charging current",
  "A circle of radius 8.0 cm about the axis, in the midplane, encloses the whole region of changing electric field, "
  "so the displacement current through it equals the full charging current, 1.0 A.",
  ["B × 2πr = µ₀ i_d with i_d = 1.0 A", "B = µ₀i/(2πr) = 2 × 10⁻⁷ × 1.0/0.080 = 2.5 × 10⁻⁶ T"],
  why="1.0 × 10⁻⁵ T applies the inside-the-plates result µ₀ir/(2πR²) at a point outside the plates. Zero ignores "
      "the displacement current. 5.0 × 10⁻⁶ T uses the plate radius instead of the distance of the point.",
  ncert=WC + "displacement current", seconds=80, rc=True)

k_w, w_w = 1.5e7, 3.0e15
n_w = 3e8 / (w_w / k_w)
lam0 = 2 * math.pi * 3e8 / w_w
close(n_w, 1.5)
close(lam0, 6.283e-7, 1e-3)
close(2 * math.pi / k_w, 4.19e-7, 1e-3)
close(3e8 / w_w, 1.0e-7)
q(EMW, "EM wave properties", "Advanced", "numerical",
  "The electric field of a plane electromagnetic wave travelling through a transparent, non-magnetic medium is "
  "E = E₀ sin(kx − ωt), with k = 1.5 × 10⁷ m⁻¹ and ω = 3.0 × 10¹⁵ rad s⁻¹. Taking c = 3 × 10⁸ m/s, the refractive "
  "index of the medium and the wavelength of this radiation in vacuum are, respectively:",
  *opt("1.5 and 628 nm", ["1.5 and 419 nm", "0.67 and 628 nm", "1.5 and 100 nm"], "B"),
  "Wave speed v = ω/k; n = c/v; vacuum wavelength λ₀ = 2πc/ω (the frequency does not change)",
  "The speed in the medium is ω/k. The frequency is the same in vacuum and in the medium, so the vacuum wavelength "
  "follows from ω and c.",
  ["v = ω/k = 3.0 × 10¹⁵/1.5 × 10⁷ = 2.0 × 10⁸ m/s → n = 3/2 = 1.5",
   "λ₀ = 2πc/ω = 2π × 3 × 10⁸/(3.0 × 10¹⁵) ≈ 6.28 × 10⁻⁷ m = 628 nm"],
  why="419 nm (= 2π/k) is the wavelength inside the medium, not in vacuum. 0.67 is v/c, the reciprocal of the "
      "refractive index. 100 nm leaves out the factor 2π.",
  ncert=WC + "electromagnetic waves (nature)", seconds=90, rc=True)

q(EMW, "EM wave properties", "Advanced", "assertion_reason",
  ar("For the same energy of light falling normally on a surface, the momentum delivered to a perfectly reflecting "
     "surface is equal to the momentum delivered to a perfectly absorbing surface.",
     "Electromagnetic waves carry momentum; when the total energy U of light is completely absorbed by a surface, the "
     "momentum delivered to the surface is U/c."),
  AR, ar_key(False, True),
  "Momentum carried by electromagnetic waves; momentum transfer on absorption and on reflection",
  "R is the NCERT result for complete absorption. On perfect reflection the light's momentum is reversed, so its "
  "change of momentum, and hence the momentum delivered to the surface, is 2U/c, twice the absorbed value. So A is "
  "false.",
  ["Absorption: Δp of light = U/c → momentum delivered U/c (R true)",
   "Reflection: momentum reversed → Δp = 2U/c → A false"],
  why="A is false because a reflecting surface receives twice the momentum; R is a correct statement from NCERT.",
  ncert=WC + "electromagnetic waves (momentum and radiation pressure)", seconds=50)


# ================================================================ Optics (B6 I9 A6)
RO = NC + "'Ray Optics and Optical Instruments', "
WO = NC + "'Wave Optics', "
rad, deg = math.radians, math.degrees


def mirror_v(u, f):
    """Mirror equation 1/v + 1/u = 1/f (Cartesian signs)."""
    return 1 / (1 / f - 1 / u)


# ---- Basic
i_p, e_p, A_p = 50, 40, 60
dev_p = i_p + e_p - A_p
assert dev_p == 30
# a prism that actually gives i = 50°, e = 40° with A = 60° exists (n ≈ 1.41) and 30° exceeds its minimum deviation
lo_n, hi_n = 1.2, 2.0
for _ in range(80):
    mid = (lo_n + hi_n) / 2
    s = deg(math.asin(math.sin(rad(i_p)) / mid)) + deg(math.asin(math.sin(rad(e_p)) / mid))
    lo_n, hi_n = (lo_n, mid) if s < A_p else (mid, hi_n)
n_p = (lo_n + hi_n) / 2
assert 1.38 < n_p < 1.43
assert 2 * deg(math.asin(n_p * math.sin(rad(A_p / 2)))) - A_p < dev_p
q(OPT, "Prism", "Basic", "numerical",
  "A ray of light passes through a glass prism of refracting angle 60°. The angle of incidence on the first face is "
  "50° and the angle of emergence from the second face is 40°. The angle of deviation of the ray is:",
  *opt("30°", ["90°", "10°", "150°"], "A"),
  "Deviation by a prism: δ = i + e − A",
  "The total deviation is the sum of the deviations at the two faces, (i − r₁) + (e − r₂), and r₁ + r₂ = A.",
  ["δ = (i − r₁) + (e − r₂) = i + e − (r₁ + r₂)", "δ = 50° + 40° − 60° = 30°"],
  why="90° adds i and e but forgets to subtract A. 10° subtracts e from i. 150° adds A instead of subtracting it.",
  ncert=RO + "refraction through a prism", seconds=30, rc=True)

ang_fw = 600e-9 / 0.50e-3
close(ang_fw, 1.2e-3)
close(600e-9 / 0.50, 1.2e-6)
close(600e-9 / (2 * 0.50e-3), 6.0e-4)
q(OPT, "Huygens' principle and interference", "Basic", "numerical",
  "In a Young's double-slit experiment, the slits are 0.50 mm apart and light of wavelength 600 nm is used. The "
  "angular separation between two consecutive bright fringes, as seen from the slits, is:",
  *opt("1.2 × 10⁻³ rad", ["1.2 × 10⁻⁶ rad", "8.3 × 10² rad", "6.0 × 10⁻⁴ rad"], "C"),
  "Angular fringe width θ = λ/d (small angles)",
  "Consecutive bright fringes are at angles differing by λ/d, independent of the screen distance.",
  ["θ = λ/d = 600 × 10⁻⁹/(0.50 × 10⁻³)", "θ = 1.2 × 10⁻³ rad"],
  why="1.2 × 10⁻⁶ rad takes the slit separation as 0.50 m. 8.3 × 10² rad inverts the ratio (d/λ). 6.0 × 10⁻⁴ rad "
      "uses λ/2d, the separation between a bright fringe and the next dark fringe.",
  ncert=WO + "interference of light waves and Young's experiment", seconds=30, rc=True)

q(OPT, "Refraction and lenses", "Basic", "direct",
  "Because of the refraction of sunlight by the Earth's atmosphere, the Sun is seen:",
  *opt("a little before the actual sunrise and until a little after the actual sunset, the time difference at "
       "sunset being about 2 minutes",
       ["only from a little after the actual sunrise until a little before the actual sunset",
        "about 2 hours before the actual sunrise and until about 2 hours after the actual sunset",
        "at exactly the actual times of sunrise and sunset, since refraction does not change the direction of "
        "sunlight"], "D"),
  "Atmospheric refraction: light bends towards the normal as it enters denser layers of air",
  "Light from the Sun just below the horizon is bent towards the Earth on passing through the atmosphere, so the Sun "
  "appears above the horizon before it actually rises and remains visible after it actually sets. NCERT gives the "
  "time difference between actual and apparent sunset as about 2 minutes.",
  ["Atmosphere denser near the ground → rays bend towards the Earth",
   "Sun below the horizon still seen → early sunrise, late sunset (about 2 min)"],
  why="Refraction makes the visible day longer, not shorter. The effect is about 2 minutes, not 2 hours. Refraction "
      "does change the direction of the light passing through layers of different density.",
  ncert=RO + "refraction", seconds=25)

v_cm = mirror_v(-9.0, 1.0)
m_cm = -v_cm / -9.0
close(v_cm, 0.9)
close(m_cm * 1.5, 0.15)
v_wrong = 1 / (1 / 1.0 - 1 / 9.0)
close(v_wrong / 9.0 * 1.5, 0.1875)
q(OPT, "Mirrors", "Basic", "numerical",
  "A convex mirror of radius of curvature 2.0 m is used as a rear-view mirror. A car 1.5 m high is 9.0 m behind the "
  "mirror, on its principal axis. The height of the image of the car and its orientation are:",
  *opt("0.15 m, erect", ["0.15 m, inverted", "about 0.19 m, erect", "1.5 m, erect"], "B"),
  "Mirror equation 1/v + 1/u = 1/f and m = −v/u, with f = +R/2 for a convex mirror",
  "With the Cartesian sign convention, u = −9.0 m and f = +1.0 m. The image is virtual (behind the mirror), erect "
  "and diminished.",
  ["1/v = 1/f − 1/u = 1/1.0 + 1/9.0 = 10/9 → v = +0.9 m", "m = −v/u = −0.9/(−9.0) = +0.1",
   "Image height = 0.1 × 1.5 = 0.15 m, erect"],
  why="A convex mirror's image of a real object is always erect, so 'inverted' is wrong. About 0.19 m comes from "
      "a sign error, taking u = +9.0 m, which gives v = 1.125 m. 1.5 m treats the mirror as plane.",
  ncert=RO + "reflection of light by spherical mirrors (mirror equation)", seconds=45, rc=True)

q(OPT, "Refraction and lenses", "Basic", "direct",
  "A thin equiconvex lens of focal length f is cut into two identical halves by a plane that contains its principal "
  "axis. The focal length of each half, for light passing through it, is:",
  *opt("f, the same as that of the original lens", ["2f", "f/2", "infinite"], "C"),
  "Lens maker's formula: 1/f = (n − 1)(1/R₁ − 1/R₂)",
  "Cutting along the principal axis does not change the material or the curvature of either surface; each half "
  "still has the radii R₁ and R₂, so its focal length is unchanged. Only the aperture (and so the amount of light "
  "collected) is halved.",
  ["Each half keeps both curved surfaces with the same radii", "1/f unchanged → focal length f"],
  why="2f is the result for a cut perpendicular to the axis (each half then has one flat surface). f/2 would need "
      "more curvature, not less. A half lens still has curved surfaces, so it still converges light.",
  ncert=RO + "refraction by a lens (lens maker's formula)", seconds=30)

imgs = {u: mirror_v(-u, -10.0) for u in (15, 20, 30, 5)}
close(imgs[15], -30)
close(imgs[20], -20)
close(imgs[30], -15)
close(imgs[5], 10)
q(OPT, "Mirrors", "Basic", "match_list",
  ml("A small object is placed on the principal axis of a concave mirror of focal length 10 cm, at the distance from "
     "the mirror given in List-I. Match each case with the position of the image in List-II.",
     ["15 cm", "20 cm", "30 cm", "5 cm"],
     ["10 cm behind the mirror (virtual)", "30 cm in front of the mirror (real)", "15 cm in front of the mirror (real)",
      "20 cm in front of the mirror (real)"]),
  *mlo("A-II, B-IV, C-III, D-I",
       ["A-III, B-IV, C-II, D-I", "A-II, B-I, C-III, D-IV", "A-II, B-IV, C-I, D-III"], "D"),
  "Mirror equation 1/v + 1/u = 1/f with f = −10 cm",
  "Use u negative for real objects. An object between F and C gives an image beyond C; at C, the image is at C; "
  "beyond C, the image lies between F and C; inside F, the image is virtual, behind the mirror.",
  ["u = −15: 1/v = −1/10 + 1/15 → v = −30 cm", "u = −20: v = −20 cm", "u = −30: v = −15 cm",
   "u = −5: 1/v = −1/10 + 1/5 → v = +10 cm (virtual)"],
  why="A-III, C-II swaps the object and image distances of a conjugate pair. B-I, D-IV gives the object at C a "
      "virtual image. C-I, D-III gives the object inside F a real image.",
  ncert=RO + "reflection of light by spherical mirrors (mirror equation)", seconds=60, rc=True)

# ---- Intermediate
F_m = 10.0
x1, x2 = 1.5 * F_m, 2 * F_m
close(-mirror_v(-x1, -F_m) / -x1, -2.0)
close(-mirror_v(-x2, -F_m) / -x2, -1.0)
close(x2 - x1, 5.0)
q(OPT, "Mirrors", "Intermediate", "numerical",
  "A concave mirror forms a real image twice the size of an object placed on its principal axis. When the object is "
  "moved 5 cm farther away from the mirror, the real image becomes the same size as the object. The focal length of "
  "the mirror is:",
  *opt("10 cm", ["5 cm", "15 cm", "20 cm"], "B"),
  "Concave mirror, real image: |m| = F/(x − F), with x and F the magnitudes of the object distance and focal length",
  "For a real image, |m| = F/(x − F), where F is the magnitude of the focal length. Write this for both positions "
  "and use the 5 cm shift.",
  ["|m| = 2 → x₁ − F = F/2 → x₁ = 1.5F", "|m| = 1 → x₂ = 2F", "x₂ − x₁ = 0.5F = 5 cm → F = 10 cm"],
  why="5 cm equates the shift to the focal length. 15 cm is the first object distance (1.5F). 20 cm is the second "
      "object distance, the centre of curvature (2F).",
  ncert=RO + "reflection of light by spherical mirrors (magnification)", seconds=75, rc=True)

v_ss = 1.5 / ((1.5 - 1) / -10 + 1 / -20)
close(v_ss, -15)
assert abs((1.5 - 1) / 10 + 1 / -20) < 1e-12
close(1 / ((1.5 - 1) / -10 + 1 / -20), -10)
q(OPT, "Refraction and lenses", "Intermediate", "numerical",
  "A point object in air is 20 cm in front of a concave spherical surface of a large block of glass (refractive "
  "index 1.5); the radius of curvature of the surface is 10 cm and the object lies on its axis. The image formed by "
  "refraction at this surface is:",
  *opt("15 cm from the surface, on the same side as the object (virtual)",
       ["15 cm inside the glass (real)", "at infinity", "10 cm from the surface, on the same side as the object "
                                                       "(virtual)"], "A"),
  "Refraction at a spherical surface: n₂/v − n₁/u = (n₂ − n₁)/R",
  "With light travelling from air into glass, u = −20 cm. The surface is concave towards the object, so its centre "
  "of curvature is on the object side: R = −10 cm.",
  ["1.5/v − 1/(−20) = (1.5 − 1)/(−10)", "1.5/v = −0.05 − 0.05 = −0.10 → v = −15 cm",
   "Negative v: image 15 cm from the surface on the object side, virtual"],
  why="15 cm inside the glass reverses the sign of v. 'At infinity' results from taking R = +10 cm. 10 cm drops the "
      "factor n₂ = 1.5 from n₂/v.",
  ncert=RO + "refraction at spherical surfaces", seconds=70, rc=True)

combos = {"A": (2, 3), "B": (5, -3), "C": (4, -6), "D": (2.5, 1.5)}
fl = {k: 100 / (a + b) for k, (a, b) in combos.items()}
assert fl == {"A": 20, "B": 50, "C": -50, "D": 25}
q(OPT, "Refraction and lenses", "Intermediate", "match_list",
  ml("Two thin lenses with the powers given in List-I are placed in contact, coaxially. Match each combination with "
     "the focal length of the combination in List-II.",
     ["+2 D and +3 D", "+5 D and −3 D", "+4 D and −6 D", "+2.5 D and +1.5 D"],
     ["−50 cm", "+20 cm", "+25 cm", "+50 cm"]),
  *mlo("A-II, B-IV, C-I, D-III",
       ["A-II, B-I, C-IV, D-III", "A-III, B-IV, C-I, D-II", "A-II, B-IV, C-III, D-I"], "C"),
  "Thin lenses in contact: P = P₁ + P₂; f (in m) = 1/P",
  "Add the powers with their signs, then f = 100/P cm.",
  ["A: P = +5 D → f = +20 cm", "B: P = +2 D → f = +50 cm", "C: P = −2 D → f = −50 cm", "D: P = +4 D → f = +25 cm"],
  why="B-I, C-IV swaps the signs of the converging and diverging combinations. A-III, D-II swaps two converging "
      "combinations. C-III, D-I gives the diverging combination a positive focal length.",
  ncert=RO + "power of a lens; combination of thin lenses in contact", seconds=60, rc=True)

dev_w = (1.5 / (4 / 3) - 1) * 6
close(dev_w, 0.75)
close((1.5 - 1) * 6, 3.0)
close((1.5 - 4 / 3) * 6, 1.0)
close((4 / 3 - 1) * 6, 2.0)
q(OPT, "Prism", "Intermediate", "numerical",
  "A thin glass prism of refracting angle 6° is made of glass of refractive index 1.5. When the prism is completely "
  "immersed in water of refractive index 4/3, the deviation it produces in a ray passing through it at near-normal "
  "incidence is:",
  *opt("0.75°", ["3°", "1°", "2°"], "D"),
  "Thin prism: δ = (n − 1)A, with n the refractive index of the prism relative to the surrounding medium",
  "In water, the relevant refractive index is that of glass relative to water: 1.5/(4/3) = 9/8.",
  ["n_rel = 1.5 × 3/4 = 1.125", "δ = (1.125 − 1) × 6° = 0.75°"],
  why="3° is the deviation in air. 1° subtracts the two refractive indices instead of dividing them. 2° uses the "
      "refractive index of water in place of that of the glass.",
  ncert=RO + "refraction through a prism", seconds=50, rc=True)

iB = deg(math.atan(1.5 / (4 / 3)))
close(iB, 48.37, 1e-3)
close(deg(math.atan(1.5)), 56.31, 1e-3)
close(deg(math.atan(4 / 3)), 53.13, 1e-3)
close(90 - iB, 41.63, 1e-3)
q(OPT, "Polarisation", "Intermediate", "numerical",
  "A flat glass plate (refractive index 1.5) is immersed in water (refractive index 4/3). Unpolarised light "
  "travelling in the water falls on the plate. The angle of incidence for which the light reflected from the plate "
  "is completely plane polarised is about:",
  *opt("48.4°", ["56.3°", "53.1°", "41.6°"], "A"),
  "Brewster's law: tan i_B = n₂/n₁ (refractive index of the second medium relative to the first)",
  "The light goes from water into glass, so the relative refractive index is n_glass/n_water.",
  ["tan i_B = 1.5/(4/3) = 9/8 = 1.125", "i_B = tan⁻¹(1.125) ≈ 48.4°"],
  why="56.3° is Brewster's angle for glass in air (tan⁻¹ 1.5). 53.1° is that for water in air (tan⁻¹ 4/3). 41.6° is "
      "the angle of refraction at the Brewster angle (90° − i_B).",
  ncert=WO + "polarisation (Brewster's law)", seconds=50, rc=True)

C_gw = deg(math.asin((4 / 3) / 1.5))
r_gw = deg(math.asin(1.5 / (4 / 3) * math.sin(rad(60))))
close(C_gw, 62.73, 1e-3)
close(r_gw, 76.97, 1e-3)
close(deg(math.asin(math.sin(rad(60)) / 1.125)), 50.34, 1e-3)
q(OPT, "Total internal reflection", "Intermediate", "numerical",
  "A ray of light travelling in glass (refractive index 1.5) strikes a plane glass–water boundary (refractive index "
  "of water 4/3) at an angle of incidence of 60°. Which statement correctly describes what happens?",
  *opt("The ray is refracted into the water, making an angle of about 77° with the normal",
       ["The ray is totally internally reflected", "The ray is refracted into the water, making an angle of about "
                                                   "50° with the normal",
        "The ray just grazes along the boundary (angle of refraction 90°)"], "B"),
  "Total internal reflection needs i > C, where sin C = n₂/n₁; otherwise Snell's law gives the refracted ray",
  "For glass to water, sin C = (4/3)/1.5 = 8/9, so C ≈ 62.7°. The angle of incidence (60°) is smaller than C, so "
  "the ray is refracted, bending away from the normal.",
  ["sin C = 8/9 → C ≈ 62.7° > 60° → no TIR", "1.5 sin 60° = (4/3) sin r → sin r = 1.125 × 0.866 ≈ 0.974",
   "r ≈ 77°"],
  why="Total internal reflection would need an angle of incidence above 62.7°; 60° would be enough only at a "
      "glass–air boundary (C ≈ 41.8°). About 50° applies Snell's law the wrong way round (bending towards the normal). "
      "Grazing emergence occurs only at exactly the critical angle.",
  ncert=RO + "total internal reflection", seconds=70, rc=True)

q(OPT, "Mirrors", "Intermediate", "assertion_reason",
  ar("A concave mirror is used as a shaving mirror.",
     "The focal length of a spherical mirror of small aperture is half its radius of curvature."),
  AR, ar_key(True, True, False),
  "Uses of concave mirrors; f = R/2",
  "A concave mirror is used for shaving because, with the face held between the pole and the focus, it forms an "
  "erect, magnified, virtual image. R is a true relation for spherical mirrors, but it does not say why the mirror "
  "gives an enlarged erect image; it holds equally for convex mirrors, which are useless for shaving.",
  ["A: true (erect magnified image when the face is within F)", "R: true (f = R/2)",
   "R does not explain A"],
  why="A and R are both true, but R is a general property of all spherical mirrors and does not account for the "
      "magnified erect image that makes a concave mirror suitable for shaving.",
  ncert=RO + "reflection of light by spherical mirrors", seconds=40)

q(OPT, "Optical instruments", "Intermediate", "multi_statement",
  ms("Which of the following statements about reflecting telescopes, as described in NCERT, are correct?",
     ["A mirror objective has no chromatic aberration.",
      "If the reflecting surface of the objective is parabolic, spherical aberration is also removed.",
      "A mirror objective weighs much less than a lens of equivalent optical quality and can be supported over its "
      "entire back surface.",
      "The objective of a reflecting telescope is a convex mirror.",
      "Very large lens objectives are easier to make and to support than mirror objectives of the same size."]),
  *mso({"a": True, "b": True, "c": True, "d": False, "e": False}, "abc", ["ab", "abcd", "bce"], "D"),
  "Advantages of reflecting telescopes",
  "NCERT lists three advantages of mirror objectives: no chromatic aberration (a), no spherical aberration with a "
  "parabolic surface (b), and easier mechanical support since a mirror is lighter and can be supported over its "
  "whole back (c). The objective is a concave mirror (d false), and large lenses are heavy, hard to make and can be "
  "supported only at the rim (e false).",
  ["(a) true", "(b) true", "(c) true", "(d) false: concave objective", "(e) false"],
  why="Options with (d) or (e) contain a false statement; (a) and (b) only leaves out the true statement (c).",
  ncert=RO + "optical instruments (telescope)", seconds=50)

q(OPT, "Diffraction", "Intermediate", "statement_pair",
  sp("In the diffraction pattern of a single slit illuminated normally, the central maximum lies at θ = 0, the "
     "direction in which the waves from all parts of the slit arrive in phase.",
     "Increasing the distance of the screen from the slit increases the angular width of the central maximum."),
  SP, sp_key(True, False),
  "Single-slit diffraction: central maximum at θ = 0; angular width 2λ/a",
  "At θ = 0 all points of the slit are equidistant (in the far field) from the screen point, so their contributions "
  "are in phase and the intensity is maximum (Statement I true). The angular width 2λ/a depends only on λ and the "
  "slit width; moving the screen changes the linear width (2λD/a) but not the angular width (Statement II false).",
  ["θ = 0: all wavelets in phase → central maximum → I true",
   "Angular width = 2λ/a, independent of D → II false"],
  why="Statement II confuses the angular width with the linear width on the screen; Statement I is correct, so "
      "the remaining options are wrong.",
  ncert=WO + "diffraction (the single slit)", seconds=45)

# ---- Advanced
fo, fe, D_ = 100.0, 6.25, 25.0
ue = fe * D_ / (fe + D_)
close(ue, 5.0)
close(fo + ue, 105.0)
close(fo / fe * (1 + fe / D_), 20.0)
q(OPT, "Optical instruments", "Advanced", "numerical",
  "An astronomical telescope has an objective of focal length 100 cm and an eyepiece of focal length 6.25 cm. It is "
  "focused on a distant object so that the final image is formed at the least distance of distinct vision, 25 cm "
  "from the eyepiece. The distance between the objective and the eyepiece is:",
  *opt("105 cm", ["106.25 cm", "125 cm", "95 cm"], "A"),
  "The objective forms the image of a distant object at its focus; the eyepiece then acts as a magnifier with the "
  "final image at D",
  "The intermediate image is at the focus of the objective (100 cm from it). For the eyepiece, this image is the "
  "object, placed so that the final virtual image is 25 cm away.",
  ["Eyepiece: 1/v − 1/u = 1/f with v = −25 cm, f = +6.25 cm → 1/u = −1/25 − 1/6.25 = −5/25 → u = −5 cm",
   "Separation = f_o + |u_e| = 100 + 5 = 105 cm"],
  why="106.25 cm is the separation in normal adjustment (final image at infinity). 125 cm adds D to f_o. 95 cm "
      "subtracts the eyepiece object distance instead of adding it.",
  ncert=RO + "optical instruments (refracting telescope)", seconds=90, rc=True)

yb = [n * 0.6 for n in range(1, 6)]
yd = [(m - 0.5) * 0.4 for m in range(1, 9)]
coinc = min(a for a in yb if any(abs(a - b) < 1e-9 for b in yd))
close(coinc, 0.6)
close(min(a for a in yb if any(abs(a - n * 0.4) < 1e-9 for n in range(1, 10))), 1.2)
q(OPT, "Huygens' principle and interference", "Advanced", "numerical",
  "In a Young's double-slit experiment, the slits are 1.0 mm apart and the screen is 1.0 m away. The slits are "
  "illuminated by light containing two wavelengths, 600 nm and 400 nm. The least distance from the central maximum "
  "at which a bright fringe of the 600 nm light falls exactly on a dark fringe of the 400 nm light is:",
  *opt("0.6 mm", ["1.2 mm", "0.2 mm", "0.3 mm"], "D"),
  "Bright fringes at y = nλD/d; dark fringes at y = (m − ½)λD/d",
  "The bright fringes of 600 nm are at 0.6, 1.2, 1.8, ... mm; the dark fringes of 400 nm are at 0.2, 0.6, 1.0, "
  "1.4, ... mm. The first common position is the answer.",
  ["600 nm bright: y = n × 0.6 mm", "400 nm dark: y = (m − ½) × 0.4 mm = 0.2, 0.6, 1.0, ... mm",
   "n × 600 = (m − ½) × 400 → n = 1, m = 2 → y = 0.6 mm"],
  why="1.2 mm is where bright fringes of the two wavelengths first coincide. 0.2 mm is the first dark fringe of "
      "400 nm, where 600 nm is not bright. 0.3 mm is the first dark fringe of 600 nm.",
  ncert=WO + "interference of light waves and Young's experiment", seconds=100, rc=True)

v_l = 1 / (1 / 20 - 1 / 30)
close(v_l, 60)
shift = 1.5 * (1 - 1 / 1.5)
close(shift, 0.5)
close(1.5 / 1.5, 1.0)
q(OPT, "Refraction and lenses", "Advanced", "numerical",
  "A thin convex lens of focal length 20 cm forms a sharp image of an object, placed 30 cm in front of it, on a "
  "screen. A parallel-sided glass slab of thickness 1.5 cm and refractive index 1.5 is then placed between the lens "
  "and the screen, with its faces perpendicular to the principal axis. To obtain a sharp image again, the screen "
  "must be moved:",
  *opt("0.5 cm away from the lens", ["0.5 cm towards the lens", "1.0 cm away from the lens",
                                     "1.5 cm away from the lens"], "B"),
  "Normal shift produced by a slab: s = t(1 − 1/n), in the direction of the light",
  "The lens alone forms the image 60 cm behind it. The converging rays pass through the slab, which shifts the "
  "point where they meet farther along the direction of the light by t(1 − 1/n).",
  ["Lens: 1/v = 1/20 − 1/30 → v = 60 cm", "Shift = 1.5 × (1 − 1/1.5) = 0.5 cm, away from the lens",
   "Screen moved 0.5 cm away (to 60.5 cm)"],
  why="'Towards the lens' reverses the direction of the shift: the slab delays the convergence of the rays. 1.0 cm "
      "uses t/n instead of t(1 − 1/n). 1.5 cm takes the shift as the full thickness of the slab.",
  ncert=RO + "refraction (apparent shift)", seconds=90, rc=True)

na = math.sqrt(1.30 ** 2 - 1.20 ** 2)
close(na, 0.5)
close(deg(math.asin(na)), 30.0)
close(deg(math.asin(1.20 / 1.30)), 67.38, 1e-3)
close(90 - deg(math.asin(1.20 / 1.30)), 22.62, 1e-3)
q(OPT, "Total internal reflection", "Advanced", "numerical",
  "An optical fibre has a core of refractive index 1.30 and a cladding of refractive index 1.20, and it is used in "
  "air. Light enters the flat end face of the fibre, which is perpendicular to its axis. The largest angle, measured "
  "from the axis, at which a ray can enter the end face and still be guided along the core by total internal "
  "reflection is:",
  *opt("30°", ["67.4°", "22.6°", "90°, so every ray entering the end face is guided"], "C"),
  "TIR at the core–cladding boundary (sin C = n₂/n₁) combined with Snell's law at the end face",
  "If the ray inside the core makes angle r with the axis, it meets the core–cladding boundary at 90° − r. TIR needs "
  "90° − r ≥ C, i.e. sin r ≤ cos C. At the end face, sin θ = n₁ sin r.",
  ["cos C = √(1 − (1.20/1.30)²) = 0.50/1.30", "sin θ_max = n₁ cos C = √(n₁² − n₂²) = √(1.69 − 1.44) = 0.50",
   "θ_max = 30°"],
  why="67.4° is the critical angle at the core–cladding boundary, not the entry angle. 22.6° is the largest angle of "
      "the ray with the axis inside the core (90° − C), before refraction at the end face. Not every ray is guided, "
      "because √(n₁² − n₂²) is less than 1.",
  ncert=RO + "total internal reflection (optical fibres)", seconds=110, rc=True)

a1, a2 = 1.0, 0.5
assert ((a1 + a2) / (a1 - a2)) ** 2 == 9 and (a1 + a2) ** 2 < 4 * a1 ** 2
q(OPT, "Huygens' principle and interference", "Advanced", "multi_statement",
  ms("In a Young's double-slit experiment with monochromatic light, the two slits initially give waves of equal "
     "intensity at the screen. A neutral filter is now placed over one slit so that the intensity of the light from "
     "it at the screen falls to one-quarter of that from the other slit, without any change of phase. Which of the "
     "following statements are correct?",
     ["The fringe width is unchanged.",
      "The dark fringes are no longer completely dark.",
      "The ratio of the maximum to the minimum intensity becomes 9 : 1.",
      "The central bright fringe shifts towards the covered slit.",
      "The intensity at the bright fringes becomes greater than before."]),
  *mso({"a": True, "b": True, "c": True, "d": False, "e": False}, "abc", ["ab", "abce", "acd"], "B"),
  "I = I₁ + I₂ + 2√(I₁I₂) cos φ; fringe width β = λD/d",
  "The fringe width depends only on λ, D and d (a true). With amplitudes in the ratio 2 : 1 the minima have "
  "intensity (2 − 1)² ≠ 0 (b true) and I_max/I_min = (2 + 1)²/(2 − 1)² = 9 (c true). Since the filter introduces no "
  "phase change, the path-difference condition for the central fringe is unchanged (d false). Before, I_max = 4I₀; "
  "now I_max = (√I₀ + √(I₀/4))² = 2.25I₀, which is smaller (e false).",
  ["(a) β = λD/d unchanged → true", "(b) I_min = I₀(1 − ½)² = 0.25I₀ ≠ 0 → true", "(c) (1.5/0.5)² = 9 → true",
   "(d) no extra phase → no shift → false", "(e) 2.25I₀ < 4I₀ → false"],
  why="Options containing (d) or (e) include a false statement; (a) and (b) only leaves out the true statement (c).",
  ncert=WO + "interference of light waves and Young's experiment", seconds=100)

q(OPT, "Optical instruments", "Advanced", "assertion_reason",
  ar("A simple microscope gives a larger angular magnification (1 + D/f) when the final image is at the near point "
     "than when the final image is at infinity (D/f).",
     "When the final image is at the near point, the object is placed nearer to the lens than its focal length, so it "
     "subtends a larger angle at the eye held close to the lens."),
  AR, ar_key(True, True, True),
  "Angular magnification of a simple microscope m = D/|u|",
  "With the eye close to the lens, the angle subtended by the image equals the angle subtended by the object at the "
  "lens, h/|u|. The magnification is (h/|u|)/(h/D) = D/|u|. For the image at infinity |u| = f, giving D/f; for the "
  "image at the near point |u| = fD/(f + D) < f, giving 1 + D/f. R gives exactly this reason.",
  ["m = D/|u|", "Image at ∞: |u| = f → m = D/f", "Image at D: |u| = fD/(f + D) < f → m = 1 + D/f (larger)",
   "R explains A"],
  why="Both statements are true and the smaller object distance (larger angle subtended) is precisely why the "
      "near-point setting gives the larger magnification.",
  ncert=RO + "optical instruments (simple microscope)", seconds=70)


# ================================================================ Dual Nature (B3 I4 A3)
DC = NC + "'Dual Nature of Radiation and Matter', "

# ---- Basic
q(DUAL, "de Broglie wavelength", "Basic", "direct",
  "An electron, a proton, a neutron and an alpha particle all move with the same speed (much less than the speed of "
  "light). The particle with the longest de Broglie wavelength is the:",
  *opt("electron", ["proton", "neutron", "alpha particle"], "C"),
  "de Broglie relation λ = h/p = h/(mv)",
  "At equal speeds, the de Broglie wavelength is inversely proportional to the mass. The electron is by far the "
  "lightest of the four particles.",
  ["λ = h/(mv) → λ ∝ 1/m at equal v", "Smallest mass: electron → longest λ"],
  why="The proton and the neutron are about 1840 times heavier than the electron, and the alpha particle about four "
      "times heavier still, so their wavelengths are much shorter. Charge does not enter λ = h/p.",
  ncert=DC + "wave nature of matter", seconds=25)

W_m = {"Cs": 2.14, "Na": 2.75, "Ca": 3.20, "Mo": 4.17}
K_m = {k: round(4.0 - w, 2) for k, w in W_m.items()}
assert K_m == {"Cs": 1.86, "Na": 1.25, "Ca": 0.80, "Mo": -0.17}
q(DUAL, "Einstein's equation", "Basic", "match_list",
  ml("Light whose photons each have energy 4.0 eV falls on clean surfaces of the metals in List-I, whose work "
     "functions are given in brackets. Match each metal with the maximum kinetic energy of the photoelectrons in "
     "List-II.",
     ["Caesium (2.14 eV)", "Sodium (2.75 eV)", "Calcium (3.20 eV)", "Molybdenum (4.17 eV)"],
     ["No photoelectrons are emitted", "1.86 eV", "0.80 eV", "1.25 eV"]),
  *mlo("A-II, B-IV, C-III, D-I",
       ["A-II, B-III, C-IV, D-I", "A-I, B-IV, C-III, D-II", "A-II, B-IV, C-I, D-III"], "A"),
  "Einstein's photoelectric equation K_max = hν − φ₀; no emission if hν < φ₀",
  "Subtract each work function from the photon energy. Where the work function exceeds the photon energy, no "
  "electron can be emitted, however intense the light.",
  ["Cs: 4.0 − 2.14 = 1.86 eV", "Na: 4.0 − 2.75 = 1.25 eV", "Ca: 4.0 − 3.20 = 0.80 eV",
   "Mo: 4.17 > 4.0 → no emission"],
  why="A-II, B-III, C-IV swaps the sodium and calcium values. A-I, D-II gives caesium no emission and molybdenum "
      "the largest energy, reversing the role of the work function. C-I, D-III makes calcium emit nothing and "
      "molybdenum emit, which is the wrong way round.",
  ncert=DC + "Einstein's photoelectric equation (work functions)", seconds=50, rc=True)

lam_ph = 1240 / (2.3 + 0.8)
close(lam_ph, 400)
close(1240 / 2.3, 539, 2e-3)
close(1240 / 0.8, 1550)
close(1240 / (2.3 - 0.8), 827, 2e-3)
q(DUAL, "Einstein's equation", "Basic", "numerical",
  "Photoelectrons are emitted from a metal surface of work function 2.3 eV, and the stopping potential is found to "
  "be 0.8 V. Taking hc = 1240 eV nm, the wavelength of the incident light is:",
  *opt("400 nm", ["539 nm", "1550 nm", "827 nm"], "D"),
  "hν = φ₀ + eV₀",
  "The photon energy is the work function plus the maximum kinetic energy, eV₀ = 0.8 eV.",
  ["hν = 2.3 + 0.8 = 3.1 eV", "λ = 1240/3.1 = 400 nm"],
  why="539 nm is the threshold wavelength (photon energy equal to the work function alone). 1550 nm uses only the "
      "kinetic energy. 827 nm subtracts the kinetic energy from the work function instead of adding it.",
  ncert=DC + "Einstein's photoelectric equation", seconds=35, rc=True)

# ---- Intermediate
assert math.isclose(1 / math.sqrt(4), 0.5) and math.isclose(1 / math.sqrt(3), 0.577, rel_tol=1e-3)
q(DUAL, "de Broglie wavelength", "Intermediate", "numerical",
  "The kinetic energy of a non-relativistic electron, whose de Broglie wavelength is λ, is increased by 300%. Its new "
  "de Broglie wavelength is:",
  *opt("λ/2", ["λ/4", "λ/√3", "λ/3"], "B"),
  "λ = h/√(2mK) ∝ 1/√K",
  "An increase of 300% makes the new kinetic energy 4 times the original (K + 3K). The wavelength varies as 1/√K.",
  ["K′ = K + 3K = 4K", "λ′ = λ/√4 = λ/2"],
  why="λ/4 takes λ ∝ 1/K. λ/√3 takes the new energy as 3K instead of 4K. λ/3 combines both mistakes.",
  ncert=DC + "wave nature of matter", seconds=35, rc=True)

E_ph = 6.6e-34 * 3e8 / 600e-9
N_ph = 1.98 / E_ph
per_m2 = N_ph / (4 * math.pi * 1.0 ** 2)
close(E_ph, 3.3e-19)
close(N_ph, 6.0e18)
close(per_m2 * 1e-4, 4.77e13, 1e-3)
close(N_ph / math.pi * 1e-4, 1.91e14, 1e-3)
q(DUAL, "Photoelectric effect", "Intermediate", "numerical",
  "A small source emits monochromatic light of wavelength 600 nm uniformly in all directions, with a power of "
  "1.98 W. Taking h = 6.6 × 10⁻³⁴ J s and c = 3 × 10⁸ m/s, the number of photons falling per second on an area of "
  "1.0 cm² held at right angles to the light, 1.0 m from the source, is about:",
  *opt("4.8 × 10¹³", ["6.0 × 10¹⁸", "1.9 × 10¹⁴", "4.8 × 10¹⁷"], "A"),
  "Photon flux = (power/photon energy) spread over a sphere of area 4πr²",
  "First find the number of photons emitted per second; they spread uniformly over a sphere of radius 1.0 m, so the "
  "fraction reaching 1.0 cm² is (1.0 × 10⁻⁴)/(4π).",
  ["E = hc/λ = 6.6 × 10⁻³⁴ × 3 × 10⁸/(600 × 10⁻⁹) = 3.3 × 10⁻¹⁹ J",
   "N = 1.98/(3.3 × 10⁻¹⁹) = 6.0 × 10¹⁸ s⁻¹",
   "On 1.0 cm²: 6.0 × 10¹⁸ × 10⁻⁴/(4π × 1²) ≈ 4.8 × 10¹³ s⁻¹"],
  why="6.0 × 10¹⁸ is the total number emitted per second. 1.9 × 10¹⁴ spreads the photons over πr² instead of 4πr². "
      "4.8 × 10¹⁷ is the number per square metre, not per square centimetre.",
  ncert=DC + "particle nature of light: the photon", seconds=90, rc=True)

q(DUAL, "Photoelectric effect", "Intermediate", "multi_statement",
  ms("Which of the following statements about the early observations of the photoelectric effect, as described in "
     "NCERT, are correct?",
     ["Lenard observed that when ultraviolet radiation fell on the emitter plate in an evacuated glass tube having "
      "two electrodes, a current flowed in the circuit.",
      "Lenard observed that the current stopped as soon as the ultraviolet radiation was stopped.",
      "Hallwachs observed that a negatively charged zinc plate lost its charge when illuminated by ultraviolet light.",
      "Hallwachs observed that an uncharged zinc plate became negatively charged when irradiated by ultraviolet "
      "light.",
      "Metals such as zinc, cadmium and magnesium respond only to ultraviolet light, not to visible light."]),
  *mso({"a": True, "b": True, "c": True, "d": False, "e": True}, "abce", ["abc", "abcd", "ace"], "C"),
  "Hertz, Hallwachs and Lenard's observations",
  "Lenard found a current when UV fell on the emitter in an evacuated tube (a) and no current once the UV was cut "
  "off (b). Hallwachs found that a negatively charged zinc plate lost its charge under UV (c), and that an "
  "uncharged zinc plate became positively, not negatively, charged (d false), because it loses electrons. NCERT "
  "notes that zinc, cadmium and magnesium respond only to ultraviolet light (e).",
  ["(a) true", "(b) true", "(c) true", "(d) false: the plate became positively charged", "(e) true"],
  why="Options with (d) include a false statement; (a), (b) and (c) only and (a), (c) and (e) only leave out true "
      "statements.",
  ncert=DC + "photoelectric effect (Hertz's, Hallwachs' and Lenard's observations)", seconds=60)

q(DUAL, "de Broglie wavelength", "Intermediate", "assertion_reason",
  ar("An electron and a proton, each starting from rest, are accelerated through the same potential difference. The "
     "de Broglie wavelength of the electron is longer than that of the proton.",
     "For a particle of charge q and mass m accelerated from rest through a potential difference V, λ = h/√(2mqV), so "
     "for equal charges the lighter particle has the longer wavelength."),
  AR, ar_key(True, True, True),
  "λ = h/p with p = √(2mqV)",
  "Both particles have charge of magnitude e and gain the same kinetic energy eV. The momentum √(2meV) is smaller "
  "for the lighter electron, so its wavelength is longer. R gives exactly this reasoning.",
  ["Same |q| and V → same kinetic energy", "p = √(2mK) smaller for the electron → λ larger",
   "R explains A"],
  why="Both statements are true and the dependence λ ∝ 1/√m at equal charge and voltage is precisely why the "
      "electron's wavelength is longer.",
  ncert=DC + "wave nature of matter", seconds=40)

# ---- Advanced
E1 = F(1)
phi = 2 * E1 / 3
assert (2 * E1 - phi) == 4 * (E1 - phi)
assert E1 / phi == F(3, 2)
q(DUAL, "Einstein's equation", "Advanced", "numerical",
  "When light of wavelength λ falls on a metal surface, the maximum speed of the photoelectrons is v. When light of "
  "wavelength λ/2 falls on the same surface, the maximum speed becomes 2v. The threshold wavelength of the metal "
  "is:",
  *opt("3λ/2", ["2λ/3", "λ", "λ/2"], "D"),
  "Einstein's equation ½mv²_max = hc/λ − φ₀; threshold λ₀ = hc/φ₀",
  "Doubling the speed makes the maximum kinetic energy four times as large. Write Einstein's equation for both "
  "wavelengths with E = hc/λ.",
  ["E − φ₀ = ½mv²", "2E − φ₀ = ½m(2v)² = 4(E − φ₀)", "3φ₀ = 2E → φ₀ = 2E/3",
   "λ₀ = hc/φ₀ = (3/2)(hc/E) = 3λ/2"],
  why="2λ/3 inverts the ratio between λ₀ and λ. λ would make the photon energy equal to the work function, so no "
      "electrons would be emitted at λ. λ/2 is simply the second wavelength used.",
  ncert=DC + "Einstein's photoelectric equation", seconds=100, rc=True)

K_ratio = F(4, 1)                  # same p → K = p²/2m → K_p/K_α = m_α/m_p = 4
V_ratio = K_ratio * F(2, 1)        # V = K/q → V_p/V_α = (K_p/K_α)(q_α/q_p)
assert V_ratio == 8
q(DUAL, "de Broglie wavelength", "Advanced", "numerical",
  "A proton and an alpha particle, each starting from rest, are accelerated through different potential differences "
  "V_p and V_α so that they acquire the same de Broglie wavelength. Taking the mass of the alpha particle as 4 times "
  "and its charge as 2 times those of the proton, the ratio V_p : V_α is:",
  *opt("8 : 1", ["4 : 1", "2 : 1", "1 : 8"], "B"),
  "Equal de Broglie wavelengths mean equal momenta; K = p²/(2m) and qV = K",
  "With equal momenta, the kinetic energy is inversely proportional to the mass, so the proton has 4 times the "
  "kinetic energy of the alpha particle. The accelerating voltage needed is K/q, and the alpha particle has twice "
  "the charge.",
  ["Equal λ → equal p", "K_p/K_α = m_α/m_p = 4", "V_p/V_α = (K_p/e)/(K_α/2e) = 4 × 2 = 8"],
  why="4 : 1 compares the kinetic energies and ignores the different charges. 2 : 1 uses only the charge ratio. "
      "1 : 8 inverts the ratio.",
  ncert=DC + "wave nature of matter", seconds=90, rc=True)

KA, KB = 9e14 - 5e14, 9e14 - 7e14
close(KA / KB, 2.0)
close(7 / 5, 1.4)
q(DUAL, "Einstein's equation", "Advanced", "numerical",
  "The threshold frequencies of two metals A and B are 5.0 × 10¹⁴ Hz and 7.0 × 10¹⁴ Hz respectively. Light of "
  "frequency 9.0 × 10¹⁴ Hz falls on each. The ratio of the maximum kinetic energy of the photoelectrons from A to "
  "that from B is:",
  *opt("2", ["1.4", "1", "0.5"], "C"),
  "K_max = h(ν − ν₀)",
  "The maximum kinetic energy depends on how far the frequency exceeds the threshold of each metal; Planck's "
  "constant cancels in the ratio.",
  ["K_A = h(9.0 − 5.0) × 10¹⁴", "K_B = h(9.0 − 7.0) × 10¹⁴", "K_A/K_B = 4.0/2.0 = 2"],
  why="1.4 is the ratio of the threshold frequencies, inverted. 1 assumes the same light gives the same kinetic "
      "energy from any metal. 0.5 inverts the correct ratio.",
  ncert=DC + "Einstein's photoelectric equation", seconds=45, rc=True)


# ================================================================ Atoms and Nuclei (B4 I5 A4)
AC_ = NC + "'Atoms', "
NU = NC + "'Nuclei', "

# ---- Basic
A_Kr, Z_Kr = 235 + 1 - 141 - 3, 92 - 56
assert (A_Kr, Z_Kr) == (92, 36)
assert 236 - 141 == 95 and 235 - 141 - 3 == 91 and 92 + 3 - 56 == 39
q(AN, "Fission and fusion", "Basic", "numerical",
  "In one mode of fission of ²³⁵₉₂U by a slow neutron, the products are ¹⁴¹₅₆Ba, a krypton nucleus and three "
  "neutrons: ²³⁵₉₂U + ¹₀n → ¹⁴¹₅₆Ba + Kr + 3 ¹₀n. The krypton nucleus formed is:",
  *opt("⁹²₃₆Kr", ["⁹⁵₃₆Kr", "⁹¹₃₆Kr", "⁹²₃₉Kr"], "B"),
  "Conservation of mass number (nucleons) and of charge (atomic number) in nuclear reactions",
  "The total mass number and the total atomic number must be the same on both sides. Neutrons carry mass number 1 "
  "and charge 0.",
  ["Mass number: 235 + 1 = 141 + A + 3 → A = 92", "Atomic number: 92 + 0 = 56 + Z + 0 → Z = 36"],
  why="⁹⁵₃₆Kr forgets the three neutrons released. ⁹¹₃₆Kr forgets the incident neutron. ⁹²₃₉Kr counts the "
      "neutrons as if each carried a unit charge.",
  ncert=NU + "nuclear energy (fission)", seconds=35, rc=True)

q(AN, "Bohr model and hydrogen spectrum", "Basic", "match_list",
  ml("Match each spectral series of the hydrogen atom in List-I with the quantum number of the lower energy level "
     "on which all its transitions end (List-II).",
     ["Lyman series", "Balmer series", "Paschen series", "Brackett series"],
     ["n = 3", "n = 1", "n = 4", "n = 2"]),
  *mlo("A-II, B-IV, C-I, D-III",
       ["A-IV, B-II, C-I, D-III", "A-II, B-IV, C-III, D-I", "A-II, B-I, C-IV, D-III"], "C"),
  "Hydrogen spectrum: 1/λ = R(1/n_f² − 1/n_i²); each series has a fixed lower level n_f",
  "The Lyman series ends on n = 1 (ultraviolet), the Balmer series on n = 2 (visible), the Paschen series on "
  "n = 3 and the Brackett series on n = 4 (both infrared).",
  ["Lyman → n_f = 1", "Balmer → n_f = 2", "Paschen → n_f = 3", "Brackett → n_f = 4"],
  why="A-IV, B-II swaps the Lyman and Balmer series. C-III, D-I swaps the Paschen and Brackett series. B-I, C-IV "
      "shifts the Balmer and Paschen series to wrong levels.",
  ncert=AC_ + "atomic spectra (spectral series of hydrogen)", seconds=30)

pairs = {"HgAu": ((198, 80), (197, 79)), "HHe": ((3, 1), (3, 2)), "CC": ((12, 6), (14, 6)), "HHe4": ((2, 1), (4, 2))}
N_of = lambda p: (p[0][0] - p[0][1], p[1][0] - p[1][1])
assert N_of(pairs["HgAu"]) == (118, 118)
assert N_of(pairs["HHe"]) == (2, 1) and N_of(pairs["CC"]) == (6, 8) and N_of(pairs["HHe4"]) == (1, 2)
q(AN, "Nuclear size and mass defect", "Basic", "direct",
  "Which one of the following pairs of nuclides are isotones (nuclides with the same number of neutrons)?",
  *opt("¹⁹⁸₈₀Hg and ¹⁹⁷₇₉Au", ["³₁H and ³₂He", "¹²₆C and ¹⁴₆C", "²₁H and ⁴₂He"], "D"),
  "Isotopes (same Z), isobars (same A), isotones (same N = A − Z)",
  "Find N = A − Z for each nuclide. ¹⁹⁸Hg has 198 − 80 = 118 neutrons and ¹⁹⁷Au has 197 − 79 = 118 neutrons.",
  ["Hg: N = 118; Au: N = 118 → isotones", "³H (N = 2), ³He (N = 1): isobars",
   "¹²C (N = 6), ¹⁴C (N = 8): isotopes", "²H (N = 1), ⁴He (N = 2): none of these"],
  why="³H and ³He have the same mass number (isobars). ¹²C and ¹⁴C have the same atomic number (isotopes). ²H and "
      "⁴He have different N, Z and A.",
  ncert=NU + "atomic masses and composition of nucleus", seconds=35, rc=True)

q(AN, "Nuclear size and mass defect", "Basic", "statement_pair",
  sp("The radius of an atom is only about 10 times the radius of its nucleus.",
     "More than 99.9% of the mass of an atom is concentrated in its nucleus."),
  SP, sp_key(False, True),
  "Size of the nucleus compared with the atom; mass of the nucleus",
  "Nuclear radii are of the order of 10⁻¹⁵ to 10⁻¹⁴ m, while atoms are about 10⁻¹⁰ m in size, so the atom is about "
  "10⁴ to 10⁵ times larger (Statement I false). The electrons are very light (about 1/1836 of a proton's mass "
  "each), so more than 99.9% of the mass is in the nucleus (Statement II true).",
  ["Atom ~10⁻¹⁰ m; nucleus ~10⁻¹⁵–10⁻¹⁴ m → ratio ~10⁴–10⁵ → I false",
   "Electrons contribute < 0.1% of the mass → II true"],
  why="Statement I understates the size of the atom relative to the nucleus by a factor of thousands; Statement II "
      "is correct.",
  ncert=NU + "size of the nucleus", seconds=30)

# ---- Intermediate
lam_b = 656 * (F(1, 4) - F(1, 9)) / (F(1, 4) - F(1, 16))
lam_g = 656 * (F(1, 4) - F(1, 9)) / (F(1, 4) - F(1, 25))
close(float(lam_b), 486, 2e-3)
close(float(lam_g), 434, 2e-3)
close(656 * 1.35, 886, 2e-3)
close(656 * 9 / 16, 369, 2e-3)
q(AN, "Bohr model and hydrogen spectrum", "Intermediate", "numerical",
  "The first line of the Balmer series of hydrogen (transition n = 3 → n = 2) has a wavelength of 656 nm. The "
  "wavelength of the second line of the series (transition n = 4 → n = 2) is about:",
  *opt("486 nm", ["886 nm", "369 nm", "434 nm"], "A"),
  "1/λ = R(1/2² − 1/n²) for the Balmer series",
  "Take the ratio of the two wavelengths so that the Rydberg constant cancels.",
  ["λ₄₂/λ₃₂ = (1/4 − 1/9)/(1/4 − 1/16) = (5/36)/(3/16) = 20/27",
   "λ₄₂ = 656 × 20/27 ≈ 486 nm"],
  why="886 nm inverts the ratio, giving a longer wavelength for a larger energy gap. 369 nm scales the wavelength by "
      "the ratio of n² values (9/16). 434 nm is the third line (n = 5 → 2).",
  ncert=AC_ + "atomic spectra (Balmer series)", seconds=60, rc=True)

E = lambda n: -13.6 / n ** 2
close(E(3) - E(1), 12.09, 1e-3)
close(E(3) - E(2), 1.89, 2e-3)
close(E(2) - E(1), 10.2)
q(AN, "Bohr model and hydrogen spectrum", "Intermediate", "numerical",
  "Hydrogen atoms in the ground state are to be excited so that they can emit the first line of the Balmer series "
  "(n = 3 → n = 2). Using E_n = −13.6/n² eV, the minimum energy that a ground-state atom must absorb is about:",
  *opt("12.09 eV", ["1.89 eV", "10.2 eV", "13.6 eV"], "C"),
  "To emit a line starting at n = 3, the electron must first be raised to n = 3",
  "The Balmer-α line comes from the n = 3 → n = 2 transition, so the atom must first reach the n = 3 level from "
  "n = 1.",
  ["E₃ − E₁ = −13.6/9 − (−13.6) = 13.6 × 8/9", "≈ 12.09 eV"],
  why="1.89 eV is the energy of the emitted Balmer-α photon, not the energy needed to reach n = 3 from the ground "
      "state. 10.2 eV only reaches n = 2, from which no Balmer line can be emitted. 13.6 eV would ionise the atom.",
  ncert=AC_ + "Bohr model of the hydrogen atom (energy levels)", seconds=45, rc=True)

S_n = 127.6 - 111.96
close(S_n, 15.64)
close(127.6 / 16, 7.975)
close(111.96 / 15, 7.464, 1e-3)
q(AN, "Binding energy", "Intermediate", "numerical",
  "The binding energy of the ¹⁶₈O nucleus is 127.6 MeV and that of the ¹⁵₈O nucleus is 111.96 MeV. The minimum "
  "energy needed to remove one neutron from a ¹⁶O nucleus is about:",
  *opt("15.6 MeV", ["8.0 MeV", "239.6 MeV", "7.5 MeV"], "B"),
  "Binding energy = energy needed to separate a nucleus completely into free nucleons",
  "Removing one neutron from ¹⁶O leaves ¹⁵O and a free neutron. The energy needed is the binding energy of ¹⁶O less "
  "the binding energy that ¹⁵O still has.",
  ["¹⁶O → ¹⁵O + n", "E = BE(¹⁶O) − BE(¹⁵O) = 127.6 − 111.96 ≈ 15.6 MeV"],
  why="8.0 MeV is the average binding energy per nucleon of ¹⁶O, not the energy for removing a particular neutron. "
      "239.6 MeV adds the two binding energies. 7.5 MeV is the binding energy per nucleon of ¹⁵O.",
  ncert=NU + "mass-energy and nuclear binding energy", seconds=50, rc=True)

q(AN, "Bohr model and hydrogen spectrum", "Intermediate", "assertion_reason",
  ar("In the Bohr model, the energy of the singly ionised helium ion (He⁺) in its ground state is −54.4 eV.",
     "In the Bohr model, the energy levels of a hydrogen-like ion of atomic number Z are proportional to Z."),
  AR, ar_key(True, False),
  "Energy levels of hydrogen-like ions: E_n = −13.6 Z²/n² eV",
  "For He⁺, Z = 2 and n = 1, so E₁ = −13.6 × 4 = −54.4 eV (A true). The energy is proportional to Z², not Z "
  "(R false); a dependence on Z alone would give −27.2 eV.",
  ["E₁(He⁺) = −13.6 × 2²/1² = −54.4 eV → A true", "E ∝ Z², not Z → R false"],
  why="A is correct, but R gives the wrong dependence on Z; with E ∝ Z the ground-state energy of He⁺ would be "
      "−27.2 eV.",
  ncert=AC_ + "Bohr model of the hydrogen atom", seconds=40)

q(AN, "Binding energy", "Intermediate", "statement_pair",
  sp("The binding energy per nucleon of the deuteron (about 1.1 MeV) is much smaller than that of the ⁴He nucleus "
     "(about 7 MeV).",
     "The mass of a ⁵⁶Fe nucleus is greater than the total mass of its 26 protons and 30 neutrons taken separately."),
  SP, sp_key(True, False),
  "Binding energy per nucleon; mass defect",
  "The deuteron's binding energy is about 2.2 MeV, i.e. about 1.1 MeV per nucleon, whereas ⁴He has about 28.3 MeV, "
  "about 7.1 MeV per nucleon (Statement I true). Every stable nucleus has a mass defect: its mass is less than the "
  "total mass of its free nucleons (Statement II false).",
  ["²H: 2.22/2 ≈ 1.1 MeV per nucleon; ⁴He: 28.3/4 ≈ 7.1 MeV → I true",
   "Nucleus mass < sum of nucleon masses (mass defect) → II false"],
  why="Statement II reverses the mass defect; Statement I is correct, so the remaining options are wrong.",
  ncert=NU + "mass-energy and nuclear binding energy", seconds=40)

# ---- Advanced
levels = [E(n) - E(1) for n in range(2, 6)]
reach = max(n for n in range(2, 6) if E(n) - E(1) <= 12.5)
assert reach == 3 and reach * (reach - 1) // 2 == 3
assert 4 * 3 // 2 == 6
q(AN, "Bohr model and hydrogen spectrum", "Advanced", "numerical",
  "A beam of electrons, each of kinetic energy 12.5 eV, passes through hydrogen gas whose atoms are in the ground "
  "state. An electron can give any part of its kinetic energy to an atom in a collision. Using E_n = −13.6/n² eV, "
  "the number of different spectral lines that can appear in the emission from the excited atoms is:",
  *opt("3", ["6", "1", "2"], "A"),
  "Collisional excitation: the atom can absorb any amount up to the electron's energy, but only reaches allowed "
  "levels",
  "E₂ − E₁ = 10.2 eV, E₃ − E₁ = 12.09 eV and E₄ − E₁ = 12.75 eV. With 12.5 eV available, atoms can be raised to "
  "n = 2 or n = 3 but not to n = 4. From n = 3 the possible transitions are 3→2, 3→1 and 2→1.",
  ["Reachable levels: n = 2 (10.2 eV), n = 3 (12.09 eV); n = 4 needs 12.75 eV > 12.5 eV",
   "Lines: 3 → 1, 3 → 2, 2 → 1 → 3 lines"],
  why="6 lines would need atoms in n = 4, which requires 12.75 eV. 1 or 2 lines ignore some of the downward "
      "transitions from n = 3 (directly to n = 1, or in steps through n = 2).",
  ncert=AC_ + "Bohr model of the hydrogen atom (energy levels)", seconds=80, rc=True)

N_D = 1000 / 2.0 * 6.0e23
E_DD = N_D / 2 * 3.27 * 1.6e-13
close(E_DD, 7.85e13, 1e-3)
close(N_D * 3.27 * 1.6e-13, 1.57e14, 1e-3)
close(1 / 2.0 * 6.0e23 / 2 * 3.27 * 1.6e-13, 7.85e10, 1e-3)
close(E_DD / 2, 3.924e13, 1e-3)
q(AN, "Fission and fusion", "Advanced", "numerical",
  "In the fusion reaction ²H + ²H → ³He + n, an energy of 3.27 MeV is released per reaction. Taking the molar mass "
  "of deuterium atoms as 2.0 g mol⁻¹, Avogadro's number as 6.0 × 10²³ mol⁻¹ and 1 MeV = 1.6 × 10⁻¹³ J, the energy "
  "that would be released if all the deuterons in 1.0 kg of deuterium fused in this way is about:",
  *opt("7.8 × 10¹³ J", ["1.6 × 10¹⁴ J", "7.8 × 10¹⁰ J", "3.9 × 10¹³ J"], "D"),
  "Energy released = number of reactions × Q; each reaction uses two deuterons",
  "Find the number of deuterons in 1.0 kg, halve it to get the number of reactions, and multiply by the energy per "
  "reaction.",
  ["Deuterons = (1000/2.0) × 6.0 × 10²³ = 3.0 × 10²⁶", "Reactions = 1.5 × 10²⁶",
   "E = 1.5 × 10²⁶ × 3.27 × 1.6 × 10⁻¹³ ≈ 7.8 × 10¹³ J"],
  why="1.6 × 10¹⁴ J counts one reaction per deuteron. 7.8 × 10¹⁰ J treats 1.0 kg as 1.0 g. 3.9 × 10¹³ J halves "
      "the number of reactions a second time.",
  ncert=NU + "nuclear energy (fusion)", seconds=90, rc=True)

r_p_over_a = F(1, 1) / F(2, 4)       # r0 ∝ q/m at equal speed (r0 = k q Z e/(½ m v²))
assert r_p_over_a == 2
q(AN, "Rutherford scattering", "Advanced", "numerical",
  "A proton and an alpha particle, moving with the same speed, are each projected head-on towards the same heavy "
  "nucleus (which may be taken as fixed). Taking the mass of the alpha particle as 4 times and its charge as 2 times "
  "those of the proton, the ratio of their distances of closest approach, r_p : r_α, is:",
  *opt("2 : 1", ["1 : 2", "1 : 1", "4 : 1"], "B"),
  "At closest approach (head-on), kinetic energy = electrostatic potential energy: ½mv² = kqZe/r₀",
  "r₀ = 2kqZe/(mv²). For equal speeds and the same nucleus, r₀ ∝ q/m.",
  ["r₀ ∝ q/m", "Proton: 1/1 = 1; alpha: 2/4 = 1/2", "r_p : r_α = 1 : 1/2 = 2 : 1"],
  why="1 : 2 inverts the ratio. 1 : 1 assumes equal kinetic energies and equal charges. 4 : 1 uses the kinetic "
      "energies (r₀ ∝ 1/K) but ignores the different charges.",
  ncert=AC_ + "alpha-particle scattering and Rutherford's nuclear model (distance of closest approach)",
  seconds=80, rc=True)

r2_ = 0.53 * 2 ** 2
lam_dB = 2 * math.pi * r2_ / 2
close(lam_dB, 6.66, 1e-3)
close(2 * math.pi * r2_, 13.3, 2e-3)
close(2 * math.pi * 0.53, 3.33, 2e-3)
close(2 * math.pi * 0.53 / 2, 1.665, 1e-3)
q(AN, "Bohr model and hydrogen spectrum", "Advanced", "numerical",
  "In the Bohr model of the hydrogen atom, the radius of the first orbit is 0.53 Å and the radius of the nth orbit is "
  "n² times this. Using de Broglie's interpretation of Bohr's quantisation condition, the de Broglie wavelength of "
  "the electron in the n = 2 orbit is about:",
  *opt("6.66 Å", ["13.3 Å", "3.33 Å", "1.67 Å"], "D"),
  "de Broglie's condition for a stationary orbit: 2πr_n = nλ",
  "The circumference of the nth orbit holds exactly n de Broglie wavelengths, so λ = 2πr_n/n.",
  ["r₂ = 4 × 0.53 = 2.12 Å", "λ = 2πr₂/2 = π × 2.12 ≈ 6.66 Å"],
  why="13.3 Å is the whole circumference (it forgets that two wavelengths fit in it). 3.33 Å is the wavelength in "
      "the ground state. 1.67 Å uses the ground-state radius with n = 2.",
  ncert=AC_ + "de Broglie's explanation of Bohr's second postulate of quantisation", seconds=70, rc=True)


# ================================================================ Electronic Devices (B4 I5 A4)
SD = NC + "'Semiconductor Electronics: Materials, Devices and Simple Circuits', "
NOT = lambda a: 1 - a
AND = lambda a, b: a & b
OR = lambda a, b: a | b
NAND = lambda a, b: NOT(a & b)
NOR = lambda a, b: NOT(a | b)

# ---- Basic
q(ED, "Semiconductors", "Basic", "direct",
  "Pure germanium is to be made an n-type semiconductor. Which one of the following should be added to it in a "
  "small, controlled amount?",
  *opt("Antimony", ["Indium", "Aluminium", "Gallium"], "D"),
  "Doping: a pentavalent (group 15) impurity gives n-type, a trivalent (group 13) impurity gives p-type",
  "Antimony is pentavalent. Four of its valence electrons form covalent bonds with neighbouring germanium atoms and "
  "the fifth is easily freed, so electrons become the majority carriers.",
  ["Antimony: pentavalent donor → extra free electrons → n-type"],
  why="Indium, aluminium and gallium are trivalent; each creates a hole and makes germanium p-type.",
  ncert=SD + "extrinsic semiconductor (n-type)", seconds=25)

q(ED, "Semiconductors", "Basic", "match_list",
  ml("Match each class of semiconductor in List-I with an example from List-II, as given in NCERT.",
     ["Elemental semiconductor", "Inorganic compound semiconductor", "Organic semiconductor",
      "Organic polymer semiconductor"],
     ["Polyaniline", "Germanium", "Anthracene", "Cadmium sulphide (CdS)"]),
  *mlo("A-II, B-IV, C-III, D-I",
       ["A-IV, B-II, C-III, D-I", "A-II, B-IV, C-I, D-III", "A-II, B-III, C-IV, D-I"], "B"),
  "Classification of semiconductor materials",
  "NCERT lists Si and Ge as elemental semiconductors; CdS, GaAs, CdSe and InP as inorganic compound semiconductors; "
  "anthracene and doped phthalocyanines as organic semiconductors; and polypyrrole, polyaniline and polythiophene "
  "as organic polymers.",
  ["Elemental → germanium", "Inorganic compound → CdS", "Organic → anthracene", "Organic polymer → polyaniline"],
  why="A-IV, B-II swaps the element and the compound. C-I, D-III swaps the organic molecule and the polymer. "
      "B-III, C-IV gives anthracene as an inorganic compound.",
  ncert=SD + "classification of metals, conductors and semiconductors", seconds=35)

A_seq = [0, 0, 1, 1, 0, 1]
B_seq = [0, 1, 1, 0, 0, 1]
seqs = {g: [fn(a, b) for a, b in zip(A_seq, B_seq)] for g, fn in
        {"NOR": NOR, "OR": OR, "NAND": NAND, "AND": AND}.items()}
assert seqs["NOR"] == [1, 0, 0, 0, 1, 0]
assert seqs["OR"] == [0, 1, 1, 1, 0, 1] and seqs["NAND"] == [1, 1, 0, 1, 1, 0] and seqs["AND"] == [0, 0, 1, 0, 0, 1]
q(ED, "Logic gates", "Basic", "direct",
  "The two inputs of a NOR gate take the following values in six successive time intervals: A = 0, 0, 1, 1, 0, 1 "
  "and B = 0, 1, 1, 0, 0, 1. The output of the gate in these intervals is:",
  *opt("1, 0, 0, 0, 1, 0", ["0, 1, 1, 1, 0, 1", "1, 1, 0, 1, 1, 0", "0, 0, 1, 0, 0, 1"], "A"),
  "NOR: output 1 only when both inputs are 0",
  "Check each interval: the output is 1 only in the intervals where A = 0 and B = 0 (the first and the fifth).",
  ["(A, B) = (0,0), (0,1), (1,1), (1,0), (0,0), (1,1)", "NOR outputs: 1, 0, 0, 0, 1, 0"],
  why="0, 1, 1, 1, 0, 1 is the OR output (NOR without the inversion). 1, 1, 0, 1, 1, 0 is the NAND output. "
      "0, 0, 1, 0, 0, 1 is the AND output.",
  ncert=SD + "digital electronics and logic gates (NOR gate)", seconds=40, rc=True)

q(ED, "p-n junction diode and rectifier", "Basic", "statement_pair",
  sp("In the depletion region of an unbiased p-n junction, the n-side has a layer of immobile positive ions.",
     "The electric field in the depletion region of an unbiased p-n junction is directed from the p-side to the "
     "n-side."),
  SP, sp_key(True, False),
  "Formation of the depletion region and the barrier field",
  "Electrons diffusing from the n-side leave behind ionised donors, which are immobile positive ions (Statement I "
  "true); holes diffusing from the p-side leave negative acceptor ions. The field points from the positive ions to "
  "the negative ions, i.e. from the n-side to the p-side (Statement II false).",
  ["n-side of depletion region: +ve donor ions → I true", "Field from + to −: n → p, not p → n → II false"],
  why="Statement II reverses the direction of the junction field; Statement I is correct, so the remaining options "
      "are wrong.",
  ncert=SD + "p-n junction formation", seconds=35)

# ---- Intermediate
I_pl = (2.7 - 0.7) / (90 + 10)
close(I_pl, 0.020)
close(2.7 / 100, 0.027)
close(2.0 / 90, 0.0222, 2e-3)
close(2.7 / 90, 0.030)
q(ED, "p-n junction diode and rectifier", "Intermediate", "numerical",
  "A junction diode is modelled as follows: it conducts only when the forward voltage across it exceeds 0.7 V, and "
  "above that its dynamic resistance is a constant 10 Ω (forward voltage = 0.7 V + 10 Ω × current). The diode, "
  "forward biased, is connected in series with a 90 Ω resistor across a 2.7 V DC source of negligible internal "
  "resistance. The current in the circuit is:",
  *opt("20 mA", ["27 mA", "22 mA", "30 mA"], "D"),
  "Piecewise-linear model of a forward-biased diode: V = V_knee + I r_d",
  "Around the loop, the source emf equals the knee voltage plus the drops across the dynamic resistance and the "
  "series resistor.",
  ["2.7 = 0.7 + I(10 + 90)", "I = 2.0/100 = 0.020 A = 20 mA"],
  why="27 mA ignores the 0.7 V knee voltage. 22 mA ignores the 10 Ω dynamic resistance. 30 mA ignores both.",
  ncert=SD + "semiconductor diode (I–V characteristics, dynamic resistance)", seconds=50, rc=True)

q(ED, "LED, photodiode and solar cell", "Intermediate", "multi_statement",
  ms("Which of the following statements about light emitting diodes (LEDs), as described in NCERT, are correct?",
     ["LEDs work at a low operational voltage and need less power than conventional incandescent lamps.",
      "LEDs act fast and need no warm-up time.",
      "The bandwidth of the light emitted by an LED is about 100 Å to 500 Å, so the light is nearly (but not "
      "exactly) monochromatic.",
      "An LED emits light when it is reverse biased.",
      "An LED is made from a lightly doped p-n junction."]),
  *mso({"a": True, "b": True, "c": True, "d": False, "e": False}, "abc", ["ab", "abce", "bcd"], "B"),
  "Light emitting diode: heavily doped, forward biased; advantages over incandescent lamps",
  "NCERT lists the advantages of LEDs: low operational voltage and less power (a), fast action with no warm-up "
  "time (b), nearly monochromatic light with a bandwidth of 100–500 Å (c), long life and fast on-off switching. An "
  "LED is a heavily doped p-n junction that emits light under forward bias, so (d) and (e) are false.",
  ["(a) true", "(b) true", "(c) true", "(d) false: forward biased", "(e) false: heavily doped"],
  why="Options containing (d) or (e) include a false statement; (a) and (b) only leaves out the true statement (c).",
  ncert=SD + "optoelectronic junction devices (light emitting diode)", seconds=50)

q(ED, "p-n junction diode and rectifier", "Intermediate", "assertion_reason",
  ar("The reverse current of a junction diode (below breakdown) increases when the temperature of the diode is "
     "raised.",
     "The reverse current is carried by minority carriers, whose number increases as more electron–hole pairs are "
     "generated thermally at higher temperature."),
  AR, ar_key(True, True, True),
  "Reverse current of a diode is due to the drift of minority carriers",
  "Under reverse bias, the junction field sweeps across only the minority carriers, so the reverse current is "
  "limited by their number, not by the applied voltage. Raising the temperature generates more electron–hole pairs, "
  "increasing the minority carriers and hence the reverse current. R explains A.",
  ["Reverse current ∝ number of minority carriers", "Higher T → more thermally generated pairs → more minority "
   "carriers", "Reverse current increases; R explains A"],
  why="Both statements are true, and the thermal generation of minority carriers is precisely why the reverse "
      "current rises with temperature.",
  ncert=SD + "p-n junction diode under reverse bias", seconds=40)

nand_or = lambda a, b: NAND(NAND(a, a), NAND(b, b))
assert all(nand_or(a, b) == OR(a, b) for a in (0, 1) for b in (0, 1))
assert any(NAND(NAND(a, a), b) != OR(a, b) for a in (0, 1) for b in (0, 1))
q(ED, "Logic gates", "Intermediate", "direct",
  "Only two-input NAND gates are available. The least number of such gates needed to make a circuit that behaves as "
  "a two-input OR gate is:",
  *opt("3", ["2", "4", "1"], "B"),
  "NAND is a universal gate; by De Morgan's theorem A + B = NOT(Ā · B̄)",
  "Two NAND gates, each with its inputs joined, act as NOT gates and give Ā and B̄. A third NAND gate fed with Ā and "
  "B̄ gives NOT(Ā · B̄) = A + B.",
  ["NAND with inputs joined → NOT: 2 gates give Ā and B̄", "Third NAND: NOT(Ā · B̄) = A + B → 3 gates"],
  why="Two gates give either an AND (NAND followed by NOT) or only one inverted input, not OR. Four NAND gates are "
      "needed for a NOR. One NAND gate is just a NAND.",
  ncert=SD + "digital electronics and logic gates (NAND as a universal gate)", seconds=45, rc=True)

Ipk1, Ipk2 = 10 / 1000, 10 / 2000
close(Ipk1, 0.010)
close(Ipk2, 0.005)
close(10 / 3000, 0.003333, 1e-3)
q(ED, "p-n junction diode and rectifier", "Intermediate", "numerical",
  "An AC source of peak voltage 10 V is connected across two branches in parallel. Branch 1 has an ideal diode D₁ "
  "in series with a 1 kΩ resistor, and branch 2 has an ideal diode D₂ in series with a 2 kΩ resistor; D₂ is "
  "connected the opposite way round to D₁, so that D₁ conducts during one half-cycle and D₂ during the other. The "
  "peak currents drawn from the source in the half-cycle when D₁ conducts and in the half-cycle when D₂ conducts are, "
  "respectively:",
  *opt("10 mA and 5 mA", ["15 mA in both half-cycles", "10 mA and zero", "3.3 mA in both half-cycles"], "D"),
  "An ideal diode conducts with zero resistance in forward bias and blocks completely in reverse bias",
  "In each half-cycle only one branch conducts, so the source sees only that branch's resistor.",
  ["D₁ half-cycle: I = 10 V/1 kΩ = 10 mA", "D₂ half-cycle: I = 10 V/2 kΩ = 5 mA"],
  why="15 mA lets both branches conduct together. 10 mA and zero ignores the reversed diode D₂, which conducts in "
      "the other half-cycle. 3.3 mA puts the two resistors in series.",
  ncert=SD + "application of junction diode as a rectifier", seconds=50, rc=True)

# ---- Advanced
V_open = 10 * 3 / (2 + 3)
assert V_open == 6 > 4                  # the ideal diode is forward biased and clamps the midpoint to 4 V
I_top, I_bot = (10 - 4) / 2, 4 / 3      # in mA (kΩ)
I_d = I_top - I_bot
close(I_d, 5 / 3)
close((V_open - 4) / (2 * 3 / (2 + 3)), 5 / 3)
close((V_open - 4) / 5, 0.4)
q(ED, "p-n junction diode and rectifier", "Advanced", "numerical",
  "An ideal 10 V battery (negative terminal at point G) is connected across a 2 kΩ resistor and a 3 kΩ resistor in "
  "series, the 3 kΩ resistor being joined to G; M is the junction of the two resistors. An ideal diode has its anode "
  "at M and its cathode joined to the positive terminal of an ideal 4 V battery whose negative terminal is at G. The "
  "current through the diode is about:",
  *opt("1.67 mA", ["zero", "0.4 mA", "3.0 mA"], "A"),
  "An ideal diode conducts if its anode would otherwise be at a higher potential than its cathode, and then has zero "
  "voltage drop",
  "Without the diode, M would be at 10 × 3/5 = 6 V, which is above 4 V, so the diode conducts and holds M at 4 V. "
  "Then apply the junction rule at M.",
  ["Diode conducting → V_M = 4 V", "Current in 2 kΩ = (10 − 4)/2 = 3 mA (into M)",
   "Current in 3 kΩ = 4/3 ≈ 1.33 mA (out of M)", "Diode current = 3 − 1.33 ≈ 1.67 mA"],
  why="Zero assumes the diode is reverse biased, but M would be at 6 V, above the 4 V on the cathode. 0.4 mA divides "
      "the 2 V excess by 5 kΩ instead of by the 1.2 kΩ of the two resistors in parallel. 3.0 mA is the current in "
      "the 2 kΩ resistor, part of which goes through the 3 kΩ resistor.",
  ncert=SD + "semiconductor diode (forward bias)", seconds=110, rc=True)

ni, NA_, ND_ = 1.5e16, 1.0e21, 5.0e20
nh = NA_ - ND_
ne = ni ** 2 / nh
close(nh, 5.0e20)
close(ne, 4.5e11)
close(ni ** 2 / NA_, 2.25e11)
q(ED, "Semiconductors", "Advanced", "numerical",
  "A silicon sample (intrinsic carrier concentration 1.5 × 10¹⁶ m⁻³) is doped with 1.0 × 10²¹ m⁻³ acceptor atoms and "
  "5.0 × 10²⁰ m⁻³ donor atoms, all of which are ionised. In thermal equilibrium, the type of the semiconductor and "
  "its electron concentration are:",
  *opt("p-type; about 4.5 × 10¹¹ m⁻³", ["p-type; about 2.25 × 10¹¹ m⁻³", "n-type; about 5.0 × 10²⁰ m⁻³",
                                         "p-type; about 1.5 × 10¹⁶ m⁻³"], "B"),
  "Net doping decides the type; n_e n_h = n_i² in equilibrium",
  "The donors' electrons fill an equal number of the acceptors' holes, so the net hole concentration is "
  "N_A − N_D = 5.0 × 10²⁰ m⁻³ (p-type). The electron concentration then follows from the mass-action law.",
  ["n_h ≈ N_A − N_D = 1.0 × 10²¹ − 5.0 × 10²⁰ = 5.0 × 10²⁰ m⁻³",
   "n_e = n_i²/n_h = (1.5 × 10¹⁶)²/(5.0 × 10²⁰) = 4.5 × 10¹¹ m⁻³"],
  why="2.25 × 10¹¹ m⁻³ ignores the donors, taking n_h = N_A. n-type with 5.0 × 10²⁰ m⁻³ electrons gets the type "
      "wrong: the acceptors outnumber the donors. 1.5 × 10¹⁶ m⁻³ is the intrinsic value, which applies only to the "
      "undoped crystal.",
  ncert=SD + "extrinsic semiconductor", seconds=90, rc=True)

Y_seq = [NAND(NOT(a), b) for a, b in ((0, 0), (0, 1), (1, 0), (1, 1))]
assert Y_seq == [1, 0, 1, 1]
assert [AND(NOT(a), b) for a, b in ((0, 0), (0, 1), (1, 0), (1, 1))] == [0, 1, 0, 0]
assert [NAND(a, NOT(b)) for a, b in ((0, 0), (0, 1), (1, 0), (1, 1))] == [1, 1, 0, 1]
assert [NAND(a, b) for a, b in ((0, 0), (0, 1), (1, 0), (1, 1))] == [1, 1, 1, 0]
q(ED, "Logic gates", "Advanced", "direct",
  "Input A is passed through a NOT gate. The output of the NOT gate and input B are then fed to a two-input NAND "
  "gate, whose output is Y. For the inputs (A, B) = (0, 0), (0, 1), (1, 0) and (1, 1), in that order, the outputs Y "
  "are:",
  *opt("1, 0, 1, 1", ["0, 1, 0, 0", "1, 1, 0, 1", "1, 1, 1, 0"], "D"),
  "Y = NOT(Ā · B) = A + B̄ (De Morgan's theorem)",
  "Work out Ā for each input, AND it with B, and invert the result. Equivalently Y = A + B̄, which is 0 only when "
  "A = 0 and B = 1.",
  ["(0,0): Ā·B = 1·0 = 0 → Y = 1", "(0,1): 1·1 = 1 → Y = 0", "(1,0): 0·0 = 0 → Y = 1", "(1,1): 0·1 = 0 → Y = 1"],
  why="0, 1, 0, 0 forgets the final inversion of the NAND gate. 1, 1, 0, 1 inverts B instead of A. 1, 1, 1, 0 "
      "ignores the NOT gate (a plain NAND of A and B).",
  ncert=SD + "digital electronics and logic gates", seconds=60, rc=True)

Iz_max = 0.50 / 5.0
I_L = 5.0 / 250
Vin_max = 5.0 + (Iz_max + I_L) * 50
close(Vin_max, 11.0)
close(5.0 + Iz_max * 50, 10.0)
close(5.0 + I_L * 50, 6.0)
close(5.0 + (Iz_max + I_L) * 250, 35.0)
q(ED, "Zener diode", "Advanced", "numerical",
  "A Zener diode of breakdown voltage 5.0 V and maximum power rating 0.50 W is used as a voltage regulator. It is "
  "connected through a 50 Ω series resistor to a variable DC input, and a 250 Ω load resistor is connected across "
  "it. Taking the voltage across the Zener diode as constant at 5.0 V in breakdown, the largest input voltage for "
  "which the Zener diode does not exceed its power rating is:",
  *opt("11 V", ["10 V", "6 V", "35 V"], "A"),
  "Zener regulator: I_series = I_Z + I_L; P_Z = V_Z I_Z",
  "The largest permissible Zener current is P/V_Z. The load current is fixed by the constant 5.0 V across the load. "
  "The series resistor carries both, and the input equals V_Z plus the drop across the series resistor.",
  ["I_Z(max) = 0.50/5.0 = 100 mA", "I_L = 5.0/250 = 20 mA", "I_series = 120 mA",
   "V_in(max) = 5.0 + 0.120 × 50 = 11 V"],
  why="10 V leaves out the load current through the series resistor. 6 V leaves out the Zener current. 35 V uses "
      "the load resistance in place of the series resistance.",
  ncert=SD + "Zener diode as a voltage regulator", seconds=90, rc=True)


# ================================================================ Experimental Skills (B3 I3 A3)
LAB = "NMC syllabus, Experimental Skills: "

# ---- Basic
g_s = 4 * math.pi ** 2 / 4.00
close(g_s, 9.87, 1e-3)
close(4.00 / (4 * math.pi ** 2), 0.101, 5e-3)
close(4 * math.pi ** 2 * 4.00, 158, 2e-3)
q(EXP, "Mechanics experiments", "Basic", "numerical",
  "In a simple pendulum experiment, a graph of T² (in s²) against the effective length L (in m) is a straight line "
  "through the origin with a slope of 4.00 s² m⁻¹. The value of g obtained from the graph is about:",
  *opt("9.87 m/s²", ["0.101 m/s²", "158 m/s²", "3.14 m/s²"], "B"),
  "T = 2π√(L/g) → T² = (4π²/g)L",
  "The slope of the T²–L line is 4π²/g, so g = 4π²/slope.",
  ["Slope = 4π²/g = 4.00 s² m⁻¹", "g = 4π²/4.00 = π² ≈ 9.87 m/s²"],
  why="0.101 m/s² takes g = slope/4π². 158 m/s² multiplies the slope by 4π². 3.14 m/s² takes the square root of the "
      "correct value (π instead of π²).",
  ncert=LAB + "simple pendulum (T² against L)", seconds=35, rc=True)

q(EXP, "Mechanics experiments", "Basic", "direct",
  "In Searle's apparatus for finding the Young's modulus of the material of a wire, two identical wires hang from "
  "the same rigid support: the experimental wire, which is loaded, and a reference wire carrying a constant load. "
  "The reference wire is used mainly to:",
  *opt("compensate for any change in length due to temperature changes and for any yielding of the support, since "
       "these affect both wires equally",
       ["double the extension, so that it can be read more easily",
        "provide a second, independent value of Young's modulus to be averaged",
        "measure the load hung on the experimental wire"], "C"),
  "Searle's method: extension measured relative to an identical reference wire",
  "The spirit level and micrometer measure the extension of the experimental wire relative to the reference wire. "
  "Changes of room temperature or a slight sag of the support lengthen both wires equally and so do not appear in "
  "the measured extension.",
  ["Both wires share the support and the surroundings", "Only the relative extension (due to the load) is measured"],
  why="The reference wire carries a constant load, so it neither doubles the extension nor gives a second value of "
      "Y, and it plays no part in measuring the load.",
  ncert=LAB + "Young's modulus of elasticity of the material of a metallic wire", seconds=35)

f_uv = 40 / 2
assert f_uv == 20
q(EXP, "Optics experiments", "Basic", "numerical",
  "In the u–v method for finding the focal length of a convex lens, a student finds that the image on the screen is "
  "the same size as the object when the object and its real image are each 40.0 cm from the lens. The focal length "
  "of the lens is:",
  *opt("20.0 cm", ["40.0 cm", "80.0 cm", "10.0 cm"], "A"),
  "Lens formula 1/v − 1/u = 1/f; u = v = 2f for unit magnification",
  "A real image of the same size is formed when the object is at 2f; then the image is also at 2f on the other side.",
  ["u = −40.0 cm, v = +40.0 cm", "1/f = 1/40 + 1/40 = 1/20 → f = 20.0 cm"],
  why="40.0 cm takes the object distance itself as f. 80.0 cm adds the two distances. 10.0 cm takes the distance "
      "as 4f.",
  ncert=LAB + "focal length of a convex lens by plotting graphs between u and v", seconds=30, rc=True)

# ---- Intermediate
M_scale = F(20 * (40 - 10), 50 - 40)
assert M_scale == 60
assert F(20 * 30, 40) == 15 and F(20 * 10, 30) == F(20, 3)
q(EXP, "Mechanics experiments", "Intermediate", "numerical",
  "A uniform metre scale balances on a knife edge at its 50.0 cm mark. When a 20 g mass is hung at its 10.0 cm mark, "
  "the scale balances with the knife edge at the 40.0 cm mark. The mass of the metre scale is:",
  *opt("60 g", ["15 g", "20 g", "6.7 g"], "D"),
  "Principle of moments about the knife edge; the weight of a uniform scale acts at its centre (50 cm mark)",
  "With the knife edge at 40.0 cm, the 20 g mass acts at 30.0 cm on one side and the scale's own weight acts at "
  "10.0 cm on the other side.",
  ["20 × (40 − 10) = M × (50 − 40)", "600 = 10M → M = 60 g"],
  why="15 g takes the lever arm of the scale's weight as 40 cm (measured from the zero end). 20 g assumes equal "
      "lever arms. 6.7 g inverts the ratio of the lever arms.",
  ncert=LAB + "mass of a given object using a metre scale by the principle of moments", seconds=50, rc=True)

R_cm = 50 - 30
assert R_cm == 20 and R_cm / 2 == 10
q(EXP, "Optics experiments", "Intermediate", "numerical",
  "To find the focal length of a convex mirror, a convex lens first forms a real image of an object needle 50.0 cm "
  "from the lens. The convex mirror is then placed between the lens and this image, 30.0 cm from the lens and facing "
  "it, and is adjusted until the image of the needle formed by the light reflected back through the lens coincides "
  "with the needle itself. The focal length of the convex mirror is:",
  *opt("10.0 cm", ["20.0 cm", "25.0 cm", "40.0 cm"], "C"),
  "Light retraces its path when it falls normally on the mirror, i.e. when it is directed towards the centre of "
  "curvature",
  "The image coincides with the object only if the rays return along their own paths. The rays converging towards the "
  "lens's image point must then strike the mirror normally, so that point is the mirror's centre of curvature.",
  ["Radius of curvature = 50.0 − 30.0 = 20.0 cm", "f = R/2 = 10.0 cm"],
  why="20.0 cm is the radius of curvature, not the focal length. 25.0 cm halves the image distance from the lens. "
      "40.0 cm doubles the radius instead of halving it.",
  ncert=LAB + "focal length of a convex mirror using a convex lens", seconds=70, rc=True)

q(EXP, "Electrical experiments", "Intermediate", "assertion_reason",
  ar("In the metre bridge experiment, the jockey should be pressed gently on the wire to find the null point, and "
     "should not be slid along the wire while it is pressed.",
     "Sliding the jockey under pressure scrapes the wire and makes its cross-section non-uniform, so its resistance "
     "per unit length no longer stays the same along its length."),
  AR, ar_key(True, True, True),
  "Metre bridge: the balance condition assumes a wire of uniform resistance per unit length",
  "The unknown resistance is found from the ratio of the balancing lengths, which is valid only if equal lengths of "
  "the wire have equal resistances. Scraping the wire by sliding the pressed jockey spoils this uniformity, which "
  "is why the jockey is only touched gently at different points. R gives the reason.",
  ["X/R = l/(100 − l) assumes uniform resistance per unit length",
   "Scraping → non-uniform cross-section → this assumption fails", "R explains A"],
  why="Both statements are true and the damage done to the uniformity of the wire is exactly why the precaution is "
      "taken.",
  ncert=LAB + "resistivity of the material of a given wire using a metre bridge", seconds=40)

# ---- Advanced
A_pr, i1, d1 = 60, 40, 40
e1 = A_pr + d1 - i1
assert e1 == 60
lo_n, hi_n = 1.2, 2.0
for _ in range(80):
    mid = (lo_n + hi_n) / 2
    s = deg(math.asin(math.sin(rad(i1)) / mid)) + deg(math.asin(math.sin(rad(e1)) / mid))
    lo_n, hi_n = (lo_n, mid) if s < A_pr else (mid, hi_n)
n_e = (lo_n + hi_n) / 2
assert 1.4 < n_e < 1.6 and 2 * deg(math.asin(n_e * math.sin(rad(A_pr / 2)))) - A_pr < d1
q(EXP, "Optics experiments", "Advanced", "numerical",
  "In the experiment to plot the graph of the angle of deviation (δ) against the angle of incidence (i) for a "
  "triangular glass prism of refracting angle 60°, a student finds δ = 40° at i = 40°. The other angle of incidence "
  "at which the same deviation of 40° would be obtained is:",
  *opt("60°", ["40°", "20°", "80°"], "B"),
  "δ = i + e − A, and by the reversibility of light paths, i and e can be interchanged without changing δ",
  "For every deviation above the minimum there are two angles of incidence: the ray can be reversed, so the angle of "
  "emergence of one becomes the angle of incidence of the other.",
  ["e = A + δ − i = 60 + 40 − 40 = 60°", "Reversing the ray: incidence at 60° gives emergence at 40° and the same "
   "δ = 40°"],
  why="40° assumes each deviation occurs at only one angle of incidence. 20° is A − i. 80° adds i and δ.",
  ncert=LAB + "graph between angle of incidence and angle of deviation for a triangular prism", seconds=80, rc=True)

k_fm = 2.0 / ((9000 + 1000) * 20)
close(k_fm, 1.0e-5)
close(2.0 / (9000 * 20), 1.111e-5, 1e-3)
close(2.0 / (1000 * 20), 1.0e-4)
close(2.0 / (9000 + 1000), 2.0e-4)
q(EXP, "Electrical experiments", "Advanced", "numerical",
  "To find the figure of merit of a galvanometer of resistance 1.0 kΩ, it is connected in series with a 9.0 kΩ "
  "resistor across a cell of emf 2.0 V and negligible internal resistance. The deflection is 20 divisions. The "
  "figure of merit (current per division) of the galvanometer is:",
  *opt("10 µA per division", ["11.1 µA per division", "100 µA per division", "200 µA per division"], "C"),
  "Figure of merit k = I/θ, with I = E/(R + G)",
  "The current through the galvanometer is fixed by the emf and the total series resistance (resistor plus "
  "galvanometer). Dividing by the deflection gives the current per division.",
  ["I = 2.0/(9000 + 1000) = 2.0 × 10⁻⁴ A = 200 µA", "k = 200 µA/20 = 10 µA per division"],
  why="11.1 µA per division leaves out the galvanometer's own resistance. 100 µA per division uses only the "
      "galvanometer's resistance. 200 µA per division is the total current, not divided by the deflection.",
  ncert=LAB + "resistance and figure of merit of a galvanometer by the half-deflection method", seconds=60, rc=True)

q(EXP, "Thermal and fluid experiments", "Advanced", "multi_statement",
  ms("Which of the following statements about laboratory experiments on heat and on fluids are correct?",
     ["In the method of mixtures, the heated solid is transferred to the calorimeter as quickly as possible to "
      "reduce heat loss on the way.",
      "In the method of mixtures, stirring the contents of the calorimeter is unnecessary.",
      "In a clean glass capillary tube, the water meniscus is concave.",
      "The calorimeter is kept polished and placed in an insulating jacket to reduce heat exchange with the "
      "surroundings.",
      "In the capillary-rise experiment, water rises higher in a wider tube."]),
  *mso({"a": True, "b": False, "c": True, "d": True, "e": False}, "acd", ["ac", "acde", "bcd"], "D"),
  "Precautions in calorimetry; capillary rise h = 2S cos θ/(rρg)",
  "The hot solid should be transferred quickly (a true), and the mixture must be stirred so that it reaches a "
  "uniform final temperature (b false). Water wets clean glass (contact angle about 0°), so its meniscus is "
  "concave (c true). Polishing and an insulating jacket reduce radiation and conduction losses (d true). The rise "
  "is inversely proportional to the radius, so it is smaller in a wider tube (e false).",
  ["(a) true", "(b) false: stirring is needed", "(c) true", "(d) true", "(e) false: h ∝ 1/r"],
  why="Options containing (b) or (e) include a false statement; (a) and (c) only leaves out the true statement (d).",
  ncert=LAB + "specific heat capacity by the method of mixtures; surface tension by capillary rise", seconds=60)


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
    doc = {"schema_version": "1.0", "batch_id": "BATCH_006", "created_at": TODAY,
           "notes": "Package PHY_006_p2: 119 original Physics questions (Current Electricity to Experimental Skills), "
                    "NEET_PHY_001382..001500. Numerical answers recomputed by tools/batch_006/PHY_006_p2.py.",
           "stimuli": [], "questions": QS}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {OUT}: {len(QS)} questions")
    print("difficulty", dict(Counter(x["difficulty"] for x in QS)))
    print("formats", dict(fmts))
    print("keys", dict(sorted(keys.items())))


if __name__ == "__main__":
    main()
