"""Writes batches/parts/BATCH_008_PHY_p1.json: package PHY_008_p1 of BATCH_008 (125 Physics questions).

Topics: Physics and Measurement, Kinematics, Laws of Motion, Work Energy and Power, Rotational Motion, Gravitation,
Properties of Solids and Liquids, Thermodynamics, Kinetic Theory of Gases, Oscillations and Waves, Electrostatics.
IDs NEET_PHY_001751 .. NEET_PHY_001875, in the order the questions are listed below.

Every computable answer is re-derived with an assert before the file is written, and so is the plan quota. If any
assert fails, nothing is written. Each question's answer position is chosen by hand and fixed.

    python tools/batch_008/PHY_008_p1.py        (run from docs/neet-bank)
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
OUT = ROOT / "batches" / "parts" / "BATCH_008_PHY_p1.json"
PLAN = ROOT / "batches" / "plans" / "BATCH_008_plan.json"
PACKAGE = "PHY_008_p1"
TODAY = "2026-11-16"
LETTERS = "ABCD"
PHY = "Physics"
RECOMPUTED = ("script:recompute", "ai:author-solve", "ai:self-recheck")
AUTHORED = ("ai:author-solve", "ai:self-recheck")
FIRST_ID = 1751

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


# =====================================================================================================================
# Physics and Measurement (B1 I2 A2)
# =====================================================================================================================
T = "Physics and Measurement"

add(T, "Units and SI system", "Basic", "direct",
    "Which of the following is a unit of length?",
    place("Light year", ["Kilowatt hour", "Electron volt", "Poise"], "B"),
    "Units of length used for very large distances",
    "A light year is the distance light travels in vacuum in one year (about 9.46 × 10¹⁵ m), so it measures "
    "length, not time. The kilowatt hour and the electron volt are units of energy, and the poise is the CGS unit "
    "of the coefficient of viscosity.",
    ["Light year = speed of light × one year → a distance", "kWh and eV → energy; poise → viscosity"],
    why="Kilowatt hour (3.6 × 10⁶ J) and electron volt (1.6 × 10⁻¹⁹ J) are energy units; the poise is a unit of "
        "viscosity. The word 'year' misleads students into treating the light year as a unit of time.",
    ncert="Class 11 Physics, 'Units and Measurement', the international system of units", seconds=25)

L_ = dims(l=1)
SPEED = dims(l=1, t=-1)
FORCE = dims(m=1, l=1, t=-2)
PRESS = dims(m=1, l=-1, t=-2)
DENS = dims(m=1, l=-3)
ANGMOM = dims(m=1, l=2, t=-1)
MOM = dims(m=1, l=1, t=-1)
assert dmul(PRESS, dinv(DENS)) == dims(l=2, t=-2)
assert dmul(FORCE, dinv(L_), dinv(SPEED)) == dims(m=1, l=-1, t=-1)
assert dpow(dmul(PRESS, dinv(DENS)), F(1, 2)) == (0, 1, -1, 0)          # Young's modulus has pressure dimensions
assert dmul(ANGMOM, dinv(MOM)) == L_
add(T, "Dimensional analysis", "Intermediate", "match_list",
    match_stem("Match List-I (combination of physical quantities) with List-II (its dimensional formula).",
               ["Pressure divided by density", "Force divided by the product of a length and a speed",
                "Square root of (Young's modulus divided by density)",
                "Angular momentum divided by linear momentum"],
               ["[L]", "[L² T⁻²]", "[M L⁻¹ T⁻¹]", "[L T⁻¹]"]),
    match_options({"A": "II", "B": "III", "C": "IV", "D": "I"},
                  [{"A": "IV", "B": "III", "C": "II", "D": "I"}, {"A": "II", "B": "I", "C": "IV", "D": "III"},
                   {"A": "III", "B": "II", "C": "IV", "D": "I"}], "D"),
    "Dimensions of derived combinations",
    "Pressure [M L⁻¹ T⁻²] ÷ density [M L⁻³] = [L² T⁻²]. Force [M L T⁻²] ÷ (length × speed) [L² T⁻¹] = "
    "[M L⁻¹ T⁻¹], the dimensions of the coefficient of viscosity. Young's modulus has the dimensions of pressure, "
    "so √(Y/ρ) = √[L² T⁻²] = [L T⁻¹], a speed. Angular momentum [M L² T⁻¹] ÷ linear momentum [M L T⁻¹] = [L].",
    ["A: [M L⁻¹ T⁻²]/[M L⁻³] = [L² T⁻²] → II", "B: [M L T⁻²]/[L² T⁻¹] = [M L⁻¹ T⁻¹] → III",
     "C: √[L² T⁻²] = [L T⁻¹] → IV", "D: [M L² T⁻¹]/[M L T⁻¹] = [L] → I"],
    why="The other codes either forget to take the square root in C (giving [L² T⁻²] instead of a speed) or swap "
        "the viscosity-type combination B with a length.",
    ncert="Class 11 Physics, 'Units and Measurement', dimensions of physical quantities", seconds=75,
    recomputed=True)

pct_V = 1.2
pct_r = pct_V / 3
assert close(pct_r, 0.4)
add(T, "Errors in measurement", "Intermediate", "numerical",
    "The volume of a small sphere is to be found from its measured radius, using V = (4/3)πr³. If the maximum "
    "percentage error in the volume must not exceed 1.2%, the largest permissible percentage error in measuring "
    "the radius is:",
    place("0.4%", ["3.6%", "1.2%", "0.6%"], "C"),
    "Propagation of relative error through a power",
    "For a quantity Z = k rⁿ, the maximum relative error is ΔZ/Z = n Δr/r; the constant 4π/3 has no error. "
    "Here n = 3, so the percentage error in V is three times that in r. Working backwards, the error allowed in r "
    "is one-third of the error allowed in V.",
    ["ΔV/V = 3 Δr/r", "3 × (Δr/r) ≤ 1.2% → Δr/r ≤ 0.4%"],
    shortcut="Allowed error in the measured quantity = allowed error in the result ÷ power.",
    why="3.6% multiplies by the power instead of dividing; 1.2% ignores the power; 0.6% divides by 2 as if the "
        "volume depended on r².",
    ncert="Class 11 Physics, 'Units and Measurement', combination of errors (quantity raised to a power)",
    seconds=50, recomputed=True)

# v = S^x rho^y lam^z ; S = [M T^-2], rho = [M L^-3], lam = [L]
x_, y_, z_ = F(1, 2), F(-1, 2), F(-1, 2)
S_D, RHO_D = dims(m=1, t=-2), DENS
assert dmul(dpow(S_D, x_), dpow(RHO_D, y_), dpow(L_, z_)) == SPEED
add(T, "Dimensional analysis", "Advanced", "numerical",
    "The speed v of short ripples on the surface of a liquid is assumed to depend only on the surface tension S of "
    "the liquid, its density ρ and the wavelength λ of the ripples, as v ∝ Sˣ ρʸ λᶻ. By the method of dimensions, "
    "the values of x, y and z are respectively:",
    place("1/2, −1/2, −1/2", ["1/2, −1/2, 1/2", "1, −1, −1", "−1/2, 1/2, −1/2"], "A"),
    "Deducing a relation by dimensional analysis",
    "S has dimensions [M T⁻²] (force per unit length), ρ is [M L⁻³] and λ is [L]. Equate powers of M, L and T on "
    "both sides of [L T⁻¹] = [M T⁻²]ˣ [M L⁻³]ʸ [L]ᶻ.",
    ["M: x + y = 0", "T: −2x = −1 → x = 1/2, so y = −1/2", "L: −3y + z = 1 → 3/2 + z = 1 → z = −1/2",
     "v ∝ √(S/(ρλ))"],
    why="(1/2, −1/2, 1/2) makes a sign slip in the L equation; (1, −1, −1) gives [L² T⁻²], the square of a speed; "
        "(−1/2, 1/2, −1/2) inverts the T equation.",
    ncert="Class 11 Physics, 'Units and Measurement', deducing relations among physical quantities",
    seconds=90, recomputed=True)

dt, T_period, limit = 0.2, 2.0, 1.0           # s, s, percent
n_min = math.ceil(2 * dt / (limit / 100) / T_period - 1e-9)
assert n_min == 20
assert all(2 * dt / (n * T_period) * 100 > limit for n in (5, 10))
add(T, "Errors in measurement", "Advanced", "numerical",
    "A student finds g from g = 4π²L/T² for a simple pendulum whose period T is about 2 s. She measures T by "
    "timing n complete oscillations with a stopwatch of resolution 0.2 s and dividing the time by n. The length L "
    "is known very accurately. The least number of oscillations she must time so that the timing error "
    "contributes at most 1% to the maximum percentage error in g is:",
    place("20", ["10", "40", "5"], "B"),
    "Reducing the error of a measured period by timing many oscillations",
    "The total time t = nT ≈ 2n s is measured with an absolute error of 0.2 s, so Δt/t = 0.2/(2n). The period "
    "T = t/n has the same relative error. Since g ∝ T⁻², the relative error in g is twice that in T.",
    ["Δg/g = 2 ΔT/T = 2 × 0.2/(2n) = 0.2/n", "0.2/n ≤ 0.01 → n ≥ 20"],
    why="10 forgets the factor 2 from T²; 40 is more than needed (it would keep the error within 0.5%); 5 "
        "oscillations would leave a timing error of 4% in g.",
    ncert="Class 11 Physics, 'Units and Measurement', errors in measurement and combination of errors",
    seconds=100, recomputed=True)

# =====================================================================================================================
# Kinematics (B3 I5 A3)
# =====================================================================================================================
T = "Kinematics"

v1, v2, t1, t2 = 10.0, 20.0, 2.0, 6.0
disp = (v1 + v2) / 2 * (t2 - t1)
assert close(disp, 60)
add(T, "Motion in a straight line", "Basic", "numerical",
    "A body moves along a straight line with uniform acceleration. Its velocity is 10 m/s at t = 2 s and 20 m/s at "
    "t = 6 s, in the same direction. Its displacement between t = 2 s and t = 6 s is:",
    place("60 m", ["80 m", "40 m", "120 m"], "D"),
    "Average velocity under uniform acceleration",
    "For uniform acceleration the average velocity over an interval is the mean of the initial and final "
    "velocities, (10 + 20)/2 = 15 m/s. Displacement = average velocity × time = 15 × 4.",
    ["v_avg = (u + v)/2 = 15 m/s", "s = 15 × (6 − 2) = 60 m"],
    why="80 m uses the final velocity for the whole interval; 40 m uses the initial velocity; 120 m adds the two "
        "velocities without halving.",
    seconds=40, recomputed=True)

ax_, az_ = 6, -8
mag = math.hypot(ax_, az_)
assert mag == 10 and (ax_ / mag, az_ / mag) == (0.6, -0.8)
add(T, "Vectors", "Basic", "numerical",
    "The unit vector in the direction of the vector A = 6î − 8k̂ is:",
    place("0.6î − 0.8k̂", ["0.6î + 0.8k̂", "(6î − 8k̂)/14", "0.8î − 0.6k̂"], "C"),
    "Unit vector along a given vector",
    "A unit vector along A is Â = A/|A|. Here |A| = √(6² + 8²) = 10, so Â = (6î − 8k̂)/10.",
    ["|A| = √(36 + 64) = 10", "Â = 0.6î − 0.8k̂"],
    why="0.6î + 0.8k̂ loses the minus sign of the k̂ component; dividing by 14 adds the components instead of "
        "taking the magnitude; 0.8î − 0.6k̂ swaps the components.",
    ncert="Class 11 Physics, 'Motion in a Plane', unit vectors and resolution of vectors", seconds=35,
    recomputed=True)

add(T, "Graphs of motion", "Basic", "direct",
    "The position–time graph of a particle moving along the x-axis is a straight line parallel to the time axis, "
    "at x = +5 m. Over this interval the particle is:",
    place("At rest at x = 5 m", ["Moving with a constant velocity of 5 m/s",
                                 "Moving with a constant acceleration", "Moving with a constant speed but "
                                 "changing direction"], "A"),
    "Reading a position–time graph",
    "The slope of a position–time graph is the velocity. A line parallel to the time axis has zero slope: the "
    "position does not change with time, so the particle is at rest at x = 5 m.",
    ["Slope of x–t graph = velocity", "Horizontal line → slope 0 → v = 0 at x = 5 m"],
    why="A constant velocity of 5 m/s would need a straight line with slope 5 m/s, not a horizontal line; constant "
        "acceleration gives a parabola; a particle moving along a line must change its x if it moves at all.",
    ncert="Class 11 Physics, 'Motion in a Straight Line', position–time graphs", seconds=25)

ux, uy = 10.0, 20.0
t45 = (uy + ux) / g                  # vy = -ux
assert close(t45, 3.0)
assert close((uy - ux) / g, 1.0) and close(uy / g, 2.0) and close(2 * uy / g, 4.0)
add(T, "Projectile motion", "Intermediate", "numerical",
    "A ball is projected from level ground with an initial velocity whose horizontal component is 10 m/s and "
    "whose vertical component is 20 m/s upward. Taking g = 10 m/s² and neglecting air resistance, after how much "
    "time is its velocity directed at 45° below the horizontal?",
    place("3 s", ["1 s", "2 s", "4 s"], "B"),
    "Direction of velocity of a projectile",
    "The horizontal component stays 10 m/s. The velocity is at 45° below the horizontal when the vertical "
    "component is 10 m/s downward, i.e. v_y = 20 − 10t = −10 m/s.",
    ["v_x = 10 m/s throughout", "45° below horizontal → v_y = −10 m/s", "20 − 10t = −10 → t = 3 s"],
    why="1 s gives 45° above the horizontal (on the way up); 2 s is the highest point, where the velocity is "
        "horizontal; 4 s is the time of flight, when the velocity is at 63° below the horizontal.",
    seconds=60, recomputed=True)

d, vs, vr = 400.0, 5.0, 3.0
t_total = d / (vs - vr) + d / (vs + vr)
assert close(t_total, 250) and close(2 * d / vs, 160) and close(d / (vs - vr), 200)
add(T, "Relative velocity", "Intermediate", "numerical",
    "A swimmer who can swim at 5 m/s relative to still water swims 400 m straight upstream along a river and then "
    "swims back to her starting point. The river flows at a uniform 3 m/s. The total time for the round trip is:",
    place("250 s", ["160 s", "200 s", "100 s"], "D"),
    "Relative velocity along a line: motion in a flowing river",
    "Relative to the ground, her speed is 5 − 3 = 2 m/s upstream and 5 + 3 = 8 m/s downstream. The times for the "
    "two legs are added; the current does not cancel out.",
    ["Upstream: 400/2 = 200 s", "Downstream: 400/8 = 50 s", "Total = 250 s"],
    shortcut="Round-trip time = (2d/v)/(1 − u²/v²) = 160/(1 − 9/25) = 250 s.",
    why="160 s ignores the current; 200 s counts only the upstream leg; 100 s uses 8 m/s for both legs.",
    ncert="Class 11 Physics, 'Motion in a Straight Line', relative velocity", seconds=60, recomputed=True)

r_c, dtheta, dt_c = 0.5, math.pi / 3, 0.5
omega_c = dtheta / dt_c
a_c = omega_c ** 2 * r_c
assert close(a_c, 2 * math.pi ** 2 / 9)
add(T, "Uniform circular motion", "Intermediate", "numerical",
    "A particle moves with constant speed along a circle of radius 0.5 m. Its velocity vector turns through 60° "
    "every 0.5 s. The magnitude of its centripetal acceleration is:",
    place("2π²/9 m/s²", ["4π²/9 m/s²", "8π²/9 m/s²", "2π/3 m/s²"], "C"),
    "Angular speed and centripetal acceleration",
    "In uniform circular motion the velocity turns through the same angle as the radius vector, so the angular "
    "speed is ω = (π/3)/0.5 = 2π/3 rad/s. The centripetal acceleration is ω²r.",
    ["ω = (π/3 rad)/(0.5 s) = 2π/3 rad/s", "a = ω²r = (4π²/9)(0.5) = 2π²/9 m/s² ≈ 2.2 m/s²"],
    why="4π²/9 m/s² is ω² without the radius; 8π²/9 m/s² uses ω²/r; 2π/3 is the angular speed itself (in rad/s, "
        "not an acceleration).",
    ncert="Class 11 Physics, 'Motion in a Plane', uniform circular motion", seconds=60, recomputed=True)

A_, B_ = (3.0, 0.0), (math.cos(math.radians(120)) * 2, math.sin(math.radians(120)) * 2)
diff = math.hypot(A_[0] - B_[0], A_[1] - B_[1])
summ = math.hypot(A_[0] + B_[0], A_[1] + B_[1])
assert diff > summ
add(T, "Vectors", "Intermediate", "statement_pair",
    SP_STEM.format(
        s1="The component of a vector along a direction can be greater in magnitude than the vector itself.",
        s2="If the angle between two non-zero vectors A and B is greater than 90°, then |A − B| is greater than "
           "|A + B|."),
    sp("D"),
    "Components of a vector; magnitudes of sum and difference",
    "The component of A along a unit vector n̂ is A cos θ, and |cos θ| ≤ 1, so a component can never exceed the "
    "magnitude: Statement I is false. |A ± B|² = A² + B² ± 2AB cos θ; for θ > 90°, cos θ < 0, so the difference "
    "has the larger magnitude: Statement II is true.",
    ["Component = A cos θ ≤ A → I false", "|A − B|² − |A + B|² = −4AB cos θ > 0 for θ > 90° → II true"],
    why="Statement I contradicts |cos θ| ≤ 1, so the options calling it true are wrong; Statement II follows "
        "directly from the law of vector addition, so the options calling it false are wrong.",
    ncert="Class 11 Physics, 'Motion in a Plane', addition of vectors and resolution of vectors", seconds=60)

add(T, "Vectors", "Intermediate", "assertion_reason",
    AR_STEM.format(
        a="The scalar (dot) product of two non-zero vectors can be negative.",
        r="The scalar product of two vectors is commutative, that is, A · B = B · A."),
    ar("B"),
    "Scalar product: sign and commutativity",
    "A · B = AB cos θ. For 90° < θ ≤ 180°, cos θ is negative, so the scalar product is negative: A is true. The "
    "scalar product is indeed commutative, so R is true; but commutativity says nothing about the sign of the "
    "product. The sign comes from cos θ, which R does not mention.",
    ["A · B = AB cos θ < 0 when θ > 90° → A true", "A · B = B · A → R true", "R does not explain the sign → B"],
    why="R is a separate property of the dot product, not the reason it can be negative, so A is wrong; both "
        "statements are true, so C and D are wrong.",
    ncert="Class 11 Physics, 'Motion in a Plane' (and 'Work, Energy and Power'), scalar product", seconds=50)

# two successive 4 s intervals: 24 m and 64 m
Ti = 4.0
a_k = (64 - 24) / Ti ** 2
u_k = (24 - 0.5 * a_k * Ti ** 2) / Ti
assert close(a_k, 2.5) and close(u_k, 1.0)
assert close(u_k * 8 + 0.5 * a_k * 64, 24 + 64)
add(T, "Motion in a straight line", "Advanced", "numerical",
    "A body moving along a straight line with uniform acceleration covers 24 m in a certain interval of 4 s and "
    "64 m in the next 4 s. Its velocity at the start of the first interval and its acceleration are respectively:",
    place("1 m/s and 2.5 m/s²", ["4 m/s and 1 m/s²", "6 m/s and 2.5 m/s²", "−4 m/s and 5 m/s²"], "A"),
    "Equations of uniformly accelerated motion over successive equal intervals",
    "Write s = ut + ½at² for the first 4 s and for the first 8 s (24 + 64 = 88 m). Alternatively, for "
    "successive equal intervals T the distances differ by aT².",
    ["4u + 8a = 24", "8u + 32a = 88", "Subtract twice the first: 16a = 40 → a = 2.5 m/s²", "u = (24 − 20)/4 = 1 m/s"],
    shortcut="s₂ − s₁ = aT² → a = 40/16 = 2.5 m/s².",
    why="(4, 1) treats 64 m as the distance covered in the whole 8 s; (6, 2.5) takes the average speed 24/4 as "
        "the initial velocity; (−4, 5) uses s₂ − s₁ = ½aT².",
    seconds=100, recomputed=True)

vx_h, vy_h, h_h = 10.0, 10.0, 15.0
uy_h = math.sqrt(vy_h ** 2 + 2 * g * h_h)
H_h = uy_h ** 2 / (2 * g)
R_h = vx_h * 2 * uy_h / g
assert close(uy_h, 20) and close(H_h, 20) and close(R_h, 40)
add(T, "Projectile motion", "Advanced", "numerical",
    "A ball is projected from level ground. When it is 15 m above the ground on its way up, its velocity is "
    "(10î + 10ĵ) m/s, where î is horizontal and ĵ is vertically upward. Taking g = 10 m/s² and neglecting air "
    "resistance, its maximum height and its horizontal range are respectively:",
    place("20 m and 40 m", ["5 m and 20 m", "20 m and 80 m", "15 m and 30 m"], "D"),
    "Projectile motion: recovering the launch velocity from data at one point",
    "The horizontal component is 10 m/s throughout. For the vertical motion, v_y² = u_y² − 2gh gives the initial "
    "vertical component; then H = u_y²/2g and R = u_x × 2u_y/g.",
    ["u_y² = 10² + 2 × 10 × 15 = 400 → u_y = 20 m/s", "H = 400/20 = 20 m",
     "Time of flight = 2 × 20/10 = 4 s → R = 10 × 4 = 40 m"],
    why="(5 m, 20 m) treats the given velocity as the launch velocity; (20 m, 80 m) doubles the time of flight "
        "again; (15 m, 30 m) takes the given height as the maximum height.",
    seconds=100, recomputed=True)


def r_vec(t):
    return (2 * t, t * t - 4 * t)


def v_vec(t):
    return (2.0, 2 * t - 4)


sp_ = lambda t: math.hypot(*v_vec(t))
truth = [v_vec(2)[1] == 0 and v_vec(2)[0] > 0, True, sp_(0) == min(sp_(t / 10) for t in range(0, 41)),
         close(sp_(0), 2 * math.sqrt(5)), close(math.hypot(*r_vec(4)), 4)]
multi_key(truth, "abd")
add(T, "Vectors", "Advanced", "multi_statement",
    multi("The position vector of a particle moving in the x–y plane is r = (2t) î + (t² − 4t) ĵ, where r is in "
          "metres and t in seconds. Which of the following statements are correct?",
          ["At t = 2 s, the velocity of the particle is along the +x direction.",
           "The acceleration of the particle is constant, of magnitude 2 m/s², along the +y direction.",
           "The speed of the particle is least at t = 0.",
           "The speed of the particle at t = 0 is 2√5 m/s.",
           "At t = 4 s, the particle is 4 m from the origin."]),
    place("(a), (b) and (d) only", ["(a), (b), (c) and (d) only", "(b), (d) and (e) only", "(a) and (e) only"], "B"),
    "Velocity and acceleration from a position vector",
    "Differentiate: v = 2î + (2t − 4)ĵ and a = 2ĵ. Check each statement with these.",
    ["(a) t = 2 s: v = 2î → along +x, true", "(b) a = 2ĵ m/s², constant, true",
     "(c) speed² = 4 + (2t − 4)² is least at t = 2 s, not t = 0 → false",
     "(d) t = 0: v = 2î − 4ĵ, speed √20 = 2√5 m/s, true", "(e) t = 4 s: r = 8î + 0ĵ, distance 8 m → false"],
    why="Options with (c) confuse the start of the motion with the instant of least speed; options with (e) take "
        "the x-coordinate's coefficient instead of evaluating r at t = 4 s.",
    ncert="Class 11 Physics, 'Motion in a Plane', position, velocity and acceleration vectors", seconds=120,
    recomputed=True)

# =====================================================================================================================
# Laws of Motion (B3 I5 A3)
# =====================================================================================================================
T = "Laws of Motion"

m_car, v_car, t_stop = 1500.0, 20.0, 5.0
F_brake = m_car * v_car / t_stop
assert close(F_brake, 6000)
add(T, "Newton's laws and impulse", "Basic", "numerical",
    "A car of mass 1500 kg moving at 20 m/s along a straight level road is brought to rest in 5 s by its brakes. "
    "The magnitude of the average force exerted on the car to stop it is:",
    place("6000 N", ["30 000 N", "300 N", "1500 N"], "B"),
    "Force as the rate of change of momentum",
    "The car's momentum changes from 1500 × 20 = 30 000 kg m/s to zero in 5 s. By Newton's second law the "
    "average force equals the change in momentum divided by the time taken.",
    ["Δp = 30 000 kg m/s", "F = Δp/Δt = 30 000/5 = 6000 N"],
    why="30 000 N is the momentum itself (units kg m/s, not a force); 300 N divides the mass by the time and "
        "leaves out the speed; 1500 N equates the force with the mass.",
    seconds=35, recomputed=True)

add(T, "Newton's laws and impulse", "Basic", "direct",
    "According to Newton's first law, every body resists a change in its state of rest or of uniform motion. The "
    "quantitative measure of this inertia of a body is its:",
    place("Mass", ["Velocity", "Acceleration", "Linear momentum"], "D"),
    "Inertia and mass",
    "Inertia is the resistance of a body to a change in its velocity. For the same force, a body of larger mass "
    "gets a smaller acceleration (a = F/m), so mass measures inertia. Velocity, acceleration and momentum describe "
    "the state of motion, not the resistance to changing it.",
    ["Same F → a ∝ 1/m", "Larger mass → harder to change velocity → mass measures inertia"],
    why="A body has the same inertia whether it is at rest (zero velocity and momentum) or moving, and whatever "
        "its acceleration, so these cannot measure inertia.",
    ncert="Class 11 Physics, 'Laws of Motion', Newton's first law of motion", seconds=25)

M_gun, m_b, v_b = 4.0, 0.020, 400.0
V_rec = m_b * v_b / M_gun
assert close(V_rec, 2.0)
add(T, "Conservation of linear momentum", "Basic", "numerical",
    "A gun of mass 4 kg, free to move, fires a bullet of mass 20 g horizontally with a speed of 400 m/s. The "
    "recoil speed of the gun is:",
    place("2 m/s", ["0.5 m/s", "20 m/s", "8 m/s"], "C"),
    "Conservation of linear momentum in firing",
    "Before firing the total momentum of the gun–bullet system is zero. With no external horizontal force it "
    "stays zero, so the gun's momentum is equal and opposite to the bullet's: M V = m v.",
    ["0 = 0.020 × 400 − 4 V", "V = 8/4 = 2 m/s (opposite to the bullet)"],
    why="0.5 m/s divides 4 by 8 the wrong way round; 20 m/s and 8 m/s come from not converting 20 g to 0.020 kg "
        "consistently (20 m/s uses 0.2 kg, 8 m/s is the bullet's momentum taken as a speed).",
    ncert="Class 11 Physics, 'Laws of Motion', conservation of momentum", seconds=35, recomputed=True)

m_p, mu_p, s37, c37 = 11.0, 0.5, 0.6, 0.8
F_pull = mu_p * m_p * g / (c37 + mu_p * s37)
assert close(F_pull, 50)
assert close(mu_p * m_p * g, 55) and close(mu_p * m_p * g / (c37 - mu_p * s37), 110)
add(T, "Friction", "Intermediate", "numerical",
    "A box of mass 11 kg rests on a rough horizontal floor; the coefficient of static friction is 0.5. A rope "
    "pulls it with a force directed at 37° above the horizontal (sin 37° = 0.6, cos 37° = 0.8). Taking "
    "g = 10 m/s², the least pull that just starts the box sliding is:",
    place("50 N", ["55 N", "110 N", "68.75 N"], "A"),
    "Limiting friction with an inclined pull",
    "The upward component of the pull reduces the normal reaction: N = mg − F sin 37°. The box just starts to "
    "slide when the horizontal component equals the limiting friction μN.",
    ["N = 110 − 0.6F", "0.8F = 0.5(110 − 0.6F) → 0.8F + 0.3F = 55", "F = 55/1.1 = 50 N"],
    why="55 N is the limiting friction for a horizontal pull; 110 N treats the pull as pressing the box down "
        "(N = mg + F sin θ); 68.75 N divides 55 N by cos 37° but keeps N = mg.",
    ncert="Class 11 Physics, 'Laws of Motion', friction", seconds=80, recomputed=True)

L_cp, th_cp = 1.0, math.radians(60)
r_cp = L_cp * math.sin(th_cp)
v_cp = math.sqrt(g * r_cp * math.tan(th_cp))
assert close(v_cp, math.sqrt(15))
add(T, "Newton's laws and impulse", "Intermediate", "numerical",
    "A small bob tied to a light string 1 m long moves in a horizontal circle with constant speed, the string "
    "making a constant angle of 60° with the vertical (a conical pendulum). Taking g = 10 m/s², the speed of the "
    "bob is:",
    place("√15 m/s", ["√(5√3) m/s", "√10 m/s", "√(10√3) m/s"], "B"),
    "Newton's second law for a body in uniform circular motion",
    "The vertical component of the tension balances the weight, T cos θ = mg, and the horizontal component "
    "provides the centripetal force, T sin θ = mv²/r, where the radius of the circle is r = L sin θ.",
    ["Dividing: tan θ = v²/(rg)", "r = 1 × sin 60° = √3/2 m", "v² = g r tan θ = 10 × (√3/2) × √3 = 15 → v = √15 m/s"],
    why="√(5√3) uses r = L cos θ; √10 sets v² = gL; √(10√3) takes the radius as the full string length.",
    seconds=80, recomputed=True)

add(T, "Conservation of linear momentum", "Intermediate", "statement_pair",
    SP_STEM.format(
        s1="When a body at rest explodes into exactly two fragments, the fragments move off in opposite directions "
           "along the same straight line.",
        s2="In an explosion, the total kinetic energy of the fragments just after the explosion equals the kinetic "
           "energy of the body just before it."),
    sp("C"),
    "Momentum and kinetic energy in an explosion",
    "The forces of the explosion are internal, so total momentum stays zero: p₁ + p₂ = 0, i.e. the two momenta "
    "are equal and opposite, along one line. Statement I is true. Kinetic energy is not conserved: it increases "
    "from zero, at the expense of chemical (internal) energy. Statement II is false.",
    ["p₁ = −p₂ → opposite directions, same line → I true", "KE rises from 0 → II false"],
    why="Momentum, not kinetic energy, is conserved in an explosion, so the options calling II true are wrong; "
        "Statement I follows from momentum conservation, so the options calling it false are wrong.",
    ncert="Class 11 Physics, 'Laws of Motion', conservation of momentum", seconds=50)

vals = {"A": 2 * 3, "B": 4 * 2, "C": 10 / 5, "D": 0.5 * 4 - 0.5 * (-4)}
assert vals == {"A": 6, "B": 8, "C": 2, "D": 4}
add(T, "Newton's laws and impulse", "Intermediate", "match_list",
    match_stem("All quantities are in SI units. Match List-I with List-II (magnitude of the quantity).",
               ["Linear momentum of a 2 kg body moving at 3 m/s",
                "Impulse of a constant force of 4 N acting for 2 s",
                "Average force needed to change the momentum of a body by 10 kg m/s in 5 s",
                "Change in momentum of a 0.5 kg ball that hits a wall normally at 4 m/s and rebounds normally at "
                "4 m/s"],
               ["2", "4", "6", "8"]),
    match_options({"A": "III", "B": "IV", "C": "I", "D": "II"},
                  [{"A": "III", "B": "IV", "C": "II", "D": "I"}, {"A": "IV", "B": "III", "C": "I", "D": "II"},
                   {"A": "III", "B": "I", "C": "IV", "D": "II"}], "D"),
    "Momentum, impulse and force",
    "p = mv; impulse = FΔt; average force = Δp/Δt; for a rebound the velocity reverses, so Δp = m(v − (−u)).",
    ["A: 2 × 3 = 6 → III", "B: 4 × 2 = 8 → IV", "C: 10/5 = 2 → I", "D: 0.5 × (4 + 4) = 4 → II"],
    why="Matching D to 2 (or C to 4) forgets that the ball's velocity reverses, so its momentum changes by 2mv, "
        "not mv; the other codes swap momentum with impulse.",
    seconds=60, recomputed=True)

mu_c = 0.5
a_min = g / mu_c
assert close(a_min, 20)
add(T, "Friction", "Intermediate", "numerical",
    "A block of mass 1 kg is placed in contact with the front vertical face of a cart (the face that looks in "
    "the direction of motion). The cart moves forward on a level road with a horizontal acceleration, so that the "
    "face pushes the block forward and nothing else holds the block. The coefficient of static friction between "
    "the block and the face is 0.5. Taking g = 10 m/s², the least acceleration of the cart for which the block "
    "does not slide down is:",
    place("20 m/s²", ["5 m/s²", "10 m/s²", "40 m/s²"], "A"),
    "Static friction and Newton's second law",
    "The face pushes the block forward with the normal force N, which alone gives the block its acceleration a: "
    "N = ma. Friction along the face, at most μN, must hold up the weight: μma ≥ mg.",
    ["N = ma", "μN ≥ mg → a ≥ g/μ", "a_min = 10/0.5 = 20 m/s²"],
    why="5 m/s² is μg, as if friction had to provide the acceleration; 10 m/s² ignores μ; 40 m/s² uses 2g/μ.",
    seconds=70, recomputed=True)

m_blk, m_rope, a_up = 3.0, 2.0, 2.0
T_mid = (m_blk + m_rope / 2) * (g + a_up)
assert close(T_mid, 48)
assert close((m_blk + m_rope) * (g + a_up), 60) and close(m_blk * (g + a_up), 36) and close((m_blk + 1) * g, 40)
add(T, "Newton's laws and impulse", "Advanced", "numerical",
    "A uniform rope of mass 2 kg hangs vertically with a block of mass 3 kg tied to its lower end. The upper end "
    "of the rope is pulled upward so that the rope and block move up with an acceleration of 2 m/s². Taking "
    "g = 10 m/s², the tension at the midpoint of the rope is:",
    place("48 N", ["60 N", "36 N", "40 N"], "B"),
    "Tension in a heavy rope: Newton's second law for a part of a system",
    "Consider everything below the midpoint: the block (3 kg) and the lower half of the rope (1 kg). The tension "
    "at the midpoint is the only upward force on this 4 kg part: T − 4g = 4a.",
    ["Mass below midpoint = 3 + 1 = 4 kg", "T = 4(g + a) = 4 × 12 = 48 N"],
    why="60 N is the pull at the top (whole 5 kg); 36 N is the tension at the bottom of the rope; 40 N ignores "
        "the acceleration.",
    seconds=80, recomputed=True)

add(T, "Equilibrium of concurrent forces", "Advanced", "assertion_reason",
    AR_STEM.format(
        a="A string fixed at both ends at the same level, with a weight hung from its midpoint, can never be made "
          "exactly horizontal, however large the tension in it.",
        r="At the midpoint, the vertical components of the tensions in the two halves must together balance the "
          "weight, and these components are zero if the string is horizontal."),
    ar("A"),
    "Equilibrium of three concurrent forces",
    "If each half makes an angle θ with the horizontal, equilibrium of the midpoint gives 2T sin θ = W, so "
    "T = W/(2 sin θ). For θ → 0, T → ∞; no finite tension makes θ exactly zero. R states exactly this vertical "
    "balance, so it explains A.",
    ["2T sin θ = W", "θ = 0 → 0 = W, impossible", "R gives the reason → A"],
    why="R is the condition that makes A true, so B is wrong; both statements are true, so C and D are wrong.",
    ncert="Class 11 Physics, 'Laws of Motion', equilibrium of a particle", seconds=60)

# F = 6t on 2 kg from rest
p2 = 3 * 2 ** 2
v2_ = p2 / 2
KE2 = 0.5 * 2 * v2_ ** 2
truth = [p2 == 12, v2_ == 6, p2 == 12, False, KE2 == 72]
assert KE2 == 36
multi_key(truth, "abc")
add(T, "Newton's laws and impulse", "Advanced", "multi_statement",
    multi("A body of mass 2 kg, initially at rest on a smooth horizontal surface, is acted on by a horizontal force "
          "F = 6t, where F is in newtons and t in seconds. Which of the following statements are correct?",
          ["Its linear momentum at t = 2 s is 12 kg m/s.", "Its velocity at t = 2 s is 6 m/s.",
           "The impulse of the force during the first 2 s is 12 N s.", "Its acceleration is constant.",
           "Its kinetic energy at t = 2 s is 72 J."]),
    place("(a), (b) and (c) only", ["(a), (b), (c) and (e) only", "(b), (d) and (e) only", "(a) and (d) only"], "C"),
    "Impulse of a variable force",
    "Impulse = ∫F dt = ∫₀² 6t dt = 3t² |₀² = 12 N s, which equals the change in momentum from zero.",
    ["(a) p = 12 kg m/s, true", "(b) v = 12/2 = 6 m/s, true", "(c) impulse = 12 N s, true",
     "(d) a = F/m = 3t, which grows with time → false", "(e) KE = ½ × 2 × 6² = 36 J, not 72 J → false"],
    why="Options with (e) use mv² instead of ½mv²; options with (d) treat the force as constant.",
    seconds=100, recomputed=True)

# =====================================================================================================================
# Work, Energy and Power (B3 I4 A3)
# =====================================================================================================================
T = "Work, Energy and Power"

m_w, L_w = 2.0, 5.0
W_g = m_w * g * L_w * math.sin(math.radians(30))
assert close(W_g, 50)
add(T, "Work by constant and variable force", "Basic", "numerical",
    "A block of mass 2 kg slides 5 m down a plane inclined at 30° to the horizontal. Taking g = 10 m/s², the work "
    "done on the block by gravity is:",
    place("50 J", ["100 J", "50√3 J", "25 J"], "D"),
    "Work done by a constant force",
    "W = F d cos φ, where φ is the angle between the weight (vertically down) and the displacement (along the "
    "incline). That angle is 60°, so W = mg × 5 × cos 60° = mg × (vertical drop).",
    ["Vertical drop = 5 sin 30° = 2.5 m", "W = 2 × 10 × 2.5 = 50 J"],
    why="100 J multiplies mg by the full length of the incline; 50√3 J uses cos 30° (the angle of the incline) "
        "instead of the angle between force and displacement; 25 J halves the result again.",
    ncert="Class 11 Physics, 'Work, Energy and Power', work", seconds=40, recomputed=True)

F_res, v_boat = 1500.0, 10.0
P_boat = F_res * v_boat
assert close(P_boat, 15000)
add(T, "Power", "Basic", "numerical",
    "A motorboat moves through still water at a constant speed of 10 m/s. The water exerts a resistive force of "
    "1500 N on it. The power delivered by the engine to move the boat is:",
    place("15 kW", ["150 W", "1.5 kW", "150 kW"], "C"),
    "Power as force × velocity",
    "At constant speed the forward force from the engine equals the resistive force, 1500 N. The power is the "
    "rate of doing work, P = F v.",
    ["Driving force = 1500 N (constant speed)", "P = 1500 × 10 = 15 000 W = 15 kW"],
    why="150 W divides the force by the speed; 1.5 kW and 150 kW are slips by a factor of 10 in the product.",
    ncert="Class 11 Physics, 'Work, Energy and Power', power", seconds=30, recomputed=True)

ke = {"A": 0.5 * 2 * 3 ** 2, "B": 0.5 * 0.5 * 4 ** 2, "C": 8 ** 2 / (2 * 4), "D": 6 ** 2 / (2 * 3)}
assert ke == {"A": 9, "B": 4, "C": 8, "D": 6}
add(T, "Work-energy theorem", "Basic", "match_list",
    match_stem("Match List-I (moving body) with List-II (its kinetic energy).",
               ["A body of mass 2 kg moving at 3 m/s", "A body of mass 0.5 kg moving at 4 m/s",
                "A body of mass 4 kg having linear momentum 8 kg m/s",
                "A body of mass 3 kg having linear momentum 6 kg m/s"],
               ["4 J", "6 J", "8 J", "9 J"]),
    match_options({"A": "IV", "B": "I", "C": "III", "D": "II"},
                  [{"A": "IV", "B": "III", "C": "I", "D": "II"}, {"A": "II", "B": "I", "C": "III", "D": "IV"},
                   {"A": "IV", "B": "I", "C": "II", "D": "III"}], "A"),
    "Kinetic energy in terms of speed and momentum",
    "K = ½mv² = p²/(2m).",
    ["A: ½ × 2 × 9 = 9 J → IV", "B: ½ × 0.5 × 16 = 4 J → I", "C: 64/8 = 8 J → III", "D: 36/6 = 6 J → II"],
    why="The other codes use p²/m (doubling C and D) or swap the momentum-based cases.",
    ncert="Class 11 Physics, 'Work, Energy and Power', kinetic energy", seconds=60, recomputed=True)

m1, m2, u1, u2 = 1.0, 2.0, 6.0, 3.0
v1e = ((m1 - m2) * u1 + 2 * m2 * u2) / (m1 + m2)
v2e = ((m2 - m1) * u2 + 2 * m1 * u1) / (m1 + m2)
assert close(v1e, 2) and close(v2e, 5)
assert close(m1 * v1e + m2 * v2e, m1 * u1 + m2 * u2)
assert close(m1 * v1e ** 2 + m2 * v2e ** 2, m1 * u1 ** 2 + m2 * u2 ** 2)
add(T, "Collisions", "Intermediate", "numerical",
    "A ball of mass 1 kg moving at 6 m/s overtakes and collides head-on, elastically, with a ball of mass 2 kg "
    "moving at 3 m/s in the same direction along the same line. Their velocities just after the collision are "
    "respectively:",
    place("2 m/s and 5 m/s, both forward", ["3 m/s and 6 m/s, both forward", "4 m/s and 4 m/s, both forward",
                                            "0 and 6 m/s forward"], "B"),
    "One-dimensional elastic collision with both bodies moving",
    "Conserve momentum, and use the fact that in a 1-D elastic collision the relative velocity of separation "
    "equals the relative velocity of approach.",
    ["Momentum: 6 + 6 = 12 = v₁ + 2v₂", "Relative velocity: v₂ − v₁ = 6 − 3 = 3",
     "→ 3v₂ = 15 → v₂ = 5 m/s, v₁ = 2 m/s", "Check KE: 18 + 9 = 27 J = 2 + 25 J"],
    why="(3, 6) simply exchanges the velocities, valid only for equal masses; (4, 4) is the perfectly inelastic "
        "result; (0, 6) conserves momentum but not kinetic energy (36 J ≠ 27 J).",
    ncert="Class 11 Physics, 'Work, Energy and Power', collisions in one dimension", seconds=90, recomputed=True)

m_s, L_s, T_max = 0.2, 0.5, 22.0
v_max = math.sqrt((T_max - m_s * g) * L_s / m_s)
assert close(v_max, 5 * math.sqrt(2))
add(T, "Motion in a vertical circle", "Intermediate", "numerical",
    "A stone of mass 0.2 kg is whirled in a vertical circle at the end of a light string 0.5 m long. The string "
    "breaks if its tension exceeds 22 N. Taking g = 10 m/s², the greatest speed the stone can have at the lowest "
    "point of the circle without the string breaking is:",
    place("5√2 m/s", ["√55 m/s", "10 m/s", "√60 m/s"], "C"),
    "Tension at the lowest point of a vertical circle",
    "At the lowest point the tension acts upward and the weight downward; their difference supplies the "
    "centripetal force: T − mg = mv²/L. The tension is greatest at the lowest point, so this is where the string "
    "would break first.",
    ["22 − 2 = 0.2 v²/0.5", "v² = 20 × 2.5 = 50 → v = 5√2 m/s"],
    why="√55 m/s ignores the weight; √60 m/s adds the weight instead of subtracting it; 10 m/s doubles the "
        "string length.",
    seconds=60, recomputed=True)

add(T, "Work-energy theorem", "Intermediate", "assertion_reason",
    AR_STEM.format(
        a="When a box is lifted vertically through a height h at a constant speed, the net work done on the box "
          "is zero, although the lifting force does work mgh on it.",
        r="By the work–energy theorem, the net work done on a body equals the change in its kinetic energy, which "
          "is zero when the speed does not change; the work +mgh of the lifting force is cancelled by the work "
          "−mgh done by gravity."),
    ar("A"),
    "Work–energy theorem: net work and the work of individual forces",
    "At constant speed the lifting force equals mg, so it does work +mgh; gravity, acting opposite to the "
    "displacement, does −mgh. The total is zero, which agrees with the work–energy theorem since ΔK = 0. R gives "
    "exactly this reasoning, so it explains A.",
    ["Lifting force: W = +mgh", "Gravity: W = −mgh", "W_net = 0 = ΔK → R explains A → A"],
    why="R is the very reason the net work is zero while one force does positive work, so B is wrong; both "
        "statements are true, so C and D are wrong.",
    ncert="Class 11 Physics, 'Work, Energy and Power', the work–energy theorem", seconds=50)

kA = 1.0                     # spring A constant k, spring B 2k
F_same, x_same = 1.0, 1.0
UA_F, UB_F = F_same ** 2 / (2 * kA), F_same ** 2 / (2 * 2 * kA)
UA_x, UB_x = 0.5 * kA * x_same ** 2, 0.5 * 2 * kA * x_same ** 2
truth = [close(UA_F, 2 * UB_F), close(UB_x, 2 * UA_x), close(F_same / kA, 2 * F_same / (2 * kA)),
         UA_x > UB_x, close(UA_F, UB_F)]
multi_key(truth, "abc")
add(T, "Spring potential energy", "Intermediate", "multi_statement",
    multi("Two ideal springs A and B have spring constants k and 2k respectively. Which of the following "
          "statements are correct?",
          ["When both are stretched by the same force, the energy stored in A is twice that stored in B.",
           "When both are stretched by the same extension, the energy stored in B is twice that stored in A.",
           "When both are stretched by the same force, the extension of A is twice that of B.",
           "When both are stretched by the same extension, more work is done on A than on B.",
           "When both are stretched by the same force, they store equal energies."]),
    place("(a), (b) and (c) only", ["(a), (c) and (d) only", "(b), (c) and (e) only", "(b) and (d) only"], "D"),
    "Elastic potential energy of a spring: ½kx² = F²/2k",
    "For the same extension use U = ½kx², which is proportional to k. For the same force the extension is F/k, "
    "so U = F²/(2k), which is inversely proportional to k.",
    ["(a) U ∝ 1/k at fixed F → U_A = 2U_B, true", "(b) U ∝ k at fixed x → U_B = 2U_A, true",
     "(c) x = F/k → x_A = 2x_B, true", "(d) work done = stored energy, larger for B → false",
     "(e) contradicts (a) → false"],
    why="Options with (d) or (e) use the wrong one of the two forms ½kx² and F²/2k for the condition stated.",
    ncert="Class 11 Physics, 'Work, Energy and Power', the potential energy of a spring", seconds=90,
    recomputed=True)

m_d, h_d, k_d = 1.0, 0.4, 1000.0
# m g (h + x) = 1/2 k x^2
a_q, b_q, c_q = 0.5 * k_d, -m_d * g, -m_d * g * h_d
x_d = (-b_q + math.sqrt(b_q ** 2 - 4 * a_q * c_q)) / (2 * a_q)
assert close(x_d, 0.1)
assert close(math.sqrt(2 * m_d * g * h_d / k_d), 0.0894, rel=1e-2)
add(T, "Spring potential energy", "Advanced", "numerical",
    "A block of mass 1 kg is dropped from rest from a height of 0.4 m above the top of a light vertical spring of "
    "spring constant 1000 N/m, whose lower end is fixed to the floor. Taking g = 10 m/s² and neglecting air "
    "resistance, the maximum compression of the spring is:",
    place("10 cm", ["8.9 cm", "1 cm", "20 cm"], "A"),
    "Conservation of mechanical energy with a spring",
    "At maximum compression x the block is momentarily at rest. It has fallen a total height (0.4 + x), so the "
    "loss of gravitational potential energy equals the elastic energy stored: mg(h + x) = ½kx².",
    ["10(0.4 + x) = 500x²", "500x² − 10x − 4 = 0", "x = [10 + √(100 + 8000)]/1000 = (10 + 90)/1000 = 0.1 m"],
    why="8.9 cm ignores the extra drop x during compression (mgh = ½kx²); 1 cm is the static compression mg/k; "
        "20 cm doubles the correct value.",
    ncert="Class 11 Physics, 'Work, Energy and Power', conservation of mechanical energy; potential energy of a "
          "spring", seconds=110, recomputed=True)

mb, ub, vb_out, Mblk = 0.020, 500.0, 100.0, 2.0
V_blk = mb * (ub - vb_out) / Mblk
h_blk = V_blk ** 2 / (2 * g)
assert close(V_blk, 4) and close(h_blk, 0.8)
add(T, "Collisions", "Advanced", "numerical",
    "A bullet of mass 20 g moving horizontally at 500 m/s passes through a wooden block of mass 2 kg hanging at "
    "rest from a long light string, and emerges at 100 m/s. Taking g = 10 m/s² and neglecting the loss of mass "
    "of the block, the maximum height through which the block rises is:",
    place("0.8 m", ["1.6 m", "0.05 m", "1.25 m"], "D"),
    "Momentum conservation in an inelastic collision followed by energy conservation",
    "During the very short passage the string force is vertical, so horizontal momentum is conserved; kinetic "
    "energy is not (heat is produced in the wood). After that, the block swings up with its mechanical energy "
    "conserved.",
    ["0.02 × 500 = 0.02 × 100 + 2V → V = 8/2 = 4 m/s", "h = V²/(2g) = 16/20 = 0.8 m"],
    why="1.6 m uses h = V²/g; 0.05 m uses the bullet's exit momentum alone; 1.25 m treats the bullet as embedded "
        "in the block (V ≈ 4.95 m/s).",
    seconds=100, recomputed=True)

m_bob, th_b = 0.2, math.radians(60)
v2_b_over_L = 2 * g * math.cos(th_b)          # v^2/L for release from horizontal
T_b = m_bob * g * math.cos(th_b) + m_bob * v2_b_over_L
assert close(T_b, 3.0)
add(T, "Motion in a vertical circle", "Advanced", "numerical",
    "A small bob of mass 0.2 kg hangs from a light inextensible string. The bob is pulled aside until the string "
    "is horizontal and taut, and is released from rest. Taking g = 10 m/s², the tension in the string at the "
    "instant the string makes an angle of 60° with the vertical is:",
    place("3 N", ["6 N", "1 N", "2 N"], "B"),
    "Energy conservation and radial equation in a vertical circle",
    "When the string makes angle θ with the vertical, the bob has fallen L cos θ from the release level, so "
    "v² = 2gL cos θ. Along the string, T − mg cos θ = mv²/L.",
    ["v²/L = 2g cos 60° = 10 m/s²", "T = mg cos 60° + m v²/L = 0.2(5) + 0.2(10) = 3 N"],
    shortcut="T = 3mg cos θ for release from the horizontal position.",
    why="6 N is the tension at the lowest point (θ = 0); 1 N keeps only the component of weight; 2 N is just mg.",
    seconds=100, recomputed=True)

# =====================================================================================================================
# Rotational Motion (B3 I5 A3)
# =====================================================================================================================
T = "Rotational Motion"

w_f = 120 * 2 * math.pi / 60
alpha_r = w_f / 4
assert close(alpha_r, math.pi)
add(T, "Rigid-body rotation", "Basic", "numerical",
    "A wheel starts from rest and, rotating about a fixed axis with uniform angular acceleration, reaches 120 "
    "revolutions per minute in 4 s. Its angular acceleration is:",
    place("π rad/s²", ["30 rad/s²", "2π rad/s²", "π/2 rad/s²"], "C"),
    "Kinematics of rotation about a fixed axis",
    "Convert the final rate to rad/s: 120 rev/min = 2 rev/s = 4π rad/s. Then α = (ω − ω₀)/t.",
    ["ω = 120 × 2π/60 = 4π rad/s", "α = 4π/4 = π rad/s²"],
    why="30 divides 120 by 4 without converting rev/min; 2π rad/s² doubles the converted angular speed (8π rad/s); "
        "π/2 rad/s² halves it (2π rad/s).",
    ncert="Class 11 Physics, 'System of Particles and Rotational Motion', kinematics of rotational motion about a "
          "fixed axis", seconds=40, recomputed=True)

M_r, R_r = 0.5, 0.2
I_tan = M_r * R_r ** 2 + M_r * R_r ** 2
assert close(I_tan, 0.04)
add(T, "Moment of inertia and axis theorems", "Basic", "numerical",
    "A thin circular ring has mass 0.5 kg and radius 20 cm. Its moment of inertia about an axis that is "
    "perpendicular to its plane and passes through a point on the ring is:",
    place("0.04 kg m²", ["0.02 kg m²", "0.03 kg m²", "0.01 kg m²"], "B"),
    "Theorem of parallel axes",
    "About the central axis perpendicular to its plane, I = MR². The required axis is parallel to it at a "
    "distance R, so I = MR² + MR² = 2MR².",
    ["I_c = 0.5 × 0.04 = 0.02 kg m²", "I = I_c + MR² = 0.04 kg m²"],
    why="0.02 kg m² is the central value; 0.03 kg m² is the value about a tangent lying in the plane of the ring "
        "(3MR²/2); 0.01 kg m² is the value about a diameter.",
    ncert="Class 11 Physics, 'System of Particles and Rotational Motion', theorem of parallel axes", seconds=40,
    recomputed=True)

add(T, "Moment of inertia and axis theorems", "Basic", "direct",
    "The radius of gyration of a thin uniform rod of length L, about an axis perpendicular to the rod through its "
    "centre, is:",
    place("L/(2√3)", ["L/√3", "L/2", "L/√2"], "D"),
    "Radius of gyration",
    "I = Mk², and for this axis I = ML²/12. Hence k² = L²/12 and k = L/√12 = L/(2√3).",
    ["ML²/12 = Mk²", "k = L/(2√3) ≈ 0.29L"],
    why="L/√3 is the radius of gyration about a perpendicular axis through one end (I = ML²/3); L/2 and L/√2 do "
        "not follow from either value of I.",
    ncert="Class 11 Physics, 'System of Particles and Rotational Motion', moment of inertia and radius of gyration",
    seconds=35)

I_w, tau_w, th_w = 2.0, 4.0, 25.0
W_w = tau_w * th_w
w_w = math.sqrt(2 * W_w / I_w)
assert close(W_w, 100) and close(w_w, 10)
add(T, "Torque and angular momentum", "Intermediate", "numerical",
    "A wheel of moment of inertia 2 kg m² about its fixed axle starts from rest. A constant torque of 4 N m acts "
    "on it about the axle while it turns through 25 rad. Neglecting friction, its final angular speed is:",
    place("10 rad/s", ["5√2 rad/s", "50 rad/s", "100 rad/s"], "A"),
    "Work done by a torque and rotational kinetic energy",
    "The work done by a constant torque is W = τθ. By the work–energy theorem for rotation it equals the gain in "
    "rotational kinetic energy ½Iω².",
    ["W = 4 × 25 = 100 J", "½ × 2 × ω² = 100 → ω = 10 rad/s"],
    why="5√2 rad/s halves the work; 50 rad/s sets ω = τθ/I; 100 rad/s equates ω with the work done.",
    ncert="Class 11 Physics, 'System of Particles and Rotational Motion', work done by a torque", seconds=60,
    recomputed=True)

add(T, "Torque and angular momentum", "Intermediate", "statement_pair",
    SP_STEM.format(
        s1="For every rigid body rotating about a fixed axis, the total angular momentum vector points along the "
           "axis of rotation.",
        s2="For a rigid body rotating about a fixed axis, the component of its angular momentum along that axis "
           "is Iω, where I is its moment of inertia about the axis and ω its angular velocity."),
    sp("D"),
    "Angular momentum of a rigid body rotating about a fixed axis",
    "In general the angular momentum of a body rotating about a fixed axis has a component along the axis and "
    "possibly a component perpendicular to it. Only the component along the axis is Iω. For bodies symmetric "
    "about the axis the perpendicular part vanishes, but not for every body. So Statement I is false and "
    "Statement II is true.",
    ["L = L_axis + L_perp; L_perp = 0 only for bodies symmetric about the axis → I false",
     "L_axis = Iω → II true"],
    why="Statement I overgeneralises the symmetric case, so options calling it true are wrong; Statement II is "
        "the standard result, so options calling it false are wrong.",
    ncert="Class 11 Physics, 'System of Particles and Rotational Motion', angular momentum in case of rotation "
          "about a fixed axis", seconds=60)

tq = {"A": 10 * 0.5, "B": 10 * 0.5 * math.sin(math.radians(30)), "C": 20 * 0.4 * math.sin(0), "D": 4 * 2}
assert close(tq["A"], 5) and close(tq["B"], 2.5) and tq["C"] == 0 and tq["D"] == 8
add(T, "Torque and angular momentum", "Intermediate", "match_list",
    match_stem("A force acts on a rigid body that can turn about a fixed axis, in a plane perpendicular to the "
               "axis. Match List-I (the force and where it acts) with List-II (magnitude of its torque about the "
               "axis).",
               ["10 N, applied 0.5 m from the axis, perpendicular to the line joining the axis to the point of "
                "application", "10 N, applied 0.5 m from the axis, at 30° to the line joining the axis to the point "
                "of application", "20 N, applied 0.4 m from the axis, along the line joining the axis to the point "
                "of application", "4 N, applied 2 m from the axis, perpendicular to the line joining the axis to the "
                "point of application"],
               ["0", "2.5 N m", "5 N m", "8 N m"]),
    match_options({"A": "III", "B": "II", "C": "I", "D": "IV"},
                  [{"A": "III", "B": "I", "C": "II", "D": "IV"}, {"A": "IV", "B": "II", "C": "I", "D": "III"},
                   {"A": "II", "B": "III", "C": "I", "D": "IV"}], "B"),
    "Moment of a force: τ = rF sin θ",
    "The magnitude of torque is rF sin θ, where θ is the angle between the position vector of the point of "
    "application (from the axis) and the force.",
    ["A: 0.5 × 10 × 1 = 5 N m → III", "B: 0.5 × 10 × sin 30° = 2.5 N m → II", "C: θ = 0 → 0 → I",
     "D: 2 × 4 = 8 N m → IV"],
    why="Matching B to 5 N m or C to 2.5 N m uses cos θ instead of sin θ; a force whose line of action passes "
        "through the axis has no torque.",
    ncert="Class 11 Physics, 'System of Particles and Rotational Motion', moment of force (torque)", seconds=70,
    recomputed=True)

R_wh, al_wh, t_wh = 0.5, 2.0, 2.0
a_t = al_wh * R_wh
a_cen = (al_wh * t_wh) ** 2 * R_wh
a_net = math.hypot(a_t, a_cen)
assert close(a_t, 1) and close(a_cen, 8) and close(a_net, math.sqrt(65))
add(T, "Rigid-body rotation", "Intermediate", "numerical",
    "A wheel of radius 0.5 m starts from rest and rotates about its fixed axle with a uniform angular acceleration "
    "of 2 rad/s². At t = 2 s, the magnitude of the total linear acceleration of a point on its rim is:",
    place("√65 m/s²", ["8 m/s²", "9 m/s²", "1 m/s²"], "D"),
    "Tangential and centripetal acceleration of a point of a rotating body",
    "A rim point has a tangential acceleration αR and a centripetal acceleration ω²R, at right angles to each "
    "other. At t = 2 s, ω = αt = 4 rad/s.",
    ["a_t = 2 × 0.5 = 1 m/s²", "a_c = 4² × 0.5 = 8 m/s²", "a = √(1 + 64) = √65 ≈ 8.06 m/s²"],
    why="8 m/s² is only the centripetal part; 1 m/s² only the tangential part; 9 m/s² adds two perpendicular "
        "components as scalars.",
    seconds=70, recomputed=True)

m_hb, M_pul, R_pul, h_fall = 2.0, 2.0, 0.2, 1.2
a_hb = m_hb * g / (m_hb + M_pul / 2)
v_hb = math.sqrt(2 * a_hb * h_fall)
w_pul = v_hb / R_pul
assert close(v_hb, 4) and close(w_pul, 20)
assert close(math.sqrt(2 * g * h_fall) / R_pul, 10 * math.sqrt(6))
assert close(math.sqrt(2 * (m_hb * g / (m_hb + M_pul)) * h_fall) / R_pul, 10 * math.sqrt(3))
add(T, "Rigid-body rotation", "Intermediate", "numerical",
    "A light string is wound round a pulley in the form of a uniform disc of mass 2 kg and radius 0.2 m, which "
    "rotates without friction about a fixed horizontal axle through its centre. A block of mass 2 kg hangs from "
    "the free end of the string and is released from rest. The string does not slip. Taking g = 10 m/s², the "
    "angular speed of the pulley when the block has descended 1.2 m is:",
    place("20 rad/s", ["10√6 rad/s", "10√3 rad/s", "4 rad/s"], "C"),
    "Energy conservation for a falling block and a rotating pulley",
    "The block's loss of potential energy goes into the block's kinetic energy and the pulley's rotational "
    "kinetic energy, with I = MR²/2 and v = ωR.",
    ["mgh = ½mv² + ½(MR²/2)(v/R)² → 24 = v² + 0.5v² ", "v² = 16 → v = 4 m/s", "ω = v/R = 20 rad/s"],
    why="10√6 rad/s ignores the pulley's rotational kinetic energy; 10√3 rad/s takes I = MR² (a ring); 4 rad/s "
        "is the block's speed in m/s, not the angular speed.",
    seconds=100, recomputed=True)

# square plate side 2a, top-right quarter removed
a_s = 1.0
pts = [(a_s / 2, a_s / 2), (3 * a_s / 2, a_s / 2), (a_s / 2, 3 * a_s / 2)]
cx = sum(p[0] for p in pts) / 3
cy = sum(p[1] for p in pts) / 3
shift = math.hypot(cx - a_s, cy - a_s)
assert close(cx, 5 / 6) and close(shift, math.sqrt(2) / 6) and cx < a_s
add(T, "Centre of mass", "Advanced", "numerical",
    "A thin uniform square plate has side 2a. One of its four quarters, a square of side a at one corner, is cut "
    "away. The centre of mass of the remaining L-shaped plate is shifted from the centre of the original square "
    "by a distance:",
    place("a√2/6, away from the removed corner", ["a√2/6, towards the removed corner",
                                                   "a√2/3, away from the removed corner", "a/6, parallel to a side"],
          "A"),
    "Centre of mass of a body with a part removed",
    "Treat the remaining plate as three equal squares, each of mass m, with centres at (a/2, a/2), (3a/2, a/2) "
    "and (a/2, 3a/2) when the original plate occupies 0 ≤ x, y ≤ 2a and the removed square is the one at the "
    "corner (2a, 2a).",
    ["x_cm = y_cm = (a/2 + 3a/2 + a/2)/3 = 5a/6", "Original centre: (a, a)",
     "Shift = √2 × (a − 5a/6) = a√2/6, along the diagonal away from the removed corner"],
    shortcut="Removing mass m at distance a√2/2 from the centre shifts the CM of the remaining 3m by "
             "(m/3m)(a√2/2) = a√2/6 the other way.",
    why="The centre of mass moves away from the region where mass was removed, not towards it; a√2/3 is twice the "
        "correct shift; a/6 gives only one coordinate of the shift.",
    ncert="Class 11 Physics, 'System of Particles and Rotational Motion', centre of mass", seconds=110,
    recomputed=True)

add(T, "Centre of mass", "Advanced", "assertion_reason",
    AR_STEM.format(
        a="A uniform rod standing vertically on a perfectly smooth horizontal floor is slightly disturbed and "
          "falls. During the fall its centre of mass moves along a vertical straight line.",
        r="The external forces on the rod (its weight and the normal reaction of the smooth floor) are both "
          "vertical, so the horizontal component of the acceleration of its centre of mass is zero."),
    ar("A"),
    "Motion of the centre of mass under external forces",
    "The centre of mass of a system moves as if all its mass were concentrated there and all external forces "
    "acted there. A smooth floor exerts no friction, so there is no horizontal external force. The CM starts "
    "with zero horizontal velocity and has zero horizontal acceleration, so it falls straight down (the foot "
    "slides sideways instead).",
    ["External forces: mg (down), N (up), no friction", "a_cm,x = 0 and v_cm,x(0) = 0 → CM moves vertically",
     "R gives this reason → A"],
    why="R is the reason the centre of mass has no horizontal motion, so B is wrong; both statements are true, so "
        "C and D are wrong.",
    ncert="Class 11 Physics, 'System of Particles and Rotational Motion', motion of centre of mass", seconds=70)

m_a, m_b2, F_ext = 1.0, 3.0, 8.0
a_cm = F_ext / (m_a + m_b2)
assert close(a_cm, 2)
multi_key([True, True, False, True, True], "abde")
add(T, "Centre of mass", "Advanced", "multi_statement",
    multi("Blocks of masses 1 kg and 3 kg, connected by a light spring, lie on a smooth horizontal floor. A "
          "constant horizontal force of 8 N, along the line of the spring, is applied to the 3 kg block only. "
          "Which of the following statements are correct?",
          ["The acceleration of the centre of mass of the system is 2 m/s².",
           "The acceleration of the centre of mass does not depend on how much the spring is stretched or "
           "compressed.", "The acceleration of the 3 kg block is 8/3 m/s² at every instant.",
           "The total linear momentum of the system increases at the rate of 8 kg m s⁻².",
           "If the force is removed at some instant, the velocity of the centre of mass stays constant after "
           "that."]),
    place("(a), (b), (d) and (e) only", ["(a), (b), (c) and (d) only", "(b), (c) and (e) only",
                                         "(a), (d) and (e) only"], "B"),
    "Centre of mass of a system with internal forces",
    "The spring force is internal: it changes the individual accelerations but not the motion of the centre of "
    "mass, which is fixed by the net external force: M a_cm = F_ext = dP/dt.",
    ["(a) a_cm = 8/4 = 2 m/s², true", "(b) internal forces do not affect a_cm, true",
     "(c) the 3 kg block also feels the spring force, which varies, so its acceleration is not always 8/3 m/s² "
     "→ false", "(d) dP/dt = F_ext = 8 N, true", "(e) no external horizontal force → v_cm constant, true"],
    why="Options with (c) ignore the spring force on the 3 kg block; omitting (b) or (e) misses that internal "
        "forces never change the motion of the centre of mass.",
    ncert="Class 11 Physics, 'System of Particles and Rotational Motion', motion of centre of mass; linear "
          "momentum of a system of particles", seconds=110, recomputed=True)

# =====================================================================================================================
# Gravitation (B2 I4 A3)
# =====================================================================================================================
T = "Gravitation"

W_e, g_e, g_p = 49.0, 9.8, 3.6
m_body = W_e / g_e
assert close(m_body, 5) and close(m_body * g_p, 18)
add(T, "Variation of g", "Basic", "numerical",
    "A body weighs 49 N on the Earth's surface, where g = 9.8 m/s². It is taken to a planet where the "
    "acceleration due to gravity at the surface is 3.6 m/s². Its mass and its weight on that planet are "
    "respectively:",
    place("5 kg and 18 N", ["1.8 kg and 18 N", "5 kg and 49 N", "13.6 kg and 49 N"], "D"),
    "Mass versus weight",
    "Mass is the amount of matter and does not change from place to place; weight is the gravitational force mg "
    "and depends on the local g.",
    ["m = 49/9.8 = 5 kg (same everywhere)", "Weight on planet = 5 × 3.6 = 18 N"],
    why="1.8 kg wrongly lets the mass change; '5 kg and 49 N' keeps the weight unchanged; 13.6 kg divides the "
        "Earth weight by the planet's g.",
    seconds=35, recomputed=True)

add(T, "Gravitational potential and energy", "Basic", "statement_pair",
    SP_STEM.format(
        s1="Taking the zero of potential energy at infinite separation, the gravitational potential energy of a "
           "system of two point masses is positive.",
        s2="The gravitational potential energy of a system of two point masses is directly proportional to the "
           "distance between them."),
    sp("B"),
    "Gravitational potential energy of two particles",
    "U = −Gm₁m₂/r with U = 0 at infinity. It is negative for every finite r (Statement I false) and varies as "
    "1/r, not as r (Statement II false). Its magnitude decreases as r increases, while U itself increases towards "
    "zero.",
    ["U = −Gm₁m₂/r < 0 → I false", "U ∝ −1/r, not ∝ r → II false"],
    why="Both statements contradict U = −Gm₁m₂/r, so every option calling either of them true is wrong.",
    ncert="Class 11 Physics, 'Gravitation', gravitational potential energy", seconds=40)

pct_T = 1.5 * (-2)
assert close(pct_T, -3)
assert close((0.98 ** 1.5 - 1) * 100, -2.98, rel=1e-2)
add(T, "Satellite energy and period", "Intermediate", "numerical",
    "Because of a small loss of energy, the radius of the circular orbit of a satellite round the Earth decreases "
    "by 2%. Its period of revolution:",
    place("decreases by about 3%", ["decreases by about 1%", "increases by about 3%", "decreases by about 2%"],
          "C"),
    "Kepler's third law for small changes",
    "For a circular orbit T² ∝ r³, so T ∝ r^(3/2). For a small change, the fractional change in T is 3/2 times "
    "the fractional change in r.",
    ["ΔT/T = (3/2)(Δr/r)", "= (3/2)(−2%) = −3%"],
    why="1% uses T ∝ r^(1/2) (the speed relation); 'increases' gets the sign wrong; 2% assumes T ∝ r.",
    ncert="Class 11 Physics, 'Gravitation', Kepler's laws; earth satellites", seconds=50, recomputed=True)


def near_surface_period(rho, R, G_=6.67e-11):
    M = rho * 4 / 3 * math.pi * R ** 3
    return 2 * math.pi * math.sqrt(R ** 3 / (G_ * M))


assert close(near_surface_period(5500, 1.28e7), near_surface_period(5500, 6.4e6))
add(T, "Satellite energy and period", "Intermediate", "numerical",
    "A satellite orbiting just above the surface of the Earth has period T. A planet has the same mean density as "
    "the Earth but twice its radius. Treating both as uniform spheres, the period of a satellite orbiting just "
    "above the surface of the planet is:",
    place("T", ["2T", "T/2", "√2 T"], "A"),
    "Period of a close-orbiting satellite in terms of density",
    "For an orbit of radius R about a uniform sphere, T = 2π√(R³/GM), and M = (4/3)πR³ρ. Substituting, "
    "T = √(3π/(Gρ)), which depends only on the density.",
    ["T = 2π√(R³/(G·(4/3)πR³ρ))", "= √(3π/(Gρ)) → same ρ gives the same T"],
    why="2T and √2 T forget that the planet's mass grows as R³; T/2 inverts the dependence.",
    ncert="Class 11 Physics, 'Gravitation', earth satellites", seconds=60, recomputed=True)

add(T, "Escape and orbital velocity", "Intermediate", "direct",
    "Two satellites of different masses revolve round the Earth in the same circular orbit. Which of the following "
    "is different for the two satellites?",
    place("Their kinetic energies", ["Their orbital speeds", "Their periods of revolution",
                                     "Their centripetal accelerations"], "B"),
    "Dependence of satellite quantities on the satellite's mass",
    "From GMm/r² = mv²/r, the orbital speed v = √(GM/r) does not depend on m; so neither does the period 2πr/v "
    "nor the acceleration GM/r². The kinetic energy ½mv² = GMm/(2r) is proportional to m.",
    ["v, T and a are independent of m", "K = GMm/2r ∝ m"],
    why="Speed, period and centripetal acceleration all cancel the satellite's mass, so they are the same for "
        "both satellites.",
    ncert="Class 11 Physics, 'Gravitation', earth satellites; energy of an orbiting satellite", seconds=40)

L_A = 2 * math.sqrt(1)            # m√(GMr) with m=2, r=1
L_B = 1 * math.sqrt(4)            # m=1, r=4
assert close(L_A / L_B, 1)
add(T, "Escape and orbital velocity", "Intermediate", "numerical",
    "Satellite A, of mass 2m, revolves round the Earth in a circular orbit of radius r. Satellite B, of mass m, "
    "revolves in a circular orbit of radius 4r. The ratio of the angular momentum of A about the Earth's centre "
    "to that of B is:",
    place("1 : 1", ["1 : 2", "2 : 1", "1 : 4"], "D"),
    "Angular momentum of a satellite in a circular orbit",
    "L = m v r with v = √(GM/r), so L = m√(GMr). Compare m√r for the two satellites.",
    ["L_A ∝ 2m × √r", "L_B ∝ m × √(4r) = 2m√r", "L_A : L_B = 1 : 1"],
    why="1 : 2 ignores the masses; 2 : 1 ignores the radii; 1 : 4 uses L ∝ m r instead of m√r.",
    seconds=60, recomputed=True)

R_E = 6.4e6
v_c = math.sqrt(g / R_E) * R_E
assert close(v_c, 8000)
add(T, "Variation of g", "Advanced", "numerical",
    "Imagine a straight narrow tunnel dug along a diameter of the Earth, treated as a uniform sphere of radius "
    "6400 km with g = 10 m/s² at its surface. A small body is released from rest at the mouth of the tunnel. "
    "Neglecting air resistance and the Earth's rotation, its speed as it passes the centre of the Earth is:",
    place("8 km/s", ["11.2 km/s", "5.66 km/s", "4 km/s"], "C"),
    "Gravity inside a uniform Earth: g ∝ distance from the centre",
    "Inside a uniform Earth, g(r) = g r/R, directed towards the centre, so the body's acceleration is −(g/R)r: "
    "simple harmonic motion with ω = √(g/R) and amplitude R. Its maximum speed, at the centre, is ωR = √(gR).",
    ["a = −(g/R) r → SHM, ω² = g/R", "v_max = ωR = √(gR) = √(10 × 6.4 × 10⁶) = 8000 m/s"],
    shortcut="Average force method: work done = ∫₀ᴿ m(g r/R) dr = mgR/2 = ½mv² → v = √(gR).",
    why="11.2 km/s is the escape speed from the surface; 5.66 km/s is √(gR/2); 4 km/s halves the answer.",
    ncert="Class 11 Physics, 'Gravitation', acceleration due to gravity below the surface of the earth",
    seconds=100, recomputed=True)

add(T, "Satellite energy and period", "Advanced", "assertion_reason",
    AR_STEM.format(
        a="When a satellite in a circular orbit round the Earth slowly loses mechanical energy because of a thin "
          "atmosphere, it spirals into lower orbits and its orbital speed increases.",
        r="The total energy of a satellite in a circular orbit of radius r is −GMm/(2r), so a loss of energy "
          "means a smaller r, and the orbital speed √(GM/r) is larger for a smaller r."),
    ar("A"),
    "Energy of an orbiting satellite",
    "E = −GMm/2r becomes more negative as r decreases; losing energy therefore moves the satellite inward. Its "
    "kinetic energy GMm/2r = −E then increases, while its potential energy −GMm/r decreases by twice as much. R "
    "states exactly this chain.",
    ["E ↓ → r ↓", "v = √(GM/r) ↑ as r ↓", "R explains A → A"],
    why="R is the full reason for the apparently surprising speed-up, so B is wrong; both statements are true, so "
        "C and D are wrong.",
    ncert="Class 11 Physics, 'Gravitation', energy of an orbiting satellite", seconds=70)

r_p, r_a = 1.0, 2.0
v_ratio = r_a / r_p
truth = [True, v_ratio == 2, v_ratio ** 2 == 4, (r_a / r_p) ** 2 == 4, False]
multi_key(truth, "abcd")
add(T, "Kepler's laws", "Advanced", "multi_statement",
    multi("A planet moves round the Sun in an elliptical orbit. Its distance from the Sun at aphelion (farthest "
          "point) is twice its distance at perihelion (nearest point). Which of the following statements are "
          "correct?",
          ["Its angular momentum about the Sun is the same at perihelion and at aphelion.",
           "Its speed at perihelion is twice its speed at aphelion.",
           "Its kinetic energy at perihelion is four times its kinetic energy at aphelion.",
           "The gravitational force on it at perihelion is four times the force at aphelion.",
           "Its total mechanical energy is greater at perihelion than at aphelion."]),
    place("(a), (b), (c) and (d) only", ["(a), (b) and (e) only", "(b), (c) and (d) only",
                                         "(a), (c) and (e) only"], "B"),
    "Kepler's second law and conservation laws for an elliptical orbit",
    "The Sun's force is central, so the planet's angular momentum is conserved (the basis of Kepler's second "
    "law). At perihelion and aphelion the velocity is perpendicular to the radius, so mv_p r_p = mv_a r_a. "
    "Gravity is conservative, so total energy is constant.",
    ["(a) true: central force", "(b) v_p/v_a = r_a/r_p = 2, true", "(c) K ∝ v² → 4 times, true",
     "(d) F ∝ 1/r² → 4 times, true", "(e) total energy is the same everywhere on the orbit → false"],
    why="Options with (e) confuse kinetic energy with total energy; omitting (a) misses the conservation law "
        "behind Kepler's second law.",
    ncert="Class 11 Physics, 'Gravitation', Kepler's laws", seconds=100, recomputed=True)

# =====================================================================================================================
# Properties of Solids and Liquids (B5 I7 A5)
# =====================================================================================================================
T = "Properties of Solids and Liquids"

p_g = 800 * g * 0.10 + 1000 * g * 0.20
assert close(p_g, 2800)
add(T, "Fluid pressure and Pascal's law", "Basic", "numerical",
    "An open vessel contains a 20 cm deep layer of water (density 1000 kg/m³) with a 10 cm deep layer of oil "
    "(density 800 kg/m³) floating on it. Taking g = 10 m/s², the gauge pressure at the bottom of the vessel is:",
    place("2800 Pa", ["3000 Pa", "2400 Pa", "800 Pa"], "A"),
    "Pressure due to liquid columns",
    "The gauge pressure at a depth is the weight per unit area of the liquid above. With two layers, add ρgh for "
    "each layer.",
    ["Oil: 800 × 10 × 0.10 = 800 Pa", "Water: 1000 × 10 × 0.20 = 2000 Pa", "Total = 2800 Pa"],
    why="3000 Pa treats both layers as water; 2400 Pa treats both as oil; 800 Pa counts only the oil layer.",
    ncert="Class 11 Physics, 'Mechanical Properties of Fluids', pressure (variation of pressure with depth)",
    seconds=40, recomputed=True)

add(T, "Elasticity and moduli", "Basic", "direct",
    "Wires of equal length and equal cross-section made of the materials below are stretched by equal loads. "
    "The extension is least for the wire made of:",
    place("Steel", ["Copper", "Aluminium", "Rubber"], "C"),
    "Young's modulus and extension",
    "Extension ΔL = FL/(AY). For equal F, L and A it is least for the largest Young's modulus. Steel "
    "(about 2 × 10¹¹ N/m²) has a larger Young's modulus than copper and aluminium, and rubber's is far smaller.",
    ["ΔL ∝ 1/Y", "Y: steel > copper > aluminium ≫ rubber"],
    why="Copper and aluminium have smaller Young's moduli than steel, and rubber stretches enormously, so all "
        "three extend more.",
    ncert="Class 11 Physics, 'Mechanical Properties of Solids', Young's modulus (table of Young's moduli)",
    seconds=30)

T_mix = (200 * 80 + 300 * 30) / 500
assert close(T_mix, 50)
add(T, "Thermal expansion and calorimetry", "Basic", "numerical",
    "200 g of water at 80 °C is mixed with 300 g of water at 30 °C in an insulated container of negligible heat "
    "capacity. The final temperature of the mixture is:",
    place("50 °C", ["55 °C", "60 °C", "45 °C"], "B"),
    "Principle of calorimetry",
    "In an insulated system, heat lost by the hot water equals heat gained by the cold water; the specific heat "
    "is the same for both, so it cancels.",
    ["200(80 − θ) = 300(θ − 30)", "16000 − 200θ = 300θ − 9000 → 500θ = 25000 → θ = 50 °C"],
    why="55 °C is the plain average of the temperatures; 60 °C swaps the masses; 45 °C is a slip in the weighted "
        "average.",
    ncert="Class 11 Physics, 'Thermal Properties of Matter', calorimetry", seconds=40, recomputed=True)

add(T, "Heat transfer", "Basic", "direct",
    "Which of the following has the lowest thermal conductivity?",
    place("Still air", ["Copper", "Steel", "Glass"], "D"),
    "Thermal conductivity of common materials",
    "Metals such as copper and steel are good conductors; glass is a poor conductor; still air is a much poorer "
    "conductor still (about 0.02 W m⁻¹ K⁻¹), which is why trapped air in wool, fibre glass or double windows "
    "insulates well.",
    ["Copper ≈ 400, steel ≈ 50, glass ≈ 1, still air ≈ 0.02 (W m⁻¹ K⁻¹)"],
    why="Copper and steel conduct heat very well, and glass, though a poor conductor, conducts far better than "
        "still air.",
    ncert="Class 11 Physics, 'Thermal Properties of Matter', conduction (table of thermal conductivities)",
    seconds=25)

add(T, "Elasticity and moduli", "Basic", "match_list",
    match_stem("Match List-I (situation) with List-II (type of stress mainly produced).",
               ["A wire from which a load hangs", "A solid metal ball resting at the bottom of a deep sea",
                "A thick book whose lower face is held fixed while its upper face is pushed sideways",
                "A pillar supporting the roof of a building"],
               ["Tensile stress", "Compressive stress", "Hydraulic stress", "Shearing stress"]),
    match_options({"A": "I", "B": "III", "C": "IV", "D": "II"},
                  [{"A": "I", "B": "II", "C": "IV", "D": "III"}, {"A": "II", "B": "III", "C": "IV", "D": "I"},
                   {"A": "I", "B": "III", "C": "II", "D": "IV"}], "B"),
    "Kinds of stress",
    "A pulling force along the length gives tensile stress; a pushing force along the length gives compressive "
    "stress; a force tangential to a face gives shearing stress; a uniform pressure from a surrounding fluid on "
    "all sides gives hydraulic stress (with a change of volume).",
    ["A: stretched → tensile (I)", "B: fluid pressure all round → hydraulic (III)",
     "C: tangential force → shearing (IV)", "D: squeezed along its length → compressive (II)"],
    why="The other codes confuse the uniform squeeze of a fluid (hydraulic) with the one-directional squeeze of a "
        "pillar (compressive), or a sideways push with compression.",
    ncert="Class 11 Physics, 'Mechanical Properties of Solids', stress and strain", seconds=50)

sig_b, rho_s = 8e8, 8000.0
L_max = sig_b / (rho_s * g)
assert close(L_max, 1e4)
add(T, "Elasticity and moduli", "Intermediate", "numerical",
    "The breaking stress of a certain steel is 8 × 10⁸ N/m² and its density is 8000 kg/m³. Taking g = 10 m/s², "
    "the greatest length of a uniform wire of this steel that can hang vertically from a rigid support without "
    "breaking under its own weight is:",
    place("10 km", ["20 km", "1 km", "100 km"], "D"),
    "Breaking stress of a wire under its own weight",
    "The stress is greatest at the top of the wire, which supports the weight of the whole wire: "
    "stress = (ρALg)/A = ρgL. The wire breaks when this reaches the breaking stress. The cross-section cancels.",
    ["ρ g L = 8 × 10⁸", "L = 8 × 10⁸/(8000 × 10) = 10⁴ m = 10 km"],
    why="20 km uses the average stress ρgL/2 instead of the greatest stress at the top; 1 km and 100 km are "
        "power-of-ten slips.",
    ncert="Class 11 Physics, 'Mechanical Properties of Solids', stress–strain curve (fracture point)", seconds=60,
    recomputed=True)

ratio_vt = (9000 - 1000) / (3000 - 1000)
assert close(ratio_vt, 4)
add(T, "Viscosity and Stokes' law", "Intermediate", "numerical",
    "Two small spheres of the same radius, with densities 9000 kg/m³ and 3000 kg/m³, fall through the same "
    "viscous liquid of density 1000 kg/m³. Assuming Stokes' law holds, the ratio of the terminal velocity of the "
    "denser sphere to that of the lighter one is:",
    place("4", ["3", "2", "9"], "A"),
    "Terminal velocity: dependence on densities",
    "At terminal velocity, weight = buoyant force + viscous drag, giving v_t = 2r²(ρ − σ)g/(9η). For equal radii "
    "in the same liquid, v_t ∝ (ρ − σ).",
    ["v₁/v₂ = (9000 − 1000)/(3000 − 1000)", "= 8000/2000 = 4"],
    why="3 is the ratio of the densities themselves, ignoring buoyancy; 9 squares it; 2 is a slip in subtracting "
        "the liquid's density.",
    ncert="Class 11 Physics, 'Mechanical Properties of Fluids', Stokes' law and terminal velocity", seconds=50,
    recomputed=True)

S_l, th_l, r_l, rho_l = 0.04, math.radians(60), 0.2e-3, 1000.0
h_l = 2 * S_l * math.cos(th_l) / (r_l * rho_l * g)
assert close(h_l, 0.02)
add(T, "Surface tension and capillarity", "Intermediate", "numerical",
    "A clean capillary tube of internal radius 0.2 mm stands vertically in a liquid of density 1000 kg/m³ and "
    "surface tension 0.04 N/m. The angle of contact between the liquid and the tube is 60°. Taking g = 10 m/s², "
    "the height to which the liquid rises in the tube is:",
    place("2 cm", ["4 cm", "1 cm", "2√3 cm"], "C"),
    "Capillary rise with a non-zero angle of contact",
    "The upward pull of surface tension around the rim, 2πrS cos θ, supports the weight of the raised column, "
    "πr²hρg, so h = 2S cos θ/(rρg).",
    ["h = 2 × 0.04 × 0.5/(0.2 × 10⁻³ × 1000 × 10)", "= 0.04/2 = 0.02 m = 2 cm"],
    why="4 cm ignores cos θ; 1 cm uses the diameter in place of the radius; 2√3 cm uses sin 60° in place of "
        "cos 60°.",
    ncert="Class 11 Physics, 'Mechanical Properties of Fluids', capillary rise", seconds=60, recomputed=True)

a1_e, a2_e, diff_e = 2e-5, 1.5e-5, 0.10
L1_e = diff_e / (a1_e / a2_e - 1)
L2_e = L1_e * a1_e / a2_e
assert close(L1_e, 0.3) and close(L2_e, 0.4) and close(L1_e * a1_e, L2_e * a2_e)
add(T, "Thermal expansion and calorimetry", "Intermediate", "numerical",
    "Two metal rods P and Q have coefficients of linear expansion 2.0 × 10⁻⁵ K⁻¹ and 1.5 × 10⁻⁵ K⁻¹ "
    "respectively. Their lengths are chosen so that the difference between their lengths is 10 cm at every "
    "temperature. The lengths of P and Q are respectively:",
    place("30 cm and 40 cm", ["40 cm and 30 cm", "10 cm and 20 cm", "20 cm and 30 cm"], "B"),
    "Linear expansion: ΔL = Lα ΔT",
    "The difference stays constant only if both rods expand by the same amount for any temperature change: "
    "L_P α_P = L_Q α_Q. The rod with the smaller α must be the longer one.",
    ["L_P × 2.0 = L_Q × 1.5 → L_Q = (4/3) L_P", "L_Q − L_P = L_P/3 = 10 cm → L_P = 30 cm, L_Q = 40 cm"],
    why="40 cm and 30 cm gives the longer length to the rod that expands more, so the difference would grow; "
        "the other pairs do not satisfy L_P α_P = L_Q α_Q.",
    ncert="Class 11 Physics, 'Thermal Properties of Matter', thermal expansion", seconds=80, recomputed=True)

add(T, "Heat transfer", "Intermediate", "match_list",
    match_stem("Match List-I (situation) with List-II (the main mode of heat transfer).",
               ["The handle of a metal spoon left in a cup of hot tea becomes hot",
                "A cool breeze blows from the sea towards the land during the day",
                "Heat is carried round the human body by the circulating blood",
                "Heat from the Sun reaches the Earth"],
               ["Conduction", "Natural convection", "Forced convection", "Radiation"]),
    match_options({"A": "I", "B": "II", "C": "III", "D": "IV"},
                  [{"A": "I", "B": "III", "C": "II", "D": "IV"}, {"A": "II", "B": "I", "C": "III", "D": "IV"},
                   {"A": "I", "B": "II", "C": "IV", "D": "III"}], "C"),
    "Modes of heat transfer",
    "In conduction heat passes through the material without bulk motion; in convection the material itself "
    "moves. In natural convection the motion is driven by gravity acting on density differences (sea breeze); in "
    "forced convection a pump or fan drives it (the heart pumping blood). Radiation needs no medium.",
    ["A: through the metal → conduction", "B: warm air over land rises → natural convection",
     "C: heart pumps blood → forced convection", "D: through space → radiation"],
    why="The other codes swap natural and forced convection or treat the sea breeze as conduction.",
    ncert="Class 11 Physics, 'Thermal Properties of Matter', heat transfer (conduction, convection, radiation)",
    seconds=50)

add(T, "Fluid pressure and Pascal's law", "Intermediate", "assertion_reason",
    AR_STEM.format(
        a="Three vessels of very different shapes, with bases of equal area, are filled with water to the same "
          "height. The pressure on the base is the same in all three, even though they hold different amounts "
          "of water.",
        r="The pressure at a depth h below the open surface of a liquid at rest is P = Pₐ + ρgh, which depends "
          "only on the depth and not on the shape or cross-section of the vessel."),
    ar("A"),
    "Hydrostatic paradox",
    "The pressure at the base depends only on the vertical depth of the liquid above it (and the atmospheric "
    "pressure), so equal heights give equal pressures whatever the shape. This is the 'hydrostatic paradox', and "
    "R states the law that resolves it.",
    ["P = Pₐ + ρgh: same h → same P", "R explains A → A"],
    why="R is exactly the reason for A, so B is wrong; both statements are true, so C and D are wrong.",
    ncert="Class 11 Physics, 'Mechanical Properties of Fluids', variation of pressure with depth (hydrostatic "
          "paradox)", seconds=50)

add(T, "Surface tension and capillarity", "Intermediate", "assertion_reason",
    AR_STEM.format(
        a="The excess pressure inside a soap bubble is twice the excess pressure inside a liquid drop of the same "
          "radius, made of a liquid of the same surface tension.",
        r="A soap bubble has two liquid–air surfaces (inner and outer), while a liquid drop has only one."),
    ar("A"),
    "Excess pressure across curved surfaces",
    "For one curved surface of radius r the excess pressure is 2S/r. A drop has one surface, so ΔP = 2S/r. The "
    "thin film of a bubble has two surfaces in series, so ΔP = 2 × 2S/r = 4S/r. R gives the reason for the "
    "factor of two.",
    ["Drop: 2S/r", "Bubble: 4S/r (two surfaces)", "R explains A → A"],
    why="R is precisely why the bubble's excess pressure is doubled, so B is wrong; both statements are true, so "
        "C and D are wrong.",
    ncert="Class 11 Physics, 'Mechanical Properties of Fluids', excess pressure inside a drop and a bubble",
    seconds=50)

v1_v, ratio_A, rho_w = 1.0, 3.0, 1000.0
v2_v = v1_v * ratio_A
dp_v = 0.5 * rho_w * (v2_v ** 2 - v1_v ** 2)
dh_v = dp_v / (rho_w * g)
assert close(dp_v, 4000) and close(dh_v, 0.40)
add(T, "Bernoulli's principle", "Advanced", "numerical",
    "Water flows steadily at 1 m/s through the wide part of a horizontal pipe, which narrows to one-third of that "
    "cross-sectional area. Two thin vertical tubes, open at the top, are fitted to the wide and the narrow "
    "parts. Treating water as non-viscous and incompressible (density 1000 kg/m³) and taking g = 10 m/s², the "
    "difference in the heights of water in the two vertical tubes is:",
    place("40 cm", ["4 cm", "80 cm", "45 cm"], "D"),
    "Equation of continuity with Bernoulli's principle",
    "Continuity gives the speed in the narrow part; Bernoulli's equation for a horizontal pipe gives the pressure "
    "difference; each vertical tube shows its pressure as a water column, so Δh = ΔP/(ρg).",
    ["v₂ = 3 × 1 = 3 m/s", "ΔP = ½ρ(v₂² − v₁²) = ½ × 1000 × 8 = 4000 Pa", "Δh = 4000/(1000 × 10) = 0.40 m"],
    why="80 cm drops the ½ in ½ρv²; 45 cm forgets v₁ (uses ½ρv₂²); 4 cm is a power-of-ten slip.",
    ncert="Class 11 Physics, 'Mechanical Properties of Fluids', equation of continuity; Bernoulli's principle",
    seconds=110, recomputed=True)

ms, mi, Lv, Lf = 10.0, 40.0, 540.0, 80.0
theta = (ms * Lv + ms * 100 - mi * Lf) / (ms + mi)
assert close(theta, 64)
assert ms * Lv > mi * Lf and 0 < theta < 100
add(T, "Thermal expansion and calorimetry", "Advanced", "numerical",
    "10 g of steam at 100 °C is passed into an insulated container of negligible heat capacity holding 40 g of "
    "ice at 0 °C. All the steam condenses. Take the latent heat of vaporisation of water as 540 cal g⁻¹, the "
    "latent heat of fusion of ice as 80 cal g⁻¹ and the specific heat of water as 1 cal g⁻¹ °C⁻¹. The final "
    "temperature of the contents is:",
    place("64 °C", ["48 °C", "80 °C", "100 °C"], "B"),
    "Calorimetry with two changes of state",
    "First check whether all the ice melts: the steam can give 10 × 540 = 5400 cal just by condensing, more than "
    "the 40 × 80 = 3200 cal needed to melt the ice. So the final state is 50 g of water at some θ between 0 °C "
    "and 100 °C.",
    ["Heat given: 10 × 540 + 10 × 1 × (100 − θ)", "Heat taken: 40 × 80 + 40 × 1 × θ",
     "5400 + 1000 − 10θ = 3200 + 40θ → 50θ = 3200 → θ = 64 °C"],
    why="48 °C ignores the cooling of the condensed steam from 100 °C; 80 °C ignores the latent heat of fusion; "
        "100 °C assumes some steam stays uncondensed, contrary to the stem.",
    ncert="Class 11 Physics, 'Thermal Properties of Matter', change of state and latent heat; calorimetry",
    seconds=120, recomputed=True)

rho_blk = 4000.0
ext_w = 1.0 * (1 - 1000 / rho_blk)
assert close(ext_w, 0.75)
add(T, "Elasticity and moduli", "Advanced", "numerical",
    "A solid block of density 4000 kg/m³ hangs from a light steel wire, which is stretched by 1.0 mm. The block "
    "is then completely immersed in water (density 1000 kg/m³), still hanging from the wire and not touching the "
    "container. Within the elastic limit, the extension of the wire becomes:",
    place("0.75 mm", ["0.25 mm", "0.80 mm", "1.0 mm"], "A"),
    "Hooke's law combined with buoyancy",
    "The extension is proportional to the tension. In water the tension is the weight minus the buoyant force: "
    "T = Vρg − Vρ_w g = W(1 − ρ_w/ρ).",
    ["T'/T = 1 − 1000/4000 = 3/4", "Extension = 0.75 × 1.0 mm = 0.75 mm"],
    why="0.25 mm keeps only the buoyant part; 0.80 mm uses a density ratio of 1/5; 1.0 mm ignores the upthrust.",
    ncert="Class 11 Physics, 'Mechanical Properties of Solids', Hooke's law and Young's modulus", seconds=70,
    recomputed=True)

alpha_s, dT_s = 2e-5, 100.0
fr = alpha_s * dT_s
truth = [close(fr, 0.002), close(2 * fr, 0.004), close(3 * fr, 0.006), close(1 - 1 / (1 + 3 * fr), 0.006, rel=1e-2),
         False]
multi_key(truth, "abcd")
add(T, "Thermal expansion and calorimetry", "Advanced", "multi_statement",
    multi("A solid metal sphere, with coefficient of linear expansion 2 × 10⁻⁵ K⁻¹, is heated from 20 °C to "
          "120 °C. Which of the following statements are correct (to a good approximation)?",
          ["Its radius increases by 0.2%.", "Its surface area increases by 0.4%.",
           "Its volume increases by 0.6%.", "Its density decreases by about 0.6%.",
           "Its mass increases by 0.6%."]),
    place("(a), (b), (c) and (d) only", ["(a), (b) and (e) only", "(a), (c), (d) and (e) only",
                                         "(b), (c) and (d) only"], "C"),
    "Linear, area and volume expansion",
    "For small changes, ΔL/L = αΔT, ΔA/A = 2αΔT and ΔV/V = 3αΔT. The mass does not change, so the density "
    "falls by the same fraction by which the volume rises.",
    ["(a) αΔT = 2 × 10⁻⁵ × 100 = 0.2%, true", "(b) 2αΔT = 0.4%, true", "(c) 3αΔT = 0.6%, true",
     "(d) ρ ∝ 1/V → falls by ≈ 0.6%, true", "(e) heating does not change mass → false"],
    why="Options with (e) confuse volume with mass; leaving out (b), (c) or (d) misses the factors 2 and 3 for "
        "area and volume.",
    ncert="Class 11 Physics, 'Thermal Properties of Matter', thermal expansion", seconds=90, recomputed=True)

add(T, "Heat transfer", "Advanced", "statement_pair",
    SP_STEM.format(
        s1="Two rods of the same cross-section but different thermal conductivities are joined end to end, their "
           "sides insulated, and conduct heat in the steady state. The temperature gradient is larger in the rod "
           "of smaller thermal conductivity.",
        s2="If the two rods are interchanged, keeping the temperatures of the two free ends unchanged, the rate of "
           "heat flow through the combination changes."),
    sp("C"),
    "Steady-state conduction through rods in series",
    "In the steady state the same heat current H flows through both rods: H = KA (dT/dx). With H and A the same, "
    "the gradient dT/dx = H/(KA) is larger where K is smaller (Statement I true). The total thermal resistance "
    "L₁/(K₁A) + L₂/(K₂A) does not depend on the order of the rods, so H is unchanged (Statement II false).",
    ["Same H in both → dT/dx ∝ 1/K → I true", "R_total = R₁ + R₂, order-independent → II false"],
    why="Series resistances add in either order, so the options calling II true are wrong; Statement I follows "
        "from the equal heat current, so the options calling it false are wrong.",
    ncert="Class 11 Physics, 'Thermal Properties of Matter', conduction (steady state, thermal conductivity)",
    seconds=70)

# =====================================================================================================================
# Thermodynamics (B3 I4 A2)
# =====================================================================================================================
T = "Thermodynamics"
R = 8.3

dU = 2 * 1.5 * R * 50
assert close(dU, 1245)
add(T, "Zeroth and first law", "Basic", "numerical",
    "The temperature of 2 moles of a monatomic ideal gas rises by 50 K. Taking R = 8.3 J mol⁻¹ K⁻¹, the increase "
    "in its internal energy, whatever the process by which the change is made, is:",
    place("1245 J", ["2075 J", "830 J", "2490 J"], "D"),
    "Internal energy of an ideal gas is a function of temperature only",
    "For an ideal gas, U depends only on T, so ΔU = nC_vΔT in every process, with C_v = 3R/2 for a monatomic "
    "gas.",
    ["ΔU = 2 × (3/2)(8.3) × 50 = 1245 J"],
    why="2075 J uses C_p = 5R/2 (that is the heat at constant pressure); 830 J uses R; 2490 J uses 3R.",
    ncert="Class 11 Physics, 'Thermodynamics', internal energy; specific heat capacity", seconds=40,
    recomputed=True)

add(T, "Zeroth and first law", "Basic", "direct",
    "Which of the following thermodynamic variables is extensive (depends on the size of the system)?",
    place("Internal energy", ["Pressure", "Temperature", "Density"], "C"),
    "Extensive and intensive variables",
    "If a system in equilibrium is divided into two equal parts, an extensive variable (internal energy, mass, "
    "volume) is halved in each part, while an intensive variable (pressure, temperature, density) is unchanged.",
    ["Halve the system: U → U/2 (extensive)", "P, T, ρ unchanged (intensive)"],
    why="Pressure, temperature and density are the same in each half of a system in equilibrium, so they are "
        "intensive.",
    ncert="Class 11 Physics, 'Thermodynamics', thermodynamic state variables", seconds=25)

n_m = 2
mt = {"A": n_m * 1.5 * R * 10, "B": n_m * R * 10, "C": 500.0, "D": -300.0}
assert close(mt["A"], 249) and close(mt["B"], 166)
add(T, "Zeroth and first law", "Basic", "match_list",
    match_stem("Two moles of a monatomic ideal gas undergo, separately, each process in List-I. Take "
               "R = 8.3 J mol⁻¹ K⁻¹. Match List-I (process) with List-II (value of the stated quantity).",
               ["Heated at constant volume so that its temperature rises by 10 K: heat absorbed",
                "Heated at constant pressure so that its temperature rises by 10 K: work done by the gas",
                "Expands isothermally, absorbing 500 J of heat: work done by the gas",
                "Expands adiabatically, doing 300 J of work: change in its internal energy"],
               ["−300 J", "166 J", "249 J", "500 J"]),
    match_options({"A": "III", "B": "II", "C": "IV", "D": "I"},
                  [{"A": "II", "B": "III", "C": "IV", "D": "I"}, {"A": "III", "B": "II", "C": "I", "D": "IV"},
                   {"A": "IV", "B": "II", "C": "III", "D": "I"}], "A"),
    "First law of thermodynamics in the four basic processes",
    "Apply ΔQ = ΔU + ΔW with ΔU = nC_vΔT (C_v = 3R/2 for a monatomic gas). At constant volume no work is done; at "
    "constant pressure W = PΔV = nRΔT; isothermally ΔU = 0 so W = Q; adiabatically Q = 0 so ΔU = −W.",
    ["A: Q = nC_vΔT = 2 × 1.5 × 8.3 × 10 = 249 J → III", "B: W = nRΔT = 2 × 8.3 × 10 = 166 J → II",
     "C: ΔU = 0 → W = Q = 500 J → IV", "D: Q = 0 → ΔU = −300 J → I"],
    why="The other codes swap the isochoric heat with the isobaric work, or give the adiabatic ΔU the wrong sign "
        "(or treat the isothermal heat as a change in internal energy).",
    ncert="Class 11 Physics, 'Thermodynamics', first law of thermodynamics; thermodynamic processes", seconds=60,
    recomputed=True)

dU_AC = 300 + (500 - 200)
Q_direct = dU_AC + 150
assert dU_AC == 600 and Q_direct == 750
add(T, "Zeroth and first law", "Intermediate", "numerical",
    "An ideal gas is taken from state A to state B at constant volume, absorbing 300 J of heat. It is then taken "
    "from B to state C at constant pressure, absorbing 500 J of heat and doing 200 J of work. If the gas is "
    "instead taken from A to C along a different path in which it does 150 J of work, the heat it absorbs along "
    "that path is:",
    place("750 J", ["800 J", "600 J", "450 J"], "B"),
    "Internal energy as a state function; first law",
    "Find ΔU from A to C using the first path. ΔU is the same for every path between the same states, so apply "
    "the first law on the new path.",
    ["A→B: W = 0, ΔU = 300 J", "B→C: ΔU = 500 − 200 = 300 J", "ΔU_AC = 600 J",
     "New path: Q = ΔU + W = 600 + 150 = 750 J"],
    why="800 J adds the heats of the first path, as if heat were a state function; 600 J forgets the work on the "
        "new path; 450 J subtracts the work instead of adding it.",
    ncert="Class 11 Physics, 'Thermodynamics', first law of thermodynamics", seconds=80, recomputed=True)

P0, dV, Lw = 1.0e5, 1700e-6, 2260.0
W_b = P0 * dV
dU_b = Lw - W_b
assert close(W_b, 170) and close(dU_b, 2090)
add(T, "Zeroth and first law", "Intermediate", "numerical",
    "1 g of water at 100 °C, occupying 1 cm³, is converted into 1701 cm³ of steam at 100 °C at a constant "
    "pressure of 1.0 × 10⁵ Pa. The latent heat of vaporisation of water is 2260 J g⁻¹. The work done by the "
    "system and the increase in its internal energy are respectively:",
    place("170 J and 2090 J", ["170 J and 2430 J", "0 and 2260 J", "2260 J and 170 J"], "D"),
    "First law applied to a change of state",
    "The heat supplied is the latent heat, 2260 J. Part of it is used as work against the constant external "
    "pressure while the volume grows by 1700 cm³; the rest increases the internal energy.",
    ["W = PΔV = 1.0 × 10⁵ × 1700 × 10⁻⁶ = 170 J", "ΔU = Q − W = 2260 − 170 = 2090 J"],
    why="2430 J adds the work instead of subtracting it; '0 and 2260 J' ignores the expansion; '2260 J and "
        "170 J' swaps the two quantities.",
    ncert="Class 11 Physics, 'Thermodynamics', first law of thermodynamics", seconds=80, recomputed=True)

add(T, "Second law, reversible and irreversible processes", "Intermediate", "statement_pair",
    SP_STEM.format(
        s1="Heat can flow by itself, with no other effect, from a colder body to a hotter body.",
        s2="After a system has undergone an irreversible process, it can never be brought back to its initial "
           "state by any means."),
    sp("B"),
    "Second law of thermodynamics and irreversible processes",
    "Statement I contradicts the Clausius statement of the second law: heat cannot pass from a colder to a hotter "
    "body as the sole result of a process. Statement II misreads 'irreversible': the system itself can be returned "
    "to its initial state (for example, a freely expanded gas can be compressed back), but not without leaving "
    "some change in the surroundings, such as work done on the system or heat given to a reservoir.",
    ["I violates the Clausius statement → false",
     "II: the system can be restored, only the surroundings cannot also be restored with no other change → false"],
    why="Irreversibility means the system and the surroundings cannot both be restored with no other change "
        "anywhere; it does not mean the system alone can never return. Statement I is false because heat does not "
        "flow by itself from a colder to a hotter body.",
    ncert="Class 11 Physics, 'Thermodynamics', second law of thermodynamics; reversible and irreversible processes",
    seconds=50)

add(T, "Isothermal and adiabatic processes", "Intermediate", "assertion_reason",
    AR_STEM.format(
        a="When an ideal gas expands at constant pressure, its internal energy decreases.",
        r="The internal energy of a given amount of an ideal gas depends only on its temperature."),
    ar("D"),
    "Internal energy in an isobaric process",
    "At constant pressure, V/T is constant for an ideal gas, so an expansion (V increasing) means a rise in "
    "temperature. Since U depends only on T (R is true), U increases: A is false.",
    ["P constant → V ∝ T", "Expansion → T ↑ → U ↑ → A false", "U = U(T) → R true"],
    why="A is false, so options A, B and C (which all call A true) are wrong.",
    ncert="Class 11 Physics, 'Thermodynamics', internal energy; thermodynamic processes", seconds=50)

Cv = 1.5
C_proc = 2 * Cv                # Q = 2 dU when W = Q/2
assert C_proc == 3
add(T, "Zeroth and first law", "Advanced", "numerical",
    "A monatomic ideal gas is heated in a process during which the work done by the gas is always half the heat "
    "supplied to it. The molar heat capacity of the gas in this process is (R is the gas constant):",
    place("3R", ["3R/2", "5R/2", "2R"], "C"),
    "Molar heat capacity for a general process from the first law",
    "If W = Q/2 then ΔU = Q − W = Q/2, i.e. Q = 2ΔU = 2nC_vΔT. The molar heat capacity is C = Q/(nΔT).",
    ["ΔU = Q/2", "Q = 2n(3R/2)ΔT = 3nRΔT", "C = 3R"],
    why="3R/2 is C_v (no work); 5R/2 is C_p, for which W = 2Q/5, not Q/2; 2R does not follow from the given "
        "condition.",
    ncert="Class 11 Physics, 'Thermodynamics', first law of thermodynamics; specific heat capacity", seconds=80,
    recomputed=True)

gam, n_g, T0g = 1.5, 2, 300.0
T_after = T0g * 4 ** (1 - gam)                 # T V^(γ-1) constant, V → 4V
Cv_g = R / (gam - 1)
Q_back = n_g * Cv_g * (T0g - T_after)
assert close(T_after, 150) and close(Cv_g, 2 * R) and close(Q_back, 4980)
assert close(n_g * R * 150, 2490) and close(n_g * 3 * R * 150, 7470) and close(n_g * 1.5 * R * 150, 3735)
add(T, "Isothermal and adiabatic processes", "Advanced", "numerical",
    "Two moles of an ideal gas with γ = C_p/C_v = 1.5, initially at 300 K, expand reversibly and adiabatically "
    "until the volume is 4 times its initial value. The gas is then heated at constant volume until its "
    "temperature is again 300 K. Taking R = 8.3 J mol⁻¹ K⁻¹, the heat absorbed by the gas in the constant-volume "
    "step is:",
    place("4980 J", ["2490 J", "7470 J", "3735 J"], "A"),
    "Reversible adiabatic process followed by an isochoric process",
    "In a reversible adiabatic process TV^(γ−1) is constant, which gives the temperature after the expansion. "
    "For the constant-volume step W = 0, so Q = ΔU = nC_vΔT, with C_v = R/(γ − 1).",
    ["T₂ = 300 × (1/4)^(0.5) = 150 K", "C_v = R/(1.5 − 1) = 2R",
     "Q = 2 × 2 × 8.3 × (300 − 150) = 4980 J"],
    why="2490 J takes C_v = R; 7470 J uses C_p = 3R although the volume is constant; 3735 J uses the monatomic "
        "value 3R/2 instead of the C_v that follows from γ = 1.5.",
    ncert="Class 11 Physics, 'Thermodynamics', adiabatic process; isochoric process; specific heat capacity",
    seconds=110, recomputed=True)

# =====================================================================================================================
# Kinetic Theory of Gases (B2 I2 A2)
# =====================================================================================================================
T = "Kinetic Theory of Gases"

p_O2 = 1e5 * 3 / 5
assert close(p_O2, 6e4)
add(T, "Ideal gas equation", "Basic", "numerical",
    "A vessel contains a mixture of 2 moles of nitrogen and 3 moles of oxygen, both behaving as ideal gases and "
    "not reacting with each other. The total pressure is 1.0 × 10⁵ Pa. The partial pressure of oxygen is:",
    place("6.0 × 10⁴ Pa", ["4.0 × 10⁴ Pa", "1.0 × 10⁵ Pa", "5.0 × 10⁴ Pa"], "B"),
    "Dalton's law of partial pressures",
    "Each gas in the mixture exerts the pressure it would exert alone in the same volume at the same "
    "temperature: Pᵢ = nᵢRT/V. So the partial pressure is proportional to the number of moles, and the partial "
    "pressures add up to the total.",
    ["P_O₂ = (3/5) × 1.0 × 10⁵ = 6.0 × 10⁴ Pa"],
    why="4.0 × 10⁴ Pa is the partial pressure of nitrogen; 1.0 × 10⁵ Pa is the total; 5.0 × 10⁴ Pa splits the "
        "pressure equally regardless of the amounts.",
    ncert="Class 11 Physics, 'Kinetic Theory', kinetic theory of an ideal gas (Dalton's law of partial "
          "pressures)", seconds=35, recomputed=True)

add(T, "Degrees of freedom and equipartition", "Basic", "statement_pair",
    SP_STEM.format(
        s1="A molecule of a monatomic gas has only translational degrees of freedom, three in number.",
        s2="According to the law of equipartition of energy, each vibrational mode of a molecule contributes "
           "k_BT to the average energy, since it has both kinetic and potential energy terms."),
    sp("A"),
    "Degrees of freedom and the law of equipartition",
    "A monatomic molecule can only move along x, y and z: 3 translational degrees of freedom (Statement I true). "
    "Each quadratic energy term contributes ½k_BT; a vibrational mode has a kinetic and a potential term, so it "
    "contributes 2 × ½k_BT = k_BT (Statement II true).",
    ["Monatomic: f = 3 (translation only) → I true", "Vibration: ½k_BT (KE) + ½k_BT (PE) = k_BT → II true"],
    why="Both statements are as given by the law of equipartition, so every option calling one of them false is "
        "wrong.",
    ncert="Class 11 Physics, 'Kinetic Theory', law of equipartition of energy", seconds=45)

lam0, vbar = 2.0e-7, 400.0
f0 = vbar / lam0
f1 = vbar / (lam0 / 2)
assert close(f0, 2e9) and close(f1, 4e9)
add(T, "Mean free path", "Intermediate", "numerical",
    "In a gas, the mean free path of the molecules is 2.0 × 10⁻⁷ m and their average speed is 400 m/s, so each "
    "molecule makes on average 2 × 10⁹ collisions per second. The pressure of the gas is now doubled at the "
    "same temperature. The average number of collisions per second made by a molecule becomes about:",
    place("4 × 10⁹", ["2 × 10⁹", "1 × 10⁹", "8 × 10⁹"], "D"),
    "Mean free path and collision frequency",
    "The mean free path is λ = 1/(√2 π n d²). At constant temperature, doubling the pressure doubles the number "
    "density n, so λ is halved. The molecular speed depends only on temperature and stays the same. The "
    "collision rate v/λ therefore doubles.",
    ["n → 2n → λ → λ/2 = 1.0 × 10⁻⁷ m", "Speed unchanged (same T)", "Rate = 400/(1.0 × 10⁻⁷) = 4 × 10⁹ s⁻¹"],
    why="2 × 10⁹ ignores the change in λ; 1 × 10⁹ makes λ grow with pressure; 8 × 10⁹ also doubles the speed.",
    ncert="Class 11 Physics, 'Kinetic Theory', mean free path", seconds=60, recomputed=True)

add(T, "Mean free path", "Intermediate", "match_list",
    match_stem("The mean free path of the molecules of an ideal gas is λ. Each change in List-I is made starting "
               "from the same original state, with everything not mentioned kept the same. Match List-I (change) "
               "with List-II (new mean free path).",
               ["The pressure is doubled at constant temperature",
                "The absolute temperature is doubled at constant pressure",
                "The absolute temperature is doubled at constant volume",
                "Molecules of twice the diameter are used, at the same number density"],
               ["λ/4", "λ/2", "λ", "2λ"]),
    match_options({"A": "II", "B": "IV", "C": "III", "D": "I"},
                  [{"A": "IV", "B": "II", "C": "III", "D": "I"}, {"A": "II", "B": "III", "C": "IV", "D": "I"},
                   {"A": "II", "B": "IV", "C": "I", "D": "III"}], "C"),
    "Dependence of mean free path on number density and molecular size",
    "λ = 1/(√2 π n d²), and for an ideal gas n = P/(k_BT).",
    ["A: n doubles → λ/2 (II)", "B: n = P/kT halves → 2λ (IV)", "C: n unchanged (fixed V) → λ (III)",
     "D: d² four times → λ/4 (I)"],
    why="The other codes let the temperature change λ even at constant volume, or treat d instead of d² as "
        "deciding the mean free path.",
    ncert="Class 11 Physics, 'Kinetic Theory', mean free path", seconds=70)

kB, eV = 1.38e-23, 1.6e-19
T_eV = 2 * eV / (3 * kB)
assert close(T_eV, 7.73e3, rel=1e-2)
add(T, "Pressure and rms speed", "Advanced", "numerical",
    "Taking Boltzmann's constant as 1.38 × 10⁻²³ J K⁻¹ and 1 eV = 1.6 × 10⁻¹⁹ J, the temperature at which the "
    "average translational kinetic energy of a molecule of an ideal gas equals 1 eV is about:",
    place("7.7 × 10³ K", ["1.16 × 10⁴ K", "2.32 × 10⁴ K", "773 K"], "A"),
    "Kinetic interpretation of temperature",
    "The average translational kinetic energy of a molecule is (3/2)k_BT. Set it equal to 1.6 × 10⁻¹⁹ J.",
    ["(3/2)k_BT = 1.6 × 10⁻¹⁹", "T = 2 × 1.6 × 10⁻¹⁹/(3 × 1.38 × 10⁻²³) ≈ 7.7 × 10³ K"],
    why="1.16 × 10⁴ K uses k_BT = 1 eV; 2.32 × 10⁴ K uses ½k_BT; 773 K is a power-of-ten slip.",
    ncert="Class 11 Physics, 'Kinetic Theory', kinetic interpretation of temperature", seconds=70,
    recomputed=True)

n_he = 2 / 4
U_he = n_he * 1.5 * R * 300
P_he = n_he * R * 300 / 8.3e-3
Q_he = n_he * 2.5 * R * 10
truth = [close(U_he, 1867.5), close(P_he, 1.5e5), close(n_he * 1.5 * R, 12.45), False, close(Q_he, 103.75)]
multi_key(truth, "abe")
add(T, "Ideal gas equation", "Advanced", "multi_statement",
    multi("A closed vessel of volume 8.3 L holds 2 g of helium (molar mass 4 g/mol), treated as a monatomic ideal "
          "gas, at 300 K. Taking R = 8.3 J mol⁻¹ K⁻¹, which of the following statements are correct?",
          ["The internal energy of the gas is 1867.5 J.", "The pressure of the gas is 1.5 × 10⁵ Pa.",
           "The heat capacity of this sample at constant volume is 12.45 J K⁻¹.",
           "If its absolute temperature is doubled at constant volume, the rms speed of its atoms doubles.",
           "If the sample were heated at constant pressure instead, 103.75 J would raise its temperature by "
           "10 K."]),
    place("(a), (b) and (e) only", ["(a), (b), (c) and (e) only", "(b), (d) and (e) only", "(a), (c) and (d) only"],
          "B"),
    "Ideal gas equation, internal energy and specific heats",
    "The sample contains n = 2/4 = 0.5 mol. Use U = n(3/2)RT, P = nRT/V, heat capacity nC_v, v_rms ∝ √T and "
    "Q = nC_pΔT.",
    ["(a) U = 0.5 × 1.5 × 8.3 × 300 = 1867.5 J, true",
     "(b) P = 0.5 × 8.3 × 300/(8.3 × 10⁻³) = 1.5 × 10⁵ Pa, true",
     "(c) nC_v = 0.5 × 12.45 = 6.225 J/K, not 12.45 → false", "(d) v_rms ∝ √T → ×√2, not ×2 → false",
     "(e) Q = 0.5 × 2.5 × 8.3 × 10 = 103.75 J, true"],
    why="(c) gives the molar value for one mole instead of 0.5 mol; (d) forgets the square root in v_rms ∝ √T.",
    ncert="Class 11 Physics, 'Kinetic Theory', ideal gas equation; specific heat capacity of gases", seconds=120,
    recomputed=True)

# =====================================================================================================================
# Oscillations and Waves (B5 I6 A5)
# =====================================================================================================================
T = "Oscillations and Waves"

A_o = 4.0
x_half = math.sqrt(A_o ** 2 - (A_o / 2) ** 2)
assert close(x_half, 2 * math.sqrt(3))
add(T, "Energy in SHM", "Basic", "numerical",
    "A particle executes simple harmonic motion with an amplitude of 4 cm. At what distance from the mean "
    "position is its speed half of its maximum speed?",
    place("2√3 cm", ["2 cm", "2√2 cm", "3 cm"], "C"),
    "Speed as a function of displacement in SHM",
    "In SHM, v = ω√(A² − x²) and v_max = ωA. Setting v = ωA/2 gives A² − x² = A²/4.",
    ["x² = A² − A²/4 = 3A²/4", "x = (√3/2) × 4 = 2√3 cm ≈ 3.46 cm"],
    why="2 cm (= A/2) is where the speed is (√3/2)v_max; 2√2 cm is where kinetic and potential energies are "
        "equal; 3 cm does not follow from v = ω√(A² − x²).",
    ncert="Class 11 Physics, 'Oscillations', velocity in simple harmonic motion", seconds=45, recomputed=True)

f0c = 150
harm = [n * f0c for n in range(1, 20, 2) if n * f0c < 1000]
assert harm == [150, 450, 750]
add(T, "Organ pipes and beats", "Basic", "numerical",
    "A pipe closed at one end has a fundamental frequency of 150 Hz. Neglecting end corrections, the number of "
    "its natural frequencies (normal modes) below 1000 Hz is:",
    place("3", ["6", "4", "2"], "B"),
    "Normal modes of a pipe closed at one end",
    "A pipe closed at one end has only the odd harmonics of its fundamental: f, 3f, 5f, 7f, …",
    ["150, 450, 750 Hz are below 1000 Hz", "The next, 1050 Hz, is above → 3 modes"],
    why="6 counts all multiples of 150 Hz below 1000 Hz, as for an open pipe; 4 and 2 miscount the odd harmonics.",
    ncert="Class 11 Physics, 'Waves', standing waves in pipes closed at one end", seconds=40, recomputed=True)

add(T, "Progressive waves and wave speed", "Basic", "direct",
    "The speed of transverse waves on a stretched string does NOT depend on:",
    place("The frequency of the wave", ["The tension in the string", "The mass per unit length of the string",
                                        "The diameter of the string, for a given material"], "D"),
    "Speed of a transverse wave on a string",
    "The speed is v = √(T/μ), fixed by the tension T and the mass per unit length μ (which depends on the "
    "material and the diameter). Changing the frequency of the source changes the wavelength, λ = v/f, not v.",
    ["v = √(T/μ)", "f changes → λ changes, v unchanged"],
    why="Tension and mass per unit length appear directly in v = √(T/μ), and for a given material μ grows with "
        "the square of the diameter.",
    ncert="Class 11 Physics, 'Waves', speed of a transverse wave on a stretched string", seconds=30)

add(T, "Spring and pendulum oscillations", "Basic", "match_list",
    match_stem("Match List-I (oscillating system, small oscillations) with List-II (its period).",
               ["A block of mass m attached to a light spring of force constant k",
                "A simple pendulum of length L at a place where the acceleration due to gravity is g",
                "The same simple pendulum hanging in a lift that accelerates upward with acceleration a",
                "A block of mass m attached to two light springs, each of force constant k, connected in parallel"],
               ["2π√(L/(g + a))", "2π√(m/2k)", "2π√(m/k)", "2π√(L/g)"]),
    match_options({"A": "III", "B": "IV", "C": "I", "D": "II"},
                  [{"A": "II", "B": "IV", "C": "I", "D": "III"}, {"A": "III", "B": "I", "C": "IV", "D": "II"},
                   {"A": "III", "B": "IV", "C": "II", "D": "I"}], "A"),
    "Periods of spring and pendulum oscillators",
    "A spring–block system has T = 2π√(m/k); springs in parallel add their force constants (2k). A simple "
    "pendulum has T = 2π√(L/g); in a lift accelerating upward the effective gravity is g + a.",
    ["A → 2π√(m/k)", "B → 2π√(L/g)", "C → 2π√(L/(g + a))", "D → k_eff = 2k → 2π√(m/2k)"],
    why="The other codes swap the series/parallel result or use g − a for an upward acceleration.",
    ncert="Class 11 Physics, 'Oscillations', oscillations due to a spring; the simple pendulum", seconds=50)

add(T, "Organ pipes and beats", "Basic", "statement_pair",
    SP_STEM.format(
        s1="A pipe open at both ends has displacement nodes at both its open ends.",
        s2="A pipe closed at one end has a displacement node at its closed end and a displacement antinode at its "
           "open end."),
    sp("D"),
    "Boundary conditions for standing waves in pipes",
    "The air at a closed end cannot move, so it is a displacement node. At an open end the air moves freely, so "
    "it is a displacement antinode. Hence an open pipe has antinodes (not nodes) at both ends (Statement I "
    "false), and a closed pipe has a node at the closed end and an antinode at the open end (Statement II true).",
    ["Open end → displacement antinode → I false", "Closed end node, open end antinode → II true"],
    why="Statement I reverses the condition at an open end, so options calling it true are wrong; Statement II "
        "is the correct pair of boundary conditions.",
    ncert="Class 11 Physics, 'Waves', standing waves in pipes", seconds=40)

vmax, amax = 10.0, 50.0
A_v = vmax ** 2 / amax
w_v = amax / vmax
assert close(A_v, 2) and close(2 * math.pi / w_v, 2 * math.pi / 5)
add(T, "SHM equation and phase", "Intermediate", "numerical",
    "A particle executing simple harmonic motion has a maximum speed of 10 cm/s and a maximum acceleration of "
    "magnitude 50 cm/s². Its amplitude and period are respectively:",
    place("2 cm and 2π/5 s", ["5 cm and 2π/5 s", "2 cm and 5/(2π) s", "50 cm and 2π s"], "C"),
    "Maximum speed and maximum acceleration in SHM",
    "v_max = ωA and a_max = ω²A. Dividing gives ω, and then A follows.",
    ["ω = a_max/v_max = 50/10 = 5 rad/s", "A = v_max/ω = 10/5 = 2 cm", "T = 2π/ω = 2π/5 s ≈ 1.26 s"],
    why="5 cm divides a_max by v_max to get A; 5/(2π) s is the frequency ω/2π (in Hz) written as if it were the period; "
        "50 cm and 2π s take ω = 1 rad/s.",
    ncert="Class 11 Physics, 'Oscillations', velocity and acceleration in simple harmonic motion", seconds=60,
    recomputed=True)

n1_, n2_ = 4, 2
T_factor = (n1_ / n2_) ** 2
assert T_factor == 4
add(T, "Superposition and standing waves", "Intermediate", "numerical",
    "A string fixed at both ends vibrates with 4 loops (segments) between its ends when driven at a fixed "
    "frequency. Keeping the length, the string and the driving frequency the same, by what factor must the tension "
    "be changed so that it vibrates with 2 loops?",
    place("Increased 4 times", ["Increased 2 times", "Reduced to one-quarter", "Reduced to one-half"], "B"),
    "Normal modes of a stretched string",
    "With n loops, f = (n/2L)√(T/μ). For fixed f, L and μ, n√T is constant, so √T ∝ 1/n.",
    ["n√T = constant", "n: 4 → 2 → √T doubles → T becomes 4 times"],
    why="'Increased 2 times' forgets that f depends on √T; 'reduced' answers move the wrong way: fewer loops need "
        "longer wavelengths and so a larger wave speed.",
    ncert="Class 11 Physics, 'Waves', standing waves and normal modes (string fixed at both ends)", seconds=60,
    recomputed=True)

amp_x = 4 * math.sin(math.pi * 5 / 30)
assert close(amp_x, 2)
add(T, "Superposition and standing waves", "Intermediate", "numerical",
    "A stationary wave on a string is described by y = 4 sin(πx/30) cos(50πt), where x and y are in centimetres "
    "and t in seconds. The amplitude of oscillation of the particle of the string at x = 5 cm is:",
    place("2 cm", ["4 cm", "2√3 cm", "Zero"], "D"),
    "Amplitude in a stationary wave varies with position",
    "In a stationary wave y = [2a sin kx] cos ωt, each particle oscillates with amplitude 2a sin kx, which depends "
    "on its position.",
    ["Amplitude = 4 sin(π × 5/30) = 4 sin(π/6)", "= 4 × 0.5 = 2 cm"],
    why="4 cm is the amplitude at an antinode (x = 15 cm); 2√3 cm uses cos(π/6); zero would hold only at a node "
        "(x = 0, 30 cm, …).",
    ncert="Class 11 Physics, 'Waves', reflection of waves and standing waves", seconds=50, recomputed=True)

add(T, "Energy in SHM", "Intermediate", "direct",
    "For a block executing simple harmonic motion on a spring of force constant k with amplitude A, the graph of "
    "its kinetic energy K against its displacement x (from −A to +A) is:",
    place("A downward-opening parabola, K = ½k(A² − x²), greatest at x = 0 and zero at x = ±A",
          ["A straight line falling steadily from x = −A to x = +A",
           "An upward-opening parabola, zero at x = 0 and greatest at x = ±A",
           "A horizontal line, since the total energy is constant"], "C"),
    "Kinetic and potential energy in SHM",
    "The total energy E = ½kA² is constant and U = ½kx², so K = E − U = ½k(A² − x²): a parabola opening "
    "downward, symmetric about x = 0.",
    ["U = ½kx² (upward parabola)", "K = ½kA² − ½kx² (downward parabola)"],
    why="The upward parabola is the potential energy graph; the horizontal line is the total energy; K depends on "
        "x², so it cannot be a straight line.",
    ncert="Class 11 Physics, 'Oscillations', energy in simple harmonic motion", seconds=40)

add(T, "Progressive waves and wave speed", "Intermediate", "assertion_reason",
    AR_STEM.format(
        a="Transverse mechanical waves cannot travel through the bulk of a liquid.",
        r="A liquid cannot be compressed at all, so longitudinal waves cannot travel through it."),
    ar("C"),
    "Transverse and longitudinal waves in fluids",
    "Transverse waves need the medium to resist shearing; a fluid has no shear modulus, so transverse waves "
    "cannot travel through the bulk of a liquid (A true). Liquids do have a finite bulk modulus, and longitudinal "
    "(sound) waves travel through water at about 1500 m/s, so R is false.",
    ["No shear modulus in fluids → no transverse waves → A true", "Sound travels in water → R false"],
    why="R is false, so A and B are wrong; A is true, so D is wrong.",
    ncert="Class 11 Physics, 'Waves', transverse and longitudinal waves", seconds=50)

add(T, "Energy in SHM", "Intermediate", "statement_pair",
    SP_STEM.format(
        s1="For a block oscillating on a spring, doubling the amplitude (block and spring unchanged) doubles its "
           "maximum speed.",
        s2="For the same block and spring, doubling the amplitude makes the total energy of oscillation four "
           "times as large."),
    sp("A"),
    "Amplitude, maximum speed and energy in SHM",
    "ω = √(k/m) does not depend on the amplitude, so v_max = ωA doubles with A (Statement I true). The total "
    "energy is ½kA², proportional to A², so it becomes four times (Statement II true).",
    ["v_max = ωA ∝ A → I true", "E = ½kA² ∝ A² → II true"],
    why="Both statements follow from ω being independent of amplitude, so every option calling one of them false "
        "is wrong.",
    ncert="Class 11 Physics, 'Oscillations', energy in simple harmonic motion", seconds=40)

M_lo, m_up, k_lo, mu_lo = 3.0, 1.0, 400.0, 0.4
A_slip = mu_lo * g * (M_lo + m_up) / k_lo
assert close(A_slip, 0.04)
add(T, "Spring and pendulum oscillations", "Advanced", "numerical",
    "A block of mass 3 kg, attached to a horizontal spring of force constant 400 N/m, oscillates on a smooth "
    "floor. A small block of mass 1 kg rests on top of it; the coefficient of static friction between the two "
    "blocks is 0.4. Taking g = 10 m/s², the largest amplitude of oscillation for which the upper block does not "
    "slip is:",
    place("4 cm", ["1 cm", "3 cm", "16 cm"], "A"),
    "SHM of a combined system and the limiting friction",
    "Without slipping both blocks move together: ω² = k/(M + m) = 400/4 = 100 s⁻². The upper block's greatest "
    "acceleration, ω²A at the extremes, must be supplied by static friction, at most μg.",
    ["ω² = 100 s⁻²", "ω²A ≤ μg = 4 m/s²", "A ≤ 4/100 m = 4 cm"],
    why="1 cm uses μmg/k (friction force divided by k); 3 cm uses only the lower block's mass in ω; 16 cm "
        "multiplies by the total mass twice.",
    seconds=100, recomputed=True)

v_air = 340.0
f_lo, f_hi = 425.0, 595.0
df = f_hi - f_lo
f0_closed = df / 2
assert f_lo / f0_closed == 5 and f_hi / f0_closed == 7
assert close(v_air / (4 * f0_closed), 1.0)
assert (f_lo / df) % 1 != 0             # not consecutive integer multiples of an open-pipe fundamental
add(T, "Organ pipes and beats", "Advanced", "numerical",
    "A pipe resonates at two successive natural frequencies of 425 Hz and 595 Hz, with no natural frequency "
    "between them. Taking the speed of sound in air as 340 m/s and neglecting end corrections, the pipe is:",
    place("Closed at one end, and 1.0 m long", ["Open at both ends, and 1.0 m long",
                                                 "Closed at one end, and 0.5 m long",
                                                 "Open at both ends, and 2.0 m long"], "B"),
    "Identifying a pipe from its harmonic series",
    "For an open pipe, successive frequencies differ by f₀ and every frequency is an integer multiple of that "
    "difference. For a closed pipe only odd harmonics occur, so successive frequencies differ by 2f₀ and are odd "
    "multiples of f₀.",
    ["Difference = 170 Hz; 425/170 = 2.5, not an integer → not an open pipe",
     "Closed: 2f₀ = 170 → f₀ = 85 Hz; 425 = 5 × 85 and 595 = 7 × 85 ✓", "L = v/(4f₀) = 340/340 = 1.0 m"],
    why="'Open, 1.0 m' takes the difference as the fundamental of an open pipe, but 425 Hz is not a multiple of "
        "170 Hz; 'closed, 0.5 m' uses f₀ = 170 Hz; 'open, 2.0 m' uses f₀ = 85 Hz for an open pipe, which would also "
        "have a mode at 510 Hz between the two given frequencies.",
    ncert="Class 11 Physics, 'Waves', standing waves in pipes", seconds=110, recomputed=True)

m_v, k_v, A_v2 = 0.2, 20.0, 0.05
x0 = m_v * g / k_v
Tmax, Tmin = k_v * (x0 + A_v2), k_v * (x0 - A_v2)
assert close(x0, 0.1) and close(Tmax, 3) and close(Tmin, 1)
add(T, "Spring and pendulum oscillations", "Advanced", "numerical",
    "A block of mass 0.2 kg hangs from a light vertical spring of force constant 20 N/m and oscillates vertically "
    "about its equilibrium position with an amplitude of 5 cm. Taking g = 10 m/s², the greatest and the least "
    "values of the force exerted by the spring on the block are respectively:",
    place("3 N and 1 N", ["3 N and zero", "2.5 N and 1.5 N", "1 N and zero"], "D"),
    "Vertical spring oscillations about the stretched equilibrium",
    "At equilibrium the spring is already stretched by mg/k. The block oscillates about this point, so the "
    "extension ranges from (mg/k − A) to (mg/k + A); the spring force is k times the extension.",
    ["Equilibrium extension = 0.2 × 10/20 = 0.10 m", "Extension: 0.05 m to 0.15 m",
     "Spring force: 20 × 0.15 = 3 N (lowest point), 20 × 0.05 = 1 N (highest point)"],
    why="'3 N and zero' assumes the spring reaches its natural length at the top; '2.5 N and 1.5 N' uses half the "
        "amplitude; '1 N and zero' takes kA as the greatest force, ignoring the equilibrium stretch.",
    seconds=100, recomputed=True)

fac = {"A": math.sqrt(2), "B": 1 / 2, "C": 2.0, "D": math.sqrt(1 / 4) / 2}
assert close(fac["A"], math.sqrt(2)) and fac["B"] == 0.5 and fac["C"] == 2 and close(fac["D"], 0.25)
add(T, "Superposition and standing waves", "Advanced", "match_list",
    match_stem("Match List-I (change made, everything else unchanged) with List-II (factor by which the "
               "fundamental frequency changes). Neglect end corrections.",
               ["A stretched string: the tension is doubled",
                "A stretched string: its vibrating length is doubled",
                "A pipe closed at one end: its length is halved",
                "A stretched string: its vibrating length is doubled and its tension is made one-quarter"],
               ["2", "1/2", "√2", "1/4"]),
    match_options({"A": "III", "B": "II", "C": "I", "D": "IV"},
                  [{"A": "I", "B": "II", "C": "III", "D": "IV"}, {"A": "III", "B": "IV", "C": "I", "D": "II"},
                   {"A": "III", "B": "II", "C": "IV", "D": "I"}], "C"),
    "Fundamental frequencies of strings and pipes",
    "For a string f = (1/2L)√(T/μ); for a pipe closed at one end f = v/(4L).",
    ["A: f ∝ √T → √2 (III)", "B: f ∝ 1/L → 1/2 (II)", "C: f ∝ 1/L → 2 (I)",
     "D: (1/2) × √(1/4) = 1/4 (IV)"],
    why="The other codes treat f as proportional to T instead of √T, or forget to combine both changes in D.",
    ncert="Class 11 Physics, 'Waves', standing waves and normal modes", seconds=80, recomputed=True)

L_st, n_st, f_st = 1.5, 3, 300.0
lam_st = 2 * L_st / n_st
v_st = f_st * lam_st
truth = [close(lam_st, 1), close(v_st, 300), close(f_st / n_st, 100), n_st + 1 == 4, close(lam_st, 1.0) and False]
multi_key(truth, "abcd")
add(T, "Superposition and standing waves", "Advanced", "multi_statement",
    multi("A string 1.5 m long, fixed at both ends, vibrates in its third harmonic at a frequency of 300 Hz. Which "
          "of the following statements are correct?",
          ["The wavelength of the waves on the string is 1 m.", "The speed of transverse waves on the string is "
           "300 m/s.", "The fundamental frequency of the string is 100 Hz.",
           "Counting the two ends, there are 4 nodes on the string.",
           "The distance between two adjacent antinodes is 1 m."]),
    place("(a), (b), (c) and (d) only", ["(a), (b) and (e) only", "(b), (c), (d) and (e) only",
                                         "(a), (c) and (d) only"], "B"),
    "Normal modes of a string fixed at both ends",
    "In the nth harmonic, L = nλ/2, so there are n loops, n + 1 nodes (including the ends), and adjacent nodes "
    "or adjacent antinodes are λ/2 apart.",
    ["(a) λ = 2L/3 = 1 m, true", "(b) v = fλ = 300 m/s, true", "(c) f₁ = 300/3 = 100 Hz, true",
     "(d) 3 loops → 4 nodes, true", "(e) adjacent antinodes are λ/2 = 0.5 m apart → false"],
    why="Options with (e) confuse the spacing of adjacent antinodes (λ/2) with the wavelength.",
    ncert="Class 11 Physics, 'Waves', standing waves and normal modes", seconds=100, recomputed=True)

# =====================================================================================================================
# Electrostatics (B6 I8 A6)
# =====================================================================================================================
T = "Electrostatics"

assert close(2 / 0.5 ** 2, 8)
add(T, "Coulomb's law and superposition", "Basic", "numerical",
    "Two point charges in air exert an electrostatic force F on each other. If one of the charges is doubled and "
    "the distance between them is halved, the force becomes:",
    place("8F", ["4F", "F", "16F"], "A"),
    "Coulomb's law: dependence on charges and distance",
    "F = kq₁q₂/r². Doubling one charge doubles F; halving r multiplies F by 4.",
    ["F' = k(2q₁)q₂/(r/2)² = 8kq₁q₂/r² = 8F"],
    why="4F forgets either the doubled charge or one factor of 2 from r²; F makes the two changes cancel; 16F "
        "doubles both charges.",
    ncert="Class 12 Physics, 'Electric Charges and Fields', Coulomb's law", seconds=30, recomputed=True)

C_sph = 0.09 / k
assert close(C_sph, 1e-11)
add(T, "Capacitors and dielectrics", "Basic", "numerical",
    "Taking 1/(4πε₀) = 9 × 10⁹ N m² C⁻², the capacitance of an isolated conducting sphere of radius 9 cm in air "
    "is:",
    place("10 pF", ["100 pF", "1 nF", "10 μF"], "C"),
    "Capacitance of an isolated spherical conductor",
    "A charge Q on an isolated sphere of radius R gives it a potential V = Q/(4πε₀R), so C = Q/V = 4πε₀R.",
    ["C = R/(9 × 10⁹) = 0.09/(9 × 10⁹) F", "= 1 × 10⁻¹¹ F = 10 pF"],
    why="100 pF and 1 nF are power-of-ten slips (using R in cm); 10 μF is 10⁶ times too large: a farad is a "
        "very large unit.",
    ncert="Class 12 Physics, 'Electrostatic Potential and Capacitance', capacitors and capacitance", seconds=40,
    recomputed=True)

E_alpha = 2 * 200
assert E_alpha == 400
add(T, "Electric potential and energy", "Basic", "numerical",
    "An alpha particle (charge +2e) starts from rest and is accelerated through a potential difference of 200 V. "
    "Its kinetic energy is:",
    place("400 eV", ["200 eV", "100 eV", "800 eV"], "B"),
    "Work done by an electric field: qΔV",
    "The kinetic energy gained equals the loss of potential energy, qΔV. One electron volt is the energy gained "
    "by a charge e through 1 V, so a charge 2e through 200 V gains 400 eV.",
    ["K = qΔV = 2e × 200 V = 400 eV"],
    why="200 eV treats the alpha particle as singly charged; 100 eV divides by its charge; 800 eV doubles twice.",
    ncert="Class 12 Physics, 'Electrostatic Potential and Capacitance', potential energy of a charge in an "
          "external field", seconds=30, recomputed=True)

add(T, "Gauss's law", "Basic", "direct",
    "An electric dipole lies entirely inside a closed surface. The total electric flux through the surface is:",
    place("Zero", ["q/ε₀, where q is the magnitude of either charge", "2q/ε₀",
                   "Different for different shapes of the surface"], "D"),
    "Gauss's law: flux depends only on the net enclosed charge",
    "By Gauss's law the total flux through a closed surface is (net charge enclosed)/ε₀. A dipole has charges +q "
    "and −q, so the net enclosed charge is zero, whatever the shape of the surface.",
    ["q_enclosed = +q − q = 0", "Φ = 0/ε₀ = 0"],
    why="q/ε₀ and 2q/ε₀ add magnitudes instead of algebraic charges; the flux through a closed surface does not "
        "depend on its shape.",
    ncert="Class 12 Physics, 'Electric Charges and Fields', Gauss's law", seconds=25)

add(T, "Coulomb's law and superposition", "Basic", "direct",
    "A neutral metal sphere is given a positive charge by touching it with a positively charged rod. As a result, "
    "the mass of the sphere:",
    place("Decreases very slightly, because electrons leave it",
          ["Increases very slightly, because protons are added to it", "Stays exactly the same",
           "Increases very slightly, because positive charge has mass"], "C"),
    "Charging by transfer of electrons",
    "In charging a solid, only electrons (the mobile charges) are transferred. A body becomes positive by losing "
    "electrons, and each electron has a mass, so its mass decreases (by an extremely small amount).",
    ["Positive charge → electrons removed", "Each electron has mass 9.1 × 10⁻³¹ kg → mass decreases slightly"],
    why="Protons are bound in nuclei and are not transferred when solids are charged; the mass cannot stay "
        "exactly the same because electrons are removed.",
    ncert="Class 12 Physics, 'Electric Charges and Fields', electric charge; conductors and insulators",
    seconds=30)

add(T, "Capacitors and dielectrics", "Basic", "statement_pair",
    SP_STEM.format(
        s1="The farad, the SI unit of capacitance, is a very large unit; practical capacitors are of the order of "
           "microfarads or picofarads.",
        s2="The capacitance of a parallel plate capacitor is inversely proportional to the area of its plates."),
    sp("C"),
    "Unit of capacitance; capacitance of a parallel plate capacitor",
    "A capacitance of 1 F between plates 1 cm apart in air would need plates about 10⁹ m² in area, so the farad "
    "is a very large unit (Statement I true). C = ε₀A/d is directly proportional to the area (Statement II "
    "false).",
    ["1 F is enormous → I true", "C = ε₀A/d ∝ A → II false"],
    why="Statement II inverts the dependence on area (C is inversely proportional to the separation d), so "
        "options calling it true are wrong.",
    ncert="Class 12 Physics, 'Electrostatic Potential and Capacitance', capacitors; the parallel plate "
          "capacitor", seconds=35)

x_z = 2.0
assert close(4 / x_z ** 2, 1 / (x_z - 1) ** 2)
add(T, "Electric field and dipole", "Intermediate", "numerical",
    "Point charges +4q and −q are fixed on the x-axis at x = 0 and x = 1 m respectively. Apart from points at "
    "infinity, the electric field is zero at:",
    place("x = 2 m", ["x = 2/3 m", "x = 4/3 m", "x = −2 m"], "C"),
    "Superposition of fields of unlike charges",
    "Between unlike charges both fields point the same way (towards −q), so they cannot cancel there. The zero "
    "must lie outside, on the side of the smaller charge, where the fields are opposite: 4kq/x² = kq/(x − 1)².",
    ["2(x − 1) = x → x = 2 m", "Check: 4/4 = 1/1 ✓"],
    why="x = 2/3 m is the answer for like charges, between them; x = 4/3 m does not satisfy 4/x² = 1/(x − 1)²; "
        "x = −2 m lies beyond the larger charge, where its field always dominates.",
    ncert="Class 12 Physics, 'Electric Charges and Fields', electric field due to a system of charges",
    seconds=70, recomputed=True)

q1v, q2v, rx, ry = 2e-6, 1e-6, 3.0, 4.0
r2v = rx ** 2 + ry ** 2
Fv = k * q1v * q2v / r2v
Fx, Fy = Fv * rx / 5, Fv * ry / 5
assert close(Fv, 7.2e-4) and close(Fx, 4.32e-4) and close(Fy, 5.76e-4)
add(T, "Coulomb's law and superposition", "Intermediate", "numerical",
    "A point charge of 2 μC is fixed at the origin and a point charge of 1 μC is at the point (3 m, 4 m) in the "
    "x–y plane, in air. Taking 1/(4πε₀) = 9 × 10⁹ N m² C⁻², the force on the 1 μC charge is:",
    place("(4.32î + 5.76ĵ) × 10⁻⁴ N", ["(5.76î + 4.32ĵ) × 10⁻⁴ N", "(−4.32î − 5.76ĵ) × 10⁻⁴ N",
                                        "(2.16î + 2.88ĵ) × 10⁻³ N"], "A"),
    "Coulomb's law in vector form",
    "F₂₁ = k q₁q₂ r̂₂₁/r², where r₂₁ is the vector from the 2 μC charge to the 1 μC charge. Like charges repel, "
    "so the force points away from the origin.",
    ["r = √(9 + 16) = 5 m, r̂ = (0.6, 0.8)", "|F| = 9 × 10⁹ × 2 × 10⁻¹² / 25 = 7.2 × 10⁻⁴ N",
     "F = 7.2 × 10⁻⁴ (0.6î + 0.8ĵ) = (4.32î + 5.76ĵ) × 10⁻⁴ N"],
    why="Swapping the components mixes up the direction cosines; the negative vector treats the charges as "
        "attracting; (2.16î + 2.88ĵ) × 10⁻³ N divides by r instead of r².",
    ncert="Class 12 Physics, 'Electric Charges and Fields', Coulomb's law (vector form)", seconds=70,
    recomputed=True)

t_sl, K_sl = 4.0, 4.0
extra = t_sl * (1 - 1 / K_sl)
assert close(extra, 3.0)
add(T, "Capacitors and dielectrics", "Intermediate", "numerical",
    "A slab of dielectric constant 4 and thickness 4 mm, of the same area as the plates, is placed between the "
    "plates of an air-filled parallel plate capacitor, parallel to them. By how much must the separation of the "
    "plates be increased so that the capacitance returns to its original value?",
    place("3 mm", ["4 mm", "1 mm", "16 mm"], "D"),
    "Capacitance with a dielectric slab of partial thickness",
    "With a slab of thickness t and dielectric constant K in a gap d, C = ε₀A/(d − t + t/K) = ε₀A/(d − t(1 − "
    "1/K)). The slab acts like a reduction of the air gap by t(1 − 1/K), which must be made up.",
    ["Effective reduction = t(1 − 1/K) = 4 × (1 − 1/4) = 3 mm", "Increase the separation by 3 mm"],
    why="4 mm treats the slab as a conductor; 1 mm is t/K; 16 mm multiplies t by K.",
    ncert="Class 12 Physics, 'Electrostatic Potential and Capacitance', effect of dielectric on capacitance",
    seconds=70, recomputed=True)

add(T, "Capacitors and dielectrics", "Intermediate", "match_list",
    match_stem("For an air-filled parallel plate capacitor of plate area A and separation d, carrying charge Q "
               "(surface charge density σ) with field E between the plates, match List-I (quantity) with List-II "
               "(expression). C denotes the capacitance.",
               ["Energy stored per unit volume between the plates", "Capacitance",
                "Energy stored in the capacitor", "Electric field between the plates"],
               ["ε₀A/d", "σ/ε₀", "½ε₀E²", "Q²/(2C)"]),
    match_options({"A": "III", "B": "I", "C": "IV", "D": "II"},
                  [{"A": "IV", "B": "I", "C": "III", "D": "II"}, {"A": "III", "B": "II", "C": "IV", "D": "I"},
                   {"A": "III", "B": "I", "C": "II", "D": "IV"}], "B"),
    "Parallel plate capacitor relations",
    "Between the plates E = σ/ε₀ and C = ε₀A/d. The stored energy is Q²/2C, and dividing it by the volume Ad "
    "gives the energy density ½ε₀E².",
    ["A → ½ε₀E² (III)", "B → ε₀A/d (I)", "C → Q²/2C (IV)", "D → σ/ε₀ (II)"],
    why="The other codes swap the total energy with the energy density, or the field with the capacitance.",
    ncert="Class 12 Physics, 'Electrostatic Potential and Capacitance', parallel plate capacitor; energy stored "
          "in a capacitor", seconds=50)

add(T, "Capacitors and dielectrics", "Intermediate", "assertion_reason",
    AR_STEM.format(
        a="A dielectric made of polar molecules has no net dipole moment when no external electric field acts "
          "on it.",
        r="In the absence of an external field, thermal agitation keeps the permanent dipole moments of the "
          "polar molecules randomly oriented, so they cancel on average."),
    ar("A"),
    "Polarisation of polar dielectrics",
    "Each polar molecule has a permanent dipole moment, but without an external field their directions are "
    "random because of thermal agitation, and the total dipole moment is zero. An external field tends to align "
    "them, producing a net polarisation. R is the reason for A.",
    ["Random orientations → Σp = 0 → A true", "R gives the cause (thermal agitation) → A"],
    why="R explains why the permanent dipoles cancel, so B is wrong; both statements are true, so C and D are "
        "wrong.",
    ncert="Class 12 Physics, 'Electrostatic Potential and Capacitance', dielectrics and polarisation", seconds=45)

add(T, "Gauss's law", "Intermediate", "statement_pair",
    SP_STEM.format(
        s1="The electric potential changes abruptly (is discontinuous) as one crosses the surface of a uniformly "
           "charged thin spherical shell.",
        s2="The electric field due to a uniformly charged thin spherical shell is zero at every point inside "
           "it."),
    sp("D"),
    "Field and potential of a charged spherical shell",
    "By Gauss's law a Gaussian sphere inside the shell encloses no charge, and by symmetry the field there is zero "
    "(Statement II true). Hence the potential inside is constant and equal to its value at the surface, kQ/R; it "
    "is continuous across the shell. It is the field that jumps, from 0 to kQ/R² (Statement I false).",
    ["E_inside = 0 → II true", "V_inside = kQ/R = V_surface → V continuous → I false"],
    why="Statement I confuses the jump in the field with the potential, so options calling it true are wrong.",
    ncert="Class 12 Physics, 'Electric Charges and Fields', field due to a uniformly charged thin spherical shell",
    seconds=50)

m_pp, q_pp, r_pp = 1e-3, 1e-6, 0.1
U_pp = k * q_pp ** 2 / r_pp
v_pp = math.sqrt(2 * (U_pp / 2) / m_pp)
assert close(U_pp, 0.09) and close(v_pp, 3 * math.sqrt(10))
add(T, "Electric potential and energy", "Intermediate", "numerical",
    "Two small identical particles, each of mass 1 g and charge 1 μC, are held at rest 10 cm apart in free space "
    "and then released. Taking 1/(4πε₀) = 9 × 10⁹ N m² C⁻² and neglecting gravity, the speed of each particle "
    "when they are very far apart is:",
    place("3√10 m/s", ["6√5 m/s", "3√5 m/s", "30 m/s"], "D"),
    "Conservation of energy and momentum for two charges",
    "The initial potential energy kq²/r becomes kinetic energy. Momentum conservation (starting from zero) makes "
    "the two equal masses move with equal speeds, so each gets half the energy.",
    ["U = 9 × 10⁹ × 10⁻¹²/0.1 = 0.09 J", "Each: ½mv² = 0.045 J", "v² = 0.09/10⁻³ = 90 → v = 3√10 ≈ 9.5 m/s"],
    why="6√5 m/s gives all the energy to one particle; 3√5 m/s halves the energy twice; 30 m/s is a slip in "
        "converting the mass.",
    ncert="Class 12 Physics, 'Electrostatic Potential and Capacitance', potential energy of a system of charges",
    seconds=80, recomputed=True)

multi_key([True, True, True, False, True], "abce")
add(T, "Gauss's law", "Intermediate", "multi_statement",
    multi("A point charge q is placed at the centre of an imaginary cube in vacuum. Which of the following "
          "statements are correct?",
          ["The total electric flux through the cube is q/ε₀.",
           "The flux through each face of the cube is q/(6ε₀).",
           "If the charge is moved to another point inside the cube, the total flux through the cube is "
           "unchanged.",
           "If the charge is moved to another point inside the cube, the flux through each face is still "
           "q/(6ε₀).",
           "If the charge is moved to a point just outside the cube, the total flux through the cube becomes "
           "zero."]),
    place("(a), (b), (c) and (e) only", ["(a), (b) and (d) only", "(a), (c), (d) and (e) only",
                                         "(b), (c) and (e) only"], "A"),
    "Gauss's law and symmetry",
    "Gauss's law fixes only the total flux through a closed surface, q_enclosed/ε₀. The equal share among the six "
    "faces follows from symmetry, which is lost when the charge is off-centre.",
    ["(a) true: Φ = q/ε₀", "(b) true: six equivalent faces at the centre",
     "(c) true: enclosed charge unchanged", "(d) false: faces nearer the charge get more flux",
     "(e) true: no enclosed charge"],
    why="Options with (d) take the symmetric share as a consequence of Gauss's law itself; omitting (e) forgets "
        "that an outside charge sends equal flux in and out.",
    ncert="Class 12 Physics, 'Electric Charges and Fields', Gauss's law", seconds=80)

U_sq = -4 + 2 / math.sqrt(2)                     # in units of k q^2 / a
assert close(U_sq, math.sqrt(2) - 4)
add(T, "Electric potential and energy", "Advanced", "numerical",
    "Four point charges +q, −q, +q and −q are placed in this order at the corners of a square of side a, so that "
    "each charge has charges of the opposite sign at the two adjacent corners. With k = 1/(4πε₀) and the potential "
    "energy zero at infinite separation, the electrostatic potential energy of the system is:",
    place("(√2 − 4) kq²/a", ["(4 − √2) kq²/a", "−4 kq²/a", "−(4 + √2) kq²/a"], "C"),
    "Potential energy of a system of point charges",
    "Add kqᵢqⱼ/rᵢⱼ over all six pairs: four sides (unlike charges, distance a) and two diagonals (like charges, "
    "distance a√2).",
    ["Sides: 4 × (−kq²/a) = −4kq²/a", "Diagonals: 2 × (+kq²/(a√2)) = +√2 kq²/a", "U = (√2 − 4) kq²/a"],
    why="(4 − √2) has the overall sign reversed; −4kq²/a leaves out the diagonal pairs; −(4 + √2) gives the "
        "like-charge diagonal pairs the wrong sign.",
    ncert="Class 12 Physics, 'Electrostatic Potential and Capacitance', potential energy of a system of charges",
    seconds=100, recomputed=True)

b_f, a_cube = 200.0, 0.1
flux_c = b_f * a_cube * a_cube ** 2
q_c = EPS0 * flux_c
assert close(flux_c, 0.2) and close(q_c, 1.77e-12)
add(T, "Gauss's law", "Advanced", "numerical",
    "In a certain region the electric field is E = (200x) î N/C, where x is in metres. A cube of side 0.1 m has "
    "its edges along the axes, with one face in the plane x = 0 and the opposite face in the plane x = 0.1 m. "
    "Taking ε₀ = 8.85 × 10⁻¹² C² N⁻¹ m⁻², the net charge inside the cube is:",
    place("1.77 × 10⁻¹² C", ["Zero", "1.77 × 10⁻¹³ C", "3.54 × 10⁻¹² C"], "A"),
    "Gauss's law with a non-uniform field",
    "The field is along x, so only the two faces perpendicular to x have flux. At x = 0 the field is zero; at "
    "x = 0.1 m it is 20 N/C, pointing outward. Gauss's law then gives the enclosed charge.",
    ["Φ = E(0.1) × a² − E(0) × a² = 20 × 0.01 − 0 = 0.2 N m² C⁻¹", "q = ε₀Φ = 8.85 × 10⁻¹² × 0.2 = 1.77 × 10⁻¹² C"],
    why="Zero would hold only for a uniform field; 1.77 × 10⁻¹³ C uses E = 2 N/C at the far face; 3.54 × 10⁻¹² C "
        "counts the far face twice.",
    ncert="Class 12 Physics, 'Electric Charges and Fields', electric flux; Gauss's law", seconds=100,
    recomputed=True)

C1s, C2s, Vb, Kd = 6.0, 6.0, 12.0, 2.0
Q_new = 1 / (1 / C1s + 1 / (Kd * C2s)) * Vb
V1_new = Q_new / C1s
assert close(Q_new, 48) and close(V1_new, 8)
add(T, "Capacitors and dielectrics", "Advanced", "numerical",
    "Two identical 6 μF air-filled capacitors are connected in series across a 12 V battery. With the battery "
    "still connected, a dielectric slab of dielectric constant 2 is inserted to fill the second capacitor "
    "completely. The potential difference across the first capacitor now becomes:",
    place("8 V", ["6 V", "4 V", "12 V"], "D"),
    "Series capacitors: effect of a dielectric with the battery connected",
    "The second capacitor becomes 12 μF. The series combination is now 6 × 12/(6 + 12) = 4 μF, so the common "
    "charge is 4 × 12 = 48 μC. The first capacitor's voltage is Q/C₁.",
    ["C₂' = 2 × 6 = 12 μF", "C_eq = 4 μF → Q = 48 μC", "V₁ = 48/6 = 8 V (and V₂ = 4 V)"],
    why="6 V is the value before the slab is inserted; 4 V is the new voltage across the second capacitor; 12 V "
        "puts the whole battery voltage across one capacitor.",
    ncert="Class 12 Physics, 'Electrostatic Potential and Capacitance', combination of capacitors; effect of "
          "dielectric", seconds=90, recomputed=True)

add(T, "Gauss's law", "Advanced", "assertion_reason",
    AR_STEM.format(
        a="Gauss's law alone provides a simple way to calculate the electric field at any point near a uniformly "
          "charged straight rod of finite length.",
        r="Gauss's law holds for every closed surface, whatever its shape and size."),
    ar("D"),
    "Using Gauss's law to find fields",
    "Gauss's law is always true (R true), but it gives only the total flux. To extract the field from it one "
    "needs a Gaussian surface on which E is constant in magnitude and normal to the surface, which requires high "
    "symmetry (infinite line, infinite plane, sphere). A finite rod lacks this symmetry near its ends, so A is "
    "false.",
    ["Gauss's law: Φ = q/ε₀ for any closed surface → R true", "No symmetric Gaussian surface for a finite rod → A "
     "false"],
    why="A is false, so the options A, B and C (which all call A true) are wrong.",
    ncert="Class 12 Physics, 'Electric Charges and Fields', applications of Gauss's law", seconds=60)

add(T, "Capacitors and dielectrics", "Advanced", "statement_pair",
    SP_STEM.format(
        s1="The energy of a charged capacitor may be regarded as stored in the electric field between its plates, "
           "with energy density ½ε₀E² in air.",
        s2="If the plates of an isolated charged parallel plate capacitor (charge fixed) are moved closer, to half "
           "their separation, the energy density between the plates is halved."),
    sp("C"),
    "Energy density of an electric field",
    "Statement I is the standard result u = ½ε₀E². For an isolated capacitor Q and hence σ are fixed, so "
    "E = σ/ε₀ does not change when the plates are moved; the energy density is unchanged (Statement II false). "
    "The total energy halves only because the volume of the field halves.",
    ["u = ½ε₀E² → I true", "Q fixed → E = σ/ε₀ fixed → u unchanged → II false"],
    why="Statement II confuses the total energy (which halves) with the energy density (which does not).",
    ncert="Class 12 Physics, 'Electrostatic Potential and Capacitance', energy stored in a capacitor", seconds=60)

Ex_, Ey_ = -4.0, -3.0
truth = [math.hypot(Ex_, Ey_) == 5, True, True, False, True]
W_field = 2e-6 * (0 - 4)                     # q (V_initial - V_final)
assert close(W_field, -8e-6)
multi_key(truth, "abce")
add(T, "Electric potential and energy", "Advanced", "multi_statement",
    multi("In a region of space the electric potential is V = 4x + 3y, where V is in volts and x, y in metres; it "
          "does not depend on z. Which of the following statements are correct?",
          ["The magnitude of the electric field is 5 V/m.",
           "The electric field is directed along −(4î + 3ĵ)/5.",
           "The equipotential surfaces are planes 4x + 3y = constant, perpendicular to the x–y plane.",
           "When a charge of +2 μC moves from (0, 0) to (1 m, 0), the work done on it by the electric field is "
           "+8 μJ.",
           "The electric field is the same at every point of the region."]),
    place("(a), (b), (c) and (e) only", ["(a), (b), (d) and (e) only", "(b), (c) and (d) only",
                                         "(a), (c) and (e) only"], "B"),
    "Electric field as the negative gradient of potential",
    "E = −(∂V/∂x) î − (∂V/∂y) ĵ = −4î − 3ĵ V/m, a uniform field. Equipotentials are perpendicular to E. The work "
    "done by the field on a charge is q(V_initial − V_final).",
    ["(a) |E| = √(16 + 9) = 5 V/m, true", "(b) E = −(4î + 3ĵ) → direction −(4î + 3ĵ)/5, true",
     "(c) V constant on 4x + 3y = c, true", "(d) W = 2 μC × (0 − 4 V) = −8 μJ → false",
     "(e) E is constant → uniform, true"],
    why="(d) has the sign reversed: a positive charge moving to higher potential has negative work done on it "
        "by the field.",
    ncert="Class 12 Physics, 'Electrostatic Potential and Capacitance', relation between field and potential; "
          "equipotential surfaces", seconds=110, recomputed=True)

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
    doc = {"schema_version": "1.0", "batch_id": "BATCH_008", "created_at": TODAY,
           "notes": "BATCH_008 package PHY_008_p1: 125 original Physics questions (Physics and Measurement through "
                    "Electrostatics). Every numerical answer is re-derived in tools/batch_008/PHY_008_p1.py.",
           "stimuli": [], "questions": QUESTIONS}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {OUT}: {n} questions, {dict(Counter(x['difficulty'] for x in QUESTIONS))}")
    print(f"keys {dict(sorted(keys.items()))}")
    print(f"formats {dict(fmts)}")
