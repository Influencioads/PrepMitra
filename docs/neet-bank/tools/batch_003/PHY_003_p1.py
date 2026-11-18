"""Writes batches/parts/BATCH_003_PHY_p1.json: package PHY_003_p1 of BATCH_003 (132 Physics questions).

Topics: Physics and Measurement, Kinematics, Laws of Motion, Work Energy and Power, Rotational Motion, Gravitation,
Properties of Solids and Liquids, Thermodynamics, Kinetic Theory of Gases, Oscillations and Waves, Electrostatics.
IDs NEET_PHY_000501 .. NEET_PHY_000632, in the order the questions are listed below.

Every computable answer is re-derived with an assert before the file is written, and so is the plan quota. If any
assert fails, nothing is written. Each question's answer position is chosen by hand and fixed.

    python tools/batch_003/PHY_003_p1.py        (run from docs/neet-bank)
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
OUT = ROOT / "batches" / "parts" / "BATCH_003_PHY_p1.json"
PLAN = ROOT / "batches" / "plans" / "BATCH_003_plan.json"
PACKAGE = "PHY_003_p1"
TODAY = "2026-11-16"
LETTERS = "ABCD"
PHY = "Physics"
RECOMPUTED = ("script:recompute", "ai:author-solve", "ai:self-recheck")
AUTHORED = ("ai:author-solve", "ai:self-recheck")
FIRST_ID = 501

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


def dims(m=0, l=0, t=0):
    return (m, l, t)


def dmul(*ds):
    return tuple(sum(x) for x in zip(*ds))


def dinv(d):
    return tuple(-x for x in d)


# =====================================================================================================================
# Physics and Measurement (B2 I2 A2)
# =====================================================================================================================
T = "Physics and Measurement"

D_STRAIN = dmul(dims(l=1), dinv(dims(l=1)))
assert D_STRAIN == (0, 0, 0)
assert dmul(dims(1, 1, -2), dinv(dims(l=2))) != (0, 0, 0)       # stress
assert dims(t=-1) != (0, 0, 0) and dims(1, 1, -1) != (0, 0, 0)    # angular velocity, impulse
add(T, "Dimensional analysis", "Basic", "direct",
    "Which of the following physical quantities is dimensionless?",
    place("Strain", ["Stress", "Angular velocity", "Impulse"], "B"),
    "Dimensionless quantities",
    "Strain is the ratio of a change in a dimension (length or volume) to the original value of that dimension. "
    "A ratio of two like quantities has no dimensions.",
    ["Longitudinal strain = ΔL/L = [L]/[L] → dimensionless",
     "Stress = force/area = [M L⁻¹ T⁻²]", "Angular velocity = angle/time = [T⁻¹]",
     "Impulse = force × time = [M L T⁻¹]"],
    why="Stress has the dimensions of pressure, angular velocity has dimensions [T⁻¹] (the angle itself is "
        "dimensionless, the time is not), and impulse has the dimensions of momentum.",
    ncert="Class 11 Physics, 'Units and Measurement', dimensions of physical quantities", seconds=30)

total = 12.5 + 3.27 + 0.418
assert close(total, 16.188) and round(total, 1) == 16.2
add(T, "Least count and significant figures", "Basic", "numerical",
    "Three lengths measured with different instruments are 12.5 cm, 3.27 cm and 0.418 cm. Their sum, written to "
    "the correct number of significant figures, is:",
    place("16.2 cm", ["16.188 cm", "16.19 cm", "16 cm"], "C"),
    "Significant figures in addition",
    "In addition or subtraction, the result is rounded to the least number of decimal places among the numbers "
    "added. 12.5 cm has only one decimal place, so the sum is rounded to one decimal place.",
    ["Raw sum = 12.5 + 3.27 + 0.418 = 16.188 cm",
     "Least number of decimal places = 1 (in 12.5 cm)", "Rounded sum = 16.2 cm"],
    why="16.188 cm keeps all the digits and claims more precision than the measurements have. 16.19 cm uses two "
        "decimal places, which only 3.27 cm has. 16 cm rounds to whole centimetres and throws away the reliable "
        "first decimal place.",
    ncert="Class 11 Physics, 'Units and Measurement', significant figures (rules for arithmetic operations)",
    seconds=40, recomputed=True)

A_rect = 5.0 * 2.0
rel_A = 0.1 / 5.0 + 0.1 / 2.0
assert close(A_rect, 10.0) and close(rel_A, 0.07) and close(A_rect * rel_A, 0.7)
add(T, "Errors in measurement", "Intermediate", "numerical",
    "The length and breadth of a rectangular sheet are measured as (5.0 ± 0.1) cm and (2.0 ± 0.1) cm. Its area, with "
    "the maximum absolute error, is:",
    place("(10.0 ± 0.7) cm²", ["(10.0 ± 0.2) cm²", "(10.0 ± 0.07) cm²", "(10.0 ± 0.01) cm²"], "D"),
    "Error in a product",
    "For a product Z = AB, the maximum relative error is the sum of the relative errors: ΔZ/Z = ΔA/A + ΔB/B. The "
    "absolute error is the relative error multiplied by the value of Z.",
    ["Area = 5.0 × 2.0 = 10.0 cm²",
     "ΔA/A = 0.1/5.0 + 0.1/2.0 = 0.02 + 0.05 = 0.07",
     "ΔA = 0.07 × 10.0 = 0.7 cm² → (10.0 ± 0.7) cm²"],
    why="± 0.2 cm² adds the absolute errors directly, which is the rule for a sum, not a product. ± 0.07 cm² quotes "
        "the relative error as if it were the absolute error. ± 0.01 cm² multiplies the two absolute errors.",
    ncert="Class 11 Physics, 'Units and Measurement', combination of errors", seconds=60, recomputed=True)

D_P = dims(1, -1, -2)
D_ENERGY_PER_VOL = dmul(dims(1, 2, -2), dinv(dims(l=3)))
D_GPOT = dmul(dims(1, 2, -2), dinv(dims(m=1)))
D_SPEED_SQ = dims(l=2, t=-2)
D_OMEGA = dims(t=-1)
D_FREQ = dims(t=-1)
D_ST = dmul(dims(1, 1, -2), dinv(dims(l=1)))
D_SPRING = dmul(dims(1, 1, -2), dinv(dims(l=1)))
assert D_P == D_ENERGY_PER_VOL and D_GPOT == D_SPEED_SQ and D_OMEGA == D_FREQ and D_ST == D_SPRING
assert len({D_ENERGY_PER_VOL, D_SPEED_SQ, D_FREQ, D_SPRING}) == 4
add(T, "Dimensional analysis", "Intermediate", "match_list",
    match_stem("Match List-I (physical quantity) with List-II (a quantity having the same dimensions).",
               ["Pressure", "Gravitational potential (work done per unit mass)", "Angular velocity",
                "Surface tension"],
               ["Square of speed", "Spring constant (force per unit extension)", "Energy per unit volume",
                "Frequency"]),
    match_options({"A": "III", "B": "I", "C": "IV", "D": "II"},
                  [{"A": "III", "B": "IV", "C": "I", "D": "II"}, {"A": "II", "B": "I", "C": "IV", "D": "III"},
                   {"A": "III", "B": "I", "C": "II", "D": "IV"}], "A"),
    "Quantities with identical dimensions",
    "Reduce each quantity to M, L, T. Pressure and energy per unit volume are both [M L⁻¹ T⁻²]; work per unit mass "
    "is [L² T⁻²], the same as speed squared; angular velocity and frequency are both [T⁻¹]; surface tension (force "
    "per length) and spring constant (force per extension) are both [M T⁻²].",
    ["Pressure = N/m² = J/m³ → [M L⁻¹ T⁻²] → III",
     "Gravitational potential = J/kg = (m/s)² → [L² T⁻²] → I",
     "Angular velocity = rad/s → [T⁻¹] → IV", "Surface tension = N/m → [M T⁻²] → II"],
    why="The other codes pair angular velocity with speed squared or surface tension with energy per volume; "
        "neither pair matches in M, L, T.",
    ncert="Class 11 Physics, 'Units and Measurement', dimensional formulae and dimensional equations", seconds=60)

th1, th2, err = 60.0, 40.0, 0.5
diff, d_err = th1 - th2, 2 * err
assert close(100 * d_err / diff, 5.0) and close(100 * (err / th1 + err / th2), 2.0833, 1e-3)
add(T, "Errors in measurement", "Advanced", "numerical",
    "The initial and final temperatures of a liquid are measured as (60.0 ± 0.5) °C and (40.0 ± 0.5) °C. The maximum "
    "percentage error in the fall in temperature is:",
    place("5%", ["2.5%", "2.1%", "0%"], "B"),
    "Error in a difference",
    "For Z = A − B the maximum absolute error is ΔA + ΔB. Because the difference is much smaller than either "
    "reading, its percentage error is much larger than theirs; this is why subtracting nearly equal quantities is "
    "avoided in precise work.",
    ["Fall in temperature = 60.0 − 40.0 = 20.0 °C",
     "Maximum absolute error = 0.5 + 0.5 = 1.0 °C",
     "Percentage error = (1.0/20.0) × 100 = 5%"],
    why="2.5% takes only one reading's error (0.5/20). 2.1% adds the relative errors of the two readings, which is "
        "the rule for a product. 0% assumes the two errors cancel, but the maximum error is found by adding them.",
    ncert="Class 11 Physics, 'Units and Measurement', combination of errors", seconds=70, recomputed=True)

add(T, "Errors in measurement", "Advanced", "statement_pair",
    SP_STEM.format(
        s1="Repeating a measurement many times with the same instrument and taking the arithmetic mean reduces the "
           "systematic error in the result.",
        s2="If the radius of a sphere is measured with a relative error of 1%, the maximum relative error in its "
           "calculated volume is 3%."),
    sp("D"),
    "Random and systematic errors; error in a power",
    "Averaging many readings reduces random errors, which are equally likely to be positive or negative. A "
    "systematic error (a zero error, a wrongly calibrated scale) shifts every reading the same way, so the mean "
    "carries it unchanged; it must be removed by correcting the instrument or method. For V ∝ r³, ΔV/V = 3Δr/r.",
    ["Statement I: averaging reduces random errors, not systematic errors → false",
     "Statement II: V = (4/3)πr³ → ΔV/V = 3 × 1% = 3% → true"],
    why="Statement I is the trap: repetition cannot remove an error that has the same sign in every reading.",
    ncert="Class 11 Physics, 'Units and Measurement', errors in measurement", seconds=50)

# =====================================================================================================================
# Kinematics (B4 I5 A4)
# =====================================================================================================================
T = "Kinematics"

x_of = lambda t: 3 * t ** 2 - 12 * t + 5
v_of = lambda t: 6 * t - 12
assert v_of(3) == 6 and x_of(3) == -4 and F(x_of(3) - x_of(0), 3) == -3
add(T, "Motion in a straight line", "Basic", "numerical",
    "The position of a particle moving along the x-axis is x = 3t² − 12t + 5, where x is in metres and t in seconds. "
    "Its velocity at t = 3 s is:",
    place("6 m/s", ["−4 m/s", "−3 m/s", "18 m/s"], "C"),
    "Instantaneous velocity as dx/dt",
    "Instantaneous velocity is the time derivative of position. Differentiate x(t) and substitute t = 3 s.",
    ["v = dx/dt = 6t − 12", "At t = 3 s: v = 18 − 12 = 6 m/s"],
    why="−4 m/s is the position x(3) in metres, not a velocity. −3 m/s is the average velocity over the first 3 s, "
        "(x(3) − x(0))/3 = (−4 − 5)/3. 18 m/s keeps only the 6t term and drops −12.",
    ncert="Class 11 Physics, 'Motion in a Straight Line', instantaneous velocity and speed", seconds=40,
    recomputed=True)

R = math.sqrt(3 ** 2 + 5 ** 2 + 2 * 3 * 5 * math.cos(math.radians(60)))
assert close(R, 7.0) and close(math.sqrt(9 + 25 - 15), math.sqrt(19))
add(T, "Vectors", "Basic", "numerical",
    "Two forces of magnitudes 3 N and 5 N act at a point, the angle between them being 60°. The magnitude of their "
    "resultant is:",
    place("7 N", ["8 N", "√34 N", "√19 N"], "B"),
    "Law of vector addition (parallelogram law)",
    "For two vectors of magnitudes A and B inclined at θ, the resultant has magnitude R = √(A² + B² + 2AB cos θ).",
    ["R² = 3² + 5² + 2(3)(5) cos 60° = 9 + 25 + 15 = 49", "R = 7 N"],
    why="8 N is the simple sum, valid only for θ = 0°. √34 N is the result for perpendicular forces (cos 90° = 0). "
        "√19 N uses −2AB cos θ, the formula for the magnitude of the difference of the vectors.",
    ncert="Class 11 Physics, 'Motion in a Plane', addition of vectors: analytical method", seconds=40,
    recomputed=True)

u, th, g = 20.0, math.radians(30), 10.0
T_f = 2 * u * math.sin(th) / g
assert close(T_f, 2.0) and close(2 * u * math.cos(th) / g, 2 * math.sqrt(3))
add(T, "Projectile motion", "Basic", "numerical",
    "A ball is projected from level ground with a speed of 20 m/s at 30° above the horizontal. Taking g = 10 m/s² and "
    "neglecting air resistance, its time of flight is:",
    place("2 s", ["1 s", "4 s", "2√3 s"], "D"),
    "Time of flight of a projectile",
    "The vertical motion alone decides the time of flight: the vertical velocity u sin θ is reversed by gravity, so "
    "T = 2u sin θ / g.",
    ["u sin θ = 20 × ½ = 10 m/s", "T = 2 × 10 / 10 = 2 s"],
    why="1 s is the time to reach the highest point (half the flight). 4 s uses 2u/g, ignoring the angle. 2√3 s uses "
        "cos θ, the horizontal component, in place of sin θ.",
    ncert="Class 11 Physics, 'Motion in a Plane', projectile motion", seconds=35, recomputed=True)

add(T, "Motion in a straight line", "Basic", "match_list",
    match_stem("A particle moves along a straight line with uniform acceleration a. Its velocity is u at t = 0 and v "
               "at time t, and its displacement in this time is s. Match List-I (quantity) with List-II "
               "(expression).",
               ["Velocity at time t", "Displacement in time t", "Square of the velocity after a displacement s",
                "Average velocity over the time interval 0 to t"],
               ["u² + 2as", "(u + v)/2", "u + at", "ut + ½at²"]),
    match_options({"A": "III", "B": "IV", "C": "I", "D": "II"},
                  [{"A": "III", "B": "II", "C": "I", "D": "IV"}, {"A": "IV", "B": "III", "C": "I", "D": "II"},
                   {"A": "III", "B": "IV", "C": "II", "D": "I"}], "B"),
    "Equations of uniformly accelerated motion",
    "For constant acceleration, v = u + at, s = ut + ½at² and v² = u² + 2as. Because velocity changes linearly "
    "with time, the average velocity is the mean of the initial and final velocities, (u + v)/2.",
    ["Velocity at time t: u + at → III", "Displacement: ut + ½at² → IV", "v² = u² + 2as → I",
     "Average velocity = (u + v)/2 → II (true only for uniform acceleration)"],
    why="The other codes swap the displacement formula with the average velocity, or the time-free relation with "
        "the average velocity.",
    ncert="Class 11 Physics, 'Motion in a Straight Line', kinematic equations for uniformly accelerated motion",
    seconds=40)

add(T, "Uniform circular motion", "Intermediate", "direct",
    "A particle moves along a circular track of radius r. When it has gone round exactly half the circle, the ratio "
    "of the distance it has travelled to the magnitude of its displacement is:",
    place("π/2", ["π", "2/π", "1"], "C"),
    "Distance versus displacement",
    "Distance is the length of the path actually covered; displacement is the straight-line separation between the "
    "initial and final positions. After half a circle the particle is at the diametrically opposite point.",
    ["Distance = half the circumference = πr", "Displacement = diameter = 2r", "Ratio = πr/2r = π/2"],
    why="π takes the displacement as r instead of 2r. 2/π is the ratio inverted. 1 would need a straight-line path.",
    ncert="Class 11 Physics, 'Motion in a Straight Line', position, path length and displacement", seconds=35)

Avec, Bvec = (1, 1, 0), (0, 1, 1)
dot = sum(a * b for a, b in zip(Avec, Bvec))
cos_t = dot / (math.sqrt(sum(a * a for a in Avec)) * math.sqrt(sum(b * b for b in Bvec)))
assert dot == 1 and close(math.degrees(math.acos(cos_t)), 60.0)
add(T, "Vectors", "Intermediate", "numerical",
    "The angle between the vectors A = î + ĵ and B = ĵ + k̂ is:",
    place("60°", ["45°", "90°", "30°"], "A"),
    "Angle between two vectors from the scalar product",
    "A · B = AB cos θ, so cos θ = (A · B)/(AB). Compute the scalar product component by component and divide by "
    "the product of the magnitudes.",
    ["A · B = (1)(0) + (1)(1) + (0)(1) = 1", "|A| = √2, |B| = √2 → AB = 2",
     "cos θ = 1/2 → θ = 60°"],
    why="45° comes from taking cos θ = 1/√2 (dividing by only one magnitude). 90° assumes vectors along different "
        "axes are perpendicular, but they share the ĵ component. 30° confuses cos θ = ½ with sin θ = ½.",
    ncert="Class 11 Physics, 'Work, Energy and Power', the scalar product", seconds=50, recomputed=True)

t_total, g = 6.0, 10.0
u_up = g * t_total / 2
H = u_up ** 2 / (2 * g)
assert close(u_up, 30.0) and close(H, 45.0) and close(0.5 * g * t_total ** 2, 180.0)
add(T, "Motion in a straight line", "Intermediate", "numerical",
    "A ball thrown vertically upward returns to the thrower's hand 6 s later. Taking g = 10 m/s² and neglecting air "
    "resistance, the maximum height it reaches above the hand is:",
    place("45 m", ["180 m", "90 m", "30 m"], "B"),
    "Symmetry of vertical motion under gravity",
    "Without air resistance the time of ascent equals the time of descent, each 3 s here. The ball falls freely from "
    "the top for 3 s, so H = ½g(3)².",
    ["Time of ascent = 6/2 = 3 s → u = g t = 30 m/s", "H = u²/2g = 900/20 = 45 m (or ½ × 10 × 3² = 45 m)"],
    why="180 m treats the whole 6 s as the fall time. 90 m uses u²/g, dropping the factor 2. 30 m confuses the "
        "launch speed (30 m/s) with the height.",
    ncert="Class 11 Physics, 'Motion in a Straight Line', kinematic equations for uniformly accelerated motion",
    seconds=45, recomputed=True)

a1, t1, t2, t3 = 2.0, 10.0, 10.0, 5.0
vmax = a1 * t1
dist = 0.5 * vmax * t1 + vmax * t2 + 0.5 * vmax * t3
assert close(dist, 350.0) and close(dist / (t1 + t2 + t3), 14.0) and close(dist / (t1 + t2), 17.5)
add(T, "Graphs of motion", "Intermediate", "numerical",
    "A car starts from rest and moves along a straight road. It accelerates uniformly at 2 m/s² for 10 s, then moves "
    "at constant velocity for 10 s, and then decelerates uniformly to rest in 5 s. Its average speed for the whole "
    "journey is:",
    place("14 m/s", ["10 m/s", "17.5 m/s", "20 m/s"], "D"),
    "Area under the velocity–time graph",
    "The velocity–time graph is a trapezium. The distance is the area under it, and the average speed is the total "
    "distance divided by the total time.",
    ["Maximum speed = 2 × 10 = 20 m/s",
     "Distances: ½ × 20 × 10 = 100 m; 20 × 10 = 200 m; ½ × 20 × 5 = 50 m → total 350 m",
     "Average speed = 350 m / 25 s = 14 m/s"],
    why="10 m/s averages the initial and maximum speeds, which is valid only for a single uniformly accelerated "
        "stage. 17.5 m/s divides by 20 s, leaving out the braking time. 20 m/s is the maximum speed.",
    ncert="Class 11 Physics, 'Motion in a Straight Line', acceleration (area under the v–t graph)", seconds=70,
    recomputed=True)

add(T, "Projectile motion", "Intermediate", "assertion_reason",
    AR_STEM.format(
        a="From the same height above level ground, one ball is dropped from rest and another is thrown horizontally "
          "at the same instant. Neglecting air resistance, both reach the ground at the same time.",
        r="The horizontal and vertical motions of a projectile are independent of each other, and the horizontal "
          "throw gives the second ball no initial vertical velocity."),
    ar("A"),
    "Independence of perpendicular motions",
    "Both balls start with zero vertical velocity and have the same vertical acceleration g. Their horizontal "
    "velocities differ, but horizontal motion does not affect vertical motion, so they fall the same height in the "
    "same time.",
    ["Vertical motion of each: y = ½gt² with zero initial vertical velocity → same time of fall",
     "R states the independence of the two motions and the zero vertical velocity, which is exactly why A holds"],
    why="R is not just true but is the reason: if the horizontal motion affected the vertical motion, the fall times "
        "would differ.",
    ncert="Class 11 Physics, 'Motion in a Plane', projectile motion", seconds=45)

a_up, a_dn, t_tot = 2.0, 4.0, 9.0
v_peak = t_tot / (1 / a_up + 1 / a_dn)
assert close(v_peak, 12.0) and close(v_peak / 2, 6.0)
add(T, "Motion in a straight line", "Advanced", "numerical",
    "A particle starts from rest and moves along a straight line with a uniform acceleration of 2 m/s². After some "
    "time it begins to decelerate uniformly at 4 m/s² and comes to rest. The whole motion lasts 9 s. The maximum "
    "velocity reached by the particle is:",
    place("12 m/s", ["6 m/s", "18 m/s", "36 m/s"], "C"),
    "Accelerate–decelerate motion",
    "If the peak velocity is v, the accelerating phase lasts v/a₁ and the decelerating phase lasts v/a₂. Their sum "
    "is the total time.",
    ["v/2 + v/4 = 9", "3v/4 = 9 → v = 12 m/s",
     "Check: 6 s accelerating (2 × 6 = 12) and 3 s decelerating (12/4 = 3); 6 + 3 = 9 s ✓"],
    why="6 m/s is the average velocity (half the peak) over the motion. 18 m/s takes 2 m/s² acting for the full 9 s. "
        "36 m/s takes 4 m/s² for the full 9 s.",
    shortcut="t = v(1/a₁ + 1/a₂) → v = t·a₁a₂/(a₁ + a₂) = 9 × 8/6 = 12 m/s.",
    ncert="Class 11 Physics, 'Motion in a Straight Line', kinematic equations for uniformly accelerated motion",
    seconds=80, recomputed=True)

u, g, t = 20 * math.sqrt(2), 10.0, 3.0
vx = u * math.cos(math.radians(45))
vy = u * math.sin(math.radians(45)) - g * t
assert close(vx, 20.0) and close(vy, -10.0) and close(math.hypot(vx, vy), 10 * math.sqrt(5))
assert 2 * u * math.sin(math.radians(45)) / g > t            # still in flight (time of flight 4 s)
assert close(math.hypot(vx, 20 + 30), 10 * math.sqrt(29))
add(T, "Projectile motion", "Advanced", "numerical",
    "A projectile is launched from level ground with a speed of 20√2 m/s at 45° above the horizontal. Taking "
    "g = 10 m/s² and neglecting air resistance, its speed 3 s after launch is:",
    place("10√5 m/s", ["10 m/s", "20 m/s", "10√29 m/s"], "B"),
    "Velocity of a projectile at an instant",
    "The horizontal component stays u cos θ; the vertical component becomes u sin θ − gt. The speed is the magnitude "
    "of their vector sum. The time of flight is 2u sin θ/g = 4 s, so at 3 s the projectile is still in the air, on "
    "its way down.",
    ["uₓ = 20√2 cos 45° = 20 m/s; u_y = 20√2 sin 45° = 20 m/s",
     "At t = 3 s: v_y = 20 − 10 × 3 = −10 m/s (downward), vₓ = 20 m/s",
     "Speed = √(20² + 10²) = √500 = 10√5 m/s ≈ 22.4 m/s"],
    why="10 m/s is only the vertical component. 20 m/s is only the horizontal component (the speed at the top). "
        "10√29 m/s adds gt to the upward velocity, a sign error.",
    shortcut="At t = 3 s the projectile is as far past the top (t = 2 s) as it was before the top at t = 1 s, so the "
             "speeds at 1 s and 3 s are equal.",
    ncert="Class 11 Physics, 'Motion in a Plane', projectile motion", seconds=75, recomputed=True)

ms_truth = [True, True, True, False, False]
multi_key(ms_truth, "abc")
add(T, "Uniform circular motion", "Advanced", "multi_statement",
    multi("Which of the following statements are correct? Neglect air resistance.",
          ["For a particle in uniform circular motion, the velocity and the acceleration are perpendicular to each "
           "other at every instant.",
           "For a particle in uniform circular motion, the angular speed remains constant.",
           "For a projectile, the velocity and the acceleration are perpendicular to each other at the highest point "
           "of its path.",
           "For a particle in uniform circular motion on a circle of fixed radius, doubling the speed doubles the "
           "centripetal acceleration.",
           "The path of a projectile is a parabola only when it is launched at 45° to the horizontal."]),
    place("(a), (b) and (c) only", ["(a), (c) and (d) only", "(b), (d) and (e) only", "(a), (b), (c) and (d) only"],
          "C"),
    "Uniform circular motion and projectile motion",
    "In uniform circular motion the acceleration v²/r points to the centre while the velocity is tangential, and "
    "the angular speed v/r is constant. At the top of a projectile's path the velocity is horizontal and g is "
    "vertical. The centripetal acceleration v²/r varies as the square of the speed, and every projectile (any angle "
    "other than 90°) follows a parabola.",
    ["(a) Centripetal acceleration ⟂ tangential velocity → true",
     "(b) ω = v/r with v and r constant → true",
     "(c) At the top the velocity is horizontal, g is vertical → true",
     "(d) a = v²/r → doubling v makes a four times → false",
     "(e) y = x tan θ − gx²/(2u²cos²θ) is a parabola for every θ → false"],
    why="Codes containing (d) forget that a ∝ v²; codes containing (e) confuse the angle of maximum range with the "
        "condition for a parabolic path.",
    ncert="Class 11 Physics, 'Motion in a Plane', projectile motion and uniform circular motion", seconds=90)

add(T, "Motion in a straight line", "Advanced", "statement_pair",
    SP_STEM.format(
        s1="For a particle moving along a straight line with constant acceleration, its average speed over any time "
           "interval equals the magnitude of its average velocity over that interval.",
        s2="For a particle moving along a straight line with constant acceleration, its average velocity over any "
           "time interval equals the mean of its velocities at the start and at the end of that interval."),
    sp("D"),
    "Average speed and average velocity in uniformly accelerated motion",
    "With constant acceleration, velocity changes linearly with time, so the average velocity is (v₁ + v₂)/2. But "
    "if the velocity reverses during the interval (for example a ball thrown up and caught again), the path length "
    "exceeds the magnitude of the displacement, so the average speed exceeds |average velocity|.",
    ["Statement I: counter-example — a ball thrown up at 10 m/s and caught 2 s later (g = 10 m/s²): average "
     "velocity 0, average speed 10 m/s → false",
     "Statement II: v is linear in t → average velocity = (v₁ + v₂)/2 → true"],
    why="Statement I holds only if the particle does not reverse its direction during the interval; constant "
        "acceleration does not guarantee that.",
    ncert="Class 11 Physics, 'Motion in a Straight Line', average velocity and average speed", seconds=70)


# =====================================================================================================================
# Laws of Motion (B4 I5 A4)
# =====================================================================================================================
T = "Laws of Motion"

p1, p2, dt = 10.0, 30.0, 4.0
assert close((p2 - p1) / dt, 5.0) and close(p2 / dt, 7.5) and close((p2 - p1) * dt, 80.0)
add(T, "Newton's laws and impulse", "Basic", "numerical",
    "The linear momentum of a body moving in a straight line increases steadily from 10 kg m/s to 30 kg m/s in 4 s. "
    "The force acting on it is:",
    place("5 N", ["7.5 N", "80 N", "2.5 N"], "B"),
    "Newton's second law in terms of momentum",
    "Force equals the rate of change of momentum, F = Δp/Δt. A steady change means the force is constant.",
    ["Δp = 30 − 10 = 20 kg m/s", "F = 20/4 = 5 N"],
    why="7.5 N divides the final momentum, not the change, by the time. 80 N multiplies the change by the time "
        "instead of dividing. 2.5 N divides the initial momentum by the time.",
    ncert="Class 11 Physics, 'Laws of Motion', Newton's second law of motion", seconds=30, recomputed=True)

Fnet = math.hypot(6, 8)
assert close(Fnet, 10.0) and close(Fnet / 2, 5.0) and close((6 + 8) / 2, 7.0)
add(T, "Newton's laws and impulse", "Basic", "numerical",
    "A body of mass 2 kg lies on a smooth horizontal surface. Two horizontal forces act on it: 6 N towards the east "
    "and 8 N towards the north. The magnitude of its acceleration is:",
    place("5 m/s²", ["7 m/s²", "1 m/s²", "10 m/s²"], "A"),
    "Second law with the vector sum of forces",
    "Acceleration is produced by the net (vector) force. Perpendicular forces combine by Pythagoras' theorem.",
    ["Net force = √(6² + 8²) = 10 N", "a = F/m = 10/2 = 5 m/s²"],
    why="7 m/s² adds the forces as numbers (14 N). 1 m/s² subtracts them (2 N). 10 m/s² is the net force in newtons "
        "not divided by the mass.",
    ncert="Class 11 Physics, 'Laws of Motion', Newton's second law of motion", seconds=35, recomputed=True)

add(T, "Equilibrium of concurrent forces", "Basic", "assertion_reason",
    AR_STEM.format(
        a="A body can remain at rest even when several forces act on it.",
        r="A body at rest has no force acting on it."),
    ar("C"),
    "Equilibrium means zero net force",
    "A body stays at rest (or in uniform motion) when the vector sum of all the forces on it is zero; the forces "
    "themselves need not be zero. A book on a table has its weight and the normal reaction acting on it, and they "
    "balance.",
    ["A: true — e.g. weight and normal reaction on a book at rest",
     "R: false — a body at rest needs zero net force, not zero forces"],
    why="R confuses 'no net force' with 'no force'; A is a direct consequence of the correct idea.",
    ncert="Class 11 Physics, 'Laws of Motion', equilibrium of a particle", seconds=30)

add(T, "Newton's laws and impulse", "Basic", "match_list",
    match_stem("Match List-I (law or theorem) with List-II (its content).",
               ["Newton's first law", "Newton's second law", "Newton's third law", "Impulse–momentum theorem"],
               ["Forces always occur in pairs; the force of A on B is equal and opposite to the force of B on A",
                "The rate of change of momentum of a body is proportional to the applied force and is in its "
                "direction",
                "A body continues in its state of rest or of uniform motion in a straight line unless an external "
                "force acts on it",
                "The product of a force and the time for which it acts equals the change in momentum it produces"]),
    match_options({"A": "III", "B": "II", "C": "I", "D": "IV"},
                  [{"A": "II", "B": "III", "C": "I", "D": "IV"}, {"A": "III", "B": "IV", "C": "I", "D": "II"},
                   {"A": "I", "B": "II", "C": "III", "D": "IV"}], "D"),
    "Statements of Newton's laws",
    "The first law describes inertia, the second law relates force to the rate of change of momentum, the third law "
    "describes action–reaction pairs, and the impulse–momentum theorem follows from the second law: FΔt = Δp.",
    ["First law → III", "Second law → II", "Third law → I", "Impulse–momentum theorem → IV"],
    why="The other codes swap the first and second laws, or treat the second law and the impulse theorem as the "
        "same statement.",
    ncert="Class 11 Physics, 'Laws of Motion', Newton's first, second and third laws; impulse", seconds=40)

add(T, "Newton's laws and impulse", "Intermediate", "direct",
    "A horse pulls a cart along a level road, and the horse and cart speed up together. The horizontal force that "
    "makes the horse accelerate forward is the force exerted by:",
    place("The ground on the horse", ["The cart on the horse", "The horse on the cart", "The horse on the ground"],
          "C"),
    "Newton's third law and the forces on a single body",
    "Consider the forces acting on the horse alone. The cart pulls the horse backward. The horse pushes the ground "
    "backward with its hooves, and by the third law the ground pushes the horse forward through friction. The horse "
    "accelerates forward because this forward push of the ground is larger than the backward pull of the cart.",
    ["Forces on the horse (horizontal): ground → forward; cart → backward",
     "Net forward force on the horse comes from the ground"],
    why="The cart's force on the horse points backward. The horse's force on the cart acts on the cart, not on the "
        "horse. The horse's force on the ground acts on the ground. A force on another body cannot accelerate the "
        "horse.",
    ncert="Class 11 Physics, 'Laws of Motion', Newton's third law of motion", seconds=45)

add(T, "Circular motion: level and banked roads", "Intermediate", "assertion_reason",
    AR_STEM.format(
        a="A vehicle can go round a banked curve at a certain speed even if the road is perfectly frictionless.",
        r="On a banked road, the horizontal component of the normal reaction points towards the centre of the curve "
          "and can supply the centripetal force."),
    ar("A"),
    "Banking of roads",
    "On a road banked at θ the normal reaction is tilted towards the centre of the curve. Its vertical component "
    "balances the weight and its horizontal component N sin θ provides mv²/r. At the speed v₀ = √(rg tan θ) no "
    "friction is needed at all.",
    ["N cos θ = mg and N sin θ = mv₀²/r → v₀² = rg tan θ",
     "R gives the source of the centripetal force when friction is absent, which is exactly why A is possible"],
    why="Both are true, and R is the physical reason for A, so the first option is the answer.",
    ncert="Class 11 Physics, 'Laws of Motion', circular motion (motion of a car on a banked road)", seconds=45)

F_, a1_, a2_ = 1.0, 6.0, 3.0
a_comb = F_ / (F_ / a1_ + F_ / a2_)
assert close(a_comb, 2.0)
add(T, "Newton's laws and impulse", "Intermediate", "numerical",
    "A certain force gives a body of mass m₁ an acceleration of 6 m/s² and a body of mass m₂ an acceleration of "
    "3 m/s². If the two bodies are tied together, the same force gives the combination an acceleration of:",
    place("2 m/s²", ["4.5 m/s²", "9 m/s²", "3 m/s²"], "B"),
    "Second law for a combined mass",
    "Write each mass in terms of the force: m₁ = F/6 and m₂ = F/3. The combination has mass m₁ + m₂ = F/2, so the "
    "same force gives it an acceleration F/(F/2).",
    ["m₁ + m₂ = F/6 + F/3 = F/2", "a = F/(m₁ + m₂) = 2 m/s²"],
    why="4.5 m/s² averages the accelerations. 9 m/s² adds them. 3 m/s² takes the smaller acceleration, as if the "
        "lighter body added nothing.",
    shortcut="1/a = 1/a₁ + 1/a₂ = 1/6 + 1/3 = 1/2.",
    ncert="Class 11 Physics, 'Laws of Motion', Newton's second law of motion", seconds=45, recomputed=True)

m_b, v_b, s_b = 0.05, 200.0, 0.10
F_res = m_b * v_b ** 2 / (2 * s_b)
assert close(F_res, 1.0e4) and close(m_b * v_b ** 2 / s_b, 2.0e4) and close(m_b * v_b ** 2 / 2, 1.0e3)
assert close(m_b * v_b / s_b, 100.0)
add(T, "Newton's laws and impulse", "Intermediate", "numerical",
    "A bullet of mass 50 g moving at 200 m/s enters a fixed wooden block and comes to rest after penetrating 10 cm. "
    "Assuming the resistive force of the wood is constant, its magnitude is:",
    place("1.0 × 10⁴ N", ["2.0 × 10⁴ N", "1.0 × 10³ N", "1.0 × 10² N"], "A"),
    "Constant retarding force from v² = u² − 2as",
    "Find the uniform retardation from the stopping distance, then multiply by the mass.",
    ["0 = 200² − 2a(0.10) → a = 40000/0.20 = 2 × 10⁵ m/s²",
     "F = ma = 0.05 × 2 × 10⁵ = 1.0 × 10⁴ N"],
    why="2.0 × 10⁴ N drops the factor 2 in v² = 2as. 1.0 × 10³ N takes the distance as 1 m (cm-to-m slip). "
        "1.0 × 10² N divides the momentum by the distance, which is not a force.",
    ncert="Class 11 Physics, 'Laws of Motion', Newton's second law of motion", seconds=55, recomputed=True)

add(T, "Friction", "Intermediate", "statement_pair",
    SP_STEM.format(
        s1="The static friction acting on a body can be in the direction of the body's motion.",
        s2="For a given pair of surfaces, the limiting value of static friction does not depend on the normal "
           "reaction between them."),
    sp("C"),
    "Direction and magnitude of static friction",
    "Static friction opposes impending relative motion between the surfaces, not the motion of the body. A box "
    "resting on the floor of a truck that is speeding up is carried forward by static friction, which then acts in "
    "the direction of motion. The limiting static friction is μₛN, directly proportional to the normal reaction.",
    ["Statement I: box on an accelerating truck — friction forward, along the motion → true",
     "Statement II: f_max = μₛN depends on N → false"],
    why="Statement II states the area-independence law wrongly; friction is independent of the area of contact, "
        "not of the normal reaction.",
    ncert="Class 11 Physics, 'Laws of Motion', friction", seconds=50)

M_r, L_r, F_pull, x_cut = 2.0, 4.0, 10.0, 1.0
a_r = F_pull / M_r
T_cut = (M_r * (L_r - x_cut) / L_r) * a_r
assert close(a_r, 5.0) and close(T_cut, 7.5) and close(F_pull * x_cut / L_r, 2.5)
add(T, "Newton's laws and impulse", "Advanced", "numerical",
    "A uniform rope of mass 2 kg and length 4 m lies straight on a smooth horizontal floor. One end is pulled "
    "horizontally along the rope with a force of 10 N. The tension in the rope at a point 1 m from the pulled end "
    "is:",
    place("7.5 N", ["10 N", "2.5 N", "5 N"], "D"),
    "Tension in a rope that has mass",
    "A massive rope accelerates with the force applied, so its tension falls along its length. The tension at a "
    "point is the force needed to accelerate the part of the rope behind that point.",
    ["Acceleration of the whole rope: a = 10/2 = 5 m/s²",
     "Part behind the point: length 3 m → mass 2 × 3/4 = 1.5 kg",
     "T = 1.5 × 5 = 7.5 N"],
    why="10 N treats the rope as massless (uniform tension). 2.5 N is the force needed by the 1 m piece in front, "
        "not the 3 m behind. 5 N is the tension at the midpoint.",
    shortcut="T(x) = F(1 − x/L) with x measured from the pulled end: 10 × 3/4 = 7.5 N.",
    ncert="Class 11 Physics, 'Laws of Motion', Newton's second law of motion", seconds=75, recomputed=True)

T1 = 100 / 2
T2 = math.sqrt(3) * T1
assert close(T1 * math.cos(math.radians(30)), T2 * math.cos(math.radians(60)))
assert close(T1 * math.sin(math.radians(30)) + T2 * math.sin(math.radians(60)), 100.0)
assert close(T2, 50 * math.sqrt(3))
add(T, "Equilibrium of concurrent forces", "Advanced", "numerical",
    "A block of mass 10 kg hangs at rest from two light strings tied to a horizontal ceiling. One string makes an "
    "angle of 30° with the ceiling and the other makes an angle of 60° with the ceiling. Taking g = 10 m/s², the "
    "tension in the string that makes 60° with the ceiling is:",
    place("50√3 N", ["50 N", "100 N", "100/√3 N"], "B"),
    "Equilibrium of three concurrent forces",
    "The weight and the two tensions meet at the knot. For equilibrium, the horizontal components of the tensions "
    "cancel and their vertical components add up to the weight.",
    ["Horizontal: T₁ cos 30° = T₂ cos 60° → T₂ = √3 T₁",
     "Vertical: T₁ sin 30° + T₂ sin 60° = 100 → T₁/2 + 3T₁/2 = 100 → T₁ = 50 N",
     "T₂ = 50√3 N ≈ 86.6 N"],
    why="50 N is the tension in the other (30°) string. 100 N assumes one string carries the whole weight. 100/√3 N "
        "comes from resolving with sine and cosine interchanged.",
    shortcut="The two strings are perpendicular (30° + 60° = 90°), so T₂ = mg sin 60° = 50√3 N and T₁ = mg cos 60°.",
    ncert="Class 11 Physics, 'Laws of Motion', equilibrium of a particle", seconds=85, recomputed=True)

n_per_s = 600 / 60
F_gun = n_per_s * 0.020 * 500
assert close(F_gun, 100.0) and close(600 * 0.020 * 500, 6000.0) and close(0.020 * 500, 10.0)
add(T, "Newton's laws and impulse", "Advanced", "numerical",
    "A machine gun fires 600 bullets per minute, each of mass 20 g, with a speed of 500 m/s relative to the ground. "
    "The average force needed to hold the gun in place is:",
    place("100 N", ["6000 N", "10 N", "50 N"], "C"),
    "Force as the rate of change of momentum",
    "Each second the gun gives a definite amount of forward momentum to the bullets; by the third law it receives an "
    "equal backward momentum each second, which must be cancelled by the holding force.",
    ["Bullets per second = 600/60 = 10",
     "Momentum given per second = 10 × 0.020 × 500 = 100 kg m/s per s", "F = 100 N"],
    why="6000 N uses 600 bullets per second (minutes not converted). 10 N is the momentum of a single bullet. "
        "50 N halves the answer with no physical reason.",
    ncert="Class 11 Physics, 'Laws of Motion', Newton's second law of motion", seconds=50, recomputed=True)

multi_key([True, True, True, False, False], "abc")
add(T, "Circular motion: level and banked roads", "Advanced", "multi_statement",
    multi("Which of the following statements about vehicles taking circular turns on roads are correct?",
          ["On a level road, the maximum speed at which a car can take a turn of radius r without skidding is "
           "√(μₛrg), whatever the mass of the car.",
           "On a road banked at a given angle, friction allows a maximum safe speed greater than the speed at which "
           "no friction is needed.",
           "A car cannot take a circular turn on a perfectly frictionless level road.",
           "When a car takes a turn at constant speed on a level road, the friction on its tyres acts opposite to its "
           "velocity.",
           "The speed at which a car can take a banked turn without needing friction depends on the mass of the "
           "car."]),
    place("(a), (b) and (c) only", ["(a), (c) and (e) only", "(b), (c) and (d) only", "(a), (b), (c) and (e) only"],
          "D"),
    "Friction and banking in circular motion",
    "On a level road static friction alone supplies mv²/r, so mv²/r ≤ μₛmg and v_max = √(μₛrg): the mass cancels. "
    "On a banked road friction can act down the slope and add to the centripetal component, raising the maximum "
    "speed above v₀ = √(rg tan θ), which is also mass-independent. With no friction on a level road nothing "
    "horizontal acts towards the centre. At constant speed the friction is radial (towards the centre), not along "
    "the velocity.",
    ["(a) μₛmg ≥ mv²/r → v_max = √(μₛrg), independent of m → true",
     "(b) v_max = √[rg(μₛ + tan θ)/(1 − μₛ tan θ)] > √(rg tan θ) → true",
     "(c) No horizontal force towards the centre → true",
     "(d) Friction is centripetal (perpendicular to v) at constant speed → false",
     "(e) v₀ = √(rg tan θ), independent of m → false"],
    why="Codes containing (d) think of friction as always opposing motion; codes containing (e) forget that the mass "
        "cancels on both sides of the equations.",
    ncert="Class 11 Physics, 'Laws of Motion', circular motion (level and banked roads)", seconds=100)

# =====================================================================================================================
# Work, Energy and Power (B3 I4 A3)
# =====================================================================================================================
T = "Work, Energy and Power"

m1_, m2_ = 1.0, 4.0
# Equal kinetic energies: p = √(2mK)
assert close(math.sqrt(m1_ / m2_), 0.5)
add(T, "Work-energy theorem", "Basic", "numerical",
    "Two bodies of masses 1 kg and 4 kg have equal kinetic energies. The ratio of the magnitude of the linear "
    "momentum of the 1 kg body to that of the 4 kg body is:",
    place("1 : 2", ["1 : 4", "2 : 1", "1 : 16"], "B"),
    "Relation between kinetic energy and momentum",
    "K = p²/2m, so p = √(2mK). For equal K, p ∝ √m.",
    ["p₁/p₂ = √(m₁/m₂) = √(1/4) = 1/2"],
    why="1 : 4 takes p ∝ m. 2 : 1 inverts the correct ratio (that is the ratio of speeds). 1 : 16 squares the mass "
        "ratio.",
    ncert="Class 11 Physics, 'Work, Energy and Power', kinetic energy", seconds=35, recomputed=True)

add(T, "Work by constant and variable force", "Basic", "direct",
    "Which of the following is a conservative force?",
    place("Gravitational force", ["Kinetic friction", "Air resistance (drag)", "Viscous force"], "B"),
    "Conservative and non-conservative forces",
    "A force is conservative if the work it does between two points does not depend on the path, so that it can be "
    "derived from a potential energy. Gravity (and the spring force) are conservative; friction, drag and viscous "
    "forces dissipate mechanical energy and are non-conservative.",
    ["Work done by gravity = −mg(h₂ − h₁), path-independent → conservative",
     "Friction, drag and viscosity always remove mechanical energy → non-conservative"],
    why="Kinetic friction, air resistance and viscous force all do negative work that depends on the length of the "
        "path, so none of them has a potential energy.",
    ncert="Class 11 Physics, 'Work, Energy and Power', conservative forces and conservation of mechanical energy",
    seconds=25)

add(T, "Work by constant and variable force", "Basic", "statement_pair",
    SP_STEM.format(
        s1="A potential energy can be defined only for a conservative force.",
        s2="The work done by the gravitational force on a body moving from one point to another near the Earth's "
           "surface does not depend on the path followed."),
    sp("A"),
    "Potential energy and path independence",
    "Potential energy is defined through the work done by a force, and this definition is meaningful only when "
    "the work is the same for every path between two points — that is, for a conservative force. Gravity is such a "
    "force: its work depends only on the change in height.",
    ["Statement I: V(x) needs path-independent work → true",
     "Statement II: W_g = −mgΔh for any path → true"],
    why="Both statements are true; neither contains the usual traps (friction having potential energy, or gravity's "
        "work depending on the path).",
    ncert="Class 11 Physics, 'Work, Energy and Power', the concept of potential energy", seconds=35)

m_f, h_f, v_f, g = 1.0, 20.0, 18.0, 10.0
W_air = 0.5 * m_f * v_f ** 2 - m_f * g * h_f
assert close(W_air, -38.0)
add(T, "Work-energy theorem", "Intermediate", "numerical",
    "A ball of mass 1 kg is dropped from rest from a height of 20 m and reaches the ground with a speed of 18 m/s. "
    "Taking g = 10 m/s², the work done on the ball by air resistance during the fall is:",
    place("−38 J", ["38 J", "−162 J", "−362 J"], "D"),
    "Work–energy theorem with a non-conservative force",
    "The total work done by all forces equals the change in kinetic energy. Gravity does +mgh; the rest of the "
    "change is due to air resistance.",
    ["ΔK = ½ × 1 × 18² − 0 = 162 J", "W_gravity = 1 × 10 × 20 = 200 J",
     "W_air = ΔK − W_gravity = 162 − 200 = −38 J"],
    why="38 J has the wrong sign: air resistance opposes the motion and does negative work. −162 J takes the whole "
        "kinetic energy as lost. −362 J adds the two energies instead of subtracting.",
    ncert="Class 11 Physics, 'Work, Energy and Power', the work-energy theorem", seconds=55, recomputed=True)

k_s, x1_, x2_ = 400.0, 0.05, 0.10
W_s = 0.5 * k_s * (x2_ ** 2 - x1_ ** 2)
assert close(W_s, 1.5) and close(0.5 * k_s * (x2_ - x1_) ** 2, 0.5) and close(0.5 * k_s * x2_ ** 2, 2.0)
add(T, "Spring potential energy", "Intermediate", "numerical",
    "A spring of spring constant 400 N/m is already stretched by 5 cm from its natural length. The work needed to "
    "stretch it further, so that its extension becomes 10 cm, is:",
    place("1.5 J", ["0.5 J", "2.0 J", "2.5 J"], "C"),
    "Work done in stretching a spring",
    "The work done against the spring force equals the increase in its elastic potential energy, ½kx², between "
    "the two extensions.",
    ["U(10 cm) = ½ × 400 × 0.10² = 2.0 J", "U(5 cm) = ½ × 400 × 0.05² = 0.5 J", "W = 2.0 − 0.5 = 1.5 J"],
    why="0.5 J uses ½k(x₂ − x₁)², as if the spring started unstretched. 2.0 J ignores the initial stretch. 2.5 J adds "
        "the two energies.",
    ncert="Class 11 Physics, 'Work, Energy and Power', the potential energy of a spring", seconds=50, recomputed=True)

m_bob, g = 0.2, 10.0
# released from rest with string horizontal: v² at bottom = 2gL, T - mg = mv²/L
T_bottom = m_bob * g + m_bob * 2 * g
assert close(T_bottom, 6.0) and close(T_bottom, 3 * m_bob * g)
add(T, "Motion in a vertical circle", "Intermediate", "numerical",
    "A small bob of mass 0.2 kg hangs from a light inextensible string. The bob is pulled aside until the string is "
    "horizontal and taut, and is then released from rest. Taking g = 10 m/s², the tension in the string as the bob "
    "passes through its lowest point is:",
    place("6 N", ["2 N", "4 N", "10 N"], "B"),
    "Energy conservation with the centripetal force equation",
    "Energy conservation gives the speed at the bottom; at the bottom the net upward force T − mg supplies the "
    "centripetal force mv²/L. The length of the string cancels.",
    ["Fall height = L → v² = 2gL", "T − mg = mv²/L = 2mg", "T = 3mg = 3 × 0.2 × 10 = 6 N"],
    why="2 N is just the weight (no centripetal term). 4 N is mv²/L alone, forgetting to add the weight. 10 N (5mg) "
        "is the tension at the lowest point when the bob just completes a full vertical circle, a different motion.",
    ncert="Class 11 Physics, 'Work, Energy and Power', conservation of mechanical energy", seconds=60,
    recomputed=True)

add(T, "Collisions", "Intermediate", "assertion_reason",
    AR_STEM.format(
        a="In a one-dimensional elastic collision between two bodies, the kinetic energy of each body is the same "
          "after the collision as before it.",
        r="In an elastic collision, the total kinetic energy of the colliding bodies after the collision is equal to "
          "that before the collision."),
    ar("D"),
    "What is conserved in an elastic collision",
    "Elastic means the total kinetic energy of the system is conserved, not the kinetic energy of each body. "
    "Kinetic energy is usually transferred from one body to the other; for example, a moving ball striking an "
    "identical ball at rest stops and gives all its kinetic energy to the other.",
    ["A: equal masses, one at rest — velocities exchange, so each body's KE changes → false",
     "R: definition of an elastic collision → true"],
    why="A wrongly applies to each body a conservation law that holds only for the system.",
    ncert="Class 11 Physics, 'Work, Energy and Power', collisions", seconds=40)

m_p, v_end, t_end = 2.0, 10.0, 5.0
a_p = v_end / t_end
F_p = m_p * a_p
assert close(F_p * v_end, 40.0) and close(0.5 * m_p * v_end ** 2 / t_end, 20.0)
add(T, "Power", "Advanced", "numerical",
    "A constant net force acts on a body of mass 2 kg, initially at rest, and gives it a speed of 10 m/s in 5 s. The "
    "instantaneous power delivered by the force at the end of the 5 s is:",
    place("40 W", ["20 W", "100 W", "8 W"], "A"),
    "Instantaneous power P = F · v",
    "With a constant force the speed rises steadily, so the power Fv also rises steadily. The instantaneous power at "
    "the end is twice the average power over the interval.",
    ["a = 10/5 = 2 m/s² → F = 2 × 2 = 4 N", "P = Fv = 4 × 10 = 40 W",
     "Check: average power = ΔK/t = 100/5 = 20 W = half the final power ✓"],
    why="20 W is the average power over the 5 s. 100 W is the kinetic energy gained (in joules), not a rate. 8 W "
        "multiplies the force by the acceleration.",
    ncert="Class 11 Physics, 'Work, Energy and Power', power", seconds=60, recomputed=True)

h0, keep = 12.5, 0.64
h2 = h0 * keep ** 2
assert close(h0 * keep, 8.0) and close(h2, 5.12) and close(h0 * (1 - 2 * 0.36), 3.5) and close(h0 * 0.36 ** 2, 1.62)
add(T, "Collisions", "Advanced", "numerical",
    "A ball is dropped from rest from a height of 12.5 m onto a hard horizontal floor. At each impact it loses 36% of "
    "the kinetic energy it has just before the impact. Neglecting air resistance, the maximum height it reaches after "
    "the second impact is:",
    place("5.12 m", ["8.0 m", "3.5 m", "1.62 m"], "C"),
    "Energy loss in successive inelastic impacts",
    "Without air resistance, the kinetic energy just before an impact equals mg × (height fallen), and the height "
    "reached after the impact is proportional to the kinetic energy kept. Each impact keeps 64% of the energy, so "
    "each rebound height is 0.64 of the previous one.",
    ["After the 1st impact: h₁ = 0.64 × 12.5 = 8.0 m", "After the 2nd impact: h₂ = 0.64 × 8.0 = 5.12 m"],
    why="8.0 m is the height after only the first impact. 3.5 m subtracts 36% of the original height twice "
        "instead of compounding. 1.62 m keeps 36% at each impact instead of losing 36%.",
    ncert="Class 11 Physics, 'Work, Energy and Power', collisions and conservation of mechanical energy", seconds=70,
    recomputed=True)

multi_key([True, False, True, False, True], "ace")
add(T, "Work-energy theorem", "Advanced", "multi_statement",
    multi("Which of the following statements are correct?",
          ["The work done by the net force on a body equals the change in its kinetic energy.",
           "Power is a vector quantity, because it is the product of force and velocity.",
           "The kinetic energy of a body can never be negative.",
           "If the linear momentum of a body increases by 100%, its kinetic energy also increases by 100%.",
           "The work done by kinetic friction on a block sliding over a fixed rough floor is negative."]),
    place("(a), (c) and (e) only", ["(a), (b) and (c) only", "(c), (d) and (e) only", "(a), (c), (d) and (e) only"],
          "B"),
    "Work, energy and power",
    "The work–energy theorem relates the net work to ΔK. Power is the scalar product F · v, so it is a scalar. "
    "K = ½mv² can never be negative. K = p²/2m, so doubling p multiplies K by 4 (an increase of 300%). On a fixed "
    "floor, kinetic friction acts opposite to the block's displacement, so its work is negative.",
    ["(a) Work–energy theorem → true", "(b) P = F · v is a scalar → false", "(c) ½mv² ≥ 0 → true",
     "(d) p → 2p gives K → 4K, a 300% increase → false", "(e) friction opposite to displacement → W < 0 → true"],
    why="Codes containing (b) treat a dot product as a vector; codes containing (d) assume K ∝ p instead of K ∝ p².",
    ncert="Class 11 Physics, 'Work, Energy and Power', work-energy theorem and power", seconds=90)


# =====================================================================================================================
# Rotational Motion (B4 I5 A4)
# =====================================================================================================================
T = "Rotational Motion"

alpha_w, t_w = 2.0, 5.0
theta_w = 0.5 * alpha_w * t_w ** 2
assert close(theta_w, 25.0) and close(alpha_w * t_w, 10.0) and close(alpha_w * t_w ** 2, 50.0)
add(T, "Rigid-body rotation", "Basic", "numerical",
    "A wheel starts from rest and rotates about a fixed axis with a uniform angular acceleration of 2 rad/s². The "
    "angle through which it turns in the first 5 s is:",
    place("25 rad", ["10 rad", "50 rad", "12.5 rad"], "D"),
    "Kinematics of rotation with constant angular acceleration",
    "The rotational equations have the same form as the linear ones: θ = ω₀t + ½αt².",
    ["ω₀ = 0", "θ = ½ × 2 × 5² = 25 rad"],
    why="10 rad is the final angular velocity αt in rad/s. 50 rad drops the factor ½. 12.5 rad uses ¼αt².",
    ncert="Class 11 Physics, 'System of Particles and Rotational Motion', kinematics of rotational motion about a "
          "fixed axis", seconds=30, recomputed=True)

I_pts = 1.0 * 0.5 ** 2 + 2.0 * 1.0 ** 2
assert close(I_pts, 2.25) and close(1.0 * 0.5 + 2.0 * 1.0, 2.5) and close(3.0 * 0.25, 0.75)
add(T, "Moment of inertia and axis theorems", "Basic", "numerical",
    "Two small balls of masses 1 kg and 2 kg are fixed to a light rigid rod at distances of 0.5 m and 1.0 m "
    "respectively from an axis perpendicular to the rod. The moment of inertia of the system about this axis is:",
    place("2.25 kg m²", ["2.5 kg m²", "3.0 kg m²", "0.75 kg m²"], "A"),
    "Moment of inertia of point masses",
    "For point masses, I = Σ mᵢrᵢ², where rᵢ is the perpendicular distance of each mass from the axis.",
    ["I = 1 × 0.5² + 2 × 1.0² = 0.25 + 2.0 = 2.25 kg m²"],
    why="2.5 kg m² uses Σmr without squaring the distances. 3.0 kg m² puts both masses at 1 m. 0.75 kg m² puts both "
        "masses at 0.5 m.",
    ncert="Class 11 Physics, 'System of Particles and Rotational Motion', moment of inertia", seconds=30,
    recomputed=True)

add(T, "Rigid-body rotation", "Basic", "match_list",
    match_stem("For a rigid body rotating about a fixed axis, with moment of inertia I and angular velocity ω about "
               "that axis, match List-I (quantity) with List-II (expression). τ is a constant torque about the axis.",
               ["Rotational kinetic energy", "Angular momentum about the axis",
                "Power delivered by the torque", "Work done by the torque in turning the body through an angle θ"],
               ["τθ", "½Iω²", "τω", "Iω"]),
    match_options({"A": "II", "B": "IV", "C": "III", "D": "I"},
                  [{"A": "IV", "B": "II", "C": "III", "D": "I"}, {"A": "II", "B": "IV", "C": "I", "D": "III"},
                   {"A": "II", "B": "III", "C": "IV", "D": "I"}], "C"),
    "Rotational analogues of linear formulas",
    "Replace m by I, v by ω, F by τ and x by θ in the linear formulas: K = ½mv² → ½Iω²; p = mv → L = Iω; P = Fv → "
    "τω; W = Fx → τθ.",
    ["Rotational KE → ½Iω² (II)", "Angular momentum → Iω (IV)", "Power → τω (III)", "Work → τθ (I)"],
    why="The other codes swap kinetic energy with angular momentum, or power with work.",
    ncert="Class 11 Physics, 'System of Particles and Rotational Motion', work done by a torque; angular momentum in "
          "case of rotation about a fixed axis", seconds=40)

add(T, "Torque and angular momentum", "Basic", "direct",
    "The angular momentum of a particle about a point is the moment, about that point, of the particle's:",
    place("Linear momentum", ["Force", "Kinetic energy", "Mass"], "B"),
    "Definition of angular momentum",
    "Angular momentum of a particle about a point O is l = r × p, where r is its position vector from O and p its "
    "linear momentum. In the same way, torque τ = r × F is the moment of force.",
    ["l = r × p → moment of linear momentum", "τ = r × F → moment of force (that is torque, not angular momentum)"],
    why="The moment of a force is torque. Kinetic energy and mass are scalars; a 'moment' is defined through the "
        "vector product r × (vector).",
    ncert="Class 11 Physics, 'System of Particles and Rotational Motion', angular momentum of a particle",
    seconds=25)

I_d, w_d, t_d = 0.2, 10.0, 4.0
tau_d = I_d * w_d / t_d
assert close(tau_d, 0.5) and close(I_d * w_d, 2.0) and close(I_d * w_d * t_d, 8.0)
add(T, "Torque and angular momentum", "Intermediate", "numerical",
    "A disc of moment of inertia 0.2 kg m² is rotating at 10 rad/s about a fixed axis. A constant braking torque "
    "brings it to rest in 4 s. The magnitude of the braking torque is:",
    place("0.5 N m", ["2.0 N m", "8.0 N m", "0.25 N m"], "B"),
    "Torque as the rate of change of angular momentum",
    "For rotation about a fixed axis, τ = dL/dt. A constant torque changes L = Iω uniformly.",
    ["Initial L = Iω = 0.2 × 10 = 2.0 kg m²/s; final L = 0",
     "τ = ΔL/Δt = 2.0/4 = 0.5 N m"],
    why="2.0 N m is the initial angular momentum, not divided by the time. 8.0 N m multiplies by the time. 0.25 N m "
        "uses half the change in angular momentum.",
    ncert="Class 11 Physics, 'System of Particles and Rotational Motion', angular momentum in case of rotation about "
          "a fixed axis", seconds=40, recomputed=True)

I_fw, rpm = 2.0, 600
w_fw = 2 * math.pi * rpm / 60
K_fw = 0.5 * I_fw * w_fw ** 2
assert close(w_fw, 20 * math.pi) and close(K_fw, 400 * math.pi ** 2) and close(0.5 * I_fw * 600 ** 2, 3.6e5)
assert close(0.5 * I_fw * (10 * math.pi) ** 2, 100 * math.pi ** 2) and close(I_fw * w_fw, 40 * math.pi)
add(T, "Rigid-body rotation", "Intermediate", "numerical",
    "A flywheel of moment of inertia 2 kg m² rotates about its axis at 600 revolutions per minute. Its rotational "
    "kinetic energy is:",
    place("400π² J", ["100π² J", "3.6 × 10⁵ J", "40π J"], "D"),
    "Rotational kinetic energy",
    "Convert the rotation rate to angular velocity in rad/s (ω = 2πf, with f in revolutions per second), then use "
    "K = ½Iω².",
    ["f = 600/60 = 10 rev/s → ω = 2π × 10 = 20π rad/s",
     "K = ½ × 2 × (20π)² = 400π² J ≈ 3.95 kJ"],
    why="100π² J uses ω = πf (forgetting the 2 in 2πf). 3.6 × 10⁵ J uses ω = 600 rad/s with no conversion. 40π J is "
        "the angular momentum Iω, not the energy.",
    ncert="Class 11 Physics, 'System of Particles and Rotational Motion', kinematics of rotational motion; rotational "
          "kinetic energy", seconds=50, recomputed=True)

add(T, "Torque and angular momentum", "Intermediate", "assertion_reason",
    AR_STEM.format(
        a="The angular momentum of a particle moving with constant velocity along a straight line is constant about "
          "any fixed point.",
        r="No net force acts on a particle moving with constant velocity, so the torque on it about any fixed point "
          "is zero."),
    ar("A"),
    "Torque and conservation of angular momentum of a particle",
    "dl/dt = τ = r × F. With F = 0 the torque about every fixed point is zero, so l = r × p stays constant. "
    "Geometrically, |l| = p × (perpendicular distance of the line from the point), and both factors are constant.",
    ["F = 0 → τ = r × F = 0 about any point", "dl/dt = τ = 0 → l constant",
     "Check: |l| = p d⊥, with p and d⊥ fixed"],
    why="R is the reason for A: zero torque is exactly the condition for angular momentum to be conserved.",
    ncert="Class 11 Physics, 'System of Particles and Rotational Motion', torque and angular momentum", seconds=50)

add(T, "Equilibrium of rigid bodies", "Intermediate", "statement_pair",
    SP_STEM.format(
        s1="A rigid body in rotational equilibrium must be at rest.",
        s2="The torque of a force about a point is zero if the line of action of the force passes through that "
           "point."),
    sp("D"),
    "Rotational equilibrium and torque",
    "Rotational equilibrium means zero net torque, so the angular momentum is constant: a body rotating at a "
    "constant angular velocity (a freely spinning wheel with no friction) is in rotational equilibrium without being "
    "at rest. Torque τ = rF sin θ = F × (perpendicular distance of the line of action from the point), which is zero "
    "when the line passes through the point.",
    ["Statement I: zero net torque allows uniform rotation → false",
     "Statement II: perpendicular distance r⊥ = 0 → τ = 0 → true"],
    why="Statement I confuses equilibrium (zero net torque) with rest, just as translational equilibrium allows "
        "uniform motion.",
    ncert="Class 11 Physics, 'System of Particles and Rotational Motion', equilibrium of a rigid body", seconds=45)

I_rod_c, I_rod_end = F(1, 12), F(1, 3)
assert I_rod_end / I_rod_c == 4
I_ring_dia, I_disc_perp, I_disc_dia = F(1, 2), F(1, 2), F(1, 4)
assert I_disc_dia < I_disc_perp
multi_key([True, False, True, True, False], "acd")
add(T, "Moment of inertia and axis theorems", "Intermediate", "multi_statement",
    multi("Which of the following statements about moment of inertia are correct?",
          ["The theorem of parallel axes applies to a body of any shape.",
           "The theorem of perpendicular axes applies to three-dimensional bodies of any shape.",
           "The moment of inertia of a body depends on the position and orientation of the axis of rotation.",
           "The moment of inertia of a thin uniform rod about an axis perpendicular to it through one end is four "
           "times its moment of inertia about a parallel axis through its centre.",
           "The moment of inertia of a uniform disc about a diameter is greater than about the axis through its "
           "centre perpendicular to its plane."]),
    place("(a), (c) and (d) only", ["(a), (b) and (c) only", "(c), (d) and (e) only", "(a), (c), (d) and (e) only"],
          "A"),
    "Theorems of parallel and perpendicular axes",
    "The parallel axes theorem I = I_cm + Md² holds for any body. The perpendicular axes theorem I_z = I_x + I_y "
    "holds only for a planar body (lamina). For a rod, I_end = ML²/12 + M(L/2)² = ML²/3, four times ML²/12. For a "
    "disc, the perpendicular axes theorem gives I_diameter = ½ × MR²/2 = MR²/4, which is less than MR²/2.",
    ["(a) true — any body", "(b) false — laminae only", "(c) true — I depends on the axis",
     "(d) ML²/3 ÷ ML²/12 = 4 → true", "(e) MR²/4 < MR²/2 → false"],
    why="Codes containing (b) extend the perpendicular axes theorem beyond plane bodies; codes containing (e) "
        "reverse the two moments of inertia of the disc.",
    ncert="Class 11 Physics, 'System of Particles and Rotational Motion', theorems of perpendicular and parallel axes",
    seconds=90)

M_disc = F(1)
m_cut, x_cut_c = F(1, 4), F(1, 2)       # mass fraction removed (radius R/2), centre of the cut part at R/2
x_rem = -(m_cut * x_cut_c) / (M_disc - m_cut)
assert x_rem == F(-1, 6) and m_cut * x_cut_c == F(1, 8) and m_cut * 1 / (1 - m_cut) == F(1, 3)
add(T, "Centre of mass", "Advanced", "numerical",
    "From a uniform circular disc of radius R, a circular hole of radius R/2 is cut out. The edge of the hole touches "
    "the rim of the disc, so the centre of the hole is at a distance R/2 from the centre O of the original disc. The "
    "centre of mass of the remaining part is at a distance from O of:",
    place("R/6, on the side opposite to the hole", ["R/8, on the side opposite to the hole",
                                                    "R/3, on the side opposite to the hole",
                                                    "R/6, on the same side as the hole"], "C"),
    "Centre of mass of a body with a part removed",
    "Treat the remaining part as the full disc minus the removed disc. The mass of a uniform disc is proportional "
    "to its area, so the hole has a quarter of the mass. Taking O as origin, the full disc's centre of mass is at O.",
    ["Mass of hole = M/4 (area ratio (R/2)²/R² = 1/4); remaining mass = 3M/4",
     "M × 0 = (3M/4) x + (M/4)(R/2) → x = −R/6",
     "The centre of mass is R/6 from O, on the side away from the hole"],
    why="R/8 divides by the full mass M instead of the remaining 3M/4. R/3 places the centre of the hole at a "
        "distance R from O instead of R/2. R/6 on the same side gets the sign wrong: removing mass shifts the "
        "centre of mass away from the hole.",
    ncert="Class 11 Physics, 'System of Particles and Rotational Motion', centre of mass", seconds=85,
    recomputed=True)

M_rod, L_rod, m_put, v_put = 0.9, 1.0, 0.1, 10.0
L_ang = m_put * v_put * L_rod / 2
I_tot = M_rod * L_rod ** 2 / 12 + m_put * (L_rod / 2) ** 2
w_rod = L_ang / I_tot
assert close(I_tot, 0.1) and close(w_rod, 5.0) and close(L_ang / (M_rod * L_rod ** 2 / 12), 20 / 3)
assert close(m_put * v_put / (M_rod + m_put) / (L_rod / 2), 2.0)
add(T, "Torque and angular momentum", "Advanced", "numerical",
    "A uniform rod of mass 0.9 kg and length 1.0 m lies at rest on a smooth horizontal table. It is pivoted at its "
    "centre so that it can rotate freely about a fixed vertical axis. A small lump of putty of mass 0.1 kg, moving "
    "horizontally at 10 m/s perpendicular to the rod, strikes one end of the rod and sticks to it. The angular "
    "velocity of the rod just after the impact is:",
    place("5 rad/s", ["20/3 rad/s", "2 rad/s", "10 rad/s"], "B"),
    "Conservation of angular momentum about a fixed axis",
    "During the short impact the pivot exerts a force, so linear momentum is not conserved; but that force passes "
    "through the axis and has no torque about it, so angular momentum about the axis is conserved.",
    ["Before: L = mv(L/2) = 0.1 × 10 × 0.5 = 0.5 kg m²/s",
     "After: I = ML²/12 + m(L/2)² = 0.075 + 0.025 = 0.1 kg m²",
     "ω = 0.5/0.1 = 5 rad/s"],
    why="20/3 rad/s leaves out the putty's own moment of inertia after it sticks. 2 rad/s conserves linear "
        "momentum, which the pivot force does not allow. 10 rad/s comes from ω = v/L with no conservation law at all.",
    ncert="Class 11 Physics, 'System of Particles and Rotational Motion', conservation of angular momentum",
    seconds=100, recomputed=True)

L_r2, g = 1.5, 10.0
alpha_r = (g * L_r2 / 2) / (L_r2 ** 2 / 3)
assert close(alpha_r, 10.0) and close(alpha_r, 3 * g / (2 * L_r2)) and close(g / L_r2, 20 / 3)
assert close(3 * g / L_r2, 20.0) and close((g * L_r2 / 2) / (L_r2 ** 2 / 12), 40.0)
add(T, "Rigid-body rotation", "Advanced", "numerical",
    "A uniform rod of length 1.5 m is hinged at one end so that it can rotate freely in a vertical plane about a "
    "horizontal axis through the hinge. It is held horizontal and then released. Taking g = 10 m/s², its angular "
    "acceleration just after release is:",
    place("10 rad/s²", ["20/3 rad/s²", "20 rad/s²", "40 rad/s²"], "D"),
    "τ = Iα about a fixed axis",
    "Just after release the angular velocity is zero, and the only torque about the hinge is that of the weight, "
    "acting at the centre of mass at L/2 from the hinge. The moment of inertia about the end is ML²/3.",
    ["τ = Mg(L/2)", "I = ML²/3", "α = τ/I = 3g/(2L) = 30/3 = 10 rad/s²"],
    why="20/3 rad/s² is g/L, treating the rod as a point mass at its far end. 20 rad/s² (3g/L) puts the weight at "
        "the far end. 40 rad/s² uses ML²/12, the moment of inertia about the centre, instead of about the hinge.",
    ncert="Class 11 Physics, 'System of Particles and Rotational Motion', dynamics of rotational motion about a fixed "
          "axis", seconds=75, recomputed=True)

multi_key([True, True, False, True, False], "abd")
add(T, "Rigid-body rotation", "Advanced", "multi_statement",
    multi("For a rigid body rotating about a fixed axis, which of the following statements are correct?",
          ["If the angular acceleration α is constant, the angular velocity at time t is ω = ω₀ + αt.",
           "The angular velocity vector is directed along the axis of rotation.",
           "All particles of the body have the same centripetal acceleration.",
           "If its angular momentum about the axis is L, its rotational kinetic energy is L²/2I.",
           "If no external torque acts and the body's moment of inertia about the axis is halved (by redistributing "
           "its mass), its rotational kinetic energy also halves."]),
    place("(a), (b) and (d) only", ["(a), (b), (d) and (e) only", "(b), (c) and (d) only", "(a), (c) and (e) only"],
          "A"),
    "Kinematics and dynamics of fixed-axis rotation",
    "The rotational kinematic equations mirror the linear ones, and ω points along the axis (right-hand rule). Every "
    "particle has the same ω but the centripetal acceleration ω²r depends on its distance r from the axis. "
    "K = ½Iω² = L²/2I. With no external torque L is constant, so halving I doubles K (the extra energy comes from "
    "the internal work done in pulling the mass inward).",
    ["(a) true", "(b) true", "(c) ω²r differs with r → false", "(d) K = (Iω)²/2I = L²/2I → true",
     "(e) L fixed, I → I/2 gives K = L²/2I → doubles → false"],
    why="Codes containing (c) confuse equal angular velocity with equal centripetal acceleration; codes containing "
        "(e) forget that L, not ω, stays fixed.",
    ncert="Class 11 Physics, 'System of Particles and Rotational Motion', rotational motion about a fixed axis; "
          "conservation of angular momentum", seconds=90)

# =====================================================================================================================
# Gravitation (B3 I4 A3)
# =====================================================================================================================
T = "Gravitation"

g_ratio = F(1, 2) / F(1, 2) ** 2
assert g_ratio == 2
add(T, "Variation of g", "Basic", "numerical",
    "A planet has half the mass and half the radius of the Earth. If g is the acceleration due to gravity on the "
    "Earth's surface, the acceleration due to gravity on the planet's surface is:",
    place("2g", ["g", "g/2", "4g"], "C"),
    "g = GM/R²",
    "At the surface of a spherical body, g = GM/R². Scale the mass and the square of the radius.",
    ["g_p/g = (M_p/M)(R/R_p)² = (1/2)(2)² = 2", "g_p = 2g"],
    why="g assumes the two halvings cancel (they would only if g ∝ M/R). g/2 ignores the radius. 4g ignores the "
        "mass.",
    ncert="Class 11 Physics, 'Gravitation', acceleration due to gravity of the earth", seconds=30, recomputed=True)

add(T, "Law of gravitation", "Basic", "direct",
    "The value of the universal gravitational constant G was first determined experimentally by:",
    place("Henry Cavendish", ["Johannes Kepler", "Isaac Newton", "Tycho Brahe"], "D"),
    "History of the measurement of G",
    "Newton stated the law of gravitation but did not measure G. The English scientist Henry Cavendish measured it "
    "in 1798 with a torsion balance, using the tiny attraction between lead spheres.",
    ["G was measured in a laboratory with a torsion balance by Cavendish (1798)"],
    why="Kepler found the laws of planetary motion from Tycho Brahe's observations; Newton proposed the law of "
        "gravitation. None of them measured G.",
    ncert="Class 11 Physics, 'Gravitation', the gravitational constant", seconds=20)

add(T, "Gravitational potential and energy", "Basic", "match_list",
    match_stem("Match List-I (quantity) with List-II (its SI unit).",
               ["Universal gravitational constant G", "Gravitational potential", "Gravitational field intensity",
                "Gravitational potential energy"],
               ["J", "N kg⁻¹", "N m² kg⁻²", "J kg⁻¹"]),
    match_options({"A": "III", "B": "IV", "C": "II", "D": "I"},
                  [{"A": "III", "B": "II", "C": "IV", "D": "I"}, {"A": "I", "B": "IV", "C": "II", "D": "III"},
                   {"A": "III", "B": "I", "C": "II", "D": "IV"}], "B"),
    "Units of gravitational quantities",
    "From F = Gm₁m₂/r², G = Fr²/(m₁m₂) has unit N m² kg⁻². Potential is potential energy per unit mass (J kg⁻¹), "
    "field intensity is force per unit mass (N kg⁻¹, equivalent to m s⁻²), and potential energy is in joules.",
    ["G → N m² kg⁻² (III)", "Potential → J kg⁻¹ (IV)", "Field → N kg⁻¹ (II)", "Potential energy → J (I)"],
    why="The other codes interchange potential (energy per mass) and field (force per mass), or potential and "
        "potential energy.",
    ncert="Class 11 Physics, 'Gravitation', universal law of gravitation; gravitational potential energy",
    seconds=35)

r_p, r_a = 1.0, 3.0
assert close(r_a / r_p, 3.0)
add(T, "Kepler's laws", "Intermediate", "numerical",
    "A planet moves round the Sun in an elliptical orbit. Its greatest distance from the Sun (at aphelion) is three "
    "times its least distance (at perihelion). The ratio of its speed at perihelion to its speed at aphelion is:",
    place("3", ["1/3", "9", "√3"], "B"),
    "Conservation of angular momentum (Kepler's second law)",
    "The Sun's force on the planet is central, so the planet's angular momentum about the Sun is constant. At "
    "perihelion and aphelion the velocity is perpendicular to the radius, so L = mvr at both points.",
    ["m v_p r_p = m v_a r_a", "v_p/v_a = r_a/r_p = 3"],
    why="1/3 inverts the ratio (the planet is fastest when nearest the Sun). 9 squares the distance ratio. √3 uses "
        "the circular-orbit relation v ∝ 1/√r, which does not apply to two points of the same ellipse.",
    ncert="Class 11 Physics, 'Gravitation', Kepler's laws", seconds=45, recomputed=True)

V_c = -4 / (1 / math.sqrt(2))      # in units of Gm/a: four masses at distance a/√2
assert close(V_c, -4 * math.sqrt(2))
add(T, "Gravitational potential and energy", "Intermediate", "numerical",
    "Four particles, each of mass m, are placed at the corners of a square of side a. The gravitational potential at "
    "the centre of the square is (G is the universal gravitational constant):",
    place("−4√2 Gm/a", ["−4Gm/a", "−2√2 Gm/a", "Zero"], "A"),
    "Superposition of gravitational potential",
    "Potential is a scalar, so the potentials of the four masses simply add. Each corner is half a diagonal, a/√2, "
    "from the centre.",
    ["Distance of each corner from the centre = a√2/2 = a/√2",
     "V = 4 × (−Gm/(a/√2)) = −4√2 Gm/a"],
    why="−4Gm/a takes the distance as a. −2√2 Gm/a takes it as the full diagonal a√2. Zero is the gravitational "
        "field at the centre (the vector contributions cancel), not the potential, which is a scalar and never "
        "cancels.",
    ncert="Class 11 Physics, 'Gravitation', gravitational potential energy", seconds=50, recomputed=True)

v_ratio = math.sqrt(1 / 4)          # v_e ∝ √(1/r); r = R + 3R = 4R
assert close(v_ratio, 0.5)
add(T, "Escape and orbital velocity", "Intermediate", "numerical",
    "The escape speed of a body from the Earth's surface is vₑ. Neglecting the Earth's rotation and the atmosphere, "
    "the escape speed of a body from a point at a height 3R above the surface (R = radius of the Earth) is:",
    place("vₑ/2", ["vₑ/√3", "vₑ/4", "vₑ/√2"], "D"),
    "Escape speed from a point at distance r from the Earth's centre",
    "To escape from a point at distance r from the centre, ½mv² must equal GMm/r, so v = √(2GM/r) ∝ 1/√r. The "
    "distance from the centre here is R + 3R = 4R.",
    ["v = √(2GM/4R) = ½√(2GM/R) = vₑ/2"],
    why="vₑ/√3 uses the height 3R instead of the distance 4R from the centre. vₑ/4 takes v ∝ 1/r. vₑ/√2 would be the "
        "answer at a height R.",
    ncert="Class 11 Physics, 'Gravitation', escape speed", seconds=45, recomputed=True)

add(T, "Gravitational potential and energy", "Intermediate", "assertion_reason",
    AR_STEM.format(
        a="When a body is moved farther away from the Earth, the gravitational potential energy of the body–Earth "
          "system increases.",
        r="The gravitational force is attractive, so an external agent must do positive work against it to increase "
          "the separation slowly."),
    ar("A"),
    "Sign of gravitational potential energy",
    "The change in potential energy equals the work done by an external agent moving the body slowly (without "
    "change in kinetic energy). Because gravity pulls the body back, that work is positive when the separation "
    "increases, so U = −GMm/r rises towards zero.",
    ["U = −GMm/r: r larger → U less negative → U increases",
     "ΔU = W_external > 0 since gravity is attractive"],
    why="R gives the physical reason for A, so both are true and R explains A.",
    ncert="Class 11 Physics, 'Gravitation', gravitational potential energy", seconds=45)

R_e, g = 6.4e6, 10.0
v_drop = math.sqrt(2 * g * R_e * (1 - 1 / 2))     # GM/R - GM/2R = gR/2 per unit mass; v² = 2 × that
assert close(v_drop, 8000.0) and close(math.sqrt(2 * g * R_e), 11313.7, 1e-4)
add(T, "Gravitational potential and energy", "Advanced", "numerical",
    "A body is released from rest at a height above the Earth's surface equal to the Earth's radius R. Neglect air "
    "resistance and the Earth's rotation, and take R = 6400 km and g = 10 m/s² at the surface. The speed with which "
    "it strikes the Earth's surface is:",
    place("8.0 km/s", ["11.3 km/s", "5.7 km/s", "4.0 km/s"], "B"),
    "Energy conservation with U = −GMm/r",
    "Over a fall comparable to R, g is not constant, so use U = −GMm/r instead of mgh, together with GM = gR².",
    ["Loss of PE = GMm/R − GMm/2R = GMm/2R = mgR/2",
     "½mv² = mgR/2 → v = √(gR) = √(10 × 6.4 × 10⁶) = 8 × 10³ m/s"],
    why="11.3 km/s uses v = √(2gR), treating g as constant over the whole height R. 5.7 km/s is √(gR/2). 4.0 km/s "
        "halves the correct speed.",
    ncert="Class 11 Physics, 'Gravitation', gravitational potential energy", seconds=80, recomputed=True)

R_km = 6400
h_exact = R_km * (1 / 0.8 - 1)
h_approx = R_km * (1 - 0.64) / 2
assert close(h_exact, 1600.0) and close(h_approx, 1152.0)
add(T, "Variation of g", "Advanced", "numerical",
    "Taking the Earth's radius as 6400 km and ignoring its rotation, the height above the Earth's surface at which "
    "the acceleration due to gravity becomes 64% of its value at the surface is:",
    place("1600 km", ["1152 km", "3200 km", "2304 km"], "C"),
    "Exact variation of g with height",
    "g(h) = g R²/(R + h)². The approximation g(1 − 2h/R) is valid only for h ≪ R; a 36% drop in g is far outside "
    "that range, so the exact expression must be used.",
    ["R²/(R + h)² = 0.64 → R/(R + h) = 0.8", "R + h = 1.25R → h = 0.25R = 1600 km"],
    why="1152 km uses the small-height formula 1 − 2h/R = 0.64, which is not valid for so large a change. 3200 km is "
        "R/2. 2304 km uses 1 − h/R = 0.64.",
    ncert="Class 11 Physics, 'Gravitation', acceleration due to gravity below and above the surface of earth",
    seconds=70, recomputed=True)

multi_key([True, False, True, False, True], "ace")
add(T, "Gravitational potential and energy", "Advanced", "multi_statement",
    multi("Which of the following statements are correct? Take the gravitational potential to be zero at infinity, "
          "and treat the Earth as a uniform sphere.",
          ["The gravitational potential at a point is the work done by an external agent, per unit mass, in bringing "
           "a body slowly from infinity to that point.",
           "The gravitational potential everywhere inside a uniform thin spherical shell is zero.",
           "The gravitational field everywhere inside a uniform thin spherical shell is zero.",
           "The acceleration due to gravity is greatest at the centre of the Earth.",
           "For a height h much smaller than the Earth's radius, the increase in gravitational potential energy of a "
           "body of mass m raised through h from the surface is approximately mgh."]),
    place("(a), (c) and (e) only", ["(a), (b), (c) and (e) only", "(b), (c) and (d) only", "(a), (d) and (e) only"],
          "A"),
    "Gravitational potential, field and shells",
    "Inside a uniform thin shell the field is zero, so the potential does not change from point to point — it is "
    "constant at its surface value −GM/R, not zero. Inside a uniform Earth g = g₀(1 − d/R) decreases to zero at the "
    "centre. Near the surface the exact ΔU = GMm[1/R − 1/(R + h)] reduces to mgh for h ≪ R.",
    ["(a) definition of potential → true", "(b) V = −GM/R (constant, not zero) → false",
     "(c) E = 0 inside the shell → true", "(d) g = 0 at the centre → false",
     "(e) ΔU ≈ mgh for h ≪ R → true"],
    why="Codes containing (b) confuse zero field with zero potential; zero field only means the potential is "
        "constant. Codes containing (d) reverse the variation of g with depth.",
    ncert="Class 11 Physics, 'Gravitation', gravitational potential energy; acceleration due to gravity below the "
          "surface", seconds=90)


# =====================================================================================================================
# Properties of Solids and Liquids (B5 I6 A5)
# =====================================================================================================================
T = "Properties of Solids and Liquids"

strain = 1e-3 / 2.0
assert close(strain, 5e-4) and close(2.0 / 1e-3, 2e3) and close(1 / 2.0, 0.5)
add(T, "Elasticity and moduli", "Basic", "numerical",
    "A wire 2 m long is stretched so that its length increases by 1 mm. The longitudinal strain in the wire is:",
    place("5 × 10⁻⁴", ["2 × 10³", "5 × 10⁻¹", "2 × 10⁻³"], "B"),
    "Longitudinal strain",
    "Longitudinal strain is the change in length divided by the original length, both in the same unit. It has no "
    "unit.",
    ["ΔL = 1 mm = 1 × 10⁻³ m, L = 2 m", "Strain = 10⁻³/2 = 5 × 10⁻⁴"],
    why="2 × 10³ is L/ΔL, the ratio inverted. 5 × 10⁻¹ divides 1 (mm) by 2 (m) without converting units. 2 × 10⁻³ "
        "multiplies instead of dividing.",
    ncert="Class 11 Physics, 'Mechanical Properties of Solids', stress and strain", seconds=25, recomputed=True)

A1_, v1_, A2_ = 4.0, 2.0, 1.0
v2_ = A1_ * v1_ / A2_
assert close(v2_, 8.0) and close(A2_ * v1_ / A1_, 0.5) and close(v1_ * math.sqrt(A1_ / A2_), 4.0)
add(T, "Bernoulli's principle", "Basic", "numerical",
    "Water flows steadily through a pipe. At a section where the cross-sectional area is 4 cm², the speed of the "
    "water is 2 m/s. The speed at a narrower section of area 1 cm² is:",
    place("8 m/s", ["0.5 m/s", "4 m/s", "32 m/s"], "D"),
    "Equation of continuity",
    "For the steady flow of an incompressible liquid, the volume flowing past every cross-section per second is the "
    "same: A₁v₁ = A₂v₂.",
    ["4 × 2 = 1 × v₂", "v₂ = 8 m/s"],
    why="0.5 m/s inverts the area ratio (the liquid must speed up where the pipe narrows). 4 m/s uses the square root "
        "of the area ratio, as if speed depended on the radius ratio. 32 m/s squares the area ratio.",
    ncert="Class 11 Physics, 'Mechanical Properties of Fluids', streamline flow (equation of continuity)", seconds=30,
    recomputed=True)

L_rail, alpha_s, dT = 10.0, 1.2e-5, 40.0
dL_rail = L_rail * alpha_s * dT
assert close(dL_rail, 4.8e-3) and close(3 * dL_rail, 14.4e-3)
add(T, "Thermal expansion and calorimetry", "Basic", "numerical",
    "A steel rail is 10 m long at 20 °C. The coefficient of linear expansion of steel is 1.2 × 10⁻⁵ K⁻¹. The increase "
    "in its length when its temperature rises to 60 °C is:",
    place("4.8 mm", ["0.48 mm", "48 mm", "14.4 mm"], "A"),
    "Linear expansion",
    "For a small temperature change, ΔL = αLΔT.",
    ["ΔT = 60 − 20 = 40 K", "ΔL = 1.2 × 10⁻⁵ × 10 × 40 = 4.8 × 10⁻³ m = 4.8 mm"],
    why="0.48 mm and 48 mm slip a power of ten in converting metres to millimetres. 14.4 mm uses 3α, the coefficient "
        "of volume expansion.",
    ncert="Class 11 Physics, 'Thermal Properties of Matter', thermal expansion", seconds=35, recomputed=True)

add(T, "Fluid pressure and Pascal's law", "Basic", "direct",
    "The hydraulic brakes of an automobile work on the principle of:",
    place("Pascal's law", ["Bernoulli's principle", "Archimedes' principle", "Stokes' law"], "C"),
    "Applications of Pascal's law",
    "In hydraulic brakes, a small force on the pedal increases the pressure in the brake fluid. By Pascal's law this "
    "pressure is transmitted undiminished through the enclosed fluid to the wider pistons at the wheels, which "
    "therefore exert a much larger force on the brake pads.",
    ["Pressure applied to an enclosed fluid is transmitted undiminished to every part of it → force multiplication"],
    why="Bernoulli's principle concerns flowing fluids, Archimedes' principle concerns buoyancy and Stokes' law "
        "gives the viscous drag on a moving sphere; none of them explains hydraulic brakes.",
    ncert="Class 11 Physics, 'Mechanical Properties of Fluids', Pascal's law (hydraulic machines)", seconds=20)

add(T, "Heat transfer", "Basic", "match_list",
    match_stem("Match List-I (law) with List-II (what it states).",
               ["Stefan–Boltzmann law", "Wien's displacement law", "Newton's law of cooling", "Hooke's law"],
               ["Within the elastic limit, stress is proportional to strain",
                "The wavelength at which a black body emits most strongly, multiplied by its absolute temperature, "
                "is a constant",
                "For a small temperature difference, the rate of loss of heat of a body is proportional to the "
                "difference between its temperature and that of its surroundings",
                "The energy radiated per unit time by a black body is proportional to the fourth power of its "
                "absolute temperature"]),
    match_options({"A": "IV", "B": "II", "C": "III", "D": "I"},
                  [{"A": "II", "B": "IV", "C": "III", "D": "I"}, {"A": "IV", "B": "III", "C": "II", "D": "I"},
                   {"A": "IV", "B": "II", "C": "I", "D": "III"}], "B"),
    "Laws of radiation, cooling and elasticity",
    "Stefan–Boltzmann: H ∝ T⁴. Wien: λₘT = constant. Newton's law of cooling: −dQ/dt ∝ (T − Tₛ) for small "
    "differences. Hooke's law: stress ∝ strain within the elastic limit.",
    ["Stefan–Boltzmann → IV", "Wien → II", "Newton's law of cooling → III", "Hooke → I"],
    why="The other codes swap the two radiation laws, or Newton's law of cooling with Wien's law.",
    ncert="Class 11 Physics, 'Thermal Properties of Matter', radiation and Newton's law of cooling; 'Mechanical "
          "Properties of Solids', Hooke's law", seconds=40)

dP, frac = 1.0e6, 0.05 / 100
B_mod = dP / frac
assert close(B_mod, 2.0e9) and close(dP / 0.05, 2.0e7) and close(dP * frac, 500.0)
add(T, "Elasticity and moduli", "Intermediate", "numerical",
    "When the pressure on a liquid is increased by 1.0 × 10⁶ Pa, its volume decreases by 0.05%. The bulk modulus of "
    "the liquid is:",
    place("2 × 10⁹ Pa", ["2 × 10⁷ Pa", "5 × 10⁻¹⁰ Pa", "5 × 10² Pa"], "A"),
    "Bulk modulus",
    "Bulk modulus B = Δp/(ΔV/V), the pressure change divided by the magnitude of the fractional change in volume. "
    "A percentage must be divided by 100 to get the fraction.",
    ["ΔV/V = 0.05/100 = 5 × 10⁻⁴", "B = 1.0 × 10⁶ / 5 × 10⁻⁴ = 2 × 10⁹ Pa"],
    why="2 × 10⁷ Pa uses 0.05 as the fraction (percentage not divided by 100). 5 × 10⁻¹⁰ is the compressibility "
        "1/B, with the wrong unit. 5 × 10² Pa multiplies the pressure by the volume strain.",
    ncert="Class 11 Physics, 'Mechanical Properties of Solids', bulk modulus", seconds=45, recomputed=True)

h_oil, h_w, rho_w = 10.0, 8.0, 1000.0
rho_oil = rho_w * h_w / h_oil
assert close(rho_oil, 800.0) and close(rho_w * h_oil / h_w, 1250.0)
add(T, "Fluid pressure and Pascal's law", "Intermediate", "numerical",
    "A U-tube open at both ends contains water. Some oil, which does not mix with water, is poured into one arm. In "
    "equilibrium the oil column stands 10 cm above the oil–water interface, while the water in the other arm stands "
    "8 cm above the level of that interface. Taking the density of water as 1000 kg/m³, the density of the oil is:",
    place("800 kg/m³", ["1250 kg/m³", "1000 kg/m³", "200 kg/m³"], "C"),
    "Equal pressures at the same level in a liquid at rest",
    "Points at the same horizontal level in the same continuous liquid (water here) are at the same pressure. Take "
    "the level of the oil–water interface: above it, one arm has 10 cm of oil and the other 8 cm of water, both open "
    "to the atmosphere.",
    ["P_atm + ρ_oil g (0.10) = P_atm + ρ_w g (0.08)", "ρ_oil = 1000 × 8/10 = 800 kg/m³"],
    why="1250 kg/m³ inverts the height ratio; a lighter liquid needs the taller column. 1000 kg/m³ ignores the "
        "height difference. 200 kg/m³ uses the 2 cm difference in heights.",
    ncert="Class 11 Physics, 'Mechanical Properties of Fluids', variation of pressure with depth", seconds=55,
    recomputed=True)

eta, A_pl, v_pl, d_pl = 1.5, 0.1, 0.2, 2e-3
F_visc = eta * A_pl * v_pl / d_pl
assert close(F_visc, 15.0) and close(eta * A_pl * v_pl / 2e-2, 1.5) and close(eta * A_pl * v_pl / 2, 0.015)
assert close(eta * A_pl * d_pl / v_pl, 1.5e-3)
add(T, "Viscosity and Stokes' law", "Intermediate", "numerical",
    "A flat plate of area 0.1 m² is moved at a steady speed of 0.2 m/s parallel to a fixed flat surface, separated "
    "from it by a 2 mm thick layer of a liquid of coefficient of viscosity 1.5 Pa s. Assuming the speed of the liquid "
    "changes uniformly across the layer, the force needed to keep the plate moving is:",
    place("15 N", ["1.5 N", "0.015 N", "1.5 × 10⁻³ N"], "B"),
    "Newton's law of viscosity",
    "The viscous force is F = ηA(dv/dx). With a uniform velocity gradient across the layer, dv/dx = v/d.",
    ["Velocity gradient = 0.2/(2 × 10⁻³) = 100 s⁻¹", "F = 1.5 × 0.1 × 100 = 15 N"],
    why="1.5 N takes the layer as 2 cm thick. 0.015 N leaves the thickness as '2' without converting millimetres to "
        "metres. 1.5 × 10⁻³ N uses d/v instead of v/d.",
    ncert="Class 11 Physics, 'Mechanical Properties of Fluids', viscosity", seconds=45, recomputed=True)

add(T, "Surface tension and capillarity", "Intermediate", "statement_pair",
    SP_STEM.format(
        s1="The surface tension of a liquid is numerically equal to the surface energy per unit area of its free "
           "surface.",
        s2="Water does not spread on a waxy surface but forms drops, because the angle of contact between water and "
           "wax is obtuse."),
    sp("A"),
    "Surface energy and angle of contact",
    "Increasing a liquid surface by area ΔA at constant temperature needs work SΔA, so the surface energy per unit "
    "area equals S (same dimensions, N/m = J/m²). When the cohesive forces in water exceed its adhesion to wax, the "
    "angle of contact is greater than 90° and water forms drops instead of wetting the surface.",
    ["Statement I: W = SΔA → S = energy per unit area → true",
     "Statement II: θ > 90° on a waxy (or oily) surface → water does not wet it → true"],
    why="Both statements are true; the usual traps (surface tension as force per area, acute angle for non-wetting) "
        "do not appear.",
    ncert="Class 11 Physics, 'Mechanical Properties of Fluids', surface tension (surface energy, angle of contact)",
    seconds=40)

add(T, "Bernoulli's principle", "Intermediate", "assertion_reason",
    AR_STEM.format(
        a="During a strong windstorm, a light roof can be lifted off a house even though the wind blows horizontally "
          "over it.",
        r="The fast-moving air above the roof is at a lower pressure than the nearly still air under the roof, as "
          "Bernoulli's principle predicts."),
    ar("A"),
    "Dynamic lift from a pressure difference",
    "Along a streamline, p + ½ρv² is constant (for horizontal flow). Air moving fast over the roof has a lower "
    "pressure than the still air inside, so the pressure difference across the roof times its area gives a net "
    "upward force.",
    ["p_inside − p_above ≈ ½ρv² > 0 → net upward force on the roof",
     "R gives exactly the cause of A"],
    why="The roof is lifted because of the pressure difference that R describes, so R explains A.",
    ncert="Class 11 Physics, 'Mechanical Properties of Fluids', Bernoulli's principle (dynamic lift)", seconds=40)

add(T, "Heat transfer", "Intermediate", "statement_pair",
    SP_STEM.format(
        s1="Heat can be transferred by natural convection within a solid.",
        s2="Of conduction, convection and radiation, only radiation can transfer heat through a vacuum."),
    sp("D"),
    "Modes of heat transfer",
    "Convection is the transfer of heat by the actual motion of matter, which is possible only in fluids (liquids "
    "and gases); natural convection arises when heated, less dense fluid rises under gravity. Conduction and "
    "convection need a medium, while radiation is carried by electromagnetic waves and needs none — that is how the "
    "Sun's heat reaches the Earth.",
    ["Statement I: the particles of a solid cannot flow → no convection → false",
     "Statement II: radiation needs no medium → true"],
    why="Statement I is false because convection needs bulk movement of the material, which a solid does not allow.",
    ncert="Class 11 Physics, 'Thermal Properties of Matter', heat transfer", seconds=35)

m_st, Lv, m_w, Tw, Tf = 10.0, 540.0, 145.0, 20.0, 60.0
assert close(m_st * Lv + m_st * (100 - Tf), m_w * (Tf - Tw))
T_noL = (m_st * 100 + m_w * Tw) / (m_st + m_w)
T_noCool = Tw + m_st * Lv / m_w
assert close(T_noL, 25.16, 1e-3) and close(T_noCool, 57.24, 1e-3)
add(T, "Thermal expansion and calorimetry", "Advanced", "numerical",
    "10 g of steam at 100 °C is passed into 145 g of water at 20 °C kept in an insulated container of negligible heat "
    "capacity, and all the steam condenses. Take the latent heat of vaporisation of water as 540 cal g⁻¹ and its "
    "specific heat as 1 cal g⁻¹ °C⁻¹. The final temperature of the mixture is:",
    place("60 °C", ["57.2 °C", "25.2 °C", "100 °C"], "D"),
    "Principle of calorimetry with a change of state",
    "Heat given out by the steam (latent heat on condensing, then the heat released as the condensed water cools to "
    "the final temperature T) equals the heat taken in by the cold water.",
    ["Heat lost by steam = 10 × 540 + 10 × 1 × (100 − T) = 6400 − 10T",
     "Heat gained by water = 145 × 1 × (T − 20) = 145T − 2900",
     "6400 − 10T = 145T − 2900 → 155T = 9300 → T = 60 °C",
     "Check: all the steam condenses, since 145 g of water needs 145 × 80 = 11 600 cal to reach 100 °C, more than "
     "the 5400 cal of latent heat available"],
    why="57.2 °C counts the latent heat but forgets the heat released as the condensed water cools from 100 °C. "
        "25.2 °C ignores the latent heat and treats the steam as water at 100 °C. 100 °C would need far more steam.",
    ncert="Class 11 Physics, 'Thermal Properties of Matter', calorimetry and change of state", seconds=100,
    recomputed=True)

T1k, T2k = 27 + 273, 327 + 273
ratio_E = (T2k / T1k) ** 4
assert close(ratio_E, 16.0) and close((327 / 27) ** 4, 2.15e4, 1e-2)
add(T, "Heat transfer", "Advanced", "numerical",
    "A black body emits radiant energy at the rate E when its temperature is 27 °C. When its temperature is raised to "
    "327 °C, it emits radiant energy at the rate:",
    place("16E", ["2E", "8E", "2.1 × 10⁴ E"], "A"),
    "Stefan–Boltzmann law",
    "The energy radiated per unit time by a black body is σAT⁴, where T is the absolute temperature. Celsius "
    "temperatures must be converted to kelvin first.",
    ["T₁ = 300 K, T₂ = 600 K", "E₂/E₁ = (600/300)⁴ = 2⁴ = 16 → 16E"],
    why="2E takes the emitted power proportional to T. 8E uses T³. 2.1 × 10⁴ E uses the Celsius temperatures, "
        "(327/27)⁴.",
    ncert="Class 11 Physics, 'Thermal Properties of Matter', radiation (Stefan–Boltzmann law)", seconds=45,
    recomputed=True)

H_ratio = (2 ** 2) / 2          # area ∝ r², rate ∝ A/L
assert H_ratio == 2
add(T, "Heat transfer", "Advanced", "numerical",
    "Heat flows at the rate H through a cylindrical rod whose ends are kept at two fixed temperatures; its sides are "
    "insulated. A second rod of the same material has twice the length and twice the radius. If its ends are kept "
    "at the same two temperatures, the rate of heat flow through it in the steady state is:",
    place("2H", ["H", "4H", "H/2"], "C"),
    "Steady-state conduction",
    "In the steady state the rate of heat flow is H = KA(T₁ − T₂)/L. The cross-sectional area A = πr² grows as the "
    "square of the radius.",
    ["A₂ = π(2r)² = 4A₁", "H₂/H₁ = (A₂/A₁)(L₁/L₂) = 4 × ½ = 2 → 2H"],
    why="H assumes doubling the radius and doubling the length cancel (they would only if H ∝ r/L). 4H ignores the "
        "longer length. H/2 makes H proportional to L/A.",
    ncert="Class 11 Physics, 'Thermal Properties of Matter', conduction", seconds=45, recomputed=True)

multi_key([True, True, False, True, False], "abd")
add(T, "Surface tension and capillarity", "Advanced", "multi_statement",
    multi("Which of the following statements about surface tension are correct?",
          ["Soaps and detergents lower the surface tension of water.",
           "The force of surface tension acts along (tangential to) the liquid surface.",
           "Surface tension is a force per unit area of the liquid surface.",
           "The excess pressure inside a soap bubble of radius r is twice the excess pressure inside a drop of the "
           "same soap solution of the same radius.",
           "A liquid rises in a capillary tube only if its angle of contact with the tube is obtuse."]),
    place("(a), (b) and (d) only", ["(a), (c) and (d) only", "(b), (d) and (e) only", "(a), (b), (d) and (e) only"],
          "D"),
    "Surface tension, excess pressure and capillarity",
    "Detergents reduce the surface tension of water, which is why they help it wet greasy cloth. Surface tension is "
    "a force per unit length acting in the surface. A soap bubble has two surfaces, so its excess pressure is 4S/r "
    "against 2S/r for a drop. Capillary rise h = 2S cos θ/(rρg) is positive only when θ is acute; for an obtuse "
    "angle (mercury in glass) the liquid is depressed.",
    ["(a) true", "(b) true", "(c) force per unit length, not per area → false",
     "(d) 4S/r = 2 × (2S/r) → true", "(e) rise needs cos θ > 0, i.e. an acute angle → false"],
    why="Codes containing (c) give surface tension the dimensions of pressure; codes containing (e) reverse the "
        "condition for capillary rise.",
    ncert="Class 11 Physics, 'Mechanical Properties of Fluids', surface tension", seconds=80)

multi_key([True, False, True, True, False], "acd")
add(T, "Elasticity and moduli", "Advanced", "multi_statement",
    multi("Which of the following statements about the elastic behaviour of solids are correct?",
          ["Steel is more elastic than copper, since its Young's modulus is larger.",
           "The Young's modulus of a wire depends on its length and its area of cross-section.",
           "Stress has the same dimensions as pressure.",
           "A material whose ultimate tensile strength and fracture point lie close together on its stress–strain "
           "curve is brittle.",
           "Strain is measured in N m⁻²."]),
    place("(a), (c) and (d) only", ["(a), (b) and (c) only", "(b), (c) and (e) only", "(c) and (d) only"], "B"),
    "Elastic moduli and the stress–strain curve",
    "A larger Young's modulus means a smaller strain for a given stress, which is what 'more elastic' means in "
    "physics; NCERT notes that steel is more elastic than copper, brass and aluminium. Young's modulus is a property "
    "of the material, not of the wire's dimensions. Stress is force per area, like pressure. Strain is a ratio of "
    "lengths and has no unit. A brittle material fractures soon after its ultimate strength is reached.",
    ["(a) Y_steel > Y_copper → steel more elastic → true",
     "(b) Y is a material constant → false", "(c) both [M L⁻¹ T⁻²] → true",
     "(d) ultimate strength and fracture close together → brittle → true",
     "(e) strain is dimensionless → false"],
    why="Codes with (b) confuse the modulus with the stiffness of a particular wire (YA/L); codes with (e) give "
        "strain the unit of stress. The code (c) and (d) only misses (a), the classic 'more elastic' trap.",
    ncert="Class 11 Physics, 'Mechanical Properties of Solids', elastic moduli and stress–strain curve", seconds=90)


# =====================================================================================================================
# Thermodynamics (B3 I4 A3)
# =====================================================================================================================
T = "Thermodynamics"

gam_b, R_b = 1.4, 8.3
Cv_b = R_b / (gam_b - 1)
assert close(Cv_b, 20.75) and close(gam_b * Cv_b, 29.05) and close(R_b / gam_b, 5.93) and close(R_b * (gam_b - 1), 3.32)
add(T, "Zeroth and first law", "Basic", "numerical",
    "For an ideal gas, the ratio of the molar specific heats is γ = C_p/C_v = 1.4. Taking R = 8.3 J mol⁻¹ K⁻¹, its "
    "molar specific heat at constant volume is:",
    place("20.75 J mol⁻¹ K⁻¹", ["29.05 J mol⁻¹ K⁻¹", "5.93 J mol⁻¹ K⁻¹", "3.32 J mol⁻¹ K⁻¹"], "C"),
    "Specific heats of an ideal gas: C_p − C_v = R and γ = C_p/C_v",
    "Put C_p = γC_v into C_p − C_v = R: C_v(γ − 1) = R, so C_v = R/(γ − 1).",
    ["C_v = R/(γ − 1) = 8.3/0.4", "= 20.75 J mol⁻¹ K⁻¹"],
    why="29.05 J mol⁻¹ K⁻¹ is C_p = γC_v, not C_v. 5.93 J mol⁻¹ K⁻¹ divides R by γ instead of by (γ − 1). "
        "3.32 J mol⁻¹ K⁻¹ multiplies R by (γ − 1) instead of dividing.",
    ncert="Class 11 Physics, 'Thermodynamics', specific heat capacity", seconds=30, recomputed=True)

add(T, "Zeroth and first law", "Basic", "direct",
    "Which of the following thermodynamic variables is an intensive variable?",
    place("Temperature", ["Volume", "Mass", "Internal energy"], "A"),
    "Extensive and intensive variables",
    "Imagine dividing a system in equilibrium into two equal halves. Variables that stay the same in each half "
    "(pressure, temperature, density) are intensive; variables that are halved (volume, mass, internal energy) are "
    "extensive.",
    ["Halve the system: temperature unchanged → intensive",
     "Volume, mass and internal energy are halved → extensive"],
    why="Volume, mass and internal energy all depend on the size of the system, so they are extensive.",
    ncert="Class 11 Physics, 'Thermodynamics', thermodynamic state variables and equation of state", seconds=25)

add(T, "Zeroth and first law", "Basic", "statement_pair",
    SP_STEM.format(
        s1="For one mole of an ideal gas, the difference of the molar specific heats is Cp − Cv = R.",
        s2="For an ideal gas, the molar specific heat at constant pressure is less than the molar specific heat at "
           "constant volume."),
    sp("C"),
    "Specific heat capacities of an ideal gas",
    "At constant volume all the heat supplied raises the internal energy. At constant pressure the gas also expands "
    "and does work, so more heat is needed for the same rise in temperature. The first law gives Cp − Cv = R "
    "(Mayer's relation).",
    ["Statement I: Cp − Cv = R → true", "Statement II: Cp = Cv + R > Cv → false"],
    why="Statement II reverses the inequality that Statement I itself implies.",
    ncert="Class 11 Physics, 'Thermodynamics', specific heat capacity", seconds=30)

V_r, P_a, P_b = 20e-3, 1.0e5, 1.5e5
Q_rigid = 2.5 * V_r * (P_b - P_a)               # diatomic: Q = nCvΔT = (5/2) V ΔP
assert close(Q_rigid, 2500.0) and close(1.5 * V_r * (P_b - P_a), 1500.0)
assert close(3.5 * V_r * (P_b - P_a), 3500.0) and close(V_r * (P_b - P_a), 1000.0)
add(T, "Zeroth and first law", "Intermediate", "numerical",
    "A diatomic ideal gas (rigid molecules, C_v = 5R/2) is enclosed in a rigid vessel of volume 20 L. Heat is "
    "supplied until its pressure rises from 1.0 × 10⁵ Pa to 1.5 × 10⁵ Pa. The heat supplied to the gas is:",
    place("2500 J", ["1500 J", "3500 J", "1000 J"], "D"),
    "First law at constant volume",
    "In a rigid vessel no work is done, so all the heat goes into internal energy: Q = nC_vΔT. From PV = nRT at "
    "constant V, nRΔT = VΔP, so Q = (C_v/R)VΔP = (5/2)VΔP.",
    ["nRΔT = VΔP = 20 × 10⁻³ × 0.5 × 10⁵ = 1000 J", "Q = (5/2) × 1000 = 2500 J"],
    why="1500 J uses C_v = 3R/2, the monatomic value. 3500 J uses C_p = 7R/2, but no expansion takes place. "
        "1000 J is only VΔP (= nRΔT), not the heat.",
    ncert="Class 11 Physics, 'Thermodynamics', first law of thermodynamics; specific heat capacity", seconds=60,
    recomputed=True)

n_g, R_g, dT_g = 2, 8.3, 40
Q_p = n_g * 2.5 * R_g * dT_g
assert close(Q_p, 1660.0) and close(n_g * 1.5 * R_g * dT_g, 996.0) and close(n_g * R_g * dT_g, 664.0)
assert close(n_g * 3.5 * R_g * dT_g, 2324.0)
add(T, "Zeroth and first law", "Intermediate", "numerical",
    "Two moles of a monatomic ideal gas are heated at constant pressure so that their temperature rises by 40 K. "
    "Taking R = 8.3 J mol⁻¹ K⁻¹, the heat supplied to the gas is:",
    place("1660 J", ["996 J", "664 J", "2324 J"], "B"),
    "Heat supplied at constant pressure",
    "At constant pressure Q = nCpΔT. For a monatomic ideal gas Cv = 3R/2 and Cp = Cv + R = 5R/2.",
    ["Q = 2 × (5/2) × 8.3 × 40 = 1660 J",
     "Of this, ΔU = nCvΔT = 996 J and W = nRΔT = 664 J (996 + 664 = 1660 ✓)"],
    why="996 J uses Cv (that is only the rise in internal energy). 664 J is only the work done. 2324 J uses Cp = 7R/2, "
        "the value for a diatomic gas.",
    ncert="Class 11 Physics, 'Thermodynamics', specific heat capacity; first law of thermodynamics", seconds=45,
    recomputed=True)

add(T, "Isothermal and adiabatic processes", "Intermediate", "match_list",
    match_stem("Match List-I (quantity, for n moles of an ideal gas) with List-II (expression). In A and C the "
               "volume changes from V₁ to V₂; in B and D the temperature changes from T₁ to T₂.",
               ["Work done by the gas in a reversible isothermal process at temperature T",
                "Work done by the gas in a reversible adiabatic process",
                "Work done by the gas in an isobaric process at pressure P",
                "Work done by the gas in an isochoric (constant-volume) process"],
               ["P(V₂ − V₁)", "Zero", "nRT ln(V₂/V₁)", "nR(T₁ − T₂)/(γ − 1)"]),
    match_options({"A": "III", "B": "IV", "C": "I", "D": "II"},
                  [{"A": "IV", "B": "III", "C": "I", "D": "II"}, {"A": "III", "B": "I", "C": "IV", "D": "II"},
                   {"A": "I", "B": "IV", "C": "III", "D": "II"}], "A"),
    "Work in standard processes",
    "Isothermal: W = ∫P dV with P = nRT/V gives nRT ln(V₂/V₁). Adiabatic: W = −ΔU = nCv(T₁ − T₂) = nR(T₁ − T₂)/(γ − 1). "
    "Isobaric: W = PΔV. Isochoric: dV = 0 throughout, so W = ∫P dV = 0 whatever the change in temperature.",
    ["Isothermal → III", "Adiabatic → IV", "Isobaric → I", "Isochoric → zero → II"],
    why="The other codes swap the isothermal and adiabatic expressions, or the isothermal and isobaric ones.",
    ncert="Class 11 Physics, 'Thermodynamics', thermodynamic processes", seconds=45)

add(T, "Isothermal and adiabatic processes", "Intermediate", "assertion_reason",
    AR_STEM.format(
        a="An ideal gas cools when it expands adiabatically.",
        r="In an adiabatic process the temperature of the system remains constant."),
    ar("C"),
    "Adiabatic expansion",
    "In an adiabatic process Q = 0, so ΔU = −W. When the gas expands it does positive work, so its internal energy "
    "and hence its temperature fall. A process at constant temperature is isothermal, not adiabatic.",
    ["A: Q = 0, W > 0 → ΔU < 0 → T falls → true",
     "R: constant temperature describes an isothermal process → false"],
    why="R describes the isothermal process; if R were true, A could not be.",
    ncert="Class 11 Physics, 'Thermodynamics', adiabatic process", seconds=35)

R_g, T_a, T_b = 8.3, 300.0, 600.0
Q_ab = 2.5 * R_g * (T_b - T_a)
Q_bc = 1.5 * R_g * (T_a - T_b)
assert close(Q_ab + Q_bc, 2490.0) and close(Q_ab, 6225.0) and close(-Q_bc, 3735.0)
assert close(R_g * (T_b - T_a), 2490.0)        # equals the work done, since the net ΔU is zero
add(T, "Zeroth and first law", "Advanced", "numerical",
    "One mole of a monatomic ideal gas at 300 K is heated at constant pressure until its temperature is 600 K. It is "
    "then cooled at constant volume until its temperature is again 300 K. Taking R = 8.3 J mol⁻¹ K⁻¹, the net heat "
    "absorbed by the gas in the two processes together is:",
    place("2490 J", ["6225 J", "3735 J", "0 J"], "B"),
    "First law over a process with no net temperature change",
    "The final temperature equals the initial one, so the net ΔU of the ideal gas is zero, and the net heat "
    "absorbed equals the net work done. Work is done only in the isobaric stage: W = PΔV = RΔT.",
    ["Isobaric: Q₁ = CpΔT = (5/2)(8.3)(300) = 6225 J",
     "Isochoric: Q₂ = CvΔT = (3/2)(8.3)(−300) = −3735 J",
     "Net Q = 6225 − 3735 = 2490 J = RΔT (the work done in the isobaric stage)"],
    why="6225 J counts only the isobaric heating. 3735 J is the heat released in the isochoric cooling. 0 J assumes "
        "the heat absorbed must be zero because the temperature returns to its starting value; that holds for ΔU, "
        "not for Q, since the gas has done work.",
    ncert="Class 11 Physics, 'Thermodynamics', first law of thermodynamics; thermodynamic processes", seconds=80,
    recomputed=True)

PA, VA, PB, VB = 2e5, 1e-3, 1e5, 3e-3
W_line = 0.5 * (PA + PB) * (VB - VA)
dU_line = 1.5 * (PB * VB - PA * VA)
assert close(W_line, 300.0) and close(dU_line, 150.0) and close(W_line + dU_line, 450.0)
assert close(PA * (VB - VA) + dU_line, 550.0)
add(T, "Zeroth and first law", "Advanced", "numerical",
    "A sample of a monatomic ideal gas is taken from state A (pressure 2 × 10⁵ Pa, volume 1 L) to state B (pressure "
    "1 × 10⁵ Pa, volume 3 L) along a path that is a straight line on the P–V diagram. The heat absorbed by the gas "
    "in this process is:",
    place("450 J", ["300 J", "150 J", "550 J"], "C"),
    "First law with work from the area under a P–V line",
    "The work done is the area under the straight line (a trapezium). For a monatomic ideal gas U = (3/2)nRT = "
    "(3/2)PV, so ΔU follows from the PV values at the two ends.",
    ["W = ½(2 × 10⁵ + 1 × 10⁵)(3 − 1) × 10⁻³ = 300 J",
     "ΔU = (3/2)(P_BV_B − P_AV_A) = 1.5 × (300 − 200) = 150 J",
     "Q = ΔU + W = 450 J"],
    why="300 J is only the work done. 150 J is only the rise in internal energy. 550 J takes the work as "
        "P_A(V_B − V_A) = 400 J, as if the pressure stayed at its initial value.",
    ncert="Class 11 Physics, 'Thermodynamics', first law of thermodynamics", seconds=100, recomputed=True)

multi_key([True, True, False, True, False], "abd")
add(T, "Isothermal and adiabatic processes", "Advanced", "multi_statement",
    multi("Which of the following statements about processes undergone by an ideal gas are correct?",
          ["A quasi-static process takes place so slowly that the system remains in equilibrium with its "
           "surroundings at every stage.",
           "Through any point of a P–V diagram, the adiabatic curve is steeper than the isothermal curve.",
           "When the gas expands at constant pressure, its temperature decreases.",
           "When the gas expands freely into a vacuum inside a rigid, thermally insulated container, its temperature "
           "does not change.",
           "The heat supplied to the gas in any process is equal to the increase in its internal energy."]),
    place("(a), (b) and (d) only", ["(a), (b), (c) and (d) only", "(b), (d) and (e) only", "(a), (c) and (e) only"],
          "B"),
    "Thermodynamic processes of an ideal gas",
    "Quasi-static means infinitely slow, so equilibrium is maintained. Along an adiabatic curve PV^γ = constant, so "
    "its slope −γP/V is γ times the isothermal slope −P/V. At constant P, V ∝ T, so expansion raises the temperature. "
    "In free expansion Q = 0 and W = 0, so ΔU = 0, and for an ideal gas the temperature is unchanged. In general "
    "Q = ΔU + W, which equals ΔU only when W = 0.",
    ["(a) true", "(b) slope ratio γ > 1 → true", "(c) V ∝ T at constant P → T rises → false",
     "(d) Q = W = 0 → ΔU = 0 → T unchanged → true", "(e) Q = ΔU only if W = 0 → false"],
    why="Codes containing (c) reverse Charles's law; codes containing (e) forget the work term in the first law.",
    ncert="Class 11 Physics, 'Thermodynamics', quasi-static, isothermal and adiabatic processes", seconds=90)

# =====================================================================================================================
# Kinetic Theory of Gases (B2 I3 A2)
# =====================================================================================================================
T = "Kinetic Theory of Gases"

n_mol = 1.0e5 * 8.3e-3 / (8.3 * 200)
assert close(n_mol, 0.5) and close(1.0e5 * 8.3 / (8.3 * 200), 500.0)
add(T, "Ideal gas equation", "Basic", "numerical",
    "An ideal gas occupies 8.3 L at a pressure of 1.0 × 10⁵ Pa and a temperature of 200 K. Taking "
    "R = 8.3 J mol⁻¹ K⁻¹, the number of moles of the gas is:",
    place("0.5", ["2", "500", "0.05"], "D"),
    "Ideal gas equation PV = nRT",
    "Solve PV = nRT for n, with the volume in cubic metres (1 L = 10⁻³ m³).",
    ["V = 8.3 × 10⁻³ m³", "n = PV/RT = (1.0 × 10⁵ × 8.3 × 10⁻³)/(8.3 × 200) = 830/1660 = 0.5"],
    why="2 inverts the expression. 500 leaves the volume in litres. 0.05 slips a power of ten.",
    ncert="Class 11 Physics, 'Kinetic Theory', behaviour of gases", seconds=35, recomputed=True)

add(T, "Degrees of freedom and equipartition", "Basic", "direct",
    "According to the law of equipartition of energy, for a gas in thermal equilibrium at absolute temperature T, "
    "the average energy associated with each quadratic term (degree of freedom) in the energy of a molecule is "
    "(k_B is Boltzmann's constant):",
    place("½k_BT", ["k_BT", "(3/2)k_BT", "2k_BT"], "B"),
    "Law of equipartition of energy",
    "Each degree of freedom (each squared term in the expression for the energy of a molecule) has an average energy "
    "½k_BT. The three translational degrees together give (3/2)k_BT.",
    ["Energy per quadratic term = ½k_BT", "Three translational terms → (3/2)k_BT"],
    why="(3/2)k_BT is the average translational energy (three terms). k_BT is the energy of a vibrational mode, "
        "which has two quadratic terms (kinetic and potential). 2k_BT has no basis.",
    ncert="Class 11 Physics, 'Kinetic Theory', law of equipartition of energy", seconds=25)

kB = 1.38e-23
KE_avg = 1.5 * kB * 300
assert close(KE_avg, 6.21e-21) and close(1.5 * kB * 27, 5.59e-22, 1e-2) and close(kB * 300, 4.14e-21)
assert close(2.5 * kB * 300, 1.035e-20)
add(T, "Pressure and rms speed", "Intermediate", "numerical",
    "Taking Boltzmann's constant as 1.38 × 10⁻²³ J K⁻¹, the average translational kinetic energy of a molecule of an "
    "ideal gas at 27 °C is:",
    place("6.21 × 10⁻²¹ J", ["5.59 × 10⁻²² J", "4.14 × 10⁻²¹ J", "1.04 × 10⁻²⁰ J"], "A"),
    "Average translational kinetic energy of a molecule",
    "The average translational kinetic energy of a molecule depends only on the absolute temperature: "
    "(3/2)k_BT, whatever the gas.",
    ["T = 27 + 273 = 300 K", "E = 1.5 × 1.38 × 10⁻²³ × 300 = 6.21 × 10⁻²¹ J"],
    why="5.59 × 10⁻²² J uses 27 instead of 300 K. 4.14 × 10⁻²¹ J is k_BT, missing the factor 3/2. 1.04 × 10⁻²⁰ J "
        "uses (5/2)k_BT, which includes rotation and is not the translational energy.",
    ncert="Class 11 Physics, 'Kinetic Theory', kinetic interpretation of temperature", seconds=40, recomputed=True)

U_d = 2 * 2.5 * 8.3 * 300
assert close(U_d, 12450.0) and close(2 * 1.5 * 8.3 * 300, 7470.0) and close(2 * 3.5 * 8.3 * 300, 17430.0)
add(T, "Degrees of freedom and equipartition", "Intermediate", "numerical",
    "Two moles of an ideal diatomic gas whose molecules are rigid (no vibration) are at 300 K. Taking "
    "R = 8.3 J mol⁻¹ K⁻¹, the total internal energy of the gas is:",
    place("12 450 J", ["7470 J", "17 430 J", "6225 J"], "C"),
    "Internal energy from equipartition",
    "A rigid diatomic molecule has 3 translational and 2 rotational degrees of freedom, each with ½k_BT on average, "
    "so U = (5/2)nRT for n moles.",
    ["U = (5/2) × 2 × 8.3 × 300 = 12 450 J"],
    why="7470 J counts only the three translational degrees of freedom. 17 430 J uses 7/2, including vibration that "
        "is absent in a rigid molecule. 6225 J is the answer for one mole.",
    ncert="Class 11 Physics, 'Kinetic Theory', law of equipartition of energy; specific heat capacity", seconds=45,
    recomputed=True)

add(T, "Ideal gas equation", "Intermediate", "statement_pair",
    SP_STEM.format(
        s1="In the kinetic theory of an ideal gas, the collisions of the molecules with one another and with the "
           "walls of the container are assumed to be inelastic.",
        s2="In an ideal gas, the molecules themselves occupy a large fraction of the volume of the container."),
    sp("B"),
    "Assumptions of the kinetic theory",
    "Kinetic theory treats the molecules as tiny particles whose own volume is negligible compared with the volume "
    "of the container, which move randomly and collide elastically (so the kinetic energy of the molecules is not "
    "lost in collisions), with no forces between them except during collisions.",
    ["Statement I: collisions are taken as elastic → false",
     "Statement II: molecular volume is taken as negligible → false"],
    why="Both statements reverse the actual assumptions of the kinetic theory.",
    ncert="Class 11 Physics, 'Kinetic Theory', kinetic theory of an ideal gas", seconds=35)

add(T, "Ideal gas equation", "Advanced", "assertion_reason",
    AR_STEM.format(
        a="Equal volumes of all ideal gases at the same temperature and pressure contain equal numbers of "
          "molecules.",
        r="For an ideal gas PV = Nk_BT, where N is the number of molecules and k_B is a constant that is the same "
          "for all gases."),
    ar("A"),
    "Avogadro's hypothesis from the ideal gas law",
    "Rearranging, N = PV/(k_BT). If P, V and T are the same for two gases, N must also be the same, because k_B is a "
    "universal constant independent of the nature of the gas.",
    ["N = PV/(k_BT) → same P, V, T → same N"],
    why="R directly yields A, so both are true and R explains A.",
    ncert="Class 11 Physics, 'Kinetic Theory', behaviour of gases (Avogadro's hypothesis)", seconds=40)

add(T, "Pressure and rms speed", "Advanced", "match_list",
    match_stem("For an ideal gas at absolute temperature T, with n molecules per unit volume, each of mass m and "
               "diameter d, and molar mass M, match List-I (quantity) with List-II (expression).",
               ["Pressure of the gas", "Average translational kinetic energy of a molecule",
                "Root mean square speed of the molecules", "Mean free path of a molecule"],
               ["1/(√2 π n d²)", "√(3RT/M)", "(1/3) n m ⟨v²⟩", "(3/2) k_BT"]),
    match_options({"A": "III", "B": "IV", "C": "II", "D": "I"},
                  [{"A": "IV", "B": "III", "C": "II", "D": "I"}, {"A": "III", "B": "IV", "C": "I", "D": "II"},
                   {"A": "III", "B": "II", "C": "IV", "D": "I"}], "D"),
    "Results of the kinetic theory",
    "P = (1/3)nm⟨v²⟩; average translational KE = ½m⟨v²⟩ = (3/2)k_BT; v_rms = √(3k_BT/m) = √(3RT/M); "
    "mean free path l = 1/(√2 π n d²).",
    ["Pressure → III", "Translational KE → IV", "v_rms → II", "Mean free path → I"],
    why="The other codes swap the pressure with the kinetic energy expression, or the rms speed with the mean free "
        "path.",
    ncert="Class 11 Physics, 'Kinetic Theory', pressure of an ideal gas; mean free path", seconds=45)


# =====================================================================================================================
# Oscillations and Waves (B4 I6 A4)
# =====================================================================================================================
T = "Oscillations and Waves"

A_s, w_s = 0.05, 4.0
assert close(w_s ** 2 * A_s, 0.8) and close(w_s * A_s, 0.2) and close(w_s ** 2 * 5, 80.0)
add(T, "SHM equation and phase", "Basic", "numerical",
    "A particle executes simple harmonic motion with an amplitude of 5 cm and an angular frequency of 4 rad/s. The "
    "maximum magnitude of its acceleration is:",
    place("0.8 m/s²", ["0.2 m/s²", "80 m/s²", "0.4 m/s²"], "A"),
    "Acceleration in SHM",
    "In SHM a = −ω²x, so the acceleration is greatest at the extreme positions, where |x| = A: a_max = ω²A.",
    ["a_max = ω²A = 4² × 0.05 = 0.8 m/s²"],
    why="0.2 m/s² is ωA, which is the maximum speed (in m/s), not the acceleration. 80 m/s² leaves the amplitude in "
        "centimetres. 0.4 m/s² halves the correct value.",
    ncert="Class 11 Physics, 'Oscillations', velocity and acceleration in simple harmonic motion", seconds=30,
    recomputed=True)

L_p, g = 2.5, 10.0
T_p = 2 * math.pi * math.sqrt(L_p / g)
assert close(T_p, math.pi) and close(2 * math.pi * math.sqrt(g / L_p), 4 * math.pi)
add(T, "Spring and pendulum oscillations", "Basic", "numerical",
    "A simple pendulum has a length of 2.5 m. Taking g = 10 m/s², the period of its small oscillations is:",
    place("π s", ["4π s", "π/2 s", "0.5 s"], "C"),
    "Period of a simple pendulum",
    "For small oscillations, T = 2π√(L/g).",
    ["L/g = 2.5/10 = 0.25 s² → √(L/g) = 0.5 s", "T = 2π × 0.5 = π s ≈ 3.14 s"],
    why="4π s inverts the ratio, using √(g/L). π/2 s uses π√(L/g). 0.5 s is √(L/g) alone, without the 2π.",
    ncert="Class 11 Physics, 'Oscillations', the simple pendulum", seconds=30, recomputed=True)

lam = 340 / 500
assert close(lam, 0.68) and close(lam / 2, 0.34) and close(500 / 340, 1.47, 1e-2)
add(T, "Progressive waves and wave speed", "Basic", "numerical",
    "A sound wave of frequency 500 Hz travels through air at 340 m/s. The distance between two consecutive "
    "compressions is:",
    place("0.68 m", ["0.34 m", "1.47 m", "1.36 m"], "B"),
    "Wavelength of a longitudinal wave",
    "Consecutive compressions are one wavelength apart, and λ = v/f.",
    ["λ = 340/500 = 0.68 m"],
    why="0.34 m is λ/2, the distance from a compression to the next rarefaction. 1.47 m is f/v (wrong way up, wrong "
        "unit). 1.36 m is 2λ.",
    ncert="Class 11 Physics, 'Waves', speed of a travelling wave", seconds=25, recomputed=True)

add(T, "Superposition and standing waves", "Basic", "direct",
    "In a stationary (standing) wave on a stretched string, all the particles of the string between two adjacent "
    "nodes oscillate:",
    place("In the same phase as one another",
          ["In opposite phase to one another",
           "With a phase that changes steadily from particle to particle, as in a travelling wave",
           "With a phase difference of π/2 between neighbouring particles"], "D"),
    "Phase in a stationary wave",
    "A stationary wave is y = 2a sin kx cos ωt. Between two adjacent nodes sin kx has a single sign, so every "
    "particle there moves as (constant amplitude) × cos ωt — all in step. Particles on opposite sides of a node are "
    "in opposite phase.",
    ["y = [2a sin kx] cos ωt: the time factor cos ωt is common to all particles",
     "Between adjacent nodes sin kx keeps one sign → same phase",
     "Across a node sin kx changes sign → phase difference π"],
    why="Opposite phase is true only for particles on opposite sides of a node. A steadily changing phase belongs "
        "to a travelling wave. A π/2 difference has no basis here.",
    ncert="Class 11 Physics, 'Waves', standing waves and normal modes", seconds=35)

w_e, phi_e, A_e = 5 * math.pi, math.pi / 6, 0.04
assert close(2 * math.pi / w_e, 0.4) and close(A_e * math.sin(phi_e), 0.02)
assert close(A_e * math.cos(phi_e), 0.02 * math.sqrt(3))
add(T, "SHM equation and phase", "Intermediate", "numerical",
    "The displacement of a particle in simple harmonic motion is x = 0.04 sin(5πt + π/6), where x is in metres and t "
    "in seconds. The period of the motion and the displacement of the particle at t = 0 are:",
    place("0.4 s and 2 cm", ["0.4 s and 4 cm", "2.5 s and 2 cm", "0.4 s and 2√3 cm"], "A"),
    "Reading an SHM equation",
    "Compare with x = A sin(ωt + φ): the period is 2π/ω, and at t = 0 the displacement is A sin φ (the initial "
    "phase decides it).",
    ["ω = 5π rad/s → T = 2π/5π = 0.4 s", "x(0) = 0.04 sin(π/6) = 0.04 × ½ = 0.02 m = 2 cm"],
    why="4 cm is the amplitude, reached only when the phase is π/2. 2.5 s is the frequency 2.5 Hz mistaken for the "
        "period. 2√3 cm uses cos(π/6) instead of sin(π/6).",
    ncert="Class 11 Physics, 'Oscillations', simple harmonic motion", seconds=40, recomputed=True)

m_x = F(3, 2) / (F(9, 4) - 1)
assert m_x == F(6, 5)
assert F(3, 2) / (F(3, 2) - 1) == 3            # wrong: T ∝ m
add(T, "Spring and pendulum oscillations", "Intermediate", "numerical",
    "A block of unknown mass m attached to a light spring oscillates with a period of 2 s. When an extra mass of "
    "1.5 kg is fixed to the block, the period becomes 3 s. The value of m is:",
    place("1.2 kg", ["3.0 kg", "2.7 kg", "1.5 kg"], "D"),
    "Period of a spring–mass system",
    "T = 2π√(m/k), so for the same spring T² ∝ m. Compare the two cases.",
    ["(3/2)² = (m + 1.5)/m → 9m = 4m + 6", "m = 6/5 = 1.2 kg"],
    why="3.0 kg takes T ∝ m. 2.7 kg is the total mass m + 1.5 in the second case. 1.5 kg assumes the unknown mass "
        "equals the added mass.",
    ncert="Class 11 Physics, 'Oscillations', oscillations due to a spring", seconds=55, recomputed=True)

v_newton, gamma = 300.0, 1.44
v_lap = v_newton * math.sqrt(gamma)
assert close(v_lap, 360.0) and close(v_newton * gamma, 432.0)
add(T, "Progressive waves and wave speed", "Intermediate", "numerical",
    "Newton's formula v = √(P/ρ), which assumes isothermal compressions, gives a speed of 300 m/s for sound in a "
    "certain gas. If the ratio of specific heats of the gas is 1.44, the speed of sound given by Laplace's corrected "
    "formula is:",
    place("360 m/s", ["432 m/s", "250 m/s", "300 m/s"], "C"),
    "Laplace correction",
    "Compressions and rarefactions in sound are too fast for heat to flow, so they are adiabatic. The adiabatic bulk "
    "modulus is γP instead of P, so v = √(γP/ρ) = √γ × (Newton's value).",
    ["v_Laplace = √1.44 × 300 = 1.2 × 300 = 360 m/s"],
    why="432 m/s multiplies by γ instead of √γ. 250 m/s divides by √γ. 300 m/s ignores the correction.",
    ncert="Class 11 Physics, 'Waves', speed of a longitudinal wave (Laplace correction)", seconds=40, recomputed=True)

add(T, "Progressive waves and wave speed", "Intermediate", "match_list",
    match_stem("Match List-I (type of wave) with List-II (expression for its speed). T is the tension, μ the mass per "
               "unit length, B the bulk modulus, Y the Young's modulus, ρ the density, P the pressure and γ the ratio "
               "of specific heats.",
               ["Transverse wave on a stretched string", "Longitudinal wave in a liquid",
                "Longitudinal wave along a thin solid rod", "Sound in an ideal gas (Laplace's formula)"],
               ["√(Y/ρ)", "√(γP/ρ)", "√(T/μ)", "√(B/ρ)"]),
    match_options({"A": "III", "B": "IV", "C": "I", "D": "II"},
                  [{"A": "III", "B": "I", "C": "IV", "D": "II"}, {"A": "III", "B": "IV", "C": "II", "D": "I"},
                   {"A": "IV", "B": "III", "C": "I", "D": "II"}], "B"),
    "Speed of mechanical waves",
    "Wave speed = √(restoring-force property/inertia property). On a string: tension and mass per length. In a "
    "fluid: bulk modulus and density. Along a thin rod: Young's modulus and density. In an ideal gas the adiabatic "
    "bulk modulus is γP.",
    ["String → √(T/μ) (III)", "Liquid → √(B/ρ) (IV)", "Thin rod → √(Y/ρ) (I)", "Gas → √(γP/ρ) (II)"],
    why="The other codes use the bulk modulus for a thin rod or Young's modulus for a liquid; a liquid has no "
        "Young's modulus.",
    ncert="Class 11 Physics, 'Waves', speed of a travelling wave", seconds=40)

add(T, "Superposition and standing waves", "Intermediate", "assertion_reason",
    AR_STEM.format(
        a="When a guitar string is tightened, keeping its vibrating length unchanged, the note it gives rises in "
          "pitch (frequency).",
        r="The speed of transverse waves on a string increases with its tension, and for a fixed length the "
          "frequencies of the string's normal modes are proportional to this speed."),
    ar("A"),
    "Normal modes of a stretched string",
    "For a string fixed at both ends the normal-mode frequencies are fₙ = nv/(2L), with v = √(T/μ). Raising the "
    "tension raises v and therefore every fₙ, including the fundamental that sets the pitch.",
    ["v = √(T/μ) increases with T", "f₁ = v/2L ∝ v for fixed L → pitch rises"],
    why="R gives the complete chain of reasoning for A, so R is the correct explanation.",
    ncert="Class 11 Physics, 'Waves', standing waves and normal modes", seconds=40)

add(T, "Superposition and standing waves", "Intermediate", "statement_pair",
    SP_STEM.format(
        s1="A stationary wave transports energy along the string from one end to the other.",
        s2="If a stationary wave is formed by two waves each of amplitude a, the displacement at an antinode varies "
           "between +2a and −2a."),
    sp("D"),
    "Energy and amplitude in a stationary wave",
    "A stationary wave is the sum of two equal waves travelling in opposite directions; their energy flows cancel, "
    "so there is no net transport of energy (the nodes never move). At an antinode the two waves always arrive in "
    "phase, so the amplitude there is 2a.",
    ["Statement I: no net energy flow (energy stays trapped between nodes) → false",
     "Statement II: y = 2a sin kx cos ωt → amplitude 2a at antinodes → true"],
    why="Statement I would be true for a travelling wave, not for a stationary one.",
    ncert="Class 11 Physics, 'Waves', standing waves and normal modes", seconds=40)

w2 = (16 ** 2 - 12 ** 2) / (4 ** 2 - 3 ** 2)
A_amp = math.sqrt(3 ** 2 + 16 ** 2 / w2)
assert close(w2, 16.0) and close(A_amp, 5.0) and close(2 * math.pi / math.sqrt(w2), math.pi / 2)
assert close(math.sqrt(12 ** 2 / w2 + 4 ** 2), 5.0)
add(T, "Energy in SHM", "Advanced", "numerical",
    "A particle executing simple harmonic motion has a speed of 16 cm/s when its displacement from the mean position "
    "is 3 cm, and a speed of 12 cm/s when its displacement is 4 cm. Its amplitude and period are:",
    place("5 cm and π/2 s", ["5 cm and π/8 s", "√7 cm and π/2 s", "5 cm and 0.25 s"], "C"),
    "Speed–displacement relation in SHM",
    "In SHM v² = ω²(A² − x²). Two (x, v) pairs give two equations; subtracting them eliminates A and gives ω.",
    ["256 = ω²(A² − 9) and 144 = ω²(A² − 16)", "Subtract: 112 = 7ω² → ω = 4 rad/s",
     "A² − 9 = 256/16 = 16 → A = 5 cm", "T = 2π/ω = π/2 s ≈ 1.57 s"],
    why="π/8 s uses 2π/ω² instead of 2π/ω. √7 cm comes from subtracting the two squared displacements (16 − 9). "
        "0.25 s takes 4 as the frequency in hertz instead of the angular frequency.",
    shortcut="ω² = (v₁² − v₂²)/(x₂² − x₁²) = (256 − 144)/(16 − 9) = 16.",
    ncert="Class 11 Physics, 'Oscillations', velocity and acceleration in simple harmonic motion", seconds=90,
    recomputed=True)

k_sw, w_sw = 2 * math.pi / 3, 120 * math.pi
v_sw = w_sw / k_sw
lam_sw = 2 * math.pi / k_sw
assert close(v_sw, 180.0) and close(lam_sw, 3.0) and close(lam_sw / 2 * 60, 90.0)
add(T, "Superposition and standing waves", "Advanced", "numerical",
    "A stationary wave on a string is described by y = 0.06 sin(2πx/3) cos(120πt), where x and y are in metres and t "
    "in seconds. The speed of the two travelling waves whose superposition gives this stationary wave is:",
    place("180 m/s", ["90 m/s", "360 m/s", "3 m/s"], "A"),
    "Decomposing a stationary wave",
    "y = 2a sin kx cos ωt is the superposition of a sin(kx − ωt) and a sin(kx + ωt), each travelling at v = ω/k. "
    "Read off k and ω from the equation.",
    ["k = 2π/3 m⁻¹ → λ = 3 m; ω = 120π rad/s → f = 60 Hz", "v = ω/k = fλ = 60 × 3 = 180 m/s"],
    why="90 m/s multiplies the frequency by the node spacing (λ/2) instead of λ. 360 m/s doubles the speed. 3 m/s "
        "is the wavelength in metres, not a speed.",
    ncert="Class 11 Physics, 'Waves', standing waves and normal modes", seconds=60, recomputed=True)

add(T, "Spring and pendulum oscillations", "Advanced", "assertion_reason",
    AR_STEM.format(
        a="The period of small oscillations of a simple pendulum of fixed length is larger on the surface of the "
          "Moon than on the surface of the Earth.",
        r="For small oscillations, the period of a simple pendulum does not depend on the amplitude of "
          "oscillation."),
    ar("B"),
    "Dependence of a pendulum's period on g",
    "T = 2π√(L/g). The Moon's surface gravity is much smaller than the Earth's, so the period is larger there. R is "
    "a separate, true property (isochronism of small oscillations) and says nothing about g.",
    ["A: g_Moon < g_Earth → T = 2π√(L/g) larger → true",
     "R: T is independent of amplitude for small oscillations → true",
     "R does not involve g, so it does not explain A"],
    why="R is true but concerns the amplitude, while A depends on the change in g; hence 'R is not the correct "
        "explanation'.",
    ncert="Class 11 Physics, 'Oscillations', the simple pendulum", seconds=45)

multi_key([True, True, True, False, False], "abc")
add(T, "Progressive waves and wave speed", "Advanced", "multi_statement",
    multi("A transverse wave on a string is described by y = A sin(kx − ωt), where A, k and ω are positive constants. "
          "Which of the following statements are correct?",
          ["The wave travels in the positive x-direction.",
           "The speed of the wave is ω/k.",
           "At a given instant, the phase difference between two points of the string a distance Δx apart along it "
           "is kΔx.",
           "The speed of the wave increases if its amplitude A is increased.",
           "If ω is doubled with k unchanged, the wavelength doubles."]),
    place("(a), (b) and (c) only", ["(a), (b), (c) and (d) only", "(b), (c) and (e) only", "(a), (d) and (e) only"],
          "D"),
    "Reading a travelling-wave equation",
    "A phase of the form (kx − ωt) stays constant when x increases with t, so the wave moves towards +x at "
    "dx/dt = ω/k. At a fixed t, the phase changes by kΔx over a distance Δx. The amplitude does not enter the wave "
    "speed. The wavelength λ = 2π/k depends only on k.",
    ["(a) kx − ωt = constant → x increases with t → true", "(b) v = ω/k → true", "(c) Δφ = kΔx → true",
     "(d) v is independent of A → false", "(e) λ = 2π/k is unchanged (the speed doubles instead) → false"],
    why="Codes containing (d) think a bigger wave travels faster; codes containing (e) tie the wavelength to ω "
        "rather than to k.",
    ncert="Class 11 Physics, 'Waves', displacement relation in a progressive wave", seconds=80)


# =====================================================================================================================
# Electrostatics (B6 I8 A6)
# =====================================================================================================================
T = "Electrostatics"
k = 9e9

E_pt = k * 2e-9 / 0.3 ** 2
assert close(E_pt, 200.0) and close(k * 2e-9 / 0.3, 60.0) and close(k * 2e-9 / 0.03 ** 2, 2e4) and close(k * 2e-9, 18)
add(T, "Electric field and dipole", "Basic", "numerical",
    "Taking 1/(4πε₀) = 9 × 10⁹ N m² C⁻², the magnitude of the electric field at a distance of 30 cm from a point "
    "charge of 2 nC in air is:",
    place("200 N/C", ["60 N/C", "2.0 × 10⁴ N/C", "18 N/C"], "B"),
    "Field of a point charge",
    "E = kq/r², with r in metres and q in coulombs.",
    ["E = 9 × 10⁹ × 2 × 10⁻⁹ / (0.3)² = 18/0.09 = 200 N/C"],
    why="60 N/C divides by r instead of r² (that would be a potential in volts). 2.0 × 10⁴ N/C takes 30 cm as 0.03 m. "
        "18 N/C forgets to divide by r².",
    ncert="Class 12 Physics, 'Electric Charges and Fields', electric field", seconds=30, recomputed=True)

U_c = 0.5 * 10e-6 * 20 ** 2
assert close(U_c, 2e-3) and close(10e-6 * 20 ** 2, 4e-3) and close(10e-6 * 20, 2e-4) and close(0.5 * 10e-6 * 20, 1e-4)
add(T, "Capacitors and dielectrics", "Basic", "numerical",
    "A 10 μF capacitor is charged to a potential difference of 20 V. The energy stored in it is:",
    place("2 mJ", ["4 mJ", "0.2 mJ", "0.1 mJ"], "D"),
    "Energy stored in a capacitor",
    "U = ½CV² (equivalently Q²/2C or ½QV).",
    ["U = ½ × 10 × 10⁻⁶ × 20² = 2 × 10⁻³ J = 2 mJ"],
    why="4 mJ drops the factor ½. 0.2 mJ is the charge CV = 200 μC read as energy. 0.1 mJ uses ½CV without squaring "
        "V.",
    ncert="Class 12 Physics, 'Electrostatic Potential and Capacitance', energy stored in a capacitor", seconds=25,
    recomputed=True)

e = 1.6e-19
ratios = {q: q / e for q in (3.2e-19, 2.4e-19, 4.8e-19, -1.6e-18)}
assert [q for q, n in ratios.items() if abs(n - round(n)) > 1e-6] == [2.4e-19]
add(T, "Coulomb's law and superposition", "Basic", "direct",
    "Taking the magnitude of the electronic charge as e = 1.6 × 10⁻¹⁹ C, which of the following CANNOT be the net "
    "charge on an isolated body?",
    place("2.4 × 10⁻¹⁹ C", ["3.2 × 10⁻¹⁹ C", "4.8 × 10⁻¹⁹ C", "−1.6 × 10⁻¹⁸ C"], "B"),
    "Quantisation of charge",
    "The charge on any body is an integral multiple of e: q = ne, with n = 0, ±1, ±2, ... A body gains or loses "
    "whole electrons only.",
    ["3.2 × 10⁻¹⁹ = 2e ✓", "2.4 × 10⁻¹⁹ = 1.5e ✗ (not an integer multiple)", "4.8 × 10⁻¹⁹ = 3e ✓",
     "−1.6 × 10⁻¹⁸ = −10e ✓"],
    why="3.2 × 10⁻¹⁹ C, 4.8 × 10⁻¹⁹ C and −1.6 × 10⁻¹⁸ C are 2e, 3e and −10e; a negative sign only means excess "
        "electrons.",
    ncert="Class 12 Physics, 'Electric Charges and Fields', basic properties of electric charge (quantisation)",
    seconds=30)

add(T, "Gauss's law", "Basic", "direct",
    "Under electrostatic conditions, an excess charge placed on an isolated solid metal conductor resides:",
    place("Only on its outer surface", ["Uniformly throughout its volume", "At its geometric centre",
                                        "Partly on its surface and partly in its interior"], "A"),
    "Electrostatics of conductors",
    "In electrostatics the field inside the material of a conductor is zero. By Gauss's law, any closed surface "
    "drawn just inside the conductor encloses zero net charge, so no net charge can be in the interior; the excess "
    "charge must sit on the surface.",
    ["E = 0 inside the conductor → flux through any interior Gaussian surface = 0",
     "Gauss's law → enclosed charge = 0 → excess charge only on the surface"],
    why="A charge in the interior would produce a field inside the conductor, driving the free electrons until it "
        "vanished, so none of the other distributions is stable.",
    ncert="Class 12 Physics, 'Electrostatic Potential and Capacitance', electrostatics of conductors", seconds=30)

add(T, "Electric field and dipole", "Basic", "assertion_reason",
    AR_STEM.format(
        a="Two electric field lines never cross each other.",
        r="Electric field lines are always straight lines."),
    ar("C"),
    "Properties of electric field lines",
    "At a crossing point the field would have two directions, which is impossible since the field at a point has a "
    "single direction. Field lines are in general curved (for example those of a dipole); they are straight only in "
    "special cases such as a single point charge or a uniform field.",
    ["A: a unique field direction at each point → lines cannot cross → true",
     "R: lines of a dipole are curved → false"],
    why="R is false; the real reason for A is that the field has a unique direction at every point.",
    ncert="Class 12 Physics, 'Electric Charges and Fields', electric field lines", seconds=30)

add(T, "Electric potential and energy", "Basic", "statement_pair",
    SP_STEM.format(
        s1="The electrostatic potential energy of a system of two like point charges increases when they are brought "
           "closer together.",
        s2="The electrostatic force is a conservative force."),
    sp("A"),
    "Potential energy of a pair of charges",
    "U = kq₁q₂/r is positive for like charges and grows as r decreases: work must be done against their repulsion "
    "to push them together. The electrostatic force, like gravity, is conservative, which is why a potential energy "
    "can be defined for it.",
    ["Statement I: q₁q₂ > 0, r smaller → U larger → true",
     "Statement II: work done by the electrostatic force is path-independent → true"],
    why="Both statements are true.",
    ncert="Class 12 Physics, 'Electrostatic Potential and Capacitance', potential energy of a system of charges",
    seconds=30)

q1_, q2_ = 6.0, -2.0
q_each = (q1_ + q2_) / 2
assert close(q_each, 2.0) and close((q_each * q_each) / abs(q1_ * q2_), 1 / 3)
assert close((4 * 4) / abs(q1_ * q2_), 4 / 3)
add(T, "Coulomb's law and superposition", "Intermediate", "numerical",
    "Two identical small metal spheres carry charges of +6 μC and −2 μC and attract each other with a force F when "
    "placed a certain distance apart. They are touched together and then put back at the same separation. The force "
    "between them now is:",
    place("F/3, repulsive", ["F/3, attractive", "4F/3, repulsive", "Zero"], "C"),
    "Charge sharing and Coulomb's law",
    "Identical conducting spheres in contact share the total charge equally. The new force is found by comparing "
    "the products of the charges, the distance being the same.",
    ["Total charge = +6 − 2 = +4 μC → each sphere +2 μC",
     "F'/F = (2 × 2)/(6 × 2) = 1/3", "Both charges positive → repulsive"],
    why="F/3 attractive gets the size right but forgets that both spheres are now positive. 4F/3 repulsive shares the "
        "sum of the magnitudes (8 μC) instead of the algebraic sum. Zero assumes the charges cancel completely.",
    ncert="Class 12 Physics, 'Electric Charges and Fields', Coulomb's law", seconds=50, recomputed=True)

p_d, r_d = 4e-10, 0.3
V_ax = k * p_d / r_d ** 2
assert close(V_ax, 40.0) and close(k * p_d / r_d ** 3, 133.3, 1e-3)
add(T, "Electric potential and energy", "Intermediate", "numerical",
    "A short electric dipole has a dipole moment of 4 × 10⁻¹⁰ C m. Taking 1/(4πε₀) = 9 × 10⁹ N m² C⁻², the electric "
    "potential at a point on its axis, 30 cm from its centre, is:",
    place("40 V", ["0 V", "80 V", "133 V"], "A"),
    "Potential of a short dipole",
    "For a short dipole V = kp cos θ/r², where θ is measured from the dipole axis. On the axis cos θ = 1.",
    ["V = 9 × 10⁹ × 4 × 10⁻¹⁰ / (0.3)² = 3.6/0.09 = 40 V"],
    why="0 V is the potential on the equatorial line. 80 V uses 2kp/r², mixing in the factor 2 of the axial field. "
        "133 V uses kp/r³, the form of a dipole field, not the potential.",
    ncert="Class 12 Physics, 'Electrostatic Potential and Capacitance', potential due to an electric dipole",
    seconds=45, recomputed=True)

lam_l, r_l = 1e-7, 0.1
E_line = 2 * k * lam_l / r_l
assert close(E_line, 1.8e4) and close(k * lam_l / r_l, 9e3) and close(2 * k * lam_l / r_l ** 2, 1.8e5)
add(T, "Gauss's law", "Intermediate", "numerical",
    "A very long straight wire carries a uniform linear charge density of 0.1 μC/m. Taking 1/(4πε₀) = "
    "9 × 10⁹ N m² C⁻², the magnitude of the electric field at a distance of 10 cm from the wire (away from its ends) "
    "is:",
    place("1.8 × 10⁴ N/C", ["9.0 × 10³ N/C", "1.8 × 10⁵ N/C", "9.0 × 10⁴ N/C"], "D"),
    "Field of an infinitely long line charge (Gauss's law)",
    "A cylindrical Gaussian surface coaxial with the wire gives E(2πrl) = λl/ε₀, so E = λ/(2πε₀r) = 2kλ/r.",
    ["E = 2 × 9 × 10⁹ × 10⁻⁷ / 0.1 = 1.8 × 10⁴ N/C"],
    why="9.0 × 10³ N/C drops the factor 2 (writing kλ/r). 1.8 × 10⁵ N/C divides by r², as for a point charge. "
        "9.0 × 10⁴ N/C combines both slips (kλ/r²).",
    ncert="Class 12 Physics, 'Electric Charges and Fields', field due to an infinitely long straight uniformly "
          "charged wire", seconds=45, recomputed=True)

E_p, V_p = 500.0, 3000.0
r_p = V_p / E_p
q_p = V_p * r_p / k
assert close(r_p, 6.0) and close(q_p, 2e-6) and close(k * q_p / r_p ** 2, E_p)
assert close(E_p * r_p / k, 3.33e-7, 1e-2) and close(V_p * (E_p / V_p) / k, 5.56e-8, 1e-2) and close(V_p * r_p ** 2 / k, 1.2e-5)
add(T, "Electric potential and energy", "Intermediate", "numerical",
    "At a certain point in air, the electric field due to an isolated point charge is 500 N/C and the electric "
    "potential due to it is 3000 V. Taking 1/(4πε₀) = 9 × 10⁹ N m² C⁻², the magnitude of the charge is:",
    place("2 μC", ["0.33 μC", "0.056 μC", "12 μC"], "B"),
    "Relating E and V of a point charge",
    "For a point charge V = kq/r and E = kq/r², so V/E = r. Find r first, then q.",
    ["r = V/E = 3000/500 = 6 m", "q = Vr/k = 3000 × 6 / (9 × 10⁹) = 2 × 10⁻⁶ C = 2 μC",
     "Check: E = kq/r² = 18 × 10³/36 = 500 N/C ✓"],
    why="0.33 μC uses q = Er/k, forgetting to square r. 0.056 μC takes r = E/V = 1/6 m instead of V/E. 12 μC uses "
        "q = Vr²/k, mixing the field and potential formulas.",
    ncert="Class 12 Physics, 'Electrostatic Potential and Capacitance', potential due to a point charge", seconds=55,
    recomputed=True)

add(T, "Electric field and dipole", "Intermediate", "match_list",
    match_stem("Match List-I (quantity) with List-II (how it depends on the distance r). For the dipole, r is much "
               "larger than its length; for the sheet, r is the distance from a large plane sheet of uniform charge "
               "density, away from its edges.",
               ["Electric field of a point charge", "Electric potential of a point charge",
                "Electric field of a short dipole", "Electric field of a large, uniformly charged plane sheet"],
               ["Proportional to 1/r", "Independent of r", "Proportional to 1/r²", "Proportional to 1/r³"]),
    match_options({"A": "III", "B": "I", "C": "IV", "D": "II"},
                  [{"A": "I", "B": "III", "C": "IV", "D": "II"}, {"A": "III", "B": "I", "C": "II", "D": "IV"},
                   {"A": "III", "B": "IV", "C": "I", "D": "II"}], "C"),
    "Distance dependence of fields and potentials",
    "Point charge: E = kq/r², V = kq/r. A dipole's opposite charges nearly cancel at large distance, so its field "
    "falls faster, as 1/r³. A large plane sheet gives E = σ/2ε₀, the same at all distances near it.",
    ["Point-charge field → 1/r² (III)", "Point-charge potential → 1/r (I)", "Dipole field → 1/r³ (IV)",
     "Plane sheet → independent of r (II)"],
    why="The other codes swap the field and potential of the point charge, or the dipole and the sheet.",
    ncert="Class 12 Physics, 'Electric Charges and Fields', dipole field and applications of Gauss's law",
    seconds=40)

add(T, "Capacitors and dielectrics", "Intermediate", "statement_pair",
    SP_STEM.format(
        s1="A dielectric slab placed in an external electric field gets polarised, and the net field inside it is "
           "smaller than the external field.",
        s2="The molecules of a non-polar dielectric have a permanent electric dipole moment even in the absence of "
           "an external field."),
    sp("C"),
    "Polarisation of dielectrics",
    "In an external field, a dielectric develops induced (non-polar molecules) or aligned (polar molecules) dipoles. "
    "The resulting surface charges produce a field opposing the external one, so the net field inside is reduced. "
    "Non-polar molecules have coinciding centres of positive and negative charge, so their dipole moment is zero "
    "until a field is applied.",
    ["Statement I: polarisation opposes the applied field → true",
     "Statement II: permanent dipole moments belong to polar molecules → false"],
    why="Statement II describes polar molecules (such as H₂O), not non-polar ones (such as O₂).",
    ncert="Class 12 Physics, 'Electrostatic Potential and Capacitance', dielectrics and polarisation", seconds=40)

add(T, "Coulomb's law and superposition", "Intermediate", "assertion_reason",
    AR_STEM.format(
        a="A charged plastic comb attracts small pieces of uncharged paper.",
        r="The comb induces charges in the paper: the side nearer the comb gets a charge opposite to the comb's, and "
          "because it is closer, the attraction on it exceeds the repulsion on the farther side."),
    ar("A"),
    "Attraction of a neutral body by induction",
    "The paper as a whole stays neutral, but the comb separates its charges. The opposite charge is nearer the comb "
    "than the like charge, and the Coulomb force falls with distance, so the net force is attractive.",
    ["Induced opposite charge at the near side, like charge at the far side",
     "Force ∝ 1/r² → attraction on the near side wins → net attraction"],
    why="R gives the mechanism of A, so it is the correct explanation.",
    ncert="Class 12 Physics, 'Electric Charges and Fields', charging by induction", seconds=40)

multi_key([True, True, True, False, True], "abce")
add(T, "Electric field and dipole", "Intermediate", "multi_statement",
    multi("Which of the following statements about an electric dipole are correct?",
          ["At a distant point on the equatorial line of the dipole, the electric field is directed opposite to the "
           "dipole moment.",
           "In a uniform electric field, the net force on the dipole is zero.",
           "In a uniform electric field, the torque on the dipole is zero when its dipole moment is parallel to the "
           "field.",
           "The dipole moment vector points from the positive charge to the negative charge.",
           "In a non-uniform electric field, a dipole in general experiences a net force."]),
    place("(a), (b), (c) and (e) only", ["(a), (b) and (e) only", "(b), (c) and (d) only",
                                         "(a), (c), (d) and (e) only"], "A"),
    "Field of a dipole and a dipole in a field",
    "On the equatorial line, E = −kp/r³ (opposite to p). In a uniform field the forces qE and −qE cancel, while the "
    "torque p × E vanishes for p parallel (or antiparallel) to E. By convention p points from −q to +q. In a "
    "non-uniform field the two forces differ, leaving a net force.",
    ["(a) true", "(b) true", "(c) τ = pE sin 0° = 0 → true", "(d) p points from −q to +q → false", "(e) true"],
    why="Codes containing (d) reverse the conventional direction of the dipole moment; codes that leave out (c) "
        "miss the zero-torque position.",
    ncert="Class 12 Physics, 'Electric Charges and Fields', electric dipole; dipole in a uniform external field",
    seconds=80)

C1_, V1_, C2_, V2_ = 2.0, 100.0, 3.0, 50.0
V_unlike = abs(C1_ * V1_ - C2_ * V2_) / (C1_ + C2_)
V_like = (C1_ * V1_ + C2_ * V2_) / (C1_ + C2_)
assert close(V_unlike, 10.0) and close(V_like, 70.0)
add(T, "Capacitors and dielectrics", "Advanced", "numerical",
    "A 2 μF capacitor charged to 100 V and a 3 μF capacitor charged to 50 V are disconnected from their batteries. "
    "They are then connected to each other with the positive plate of each joined to the negative plate of the "
    "other. The final potential difference across each capacitor is:",
    place("10 V", ["70 V", "75 V", "0 V"], "D"),
    "Charge sharing between capacitors with opposite polarity",
    "Joining unlike plates lets the charges partly neutralise each other. The net charge on each connected pair of "
    "plates is the difference of the original charges, and it is shared by the two capacitors, now in parallel.",
    ["Q₁ = 2 × 100 = 200 μC; Q₂ = 3 × 50 = 150 μC",
     "Net charge = 200 − 150 = 50 μC", "V = 50/(2 + 3) = 10 V"],
    why="70 V = (200 + 150)/5 is the common voltage when like plates are joined. 75 V is the average of the two "
        "voltages. 0 V assumes the charges cancel completely, which happens only if Q₁ = Q₂.",
    ncert="Class 12 Physics, 'Electrostatic Potential and Capacitance', combination of capacitors", seconds=70,
    recomputed=True)

q_in, q_out, Rs = 1e-9, 2e-9, 0.1
V_inner = k * q_in / Rs + k * q_out / (2 * Rs)
V_outer = k * (q_in + q_out) / (2 * Rs)
assert close(V_inner, 180.0) and close(V_outer, 135.0) and close(V_inner - V_outer, 45.0)
add(T, "Electric potential and energy", "Advanced", "numerical",
    "Two thin concentric conducting spherical shells have radii 10 cm and 20 cm. The inner shell carries a charge of "
    "1 nC and the outer shell a charge of 2 nC. Taking 1/(4πε₀) = 9 × 10⁹ N m² C⁻², the potential difference between "
    "the inner and the outer shell is:",
    place("45 V", ["180 V", "135 V", "90 V"], "B"),
    "Potentials of concentric shells",
    "A shell of charge Q and radius R gives a potential kQ/R everywhere inside it and kQ/r outside. Add the "
    "contributions of both shells at each shell's radius. The outer shell adds the same potential at both places, so "
    "it drops out of the difference.",
    ["V_inner = k(1 nC)/0.1 + k(2 nC)/0.2 = 90 + 90 = 180 V",
     "V_outer = k(3 nC)/0.2 = 135 V", "V_inner − V_outer = 45 V = kq_in(1/0.1 − 1/0.2)"],
    why="180 V and 135 V are the potentials of the individual shells, not their difference. 90 V is kq_in/R₁, "
        "forgetting to subtract the inner charge's potential at the outer shell.",
    shortcut="ΔV depends only on the inner charge: kq(1/R₁ − 1/R₂) = 9 × (10 − 5) = 45 V.",
    ncert="Class 12 Physics, 'Electrostatic Potential and Capacitance', potential due to a system of charges",
    seconds=85, recomputed=True)

# Capacitor bridge: A–C1–P–C2–B and A–C3–Q–C4–B, with C5 between P and Q; all initially uncharged, V_A = 1, V_B = 0.
c1, c2, c3, c4, c5 = F(1), F(2), F(2), F(4), F(5)
# Charge conservation at the isolated nodes P and Q:
#   c1(VP-1) + c2 VP + c5(VP-VQ) = 0 ;  c3(VQ-1) + c4 VQ + c5(VQ-VP) = 0
a11, a12, b1 = c1 + c2 + c5, -c5, c1
a21, a22, b2 = -c5, c3 + c4 + c5, c3
det = a11 * a22 - a12 * a21
VP = (b1 * a22 - a12 * b2) / det
VQ = (a11 * b2 - b1 * a21) / det
C_eq = c1 * (1 - VP) + c3 * (1 - VQ)
assert VP == VQ == F(1, 3) and C_eq == 2 and c1 / c2 == c3 / c4
add(T, "Capacitors and dielectrics", "Advanced", "numerical",
    "Five uncharged capacitors are connected between two terminals A and B as follows. A 1 μF capacitor joins A to a "
    "point P, and a 2 μF capacitor joins P to B. A 2 μF capacitor joins A to a point Q, and a 4 μF capacitor joins Q "
    "to B. A 5 μF capacitor joins P to Q. The equivalent capacitance between A and B is:",
    place("2 μF", ["7 μF", "14 μF", "4/3 μF"], "C"),
    "Balanced capacitor bridge",
    "In series, capacitors share the voltage in inverse proportion to their capacitances. Branch A–P–B (1 μF, 2 μF) "
    "puts 2/3 of the applied voltage across the 1 μF capacitor; branch A–Q–B (2 μF, 4 μF) puts 2/3 across the 2 μF "
    "capacitor. So P and Q are at the same potential (the bridge is balanced since 1/2 = 2/4), the 5 μF capacitor "
    "gets no charge, and it can be removed.",
    ["Balance: C(AP)/C(PB) = 1/2 = C(AQ)/C(QB) = 2/4 → V_P = V_Q, no charge on 5 μF",
     "Branch A–P–B: 1 × 2/(1 + 2) = 2/3 μF; branch A–Q–B: 2 × 4/(2 + 4) = 4/3 μF",
     "C_eq = 2/3 + 4/3 = 2 μF"],
    why="7 μF adds the idle 5 μF capacitor in parallel with the bridge. 14 μF adds all five capacitances. 4/3 μF "
        "keeps only the A–Q–B branch.",
    ncert="Class 12 Physics, 'Electrostatic Potential and Capacitance', combination of capacitors", seconds=100,
    recomputed=True)

E_h, R_h = 200.0, 0.1
flux_curved = E_h * math.pi * R_h ** 2
assert close(flux_curved, 2 * math.pi) and close(E_h * 2 * math.pi * R_h ** 2, 4 * math.pi)
add(T, "Gauss's law", "Advanced", "numerical",
    "A hemispherical surface of radius 10 cm (open, without its flat base) is placed in a uniform electric field of "
    "200 N/C. The field is parallel to the axis of the hemisphere, that is, perpendicular to the plane of its rim. "
    "The magnitude of the electric flux through the curved surface is:",
    place("2π N m² C⁻¹", ["4π N m² C⁻¹", "Zero", "8π N m² C⁻¹"], "A"),
    "Flux through an open curved surface in a uniform field",
    "Close the hemisphere with its flat circular base. The closed surface encloses no charge, so the total flux is "
    "zero: whatever field lines enter through the flat base leave through the curved surface. The flux through the "
    "base is simply E × πR², since the field is perpendicular to it.",
    ["Closed surface (hemisphere + base) encloses no charge → total flux 0",
     "|Flux through base| = E πR² = 200 × π × 0.01 = 2π N m² C⁻¹",
     "|Flux through curved surface| = 2π N m² C⁻¹ ≈ 6.3 N m² C⁻¹"],
    why="4π multiplies E by the curved area 2πR², as if the field were normal to the curved surface everywhere. "
        "Zero applies to the closed surface, not to the open hemisphere. 8π uses the area of a full sphere.",
    ncert="Class 12 Physics, 'Electric Charges and Fields', electric flux and Gauss's law", seconds=70,
    recomputed=True)

Kd = 4
V0, d0, Q0, C0 = F(1), F(1), F(1), F(1)          # initial values (units arbitrary)
assert (V0 / (2 * d0)) / (V0 / d0) == F(1, 2)                       # A: V fixed, E = V/d
assert ((Q0 * d0 * 2) / (2 * d0)) / ((Q0 * d0) / d0) == 1           # B: Q fixed, V = Qd/(eps A) ∝ d, E = V/d
assert ((Kd * C0) * V0) / (C0 * V0) == 4                            # C: V fixed, Q = CV
assert (Q0 / (Kd * C0)) / (Q0 / C0) == F(1, 4)                      # D: Q fixed, V = Q/C
add(T, "Capacitors and dielectrics", "Advanced", "match_list",
    match_stem("A parallel plate capacitor with air between its plates is first charged by a battery. Match List-I "
               "(change made) with List-II (resulting change in the stated quantity).",
               ["The battery stays connected and the plate separation is doubled: the electric field between the "
                "plates",
                "The battery is disconnected and the plate separation is doubled: the electric field between the "
                "plates",
                "The battery stays connected and a dielectric of constant 4 fills the gap: the charge on the plates",
                "The battery is disconnected and a dielectric of constant 4 fills the gap: the potential difference "
                "between the plates"],
               ["Becomes 4 times", "Becomes one-fourth", "Becomes half", "Remains unchanged"]),
    match_options({"A": "III", "B": "IV", "C": "I", "D": "II"},
                  [{"A": "IV", "B": "III", "C": "I", "D": "II"}, {"A": "III", "B": "IV", "C": "II", "D": "I"},
                   {"A": "III", "B": "I", "C": "IV", "D": "II"}], "B"),
    "Capacitor at constant V and at constant Q",
    "Connected to the battery, V is fixed; disconnected, Q is fixed. E = V/d between the plates, and C = Kε₀A/d.",
    ["A: V fixed, d doubled → E = V/2d → half (III)",
     "B: Q fixed → E = Q/(ε₀A) does not involve d → unchanged (IV)",
     "C: V fixed, C → 4C → Q = CV becomes 4 times (I)",
     "D: Q fixed, C → 4C → V = Q/C becomes one-fourth (II)"],
    why="The other codes treat the disconnected capacitor's field as halving (it depends only on Q/A), or swap the "
        "constant-V and constant-Q results for the dielectric.",
    ncert="Class 12 Physics, 'Electrostatic Potential and Capacitance', the parallel plate capacitor; effect of "
          "dielectric on capacitance", seconds=80)

multi_key([True, True, False, False, True], "abe")
add(T, "Electric potential and energy", "Advanced", "multi_statement",
    multi("Which of the following statements are correct? Take the potential to be zero at infinity.",
          ["The electrostatic potential energy of a system of two opposite point charges is negative.",
           "The work done by an electrostatic field on a charge carried round any closed path is zero.",
           "If the electric field at a point is zero, the electric potential at that point must also be zero.",
           "The electron volt is a unit of potential difference.",
           "An electron released from rest in an electrostatic field moves towards the region of higher "
           "potential."]),
    place("(a), (b) and (e) only", ["(a), (b), (c) and (e) only", "(b), (c) and (d) only", "(a), (d) and (e) only"],
          "D"),
    "Potential, potential energy and the electron volt",
    "U = kq₁q₂/r < 0 for opposite charges. The electrostatic force is conservative, so its work round a closed path "
    "is zero. E = −dV/dr, so zero field means a stationary potential, not zero potential (at the midpoint between "
    "two equal like charges E = 0 but V ≠ 0). The electron volt is a unit of energy. A negative charge lowers its "
    "potential energy qV by moving to a higher potential.",
    ["(a) q₁q₂ < 0 → U < 0 → true", "(b) conservative force → true",
     "(c) two equal like charges: E = 0 at the midpoint, V = 2kq/(d/2) ≠ 0 → false",
     "(d) 1 eV = 1.6 × 10⁻¹⁹ J, an energy → false",
     "(e) U = −eV decreases as V increases → electron moves to higher V → true"],
    why="Codes containing (c) equate zero field with zero potential; codes containing (d) take the electron volt as "
        "a potential difference because of its name.",
    ncert="Class 12 Physics, 'Electrostatic Potential and Capacitance', potential energy of a system of charges",
    seconds=90)


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
    doc = {"schema_version": "1.0", "batch_id": "BATCH_003", "created_at": TODAY,
           "notes": "BATCH_003 package PHY_003_p1: 132 original Physics questions (Physics and Measurement through "
                    "Electrostatics). Every numerical answer is re-derived in tools/batch_003/PHY_003_p1.py.",
           "stimuli": [], "questions": QUESTIONS}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {OUT}: {n} questions, {dict(Counter(x['difficulty'] for x in QUESTIONS))}")
    print(f"keys {dict(sorted(keys.items()))}")
    print(f"formats {dict(fmts)}")
