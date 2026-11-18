"""Writes batches/parts/BATCH_009_PHY_p1.json: package PHY_009_p1 of BATCH_009 (117 Physics questions).

Topics: Physics and Measurement, Kinematics, Laws of Motion, Work Energy and Power, Rotational Motion, Gravitation,
Properties of Solids and Liquids, Thermodynamics, Kinetic Theory of Gases, Oscillations and Waves.
IDs NEET_PHY_002001 .. NEET_PHY_002117, in the order the questions are listed below.

Every computable answer is re-derived with an assert before the file is written, and so is the plan quota. If any
assert fails, nothing is written. Each question's answer position is chosen by hand and fixed.

    python tools/batch_009/PHY_009_p1.py        (run from docs/neet-bank)
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
OUT = ROOT / "batches" / "parts" / "BATCH_009_PHY_p1.json"
PLAN = ROOT / "batches" / "plans" / "BATCH_009_plan.json"
PACKAGE = "PHY_009_p1"
TODAY = "2026-11-16"
LETTERS = "ABCD"
PHY = "Physics"
RECOMPUTED = ("script:recompute", "ai:author-solve", "ai:self-recheck")
AUTHORED = ("ai:author-solve", "ai:self-recheck")
FIRST_ID = 2001

QUESTIONS = []


def close(a, b, rel=1e-3):
    return math.isclose(a, b, rel_tol=rel, abs_tol=1e-12)


def place(correct, wrong, at):
    """Options with the correct text at letter `at`; returns (options, answer)."""
    assert len(wrong) == 3 and at in LETTERS
    opts = list(wrong)
    opts.insert(LETTERS.index(at), correct)
    assert len(set(opts)) == 4, opts
    return opts, at


def match_options(correct: dict, wrong: list, at: str):
    """Match-the-list option codes with the correct code at `at`; returns (options, answer)."""
    code = lambda m: ", ".join(f"{k}-{m[k]}" for k in "ABCD")
    for m in [correct, *wrong]:
        assert sorted(m.values()) == sorted(["I", "II", "III", "IV"]), m
    return place(code(correct), [code(w) for w in wrong], at)


def ar(answer):
    return list(ASSERTION_REASON), answer


def sp(answer):
    return list(STATEMENT_PAIR), answer


def add(topic, subtopic, difficulty, fmt, text, opt, concept, explanation, steps, shortcut=None, why=None,
        ncert=None, seconds=60, recomputed=False):
    options, answer = opt
    assert answer in LETTERS and len(options) == 4
    if fmt == "numerical":
        assert recomputed, f"numerical question {len(QUESTIONS) + FIRST_ID} must be recomputed"
    qid = f"NEET_PHY_{len(QUESTIONS) + FIRST_ID:06d}"
    QUESTIONS.append({
        "question_id": qid, "exam_mappings": default_mappings(PHY), "subject": PHY, "topic": topic,
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
                         "verified_by": list(RECOMPUTED if recomputed else AUTHORED), "verified_at": TODAY},
    })


AR_STEM = ("Given below are two statements: one is labelled Assertion (A) and the other is labelled Reason (R).\n\n"
           "Assertion (A): {a}\nReason (R): {r}\n\nChoose the correct answer from the options given below:")
SP_STEM = ("Given below are two statements:\n\nStatement I: {s1}\nStatement II: {s2}\n\n"
           "In the light of the above statements, choose the correct answer from the options given below:")
CHOOSE = "\n\nChoose the correct answer from the options given below:"


def multi(intro, statements):
    return intro + "\n\n" + "\n".join(f"({c}) {s}" for c, s in zip("abcde", statements)) + CHOOSE


def match_stem(intro, list1, list2):
    return (intro + "\n\nList-I:\n" + "\n".join(f"{k}. {v}" for k, v in zip("ABCD", list1))
            + "\n\nList-II:\n" + "\n".join(f"{k}. {v}" for k, v in zip(["I", "II", "III", "IV"], list2)) + CHOOSE)


def multi_key(truth, chosen):
    """Assert that the statements marked True are exactly the letters in `chosen`."""
    assert [c for c, t in zip("abcde", truth) if t] == list(chosen), (truth, chosen)


def dims(m=0, l=0, t=0, k=0):
    return (m, l, t, k)


def dmul(*ds):
    return tuple(sum(x) for x in zip(*ds))


def dpow(d, n):
    return tuple(n * x for x in d)


def dinv(d):
    return tuple(-x for x in d)


g = 10.0
k = 9e9
EPS0 = 8.85e-12
E_CH = 1.6e-19


def solve3(rows, rhs):
    """Solve a 3x3 linear system exactly (Fractions) by Cramer's rule."""
    def det(m):
        return (m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1]) - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
                + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0]))
    rows = [[F(x) for x in r] for r in rows]
    d = det(rows)
    out = []
    for i in range(3):
        m = [r[:] for r in rows]
        for j in range(3):
            m[j][i] = F(rhs[j])
        out.append(det(m) / d)
    return out


# =====================================================================================================================
# Physics and Measurement (B2 I3 A2)
# =====================================================================================================================
T = "Physics and Measurement"

add(T, "Units and SI system", "Basic", "direct",
    "The SI unit of solid angle is:",
    place("Steradian", ["Radian", "Degree", "Candela"], "B"),
    "Supplementary units: radian and steradian",
    "In the SI system the plane angle is measured in radian (rad) and the solid angle in steradian (sr). A solid "
    "angle is the ratio of the intercepted area on a sphere to the square of its radius, so like the plane angle it "
    "is dimensionless but has a named unit.",
    ["Plane angle dθ = ds/r → radian", "Solid angle dΩ = dA/r² → steradian"],
    why="The radian and the degree are units of plane angle, not solid angle. The candela is the SI base unit of "
        "luminous intensity.",
    ncert="Class 11 Physics, 'Units and Measurement', the international system of units (radian and steradian)",
    seconds=20)

assert close(0.05 / 2.50 * 100, 2.0)
add(T, "Errors in measurement", "Basic", "numerical",
    "Repeated measurements of the period of a pendulum give a mean value of 2.50 s and a mean absolute error of "
    "0.05 s. The percentage error in the measured period is:",
    place("2%", ["0.02%", "5%", "0.2%"], "C"),
    "Relative and percentage error",
    "The relative error is the mean absolute error divided by the mean value; multiplying by 100 gives the "
    "percentage error.",
    ["δa = Δa_mean / a_mean = 0.05 / 2.50 = 0.02", "Percentage error = 0.02 × 100 = 2%"],
    why="0.02% forgets to multiply by 100 correctly (it treats 0.02 itself as a percentage); 5% writes the absolute "
        "error 0.05 as 5%; 0.2% misplaces the decimal point.",
    ncert="Class 11 Physics, 'Units and Measurement', errors in measurement (relative and percentage error)",
    seconds=30, recomputed=True)

# centripetal force: F = m^x v^y r^z ; m [M], v [L T^-1], r [L], F [M L T^-2]
x_, y_, z_ = solve3([[1, 0, 0], [0, 1, 1], [0, -1, 0]], [1, 1, -2])
assert (x_, y_, z_) == (1, 2, -1)
add(T, "Dimensional analysis", "Intermediate", "numerical",
    "The force F needed to keep a body moving uniformly in a circle is assumed to depend only on its mass m, its "
    "speed v and the radius r of the circle, as F ∝ mˣ vʸ rᶻ. By the method of dimensions, the values of x, y and z "
    "are respectively:",
    place("1, 2 and −1", ["1, 1 and −1", "1, 2 and 1", "1, −2 and 1"], "D"),
    "Deducing a relation by the method of dimensions",
    "Equate the powers of M, L and T on the two sides. With m = [M], v = [L T⁻¹] and r = [L], the force "
    "[M L T⁻²] requires x = 1, y = 2 and z = −1, i.e. F ∝ mv²/r (the dimensionless constant, here 1, cannot be "
    "found this way).",
    ["[M L T⁻²] = [M]ˣ [L T⁻¹]ʸ [L]ᶻ", "M: x = 1", "T: −y = −2 → y = 2", "L: y + z = 1 → z = −1"],
    why="(1, 1, −1) gives [M T⁻¹], not a force; (1, 2, 1) gives [M L³ T⁻²]; (1, −2, 1) gives [M L⁻¹ T²].",
    ncert="Class 11 Physics, 'Units and Measurement', deducing relations among physical quantities", seconds=60,
    recomputed=True)

ML2 = {"Moment of inertia": dims(1, 2, 0), "Angular momentum": dims(1, 2, -1), "Torque": dims(1, 2, -2),
       "Power": dims(1, 2, -3)}
assert ML2["Angular momentum"] == dmul(dims(1, 0, 0), dims(0, 1, -1), dims(0, 1, 0))     # m v r
assert ML2["Torque"] == dmul(dims(1, 1, -2), dims(0, 1, 0))                               # F r
assert ML2["Power"] == dmul(dims(1, 1, -2), dims(0, 1, -1))                               # F v
add(T, "Dimensional analysis", "Intermediate", "match_list",
    match_stem("Match List-I (physical quantity) with List-II (its dimensional formula).",
               ["Moment of inertia", "Angular momentum", "Torque", "Power"],
               ["[M L² T⁻²]", "[M L² T⁻³]", "[M L² T⁰]", "[M L² T⁻¹]"]),
    match_options({"A": "III", "B": "IV", "C": "I", "D": "II"},
                  [{"A": "III", "B": "I", "C": "IV", "D": "II"}, {"A": "IV", "B": "III", "C": "I", "D": "II"},
                   {"A": "III", "B": "IV", "C": "II", "D": "I"}], "A"),
    "Dimensional formulae of rotational quantities",
    "All four quantities contain M L²; they differ only in the power of time. Moment of inertia is mr² → [M L²]; "
    "angular momentum is mvr → [M L² T⁻¹]; torque is force × distance → [M L² T⁻²]; power is force × velocity → "
    "[M L² T⁻³].",
    ["I = mr² → [M L² T⁰] (III)", "L = mvr → [M L² T⁻¹] (IV)", "τ = rF → [M L² T⁻²] (I)",
     "P = Fv → [M L² T⁻³] (II)"],
    shortcut="Each time derivative adds one T⁻¹: I → L (= Iω) → τ (= dL/dt); power = τω adds one more T⁻¹.",
    why="The other codes swap neighbouring powers of T: angular momentum with torque, moment of inertia with angular "
        "momentum, or torque with power.",
    ncert="Class 11 Physics, 'Units and Measurement', dimensional formulae", seconds=60)

add(T, "Least count and significant figures", "Intermediate", "statement_pair",
    SP_STEM.format(
        s1="When a measured value is written in scientific notation, a × 10ᵇ, the power of ten does not affect the "
           "number of significant figures.",
        s2="According to the rules given in NCERT, a length written as 12300 cm (without a decimal point) has five "
           "significant figures."),
    sp("C"),
    "Rules for counting significant figures",
    "In scientific notation all the significant digits appear in a; the factor 10ᵇ only fixes the order of "
    "magnitude, so Statement I is true. NCERT states that trailing zeros in a number without a decimal point are "
    "not significant: 123 m = 12300 cm = 123000 mm has three significant figures, so Statement II is false.",
    ["Statement I: 10ᵇ is irrelevant to significant figures → true",
     "Statement II: 12300 (no decimal point) → trailing zeros not significant → 3 significant figures → false"],
    why="Statement II would be true only if the number were written 12300. (with a decimal point) or as 1.2300 × 10⁴.",
    ncert="Class 11 Physics, 'Units and Measurement', significant figures", seconds=45)

# deep-water waves: v = g^x lam^y rho^z ; g [L T^-2], lam [L], rho [M L^-3], v [L T^-1]
x_, y_, z_ = solve3([[0, 0, 1], [1, 1, -3], [-2, 0, 0]], [0, 1, -1])
assert (x_, y_, z_) == (F(1, 2), F(1, 2), 0)
assert close(4 ** float(y_) * 2 ** float(z_), 2.0)
add(T, "Dimensional analysis", "Advanced", "numerical",
    "The speed v of waves on the surface of deep water is assumed to depend only on the acceleration due to "
    "gravity g, the wavelength λ of the waves and the density ρ of the liquid. Using the method of dimensions, if "
    "the wavelength is made 4 times and the water is replaced by a liquid of twice the density, the wave speed "
    "becomes:",
    place("2 times", ["√2 times", "4 times", "2√2 times"], "D"),
    "Method of dimensions: a variable whose exponent comes out zero",
    "Writing v ∝ gˣ λʸ ρᶻ and equating the powers of M, L and T gives z = 0: density is the only quantity with "
    "mass in it, so it cannot appear. Then x = y = 1/2, so v ∝ √(gλ), independent of the density.",
    ["[L T⁻¹] = [L T⁻²]ˣ [L]ʸ [M L⁻³]ᶻ", "M: z = 0", "T: −2x = −1 → x = 1/2", "L: x + y − 3z = 1 → y = 1/2",
     "v'/v = √4 = 2 (the change of density has no effect)"],
    shortcut="A quantity is the only one containing a base dimension (here ρ with M) → its exponent must be zero.",
    why="√2 times wrongly keeps ρ^(−1/2), giving √4/√2; 4 times forgets the square root; 2√2 times takes "
        "v ∝ √(gλρ).",
    ncert="Class 11 Physics, 'Units and Measurement', dimensional analysis and its applications", seconds=110,
    recomputed=True)

P_ = 2 * (12.5 + 4.2)
dP = 2 * (0.1 + 0.1)
assert close(P_, 33.4) and close(dP, 0.4) and round(dP / P_ * 100, 1) == 1.2
assert round((0.1 / 12.5 + 0.1 / 4.2) * 100, 1) == 3.2
add(T, "Errors in measurement", "Advanced", "numerical",
    "The length and breadth of a rectangular plate are measured as l = (12.5 ± 0.1) cm and b = (4.2 ± 0.1) cm. "
    "The perimeter of the plate with its maximum absolute error, and the corresponding percentage error "
    "(to one decimal place), are:",
    place("(33.4 ± 0.4) cm; 1.2%", ["(33.4 ± 0.2) cm; 0.6%", "(33.4 ± 0.4) cm; 3.2%", "(33.4 ± 0.8) cm; 2.4%"], "B"),
    "Combination of errors in a sum",
    "For a sum the absolute errors add. The perimeter is P = 2(l + b), so ΔP = 2(Δl + Δb). The percentage error is "
    "then ΔP/P × 100; relative errors are added only for products and quotients, not for sums.",
    ["P = 2(12.5 + 4.2) = 33.4 cm", "ΔP = 2(0.1 + 0.1) = 0.4 cm", "Percentage error = 0.4/33.4 × 100 ≈ 1.2%"],
    why="(33.4 ± 0.2) cm forgets the factor 2 in P = 2(l + b); 3.2% adds the relative errors of l and b as if P were "
        "a product; (33.4 ± 0.8) cm counts the error of each of the four sides twice.",
    ncert="Class 11 Physics, 'Units and Measurement', combination of errors (error of a sum)", seconds=80,
    recomputed=True)


def cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def norm(a):
    return math.sqrt(sum(x * x for x in a))


# =====================================================================================================================
# Kinematics (B4 I5 A4)
# =====================================================================================================================
T = "Kinematics"

a_ = (20 ** 2 - 10 ** 2) / (2 * 75)
assert close(a_, 2.0)
add(T, "Motion in a straight line", "Basic", "numerical",
    "A car moving along a straight road with uniform acceleration increases its speed from 10 m/s to 20 m/s while "
    "covering a distance of 75 m. Its acceleration is:",
    place("2 m/s²", ["4 m/s²", "0.13 m/s²", "3.3 m/s²"], "A"),
    "Equation of motion v² = u² + 2as",
    "When the distance, not the time, is given, use the third equation of uniformly accelerated motion, "
    "v² = u² + 2as.",
    ["a = (v² − u²)/(2s)", "a = (400 − 100)/(2 × 75) = 300/150 = 2 m/s²"],
    why="4 m/s² forgets the 2 in 2as; 0.13 m/s² divides the change in speed by the distance (10/75); 3.3 m/s² adds "
        "the squares of the speeds instead of subtracting them (500/150).",
    ncert="Class 11 Physics, 'Motion in a Straight Line', kinematic equations for uniformly accelerated motion",
    seconds=35, recomputed=True)

assert close(4 * 5 * math.sin(math.radians(30)), 10.0)
add(T, "Vectors", "Basic", "numerical",
    "Two vectors of magnitudes 4 units and 5 units are inclined to each other at 30°. The magnitude of their vector "
    "(cross) product is:",
    place("10 units", ["10√3 units", "20 units", "9 units"], "C"),
    "Magnitude of the vector product",
    "|A × B| = AB sin θ, where θ is the angle between the vectors.",
    ["|A × B| = 4 × 5 × sin 30°", "= 20 × 1/2 = 10 units"],
    why="10√3 uses cos 30° (the scalar product); 20 takes sin θ = 1; 9 simply adds the magnitudes.",
    ncert="Class 11 Physics, 'Motion in a Plane' and 'System of Particles and Rotational Motion', vector product",
    seconds=25, recomputed=True)

assert close(30 ** 2 / g, 90.0)
add(T, "Projectile motion", "Basic", "numerical",
    "A ball can be thrown from level ground with a speed of 30 m/s in any direction. Taking g = 10 m/s² and "
    "neglecting air resistance, the greatest horizontal distance it can be thrown along the ground is:",
    place("90 m", ["45 m", "180 m", "45√2 m"], "B"),
    "Maximum horizontal range",
    "The range R = u² sin 2θ / g is greatest when sin 2θ = 1, i.e. θ = 45°, so R_max = u²/g.",
    ["R_max = u²/g", "= 900/10 = 90 m"],
    why="45 m is u²/(2g), the greatest height for a vertical throw; 180 m is 2u²/g; 45√2 m uses sin θ = sin 45° "
        "in place of sin 2θ = sin 90°.",
    ncert="Class 11 Physics, 'Motion in a Plane', projectile motion (horizontal range)", seconds=25,
    recomputed=True)

add(T, "Vectors", "Basic", "direct",
    "A vector A is multiplied by the real number −2. The resulting vector:",
    place("Has magnitude 2|A| and points opposite to A",
          ["Has magnitude 2|A| and points along A", "Has magnitude |A|/2 and points opposite to A",
           "Is a scalar of value −2|A|"], "D"),
    "Multiplication of a vector by a real number",
    "Multiplying a vector by a real number λ gives a vector of magnitude |λ| times the original. If λ is negative, "
    "the direction is reversed.",
    ["|−2A| = 2|A|", "λ < 0 → direction reversed"],
    why="A negative multiplier reverses the direction, so 'along A' is wrong; the magnitude is multiplied by 2, not "
        "divided; and a vector multiplied by a scalar is still a vector.",
    ncert="Class 11 Physics, 'Motion in a Plane', multiplication of vectors by real numbers", seconds=20)

# v = 6t - 3t^2, x(0) = 0 -> x = 3t^2 - t^3 ; v = 0 at t = 2
t_rest = 2.0
assert close(6 * t_rest - 3 * t_rest ** 2, 0.0)
assert close(3 * t_rest ** 2 - t_rest ** 3, 4.0)
add(T, "Motion in a straight line", "Intermediate", "numerical",
    "A particle starts from the origin at t = 0 and moves along the x-axis with velocity v = 6t − 3t², where v is "
    "in m/s and t in seconds. Its position at the instant (after t = 0) when it comes momentarily to rest is:",
    place("4 m", ["12 m", "2 m", "6 m"], "B"),
    "Position from velocity by integration",
    "Set v = 0 to find the instant of rest, then integrate the velocity from t = 0 to get the position, using "
    "x = 0 at t = 0.",
    ["v = 0 → 6t − 3t² = 0 → t = 2 s", "x = ∫₀ᵗ (6t − 3t²) dt = 3t² − t³", "x(2) = 12 − 8 = 4 m"],
    why="12 m keeps only the 3t² term; 2 m gives the time, not the position; 6 m multiplies the greatest speed "
        "(3 m/s, at t = 1 s) by the whole 2 s, as if the speed were constant.",
    ncert="Class 11 Physics, 'Motion in a Straight Line', instantaneous velocity and kinematic relations",
    seconds=60, recomputed=True)

