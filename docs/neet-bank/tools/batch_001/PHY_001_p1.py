"""Writes batches/parts/BATCH_001_PHY_p1.json: package PHY_001_p1 of BATCH_001 (130 Physics questions).

Topics: Physics and Measurement, Kinematics, Laws of Motion, Work Energy and Power, Rotational Motion, Gravitation,
Properties of Solids and Liquids, Thermodynamics, Kinetic Theory of Gases, Oscillations and Waves, Electrostatics.
IDs NEET_PHY_000006 .. NEET_PHY_000135, in the order the questions are listed below.

Every computable answer is re-derived with an assert before the file is written, and so is the plan quota. If any
assert fails, nothing is written.

    python tools/batch_001/PHY_001_p1.py        (run from docs/neet-bank)
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
OUT = ROOT / "batches" / "parts" / "BATCH_001_PHY_p1.json"
PLAN = ROOT / "batches" / "plans" / "BATCH_001_plan.json"
PACKAGE = "PHY_001_p1"
TODAY = "2026-11-16"
LETTERS = "ABCD"
PHY = "Physics"
RECOMPUTED = ("script:recompute", "ai:author-solve", "ai:self-recheck")
AUTHORED = ("ai:author-solve", "ai:self-recheck")
FIRST_ID = 6

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


# =====================================================================================================================
# Physics and Measurement (B2 I2 A2)
# =====================================================================================================================
T = "Physics and Measurement"

add(T, "Units and SI system", "Basic", "match_list",
    match_stem("Match List-I (base quantity) with List-II (its SI unit).",
               ["Luminous intensity", "Amount of substance", "Thermodynamic temperature", "Electric current"],
               ["kelvin", "ampere", "candela", "mole"]),
    match_options({"A": "III", "B": "IV", "C": "I", "D": "II"},
                  [{"A": "IV", "B": "III", "C": "I", "D": "II"}, {"A": "III", "B": "IV", "C": "II", "D": "I"},
                   {"A": "II", "B": "IV", "C": "I", "D": "III"}], "B"),
    "The seven SI base quantities and their units",
    "The SI has seven base units. Four of them are asked here: candela (luminous intensity), mole (amount of "
    "substance), kelvin (thermodynamic temperature) and ampere (electric current).",
    ["Luminous intensity → candela (cd) → III", "Amount of substance → mole (mol) → IV",
     "Thermodynamic temperature → kelvin (K) → I", "Electric current → ampere (A) → II"],
    why="The other codes swap candela with mole, or kelvin with ampere.",
    ncert="Class 11 Physics, 'Units and Measurement', the international system of units", seconds=30)

# 4.235 x 2.1 -> 2 significant figures
prod = 4.235 * 2.1
assert close(prod, 8.8935) and f"{prod:.1f}" == "8.9"
add(T, "Least count and significant figures", "Basic", "numerical",
    "The product 4.235 × 2.1, written with the correct number of significant figures, is:",
    place("8.9", ["8.8935", "8.89", "9"], "C"),
    "Significant figures in multiplication",
    "In a product or quotient, the result keeps as many significant figures as the factor with the fewest "
    "significant figures. 2.1 has two significant figures, so the answer is rounded to two.",
    ["4.235 × 2.1 = 8.8935 (calculator value)", "Least number of significant figures among the factors = 2 (in 2.1)",
     "Round 8.8935 to two significant figures → 8.9"],
    why="8.8935 keeps every calculator digit. 8.89 keeps three significant figures (rounding to decimal places, "
        "a rule for addition). 9 keeps only one.",
    ncert="Class 11 Physics, 'Units and Measurement', significant figures (rules for arithmetic operations)",
    seconds=30, recomputed=True)

# Z = A^2 B^3 / sqrt(C); errors 1 %, 2 %, 4 %
pz = 2 * 1 + 3 * 2 + F(1, 2) * 4
assert pz == 10 and 1 + 2 + 4 == 7 and 2 * 1 + 3 * 2 + 4 == 12 and 2 * 1 + 3 * 2 - 2 == 6
add(T, "Errors in measurement", "Intermediate", "numerical",
    "A quantity Z is calculated from Z = A²B³/√C. The percentage errors in measuring A, B and C are 1%, 2% and "
    "4% respectively. The maximum percentage error in Z is:",
    place("10%", ["7%", "12%", "6%"], "D"),
    "Propagation of relative error through powers",
    "For Z = (A to the power p)(B to the power q)/(C to the power r), the maximum relative error is p(ΔA/A) + q(ΔB/B) + r(ΔC/C). Errors always add, even for "
    "a quantity in the denominator, and each is multiplied by its power.",
    ["ΔZ/Z = 2(ΔA/A) + 3(ΔB/B) + ½(ΔC/C)", "= 2(1%) + 3(2%) + ½(4%)", "= 2% + 6% + 2% = 10%"],
    why="7% adds the errors without their powers. 12% uses power 1 for C instead of ½. 6% subtracts the error of "
        "C because C is in the denominator; maximum errors never subtract.",
    ncert="Class 11 Physics, 'Units and Measurement', combination of errors", seconds=50, recomputed=True)

# new units: mass 2 kg, length 4 m, time 2 s -> new unit of force = 2*4/2^2 = 2 N, so 1 N = 0.5 new unit
new_force_unit = F(2) * 4 / 2 ** 2
assert new_force_unit == 2 and 1 / new_force_unit == F(1, 2)
add(T, "Units and SI system", "Intermediate", "numerical",
    "In a new system of units, the unit of mass is 2 kg, the unit of length is 4 m and the unit of time is 2 s. "
    "A force of 1 N, expressed in this system, has the numerical value:",
    place("0.5", ["2", "8", "0.125"], "A"),
    "Conversion of a numerical value between systems of units",
    "Force has dimensions [M L T⁻²]. The new unit of force is (2 kg)(4 m)/(2 s)² = 2 N. A force of 1 N is "
    "half of this unit. In general n₂ = n₁ (M₁/M₂)(L₁/L₂)(T₁/T₂)⁻².",
    ["n₂ = 1 × (1 kg/2 kg)¹ × (1 m/4 m)¹ × (1 s/2 s)⁻²", "= 1 × ½ × ¼ × 4", "= 0.5"],
    shortcut="New unit of force = 2 × 4 / 2² = 2 N, so 1 N = 1/2 = 0.5 new unit.",
    why="2 is the size of the new unit in newtons, not the value of 1 N in the new unit. 8 ignores the time "
        "unit. 0.125 ignores the time unit and inverts.",
    seconds=60, recomputed=True)

# T ~ rho^a r^b S^c: M: a + c = 0, L: -3a + b = 0, T: -2c = 1
c_ = F(-1, 2)
a_ = -c_
b_ = 3 * a_
assert (a_ + c_, -3 * a_ + b_, -2 * c_) == (0, 0, 1) and (a_, b_, c_) == (F(1, 2), F(3, 2), F(-1, 2))
add(T, "Dimensional analysis", "Advanced", "direct",
    "The time period T of small oscillations of a liquid drop is assumed to depend only on the density ρ of the "
    "liquid, the radius r of the drop and the surface tension S. By dimensional analysis, T is proportional to:",
    place("√(ρr³/S)", ["√(S/(ρr³))", "√(ρr²/S)", "√(ρr/S)"], "B"),
    "Finding a relation by the method of dimensions",
    "Write T = k ρᵃ rᵇ Sᶜ and equate the powers of M, L and T on both sides. Surface tension is force per length, "
    "[M T⁻²], and density is [M L⁻³].",
    ["[T] = [M L⁻³]ᵃ [L]ᵇ [M T⁻²]ᶜ", "M: a + c = 0;  L: −3a + b = 0;  T: −2c = 1",
     "c = −½, a = ½, b = 3/2", "T ∝ ρ^½ r^(3/2) S^(−½) = √(ρr³/S)"],
    why="√(S/(ρr³)) is the inverse (it has the dimensions of frequency). √(ρr²/S) and √(ρr/S) do not have the "
        "dimensions of time: their L powers do not cancel.",
    ncert="Class 11 Physics, 'Units and Measurement', dimensional analysis and its applications", seconds=90)

# parallel resistors (30 +/- 0.9) and (60 +/- 1.8)
R1, d1, R2, d2 = F(30), F(9, 10), F(60), F(18, 10)
Rp = R1 * R2 / (R1 + R2)
dRp = Rp ** 2 * (d1 / R1 ** 2 + d2 / R2 ** 2)
assert Rp == 20 and dRp == F(3, 5)
assert Rp * (d1 / R1 + d2 / R2) == F(6, 5) and d1 + d2 == F(27, 10)
add(T, "Errors in measurement", "Advanced", "numerical",
    "Two resistors of resistances R₁ = (30 ± 0.9) Ω and R₂ = (60 ± 1.8) Ω are connected in parallel. The "
    "equivalent resistance, with its maximum absolute error, is:",
    place("(20.0 ± 0.6) Ω", ["(20.0 ± 1.2) Ω", "(20.0 ± 2.7) Ω", "(90.0 ± 2.7) Ω"], "C"),
    "Error in a quantity given by a reciprocal sum",
    "For 1/R = 1/R₁ + 1/R₂, differentiating gives ΔR/R² = ΔR₁/R₁² + ΔR₂/R₂² for the maximum error.",
    ["R = (30 × 60)/(30 + 60) = 20 Ω", "ΔR = R² (ΔR₁/R₁² + ΔR₂/R₂²) = 400 × (0.9/900 + 1.8/3600)",
     "ΔR = 400 × (0.001 + 0.0005) = 0.6 Ω", "R = (20.0 ± 0.6) Ω"],
    why="(20.0 ± 1.2) Ω adds the relative errors (3% + 3%) as for a product. (20.0 ± 2.7) Ω adds the absolute "
        "errors as for a sum. (90.0 ± 2.7) Ω treats the resistors as in series.",
    seconds=120, recomputed=True)

# =====================================================================================================================
# Kinematics (B4 I5 A4)
# =====================================================================================================================
T = "Kinematics"

s = F(1, 2) * 2 * 5 ** 2
assert s == 25 and 2 * 5 == 10 and 2 * 5 ** 2 == 50 and (2 * 5) ** 2 == 100
add(T, "Motion in a straight line", "Basic", "numerical",
    "A car starts from rest and moves along a straight road with a uniform acceleration of 2 m/s². The distance "
    "it covers in the first 5 s is:",
    place("25 m", ["50 m", "10 m", "100 m"], "A"),
    "Equations of uniformly accelerated motion",
    "With u = 0, the distance covered in time t is s = ½at².",
    ["s = ut + ½at²", "s = 0 + ½ × 2 × 5² = 25 m"],
    why="50 m drops the ½. 10 m is the final velocity (in m/s), not a distance. 100 m squares the product at.",
    seconds=30, recomputed=True)

add(T, "Graphs of motion", "Basic", "match_list",
    match_stem("Match List-I (feature of a motion graph) with List-II (what it gives).",
               ["Slope of a position–time graph", "Slope of a velocity–time graph",
                "Area under a velocity–time graph", "Area under an acceleration–time graph"],
               ["Change in velocity", "Displacement", "Velocity", "Acceleration"]),
    match_options({"A": "III", "B": "IV", "C": "II", "D": "I"},
                  [{"A": "IV", "B": "III", "C": "II", "D": "I"}, {"A": "III", "B": "IV", "C": "I", "D": "II"},
                   {"A": "II", "B": "IV", "C": "III", "D": "I"}], "D"),
    "Reading slopes and areas of kinematic graphs",
    "A slope is a rate of change: dx/dt = v and dv/dt = a. An area is an accumulation: ∫v dt = displacement and "
    "∫a dt = change in velocity.",
    ["Slope of x–t = dx/dt = velocity → III", "Slope of v–t = dv/dt = acceleration → IV",
     "Area under v–t = ∫v dt = displacement → II", "Area under a–t = ∫a dt = change in velocity → I"],
    why="The wrong codes swap slope and area, or confuse velocity with acceleration.",
    ncert="Class 11 Physics, 'Motion in a Straight Line', instantaneous velocity and acceleration", seconds=35)

add(T, "Vectors", "Basic", "multi_statement",
    multi("Which of the following statements about vectors are correct?",
          ["The scalar (dot) product of two vectors is commutative: A·B = B·A.",
           "The vector (cross) product of two vectors is commutative: A × B = B × A.",
           "î × ĵ = k̂ for the unit vectors of a right-handed coordinate system.",
           "The scalar product of two perpendicular vectors is zero.",
           "Two vectors of unequal magnitudes can add up to give a zero resultant."]),
    place("(a), (c) and (d) only", ["(a), (b) and (d) only", "(b), (c) and (e) only", "(a), (c), (d) and (e) only"],
          "B"),
    "Properties of scalar and vector products",
    "A·B = AB cos θ is the same either way round, and is zero when θ = 90°. The cross product changes sign when "
    "the order is reversed: B × A = −(A × B). Two vectors can cancel only if they are equal in magnitude and "
    "opposite in direction.",
    ["(a) True: AB cos θ is symmetric", "(b) False: A × B = −B × A", "(c) True: right-hand rule",
     "(d) True: cos 90° = 0", "(e) False: |A + B| ≥ |A| − |B| > 0 when the magnitudes differ"],
    ncert="Class 11 Physics, 'Motion in a Plane', scalars and vectors (scalar and vector products)", seconds=45)

add(T, "Projectile motion", "Basic", "direct",
    "For a projectile moving under gravity alone (air resistance neglected), which of the following remains "
    "constant throughout its flight?",
    place("The horizontal component of its velocity",
          ["Its speed", "The vertical component of its velocity", "Its kinetic energy"], "C"),
    "Independence of horizontal and vertical motion",
    "Gravity acts vertically, so there is no horizontal acceleration. The horizontal velocity u cos θ stays "
    "the same, while the vertical velocity changes at the rate g.",
    ["aₓ = 0 → vₓ = u cos θ throughout", "a_y = −g → v_y = u sin θ − gt changes",
     "Speed and kinetic energy depend on v_y, so they change too"],
    why="Speed and kinetic energy are least at the top and greatest at launch and landing. The vertical "
        "component decreases, becomes zero at the top, then grows downward.",
    ncert="Class 11 Physics, 'Motion in a Plane', projectile motion", seconds=25)

rel = math.hypot(12, 5)
assert rel == 13
add(T, "Relative velocity", "Intermediate", "numerical",
    "Rain is falling vertically downward with a speed of 12 m/s. A woman runs along a horizontal road with a "
    "speed of 5 m/s. The speed of the rain relative to the woman is:",
    place("13 m/s", ["17 m/s", "7 m/s", "12 m/s"], "B"),
    "Relative velocity in two dimensions",
    "Velocity of rain relative to the woman = v_rain − v_woman. The two velocities are perpendicular, so the "
    "relative velocity has components 12 m/s (down) and 5 m/s (opposite to her motion).",
    ["v_rel = v_rain − v_woman", "|v_rel| = √(12² + 5²) = √169 = 13 m/s"],
    why="17 m/s adds the speeds and 7 m/s subtracts them, as if the velocities were along one line. 12 m/s "
        "ignores the woman's motion.",
    seconds=40, recomputed=True)

g = 10
h = 80
tf = math.sqrt(2 * h / g)
last = h - F(1, 2) * g * (tf - 1) ** 2
assert tf == 4 and last == 35 and 0 + F(g, 2) * (2 * 4 - 1) == 35
add(T, "Motion in a straight line", "Intermediate", "numerical",
    "A stone is dropped from rest from the top of a tower 80 m high. Taking g = 10 m/s² and neglecting air "
    "resistance, the distance it falls during the last second of its fall is:",
    place("35 m", ["45 m", "20 m", "40 m"], "D"),
    "Free fall: distance in a particular second",
    "First find the total time of fall, then subtract the distance covered up to one second before landing.",
    ["Time of fall: 80 = ½ × 10 × t² → t = 4 s", "Distance in first 3 s = ½ × 10 × 3² = 45 m",
     "Distance in the last (4th) second = 80 − 45 = 35 m"],
    shortcut="Distance in the nth second from rest = (g/2)(2n − 1) = 5 × 7 = 35 m.",
    why="45 m is the distance in the first 3 s. 20 m is the average distance per second (80/4). 40 m is the "
        "speed (in m/s) on reaching the ground.",
    seconds=60, recomputed=True)

add(T, "Motion in a straight line", "Intermediate", "multi_statement",
    multi("Which of the following statements about motion in a straight line are correct?",
          ["A body can have zero velocity and a non-zero acceleration at the same instant.",
           "Over any time interval, the average speed is greater than or equal to the magnitude of the average "
           "velocity.",
           "If the acceleration is opposite in direction to the velocity, the speed of the body decreases.",
           "A body whose velocity–time graph is a straight line with a negative slope is always slowing down.",
           "If the distance travelled by a body is non-zero, its displacement cannot be zero."]),
    place("(a), (b) and (c) only", ["(a), (b), (c) and (d) only", "(b), (c) and (e) only", "(a), (d) and (e) only"],
          "A"),
    "Speed, velocity and acceleration",
    "A ball thrown upward has v = 0 but a = g at the top. Distance is never less than the magnitude of "
    "displacement, so average speed ≥ |average velocity|. Acceleration opposite to velocity slows the body. "
    "A straight v–t line with negative slope means constant negative acceleration: the body slows only while v is "
    "positive, then speeds up in the negative direction. A round trip has non-zero distance but zero displacement.",
    ["(a) True: top of a vertical throw", "(b) True: path length ≥ |displacement|",
     "(c) True: retardation", "(d) False: after v passes through zero, v and a point the same way and the speed increases",
     "(e) False: a round trip has zero displacement"],
    ncert="Class 11 Physics, 'Motion in a Straight Line', average velocity and average speed; acceleration",
    seconds=60)

t_fall = math.sqrt(2 * 45 / 10)
assert t_fall == 3 and 20 * t_fall == 60
assert round(20 * math.sqrt(45 / 10), 1) == 42.4 and 20 * 2 * t_fall == 120
add(T, "Projectile motion", "Intermediate", "numerical",
    "A ball is thrown horizontally with a speed of 20 m/s from the top of a cliff 45 m high. Taking g = 10 m/s², "
    "how far from the foot of the cliff does it hit the level ground below?",
    place("60 m", ["42.4 m", "120 m", "45 m"], "C"),
    "Horizontal projection",
    "The time of fall depends only on the height (vertical motion from rest). During that time the ball moves "
    "horizontally at a constant 20 m/s.",
    ["Vertical: 45 = ½ × 10 × t² → t = 3 s", "Horizontal: x = 20 × 3 = 60 m"],
    why="42.4 m uses t = √(h/g), forgetting the 2. 120 m doubles the time as if the ball also had to rise "
        "first. 45 m just equates the horizontal distance with the height.",
    seconds=45, recomputed=True)

add(T, "Uniform circular motion", "Intermediate", "assertion_reason",
    AR_STEM.format(a="In uniform circular motion, the acceleration of the particle is constant.",
                   r="In uniform circular motion, the speed of the particle is constant."),
    ar("D"),
    "Centripetal acceleration in uniform circular motion",
    "The magnitude of the acceleration, v²/R, is constant, but its direction keeps changing so that it always "
    "points towards the centre. A vector whose direction changes is not constant, so A is false. The speed is "
    "constant by definition of uniform circular motion, so R is true.",
    ["Acceleration = v²/R towards the centre; its direction rotates with the particle → not a constant vector",
     "A is false", "Speed is constant → R is true"],
    why="Options A and B need A to be true. Option C has R false, but constant speed is what 'uniform' means.",
    ncert="Class 11 Physics, 'Motion in a Plane', uniform circular motion", seconds=40)

u = 10 * math.sqrt(3)
ux, uy = u * math.cos(math.radians(60)), u * math.sin(math.radians(60))
t_perp = (ux * ux + uy * uy) / (g * uy)
assert close(t_perp, 2) and close(2 * uy / g, 3) and close(uy / g, 1.5) and close(u / g, math.sqrt(3))
add(T, "Projectile motion", "Advanced", "numerical",
    "A particle is projected from level ground with a speed of 10√3 m/s at an angle of 60° above the horizontal. "
    "Taking g = 10 m/s², after how much time does its velocity become perpendicular to its initial velocity?",
    place("2 s", ["3 s", "1.5 s", "√3 s"], "A"),
    "Velocity of a projectile as a vector; perpendicular vectors have zero dot product",
    "Write the velocity at time t in components and set its dot product with the initial velocity to zero. Then "
    "check that this time is before the particle lands.",
    ["uₓ = 10√3 cos 60° = 5√3 m/s, u_y = 10√3 sin 60° = 15 m/s",
     "v(t) = (5√3, 15 − 10t)", "u · v = 75 + 15(15 − 10t) = 300 − 150t = 0 → t = 2 s",
     "Time of flight = 2u_y/g = 3 s, so t = 2 s is during the flight"],
    shortcut="u · v = u² − g t u sin θ = 0 → t = u/(g sin θ) = 10√3/(10 × √3/2) = 2 s.",
    why="3 s is the time of flight. 1.5 s is the time to reach the top, where velocity is horizontal, not "
        "perpendicular to the initial velocity. √3 s is u/g, which drops the sin θ.",
    seconds=120, recomputed=True)

w_, vr, vs = 120, 3, 5
t_short_path = w_ / math.sqrt(vs ** 2 - vr ** 2)
assert t_short_path == 30 and w_ / vs == 24 and w_ / vr == 40 and w_ / (vs + vr) == 15
add(T, "Relative velocity", "Advanced", "numerical",
    "A river 120 m wide flows at 3 m/s. A swimmer can swim at 5 m/s relative to still water. If she wants to "
    "reach the point directly opposite her starting point, the time she takes to cross is:",
    place("30 s", ["24 s", "40 s", "15 s"], "B"),
    "Crossing a river along the shortest path",
    "To go straight across, she must head partly upstream so that the upstream component of her velocity "
    "cancels the river's 3 m/s. Only the remaining component carries her across.",
    ["Upstream component = 3 m/s → cross-stream component = √(5² − 3²) = 4 m/s", "t = 120/4 = 30 s"],
    why="24 s (120/5) is the shortest-time crossing, heading straight across and drifting downstream. 40 s divides "
        "by the river speed. 15 s divides by the sum of the speeds.",
    seconds=75, recomputed=True)

xf = lambda t: t ** 3 - 6 * t ** 2 + 9 * t
dist = abs(xf(1) - xf(0)) + abs(xf(3) - xf(1))
assert xf(1) == 4 and xf(3) == 0 and dist == 8 and 3 * 1 ** 2 - 12 * 1 + 9 == 0 and 3 * 9 - 36 + 9 == 0
add(T, "Motion in a straight line", "Advanced", "numerical",
    "The position of a particle moving along the x-axis is x = t³ − 6t² + 9t, where x is in metres and t in "
    "seconds. The distance travelled by the particle from t = 0 to t = 3 s is:",
    place("8 m", ["0 m", "4 m", "16 m"], "C"),
    "Distance versus displacement when the particle turns back",
    "Distance must be found leg by leg: find where the velocity is zero (turning points), then add the magnitudes "
    "of the displacements of each leg.",
    ["v = dx/dt = 3t² − 12t + 9 = 3(t − 1)(t − 3) → turns at t = 1 s",
     "x(0) = 0, x(1) = 1 − 6 + 9 = 4 m, x(3) = 27 − 54 + 27 = 0 m",
     "Distance = |4 − 0| + |0 − 4| = 8 m"],
    why="0 m is the displacement. 4 m counts only the first leg. 16 m counts each leg twice.",
    seconds=90, recomputed=True)

add(T, "Projectile motion", "Advanced", "statement_pair",
    SP_STEM.format(s1="For projectiles launched from level ground with the same speed, the horizontal range is the "
                      "same for angles of projection 15° and 75°.",
                   s2="For projectiles launched from level ground with the same speed, the time of flight does not "
                      "depend on the angle of projection."),
    sp("C"),
    "Range and time of flight of a projectile",
    "R = u² sin 2θ/g, and sin 30° = sin 150°, so complementary angles give equal ranges: Statement I is true. "
    "T = 2u sin θ/g depends on θ (the 75° projectile stays in the air longer), so Statement II is false.",
    ["R(15°) ∝ sin 30° = ½; R(75°) ∝ sin 150° = ½ → equal → I true",
     "T ∝ sin θ: sin 75° > sin 15° → different times → II false"],
    ncert="Class 11 Physics, 'Motion in a Plane', projectile motion", seconds=50)

# =====================================================================================================================
# Laws of Motion (B4 I5 A4)
# =====================================================================================================================
T = "Laws of Motion"

m, v1, v2 = F(2, 10), 10, -10
J = m * (v1 - v2)
assert J == 4 and m * 10 == 2 and v1 - v2 == 20
add(T, "Newton's laws and impulse", "Basic", "numerical",
    "A ball of mass 200 g moving horizontally at 10 m/s strikes a vertical wall and rebounds along the same line "
    "with the same speed. The magnitude of the impulse delivered to the ball by the wall is:",
    place("4 N s", ["2 N s", "0 N s", "20 N s"], "D"),
    "Impulse equals change in momentum",
    "Momentum is a vector. When the ball reverses direction, the change in velocity is 10 − (−10) = 20 m/s, "
    "not zero.",
    ["Take the rebound direction as positive: initial p = 0.2 × (−10) = −2 kg m/s, final p = +2 kg m/s",
     "Impulse = Δp = 2 − (−2) = 4 N s"],
    why="2 N s counts only stopping the ball, not sending it back. 0 N s treats momentum as a scalar because the "
        "speed is unchanged. 20 N s forgets to multiply the change in velocity by the mass.",
    seconds=35, recomputed=True)

add(T, "Newton's laws and impulse", "Basic", "direct",
    "Passengers standing in a bus tend to fall backward when the bus suddenly starts moving forward. This is "
    "best explained by:",
    place("Inertia of rest", ["Inertia of direction", "Newton's third law", "Conservation of energy"], "B"),
    "Newton's first law: inertia",
    "The bus floor drags the feet forward, but the upper body, having no forward force on it at first, tends to "
    "stay at rest. Relative to the bus, the passenger falls backward.",
    ["Feet move with the bus", "Upper body tends to remain at rest (inertia of rest)",
     "Relative to the accelerating bus, the body tilts backward"],
    why="Inertia of direction explains being thrown sideways on a turn. Newton's third law concerns action–reaction "
        "pairs, and energy conservation does not explain this tendency.",
    ncert="Class 11 Physics, 'Laws of Motion', Newton's first law of motion", seconds=25)

add(T, "Conservation of linear momentum", "Basic", "assertion_reason",
    AR_STEM.format(a="A gun recoils backward when a bullet is fired from it.",
                   r="When no external horizontal force acts on the gun–bullet system, its total linear momentum "
                     "is conserved, and it is zero before firing."),
    ar("A"),
    "Conservation of linear momentum",
    "Before firing, the gun and bullet are at rest, so the total momentum is zero. After firing, the bullet's "
    "forward momentum must be balanced by an equal backward momentum of the gun. R is true and is exactly why "
    "the gun recoils.",
    ["Initial momentum = 0", "Final: m_b v_b + M v_g = 0 → v_g = −m_b v_b / M (backward)",
     "So R explains A"],
    ncert="Class 11 Physics, 'Laws of Motion', conservation of momentum", seconds=30)

r_, th = 40, 45
v_bank = math.sqrt(r_ * 10 * math.tan(math.radians(th)))
assert close(v_bank, 20) and round(math.sqrt(r_ * 10 * math.sin(math.radians(45))), 1) == 16.8
assert round(math.sqrt(2 * r_ * 10), 1) == 28.3
add(T, "Circular motion: level and banked roads", "Basic", "numerical",
    "A curved road of radius 40 m is banked at 45°. Taking g = 10 m/s², the speed at which a car can take this "
    "turn without needing any friction is:",
    place("20 m/s", ["400 m/s", "16.8 m/s", "28.3 m/s"], "A"),
    "Optimum speed on a banked road",
    "At this speed the horizontal component of the normal reaction alone provides the centripetal force: "
    "N sin θ = mv²/r and N cos θ = mg, so v² = rg tan θ.",
    ["v² = r g tan θ = 40 × 10 × tan 45° = 400", "v = 20 m/s"],
    why="400 m/s forgets the square root. 16.8 m/s uses sin θ in place of tan θ. 28.3 m/s uses v² = 2rg, mixing "
        "in a free-fall formula.",
    ncert="Class 11 Physics, 'Laws of Motion', motion of a car on a banked road", seconds=40, recomputed=True)

ms, mus, muk = 5, F(4, 10), F(25, 100)
f_lim = mus * ms * 10
assert f_lim == 20 and 15 < f_lim and muk * ms * 10 == F(25, 2)
add(T, "Friction", "Intermediate", "numerical",
    "A 5 kg block rests on a horizontal floor. The coefficients of static and kinetic friction between them are "
    "0.4 and 0.25. A horizontal force of 15 N is applied to the block. Taking g = 10 m/s², the friction force on "
    "the block is:",
    place("15 N", ["20 N", "12.5 N", "0 N"], "C"),
    "Static friction is self-adjusting",
    "First check whether the block moves. The largest static friction possible is μₛN = 20 N. The applied 15 N "
    "is less than this, so the block stays at rest and static friction just balances the applied force.",
    ["N = mg = 50 N; limiting friction = 0.4 × 50 = 20 N", "Applied force 15 N < 20 N → no motion",
     "Static friction = applied force = 15 N"],
    why="20 N is the limiting (maximum) value, reached only when the block is about to slip. 12.5 N is kinetic "
        "friction, which acts only once the block slides. 0 N ignores friction altogether.",
    ncert="Class 11 Physics, 'Laws of Motion', friction", seconds=50, recomputed=True)

a_c = F(10, 3 + 2)
assert a_c == 2 and 2 * a_c == 4 and 3 * a_c == 6
add(T, "Newton's laws and impulse", "Intermediate", "numerical",
    "Two blocks of masses 3 kg and 2 kg are in contact on a smooth horizontal table. A horizontal force of 10 N "
    "is applied to the 3 kg block, pushing both blocks together. The force exerted by the 3 kg block on the 2 kg "
    "block is:",
    place("4 N", ["6 N", "10 N", "2 N"], "A"),
    "Newton's second law applied to a system and to one part of it",
    "Both blocks share the same acceleration. The only horizontal force on the 2 kg block is the contact force, "
    "so it must equal (2 kg) × a.",
    ["Whole system: a = 10/(3 + 2) = 2 m/s²", "2 kg block alone: contact force = 2 × 2 = 4 N"],
    why="6 N is the net force on the 3 kg block, not the contact force. 10 N assumes the full applied force is "
        "passed on. 2 N is the acceleration in m/s².",
    seconds=45, recomputed=True)

add(T, "Circular motion: level and banked roads", "Intermediate", "match_list",
    match_stem("Match List-I (body moving in a circle) with List-II (force that provides the centripetal force).",
               ["A car taking a turn on a level (unbanked) road", "A satellite in a circular orbit around the Earth",
                "A stone whirled in a horizontal circle at the end of a string",
                "An electron revolving around the nucleus in Bohr's model of the hydrogen atom"],
               ["Gravitational force", "Tension", "Friction", "Electrostatic attraction"]),
    match_options({"A": "III", "B": "I", "C": "II", "D": "IV"},
                  [{"A": "II", "B": "I", "C": "III", "D": "IV"}, {"A": "III", "B": "IV", "C": "II", "D": "I"},
                   {"A": "I", "B": "III", "C": "II", "D": "IV"}], "B"),
    "Centripetal force is supplied by a real force",
    "Centripetal force is not a new kind of force; in each case some real force points towards the centre.",
    ["Car on a level road: static friction between tyres and road → III",
     "Satellite: Earth's gravitational pull → I", "Stone on a string: tension in the string → II",
     "Electron in Bohr's model: Coulomb attraction of the nucleus → IV"],
    why="The other codes swap friction with tension, or gravity with the electrostatic force.",
    ncert="Class 11 Physics, 'Laws of Motion', dynamics of uniform circular motion", seconds=35)

add(T, "Equilibrium of concurrent forces", "Intermediate", "statement_pair",
    SP_STEM.format(s1="Three forces of magnitudes 3 N, 4 N and 8 N, acting at a point, can keep a particle in "
                      "equilibrium.",
                   s2="A particle acted on by concurrent forces is in equilibrium only if the vector sum of the "
                      "forces is zero."),
    sp("D"),
    "Equilibrium of concurrent forces",
    "For equilibrium the forces must form a closed triangle, so the largest force cannot exceed the sum of the "
    "other two. The resultant of 3 N and 4 N lies between 1 N and 7 N, so it can never balance 8 N: Statement I "
    "is false. Statement II is the condition for equilibrium: true.",
    ["Resultant of 3 N and 4 N: 1 N ≤ R ≤ 7 N", "8 N > 7 N → cannot be balanced → I false",
     "Equilibrium ⇔ ΣF = 0 → II true"],
    ncert="Class 11 Physics, 'Laws of Motion', equilibrium of a particle", seconds=40)

add(T, "Friction", "Intermediate", "assertion_reason",
    AR_STEM.format(a="It is easier to pull a lawn roller by a handle inclined above the horizontal than to push it "
                     "with the same handle.",
                   r="While pulling, the vertical component of the applied force acts upward and reduces the normal "
                     "reaction, and hence the friction force; while pushing, it acts downward and increases them."),
    ar("A"),
    "Friction depends on the normal reaction",
    "Friction is proportional to the normal reaction. Pulling at an angle θ gives N = mg − F sin θ; pushing gives "
    "N = mg + F sin θ. Less normal reaction means less friction to overcome, so pulling is easier. R is true and "
    "explains A.",
    ["Pull: N = mg − F sin θ → smaller friction", "Push: N = mg + F sin θ → larger friction",
     "R gives the reason for A"],
    seconds=40)

th = math.radians(30)
muk2 = 1 / (2 * math.sqrt(3))
a_inc = 10 * (math.sin(th) - muk2 * math.cos(th))
assert close(a_inc, 2.5) and close(10 * math.sin(th), 5) and close(10 * (math.sin(th) + muk2 * math.cos(th)), 7.5)
assert round(10 * (math.sin(th) - muk2 * math.sin(th)), 1) == 3.6
add(T, "Friction", "Advanced", "numerical",
    "A block slides down a rough plane inclined at 30° to the horizontal. The coefficient of kinetic friction "
    "between the block and the plane is 1/(2√3). Taking g = 10 m/s², the acceleration of the block is:",
    place("2.5 m/s²", ["5.0 m/s²", "7.5 m/s²", "3.6 m/s²"], "D"),
    "Motion on a rough inclined plane",
    "Along the incline, the gravity component mg sin θ pulls the block down and kinetic friction μₖmg cos θ acts "
    "up the incline (opposing the sliding).",
    ["a = g(sin θ − μₖ cos θ)", "= 10 × (½ − (1/(2√3)) × (√3/2))", "= 10 × (0.5 − 0.25) = 2.5 m/s²"],
    why="5.0 m/s² ignores friction. 7.5 m/s² adds friction as if it helped the motion. 3.6 m/s² takes friction as "
        "μₖ mg sin θ instead of μₖ mg cos θ.",
    seconds=75, recomputed=True)

p_each = 1 * 30
p3 = math.hypot(p_each, p_each)
v3 = p3 / 2
assert close(v3, 15 * math.sqrt(2)) and close(p3, 30 * math.sqrt(2)) and close(p3 / 3, 10 * math.sqrt(2))
add(T, "Conservation of linear momentum", "Advanced", "numerical",
    "A shell of mass 4 kg at rest explodes into three pieces. Two pieces, each of mass 1 kg, fly off "
    "perpendicular to each other, each with a speed of 30 m/s. The speed of the third piece is:",
    place("15√2 m/s", ["30√2 m/s", "30 m/s", "10√2 m/s"], "B"),
    "Conservation of linear momentum in two dimensions",
    "The total momentum is zero before and after the explosion. So the third piece (mass 4 − 1 − 1 = 2 kg) "
    "must carry momentum equal and opposite to the vector sum of the other two.",
    ["Momentum of each 1 kg piece = 30 kg m/s, at right angles", "Their resultant = √(30² + 30²) = 30√2 kg m/s",
     "Third piece: 2 × v = 30√2 → v = 15√2 m/s ≈ 21.2 m/s"],
    why="30√2 m/s forgets to divide by the 2 kg mass of the third piece. 30 m/s adds the momenta as scalars "
        "(60/2). 10√2 m/s divides by 3 kg instead of the 2 kg mass of the third piece.",
    seconds=90, recomputed=True)

m1, m2 = 3, 5
Ten = F(2 * m1 * m2 * 10, m1 + m2)
assert Ten == F(75, 2) and (m2 - m1) * 10 == 20
add(T, "Newton's laws and impulse", "Advanced", "numerical",
    "Two blocks of masses 3 kg and 5 kg hang at the two ends of a light inextensible string passing over a "
    "smooth, light pulley. The system is released from rest. Taking g = 10 m/s², the tension in the string is:",
    place("37.5 N", ["30 N", "50 N", "20 N"], "C"),
    "Newton's second law for connected bodies",
    "The heavier block accelerates down and the lighter one up with the same acceleration a. Write F = ma for each "
    "block separately and solve for T.",
    ["a = (m₂ − m₁)g/(m₁ + m₂) = (5 − 3) × 10/8 = 2.5 m/s²", "For the 3 kg block: T − 30 = 3 × 2.5 → T = 37.5 N",
     "Check with the 5 kg block: 50 − T = 5 × 2.5 → T = 37.5 N"],
    shortcut="T = 2m₁m₂g/(m₁ + m₂) = 2 × 3 × 5 × 10/8 = 37.5 N.",
    why="30 N and 50 N are the weights of the blocks; the tension lies between them because both blocks "
        "accelerate. 20 N is the net driving force (m₂ − m₁)g.",
    seconds=75, recomputed=True)

add(T, "Friction", "Advanced", "multi_statement",
    multi("Which of the following statements about friction are correct?",
          ["Static friction is self-adjusting: it takes any value up to a limiting value.",
           "For a given pair of surfaces, the coefficient of kinetic friction is generally less than the "
           "coefficient of static friction.",
           "For the same normal reaction, limiting friction increases with the area of contact.",
           "Kinetic friction acts opposite to the velocity of a body relative to the surface it slides on.",
           "Rolling friction is generally much smaller than sliding friction."]),
    place("(a), (b), (d) and (e) only", ["(a), (b) and (c) only", "(b), (c) and (d) only",
                                         "(a), (c), (d) and (e) only"], "A"),
    "Laws of friction",
    "Static friction matches the applied force up to μₛN; once sliding starts, μₖ (usually smaller than μₛ) "
    "applies. Limiting friction depends on the normal reaction, not on the area of contact. Friction opposes "
    "relative motion. Rolling friction is much smaller, which is why wheels and ball bearings help.",
    ["(a) True", "(b) True: μₖ < μₛ", "(c) False: independent of area of contact",
     "(d) True: kinetic friction opposes relative velocity", "(e) True"],
    why="Every other option includes (c), the area trap, or leaves out a true statement.",
    ncert="Class 11 Physics, 'Laws of Motion', friction (static, kinetic and rolling friction)", seconds=60)

# =====================================================================================================================
# Work, Energy and Power (B3 I4 A3)
# =====================================================================================================================
T = "Work, Energy and Power"

add(T, "Work by constant and variable force", "Basic", "direct",
    "A stone tied to a string is whirled in a horizontal circle with constant speed. The work done by the tension "
    "in the string during one complete revolution is:",
    place("Zero", ["Positive", "Negative", "Equal to the kinetic energy of the stone"], "C"),
    "Work done by a force perpendicular to displacement",
    "In uniform circular motion the tension points towards the centre, while each small displacement is along the "
    "tangent. Since F ⊥ ds at every instant, W = ∫F·ds = 0. This agrees with the work-energy theorem: the speed, "
    "and so the kinetic energy, does not change.",
    ["F (radial) ⊥ ds (tangential) → F·ds = 0", "W = 0 for every part of the circle"],
    why="A force always at 90° to the motion can change the direction of the velocity but not the speed, so it "
        "does no work, neither positive nor negative.",
    ncert="Class 11 Physics, 'Work, Energy and Power', the scalar product and work", seconds=25)

k_, x_ = 200, F(1, 10)
U = F(1, 2) * k_ * x_ ** 2
assert U == 1 and k_ * x_ ** 2 == 2 and k_ * x_ == 20 and F(1, 2) * k_ * x_ == 10
add(T, "Spring potential energy", "Basic", "numerical",
    "A spring of spring constant 200 N/m is compressed by 10 cm from its natural length. The potential energy "
    "stored in the spring is:",
    place("1 J", ["2 J", "20 J", "10 J"], "B"),
    "Elastic potential energy of a spring",
    "The work done in compressing the spring against the force kx is stored as U = ½kx².",
    ["x = 10 cm = 0.1 m", "U = ½ × 200 × (0.1)² = 1 J"],
    why="2 J drops the ½. 20 J is the spring force kx (in newtons), not energy. 10 J uses ½kx instead of ½kx².",
    seconds=30, recomputed=True)

assert 1000 * 3600 == 3_600_000
add(T, "Power", "Basic", "statement_pair",
    SP_STEM.format(s1="Power is the rate at which work is done, and its SI unit is the watt.",
                   s2="One kilowatt hour (kWh) is equal to 3.6 × 10⁶ J."),
    sp("A"),
    "Power and the commercial unit of energy",
    "P = dW/dt, measured in J/s = W, so Statement I is true. 1 kWh = 1000 W × 3600 s = 3.6 × 10⁶ J, so "
    "Statement II is true. The kWh is a unit of energy, not of power.",
    ["P = W/t → watt (J s⁻¹) → I true", "1 kWh = 10³ × 3600 J = 3.6 × 10⁶ J → II true"],
    ncert="Class 11 Physics, 'Work, Energy and Power', power", seconds=30)

add(T, "Collisions", "Intermediate", "match_list",
    match_stem("Match List-I (type of collision) with List-II (its feature). All collisions are head-on, in one "
               "dimension.",
               ["Perfectly elastic collision", "Perfectly inelastic collision",
                "Elastic collision of two equal masses, one initially at rest",
                "Elastic collision of a very light body with a very heavy body at rest"],
               ["The velocities of the two bodies are exchanged",
                "The light body rebounds with nearly its original speed",
                "The bodies move together after the collision",
                "The total kinetic energy after the collision equals that before it"]),
    match_options({"A": "IV", "B": "III", "C": "I", "D": "II"},
                  [{"A": "III", "B": "IV", "C": "I", "D": "II"}, {"A": "IV", "B": "III", "C": "II", "D": "I"},
                   {"A": "IV", "B": "I", "C": "III", "D": "II"}], "D"),
    "Elastic and inelastic collisions in one dimension",
    "In every collision momentum is conserved. In an elastic collision the total kinetic energy is also the same "
    "before and after. In a perfectly inelastic one the bodies stick together. The elastic results "
    "v₁ = (m₁ − m₂)u/(m₁ + m₂) and v₂ = 2m₁u/(m₁ + m₂) give the two special cases.",
    ["Perfectly elastic: KE after = KE before → IV", "Perfectly inelastic: bodies stick and move together → III",
     "m₁ = m₂: v₁ = 0, v₂ = u → velocities exchanged → I",
     "m₁ ≪ m₂: v₁ ≈ −u, v₂ ≈ 0 → light body rebounds with nearly the same speed → II"],
    why="The other codes swap the two general cases (IV and III) or the two special cases (I and II).",
    ncert="Class 11 Physics, 'Work, Energy and Power', collisions in one dimension", seconds=45)

W_var = F(2) ** 3
assert W_var == 8 and 3 * 2 ** 2 * 2 == 24 and F(0 + 12, 2) * 2 == 12 and round(8 / 3, 2) == 2.67
add(T, "Work by constant and variable force", "Intermediate", "numerical",
    "A force F = 3x² N, where x is in metres, acts on a particle along the x-axis. The work done by this force as "
    "the particle moves from x = 0 to x = 2 m is:",
    place("8 J", ["24 J", "12 J", "2.67 J"], "A"),
    "Work done by a variable force",
    "When the force changes with position, the work is the area under the F–x curve: W = ∫F dx.",
    ["W = ∫₀² 3x² dx", "= [x³]₀² = 8 J"],
    why="24 J multiplies the final force (12 N) by the displacement, as if the force were constant. 12 J uses the "
        "average of the end forces, which works only for a force linear in x. 2.67 J integrates x² but drops the "
        "factor 3.",
    seconds=45, recomputed=True)

add(T, "Work-energy theorem", "Intermediate", "assertion_reason",
    AR_STEM.format(a="The work done by friction on a body can be positive.",
                   r="Friction always opposes the motion of a body."),
    ar("C"),
    "Friction opposes relative motion, not motion",
    "A box on the floor of a truck that is speeding up is carried forward by static friction from the floor. That "
    "friction acts along the box's displacement, so it does positive work and increases the box's kinetic energy: "
    "A is true. Friction opposes relative motion between the surfaces, not the motion of the body itself, so R is "
    "false.",
    ["Box on an accelerating truck: friction forward, displacement forward → W > 0 → A true",
     "Friction opposes relative motion (slipping), not motion as such → R false"],
    why="Options A and B need R to be true. Option D is wrong because A is true.",
    ncert="Class 11 Physics, 'Laws of Motion', friction", seconds=45)

r_vc = 1.6
v_min = math.sqrt(5 * 10 * r_vc)
assert close(v_min, 4 * math.sqrt(5)) and close(math.sqrt(10 * r_vc), 4)
assert close(math.sqrt(2 * 10 * r_vc), 4 * math.sqrt(2)) and close(math.sqrt(4 * 10 * r_vc), 8)
add(T, "Motion in a vertical circle", "Intermediate", "numerical",
    "A small stone tied to a light string of length 1.6 m is whirled in a vertical circle. Taking g = 10 m/s², "
    "the minimum speed it must have at the lowest point to just complete the circle is:",
    place("4√5 m/s", ["4 m/s", "4√2 m/s", "8 m/s"], "C"),
    "Minimum speed in a vertical circle (string)",
    "A string can only pull. At the top the string just goes slack when gravity alone provides the centripetal "
    "force: v_top² = gr. Energy conservation from the bottom to the top (a rise of 2r) then gives v_bottom.",
    ["Top: mg = mv_top²/r → v_top² = gr = 16", "Bottom: v² = v_top² + 2g(2r) = gr + 4gr = 5gr",
     "v = √(5 × 10 × 1.6) = √80 = 4√5 m/s ≈ 8.9 m/s"],
    why="4 m/s is the minimum speed at the top, √(gr). 4√2 m/s is √(2gr). 8 m/s is √(4gr), which is right for a "
        "rigid rod (it can push, so the speed at the top may be zero) but not for a string.",
    ncert="Class 11 Physics, 'Work, Energy and Power', motion in a vertical circle", seconds=75, recomputed=True)

ma, ua, mb = 2, 6, 4
vb = F(2 * ma * ua, ma + mb)
va = F((ma - mb) * ua, ma + mb)
frac = (F(1, 2) * mb * vb ** 2) / (F(1, 2) * ma * ua ** 2)
assert vb == 4 and va == -2 and frac == F(8, 9) and 1 - frac == F(1, 9) and vb / ua == F(2, 3)
assert (vb / ua) ** 2 == F(4, 9) and F(4 * ma * mb, (ma + mb) ** 2) == frac
add(T, "Collisions", "Advanced", "numerical",
    "A body of mass 2 kg moving at 6 m/s collides head-on and elastically with a body of mass 4 kg at rest. "
    "The fraction of the initial kinetic energy transferred to the 4 kg body is:",
    place("8/9", ["1/9", "2/3", "4/9"], "D"),
    "Elastic collision in one dimension",
    "Use the elastic-collision results for a target at rest to find the velocity of the 4 kg body, then compare "
    "kinetic energies.",
    ["v₂ = 2m₁u/(m₁ + m₂) = 2 × 2 × 6/6 = 4 m/s (and v₁ = −2 m/s)",
     "KE given to the 4 kg body = ½ × 4 × 4² = 32 J; initial KE = ½ × 2 × 6² = 36 J",
     "Fraction = 32/36 = 8/9"],
    shortcut="Fraction transferred = 4m₁m₂/(m₁ + m₂)² = 4 × 2 × 4/36 = 8/9.",
    why="1/9 is the fraction kept by the 2 kg body. 2/3 is the velocity ratio v₂/u. 4/9 squares the velocity "
        "ratio but ignores the different masses.",
    seconds=90, recomputed=True)

mbul, vbul, mblk = F(1, 100), 200, F(99, 100)
V = mbul * vbul / (mbul + mblk)
H_rise = V ** 2 / (2 * 10)
assert V == 2 and H_rise == F(1, 5) and F(1, 2) * mbul * vbul ** 2 / (1 * 10) == 20
assert V ** 2 / 10 == F(2, 5) and V ** 2 / 40 == F(1, 10)
add(T, "Collisions", "Advanced", "numerical",
    "A bullet of mass 10 g moving horizontally at 200 m/s gets embedded in a wooden block of mass 990 g "
    "suspended by a long string. Taking g = 10 m/s², the maximum height through which the block (with the "
    "bullet) rises is:",
    place("0.2 m", ["20 m", "0.4 m", "0.1 m"], "B"),
    "Perfectly inelastic collision followed by energy conservation",
    "Two stages. During the collision only momentum is conserved (kinetic energy is lost as heat). After the "
    "collision, mechanical energy is conserved as the block swings up.",
    ["Collision: 0.01 × 200 = (0.01 + 0.99) V → V = 2 m/s",
     "Swing: ½(1)V² = (1)(10)h → h = V²/2g = 4/20 = 0.2 m"],
    why="20 m wrongly conserves kinetic energy through the collision (200 J = 1 kg × 10 × h). 0.4 m uses h = V²/g. "
        "0.1 m uses h = V²/4g.",
    seconds=90, recomputed=True)

add(T, "Collisions", "Advanced", "multi_statement",
    multi("Which of the following statements are correct?",
          ["In an elastic collision, the total kinetic energy is conserved at every instant during the collision.",
           "Total linear momentum of an isolated system is conserved in both elastic and inelastic collisions.",
           "The work done by a conservative force on a body moving around a closed path is zero.",
           "The total mechanical energy of a body sliding on a rough surface remains constant.",
           "In an inelastic collision, part of the initial kinetic energy is converted into other forms such as "
           "heat, sound and energy of deformation."]),
    place("(b), (c) and (e) only", ["(a), (b) and (c) only", "(b), (c), (d) and (e) only",
                                    "(a), (b), (c) and (e) only"], "A"),
    "Momentum, kinetic energy and conservative forces",
    "During any collision the bodies deform and some kinetic energy is temporarily stored; only in the elastic "
    "case is the total after the collision equal to that before. Momentum is conserved in all collisions of an "
    "isolated system. Friction is non-conservative, so it reduces mechanical energy.",
    ["(a) False: KE is not conserved during the short time of deformation",
     "(b) True", "(c) True: definition of a conservative force", "(d) False: kinetic friction dissipates energy",
     "(e) True"],
    why="Options with (a) miss the 'during the collision' trap; the option with (d) ignores that friction is "
        "non-conservative.",
    ncert="Class 11 Physics, 'Work, Energy and Power', conservative forces and collisions", seconds=60)

# =====================================================================================================================
# Rotational Motion (B4 I5 A4)
# =====================================================================================================================
T = "Rotational Motion"

xcm = F(2 * 0 + 3 * 5, 2 + 3)
assert xcm == 3 and 5 - xcm == 2 and F(15, 2) == F(15, 2)
add(T, "Centre of mass", "Basic", "numerical",
    "Two particles of masses 2 kg and 3 kg are placed on the x-axis at x = 0 and x = 5 m respectively. The "
    "position of their centre of mass is:",
    place("x = 3 m", ["x = 2 m", "x = 2.5 m", "x = 7.5 m"], "D"),
    "Centre of mass of a two-particle system",
    "X = (m₁x₁ + m₂x₂)/(m₁ + m₂). The centre of mass lies closer to the heavier particle.",
    ["X = (2 × 0 + 3 × 5)/(2 + 3) = 15/5 = 3 m"],
    why="2 m is the distance from the heavier particle, i.e. the masses were swapped. 2.5 m is the midpoint, "
        "right only for equal masses. 7.5 m divides by 2 kg alone instead of the total mass.",
    ncert="Class 11 Physics, 'System of Particles and Rotational Motion', centre of mass", seconds=30,
    recomputed=True)

add(T, "Rigid-body rotation", "Basic", "match_list",
    match_stem("Match List-I (quantity in linear motion) with List-II (its analogue in rotational motion).",
               ["Mass", "Force", "Linear momentum", "Linear velocity"],
               ["Torque", "Angular momentum", "Moment of inertia", "Angular velocity"]),
    match_options({"A": "III", "B": "I", "C": "II", "D": "IV"},
                  [{"A": "I", "B": "III", "C": "II", "D": "IV"}, {"A": "III", "B": "II", "C": "I", "D": "IV"},
                   {"A": "IV", "B": "I", "C": "II", "D": "III"}], "B"),
    "Comparison of translational and rotational motion",
    "Every translational quantity has a rotational analogue: F = ma corresponds to τ = Iα, p = mv to L = Iω.",
    ["Mass m ↔ moment of inertia I → III", "Force F ↔ torque τ → I", "Linear momentum p ↔ angular momentum L → II",
     "Velocity v ↔ angular velocity ω → IV"],
    why="The wrong codes swap force with mass, or momentum with force, which breaks F = ma ↔ τ = Iα.",
    ncert="Class 11 Physics, 'System of Particles and Rotational Motion', comparison of translational and "
          "rotational motion", seconds=30)

add(T, "Moment of inertia and axis theorems", "Basic", "direct",
    "The moment of inertia of a rigid body about a given axis does NOT depend on:",
    place("The angular velocity of the body", ["The mass of the body", "How the mass is distributed about the axis",
                                                "The position and orientation of the axis"], "D"),
    "What moment of inertia depends on",
    "I = Σmᵢrᵢ², where rᵢ is the perpendicular distance of each particle from the axis. It depends on the masses "
    "and their distances from the chosen axis, but not on how fast the body is rotating.",
    ["I = Σ mᵢ rᵢ²", "Depends on mass, its distribution and the axis", "ω does not appear → independent of ω"],
    why="Mass, mass distribution and the choice of axis all enter Σmᵢrᵢ² directly.",
    ncert="Class 11 Physics, 'System of Particles and Rotational Motion', moment of inertia", seconds=25)

add(T, "Torque and angular momentum", "Basic", "assertion_reason",
    AR_STEM.format(a="A diver pulls in her arms and legs during a somersault to spin faster.",
                   r="When no external torque acts, angular momentum Iω is conserved, so reducing the moment of "
                     "inertia increases the angular speed."),
    ar("A"),
    "Conservation of angular momentum",
    "Gravity acts at the centre of mass, so it gives no torque about it: angular momentum about the centre of mass "
    "stays constant. Tucking in brings mass closer to the axis, I falls and ω rises. R is true and explains A.",
    ["No external torque about the centre of mass → Iω = constant", "Tuck in → I decreases → ω increases",
     "R explains A"],
    ncert="Class 11 Physics, 'System of Particles and Rotational Motion', conservation of angular momentum",
    seconds=30)

add(T, "Moment of inertia and axis theorems", "Intermediate", "match_list",
    match_stem("Match List-I (body of mass M) with List-II (its moment of inertia about the stated axis).",
               ["Thin rod of length L, about an axis perpendicular to it through its centre",
                "Thin circular ring of radius R, about a diameter",
                "Uniform circular disc of radius R, about a diameter",
                "Uniform solid sphere of radius R, about a diameter"],
               ["MR²/4", "2MR²/5", "ML²/12", "MR²/2"]),
    match_options({"A": "III", "B": "IV", "C": "I", "D": "II"},
                  [{"A": "III", "B": "I", "C": "IV", "D": "II"}, {"A": "III", "B": "IV", "C": "II", "D": "I"},
                   {"A": "I", "B": "IV", "C": "III", "D": "II"}], "C"),
    "Moments of inertia of standard bodies",
    "For the ring and the disc, the diameter values follow from the perpendicular axis theorem: the moment of "
    "inertia about the central axis normal to the plane (MR² for a ring, MR²/2 for a disc) equals the sum of the "
    "moments about two perpendicular diameters.",
    ["Rod about its centre: ML²/12 → III", "Ring about a diameter: MR²/2 (half of MR²) → IV",
     "Disc about a diameter: MR²/4 (half of MR²/2) → I", "Solid sphere about a diameter: 2MR²/5 → II"],
    why="The usual slips are swapping the ring and disc values, or taking the sphere as MR²/4.",
    ncert="Class 11 Physics, 'System of Particles and Rotational Motion', moment of inertia (table of simple "
          "bodies)", seconds=45)

I0, w0 = F(1), F(1)
w_f = I0 * w0 / (2 * I0)
KE_i, KE_f = F(1, 2) * I0 * w0 ** 2, F(1, 2) * (2 * I0) * w_f ** 2
assert w_f == F(1, 2) and (KE_i - KE_f) / KE_i == F(1, 2) and 1 - (w_f / w0) ** 2 == F(3, 4)
add(T, "Torque and angular momentum", "Intermediate", "numerical",
    "A disc rotates freely about a fixed vertical axis through its centre with angular velocity ω. An identical "
    "disc, initially not rotating, is gently placed on it coaxially, and the two soon rotate together. The "
    "fraction of the initial rotational kinetic energy that is lost is:",
    place("1/2", ["3/4", "0", "1/4"], "B"),
    "Conservation of angular momentum with loss of kinetic energy",
    "There is no external torque about the axis, so angular momentum is conserved. Kinetic energy is not "
    "conserved: friction between the discs, which brings them to a common speed, turns some of it into heat.",
    ["Iω = (2I)ω' → ω' = ω/2", "KE_initial = ½Iω²; KE_final = ½(2I)(ω/2)² = ¼Iω²",
     "Fraction lost = (½ − ¼)/½ = 1/2"],
    why="3/4 takes the final kinetic energy as ½Iω'² with the original I, forgetting the doubled moment of inertia. "
        "0 wrongly assumes kinetic energy is conserved. 1/4 reports the final energy as a fraction of Iω², not the "
        "fraction lost.",
    seconds=75, recomputed=True)

add(T, "Rigid-body rotation", "Intermediate", "statement_pair",
    SP_STEM.format(s1="When a rigid body rotates about a fixed axis, all its particles have the same linear speed.",
                   s2="When a rigid body rotates about a fixed axis, all its particles have the same angular "
                      "velocity."),
    sp("D"),
    "Kinematics of rotation about a fixed axis",
    "Each particle moves in a circle centred on the axis, and the whole body turns through the same angle in the "
    "same time, so ω is common: Statement II is true. Linear speed v = ωr grows with distance r from the axis, so "
    "Statement I is false.",
    ["v = ωr → particles farther from the axis move faster → I false", "Same ω for all particles → II true"],
    ncert="Class 11 Physics, 'System of Particles and Rotational Motion', angular velocity and its relation with "
          "linear velocity", seconds=30)

Fd, Md, Rd = 10, 4, F(1, 2)
alpha = Fd * Rd / (F(1, 2) * Md * Rd ** 2)
assert alpha == 10 and Fd * Rd / (Md * Rd ** 2) == 5 and Fd / (F(1, 2) * Md * Rd ** 2) == 20 and F(Fd, Md) == F(5, 2)
add(T, "Rigid-body rotation", "Intermediate", "numerical",
    "A light string is wound round the rim of a uniform disc of mass 4 kg and radius 0.5 m, which can rotate "
    "freely about a fixed horizontal axis through its centre. The string is pulled with a constant force of 10 N. "
    "The angular acceleration of the disc is:",
    place("10 rad/s²", ["5 rad/s²", "20 rad/s²", "2.5 rad/s²"], "A"),
    "Torque and angular acceleration: τ = Iα",
    "The string pulls tangentially at the rim, so the torque is F × R. A uniform disc about its central axis has "
    "I = ½MR².",
    ["τ = FR = 10 × 0.5 = 5 N m", "I = ½ × 4 × 0.5² = 0.5 kg m²", "α = τ/I = 5/0.5 = 10 rad/s²"],
    why="5 rad/s² uses I = MR² (a ring). 20 rad/s² takes the torque as just F = 10, without the lever arm R. "
        "2.5 rad/s² is F/M, a linear acceleration, not an angular one.",
    seconds=60, recomputed=True)

add(T, "Equilibrium of rigid bodies", "Intermediate", "statement_pair",
    SP_STEM.format(s1="A rigid body is in mechanical equilibrium only if both the net external force and the net "
                      "external torque on it are zero.",
                   s2="A couple (two equal and opposite forces with different lines of action) produces translation "
                      "of a body without rotation."),
    sp("C"),
    "Conditions of equilibrium; the couple",
    "Zero net force gives translational equilibrium, zero net torque gives rotational equilibrium; both are "
    "needed, so Statement I is true. A couple has zero net force (no translation) but a non-zero torque, so it "
    "produces rotation without translation: Statement II is false.",
    ["Equilibrium: ΣF = 0 and Στ = 0 → I true", "Couple: ΣF = 0 but τ ≠ 0 → rotation only → II false"],
    ncert="Class 11 Physics, 'System of Particles and Rotational Motion', equilibrium of a rigid body; couple",
    seconds=35)

Mr, Rr = 2, F(2, 10)
I_rim = F(1, 2) * Mr * Rr ** 2 + Mr * Rr ** 2
assert I_rim == F(12, 100) and F(1, 2) * Mr * Rr ** 2 == F(4, 100) and 2 * Mr * Rr ** 2 == F(16, 100)
assert F(1, 4) * Mr * Rr ** 2 + Mr * Rr ** 2 == F(10, 100)
add(T, "Moment of inertia and axis theorems", "Advanced", "numerical",
    "A uniform disc has mass 2 kg and radius 20 cm. Its moment of inertia about an axis perpendicular to its "
    "plane and passing through a point on its rim is:",
    place("0.12 kg m²", ["0.04 kg m²", "0.16 kg m²", "0.10 kg m²"], "B"),
    "Theorem of parallel axes",
    "Start from the axis through the centre perpendicular to the plane (I = ½MR²) and shift it parallel by R to "
    "the rim: I = I_cm + MR².",
    ["I_cm = ½MR² = ½ × 2 × 0.2² = 0.04 kg m²", "Parallel axis at distance R: I = 0.04 + 2 × 0.2² = 0.04 + 0.08",
     "I = 0.12 kg m² (= 3MR²/2)"],
    why="0.04 kg m² is the value about the central axis. 0.16 kg m² uses MR² for the central axis (a ring). "
        "0.10 kg m² starts from the diameter value MR²/4, but the required axis is parallel to the central "
        "perpendicular axis, not to a diameter.",
    seconds=75, recomputed=True)

Wb, Wl, Lb, xl = 200, 400, 4, 1
RL = F(Wb * (Lb - F(Lb, 2)) + Wl * (Lb - xl), Lb)
RR = Wb + Wl - RL
assert RL == 400 and RR == 200 and (Wb + Wl) / 2 == 300
add(T, "Equilibrium of rigid bodies", "Advanced", "numerical",
    "A uniform beam 4 m long and of mass 20 kg rests horizontally on two supports at its ends. A load of mass "
    "40 kg is placed on it 1 m from the left end. Taking g = 10 m/s², the reaction force at the left support is:",
    place("400 N", ["200 N", "300 N", "600 N"], "D"),
    "Rotational and translational equilibrium",
    "Take moments about the right support, so its unknown reaction drops out. The beam's weight acts at its "
    "centre (2 m from either end) and the load is 3 m from the right end.",
    ["Moments about the right end: R_L × 4 = 200 × 2 + 400 × 3 = 1600", "R_L = 400 N",
     "Check: R_R = 600 − 400 = 200 N"],
    why="200 N is the reaction at the right support. 300 N shares the total weight equally, ignoring where the load "
        "is. 600 N puts the whole weight on one support.",
    seconds=90, recomputed=True)

mp, yline, vx = 2, 3, 4
Lz = mp * (0 * 0 - yline * vx)  # r = (x, 3, 0), v = (4, 0, 0): (r x v)_z = x*0 - 3*4
assert abs(Lz) == 24 and yline * vx == 12 and mp * vx == 8
add(T, "Torque and angular momentum", "Advanced", "numerical",
    "A particle of mass 2 kg moves with a constant velocity of 4 m/s along the line y = 3 m in the x–y plane, "
    "parallel to the x-axis. The magnitude of its angular momentum about the origin is:",
    place("24 kg m²/s", ["0", "12 kg m²/s", "8 kg m²/s"], "C"),
    "Angular momentum of a particle moving in a straight line",
    "L = r × p. Its magnitude is p times the perpendicular distance of the line of motion from the origin, which "
    "is 3 m for every position on the line. So L is constant even though the particle moves in a straight line.",
    ["p = mv = 2 × 4 = 8 kg m/s", "Perpendicular distance of the line y = 3 m from the origin = 3 m",
     "|L| = p × d = 8 × 3 = 24 kg m²/s"],
    why="0 assumes a particle moving in a straight line has no angular momentum; that is true only about points on "
        "its line of motion. 12 kg m²/s forgets the mass. 8 kg m²/s is the linear momentum.",
    seconds=60, recomputed=True)

add(T, "Centre of mass", "Advanced", "multi_statement",
    multi("Which of the following statements are correct?",
          ["The centre of mass of a body may lie at a point where there is no mass of the body.",
           "The centre of mass of a system moves as if all the mass were concentrated there and all the external "
           "forces acted there.",
           "Internal forces between the particles of a system can change the velocity of its centre of mass.",
           "For the same mass and radius, a thin ring has a greater moment of inertia than a uniform disc about "
           "their central axes perpendicular to their planes.",
           "If the net external force on a system is zero, its centre of mass must be at rest."]),
    place("(a), (b) and (d) only", ["(a), (c) and (d) only", "(b), (d) and (e) only", "(a), (b), (d) and (e) only"],
          "B"),
    "Motion of the centre of mass; distribution of mass",
    "The centre of mass of a ring is at its centre, where there is no material. Internal forces cancel in pairs "
    "(Newton's third law), so only external forces change the motion of the centre of mass. With zero external "
    "force the centre of mass moves with constant velocity, which need not be zero. A ring has all its mass at "
    "distance R (MR²), a disc has much of it nearer the axis (MR²/2).",
    ["(a) True: e.g. a ring", "(b) True: M a_cm = F_ext", "(c) False: internal forces cancel in pairs",
     "(d) True: MR² > MR²/2", "(e) False: v_cm is constant, not necessarily zero"],
    ncert="Class 11 Physics, 'System of Particles and Rotational Motion', motion of centre of mass", seconds=60)

# =====================================================================================================================
# Gravitation (B3 I4 A3)
# =====================================================================================================================
T = "Gravitation"

add(T, "Law of gravitation", "Basic", "multi_statement",
    multi("Which of the following statements about the gravitational force between two point masses are correct?",
          ["It is always attractive.",
           "It varies inversely as the square of the distance between the masses.",
           "It depends on the medium between the masses.",
           "It acts along the line joining the two masses.",
           "The value of the universal gravitational constant G is different at different places on the Earth."]),
    place("(a), (b) and (d) only", ["(a), (b), (c) and (d) only", "(b), (d) and (e) only", "(a), (c) and (e) only"],
          "D"),
    "Newton's law of universal gravitation",
    "F = Gm₁m₂/r², directed along the line joining the masses and always attractive. G is a universal constant, "
    "and unlike the electrostatic force, gravitation does not depend on the medium in between.",
    ["(a) True", "(b) True: F ∝ 1/r²", "(c) False: independent of the intervening medium",
     "(d) True: a central force", "(e) False: G is universal; it is g that varies"],
    ncert="Class 11 Physics, 'Gravitation', universal law of gravitation", seconds=40)

ve_ratio = math.sqrt(8 / 2)
assert ve_ratio == 2 and round(11.2 * ve_ratio, 1) == 22.4 and round(11.2 * 4, 1) == 44.8
add(T, "Escape and orbital velocity", "Basic", "numerical",
    "The escape speed from the Earth's surface is 11.2 km/s. A planet has 8 times the mass and 2 times the radius "
    "of the Earth. The escape speed from its surface is:",
    place("22.4 km/s", ["11.2 km/s", "44.8 km/s", "5.6 km/s"], "C"),
    "Escape speed v_e = √(2GM/R)",
    "Escape speed varies as √(M/R). Here M/R becomes 8/2 = 4 times, so v_e becomes √4 = 2 times.",
    ["v_e ∝ √(M/R)", "Ratio = √(8/2) = 2", "v_e = 2 × 11.2 = 22.4 km/s"],
    why="11.2 km/s ignores the change in mass and radius. 44.8 km/s forgets the square root. 5.6 km/s inverts "
        "the ratio.",
    seconds=40, recomputed=True)

add(T, "Kepler's laws", "Basic", "match_list",
    match_stem("Match List-I (law) with List-II (its statement).",
               ["Kepler's first law", "Kepler's second law", "Kepler's third law", "Newton's law of gravitation"],
               ["The square of the period of revolution is proportional to the cube of the semi-major axis",
                "The line joining a planet to the Sun sweeps out equal areas in equal intervals of time",
                "Planets move in elliptical orbits with the Sun at one focus",
                "F = Gm₁m₂/r²"]),
    match_options({"A": "III", "B": "II", "C": "I", "D": "IV"},
                  [{"A": "II", "B": "III", "C": "I", "D": "IV"}, {"A": "III", "B": "I", "C": "II", "D": "IV"},
                   {"A": "I", "B": "II", "C": "III", "D": "IV"}], "A"),
    "Kepler's laws of planetary motion",
    "First law: law of orbits. Second law: law of areas. Third law: law of periods.",
    ["First law (orbits): ellipse with the Sun at a focus → III", "Second law (areas): equal areas in equal times → II",
     "Third law (periods): T² ∝ a³ → I", "Newton: F = Gm₁m₂/r² → IV"],
    why="The other codes swap the first and second laws, or the second and third.",
    ncert="Class 11 Physics, 'Gravitation', Kepler's laws", seconds=30)

Tp = 4 ** 1.5
assert Tp == 8 and 4 ** 2 == 16 and 4 ** 0.5 == 2
add(T, "Kepler's laws", "Intermediate", "numerical",
    "A planet moves round the Sun in a nearly circular orbit whose radius is 4 times the radius of the Earth's "
    "orbit. Its period of revolution is:",
    place("8 years", ["4 years", "16 years", "2 years"], "B"),
    "Kepler's third law: T² ∝ r³",
    "Compare with the Earth (T = 1 year): T_p/T_E = (r_p/r_E)^(3/2).",
    ["T_p = 1 year × 4^(3/2)", "= (√4)³ = 2³ = 8 years"],
    why="4 years assumes T ∝ r. 16 years uses T ∝ r². 2 years uses T ∝ √r.",
    seconds=40, recomputed=True)

g0, Re = 10, 6.4e6
v_orb = math.sqrt(g0 * Re ** 2 / (2 * Re))
assert round(v_orb / 1000, 2) == 5.66 and round(math.sqrt(g0 * Re) / 1000, 1) == 8.0
assert round(math.sqrt(2 * g0 * Re) / 1000, 1) == 11.3 and round(math.sqrt(g0 * Re) / 2000, 1) == 4.0
add(T, "Escape and orbital velocity", "Intermediate", "numerical",
    "A satellite revolves in a circular orbit at a height above the Earth's surface equal to the Earth's radius. "
    "Taking the Earth's radius as 6400 km and g = 10 m/s² at the surface, the orbital speed of the satellite is "
    "about:",
    place("5.66 km/s", ["8.0 km/s", "11.3 km/s", "4.0 km/s"], "D"),
    "Orbital speed v = √(GM/r)",
    "The orbit radius is r = R + h = 2R. Use GM = gR² to avoid needing G and M.",
    ["v = √(GM/r) = √(gR²/2R) = √(gR/2)", "= √(10 × 6.4 × 10⁶/2) = √(3.2 × 10⁷)", "≈ 5.66 × 10³ m/s = 5.66 km/s"],
    why="8.0 km/s is the orbital speed close to the surface (r = R). 11.3 km/s is the escape speed √(2gR). 4.0 km/s "
        "halves √(gR) instead of dividing gR by 2 under the root.",
    seconds=60, recomputed=True)

W_raise = F(1, 1) - F(1, 2)  # GMm (1/R - 1/2R) in units of mgR
assert W_raise == F(1, 2) and (F(1) + F(1, 4)) / 2 == F(5, 8)
add(T, "Gravitational potential and energy", "Intermediate", "numerical",
    "A body of mass m is raised from the surface of the Earth to a height equal to the Earth's radius R. If g is "
    "the acceleration due to gravity at the surface, the work done against gravity is:",
    place("mgR/2", ["mgR", "mgR/4", "5mgR/8"], "A"),
    "Gravitational potential energy U = −GMm/r",
    "For heights comparable to R, g is not constant, so mgh does not apply. Use the change in U = −GMm/r with "
    "GM = gR².",
    ["W = U(2R) − U(R) = −GMm/2R + GMm/R = GMm/2R", "With GM = gR²: W = mgR/2"],
    why="mgR uses mgh with g taken as constant. mgR/4 uses the value of g at height R (g/4) throughout. 5mgR/8 "
        "averages the values of g at the two ends, which is still not the correct integral.",
    seconds=60, recomputed=True)

add(T, "Variation of g", "Intermediate", "statement_pair",
    SP_STEM.format(s1="The period of a satellite in a circular orbit close to the Earth's surface depends on the "
                      "mass of the satellite.",
                   s2="Assuming the Earth to be a sphere of uniform density, the acceleration due to gravity "
                      "decreases as one goes below the Earth's surface."),
    sp("D"),
    "Satellite period; g at depth",
    "T = 2π√(r³/GM) contains only the Earth's mass, not the satellite's, so Statement I is false. Below the "
    "surface g(d) = g(1 − d/R), which decreases with depth, so Statement II is true.",
    ["T = 2π√(r³/GM): no satellite mass → I false", "g(d) = g(1 − d/R) → decreases → II true"],
    ncert="Class 11 Physics, 'Gravitation', acceleration due to gravity below the surface; earth satellites",
    seconds=40)

E2, E4 = -F(1, 2 * 2), -F(1, 2 * 4)  # E = -GMm/2r in units of GMm/R
dE = E4 - E2
assert dE == F(1, 8) and (F(1, 2) - F(1, 4)) == F(1, 4) and F(1, 2) * (F(1, 3) - F(1, 5)) == F(1, 15)
assert -E2 + -E4 == F(3, 8)
add(T, "Satellite energy and period", "Advanced", "numerical",
    "A satellite of mass m is moved from a circular orbit of radius 2R to a circular orbit of radius 4R around the "
    "Earth, where R is the Earth's radius. If g is the acceleration due to gravity at the Earth's surface, the "
    "minimum energy that must be supplied is:",
    place("mgR/8", ["mgR/4", "mgR/15", "3mgR/8"], "C"),
    "Total energy of a satellite: E = −GMm/2r",
    "The energy to be supplied is the increase in total (kinetic + potential) energy, not just in potential "
    "energy, because the satellite also slows down in the higher orbit.",
    ["E(2R) = −GMm/4R; E(4R) = −GMm/8R", "ΔE = −GMm/8R + GMm/4R = GMm/8R", "With GM = gR²: ΔE = mgR/8"],
    why="mgR/4 is the change in potential energy alone; the kinetic energy decreases by mgR/8 and offsets half of it. "
        "mgR/15 treats 2R and 4R as heights above the surface (radii 3R and 5R). 3mgR/8 adds the magnitudes of the "
        "two energies instead of subtracting.",
    seconds=120, recomputed=True)

# launched up with v = v_e/2: (1/2)v^2 - GM/R = -GM/(R+h), with v^2 = GM/(2R)
rh = 1 / (F(1) - F(1, 2) * F(1, 2))  # (R+h)/R
assert rh == F(4, 3) and rh - 1 == F(1, 3)
assert (F(2, 4)) / 2 == F(1, 4)  # constant g: v^2 = 2gR/4, h = v^2/2g = R/4
assert 1 / (F(1) - F(1, 2)) - 1 == 1  # dropping the 1/2 in KE gives h = R
assert 1 / (F(1) - F(1, 2) * F(1, 4)) - 1 == F(1, 7)  # using v_e = sqrt(gR) gives h = R/7
add(T, "Escape and orbital velocity", "Advanced", "numerical",
    "A body is projected vertically upward from the Earth's surface with a speed equal to half the escape speed. "
    "If R is the radius of the Earth, the maximum height it reaches above the surface is (neglect air resistance):",
    place("R/3", ["R/4", "R", "R/7"], "B"),
    "Energy conservation in a non-uniform gravitational field",
    "g falls off with height, so use energy conservation with U = −GMm/r, not v² = 2gh.",
    ["v² = v_e²/4 = (2GM/R)/4 = GM/2R", "½mv² − GMm/R = −GMm/(R + h)", "GM/4R − GM/R = −GM/(R + h) → R + h = 4R/3",
     "h = R/3"],
    why="R/4 uses h = v²/2g with constant g. R drops the ½ in the kinetic energy. R/7 takes the escape speed as "
        "√(gR) instead of √(2gR).",
    seconds=120, recomputed=True)

add(T, "Satellite energy and period", "Advanced", "assertion_reason",
    AR_STEM.format(a="An astronaut inside a satellite orbiting the Earth experiences weightlessness.",
                   r="The gravitational force of the Earth on the astronaut in orbit is zero."),
    ar("C"),
    "Weightlessness in orbit",
    "The astronaut and the satellite both fall freely towards the Earth with the same acceleration, so the floor "
    "pushes on the astronaut with zero force: A is true. Gravity at orbital heights is still strong (it is what "
    "keeps the satellite in orbit), so R is false.",
    ["Both in free fall with the same acceleration → no normal reaction → weightless → A true",
     "Gravity provides the centripetal force of the orbit, so it is not zero → R false"],
    why="Options A and B accept the false reason. Option D denies the true assertion.",
    seconds=40)

# =====================================================================================================================
# Properties of Solids and Liquids (B5 I6 A5)
# =====================================================================================================================
T = "Properties of Solids and Liquids"

Fw, Lw, Aw, Yw = 10 * 10, 2, 1e-6, 2e11
dL = Fw * Lw / (Aw * Yw)
assert close(dL, 1e-3) and close(10 * Lw / (Aw * Yw), 1e-4)
assert close(Fw * Lw / (1e-9 * Yw), 1.0) and close(Fw * Lw / (1e-4 * Yw), 1e-5)
add(T, "Elasticity and moduli", "Basic", "numerical",
    "A steel wire 2 m long with a cross-sectional area of 1 mm² hangs from a rigid support and carries a load of "
    "mass 10 kg. Young's modulus of steel is 2 × 10¹¹ N/m² and g = 10 m/s². The extension of the wire is:",
    place("1 mm", ["0.1 mm", "1 m", "0.01 mm"], "A"),
    "Young's modulus Y = (F/A)/(ΔL/L)",
    "Rearrange Young's modulus for the extension, ΔL = FL/(AY), and work in SI units: 1 mm² = 10⁻⁶ m².",
    ["F = mg = 100 N; A = 1 mm² = 10⁻⁶ m²", "ΔL = FL/(AY) = (100 × 2)/(10⁻⁶ × 2 × 10¹¹)", "ΔL = 10⁻³ m = 1 mm"],
    why="0.1 mm uses the mass (10) instead of the weight (100 N). 1 m converts 1 mm² to 10⁻⁹ m². 0.01 mm converts "
        "1 mm² to 10⁻⁴ m².",
    seconds=45, recomputed=True)

r_small, r_large, F_small = 2, 10, 200
F_large = F_small * (r_large / r_small) ** 2
assert F_large == 5000 and F_small * r_large / r_small == 1000 and F_small / (r_large / r_small) ** 2 == 8
add(T, "Fluid pressure and Pascal's law", "Basic", "numerical",
    "In a hydraulic lift, the small piston has a radius of 2 cm and the large piston a radius of 10 cm. A force of "
    "200 N is applied on the small piston. The largest load the large piston can support is:",
    place("5000 N", ["1000 N", "8 N", "200 N"], "D"),
    "Pascal's law: pressure is transmitted undiminished",
    "The same pressure acts on both pistons, so F₂/A₂ = F₁/A₁. The force is multiplied by the ratio of areas, which "
    "is the square of the ratio of radii.",
    ["A₂/A₁ = (10/2)² = 25", "F₂ = 200 × 25 = 5000 N"],
    why="1000 N uses the ratio of radii instead of areas. 8 N divides by the area ratio. 200 N assumes force, not "
        "pressure, is transmitted.",
    ncert="Class 11 Physics, 'Mechanical Properties of Fluids', Pascal's law and its applications",
    seconds=40, recomputed=True)

S_b, r_b = 0.03, 0.02
assert close(4 * S_b / r_b, 6) and close(2 * S_b / r_b, 3) and close(S_b / r_b, 1.5) and close(4 * S_b / 0.01, 12)
add(T, "Surface tension and capillarity", "Basic", "numerical",
    "A soap bubble has a radius of 2 cm. The surface tension of the soap solution is 0.03 N/m. The excess pressure "
    "inside the bubble over the outside pressure is:",
    place("6 Pa", ["3 Pa", "1.5 Pa", "12 Pa"], "B"),
    "Excess pressure inside a soap bubble",
    "A soap bubble has two surfaces (inner and outer), so its excess pressure is twice that of a liquid drop: "
    "ΔP = 4S/r.",
    ["r = 2 cm = 0.02 m", "ΔP = 4S/r = 4 × 0.03/0.02 = 6 Pa"],
    why="3 Pa uses 2S/r, which is for a liquid drop with one surface. 1.5 Pa uses S/r. 12 Pa takes 2 cm as the "
        "diameter.",
    ncert="Class 11 Physics, 'Mechanical Properties of Fluids', excess pressure across a curved surface",
    seconds=35, recomputed=True)

add(T, "Viscosity and Stokes' law", "Basic", "direct",
    "According to Stokes' law, the viscous drag force on a small sphere of radius r moving slowly with speed v "
    "through a fluid of coefficient of viscosity η is proportional to:",
    place("ηrv", ["ηr²v", "ηrv²", "η²rv"], "A"),
    "Stokes' law",
    "For a small sphere moving slowly (streamline flow around it), F = 6πηrv: the drag is proportional to the "
    "first power of each of η, r and v.",
    ["F = 6πηrv → F ∝ ηrv"],
    why="Each wrong option raises one of the three quantities to the second power.",
    ncert="Class 11 Physics, 'Mechanical Properties of Fluids', Stokes' law", seconds=25)

add(T, "Elasticity and moduli", "Basic", "match_list",
    match_stem("Match List-I (physical quantity) with List-II (its SI unit).",
               ["Surface tension", "Coefficient of viscosity", "Young's modulus", "Thermal conductivity"],
               ["W m⁻¹ K⁻¹", "N m⁻¹", "N m⁻²", "N s m⁻²"]),
    match_options({"A": "II", "B": "IV", "C": "III", "D": "I"},
                  [{"A": "III", "B": "IV", "C": "II", "D": "I"}, {"A": "II", "B": "III", "C": "IV", "D": "I"},
                   {"A": "IV", "B": "II", "C": "III", "D": "I"}], "C"),
    "SI units from defining equations",
    "Write each quantity from its defining equation and read off the unit.",
    ["Surface tension = force/length → N m⁻¹ → II", "Viscosity: F = ηA(dv/dx) → η in N s m⁻² (Pa s) → IV",
     "Young's modulus = stress/strain → N m⁻² (Pa) → III", "Thermal conductivity: H = KA ΔT/L → W m⁻¹ K⁻¹ → I"],
    why="The usual slips swap surface tension (force per length) with modulus (force per area), or viscosity with "
        "modulus (they differ by a factor of time).",
    seconds=35)

c_liq = 500 * 120 / (1 * (45 - 20))
assert c_liq == 2400 and 500 * 2 / 25 == 40 and round(60000 / 45) == 1333 and 60000 / 20 == 3000
add(T, "Thermal expansion and calorimetry", "Intermediate", "numerical",
    "A 500 W electric heater immersed in 1 kg of a liquid raises its temperature from 20 °C to 45 °C in 2 minutes. "
    "Assuming no heat is lost, the specific heat capacity of the liquid is:",
    place("2400 J kg⁻¹ K⁻¹", ["40 J kg⁻¹ K⁻¹", "1333 J kg⁻¹ K⁻¹", "3000 J kg⁻¹ K⁻¹"], "B"),
    "Calorimetry: Q = mcΔT",
    "All the electrical energy supplied, P × t, heats the liquid.",
    ["Q = 500 W × 120 s = 60 000 J", "ΔT = 45 − 20 = 25 K", "c = Q/(mΔT) = 60 000/(1 × 25) = 2400 J kg⁻¹ K⁻¹"],
    why="40 leaves the time in minutes. 1333 divides by the final temperature (45) instead of the rise. 3000 "
        "divides by the initial temperature (20).",
    seconds=50, recomputed=True)

rho_w, va_, vb_ = 1000, 2, 4
dP = F(1, 2) * rho_w * (vb_ ** 2 - va_ ** 2)
assert dP == 6000 and F(1, 2) * rho_w * (vb_ - va_) ** 2 == 2000 and F(1, 2) * rho_w * vb_ ** 2 == 8000
assert rho_w * (vb_ ** 2 - va_ ** 2) == 12000
add(T, "Bernoulli's principle", "Intermediate", "numerical",
    "Water flows steadily through a horizontal pipe. At a wide section its speed is 2 m/s and at a narrow section "
    "it is 4 m/s. Taking the density of water as 1000 kg/m³, the pressure at the wide section exceeds that at the "
    "narrow section by:",
    place("6000 Pa", ["2000 Pa", "8000 Pa", "12000 Pa"], "D"),
    "Bernoulli's equation for a horizontal pipe",
    "With no change in height, P + ½ρv² is constant along a streamline. Where the fluid moves faster, the pressure "
    "is lower.",
    ["P₁ + ½ρv₁² = P₂ + ½ρv₂²", "P₁ − P₂ = ½ × 1000 × (4² − 2²) = 500 × 12 = 6000 Pa"],
    why="2000 Pa squares the difference of speeds instead of taking the difference of squares. 8000 Pa uses only "
        "the faster speed. 12000 Pa drops the ½.",
    seconds=50, recomputed=True)

add(T, "Surface tension and capillarity", "Intermediate", "statement_pair",
    SP_STEM.format(s1="Water rises in a clean glass capillary tube dipped in it, while mercury is depressed in a "
                      "glass capillary tube.",
                   s2="The angle of contact between mercury and glass is obtuse."),
    sp("A"),
    "Capillarity and angle of contact",
    "Capillary rise h = 2S cos θ/(rρg). For water on clean glass θ is acute (cos θ > 0), so water rises. For "
    "mercury on glass θ is obtuse (about 140°, cos θ < 0), so mercury is depressed. Both statements are true.",
    ["Water–glass: θ acute → h > 0 → rises", "Mercury–glass: θ obtuse → h < 0 → depressed",
     "Statement I true, Statement II true"],
    ncert="Class 11 Physics, 'Mechanical Properties of Fluids', angle of contact and capillary rise", seconds=35)

ratio_r = 8 ** (1 / 3)
assert close(ratio_r, 2) and close(ratio_r ** 2, 4)
add(T, "Viscosity and Stokes' law", "Intermediate", "numerical",
    "Eight identical small raindrops, each falling through air with terminal velocity v, combine to form one "
    "bigger drop. Assuming Stokes' law holds, the terminal velocity of the bigger drop is:",
    place("4v", ["2v", "8v", "v"], "C"),
    "Terminal velocity v_t = 2r²(ρ − σ)g/9η ∝ r²",
    "The volume is conserved when the drops merge, so the radius of the big drop follows from R³ = 8r³. Terminal "
    "velocity then scales as the square of the radius.",
    ["(4/3)πR³ = 8 × (4/3)πr³ → R = 2r", "v_t ∝ r² → v' = (2)² v = 4v"],
    why="2v assumes v_t ∝ r. 8v assumes v_t ∝ volume. v assumes terminal velocity does not depend on size.",
    seconds=50, recomputed=True)

add(T, "Heat transfer", "Intermediate", "assertion_reason",
    AR_STEM.format(a="At room temperature, a metal object feels colder to the touch than a wooden object kept at "
                     "the same temperature.",
                   r="Metals have a much higher thermal conductivity than wood, so they conduct heat away from the "
                     "hand much faster."),
    ar("A"),
    "Thermal conductivity",
    "Both objects are at the same temperature, below body temperature. The sensation of cold depends on how fast "
    "heat leaves the skin. Metal conducts heat away from the hand quickly; wood, a poor conductor, does not. R is "
    "true and explains A.",
    ["Same temperature, but different rates of heat flow from the hand", "K_metal ≫ K_wood → faster heat loss → feels "
     "colder", "R explains A"],
    ncert="Class 11 Physics, 'Thermal Properties of Matter', conduction", seconds=35)

add(T, "Elasticity and moduli", "Intermediate", "statement_pair",
    SP_STEM.format(s1="Young's modulus is defined for liquids as well as for solids.",
                   s2="Within the elastic limit, stress is directly proportional to strain."),
    sp("D"),
    "Moduli of elasticity and Hooke's law",
    "Young's modulus involves a change in length of a body with a definite shape, so it applies only to solids. "
    "Liquids (and gases) have only a bulk modulus. Statement I is false. Statement II is Hooke's law: true.",
    ["Liquids have no definite length or shape → no Young's modulus → I false",
     "Hooke's law: stress ∝ strain within the elastic limit → II true"],
    ncert="Class 11 Physics, 'Mechanical Properties of Solids', Hooke's law and elastic moduli", seconds=30)

m_ice, m_w, Tw, Lf = 50, 200, 40, 80
heat_avail = m_w * 1 * Tw
heat_melt = m_ice * Lf
assert heat_avail >= heat_melt
Tf = F(heat_avail - heat_melt, m_ice + m_w)
assert Tf == 16 and F(heat_avail, m_ice + m_w) == 32 and F(heat_avail - heat_melt, m_w) == 20
add(T, "Thermal expansion and calorimetry", "Advanced", "numerical",
    "50 g of ice at 0 °C is dropped into 200 g of water at 40 °C in an insulated container of negligible heat "
    "capacity. Take the specific heat of water as 1 cal g⁻¹ °C⁻¹ and the latent heat of fusion of ice as "
    "80 cal g⁻¹. The final temperature of the mixture is:",
    place("16 °C", ["32 °C", "0 °C", "20 °C"], "B"),
    "Calorimetry with a change of state",
    "First check whether all the ice can melt. Then the remaining heat warms the whole 250 g of water.",
    ["Heat the water can give in cooling to 0 °C: 200 × 1 × 40 = 8000 cal",
     "Heat to melt all the ice: 50 × 80 = 4000 cal < 8000 cal → all the ice melts",
     "Heat left = 4000 cal, shared by 250 g: ΔT = 4000/250 = 16 °C"],
    shortcut="Heat lost = heat gained: 200(40 − T) = 50 × 80 + 50(T − 0) → 8000 − 4000 = 250T → T = 16 °C.",
    why="32 °C ignores the latent heat of fusion. 0 °C assumes some ice is left, but 8000 cal is more than enough "
        "to melt it all. 20 °C forgets that the 50 g of melted ice must also be warmed.",
    ncert="Class 11 Physics, 'Thermal Properties of Matter', calorimetry and change of state", seconds=120,
    recomputed=True)

h_surf, h_hole = 5.0, 3.2
v_eff = math.sqrt(2 * 10 * (h_surf - h_hole))
t_drop = math.sqrt(2 * h_hole / 10)
assert close(v_eff, 6) and close(t_drop, 0.8) and close(v_eff * t_drop, 4.8)
assert close(math.sqrt(2 * 10 * h_surf) * t_drop, 8.0) and round(math.sqrt(10 * 1.8) * t_drop, 1) == 3.4
assert close(math.sqrt(2 * 10 * 3.2) * t_drop, 6.4)
add(T, "Bernoulli's principle", "Advanced", "numerical",
    "A wide open tank stands on level ground and is filled with water to a height of 5.0 m above the ground. A "
    "small hole is made in its side wall at a height of 3.2 m above the ground. Taking g = 10 m/s², the water "
    "jet strikes the ground at a horizontal distance from the wall of:",
    place("4.8 m", ["8.0 m", "3.4 m", "6.4 m"], "C"),
    "Torricelli's law followed by horizontal projection",
    "The speed of efflux depends on the depth of the hole below the water surface (Torricelli). The jet then falls "
    "freely through the height of the hole above the ground.",
    ["Depth of hole below surface = 5.0 − 3.2 = 1.8 m", "Efflux speed v = √(2gh) = √(2 × 10 × 1.8) = 6 m/s",
     "Time to fall 3.2 m: t = √(2 × 3.2/10) = 0.8 s", "Range = 6 × 0.8 = 4.8 m"],
    why="8.0 m uses the full water height (5 m) for the efflux speed. 3.4 m uses v = √(gh), missing the 2. 6.4 m "
        "uses the hole's height (3.2 m) as its depth below the surface.",
    ncert="Class 11 Physics, 'Mechanical Properties of Fluids', speed of efflux: Torricelli's law", seconds=120,
    recomputed=True)

# rods in series: rod P (K, L) at 100 C end, rod Q (3K, 2L) at 0 C end
Tj = F(100, 1 + F(3, 2))
assert Tj == 40
assert F(100 * F(3, 2), 1 + F(3, 2)) == 60 and F(100, 1 + 3) == 25
add(T, "Heat transfer", "Advanced", "numerical",
    "Two rods P and Q of the same cross-sectional area are joined end to end. Rod P has thermal conductivity K and "
    "length L; rod Q has thermal conductivity 3K and length 2L. The free end of P is kept at 100 °C and the free "
    "end of Q at 0 °C. The sides are insulated. In the steady state, the temperature of the junction is:",
    place("40 °C", ["60 °C", "25 °C", "50 °C"], "D"),
    "Steady-state conduction through rods in series",
    "In the steady state the same heat current flows through both rods: H = KA ΔT/L for each.",
    ["K A (100 − T)/L = 3K A (T − 0)/(2L)", "100 − T = 1.5 T", "T = 100/2.5 = 40 °C"],
    why="60 °C attaches the rods the other way round. 25 °C ignores the different lengths. 50 °C ignores both the "
        "conductivities and the lengths.",
    ncert="Class 11 Physics, 'Thermal Properties of Matter', conduction", seconds=90, recomputed=True)

add(T, "Viscosity and Stokes' law", "Advanced", "multi_statement",
    multi("Which of the following statements about fluids are correct?",
          ["In steady (streamline) flow, the velocity of the fluid at any given point does not change with time.",
           "Bernoulli's principle expresses the conservation of energy for the steady flow of an incompressible, "
           "non-viscous fluid.",
           "The viscosity of a gas increases as its temperature rises.",
           "The surface tension of a liquid generally decreases as its temperature rises.",
           "Pascal's law states that a pressure applied to an enclosed fluid is transmitted undiminished only in the "
           "direction of the applied force."]),
    place("(a), (b), (c) and (d) only", ["(a), (b) and (d) only", "(b), (c) and (e) only",
                                         "(a), (c), (d) and (e) only"], "B"),
    "Streamline flow, Bernoulli, viscosity, surface tension and Pascal's law",
    "In steady flow each point has a fixed velocity. Bernoulli's equation is the work-energy theorem for an ideal "
    "fluid. The viscosity of liquids falls with temperature but that of gases rises. Surface tension falls as "
    "temperature rises. Pascal's law says the pressure is transmitted equally in all directions.",
    ["(a) True", "(b) True", "(c) True: gases become more viscous when heated (liquids less)", "(d) True",
     "(e) False: transmitted undiminished to every part of the fluid and the container walls"],
    why="(a), (b) and (d) only leaves out (c), the gas-viscosity trap. Every other option includes the false (e) "
        "or leaves out a true statement.",
    ncert="Class 11 Physics, 'Mechanical Properties of Fluids', streamline flow, Bernoulli's principle, viscosity",
    seconds=75)

# drop of radius R into 1000 droplets of radius R/10
dA = 1000 * 4 * F(1, 100) - 4  # in units of pi R^2
assert dA == 36 and 1000 * 4 * F(1, 100) == 40 and 2 * dA == 72 and 1000 * F(1, 100) - 1 == 9
add(T, "Surface tension and capillarity", "Advanced", "numerical",
    "A liquid drop of radius R breaks up isothermally into 1000 identical droplets. If S is the surface tension of "
    "the liquid, the work done in this process is:",
    place("36πR²S", ["40πR²S", "72πR²S", "9πR²S"], "C"),
    "Surface energy: work = S × increase in surface area",
    "The total volume stays the same, so each droplet has radius r = R/10. The work needed equals S times the "
    "increase in total surface area.",
    ["(4/3)πR³ = 1000 × (4/3)πr³ → r = R/10", "Final area = 1000 × 4π(R/10)² = 40πR²; initial area = 4πR²",
     "ΔA = 36πR² → W = 36πR²S"],
    why="40πR²S uses the final area and forgets to subtract the initial area. 72πR²S counts two surfaces per drop, "
        "as for a soap bubble. 9πR²S uses πR² instead of 4πR² for the area of a sphere.",
    ncert="Class 11 Physics, 'Mechanical Properties of Fluids', surface energy", seconds=90, recomputed=True)

# =====================================================================================================================
# Thermodynamics (B3 I4 A3)
# =====================================================================================================================
T = "Thermodynamics"

Qs, Wb_ = 500, 200
assert Qs - Wb_ == 300 and Qs + Wb_ == 700
add(T, "Zeroth and first law", "Basic", "numerical",
    "A gas absorbs 500 J of heat and does 200 J of work on its surroundings. The change in its internal energy is:",
    place("300 J", ["700 J", "−300 J", "200 J"], "C"),
    "First law of thermodynamics: ΔQ = ΔU + ΔW",
    "Heat supplied to the system goes partly into raising its internal energy and partly into work done by it.",
    ["ΔU = ΔQ − ΔW", "= 500 − 200 = 300 J (internal energy increases)"],
    why="700 J adds the work instead of subtracting it. −300 J gets the sign convention backwards. 200 J is the "
        "work done, not the change in internal energy.",
    ncert="Class 11 Physics, 'Thermodynamics', first law of thermodynamics", seconds=25, recomputed=True)

add(T, "Zeroth and first law", "Basic", "direct",
    "The zeroth law of thermodynamics leads directly to the concept of:",
    place("Temperature", ["Internal energy", "Entropy", "Heat capacity"], "A"),
    "Zeroth law and thermal equilibrium",
    "If two systems are each in thermal equilibrium with a third, they are in thermal equilibrium with each other. "
    "The physical quantity that has the same value for systems in thermal equilibrium is temperature.",
    ["A ~ C and B ~ C (thermal equilibrium) → A ~ B", "The common property of systems in equilibrium = temperature"],
    why="Internal energy comes from the first law, and entropy from the second. Heat capacity is a property of a "
        "body, not the quantity the zeroth law defines.",
    ncert="Class 11 Physics, 'Thermodynamics', zeroth law of thermodynamics", seconds=20)

add(T, "Isothermal and adiabatic processes", "Basic", "statement_pair",
    SP_STEM.format(s1="When an ideal gas undergoes an isothermal process, the change in its internal energy is zero.",
                   s2="In an adiabatic process, no heat is exchanged between the system and its surroundings."),
    sp("A"),
    "Isothermal and adiabatic processes",
    "The internal energy of an ideal gas depends only on its temperature, so at constant temperature ΔU = 0: "
    "Statement I is true. An adiabatic process is defined by ΔQ = 0: Statement II is true.",
    ["Ideal gas: U = U(T) → isothermal → ΔU = 0 → I true", "Adiabatic: ΔQ = 0 by definition → II true"],
    ncert="Class 11 Physics, 'Thermodynamics', thermodynamic processes", seconds=30)

W_iso = 2 * 8.3 * 300 * 0.693
assert round(W_iso / 1000, 2) == 3.45 and round(2 * 8.3 * 300 / 1000, 2) == 4.98
assert round(8.3 * 300 * 0.693 / 1000, 2) == 1.73 and round(2 * 8.3 * 300 * 0.301 / 1000, 2) == 1.50
add(T, "Isothermal and adiabatic processes", "Intermediate", "numerical",
    "Two moles of an ideal gas at 300 K expand isothermally and reversibly until the volume doubles. Taking "
    "R = 8.3 J mol⁻¹ K⁻¹ and ln 2 = 0.693, the work done by the gas is about:",
    place("3.45 kJ", ["4.98 kJ", "1.73 kJ", "1.50 kJ"], "D"),
    "Work in a reversible isothermal process",
    "For an ideal gas at constant temperature, W = ∫P dV = nRT ln(V₂/V₁).",
    ["W = nRT ln(V₂/V₁) = 2 × 8.3 × 300 × ln 2", "= 4980 × 0.693 ≈ 3451 J ≈ 3.45 kJ"],
    why="4.98 kJ leaves out the ln 2 factor (it is nRT). 1.73 kJ uses n = 1. 1.50 kJ uses log₁₀ 2 = 0.301 instead "
        "of ln 2.",
    ncert="Class 11 Physics, 'Thermodynamics', isothermal process", seconds=60, recomputed=True)

T2 = 300 * 8 ** F(2, 3).__float__()
assert close(T2, 1200) and 300 * 8 == 2400 and close(300 * 8 ** (1 / 3), 600) and close(300 * 8 ** (5 / 3), 9600)
add(T, "Isothermal and adiabatic processes", "Intermediate", "numerical",
    "A monatomic ideal gas (γ = 5/3) at 300 K is compressed adiabatically and reversibly to one-eighth of its "
    "initial volume. Its final temperature is:",
    place("1200 K", ["2400 K", "600 K", "9600 K"], "B"),
    "Adiabatic relation TV^(γ−1) = constant",
    "In a reversible adiabatic process of an ideal gas, T V^(γ−1) stays constant. Here γ − 1 = 2/3.",
    ["T₂ = T₁ (V₁/V₂)^(γ−1) = 300 × 8^(2/3)", "8^(2/3) = (8^(1/3))² = 2² = 4", "T₂ = 1200 K"],
    why="2400 K uses T ∝ 1/V (power 1). 600 K uses the power 1/3. 9600 K uses the power γ = 5/3, which belongs to "
        "PV^γ, not TV^(γ−1).",
    ncert="Class 11 Physics, 'Thermodynamics', adiabatic process", seconds=60, recomputed=True)

add(T, "Zeroth and first law", "Intermediate", "assertion_reason",
    AR_STEM.format(a="The work done by a gas in going from one equilibrium state to another depends on the path "
                     "followed.",
                   r="The internal energy of an ideal gas is a state function."),
    ar("B"),
    "Path functions and state functions",
    "Work is the area under the P–V curve, which differs from path to path, so A is true. Internal energy depends "
    "only on the state, so R is true. But R does not explain A: it is about internal energy, while A is about "
    "work. The path dependence of work is due to the different areas under different P–V curves.",
    ["W = ∫P dV = area under the path → path-dependent → A true", "U depends only on the state → R true",
     "R is about U, not W → R does not explain A"],
    why="Option A is the trap: R is true, but a property of U cannot explain why W depends on the path.",
    ncert="Class 11 Physics, 'Thermodynamics', heat, internal energy and work; state variables", seconds=45)

frac_w = F(1) / F(7, 2)  # R / Cp for a diatomic gas
assert frac_w == F(2, 7) and 1 - frac_w == F(5, 7) and F(1) / F(5, 2) == F(2, 5)
add(T, "Zeroth and first law", "Intermediate", "numerical",
    "An ideal diatomic gas (Cv = 5R/2) is heated at constant pressure. The fraction of the heat supplied that is "
    "used in doing external work is:",
    place("2/7", ["5/7", "2/5", "1"], "C"),
    "First law at constant pressure",
    "At constant pressure, Q = nC_pΔT, ΔU = nC_vΔT and W = PΔV = nRΔT. So W/Q = R/C_p.",
    ["C_p = C_v + R = 7R/2", "W/Q = nRΔT/(nC_pΔT) = R/(7R/2) = 2/7"],
    why="5/7 is the fraction that goes into internal energy. 2/5 divides by C_v instead of C_p. 1 is true only for "
        "an isothermal process of an ideal gas, where ΔU = 0.",
    seconds=50, recomputed=True)

P_lo, P_hi, V_lo, V_hi = 1e5, 2e5, 1e-3, 3e-3
W_cycle = (P_hi - P_lo) * (V_hi - V_lo)
assert close(W_cycle, 200) and close(P_hi * (V_hi - V_lo), 400)
add(T, "Zeroth and first law", "Advanced", "numerical",
    "An ideal gas is taken round the cycle A → B → C → D → A. A (1 L, 1 × 10⁵ Pa) → B (1 L, 2 × 10⁵ Pa) at "
    "constant volume; B → C (3 L, 2 × 10⁵ Pa) at constant pressure; C → D (3 L, 1 × 10⁵ Pa) at constant volume; "
    "D → A at constant pressure. The net heat absorbed by the gas in one cycle is:",
    place("200 J", ["−200 J", "400 J", "0 J"], "A"),
    "First law for a cyclic process",
    "Over a complete cycle the gas returns to its initial state, so ΔU = 0 and the net heat absorbed equals the net "
    "work done by the gas, which is the area enclosed by the cycle on the P–V diagram.",
    ["Work at constant volume (A→B, C→D) = 0", "B→C: W = 2 × 10⁵ × (3 − 1) × 10⁻³ = +400 J",
     "D→A: W = 1 × 10⁵ × (1 − 3) × 10⁻³ = −200 J", "Net W = 200 J; ΔU = 0 → Q = W = 200 J"],
    why="−200 J gets the sign wrong: the gas expands at the higher pressure, so the net work by the gas is positive. "
        "400 J counts only the expansion. 0 J confuses ΔU = 0 with Q = 0.",
    seconds=90, recomputed=True)

dT_v = 50
dT_p = F(3, 5) * dT_v
assert dT_p == 30 and F(5, 3) * dT_v == F(250, 3) and F(3, 2) * dT_v == 75
add(T, "Zeroth and first law", "Advanced", "numerical",
    "A certain amount of heat Q, supplied to one mole of a monatomic ideal gas at constant volume, raises its "
    "temperature by 50 K. If the same amount of heat is supplied to the same gas at constant pressure instead, its "
    "temperature rises by:",
    place("30 K", ["50 K", "83.3 K", "75 K"], "D"),
    "Molar heat capacities C_v and C_p",
    "Q = C_vΔT at constant volume and Q = C_pΔT' at constant pressure. For a monatomic gas C_v = 3R/2 and "
    "C_p = 5R/2. At constant pressure part of the heat goes into work, so the temperature rises less.",
    ["Q = (3R/2)(50) = 75R", "ΔT' = Q/C_p = 75R/(5R/2) = 30 K"],
    why="50 K forgets that some heat does work at constant pressure. 83.3 K multiplies by C_p/C_v instead of "
        "C_v/C_p. 75 K divides Q by R (= C_p − C_v) instead of by C_p.",
    seconds=75, recomputed=True)

add(T, "Second law, reversible and irreversible processes", "Advanced", "multi_statement",
    multi("Which of the following statements are correct?",
          ["No process is possible whose sole result is the absorption of heat from a reservoir and its complete "
           "conversion into work.",
           "No process is possible whose sole result is the transfer of heat from a colder body to a hotter body.",
           "The free expansion of a gas into vacuum is a reversible process.",
           "A quasi-static isothermal expansion of an ideal gas in a cylinder fitted with a frictionless piston "
           "is a reversible process.",
           "The first law of thermodynamics rules out the complete conversion of heat into work in a cycle."]),
    place("(a), (b) and (d) only", ["(a), (b), (c) and (d) only", "(b), (d) and (e) only", "(a), (c) and (e) only"],
          "B"),
    "Second law of thermodynamics; reversibility",
    "(a) is the Kelvin–Planck statement and (b) the Clausius statement of the second law. Free expansion is "
    "sudden and uncontrolled, and the gas never returns to the cylinder by itself, so it is irreversible. A "
    "quasi-static process without dissipative effects such as friction is reversible. The first law only "
    "demands energy conservation; it is the second law that forbids 100% conversion of heat into work.",
    ["(a) True: Kelvin–Planck", "(b) True: Clausius", "(c) False: free expansion is irreversible",
     "(d) True: quasi-static and frictionless", "(e) False: that is the second law, not the first"],
    ncert="Class 11 Physics, 'Thermodynamics', second law; reversible and irreversible processes", seconds=60)

# =====================================================================================================================
# Kinetic Theory of Gases (B2 I2 A2)
# =====================================================================================================================
T = "Kinetic Theory of Gases"

T1, T2k = 27 + 273, 927 + 273
assert math.sqrt(T2k / T1) == 2 and round(math.sqrt(927 / 27), 2) == 5.86
add(T, "Pressure and rms speed", "Basic", "numerical",
    "The rms speed of the molecules of an ideal gas at 27 °C is v. At 927 °C, the rms speed of the molecules of "
    "the same gas is:",
    place("2v", ["4v", "5.86v", "v/2"], "A"),
    "rms speed v_rms = √(3RT/M) ∝ √T (kelvin)",
    "The rms speed depends on the square root of the absolute temperature, so first convert to kelvin.",
    ["T₁ = 300 K, T₂ = 1200 K", "v₂/v₁ = √(1200/300) = √4 = 2 → v₂ = 2v"],
    why="4v takes v_rms ∝ T. 5.86v uses the Celsius temperatures, √(927/27). v/2 inverts the ratio.",
    ncert="Class 11 Physics, 'Kinetic Theory', kinetic interpretation of temperature", seconds=30, recomputed=True)

add(T, "Degrees of freedom and equipartition", "Basic", "direct",
    "A rigid diatomic molecule (vibration not excited) has a total of how many degrees of freedom?",
    place("5", ["3", "6", "7"], "C"),
    "Degrees of freedom of a molecule",
    "A diatomic molecule can translate along three axes (3 translational degrees of freedom). Treated as a rigid "
    "rotor, it can rotate about the two axes perpendicular to its line; rotation about its own axis does not count. "
    "So 3 + 2 = 5.",
    ["Translational: 3", "Rotational (about the two axes normal to the bond): 2", "Total = 5"],
    why="3 counts translation only (a monatomic gas). 6 adds a third rotation that a linear molecule does not have. "
        "7 includes the vibrational mode (two quadratic terms), which is excluded for a rigid molecule.",
    ncert="Class 11 Physics, 'Kinetic Theory', law of equipartition of energy", seconds=25)

Cv_mix = (F(3, 2) + F(5, 2)) / 2
Cp_mix = Cv_mix + 1
gam = Cp_mix / Cv_mix
assert gam == F(3, 2) and round(float((F(5, 3) + F(7, 5)) / 2), 2) == 1.53
add(T, "Degrees of freedom and equipartition", "Intermediate", "numerical",
    "One mole of a monatomic ideal gas is mixed with one mole of a rigid diatomic ideal gas. The ratio of specific "
    "heats γ = Cp/Cv of the mixture is:",
    place("1.50", ["1.53", "1.40", "1.67"], "D"),
    "Heat capacities of a gas mixture from equipartition",
    "Molar C_v adds in proportion to the number of moles: monatomic C_v = 3R/2, diatomic C_v = 5R/2. Then "
    "C_p = C_v + R for the mixture. The γ values themselves cannot be averaged.",
    ["C_v(mix) = (1 × 3R/2 + 1 × 5R/2)/2 = 2R", "C_p(mix) = 2R + R = 3R", "γ = 3R/2R = 1.50"],
    why="1.53 averages the two γ values (5/3 and 7/5) directly, which is wrong. 1.40 and 1.67 are the γ values of "
        "the diatomic and monatomic gases alone.",
    seconds=75, recomputed=True)

add(T, "Pressure and rms speed", "Intermediate", "assertion_reason",
    AR_STEM.format(a="At the same temperature, the molecules of all ideal gases have the same rms speed.",
                   r="The average translational kinetic energy of a molecule of an ideal gas is (3/2)k_BT, where k_B "
                     "is Boltzmann's constant and T the absolute temperature."),
    ar("D"),
    "Temperature fixes the average kinetic energy, not the speed",
    "R is true. Because ½m⟨v²⟩ = (3/2)k_BT is the same for every gas at a given T, the rms speed √(3k_BT/m) is "
    "smaller for heavier molecules. So different gases at the same temperature have different rms speeds: A is "
    "false.",
    ["½m v_rms² = (3/2)k_BT → R true", "v_rms = √(3k_BT/m) depends on m → A false"],
    why="Options A, B and C all treat A as true; at the same T, hydrogen molecules move about four times faster "
        "than oxygen molecules.",
    ncert="Class 11 Physics, 'Kinetic Theory', kinetic interpretation of temperature", seconds=40)

# lambda = kT / (sqrt(2) pi d^2 P): P -> P/2, T -> 2T
lam_ratio = F(2) / F(1, 2)
assert lam_ratio == 4
add(T, "Mean free path", "Advanced", "numerical",
    "The mean free path of the molecules of an ideal gas is λ. If the pressure of the gas is halved and its "
    "absolute temperature is doubled, the new mean free path is:",
    place("4λ", ["λ", "λ/4", "2λ"], "B"),
    "Mean free path depends on the number density",
    "λ = 1/(√2 π d² n), and the number of molecules per unit volume is n = P/(k_BT). So λ = k_BT/(√2 π d² P), "
    "which is proportional to T/P.",
    ["λ ∝ 1/n and n = P/k_BT → λ ∝ T/P", "New λ' = λ × (2T/T) × (P/(P/2)) = 4λ"],
    why="λ assumes the two changes cancel; in fact both lower the number density. λ/4 inverts the dependence. 2λ "
        "accounts for only one of the two changes.",
    ncert="Class 11 Physics, 'Kinetic Theory', mean free path", seconds=60, recomputed=True)

P0, rho0 = 1.0e5, 1.2
v_rms = math.sqrt(3 * P0 / rho0)
assert close(v_rms, 500) and round(math.sqrt(P0 / rho0)) == 289 and close(v_rms * math.sqrt(2), 707.1)
assert close(v_rms / math.sqrt(2), 353.6)
add(T, "Pressure and rms speed", "Advanced", "numerical",
    "An ideal gas has density 1.2 kg/m³ at a pressure of 1.0 × 10⁵ Pa. What is the rms speed of its molecules, "
    "and what does it become if the gas is then compressed isothermally to half its volume?",
    place("500 m/s, and it stays 500 m/s", ["500 m/s, and it becomes 707 m/s", "289 m/s, and it stays 289 m/s",
                                             "500 m/s, and it becomes 354 m/s"], "A"),
    "Kinetic theory pressure P = ⅓ρv_rms²; v_rms depends only on T",
    "From P = ⅓ρv_rms², v_rms = √(3P/ρ). In an isothermal compression P and ρ both double, so P/ρ (which equals "
    "RT/M) is unchanged, and so is v_rms.",
    ["v_rms = √(3P/ρ) = √(3 × 10⁵/1.2) = √(2.5 × 10⁵) = 500 m/s",
     "Isothermal: P → 2P and ρ → 2ρ, so P/ρ is unchanged", "v_rms stays 500 m/s (it depends only on T)"],
    why="707 m/s lets the pressure double but keeps the density fixed. 289 m/s uses √(P/ρ) without the 3. 354 m/s "
        "lets the density double but keeps the pressure fixed.",
    ncert="Class 11 Physics, 'Kinetic Theory', pressure of an ideal gas", seconds=90, recomputed=True)

# =====================================================================================================================
# Oscillations and Waves (B4 I6 A4)
# =====================================================================================================================
T = "Oscillations and Waves"

m_s, k_s = 0.2, 80
Ts = 2 * math.pi * math.sqrt(m_s / k_s)
assert close(Ts, 0.1 * math.pi) and close(math.pi * math.sqrt(m_s / k_s), 0.05 * math.pi)
assert close(2 * math.pi * math.sqrt(k_s / m_s), 40 * math.pi) and close(2 * math.pi * m_s / k_s, 0.005 * math.pi)
add(T, "Spring and pendulum oscillations", "Basic", "numerical",
    "A block of mass 0.2 kg attached to a spring of force constant 80 N/m oscillates on a smooth horizontal surface. "
    "The time period of oscillation is:",
    place("0.1π s", ["0.05π s", "40π s", "0.005π s"], "C"),
    "Period of a spring–mass oscillator: T = 2π√(m/k)",
    "The restoring force −kx gives SHM with ω = √(k/m), so T = 2π/ω = 2π√(m/k).",
    ["m/k = 0.2/80 = 0.0025 → √(m/k) = 0.05 s", "T = 2π × 0.05 = 0.1π s ≈ 0.31 s"],
    why="0.05π s uses π instead of 2π. 40π s inverts the ratio (√(k/m)). 0.005π s forgets the square root.",
    ncert="Class 11 Physics, 'Oscillations', oscillations due to a spring", seconds=30, recomputed=True)

Tn, mu_s = 100, 0.01
assert math.sqrt(Tn / mu_s) == 100 and Tn / mu_s == 1e4 and math.sqrt(Tn * mu_s) == 1 and math.sqrt(mu_s / Tn) == 0.01
add(T, "Progressive waves and wave speed", "Basic", "numerical",
    "A string with a linear mass density of 0.01 kg/m is stretched with a tension of 100 N. The speed of transverse "
    "waves on the string is:",
    place("100 m/s", ["10⁴ m/s", "1 m/s", "0.01 m/s"], "D"),
    "Speed of a transverse wave on a stretched string",
    "The speed depends on the restoring property (tension T) and the inertial property (mass per unit length μ): "
    "v = √(T/μ).",
    ["v = √(T/μ) = √(100/0.01) = √10⁴ = 100 m/s"],
    why="10⁴ m/s forgets the square root. 1 m/s multiplies T and μ. 0.01 m/s inverts the ratio.",
    ncert="Class 11 Physics, 'Waves', speed of a transverse wave on a stretched string", seconds=25, recomputed=True)

add(T, "SHM equation and phase", "Basic", "direct",
    "In simple harmonic motion, the phase difference between the displacement and the acceleration of the particle "
    "is:",
    place("π rad", ["π/2 rad", "0", "π/4 rad"], "B"),
    "Defining relation of SHM: a = −ω²x",
    "The acceleration is always proportional to the displacement and opposite to it, so the two are exactly out of "
    "phase.",
    ["x = A cos(ωt + φ)", "a = −ω²A cos(ωt + φ) = ω²A cos(ωt + φ + π)", "Phase difference = π"],
    why="π/2 is the phase difference between displacement and velocity (or velocity and acceleration). 0 ignores the "
        "minus sign. π/4 has no basis.",
    ncert="Class 11 Physics, 'Oscillations', velocity and acceleration in simple harmonic motion", seconds=25)

add(T, "Progressive waves and wave speed", "Basic", "multi_statement",
    multi("Which of the following statements about mechanical waves are correct?",
          ["Mechanical waves need a material medium to travel.",
           "A travelling wave carries energy from one place to another, but the medium as a whole does not move "
           "along with it.",
           "Beats are produced by the superposition of two sound waves of slightly different frequencies.",
           "In a given medium at a fixed temperature, the speed of sound increases with the frequency of the source.",
           "A wave travelling along a stretched string is a longitudinal wave."]),
    place("(a), (b) and (c) only", ["(a), (b), (c) and (d) only", "(b), (c) and (e) only", "(a), (d) and (e) only"],
          "A"),
    "Basic properties of mechanical waves",
    "Mechanical waves are disturbances of a medium; the particles only oscillate about their mean positions while "
    "energy moves on. Beats arise from two nearly equal frequencies. In a non-dispersive medium like air the speed "
    "of sound depends on the medium, not on the frequency. Waves on a string are transverse.",
    ["(a) True", "(b) True", "(c) True", "(d) False: v = fλ, but a higher f just gives a shorter λ",
     "(e) False: string waves are transverse"],
    ncert="Class 11 Physics, 'Waves', introduction; transverse and longitudinal waves; beats", seconds=45)

w_, A_, x_p = math.pi, 10, 6
v_p = w_ * math.sqrt(A_ ** 2 - x_p ** 2)
assert close(v_p, 8 * math.pi) and close(w_ * A_, 10 * math.pi) and close(w_ * x_p, 6 * math.pi)
assert close(w_ * (A_ - x_p), 4 * math.pi)
add(T, "SHM equation and phase", "Intermediate", "numerical",
    "A particle executes simple harmonic motion with amplitude 10 cm and period 2 s. Its speed when it is 6 cm from "
    "the mean position is:",
    place("8π cm/s", ["10π cm/s", "6π cm/s", "4π cm/s"], "D"),
    "Velocity in SHM: v = ω√(A² − x²)",
    "Find ω from the period, then use the velocity–displacement relation of SHM.",
    ["ω = 2π/T = π rad/s", "v = ω√(A² − x²) = π√(100 − 36) = π × 8 = 8π cm/s ≈ 25 cm/s"],
    why="10π cm/s is the maximum speed ωA, reached only at the mean position. 6π cm/s uses ωx. 4π cm/s uses "
        "ω(A − x).",
    ncert="Class 11 Physics, 'Oscillations', velocity and acceleration in simple harmonic motion", seconds=50,
    recomputed=True)

add(T, "Energy in SHM", "Intermediate", "multi_statement",
    multi("For a particle executing undamped simple harmonic motion, which of the following statements are correct?",
          ["The total mechanical energy remains constant.",
           "The kinetic energy is maximum at the mean position.",
           "The potential energy is maximum at the extreme positions.",
           "The kinetic energy varies periodically with the same frequency as the displacement.",
           "The magnitude of the acceleration is maximum at the mean position."]),
    place("(a), (b) and (c) only", ["(a), (b), (c) and (d) only", "(b), (c) and (e) only", "(a), (c), (d) and (e) only"],
          "C"),
    "Energy in SHM",
    "With no damping, E = ½kA² is constant and is shared between K = ½k(A² − x²) and U = ½kx². K is greatest at "
    "x = 0 and U at x = ±A. K depends on x², so it goes through a full cycle twice per oscillation: its frequency is "
    "twice that of the displacement. |a| = ω²|x| is zero at the mean position and largest at the extremes.",
    ["(a) True", "(b) True: K = ½k(A² − x²) is largest at x = 0", "(c) True: U = ½kx² is largest at x = ±A",
     "(d) False: K oscillates at twice the frequency", "(e) False: acceleration is zero at the mean position"],
    ncert="Class 11 Physics, 'Oscillations', energy in simple harmonic motion", seconds=50)

pct = (math.sqrt(1.21) - 1) * 100
assert close(pct, 10) and round(math.sqrt(21), 1) == 4.6
add(T, "Spring and pendulum oscillations", "Intermediate", "numerical",
    "The length of a simple pendulum is increased by 21%. Its time period increases by:",
    place("10%", ["21%", "10.5%", "4.6%"], "B"),
    "Period of a simple pendulum: T = 2π√(l/g)",
    "T ∝ √l. Work with the exact ratio, because 21% is too large for the small-change approximation to be exact.",
    ["T₂/T₁ = √(1.21 l/l) = √1.21 = 1.1", "Increase = 10%"],
    why="21% assumes T ∝ l. 10.5% uses the approximation ΔT/T ≈ ½ Δl/l, which is only approximate for a 21% "
        "change; here the exact value √1.21 = 1.1 is available. 4.6% takes the square root of the percentage "
        "itself (√21).",
    ncert="Class 11 Physics, 'Oscillations', the simple pendulum", seconds=40, recomputed=True)

Ls, vw = 1, 200
f3 = 3 * vw / (2 * Ls)
assert f3 == 300 and vw / (2 * Ls) == 100 and 3 * vw / Ls == 600 and 3 * vw / (4 * Ls) == 150
add(T, "Superposition and standing waves", "Intermediate", "numerical",
    "A string 1 m long is fixed at both ends. Transverse waves travel on it at 200 m/s. The frequency of its third "
    "harmonic is:",
    place("300 Hz", ["100 Hz", "600 Hz", "150 Hz"], "A"),
    "Normal modes of a string fixed at both ends",
    "Both ends are nodes, so a whole number of half-wavelengths fits on the string: L = nλ/2, giving "
    "fₙ = nv/2L.",
    ["Fundamental f₁ = v/2L = 200/2 = 100 Hz", "Third harmonic f₃ = 3f₁ = 300 Hz"],
    why="100 Hz is the fundamental. 600 Hz takes λ = L/3 instead of 2L/3. 150 Hz uses the closed-pipe formula "
        "3v/4L.",
    ncert="Class 11 Physics, 'Waves', standing waves and normal modes", seconds=40, recomputed=True)

add(T, "Progressive waves and wave speed", "Intermediate", "statement_pair",
    SP_STEM.format(s1="Sound waves travelling through air are longitudinal waves.",
                   s2="Transverse mechanical waves can travel through gases."),
    sp("C"),
    "Transverse and longitudinal waves",
    "In air, sound travels as compressions and rarefactions along the direction of propagation, so it is "
    "longitudinal: Statement I is true. Transverse waves need a shear (rigidity) restoring force, which fluids "
    "cannot provide, so they cannot travel through gases: Statement II is false.",
    ["Sound in air: longitudinal → I true", "Gases have no shear modulus → no transverse mechanical waves → II false"],
    ncert="Class 11 Physics, 'Waves', transverse and longitudinal waves", seconds=30)

amp, k_w, om = 0.02, 0.5 * math.pi, 20 * math.pi
lam_w, f_w = 2 * math.pi / k_w, om / (2 * math.pi)
assert close(lam_w, 4) and close(f_w, 10) and close(om / k_w, 40) and close(f_w * lam_w, 40)
add(T, "Progressive waves and wave speed", "Intermediate", "match_list",
    match_stem("A wave on a string is described by y(x, t) = 0.02 sin(0.5πx − 20πt), where x and y are in metres "
               "and t in seconds. Match List-I (property) with List-II (value).",
               ["Amplitude", "Wavelength", "Frequency", "Wave speed"],
               ["40 m/s", "4 m", "10 Hz", "0.02 m"]),
    match_options({"A": "IV", "B": "II", "C": "III", "D": "I"},
                  [{"A": "IV", "B": "III", "C": "II", "D": "I"}, {"A": "IV", "B": "I", "C": "III", "D": "II"},
                   {"A": "I", "B": "II", "C": "III", "D": "IV"}], "D"),
    "Reading a progressive wave equation y = a sin(kx − ωt)",
    "Compare with y = a sin(kx − ωt): a = 0.02 m, k = 0.5π rad/m, ω = 20π rad/s. Then λ = 2π/k, f = ω/2π and "
    "v = ω/k.",
    ["Amplitude a = 0.02 m → IV", "λ = 2π/(0.5π) = 4 m → II", "f = 20π/2π = 10 Hz → III",
     "v = ω/k = 20π/0.5π = 40 m/s (= fλ) → I"],
    why="The wrong codes swap wavelength with frequency (k with ω), or wavelength with speed.",
    ncert="Class 11 Physics, 'Waves', displacement relation in a progressive wave", seconds=60)

f_fork, beats1, beats2 = 256, 4, 2
cands = [f_fork + beats1, f_fork - beats1]
# waxing lowers the unknown frequency (say by 2 Hz); keep the candidate whose beat frequency then falls to 2
ok = [f for f in cands if abs((f - 2) - f_fork) == beats2]
assert ok == [260]
add(T, "Organ pipes and beats", "Advanced", "numerical",
    "A tuning fork of unknown frequency produces 4 beats per second with a standard fork of frequency 256 Hz. When "
    "the prongs of the unknown fork are loaded with a little wax, the beat frequency falls to 2 per second. The "
    "frequency of the unknown fork before loading was:",
    place("260 Hz", ["252 Hz", "258 Hz", "254 Hz"], "A"),
    "Beats and the effect of loading a tuning fork",
    "4 beats/s means the unknown frequency is 256 ± 4 Hz. Loading a fork with wax increases the mass of its prongs "
    "and lowers its frequency. Only the higher value can move closer to 256 Hz when lowered.",
    ["Possible values: 260 Hz or 252 Hz", "Wax lowers the frequency",
     "260 → about 258 Hz: beats with 256 Hz fall to 2/s ✓; 252 → about 250 Hz: beats would rise to 6/s ✗",
     "Unknown frequency = 260 Hz"],
    why="252 Hz would give more beats, not fewer, after loading. 258 Hz is the frequency after loading. 254 Hz "
        "comes from subtracting the new beat frequency from 256 Hz.",
    ncert="Class 11 Physics, 'Waves', beats", seconds=75, recomputed=True)

k1, k2 = 100, 300
ks, kp = F(k1 * k2, k1 + k2), k1 + k2
ratio_T = math.sqrt(kp / ks)
assert ks == 75 and kp == 400 and close(ratio_T, 4 / math.sqrt(3)) and kp / ks == F(16, 3)
add(T, "Spring and pendulum oscillations", "Advanced", "numerical",
    "Two springs of force constants 100 N/m and 300 N/m are used to support the same block, first joined in series "
    "and then joined in parallel. The ratio of the period of oscillation with the springs in series to that with "
    "the springs in parallel is:",
    place("4/√3", ["16/3", "√3/4", "2"], "C"),
    "Combination of springs and T = 2π√(m/k)",
    "Springs in series: 1/k_s = 1/k₁ + 1/k₂. In parallel: k_p = k₁ + k₂. The period varies as 1/√k for the same "
    "mass.",
    ["k_s = (100 × 300)/(100 + 300) = 75 N/m", "k_p = 100 + 300 = 400 N/m",
     "T_s/T_p = √(k_p/k_s) = √(400/75) = √(16/3) = 4/√3 ≈ 2.31"],
    why="16/3 forgets the square root. √3/4 is the inverse ratio (parallel to series). 2 is the ratio for two "
        "identical springs, not for these.",
    seconds=75, recomputed=True)

t1 = math.asin(0.5) / (2 * math.pi)  # in units of T, from x = 0
t2 = math.asin(1.0) / (2 * math.pi)
assert close(t2 - t1, 1 / 6) and close(t1, 1 / 12) and close(t2, 1 / 4)
add(T, "SHM equation and phase", "Advanced", "numerical",
    "A particle executes simple harmonic motion with amplitude A and period T. The minimum time it takes to move "
    "from the position x = A/2 to the extreme position x = A is:",
    place("T/6", ["T/12", "T/4", "T/8"], "B"),
    "Phase of SHM: x = A sin ωt",
    "In SHM the speed is not constant, so time is not proportional to distance. Use the phase angle at each "
    "position.",
    ["x = A sin ωt; x = A/2 at ωt = π/6, x = A at ωt = π/2", "Δ(ωt) = π/2 − π/6 = π/3",
     "Δt = (π/3)/(2π/T) = T/6"],
    why="T/12 is the time from the mean position to A/2. T/4 is the time from the mean position to the extreme. "
        "T/8 assumes uniform speed (half the distance in half of T/4).",
    ncert="Class 11 Physics, 'Oscillations', simple harmonic motion", seconds=75, recomputed=True)

add(T, "Organ pipes and beats", "Advanced", "assertion_reason",
    AR_STEM.format(a="The fundamental frequency of an open organ pipe is twice that of a closed organ pipe of the "
                     "same length.",
                   r="A closed organ pipe produces only the odd harmonics of its fundamental."),
    ar("B"),
    "Normal modes of open and closed pipes",
    "An open pipe has antinodes at both ends, so L = λ/2 and f = v/2L. A closed pipe has a node at the closed end "
    "and an antinode at the open end, so L = λ/4 and f = v/4L. So A is true. R is also true (fₙ = nv/4L, n odd). "
    "But R is about which harmonics a closed pipe has, not about the ratio of the two fundamentals, so it does not "
    "explain A.",
    ["Open: f₁ = v/2L; closed: f₁ = v/4L → ratio 2 → A true", "Closed pipe: n = 1, 3, 5, … → R true",
     "The ratio comes from L = λ/2 versus L = λ/4, not from R → option B"],
    why="Option A is the trap: R is true but explains the harmonic series of a closed pipe, not why its fundamental "
        "is half that of an open pipe.",
    ncert="Class 11 Physics, 'Waves', standing waves in closed and open pipes", seconds=50)

# =====================================================================================================================
# Electrostatics (B6 I7 A6)
# =====================================================================================================================
T = "Electrostatics"
K = 9e9
EPS0 = 8.85e-12

Fc = K * 2e-6 * 3e-6 / 0.3 ** 2
assert close(Fc, 0.6) and close(K * 6e-12 / 0.3, 0.18) and close(K * 6e-12 / 0.009, 6) and close(K * 6e-12 / 0.9, 0.06)
add(T, "Coulomb's law and superposition", "Basic", "numerical",
    "Two point charges of 2 μC and 3 μC are placed 30 cm apart in air. Taking 1/(4πε₀) = 9 × 10⁹ N m² C⁻², the "
    "electrostatic force between them is:",
    place("0.6 N", ["0.18 N", "6 N", "0.06 N"], "D"),
    "Coulomb's law",
    "F = (1/4πε₀) q₁q₂/r², with the charges in coulombs and the distance in metres.",
    ["q₁q₂ = 2 × 10⁻⁶ × 3 × 10⁻⁶ = 6 × 10⁻¹² C²", "r² = (0.3)² = 0.09 m²",
     "F = 9 × 10⁹ × 6 × 10⁻¹²/0.09 = 0.054/0.09 = 0.6 N"],
    why="0.18 N divides by r instead of r². 6 N squares 0.3 as 0.009. 0.06 N squares 0.3 as 0.9.",
    ncert="Class 12 Physics, 'Electric Charges and Fields', Coulomb's law", seconds=35, recomputed=True)

add(T, "Electric field and dipole", "Basic", "direct",
    "Which of the following is a property of electrostatic field lines?",
    place("They start from positive charges and end on negative charges",
          ["They form closed loops", "Two field lines can cross each other",
           "The tangent to a field line gives the direction of the force on a negative test charge"], "A"),
    "Properties of electric field lines",
    "Electrostatic field lines start on positive charges and end on negative charges (or at infinity). They never "
    "form closed loops, since the electrostatic field is conservative, and never cross, since the field has one "
    "direction at each point. The tangent gives the direction of the force on a positive test charge.",
    ["Start: + charge; end: − charge (or infinity)", "No closed loops; no crossing",
     "Tangent = direction of E = direction of force on a positive charge"],
    why="Closed loops would mean non-zero work round a closed path. Crossing lines would give two field directions "
        "at one point. The force on a negative charge is opposite to the tangent.",
    ncert="Class 12 Physics, 'Electric Charges and Fields', electric field lines", seconds=30)

q_in = 5e-6 - 3e-6
assert round(q_in / EPS0 / 1e5, 2) == 2.26 and round(6e-6 / EPS0 / 1e5, 2) == 6.78
assert round(8e-6 / EPS0 / 1e5, 2) == 9.04 and round(5e-6 / EPS0 / 1e5, 2) == 5.65
add(T, "Gauss's law", "Basic", "numerical",
    "A closed surface encloses charges of +5 μC and −3 μC. A charge of +4 μC lies outside the surface. Taking "
    "ε₀ = 8.85 × 10⁻¹² C² N⁻¹ m⁻², the total electric flux through the closed surface is about:",
    place("2.26 × 10⁵ N m² C⁻¹", ["6.78 × 10⁵ N m² C⁻¹", "9.04 × 10⁵ N m² C⁻¹", "5.65 × 10⁵ N m² C⁻¹"], "C"),
    "Gauss's law: Φ = q_enclosed/ε₀",
    "Only the net charge inside the closed surface decides the total flux. A charge outside sends in as much flux as "
    "it takes out.",
    ["q_enclosed = +5 − 3 = +2 μC", "Φ = 2 × 10⁻⁶/(8.85 × 10⁻¹²) ≈ 2.26 × 10⁵ N m² C⁻¹"],
    why="6.78 × 10⁵ includes the outside charge (+6 μC in all). 9.04 × 10⁵ adds the magnitudes of the enclosed "
        "charges (8 μC). 5.65 × 10⁵ counts only the positive charge inside.",
    ncert="Class 12 Physics, 'Electric Charges and Fields', Gauss's law", seconds=40, recomputed=True)

add(T, "Capacitors and dielectrics", "Basic", "direct",
    "The capacitance of a parallel plate capacitor does NOT depend on:",
    place("The charge on its plates", ["The area of its plates", "The separation between its plates",
                                        "The dielectric medium between its plates"], "B"),
    "Capacitance depends on geometry and medium",
    "C = Kε₀A/d. Capacitance is the ratio Q/V; if Q is increased, V rises in the same proportion, so the ratio "
    "is unchanged.",
    ["C = Kε₀A/d depends on A, d and K only", "Q and V change together, keeping Q/V fixed"],
    why="Area, separation and dielectric constant all appear in C = Kε₀A/d.",
    ncert="Class 12 Physics, 'Electrostatic Potential and Capacitance', capacitors and capacitance", seconds=25)

add(T, "Electric field and dipole", "Basic", "match_list",
    match_stem("Match List-I (physical quantity) with List-II (its SI unit).",
               ["Electric flux", "Electric dipole moment", "Permittivity of free space ε₀", "Electric field"],
               ["C m", "N m² C⁻¹", "V m⁻¹", "C² N⁻¹ m⁻²"]),
    match_options({"A": "II", "B": "I", "C": "IV", "D": "III"},
                  [{"A": "I", "B": "II", "C": "IV", "D": "III"}, {"A": "II", "B": "I", "C": "III", "D": "IV"},
                   {"A": "III", "B": "I", "C": "IV", "D": "II"}], "D"),
    "SI units of electrostatic quantities",
    "Read each unit from a defining relation.",
    ["Flux Φ = E × area → (N C⁻¹)(m²) = N m² C⁻¹ → II", "Dipole moment p = q × 2a → C m → I",
     "ε₀ from F = q₁q₂/(4πε₀r²) → C² N⁻¹ m⁻² → IV", "Field E = −dV/dr → V m⁻¹ (same as N C⁻¹) → III"],
    why="The wrong codes swap flux with dipole moment, or field with ε₀ or flux.",
    seconds=35)

add(T, "Electric potential and energy", "Basic", "assertion_reason",
    AR_STEM.format(a="The electric potential at the midpoint of the line joining two equal and opposite point "
                     "charges is zero.",
                   r="The electric field at the midpoint of the line joining two equal and opposite point charges is "
                     "zero."),
    ar("C"),
    "Potential is a scalar sum; field is a vector sum",
    "At the midpoint, kq/r + k(−q)/r = 0, so the potential is zero: A is true. The fields of the two charges both "
    "point from the positive charge towards the negative charge, so they add instead of cancelling: R is false.",
    ["V = kq/r − kq/r = 0 → A true", "E from +q points away from +q, E from −q points towards −q: same direction",
     "E = 2kq/r² ≠ 0 → R false"],
    why="Options A and B treat R as true. Option D denies A, but the scalar potentials do cancel.",
    ncert="Class 12 Physics, 'Electrostatic Potential and Capacitance', potential due to an electric dipole",
    seconds=40)

# +q at x = 0, +4q at x = 3 m: q/x^2 = 4q/(3 - x)^2 between them
x0 = F(3, 1 + 2)
assert x0 == 1 and F(1) / x0 ** 2 == F(4) / (3 - x0) ** 2 and F(3, 5) == F(3, 5)
add(T, "Coulomb's law and superposition", "Intermediate", "numerical",
    "Point charges +q and +4q are fixed on the x-axis at x = 0 and x = 3 m respectively. The electric field is zero "
    "at x =",
    place("1 m", ["2 m", "0.6 m", "1.5 m"], "A"),
    "Superposition of electric fields",
    "For two like charges the null point lies between them, closer to the smaller charge. There the two fields are "
    "equal and opposite.",
    ["kq/x² = k(4q)/(3 − x)²", "(3 − x)/x = 2 → 3 − x = 2x", "x = 1 m"],
    why="2 m is the distance from the larger charge, i.e. the point is placed nearer the wrong charge. 0.6 m divides "
        "the 3 m in the ratio 1 : 4 of the charges instead of 1 : 2 of their square roots. 1.5 m assumes the charges "
        "are equal.",
    seconds=60, recomputed=True)

p_d = 2e-9 * 2e-3
E_ax = 2 * K * p_d / 0.1 ** 3
assert close(p_d, 4e-12) and close(E_ax, 72) and close(K * p_d / 0.1 ** 3, 36)
assert close(2 * K * 2 * p_d / 0.1 ** 3, 144) and close(2 * K * p_d / 0.1 ** 2, 7.2)
add(T, "Electric field and dipole", "Intermediate", "numerical",
    "An electric dipole consists of charges +2 nC and −2 nC separated by 2 mm. Taking 1/(4πε₀) = 9 × 10⁹ N m² C⁻², "
    "the electric field at a point on its axis 10 cm from its centre is about:",
    place("72 N/C", ["36 N/C", "144 N/C", "7.2 N/C"], "B"),
    "Field of a short dipole on its axis",
    "The point is far from the dipole (10 cm ≫ 2 mm), so the short-dipole result E = 2kp/r³ applies.",
    ["p = q × 2a = 2 × 10⁻⁹ × 2 × 10⁻³ = 4 × 10⁻¹² C m", "E = 2kp/r³ = 2 × 9 × 10⁹ × 4 × 10⁻¹²/(0.1)³",
     "E = 0.072/10⁻³ = 72 N/C"],
    why="36 N/C uses the equatorial formula kp/r³. 144 N/C doubles the dipole moment by taking the separation as 2a "
        "with a = 2 mm. 7.2 N/C divides by r² instead of r³.",
    ncert="Class 12 Physics, 'Electric Charges and Fields', electric field of a dipole", seconds=60, recomputed=True)

add(T, "Gauss's law", "Intermediate", "match_list",
    match_stem("Match List-I (charge distribution and point) with List-II (magnitude of the electric field there), "
               "using Gauss's law.",
               ["Infinitely long straight wire with linear charge density λ, at distance r",
                "Infinite plane sheet with surface charge density σ, at any point near it",
                "Thin spherical shell with total charge q, at distance r from its centre (r > radius)",
                "Thin spherical shell with total charge q, at a point inside it"],
               ["Zero", "σ/(2ε₀)", "λ/(2πε₀r)", "q/(4πε₀r²)"]),
    match_options({"A": "III", "B": "II", "C": "IV", "D": "I"},
                  [{"A": "IV", "B": "II", "C": "III", "D": "I"}, {"A": "III", "B": "I", "C": "IV", "D": "II"},
                   {"A": "II", "B": "III", "C": "IV", "D": "I"}], "C"),
    "Applications of Gauss's law",
    "Choose a Gaussian surface that matches the symmetry: a coaxial cylinder for the wire, a pill-box for the sheet "
    "and a concentric sphere for the shell.",
    ["Wire: E(2πrl) = λl/ε₀ → E = λ/(2πε₀r) → III", "Sheet: 2EA = σA/ε₀ → E = σ/(2ε₀) → II",
     "Shell, outside: E(4πr²) = q/ε₀ → q/(4πε₀r²) → IV", "Shell, inside: no charge enclosed → E = 0 → I"],
    why="The wrong codes swap the wire and shell results, or give the sheet a zero field.",
    ncert="Class 12 Physics, 'Electric Charges and Fields', applications of Gauss's law", seconds=50)

U3 = 3 * K * (1e-6) ** 2 / 0.1
assert close(U3, 0.27) and close(U3 / 3, 0.09) and close(2 * U3, 0.54) and close(3 * K * 1e-12 / 0.01, 2.7)
add(T, "Electric potential and energy", "Intermediate", "numerical",
    "Three point charges, each of +1 μC, are placed at the corners of an equilateral triangle of side 10 cm. Taking "
    "1/(4πε₀) = 9 × 10⁹ N m² C⁻², the electrostatic potential energy of the system is:",
    place("0.27 J", ["0.09 J", "0.54 J", "2.7 J"], "D"),
    "Potential energy of a system of point charges",
    "U is the sum of kqᵢqⱼ/rᵢⱼ over every distinct pair. Three charges make three pairs, all at the same distance "
    "here.",
    ["One pair: kq²/a = 9 × 10⁹ × 10⁻¹²/0.1 = 0.09 J", "Three pairs: U = 3 × 0.09 = 0.27 J"],
    why="0.09 J counts only one pair. 0.54 J counts each pair twice. 2.7 J divides by a² instead of a.",
    ncert="Class 12 Physics, 'Electrostatic Potential and Capacitance', potential energy of a system of charges",
    seconds=50, recomputed=True)

C1s, C2s, Vb = 3, 6, 90
Cs = F(C1s * C2s, C1s + C2s)
Qs_ = Cs * Vb
assert Cs == 2 and Qs_ == 180 and Qs_ / C1s == 60 and Qs_ / C2s == 30
add(T, "Capacitors and dielectrics", "Intermediate", "numerical",
    "Capacitors of 3 μF and 6 μF are connected in series across a 90 V battery. The potential difference across the "
    "3 μF capacitor is:",
    place("60 V", ["30 V", "45 V", "90 V"], "A"),
    "Capacitors in series carry the same charge",
    "In series every capacitor gets the same charge Q, so the voltage V = Q/C is larger across the smaller "
    "capacitor.",
    ["C_eq = (3 × 6)/(3 + 6) = 2 μF", "Q = 2 μF × 90 V = 180 μC", "V(3 μF) = 180/3 = 60 V (and 30 V across 6 μF)"],
    why="30 V is the voltage across the 6 μF capacitor. 45 V splits the voltage equally. 90 V treats the capacitors "
        "as if in parallel.",
    seconds=45, recomputed=True)

add(T, "Capacitors and dielectrics", "Intermediate", "statement_pair",
    SP_STEM.format(s1="When a dielectric slab is inserted between the plates of a charged parallel plate capacitor "
                      "that has been disconnected from the battery, the potential difference between the plates "
                      "increases.",
                   s2="When a dielectric slab is inserted between the plates of a parallel plate capacitor that stays "
                      "connected to a battery, the charge on the plates remains unchanged."),
    sp("B"),
    "Effect of a dielectric: isolated capacitor versus capacitor kept at fixed voltage",
    "A dielectric raises the capacitance (C → KC). Isolated capacitor: Q is fixed, so V = Q/C falls, and Statement "
    "I is false. Battery connected: V is fixed, so Q = CV rises, and Statement II is false.",
    ["Isolated: Q constant, C → KC → V → V/K (decreases) → I false",
     "Connected: V constant, C → KC → Q → KQ (increases) → II false"],
    ncert="Class 12 Physics, 'Electrostatic Potential and Capacitance', effect of dielectric on capacitance",
    seconds=45)

add(T, "Electric potential and energy", "Intermediate", "multi_statement",
    multi("Which of the following statements about equipotential surfaces are correct?",
          ["No work is done in moving a test charge from one point to another on an equipotential surface.",
           "The electric field at every point is normal to the equipotential surface through that point.",
           "Two different equipotential surfaces can intersect each other.",
           "The equipotential surfaces of an isolated point charge are concentric spheres centred on the charge.",
           "Electric field lines point in the direction in which the potential increases."]),
    place("(a), (b) and (d) only", ["(a), (b), (c) and (d) only", "(b), (d) and (e) only", "(a), (d) and (e) only"],
          "D"),
    "Equipotential surfaces",
    "On an equipotential surface ΔV = 0, so W = qΔV = 0 and the field can have no component along the surface. "
    "If two equipotentials met, the meeting point would have two potentials. For a point charge V = kq/r, constant "
    "on spheres. The field points from higher to lower potential (E = −dV/dr).",
    ["(a) True: W = qΔV = 0", "(b) True: E has no component along the surface", "(c) False",
     "(d) True: V depends only on r", "(e) False: E points towards decreasing potential"],
    ncert="Class 12 Physics, 'Electrostatic Potential and Capacitance', equipotential surfaces", seconds=50)

Ca, Va, Cb = 6e-6, 100, 3e-6
Vc = Ca * Va / (Ca + Cb)
U_i, U_f = 0.5 * Ca * Va ** 2, 0.5 * (Ca + Cb) * Vc ** 2
assert close(U_i, 0.03) and close(U_f, 0.02) and close(U_i - U_f, 0.01)
add(T, "Capacitors and dielectrics", "Advanced", "numerical",
    "A 6 μF capacitor is charged to 100 V and then disconnected from the battery. It is now connected across an "
    "uncharged 3 μF capacitor. The energy lost in the process (as heat and radiation) is:",
    place("0.01 J", ["0.02 J", "0.03 J", "0 J"], "C"),
    "Charge sharing between capacitors",
    "Charge is conserved when the capacitors are joined, but electrostatic energy is not: some is lost in the "
    "connecting wires as the charge redistributes.",
    ["Initial charge Q = 6 μF × 100 V = 600 μC; initial energy = ½ × 6 × 10⁻⁶ × 100² = 0.03 J",
     "Common voltage V = 600 μC/9 μF = 200/3 V", "Final energy = ½ × 9 × 10⁻⁶ × (200/3)² = 0.02 J",
     "Energy lost = 0.03 − 0.02 = 0.01 J"],
    shortcut="Loss = ½ (C₁C₂/(C₁ + C₂)) V² = ½ × 2 × 10⁻⁶ × 100² = 0.01 J.",
    why="0.02 J is the final stored energy. 0.03 J is the initial energy. 0 J wrongly assumes energy is conserved "
        "just because charge is.",
    seconds=90, recomputed=True)

d_ = F(1)
C_slab = d_ / (d_ - F(1, 2) + F(1, 2) / 3)  # in units of C0
assert C_slab == F(3, 2) and d_ / (d_ - F(1, 2) + F(1, 2) * 3) == F(1, 2)
add(T, "Capacitors and dielectrics", "Advanced", "numerical",
    "A parallel plate capacitor has capacitance C₀ with air between its plates, which are a distance d apart. A slab "
    "of dielectric constant 3, of the same area as the plates and of thickness d/2, is placed between the plates. "
    "The new capacitance is:",
    place("1.5 C₀", ["2 C₀", "3 C₀", "0.5 C₀"], "A"),
    "Capacitor partly filled with a dielectric",
    "The slab and the remaining air gap act like two capacitors in series. Equivalently, a slab of thickness t "
    "replaces a thickness t of air by an 'effective' thickness t/K: C = ε₀A/(d − t + t/K).",
    ["C = ε₀A/(d − t + t/K) with t = d/2, K = 3", "Denominator = d/2 + d/6 = 2d/3", "C = (3/2) ε₀A/d = 1.5 C₀"],
    why="2 C₀ averages the dielectric constants (as if the slab covered half the area side by side). 3 C₀ assumes "
        "the slab fills the whole gap. 0.5 C₀ multiplies the slab thickness by K instead of dividing.",
    ncert="Class 12 Physics, 'Electrostatic Potential and Capacitance', effect of dielectric on capacitance",
    seconds=90, recomputed=True)

p_w, E_w = 3e-9, 2e4
W_rot = p_w * E_w * (math.cos(0) - math.cos(math.pi))
assert close(W_rot, 1.2e-4) and close(p_w * E_w, 6e-5)
add(T, "Electric field and dipole", "Advanced", "numerical",
    "An electric dipole of dipole moment 3 × 10⁻⁹ C m is in stable equilibrium in a uniform electric field of "
    "2 × 10⁴ N/C. The work done by an external agent in slowly rotating it through 180° is:",
    place("1.2 × 10⁻⁴ J", ["6.0 × 10⁻⁵ J", "0", "−1.2 × 10⁻⁴ J"], "B"),
    "Potential energy of a dipole in a uniform field: U = −pE cos θ",
    "Stable equilibrium is θ = 0 (U = −pE). After turning through 180°, θ = 180° (U = +pE), the unstable position. "
    "The external work (done slowly, so no kinetic energy is given) equals the rise in potential energy.",
    ["U(0°) = −pE; U(180°) = +pE", "W = ΔU = 2pE = 2 × 3 × 10⁻⁹ × 2 × 10⁴", "W = 1.2 × 10⁻⁴ J"],
    why="6.0 × 10⁻⁵ J (= pE) is the work for turning through only 90°. 0 assumes the start and end positions are "
        "equivalent. −1.2 × 10⁻⁴ J is the work done by the field, not by the external agent.",
    ncert="Class 12 Physics, 'Electrostatic Potential and Capacitance', potential energy of a dipole in an external "
          "field", seconds=75, recomputed=True)

q_c = 53.1e-9
assert close(q_c / EPS0, 6000) and close(q_c / (8 * EPS0), 750) and close(q_c / (6 * EPS0), 1000)
assert close(q_c / (2 * EPS0), 3000)
add(T, "Gauss's law", "Advanced", "numerical",
    "A point charge of 53.1 nC is placed at one corner of a cube. Taking ε₀ = 8.85 × 10⁻¹² C² N⁻¹ m⁻², the total "
    "electric flux through the cube is:",
    place("750 N m² C⁻¹", ["1000 N m² C⁻¹", "6000 N m² C⁻¹", "3000 N m² C⁻¹"], "D"),
    "Gauss's law with symmetry",
    "A charge at a corner is shared by 8 identical cubes that together surround it completely. By symmetry each "
    "cube receives one-eighth of the total flux q/ε₀.",
    ["Total flux from the charge = q/ε₀ = 53.1 × 10⁻⁹/(8.85 × 10⁻¹²) = 6000 N m² C⁻¹",
     "8 cubes meet at a corner → flux through one cube = 6000/8 = 750 N m² C⁻¹"],
    why="1000 is q/6ε₀, the flux through one face when the charge is at the centre of the cube. 6000 is the full "
        "q/ε₀, as if the charge were inside. 3000 is q/2ε₀, the case of a charge at the centre of a face.",
    ncert="Class 12 Physics, 'Electric Charges and Fields', Gauss's law", seconds=75, recomputed=True)

R_sh, V_s = 0.10, 900
Q_sh = V_s * R_sh / K
assert close(K * Q_sh / R_sh, 900) and close(K * Q_sh / 0.20, 450) and close(K * Q_sh / 0.05, 1800)
assert close(V_s * (R_sh / 0.20) ** 2, 225)
add(T, "Electric potential and energy", "Advanced", "numerical",
    "A thin spherical conducting shell of radius 10 cm is charged so that the potential at its surface is 900 V. "
    "The potentials at points 5 cm and 20 cm from its centre are respectively:",
    place("900 V and 450 V", ["1800 V and 450 V", "0 V and 450 V", "900 V and 225 V"], "C"),
    "Potential inside and outside a charged spherical shell",
    "Outside the shell, V = kQ/r, as if all the charge were at the centre. Inside, the field is zero, so the "
    "potential does not change from its value at the surface.",
    ["Inside (r = 5 cm): E = 0 → V = V(surface) = 900 V", "Outside (r = 20 cm): V ∝ 1/r → 900 × 10/20 = 450 V"],
    why="1800 V applies kQ/r inside the shell as well. 0 V confuses zero field with zero potential. 225 V uses "
        "1/r² (as for the field) outside.",
    ncert="Class 12 Physics, 'Electrostatic Potential and Capacitance', electrostatics of conductors", seconds=60,
    recomputed=True)

Cpar = 2 + 4
Cnet = F(Cpar * 3, Cpar + 3)
Qn = Cnet * 12
Vpar = Qn / Cpar
assert Cnet == 2 and Qn == 24 and Vpar == 4 and 4 * Vpar == 16 and 2 * Vpar == 8 and 4 * 12 == 48
add(T, "Capacitors and dielectrics", "Advanced", "numerical",
    "Capacitors of 2 μF and 4 μF are connected in parallel, and this combination is connected in series with a "
    "3 μF capacitor. The arrangement is connected across a 12 V battery. The charge on the 4 μF capacitor is:",
    place("16 μC", ["24 μC", "8 μC", "48 μC"], "A"),
    "Series–parallel combinations of capacitors",
    "Reduce the network step by step, find the total charge, then the voltage across the parallel pair, and finally "
    "the charge on the 4 μF capacitor.",
    ["Parallel pair: 2 + 4 = 6 μF", "Series with 3 μF: C = (6 × 3)/(6 + 3) = 2 μF", "Q = 2 × 12 = 24 μC",
     "Voltage across the pair = 24/6 = 4 V → Q(4 μF) = 4 × 4 = 16 μC"],
    why="24 μC is the total charge, which the parallel pair shares. 8 μC is the charge on the 2 μF capacitor. "
        "48 μC puts the full 12 V across the 4 μF capacitor.",
    seconds=90, recomputed=True)


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
    doc = {"schema_version": "1.0", "batch_id": "BATCH_001", "created_at": TODAY,
           "notes": "BATCH_001 package PHY_001_p1: 130 original Physics questions (Physics and Measurement through "
                    "Electrostatics). Every numerical answer is re-derived in tools/batch_001/PHY_001_p1.py.",
           "stimuli": [], "questions": QUESTIONS}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {OUT}: {n} questions, {dict(Counter(x['difficulty'] for x in QUESTIONS))}")
    print(f"keys {dict(sorted(keys.items()))}")
    print(f"formats {dict(fmts)}")
