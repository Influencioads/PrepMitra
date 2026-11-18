"""Writes batches/parts/BATCH_010_PHY_p1.json: package PHY_010_p1 of BATCH_010 (116 Physics questions).

Topics: Physics and Measurement, Kinematics, Laws of Motion, Work Energy and Power, Rotational Motion, Gravitation,
Properties of Solids and Liquids, Thermodynamics, Kinetic Theory of Gases, Oscillations and Waves, Electrostatics.
IDs NEET_PHY_002251 .. NEET_PHY_002366, in the order the questions are listed below.

Every computable answer is re-derived with an assert before the file is written, and so is the plan quota. If any
assert fails, nothing is written. Each question's answer position is chosen by hand and fixed.

    python tools/batch_010/PHY_010_p1.py        (run from docs/neet-bank)
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
OUT = ROOT / "batches" / "parts" / "BATCH_010_PHY_p1.json"
PLAN = ROOT / "batches" / "plans" / "BATCH_010_plan.json"
PACKAGE = "PHY_010_p1"
TODAY = "2026-11-16"
LETTERS = "ABCD"
PHY = "Physics"
RECOMPUTED = ("script:recompute", "ai:author-solve", "ai:self-recheck")
AUTHORED = ("ai:author-solve", "ai:self-recheck")
FIRST_ID = 2251

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


def dims(m=0, l=0, t=0, a=0):
    return (m, l, t, a)


def dmul(*ds):
    return tuple(sum(x) for x in zip(*ds))


def ddiv(a, b):
    return tuple(x - y for x, y in zip(a, b))


g = 10.0
k = 9e9
EPS0 = 8.85e-12

# =====================================================================================================================
# Physics and Measurement (B1 I2 A1)
# =====================================================================================================================
T = "Physics and Measurement"

assert close(2.25 / 100, 0.0225)
add(T, "Least count and significant figures", "Basic", "numerical",
    "A stack of exactly 100 identical sheets of paper is measured to be 2.25 cm thick. The thickness of one sheet, "
    "written with the correct number of significant figures, is:",
    place("0.0225 cm", ["0.02 cm", "0.023 cm", "0.02250 cm"], "B"),
    "Significant figures when a measured value is divided by an exact number",
    "The number of sheets, 100, is a count and so an exact number with unlimited significant figures. The result "
    "therefore keeps the three significant figures of the measured thickness 2.25 cm.",
    ["Thickness of one sheet = 2.25 cm / 100 = 0.0225 cm",
     "100 is exact, so the result has as many significant figures as 2.25, i.e. three: 0.0225 cm"],
    why="0.02 cm treats 100 as having only one significant figure; 0.023 cm wrongly rounds to two significant "
        "figures; 0.02250 cm adds a fourth significant figure that the measurement does not have.",
    ncert="Class 11 Physics, 'Units and Measurement', significant figures (exact numbers in a calculation)",
    seconds=40, recomputed=True)

# dimensions with current: resistance, magnetic field, magnetic flux, inductance
FORCE = dims(1, 1, -2)
CHARGE = dims(0, 0, 1, 1)
VOLT = ddiv(dims(1, 2, -2), CHARGE)                       # energy per charge
RES = ddiv(VOLT, dims(0, 0, 0, 1))                        # V / I
BFIELD = ddiv(FORCE, dmul(CHARGE, dims(0, 1, -1)))        # F = q v B
FLUX = dmul(BFIELD, dims(0, 2, 0))                        # B x area
IND = ddiv(FLUX, dims(0, 0, 0, 1))                        # flux = L I
assert RES == (1, 2, -3, -2) and BFIELD == (1, 0, -2, -1) and FLUX == (1, 2, -2, -1) and IND == (1, 2, -2, -2)
add(T, "Dimensional analysis", "Intermediate", "match_list",
    match_stem("Match List-I (physical quantity) with List-II (its dimensional formula). A stands for the dimension "
               "of electric current.",
               ["Electrical resistance", "Magnetic field (magnetic induction) B", "Magnetic flux",
                "Self-inductance"],
               ["[M L² T⁻² A⁻¹]", "[M L² T⁻³ A⁻²]", "[M L² T⁻² A⁻²]", "[M T⁻² A⁻¹]"]),
    match_options({"A": "II", "B": "IV", "C": "I", "D": "III"},
                  [{"A": "II", "B": "I", "C": "IV", "D": "III"}, {"A": "III", "B": "IV", "C": "I", "D": "II"},
                   {"A": "II", "B": "IV", "C": "III", "D": "I"}], "D"),
    "Dimensional formulae built step by step from defining relations",
    "Start from relations whose dimensions are known. Potential difference is work per unit charge, "
    "[M L² T⁻²]/[A T] = [M L² T⁻³ A⁻¹]; resistance is V/I. The magnetic force on a moving charge is F = qvB, "
    "so B = F/(qv). Flux is B × area, and self-inductance is flux per unit current (Φ = LI).",
    ["V = W/q → [M L² T⁻³ A⁻¹]; R = V/I → [M L² T⁻³ A⁻²] (II)",
     "B = F/(qv) = [M L T⁻²]/([A T][L T⁻¹]) = [M T⁻² A⁻¹] (IV)",
     "Φ = B × area → [M L² T⁻² A⁻¹] (I)",
     "L = Φ/I → [M L² T⁻² A⁻²] (III)"],
    shortcut="Flux and inductance differ only by one power of A; resistance is the only one with T⁻³.",
    why="The other codes swap flux with inductance (they differ by A⁻¹), or swap resistance with inductance, which "
        "share M L² A⁻² but differ in the power of T.",
    ncert="Class 11 Physics, 'Units and Measurement', dimensional formulae and dimensional equations",
    seconds=90)

l1, l2, dl = 20.0, 45.0, 0.1
x_ = l2 - l1
dx = 2 * dl
pct = 2 * dx / x_ * 100
assert close(x_, 25.0) and close(dx, 0.2) and close(pct, 1.6)
assert close(2 * (dl / l1 + dl / l2) * 100, 1.444, rel=1e-3)
add(T, "Errors in measurement", "Intermediate", "numerical",
    "The positions of the two ends of a rod on a metre scale are read as (20.0 ± 0.1) cm and (45.0 ± 0.1) cm. The "
    "length x of the rod is the difference of the two readings. The maximum percentage error in the quantity x² is:",
    place("1.6%", ["0.8%", "1.4%", "0.4%"], "A"),
    "Error in a difference, then error in a power",
    "When two quantities are subtracted, their absolute errors add: x = (25.0 ± 0.2) cm. When a quantity is "
    "raised to a power n, its relative error is multiplied by n.",
    ["x = 45.0 − 20.0 = 25.0 cm, Δx = 0.1 + 0.1 = 0.2 cm",
     "Relative error in x = 0.2/25.0 = 0.008 = 0.8%",
     "Relative error in x² = 2 × 0.8% = 1.6%"],
    why="0.8% is the error in x itself (the square is forgotten); 1.4% adds the percentage errors of the two "
        "readings (0.5% + 0.22%) and doubles them, but errors of a difference must be added as absolute errors; "
        "0.4% takes Δx as 0.1 cm and forgets to double for the square.",
    ncert="Class 11 Physics, 'Units and Measurement', combination of errors", seconds=75, recomputed=True)

d = [2.02, 1.98, 2.03, 1.97, 2.00]
mean = sum(d) / 5
mae = sum(abs(v - mean) for v in d) / 5
assert close(mean, 2.00) and close(mae, 0.02) and close(2 * mae / mean * 100, 2.0)
add(T, "Errors in measurement", "Advanced", "numerical",
    "The diameter of a wire is measured five times with a screw gauge, giving 2.02 mm, 1.98 mm, 2.03 mm, 1.97 mm and "
    "2.00 mm. Taking the mean absolute error as the error in the diameter, the percentage error in the area of "
    "cross-section of the wire, calculated as πd²/4, is:",
    place("2%", ["1%", "4%", "0.5%"], "C"),
    "Mean value, mean absolute error and the error in a squared quantity",
    "The best estimate is the arithmetic mean; the mean absolute error is the mean of the magnitudes of the "
    "deviations. The area depends on d², so its relative error is twice that of d (π/4 is exact).",
    ["Mean d = (2.02 + 1.98 + 2.03 + 1.97 + 2.00)/5 = 2.00 mm",
     "|Deviations| = 0.02, 0.02, 0.03, 0.03, 0.00 → mean absolute error = 0.10/5 = 0.02 mm",
     "Relative error in d = 0.02/2.00 = 1%",
     "Area ∝ d² → percentage error = 2 × 1% = 2%"],
    why="1% is the error in the diameter, not the area; 4% multiplies the relative error by 4 (the 4 in πd²/4 "
        "is exact and adds no error); 0.5% halves the relative error instead of doubling it.",
    ncert="Class 11 Physics, 'Units and Measurement', absolute error, relative error and percentage error",
    seconds=110, recomputed=True)

# =====================================================================================================================
# Kinematics (B3 I5 A3)
# =====================================================================================================================
T = "Kinematics"

assert close(math.sqrt(2 * g * 45), 30.0)
add(T, "Motion in a straight line", "Basic", "numerical",
    "A stone is dropped from rest from the top of a building 45 m high. Taking g = 10 m/s² and neglecting air "
    "resistance, the speed with which it hits the ground is:",
    place("30 m/s", ["15 m/s", "45 m/s", "30√2 m/s"], "D"),
    "Uniformly accelerated motion: v² = u² + 2as",
    "For free fall from rest, u = 0 and a = g, so v² = 2gh.",
    ["v² = 0 + 2 × 10 × 45 = 900", "v = 30 m/s"],
    shortcut="Time of fall √(2h/g) = 3 s, and v = gt = 30 m/s.",
    why="15 m/s is half the speed (v = gt/2 confuses average and final speed); 45 m/s takes v numerically equal to h; "
        "30√2 m/s uses v² = 4gh.",
    seconds=30, recomputed=True)

Av, Bv = (3, 4, 0), (4, -3, 0)
dot = sum(a * b for a, b in zip(Av, Bv))
crs = Av[0] * Bv[1] - Av[1] * Bv[0]
summ = math.hypot(Av[0] + Bv[0], Av[1] + Bv[1])
assert dot == 0 and abs(crs) == 25 and close(summ, 5 * math.sqrt(2)) and close(math.hypot(3, 4), 5)
add(T, "Vectors", "Basic", "match_list",
    match_stem("For the vectors A = 3î + 4ĵ and B = 4î − 3ĵ, match List-I (quantity) with List-II (its value).",
               ["A · B", "|A × B|", "|A + B|", "|A|"],
               ["5", "0", "5√2", "25"]),
    match_options({"A": "II", "B": "IV", "C": "III", "D": "I"},
                  [{"A": "IV", "B": "II", "C": "III", "D": "I"}, {"A": "II", "B": "IV", "C": "I", "D": "III"},
                   {"A": "II", "B": "III", "C": "IV", "D": "I"}], "B"),
    "Scalar product, vector product and magnitude of vectors in component form",
    "A · B = AₓBₓ + A_yB_y. For vectors in the x–y plane, A × B = (AₓB_y − A_yBₓ) k̂. The magnitude of a vector "
    "is the square root of the sum of the squares of its components.",
    ["A · B = 3 × 4 + 4 × (−3) = 0 (II): the vectors are perpendicular",
     "A × B = (3 × (−3) − 4 × 4) k̂ = −25 k̂ → |A × B| = 25 (IV)",
     "A + B = 7î + ĵ → |A + B| = √50 = 5√2 (III)", "|A| = √(9 + 16) = 5 (I)"],
    shortcut="Since A ⊥ B and |A| = |B| = 5, |A × B| = 5 × 5 = 25 and |A + B| = 5√2 at once.",
    why="Swapping the dot and cross products is the usual slip; the other codes put |A + B| = 5 (adding magnitudes "
        "wrongly) or interchange 5√2 and 25.",
    ncert="Class 11 Physics, 'Motion in a Plane', addition of vectors and resolution; scalar and vector products",
    seconds=60)

add(T, "Uniform circular motion", "Basic", "direct",
    "A particle moves with constant speed around a circle. Over the time it takes to go round the circle exactly "
    "once, its average velocity and its average acceleration are:",
    place("both zero",
          ["zero and v²/r respectively", "2πr/T and zero respectively", "both non-zero"], "C"),
    "Average velocity and average acceleration over a closed path",
    "Average velocity is (net displacement)/(time) and average acceleration is (change in velocity)/(time). After "
    "one full revolution the particle is back at its starting point (zero displacement) and has the same velocity, "
    "in magnitude and direction, as at the start (zero change in velocity). Both averages are therefore zero, even "
    "though the instantaneous acceleration v²/r is never zero.",
    ["Net displacement in one revolution = 0 → average velocity = 0",
     "Final velocity = initial velocity → Δv = 0 → average acceleration = 0"],
    why="v²/r is the magnitude of the instantaneous (centripetal) acceleration, not its average over a revolution; "
        "2πr/T is the average speed, not the average velocity.",
    ncert="Class 11 Physics, 'Motion in a Plane', uniform circular motion", seconds=35)

# v = 3x -> a = v dv/dx = 9x
a_ = 3 * (3 * 2)
assert a_ == 18
add(T, "Motion in a straight line", "Intermediate", "numerical",
    "A particle moves along the x-axis so that its velocity at position x is v = 3x, where v is in m/s and x in "
    "metres. Its acceleration when it is at x = 2 m is:",
    place("18 m/s²", ["3 m/s²", "6 m/s²", "9 m/s²"], "B"),
    "Acceleration from velocity given as a function of position: a = v (dv/dx)",
    "By the chain rule, a = dv/dt = (dv/dx)(dx/dt) = v (dv/dx). Here dv/dx = 3, so a = 3v = 9x.",
    ["dv/dx = 3 s⁻¹", "At x = 2 m: v = 6 m/s", "a = v dv/dx = 6 × 3 = 18 m/s²"],
    why="3 m/s² takes dv/dx alone as the acceleration; 6 m/s² is the velocity at x = 2 m; 9 m/s² is the value of "
        "9x at x = 1 m.",
    seconds=60, recomputed=True)

vr, ang = 20.0, math.radians(30)
vx_rain, vy_rain = vr * math.sin(ang), vr * math.cos(ang)
assert close(vx_rain, 10) and close(vy_rain, 10 * math.sqrt(3))
add(T, "Relative velocity", "Intermediate", "numerical",
    "Rain is falling with a speed of 20 m/s at an angle of 30° with the vertical, its horizontal component of "
    "velocity being towards the east. A man walks on a level road. The velocity with which he must walk so that "
    "the rain appears to him to fall vertically, and the speed of the rain relative to him, are respectively:",
    place("10 m/s towards the east, 10√3 m/s",
          ["10 m/s towards the west, 10√3 m/s", "10√3 m/s towards the east, 10 m/s",
           "10 m/s towards the east, 20 m/s"], "D"),
    "Relative velocity in two dimensions",
    "The velocity of the rain relative to the man is v_rain − v_man. For it to be vertical, the man's velocity must "
    "cancel the horizontal component of the rain's velocity, so he must walk east at that component. What is left "
    "is the vertical component of the rain's velocity.",
    ["Horizontal component of rain = 20 sin 30° = 10 m/s (east)",
     "Vertical component = 20 cos 30° = 10√3 m/s (downward)",
     "Man walks east at 10 m/s → relative velocity = 10√3 m/s vertically downward"],
    why="Walking west would double the horizontal relative component; 10√3 m/s east uses cos 30° for the horizontal "
        "component; 20 m/s is the speed relative to the ground, not relative to the man.",
    seconds=75, recomputed=True)

v2, a2 = (4, 2 * 2), (0, 2)
cosang = (v2[0] * a2[0] + v2[1] * a2[1]) / (math.hypot(*v2) * math.hypot(*a2))
assert close(math.degrees(math.acos(cosang)), 45)
add(T, "Vectors", "Intermediate", "numerical",
    "The position vector of a particle moving in the x–y plane is r = (4t) î + (t²) ĵ, where r is in metres and t "
    "in seconds. At t = 2 s, the angle between its velocity and its acceleration is:",
    place("45°", ["0°", "90°", "60°"], "A"),
    "Velocity and acceleration as derivatives of the position vector",
    "v = dr/dt and a = dv/dt; the angle between them follows from cos θ = (v · a)/(|v||a|).",
    ["v = 4 î + 2t ĵ → at t = 2 s, v = 4î + 4ĵ m/s", "a = 2 ĵ m/s² (constant)",
     "cos θ = (4 × 0 + 4 × 2)/(4√2 × 2) = 1/√2 → θ = 45°"],
    why="90° would hold only at t = 0, when v = 4î; 0° would need v along ĵ; 60° comes from a wrong magnitude of v.",
    seconds=70, recomputed=True)

# trajectory y = x - 0.05 x^2 ; tan(theta) = 1 ; g/(2u^2 cos^2) = 0.05
u2 = g / (2 * 0.05 * 0.5)
u_ = math.sqrt(u2)
R_ = u2 * 1 / g
H_ = u2 * 0.5 / (2 * g)
Tf = 2 * u_ * math.sin(math.pi / 4) / g
assert close(u_, 10 * math.sqrt(2)) and close(R_, 20) and close(H_, 5) and close(Tf, 2)
truth = [True, True, True, False, False]
multi_key(truth, "abc")
add(T, "Projectile motion", "Intermediate", "multi_statement",
    multi("A projectile launched from level ground moves along the path y = x − 0.05x², where x (horizontal) and y "
          "(vertical) are in metres, measured from the point of projection. Taking g = 10 m/s² and neglecting air "
          "resistance, which of the following statements are correct?",
          ["The angle of projection is 45° above the horizontal.",
           "The speed of projection is 10√2 m/s.",
           "The horizontal range is 20 m.",
           "The maximum height reached is 10 m.",
           "The time of flight is 2√2 s."]),
    place("(a), (b) and (c) only", ["(a), (b), (c) and (d) only", "(a), (c) and (e) only",
                                    "(b), (d) and (e) only"], "B"),
    "Reading a projectile's speed and angle from its trajectory equation",
    "The trajectory is y = x tan θ − g x²/(2u² cos² θ). Comparing coefficients gives tan θ = 1 and "
    "g/(2u² cos² θ) = 0.05. The range, height and time then follow from the usual formulas, or directly from the "
    "equation (y = 0 again at x = 20 m).",
    ["(a) tan θ = 1 → θ = 45°, true",
     "(b) 10/(2u² × ½) = 0.05 → u² = 200 → u = 10√2 m/s, true",
     "(c) y = 0 at x = 0 and x = 1/0.05 = 20 m → R = 20 m, true",
     "(d) H = u² sin² θ/2g = 200 × ½/20 = 5 m (or y at x = 10 m = 10 − 5 = 5 m) → false",
     "(e) T = 2u sin θ/g = 2 × 10√2 × (1/√2)/10 = 2 s → false"],
    shortcut="The maximum height occurs at half the range: y(10) = 10 − 0.05 × 100 = 5 m.",
    why="(d) doubles the true height; (e) forgets the factor sin 45° in the vertical component of velocity.",
    ncert="Class 11 Physics, 'Motion in a Plane', projectile motion (equation of path)", seconds=120,
    recomputed=True)

add(T, "Motion in a straight line", "Intermediate", "assertion_reason",
    AR_STEM.format(
        a="For a particle moving along a straight line with constant acceleration, its average velocity over a time "
          "interval equals its instantaneous velocity at the middle instant of that interval.",
        r="When the acceleration is constant, the velocity changes linearly with time, so the average of the "
          "velocities at the beginning and end of the interval is also the velocity at its mid-instant."),
    ar("A"),
    "Average velocity for uniformly accelerated motion",
    "With constant acceleration, v = u + at is linear in t. The displacement in time t is ut + ½at², so the "
    "average velocity is u + ½at, which is exactly the velocity at time t/2. The reason states the linearity that "
    "makes this true, so R correctly explains A.",
    ["Average velocity = s/t = u + ½at", "Velocity at t/2 = u + a(t/2) = u + ½at → equal",
     "This depends on v being linear in t (constant a) → R explains A"],
    why="R is not merely a related fact: if the acceleration were not constant, v(t) would not be linear and the "
        "average velocity would not in general equal the mid-instant velocity.",
    ncert="Class 11 Physics, 'Motion in a Straight Line', kinematic equations for uniformly accelerated motion",
    seconds=60)

h_w, vs = 80.0, 320.0
t1 = math.sqrt(2 * h_w / g)
assert close(t1 + h_w / vs, 4.25)
assert close(0.5 * g * 4.25 ** 2, 90.3125)
add(T, "Motion in a straight line", "Advanced", "numerical",
    "A stone is dropped from rest into a well. The sound of the splash is heard 4.25 s after the stone is released. "
    "Taking g = 10 m/s², the speed of sound in air as 320 m/s and neglecting air resistance, the depth of the water "
    "surface below the point of release is:",
    place("80 m", ["90.3 m", "45 m", "68 m"], "C"),
    "Two successive motions: free fall, then sound returning at constant speed",
    "The total time is the time of fall, √(2h/g), plus the time the sound takes to come back up, h/v. The depth "
    "must satisfy both together; trying the value that makes the fall time a whole number of seconds shows "
    "h = 80 m works.",
    ["Fall time t₁ = √(2h/10), sound time t₂ = h/320, t₁ + t₂ = 4.25 s",
     "Try h = 80 m: t₁ = √16 = 4 s, t₂ = 80/320 = 0.25 s → total 4.25 s ✓",
     "(Only one positive depth satisfies the condition, since t₁ + t₂ increases steadily with h.)"],
    why="90.3 m ignores the time taken by the sound (½ × 10 × 4.25²); 45 m and 68 m do not give a total time of "
        "4.25 s (they give 3.14 s and about 3.90 s).",
    seconds=120, recomputed=True)

t_a, t_b = 2.0, 4.0
u_v = g * (t_a + t_b) / 2
h_c = u_v * t_a - 0.5 * g * t_a ** 2
Hm = u_v ** 2 / (2 * g)
assert close(u_v, 30) and close(h_c, 40) and close(Hm, 45) and close(u_v - g * t_a, 10) and close(2 * u_v / g, 6)
truth = [True, False, True, False, True]
multi_key(truth, "ace")
add(T, "Motion in a straight line", "Advanced", "multi_statement",
    multi("A ball is thrown vertically upward from the ground. It is at the same height above the ground at t = 2 s "
          "(going up) and at t = 4 s (coming down). Taking g = 10 m/s² and neglecting air resistance, which of the "
          "following statements are correct?",
          ["The ball was thrown up with a speed of 30 m/s.",
           "The common height at t = 2 s and t = 4 s is 30 m.",
           "The maximum height reached by the ball is 45 m.",
           "The speed of the ball at t = 2 s is 20 m/s.",
           "The ball returns to the ground at t = 6 s."]),
    place("(a), (c) and (e) only", ["(a), (b), (c) and (e) only", "(a), (d) and (e) only",
                                    "(b), (c) and (d) only"], "D"),
    "Symmetry of vertical motion under gravity",
    "The ball is at its highest point midway between two instants at which it is at the same height, i.e. at "
    "t = 3 s. So u = g × 3 = 30 m/s. The rest follows from the equations of motion.",
    ["Highest point at t = (2 + 4)/2 = 3 s → u = 10 × 3 = 30 m/s → (a) true",
     "Height at t = 2 s: 30 × 2 − 5 × 4 = 40 m → (b) false",
     "H = u²/2g = 900/20 = 45 m → (c) true",
     "Speed at t = 2 s: 30 − 20 = 10 m/s → (d) false",
     "Time of flight = 2u/g = 6 s → (e) true"],
    shortcut="For heights reached at t₁ and t₂: u = g(t₁ + t₂)/2 and h = g t₁t₂/2 = 5 × 2 × 4 = 40 m.",
    why="(b) takes the height as u × 1 s; (d) uses the speed lost in 1 s instead of 2 s.",
    seconds=110, recomputed=True)

u_rel, gap = 20.0 - 10.0, 50.0
amin = u_rel ** 2 / (2 * gap)
assert close(amin, 1.0) and close((20 ** 2 - 10 ** 2) / (2 * gap), 3.0) and close(20 ** 2 / (2 * gap), 4.0)
add(T, "Relative velocity", "Advanced", "numerical",
    "A car moving at 20 m/s along a straight road is 50 m behind a truck moving in the same direction at a "
    "constant 10 m/s. At this instant the driver of the car applies the brakes, giving the car a uniform "
    "retardation. The least retardation that will just prevent the car from hitting the truck is:",
    place("1 m/s²", ["3 m/s²", "4 m/s²", "0.5 m/s²"], "A"),
    "Relative motion in one dimension with constant relative acceleration",
    "Work in the frame of the truck, which moves with constant velocity. Relative to the truck, the car starts "
    "50 m behind with a speed of 10 m/s and decelerates at a. A collision is just avoided if the relative speed "
    "becomes zero exactly as the gap closes.",
    ["Initial relative speed = 20 − 10 = 10 m/s; relative retardation = a (the truck does not accelerate)",
     "Relative distance covered before relative rest = 10²/(2a)",
     "10²/(2a) = 50 → a = 1 m/s²"],
    why="3 m/s² applies (20² − 10²)/(2 × 50) using ground distances while ignoring that the truck also moves; "
        "4 m/s² stops the car completely within 50 m; 0.5 m/s² is too small (the gap closes before the speeds "
        "become equal).",
    seconds=100, recomputed=True)

# =====================================================================================================================
# Laws of Motion (B3 I5 A3)
# =====================================================================================================================
T = "Laws of Motion"

# x = 3t^2 - 2t -> a = 6
assert 2 * 6 == 12
add(T, "Newton's laws and impulse", "Basic", "numerical",
    "A body of mass 2 kg moves along the x-axis so that its position is x = 3t² − 2t, where x is in metres and t "
    "in seconds. The net force acting on it is:",
    place("12 N", ["6 N", "8 N", "24 N"], "C"),
    "Newton's second law with acceleration found by differentiation",
    "Differentiate the position twice to get the acceleration; it is constant here, so the net force is constant.",
    ["v = dx/dt = 6t − 2", "a = dv/dt = 6 m/s²", "F = ma = 2 × 6 = 12 N"],
    why="6 N omits the factor 2 on differentiating 3t² (takes a = 3 m/s²); 8 N uses the velocity 6t − 2 at t = 1 s "
        "as an acceleration and multiplies by 2; 24 N doubles the correct value.",
    seconds=40, recomputed=True)

add(T, "Friction", "Basic", "direct",
    "A block is pulled along a rough horizontal floor with a constant velocity by a horizontal force of 12 N. The "
    "frictional force acting on the block is:",
    place("12 N, directed opposite to the motion",
          ["zero, since the block is not accelerating", "more than 12 N, directed opposite to the motion",
           "12 N, directed along the motion"], "A"),
    "Newton's first law: constant velocity means zero net force",
    "The block moves with constant velocity, so its acceleration is zero and the net horizontal force on it is "
    "zero. The only horizontal forces are the pull and kinetic friction, so friction must be 12 N and opposite to "
    "the pull, i.e. opposite to the motion.",
    ["a = 0 → net horizontal force = 0", "12 N (pull) − f = 0 → f = 12 N, opposite to the motion"],
    why="Zero acceleration means zero net force, not zero friction; friction larger than 12 N would decelerate the "
        "block; kinetic friction opposes the relative sliding, so it cannot point along the motion.",
    ncert="Class 11 Physics, 'Laws of Motion', Newton's first law and friction", seconds=30)

assert close(40 / (10 * g), 0.4)
add(T, "Friction", "Basic", "numerical",
    "A block of mass 10 kg rests on a rough horizontal floor. The least horizontal force needed just to start it "
    "moving is 40 N. Taking g = 10 m/s², the coefficient of static friction between the block and the floor is:",
    place("0.4", ["4", "0.25", "2.5"], "D"),
    "Limiting static friction: f_s(max) = μₛN",
    "The force that just starts the motion equals the limiting value of static friction, μₛN, with N = mg on a "
    "horizontal floor.",
    ["N = mg = 10 × 10 = 100 N", "μₛ = 40/100 = 0.4"],
    why="4 divides the force by the mass instead of by the weight; 2.5 inverts the ratio (N/F); 0.25 divides the "
        "mass by the force.",
    ncert="Class 11 Physics, 'Laws of Motion', friction (limiting static friction)", seconds=30, recomputed=True)

mA, uA, mB = 2.0, 6.0, 1.0
vc = mA * uA / (mA + mB)
assert close(vc, 4.0) and close(mB * vc, 4.0) and close(mA * (uA - vc), 4.0)
add(T, "Conservation of linear momentum", "Intermediate", "numerical",
    "On a smooth horizontal floor, block A of mass 2 kg moves at 6 m/s directly away from block B of mass 1 kg, "
    "which is at rest. The blocks are connected by a light inextensible string that is initially slack. When the string becomes taut, the "
    "two blocks are jerked into moving together with a common velocity. The magnitude of the impulse of the "
    "tension on block B during the jerk is:",
    place("4 N s", ["6 N s", "2 N s", "12 N s"], "B"),
    "Impulsive tension: momentum of the system conserved, impulse = change in momentum",
    "During the very short jerk, the only horizontal forces are the equal and opposite tensions at the two ends of "
    "the string, which are internal to the system. The total momentum is conserved, which gives the common "
    "velocity. The impulse on B equals its change of momentum.",
    ["Momentum: 2 × 6 = (2 + 1)v → v = 4 m/s",
     "Impulse on B = 1 × (4 − 0) = 4 N s",
     "Check: impulse on A = 2 × (4 − 6) = −4 N s (equal and opposite)"],
    why="6 N s gives B the initial speed of A; 2 N s is the impulse that would bring B only to 2 m/s; 12 N s is the "
        "initial momentum of A.",
    seconds=80, recomputed=True)

m_tab, m_hang = 8.0, 2.0
assert close(m_hang / m_tab, 0.25)
add(T, "Friction", "Intermediate", "numerical",
    "A block of mass 8 kg rests on a rough horizontal table. It is tied to a light string that passes over a "
    "smooth, light pulley at the edge of the table and carries a hanging mass of 2 kg. The system stays at rest. "
    "The least coefficient of static friction between the block and the table for which this is possible is:",
    place("0.25", ["0.2", "4", "0.5"], "C"),
    "Equilibrium with static friction",
    "For the hanging mass at rest, the tension equals its weight. For the block at rest, static friction must "
    "balance this tension, and static friction cannot exceed μₛN with N equal to the block's weight.",
    ["T = 2g = 20 N", "Friction needed on the 8 kg block = 20 N",
     "20 ≤ μₛ × 8g = 80μₛ → μₛ ≥ 0.25"],
    why="0.2 divides by the total weight of both masses (100 N); 4 inverts the ratio; 0.5 halves the normal force.",
    seconds=60, recomputed=True)

m_b, mus, muk = 2.0, 0.5, 0.4
lim, kin = mus * m_b * g, muk * m_b * g
cases = {"A": (4, 4), "B": (9, 9), "C": (15, kin), "D": (20, muk * 3 * g)}
assert close(lim, 10) and close(kin, 8) and 4 < lim and 9 < lim and 15 > lim and 20 > mus * 3 * g
assert close(cases["D"][1], 12)
add(T, "Friction", "Intermediate", "match_list",
    match_stem("A block of mass 2 kg lies on a rough horizontal floor; the coefficients of static and kinetic "
               "friction are 0.5 and 0.4. Take g = 10 m/s². A horizontal force P is applied to it, starting from rest. "
               "Match List-I (situation) with List-II (magnitude of the friction force on the block, or on the "
               "block and load together).",
               ["P = 4 N", "P = 9 N", "P = 15 N",
                "P = 20 N, with a 1 kg load fixed on top of the block"],
               ["12 N", "9 N", "4 N", "8 N"]),
    match_options({"A": "III", "B": "II", "C": "IV", "D": "I"},
                  [{"A": "III", "B": "II", "C": "I", "D": "IV"}, {"A": "III", "B": "IV", "C": "II", "D": "I"},
                   {"A": "I", "B": "II", "C": "IV", "D": "III"}], "D"),
    "Static friction is self-adjusting; kinetic friction is μₖN",
    "Limiting friction = μₛN = 0.5 × 20 = 10 N. While P is below this, the block stays at rest and static friction "
    "equals P. Once P exceeds the limit, the block slides and friction is kinetic, μₖN, whatever P is.",
    ["P = 4 N < 10 N → at rest, f = 4 N (III)", "P = 9 N < 10 N → at rest, f = 9 N (II)",
     "P = 15 N > 10 N → slides, f = 0.4 × 20 = 8 N (IV)",
     "With the load N = 30 N, limit = 15 N < 20 N → slides, f = 0.4 × 30 = 12 N (I)"],
    why="Taking friction as μₛN = 10 N or μₖN = 8 N in every case, or keeping f = P after the block has started to "
        "slide, leads to the other codes.",
    ncert="Class 11 Physics, 'Laws of Motion', static and kinetic friction", seconds=90)

add(T, "Newton's laws and impulse", "Intermediate", "assertion_reason",
    AR_STEM.format(
        a="Newton's second law, in the form F = ma, is consistent with Newton's first law.",
        r="If the net external force on a body is zero, F = ma gives a = 0, so the body stays at rest or keeps "
          "moving with uniform velocity."),
    ar("A"),
    "Relation between the first and second laws",
    "NCERT points out that the second law is consistent with the first: setting F = 0 in F = ma gives a = 0, which "
    "is exactly the statement of the first law. R shows why A holds, so it is the correct explanation.",
    ["F = 0 → a = 0 → constant velocity (or rest)", "This is the content of the first law → A true, R explains A"],
    ncert="Class 11 Physics, 'Laws of Motion', Newton's second law of motion", seconds=40)

add(T, "Equilibrium of concurrent forces", "Intermediate", "statement_pair",
    SP_STEM.format(
        s1="If a particle is in equilibrium under the action of three concurrent forces, the three forces must lie "
           "in one plane.",
        s2="A particle can be in equilibrium under the action of just two forces of magnitudes 5 N and 3 N."),
    sp("C"),
    "Conditions for equilibrium of a particle",
    "Equilibrium requires the vector sum of the forces to be zero. With three forces, F₃ = −(F₁ + F₂), and F₁ + F₂ "
    "lies in the plane of F₁ and F₂, so F₃ lies in that plane too: Statement I is true. With two forces, "
    "equilibrium requires F₁ = −F₂, i.e. equal magnitudes; 5 N and 3 N can never cancel, so Statement II is false.",
    ["Three forces: F₃ = −(F₁ + F₂) lies in the plane of F₁ and F₂ → I true",
     "Two forces: need |F₁| = |F₂| and opposite → 5 N and 3 N cannot balance → II false"],
    ncert="Class 11 Physics, 'Laws of Motion', equilibrium of a particle", seconds=50)

m_c, vbelt, mu_c = 2.0, 4.0, 0.2
acc = mu_c * g
t_slip = vbelt / acc
x_block = 0.5 * acc * t_slip ** 2
x_belt = vbelt * t_slip
slip = x_belt - x_block
w_fric = 0.5 * m_c * vbelt ** 2
heat = mu_c * m_c * g * slip
assert close(acc, 2) and close(t_slip, 2) and close(slip, 4) and close(w_fric, 16) and close(heat, 16)
assert not close(x_block, 8) and close(x_block, 4)
truth = [True, True, True, True, False]
multi_key(truth, "abcd")
add(T, "Friction", "Advanced", "multi_statement",
    multi("A conveyor belt moves horizontally with a constant speed of 4 m/s. A block of mass 2 kg is placed gently "
          "(at rest) on it. The coefficient of kinetic friction between the block and the belt is 0.2. Taking "
          "g = 10 m/s², which of the following statements are correct?",
          ["The block's acceleration while it slips on the belt is 2 m/s².",
           "The block slips on the belt for 2 s.",
           "The distance the block slides relative to the belt is 4 m.",
           "The work done by friction on the block is +16 J.",
           "While it slips, the block moves 8 m relative to the ground."]),
    place("(a), (b), (c) and (d) only", ["(a), (b) and (e) only", "(a), (c), (d) and (e) only",
                                         "(b), (d) and (e) only"], "B"),
    "Kinetic friction accelerating a body to the speed of a moving surface",
    "Friction μₖmg acts forward on the block until it reaches the belt's speed. The block covers less ground "
    "than the belt in this time; the difference is the slip. Friction does positive work on the block equal to its "
    "gain of kinetic energy, while the heat produced is friction × relative sliding distance.",
    ["(a) a = μₖg = 2 m/s², true", "(b) t = 4/2 = 2 s, true",
     "(c) block moves ½ × 2 × 4 = 4 m, belt moves 4 × 2 = 8 m → slip = 4 m, true",
     "(d) W = ½ × 2 × 4² = 16 J, true",
     "(e) the block moves 4 m over the ground; 8 m is the distance moved by the belt → false"],
    why="(e) gives the belt's displacement (4 m/s × 2 s), not the block's; the block starts from rest and "
        "averages only 2 m/s while slipping. Every wrong option contains (e).",
    seconds=130, recomputed=True)

mu_ch = 0.25
f_max = mu_ch / (1 + mu_ch)
assert close(f_max, 0.2)
add(T, "Friction", "Advanced", "numerical",
    "A uniform chain lies straight on a rough horizontal table, perpendicular to the edge, with part of it hanging "
    "vertically over the edge. The coefficient of static friction between the chain and the table is 0.25. The "
    "largest fraction of the length of the chain that can hang over the edge without the chain beginning to "
    "slide is:",
    place("1/5", ["1/4", "1/3", "4/5"], "A"),
    "Limiting friction balancing the weight of the hanging part",
    "If a fraction f of the chain hangs, the weight of the hanging part, f Mg, pulls the chain. The part on the "
    "table, of weight (1 − f)Mg, can provide at most μₛ(1 − f)Mg of static friction. At the limit these are equal.",
    ["f Mg = μₛ (1 − f) Mg", "f = μₛ/(1 + μₛ) = 0.25/1.25 = 0.2 = 1/5"],
    why="1/4 sets f = μₛ, forgetting that only the part on the table presses on it; 1/3 uses μₛ/(1 − μₛ); 4/5 is "
        "the fraction that stays on the table.",
    seconds=90, recomputed=True)

th = math.atan2(3, 4)        # 37 degrees: sin 0.6 cos 0.8
a_w = g * math.tan(th)
N_rel = 1 / math.cos(th)
assert close(a_w, 7.5) and close(N_rel, 1.25) and close(g * math.sin(th), 6.0)
truth = [True, False, True, True, False]
multi_key(truth, "acd")
add(T, "Newton's laws and impulse", "Advanced", "multi_statement",
    multi("A block of mass m rests on the smooth inclined face of a wedge; the face makes 37° with the horizontal "
          "(sin 37° = 0.6, cos 37° = 0.8). The wedge is pushed along a horizontal floor with a constant acceleration "
          "a, directed horizontally towards the side that the inclined face looks towards, so that the block stays "
          "at rest relative to the wedge. Take g = 10 m/s². Which of the following statements are correct?",
          ["The normal force exerted by the wedge on the block is 1.25 mg.",
           "The net force on the block is zero.",
           "The required acceleration a (7.5 m/s²) does not depend on the mass of the block.",
           "If the wedge were instead moved with constant velocity, the block would slide down the face with an "
           "acceleration of 6 m/s² relative to the wedge.",
           "The normal force exerted by the wedge on the block is 0.8 mg."]),
    place("(a), (c) and (d) only", ["(a), (b) and (c) only", "(c), (d) and (e) only",
                                    "(b), (d) and (e) only"], "D"),
    "Newton's second law in the ground frame for a body accelerating with a wedge",
    "In the ground frame the block accelerates horizontally with a, so the net force on it is ma, horizontal. Only "
    "gravity and the normal force act (the face is smooth). The vertical component of N balances mg and the "
    "horizontal component supplies ma.",
    ["Vertical: N cos 37° = mg → N = mg/0.8 = 1.25 mg → (a) true, (e) false",
     "Horizontal: N sin 37° = ma → a = g tan 37° = 7.5 m/s², independent of m → (c) true",
     "The block accelerates, so the net force is ma ≠ 0 → (b) false",
     "Wedge moving uniformly (an inertial frame): block slides with g sin 37° = 6 m/s² → (d) true"],
    why="(b) confuses rest relative to the wedge with equilibrium; (e) is the normal force on a block resting on a "
        "fixed incline, where there is no horizontal acceleration.",
    seconds=130, recomputed=True)

# =====================================================================================================================
# Work, Energy and Power (B3 I4 A3)
# =====================================================================================================================
T = "Work, Energy and Power"

assert -2 * g * 5 == -100
add(T, "Work by constant and variable force", "Basic", "numerical",
    "A ball of mass 2 kg is thrown vertically upward and rises through 5 m. Taking g = 10 m/s², the work done on "
    "the ball by the force of gravity during this rise is:",
    place("−100 J", ["+100 J", "−10 J", "zero"], "B"),
    "Work done by a constant force: W = F d cos θ",
    "Gravity (mg, downward) and the displacement (5 m, upward) are opposite, so θ = 180° and the work done by "
    "gravity is negative.",
    ["F = mg = 20 N downward, d = 5 m upward, θ = 180°", "W = 20 × 5 × cos 180° = −100 J"],
    why="+100 J ignores the angle between force and displacement; −10 J leaves out g (uses m × h); zero would "
        "need the force to be perpendicular to the displacement.",
    seconds=30, recomputed=True)

add(T, "Power", "Basic", "direct",
    "For a machine whose power output P varies with time t, the area under its power–time (P–t) graph between two "
    "instants gives:",
    place("the work done by the machine in that interval",
          ["the force exerted by the machine", "the average power of the machine",
           "the rate of doing work at the later instant"], "D"),
    "Power as the rate of doing work",
    "Instantaneous power is P = dW/dt, so the work done between t₁ and t₂ is W = ∫P dt, which is the area under "
    "the P–t graph between those instants.",
    ["P = dW/dt → dW = P dt", "W = ∫ P dt = area under the P–t graph"],
    why="The average power is that area divided by the time interval, not the area itself; the rate of doing work "
        "at an instant is the ordinate P, not an area; force is not obtained from a P–t graph.",
    ncert="Class 11 Physics, 'Work, Energy and Power', power", seconds=25)

kk = 200.0
vals = {"A": 0.5 * kk * 0.1 ** 2, "B": 0.5 * kk * (0.2 ** 2 - 0.1 ** 2), "C": 0.5 * kk * 0.2 ** 2,
        "D": 0.5 * kk * 0.3 ** 2}
assert [round(v, 6) for v in vals.values()] == [1.0, 3.0, 4.0, 9.0]
add(T, "Spring potential energy", "Basic", "match_list",
    match_stem("An ideal spring has spring constant 200 N/m. Match List-I with List-II (the energy or work).",
               ["Potential energy stored when it is stretched 10 cm from its natural length",
                "Work needed to increase its extension slowly from 10 cm to 20 cm",
                "Potential energy stored when it is compressed 20 cm from its natural length",
                "Potential energy stored when it is stretched 30 cm from its natural length"],
               ["4 J", "9 J", "1 J", "3 J"]),
    match_options({"A": "III", "B": "IV", "C": "I", "D": "II"},
                  [{"A": "III", "B": "I", "C": "IV", "D": "II"}, {"A": "IV", "B": "III", "C": "I", "D": "II"},
                   {"A": "III", "B": "IV", "C": "II", "D": "I"}], "C"),
    "Elastic potential energy of a spring: U = ½kx²",
    "The energy stored depends on the square of the extension or compression x, measured from the natural length, "
    "and not on whether the spring is stretched or compressed. The work needed to go from x₁ to x₂ is the "
    "difference ½k(x₂² − x₁²).",
    ["U(10 cm) = ½ × 200 × 0.01 = 1 J (III)", "W(10 → 20 cm) = ½ × 200 × (0.04 − 0.01) = 3 J (IV)",
     "U(compressed 20 cm) = ½ × 200 × 0.04 = 4 J (I)", "U(30 cm) = ½ × 200 × 0.09 = 9 J (II)"],
    why="Taking the extra 10 cm as starting from the natural length gives 1 J for B; treating energy as "
        "proportional to x (not x²) gives the other codes.",
    ncert="Class 11 Physics, 'Work, Energy and Power', the potential energy of a spring", seconds=60)

# x = t^3/3 -> v = t^2
m4 = 2.0
v_at2 = 2.0 ** 2
assert close(0.5 * m4 * v_at2 ** 2, 16.0)
add(T, "Work-energy theorem", "Intermediate", "numerical",
    "A body of mass 2 kg, initially at rest at the origin, moves along the x-axis so that its position is x = t³/3, "
    "where x is in metres and t in seconds. The work done by the net force on it during the first 2 s is:",
    place("16 J", ["4 J", "32 J", "21.3 J"], "A"),
    "Work–energy theorem: W_net = ΔK",
    "The net work equals the change in kinetic energy, so only the speeds at the two instants are needed.",
    ["v = dx/dt = t² → v(0) = 0, v(2) = 4 m/s", "W = ½ × 2 × 4² − 0 = 16 J"],
    why="4 J takes v = t (2 m/s at t = 2 s) instead of t²; 32 J forgets the ½ in the kinetic energy; 21.3 J "
        "multiplies the force at t = 2 s (m × 2t = 8 N) by the displacement 8/3 m, but the force is not constant.",
    seconds=60, recomputed=True)

k5, x5, m5 = 800.0, 0.05, 0.1
E5 = 0.5 * k5 * x5 ** 2
assert close(E5, 1.0) and close(E5 / (m5 * g), 1.0)
add(T, "Spring potential energy", "Intermediate", "numerical",
    "A light vertical spring of spring constant 800 N/m is fixed to the floor and is held compressed by 5 cm from "
    "its natural length, with a ball of mass 0.1 kg resting on its top. The ball is released from rest and is "
    "thrown upward by the spring. Neglecting air resistance and taking g = 10 m/s², the maximum height to which "
    "the ball rises above its point of release is:",
    place("1 m", ["0.5 m", "2 m", "0.95 m"], "D"),
    "Conservation of mechanical energy: elastic potential energy → gravitational potential energy",
    "The energy stored by the 5 cm compression is ½kx². The light spring keeps no kinetic energy, and at the "
    "highest point the ball is momentarily at rest, so all this energy has become gravitational potential energy "
    "mgh, measured from the point of release (this already includes the 5 cm rise while the spring extends).",
    ["½kx² = ½ × 800 × (0.05)² = 1 J", "mgh = 1 J → h = 1/(0.1 × 10) = 1 m"],
    why="0.5 m forgets that the stored energy is already ½kx² and halves again; 2 m uses kx² without the ½; 0.95 m "
        "subtracts the 5 cm compression, but the height asked is measured from the release point itself.",
    seconds=70, recomputed=True)

P1, v1, v2_ = 10.0, 20.0, 40.0
P2 = P1 * (v2_ / v1) ** 3
assert close(P2, 80.0)
add(T, "Power", "Intermediate", "numerical",
    "A car moving at a steady 20 m/s on a level road needs 10 kW of engine power to overcome air resistance, which "
    "is proportional to the square of its speed. Ignoring all other resistance, the power needed to keep it moving "
    "at a steady 40 m/s is:",
    place("80 kW", ["40 kW", "20 kW", "160 kW"], "B"),
    "Power at constant velocity: P = Fv",
    "At steady speed the driving force equals the resistive force, F = bv². The power is P = Fv = bv³, so it "
    "grows as the cube of the speed.",
    ["P ∝ v³", "P₂ = 10 kW × (40/20)³ = 10 × 8 = 80 kW"],
    why="40 kW takes P ∝ v²; 20 kW takes P ∝ v; 160 kW takes P ∝ v⁴.",
    seconds=55, recomputed=True)

add(T, "Work-energy theorem", "Intermediate", "assertion_reason",
    AR_STEM.format(
        a="When a block slides down a rough inclined plane, the decrease in its gravitational potential energy is "
          "greater than the increase in its kinetic energy.",
        r="The kinetic friction on the block does negative work, so part of the mechanical energy is converted into "
          "heat (internal energy) at the sliding surfaces."),
    ar("A"),
    "Work–energy theorem with a non-conservative force",
    "By the work–energy theorem, ΔK = W_gravity + W_friction (the normal force does no work). W_gravity equals the "
    "loss of potential energy, and W_friction is negative, so ΔK is less than the loss of potential energy; the "
    "difference appears as heat. R gives exactly this cause.",
    ["ΔK = (−ΔU) + W_f", "W_f < 0 → ΔK < −ΔU → A true", "The negative work of friction is the cause → R explains A"],
    ncert="Class 11 Physics, 'Work, Energy and Power', the work–energy theorem and conservative forces",
    seconds=45)

L8, u8sq = 1.0, 35.0
cos_th = (2 * g * L8 - u8sq) / (3 * g * L8)
h_slack = L8 * (1 - cos_th)
assert close(cos_th, -0.5) and close(h_slack, 1.5) and close(u8sq / (2 * g), 1.75)
assert close(u8sq - 2 * g * h_slack, -g * L8 * cos_th)          # T = 0 there
add(T, "Motion in a vertical circle", "Advanced", "numerical",
    "A small stone tied to a light inextensible string 1.0 m long hangs at rest. It is given a horizontal speed of "
    "√35 m/s at the lowest point so that it moves in a vertical circle. Taking g = 10 m/s² and neglecting air "
    "resistance, the height above the lowest point at which the string becomes slack is:",
    place("1.5 m", ["1.75 m", "2.0 m", "1.25 m"], "C"),
    "Vertical circle: the string slackens where the tension becomes zero",
    "At an angle θ measured from the lowest position, energy conservation gives v² = u² − 2gL(1 − cos θ), and the "
    "radial equation gives T = mv²/L + mg cos θ. The string slackens where T = 0, which needs cos θ < 0 (above "
    "the horizontal through the centre).",
    ["T = 0 → v² = −gL cos θ", "u² − 2gL + 2gL cos θ = −gL cos θ → cos θ = (2gL − u²)/(3gL)",
     "cos θ = (20 − 35)/30 = −0.5 → θ = 120°", "Height above lowest point = L(1 − cos θ) = 1.5 m"],
    why="1.75 m is u²/2g, the height at which the speed would become zero, but the string slackens earlier while "
        "the stone still moves; 2.0 m is the top of the circle, which needs u² ≥ 5gL = 50; 1.25 m does not make "
        "the tension zero.",
    seconds=150, recomputed=True)

# constant power from rest: x proportional to t^(3/2)
ratio = (1 / 4) ** 1.5
assert close(ratio, 1 / 8)
add(T, "Power", "Advanced", "numerical",
    "A body starts from rest on a smooth horizontal surface and is pushed by a machine that delivers a constant "
    "power to it. The ratio of the distance it covers in the first 1 s to the distance it covers in the first 4 s "
    "is:",
    place("1 : 8", ["1 : 16", "1 : 4", "1 : 2"], "D"),
    "Constant power: kinetic energy grows linearly with time",
    "With constant power P and no losses, ½mv² = Pt, so v = √(2Pt/m) ∝ t^(1/2). Integrating, the distance is "
    "x ∝ t^(3/2).",
    ["½mv² = Pt → v ∝ √t", "x = ∫v dt ∝ t^(3/2)", "x₁/x₄ = (1/4)^(3/2) = 1/8"],
    why="1 : 16 assumes uniform acceleration (x ∝ t²); 1 : 4 takes x ∝ t; 1 : 2 takes x ∝ √t, which is how the "
        "speed (not the distance) grows.",
    seconds=100, recomputed=True)

# elastic head-on collisions in the limits
def elastic(m1, m2, u):
    return ((m1 - m2) * u / (m1 + m2), 2 * m1 * u / (m1 + m2))


v1h, v2h = elastic(1e6, 1.0, 1.0)
v1l, v2l = elastic(1.0, 1e6, 1.0)
assert close(v2h, 2.0, rel=1e-5) and close(v1l, -1.0, rel=1e-5) and (1e6 * v2l ** 2) / 1.0 < 1e-5
add(T, "Collisions", "Advanced", "statement_pair",
    SP_STEM.format(
        s1="When a very heavy body moving with speed u collides head-on and elastically with a very light body at "
           "rest, the light body moves off with a speed of nearly 2u.",
        s2="When a very light body moving with speed u collides head-on and elastically with a very heavy body at "
           "rest, the light body rebounds with a speed of nearly u and transfers nearly all of its kinetic energy "
           "to the heavy body."),
    sp("C"),
    "One-dimensional elastic collision with a target at rest: limiting cases",
    "For m₁ moving at u striking m₂ at rest: v₁ = (m₁ − m₂)u/(m₁ + m₂) and v₂ = 2m₁u/(m₁ + m₂). If m₁ ≫ m₂, "
    "v₂ ≈ 2u, so Statement I is true. If m₁ ≪ m₂, v₁ ≈ −u: the light body bounces back with almost its whole "
    "speed, so it keeps almost all its kinetic energy and the heavy body gains almost none. Statement II's second "
    "part is false.",
    ["m₁ ≫ m₂: v₂ = 2m₁u/(m₁ + m₂) → 2u → I true",
     "m₁ ≪ m₂: v₁ → −u, v₂ → 2m₁u/m₂ → 0 → kinetic energy transferred → 0 → II false"],
    ncert="Class 11 Physics, 'Work, Energy and Power', collisions in one dimension", seconds=70, recomputed=True)

# =====================================================================================================================
# Rotational Motion (B3 I5 A3)
# =====================================================================================================================
T = "Rotational Motion"

al = 2.0
rv = {"A": al * 3, "B": 0.5 * al * 9, "C": 0.5 * al * 9 - 0.5 * al * 4, "D": math.sqrt(2 * al * 16)}
assert [round(v, 9) for v in rv.values()] == [6.0, 9.0, 5.0, 8.0]
add(T, "Rigid-body rotation", "Basic", "match_list",
    match_stem("A wheel starts from rest and rotates about a fixed axis with a uniform angular acceleration of "
               "2 rad/s². Match List-I (quantity) with List-II (its value).",
               ["Angular speed at t = 3 s", "Angle turned through in the first 3 s",
                "Angle turned through during the third second (from t = 2 s to t = 3 s)",
                "Angular speed after it has turned through 16 rad"],
               ["8 rad/s", "5 rad", "9 rad", "6 rad/s"]),
    match_options({"A": "IV", "B": "III", "C": "II", "D": "I"},
                  [{"A": "I", "B": "III", "C": "II", "D": "IV"}, {"A": "IV", "B": "II", "C": "III", "D": "I"},
                   {"A": "IV", "B": "III", "C": "I", "D": "II"}], "B"),
    "Kinematic equations of rotational motion with constant angular acceleration",
    "With ω₀ = 0 and constant α: ω = αt, θ = ½αt² and ω² = 2αθ. These are the rotational analogues of the "
    "equations of uniformly accelerated linear motion.",
    ["ω(3) = 2 × 3 = 6 rad/s (IV)", "θ(3) = ½ × 2 × 9 = 9 rad (III)", "θ(3) − θ(2) = 9 − 4 = 5 rad (II)",
     "ω² = 2 × 2 × 16 = 64 → ω = 8 rad/s (I)"],
    why="Confusing the angle in the first 3 s with the angle in the third second, or the angular speed at 3 s with "
        "that after 16 rad, gives the other codes.",
    ncert="Class 11 Physics, 'System of Particles and Rotational Motion', kinematics of rotational motion about a "
          "fixed axis", seconds=70)

add(T, "Centre of mass", "Basic", "direct",
    "The centre of gravity of a body coincides with its centre of mass when:",
    place("the acceleration due to gravity has the same value at all points of the body",
          ["the body is a rigid body of any size", "the body is at rest",
           "the body is symmetrical about a vertical axis"], "A"),
    "Centre of gravity and centre of mass",
    "The centre of gravity is the point about which the total gravitational torque on the body is zero. If g is "
    "the same at every point of the body, this condition becomes Σmᵢrᵢ = 0 about that point, which defines the "
    "centre of mass. For bodies small compared with the Earth this holds, so the two points coincide.",
    ["Σ rᵢ × mᵢg = 0 about the centre of gravity", "g uniform → (Σmᵢrᵢ) × g = 0 → Σmᵢrᵢ = 0 → centre of mass"],
    why="Rigidity, rest or symmetry about a vertical axis do not make the weights of all parts proportional to "
        "their masses; only a uniform g does.",
    ncert="Class 11 Physics, 'System of Particles and Rotational Motion', centre of gravity", seconds=30)

I3, w1, w2 = 2.0, 10.0, 20.0
assert close(0.5 * I3 * (w2 ** 2 - w1 ** 2), 300.0)
add(T, "Rigid-body rotation", "Basic", "numerical",
    "A flywheel has a moment of inertia of 2 kg m² about its axle. The work needed to increase its angular speed "
    "from 10 rad/s to 20 rad/s is:",
    place("300 J", ["100 J", "400 J", "600 J"], "D"),
    "Work–energy theorem for rotation: W = ΔK = ½I(ω₂² − ω₁²)",
    "The work done by the torque equals the change in rotational kinetic energy.",
    ["K₁ = ½ × 2 × 100 = 100 J", "K₂ = ½ × 2 × 400 = 400 J", "W = 400 − 100 = 300 J"],
    why="100 J uses ½I(ω₂ − ω₁)²; 400 J is the final kinetic energy alone; 600 J forgets the ½.",
    seconds=35, recomputed=True)

add(T, "Moment of inertia and axis theorems", "Intermediate", "direct",
    "Of all the axes parallel to a given direction, the moment of inertia of a rigid body is the least about the "
    "axis that:",
    place("passes through its centre of mass",
          ["is farthest from its centre of mass", "touches the surface of the body",
           "passes through its heaviest part, whatever the position of the centre of mass"], "B"),
    "Theorem of parallel axes",
    "By the theorem of parallel axes, I = I_cm + Md², where d is the distance of the axis from the parallel axis "
    "through the centre of mass. Since Md² ≥ 0, I is least when d = 0, i.e. for the axis through the centre of "
    "mass.",
    ["I = I_cm + Md²", "Md² is smallest (zero) for d = 0 → axis through the centre of mass"],
    why="Moving the axis away from the centre of mass only adds Md²; a tangent is a particular parallel axis at "
        "d > 0, so it cannot give the minimum.",
    ncert="Class 11 Physics, 'System of Particles and Rotational Motion', theorem of parallel axes", seconds=35)

M5, L5, m5p = 3.0, 2.0, 1.0
I5 = M5 * L5 ** 2 / 12 + 2 * m5p * (L5 / 2) ** 2
assert close(I5, 3.0)
add(T, "Moment of inertia and axis theorems", "Intermediate", "numerical",
    "A thin uniform rod of mass 3 kg and length 2 m carries a small ball of mass 1 kg fixed at each end. The moment "
    "of inertia of this system about an axis perpendicular to the rod through its midpoint is:",
    place("3 kg m²", ["1 kg m²", "2 kg m²", "5 kg m²"], "C"),
    "Moment of inertia of a composite body: add the parts about the same axis",
    "The rod contributes ML²/12 about its perpendicular bisector; each ball, a point mass at distance L/2, "
    "contributes m(L/2)².",
    ["Rod: 3 × 4/12 = 1 kg m²", "Balls: 2 × 1 × 1² = 2 kg m²", "Total = 3 kg m²"],
    why="1 kg m² is the rod alone; 2 kg m² is the balls alone; 5 kg m² uses ML²/3 for the rod (axis at an end).",
    seconds=55, recomputed=True)

Ip, Rp, mc, vc_ = 200.0, 2.0, 50.0, 4.0
Lc = mc * vc_ * Rp
w_f = Lc / (Ip + mc * Rp ** 2)
K_i, K_f = 0.5 * mc * vc_ ** 2, 0.5 * (Ip + mc * Rp ** 2) * w_f ** 2
assert close(w_f, 1.0) and close(K_i - K_f, 200.0) and close(mc * w_f * Rp, 100.0)
truth = [True, True, False, False, True]
multi_key(truth, "abe")
add(T, "Torque and angular momentum", "Intermediate", "multi_statement",
    multi("A horizontal platform with moment of inertia 200 kg m² about its vertical axle is at rest and can turn "
          "freely. A child of mass 50 kg runs at 4 m/s along a tangent to the rim (radius 2 m) and jumps onto the "
          "rim. Treat the child as a particle. Which of the following statements are correct?",
          ["The platform and child then rotate with an angular speed of 1 rad/s.",
           "The angular momentum of the child–platform system about the axle is conserved during the jump.",
           "The kinetic energy of the system is conserved during the jump.",
           "The linear momentum of the child–platform system is conserved during the jump.",
           "200 J of kinetic energy is lost in the process."]),
    place("(a), (b) and (e) only", ["(a), (b), (c) and (d) only", "(a), (c) and (d) only",
                                    "(b), (d) and (e) only"], "D"),
    "Conservation of angular momentum about a fixed axis",
    "The axle can exert forces but no torque about itself, so angular momentum about the axle is conserved. The "
    "child's angular momentum about the axle is mvR. The child 'sticks' to the platform, so kinetic energy is not "
    "conserved. Linear momentum is not conserved either, because the axle exerts an external horizontal force.",
    ["L = mvR = 50 × 4 × 2 = 400 kg m² s⁻¹", "I_total = 200 + 50 × 2² = 400 kg m² → ω = 1 rad/s → (a) true",
     "No external torque about the axle → (b) true",
     "K before = ½ × 50 × 16 = 400 J; K after = ½ × 400 × 1 = 200 J → (c) false, (e) true",
     "Momentum before 200 kg m/s; after, only the child moves (at ωR = 2 m/s) → 100 kg m/s → (d) false"],
    why="(c) treats the jump as elastic; (d) ignores the force exerted by the fixed axle on the platform.",
    ncert="Class 11 Physics, 'System of Particles and Rotational Motion', conservation of angular momentum",
    seconds=130, recomputed=True)

add(T, "Centre of mass", "Intermediate", "assertion_reason",
    AR_STEM.format(
        a="When a shell fired from a gun explodes in mid-air, the centre of mass of its fragments continues to move "
          "along the same parabolic path that the unexploded shell would have followed (until a fragment hits the "
          "ground).",
        r="The forces of the explosion are internal to the system of fragments, and the only external force, the "
          "total weight, is unchanged, so the acceleration of the centre of mass stays equal to g."),
    ar("A"),
    "Motion of the centre of mass of a system: M a_cm = F_ext",
    "The centre of mass of a system moves as a particle of mass M acted on by the total external force. Internal "
    "forces, however large, cancel in pairs. Since the external force (gravity) is the same before and after the "
    "explosion, the centre of mass keeps the same acceleration and hence the same trajectory. R gives this cause, "
    "so it explains A.",
    ["M a_cm = F_ext = Mg before and after the explosion", "Internal forces cancel → path of CM unchanged"],
    ncert="Class 11 Physics, 'System of Particles and Rotational Motion', motion of centre of mass", seconds=45)

Mx, Rx = 1.0, 1.0
I_tan_in = Mx * Rx ** 2 / 4 + Mx * Rx ** 2
I_tan_perp = Mx * Rx ** 2 / 2 + Mx * Rx ** 2
assert I_tan_in < I_tan_perp and close(math.sqrt((Mx * Rx ** 2 / 2) / Mx), Rx / math.sqrt(2))
add(T, "Moment of inertia and axis theorems", "Intermediate", "statement_pair",
    SP_STEM.format(
        s1="For a uniform circular disc, the moment of inertia about a tangent lying in its plane is smaller than "
           "the moment of inertia about a tangent perpendicular to its plane.",
        s2="The radius of gyration of a thin uniform ring of radius R about any of its diameters is R/√2."),
    sp("A"),
    "Theorems of parallel and perpendicular axes for a disc and a ring",
    "For a disc, I about a diameter is MR²/4 and about the central perpendicular axis MR²/2. Adding MR² by the "
    "parallel-axes theorem gives 5MR²/4 for a tangent in the plane and 3MR²/2 for a tangent perpendicular to the "
    "plane, so Statement I is true. For a ring, I about the central axis is MR², and by the perpendicular-axes "
    "theorem I about a diameter is MR²/2 = Mk², giving k = R/√2: Statement II is true.",
    ["Disc: tangent in plane = MR²/4 + MR² = 1.25 MR²; tangent ⊥ plane = MR²/2 + MR² = 1.5 MR² → I true",
     "Ring: I_diameter = MR²/2 → k = R/√2 → II true"],
    ncert="Class 11 Physics, 'System of Particles and Rotational Motion', theorems of perpendicular and parallel "
          "axes", seconds=70, recomputed=True)

al9 = 4.0
t9 = 1 / math.sqrt(al9)
assert close(t9, 0.5) and close((al9 * t9) ** 2, al9)            # omega^2 r = alpha r
add(T, "Rigid-body rotation", "Advanced", "numerical",
    "A wheel starts from rest and rotates about a fixed axle with a constant angular acceleration of 4 rad/s². At "
    "what time after the start does the total acceleration of a point on its rim make an angle of 45° with the "
    "radius through that point?",
    place("0.5 s", ["0.25 s", "1 s", "2 s"], "B"),
    "Tangential and centripetal components of acceleration in non-uniform rotation",
    "A point at distance r has a tangential acceleration αr (constant) and a centripetal acceleration ω²r directed "
    "along the radius. The total acceleration makes 45° with the radius when the two components are equal.",
    ["a_t = αr, a_c = ω²r = α²t²r", "a_t = a_c → α = α²t² → t² = 1/α", "t = 1/√4 = 0.5 s"],
    why="0.25 s takes t = 1/α; 1 s and 2 s give a centripetal component 4 and 16 times the tangential one.",
    seconds=90, recomputed=True)

W10 = 60 * math.sqrt(3)
T10 = W10 * 0.5 * math.cos(math.radians(60)) / math.sin(math.radians(60))
assert close(T10, 30.0) and close(W10 * 0.5 * math.tan(math.radians(60)), 90.0)
add(T, "Equilibrium of rigid bodies", "Advanced", "numerical",
    "A uniform rod of weight 60√3 N has its lower end hinged smoothly to the floor. It is held at rest at 60° to "
    "the horizontal by a light horizontal string tied to its upper end and fixed to a vertical wall. The tension in "
    "the string is:",
    place("30 N", ["90 N", "60√3 N", "30√3 N"], "A"),
    "Rotational equilibrium: net torque about the hinge is zero",
    "Take torques about the hinge, so the unknown hinge force has no moment. The weight acts at the midpoint, at a "
    "horizontal distance (L/2) cos 60° from the hinge; the horizontal tension acts at the top, at a height "
    "L sin 60° above the hinge.",
    ["Torque of weight = W (L/2) cos 60°", "Torque of tension = T L sin 60°",
     "T = W cos 60°/(2 sin 60°) = W/(2√3) = 60√3/(2√3) = 30 N"],
    why="90 N interchanges sine and cosine (uses the rod's angle with the vertical); 60√3 N takes the tension equal "
        "to the weight; 30√3 N takes it as half the weight, ignoring the geometry.",
    seconds=110, recomputed=True)

I11 = 2.0
tau = I11 * 6 * 2           # omega = 3t^2 -> alpha = 6t
om = 3 * 2 ** 2
assert tau == 24 and om == 12 and tau * om == 288
add(T, "Torque and angular momentum", "Advanced", "numerical",
    "The angular velocity of a wheel of moment of inertia 2 kg m² about its fixed axle varies with time as "
    "ω = 3t², where ω is in rad/s and t in seconds. The power delivered by the net torque on the wheel at t = 2 s "
    "is:",
    place("288 W", ["144 W", "24 W", "576 W"], "C"),
    "Rotational power: P = τω, with τ = I dω/dt",
    "The torque is found from the angular acceleration, and the instantaneous power is the product of torque and "
    "angular velocity. (Equivalently, P = dK/dt with K = ½Iω².)",
    ["α = dω/dt = 6t → at t = 2 s, α = 12 rad/s²", "τ = Iα = 24 N m", "ω(2) = 12 rad/s",
     "P = τω = 24 × 12 = 288 W"],
    shortcut="K = ½ × 2 × 9t⁴ = 9t⁴ → P = dK/dt = 36t³ = 288 W at t = 2 s.",
    why="144 W is the kinetic energy at t = 2 s, not its rate of change; 24 W is the torque value; 576 W takes "
        "K = Iω² (forgetting the ½) before differentiating.",
    seconds=90, recomputed=True)

# =====================================================================================================================
# Gravitation (B2 I3 A2)
# =====================================================================================================================
T = "Gravitation"

# g = (4/3) pi G rho R ; v_e = sqrt(2 g R)
g_ratio = 2 * 0.5
ve_ratio = math.sqrt(g_ratio * 0.5)
assert close(g_ratio, 1.0) and close(ve_ratio, 1 / math.sqrt(2))
add(T, "Variation of g", "Basic", "statement_pair",
    SP_STEM.format(
        s1="For a planet that is a uniform sphere of density ρ and radius R, the acceleration due to gravity at its "
           "surface is proportional to the product ρR.",
        s2="A planet with twice the mean density of the Earth and half its radius has the same escape speed from "
           "its surface as the Earth."),
    sp("C"),
    "g and escape speed in terms of density and radius",
    "With M = (4/3)πR³ρ, g = GM/R² = (4/3)πGρR, so Statement I is true. For the planet, ρR is unchanged, so g is "
    "the same as on the Earth; but the escape speed is √(2gR), and R is halved, so the escape speed is 1/√2 times "
    "the Earth's. Statement II is false.",
    ["g = GM/R² = (4/3)πGρR ∝ ρR → I true", "Planet: ρR same → g same",
     "vₑ = √(2gR) → R halved → vₑ becomes vₑ/√2 → II false"],
    ncert="Class 11 Physics, 'Gravitation', acceleration due to gravity of the Earth and escape speed",
    seconds=60, recomputed=True)

add(T, "Variation of g", "Basic", "direct",
    "A body is taken to the centre of the Earth (treated as a uniform sphere). There, its mass and its weight are "
    "respectively:",
    place("unchanged, and zero",
          ["zero, and zero", "unchanged, and infinite", "unchanged, and unchanged"], "B"),
    "Variation of g with depth",
    "Mass is the amount of matter and does not depend on location. Inside a uniform Earth, g(d) = g(1 − d/R), "
    "which becomes zero at d = R (the centre). The weight mg is therefore zero there.",
    ["g(d) = g(1 − d/R) → g(R) = 0", "Weight = m × 0 = 0; mass unchanged"],
    why="Mass never becomes zero by moving a body; g does not become infinite at the centre (the 1/r² law holds "
        "only outside the Earth); the weight does change because g changes with depth.",
    ncert="Class 11 Physics, 'Gravitation', acceleration due to gravity below the surface of the Earth",
    seconds=25)

R_, gS = 1.0, 1.0
r2 = 2 * R_
GM = gS * R_ ** 2
v_o = math.sqrt(GM / r2)
acc_o = GM / r2 ** 2
T_o = 2 * math.pi * r2 / v_o
v_esc = math.sqrt(2 * GM / r2)
assert close(v_o, math.sqrt(0.5)) and close(acc_o, 0.25) and close(T_o, 4 * math.pi * math.sqrt(2)) \
    and close(v_esc, 1.0)
add(T, "Satellite energy and period", "Intermediate", "match_list",
    match_stem("A satellite revolves round the Earth in a circular orbit at a height above the surface equal to the "
               "Earth's radius R. Take g as the acceleration due to gravity at the Earth's surface and ignore the "
               "Earth's rotation. Match List-I (quantity for the satellite) with List-II (its value).",
               ["Orbital speed", "Acceleration of the satellite", "Period of revolution",
                "Speed needed at that height to escape from the Earth"],
               ["√(gR)", "g/4", "√(gR/2)", "4π√(2R/g)"]),
    match_options({"A": "III", "B": "II", "C": "IV", "D": "I"},
                  [{"A": "I", "B": "II", "C": "IV", "D": "III"}, {"A": "III", "B": "IV", "C": "II", "D": "I"},
                   {"A": "III", "B": "II", "C": "I", "D": "IV"}], "D"),
    "Satellite in a circular orbit of radius r = 2R, with GM = gR²",
    "The orbit radius is r = R + R = 2R. Use GM = gR². The orbital speed is √(GM/r), the acceleration is the local "
    "gravitational field GM/r², the period is 2πr/v, and the escape speed from distance r is √(2GM/r).",
    ["v₀ = √(gR²/2R) = √(gR/2) (III)", "a = GM/r² = gR²/4R² = g/4 (II)",
     "T = 2π(2R)/√(gR/2) = 4π√(2R/g) (IV)", "vₑ(r) = √(2gR²/2R) = √(gR) (I)"],
    shortcut="At the same distance, escape speed = √2 × orbital speed.",
    why="Interchanging the orbital speed with the escape speed, or using g/2 (dividing by r instead of r²) for "
        "the acceleration, gives the other codes.",
    ncert="Class 11 Physics, 'Gravitation', earth satellites and escape speed", seconds=100)

# masses m at (-3,0) and (3,0); point (0,4)
E_each = 1 / 25
E_y = 2 * E_each * (4 / 5)
assert close(E_y, 8 / 125)
add(T, "Law of gravitation", "Intermediate", "numerical",
    "Two point masses, each of mass m, are fixed at the points (−3 m, 0) and (3 m, 0). G is the universal "
    "gravitational constant. The magnitude of the gravitational field (intensity) due to them at the point "
    "(0, 4 m) is:",
    place("8Gm/125", ["6Gm/125", "2Gm/25", "zero"], "A"),
    "Superposition of gravitational fields (vector addition)",
    "Each mass is 5 m from the point, so each field has magnitude Gm/25 and points towards its mass. The "
    "x-components cancel by symmetry; the y-components (towards the line joining the masses) add.",
    ["Distance = √(3² + 4²) = 5 m → each field = Gm/25", "Component along −y of each = (Gm/25)(4/5)",
     "Resultant = 2 × (Gm/25) × (4/5) = 8Gm/125, directed towards the origin"],
    why="6Gm/125 adds the x-components (cos factor 3/5) instead of the y-components; 2Gm/25 adds the magnitudes "
        "as if the fields were parallel; zero would hold only at the midpoint of the line joining the masses.",
    seconds=80, recomputed=True)

add(T, "Gravitational potential and energy", "Intermediate", "assertion_reason",
    AR_STEM.format(
        a="Taking the gravitational potential energy to be zero at infinity, the potential energy of a body of "
          "mass m at a height equal to the Earth's radius R above the surface is −mgR/2, where g is the "
          "acceleration due to gravity at the surface.",
        r="The acceleration due to gravity at a height R above the Earth's surface is g/2."),
    ar("C"),
    "Gravitational potential energy at a distance r: U = −GMm/r",
    "At height R, r = 2R and U = −GMm/(2R) = −gR²m/(2R) = −mgR/2, so A is true. The acceleration due to gravity "
    "there is GM/(2R)² = g/4, not g/2, so R is false. (The potential falls off as 1/r, the field as 1/r².)",
    ["U = −GMm/(2R), GM = gR² → U = −mgR/2 → A true", "g(2R) = GM/4R² = g/4 → R false"],
    ncert="Class 11 Physics, 'Gravitation', gravitational potential energy and acceleration due to gravity above "
          "the surface", seconds=50)

ve_ratio2, g_ratio2 = 2.0, 1.0
Rp = ve_ratio2 ** 2 / g_ratio2           # v_e^2 = 2 g R
Mp = g_ratio2 * Rp ** 2                  # M = g R^2 / G
assert close(Rp, 4) and close(Mp, 16)
add(T, "Escape and orbital velocity", "Advanced", "numerical",
    "On the surface of a planet, the acceleration due to gravity is the same as on the Earth's surface, but the "
    "escape speed is twice that from the Earth. Treating both as uniform spheres and ignoring rotation, the mass of "
    "the planet is (Mₑ = mass of the Earth):",
    place("16 Mₑ", ["4 Mₑ", "8 Mₑ", "2 Mₑ"], "B"),
    "Escape speed vₑ = √(2gR) and surface gravity g = GM/R²",
    "Write the escape speed in terms of g and R. With g the same, a doubled escape speed needs a radius four times "
    "larger. Then M = gR²/G grows as R².",
    ["vₑ = √(2gR) → 2 = √(Rₚ/Rₑ) → Rₚ = 4Rₑ", "M = gR²/G → Mₚ/Mₑ = (Rₚ/Rₑ)² = 16"],
    why="4 Mₑ takes M ∝ R (stops after finding the radius); 8 Mₑ assumes the radius is only doubled "
        "and the density unchanged (M ∝ R³); 2 Mₑ takes M proportional to the escape speed.",
    seconds=90, recomputed=True)

m1, m2 = 1.0, 4.0
v1sq = 2 * m1 * m2 / (m1 * (1 + m1 / m2))      # in units of G m / r with m = 1
assert close(v1sq, 32 / 5)
assert close((1 + 1 / 4) ** 2 * v1sq, 10.0)    # relative speed squared
add(T, "Gravitational potential and energy", "Advanced", "numerical",
    "Two particles of masses m and 4m are initially at rest very far apart in free space. They move towards each "
    "other only because of their mutual gravitational attraction. When the distance between them is r, the speed of "
    "the particle of mass m is (G is the universal gravitational constant):",
    place("√(32Gm/5r)", ["√(8Gm/r)", "√(10Gm/r)", "√(8Gm/5r)"], "D"),
    "Conservation of linear momentum and of energy for two gravitating particles",
    "No external force acts, so the total momentum stays zero: m v₁ = 4m v₂. The gain in total kinetic energy "
    "equals the loss of gravitational potential energy, G(m)(4m)/r.",
    ["Momentum: v₂ = v₁/4", "Energy: ½mv₁² + ½(4m)(v₁/4)² = 4Gm²/r",
     "½mv₁² (1 + 1/4) = 4Gm²/r → v₁² = 32Gm/(5r)"],
    why="√(8Gm/r) gives all the energy to the lighter particle (ignores the heavy one's kinetic energy); √(10Gm/r) "
        "is their relative speed, (5/4)v₁; √(8Gm/5r) takes the potential energy as Gm²/r, forgetting the "
        "factor 4.",
    seconds=120, recomputed=True)

# =====================================================================================================================
# Properties of Solids and Liquids (B4 I6 A4)
# =====================================================================================================================
T = "Properties of Solids and Liquids"

stress = 100 / 2e-6
strain = 1e-3 / 4
assert close(stress, 5e7) and close(strain, 2.5e-4) and close(stress / strain, 2e11)
add(T, "Elasticity and moduli", "Basic", "numerical",
    "A wire 4 m long with a cross-sectional area of 2 mm² is stretched by 1 mm when a force of 100 N is applied "
    "along its length. Young's modulus of the material of the wire is:",
    place("2 × 10¹¹ N/m²", ["5 × 10¹⁰ N/m²", "2 × 10⁸ N/m²", "8 × 10¹¹ N/m²"], "C"),
    "Young's modulus Y = (F/A)/(ΔL/L)",
    "Young's modulus is the ratio of the tensile stress to the longitudinal strain, within the elastic limit.",
    ["Stress = 100/(2 × 10⁻⁶) = 5 × 10⁷ N/m²", "Strain = 1 × 10⁻³/4 = 2.5 × 10⁻⁴",
     "Y = 5 × 10⁷/2.5 × 10⁻⁴ = 2 × 10¹¹ N/m²"],
    why="5 × 10¹⁰ N/m² forgets to divide the extension by the length 4 m (uses strain 10⁻³); 2 × 10⁸ N/m² puts "
        "the extension in millimetres (1) instead of metres; 8 × 10¹¹ N/m² multiplies by the length twice.",
    seconds=40, recomputed=True)

S2, dA = 0.03, 0.10 * (0.08 - 0.06)
W2 = 2 * S2 * dA
assert close(W2, 1.2e-4)
add(T, "Surface tension and capillarity", "Basic", "numerical",
    "A soap film is held in a rectangular wire frame of size 10 cm × 6 cm. One side of the frame is moved slowly so "
    "that the film becomes 10 cm × 8 cm, at constant temperature. The surface tension of the soap solution is "
    "0.03 N/m. The work done in stretching the film is:",
    place("1.2 × 10⁻⁴ J", ["6.0 × 10⁻⁵ J", "2.4 × 10⁻⁴ J", "1.2 × 10⁻² J"], "A"),
    "Surface energy: work = surface tension × increase in surface area",
    "Surface tension equals the surface energy per unit area. A soap film has two surfaces, front and back, so the "
    "total new surface area is twice the increase in the area of the frame.",
    ["Increase in frame area = 10 cm × 2 cm = 20 cm² = 2 × 10⁻³ m²",
     "Increase in surface area = 2 × 2 × 10⁻³ = 4 × 10⁻³ m²", "W = 0.03 × 4 × 10⁻³ = 1.2 × 10⁻⁴ J"],
    why="6.0 × 10⁻⁵ J counts only one surface; 2.4 × 10⁻⁴ J counts four surfaces; 1.2 × 10⁻² J leaves the area in "
        "cm² while using S in N/m.",
    ncert="Class 11 Physics, 'Mechanical Properties of Fluids', surface energy and surface tension", seconds=50,
    recomputed=True)

add(T, "Bernoulli's principle", "Basic", "direct",
    "For the steady, streamline flow of an ideal (incompressible, non-viscous) liquid through a horizontal pipe of "
    "varying cross-section, Bernoulli's equation takes the form:",
    place("P + ½ρv² = constant along a streamline",
          ["P + ρgh = constant, whatever the speed", "Pv = constant along a streamline",
           "P − ½ρv² = constant along a streamline"], "D"),
    "Bernoulli's equation for a horizontal streamline",
    "Bernoulli's principle states that P + ½ρv² + ρgh is the same at all points along a streamline in steady flow "
    "of an ideal fluid. In a horizontal pipe the height h is the same everywhere, so P + ½ρv² is constant: where "
    "the liquid moves faster, its pressure is lower.",
    ["P + ½ρv² + ρgh = constant (Bernoulli)", "Horizontal pipe: ρgh same everywhere → P + ½ρv² = constant"],
    why="P + ρgh = constant is the law for a liquid at rest; Pv = constant has no basis (pressure and speed are "
        "not inversely proportional); P − ½ρv² would make the pressure rise where the liquid speeds up.",
    ncert="Class 11 Physics, 'Mechanical Properties of Fluids', Bernoulli's principle", seconds=25)

P0, rho_w = 1.0e5, 1000.0
h4 = P0 / (rho_w * g)
assert close(h4, 10.0)
add(T, "Fluid pressure and Pascal's law", "Basic", "numerical",
    "Taking the atmospheric pressure as 1.0 × 10⁵ Pa, the density of water as 1000 kg/m³ and g = 10 m/s², the depth "
    "below the surface of a lake at which the absolute pressure is twice the atmospheric pressure is:",
    place("10 m", ["20 m", "5 m", "1 m"], "B"),
    "Pressure at a depth: P = P₀ + ρgh",
    "The absolute pressure at depth h is the atmospheric pressure plus the pressure of the water column above. It "
    "is 2P₀ when the water column alone supplies P₀.",
    ["2P₀ = P₀ + ρgh → ρgh = P₀", "h = 1.0 × 10⁵/(1000 × 10) = 10 m"],
    why="20 m makes the gauge pressure (ρgh) equal to 2P₀, forgetting the atmosphere's own contribution; 5 m halves "
        "it; 1 m drops a factor of 10.",
    ncert="Class 11 Physics, 'Mechanical Properties of Fluids', pressure (variation with depth)", seconds=35,
    recomputed=True)

r1, S1 = 0.5e-3, 0.07
mass1 = 2 * (22 / 7) * r1 * S1 / g
assert close(mass1, 2.2e-5)
add(T, "Surface tension and capillarity", "Intermediate", "numerical",
    "A clean glass capillary tube of internal radius 0.5 mm is dipped vertically in water. The surface tension of "
    "water is 0.07 N/m and the angle of contact is zero. Taking g = 10 m/s² and π = 22/7, the mass of water "
    "raised in the tube above the outside water level (neglecting the small amount in the meniscus) is:",
    place("22 mg", ["11 mg", "44 mg", "2.2 mg"], "D"),
    "Equilibrium of the raised liquid column: upward surface-tension force = weight of column",
    "Around the circular line of contact of length 2πr, surface tension pulls the liquid up with a force "
    "2πrS cos θ. In equilibrium this balances the weight mg of the raised column, so m = 2πrS cos θ/g, "
    "independent of the density and of the height.",
    ["Upward force = 2πrS = 2 × (22/7) × 0.5 × 10⁻³ × 0.07 = 2.2 × 10⁻⁴ N",
     "m = 2.2 × 10⁻⁴/10 = 2.2 × 10⁻⁵ kg = 22 mg"],
    why="11 mg uses πrS (only half the contact line); 44 mg uses the diameter in 2πr; 2.2 mg slips a power of ten "
        "in converting kg to mg.",
    seconds=80, recomputed=True)

Q2 = 0.84 * 400 * 100
assert close(Q2 / 3.36e5, 0.1)
add(T, "Thermal expansion and calorimetry", "Intermediate", "numerical",
    "A metal block of mass 0.84 kg and specific heat capacity 400 J kg⁻¹ K⁻¹, at 100 °C, is placed in a cavity in a "
    "large block of ice at 0 °C, and the cavity is closed. The latent heat of fusion of ice is 3.36 × 10⁵ J/kg. "
    "Assuming no heat is lost, the mass of ice that melts is:",
    place("100 g", ["10 g", "1 kg", "50 g"], "B"),
    "Calorimetry: heat lost by the hot body = heat used to melt ice",
    "The large block of ice stays at 0 °C, so the metal cools to 0 °C. All the heat it gives out melts ice at "
    "0 °C, without changing its temperature.",
    ["Heat given by metal = 0.84 × 400 × (100 − 0) = 33 600 J", "Mass melted = 33 600/(3.36 × 10⁵) = 0.1 kg = 100 g"],
    why="10 g and 1 kg slip a power of ten; 50 g takes the metal to cool only to 50 °C.",
    seconds=55, recomputed=True)

Y3, A3w, L3w, x3 = 2e11, 1e-6, 2.0, 1e-3
k3 = Y3 * A3w / L3w
W3 = 0.5 * k3 * x3 ** 2
assert close(k3, 1e5) and close(W3, 0.05)
add(T, "Elasticity and moduli", "Intermediate", "numerical",
    "A steel wire 2 m long with a cross-sectional area of 1 mm² is stretched by 1 mm within its elastic limit. "
    "Young's modulus of steel is 2 × 10¹¹ N/m². The elastic potential energy stored in the wire is:",
    place("0.05 J", ["0.1 J", "0.025 J", "0.5 J"], "C"),
    "Elastic potential energy of a stretched wire: U = ½ × force × extension",
    "Within the elastic limit the wire behaves like a spring of force constant k = YA/L. The work done in "
    "stretching it, stored as elastic energy, is ½kx² (equivalently ½ × stress × strain × volume).",
    ["k = YA/L = 2 × 10¹¹ × 10⁻⁶/2 = 10⁵ N/m", "U = ½ × 10⁵ × (10⁻³)² = 0.05 J",
     "Check: final force = kx = 100 N → U = ½ × 100 × 10⁻³ = 0.05 J"],
    why="0.1 J forgets the ½ (uses force × extension); 0.025 J halves twice; 0.5 J slips a power of ten in the "
        "area.",
    ncert="Class 11 Physics, 'Mechanical Properties of Solids', elastic potential energy in a stretched wire",
    seconds=60, recomputed=True)

add(T, "Elasticity and moduli", "Intermediate", "assertion_reason",
    AR_STEM.format(
        a="Within the elastic limit, doubling the load hung from a given wire doubles its extension.",
        r="Within the elastic limit stress is proportional to strain (Hooke's law); for a given wire the stress is "
          "proportional to the load and the strain to the extension."),
    ar("A"),
    "Hooke's law applied to a stretched wire",
    "For a wire of cross-section A and length L, stress = F/A and strain = ΔL/L. Hooke's law (stress ∝ strain, "
    "i.e. F/A = Y ΔL/L) then gives ΔL = FL/(AY) ∝ F for the given wire. So doubling the load doubles the "
    "extension, and R is exactly the reason.",
    ["Stress ∝ strain → F/A = Y ΔL/L", "A, L, Y fixed → ΔL ∝ F → doubling F doubles ΔL → A true, R explains A"],
    ncert="Class 11 Physics, 'Mechanical Properties of Solids', Hooke's law and Young's modulus", seconds=40)

add(T, "Thermal expansion and calorimetry", "Intermediate", "statement_pair",
    SP_STEM.format(
        s1="The heat capacity of a body depends on its mass, whereas the specific heat capacity of its material does "
           "not.",
        s2="The coefficient of linear expansion of a material has the same numerical value whether it is expressed "
           "per °C or per K."),
    sp("A"),
    "Heat capacity versus specific heat capacity; size of a temperature interval",
    "Heat capacity S = ΔQ/ΔT is the heat needed to raise the whole body by 1 K, so it is proportional to the mass; "
    "specific heat capacity s = S/m is a property of the substance. Statement I is true. A temperature change of "
    "1 °C is the same as a change of 1 K, so α (fractional change in length per unit change of temperature) has the "
    "same value in either unit. Statement II is true.",
    ["S = ms → depends on mass; s does not → I true", "ΔT (°C) = ΔT (K) → α per °C = α per K → II true"],
    ncert="Class 11 Physics, 'Thermal Properties of Matter', specific heat capacity and thermal expansion",
    seconds=45)

base = 1.0
fac = {"A": 2 / 1 ** 2, "B": 1 / 2 ** 2, "C": 0.5 * 2 / 1, "D": 2 / 0.5 ** 2}   # extension ∝ F L / d^2
assert fac == {"A": 2.0, "B": 0.25, "C": 1.0, "D": 8.0}
add(T, "Elasticity and moduli", "Intermediate", "match_list",
    match_stem("A load hung from a wire produces an extension e. The wire is replaced by another wire of the same "
               "material, with the changes listed in List-I (anything not mentioned is unchanged). Match List-I with "
               "List-II (the new extension, within the elastic limit).",
               ["Length doubled", "Diameter doubled", "Length doubled and load halved",
                "Length doubled and diameter halved"],
               ["e/4", "e", "2e", "8e"]),
    match_options({"A": "III", "B": "I", "C": "II", "D": "IV"},
                  [{"A": "III", "B": "II", "C": "I", "D": "IV"}, {"A": "II", "B": "I", "C": "III", "D": "IV"},
                   {"A": "III", "B": "IV", "C": "II", "D": "I"}], "B"),
    "Extension of a wire: e = FL/(AY) = 4FL/(πd²Y)",
    "For the same material, Y is fixed, so the extension is proportional to the load and the length and inversely "
    "proportional to the square of the diameter.",
    ["e ∝ F L/d²", "A: L × 2 → 2e (III)", "B: d × 2 → e/4 (I)", "C: L × 2, F × ½ → e (II)",
     "D: L × 2, d × ½ → 2 × 4 = 8e (IV)"],
    why="Treating the extension as inversely proportional to the diameter (not its square) gives 2e for B and 4e "
        "for D, which leads to the wrong codes.",
    ncert="Class 11 Physics, 'Mechanical Properties of Solids', Young's modulus", seconds=60)

A_pist, F_pist = 1e-4, 3.2
dP = F_pist / A_pist
v_j = math.sqrt(2 * dP / rho_w)
assert close(dP, 3.2e4) and close(v_j, 8.0)
add(T, "Bernoulli's principle", "Advanced", "numerical",
    "A horizontal syringe filled with water has a piston of cross-sectional area 1 cm² and a very narrow nozzle open "
    "to the atmosphere. The piston is pushed steadily with a force of 3.2 N. Treating water (density 1000 kg/m³) as "
    "an ideal fluid in steady flow and neglecting the speed of the water inside the barrel, the speed with which "
    "water comes out of the nozzle is:",
    place("8 m/s", ["5.7 m/s", "64 m/s", "4 m/s"], "D"),
    "Bernoulli's equation between the barrel and the nozzle",
    "Inside the barrel the pressure exceeds atmospheric by F/A. At the nozzle the pressure is atmospheric. Both "
    "points are at the same height, and the speed in the wide barrel is negligible, so all the excess pressure "
    "becomes kinetic energy per unit volume at the nozzle.",
    ["Excess pressure = 3.2/10⁻⁴ = 3.2 × 10⁴ Pa", "½ρv² = 3.2 × 10⁴ → v² = 64 → v = 8 m/s"],
    why="5.7 m/s uses v² = ΔP/ρ (drops the ½); 64 m/s is v², not v; 4 m/s halves the excess pressure.",
    ncert="Class 11 Physics, 'Mechanical Properties of Fluids', Bernoulli's principle", seconds=90,
    recomputed=True)

gain = (0.1 * 4200 + 80) * (40 - 20)
c_m = gain / (0.25 * (140 - 40))
assert close(c_m, 400.0) and close(0.1 * 4200 * 20 / 25, 336.0)
add(T, "Thermal expansion and calorimetry", "Advanced", "numerical",
    "A metal block of mass 0.25 kg at 140 °C is dropped into a calorimeter of heat capacity 80 J/K containing "
    "0.1 kg of water at 20 °C. The final common temperature is 40 °C. The specific heat capacity of water is "
    "4200 J kg⁻¹ K⁻¹ and no heat is lost to the surroundings. The specific heat capacity of the metal is:",
    place("400 J kg⁻¹ K⁻¹", ["336 J kg⁻¹ K⁻¹", "200 J kg⁻¹ K⁻¹", "800 J kg⁻¹ K⁻¹"], "A"),
    "Principle of calorimetry including the calorimeter",
    "Heat lost by the metal equals heat gained by the water and the calorimeter together, both of which warm from "
    "20 °C to 40 °C.",
    ["Heat gained = (0.1 × 4200 + 80) × (40 − 20) = 500 × 20 = 10 000 J",
     "Heat lost by metal = 0.25 × c × (140 − 40) = 25c", "25c = 10 000 → c = 400 J kg⁻¹ K⁻¹"],
    why="336 J kg⁻¹ K⁻¹ ignores the heat taken by the calorimeter; 200 J kg⁻¹ K⁻¹ doubles the mass of the "
        "metal; 800 J kg⁻¹ K⁻¹ halves it.",
    seconds=100, recomputed=True)

H3 = 400 * 4e-4 * 100 / 0.4
m_ice = H3 * 7 * 60 / 3.36e5
assert close(H3, 40.0) and close(m_ice, 0.05)
add(T, "Heat transfer", "Advanced", "numerical",
    "One end of a copper rod, 0.4 m long and of cross-sectional area 4 cm², is kept in steam at 100 °C and the other "
    "end in a large block of ice at 0 °C. The sides of the rod are insulated. The thermal conductivity of copper is "
    "400 W m⁻¹ K⁻¹ and the latent heat of fusion of ice is 3.36 × 10⁵ J/kg. In the steady state, the mass of ice "
    "melted in 7 minutes is:",
    place("50 g", ["100 g", "0.83 g", "5 g"], "B"),
    "Steady-state conduction H = KA(T₁ − T₂)/L, followed by latent heat",
    "In the steady state the rate of heat flow is the same at every section of the rod. All the heat arriving at "
    "the cold end melts ice at 0 °C.",
    ["H = 400 × 4 × 10⁻⁴ × 100/0.4 = 40 W", "Heat in 7 min = 40 × 420 = 16 800 J",
     "Ice melted = 16 800/3.36 × 10⁵ = 0.05 kg = 50 g"],
    why="100 g doubles the area or the time; 0.83 g uses 7 s instead of 7 minutes (time not converted to "
        "seconds); 5 g takes the area as 0.4 cm², slipping a power of ten.",
    seconds=110, recomputed=True)

S4, r4 = 0.07, 0.05e-3
h_a = 2 * S4 / (rho_w * g * r4)
h_b = 2 * S4 / (rho_w * g * 0.2e-3)
assert close(h_a, 0.28) and close(h_b, 0.07) and close(h_a * 6, 1.68)
truth = [True, True, False, True, False]
multi_key(truth, "abd")
add(T, "Surface tension and capillarity", "Advanced", "multi_statement",
    multi("A clean glass capillary tube of internal radius 0.05 mm is held vertically with its lower end in water. "
          "The surface tension of water is 0.07 N/m, its density 1000 kg/m³ and the angle of contact zero; take "
          "g = 10 m/s². The tube is long enough in every case. Which of the following statements are correct?",
          ["Water rises 28 cm in the tube.",
           "In a tube of internal radius 0.2 mm of the same glass, water would rise 7 cm.",
           "The height of rise does not depend on the density of the liquid.",
           "If the same experiment were done on the Moon (g one-sixth of that on the Earth), water would rise "
           "168 cm in the 0.05 mm tube.",
           "Adding a detergent to the water would make it rise higher in the tube."]),
    place("(a), (b) and (d) only", ["(a), (b), (c) and (d) only", "(a), (d) and (e) only",
                                    "(b), (c) and (e) only"], "C"),
    "Capillary rise: h = 2S cos θ/(ρgr)",
    "The height of rise is inversely proportional to the radius, the density and g, and proportional to the "
    "surface tension (for θ = 0).",
    ["(a) h = 2 × 0.07/(1000 × 10 × 5 × 10⁻⁵) = 0.28 m = 28 cm, true",
     "(b) radius 4 times larger → h = 28/4 = 7 cm, true", "(c) h ∝ 1/ρ → false",
     "(d) h ∝ 1/g → 6 × 28 = 168 cm, true",
     "(e) detergent lowers the surface tension → the rise decreases → false"],
    why="(c) forgets that the weight of the raised column, which balances surface tension, depends on ρ; (e) has "
        "the effect of detergents the wrong way round.",
    ncert="Class 11 Physics, 'Mechanical Properties of Fluids', capillary rise", seconds=120, recomputed=True)

# =====================================================================================================================
# Thermodynamics (B2 I3 A3)  - no heat engines, efficiency or refrigerators
# =====================================================================================================================
T = "Thermodynamics"
R = 8.3

assert 0 - 300 == -300
add(T, "Isothermal and adiabatic processes", "Basic", "numerical",
    "A gas expands adiabatically and does 300 J of work on its surroundings. The change in its internal energy is:",
    place("−300 J", ["+300 J", "zero", "−150 J"], "D"),
    "First law of thermodynamics for an adiabatic process (ΔQ = 0)",
    "In the form ΔQ = ΔU + ΔW (ΔW = work done by the system), an adiabatic process has ΔQ = 0, so ΔU = −ΔW. The "
    "work done by the gas comes entirely from its internal energy.",
    ["ΔQ = 0, ΔW = +300 J", "ΔU = ΔQ − ΔW = −300 J (the gas cools)"],
    why="+300 J reverses the sign convention; zero would be the isothermal case for an ideal gas; −150 J halves the "
        "work for no reason.",
    ncert="Class 11 Physics, 'Thermodynamics', first law of thermodynamics and adiabatic process", seconds=25,
    recomputed=True)

add(T, "Zeroth and first law", "Basic", "direct",
    "Which of the following statements about heat is correct, in the sense used in thermodynamics?",
    place("Heat is energy that flows between a system and its surroundings because of a temperature difference",
          ["A hot body contains a large amount of heat", "Heat, like internal energy, is a state variable",
           "Heat can flow only by doing mechanical work"], "B"),
    "Heat, work and internal energy",
    "Internal energy is a property of the state of a system. Heat and work are not; they are two modes of "
    "transferring energy. Heat is the energy transferred because of a temperature difference. A body contains "
    "internal energy, not 'heat'.",
    ["Internal energy U: state variable", "Heat ΔQ and work ΔW: energy in transit, depend on the path"],
    why="A body has internal energy, not a store of heat; heat depends on the path and so is not a state variable; "
        "heat transfer due to a temperature difference does not need mechanical work.",
    ncert="Class 11 Physics, 'Thermodynamics', heat, internal energy and work", seconds=30)

a_P, b_V = 1e5, 1e-3            # semi-axes of the ellipse on the P–V diagram
Wc = math.pi * a_P * b_V
assert close(Wc, 100 * math.pi)
add(T, "Zeroth and first law", "Intermediate", "numerical",
    "A gas is taken once, clockwise, round a closed cycle that appears on a P–V diagram as an ellipse. The pressure "
    "in the cycle varies between 1 × 10⁵ Pa and 3 × 10⁵ Pa and the volume between 1 L and 3 L, the ellipse having "
    "its axes parallel to the P and V axes. The net work done by the gas in one cycle is:",
    place("100π J", ["400 J", "400π J", "50π J"], "C"),
    "Work in a cyclic process = area enclosed on the P–V diagram",
    "For a cycle traversed clockwise on a P–V diagram (V horizontal), the net work done by the gas is positive and "
    "equal to the enclosed area. An ellipse with semi-axes a and b has area πab.",
    ["Semi-axis along P: (3 − 1) × 10⁵/2 = 1 × 10⁵ Pa", "Semi-axis along V: (3 − 1)/2 = 1 L = 10⁻³ m³",
     "W = π × 10⁵ × 10⁻³ = 100π J ≈ 314 J"],
    why="400 J is the area of the bounding rectangle; 400π J uses the full axes (2 × 10⁵ Pa and 2 L) instead of "
        "the semi-axes; 50π J halves the area.",
    ncert="Class 11 Physics, 'Thermodynamics', work done in a cyclic process (area on the P–V diagram)", seconds=70,
    recomputed=True)

truth = [True, True, True, False, False]
multi_key(truth, "abc")
add(T, "Zeroth and first law", "Intermediate", "multi_statement",
    multi("An ideal gas is enclosed in a rigid, thermally insulated container. A paddle wheel inside, driven from "
          "outside, stirs the gas, and in this way 500 J of work is done on the gas. Which of the following "
          "statements are correct?",
          ["No heat is exchanged between the gas and its surroundings.",
           "The internal energy of the gas increases by 500 J.",
           "The temperature of the gas rises.",
           "The process is reversible: turning the paddle backwards would cool the gas back to its initial "
           "state.",
           "The gas does 500 J of work on the paddle."]),
    place("(a), (b) and (c) only", ["(a), (b), (c) and (d) only", "(b), (c) and (e) only",
                                    "(a), (d) and (e) only"], "D"),
    "First law with work done on a system; dissipative processes are irreversible",
    "The walls are insulating, so ΔQ = 0. Work is done on the gas, so in ΔQ = ΔU + ΔW we have ΔW = −500 J and "
    "ΔU = +500 J. For an ideal gas U depends only on T, so T rises. Stirring is a dissipative process: turning the "
    "paddle the other way also heats the gas, so the process cannot be reversed.",
    ["(a) insulated walls → ΔQ = 0, true", "(b) ΔU = ΔQ − ΔW = 0 − (−500) = +500 J, true",
     "(c) U rises → T rises (ideal gas), true", "(d) stirring is dissipative → irreversible, false",
     "(e) work is done ON the gas (ΔW = −500 J), not by it, false"],
    why="(d) ignores that dissipative effects such as viscous stirring make a process irreversible; (e) reverses "
        "the direction of the energy transfer.",
    ncert="Class 11 Physics, 'Thermodynamics', first law and reversible and irreversible processes", seconds=90)

add(T, "Second law, reversible and irreversible processes", "Intermediate", "statement_pair",
    SP_STEM.format(
        s1="In a reversible isothermal expansion of an ideal gas, all the heat absorbed by the gas is converted "
           "into work.",
        s2="This does not contradict the Kelvin–Planck statement of the second law, because the conversion of "
           "heat into work is not the sole result of the process: the gas ends up in a different state, with a "
           "larger volume."),
    sp("A"),
    "First law for an isothermal process and the wording of the Kelvin–Planck statement",
    "For an ideal gas U depends only on T, so in an isothermal process ΔU = 0 and ΔQ = ΔW: all the heat absorbed "
    "becomes work. Statement I is true. The Kelvin–Planck statement forbids a process whose SOLE result is the "
    "absorption of heat from a reservoir and its complete conversion into work. Here the gas is left expanded, "
    "so the conversion is not the sole result; Statement II is true.",
    ["Isothermal, ideal gas: ΔU = 0 → ΔQ = ΔW → I true",
     "Kelvin–Planck forbids complete conversion as the sole result; here the state of the gas changes → II true"],
    ncert="Class 11 Physics, 'Thermodynamics', second law of thermodynamics", seconds=60)

n6, dT6 = 2, 100
W6 = 2 * n6 * R * dT6               # V = kT^2 -> P dV = 2nR dT
Q6 = n6 * 1.5 * R * dT6 + W6
assert close(W6, 3320) and close(Q6, 5810)
add(T, "Zeroth and first law", "Advanced", "numerical",
    "Two moles of a monatomic ideal gas are heated so that throughout the process its volume is proportional to the "
    "square of its absolute temperature (V ∝ T²). Its temperature rises by 100 K. Taking R = 8.3 J mol⁻¹ K⁻¹ and "
    "Cᵥ = 3R/2, the heat absorbed by the gas is:",
    place("5810 J", ["2490 J", "4150 J", "3320 J"], "B"),
    "First law with work computed for a given process",
    "Write V = kT². With PV = nRT, P = nRT/V, so the work in a small step is P dV = (nRT/kT²)(2kT dT) = 2nR dT. The "
    "total work is 2nRΔT; the change in internal energy is nCᵥΔT whatever the process.",
    ["W = 2nRΔT = 2 × 2 × 8.3 × 100 = 3320 J", "ΔU = nCᵥΔT = 2 × 1.5 × 8.3 × 100 = 2490 J",
     "Q = ΔU + W = 5810 J"],
    shortcut="The molar heat capacity of this process is Cᵥ + 2R = 3.5R.",
    why="2490 J is ΔU alone; 4150 J is the heat at constant pressure (2.5R per mole), for which W would be nRΔT; "
        "3320 J is the work alone.",
    seconds=120, recomputed=True)

P07, A7, k7, x7 = 1e5, 0.01, 2000.0, 0.1
W7 = P07 * A7 * x7 + 0.5 * k7 * x7 ** 2
assert close(W7, 110.0)
add(T, "Zeroth and first law", "Advanced", "numerical",
    "A gas is enclosed in a horizontal cylinder by a light, frictionless piston of area 0.01 m². The outside of the "
    "piston is attached to a spring of spring constant 2000 N/m and is open to the atmosphere (pressure "
    "1 × 10⁵ Pa). Initially the spring is at its natural length and the gas is at atmospheric pressure. The gas is "
    "heated slowly until the piston has moved out by 0.1 m. The work done by the gas is:",
    place("110 J", ["100 J", "10 J", "120 J"], "A"),
    "Work done by a gas against the atmosphere and a spring in a quasi-static process",
    "For a light piston moving slowly, the gas pressure always balances the atmospheric pressure plus the spring "
    "force per unit area. The work done by the gas is therefore the work done against the atmosphere plus the "
    "elastic energy stored in the spring.",
    ["Against atmosphere: P₀AΔx = 10⁵ × 0.01 × 0.1 = 100 J", "Stored in spring: ½kx² = ½ × 2000 × 0.01 = 10 J",
     "Total W = 110 J"],
    why="100 J ignores the spring; 10 J ignores the atmosphere; 120 J uses kx² for the spring energy (forgets the "
        "½).",
    seconds=100, recomputed=True)

Tf8 = (1.5 * 400 + 2.5 * 240) / (1.5 + 2.5)
assert close(Tf8, 300.0) and close((2.5 * 400 + 1.5 * 240) / 4, 340) and close((2.5 * 400 + 3.5 * 240) / 6, 306.67)
add(T, "Zeroth and first law", "Advanced", "numerical",
    "A rigid, thermally insulated container is divided by a partition. One part holds 1 mol of a monatomic ideal gas "
    "at 400 K and the other 1 mol of a diatomic ideal gas (rigid molecules) at 240 K. The partition is removed and "
    "the gases mix without reacting. Using Cᵥ = 3R/2 and 5R/2 respectively, the final temperature is:",
    place("300 K", ["320 K", "340 K", "306.7 K"], "D"),
    "First law for an isolated system: total internal energy is conserved",
    "The container is rigid (no work) and insulated (no heat), so the total internal energy does not change. For an "
    "ideal gas U = nCᵥT, so the final temperature is the Cᵥ-weighted mean, not the simple mean.",
    ["1 × 1.5R × 400 + 1 × 2.5R × 240 = (1.5R + 2.5R) T", "600 + 600 = 4T → T = 300 K"],
    why="320 K is the simple average of 400 K and 240 K; 340 K swaps the weights (2.5R with 400 K and 1.5R with "
        "240 K); 306.7 K weights by Cₚ (2.5R and 3.5R), but no work is done in a rigid container, so Cᵥ applies.",
    seconds=100, recomputed=True)

# =====================================================================================================================
# Kinetic Theory of Gases (B1 I3 A1)
# =====================================================================================================================
T = "Kinetic Theory of Gases"

T2k = 300 * 2
assert T2k - 273 == 327
add(T, "Ideal gas equation", "Basic", "numerical",
    "A fixed mass of an ideal gas at 27 °C is heated at constant pressure until its volume doubles. Its final "
    "temperature is:",
    place("327 °C", ["54 °C", "600 °C", "300 °C"], "B"),
    "Ideal gas at constant pressure: V ∝ T (absolute temperature)",
    "From PV = μRT at constant P, V/T is constant, with T in kelvin. Doubling V doubles the absolute temperature.",
    ["T₁ = 27 + 273 = 300 K", "T₂ = 2 × 300 = 600 K = 327 °C"],
    why="54 °C doubles the Celsius temperature; 600 °C gives the kelvin value with the wrong unit; 300 °C confuses "
        "the initial absolute temperature with the answer.",
    ncert="Class 11 Physics, 'Kinetic Theory', molecular nature of matter and ideal gas equation", seconds=30,
    recomputed=True)

sp_ = [1, 2, 3, 4, 5]
vrms = math.sqrt(sum(v * v for v in sp_) / 5)
assert close(vrms, math.sqrt(11)) and close(sum(sp_) / 5, 3)
add(T, "Pressure and rms speed", "Intermediate", "numerical",
    "Five molecules of a gas have speeds of 1, 2, 3, 4 and 5 km/s. Their root mean square speed is:",
    place("√11 km/s", ["3 km/s", "11 km/s", "√55 km/s"], "D"),
    "Root mean square speed",
    "The rms speed is the square root of the mean of the squares of the speeds. It is not the same as the average "
    "speed.",
    ["Sum of squares = 1 + 4 + 9 + 16 + 25 = 55", "Mean of squares = 55/5 = 11", "v_rms = √11 ≈ 3.32 km/s"],
    why="3 km/s is the average speed; 11 km/s forgets the square root; √55 km/s forgets to divide by the number of "
        "molecules.",
    ncert="Class 11 Physics, 'Kinetic Theory', kinetic interpretation of temperature (rms speed)", seconds=40,
    recomputed=True)

add(T, "Pressure and rms speed", "Intermediate", "assertion_reason",
    AR_STEM.format(
        a="At a fixed temperature, the pressure of a given ideal gas is directly proportional to its density.",
        r="The pressure of an ideal gas is P = (1/3)ρv̄², where v̄² is the mean of the squares of the molecular "
          "speeds, and for a given gas v̄² depends only on the temperature."),
    ar("A"),
    "Kinetic theory expression for pressure",
    "Kinetic theory gives P = (1/3)nmv̄² = (1/3)ρv̄². For a given gas the mean square speed is fixed by the "
    "temperature (½mv̄² = (3/2)k_BT), so at constant temperature P ∝ ρ. R supplies exactly this reasoning.",
    ["P = (1/3)ρv̄²", "T fixed → v̄² fixed → P ∝ ρ → A true and explained by R"],
    ncert="Class 11 Physics, 'Kinetic Theory', pressure of an ideal gas", seconds=45)

truth = [True, True, False, False, False]
multi_key(truth, "ab")
add(T, "Degrees of freedom and equipartition", "Intermediate", "multi_statement",
    multi("Two identical vessels, one containing helium (monatomic) and the other oxygen (rigid diatomic molecules), "
          "are at the same temperature and the same pressure. Treating both as ideal gases, which of the following "
          "statements are correct?",
          ["The two vessels contain equal numbers of molecules.",
           "The average translational kinetic energy per molecule is the same in the two vessels.",
           "The rms speed of the molecules is the same in the two vessels.",
           "The total internal energy of the gas is the same in the two vessels.",
           "The mass of gas is the same in the two vessels."]),
    place("(a) and (b) only", ["(a), (b) and (d) only", "(a), (c) and (e) only", "(b), (c) and (d) only"], "C"),
    "Avogadro's hypothesis and equipartition of energy",
    "PV = Nk_BT: equal P, V and T mean equal N. The average translational kinetic energy per molecule is (3/2)k_BT "
    "for any gas. The rms speed √(3k_BT/m) depends on the molecular mass, the internal energy per molecule is "
    "(3/2)k_BT for helium but (5/2)k_BT for oxygen, and equal numbers of molecules of different masses have "
    "different total masses.",
    ["(a) N = PV/k_BT → equal, true", "(b) (3/2)k_BT for both, true", "(c) v_rms ∝ 1/√m → different, false",
     "(d) U = N(f/2)k_BT with f = 3 and 5 → different, false", "(e) masses differ (4 : 32 per molecule), false"],
    why="(d) counts only translational energy and forgets the two rotational degrees of freedom of O₂; (c) "
        "forgets that equal kinetic energies with unequal masses give unequal speeds.",
    ncert="Class 11 Physics, 'Kinetic Theory', law of equipartition of energy", seconds=90)

P1b = 1e5 + 1000 * g * 10
ratio_b = (P1b / 1e5) * (308 / 280)
assert close(P1b, 2e5) and close(ratio_b, 2.2)
add(T, "Ideal gas equation", "Advanced", "numerical",
    "A small air bubble at the bottom of a lake 10 m deep, where the temperature is 7 °C, rises to the surface, "
    "where the temperature is 35 °C. Take the atmospheric pressure as 1 × 10⁵ Pa, the density of water as "
    "1000 kg/m³ and g = 10 m/s², treat the air as an ideal gas and neglect surface tension. The ratio of the volume "
    "of the bubble at the surface to its volume at the bottom is:",
    place("2.2", ["2.0", "1.1", "10"], "A"),
    "Ideal gas equation for a fixed amount of gas: P₁V₁/T₁ = P₂V₂/T₂, with hydrostatic pressure",
    "The pressure at the bottom is atmospheric pressure plus ρgh. The amount of air does not change, so "
    "V₂/V₁ = (P₁/P₂)(T₂/T₁), with absolute temperatures.",
    ["P₁ = 10⁵ + 1000 × 10 × 10 = 2 × 10⁵ Pa, P₂ = 10⁵ Pa", "T₁ = 280 K, T₂ = 308 K",
     "V₂/V₁ = 2 × 308/280 = 2.2"],
    why="2.0 ignores the temperature change; 1.1 ignores the pressure change; 10 uses the Celsius temperatures "
        "35/7 × 2.",
    seconds=90, recomputed=True)

# =====================================================================================================================
# Oscillations and Waves (B4 I6 A5)
# =====================================================================================================================
T = "Oscillations and Waves"

w1_ = 2 * math.pi / (math.pi / 5)
assert close(0.5 * w1_ ** 2, 50.0)
add(T, "Spring and pendulum oscillations", "Basic", "statement_pair",
    SP_STEM.format(
        s1="The period of oscillation of a block attached to an ideal spring on a smooth horizontal surface does "
           "not depend on the amplitude of oscillation.",
        s2="A block of mass 0.5 kg oscillating on a spring with a period of π/5 s is attached to a spring of spring "
           "constant 50 N/m."),
    sp("A"),
    "Period of a spring–block oscillator: T = 2π√(m/k)",
    "The restoring force −kx gives simple harmonic motion with ω = √(k/m), so the period depends only on m and k, "
    "not on the amplitude: Statement I is true. With T = π/5 s, ω = 2π/T = 10 rad/s and k = mω² = 0.5 × 100 = "
    "50 N/m: Statement II is true.",
    ["T = 2π√(m/k), no amplitude → I true", "ω = 2π/(π/5) = 10 rad/s → k = mω² = 50 N/m → II true"],
    ncert="Class 11 Physics, 'Oscillations', oscillations due to a spring", seconds=45, recomputed=True)

mu2 = 0.010 / 4
v_s = math.sqrt(100 / mu2)
assert close(mu2, 2.5e-3) and close(v_s, 200.0) and close(math.sqrt(100 / 2.5), 6.32, rel=1e-2)
add(T, "Progressive waves and wave speed", "Basic", "numerical",
    "A uniform string 4 m long has a mass of 10 g. It is stretched with a tension of 100 N. The speed of transverse "
    "waves on it is:",
    place("200 m/s", ["6.3 m/s", "100 m/s", "4 × 10⁴ m/s"], "B"),
    "Speed of a transverse wave on a stretched string: v = √(T/μ)",
    "The speed depends on the tension and on the mass per unit length μ, which must first be found from the mass "
    "and the length of the string.",
    ["μ = 0.010 kg/4 m = 2.5 × 10⁻³ kg/m", "v = √(100/2.5 × 10⁻³) = √(4 × 10⁴) = 200 m/s"],
    why="6.3 m/s keeps the mass in grams (μ = 2.5, giving √40); 100 m/s uses μ = 10⁻² kg/m (forgets to divide by "
        "the length); 4 × 10⁴ m/s is T/μ, the square of the speed.",
    ncert="Class 11 Physics, 'Waves', speed of a transverse wave on a stretched string", seconds=35,
    recomputed=True)

add(T, "Organ pipes and beats", "Basic", "direct",
    "The phenomenon of beats, a periodic rise and fall in the loudness of sound, is a result of:",
    place("the superposition of two sound waves of slightly different frequencies",
          ["the reflection of sound from a distant surface", "the superposition of two waves of the same frequency "
           "travelling in opposite directions", "the change in the speed of sound with temperature"], "D"),
    "Beats",
    "When two harmonic sound waves of nearly equal frequencies ν₁ and ν₂ are heard together, their superposition "
    "has an amplitude that varies slowly with time; the loudness rises and falls ν₁ − ν₂ times per second.",
    ["s = 2a cos(πΔν t) sin(2πν̄ t)", "Loudness maxima occur |ν₁ − ν₂| times per second"],
    why="Reflection from a distant surface gives an echo; two waves of the same frequency travelling in opposite "
        "directions give a stationary wave; a change in the speed of sound does not produce periodic loudness "
        "changes.",
    ncert="Class 11 Physics, 'Waves', beats", seconds=25)

assert close(0.03 * 10, 0.3)
add(T, "SHM equation and phase", "Basic", "numerical",
    "The displacement of a particle in simple harmonic motion is x = 0.03 cos(10t), where x is in metres and t in "
    "seconds. The maximum speed of the particle is:",
    place("0.3 m/s", ["3 m/s", "0.03 m/s", "0.6 m/s"], "C"),
    "Maximum speed in SHM: v_max = Aω",
    "Comparing with x = A cos(ωt), A = 0.03 m and ω = 10 rad/s. The speed is greatest at the mean position, where "
    "it equals Aω.",
    ["A = 0.03 m, ω = 10 rad/s", "v_max = Aω = 0.3 m/s"],
    why="3 m/s is the maximum acceleration Aω² written with the wrong unit; 0.03 m/s is the amplitude; 0.6 m/s "
        "doubles Aω.",
    ncert="Class 11 Physics, 'Oscillations', velocity in simple harmonic motion", seconds=25, recomputed=True)

h5, Re = 6.4, 6400.0
ratio5 = (Re + h5) / Re
loss = 86400 * (1 - 1 / ratio5)
assert close(ratio5, 1.001) and 86 < loss < 86.5 and close(86400 * h5 / Re, 86.4)
add(T, "Spring and pendulum oscillations", "Intermediate", "numerical",
    "A pendulum clock keeps correct time at sea level. It is taken to the top of a mountain 6.4 km high. Taking the "
    "Earth's radius as 6400 km and treating the pendulum as a simple pendulum of unchanged length, the clock at the "
    "mountain top:",
    place("loses about 86 s per day", ["gains about 86 s per day", "loses about 173 s per day",
                                       "loses about 43 s per day"], "B"),
    "Period of a simple pendulum T = 2π√(L/g) with g varying with height",
    "At height h, g′ = g R²/(R + h)². Since T ∝ 1/√g, T′/T = (R + h)/R = 1.001. The pendulum swings more slowly, "
    "so the clock counts fewer seconds and loses time: in a day it loses about 86400 × 0.001 s.",
    ["g′/g = (R/(R + h))² → T′/T = (R + h)/R = 1 + 6.4/6400 = 1.001",
     "Time lost per day ≈ 86400 × 0.001 ≈ 86 s"],
    why="'Gains' gets the direction wrong (a smaller g gives a longer period); 173 s uses T ∝ 1/g (doubles the "
        "fraction); 43 s halves it, as if g changed by h/R instead of 2h/R.",
    ncert="Class 11 Physics, 'Oscillations', the simple pendulum; 'Gravitation', acceleration due to gravity above "
          "the surface", seconds=90, recomputed=True)

phi6 = math.pi / 3
assert close(2 * math.cos(phi6 / 2), math.sqrt(3))
add(T, "Superposition and standing waves", "Intermediate", "numerical",
    "Two waves of the same frequency and the same amplitude a travel along a string in the same direction. One leads "
    "the other in phase by π/3. The amplitude of the resultant wave is:",
    place("√3 a", ["2a", "a", "a/2"], "D"),
    "Principle of superposition for two waves with a phase difference",
    "Adding y₁ = a sin(kx − ωt) and y₂ = a sin(kx − ωt + φ) gives y = [2a cos(φ/2)] sin(kx − ωt + φ/2), a wave of "
    "the same frequency with amplitude 2a cos(φ/2).",
    ["A = 2a cos(φ/2) = 2a cos(π/6)", "A = 2a × (√3/2) = √3 a"],
    why="2a holds only for waves in phase (φ = 0); a is the result for φ = 2π/3; a/2 has no basis in the "
        "superposition formula.",
    ncert="Class 11 Physics, 'Waves', the principle of superposition of waves", seconds=50, recomputed=True)

m7, k7_, x7_, v7 = 1.0, 100.0, 0.1, 1.0
A7 = math.sqrt(x7_ ** 2 + m7 * v7 ** 2 / k7_)
assert close(A7, 0.1 * math.sqrt(2))
add(T, "Energy in SHM", "Intermediate", "numerical",
    "A block of mass 1 kg attached to a spring of spring constant 100 N/m oscillates on a smooth horizontal "
    "surface. When its displacement from the mean position is 0.1 m, its speed is 1 m/s. The amplitude of the "
    "oscillation is:",
    place("0.1√2 m", ["0.2 m", "0.1 m", "0.15 m"], "A"),
    "Conservation of energy in SHM: ½kA² = ½kx² + ½mv²",
    "The total energy is constant and equals the potential energy at the extreme position, ½kA².",
    ["Energy = ½ × 100 × 0.01 + ½ × 1 × 1 = 0.5 + 0.5 = 1 J", "½kA² = 1 → A² = 0.02 → A = 0.1√2 m ≈ 0.14 m"],
    why="0.2 m adds the displacement and v/ω directly instead of in quadrature; 0.1 m ignores the kinetic energy; "
        "0.15 m averages the two.",
    ncert="Class 11 Physics, 'Oscillations', energy in simple harmonic motion", seconds=60, recomputed=True)

add(T, "Energy in SHM", "Intermediate", "assertion_reason",
    AR_STEM.format(
        a="The total mechanical energy of a block oscillating on an ideal spring is directly proportional to the "
          "amplitude of its oscillation.",
        r="The total mechanical energy of a block oscillating on an ideal spring of spring constant k with amplitude "
          "A is ½kA²."),
    ar("D"),
    "Total energy of a spring–block oscillator",
    "At an extreme position the block is momentarily at rest and all the energy is elastic potential energy ½kA². "
    "Since energy is conserved, the total energy is ½kA², so R is true. The energy is proportional to the SQUARE of "
    "the amplitude, not to the amplitude itself: doubling A makes the energy four times. A is false.",
    ["E = ½kA² → R true", "E ∝ A², not A → A false"],
    ncert="Class 11 Physics, 'Oscillations', energy in simple harmonic motion", seconds=35)

add(T, "Spring and pendulum oscillations", "Intermediate", "statement_pair",
    SP_STEM.format(
        s1="For a simple pendulum displaced through an angle θ, the restoring force on the bob is the tangential "
           "component of its weight, −mg sin θ.",
        s2="For a simple pendulum, the tension in the string provides the restoring force that brings the bob back "
           "towards the mean position."),
    sp("C"),
    "Forces on the bob of a simple pendulum",
    "The forces on the bob are its weight and the tension. The tension acts along the string, i.e. along the "
    "radius through the point of suspension, so it has no tangential component and no torque about the "
    "suspension. The tangential component of the weight, mg sin θ, directed towards the mean position, is the "
    "restoring force. Statement I is true and Statement II is false.",
    ["Tension: along the string → no tangential component", "Restoring force = −mg sin θ (tangential) → I true",
     "Tension is not the restoring force → II false"],
    ncert="Class 11 Physics, 'Oscillations', the simple pendulum", seconds=40)

waves = {"A": (2, -4), "B": (4, 2), "D": (2, 4)}           # y = sin(kx + c t): speed |c|/k, direction -sign(c)
desc = {key: ("+x" if c < 0 else "-x", abs(c) / kk_) for key, (kk_, c) in waves.items()}
assert desc == {"A": ("+x", 2.0), "B": ("-x", 0.5), "D": ("-x", 2.0)}
add(T, "Progressive waves and wave speed", "Intermediate", "match_list",
    match_stem("In each equation of List-I, x and y are in metres and t in seconds. Match List-I (wave equation) "
               "with List-II (description of the wave).",
               ["y = 0.1 sin(2x − 4t)", "y = 0.1 sin(4x + 2t)", "y = 0.2 sin(2x) cos(4t)", "y = 0.1 sin(2x + 4t)"],
               ["A wave travelling in the −x direction at 0.5 m/s", "A wave travelling in the −x direction at 2 m/s",
                "A wave travelling in the +x direction at 2 m/s", "A stationary wave"]),
    match_options({"A": "III", "B": "I", "C": "IV", "D": "II"},
                  [{"A": "III", "B": "II", "C": "IV", "D": "I"}, {"A": "II", "B": "I", "C": "IV", "D": "III"},
                   {"A": "III", "B": "I", "C": "II", "D": "IV"}], "C"),
    "Reading direction and speed from y = a sin(kx ∓ ωt); stationary waves",
    "A wave a sin(kx − ωt) travels towards +x and a sin(kx + ωt) towards −x, both with speed ω/k. A product of a "
    "function of x and a function of t, such as sin kx cos ωt, does not travel: it is a stationary wave.",
    ["A: k = 2, ω = 4, minus sign → +x at 2 m/s (III)", "B: k = 4, ω = 2, plus sign → −x at 0.5 m/s (I)",
     "C: sin kx cos ωt → stationary wave (IV)", "D: k = 2, ω = 4, plus sign → −x at 2 m/s (II)"],
    why="Taking the speed as k/ω (giving 2 m/s for B) or reversing the direction rule leads to the other codes.",
    ncert="Class 11 Physics, 'Waves', displacement relation in a progressive wave and standing waves",
    seconds=70)

A11, w11 = math.hypot(3, 4), 2.0
assert close(A11 * w11, 10.0)
add(T, "SHM equation and phase", "Advanced", "numerical",
    "The displacement of a particle is x = 3 sin(2t) + 4 cos(2t), where x is in centimetres and t in seconds. The "
    "maximum speed of the particle is:",
    place("10 cm/s", ["14 cm/s", "5 cm/s", "20 cm/s"], "B"),
    "Sum of a sine and a cosine of the same frequency is a single SHM",
    "A sin ωt + B cos ωt = √(A² + B²) sin(ωt + φ) with tan φ = B/A. So the motion is SHM of amplitude "
    "√(3² + 4²) = 5 cm and ω = 2 rad/s, whose maximum speed is Aω.",
    ["Amplitude = √(9 + 16) = 5 cm", "ω = 2 rad/s", "v_max = 5 × 2 = 10 cm/s"],
    why="14 cm/s adds the amplitudes 3 + 4 directly; 5 cm/s is the amplitude, not the speed; 20 cm/s multiplies by "
        "ω twice (that is the maximum acceleration, in cm/s²).",
    ncert="Class 11 Physics, 'Oscillations', simple harmonic motion (sum of sine and cosine functions)",
    seconds=70, recomputed=True)

f_air, f_wat = 300.0, 200.0
rel_d = 1 / (1 - (f_wat / f_air) ** 2)
assert close(rel_d, 1.8)
add(T, "Superposition and standing waves", "Advanced", "numerical",
    "A sonometer wire of fixed vibrating length is kept taut by a solid block hanging from its end. Its fundamental "
    "frequency is 300 Hz. When the hanging block is completely immersed in water, the fundamental frequency becomes "
    "200 Hz. The relative density of the material of the block is:",
    place("1.8", ["2.25", "1.5", "3.0"], "D"),
    "Fundamental frequency of a stretched string, ν = (1/2L)√(T/μ), with buoyancy reducing the tension",
    "With L and μ fixed, ν ∝ √T. In water the tension falls from the weight W to W − upthrust. For a block of "
    "relative density d, the upthrust is W/d.",
    ["(ν₂/ν₁)² = T₂/T₁ = (2/3)² = 4/9", "T₂/T₁ = 1 − 1/d = 4/9 → 1/d = 5/9", "d = 9/5 = 1.8"],
    why="2.25 is (300/200)², the ratio of tensions, not the relative density; 1.5 takes ν ∝ T; 3.0 takes the "
        "frequency drop of 1/3 as 1/d.",
    ncert="Class 11 Physics, 'Waves', speed of a transverse wave on a string and normal modes of a string",
    seconds=110, recomputed=True)

Tbase = 1.0
pers = {"A": Tbase / math.sqrt(2), "B": Tbase * math.sqrt(2), "C": 2 * Tbase, "D": Tbase / math.sqrt(3)}
assert close(pers["A"], 2 * math.pi * math.sqrt(1 / 2) / (2 * math.pi))          # half spring -> 2k
assert close(pers["B"], math.sqrt(1 / 0.5)) and close(pers["C"], math.sqrt(4)) and close(pers["D"], math.sqrt(1 / 3))
add(T, "Spring and pendulum oscillations", "Advanced", "match_list",
    match_stem("A block of mass m attached to an ideal spring of spring constant k oscillates on a smooth "
               "horizontal surface with period T. Match List-I (change made, everything else unchanged) with "
               "List-II (the new period).",
               ["The spring is cut into two equal halves and the block is attached to one half",
                "The block is attached to two such springs (each of constant k) joined in series",
                "The block is replaced by one of mass 4m",
                "The block is attached to three such springs (each of constant k) side by side, in parallel"],
               ["T/√3", "√2 T", "2T", "T/√2"]),
    match_options({"A": "IV", "B": "II", "C": "III", "D": "I"},
                  [{"A": "II", "B": "IV", "C": "III", "D": "I"}, {"A": "IV", "B": "II", "C": "I", "D": "III"},
                   {"A": "I", "B": "II", "C": "III", "D": "IV"}], "B"),
    "T = 2π√(m/k) with the effective spring constant",
    "Cutting a spring into halves doubles the constant of each half (each half stretches half as much for the same "
    "force). Two springs in series have 1/k_eff = 1/k + 1/k, i.e. k/2; in parallel the constants add.",
    ["A: k → 2k → T/√2 (IV)", "B: k_eff = k/2 → √2 T (II)", "C: m → 4m → 2T (III)",
     "D: k_eff = 3k → T/√3 (I)"],
    why="Taking a half spring as having constant k/2 interchanges A and B; mixing up the series and parallel rules "
        "gives the remaining codes.",
    ncert="Class 11 Physics, 'Oscillations', oscillations due to a spring", seconds=80)

kF, mF = 10.0, 0.1
x0 = -2 / kF
T14 = 2 * math.pi / math.sqrt(kF / mF)
assert close(x0, -0.2) and close(T14, math.pi / 5)
add(T, "SHM equation and phase", "Advanced", "numerical",
    "A particle of mass 0.1 kg moves along the x-axis under a single force F = −10x − 2, where F is in newtons and "
    "x in metres. Its motion is simple harmonic. The mean position of the motion and the period are respectively:",
    place("x = −0.2 m and π/5 s",
          ["x = 0 and π/5 s", "x = +0.2 m and π/5 s", "x = −0.2 m and 2π s"], "A"),
    "SHM about a shifted equilibrium position",
    "The mean position is where the force is zero. Writing F = −10(x + 0.2) shows that the force is proportional "
    "to the displacement from x = −0.2 m and directed towards it, so the motion is SHM about that point with "
    "ω² = k/m.",
    ["F = 0 → x₀ = −2/10 = −0.2 m", "F = −10(x − x₀) → k = 10 N/m",
     "ω = √(10/0.1) = 10 rad/s → T = 2π/10 = π/5 s"],
    why="x = 0 ignores the constant force; +0.2 m gets its sign wrong; 2π s uses ω = √(k m) or forgets the mass.",
    seconds=80, recomputed=True)

f15 = 300 * math.sqrt((90 + 273) / (27 + 273))
assert close(f15, 330.0)
add(T, "Organ pipes and beats", "Advanced", "numerical",
    "A pipe open at both ends has a fundamental frequency of 300 Hz when the air in it is at 27 °C. Neglecting end "
    "corrections and any change in the length of the pipe, its fundamental frequency when the air in it is at 90 °C "
    "is (treat air as an ideal gas):",
    place("330 Hz", ["1000 Hz", "363 Hz", "300 Hz"], "C"),
    "Speed of sound in a gas ∝ √T; frequency of a pipe ∝ speed of sound",
    "For an open pipe ν = v/2L. With L fixed, ν ∝ v. For an ideal gas, v = √(γRT/M) ∝ √T, with T the absolute "
    "temperature.",
    ["T₁ = 300 K, T₂ = 363 K", "ν₂ = 300 × √(363/300) = 300 × √1.21 = 300 × 1.1 = 330 Hz"],
    why="1000 Hz scales with the Celsius temperatures (90/27); 363 Hz takes ν ∝ T; 300 Hz assumes the frequency "
        "depends only on the length of the pipe.",
    ncert="Class 11 Physics, 'Waves', speed of a longitudinal wave (Laplace correction) and standing waves in pipes",
    seconds=80, recomputed=True)

# =====================================================================================================================
# Electrostatics (B6 I8 A6)
# =====================================================================================================================
T = "Electrostatics"

V1 = k * 3e-9 / 0.9
assert close(V1, 30.0) and close(k * 3e-9 / 0.81, 33.33, rel=1e-3)
add(T, "Electric potential and energy", "Basic", "numerical",
    "Taking 1/(4πε₀) = 9 × 10⁹ N m² C⁻² and the potential to be zero at infinity, the electric potential at a "
    "distance of 0.9 m from a point charge of 3 nC in air is:",
    place("30 V", ["33.3 V", "300 V", "10 V"], "D"),
    "Potential due to a point charge: V = q/(4πε₀r)",
    "The potential falls off as 1/r (not 1/r², which is the law for the field).",
    ["V = 9 × 10⁹ × 3 × 10⁻⁹/0.9", "V = 27/0.9 = 30 V"],
    why="33.3 V divides by r² (that is the field, 33.3 N/C); 300 V slips a power of ten; 10 V divides by 2.7 "
        "instead of 0.9.",
    ncert="Class 12 Physics, 'Electrostatic Potential and Capacitance', potential due to a point charge",
    seconds=30, recomputed=True)

u2_ = 0.5 * EPS0 * (1e5) ** 2
assert close(u2_, 4.425e-2)
add(T, "Capacitors and dielectrics", "Basic", "numerical",
    "In a region of empty space the electric field has a magnitude of 1 × 10⁵ V/m. Taking ε₀ = 8.85 × 10⁻¹² "
    "C² N⁻¹ m⁻², the energy stored per unit volume of this region is about:",
    place("4.4 × 10⁻² J/m³", ["8.9 × 10⁻² J/m³", "4.4 × 10⁻⁷ J/m³", "0.44 J/m³"], "B"),
    "Energy density of an electric field: u = ½ε₀E²",
    "The energy of a charged capacitor can be regarded as stored in the field, with energy per unit volume "
    "½ε₀E². This expression holds for any electrostatic field in vacuum.",
    ["u = ½ × 8.85 × 10⁻¹² × (10⁵)²", "u = ½ × 8.85 × 10⁻² ≈ 4.4 × 10⁻² J/m³"],
    why="8.9 × 10⁻² J/m³ forgets the ½; 4.4 × 10⁻⁷ J/m³ uses E instead of E²; 0.44 J/m³ slips a power of ten.",
    ncert="Class 12 Physics, 'Electrostatic Potential and Capacitance', energy stored in a capacitor (energy "
          "density)", seconds=35, recomputed=True)

add(T, "Electric field and dipole", "Basic", "direct",
    "An electric dipole consists of charges +q and −q separated by a distance 2a. Its dipole moment vector p has "
    "magnitude 2qa and is directed:",
    place("along the line joining the charges, from −q to +q",
          ["along the line joining the charges, from +q to −q", "perpendicular to the line joining the charges",
           "along the electric field at the centre of the dipole"], "A"),
    "Definition of the electric dipole moment",
    "The dipole moment is defined as p = q × 2a p̂, where p̂ is the unit vector along the dipole axis pointing from "
    "the negative charge to the positive charge.",
    ["|p| = q × 2a", "Direction: from −q to +q"],
    why="From +q to −q is the direction of the electric field at the centre of the dipole, which is opposite to p; "
        "p lies along the axis, not perpendicular to it.",
    ncert="Class 12 Physics, 'Electric Charges and Fields', electric dipole", seconds=25)

E_vec, A_vec = (5e3, 2e3, 0.0), (0.0, 0.2, 0.0)
flux = sum(a * b for a, b in zip(E_vec, A_vec))
assert close(flux, 400.0) and close(math.hypot(5e3, 2e3) * 0.2, 1077.0, rel=1e-3)
add(T, "Gauss's law", "Basic", "numerical",
    "A uniform electric field E = (5 × 10³ î + 2 × 10³ ĵ) N/C exists in a region. A flat surface of area 0.2 m² is "
    "placed in it with its area vector pointing along +ĵ. The electric flux through the surface is:",
    place("400 N m² C⁻¹", ["1000 N m² C⁻¹", "1077 N m² C⁻¹", "zero"], "C"),
    "Electric flux through a flat surface in a uniform field: Φ = E · ΔS",
    "Only the component of the field along the area vector (normal to the surface) contributes to the flux. Here "
    "ΔS = 0.2 ĵ m², so only E_y counts.",
    ["Φ = E · ΔS = (5 × 10³)(0) + (2 × 10³)(0.2)", "Φ = 400 N m² C⁻¹"],
    why="1000 N m² C⁻¹ uses the x-component, which is parallel to the surface; 1077 N m² C⁻¹ uses the magnitude of "
        "E as if it were normal to the surface; zero would need the field to be parallel to the surface.",
    ncert="Class 12 Physics, 'Electric Charges and Fields', electric flux", seconds=35, recomputed=True)

add(T, "Electric potential and energy", "Basic", "assertion_reason",
    AR_STEM.format(
        a="In electrostatics, every point inside and on the surface of a conductor is at the same potential.",
        r="In the electrostatic situation, the electric field inside a conductor is zero and the field at its "
          "surface has no tangential component, so no work is done in moving a small test charge within the "
          "conductor or along its surface."),
    ar("A"),
    "Electrostatics of conductors",
    "The potential difference between two points is the work done per unit charge in moving a test charge between "
    "them. Since E = 0 inside and E is normal to the surface just outside, this work is zero for any path inside or "
    "along the surface, so the whole conductor is an equipotential. R gives the cause of A.",
    ["E = 0 inside; E normal at the surface", "Work = 0 → ΔV = 0 → conductor is an equipotential"],
    ncert="Class 12 Physics, 'Electrostatic Potential and Capacitance', electrostatics of conductors", seconds=40)

C6 = 5 * EPS0 * 0.04 / 2e-3
assert close(C6, 885e-12)
add(T, "Capacitors and dielectrics", "Basic", "numerical",
    "A parallel plate capacitor has plates of area 0.04 m² separated by 2 mm. The space between the plates is "
    "completely filled with a material of dielectric constant 5. Taking ε₀ = 8.85 × 10⁻¹² C² N⁻¹ m⁻², its "
    "capacitance is:",
    place("885 pF", ["177 pF", "88.5 pF", "1770 pF"], "D"),
    "Capacitance of a parallel plate capacitor filled with a dielectric: C = Kε₀A/d",
    "Filling the space with a dielectric of constant K multiplies the vacuum capacitance ε₀A/d by K.",
    ["ε₀A/d = 8.85 × 10⁻¹² × 0.04/(2 × 10⁻³) = 177 pF", "C = 5 × 177 pF = 885 pF"],
    why="177 pF is the value without the dielectric; 88.5 pF slips a power of ten; 1770 pF takes the separation "
        "as 1 mm.",
    ncert="Class 12 Physics, 'Electrostatic Potential and Capacitance', effect of dielectric on capacitance",
    seconds=40, recomputed=True)

Q7 = 10.0
best = max((q * (Q7 - q), q) for q in [x / 10 for x in range(0, 101)])
assert best[1] == 5.0
add(T, "Coulomb's law and superposition", "Intermediate", "numerical",
    "A charge of 10 μC is to be divided into two parts, which are then placed a fixed distance apart. For the "
    "electrostatic force between the two parts to be the greatest, the parts should be:",
    place("5 μC and 5 μC", ["2.5 μC and 7.5 μC", "3.3 μC and 6.7 μC", "10 μC and 0"], "B"),
    "Coulomb's law: F ∝ q(Q − q); maximum by differentiation",
    "With parts q and Q − q at a fixed distance r, F = kq(Q − q)/r². This is greatest when dF/dq = 0.",
    ["F ∝ q(Q − q) = Qq − q²", "dF/dq = Q − 2q = 0 → q = Q/2 = 5 μC", "Second derivative −2 < 0 → maximum"],
    why="Unequal parts give a smaller product q(Q − q) (2.5 × 7.5 = 18.75 and 3.3 × 6.7 ≈ 22.1, against 25); "
        "10 μC and 0 gives no force at all.",
    seconds=50, recomputed=True)

E_each8 = k * 4e-9 / 0.05 ** 2
E_res8 = 2 * E_each8 * (3 / 5)
assert close(E_each8, 14400.0) and close(E_res8, 17280.0) and close(2 * E_each8 * 0.8, 23040.0)
add(T, "Coulomb's law and superposition", "Intermediate", "numerical",
    "Point charges of +4 nC and −4 nC are fixed at points A and B, 6 cm apart, in air. P is a point on the "
    "perpendicular bisector of AB at a distance of 4 cm from the midpoint of AB. Taking 1/(4πε₀) = "
    "9 × 10⁹ N m² C⁻², the electric field at P is:",
    place("about 1.7 × 10⁴ N/C, parallel to AB (directed from A towards B)",
          ["about 2.3 × 10⁴ N/C, along the perpendicular bisector", "about 2.9 × 10⁴ N/C, parallel to AB",
           "zero"], "D"),
    "Superposition of the fields of two point charges",
    "P is 5 cm from each charge. The field of +4 nC points away from A and that of −4 nC points towards B. Their "
    "components along the bisector cancel, and their components parallel to AB add.",
    ["AP = BP = √(3² + 4²) = 5 cm", "Each field = 9 × 10⁹ × 4 × 10⁻⁹/(0.05)² = 1.44 × 10⁴ N/C",
     "Parallel to AB: 2 × 1.44 × 10⁴ × (3/5) = 1.73 × 10⁴ N/C, from A towards B"],
    why="2.3 × 10⁴ N/C along the bisector is the answer for two equal positive charges (components along the "
        "bisector add, with factor 4/5); 2.9 × 10⁴ N/C adds the magnitudes; the field is zero only for like "
        "charges at the midpoint.",
    seconds=100, recomputed=True)

r30, r20 = k * 3e-9 / 30, k * 3e-9 / 20
assert close(r30, 0.9) and close(r20, 1.35) and close(r20 - r30, 0.45)
add(T, "Electric potential and energy", "Intermediate", "numerical",
    "Taking 1/(4πε₀) = 9 × 10⁹ N m² C⁻² and the potential to be zero at infinity, the separation between the "
    "equipotential surfaces of 30 V and 20 V around an isolated point charge of 3 nC is:",
    place("0.45 m", ["0.90 m", "1.35 m", "2.7 m"], "A"),
    "Equipotential surfaces of a point charge are concentric spheres of radius r = q/(4πε₀V)",
    "For a point charge, V = kq/r, so each equipotential surface is a sphere centred on the charge with r = kq/V. "
    "The separation is the difference of the radii.",
    ["kq = 9 × 10⁹ × 3 × 10⁻⁹ = 27 V m", "r(30 V) = 27/30 = 0.90 m, r(20 V) = 27/20 = 1.35 m",
     "Separation = 0.45 m"],
    why="0.90 m and 1.35 m are the radii of the two spheres, not their separation; 2.7 m divides kq by the "
        "potential difference (27/10), which has no meaning for spheres of different radii.",
    ncert="Class 12 Physics, 'Electrostatic Potential and Capacitance', equipotential surfaces", seconds=60,
    recomputed=True)

p10 = 5e-9 * 1e-3
E10e = k * p10 / 0.1 ** 3
assert close(p10, 5e-12) and close(E10e, 45.0)
add(T, "Electric field and dipole", "Intermediate", "numerical",
    "An electric dipole is made of charges +5 nC and −5 nC separated by 1 mm. Taking 1/(4πε₀) = 9 × 10⁹ N m² C⁻², "
    "the magnitude of the electric field at a point on its equatorial line, 10 cm from its centre, is:",
    place("45 N/C", ["90 N/C", "4.5 N/C", "450 N/C"], "C"),
    "Field of a short dipole on its equatorial line: E = p/(4πε₀r³)",
    "Since 10 cm ≫ 1 mm, the dipole is short. On the equatorial line its field has magnitude kp/r³ and points "
    "opposite to p; on the axis it would be 2kp/r³.",
    ["p = 5 × 10⁻⁹ × 10⁻³ = 5 × 10⁻¹² C m", "E = 9 × 10⁹ × 5 × 10⁻¹²/(0.1)³ = 45 N/C"],
    why="90 N/C is the axial value 2kp/r³; 4.5 N/C and 450 N/C slip a power of ten in r³ or in p.",
    ncert="Class 12 Physics, 'Electric Charges and Fields', field of an electric dipole", seconds=55,
    recomputed=True)

add(T, "Electric field and dipole", "Intermediate", "assertion_reason",
    AR_STEM.format(
        a="Electrostatic field lines never form closed loops.",
        r="The electrostatic field is a non-conservative field."),
    ar("C"),
    "Properties of electrostatic field lines",
    "NCERT states that electrostatic field lines do not form closed loops, and that this follows from the "
    "CONSERVATIVE nature of the electrostatic field: the work done by it round any closed path is zero, which "
    "would not be so if a line closed on itself. A is true; R is false.",
    ["A: field lines start on positive and end on negative charges (or infinity), no closed loops → true",
     "R: the electrostatic field is conservative → R false"],
    ncert="Class 12 Physics, 'Electric Charges and Fields', electric field lines", seconds=30)

add(T, "Capacitors and dielectrics", "Intermediate", "statement_pair",
    SP_STEM.format(
        s1="In a non-polar molecule, the centre of positive charge coincides with the centre of negative charge, so "
           "the molecule has no permanent dipole moment.",
        s2="When a non-polar molecule is placed in an external electric field, it develops an induced dipole moment "
           "because the field displaces its positive and negative charges in opposite directions."),
    sp("A"),
    "Polar and non-polar molecules; polarisation",
    "NCERT: in a non-polar molecule (such as O₂ or H₂) the centres of positive and negative charge coincide, so "
    "there is no permanent dipole moment. An external field pushes the positive charge along the field and the "
    "negative charge against it, separating the centres and inducing a dipole moment. Both statements are true.",
    ["Non-polar: centres coincide → p = 0 → I true", "External field separates the centres → induced p → II true"],
    ncert="Class 12 Physics, 'Electrostatic Potential and Capacitance', dielectrics and polarisation", seconds=40)

U = {"A": -math.cos(0), "B": -math.cos(math.pi / 2), "C": -math.cos(math.pi), "D": -math.cos(math.pi / 3)}
assert close(U["A"], -1) and abs(U["B"]) < 1e-12 and close(U["C"], 1) and close(U["D"], -0.5)
add(T, "Electric field and dipole", "Intermediate", "match_list",
    match_stem("An electric dipole of moment p is placed in a uniform electric field E. Its potential energy is "
               "taken as zero when p is perpendicular to E. Match List-I (angle between p and E) with List-II "
               "(potential energy of the dipole).",
               ["0°", "90°", "180°", "60°"],
               ["+pE", "−pE/2", "−pE", "0"]),
    match_options({"A": "III", "B": "IV", "C": "I", "D": "II"},
                  [{"A": "I", "B": "IV", "C": "III", "D": "II"}, {"A": "III", "B": "IV", "C": "II", "D": "I"},
                   {"A": "IV", "B": "III", "C": "I", "D": "II"}], "B"),
    "Potential energy of a dipole in a uniform field: U = −pE cos θ",
    "With the zero of energy at θ = 90°, the potential energy is U(θ) = −pE cos θ. It is least (most negative) "
    "when p is along E, the position of stable equilibrium, and greatest when p is opposite to E.",
    ["θ = 0°: U = −pE (III)", "θ = 90°: U = 0 (IV)", "θ = 180°: U = +pE (I)", "θ = 60°: U = −pE/2 (II)"],
    why="Using U = +pE cos θ reverses the signs (A-I, C-III); using sin θ instead of cos θ moves the zero to 0°.",
    ncert="Class 12 Physics, 'Electrostatic Potential and Capacitance', potential energy of a dipole in an external "
          "field", seconds=50)

truth = [True, True, True, False, False]
multi_key(truth, "abc")
add(T, "Gauss's law", "Intermediate", "multi_statement",
    multi("A thin spherical shell of radius R in vacuum carries a charge Q spread uniformly over it. Take "
          "k = 1/(4πε₀) and the potential to be zero at infinity. Which of the following statements are correct?",
          ["The electric field at every point inside the shell is zero.",
           "The potential at every point inside the shell is kQ/R.",
           "The magnitude of the field just outside the shell is kQ/R².",
           "The magnitude of the field at a distance 2R from the centre is kQ/(2R²).",
           "The potential at a distance 2R from the centre is kQ/(4R)."]),
    place("(a), (b) and (c) only", ["(a), (b), (c) and (e) only", "(a), (c) and (d) only",
                                    "(b), (d) and (e) only"], "D"),
    "Field and potential of a uniformly charged thin spherical shell (Gauss's law)",
    "A Gaussian sphere inside the shell encloses no charge, so E = 0 inside; the potential is then constant inside "
    "and equal to its value at the surface, kQ/R. Outside, the shell acts as a point charge Q at its centre: "
    "E = kQ/r² and V = kQ/r.",
    ["(a) E = 0 inside, true", "(b) V inside = V(surface) = kQ/R, true", "(c) E(R⁺) = kQ/R², true",
     "(d) E(2R) = kQ/(4R²), not kQ/(2R²) → false", "(e) V(2R) = kQ/(2R), not kQ/(4R) → false"],
    why="(d) uses 1/r for the field and (e) uses 1/r² for the potential: the two laws are interchanged.",
    ncert="Class 12 Physics, 'Electric Charges and Fields', field due to a uniformly charged thin spherical shell",
    seconds=80)

q15, lam15, m15 = 1e-6, 1e-6, 1.8e-4
v15 = math.sqrt(q15 * lam15 * 2 * k / m15)
assert close(v15, 10.0) and close(math.sqrt(q15 * lam15 * k / m15), math.sqrt(50))
add(T, "Gauss's law", "Advanced", "numerical",
    "A very long straight wire carries a uniform linear charge density of +1 μC/m. A particle of mass 0.18 g and "
    "charge −1 μC moves in a circle around the wire, in a plane perpendicular to it with the wire at the centre, "
    "under the electric force alone. Taking 1/(4πε₀) = 9 × 10⁹ N m² C⁻², the speed of the particle is:",
    place("10 m/s, whatever the radius of the circle",
          ["100 m/s, whatever the radius", "about 7.1 m/s, whatever the radius",
           "10 m/s only if the radius is 1 m; smaller for larger radii"], "B"),
    "Field of an infinite line charge (Gauss's law) providing the centripetal force",
    "By Gauss's law the field of the line charge at distance r is E = λ/(2πε₀r), directed radially. The attractive "
    "force on the particle, qλ/(2πε₀r), provides mv²/r, and r cancels.",
    ["mv²/r = qλ/(2πε₀r) → v² = qλ/(2πε₀m) = 2kqλ/m",
     "v² = 2 × 9 × 10⁹ × 10⁻⁶ × 10⁻⁶/(1.8 × 10⁻⁴) = 100", "v = 10 m/s, independent of r"],
    why="100 m/s is v², not v; 7.1 m/s uses 1/(4πε₀r) instead of 1/(2πε₀r) for the line-charge field; the radius "
        "cancels because both the force and mv²/r vary as 1/r.",
    ncert="Class 12 Physics, 'Electric Charges and Fields', field due to an infinitely long straight uniformly "
          "charged wire", seconds=110, recomputed=True)

m16, q16, E16 = 2e-3, 5e-6, 4000.0
T16 = math.hypot(m16 * g, q16 * E16)
assert close(q16 * E16, m16 * g) and close(T16, 0.02 * math.sqrt(2))
add(T, "Coulomb's law and superposition", "Advanced", "numerical",
    "A small ball of mass 2 g carrying a charge of +5 μC hangs from a light insulating thread in a uniform "
    "horizontal electric field of 4000 N/C. Taking g = 10 m/s², in equilibrium the thread makes an angle θ with "
    "the vertical and the tension in it is T. Then:",
    place("θ = 45° and T = 2√2 × 10⁻² N",
          ["θ = 45° and T = 2 × 10⁻² N", "θ = 45° and T = 4 × 10⁻² N", "θ = 30° and T = 2√2 × 10⁻² N"], "C"),
    "Equilibrium of a charged body under weight, electric force and tension",
    "The horizontal electric force qE and the weight mg are balanced by the tension. Hence tan θ = qE/mg and "
    "T = √((mg)² + (qE)²).",
    ["qE = 5 × 10⁻⁶ × 4000 = 0.02 N; mg = 2 × 10⁻³ × 10 = 0.02 N", "tan θ = 1 → θ = 45°",
     "T = √(0.02² + 0.02²) = 0.02√2 = 2√2 × 10⁻² N"],
    why="2 × 10⁻² N balances only the weight (or only the electric force); 4 × 10⁻² N adds the two forces as if "
        "parallel; θ = 30° would need qE = mg tan 30°, i.e. a field of only about 2300 N/C.",
    seconds=90, recomputed=True)

sig17, q17, d17 = 1.77e-7, 0.4e-6, 1.0
E_sheet = sig17 / (2 * EPS0)
r_null = math.sqrt(k * q17 / E_sheet)
assert close(E_sheet, 1e4) and close(r_null, 0.6) and r_null < d17
add(T, "Gauss's law", "Advanced", "numerical",
    "A large, thin, plane sheet carries a uniform surface charge density of +1.77 × 10⁻⁷ C/m². A point charge of "
    "+0.4 μC is held 1 m from the sheet. Taking ε₀ = 8.85 × 10⁻¹² C² N⁻¹ m⁻² and 1/(4πε₀) = 9 × 10⁹ N m² C⁻², the "
    "net electric field is zero at a point:",
    place("0.4 m from the sheet, between the sheet and the charge",
          ["0.6 m from the sheet, between the sheet and the charge",
           "0.6 m from the charge, on the side of the charge away from the sheet",
           "nowhere at a finite distance"], "D"),
    "Superposition of the uniform field of a sheet (Gauss's law) and the field of a point charge",
    "The sheet's field has magnitude σ/2ε₀ on both sides, pointing away from it. The point charge's field points "
    "away from the charge. Only on the line between them do the two fields point in opposite directions, so the "
    "null point lies there, at a distance r from the charge where kq/r² = σ/2ε₀.",
    ["σ/2ε₀ = 1.77 × 10⁻⁷/(2 × 8.85 × 10⁻¹²) = 1.0 × 10⁴ N/C",
     "kq/r² = 10⁴ → r² = 9 × 10⁹ × 4 × 10⁻⁷/10⁴ = 0.36 → r = 0.6 m from the charge",
     "This point is 1 − 0.6 = 0.4 m from the sheet, between the two"],
    why="0.6 m from the sheet measures r from the wrong end; beyond the charge both fields point away from the sheet "
        "and add; a null point does exist because the charge's field decreases from very large values near it.",
    ncert="Class 12 Physics, 'Electric Charges and Fields', field due to a uniformly charged infinite plane sheet",
    seconds=130, recomputed=True)

Cs = 3 * 6 / (3 + 6)
Qs = Cs * 9
Vp = 2 * Qs / (3 + 6)
assert close(Cs, 2) and close(Qs, 18) and close(Vp, 4.0)
add(T, "Capacitors and dielectrics", "Advanced", "numerical",
    "Capacitors of 3 μF and 6 μF are connected in series across a 9 V battery. When fully charged, they are "
    "disconnected from the battery and from each other, and are then connected in parallel, positive plate to "
    "positive plate. The common potential difference across them is:",
    place("4 V", ["9 V", "0 V", "6 V"], "A"),
    "Charge on capacitors in series, then redistribution of charge in parallel",
    "In series both capacitors carry the same charge, Q = C_eq V. On reconnecting in parallel with like plates "
    "together, the total charge 2Q spreads over the combined capacitance 3 + 6 = 9 μF.",
    ["C_eq (series) = 3 × 6/9 = 2 μF → Q = 2 × 9 = 18 μC on each",
     "Parallel, like plates joined: total charge 36 μC on 9 μF", "V = 36/9 = 4 V"],
    why="9 V assumes the battery voltage is restored; 0 V is the result if unlike plates are joined; 6 V is the "
        "potential difference the 3 μF capacitor had in series.",
    seconds=100, recomputed=True)

C19, V19 = 1.0, 1.0
Ui = 0.5 * C19 * V19 ** 2
Uf = 0.5 * (2 * C19) * (V19 / 2) ** 2
assert close(Uf, Ui / 2)
add(T, "Capacitors and dielectrics", "Advanced", "statement_pair",
    SP_STEM.format(
        s1="A capacitor charged to a potential difference V is disconnected from the battery and connected across an "
           "identical, uncharged capacitor. Half of the energy initially stored is lost in the process.",
        s2="In this process the total charge on the two capacitors decreases, because some charge is lost as "
           "heat in the connecting wires."),
    sp("C"),
    "Sharing of charge between capacitors: charge conserved, energy not",
    "The total charge CV is conserved and is shared equally, so each capacitor ends at V/2. The final energy is "
    "2 × ½C(V/2)² = ¼CV², half the initial ½CV²: Statement I is true. The 'lost' energy is dissipated as heat "
    "(and radiation) while charge flows; the charge itself is conserved, so Statement II is false.",
    ["Charge: CV = 2C V′ → V′ = V/2", "Energy: ½CV² → 2 × ½C(V/2)² = ¼CV² → half lost → I true",
     "Charge is conserved; energy, not charge, is converted to heat → II false"],
    ncert="Class 12 Physics, 'Electrostatic Potential and Capacitance', combination of capacitors and energy "
          "stored", seconds=70, recomputed=True)

a20 = 1.0
Ey = lambda y: 2 * y / (a20 ** 2 + y ** 2) ** 1.5
ys = [i / 10000 for i in range(1, 30000)]
ymax = max(ys, key=Ey)
assert abs(ymax - a20 / math.sqrt(2)) < 1e-3
truth = [True, True, False, True, True]
multi_key(truth, "abde")
add(T, "Coulomb's law and superposition", "Advanced", "multi_statement",
    multi("Two equal point charges +q are fixed at points A and B, a distance 2a apart, in vacuum; O is the midpoint "
          "of AB. Take k = 1/(4πε₀) and the potential to be zero at infinity. Which of the following statements "
          "are correct?",
          ["The electric field at O is zero.",
           "The electric potential at O is 2kq/a.",
           "A small positive test charge placed at O is in stable equilibrium for small displacements along the "
           "perpendicular bisector of AB.",
           "A small positive test charge placed at O is in stable equilibrium for small displacements along AB.",
           "On the perpendicular bisector of AB, the field is greatest at a distance a/√2 from O."]),
    place("(a), (b), (d) and (e) only", ["(a), (b) and (c) only", "(a), (c), (d) and (e) only",
                                         "(b), (c) and (e) only"], "B"),
    "Superposition of the fields and potentials of two like charges",
    "At O the two fields are equal and opposite, while the potentials (scalars) add. On the perpendicular bisector "
    "the field at distance y from O is E = 2kqy/(a² + y²)^(3/2), directed away from O; along AB a displaced "
    "charge is pushed back towards O by the nearer charge.",
    ["(a) Fields cancel at O, true", "(b) V = kq/a + kq/a = 2kq/a, true",
     "(c) On the bisector E points away from O → the charge moves further away → unstable → false",
     "(d) Along AB the nearer charge repels it back → stable → true",
     "(e) dE/dy = 0 → a² + y² = 3y² → y = a/√2, true"],
    why="(c) is the classic trap: the equilibrium at O is stable along AB but unstable along the bisector.",
    seconds=150, recomputed=True)

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
    doc = {"schema_version": "1.0", "batch_id": "BATCH_010", "created_at": TODAY,
           "notes": "BATCH_010 package PHY_010_p1: 116 original Physics questions (Physics and Measurement through "
                    "Electrostatics). Every numerical answer is re-derived in tools/batch_010/PHY_010_p1.py.",
           "stimuli": [], "questions": QUESTIONS}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {OUT}: {n} questions, {dict(Counter(x['difficulty'] for x in QUESTIONS))}")
    print(f"keys {dict(sorted(keys.items()))}")
    print(f"formats {dict(fmts)}")