uy = g * (2 * math.sqrt(3)) / 2
assert close(math.degrees(math.atan2(uy, 10)), 60.0)
add(T, "Projectile motion", "Intermediate", "numerical",
    "A projectile launched from level ground has a speed of 10 m/s at the highest point of its path and a time of "
    "flight of 2√3 s. Taking g = 10 m/s² and neglecting air resistance, its angle of projection above the "
    "horizontal is:",
    place("60°", ["30°", "45°", "tan⁻¹(2√3)"], "A"),
    "Horizontal and vertical components of a projectile's velocity",
    "At the highest point only the horizontal component u cos θ remains, so u cos θ = 10 m/s. The time of flight "
    "T = 2u sin θ / g gives the vertical component u sin θ = gT/2.",
    ["u cos θ = 10 m/s", "u sin θ = gT/2 = 10 × 2√3/2 = 10√3 m/s", "tan θ = √3 → θ = 60°"],
    why="30° swaps the two components; 45° assumes the components are equal; tan⁻¹(2√3) uses u sin θ = gT, "
        "forgetting that the rise takes only half the flight time.",
    ncert="Class 11 Physics, 'Motion in a Plane', projectile motion", seconds=60, recomputed=True)

t_meet = 40 / 20
assert close(t_meet, 2.0) and close(20 * t_meet - 0.5 * g * t_meet ** 2, 40 - 0.5 * g * t_meet ** 2)
add(T, "Relative velocity", "Intermediate", "numerical",
    "At the same instant, ball P is thrown vertically upward from the ground with a speed of 20 m/s, and ball Q is "
    "released from rest at a height of 40 m vertically above P's starting point. Taking g = 10 m/s² and neglecting "
    "air resistance, the two balls meet after:",
    place("2 s", ["4 s", "2√2 s", "1 s"], "D"),
    "Relative motion of two bodies with the same acceleration",
    "Both balls have the same acceleration g, so the acceleration of one relative to the other is zero. Relative "
    "to Q, ball P moves upward at a constant 20 m/s, and it must close a gap of 40 m.",
    ["Relative acceleration = g − g = 0", "Relative speed = 20 − 0 = 20 m/s", "t = 40/20 = 2 s",
     "Check: P at 20(2) − 5(4) = 20 m; Q at 40 − 5(4) = 20 m"],
    shortcut="Same acceleration → treat the gap as closing at the constant relative speed.",
    why="4 s is P's time of flight; 2√2 s is the time Q alone would take to fall 40 m; 1 s halves the correct time "
        "by adding the two speeds wrongly (40/40).",
    ncert="Class 11 Physics, 'Motion in a Straight Line', relative velocity", seconds=60, recomputed=True)

add(T, "Graphs of motion", "Intermediate", "match_list",
    match_stem("The position x of a particle moving along the x-axis is given by each relation in List-I (x in "
               "metres, t in seconds, t ≥ 0). Match List-I with the description of the motion in List-II.",
               ["x = 5", "x = 3t", "x = 2t²", "x = 4t − t²"],
               ["Constant acceleration opposite to the initial velocity; the particle stops at t = 2 s and then "
                "moves back", "Constant non-zero velocity, zero acceleration",
                "At rest", "Starts from rest with constant acceleration along +x"]),
    match_options({"A": "III", "B": "II", "C": "IV", "D": "I"},
                  [{"A": "II", "B": "III", "C": "IV", "D": "I"}, {"A": "III", "B": "II", "C": "I", "D": "IV"},
                   {"A": "III", "B": "IV", "C": "II", "D": "I"}], "C"),
    "Reading velocity and acceleration from x(t)",
    "Differentiate each relation once for the velocity and twice for the acceleration.",
    ["x = 5: v = 0, a = 0 → at rest (III)", "x = 3t: v = 3 m/s, a = 0 → uniform velocity (II)",
     "x = 2t²: v = 4t (0 at t = 0), a = 4 m/s² → from rest with constant acceleration (IV)",
     "x = 4t − t²: v = 4 − 2t, a = −2 m/s² → stops at t = 2 s and returns (I)"],
    why="The wrong codes confuse a constant position (rest) with a constant velocity, or exchange the two "
        "accelerated motions, which differ in the sign of the acceleration relative to the initial velocity.",
    ncert="Class 11 Physics, 'Motion in a Straight Line', position-time graphs and kinematic relations",
    seconds=70)

add(T, "Vectors", "Intermediate", "statement_pair",
    SP_STEM.format(
        s1="A particle moving in a plane with a constant acceleration must always move along a parabolic path.",
        s2="For a particle moving in a plane with a constant acceleration a, its position vector at time t is "
           "r = r₀ + v₀t + ½at², where r₀ and v₀ are its position and velocity at t = 0."),
    sp("D"),
    "Motion in a plane with constant acceleration",
    "The vector relation r = r₀ + v₀t + ½at² holds for any constant acceleration, so Statement II is true. The "
    "path is a parabola only when v₀ is not parallel to a; if v₀ is zero or parallel (or antiparallel) to a, the "
    "particle moves along a straight line. So Statement I is false.",
    ["Statement II: integrate a = constant twice → r = r₀ + v₀t + ½at² → true",
     "Statement I: v₀ ∥ a (e.g. a ball thrown straight up) → straight-line path → false"],
    why="Statement I ignores the special case of initial velocity along the acceleration, such as vertical "
        "throws under gravity.",
    ncert="Class 11 Physics, 'Motion in a Plane', motion in a plane with constant acceleration", seconds=50)

# velocity 45 deg above horizontal at t = 1 s and 45 deg below at t = 3 s
uy = (g * 1 + g * 3) / 2
ux = uy - g * 1
assert close(uy, 20) and close(ux, 10) and close(-(uy - g * 3), ux)
assert close(uy / ux, 2.0)
add(T, "Projectile motion", "Advanced", "numerical",
    "A ball is projected from level ground. Its velocity is directed at 45° above the horizontal at t = 1 s and at "
    "45° below the horizontal at t = 3 s. Taking g = 10 m/s² and neglecting air resistance, the angle of projection "
    "above the horizontal is:",
    place("tan⁻¹(2)", ["45°", "tan⁻¹(1/2)", "60°"], "C"),
    "Components of projectile velocity at two instants",
    "The horizontal component u_x is constant and the vertical component falls as u_y − gt. At 45° above, "
    "u_y − g(1) = u_x; at 45° below, u_y − g(3) = −u_x. Solving gives both components.",
    ["u_y − 10 = u_x", "u_y − 30 = −u_x", "Adding: 2u_y = 40 → u_y = 20 m/s, so u_x = 10 m/s",
     "tan θ = u_y/u_x = 2 → θ = tan⁻¹(2)"],
    shortcut="By symmetry the highest point is midway, at t = 2 s, so u_y = 2g = 20 m/s; then u_x = u_y − g(1).",
    why="45° assumes the launch direction equals the direction at t = 1 s; tan⁻¹(1/2) inverts the ratio of "
        "components; 60° would need u_y/u_x = √3.",
    ncert="Class 11 Physics, 'Motion in a Plane', projectile motion", seconds=110, recomputed=True)

Pd, Qd = (3, 1, -2), (1, -3, 4)
assert cross(Pd, Qd) == (-2, -14, -10)
assert close(0.5 * norm(cross(Pd, Qd)), 5 * math.sqrt(3))
add(T, "Vectors", "Advanced", "numerical",
    "The two diagonals of a parallelogram are represented by the vectors P = 3î + ĵ − 2k̂ and Q = î − 3ĵ + 4k̂. "
    "The area of the parallelogram is:",
    place("5√3 square units", ["10√3 square units", "20√3 square units", "(5√3)/2 square units"], "B"),
    "Area of a parallelogram from its diagonals",
    "If the sides are a and b, the diagonals are P = a + b and Q = a − b (or b − a). Then P × Q = −2(a × b) in "
    "magnitude 2|a × b|, so the area |a × b| equals ½|P × Q|.",
    ["P × Q = î(1·4 − (−2)(−3)) − ĵ(3·4 − (−2)·1) + k̂(3·(−3) − 1·1) = −2î − 14ĵ − 10k̂",
     "|P × Q| = √(4 + 196 + 100) = √300 = 10√3", "Area = ½|P × Q| = 5√3 square units"],
    why="10√3 uses |P × Q| directly, as if P and Q were the sides; 20√3 doubles instead of halving; (5√3)/2 "
        "halves twice, mixing up the area of a triangle with that of the parallelogram.",
    ncert="Class 11 Physics, 'System of Particles and Rotational Motion', vector product of two vectors",
    seconds=120, recomputed=True)

add(T, "Vectors", "Advanced", "assertion_reason",
    AR_STEM.format(
        a="If two non-parallel vectors A and B have equal magnitudes, the vectors (A + B) and (A − B) are "
          "perpendicular to each other.",
        r="(A + B) · (A − B) = A² − B², where A and B are the magnitudes of the two vectors."),
    ar("A"),
    "Scalar product and perpendicularity",
    "Expanding the scalar product, (A + B)·(A − B) = A·A − A·B + B·A − B·B = A² − B², because the scalar product "
    "is commutative. When A = B this is zero, and a zero scalar product of two non-zero vectors means they are "
    "perpendicular. So R is exactly the reason for A.",
    ["(A + B)·(A − B) = A² − B² (R true)", "A = B → product = 0 → (A + B) ⊥ (A − B) (A true)",
     "R directly gives A → option A"],
    why="R is not a separate fact: setting A = B in R is the whole proof of A, so B is wrong; both statements are "
        "true, so C and D are wrong.",
    ncert="Class 11 Physics, 'Work, Energy and Power', the scalar product", seconds=60)

add(T, "Motion in a straight line", "Advanced", "multi_statement",
    multi("A ball is thrown vertically upward from the ground with a speed of 20 m/s. Taking g = 10 m/s² and "
          "neglecting air resistance, which of the following statements are correct?",
          ["It rises to a maximum height of 20 m.",
           "At t = 3 s, it is 15 m above the ground.",
           "The distance it travels in the first 3 s is 25 m.",
           "At t = 3 s, its velocity is 10 m/s directed upward.",
           "Its average velocity over the first 4 s is zero."]),
    place("(a), (b), (c) and (e) only", ["(a), (b) and (d) only", "(a), (c) and (e) only",
                                         "(b), (c), (d) and (e) only"], "D"),
    "Vertical motion under gravity: displacement versus distance",
    "The ball rises for u/g = 2 s to a height u²/2g = 20 m and is back on the ground at 2u/g = 4 s. After 2 s it "
    "falls, so its velocity at 3 s is downward.",
    ["(a) H = 400/20 = 20 m, true", "(b) y(3) = 20(3) − 5(9) = 15 m, true",
     "(c) 20 m up in 2 s, then 5 m down in the next 1 s → 25 m, true",
     "(d) v(3) = 20 − 30 = −10 m/s → 10 m/s downward, false", "(e) y(4) = 80 − 80 = 0 → average velocity 0, true"],
    why="(d) has the right speed but the wrong direction: after the highest point (t = 2 s) the ball moves down. "
        "Every option without (c) or including (d) is wrong.",
    ncert="Class 11 Physics, 'Motion in a Straight Line', kinematic equations for uniformly accelerated motion",
    seconds=100, recomputed=True)


# =====================================================================================================================
# Laws of Motion (B4 I5 A4)
# =====================================================================================================================
T = "Laws of Motion"

assert close(0.6 / 0.8, 0.75)
add(T, "Friction", "Basic", "numerical",
    "A block placed on a plank begins to slide down when one end of the plank is slowly raised until the plank "
    "makes an angle of 37° with the horizontal (sin 37° = 0.6, cos 37° = 0.8). The coefficient of static friction "
    "between the block and the plank is:",
    place("0.75", ["0.6", "0.8", "1.33"], "C"),
    "Angle of repose",
    "At the angle of repose θᵣ the component of weight along the incline just equals the limiting static "
    "friction: mg sin θᵣ = μₛ mg cos θᵣ, so μₛ = tan θᵣ.",
    ["μₛ = tan 37° = sin 37°/cos 37°", "= 0.6/0.8 = 0.75"],
    why="0.6 is sin 37° and 0.8 is cos 37°, not their ratio; 1.33 is cot 37°, the ratio taken upside down.",
    ncert="Class 11 Physics, 'Laws of Motion', friction (angle of repose)", seconds=30, recomputed=True)

assert close(1000 * 10 ** 2 / 50, 2000)
add(T, "Circular motion: level and banked roads", "Basic", "numerical",
    "A car of mass 1000 kg takes a turn of radius 50 m on a level (unbanked) road at a steady speed of 10 m/s. The "
    "magnitude of the frictional force exerted by the road on the car is:",
    place("2000 N", ["200 N", "20000 N", "10000 N"], "D"),
    "Friction as the centripetal force on a level road",
    "On a level road the only horizontal force on the car is static friction, so it alone supplies the "
    "centripetal force mv²/r. It need not be the limiting value μₛN.",
    ["f = mv²/r", "= 1000 × 100/50 = 2000 N"],
    why="200 N uses mv/r (speed not squared); 20000 N uses mv²/r with r = 5 m; 10000 N is the weight mg, which "
        "would be μN with μ = 1.",
    ncert="Class 11 Physics, 'Laws of Motion', circular motion (car on a level road)", seconds=30, recomputed=True)

a_ = g * math.sin(math.radians(30))
assert close(math.sqrt(2 * a_ * 10), 10.0)
add(T, "Newton's laws and impulse", "Basic", "numerical",
    "A block is released from rest on a smooth plane inclined at 30° to the horizontal. Taking g = 10 m/s², its "
    "speed after it has slid 10 m along the incline is:",
    place("10 m/s", ["10√3 m/s", "10√2 m/s", "5 m/s"], "A"),
    "Motion on a smooth inclined plane",
    "On a smooth incline the only force along the plane is the component of weight mg sin θ, so the block "
    "accelerates uniformly at g sin θ along the incline.",
    ["a = g sin 30° = 5 m/s²", "v² = 2as = 2 × 5 × 10 = 100", "v = 10 m/s"],
    why="10√3 m/s uses g cos θ as the acceleration; 10√2 m/s uses the full g (free fall through 10 m); 5 m/s gives "
        "the acceleration value instead of the speed.",
    ncert="Class 11 Physics, 'Laws of Motion', Newton's second law", seconds=35, recomputed=True)

add(T, "Newton's laws and impulse", "Basic", "direct",
    "Which of the following is NOT a contact force?",
    place("The gravitational force between the Earth and the Moon",
          ["The frictional force between a block and the floor", "The normal reaction of a table on a book",
           "The tension in a string pulling a block"], "B"),
    "Contact and non-contact forces",
    "Friction, the normal reaction and the tension in a string act only when bodies touch. Gravitational (and "
    "magnetic) forces act across a distance, without contact.",
    ["Friction, normal force, tension → contact forces", "Gravitation → acts at a distance"],
    why="The other three forces all need physical contact between the bodies concerned.",
    ncert="Class 11 Physics, 'Laws of Motion', introduction (contact and non-contact forces)", seconds=20)

# blocks 1, 2, 3 kg in a line, 12 N pulls the 3 kg block
a_ = 12 / (1 + 2 + 3)
assert close(a_, 2) and close((1 + 2) * a_, 6) and close(1 * a_, 2)
add(T, "Newton's laws and impulse", "Intermediate", "numerical",
    "Three blocks of masses 1 kg, 2 kg and 3 kg lie in a line on a smooth horizontal table, in that order, joined "
    "by two light horizontal strings (1 kg to 2 kg, and 2 kg to 3 kg). A horizontal force of 12 N pulls the 3 kg "
    "block away from the others. The tension in the string joining the 2 kg and 3 kg blocks is:",
    place("6 N", ["2 N", "10 N", "4 N"], "A"),
    "Connected bodies: tension from the free-body diagram of the trailing part",
    "All three blocks have the same acceleration. The string between the 2 kg and 3 kg blocks pulls the 1 kg and "
    "2 kg blocks together, so its tension equals their combined mass times the acceleration.",
    ["a = 12/(1 + 2 + 3) = 2 m/s²", "T = (1 + 2) × 2 = 6 N"],
    why="2 N is the tension in the other string (1 kg × 2 m/s²); 10 N subtracts only the 1 kg block's share from "
        "12 N; 4 N uses the 2 kg block alone.",
    ncert="Class 11 Physics, 'Laws of Motion', Newton's second law and the dynamics of connected bodies",
    seconds=55, recomputed=True)

a_ = 0.5 * g
assert close(10 ** 2 / (2 * a_), 10.0)
add(T, "Friction", "Intermediate", "numerical",
    "A block slides onto a rough horizontal floor with a speed of 10 m/s. The coefficient of kinetic friction "
    "between the block and the floor is 0.5. Taking g = 10 m/s², the distance it slides before coming to rest is:",
    place("10 m", ["20 m", "5 m", "2 m"], "C"),
    "Retardation due to kinetic friction",
    "The only horizontal force is kinetic friction μₖmg, so the retardation is μₖg, independent of the mass.",
    ["a = μₖg = 0.5 × 10 = 5 m/s²", "s = u²/(2a) = 100/10 = 10 m"],
    why="20 m forgets the 2 in u²/(2a); 5 m is the value of the retardation; 2 m is the stopping time "
        "(u/a = 2 s) written as a distance.",
    ncert="Class 11 Physics, 'Laws of Motion', friction (kinetic friction)", seconds=40, recomputed=True)

px, py = 2 * 3, 1 * 6
assert close(math.hypot(px, py) / 3, 2 * math.sqrt(2))
add(T, "Conservation of linear momentum", "Intermediate", "numerical",
    "On a smooth horizontal surface, a ball of mass 2 kg moving due east at 3 m/s collides with a ball of mass "
    "1 kg moving due north at 6 m/s. The balls stick together. The speed of the combined body just after the "
    "collision is:",
    place("2√2 m/s", ["4 m/s", "6√2 m/s", "2 m/s"], "B"),
    "Conservation of momentum in two dimensions",
    "With no external horizontal force, the total momentum is conserved as a vector. Conserve each component "
    "separately and combine.",
    ["East: 2 × 3 = 6 kg m/s; North: 1 × 6 = 6 kg m/s", "Total p = √(6² + 6²) = 6√2 kg m/s",
     "v = 6√2/3 = 2√2 m/s, directed north-east"],
    why="4 m/s adds the two momenta as scalars (12/3); 6√2 m/s is the magnitude of the total momentum, not divided "
        "by the total mass; 2 m/s is only one component of the final velocity.",
    ncert="Class 11 Physics, 'Laws of Motion', conservation of momentum", seconds=50, recomputed=True)

assert (0, 2 * 4, 2 * 3 ** 2 / 2, 6) == (0, 8, 9, 6)
add(T, "Newton's laws and impulse", "Intermediate", "match_list",
    match_stem("A body of mass 2 kg moves as described in List-I (SI units). Match List-I with List-II "
               "(magnitude of the net force on the body).",
               ["It moves with a constant velocity v = (3î + 4ĵ) m/s",
                "Its position along a straight line is x = 2t²",
                "It moves uniformly on a circle of radius 2 m with a speed of 3 m/s",
                "Its linear momentum along a straight line is p = 6t"],
               ["9 N", "Zero", "6 N", "8 N"]),
    match_options({"A": "II", "B": "IV", "C": "I", "D": "III"},
                  [{"A": "II", "B": "III", "C": "I", "D": "IV"}, {"A": "III", "B": "IV", "C": "I", "D": "II"},
                   {"A": "II", "B": "IV", "C": "III", "D": "I"}], "D"),
    "Net force from the state of motion",
    "Newton's second law: F = dp/dt = ma. Constant velocity means zero net force; in uniform circular motion the "
    "net force is mv²/r.",
    ["A: a = 0 → F = 0 (II)", "B: a = d²x/dt² = 4 m/s² → F = 8 N (IV)", "C: F = mv²/r = 2 × 9/2 = 9 N (I)",
     "D: F = dp/dt = 6 N (III)"],
    why="The wrong codes give x = 2t² the value 6 N (taking a = 2t² differentiated once) or swap the circular-"
        "motion and momentum cases.",
    ncert="Class 11 Physics, 'Laws of Motion', Newton's second law", seconds=70, recomputed=True)

