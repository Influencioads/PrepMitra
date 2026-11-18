"""Writes batches/parts/BATCH_005_PHY_p1.json: package PHY_005_p1 of BATCH_005 (127 Physics questions).

Topics: Physics and Measurement, Kinematics, Laws of Motion, Work Energy and Power, Rotational Motion, Gravitation,
Properties of Solids and Liquids, Thermodynamics, Kinetic Theory of Gases, Oscillations and Waves, Electrostatics.
IDs NEET_PHY_001001 .. NEET_PHY_001127, in the order the questions are listed below.

Every computable answer is re-derived with an assert before the file is written, and so is the plan quota. If any
assert fails, nothing is written. Each question's answer position is chosen by hand and fixed.

    python tools/batch_005/PHY_005_p1.py        (run from docs/neet-bank)
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
OUT = ROOT / "batches" / "parts" / "BATCH_005_PHY_p1.json"
PLAN = ROOT / "batches" / "plans" / "BATCH_005_plan.json"
PACKAGE = "PHY_005_p1"
TODAY = "2026-11-16"
LETTERS = "ABCD"
PHY = "Physics"
RECOMPUTED = ("script:recompute", "ai:author-solve", "ai:self-recheck")
AUTHORED = ("ai:author-solve", "ai:self-recheck")
FIRST_ID = 1001

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


def round_half_even_3sf(s):
    """NCERT rounding of a 4-significant-figure decimal string whose last digit is 5 to 3 significant figures."""
    head, last = s[:-1], s[-1]
    assert last == "5"
    prev = int(head[-1])
    if prev % 2 == 1:
        return f"{float(head) + 0.01:.2f}"
    return head


# =====================================================================================================================
# Physics and Measurement (B2 I2 A2)
# =====================================================================================================================
T = "Physics and Measurement"

assert round_half_even_3sf("2.745") == "2.74" and round_half_even_3sf("2.735") == "2.74"
add(T, "Least count and significant figures", "Basic", "direct",
    "Following the rules for rounding off given in NCERT, the numbers 2.745 and 2.735, each rounded off to three "
    "significant figures, become respectively:",
    place("2.74 and 2.74", ["2.75 and 2.74", "2.74 and 2.73", "2.75 and 2.73"], "B"),
    "Rounding off when the dropped digit is 5",
    "When the digit to be dropped is 5 (with nothing after it), NCERT's convention looks at the digit before it: "
    "if that digit is even it is left unchanged, and if it is odd it is raised by one. This avoids always rounding "
    "up, which would bias a long calculation.",
    ["2.745: digit before the 5 is 4 (even) → drop the 5 → 2.74",
     "2.735: digit before the 5 is 3 (odd) → raise it by one → 2.74"],
    why="2.75 rounds every 5 upward; 2.73 simply truncates; both ignore the even-odd rule.",
    ncert="Class 11 Physics, 'Units and Measurement', significant figures (rounding off the uncertain digits)",
    seconds=35)

add(T, "Units and SI system", "Basic", "match_list",
    match_stem("Match List-I (derived quantity) with List-II (its SI unit written in terms of SI base units).",
               ["Pressure", "Power", "Electric charge", "Linear momentum"],
               ["kg m s⁻¹", "A s", "kg m⁻¹ s⁻²", "kg m² s⁻³"]),
    match_options({"A": "III", "B": "IV", "C": "II", "D": "I"},
                  [{"A": "IV", "B": "III", "C": "II", "D": "I"}, {"A": "III", "B": "IV", "C": "I", "D": "II"},
                   {"A": "I", "B": "IV", "C": "II", "D": "III"}], "C"),
    "Derived SI units in base units",
    "Each derived unit follows from the defining relation of the quantity, with the newton written as kg m s⁻².",
    ["Pressure = force/area = kg m s⁻²/m² = kg m⁻¹ s⁻² → III",
     "Power = work/time = kg m² s⁻²/s = kg m² s⁻³ → IV",
     "Charge = current × time = A s (coulomb) → II", "Momentum = mass × velocity = kg m s⁻¹ → I"],
    why="The other codes swap pressure with power, or charge with momentum; only charge involves the ampere.",
    ncert="Class 11 Physics, 'Units and Measurement', the international system of units", seconds=45)

m_, dm_ = 10.0, 0.1
a_, da_ = 2.00, 0.01
rho = m_ / a_ ** 3
rel = dm_ / m_ + 3 * da_ / a_
assert close(rho, 1.25) and close(rel, 0.025) and round(rho * rel, 2) == 0.03
assert round(rho * (dm_ / m_), 2) == 0.01 and round(rho * (dm_ / m_ + da_ / a_), 2) == 0.02
assert round(rho * (0.01 + 3 * 0.01), 2) == 0.05
add(T, "Errors in measurement", "Intermediate", "numerical",
    "The mass of a cube is measured as (10.0 ± 0.1) g and the length of its side as (2.00 ± 0.01) cm. Its density, "
    "with the maximum absolute error rounded to two decimal places, is:",
    place("(1.25 ± 0.03) g cm⁻³", ["(1.25 ± 0.01) g cm⁻³", "(1.25 ± 0.02) g cm⁻³", "(1.25 ± 0.05) g cm⁻³"], "D"),
    "Combination of errors in a quotient and a power",
    "ρ = m/a³. In a quotient the relative errors add, and a quantity raised to the power n contributes n times "
    "its relative error. The absolute error is the relative error times the value.",
    ["ρ = 10.0/2.00³ = 1.25 g cm⁻³",
     "Δρ/ρ = Δm/m + 3Δa/a = 0.01 + 3 × 0.005 = 0.025",
     "Δρ = 0.025 × 1.25 = 0.031 ≈ 0.03 g cm⁻³"],
    why="±0.01 keeps only the mass error. ±0.02 forgets to multiply the side's relative error by 3. ±0.05 treats "
        "the absolute error 0.01 cm of the side as a 1% relative error.",
    ncert="Class 11 Physics, 'Units and Measurement', combination of errors", seconds=75, recomputed=True)

add(T, "Least count and significant figures", "Intermediate", "assertion_reason",
    AR_STEM.format(
        a="When the circumference of a circle is calculated from 2πr using a measured radius, the factor 2 does not "
          "limit the number of significant figures in the result.",
        r="Exact numbers, such as the 2 in 2πr, have an infinite number of significant figures."),
    ar("A"),
    "Significant figures of exact numbers",
    "Only measured values carry uncertainty. Pure counting or defining numbers like the 2 in 2πr are exact, so "
    "they can be written 2.000… with as many zeros as needed. Because they have unlimited significant figures, "
    "the result's significant figures are fixed by the measured radius (and by the value of π used).",
    ["2 is exact → infinitely many significant figures (R)",
     "So it never is the least precise factor → it does not limit the result (A)"],
    why="R is the very reason the factor 2 cannot limit the significant figures, so it explains A.",
    ncert="Class 11 Physics, 'Units and Measurement', rules for arithmetic operations with significant figures",
    seconds=45)

D_E = dims(1, 2, -2)
D_beta = dmul(dims(t=2), dinv(dmul(D_E, dims(l=1))))
assert D_beta == (-1, -3, 4)
add(T, "Dimensional analysis", "Advanced", "direct",
    "The energy E of a system depends on the distance x and the time t as E = (α − t²)/(βx), where α and β are "
    "constants. The dimensional formula of β is:",
    place("[M⁻¹ L⁻³ T⁴]", ["[M L³ T⁻⁴]", "[M⁻¹ L⁻¹ T⁴]", "[M⁻¹ L⁻³ T²]"], "B"),
    "Principle of homogeneity of dimensions",
    "α is subtracted from t², so α has the dimensions of t², i.e. [T²]. The numerator therefore has dimensions "
    "[T²], and dividing it by βx must give an energy.",
    ["[α] = [T²] → numerator has [T²]",
     "[E] = [T²]/([β][L]) → [β] = [T²]/([M L² T⁻²][L])",
     "[β] = [M⁻¹ L⁻³ T⁴]"],
    why="[M L³ T⁻⁴] is the reciprocal. [M⁻¹ L⁻¹ T⁴] forgets the factor x in the denominator. [M⁻¹ L⁻³ T²] drops "
        "the T⁻² inside the energy.",
    ncert="Class 11 Physics, 'Units and Measurement', dimensional analysis and its applications", seconds=75)

add(T, "Errors in measurement", "Advanced", "statement_pair",
    SP_STEM.format(
        s1="A set of measurements can be precise without being accurate.",
        s2="If the true length of a rod is 3.678 cm, a reading of 3.5 cm taken with an instrument of resolution "
           "0.1 cm is more precise than a reading of 3.38 cm taken with an instrument of resolution 0.01 cm."),
    sp("C"),
    "Accuracy versus precision",
    "Accuracy is how close a measurement is to the true value; precision is the resolution, the limit to which "
    "the quantity is measured. A finely graduated instrument with a zero error gives precise but inaccurate "
    "readings, so Statement I is true. In Statement II the 0.1 cm instrument gives 3.5 cm, which is closer to "
    "3.678 cm (more accurate) but less precise; the 0.01 cm instrument gives the more precise reading 3.38 cm.",
    ["Statement I: precision ≠ accuracy → true",
     "|3.678 − 3.5| = 0.178 < |3.678 − 3.38| = 0.298 → 3.5 cm is more accurate",
     "Resolution 0.1 cm is coarser than 0.01 cm → 3.5 cm is less precise → Statement II false"],
    why="Statement II swaps the two ideas: the closer reading is the more accurate one, not the more precise one.",
    ncert="Class 11 Physics, 'Units and Measurement', accuracy, precision of instruments and errors in "
          "measurement", seconds=60)


# =====================================================================================================================
# Kinematics (B3 I5 A4)
# =====================================================================================================================
T = "Kinematics"

x_ = lambda t: 2 * t ** 2 + 3
assert (x_(3) - x_(1)) / 2 == 8 and 4 * 3 == 12 and 4 * 1 == 4 and x_(3) / 2 == 10.5
add(T, "Motion in a straight line", "Basic", "numerical",
    "The position of a particle moving along the x-axis is x = 2t² + 3, where x is in metres and t in seconds. Its "
    "average velocity between t = 1 s and t = 3 s is:",
    place("8 m/s", ["12 m/s", "4 m/s", "10.5 m/s"], "D"),
    "Average velocity from a position–time relation",
    "Average velocity is the change in position divided by the time interval, not the velocity at either end.",
    ["x(1) = 5 m, x(3) = 21 m", "Average velocity = (21 − 5)/(3 − 1) = 8 m/s"],
    shortcut="For uniform acceleration the average velocity is the mean of the end velocities: (4 + 12)/2 = 8 m/s.",
    why="12 m/s and 4 m/s are the instantaneous velocities (v = 4t) at t = 3 s and t = 1 s. 10.5 m/s divides the "
        "final position by the interval instead of the displacement.",
    ncert="Class 11 Physics, 'Motion in a Straight Line', average velocity and average speed", seconds=40,
    recomputed=True)

add(T, "Vectors", "Basic", "match_list",
    match_stem("î, ĵ and k̂ are the unit vectors along the x-, y- and z-axes of a right-handed coordinate system. "
               "Match List-I (product) with List-II (its value).",
               ["î × ĵ", "ĵ × î", "î · î", "k̂ × î"], ["ĵ", "1", "−k̂", "k̂"]),
    match_options({"A": "IV", "B": "III", "C": "II", "D": "I"},
                  [{"A": "III", "B": "IV", "C": "II", "D": "I"}, {"A": "IV", "B": "III", "C": "I", "D": "II"},
                   {"A": "IV", "B": "I", "C": "II", "D": "III"}], "A"),
    "Scalar and vector products of unit vectors",
    "In a right-handed system the cyclic order î → ĵ → k̂ → î gives positive cross products; reversing the order "
    "changes the sign. The dot product of a unit vector with itself is 1.",
    ["î × ĵ = k̂ → IV", "ĵ × î = −(î × ĵ) = −k̂ → III", "î · î = 1 × 1 × cos 0° = 1 → II",
     "k̂ × î = ĵ (cyclic order) → I"],
    why="The other codes either forget that the cross product changes sign when the order is reversed, or treat "
        "î · î as a vector.",
    ncert="Class 11 Physics, 'Motion in a Plane' (scalar product) and 'System of Particles and Rotational Motion' "
          "(vector product)", seconds=40)

vA, vB = 54 * 5 / 18, 72 * 5 / 18
assert vA == 15 and vB == 20 and vB - vA == 5 and vA + vB == 35
add(T, "Relative velocity", "Basic", "numerical",
    "Two cars move along a straight road in the same direction, car P at 54 km/h and car Q at 72 km/h. The velocity "
    "of Q relative to P is:",
    place("5 m/s, in the direction of motion", ["35 m/s, in the direction of motion", "5 m/s, opposite to the "
          "direction of motion", "20 m/s, in the direction of motion"], "C"),
    "Relative velocity in one dimension",
    "v_QP = v_Q − v_P. With both velocities along the same direction, the relative velocity is the difference of "
    "the speeds and points along the motion because Q is faster.",
    ["54 km/h = 15 m/s, 72 km/h = 20 m/s", "v_QP = 20 − 15 = +5 m/s (along the motion)"],
    why="35 m/s adds the speeds, as for cars moving in opposite directions. 'Opposite to the motion' is the "
        "velocity of P relative to Q. 20 m/s is Q's velocity relative to the ground.",
    ncert="Class 11 Physics, 'Motion in a Straight Line', relative velocity", seconds=35, recomputed=True)

ratio = math.sin(math.radians(30)) ** 2 / math.sin(math.radians(60)) ** 2
assert close(ratio, 1 / 3)
add(T, "Projectile motion", "Intermediate", "numerical",
    "Two balls are projected from level ground with the same speed, one at 30° and the other at 60° above the "
    "horizontal. Neglecting air resistance, the ratio of the maximum height reached by the first ball to that "
    "reached by the second is:",
    place("1 : 3", ["1 : √3", "1 : 2", "1 : 1"], "B"),
    "Maximum height of a projectile",
    "H = u² sin² θ/(2g). With the same speed, H is proportional to sin² θ.",
    ["H₁/H₂ = sin² 30°/sin² 60° = (1/4)/(3/4) = 1/3"],
    why="1 : √3 uses sin θ instead of sin² θ. 1 : 2 compares the angles themselves. 1 : 1 confuses the heights "
        "with the ranges, which are equal for complementary angles.",
    ncert="Class 11 Physics, 'Motion in a Plane', projectile motion", seconds=45, recomputed=True)

v_rain = 10 * math.sqrt(3)
v_cyc = v_rain * math.tan(math.radians(30))
assert close(v_cyc, 10) and close(v_rain * math.tan(math.radians(60)), 30) and close(v_rain * 0.5, 5 * math.sqrt(3))
add(T, "Relative velocity", "Intermediate", "numerical",
    "Rain falls vertically downward with a speed of 10√3 m/s. To a cyclist moving along a level road, the rain "
    "appears to fall at an angle of 30° with the vertical. The speed of the cyclist is:",
    place("10 m/s", ["30 m/s", "5√3 m/s", "20 m/s"], "B"),
    "Relative velocity of rain with respect to a moving observer",
    "Relative to the cyclist, the rain has its true vertical velocity plus a horizontal velocity equal and opposite "
    "to the cyclist's. The angle α with the vertical satisfies tan α = v_cyclist/v_rain.",
    ["tan 30° = v_c/(10√3)", "v_c = 10√3 × (1/√3) = 10 m/s"],
    why="30 m/s uses tan 60°, i.e. measures the angle from the horizontal. 5√3 m/s uses sin 30° instead of tan "
        "30°. 20 m/s is the apparent speed of the rain, not the cyclist's speed.",
    ncert="Class 11 Physics, 'Motion in a Plane', relative velocity in two dimensions", seconds=50, recomputed=True)

r_, v_ = 5, 10
dv = v_ * math.sqrt(2)
t_q = (2 * math.pi * r_ / 4) / v_
a_avg = dv / t_q
assert close(t_q, math.pi / 4) and close(a_avg, 40 * math.sqrt(2) / math.pi) and v_ ** 2 / r_ == 20
add(T, "Uniform circular motion", "Intermediate", "numerical",
    "A particle moves with a constant speed of 10 m/s along a circle of radius 5 m. The magnitude of its average "
    "acceleration while it goes round one quarter of the circle is:",
    place("40√2/π m/s²", ["20 m/s²", "40/π m/s²", "80/π m/s²"], "D"),
    "Average acceleration as change in velocity over time",
    "Average acceleration = (change in velocity)/(time). After a quarter turn the velocity has the same magnitude "
    "but has turned through 90°, so |Δv| = v√2. The time is a quarter of the period.",
    ["|Δv| = √(10² + 10²) = 10√2 m/s", "t = (2π × 5/4)/10 = π/4 s",
     "a_avg = 10√2/(π/4) = 40√2/π ≈ 18 m/s²"],
    why="20 m/s² is the instantaneous centripetal acceleration v²/r, not the average over the quarter turn. "
        "40/π m/s² takes |Δv| as 10 m/s. 80/π m/s² takes |Δv| as 2v, as for half a turn.",
    ncert="Class 11 Physics, 'Motion in a Plane', uniform circular motion", seconds=80, recomputed=True)

add(T, "Projectile motion", "Intermediate", "assertion_reason",
    AR_STEM.format(
        a="For a projectile moving under gravity alone, the change in its velocity over any time interval is "
          "directed vertically downward.",
        r="The acceleration of such a projectile is constant and directed vertically downward."),
    ar("A"),
    "Constant acceleration in projectile motion",
    "With constant acceleration g, the change in velocity over an interval Δt is Δv = gΔt, which has the "
    "direction of g. The horizontal component of velocity never changes, so the whole change is vertical.",
    ["a = g (constant, downward)", "Δv = g Δt → vertically downward for every Δt"],
    why="R gives the constant downward acceleration, which directly makes every Δv vertical, so R explains A.",
    ncert="Class 11 Physics, 'Motion in a Plane', projectile motion", seconds=45)

Ax, Ay, Bx, By = 3, 4, 1, 1
comp = (Ax * Bx + Ay * By) / math.hypot(Bx, By)
assert close(comp, 7 / math.sqrt(2))
add(T, "Vectors", "Intermediate", "numerical",
    "The component of the vector A = 3î + 4ĵ along the direction of the vector B = î + ĵ is:",
    place("7/√2", ["7", "5", "7√2"], "C"),
    "Projection of one vector on another",
    "The component of A along B is A · B̂ = (A · B)/|B|, the scalar projection of A on the direction of B.",
    ["A · B = 3 + 4 = 7", "|B| = √2", "Component = 7/√2 ≈ 4.95"],
    why="7 forgets to divide by |B|. 5 is the magnitude of A itself. 7√2 multiplies by |B| instead of dividing.",
    ncert="Class 11 Physics, 'Motion in a Plane', resolution of vectors and scalar product", seconds=45,
    recomputed=True)

# oblique components larger than the vector: A = a + b with a, b at 160° to each other
a_obl = b_obl = 5.0
res = math.sqrt(a_obl ** 2 + b_obl ** 2 + 2 * a_obl * b_obl * math.cos(math.radians(160)))
assert res < a_obl
add(T, "Vectors", "Advanced", "statement_pair",
    SP_STEM.format(
        s1="A vector lying in a plane can be expressed as the sum of two vectors along any two given non-parallel "
           "directions in that plane.",
        s2="When a vector is resolved along two non-parallel directions (not necessarily perpendicular), the "
           "magnitude of each component is always less than or equal to the magnitude of the vector."),
    sp("C"),
    "Resolution of vectors along arbitrary directions",
    "Any vector A in a plane can be written as A = λa + μb for two non-zero, non-parallel vectors a and b in that "
    "plane, so Statement I is true. Only for perpendicular (rectangular) components is each component limited by "
    "|A|. For oblique directions the components can be larger: two vectors of magnitude 5 at 160° to each other "
    "add up to a resultant of only about 1.7.",
    ["Statement I: resolution along any two non-parallel directions → true",
     "R² = 5² + 5² + 2·5·5·cos 160° → R ≈ 1.74 < 5 → components larger than the vector",
     "Statement II → false"],
    why="Statement II holds only for rectangular components, where A_x = A cos θ ≤ A.",
    ncert="Class 11 Physics, 'Motion in a Plane', resolution of vectors", seconds=70)

g = 10
y1 = lambda t: 20 * t - 0.5 * g * t ** 2
y2 = lambda t: 20 * (t - 1) - 0.5 * g * (t - 1) ** 2
t_meet = 2.5
assert close(y1(t_meet), y2(t_meet)) and close(y1(t_meet), 18.75) and 20 ** 2 / (2 * g) == 20
add(T, "Motion in a straight line", "Advanced", "numerical",
    "A ball is thrown vertically upward from the ground with a speed of 20 m/s. One second later, a second ball is "
    "thrown vertically upward from the same point with the same speed. Taking g = 10 m/s² and neglecting air "
    "resistance, the two balls meet at a height above the ground of:",
    place("18.75 m", ["20 m", "15 m", "11.25 m"], "B"),
    "Two bodies under free fall with a time lag",
    "Write the height of each ball as a function of the time t after the first throw and equate them.",
    ["First ball: y₁ = 20t − 5t²", "Second ball: y₂ = 20(t − 1) − 5(t − 1)²",
     "y₁ = y₂ → 0 = −20 − 5(1 − 2t) → 10t = 25 → t = 2.5 s",
     "y = 20(2.5) − 5(2.5)² = 50 − 31.25 = 18.75 m"],
    shortcut="By symmetry the balls meet half a second either side of the first ball's peak time (2 s): t = 2.5 s.",
    why="20 m is the maximum height of each ball; they cannot meet there because the first ball is already "
        "falling when the second rises. 15 m and 11.25 m are heights at t = 1 s and 1.5 s of one ball's motion.",
    seconds=100, recomputed=True)

v4 = 2 * 4
s1 = 0.5 * 2 * 4 ** 2
s2 = v4 * 4 - 0.5 * 1 * 4 ** 2
assert s1 == 16 and s2 == 24 and s1 + s2 == 40 and s1 + v4 * 4 == 48
add(T, "Graphs of motion", "Advanced", "numerical",
    "A particle starts from rest and moves along a straight line. Its acceleration–time graph shows a constant "
    "acceleration of +2 m/s² from t = 0 to t = 4 s, and a constant acceleration of −1 m/s² from t = 4 s to "
    "t = 8 s. The displacement of the particle in the first 8 s is:",
    place("40 m", ["48 m", "24 m", "32 m"], "A"),
    "Using an acceleration–time graph",
    "The area under the a–t graph gives the change in velocity. Find the velocity at the end of each stage and "
    "apply the equations of uniformly accelerated motion stage by stage.",
    ["0–4 s: v = 2 × 4 = 8 m/s, s₁ = ½ × 2 × 4² = 16 m",
     "4–8 s: v goes from 8 to 4 m/s, s₂ = 8 × 4 − ½ × 1 × 4² = 24 m",
     "Total = 16 + 24 = 40 m (the velocity stays positive throughout)"],
    why="48 m ignores the deceleration in the second stage. 24 m is the second stage alone. 32 m is 8 m/s × 4 s, "
        "the second stage at constant speed without the first stage.",
    seconds=90, recomputed=True)

truth = [True, True, False, True, False]
multi_key(truth, "abd")
add(T, "Vectors", "Advanced", "multi_statement",
    multi("Which of the following statements are correct?",
          ["For two non-zero vectors A and B, if |A + B| = |A − B|, then A is perpendicular to B.",
           "If the vector product of two non-zero vectors is the null vector, the two vectors are parallel or "
           "antiparallel.",
           "The scalar product of two unit vectors can be greater than 1.",
           "For any two vectors A and B, A · (A × B) = 0.",
           "Multiplying a vector by −2 doubles its magnitude and leaves its direction unchanged."]),
    place("(a), (b) and (d) only", ["(a), (b), (d) and (e) only", "(b), (c) and (d) only", "(a) and (d) only"],
          "D"),
    "Properties of scalar and vector products",
    "Squaring gives |A ± B|² = A² + B² ± 2A·B, so equal magnitudes need A·B = 0. |A × B| = AB sin θ vanishes only "
    "for θ = 0° or 180°. For unit vectors â·b̂ = cos θ ≤ 1. A × B is perpendicular to A, so its dot product with A "
    "is zero. Multiplying by a negative number reverses the direction.",
    ["(a) 2A·B = −2A·B → A·B = 0 → true", "(b) sin θ = 0 → θ = 0° or 180° → true",
     "(c) cos θ ≤ 1 → false", "(d) A × B ⊥ A → true", "(e) direction reversed → false"],
    why="Codes with (e) forget that a negative scalar reverses the direction; codes with (c) forget that cos θ "
        "never exceeds 1; (a) and (d) only leaves out the true statement (b).",
    ncert="Class 11 Physics, 'Motion in a Plane' and 'System of Particles and Rotational Motion' (vector "
          "product)", seconds=90)


# =====================================================================================================================
# Laws of Motion (B4 I5 A4)
# =====================================================================================================================
T = "Laws of Motion"

assert dmul(dims(1, 1, -2), dims(t=1)) == dmul(dims(m=1), dims(l=1, t=-1)) == (1, 1, -1)
add(T, "Newton's laws and impulse", "Basic", "direct",
    "Impulse has the same dimensions as:",
    place("Linear momentum", ["Force", "Work", "Power"], "B"),
    "Impulse and momentum",
    "Impulse is force × time, and by the impulse–momentum theorem it equals the change in linear momentum, so the "
    "two quantities have the same dimensions [M L T⁻¹] and the same SI unit (N s = kg m s⁻¹).",
    ["Impulse = F Δt → [M L T⁻²][T] = [M L T⁻¹]", "Momentum = mv → [M][L T⁻¹] = [M L T⁻¹]"],
    why="Force is [M L T⁻²], work is [M L² T⁻²] and power is [M L² T⁻³]; none of these equals [M L T⁻¹].",
    ncert="Class 11 Physics, 'Laws of Motion', impulse", seconds=25)

m_ = 5
dvx, dvy = 5 - 2, 4 - 0
J = m_ * math.hypot(dvx, dvy)
assert J == 25 and m_ * dvx == 15 and m_ * (dvx + dvy) == 35
add(T, "Newton's laws and impulse", "Basic", "numerical",
    "The velocity of a body of mass 5 kg changes from (2î) m/s to (5î + 4ĵ) m/s because of a force acting on it. "
    "The magnitude of the impulse of the force is:",
    place("25 N s", ["15 N s", "35 N s", "5 N s"], "C"),
    "Impulse as a vector change of momentum",
    "Impulse = Δp = m(v_final − v_initial). The change of velocity must be found as a vector before taking the "
    "magnitude.",
    ["Δv = (5 − 2)î + 4ĵ = 3î + 4ĵ m/s, |Δv| = 5 m/s", "|J| = 5 × 5 = 25 N s"],
    why="15 N s uses only the x-change. 35 N s adds the components (3 + 4) instead of combining them. 5 N s is "
        "|Δv| without the mass.",
    ncert="Class 11 Physics, 'Laws of Motion', Newton's second law and impulse", seconds=40, recomputed=True)

F1, F2 = (3, 4), (-1, 2)
F3 = (-(F1[0] + F2[0]), -(F1[1] + F2[1]))
assert F3 == (-2, -6)
add(T, "Equilibrium of concurrent forces", "Basic", "numerical",
    "Two concurrent forces F₁ = (3î + 4ĵ) N and F₂ = (−î + 2ĵ) N act on a particle. The third force that must act "
    "on the particle to keep it in equilibrium is:",
    place("(−2î − 6ĵ) N", ["(2î + 6ĵ) N", "(−4î − 2ĵ) N", "(4î + 2ĵ) N"], "D"),
    "Equilibrium of concurrent forces",
    "A particle is in equilibrium when the vector sum of all forces on it is zero, so the third force is the "
    "negative of the resultant of the other two.",
    ["F₁ + F₂ = 2î + 6ĵ N", "F₃ = −(F₁ + F₂) = −2î − 6ĵ N"],
    why="(2î + 6ĵ) N is the resultant itself, not the balancing force. (−4î − 2ĵ) N and (4î + 2ĵ) N come from "
        "subtracting the forces instead of adding them.",
    ncert="Class 11 Physics, 'Laws of Motion', equilibrium of a particle", seconds=40, recomputed=True)

add(T, "Newton's laws and impulse", "Basic", "assertion_reason",
    AR_STEM.format(
        a="A rocket can accelerate in outer space, where there is no air around it.",
        r="A rocket moves forward because its exhaust gases push against the surrounding air."),
    ar("C"),
    "Third law and rocket propulsion",
    "The rocket exerts a force on the exhaust gases to push them backward; by Newton's third law the gases exert "
    "an equal and opposite force on the rocket. No outside air is needed, so the rocket accelerates even in "
    "empty space. R gives the wrong mechanism.",
    ["Rocket pushes gases back ↔ gases push rocket forward (action–reaction pair)",
     "No air needed → A true", "Thrust is not due to pushing on air → R false"],
    why="R is a common misconception: if thrust came from pushing on air, rockets could not work in space.",
    ncert="Class 11 Physics, 'Laws of Motion', Newton's third law and conservation of momentum", seconds=40)

atwood = lambda m1, m2: abs(m2 - m1) * 10 / (m1 + m2)
table = lambda m_table, m_hang: m_hang * 10 / (m_table + m_hang)
assert atwood(2, 3) == 2 and table(3, 2) == 4 and table(1, 1) == 5 and atwood(1, 4) == 6
add(T, "Newton's laws and impulse", "Intermediate", "match_list",
    match_stem("Each arrangement uses a light inextensible string over a smooth light pulley, starts from rest, "
               "and g = 10 m/s². Match List-I (arrangement) with List-II (magnitude of the acceleration of the "
               "blocks).",
               ["Blocks of 2 kg and 3 kg hanging on the two sides of the pulley",
                "A 3 kg block on a smooth horizontal table, pulled by a 2 kg block hanging over the edge",
                "A 1 kg block on a smooth horizontal table, pulled by a 1 kg block hanging over the edge",
                "Blocks of 1 kg and 4 kg hanging on the two sides of the pulley"],
               ["5 m/s²", "2 m/s²", "6 m/s²", "4 m/s²"]),
    match_options({"A": "II", "B": "IV", "C": "I", "D": "III"},
                  [{"A": "IV", "B": "II", "C": "I", "D": "III"}, {"A": "II", "B": "IV", "C": "III", "D": "I"},
                   {"A": "II", "B": "I", "C": "IV", "D": "III"}], "B"),
    "Acceleration of connected bodies",
    "Treat the blocks and string as one system: the net driving force divided by the total mass gives the common "
    "acceleration. For two hanging blocks the driving force is the difference of their weights; for a block on a "
    "smooth table it is the weight of the hanging block.",
    ["A: (3 − 2) × 10/5 = 2 m/s² → II", "B: 2 × 10/5 = 4 m/s² → IV", "C: 1 × 10/2 = 5 m/s² → I",
     "D: (4 − 1) × 10/5 = 6 m/s² → III"],
    why="The wrong codes divide the driving force by the hanging mass alone, or use the sum of weights for the "
        "hanging pairs.",
    ncert="Class 11 Physics, 'Laws of Motion', Newton's second law (motion of connected bodies)", seconds=90)

a_max = 900 / 60 - 10
assert a_max == 5 and 900 / 60 == 15 and 900 / 60 + 10 == 25
add(T, "Newton's laws and impulse", "Intermediate", "numerical",
    "A rope hanging from a fixed support can bear a maximum tension of 900 N. A man of mass 60 kg climbs up the "
    "rope. Taking g = 10 m/s² and treating the rope as light, the maximum acceleration with which he can climb up "
    "without breaking the rope is:",
    place("5 m/s²", ["15 m/s²", "25 m/s²", "10 m/s²"], "A"),
    "Newton's second law for a climbing body",
    "The rope pulls the man up with tension T while gravity pulls him down. For upward acceleration a, "
    "T − mg = ma, so the tension needed grows with a.",
    ["T − mg = ma → a = T/m − g", "a_max = 900/60 − 10 = 15 − 10 = 5 m/s²"],
    why="15 m/s² ignores the man's weight. 25 m/s² adds g instead of subtracting it. 10 m/s² is simply g.",
    ncert="Class 11 Physics, 'Laws of Motion', Newton's second law", seconds=50, recomputed=True)

n2 = 45 * math.sqrt(4 / 9)
assert close(n2, 30) and close(45 * 4 / 9, 20) and close(45 * 9 / 4 / 1.5, 67.5)
add(T, "Friction", "Intermediate", "numerical",
    "A coin placed on a horizontal turntable at 4 cm from its axis just stays without slipping when the turntable "
    "rotates at 45 rpm. If the coin is placed at 9 cm from the axis, the maximum rate of rotation at which it will "
    "stay without slipping is:",
    place("30 rpm", ["20 rpm", "67.5 rpm", "45 rpm"], "D"),
    "Static friction providing the centripetal force",
    "The limiting static friction μmg supplies the centripetal force mω²r. At the limit ω²r = μg is the same at "
    "every radius, so ω ∝ 1/√r.",
    ["mω²r = μₛmg → ω ∝ 1/√r", "n₂ = 45 × √(4/9) = 45 × 2/3 = 30 rpm"],
    why="20 rpm takes ω ∝ 1/r. 67.5 rpm takes ω ∝ √r. 45 rpm forgets that the required centripetal force grows "
        "with r.",
    ncert="Class 11 Physics, 'Laws of Motion', static friction and circular motion", seconds=60, recomputed=True)

m_, u_ = 0.1, 20
vn = u_ * math.sin(math.radians(30))
J = 2 * m_ * vn
assert close(J, 2) and close(2 * m_ * u_ * math.cos(math.radians(30)), 2 * math.sqrt(3)) and 2 * m_ * u_ == 4
add(T, "Newton's laws and impulse", "Intermediate", "numerical",
    "A ball of mass 0.1 kg moving at 20 m/s strikes a smooth vertical wall, its velocity making an angle of 30° "
    "with the surface of the wall. It rebounds with the same speed, making the same angle with the wall. The "
    "magnitude of the impulse exerted by the wall on the ball is:",
    place("2 N s", ["2√3 N s", "4 N s", "Zero"], "C"),
    "Impulse in an oblique collision",
    "A smooth wall exerts only a normal force, so only the velocity component perpendicular to the wall is "
    "reversed; the component along the wall is unchanged. The impulse equals the change in the normal momentum.",
    ["Normal component = 20 sin 30° = 10 m/s (reversed)", "Along the wall: 20 cos 30° (unchanged)",
     "J = 2 × 0.1 × 10 = 2 N s, perpendicular to the wall"],
    why="2√3 N s uses the component along the wall (the angle is measured from the wall, not from the normal). "
        "4 N s treats the impact as head-on. Zero forgets that the normal component reverses.",
    ncert="Class 11 Physics, 'Laws of Motion', impulse", seconds=60, recomputed=True)

add(T, "Friction", "Intermediate", "statement_pair",
    SP_STEM.format(
        s1="Kinetic friction, like static friction, is found to be independent of the area of contact and nearly "
           "independent of the velocity of the body.",
        s2="Static friction does not exist by itself: when no applied force tends to cause relative motion "
           "between the surfaces, the static friction is zero."),
    sp("A"),
    "Laws of static and kinetic friction",
    "Experiments show that kinetic friction fₖ = μₖN depends on the normal reaction but is independent of the "
    "area of contact and nearly independent of speed. Static friction is self-adjusting: it opposes impending "
    "motion and is zero when nothing tends to produce relative motion.",
    ["Statement I: fₖ = μₖN, independent of area, nearly independent of velocity → true",
     "Statement II: no applied force → no impending motion → fₛ = 0 → true"],
    why="Both statements are NCERT's own description of friction.",
    ncert="Class 11 Physics, 'Laws of Motion', friction", seconds=45)

F_, m1, m2, mu = 30, 2, 3, 0.2
a_ = (F_ - mu * (m1 + m2) * 10) / (m1 + m2)
T_ = m1 * a_ + mu * m1 * 10
assert a_ == 4 and close(T_, 12) and close(T_, m1 / (m1 + m2) * F_) and m1 * a_ == 8
add(T, "Friction", "Advanced", "numerical",
    "Blocks of 2 kg and 3 kg lie on a rough horizontal floor, connected by a light horizontal string. A horizontal "
    "force of 30 N is applied to the 3 kg block, pulling it away from the 2 kg block, and both blocks slide. The "
    "coefficient of kinetic friction between each block and the floor is 0.2. Taking g = 10 m/s², the tension in "
    "the string is:",
    place("12 N", ["8 N", "18 N", "30 N"], "B"),
    "Connected bodies with friction",
    "First find the common acceleration of the whole system, then apply Newton's second law to the 2 kg block "
    "alone, which is pulled by the tension and held back by its own friction.",
    ["Friction on system = 0.2 × 50 = 10 N → a = (30 − 10)/5 = 4 m/s²",
     "2 kg block: T − 0.2 × 20 = 2 × 4 → T = 8 + 4 = 12 N"],
    shortcut="With the same μ for both blocks, friction cancels out: T = F × (2 kg)/(5 kg) = 30 × 2/5 = 12 N.",
    why="8 N forgets the friction on the 2 kg block. 18 N is the share of the 3 kg block. 30 N treats the string "
        "as transmitting the whole applied force.",
    ncert="Class 11 Physics, 'Laws of Motion', friction and motion of connected bodies", seconds=90,
    recomputed=True)

M_man, M_boat, L_ = 60, 40, 4
d_boat = M_man * L_ / (M_man + M_boat)
assert close(d_boat, 2.4) and close(L_ - d_boat, 1.6) and M_man * L_ / M_boat == 6
add(T, "Conservation of linear momentum", "Advanced", "numerical",
    "A man of mass 60 kg stands at one end of a boat of mass 40 kg and length 4 m. The boat floats at rest on "
    "still water. The man walks to the other end of the boat. Neglecting the resistance of the water, the distance "
    "through which the boat moves is:",
    place("2.4 m", ["1.6 m", "6 m", "4 m"], "D"),
    "Conservation of momentum (centre of mass at rest)",
    "No horizontal external force acts on the man–boat system, which starts at rest, so its total momentum stays "
    "zero and its centre of mass does not move. The man moves forward relative to the ground by (L − d) while the "
    "boat moves back by d.",
    ["60(4 − d) = 40d", "240 = 100d → d = 2.4 m (opposite to the man's walk)"],
    why="1.6 m is how far the man moves relative to the ground. 6 m uses 60 × 4/40, ignoring that the man's "
        "ground displacement is less than 4 m. 4 m is the length of the boat.",
    ncert="Class 11 Physics, 'Laws of Motion', conservation of momentum", seconds=80, recomputed=True)

rate, v_belt = 2, 3
assert rate * v_belt == 6 and rate * v_belt / 2 == 3 and rate * 10 == 20
add(T, "Newton's laws and impulse", "Advanced", "numerical",
    "Sand falls vertically, at a steady rate of 2 kg/s, onto a horizontal conveyor belt that moves with a constant "
    "velocity of 3 m/s. Neglecting friction in the belt's mechanism, the extra horizontal force needed to keep the "
    "belt moving with constant velocity is:",
    place("6 N", ["3 N", "20 N", "Zero, since the belt moves with constant velocity"], "A"),
    "Force as the rate of change of momentum",
    "Sand arrives with no horizontal velocity and is quickly brought to the belt's speed. Every second the belt "
    "must give horizontal momentum (dm/dt) × v to the new sand, and by Newton's second law this needs a force "
    "F = (dm/dt) v.",
    ["F = (dm/dt) × v = 2 × 3 = 6 N"],
    why="3 N halves the result by confusing it with the rate of gain of kinetic energy. 20 N is the weight of the "
        "sand arriving per second, which is vertical. The belt's velocity is constant, but the moving mass grows, "
        "so momentum still increases.",
    ncert="Class 11 Physics, 'Laws of Motion', Newton's second law (F = dp/dt)", seconds=60, recomputed=True)

truth = [False, True, False, True, True]
multi_key(truth, "bde")
add(T, "Newton's laws and impulse", "Advanced", "multi_statement",
    multi("A book rests on a table, and the table stands on the floor. Which of the following statements are "
          "correct?",
          ["The weight of the book and the normal force exerted by the table on the book form an action–reaction "
           "pair.",
           "The normal force exerted by the table on the book and the normal force exerted by the book on the "
           "table form an action–reaction pair.",
           "The normal force exerted by the floor on the table is equal to the weight of the table alone.",
           "The net force on the book is zero.",
           "Action and reaction forces act at the same instant."]),
    place("(b), (d) and (e) only", ["(a), (b) and (d) only", "(b), (c), (d) and (e) only", "(a), (c) and (e) only"],
          "C"),
    "Third-law pairs and equilibrium",
    "An action–reaction pair consists of two forces of the same kind acting on two different bodies. The weight of "
    "the book and the table's push on it both act on the book; they balance because the book is in equilibrium, "
    "not because of the third law. The floor supports the table and the book on it. NCERT notes that action and "
    "reaction are simultaneous.",
    ["(a) both forces act on the book → not a pair → false", "(b) table on book ↔ book on table → true",
     "(c) floor pushes with (weight of table + weight of book) → false", "(d) book at rest → true",
     "(e) action and reaction are simultaneous → true"],
    why="Codes with (a) confuse balanced forces with a third-law pair; codes with (c) forget the book's weight "
        "transmitted through the table.",
    ncert="Class 11 Physics, 'Laws of Motion', Newton's third law", seconds=80)


# =====================================================================================================================
# Work, Energy and Power (B3 I4 A3)
# =====================================================================================================================
T = "Work, Energy and Power"

eV, MeV = 1.6e-19, 1.6e-13
assert close(MeV / eV, 1e6)
add(T, "Work-energy theorem", "Basic", "match_list",
    match_stem("Match List-I (unit of energy) with List-II (its value in joules).",
               ["1 electron volt (eV)", "1 erg", "1 calorie", "1 MeV"],
               ["10⁻⁷ J", "1.6 × 10⁻¹³ J", "4.186 J", "1.6 × 10⁻¹⁹ J"]),
    match_options({"A": "IV", "B": "I", "C": "III", "D": "II"},
                  [{"A": "II", "B": "I", "C": "III", "D": "IV"}, {"A": "IV", "B": "III", "C": "I", "D": "II"},
                   {"A": "I", "B": "IV", "C": "III", "D": "II"}], "D"),
    "Alternative units of work and energy",
    "1 eV is the energy gained by a charge e falling through 1 V; 1 MeV = 10⁶ eV. The erg is the CGS unit "
    "(1 g cm² s⁻²), and the calorie is the heat that raises 1 g of water by 1 °C (from 14.5 °C to 15.5 °C).",
    ["1 eV = 1.6 × 10⁻¹⁹ J → IV", "1 erg = 10⁻⁷ J → I", "1 cal = 4.186 J → III",
     "1 MeV = 10⁶ × 1.6 × 10⁻¹⁹ = 1.6 × 10⁻¹³ J → II"],
    why="The wrong codes swap eV with MeV (a factor of 10⁶) or the erg with the calorie.",
    ncert="Class 11 Physics, 'Work, Energy and Power', alternative units of work/energy (table)", seconds=40)

add(T, "Work by constant and variable force", "Basic", "direct",
    "A constant force F acts on a body while the body undergoes a displacement d. The work done by the force is "
    "negative when the angle θ between F and d satisfies:",
    place("90° < θ ≤ 180°", ["0° ≤ θ < 90°", "θ = 90°", "θ = 0° only"], "A"),
    "Sign of the work done by a constant force",
    "W = F d cos θ. Since F and d are magnitudes, the sign of W is the sign of cos θ, which is negative for angles "
    "greater than 90° and up to 180°.",
    ["cos θ > 0 for 0° ≤ θ < 90° → W positive", "cos 90° = 0 → W zero",
     "cos θ < 0 for 90° < θ ≤ 180° → W negative"],
    why="0° ≤ θ < 90° gives positive work; θ = 90° gives zero work; θ = 0° gives the largest positive work.",
    ncert="Class 11 Physics, 'Work, Energy and Power', work", seconds=25)

Fv = (2, 3)
vv = (4, -1)
P_ = Fv[0] * vv[0] + Fv[1] * vv[1]
assert P_ == 5 and 8 + 3 == 11
add(T, "Power", "Basic", "numerical",
    "A force F = (2î + 3ĵ) N acts on a particle that is moving with a velocity v = (4î − ĵ) m/s. The instantaneous "
    "power delivered by the force is:",
    place("5 W", ["11 W", "8 W", "√221 W"], "B"),
    "Instantaneous power P = F · v",
    "Power is the scalar product of the force and the velocity, so only the components along the same axes "
    "multiply, with their signs.",
    ["P = (2)(4) + (3)(−1) = 8 − 3 = 5 W"],
    why="11 W ignores the minus sign of the y-component of velocity. 8 W keeps only the x-terms. √221 W multiplies "
        "the magnitudes √13 × √17, which would need F and v to be parallel.",
    ncert="Class 11 Physics, 'Work, Energy and Power', power", seconds=35, recomputed=True)

U = lambda x: 2 * x ** 2 - 8 * x + 3
Fx = lambda x: -(4 * x - 8)
assert Fx(2) == 0 and U(2) < U(1.9) and U(2) < U(2.1)
add(T, "Work by constant and variable force", "Intermediate", "numerical",
    "A particle moving along the x-axis is acted on by a conservative force whose potential energy is "
    "U(x) = 2x² − 8x + 3, where U is in joules and x in metres. The position of equilibrium of the particle and "
    "the nature of the equilibrium are:",
    place("x = 2 m; stable", ["x = 2 m; unstable", "x = 4 m; stable", "x = 0; neutral"], "C"),
    "Force from potential energy, and stability",
    "For a conservative force F(x) = −dU/dx. Equilibrium is where F = 0. If U is a minimum there, a small "
    "displacement produces a force back towards the equilibrium point, so it is stable.",
    ["F = −dU/dx = −(4x − 8)", "F = 0 → x = 2 m", "d²U/dx² = 4 > 0 → U is a minimum → stable"],
    why="'Unstable' would need U to be a maximum. x = 4 m is where U returns to its value at x = 0, not where the "
        "force vanishes. x = 0 has F = 8 N ≠ 0.",
    ncert="Class 11 Physics, 'Work, Energy and Power', the concept of potential energy (F = −dV/dx)", seconds=60,
    recomputed=True)

L_, vb = 1.0, math.sqrt(10)
h_ = vb ** 2 / (2 * 10)
th = math.degrees(math.acos(1 - h_ / L_))
assert close(h_, 0.5) and close(th, 60) and h_ < L_
add(T, "Motion in a vertical circle", "Intermediate", "numerical",
    "The bob of a simple pendulum of length 1 m hangs at rest. It is given a horizontal speed of √10 m/s. Taking "
    "g = 10 m/s² and neglecting air resistance, the angle that the string makes with the vertical when the bob "
    "first comes momentarily to rest is:",
    place("60°", ["30°", "90°", "45°"], "D"),
    "Energy conservation in motion along a vertical circle",
    "The tension is always perpendicular to the bob's velocity and does no work, so the bob's kinetic energy "
    "turns into gravitational potential energy. The bob rises h = v²/2g, which is less than L, so the string stays "
    "taut and the bob stops at height h on the circle.",
    ["h = v²/(2g) = 10/20 = 0.5 m", "h = L(1 − cos θ) → cos θ = 1 − 0.5 = 0.5", "θ = 60°"],
    why="30° takes sin θ = 0.5. 90° would need h = L = 1 m. 45° does not follow from h = 0.5 m.",
    ncert="Class 11 Physics, 'Work, Energy and Power', conservation of mechanical energy and motion in a vertical "
          "circle", seconds=60, recomputed=True)

m1, m2, u1 = 3, 1, 4
v1 = (m1 - m2) / (m1 + m2) * u1
v2 = 2 * m1 / (m1 + m2) * u1
assert v1 == 2 and v2 == 6 and m1 * u1 == m1 * v1 + m2 * v2 and close(0.5 * m1 * u1 ** 2, 0.5 * m1 * v1 ** 2 + 0.5 * m2 * v2 ** 2)
assert m1 * 1 + m2 * 9 == 12 and 0.5 * m1 * 1 + 0.5 * m2 * 81 != 24
add(T, "Collisions", "Intermediate", "numerical",
    "A ball of mass 3 kg moving at 4 m/s collides head-on and elastically with a ball of mass 1 kg at rest. The "
    "velocities of the 3 kg ball and the 1 kg ball just after the collision are respectively:",
    place("2 m/s and 6 m/s, both forward", ["0 and 4 m/s, forward", "3 m/s and 3 m/s, both forward",
          "1 m/s and 9 m/s, both forward"], "A"),
    "One-dimensional elastic collision",
    "In a head-on elastic collision with the second body at rest, v₁ = (m₁ − m₂)u₁/(m₁ + m₂) and "
    "v₂ = 2m₁u₁/(m₁ + m₂). Both momentum and kinetic energy are conserved.",
    ["v₁ = (3 − 1)/4 × 4 = 2 m/s", "v₂ = 2 × 3/4 × 4 = 6 m/s",
     "Check: momentum 12 = 3 × 2 + 1 × 6; KE 24 J = 6 + 18 J"],
    why="0 and 4 m/s is the exchange of velocities, true only for equal masses. 3 m/s each is a perfectly "
        "inelastic collision. 1 m/s and 9 m/s conserves momentum but gives KE 42 J, more than the initial 24 J.",
    ncert="Class 11 Physics, 'Work, Energy and Power', collisions in one dimension", seconds=60, recomputed=True)

add(T, "Work-energy theorem", "Intermediate", "statement_pair",
    SP_STEM.format(
        s1="A body released from rest at the top of a fixed smooth curved track reaches the bottom with a speed "
           "that depends on the shape of the track, and not only on the vertical height of the drop.",
        s2="The normal reaction exerted by a fixed smooth track on a body sliding along it does no work on the "
           "body."),
    sp("D"),
    "Work–energy theorem on a smooth track",
    "On a fixed smooth track only gravity and the normal reaction act. The normal reaction is perpendicular to the "
    "velocity at every instant, so it does no work. Gravity's work is mgh, independent of the path. Hence "
    "½mv² = mgh and v = √(2gh) depends only on the height h.",
    ["Normal reaction ⊥ velocity → W_N = 0 → Statement II true",
     "½mv² = mgh → v = √(2gh), independent of shape → Statement I false"],
    why="The shape changes how long the body takes, not the speed it reaches at a given depth.",
    ncert="Class 11 Physics, 'Work, Energy and Power', work–energy theorem and conservation of mechanical energy",
    seconds=50)

m_car, v_car, R_res, sin_t = 1000, 10, 500, 1 / 20
F_eng = R_res + m_car * 10 * sin_t
assert F_eng == 1000 and F_eng * v_car == 10_000 and R_res * v_car == 5000
add(T, "Power", "Advanced", "numerical",
    "A car of mass 1000 kg moves up a straight road inclined at an angle θ to the horizontal, where sin θ = 1/20, "
    "with a constant speed of 10 m/s. The resistive forces on it total 500 N. Taking g = 10 m/s², the power "
    "delivered by the engine is:",
    place("10 kW", ["5 kW", "15 kW", "105 kW"], "C"),
    "Power at constant speed on an incline",
    "At constant speed the net force is zero, so the engine's driving force balances the resistance plus the "
    "component of the weight along the slope. The power is this force times the speed.",
    ["mg sin θ = 1000 × 10 × 1/20 = 500 N", "Driving force = 500 + 500 = 1000 N",
     "P = 1000 × 10 = 10 000 W = 10 kW"],
    why="5 kW ignores the slope. 15 kW counts the weight component twice. 105 kW uses the whole weight mg instead "
        "of its component along the slope.",
    ncert="Class 11 Physics, 'Work, Energy and Power', power", seconds=70, recomputed=True)

mb, ub, M_, k_ = 0.02, 200, 1.98, 400
V_ = mb * ub / (mb + M_)
x_c = V_ * math.sqrt((mb + M_) / k_)
assert close(V_, 2) and close(x_c, 0.1 * math.sqrt(2)) and close(math.sqrt(2 * 0.5 * mb * ub ** 2 / k_), math.sqrt(2))
add(T, "Collisions", "Advanced", "numerical",
    "A bullet of mass 20 g moving horizontally at 200 m/s strikes a wooden block of mass 1.98 kg and gets embedded "
    "in it. The block rests on a smooth horizontal surface and is attached to one end of a light horizontal "
    "spring of spring constant 400 N/m whose other end is fixed to a wall. The maximum compression of the spring "
    "is:",
    place("10√2 cm", ["100√2 cm", "10 cm", "20√2 cm"], "B"),
    "Perfectly inelastic collision followed by conservation of energy",
    "During the very short impact the spring has no time to compress, so momentum is conserved but kinetic energy "
    "is not. After the impact, the block and bullet compress the spring and their kinetic energy turns into "
    "spring potential energy.",
    ["Common speed V = (0.02 × 200)/2 = 2 m/s", "KE after impact = ½ × 2 × 2² = 4 J",
     "½ × 400 × x² = 4 → x² = 0.02 → x = 0.1√2 m = 10√2 cm ≈ 14 cm"],
    why="100√2 cm assumes the bullet's whole KE (400 J) is stored in the spring, ignoring the loss in the "
        "inelastic impact. 10 cm drops the ½ on one side of the energy equation. 20√2 cm doubles the common speed.",
    ncert="Class 11 Physics, 'Work, Energy and Power', collisions and the potential energy of a spring",
    seconds=100, recomputed=True)

truth = [True, True, True, False, False]
multi_key(truth, "abc")
add(T, "Work-energy theorem", "Advanced", "multi_statement",
    multi("A ball is thrown vertically upward and later returns to the thrower's hand. Air resistance on the ball "
          "is NOT negligible. Which of the following statements are correct?",
          ["The ball takes less time to rise than to fall back.",
           "The ball returns to the hand with a smaller speed than the speed with which it was thrown.",
           "The work done by gravity on the ball over the whole up-and-down trip is zero.",
           "The work done by air resistance on the ball over the whole trip is zero.",
           "At the highest point, the mechanical energy of the ball equals the kinetic energy with which it was "
           "thrown."]),
    place("(a), (b) and (c) only", ["(b), (c) and (d) only", "(a), (b) and (e) only", "(b) and (c) only"], "D"),
    "Conservative and non-conservative forces in vertical motion",
    "Going up, gravity and drag both act downward, so the retardation exceeds g; coming down, drag opposes "
    "gravity, so the acceleration is less than g. Over the same height, the rise is therefore quicker. Gravity is "
    "conservative, so its work over a closed path is zero. Drag always opposes motion and does negative work both "
    "ways, so the ball loses mechanical energy throughout.",
    ["(a) a_up > g > a_down over the same distance → t_up < t_down → true",
     "(b) W_drag < 0 → KE on return < initial KE → true",
     "(c) gravity conservative, closed path → W = 0 → true",
     "(d) drag does negative work on both legs → false",
     "(e) energy already lost to drag on the way up → false"],
    why="Codes with (d) treat air resistance as conservative; codes with (e) ignore the energy lost on the way up; "
        "(b) and (c) only misses the true statement (a).",
    ncert="Class 11 Physics, 'Work, Energy and Power', conservative forces and the work–energy theorem",
    seconds=90)


# =====================================================================================================================
# Rotational Motion (B4 I5 A4)
# =====================================================================================================================
T = "Rotational Motion"

v_cm = (2 * 3 + 3 * (-2)) / 5
assert v_cm == 0 and (2 * 3 + 3 * 2) / 5 == 2.4
add(T, "Centre of mass", "Basic", "numerical",
    "A body of mass 2 kg moves due east at 3 m/s, and a body of mass 3 kg moves due west at 2 m/s. The velocity of "
    "the centre of mass of the two-body system is:",
    place("Zero", ["2.4 m/s, towards the east", "2.5 m/s, towards the west", "1.2 m/s, towards the east"], "B"),
    "Velocity of the centre of mass",
    "V_cm = (m₁v₁ + m₂v₂)/(m₁ + m₂), with the velocities taken with their signs. Equivalently, V_cm is the total "
    "momentum divided by the total mass.",
    ["Take east as positive: m₁v₁ = 2 × 3 = +6, m₂v₂ = 3 × (−2) = −6 kg m/s",
     "V_cm = (6 − 6)/5 = 0"],
    why="2.4 m/s adds the momenta as if both moved east. 2.5 m/s averages the speeds. 1.2 m/s keeps only the "
        "first body's momentum (6/5).",
    ncert="Class 11 Physics, 'System of Particles and Rotational Motion', motion of centre of mass", seconds=35,
    recomputed=True)

w0 = 1200 / 60
revs = 0.5 * w0 * 20
assert revs == 200 and w0 * 20 == 400
add(T, "Rigid-body rotation", "Basic", "numerical",
    "A flywheel rotating at 1200 revolutions per minute is brought to rest with a uniform angular retardation in "
    "20 s. The number of revolutions it makes in this time is:",
    place("200", ["400", "24 000", "100"], "D"),
    "Equations of rotational motion with uniform angular acceleration",
    "With uniform retardation the average angular speed is half the initial one, and the angle turned equals the "
    "average angular speed times the time (the rotational analogue of s = (u + v)t/2).",
    ["ω₀ = 1200 rpm = 20 rev/s", "θ = ½(ω₀ + 0)t = ½ × 20 × 20 = 200 revolutions"],
    why="400 uses the initial speed for the whole time. 24 000 multiplies revolutions per minute by seconds. 100 "
        "halves the result twice.",
    ncert="Class 11 Physics, 'System of Particles and Rotational Motion', kinematics of rotational motion about a "
          "fixed axis", seconds=40, recomputed=True)

add(T, "Moment of inertia and axis theorems", "Basic", "direct",
    "The radius of gyration of a thin uniform ring of radius R about the axis passing through its centre and "
    "perpendicular to its plane is:",
    place("R", ["R/√2", "R/2", "√2 R"], "C"),
    "Radius of gyration",
    "The radius of gyration k is defined by I = Mk². For a thin ring about its central perpendicular axis every "
    "particle is at distance R from the axis, so I = MR² and k = R.",
    ["I = MR² = Mk² → k = R"],
    why="R/√2 is the radius of gyration of the ring about a diameter (I = MR²/2), or of a disc about its central "
        "axis. R/2 and √2 R do not correspond to I = MR².",
    ncert="Class 11 Physics, 'System of Particles and Rotational Motion', moment of inertia and radius of gyration",
    seconds=30)

add(T, "Centre of mass", "Basic", "statement_pair",
    SP_STEM.format(
        s1="The centre of mass of a thin uniform rod lies at its midpoint.",
        s2="Since the coordinates of the centre of mass depend on the choice of origin, the centre of mass of a "
           "rigid body lies at different points of the body for different choices of origin."),
    sp("C"),
    "Centre of mass is a property of the body",
    "By symmetry, every element of a uniform rod on one side of the midpoint is matched by an equal element on the "
    "other side, so the centre of mass is the midpoint. Shifting the origin changes the coordinates of every "
    "particle and of the centre of mass by the same amount, so the centre of mass stays at the same physical point "
    "of the body.",
    ["Statement I: symmetry → midpoint → true",
     "Statement II: coordinates change, the physical point does not → false"],
    why="Statement II confuses the coordinates of a point with the point itself.",
    ncert="Class 11 Physics, 'System of Particles and Rotational Motion', centre of mass", seconds=40)

M_, L_, d_ = 2, 3, 1.0
I_c = M_ * L_ ** 2 / 12
I_p = I_c + M_ * d_ ** 2
assert close(I_c, 1.5) and close(I_p, 3.5) and close(M_ * L_ ** 2 / 3, 6)
add(T, "Moment of inertia and axis theorems", "Intermediate", "numerical",
    "A thin uniform rod of mass 2 kg and length 3 m rotates about an axis perpendicular to it and passing through "
    "a point on the rod 0.5 m from one end. Its moment of inertia about this axis is:",
    place("3.5 kg m²", ["1.5 kg m²", "6.0 kg m²", "2.0 kg m²"], "B"),
    "Theorem of parallel axes",
    "I = I_cm + Md², where d is the distance between the given axis and the parallel axis through the centre of "
    "mass. The centre is 1.5 m from each end, so the axis 0.5 m from an end is d = 1.0 m from the centre.",
    ["I_cm = ML²/12 = 2 × 9/12 = 1.5 kg m²", "d = 1.5 − 0.5 = 1.0 m",
     "I = 1.5 + 2 × 1.0² = 3.5 kg m²"],
    why="1.5 kg m² is the value about the centre. 6.0 kg m² is the value about an end (ML²/3). 2.0 kg m² is only "
        "the Md² term.",
    ncert="Class 11 Physics, 'System of Particles and Rotational Motion', theorem of parallel axes", seconds=50,
    recomputed=True)

I1 = 4 * 0.5 ** 2
I2 = I1 + 2 * 1 * 0.5 ** 2
w2 = I1 * 30 / I2
assert close(I1, 1) and close(I2, 1.5) and close(w2, 20) and close(I1 * 30 / (I1 + 2 * 0.5), 15)
add(T, "Torque and angular momentum", "Intermediate", "numerical",
    "A thin ring of mass 4 kg and radius 0.5 m rotates freely in a horizontal plane about a fixed vertical axis "
    "through its centre, at 30 rad/s. Two small particles, each of mass 1 kg, are gently attached to the ring at "
    "the two ends of a diameter. Neglecting friction, the new angular speed of the ring is:",
    place("20 rad/s", ["15 rad/s", "45 rad/s", "30 rad/s"], "D"),
    "Conservation of angular momentum",
    "No external torque acts about the axis, so Iω stays constant. Attaching the particles at the rim increases "
    "the moment of inertia, so ω decreases.",
    ["I₁ = MR² = 4 × 0.25 = 1 kg m²", "I₂ = 1 + 2 × 1 × 0.25 = 1.5 kg m²",
     "ω₂ = I₁ω₁/I₂ = 1 × 30/1.5 = 20 rad/s"],
    why="15 rad/s takes each particle's moment of inertia as mR instead of mR². 45 rad/s inverts the ratio. "
        "30 rad/s ignores the added moment of inertia.",
    ncert="Class 11 Physics, 'System of Particles and Rotational Motion', conservation of angular momentum",
    seconds=60, recomputed=True)

m_scale, pivot, cm_scale, at = 150, 40, 50, 10
m_need = m_scale * (cm_scale - pivot) / (pivot - at)
assert m_need == 50
add(T, "Equilibrium of rigid bodies", "Intermediate", "numerical",
    "A uniform metre scale of mass 150 g is balanced horizontally on a knife edge placed at its 40 cm mark, with a "
    "small body hung at its 10 cm mark. The mass of the body is:",
    place("50 g", ["150 g", "450 g", "75 g"], "B"),
    "Rotational equilibrium (principle of moments)",
    "The weight of a uniform scale acts at its centre of mass, the 50 cm mark. For balance, the clockwise and "
    "anticlockwise moments about the knife edge must be equal.",
    ["Scale's weight acts 50 − 40 = 10 cm from the pivot", "Body hangs 40 − 10 = 30 cm from the pivot",
     "m × 30 = 150 × 10 → m = 50 g"],
    why="150 g assumes equal arms. 450 g inverts the ratio of the arms. 75 g takes the scale's lever arm as 15 cm.",
    ncert="Class 11 Physics, 'System of Particles and Rotational Motion', equilibrium of a rigid body (principle of "
          "moments)", seconds=50, recomputed=True)

Lm, Ia, Ib = 12.0, 6.0, 4.0
assert Lm ** 2 / (2 * Ib) > Lm ** 2 / (2 * Ia)
add(T, "Torque and angular momentum", "Intermediate", "assertion_reason",
    AR_STEM.format(
        a="When a skater spinning freely on smooth ice pulls her arms in, her rotational kinetic energy increases.",
        r="Her angular momentum L about the vertical axis stays constant, and the rotational kinetic energy can be "
          "written as L²/(2I)."),
    ar("A"),
    "Kinetic energy at constant angular momentum",
    "With no external torque about the axis, L = Iω is conserved. Writing K = ½Iω² = L²/(2I) shows that a smaller "
    "moment of inertia at the same L means a larger kinetic energy. The extra energy comes from the work her "
    "muscles do in pulling her arms in.",
    ["L constant, I decreases", "K = L²/(2I) → K increases"],
    why="R gives exactly the relation from which A follows, so it is the correct explanation.",
    ncert="Class 11 Physics, 'System of Particles and Rotational Motion', conservation of angular momentum and "
          "kinetic energy of rotation", seconds=50)

assert F(1, 12) + F(1, 4) == F(1, 3) and F(1, 12) + F(1, 16) == F(7, 48)
add(T, "Moment of inertia and axis theorems", "Intermediate", "match_list",
    match_stem("A thin uniform rod has mass M and length L. Match List-I (axis) with List-II (moment of inertia "
               "of the rod about that axis).",
               ["Perpendicular to the rod, through its centre",
                "Perpendicular to the rod, through one end",
                "Perpendicular to the rod, through a point at a distance L/4 from its centre",
                "Parallel to the rod, at a distance L from it"],
               ["ML²/3", "7ML²/48", "ML²", "ML²/12"]),
    match_options({"A": "IV", "B": "I", "C": "II", "D": "III"},
                  [{"A": "IV", "B": "II", "C": "I", "D": "III"}, {"A": "I", "B": "IV", "C": "II", "D": "III"},
                   {"A": "IV", "B": "I", "C": "III", "D": "II"}], "C"),
    "Moment of inertia of a rod and the parallel-axis theorem",
    "Start from ML²/12 about the central perpendicular axis and use I = I_cm + Md² for parallel axes. For an axis "
    "parallel to a thin rod, every element is at the same distance from the axis.",
    ["A: ML²/12 → IV", "B: ML²/12 + M(L/2)² = ML²/3 → I",
     "C: ML²/12 + M(L/4)² = 4ML²/48 + 3ML²/48 = 7ML²/48 → II", "D: every element at distance L → ML² → III"],
    why="The wrong codes swap the end and the L/4 values, or apply the parallel-axis shift to the axis parallel to "
        "the rod.",
    ncert="Class 11 Physics, 'System of Particles and Rotational Motion', moments of inertia and the theorem of "
          "parallel axes", seconds=80)

r_ = (1, 2, -1)
Fo = (3, 1, 2)
cross = lambda a, b: (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])
assert cross(r_, Fo) == (5, -5, -5) and cross(Fo, r_) == (-5, 5, 5)
add(T, "Torque and angular momentum", "Advanced", "numerical",
    "A force F = (3î + ĵ + 2k̂) N acts at a point whose position vector with respect to the origin is "
    "r = (î + 2ĵ − k̂) m. The torque of the force about the origin is:",
    place("(5î − 5ĵ − 5k̂) N m", ["(−5î + 5ĵ + 5k̂) N m", "(5î + 5ĵ − 5k̂) N m", "(3î + 2ĵ − 2k̂) N m"], "A"),
    "Torque as the vector product r × F",
    "τ = r × F, evaluated with the determinant of î, ĵ, k̂ over the components of r (second row) and F (third "
    "row). The order matters: F × r = −(r × F).",
    ["τₓ = (2)(2) − (−1)(1) = 5", "τᵧ = (−1)(3) − (1)(2) = −5", "τ_z = (1)(1) − (2)(3) = −5",
     "τ = 5î − 5ĵ − 5k̂ N m (magnitude 5√3 N m)"],
    why="(−5î + 5ĵ + 5k̂) is F × r. (5î + 5ĵ − 5k̂) misses the minus sign of the ĵ term. (3î + 2ĵ − 2k̂) "
        "multiplies matching components, which is not a vector product.",
    ncert="Class 11 Physics, 'System of Particles and Rotational Motion', torque and the vector product",
    seconds=80, recomputed=True)

m_, u_, th_ = 0.2, 20, 45
ux = u_ * math.cos(math.radians(th_))
H_ = (u_ * math.sin(math.radians(th_))) ** 2 / 20
Lp = m_ * ux * H_
assert close(H_, 10) and close(Lp, 20 * math.sqrt(2)) and close(m_ * u_ * H_, 40)
add(T, "Torque and angular momentum", "Advanced", "numerical",
    "A particle of mass 0.2 kg is projected from a point O on level ground with a speed of 20 m/s at 45° above the "
    "horizontal. Taking g = 10 m/s² and neglecting air resistance, the magnitude of its angular momentum about O "
    "when it is at the highest point of its path is:",
    place("20√2 kg m² s⁻¹", ["40√2 kg m² s⁻¹", "40 kg m² s⁻¹", "Zero"], "B"),
    "Angular momentum of a particle about a point",
    "L = r × p. At the highest point the velocity is horizontal (u cos θ), so the moment arm of the momentum about "
    "O is the vertical height H of that point above the line of motion through O.",
    ["H = u² sin² θ/(2g) = 400 × ½/20 = 10 m", "v at top = u cos 45° = 10√2 m/s",
     "L = m v H = 0.2 × 10√2 × 10 = 20√2 kg m² s⁻¹ (perpendicular to the plane of motion)"],
    why="40 kg m² s⁻¹ uses the launch speed u instead of the horizontal velocity. 40√2 doubles the height. Zero "
        "would need the momentum to point along the line joining O to the particle.",
    ncert="Class 11 Physics, 'System of Particles and Rotational Motion', angular momentum of a particle",
    seconds=90, recomputed=True)

W_ = 100
T_ = W_ * 0.5 / math.sin(math.radians(30))
assert close(T_, 100) and close(W_ * 0.5 / math.cos(math.radians(30)), 100 / math.sqrt(3))
add(T, "Equilibrium of rigid bodies", "Advanced", "numerical",
    "A uniform rod of weight 100 N is hinged at one end to a vertical wall and is held horizontal by a light string "
    "tied to its other end. The string goes up to a point on the wall above the hinge and makes an angle of 30° "
    "with the rod. The tension in the string is:",
    place("100 N", ["50 N", "200 N", "100/√3 N"], "D"),
    "Rotational equilibrium with a hinge",
    "Take moments about the hinge, so that the unknown hinge force has no moment. The weight acts at the middle of "
    "the rod; only the component of the tension perpendicular to the rod (T sin 30°) has a moment about the hinge.",
    ["Moment of weight = 100 × L/2", "Moment of tension = T sin 30° × L",
     "T × ½ × L = 50L → T = 100 N"],
    why="50 N ignores the angle of the string. 200 N puts the weight at the far end. 100/√3 N uses cos 30°, the "
        "component along the rod, which has no moment about the hinge.",
    ncert="Class 11 Physics, 'System of Particles and Rotational Motion', equilibrium of a rigid body", seconds=80,
    recomputed=True)

truth = [True, True, False, False, True]
multi_key(truth, "abe")
add(T, "Equilibrium of rigid bodies", "Advanced", "multi_statement",
    multi("Which of the following statements are correct?",
          ["The moment of a couple about any point is the same, whatever point is chosen.",
           "If the net external force on a rigid body is zero and the net torque about one point is zero, the net "
           "torque about every other point is also zero.",
           "The centre of gravity of an extended body always coincides with its centre of mass, however large the "
           "body is compared with the Earth.",
           "The total angular momentum of a system of particles can be changed by internal forces alone.",
           "The torque of a force about an axis parallel to the line of action of the force is zero."]),
    place("(a), (b) and (e) only", ["(a), (b), (c) and (e) only", "(b), (d) and (e) only", "(a) and (c) only"],
          "C"),
    "Couples, equilibrium and angular momentum",
    "A couple has zero resultant force, so its moment does not depend on the reference point. Similarly, when the "
    "net force is zero, the net torque is the same about every point. The centre of gravity coincides with the "
    "centre of mass only where g is uniform over the body. Internal forces occur in third-law pairs along the same "
    "line, so their torques cancel. r × F has no component along a direction parallel to F.",
    ["(a) true", "(b) τ_P = τ_O − (OP) × F_net → equal when F_net = 0 → true",
     "(c) needs uniform g → false for very large bodies", "(d) internal torques cancel → false",
     "(e) (r × F) · n̂ = 0 when F ∥ n̂ → true"],
    why="Codes with (c) forget that CG = CM only in a uniform field; codes with (d) contradict the conservation of "
        "angular momentum; (a) and (c) only drops two true statements.",
    ncert="Class 11 Physics, 'System of Particles and Rotational Motion', equilibrium of a rigid body, couple and "
          "centre of gravity", seconds=90)


# =====================================================================================================================
# Gravitation (B3 I4 A2)
# =====================================================================================================================
T = "Gravitation"

G = 6.67e-11
U_ = -G * 10 * 10 / 1
assert close(U_, -6.67e-9)
add(T, "Gravitational potential and energy", "Basic", "numerical",
    "Two point masses, each of 10 kg, are 1 m apart. Taking G = 6.67 × 10⁻¹¹ N m² kg⁻² and the potential energy "
    "to be zero at infinite separation, the gravitational potential energy of the pair is:",
    place("−6.67 × 10⁻⁹ J", ["+6.67 × 10⁻⁹ J", "−6.67 × 10⁻¹⁰ J", "−1.33 × 10⁻⁸ J"], "A"),
    "Gravitational potential energy of two particles",
    "U = −Gm₁m₂/r, negative because the force is attractive and the zero is at infinite separation.",
    ["U = −6.67 × 10⁻¹¹ × 10 × 10/1 = −6.67 × 10⁻⁹ J"],
    why="The positive value has the wrong sign. −6.67 × 10⁻¹⁰ J uses only one mass. −1.33 × 10⁻⁸ J doubles the "
        "energy, counting the pair twice.",
    ncert="Class 11 Physics, 'Gravitation', gravitational potential energy", seconds=35, recomputed=True)

add(T, "Satellite energy and period", "Basic", "direct",
    "A geostationary satellite revolves round the Earth in a circular orbit:",
    place("In the equatorial plane, from west to east, with a period of 24 hours",
          ["In the equatorial plane, from east to west, with a period of 24 hours",
           "In a polar orbit, with a period of 12 hours",
           "Just above the Earth's surface, with a period of about 84 minutes"], "B"),
    "Geostationary satellites",
    "A geostationary satellite stays above the same point of the equator. It must therefore move in the "
    "equatorial plane in the same sense as the Earth's rotation (west to east) and have the same period, "
    "24 hours. Such satellites are used for communication.",
    ["Same period as Earth's rotation → 24 h", "Same sense of rotation → west to east",
     "Fixed above the equator → equatorial plane"],
    why="East to west would make it drift across the sky. A polar orbit cannot stay above one point. 84 minutes is "
        "the period of a satellite skimming the Earth's surface.",
    ncert="Class 11 Physics, 'Gravitation', earth satellites (geostationary satellites)", seconds=30)

add(T, "Law of gravitation", "Basic", "statement_pair",
    SP_STEM.format(
        s1="A uniform thin spherical shell exerts a non-zero gravitational force on a point mass placed anywhere "
           "inside it.",
        s2="In the absence of air resistance, the acceleration due to gravity of a falling body does not depend "
           "on the mass of the body."),
    sp("D"),
    "Shell theorem and free fall",
    "NCERT states that the gravitational force on a point mass inside a uniform spherical shell is zero: the pulls "
    "of different parts of the shell cancel. The acceleration of a freely falling body is g = GM/R², which does "
    "not contain the body's own mass.",
    ["Inside a uniform shell → net force zero → Statement I false",
     "g = GM/R² (independent of the falling body's mass) → Statement II true"],
    why="Statement I contradicts the shell result; Statement II is Galileo's observation explained by Newton's law.",
    ncert="Class 11 Physics, 'Gravitation', universal law of gravitation and acceleration due to gravity",
    seconds=40)

Lang, mp = 2.7e40, 6e24
areal = Lang / (2 * mp)
assert close(areal, 2.25e15) and close(Lang / mp, 4.5e15)
add(T, "Kepler's laws", "Intermediate", "numerical",
    "A planet of mass 6 × 10²⁴ kg revolves round the Sun. Its angular momentum about the Sun is "
    "2.7 × 10⁴⁰ kg m² s⁻¹. The area swept out per second by the line joining the planet to the Sun is:",
    place("2.25 × 10¹⁵ m²/s", ["4.5 × 10¹⁵ m²/s", "1.125 × 10¹⁵ m²/s", "9.0 × 10¹⁵ m²/s"], "C"),
    "Areal velocity and angular momentum",
    "In a short time Δt the radius vector sweeps a triangle of area ½|r × vΔt|, so the areal velocity is "
    "ΔA/Δt = |r × v|/2 = L/(2m). Its constancy is Kepler's second law.",
    ["ΔA/Δt = L/(2m) = 2.7 × 10⁴⁰/(2 × 6 × 10²⁴)", "= 2.25 × 10¹⁵ m²/s"],
    why="4.5 × 10¹⁵ forgets the ½ in the area of a triangle. 1.125 × 10¹⁵ divides by 4m. 9.0 × 10¹⁵ multiplies "
        "by 2 instead of dividing.",
    ncert="Class 11 Physics, 'Gravitation', Kepler's laws (areal velocity, ΔA/Δt = L/2m)", seconds=50,
    recomputed=True)

f_each = 1.0
net = 2 * f_each * math.cos(math.radians(30))
assert close(net, math.sqrt(3))
add(T, "Law of gravitation", "Intermediate", "numerical",
    "Three point masses, each of mass m, are placed at the corners of an equilateral triangle of side a. The "
    "magnitude of the net gravitational force on any one of them, due to the other two, is (G is the universal "
    "gravitational constant):",
    place("√3 Gm²/a²", ["2Gm²/a²", "Gm²/a²", "Zero"], "A"),
    "Superposition of gravitational forces",
    "Each of the other two masses pulls with Gm²/a² along a side of the triangle. The two pulls make 60° with each "
    "other, so the resultant is 2F cos 30°, along the bisector towards the opposite side.",
    ["F = Gm²/a² from each", "Angle between the two forces = 60°",
     "F_net = 2F cos 30° = √3 Gm²/a²"],
    why="2Gm²/a² adds the forces as if parallel. Gm²/a² is one force alone. Zero is the net field at the centroid "
        "of the triangle, not the force on a corner mass.",
    ncert="Class 11 Physics, 'Gravitation', universal law of gravitation (superposition)", seconds=55,
    recomputed=True)

add(T, "Escape and orbital velocity", "Intermediate", "assertion_reason",
    AR_STEM.format(
        a="A satellite in a circular orbit above the atmosphere keeps revolving round the Earth with a constant "
          "speed without using any fuel.",
        r="The Earth's gravitational pull on the satellite provides the centripetal force, and being perpendicular "
          "to the satellite's velocity, it does no work on it."),
    ar("A"),
    "Why a satellite needs no fuel to stay in orbit",
    "Above the atmosphere there is no drag. In a circular orbit the only force, gravity, points to the centre and "
    "is always perpendicular to the velocity. It bends the path into a circle but does no work, so the kinetic "
    "energy and speed stay constant without any engine.",
    ["Gravity = centripetal force mv²/r", "F ⊥ v → W = 0 → speed constant (A)"],
    why="R gives both parts of the reason: gravity supplies the needed centripetal force and does no work.",
    ncert="Class 11 Physics, 'Gravitation', earth satellites", seconds=45)

add(T, "Satellite energy and period", "Intermediate", "match_list",
    match_stem("A satellite of mass m revolves round the Earth (mass M) in a circular orbit of radius r. Match "
               "List-I (quantity) with List-II (expression). G is the universal gravitational constant and the "
               "potential energy is zero at infinity.",
               ["Orbital speed", "Period of revolution", "Kinetic energy", "Total mechanical energy"],
               ["−GMm/(2r)", "√(GM/r)", "GMm/(2r)", "2π√(r³/(GM))"]),
    match_options({"A": "II", "B": "IV", "C": "III", "D": "I"},
                  [{"A": "II", "B": "IV", "C": "I", "D": "III"}, {"A": "IV", "B": "II", "C": "III", "D": "I"},
                   {"A": "III", "B": "IV", "C": "II", "D": "I"}], "B"),
    "Orbital speed, period and energy of a satellite",
    "Gravity supplies the centripetal force: GMm/r² = mv²/r gives v. The period is 2πr/v. The kinetic energy is "
    "½mv² and the potential energy −GMm/r, so the total energy is negative and equal to −KE.",
    ["v = √(GM/r) → II", "T = 2πr/v = 2π√(r³/GM) → IV", "KE = ½m(GM/r) = GMm/2r → III",
     "E = GMm/2r − GMm/r = −GMm/2r → I"],
    why="The wrong codes give the kinetic energy a negative sign, or swap speed and period.",
    ncert="Class 11 Physics, 'Gravitation', earth satellites and energy of an orbiting satellite", seconds=60)

m1, m2, d = 4, 9, 1.0
x0 = d * math.sqrt(m1) / (math.sqrt(m1) + math.sqrt(m2))
V0 = -(m1 / x0 + m2 / (d - x0))
assert close(x0, 0.4) and close(m1 / x0 ** 2, m2 / (d - x0) ** 2) and close(V0, -25)
add(T, "Gravitational potential and energy", "Advanced", "numerical",
    "Two point masses of 4 kg and 9 kg are fixed 1 m apart. At the point on the line joining them where the net "
    "gravitational field is zero, the gravitational potential is (G is the universal gravitational constant; "
    "potential is zero at infinity):",
    place("−25G J/kg", ["−10G J/kg", "−15G J/kg", "Zero"], "D"),
    "Field and potential are different: neutral point",
    "The field vanishes where the two pulls are equal and opposite, between the masses. Potential is a scalar: the "
    "contributions −Gm/r of both masses add and cannot cancel, since each is negative.",
    ["4/x² = 9/(1 − x)² → 2(1 − x) = 3x → x = 0.4 m from the 4 kg mass",
     "V = −G(4/0.4 + 9/0.6) = −G(10 + 15) = −25G J/kg"],
    why="−10G and −15G each keep only one mass's contribution. Zero confuses a zero field with a zero potential.",
    ncert="Class 11 Physics, 'Gravitation', gravitational potential energy and potential", seconds=90,
    recomputed=True)

truth = [True, False, True, True, False]
multi_key(truth, "acd")
add(T, "Kepler's laws", "Advanced", "multi_statement",
    multi("Which of the following statements about the motion of planets round the Sun are correct?",
          ["A planet moves fastest when it is nearest to the Sun.",
           "The Sun lies at the centre of the elliptical orbit of each planet.",
           "For a planet in a circular orbit, Kepler's second law implies that it moves with uniform speed.",
           "The orbit of a planet lies in a fixed plane containing the Sun.",
           "Kepler obtained his three laws by deriving them from Newton's law of gravitation."]),
    place("(a), (c) and (d) only", ["(a), (b) and (c) only", "(c), (d) and (e) only", "(a), (b), (c) and (d) only"],
          "A"),
    "Kepler's laws and conservation of angular momentum",
    "The Sun is at one focus, not the centre. Equal areas in equal times mean the planet speeds up near the Sun "
    "(perihelion); in a circle equal areas mean equal arcs, i.e. uniform speed. Because the gravitational force is "
    "central, the angular momentum about the Sun is conserved, so the orbit stays in one plane. Kepler found his "
    "laws empirically from Tycho Brahe's observations, before Newton's theory.",
    ["(a) true (perihelion)", "(b) focus, not centre → false", "(c) true",
     "(d) L conserved (direction fixed) → true", "(e) empirical, from Tycho Brahe's data → false"],
    why="Codes with (b) put the Sun at the centre; codes with (e) reverse the history: Newton explained Kepler's "
        "laws, not the other way round.",
    ncert="Class 11 Physics, 'Gravitation', Kepler's laws", seconds=75)


# =====================================================================================================================
# Properties of Solids and Liquids (B4 I6 A4)
# =====================================================================================================================
T = "Properties of Solids and Liquids"

S_, l_ = 0.03, 0.05
assert close(2 * S_ * l_, 3e-3) and close(S_ * l_, 1.5e-3)
add(T, "Surface tension and capillarity", "Basic", "numerical",
    "A soap film is formed in a rectangular wire frame, one side of which is a light movable wire 5 cm long. The "
    "surface tension of the soap solution is 0.03 N/m. Neglecting the weight of the wire, the force needed to hold "
    "the movable wire in equilibrium is:",
    place("3 × 10⁻³ N", ["1.5 × 10⁻³ N", "6 × 10⁻³ N", "0.15 N"], "C"),
    "Surface tension as force per unit length",
    "Surface tension S is the force per unit length acting along the surface, perpendicular to a line in it. A "
    "soap film has two surfaces, so the film pulls the wire with 2Sl.",
    ["Two surfaces pull on the wire: F = 2Sl", "F = 2 × 0.03 × 0.05 = 3 × 10⁻³ N"],
    why="1.5 × 10⁻³ N counts only one surface. 6 × 10⁻³ N counts four surfaces. 0.15 N uses l = 5 instead of "
        "0.05 m.",
    ncert="Class 11 Physics, 'Mechanical Properties of Fluids', surface tension (surface energy of a film)",
    seconds=40, recomputed=True)

eta, r_, v_ = 1.5, 1e-3, 0.02
Fd = 6 * math.pi * eta * r_ * v_
assert close(Fd, 1.8 * math.pi * 1e-4) and close(math.pi * eta * r_ * v_, 0.3 * math.pi * 1e-4)
add(T, "Viscosity and Stokes' law", "Basic", "numerical",
    "A small sphere of radius 1 mm moves slowly with a speed of 2 cm/s through glycerine, whose coefficient of "
    "viscosity is 1.5 Pa s. According to Stokes' law, the viscous force on the sphere is:",
    place("1.8π × 10⁻⁴ N", ["0.3π × 10⁻⁴ N", "1.8π × 10⁻⁷ N", "1.8π × 10⁻² N"], "D"),
    "Stokes' law",
    "For a small sphere moving slowly through a viscous fluid, F = 6πηrv. Convert the radius and the speed to SI "
    "units first.",
    ["r = 10⁻³ m, v = 0.02 m/s", "F = 6π × 1.5 × 10⁻³ × 0.02 = 1.8π × 10⁻⁴ N ≈ 5.7 × 10⁻⁴ N"],
    why="0.3π × 10⁻⁴ N drops the factor 6. 1.8π × 10⁻⁷ N squares the radius. 1.8π × 10⁻² N uses v = 2 instead of "
        "0.02 m/s.",
    ncert="Class 11 Physics, 'Mechanical Properties of Fluids', Stokes' law", seconds=40, recomputed=True)

add(T, "Heat transfer", "Basic", "direct",
    "The mode of heat transfer that does not need any material medium, and in which the energy travels with the "
    "speed of light, is:",
    place("Radiation", ["Conduction", "Natural convection", "Forced convection"], "D"),
    "Thermal radiation",
    "Conduction and convection need a material medium (conduction through contact of neighbouring particles, "
    "convection through bulk movement of a fluid). Radiation is carried by electromagnetic waves, which travel "
    "through vacuum at the speed of light; this is how the Sun's heat reaches the Earth.",
    ["Conduction: needs matter", "Convection: needs a moving fluid", "Radiation: electromagnetic waves → vacuum, c"],
    why="All the other options need a material medium and are far slower than light.",
    ncert="Class 11 Physics, 'Thermal Properties of Matter', heat transfer (radiation)", seconds=25)

add(T, "Thermal expansion and calorimetry", "Basic", "assertion_reason",
    AR_STEM.format(
        a="Small gaps are left between successive sections of a railway track.",
        r="The rails expand when their temperature rises, and if this expansion were prevented, large thermal "
          "stresses would develop and could bend the track."),
    ar("A"),
    "Thermal expansion and thermal stress",
    "A heated rail tends to lengthen by ΔL = αLΔT. If the ends are held rigidly, the rail is compressed instead and "
    "a thermal stress YαΔT develops, which can buckle the track. Gaps allow the rails to expand freely.",
    ["Rails expand on heating", "Blocked expansion → stress Y α ΔT → buckling", "Gaps avoid this → A"],
    why="R gives exactly why the gaps are needed, so it explains A.",
    ncert="Class 11 Physics, 'Thermal Properties of Matter', thermal expansion", seconds=35)

S_, r_ = 0.07, 1e-4
assert close(2 * S_ / r_, 1400) and close(4 * S_ / r_, 2800)
add(T, "Surface tension and capillarity", "Intermediate", "numerical",
    "An air bubble of radius 0.1 mm is formed just below the surface of water. The surface tension of water is "
    "0.07 N/m. The excess of pressure inside the bubble over that in the water outside it is:",
    place("1400 Pa", ["2800 Pa", "700 Pa", "14 Pa"], "B"),
    "Excess pressure inside an air bubble in a liquid",
    "An air bubble inside a liquid has only one liquid–air surface (its inner surface), so the excess pressure is "
    "2S/r, as for a liquid drop. A soap bubble in air has two surfaces and an excess pressure of 4S/r.",
    ["One surface → ΔP = 2S/r", "ΔP = 2 × 0.07/(1 × 10⁻⁴) = 1400 Pa"],
    why="2800 Pa uses 4S/r, which applies to a soap bubble in air. 700 Pa uses S/r. 14 Pa uses r in centimetres.",
    ncert="Class 11 Physics, 'Mechanical Properties of Fluids', excess pressure inside a drop and a bubble",
    seconds=45, recomputed=True)

rho_air, v_up, v_dn, A_ = 1.2, 50, 40, 10
lift = 0.5 * rho_air * (v_up ** 2 - v_dn ** 2) * A_
assert close(lift, 5400) and close(0.5 * rho_air * (v_up - v_dn) ** 2 * A_, 600)
add(T, "Bernoulli's principle", "Intermediate", "numerical",
    "In level flight, air flows past the upper surface of an aeroplane wing at 50 m/s and past its lower surface at "
    "40 m/s. The wing has an area of 10 m², and the density of air is 1.2 kg/m³. Neglecting the small difference "
    "in height between the two surfaces, the upward (lift) force on the wing due to this pressure difference is:",
    place("5400 N", ["600 N", "10 800 N", "540 N"], "A"),
    "Dynamic lift from Bernoulli's principle",
    "Along a streamline at the same height, P + ½ρv² is constant, so the faster air above the wing is at lower "
    "pressure. The pressure difference times the area gives the lift.",
    ["ΔP = ½ρ(v₁² − v₂²) = ½ × 1.2 × (2500 − 1600) = 540 Pa", "Lift = ΔP × A = 540 × 10 = 5400 N"],
    why="600 N uses (v₁ − v₂)² instead of v₁² − v₂². 10 800 N drops the ½. 540 N is the pressure difference, not "
        "the force.",
    ncert="Class 11 Physics, 'Mechanical Properties of Fluids', Bernoulli's principle (dynamic lift)", seconds=60,
    recomputed=True)

Q_w = 0.3 * 4200 * (25 - 20)
c_ball = Q_w / (0.1 * (200 - 25))
assert Q_w == 6300 and close(c_ball, 360) and close(Q_w / (0.1 * 180), 350)
add(T, "Thermal expansion and calorimetry", "Intermediate", "numerical",
    "A metal ball of mass 100 g, heated to 200 °C, is dropped into 300 g of water at 20 °C in an insulated vessel "
    "of negligible heat capacity. The final temperature of the water and ball is 25 °C. Taking the specific heat "
    "capacity of water as 4200 J kg⁻¹ K⁻¹, the specific heat capacity of the metal is:",
    place("360 J kg⁻¹ K⁻¹", ["350 J kg⁻¹ K⁻¹", "40 J kg⁻¹ K⁻¹", "3600 J kg⁻¹ K⁻¹"], "C"),
    "Principle of calorimetry",
    "With no heat lost, the heat given out by the ball as it cools to the final temperature equals the heat taken "
    "in by the water as it warms to the same temperature.",
    ["Heat gained by water = 0.3 × 4200 × (25 − 20) = 6300 J",
     "Heat lost by ball = 0.1 × c × (200 − 25) = 17.5c",
     "17.5c = 6300 → c = 360 J kg⁻¹ K⁻¹"],
    why="350 uses a fall of 180 °C (200 − 20), forgetting that the ball ends at 25 °C. 40 swaps the masses of "
        "ball and water. 3600 mixes grams and kilograms.",
    ncert="Class 11 Physics, 'Thermal Properties of Matter', calorimetry", seconds=70, recomputed=True)

K = 1.0
K_eq = (K + 2 * K) / 2
assert K_eq == 1.5 and close(2 / (1 / K + 1 / (2 * K)), 4 / 3)
add(T, "Heat transfer", "Intermediate", "numerical",
    "Two rods of the same length and the same area of cross-section, with thermal conductivities K and 2K, are "
    "placed side by side between the same two heat reservoirs, so that heat flows through them in parallel. Their "
    "sides are insulated. In the steady state, a single rod of the same length and twice the area of cross-section "
    "would carry the same total rate of heat flow if its thermal conductivity were:",
    place("1.5K", ["3K", "4K/3", "2K/3"], "A"),
    "Conduction through rods in parallel",
    "For each rod H = KAΔT/L. In parallel both rods have the same temperature difference, so the rates add. The "
    "equivalent rod of area 2A must give the same total.",
    ["H = KAΔT/L + 2KAΔT/L = 3KAΔT/L", "K_eq(2A)ΔT/L = 3KAΔT/L → K_eq = 1.5K"],
    why="3K forgets that the equivalent rod has twice the area. 4K/3 is the series result for the two rods placed "
        "end to end. 2K/3 is the series formula without the factor for the doubled length.",
    ncert="Class 11 Physics, 'Thermal Properties of Matter', conduction and thermal conductivity", seconds=70,
    recomputed=True)

add(T, "Elasticity and moduli", "Intermediate", "statement_pair",
    SP_STEM.format(
        s1="Stress is the restoring force per unit area that develops inside a deformed body.",
        s2="Rubber has a larger Young's modulus than steel, because rubber stretches more easily."),
    sp("C"),
    "Stress and Young's modulus",
    "When a body is deformed, internal restoring forces develop; the restoring force per unit area is the stress. "
    "Young's modulus is stress/strain. For the same stress, rubber shows a much larger strain than steel, so its "
    "Young's modulus is far smaller: a material that stretches easily has a small modulus.",
    ["Statement I: NCERT definition of stress → true",
     "Statement II: larger strain for the same stress → smaller Y → rubber's Y ≪ steel's → false"],
    why="Statement II reverses the meaning of the modulus: steel is the more 'elastic' of the two in this sense.",
    ncert="Class 11 Physics, 'Mechanical Properties of Solids', stress and strain; Young's modulus", seconds=45)

add(T, "Fluid pressure and Pascal's law", "Intermediate", "match_list",
    match_stem("Match List-I (device or observation) with List-II (the principle or property it depends on).",
               ["A paint sprayer (atomiser)", "A hydraulic lift", "Rise of oil in the wick of a lamp",
                "A raindrop falling with a constant velocity"],
               ["Capillarity (surface tension)", "Viscous drag (Stokes' law)", "Bernoulli's principle",
                "Pascal's law"]),
    match_options({"A": "III", "B": "IV", "C": "I", "D": "II"},
                  [{"A": "IV", "B": "III", "C": "I", "D": "II"}, {"A": "III", "B": "IV", "C": "II", "D": "I"},
                   {"A": "I", "B": "IV", "C": "III", "D": "II"}], "D"),
    "Applications of fluid properties",
    "A sprayer blows air fast over the top of a tube; the low pressure there draws the liquid up (Bernoulli). A "
    "hydraulic lift transmits pressure undiminished through an enclosed liquid (Pascal). Oil climbs the narrow "
    "spaces of a wick by capillary action. A falling drop speeds up until the viscous drag plus buoyancy balances "
    "its weight, giving the terminal velocity.",
    ["Atomiser → Bernoulli → III", "Hydraulic lift → Pascal → IV", "Wick → capillarity → I",
     "Terminal velocity of raindrop → viscous drag → II"],
    why="The wrong codes swap the sprayer with the lift, or the wick with the raindrop.",
    ncert="Class 11 Physics, 'Mechanical Properties of Fluids', applications of Pascal's law, Bernoulli's "
          "principle, viscosity and surface tension", seconds=50)

load, L1, A1 = 100, 1.0, 1e-6
ext_s = load * L1 / (A1 * 2e11)
ext_b = load * L1 / (A1 * 1e11)
assert close(ext_s, 0.5e-3) and close(ext_b, 1.0e-3) and close(ext_s + ext_b, 1.5e-3)
add(T, "Elasticity and moduli", "Advanced", "numerical",
    "A steel wire and a brass wire, each 1 m long and of cross-sectional area 1 mm², are joined end to end. The "
    "combination hangs vertically from a rigid support and a load of 100 N is hung from its lower end. Young's "
    "modulus of steel is 2 × 10¹¹ N/m² and that of brass is 1 × 10¹¹ N/m². Neglecting the weights of the wires, "
    "the total extension of the combination is:",
    place("1.5 mm", ["0.5 mm", "1.0 mm", "0.33 mm"], "B"),
    "Young's modulus for wires in series",
    "Joined end to end, both wires carry the same tension, equal to the load. Each stretches by ΔL = FL/(AY), and "
    "the total extension is the sum.",
    ["Steel: 100 × 1/(10⁻⁶ × 2 × 10¹¹) = 0.5 mm", "Brass: 100 × 1/(10⁻⁶ × 1 × 10¹¹) = 1.0 mm",
     "Total = 1.5 mm"],
    why="0.5 mm and 1.0 mm are the separate extensions. 0.33 mm treats the wires as sharing the load side by side "
        "(in parallel).",
    ncert="Class 11 Physics, 'Mechanical Properties of Solids', Young's modulus", seconds=70, recomputed=True)

V0, dT, g_hg, a_gl = 500, 80, 1.8e-4, 9e-6
over = V0 * dT * (g_hg - 3 * a_gl)
assert close(over, 6.12) and close(V0 * dT * g_hg, 7.2) and close(V0 * dT * (g_hg - a_gl), 6.84)
add(T, "Thermal expansion and calorimetry", "Advanced", "numerical",
    "A glass flask of volume 500 cm³ at 20 °C is completely filled with mercury at that temperature. The flask "
    "and the mercury are heated together to 100 °C. The coefficient of volume expansion of mercury is "
    "1.8 × 10⁻⁴ °C⁻¹ and the coefficient of linear expansion of glass is 9 × 10⁻⁶ °C⁻¹. The volume of mercury "
    "that overflows is:",
    place("6.12 cm³", ["7.2 cm³", "6.84 cm³", "8.28 cm³"], "C"),
    "Volume expansion of a liquid in an expanding container",
    "Both the mercury and the flask expand. The overflow is the difference between the expansion of the mercury "
    "and the increase in the flask's capacity. For an isotropic solid, the coefficient of volume expansion is "
    "about three times the coefficient of linear expansion.",
    ["γ_glass = 3 × 9 × 10⁻⁶ = 2.7 × 10⁻⁵ °C⁻¹",
     "Overflow = V₀ΔT(γ_Hg − γ_glass) = 500 × 80 × (1.8 × 10⁻⁴ − 0.27 × 10⁻⁴)",
     "= 40 000 × 1.53 × 10⁻⁴ = 6.12 cm³"],
    why="7.2 cm³ ignores the expansion of the flask. 6.84 cm³ uses the linear coefficient of glass instead of its "
        "volume coefficient. 8.28 cm³ adds the flask's expansion instead of subtracting it.",
    ncert="Class 11 Physics, 'Thermal Properties of Matter', thermal expansion", seconds=90, recomputed=True)

r_c, S_ = 5e-4, 0.07
m_lift = 2 * math.pi * r_c * S_ / 10
assert close(m_lift, 7 * math.pi * 1e-6) and close(math.pi * r_c * S_ / 10, 3.5 * math.pi * 1e-6)
add(T, "Surface tension and capillarity", "Advanced", "numerical",
    "A clean glass capillary tube of internal radius 0.5 mm stands vertically with its lower end in water. The "
    "surface tension of water is 0.07 N/m and the angle of contact is 0°. Taking g = 10 m/s², the mass of the "
    "water column raised in the tube above the outside level is (neglect the small volume of the meniscus):",
    place("7π × 10⁻⁶ kg", ["3.5π × 10⁻⁶ kg", "14π × 10⁻⁶ kg", "7π × 10⁻⁹ kg"], "D"),
    "Force balance in capillary rise",
    "Surface tension acts along the circle of contact, of length 2πr, pulling the liquid up with force 2πrS cos θ. "
    "In equilibrium this supports the weight of the raised column. So the mass raised does not depend on the "
    "density and only on r and S.",
    ["2πrS cos θ = mg", "m = 2π × 5 × 10⁻⁴ × 0.07/10 = 7π × 10⁻⁶ kg ≈ 2.2 × 10⁻⁵ kg"],
    shortcut="From h = 2S cos θ/(rρg): m = ρπr²h = 2πrS cos θ/g, the same result.",
    why="3.5π × 10⁻⁶ kg uses the radius instead of the circumference (πr instead of 2πr). 14π × 10⁻⁶ kg counts two "
        "surfaces, as for a film. 7π × 10⁻⁹ kg uses the radius in millimetres once and metres once.",
    ncert="Class 11 Physics, 'Mechanical Properties of Fluids', capillary rise", seconds=80, recomputed=True)

truth = [True, True, False, False, True]
multi_key(truth, "abe")
add(T, "Elasticity and moduli", "Advanced", "multi_statement",
    multi("The following statements refer to the stress–strain curve of a metal wire loaded gradually until it "
          "breaks, and to elastic materials in general. Which of them are correct?",
          ["Up to the proportional limit, the stress is proportional to the strain.",
           "If the wire is loaded beyond its yield point (elastic limit) and the load is then removed, the wire "
           "does not return to its original length.",
           "On the curve, the fracture point is reached before the yield point.",
           "The ultimate tensile strength is the stress at which the wire just begins to yield.",
           "Substances such as the elastic tissue of the aorta can be stretched to large strains although they "
           "do not obey Hooke's law over most of the range; such substances are called elastomers."]),
    place("(a), (b) and (e) only", ["(a), (b), (d) and (e) only", "(b), (c) and (e) only", "(a) and (d) only"],
          "A"),
    "Stress–strain curve",
    "In the initial linear region Hooke's law holds. Beyond the yield point (elastic limit) the deformation is "
    "plastic: a permanent set remains when the load is removed. Loading further, the stress reaches a maximum, "
    "the ultimate tensile strength, after which the wire thins and breaks at the fracture point. The yield "
    "strength, not the ultimate strength, marks the start of yielding. NCERT describes the aorta's tissue as an "
    "elastomer.",
    ["(a) true", "(b) permanent set beyond the elastic limit → true",
     "(c) yield point comes first, fracture last → false", "(d) that is the yield strength → false",
     "(e) true (elastomers)"],
    why="Codes with (d) confuse the ultimate tensile strength with the yield strength; codes with (c) reverse the "
        "order of points on the curve.",
    ncert="Class 11 Physics, 'Mechanical Properties of Solids', stress–strain curve", seconds=90)


# =====================================================================================================================
# Thermodynamics (B3 I4 A3)
# =====================================================================================================================
T = "Thermodynamics"

dT_ = 10 * 84 / 4200
assert close(dT_, 0.2)
add(T, "Zeroth and first law", "Basic", "numerical",
    "Water falls through a height of 84 m. Assume that all the gravitational potential energy it loses is "
    "converted into heat that stays in the water. Taking g = 10 m/s² and the specific heat capacity of water as "
    "4200 J kg⁻¹ K⁻¹, the rise in the temperature of the water is:",
    place("0.2 °C", ["2 °C", "0.02 °C", "20 °C"], "B"),
    "Equivalence of work and heat",
    "Mechanical work and heat are both forms of energy transfer. Each kilogram of water loses mgh = gh of "
    "potential energy and gains c ΔT of internal energy, so the mass cancels.",
    ["gh = cΔT", "ΔT = 10 × 84/4200 = 0.2 °C"],
    why="2 °C and 0.02 °C are powers-of-ten slips. 20 °C would need a fall of 8.4 km.",
    ncert="Class 11 Physics, 'Thermodynamics', heat, internal energy and work", seconds=35, recomputed=True)

add(T, "Zeroth and first law", "Basic", "statement_pair",
    SP_STEM.format(
        s1="If two systems A and B are each separately in thermal equilibrium with a third system C, then A and B "
           "need not be in thermal equilibrium with each other.",
        s2="A body contains a definite amount of heat, so heat is a thermodynamic state variable like "
           "temperature."),
    sp("B"),
    "Zeroth law, and heat as energy in transit",
    "The zeroth law says the opposite of Statement I: A and B must be in thermal equilibrium with each other, "
    "which is what allows temperature to be defined. Heat is energy transferred because of a temperature "
    "difference; a body has internal energy, not 'heat', and the heat exchanged depends on the process, so heat "
    "is not a state variable.",
    ["Statement I contradicts the zeroth law → false",
     "Statement II: heat is energy in transit, path dependent → false"],
    why="Both statements are false: Statement I negates the zeroth law and Statement II confuses heat with "
        "internal energy.",
    ncert="Class 11 Physics, 'Thermodynamics', zeroth law; heat, internal energy and work", seconds=40)

add(T, "Isothermal and adiabatic processes", "Basic", "direct",
    "A gas is enclosed in a cylinder whose walls and piston are perfectly insulating. The gas is compressed by "
    "pushing the piston in. The process is:",
    place("Adiabatic, and the temperature of the gas rises",
          ["Adiabatic, and the temperature of the gas falls", "Isothermal, and the temperature of the gas stays "
           "constant", "Isochoric, and the temperature of the gas rises"], "B"),
    "Adiabatic compression",
    "Perfectly insulating walls allow no heat exchange, so Q = 0 and the process is adiabatic. The work done on "
    "the gas then all goes into its internal energy: ΔU = −W > 0 for a compression, so the temperature rises.",
    ["Q = 0 → adiabatic", "Compression: W (by gas) < 0 → ΔU = −W > 0 → T rises"],
    why="An adiabatic expansion (not compression) cools the gas. An isothermal process needs heat exchange with a "
        "reservoir, impossible through insulating walls. The volume changes, so it is not isochoric.",
    ncert="Class 11 Physics, 'Thermodynamics', adiabatic process", seconds=30)

P0, Vl = 1e5, 1e-3
W_AB = P0 * (3 - 1) * Vl
W_BC = -(1e5 + 4e5) / 2 * (3 - 1) * Vl
W_net = W_AB + W_BC
assert close(W_AB, 200) and close(W_BC, -500) and close(W_net, -300)
add(T, "Zeroth and first law", "Intermediate", "numerical",
    "An ideal gas is taken round the cycle A → B → C → A. From A (1 L, 1 × 10⁵ Pa) it expands at constant "
    "pressure to B (3 L, 1 × 10⁵ Pa). It is then compressed to C (1 L, 4 × 10⁵ Pa) along a straight line on the "
    "P–V diagram, and finally its pressure is lowered at constant volume back to A. The net heat absorbed by the "
    "gas in one cycle is:",
    place("−300 J, i.e. the gas gives out 300 J of heat", ["+300 J, i.e. the gas absorbs 300 J of heat",
          "−600 J, i.e. the gas gives out 600 J of heat", "Zero, since the process is cyclic"], "C"),
    "First law for a cyclic process",
    "In a cycle ΔU = 0, so the net heat absorbed equals the net work done by the gas, which is the area enclosed "
    "on the P–V diagram, positive for a clockwise cycle and negative for an anticlockwise one. Here the "
    "compression B → C happens at higher pressures than the expansion A → B, so more work is done on the gas "
    "than by it.",
    ["W_AB = 1 × 10⁵ × 2 × 10⁻³ = +200 J",
     "W_BC = −(average pressure 2.5 × 10⁵ Pa) × 2 × 10⁻³ = −500 J", "W_CA = 0 (constant volume)",
     "Q_net = W_net = 200 − 500 = −300 J (triangle area ½ × 2 × 10⁻³ × 3 × 10⁵ = 300 J)"],
    why="+300 J has the right size but the wrong sign: the cycle runs anticlockwise. −600 J takes the whole "
        "rectangle instead of the triangle. Zero confuses ΔU = 0 with Q = 0.",
    ncert="Class 11 Physics, 'Thermodynamics', first law and cyclic processes", seconds=100, recomputed=True)

T2 = 280 * 128 ** ((1.4 - 1) / 1.4)
assert close(T2, 1120) and close(280 * 128 ** (1 / 7), 560) and close(280 * 128 ** (3 / 7), 2240)
add(T, "Isothermal and adiabatic processes", "Intermediate", "numerical",
    "An ideal diatomic gas (γ = 1.4) at 280 K is compressed reversibly and adiabatically until its pressure "
    "becomes 128 times its initial pressure. Its final temperature is:",
    place("1120 K", ["560 K", "280 K", "2240 K"], "A"),
    "Pressure–temperature relation in an adiabatic process",
    "Combining PV^γ = constant with PV = nRT gives T ∝ P^((γ−1)/γ) for a reversible adiabatic process.",
    ["(γ − 1)/γ = 0.4/1.4 = 2/7", "T₂ = 280 × 128^(2/7) = 280 × (2⁷)^(2/7) = 280 × 4 = 1120 K"],
    why="560 K uses the exponent 1/7. 280 K treats the compression as isothermal. 2240 K uses the exponent 3/7.",
    ncert="Class 11 Physics, 'Thermodynamics', adiabatic process", seconds=60, recomputed=True)

add(T, "Isothermal and adiabatic processes", "Intermediate", "assertion_reason",
    AR_STEM.format(
        a="When a gas in a cylinder is compressed very rapidly by a piston, its temperature rises.",
        r="During a very rapid compression, heat flows into the gas from the surroundings."),
    ar("C"),
    "Rapid processes are nearly adiabatic",
    "A very rapid compression leaves no time for heat exchange, so it is nearly adiabatic (Q ≈ 0). The work done "
    "on the gas then raises its internal energy, and so its temperature (the reason a bicycle pump gets hot). Heat "
    "does not flow in; if anything, the warmed gas would later lose heat to the surroundings.",
    ["Rapid → Q ≈ 0 → ΔU = work done on gas > 0 → T rises → A true",
     "No time for heat flow, and the gas becomes hotter than the surroundings → R false"],
    why="R gives a wrong mechanism: the temperature rises because of the work done on the gas, not because of "
        "heat flowing in.",
    ncert="Class 11 Physics, 'Thermodynamics', adiabatic process", seconds=45)

add(T, "Zeroth and first law", "Intermediate", "match_list",
    match_stem("A fixed amount of an ideal gas undergoes each of the processes in List-I. Q is the heat absorbed by "
               "the gas, W the work done by the gas and ΔU the change in its internal energy. Match List-I with "
               "List-II.",
               ["Isothermal expansion", "Adiabatic expansion", "Heating at constant volume",
                "Compression at constant pressure"],
               ["Q = 0 and ΔU < 0", "W = 0 and ΔU > 0", "Q > 0 and ΔU = 0", "Q < 0, W < 0 and ΔU < 0"]),
    match_options({"A": "III", "B": "I", "C": "II", "D": "IV"},
                  [{"A": "I", "B": "III", "C": "II", "D": "IV"}, {"A": "III", "B": "I", "C": "IV", "D": "II"},
                   {"A": "III", "B": "II", "C": "I", "D": "IV"}], "B"),
    "Signs of Q, W and ΔU in ideal-gas processes",
    "Apply Q = ΔU + W, remembering that ΔU of an ideal gas follows its temperature, and that W > 0 for "
    "expansion. In an isobaric compression V falls at constant P, so T = PV/nR falls too.",
    ["Isothermal expansion: ΔU = 0, W > 0 → Q > 0 → III",
     "Adiabatic expansion: Q = 0, W > 0 → ΔU < 0 → I",
     "Isochoric heating: W = 0, T rises → ΔU > 0 → II",
     "Isobaric compression: W < 0, T falls → ΔU < 0 → Q = ΔU + W < 0 → IV"],
    why="The wrong codes swap the isothermal and adiabatic expansions, or think an isobaric compression warms the "
        "gas.",
    ncert="Class 11 Physics, 'Thermodynamics', first law and thermodynamic processes", seconds=70)

nR, Tg = 1.0, 300.0
W_isobaric = nR * Tg * (2 - 1)
W_isothermal = nR * Tg * math.log(2)
gam = 1.4
W_adiabatic = nR * Tg * (1 - 2 ** (1 - gam)) / (gam - 1)
assert W_isobaric > W_isothermal > W_adiabatic > 0
add(T, "Isothermal and adiabatic processes", "Advanced", "direct",
    "Equal amounts of the same ideal gas, starting from the same initial state, are expanded reversibly from "
    "volume V to volume 2V in three different ways: (i) at constant pressure, (ii) isothermally and "
    "(iii) adiabatically. If W₁, W₂ and W₃ are the respective works done by the gas, then:",
    place("W₁ > W₂ > W₃", ["W₃ > W₂ > W₁", "W₂ > W₁ > W₃", "W₁ = W₂ = W₃"], "D"),
    "Comparing works from P–V curves",
    "The work done is the area under the P–V curve from V to 2V. From the same starting point, the isobaric line is "
    "horizontal, the isotherm falls (P ∝ 1/V), and the adiabat falls even more steeply (P ∝ 1/V^γ). So the areas, "
    "and the works, are in the order isobaric > isothermal > adiabatic.",
    ["Isobaric: W₁ = P₀V = nRT₀", "Isothermal: W₂ = nRT₀ ln 2 ≈ 0.69 nRT₀",
     "Adiabatic (γ = 1.4): W₃ = nRT₀(1 − 2^(−0.4))/0.4 ≈ 0.61 nRT₀", "W₁ > W₂ > W₃"],
    why="W₃ > W₂ > W₁ reverses the order. W₂ > W₁ forgets that pressure stays highest in the isobaric process. "
        "Equal works ignore that work depends on the path.",
    ncert="Class 11 Physics, 'Thermodynamics', isothermal and adiabatic processes", seconds=75)

Q1, W1 = 80, 50
dU = Q1 - W1
Q2 = dU + 20
Q_back = -dU + (-40)
assert dU == 30 and Q2 == 50 and Q_back == -70
add(T, "Zeroth and first law", "Advanced", "numerical",
    "A gas is taken from state A to state B along path 1, absorbing 80 J of heat and doing 50 J of work. It is then "
    "brought back from B to A along a different path, during which 40 J of work is done ON the gas. In the return "
    "from B to A, the gas:",
    place("Gives out 70 J of heat", ["Absorbs 10 J of heat", "Gives out 10 J of heat", "Absorbs 70 J of heat"],
          "B"),
    "Internal energy as a state function",
    "ΔU between two states is the same for every path. Find U_B − U_A from path 1, then apply the first law to the "
    "return path with the correct signs.",
    ["Path 1: ΔU_AB = Q − W = 80 − 50 = 30 J",
     "Return: ΔU_BA = −30 J, W_BA = −40 J (work done on the gas)",
     "Q_BA = ΔU_BA + W_BA = −30 − 40 = −70 J → 70 J given out"],
    why="'Absorbs 10 J' and 'gives out 10 J' add −30 and +40 with a sign error in W. 'Absorbs 70 J' has the right "
        "size but the wrong sign.",
    ncert="Class 11 Physics, 'Thermodynamics', first law of thermodynamics", seconds=80, recomputed=True)

truth = [True, True, True, False, False]
multi_key(truth, "abc")
add(T, "Isothermal and adiabatic processes", "Advanced", "multi_statement",
    multi("Two identical samples of an ideal gas start from the same state. One is compressed reversibly and "
          "isothermally, and the other reversibly and adiabatically, both to the same final volume. Which of the "
          "following statements are correct?",
          ["The final pressure is greater in the adiabatic compression.",
           "More work is done on the gas in the adiabatic compression.",
           "In the isothermal compression, the gas gives out heat equal to the work done on it.",
           "In the adiabatic compression, the internal energy of the gas decreases.",
           "The final temperature is the same in both compressions."]),
    place("(a), (b) and (c) only", ["(a), (c) and (e) only", "(b), (c) and (d) only", "(a) and (c) only"], "C"),
    "Isothermal versus adiabatic compression",
    "For compression from the same point, the adiabat (PV^γ = constant) rises more steeply than the isotherm "
    "(PV = constant), so the pressure is higher at every smaller volume, the final pressure is higher, and the "
    "area under the curve (work done on the gas) is larger. In the isothermal case ΔU = 0, so the heat given out "
    "equals the work done on the gas. In the adiabatic case Q = 0 and the work done on the gas raises U and T.",
    ["(a) steeper adiabat → higher P → true", "(b) larger area → true", "(c) ΔU = 0 → Q = W → true",
     "(d) ΔU = +W_on > 0 → false", "(e) adiabatic T rises, isothermal T constant → false"],
    why="Codes with (d) or (e) treat the adiabatic compression as if it cooled the gas or kept T fixed; (a) and "
        "(c) only misses (b).",
    ncert="Class 11 Physics, 'Thermodynamics', isothermal and adiabatic processes", seconds=90)


# =====================================================================================================================
# Kinetic Theory of Gases (B2 I2 A2)
# =====================================================================================================================
T = "Kinetic Theory of Gases"

truth = [True, False, True, False]
multi_key(truth, "ac")
add(T, "Ideal gas equation", "Basic", "multi_statement",
    multi("Which of the following statements are correct?",
          ["For μ moles of an ideal gas, PV = μRT, where R is the universal gas constant.",
           "Boltzmann's constant is related to the gas constant R and Avogadro's number N_A by k_B = N_A/R.",
           "Real gases approach ideal-gas behaviour at low pressures and high temperatures.",
           "The value of the gas constant R is different for different gases."]),
    place("(a) and (c) only", ["(a), (b) and (c) only", "(c) and (d) only", "(a), (c) and (d) only"], "D"),
    "Ideal gas equation",
    "The ideal gas equation is PV = μRT with the same R for all gases. Writing μ = N/N_A gives PV = Nk_BT with "
    "k_B = R/N_A. Real gases behave nearly ideally when the molecules are far apart and fast (low pressure, high "
    "temperature).",
    ["(a) true", "(b) k_B = R/N_A, not N_A/R → false", "(c) true", "(d) R is universal → false"],
    why="Codes with (b) invert the relation between k_B, R and N_A; codes with (d) forget that R is universal.",
    ncert="Class 11 Physics, 'Kinetic Theory', molecular nature of matter and behaviour of gases", seconds=45)

add(T, "Ideal gas equation", "Basic", "direct",
    "The number of molecules in 22.4 litres of any ideal gas at standard temperature and pressure (273 K, 1 atm) "
    "is about:",
    place("6.02 × 10²³", ["2.69 × 10²⁵", "6.02 × 10²⁶", "1.38 × 10⁻²³"], "D"),
    "Avogadro's number",
    "One mole of an ideal gas occupies 22.4 L at STP, and one mole contains Avogadro's number of molecules, "
    "N_A = 6.02 × 10²³. This also follows from Avogadro's hypothesis that equal volumes of all gases at the same "
    "temperature and pressure contain equal numbers of molecules.",
    ["22.4 L at STP = 1 mol", "1 mol = 6.02 × 10²³ molecules"],
    why="2.69 × 10²⁵ is roughly the number in one cubic metre at STP. 6.02 × 10²⁶ is the number in a "
        "kilomole. 1.38 × 10⁻²³ is Boltzmann's constant in J/K.",
    ncert="Class 11 Physics, 'Kinetic Theory', behaviour of gases (Avogadro's hypothesis)", seconds=25)

R = 8.3
U_m, Cv, Cp, PV = 1.5 * R * 300, 1.5 * R, 2.5 * R, R * 300
assert close(U_m, 3735) and close(Cv, 12.45) and close(Cp, 20.75) and close(PV, 2490)
add(T, "Degrees of freedom and equipartition", "Intermediate", "match_list",
    match_stem("One mole of a monatomic ideal gas is at 300 K. Taking R = 8.3 J mol⁻¹ K⁻¹ and using the law of "
               "equipartition of energy, match List-I (quantity) with List-II (its numerical value in SI units).",
               ["Internal energy of the gas (in J)",
                "Molar specific heat at constant volume (in J mol⁻¹ K⁻¹)",
                "Molar specific heat at constant pressure (in J mol⁻¹ K⁻¹)",
                "Product PV of its pressure and volume (in J)"],
               ["2490", "20.75", "3735", "12.45"]),
    match_options({"A": "III", "B": "IV", "C": "II", "D": "I"},
                  [{"A": "I", "B": "IV", "C": "II", "D": "III"}, {"A": "III", "B": "II", "C": "IV", "D": "I"},
                   {"A": "III", "B": "IV", "C": "I", "D": "II"}], "B"),
    "Equipartition and specific heats of a monatomic gas",
    "A monatomic molecule has 3 translational degrees of freedom, each with ½k_BT on average, so U = (3/2)RT per "
    "mole and C_v = (3/2)R. Then C_p = C_v + R = (5/2)R, and PV = RT for one mole.",
    ["U = 1.5 × 8.3 × 300 = 3735 J → III", "C_v = 1.5 × 8.3 = 12.45 → IV", "C_p = 2.5 × 8.3 = 20.75 → II",
     "PV = 8.3 × 300 = 2490 J → I"],
    why="The wrong codes swap U with PV, or C_v with C_p.",
    ncert="Class 11 Physics, 'Kinetic Theory', law of equipartition of energy and specific heat capacity",
    seconds=70)

add(T, "Pressure and rms speed", "Intermediate", "statement_pair",
    SP_STEM.format(
        s1="For a gas in equilibrium in a stationary container, the average velocity (a vector) of its molecules "
           "is zero, although their rms speed is not zero.",
        s2="The pressure exerted by a mixture of non-reacting ideal gases is the sum of the pressures that each "
           "gas would exert if it alone occupied the container at the same temperature."),
    sp("A"),
    "Molecular velocities and Dalton's law of partial pressures",
    "Molecular motion is random: for every molecule moving one way there is, on average, another moving the "
    "opposite way, so the vector average is zero while the average of v² is not. In kinetic theory each gas in a "
    "mixture contributes (1/3)nm⟨v²⟩ independently, so the partial pressures add (Dalton's law).",
    ["Statement I: random directions → ⟨v⟩ = 0, but ⟨v²⟩ ≠ 0 → true",
     "Statement II: P = P₁ + P₂ + … → true"],
    why="Both statements are standard results of kinetic theory.",
    ncert="Class 11 Physics, 'Kinetic Theory', pressure of an ideal gas (law of partial pressures)", seconds=45)

Tf = (2.5 * 300 + 1.5 * 380) / (2.5 + 1.5)
assert close(Tf, 330) and close((300 + 380) / 2, 340) and close((1.5 * 300 + 2.5 * 380) / 4, 350)
assert close((3.5 * 300 + 2.5 * 380) / 6, 333.33, 1e-3)
add(T, "Degrees of freedom and equipartition", "Advanced", "numerical",
    "One mole of oxygen (rigid diatomic molecules) at 300 K and one mole of helium (monatomic) at 380 K are mixed "
    "in a thermally insulated, rigid container. Treating both as ideal gases and using the law of equipartition "
    "of energy, the final temperature of the mixture is:",
    place("330 K", ["340 K", "350 K", "333 K"], "C"),
    "Energy conservation with equipartition specific heats",
    "No heat enters and no work is done (rigid, insulated container), so the total internal energy is conserved. "
    "The internal energy of each gas is μC_vT, with C_v = (5/2)R for rigid diatomic oxygen and (3/2)R for helium.",
    ["(5/2)R(300) + (3/2)R(380) = [(5/2) + (3/2)]R T_f",
     "750 + 570 = 4T_f → T_f = 330 K"],
    why="340 K is the simple average, ignoring the different specific heats. 350 K swaps the specific heats of the "
        "two gases. 333 K uses C_p instead of C_v, although the container is rigid.",
    ncert="Class 11 Physics, 'Kinetic Theory', law of equipartition of energy and specific heats of gases",
    seconds=80, recomputed=True)

v_ratio = math.sqrt((2 / 1) * (32 / 16))
assert close(v_ratio, 2)
add(T, "Pressure and rms speed", "Advanced", "numerical",
    "Oxygen gas (O₂) at absolute temperature T has an rms molecular speed v. The temperature is raised to 2T, and "
    "at this temperature all the molecules dissociate into oxygen atoms. Treating the gas as ideal, the rms speed "
    "of the oxygen atoms is:",
    place("2v", ["√2 v", "v", "2√2 v"], "A"),
    "Dependence of rms speed on temperature and molar mass",
    "v_rms = √(3RT/M). Doubling T multiplies v_rms by √2; halving the molar mass (O₂ → O, 32 → 16 g/mol) "
    "multiplies it by a further √2.",
    ["v_rms ∝ √(T/M)", "v' = v √(2T/T × 32/16) = v √4 = 2v"],
    why="√2 v accounts for only one of the two changes. v ignores both. 2√2 v takes the molar mass as falling by "
        "a factor of 4.",
    ncert="Class 11 Physics, 'Kinetic Theory', kinetic interpretation of temperature (rms speed)", seconds=60,
    recomputed=True)


# =====================================================================================================================
# Oscillations and Waves (B4 I6 A4)
# =====================================================================================================================
T = "Oscillations and Waves"

lam = 340 / 680
dphi = 2 * math.pi * 0.25 / lam
assert close(lam, 0.5) and close(dphi, math.pi)
add(T, "Progressive waves and wave speed", "Basic", "numerical",
    "A sound wave of frequency 680 Hz travels through air with a speed of 340 m/s. The phase difference between "
    "the oscillations of two points of the air, 25 cm apart along the direction of propagation, is:",
    place("π rad", ["π/2 rad", "2π rad", "π/4 rad"], "B"),
    "Phase difference and path difference in a progressive wave",
    "At a given instant, points separated by Δx along the wave differ in phase by kΔx = 2πΔx/λ.",
    ["λ = v/f = 340/680 = 0.5 m", "Δφ = 2π × 0.25/0.5 = π rad"],
    why="π/2 rad and π/4 rad take the separation as λ/4 or λ/8. 2π rad takes it as a full wavelength.",
    ncert="Class 11 Physics, 'Waves', displacement relation in a progressive wave (phase)", seconds=40,
    recomputed=True)

assert (6 / 2) ** 2 == 9
add(T, "Energy in SHM", "Basic", "numerical",
    "A block attached to a spring oscillates on a smooth horizontal surface. The amplitude of the oscillation is "
    "increased from 2 cm to 6 cm, the block and spring being the same. The total energy of the oscillation "
    "becomes:",
    place("9 times as large", ["3 times as large", "6 times as large", "Unchanged, since the frequency is "
          "unchanged"], "D"),
    "Energy of a simple harmonic oscillator",
    "The total energy of a spring–block oscillator is E = ½kA², so with the same spring it is proportional to the "
    "square of the amplitude.",
    ["E ∝ A²", "E₂/E₁ = (6/2)² = 9"],
    why="3 times assumes E ∝ A. 6 times adds instead of squaring. The frequency is indeed unchanged, but the "
        "energy depends on the amplitude.",
    ncert="Class 11 Physics, 'Oscillations', energy in simple harmonic motion", seconds=30, recomputed=True)

add(T, "Progressive waves and wave speed", "Basic", "direct",
    "The equation y(x, t) = a sin(kx + ωt), where a, k and ω are positive constants, represents a wave travelling:",
    place("Along the negative x-direction with speed ω/k",
          ["Along the positive x-direction with speed ω/k", "Along the negative x-direction with speed k/ω",
           "Nowhere: it is a stationary wave"], "C"),
    "Direction of a travelling wave from its equation",
    "A fixed phase kx + ωt = constant moves so that x decreases as t increases: dx/dt = −ω/k. So the wave travels "
    "along −x with speed ω/k. The form sin(kx − ωt) would travel along +x.",
    ["kx + ωt = constant → dx/dt = −ω/k"],
    why="The positive direction belongs to sin(kx − ωt). k/ω is the reciprocal of the speed. A stationary wave "
        "has a product form such as sin kx cos ωt.",
    ncert="Class 11 Physics, 'Waves', displacement relation in a progressive wave", seconds=30)

add(T, "Superposition and standing waves", "Basic", "assertion_reason",
    AR_STEM.format(
        a="When two waves of the same amplitude arrive at a point exactly in opposite phase, the resultant "
          "displacement at that point is zero.",
        r="According to the principle of superposition, the resultant displacement is the algebraic sum of the "
          "displacements due to the individual waves."),
    ar("A"),
    "Principle of superposition (destructive interference)",
    "In opposite phase the two displacements at every instant are equal in size and opposite in sign, so their "
    "algebraic sum is zero.",
    ["y₁ = a sin ωt, y₂ = a sin(ωt + π) = −a sin ωt", "y = y₁ + y₂ = 0"],
    why="The zero resultant follows directly from adding the displacements, as R states.",
    ncert="Class 11 Physics, 'Waves', the principle of superposition of waves", seconds=35)

assert close(1 / 0.8, 1.25)
add(T, "Superposition and standing waves", "Intermediate", "numerical",
    "A string fixed at both ends vibrates in its fundamental mode. Its vibrating length is reduced by 20%, the "
    "tension and the string being unchanged. Its fundamental frequency:",
    place("Increases by 25%", ["Increases by 20%", "Decreases by 20%", "Increases by about 12%"], "A"),
    "Fundamental frequency of a stretched string",
    "In the fundamental mode λ = 2L, so f = v/(2L). With the same tension and mass per unit length, v is "
    "unchanged and f ∝ 1/L.",
    ["L' = 0.8L", "f'/f = 1/0.8 = 1.25 → increases by 25%"],
    why="20% assumes f changes by the same percentage as L. A decrease would follow from f ∝ L. 12% uses f ∝ "
        "1/√L.",
    ncert="Class 11 Physics, 'Waves', standing waves and normal modes of a string", seconds=45, recomputed=True)

f1, f2 = 400 / 2, 406 / 2
assert f2 - f1 == 3
add(T, "Organ pipes and beats", "Intermediate", "numerical",
    "Two sound waves arriving at a point produce displacements y₁ = a sin(400πt) and y₂ = a sin(406πt), where t is "
    "in seconds. The number of beats heard per second is:",
    place("3", ["6", "1.5", "203"], "C"),
    "Beat frequency",
    "Read each frequency from ω = 2πf. The beat frequency is the difference of the two frequencies, not of the "
    "angular frequencies.",
    ["f₁ = 400π/2π = 200 Hz, f₂ = 406π/2π = 203 Hz", "Beats = 203 − 200 = 3 per second"],
    why="6 subtracts the coefficients 406 − 400 directly (angular frequency/π). 1.5 halves the beat frequency. "
        "203 Hz is the frequency of the second wave.",
    ncert="Class 11 Physics, 'Waves', beats", seconds=40, recomputed=True)

T_K = 273 * 4
assert T_K == 1092 and T_K - 273 == 819
add(T, "Progressive waves and wave speed", "Intermediate", "numerical",
    "At what temperature will the speed of sound in air be twice its value at 0 °C? (Treat air as an ideal gas.)",
    place("819 °C", ["1092 °C", "273 °C", "546 °C"], "D"),
    "Variation of the speed of sound with temperature",
    "For an ideal gas v = √(γRT/M), so v ∝ √T with T in kelvin. Doubling v needs four times the absolute "
    "temperature.",
    ["v₂/v₁ = 2 → T₂ = 4T₁ = 4 × 273 = 1092 K", "1092 − 273 = 819 °C"],
    why="1092 °C forgets to convert back from kelvin. 273 °C (546 K) doubles the absolute temperature, which only "
        "raises v by √2. 546 °C mixes up the scales.",
    ncert="Class 11 Physics, 'Waves', speed of a longitudinal wave (Laplace correction)", seconds=45,
    recomputed=True)

add(T, "Spring and pendulum oscillations", "Intermediate", "statement_pair",
    SP_STEM.format(
        s1="The motion of a simple pendulum is simple harmonic only for small angular displacements.",
        s2="The period of a simple pendulum of fixed length increases when it is taken from the Earth's surface to "
           "the top of a high mountain."),
    sp("A"),
    "Simple pendulum",
    "The restoring torque is −mgL sin θ. Only when sin θ ≈ θ (small angles) is it proportional to the "
    "displacement, which is the condition for SHM. The period T = 2π√(L/g) increases where g is smaller, and g "
    "decreases with height above the surface.",
    ["Statement I: sin θ ≈ θ needed → true", "Statement II: g decreases with height → T increases → true"],
    why="Both statements are correct consequences of T = 2π√(L/g) and its small-angle derivation.",
    ncert="Class 11 Physics, 'Oscillations', the simple pendulum", seconds=45)

xs = {f: math.sin(2 * math.pi * f) for f in (1 / 12, 1 / 8, 1 / 4, 1 / 2)}
assert close(xs[1 / 12], 0.5) and close(xs[1 / 8], 1 / math.sqrt(2)) and close(xs[1 / 4], 1) and abs(xs[1 / 2]) < 1e-9
add(T, "SHM equation and phase", "Intermediate", "match_list",
    match_stem("A particle executes simple harmonic motion x = A sin(2πt/T), where T is the period. Match List-I "
               "(time t) with List-II (displacement x at that time).",
               ["t = T/12", "t = T/8", "t = T/4", "t = T/2"],
               ["Zero", "A/√2", "A/2", "A"]),
    match_options({"A": "III", "B": "II", "C": "IV", "D": "I"},
                  [{"A": "II", "B": "III", "C": "IV", "D": "I"}, {"A": "III", "B": "II", "C": "I", "D": "IV"},
                   {"A": "III", "B": "IV", "C": "II", "D": "I"}], "A"),
    "Displacement and phase in SHM",
    "The phase at time t is 2πt/T. Evaluate sin of the phase at each time.",
    ["T/12: phase π/6 → x = A/2 → III", "T/8: phase π/4 → x = A/√2 → II", "T/4: phase π/2 → x = A → IV",
     "T/2: phase π → x = 0 → I"],
    why="The wrong codes swap T/12 and T/8, or put the extreme position at T/2 instead of T/4.",
    ncert="Class 11 Physics, 'Oscillations', simple harmonic motion (phase)", seconds=60)

truth = [True, True, True, False, False]
multi_key(truth, "abc")
add(T, "Superposition and standing waves", "Intermediate", "multi_statement",
    multi("A stationary (standing) wave is set up on a stretched string fixed at both ends. Which of the following "
          "statements are correct?",
          ["Both fixed ends are nodes.",
           "The frequencies of the normal modes are integral multiples of the fundamental frequency.",
           "The distance between two consecutive nodes is half a wavelength.",
           "All the points between two consecutive nodes oscillate with the same amplitude.",
           "In the fundamental mode, the wavelength equals the length of the string."]),
    place("(a), (b) and (c) only", ["(a), (b), (c) and (d) only", "(a), (c) and (e) only", "(b), (c) and (e) only"],
          "B"),
    "Normal modes of a string fixed at both ends",
    "Fixed ends cannot move, so they are nodes. Fitting a whole number of half-wavelengths into L gives "
    "λₙ = 2L/n and fₙ = nv/(2L), integral multiples of v/2L. Nodes are λ/2 apart. The amplitude 2a|sin kx| varies "
    "from zero at the nodes to a maximum at the antinodes.",
    ["(a) true", "(b) fₙ = n f₁ → true", "(c) true", "(d) amplitude varies with position → false",
     "(e) fundamental: λ = 2L → false"],
    why="Codes with (d) treat a standing wave like a travelling wave of uniform amplitude; codes with (e) forget "
        "that the fundamental is half a wavelength long.",
    ncert="Class 11 Physics, 'Waves', standing waves and normal modes", seconds=60)

m_b, u_b, M_blk, k_ = 0.5, 4, 1.5, 400
V_ = m_b * u_b / (m_b + M_blk)
Amp = V_ / math.sqrt(k_ / (m_b + M_blk))
assert close(1 / math.sqrt(k_ / 1.5), 0.025 * math.sqrt(6)) and close(1 / math.sqrt(k_ / 0.5), 0.025 * math.sqrt(2))
assert close(V_, 1) and close(Amp, 0.05 * math.sqrt(2)) and close(math.sqrt(2 * 0.5 * m_b * u_b ** 2 / k_), 0.1 * math.sqrt(2))
add(T, "Spring and pendulum oscillations", "Advanced", "numerical",
    "A block of mass 1.5 kg rests on a smooth horizontal surface, attached to a light horizontal spring of spring "
    "constant 400 N/m whose other end is fixed. A ball of putty of mass 0.5 kg moving at 4 m/s along the axis of "
    "the spring hits the block and sticks to it. The amplitude of the resulting oscillations is:",
    place("5√2 cm", ["10√2 cm", "2.5√6 cm", "2.5√2 cm"], "C"),
    "SHM after a perfectly inelastic collision",
    "The collision happens at the equilibrium position, so the common velocity just after it is the maximum "
    "velocity of the new oscillation: v_max = Aω, with ω = √(k/(m + M)).",
    ["V = 0.5 × 4/2 = 1 m/s", "ω = √(400/2) = 10√2 rad/s",
     "A = V/ω = 1/(10√2) m = 5√2 cm ≈ 7.1 cm"],
    why="10√2 cm equates the putty's kinetic energy before the collision to ½kA², ignoring the loss in the "
        "inelastic collision. 2.5√6 cm uses only the block's mass (1.5 kg) in ω. 2.5√2 cm uses only the putty's mass "
        "(0.5 kg) in ω.",
    ncert="Class 11 Physics, 'Oscillations', oscillations due to a spring", seconds=90, recomputed=True)

fA, fB, Ls = 300, 400, 1.2
f1 = fB - fA
assert f1 == 100 and fA % f1 == 0 and 2 * Ls * f1 == 240
add(T, "Superposition and standing waves", "Advanced", "numerical",
    "A string 1.2 m long is fixed at both ends. Two successive resonant frequencies of the string are 300 Hz and "
    "400 Hz, with no resonance between them. The speed of transverse waves on the string is:",
    place("240 m/s", ["120 m/s", "480 m/s", "960 m/s"], "D"),
    "Successive harmonics of a string",
    "The normal-mode frequencies are fₙ = n v/(2L). Successive harmonics differ by the fundamental frequency "
    "f₁ = v/(2L).",
    ["f₁ = 400 − 300 = 100 Hz (300 Hz and 400 Hz are the 3rd and 4th harmonics)",
     "v = 2Lf₁ = 2 × 1.2 × 100 = 240 m/s"],
    why="120 m/s uses v = Lf₁. 480 m/s uses v = 4Lf₁, as for a pipe closed at one end. 960 m/s uses 400 Hz as the "
        "fundamental.",
    ncert="Class 11 Physics, 'Waves', standing waves and normal modes", seconds=60, recomputed=True)

f_open = F(100) / (F(3, 2) - 1)
assert f_open == 200
add(T, "Organ pipes and beats", "Advanced", "numerical",
    "A pipe open at both ends has fundamental frequency f. The pipe is now closed at one end, its length being "
    "unchanged. The frequency of the third harmonic of the closed pipe is found to be 100 Hz higher than f. "
    "Neglecting end corrections, f is:",
    place("200 Hz", ["100 Hz", "400 Hz", "300 Hz"], "A"),
    "Harmonics of open and closed pipes",
    "For length L, an open pipe has fundamental v/(2L). A pipe closed at one end has fundamental v/(4L), i.e. f/2, "
    "and only odd harmonics; its third harmonic is 3v/(4L) = 3f/2.",
    ["Closed pipe third harmonic = 3f/2", "3f/2 − f = 100 → f/2 = 100 → f = 200 Hz"],
    why="100 Hz takes the closed pipe's third harmonic as 2f. 400 Hz takes it as 5f/4. 300 Hz is the closed "
        "pipe's third harmonic itself.",
    ncert="Class 11 Physics, 'Waves', standing waves in pipes", seconds=70, recomputed=True)

add(T, "Progressive waves and wave speed", "Advanced", "assertion_reason",
    AR_STEM.format(
        a="At a constant temperature, the speed of sound in an ideal gas increases when the pressure of the gas is "
          "increased.",
        r="At a constant temperature, the ratio P/ρ of the pressure to the density of a given ideal gas remains "
          "constant."),
    ar("D"),
    "Effect of pressure on the speed of sound",
    "v = √(γP/ρ). For an ideal gas P/ρ = RT/M, which depends only on temperature. Raising the pressure at constant "
    "temperature raises the density in the same proportion, so the speed does not change.",
    ["P = ρRT/M → P/ρ = RT/M (constant at fixed T) → R true", "v = √(γP/ρ) → unchanged → A false"],
    why="A is the trap: pressure appears in Laplace's formula, but density changes with it.",
    ncert="Class 11 Physics, 'Waves', speed of a longitudinal wave (Laplace correction)", seconds=50)


# =====================================================================================================================
# Electrostatics (B6 I8 A6)
# =====================================================================================================================
T = "Electrostatics"
k = 9e9

assert 8 / 4 == 2 and 8 * 4 == 32
add(T, "Coulomb's law and superposition", "Basic", "numerical",
    "Two point charges kept a certain distance apart in air repel each other with a force of 8 N. Keeping the "
    "separation unchanged, they are immersed in an oil of dielectric constant 4. The force between them now is:",
    place("2 N", ["32 N", "4 N", "0.5 N"], "B"),
    "Coulomb's law in a dielectric medium",
    "In a medium of dielectric constant K the permittivity is Kε₀, so the Coulomb force between the same charges "
    "at the same separation is reduced by the factor K.",
    ["F_medium = F_air/K = 8/4 = 2 N"],
    why="32 N multiplies by K. 4 N divides by √K. 0.5 N divides by K².",
    ncert="Class 12 Physics, 'Electric Charges and Fields', Coulomb's law (permittivity of a medium)",
    seconds=30, recomputed=True)

U_ = k * 2e-6 * (-3e-6) / 0.3
assert close(U_, -0.18) and close(k * 6e-12 / 0.09, 0.6)
add(T, "Electric potential and energy", "Basic", "numerical",
    "Point charges of +2 μC and −3 μC are held 30 cm apart in air. Taking 1/(4πε₀) = 9 × 10⁹ N m² C⁻² and the "
    "potential energy to be zero at infinite separation, the electrostatic potential energy of the pair is:",
    place("−0.18 J", ["+0.18 J", "−0.6 J", "−0.054 J"], "D"),
    "Potential energy of a system of two point charges",
    "U = q₁q₂/(4πε₀r), with the signs of the charges kept. Unlike charges give a negative potential energy.",
    ["U = 9 × 10⁹ × (2 × 10⁻⁶)(−3 × 10⁻⁶)/0.3", "= −54 × 10⁻³/0.3 = −0.18 J"],
    why="+0.18 J drops the sign of the negative charge. −0.6 J divides by r² (that is the force in newtons, with "
        "a sign). −0.054 J forgets to divide by r.",
    ncert="Class 12 Physics, 'Electrostatic Potential and Capacitance', potential energy of a system of charges",
    seconds=40, recomputed=True)

Cs = 1 / (1 / 2 + 1 / 3 + 1 / 6)
assert close(Cs, 1)
add(T, "Capacitors and dielectrics", "Basic", "numerical",
    "Capacitors of 2 μF, 3 μF and 6 μF are connected in series. Their equivalent capacitance is:",
    place("1 μF", ["11 μF", "2 μF", "0.5 μF"], "D"),
    "Capacitors in series",
    "In series the reciprocals of the capacitances add: 1/C = 1/C₁ + 1/C₂ + 1/C₃. The result is smaller than the "
    "smallest capacitance.",
    ["1/C = 1/2 + 1/3 + 1/6 = (3 + 2 + 1)/6 = 1", "C = 1 μF"],
    why="11 μF is the parallel sum. 2 μF and 0.5 μF do not follow from the series rule (0.5 μF would be 1/C "
        "= 2).",
    ncert="Class 12 Physics, 'Electrostatic Potential and Capacitance', combination of capacitors", seconds=30,
    recomputed=True)

add(T, "Coulomb's law and superposition", "Basic", "match_list",
    match_stem("Match List-I (property or law) with List-II (its statement).",
               ["Additivity of charges", "Quantisation of charge", "Conservation of charge", "Coulomb's law"],
               ["The charge on any body is an integral multiple of e, q = ne",
                "The total charge of an isolated system remains constant",
                "The force between two point charges varies as q₁q₂/r²",
                "The total charge of a system is the algebraic sum of the individual charges"]),
    match_options({"A": "IV", "B": "I", "C": "II", "D": "III"},
                  [{"A": "II", "B": "I", "C": "IV", "D": "III"}, {"A": "IV", "B": "II", "C": "I", "D": "III"},
                   {"A": "I", "B": "IV", "C": "II", "D": "III"}], "C"),
    "Basic properties of electric charge",
    "NCERT lists three basic properties of charge (additivity, conservation and quantisation), and Coulomb's law "
    "gives the force between point charges.",
    ["Additivity → algebraic sum → IV", "Quantisation → q = ne → I", "Conservation → isolated system → II",
     "Coulomb's law → q₁q₂/r² → III"],
    why="The wrong codes swap additivity with conservation, or quantisation with additivity.",
    ncert="Class 12 Physics, 'Electric Charges and Fields', basic properties of electric charge", seconds=40)

add(T, "Electric field and dipole", "Basic", "direct",
    "Which of the following molecules has a permanent electric dipole moment (is a polar molecule)?",
    place("H₂O", ["CO₂", "CH₄", "O₂"], "A"),
    "Polar and non-polar molecules",
    "In a polar molecule the centres of positive and negative charge do not coincide even without an external "
    "field. NCERT gives water (H₂O) as an example. In CO₂ and CH₄ the centres coincide because of the symmetry of "
    "the molecule, and O₂ is a symmetric molecule of two identical atoms; these are non-polar.",
    ["H₂O: bent molecule → charge centres separated → polar",
     "CO₂ (linear), CH₄ (symmetric), O₂ (identical atoms) → non-polar"],
    why="CO₂ and CH₄ are NCERT's examples of non-polar molecules; O₂ has no charge separation either.",
    ncert="Class 12 Physics, 'Electric Charges and Fields', physical significance of dipoles", seconds=30)

add(T, "Capacitors and dielectrics", "Basic", "assertion_reason",
    AR_STEM.format(
        a="The capacitance of a parallel plate capacitor increases when the separation between its plates is "
          "decreased.",
        r="The energy stored in a capacitor of capacitance C carrying a charge Q is Q²/(2C)."),
    ar("B"),
    "Capacitance of a parallel plate capacitor",
    "C = ε₀A/d, so a smaller separation d gives a larger capacitance; A is true. R is a correct formula for the "
    "stored energy, but it is about a different property of the capacitor and says nothing about how C depends "
    "on d.",
    ["C = ε₀A/d → d decreases → C increases (A true)", "U = Q²/2C (R true, but unrelated to A)"],
    why="R does not mention the plate separation at all, so it cannot explain A.",
    ncert="Class 12 Physics, 'Electrostatic Potential and Capacitance', the parallel plate capacitor", seconds=35)

F_each = k * 4e-6 * 1e-6 / 0.1 ** 2
assert close(F_each, 3.6) and close(2 * F_each, 7.2)
add(T, "Coulomb's law and superposition", "Intermediate", "numerical",
    "A charge of +4 μC is fixed at x = 0 and a charge of −4 μC at x = 0.2 m on the x-axis, in air. A charge of "
    "+1 μC is placed at x = 0.1 m. Taking 1/(4πε₀) = 9 × 10⁹ N m² C⁻², the net force on the +1 μC charge is:",
    place("7.2 N, along +x", ["Zero", "3.6 N, along +x", "7.2 N, along −x"], "D"),
    "Superposition of Coulomb forces",
    "The +4 μC charge repels the +1 μC charge towards +x, and the −4 μC charge attracts it, also towards +x. The "
    "two forces are equal in size and in the same direction, so they add.",
    ["Each force = 9 × 10⁹ × 4 × 10⁻⁶ × 1 × 10⁻⁶/(0.1)² = 3.6 N", "Both along +x → F = 7.2 N along +x"],
    why="Zero treats the two forces as opposite, as they would be for two like charges. 3.6 N counts only one "
        "charge. −x reverses both forces.",
    ncert="Class 12 Physics, 'Electric Charges and Fields', forces between multiple charges", seconds=50,
    recomputed=True)

q_drop = 3.2e-15 * 10 / 1e5
n_e = q_drop / 1.6e-19
assert close(n_e, 2)
add(T, "Electric field and dipole", "Intermediate", "numerical",
    "A tiny oil drop of mass 3.2 × 10⁻¹⁵ kg is held stationary in air by a uniform vertical electric field of "
    "magnitude 1 × 10⁵ N/C. The drop carries excess electrons. Taking g = 10 m/s², e = 1.6 × 10⁻¹⁹ C and "
    "neglecting buoyancy, the number of excess electrons on the drop is:",
    place("2", ["1", "4", "20"], "B"),
    "Balance of electric and gravitational forces; quantisation of charge",
    "For the drop to stay at rest, the electric force qE must balance its weight mg. (Since the drop is negatively "
    "charged, the field must point downward to give an upward force.) The charge is then a whole number of "
    "electronic charges.",
    ["q = mg/E = 3.2 × 10⁻¹⁵ × 10/10⁵ = 3.2 × 10⁻¹⁹ C", "n = q/e = 3.2 × 10⁻¹⁹/1.6 × 10⁻¹⁹ = 2"],
    why="1 and 4 come from slips of a factor of 2 (dropping or doubling e). 20 forgets g = 10 in mg.",
    ncert="Class 12 Physics, 'Electric Charges and Fields', electric field and quantisation of charge",
    seconds=55, recomputed=True)

V_s, R_s = 3000, 0.2
assert close(V_s / R_s, 1.5e4) and close(V_s / R_s ** 2, 7.5e4)
add(T, "Gauss's law", "Intermediate", "numerical",
    "A thin spherical conducting shell of radius 20 cm, in air, is charged so that its potential is 3000 V (zero "
    "at infinity). The magnitude of the electric field just outside its surface is:",
    place("1.5 × 10⁴ V/m", ["600 V/m", "Zero", "7.5 × 10⁴ V/m"], "A"),
    "Field and potential of a charged spherical shell",
    "Outside the shell, by Gauss's law, the field and potential are those of a point charge Q at the centre: "
    "E = kQ/r² and V = kQ/r. At the surface (r = R) they are related by E = V/R.",
    ["V = kQ/R and E = kQ/R² → E = V/R", "E = 3000/0.2 = 1.5 × 10⁴ V/m"],
    why="600 V/m multiplies V by R. Zero is the field inside the shell, not just outside it. 7.5 × 10⁴ V/m "
        "divides by R².",
    ncert="Class 12 Physics, 'Electric Charges and Fields', applications of Gauss's law (thin spherical shell)",
    seconds=50, recomputed=True)

eps0 = 8.85e-12
E_ = 1000 / 1e-3
u_ = 0.5 * eps0 * E_ ** 2
assert close(u_, 4.425) and close(0.5 * eps0 * 1000 ** 2, 4.425e-6)
add(T, "Capacitors and dielectrics", "Intermediate", "numerical",
    "A parallel plate capacitor with air between its plates, which are 1 mm apart, is charged to a potential "
    "difference of 1000 V. Taking ε₀ = 8.85 × 10⁻¹² C² N⁻¹ m⁻², the energy stored per unit volume in the field "
    "between the plates is about:",
    place("4.4 J/m³", ["8.9 J/m³", "4.4 × 10⁻⁶ J/m³", "4.4 × 10⁻³ J/m³"], "A"),
    "Energy density of an electric field",
    "Between the plates the field is uniform, E = V/d, and the energy density is u = ½ε₀E².",
    ["E = 1000/(1 × 10⁻³) = 1 × 10⁶ V/m", "u = ½ × 8.85 × 10⁻¹² × 10¹² ≈ 4.4 J/m³"],
    why="8.9 J/m³ drops the ½. 4.4 × 10⁻⁶ J/m³ uses E = 1000 V/m (d in mm). 4.4 × 10⁻³ J/m³ is a powers-of-ten "
        "slip in E.",
    ncert="Class 12 Physics, 'Electrostatic Potential and Capacitance', energy stored in a capacitor (energy "
          "density)", seconds=50, recomputed=True)

V_ring = k * 1e-9 / math.hypot(0.3, 0.4)
assert close(V_ring, 18) and close(k * 1e-9 / 0.4, 22.5) and close(k * 1e-9 / 0.3, 30)
add(T, "Electric potential and energy", "Intermediate", "numerical",
    "A charge of 1 nC is uniformly distributed over a thin ring of radius 0.3 m, in air. Taking "
    "1/(4πε₀) = 9 × 10⁹ N m² C⁻² and the potential to be zero at infinity, the electric potential at a point on "
    "the axis of the ring, 0.4 m from its centre, is:",
    place("18 V", ["22.5 V", "30 V", "Zero"], "C"),
    "Potential due to a system of charges",
    "Potential is a scalar, so the contributions of all the elements of the ring simply add. Every element is at "
    "the same distance √(R² + x²) from a point on the axis, so the ring acts like its whole charge at that "
    "distance.",
    ["Distance of every element = √(0.3² + 0.4²) = 0.5 m", "V = 9 × 10⁹ × 10⁻⁹/0.5 = 18 V"],
    why="22.5 V uses the axial distance 0.4 m. 30 V uses the radius 0.3 m. Zero confuses the potential with the "
        "field at the centre of the ring.",
    ncert="Class 12 Physics, 'Electrostatic Potential and Capacitance', potential due to a system of charges",
    seconds=50, recomputed=True)

add(T, "Capacitors and dielectrics", "Intermediate", "statement_pair",
    SP_STEM.format(
        s1="When two charged conductors are connected by a conducting wire, charge flows between them until their "
           "potentials become equal.",
        s2="When a dielectric slab is placed in a uniform external electric field, equal and opposite surface "
           "charges are induced on its two faces."),
    sp("A"),
    "Conductors in contact; polarisation of a dielectric",
    "Charges in a conductor move from higher to lower potential energy until the whole connected conductor is at "
    "one potential, so the flow stops when the two potentials are equal. A dielectric in a field becomes "
    "polarised; inside, the dipoles cancel, leaving surface charge densities +σₚ and −σₚ on the two faces, whose "
    "field opposes the external field.",
    ["Statement I: flow stops at equal potential → true",
     "Statement II: polarisation → ±σₚ on opposite faces → true"],
    why="Both are NCERT descriptions of conductors and dielectrics.",
    ncert="Class 12 Physics, 'Electrostatic Potential and Capacitance', conductors and dielectrics (polarisation)",
    seconds=45)

add(T, "Gauss's law", "Intermediate", "match_list",
    match_stem("Match List-I (situation) with List-II (electric flux through the stated surface). The charges are "
               "in vacuum.",
               ["A point charge q at the centre of a cube: flux through the whole cube",
                "A point charge q at the centre of a cube: flux through one face",
                "A point charge q at one corner of a cube: flux through the whole cube",
                "An electric dipole lying entirely inside a closed surface: flux through that surface"],
               ["q/(6ε₀)", "Zero", "q/ε₀", "q/(8ε₀)"]),
    match_options({"A": "III", "B": "I", "C": "IV", "D": "II"},
                  [{"A": "III", "B": "IV", "C": "I", "D": "II"}, {"A": "I", "B": "III", "C": "IV", "D": "II"},
                   {"A": "III", "B": "I", "C": "II", "D": "IV"}], "D"),
    "Gauss's law and symmetry",
    "The total flux through a closed surface is q_enclosed/ε₀. A charge at the centre of a cube sends equal flux "
    "through the six faces. A charge at a corner is shared by eight cubes that meet there, so one cube gets 1/8 of "
    "the total. A dipole has zero net charge.",
    ["A: q/ε₀ → III", "B: q/(6ε₀) → I", "C: q/(8ε₀) → IV", "D: net charge 0 → zero flux → II"],
    why="The wrong codes swap the face flux with the corner case, or give a dipole a non-zero flux.",
    ncert="Class 12 Physics, 'Electric Charges and Fields', Gauss's law", seconds=60)

C1, C2 = 2.0, 6.0
Vser = 8.0
Q_ = Vser / (1 / C1 + 1 / C2)
U1, U2 = Q_ ** 2 / (2 * C1), Q_ ** 2 / (2 * C2)
assert U1 > U2 and 0.5 * C2 * Vser ** 2 > 0.5 * C1 * Vser ** 2
truth = [True, True, False, False, True]
multi_key(truth, "abe")
add(T, "Capacitors and dielectrics", "Intermediate", "multi_statement",
    multi("Two capacitors of different capacitances are charged by connecting them to a battery, first in parallel "
          "and then, separately, in series. Which of the following statements are correct?",
          ["In parallel, the charges on the capacitors are in the ratio of their capacitances.",
           "In series, the potential differences across the capacitors are in the inverse ratio of their "
           "capacitances.",
           "The equivalent capacitance of the parallel combination is less than the smaller capacitance.",
           "In series, the capacitor of larger capacitance stores more energy.",
           "In parallel, the capacitor of larger capacitance stores more energy."]),
    place("(a), (b) and (e) only", ["(a), (b) and (d) only", "(b), (c) and (e) only", "(a), (b), (d) and (e) only"],
          "B"),
    "Charge, voltage and energy in series and parallel combinations",
    "In parallel the voltage is common, so Q = CV ∝ C and U = ½CV² ∝ C. In series the charge is common, so "
    "V = Q/C ∝ 1/C and U = Q²/(2C) ∝ 1/C: the smaller capacitor stores more. The parallel equivalent is the sum, "
    "larger than either capacitance.",
    ["(a) Q ∝ C → true", "(b) V ∝ 1/C → true", "(c) C_p = C₁ + C₂ → false",
     "(d) series: U = Q²/2C → smaller C stores more → false", "(e) parallel: U = ½CV² → larger C stores more → true"],
    why="Codes with (d) apply ½CV² to the series case, where V is not common; codes with (c) use the series rule "
        "for a parallel combination.",
    ncert="Class 12 Physics, 'Electrostatic Potential and Capacitance', combination of capacitors and energy "
          "stored", seconds=80)

truth = [True, True, True, False, True]
multi_key(truth, "abce")
add(T, "Coulomb's law and superposition", "Advanced", "multi_statement",
    multi("Which of the following statements about electrostatic forces and fields are correct?",
          ["The force between two point charges is not changed by the presence of a third charge nearby.",
           "The electrostatic force between two point charges acts along the line joining them.",
           "Coulomb's law in its simple form applies to point charges, i.e. charged bodies whose sizes are small "
           "compared with the distance between them.",
           "The electric field produced by a point charge at a given point depends on the size of the small test "
           "charge used to measure it.",
           "Two unequal point charges exert forces of equal magnitude on each other."]),
    place("(a), (b), (c) and (e) only", ["(b), (c) and (e) only", "(a), (b), (d) and (e) only",
          "(a), (b), (c), (d) and (e)"], "A"),
    "Coulomb's law and the superposition principle",
    "By the superposition principle, the force between any two charges is unaffected by other charges; the net "
    "force on a charge is the vector sum of these pair forces. Coulomb forces are central and obey Newton's third "
    "law whatever the sizes of the charges. The field E = F/q is a property of the source charge alone; the test "
    "charge only measures it.",
    ["(a) superposition → true", "(b) central force → true", "(c) point charges → true",
     "(d) E = F/q is independent of q → false", "(e) third law → true"],
    why="(b), (c) and (e) only leaves out the superposition statement (a), which students often doubt; codes with "
        "(d) make the field depend on the probe.",
    ncert="Class 12 Physics, 'Electric Charges and Fields', Coulomb's law, forces between multiple charges and "
          "electric field", seconds=75)

C0, V0, K_ = 10e-6, 20, 3
dQ = (K_ - 1) * C0 * V0
dU = 0.5 * (K_ - 1) * C0 * V0 ** 2
assert close(dQ, 400e-6) and close(dU, 4e-3) and close(dQ * V0, 8e-3)
add(T, "Capacitors and dielectrics", "Advanced", "numerical",
    "A 10 μF air-filled parallel plate capacitor remains connected to a 20 V battery. A dielectric slab of "
    "dielectric constant 3 is inserted so that it completely fills the space between the plates. The extra charge "
    "drawn from the battery and the increase in the energy stored in the capacitor are respectively:",
    place("400 μC and 4 mJ", ["400 μC and 8 mJ", "Zero and 4 mJ", "600 μC and 6 mJ"], "C"),
    "Dielectric inserted at constant potential difference",
    "With the battery connected, V stays 20 V while C becomes KC₀. The charge and the stored energy (½CV²) both "
    "become K times as large. The battery does work (ΔQ)V, twice the increase in stored energy; the rest goes "
    "into pulling the slab in.",
    ["C: 10 → 30 μF; Q: 200 → 600 μC → ΔQ = 400 μC",
     "U: ½ × 10 × 10⁻⁶ × 400 = 2 mJ → 6 mJ → ΔU = 4 mJ"],
    why="8 mJ is the work done by the battery, not the increase in stored energy. 'Zero' treats the charge as "
        "fixed, which holds only with the battery disconnected. 600 μC and 6 mJ are the final values, not the "
        "changes.",
    ncert="Class 12 Physics, 'Electrostatic Potential and Capacitance', effect of dielectric on capacitance and "
          "energy stored", seconds=90, recomputed=True)

KE0 = 0.5 * 1e-3 * 6 ** 2
r_min = k * 1e-6 * 2e-6 / KE0
assert close(KE0, 0.018) and close(r_min, 1) and close(k * 2e-12 / (2 * KE0), 0.5)
add(T, "Electric potential and energy", "Advanced", "numerical",
    "A point charge of +2 μC is held fixed. A small particle of mass 1 g carrying a charge of +1 μC is projected "
    "straight towards it from a very large distance with a speed of 6 m/s. Taking 1/(4πε₀) = 9 × 10⁹ N m² C⁻² and "
    "neglecting gravity, the distance of closest approach between them is:",
    place("1 m", ["0.5 m", "2 m", "0.1 m"], "B"),
    "Conservation of energy with electrostatic potential energy",
    "As the particle approaches, its kinetic energy is converted into electrostatic potential energy. At the "
    "closest approach it is momentarily at rest, so all its initial kinetic energy has become q₁q₂/(4πε₀r).",
    ["Initial KE = ½ × 10⁻³ × 6² = 0.018 J", "0.018 = 9 × 10⁹ × 2 × 10⁻⁶ × 1 × 10⁻⁶/r = 0.018/r",
     "r = 1 m"],
    why="0.5 m uses mv² instead of ½mv² for the kinetic energy. 2 m halves the potential energy. 0.1 m is a "
        "powers-of-ten slip.",
    ncert="Class 12 Physics, 'Electrostatic Potential and Capacitance', potential energy of a system of charges",
    seconds=80, recomputed=True)

a_sq, q_ = 0.3, 1e-6
pts = {(0, 0): q_, (a_sq, 0): q_, (a_sq, a_sq): -q_, (0, a_sq): -q_}
cx = cy = a_sq / 2
Ex = Ey = 0.0
for (px, py), qq in pts.items():
    dx, dy = cx - px, cy - py
    rr = math.hypot(dx, dy)
    Ex += k * qq * dx / rr ** 3
    Ey += k * qq * dy / rr ** 3
E_c = math.hypot(Ex, Ey)
assert close(E_c, 4 * math.sqrt(2) * 1e5)
add(T, "Electric field and dipole", "Advanced", "numerical",
    "Four point charges are placed at the corners of a square ABCD of side 0.3 m, in air: +1 μC at A and at B, and "
    "−1 μC at C and at D (A, B, C, D taken in order round the square). Taking 1/(4πε₀) = 9 × 10⁹ N m² C⁻², the "
    "magnitude of the electric field at the centre of the square is:",
    place("4√2 × 10⁵ N/C", ["2√2 × 10⁵ N/C", "Zero", "8 × 10⁵ N/C"], "C"),
    "Superposition of electric fields",
    "Each charge is at a distance a/√2 from the centre and produces a field kq/(a²/2) = 2kq/a². Opposite corners "
    "carry opposite charges, so along each diagonal the two fields point the same way and add. The two diagonal "
    "resultants are perpendicular.",
    ["Each field = 2 × 9 × 10⁹ × 10⁻⁶/0.09 = 2 × 10⁵ N/C",
     "Along diagonal AC: 2 × 2 × 10⁵ = 4 × 10⁵ N/C; along BD: 4 × 10⁵ N/C",
     "Resultant = √2 × 4 × 10⁵ = 4√2 × 10⁵ ≈ 5.7 × 10⁵ N/C"],
    why="2√2 × 10⁵ N/C counts only one charge on each diagonal. Zero would be correct only if all four "
        "charges were equal. 8 × 10⁵ N/C adds the four fields as if they were parallel.",
    ncert="Class 12 Physics, 'Electric Charges and Fields', electric field due to a system of charges",
    seconds=100, recomputed=True)

add(T, "Electric potential and energy", "Advanced", "statement_pair",
    SP_STEM.format(
        s1="When a positive charge moves in the direction of an electrostatic field, the potential energy of the "
           "system decreases.",
        s2="When a negative charge moves opposite to the direction of an electrostatic field, the potential energy "
           "of the system increases."),
    sp("C"),
    "Sign of the change in electrostatic potential energy",
    "The potential decreases along the field. A change in potential energy is ΔU = qΔV. A positive charge moving "
    "along E goes to lower V, so ΔU < 0. A negative charge moving against E goes to higher V (ΔV > 0), and with "
    "q < 0 this gives ΔU < 0: its potential energy also decreases, the field doing positive work on it.",
    ["Statement I: q > 0, ΔV < 0 → ΔU < 0 → true",
     "Statement II: q < 0, ΔV > 0 → ΔU < 0 (decreases) → false"],
    why="Statement II forgets that the sign of the charge reverses the sign of ΔU; a negative charge naturally "
        "moves against the field, just as a positive one moves along it.",
    ncert="Class 12 Physics, 'Electrostatic Potential and Capacitance', electrostatic potential and potential "
          "energy", seconds=55)

r_of_V = lambda V: k * 1e-9 / V
assert r_of_V(30) - r_of_V(45) < r_of_V(15) - r_of_V(30)
add(T, "Electric potential and energy", "Advanced", "assertion_reason",
    AR_STEM.format(
        a="For an isolated point charge, equipotential surfaces drawn for equal steps of potential get farther "
          "apart as one moves away from the charge.",
        r="The magnitude of the electric field, which equals the rate of fall of potential with distance, "
          "decreases with distance from the charge, so a given step of potential needs a larger radial distance."),
    ar("A"),
    "Spacing of equipotential surfaces",
    "The equipotentials of a point charge are spheres with V = kq/r. Since |E| = |dV/dr|, the radial gap needed for "
    "a fixed ΔV is about ΔV/|E|, which grows as E = kq/r² weakens. For example, with kq = 9 V m the surfaces of "
    "45 V, 30 V and 15 V lie at 0.2 m, 0.3 m and 0.6 m.",
    ["|E| = ΔV/Δr → Δr = ΔV/|E|", "E ∝ 1/r² falls with r → Δr grows → A"],
    why="R gives the exact reason for the widening spacing, so it explains A.",
    ncert="Class 12 Physics, 'Electrostatic Potential and Capacitance', equipotential surfaces and the relation "
          "between field and potential", seconds=60)


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
    doc = {"schema_version": "1.0", "batch_id": "BATCH_005", "created_at": TODAY,
           "notes": "BATCH_005 package PHY_005_p1: 127 original Physics questions (Physics and Measurement through "
                    "Electrostatics). Every numerical answer is re-derived in tools/batch_005/PHY_005_p1.py.",
           "stimuli": [], "questions": QUESTIONS}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {OUT}: {n} questions, {dict(Counter(x['difficulty'] for x in QUESTIONS))}")
    print(f"keys {dict(sorted(keys.items()))}")
    print(f"formats {dict(fmts)}")
