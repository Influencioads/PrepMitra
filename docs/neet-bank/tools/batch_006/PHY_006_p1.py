"""Writes batches/parts/BATCH_006_PHY_p1.json: package PHY_006_p1 of BATCH_006 (131 Physics questions).

Topics: Physics and Measurement, Kinematics, Laws of Motion, Work Energy and Power, Rotational Motion, Gravitation,
Properties of Solids and Liquids, Thermodynamics, Kinetic Theory of Gases, Oscillations and Waves, Electrostatics.
IDs NEET_PHY_001251 .. NEET_PHY_001381, in the order the questions are listed below.

Every computable answer is re-derived with an assert before the file is written, and so is the plan quota. If any
assert fails, nothing is written. Each question's answer position is chosen by hand and fixed.

    python tools/batch_006/PHY_006_p1.py        (run from docs/neet-bank)
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
OUT = ROOT / "batches" / "parts" / "BATCH_006_PHY_p1.json"
PLAN = ROOT / "batches" / "plans" / "BATCH_006_plan.json"
PACKAGE = "PHY_006_p1"
TODAY = "2026-11-16"
LETTERS = "ABCD"
PHY = "Physics"
RECOMPUTED = ("script:recompute", "ai:author-solve", "ai:self-recheck")
AUTHORED = ("ai:author-solve", "ai:self-recheck")
FIRST_ID = 1251

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
# Physics and Measurement (B2 I3 A2)
# =====================================================================================================================
T = "Physics and Measurement"

G_SI = 6.67e-11
G_cgs = G_SI * 1e5 * (1e2) ** 2 / (1e3) ** 2      # N → dyn, m² → cm², kg⁻² → g⁻²
assert close(G_cgs, 6.67e-8)
assert close(G_SI * 1e5 * 1e2 / 1e6, 6.67e-10) and close(G_SI * 1e4 / 1e6, 6.67e-13)
assert close(G_SI * 1e5 * 1e4 * 1e6, 6.67e4)
add(T, "Units and SI system", "Basic", "numerical",
    "The universal gravitational constant is G = 6.67 × 10⁻¹¹ N m² kg⁻². Given 1 N = 10⁵ dyne, its value in CGS "
    "units (dyne cm² g⁻²) is:",
    place("6.67 × 10⁻⁸", ["6.67 × 10⁻¹⁰", "6.67 × 10⁻¹³", "6.67 × 10⁴"], "B"),
    "Conversion of a derived unit between systems",
    "Replace each SI unit by its CGS equivalent: 1 N = 10⁵ dyne, 1 m² = 10⁴ cm² and 1 kg⁻² = (10³ g)⁻² = 10⁻⁶ g⁻².",
    ["G = 6.67 × 10⁻¹¹ × 10⁵ × 10⁴ × 10⁻⁶ dyne cm² g⁻²", "= 6.67 × 10⁻⁸ dyne cm² g⁻²"],
    why="10⁻¹⁰ converts m² as if 1 m² = 10² cm². 10⁻¹³ leaves the newton unconverted. 10⁴ multiplies by 10⁶ for "
        "kg⁻² instead of dividing.",
    ncert="Class 11 Physics, 'Units and Measurement', the international system of units", seconds=45,
    recomputed=True)

D_INT = dmul(dims(1, 2, -3), dinv(dims(0, 2, 0)))           # power / area
assert D_INT == (1, 0, -3)
assert dims(1, 0, -2) != D_INT and dims(1, 2, -3) != D_INT and dims(1, -1, -2) != D_INT
add(T, "Dimensional analysis", "Basic", "direct",
    "Which of the following physical quantities has the dimensional formula [M L⁰ T⁻³]?",
    place("Intensity of a wave (power transmitted per unit area)",
          ["Surface tension", "Power", "Pressure"], "C"),
    "Dimensional formula of a derived quantity",
    "Power is energy per unit time, [M L² T⁻³]. Dividing by an area [L²] removes the length dimension, leaving "
    "[M T⁻³].",
    ["Power = [M L² T⁻³]", "Intensity = power/area = [M L² T⁻³]/[L²] = [M L⁰ T⁻³]"],
    why="Surface tension (force per length) is [M T⁻²]; power is [M L² T⁻³]; pressure is [M L⁻¹ T⁻²].",
    ncert="Class 11 Physics, 'Units and Measurement', dimensional formulae", seconds=35)

F_u, E_u, v_u = 10, 100, 5
L_u = E_u / F_u
T_u = L_u / v_u
M_u = E_u / v_u ** 2
assert L_u == 10 and T_u == 2 and M_u == 4 and v_u / L_u == 0.5 and E_u / F_u * v_u == 50
add(T, "Units and SI system", "Intermediate", "numerical",
    "In a new system of units, the unit of force is 10 N, the unit of energy is 100 J and the unit of velocity is "
    "5 m s⁻¹. The unit of time in this system is equal to:",
    place("2 s", ["0.5 s", "4 s", "50 s"], "D"),
    "Building units of a new system from chosen derived units",
    "Energy = force × length, so the unit of length is (100 J)/(10 N). Time = length/velocity then gives the unit "
    "of time.",
    ["Unit of length = 100 J / 10 N = 10 m", "Unit of time = 10 m / (5 m s⁻¹) = 2 s"],
    why="0.5 s inverts the last step (velocity/length). 4 s is the numerical value of the unit of mass "
        "(E/v² = 4 kg), not of time. 50 s multiplies the length by the velocity.",
    ncert="Class 11 Physics, 'Units and Measurement', dimensions and dimensional analysis", seconds=60,
    recomputed=True)

add(T, "Errors in measurement", "Intermediate", "match_list",
    match_stem("Match List-I (source of error in a measurement) with List-II (type of error, as classified in NCERT).",
               ["The zero mark of the vernier scale does not coincide with the zero of the main scale when the jaws "
                "of a vernier calliper are closed",
                "An observer, out of habit, always reads a needle with the head slightly to one side, introducing "
                "parallax",
                "Body temperature is measured by placing a thermometer under the armpit, which always gives a value "
                "lower than the actual body temperature",
                "Unpredictable fluctuations in the readings caused by unpredictable changes in the supply voltage"],
               ["Random error", "Instrumental error", "Personal error",
                "Error due to imperfection in experimental technique or procedure"]),
    match_options({"A": "II", "B": "III", "C": "IV", "D": "I"},
                  [{"A": "IV", "B": "III", "C": "II", "D": "I"}, {"A": "II", "B": "IV", "C": "III", "D": "I"},
                   {"A": "II", "B": "III", "C": "I", "D": "IV"}], "A"),
    "Systematic and random errors",
    "NCERT divides systematic errors into instrumental errors (imperfect design or calibration, such as a zero "
    "error), errors from imperfect experimental technique or procedure (the armpit thermometer always reads low) and "
    "personal errors (an observer's bias or habit, such as a parallax habit). Errors that occur irregularly and are "
    "random in size and sign, like those from supply-voltage fluctuations, are random errors.",
    ["Zero error → instrumental (II)", "Parallax habit → personal (III)", "Armpit thermometer → technique (IV)",
     "Unpredictable fluctuations → random (I)"],
    why="The other codes confuse the armpit thermometer (a faulty procedure) with an instrument fault or a personal "
        "habit, or call a systematic error random.",
    ncert="Class 11 Physics, 'Units and Measurement', errors in measurement (systematic and random errors)",
    seconds=60)

D_b = dinv(dims(0, 0, 1))
D_c = dinv(dims(0, 1, 0))
assert dmul(D_b, dinv(D_c)) == (0, 1, -1)
add(T, "Dimensional analysis", "Intermediate", "assertion_reason",
    AR_STEM.format(
        a="In the relation y = a sin(bt − cx), where y and x are distances and t is time, the ratio b/c has the "
          "dimensions of speed.",
        r="The argument of a trigonometric function must be dimensionless, so bt and cx must each be "
          "dimensionless."),
    ar("A"),
    "Dimensionless arguments of functions",
    "An angle is a pure number, so bt and cx must each be dimensionless. That forces [b] = [T⁻¹] and [c] = [L⁻¹], "
    "and b/c = [L T⁻¹], the dimensions of speed. The reason is exactly what fixes the dimensions in A.",
    ["bt dimensionless → [b] = T⁻¹", "cx dimensionless → [c] = L⁻¹", "[b/c] = L T⁻¹ (speed) → A true, R explains"],
    why="Both statements are true and R is the very rule used to find [b] and [c], so options B, C and D fail.",
    ncert="Class 11 Physics, 'Units and Measurement', dimensional analysis and its applications", seconds=50)

m_, dm_ = 200.0, 2.0
T1, T2, dT_ = 20.0, 45.0, 0.5
dTh = T2 - T1
rel_c = dm_ / m_ + (2 * dT_) / dTh
assert close(rel_c * 100, 5.0)
assert close((dm_ / m_ + dT_ / dTh) * 100, 3.0)
assert round((dm_ / m_ + dT_ / T1 + dT_ / T2) * 100, 1) == 4.6
add(T, "Errors in measurement", "Advanced", "numerical",
    "The specific heat capacity of a liquid is found from c = Q/(mΔθ), where the heat Q supplied by a calibrated "
    "heater may be taken as exact. The mass of the liquid is (200 ± 2) g, and its initial and final temperatures "
    "are (20.0 ± 0.5) °C and (45.0 ± 0.5) °C. The maximum percentage error in c is:",
    place("5%", ["3%", "1%", "about 4.6%"], "C"),
    "Error of a difference combined with a quotient",
    "The rise in temperature is a difference, so its absolute errors add. Its relative error then adds to the "
    "relative error of the mass, because c is a quotient.",
    ["Δθ = 45.0 − 20.0 = 25.0 °C, with absolute error 0.5 + 0.5 = 1.0 °C → 4%",
     "Relative error in m = 2/200 = 1%", "Maximum error in c = 1% + 4% = 5%"],
    why="3% takes the error of Δθ as 0.5 °C instead of 1.0 °C. 1% subtracts the two temperature errors (0.5 − 0.5) "
        "and keeps only the mass error. About 4.6% uses the relative errors of the two temperature readings instead "
        "of the error of their difference.",
    ncert="Class 11 Physics, 'Units and Measurement', combination of errors", seconds=90, recomputed=True)

D_h, D_G, D_c3 = dims(1, 2, -1), dims(-1, 3, -2), dims(0, 1, -1)


def power_dims(a, b, c):
    return tuple(a * x + b * y + c * z for x, y, z in zip(D_h, D_G, D_c3))


assert power_dims(F(1, 2), F(1, 2), F(-5, 2)) == (0, 0, 1)          # √(hG/c⁵): time
assert power_dims(F(1, 2), F(1, 2), F(-3, 2)) == (0, 1, 0)          # √(hG/c³): length
assert power_dims(F(1, 2), F(-1, 2), F(1, 2)) == (1, 0, 0)          # √(hc/G): mass
assert power_dims(F(1, 2), F(-1, 2), F(5, 2)) == (1, 2, -2)         # √(hc⁵/G): energy
add(T, "Dimensional analysis", "Advanced", "direct",
    "A quantity having the dimensions of time is to be formed from Planck's constant h [M L² T⁻¹], the universal "
    "gravitational constant G [M⁻¹ L³ T⁻²] and the speed of light c [L T⁻¹], without any other constant. Ignoring "
    "dimensionless factors, this quantity is:",
    place("√(hG/c⁵)", ["√(hc/G)", "√(hG/c³)", "√(hc⁵/G)"], "D"),
    "Constructing a quantity by equating dimensions",
    "Write t = h^a G^b c^d and equate the powers of M, L and T on both sides. The three equations fix a, b and d "
    "uniquely.",
    ["M: a − b = 0", "L: 2a + 3b + d = 0", "T: −a − 2b − d = 1",
     "a = b → d = −5a; then −3a + 5a = 1 → a = b = 1/2, d = −5/2", "t ∝ √(hG/c⁵)"],
    why="√(hc/G) has the dimensions of mass, √(hG/c³) of length and √(hc⁵/G) of energy.",
    ncert="Class 11 Physics, 'Units and Measurement', deducing relations by the method of dimensions",
    seconds=120, recomputed=True)


# =====================================================================================================================
# Kinematics (B4 I5 A4)
# =====================================================================================================================
T = "Kinematics"

g = 10
v2 = 15 - g * 2
assert v2 == -5 and 15 + g * 2 == 35
add(T, "Motion in a straight line", "Basic", "numerical",
    "A stone is thrown vertically upward with a speed of 15 m/s. Taking g = 10 m/s² and neglecting air "
    "resistance, its velocity 2 s after the throw is:",
    place("5 m/s, directed downward", ["5 m/s, directed upward", "35 m/s, directed downward",
                                       "zero, because the stone is at its highest point"], "A"),
    "Velocity under uniform acceleration with sign convention",
    "Take upward as positive. The acceleration is −g throughout, so v = u − gt. A negative result means the stone "
    "has passed its highest point (at 1.5 s) and is falling.",
    ["v = 15 − 10 × 2 = −5 m/s", "Negative sign → 5 m/s downward"],
    why="'Upward' drops the sign of the answer. 35 m/s adds gt to u as if g pointed upward. The highest point is "
        "reached at u/g = 1.5 s, not at 2 s.",
    ncert="Class 11 Physics, 'Motion in a Straight Line', kinematic equations for uniformly accelerated motion",
    seconds=35, recomputed=True)

a = 2
dist = [0.5 * a * n ** 2 - 0.5 * a * (n - 1) ** 2 for n in range(1, 5)]
assert [d / dist[0] for d in dist] == [1, 3, 5, 7]
add(T, "Motion in a straight line", "Basic", "direct",
    "A body starts from rest and moves along a straight line with uniform acceleration. The distances it covers in "
    "successive equal intervals of time (the 1st, 2nd, 3rd and 4th interval) are in the ratio:",
    place("1 : 3 : 5 : 7", ["1 : 2 : 3 : 4", "1 : 4 : 9 : 16", "1 : √2 : √3 : 2"], "B"),
    "Galileo's law of odd numbers",
    "From rest, the distance covered up to the end of the nth interval τ is ½a(nτ)², proportional to n². The "
    "distance in the nth interval alone is proportional to n² − (n − 1)² = 2n − 1, the odd numbers.",
    ["Total distances ∝ 1, 4, 9, 16", "Successive differences ∝ 1, 3, 5, 7"],
    why="1 : 4 : 9 : 16 are the total distances from the start, not the distances in each interval. 1 : 2 : 3 : 4 "
        "would be the velocities at the ends of the intervals. 1 : √2 : √3 : 2 are the times to cover equal "
        "distances from rest, measured from the start.",
    ncert="Class 11 Physics, 'Motion in a Straight Line', kinematic equations (Galileo's law of odd numbers)",
    seconds=35, recomputed=True)

Ax, Ay, Bx, By = 2, 3, 1, 1
assert math.hypot(Ax + Bx, Ay + By) == 5 and math.hypot(Ax - Bx, Ay - By) == math.sqrt(5)
add(T, "Vectors", "Basic", "numerical",
    "For the vectors A = 2î + 3ĵ and B = î + ĵ, the magnitude of A + B is:",
    place("5", ["7", "√5", "√13 + √2"], "D"),
    "Adding vectors by components",
    "Add the x-components and the y-components separately, then find the magnitude of the resultant.",
    ["A + B = 3î + 4ĵ", "|A + B| = √(9 + 16) = 5"],
    why="7 adds the components 3 + 4 without squaring. √5 is the magnitude of A − B. √13 + √2 adds the magnitudes, "
        "which is valid only for parallel vectors.",
    ncert="Class 11 Physics, 'Motion in a Plane', vector addition: analytical method", seconds=30, recomputed=True)

w_min = 2 * math.pi / 3600
assert close(w_min, math.pi / 1800)
add(T, "Uniform circular motion", "Basic", "numerical",
    "The angular speed of the minute hand of a clock that is keeping correct time is:",
    place("π/1800 rad/s", ["π/30 rad/s", "π/3600 rad/s", "π/21600 rad/s"], "C"),
    "Angular speed from the period",
    "The minute hand turns through 2π rad in one hour (3600 s) at a steady rate, so ω = 2π/T.",
    ["T = 3600 s", "ω = 2π/3600 = π/1800 rad/s"],
    why="π/30 rad/s is the angular speed of the seconds hand (T = 60 s). π/3600 rad/s forgets the factor 2 in 2π. "
        "π/21600 rad/s is the hour hand (T = 12 h).",
    ncert="Class 11 Physics, 'Motion in a Plane', uniform circular motion (angular speed)", seconds=30,
    recomputed=True)

v1_, v2_ = 40, 60
vav = 2 * v1_ * v2_ / (v1_ + v2_)
assert vav == 48
add(T, "Motion in a straight line", "Intermediate", "numerical",
    "A car travels the first half of the distance between two towns at a constant speed of 40 km/h and the second "
    "half at a constant speed of 60 km/h, along a straight road. Its average speed for the whole journey is:",
    place("48 km/h", ["50 km/h", "24 km/h", "52 km/h"], "A"),
    "Average speed as total distance over total time",
    "Average speed is total distance divided by total time. With equal distances, the slower half takes longer, so "
    "the average is weighted towards the lower speed: it is the harmonic mean 2v₁v₂/(v₁ + v₂).",
    ["Let each half be d: total time = d/40 + d/60 = d/24", "Average speed = 2d ÷ (d/24) = 48 km/h"],
    shortcut="Equal distances → v_av = 2v₁v₂/(v₁ + v₂) = 4800/100 = 48 km/h.",
    why="50 km/h is the arithmetic mean, true only for equal time intervals. 24 km/h forgets that the total distance "
        "is 2d. 52 km/h weights the average towards the faster speed.",
    ncert="Class 11 Physics, 'Motion in a Straight Line', average velocity and average speed", seconds=45,
    recomputed=True)

u, th = 20, math.radians(30)
ux, uy = u * math.cos(th), u * math.sin(th)
t1 = 10 * math.sqrt(3) / ux
y1 = uy * t1 - 0.5 * g * t1 ** 2
assert close(t1, 1) and close(y1, 5) and close(uy * t1, 10)
add(T, "Projectile motion", "Intermediate", "numerical",
    "A ball is projected from level ground with a speed of 20 m/s at 30° above the horizontal. Taking g = 10 m/s² "
    "and neglecting air resistance, its height above the ground when it has moved a horizontal distance of 10√3 m "
    "is:",
    place("5 m", ["10 m", "15 m", "2.5 m"], "B"),
    "Independence of horizontal and vertical motion",
    "The horizontal velocity u cos θ is constant, so the horizontal distance fixes the time. That time then gives "
    "the height from the vertical motion, which has acceleration −g.",
    ["uₓ = 20 cos 30° = 10√3 m/s → t = 10√3/10√3 = 1 s", "u_y = 20 sin 30° = 10 m/s",
     "y = 10 × 1 − ½ × 10 × 1² = 5 m"],
    why="10 m ignores the fall due to gravity (u_y t only). 15 m adds ½gt² instead of subtracting it. 2.5 m uses "
        "½ × ½gt² for the drop and the wrong sign.",
    ncert="Class 11 Physics, 'Motion in a Plane', projectile motion", seconds=60, recomputed=True)

vA = (10, 0)        # east, north components
vB = (0, 10)
vBA = (vB[0] - vA[0], vB[1] - vA[1])
assert vBA == (-10, 10) and close(math.hypot(*vBA), 10 * math.sqrt(2))
add(T, "Relative velocity", "Intermediate", "numerical",
    "Ship A sails due east at 10 m/s and ship B sails due north at 10 m/s, both with constant velocities. The "
    "velocity of ship B relative to ship A is:",
    place("10√2 m/s towards north-west", ["10√2 m/s towards north-east", "20 m/s towards north",
                                          "10√2 m/s towards south-east"], "C"),
    "Relative velocity in two dimensions",
    "v_BA = v_B − v_A. Subtracting an eastward velocity is the same as adding a westward one, so B appears to A to "
    "move north and west at once.",
    ["v_BA = (10 north) + (10 west)", "|v_BA| = √(10² + 10²) = 10√2 m/s", "Direction: 45° west of north (north-west)"],
    why="North-east adds v_A instead of subtracting it. 20 m/s towards north adds the magnitudes as if the "
        "velocities were parallel. South-east is the velocity of A relative to B.",
    ncert="Class 11 Physics, 'Motion in a Plane', relative velocity in two dimensions", seconds=50, recomputed=True)

# v = 10 − 5t from t = 0 to 4 s
disp = 10 * 4 - 2.5 * 16
dist_ = 2 * (0.5 * 2 * 10)
assert disp == 0 and dist_ == 20
add(T, "Graphs of motion", "Intermediate", "numerical",
    "The velocity–time graph of a particle moving along a straight line is a single straight line going from "
    "+10 m/s at t = 0 to −10 m/s at t = 4 s. For the interval t = 0 to t = 4 s, its displacement and the distance "
    "it travels are respectively:",
    place("0 and 20 m", ["20 m and 20 m", "0 and 0", "0 and 40 m"], "D"),
    "Displacement and distance from a velocity–time graph",
    "The area between the v–t graph and the time axis gives displacement, with area below the axis counted "
    "negative. Distance adds the magnitudes of the areas. The line crosses the axis at t = 2 s.",
    ["Area from 0 to 2 s = ½ × 2 × 10 = +10 m", "Area from 2 s to 4 s = −10 m",
     "Displacement = 0; distance = 10 + 10 = 20 m"],
    why="20 m for displacement ignores the sign of the area below the axis. 0 for distance forgets that the particle "
        "actually moves. 40 m doubles the area of each triangle.",
    ncert="Class 11 Physics, 'Motion in a Straight Line', velocity–time graph and displacement", seconds=50,
    recomputed=True)

P = 1.0
assert close(math.sqrt(2 * P ** 2 + 2 * P ** 2 * math.cos(math.radians(120))), P)
assert close(2 * P * math.sin(math.radians(30)), P)       # |A − B| at 60°
add(T, "Vectors", "Intermediate", "statement_pair",
    SP_STEM.format(
        s1="If two vectors of equal magnitude P have a resultant of magnitude P, the angle between them is 120°.",
        s2="If two vectors of equal magnitude P are inclined at 60° to each other, the magnitude of their "
           "difference is P√3."),
    sp("C"),
    "Resultant and difference of two equal vectors",
    "For two vectors of magnitude P at angle θ, |A + B|² = 2P²(1 + cos θ) and |A − B|² = 2P²(1 − cos θ), that is "
    "|A + B| = 2P cos(θ/2) and |A − B| = 2P sin(θ/2).",
    ["Statement I: P² = 2P²(1 + cos θ) → cos θ = −½ → θ = 120° (true)",
     "Statement II: |A − B| = 2P sin 30° = P, not P√3 (false; P√3 is |A + B| at 60°)"],
    why="Statement II gives the magnitude of the sum, not the difference, so options A, B and D fail.",
    ncert="Class 11 Physics, 'Motion in a Plane', addition and subtraction of vectors", seconds=60)

beta = 4
acc = beta ** 2 / 2
x2 = 0.5 * acc * 2 ** 2
assert acc == 8 and x2 == 16
add(T, "Motion in a straight line", "Advanced", "numerical",
    "A particle starts from rest at the origin and moves along the positive x-axis so that its velocity at position "
    "x is v = 4√x, with v in m/s and x in metres. The distance it covers in the first 2 s is:",
    place("16 m", ["8 m", "32 m", "64 m"], "B"),
    "Acceleration from velocity as a function of position",
    "With v given as a function of x, a = v(dv/dx). For v = β√x this is a constant, β²/2, so the particle moves with "
    "uniform acceleration from rest.",
    ["dv/dx = 4 × 1/(2√x) = 2/√x", "a = v dv/dx = 4√x × 2/√x = 8 m/s² (constant)",
     "x = ½ × 8 × 2² = 16 m"],
    shortcut="v² = 16x = 2ax → a = 8 m/s² directly.",
    why="8 m uses a = 4 m/s² (β instead of β²/2). 32 m forgets the factor ½ in ½at². 64 m takes x = (vt)² with "
        "v = 4 m/s.",
    ncert="Class 11 Physics, 'Motion in a Straight Line', instantaneous velocity and acceleration", seconds=90,
    recomputed=True)

u, th = 20, math.radians(60)
r_top = (u * math.cos(th)) ** 2 / g
assert close(r_top, 10) and close(u ** 2 / g, 40) and close((u * math.sin(th)) ** 2 / g, 30)
assert close((u * math.sin(th)) ** 2 / (2 * g), 15)
add(T, "Projectile motion", "Advanced", "numerical",
    "A particle is projected from level ground with a speed of 20 m/s at 60° above the horizontal. Taking "
    "g = 10 m/s² and neglecting air resistance, the radius of curvature of its path at the highest point is:",
    place("10 m", ["40 m", "30 m", "15 m"], "D"),
    "Projectile at its highest point as instantaneous circular motion",
    "At the top the velocity is horizontal (u cos θ) and the acceleration g is vertical, i.e. perpendicular to the "
    "velocity. So g acts as the centripetal acceleration: g = v²/r.",
    ["v at top = 20 cos 60° = 10 m/s", "r = v²/g = 100/10 = 10 m"],
    why="40 m uses the full launch speed (u²/g). 30 m uses the vertical component of the launch velocity. 15 m is "
        "the maximum height, not the radius of curvature.",
    ncert="Class 11 Physics, 'Motion in a Plane', projectile motion and centripetal acceleration", seconds=75,
    recomputed=True)

x = lambda t: 5 + 4 * t - t ** 2
v = lambda t: 4 - 2 * t
assert v(2) == 0 and x(4) - x(0) == 0 and abs(x(2) - x(0)) + abs(x(4) - x(2)) == 8 and abs(v(4)) == 4
multi_key([v(2) == 0, x(4) == x(0), False, False, abs(v(4)) == 4], "abe")
add(T, "Motion in a straight line", "Advanced", "multi_statement",
    multi("The position of a particle moving along the x-axis is x = 5 + 4t − t², with x in metres and t in "
          "seconds. Consider its motion from t = 0 to t = 4 s. Which of the following statements are correct?",
          ["The particle reverses its direction of motion at t = 2 s.",
           "Its displacement over the interval t = 0 to t = 4 s is zero.",
           "The distance it travels over the interval t = 0 to t = 4 s is 4 m.",
           "Its acceleration is zero at t = 2 s.",
           "Its speed at t = 4 s is 4 m/s."]),
    place("(a), (b) and (e) only", ["(a), (c) and (d) only", "(b), (c) and (e) only", "(a), (b), (d) and (e) only"],
          "A"),
    "Velocity, acceleration, distance and displacement from x(t)",
    "v = dx/dt = 4 − 2t and a = −2 m/s² (constant). The particle stops and turns back where v = 0. Distance must "
    "be added in pieces on either side of the turning point.",
    ["(a) v = 0 at t = 2 s and changes sign → true",
     "(b) x(0) = 5 m, x(4) = 5 m → displacement 0 → true",
     "(c) x(2) = 9 m: distance = 4 + 4 = 8 m, not 4 m → false",
     "(d) a = −2 m/s² at all times → false (v = 0 does not mean a = 0)",
     "(e) v(4) = −4 m/s → speed 4 m/s → true"],
    why="Options with (c) halve the distance; options with (d) confuse momentary rest with zero acceleration.",
    ncert="Class 11 Physics, 'Motion in a Straight Line', instantaneous velocity and acceleration", seconds=120,
    recomputed=True)

add(T, "Relative velocity", "Advanced", "statement_pair",
    SP_STEM.format(
        s1="A man standing on a platform that moves vertically upward with a constant velocity throws a ball "
           "vertically upward. Neglecting air resistance, the time after which the ball returns to his hand is the "
           "same as it would be if the platform were at rest.",
        s2="An observer on the ground finds the ball momentarily at rest at the instant when it is at its greatest "
           "height above the man."),
    sp("C"),
    "Relative motion in a frame moving with constant velocity",
    "Relative to the platform, the ball starts with the throw speed u and has acceleration g downward (the "
    "platform does not accelerate), so it returns after 2u/g, just as on a fixed platform. At its greatest height "
    "above the man, the ball's velocity relative to him is zero, so relative to the ground it moves upward with the "
    "platform's velocity, not zero.",
    ["Relative acceleration = g − 0 = g; relative initial velocity = u → return time 2u/g (Statement I true)",
     "Greatest height above the man: v_ball − v_platform = 0 → v_ball = v_platform ≠ 0 (Statement II false)"],
    why="Statement II mixes the man's frame with the ground frame; in the ground frame the ball is at rest only "
        "later, when it reaches its greatest height above the ground.",
    ncert="Class 11 Physics, 'Motion in a Straight Line', relative velocity", seconds=75)


# =====================================================================================================================
# Laws of Motion (B4 I5 A4)
# =====================================================================================================================
T = "Laws of Motion"

p = lambda t: 2 * t ** 2 + 3 * t
Fp = lambda t: 4 * t + 3
assert Fp(2) == 11 and p(2) == 14 and p(2) / 2 == 7
add(T, "Newton's laws and impulse", "Basic", "numerical",
    "The linear momentum of a body moving along a straight line varies with time as p = 2t² + 3t, where p is in "
    "kg m/s and t in seconds. The net force acting on the body at t = 2 s is:",
    place("11 N", ["14 N", "8 N", "7 N"], "C"),
    "Newton's second law as rate of change of momentum",
    "The net force equals the instantaneous rate of change of linear momentum, F = dp/dt.",
    ["F = dp/dt = 4t + 3", "At t = 2 s: F = 8 + 3 = 11 N"],
    why="14 N is the momentum (in kg m/s) at t = 2 s, not its rate of change. 8 N drops the 3t term's derivative. "
        "7 N is the average p/t, which is not the instantaneous force.",
    ncert="Class 11 Physics, 'Laws of Motion', Newton's second law of motion", seconds=35, recomputed=True)

add(T, "Newton's laws and impulse", "Basic", "direct",
    "At a certain instant, the net force acting on a moving body is directed due north. Which of the following must "
    "be true at that instant?",
    place("The acceleration of the body is directed due north, but its velocity may be in any direction",
          ["The velocity of the body is directed due north",
           "The body is moving due north with increasing speed",
           "The velocity and the acceleration of the body are both directed due north"], "D"),
    "Force fixes acceleration, not velocity",
    "By the second law, F = ma, so the acceleration is always along the net force. The velocity at an instant "
    "depends on the past motion: a body thrown upward has a downward force on it while it still moves up, and a "
    "body in circular motion has a force perpendicular to its velocity.",
    ["a is parallel to F_net → a is due north", "Velocity is not fixed by the force at that instant"],
    why="All the other options tie the velocity to the force, which is not required (e.g. a body moving south while "
        "being slowed down by a northward force).",
    ncert="Class 11 Physics, 'Laws of Motion', Newton's second law of motion", seconds=35)

mu_s, g = 0.4, 10
assert mu_s * g == 4
add(T, "Friction", "Basic", "numerical",
    "A wooden box rests on the horizontal floor of a truck. The coefficient of static friction between the box and "
    "the floor is 0.4. Taking g = 10 m/s², the maximum acceleration with which the truck can start moving along a "
    "level road without the box slipping on its floor is:",
    place("4 m/s²", ["0.4 m/s²", "40 m/s²", "25 m/s²"], "A"),
    "Static friction as the force that accelerates a body",
    "The only horizontal force on the box is the static friction from the floor, so it must supply ma. The largest "
    "value it can take is μₛmg, which limits the acceleration to μₛg, whatever the mass of the box.",
    ["ma ≤ μₛmg → a ≤ μₛg", "a_max = 0.4 × 10 = 4 m/s²"],
    why="0.4 m/s² forgets to multiply by g. 40 m/s² multiplies by 100 instead of g. 25 m/s² divides g by μₛ.",
    ncert="Class 11 Physics, 'Laws of Motion', friction (static friction)", seconds=35, recomputed=True)

add(T, "Equilibrium of concurrent forces", "Basic", "direct",
    "A particle is in equilibrium under the action of three coplanar concurrent forces. Which of the following must "
    "be true?",
    place("The three forces can be represented in magnitude and direction by the three sides of a triangle taken "
          "in the same order",
          ["The three forces must be equal in magnitude",
           "The three forces must be mutually perpendicular",
           "One of the forces must be greater than the sum of the other two"], "B"),
    "Equilibrium under three concurrent forces",
    "For equilibrium the vector sum of the forces must be zero: F₁ + F₂ + F₃ = 0. Placing the forces head to tail "
    "then closes the figure, so they form the sides of a triangle taken in order.",
    ["F₁ + F₂ + F₃ = 0", "Head-to-tail placement returns to the start → closed triangle"],
    why="The forces need not be equal or perpendicular (three mutually perpendicular forces cannot even be coplanar "
        "and sum to zero). If one force exceeded the sum of the others, they could never cancel.",
    ncert="Class 11 Physics, 'Laws of Motion', equilibrium of a particle", seconds=35)

m = 0.2
v1, v2 = math.sqrt(2 * g * 5), math.sqrt(2 * g * 1.25)
J = m * (v1 + v2)
assert close(v1, 10) and close(v2, 5) and close(J, 3)
add(T, "Newton's laws and impulse", "Intermediate", "numerical",
    "A ball of mass 0.2 kg is dropped from rest from a height of 5 m onto a hard horizontal floor and rebounds "
    "vertically to a height of 1.25 m. Taking g = 10 m/s² and neglecting air resistance, the magnitude of the impulse "
    "exerted by the floor on the ball is:",
    place("3 N s", ["1 N s", "2 N s", "4 N s"], "D"),
    "Impulse as change in momentum, with direction",
    "The impulse equals the change in momentum. The ball reaches the floor moving down and leaves it moving up, so "
    "the change in velocity is the sum of the two speeds.",
    ["Speed on striking: √(2 × 10 × 5) = 10 m/s (down)", "Speed on leaving: √(2 × 10 × 1.25) = 5 m/s (up)",
     "J = 0.2 × (5 − (−10)) = 3 N s (upward)"],
    why="1 N s subtracts the speeds, ignoring the reversal of direction. 2 N s only removes the downward momentum. "
        "4 N s assumes the ball bounces back with the same speed of 10 m/s.",
    ncert="Class 11 Physics, 'Laws of Motion', impulse", seconds=60, recomputed=True)

m1, m2 = 1, 2
v1, v2 = 2, 1                                    # equal and opposite momenta
K1, K2 = F(1, 2) * m1 * v1 ** 2, F(1, 2) * m2 * v2 ** 2
assert m1 * v1 == m2 * v2 and K1 / K2 == 2
add(T, "Conservation of linear momentum", "Intermediate", "numerical",
    "A bomb at rest explodes into two fragments whose masses are in the ratio 1 : 2. Just after the explosion, the "
    "ratio of the kinetic energy of the lighter fragment to that of the heavier fragment is:",
    place("2 : 1", ["1 : 2", "1 : 4", "4 : 1"], "C"),
    "Momentum conservation in an explosion with K = p²/2m",
    "The total momentum is zero before the explosion, so the two fragments have momenta equal in magnitude and "
    "opposite in direction. With equal p, K = p²/2m is inversely proportional to the mass.",
    ["p₁ = p₂ = p", "K₁/K₂ = (p²/2m₁)/(p²/2m₂) = m₂/m₁ = 2/1"],
    why="1 : 2 makes kinetic energy proportional to mass. 1 : 4 and 4 : 1 square the mass ratio, as if the speeds "
        "were equal or the momentum ratio were squared incorrectly.",
    ncert="Class 11 Physics, 'Laws of Motion', conservation of momentum", seconds=50, recomputed=True)

a = 10 / 2
s1 = 0.5 * a * 3 ** 2
v3 = a * 3
s2 = v3 * 2
assert s1 == 22.5 and v3 == 15 and s1 + s2 == 52.5 and 0.5 * a * 25 == 62.5
add(T, "Newton's laws and impulse", "Intermediate", "numerical",
    "A constant horizontal force of 10 N acts for 3 s on a body of mass 2 kg lying at rest on a smooth horizontal "
    "surface, and is then removed. The distance the body covers in the first 5 s from the start is:",
    place("52.5 m", ["62.5 m", "22.5 m", "37.5 m"], "A"),
    "Accelerated motion followed by motion with constant velocity (first law)",
    "While the force acts the body accelerates at F/m. Once the force is removed the net force is zero, so by the "
    "first law the body keeps the velocity it has gained.",
    ["a = 10/2 = 5 m/s²; distance in 3 s = ½ × 5 × 9 = 22.5 m", "Velocity at 3 s = 15 m/s",
     "Next 2 s at constant velocity: 15 × 2 = 30 m", "Total = 52.5 m"],
    why="62.5 m assumes the force acts for all 5 s. 22.5 m assumes the body stops when the force is removed. "
        "37.5 m adds only one second of uniform motion.",
    ncert="Class 11 Physics, 'Laws of Motion', Newton's first and second laws", seconds=60, recomputed=True)

add(T, "Friction", "Intermediate", "statement_pair",
    SP_STEM.format(
        s1="When a car speeds up along a level road, the frictional force exerted by the road on its driven wheels is "
           "directed forward, in the direction of the car's motion.",
        s2="A box placed on the floor of a truck that is speeding up along a level road, without the box slipping, "
           "experiences a static frictional force directed backward, opposite to the truck's motion."),
    sp("C"),
    "Direction of static friction",
    "Friction opposes relative motion (or impending relative motion) between surfaces in contact, not the motion of "
    "the body. A driven wheel pushes the road backward at the contact point, so the road pushes the car forward. The "
    "box tends to slide backward relative to the accelerating floor, so static friction on it acts forward; this is "
    "the only horizontal force that can accelerate the box with the truck.",
    ["Statement I: forward friction on the driven wheels accelerates the car (true)",
     "Statement II: friction on the box must be forward to give it the truck's acceleration (false)"],
    why="Statement II assumes friction always acts against the direction of motion; here it is the force that "
        "produces the motion.",
    ncert="Class 11 Physics, 'Laws of Motion', friction", seconds=60)

m = 0.5
netA = m * g
netB = 0
netC = m * 2
netD = m * 2 ** 2 / 0.5
assert (netA, netB, netC, netD) == (5, 0, 1, 4)
add(T, "Newton's laws and impulse", "Intermediate", "match_list",
    match_stem("A small stone of mass 0.5 kg is in each of the situations in List-I. Take g = 10 m/s² and neglect air "
               "resistance. Match List-I (situation) with List-II (magnitude of the net force on the stone).",
               ["Just after it is released from rest from a window, falling freely",
                "Resting on the floor of a lift that moves upward with a constant velocity",
                "Resting on the floor of a lift that is accelerating upward at 2 m/s²",
                "Moving in a circle of radius 0.5 m at a constant speed of 2 m/s on a smooth horizontal table, held "
                "by a string"],
               ["0", "1 N", "4 N", "5 N"]),
    match_options({"A": "IV", "B": "I", "C": "II", "D": "III"},
                  [{"A": "I", "B": "IV", "C": "II", "D": "III"}, {"A": "IV", "B": "II", "C": "I", "D": "III"},
                   {"A": "IV", "B": "I", "C": "III", "D": "II"}], "D"),
    "Net force equals mass times acceleration",
    "In every case the net force is simply m times the acceleration of the stone, whatever forces make it up.",
    ["A: a = g → F = 0.5 × 10 = 5 N (IV)", "B: constant velocity → F = 0 (I)", "C: F = 0.5 × 2 = 1 N (II)",
     "D: F = mv²/r = 0.5 × 4/0.5 = 4 N, towards the centre (III)"],
    why="The other codes give the stone at rest in the lift a non-zero net force, or confuse the net force in the "
        "accelerating lift (ma) with the normal force m(g + a) = 6 N.",
    ncert="Class 11 Physics, 'Laws of Motion', Newton's second law and circular motion", seconds=60, recomputed=True)

r, mu, g = 30, 0.5, 10
tan_t = 1.0
vmin = math.sqrt(r * g * (tan_t - mu) / (1 + mu * tan_t))
vmax = math.sqrt(r * g * (tan_t + mu) / (1 - mu * tan_t))
assert close(vmin, 10) and close(vmax, 30) and close(math.sqrt(r * g * tan_t), 10 * math.sqrt(3))
assert close(math.sqrt(r * g * (tan_t - mu)), 5 * math.sqrt(6))
add(T, "Circular motion: level and banked roads", "Advanced", "numerical",
    "A circular road of radius 30 m is banked at 45°. The coefficient of static friction between the tyres and the "
    "road is 0.5. Taking g = 10 m/s², the minimum speed at which a car can go round the curve without sliding down "
    "the slope is:",
    place("10 m/s", ["10√3 m/s", "30 m/s", "5√6 m/s"], "B"),
    "Banked road: friction acting up the slope at low speed",
    "Below the speed for which no friction is needed, the car tends to slide down the slope, so friction acts up "
    "the slope. At the minimum speed this friction is limiting (μN).",
    ["Vertical: N cos θ + μN sin θ = mg", "Horizontal: N sin θ − μN cos θ = mv²/r",
     "v²_min = rg (tan θ − μ)/(1 + μ tan θ) = 300 × 0.5/1.5 = 100", "v_min = 10 m/s"],
    why="10√3 m/s is the speed that needs no friction (√(rg tan θ)). 30 m/s is the maximum safe speed, with friction "
        "down the slope. 5√6 m/s drops the denominator (1 + μ tan θ).",
    ncert="Class 11 Physics, 'Laws of Motion', circular motion: car on a banked road", seconds=120, recomputed=True)

m, sin_t, cos_t, mu = 5, 0.6, 0.8, 0.5
F_low = m * g * (sin_t - mu * cos_t)
F_high = m * g * (sin_t + mu * cos_t)
assert close(F_low, 10) and close(F_high, 50) and sin_t / cos_t > mu
add(T, "Friction", "Advanced", "numerical",
    "A block of mass 5 kg rests on a rough plane inclined at 37° to the horizontal (sin 37° = 0.6, cos 37° = 0.8). "
    "The coefficient of static friction between the block and the plane is 0.5. A force F is applied to the block "
    "parallel to the incline, pointing up the slope. Taking g = 10 m/s², the block stays at rest for:",
    place("10 N ≤ F ≤ 50 N", ["0 ≤ F ≤ 50 N", "10 N ≤ F ≤ 30 N", "F = 30 N only"], "D"),
    "Range of an applied force for which static friction can hold a block",
    "Static friction can act either way along the incline, up to μₛN. At the lower limit the block is about to slide "
    "down (friction up the slope); at the upper limit it is about to slide up (friction down the slope).",
    ["N = mg cos θ = 40 N → f_max = 0.5 × 40 = 20 N; mg sin θ = 30 N",
     "About to slide down: F + 20 = 30 → F = 10 N", "About to slide up: F = 30 + 20 = 50 N"],
    why="0 ≤ F ≤ 50 N forgets that tan 37° = 0.75 > 0.5, so without help the block slides down. 10 N ≤ F ≤ 30 N "
        "lets friction act only up the slope. F = 30 N only ignores static friction altogether.",
    ncert="Class 11 Physics, 'Laws of Motion', friction (static friction on an inclined plane)", seconds=120,
    recomputed=True)

m, th, mus, muk = 2, math.radians(30), 0.7, 0.5
N = m * g * math.cos(th)
stays = math.tan(th) < mus
contact = math.hypot(N, m * g * math.sin(th))
accel_down = g * (math.sin(th) - muk * math.cos(th))
multi_key([stays, close(contact, 20), close(m * g * math.sin(th), mus * N), accel_down > 0, close(N, 20)], "abd")
add(T, "Friction", "Advanced", "multi_statement",
    multi("A block of mass 2 kg is placed on a rough plane inclined at 30° to the horizontal. The coefficients of "
          "static and kinetic friction between the block and the plane are 0.7 and 0.5. Take g = 10 m/s². Which of "
          "the following statements are correct?",
          ["Left to itself, the block stays at rest on the incline.",
           "While the block is at rest, the total force exerted by the plane on it is 20 N, directed vertically "
           "upward.",
           "While the block is at rest, the friction force on it equals μₛ times the normal reaction.",
           "If the block is set sliding down the incline and then left to itself, it keeps speeding up.",
           "The normal reaction on the block is 20 N."]),
    place("(a), (b) and (d) only", ["(a), (c) and (e) only", "(a), (b), (c) and (d) only", "(b), (d) and (e) only"],
          "B"),
    "Static and kinetic friction on an incline",
    "The block stays at rest if tan θ ≤ μₛ. At rest, gravity is balanced by the plane, so the plane's total force "
    "(normal force plus friction) is equal and opposite to the weight. Once sliding, kinetic friction μₖN is smaller, "
    "and if tan θ > μₖ the block accelerates down.",
    ["(a) tan 30° = 0.577 < 0.7 → at rest (true)",
     "(b) Plane's force = −(weight) = 20 N upward (true)",
     "(c) Friction = mg sin 30° = 10 N, less than μₛN = 0.7 × 17.3 = 12.1 N (false)",
     "(d) tan 30° = 0.577 > 0.5 → net force down the incline = 10 − 8.66 > 0 (true)",
     "(e) N = mg cos 30° = 10√3 ≈ 17.3 N, not 20 N (false)"],
    why="(c) treats static friction as always limiting; (e) forgets the factor cos θ.",
    ncert="Class 11 Physics, 'Laws of Motion', friction", seconds=150, recomputed=True)

u, th = 20 * math.sqrt(2), math.radians(45)
R = u ** 2 * math.sin(2 * th) / g
# at the top, one half falls straight down (velocity 0), the other gets 2u cos θ; it lands R/2 farther than a whole shell would
x_far = R / 2 + 2 * (R / 2)
assert close(R, 80) and close(x_far, 120) and close(R / 2 + 40 * 4, 200)
add(T, "Conservation of linear momentum", "Advanced", "numerical",
    "A shell is fired from level ground with a speed of 20√2 m/s at 45° above the horizontal. At the highest point of "
    "its path it explodes into two fragments of equal mass. One fragment falls vertically downward, starting from "
    "rest just after the explosion. Taking g = 10 m/s² and neglecting air resistance, the other fragment lands at a "
    "distance from the point of firing of:",
    place("120 m", ["80 m", "160 m", "200 m"], "A"),
    "Conservation of momentum in an explosion during projectile motion",
    "The explosion forces are internal and act for a very short time, so the horizontal momentum just before and "
    "just after the explosion is the same. If one half is left at rest, the other half carries all the momentum and "
    "moves horizontally with twice the shell's speed. Both halves take the same time to fall as the shell would "
    "have taken to come down.",
    ["Range of the shell R = u² sin 90°/g = 800/10 = 80 m; top is at 40 m",
     "Speed at top = 20√2 cos 45° = 20 m/s → other fragment: (m/2)v = m × 20 → v = 40 m/s",
     "Fall time from top = u sin 45°/g = 2 s → extra distance = 40 × 2 = 80 m",
     "Landing point = 40 + 80 = 120 m"],
    shortcut="The second fragment lands at R/2 + R = 1.5R = 120 m.",
    why="80 m is where the unbroken shell would land. 160 m doubles the whole range. 200 m lets the fragment move "
        "at 40 m/s for the full 4 s time of flight instead of only the 2 s of its fall.",
    ncert="Class 11 Physics, 'Laws of Motion', conservation of momentum", seconds=120, recomputed=True)


# =====================================================================================================================
# Work, Energy and Power (B4 I5 A4)
# =====================================================================================================================
T = "Work, Energy and Power"

Fv, dv = (3, 4, 0), (2, -1, 5)
W = sum(a * b for a, b in zip(Fv, dv))
assert W == 2 and 3 * 2 + 4 * 1 == 10
add(T, "Work by constant and variable force", "Basic", "numerical",
    "A constant force F = (3î + 4ĵ) N acts on a particle while it undergoes a displacement d = (2î − ĵ + 5k̂) m. "
    "The work done by the force is:",
    place("2 J", ["−2 J", "10 J", "5√30 J"], "C"),
    "Work as the scalar product of force and displacement",
    "W = F · d = FₓDₓ + F_yD_y + F_zD_z. Components of the displacement along which the force has no component "
    "contribute nothing.",
    ["W = 3 × 2 + 4 × (−1) + 0 × 5", "= 6 − 4 + 0 = 2 J"],
    why="−2 J reverses the sign of the result. 10 J ignores the negative sign of the y-component of d. 5√30 J "
        "multiplies the magnitudes, as if F and d were parallel.",
    ncert="Class 11 Physics, 'Work, Energy and Power', notions of work and kinetic energy (scalar product)",
    seconds=30, recomputed=True)

m = 0.5
Wn = 0.5 * m * (6 ** 2 - 2 ** 2)
assert Wn == 8 and 0.5 * m * (6 - 2) ** 2 == 4 and 0.5 * m * 36 == 9 and m * (36 - 4) == 16
add(T, "Work-energy theorem", "Basic", "numerical",
    "The speed of a ball of mass 0.5 kg increases from 2 m/s to 6 m/s. The work done by the net force on the ball is:",
    place("8 J", ["4 J", "9 J", "16 J"], "A"),
    "Work-energy theorem",
    "The work done by the net force equals the change in kinetic energy, W = ½mv² − ½mu².",
    ["W = ½ × 0.5 × (6² − 2²) = 0.25 × 32 = 8 J"],
    why="4 J uses the square of the change in speed, (6 − 2)², instead of the change in the squares. 9 J is the final "
        "kinetic energy alone. 16 J drops the factor ½.",
    ncert="Class 11 Physics, 'Work, Energy and Power', work-energy theorem", seconds=30, recomputed=True)

k_, x_ = 100, 0.1
assert 0.5 * k_ * (2 * x_) ** 2 == 4 * (0.5 * k_ * x_ ** 2)
add(T, "Spring potential energy", "Basic", "direct",
    "The extension of an ideal spring, within its elastic limit, is doubled. The elastic potential energy stored in "
    "it becomes:",
    place("four times its earlier value", ["twice its earlier value", "the same as before", "half its earlier value"],
          "B"),
    "Potential energy of a spring",
    "The potential energy of a spring stretched by x is ½kx², proportional to the square of the extension.",
    ["U ∝ x²", "x → 2x: U → 4U"],
    why="'Twice' treats U as proportional to x (true of the spring force, not of the energy). The others ignore the "
        "dependence on x.",
    ncert="Class 11 Physics, 'Work, Energy and Power', the potential energy of a spring", seconds=25)

p_, m_ = 20, 4
assert p_ ** 2 / (2 * m_) == 50 and p_ ** 2 / m_ == 100 and p_ * m_ / 2 == 40
add(T, "Work-energy theorem", "Basic", "numerical",
    "A body of mass 4 kg has a linear momentum of magnitude 20 kg m/s. Its kinetic energy is:",
    place("50 J", ["100 J", "40 J", "5 J"], "D"),
    "Relation between kinetic energy and momentum",
    "K = ½mv² and p = mv, so K = p²/2m.",
    ["K = 20²/(2 × 4) = 400/8 = 50 J"],
    why="100 J drops the factor 2 in the denominator. 40 J computes pm/2 instead of p²/2m. 5 J is only the speed "
        "p/m = 5 m/s.",
    ncert="Class 11 Physics, 'Work, Energy and Power', kinetic energy", seconds=30, recomputed=True)

mass_per_s = 600 / 60
P_out = mass_per_s * g * 10
P_in = P_out / 0.8
assert P_out == 1000 and P_in == 1250 and P_out * 0.8 == 800
add(T, "Power", "Intermediate", "numerical",
    "An electric pump raises 600 kg of water per minute through a height of 10 m. The efficiency of the pump is 80%. "
    "Taking g = 10 m/s² and neglecting the kinetic energy given to the water, the electrical power drawn by the pump "
    "is:",
    place("1250 W", ["1000 W", "800 W", "60 kW"], "B"),
    "Power and efficiency",
    "The useful (output) power is the rate of gain of potential energy of the water. Efficiency is output power "
    "divided by input power, so the input is the output divided by 0.8.",
    ["Mass per second = 600/60 = 10 kg/s", "Output power = 10 × 10 × 10 = 1000 W",
     "Input power = 1000/0.8 = 1250 W"],
    why="1000 W is the useful output, not the power drawn. 800 W multiplies by the efficiency instead of dividing. "
        "60 kW takes the energy per minute (60 000 J) as the power.",
    ncert="Class 11 Physics, 'Work, Energy and Power', power", seconds=50, recomputed=True)

Wx = lambda a_, b_: (6 * b_ - b_ ** 2) - (6 * a_ - a_ ** 2)
assert Wx(0, 4) == 8 and Wx(0, 3) == 9 and Wx(0, 3) + abs(Wx(3, 4)) == 10
add(T, "Work by constant and variable force", "Intermediate", "numerical",
    "A force F = (6 − 2x) N, where x is in metres, acts along the x-axis on a particle. The work done by this force "
    "as the particle moves from x = 0 to x = 4 m is:",
    place("8 J", ["9 J", "10 J", "24 J"], "A"),
    "Work done by a variable force as an integral",
    "W = ∫F dx. The force is positive up to x = 3 m and negative beyond it, so the area under the F–x graph between "
    "3 m and 4 m counts as negative work.",
    ["W = ∫₀⁴ (6 − 2x) dx = [6x − x²]₀⁴", "= 24 − 16 = 8 J",
     "(Check: +9 J from 0 to 3 m and −1 J from 3 to 4 m)"],
    why="9 J stops at x = 3 m, where the force becomes zero. 10 J adds the magnitude of the negative area. 24 J "
        "treats the force as constant at its initial value of 6 N.",
    ncert="Class 11 Physics, 'Work, Energy and Power', work done by a variable force", seconds=60, recomputed=True)

# Just completes the circle: v_top² = gr; at horizontal position v² = 3gr, tension = mv²/r = 3mg
v_top2 = 1
v_h2 = v_top2 + 2 * 1
assert v_h2 == 3
add(T, "Motion in a vertical circle", "Intermediate", "numerical",
    "A small bob of mass m, tied to a light string, is whirled in a vertical circle with the least speed that lets "
    "it just complete the circle. Neglecting air resistance, the tension in the string when the string is "
    "horizontal is:",
    place("3mg", ["mg", "2mg", "6mg"], "D"),
    "Energy conservation and the radial equation in a vertical circle",
    "Just completing the circle means the tension is zero at the top, so v_top² = gr. Coming down to the level of "
    "the centre, the bob falls through r. With the string horizontal, gravity is perpendicular to it, so the tension "
    "alone provides the centripetal force.",
    ["v_top² = gr", "v² (string horizontal) = gr + 2gr = 3gr", "T = mv²/r = 3mg"],
    why="mg is the tension when the bob hangs at rest. 2mg uses v² = 2gr, forgetting the speed at the top. 6mg is "
        "the tension at the lowest point.",
    ncert="Class 11 Physics, 'Work, Energy and Power', motion in a vertical circle", seconds=75, recomputed=True)

m1, u1, m2, u2 = 2, 3, 1, -3
vc = F(m1 * u1 + m2 * u2, m1 + m2)
Ki = F(1, 2) * m1 * u1 ** 2 + F(1, 2) * m2 * u2 ** 2
Kf = F(1, 2) * (m1 + m2) * vc ** 2
assert vc == 1 and Ki == F(27, 2) and Kf == F(3, 2) and Ki - Kf == 12
add(T, "Collisions", "Intermediate", "numerical",
    "A block of mass 2 kg moving at 3 m/s on a smooth horizontal surface collides head-on with a block of mass 1 kg "
    "moving towards it at 3 m/s. The two blocks stick together. The loss of kinetic energy in the collision is:",
    place("12 J", ["13.5 J", "1.5 J", "6 J"], "C"),
    "Perfectly inelastic collision: momentum conserved, kinetic energy lost",
    "Momentum is conserved (with signs for the opposite directions), giving the common velocity. The loss is the "
    "initial total kinetic energy minus the final one.",
    ["Common velocity = (2 × 3 − 1 × 3)/3 = 1 m/s", "Initial KE = ½ × 2 × 9 + ½ × 1 × 9 = 13.5 J",
     "Final KE = ½ × 3 × 1² = 1.5 J", "Loss = 12 J"],
    why="13.5 J assumes the blocks stop dead. 1.5 J is the kinetic energy left after the collision. 6 J halves the "
        "loss.",
    ncert="Class 11 Physics, 'Work, Energy and Power', collisions (completely inelastic collision)", seconds=60,
    recomputed=True)

add(T, "Work by constant and variable force", "Intermediate", "statement_pair",
    SP_STEM.format(
        s1="The work needed to push a box slowly up a smooth inclined plane to a height h is the same as the work "
           "needed to lift it slowly and vertically through the same height h.",
        s2="Pushing the box slowly up the smooth inclined plane needs a smaller force than lifting it slowly and "
           "vertically."),
    sp("A"),
    "Work against gravity is path independent",
    "Moving the box slowly means its kinetic energy does not change, so the work done by the applied force equals "
    "the gain in potential energy, mgh, whatever the path. On the smooth incline the force needed is only "
    "mg sin θ, smaller than mg, but it acts over a longer distance h/sin θ, so the product is still mgh.",
    ["Incline: F = mg sin θ, distance = h/sin θ → W = mgh", "Vertical: F = mg, distance = h → W = mgh",
     "mg sin θ < mg → Statement II true"],
    why="Both statements are true: the incline trades a smaller force for a longer distance.",
    ncert="Class 11 Physics, 'Work, Energy and Power', the potential energy (conservative force)", seconds=50)

P, m, t = 10e3, 500, 10
vt = math.sqrt(2 * P * t / m)
assert close(vt, 20) and close(math.sqrt(P * t / m), 10 * math.sqrt(2)) and P * t / m == 200
assert round(math.sqrt(2 * 10 * t / m), 2) == 0.63
add(T, "Power", "Advanced", "numerical",
    "A car of mass 500 kg starts from rest on a level road. Its engine delivers a constant power of 10 kW to it. "
    "Neglecting friction and air resistance, the speed of the car after 10 s is:",
    place("20 m/s", ["10√2 m/s", "200 m/s", "about 0.63 m/s"], "C"),
    "Constant power: energy, not force, grows uniformly",
    "With constant power the force P/v falls as the car speeds up, so the acceleration is not uniform. The energy "
    "delivered, however, is P t, and all of it becomes kinetic energy.",
    ["Energy delivered in 10 s = 10⁴ × 10 = 10⁵ J", "½ × 500 × v² = 10⁵ → v² = 400", "v = 20 m/s"],
    why="10√2 m/s writes the kinetic energy as mv² instead of ½mv². 200 m/s equates Pt to the momentum mv. "
        "About 0.63 m/s takes the power as 10 W instead of 10 kW.",
    ncert="Class 11 Physics, 'Work, Energy and Power', power and the work-energy theorem", seconds=75,
    recomputed=True)

m, v0, mu, k = 1, 3, 0.25, 200
f = mu * m * g
x = (-f + math.sqrt(f ** 2 + 4 * (k / 2) * (0.5 * m * v0 ** 2))) / k
assert close(x, 0.2)
x_smooth = math.sqrt(m * v0 ** 2 / k)
x_wrong = (f + math.sqrt(f ** 2 + 2 * k * (0.5 * m * v0 ** 2))) / k
x_noh = (-f + math.sqrt(f ** 2 + 4 * k * (0.5 * m * v0 ** 2))) / (2 * k)
assert round(x_smooth * 100, 1) == 21.2 and close(x_wrong, 0.225) and round(x_noh * 100) == 14
add(T, "Spring potential energy", "Advanced", "numerical",
    "A block of mass 1 kg slides at 3 m/s on a rough horizontal floor (coefficient of kinetic friction 0.25) "
    "and hits the free end of a light horizontal spring of spring constant 200 N/m, whose other end is fixed to a "
    "wall. Taking g = 10 m/s², the maximum compression of the spring is:",
    place("20 cm", ["about 21.2 cm", "22.5 cm", "about 14 cm"], "B"),
    "Work-energy theorem with a spring and friction",
    "During compression the block's kinetic energy goes partly into the spring's potential energy and partly into "
    "work against friction over the compression x.",
    ["½mv² = ½kx² + μmgx", "4.5 = 100x² + 2.5x → 100x² + 2.5x − 4.5 = 0",
     "x = [−2.5 + √(6.25 + 1800)]/200 = (−2.5 + 42.5)/200 = 0.2 m"],
    why="About 21.2 cm ignores friction. 22.5 cm adds the friction term with the wrong sign, as if friction helped "
        "compress the spring. About 14 cm writes the spring energy as kx² instead of ½kx².",
    ncert="Class 11 Physics, 'Work, Energy and Power', the potential energy of a spring", seconds=120,
    recomputed=True)

R_ = 0.4
h_min = 2 * R_ + R_ / 2
assert close(h_min, 1.0)
add(T, "Motion in a vertical circle", "Advanced", "numerical",
    "A small ball is released from rest on a smooth track that runs down into a vertical circular loop of radius "
    "0.4 m, the ball moving on the inside of the loop. The minimum height above the bottom of the loop from which it "
    "must be released to go round the loop without losing contact with the track is:",
    place("1.0 m", ["0.8 m", "1.2 m", "2.0 m"], "D"),
    "Condition for looping the loop, with energy conservation",
    "At the top of the loop the normal force may at most fall to zero, so gravity alone supplies the centripetal "
    "force: v_top² ≥ gR. Energy conservation from the release point then gives the least release height.",
    ["At the top: v² = gR (minimum)", "mgh = mg(2R) + ½m(gR) → h = 2.5R", "h = 2.5 × 0.4 = 1.0 m"],
    why="0.8 m (2R) only reaches the top with zero speed, so the ball falls off before it gets there. 1.2 m (3R) "
        "and 2.0 m (5R) are larger than needed; 5R comes from confusing v² = 5gR at the bottom with a height.",
    ncert="Class 11 Physics, 'Work, Energy and Power', motion in a vertical circle", seconds=90, recomputed=True)

m, th, d = 2, math.radians(30), 5
muk = 1 / (2 * math.sqrt(3))
Fap = m * g * math.sin(th) + muk * m * g * math.cos(th)
Wap, Wg, Wf = Fap * d, -m * g * math.sin(th) * d, -muk * m * g * math.cos(th) * d
assert close(Fap, 15) and close(Wap, 75) and close(Wg, -50) and close(Wf, -25) and close(Wap + Wg + Wf, 0)
multi_key([close(Wap, 75), close(Wg, -50), close(Wf, -50), True, close(Wap + Wg + Wf, 75)], "abd")
add(T, "Work-energy theorem", "Advanced", "multi_statement",
    multi("A block of mass 2 kg is pulled at a constant speed through 5 m up a rough plane inclined at 30° to the "
          "horizontal, by a force parallel to the plane. The coefficient of kinetic friction is 1/(2√3). Take "
          "g = 10 m/s². Which of the following statements are correct?",
          ["The work done by the applied force is 75 J.",
           "The work done by gravity on the block is −50 J.",
           "The work done by friction on the block is −50 J.",
           "The work done by the normal reaction on the block is zero.",
           "The total work done by all the forces on the block is 75 J."]),
    place("(a), (b) and (d) only", ["(a), (c) and (d) only", "(b), (c) and (e) only", "(a), (b), (d) and (e) only"],
          "A"),
    "Work done by individual forces and the work-energy theorem",
    "At constant speed the change in kinetic energy is zero, so the total work by all forces is zero. The applied "
    "force balances gravity's component along the incline plus kinetic friction.",
    ["Height gained = 5 sin 30° = 2.5 m → W_gravity = −20 × 2.5 = −50 J (b true)",
     "Friction = μmg cos 30° = (1/(2√3)) × 20 × (√3/2) = 5 N → W_friction = −25 J (c false)",
     "Applied force = 10 + 5 = 15 N → W = 75 J (a true)",
     "Normal force ⟂ displacement → zero work (d true)", "Total work = 75 − 50 − 25 = 0 (e false)"],
    why="(c) takes friction equal to the gravity component; (e) forgets that constant speed means zero total work.",
    ncert="Class 11 Physics, 'Work, Energy and Power', work-energy theorem", seconds=150, recomputed=True)


# =====================================================================================================================
# Rotational Motion (B4 I5 A4)
# =====================================================================================================================
T = "Rotational Motion"

M_, R_, w_ = 2, 0.5, 10
I_disc = 0.5 * M_ * R_ ** 2
assert close(I_disc * w_, 2.5) and close(M_ * R_ ** 2 * w_, 5) and close(0.25 * M_ * R_ ** 2 * w_, 1.25)
assert close(M_ * R_ * w_, 10)
add(T, "Torque and angular momentum", "Basic", "numerical",
    "A uniform circular disc of mass 2 kg and radius 0.5 m rotates at 10 rad/s about the axis through its centre "
    "perpendicular to its plane. The magnitude of its angular momentum about this axis is:",
    place("2.5 kg m² s⁻¹", ["5 kg m² s⁻¹", "1.25 kg m² s⁻¹", "10 kg m² s⁻¹"], "C"),
    "Angular momentum of a rigid body about a fixed axis",
    "For rotation about a fixed axis, L = Iω. For a uniform disc about its own axis, I = ½MR².",
    ["I = ½ × 2 × 0.5² = 0.25 kg m²", "L = 0.25 × 10 = 2.5 kg m² s⁻¹"],
    why="5 uses MR² (a ring). 1.25 uses ¼MR², the disc's moment of inertia about a diameter. 10 multiplies M, R "
        "and ω, mixing up L with the momentum of a point mass at the rim.",
    ncert="Class 11 Physics, 'System of Particles and Rotational Motion', angular momentum in case of rotation about "
          "a fixed axis", seconds=35, recomputed=True)

load, d_load, d_eff = 400, 0.2, 0.8
effort = load * d_load / d_eff
assert effort == 100 and load * d_load / 1.0 == 80 and load * d_eff / d_load == 1600
add(T, "Equilibrium of rigid bodies", "Basic", "numerical",
    "A crowbar of length 1.0 m rests on a fulcrum 0.2 m from the end that is under a load of 400 N. Neglecting the "
    "weight of the crowbar, the least force that must be applied perpendicular to the bar at its other end to lift "
    "the load is:",
    place("100 N", ["1600 N", "400 N", "80 N"], "A"),
    "Principle of moments (lever)",
    "For a lever in equilibrium, the moments about the fulcrum balance: load × load arm = effort × effort arm. Here "
    "the load arm is 0.2 m and the effort arm is 1.0 − 0.2 = 0.8 m.",
    ["400 × 0.2 = F × 0.8", "F = 80/0.8 = 100 N (mechanical advantage 4)"],
    why="1600 N inverts the ratio of the arms. 400 N ignores the lever action. 80 N takes the whole length of the "
        "bar (1.0 m) as the effort arm.",
    ncert="Class 11 Physics, 'System of Particles and Rotational Motion', principle of moments", seconds=35,
    recomputed=True)

w_ = 2 * math.pi * 120 / 60
assert close(w_ * 0.3, 1.2 * math.pi) and close(2 * 0.3, 0.6) and close(120 * 0.3, 36)
add(T, "Rigid-body rotation", "Basic", "numerical",
    "A wheel of radius 0.3 m rotates about its fixed axle at 120 revolutions per minute. The linear speed of a point "
    "on its rim is:",
    place("1.2π m/s", ["0.6 m/s", "36 m/s", "2.4π m/s"], "D"),
    "Relation between linear and angular speed, v = ωr",
    "Convert the rate of rotation to rad/s first: 1 revolution = 2π rad. Every point of a rigid body rotating about "
    "a fixed axis has the same ω, and v = ωr for a point at distance r from the axis.",
    ["120 rev/min = 2 rev/s → ω = 4π rad/s", "v = 4π × 0.3 = 1.2π m/s (about 3.8 m/s)"],
    why="0.6 m/s uses 2 rev/s as if it were 2 rad/s. 36 m/s multiplies 120 rev/min by r without any conversion. "
        "2.4π m/s uses the diameter instead of the radius.",
    ncert="Class 11 Physics, 'System of Particles and Rotational Motion', angular velocity and its relation with "
          "linear velocity", seconds=35, recomputed=True)

add(T, "Moment of inertia and axis theorems", "Basic", "assertion_reason",
    AR_STEM.format(
        a="A thin uniform ring has a larger moment of inertia than a uniform disc of the same mass and radius, both "
          "about the axis through the centre perpendicular to the plane.",
        r="In the ring, all of the mass lies at the greatest distance R from this axis, while in the disc much of "
          "the mass lies closer to the axis."),
    ar("A"),
    "Moment of inertia depends on the distribution of mass about the axis",
    "I = Σmr². Moving mass farther from the axis raises I. The ring has I = MR², the disc only ½MR², because the "
    "disc's mass is spread from r = 0 to r = R.",
    ["Ring: every element at r = R → I = MR²", "Disc: elements from 0 to R → I = ½MR²",
     "R states exactly why the ring's I is larger → A"],
    why="Both statements are true, and R is the reason for A, so B, C and D are wrong.",
    ncert="Class 11 Physics, 'System of Particles and Rotational Motion', moment of inertia", seconds=40)

m1, m2, d_ = 1, 3, 8
xcm = (m1 * 0 + m2 * d_) / (m1 + m2)
assert xcm == 6
add(T, "Centre of mass", "Intermediate", "numerical",
    "Two particles of masses 1 kg and 3 kg are initially at rest, 8 m apart, in free space. They move towards each "
    "other only because of their mutual gravitational attraction. When they collide, the distance moved by the "
    "1 kg particle is:",
    place("6 m", ["2 m", "4 m", "8 m"], "B"),
    "Centre of mass stays at rest when only internal forces act",
    "The mutual attraction is an internal force of the two-particle system, and no external force acts. The centre "
    "of mass, at rest initially, stays at rest, so the particles meet there.",
    ["Place 1 kg at x = 0 and 3 kg at x = 8 m", "x_cm = (1 × 0 + 3 × 8)/4 = 6 m",
     "The 1 kg particle moves 6 m (the 3 kg one moves 2 m)"],
    why="2 m is the distance moved by the 3 kg particle. 4 m assumes they meet at the midpoint, as for equal masses. "
        "8 m assumes the heavier particle stays fixed.",
    ncert="Class 11 Physics, 'System of Particles and Rotational Motion', motion of centre of mass", seconds=50,
    recomputed=True)

m, a_ = 0.5, 0.2
I_diag = 2 * m * (a_ / math.sqrt(2)) ** 2
I_side = 2 * m * a_ ** 2
I_corner = m * (a_ ** 2 + a_ ** 2 + 2 * a_ ** 2)
assert close(I_diag, 0.02) and close(I_side, 0.04) and close(I_corner, 0.08)
add(T, "Moment of inertia and axis theorems", "Intermediate", "numerical",
    "Four small balls, each of mass 0.5 kg, are fixed at the corners of a light square frame of side 0.2 m. The "
    "moment of inertia of the system about an axis along one diagonal of the square is:",
    place("0.02 kg m²", ["0.04 kg m²", "0.08 kg m²", "0.01 kg m²"], "D"),
    "Moment of inertia of a system of point masses",
    "I = Σmr², where r is each ball's perpendicular distance from the axis. The two balls on the diagonal lie on the "
    "axis (r = 0); the other two are at half the length of the other diagonal, a/√2.",
    ["r = 0.2/√2 m → r² = 0.02 m²", "I = 2 × 0.5 × 0.02 = 0.02 kg m²"],
    why="0.04 kg m² is the moment of inertia about a side (or about the perpendicular axis through the centre). "
        "0.08 kg m² is about the perpendicular axis through a corner. 0.01 kg m² counts only one ball.",
    ncert="Class 11 Physics, 'System of Particles and Rotational Motion', moment of inertia", seconds=60,
    recomputed=True)

add(T, "Moment of inertia and axis theorems", "Intermediate", "direct",
    "Two uniform circular discs have the same mass and the same thickness. One is made of iron and the other of "
    "aluminium (aluminium is less dense than iron). About the axis through the centre perpendicular to the plane:",
    place("the aluminium disc has the larger moment of inertia",
          ["the iron disc has the larger moment of inertia",
           "both discs have the same moment of inertia, since their masses are equal",
           "the ratio of their moments of inertia equals the ratio of their densities"],
          "C"),
    "Moment of inertia depends on size, not only on mass",
    "Same mass and thickness means the less dense aluminium disc must have a larger area, i.e. a larger radius. "
    "Since I = ½MR² for each disc, the larger radius gives the larger moment of inertia.",
    ["M = ρ(πR²)t, with M and t equal → R² ∝ 1/ρ", "ρ_Al < ρ_Fe → R_Al > R_Fe", "I = ½MR² → I_Al > I_Fe"],
    why="The other options ignore that, for equal mass, the less dense material forms a wider disc with its mass "
        "farther from the axis. In fact I ∝ R² ∝ 1/ρ, so the ratio of the moments of inertia is the inverse "
        "ratio of the densities.",
    ncert="Class 11 Physics, 'System of Particles and Rotational Motion', moment of inertia", seconds=50)

add(T, "Equilibrium of rigid bodies", "Intermediate", "match_list",
    match_stem("A rigid body, initially at rest in free space, is acted on only by the forces described in List-I. "
               "Match List-I (forces) with List-II (resulting motion).",
               ["Two equal and opposite forces acting along the same line",
                "Two equal and opposite forces whose lines of action are different (a couple)",
                "A single force whose line of action passes through the centre of mass",
                "A single force whose line of action does not pass through the centre of mass"],
               ["Both translation and rotation", "Rotation without translation", "Translation without rotation",
                "Neither translation nor rotation"]),
    match_options({"A": "IV", "B": "II", "C": "III", "D": "I"},
                  [{"A": "II", "B": "IV", "C": "III", "D": "I"}, {"A": "IV", "B": "III", "C": "II", "D": "I"},
                   {"A": "IV", "B": "II", "C": "I", "D": "III"}], "B"),
    "Translational and rotational equilibrium",
    "Translation is decided by the net force, rotation by the net torque. Two equal and opposite forces give zero "
    "net force; their torque is zero only if they share a line of action. A single force always gives a net force; "
    "it gives a torque about the centre of mass only if its line misses the centre of mass.",
    ["A: ΣF = 0, Στ = 0 → IV", "B: ΣF = 0, Στ ≠ 0 → II", "C: ΣF ≠ 0, Στ about CM = 0 → III",
     "D: ΣF ≠ 0, Στ ≠ 0 → I"],
    why="The other codes swap the effects of a couple and of a single force through the centre of mass, or of the "
        "two cases of a single force.",
    ncert="Class 11 Physics, 'System of Particles and Rotational Motion', equilibrium of a rigid body and couple",
    seconds=50)

I_, tau, t_ = 0.5, 2, 5
alpha = tau / I_
w5 = alpha * t_
th5 = 0.5 * alpha * t_ ** 2
K5 = 0.5 * I_ * w5 ** 2
L5 = I_ * w5
assert alpha == 4 and w5 == 20 and th5 == 50 and K5 == 100 and L5 == 10 and tau * th5 == K5
multi_key([alpha == 4, w5 == 20, th5 == 100, K5 == 100, L5 == 10], "abde")
add(T, "Rigid-body rotation", "Intermediate", "multi_statement",
    multi("A wheel whose moment of inertia about its fixed axle is 0.5 kg m² starts from rest. A constant torque of "
          "2 N m acts on it about the axle for 5 s. Neglecting friction, which of the following statements are "
          "correct?",
          ["Its angular acceleration is 4 rad/s².",
           "Its angular velocity at the end of 5 s is 20 rad/s.",
           "It turns through 100 rad in the 5 s.",
           "Its rotational kinetic energy at the end of 5 s is 100 J.",
           "Its angular momentum about the axle at the end of 5 s is 10 kg m² s⁻¹."]),
    place("(a), (b), (d) and (e) only", ["(a), (b) and (c) only", "(a), (c), (d) and (e) only",
                                         "(b), (d) and (e) only"], "D"),
    "Rotation with constant angular acceleration",
    "τ = Iα gives a constant α, after which the equations of rotational kinematics apply exactly as their linear "
    "counterparts do.",
    ["(a) α = 2/0.5 = 4 rad/s² (true)", "(b) ω = 4 × 5 = 20 rad/s (true)",
     "(c) θ = ½ × 4 × 25 = 50 rad, not 100 rad (false)", "(d) K = ½ × 0.5 × 400 = 100 J (true; = τθ)",
     "(e) L = 0.5 × 20 = 10 kg m² s⁻¹ (true; = τt)"],
    why="(c) drops the ½ in θ = ½αt²; every option that includes (c) or leaves out (a) is wrong.",
    ncert="Class 11 Physics, 'System of Particles and Rotational Motion', kinematics and dynamics of rotational "
          "motion about a fixed axis", seconds=100, recomputed=True)

m1, m2, Mp = 3, 1, 4
acc = (m1 - m2) * g / (m1 + m2 + Mp / 2)
assert close(acc, 10 / 3) and (m1 - m2) * g / (m1 + m2) == 5 and (m1 - m2) * g / (m1 + m2 + Mp) == 2.5
assert (m1 - m2) * g / (Mp / 2) == 10
add(T, "Rigid-body rotation", "Advanced", "numerical",
    "Blocks of masses 3 kg and 1 kg hang at the two ends of a light string that passes over a pulley in the form of "
    "a uniform disc of mass 4 kg, which rotates without friction about a fixed horizontal axle through its centre. "
    "The string does not slip on the pulley. Taking g = 10 m/s², the magnitude of the acceleration of the blocks is:",
    place("10/3 m/s²", ["5 m/s²", "2.5 m/s²", "10 m/s²"], "A"),
    "Coupled translation and rotation (pulley with moment of inertia)",
    "Because the pulley has a moment of inertia, the tensions on the two sides differ. Their difference supplies "
    "the torque Iα, with a = αr since the string does not slip.",
    ["3g − T₁ = 3a; T₂ − 1g = 1a", "(T₁ − T₂)r = ½Mr² × (a/r) → T₁ − T₂ = ½Ma = 2a",
     "Adding: 2g = (3 + 1 + 2)a → a = 20/6 = 10/3 m/s²"],
    why="5 m/s² treats the pulley as massless. 2.5 m/s² takes the pulley's moment of inertia as Mr² (a ring). "
        "10 m/s² leaves out the masses of the blocks from the inertia.",
    ncert="Class 11 Physics, 'System of Particles and Rotational Motion', dynamics of rotational motion about a "
          "fixed axis", seconds=120, recomputed=True)

I1, w1, I2, w2 = 2, 10, 3, -5
wc = (I1 * w1 + I2 * w2) / (I1 + I2)
Ki = 0.5 * I1 * w1 ** 2 + 0.5 * I2 * w2 ** 2
Kf = 0.5 * (I1 + I2) * wc ** 2
assert wc == 1 and Ki == 137.5 and Kf == 2.5 and Ki - Kf == 135
assert Ki - 0.5 * (I1 + I2) * ((I1 * w1 - I2 * w2) / (I1 + I2)) ** 2 == 15
add(T, "Torque and angular momentum", "Advanced", "numerical",
    "Two discs rotate about the same fixed axle without friction. Disc P (moment of inertia 2 kg m²) spins at "
    "10 rad/s, and disc Q (moment of inertia 3 kg m²) spins at 5 rad/s in the opposite sense. They are brought "
    "into contact along the axle and soon rotate together. The kinetic energy lost in the process is:",
    place("135 J", ["15 J", "137.5 J", "2.5 J"], "C"),
    "Conservation of angular momentum with opposite senses of rotation",
    "Only internal torques (friction between the discs) act, so the total angular momentum about the axle is "
    "conserved. Angular momenta in opposite senses must be given opposite signs.",
    ["L = 2 × 10 + 3 × (−5) = 5 kg m² s⁻¹", "Common ω = 5/(2 + 3) = 1 rad/s (in P's sense)",
     "K_initial = ½ × 2 × 100 + ½ × 3 × 25 = 137.5 J", "K_final = ½ × 5 × 1² = 2.5 J", "Loss = 135 J"],
    why="15 J treats both discs as spinning in the same sense (common ω = 7 rad/s). 137.5 J assumes the discs stop. "
        "2.5 J is the kinetic energy left, not the energy lost.",
    ncert="Class 11 Physics, 'System of Particles and Rotational Motion', conservation of angular momentum",
    seconds=100, recomputed=True)

M_, L_ = 1.0, 1.0
alpha0 = (M_ * g * L_ / 2) / (M_ * L_ ** 2 / 3)
a_cm = alpha0 * L_ / 2
N_h = M_ * g - M_ * a_cm
assert close(a_cm, 0.75 * g) and close(N_h, 0.25 * M_ * g)
add(T, "Rigid-body rotation", "Advanced", "assertion_reason",
    AR_STEM.format(
        a="A uniform rod, hinged at one end so that it can turn freely in a vertical plane, is held horizontal and "
          "released. Just after release, the upward force exerted by the hinge on the rod is less than the weight "
          "of the rod.",
        r="Just after release, the centre of mass of the rod has a downward acceleration."),
    ar("A"),
    "Hinge reaction on a rotating rod",
    "Just after release the rod has no angular velocity, so the only acceleration of its centre of mass is the "
    "tangential one, downward. Newton's second law for the centre of mass, Mg − N = Ma_cm, then makes N less than "
    "Mg. With α = 3g/2L from τ = Iα (I = ML²/3), a_cm = 3g/4 and N = Mg/4.",
    ["τ = Mg(L/2) = (ML²/3)α → α = 3g/(2L)", "a_cm = α(L/2) = 3g/4 (downward)",
     "Mg − N = M(3g/4) → N = Mg/4 < Mg"],
    why="R is exactly the reason the hinge force falls below the weight, so B is wrong; both statements are true, so "
        "C and D are wrong.",
    ncert="Class 11 Physics, 'System of Particles and Rotational Motion', motion of centre of mass and dynamics of "
          "rotational motion", seconds=90, recomputed=True)

Wb, Wl, Lb, d_rope = 500, 250, 6, 2
Tr = (Wb * Lb / 2 + Wl * Lb) / d_rope
V = Wb + Wl - Tr
assert Tr == 1500 and V == -750
Tr2 = (Wb * Lb / 2) / d_rope
assert Wb - Tr2 == -250
add(T, "Equilibrium of rigid bodies", "Advanced", "numerical",
    "A uniform horizontal beam of length 6 m and mass 50 kg is hinged at one end to a wall. It is held horizontal by "
    "a vertical rope tied to the beam 2 m from the hinge, and a load of mass 25 kg hangs from the free end of the "
    "beam. Taking g = 10 m/s², the vertical force exerted by the hinge on the beam is:",
    place("750 N, directed downward", ["750 N, directed upward", "1500 N, directed upward",
                                       "250 N, directed downward"], "B"),
    "Conditions of equilibrium: forces and moments",
    "Take moments about the hinge to find the rope tension (the hinge force then has no moment). The vertical forces "
    "must then add to zero. Because the rope is attached inside the length of the beam, it must pull up with more "
    "than the total weight, and the hinge must pull the beam down.",
    ["Moments about the hinge: T × 2 = 500 × 3 + 250 × 6 = 3000 → T = 1500 N",
     "Vertical: V + 1500 = 500 + 250 → V = −750 N", "The hinge pulls the beam down with 750 N"],
    why="'Upward' assumes the hinge must support the beam. 1500 N upward is the rope tension. 250 N downward "
        "forgets the load's moment when finding the tension.",
    ncert="Class 11 Physics, 'System of Particles and Rotational Motion', equilibrium of a rigid body", seconds=120,
    recomputed=True)


# =====================================================================================================================
# Gravitation (B3 I4 A3)
# =====================================================================================================================
T = "Gravitation"

G = 6.67e-11
E_ = G * 10 / 2 ** 2
assert round(E_ / 1e-10, 2) == 1.67 and round(G * 10 / 2 / 1e-10, 1) == 3.3 and close(G * 10, 6.67e-10)
add(T, "Law of gravitation", "Basic", "numerical",
    "Taking G = 6.67 × 10⁻¹¹ N m² kg⁻², the magnitude of the gravitational field intensity at a distance of 2 m from "
    "a point mass of 10 kg is about:",
    place("1.67 × 10⁻¹⁰ N kg⁻¹", ["3.3 × 10⁻¹⁰ N kg⁻¹", "6.67 × 10⁻¹⁰ N kg⁻¹", "1.67 × 10⁻¹¹ N kg⁻¹"], "D"),
    "Gravitational field of a point mass",
    "The gravitational field intensity is the force per unit mass on a test mass: E = GM/r².",
    ["E = 6.67 × 10⁻¹¹ × 10/2²", "= 1.67 × 10⁻¹⁰ N kg⁻¹"],
    why="3.3 × 10⁻¹⁰ divides by r instead of r². 6.67 × 10⁻¹⁰ leaves out the distance. 1.67 × 10⁻¹¹ slips a "
        "power of ten.",
    ncert="Class 11 Physics, 'Gravitation', universal law of gravitation", seconds=35, recomputed=True)

r1, r2 = 1, 4
assert math.sqrt(r2 / r1) == 2
add(T, "Escape and orbital velocity", "Basic", "numerical",
    "Two satellites revolve round the Earth in circular orbits of radii r and 4r. The ratio of the orbital speed of "
    "the inner satellite to that of the outer satellite is:",
    place("2 : 1", ["1 : 2", "4 : 1", "1 : 4"], "B"),
    "Orbital speed and orbital radius",
    "Gravity supplies the centripetal force: GMm/r² = mv²/r, so v = √(GM/r). The orbital speed falls as the "
    "square root of the radius grows.",
    ["v ∝ 1/√r", "v_inner/v_outer = √(4r/r) = 2"],
    why="1 : 2 inverts the ratio. 4 : 1 takes v ∝ 1/r. 1 : 4 takes v ∝ r.",
    ncert="Class 11 Physics, 'Gravitation', earth satellites", seconds=30, recomputed=True)

gs, Rs = 10, 6.4e6
V_s = -gs * Rs
assert close(V_s, -6.4e7) and close(-gs * 6.4e3, -6.4e4)
add(T, "Gravitational potential and energy", "Basic", "numerical",
    "Treat the Earth as a uniform sphere of radius 6400 km with g = 10 m/s² at its surface, and take the "
    "gravitational potential to be zero at infinity. The gravitational potential at the Earth's surface is:",
    place("−6.4 × 10⁷ J kg⁻¹", ["+6.4 × 10⁷ J kg⁻¹", "−6.4 × 10⁴ J kg⁻¹", "−3.2 × 10⁷ J kg⁻¹"], "C"),
    "Gravitational potential at the surface in terms of g",
    "V = −GM/R, and since g = GM/R², GM/R = gR. So V = −gR at the surface.",
    ["V = −gR = −10 × 6.4 × 10⁶", "= −6.4 × 10⁷ J kg⁻¹"],
    why="The positive value ignores that gravitational potential is negative (taken zero at infinity). "
        "−6.4 × 10⁴ uses R in km. −3.2 × 10⁷ brings in a spurious factor ½.",
    ncert="Class 11 Physics, 'Gravitation', gravitational potential energy",
    seconds=35, recomputed=True)

add(T, "Gravitational potential and energy", "Intermediate", "statement_pair",
    SP_STEM.format(
        s1="Inside a uniform thin spherical shell, the gravitational potential due to the shell is the same at "
           "every point and equals its value at the surface of the shell.",
        s2="At the centre of a uniform solid sphere, the gravitational field and the gravitational potential due to "
           "the sphere are both zero (potential taken as zero at infinity)."),
    sp("C"),
    "Field and potential inside spherical mass distributions",
    "Inside a uniform shell the gravitational force (field) is zero, so no work is done in moving a test mass "
    "around inside it: the potential is constant and equal to its surface value, −GM/R. At the centre of a solid "
    "sphere the field is zero by symmetry, but the potential is not zero: work must be done to take a mass from the "
    "centre out to infinity, so the potential there is negative (indeed lower than at the surface).",
    ["Shell: E = 0 inside → V constant = −GM/R (Statement I true)",
     "Solid sphere: E = 0 at centre, but V(centre) < V(surface) < 0 (Statement II false)"],
    why="Statement II wrongly concludes zero potential from zero field; a zero field only means the potential has no "
        "slope there.",
    ncert="Class 11 Physics, 'Gravitation', gravitational potential energy and the shell theorem", seconds=60)

ratio = 1 / 0.99 ** 2
assert round((ratio - 1) * 100, 1) == 2.0
add(T, "Variation of g", "Intermediate", "numerical",
    "If the radius of the Earth were to shrink by 1% while its mass stayed the same, the acceleration due to "
    "gravity at its surface would:",
    place("increase by about 2%", ["decrease by about 2%", "increase by about 1%", "remain unchanged"], "A"),
    "Dependence of g on the radius for a fixed mass",
    "g = GM/R². With M fixed, g ∝ R⁻², so for a small change Δg/g = −2ΔR/R.",
    ["ΔR/R = −1%", "Δg/g = −2 × (−1%) = +2% (exactly 1/0.99² = 1.0203)"],
    why="'Decrease' gets the sign wrong: a smaller radius brings the surface closer to the centre. 1% ignores the "
        "square. 'Unchanged' would hold only if g depended on mass alone.",
    ncert="Class 11 Physics, 'Gravitation', acceleration due to gravity of the earth", seconds=45, recomputed=True)

add(T, "Satellite energy and period", "Intermediate", "assertion_reason",
    AR_STEM.format(
        a="A satellite in a circular orbit round the Earth has kinetic energy K. The least additional energy that "
          "must be given to it to make it escape from the Earth's gravity is K.",
        r="The total mechanical energy of a satellite in a circular orbit is −K, where K is its kinetic energy."),
    ar("A"),
    "Energy of an orbiting satellite and the energy to escape",
    "For a circular orbit, K = GMm/2r and U = −GMm/r, so the total energy is −GMm/2r = −K. To escape, the total "
    "energy must be raised to at least zero, so at least K must be added.",
    ["K = GMm/(2r), U = −2K", "E = K + U = −K", "Energy to reach E = 0: ΔE = K"],
    why="R gives the satellite's total energy, which is exactly what fixes the escape energy in A, so B is wrong.",
    ncert="Class 11 Physics, 'Gravitation', energy of an orbiting satellite", seconds=50)

U3 = 3 * G * 1 * 1 / 1
assert round(U3 / 1e-10, 1) == 2.0 and round(2 * G / 1e-10, 2) == 1.33 and round(6 * G / 1e-10, 1) == 4.0
add(T, "Gravitational potential and energy", "Intermediate", "numerical",
    "Three point masses, each of 1 kg, are placed at the corners of an equilateral triangle of side 1 m. Taking "
    "G = 6.67 × 10⁻¹¹ N m² kg⁻², the minimum work needed to separate them to infinite distances from one another is "
    "about:",
    place("2.0 × 10⁻¹⁰ J", ["6.67 × 10⁻¹¹ J", "1.33 × 10⁻¹⁰ J", "4.0 × 10⁻¹⁰ J"], "B"),
    "Potential energy of a system of particles",
    "The potential energy of a system of point masses is the sum over every distinct pair of −Gmᵢmⱼ/rᵢⱼ. Three "
    "masses form three pairs. The work needed to pull them apart slowly equals −U.",
    ["U = −3 × G × 1 × 1/1 = −3G", "W = −U = 3 × 6.67 × 10⁻¹¹ ≈ 2.0 × 10⁻¹⁰ J"],
    why="6.67 × 10⁻¹¹ J counts one pair. 1.33 × 10⁻¹⁰ J counts two pairs. 4.0 × 10⁻¹⁰ J counts each pair twice.",
    ncert="Class 11 Physics, 'Gravitation', gravitational potential energy", seconds=50, recomputed=True)

Rp, rho_p = 3.0e6, 5000.0
Mp_ = rho_p * 4 / 3 * math.pi * Rp ** 3
Tp = 2 * math.pi * math.sqrt(Rp ** 3 / (G * Mp_))
assert close(3 * math.pi / (G * Tp ** 2), rho_p)
add(T, "Satellite energy and period", "Advanced", "direct",
    "A satellite revolves round a planet in a circular orbit just above the planet's surface, with period T. "
    "Treating the planet as a uniform sphere and G as the universal gravitational constant, the mean density of the "
    "planet is:",
    place("3π/(GT²)", ["4π²/(GT²)", "3/(4πGT²)", "GT²/(3π)"], "D"),
    "Density of a planet from the period of a close satellite",
    "For an orbit of radius R (just above the surface), T² = 4π²R³/(GM). Writing M = ρ(4/3)πR³ makes R cancel, so "
    "the period of a close satellite depends only on the planet's density.",
    ["T² = 4π²R³/(G ρ (4/3)πR³) = 3π/(Gρ)", "ρ = 3π/(GT²)"],
    why="4π²/(GT²) forgets the volume factor (4/3)π. 3/(4πGT²) mishandles π. GT²/(3π) inverts the result and does "
        "not even have the dimensions of density.",
    ncert="Class 11 Physics, 'Gravitation', earth satellites (period of a satellite)", seconds=90, recomputed=True)

ve = 11.2
k_r, k_rho = 2, 0.5
ve_p = ve * k_r * math.sqrt(k_rho)
assert close(ve_p, 11.2 * math.sqrt(2)) and round(ve_p, 1) == 15.8
add(T, "Escape and orbital velocity", "Advanced", "numerical",
    "The escape speed from the Earth's surface is 11.2 km/s. A planet has twice the radius of the Earth and half its "
    "mean density. The escape speed from the surface of this planet is about:",
    place("15.8 km/s", ["11.2 km/s", "22.4 km/s", "7.9 km/s"], "C"),
    "Escape speed in terms of radius and density",
    "vₑ = √(2GM/R) with M = ρ(4/3)πR³ gives vₑ = R√(8πGρ/3), so vₑ ∝ R√ρ.",
    ["vₑ ∝ R√ρ", "Ratio = 2 × √(1/2) = √2", "vₑ = 11.2 × 1.414 ≈ 15.8 km/s"],
    why="11.2 km/s notices that g = (4/3)πGρR is unchanged but forgets that vₑ = √(2gR) also grows with R. "
        "22.4 km/s ignores the change of density. 7.9 km/s divides by √2 instead of multiplying.",
    ncert="Class 11 Physics, 'Gravitation', escape speed", seconds=90, recomputed=True)

m, R = 100, 6.4e6
E_need = (-(m * g * R) / (2 * 2)) - (-(m * g * R))
assert close(E_need, 4.8e9) and close(m * g * R / 2, 3.2e9) and close(m * g * R / 4, 1.6e9)
add(T, "Satellite energy and period", "Advanced", "numerical",
    "A satellite of mass 100 kg is to be placed in a circular orbit at a height above the Earth's surface equal to "
    "the Earth's radius R = 6400 km. Taking g = 10 m/s² at the surface and neglecting the Earth's rotation and air "
    "resistance, the minimum energy that must be supplied to it, starting from rest on the surface, is:",
    place("4.8 × 10⁹ J", ["3.2 × 10⁹ J", "6.4 × 10⁹ J", "1.6 × 10⁹ J"], "B"),
    "Energy to put a satellite into orbit",
    "The energy supplied equals the satellite's total energy in orbit minus its energy at rest on the surface. In an "
    "orbit of radius r = 2R, E = −GMm/(2r) = −GMm/(4R); on the surface (at rest), E = −GMm/R. Use GM = gR².",
    ["E_orbit = −mgR/4", "E_surface = −mgR", "Energy needed = mgR − mgR/4 = (3/4)mgR",
     "= 0.75 × 100 × 10 × 6.4 × 10⁶ = 4.8 × 10⁹ J"],
    why="3.2 × 10⁹ J is only the gain in potential energy (mgR/2), with no kinetic energy for orbiting. 6.4 × 10⁹ J "
        "is mgR, the energy to escape from rest. 1.6 × 10⁹ J is only the kinetic energy in orbit.",
    ncert="Class 11 Physics, 'Gravitation', energy of an orbiting satellite", seconds=100, recomputed=True)


# =====================================================================================================================
# Properties of Solids and Liquids (B5 I6 A4)
# =====================================================================================================================
T = "Properties of Solids and Liquids"

P0, rho_w = 1.0e5, 1000
h_w = P0 / (rho_w * g)
assert h_w == 10
add(T, "Fluid pressure and Pascal's law", "Basic", "numerical",
    "If water (density 1000 kg/m³) were used instead of mercury in a simple barometer, the height of the water "
    "column supported by an atmospheric pressure of 1.0 × 10⁵ Pa would be (g = 10 m/s²):",
    place("10 m", ["0.76 m", "1 m", "100 m"], "D"),
    "Pressure of a liquid column",
    "The atmosphere supports a liquid column whose pressure hρg equals the atmospheric pressure. A less dense liquid "
    "needs a taller column.",
    ["hρg = P₀ → h = P₀/(ρg)", "h = 1.0 × 10⁵/(1000 × 10) = 10 m"],
    why="0.76 m is the height of a mercury barometer. 1 m and 100 m are slips by a factor of 10 in ρg.",
    ncert="Class 11 Physics, 'Mechanical Properties of Fluids', atmospheric pressure and gauge pressure",
    seconds=30, recomputed=True)

add(T, "Thermal expansion and calorimetry", "Basic", "direct",
    "A thin uniform metal plate has a circular hole cut in it. When the plate is heated uniformly, the diameter of the "
    "hole:",
    place("increases", ["decreases", "remains unchanged",
                        "increases or decreases depending on the size of the hole"], "B"),
    "Thermal expansion of a plate with a hole",
    "On uniform heating every linear dimension of the plate grows by the same fraction αΔT, just as in a "
    "photographic enlargement. The hole expands exactly as a disc of the same metal filling it would.",
    ["All lengths → (1 + αΔT) × length", "The hole's diameter is such a length → it increases"],
    why="The metal does not expand 'into' the hole; every distance between points of the plate, including across "
        "the hole, grows by the same fraction, whatever the hole's size.",
    ncert="Class 11 Physics, 'Thermal Properties of Matter', thermal expansion", seconds=30)

tF = 9 / 5 * 50 + 32
assert tF == 122 and 9 / 5 * 50 == 90 and round(5 / 9 * 50 + 32, 1) == 59.8
add(T, "Thermal expansion and calorimetry", "Basic", "numerical",
    "A temperature of 50 °C, expressed on the Fahrenheit scale, is:",
    place("122 °F", ["90 °F", "82 °F", "59.8 °F"], "A"),
    "Relation between the Celsius and Fahrenheit scales",
    "The ice and steam points are 0 °C and 32 °F, and 100 °C and 212 °F. So t_F − 32 = (180/100) t_C, i.e. "
    "t_F = (9/5)t_C + 32.",
    ["t_F = (9/5) × 50 + 32", "= 90 + 32 = 122 °F"],
    why="90 °F forgets to add 32. 82 °F only adds 32. 59.8 °F uses the factor 5/9 instead of 9/5.",
    ncert="Class 11 Physics, 'Thermal Properties of Matter', temperature and heat (measurement of temperature)",
    seconds=30, recomputed=True)

b_w, lam = 2.88e-3, 480e-9
assert close(b_w / lam, 6000) and round(b_w * lam / 1e-9, 1) == 1.4
add(T, "Heat transfer", "Basic", "numerical",
    "The spectrum of the Sun's radiation has its maximum intensity at a wavelength of about 480 nm. Treating the Sun "
    "as a black body and taking Wien's constant as 2.88 × 10⁻³ m K, the temperature of its surface is about:",
    place("6000 K", ["600 K", "1.4 × 10⁻⁹ K", "60 000 K"], "C"),
    "Wien's displacement law",
    "Wien's law states λₘT = b: the wavelength of maximum emission times the absolute temperature is a constant.",
    ["T = b/λₘ = 2.88 × 10⁻³/(480 × 10⁻⁹)", "= 6.0 × 10³ K"],
    why="600 K and 60 000 K slip the power of ten in 480 nm = 4.8 × 10⁻⁷ m. 1.4 × 10⁻⁹ K multiplies b by λₘ "
        "instead of dividing.",
    ncert="Class 11 Physics, 'Thermal Properties of Matter', blackbody radiation (Wien's displacement law)",
    seconds=35, recomputed=True)

add(T, "Thermal expansion and calorimetry", "Basic", "assertion_reason",
    AR_STEM.format(
        a="A metal lid that is stuck tight on a glass jar can often be loosened by pouring hot water over the lid.",
        r="For the same rise in temperature, the metal of the lid expands more than the glass of the jar, because "
          "its coefficient of thermal expansion is larger."),
    ar("A"),
    "Differential thermal expansion",
    "Heating the lid makes it expand. Since the metal's coefficient of expansion is larger than that of glass, the "
    "lid grows more than the neck of the jar and the grip loosens.",
    ["Δd = αdΔT for each", "α_metal > α_glass → the lid's diameter grows more than the neck's → A, explained by R"],
    why="Both statements are true and R is the reason the lid loosens, so B, C and D are wrong.",
    ncert="Class 11 Physics, 'Thermal Properties of Matter', thermal expansion", seconds=35)

B_s, depth = 1.0e11, 1000
frac = rho_w * g * depth / B_s
assert close(frac, 1e-4)
add(T, "Elasticity and moduli", "Intermediate", "numerical",
    "A solid metal sphere of bulk modulus 1.0 × 10¹¹ N/m² is lowered from the surface of the sea to a depth of "
    "1000 m. Taking the density of sea water as 1000 kg/m³ and g = 10 m/s², the fractional decrease in its volume is:",
    place("0.01%", ["0.1%", "1%", "0.001%"], "B"),
    "Hydraulic stress and bulk modulus",
    "The extra pressure at a depth h is hρg (the atmospheric pressure acts at the surface as well, so it cancels in "
    "the change). Bulk modulus B = Δp/(ΔV/V), so ΔV/V = Δp/B.",
    ["Δp = 1000 × 10 × 1000 = 1.0 × 10⁷ Pa", "ΔV/V = 10⁷/10¹¹ = 10⁻⁴ = 0.01%"],
    why="0.1%, 1% and 0.001% are slips by powers of ten in Δp or in converting 10⁻⁴ into a percentage.",
    ncert="Class 11 Physics, 'Mechanical Properties of Solids', bulk modulus", seconds=50, recomputed=True)

pg, hh = 3.0e4, 2.0
v_eff = math.sqrt(2 * (pg / rho_w + g * hh))
assert close(v_eff, 10) and round(math.sqrt(2 * g * hh), 1) == 6.3
assert round(math.sqrt(2 * pg / rho_w), 1) == 7.7 and round(math.sqrt(pg / rho_w + 2 * g * hh), 1) == 8.4
add(T, "Bernoulli's principle", "Intermediate", "numerical",
    "A large closed tank contains water (density 1000 kg/m³). The air above the water is at a pressure "
    "3.0 × 10⁴ Pa above atmospheric pressure. Water flows out into the atmosphere through a small hole in the side "
    "of the tank, 2.0 m below the water surface. Taking g = 10 m/s², the speed of efflux is:",
    place("10 m/s", ["about 6.3 m/s", "about 7.7 m/s", "about 8.4 m/s"], "A"),
    "Bernoulli's principle for efflux from a pressurised tank",
    "Apply Bernoulli's equation between the water surface (speed ≈ 0 in a large tank, pressure P₀ + p) and the jet "
    "at the hole (pressure P₀). Both the excess pressure and the depth drive the flow.",
    ["(P₀ + p) + ρgh = P₀ + ½ρv²", "v² = 2(p/ρ + gh) = 2(30 + 20) = 100", "v = 10 m/s"],
    why="About 6.3 m/s uses Torricelli's √(2gh) and ignores the excess air pressure. About 7.7 m/s ignores the "
        "depth. About 8.4 m/s forgets to double the pressure term.",
    ncert="Class 11 Physics, 'Mechanical Properties of Fluids', Bernoulli's principle (speed of efflux)", seconds=75,
    recomputed=True)

r_b, eta = 1.5e-3, 0.5
vt = 2 * r_b ** 2 * (rho_w - 0) * g / (9 * eta)
assert close(vt, 0.01) and close(r_b ** 2 * rho_w * g / eta, 0.045)
add(T, "Viscosity and Stokes' law", "Intermediate", "numerical",
    "A small air bubble of radius 1.5 mm rises slowly through a liquid of density 1000 kg/m³ and coefficient of "
    "viscosity 0.5 Pa s. Neglecting the density of air, taking g = 10 m/s² and assuming Stokes' law holds, its "
    "terminal velocity is:",
    place("1 cm/s, upward", ["1 cm/s, downward", "4.5 cm/s, upward", "0.5 cm/s, upward"], "C"),
    "Terminal velocity when the body is lighter than the fluid",
    "The terminal velocity is v = 2r²(ρ − σ)g/(9η), where ρ is the density of the body and σ that of the fluid. For "
    "a bubble ρ ≈ 0, so v is negative: the bubble moves upward, with buoyancy balanced by weight (negligible) plus "
    "the downward viscous drag.",
    ["|v| = 2 × (1.5 × 10⁻³)² × 1000 × 10/(9 × 0.5)", "= 0.045/4.5 = 0.01 m/s = 1 cm/s, upward"],
    why="'Downward' ignores that the bubble is lighter than the liquid. 4.5 cm/s leaves out the factor 2/9. "
        "0.5 cm/s uses 1/9 instead of 2/9.",
    ncert="Class 11 Physics, 'Mechanical Properties of Fluids', Stokes' law (terminal velocity)", seconds=75,
    recomputed=True)

r_r, S_w = 0.02, 0.07
F_ring = 2 * (2 * math.pi * r_r) * S_w
assert close(F_ring, 5.6e-3 * math.pi)
add(T, "Surface tension and capillarity", "Intermediate", "numerical",
    "A thin horizontal wire ring of radius 2 cm rests on the surface of water (surface tension 0.07 N/m, angle of "
    "contact 0°). Neglecting the weight of the ring, the extra force needed to pull it vertically off the surface is "
    "about:",
    place("5.6π × 10⁻³ N", ["2.8π × 10⁻³ N", "1.4π × 10⁻³ N", "11.2π × 10⁻³ N"], "D"),
    "Force of surface tension on a ring with two contact lines",
    "As the ring is lifted, a film of water clings to it along both its inner and its outer edge. Surface tension "
    "pulls down along each edge, so the total length in contact is twice the circumference.",
    ["Contact length = 2 × 2πr = 2 × 2π × 0.02 = 0.08π m", "F = S × length = 0.07 × 0.08π = 5.6π × 10⁻³ N"],
    why="2.8π × 10⁻³ N counts only one edge. 1.4π × 10⁻³ N uses πr instead of 2πr for one edge. 11.2π × 10⁻³ N "
        "counts each edge twice.",
    ncert="Class 11 Physics, 'Mechanical Properties of Fluids', surface tension", seconds=60, recomputed=True)

add(T, "Thermal expansion and calorimetry", "Intermediate", "match_list",
    match_stem("Match List-I (thermal quantity) with List-II (its SI unit).",
               ["Specific heat capacity", "Molar specific heat capacity", "Latent heat", "Heat capacity of a body"],
               ["J kg⁻¹", "J kg⁻¹ K⁻¹", "J mol⁻¹ K⁻¹", "J K⁻¹"]),
    match_options({"A": "II", "B": "III", "C": "I", "D": "IV"},
                  [{"A": "II", "B": "III", "C": "IV", "D": "I"}, {"A": "IV", "B": "III", "C": "I", "D": "II"},
                   {"A": "I", "B": "III", "C": "II", "D": "IV"}], "C"),
    "Definitions of heat capacity, specific heat and latent heat",
    "Heat capacity S = ΔQ/ΔT belongs to a whole body. Dividing by its mass gives the specific heat capacity, and "
    "dividing by the amount of substance gives the molar specific heat capacity. Latent heat is the heat per unit "
    "mass for a change of state, which happens without a change in temperature, so it has no K⁻¹.",
    ["Specific heat: ΔQ/(mΔT) → J kg⁻¹ K⁻¹ (II)", "Molar specific heat: ΔQ/(μΔT) → J mol⁻¹ K⁻¹ (III)",
     "Latent heat: Q/m → J kg⁻¹ (I)", "Heat capacity: ΔQ/ΔT → J K⁻¹ (IV)"],
    why="The other codes give latent heat a K⁻¹ (it involves no temperature change) or swap the heat capacity of a "
        "body with the specific heat capacity.",
    ncert="Class 11 Physics, 'Thermal Properties of Matter', specific heat capacity and latent heat", seconds=45)

add(T, "Heat transfer", "Intermediate", "statement_pair",
    SP_STEM.format(
        s1="When heat is conducted through a rod in the steady state, the temperature at each point of the rod "
           "does not change with time.",
        s2="In the steady state of conduction through a uniform rod with insulated sides, the temperature falls "
           "uniformly (linearly) with distance along the rod, from the hot end to the cold end."),
    sp("A"),
    "Steady-state conduction",
    "In the steady state no part of the rod is still absorbing heat, so every temperature stays fixed. With "
    "insulated sides, the same heat current H = KA(dT/dx) passes every cross-section; for a uniform rod K and A are "
    "constant, so the temperature gradient is the same everywhere.",
    ["Steady state → temperatures constant in time (I true)",
     "H, K and A constant along the rod → dT/dx constant → linear fall (II true)"],
    why="Both statements are true for a uniform rod with insulated sides, so options B, C and D are wrong.",
    ncert="Class 11 Physics, 'Thermal Properties of Matter', heat transfer (conduction)", seconds=50)

rho_s, L_w, Y_s = 8000, 10, 2e11
dl = rho_s * g * L_w ** 2 / (2 * Y_s)
assert close(dl, 2e-5) and close(2 * dl, 4e-5)
add(T, "Elasticity and moduli", "Advanced", "numerical",
    "A uniform steel wire 10 m long hangs vertically from a rigid support with nothing attached to its lower end. "
    "The density of steel is 8000 kg/m³ and its Young's modulus is 2 × 10¹¹ N/m². Taking g = 10 m/s², the extension "
    "of the wire due to its own weight is:",
    place("0.02 mm", ["0.04 mm", "0.01 mm", "2 mm"], "C"),
    "Extension of a wire under its own weight",
    "The tension is not uniform: at a distance x above the lower end it equals the weight of the wire below, ρAgx. "
    "Each element dx stretches by (ρAgx/AY)dx, and adding these up gives half of what the whole weight would produce "
    "if it hung at the bottom.",
    ["d(Δl) = ρgx dx/Y", "Δl = ρgL²/(2Y) = 8000 × 10 × 100/(4 × 10¹¹)", "= 2 × 10⁻⁵ m = 0.02 mm"],
    why="0.04 mm treats the whole weight as acting at the lower end (uniform tension). 0.01 mm halves twice. 2 mm "
        "is a slip by a factor of 100.",
    ncert="Class 11 Physics, 'Mechanical Properties of Solids', Young's modulus", seconds=100, recomputed=True)

r1_, r2_ = 3, 4
r_new = math.sqrt(r1_ ** 2 + r2_ ** 2)
assert r_new == 5 and round((r1_ ** 3 + r2_ ** 3) ** (1 / 3), 1) == 4.5 and r1_ * r2_ / (r2_ - r1_) == 12
add(T, "Surface tension and capillarity", "Advanced", "numerical",
    "Two soap bubbles of radii 3 cm and 4 cm, in vacuum, coalesce to form a single bubble at the same temperature. "
    "The amount of air inside stays the same. The radius of the new bubble is:",
    place("5 cm", ["7 cm", "about 4.5 cm", "12 cm"], "A"),
    "Excess pressure in a soap bubble with the gas law",
    "In vacuum the pressure of the air inside a bubble equals the excess pressure 4S/r. At constant temperature the "
    "total amount of air, measured by PV, is unchanged: (4S/r)(4πr³/3) ∝ r², so the squares of the radii add.",
    ["P₁V₁ + P₂V₂ = PV", "(4S/r₁)r₁³ + (4S/r₂)r₂³ = (4S/r)r³ → r₁² + r₂² = r²", "r = √(9 + 16) = 5 cm"],
    why="7 cm adds the radii. About 4.5 cm keeps the total volume constant, ignoring the change of pressure. 12 cm is "
        "r₁r₂/(r₂ − r₁), the radius of the common film when two bubbles stick together, not the radius of a merged "
        "bubble.",
    ncert="Class 11 Physics, 'Mechanical Properties of Fluids', surface tension (excess pressure inside a bubble)",
    seconds=120, recomputed=True)

alpha_b, dT_, day = 2e-5, 20, 86400
lost = day * 0.5 * alpha_b * dT_
assert round(lost, 2) == 17.28 and round(day * alpha_b * dT_, 1) == 34.6
add(T, "Thermal expansion and calorimetry", "Advanced", "numerical",
    "A pendulum clock with a brass pendulum rod (coefficient of linear expansion 2 × 10⁻⁵ K⁻¹) keeps correct time "
    "at 20 °C. Treating the pendulum as a simple pendulum, at 40 °C the clock:",
    place("loses about 17 s per day", ["gains about 17 s per day", "loses about 35 s per day",
                                       "loses about 8.6 s per day"], "D"),
    "Thermal expansion of a pendulum and its period",
    "The period T = 2π√(l/g) grows as the rod lengthens. For a small change, ΔT/T = ½Δl/l = ½αΔθ. A longer period "
    "means the clock ticks fewer times per day, so it loses time.",
    ["Δl/l = αΔθ = 2 × 10⁻⁵ × 20 = 4 × 10⁻⁴", "ΔT/T = ½ × 4 × 10⁻⁴ = 2 × 10⁻⁴",
     "Time lost per day = 86 400 × 2 × 10⁻⁴ ≈ 17.3 s"],
    why="'Gains' has the sign reversed: a longer period makes a slow clock. 35 s forgets the ½ from the square "
        "root. 8.6 s halves twice.",
    ncert="Class 11 Physics, 'Thermal Properties of Matter', thermal expansion", seconds=100, recomputed=True)

c_ice, c_w, Lf, Lv = 2100, 4200, 3.36e5, 2.26e6
Q_ice = 1 * c_ice * 20
Q_melt = 1 * Lf
Q_water = 1 * c_w * 100
Q_vap = 1 * Lv
multi_key([Q_ice == 42000, Q_melt > Q_ice, round(Q_vap / Q_melt, 1) == 6.7, Q_water < Q_melt, c_ice < c_w], "abce")
add(T, "Thermal expansion and calorimetry", "Advanced", "multi_statement",
    multi("1 kg of ice at −20 °C is heated at a constant rate, with no heat lost, until it has all turned into steam "
          "at 100 °C. Take the specific heat capacities of ice and water as 2100 and 4200 J kg⁻¹ K⁻¹, and the latent "
          "heats of fusion and vaporisation as 3.36 × 10⁵ and 2.26 × 10⁶ J kg⁻¹. Which of the following statements "
          "are correct?",
          ["Warming the ice from −20 °C to 0 °C needs 42 kJ.",
           "Melting the ice takes longer than warming it from −20 °C to 0 °C.",
           "Boiling away the water at 100 °C takes about 6.7 times as long as melting the ice.",
           "Heating the water from 0 °C to 100 °C takes less time than melting the ice.",
           "The temperature rises faster while the ice is warming than while the water is warming."]),
    place("(a), (b), (c) and (e) only", ["(a), (b) and (d) only", "(b), (c), (d) and (e) only",
                                         "(a), (c) and (e) only"], "B"),
    "Heating curve: specific heats and latent heats",
    "With a constant rate of heating, the time for each stage is proportional to the heat that stage needs. "
    "The slope of the temperature–time graph is inversely proportional to the specific heat capacity.",
    ["(a) 1 × 2100 × 20 = 42 000 J (true)", "(b) melting needs 336 kJ > 42 kJ (true)",
     "(c) 2.26 × 10⁶/3.36 × 10⁵ ≈ 6.7 (true)", "(d) 1 × 4200 × 100 = 420 kJ > 336 kJ (false)",
     "(e) c_ice = 2100 < c_water = 4200 → steeper rise for ice (true)"],
    why="(d) is false: warming the water through 100 °C needs 420 kJ, more than the 336 kJ for melting.",
    ncert="Class 11 Physics, 'Thermal Properties of Matter', change of state and latent heat", seconds=150,
    recomputed=True)


# =====================================================================================================================
# Thermodynamics (B3 I4 A3)
# =====================================================================================================================
T = "Thermodynamics"

Q_in6, dU6, P6 = 500, 300, 2e5
dV6 = (Q_in6 - dU6) / P6                          # m^3
assert close(dV6 * 1000, 1.0) and close(Q_in6 / P6 * 1000, 2.5) and close((Q_in6 + dU6) / P6 * 1000, 4.0)
assert close(dU6 / P6 * 1000, 1.5)
add(T, "Zeroth and first law", "Basic", "numerical",
    "A gas absorbs 500 J of heat while it expands at a constant pressure of 2 × 10⁵ Pa, and its internal energy "
    "increases by 300 J. The increase in the volume of the gas is:",
    place("1 L", ["2.5 L", "4 L", "1.5 L"], "B"),
    "First law with work at constant pressure: ΔQ = ΔU + PΔV",
    "The part of the heat that does not go into internal energy is the work done by the gas, and at constant "
    "pressure that work is PΔV.",
    ["W = ΔQ − ΔU = 500 − 300 = 200 J", "ΔV = W/P = 200/(2 × 10⁵) = 1 × 10⁻³ m³ = 1 L"],
    why="2.5 L treats all 500 J of heat as work. 4 L adds ΔU to the heat instead of subtracting it. 1.5 L divides "
        "ΔU, not the work, by the pressure.",
    ncert="Class 11 Physics, 'Thermodynamics', first law of thermodynamics", seconds=30, recomputed=True)

add(T, "Zeroth and first law", "Basic", "direct",
    "For a gas undergoing a quasi-static process, the area under its curve on a pressure–volume (P–V) diagram, "
    "between the initial and final volumes, gives:",
    place("the work done by the gas", ["the change in its internal energy", "the heat absorbed by the gas",
                                       "the change in its temperature"], "D"),
    "Work done as area on a P–V diagram",
    "For a small change in volume dV at pressure P, the gas does work P dV. Adding these up from V₁ to V₂ gives "
    "W = ∫P dV, which is the area under the P–V curve.",
    ["dW = P dV", "W = ∫P dV = area under the P–V curve"],
    why="Internal energy depends only on the state (end points), not on the area. Heat absorbed equals ΔU + W, not W "
        "alone. Temperature changes are not given by this area.",
    ncert="Class 11 Physics, 'Thermodynamics', first law of thermodynamics (work done by a gas)", seconds=30)

add(T, "Zeroth and first law", "Basic", "assertion_reason",
    AR_STEM.format(
        a="The first law of thermodynamics is the principle of conservation of energy applied to a system that "
          "exchanges energy with its surroundings.",
        r="Heat and work are both ways of transferring energy, and the heat supplied to a system goes partly into "
          "raising its internal energy and partly into the work it does (ΔQ = ΔU + ΔW)."),
    ar("A"),
    "First law of thermodynamics",
    "Heat and work are two modes of energy transfer. The first law states that the energy supplied as heat is "
    "accounted for completely by the change in internal energy and the work done by the system: no energy is "
    "created or lost.",
    ["ΔQ = ΔU + ΔW", "This is energy bookkeeping → conservation of energy → A, explained by R"],
    why="R spells out exactly why the first law is a statement of energy conservation, so B is wrong; both are "
        "true, so C and D are wrong.",
    ncert="Class 11 Physics, 'Thermodynamics', first law of thermodynamics", seconds=35)

n, Rg, dT = 2, 8.3, 50
W_p = n * Rg * dT
assert close(W_p, 830)
add(T, "Zeroth and first law", "Intermediate", "numerical",
    "Two moles of an ideal gas are heated at constant pressure from 300 K to 350 K. Taking R = 8.3 J mol⁻¹ K⁻¹, the "
    "work done by the gas is:",
    place("830 J", ["415 J", "2075 J", "5810 J"], "C"),
    "Work done in an isobaric process",
    "At constant pressure W = PΔV, and for an ideal gas PΔV = nRΔT, so the work does not depend on whether the gas "
    "is monatomic or diatomic.",
    ["W = nRΔT = 2 × 8.3 × 50", "= 830 J"],
    why="415 J uses one mole. 2075 J is (5/2)nRΔT, the internal energy change of a diatomic gas. 5810 J multiplies "
        "by 350 K instead of the 50 K change.",
    ncert="Class 11 Physics, 'Thermodynamics', thermodynamic processes (isobaric process)", seconds=40,
    recomputed=True)
assert close(1 * Rg * dT, 415) and close(2.5 * n * Rg * dT, 2075) and close(n * Rg * 350, 5810)

add(T, "Second law, reversible and irreversible processes", "Intermediate", "statement_pair",
    SP_STEM.format(
        s1="A book lying on a table never cools down by itself and uses that energy to jump up, even though such "
           "an event would not violate the first law of thermodynamics.",
        s2="A process is irreversible only if friction is present; any process free of friction is reversible."),
    sp("C"),
    "Second law of thermodynamics and irreversibility",
    "The first law only demands that energy be conserved; many processes that conserve energy are never observed, "
    "and the second law is what rules them out. Friction is only one cause of irreversibility: a process that "
    "takes the system through non-equilibrium states, such as the free expansion of a gas, is irreversible even "
    "with no friction at all.",
    ["Statement I: energy would be conserved, yet the process never happens; the second law forbids it → true",
     "Statement II: free expansion has no friction but is irreversible → false"],
    why="Statement II ignores the other source of irreversibility, non-equilibrium states, so 'both true' and "
        "'I false, II true' are wrong; Statement I is true, so 'both false' is wrong.",
    ncert="Class 11 Physics, 'Thermodynamics', second law of thermodynamics; reversible and irreversible processes",
    seconds=50)

add(T, "Isothermal and adiabatic processes", "Intermediate", "match_list",
    match_stem("A fixed amount of an ideal gas undergoes each process in List-I. On a P–V diagram, with pressure P "
               "along the vertical axis and volume V along the horizontal axis, match List-I (process) with List-II "
               "(shape of its graph).",
               ["Isochoric process", "Isobaric process", "Isothermal process",
                "A process in which the pressure is directly proportional to the volume"],
               ["A straight line which, when extended, passes through the origin",
                "A straight line parallel to the P-axis", "A straight line parallel to the V-axis",
                "A rectangular hyperbola"]),
    match_options({"A": "II", "B": "III", "C": "IV", "D": "I"},
                  [{"A": "III", "B": "II", "C": "IV", "D": "I"}, {"A": "II", "B": "III", "C": "I", "D": "IV"},
                   {"A": "II", "B": "IV", "C": "III", "D": "I"}], "A"),
    "Graphs of thermodynamic processes on a P–V diagram",
    "At constant volume only P changes (vertical line). At constant pressure only V changes (horizontal line). At "
    "constant temperature PV = constant, a rectangular hyperbola. P = kV is a straight line through the origin.",
    ["Isochoric: V fixed → parallel to P-axis (II)", "Isobaric: P fixed → parallel to V-axis (III)",
     "Isothermal: PV = const → hyperbola (IV)", "P ∝ V → line through origin (I)"],
    why="The other codes swap the isochoric and isobaric lines or confuse the hyperbola with the line through the "
        "origin.",
    ncert="Class 11 Physics, 'Thermodynamics', thermodynamic processes", seconds=45)

add(T, "Second law, reversible and irreversible processes", "Intermediate", "direct",
    "A gas in a cylinder fitted with a frictionless piston is to be expanded quasi-statically, so that the process "
    "can be reversed. For this, the external pressure on the piston must at every stage:",
    place("differ from the pressure of the gas only by an infinitesimal amount",
          ["be kept equal to zero, so that the gas expands freely",
           "be suddenly lowered to the final pressure and then held constant",
           "be kept equal to the initial pressure of the gas throughout"], "B"),
    "Quasi-static (reversible) expansion",
    "A quasi-static process is carried out so slowly that the system stays in equilibrium with its surroundings "
    "at every stage. For mechanical equilibrium, the external pressure must be lowered in tiny steps, never "
    "differing from the gas pressure by more than an infinitesimal amount; then an infinitesimal increase in the "
    "external pressure would reverse the motion of the piston.",
    ["Quasi-static → equilibrium at every stage", "Mechanical equilibrium → P_ext differs from P_gas only "
     "infinitesimally", "A finite pressure difference produces non-equilibrium states → irreversible"],
    why="Zero external pressure gives free expansion, which is irreversible. A sudden drop to the final pressure "
        "creates a finite pressure difference, so the gas passes through non-equilibrium states. If the external "
        "pressure stayed equal to the initial gas pressure, the piston would not move out at all.",
    ncert="Class 11 Physics, 'Thermodynamics', quasi-static process; reversible and irreversible processes",
    seconds=45)

PV0 = 1e5 * 10e-3                               # 1000 J at the start
W_iso = -PV0 * 0.693                            # compression 10 L -> 5 L, work done BY the gas
PV2 = PV0                                       # isothermal: P2V2 = P1V1, P2 = 2e5 Pa
P3 = 2e5 / (2 * 1.414)                          # adiabatic 5 L -> 10 L with gamma = 1.5: P3 = P2 (1/2)^1.5
W_adi = (PV2 - P3 * 10e-3) / 0.5
assert close(W_iso, -693) and close(P3, 70721.4, 1e-4) and round(W_adi) == 586 and round(W_iso + W_adi) == -107
assert round(-W_iso + W_adi) == 1279
add(T, "Isothermal and adiabatic processes", "Advanced", "numerical",
    "An ideal gas (γ = 1.5) at a pressure of 1 × 10⁵ Pa occupies 10 L. It is first compressed reversibly and "
    "isothermally to 5 L, and then allowed to expand reversibly and adiabatically back to 10 L. Taking ln 2 = 0.693 "
    "and √2 = 1.414, the net work in the two processes together is:",
    place("107 J, done on the gas", ["1279 J, done by the gas", "586 J, done by the gas", "693 J, done on the gas"],
          "D"),
    "Work in isothermal and adiabatic processes",
    "Isothermal: W = P₁V₁ ln(V₂/V₁), negative for a compression. Adiabatic: PV^γ = constant gives the final "
    "pressure, and the work done by the gas is (P_iV_i − P_fV_f)/(γ − 1).",
    ["Isothermal 10 L → 5 L: W₁ = 1000 × ln(1/2) = −693 J; P₂ = 2 × 10⁵ Pa",
     "Adiabatic 5 L → 10 L: P₃ = 2 × 10⁵ × (1/2)^1.5 = 2 × 10⁵/(2 × 1.414) ≈ 7.07 × 10⁴ Pa",
     "W₂ = (2 × 10⁵ × 5 × 10⁻³ − 7.07 × 10⁴ × 10 × 10⁻³)/0.5 = (1000 − 707)/0.5 ≈ 586 J",
     "Net W = −693 + 586 ≈ −107 J, i.e. 107 J of work is done on the gas"],
    why="1279 J adds the two works, ignoring that the isothermal work is negative (done on the gas). 586 J is only "
        "the adiabatic work, and 693 J is only the isothermal work.",
    ncert="Class 11 Physics, 'Thermodynamics', isothermal and adiabatic processes", seconds=150, recomputed=True)

V_a, P_lo, P_hi, ln3 = 4e-3, 1e5, 3e5, 1.1
Q_iso_v = 2.5 * V_a * (P_hi - P_lo)              # diatomic, constant volume: (5/2) V ΔP
Q_iso_t = P_hi * V_a * ln3                       # isothermal 4 L -> 12 L at P_hi V_a = const
assert close(Q_iso_v, 2000) and close(Q_iso_t, 1320) and close(Q_iso_v + Q_iso_t, 3320)
assert close(1.5 * V_a * (P_hi - P_lo) + Q_iso_t, 2520) and close(Q_iso_v + P_lo * V_a * ln3, 2440)
assert close(3 * P_lo * V_a, P_lo * 12e-3)          # final state really is 12 L at 1e5 Pa
add(T, "Isothermal and adiabatic processes", "Advanced", "numerical",
    "A diatomic ideal gas (rigid molecules, C_v = 5R/2) occupies 4 L at 1 × 10⁵ Pa. It is heated at constant "
    "volume until its pressure is 3 × 10⁵ Pa, and then expands reversibly and isothermally until its volume is "
    "12 L. Taking ln 3 = 1.1, the total heat absorbed by the gas in the two processes is:",
    place("3320 J", ["2520 J", "2000 J", "2440 J"], "A"),
    "Heat in isochoric and isothermal processes",
    "At constant volume no work is done, so Q = nC_vΔT = (5/2)VΔP. In the isothermal step ΔU = 0, so the heat "
    "absorbed equals the work done, nRT ln(V_f/V_i) = PV ln(V_f/V_i), using PV at the temperature of that step.",
    ["Isochoric: Q₁ = (5/2) × 4 × 10⁻³ × 2 × 10⁵ = 2000 J",
     "Isothermal at PV = 3 × 10⁵ × 4 × 10⁻³ = 1200 J: Q₂ = 1200 × ln 3 = 1320 J",
     "Total Q = 2000 + 1320 = 3320 J"],
    why="2520 J uses C_v = 3R/2 (monatomic) in the constant-volume step. 2000 J leaves out the isothermal step, "
        "assuming no heat is absorbed when the temperature is constant. 2440 J uses the initial PV (400 J) instead "
        "of the PV at the higher temperature (1200 J) for the isothermal step.",
    ncert="Class 11 Physics, 'Thermodynamics', thermodynamic processes; first law of thermodynamics", seconds=150,
    recomputed=True)

add(T, "Second law, reversible and irreversible processes", "Advanced", "statement_pair",
    SP_STEM.format(
        s1="An ideal gas in a thermally insulated container expands freely into a vacuum. A reversible adiabatic "
           "compression back to its original volume then restores the gas to its original state.",
        s2="Heat exchanged between a system and a reservoir approaches a reversible process only when the "
           "temperature difference between them is made infinitesimally small."),
    sp("D"),
    "Free expansion and reversible heat transfer",
    "In free expansion Q = 0 and W = 0, so ΔU = 0 and the temperature of the ideal gas is unchanged. A reversible "
    "adiabatic compression then does work on the gas with no heat leaving it, so its internal energy and "
    "temperature rise: it reaches the original volume at a higher temperature (and pressure), not the original "
    "state. Heat flow across a finite temperature difference is irreversible; it is reversible only in the limit "
    "of an infinitesimal difference, as in a quasi-static isothermal process.",
    ["Free expansion: ΔU = 0 → T unchanged at the larger volume",
     "Adiabatic compression: W on gas > 0, Q = 0 → ΔU > 0 → T ends above the original → Statement I false",
     "Finite ΔT heat flow is irreversible; infinitesimal ΔT is the reversible limit → Statement II true"],
    why="Statement I overlooks that the adiabatic compression adds internal energy; to undo a free expansion heat "
        "must be removed, which changes the surroundings. Statement II is true, so 'both false' and 'I true, II "
        "false' are wrong.",
    ncert="Class 11 Physics, 'Thermodynamics', reversible and irreversible processes", seconds=75)


# =====================================================================================================================
# Kinetic Theory of Gases (B2 I3 A2)
# =====================================================================================================================
T = "Kinetic Theory of Gases"

kB = 1.38e-23
n_ = 1e5 / (kB * 300)
assert round(n_ / 1e25, 1) == 2.4 and round(kB * 300 / 1e-21, 1) == 4.1
add(T, "Ideal gas equation", "Basic", "numerical",
    "Taking Boltzmann's constant as 1.38 × 10⁻²³ J K⁻¹, the number of molecules per cubic metre in an ideal gas at "
    "a pressure of 1.0 × 10⁵ Pa and a temperature of 300 K is about:",
    place("2.4 × 10²⁵", ["6.0 × 10²³", "2.4 × 10²²", "4.1 × 10⁻²¹"], "A"),
    "Ideal gas equation in terms of the number of molecules",
    "PV = Nk_BT, so the number density is N/V = P/(k_BT).",
    ["n = 1.0 × 10⁵/(1.38 × 10⁻²³ × 300)", "= 1.0 × 10⁵/(4.14 × 10⁻²¹) ≈ 2.4 × 10²⁵ m⁻³"],
    why="6.0 × 10²³ is Avogadro's number, the number in one mole, not in one cubic metre. 2.4 × 10²² is the number "
        "per litre. 4.1 × 10⁻²¹ is k_BT, an energy.",
    ncert="Class 11 Physics, 'Kinetic Theory', behaviour of gases (ideal gas equation)", seconds=40, recomputed=True)

assert F(273 + 127, 273 + 27) == F(4, 3)
add(T, "Ideal gas equation", "Basic", "numerical",
    "An ideal gas is sealed in a rigid container at 27 °C and pressure P. It is heated to 127 °C. Its pressure "
    "becomes:",
    place("4P/3", ["127P/27", "3P/4", "P"], "D"),
    "Pressure law at constant volume",
    "At constant volume, P ∝ T, where T must be the absolute (kelvin) temperature.",
    ["T₁ = 300 K, T₂ = 400 K", "P₂ = P × 400/300 = 4P/3"],
    why="127P/27 uses Celsius temperatures. 3P/4 inverts the ratio. P assumes pressure does not depend on "
        "temperature in a sealed container.",
    ncert="Class 11 Physics, 'Kinetic Theory', behaviour of gases", seconds=30, recomputed=True)

assert (2 * F(1, 2)) / (3 * F(1, 2)) == F(2, 3)
add(T, "Degrees of freedom and equipartition", "Intermediate", "numerical",
    "For an ideal gas of rigid diatomic molecules (vibrations not excited) in thermal equilibrium, the ratio of the "
    "total rotational kinetic energy of the molecules to their total translational kinetic energy is:",
    place("2 : 3", ["3 : 2", "1 : 1", "2 : 5"], "C"),
    "Law of equipartition of energy",
    "Each quadratic degree of freedom carries ½k_BT on average. A rigid diatomic molecule has 3 translational and 2 "
    "rotational degrees of freedom.",
    ["Translational: 3 × ½k_BT = (3/2)k_BT", "Rotational: 2 × ½k_BT = k_BT", "Ratio = 1 : 3/2 = 2 : 3"],
    why="3 : 2 inverts the ratio. 1 : 1 gives each kind of motion the same energy. 2 : 5 compares rotational energy "
        "with the total kinetic energy.",
    ncert="Class 11 Physics, 'Kinetic Theory', law of equipartition of energy", seconds=45, recomputed=True)

nd, mm, vr = 2e25, 5e-26, 600
P_k = nd * mm * vr ** 2 / 3
assert close(P_k, 1.2e5) and close(3 * P_k, 3.6e5) and close(nd * mm * vr / 3, 200)
add(T, "Pressure and rms speed", "Intermediate", "numerical",
    "A gas contains 2 × 10²⁵ molecules per cubic metre, each of mass 5 × 10⁻²⁶ kg, and the rms speed of the "
    "molecules is 600 m/s. According to the kinetic theory of an ideal gas, the pressure of the gas is:",
    place("1.2 × 10⁵ Pa", ["3.6 × 10⁵ Pa", "200 Pa", "6.0 × 10⁴ Pa"], "B"),
    "Kinetic-theory expression for pressure",
    "P = (1/3)nm v²_rms, where n is the number of molecules per unit volume and m the mass of one molecule; nm is "
    "the density of the gas.",
    ["nm = 2 × 10²⁵ × 5 × 10⁻²⁶ = 1 kg/m³", "P = (1/3) × 1 × 600² = 1.2 × 10⁵ Pa"],
    why="3.6 × 10⁵ Pa drops the factor 1/3. 200 Pa forgets to square the speed. 6.0 × 10⁴ Pa adds an extra factor "
        "½ as if computing kinetic energy.",
    ncert="Class 11 Physics, 'Kinetic Theory', pressure of an ideal gas", seconds=50, recomputed=True)
assert close(P_k / 2, 6.0e4)

assert F(1, 2) * 2 == 1
add(T, "Ideal gas equation", "Intermediate", "direct",
    "An ideal gas is held in a rigid container. Half of its molecules leak out, and at the same time the absolute "
    "temperature of the gas left inside is doubled. The pressure of the gas:",
    place("remains the same", ["is doubled", "is halved", "becomes four times"], "A"),
    "P = nk_BT with two changes at once",
    "P = (N/V)k_BT. The volume is fixed, N is halved and T is doubled, so the product NT, and hence P, is unchanged.",
    ["P ∝ NT (V fixed)", "N → N/2, T → 2T → NT unchanged"],
    why="'Doubled' looks only at the temperature, 'halved' only at the leak. 'Four times' multiplies the two "
        "changes instead of combining them as factors 2 and ½.",
    ncert="Class 11 Physics, 'Kinetic Theory', behaviour of gases", seconds=40)

M_He, M_O = 4, 32
nHe_nO = F(M_O, M_He)
U_He = nHe_nO * F(3, 2)
U_O = F(5, 2)
multi_key([True, close(math.sqrt(M_O / M_He), 2 * math.sqrt(2)), nHe_nO == 8, U_He > U_O, F(3, 2) > F(5, 2)],
          "abcd")
add(T, "Degrees of freedom and equipartition", "Advanced", "multi_statement",
    multi("Equal masses of helium (monatomic, molar mass 4 g/mol) and oxygen (rigid diatomic molecules, molar mass "
          "32 g/mol) are kept in separate containers at the same temperature. Treating both as ideal gases, which "
          "of the following statements are correct?",
          ["The average translational kinetic energy per molecule is the same in both gases.",
           "The rms speed of the helium atoms is 2√2 times that of the oxygen molecules.",
           "The helium sample contains 8 times as many moles as the oxygen sample.",
           "The total internal energy of the helium sample is greater than that of the oxygen sample.",
           "The molar specific heat at constant volume of helium is greater than that of oxygen."]),
    place("(a), (b), (c) and (d) only", ["(a), (b) and (e) only", "(b), (c) and (d) only",
                                         "(a), (d) and (e) only"], "C"),
    "Equipartition, rms speed and internal energy compared",
    "At the same temperature every molecule has (3/2)k_BT of translational energy. v_rms = √(3RT/M). Equal masses "
    "give moles inversely proportional to molar mass. U = n(f/2)RT and C_v = (f/2)R with f = 3 for helium and 5 "
    "for rigid oxygen.",
    ["(a) (3/2)k_BT for both (true)", "(b) √(32/4) = √8 = 2√2 (true)", "(c) n ∝ 1/M → 32/4 = 8 (true)",
     "(d) U_He = 8n × (3/2)RT = 12nRT > U_O₂ = n × (5/2)RT (true)",
     "(e) C_v(He) = 1.5R < C_v(O₂) = 2.5R (false)"],
    why="(e) reverses the comparison of molar specific heats; every option without all of (a)–(d) is incomplete.",
    ncert="Class 11 Physics, 'Kinetic Theory', kinetic interpretation of temperature and law of equipartition",
    seconds=150, recomputed=True)

mm2, v_, flux = 5e-26, 500, 2e23
P_w = flux * 2 * mm2 * v_ * math.cos(math.radians(60))
assert close(P_w, 5) and close(flux * 2 * mm2 * v_, 10) and close(flux * mm2 * v_ * 0.5, 2.5)
assert round(flux * 2 * mm2 * v_ * math.sin(math.radians(60)), 2) == 8.66
add(T, "Pressure and rms speed", "Advanced", "numerical",
    "A beam of molecules, each of mass 5 × 10⁻²⁶ kg and speed 500 m/s, strikes a flat wall, each molecule moving at "
    "60° to the normal to the wall. The collisions are elastic. If 2 × 10²³ molecules strike each square metre of "
    "the wall per second, the pressure the beam exerts on the wall is:",
    place("5 Pa", ["10 Pa", "2.5 Pa", "8.66 Pa"], "D"),
    "Pressure as the rate of momentum transfer per unit area",
    "In an elastic collision with the wall, only the component of velocity normal to the wall reverses. The "
    "momentum given to the wall by each molecule is 2mv cos θ; pressure is this times the number of hits per unit "
    "area per second.",
    ["Normal component = 500 cos 60° = 250 m/s", "Δp per molecule = 2 × 5 × 10⁻²⁶ × 250 = 2.5 × 10⁻²³ kg m/s",
     "P = 2 × 10²³ × 2.5 × 10⁻²³ = 5 Pa"],
    why="10 Pa treats the molecules as striking normally. 2.5 Pa forgets that the normal component reverses "
        "(change 2mv cos θ, not mv cos θ). 8.66 Pa uses sin 60°, the component along the wall.",
    ncert="Class 11 Physics, 'Kinetic Theory', pressure of an ideal gas", seconds=100, recomputed=True)


# =====================================================================================================================
# Oscillations and Waves (B4 I5 A4)
# =====================================================================================================================
T = "Oscillations and Waves"

add(T, "Progressive waves and wave speed", "Basic", "match_list",
    match_stem("For a progressive wave y(x, t) = a sin(kx − ωt), match List-I (quantity) with List-II (its SI unit).",
               ["Angular wave number k", "Angular frequency ω", "Wave speed ω/k", "Frequency ω/2π"],
               ["rad m⁻¹", "rad s⁻¹", "m s⁻¹", "s⁻¹ (hertz)"]),
    match_options({"A": "I", "B": "II", "C": "III", "D": "IV"},
                  [{"A": "II", "B": "I", "C": "III", "D": "IV"}, {"A": "I", "B": "IV", "C": "III", "D": "II"},
                   {"A": "III", "B": "II", "C": "I", "D": "IV"}], "B"),
    "Parameters of a harmonic wave and their units",
    "The phase kx − ωt is an angle in radians, so k carries radians per metre and ω radians per second. Their ratio "
    "ω/k is a speed, and ω/2π, the number of oscillations per second, is measured in hertz.",
    ["k = 2π/λ → rad m⁻¹ (I)", "ω = 2π/T → rad s⁻¹ (II)", "v = ω/k → m s⁻¹ (III)", "ν = ω/2π → s⁻¹ (IV)"],
    why="The other codes swap k with ω, or ω with ν: ω is an angular quantity (rad s⁻¹), while ν counts cycles per "
        "second.",
    ncert="Class 11 Physics, 'Waves', displacement relation in a progressive wave", seconds=40)

add(T, "SHM equation and phase", "Basic", "match_list",
    match_stem("The displacement of a particle in simple harmonic motion is x(t) = A cos(ωt + φ). Match List-I "
               "(term) with List-II (its name).",
               ["A", "ω", "(ωt + φ)", "φ"],
               ["Phase constant (phase angle)", "Amplitude", "Phase of the motion", "Angular frequency"]),
    match_options({"A": "II", "B": "IV", "C": "III", "D": "I"},
                  [{"A": "II", "B": "IV", "C": "I", "D": "III"}, {"A": "IV", "B": "II", "C": "III", "D": "I"},
                   {"A": "II", "B": "III", "C": "IV", "D": "I"}], "D"),
    "Terms in the equation of SHM",
    "A is the greatest displacement (amplitude). ω = 2π/T is the angular frequency. The time-dependent quantity "
    "(ωt + φ) is the phase, which fixes the state of motion at time t, and φ is its value at t = 0, the phase "
    "constant.",
    ["A → amplitude (II)", "ω → angular frequency (IV)", "ωt + φ → phase (III)", "φ → phase constant (I)"],
    why="The other codes confuse the phase (which changes with time) with the phase constant (its value at t = 0), "
        "or the amplitude with the angular frequency.",
    ncert="Class 11 Physics, 'Oscillations', simple harmonic motion", seconds=35)

add(T, "SHM equation and phase", "Basic", "assertion_reason",
    AR_STEM.format(
        a="In simple harmonic motion, the acceleration of the particle is always directed towards the mean "
          "position.",
        r="In simple harmonic motion, the restoring force on the particle is proportional to its displacement from "
          "the mean position and acts opposite to the displacement (F = −kx)."),
    ar("A"),
    "Defining property of simple harmonic motion",
    "Since F = −kx, the acceleration a = F/m = −(k/m)x is always opposite to the displacement: on either side of the "
    "mean position it points back towards it.",
    ["F = −kx → a = −(k/m)x", "x > 0 → a < 0; x < 0 → a > 0 → always towards the mean position"],
    why="R gives exactly the reason for A, so B is wrong; both statements are true, so C and D are wrong.",
    ncert="Class 11 Physics, 'Oscillations', force law for simple harmonic motion", seconds=30)

T0 = 2
assert T0 * math.sqrt(4) == 4
add(T, "Spring and pendulum oscillations", "Basic", "numerical",
    "A simple pendulum has a period of 2 s for small oscillations on the Earth. On a planet where the acceleration "
    "due to gravity is one-quarter of its value on the Earth, the period of the same pendulum is:",
    place("4 s", ["1 s", "8 s", "2 s"], "B"),
    "Period of a simple pendulum and g",
    "T = 2π√(L/g). With L fixed, T ∝ 1/√g, so a quarter of the gravity doubles the period.",
    ["T'/T = √(g/g') = √4 = 2", "T' = 2 × 2 = 4 s"],
    why="1 s takes T ∝ √g. 8 s takes T ∝ 1/g. 2 s assumes the period does not depend on g.",
    ncert="Class 11 Physics, 'Oscillations', the simple pendulum", seconds=30, recomputed=True)

add(T, "Energy in SHM", "Intermediate", "statement_pair",
    SP_STEM.format(
        s1="For a particle in simple harmonic motion, its kinetic energy averaged over one complete period is equal "
           "to its total mechanical energy.",
        s2="For a particle of given mass executing simple harmonic motion with a given amplitude, the total "
           "mechanical energy is proportional to the square of the frequency of oscillation."),
    sp("D"),
    "Energy of a simple harmonic oscillator",
    "E = ½mω²A², with ω = 2πν, so E ∝ ν² for fixed m and A. The kinetic energy ½mω²A² sin²(ωt) averages to half "
    "of E over a period, because the average of sin² over a period is ½; the other half is, on average, potential "
    "energy.",
    ["E = ½mω²A² = 2π²mν²A² → E ∝ ν² (Statement II true)",
     "⟨K⟩ = ½mω²A² × ⟨sin²ωt⟩ = E/2, not E (Statement I false)"],
    why="Statement I confuses the maximum kinetic energy (equal to E, at the mean position) with its average over "
        "a period.",
    ncert="Class 11 Physics, 'Oscillations', energy in simple harmonic motion", seconds=60)

ph1 = math.asin(0.5)                 # moving in +x: cos > 0
ph2 = math.pi - math.asin(0.5)       # moving in −x: cos < 0
assert math.cos(ph1) > 0 > math.cos(ph2) and close(ph2 - ph1, 2 * math.pi / 3)
add(T, "SHM equation and phase", "Intermediate", "numerical",
    "Two particles execute simple harmonic motion along the same line with the same amplitude A and the same "
    "frequency, about the same mean position. They pass each other at x = A/2, moving in opposite directions. The "
    "phase difference between them is:",
    place("2π/3", ["π/3", "π", "π/6"], "B"),
    "Phase from position and direction of motion",
    "Write x = A sin θ with velocity ∝ cos θ. At x = A/2, sin θ = ½. Moving one way gives θ = π/6 (cos θ > 0); "
    "moving the other way gives θ = 5π/6 (cos θ < 0).",
    ["θ₁ = π/6, θ₂ = π − π/6 = 5π/6", "Phase difference = 5π/6 − π/6 = 2π/3"],
    why="π/3 doubles π/6 without using the opposite directions. π assumes opposite directions always mean opposite "
        "phase, which holds only at the mean position. π/6 is the phase of one particle alone.",
    ncert="Class 11 Physics, 'Oscillations', simple harmonic motion (phase)", seconds=75, recomputed=True)

assert math.sqrt(32 / 2) == 4
add(T, "Progressive waves and wave speed", "Intermediate", "numerical",
    "Hydrogen (molar mass 2 g/mol) and oxygen (molar mass 32 g/mol) are both diatomic gases with the same ratio of "
    "specific heats. Treating them as ideal gases at the same temperature, the ratio of the speed of sound in "
    "hydrogen to that in oxygen is:",
    place("4 : 1", ["16 : 1", "1 : 4", "1 : 1"], "D"),
    "Speed of sound in a gas (Laplace)",
    "v = √(γP/ρ) = √(γRT/M) for an ideal gas. With equal γ and T, v ∝ 1/√M.",
    ["v_H/v_O = √(M_O/M_H) = √(32/2) = √16 = 4"],
    why="16 : 1 forgets the square root. 1 : 4 inverts the ratio. 1 : 1 assumes the speed depends only on "
        "temperature, as for the rms speed comparison of the same gas.",
    ncert="Class 11 Physics, 'Waves', speed of a longitudinal wave (speed of sound)", seconds=45, recomputed=True)

f_, l1, l2 = 500, 0.165, 0.505
lam_ = 2 * (l2 - l1)
v_s = f_ * lam_
assert close(lam_, 0.68) and close(v_s, 340) and close(l2 + lam_ / 2, 0.845)
multi_key([close(lam_, 0.68), close(v_s, 340), close(l2 + lam_ / 2, 0.845), False, close(l1, lam_ / 2)], "abc")
add(T, "Organ pipes and beats", "Intermediate", "multi_statement",
    multi("A tube closed at its lower end by a water surface resonates with a tuning fork of frequency 500 Hz when "
          "the air column is 16.5 cm long, and next when it is 50.5 cm long. Which of the following statements are "
          "correct?",
          ["The wavelength of the sound in the air column is 68 cm.",
           "The speed of sound in the air column is 340 m/s.",
           "The next resonance will occur when the air column is 84.5 cm long.",
           "At the water surface (the closed end) there is a displacement antinode.",
           "The first resonance length, 16.5 cm, is equal to half the wavelength."]),
    place("(a), (b) and (c) only", ["(a), (b) and (e) only", "(b), (c) and (d) only", "(a), (c), (d) and (e) only"],
          "A"),
    "Resonance in a pipe closed at one end",
    "In a pipe closed at one end the closed end is a displacement node. Successive resonance lengths differ by λ/2, "
    "whatever the end correction, so λ = 2(l₂ − l₁). The first resonance is near λ/4 (plus a small end correction).",
    ["(a) λ = 2(50.5 − 16.5) = 68 cm (true)", "(b) v = 500 × 0.68 = 340 m/s (true)",
     "(c) next length = 50.5 + 34 = 84.5 cm (true)", "(d) the closed end is a node, not an antinode (false)",
     "(e) 16.5 cm is close to λ/4 = 17 cm, not λ/2 = 34 cm (false)"],
    why="(d) and (e) treat the closed end like an open end; options containing them are wrong.",
    ncert="Class 11 Physics, 'Waves', standing waves and normal modes (pipe closed at one end)", seconds=100,
    recomputed=True)

v_air, Lp = 340, 0.25
fo1, fc1, fc3, fo2 = v_air / (2 * Lp), v_air / (4 * Lp), 3 * v_air / (4 * Lp), 2 * v_air / (2 * Lp)
assert (fo1, fc1, fc3, fo2) == (680, 340, 1020, 1360)
add(T, "Organ pipes and beats", "Intermediate", "match_list",
    match_stem("Each pipe is 25 cm long and the speed of sound in air is 340 m/s; neglect end corrections. Match "
               "List-I (mode) with List-II (frequency).",
               ["Fundamental mode of a pipe open at both ends", "Fundamental mode of a pipe closed at one end",
                "First overtone of a pipe closed at one end", "First overtone of a pipe open at both ends"],
               ["340 Hz", "680 Hz", "1020 Hz", "1360 Hz"]),
    match_options({"A": "II", "B": "I", "C": "III", "D": "IV"},
                  [{"A": "I", "B": "II", "C": "III", "D": "IV"}, {"A": "II", "B": "I", "C": "IV", "D": "III"},
                   {"A": "II", "B": "III", "C": "I", "D": "IV"}], "D"),
    "Normal modes of open and closed pipes",
    "An open pipe has antinodes at both ends: νₙ = nv/2L, n = 1, 2, 3, … A pipe closed at one end has a node at the "
    "closed end: νₙ = (2n − 1)v/4L, only odd harmonics. The first overtone is the next allowed mode above the "
    "fundamental.",
    ["Open: ν₁ = 340/0.5 = 680 Hz (II); first overtone 2ν₁ = 1360 Hz (IV)",
     "Closed: ν₁ = 340/1.0 = 340 Hz (I); first overtone = 3ν₁ = 1020 Hz (III)"],
    why="The other codes swap the open and closed fundamentals, or take the closed pipe's first overtone as twice "
        "its fundamental, which a closed pipe cannot produce.",
    ncert="Class 11 Physics, 'Waves', standing waves in pipes", seconds=60, recomputed=True)

m, k = 0.5, 50
x_eq = m * g / k
assert close(x_eq, 0.1) and close(2 * x_eq, 0.2)
add(T, "Spring and pendulum oscillations", "Advanced", "numerical",
    "A block of mass 0.5 kg is attached to the lower end of a light vertical spring (spring constant 50 N/m) whose "
    "upper end is fixed. The block is held so that the spring is at its natural length and is then released from "
    "rest. Taking g = 10 m/s², the maximum extension of the spring during the motion is:",
    place("20 cm", ["10 cm", "40 cm", "30 cm"], "C"),
    "Vertical oscillations about the shifted equilibrium position",
    "The block oscillates in SHM about the equilibrium position, where mg = kx₀. It is released from rest at the "
    "natural length, a distance x₀ above that position, so the amplitude is x₀ and the lowest point is 2x₀ below "
    "the natural length.",
    ["x₀ = mg/k = 5/50 = 0.1 m", "Amplitude = x₀ = 0.1 m", "Maximum extension = 2x₀ = 0.2 m = 20 cm"],
    shortcut="Energy: mgx = ½kx² → x = 2mg/k = 0.2 m.",
    why="10 cm is the equilibrium extension, where the block moves fastest, not where it stops. 40 cm and 30 cm do "
        "not follow from either the force or the energy balance.",
    ncert="Class 11 Physics, 'Oscillations', oscillations due to a spring", seconds=90, recomputed=True)

A_, w_ = 0.05, 4 * math.pi
assert close(2 * math.pi / w_, 0.5) and close(A_ * w_, 0.2 * math.pi) and close(A_ * w_ ** 2, 0.8 * math.pi ** 2)
multi_key([A_ == 0.05, close(2 * math.pi / w_, 0.5), A_ * math.cos(0) == 0, close(A_ * w_, 0.2 * math.pi),
           close(A_ * w_ ** 2, 0.8 * math.pi ** 2)], "abde")
add(T, "SHM equation and phase", "Advanced", "multi_statement",
    multi("The displacement of a particle is x = 0.05 cos(4πt), where x is in metres and t in seconds. Which of the "
          "following statements are correct?",
          ["The amplitude of the motion is 5 cm.",
           "The period of the motion is 0.5 s.",
           "At t = 0 the particle is at its mean position.",
           "The maximum speed of the particle is 0.2π m/s.",
           "The maximum magnitude of its acceleration is 0.8π² m/s²."]),
    place("(a), (b), (d) and (e) only", ["(a), (b) and (c) only", "(b), (c), (d) and (e) only",
                                         "(a), (d) and (e) only"], "D"),
    "Reading an SHM equation",
    "Compare with x = A cos ωt: A = 0.05 m and ω = 4π rad/s. Then T = 2π/ω, v_max = Aω and a_max = Aω². With a "
    "cosine, the particle starts at an extreme position.",
    ["(a) A = 0.05 m = 5 cm (true)", "(b) T = 2π/4π = 0.5 s (true)",
     "(c) x(0) = 0.05 m → extreme position, not the mean position (false)",
     "(d) v_max = 0.05 × 4π = 0.2π m/s (true)", "(e) a_max = 0.05 × 16π² = 0.8π² m/s² (true)"],
    why="(c) applies to a sine function; with x = A cos ωt the particle is at x = A when t = 0.",
    ncert="Class 11 Physics, 'Oscillations', simple harmonic motion (velocity and acceleration)", seconds=100,
    recomputed=True)

add(T, "Progressive waves and wave speed", "Advanced", "assertion_reason",
    AR_STEM.format(
        a="When a sound wave passes from air into water, its wavelength increases.",
        r="The frequency of the wave does not change when it passes from one medium into another, while the speed "
          "of sound in water is much greater than in air."),
    ar("A"),
    "Wavelength change on refraction of sound",
    "The frequency is set by the source and stays the same across the boundary. Since λ = v/ν, a larger speed in "
    "water (about 1500 m/s against about 340 m/s in air) means a proportionally longer wavelength.",
    ["ν unchanged", "λ = v/ν → λ_water/λ_air = v_water/v_air > 1"],
    why="R gives both facts that together fix the change in wavelength, so it explains A; B, C and D are wrong.",
    ncert="Class 11 Physics, 'Waves', speed of a travelling wave", seconds=50)

assert F(2 * 2, 1 * 1) == 4 and F(2 * 4, 1) == 8      # f ∝ 1/(L r)
add(T, "Superposition and standing waves", "Advanced", "numerical",
    "Two wires P and Q are made of the same material and are stretched with the same tension, each fixed at both "
    "ends. Wire Q has twice the length and twice the radius of wire P. The ratio of the fundamental frequency of P "
    "to that of Q is:",
    place("4 : 1", ["1 : 4", "2 : 1", "8 : 1"], "B"),
    "Fundamental frequency of a stretched string",
    "ν = (1/2L)√(T/μ), where the mass per unit length μ = ρπr² for a wire of density ρ. So with T and ρ fixed, "
    "ν ∝ 1/(Lr).",
    ["ν ∝ 1/(L r)", "ν_P/ν_Q = (L_Q r_Q)/(L_P r_P) = 2 × 2 = 4"],
    why="1 : 4 inverts the ratio. 2 : 1 keeps only the change in length (or only the radius). 8 : 1 takes ν ∝ "
        "1/(Lr²), forgetting the square root over μ.",
    ncert="Class 11 Physics, 'Waves', speed of a transverse wave on a stretched string and normal modes",
    seconds=75, recomputed=True)


# =====================================================================================================================
# Electrostatics (B5 I7 A5)
# =====================================================================================================================
T = "Electrostatics"
k = 9e9

E_pp = 100 / 2e-3
assert close(E_pp, 5e4) and 100 / 2 == 50 and 100 * 2 == 200 and close(2e-3 / 100, 2e-5)
add(T, "Electric potential and energy", "Basic", "numerical",
    "Two large parallel conducting plates, 2 mm apart, are connected to a 100 V battery. The magnitude of the "
    "uniform electric field between the plates, away from their edges, is:",
    place("5 × 10⁴ V/m", ["50 V/m", "200 V/m", "2 × 10⁻⁵ V/m"], "B"),
    "Relation between a uniform field and potential difference",
    "In a uniform field, E = V/d, where d is the distance between the equipotential plates (in metres).",
    ["d = 2 mm = 2 × 10⁻³ m", "E = 100/(2 × 10⁻³) = 5 × 10⁴ V/m"],
    why="50 V/m leaves d in millimetres. 200 V/m multiplies V by d. 2 × 10⁻⁵ V/m divides d by V.",
    ncert="Class 12 Physics, 'Electrostatic Potential and Capacitance', relation between electric field and "
          "potential", seconds=30, recomputed=True)

q_, d_ = 3e-9, 2e-3
p_ = q_ * d_
assert close(p_, 6e-12) and close(q_ * d_ / 2, 3e-12) and close(2 * q_ * d_, 1.2e-11)
add(T, "Electric field and dipole", "Basic", "numerical",
    "An electric dipole consists of charges +3 nC and −3 nC separated by 2 mm. The magnitude of its electric dipole "
    "moment is:",
    place("6 × 10⁻¹² C m", ["3 × 10⁻¹² C m", "1.2 × 10⁻¹¹ C m", "zero, because the net charge is zero"], "C"),
    "Electric dipole moment",
    "The dipole moment has magnitude q × 2a, where 2a is the separation of the charges, and points from −q to +q. "
    "It is not zero even though the net charge is zero.",
    ["p = q × 2a = 3 × 10⁻⁹ × 2 × 10⁻³", "= 6 × 10⁻¹² C m, directed from −q to +q"],
    why="3 × 10⁻¹² C m uses half the separation. 1.2 × 10⁻¹¹ C m adds the magnitudes of both charges. A zero "
        "dipole moment confuses the net charge with the dipole moment.",
    ncert="Class 12 Physics, 'Electric Charges and Fields', electric dipole", seconds=30, recomputed=True)

add(T, "Electric potential and energy", "Basic", "match_list",
    match_stem("Match List-I (charge configuration) with List-II (shape of its equipotential surfaces).",
               ["An isolated point charge", "A uniform electric field",
                "A very long, uniformly charged straight wire (away from its ends)",
                "The cavity inside a charged hollow conductor, with no charge in the cavity"],
               ["Planes perpendicular to the field", "The whole region is at one and the same potential",
                "Concentric spheres centred on the charge", "Coaxial cylinders with the wire as their axis"]),
    match_options({"A": "III", "B": "I", "C": "IV", "D": "II"},
                  [{"A": "IV", "B": "I", "C": "III", "D": "II"}, {"A": "III", "B": "II", "C": "IV", "D": "I"},
                   {"A": "III", "B": "I", "C": "II", "D": "IV"}], "B"),
    "Equipotential surfaces are normal to the field",
    "An equipotential surface is everywhere perpendicular to the field lines. Radial field lines from a point "
    "charge give spheres; parallel lines of a uniform field give planes; lines radiating from a long wire give "
    "cylinders. Inside the cavity of a conductor the field is zero, so the whole region has one potential.",
    ["Point charge → spheres (III)", "Uniform field → planes ⟂ field (I)", "Long wire → coaxial cylinders (IV)",
     "Field-free cavity → one potential throughout (II)"],
    why="The other codes give the point charge cylindrical surfaces, or put the uniform field and the field-free "
        "cavity in each other's places.",
    ncert="Class 12 Physics, 'Electrostatic Potential and Capacitance', equipotential surfaces", seconds=50)

add(T, "Electric field and dipole", "Basic", "assertion_reason",
    AR_STEM.format(
        a="The torque on an electric dipole in a uniform electric field is greatest when the dipole moment is "
          "perpendicular to the field.",
        r="The torque on the dipole is τ = p × E, whose magnitude is pE sin θ, where θ is the angle between p and "
          "E."),
    ar("A"),
    "Torque on a dipole in a uniform field",
    "τ = pE sin θ is largest when sin θ = 1, i.e. θ = 90°, and zero when p is parallel or antiparallel to E.",
    ["|τ| = pE sin θ", "Maximum at θ = 90° → τ_max = pE"],
    why="R gives the formula from which A follows directly, so it explains A; B, C and D are wrong.",
    ncert="Class 12 Physics, 'Electric Charges and Fields', dipole in a uniform external field", seconds=30)

add(T, "Capacitors and dielectrics", "Basic", "statement_pair",
    SP_STEM.format(
        s1="The dielectric constant of a medium is the ratio of the permittivity of the medium to the permittivity "
           "of free space.",
        s2="The dielectric constant of a metal is zero."),
    sp("C"),
    "Dielectric constant",
    "K = ε/ε₀ is the factor by which a medium reduces the field (and the force between charges) compared with "
    "vacuum. A metal reduces the field inside it to zero, which corresponds to an infinitely large dielectric "
    "constant, not zero. (K = 1 for vacuum, and K ≥ 1 for every material.)",
    ["K = ε/ε₀ (Statement I true)", "Field inside a metal = E₀/K = 0 → K → ∞ (Statement II false)"],
    why="Statement II reverses the limit: a perfect screening of the field needs K → ∞.",
    ncert="Class 12 Physics, 'Electrostatic Potential and Capacitance', dielectrics and polarisation", seconds=40)

Q_, qq = 2e-6, 1e-6
W_ext = qq * k * Q_ * (1 / 0.1 - 1 / 0.3)
assert close(W_ext, 0.12) and close(qq * k * Q_ / 0.1, 0.18) and close(qq * k * Q_ / 0.3, 0.06)
add(T, "Electric potential and energy", "Intermediate", "numerical",
    "A point charge of +2 μC is held fixed in air. Taking 1/(4πε₀) = 9 × 10⁹ N m² C⁻², the work an external agent "
    "must do to move a charge of +1 μC slowly from a point 30 cm away from the fixed charge to a point 10 cm away "
    "from it is:",
    place("0.12 J", ["0.18 J", "−0.12 J", "0.06 J"], "C"),
    "Work done against an electrostatic field",
    "For slow motion, the external agent's work equals the increase in potential energy, q(V_final − V_initial), "
    "where V = kQ/r. The path does not matter.",
    ["V(10 cm) = 9 × 10⁹ × 2 × 10⁻⁶/0.1 = 1.8 × 10⁵ V", "V(30 cm) = 6.0 × 10⁴ V",
     "W = 10⁻⁶ × (1.8 × 10⁵ − 0.6 × 10⁵) = 0.12 J"],
    why="0.18 J is the work to bring the charge from infinity to 10 cm. −0.12 J is the work done by the field, not "
        "by the external agent. 0.06 J uses only the starting point.",
    ncert="Class 12 Physics, 'Electrostatic Potential and Capacitance', potential due to a point charge", seconds=60,
    recomputed=True)

C1, C2, Vb = 2e-6, 3e-6, 100
Cs = C1 * C2 / (C1 + C2)
Qs = Cs * Vb
U1, U2 = Qs ** 2 / (2 * C1), Qs ** 2 / (2 * C2)
assert close(Cs, 1.2e-6) and close(Qs, 120e-6) and close(Qs / C1, 60) and close(U1, 3.6e-3) and close(U2, 2.4e-3)
assert close(U1 + U2, 6e-3)
multi_key([close(Cs, 1.2e-6), close(Qs, 1.2e-4), close(Qs / C1, 40), U1 > U2, close(U1 + U2, 6e-3)], "abde")
add(T, "Capacitors and dielectrics", "Intermediate", "multi_statement",
    multi("Capacitors of 2 μF and 3 μF are connected in series across a 100 V battery. Which of the following "
          "statements are correct?",
          ["The equivalent capacitance of the combination is 1.2 μF.",
           "The charge on each capacitor is 120 μC.",
           "The potential difference across the 2 μF capacitor is 40 V.",
           "The energy stored in the 2 μF capacitor is greater than that stored in the 3 μF capacitor.",
           "The total energy stored in the combination is 6 mJ."]),
    place("(a), (b), (d) and (e) only", ["(a), (b) and (c) only", "(a), (c) and (e) only",
                                         "(b), (c), (d) and (e) only"], "B"),
    "Capacitors in series",
    "Capacitors in series carry the same charge, so the smaller capacitor takes the larger share of the voltage "
    "(V = Q/C) and stores the larger energy (Q²/2C).",
    ["(a) Cs = 2 × 3/5 = 1.2 μF (true)", "(b) Q = 1.2 μF × 100 V = 120 μC (true)",
     "(c) V₂μF = 120/2 = 60 V, not 40 V (false)", "(d) U₂ = 3.6 mJ > U₃ = 2.4 mJ (true)",
     "(e) U = ½ × 1.2 × 10⁻⁶ × 100² = 6 mJ (true)"],
    why="(c) gives the 2 μF capacitor the share of the larger capacitor; in series the smaller capacitance has the "
        "larger potential difference.",
    ncert="Class 12 Physics, 'Electrostatic Potential and Capacitance', combination of capacitors and energy stored",
    seconds=100, recomputed=True)

C0 = F(1)
assert C0 * 2 == 2 and C0 / 2 == F(1, 2) and 3 * C0 == 3 and C0 * 2 / 3 == F(2, 3)
add(T, "Capacitors and dielectrics", "Intermediate", "match_list",
    match_stem("A parallel plate capacitor has capacitance C₀ with air between its plates. Match List-I (change "
               "made) with List-II (new capacitance). Each change is made starting from the original capacitor.",
               ["The plate separation is halved",
                "The area of each plate is halved",
                "The space between the plates is completely filled with a dielectric of dielectric constant 3",
                "The plate area is doubled and the plate separation is tripled"],
               ["C₀/2", "2C₀/3", "2C₀", "3C₀"]),
    match_options({"A": "III", "B": "I", "C": "IV", "D": "II"},
                  [{"A": "I", "B": "III", "C": "IV", "D": "II"}, {"A": "III", "B": "II", "C": "IV", "D": "I"},
                   {"A": "III", "B": "I", "C": "II", "D": "IV"}], "C"),
    "Dependence of the capacitance of a parallel plate capacitor",
    "C = Kε₀A/d: proportional to the plate area and the dielectric constant, and inversely proportional to the plate "
    "separation.",
    ["A: d → d/2 → 2C₀ (III)", "B: A → A/2 → C₀/2 (I)", "C: K = 3 → 3C₀ (IV)", "D: (2A)/(3d) → 2C₀/3 (II)"],
    why="The other codes treat C as proportional to the separation, or swap the effects of area and separation.",
    ncert="Class 12 Physics, 'Electrostatic Potential and Capacitance', the parallel plate capacitor and effect of "
          "dielectric", seconds=50, recomputed=True)

add(T, "Gauss's law", "Intermediate", "statement_pair",
    SP_STEM.format(
        s1="If the net electric flux through a closed surface is zero, the electric field must be zero at every "
           "point of that surface.",
        s2="A closed surface placed in a uniform electric field, with no charge inside it, has zero net electric "
           "flux through it."),
    sp("D"),
    "What zero net flux does and does not imply",
    "Gauss's law fixes only the total flux, q_enclosed/ε₀. Zero net flux means as many field lines leave as enter; "
    "the field on the surface can still be large. In a uniform field with no charge inside, every line that enters "
    "the surface also leaves it.",
    ["Uniform field, closed surface: inward flux = outward flux → net 0 (Statement II true)",
     "That same surface has a non-zero field at every point although the net flux is zero (Statement I false)"],
    why="Statement I confuses the net flux, a total over the surface, with the field at individual points.",
    ncert="Class 12 Physics, 'Electric Charges and Fields', electric flux and Gauss's law", seconds=50)

add(T, "Electric potential and energy", "Intermediate", "match_list",
    match_stem("Point charges are placed in air; a is a fixed distance and k = 1/(4πε₀). Match List-I (system) with "
               "List-II (its electrostatic potential energy, taken zero when the charges are infinitely far apart).",
               ["+q and +q, a distance a apart", "+q and −2q, a distance a apart",
                "+q, +q and +q at the corners of an equilateral triangle of side a",
                "+q, +q and −q at the corners of an equilateral triangle of side a"],
               ["−kq²/a", "+kq²/a", "+3kq²/a", "−2kq²/a"]),
    match_options({"A": "II", "B": "IV", "C": "III", "D": "I"},
                  [{"A": "II", "B": "I", "C": "III", "D": "IV"}, {"A": "III", "B": "IV", "C": "II", "D": "I"},
                   {"A": "II", "B": "IV", "C": "I", "D": "III"}], "B"),
    "Potential energy of a system of point charges",
    "U is the sum over every distinct pair of kqᵢqⱼ/rᵢⱼ, with the signs of the charges included.",
    ["A: kq²/a (II)", "B: k(q)(−2q)/a = −2kq²/a (IV)", "C: three pairs of +kq²/a → +3kq²/a (III)",
     "D: kq²/a − kq²/a − kq²/a = −kq²/a (I)"],
    why="The other codes count only one pair in the triangles or ignore the sign of the −q and −2q charges.",
    ncert="Class 12 Physics, 'Electrostatic Potential and Capacitance', potential energy of a system of charges",
    seconds=60, recomputed=True)
assert (1 * 1) == 1 and (1 * -2) == -2 and 3 * (1 * 1) == 3 and (1 * 1 + 1 * -1 + 1 * -1) == -1

add(T, "Capacitors and dielectrics", "Intermediate", "assertion_reason",
    AR_STEM.format(
        a="The capacitance of an isolated conducting sphere in air is directly proportional to its radius.",
        r="The capacitance of a conductor increases when a larger charge is placed on it."),
    ar("C"),
    "Capacitance of an isolated sphere",
    "A charge Q on an isolated sphere of radius R gives it a potential V = Q/(4πε₀R), so C = Q/V = 4πε₀R, "
    "proportional to R. Capacitance depends only on the size, shape and surroundings of the conductor: doubling "
    "the charge doubles the potential and leaves Q/V unchanged.",
    ["V = Q/(4πε₀R) → C = 4πε₀R ∝ R (A true)", "Q/V is independent of Q (R false)"],
    why="R is false because capacitance does not depend on the charge, so options A, B and D are wrong.",
    ncert="Class 12 Physics, 'Electrostatic Potential and Capacitance', capacitors and capacitance", seconds=45)

qA, qB = 8e-6, -2e-6
each = (qA + qB) / 2
moved = (each - qB) / 1.6e-19
assert close(each, 3e-6) and round(moved / 1e13, 3) == 3.125
multi_key([close(each, 3e-6), True, False, round(moved / 1e13, 3) == 3.125, each > 0], "abde")
add(T, "Coulomb's law and superposition", "Intermediate", "multi_statement",
    multi("Two identical small conducting spheres A and B carry charges of +8 μC and −2 μC. They are touched together "
          "and then separated. Take the magnitude of the electronic charge as 1.6 × 10⁻¹⁹ C. Which of the following "
          "statements are correct?",
          ["After separation, each sphere carries a charge of +3 μC.",
           "The total charge of the two spheres is the same before and after the contact.",
           "During the contact, electrons flow from A to B.",
           "About 3.1 × 10¹³ electrons are transferred during the contact.",
           "After separation, the spheres repel each other."]),
    place("(a), (b), (d) and (e) only", ["(a), (b) and (c) only", "(b), (c), (d) and (e) only",
                                         "(a), (c) and (e) only"], "C"),
    "Conservation of charge in charge sharing",
    "Charge is conserved, and identical spheres in contact share the total charge equally: (8 − 2)/2 = +3 μC each. "
    "B goes from −2 μC to +3 μC, so it loses 5 μC worth of electrons, which go to A.",
    ["(a) (8 + (−2))/2 = +3 μC (true)", "(b) +6 μC before and after (true)",
     "(c) B (negative) gives electrons to A: flow is from B to A (false)",
     "(d) n = 5 × 10⁻⁶/1.6 × 10⁻¹⁹ ≈ 3.1 × 10¹³ (true)", "(e) both +3 μC → repulsion (true)"],
    why="(c) reverses the direction of electron flow; options with (c) or without (d) are wrong.",
    ncert="Class 12 Physics, 'Electric Charges and Fields', conservation and quantisation of charge", seconds=90,
    recomputed=True)

m_b, L_t = 0.9e-3, 0.1 * math.sqrt(2)
r_sep = 2 * L_t * math.sin(math.radians(45))
Fe = m_b * g * math.tan(math.radians(45))
q_b = math.sqrt(Fe * r_sep ** 2 / k)
assert close(r_sep, 0.2) and close(Fe, 9e-3) and close(q_b, 2e-7)
assert close(math.sqrt(Fe * (L_t * math.sin(math.radians(45))) ** 2 / k), 1e-7)
assert round(math.sqrt(m_b * g * math.sin(math.radians(45)) * r_sep ** 2 / k) * 1e6, 2) == 0.17
add(T, "Coulomb's law and superposition", "Advanced", "numerical",
    "Two identical small balls, each of mass 0.9 g and carrying equal charges, hang in air from the same point by "
    "light insulating threads, each 0.1√2 m long. In equilibrium each thread makes an angle of 45° with the "
    "vertical. Taking g = 10 m/s² and 1/(4πε₀) = 9 × 10⁹ N m² C⁻², the charge on each ball is:",
    place("0.2 μC", ["0.1 μC", "about 0.17 μC", "0.4 μC"], "B"),
    "Equilibrium under gravity, tension and Coulomb force",
    "Each ball is in equilibrium under its weight, the thread's tension and the horizontal Coulomb repulsion. "
    "Resolving: T cos θ = mg and T sin θ = F, so F = mg tan θ. The distance between the balls is 2L sin θ.",
    ["Separation r = 2 × 0.1√2 × sin 45° = 0.2 m", "F = mg tan 45° = 0.9 × 10⁻³ × 10 = 9 × 10⁻³ N",
     "kq²/r² = F → q² = 9 × 10⁻³ × 0.04/(9 × 10⁹) = 4 × 10⁻¹⁴", "q = 2 × 10⁻⁷ C = 0.2 μC"],
    why="0.1 μC takes the separation as L sin θ = 0.1 m (one thread's horizontal reach). About 0.17 μC uses "
        "F = mg sin θ. 0.4 μC doubles the separation again.",
    ncert="Class 12 Physics, 'Electric Charges and Fields', Coulomb's law", seconds=120, recomputed=True)
assert close(math.sqrt(Fe * 0.4 ** 2 / k), 4e-7)

a_s, b_s, Q_out = 0.1, 0.2, 6e-9
q_in = -Q_out * a_s / b_s
assert close(q_in, -3e-9) and close(k * q_in / a_s + k * Q_out / b_s, 0)
add(T, "Electric potential and energy", "Advanced", "numerical",
    "Two thin concentric conducting spherical shells have radii 10 cm and 20 cm. The outer shell is given a charge "
    "of +6 nC. The inner shell is then connected to the earth through a thin insulated wire passing through a small "
    "hole in the outer shell. The charge that appears on the inner shell is:",
    place("−3 nC", ["zero", "−6 nC", "+3 nC"], "B"),
    "Earthed conductor: potential zero, not charge zero",
    "Connecting the inner shell to the earth makes its potential zero (taken equal to the potential at infinity). "
    "The potential of the inner shell is due to its own charge q (k q/a) and to the outer shell's charge Q, which "
    "contributes kQ/b at every point inside the outer shell.",
    ["V_inner = kq/a + kQ/b = 0", "q = −Q a/b = −6 × (10/20) = −3 nC"],
    why="'Zero' assumes an earthed conductor must be uncharged. −6 nC assumes the inner shell must cancel the outer "
        "charge completely. +3 nC has the wrong sign.",
    ncert="Class 12 Physics, 'Electrostatic Potential and Capacitance', potential due to a system of charges and "
          "electrostatics of conductors", seconds=120, recomputed=True)

E_u = 100
VA, VB, VC = 0, -E_u * 2, -E_u * 2
qt = 1e-6
multi_key([VA - VB == 200, VB == VC, close(qt * (VA - VC), 2e-4), qt * (VB - VC) == 0,
           close(VA - VC, E_u * math.hypot(2, 3))], "abcd")
add(T, "Electric potential and energy", "Advanced", "multi_statement",
    multi("A uniform electric field of 100 V/m points along the +x direction. Points A, B and C have coordinates "
          "(0, 0), (2 m, 0) and (2 m, 3 m). Which of the following statements are correct?",
          ["The potential at A is 200 V higher than the potential at B.",
           "B and C are at the same potential.",
           "The work done by the field on a charge of +1 μC moved from A to C is 2 × 10⁻⁴ J.",
           "The work done by the field on a charge of +1 μC moved from B to C is zero.",
           "The potential difference between A and C is about 360 V, since A and C are √13 m apart."]),
    place("(a), (b), (c) and (d) only", ["(a), (b) and (e) only", "(b), (c), (d) and (e) only",
                                         "(a), (d) and (e) only"], "C"),
    "Potential in a uniform field",
    "In a uniform field E along x, V = −Ex + constant: the potential falls by E per metre along the field and does "
    "not change perpendicular to it. Work done by the field on q is q(V_initial − V_final), independent of path.",
    ["(a) V_A − V_B = 100 × 2 = 200 V (true)", "(b) B and C differ only in y → same potential (true)",
     "(c) W = q(V_A − V_C) = 10⁻⁶ × 200 = 2 × 10⁻⁴ J (true)", "(d) V_B = V_C → zero work (true)",
     "(e) Only the component of AC along the field (2 m) counts → 200 V, not 360 V (false)"],
    why="(e) multiplies the field by the full distance AC instead of the displacement along the field.",
    ncert="Class 12 Physics, 'Electrostatic Potential and Capacitance', equipotential surfaces and relation between "
          "field and potential", seconds=120, recomputed=True)

add(T, "Capacitors and dielectrics", "Advanced", "assertion_reason",
    AR_STEM.format(
        a="When a dielectric slab is brought near the edge of the gap between the plates of a charged capacitor "
          "that has been disconnected from its battery, the slab is pulled into the gap.",
        r="With the charge Q fixed, the stored energy Q²/2C decreases as the slab enters and the capacitance "
          "increases, so the electric forces do positive work on the slab as it moves in."),
    ar("A"),
    "Force on a dielectric from the energy of an isolated capacitor",
    "For an isolated capacitor the charge stays fixed. As more of the gap is filled with dielectric, C rises and the "
    "stored energy Q²/2C falls. Energy released this way is the work done by the field's forces on the slab, so the "
    "force on the slab points inward, into the gap.",
    ["Q fixed; C increases as the slab enters", "U = Q²/2C decreases → field does positive work on the slab",
     "Hence the slab is drawn in (A), as R explains"],
    why="R gives the energy argument that fixes the direction of the force, so it explains A; B, C and D are wrong.",
    ncert="Class 12 Physics, 'Electrostatic Potential and Capacitance', effect of dielectric on capacitance and "
          "energy stored in a capacitor", seconds=75)

add(T, "Gauss's law", "Advanced", "statement_pair",
    SP_STEM.format(
        s1="For two thin concentric conducting spherical shells, the potential difference between the inner and the "
           "outer shell depends only on the charge on the inner shell, and not on the charge on the outer shell.",
        s2="The electric field in the region between the two shells depends on the charge carried by the outer "
           "shell."),
    sp("C"),
    "Field between concentric shells from Gauss's law",
    "A Gaussian sphere drawn between the shells encloses only the inner shell's charge q, so the field there is "
    "kq/r², whatever the outer shell carries (a uniform shell produces no field inside itself). The potential "
    "difference is the integral of this field, kq(1/a − 1/b), so it too depends only on q. The outer charge adds "
    "the same constant kQ/b to the potentials of both shells.",
    ["Between shells: E = kq/r² (outer charge contributes nothing) → Statement II false",
     "V_inner − V_outer = kq(1/a − 1/b), independent of Q → Statement I true"],
    why="Statement II forgets that the outer shell's charge produces no field anywhere inside it.",
    ncert="Class 12 Physics, 'Electric Charges and Fields', applications of Gauss's law (field due to a uniformly "
          "charged thin spherical shell)", seconds=75)
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
    doc = {"schema_version": "1.0", "batch_id": "BATCH_006", "created_at": TODAY,
           "notes": "BATCH_006 package PHY_006_p1: 131 original Physics questions (Physics and Measurement through "
                    "Electrostatics). Every numerical answer is re-derived in tools/batch_006/PHY_006_p1.py.",
           "stimuli": [], "questions": QUESTIONS}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {OUT}: {n} questions, {dict(Counter(x['difficulty'] for x in QUESTIONS))}")
    print(f"keys {dict(sorted(keys.items()))}")
    print(f"formats {dict(fmts)}")