add(T, "Newton's laws and impulse", "Intermediate", "statement_pair",
    SP_STEM.format(
        s1="Newton's second law is a local relation: the force at a point at a certain instant determines the "
           "acceleration at that point at that instant, independent of the history of motion.",
        s2="A stone is dropped from the window of a train that is accelerating along a level track. Just after its "
           "release, the stone has the train's horizontal acceleration in addition to the acceleration g "
           "(neglect air resistance)."),
    sp("C"),
    "Second law as a local relation",
    "Statement I is NCERT's description of the second law. For the stone: once it leaves the hand, no horizontal "
    "force acts on it (air resistance neglected), so by this local relation its acceleration is g, vertically "
    "downward, at once. It keeps the train's horizontal velocity at the instant of release, but not the train's "
    "acceleration. So Statement II is false.",
    ["Statement I: acceleration depends only on the force at that instant → true",
     "Statement II: after release, horizontal force = 0 → horizontal acceleration = 0 → false"],
    why="Statement II confuses velocity, which the stone keeps, with acceleration, which depends only on the "
        "force acting at that instant.",
    ncert="Class 11 Physics, 'Laws of Motion', Newton's second law of motion", seconds=50)

cos_t = (13 ** 2 - 7 ** 2 - 8 ** 2) / (2 * 7 * 8)
assert close(cos_t, 0.5) and close(math.degrees(math.acos(cos_t)), 60)
add(T, "Equilibrium of concurrent forces", "Advanced", "numerical",
    "Three concurrent forces of magnitudes 7 N, 8 N and 13 N keep a particle in equilibrium. The angle between the "
    "directions of the 7 N and the 8 N forces is:",
    place("60°", ["120°", "90°", "30°"], "B"),
    "Equilibrium of three concurrent forces",
    "In equilibrium the 13 N force is equal and opposite to the resultant of the other two, so the resultant of the "
    "7 N and 8 N forces has magnitude 13 N. Use R² = A² + B² + 2AB cos θ.",
    ["169 = 49 + 64 + 2(7)(8) cos θ", "cos θ = 56/112 = 1/2", "θ = 60°"],
    why="120° is the interior angle of the triangle of forces (180° − 60°), not the angle between the force "
        "directions; 90° assumes the forces form a right angle; 30° results from using sin θ for cos θ.",
    ncert="Class 11 Physics, 'Laws of Motion', equilibrium of a particle", seconds=75, recomputed=True)

theta = math.radians(45)
mu = math.tan(theta) * (1 - 1 / 2 ** 2)
assert close(mu, 0.75)
a_s, a_r = g * math.sin(theta), g * (math.sin(theta) - mu * math.cos(theta))
assert close(math.sqrt(2 * 1 / a_r) / math.sqrt(2 * 1 / a_s), 2.0)
add(T, "Friction", "Advanced", "numerical",
    "A block takes twice as long to slide from rest down a rough plane inclined at 45° as it would take to slide "
    "the same distance from rest down a smooth plane of the same inclination. The coefficient of kinetic friction "
    "between the block and the rough plane is:",
    place("0.75", ["0.5", "0.25", "1.33"], "A"),
    "Motion on a rough incline compared with a smooth one",
    "From rest, s = ½at², so for the same distance t ∝ 1/√a. Twice the time means one quarter of the "
    "acceleration. On the rough plane a = g(sin θ − μ cos θ); on the smooth plane a = g sin θ.",
    ["t_rough/t_smooth = 2 → a_smooth/a_rough = 4", "sin θ − μ cos θ = (sin θ)/4",
     "μ = (3/4) tan θ = 0.75 at θ = 45°"],
    shortcut="μ = tan θ (1 − 1/n²) when the time is n times as long.",
    why="0.5 takes t ∝ 1/a (forgetting the square root); 0.25 writes μ = tan θ/n²; 1.33 inverts the ratio 3/4.",
    ncert="Class 11 Physics, 'Laws of Motion', friction on an inclined plane", seconds=110, recomputed=True)

add(T, "Circular motion: level and banked roads", "Advanced", "assertion_reason",
    AR_STEM.format(
        a="When a car turns sharply to the left, a passenger sitting on the right side is pressed against the "
          "right-hand door.",
        r="The passenger's body tends to keep moving in a straight line because of inertia, so the car turns "
          "towards the left under the passenger until the door pushes on the passenger and supplies the "
          "centripetal force needed to turn."),
    ar("A"),
    "Inertia of direction and the centripetal force",
    "Seen from the ground, no force pushes the passenger outward. Her body tends to continue in its original "
    "straight line (first law); the car turns left beneath her, so the right-hand door moves into her, and the "
    "door's push towards the centre of the turn supplies the centripetal force. This is exactly why she is pressed "
    "against the door.",
    ["A: true, a familiar observation", "R: true, it is the first-law explanation", "R explains A → option A"],
    why="R is the explanation, not a separate fact, so B is wrong; both statements are true, so C and D are wrong. "
        "The common wrong idea is an outward 'centrifugal' force, which R correctly avoids.",
    ncert="Class 11 Physics, 'Laws of Motion', Newton's first law of motion", seconds=50)

a_ = (20 - 0.2 * 5 * g) / 5
N12 = 3 * a_ + 0.2 * 3 * g
N_alt = 2 * a_ + 0.2 * 2 * g
assert close(a_, 2) and close(N12, 12) and close(N_alt, 8) and close(2 * a_, 4) and close(0.2 * 3 * g, 6)
truth = [True, True, True, False, False]
multi_key(truth, "abc")
add(T, "Friction", "Advanced", "multi_statement",
    multi("Blocks of masses 2 kg and 3 kg are placed in contact on a rough horizontal floor. The coefficient of "
          "kinetic friction between each block and the floor is 0.2. A horizontal force of 20 N is applied to the "
          "2 kg block, pushing both blocks along together. Take g = 10 m/s². Which of the following statements "
          "are correct?",
          ["The acceleration of the blocks is 2 m/s².",
           "The 2 kg block pushes the 3 kg block with a force of 12 N.",
           "If the same 20 N force were instead applied to the 3 kg block, pushing the blocks the other way, the "
           "contact force between them would be 8 N.",
           "The net force on the 2 kg block is 8 N.",
           "The friction force on the 3 kg block is 10 N."]),
    place("(a), (b) and (c) only", ["(a), (b) and (d) only", "(a), (c) and (e) only",
                                    "(b), (d) and (e) only"], "D"),
    "Connected bodies with friction: free-body diagrams",
    "Total friction = 0.2 × 50 = 10 N, so the common acceleration is (20 − 10)/5 = 2 m/s². The contact force on "
    "the leading block must accelerate it and overcome its own friction.",
    ["(a) a = (20 − 10)/5 = 2 m/s², true", "(b) N = 3(2) + 0.2(30) = 6 + 6 = 12 N, true",
     "(c) N' = 2(2) + 0.2(20) = 4 + 4 = 8 N, true", "(d) net force on 2 kg = 2 × 2 = 4 N, not 8 N → false",
     "(e) friction on 3 kg = 0.2 × 30 = 6 N; 10 N is the total friction on both → false"],
    why="(d) confuses the net force with the contact force on the other block; (e) uses the total friction on both "
        "blocks for one of them.",
    ncert="Class 11 Physics, 'Laws of Motion', friction and the dynamics of connected bodies", seconds=120,
    recomputed=True)


# =====================================================================================================================
# Work, Energy and Power (B4 I5 A4)
# =====================================================================================================================
T = "Work, Energy and Power"

assert close(0.5 * 2 * (3 ** 2 + 4 ** 2), 25)
add(T, "Work-energy theorem", "Basic", "numerical",
    "A body of mass 2 kg moves with a velocity v = (3î + 4ĵ) m/s. Its kinetic energy is:",
    place("25 J", ["49 J", "50 J", "5 J"], "B"),
    "Kinetic energy from a velocity vector",
    "Kinetic energy depends on the square of the speed, v² = v·v = vₓ² + v_y². It is a scalar.",
    ["v² = 3² + 4² = 25 m²/s²", "K = ½ × 2 × 25 = 25 J"],
    why="49 J squares the sum of the components, (3 + 4)²; 50 J forgets the ½; 5 J is the speed in m/s.",
    ncert="Class 11 Physics, 'Work, Energy and Power', kinetic energy", seconds=25, recomputed=True)

assert close(2 * g * 5, 100)
add(T, "Work-energy theorem", "Basic", "numerical",
    "A ball of mass 2 kg is dropped from rest from a height of 5 m. Taking g = 10 m/s² and neglecting air "
    "resistance, its kinetic energy just before it strikes the ground is:",
    place("100 J", ["10 J", "50 J", "200 J"], "C"),
    "Work done by gravity equals the gain in kinetic energy",
    "The only force doing work is gravity, which does work mgh on the ball as it falls through h. By the "
    "work-energy theorem this equals the gain in kinetic energy.",
    ["W_gravity = mgh = 2 × 10 × 5 = 100 J", "K = 0 + 100 = 100 J"],
    why="10 J is the speed (10 m/s) written as an energy; 50 J halves mgh; 200 J doubles it.",
    ncert="Class 11 Physics, 'Work, Energy and Power', the work-energy theorem", seconds=25, recomputed=True)

assert close(math.sqrt(g * 2.5), 5.0)
add(T, "Motion in a vertical circle", "Basic", "numerical",
    "A small stone tied to a light string 2.5 m long is whirled in a vertical circle. Taking g = 10 m/s², the least "
    "speed it must have at the highest point for the string to remain taut there is:",
    place("5 m/s", ["5√5 m/s", "25 m/s", "5√2 m/s"], "A"),
    "Critical speed at the top of a vertical circle",
    "At the highest point both gravity and the tension point towards the centre: T + mg = mv²/L. The string just "
    "stays taut when T = 0, so v² = gL.",
    ["T + mg = mv²/L with T = 0", "v = √(gL) = √25 = 5 m/s"],
    why="5√5 m/s is √(5gL), the least speed needed at the LOWEST point; 25 m/s is gL without the square root; "
        "5√2 m/s is √(2gL), the speed gained in falling through L, which is not the condition here.",
    ncert="Class 11 Physics, 'Work, Energy and Power', motion in a vertical circle", seconds=30, recomputed=True)

add(T, "Spring potential energy", "Basic", "direct",
    "A block attached to an ideal spring is pulled slowly from the spring's natural length to an extension x and "
    "then allowed to return slowly to the natural length. The total work done by the spring force over this whole "
    "cycle is:",
    place("Zero", ["½kx²", "−½kx²", "kx²"], "D"),
    "Spring force is conservative",
    "The spring force is conservative: the work it does depends only on the initial and final positions. While "
    "stretching it does −½kx², while returning it does +½kx², so the total over a closed cycle is zero.",
    ["Stretching: W = −½kx²", "Returning: W = +½kx²", "Total over the cycle = 0"],
    why="½kx² and −½kx² are the work in only one half of the cycle; kx² adds the magnitudes of the two halves.",
    ncert="Class 11 Physics, 'Work, Energy and Power', the potential energy of a spring", seconds=25)

t_ = 3.0
v_ = t_ ** 2          # a = 2t / 1 kg  ->  v = t^2
assert close(2 * t_ * v_, 54)
add(T, "Power", "Intermediate", "numerical",
    "A body of mass 1 kg, initially at rest, is acted on by a single force F = 2t along a straight line, where F is "
    "in newtons and t in seconds. The instantaneous power delivered by the force at t = 3 s is:",
    place("54 W", ["18 W", "27 W", "6 W"], "C"),
    "Instantaneous power P = Fv",
    "First find the velocity at t = 3 s by integrating the acceleration, then multiply by the force at that "
    "instant.",
    ["a = F/m = 2t → v = ∫₀ᵗ 2t dt = t²", "At t = 3 s: F = 6 N, v = 9 m/s", "P = Fv = 6 × 9 = 54 W"],
    why="18 W takes v = at = 6 × 3, treating the acceleration as constant; 27 W uses the average force 3 N; 6 W "
        "gives the force alone.",
    ncert="Class 11 Physics, 'Work, Energy and Power', power", seconds=60, recomputed=True)

assert close(5 / 0.5, 10)
add(T, "Work-energy theorem", "Intermediate", "numerical",
    "A small block is released from rest at a height of 5 m on a smooth curved track. At the bottom the track "
    "becomes horizontal and rough, with coefficient of kinetic friction 0.5. The distance the block slides along "
    "the rough part before stopping is:",
    place("10 m", ["5 m", "2.5 m", "20 m"], "B"),
    "Work-energy theorem with gravity and friction",
    "Over the whole motion the block starts and ends at rest, so the work done by gravity (mgh) and by friction "
    "(−μmgd) add up to zero. The smooth curved part does no frictional work, and the normal force does no work.",
    ["mgh − μmgd = 0", "d = h/μ = 5/0.5 = 10 m"],
    shortcut="d = h/μ; the mass and g cancel.",
    why="5 m equates d to h; 2.5 m multiplies h by μ instead of dividing; 20 m finds v² = 2gh = 100 m²/s² at the "
        "bottom and then forgets the 2 in d = v²/(2μg).",
    ncert="Class 11 Physics, 'Work, Energy and Power', the work-energy theorem", seconds=50, recomputed=True)

assert close(0.5 * 800 * 20 ** 2 / 10, 16000)
assert close(800 * 2 * 20, 32000) and close(0.5 * 800 * 10 ** 2 / 10, 4000)
add(T, "Power", "Intermediate", "numerical",
    "A car of mass 800 kg accelerates uniformly from rest to 20 m/s in 10 s along a level road. Neglecting friction "
    "and air resistance, the average power delivered to the car in these 10 s is:",
    place("16 kW", ["32 kW", "4 kW", "160 kW"], "D"),
    "Average power as work done divided by time",
    "The work done on the car equals its gain in kinetic energy. Average power is this work divided by the time. "
    "With uniform acceleration the instantaneous power rises steadily, so its final value is twice the average.",
    ["W = ½mv² = ½ × 800 × 400 = 160 kJ", "P_avg = 160 kJ / 10 s = 16 kW"],
    why="32 kW is the instantaneous power at the end (F = 1600 N times 20 m/s); 4 kW puts the average speed 10 m/s "
        "into ½mv²; 160 kW is the work in kJ, not divided by 10 s.",
    ncert="Class 11 Physics, 'Work, Energy and Power', power", seconds=50, recomputed=True)

add(T, "Work by constant and variable force", "Intermediate", "match_list",
    match_stem("A body moves along a straight line (the x-axis). Match List-I (feature of a graph) with List-II "
               "(the quantity it gives).",
               ["Area under the force–position (F–x) graph between two positions",
                "Slope of the kinetic energy–position (K–x) graph",
                "Negative of the slope of the potential energy–position (U–x) graph of a conservative force",
                "Slope of the kinetic energy–time (K–t) graph"],
               ["Power delivered by the net force", "The conservative force at that position",
                "Net force on the body along the x-axis", "Work done by the force between those positions"]),
    match_options({"A": "IV", "B": "III", "C": "II", "D": "I"},
                  [{"A": "IV", "B": "I", "C": "II", "D": "III"}, {"A": "III", "B": "IV", "C": "II", "D": "I"},
                   {"A": "IV", "B": "III", "C": "I", "D": "II"}], "A"),
    "Graphical meaning of work, force and power",
    "Work is ∫F dx, the area under F–x. By the work-energy theorem dK = F_net dx, so dK/dx = F_net and "
    "dK/dt = F_net·v, the power of the net force. For a conservative force F = −dU/dx.",
    ["A: W = ∫F dx → area (IV)", "B: dK/dx = F_net (III)", "C: −dU/dx = F (II)", "D: dK/dt = F_net v = P (I)"],
    why="The wrong codes swap the slope against position (a force) with the slope against time (a power), or the "
        "net force with the conservative force.",
    ncert="Class 11 Physics, 'Work, Energy and Power', work done by a variable force; the concept of potential "
          "energy; power", seconds=70)

add(T, "Work-energy theorem", "Intermediate", "statement_pair",
    SP_STEM.format(
        s1="The potential energy of a body can have a negative value.",
        s2="When only conservative forces do work on a body, its total mechanical energy remains constant, although "
           "its kinetic energy may change."),
    sp("A"),
    "Potential energy and conservation of mechanical energy",
    "Potential energy is defined only up to an additive constant: it is measured from a chosen zero, and below "
    "that reference (for example a body below the chosen ground level, or gravitational potential energy taken "
    "zero at infinity) it is negative. So Statement I is true. With only conservative forces, K + U is constant; K "
    "and U can each change as one is converted into the other. So Statement II is true.",
    ["Statement I: U depends on the reference level → can be negative → true",
     "Statement II: conservative forces → K + U = constant, K may vary → true"],
    why="Only the difference of potential energy is physically fixed, not its sign; and conservation of mechanical "
        "energy does not mean that the kinetic energy stays constant.",
    ncert="Class 11 Physics, 'Work, Energy and Power', the concept of potential energy; conservation of mechanical "
          "energy", seconds=45)

x_ = 2 * g / 200
W_g = 2 * g * x_
U_s = 0.5 * 200 * x_ ** 2
assert close(x_, 0.1) and close(W_g, 2) and close(U_s, 1) and close(U_s - W_g, -1)
add(T, "Spring potential energy", "Advanced", "numerical",
    "A block of mass 2 kg is attached to the lower end of a light vertical spring of spring constant 200 N/m whose "
    "upper end is fixed. Starting with the spring at its natural length, the block is lowered slowly by hand until "
    "it hangs at rest in equilibrium. Taking g = 10 m/s², the work done by the hand on the block is:",
    place("−1 J", ["+1 J", "−2 J", "Zero"], "C"),
    "Work-energy theorem with gravity, spring and an applied force",
    "The block starts and ends at rest, so the total work done on it is zero. Gravity does +mgx; the spring does "
    "−½kx²; the hand, holding the block back, does the rest (negative work).",
    ["Equilibrium extension x = mg/k = 20/200 = 0.1 m", "W_gravity = mgx = 2 J; W_spring = −½kx² = −1 J",
     "W_hand = 0 − (2 − 1) = −1 J"],
    shortcut="Lowered slowly to equilibrium, the spring stores only half of the gravitational PE lost; the hand "
             "takes the other half.",
    why="+1 J has the wrong sign: the hand pushes up while the block moves down; −2 J ignores the spring; zero "
        "assumes gravity and the spring do equal and opposite work.",
    ncert="Class 11 Physics, 'Work, Energy and Power', the potential energy of a spring; the work-energy theorem",
    seconds=110, recomputed=True)

L_ = 0.4
v_low = math.sqrt(5 * g * L_)
u_b = v_low * (0.05 + 0.95) / 0.05
assert close(v_low, 2 * math.sqrt(5)) and close(u_b, 40 * math.sqrt(5))
add(T, "Motion in a vertical circle", "Advanced", "numerical",
    "A wooden block of mass 0.95 kg hangs at rest from a light inextensible string 0.4 m long. A bullet of mass "
    "50 g moving horizontally strikes the block and gets embedded in it. Taking g = 10 m/s², the least speed of the "
    "bullet for which the block (with the bullet) just completes a vertical circle is:",
    place("40√5 m/s", ["40√2 m/s", "40 m/s", "2√5 m/s"], "B"),
    "Momentum conservation in the impact, then energy conservation in the vertical circle",
    "During the brief impact, momentum is conserved (kinetic energy is not). Just after the impact the block must "
    "have at least √(5gL) at the lowest point to go round the circle on a string.",
    ["Needed speed of block after impact: V = √(5gL) = √20 = 2√5 m/s",
     "Momentum: 0.05u = (0.05 + 0.95)V", "u = 20 × 2√5 = 40√5 m/s"],
    why="40√2 m/s uses √(2gL), which only raises the block to the level of the support; 40 m/s uses √(4gL), the "
        "condition for a light rod; 2√5 m/s is the block's speed, not the bullet's.",
    ncert="Class 11 Physics, 'Work, Energy and Power', motion in a vertical circle; collisions", seconds=120,
    recomputed=True)

