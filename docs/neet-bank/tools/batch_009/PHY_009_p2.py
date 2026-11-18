"""Builder for batches/parts/BATCH_009_PHY_p2.json (package PHY_009_p2 of BATCH_009).

Physics, 133 original questions, NEET_PHY_002118..NEET_PHY_002250: Electrostatics, Current Electricity, Magnetic
Effects of Current and Magnetism, Electromagnetic Induction and Alternating Currents, Electromagnetic Waves, Optics,
Dual Nature of Matter and Radiation, Atoms and Nuclei, Electronic Devices, Experimental Skills.

Every numerical answer is recomputed below with an assert next to its question; multi-statement, assertion-reason
and statement-pair keys are derived from truth tables; the plan quota, format mix and answer-key balance are
asserted before anything is written. If any assert fails, nothing is written.

    python tools/batch_009/PHY_009_p2.py        (run from docs/neet-bank)
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
PLAN = ROOT / "batches" / "plans" / "BATCH_009_plan.json"
OUT = ROOT / "batches" / "parts" / "BATCH_009_PHY_p2.json"
PACKAGE = "PHY_009_p2"
FIRST_ID = 2118
COUNT = 133

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
rad, deg = math.radians, math.degrees

NC = "Class 12 Physics, "
rad, deg = math.radians, math.degrees
K9 = 9e9

# ================================================================ Electrostatics (B5 I7 A5)
ESC = NC + "'Electric Charges and Fields', "
ESP = NC + "'Electrostatic Potential and Capacitance', "

# ---- Basic
C_ = F(240, 60)
assert C_ == 4 and C_ * 90 == 360 and F(240 * 60, 90) == 160 and F(240) * F(90, 60) ** 2 == 540
q(ES, "Capacitors and dielectrics", "Basic", "numerical",
  "A capacitor holds a charge of 240 μC when a potential difference of 60 V is applied across it. If the potential "
  "difference is raised to 90 V, the charge it holds becomes:",
  *opt("360 μC", ["160 μC", "240 μC", "540 μC"], "A"),
  "Capacitance C = Q/V is fixed by the geometry and the medium, so Q is proportional to V",
  "The capacitance found from the first reading stays the same when the voltage changes; only the charge changes.",
  ["C = 240 μC / 60 V = 4 μF", "New charge Q = CV = 4 μF × 90 V = 360 μC"],
  shortcut="Q ∝ V: Q = 240 × 90/60 = 360 μC.",
  why="160 μC scales the charge by 60/90 instead of 90/60. 240 μC assumes the charge stays fixed. 540 μC scales the "
      "charge with V², which is how the stored energy (not the charge) changes.",
  ncert=ESP + "capacitors and capacitance", seconds=30, rc=True)

n_ = 10
assert F(n_) / F(1, n_) == 100
q(ES, "Capacitors and dielectrics", "Basic", "numerical",
  "Ten identical capacitors are first connected all in parallel and then all in series. The ratio of the equivalent "
  "capacitance of the parallel combination to that of the series combination is:",
  *opt("100", ["1/100", "10", "1"], "B"),
  "Parallel: C_p = sum of capacitances; series: 1/C_s = sum of reciprocals",
  "For n identical capacitors C, the parallel combination is nC and the series combination is C/n.",
  ["C_p = 10C", "C_s = C/10", "C_p/C_s = 10C ÷ (C/10) = 100"],
  shortcut="For n identical capacitors the ratio is n².",
  why="1/100 is the series-to-parallel ratio, inverted. 10 compares only one of the combinations with a single "
      "capacitor. 1 assumes the arrangement does not matter.",
  ncert=ESP + "combination of capacitors", seconds=30, rc=True)

q(ES, "Gauss's law", "Basic", "direct",
  "A student applies Gauss's law to a system of discrete point charges. Which of the following is a correct "
  "guideline for choosing the Gaussian surface?",
  *opt("It must not pass through any of the discrete point charges",
       ["It must be a sphere centred on one of the charges",
        "It must be the surface of a real conductor",
        "It must enclose all the charges, because charges outside change the total flux through it"], "C"),
  "Gauss's law and the Gaussian surface",
  "Any closed surface may be used as a Gaussian surface, of any shape or size, real or imaginary. The one caution "
  "NCERT gives is that the surface should not pass through a discrete charge, because the electric field of a system "
  "of point charges is not well defined at the location of a charge.",
  ["Gaussian surface: any closed surface", "Field undefined at a point charge → surface must not pass through one"],
  why="The sphere is only a convenient choice when there is spherical symmetry; Gauss's law holds for any shape. The "
      "surface may be imaginary. Charges outside the surface contribute zero total flux (they change the field on the "
      "surface, but not the net flux).",
  ncert=ESC + "Gauss's law", seconds=35)

q(ES, "Electric field and dipole", "Basic", "assertion_reason",
  ar("To find the electric field produced by a source charge, the force is measured on a test charge that is made "
     "vanishingly small.",
     "A test charge that is not small could push or pull the source charges and disturb their arrangement, so the "
     "field measured would not be the field of the original arrangement."),
  AR, ar_key(True, True, True),
  "Definition of the electric field using a test charge",
  "The field at a point is E = F/q for a test charge q placed there. If q were large, the force it exerts on the "
  "source charges could move them (or, on a conductor, redistribute them), so the field being measured would be "
  "changed by the act of measuring it. Making q negligibly small avoids this. R is exactly why A is done.",
  ["A: test charge made vanishingly small → true", "R: a large test charge disturbs the source arrangement → true",
   "R gives the reason for A"],
  why="R is not an unrelated fact: it is the very reason the test charge must be small, so the 'NOT the correct "
      "explanation' option fails.",
  ncert=ESC + "electric field", seconds=40)

W_ = 1.6e-19 * (70 - 20)
close(W_, 8.0e-18)
close(1.6e-19 * 90, 1.44e-17)
q(ES, "Electric potential and energy", "Basic", "numerical",
  "An electron moves from a point where the electrostatic potential is 20 V to a point where it is 70 V. Taking "
  "e = 1.6 × 10⁻¹⁹ C, the work done on the electron by the electric field is:",
  *opt("+8.0 × 10⁻¹⁸ J", ["−8.0 × 10⁻¹⁸ J", "+1.12 × 10⁻¹⁷ J", "+1.44 × 10⁻¹⁷ J"], "D"),
  "Work done by the field = −(change in potential energy) = −q(V_final − V_initial)",
  "The potential energy of a charge q at potential V is qV. For the electron q = −e, so moving to a higher potential "
  "lowers its potential energy, and the field does positive work on it.",
  ["ΔU = q ΔV = (−1.6 × 10⁻¹⁹ C)(70 V − 20 V) = −8.0 × 10⁻¹⁸ J",
   "Work by the field = −ΔU = +8.0 × 10⁻¹⁸ J"],
  shortcut="A negative charge moving towards higher potential gains kinetic energy: |W| = e × 50 V = 50 eV, positive.",
  why="−8.0 × 10⁻¹⁸ J treats the electron as a positive charge (or gives the work of an external agent). "
      "+1.12 × 10⁻¹⁷ J uses the final potential (70 V) alone. +1.44 × 10⁻¹⁷ J adds the two potentials instead of "
      "taking their difference.",
  ncert=ESP + "potential energy of a charge in an external field", seconds=40, rc=True)

# ---- Intermediate
E_hex = K9 * 2e-6 / 0.3 ** 2
close(E_hex, 2e5)
close(5 * E_hex, 1e6)
q(ES, "Coulomb's law and superposition", "Intermediate", "numerical",
  "Point charges, each of +2 μC, are placed at five of the six corners of a regular hexagon of side 30 cm, in air; "
  "the sixth corner is empty. Taking 1/(4πε₀) = 9 × 10⁹ N m² C⁻², the electric field at the centre of the hexagon "
  "is:",
  *opt("2 × 10⁵ N/C, directed towards the empty corner",
       ["2 × 10⁵ N/C, directed away from the empty corner", "1 × 10⁶ N/C, directed towards the empty corner",
        "zero"], "A"),
  "Superposition principle; symmetry",
  "If all six corners carried +2 μC, the fields at the centre would cancel in pairs (opposite corners). So the field "
  "of the five charges equals minus the field that the missing sixth charge would produce. A +2 μC charge at the "
  "empty corner would give a field at the centre pointing away from that corner; the actual field therefore points "
  "towards the empty corner. In a regular hexagon each corner is at a distance equal to the side from the centre.",
  ["Distance of each corner from the centre = side = 0.30 m",
   "Field of one charge there = 9 × 10⁹ × 2 × 10⁻⁶ / 0.09 = 2 × 10⁵ N/C",
   "Five charges = six charges (zero) − one charge → 2 × 10⁵ N/C towards the empty corner"],
  shortcut="Field of the gap = field of a −2 μC charge placed at the empty corner.",
  why="'Away from the empty corner' gets the magnitude right but reverses the direction. 1 × 10⁶ N/C adds the five "
      "magnitudes as if all the fields were parallel. Zero assumes the five charges are still symmetric.",
  seconds=75, rc=True)

kk, e_, G_, mp = 9e9, 1.6e-19, 6.67e-11, 1.67e-27
ratio = kk * e_ ** 2 / (G_ * mp ** 2)
close(ratio, 1.24e36, 1e-2)
close(kk * e_ ** 2 / (G_ * mp), 2.07e9, 1e-2)
close(1 / ratio, 8.07e-37, 1e-2)
q(ES, "Coulomb's law and superposition", "Intermediate", "numerical",
  "Two protons are a distance r apart in vacuum. Taking 1/(4πε₀) = 9 × 10⁹ N m² C⁻², G = 6.67 × 10⁻¹¹ N m² kg⁻², "
  "e = 1.6 × 10⁻¹⁹ C and the proton mass as 1.67 × 10⁻²⁷ kg, the ratio of the electrostatic force between them to "
  "the gravitational force between them is about:",
  *opt("1.2 × 10³⁶, whatever the value of r",
       ["8.1 × 10⁻³⁷, whatever the value of r", "2.1 × 10⁹, whatever the value of r",
        "1.2 × 10³⁶ at r = 1 m, and larger at smaller r"], "C"),
  "Coulomb's law and Newton's law of gravitation are both inverse-square laws",
  "Both forces vary as 1/r², so r cancels in the ratio: F_e/F_G = ke²/(Gm²).",
  ["ke² = 9 × 10⁹ × (1.6 × 10⁻¹⁹)² = 2.30 × 10⁻²⁸ N m²",
   "Gm² = 6.67 × 10⁻¹¹ × (1.67 × 10⁻²⁷)² = 1.86 × 10⁻⁶⁴ N m²",
   "Ratio = 2.30 × 10⁻²⁸ / 1.86 × 10⁻⁶⁴ ≈ 1.2 × 10³⁶"],
  why="8.1 × 10⁻³⁷ is the gravitational-to-electrostatic ratio. 2.1 × 10⁹ forgets to square the mass. The last "
      "option wrongly makes the ratio depend on r, although both forces fall off as 1/r².",
  ncert=ESC + "Coulomb's law", seconds=75, rc=True)

Qf, Kd = F(40), 5
Qp = Qf * (1 - F(1, Kd))
assert Qp == 32 and Qf / Kd == 8
q(ES, "Capacitors and dielectrics", "Intermediate", "numerical",
  "An isolated parallel plate capacitor carries charges +40 μC and −40 μC on its plates. A slab of dielectric "
  "constant 5 is slid in so that it completely fills the space between the plates. The magnitude of the charge "
  "induced (by polarisation) on each face of the slab is:",
  *opt("32 μC", ["8 μC", "200 μC", "40 μC"], "D"),
  "Polarisation of a dielectric: induced surface charge reduces the field to E₀/K",
  "The free charge Q on the plates stays 40 μC (the capacitor is isolated). The face of the slab next to the "
  "positive plate acquires a charge −Q_p and the other face +Q_p. The field inside the slab is due to the net "
  "charge Q − Q_p, and it must be 1/K of the field without the slab.",
  ["(Q − Q_p) = Q/K", "Q_p = Q(1 − 1/K) = 40 × (1 − 1/5)", "Q_p = 32 μC"],
  why="8 μC is Q/K, the net (free minus induced) charge, not the induced charge. 200 μC multiplies by K; the induced "
      "charge can never exceed the free charge. 40 μC would cancel the field inside completely, which happens in a "
      "conductor, not a dielectric.",
  ncert=ESP + "dielectrics and polarisation", seconds=60, rc=True)

Cc, Vv = 20e-12, 100
Ui = 0.5 * Cc * Vv ** 2
Uf = (Cc * Vv) ** 2 / (2 * (Cc / 2))
close(Ui, 1e-7)
close(Uf - Ui, 1e-7)
close(Uf, 2e-7)
q(ES, "Capacitors and dielectrics", "Intermediate", "numerical",
  "A 20 pF parallel plate capacitor with air between its plates is charged to 100 V and then disconnected from the "
  "battery. Its plates are now slowly pulled apart until their separation is doubled. The work done by the agent "
  "pulling the plates apart is:",
  *opt("1 × 10⁻⁷ J", ["2 × 10⁻⁷ J", "−5 × 10⁻⁸ J", "zero"], "B"),
  "With the battery disconnected the charge stays constant; U = Q²/(2C)",
  "Doubling the separation halves the capacitance. With Q fixed, the stored energy Q²/(2C) doubles. The plates "
  "attract each other, so the agent does positive work, equal to the increase in stored energy.",
  ["Initial energy U = ½CV² = ½ × 20 × 10⁻¹² × 100² = 1 × 10⁻⁷ J",
   "C → C/2 with Q fixed → U → 2U = 2 × 10⁻⁷ J", "Work done = 2 × 10⁻⁷ − 1 × 10⁻⁷ = 1 × 10⁻⁷ J"],
  why="2 × 10⁻⁷ J is the final stored energy, not the increase. −5 × 10⁻⁸ J treats the voltage as fixed (as if the "
      "battery stayed connected), which would halve the energy. The work is not zero: the attracting plates must be "
      "pulled apart.",
  ncert=ESP + "energy stored in a capacitor", seconds=75, rc=True)

q(ES, "Electric potential and energy", "Intermediate", "match_list",
  ml("Match List-I (physical quantity) with List-II (its dimensional formula). A stands for the dimension of "
     "electric current.",
     ["Electric field", "Electric potential", "Capacitance", "Permittivity of free space, ε₀"],
     ["[M⁻¹ L⁻³ T⁴ A²]", "[M L T⁻³ A⁻¹]", "[M⁻¹ L⁻² T⁴ A²]", "[M L² T⁻³ A⁻¹]"]),
  *mlo("A-II, B-IV, C-III, D-I", ["A-IV, B-II, C-III, D-I", "A-II, B-IV, C-I, D-III", "A-IV, B-II, C-I, D-III"], "C"),
  "Dimensions from defining relations: E = F/q, V = W/q, C = Q/V, ε₀ = C d/A",
  "Charge has dimensions [A T]. E = F/q = [M L T⁻²]/[A T] = [M L T⁻³ A⁻¹]. V = W/q = [M L² T⁻²]/[A T] = "
  "[M L² T⁻³ A⁻¹]. C = Q/V = [A T]/[M L² T⁻³ A⁻¹] = [M⁻¹ L⁻² T⁴ A²]. ε₀ = Cd/A has one more L⁻¹ than C: "
  "[M⁻¹ L⁻³ T⁴ A²] (its unit is F/m).",
  ["E → II", "V → IV", "C → III", "ε₀ → I"],
  why="Swapping E and V confuses N/C with J/C (they differ by one power of length). Swapping C and ε₀ forgets that "
      "ε₀ is capacitance per unit length (F/m).",
  seconds=60)

q(ES, "Gauss's law", "Intermediate", "statement_pair",
  sp("Two large, thin, parallel plane sheets carry the same uniform surface charge density +σ. In the region "
     "between the sheets (away from the edges), the electric field is zero.",
     "For the same two sheets, the electric field in the region outside them (away from the edges) has magnitude "
     "σ/(2ε₀)."),
  SP, sp_key(True, False),
  "Field of a large plane sheet, σ/(2ε₀), and superposition",
  "Each sheet produces a field of magnitude σ/(2ε₀) directed away from it on both sides. Between the sheets the two "
  "fields are opposite and cancel, so Statement I is true. Outside, both fields point the same way and add to "
  "σ/ε₀, so Statement II is false.",
  ["Between: σ/(2ε₀) − σ/(2ε₀) = 0 → I true", "Outside: σ/(2ε₀) + σ/(2ε₀) = σ/ε₀ → II false"],
  why="σ/(2ε₀) is the field of a single sheet; outside two like sheets the fields add.",
  ncert=ESC + "applications of Gauss's law: field due to a uniformly charged infinite plane sheet", seconds=50)

truth = {"a": True, "b": True, "c": True, "d": False, "e": False}
q(ES, "Electric field and dipole", "Intermediate", "multi_statement",
  ms("An electric dipole of dipole moment p is placed in a non-uniform electric field E. Which of the following "
     "statements are correct?",
     ["In general, the dipole experiences both a net force and a torque.",
      "If p is parallel to E, the net force on the dipole is in the direction of increasing field.",
      "If p is antiparallel to E, the net force on the dipole is in the direction of decreasing field.",
      "If p is parallel to E, the torque on the dipole is maximum.",
      "If p is antiparallel to E, the torque on the dipole is maximum."]),
  *mso(truth, "abc", ["abd", "bce", "ad"], "B"),
  "Dipole in a non-uniform field: torque p × E and a net force that depends on how E varies",
  "In a non-uniform field the forces qE on the two charges are unequal, so there is in general a net force as well "
  "as a torque. With p parallel to E the dipole is pulled towards the stronger field; with p antiparallel it is "
  "pushed towards the weaker field (NCERT states both). The torque p × E has magnitude pE sin θ, which is zero (not "
  "maximum) when p is parallel or antiparallel to E.",
  ["(a) true", "(b) true", "(c) true", "(d) false: sin 0° = 0, torque zero", "(e) false: sin 180° = 0, torque zero"],
  why="Any option containing (d) or (e) treats the aligned positions as positions of maximum torque; the torque is "
      "maximum when p is perpendicular to E.",
  ncert=ESC + "dipole in a uniform external field", seconds=70)

# ---- Advanced
Q_end = F(8)
q_mid = -Q_end / 4
assert Q_end * Q_end / 4 + Q_end * q_mid == 0 and q_mid == -2
q(ES, "Coulomb's law and superposition", "Advanced", "numerical",
  "Two point charges, each of +8 μC, are fixed at x = 0 and x = 2a on the x-axis. A third point charge q is placed "
  "at x = a. For all three charges to be in equilibrium under their mutual electrostatic forces alone, q must be:",
  *opt("−2 μC", ["+2 μC", "−8 μC", "−4 μC"], "D"),
  "Equilibrium of a system of charges: net Coulomb force on each charge zero",
  "The middle charge is in equilibrium for any q, by symmetry. For the charge at x = 0, the repulsion from the "
  "other +8 μC charge (distance 2a) must be balanced by an attraction towards the middle charge (distance a), so q "
  "must be negative.",
  ["Force on the end charge from the other end: k(8)(8)/(2a)² = 16k/a² (away)",
   "Force from q: k(8)|q|/a² (towards q, if q is negative)", "8|q| = 16 → |q| = 2 μC, negative"],
  shortcut="q = −Q/4 for equal charges Q at the ends.",
  why="+2 μC has the right size but would repel the end charges. −8 μC ignores that the middle charge is at half "
      "the distance. −4 μC uses distances a and 2a without squaring them.",
  ncert=ESC + "forces between multiple charges", seconds=75, rc=True)

r1, r2, Qt = F(1, 10), F(2, 10), F(5)
Q1 = Qt * r1 ** 2 / (r1 ** 2 + r2 ** 2)
Q2 = Qt - Q1
assert Q1 == 1 and Q2 == 4 and Q1 / (4 * r1 ** 2) == Q2 / (4 * r2 ** 2)
Vc = 9 * (Q1 / r1 + Q2 / r2)       # k × 1e-9 = 9
assert Vc == 270 and 9 * Qt / r1 == 450 and 9 * (4 / r1 + 1 / r2) == 405 and 9 * Qt / r2 == 225
q(ES, "Electric potential and energy", "Advanced", "numerical",
  "A total charge of 5 nC is shared between two thin concentric conducting spherical shells of radii 10 cm and "
  "20 cm (kept insulated from each other) so that the two shells have equal surface charge densities. Taking "
  "1/(4πε₀) = 9 × 10⁹ N m² C⁻², the electric potential at the common centre is:",
  *opt("270 V", ["450 V", "405 V", "225 V"], "A"),
  "Potential due to a charged spherical shell; superposition of potentials",
  "Equal surface densities mean the charges are in the ratio of the areas, r₁² : r₂² = 1 : 4, so the shells carry "
  "1 nC and 4 nC. Inside a shell its potential is constant and equal to kQ/R, so at the centre each shell "
  "contributes kQ/R.",
  ["Q₁ : Q₂ = 10² : 20² = 1 : 4 → Q₁ = 1 nC, Q₂ = 4 nC",
   "V = k(Q₁/r₁ + Q₂/r₂) = 9 × 10⁹ × (10⁻⁹/0.1 + 4 × 10⁻⁹/0.2)", "V = 9 × (10 + 20) = 270 V"],
  why="450 V puts the whole 5 nC on the inner shell. 405 V divides the charge in the inverse ratio (4 nC on the "
      "inner shell). 225 V puts all the charge on the outer shell.",
  ncert=ESP + "potential due to a system of charges", seconds=100, rc=True)

C1, V1, Vc2 = F(5), F(200), F(40)
Ctot = C1 * V1 / Vc2
C2 = Ctot - C1
heat = F(1, 2) * C1 * V1 ** 2 - F(1, 2) * Ctot * Vc2 ** 2      # in μJ
assert C2 == 20 and heat == 80000 and F(1, 2) * Ctot * Vc2 ** 2 == 20000 and F(1, 2) * C2 * Vc2 ** 2 == 16000
assert heat == F(1, 2) * C1 * C2 / (C1 + C2) * V1 ** 2
q(ES, "Capacitors and dielectrics", "Advanced", "numerical",
  "A 5 μF capacitor charged to 200 V is disconnected from the battery and connected across an uncharged capacitor "
  "of unknown capacitance. The common potential difference across the two capacitors settles at 40 V. The energy "
  "dissipated (as heat and radiation) during the redistribution of charge is:",
  *opt("0.08 J", ["0.02 J", "0.1 J", "0.016 J"], "C"),
  "Conservation of charge when capacitors are connected; stored energy ½CV²",
  "Charge is conserved: 5 μF × 200 V = 1000 μC is shared between the two capacitors at 40 V, so the total "
  "capacitance is 25 μF and the unknown capacitor is 20 μF. The energy lost is the initial stored energy minus the "
  "final stored energy.",
  ["Q = 5 μF × 200 V = 1000 μC; total C = 1000/40 = 25 μF → unknown C = 20 μF",
   "Initial energy = ½ × 5 × 10⁻⁶ × 200² = 0.1 J", "Final energy = ½ × 25 × 10⁻⁶ × 40² = 0.02 J",
   "Energy dissipated = 0.1 − 0.02 = 0.08 J"],
  shortcut="Loss = ½ [C₁C₂/(C₁ + C₂)] V₁² = ½ × 4 μF × (200 V)² = 0.08 J.",
  why="0.02 J is the energy finally stored. 0.1 J is the energy initially stored. 0.016 J is the energy finally "
      "stored in the 20 μF capacitor alone.",
  ncert=ESP + "energy stored in a capacitor", seconds=110, rc=True)

q(ES, "Capacitors and dielectrics", "Advanced", "assertion_reason",
  ar("When a dielectric slab that completely fills the space between the plates is inserted into an air-filled "
     "parallel plate capacitor that remains connected to a battery, the electric field between the plates does not "
     "change.",
     "With the battery connected, the potential difference V between the plates and the plate separation d both "
     "stay the same, and the uniform field between the plates is E = V/d."),
  AR, ar_key(True, True, True),
  "Capacitor with a dielectric: which quantity is held fixed",
  "The familiar result that a dielectric reduces the field to E₀/K applies when the charge is fixed (isolated "
  "capacitor). With the battery connected, V is fixed; the field in the filled gap is V/d, so it cannot change. The "
  "battery supplies extra charge (K times the original) so that the field of the free charges, reduced by the "
  "polarisation charges, is again V/d. R states exactly why A holds.",
  ["A: V fixed, d fixed → E = V/d unchanged → true", "R: true, and it is the reason for A"],
  why="Students who apply E₀/K regardless of the battery would mark A false; that rule needs the charge to be "
      "fixed. R is not an unrelated fact; it is the derivation of A.",
  ncert=ESP + "effect of dielectric on capacitance", seconds=60)

Cb = F(50, 10 ** 6)
Wb = Cb * (12 - 4) * 12
dU = F(1, 2) * Cb * (12 ** 2 - 4 ** 2)
assert Wb == F(48, 10 ** 4) and dU == F(32, 10 ** 4) and Wb - dU == F(16, 10 ** 4) == F(1, 2) * Cb * 8 ** 2
q(ES, "Capacitors and dielectrics", "Advanced", "numerical",
  "A 50 μF capacitor already charged to 4 V is connected, through a resistor and with like terminals joined, to a "
  "12 V battery of negligible internal resistance, and is left until it is fully charged to 12 V. The heat produced "
  "in the resistor during this process is:",
  *opt("1.6 mJ", ["3.2 mJ", "4.8 mJ", "2.4 mJ"], "B"),
  "Energy balance in charging: work done by the battery = increase in stored energy + heat",
  "The battery moves the extra charge ΔQ = C(12 − 4) through its emf of 12 V, so it does work ΔQ × 12 V. Only part of "
  "this goes into the capacitor's stored energy; the rest is dissipated in the resistor.",
  ["ΔQ = 50 μF × 8 V = 400 μC; battery work = 400 μC × 12 V = 4.8 mJ",
   "Increase in stored energy = ½ × 50 μF × (12² − 4²) V² = 3.2 mJ", "Heat = 4.8 − 3.2 = 1.6 mJ"],
  shortcut="Heat = ½C(ΔV)² = ½ × 50 μF × 8² = 1.6 mJ when a battery tops up a capacitor through a resistor.",
  why="3.2 mJ is the increase in stored energy. 4.8 mJ is the work done by the battery. 2.4 mJ assumes that half of "
      "the battery's work always becomes heat, which is true only when the capacitor starts uncharged.",
  ncert=ESP + "energy stored in a capacitor", seconds=110, rc=True)


# ================================================================ Current Electricity (B5 I7 A5)
CEC = NC + "'Current Electricity', "

# ---- Basic
R_b = F(220 ** 2, 100)
assert R_b == 484 and F(220, 100) == F(22, 10) and 220 * 100 == 22000 and round(100 / 220, 2) == 0.45
q(CE, "Drift velocity and Ohm's law", "Basic", "numerical",
  "An electric bulb is rated 100 W, 220 V. Treating its resistance as constant, the resistance of its filament when "
  "it is working at its rated voltage is:",
  *opt("484 Ω", ["2.2 Ω", "0.45 Ω", "22 kΩ"], "C"),
  "Electrical power P = V²/R",
  "At its rated voltage the bulb draws its rated power, so R = V²/P.",
  ["R = V²/P = (220 V)² / 100 W", "R = 48400/100 = 484 Ω"],
  why="2.2 Ω is V/P, which has no physical meaning here. 0.45 is P/V, the current in amperes, not a resistance. "
      "22 kΩ multiplies V by P.",
  ncert=CEC + "electrical energy, power", seconds=30, rc=True)

I_tot = F(6)
I4 = I_tot * 2 / (2 + 4)
assert I4 == 2 and I_tot * 4 / 6 == 4 and I_tot / 2 == 3
q(CE, "Combination of resistors", "Basic", "numerical",
  "A current of 6 A enters a parallel combination of a 2 Ω resistor and a 4 Ω resistor. The current through the "
  "4 Ω resistor is:",
  *opt("2 A", ["4 A", "3 A", "6 A"], "A"),
  "In a parallel combination the potential difference is the same, so the current divides in inverse proportion to "
  "the resistances",
  "The equivalent resistance is 2 × 4/(2 + 4) = 4/3 Ω, so the common potential difference is 6 A × 4/3 Ω = 8 V.",
  ["Common PD = 6 × (4/3) = 8 V", "Current in 4 Ω = 8/4 = 2 A (and 4 A in the 2 Ω resistor)"],
  shortcut="I₄ = I × R₂/(R₂ + R₄) = 6 × 2/6 = 2 A.",
  why="4 A is the current in the 2 Ω resistor (the larger share goes through the smaller resistance). 3 A assumes "
      "an equal split. 6 A treats the resistors as if they were in series.",
  ncert=CEC + "combination of resistors - series and parallel", seconds=30, rc=True)

assert F(2) / F(1, 2) == 4
q(CE, "Drift velocity and Ohm's law", "Basic", "numerical",
  "The current through a metal wire is doubled, and at the same time the wire is replaced by another wire of the "
  "same metal (at the same temperature) with half the cross-sectional area. The drift speed of the free electrons "
  "becomes:",
  *opt("4 times the original value", ["2 times the original value", "the same as before", "1/4 of the original value"],
       "D"),
  "I = n e A v_d, so v_d = I/(n e A)",
  "The number density n of free electrons is a property of the metal and does not change. The drift speed is "
  "proportional to I and inversely proportional to A.",
  ["v_d ∝ I/A", "New v_d ∝ (2I)/(A/2) = 4 × (I/A)"],
  why="'2 times' accounts for the doubled current but not the smaller area. 'The same' assumes the two changes "
      "cancel. '1/4' inverts the dependence on both I and A.",
  ncert=CEC + "drift of electrons and the origin of resistivity", seconds=30, rc=True)

q(CE, "Drift velocity and Ohm's law", "Basic", "assertion_reason",
  ar("Although the drift speed of the free electrons in a copper wire is only of the order of 1 mm/s, a wire of "
     "cross-sectional area 1 mm² can carry a current of several amperes.",
     "The number density of free electrons in a metal such as copper is very large, of the order of 10²⁸ to 10²⁹ "
     "per cubic metre."),
  AR, ar_key(True, True, True),
  "Current in terms of drift speed: I = n e A v_d",
  "The current through a cross-section is the charge carried across it per second, n e A v_d. With n ≈ 8.5 × 10²⁸ "
  "m⁻³, e = 1.6 × 10⁻¹⁹ C, A = 10⁻⁶ m² and v_d = 10⁻³ m/s, I ≈ 14 A. A tiny drift speed still gives a sizeable "
  "current only because n is enormous, so R explains A.",
  ["A: true", "R: true", "I = n e A v_d: small v_d is compensated by very large n → R explains A"],
  why="R is not a separate property: the large n is exactly what makes the current large in spite of the small "
      "drift speed.",
  ncert=CEC + "drift of electrons and the origin of resistivity", seconds=40)

q(CE, "Resistivity and temperature", "Basic", "statement_pair",
  sp("The resistivity of a metal wire at a given temperature increases if the wire is made longer.",
     "The SI unit of conductance, the reciprocal of resistance, is the siemens (S), with 1 S = 1 Ω⁻¹."),
  SP, sp_key(False, True),
  "Resistance depends on dimensions; resistivity is a property of the material",
  "R = ρl/A depends on the length and area, but ρ depends only on the material and its temperature, so Statement I "
  "is false. Conductance G = 1/R is measured in siemens, 1 S = 1 Ω⁻¹, so Statement II is true.",
  ["I: a longer wire has more resistance, not more resistivity → false", "II: G = 1/R, unit S = Ω⁻¹ → true"],
  why="Statement I confuses resistance with resistivity.",
  ncert=CEC + "Ohm's law; resistivity", seconds=35)

# ---- Intermediate
assert F(3, 1) / F(1, 3) == 9
q(CE, "Combination of resistors", "Intermediate", "numerical",
  "Three identical bulbs, connected in series across a supply of constant voltage, together consume a power P. "
  "Treating the resistance of each bulb as constant, the total power they consume when they are connected in "
  "parallel across the same supply is:",
  *opt("9P", ["3P", "P/9", "P"], "B"),
  "For a fixed supply voltage, total power = V²/R_eq",
  "In series the equivalent resistance is 3R; in parallel it is R/3, which is 9 times smaller. With V fixed, power is "
  "inversely proportional to the equivalent resistance.",
  ["Series: P = V²/(3R)", "Parallel: P' = V²/(R/3) = 3V²/R", "P'/P = 9 → P' = 9P"],
  why="3P compares the parallel combination with a single bulb's resistance R. P/9 inverts the ratio. P assumes the "
      "arrangement does not matter.",
  ncert=CEC + "electrical energy, power", seconds=45, rc=True)

R_side = F(18, 3)
R_path = R_side + R_side / 2
assert R_path == 9 and R_path / 2 == F(9, 2) and R_side * 2 * R_side / (3 * R_side) == 4
q(CE, "Combination of resistors", "Intermediate", "numerical",
  "A uniform wire of resistance 18 Ω is bent into the shape of an equilateral triangle ABC, its ends being joined. "
  "The resistance between the corner A and the midpoint M of the opposite side BC is:",
  *opt("4.5 Ω", ["9 Ω", "4 Ω", "6 Ω"], "D"),
  "Resistance proportional to length; parallel combination",
  "Each side is 6 Ω, and half a side is 3 Ω. From A to M there are two identical paths: A → B → M and A → C → M, each "
  "of 6 + 3 = 9 Ω. These two paths are in parallel.",
  ["Each side 6 Ω; BM = MC = 3 Ω", "Each path A→B→M or A→C→M = 9 Ω", "Two 9 Ω paths in parallel = 4.5 Ω"],
  why="9 Ω takes only one of the two paths. 4 Ω is the resistance between two corners (6 Ω in parallel with 12 Ω). "
      "6 Ω is just the resistance of one side.",
  ncert=CEC + "combination of resistors - series and parallel", seconds=60, rc=True)

lx, ly = F(1), F(2)
assert (lx ** 2) / (ly ** 2) == F(1, 4) and lx / ly == F(1, 2)
q(CE, "Resistivity and temperature", "Intermediate", "numerical",
  "Two wires X and Y are made of the same metal and have the same mass. The length of Y is twice that of X. The two "
  "wires are connected in series across a battery. The ratio of the heat produced per second in X to that in Y is:",
  *opt("1 : 4", ["1 : 2", "4 : 1", "1 : 8"], "B"),
  "R = ρl/A, with equal mass (equal volume) fixing A = volume/l; in series, heat ∝ R",
  "Same metal and same mass means the same volume V. The cross-sectional area is A = V/l, so R = ρl/A = ρl²/V, "
  "i.e. R ∝ l². In series the same current flows through both, so the heat per second I²R is proportional to R.",
  ["R ∝ l² at fixed volume", "R_X : R_Y = 1² : 2² = 1 : 4", "Series: heat ∝ R → 1 : 4"],
  why="1 : 2 uses R ∝ l and forgets that the longer wire is also thinner. 4 : 1 is the ratio for a parallel "
      "connection, where heat ∝ 1/R. 1 : 8 cubes the length ratio.",
  ncert=CEC + "resistivity of various materials; electrical energy, power", seconds=60, rc=True)

eps, r_ = 6, 1
assert eps - 0 == 6 and eps - eps / (r_ + 2) * r_ == 4 and eps + 2 * r_ == 8
q(CE, "Cells, emf and internal resistance", "Intermediate", "match_list",
  ml("A cell has emf 6 V and internal resistance 1 Ω. Match each situation in List-I with the potential difference "
     "between the terminals of the cell in List-II.",
     ["No current is drawn from the cell (open circuit)",
      "The terminals are joined directly by a thick wire of negligible resistance",
      "A 2 Ω resistor is connected across the terminals",
      "The cell is being charged by an external source, the charging current being 2 A"],
     ["8 V", "0 V", "6 V", "4 V"]),
  *mlo("A-III, B-II, C-IV, D-I", ["A-III, B-IV, C-II, D-I", "A-I, B-II, C-IV, D-III", "A-III, B-II, C-I, D-IV"], "B"),
  "Terminal potential difference V = ε − Ir while discharging and V = ε + Ir while charging",
  "Open circuit: no current, so V = ε = 6 V. Short circuit: the terminals are at the same potential, V = 0 (the "
  "current ε/r = 6 A makes Ir = ε). With 2 Ω: I = 6/3 = 2 A and V = 6 − 2 × 1 = 4 V. While charging, the current "
  "enters the positive terminal and V = ε + Ir = 6 + 2 = 8 V.",
  ["A → 6 V (III)", "B → 0 V (II)", "C → 4 V (IV)", "D → 8 V (I)"],
  why="The other codes either give the charging case ε − Ir (4 V), or give the short-circuited cell its emf, "
      "although its terminals are joined by a wire of negligible resistance.",
  ncert=CEC + "cells, emf, internal resistance", seconds=60)

I_ = F(1)
P4, P6, P12 = 4 * I_ ** 2, 6 * (I_ * 12 / 18) ** 2, 12 * (I_ * 6 / 18) ** 2
assert P4 == 4 and P6 == F(8, 3) and P12 == F(4, 3) and max(P4, P6, P12) == P4
q(CE, "Combination of resistors", "Intermediate", "direct",
  "A 4 Ω resistor is connected in series with a parallel combination of a 6 Ω resistor and a 12 Ω resistor, and the "
  "arrangement is connected across a battery. In which resistor is heat produced at the greatest rate?",
  *opt("The 4 Ω resistor", ["The 6 Ω resistor", "The 12 Ω resistor",
                             "The 6 Ω and 12 Ω resistors equally, since they have the same potential difference"], "A"),
  "Heat produced per second = I²R; current division in a parallel combination",
  "Let the current through the 4 Ω resistor be I. It divides in inverse ratio of the resistances: 2I/3 through "
  "6 Ω and I/3 through 12 Ω. The heating rates are 4I², 6(2I/3)² = 8I²/3 and 12(I/3)² = 4I²/3.",
  ["4 Ω: 4I²", "6 Ω: 6 × 4I²/9 = 2.67 I²", "12 Ω: 12 × I²/9 = 1.33 I²", "Largest: the 4 Ω resistor"],
  why="The 6 Ω resistor gets more heat than the 12 Ω one (same V, so heat ∝ 1/R), but still less than the 4 Ω "
      "resistor, which carries the full current. The 12 Ω resistor gets the least. Equal potential difference does "
      "not mean equal heat when the resistances differ.",
  ncert=CEC + "electrical energy, power", seconds=60, rc=True)

q(CE, "Cells, emf and internal resistance", "Intermediate", "assertion_reason",
  ar("A voltmeter of very high resistance connected directly across the terminals of a cell reads very nearly the "
     "emf of the cell.",
     "Such a voltmeter draws a negligible current, so the potential drop across the internal resistance of the cell "
     "is negligible."),
  AR, ar_key(True, True, True),
  "Terminal voltage V = ε − Ir",
  "The terminal voltage differs from the emf by the drop Ir across the internal resistance. A voltmeter of very high "
  "resistance R_V draws a current ε/(R_V + r), which is tiny, so Ir is tiny and the reading is almost ε. R gives the "
  "reason for A.",
  ["V = ε − Ir", "I ≈ 0 for a very high resistance voltmeter → V ≈ ε", "R explains A"],
  why="R is the direct reason for A; it is not an unrelated statement.",
  ncert=CEC + "cells, emf, internal resistance", seconds=40)

R0, R100, Rt = F(50), F(70), F(61)
alpha = (R100 - R0) / (R0 * 100)
t_ = (Rt - R0) / (R0 * alpha)
assert alpha == F(4, 1000) and t_ == 55
assert round(float(Rt / R100 * 100)) == 87 and Rt / R0 * 100 == 122
q(CE, "Resistivity and temperature", "Intermediate", "numerical",
  "The resistance of a metal wire is 50 Ω at 0 °C and 70 Ω at 100 °C. Assuming that the resistance varies linearly "
  "with temperature, the temperature at which its resistance is 61 Ω is:",
  *opt("55 °C", ["87 °C", "122 °C", "45 °C"], "D"),
  "R_t = R₀(1 + αt) for a linear variation",
  "The resistance rises by 20 Ω over 100 °C, i.e. 0.2 Ω per °C. A rise of 11 Ω above the 0 °C value therefore needs "
  "55 °C.",
  ["α = (70 − 50)/(50 × 100) = 4 × 10⁻³ °C⁻¹", "61 = 50(1 + 4 × 10⁻³ t)", "t = 11/(50 × 4 × 10⁻³) = 55 °C"],
  shortcut="t = 100 × (61 − 50)/(70 − 50) = 55 °C.",
  why="87 °C takes R/R₁₀₀ × 100. 122 °C takes R/R₀ × 100. 45 °C measures the 11 Ω step down from 100 °C instead of "
      "up from 0 °C.",
  ncert=CEC + "temperature dependence of resistivity", seconds=50, rc=True)

# ---- Advanced
wheel = [(0, i, 5) for i in range(1, 7)] + [(i, i % 6 + 1, 5) for i in range(1, 7)]
R_opp = equivalent_resistance(7, wheel, 1, 4)
assert R_opp == 4
assert F(15, 2) == F(15 * 15, 30) and F(10 * F(15, 2), 10 + F(15, 2)) == F(30, 7)
q(CE, "Kirchhoff's laws", "Advanced", "numerical",
  "Twelve identical resistors, each of 5 Ω, form a wheel: six of them make the sides of a regular hexagon (the rim) "
  "and the other six join each corner of the hexagon to its centre O (the spokes). The equivalent resistance "
  "between two diametrically opposite corners of the hexagon is:",
  *opt("4 Ω", ["7.5 Ω", "30/7 Ω ≈ 4.3 Ω", "10 Ω"], "B"),
  "Symmetry of a network and Kirchhoff's junction rule",
  "Hold corner 1 at potential V and the opposite corner 4 at 0. By symmetry the centre O is at V/2, corners 2 and 6 "
  "(next to 1) are at a common potential x, and corners 3 and 5 are at V − x. Apply the junction rule at corner 2, "
  "which is joined to 1, to 3 and to O.",
  ["At corner 2: (V − x) + ((V − x) − x) + (V/2 − x) = 0 → x = 5V/8",
   "Current leaving corner 1 (each resistor 5 Ω): [2(V − 5V/8) + (V − V/2)]/5 = (5V/4)/5 = V/4",
   "R_eq = V ÷ (V/4) = 4 Ω"],
  why="7.5 Ω uses only the two rim paths (15 Ω each, in parallel). 30/7 Ω adds the 10 Ω spoke path through O in "
      "parallel with the rim but ignores the spokes to the other corners, which carry current. 10 Ω uses the spoke "
      "path alone.",
  seconds=150, rc=True)

X_ = F(10) * 50 / 50
Y_ = F(10) * 60 / 40
Pxy = X_ * Y_ / (X_ + Y_)
l_ = 100 * Pxy / (Pxy + 10)
assert X_ == 10 and Y_ == 15 and Pxy == 6 and l_ == F(75, 2)
assert round(float(100 * 25 / 35), 1) == 71.4
q(CE, "Wheatstone and metre bridge", "Advanced", "numerical",
  "In a metre bridge with a 10 Ω standard resistor in the right gap, the null point is 50.0 cm from the left end "
  "when a resistor X is in the left gap, and 60.0 cm from the left end when X is replaced by a resistor Y. When X and "
  "Y are connected in parallel and placed together in the left gap (10 Ω still in the right gap), the null point "
  "will be at a distance from the left end of:",
  *opt("37.5 cm", ["71.4 cm", "55.0 cm", "62.5 cm"], "C"),
  "Metre bridge balance: X/R = l/(100 − l)",
  "The two separate balances give X and Y; their parallel combination is then balanced against the same 10 Ω.",
  ["X = 10 × 50/50 = 10 Ω", "Y = 10 × 60/40 = 15 Ω", "X ∥ Y = 10 × 15/25 = 6 Ω",
   "6/10 = l/(100 − l) → l = 37.5 cm"],
  why="71.4 cm uses X and Y in series (25 Ω). 55.0 cm simply averages the two balance lengths. 62.5 cm is the "
      "correct balance length measured from the wrong (right-hand) end.",
  ncert=CEC + "Wheatstone bridge", seconds=110, rc=True)

R_wire = F(9) * 3 ** 2
piece = R_wire / 3
assert R_wire == 81 and piece == 27 and piece / 3 == 9
assert F(9, 3) / 3 == 1 and (F(9) * 3 / 3) / 3 == 3
q(CE, "Resistivity and temperature", "Advanced", "numerical",
  "A uniform wire of resistance 9 Ω is stretched uniformly to three times its original length, its volume and "
  "resistivity remaining unchanged. It is then cut into three pieces of equal length, and the three pieces are "
  "connected in parallel. The resistance of the combination is:",
  *opt("9 Ω", ["1 Ω", "27 Ω", "3 Ω"], "A"),
  "R = ρl/A with volume constant gives R ∝ l²; identical resistors in parallel",
  "Stretching to three times the length at constant volume reduces the area to one third, so the resistance becomes "
  "3² = 9 times larger. Each third of the stretched wire then has one third of that resistance, and three equal "
  "resistors in parallel give one third of one piece.",
  ["Stretched: R = 9 × 3² = 81 Ω", "Each piece: 81/3 = 27 Ω", "Three 27 Ω pieces in parallel: 27/3 = 9 Ω"],
  why="1 Ω ignores the stretching (pieces of 3 Ω in parallel). 27 Ω is the resistance of one piece. 3 Ω uses R ∝ l "
      "for the stretching, forgetting that the area also decreases.",
  ncert=CEC + "Ohm's law; resistivity", seconds=80, rc=True)

truth = {"a": True, "b": True, "c": True, "d": False, "e": True}
q(CE, "Wheatstone and metre bridge", "Advanced", "multi_statement",
  ms("In a Wheatstone bridge, resistors P and Q form one branch and R and S the other; both branches are connected "
     "across a cell of emf ε and internal resistance r, and a galvanometer joins the P–Q junction to the R–S "
     "junction. The bridge is balanced. Which of the following statements are correct?",
     ["No current flows through the galvanometer.",
      "The balance condition P/Q = R/S does not depend on the emf of the cell.",
      "The balance condition does not depend on the resistance of the galvanometer.",
      "The balance condition depends on the internal resistance of the cell.",
      "If the galvanometer is replaced by a resistor of any value, the currents through P, Q, R and S do not "
      "change."]),
  *mso(truth, "abce", ["abc", "abde", "bce"], "D"),
  "Balanced Wheatstone bridge: the two junctions are at the same potential",
  "At balance the P–Q and R–S junctions are at the same potential, so no current flows through anything connected "
  "between them, whatever its resistance. Hence (a) and (e). The condition P/Q = R/S comes from the ratios of the "
  "resistances alone; ε, r and the galvanometer resistance change only the size of the currents, not whether the "
  "bridge balances. So (b) and (c) are true and (d) is false.",
  ["(a) true", "(b) true", "(c) true", "(d) false: r affects the currents, not the balance", "(e) true: no PD across "
   "the junctions, so no current in any element joining them"],
  why="Options with (d) wrongly make the balance depend on the cell; the option without (e) misses that a balanced "
      "bridge passes no current between the junctions whatever element joins them; the option without (a) misses "
      "the defining property of balance.",
  ncert=CEC + "Wheatstone bridge", seconds=80)

n_c, e_c, r_c = 4, F(3, 2), F(1, 4)
I_ring = n_c * e_c / (n_c * r_c)
assert I_ring == 6 and e_c - I_ring * r_c == 0 and n_c * e_c / r_c == 24
q(CE, "Cells, emf and internal resistance", "Advanced", "numerical",
  "Four identical cells, each of emf 1.5 V and internal resistance 0.25 Ω, are connected in series to form a closed "
  "ring (the positive terminal of each joined to the negative terminal of the next), with nothing else in the "
  "circuit. The current in the ring and the reading of an ideal voltmeter connected across the terminals of any "
  "one cell are, respectively:",
  *opt("6 A and 0 V", ["6 A and 1.5 V", "24 A and 0 V", "zero and 1.5 V"], "C"),
  "Current in a closed loop of cells; terminal voltage V = ε − Ir",
  "Round the ring the emfs add to 6 V and the internal resistances to 1 Ω, so the current is 6 A. For each cell the "
  "drop across its internal resistance is Ir = 6 × 0.25 = 1.5 V, exactly its emf, so its terminal voltage is zero.",
  ["Total emf = 4 × 1.5 = 6 V; total resistance = 4 × 0.25 = 1 Ω", "I = 6/1 = 6 A",
   "Terminal voltage of each cell = 1.5 − 6 × 0.25 = 0 V"],
  shortcut="By symmetry all four terminals of the ring must be at the same potential, so every voltmeter reads zero.",
  why="1.5 V is the emf, which a voltmeter would read only if no current flowed. 24 A divides the total emf by the "
      "internal resistance of one cell. 'Zero' current wrongly assumes the cells cancel; they all push current the "
      "same way round the ring.",
  ncert=CEC + "cells in series and in parallel", seconds=80, rc=True)


# ================================================================ Magnetic Effects of Current and Magnetism (B5 I7 A5)
MCC = NC + "'Moving Charges and Magnetism', "
MMC = NC + "'Magnetism and Matter', "

# ---- Basic
chi = F(-2, 100000)
assert 1 + chi == F(99998, 100000)
q(MAG, "Magnetic materials", "Basic", "numerical",
  "The magnetic susceptibility of a material is −2.0 × 10⁻⁵. Its relative magnetic permeability and the class of "
  "magnetic material it belongs to are:",
  *opt("0.99998; diamagnetic", ["1.00002; paramagnetic", "−2.0 × 10⁻⁵; diamagnetic", "0.99998; paramagnetic"], "B"),
  "Relative permeability μ_r = 1 + χ; a small negative χ (μ_r slightly less than 1) marks a diamagnetic material",
  "Susceptibility and relative permeability are related by μ_r = 1 + χ. A small negative susceptibility means the "
  "material is magnetised weakly opposite to the applied field, which is diamagnetism.",
  ["μ_r = 1 + (−2.0 × 10⁻⁵) = 0.99998", "χ small and negative (μ_r < 1) → diamagnetic"],
  why="1.00002 adds the magnitude of χ and would describe a paramagnetic material. −2.0 × 10⁻⁵ is χ itself, not "
      "μ_r. A paramagnetic material has μ_r slightly greater than 1.",
  ncert=MMC + "magnetic properties of materials", seconds=35, rc=True)

Fmax = 0.20 * 5 * 0.4
close(Fmax, 0.40)
close(20 * 5 * 0.4, 40)
q(MAG, "Force on charges and conductors", "Basic", "numerical",
  "A straight wire 20 cm long carries a current of 5 A in a uniform magnetic field of 0.4 T. As the orientation of "
  "the wire in the field is changed, the largest and the smallest possible magnitudes of the magnetic force on it "
  "are, respectively:",
  *opt("0.40 N and zero", ["0.40 N and 0.20 N", "40 N and zero", "0.20 N and zero"], "A"),
  "Force on a straight current-carrying conductor: F = I l B sin θ",
  "The force is largest when the wire is perpendicular to the field (sin θ = 1) and zero when the wire lies along the "
  "field (sin θ = 0).",
  ["F_max = I l B = 5 × 0.20 × 0.4 = 0.40 N", "F_min = 0 (wire parallel to B)"],
  why="0.20 N is the force at 30° (sin 30° = ½); it is not a minimum. 40 N keeps the length in centimetres. "
      "0.20 N as the maximum halves the correct value.",
  ncert=MCC + "magnetic force on a current-carrying conductor", seconds=30, rc=True)

q(MAG, "Magnetic materials", "Basic", "statement_pair",
  sp("A ferromagnetic material consists of domains; a typical domain is about 1 mm across and contains about 10¹¹ "
     "atoms whose magnetic moments are aligned in the same direction.",
     "When a paramagnetic sample is kept in a fixed weak magnetic field and its temperature is raised, its "
     "magnetisation increases."),
  SP, sp_key(True, False),
  "Domains in ferromagnets; effect of temperature on paramagnets",
  "Statement I is NCERT's description of domains. Statement II is false: in a paramagnet, thermal agitation "
  "randomises the atomic dipoles, so at higher temperature fewer of them line up with the field and the "
  "magnetisation decreases (Curie's law, M ∝ B/T).",
  ["I: domain ≈ 1 mm, ≈ 10¹¹ atoms → true", "II: M ∝ 1/T for a paramagnet → false"],
  why="Statement II reverses the effect of temperature on a paramagnet.",
  ncert=MMC + "ferromagnetism; paramagnetism", seconds=40)

q(MAG, "Magnetic dipole and bar magnet", "Basic", "direct",
  "A square loop of wire lies in the x–y plane and carries a steady current that circulates anticlockwise when "
  "viewed from a point on the positive z-axis. The magnetic dipole moment of the loop is directed along:",
  *opt("the +z axis", ["the −z axis", "the +x axis", "the diagonal of the square, in the plane of the loop"], "D"),
  "Magnetic moment of a current loop: m = I A, with A along the normal given by the right-hand rule",
  "The magnetic moment is perpendicular to the plane of the loop. Curling the fingers of the right hand in the "
  "direction of the current, the thumb points along m. An anticlockwise current seen from +z gives m along +z.",
  ["m ⊥ plane of loop", "Right-hand rule: anticlockwise seen from +z → m along +z"],
  why="−z would correspond to a clockwise current seen from +z. A magnetic moment never lies in the plane of a "
      "plane loop, so +x and the diagonal are both wrong.",
  ncert=MCC + "the current loop as a magnetic dipole", seconds=30)

q(MAG, "Magnetic materials", "Basic", "assertion_reason",
  ar("The magnetic field inside a long current-carrying solenoid becomes much stronger when a soft iron core is "
     "placed inside it.",
     "Soft iron is ferromagnetic, with a relative permeability very much larger than 1, so it is strongly magnetised "
     "along the field of the solenoid."),
  AR, ar_key(True, True, True),
  "Field in a solenoid filled with a material: B = μ₀μ_r n I",
  "With the core in place, the field is μ_r times the field of the empty solenoid. For soft iron μ_r is very large "
  "(its domains line up readily with the applied field), so the field increases greatly. R is the cause of A.",
  ["Empty solenoid: B₀ = μ₀ n I", "With core: B = μ_r B₀, μ_r ≫ 1 for soft iron", "R explains A"],
  why="R is not a separate property of iron; the strong magnetisation of the core is exactly why the field grows.",
  ncert=MMC + "ferromagnetism", seconds=35)

# ---- Intermediate
B0, chi_p = 2.5e-3, 2.0e-4
dB = chi_p * B0
close(dB, 5.0e-7)
close((1 + chi_p) * B0, 2.5005e-3)
close(chi_p * 100 * B0, 5.0e-5)
q(MAG, "Magnetic materials", "Intermediate", "numerical",
  "The magnetic field well inside a long, air-filled solenoid carrying a steady current is 2.5 mT. The solenoid is "
  "completely filled with a paramagnetic material of magnetic susceptibility 2.0 × 10⁻⁴, the current being kept "
  "the same. The magnetic field inside the solenoid:",
  *opt("increases by 5.0 × 10⁻⁷ T", ["decreases by 5.0 × 10⁻⁷ T", "becomes 5.0 × 10⁻⁷ T",
                                     "increases by 5.0 × 10⁻⁵ T"], "C"),
  "Field in a material: B = µ₀µ_r H with µ_r = 1 + χ; a paramagnetic material has a small positive χ",
  "With the current unchanged, the field inside becomes µ_r = 1 + χ times the field of the empty solenoid. For a "
  "paramagnetic material χ is small and positive, so the field increases slightly; the increase is χ times the "
  "original field.",
  ["B = (1 + χ)B₀", "Increase = χB₀ = 2.0 × 10⁻⁴ × 2.5 × 10⁻³ T = 5.0 × 10⁻⁷ T"],
  why="'Decreases' is what a diamagnetic material (χ < 0) would do. 'Becomes 5.0 × 10⁻⁷ T' multiplies B₀ by χ "
      "instead of by 1 + χ, leaving almost no field. 5.0 × 10⁻⁵ T treats χ as a percentage (×100).",
  ncert=MMC + "magnetisation and magnetic intensity; paramagnetism", seconds=50, rc=True)

G_, Ig, Ir = F(60), F(3, 100), F(3)
S_ = Ig * G_ / (Ir - Ig)
RA = G_ * S_ / (G_ + S_)
assert RA == F(6, 10) and RA == Ig * G_ / Ir and round(float(S_), 3) == 0.606 and round(float(G_ + S_), 1) == 60.6
q(MAG, "Torque on loop and galvanometer", "Intermediate", "numerical",
  "A galvanometer of resistance 60 Ω gives full-scale deflection for a current of 30 mA. It is converted into an "
  "ammeter of range 0–3 A by connecting a suitable shunt. The resistance of the ammeter so formed (galvanometer and "
  "shunt together) is:",
  *opt("0.60 Ω", ["0.606 Ω", "60.6 Ω", "60 Ω"], "D"),
  "Conversion of a galvanometer into an ammeter: a low resistance shunt S in parallel",
  "At full scale, 30 mA flows through the galvanometer and the remaining 2.97 A through the shunt, both having the "
  "same potential difference I_g G across them. The ammeter's resistance is the parallel combination of G and S, "
  "which is also (I_g G)/I.",
  ["PD at full scale = 0.030 × 60 = 1.8 V", "S = 1.8/2.97 ≈ 0.606 Ω",
   "R_ammeter = G S/(G + S) = 1.8 V / 3 A = 0.60 Ω"],
  shortcut="R_ammeter = (full-scale PD)/(full-scale current) = 1.8/3 = 0.60 Ω.",
  why="0.606 Ω is the shunt alone. 60.6 Ω adds G and S as if they were in series. 60 Ω ignores the shunt.",
  ncert=MCC + "moving coil galvanometer", seconds=60, rc=True)

q(MAG, "Magnetic dipole and bar magnet", "Intermediate", "match_list",
  ml("Match List-I (physical quantity) with List-II (an SI unit in which it can be expressed).",
     ["Magnetisation (magnetic moment per unit volume)", "Magnetic susceptibility",
      "Magnetic dipole moment", "Current sensitivity of a moving-coil galvanometer"],
     ["A m⁻¹", "no unit (a pure number)", "J T⁻¹", "rad A⁻¹"]),
  *mlo("A-I, B-II, C-III, D-IV", ["A-III, B-II, C-I, D-IV", "A-I, B-IV, C-III, D-II", "A-II, B-I, C-III, D-IV"], "B"),
  "Units from definitions: M = m/V, χ = M/H, U = −m·B, current sensitivity φ/I",
  "Magnetisation is magnetic moment (A m²) per unit volume (m³): A m⁻¹. Susceptibility is the ratio of two "
  "quantities with the same unit (M and H), so it has none. From U = −m·B, m has the unit J T⁻¹ (equivalent to "
  "A m²). Current sensitivity is deflection per unit current: rad A⁻¹.",
  ["A → I", "B → II", "C → III", "D → IV"],
  why="The other codes exchange magnetisation with magnetic moment (they differ by a factor of volume), or give "
      "susceptibility a unit although it is a ratio.",
  ncert=MMC + "magnetisation and magnetic intensity", seconds=50)

m_, g_, qq, BB = 1e-3, 10, 1e-6, 0.5
v_lev = m_ * g_ / (qq * BB)
close(v_lev, 2e4)
close(m_ / (qq * BB), 2e3)
close(qq * BB / (m_ * g_), 5e-5)
q(MAG, "Force on charges and conductors", "Intermediate", "numerical",
  "A small particle of mass 1.0 g carrying a charge of +1.0 μC is projected horizontally, at right angles to a "
  "uniform horizontal magnetic field of 0.50 T, in a direction such that the magnetic force on it is vertically "
  "upwards. Taking g = 10 m/s², the speed with which it must be projected so that it moves along a horizontal straight "
  "line is:",
  *opt("2.0 × 10⁴ m/s", ["2.0 × 10³ m/s", "2.0 × 10⁷ m/s", "5.0 × 10⁻⁵ m/s"], "A"),
  "Magnetic force qvB balancing the weight mg",
  "For straight-line motion the upward magnetic force must cancel the weight exactly. Since v is perpendicular to B, "
  "the force is qvB, and it stays vertical as long as the particle moves horizontally.",
  ["qvB = mg", "v = mg/(qB) = (1.0 × 10⁻³ × 10)/(1.0 × 10⁻⁶ × 0.50)", "v = 2.0 × 10⁴ m/s"],
  why="2.0 × 10³ m/s leaves out g. 2.0 × 10⁷ m/s keeps the mass in grams. 5.0 × 10⁻⁵ m/s inverts the expression.",
  ncert=MCC + "magnetic force", seconds=50, rc=True)

truth = {"a": True, "b": True, "c": False, "d": True, "e": False}
q(MAG, "Magnetic dipole and bar magnet", "Intermediate", "multi_statement",
  ms("An electron (charge −e, mass mₑ) revolves with speed v in a circular orbit of radius r round the nucleus, as in "
     "the Bohr model of the hydrogen atom. Its orbital angular momentum is l. Which of the following statements are "
     "correct?",
     ["The magnitude of its orbital magnetic moment is evr/2.",
      "The ratio of the magnitude of its orbital magnetic moment to that of its orbital angular momentum is "
      "e/(2mₑ).",
      "Its orbital magnetic moment points in the same direction as its orbital angular momentum.",
      "The smallest value of the orbital magnetic moment, the Bohr magneton, is about 9.27 × 10⁻²⁴ A m².",
      "The equivalent current of the revolving electron is ev/r."]),
  *mso(truth, "abd", ["abc", "ade", "bcd"], "C"),
  "Magnetic dipole moment of a revolving electron",
  "The revolving electron is a current loop with I = e/T = ev/(2πr), so μ = Iπr² = evr/2. Since l = mₑvr, "
  "μ/l = e/(2mₑ). Because the electron's charge is negative, its magnetic moment is opposite to its angular "
  "momentum: μ = −(e/2mₑ) l. Using Bohr's l = h/2π gives the least value eh/(4πmₑ) ≈ 9.27 × 10⁻²⁴ A m², the Bohr "
  "magneton.",
  ["(a) true", "(b) true", "(c) false: opposite, as the charge is negative", "(d) true",
   "(e) false: I = ev/(2πr)"],
  why="Options with (c) forget the negative charge of the electron; options with (e) leave out the 2π in the period "
      "2πr/v.",
  ncert=MCC + "magnetic dipole moment of a revolving electron", seconds=70)

q(MAG, "Force on charges and conductors", "Intermediate", "statement_pair",
  sp("A charged particle moving along a helix in a uniform magnetic field (no other force acting) has a constant "
     "velocity.",
     "The kinetic energy of such a particle remains constant."),
  SP, sp_key(False, True),
  "Magnetic force is perpendicular to velocity: it changes direction, not speed",
  "The magnetic force q(v × B) is always perpendicular to the velocity, so it does no work: the speed and the kinetic "
  "energy stay constant (Statement II true). But the direction of motion keeps changing round the helix, so the "
  "velocity, a vector, is not constant (Statement I false).",
  ["I: direction changes → velocity not constant → false", "II: F ⊥ v → no work → KE constant → true"],
  why="Statement I confuses constant speed with constant velocity.",
  ncert=MCC + "motion in a magnetic field", seconds=40)

q(MAG, "Biot-Savart law", "Intermediate", "direct",
  "Two identical circular loops of wire are placed coaxially, a short distance apart, in parallel planes. They carry "
  "steady currents circulating in the same sense when viewed along the common axis. The loops will:",
  *opt("attract each other", ["repel each other", "exert no force on each other, since their fields are parallel",
                              "rotate so that their planes become perpendicular"], "B"),
  "Force between parallel currents; a current loop as a magnetic dipole",
  "Facing portions of the two loops carry currents in the same direction, and parallel currents in the same "
  "direction attract. Equivalently, each loop is a magnetic dipole and the two moments point the same way along the "
  "common axis, so the north face of one faces the south face of the other.",
  ["Adjacent segments carry parallel currents → attraction",
   "Dipole picture: moments aligned along the axis, N of one facing S of the other → attraction"],
  why="Repulsion would need opposite senses of circulation. The loops do exert forces on each other. Coaxial loops "
      "with aligned moments are already in equilibrium as far as torque is concerned, so they do not turn.",
  ncert=MCC + "force between two parallel currents; the current loop as a magnetic dipole", seconds=40)

# ---- Advanced
Bt, It, Rt_ = 0.5, 4, 0.10
T_loop = Bt * It * Rt_
close(T_loop, 0.2)
close(2 * Bt * It * Rt_, 0.4)
close(2 * math.pi * Rt_ * Bt * It, 1.2566)
q(MAG, "Force on charges and conductors", "Advanced", "numerical",
  "A thin flexible circular loop of wire of radius 10 cm lies in a plane perpendicular to a uniform magnetic field of "
  "0.50 T and carries a current of 4.0 A, in the sense for which the magnetic forces on it act outwards (away from "
  "its centre) everywhere. The tension in the wire is:",
  *opt("0.20 N", ["0.40 N", "1.3 N", "zero, because the net force on the loop is zero"], "D"),
  "Force on a curved conductor in a uniform field; equilibrium of half the loop",
  "Consider one half of the loop. The magnetic force on a semicircle in a uniform field equals the force on the "
  "straight diameter joining its ends: B I (2R), directed outwards. This half is held in equilibrium by the tension "
  "T acting at each of its two cut ends, both pulling towards the other half: 2T = 2BIR.",
  ["Force on a semicircle = B I × 2R = 0.50 × 4.0 × 0.20 = 0.40 N", "2T = 0.40 N", "T = BIR = 0.20 N"],
  why="0.40 N is the net magnetic force on half the loop, which is shared by two ends. 1.3 N multiplies B I by the "
      "whole circumference, adding force magnitudes that point in different directions. The net force on the whole "
      "loop is zero, but each part is still stretched.",
  ncert=MCC + "magnetic force on a current-carrying conductor", seconds=110, rc=True)

Bw = 2e-7 * 10 / 0.05
Fp = 1.6e-19 * 2e6 * Bw
close(Bw, 4e-5)
close(Fp, 1.28e-17)
q(MAG, "Force on charges and conductors", "Advanced", "numerical",
  "A long straight wire carries a steady current of 10 A. At an instant when a proton is 5.0 cm from the wire, it is "
  "moving with a speed of 2.0 × 10⁶ m/s directly towards the wire (along the perpendicular from it to the wire). "
  "Taking µ₀ = 4π × 10⁻⁷ T m A⁻¹ and e = 1.6 × 10⁻¹⁹ C, the magnetic force on the proton at that instant is:",
  *opt("1.28 × 10⁻¹⁷ N, parallel to the wire and opposite to the current",
       ["1.28 × 10⁻¹⁷ N, parallel to the wire and in the direction of the current",
        "1.28 × 10⁻¹⁷ N, directed away from the wire",
        "6.4 × 10⁻¹⁸ N, parallel to the wire and opposite to the current"], "C"),
  "Field of a long straight wire; Lorentz force F = q v × B",
  "Take the wire along the z-axis with the current along +z, and the proton on the +x axis moving in the −x "
  "direction. At that point the field is along +y (right-hand rule). Then v × B = (−v x̂) × (B ŷ) = −vB ẑ, so the "
  "force is parallel to the wire and opposite to the current.",
  ["B = µ₀I/(2πd) = 2 × 10⁻⁷ × 10/0.05 = 4.0 × 10⁻⁵ T", "|F| = evB = 1.6 × 10⁻¹⁹ × 2.0 × 10⁶ × 4.0 × 10⁻⁵ "
   "= 1.28 × 10⁻¹⁷ N", "Direction: (−x̂) × ŷ = −ẑ → opposite to the current"],
  why="'In the direction of the current' reverses the cross product. 'Away from the wire' is the direction for a "
      "proton moving parallel to the current in the opposite direction, not one moving towards the wire. "
      "6.4 × 10⁻¹⁸ N uses µ₀I/(4πd) for the field, half the correct value.",
  ncert=MCC + "Ampere's circuital law (field of a straight wire); magnetic force",
  seconds=120, rc=True)

Gv, Igv = F(50), F(2, 1000)
R1v = 5 / Igv - Gv
R2v = 20 / Igv - Gv - R1v
assert R1v == 2450 and R2v == 7500 and 20 / Igv - Gv == 9950
q(MAG, "Torque on loop and galvanometer", "Advanced", "numerical",
  "A galvanometer of resistance 50 Ω gives full-scale deflection for a current of 2.0 mA. It is made into a "
  "two-range voltmeter: a resistor R₁ in series with the galvanometer gives the 0–5 V range, and a further resistor "
  "R₂ added in series with R₁ (between R₁ and a second terminal) gives the 0–20 V range. The values of R₁ and R₂ "
  "are:",
  *opt("2450 Ω and 7500 Ω", ["2500 Ω and 10 000 Ω", "2450 Ω and 9950 Ω", "2500 Ω and 7500 Ω"], "A"),
  "Galvanometer as a voltmeter: total resistance = range ÷ full-scale current",
  "On the 5 V range the total resistance must be 5/0.002 = 2500 Ω, which includes the 50 Ω galvanometer. On the "
  "20 V range the total must be 20/0.002 = 10 000 Ω, which includes both the galvanometer and R₁.",
  ["R₁ = 5/0.002 − 50 = 2450 Ω", "R₁ + R₂ + 50 = 10 000 Ω", "R₂ = 10 000 − 2500 = 7500 Ω"],
  why="2500 Ω and 10 000 Ω are the total resistances of the two ranges, not the added resistors. 9950 Ω is the "
      "resistor needed for 20 V on its own, forgetting that R₁ is already in the circuit. 2500 Ω for R₁ ignores the "
      "galvanometer's own resistance.",
  ncert=MCC + "moving coil galvanometer", seconds=100, rc=True)

truth = {"a": True, "b": True, "c": False, "d": True, "e": True}
q(MAG, "Force on charges and conductors", "Advanced", "multi_statement",
  ms("In a region there are a uniform electric field E and a uniform magnetic field B, both directed along the +z "
     "axis. A positively charged particle is introduced into the region (gravity negligible). Which of the following "
     "statements are correct?",
     ["If it is released from rest, it moves along a straight line parallel to the z-axis with uniform "
      "acceleration.",
      "If its initial velocity is perpendicular to the z-axis, it moves along a helix about an axis parallel to z, "
      "advancing a greater distance along z in each successive turn.",
      "Its speed remains constant whatever its initial velocity.",
      "The magnetic force on it does no work.",
      "The time it takes for each turn round the z-direction is 2πm/(qB), the same for every turn."]),
  *mso(truth, "abde", ["abcd", "ade", "bcde"], "B"),
  "Superposition of the motions due to E and B when the fields are parallel",
  "The electric force qE is along z and changes only the z-component of velocity, uniformly. The magnetic force acts "
  "only on the velocity component perpendicular to B (which E does not change), giving uniform circular motion in "
  "the x–y projection with period 2πm/(qB). Released from rest, there is no perpendicular velocity and the particle "
  "simply accelerates along z. With a perpendicular initial velocity the path is a helix whose step along z grows "
  "each turn, because v_z keeps increasing. The magnetic force is always perpendicular to the velocity and does no "
  "work, but the electric force does work, so the speed is not constant.",
  ["(a) true", "(b) true", "(c) false: E does work", "(d) true", "(e) true: period independent of speed"],
  why="Options with (c) forget that the electric field does work on the charge; the options leaving out (b) or (e) "
      "miss that the circular part of the motion depends only on B.",
  ncert=MCC + "motion in a magnetic field; motion in combined electric and magnetic fields", seconds=100)

KE_e, B_e = 100 * 1.6e-19, 1.0e-3
mu_e = KE_e / B_e
close(mu_e, 1.6e-14)
m_e = 9.1e-31
v_e = math.sqrt(2 * KE_e / m_e)
r_e = m_e * v_e / (1.6e-19 * B_e)
close(1.6e-19 * v_e * r_e / 2, mu_e, 1e-9)
q(MAG, "Magnetic dipole and bar magnet", "Advanced", "numerical",
  "An electron with a kinetic energy of 100 eV moves in a circle in a plane perpendicular to a uniform magnetic field "
  "of 1.0 mT (1 eV = 1.6 × 10⁻¹⁹ J). Treating the circulating electron as a current loop, the magnitude of its "
  "magnetic dipole moment and its direction relative to the field are:",
  *opt("1.6 × 10⁻¹⁴ A m², opposite to the field",
       ["1.6 × 10⁻¹⁴ A m², along the field", "3.2 × 10⁻¹⁴ A m², opposite to the field",
        "1.6 × 10⁻²⁰ A m², opposite to the field"], "D"),
  "Magnetic moment of a circulating charge, μ = IA with I = q/T; radius r = mv/(qB)",
  "For a charge circulating in a field B: I = e/T = e²B/(2πm) and A = πr² with r = mv/(eB). Then "
  "μ = IA = e²B r²/(2m) = (½mv²)/B, the kinetic energy divided by the field. The sense of circulation is such that "
  "the moment opposes the applied field (for either sign of charge), the same tendency that underlies diamagnetism.",
  ["μ = evr/2 with r = mv/(eB) → μ = mv²/(2B) = KE/B", "KE = 100 × 1.6 × 10⁻¹⁹ = 1.6 × 10⁻¹⁷ J",
   "μ = 1.6 × 10⁻¹⁷/1.0 × 10⁻³ = 1.6 × 10⁻¹⁴ A m², opposite to B"],
  why="'Along the field' gets the sense of circulation wrong: an electron in a field B along +z circulates "
      "anticlockwise seen from +z, so the conventional current is clockwise and the moment points along −z. "
      "3.2 × 10⁻¹⁴ A m² uses mv²/B, dropping the ½. 1.6 × 10⁻²⁰ A m² multiplies KE by B instead of dividing.",
  ncert=MCC + "motion in a magnetic field; magnetic dipole moment of a revolving electron", seconds=140, rc=True)


# ================================================================ Electromagnetic Induction and AC (B4 I5 A4)
EMC = NC + "'Electromagnetic Induction', "
ACC = NC + "'Alternating Current', "

# ---- Basic
U_, I_l = F(4, 10), F(2)
L_ = 2 * U_ / I_l ** 2
assert L_ == F(1, 5) and U_ / I_l ** 2 == F(1, 10) and 2 * U_ / I_l == F(2, 5) and U_ / (2 * I_l ** 2) == F(1, 20)
q(EMI, "Self and mutual inductance", "Basic", "numerical",
  "When a steady current of 2.0 A flows through a coil, the energy stored in its magnetic field is 0.40 J. The "
  "self-inductance of the coil is:",
  *opt("0.20 H", ["0.10 H", "0.40 H", "0.05 H"], "C"),
  "Magnetic energy stored in an inductor: U = ½ L I²",
  "Rearranging U = ½LI² gives L = 2U/I².",
  ["L = 2U/I² = 2 × 0.40/2.0²", "L = 0.80/4.0 = 0.20 H"],
  why="0.10 H drops the factor ½ from U = ½LI². 0.40 H divides by I instead of I². 0.05 H puts the ½ on the wrong "
      "side of the equation.",
  ncert=EMC + "self-inductance", seconds=30, rc=True)

q(EMI, "Self and mutual inductance", "Basic", "direct",
  "For a coil of self-inductance L and resistance R, the ratio L/R has the dimensions of:",
  *opt("time", ["frequency", "resistance", "a pure number (it is dimensionless)"], "A"),
  "Dimensional analysis using ε = L dI/dt and V = IR",
  "From ε = L (dI/dt), the unit of L is V s A⁻¹ = Ω s. Dividing by the unit of R (Ω) leaves seconds, so L/R has the "
  "dimensions of time. (It is the time constant of an L–R circuit.)",
  ["[L] = V s A⁻¹ = Ω s", "[L/R] = Ω s / Ω = s → time"],
  why="Frequency would be R/L, the inverse. L/R is not a resistance and it is not dimensionless, since the henry "
      "is an ohm-second.",
  ncert=EMC + "self-inductance", seconds=30)

assert F(1, 2) ** 2 == F(1, 4)
q(EMI, "LCR resonance and power", "Basic", "numerical",
  "A series LCR circuit is in resonance at a frequency f₀. Keeping L and R unchanged, the capacitance C must be "
  "changed to which value so that the resonant frequency becomes 2f₀?",
  *opt("C/4", ["C/2", "2C", "4C"], "D"),
  "Resonant frequency f₀ = 1/(2π√(LC))",
  "The resonant frequency varies inversely as the square root of C. To double it with L fixed, √C must be halved, "
  "so C must become one quarter.",
  ["f ∝ 1/√C", "2f₀ → √C' = √C/2 → C' = C/4"],
  why="C/2 treats f as inversely proportional to C, not to √C. 2C and 4C change C in the wrong direction; they "
      "would lower the resonant frequency.",
  ncert=ACC + "series LCR circuit: resonance", seconds=30, rc=True)

q(EMI, "Self and mutual inductance", "Basic", "statement_pair",
  sp("For a pair of coils, the flux linked with the second coil per unit current in the first equals the flux linked "
     "with the first coil per unit current in the second; that is, M₁₂ = M₂₁.",
     "Self-inductance and mutual inductance are both measured in the same SI unit, the henry."),
  SP, sp_key(True, True),
  "Mutual inductance and its unit",
  "NCERT shows for two long coaxial solenoids that M₁₂ = M₂₁ and states that the relation holds in general, so "
  "Statement I is true. Both inductances are flux linkage per unit current (Wb A⁻¹), the henry, so Statement II is "
  "true.",
  ["I: M₁₂ = M₂₁ → true", "II: unit of both = henry = Wb A⁻¹ → true"],
  why="Both statements are true; neither is a trap.",
  ncert=EMC + "mutual inductance", seconds=35)

# ---- Intermediate
q(EMI, "Faraday's and Lenz's laws", "Intermediate", "direct",
  "A closed coil B (not connected to any battery) is placed close to a coil A, the two being coaxial. A steady "
  "battery is connected to A through a switch. When the switch is closed, coil B is:",
  *opt("repelled from A, but only while the current in A is growing",
       ["attracted towards A, but only while the current in A is growing",
        "repelled from A for as long as the current in A flows",
        "not acted on by any force, since no battery drives a current in B"], "B"),
  "Lenz's law: the induced current opposes the change of flux that produces it",
  "While the current in A grows, the flux through B increases, so the induced current in B circulates in the "
  "opposite sense to the current in A, opposing the increase. Antiparallel currents repel (equivalently, like poles "
  "face each other), so B is pushed away. Once the current in A is steady, the flux through B no longer changes, "
  "the induced current stops and so does the force.",
  ["Growing current in A → increasing flux through B", "Induced current in B opposite to that in A → repulsion",
   "Steady current in A → no induced current → no force"],
  why="Attraction would occur while the current in A is decreasing (for example when the switch is opened). A "
      "steady current induces nothing, so the force does not last. B needs no battery: the changing flux induces a "
      "current in it.",
  ncert=EMC + "Lenz's law and conservation of energy", seconds=45)

Lc, Ic, dIdt = 0.5, 2, 4
P_store = Lc * Ic * dIdt
close(P_store, 4)
q(EMI, "Self and mutual inductance", "Intermediate", "numerical",
  "The current in an ideal coil of self-inductance 0.50 H is increasing at a steady rate of 4.0 A/s. At the instant "
  "when the current is 2.0 A, the rate at which energy is being stored in the magnetic field of the coil is:",
  *opt("4.0 W", ["2.0 W", "1.0 W", "8.0 W"], "C"),
  "Energy stored U = ½LI², so dU/dt = L I (dI/dt) = (self-induced emf) × current",
  "The source must push the current against the self-induced emf L dI/dt = 0.50 × 4.0 = 2.0 V. The power it delivers "
  "to the coil, all of which is stored in the field of an ideal coil, is this emf times the current.",
  ["Self-induced emf = L dI/dt = 2.0 V", "dU/dt = emf × I = 2.0 V × 2.0 A = 4.0 W"],
  shortcut="dU/dt = d(½LI²)/dt = LI dI/dt = 0.5 × 2 × 4 = 4 W.",
  why="2.0 W keeps an extra ½ when differentiating ½LI². 1.0 W is the stored energy ½LI² = 1.0 J at that instant, "
      "not its rate of increase. 8.0 W multiplies L by I² and dI/dt.",
  ncert=EMC + "self-inductance", seconds=60, rc=True)

mu0 = 4 * math.pi * 1e-7
Ls = mu0 * 1000 ** 2 * 1e-3 / 0.5
Us = 0.5 * Ls * 2 ** 2
close(Ls, 2.513e-3)
close(Us, 5.03e-3)
close(0.5 * Ls * 2, 2.51e-3)
close(0.5 * mu0 * 1000 ** 2 * 1e-3 * 0.5 * 4, 1.257e-3)
q(EMI, "Self and mutual inductance", "Intermediate", "numerical",
  "A long air-cored solenoid is 50 cm long, has 1000 turns and a cross-sectional area of 10 cm², and carries a "
  "steady current of 2.0 A. Taking µ₀ = 4π × 10⁻⁷ T m A⁻¹, the energy stored in its magnetic field is about:",
  *opt("5.0 mJ", ["2.5 mJ", "10 mJ", "1.3 mJ"], "D"),
  "Self-inductance of a long solenoid L = µ₀N²A/l; energy U = ½LI²",
  "First find the self-inductance from the dimensions of the solenoid, then the energy for a current of 2.0 A.",
  ["L = µ₀N²A/l = 4π × 10⁻⁷ × 10⁶ × 10 × 10⁻⁴/0.50 ≈ 2.5 × 10⁻³ H",
   "U = ½LI² = ½ × 2.5 × 10⁻³ × 2.0² ≈ 5.0 × 10⁻³ J = 5.0 mJ"],
  why="2.5 mJ uses ½LI instead of ½LI². 10 mJ drops the ½. 1.3 mJ uses µ₀N²Al, putting the total number of turns N "
      "in place of n = N/l in L = µ₀n²Al.",
  ncert=EMC + "self-inductance", seconds=75, rc=True)

q(EMI, "AC generator and transformer", "Intermediate", "match_list",
  ml("Match each device or effect in List-I with the phenomenon on which it is based in List-II.",
     ["Transformer", "AC generator", "Induction furnace",
      "A spark across the switch when a circuit containing a large coil is suddenly broken"],
     ["Mutual induction", "Self-induction", "Heating by eddy currents",
      "Change of flux linkage of a coil rotated in a magnetic field"]),
  *mlo("A-I, B-IV, C-III, D-II", ["A-II, B-IV, C-III, D-I", "A-I, B-III, C-IV, D-II", "A-IV, B-I, C-III, D-II"], "A"),
  "Applications of electromagnetic induction",
  "A transformer transfers energy from the primary to the secondary through their mutual inductance. An AC "
  "generator produces an emf because the flux linkage of its rotating coil changes continuously. An induction "
  "furnace melts metal using the heat produced by large eddy currents. When a current in a coil of large "
  "self-inductance is cut off quickly, the large self-induced emf can make a spark jump across the switch.",
  ["A → I", "B → IV", "C → III", "D → II"],
  why="The other codes swap self- and mutual induction between the transformer and the spark, or attribute the "
      "generator to eddy currents; eddy currents are a loss in a generator, not its working principle.",
  ncert=EMC + "self-inductance; mutual inductance; eddy currents; AC generator", seconds=50)

q(EMI, "AC: rms, reactance and impedance", "Intermediate", "assertion_reason",
  ar("An ideal inductor, which has no resistance, limits the alternating current through it, although it lets a "
     "steady direct current pass without any opposition once the current has become steady.",
     "The emf self-induced in the inductor opposes every change of current in it, giving it a reactance "
     "X_L = ωL, which is zero for a steady current (ω = 0)."),
  AR, ar_key(True, True, True),
  "Inductive reactance X_L = ωL",
  "For an alternating current the current is always changing, so the self-induced emf L(di/dt) always opposes it; "
  "this opposition is the reactance ωL, which limits the rms current to V/(ωL). For a steady current di/dt = 0, the "
  "self-induced emf is zero and an ideal inductor offers no opposition. R gives exactly this reason.",
  ["AC: X_L = ωL > 0 → current limited", "Steady DC: ω = 0 → X_L = 0", "R explains A"],
  why="R is not a separate fact about inductors; the self-induced emf is the cause of the reactance.",
  ncert=ACC + "AC voltage applied to an inductor", seconds=40)

# ---- Advanced
m_r, v0, Rr, Br, lr = F(1, 10), F(2), F(1), F(1, 2), F(4, 10)
X_stop = m_r * v0 * Rr / (Br ** 2 * lr ** 2)
a0 = Br ** 2 * lr ** 2 * v0 / (m_r * Rr)
assert X_stop == 5 and v0 ** 2 / (2 * a0) == F(5, 2)
q(EMI, "Faraday's and Lenz's laws", "Advanced", "numerical",
  "A metal rod of mass 0.10 kg lies across two smooth, horizontal, parallel conducting rails 0.40 m apart, which are "
  "joined at one end through a 1.0 Ω resistor; the rod and rails have negligible resistance. A uniform vertical "
  "magnetic field of 0.50 T acts on the region. The rod is given a velocity of 2.0 m/s along the rails, away from the "
  "resistor, and is then left to itself. The total distance it moves before coming to rest is:",
  *opt("5.0 m", ["2.5 m", "10 m", "infinite, because the rod never stops completely"], "B"),
  "Motional emf, induced current and the retarding force; charge through the circuit = change of flux / R",
  "The induced current I = Blv/R gives a retarding force BIl. Over the whole motion, the impulse of this force equals "
  "the momentum lost: Bl × (total charge Q) = mv₀. The total charge is the change of flux divided by R: "
  "Q = BlX/R, where X is the distance moved.",
  ["Impulse: Bl Q = m v₀", "Q = ΔΦ/R = BlX/R", "B²l²X/R = m v₀ → X = m v₀ R/(B²l²)",
   "X = 0.10 × 2.0 × 1.0/(0.25 × 0.16) = 5.0 m"],
  why="2.5 m treats the initial retarding force as constant (uniform deceleration), though it falls as the rod slows. "
      "10 m is twice the correct value. The speed decays exponentially, so the rod takes an infinite time to stop, "
      "but the distance covered is finite.",
  ncert=EMC + "motional electromotive force", seconds=150, rc=True)

lw, xw, Bw_, kw, vw = 0.5, 0.4, 0.5, 0.1, 2.0
emf_tot = lw * (xw * kw + Bw_ * vw)
close(emf_tot, 0.52)
close(lw * Bw_ * vw, 0.50)
close(lw * xw * kw, 0.02)
q(EMI, "Faraday's and Lenz's laws", "Advanced", "numerical",
  "A metal rod slides with a constant speed of 2.0 m/s along two parallel conducting rails 0.50 m apart that are "
  "joined at one end, forming a rectangular circuit whose area grows as the rod moves away from the joined end. A "
  "uniform magnetic field perpendicular to the plane of the rails is increasing at a steady rate of 0.10 T/s. At the "
  "instant when the field is 0.50 T and the rod is 0.40 m from the joined end, the magnitude of the emf induced in the "
  "circuit is:",
  *opt("0.52 V", ["0.50 V", "0.02 V", "0.48 V"], "C"),
  "Faraday's law with both the field and the area changing: Φ = B l x, dΦ/dt = l x (dB/dt) + B l (dx/dt)",
  "Both changes increase the flux through the circuit (the area grows and the field grows), so their contributions "
  "add.",
  ["Flux Φ = B l x", "Term from changing field: l x dB/dt = 0.50 × 0.40 × 0.10 = 0.02 V",
   "Term from moving rod: B l v = 0.50 × 0.50 × 2.0 = 0.50 V", "Total emf = 0.52 V"],
  why="0.50 V keeps only the motional emf. 0.02 V keeps only the part due to the changing field. 0.48 V subtracts "
      "the two parts, although both increase the flux.",
  ncert=EMC + "Faraday's law of induction; motional electromotive force", seconds=110, rc=True)

truth = {"a": True, "b": True, "c": True, "d": False, "e": True}
q(EMI, "AC: rms, reactance and impedance", "Advanced", "multi_statement",
  ms("A coil of large inductance and small resistance is connected in series with a bulb across an AC supply of "
     "fixed voltage and frequency. A soft-iron rod is then pushed into the coil. Which of the following statements "
     "are correct?",
     ["The self-inductance of the coil increases.",
      "The bulb becomes dimmer.",
      "The power factor of the circuit decreases.",
      "The current in the circuit starts to lead the supply voltage.",
      "If the same arrangement were connected to a steady DC supply instead, pushing the rod in would not change "
      "the steady brightness of the bulb."]),
  *mso(truth, "abce", ["abd", "acde", "bce"], "D"),
  "Inductive reactance X_L = ωL; impedance and power factor of an R–L circuit",
  "Soft iron has a large permeability, so the inductance of the coil increases (a). Then X_L = ωL increases, the "
  "impedance √(R² + X_L²) increases and the current falls, so the bulb dims (b). The power factor R/Z falls (c). In "
  "an R–L circuit the current always lags the voltage (d is false). With steady DC, an inductor offers no opposition "
  "once the current is steady, so the steady current depends only on the resistances (e).",
  ["(a) true", "(b) true", "(c) true: cos φ = R/Z", "(d) false: current lags in an R–L circuit",
   "(e) true: X_L = 0 for steady DC"],
  why="Any option containing (d) makes the inductive circuit capacitive. The options leaving out (c) or (a) miss "
      "the effect of the larger inductance on the power factor or the inductance itself.",
  ncert=ACC + "AC voltage applied to an inductor; power factor", seconds=90)

q(EMI, "Faraday's and Lenz's laws", "Advanced", "direct",
  "A flexible circular loop of wire lies in the plane of the page in a uniform magnetic field directed into the page. "
  "The field is steadily increasing. Because of the current induced in it, the loop tends to:",
  *opt("contract (its area tends to decrease)",
       ["expand (its area tends to increase)", "rotate about one of its diameters",
        "stay unchanged, since the net force on a closed loop in a uniform field is zero"], "B"),
  "Lenz's law; force on the induced current, F = I dl × B",
  "The induced current opposes the increase of the inward flux, so it produces an outward field inside the loop: it "
  "flows anticlockwise as seen by the reader. On each element the force I dl × B (dl anticlockwise, B into the page) "
  "points towards the centre. These inward forces squeeze the loop, tending to reduce its area and hence the flux, as "
  "Lenz's law requires.",
  ["Inward flux increasing → induced current anticlockwise", "F = I dl × B on each element points inwards",
   "Loop tends to contract, reducing the flux"],
  why="Expansion would increase the flux, which is the opposite of what Lenz's law demands (it would happen if the "
      "field were decreasing). There is no torque about a diameter in a uniform field when the moment is along B. The "
      "net force is zero, but the inward forces on the different parts still tend to change the shape.",
  ncert=EMC + "Lenz's law and conservation of energy", seconds=70)


# ================================================================ Electromagnetic Waves (B1 I1 A1)
EWC = NC + "'Electromagnetic Waves', "

c_ = 1 / math.sqrt(4 * math.pi * 1e-7 * 8.85e-12)
close(c_, 3.0e8, 2e-3)
close(1 / (4 * math.pi * 1e-7 * 8.85e-12), 9.0e16, 2e-3)
close(math.sqrt(4 * math.pi * 1e-7 * 8.85e-12), 3.3e-9, 2e-2)
q(EMW, "EM wave properties", "Basic", "numerical",
  "Taking µ₀ = 4π × 10⁻⁷ T m A⁻¹ and ε₀ = 8.85 × 10⁻¹² C² N⁻¹ m⁻², the speed of electromagnetic waves in vacuum "
  "predicted by Maxwell's equations is about:",
  *opt("3.0 × 10⁸ m/s", ["9.0 × 10¹⁶ m/s", "3.3 × 10⁻⁹ m/s", "1.1 × 10⁻¹⁷ m/s"], "B"),
  "Speed of electromagnetic waves in vacuum c = 1/√(µ₀ε₀)",
  "Maxwell found that his equations give waves travelling with speed 1/√(µ₀ε₀), which agrees with the measured "
  "speed of light.",
  ["µ₀ε₀ = 4π × 10⁻⁷ × 8.85 × 10⁻¹² ≈ 1.11 × 10⁻¹⁷ s² m⁻²", "c = 1/√(1.11 × 10⁻¹⁷) ≈ 3.0 × 10⁸ m/s"],
  why="9.0 × 10¹⁶ m/s forgets the square root (it is c², in m² s⁻²). 3.3 × 10⁻⁹ m/s is √(µ₀ε₀), the reciprocal of c. "
      "1.1 × 10⁻¹⁷ is µ₀ε₀ itself.",
  ncert=EWC + "electromagnetic waves: sources and nature", seconds=35, rc=True)

q(EMW, "EM wave properties", "Intermediate", "match_list",
  ml("Match each scientist in List-I with the contribution to the study of electromagnetic waves (List-II) that NCERT "
     "describes.",
     ["J. C. Maxwell", "H. Hertz", "J. C. Bose", "G. Marconi"],
     ["Transmitted electromagnetic waves over distances of many kilometres",
      "Produced and observed electromagnetic waves of much shorter wavelength, 25 mm to 5 mm",
      "Introduced the displacement current and predicted the existence of electromagnetic waves",
      "First demonstrated electromagnetic waves experimentally, in 1887"]),
  *mlo("A-III, B-IV, C-II, D-I", ["A-IV, B-III, C-II, D-I", "A-III, B-IV, C-I, D-II", "A-III, B-II, C-IV, D-I"], "C"),
  "History of electromagnetic waves (NCERT introduction to the chapter)",
  "Maxwell added the displacement current to Ampere's law and showed that the equations predict electromagnetic "
  "waves. Hertz demonstrated such waves experimentally in 1887. J. C. Bose, working in Calcutta, produced and "
  "observed waves of much shorter wavelength (25 mm to 5 mm). Marconi transmitted electromagnetic waves over "
  "distances of many kilometres.",
  ["Maxwell → III", "Hertz → IV", "Bose → II", "Marconi → I"],
  why="The other codes swap the theoretical prediction (Maxwell) with the first experiment (Hertz), or swap the "
      "short-wavelength work of Bose with Marconi's long-distance transmission.",
  ncert=EWC + "introduction", seconds=45)

r_in, r_out = F(1, 2), F(3)          # in units of the plate radius R
B_in = r_in                           # µ₀ i r/(2πR²), in units of µ₀i/(2πR)
B_out = 1 / r_out                     # µ₀ i/(2πr), same units
assert B_in / B_out == F(3, 2) and r_in / r_out == F(1, 6) and (1 / r_in) / (1 / r_out) == 6
q(EMW, "Displacement current", "Advanced", "numerical",
  "A parallel-plate capacitor with circular plates of radius R is being charged by a steady current. Neglect edge "
  "effects, so that the uniform, changing electric field exists only in the cylindrical region between the plates. "
  "In the plane midway between the plates, the ratio of the magnitude of the magnetic field at a distance R/2 from "
  "the axis to that at a distance 3R from the axis is:",
  *opt("3 : 2", ["1 : 6", "6 : 1", "2 : 3"], "D"),
  "Ampere–Maxwell law: ∮B·dl = µ₀ i_d, where i_d = ε₀ dΦ_E/dt is the displacement current enclosed by the loop",
  "Take circular loops coaxial with the plates. The displacement current, equal to the charging current i, is spread "
  "uniformly over the plate area. A loop of radius r < R encloses the fraction r²/R² of it; a loop of radius r > R "
  "encloses all of it.",
  ["r = R/2: B × 2π(R/2) = µ₀ i (1/4) → B = µ₀i/(4πR)", "r = 3R: B × 2π(3R) = µ₀ i → B = µ₀i/(6πR)",
   "Ratio = (1/4)/(1/6) = 3 : 2"],
  why="1 : 6 assumes B ∝ r at both points, as if the changing field filled the whole plane. 6 : 1 assumes B ∝ 1/r "
      "at both points, as if all of the displacement current were enclosed even at R/2. 2 : 3 inverts the answer.",
  ncert=EWC + "displacement current", seconds=100, rc=True)


# ================================================================ Optics (B6 I9 A6)
ROC = NC + "'Ray Optics and Optical Instruments', "
WOC = NC + "'Wave Optics', "


def lens_v(u, f):
    """Thin lens, Cartesian convention: 1/v − 1/u = 1/f."""
    return 1 / (1 / F(f) + 1 / F(u))


def mirror_v(u, f):
    """Spherical mirror, Cartesian convention: 1/v + 1/u = 1/f."""
    return 1 / (1 / F(f) - 1 / F(u))


# ---- Basic
assert 2 * 10 == 20
q(OPT, "Mirrors", "Basic", "numerical",
  "A ray of light falls on a plane mirror. Keeping the incident ray fixed, the mirror is rotated through 10° about an "
  "axis lying in its plane and perpendicular to the plane of incidence. The reflected ray turns through:",
  *opt("20°", ["10°", "5°", "40°"], "A"),
  "Laws of reflection: angle of incidence = angle of reflection, both measured from the normal",
  "Rotating the mirror through θ rotates its normal through θ. The angle of incidence therefore changes by θ, and so "
  "does the angle of reflection; the angle between the incident and reflected rays (2i) changes by 2θ. Since the "
  "incident ray is fixed, the reflected ray turns through 2θ.",
  ["Normal turns through 10°", "i changes by 10°, so 2i changes by 20°", "Reflected ray turns through 20°"],
  why="10° is the rotation of the mirror (and of its normal), not of the reflected ray. 5° halves instead of "
      "doubling. 40° doubles twice.",
  ncert=ROC + "reflection of light by spherical mirrors (laws of reflection)", seconds=30, rc=True)

f_b = 1 / F(4) * 100          # cm
v_b = lens_v(-50, f_b)
assert f_b == 25 and v_b == 50 and v_b / -50 == -1
assert 1 / (F(4) + 2) * 100 == F(50, 3)
q(OPT, "Refraction and lenses", "Basic", "numerical",
  "A thin lens has a power of +4 D. An object is placed on its principal axis 50 cm in front of it. The image is "
  "formed:",
  *opt("50 cm behind the lens; real, inverted and of the same size as the object",
       ["about 16.7 cm behind the lens; real, inverted and diminished",
        "50 cm in front of the lens; virtual, erect and of the same size",
        "25 cm behind the lens, at its focus"], "C"),
  "Power P = 1/f (f in metres); thin lens formula 1/v − 1/u = 1/f",
  "A power of +4 D means a converging lens of focal length 1/4 m = 25 cm. The object at 50 cm is at 2f, so the image "
  "is at 2f on the other side, real, inverted and of the same size.",
  ["f = 1/P = 0.25 m = 25 cm", "1/v = 1/25 + 1/(−50) = 1/50 → v = +50 cm", "m = v/u = 50/(−50) = −1"],
  why="16.7 cm adds 1/50 to 1/25 instead of subtracting (sign error for u). The virtual-image option gets the sign "
      "of v wrong. 25 cm is where the image of a very distant object would form.",
  ncert=ROC + "power of a lens; thin lens formula", seconds=40, rc=True)

q(OPT, "Huygens' principle and interference", "Basic", "direct",
  "A point source of light is placed at the principal focus of a thin convex lens, on its axis. The wavefront of the "
  "light emerging from the lens is:",
  *opt("plane", ["spherical, diverging from the focus on the other side", "spherical, converging to a point",
                 "cylindrical"], "D"),
  "Wavefronts and rays: rays are normal to the wavefront",
  "Light from a point source at the focus of a convex lens emerges as a parallel beam. Rays of a parallel beam are "
  "all perpendicular to a plane, so the emerging wavefront is plane.",
  ["Source at F → emergent rays parallel to the axis", "Parallel rays ↔ plane wavefront"],
  why="A spherical wavefront (diverging or converging) would need the rays to spread out from, or meet at, a point. "
      "A cylindrical wavefront comes from a line source, not a point source.",
  ncert=WOC + "Huygens' principle", seconds=30)

q(OPT, "Optical instruments", "Basic", "assertion_reason",
  ar("The final image seen through an astronomical (refracting) telescope is inverted with respect to the object.",
     "The objective forms a real, inverted image of the distant object, and the eyepiece, acting as a simple "
     "magnifier, forms an enlarged virtual image of that intermediate image without inverting it again."),
  AR, ar_key(True, True, True),
  "Image formation in an astronomical telescope",
  "The objective, a converging lens, forms a real inverted image of the distant object at its focus. The eyepiece "
  "views this image as a magnifying glass: a simple magnifier gives an erect (non-inverted) virtual image of what it "
  "views. So the single inversion by the objective remains in the final image. R is the reason for A.",
  ["Objective: real, inverted image", "Eyepiece: virtual, erect image of that image", "Net: inverted → R explains A"],
  why="R explains A directly; it is not a separate fact about telescopes.",
  ncert=ROC + "optical instruments: telescope", seconds=40)

q(OPT, "Mirrors", "Basic", "statement_pair",
  sp("The laws of reflection hold at every point of a curved mirror, the normal at the point of incidence being "
     "along the radius of curvature through that point.",
     "The mirror formula 1/v + 1/u = 1/f applies only to concave mirrors; a convex mirror needs a different "
     "formula."),
  SP, sp_key(True, False),
  "Reflection by spherical mirrors; mirror equation with the Cartesian sign convention",
  "NCERT states that the laws of reflection are true for any reflecting surface, plane or curved; for a spherical "
  "mirror the normal is along the radius. So Statement I is true. With the Cartesian sign convention the same "
  "mirror equation applies to both concave and convex mirrors (f is negative for a concave mirror and positive for "
  "a convex one), so Statement II is false.",
  ["I: true", "II: one formula for both mirrors, with signs → false"],
  why="Statement II forgets that the sign convention lets a single equation cover both kinds of mirror.",
  ncert=ROC + "the mirror equation", seconds=35)

lam_b = 600e-9
pd4 = (2 * 4 - 1) / 2 * lam_b
close(pd4, 2.1e-6)
q(OPT, "Huygens' principle and interference", "Basic", "numerical",
  "In a Young's double-slit experiment with light of wavelength 600 nm, the path difference between the waves "
  "reaching the fourth dark fringe (counted from the central bright fringe, on one side) from the two slits is:",
  *opt("2.1 µm", ["2.4 µm", "2.7 µm", "1.8 µm"], "B"),
  "Dark fringe: path difference = (2n − 1)λ/2, n = 1, 2, 3, ...",
  "The first dark fringe has a path difference λ/2, the second 3λ/2, the third 5λ/2 and the fourth 7λ/2.",
  ["Fourth dark fringe: Δ = 7λ/2 = 3.5λ", "Δ = 3.5 × 600 nm = 2100 nm = 2.1 µm"],
  why="2.4 µm (4λ) is the path difference for the fourth bright fringe. 2.7 µm (9λ/2) is for the fifth dark "
      "fringe. 1.8 µm (3λ) is for the third bright fringe.",
  ncert=WOC + "interference of light waves and Young's experiment", seconds=35, rc=True)

# ---- Intermediate
fc = F(20)
x_obj = 40
assert fc / (fc + x_obj) == F(1, 3) and fc / 60 == F(1, 3)
v_c = mirror_v(-x_obj, fc)
assert v_c == F(40, 3) and -v_c / -x_obj == F(1, 3)
assert mirror_v(-80, -20) == F(-80, 3) and -mirror_v(-80, -20) / -80 == F(-1, 3)
q(OPT, "Mirrors", "Intermediate", "numerical",
  "A convex mirror has a radius of curvature of 40 cm. For a real object on its axis, the image formed is one-third "
  "the size of the object. The distance of the object from the mirror is:",
  *opt("40 cm", ["60 cm", "20 cm", "80 cm"], "D"),
  "Mirror equation and magnification m = −v/u = f/(f − u)",
  "With the Cartesian convention f = +20 cm for the convex mirror and u = −x. The image of a real object in a "
  "convex mirror is virtual and erect, so m = +1/3.",
  ["m = f/(f − u) = 20/(20 + x) = 1/3", "20 + x = 60 → x = 40 cm",
   "Check: 1/v = 1/20 + 1/40 → v = +13.3 cm; m = −v/u = 13.3/40 = 1/3"],
  why="60 cm uses m = f/u. 20 cm puts the object at the focal length. 80 cm treats the mirror as concave (f = −20 cm) "
      "giving a real inverted image of one-third size.",
  ncert=ROC + "the mirror equation; magnification", seconds=60, rc=True)

i_p = deg(math.asin(math.sqrt(2) * math.sin(rad(30))))
close(i_p, 45)
close(deg(math.asin(0.5 / math.sqrt(2))), 20.7, 1e-2)
q(OPT, "Prism", "Intermediate", "numerical",
  "A ray of light falls on one refracting face of a prism of refracting angle 30°, made of glass of refractive index "
  "√2, and emerges from the second refracting face along its normal. The angle of incidence on the first face is:",
  *opt("45°", ["30°", "about 21°", "60°"], "B"),
  "Refraction through a prism: r₁ + r₂ = A; Snell's law at each face",
  "The ray leaves the second face along the normal, so the angle of refraction inside at the second face is r₂ = 0. "
  "Then r₁ = A − r₂ = 30°, and Snell's law at the first face gives the angle of incidence.",
  ["r₂ = 0 → r₁ = A = 30°", "sin i = √2 sin 30° = 1/√2", "i = 45° (deviation = i + 0 − A = 15°)"],
  why="30° takes the angle inside the glass (r₁) as the angle of incidence. 'About 21°' divides by √2 instead of "
      "multiplying (sin i = sin 30°/√2). 60° is just 2A.",
  ncert=ROC + "refraction through a prism", seconds=60, rc=True)

t_s, n_s, lam_s = 6e-6, 1.5, 600e-9
N_shift = (n_s - 1) * t_s / lam_s
close(N_shift, 5)
close(n_s * t_s / lam_s, 15)
q(OPT, "Huygens' principle and interference", "Intermediate", "numerical",
  "In a Young's double-slit experiment with light of wavelength 600 nm, one of the slits is covered by a thin "
  "transparent sheet of thickness 6.0 µm and refractive index 1.5. The interference pattern on the screen shifts "
  "through:",
  *opt("5 fringes, towards the side of the covered slit",
       ["5 fringes, away from the side of the covered slit", "15 fringes, towards the side of the covered slit",
        "10 fringes, towards the side of the covered slit"], "C"),
  "Optical path: a thickness t of a medium of refractive index n adds (n − 1)t to the path compared with air",
  "Light through the covered slit gains an extra optical path (n − 1)t. The central bright fringe, where the two "
  "optical paths are equal, moves to a point that is geometrically nearer the covered slit, so the whole pattern "
  "shifts towards that side. Each fringe width of shift corresponds to a path change of one wavelength.",
  ["Extra optical path = (1.5 − 1) × 6.0 µm = 3.0 µm", "Number of fringes = 3.0 µm / 0.60 µm = 5",
   "Shift is towards the covered slit"],
  why="'Away from the covered slit' reverses the direction: the extra path through the sheet must be compensated by "
      "a shorter geometrical path from that slit. 15 fringes uses nt instead of (n − 1)t. 10 fringes uses t alone.",
  ncert=WOC + "interference of light waves and Young's experiment", seconds=75, rc=True)

thetas = [k * math.pi / 180 for k in range(0, 91)]
I_mid = [0.5 * math.cos(t) ** 2 * math.sin(t) ** 2 for t in thetas]
best = max(range(91), key=lambda k: I_mid[k])
assert best == 45 and math.isclose(I_mid[45], 1 / 8)
q(OPT, "Polarisation", "Intermediate", "numerical",
  "Unpolarised light of intensity I₀ falls on two ideal polaroids whose pass axes are crossed (at 90°), so that no "
  "light emerges. A third ideal polaroid is inserted between them, and its pass axis is turned in its own plane. "
  "The greatest intensity of light that can now emerge from the last polaroid, and the angle between the pass axes "
  "of the first and the middle polaroid when this happens, are:",
  *opt("I₀/8, at 45°", ["I₀/4, at 45°", "I₀/2, at 0°", "I₀/2, at 45°"], "D"),
  "Malus's law I = I' cos²θ; unpolarised light loses half its intensity at the first polaroid",
  "After the first polaroid the intensity is I₀/2. If the middle polaroid's axis makes θ with the first, the "
  "intensity after it is (I₀/2)cos²θ, and after the last (axis at 90° − θ to the middle one) it is "
  "(I₀/2)cos²θ sin²θ = (I₀/8) sin²2θ.",
  ["I = (I₀/2) cos²θ sin²θ = (I₀/8) sin²2θ", "Maximum when sin 2θ = 1, i.e. θ = 45°", "I_max = I₀/8"],
  why="I₀/4 forgets that unpolarised light is halved by the first polaroid. At 0° the middle polaroid is parallel "
      "to the first and crossed with the last, so nothing emerges, not I₀/2. I₀/2 at 45° ignores the losses at the "
      "second and third polaroids.",
  ncert=WOC + "polarisation", seconds=80, rc=True)

C_w = deg(math.asin(3 / 4))
close(C_w, 48.6, 1e-2)
q(OPT, "Total internal reflection", "Intermediate", "direct",
  "A fish looks up from some depth below the calm surface of a pond (refractive index of water 4/3). Light from the "
  "entire sky above the water reaches the fish's eye only from within a cone whose axis is vertical. The "
  "semi-vertical angle of this cone is about:",
  *opt("49°, the critical angle for water", ["41°, the complement of the critical angle",
                                             "37°", "90°, since light arrives from the whole sky"], "B"),
  "Refraction at a plane surface; critical angle sin C = 1/n",
  "Light from the sky enters the water at angles of incidence from 0° to almost 90° (grazing). By Snell's law the "
  "largest angle of refraction, for grazing incidence, is the critical angle C with sin C = 1/n = 3/4. So all the "
  "light from the sky reaches the fish within a cone of semi-vertical angle C ≈ 49°; outside it the fish sees light "
  "totally reflected from below the surface.",
  ["Grazing incidence (90°) → angle of refraction = C", "sin C = 3/4 → C ≈ 48.6° ≈ 49°"],
  why="41° is 90° − C, the angle measured from the surface rather than from the vertical. 37° is sin⁻¹(3/5), not "
      "related to n = 4/3. The sky is compressed into the cone by refraction; it does not fill the hemisphere as "
      "seen from under water.",
  ncert=ROC + "total internal reflection", seconds=60, rc=True)

q(OPT, "Refraction and lenses", "Intermediate", "assertion_reason",
  ar("A ray of light passing through the optical centre of a thin lens emerges without deviation.",
     "Near the optical centre the two surfaces of a thin lens are parallel to each other, so this part of the lens "
     "acts like a thin parallel-sided glass slab."),
  AR, ar_key(True, True, True),
  "The optical centre of a thin lens",
  "A parallel-sided slab does not change the direction of a ray; it only shifts it sideways, and the shift is "
  "negligible for a thin slab. At the optical centre the tangent planes to the two lens surfaces are parallel, so "
  "the lens behaves there like such a slab. R explains A.",
  ["A: ray through the optical centre is undeviated → true", "R: faces parallel near the centre → slab → true",
   "R explains A"],
  why="R is the reason for A, not an unrelated property of lenses.",
  ncert=ROC + "refraction by a lens", seconds=40)

q(OPT, "Total internal reflection", "Intermediate", "statement_pair",
  sp("Optical fibres are extensively used to transmit audio and video signals over long distances.",
     "Bundles of optical fibres used as light pipes allow doctors to examine internal organs such as the "
     "oesophagus, stomach and intestines."),
  SP, sp_key(True, True),
  "Applications of total internal reflection: optical fibres",
  "Both are uses of optical fibres described in NCERT. In each fibre, light is guided by repeated total internal "
  "reflection at the core–cladding boundary, so it can be carried round bends with little loss.",
  ["I: signal transmission → true", "II: light pipes for viewing internal organs → true"],
  why="Both statements are NCERT applications of optical fibres; neither is false.",
  ncert=ROC + "total internal reflection: optical fibres", seconds=30)

I_of = lambda frac: 4 * math.cos(math.pi * frac) ** 2      # Δ = frac × λ, I in units of I₀
close(I_of(0), 4)
close(I_of(1 / 6), 3)
close(I_of(1 / 4), 2)
assert abs(I_of(1 / 2)) < 1e-12
q(OPT, "Huygens' principle and interference", "Intermediate", "match_list",
  ml("In a Young's double-slit experiment the waves from the two slits reach the screen with equal intensities, each "
     "I₀. Match the path difference at a point of the screen (List-I) with the resultant intensity there (List-II).",
     ["0", "λ/6", "λ/4", "λ/2"],
     ["2I₀", "zero", "4I₀", "3I₀"]),
  *mlo("A-III, B-IV, C-I, D-II", ["A-III, B-I, C-IV, D-II", "A-I, B-IV, C-III, D-II", "A-III, B-II, C-I, D-IV"], "D"),
  "Resultant intensity I = 4I₀ cos²(φ/2) with phase difference φ = 2πΔ/λ",
  "A path difference Δ gives a phase difference φ = 2πΔ/λ, and for equal intensities the resultant is "
  "4I₀ cos²(φ/2) = 4I₀ cos²(πΔ/λ).",
  ["Δ = 0: 4I₀ cos² 0 = 4I₀", "Δ = λ/6: 4I₀ cos²(30°) = 3I₀", "Δ = λ/4: 4I₀ cos²(45°) = 2I₀",
   "Δ = λ/2: 4I₀ cos²(90°) = 0"],
  why="Swapping λ/6 and λ/4 confuses cos² 30° (3/4) with cos² 45° (1/2). Treating the maximum as 2I₀ adds "
      "intensities instead of amplitudes.",
  ncert=WOC + "coherent and incoherent addition of waves", seconds=70, rc=True)

truth = {"a": True, "b": True, "c": False, "d": True, "e": False}
q(OPT, "Huygens' principle and interference", "Intermediate", "multi_statement",
  ms("A Young's double-slit experiment is set up in air with monochromatic light. Each of the following changes is "
     "made separately, everything else being unchanged. Which of the following statements are correct?",
     ["Moving the screen farther from the slits increases the fringe width.",
      "Using light of shorter wavelength decreases the fringe width.",
      "Increasing the separation between the slits increases the fringe width.",
      "Covering one slit completely makes the interference fringes disappear; only the broad diffraction pattern "
      "of the other slit remains.",
      "Immersing the whole apparatus in water increases the fringe width."]),
  *mso(truth, "abd", ["abc", "bde", "ade"], "C"),
  "Fringe width β = λD/d; interference needs two coherent sources",
  "β = λD/d increases with D (a true), decreases with λ (b true) and decreases as d increases (c false). In water the "
  "wavelength becomes λ/n, so β decreases (e false). With one slit covered there is only one source, so there can be "
  "no two-source interference; the single slit gives its own diffraction pattern (d true).",
  ["(a) β ∝ D → true", "(b) β ∝ λ → true", "(c) β ∝ 1/d → false", "(d) true", "(e) λ → λ/n → β decreases → false"],
  why="Options with (c) or (e) reverse the dependence of β on d or on the medium.",
  ncert=WOC + "interference of light waves and Young's experiment", seconds=70)

# ---- Advanced
f1 = F(20)                                  # equiconvex, n = 1.5, R = 20 cm
f2 = -F(20) / (F(4, 3) - 1)                 # plano-concave water lens, R = 20 cm
Fc = 1 / (1 / f1 + 1 / f2)
assert f2 == -60 and Fc == 30 and 1 / (1 / f1 + 1 / F(60)) == 15
q(OPT, "Refraction and lenses", "Advanced", "numerical",
  "A thin equiconvex lens of glass (refractive index 1.5), each face of radius of curvature 20 cm, rests on a "
  "horizontal plane mirror. A little water (refractive index 4/3) is put between the lens and the mirror, so that it "
  "forms a thin layer bounded by the lower face of the lens and the flat mirror. Looking down along the axis, a pin "
  "held above the lens coincides with its own image (no parallax) when the pin is at a height h above the lens. The "
  "value of h is:",
  *opt("30 cm", ["15 cm", "20 cm", "60 cm"], "C"),
  "Lens maker's formula; lenses in contact; image coincides with the object when the light returns along its path",
  "The pin coincides with its image when the rays, after passing through the glass lens and the water layer, strike "
  "the mirror normally and retrace their path; that is when the pin is at the focus of the combination (glass lens + "
  "water lens). The water layer is a plano-concave lens with one face of radius 20 cm.",
  ["Glass lens: 1/f₁ = (1.5 − 1)(2/20) → f₁ = 20 cm",
   "Water lens: 1/f₂ = (4/3 − 1)(−1/20) → f₂ = −60 cm",
   "1/F = 1/20 − 1/60 = 1/30 → F = 30 cm = h"],
  why="15 cm adds the powers as if the water layer were converging. 20 cm ignores the water layer. 60 cm is the "
      "magnitude of the focal length of the water lens alone.",
  ncert=ROC + "lens maker's formula; combination of thin lenses in contact", seconds=140, rc=True)

v_near, v_far = mirror_v(-30, -20), mirror_v(-40, -20)
v_mid = mirror_v(-35, -20)
assert v_near == -60 and v_far == -40 and abs(v_near - v_far) == 20
assert (v_near / 30) ** 2 * 10 == 40 and round(float((v_mid / 35) ** 2 * 10), 1) == 17.8
q(OPT, "Mirrors", "Advanced", "numerical",
  "A thin rod 10 cm long lies along the principal axis of a concave mirror of focal length 20 cm, its nearer end "
  "being 30 cm from the pole and its farther end 40 cm from the pole. The length of the image of the rod is:",
  *opt("20 cm", ["40 cm", "10 cm", "about 17.8 cm"], "A"),
  "Mirror equation applied to each end of an extended object along the axis",
  "For an object along the axis the magnification is not the same at every point, so find the image of each end "
  "separately. The end at 40 cm (= 2f, the centre of curvature) images onto itself.",
  ["Near end: 1/v = −1/20 + 1/30 → v = −60 cm", "Far end: 1/v = −1/20 + 1/40 → v = −40 cm",
   "Image length = 60 − 40 = 20 cm"],
  why="40 cm uses m² × 10 cm with m = 2, the magnification at the near end only. 10 cm assumes the image is the same "
      "length. 17.8 cm uses m² with the magnification at the middle of the rod; that approximation is valid only for "
      "a very short object.",
  ncert=ROC + "the mirror equation", seconds=120, rc=True)

h_eye, depth, n_w = F(30), F(40), F(4, 3)
app_mirror = h_eye + depth / n_w
assert app_mirror == 60 and 2 * app_mirror == 120 and 2 * (h_eye + depth) == 140 and 2 * h_eye + depth == 100
q(OPT, "Refraction and lenses", "Advanced", "numerical",
  "A tank contains water (refractive index 4/3) 40 cm deep, and a plane mirror lies flat on its bottom. A person "
  "looks vertically down at the mirror, his eye being 30 cm above the water surface. Using the near-normal "
  "(paraxial) approximation, the distance from his eye at which he sees the image of his own eye is:",
  *opt("120 cm", ["140 cm", "60 cm", "100 cm"], "B"),
  "Apparent depth (real depth/n) for near-normal viewing; image in a plane mirror",
  "Seen from the air, the mirror on the bottom appears raised to an apparent depth of 40/(4/3) = 30 cm below the "
  "surface, i.e. 60 cm below the eye. The light travels down and back up through the same water, so the eye sees "
  "itself as in a plane mirror placed at this apparent position: the image lies as far behind the apparent mirror "
  "as the eye is in front of it.",
  ["Apparent depth of mirror = 40 × 3/4 = 30 cm", "Eye to apparent mirror = 30 + 30 = 60 cm",
   "Image of eye is 60 cm behind it → 120 cm from the eye"],
  why="140 cm ignores refraction and doubles the actual distance 70 cm. 60 cm is the distance to the apparent "
      "mirror, not to the image. 100 cm applies the refraction correction to neither water path.",
  ncert=ROC + "refraction (real and apparent depth)", seconds=120, rc=True)

v1, v2 = lens_v(-30, 20), F(80)
f_conc = 1 / (1 / v2 - 1 / v1)
assert v1 == 60 and f_conc == -240
q(OPT, "Refraction and lenses", "Advanced", "numerical",
  "A thin convex lens of focal length 20 cm forms a sharp image of an object, placed 30 cm in front of it, on a "
  "screen. A thin concave lens is now placed in contact with the convex lens, and the screen has to be moved 20 cm "
  "farther from the lenses to obtain a sharp image again (the object stays where it was). The focal length of the "
  "concave lens is:",
  *opt("−240 cm", ["−20 cm", "+240 cm", "about −34 cm"], "C"),
  "Thin lens formula; lenses in contact: 1/F = 1/f₁ + 1/f₂",
  "First the convex lens alone: the image is at v = 60 cm. With the concave lens added, the image is at 80 cm. For the "
  "same object distance, 1/v − 1/u = 1/F, so the change in 1/v equals the power added by the concave lens.",
  ["Convex lens alone: 1/v = 1/20 − 1/30 → v = 60 cm", "Combination: v' = 80 cm",
   "1/f₂ = 1/v' − 1/v = 1/80 − 1/60 = −1/240 → f₂ = −240 cm"],
  why="−20 cm takes the shift of the screen as the focal length. +240 cm gets the sign wrong; adding a converging lens "
      "would bring the image closer. About −34 cm adds 1/80 and 1/60.",
  ncert=ROC + "combination of thin lenses in contact", seconds=110, rc=True)

nn = math.sqrt(3)
ib = deg(math.atan(nn))
close(ib, 60)
close(90 - ib, 30)
close(deg(math.asin(1 / nn)), 35.26)
close((nn - 1) * 6, 4.39)
q(OPT, "Polarisation", "Advanced", "match_list",
  ml("A transparent material has refractive index √3 (about 1.73) and is used in air. Match each quantity in List-I "
     "with its value in List-II.",
     ["Angle of incidence (in air) at which the reflected light is completely plane polarised",
      "Angle of refraction (in the material) for light incident at that angle",
      "Critical angle for light going from the material into air",
      "Deviation produced by a thin prism of this material with a refracting angle of 6°"],
     ["30°", "60°", "about 35°", "about 4.4°"]),
  *mlo("A-II, B-I, C-III, D-IV", ["A-I, B-II, C-III, D-IV", "A-II, B-I, C-IV, D-III", "A-III, B-I, C-II, D-IV"], "B"),
  "Brewster's law tan i_B = n; reflected and refracted rays perpendicular at i_B; sin C = 1/n; thin prism δ = (n − 1)A",
  "tan i_B = √3 gives i_B = 60°. At Brewster's angle the reflected and refracted rays are perpendicular, so the "
  "angle of refraction is 90° − 60° = 30°. sin C = 1/√3 gives C ≈ 35.3°. A thin prism deviates light by "
  "(n − 1)A = 0.732 × 6° ≈ 4.4°.",
  ["A → 60° (II)", "B → 30° (I)", "C → about 35° (III)", "D → about 4.4° (IV)"],
  why="Swapping A and B confuses the Brewster angle with the refraction angle. The other codes mix up the critical "
      "angle with the prism deviation.",
  ncert=WOC + "polarisation by reflection; " + "Ray Optics: critical angle, refraction through a prism", seconds=100,
  rc=True)

us = [-60, -40, -30]
vs = [lens_v(u, 20) for u in us]
ms_ = [v / u for v, u in zip(vs, us)]
assert vs == [30, 40, 60] and ms_ == [F(-1, 2), -1, -2]
assert (ms_[0] ** 2 < 1) and (ms_[2] ** 2 > 1)          # image slower at 60 cm, faster at 30 cm
truth = {"a": True, "b": True, "c": True, "d": False, "e": True}
q(OPT, "Refraction and lenses", "Advanced", "multi_statement",
  ms("An object is moved steadily along the principal axis of a thin convex lens of focal length 20 cm, from a "
     "distance of 60 cm to a distance of 30 cm from the lens. During this motion, which of the following statements "
     "are correct?",
     ["The image moves away from the lens, from 30 cm to 60 cm behind it.",
      "The image grows from half the size of the object to twice its size.",
      "The image stays real and inverted.",
      "Throughout the motion, the image moves more slowly than the object.",
      "When the object is 40 cm from the lens, the image is of the same size as the object."]),
  *mso(truth, "abce", ["abcd", "ace", "bcde"], "A"),
  "Thin lens formula; magnification; speed of the image along the axis = m² × speed of the object",
  "With f = 20 cm: u = −60 gives v = 30 cm (m = −½), u = −40 gives v = 40 cm (m = −1) and u = −30 gives v = 60 cm "
  "(m = −2). The object stays beyond f, so the image is real and inverted throughout. Differentiating the lens "
  "formula gives (image speed) = m² × (object speed): slower than the object while |m| < 1 (object beyond 2f) but "
  "faster once |m| > 1 (object between f and 2f), so (d) is false.",
  ["(a) v: 30 → 60 cm → true", "(b) |m|: ½ → 2 → true", "(c) object beyond f → real, inverted → true",
   "(d) speed ratio m²: ¼ → 4 → false", "(e) u = 2f → |m| = 1 → true"],
  why="Options with (d) ignore that the image speeds up once the magnification exceeds 1; the options leaving out "
      "(a) or (b) miss changes that follow directly from the lens formula.",
  ncert=ROC + "thin lens formula; magnification", seconds=110, rc=True)


# ================================================================ Dual Nature of Matter and Radiation (B3 I4 A3)
DNC = NC + "'Dual Nature of Radiation and Matter', "

# ---- Basic
h_ = 6.6e-34
lam_ball = h_ / (0.05 * 30)
close(lam_ball, 4.4e-34)
close(h_ / (50 * 30), 4.4e-37)
close(h_ / 0.05, 1.32e-32)
q(DUAL, "de Broglie wavelength", "Basic", "numerical",
  "A ball of mass 50 g is thrown with a speed of 30 m/s. Taking h = 6.6 × 10⁻³⁴ J s, its de Broglie wavelength is:",
  *opt("4.4 × 10⁻³⁴ m", ["4.4 × 10⁻³⁷ m", "1.3 × 10⁻³² m", "2.3 × 10³³ m"], "B"),
  "de Broglie relation λ = h/p = h/(mv)",
  "The momentum of the ball is p = mv = 0.050 kg × 30 m/s = 1.5 kg m/s. Its de Broglie wavelength is far too small "
  "to be detected, which is why a ball shows no wave behaviour.",
  ["p = 0.050 × 30 = 1.5 kg m s⁻¹", "λ = 6.6 × 10⁻³⁴/1.5 = 4.4 × 10⁻³⁴ m"],
  why="4.4 × 10⁻³⁷ m keeps the mass in grams. 1.3 × 10⁻³² m divides h by the mass only, leaving out the speed. "
      "2.3 × 10³³ m is p/h, the inverse of the correct ratio.",
  ncert=DNC + "wave nature of matter", seconds=30, rc=True)

q(DUAL, "Photoelectric effect", "Basic", "assertion_reason",
  ar("A photon of violet light carries more momentum than a photon of red light.",
     "The momentum of a photon is p = hν/c = h/λ, and violet light has a higher frequency (shorter wavelength) than "
     "red light."),
  AR, ar_key(True, True, True),
  "Photon picture of light: energy hν and momentum hν/c",
  "Each photon of frequency ν carries momentum hν/c. Violet light has a higher frequency than red light, so each "
  "violet photon carries more momentum. R is the reason for A.",
  ["p = hν/c", "ν_violet > ν_red → p_violet > p_red", "R explains A"],
  why="R is the direct reason; it is not an unrelated statement about photons.",
  ncert=DNC + "Einstein's photoelectric equation: energy quantum of radiation; particle nature of light: the photon",
  seconds=30)

q(DUAL, "Einstein's equation", "Basic", "statement_pair",
  sp("Millikan's careful experiments on the photoelectric effect verified Einstein's photoelectric equation and gave "
     "an accurate value of Planck's constant.",
     "Einstein's photoelectric equation predicts that the maximum kinetic energy of the photoelectrons increases "
     "linearly with the intensity of the incident light."),
  SP, sp_key(True, False),
  "Einstein's photoelectric equation K_max = hν − φ₀ and its experimental verification",
  "NCERT records that Millikan's photoelectric experiments (1906–1916) verified Einstein's equation and gave an "
  "accurate value of h, so Statement I is true. The equation K_max = hν − φ₀ contains no intensity at all: K_max "
  "depends linearly on the frequency, not on the intensity. Statement II is false.",
  ["I: true", "II: K_max = hν − φ₀ depends on ν, not on intensity → false"],
  why="Statement II replaces frequency by intensity, which is the prediction of the wave picture that the photoelectric "
      "effect contradicts.",
  ncert=DNC + "Einstein's photoelectric equation", seconds=35)

# ---- Intermediate
hc_l, phi_ = F(10), F(2)          # hc/λ = 10 units, φ = 2 units (any example)
V1 = hc_l - phi_
V2 = 2 * hc_l - phi_
assert V2 == 2 * V1 + phi_ and V2 > 2 * V1
q(DUAL, "Einstein's equation", "Intermediate", "direct",
  "Monochromatic light of wavelength λ falls on a metal surface and the stopping potential is V₀. If light of "
  "wavelength λ/2 is used instead, the stopping potential becomes:",
  *opt("more than 2V₀", ["exactly 2V₀", "more than V₀ but less than 2V₀", "V₀/2"], "C"),
  "Einstein's photoelectric equation eV₀ = hc/λ − φ₀",
  "Halving the wavelength doubles the photon energy, but the work function stays the same, so the stopping potential "
  "more than doubles.",
  ["eV₀ = hc/λ − φ₀", "eV₀' = 2hc/λ − φ₀ = 2(hc/λ − φ₀) + φ₀ = 2eV₀ + φ₀", "V₀' = 2V₀ + φ₀/e > 2V₀"],
  why="'Exactly 2V₀' assumes V₀ is proportional to the photon energy, forgetting the work function. 'Less than 2V₀' "
      "subtracts the work function twice. V₀/2 treats V₀ as proportional to λ.",
  ncert=DNC + "Einstein's photoelectric equation", seconds=50, rc=True)

E_ph = F(136, 10) * (1 - F(1, 4))
K_ = E_ph - F(42, 10)
assert E_ph == F(102, 10) and K_ == 6 and E_ph + F(42, 10) == F(144, 10) and F(136, 10) - F(42, 10) == F(94, 10)
q(DUAL, "Einstein's equation", "Intermediate", "numerical",
  "The energy of the electron in the nth orbit of the hydrogen atom is −13.6/n² eV. Photons emitted when hydrogen "
  "atoms make transitions from n = 2 to n = 1 fall on a metal surface of work function 4.2 eV. The stopping potential "
  "for the photoelectrons is:",
  *opt("6.0 V", ["10.2 V", "14.4 V", "9.4 V"], "D"),
  "Photon energy from an atomic transition; Einstein's equation eV₀ = hν − φ₀",
  "The photon carries the energy difference of the two levels. The fastest photoelectron leaves with that energy minus "
  "the work function, and the stopping potential (in volts) equals that kinetic energy in eV.",
  ["hν = E₂ − E₁ = −3.4 − (−13.6) = 10.2 eV", "K_max = 10.2 − 4.2 = 6.0 eV", "V₀ = 6.0 V"],
  why="10.2 V ignores the work function. 14.4 V adds the work function instead of subtracting it. 9.4 V takes the "
      "photon energy as the full ionisation energy 13.6 eV.",
  ncert=DNC + "Einstein's photoelectric equation", seconds=60, rc=True)

q(DUAL, "Einstein's equation", "Intermediate", "match_list",
  ml("Graphs are drawn from photoelectric data for one metal: the stopping potential V₀ against the frequency ν, and "
     "the maximum kinetic energy K_max against ν. Match each feature in List-I with what it gives in List-II.",
     ["Slope of the V₀–ν graph", "Intercept of the V₀–ν line on the ν axis",
      "Intercept of the extended K_max–ν line on the K_max axis", "Slope of the K_max–ν graph"],
     ["h", "h/e", "the threshold frequency ν₀", "−φ₀ (minus the work function)"]),
  *mlo("A-II, B-III, C-IV, D-I", ["A-I, B-III, C-IV, D-II", "A-II, B-IV, C-III, D-I", "A-II, B-III, C-I, D-IV"], "B"),
  "Einstein's equation as a straight line: K_max = hν − φ₀ and V₀ = (h/e)ν − φ₀/e",
  "K_max = hν − φ₀ is a straight line of slope h that cuts the K_max axis at −φ₀. Dividing by e, V₀ = (h/e)ν − φ₀/e has "
  "slope h/e, and V₀ = 0 at ν = φ₀/h = ν₀, the threshold frequency.",
  ["A → h/e (II)", "B → ν₀ (III)", "C → −φ₀ (IV)", "D → h (I)"],
  why="Swapping the two slopes forgets the factor e between the energy (K_max) and the potential (V₀). The other "
      "codes confuse the frequency-axis intercept (ν₀) with the energy-axis intercept (−φ₀).",
  ncert=DNC + "experimental study of photoelectric effect; Einstein's photoelectric equation", seconds=60)

Kmax_e = F(3) - F(2)
assert Kmax_e + F(3, 2) == F(5, 2) and 0 + F(3, 2) == F(3, 2)
q(DUAL, "Einstein's equation", "Intermediate", "numerical",
  "Photons of energy 3.0 eV fall on the emitter of a photocell, whose work function is 2.0 eV. The collector is kept "
  "at a potential of +1.5 V with respect to the emitter. The kinetic energies of the photoelectrons arriving at the "
  "collector lie in the range:",
  *opt("1.5 eV to 2.5 eV", ["0 to 1.0 eV", "0 to 2.5 eV", "exactly 2.5 eV for every electron"], "C"),
  "Photoelectrons leave with kinetic energies from 0 to K_max; an accelerating potential adds eV to each",
  "Electrons leave the emitter with kinetic energies from zero up to K_max = 3.0 − 2.0 = 1.0 eV. The collector is "
  "1.5 V higher, so every electron gains 1.5 eV on the way.",
  ["K at emitter: 0 to 1.0 eV", "Gain from accelerating potential: +1.5 eV", "K at collector: 1.5 eV to 2.5 eV"],
  why="'0 to 1.0 eV' ignores the accelerating potential. '0 to 2.5 eV' adds 1.5 eV only to the fastest electrons. "
      "Photoelectrons are not all emitted with K_max, so they do not all arrive with 2.5 eV.",
  ncert=DNC + "experimental study of photoelectric effect: effect of potential on photoelectric current",
  seconds=60, rc=True)

# ---- Advanced
nu0 = F(1)
K = lambda nu: nu - nu0                     # in units of hν₀
assert K(3) == 2 * K(2) and K(4) == 3 * K(2)
truth = {"a": True, "b": True, "c": True, "d": False, "e": False}
q(DUAL, "Photoelectric effect", "Advanced", "multi_statement",
  ms("Monochromatic light of frequency 2ν₀, where ν₀ is the threshold frequency of a metal, falls on it and gives a "
     "stopping potential V₀ and a saturation current I_s. Each change below is made separately, the other conditions "
     "being kept as they were. Which of the following statements are correct?",
     ["If the frequency is raised to 3ν₀ (the number of photons falling per second unchanged), the stopping potential "
      "becomes 2V₀.",
      "If the number of photons falling per second is doubled (frequency unchanged), the saturation current becomes "
      "2I_s.",
      "If the frequency is raised to 4ν₀, the maximum kinetic energy of the photoelectrons becomes three times its "
      "original value.",
      "If the number of photons falling per second is doubled (frequency unchanged), the stopping potential becomes "
      "2V₀.",
      "If the frequency is lowered to 0.9ν₀, a small photocurrent still flows provided the light is intense "
      "enough."]),
  *mso(truth, "abc", ["abd", "bce", "acd"], "B"),
  "Einstein's equation K_max = h(ν − ν₀); saturation current ∝ number of photons per second",
  "eV₀ = h(ν − ν₀). At 2ν₀: eV₀ = hν₀. At 3ν₀: 2hν₀, i.e. 2V₀ (a). At 4ν₀: 3hν₀, three times (c). Each photon can "
  "free at most one electron, so the number of photoelectrons per second, and hence the saturation current, is "
  "proportional to the number of photons per second (b), while the stopping potential does not depend on it (d "
  "false). Below the threshold frequency no photoelectrons are emitted however intense the light (e false).",
  ["(a) h(3ν₀ − ν₀) = 2hν₀ → 2V₀ → true", "(b) true", "(c) h(4ν₀ − ν₀) = 3hν₀ → true",
   "(d) V₀ independent of photon flux → false", "(e) ν < ν₀ → no emission → false"],
  why="Options with (d) let the photon flux change the stopping potential; options with (e) ignore the threshold "
      "frequency.",
  ncert=DNC + "experimental study of photoelectric effect; Einstein's photoelectric equation", seconds=100,
  rc=True)

E_J = 10.2 * 1.6e-19
v_rec = E_J / (1.67e-27 * 3e8)
close(v_rec, 3.26, 1e-2)
close(2 * v_rec, 6.5, 1e-2)
close(math.sqrt(2 * E_J / 1.67e-27), 4.42e4, 1e-2)
q(DUAL, "Photoelectric effect", "Advanced", "numerical",
  "A hydrogen atom, initially at rest, emits a photon of energy 10.2 eV. Taking the mass of the atom as "
  "1.67 × 10⁻²⁷ kg, 1 eV = 1.6 × 10⁻¹⁹ J and c = 3 × 10⁸ m/s, the speed with which the atom recoils is about:",
  *opt("3.3 m/s", ["6.5 m/s", "4.4 × 10⁴ m/s", "zero, since a photon has no mass and carries no momentum"], "D"),
  "Photon momentum p = E/c = hν/c; conservation of momentum",
  "Before the emission the total momentum is zero. The photon carries away momentum E/c, so the atom recoils with an "
  "equal and opposite momentum: m v = E/c.",
  ["E = 10.2 × 1.6 × 10⁻¹⁹ = 1.63 × 10⁻¹⁸ J", "p = E/c = 5.44 × 10⁻²⁷ kg m s⁻¹",
   "v = p/m = 5.44 × 10⁻²⁷/1.67 × 10⁻²⁷ ≈ 3.3 m/s"],
  why="6.5 m/s uses 2E/c, the momentum change on reflection of a photon, not on emission. 4.4 × 10⁴ m/s gives all "
      "the photon's energy to the atom as kinetic energy. A photon has no rest mass but does carry momentum hν/c.",
  ncert=DNC + "particle nature of light: the photon", seconds=100, rc=True)

phi_m = F(2)
K1, K2 = F(4) - phi_m, F(8) - phi_m
assert K1 == 2 and K2 == 6 and K2 / K1 == 3
q(DUAL, "de Broglie wavelength", "Advanced", "numerical",
  "Photons of energy 4.0 eV, and then photons of energy 8.0 eV, fall on a metal of work function 2.0 eV. The ratio "
  "of the de Broglie wavelength of the fastest photoelectrons in the first case to that in the second case is:",
  *opt("√3 : 1", ["√2 : 1", "3 : 1", "1 : √3"], "A"),
  "Einstein's equation K_max = hν − φ₀; de Broglie wavelength λ = h/√(2mK) ∝ 1/√K",
  "Doubling the photon energy does not double K_max, because the work function is subtracted each time. For "
  "non-relativistic electrons λ ∝ 1/√K.",
  ["K₁ = 4.0 − 2.0 = 2.0 eV", "K₂ = 8.0 − 2.0 = 6.0 eV", "λ₁/λ₂ = √(K₂/K₁) = √3"],
  why="√2 : 1 assumes K_max doubles when the photon energy doubles. 3 : 1 is the ratio of the kinetic energies, not "
      "of the wavelengths. 1 : √3 inverts the ratio; the slower electrons have the longer wavelength.",
  ncert=DNC + "wave nature of matter", seconds=80, rc=True)


# ================================================================ Atoms and Nuclei (B4 I5 A4)
ATC = NC + "'Atoms', "
NUC = NC + "'Nuclei', "

# ---- Basic
avg = F(2, 10) * F(1001, 100) + F(8, 10) * F(1101, 100)
assert avg == F(1081, 100) and (F(1001, 100) + F(1101, 100)) / 2 == F(1051, 100)
assert F(8, 10) * F(1001, 100) + F(2, 10) * F(1101, 100) == F(1021, 100)
q(AN, "Nuclear size and mass defect", "Basic", "numerical",
  "Naturally occurring boron consists of two isotopes: ¹⁰B (atomic mass 10.01 u), making up 20% of the atoms, and "
  "¹¹B (atomic mass 11.01 u), making up 80%. The average atomic mass of natural boron is:",
  *opt("10.81 u", ["10.51 u", "10.21 u", "21.02 u"], "C"),
  "Atomic mass of an element = abundance-weighted average of the masses of its isotopes",
  "The average mass is found by weighting each isotope's mass by the fraction of atoms that are of that isotope.",
  ["Average = 0.20 × 10.01 + 0.80 × 11.01", "= 2.002 + 8.808 = 10.81 u"],
  why="10.51 u is the simple average, ignoring the abundances. 10.21 u swaps the two abundances. 21.02 u adds the "
      "two masses.",
  ncert=NUC + "atomic masses and composition of nucleus", seconds=35, rc=True)

q(AN, "Rutherford scattering", "Basic", "assertion_reason",
  ar("In the alpha-particle scattering experiment, the electrons of the gold atoms have practically no effect on the "
     "paths of the alpha particles.",
     "The mass of an electron is very small compared with that of an alpha particle, so an alpha particle hardly "
     "changes its direction when it collides with an electron."),
  AR, ar_key(True, True, True),
  "Interpretation of the alpha-particle scattering experiment",
  "An alpha particle is several thousand times heavier than an electron. In a collision with such a light particle "
  "it is deflected very little, just as a heavy ball is hardly deflected by striking a much lighter one. The large "
  "deflections must therefore be due to the heavy, positively charged nucleus. R is the reason for A.",
  ["A: true", "R: true", "Light electrons cannot appreciably deflect a heavy alpha particle → R explains A"],
  why="R directly explains A; it is not an unrelated property of electrons.",
  ncert=ATC + "alpha-particle scattering and Rutherford's nuclear model of atom", seconds=35)

q(AN, "Rutherford scattering", "Basic", "statement_pair",
  sp("In the Geiger–Marsden experiment, only about 0.14% of the incident alpha particles were scattered by more "
     "than 1°, and about 1 in 8000 was deflected by more than 90°.",
     "In Thomson's model of the atom, the positive charge is spread uniformly through the volume of the atom and the "
     "electrons are embedded in it, like seeds in a watermelon."),
  SP, sp_key(True, True),
  "Early models of the atom and the results of the scattering experiment",
  "Both statements are as given in NCERT. The tiny fraction scattered through large angles could not be explained "
  "by Thomson's model, in which the positive charge is spread out, and led Rutherford to propose a small, massive "
  "nucleus.",
  ["I: NCERT's figures for the scattering → true", "II: Thomson's (plum pudding) model → true"],
  why="Both statements are correct descriptions; neither is altered.",
  ncert=ATC + "introduction; alpha-particle scattering", seconds=35)

assert F(1, 2) == F(1) / 2
q(AN, "Rutherford scattering", "Basic", "direct",
  "An alpha particle is projected head-on towards a fixed heavy nucleus and comes momentarily to rest at a distance "
  "d from it. If the kinetic energy of the alpha particle is doubled, the distance of closest approach becomes:",
  *opt("d/2", ["2d", "d/√2", "d/4"], "D"),
  "Distance of closest approach: K = (1/4πε₀)(2e)(Ze)/d",
  "At the distance of closest approach the whole initial kinetic energy has become electrostatic potential energy, "
  "which varies as 1/d. So d is inversely proportional to the kinetic energy.",
  ["K = k(2e)(Ze)/d → d ∝ 1/K", "K → 2K gives d → d/2"],
  why="2d has the dependence inverted. d/√2 would follow if d varied as 1/√K. d/4 would follow if d varied as 1/K².",
  ncert=ATC + "alpha-particle trajectory; distance of closest approach", seconds=30, rc=True)

# ---- Intermediate
Ryd = 13.6 / 1240 * 1e9
close(Ryd, 1.097e7, 1e-3)
close(1240 / 13.6 * 1e-9, 9.12e-8, 1e-3)
close(13.6 / 1240 / 4 * 1e9, 2.74e6, 1e-2)
q(AN, "Bohr model and hydrogen spectrum", "Intermediate", "numerical",
  "In the Bohr model the energy levels of the hydrogen atom are E_n = −13.6/n² eV, and the wavelengths emitted obey "
  "1/λ = R(1/n_f² − 1/n_i²). Taking hc = 1240 eV nm, the value of the Rydberg constant R obtained from these is "
  "about:",
  *opt("1.1 × 10⁷ m⁻¹", ["9.1 × 10⁻⁸ m⁻¹", "1.1 × 10⁻² m⁻¹", "2.7 × 10⁶ m⁻¹"], "B"),
  "Bohr's frequency condition hc/λ = E_i − E_f = 13.6 eV (1/n_f² − 1/n_i²)",
  "Comparing hc/λ = 13.6 eV (1/n_f² − 1/n_i²) with 1/λ = R(1/n_f² − 1/n_i²) gives R = 13.6 eV/hc.",
  ["R = 13.6 eV / (1240 eV nm) = 0.01097 nm⁻¹", "1 nm⁻¹ = 10⁹ m⁻¹ → R ≈ 1.1 × 10⁷ m⁻¹"],
  why="9.1 × 10⁻⁸ m⁻¹ is the number 91.2 nm (hc/13.6 eV, the Lyman series limit) written with the wrong unit. "
      "1.1 × 10⁻² m⁻¹ leaves the answer in nm⁻¹ but labels it m⁻¹. 2.7 × 10⁶ m⁻¹ divides by an extra factor of 4.",
  ncert=ATC + "Bohr model; the line spectra of the hydrogen atom", seconds=60, rc=True)

E_e = 9.1e-31 * (3e8) ** 2 / 1.6e-13
close(E_e, 0.512, 1e-2)
q(AN, "Binding energy", "Intermediate", "numerical",
  "Taking the mass of the electron as 9.1 × 10⁻³¹ kg, c = 3 × 10⁸ m/s and 1 MeV = 1.6 × 10⁻¹³ J, the energy "
  "equivalent of the rest mass of an electron is about:",
  *opt("0.51 MeV", ["0.26 MeV", "931 MeV", "5.1 × 10⁵ MeV"], "D"),
  "Einstein's mass–energy relation E = mc²",
  "A mass m is equivalent to an energy mc². Convert joules to MeV at the end.",
  ["E = 9.1 × 10⁻³¹ × (3 × 10⁸)² = 8.19 × 10⁻¹⁴ J", "E = 8.19 × 10⁻¹⁴/1.6 × 10⁻¹³ ≈ 0.51 MeV"],
  why="0.26 MeV uses ½mc², a kinetic-energy expression. 931 MeV is the energy equivalent of 1 u, not of an electron. "
      "5.1 × 10⁵ MeV is the value in eV mislabelled as MeV.",
  ncert=NUC + "mass-energy and nuclear binding energy", seconds=45, rc=True)

a_c = (2.2e6) ** 2 / 0.53e-10
close(a_c, 9.13e22, 1e-2)
close(2.2e6 / 0.53e-10, 4.15e16, 1e-2)
close((2.2e6) ** 2 / 0.53, 9.13e12, 1e-2)
q(AN, "Bohr model and hydrogen spectrum", "Intermediate", "numerical",
  "In the ground state of the hydrogen atom in the Bohr model, the electron moves in a circle of radius "
  "0.53 × 10⁻¹⁰ m with a speed of 2.2 × 10⁶ m/s. The magnitude of its acceleration is about:",
  *opt("9.1 × 10²² m/s²", ["4.2 × 10¹⁶ m/s²", "1.8 × 10²³ m/s²", "9.1 × 10¹² m/s²"], "C"),
  "Uniform circular motion: centripetal acceleration a = v²/r",
  "The electron moves with constant speed in its orbit, so its acceleration is purely centripetal, directed towards "
  "the nucleus; it is provided by the Coulomb attraction.",
  ["a = v²/r = (2.2 × 10⁶)²/(0.53 × 10⁻¹⁰)", "a = 4.84 × 10¹²/0.53 × 10⁻¹⁰ ≈ 9.1 × 10²² m/s²"],
  why="4.2 × 10¹⁶ is v/r, which is the angular speed in rad/s, not an acceleration. 1.8 × 10²³ m/s² doubles v²/r. "
      "9.1 × 10¹² m/s² takes the radius in Å instead of metres.",
  ncert=ATC + "Bohr model of the hydrogen atom", seconds=45, rc=True)

q(AN, "Nuclear size and mass defect", "Intermediate", "match_list",
  ml("Match each scientist (or pair of scientists) in List-I with the contribution described in NCERT (List-II).",
     ["H. Geiger and E. Marsden", "E. Rutherford", "N. Bohr", "J. Chadwick"],
     ["Discovered the neutron (1932)", "Proposed the nuclear model of the atom to explain the scattering results",
      "Carried out the alpha-particle scattering experiment with a thin gold foil",
      "Proposed stationary orbits in which the electron does not radiate"]),
  *mlo("A-III, B-II, C-IV, D-I", ["A-II, B-III, C-IV, D-I", "A-III, B-II, C-I, D-IV", "A-III, B-IV, C-II, D-I"], "B"),
  "History of atomic and nuclear structure",
  "Geiger and Marsden, at Rutherford's suggestion, performed the alpha-particle scattering experiment (1911). "
  "Rutherford explained the results with the nuclear model. Bohr (1913) proposed stationary, non-radiating orbits. "
  "Chadwick discovered the neutron in 1932.",
  ["A → III", "B → II", "C → IV", "D → I"],
  why="The other codes swap the experimenters with the person who interpreted the experiment, or give the neutron "
      "to Bohr.",
  ncert=ATC + "alpha-particle scattering; Bohr model; " + "'Nuclei', discovery of neutron", seconds=45)

lines = [(i, f) for i in range(2, 5) for f in range(1, i) if i <= 4]
E = lambda n: -F(136, 10) / n ** 2
dE = {(i, f): E(i) - E(f) for i, f in lines}
assert len(lines) == 6 and min(dE, key=dE.get) == (4, 3) and max(dE, key=dE.get) == (4, 1)
assert sum(1 for i, f in lines if f == 2) == 2 and dE[(4, 1)] == F(1275, 100)
truth = {"a": True, "b": True, "c": True, "d": True, "e": False}
q(AN, "Bohr model and hydrogen spectrum", "Intermediate", "multi_statement",
  ms("A sample of hydrogen atoms is excited to the n = 4 level (E_n = −13.6/n² eV). As the atoms return to the ground "
     "state by all possible downward transitions, which of the following statements about the emitted radiation are "
     "correct?",
     ["Six different spectral lines can appear.",
      "The line of longest wavelength comes from the transition n = 4 → n = 3 and lies in the infrared.",
      "The line of shortest wavelength comes from the transition n = 4 → n = 1.",
      "Exactly two of the lines belong to the Balmer series.",
      "The most energetic photon emitted has an energy of 13.6 eV."]),
  *mso(truth, "abcd", ["abce", "bcd", "acde"], "D"),
  "Bohr's frequency condition; spectral series of hydrogen",
  "From n = 4 the possible transitions are 4→3, 4→2, 4→1, 3→2, 3→1 and 2→1: six lines. The smallest energy gap, "
  "4→3 (0.66 eV), gives the longest wavelength, a Paschen line in the infrared; the largest, 4→1 (12.75 eV), the "
  "shortest. Transitions ending on n = 2 (4→2 and 3→2) form Balmer lines: two of them. The largest photon energy is "
  "12.75 eV, not 13.6 eV, which would need an electron from n = ∞.",
  ["(a) 4 × 3/2 = 6 → true", "(b) 4→3: 0.66 eV, Paschen (IR) → true", "(c) 4→1: 12.75 eV → true",
   "(d) 4→2 and 3→2 → true", "(e) maximum 12.75 eV → false"],
  why="Options with (e) take the ionisation energy as the largest photon energy; the options leaving out (a) or (b) "
      "miss correct statements.",
  ncert=ATC + "the line spectra of the hydrogen atom", seconds=80, rc=True)

# ---- Advanced
r_ratio = F(1, 2)
m_ratio = r_ratio ** 3
v_ratio = 1 / m_ratio
assert m_ratio == F(1, 8) and v_ratio == 8
q(AN, "Fission and fusion", "Advanced", "numerical",
  "A nucleus at rest splits into two fragments whose radii are in the ratio 1 : 2 (take R = R₀A^(1/3) for each "
  "fragment and the mass of each fragment as proportional to its mass number). The ratio of the speed of the "
  "smaller fragment to that of the larger fragment is:",
  *opt("8 : 1", ["2 : 1", "4 : 1", "1 : 8"], "C"),
  "Nuclear radius R ∝ A^(1/3); conservation of momentum",
  "Since R ∝ A^(1/3), the mass numbers (and masses) are in the ratio of the cubes of the radii, 1 : 8. The parent "
  "was at rest, so the fragments move off with equal and opposite momenta, and their speeds are in the inverse ratio "
  "of their masses.",
  ["A₁ : A₂ = 1³ : 2³ = 1 : 8", "m₁v₁ = m₂v₂ → v₁ : v₂ = m₂ : m₁ = 8 : 1"],
  why="2 : 1 takes the masses in the ratio of the radii. 4 : 1 squares the radius ratio (as for surface areas). "
      "1 : 8 inverts the speed ratio: the lighter fragment moves faster.",
  ncert=NUC + "size of the nucleus", seconds=80, rc=True)

T1 = 1.5e-16
N_rev = 1.0e-8 / (8 * T1)
close(N_rev, 8.33e6, 1e-2)
close(1.0e-8 / T1, 6.67e7, 1e-2)
close(1.0e-8 / (4 * T1), 1.67e7, 1e-2)
q(AN, "Bohr model and hydrogen spectrum", "Advanced", "numerical",
  "In the Bohr model of the hydrogen atom, the electron takes 1.5 × 10⁻¹⁶ s to complete one revolution in the ground "
  "state, and the orbit radius and the electron's speed vary as n² and 1/n respectively. An electron remains in the "
  "n = 2 state for 1.0 × 10⁻⁸ s before returning to the ground state. The number of revolutions it makes in the "
  "n = 2 orbit in this time is about:",
  *opt("8.3 × 10⁶", ["6.7 × 10⁷", "1.7 × 10⁷", "4.2 × 10⁶"], "B"),
  "Time period of revolution T = 2πr/v ∝ n²/(1/n) = n³",
  "The period grows as n³, so in the n = 2 orbit it is 8 times the ground-state period. The number of revolutions "
  "is the time spent divided by this period.",
  ["T ∝ n³ → T₂ = 8 × 1.5 × 10⁻¹⁶ = 1.2 × 10⁻¹⁵ s", "N = 1.0 × 10⁻⁸/1.2 × 10⁻¹⁵ ≈ 8.3 × 10⁶"],
  why="6.7 × 10⁷ uses the ground-state period. 1.7 × 10⁷ takes T ∝ n² (only the larger radius). 4.2 × 10⁶ takes "
      "T ∝ n⁴.",
  ncert=ATC + "Bohr model of the hydrogen atom", seconds=100, rc=True)

R_cu = 1.2 * 64 ** (1 / 3)
K_alpha = 2 * 29 * 1.44 / R_cu
close(R_cu, 4.8)
close(K_alpha, 17.4, 1e-2)
close(29 * 1.44 / R_cu, 8.7, 1e-2)
close(2 * 29 * 1.44 / (1.2 * 64), 1.09, 1e-2)
close(2 * 64 * 1.44 / R_cu, 38.4, 1e-2)
q(AN, "Rutherford scattering", "Advanced", "numerical",
  "An alpha particle is projected head-on towards a copper nucleus (Z = 29, A = 64), which may be taken as fixed. "
  "Taking the nuclear radius R = R₀A^(1/3) with R₀ = 1.2 fm and e²/(4πε₀) = 1.44 MeV fm, and treating the nucleus "
  "and the alpha particle as point charges, the least kinetic energy the alpha particle must have for its distance "
  "of closest approach to equal the radius of the copper nucleus is about:",
  *opt("17 MeV", ["8.7 MeV", "1.1 MeV", "38 MeV"], "D"),
  "Nuclear radius R = R₀A^(1/3); distance of closest approach K = k(2e)(Ze)/d",
  "At closest approach the kinetic energy has all become electrostatic potential energy. Setting the distance equal "
  "to the nuclear radius gives the required energy.",
  ["R = 1.2 × 64^(1/3) = 1.2 × 4 = 4.8 fm", "K = (2 × 29 × 1.44 MeV fm)/4.8 fm", "K = 83.5/4.8 ≈ 17.4 MeV"],
  why="8.7 MeV gives the alpha particle a charge of e instead of 2e. 1.1 MeV uses R = R₀A instead of R₀A^(1/3). "
      "38 MeV uses the mass number 64 in place of the atomic number 29.",
  ncert=ATC + "alpha-particle trajectory; " + "'Nuclei', size of the nucleus", seconds=110, rc=True)

q(AN, "Binding energy", "Advanced", "statement_pair",
  sp("The binding energy of a nucleus is the energy needed to separate it completely into its constituent protons "
     "and neutrons.",
     "Of two nuclei, the one with the larger total binding energy is always the more stable."),
  SP, sp_key(True, False),
  "Binding energy and binding energy per nucleon",
  "Statement I is the definition of binding energy (it equals the mass defect times c²). Statement II is false: the "
  "stability of a nucleus is judged by its binding energy per nucleon. A heavy nucleus such as ²³⁸U has a much larger "
  "total binding energy than ⁵⁶Fe but a smaller binding energy per nucleon, and it releases energy when it splits.",
  ["I: definition → true", "II: stability depends on BE per nucleon, not total BE → false"],
  why="Statement II ignores that the total binding energy grows with the number of nucleons; it is the value per "
      "nucleon that measures how tightly each nucleon is bound.",
  ncert=NUC + "mass-energy and nuclear binding energy", seconds=50)


# ================================================================ Electronic Devices (B4 I5 A4)
SCC = NC + "'Semiconductor Electronics: Materials, Devices and Simple Circuits', "


def truth_table(fn):
    return [fn(a, b) for a, b in ((0, 0), (0, 1), (1, 0), (1, 1))]


NAND = lambda a, b: 1 - (a & b)
NOR = lambda a, b: 1 - (a | b)

# ---- Basic
q(ED, "p-n junction diode and rectifier", "Basic", "numerical",
  "A half-wave rectifier (a single junction diode in series with a load resistor) is fed from a 60 Hz AC supply. The "
  "number of current pulses through the load per second, i.e. the frequency of the rectified output, is:",
  *opt("60 Hz", ["120 Hz", "30 Hz", "zero, since the output is DC"], "B"),
  "Half-wave rectification: the diode conducts in only one half of each input cycle",
  "In each cycle of the input, the diode conducts during one half-cycle and blocks during the other, so the load "
  "receives one pulse per input cycle. The pulsating output therefore repeats 60 times a second.",
  ["One conducting half-cycle per input cycle", "Pulses per second = input frequency = 60 Hz"],
  why="120 Hz is the ripple frequency of a full-wave rectifier, which conducts in both halves. 30 Hz halves the "
      "frequency for no reason. The output is unidirectional but pulsating, not steady DC.",
  ncert=SCC + "application of junction diode as a rectifier", seconds=25, rc=True)

frac = 1.5e16 / 5e28
close(frac, 3e-13)
q(ED, "Semiconductors", "Basic", "numerical",
  "Pure silicon contains about 5 × 10²⁸ atoms per m³, and at room temperature its intrinsic carrier concentration is "
  "1.5 × 10¹⁶ m⁻³. The fraction of the silicon atoms that have released an electron into the conduction band is "
  "about:",
  *opt("3 × 10⁻¹³", ["3.3 × 10¹²", "1.5 × 10¹⁶", "6 × 10⁻¹³"], "D"),
  "Intrinsic semiconductor: n_e = n_h = n_i; each free electron comes from one broken covalent bond",
  "Each thermally generated free electron leaves one hole, so the number of atoms that have lost an electron per m³ "
  "is n_e = n_i. Dividing by the number of atoms per m³ gives the fraction, which is extremely small; this is why "
  "pure silicon conducts so poorly.",
  ["Fraction = n_i/N = 1.5 × 10¹⁶/5 × 10²⁸", "= 3 × 10⁻¹³"],
  why="3.3 × 10¹² is N/n_i, the inverse. 1.5 × 10¹⁶ is the carrier concentration itself, not a fraction. 6 × 10⁻¹³ "
      "counts the electrons and the holes as if each came from a different atom.",
  ncert=SCC + "intrinsic semiconductor", seconds=35, rc=True)

q(ED, "Semiconductors", "Basic", "direct",
  "An electric field is applied across a sample of pure silicon. The holes in its valence band move:",
  *opt("in the direction of the electric field, as positive charges would",
       ["opposite to the electric field, in the same direction as the free electrons",
        "at random, with no net drift, because holes are not real particles",
        "only if the sample has been doped with a trivalent impurity"], "A"),
  "Hole motion: a vacancy filled successively by neighbouring bound electrons behaves as a positive charge",
  "Bound electrons near a hole jump into it against the field direction, leaving a vacancy behind them. The vacancy "
  "therefore moves along the field, exactly as a positive charge would, and the hole current adds to the electron "
  "current.",
  ["Bound electrons move opposite to E (negative charge)", "The vacancy moves the other way → along E",
   "Holes act as positive carriers"],
  why="Free electrons move opposite to the field; holes move the other way. Although a hole is a vacancy, its motion "
      "is a real drift of charge. Pure silicon also has holes (thermally generated), not only doped silicon.",
  ncert=SCC + "intrinsic semiconductor", seconds=35)

q(ED, "Zener diode", "Basic", "statement_pair",
  sp("A Zener diode is made by heavily doping both its p- and n-sides, so that its depletion region is very thin.",
     "Because its depletion region is so thin, the electric field across the junction is very high (of the order of "
     "5 × 10⁶ V/m) even for a small reverse bias of about 5 V."),
  SP, sp_key(True, True),
  "Construction of the Zener diode",
  "Both statements are as described in NCERT. Heavy doping makes the depletion layer very thin (less than about "
  "10⁻⁶ m), so even a few volts of reverse bias produce an extremely high field, which can pull valence electrons "
  "out of their bonds and cause breakdown at a well-defined voltage.",
  ["I: heavy doping → thin depletion region → true", "II: thin region → very high field at small reverse bias → true"],
  why="Both statements are correct; neither has been altered.",
  ncert=SCC + "Zener diode", seconds=35)

# ---- Intermediate
q(ED, "p-n junction diode and rectifier", "Intermediate", "assertion_reason",
  ar("When a p-n junction is forward biased, a large current flows, carried mainly by the diffusion of majority "
     "carriers across the junction.",
     "Forward bias lowers the potential barrier at the junction, so that many more majority carriers have enough "
     "energy to diffuse across it."),
  AR, ar_key(True, True, True),
  "p-n junction under forward bias",
  "With forward bias the applied voltage opposes the built-in barrier, so the effective barrier height falls to "
  "V₀ − V. Majority carriers (holes from p, electrons from n) can then diffuse across in large numbers and become "
  "minority carriers on the other side, giving a large current that grows rapidly with V. R explains A.",
  ["A: forward current large, mainly diffusion of majority carriers → true",
   "R: barrier lowered → more carriers cross → true, and the cause of A"],
  why="R is the reason for the large diffusion current; it is not an unrelated property.",
  ncert=SCC + "semiconductor diode: p-n junction diode under forward bias", seconds=40)

q(ED, "p-n junction diode and rectifier", "Intermediate", "match_list",
  ml("Match each condition of a p-n junction (List-I) with its description (List-II).",
     ["No bias, in equilibrium", "Forward bias", "Reverse bias, below breakdown",
      "Reverse bias, at the breakdown voltage of a Zener diode"],
     ["No net current: the diffusion current is balanced by an equal and opposite drift current",
      "Barrier lowered and depletion region narrowed; a large current due mainly to majority carriers",
      "Barrier raised and depletion region widened; a small current due to minority carriers",
      "The current rises sharply while the voltage across the diode stays almost constant"]),
  *mlo("A-I, B-II, C-III, D-IV", ["A-II, B-I, C-III, D-IV", "A-I, B-III, C-II, D-IV", "A-I, B-II, C-IV, D-III"], "C"),
  "p-n junction: formation, forward bias, reverse bias and breakdown",
  "Without bias the junction settles into equilibrium in which diffusion and drift currents cancel. Forward bias "
  "reduces the barrier and the depletion width, giving a large majority-carrier current. Reverse bias raises the "
  "barrier and widens the depletion region; only minority carriers drift across, giving a small current. At the "
  "Zener breakdown voltage the reverse current increases sharply at an almost constant voltage.",
  ["A → I", "B → II", "C → III", "D → IV"],
  why="The other codes exchange the forward and reverse descriptions or give the breakdown behaviour to ordinary "
      "reverse bias.",
  ncert=SCC + "p-n junction formation; semiconductor diode; Zener diode", seconds=60)

truth = {"a": True, "b": True, "c": False, "d": True, "e": True}
q(ED, "Semiconductors", "Intermediate", "multi_statement",
  ms("Which of the following statements about doping and extrinsic semiconductors are correct?",
     ["An n-type semiconductor is electrically neutral as a whole.",
      "The dopant atoms should be of nearly the same size as the atoms of the pure semiconductor, so that they do not "
      "distort its crystal lattice.",
      "Pentavalent dopant atoms such as arsenic and phosphorus are called acceptors.",
      "In a p-type semiconductor, the number density of holes is much greater than that of free electrons.",
      "Trivalent dopants such as indium, boron and aluminium make silicon a p-type semiconductor."]),
  *mso(truth, "abde", ["abcd", "bde", "acde"], "B"),
  "Extrinsic semiconductors: donors (pentavalent) and acceptors (trivalent)",
  "Every free electron in n-type material is balanced by a positive donor ion, so the crystal stays neutral (a). "
  "NCERT notes that the dopant must not distort the lattice, so its atoms should be of nearly the same size (b). "
  "Pentavalent atoms donate an electron and are called donors, not acceptors (c false). In p-type material the "
  "acceptors create holes, so n_h ≫ n_e (d). In, B and Al are trivalent acceptors (e).",
  ["(a) true", "(b) true", "(c) false: pentavalent atoms are donors", "(d) true", "(e) true"],
  why="Options with (c) swap the names donor and acceptor; the options leaving out (a) or (e) miss correct "
      "statements.",
  ncert=SCC + "extrinsic semiconductor", seconds=60)

Y_i4 = truth_table(lambda a, b: NAND(a, b) | a)
assert Y_i4 == [1, 1, 1, 1]
q(ED, "Logic gates", "Intermediate", "direct",
  "Inputs A and B are fed to a NAND gate. The output of the NAND gate and the input A are then fed to an OR gate, "
  "whose output is Y. For the inputs (A, B) = (0, 0), (0, 1), (1, 0) and (1, 1), in that order, the outputs Y are:",
  *opt("1, 1, 1, 1", ["1, 1, 1, 0", "0, 1, 1, 1", "1, 0, 1, 1"], "D"),
  "Truth tables of NAND and OR gates",
  "The NAND output is 0 only for A = B = 1. Whenever the NAND output is 0, A is 1, so the OR gate still gives 1. In "
  "every other case the NAND output is 1 and the OR output is 1.",
  ["NAND: 1, 1, 1, 0", "A: 0, 0, 1, 1", "Y = NAND OR A: 1, 1, 1, 1"],
  shortcut="Y = (A·B)' + A = A' + B' + A = 1 always.",
  why="1, 1, 1, 0 is the NAND output alone. 0, 1, 1, 1 is A OR B. 1, 0, 1, 1 is A + B′, which would need "
      "the inverse of B, not the NAND output, at the OR gate.",
  ncert=SCC + "logic gates", seconds=50, rc=True)

I_z = F(20 - 5 - 7, 400)
assert I_z == F(20, 1000) and F(20 - 7, 400) == F(325, 10000) and F(20, 400) == F(50, 1000) and F(12, 400) == F(3, 100)
q(ED, "Zener diode", "Intermediate", "numerical",
  "Two Zener diodes, of breakdown voltages 5.0 V and 7.0 V, are connected in series with each other and with a "
  "400 Ω resistor across a 20 V DC supply. Both Zener diodes are reverse biased and operating in their breakdown "
  "regions. The current in the circuit is:",
  *opt("20 mA", ["32.5 mA", "50 mA", "30 mA"], "B"),
  "A Zener diode in breakdown keeps an (almost) constant voltage across itself",
  "With both Zeners in breakdown, the voltage across them together is 5.0 + 7.0 = 12 V. The rest of the supply "
  "voltage appears across the resistor, which fixes the current.",
  ["Voltage across the Zeners = 12 V", "Voltage across 400 Ω = 20 − 12 = 8 V", "I = 8/400 = 0.020 A = 20 mA"],
  why="32.5 mA subtracts only one Zener voltage. 50 mA ignores both Zener voltages. 30 mA divides the Zener voltage "
      "(12 V), instead of the resistor's voltage, by 400 Ω.",
  ncert=SCC + "Zener diode as a voltage regulator", seconds=50, rc=True)

# ---- Advanced
v_open = solve_network(3, [(0, 1, 1000), (1, 2, 2000)], {0: 6, 2: 0})
assert v_open[1] == 4 and v_open[1] > 3                        # diode would be forward biased
VM = F(3)
I_R1, I_R2 = (6 - VM) / 1000, VM / 2000
I_D = I_R1 - I_R2
assert I_R1 == F(3, 1000) and I_R2 == F(15, 10000) and I_D == F(15, 10000)
q(ED, "p-n junction diode and rectifier", "Advanced", "numerical",
  "An ideal 6.0 V battery (negative terminal at the earth point G) is connected through a 1.0 kΩ resistor to a point "
  "M. From M a 2.0 kΩ resistor goes to G. An ideal diode has its anode at M and its cathode at the positive terminal "
  "of an ideal 3.0 V battery whose negative terminal is at G. The current through the diode is:",
  *opt("1.5 mA", ["zero", "2.0 mA", "3.0 mA"], "D"),
  "Ideal diode: test whether it is forward biased, then treat it as a short (forward) or an open circuit (reverse)",
  "Without the diode branch, M would be at 6 × 2/3 = 4.0 V, higher than the 3.0 V at the cathode, so the diode is "
  "forward biased and conducts. An ideal conducting diode has no voltage across it, so M is held at 3.0 V.",
  ["Test: V_M (diode removed) = 4.0 V > 3.0 V → diode conducts", "V_M = 3.0 V",
   "Current in 1.0 kΩ = (6 − 3)/1.0 kΩ = 3.0 mA; in 2.0 kΩ = 3/2.0 kΩ = 1.5 mA",
   "Diode current = 3.0 − 1.5 = 1.5 mA"],
  why="Zero assumes the diode is reverse biased; the test shows it is not. 2.0 mA is the current with the diode "
      "branch removed. 3.0 mA is the current in the 1.0 kΩ resistor, part of which goes through the 2.0 kΩ "
      "resistor.",
  ncert=SCC + "semiconductor diode", seconds=120, rc=True)

A_seq, B_seq = [1, 1, 0, 0, 1], [0, 1, 1, 0, 1]
seq = lambda fn: [fn(a, b) for a, b in zip(A_seq, B_seq)]
assert seq(lambda a, b: a | b) == [1, 1, 1, 0, 1] and seq(lambda a, b: a & b) == [0, 1, 0, 0, 1]
assert seq(NAND) == [1, 0, 1, 1, 0] and seq(NOR) == [0, 0, 0, 1, 0]
q(ED, "Logic gates", "Advanced", "match_list",
  ml("The two inputs of a gate take the following values in five successive time intervals: A = 1, 1, 0, 0, 1 and "
     "B = 0, 1, 1, 0, 1. Match each two-input gate in List-I with its output in these five intervals (List-II).",
     ["OR", "AND", "NAND", "NOR"],
     ["0, 1, 0, 0, 1", "1, 0, 1, 1, 0", "1, 1, 1, 0, 1", "0, 0, 0, 1, 0"]),
  *mlo("A-III, B-I, C-II, D-IV", ["A-I, B-III, C-IV, D-II", "A-III, B-I, C-IV, D-II", "A-II, B-I, C-III, D-IV"], "C"),
  "Truth tables of OR, AND, NAND and NOR gates",
  "Take the input pairs in turn: (1, 0), (1, 1), (0, 1), (0, 0), (1, 1). OR gives 1 unless both inputs are 0; AND "
  "gives 1 only when both are 1; NAND and NOR are the inverses of AND and OR respectively.",
  ["OR: 1, 1, 1, 0, 1 → III", "AND: 0, 1, 0, 0, 1 → I", "NAND (NOT AND): 1, 0, 1, 1, 0 → II",
   "NOR (NOT OR): 0, 0, 0, 1, 0 → IV"],
  why="The other codes swap OR with AND, or NAND with NOR, i.e. invert the wrong basic gate.",
  ncert=SCC + "logic gates", seconds=70, rc=True)

X = truth_table(NOR)
Y = [x & b for x, (a, b) in zip(X, ((0, 0), (0, 1), (1, 0), (1, 1)))]
Y_or = [x | b for x, (a, b) in zip(X, ((0, 0), (0, 1), (1, 0), (1, 1)))]
Y_e = [(a | b) & b for a, b in ((0, 0), (0, 1), (1, 0), (1, 1))]
assert X == [1, 0, 0, 0] and Y == [0, 0, 0, 0] and Y_or == [1, 1, 0, 1] and Y_e == [0, 1, 0, 1]
truth = {"a": True, "b": True, "c": False, "d": False, "e": True}
q(ED, "Logic gates", "Advanced", "multi_statement",
  ms("Inputs A and B are fed to a NOR gate, whose output is X. X and the input B are then fed to an AND gate, whose "
     "output is Y. Which of the following statements are correct?",
     ["X = 1 only when A = 0 and B = 0.",
      "Y = 0 for every combination of the inputs.",
      "Y = 1 when A = 0 and B = 1.",
      "If the AND gate is replaced by an OR gate, the new output is 1 for every combination of the inputs.",
      "If the NOR gate is replaced by an OR gate (the AND gate kept), the new output Y is always equal to B."]),
  *mso(truth, "abe", ["abd", "ace", "be"], "A"),
  "Truth tables of NOR, AND and OR; Boolean simplification",
  "X = (A + B)' is 1 only for A = B = 0 (a). Then Y = X·B: when X = 1, B = 0, and when B = 1, X = 0, so Y is always 0 "
  "(b true, c false). With an OR gate instead, X + B gives 1, 1, 0, 1 for the four input pairs; it is 0 for A = 1, "
  "B = 0, so (d) is false. With an OR gate in place of the NOR, Y = (A + B)·B = B (e).",
  ["X: 1, 0, 0, 0 → (a) true", "Y = X·B: 0, 0, 0, 0 → (b) true, (c) false",
   "X + B: 1, 1, 0, 1 → (d) false", "(A + B)·B = B → (e) true"],
  why="Options with (c) or (d) contradict the truth tables; the option without (a) misses the defining property of "
      "the NOR gate.",
  ncert=SCC + "logic gates", seconds=100, rc=True)

ni_ratio = 2
assert ni_ratio ** 2 == 4
q(ED, "Semiconductors", "Advanced", "numerical",
  "A silicon sample is doped with donor atoms, all of which are ionised, the donor concentration being far larger "
  "than the intrinsic carrier concentration n_i. When the temperature of the sample is raised, n_i doubles, while "
  "the electron concentration remains practically equal to the donor concentration. The hole concentration in the "
  "sample becomes:",
  *opt("4 times its earlier value", ["2 times its earlier value", "unchanged", "1/4 of its earlier value"], "B"),
  "Mass-action law in thermal equilibrium: n_e n_h = n_i²",
  "In the n-type sample n_e ≈ N_D is fixed by the doping. The minority (hole) concentration is n_h = n_i²/n_e, so it "
  "varies as the square of n_i. This is why the reverse current of a junction diode, carried by minority carriers, "
  "rises steeply with temperature.",
  ["n_h = n_i²/N_D", "n_i → 2n_i, N_D unchanged → n_h → 4n_h"],
  why="'2 times' treats n_h as proportional to n_i. 'Unchanged' assumes the doping alone fixes the minority carriers. "
      "'1/4' inverts the dependence.",
  ncert=SCC + "extrinsic semiconductor", seconds=60, rc=True)


# ================================================================ Experimental Skills (B3 I3 A3)
LAB = "NMC syllabus, Experimental Skills: "

# ---- Basic
rel_d = F(1, 100) / F(2)
assert rel_d * 100 == F(1, 2) and 3 * rel_d * 100 == F(3, 2)
q(EXP, "Vernier calipers and screw gauge", "Basic", "numerical",
  "The diameter of a small steel sphere is measured with a vernier calipers of least count 0.01 cm and found to be "
  "2.00 cm. Taking the uncertainty in the diameter as one least count, the maximum percentage error in the volume of "
  "the sphere calculated from this measurement is:",
  *opt("1.5%", ["0.5%", "1.0%", "0.17%"], "C"),
  "Propagation of relative errors: for V ∝ d³, ΔV/V = 3 Δd/d",
  "The volume of a sphere is πd³/6, so its relative error is three times the relative error in the diameter.",
  ["Δd/d = 0.01/2.00 = 0.5%", "ΔV/V = 3 × 0.5% = 1.5%"],
  why="0.5% is the error in the diameter alone. 1.0% uses the square of d (as for an area). 0.17% divides by 3 "
      "instead of multiplying.",
  ncert=LAB + "use of vernier callipers to measure the diameter of a small spherical body", seconds=35, rc=True)

Rm = F(36)
assert Rm / 2 == 18
q(EXP, "Optics experiments", "Basic", "numerical",
  "In an experiment with a concave mirror, an object needle is moved along the principal axis until its real, "
  "inverted image coincides with it with no parallax between them. The needle is then 36.0 cm from the pole of the "
  "mirror. The focal length of the mirror is:",
  *opt("18.0 cm", ["36.0 cm", "9.0 cm", "72.0 cm"], "D"),
  "A real image coincides with the object only when the object is at the centre of curvature (u = v = R = 2f)",
  "For the reflected rays to return along their own paths and form the image on the object itself, they must strike "
  "the mirror normally, i.e. pass through the centre of curvature. So the needle is at C, 36.0 cm from the pole, and "
  "f = R/2.",
  ["Object and image coincide → needle at C", "R = 36.0 cm → f = R/2 = 18.0 cm"],
  why="36.0 cm is the radius of curvature, not the focal length. 9.0 cm halves R twice. 72.0 cm doubles R.",
  ncert=LAB + "focal length of a concave mirror", seconds=30, rc=True)

q(EXP, "Vernier calipers and screw gauge", "Basic", "assertion_reason",
  ar("The internal diameter of a beaker is measured with the upper pair of jaws of a vernier calipers, not with the "
     "lower (main) jaws.",
     "The upper jaws have their measuring edges on the outside, so they can be placed against the inner walls of the "
     "beaker and opened out until they touch them."),
  AR, ar_key(True, True, True),
  "Use of the vernier calipers: outside jaws, inside jaws and depth rod",
  "The lower jaws grip an object between their inner faces and so measure external dimensions. The small upper jaws "
  "have their measuring faces facing outwards; inserted into the beaker and opened, they press against the inner "
  "wall, giving the internal diameter. (The depth is measured with the thin strip at the end.) R explains A.",
  ["Lower jaws → external diameter", "Upper jaws (outward-facing edges) → internal diameter", "R explains A"],
  why="R gives the very reason the upper jaws are used for an internal measurement.",
  ncert=LAB + "use of vernier callipers to measure the internal diameter and depth of a given beaker", seconds=35)

# ---- Intermediate
l1, l2 = F(17), F(52)
l3 = l2 + (l2 - l1)
assert l3 == 87 and 5 * l1 == 85 and l1 + l2 == 69 and 2 * l2 == 104
q(EXP, "Mechanics experiments", "Intermediate", "numerical",
  "In a resonance-tube experiment with a tuning fork, the first and second resonances are obtained at air-column "
  "lengths of 17.0 cm and 52.0 cm. If the tube is long enough, the third resonance will be obtained at an air-column "
  "length of:",
  *opt("87.0 cm", ["69.0 cm", "104.0 cm", "85.0 cm"], "B"),
  "Successive resonances of a tube closed at one end are half a wavelength apart; the end correction is the same "
  "for all of them",
  "The resonances occur at l + e = λ/4, 3λ/4, 5λ/4, ..., where e is the end correction. So the difference between "
  "successive resonance lengths is λ/2, which is 52.0 − 17.0 = 35.0 cm, and the third resonance is another 35.0 cm "
  "further on.",
  ["λ/2 = l₂ − l₁ = 35.0 cm", "l₃ = l₂ + λ/2 = 52.0 + 35.0 = 87.0 cm"],
  why="69.0 cm adds l₁ and l₂. 104.0 cm doubles l₂. 85.0 cm takes 5l₁, which assumes no end correction "
      "(l₁ = λ/4 exactly); here 3l₁ = 51 cm ≠ 52 cm shows that there is an end correction.",
  ncert=LAB + "speed of sound in air at room temperature using a resonance tube", seconds=60, rc=True)

A0, A1_ = F(8), F(4)
remaining = (A1_ / A0) ** 2
assert remaining == F(1, 4) and (1 - remaining) * 100 == 75
q(EXP, "Mechanics experiments", "Intermediate", "numerical",
  "In an experiment on the dissipation of energy of a simple pendulum, the amplitude of the oscillations falls from "
  "8.0 cm to 4.0 cm in a certain time. The percentage of the initial energy of oscillation that has been dissipated "
  "in this time is:",
  *opt("75%", ["50%", "25%", "94%"], "D"),
  "Energy of a pendulum oscillating with small amplitude A is proportional to A²",
  "Halving the amplitude reduces the energy to (1/2)² = 1/4 of its initial value. The rest has been dissipated "
  "(mainly by air resistance and friction at the support).",
  ["E ∝ A²", "E_final/E_initial = (4/8)² = 1/4", "Energy dissipated = 1 − 1/4 = 75%"],
  why="50% takes the energy as proportional to the amplitude. 25% is the fraction of energy remaining, not the "
      "fraction dissipated. 94% uses A⁴.",
  ncert=LAB + "dissipation of energy of a simple pendulum by plotting a graph between square of amplitude and time",
  seconds=40, rc=True)

q(EXP, "Mechanics experiments", "Intermediate", "statement_pair",
  sp("In finding the mass of an object with a metre scale and a knife edge, the weight of the metre scale acts at its "
     "centre of gravity.",
     "If the scale is balanced on the knife edge at a point other than its centre of gravity, the moment of the "
     "scale's own weight about the knife edge must be included in the balance condition."),
  SP, sp_key(True, True),
  "Principle of moments; centre of gravity",
  "The whole weight of a uniform scale can be taken to act at its centre of gravity (its midpoint). When the knife "
  "edge is at the centre of gravity, this weight has no moment and drops out of the balance condition; when the "
  "knife edge is elsewhere, the weight has a moment about it, which must be included. Both statements are true.",
  ["I: weight acts at the centre of gravity → true",
   "II: knife edge away from the CG → weight has a moment → true"],
  why="Both statements are correct; neither is a trap.",
  ncert=LAB + "mass of a given object using a metre scale by the principle of moments", seconds=40)

# ---- Advanced
i_m, A_p = 50, 60
dm = 2 * i_m - A_p
n_p = 0.766 / math.sin(rad(A_p / 2))
assert dm == 40
close(n_p, 1.532)
close(0.766 / math.sin(rad(40)), 1.19, 1e-2)
q(EXP, "Optics experiments", "Advanced", "numerical",
  "In the experiment to draw the i–δ curve for a triangular glass prism of refracting angle 60°, the lowest point of "
  "the curve (minimum deviation) occurs at an angle of incidence of 50°. Taking sin 50° = 0.766, the angle of minimum "
  "deviation and the refractive index of the glass are, respectively:",
  *opt("40° and about 1.53", ["50° and about 1.53", "40° and about 1.19", "20° and about 1.53"], "B"),
  "At minimum deviation i = e and r₁ = r₂ = A/2, so δ_m = 2i − A and n = sin i / sin(A/2)",
  "At the minimum of the i–δ curve the ray passes symmetrically through the prism. Then i + e = A + δ with e = i "
  "gives δ_m, and Snell's law at the first face with r = A/2 gives n.",
  ["δ_m = 2i − A = 100° − 60° = 40°", "r = A/2 = 30°", "n = sin 50°/sin 30° = 0.766/0.5 ≈ 1.53"],
  why="'50°' takes the angle of incidence itself as the deviation. 'About 1.19' divides sin i by sin δ_m instead of "
      "sin(A/2). '20°' subtracts A/2 from i instead of using δ_m = 2i − A.",
  ncert=LAB + "plot a graph of angle of deviation versus angle of incidence for a triangular prism", seconds=90,
  rc=True)

q(EXP, "Thermal and fluid experiments", "Advanced", "match_list",
  ml("Match each laboratory determination in List-I with the relation used to calculate the result (List-II). "
     "(r = radius, ρ and σ = densities of ball and liquid, v = terminal velocity, h = capillary rise, M = load, "
     "L = length of wire, l = extension, f = frequency, l₁ and l₂ = first two resonance lengths.)",
     ["Coefficient of viscosity from the terminal velocity of a steel ball",
      "Surface tension from capillary rise (angle of contact zero)",
      "Young's modulus with Searle's apparatus",
      "Speed of sound with a resonance tube"],
     ["v = 2f(l₂ − l₁)", "T = rhρg/2", "Y = MgL/(πr²l)", "η = 2r²(ρ − σ)g/(9v)"]),
  *mlo("A-IV, B-II, C-III, D-I", ["A-II, B-IV, C-III, D-I", "A-IV, B-III, C-II, D-I", "A-IV, B-II, C-I, D-III"], "C"),
  "Working formulae of standard laboratory experiments",
  "At terminal velocity the viscous force 6πηrv balances the weight minus the upthrust, (4/3)πr³(ρ − σ)g, giving "
  "η = 2r²(ρ − σ)g/(9v). For capillary rise with zero contact angle, 2πrT = πr²hρg, so T = rhρg/2. Young's modulus "
  "is stress/strain = (Mg/πr²)/(l/L). Successive resonances are λ/2 apart, so v = fλ = 2f(l₂ − l₁).",
  ["A → IV", "B → II", "C → III", "D → I"],
  why="The other codes exchange the viscosity and surface-tension relations or the Young's modulus and speed-of-sound "
      "relations; each formula follows from a different balance of forces or wave condition.",
  ncert=LAB + "viscosity by terminal velocity; surface tension by capillary rise; Young's modulus; resonance tube",
  seconds=70)

truth = {"a": True, "b": True, "c": True, "d": True, "e": False}
q(EXP, "Electrical experiments", "Advanced", "multi_statement",
  ms("In the experiment to find the resistance of a given wire using Ohm's law, a graph of the potential difference "
     "V across the wire (y-axis) is plotted against the current I through it (x-axis). Which of the following "
     "statements are correct?",
     ["For the wire at a constant temperature, the graph is a straight line through the origin.",
      "The slope of the graph gives the resistance of the wire.",
      "A rheostat in the circuit is used to change the current in steps.",
      "The current should be kept small and passed only while readings are taken, so that the wire does not heat up.",
      "If a wire of the same material and thickness but twice the length is used, the slope of the graph is "
      "halved."]),
  *mso(truth, "abcd", ["abce", "abd", "bcde"], "D"),
  "Ohm's law, V = IR; R = ρL/A",
  "At constant temperature V ∝ I, so the V–I graph is a straight line through the origin (a) whose slope V/I is R "
  "(b). The rheostat varies the current (c). Heating raises the resistance and spoils the straight line, so the "
  "current is kept small and switched off between readings (d). Doubling the length doubles R = ρL/A, so the slope "
  "doubles, not halves (e false).",
  ["(a) true", "(b) true", "(c) true", "(d) true", "(e) false: R ∝ L → slope doubles"],
  why="Options with (e) invert the dependence of resistance on length; the options leaving out (c) or (a) miss "
      "correct statements about the set-up.",
  ncert=LAB + "resistivity of the material of a given wire using Ohm's law (graph of potential difference versus "
              "current)", seconds=70)


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
    assert all(31 <= keys[k] <= 36 for k in LETTERS), keys
    texts = [x["question_text"] for x in QS]
    assert len(set(texts)) == len(texts)
    doc = {"schema_version": "1.0", "batch_id": "BATCH_009", "created_at": TODAY,
           "notes": "Package PHY_009_p2: 133 original Physics questions (Electrostatics to Experimental Skills), "
                    "NEET_PHY_002118..002250. Numerical answers recomputed by tools/batch_009/PHY_009_p2.py.",
           "stimuli": [], "questions": QS}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {OUT}: {len(QS)} questions")
    print("difficulty", dict(Counter(x["difficulty"] for x in QS)))
    print("formats", dict(fmts))
    print("keys", dict(sorted(keys.items())))


if __name__ == "__main__":
    main()
