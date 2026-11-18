"""Writes batches/parts/BATCH_004_PHY_p1.json: package PHY_004_p1 of BATCH_004 (130 Physics questions).

Topics: Physics and Measurement, Kinematics, Laws of Motion, Work Energy and Power, Rotational Motion, Gravitation,
Properties of Solids and Liquids, Thermodynamics, Kinetic Theory of Gases, Oscillations and Waves, Electrostatics.
IDs NEET_PHY_000751 .. NEET_PHY_000880, in the order the questions are listed below.

Every computable answer is re-derived with an assert before the file is written, and so is the plan quota. If any
assert fails, nothing is written. Each question's answer position is chosen by hand and fixed.

    python tools/batch_004/PHY_004_p1.py        (run from docs/neet-bank)
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
OUT = ROOT / "batches" / "parts" / "BATCH_004_PHY_p1.json"
PLAN = ROOT / "batches" / "plans" / "BATCH_004_plan.json"
PACKAGE = "PHY_004_p1"
TODAY = "2026-11-16"
LETTERS = "ABCD"
PHY = "Physics"
RECOMPUTED = ("script:recompute", "ai:author-solve", "ai:self-recheck")
AUTHORED = ("ai:author-solve", "ai:self-recheck")
FIRST_ID = 751

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
# Physics and Measurement (B2 I3 A2)
# =====================================================================================================================
T = "Physics and Measurement"

assert dims() == (0, 0, 0)                                    # plane angle = arc/radius
assert dims(t=-1) != (0, 0, 0)                                # angular velocity
add(T, "Units and SI system", "Basic", "direct",
    "Which of the following quantities has a unit but is dimensionless?",
    place("Plane angle", ["Strain", "Relative density", "Angular velocity"], "A"),
    "Dimensionless quantities that carry a unit",
    "Plane angle is defined as arc length divided by radius, a ratio of two lengths, so it has no dimensions. Yet "
    "SI gives it a unit, the radian, so that angles can be stated unambiguously.",
    ["Plane angle = arc/radius = [L]/[L] → dimensionless, unit radian (rad)",
     "Strain = ΔL/L → dimensionless, no unit", "Relative density = density/density of water → no unit",
     "Angular velocity = angle/time → [T⁻¹], unit rad/s"],
    why="Strain and relative density are ratios of like quantities with no unit at all. Angular velocity has a "
        "unit but also has dimensions [T⁻¹], because the time in its denominator is not cancelled.",
    ncert="Class 11 Physics, 'Units and Measurement', the international system of units (plane angle and solid "
          "angle)", seconds=30)

assert 1000 * 100 ** 2 == 10 ** 7                             # 1 kg m² s⁻² in g cm² s⁻²
assert 5 * 10 ** 7 == 50_000_000
add(T, "Units and SI system", "Basic", "numerical",
    "The CGS unit of energy is the erg (1 erg = 1 g cm² s⁻²). An energy of 5 J, expressed in ergs, is:",
    place("5 × 10⁷ erg", ["5 × 10⁵ erg", "5 × 10³ erg", "5 × 10⁻⁷ erg"], "A"),
    "Conversion between SI and CGS units",
    "Write the joule in base units, 1 J = 1 kg m² s⁻², and replace each base unit by its CGS equivalent: "
    "1 kg = 10³ g and 1 m = 10² cm, so 1 m² = 10⁴ cm².",
    ["1 J = (10³ g)(10² cm)² s⁻² = 10³ × 10⁴ g cm² s⁻² = 10⁷ erg",
     "5 J = 5 × 10⁷ erg"],
    why="5 × 10⁵ erg converts metres to centimetres without squaring (10³ × 10²). 5 × 10³ erg converts only the "
        "kilogram. 5 × 10⁻⁷ erg uses the factor upside down.",
    ncert="Class 11 Physics, 'Units and Measurement', dimensional formulae and conversion of units", seconds=40,
    recomputed=True)

r = 1.20
V_sphere = 4 / 3 * 3.1416 * r ** 3
assert close(V_sphere, 7.2382, 1e-4) and f"{V_sphere:.3g}" == "7.24"
add(T, "Least count and significant figures", "Intermediate", "numerical",
    "The radius of a small sphere is measured as 1.20 cm. Taking π = 3.1416, its volume V = (4/3)πr³, written with "
    "the correct number of significant figures, is:",
    place("7.24 cm³", ["7.238 cm³", "7.2 cm³", "7.2382 cm³"], "D"),
    "Significant figures in multiplication",
    "In a product the result keeps as many significant figures as the least precise measured factor. The radius "
    "1.20 cm has three significant figures (the trailing zero after the decimal point counts). The numbers 4/3 and "
    "π are exact or taken to more figures, so they do not limit the result.",
    ["r³ = 1.20³ = 1.728 cm³", "V = (4/3) × 3.1416 × 1.728 = 7.238 cm³",
     "Radius has 3 significant figures → V = 7.24 cm³"],
    why="7.238 cm³ and 7.2382 cm³ keep more figures than the radius justifies. 7.2 cm³ treats 1.20 as having only "
        "two significant figures, ignoring the significant trailing zero.",
    ncert="Class 11 Physics, 'Units and Measurement', significant figures (rules for arithmetic operations)",
    seconds=60, recomputed=True)

D_ETA = dmul(dims(1, 1, -2), dinv(dims(l=2)), dims(t=1))          # F/(A × velocity gradient) = stress × time
D_G = dmul(dims(1, 1, -2), dims(l=2), dinv(dims(m=2)))           # F r²/m²
D_POWER = dmul(dims(1, 2, -2), dims(t=-1))
assert D_ETA == (1, -1, -1) and D_G == (-1, 3, -2) and D_POWER == (1, 2, -3)
add(T, "Dimensional analysis", "Intermediate", "match_list",
    match_stem("Match List-I (physical quantity) with List-II (its dimensional formula). K denotes the dimension of "
               "temperature.",
               ["Coefficient of viscosity", "Universal gravitational constant G", "Power",
                "Specific heat capacity"],
               ["[M⁻¹ L³ T⁻²]", "[M L⁻¹ T⁻¹]", "[L² T⁻² K⁻¹]", "[M L² T⁻³]"]),
    match_options({"A": "II", "B": "I", "C": "IV", "D": "III"},
                  [{"A": "II", "B": "I", "C": "III", "D": "IV"}, {"A": "IV", "B": "I", "C": "II", "D": "III"},
                   {"A": "II", "B": "III", "C": "IV", "D": "I"}], "B"),
    "Dimensional formulae of derived quantities",
    "Write each quantity from its defining relation. Viscosity: F = ηA(dv/dx), so η = stress × time. G: "
    "F = Gm₁m₂/r², so G = Fr²/m². Power = work/time. Specific heat capacity = heat/(mass × temperature change).",
    ["η = [M L⁻¹ T⁻²][T] = [M L⁻¹ T⁻¹] → II", "G = [M L T⁻²][L²]/[M²] = [M⁻¹ L³ T⁻²] → I",
     "Power = [M L² T⁻²]/[T] = [M L² T⁻³] → IV", "c = [M L² T⁻²]/([M][K]) = [L² T⁻² K⁻¹] → III"],
    why="The other codes swap power with specific heat (only specific heat contains K), give viscosity the "
        "dimensions of power, or give G the dimensions of specific heat.",
    ncert="Class 11 Physics, 'Units and Measurement', dimensions of physical quantities", seconds=70)

add(T, "Least count and significant figures", "Intermediate", "assertion_reason",
    AR_STEM.format(
        a="Writing a measured length of 2.308 cm as 0.02308 m does not change the number of significant figures "
          "in it.",
        r="In a number less than one, the zeros to the left of the first non-zero digit are not significant."),
    ar("A"),
    "Significant figures and change of units",
    "A change of units only shifts the decimal point. The zeros it introduces in 0.02308 m stand to the left of the "
    "first non-zero digit, and such zeros only locate the decimal point, so they are not significant. Both forms "
    "therefore have the same four significant figures (2, 3, 0, 8).",
    ["2.308 cm → significant figures 2, 3, 0, 8 → four",
     "0.02308 m → leading zeros not significant → still four", "R is the rule that keeps the count unchanged"],
    why="R is exactly why the extra zeros do not add significant figures, so it explains A.",
    ncert="Class 11 Physics, 'Units and Measurement', significant figures", seconds=45)

D_V, D_TT = dims(l=1, t=-1), dims(t=1)
D_a = dmul(D_V, dinv(D_TT))
D_b = dmul(D_V, D_TT)
assert D_a == (0, 1, -2) and D_b == (0, 1, 0)
add(T, "Dimensional analysis", "Advanced", "direct",
    "The velocity v of a particle at time t is given by v = at + b/(t + c), where a, b and c are constants. The "
    "dimensions of a, b and c are respectively:",
    place("[L T⁻²], [L] and [T]",
          ["[L T⁻²], [L T⁻¹] and [T]", "[L T⁻¹], [L] and [T]", "[L T⁻²], [L] and [T⁻¹]"], "D"),
    "Principle of homogeneity of dimensions",
    "Only quantities of the same dimensions can be added. So c, which is added to t, must be a time. Each term on "
    "the right must have the dimensions of velocity: at gives a = v/t, and b/(t + c) gives b = v × time.",
    ["c added to t → [c] = [T]", "[at] = [L T⁻¹] → [a] = [L T⁻²]",
     "[b]/[T] = [L T⁻¹] → [b] = [L]"],
    why="[L T⁻¹] for b gives b itself the dimensions of velocity, forgetting that it is divided by a time. "
        "[L T⁻¹] for a forgets that a is multiplied by t. [T⁻¹] for c would mean adding a frequency to a time.",
    ncert="Class 11 Physics, 'Units and Measurement', checking the dimensional consistency of equations",
    seconds=60)

truth = [True, False, True, False, True]
multi_key(truth, "ace")
add(T, "Dimensional analysis", "Advanced", "multi_statement",
    multi("Which of the following statements are correct?",
          ["Relative density has neither a unit nor dimensions.",
           "The dimensional formula of a physical quantity in the SI system differs from its dimensional formula "
           "in the CGS system.",
           "Two physical quantities with different dimensions cannot be added to or subtracted from each other.",
           "The numerical value of a measured physical quantity is the same in every system of units.",
           "In a physically correct formula, the argument of a trigonometric or exponential function must be "
           "dimensionless."]),
    place("(a), (c) and (e) only", ["(a), (b) and (c) only", "(c), (d) and (e) only", "(a), (c), (d) and (e) only"],
          "C"),
    "Dimensions, units and homogeneity",
    "Relative density is a ratio of two densities. Dimensions describe how a quantity depends on the base "
    "quantities (mass, length, time), not on the size of the units, so they are the same in SI and CGS. Only like "
    "quantities can be added. The numerical value n of a quantity changes with the unit u, since nu stays constant. "
    "sin θ, e^x and similar functions are defined for pure numbers only.",
    ["(a) ratio of like quantities → true", "(b) e.g. force is [M L T⁻²] in both systems → false",
     "(c) homogeneity principle → true", "(d) 5 J = 5 × 10⁷ erg: n changes with u → false",
     "(e) e.g. y = A sin(kx − ωt): kx and ωt are pure numbers → true"],
    why="Codes with (b) mix up units with dimensions; codes with (d) forget that a smaller unit gives a larger "
        "numerical value.",
    ncert="Class 11 Physics, 'Units and Measurement', dimensions and dimensional analysis", seconds=80)


# =====================================================================================================================
# Kinematics (B4 I5 A4)
# =====================================================================================================================
T = "Kinematics"


def cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


assert cross((2, 3, 0), (1, 4, 0)) == (0, 0, 5) and cross((1, 4, 0), (2, 3, 0)) == (0, 0, -5)
assert 2 * 1 + 3 * 4 == 14
add(T, "Vectors", "Basic", "numerical",
    "For the vectors A = 2î + 3ĵ and B = î + 4ĵ, the vector product A × B is:",
    place("5k̂", ["−5k̂", "11k̂", "14k̂"], "B"),
    "Vector product in component form",
    "Use î × ĵ = k̂, ĵ × î = −k̂ and î × î = ĵ × ĵ = 0. For vectors in the x–y plane, "
    "A × B = (AₓB_y − A_yBₓ)k̂.",
    ["A × B = (2î + 3ĵ) × (î + 4ĵ) = 8(î × ĵ) + 3(ĵ × î)", "= 8k̂ − 3k̂ = 5k̂"],
    why="−5k̂ is B × A; the vector product is not commutative. 11k̂ adds the two cross terms, forgetting that "
        "ĵ × î = −k̂. 14k̂ uses the scalar-product value 2 × 1 + 3 × 4 as a vector.",
    ncert="Class 11 Physics, 'Motion in a Plane', and the appendix on vectors (vector product)", seconds=45,
    recomputed=True)

s_acc = 0.5 * 20 * 4
s_const = 20 * 6
assert s_acc == 40 and s_const == 120 and s_acc + s_const == 160
add(T, "Graphs of motion", "Basic", "numerical",
    "The velocity–time graph of a car moving along a straight road is a straight line rising uniformly from 0 to "
    "20 m/s in the first 4 s, followed by a horizontal line at 20 m/s for the next 6 s. The displacement of the car "
    "in these 10 s is:",
    place("160 m", ["200 m", "120 m", "100 m"], "C"),
    "Displacement as the area under a velocity–time graph",
    "The area between a velocity–time graph and the time axis gives the displacement. Split it into a triangle (the "
    "accelerating part) and a rectangle (the constant-velocity part).",
    ["Triangle: ½ × 4 s × 20 m/s = 40 m", "Rectangle: 6 s × 20 m/s = 120 m", "Total = 40 + 120 = 160 m"],
    why="200 m assumes 20 m/s for all 10 s. 120 m counts only the constant-velocity part. 100 m takes the whole "
        "area as one triangle, ½ × 10 × 20.",
    ncert="Class 11 Physics, 'Motion in a Straight Line', kinematic equations and velocity–time graphs",
    seconds=40, recomputed=True)

T_circ = 2 * math.pi * 2 / 4
assert close(T_circ, math.pi)
add(T, "Uniform circular motion", "Basic", "numerical",
    "A particle moves along a circle of radius 2 m with a constant speed of 4 m/s. The time it takes to complete one "
    "revolution is:",
    place("π s", ["16π s", "π/2 s", "4π s"], "A"),
    "Period of uniform circular motion",
    "In one revolution the particle covers the circumference 2πr at constant speed v, so T = 2πr/v. Equivalently "
    "ω = v/r and T = 2π/ω.",
    ["T = 2πr/v = 2π × 2/4 = π s", "Check: ω = v/r = 2 rad/s → T = 2π/2 = π s"],
    why="16π s multiplies the circumference by the speed (2πrv) instead of dividing. π/2 s uses half the "
        "circumference, πr/v. 4π s uses 2πv/r, with r and v interchanged.",
    ncert="Class 11 Physics, 'Motion in a Plane', uniform circular motion", seconds=35, recomputed=True)

add(T, "Graphs of motion", "Basic", "direct",
    "A particle starts from rest and moves along a straight line with a constant acceleration. Its position–time "
    "graph is:",
    place("A parabola", ["A straight line inclined to the time axis", "A straight line parallel to the time axis",
                         "A rectangular hyperbola"], "D"),
    "Shape of the position–time graph for uniform acceleration",
    "With u = 0 and constant a, x = ½at², a quadratic function of time. The graph of x against t is therefore a "
    "parabola whose slope (the velocity) increases steadily.",
    ["x = ut + ½at² with u = 0 → x = ½at²", "x ∝ t² → parabola"],
    why="An inclined straight line is the position–time graph of uniform velocity. A line parallel to the time axis "
        "means the particle is at rest. A rectangular hyperbola would mean xt = constant.",
    ncert="Class 11 Physics, 'Motion in a Straight Line', position–time graph for uniformly accelerated motion",
    seconds=25)

# a = 6t from rest at the origin → v = 3t², x = t³
assert 3 * 2 ** 2 == 12 and 2 ** 3 == 8
assert 0.5 * (6 * 2) * 2 ** 2 == 24 and 2 * 2 ** 3 == 16
add(T, "Motion in a straight line", "Intermediate", "numerical",
    "A particle starts from rest at the origin and moves along the x-axis with an acceleration a = 6t, where a is "
    "in m/s² and t in seconds. Its position at t = 2 s is:",
    place("8 m", ["12 m", "24 m", "16 m"], "A"),
    "Non-uniform acceleration: integrate twice",
    "When the acceleration changes with time, the equations of uniformly accelerated motion do not apply. "
    "Integrate a(t) to get v(t) and v(t) to get x(t), using v = 0 and x = 0 at t = 0.",
    ["v = ∫6t dt = 3t² (v = 0 at t = 0)", "x = ∫3t² dt = t³ (x = 0 at t = 0)", "At t = 2 s: x = 8 m"],
    why="12 m is the velocity at t = 2 s (in m/s), not the position. 24 m applies s = ½at² with the final "
        "acceleration 12 m/s², which is valid only for constant acceleration. 16 m drops the ½ in the first "
        "integration (v = 6t²).",
    ncert="Class 11 Physics, 'Motion in a Straight Line', instantaneous velocity and acceleration", seconds=60,
    recomputed=True)

u = math.sqrt(10 * 10 * 2 * 2)          # H = u²/(4g) at 45° = 10 m → u² = 400
H45 = u ** 2 * math.sin(math.radians(45)) ** 2 / (2 * 10)
R45 = u ** 2 / 10
assert close(H45, 10) and close(R45, 40) and close(R45 / H45, 4)
add(T, "Projectile motion", "Intermediate", "numerical",
    "A ball is projected from level ground at the angle that gives the greatest horizontal range for its speed of "
    "projection. It rises to a maximum height of 10 m. Neglecting air resistance, its horizontal range is:",
    place("40 m", ["20 m", "10 m", "80 m"], "D"),
    "Relation between range and maximum height at 45°",
    "The range u² sin 2θ/g is greatest at θ = 45°. At this angle H = u² sin²45°/(2g) = u²/(4g) and R = u²/g, so "
    "R = 4H.",
    ["θ = 45° for maximum range", "H = u²/(4g), R = u²/g → R = 4H", "R = 4 × 10 = 40 m"],
    why="20 m takes R = 2H. 10 m takes R = H, which holds at tan θ = 4, not at 45°. 80 m takes R = 8H.",
    ncert="Class 11 Physics, 'Motion in a Plane', projectile motion", seconds=50, recomputed=True)

add(T, "Uniform circular motion", "Intermediate", "assertion_reason",
    AR_STEM.format(
        a="A body moving with a constant speed can have a non-zero acceleration.",
        r="Acceleration is defined as the rate of change of speed."),
    ar("C"),
    "Acceleration with constant speed",
    "Acceleration is the rate of change of velocity, a vector. If a body keeps its speed but turns (as in uniform "
    "circular motion), its velocity changes, so it has an acceleration, directed towards the centre for circular "
    "motion. If acceleration were the rate of change of speed, A would be impossible.",
    ["A: e.g. uniform circular motion has a = v²/r ≠ 0 at constant speed → true",
     "R: acceleration = dv/dt (velocity, not speed) → false"],
    why="R is false: defining acceleration through speed alone would make every constant-speed motion "
        "unaccelerated, contradicting A.",
    ncert="Class 11 Physics, 'Motion in a Plane', uniform circular motion", seconds=40)

add(T, "Vectors", "Intermediate", "statement_pair",
    SP_STEM.format(
        s1="The magnitude of the vector product of two vectors is equal to the area of the triangle having the two "
           "vectors as adjacent sides.",
        s2="The vector product of any vector with itself is the null vector."),
    sp("D"),
    "Geometrical meaning of the vector product",
    "|A × B| = AB sin θ is the area of the parallelogram with A and B as adjacent sides; the triangle on the same two "
    "sides has half that area. For A × A, θ = 0 and sin 0 = 0, so the product is the null vector.",
    ["Statement I: |A × B| = parallelogram area = 2 × triangle area → false",
     "Statement II: |A × A| = A² sin 0° = 0 → true"],
    why="Statement I is the trap: the triangle has only half the area given by |A × B|.",
    ncert="Class 11 Physics, 'Motion in a Plane', and the appendix on vectors (vector product)", seconds=40)

th = math.radians(30)
u0, g = 20, 10
assert close(2 * u0 * math.sin(th) / g, 2) and close(u0 ** 2 * math.sin(th) ** 2 / (2 * g), 5)
assert close(u0 ** 2 * math.sin(2 * th) / g, 20 * math.sqrt(3))
add(T, "Projectile motion", "Intermediate", "match_list",
    match_stem("A particle is projected from level ground with speed u at an angle θ above the horizontal. Neglect "
               "air resistance. Match List-I (quantity) with List-II (expression).",
               ["Time of flight", "Maximum height", "Horizontal range",
                "Vertical height y at horizontal distance x (equation of the path)"],
               ["u² sin 2θ/g", "x tan θ − gx²/(2u² cos² θ)", "2u sin θ/g", "u² sin² θ/(2g)"]),
    match_options({"A": "III", "B": "IV", "C": "I", "D": "II"},
                  [{"A": "III", "B": "I", "C": "IV", "D": "II"}, {"A": "IV", "B": "III", "C": "I", "D": "II"},
                   {"A": "I", "B": "IV", "C": "III", "D": "II"}], "B"),
    "Standard results for projectile motion",
    "Treat the horizontal motion as uniform (uₓ = u cos θ) and the vertical motion as uniformly decelerated "
    "(u_y = u sin θ, acceleration −g). Eliminating t from x = u cos θ t and y = u sin θ t − ½gt² gives the parabolic "
    "path.",
    ["Time of flight: y = 0 again at t = 2u sin θ/g → III", "Maximum height: v_y = 0 → H = u² sin² θ/(2g) → IV",
     "Range = u cos θ × 2u sin θ/g = u² sin 2θ/g → I", "Path: y = x tan θ − gx²/(2u² cos² θ) → II"],
    why="The other codes swap the range with the maximum height, or the time of flight with the range or with the "
        "height; only the time of flight has dimensions of time.",
    ncert="Class 11 Physics, 'Motion in a Plane', projectile motion", seconds=60)

R_c = 40
T1T2 = 2 * R_c / 10
th_a = 0.5 * math.asin(R_c * 10 / 30 ** 2)          # check with u = 30 m/s
t1, t2 = 2 * 30 * math.sin(th_a) / 10, 2 * 30 * math.cos(th_a) / 10
assert close(T1T2, 8) and close(t1 * t2, 8)
add(T, "Projectile motion", "Advanced", "numerical",
    "Two balls are projected from the same point on level ground with the same speed but at different angles of "
    "projection, and both land at the same point 40 m away. Taking g = 10 m/s² and neglecting air resistance, the "
    "product of their times of flight is:",
    place("8 s²", ["4 s²", "16 s²", "2 s²"], "B"),
    "Complementary angles of projection",
    "For the same speed, two angles give the same range only if they are complementary, θ and 90° − θ. Their times "
    "of flight are 2u sin θ/g and 2u cos θ/g. Their product is 4u² sin θ cos θ/g² = 2(u² sin 2θ/g)/g = 2R/g, "
    "independent of the unknown speed and angle.",
    ["Angles θ and 90° − θ", "T₁T₂ = (2u sin θ/g)(2u cos θ/g) = 2R/g", "T₁T₂ = 2 × 40/10 = 8 s²"],
    shortcut="T₁T₂ = 2R/g for complementary angles.",
    why="4 s² takes T₁T₂ = R/g, using sin 2θ = sin θ cos θ. 16 s² takes 4R/g, forgetting that 2 sin θ cos θ = "
        "sin 2θ. 2 s² takes R/(2g).",
    ncert="Class 11 Physics, 'Motion in a Plane', projectile motion", seconds=90, recomputed=True)

t_cross = 100 / 5
drift = 4 * t_cross
assert t_cross == 20 and drift == 80
add(T, "Relative velocity", "Advanced", "numerical",
    "A river 100 m wide flows with a uniform speed of 4 m/s. A swimmer whose speed relative to still water is 5 m/s "
    "wants to cross it in the least possible time. How far downstream from the point directly opposite her starting "
    "point does she land?",
    place("80 m", ["133 m", "125 m", "0 m"], "A"),
    "River crossing in the shortest time",
    "The time to cross depends only on the component of her velocity across the river. It is least when she heads "
    "straight across (perpendicular to the flow), so t = width/5. During this time the current carries her "
    "downstream at 4 m/s.",
    ["Head perpendicular to the banks: t = 100/5 = 20 s", "Drift = river speed × t = 4 × 20 = 80 m"],
    why="133 m takes the speed across as √(5² − 4²) = 3 m/s (t = 100/3 s), which is the cross-component for a "
        "heading partly upstream, not for the quickest crossing. 125 m uses width × 5/4, inverting the ratio. 0 m "
        "would need her to head partly upstream, which takes longer.",
    seconds=70, recomputed=True)

add(T, "Relative velocity", "Advanced", "statement_pair",
    SP_STEM.format(
        s1="Two particles are projected at the same instant from the same point with different velocities. "
           "Neglecting air resistance, the velocity of one particle relative to the other stays constant during "
           "their flight.",
        s2="Two particles are projected at the same instant from the same point with different velocities. "
           "Neglecting air resistance, the path of one particle as seen from the other is a parabola."),
    sp("C"),
    "Relative motion of two projectiles",
    "Both particles have the same acceleration g, so the relative acceleration is g − g = 0. Their relative velocity "
    "therefore never changes, and a body moving with constant velocity relative to an observer moves along a "
    "straight line as seen by that observer.",
    ["Relative acceleration = g − g = 0 → relative velocity constant → Statement I true",
     "Constant relative velocity, starting from the same point → straight-line relative path → Statement II false"],
    why="Statement II is the trap: each path is a parabola as seen from the ground, but the relative path is a "
        "straight line.",
    seconds=60)

truth = [True, True, True, False, True]
multi_key(truth, "abce")
add(T, "Relative velocity", "Advanced", "multi_statement",
    multi("A train moves along a straight level track with a constant velocity. A passenger standing in it lets a "
          "ball drop from rest (relative to the train) from his hand. Neglecting air resistance, which of the "
          "following statements are correct?",
          ["To the passenger, the ball falls along a vertical straight line.",
           "To an observer standing on the ground beside the track, the ball moves along a parabola.",
           "The acceleration of the ball is g, directed vertically downward, for both observers.",
           "The horizontal velocity of the ball relative to the ground is zero while it falls.",
           "The ball lands on the floor of the train at the point vertically below the passenger's hand."]),
    place("(a), (b), (c) and (e) only",
          ["(a), (b) and (c) only", "(b), (c) and (d) only", "(a), (c), (d) and (e) only"], "B"),
    "Motion seen from two inertial frames",
    "When released, the ball keeps the train's horizontal velocity v relative to the ground. Relative to the "
    "train its initial velocity is zero. The train does not accelerate, so both frames measure the same "
    "acceleration g downward.",
    ["(a) train frame: starts from rest, acceleration g → vertical line → true",
     "(b) ground frame: horizontal velocity v plus vertical acceleration g → parabola → true",
     "(c) the frames differ by a constant velocity → same acceleration → true",
     "(d) the ball keeps the train's horizontal velocity → false",
     "(e) ball and train move forward equally → lands directly below the hand → true"],
    why="Codes with (d) assume the ball loses the train's horizontal velocity when released; codes without (e) "
        "or (a) assume the ball falls behind the passenger.",
    seconds=80)


# =====================================================================================================================
# Laws of Motion (B4 I5 A4)
# =====================================================================================================================
T = "Laws of Motion"

J_trap = 0.5 * 100 * 0.1 + 100 * 0.2 + 0.5 * 100 * 0.1
assert close(J_trap, 30) and close(100 * 0.4, 40) and close(100 * 0.2, 20) and close(2 * 0.5 * 100 * 0.1, 10)
add(T, "Newton's laws and impulse", "Basic", "numerical",
    "A force acting on a body along a fixed direction rises uniformly from 0 to 100 N in 0.1 s, stays at 100 N for "
    "the next 0.2 s, and then falls uniformly to 0 in a further 0.1 s. The impulse of the force on the body is:",
    place("30 N s", ["40 N s", "20 N s", "10 N s"], "A"),
    "Impulse as the area under a force–time graph",
    "Impulse is ∫F dt, the area under the force–time graph. Here the graph is a trapezium: two triangles of base "
    "0.1 s and a rectangle of base 0.2 s, all of height 100 N.",
    ["Rising triangle: ½ × 0.1 × 100 = 5 N s", "Flat part: 0.2 × 100 = 20 N s",
     "Falling triangle: ½ × 0.1 × 100 = 5 N s", "Impulse = 5 + 20 + 5 = 30 N s"],
    why="40 N s takes the force as 100 N for the whole 0.4 s. 20 N s counts only the flat part. 10 N s counts only "
        "the two sloping parts.",
    ncert="Class 11 Physics, 'Laws of Motion', impulse", seconds=40, recomputed=True)

a_pull = 20 * math.cos(math.radians(60)) / 2
assert close(a_pull, 5) and 20 * math.sin(math.radians(60)) < 2 * 10      # block stays on the floor
add(T, "Newton's laws and impulse", "Basic", "numerical",
    "A block of mass 2 kg rests on a smooth horizontal floor. It is pulled by a force of 20 N directed at 60° above "
    "the horizontal. Taking g = 10 m/s², the acceleration of the block along the floor is:",
    place("5 m/s²", ["10 m/s²", "5√3 m/s²", "Zero, because the force is not directed along the floor"], "D"),
    "Newton's second law with a resolved force",
    "Only the horizontal component F cos 60° accelerates the block along the smooth floor. The vertical component "
    "(10√3 ≈ 17.3 N) is less than the weight (20 N), so the block stays on the floor and the normal reaction "
    "balances the rest of the weight.",
    ["Horizontal component = 20 cos 60° = 10 N", "a = 10/2 = 5 m/s²"],
    why="10 m/s² uses the whole 20 N. 5√3 m/s² uses the vertical component 20 sin 60°. 'Zero' forgets that an "
        "inclined force still has a horizontal component that accelerates the block.",
    ncert="Class 11 Physics, 'Laws of Motion', Newton's second law of motion", seconds=40, recomputed=True)

F_h = 5 * 10 * math.tan(math.radians(30))
assert close(F_h, 50 / math.sqrt(3)) and close(F_h * math.cos(math.radians(30)), 5 * 10 * math.sin(math.radians(30)))
add(T, "Equilibrium of concurrent forces", "Intermediate", "numerical",
    "A block of mass 5 kg is held at rest on a smooth plane inclined at 30° to the horizontal by a horizontal force "
    "F. Taking g = 10 m/s², the magnitude of F is:",
    place("50/√3 N", ["25 N", "50√3 N", "25√3 N"], "C"),
    "Equilibrium of three concurrent forces",
    "Three forces act on the block: its weight mg, the normal reaction (perpendicular to the plane, no friction) and "
    "the horizontal force F. Resolve along the incline, where the normal reaction has no component.",
    ["Along the incline: F cos 30° = mg sin 30°", "F = mg tan 30° = 50 × (1/√3) = 50/√3 N ≈ 28.9 N"],
    why="25 N is mg sin 30°, the force needed if it were applied along the incline. 50√3 N uses mg/tan 30°. 25√3 N "
        "is mg cos 30°, the component of the weight perpendicular to the incline.",
    ncert="Class 11 Physics, 'Laws of Motion', equilibrium of a particle", seconds=60, recomputed=True)

m1, m2 = 2, 3
a_inc = (m2 * 10 - m1 * 10 * 0.5) / (m1 + m2)
assert close(a_inc, 4)
add(T, "Newton's laws and impulse", "Intermediate", "numerical",
    "A block of mass 2 kg lies on a smooth plane inclined at 30° to the horizontal. It is tied to a light "
    "inextensible string that runs parallel to the incline, over a smooth light pulley at the top of the incline, "
    "and carries a block of mass 3 kg hanging vertically. The system is released from rest. Taking g = 10 m/s², the "
    "acceleration of the blocks is:",
    place("4 m/s²", ["6 m/s²", "2 m/s²", "20/3 m/s²"], "B"),
    "Connected bodies on an incline",
    "The hanging weight (30 N) pulls the system one way; the component of the 2 kg block's weight along the incline "
    "(mg sin 30° = 10 N) pulls the other way. The net force accelerates the total mass of 5 kg.",
    ["Driving force = 3 × 10 = 30 N", "Opposing force = 2 × 10 × sin 30° = 10 N",
     "a = (30 − 10)/(2 + 3) = 4 m/s² (hanging block moves down)"],
    why="6 m/s² ignores the component of the 2 kg block's weight along the incline (30/5). 2 m/s² subtracts the "
        "full weight 20 N of the 2 kg block. 20/3 m/s² divides the net force by the hanging mass alone.",
    ncert="Class 11 Physics, 'Laws of Motion', solving problems in mechanics", seconds=70, recomputed=True)

F_wall = 2 * 10 / 0.5
assert close(F_wall, 40) and close(0.5 * F_wall, 2 * 10)
add(T, "Friction", "Intermediate", "numerical",
    "A block of mass 2 kg is held against a rough vertical wall by pressing it with a horizontal force F. The "
    "coefficient of static friction between the block and the wall is 0.5. Taking g = 10 m/s², the least value of F "
    "that keeps the block from sliding down is:",
    place("40 N", ["10 N", "20 N", "Any force, however small, since the wall is rough"], "D"),
    "Limiting friction on a vertical wall",
    "F presses the block into the wall, so the normal reaction is N = F. The vertical friction must balance the "
    "weight, and friction can be at most μN. So μF ≥ mg.",
    ["N = F", "Need μN ≥ mg → 0.5F ≥ 20 N", "F_min = 20/0.5 = 40 N"],
    why="10 N is μmg, which treats the weight as the normal force. 20 N equals the weight but ignores that "
        "friction is only μ times the normal force. A rough wall can supply friction only in proportion to how hard "
        "the block is pressed, so a very small F is not enough.",
    ncert="Class 11 Physics, 'Laws of Motion', friction", seconds=50, recomputed=True)

m, rr, v, s, c = 1000, 20, 10, 0.6, 0.8
f_bank = m * 10 * s - (m * v ** 2 / rr) * c
N_bank = m * 10 * c + (m * v ** 2 / rr) * s
assert close(f_bank, 2000) and N_bank > 0
# check both equations: vertical and horizontal (towards centre)
assert close(N_bank * c + f_bank * s, m * 10) and close(N_bank * s - f_bank * c, m * v ** 2 / rr)
assert v ** 2 < rr * 10 * s / c                         # below the no-friction speed → friction up the slope
add(T, "Circular motion: level and banked roads", "Advanced", "numerical",
    "A car of mass 1000 kg goes round a circular curve of radius 20 m, banked at an angle θ with sin θ = 0.6 and "
    "cos θ = 0.8, at a steady speed of 10 m/s. The road is rough enough that the car does not slip. Taking "
    "g = 10 m/s², the friction force exerted by the road on the car is:",
    place("2000 N, directed up the slope", ["2000 N, directed down the slope", "6000 N, directed up the slope",
                                            "1000 N, directed up the slope"], "A"),
    "Friction on a banked road below the optimum speed",
    "With no friction the speed would have to satisfy v₀² = rg tan θ = 20 × 10 × 0.75 = 150, so v₀ ≈ 12.2 m/s. "
    "The car is slower than this, so it tends to slide down the slope and friction acts up the slope. Resolving "
    "along the slope: the component of the weight down the slope minus friction must supply the component of the "
    "centripetal force along the slope.",
    ["Required centripetal force = mv²/r = 1000 × 100/20 = 5000 N (horizontal, towards the centre)",
     "Along the slope: mg sin θ − f = (mv²/r) cos θ", "f = 10000 × 0.6 − 5000 × 0.8 = 6000 − 4000 = 2000 N",
     "f is positive → up the slope (check: N = mg cos θ + (mv²/r) sin θ = 11000 N)"],
    why="'Down the slope' is the direction only above the optimum speed. 6000 N is just mg sin θ, ignoring the "
        "centripetal requirement. 1000 N subtracts mv²/r without resolving it along the slope.",
    seconds=120, recomputed=True)

mu, mt, mb, Fp = 0.2, 1, 3, 20
f_max = mu * mt * 10
a_common = Fp / (mt + mb)
assert mb * a_common > f_max                            # common motion would need more friction than available
a_lower, a_upper = f_max / mb, (Fp - f_max) / mt
assert close(a_lower, 2 / 3) and close(a_upper, 18)
add(T, "Friction", "Advanced", "numerical",
    "A block P of mass 1 kg rests on top of a block Q of mass 3 kg, which lies on a frictionless horizontal floor. "
    "The coefficient of friction (static and kinetic) between P and Q is 0.2. A horizontal force of 20 N is applied "
    "to P. Taking g = 10 m/s², the acceleration of Q is:",
    place("2/3 m/s²", ["5 m/s²", "18 m/s²", "2 m/s²"], "C"),
    "Checking for slipping between stacked blocks",
    "First test whether the blocks can move together. Together they would have a = 20/4 = 5 m/s², and Q would then "
    "need a friction force 3 × 5 = 15 N from P. The friction between them can be at most μm_Pg = 2 N, so P slips "
    "over Q. Q is then driven only by the kinetic friction of 2 N.",
    ["Common acceleration test: Q would need 15 N > 2 N available → slipping",
     "Friction on Q = 0.2 × 1 × 10 = 2 N (forward)", "a_Q = 2/3 m/s² (and a_P = (20 − 2)/1 = 18 m/s²)"],
    why="5 m/s² assumes the blocks move together without checking the friction limit. 18 m/s² is the acceleration "
        "of P. 2 m/s² divides the friction force by the mass of P instead of Q.",
    seconds=110, recomputed=True)

add(T, "Friction", "Basic", "direct",
    "For the same pair of materials and the same normal force, how does rolling friction compare with sliding "
    "(kinetic) friction?",
    place("Rolling friction is much smaller than sliding friction",
          ["Rolling friction is much larger than sliding friction",
           "Rolling friction is exactly equal to sliding friction",
           "Rolling friction is zero for every real body"], "B"),
    "Rolling friction",
    "When a body rolls, the contact is momentarily at rest and the surfaces deform only slightly near the contact. "
    "The opposing force that results is much smaller than the friction when one surface slides over the other; "
    "this is why wheels and ball bearings reduce friction.",
    ["Rolling friction ≪ sliding friction", "Application: ball bearings, wheels"],
    why="Real bodies and surfaces deform a little, so rolling friction is small but not zero; it is never larger "
        "than or equal to sliding friction in ordinary cases.",
    ncert="Class 11 Physics, 'Laws of Motion', rolling friction", seconds=25)

add(T, "Newton's laws and impulse", "Basic", "match_list",
    match_stem("Match List-I (observation) with List-II (the law or idea that best explains it).",
               ["Dust comes out of a hanging carpet when it is beaten with a stick",
                "A swimmer moves forward by pushing the water backward with her arms",
                "A loaded truck needs a larger braking force than an empty one to stop in the same time from the same "
                "speed",
                "A man standing inside a closed box resting on a frictionless floor cannot set the box moving by "
                "pushing on its inside walls"],
               ["Newton's third law", "Total momentum of a system changes only under an external force",
                "Inertia of rest (Newton's first law)", "Force equals rate of change of momentum (Newton's second law)"]),
    match_options({"A": "III", "B": "I", "C": "IV", "D": "II"},
                  [{"A": "I", "B": "III", "C": "IV", "D": "II"}, {"A": "III", "B": "I", "C": "II", "D": "IV"},
                   {"A": "IV", "B": "I", "C": "III", "D": "II"}], "C"),
    "Applications of Newton's laws",
    "The carpet moves when struck but the dust, by inertia, stays behind. The swimmer pushes water back and the "
    "water pushes her forward (action–reaction). A loaded truck has more momentum at the same speed, so stopping it "
    "in the same time needs a larger force. Forces between the man and the box are internal to the man–box system, "
    "so they cannot change its total momentum.",
    ["A → inertia of rest → III", "B → action and reaction → I", "C → F = Δp/Δt → IV",
     "D → internal forces only → total momentum stays zero → II"],
    why="The other codes swap the carpet and the swimmer, or the truck and the box: the truck is about the force "
        "needed for a given momentum change, the box about the absence of an external force.",
    ncert="Class 11 Physics, 'Laws of Motion', Newton's laws of motion", seconds=60)

add(T, "Newton's laws and impulse", "Intermediate", "assertion_reason",
    AR_STEM.format(
        a="A light body and a heavy body, both initially at rest, are acted on by equal constant forces for the same "
          "time interval. At the end of the interval they have equal linear momenta.",
        r="The impulse of a force, the product of the force and the time for which it acts, is equal to the change "
          "in linear momentum of the body."),
    ar("A"),
    "Impulse–momentum theorem",
    "Equal forces acting for equal times give equal impulses FΔt. Since impulse equals the change in momentum and "
    "both start from rest, both end with the same momentum FΔt; only their speeds differ (the lighter body moves "
    "faster).",
    ["Impulse on each = FΔt", "Δp = FΔt and initial p = 0 → final p equal for both"],
    why="R is the very law that gives equal momenta, so it explains A.",
    ncert="Class 11 Physics, 'Laws of Motion', Newton's second law and impulse", seconds=45)

add(T, "Friction", "Intermediate", "match_list",
    match_stem("A block of mass m rests on a rough surface; μₛ and μₖ are the coefficients of static and kinetic "
               "friction. Match List-I (situation) with List-II (magnitude of the friction force on the block).",
               ["The block lies on a horizontal floor and no horizontal force acts on it",
                "The block lies on a horizontal floor and stays at rest under a horizontal pull F smaller than "
                "μₛmg",
                "The block slides along a horizontal floor",
                "The block rests on an incline of angle θ, smaller than the angle of repose"],
               ["μₖmg", "mg sin θ", "Zero", "F"]),
    match_options({"A": "III", "B": "IV", "C": "I", "D": "II"},
                  [{"A": "III", "B": "I", "C": "IV", "D": "II"}, {"A": "IV", "B": "III", "C": "I", "D": "II"},
                   {"A": "III", "B": "IV", "C": "II", "D": "I"}], "D"),
    "Static and kinetic friction",
    "Static friction is self-adjusting: it is only as large as needed to prevent relative motion, up to μₛN. With "
    "nothing trying to move the block it is zero; under a pull F it equals F; on an incline it balances mg sin θ. "
    "Once the block slides, kinetic friction μₖN acts, with N = mg on a horizontal floor.",
    ["A: no tendency to slide → 0 → III", "B: balances the pull → F → IV",
     "C: kinetic friction = μₖmg → I", "D: balances the weight component along the incline → mg sin θ → II"],
    why="The other codes give a resting block the limiting or kinetic value, or give the sliding block the value "
        "for the incline; friction on a resting body is not μN unless motion is just about to start.",
    ncert="Class 11 Physics, 'Laws of Motion', friction", seconds=60)

mu_s = 0.5
F_min_ang = mu_s * 10 / math.sqrt(1 + mu_s ** 2)
F_horiz = mu_s * 10
assert F_min_ang < F_horiz                                                 # pulling at tan θ = μ beats a level pull
for deg in (10, 20, 30, 40):                                               # F(θ) = μmg/(cos θ + μ sin θ) is least at tan θ = μ
    th_ = math.radians(deg)
    assert mu_s * 10 / (math.cos(th_) + mu_s * math.sin(th_)) >= F_min_ang - 1e-9
add(T, "Friction", "Advanced", "statement_pair",
    SP_STEM.format(
        s1="A block rests on a rough horizontal floor (coefficient of static friction μ). If it is pulled by a force "
           "directed at an angle θ above the horizontal, the force needed to just start it sliding is least when "
           "tan θ = μ.",
        s2="For a given pair of surfaces and a given normal reaction, the kinetic friction is larger when the area of "
           "contact is larger."),
    sp("C"),
    "Pulling at an angle; laws of friction",
    "At the point of sliding, F cos θ = μ(mg − F sin θ), so F = μmg/(cos θ + μ sin θ). The denominator is greatest, "
    "and F least, when tan θ = μ; then F_min = μmg/√(1 + μ²). Kinetic friction is μₖN and, to a good approximation, "
    "does not depend on the area of contact.",
    ["Statement I: dF/dθ = 0 at tan θ = μ → true",
     "Statement II: friction is independent of the apparent area of contact → false"],
    why="Statement II is the common misconception that wider tyres or blocks slide with more friction.",
    ncert="Class 11 Physics, 'Laws of Motion', friction", seconds=90)

truth = [True, True, False, True, False]
multi_key(truth, "abd")
add(T, "Conservation of linear momentum", "Advanced", "multi_statement",
    multi("Which of the following statements are correct?",
          ["Internal forces between the particles of a system cannot change the total linear momentum of the "
           "system.",
           "When a shell at rest explodes into fragments, the vector sum of the momenta of the fragments just after "
           "the explosion is zero.",
           "If no external force acts on a system, its total kinetic energy must also remain constant.",
           "A shell moving under gravity alone explodes in mid-air; until the first fragment hits the ground, the "
           "centre of mass of the fragments continues along the shell's original parabolic path.",
           "The linear momentum of a body stays constant whenever its kinetic energy stays constant."]),
    place("(a), (b) and (d) only", ["(a), (b), (c) and (d) only", "(a), (d) and (e) only", "(b), (c) and (e) only"],
          "B"),
    "Conservation of linear momentum",
    "Internal forces occur in equal and opposite pairs (third law), so they cancel in the total momentum. An "
    "explosion uses only internal forces. Kinetic energy, however, can change through internal forces (chemical "
    "energy is released in an explosion). The centre of mass moves under the net external force (gravity) only, so "
    "its path is unchanged. In uniform circular motion KE is constant but the momentum changes direction.",
    ["(a) internal forces cancel in pairs → true", "(b) initial momentum zero, only internal forces → true",
     "(c) explosion raises KE with no external force → false",
     "(d) centre of mass accelerates at g as before → true", "(e) uniform circular motion is a counter-example → false"],
    why="Codes with (c) confuse conservation of momentum with conservation of kinetic energy; codes with (e) treat "
        "momentum as a scalar.",
    ncert="Class 11 Physics, 'Laws of Motion', conservation of momentum", seconds=90)


# =====================================================================================================================
# Work, Energy and Power (B3 I5 A3)
# =====================================================================================================================
T = "Work, Energy and Power"

W_fx = 10 * 2 + 0.5 * 2 * 10
assert W_fx == 30 and 10 * 4 == 40
add(T, "Work by constant and variable force", "Basic", "numerical",
    "A force acting along the x-axis on a particle has a constant value of 10 N from x = 0 to x = 2 m, and then "
    "decreases uniformly to zero at x = 4 m. The work done by the force as the particle moves from x = 0 to x = 4 m "
    "is:",
    place("30 J", ["40 J", "20 J", "10 J"], "B"),
    "Work as the area under a force–displacement graph",
    "For a force along the displacement, W = ∫F dx, which is the area under the F–x graph: a rectangle from 0 to 2 m "
    "and a triangle from 2 m to 4 m.",
    ["Rectangle: 10 N × 2 m = 20 J", "Triangle: ½ × 2 m × 10 N = 10 J", "W = 20 + 10 = 30 J"],
    why="40 J takes the force as 10 N over the whole 4 m. 20 J counts only the constant part, and 10 J only the "
        "decreasing part.",
    ncert="Class 11 Physics, 'Work, Energy and Power', work done by a variable force", seconds=40, recomputed=True)

P_climb = 60 * 10 * (20 * 0.25) / 10
assert P_climb == 300 and 60 * 10 * 0.25 / 10 == 15 and 60 * 20 * 0.25 / 10 == 30
add(T, "Power", "Basic", "numerical",
    "A man of mass 60 kg runs up a staircase of 20 steps, each 25 cm high, in 10 s. Taking g = 10 m/s², the average "
    "power he develops in raising his body is:",
    place("300 W", ["15 W", "30 W", "30 kW"], "D"),
    "Average power",
    "The work done against gravity is mgh, where h is the total height climbed. Average power is this work divided "
    "by the time taken.",
    ["h = 20 × 0.25 m = 5 m", "W = mgh = 60 × 10 × 5 = 3000 J", "P = 3000/10 = 300 W"],
    why="15 W uses the height of one step only. 30 W leaves out g (uses mh/t). 30 kW takes each step as 25 m.",
    ncert="Class 11 Physics, 'Work, Energy and Power', power", seconds=40, recomputed=True)

add(T, "Power", "Basic", "direct",
    "The horsepower, a unit of power still used for engines and motors, is equal to about:",
    place("746 W", ["1000 W", "100 W", "3.6 × 10⁶ W"], "A"),
    "Units of power",
    "The SI unit of power is the watt (1 W = 1 J/s). The horsepower is an older unit used for automobile engines and "
    "motors, and 1 hp = 746 W.",
    ["1 hp = 746 W"],
    why="1000 W is a kilowatt, not a horsepower. 3.6 × 10⁶ is the number of joules in a kilowatt hour, a unit of "
        "energy. 100 W is far too small.",
    ncert="Class 11 Physics, 'Work, Energy and Power', power", seconds=20)

K_ratio = 4                                                # 300% increase → 4K
p_ratio = math.sqrt(K_ratio)
assert close(100 * (p_ratio - 1), 100) and close(100 * (math.sqrt(3) - 1), 73.2, 1e-2)
add(T, "Work-energy theorem", "Intermediate", "numerical",
    "The kinetic energy of a body increases by 300% while its mass stays the same. Its linear momentum increases by:",
    place("100%", ["300%", "200%", "73%"], "C"),
    "Relation between kinetic energy and momentum",
    "K = p²/(2m), so for a fixed mass p ∝ √K. A 300% increase makes the new kinetic energy four times the old one.",
    ["K' = K + 3K = 4K", "p'/p = √(K'/K) = √4 = 2", "Increase in momentum = (2 − 1) × 100% = 100%"],
    why="300% assumes momentum is proportional to kinetic energy. 200% takes the new momentum as 3 times the old. "
        "73% takes the new kinetic energy as 3K (√3 − 1), misreading 'increases by 300%' as 'becomes 300%'.",
    ncert="Class 11 Physics, 'Work, Energy and Power', kinetic energy", seconds=50, recomputed=True)

decel = 10 * (0.6 + 0.25 * 0.8)
s_up = 8 ** 2 / (2 * decel)
assert close(decel, 8) and close(s_up, 4)
assert close(8 ** 2 / (2 * 10 * 0.6), 16 / 3) and close(8 ** 2 / (2 * 10 * (0.6 - 0.25 * 0.8)), 8)
assert close(8 ** 2 / (2 * 10 * (0.8 + 0.25 * 0.6)), 3.37, 1e-2)
add(T, "Work-energy theorem", "Intermediate", "numerical",
    "A block is projected up a rough plane inclined at θ to the horizontal (sin θ = 0.6, cos θ = 0.8) with a speed of "
    "8 m/s along the plane. The coefficient of kinetic friction between the block and the plane is 0.25. Taking "
    "g = 10 m/s², the distance it moves up the plane before coming to rest is:",
    place("4 m", ["16/3 m", "8 m", "3.4 m"], "B"),
    "Work–energy theorem with gravity and friction",
    "While the block moves up, both the component of gravity along the plane (mg sin θ) and kinetic friction "
    "(μmg cos θ) act down the plane. By the work–energy theorem, their total work over the distance s equals the "
    "loss of kinetic energy.",
    ["½mv² = (mg sin θ + μmg cos θ)s", "s = v²/[2g(sin θ + μ cos θ)] = 64/[2 × 10 × (0.6 + 0.2)]",
     "s = 64/16 = 4 m"],
    why="16/3 m ignores friction. 8 m takes friction as acting up the plane (sin θ − μ cos θ). 3.4 m interchanges "
        "sin θ and cos θ.",
    ncert="Class 11 Physics, 'Work, Energy and Power', the work-energy theorem", seconds=70, recomputed=True)

v_top_sq = 8 ** 2 - 4 * 10 * 1
assert v_top_sq == 24 and v_top_sq >= 10 * 1                    # string stays taut at the top
add(T, "Motion in a vertical circle", "Intermediate", "numerical",
    "A small stone tied to a light string 1 m long is whirled in a vertical circle. Its speed at the lowest point is "
    "8 m/s. Taking g = 10 m/s² and neglecting air resistance, its speed at the highest point is:",
    place("2√6 m/s", ["2√11 m/s", "8 m/s", "2√26 m/s"], "D"),
    "Energy conservation in a vertical circle",
    "The tension is always perpendicular to the velocity and does no work, so mechanical energy is conserved. The "
    "highest point is 2l above the lowest point. (Check: v² = 24 m²/s² exceeds gl = 10 m²/s², so the string stays "
    "taut there.)",
    ["½mv₁² = ½mv₂² + mg(2l)", "v₂² = 64 − 4 × 10 × 1 = 24", "v₂ = √24 = 2√6 m/s ≈ 4.9 m/s"],
    why="2√11 m/s uses a rise of l instead of 2l (that is the speed at the side, level with the centre). 8 m/s "
        "ignores the gain in potential energy. 2√26 m/s adds the potential energy instead of subtracting it.",
    ncert="Class 11 Physics, 'Work, Energy and Power', motion in a vertical circle", seconds=60, recomputed=True)

add(T, "Power", "Intermediate", "assertion_reason",
    AR_STEM.format(
        a="To drive a car up a slope at a constant speed, the engine must deliver more power than to drive it at the "
          "same speed along a level road with the same resistive forces.",
        r="The power delivered by a force F to a body moving with velocity v is F · v, and on the slope the engine's "
          "force must also balance the component of the car's weight along the slope."),
    ar("A"),
    "Power as F · v",
    "At constant speed the net force is zero. On level ground the engine force only balances the resistances; on "
    "the slope it must also balance mg sin θ. With the same speed v, the larger force means larger power P = Fv.",
    ["Level: F = f_resist → P = f_resist v", "Slope: F = f_resist + mg sin θ → P larger"],
    why="R gives both the formula P = Fv and the reason the force is larger, so it explains A.",
    ncert="Class 11 Physics, 'Work, Energy and Power', power", seconds=50)

W_lift, W_grav, W_tension, W_spring = 2 * 10 * 5, -2 * 10 * 5, 0, 0.5 * 200 * 0.5 ** 2
assert (W_lift, W_grav, W_tension, W_spring) == (100, -100, 0, 25)
add(T, "Work by constant and variable force", "Intermediate", "match_list",
    match_stem("Take g = 10 m/s². Match List-I (work done) with List-II (its value).",
               ["Work done by a person in slowly lifting a 2 kg box through a height of 5 m",
                "Work done by gravity on the same box during this lift",
                "Work done by the tension in the string of a simple pendulum during one complete oscillation",
                "Work done in slowly stretching a spring of spring constant 200 N/m by 0.5 m from its natural length"],
               ["25 J", "−100 J", "100 J", "Zero"]),
    match_options({"A": "III", "B": "II", "C": "IV", "D": "I"},
                  [{"A": "II", "B": "III", "C": "IV", "D": "I"}, {"A": "III", "B": "II", "C": "I", "D": "IV"},
                   {"A": "III", "B": "IV", "C": "II", "D": "I"}], "C"),
    "Sign and size of work",
    "Lifting slowly, the person's force equals mg and is along the displacement: W = mgh. Gravity acts opposite to "
    "the displacement: W = −mgh. The string's tension is always perpendicular to the bob's velocity, so it does no "
    "work. Stretching a spring slowly needs work ½kx².",
    ["A: 2 × 10 × 5 = 100 J → III", "B: −100 J → II", "C: tension ⊥ velocity → 0 → IV",
     "D: ½ × 200 × 0.25 = 25 J → I"],
    why="The other codes swap the signs of the person's work and gravity's work, or give a non-zero value to the "
        "tension, which is perpendicular to the motion and does no work.",
    ncert="Class 11 Physics, 'Work, Energy and Power', work and potential energy of a spring", seconds=60)

vB, vA = 10 * math.cos(math.radians(60)), 10 * math.cos(math.radians(30))
assert close(vA * math.cos(math.radians(30)) + vB * math.cos(math.radians(60)), 10)      # x-momentum
assert abs(vA * math.sin(math.radians(30)) - vB * math.sin(math.radians(60))) < 1e-9       # y-momentum
assert close(vA ** 2 + vB ** 2, 100) and close(vB, 5)                                     # kinetic energy
add(T, "Collisions", "Advanced", "numerical",
    "A ball moving at 10 m/s on a smooth horizontal surface collides elastically, but not head-on, with an "
    "identical ball at rest. After the collision the struck ball moves off at 60° to the original direction of "
    "motion. Its speed is:",
    place("5 m/s", ["5√3 m/s", "10 m/s", "5√2 m/s"], "D"),
    "Oblique elastic collision of equal masses",
    "For equal masses with one at rest, momentum conservation gives u = v₁ + v₂ (vectors) and kinetic energy "
    "conservation gives u² = v₁² + v₂². Both hold only if v₁ ⊥ v₂, so the two balls move off at right angles, and "
    "the velocity triangle is right-angled with u as hypotenuse.",
    ["Balls move at 90° to each other: struck ball at 60°, other ball at 30° on the other side",
     "Struck ball: v₂ = u cos 60° = 5 m/s", "Other ball: v₁ = u cos 30° = 5√3 m/s",
     "Check: 5² + (5√3)² = 100 = u² ✓"],
    why="5√3 m/s is the speed of the incident ball, which moves at 30°. 10 m/s is what happens in a head-on elastic "
        "collision of equal masses. 5√2 m/s assumes both balls move at 45° with equal speeds.",
    ncert="Class 11 Physics, 'Work, Energy and Power', collisions in two dimensions", seconds=100, recomputed=True)

add(T, "Collisions", "Advanced", "statement_pair",
    SP_STEM.format(
        s1="In a one-dimensional elastic collision of two bodies, the relative speed with which they separate after "
           "the collision equals the relative speed with which they approach each other before it.",
        s2="When two bodies rub against each other with kinetic friction between them, the total work done by the "
           "pair of friction forces on the two bodies together is negative."),
    sp("A"),
    "Elastic collisions; work done by kinetic friction",
    "Combining momentum and kinetic-energy conservation for a 1D elastic collision gives v₂ − v₁ = u₁ − u₂. For the "
    "friction pair, the two forces are equal and opposite, but the bodies move different distances. The total work "
    "is −f × (relative sliding distance), which is negative; this is the mechanical energy turned into heat.",
    ["Statement I: from m₁(u₁² − v₁²) = m₂(v₂² − u₂²) and m₁(u₁ − v₁) = m₂(v₂ − u₂) → u₁ + v₁ = u₂ + v₂ → true",
     "Statement II: W_total = −f × s_relative < 0 → true"],
    why="Statement II can look false because the friction forces form an action–reaction pair, but their works do "
        "not cancel when the bodies slide relative to each other.",
    seconds=80)

truth = [True, True, True, True, False]
multi_key(truth, "abcd")
add(T, "Work-energy theorem", "Advanced", "multi_statement",
    multi("A body moves under the action of a single conservative force. Which of the following statements are "
          "correct?",
          ["The sum of its kinetic energy and potential energy remains constant.",
           "At the position where its kinetic energy is greatest, its potential energy is least.",
           "The work done by the force between two positions equals the decrease in potential energy between them.",
           "Its speed is the same every time it passes through a given position.",
           "The work done by the force between two given positions depends on the path followed."]),
    place("(a), (b), (c) and (d) only",
          ["(a), (b) and (c) only", "(a), (c) and (e) only", "(b), (c), (d) and (e) only"], "B"),
    "Conservative forces and mechanical energy",
    "For a conservative force W = −ΔU, independent of the path. With no other force acting, the work–energy "
    "theorem gives ΔK = W = −ΔU, so K + U is constant. Then K is largest where U is smallest, and K (hence the "
    "speed) depends only on position.",
    ["(a) ΔK + ΔU = 0 → true", "(b) K = E − U → true", "(c) W = −ΔU → true",
     "(d) K depends only on U at that position → true", "(e) path-independence is what defines a conservative "
     "force → false"],
    why="(e) describes a non-conservative force such as friction. Codes leaving out (d) miss that a constant total "
        "energy fixes the speed at every position.",
    ncert="Class 11 Physics, 'Work, Energy and Power', conservative forces and conservation of mechanical energy",
    seconds=80)


# =====================================================================================================================
# Rotational Motion (B4 I5 A4)
# =====================================================================================================================
T = "Rotational Motion"

M_rod, L_rod = 3, 2
I_end = M_rod * L_rod ** 2 / 12 + M_rod * (L_rod / 2) ** 2
assert close(I_end, 4) and close(M_rod * L_rod ** 2 / 12, 1) and M_rod * L_rod ** 2 == 12
add(T, "Moment of inertia and axis theorems", "Basic", "numerical",
    "A thin uniform rod has mass 3 kg and length 2 m. Its moment of inertia about an axis perpendicular to the rod "
    "and passing through one of its ends is:",
    place("4 kg m²", ["1 kg m²", "12 kg m²", "3 kg m²"], "C"),
    "Parallel axes theorem for a rod",
    "About the perpendicular axis through its centre, a thin rod has I = ML²/12. The end is L/2 from the centre, so "
    "the parallel axes theorem adds M(L/2)², giving ML²/3.",
    ["I_c = ML²/12 = 3 × 4/12 = 1 kg m²", "I_end = I_c + M(L/2)² = 1 + 3 × 1 = 4 kg m² (= ML²/3)"],
    why="1 kg m² is the value about the centre. 12 kg m² is ML², as if all the mass were at the far end. 3 kg m² "
        "takes ML²/4, adding nothing for the shift of the axis.",
    ncert="Class 11 Physics, 'System of Particles and Rotational Motion', theorem of parallel axes", seconds=40,
    recomputed=True)

tau_sp = 20 * 0.5 * math.sin(math.radians(30))
assert close(tau_sp, 5)
add(T, "Torque and angular momentum", "Basic", "numerical",
    "A force of 20 N is applied at the free end of a spanner 0.5 m long, in the plane of rotation, at an angle of 30° "
    "to the length of the spanner. The magnitude of the torque about the bolt at the other end is:",
    place("5 N m", ["10 N m", "5√3 N m", "40 N m"], "A"),
    "Torque as rF sin θ",
    "Torque τ = r × F has magnitude rF sin θ, where θ is the angle between the position vector (along the spanner) "
    "and the force. Only the component of F perpendicular to the spanner turns the bolt.",
    ["τ = rF sin θ = 0.5 × 20 × sin 30°", "τ = 0.5 × 20 × 0.5 = 5 N m"],
    why="10 N m drops sin θ, as if the force were perpendicular to the spanner. 5√3 N m uses cos θ, the component "
        "along the spanner, which produces no turning. 40 N m divides F by r.",
    ncert="Class 11 Physics, 'System of Particles and Rotational Motion', moment of force (torque)", seconds=35,
    recomputed=True)

assert 10 ** 2 / (2 * 2) == 25 and 10 ** 2 / 2 == 50
add(T, "Rigid-body rotation", "Basic", "numerical",
    "A wheel whose moment of inertia about its axle is 2 kg m² rotates about the axle with an angular momentum of "
    "10 kg m² s⁻¹. Its rotational kinetic energy is:",
    place("25 J", ["50 J", "5 J", "100 J"], "D"),
    "Rotational kinetic energy in terms of angular momentum",
    "With L = Iω and K = ½Iω², eliminating ω gives K = L²/(2I), the rotational form of K = p²/(2m).",
    ["ω = L/I = 10/2 = 5 rad/s", "K = ½Iω² = ½ × 2 × 25 = 25 J (= L²/2I = 100/4)"],
    why="50 J uses L²/I, dropping the ½. 5 J is the angular velocity in rad/s, not an energy. 100 J is L² with no "
        "division by 2I.",
    ncert="Class 11 Physics, 'System of Particles and Rotational Motion', kinetic energy of rotation", seconds=35,
    recomputed=True)

add(T, "Torque and angular momentum", "Basic", "direct",
    "The net external torque acting on a system of particles is equal to the time rate of change of its:",
    place("Total angular momentum", ["Total linear momentum", "Moment of inertia", "Angular velocity"], "B"),
    "Torque and angular momentum",
    "For a system of particles, dL/dt = τ_ext, the rotational analogue of dP/dt = F_ext. Internal torques cancel in "
    "pairs, so only the external torque changes the total angular momentum.",
    ["τ_ext = dL/dt"],
    why="The rate of change of linear momentum is the net external force, not the torque. Torque equals I times "
        "angular acceleration only for a fixed axis and fixed I, so it is not in general the rate of change of "
        "moment of inertia or of angular velocity.",
    ncert="Class 11 Physics, 'System of Particles and Rotational Motion', angular momentum of a system of particles",
    seconds=25)

x_cm = (1 * 0.5 + 1 * 0) / 2
y_cm = (1 * 0 + 1 * 0.5) / 2
assert x_cm == 0.25 and y_cm == 0.25
add(T, "Centre of mass", "Intermediate", "numerical",
    "Two thin uniform rods, each of mass m and length L, are joined at one end to form an L shape. The joint is at the "
    "origin, one rod lies along the positive x-axis and the other along the positive y-axis. The coordinates of the "
    "centre of mass of the L-shaped body are:",
    place("(L/4, L/4)", ["(L/2, L/2)", "(L/2, L/4)", "(L/3, L/3)"], "A"),
    "Centre of mass of a composite body",
    "Replace each uniform rod by a point mass m at its own centre: (L/2, 0) for the x-rod and (0, L/2) for the "
    "y-rod. The centre of mass of the two equal masses is midway between these points.",
    ["x_cm = (m · L/2 + m · 0)/(2m) = L/4", "y_cm = (m · 0 + m · L/2)/(2m) = L/4"],
    why="(L/2, L/2) adds the two rods' coordinates without dividing by the total mass. (L/2, L/4) treats only one "
        "coordinate correctly. (L/3, L/3) uses the centroid of a triangle formed by the rods, which would need a "
        "third side.",
    ncert="Class 11 Physics, 'System of Particles and Rotational Motion', centre of mass", seconds=50,
    recomputed=True)

a_sq, M_sq = 1.0, 1.0
I_z = M_sq * a_sq ** 2 / 6                    # square plate about the central perpendicular axis
I_side = M_sq * a_sq ** 2 / 12                # about a central line parallel to a side
assert close(2 * I_side, I_z)                 # perpendicular axes theorem
I_diag = I_z / 2                              # the two diagonals are perpendicular and equivalent by symmetry
assert close(I_diag, I_side)
add(T, "Moment of inertia and axis theorems", "Intermediate", "numerical",
    "The moment of inertia of a thin uniform square plate about an axis through its centre and perpendicular to its "
    "plane is I. Its moment of inertia about one of its diagonals is:",
    place("I/2", ["I", "I/√2", "2I"], "D"),
    "Theorem of perpendicular axes with symmetry",
    "For a plane lamina, I_z = I_x + I_y for any two perpendicular axes in its plane meeting on the z-axis. The two "
    "diagonals of a square are perpendicular, pass through the centre and are equivalent by symmetry, so each has "
    "half of I_z.",
    ["I_d₁ + I_d₂ = I (perpendicular axes theorem)", "I_d₁ = I_d₂ by symmetry → I_d = I/2",
     "(Check: I = Ma²/6 and I_d = Ma²/12, the same as about a central line parallel to a side)"],
    why="I takes the in-plane axis to have the same moment of inertia as the perpendicular axis. I/√2 has no basis "
        "in either theorem. 2I adds instead of sharing.",
    ncert="Class 11 Physics, 'System of Particles and Rotational Motion', theorem of perpendicular axes",
    seconds=55, recomputed=True)

I_w, tau_w, t_w = 4, 8, 5
omega_w = tau_w / I_w * t_w
K_w = 0.5 * I_w * omega_w ** 2
theta_w = 0.5 * (tau_w / I_w) * t_w ** 2
assert omega_w == 10 and K_w == 200 and close(tau_w * theta_w, K_w)
assert I_w * omega_w ** 2 == 400 and tau_w * t_w == 40 and tau_w * omega_w == 80
add(T, "Rigid-body rotation", "Intermediate", "numerical",
    "A flywheel with a moment of inertia of 4 kg m² about its axle starts from rest. A constant torque of 8 N m acts "
    "on it about the axle. Neglecting friction, its rotational kinetic energy after 5 s is:",
    place("200 J", ["400 J", "40 J", "80 J"], "B"),
    "Rotational equations of motion",
    "A constant torque gives a constant angular acceleration α = τ/I. Find ω after 5 s and use K = ½Iω². "
    "Equivalently, the work done by the torque, τθ, equals the kinetic energy gained.",
    ["α = τ/I = 8/4 = 2 rad/s²", "ω = αt = 10 rad/s", "K = ½ × 4 × 10² = 200 J",
     "Check: θ = ½αt² = 25 rad, W = τθ = 200 J"],
    why="400 J drops the ½ in ½Iω². 40 J is τt, which is the angular momentum gained (in kg m² s⁻¹). 80 J is τω, "
        "which is the power at t = 5 s (in W).",
    ncert="Class 11 Physics, 'System of Particles and Rotational Motion', dynamics of rotational motion about a fixed "
          "axis", seconds=60, recomputed=True)

L_fall = 0.6
v_tip = math.sqrt(3 * 10 * L_fall)
assert close(v_tip, 3 * math.sqrt(2)) and close(math.sqrt(2 * 10 * L_fall), 2 * math.sqrt(3))
assert close(math.sqrt(6 * 10 * L_fall), 6) and close(math.sqrt(10 * L_fall), math.sqrt(6))
add(T, "Rigid-body rotation", "Advanced", "numerical",
    "A thin uniform rod 0.6 m long stands vertically on the floor, its lower end attached to a frictionless hinge on "
    "the floor. It is disturbed slightly and falls, rotating about the hinge. Taking g = 10 m/s², the speed of its "
    "upper end just as the rod hits the floor is:",
    place("3√2 m/s", ["2√3 m/s", "√6 m/s", "6 m/s"], "C"),
    "Energy conservation in rotation about a fixed axis",
    "The hinge does no work, so the loss of gravitational potential energy (the centre of mass falls L/2) becomes "
    "rotational kinetic energy about the hinge, with I = ML²/3. The end moves with v = ωL.",
    ["Mg(L/2) = ½(ML²/3)ω² → ω² = 3g/L", "v_end = ωL = √(3gL) = √(3 × 10 × 0.6) = √18 = 3√2 m/s ≈ 4.2 m/s"],
    why="2√3 m/s = √(2gL) treats the end as falling freely through L. √6 m/s = √(gL) uses the moment of inertia "
        "about the centre. 6 m/s = √(6gL) takes the centre of mass to fall a full L.",
    ncert="Class 11 Physics, 'System of Particles and Rotational Motion', kinetic energy of rotation", seconds=90,
    recomputed=True)

W_lad, L_lad, base = 200, 5, 3
height = math.sqrt(L_lad ** 2 - base ** 2)
N_wall = W_lad * (base / 2) / height
assert height == 4 and close(N_wall, 75)
add(T, "Equilibrium of rigid bodies", "Advanced", "numerical",
    "A uniform ladder 5 m long and of weight 200 N rests against a smooth vertical wall, with its foot on a rough "
    "horizontal floor 3 m from the wall. The ladder is in equilibrium. The friction force exerted by the floor on the "
    "ladder is:",
    place("75 N", ["150 N", "100 N", "200 N"], "B"),
    "Translational and rotational equilibrium",
    "The smooth wall exerts only a horizontal force N₁. The floor exerts a vertical normal force N₂ and a horizontal "
    "friction f. Horizontal balance gives f = N₁; vertical balance gives N₂ = W. Take moments about the foot to "
    "remove N₂ and f.",
    ["Top of ladder is √(5² − 3²) = 4 m above the floor",
     "Moments about the foot: N₁ × 4 = W × 1.5 (weight acts at the midpoint, 1.5 m from the wall-foot line)",
     "N₁ = 200 × 1.5/4 = 75 N", "f = N₁ = 75 N"],
    why="150 N takes the weight's moment arm as the full 3 m instead of half of it. 100 N assumes the friction is "
        "half the weight. 200 N equates friction with the weight, which is the vertical force N₂.",
    ncert="Class 11 Physics, 'System of Particles and Rotational Motion', equilibrium of a rigid body", seconds=100,
    recomputed=True)

add(T, "Torque and angular momentum", "Intermediate", "assertion_reason",
    AR_STEM.format(
        a="If the polar ice caps melted and the water spread over the oceans, the length of a day on the Earth would "
          "increase slightly.",
        r="The melted water would move farther from the Earth's axis of rotation, increasing the Earth's moment of "
          "inertia, while its angular momentum about the axis stays constant."),
    ar("A"),
    "Conservation of angular momentum",
    "With no external torque about the axis, L = Iω is constant. Water from the poles lies almost on the axis; "
    "spread over the oceans it is on average much farther away, so I increases and ω decreases. A smaller ω means a "
    "longer day.",
    ["L = Iω = constant", "I increases → ω decreases → period 2π/ω increases"],
    why="R gives both the change in I and the conservation law that turns it into a slower spin, so it explains A.",
    ncert="Class 11 Physics, 'System of Particles and Rotational Motion', conservation of angular momentum",
    seconds=45)

add(T, "Torque and angular momentum", "Intermediate", "match_list",
    match_stem("Match List-I (quantity) with List-II (its expression). r is the position vector from the origin or "
               "a point on the axis, F a force, p a linear momentum, ω the angular velocity and τ a torque.",
               ["Torque of a force about the origin", "Angular momentum of a particle about the origin",
                "Linear velocity of a particle of a rigid body rotating about a fixed axis",
                "Power delivered by a torque to a body rotating about a fixed axis"],
               ["r × p", "τ · ω", "r × F", "ω × r"]),
    match_options({"A": "III", "B": "I", "C": "IV", "D": "II"},
                  [{"A": "I", "B": "III", "C": "IV", "D": "II"}, {"A": "III", "B": "I", "C": "II", "D": "IV"},
                   {"A": "III", "B": "IV", "C": "I", "D": "II"}], "D"),
    "Vector relations in rotational motion",
    "Torque is the moment of force, τ = r × F; angular momentum is the moment of linear momentum, l = r × p. A "
    "point of a rotating rigid body moves with v = ω × r. For rotation about a fixed axis, P = τω, the rotational "
    "analogue of P = F · v, and it is a scalar product.",
    ["A → r × F → III", "B → r × p → I", "C → ω × r → IV", "D → τ · ω → II"],
    why="The other codes swap torque and angular momentum, or give the power, which is a scalar, a cross-product "
        "form.",
    ncert="Class 11 Physics, 'System of Particles and Rotational Motion', torque, angular momentum and work done by "
          "a torque", seconds=55)

add(T, "Centre of mass", "Advanced", "statement_pair",
    SP_STEM.format(
        s1="If the net external force on a system of particles is zero, its centre of mass moves with a constant "
           "velocity (or stays at rest).",
        s2="The angular momentum of a system about a point can stay constant even though the net external force on "
           "the system is not zero."),
    sp("A"),
    "Motion of the centre of mass; conservation of angular momentum",
    "M a_cm = F_ext, so F_ext = 0 gives a constant velocity of the centre of mass. Angular momentum about a point is "
    "conserved when the net external torque about that point is zero, which can happen with a non-zero force: for "
    "a planet, the Sun's force is not zero but always points towards the Sun, so its torque about the Sun is zero.",
    ["Statement I: Ma_cm = F_ext = 0 → v_cm constant → true",
     "Statement II: central force → r ∥ F → τ = 0 → L conserved → true"],
    why="Statement II is true because what matters is the torque, not the force; a central force has zero torque "
        "about its centre.",
    ncert="Class 11 Physics, 'System of Particles and Rotational Motion', motion of centre of mass and conservation "
          "of angular momentum", seconds=60)

# particle at angle φ on a circle of radius 1 (centre O), speed 1; L about P = (1, 0) on the circle
Lp = []
for deg in (0, 90, 180):
    ph = math.radians(deg)
    pos = (math.cos(ph) - 1, math.sin(ph))
    vel = (-math.sin(ph), math.cos(ph))
    Lp.append(pos[0] * vel[1] - pos[1] * vel[0])
assert close(Lp[0], 0, 1e-9) or abs(Lp[0]) < 1e-12
assert close(Lp[2], 2) and close(Lp[1], 1)                 # not constant about a point on the circle
truth = [True, True, True, False, False]
multi_key(truth, "abc")
add(T, "Torque and angular momentum", "Advanced", "multi_statement",
    multi("A particle of mass m moves with a constant speed v along a horizontal circle of radius r. Which of the "
          "following statements are correct?",
          ["Its angular momentum about the centre of the circle has magnitude mvr.",
           "Its angular momentum about the centre of the circle is constant in both magnitude and direction.",
           "The net torque on it about the centre of the circle is zero.",
           "Its linear momentum is constant.",
           "Its angular momentum about a fixed point on the circle itself is constant."]),
    place("(a), (b) and (c) only", ["(a), (b), (c) and (d) only", "(a), (c) and (e) only", "(b), (d) and (e) only"],
          "C"),
    "Angular momentum in uniform circular motion",
    "About the centre, r ⊥ v at every instant, so |l| = mvr, and l points along the axis of the circle all the time. "
    "The net force points to the centre, so its torque about the centre is zero, consistent with constant l. The "
    "linear momentum keeps changing direction. About a point P on the circle, the particle's distance and direction "
    "from P change: l is zero when the particle is at P and 2mvr when it is diametrically opposite.",
    ["(a) |r × p| = rmv sin 90° → true", "(b) l along the axis, fixed magnitude → true",
     "(c) centripetal force passes through the centre → τ = 0 → true", "(d) direction of p changes → false",
     "(e) l about P varies from 0 to 2mvr → false"],
    why="Codes with (d) treat momentum as a scalar; codes with (e) forget that angular momentum depends on the point "
        "about which it is taken.",
    seconds=80)


# =====================================================================================================================
# Gravitation (B3 I4 A3)
# =====================================================================================================================
T = "Gravitation"

assert F(2 * 2, 3 ** 2) == F(4, 9)
add(T, "Law of gravitation", "Basic", "numerical",
    "The gravitational force between two point masses is F. If each mass is doubled and the distance between them "
    "is tripled, the force becomes:",
    place("4F/9", ["4F/3", "2F/9", "2F/3"], "B"),
    "Newton's law of gravitation",
    "F = Gm₁m₂/r². The force is proportional to the product of the masses and inversely proportional to the "
    "square of the distance.",
    ["Product of masses → 2 × 2 = 4 times", "r² → 3² = 9 times", "F' = 4F/9"],
    why="4F/3 divides by r instead of r². 2F/9 doubles only one mass. 2F/3 doubles one mass and uses 1/r.",
    ncert="Class 11 Physics, 'Gravitation', universal law of gravitation", seconds=30, recomputed=True)

R_E = 6400
d_quarter = R_E * (1 - 0.25)
assert d_quarter == 4800
add(T, "Variation of g", "Basic", "numerical",
    "Treating the Earth as a uniform sphere of radius 6400 km, the depth below its surface at which the acceleration "
    "due to gravity is one-quarter of its value at the surface is:",
    place("4800 km", ["1600 km", "3200 km", "6400 km"], "C"),
    "Acceleration due to gravity below the surface",
    "For a uniform Earth, only the mass inside radius (R − d) attracts the body, and g(d) = g(1 − d/R), decreasing "
    "linearly to zero at the centre.",
    ["g(1 − d/R) = g/4 → d/R = 3/4", "d = 0.75 × 6400 = 4800 km"],
    why="1600 km is the depth at which g falls by one-quarter (to 3g/4). 3200 km gives g/2. 6400 km is the centre, "
        "where g = 0.",
    ncert="Class 11 Physics, 'Gravitation', acceleration due to gravity below the surface of the Earth", seconds=40,
    recomputed=True)

add(T, "Law of gravitation", "Basic", "direct",
    "Two point masses A and B attract each other with a gravitational force F. A third point mass C is now placed on "
    "the line joining them, between A and B. The gravitational force exerted by A on B:",
    place("Remains F", ["Becomes zero", "Becomes less than F", "Becomes greater than F"], "D"),
    "Independence of gravitational forces (superposition)",
    "The gravitational force between two masses depends only on their masses and separation. It is not screened or "
    "altered by other bodies; C simply adds its own forces on A and on B, and the net force on B is the vector sum.",
    ["F_AB = Gm_Am_B/r², unchanged by C", "Net force on B = F_AB + F_CB (superposition)"],
    why="'Zero' and 'less than F' imagine that C shields B from A. 'Greater than F' confuses the force of A on B "
        "with the net force on B.",
    ncert="Class 11 Physics, 'Gravitation', universal law of gravitation (principle of superposition)", seconds=30)

T_near = 2 * math.pi * math.sqrt(6.4e6 / 10)
assert close(T_near, 5026.5, 1e-4) and round(T_near / 60) == 84
assert round(T_near / 120) == 42 and round(math.sqrt(2) * T_near / 60) == 118
add(T, "Satellite energy and period", "Intermediate", "numerical",
    "A satellite revolves in a circular orbit just above the Earth's surface. Taking the Earth's radius as 6400 km "
    "and g = 10 m/s², and neglecting air resistance, its period of revolution is about:",
    place("84 minutes", ["42 minutes", "118 minutes", "24 hours"], "C"),
    "Period of a satellite close to the Earth",
    "For an orbit of radius r ≈ R, gravity mg supplies the centripetal force: mg = mv²/R, so v = √(gR) and "
    "T = 2πR/v = 2π√(R/g).",
    ["T = 2π√(R/g) = 2π√(6.4 × 10⁶/10) = 2π × 800 s", "T ≈ 5027 s ≈ 84 min"],
    why="42 minutes uses π√(R/g), half the circumference. 118 minutes uses 2π√(2R/g), as if the speed were "
        "√(gR/2). 24 hours is the Earth's rotation period, unrelated to a low orbit.",
    ncert="Class 11 Physics, 'Gravitation', earth satellites", seconds=50, recomputed=True)

g_p, R_p = 4, 2.0e6
ve_p = math.sqrt(2 * g_p * R_p)
assert close(ve_p, 4000) and close(math.sqrt(g_p * R_p), 2000 * math.sqrt(2))
assert close(math.sqrt(4 * g_p * R_p), 4000 * math.sqrt(2)) and close(math.sqrt(2 * g_p * 2000), 126.5, 1e-3)
add(T, "Escape and orbital velocity", "Intermediate", "numerical",
    "The acceleration due to gravity at the surface of a planet is 4 m/s² and its radius is 2000 km. Ignoring its "
    "atmosphere and rotation, the escape speed from its surface is:",
    place("4 km/s", ["2√2 km/s", "4√2 km/s", "0.13 km/s"], "B"),
    "Escape speed in terms of g and R",
    "Escape speed vₑ = √(2GM/R). Since g = GM/R² at the surface, GM = gR², so vₑ = √(2gR).",
    ["vₑ = √(2gR) = √(2 × 4 × 2 × 10⁶) m/s", "= √(1.6 × 10⁷) = 4000 m/s = 4 km/s"],
    why="2√2 km/s is √(gR), the orbital speed just above the surface. 4√2 km/s uses √(4gR). 0.13 km/s puts R in "
        "kilometres instead of metres.",
    ncert="Class 11 Physics, 'Gravitation', escape speed", seconds=45, recomputed=True)

add(T, "Kepler's laws", "Intermediate", "assertion_reason",
    AR_STEM.format(
        a="The ratio T²/a³ (T = period, a = semi-major axis of the orbit) has the same value for the Earth "
          "orbiting the Sun as for the Moon orbiting the Earth.",
        r="For a body orbiting a much heavier central body of mass M, T² = (4π²/GM)a³, so the constant of "
          "proportionality depends on the mass of the central body but not on that of the orbiting body."),
    ar("D"),
    "Kepler's law of periods",
    "Equating the gravitational force to the centripetal force for a (nearly circular) orbit gives "
    "GMm/r² = m(2π/T)²r, so T²/r³ = 4π²/(GM). The orbiting body's mass m cancels, but M is the mass of the body at "
    "the centre. The Sun and the Earth have very different masses, so the ratio is different for the Earth's orbit "
    "and for the Moon's orbit.",
    ["T²/a³ = 4π²/GM_central", "M_Sun ≠ M_Earth → different ratios → A false", "R is the correct relation → true"],
    why="A is the trap: the ratio is common only to bodies orbiting the same central body (all the planets of the "
        "Sun, or all satellites of the Earth).",
    ncert="Class 11 Physics, 'Gravitation', Kepler's laws", seconds=45)

truth = [True, True, False, False, True]
multi_key(truth, "abe")
add(T, "Satellite energy and period", "Intermediate", "multi_statement",
    multi("An astronaut is inside a spacecraft orbiting the Earth in a circular orbit with its engines off. Which of "
          "the following statements are correct?",
          ["A spring balance from which a body hangs inside the spacecraft reads zero.",
           "An ordinary pendulum clock inside the spacecraft cannot keep time.",
           "The mass of the astronaut becomes zero.",
           "A simple pendulum inside the spacecraft oscillates with period 2π√(L/g'), where g' is the acceleration "
           "due to gravity at the height of the orbit.",
           "The astronaut's mass, as found from how hard it is to accelerate him, is the same as on the Earth."]),
    place("(a), (b) and (e) only", ["(a), (b), (c) and (e) only", "(b), (d) and (e) only", "(a), (d) and (e) only"],
          "D"),
    "Weightlessness in an orbiting satellite",
    "The spacecraft and everything in it fall freely together with acceleration g'. Relative to the spacecraft "
    "there is no effective gravity: nothing presses on a support or stretches a spring, and a pendulum has no "
    "restoring force, so it does not oscillate. Mass is a property of the body and does not change.",
    ["(a) no effective weight → reading zero → true", "(b) pendulum needs effective gravity → true",
     "(c) mass unchanged → false", "(d) effective g inside = 0 → no oscillation → false", "(e) inertia unchanged → true"],
    why="Codes with (c) confuse weightlessness with masslessness; codes with (d) use the actual field g' instead of "
        "the effective gravity, which is zero in free fall.",
    seconds=70)

ve = 1.0
v_inf = math.sqrt((2 * ve) ** 2 - ve ** 2)
assert close(v_inf, math.sqrt(3))
add(T, "Escape and orbital velocity", "Advanced", "numerical",
    "A body is projected from the Earth's surface with a speed equal to twice the escape speed vₑ. Neglecting air "
    "resistance and the Earth's rotation, and ignoring all bodies other than the Earth, its speed when it is very far "
    "from the Earth is:",
    place("√3 vₑ", ["vₑ", "2vₑ", "√5 vₑ"], "D"),
    "Energy conservation beyond the escape speed",
    "Kinetic energy ½mvₑ² is exactly what is needed to climb out of the Earth's potential well, since "
    "½mvₑ² = GMm/R. Any extra kinetic energy remains at infinity.",
    ["½m(2vₑ)² − GMm/R = ½mv∞²", "GMm/R = ½mvₑ² → 4vₑ² − vₑ² = v∞²", "v∞ = √3 vₑ"],
    why="vₑ subtracts speeds instead of energies. 2vₑ ignores the energy spent against gravity. √5 vₑ adds the "
        "potential-energy term instead of subtracting it.",
    seconds=70, recomputed=True)

a_comet = (1 + 7) / 2
assert a_comet == 4 and close(a_comet ** 1.5, 8)
assert close(7 ** 1.5, 18.52, 1e-3) and close(3 ** 1.5, 5.196, 1e-3) and a_comet ** 2 == 16
add(T, "Kepler's laws", "Advanced", "numerical",
    "A comet moves round the Sun in an elliptical orbit. Its closest distance from the Sun is 1 AU and its greatest "
    "distance is 7 AU, where 1 AU is the radius of the Earth's (nearly circular) orbit. Its period of revolution is:",
    place("8 years", ["about 18.5 years", "about 5.2 years", "16 years"], "C"),
    "Kepler's third law for an elliptical orbit",
    "In T² ∝ a³, a is the semi-major axis, half the sum of the closest and greatest distances. Compare with the "
    "Earth (a = 1 AU, T = 1 year).",
    ["a = (1 + 7)/2 = 4 AU", "T = (4)^(3/2) years = 8 years"],
    why="About 18.5 years uses the greatest distance 7 AU as a. About 5.2 years uses half the difference, 3 AU. "
        "16 years takes T ∝ a² instead of T² ∝ a³.",
    ncert="Class 11 Physics, 'Gravitation', Kepler's laws", seconds=70, recomputed=True)

assert close(2 ** 1.5, 2 * math.sqrt(2))
add(T, "Satellite energy and period", "Advanced", "statement_pair",
    SP_STEM.format(
        s1="A small object released gently (with zero velocity relative to the spacecraft) from a spacecraft "
           "orbiting the Earth in a circular orbit continues to move in the same orbit alongside the spacecraft.",
        s2="If the radius of a satellite's circular orbit round the Earth is doubled, its period becomes 2√2 times "
           "the original period."),
    sp("A"),
    "Orbits and Kepler's third law",
    "The released object has the same position and velocity as the spacecraft, and the orbital speed √(GM/r) does "
    "not depend on the orbiting body's mass, so it follows the same orbit. From T² ∝ r³, doubling r multiplies T by "
    "2^(3/2) = 2√2.",
    ["Statement I: same r and v, v_orbit independent of mass → same orbit → true",
     "Statement II: T ∝ r^(3/2) → T' = 2√2 T → true"],
    why="Statement I is not false: the object does not fall to the Earth, because it already has the orbital "
        "speed needed at that radius.",
    seconds=60)


# =====================================================================================================================
# Properties of Solids and Liquids (B5 I6 A5)
# =====================================================================================================================
T = "Properties of Solids and Liquids"

G_sh = (1000 / 0.01) / 2e-4
assert close(G_sh, 5e8) and close(1000 / 2e-4, 5e6) and close(1000 * 0.01 / 2e-4, 5e4)
add(T, "Elasticity and moduli", "Basic", "numerical",
    "A tangential force of 1000 N acts on the top face, of area 0.01 m², of a block whose bottom face is fixed. The "
    "resulting shearing strain (angular deformation) is 2 × 10⁻⁴. The shear modulus of the material is:",
    place("5 × 10⁸ N m⁻²", ["5 × 10⁶ N m⁻²", "2 × 10⁻⁹ N m²", "5 × 10⁴ N m⁻²"], "B"),
    "Shear modulus (modulus of rigidity)",
    "Shear modulus G = shearing stress/shearing strain, where shearing stress is the tangential force per unit area "
    "of the face on which it acts.",
    ["Shearing stress = 1000/0.01 = 1 × 10⁵ N m⁻²", "G = 1 × 10⁵/(2 × 10⁻⁴) = 5 × 10⁸ N m⁻²"],
    why="5 × 10⁶ N m⁻² divides the force, not the stress, by the strain. 2 × 10⁻⁹ is strain/stress, the inverse "
        "ratio. 5 × 10⁴ N m⁻² multiplies the force by the area instead of dividing.",
    ncert="Class 11 Physics, 'Mechanical Properties of Solids', shear modulus", seconds=40, recomputed=True)

H_win = 0.8 * 1 * 5 / 0.004
assert close(H_win, 1000) and close(0.8 * 5 / 4, 1) and close(1 * 5 / 0.004, 1250)
add(T, "Heat transfer", "Basic", "numerical",
    "A glass window pane has an area of 1 m² and a thickness of 4 mm. The thermal conductivity of the glass is "
    "0.8 W m⁻¹ K⁻¹. In the steady state the inner surface of the glass is 5 °C warmer than the outer surface. The "
    "rate at which heat flows through the pane is:",
    place("1000 W", ["1 W", "1250 W", "1.6 × 10⁻² W"], "A"),
    "Steady-state heat conduction",
    "For a slab, the heat current is H = KA(T₁ − T₂)/L, where L is the thickness in the direction of flow. A "
    "temperature difference of 5 °C is the same as 5 K.",
    ["L = 4 mm = 4 × 10⁻³ m", "H = 0.8 × 1 × 5/(4 × 10⁻³) = 1000 W"],
    why="1 W keeps the thickness in millimetres. 1250 W leaves out the thermal conductivity. 1.6 × 10⁻² W "
        "multiplies by the thickness instead of dividing.",
    ncert="Class 11 Physics, 'Thermal Properties of Matter', heat transfer (conduction)", seconds=40,
    recomputed=True)

dA = 2 * 2e-5 * 1 * 100
assert close(dA, 4e-3) and close(2e-5 * 100, 2e-3) and close(2 * 2e-5 * 120, 4.8e-3)
add(T, "Thermal expansion and calorimetry", "Basic", "numerical",
    "A thin metal plate has an area of 1 m² at 20 °C. The coefficient of linear expansion of the metal is "
    "2 × 10⁻⁵ K⁻¹. When the plate is heated to 120 °C, the increase in its area is:",
    place("4 × 10⁻³ m²", ["2 × 10⁻³ m²", "6 × 10⁻³ m²", "4.8 × 10⁻³ m²"], "D"),
    "Area expansion",
    "For small temperature changes the coefficient of area expansion is twice the coefficient of linear expansion, "
    "so ΔA = 2αAΔT, where ΔT is the change in temperature.",
    ["ΔT = 120 − 20 = 100 K", "ΔA = 2 × 2 × 10⁻⁵ × 1 × 100 = 4 × 10⁻³ m²"],
    why="2 × 10⁻³ m² uses α instead of 2α. 6 × 10⁻³ m² uses 3α, the volume coefficient. 4.8 × 10⁻³ m² uses the "
        "final temperature 120 °C instead of the change in temperature.",
    ncert="Class 11 Physics, 'Thermal Properties of Matter', thermal expansion", seconds=40, recomputed=True)

Q_ice = 0.1 * 2100 * 10 + 0.1 * 3.36e5
assert close(Q_ice, 35700) and close(0.1 * 4200 * 10 + 0.1 * 3.36e5, 37800)
add(T, "Thermal expansion and calorimetry", "Intermediate", "numerical",
    "How much heat is needed to change 100 g of ice at −10 °C into water at 0 °C? Take the specific heat capacity "
    "of ice as 2100 J kg⁻¹ K⁻¹ and the latent heat of fusion of ice as 3.36 × 10⁵ J kg⁻¹.",
    place("35.7 kJ", ["33.6 kJ", "37.8 kJ", "2.1 kJ"], "C"),
    "Sensible heat and latent heat",
    "The ice is first warmed from −10 °C to its melting point 0 °C (sensible heat mcΔT), and then melted at 0 °C "
    "without change of temperature (latent heat mL).",
    ["Warming: 0.1 × 2100 × 10 = 2100 J", "Melting: 0.1 × 3.36 × 10⁵ = 33 600 J",
     "Total = 35 700 J = 35.7 kJ"],
    why="33.6 kJ leaves out warming the ice to 0 °C. 37.8 kJ uses the specific heat of water (4200 J kg⁻¹ K⁻¹) for "
        "the ice. 2.1 kJ leaves out the latent heat.",
    ncert="Class 11 Physics, 'Thermal Properties of Matter', change of state and latent heat", seconds=60,
    recomputed=True)

v1 = math.sqrt(7500 * 2 / (1000 * (4 ** 2 - 1)))
assert close(v1, 1) and close(0.5 * 1000 * ((4 * v1) ** 2 - v1 ** 2), 7500)
assert close(math.sqrt(2 * 7500 / 1000), math.sqrt(15)) and close(math.sqrt(7500 * 2 / (1000 * 3)), math.sqrt(5))
add(T, "Bernoulli's principle", "Intermediate", "numerical",
    "Water flows steadily through a horizontal pipe. The cross-sectional area of the wide part is 4 times that of "
    "the narrow part, and the pressure in the wide part exceeds that in the narrow part by 7500 Pa. Taking the "
    "density of water as 1000 kg/m³ and neglecting viscosity, the speed of the water in the wide part is:",
    place("1 m/s", ["4 m/s", "√15 m/s", "√5 m/s"], "B"),
    "Equation of continuity with Bernoulli's principle",
    "Continuity gives A₁v₁ = A₂v₂, so the water in the narrow part moves 4 times as fast. For a horizontal pipe "
    "Bernoulli's principle gives P₁ − P₂ = ½ρ(v₂² − v₁²).",
    ["v₂ = (A₁/A₂)v₁ = 4v₁", "7500 = ½ × 1000 × (16v₁² − v₁²) = 7500v₁²", "v₁ = 1 m/s (and v₂ = 4 m/s)"],
    why="4 m/s is the speed in the narrow part. √15 m/s uses ½ρv² = ΔP, ignoring the speed in the wide part and the "
        "continuity relation. √5 m/s takes the speed ratio as √4 = 2 instead of the area ratio 4.",
    ncert="Class 11 Physics, 'Mechanical Properties of Fluids', equation of continuity and Bernoulli's principle",
    seconds=80, recomputed=True)

Q_k = 1 * 4200 * 80
t_k = Q_k / (2000 * 0.8)
assert close(t_k, 210) and close(Q_k / 2000, 168) and close(Q_k / 2000 * 0.8, 134.4)
assert close(1 * 4200 * 100 / 1600, 262.5)
add(T, "Thermal expansion and calorimetry", "Intermediate", "numerical",
    "An electric kettle rated 2 kW heats 1 kg of water from 20 °C to 100 °C. Only 80% of the electrical energy "
    "supplied goes into the water. Taking the specific heat capacity of water as 4200 J kg⁻¹ K⁻¹, the time taken is:",
    place("210 s", ["168 s", "134.4 s", "262.5 s"], "A"),
    "Calorimetry with an efficiency",
    "The heat needed is mcΔT. The useful heating rate is 80% of 2 kW, i.e. 1600 W.",
    ["Q = 1 × 4200 × 80 = 336 000 J", "Useful power = 0.8 × 2000 = 1600 W", "t = 336 000/1600 = 210 s"],
    why="168 s ignores the efficiency. 134.4 s multiplies the time by 0.8 instead of dividing. 262.5 s takes the "
        "temperature rise as 100 °C instead of 80 °C.",
    ncert="Class 11 Physics, 'Thermal Properties of Matter', specific heat capacity", seconds=60, recomputed=True)

F_wall = 1000 * 10 * 3 * 2 ** 2 / 2
assert close(F_wall, 60000) and close(1000 * 10 * 2 * (3 * 2), 120000) and close(F_wall + 1e5 * 6, 660000)
add(T, "Fluid pressure and Pascal's law", "Advanced", "numerical",
    "A rectangular tank with vertical walls contains water to a depth of 2 m. One wall is 3 m wide. The atmospheric "
    "pressure acts on both the water surface and the outside of the wall. Taking the density of water as "
    "1000 kg/m³ and g = 10 m/s², the net horizontal force exerted on this wall is:",
    place("6.0 × 10⁴ N", ["1.2 × 10⁵ N", "6.6 × 10⁵ N", "3.0 × 10⁴ N"], "D"),
    "Force due to a pressure that varies with depth",
    "The gauge pressure ρgy increases linearly from zero at the surface to ρgh at the bottom. Since the atmosphere "
    "acts on both sides, only the gauge pressure produces a net force. For a linear variation the average gauge "
    "pressure is ρgh/2, acting over the area wh.",
    ["Average gauge pressure = ρgh/2 = 1000 × 10 × 2/2 = 1.0 × 10⁴ Pa",
     "Wetted area = 3 × 2 = 6 m²", "F = 1.0 × 10⁴ × 6 = 6.0 × 10⁴ N  (= ρgwh²/2)"],
    why="1.2 × 10⁵ N uses the pressure at the bottom for the whole wall. 6.6 × 10⁵ N adds the atmospheric force, "
        "which is cancelled by the atmosphere outside. 3.0 × 10⁴ N halves the result twice (ρgwh²/4).",
    ncert="Class 11 Physics, 'Mechanical Properties of Fluids', pressure and variation of pressure with depth",
    seconds=90, recomputed=True)

h_v = 4.0
l_tilt = h_v / math.cos(math.radians(60))
assert close(l_tilt, 8) and close(h_v * math.cos(math.radians(60)), 2) and close(h_v / math.sin(math.radians(60)), 4.62, 1e-3)
add(T, "Surface tension and capillarity", "Advanced", "numerical",
    "Water rises to a height of 4 cm in a clean, long glass capillary tube held vertically in a dish of water. The "
    "same tube is now held so that it makes an angle of 60° with the vertical, its lower end still dipping in the "
    "water. The length of the water column inside the tube is now:",
    place("8 cm", ["4 cm", "2 cm", "4.62 cm"], "C"),
    "Capillary rise in an inclined tube",
    "The weight of the raised liquid is balanced by the surface-tension force, which fixes the vertical height "
    "h = 2S cos θ/(rρg) of the meniscus above the outside level, whatever the tilt. In a tube tilted at 60° to the "
    "vertical, a vertical height h needs a column of length l with l cos 60° = h.",
    ["Vertical height stays h = 4 cm", "l = h/cos 60° = 4/0.5 = 8 cm"],
    why="4 cm forgets that the column now lies along a slant. 2 cm multiplies by cos 60° instead of dividing. "
        "4.62 cm uses sin 60°, the angle with the horizontal rather than with the vertical.",
    seconds=70, recomputed=True)

add(T, "Viscosity and Stokes' law", "Basic", "direct",
    "A liquid flows steadily (streamline flow) through a long horizontal pipe. Because of viscosity, the speed of the "
    "liquid is:",
    place("Greatest along the axis of the pipe and least at the walls",
          ["Greatest at the walls and least along the axis", "The same at every point of a cross-section",
           "Zero along the axis of the pipe"], "C"),
    "Velocity profile in viscous flow",
    "The layer in contact with the wall is held almost at rest, and each layer drags on its neighbours. The speed "
    "therefore increases from the wall towards the axis, where it is largest (a parabolic profile for steady flow "
    "in a tube).",
    ["Layer at the wall: v ≈ 0", "Speed increases inwards → maximum on the axis"],
    why="Equal speeds at all points would need zero viscosity. Larger speed at the walls or zero speed on the axis "
        "reverses the real profile.",
    ncert="Class 11 Physics, 'Mechanical Properties of Fluids', viscosity", seconds=25)

add(T, "Heat transfer", "Basic", "direct",
    "During the day, a cool breeze blows from the sea towards the land. This sea breeze is an example of heat "
    "transfer by:",
    place("Natural convection", ["Conduction", "Radiation alone", "Forced convection"], "B"),
    "Natural convection",
    "In the day the land heats up faster than the sea. The air over the land becomes warmer and lighter and rises, "
    "and cooler, denser air from over the sea moves in to take its place. Bulk movement of a fluid driven by "
    "density differences due to heating is natural convection.",
    ["Land warms faster → air above it rises", "Cool sea air flows in → convection current"],
    why="Conduction involves no bulk flow of the medium. Radiation heats the land but does not by itself move air. "
        "Forced convection needs a pump or fan.",
    ncert="Class 11 Physics, 'Thermal Properties of Matter', convection", seconds=25)

add(T, "Fluid pressure and Pascal's law", "Intermediate", "assertion_reason",
    AR_STEM.format(
        a="The force exerted by a liquid at rest on any surface in contact with it acts perpendicular to that "
          "surface.",
        r="A fluid at rest cannot sustain a shearing (tangential) stress."),
    ar("A"),
    "Why fluid pressure acts normally",
    "If a resting fluid exerted a tangential force on a surface, by the third law the surface would exert an equal "
    "tangential force back on the fluid. A fluid cannot resist a shearing stress, so it would start to flow, "
    "contradicting the assumption of rest. Hence the force must be normal.",
    ["A tangential component would make the fluid flow", "Fluid at rest → no tangential force → force is normal"],
    why="R is exactly the property that rules out a tangential component, so it explains A.",
    ncert="Class 11 Physics, 'Mechanical Properties of Fluids', pressure", seconds=45)

add(T, "Viscosity and Stokes' law", "Intermediate", "statement_pair",
    SP_STEM.format(
        s1="The coefficient of viscosity of a liquid decreases when its temperature rises, while that of a gas "
           "increases.",
        s2="In the steady (streamline) flow of a fluid, two streamlines can cross each other."),
    sp("C"),
    "Viscosity and temperature; streamlines",
    "Liquids become less viscous on heating, whereas the viscosity of gases increases with temperature, as NCERT "
    "notes. A streamline gives the direction of the velocity at each of its points; if two crossed, the fluid at the "
    "crossing would have two velocities at once, which is impossible in steady flow.",
    ["Statement I → true", "Statement II: unique velocity at each point → streamlines never cross → false"],
    why="The trap in Statement I is to assume gases behave like liquids; they do not.",
    ncert="Class 11 Physics, 'Mechanical Properties of Fluids', streamline flow and viscosity", seconds=45)

truth = [True, True, True, False, True]
multi_key(truth, "abce")
add(T, "Viscosity and Stokes' law", "Intermediate", "multi_statement",
    multi("Which of the following statements about the flow of fluids are correct?",
          ["In streamline flow, every fluid particle passing through a given point has the same velocity there.",
           "A flow becomes turbulent when its speed exceeds a certain critical value.",
           "Stokes' law, F = 6πηrv, gives the viscous drag on a small sphere moving slowly through a viscous fluid.",
           "The viscous force on a body moving through a fluid acts in the direction of its motion.",
           "When a sphere falling through a viscous liquid reaches its terminal velocity, the net force on it is "
           "zero."]),
    place("(a), (b), (c) and (e) only",
          ["(a), (b) and (c) only", "(b), (c), (d) and (e) only", "(a), (d) and (e) only"], "D"),
    "Streamline flow, critical speed and terminal velocity",
    "In steady flow the velocity at each point does not change with time, so every particle reaching a point has "
    "the same velocity there. Above a critical speed the flow becomes turbulent. Stokes' law holds for slow motion "
    "of a small sphere. Viscous drag opposes relative motion. At terminal velocity, weight = buoyancy + drag, so "
    "the net force (and acceleration) is zero.",
    ["(a) steady flow → true", "(b) critical speed → true", "(c) Stokes' law → true",
     "(d) drag opposes motion → false", "(e) constant velocity → zero net force → true"],
    why="Codes with (d) reverse the direction of the drag; codes without (e) miss that constant velocity means zero "
        "net force.",
    ncert="Class 11 Physics, 'Mechanical Properties of Fluids', streamline flow, viscosity and Stokes' law",
    seconds=70)

add(T, "Thermal expansion and calorimetry", "Advanced", "statement_pair",
    SP_STEM.format(
        s1="For an ideal gas at constant pressure, the coefficient of volume expansion is equal to 1/T, where T is "
           "its absolute temperature.",
        s2="For an isotropic solid, the coefficient of volume expansion is about three times its coefficient of "
           "linear expansion."),
    sp("A"),
    "Coefficients of expansion",
    "For an ideal gas PV = μRT; at constant pressure V ∝ T, so (1/V)(dV/dT) = 1/T, which decreases as the gas gets "
    "hotter. For a solid cube of side l, V = l³ and ΔV/V = 3Δl/l for small changes, so α_V = 3α_l.",
    ["Statement I: α_V = (1/V)(dV/dT)_P = 1/T → true", "Statement II: α_V = 3α_l → true"],
    why="Statement I may look odd because α_V is not a constant for a gas, but it is exactly 1/T at constant "
        "pressure.",
    ncert="Class 11 Physics, 'Thermal Properties of Matter', thermal expansion", seconds=60)

ratios = {"A": F(1, 2), "B": F(2) ** 2, "C": F(2), "D": F(2) * F(2) ** 2}
assert ratios == {"A": F(1, 2), "B": 4, "C": 2, "D": 8}
add(T, "Surface tension and capillarity", "Advanced", "match_list",
    match_stem("Match List-I (change made) with List-II (factor by which the stated quantity changes). Everything "
               "not mentioned stays the same.",
               ["The radius of a capillary tube is doubled: the height to which water rises in it",
                "The radius of a small sphere falling through a viscous liquid is doubled: its terminal velocity",
                "The radius of a soap bubble is halved: the excess pressure inside it",
                "The length of a wire is doubled and its diameter halved, with the same load: its extension"],
               ["2", "1/2", "8", "4"]),
    match_options({"A": "II", "B": "IV", "C": "I", "D": "III"},
                  [{"A": "I", "B": "IV", "C": "II", "D": "III"}, {"A": "II", "B": "I", "C": "IV", "D": "III"},
                   {"A": "II", "B": "IV", "C": "III", "D": "I"}], "B"),
    "Scaling laws for capillarity, Stokes' law, bubbles and elasticity",
    "Capillary rise h = 2S cos θ/(rρg) ∝ 1/r. Terminal velocity v = 2r²(ρ − σ)g/(9η) ∝ r². Excess pressure in a "
    "soap bubble = 4S/r ∝ 1/r. Extension ΔL = FL/(AY) with A ∝ d², so ΔL ∝ L/d².",
    ["A: h ∝ 1/r → ½ → II", "B: v ∝ r² → 4 → IV", "C: ΔP ∝ 1/r → 2 → I", "D: ΔL ∝ L/d² → 2 × 4 = 8 → III"],
    why="The other codes take capillary rise as proportional to r, terminal velocity as proportional to r, or the "
        "extension as depending on diameter rather than its square.",
    seconds=90)

truth = [True, True, True, False, False]
multi_key(truth, "abc")
add(T, "Thermal expansion and calorimetry", "Advanced", "multi_statement",
    multi("Which of the following statements about change of state are correct?",
          ["While a pure solid melts at constant pressure, its temperature remains constant.",
           "The latent heat of vaporisation of water is greater than its latent heat of fusion.",
           "The boiling point of water rises when the pressure on it is increased.",
           "The melting point of ice rises when the pressure on it is increased.",
           "The heat absorbed by ice while it melts at 0 °C increases the average kinetic energy of its "
           "molecules."]),
    place("(a), (b) and (c) only", ["(a), (b), (c) and (d) only", "(a), (c) and (e) only", "(b), (d) and (e) only"],
          "D"),
    "Change of state and latent heat",
    "During a change of state, heat goes into changing the arrangement of molecules (their potential energy), not "
    "their average kinetic energy, so the temperature stays constant. For water L_v ≈ 22.6 × 10⁵ J/kg and "
    "L_f ≈ 3.33 × 10⁵ J/kg. Increasing pressure raises the boiling point (as in a pressure cooker) but lowers the "
    "melting point of ice (regelation).",
    ["(a) constant temperature during melting → true", "(b) L_v > L_f for water → true",
     "(c) pressure cooker → true", "(d) melting point of ice falls with pressure → false",
     "(e) heat goes into potential energy, temperature constant → false"],
    why="Codes with (d) treat ice like substances that expand on melting; codes with (e) forget that the temperature "
        "(the measure of average kinetic energy) does not change while ice melts.",
    ncert="Class 11 Physics, 'Thermal Properties of Matter', change of state and latent heat", seconds=80)


# =====================================================================================================================
# Thermodynamics (B3 I4 A3)
# =====================================================================================================================
T = "Thermodynamics"

Q_in, W_by = -100, -300                          # heat released; work done ON the gas
assert Q_in - W_by == 200
add(T, "Zeroth and first law", "Basic", "numerical",
    "A gas is compressed: 300 J of work is done on it, and during the compression it gives out 100 J of heat to its "
    "surroundings. The change in its internal energy is:",
    place("+200 J (an increase)", ["+400 J (an increase)", "−400 J (a decrease)", "−200 J (a decrease)"], "B"),
    "First law of thermodynamics with signs",
    "ΔQ = ΔU + ΔW, where ΔQ is the heat supplied to the system and ΔW the work done by the system. Heat given out "
    "is negative, and work done on the gas means the work done by it is negative.",
    ["ΔQ = −100 J, ΔW = −300 J", "ΔU = ΔQ − ΔW = −100 − (−300) = +200 J"],
    why="+400 J adds the heat released instead of subtracting it. −400 J and −200 J get the sign of the work wrong: "
        "work done on a gas increases its internal energy.",
    ncert="Class 11 Physics, 'Thermodynamics', first law of thermodynamics", seconds=40, recomputed=True)

add(T, "Second law, reversible and irreversible processes", "Basic", "direct",
    "Which of the following processes is irreversible?",
    place("Heat flowing by itself from a hot body to a cold body in contact with it",
          ["A quasi-static isothermal expansion of an ideal gas in a cylinder with a frictionless piston",
           "A quasi-static adiabatic compression of an ideal gas in a cylinder with a frictionless piston",
           "A quasi-static isothermal compression of an ideal gas in a cylinder with a frictionless piston"], "C"),
    "Reversible and irreversible processes",
    "A process is reversible only if it is quasi-static (the system passes through equilibrium states) and has no "
    "dissipative effects such as friction. Heat conduction across a finite temperature difference cannot be "
    "reversed without producing other changes, so it is irreversible; spontaneous processes in nature are "
    "irreversible.",
    ["Quasi-static + no friction → reversible (the three piston processes)",
     "Spontaneous heat flow across a finite temperature difference → irreversible"],
    why="The three piston processes are carried out quasi-statically with no friction, which is exactly the "
        "condition NCERT gives for a reversible process.",
    ncert="Class 11 Physics, 'Thermodynamics', reversible and irreversible processes", seconds=30)

add(T, "Isothermal and adiabatic processes", "Basic", "match_list",
    match_stem("Match List-I (process undergone by a fixed amount of an ideal gas) with List-II (the relation that "
               "holds during it).",
               ["Isothermal", "Reversible adiabatic", "Isobaric", "Isochoric"],
               ["V/T = constant", "P/T = constant", "PV = constant", "PV^γ = constant"]),
    match_options({"A": "III", "B": "IV", "C": "I", "D": "II"},
                  [{"A": "IV", "B": "III", "C": "I", "D": "II"}, {"A": "III", "B": "IV", "C": "II", "D": "I"},
                   {"A": "III", "B": "I", "C": "IV", "D": "II"}], "A"),
    "Equations of state for special processes",
    "From PV = μRT: at constant T, PV is constant; at constant P, V ∝ T; at constant V, P ∝ T. For a reversible "
    "adiabatic process of an ideal gas, PV^γ is constant.",
    ["Isothermal → PV = const → III", "Adiabatic → PV^γ = const → IV", "Isobaric → V/T = const → I",
     "Isochoric → P/T = const → II"],
    why="The other codes swap the isothermal and adiabatic relations or the isobaric and isochoric ones.",
    ncert="Class 11 Physics, 'Thermodynamics', thermodynamic processes", seconds=40)

P_ratio = 2 ** 1.5
assert close(P_ratio, 2 * math.sqrt(2))
add(T, "Isothermal and adiabatic processes", "Intermediate", "numerical",
    "An ideal gas with γ = Cp/Cv = 1.5 is compressed reversibly and adiabatically to half its initial volume. If its "
    "initial pressure is P, its final pressure is:",
    place("2√2 P", ["2P", "4P", "√2 P"], "D"),
    "Reversible adiabatic process: PV^γ = constant",
    "For a reversible adiabatic process PV^γ is constant, so P₂ = P₁(V₁/V₂)^γ. The pressure rises more than in an "
    "isothermal compression, because the gas also gets hotter.",
    ["P₂ = P(2)^1.5", "= 2√2 P ≈ 2.83P"],
    why="2P is the isothermal result (PV constant). 4P uses an exponent of 2. √2 P uses an exponent of γ − 1 = 0.5, "
        "which belongs to TV^(γ−1).",
    ncert="Class 11 Physics, 'Thermodynamics', adiabatic process", seconds=45, recomputed=True)

assert close(math.log(2 / 1), math.log(4 / 2))
add(T, "Isothermal and adiabatic processes", "Intermediate", "numerical",
    "A fixed amount of an ideal gas expands reversibly and isothermally at temperature T, first from volume V to 2V "
    "and then, at the same temperature, from 2V to 4V. The ratio of the work done by the gas in the first expansion "
    "to that in the second is:",
    place("1 : 1", ["1 : 2", "2 : 1", "ln 2 : 1"], "B"),
    "Work in an isothermal process depends on the volume ratio",
    "For a reversible isothermal process of an ideal gas, W = μRT ln(V₂/V₁). Only the ratio of the volumes "
    "matters, and both stages double the volume.",
    ["W₁ = μRT ln(2V/V) = μRT ln 2", "W₂ = μRT ln(4V/2V) = μRT ln 2", "W₁ : W₂ = 1 : 1"],
    why="1 : 2 uses the volume changes V and 2V, as if the pressure were constant. 2 : 1 thinks the first stage, at "
        "higher pressure, does more work, forgetting that it also has a smaller volume change. ln 2 : 1 takes the "
        "logarithm of only one stage.",
    ncert="Class 11 Physics, 'Thermodynamics', isothermal process", seconds=50, recomputed=True)

add(T, "Zeroth and first law", "Intermediate", "assertion_reason",
    AR_STEM.format(
        a="When an ideal gas in a thermally insulated container expands suddenly into an evacuated region (free "
          "expansion), its internal energy does not change.",
        r="In free expansion heat flows into the gas from its surroundings, exactly balancing the work it does."),
    ar("C"),
    "Free expansion and the first law",
    "With ΔQ = 0 (insulated) and ΔW = 0 (nothing pushes back on the expanding gas), the first law gives ΔU = 0. "
    "For an ideal gas this also means that the temperature does not change.",
    ["ΔQ = 0 (insulated), ΔW = 0 (no external pressure)", "ΔU = ΔQ − ΔW = 0 → A true",
     "R: no heat can enter an insulated container, and no work is done → R false"],
    why="R is false: in free expansion both the heat and the work are zero; nothing flows in to balance anything.",
    ncert="Class 11 Physics, 'Thermodynamics', first law of thermodynamics", seconds=45)

add(T, "Zeroth and first law", "Intermediate", "statement_pair",
    SP_STEM.format(
        s1="In a reversible adiabatic expansion of an ideal gas, all the work done by the gas comes from its "
           "internal energy.",
        s2="Two systems in thermal equilibrium with each other must have the same internal energy."),
    sp("C"),
    "Adiabatic work; meaning of thermal equilibrium",
    "In an adiabatic process ΔQ = 0, so ΔW = −ΔU: the gas does work at the expense of its internal energy and cools. "
    "Thermal equilibrium means equal temperatures, not equal internal energies; a large and a small body at the same "
    "temperature have very different internal energies.",
    ["Statement I: ΔQ = 0 → ΔW = −ΔU → true", "Statement II: equilibrium → same temperature only → false"],
    why="Statement II confuses temperature (an intensive variable) with internal energy (an extensive one).",
    ncert="Class 11 Physics, 'Thermodynamics', zeroth law and adiabatic process", seconds=45)

R_ = 8.3
Q_iso = 1 * R_ * 400 * 0.693
Q_isoch = 1 * 1.5 * R_ * (300 - 400)
assert close(Q_iso, 2300.8, 1e-4) and close(Q_isoch, -1245) and round(Q_iso + Q_isoch) == 1056
assert round(Q_iso - Q_isoch) == 3546 and round(Q_iso - 2.5 * R_ * 100) == 226
add(T, "Isothermal and adiabatic processes", "Advanced", "numerical",
    "One mole of a monatomic ideal gas first expands reversibly and isothermally at 400 K until its volume doubles. "
    "It is then cooled at constant volume until its temperature is 300 K. Taking R = 8.3 J mol⁻¹ K⁻¹ and "
    "ln 2 = 0.693, the net heat absorbed by the gas in the two processes is about:",
    place("1056 J", ["2301 J", "3546 J", "226 J"], "B"),
    "First law over a two-step process",
    "In the isothermal step ΔU = 0, so the heat absorbed equals the work done, μRT ln(V₂/V₁). In the isochoric step "
    "no work is done, so the heat is μC_vΔT with C_v = 3R/2 for a monatomic gas; ΔT is negative, so heat is given "
    "out.",
    ["Isothermal: Q₁ = 1 × 8.3 × 400 × 0.693 ≈ +2301 J",
     "Isochoric: Q₂ = 1 × (3/2) × 8.3 × (300 − 400) = −1245 J", "Net Q = 2301 − 1245 ≈ 1056 J"],
    why="2301 J leaves out the heat given out during cooling. 3546 J adds it with the wrong sign. 226 J uses "
        "C_p = 5R/2 for the constant-volume step.",
    ncert="Class 11 Physics, 'Thermodynamics', thermodynamic processes", seconds=110, recomputed=True)

P1, V1, P2, gam = 8e5, 1e-3, 1e5, 1.5
V2 = V1 * (P1 / P2) ** (1 / gam)
W_ad = (P1 * V1 - P2 * V2) / (gam - 1)
assert close(V2, 4e-3) and close(W_ad, 800)
assert close(P1 * V1 - P2 * V2, 400) and close(P1 * V1 * math.log(4), 1109, 1e-3)
add(T, "Isothermal and adiabatic processes", "Advanced", "numerical",
    "An ideal gas with γ = 1.5 is initially at a pressure of 8 × 10⁵ Pa and occupies 1 L. It expands reversibly and "
    "adiabatically until its pressure falls to 1 × 10⁵ Pa. The work done by the gas is:",
    place("800 J", ["400 J", "1109 J", "0 J"], "D"),
    "Work done in a reversible adiabatic process",
    "First find the final volume from PV^γ = constant, then use W = (P₁V₁ − P₂V₂)/(γ − 1), which follows from "
    "W = −ΔU = μC_v(T₁ − T₂).",
    ["V₂ = V₁(P₁/P₂)^(1/γ) = 1 L × 8^(2/3) = 4 L",
     "P₁V₁ = 800 J, P₂V₂ = 1 × 10⁵ × 4 × 10⁻³ = 400 J", "W = (800 − 400)/(1.5 − 1) = 800 J"],
    why="400 J forgets to divide by γ − 1. 1109 J uses the isothermal formula P₁V₁ ln(V₂/V₁). 0 J finds V₂ from "
        "Boyle's law (8 L), which makes P₁V₁ = P₂V₂.",
    ncert="Class 11 Physics, 'Thermodynamics', adiabatic process", seconds=120, recomputed=True)

truth = [True, True, False, True, False]
multi_key(truth, "abd")
add(T, "Second law, reversible and irreversible processes", "Advanced", "multi_statement",
    multi("Which of the following statements are correct?",
          ["A reversible process must be quasi-static.",
           "A process in which work is lost to friction is irreversible.",
           "Every quasi-static process is reversible, whether or not friction is present.",
           "Spontaneous natural processes, such as the free expansion of a gas, are irreversible.",
           "A quasi-static process may pass through states in which the system is far from equilibrium with its "
           "surroundings."]),
    place("(a), (b) and (d) only", ["(a), (b), (c) and (d) only", "(b), (c) and (e) only", "(a), (d) and (e) only"],
          "A"),
    "Reversibility and the second law",
    "A reversible process needs two things: it must be quasi-static and free of dissipative effects. Friction "
    "makes a quasi-static process irreversible, so being quasi-static is necessary but not sufficient. Natural "
    "spontaneous processes are irreversible. A quasi-static process is, by definition, carried out so slowly that "
    "the system stays in equilibrium (thermal and mechanical) with its surroundings at every stage.",
    ["(a) quasi-static is necessary → true", "(b) dissipation → irreversible → true",
     "(c) quasi-static with friction is irreversible → false", "(d) spontaneous → irreversible → true",
     "(e) a quasi-static process passes only through equilibrium states → false"],
    why="Codes with (c) treat 'quasi-static' and 'reversible' as the same thing; codes with (e) contradict the "
        "meaning of a quasi-static process.",
    ncert="Class 11 Physics, 'Thermodynamics', second law and reversible and irreversible processes", seconds=80)


# =====================================================================================================================
# Kinetic Theory of Gases (B2 I3 A2)
# =====================================================================================================================
T = "Kinetic Theory of Gases"

f_poly = 6
Cv_poly, Cp_poly = f_poly / 2 * 8.3, (f_poly / 2 + 1) * 8.3
assert close(Cp_poly, 33.2) and close(Cv_poly, 24.9) and close(3.5 * 8.3, 29.05) and close(5 * 8.3, 41.5)
add(T, "Degrees of freedom and equipartition", "Basic", "numerical",
    "A polyatomic gas has rigid, non-linear molecules, each with 3 translational and 3 rotational degrees of freedom "
    "(vibrations are not excited). Using the law of equipartition of energy and taking R = 8.3 J mol⁻¹ K⁻¹, its "
    "molar specific heat at constant pressure is:",
    place("33.2 J mol⁻¹ K⁻¹", ["24.9 J mol⁻¹ K⁻¹", "29.05 J mol⁻¹ K⁻¹", "41.5 J mol⁻¹ K⁻¹"], "C"),
    "Specific heats from equipartition",
    "Each degree of freedom contributes ½k_BT per molecule, i.e. ½RT per mole. With f = 6, U = 3RT per mole, so "
    "C_v = 3R; for an ideal gas C_p = C_v + R = 4R.",
    ["f = 3 + 3 = 6", "C_v = (f/2)R = 3R = 24.9 J mol⁻¹ K⁻¹", "C_p = C_v + R = 4R = 33.2 J mol⁻¹ K⁻¹"],
    why="24.9 J mol⁻¹ K⁻¹ is C_v, not C_p. 29.05 J mol⁻¹ K⁻¹ is 7R/2, the C_p of a rigid diatomic gas (f = 5). "
        "41.5 J mol⁻¹ K⁻¹ is 5R, which adds 2R instead of R.",
    ncert="Class 11 Physics, 'Kinetic Theory', specific heat capacity of polyatomic gases", seconds=45,
    recomputed=True)

add(T, "Pressure and rms speed", "Basic", "match_list",
    match_stem("A fixed amount of an ideal gas is used throughout. Match List-I (change) with List-II (factor by "
               "which the stated quantity changes).",
               ["Absolute temperature doubled at constant volume: the pressure",
                "Absolute temperature doubled: the rms speed of the molecules",
                "Gas replaced by another gas of 4 times the molar mass at the same temperature: the rms speed",
                "Pressure doubled and volume doubled: the absolute temperature"],
               ["4", "1/2", "2", "√2"]),
    match_options({"A": "III", "B": "IV", "C": "II", "D": "I"},
                  [{"A": "IV", "B": "III", "C": "II", "D": "I"}, {"A": "III", "B": "IV", "C": "I", "D": "II"},
                   {"A": "III", "B": "II", "C": "IV", "D": "I"}], "B"),
    "Ideal gas equation and rms speed",
    "PV = μRT gives P ∝ T at constant V and T ∝ PV. The rms speed is v_rms = √(3RT/M), so v_rms ∝ √T and "
    "v_rms ∝ 1/√M.",
    ["A: P ∝ T → 2 → III", "B: v_rms ∝ √T → √2 → IV", "C: v_rms ∝ 1/√M → 1/2 → II", "D: T ∝ PV → 2 × 2 = 4 → I"],
    why="The other codes give the rms speed a linear dependence on T, or take T ∝ P/V instead of PV.",
    ncert="Class 11 Physics, 'Kinetic Theory', kinetic interpretation of temperature", seconds=50)

n_d, d_m = 2.5e25, 3e-10
lam = 1 / (math.sqrt(2) * math.pi * d_m ** 2 * n_d)
assert close(lam, 1.0e-7, 1e-2)
assert close(1 / (math.pi * d_m ** 2 * n_d), 1.41e-7, 1e-2) and close(1 / (math.sqrt(2) * math.pi * (2 * d_m) ** 2 * n_d), 2.5e-8, 1e-2)
assert close(1 / (2 * math.pi * d_m ** 2 * n_d), 7.07e-8, 1e-2)
add(T, "Mean free path", "Intermediate", "numerical",
    "A gas contains 2.5 × 10²⁵ molecules per cubic metre, and the diameter of each molecule is 3 × 10⁻¹⁰ m. Using "
    "the kinetic-theory expression for the mean free path, its value is about:",
    place("1.0 × 10⁻⁷ m", ["1.4 × 10⁻⁷ m", "2.5 × 10⁻⁸ m", "7.1 × 10⁻⁸ m"], "D"),
    "Mean free path",
    "A molecule of diameter d collides with every molecule whose centre lies within a distance d of its path. "
    "Allowing for the motion of the other molecules, l = 1/(√2 nπd²).",
    ["nπd² = 2.5 × 10²⁵ × π × 9 × 10⁻²⁰ ≈ 7.07 × 10⁶ m⁻¹",
     "l = 1/(√2 × 7.07 × 10⁶) ≈ 1.0 × 10⁻⁷ m"],
    why="1.4 × 10⁻⁷ m leaves out the factor √2. 2.5 × 10⁻⁸ m treats the given diameter as a radius. 7.1 × 10⁻⁸ m "
        "divides by 2 instead of √2.",
    ncert="Class 11 Physics, 'Kinetic Theory', mean free path", seconds=60, recomputed=True)

U_mix = 2 * F(5, 2) + 3 * F(3, 2)
assert U_mix == F(19, 2) and 5 * F(5, 2) == F(25, 2) and 5 * F(3, 2) == F(15, 2)
add(T, "Degrees of freedom and equipartition", "Intermediate", "numerical",
    "A container holds a mixture of 2 moles of oxygen (rigid diatomic molecules) and 3 moles of argon (monatomic), "
    "both treated as ideal gases, at absolute temperature T. Ignoring vibrational motion, the total internal energy "
    "of the mixture is (R is the gas constant):",
    place("9.5RT", ["12.5RT", "7.5RT", "19RT"], "C"),
    "Internal energy from equipartition",
    "For an ideal gas the internal energy is the kinetic energy of its molecules. A rigid diatomic molecule has 5 "
    "degrees of freedom (U = 5RT/2 per mole); a monatomic molecule has 3 (U = 3RT/2 per mole). Add the two "
    "contributions.",
    ["Oxygen: 2 × (5/2)RT = 5RT", "Argon: 3 × (3/2)RT = 4.5RT", "Total = 9.5RT"],
    why="12.5RT treats all 5 moles as diatomic and 7.5RT treats all 5 as monatomic. 19RT gives each degree of "
        "freedom RT per mole instead of RT/2.",
    ncert="Class 11 Physics, 'Kinetic Theory', law of equipartition of energy", seconds=60, recomputed=True)

add(T, "Pressure and rms speed", "Intermediate", "assertion_reason",
    AR_STEM.format(
        a="When a fixed amount of an ideal gas is compressed isothermally to a smaller volume, its pressure "
          "increases.",
        r="When the gas is compressed isothermally, its molecules move faster and so strike the walls harder."),
    ar("C"),
    "Kinetic interpretation of pressure",
    "P = (1/3)nm v²_rms (n = number per unit volume). At constant T, v_rms is fixed; halving the volume doubles n, so "
    "the rate of collisions with unit area of the wall, and hence the pressure, doubles (Boyle's law).",
    ["P = (1/3)nm v²_rms", "T constant → v_rms constant; V smaller → n larger → P larger → A true",
     "R: v_rms depends only on T, which is constant → molecules do not move faster → R false"],
    why="R is false: the molecules' average speed is fixed by the temperature; the pressure rises because there are "
        "more molecules per unit volume, not because they move faster.",
    ncert="Class 11 Physics, 'Kinetic Theory', pressure of an ideal gas", seconds=45)

U_before = 1 * F(5, 2)
U_after = 2 * F(3, 2)
assert U_after / U_before == F(6, 5)
add(T, "Degrees of freedom and equipartition", "Advanced", "numerical",
    "A sealed rigid vessel contains oxygen as rigid diatomic molecules (O₂) at absolute temperature T. All the "
    "molecules are then dissociated into oxygen atoms, and the gas is brought back to the same temperature T. "
    "Treating both as ideal gases and counting only the kinetic energy of translation and rotation, the ratio of "
    "the internal energy of the atomic gas to that of the original molecular gas is:",
    place("6/5", ["2", "3/5", "5/3"], "D"),
    "Equipartition and number of particles",
    "Dissociation doubles the number of particles. Each O₂ molecule has 5 degrees of freedom (3 translational, 2 "
    "rotational); each O atom has 3 translational degrees of freedom. Each degree of freedom carries ½k_BT on "
    "average.",
    ["Before: N molecules × (5/2)k_BT", "After: 2N atoms × (3/2)k_BT = 3Nk_BT",
     "Ratio = 3/(5/2) = 6/5"],
    why="2 counts only the doubling of the number of particles. 3/5 ignores that doubling. 5/3 is γ of a "
        "monatomic gas, not an energy ratio.",
    seconds=90, recomputed=True)

add(T, "Degrees of freedom and equipartition", "Advanced", "statement_pair",
    SP_STEM.format(
        s1="At the same temperature, the average total kinetic energy of a molecule of a rigid diatomic gas is "
           "greater than that of a molecule of a monatomic gas.",
        s2="According to the law of equipartition of energy, each vibrational mode of a molecule has an average "
           "energy of ½k_BT."),
    sp("C"),
    "Equipartition for translation, rotation and vibration",
    "A rigid diatomic molecule has 3 translational and 2 rotational degrees of freedom, so its average kinetic "
    "energy is (5/2)k_BT against (3/2)k_BT for a monatomic molecule. A vibrational mode has both kinetic and "
    "potential energy terms, so it carries 2 × ½k_BT = k_BT.",
    ["Statement I: (5/2)k_BT > (3/2)k_BT → true", "Statement II: vibration → k_BT, not ½k_BT → false"],
    why="Statement II forgets the potential-energy term of a vibration; only the average translational kinetic "
        "energy, (3/2)k_BT, is the same for all gases at a given temperature.",
    ncert="Class 11 Physics, 'Kinetic Theory', law of equipartition of energy", seconds=60)


# =====================================================================================================================
# Oscillations and Waves (B4 I5 A4)
# =====================================================================================================================
T = "Oscillations and Waves"

E_shm = 0.5 * 50 * 0.1 ** 2
assert close(E_shm, 0.25) and close(50 * 0.1 ** 2, 0.5) and close(0.5 * 50 * 0.1, 2.5) and close(50 * 0.1, 5)
add(T, "Energy in SHM", "Basic", "numerical",
    "A block of mass 0.2 kg attached to a light spring of force constant 50 N/m oscillates on a smooth horizontal "
    "surface with an amplitude of 10 cm. The total mechanical energy of the oscillation is:",
    place("0.25 J", ["0.5 J", "2.5 J", "5 J"], "B"),
    "Energy of a spring–block oscillator",
    "At the extreme position the block is momentarily at rest, so all the energy is the spring's potential energy, "
    "½kA². The total energy stays the same throughout the motion and does not depend on the mass.",
    ["A = 0.1 m", "E = ½kA² = ½ × 50 × 0.01 = 0.25 J"],
    why="0.5 J drops the ½. 2.5 J uses ½kA without squaring the amplitude. 5 J uses kA, which is the maximum "
        "force in newtons, not an energy.",
    ncert="Class 11 Physics, 'Oscillations', energy in simple harmonic motion", seconds=35, recomputed=True)

f_open = 340 / (2 * 0.5)
assert f_open == 340 and 340 / (4 * 0.5) == 170 and 340 / 0.5 == 680 and 340 / (8 * 0.5) == 85
add(T, "Organ pipes and beats", "Basic", "numerical",
    "A pipe 50 cm long is open at both ends. Taking the speed of sound in air as 340 m/s and neglecting end "
    "corrections, the frequency of its fundamental mode is:",
    place("340 Hz", ["170 Hz", "680 Hz", "85 Hz"], "D"),
    "Fundamental mode of an open pipe",
    "An open end is a displacement antinode. The fundamental of a pipe open at both ends has antinodes at both "
    "ends and one node in the middle, so the pipe length is half a wavelength: λ = 2L.",
    ["λ = 2L = 1.0 m", "f = v/λ = 340/1.0 = 340 Hz"],
    why="170 Hz uses λ = 4L, which is the fundamental of a pipe closed at one end. 680 Hz uses λ = L (the second "
        "harmonic). 85 Hz uses λ = 8L.",
    ncert="Class 11 Physics, 'Waves', standing waves in pipes", seconds=35, recomputed=True)

L_sec = math.pi ** 2 * 2 ** 2 / (4 * math.pi ** 2)
assert close(L_sec, 1) and close(math.pi ** 2 * 1 ** 2 / (4 * math.pi ** 2), 0.25)
add(T, "Spring and pendulum oscillations", "Basic", "numerical",
    "A simple pendulum has a time period of 2 s for small oscillations at a place where g = π² m/s². Its length is:",
    place("1 m", ["2 m", "0.5 m", "0.25 m"], "A"),
    "Period of a simple pendulum",
    "For small oscillations T = 2π√(L/g), so L = gT²/(4π²).",
    ["L = π² × 2²/(4π²)", "L = 1 m"],
    why="2 m takes L proportional to T instead of T². 0.5 m halves the correct value. 0.25 m uses T = 1 s, "
        "confusing the period with the time for one swing from one side to the other.",
    ncert="Class 11 Physics, 'Oscillations', the simple pendulum", seconds=30, recomputed=True)

add(T, "SHM equation and phase", "Basic", "direct",
    "For a particle executing simple harmonic motion x = A sin ωt, the velocity leads the displacement in phase by:",
    place("π/2 rad", ["π rad", "Zero", "π/4 rad"], "B"),
    "Phase of velocity in SHM",
    "Differentiating x = A sin ωt gives v = Aω cos ωt = Aω sin(ωt + π/2). The velocity is a quarter cycle ahead of "
    "the displacement: it is greatest at the mean position, where the displacement is zero.",
    ["x = A sin ωt", "v = dx/dt = Aω cos ωt = Aω sin(ωt + π/2) → leads by π/2"],
    why="π rad is the phase difference between acceleration and displacement. Zero would make velocity greatest "
        "at the extremes. π/4 rad has no basis in the equation.",
    ncert="Class 11 Physics, 'Oscillations', velocity and acceleration in simple harmonic motion", seconds=30)

beats = 330 / 1.00 - 330 / 1.01
assert close(beats, 3.267, 1e-3) and round(beats, 1) == 3.3
add(T, "Organ pipes and beats", "Intermediate", "numerical",
    "Two sound waves of wavelengths 1.00 m and 1.01 m travel in air with a speed of 330 m/s. When both are heard "
    "together, the number of beats heard per second is about:",
    place("3.3", ["6.5", "1.6", "0.01"], "D"),
    "Beat frequency",
    "The beat frequency equals the difference of the two frequencies, f = v/λ for each wave.",
    ["f₁ = 330/1.00 = 330 Hz", "f₂ = 330/1.01 ≈ 326.7 Hz", "Beats per second = f₁ − f₂ ≈ 3.3"],
    why="6.5 doubles the difference, and 1.6 halves it; the beat frequency is exactly the difference of the "
        "frequencies. 0.01 is the difference of the wavelengths in metres, not of the frequencies.",
    ncert="Class 11 Physics, 'Waves', beats", seconds=50, recomputed=True)

lam_s = 2 * 0.6 / 3
v_s = 300 * lam_s
Tens = 0.01 * v_s ** 2
assert close(lam_s, 0.4) and close(v_s, 120) and close(Tens, 144)
assert close(0.01 * (300 * 0.2) ** 2, 36) and close(0.01 * (300 * 0.6) ** 2, 324) and close(0.01 * v_s, 1.2)
add(T, "Superposition and standing waves", "Intermediate", "numerical",
    "A string 60 cm long, with a linear mass density of 0.01 kg/m, is fixed at both ends. It vibrates at 300 Hz in "
    "a mode with three loops (segments) along its length. The tension in the string is:",
    place("144 N", ["36 N", "324 N", "1.2 N"], "B"),
    "Standing waves on a string",
    "Each loop of a standing wave is half a wavelength long, so three loops give L = 3λ/2. The wave speed is fλ, and "
    "for a stretched string v = √(T/μ), so T = μv².",
    ["λ = 2L/3 = 0.4 m", "v = fλ = 300 × 0.4 = 120 m/s", "T = μv² = 0.01 × 120² = 144 N"],
    why="36 N takes each loop as a full wavelength (λ = L/3 = 0.2 m). 324 N takes the whole length as "
        "one wavelength (λ = 0.6 m). 1.2 N uses T = μv instead of μv².",
    ncert="Class 11 Physics, 'Waves', standing waves and normal modes", seconds=70, recomputed=True)

T_vs = 2 * math.pi * math.sqrt(0.04 / math.pi ** 2)
assert close(T_vs, 0.4) and close(2 * math.pi * math.sqrt(0.04), 1.2566, 1e-3)
add(T, "Spring and pendulum oscillations", "Intermediate", "numerical",
    "A block hung from a light vertical spring stretches it by 4 cm when at rest. The block is pulled down slightly "
    "and released. Taking g = π² m/s², the period of its vertical oscillations is:",
    place("0.4 s", ["0.2 s", "4 s", "1.26 s"], "C"),
    "Period of a vertical spring–block system",
    "At equilibrium kx₀ = mg, so m/k = x₀/g. The period T = 2π√(m/k) = 2π√(x₀/g); gravity only shifts the mean "
    "position and does not change the period.",
    ["m/k = x₀/g = 0.04/π² s²", "T = 2π × 0.2/π = 0.4 s"],
    why="0.2 s drops the factor 2 in 2π. 4 s keeps x₀ in centimetres. 1.26 s leaves g out, using 2π√(x₀).",
    ncert="Class 11 Physics, 'Oscillations', oscillations due to a spring", seconds=50, recomputed=True)

Lo = 60
Lc = Lo / 4                              # v/(4Lc) = 2v/(2Lo)
assert Lc == 15 and Lo / 2 == 30 and Lo / 6 == 10
add(T, "Organ pipes and beats", "Advanced", "numerical",
    "The fundamental frequency of a pipe closed at one end is equal to the frequency of the first overtone of a pipe "
    "60 cm long that is open at both ends. Both pipes contain air at the same temperature. Neglecting end "
    "corrections, the length of the closed pipe is:",
    place("15 cm", ["30 cm", "10 cm", "60 cm"], "D"),
    "Harmonics of closed and open pipes",
    "A closed pipe has fundamental v/(4L_c). An open pipe has all harmonics nv/(2L_o); its first overtone is the "
    "second harmonic, 2v/(2L_o) = v/L_o.",
    ["v/(4L_c) = v/L_o", "L_c = L_o/4 = 60/4 = 15 cm"],
    why="30 cm equates the closed pipe's fundamental to the open pipe's fundamental v/(2L_o). 10 cm takes the "
        "first overtone of the open pipe as the third harmonic. 60 cm assumes equal lengths give equal "
        "frequencies.",
    ncert="Class 11 Physics, 'Waves', standing waves in pipes", seconds=80, recomputed=True)

T_ratio = math.sqrt(10 / (10 + 10 / 3))
assert close(T_ratio, math.sqrt(3) / 2)
add(T, "Spring and pendulum oscillations", "Advanced", "numerical",
    "A simple pendulum has a period T for small oscillations when it hangs in a lift at rest. The lift now moves "
    "upward with a constant acceleration of g/3. The period of small oscillations of the pendulum becomes:",
    place("(√3/2)T", ["(2/√3)T", "T", "(3/4)T"], "A"),
    "Pendulum in an accelerating frame",
    "In a frame accelerating upward with a, the bob behaves as if gravity were g + a (a pseudo-force ma acts "
    "downward). The period is 2π√(L/g_eff).",
    ["g_eff = g + g/3 = 4g/3", "T' = T√(g/g_eff) = T√(3/4) = (√3/2)T"],
    why="(2/√3)T uses g − a, which applies when the lift accelerates downward. T ignores the acceleration of the "
        "lift. (3/4)T forgets the square root.",
    seconds=70, recomputed=True)

add(T, "Spring and pendulum oscillations", "Intermediate", "assertion_reason",
    AR_STEM.format(
        a="A block attached to a horizontal spring on a smooth surface oscillates with the same period on the Moon "
          "as on the Earth.",
        r="The period of a spring–block system, T = 2π√(m/k), depends only on the mass and the force constant, not "
          "on the acceleration due to gravity."),
    ar("A"),
    "Period of a spring–block oscillator",
    "The restoring force comes from the spring (F = −kx), not from gravity. The mass and spring are the same on the "
    "Moon, so the period is unchanged; this is unlike a simple pendulum, whose restoring force is due to gravity.",
    ["T = 2π√(m/k)", "m and k unchanged → T unchanged"],
    why="R gives exactly the formula and the reason the period does not depend on g, so it explains A.",
    ncert="Class 11 Physics, 'Oscillations', oscillations due to a spring", seconds=40)

A_, w_ = 1.0, 1.0
assert close(w_ * math.sqrt(A_ ** 2 - (A_ / 2) ** 2), math.sqrt(3) / 2) and close(w_ ** 2 * A_ / 2, 0.5)
add(T, "SHM equation and phase", "Intermediate", "match_list",
    match_stem("A particle executes simple harmonic motion with amplitude A and angular frequency ω. Match List-I "
               "(quantity) with List-II (its value).",
               ["Speed at the mean position", "Magnitude of acceleration at an extreme position",
                "Speed at a displacement A/2 from the mean position",
                "Magnitude of acceleration at a displacement A/2 from the mean position"],
               ["(√3/2)Aω", "Aω²/2", "Aω", "Aω²"]),
    match_options({"A": "III", "B": "IV", "C": "I", "D": "II"},
                  [{"A": "III", "B": "IV", "C": "II", "D": "I"}, {"A": "IV", "B": "III", "C": "I", "D": "II"},
                   {"A": "I", "B": "IV", "C": "III", "D": "II"}], "B"),
    "Velocity and acceleration in SHM",
    "In SHM, v = ω√(A² − x²) and a = −ω²x. The speed is greatest at the mean position (x = 0) and the acceleration "
    "is greatest at the extremes (x = ±A).",
    ["A: v = ωA at x = 0 → III", "B: |a| = ω²A at x = A → IV",
     "C: v = ω√(A² − A²/4) = (√3/2)Aω → I", "D: |a| = ω²(A/2) → II"],
    why="The other codes swap the speed and the acceleration at x = A/2, or put the largest speed at the extreme "
        "position.",
    ncert="Class 11 Physics, 'Oscillations', velocity and acceleration in simple harmonic motion", seconds=60)

# particle velocity = −(ω/k) × slope for y = A sin(kx − ωt)
A0, k0, w0, x0, t0 = 0.1, 2.0, 5.0, 0.3, 0.7
vp = -A0 * w0 * math.cos(k0 * x0 - w0 * t0)
slope = A0 * k0 * math.cos(k0 * x0 - w0 * t0)
assert close(vp, -(w0 / k0) * slope)
add(T, "Progressive waves and wave speed", "Advanced", "statement_pair",
    SP_STEM.format(
        s1="When a wave travelling along a string is reflected from a free end, the reflected wave has no phase "
           "change.",
        s2="For a transverse wave y = A sin(kx − ωt) on a string, the velocity of a particle of the string at any "
           "point equals −(ω/k) times the slope ∂y/∂x of the string at that point."),
    sp("A"),
    "Reflection at an open boundary; particle velocity and slope",
    "At a rigid boundary the reflected wave is inverted (phase change π); at a free (open) boundary the end is an "
    "antinode and the reflected wave has no phase change. For y = A sin(kx − ωt), ∂y/∂t = −Aω cos(kx − ωt) and "
    "∂y/∂x = Ak cos(kx − ωt), so ∂y/∂t = −(ω/k)∂y/∂x = −v ∂y/∂x.",
    ["Statement I → true", "Statement II: ∂y/∂t = −(ω/k)(∂y/∂x) → true"],
    why="Statement II looks unfamiliar but follows directly from differentiating the wave equation; ω/k is the wave "
        "speed.",
    ncert="Class 11 Physics, 'Waves', reflection of waves and the displacement relation in a progressive wave",
    seconds=80)

# x = a sin ωt + b cos ωt has amplitude √(a² + b²)
a1, b1 = 3.0, 4.0
mx = max(a1 * math.sin(th_) + b1 * math.cos(th_) for th_ in [i * 0.001 for i in range(6284)])
assert close(mx, 5, 1e-4)
truth = [True, True, False, False, True]
multi_key(truth, "abe")
add(T, "SHM equation and phase", "Advanced", "multi_statement",
    multi("Which of the following statements are correct? (a, b, ω are positive constants.)",
          ["Every simple harmonic motion is periodic, but not every periodic motion is simple harmonic.",
           "x = a sin ωt + b cos ωt represents simple harmonic motion with amplitude √(a² + b²).",
           "x = sin ωt + sin 2ωt represents simple harmonic motion.",
           "x = e^(−ωt) represents a periodic motion.",
           "The projection, on a diameter, of a particle in uniform circular motion executes simple harmonic "
           "motion."]),
    place("(a), (b) and (e) only", ["(a), (b), (c) and (e) only", "(b), (c) and (d) only", "(a), (d) and (e) only"],
          "C"),
    "Periodic motion and simple harmonic motion",
    "SHM is the special periodic motion with x a single sinusoidal function of time. a sin ωt + b cos ωt can be "
    "written as √(a² + b²) sin(ωt + φ). The sum of sinusoids of different frequencies (ω and 2ω) is periodic but not "
    "SHM. e^(−ωt) only decreases and never repeats. The foot of the perpendicular from a particle in uniform "
    "circular motion on a diameter moves as x = A cos(ωt + φ).",
    ["(a) true", "(b) amplitude √(a² + b²) → true", "(c) two frequencies → not SHM → false",
     "(d) never repeats → not periodic → false", "(e) SHM and uniform circular motion → true"],
    why="Codes with (c) treat any periodic sum of sines as SHM; codes with (d) confuse a decaying function with a "
        "periodic one.",
    ncert="Class 11 Physics, 'Oscillations', periodic and oscillatory motions, SHM and uniform circular motion",
    seconds=80)


# =====================================================================================================================
# Electrostatics (B5 I7 A5)
# =====================================================================================================================
T = "Electrostatics"

e_c, m_e, m_p = 1.6e-19, 9.1e-31, 1.67e-27
a_e = e_c * 2e4 / m_e
assert close(a_e, 3.5e15, 5e-3) and close(e_c * 2e4 / m_p, 1.9e12, 1e-2) and close(m_e / (e_c * 2e4), 2.8e-16, 2e-2)
add(T, "Electric field and dipole", "Basic", "numerical",
    "An electron is in a uniform electric field of magnitude 2 × 10⁴ N/C. Taking e = 1.6 × 10⁻¹⁹ C and the mass of "
    "the electron as 9.1 × 10⁻³¹ kg, and neglecting gravity, the magnitude of its acceleration is about:",
    place("3.5 × 10¹⁵ m/s²", ["1.9 × 10¹² m/s²", "3.2 × 10⁻¹⁵ m/s²", "2.8 × 10⁻¹⁶ m/s²"], "C"),
    "Force on a charge in an electric field",
    "The field exerts a force F = qE on the electron (opposite to E, since its charge is negative). By Newton's "
    "second law a = eE/m.",
    ["F = eE = 1.6 × 10⁻¹⁹ × 2 × 10⁴ = 3.2 × 10⁻¹⁵ N", "a = F/m = 3.2 × 10⁻¹⁵/9.1 × 10⁻³¹ ≈ 3.5 × 10¹⁵ m/s²"],
    why="1.9 × 10¹² m/s² uses the proton's mass. 3.2 × 10⁻¹⁵ is the force in newtons, not the acceleration. "
        "2.8 × 10⁻¹⁶ m/s² inverts the ratio (m/eE).",
    ncert="Class 12 Physics, 'Electric Charges and Fields', electric field", seconds=40, recomputed=True)

W_q = 2e-6 * (400 - 100)
assert close(W_q, 6e-4) and close(2e-6 * 400, 8e-4) and close(2e-6 * 500, 1e-3)
add(T, "Electric potential and energy", "Basic", "numerical",
    "A charge of +2 μC is moved slowly by an external agent from a point where the electrostatic potential is 100 V "
    "to a point where it is 400 V. The work done by the external agent is:",
    place("6.0 × 10⁻⁴ J", ["8.0 × 10⁻⁴ J", "1.0 × 10⁻³ J", "−6.0 × 10⁻⁴ J"], "B"),
    "Work and potential difference",
    "The potential difference V_B − V_A is the work done by an external agent per unit positive charge in moving it "
    "slowly from A to B, so W = q(V_B − V_A); the path does not matter.",
    ["V_B − V_A = 400 − 100 = 300 V", "W = 2 × 10⁻⁶ × 300 = 6.0 × 10⁻⁴ J"],
    why="8.0 × 10⁻⁴ J uses only the final potential. 1.0 × 10⁻³ J adds the two potentials. −6.0 × 10⁻⁴ J is the "
        "work done by the field; moving a positive charge to a higher potential needs positive work by the agent.",
    ncert="Class 12 Physics, 'Electrostatic Potential and Capacitance', electrostatic potential", seconds=35,
    recomputed=True)

flux = 100 * 0.2 * math.cos(math.radians(60))
assert close(flux, 10) and close(100 * 0.2 * math.sin(math.radians(60)), 17.32, 1e-3)
add(T, "Gauss's law", "Basic", "numerical",
    "A flat surface of area 0.2 m² is placed in a uniform electric field of 100 N/C. The normal to the surface makes "
    "an angle of 60° with the field. The electric flux through the surface is:",
    place("10 N m² C⁻¹", ["17.3 N m² C⁻¹", "20 N m² C⁻¹", "500 N m² C⁻¹"], "D"),
    "Electric flux through a plane surface",
    "Flux = E · ΔS = EΔS cos θ, where θ is the angle between the field and the normal (area vector) of the "
    "surface.",
    ["Φ = 100 × 0.2 × cos 60°", "Φ = 20 × 0.5 = 10 N m² C⁻¹"],
    why="17.3 N m² C⁻¹ uses sin 60°, treating 60° as the angle between the field and the surface. 20 N m² C⁻¹ "
        "ignores the angle. 500 N m² C⁻¹ divides E by the area.",
    ncert="Class 12 Physics, 'Electric Charges and Fields', electric flux", seconds=35, recomputed=True)

add(T, "Gauss's law", "Basic", "direct",
    "A charged conductor in electrostatic equilibrium has a surface charge density σ at a certain point of its "
    "surface. The magnitude of the electric field just outside the conductor at that point is:",
    place("σ/ε₀", ["σ/(2ε₀)", "2σ/ε₀", "Zero"], "A"),
    "Field at the surface of a conductor",
    "Inside the conductor E = 0, and just outside, E is normal to the surface. A small Gaussian pillbox straddling "
    "the surface encloses charge σΔS, and only its outer face has flux EΔS, so E = σ/ε₀.",
    ["Flux through pillbox = EΔS (inside face: E = 0; sides: E ⊥ normal)", "EΔS = σΔS/ε₀ → E = σ/ε₀"],
    why="σ/(2ε₀) is the field of an isolated thin sheet of charge, which has field on both sides. 2σ/ε₀ has no "
        "basis. Zero is the field inside the conductor, not just outside it.",
    ncert="Class 12 Physics, 'Electrostatic Potential and Capacitance', electrostatics of conductors", seconds=30)

add(T, "Capacitors and dielectrics", "Basic", "match_list",
    match_stem("Match List-I (physical quantity) with List-II (its SI unit).",
               ["Capacitance", "Electric potential", "Surface charge density", "Linear charge density"],
               ["C m⁻¹", "J C⁻¹", "C V⁻¹", "C m⁻²"]),
    match_options({"A": "III", "B": "II", "C": "IV", "D": "I"},
                  [{"A": "II", "B": "III", "C": "IV", "D": "I"}, {"A": "III", "B": "II", "C": "I", "D": "IV"},
                   {"A": "IV", "B": "II", "C": "III", "D": "I"}], "C"),
    "Units of electrostatic quantities",
    "Capacitance C = Q/V, so its unit (the farad) is C V⁻¹. Potential is work per unit charge, J C⁻¹ (the volt). "
    "Surface charge density is charge per unit area and linear charge density is charge per unit length.",
    ["A: farad = C V⁻¹ → III", "B: volt = J C⁻¹ → II", "C: σ → C m⁻² → IV", "D: λ → C m⁻¹ → I"],
    why="The other codes swap capacitance with potential (inverting C = Q/V) or swap the surface and linear charge "
        "densities.",
    ncert="Class 12 Physics, 'Electrostatic Potential and Capacitance', capacitance", seconds=40)

k_e = 9e9
E_each = k_e * 2e-6 / 0.05 ** 2
E_net = 2 * E_each * (4 / 5)
assert close(E_each, 7.2e6) and close(E_net, 1.152e7) and close(2 * E_each * 0.6, 8.64e6)
add(T, "Coulomb's law and superposition", "Intermediate", "numerical",
    "Two point charges, each of +2 μC, are fixed at points A and B, 6 cm apart, in air. P is a point on the "
    "perpendicular bisector of AB, at a distance of 4 cm from the midpoint of AB. Taking 1/(4πε₀) = 9 × 10⁹ N m² C⁻², "
    "the magnitude of the electric field at P is about:",
    place("1.15 × 10⁷ N/C", ["1.44 × 10⁷ N/C", "8.64 × 10⁶ N/C", "Zero"], "B"),
    "Superposition of electric fields",
    "P is 5 cm from each charge (a 3-4-5 triangle). The two fields have equal magnitude; their components along AB "
    "cancel and their components along the bisector add.",
    ["AP = BP = √(3² + 4²) = 5 cm", "Each field = 9 × 10⁹ × 2 × 10⁻⁶/(0.05)² = 7.2 × 10⁶ N/C",
     "Along the bisector: cos α = 4/5 → E = 2 × 7.2 × 10⁶ × 0.8 ≈ 1.15 × 10⁷ N/C"],
    why="1.44 × 10⁷ N/C adds the magnitudes as if the fields were parallel. 8.64 × 10⁶ N/C adds the components "
        "along AB (which actually cancel) instead of those along the bisector. Zero is true only at the midpoint.",
    ncert="Class 12 Physics, 'Electric Charges and Fields', electric field due to a system of charges", seconds=80,
    recomputed=True)

v_el = math.sqrt(2 * e_c * 100 / m_e)
assert close(v_el, 5.93e6, 1e-3) and close(math.sqrt(e_c * 100 / m_e), 4.19e6, 1e-3)
assert close(math.sqrt(2 * e_c * 100 / m_p), 1.38e5, 1e-2)
add(T, "Electric potential and energy", "Intermediate", "numerical",
    "An electron starts from rest and is accelerated through a potential difference of 100 V. Taking "
    "e = 1.6 × 10⁻¹⁹ C and the mass of the electron as 9.1 × 10⁻³¹ kg, its final speed is about:",
    place("5.9 × 10⁶ m/s", ["4.2 × 10⁶ m/s", "3.5 × 10¹³ m/s", "1.4 × 10⁵ m/s"], "D"),
    "Energy gained in a potential difference",
    "The loss of electrostatic potential energy, eV, becomes kinetic energy: ½mv² = eV.",
    ["eV = 1.6 × 10⁻¹⁹ × 100 = 1.6 × 10⁻¹⁷ J", "v = √(2eV/m) = √(3.52 × 10¹³) ≈ 5.9 × 10⁶ m/s"],
    why="4.2 × 10⁶ m/s drops the factor 2 (uses √(eV/m)). 3.5 × 10¹³ is v² in m²/s², not the speed. "
        "1.4 × 10⁵ m/s uses the proton's mass.",
    ncert="Class 12 Physics, 'Electrostatic Potential and Capacitance', potential energy of a charge", seconds=50,
    recomputed=True)

eps0 = 8.85e-12
sigma = 8.85e-9
E_out = sigma * 0.1 ** 2 / (eps0 * 0.2 ** 2)
assert close(E_out, 250) and close(sigma / eps0, 1000) and close(sigma * 0.1 / (eps0 * 0.2), 500)
add(T, "Gauss's law", "Intermediate", "numerical",
    "A thin spherical shell of radius 10 cm carries a uniform surface charge density of 8.85 × 10⁻⁹ C/m². Taking "
    "ε₀ = 8.85 × 10⁻¹² C² N⁻¹ m⁻², the magnitude of the electric field at a distance of 20 cm from its centre is:",
    place("250 N/C", ["1000 N/C", "500 N/C", "125 N/C"], "C"),
    "Field outside a uniformly charged thin spherical shell",
    "By Gauss's law, outside the shell the field is as if the whole charge q = 4πR²σ were at the centre: "
    "E = q/(4πε₀r²) = σR²/(ε₀r²).",
    ["σ/ε₀ = 8.85 × 10⁻⁹/8.85 × 10⁻¹² = 1000 N/C (the field just outside the shell)",
     "E(r) = (σ/ε₀)(R/r)² = 1000 × (10/20)² = 250 N/C"],
    why="1000 N/C is the field just outside the surface (r = R). 500 N/C uses R/r instead of (R/r)². 125 N/C "
        "starts from the sheet formula σ/(2ε₀).",
    ncert="Class 12 Physics, 'Electric Charges and Fields', field due to a uniformly charged thin spherical shell",
    seconds=60, recomputed=True)

dVdx = lambda x: 10 * x - 10
assert -dVdx(2) == -10 and 5 * 2 ** 2 - 10 * 2 == 0
add(T, "Electric potential and energy", "Intermediate", "numerical",
    "In a certain region the electric potential varies along the x-axis as V = 5x² − 10x, where V is in volts and x "
    "in metres; it does not depend on y or z. The electric field at x = 2 m is:",
    place("10 V/m, directed along −x", ["10 V/m, directed along +x", "Zero", "20 V/m, directed along −x"], "B"),
    "Electric field as the negative potential gradient",
    "E = −dV/dx. The field points in the direction in which the potential decreases fastest.",
    ["dV/dx = 10x − 10 → 10 V/m at x = 2 m", "Eₓ = −10 V/m → magnitude 10 V/m along −x"],
    why="'+x' forgets the minus sign in E = −dV/dx. 'Zero' uses the value of V at x = 2 m (which happens to be zero) "
        "instead of its slope. 20 V/m differentiates only the 5x² term.",
    ncert="Class 12 Physics, 'Electrostatic Potential and Capacitance', relation between field and potential",
    seconds=50, recomputed=True)

add(T, "Electric field and dipole", "Intermediate", "assertion_reason",
    AR_STEM.format(
        a="In electrostatics, the electric field just outside the surface of a charged conductor is normal to the "
          "surface at every point.",
        r="If the field had a component tangential to the surface, it would make the free charges on the surface "
          "move along it, so the charges could not be in equilibrium."),
    ar("A"),
    "Field at the surface of a conductor",
    "Electrostatics means the charges are at rest. A tangential component of E would push the free charges along "
    "the surface, so in equilibrium the tangential component must vanish and E is normal to the surface.",
    ["Equilibrium → no force along the surface on free charges", "→ tangential E = 0 → E normal to surface"],
    why="R is the very argument that proves A, so it explains A.",
    ncert="Class 12 Physics, 'Electrostatic Potential and Capacitance', electrostatics of conductors", seconds=45)

Cc = F(6)
ser = lambda *cs: 1 / sum(1 / c for c in cs)
vals = {"A": ser(Cc, Cc, Cc), "B": 3 * Cc, "C": ser(Cc, Cc) + Cc, "D": ser(Cc + Cc, Cc)}
assert vals == {"A": 2, "B": 18, "C": 9, "D": 4}
add(T, "Capacitors and dielectrics", "Intermediate", "match_list",
    match_stem("Three identical capacitors, each of capacitance 6 μF, are connected in different ways. Match List-I "
               "(arrangement) with List-II (equivalent capacitance).",
               ["All three in series", "All three in parallel",
                "Two in series, and this pair in parallel with the third",
                "Two in parallel, and this pair in series with the third"],
               ["9 μF", "18 μF", "4 μF", "2 μF"]),
    match_options({"A": "IV", "B": "II", "C": "I", "D": "III"},
                  [{"A": "IV", "B": "II", "C": "III", "D": "I"}, {"A": "II", "B": "IV", "C": "I", "D": "III"},
                   {"A": "III", "B": "II", "C": "I", "D": "IV"}], "D"),
    "Series and parallel combinations of capacitors",
    "In parallel, capacitances add. In series, the reciprocals add.",
    ["A: 1/C = 3/6 → 2 μF → IV", "B: 3 × 6 = 18 μF → II", "C: (6 × 6)/(6 + 6) = 3 μF, plus 6 μF → 9 μF → I",
     "D: 6 + 6 = 12 μF in series with 6 μF → (12 × 6)/18 = 4 μF → III"],
    why="The other codes swap the two mixed arrangements, or swap the all-series and all-parallel values, as if "
        "capacitors combined like resistors.",
    ncert="Class 12 Physics, 'Electrostatic Potential and Capacitance', combination of capacitors", seconds=70)

truth = [True, True, False, False, True]
multi_key(truth, "abe")
add(T, "Gauss's law", "Intermediate", "multi_statement",
    multi("Which of the following statements about Gauss's law are correct?",
          ["It holds for any closed surface, whatever its shape or size.",
           "The total electric flux through a closed surface depends only on the net charge enclosed by it.",
           "The electric field at each point of a Gaussian surface is produced only by the charges enclosed by the "
           "surface.",
           "If the net electric flux through a closed surface is zero, there can be no charge anywhere inside the "
           "surface.",
           "It is especially useful for finding the electric field when the charge distribution has a symmetry."]),
    place("(a), (b) and (e) only", ["(a), (b), (c) and (e) only", "(b), (d) and (e) only", "(a), (c) and (d) only"],
          "C"),
    "Gauss's law",
    "Φ = q_enclosed/ε₀ for any closed surface. The field on the surface, however, is due to all charges, inside "
    "and outside; outside charges just contribute zero net flux. Zero flux means zero net enclosed charge, which "
    "can be equal positive and negative charges. Symmetry (spherical, cylindrical, planar) lets E be taken out of "
    "the flux integral.",
    ["(a) true", "(b) true", "(c) outside charges also contribute to E → false",
     "(d) e.g. +q and −q inside give zero flux → false", "(e) true"],
    why="Codes with (c) confuse the flux (which depends only on enclosed charge) with the field (which does not); "
        "codes with (d) confuse zero net charge with no charge.",
    ncert="Class 12 Physics, 'Electric Charges and Fields', Gauss's law", seconds=70)

y_def = 0.5 * (e_c * 4.55e3 / m_e) * (0.1 / 2e7) ** 2
assert close(e_c * 4.55e3 / m_e, 8e14) and close(y_def, 0.01)
assert close(0.5 * (e_c * 4.55e3 / m_p) * (0.1 / 2e7) ** 2 * 100, 5.4e-4, 1e-2)
add(T, "Electric field and dipole", "Advanced", "numerical",
    "An electron enters the region between two parallel plates moving parallel to the plates with a speed of "
    "2 × 10⁷ m/s. The plates are 10 cm long, and the uniform electric field between them, perpendicular to the "
    "plates, is 4.55 × 10³ N/C. Taking e = 1.6 × 10⁻¹⁹ C and the electron's mass as 9.1 × 10⁻³¹ kg, and neglecting "
    "gravity and edge effects, how far is the electron deflected (perpendicular to the plates) by the time it leaves "
    "the plates? (It does not strike a plate.)",
    place("1.0 cm", ["2.0 cm", "Zero", "5.4 × 10⁻⁴ cm"], "B"),
    "Motion of a charge in a uniform electric field",
    "Along the plates there is no force, so the electron keeps its speed and spends t = L/v between them. "
    "Perpendicular to the plates it starts from rest with a constant acceleration eE/m, like a projectile.",
    ["t = 0.10/(2 × 10⁷) = 5 × 10⁻⁹ s", "a = eE/m = 1.6 × 10⁻¹⁹ × 4.55 × 10³/9.1 × 10⁻³¹ = 8 × 10¹⁴ m/s²",
     "y = ½at² = ½ × 8 × 10¹⁴ × 25 × 10⁻¹⁸ = 1.0 × 10⁻² m = 1.0 cm"],
    why="2.0 cm drops the ½ in ½at². 'Zero' assumes a field perpendicular to the velocity cannot deflect the "
        "electron. 5.4 × 10⁻⁴ cm uses the proton's mass.",
    seconds=110, recomputed=True)

Vx = lambda x: 4 / abs(x) - 1 / abs(x - 3)
assert abs(Vx(2.4)) < 1e-12 and abs(Vx(4.0)) < 1e-12
assert all(Vx(-x) > 0 for x in (0.5, 1, 3, 10, 100))                  # no zero on the negative axis
assert close(4 / 6 ** 2, 1 / 3 ** 2)                                   # x = 6 m is where E (not V) is zero
add(T, "Electric potential and energy", "Advanced", "numerical",
    "A point charge of +4 μC is fixed at the origin and a point charge of −1 μC is fixed at x = 3 m on the x-axis. "
    "At which point(s) on the x-axis, at finite distance, is the electrostatic potential zero?",
    place("At x = 2.4 m and at x = 4 m", ["At x = 2.4 m only", "At x = 6 m only", "At x = 4 m only"], "C"),
    "Zero-potential points of two unlike charges",
    "Potential is a scalar: V = k(4 μC)/|x| − k(1 μC)/|x − 3|. Set V = 0 separately in each region of the axis. "
    "Zeros lie nearer the smaller charge.",
    ["Between the charges (0 < x < 3): 4/x = 1/(3 − x) → x = 2.4 m",
     "Beyond the −1 μC charge (x > 3): 4/x = 1/(x − 3) → x = 4 m",
     "For x < 0: 4/|x| > 1/(|x| + 3) always → no zero"],
    why="'2.4 m only' and '4 m only' each miss one region. 'x = 6 m' is where the electric field, not the "
        "potential, is zero (4/x² = 1/(x − 3)²).",
    seconds=100, recomputed=True)

add(T, "Electric field and dipole", "Advanced", "statement_pair",
    SP_STEM.format(
        s1="A small positive test charge placed at rest at a point in an electrostatic field always moves along the "
           "electric field line passing through that point.",
        s2="Electrostatic field lines form closed loops."),
    sp("B"),
    "Meaning of field lines",
    "A field line gives the direction of the force, i.e. of the acceleration, not of the velocity. On a curved field "
    "line the charge, once moving, cannot follow the curve exactly (its velocity lags behind the changing "
    "direction of the force), so it leaves the line; it follows the line only if the line is straight. "
    "Electrostatic field lines start on positive charges and end on negative charges (or at infinity), so they "
    "never form closed loops.",
    ["Statement I: true only for straight field lines → false as a general statement",
     "Statement II: electrostatic field is conservative → no closed loops → false"],
    why="Statement I is a common misreading of field lines as trajectories; Statement II describes magnetic field "
        "lines, not electrostatic ones.",
    ncert="Class 12 Physics, 'Electric Charges and Fields', electric field lines", seconds=60)

truth = [True, True, True, True, False]
multi_key(truth, "abcd")
add(T, "Electric potential and energy", "Advanced", "multi_statement",
    multi("Which of the following statements about electric field and potential in electrostatics are correct?",
          ["The electric field points in the direction in which the potential decreases.",
           "In a region where the potential is the same at every point, the electric field is zero.",
           "The magnitude of the electric field equals the rate of decrease of potential with distance, measured "
           "along the direction in which the potential decreases fastest.",
           "The potential difference between any two points on the surface of a charged conductor in equilibrium "
           "is zero.",
           "The potential difference between two points depends on the path along which a test charge is carried "
           "between them."]),
    place("(a), (b), (c) and (d) only",
          ["(a), (b) and (c) only", "(b), (c), (d) and (e) only", "(a), (d) and (e) only"], "D"),
    "Relation between field and potential",
    "E = −dV/dl along the direction of steepest decrease, so E points towards lower potential and vanishes where V "
    "is uniform. The surface (and the whole volume) of a conductor in electrostatic equilibrium is an "
    "equipotential. The electrostatic field is conservative, so the work per unit charge between two points — the "
    "potential difference — is independent of the path.",
    ["(a) true", "(b) dV/dl = 0 → E = 0 → true", "(c) |E| = −dV/dl (steepest) → true",
     "(d) conductor surface is equipotential → true", "(e) conservative field → path-independent → false"],
    why="(e) would make the potential undefined; codes leaving out (d) forget that a conductor in equilibrium is "
        "an equipotential.",
    ncert="Class 12 Physics, 'Electrostatic Potential and Capacitance', equipotential surfaces and relation between "
          "field and potential", seconds=80)

U_dip = lambda th_deg: -1.0 * math.cos(math.radians(th_deg))
assert U_dip(180) > U_dip(170) and U_dip(180) > U_dip(190)          # θ = 180° is a maximum of U → unstable
add(T, "Electric field and dipole", "Advanced", "assertion_reason",
    AR_STEM.format(
        a="An electric dipole placed in a uniform electric field with its dipole moment antiparallel to the field "
          "is in stable equilibrium.",
        r="In a uniform electric field, the net force on an electric dipole is zero."),
    ar("D"),
    "Equilibrium of a dipole in a uniform field",
    "The torque p × E is zero both when p is parallel and when it is antiparallel to E, so both are equilibrium "
    "positions. The potential energy U = −pE cos θ is least at θ = 0 (stable) and greatest at θ = 180° (unstable): "
    "a small rotation from the antiparallel position produces a torque that turns the dipole further away. The "
    "forces qE and −qE on the two charges cancel in a uniform field, so R is true.",
    ["θ = 180°: τ = 0 but U = +pE is a maximum → unstable → A false",
     "F_net = qE − qE = 0 → R true"],
    why="A is the trap: zero torque makes the antiparallel position an equilibrium, but not a stable one.",
    ncert="Class 12 Physics, 'Electric Charges and Fields', dipole in a uniform external field", seconds=50)


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
    doc = {"schema_version": "1.0", "batch_id": "BATCH_004", "created_at": TODAY,
           "notes": "BATCH_004 package PHY_004_p1: 130 original Physics questions (Physics and Measurement through "
                    "Electrostatics). Every numerical answer is re-derived in tools/batch_004/PHY_004_p1.py.",
           "stimuli": [], "questions": QUESTIONS}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {OUT}: {n} questions, {dict(Counter(x['difficulty'] for x in QUESTIONS))}")
    print(f"keys {dict(sorted(keys.items()))}")
    print(f"formats {dict(fmts)}")