add(T, "Work by constant and variable force", "Advanced", "assertion_reason",
    AR_STEM.format(
        a="The tension in the string of a swinging simple pendulum does no work on the bob.",
        r="The tension in the string of a swinging simple pendulum has the same magnitude at every point of the "
          "swing."),
    ar("C"),
    "Work done by a force perpendicular to the displacement",
    "The bob moves along an arc of a circle centred on the point of support, so its displacement at every instant "
    "is along the tangent, perpendicular to the string. The tension is along the string, so T·dr = 0 and the "
    "tension does no work: A is true. The tension is not constant: it must supply mv²/L plus the radial component "
    "of weight, T = mg cos θ + mv²/L, which is largest at the lowest point. So R is false.",
    ["A: tension ⊥ displacement → W = 0 → true", "R: T = mg cos θ + mv²/L varies with θ and v → false"],
    why="R is false, so options A and B are wrong; A is true, so D is wrong. The work is zero because of the "
        "direction of the tension, whatever its magnitude.",
    ncert="Class 11 Physics, 'Work, Energy and Power', the scalar product and work", seconds=50)

k_, m_, u_ = 100, 1, 2
xmax = math.sqrt(m_ * u_ ** 2 / k_)
assert close(xmax, 0.2) and close(k_ * xmax, 20)
assert close(math.sqrt((0.5 * m_ * u_ ** 2 - 0.5 * k_ * 0.1 ** 2) * 2 / m_), math.sqrt(3))
truth = [True, True, False, True, False]
multi_key(truth, "abd")
add(T, "Spring potential energy", "Advanced", "multi_statement",
    multi("A block of mass 1 kg moving at 2 m/s on a smooth horizontal surface strikes the free end of a light "
          "horizontal spring of spring constant 100 N/m, whose other end is fixed to a wall. Which of the following "
          "statements are correct?",
          ["The greatest force exerted by the spring on the block is 20 N.",
           "When the compression is 0.1 m, the speed of the block is √3 m/s.",
           "While the spring is being compressed, the spring force does +2 J of work on the block.",
           "The block leaves the spring with a speed of 2 m/s, moving away from the wall.",
           "Over the whole interaction, the net work done by the spring force on the block is +2 J."]),
    place("(a), (b) and (d) only", ["(a), (c) and (d) only", "(b), (c) and (e) only",
                                    "(a), (b), (d) and (e) only"], "D"),
    "Conservation of energy with an ideal spring",
    "All the kinetic energy (2 J) is stored at maximum compression, ½kx_m² = 2 J, so x_m = 0.2 m. The spring force "
    "opposes the block while it compresses (negative work) and pushes it back while it extends (positive work).",
    ["(a) x_m = √(2 × 2/100) = 0.2 m → F_max = kx_m = 20 N, true",
     "(b) ½v² = 2 − ½(100)(0.01) = 1.5 → v = √3 m/s, true",
     "(c) compression: W = −2 J, not +2 J → false", "(d) energy conserved → leaves at 2 m/s, reversed, true",
     "(e) net work = ΔK = 0 (speed unchanged) → false"],
    why="(c) has the wrong sign; (e) forgets that the block leaves with the same speed it came in with, so the net "
        "work is zero.",
    ncert="Class 11 Physics, 'Work, Energy and Power', the potential energy of a spring", seconds=110,
    recomputed=True)


# =====================================================================================================================
# Rotational Motion (B4 I5 A4)
# =====================================================================================================================
T = "Rotational Motion"

assert close(5 * 4 * 2 * math.pi, 40 * math.pi)
add(T, "Rigid-body rotation", "Basic", "numerical",
    "A constant torque of 5 N m acts on a wheel about its fixed axle while the wheel turns through 4 complete "
    "revolutions. The work done by the torque is:",
    place("40π J", ["20 J", "20π J", "40 J"], "A"),
    "Work done by a torque",
    "For rotation about a fixed axis, the work done by a constant torque is W = τθ, with θ in radians, just as "
    "W = Fs in linear motion.",
    ["θ = 4 × 2π = 8π rad", "W = τθ = 5 × 8π = 40π J"],
    why="20 J multiplies the torque by the number of revolutions; 20π J uses π rad per revolution; 40 J uses 2 rad "
        "per revolution, dropping π.",
    ncert="Class 11 Physics, 'System of Particles and Rotational Motion', work done by a torque", seconds=30,
    recomputed=True)

assert close(20 * 10, 200)
add(T, "Rigid-body rotation", "Basic", "numerical",
    "The engine of a machine applies a constant torque of 20 N m to a shaft rotating steadily at 10 rad/s about its "
    "axis. The power delivered to the shaft is:",
    place("200 W", ["2 W", "20 W", "100 W"], "C"),
    "Power in rotational motion",
    "Instantaneous power in rotation is P = τω, the analogue of P = Fv.",
    ["P = τω = 20 × 10 = 200 W"],
    why="2 W divides the torque by ω; 20 W ignores ω; 100 W takes half the product, confusing P with a kinetic "
        "energy expression.",
    ncert="Class 11 Physics, 'System of Particles and Rotational Motion', power in rotational motion", seconds=20,
    recomputed=True)

assert close(math.sqrt(0.18 / 2), 0.3)
add(T, "Moment of inertia and axis theorems", "Basic", "numerical",
    "The moment of inertia of a body of mass 2 kg about a certain axis is 0.18 kg m². Its radius of gyration about "
    "this axis is:",
    place("0.3 m", ["0.09 m", "0.36 m", "0.6 m"], "D"),
    "Radius of gyration",
    "The radius of gyration k about an axis is defined by I = Mk²: it is the distance from the axis at which the "
    "whole mass, placed as a point, would have the same moment of inertia.",
    ["k = √(I/M) = √(0.18/2) = √0.09", "k = 0.3 m"],
    why="0.09 m forgets the square root; 0.36 m multiplies I by M; 0.6 m doubles the correct value.",
    ncert="Class 11 Physics, 'System of Particles and Rotational Motion', moment of inertia (radius of gyration)",
    seconds=25, recomputed=True)

add(T, "Torque and angular momentum", "Basic", "direct",
    "The SI unit of angular momentum can also be written as:",
    place("J s", ["N m", "kg m² s⁻²", "W s"], "B"),
    "Units of angular momentum",
    "Angular momentum L = r × p has unit m × kg m s⁻¹ = kg m² s⁻¹. Since 1 J = 1 kg m² s⁻², this is the same as "
    "J s (also the unit of Planck's constant).",
    ["L = mvr → kg m² s⁻¹", "J s = kg m² s⁻² × s = kg m² s⁻¹"],
    why="N m (= kg m² s⁻²) is the unit of torque; kg m² s⁻² is the same unit written in base units; W s is the joule, "
        "a unit of energy.",
    ncert="Class 11 Physics, 'System of Particles and Rotational Motion', angular momentum of a particle",
    seconds=25)

I_t = (F(2, 3) + 1) * 3 * F(2, 10) ** 2
assert I_t == F(1, 5)
add(T, "Moment of inertia and axis theorems", "Intermediate", "numerical",
    "A thin spherical shell has mass 3 kg and radius 0.2 m. Its moment of inertia about a diameter is (2/3)MR². Its "
    "moment of inertia about a tangent to its surface is:",
    place("0.2 kg m²", ["0.08 kg m²", "0.168 kg m²", "0.12 kg m²"], "B"),
    "Theorem of parallel axes",
    "A tangent is parallel to a diameter at a distance R from it. By the parallel axis theorem, "
    "I = I_cm + MR² = (2/3 + 1)MR² = (5/3)MR².",
    ["MR² = 3 × 0.04 = 0.12 kg m²", "I = (5/3) × 0.12 = 0.2 kg m²"],
    why="0.08 kg m² is the moment of inertia about a diameter; 0.168 kg m² uses (7/5)MR², the result for a SOLID "
        "sphere; 0.12 kg m² is MR² alone, leaving out I_cm.",
    ncert="Class 11 Physics, 'System of Particles and Rotational Motion', theorem of parallel axes", seconds=45,
    recomputed=True)

L_ = F(3)
x_cm = (L_ ** 3 / 3) / (L_ ** 2 / 2)
assert x_cm == 2
add(T, "Centre of mass", "Intermediate", "numerical",
    "A thin rod 3 m long lies along the x-axis from x = 0 to x = 3 m. Its mass per unit length increases with x as "
    "λ = kx, where k is a constant. The position of its centre of mass is:",
    place("x = 2 m", ["x = 1.5 m", "x = 1 m", "x = 2.25 m"], "D"),
    "Centre of mass of a continuous body",
    "For a continuous body, X = ∫x dm / ∫dm with dm = λ dx. Because the rod is heavier towards x = 3 m, the centre "
    "of mass lies beyond the midpoint.",
    ["M = ∫₀³ kx dx = 9k/2", "∫₀³ x·kx dx = 9k", "X = 9k/(9k/2) = 2 m (= 2L/3)"],
    why="1.5 m treats the rod as uniform; 1 m is L/3, measured from the wrong end; 2.25 m uses ∫x³/∫x² "
        "(as if λ ∝ x²).",
    ncert="Class 11 Physics, 'System of Particles and Rotational Motion', centre of mass of a continuous body",
    seconds=70, recomputed=True)

ratio = (F(1, 4)) / F(1, 12)          # (L/2pi)^2 / (L^2/12) without pi^2 -> 3/pi^2
assert ratio == 3
assert close(1 / (4 * math.pi ** 2) / (1 / 12), 3 / math.pi ** 2)
add(T, "Moment of inertia and axis theorems", "Intermediate", "numerical",
    "A thin uniform straight wire of mass M and length L has moment of inertia I₁ about an axis perpendicular to it "
    "through its midpoint. The same wire is bent into a circular ring, whose moment of inertia about the axis "
    "through its centre perpendicular to its plane is I₂. The ratio I₂/I₁ is:",
    place("3/π²", ["π²/3", "12/π²", "3/(2π²)"], "A"),
    "Moment of inertia of a rod and a ring",
    "For the straight wire I₁ = ML²/12. Bent into a ring, the circumference is L, so R = L/(2π) and "
    "I₂ = MR² = ML²/(4π²).",
    ["I₁ = ML²/12", "R = L/(2π) → I₂ = ML²/(4π²)", "I₂/I₁ = 12/(4π²) = 3/π²"],
    why="π²/3 is the inverse ratio; 12/π² takes R = L/π (forgetting the 2 in 2πR); 3/(2π²) uses MR²/2, the moment "
        "of inertia of a ring about a diameter.",
    ncert="Class 11 Physics, 'System of Particles and Rotational Motion', moments of inertia of some regular "
          "shaped bodies", seconds=60, recomputed=True)

r_ = (2, 0, 0)
Ls = {k_: cross(r_, v) for k_, v in {"A": (0, 3, 0), "B": (3, 0, 0), "C": (0, -3, 0), "D": (0, 0, 3)}.items()}
assert Ls == {"A": (0, 0, 6), "B": (0, 0, 0), "C": (0, 0, -6), "D": (0, -6, 0)}
add(T, "Torque and angular momentum", "Intermediate", "match_list",
    match_stem("A particle of mass 1 kg is at the point r = 2î m. Match List-I (its velocity, in m/s) with List-II "
               "(its angular momentum about the origin, in kg m² s⁻¹).",
               ["v = 3ĵ", "v = 3î", "v = −3ĵ", "v = 3k̂"],
               ["Zero", "−6ĵ", "6k̂", "−6k̂"]),
    match_options({"A": "III", "B": "I", "C": "IV", "D": "II"},
                  [{"A": "IV", "B": "I", "C": "III", "D": "II"}, {"A": "III", "B": "II", "C": "IV", "D": "I"},
                   {"A": "III", "B": "I", "C": "II", "D": "IV"}], "C"),
    "Angular momentum as a vector product, l = r × p",
    "l = r × p = m(r × v). Use î × ĵ = k̂, ĵ × î = −k̂, î × î = 0 and î × k̂ = −ĵ.",
    ["A: 2î × 3ĵ = 6k̂ (III)", "B: 2î × 3î = 0, since r ∥ v (I)", "C: 2î × (−3ĵ) = −6k̂ (IV)",
     "D: 2î × 3k̂ = 6(î × k̂) = −6ĵ (II)"],
    why="The wrong codes reverse the sign for v = ±3ĵ, take î × k̂ = +ĵ, or give a non-zero angular momentum when "
        "the velocity is along r.",
    ncert="Class 11 Physics, 'System of Particles and Rotational Motion', angular momentum of a particle",
    seconds=70, recomputed=True)

add(T, "Torque and angular momentum", "Intermediate", "statement_pair",
    SP_STEM.format(
        s1="If no external torque acts on a body rotating about a fixed axis, its angular velocity must remain "
           "constant.",
        s2="The kinetic energy of a rigid body rotating about a fixed axis with angular velocity ω is ½Iω², where I "
           "is its moment of inertia about that axis."),
    sp("D"),
    "Conservation of angular momentum versus constant angular velocity",
    "With no external torque the angular momentum Iω is conserved, not ω itself. If the body changes shape and its "
    "moment of inertia changes (a skater pulling in her arms, a diver tucking), ω changes. So Statement I is false. "
    "Statement II is the standard result K = Σ½mᵢ(rᵢω)² = ½Iω², true.",
    ["Statement I: τ = 0 → Iω constant; I can change → ω can change → false",
     "Statement II: K = ½Iω² → true"],
    why="Statement I would hold only for a body whose moment of inertia cannot change, such as a rigid wheel.",
    ncert="Class 11 Physics, 'System of Particles and Rotational Motion', conservation of angular momentum; "
          "kinematics of rotational motion", seconds=40)

a2 = F(1)
I_corner = (a2 / 12 + a2 / 12) + a2 / 2           # in units of M a^2
assert I_corner == F(2, 3)
add(T, "Moment of inertia and axis theorems", "Advanced", "numerical",
    "A thin uniform square plate has mass M and side a. Its moment of inertia about an axis in its plane, passing "
    "through its centre and parallel to one side, is Ma²/12. Its moment of inertia about an axis perpendicular to "
    "the plate and passing through one corner is:",
    place("2Ma²/3", ["Ma²/3", "7Ma²/12", "7Ma²/6"], "A"),
    "Perpendicular and parallel axes theorems together",
    "First use the perpendicular axes theorem at the centre: the axis perpendicular to the plate through the "
    "centre has I = Ma²/12 + Ma²/12 = Ma²/6. Then shift it parallel to the corner, a distance a/√2 away.",
    ["I_z(centre) = Ma²/12 + Ma²/12 = Ma²/6", "d = half-diagonal = a/√2 → Md² = Ma²/2",
     "I_corner = Ma²/6 + Ma²/2 = 2Ma²/3"],
    why="Ma²/3 is the moment of inertia about a side (in the plane); 7Ma²/12 starts from Ma²/12 instead of using "
        "the perpendicular axes theorem; 7Ma²/6 takes the shift distance as a instead of a/√2.",
    ncert="Class 11 Physics, 'System of Particles and Rotational Motion', theorems of perpendicular and parallel "
          "axes", seconds=100, recomputed=True)

I_ratio = F(1, 2) ** 2
w_ratio = 1 / I_ratio
assert w_ratio == 4 and 24 / w_ratio == 6
assert w_ratio ** 2 * I_ratio == 4                  # K = I w^2 / 2
add(T, "Torque and angular momentum", "Advanced", "numerical",
    "Treat the Earth as a uniform solid sphere spinning about its axis once in 24 h. Suppose it contracted, with no "
    "external torque and no change of mass, until its radius was half its present value. The new length of the day "
    "and the factor by which its rotational kinetic energy would change are:",
    place("6 h; rotational kinetic energy becomes 4 times",
          ["12 h; rotational kinetic energy becomes 2 times", "6 h; rotational kinetic energy is unchanged",
           "96 h; rotational kinetic energy becomes 1/4 times"], "C"),
    "Conservation of angular momentum and the energy that goes with it",
    "With no external torque, L = Iω is constant. For a uniform sphere I = (2/5)MR², so halving R makes I one "
    "quarter, and ω four times as large. Rotational KE = L²/(2I), so with L fixed it rises four times; the extra "
    "energy comes from the work done by the internal forces during contraction.",
    ["I' = I/4", "ω' = 4ω → T' = 24/4 = 6 h", "K' = L²/(2I') = 4K"],
    why="12 h and 2 times assume I ∝ R instead of R²; 'unchanged' wrongly assumes rotational KE is conserved along "
        "with L; 96 h inverts the change in ω.",
    ncert="Class 11 Physics, 'System of Particles and Rotational Motion', conservation of angular momentum",
    seconds=100, recomputed=True)

add(T, "Equilibrium of rigid bodies", "Advanced", "assertion_reason",
    AR_STEM.format(
        a="A rigid body cannot be in rotational equilibrium while a non-zero net external force acts on it.",
        r="Translational equilibrium requires the net external force to be zero and rotational equilibrium requires "
          "the net external torque to be zero; the two conditions are independent of each other."),
    ar("D"),
    "Conditions of translational and rotational equilibrium",
    "R is true: the two conditions of mechanical equilibrium are separate. A body can satisfy one without the "
    "other. For example, a single force acting through the centre of mass of a free body accelerates it but gives "
    "zero torque about the centre of mass, so the body is in rotational equilibrium while the net force is not "
    "zero. So A is false.",
    ["R: ΣF = 0 and Στ = 0 are independent conditions → true",
     "A: net force ≠ 0 with net torque = 0 is possible → false"],
    why="Because A is false, options A, B and C are wrong. A couple shows the converse: zero net force with a "
        "non-zero torque.",
    ncert="Class 11 Physics, 'System of Particles and Rotational Motion', equilibrium of a rigid body",
    seconds=55)

X0 = F(2 * 0 + 1 * 6, 3)
Vcm = F(2 * 3 + 1 * (-3), 3)
t_c = F(6, 3 + 3)
x_c = 0 + 3 * t_c
K_i, K_f = F(1, 2) * 2 * 9 + F(1, 2) * 1 * 9, F(1, 2) * 3 * Vcm ** 2
assert X0 == 2 and Vcm == 1 and x_c == 3 and X0 + Vcm * t_c == 3 and K_i - K_f == 12
truth = [True, False, True, True, False]
multi_key(truth, "acd")
add(T, "Centre of mass", "Advanced", "multi_statement",
    multi("On a smooth horizontal surface, a particle of mass 2 kg is at x = 0 moving at 3 m/s in the +x direction "
          "and, at the same instant, a particle of mass 1 kg is at x = 6 m moving at 3 m/s in the −x direction. "
          "They move along the x-axis, collide and stick together. Which of the following statements are correct?",
          ["At the initial instant the centre of mass of the two particles is at x = 2 m.",
           "The velocity of the centre of mass is 2 m/s in the +x direction.",
           "After the collision the combined body moves at 1 m/s in the +x direction.",
           "The particles collide at x = 3 m, which is also where the centre of mass is at that instant.",
           "The total kinetic energy of the particles is the same after the collision as before it."]),
    place("(a), (c) and (d) only", ["(a), (b) and (d) only", "(c), (d) and (e) only",
                                    "(a), (b), (c) and (d) only"], "B"),
    "Motion of the centre of mass of an isolated system",
    "No external horizontal force acts, so the centre of mass moves with a constant velocity, before and after the "
    "collision. The combined body after sticking moves with the velocity of the centre of mass.",
    ["(a) X = (2 × 0 + 1 × 6)/3 = 2 m, true", "(b) V = (2 × 3 − 1 × 3)/3 = 1 m/s, not 2 m/s → false",
     "(c) the stuck pair moves with V = 1 m/s, true",
     "(d) closing speed 6 m/s, gap 6 m → t = 1 s; x = 3 m; X(1 s) = 2 + 1 = 3 m, true",
     "(e) K before = 9 + 4.5 = 13.5 J, after = ½ × 3 × 1² = 1.5 J → false"],
    why="(b) adds speeds without the signs of the velocities; (e) ignores that a sticking (perfectly inelastic) "
        "collision always loses kinetic energy, here 12 J.",
    ncert="Class 11 Physics, 'System of Particles and Rotational Motion', motion of centre of mass; linear "
          "momentum of a system of particles", seconds=120, recomputed=True)


# =====================================================================================================================
# Gravitation (B3 I4 A3)
# =====================================================================================================================
T = "Gravitation"
G_ = 6.67e-11

assert close(1000 * g * 6.4e6, 6.4e10)
add(T, "Escape and orbital velocity", "Basic", "numerical",
    "Taking the Earth's radius as 6400 km and g = 10 m/s² at its surface, and neglecting air resistance and the "
    "Earth's rotation, the minimum energy that must be given to a body of mass 1000 kg at the Earth's surface so "
    "that it escapes from the Earth's gravity is:",
    place("6.4 × 10¹⁰ J", ["3.2 × 10¹⁰ J", "1.28 × 10¹¹ J", "6.4 × 10⁷ J"], "B"),
    "Energy needed for escape",
    "With the zero of potential energy at infinity, the body at the surface has U = −GMm/R. To escape it needs at "
    "least enough kinetic energy to bring its total energy to zero: K = GMm/R = mgR, since GM = gR².",
    ["E = GMm/R = mgR", "= 1000 × 10 × 6.4 × 10⁶ = 6.4 × 10¹⁰ J"],
    why="3.2 × 10¹⁰ J is mgR/2, the energy to raise the body only to a height R; 1.28 × 10¹¹ J doubles mgR; "
        "6.4 × 10⁷ J uses R in kilometres.",
    ncert="Class 11 Physics, 'Gravitation', escape speed", seconds=35, recomputed=True)

V_ = -G_ * 45 / 3
assert close(V_, -1.0e-9, rel=2e-3)
add(T, "Gravitational potential and energy", "Basic", "numerical",
    "Taking G = 6.67 × 10⁻¹¹ N m² kg⁻² and the gravitational potential to be zero at infinity, the gravitational "
    "potential at a distance of 3 m from a point mass of 45 kg is about:",
    place("−1.0 × 10⁻⁹ J kg⁻¹", ["−3.3 × 10⁻¹⁰ J kg⁻¹", "+1.0 × 10⁻⁹ J kg⁻¹", "−3.0 × 10⁻⁹ J kg⁻¹"], "A"),
    "Gravitational potential of a point mass",
    "The gravitational potential at distance r from a point mass M is V = −GM/r: the work done per unit mass by an "
    "external agent in bringing a test mass slowly from infinity. It is negative because gravity is attractive.",
    ["V = −GM/r = −(6.67 × 10⁻¹¹ × 45)/3", "= −1.0 × 10⁻⁹ J kg⁻¹"],
    why="−3.3 × 10⁻¹⁰ divides by r² (that is the field strength, in N kg⁻¹); +1.0 × 10⁻⁹ has the wrong sign; "
        "−3.0 × 10⁻⁹ forgets to divide by r.",
    ncert="Class 11 Physics, 'Gravitation', gravitational potential energy (gravitational potential)",
    seconds=35, recomputed=True)

add(T, "Kepler's laws", "Basic", "match_list",
    match_stem("Match List-I (scientist) with List-II (contribution described in NCERT's account of gravitation).",
               ["Ptolemy", "Tycho Brahe", "Johannes Kepler", "Galileo Galilei"],
               ["Recognised that all bodies, irrespective of their masses, are accelerated towards the Earth with a "
                "constant acceleration", "Proposed a geocentric model in which the planets move round the Earth",
                "Made detailed observations of the positions of the planets with the naked eye",
                "Analysed these observations and arrived at three laws of planetary motion"]),
    match_options({"A": "II", "B": "III", "C": "IV", "D": "I"},
                  [{"A": "III", "B": "II", "C": "IV", "D": "I"}, {"A": "II", "B": "IV", "C": "III", "D": "I"},
                   {"A": "II", "B": "III", "C": "I", "D": "IV"}], "D"),
    "History of the study of gravitation",
    "NCERT's introduction to gravitation: Ptolemy's geocentric model; Tycho Brahe's naked-eye observations of "
    "planetary positions; Kepler's three laws drawn from Brahe's data; Galileo's finding that all bodies fall with "
    "the same constant acceleration.",
    ["Ptolemy → geocentric model (II)", "Tycho Brahe → planetary observations (III)",
     "Kepler → three laws of planetary motion (IV)", "Galileo → equal acceleration of falling bodies (I)"],
    why="The wrong codes exchange the observer (Brahe) with the analyst (Kepler), or give Galileo's result on "
        "falling bodies to Kepler.",
    ncert="Class 11 Physics, 'Gravitation', introduction and Kepler's laws", seconds=40)

assert close((2 ** 3) ** 2 / 2 ** 2, 16)
add(T, "Law of gravitation", "Intermediate", "numerical",
    "Two identical uniform solid spheres of the same material are placed in contact. If each sphere is replaced by "
    "one of the same material but twice the radius, again placed in contact, the gravitational force between them "
    "becomes:",
    place("16 times", ["4 times", "64 times", "1/4 times"], "C"),
    "Scaling of the gravitational force with size",
    "For a uniform sphere M = (4/3)πR³ρ, so doubling R makes each mass 8 times. The distance between the centres of "
    "touching spheres is 2R, so it doubles. Each sphere attracts as a point mass at its centre.",
    ["F = GM²/(2R)² with M ∝ R³ → F ∝ R⁶/R² = R⁴", "Doubling R → F becomes 2⁴ = 16 times"],
    why="4 times treats the mass as proportional to R; 64 times ignores the larger separation; 1/4 times keeps the "
        "masses fixed and only doubles the separation.",
    ncert="Class 11 Physics, 'Gravitation', universal law of gravitation", seconds=60, recomputed=True)

V_c, V_x = -1.0, -1 / math.sqrt(1 + 3)          # in units of GM/R
assert close(V_x - V_c, 0.5)
add(T, "Gravitational potential and energy", "Intermediate", "numerical",
    "A thin uniform ring has mass M and radius R. Taking the gravitational potential to be zero at infinity, the "
    "minimum work needed to move a particle of mass m slowly from the centre of the ring to a point on its axis at "
    "a distance √3R from the centre is (G is the universal gravitational constant):",
    place("GMm/(2R)", ["−GMm/(2R)", "GMm/R", "(GMm/R)(1 − 1/√3)"], "A"),
    "Gravitational potential by superposition",
    "Potential is a scalar, so add the contributions −G dM/s of all mass elements. Every element of the ring is the "
    "same distance s from a point on the axis: s = R at the centre and s = √(R² + 3R²) = 2R at the second point. The "
    "work done by an external agent is m(V_final − V_initial).",
    ["V(centre) = −GM/R", "V(axis, √3R) = −GM/(2R)", "W = m[−GM/(2R) − (−GM/R)] = GMm/(2R)"],
    why="−GMm/(2R) has the sign reversed (the agent must do positive work to pull m away from the ring); GMm/R "
        "assumes the far point is at zero potential; (GMm/R)(1 − 1/√3) takes the distance from the ring as √3R "
        "instead of 2R.",
    ncert="Class 11 Physics, 'Gravitation', gravitational potential energy", seconds=80, recomputed=True)

add(T, "Gravitational potential and energy", "Intermediate", "assertion_reason",
    AR_STEM.format(
        a="For a height h much smaller than the Earth's radius R, the gain in gravitational potential energy when a "
          "body of mass m is raised from the surface to the height h may be taken as mgh.",
        r="The exact gain is GMm/R − GMm/(R + h) = GMmh/[R(R + h)], which is nearly GMmh/R² = mgh when h ≪ R."),
    ar("A"),
    "mgh as an approximation to −GMm/r",
    "The general expression for gravitational potential energy is −GMm/r. The difference between r = R + h and "
    "r = R reduces to GMmh/R² when R + h ≈ R, and GM/R² = g. So R is exactly the derivation of A.",
    ["ΔU = GMm[1/R − 1/(R + h)] = GMmh/[R(R + h)]", "h ≪ R → ΔU ≈ GMmh/R² = mgh",
     "Both true; R explains A → option A"],
    why="R is the reason, not a separate fact, so B is wrong; both statements are true, so C and D are wrong.",
    ncert="Class 11 Physics, 'Gravitation', gravitational potential energy", seconds=50)

add(T, "Escape and orbital velocity", "Intermediate", "statement_pair",
    SP_STEM.format(
        s1="If the mass of the Earth were doubled with its radius unchanged, the escape speed from its surface "
           "would become √2 times its present value.",
        s2="If both the mass and the radius of the Earth were doubled, the acceleration due to gravity at its "
           "surface would remain unchanged."),
    sp("C"),
    "Dependence of escape speed and g on mass and radius",
    "v_e = √(2GM/R): doubling M alone multiplies it by √2, so Statement I is true. g = GM/R²: doubling both M and R "
    "gives 2/4 = 1/2, so g would halve, and Statement II is false. (It is the escape speed, ∝ √(M/R), that would "
    "stay unchanged.)",
    ["Statement I: v_e ∝ √M at fixed R → √2 times → true",
     "Statement II: g ∝ M/R² → 2/2² = 1/2 → false"],
    why="Statement II applies the M/R ratio, which governs escape speed, to g, which depends on M/R².",
    ncert="Class 11 Physics, 'Gravitation', acceleration due to gravity of the earth; escape speed", seconds=45)

# binary: masses M and 2M, separation d; M orbits at 2d/3 from the CM
w2 = (G_ * 2 * 1.0 / 1.0 ** 2) / (2 / 3)        # G M (2M)/d^2 = M w^2 (2d/3) with M = d = 1
assert close(w2, 3 * G_)
add(T, "Law of gravitation", "Advanced", "numerical",
    "Two stars of masses M and 2M, a distance d apart, revolve in circles about their common centre of mass under "
    "their mutual gravitational attraction alone. Their common period of revolution is (G is the universal "
    "gravitational constant):",
    place("2π√(d³/(3GM))", ["2π√(d³/(GM))", "2π√(d³/(2GM))", "2π√(d³/(4GM))"], "D"),
    "Gravitation with the centre of mass: a binary system",
    "Each star moves on a circle about the centre of mass, not about the other star. The star of mass M is at "
    "2d/3 from the centre of mass. The gravitational force between the stars, G(M)(2M)/d², supplies its centripetal "
    "force Mω²(2d/3).",
    ["r(M) = 2M·d/(3M) = 2d/3", "G·2M²/d² = Mω²(2d/3) → ω² = 3GM/d³", "T = 2π/ω = 2π√(d³/(3GM))"],
    shortcut="For two bodies, ω² = G(m₁ + m₂)/d³: here G(3M)/d³.",
    why="2π√(d³/(GM)) treats the star M as orbiting a fixed mass M at distance d; 2π√(d³/(2GM)) has M orbit the "
        "fixed 2M star at distance d; 2π√(d³/(4GM)) takes the centre of mass at the midpoint d/2.",
    ncert="Class 11 Physics, 'Gravitation', universal law of gravitation; 'System of Particles and Rotational "
          "Motion', centre of mass", seconds=120, recomputed=True)

E1 = F(1) - F(1, 2)                       # GMm/R units: reach height R and stop
E2 = (-F(1, 2 * 2)) - (-F(1))            # orbit at radius 2R: E = -GMm/(2r)
assert E1 / E2 == F(2, 3)
add(T, "Satellite energy and period", "Advanced", "numerical",
    "A body at rest on the Earth's surface needs a minimum energy E₁ to be thrown vertically up to a height equal "
    "to the Earth's radius R, and a minimum energy E₂ to be placed in a circular orbit at a height R above the "
    "surface. Neglecting air resistance and the Earth's rotation, E₁ : E₂ is:",
    place("2 : 3", ["3 : 2", "1 : 1", "1 : 2"], "B"),
    "Energy of a body at a height versus energy of a satellite",
    "To just reach height R the body only needs the rise in potential energy. To orbit at radius 2R it must also have "
    "the orbital kinetic energy GMm/(2·2R); its total energy there is −GMm/(4R).",
    ["E₁ = −GMm/(2R) − (−GMm/R) = GMm/(2R)", "E₂ = −GMm/(4R) − (−GMm/R) = 3GMm/(4R)",
     "E₁ : E₂ = (1/2) : (3/4) = 2 : 3"],
    why="3 : 2 inverts the ratio; 1 : 1 forgets the satellite's kinetic energy; 1 : 2 adds the kinetic energy of an "
        "orbit at the SURFACE, GMm/(2R), instead of at radius 2R.",
    ncert="Class 11 Physics, 'Gravitation', energy of an orbiting satellite", seconds=110, recomputed=True)

truth = [True, False, True, True, False]
multi_key(truth, "acd")
assert close(math.sqrt(2), (2 / 1) ** 0.5) and close((1 / 2) ** 1.5, 1 / (2 * math.sqrt(2)))
add(T, "Satellite energy and period", "Advanced", "multi_statement",
    multi("A satellite in a circular orbit of radius 2r round the Earth is shifted to a circular orbit of radius r. "
          "Taking the potential energy to be zero at infinity, which of the following statements are correct?",
          ["Its kinetic energy becomes twice as large.",
           "Its gravitational potential energy increases.",
           "Its total mechanical energy decreases.",
           "Its orbital speed becomes √2 times as large.",
           "Its period of revolution becomes half as large."]),
    place("(a), (c) and (d) only", ["(a), (b) and (d) only", "(c), (d) and (e) only",
                                    "(a), (c), (d) and (e) only"], "C"),
    "Dependence of satellite energies, speed and period on orbit radius",
    "K = GMm/(2r), U = −GMm/r and E = −GMm/(2r); v = √(GM/r) and T ∝ r^(3/2). Halving the radius doubles K, doubles "
    "the magnitude of both U and E (making them more negative), raises v by √2 and reduces T by a factor 2√2.",
    ["(a) K ∝ 1/r → 2K, true", "(b) U = −GMm/r becomes more negative → it decreases → false",
     "(c) E = −GMm/(2r) becomes more negative → decreases, true", "(d) v ∝ r^(−1/2) → √2 times, true",
     "(e) T ∝ r^(3/2) → (1/2)^(3/2) = 1/(2√2) times, not 1/2 → false"],
    why="(b) confuses a larger magnitude with a larger value: −2x is less than −x. (e) uses T ∝ r instead of "
        "Kepler's T² ∝ r³.",
    ncert="Class 11 Physics, 'Gravitation', earth satellites; energy of an orbiting satellite", seconds=100,
    recomputed=True)


# =====================================================================================================================
# Properties of Solids and Liquids (B5 I7 A5)
# =====================================================================================================================
T = "Properties of Solids and Liquids"

assert close(0.5 * (1e-3 / (1e-2 * 1)), 0.05)        # 0.5 g cm^-1 s^-1 -> kg m^-1 s^-1
add(T, "Viscosity and Stokes' law", "Basic", "numerical",
    "The coefficient of viscosity of a liquid is 0.5 poise, where 1 poise = 1 g cm⁻¹ s⁻¹ (the CGS unit). Its value "
    "in SI units is:",
    place("0.05 Pa s", ["5 Pa s", "0.5 Pa s", "0.005 Pa s"], "C"),
    "Conversion between CGS and SI units of viscosity",
    "1 g cm⁻¹ s⁻¹ = 10⁻³ kg / (10⁻² m × 1 s) = 0.1 kg m⁻¹ s⁻¹ = 0.1 Pa s. So 1 poise = 0.1 Pa s.",
    ["1 poise = 10⁻³ kg × 10² m⁻¹ s⁻¹ = 0.1 Pa s", "0.5 poise = 0.05 Pa s"],
    why="5 Pa s multiplies by 10 instead of dividing; 0.5 Pa s assumes the two units are equal; 0.005 Pa s divides "
        "by 100 instead of 10, treating 1 poise as 10⁻² Pa s.",
    ncert="Class 11 Physics, 'Mechanical Properties of Fluids', viscosity", seconds=30, recomputed=True)

assert close(math.sqrt(2 * g * 5), 10)
add(T, "Bernoulli's principle", "Basic", "numerical",
    "Water flows out of a small hole in the side of a wide open tank, 5 m below the free surface of the water. "
    "Taking g = 10 m/s², the speed of efflux is:",
    place("10 m/s", ["100 m/s", "5√2 m/s", "50 m/s"], "A"),
    "Torricelli's law",
    "Applying Bernoulli's principle between the free surface (speed ≈ 0, pressure Pₐ) and the hole (pressure Pₐ), "
    "the speed of efflux is √(2gh), the speed a body gains in falling freely through h.",
    ["v = √(2gh) = √(2 × 10 × 5)", "= √100 = 10 m/s"],
    why="100 m/s forgets the square root; 5√2 m/s uses √(gh); 50 m/s uses gh.",
    ncert="Class 11 Physics, 'Mechanical Properties of Fluids', Bernoulli's principle (speed of efflux: "
          "Torricelli's law)", seconds=25, recomputed=True)

X_ = 20 + (220 - 20) / 100 * 50
assert close(X_, 120)
add(T, "Thermal expansion and calorimetry", "Basic", "numerical",
    "On a new temperature scale X, the melting point of ice is 20 °X and the boiling point of water is 220 °X, both "
    "at standard pressure, and the scale is linear. A temperature of 50 °C on this scale is:",
    place("120 °X", ["100 °X", "70 °X", "110 °X"], "D"),
    "Relation between linear temperature scales",
    "For any two linear scales, (reading − ice point)/(steam point − ice point) is the same. So "
    "(X − 20)/(220 − 20) = (C − 0)/(100 − 0).",
    ["(X − 20)/200 = 50/100", "X − 20 = 100", "X = 120 °X"],
    why="100 °X forgets to add the ice-point offset of 20; 70 °X just adds 20 to 50; 110 °X multiplies 50 by "
        "220/100 without the offset.",
    ncert="Class 11 Physics, 'Thermal Properties of Matter', temperature and heat; measurement of temperature",
    seconds=35, recomputed=True)

add(T, "Heat transfer", "Basic", "direct",
    "Cooking pots are often given a copper coating on the bottom mainly because copper:",
    place("Is a good conductor of heat, so it spreads the heat over the bottom of the pot",
          ["Is a poor conductor of heat, so it keeps the heat inside the food",
           "Has a very high specific heat capacity, so it stores a large amount of heat",
           "Reflects heat radiation back into the pot"], "B"),
    "Thermal conductivity and its uses",
    "Copper has a high thermal conductivity. A copper-coated bottom conducts heat quickly and spreads it evenly "
    "over the base, so the food is heated uniformly.",
    ["Copper → high thermal conductivity", "Good conductor → faster, more uniform heating of the pot's base"],
    why="Copper is a good, not a poor, conductor; its specific heat capacity is low, not high; reflection of "
        "radiation is not why it is used on the bottom of a pot heated by a flame.",
    ncert="Class 11 Physics, 'Thermal Properties of Matter', heat transfer (conduction)", seconds=25)

add(T, "Elasticity and moduli", "Basic", "direct",
    "The ropes of cranes used to lift heavy loads are made of a large number of thin wires braided together, rather "
    "than of a single thick wire of the same total cross-section. The main reason is that the braided rope:",
    place("Is easier to manufacture and more flexible, while giving the required strength",
          ["Has a much larger Young's modulus than a single wire of the same material",
           "Is lighter for the same cross-sectional area of metal",
           "Stretches more under the load, so it stores more energy"], "A"),
    "Application of elastic behaviour: design of crane ropes",
    "The required radius of the rope is fixed by the load and the yield strength of steel (with a safety factor). "
    "A single thick wire of that radius would be practically a rigid rod; braiding many thin wires gives the same "
    "strength with ease of manufacture, flexibility and strength.",
    ["Required cross-section is set by load and yield strength", "Many thin braided wires → flexible, easy to make"],
    why="Young's modulus is a property of the material, not of how the wires are arranged; the mass of metal for "
        "the same cross-section is the same; extra stretching is not the aim.",
    ncert="Class 11 Physics, 'Mechanical Properties of Solids', applications of elastic behaviour of materials",
    seconds=30)

assert close(2 ** 2 * 0.5 ** 4, 0.25)
add(T, "Heat transfer", "Intermediate", "numerical",
    "A sphere radiates energy at the rate P as a black body at absolute temperature T. Another black-body sphere has "
    "twice the radius and is at an absolute temperature T/2. The rate at which it radiates energy is:",
    place("P/4", ["P/2", "4P", "P/8"], "B"),
    "Stefan-Boltzmann law",
    "The power radiated by a black body is P = σAT⁴, with A = 4πr² for a sphere. So P ∝ r²T⁴.",
    ["P'/P = (r'/r)² × (T'/T)⁴", "= 2² × (1/2)⁴ = 4/16 = 1/4"],
    why="P/2 uses T² instead of T⁴; 4P ignores the change in temperature; P/8 takes the area as proportional to r "
        "instead of r².",
    ncert="Class 11 Physics, 'Thermal Properties of Matter', radiation (Stefan-Boltzmann law)", seconds=40,
    recomputed=True)

P_in = 1.0e5 + 1000 * g * 0.10 + 2 * 0.07 / 1e-4
assert close(P_in, 1.024e5)
add(T, "Surface tension and capillarity", "Intermediate", "numerical",
    "An air bubble of radius 0.1 mm is formed 10 cm below the surface of water in an open vessel. The surface "
    "tension of water is 0.07 N/m, its density is 1000 kg/m³, the atmospheric pressure is 1.0 × 10⁵ Pa and "
    "g = 10 m/s². The pressure inside the bubble is:",
    place("1.024 × 10⁵ Pa", ["1.014 × 10⁵ Pa", "1.010 × 10⁵ Pa", "1.038 × 10⁵ Pa"], "D"),
    "Pressure inside an air bubble in a liquid",
    "The water just outside the bubble is at Pₐ + ρgh. An air bubble in a liquid has one liquid surface, so the "
    "pressure inside exceeds this by 2S/r.",
    ["Pressure outside = 1.0 × 10⁵ + 1000 × 10 × 0.10 = 1.010 × 10⁵ Pa", "2S/r = 0.14/10⁻⁴ = 1400 Pa",
     "P_inside = 1.010 × 10⁵ + 1400 = 1.024 × 10⁵ Pa"],
    why="1.014 × 10⁵ Pa leaves out the hydrostatic pressure ρgh; 1.010 × 10⁵ Pa leaves out the surface-tension "
        "term; 1.038 × 10⁵ Pa uses 4S/r, which applies to a soap bubble with two surfaces.",
    ncert="Class 11 Physics, 'Mechanical Properties of Fluids', surface tension (excess pressure inside a drop and "
          "a bubble)", seconds=60, recomputed=True)

assert close(5e-4 * 40 * 100, 2.0)
add(T, "Thermal expansion and calorimetry", "Intermediate", "numerical",
    "The coefficient of volume expansion of a liquid is 5 × 10⁻⁴ K⁻¹. When the liquid is heated through 40 K, its "
    "density decreases by about:",
    place("2%", ["0.67%", "6%", "0.02%"], "C"),
    "Change of density with temperature",
    "The mass stays fixed while the volume grows by the factor (1 + γΔT), so ρ' = ρ/(1 + γΔT) ≈ ρ(1 − γΔT) when "
    "γΔT ≪ 1. The fractional decrease in density is γΔT.",
    ["Δρ/ρ ≈ γΔT = 5 × 10⁻⁴ × 40 = 0.02", "Percentage decrease ≈ 2%"],
    why="0.67% treats 5 × 10⁻⁴ as a volume coefficient and divides by 3; 6% multiplies by 3, treating the given value "
        "as a linear coefficient; 0.02% leaves out the factor 100.",
    ncert="Class 11 Physics, 'Thermal Properties of Matter', thermal expansion", seconds=40, recomputed=True)

H_ = 0.021 * 1.0 * 40 / 0.05
m_ice = H_ * 3600 / 3.36e5
assert close(H_, 16.8) and close(m_ice, 0.18)
add(T, "Heat transfer", "Intermediate", "numerical",
    "The walls of an ice box have a total area of 1.0 m² and a thickness of 5 cm, and are made of a material of "
    "thermal conductivity 0.021 W m⁻¹ K⁻¹. The ice box contains ice at 0 °C and the outside temperature is 40 °C. "
    "Taking the latent heat of fusion of ice as 3.36 × 10⁵ J kg⁻¹ and neglecting heat flow other than by conduction "
    "through the walls, the mass of ice that melts in one hour is:",
    place("180 g", ["3 g", "1.8 g", "0.18 g"], "A"),
    "Steady-state conduction combined with latent heat",
    "In the steady state the heat current through the walls is H = KAΔT/d. All this heat melts ice at 0 °C.",
    ["H = 0.021 × 1.0 × 40 / 0.05 = 16.8 W", "Heat in 1 h = 16.8 × 3600 = 60480 J",
     "m = 60480 / 3.36 × 10⁵ = 0.18 kg = 180 g"],
    why="3 g is the mass melted in one minute; 1.8 g puts the thickness as 5 m instead of 0.05 m (a factor 100); "
        "0.18 g leaves the answer in the wrong unit (0.18 kg read as grams).",
    ncert="Class 11 Physics, 'Thermal Properties of Matter', conduction; latent heat", seconds=80, recomputed=True)

Q = {"A": 1 * 4200 * 10, "B": 1 * 3.36e5, "C": 0.1 * 2.26e6, "D": 1 * 2100 * 10}
assert [round(Q[k] / 1000) for k in "ABCD"] == [42, 336, 226, 21]
add(T, "Thermal expansion and calorimetry", "Intermediate", "match_list",
    match_stem("Take the specific heat capacity of water as 4200 J kg⁻¹ K⁻¹, that of ice as 2100 J kg⁻¹ K⁻¹, the "
               "latent heat of fusion of ice as 3.36 × 10⁵ J kg⁻¹ and the latent heat of vaporisation of water as "
               "2.26 × 10⁶ J kg⁻¹. Match List-I (process, at standard pressure) with List-II (heat needed).",
               ["Warming 1 kg of water from 20 °C to 30 °C", "Melting 1 kg of ice at 0 °C into water at 0 °C",
                "Turning 0.1 kg of water at 100 °C into steam at 100 °C",
                "Warming 1 kg of ice from −10 °C to 0 °C (without melting it)"],
               ["226 kJ", "21 kJ", "42 kJ", "336 kJ"]),
    match_options({"A": "III", "B": "IV", "C": "I", "D": "II"},
                  [{"A": "II", "B": "IV", "C": "I", "D": "III"}, {"A": "III", "B": "I", "C": "IV", "D": "II"},
                   {"A": "III", "B": "IV", "C": "II", "D": "I"}], "B"),
    "Sensible heat (mcΔT) and latent heat (mL)",
    "A change of temperature needs Q = mcΔT; a change of state at constant temperature needs Q = mL.",
    ["A: 1 × 4200 × 10 = 42 kJ (III)", "B: 1 × 3.36 × 10⁵ = 336 kJ (IV)", "C: 0.1 × 2.26 × 10⁶ = 226 kJ (I)",
     "D: 1 × 2100 × 10 = 21 kJ (II)"],
    why="The wrong codes swap the specific heats of ice and water, or the two latent heats (forgetting that only "
        "0.1 kg is vaporised).",
    ncert="Class 11 Physics, 'Thermal Properties of Matter', specific heat capacity; change of state (latent heat)",
    seconds=70, recomputed=True)

add(T, "Elasticity and moduli", "Intermediate", "statement_pair",
    SP_STEM.format(
        s1="Within the elastic limit, the elastic potential energy stored per unit volume of a stretched wire is "
           "½ × stress × strain.",
        s2="For the same tensile stress, a wire of a material with a larger Young's modulus stores more elastic "
           "energy per unit volume."),
    sp("C"),
    "Elastic potential energy density",
    "The work done in stretching a wire is ½Fl, so the energy per unit volume is ½(F/A)(l/L) = ½ × stress × strain: "
    "Statement I is true. With strain = stress/Y, the energy density is stress²/(2Y), so at the same stress a "
    "larger Y gives LESS stored energy per unit volume: Statement II is false.",
    ["u = ½ σ ε (Statement I, true)", "u = σ²/(2Y) → larger Y, smaller u at fixed σ (Statement II, false)"],
    why="Statement II would be right for the same STRAIN (u = ½Yε²), not for the same stress.",
    ncert="Class 11 Physics, 'Mechanical Properties of Solids', elastic potential energy in a stretched wire",
    seconds=50)

add(T, "Heat transfer", "Intermediate", "statement_pair",
    SP_STEM.format(
        s1="Newton's law of cooling, that the rate of loss of heat is proportional to the temperature difference "
           "between a body and its surroundings, holds for small temperature differences.",
        s2="A body cooling according to Newton's law takes longer to cool through 10 °C when its temperature is "
           "closer to that of the surroundings."),
    sp("A"),
    "Newton's law of cooling",
    "NCERT states the law for a small temperature difference between the body and its surroundings, so Statement I "
    "is true. Since −dT/dt = k(T − T₀), the rate of cooling is smaller when T is closer to T₀, so the same 10 °C "
    "drop takes more time near the surrounding temperature. Statement II is true.",
    ["Statement I: law valid for small (T − T₀) → true",
     "Statement II: rate ∝ (T − T₀) → slower cooling near T₀ → more time → true"],
    why="Both statements are true; Statement II follows from the law, since the cooling rate falls as the "
        "temperature difference falls.",
    ncert="Class 11 Physics, 'Thermal Properties of Matter', Newton's law of cooling", seconds=45)

assert 2 ** 5 == 32
add(T, "Viscosity and Stokes' law", "Advanced", "numerical",
    "A small metal sphere falls through a viscous liquid with its terminal velocity, and the viscous force on it "
    "dissipates energy at the rate P. A sphere of the same metal with twice the radius falls through the same liquid "
    "with its terminal velocity. Assuming Stokes' law holds, the rate at which the viscous force dissipates energy "
    "on the second sphere is:",
    place("32P", ["16P", "8P", "4P"], "D"),
    "Terminal velocity and viscous power",
    "At terminal velocity v = 2r²(ρ − σ)g/(9η), so v ∝ r². The viscous force equals the weight minus the buoyancy, "
    "6πηrv ∝ r³. The power dissipated is F v ∝ r³ × r² = r⁵.",
    ["v_t ∝ r² → 4 times", "F = 6πηrv_t ∝ r³ → 8 times", "P = Fv_t ∝ r⁵ → 2⁵ = 32 times"],
    why="16P takes F ∝ r²; 8P gives only the change in the force; 4P gives only the change in the terminal velocity.",
    ncert="Class 11 Physics, 'Mechanical Properties of Fluids', Stokes' law and terminal velocity", seconds=90,
    recomputed=True)

v2 = math.sqrt(1 ** 2 + 2 * g * 0.15)
r2 = 1.0 * math.sqrt(1 / v2)
assert close(v2, 2) and close(r2, 1 / math.sqrt(2))
add(T, "Bernoulli's principle", "Advanced", "numerical",
    "A steady, smooth stream of water comes vertically down out of a tap whose opening has a radius of 1 cm, with a "
    "speed of 1 m/s at the opening. Taking g = 10 m/s² and neglecting viscosity, air resistance and surface tension, "
    "the radius of the stream 15 cm below the opening is:",
    place("1/√2 cm", ["1/2 cm", "1/4 cm", "√2 cm"], "C"),
    "Free fall combined with the equation of continuity",
    "Each element of water falls freely, so its speed grows as v² = v₀² + 2gh. The same volume flows through every "
    "cross-section per second, so Av is constant and the stream narrows.",
    ["v² = 1 + 2 × 10 × 0.15 = 4 → v = 2 m/s", "πr²v = constant → r² = (1 cm)² × (1/2)",
     "r = 1/√2 cm ≈ 0.71 cm"],
    why="1/2 cm takes r ∝ 1/v instead of A ∝ 1/v; 1/4 cm uses the ratio of v² for the radius; √2 cm assumes the "
        "stream widens as it speeds up.",
    ncert="Class 11 Physics, 'Mechanical Properties of Fluids', streamline flow (equation of continuity)",
    seconds=100, recomputed=True)

add(T, "Heat transfer", "Advanced", "numerical",
    "Two solid spheres of the same material, with radii in the ratio 1 : 2, have the same surface finish and are at "
    "the same temperature, in the same surroundings, losing heat only by radiation. The ratio of their initial "
    "rates of fall of temperature (smaller sphere : larger sphere) is:",
    place("2 : 1", ["1 : 2", "4 : 1", "1 : 1"], "B"),
    "Rate of cooling by radiation depends on area/heat capacity",
    "The rate of heat loss by radiation is proportional to the surface area (same T, same surroundings, same "
    "surface). The fall of temperature is this rate divided by the heat capacity mc, which is proportional to the "
    "volume. So dT/dt ∝ r²/r³ = 1/r.",
    ["Heat loss rate ∝ 4πr²", "Heat capacity ∝ (4/3)πr³ρc", "dT/dt ∝ 1/r → (1/1) : (1/2) = 2 : 1"],
    why="1 : 2 inverts the ratio; 4 : 1 uses only the ratio of the areas inverted (1/r²); 1 : 1 assumes that the "
        "same temperature means the same rate of cooling.",
    ncert="Class 11 Physics, 'Thermal Properties of Matter', radiation; specific heat capacity", seconds=80,
    recomputed=True)
assert close((1 / 1) / (1 / 2), 2)

add(T, "Thermal expansion and calorimetry", "Advanced", "assertion_reason",
    AR_STEM.format(
        a="During a long spell of very cold weather, a deep lake freezes at its surface while the water near its "
          "bottom stays liquid, at about 4 °C.",
        r="Water has its maximum density at about 4 °C, so as the lake cools, water at 4 °C sinks to the bottom "
          "while the colder, less dense water stays at the top and freezes there."),
    ar("A"),
    "Anomalous expansion of water",
    "Most liquids become denser as they cool, but water contracts only down to about 4 °C and expands on further "
    "cooling. As a lake cools, surface water sinks until the whole lake is near 4 °C; after that, colder water is "
    "lighter and stays on top, where it freezes. The ice and the cold surface layer insulate the water below, which "
    "stays liquid near 4 °C, allowing aquatic life to survive. R is the reason for A.",
    ["Water: maximum density at about 4 °C", "Water at 4 °C collects at the bottom; colder water stays on top",
     "Freezing starts at the surface; the bottom stays near 4 °C → A true, R explains it"],
    why="R is the cause of A, not a separate fact, so B is wrong; both statements are true, so C and D are wrong.",
    ncert="Class 11 Physics, 'Thermal Properties of Matter', thermal expansion (anomalous expansion of water)",
    seconds=50)

stress, strain = 50 / 0.5e-6, 50 / 0.5e-6 / 1e11
ext = strain * 1.5
U_ = 0.5 * 50 * ext
assert close(stress, 1e8) and close(strain, 1e-3) and close(ext, 1.5e-3) and close(U_, 0.0375)
assert close(ext / 4, 0.375e-3)
truth = [True, True, True, False, False]
multi_key(truth, "abc")
add(T, "Elasticity and moduli", "Advanced", "multi_statement",
    multi("A wire 1.5 m long, of cross-sectional area 0.5 mm² and Young's modulus 1 × 10¹¹ N/m², hangs from a rigid "
          "support and carries a load that exerts a force of 50 N on it. Within the elastic limit, which of the "
          "following statements are correct?",
          ["The tensile stress in the wire is 1 × 10⁸ N/m².",
           "The longitudinal strain is 1 × 10⁻³.",
           "The extension of the wire is 1.5 mm.",
           "The elastic potential energy stored in the wire is 75 mJ.",
           "A wire of the same material and length but twice the diameter, carrying the same load, would extend "
           "by 0.75 mm."]),
    place("(a), (b) and (c) only", ["(a), (b), (c) and (d) only", "(a), (c) and (e) only",
                                    "(b), (d) and (e) only"], "D"),
    "Stress, strain, extension and stored energy of a wire",
    "Stress = F/A, strain = stress/Y, extension = strain × L, and the energy stored = ½ × F × extension. Doubling "
    "the diameter makes the area 4 times, so the extension falls to one quarter.",
    ["(a) 50 / (0.5 × 10⁻⁶) = 1 × 10⁸ N/m², true", "(b) 10⁸ / 10¹¹ = 10⁻³, true",
     "(c) 10⁻³ × 1.5 m = 1.5 mm, true", "(d) U = ½ × 50 × 1.5 × 10⁻³ = 37.5 mJ, not 75 mJ → false",
     "(e) area × 4 → extension 1.5/4 = 0.375 mm, not 0.75 mm → false"],
    why="(d) forgets the ½ in U = ½F·Δl; (e) treats the area as proportional to the diameter instead of its "
        "square.",
    ncert="Class 11 Physics, 'Mechanical Properties of Solids', Young's modulus; elastic potential energy in a "
          "stretched wire", seconds=110, recomputed=True)


# =====================================================================================================================
# Thermodynamics (B3 I4 A3)  -- no heat engines, Carnot, efficiency or COP
# =====================================================================================================================
T = "Thermodynamics"
R_ = 8.3

add(T, "Zeroth and first law", "Basic", "direct",
    "A gas enclosed in a cylinder is said to be in thermodynamic equilibrium when:",
    place("Its macroscopic variables, such as pressure, volume, temperature, mass and composition, do not change "
          "with time",
          ["Its molecules have stopped moving", "Its temperature is 0 °C and its pressure is 1 atm",
           "Its internal energy is zero"], "C"),
    "Thermodynamic equilibrium",
    "NCERT: a system is in thermodynamic equilibrium if the macroscopic variables that characterise it do not "
    "change in time. Its molecules keep moving randomly; equilibrium is a property of the macroscopic state, not of "
    "any particular values of P and T.",
    ["Equilibrium → P, V, T, mass and composition constant in time",
     "Molecular motion continues in equilibrium"],
    why="Molecular motion never stops in a gas at any real temperature; equilibrium can occur at any pressure and "
        "temperature; the internal energy of a gas in equilibrium is not zero.",
    ncert="Class 11 Physics, 'Thermodynamics', thermal equilibrium", seconds=25)

add(T, "Zeroth and first law", "Basic", "match_list",
    match_stem("Match List-I (term used in thermodynamics) with List-II (its meaning).",
               ["Diathermic wall", "Adiabatic wall", "Heat reservoir", "Cyclic process"],
               ["A body so large that its temperature does not change appreciably when heat flows into or out of it",
                "A process in which the system returns to its initial state",
                "A conducting wall that allows heat to flow through it",
                "An insulating wall that does not allow heat to flow through it"]),
    match_options({"A": "III", "B": "IV", "C": "I", "D": "II"},
                  [{"A": "IV", "B": "III", "C": "I", "D": "II"}, {"A": "III", "B": "IV", "C": "II", "D": "I"},
                   {"A": "I", "B": "IV", "C": "III", "D": "II"}], "A"),
    "Basic terms of thermodynamics",
    "A diathermic (conducting) wall lets heat pass; an adiabatic (insulating) wall does not. A heat reservoir is so "
    "large that its temperature stays fixed while it exchanges heat. In a cyclic process the system comes back to "
    "its initial state.",
    ["Diathermic → conducting (III)", "Adiabatic → insulating (IV)", "Heat reservoir → constant temperature (I)",
     "Cyclic process → returns to initial state (II)"],
    why="The wrong codes exchange the two kinds of wall, or the reservoir with the cyclic process.",
    ncert="Class 11 Physics, 'Thermodynamics', thermal equilibrium; thermodynamic processes", seconds=40)

add(T, "Isothermal and adiabatic processes", "Basic", "assertion_reason",
    AR_STEM.format(
        a="No work is done by or on an ideal gas in an isochoric process.",
        r="In an isochoric process, the temperature of the gas remains constant."),
    ar("C"),
    "Isochoric process",
    "In an isochoric process the volume is constant, so W = ∫P dV = 0: A is true. The heat supplied changes the "
    "internal energy and therefore the temperature; it is the isothermal process, not the isochoric one, in which "
    "the temperature stays constant. So R is false.",
    ["A: ΔV = 0 → W = 0 → true", "R: Q = ΔU = nC_vΔT ≠ 0 in general → T changes → false"],
    why="R describes an isothermal process, so options A and B are wrong; A is true, so D is wrong.",
    ncert="Class 11 Physics, 'Thermodynamics', thermodynamic processes (isochoric process)", seconds=30)

W1, W2 = 2e5 * 1e-3, 1e5 * 1e-3
assert close(W1 - W2, 100)
add(T, "Zeroth and first law", "Intermediate", "numerical",
    "An ideal gas is taken from state A (pressure 1 × 10⁵ Pa, volume 1 L) to state B (pressure 2 × 10⁵ Pa, volume "
    "2 L) by two different paths. Path 1: first at constant volume to 2 × 10⁵ Pa, then at constant pressure to 2 L. "
    "Path 2: first at constant pressure to 2 L, then at constant volume to 2 × 10⁵ Pa. The heat absorbed along "
    "path 1 exceeds that absorbed along path 2 by:",
    place("100 J", ["Zero", "200 J", "300 J"], "B"),
    "Heat depends on the path; internal energy does not",
    "Both paths join the same two states, so ΔU is the same. By the first law Q = ΔU + W, so the difference in heat "
    "equals the difference in the work done by the gas, which is the area under each path on the P–V diagram.",
    ["Path 1: W₁ = (2 × 10⁵)(1 × 10⁻³) = 200 J (expansion at the higher pressure)",
     "Path 2: W₂ = (1 × 10⁵)(1 × 10⁻³) = 100 J", "Q₁ − Q₂ = W₁ − W₂ = 100 J"],
    why="Zero assumes heat is a state function like U; 200 J and 300 J give the work along path 1 alone or the sum "
        "of the two works.",
    ncert="Class 11 Physics, 'Thermodynamics', first law of thermodynamics; state variables", seconds=70,
    recomputed=True)

assert close(1 / 0.693, 1.443, rel=1e-3)
add(T, "Isothermal and adiabatic processes", "Intermediate", "numerical",
    "Two identical samples of an ideal gas start from the same state (P, V, T). One expands reversibly at constant "
    "pressure to volume 2V; the other expands reversibly and isothermally to volume 2V. Taking ln 2 = 0.693, the "
    "ratio of the work done by the gas at constant pressure to that done isothermally is about:",
    place("1.44", ["0.69", "1", "2"], "D"),
    "Work in isobaric and isothermal expansions",
    "At constant pressure W₁ = P(2V − V) = PV. Isothermally W₂ = nRT ln(2V/V) = PV ln 2, since nRT = PV at the "
    "start. The ratio is 1/ln 2.",
    ["W_isobaric = PV", "W_isothermal = PV ln 2 = 0.693 PV", "Ratio = 1/0.693 ≈ 1.44"],
    why="0.69 is the inverse ratio; 1 assumes equal work for the same change of volume; 2 compares the final "
        "volumes instead of the work.",
    ncert="Class 11 Physics, 'Thermodynamics', thermodynamic processes (isothermal and isobaric)", seconds=60,
    recomputed=True)

add(T, "Zeroth and first law", "Intermediate", "statement_pair",
    SP_STEM.format(
        s1="The molar specific heat of a gas at constant pressure is greater than that at constant volume because, at "
           "constant pressure, part of the heat supplied is used in doing work as the gas expands.",
        s2="The specific heat capacity of a gas is not unique: it depends on the process by which heat is supplied "
           "to it."),
    sp("A"),
    "Specific heat capacities of a gas",
    "At constant volume all the heat raises the internal energy. At constant pressure the gas also expands and "
    "does work, so more heat is needed for the same rise in temperature: C_p > C_v (C_p − C_v = R for an ideal "
    "gas). Statement I is true. Because the heat needed depends on how much work is done, the specific heat "
    "depends on the process: Statement II is true.",
    ["Statement I: Q_p = ΔU + PΔV > Q_v = ΔU → true", "Statement II: heat for a given ΔT depends on the process → true"],
    why="Both statements are true. Statement II is the general point, Statement I a particular case of it.",
    ncert="Class 11 Physics, 'Thermodynamics', specific heat capacity", seconds=45)

n_, dT_ = 3, 20
dU_ = 1.5 * R_ * n_ * dT_
assert close(dU_, 747) and close(2.5 * R_ * n_ * dT_, 1245) and F(320, 300) == F(16, 15)
truth = [True, True, True, True, False]
multi_key(truth, "abcd")
add(T, "Zeroth and first law", "Intermediate", "multi_statement",
    multi("Three moles of a monatomic ideal gas in a closed rigid vessel are heated from 300 K to 320 K. Taking "
          "R = 8.3 J mol⁻¹ K⁻¹, which of the following statements are correct?",
          ["No work is done by the gas.",
           "The internal energy of the gas increases by 747 J.",
           "The heat supplied to the gas is 747 J.",
           "The final pressure of the gas is 16/15 of its initial pressure.",
           "If the same gas were heated at constant pressure through the same 20 K, it would also need 747 J of "
           "heat."]),
    place("(a), (b), (c) and (d) only", ["(a), (b) and (e) only", "(b), (c) and (d) only",
                                         "(a), (c), (d) and (e) only"], "B"),
    "First law in an isochoric process",
    "A rigid vessel keeps the volume fixed, so W = 0 and Q = ΔU = nC_vΔT. At constant volume P ∝ T. At constant "
    "pressure the gas would also do work, so more heat, nC_pΔT, would be needed.",
    ["(a) ΔV = 0 → W = 0, true", "(b) ΔU = 3 × (3/2)(8.3)(20) = 747 J, true", "(c) Q = ΔU + 0 = 747 J, true",
     "(d) P₂/P₁ = 320/300 = 16/15, true", "(e) Q_p = 3 × (5/2)(8.3)(20) = 1245 J, not 747 J → false"],
    why="(e) forgets the work done during expansion at constant pressure. Options leaving out (a) or (d), or "
        "including (e), are wrong.",
    ncert="Class 11 Physics, 'Thermodynamics', first law of thermodynamics; specific heat capacity", seconds=100,
    recomputed=True)

P_gas = 1.0e5 + 10 * g / 0.01
W_ = P_gas * 0.01 * 0.2
Q_ = 3.5 * W_
assert close(P_gas, 1.1e5) and close(W_, 220) and close(Q_, 770) and close(2.5 * W_, 550)
add(T, "Zeroth and first law", "Advanced", "numerical",
    "A diatomic ideal gas (rigid molecules) is enclosed in a vertical cylinder by a smooth piston of mass 10 kg and "
    "area 0.01 m². The atmospheric pressure is 1.0 × 10⁵ Pa and g = 10 m/s². The gas is heated slowly, and the "
    "piston rises through 0.2 m. The heat supplied to the gas is:",
    place("770 J", ["220 J", "550 J", "700 J"], "C"),
    "First law with a constant-pressure expansion against a loaded piston",
    "The piston moves slowly, so the gas pressure stays equal to atmospheric pressure plus the piston's weight per "
    "unit area: an isobaric process. For a diatomic gas at constant pressure, Q = nC_pΔT = (7/2)nRΔT = (7/2)PΔV.",
    ["P = 1.0 × 10⁵ + (10 × 10)/0.01 = 1.1 × 10⁵ Pa", "ΔV = 0.01 × 0.2 = 2 × 10⁻³ m³ → W = PΔV = 220 J",
     "ΔU = (5/2)PΔV = 550 J", "Q = ΔU + W = (7/2) × 220 = 770 J"],
    why="220 J is only the work done by the gas; 550 J is only the rise in internal energy; 700 J leaves out the "
        "piston's weight in the pressure.",
    ncert="Class 11 Physics, 'Thermodynamics', first law of thermodynamics; isobaric process", seconds=120,
    recomputed=True)

add(T, "Second law, reversible and irreversible processes", "Advanced", "assertion_reason",
    AR_STEM.format(
        a="Real thermodynamic processes can at best approximate a reversible process, which is an idealisation.",
        r="In real processes there are dissipative effects, such as friction and viscosity, and heat flows across "
          "finite temperature differences, so the system and surroundings cannot both be restored exactly."),
    ar("A"),
    "Reversible and irreversible processes",
    "A reversible process must be quasi-static and free of dissipative effects; only then can it be retraced with "
    "both system and surroundings returning to their original states. Every real process involves some friction, "
    "viscosity or finite-rate heat flow, which is why it is irreversible and why the reversible process is only an "
    "idealisation. R gives exactly this reason.",
    ["Reversible ⇔ quasi-static and no dissipation", "Real processes always have dissipation → irreversible",
     "R explains A → option A"],
    why="R is the cause of A, not an unrelated fact, so B is wrong; both statements are true, so C and D are wrong.",
    ncert="Class 11 Physics, 'Thermodynamics', reversible and irreversible processes", seconds=50)

n_, dT_ = 2, 100
W_ = n_ * R_ * dT_
assert close(W_, 1660) and close(3.5 * W_, 5810) and close(2.5 * W_, 4150)
truth = [True, True, True, False, False]
multi_key(truth, "abc")
add(T, "Isothermal and adiabatic processes", "Advanced", "multi_statement",
    multi("Two moles of a diatomic ideal gas (rigid molecules) are taken from 300 K to 400 K along a process that is a "
          "straight line passing through the origin on a volume–temperature (V–T) graph. Taking R = "
          "8.3 J mol⁻¹ K⁻¹, which of the following statements are correct?",
          ["The pressure of the gas stays constant.",
           "The work done by the gas is 1660 J.",
           "The heat absorbed by the gas is 5810 J.",
           "The internal energy of the gas increases by 1660 J.",
           "The density of the gas increases during the process."]),
    place("(a), (b) and (c) only", ["(a), (b) and (d) only", "(b), (c) and (e) only",
                                    "(a), (c), (d) and (e) only"], "D"),
    "Reading a process from a V–T graph",
    "V ∝ T means V/T is constant, which by PV = nRT means P is constant: an isobaric process. Then W = PΔV = nRΔT, "
    "ΔU = nC_vΔT with C_v = (5/2)R, and Q = nC_pΔT with C_p = (7/2)R.",
    ["(a) V/T constant → P constant, true", "(b) W = nRΔT = 2 × 8.3 × 100 = 1660 J, true",
     "(c) Q = (7/2)nRΔT = 5810 J, true", "(d) ΔU = (5/2)nRΔT = 4150 J, not 1660 J → false",
     "(e) volume increases at fixed mass → density decreases → false"],
    why="(d) gives the work done instead of the change in internal energy; (e) has the wrong direction, since the "
        "gas expands as it is heated at constant pressure.",
    ncert="Class 11 Physics, 'Thermodynamics', first law of thermodynamics; isobaric process", seconds=110,
    recomputed=True)


# =====================================================================================================================
# Kinetic Theory of Gases (B2 I3 A2)
# =====================================================================================================================
T = "Kinetic Theory of Gases"

assert 2 ** 2 == 4
add(T, "Pressure and rms speed", "Basic", "numerical",
    "An ideal gas is kept in a closed rigid container. If the speed of every one of its molecules were doubled, the "
    "pressure of the gas would become:",
    place("4 times", ["2 times", "√2 times", "8 times"], "C"),
    "Kinetic-theory expression for pressure",
    "P = (1/3)nm⟨v²⟩. In a rigid closed container n (molecules per unit volume) and m are fixed, so P ∝ ⟨v²⟩. "
    "Doubling every speed makes ⟨v²⟩ four times. (Each collision transfers twice the momentum, and collisions "
    "happen twice as often.)",
    ["P = (1/3)nm⟨v²⟩", "v → 2v ⇒ ⟨v²⟩ → 4⟨v²⟩", "P → 4P"],
    why="2 times counts only the larger momentum per collision (or takes P ∝ v); √2 times confuses the result with "
        "the rms speed when T doubles; 8 times uses P ∝ v³.",
    ncert="Class 11 Physics, 'Kinetic Theory', pressure of an ideal gas", seconds=30, recomputed=True)

add(T, "Pressure and rms speed", "Basic", "direct",
    "According to the kinetic theory of gases, the absolute temperature of an ideal gas is directly proportional "
    "to:",
    place("The average translational kinetic energy of its molecules",
          ["The rms speed of its molecules", "The total linear momentum of its molecules",
           "The number of molecules in the gas"], "A"),
    "Kinetic interpretation of temperature",
    "Kinetic theory gives the average translational kinetic energy of a molecule as (3/2)k_BT, so T is directly "
    "proportional to it. The rms speed is proportional to √T, not to T.",
    ["⟨½mv²⟩ = (3/2)k_BT → T ∝ average KE", "v_rms = √(3k_BT/m) ∝ √T"],
    why="The rms speed varies as √T; the total momentum of a gas at rest in its container is zero on average; "
        "temperature does not depend on how many molecules there are.",
    ncert="Class 11 Physics, 'Kinetic Theory', kinetic interpretation of temperature", seconds=25)

P_f = F(2 * 2 + 3 * 1, 2 + 3)
assert P_f == F(7, 5)
add(T, "Ideal gas equation", "Intermediate", "numerical",
    "A vessel of volume 2 L contains a gas at a pressure of 2 atm and another vessel of volume 3 L contains the same "
    "gas at 1 atm, both at the same temperature. The vessels are connected by a narrow tube of negligible volume and "
    "the temperature is kept the same. Treating the gas as ideal, the final common pressure is:",
    place("1.4 atm", ["1.5 atm", "3 atm", "1.6 atm"], "D"),
    "Ideal gas equation: conservation of the number of moles",
    "At a fixed temperature, the number of moles in each vessel is proportional to PV. The total number of moles "
    "does not change when the vessels are joined, so P_f(V₁ + V₂) = P₁V₁ + P₂V₂.",
    ["P₁V₁ + P₂V₂ = 2 × 2 + 1 × 3 = 7 atm L", "P_f = 7/(2 + 3) = 1.4 atm"],
    why="1.5 atm is the simple average of the pressures; 3 atm adds the pressures; 1.6 atm weights each pressure by "
        "the wrong volume (2 × 3 + 1 × 2)/5.",
    ncert="Class 11 Physics, 'Kinetic Theory', behaviour of gases (ideal gas equation)", seconds=50, recomputed=True)

cv_kg = 1.5 * 8.3 / 0.004
assert close(cv_kg, 3112.5)
add(T, "Degrees of freedom and equipartition", "Intermediate", "numerical",
    "Helium is a monatomic gas of molar mass 4 g/mol. Using the law of equipartition of energy and taking "
    "R = 8.3 J mol⁻¹ K⁻¹, the specific heat capacity of helium at constant volume (per unit mass) is about:",
    place("3.1 × 10³ J kg⁻¹ K⁻¹", ["12.5 J kg⁻¹ K⁻¹", "5.2 × 10³ J kg⁻¹ K⁻¹", "3.1 J kg⁻¹ K⁻¹"], "B"),
    "From molar specific heat to specific heat per unit mass",
    "A monatomic molecule has 3 translational degrees of freedom, so U = (3/2)RT per mole and C_v = (3/2)R per "
    "mole. Dividing by the molar mass in kg/mol gives the value per kilogram.",
    ["Molar C_v = (3/2)R = 12.45 J mol⁻¹ K⁻¹", "c_v = 12.45 / 0.004 kg mol⁻¹ ≈ 3.1 × 10³ J kg⁻¹ K⁻¹"],
    why="12.5 J kg⁻¹ K⁻¹ is the MOLAR value with the wrong unit; 5.2 × 10³ J kg⁻¹ K⁻¹ is c_p, from (5/2)R; "
        "3.1 J kg⁻¹ K⁻¹ divides by 4 instead of 0.004 kg/mol.",
    ncert="Class 11 Physics, 'Kinetic Theory', law of equipartition of energy; specific heat capacity",
    seconds=50, recomputed=True)

add(T, "Degrees of freedom and equipartition", "Intermediate", "match_list",
    match_stem("Match List-I (gas molecule) with List-II (number of quadratic terms in its energy that share the "
               "energy, each contributing ½k_BT on average, according to the law of equipartition of energy).",
               ["Helium (monatomic)", "Nitrogen (N₂) with rigid molecules",
                "Nitrogen (N₂) whose molecules also vibrate in one mode", "A rigid non-linear polyatomic molecule"],
               ["6", "3", "7", "5"]),
    match_options({"A": "II", "B": "IV", "C": "III", "D": "I"},
                  [{"A": "II", "B": "III", "C": "IV", "D": "I"}, {"A": "II", "B": "I", "C": "III", "D": "IV"},
                   {"A": "IV", "B": "II", "C": "III", "D": "I"}], "C"),
    "Equipartition of energy and degrees of freedom",
    "Translational motion gives 3 terms; a rigid diatomic (linear) molecule adds 2 rotational terms; a rigid "
    "non-linear molecule adds 3. A vibrational mode adds 2 terms (kinetic and potential energy), i.e. k_BT.",
    ["He: 3 translational → 3 (II)", "Rigid N₂: 3 + 2 → 5 (IV)", "Vibrating N₂: 5 + 2 → 7 (III)",
     "Rigid non-linear polyatomic: 3 + 3 → 6 (I)"],
    why="The wrong codes count a vibrational mode as one term instead of two, or give a linear molecule three "
        "rotational terms.",
    ncert="Class 11 Physics, 'Kinetic Theory', law of equipartition of energy", seconds=50)

T_ratio = 32 ** (F(7, 5) - 1)
assert close(float(T_ratio), 4.0) and close(math.sqrt(float(T_ratio)), 2.0)
add(T, "Pressure and rms speed", "Advanced", "numerical",
    "An ideal gas of rigid diatomic molecules (γ = 7/5) has an rms molecular speed v. It is compressed reversibly "
    "and adiabatically to 1/32 of its volume. The rms speed of its molecules becomes:",
    place("2v", ["4v", "√2 v", "32v"], "A"),
    "Adiabatic compression and the rms speed",
    "In a reversible adiabatic process TV^(γ−1) is constant, so the temperature rises by 32^(2/5). The rms speed is "
    "proportional to √T.",
    ["T₂/T₁ = (V₁/V₂)^(γ−1) = 32^(2/5) = 4", "v_rms ∝ √T → v₂ = √4 v = 2v"],
    why="4v gives the factor for the temperature, not the speed; √2 v uses the exponent 1/5 instead of 2/5, so T only doubles; "
        "32v treats the speed as proportional to the compression ratio.",
    ncert="Class 11 Physics, 'Kinetic Theory', kinetic interpretation of temperature; 'Thermodynamics', adiabatic "
          "process", seconds=80, recomputed=True)

add(T, "Degrees of freedom and equipartition", "Advanced", "assertion_reason",
    AR_STEM.format(
        a="Equal masses of hydrogen (H₂) and oxygen (O₂), both treated as ideal gases of rigid diatomic molecules, "
          "have equal internal energies at the same temperature.",
        r="At a given temperature, the average energy of a rigid diatomic molecule is (5/2)k_BT, the same for H₂ and "
          "O₂."),
    ar("D"),
    "Internal energy depends on the number of molecules",
    "R is true by the law of equipartition (3 translational + 2 rotational terms). But equal masses contain very "
    "different numbers of molecules: with molar masses 2 g/mol and 32 g/mol, the hydrogen sample has 16 times as "
    "many molecules, so 16 times the internal energy. So A is false.",
    ["R: energy per molecule = (5/2)k_BT for both → true",
     "A: N(H₂)/N(O₂) = 32/2 = 16 → U(H₂) = 16 U(O₂) → false"],
    why="A is false, so options A, B and C are wrong. Equal energy per molecule does not mean equal energy per unit "
        "mass.",
    ncert="Class 11 Physics, 'Kinetic Theory', law of equipartition of energy", seconds=50)


# =====================================================================================================================
# Oscillations and Waves (B5 I5 A4)
# =====================================================================================================================
T = "Oscillations and Waves"

assert close(4 * 5 / 2, 10)
add(T, "SHM equation and phase", "Basic", "numerical",
    "A particle executes simple harmonic motion with an amplitude of 5 cm and a period of 2 s. Its average speed "
    "over one complete oscillation is:",
    place("10 cm/s", ["Zero", "5π cm/s", "5 cm/s"], "B"),
    "Distance covered in one period of SHM",
    "In one complete oscillation the particle goes from the mean position to one extreme, back, to the other "
    "extreme and back: a distance of 4A. Average speed = total distance / time.",
    ["Distance in one period = 4A = 20 cm", "Average speed = 20 cm / 2 s = 10 cm/s"],
    why="Zero is the average VELOCITY over a period (the displacement is zero); 5π cm/s is the maximum speed Aω; "
        "5 cm/s counts only 2A per period.",
    ncert="Class 11 Physics, 'Oscillations', simple harmonic motion", seconds=30, recomputed=True)

assert close(math.pi / 2 - math.pi / 6, math.pi / 3)
add(T, "SHM equation and phase", "Basic", "numerical",
    "Two particles execute simple harmonic motions given by x₁ = A sin(ωt + π/6) and x₂ = A cos ωt along the same "
    "line. The phase difference between the two motions is:",
    place("π/3", ["π/6", "2π/3", "π/2"], "D"),
    "Comparing phases: writing cosine as a sine",
    "To compare phases, write both motions with the same function: A cos ωt = A sin(ωt + π/2). The phase "
    "difference is then the difference of the phase constants.",
    ["x₂ = A sin(ωt + π/2)", "Δφ = π/2 − π/6 = π/3 (x₂ leads x₁)"],
    why="π/6 compares cos ωt with sin ωt as if they were in phase; 2π/3 adds the phase constants; π/2 is the "
        "difference between sine and cosine alone, ignoring the π/6.",
    ncert="Class 11 Physics, 'Oscillations', simple harmonic motion (phase)", seconds=30, recomputed=True)

assert close(2 * 0.20 * 500, 200)
add(T, "Superposition and standing waves", "Basic", "numerical",
    "In a stationary wave set up on a stretched string at a frequency of 500 Hz, adjacent nodes are 20 cm apart. The "
    "speed of the travelling waves on the string is:",
    place("200 m/s", ["100 m/s", "400 m/s", "20 m/s"], "B"),
    "Node spacing in a stationary wave",
    "Adjacent nodes in a stationary wave are half a wavelength apart, so λ = 2 × 20 cm = 0.40 m. The speed of the "
    "travelling waves is v = fλ.",
    ["λ/2 = 0.20 m → λ = 0.40 m", "v = fλ = 500 × 0.40 = 200 m/s"],
    why="100 m/s takes the node spacing as a whole wavelength; 400 m/s takes it as a quarter wavelength (the "
        "node-to-antinode distance); 20 m/s converts 20 cm wrongly to 0.02 m.",
    ncert="Class 11 Physics, 'Waves', reflection of waves (standing waves and normal modes)", seconds=30,
    recomputed=True)

add(T, "SHM equation and phase", "Basic", "direct",
    "Which of the following motions is periodic but NOT oscillatory?",
    place("A particle moving uniformly along a circle",
          ["The bob of a simple pendulum swinging through a small angle",
           "A block oscillating on a horizontal spring", "A prong of a vibrating tuning fork"], "C"),
    "Periodic and oscillatory motion",
    "NCERT: every oscillatory motion is periodic, but not every periodic motion is oscillatory. Uniform circular "
    "motion repeats itself after a fixed time, but the particle does not move to and fro about a mean position.",
    ["Periodic → repeats after a fixed interval", "Oscillatory → to-and-fro about a mean position",
     "Uniform circular motion: periodic, not oscillatory"],
    why="A pendulum bob, a block on a spring and a tuning-fork prong all move to and fro about a mean position, so "
        "their motions are both periodic and oscillatory.",
    ncert="Class 11 Physics, 'Oscillations', periodic and oscillatory motions", seconds=20)

add(T, "Progressive waves and wave speed", "Basic", "statement_pair",
    SP_STEM.format(
        s1="When a transverse wave passes from a light string into a heavier string joined to it, under the same "
           "tension, its frequency stays the same while its speed and wavelength decrease.",
        s2="In a sound wave travelling through air, a compression is a region where the density and the pressure "
           "of the air are higher than normal."),
    sp("A"),
    "Wave speed, frequency and wavelength; compressions",
    "The frequency of a wave is set by the source and does not change at a boundary. The speed on a string is "
    "√(T/μ), so a larger μ means a smaller speed, and λ = v/f is smaller too: Statement I is true. In a longitudinal "
    "wave, compressions are regions of higher density and pressure, rarefactions of lower: Statement II is true.",
    ["Statement I: f fixed, v = √(T/μ) falls as μ rises, λ = v/f falls → true",
     "Statement II: compression = higher density and pressure → true"],
    why="Both statements are true.",
    ncert="Class 11 Physics, 'Waves', speed of a travelling wave; transverse and longitudinal waves", seconds=40)

t_eq = 2.0 / 8
assert close(math.sin(2 * math.pi / 2.0 * t_eq), 1 / math.sqrt(2))
add(T, "Energy in SHM", "Intermediate", "numerical",
    "A particle starts from its mean position at t = 0 and executes simple harmonic motion with a period of 2 s. The "
    "earliest time at which its kinetic energy equals its potential energy is:",
    place("0.25 s", ["0.5 s", "0.125 s", "0.33 s"], "B"),
    "Energy sharing in SHM and the corresponding time",
    "K = U when each is half the total energy: ½kx² = ¼kA², so x = A/√2. With x = A sin(2πt/T), this first happens "
    "at 2πt/T = π/4, i.e. t = T/8.",
    ["K = U → x = A/√2", "sin(2πt/T) = 1/√2 → 2πt/T = π/4", "t = T/8 = 2/8 = 0.25 s"],
    why="0.5 s (T/4) is the time to reach the extreme position; 0.125 s (T/16) halves the phase angle; 0.33 s (T/6) "
        "is the time to reach x = A/2, where K = 3U.",
    ncert="Class 11 Physics, 'Oscillations', energy in simple harmonic motion", seconds=60, recomputed=True)

f_B = 256 - 6
assert abs((f_B + 2) - 256) == 4 and abs((256 + 6 + 2) - 256) == 8
add(T, "Organ pipes and beats", "Intermediate", "numerical",
    "Tuning fork P of frequency 256 Hz and tuning fork Q produce 6 beats per second when sounded together. When the "
    "prongs of Q are filed slightly, the two forks produce 4 beats per second. The frequency of Q before filing "
    "was:",
    place("250 Hz", ["262 Hz", "252 Hz", "260 Hz"], "C"),
    "Beats, and the effect of filing a tuning fork",
    "Beat frequency = |f_P − f_Q|, so f_Q is 250 Hz or 262 Hz. Filing the prongs makes them lighter, which RAISES "
    "the frequency of the fork. If f_Q were 262 Hz, raising it would increase the beat frequency; since the beats "
    "fall to 4 per second, f_Q must have been 250 Hz (raised to 252 Hz).",
    ["f_Q = 256 ± 6 = 250 Hz or 262 Hz", "Filing → f_Q increases",
     "250 → 252 Hz gives 4 beats/s (matches); 262 → higher gives more than 6 beats/s",
     "f_Q = 250 Hz"],
    why="262 Hz assumes filing lowers the frequency (that is the effect of loading with wax); 252 Hz is the "
        "frequency after filing; 260 Hz uses the second beat count with the wrong sign.",
    ncert="Class 11 Physics, 'Waves', beats", seconds=60, recomputed=True)

n_h = 2 * 1.5 * 500 / 300
assert close(n_h, 5) and int(round(n_h)) + 1 == 6
add(T, "Superposition and standing waves", "Intermediate", "numerical",
    "A string 1.5 m long is fixed at both ends. Transverse waves travel on it at 300 m/s. When it vibrates in a "
    "normal mode of frequency 500 Hz, the number of nodes on it, including the two fixed ends, is:",
    place("6", ["5", "4", "10"], "B"),
    "Normal modes of a string fixed at both ends",
    "The normal modes have L = nλ/2, i.e. fₙ = nv/(2L). The nth mode has n loops, and therefore n + 1 nodes "
    "counting the two ends.",
    ["λ = v/f = 300/500 = 0.6 m", "n = 2L/λ = 3/0.6 = 5 (fifth harmonic, 5 loops)", "Nodes = n + 1 = 6"],
    why="5 is the number of loops (antinodes), not nodes; 4 leaves out both ends; 10 counts the number of half "
        "wavelengths in a doubled length.",
    ncert="Class 11 Physics, 'Waves', standing waves and normal modes", seconds=60, recomputed=True)

add(T, "Energy in SHM", "Intermediate", "match_list",
    match_stem("For a particle executing simple harmonic motion about x = 0 between x = −A and x = +A, match "
               "List-I (graph) with List-II (its shape).",
               ["Velocity v against displacement x", "Acceleration a against displacement x",
                "Potential energy U against displacement x", "Total mechanical energy E against displacement x"],
               ["A horizontal straight line", "An ellipse",
                "A straight line through the origin with a negative slope",
                "A parabola opening upward with its minimum at x = 0"]),
    match_options({"A": "II", "B": "III", "C": "IV", "D": "I"},
                  [{"A": "III", "B": "II", "C": "IV", "D": "I"}, {"A": "II", "B": "III", "C": "I", "D": "IV"},
                   {"A": "IV", "B": "III", "C": "II", "D": "I"}], "D"),
    "Graphs of SHM quantities against displacement",
    "v = ±ω√(A² − x²) gives v²/(ωA)² + x²/A² = 1, an ellipse. a = −ω²x is a straight line of negative slope through "
    "the origin. U = ½kx² is a parabola with its minimum at the mean position. E = ½kA² is the same at every x.",
    ["A: v² + ω²x² = ω²A² → ellipse (II)", "B: a = −ω²x → straight line, negative slope (III)",
     "C: U = ½kx² → upward parabola (IV)", "D: E = ½kA² constant → horizontal line (I)"],
    why="The wrong codes swap the velocity graph with the acceleration graph, or the potential energy with the "
        "total energy.",
    ncert="Class 11 Physics, 'Oscillations', velocity and acceleration in SHM; energy in SHM", seconds=60)

add(T, "SHM equation and phase", "Intermediate", "assertion_reason",
    AR_STEM.format(
        a="For a particle executing simple harmonic motion, the speed is greatest at the extreme positions.",
        r="At the extreme positions of simple harmonic motion, the restoring force and the acceleration have their "
          "greatest magnitudes."),
    ar("D"),
    "Speed and acceleration in SHM",
    "v = ω√(A² − x²) is zero at the extremes (x = ±A) and greatest at the mean position, so A is false. "
    "a = −ω²x has its greatest magnitude ω²A at the extremes, so R is true.",
    ["A: at x = ±A, v = 0 → speed least, not greatest → false", "R: |a| = ω²|x| greatest at |x| = A → true"],
    why="A is false, so options A, B and C are wrong. A large acceleration does not mean a large speed: at the "
        "extremes the particle is momentarily at rest.",
    ncert="Class 11 Physics, 'Oscillations', velocity and acceleration in simple harmonic motion", seconds=40)

ratio_A = (3 / 4) / math.sqrt(3 / 4)
assert close(ratio_A, math.sqrt(3) / 2)
add(T, "Spring and pendulum oscillations", "Advanced", "numerical",
    "A block of mass 3 kg attached to a light horizontal spring oscillates on a smooth floor with amplitude A. Just as "
    "the block passes through its mean position, a lump of putty of mass 1 kg is dropped vertically onto it and "
    "sticks. The new amplitude of oscillation is:",
    place("(√3/2)A", ["(3/4)A", "A", "(9/16)A"], "B"),
    "SHM combined with conservation of momentum",
    "The putty has no horizontal velocity, so horizontal momentum is conserved: the speed at the mean position drops "
    "from v₀ = Aω to 3v₀/4. The angular frequency also changes, to ω' = √(k/4) = ω√(3/4). The new amplitude is the "
    "new maximum speed divided by ω'.",
    ["3v₀ = 4v' → v' = (3/4)Aω", "ω' = ω√(3/4)", "A' = v'/ω' = (3/4)A/√(3/4) = (√3/2)A"],
    shortcut="A' = A√(M/(M + m)) when mass is added at the mean position.",
    why="(3/4)A divides by the old ω, forgetting that the mass change also changes ω; A assumes the amplitude is "
        "unaffected; (9/16)A squares the velocity ratio.",
    ncert="Class 11 Physics, 'Oscillations', oscillations due to a spring; 'Laws of Motion', conservation of "
          "momentum", seconds=120, recomputed=True)

ts = [i / 1000 * 2 * math.pi for i in range(1001)]
sep = max(abs(math.sin(t) - math.sin(t + math.pi / 3)) for t in ts)
assert close(sep, 1.0, rel=1e-4)
add(T, "SHM equation and phase", "Advanced", "numerical",
    "Two particles execute simple harmonic motions x₁ = A sin ωt and x₂ = A sin(ωt + π/3) along the same straight "
    "line, about the same mean position. The maximum distance between the two particles during the motion is:",
    place("A", ["2A", "√3 A", "A/2"], "C"),
    "Superposing two SHMs of the same frequency",
    "Their separation is x₂ − x₁ = A[sin(ωt + π/3) − sin ωt] = 2A cos(ωt + π/6) sin(π/6) = A cos(ωt + π/6). It is "
    "itself simple harmonic with amplitude 2A sin(Δφ/2) = A.",
    ["x₂ − x₁ = 2A sin(π/6) cos(ωt + π/6)", "= A cos(ωt + π/6)", "Maximum |x₂ − x₁| = A"],
    shortcut="Maximum separation = 2A sin(Δφ/2).",
    why="2A would need opposite phase (Δφ = π); √3 A uses 2A cos(Δφ/2), the amplitude of the SUM x₁ + x₂; A/2 "
        "uses A sin(Δφ/2) without the factor 2.",
    ncert="Class 11 Physics, 'Oscillations', simple harmonic motion (phase)", seconds=110, recomputed=True)

assert close(2 * math.pi * math.sqrt(1 / math.pi ** 2), 2) and close(2 * math.pi * math.sqrt(4 / math.pi ** 2), 4)
truth = [True, True, False, True, False]
multi_key(truth, "abd")
add(T, "Spring and pendulum oscillations", "Advanced", "multi_statement",
    multi("A simple pendulum of length 1 m, at a place where g = π² m/s², is pulled aside through 4° and released. "
          "Which of the following statements are correct?",
          ["Its period is 2 s.",
           "If it were released from 2° instead, its period would still be very nearly 2 s.",
           "As the bob passes through the mean position, the tension in the string is equal to the weight of the bob.",
           "If the length were made 4 m, the period would become 4 s.",
           "If the mass of the bob were doubled, the period would become √2 times as long."]),
    place("(a), (b) and (d) only", ["(a), (b), (c) and (d) only", "(a), (d) and (e) only",
                                    "(b), (c) and (e) only"], "A"),
    "Simple pendulum: period, and tension at the mean position",
    "For small angles T = 2π√(L/g), independent of amplitude and of the mass of the bob. At the mean position the "
    "bob is moving along a circular arc with speed v, so the string must supply a net upward force mv²/L: "
    "T − mg = mv²/L, and the tension exceeds the weight.",
    ["(a) T = 2π√(1/π²) = 2 s, true", "(b) small angles → T independent of amplitude, true",
     "(c) T = mg + mv²/L > mg, since v ≠ 0 at the mean position → false", "(d) T ∝ √L → 2 × 2 = 4 s, true",
     "(e) T does not depend on mass → false"],
    why="(c) treats the moving bob as if it were hanging at rest, forgetting the centripetal force mv²/L; (e) wrongly brings in the mass, which cancels "
        "in the restoring-force equation.",
    ncert="Class 11 Physics, 'Oscillations', the simple pendulum", seconds=100, recomputed=True)

k_, w_ = 5 * math.pi, 200 * math.pi
assert close(2 * math.pi / k_, 0.4) and close(w_ / (2 * math.pi), 100) and close(w_ / k_, 40)
assert all(close(math.sin(k_ * x), 0, rel=0) or abs(math.sin(k_ * x)) < 1e-9 for x in (0, 0.2, 0.4))
truth = [True, True, False, False, True]
multi_key(truth, "abe")
add(T, "Superposition and standing waves", "Advanced", "multi_statement",
    multi("A stationary wave on a string is described by y = 0.04 sin(5πx) cos(200πt), where x and y are in metres "
          "and t in seconds. Which of the following statements are correct?",
          ["The wavelength of the component travelling waves is 0.4 m.",
           "The frequency of oscillation of the particles is 100 Hz.",
           "The speed of each component travelling wave is 0.025 m/s.",
           "The amplitude of each component travelling wave is 0.04 m.",
           "There are nodes at x = 0, x = 0.2 m and x = 0.4 m."]),
    place("(a), (b) and (e) only", ["(a), (b), (d) and (e) only", "(b), (c) and (e) only",
                                    "(a), (c) and (d) only"], "B"),
    "Reading a stationary-wave equation",
    "y = 2a sin kx cos ωt is the superposition of two waves of amplitude a travelling in opposite directions. Here "
    "k = 5π m⁻¹ and ω = 200π rad/s. Nodes are where sin kx = 0.",
    ["(a) λ = 2π/k = 0.4 m, true", "(b) f = ω/2π = 100 Hz, true",
     "(c) v = ω/k = 40 m/s, not 0.025 m/s (that is k/ω) → false",
     "(d) 2a = 0.04 m → each wave has a = 0.02 m → false", "(e) sin 5πx = 0 at x = 0, 0.2, 0.4 m, true"],
    why="(c) inverts ω/k; (d) takes the amplitude at an antinode, 2a, as the amplitude of each component wave.",
    ncert="Class 11 Physics, 'Waves', reflection of waves (standing waves and normal modes)", seconds=110,
    recomputed=True)

# =====================================================================================================================
# Checks and output
# =====================================================================================================================
def check_plan():
    plan = json.loads(PLAN.read_text(encoding="utf-8"))
    subj = next(s for s in plan["subjects"] if any(p["package"] == PACKAGE for p in s["packages"]))
    pkg = next(p for p in subj["packages"] if p["package"] == PACKAGE)
    planned = Counter({(t["topic"], d): n for t in subj["topics"] if t["topic"] in pkg["topics"]
                       for d, n in t["quota"].items() if n})
    have = Counter((x["topic"], x["difficulty"]) for x in QUESTIONS)
    assert have == planned, (have - planned, planned - have)
    subtopics = {t["topic"]: set(t["subtopics"]) for t in subj["topics"]}
    for x in QUESTIONS:
        assert x["subtopic"] in subtopics[x["topic"]], (x["question_id"], x["subtopic"])
    lo, hi = pkg["question_ids"]
    ids = [x["question_id"] for x in QUESTIONS]
    assert ids[0] == lo and ids[-1] == hi and len(ids) == pkg["count"] == len(set(ids))
    assert Path(pkg["output"]) == OUT.relative_to(ROOT), pkg["output"]


if __name__ == "__main__":
    check_plan()
    keys = Counter(x["correct_answer"] for x in QUESTIONS)
    fmts = Counter(x["format"] for x in QUESTIONS)
    n = len(QUESTIONS)
    assert all(0.20 * n <= v <= 0.30 * n for v in keys.values()) and len(keys) == 4, keys
    assert fmts["numerical"] >= 0.5 * n, fmts
    assert all(fmts[f] >= 0.08 * n for f in ("direct", "assertion_reason", "statement_pair", "match_list",
                                              "multi_statement")), fmts
    doc = {"schema_version": "1.0", "batch_id": "BATCH_009", "created_at": TODAY,
           "notes": "BATCH_009 package PHY_009_p1: 117 original Physics questions (Physics and Measurement through "
                    "Oscillations and Waves). Every numerical answer is re-derived in tools/batch_009/PHY_009_p1.py.",
           "stimuli": [], "questions": QUESTIONS}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {OUT}: {n} questions, {dict(Counter(x['difficulty'] for x in QUESTIONS))}")
    print(f"keys {dict(sorted(keys.items()))}")
    print(f"formats {dict(fmts)}")
