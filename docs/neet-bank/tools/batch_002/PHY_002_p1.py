"""Writes batches/parts/BATCH_002_PHY_p1.json: package PHY_002_p1 of BATCH_002 (128 Physics questions).

Topics: Physics and Measurement, Kinematics, Laws of Motion, Work Energy and Power, Rotational Motion, Gravitation,
Properties of Solids and Liquids, Thermodynamics, Kinetic Theory of Gases, Oscillations and Waves, Electrostatics.
IDs NEET_PHY_000251 .. NEET_PHY_000378, in the order the questions are listed below.

Every computable answer is re-derived with an assert before the file is written, and so is the plan quota. If any
assert fails, nothing is written. Each question's answer position is chosen by hand and fixed.

    python tools/batch_002/PHY_002_p1.py        (run from docs/neet-bank)
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
OUT = ROOT / "batches" / "parts" / "BATCH_002_PHY_p1.json"
PLAN = ROOT / "batches" / "plans" / "BATCH_002_plan.json"
PACKAGE = "PHY_002_p1"
TODAY = "2026-11-16"
LETTERS = "ABCD"
PHY = "Physics"
RECOMPUTED = ("script:recompute", "ai:author-solve", "ai:self-recheck")
AUTHORED = ("ai:author-solve", "ai:self-recheck")
FIRST_ID = 251

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


def sig_figs(s):
    """Significant figures of a decimal string written with a decimal point (NCERT rules)."""
    assert "." in s
    digits = s.replace(".", "").lstrip("0")
    return len(digits)


# =====================================================================================================================
# Physics and Measurement (B2 I3 A2)
# =====================================================================================================================
T = "Physics and Measurement"

add(T, "Dimensional analysis", "Basic", "direct",
    "Which of the following pairs of physical quantities have the same dimensions?",
    place("Work and torque", ["Force and pressure", "Power and work", "Linear momentum and kinetic energy"], "B"),
    "Dimensions of mechanical quantities",
    "Work = force × displacement and torque = force × perpendicular distance. Both are a force multiplied by a "
    "length, so both have dimensions [M L² T⁻²], although torque is not a form of energy.",
    ["Work: [M L T⁻²][L] = [M L² T⁻²]", "Torque: [M L T⁻²][L] = [M L² T⁻²] → same",
     "Force [M L T⁻²] vs pressure [M L⁻¹ T⁻²]; power [M L² T⁻³] vs work [M L² T⁻²]; momentum [M L T⁻¹] vs kinetic "
     "energy [M L² T⁻²] → all different"],
    why="Pressure is force per unit area, power is work per unit time and kinetic energy has an extra factor of "
        "velocity compared with momentum, so each of these pairs differs in dimensions.",
    ncert="Class 11 Physics, 'Units and Measurement', dimensions of physical quantities", seconds=30)

assert [sig_figs(s) for s in ("0.00450", "6.0300", "20.05", "0.70")] == [3, 5, 4, 2]
add(T, "Least count and significant figures", "Basic", "match_list",
    match_stem("Match List-I (measured value) with List-II (number of significant figures in it).",
               ["0.00450", "6.0300", "20.05", "0.70"], ["2", "3", "4", "5"]),
    match_options({"A": "II", "B": "IV", "C": "III", "D": "I"},
                  [{"A": "III", "B": "IV", "C": "II", "D": "I"}, {"A": "I", "B": "IV", "C": "III", "D": "II"},
                   {"A": "II", "B": "III", "C": "IV", "D": "I"}], "C"),
    "Rules for counting significant figures",
    "Leading zeros (zeros before the first non-zero digit) are not significant. Zeros between non-zero digits are "
    "significant. Trailing zeros after the decimal point are significant.",
    ["0.00450 → digits 4, 5, 0 → 3 (II)", "6.0300 → 6, 0, 3, 0, 0 → 5 (IV)", "20.05 → 2, 0, 0, 5 → 4 (III)",
     "0.70 → 7, 0 → 2 (I)"],
    why="The other codes either count the leading zeros of 0.00450, drop the trailing zero of 0.70, or drop the "
        "zeros sandwiched between 2 and 5 in 20.05.",
    ncert="Class 11 Physics, 'Units and Measurement', significant figures", seconds=45)

readings = [1.52, 1.48, 1.55, 1.45, 1.50]
mean_t = sum(readings) / 5
dev = [abs(r - mean_t) for r in readings]
mae = sum(dev) / 5
assert close(mean_t, 1.50) and close(mae, 0.028) and round(mae, 2) == 0.03 and close(max(dev), 0.05)
assert close(sum(dev), 0.14) and abs(sum(r - mean_t for r in readings)) < 1e-9
add(T, "Errors in measurement", "Intermediate", "numerical",
    "The period of a pendulum is measured five times, giving 1.52 s, 1.48 s, 1.55 s, 1.45 s and 1.50 s. The mean "
    "absolute error of these measurements, rounded to two decimal places, is:",
    place("0.03 s", ["0.05 s", "0.00 s", "0.14 s"], "D"),
    "Mean value and mean absolute error",
    "The best estimate is the arithmetic mean of the readings. The absolute error of each reading is the magnitude of "
    "its difference from the mean, and the mean absolute error is the average of these magnitudes.",
    ["Mean = (1.52 + 1.48 + 1.55 + 1.45 + 1.50)/5 = 7.50/5 = 1.50 s",
     "|Δa| = 0.02, 0.02, 0.05, 0.05, 0.00 s; their sum = 0.14 s",
     "Mean absolute error = 0.14/5 = 0.028 s ≈ 0.03 s"],
    why="0.05 s is the largest single deviation, not the mean. 0.00 s averages the signed deviations, which always "
        "cancel. 0.14 s is the sum of the deviations, not divided by 5.",
    ncert="Class 11 Physics, 'Units and Measurement', absolute error, relative error and percentage error",
    seconds=75, recomputed=True)

add(T, "Dimensional analysis", "Intermediate", "direct",
    "Suppose force (F), velocity (v) and time (T) are chosen as the fundamental quantities instead of mass, length "
    "and time. The dimensional formula of mass in this system is:",
    place("[F v⁻¹ T]", ["[F v T⁻¹]", "[F v⁻¹ T⁻¹]", "[F v⁻² T²]"], "A"),
    "Expressing a quantity in a new set of base quantities",
    "Write a physical relation that links mass with F, v and T. From Newton's second law, F = ma = m(v/T), so "
    "m = F T / v.",
    ["F = m × (change in velocity)/(time) → F = m v / T", "m = F T / v → [F v⁻¹ T]",
     "Check: [M L T⁻²][T]/[L T⁻¹] = [M] ✓"],
    why="Check each in M, L, T: [F v T⁻¹] = [M L² T⁻⁴] (it inverts the relation), [F v⁻¹ T⁻¹] = [M T⁻²] and "
        "[F v⁻² T²] = [M L⁻¹ T²]. Only [F v⁻¹ T] reduces to [M].",
    ncert="Class 11 Physics, 'Units and Measurement', dimensional formulae and dimensional equations", seconds=60)

add(T, "Errors in measurement", "Intermediate", "statement_pair",
    SP_STEM.format(
        s1="When two measured quantities are multiplied or divided, the maximum relative error in the result is the "
           "sum of the relative errors in the quantities.",
        s2="When one measured quantity is subtracted from another, the maximum absolute error in the result is the "
           "difference of their absolute errors."),
    sp("C"),
    "Combination of errors",
    "For Z = AB or Z = A/B, ΔZ/Z = ΔA/A + ΔB/B. For Z = A + B or Z = A − B, the maximum absolute error is "
    "ΔZ = ΔA + ΔB in both cases: errors always add in the worst case, even when the quantities are subtracted.",
    ["Statement I: relative errors add for a product or a quotient → true",
     "Statement II: for Z = A − B, ΔZ = ΔA + ΔB (not ΔA − ΔB) → false"],
    why="Statement II is the common trap: subtracting the quantities does not subtract their errors, because the "
        "errors can have either sign and the maximum error is their sum.",
    ncert="Class 11 Physics, 'Units and Measurement', combination of errors", seconds=45)

dL_rel = 0.1 / 100.0          # 1 mm on 100.0 cm
dT_rel = 1 / 40               # 1 s on 40 s for 20 oscillations
g_err = 100 * (dL_rel + 2 * dT_rel)
assert close(g_err, 5.1) and close(100 * (dL_rel + dT_rel), 2.6) and close(100 * 2 * dT_rel, 5.0)
assert close(100 * (dL_rel + 2 * (1 / 2)), 100.1)
add(T, "Errors in measurement", "Advanced", "numerical",
    "In a simple pendulum experiment, g is found from g = 4π²L/T². The length L is measured as 100.0 cm with a scale "
    "of least count 1 mm. The time taken for 20 oscillations is measured as 40 s with a watch of resolution 1 s. The "
    "maximum percentage error in the value of g is:",
    place("5.1%", ["2.6%", "5.0%", "100.1%"], "B"),
    "Percentage error from least counts, and the power rule",
    "The relative error in L is its least count divided by L. Timing 20 oscillations together means the 1 s "
    "resolution applies to the 40 s total, so ΔT/T = 1/40. Since g ∝ L T⁻², the relative error in g is "
    "ΔL/L + 2 ΔT/T.",
    ["ΔL/L = 0.1 cm/100.0 cm = 0.1%", "ΔT/T = Δt/t = 1 s/40 s = 2.5%",
     "Δg/g = 0.1% + 2 × 2.5% = 5.1%"],
    why="2.6% forgets the factor 2 from T². 5.0% ignores the error in L. 100.1% applies the 1 s resolution to a "
        "single period of 2 s instead of to the 40 s total.",
    shortcut="Timing N oscillations divides the timing error by N; that is why the experiment counts many.",
    ncert="Class 11 Physics, 'Units and Measurement', combination of errors", seconds=90, recomputed=True)

add(T, "Dimensional analysis", "Advanced", "multi_statement",
    multi("Which of the following statements are correct?",
          ["A dimensionally correct equation need not be a correct physical relation.",
           "An equation that is dimensionally inconsistent must be wrong.",
           "Dimensional analysis gives the values of the dimensionless constants in a physical relation.",
           "In a number written without a decimal point, the trailing zeros are not significant.",
           "The number of significant figures in a measured value depends on the unit in which it is expressed."]),
    place("(a), (b) and (d) only", ["(a), (b) and (c) only", "(b), (d) and (e) only", "(a), (c), (d) and (e) only"],
          "D"),
    "Uses and limits of dimensional analysis; significant figures",
    "Dimensional consistency is necessary but not sufficient for a relation to be correct. Dimensional analysis "
    "cannot find pure numbers such as 1/2 or 2π. By NCERT's rules, trailing zeros in a number without a decimal "
    "point are not significant, and a change of units does not change the number of significant figures.",
    ["(a) True: e.g. s = ut + at² is dimensionally correct but wrong (the factor 1/2 is missing)",
     "(b) True: terms of different dimensions cannot be equated",
     "(c) False: dimensionless constants cannot be found by this method",
     "(d) True: e.g. 123000 mm has three significant figures",
     "(e) False: 2.308 cm = 0.02308 m = 23.08 mm, all with four significant figures"],
    why="Any option with (c) or (e) includes a false statement; (a), (b) and (d) are all true.",
    ncert="Class 11 Physics, 'Units and Measurement', significant figures and dimensional analysis", seconds=75)


# =====================================================================================================================
# Kinematics (B4 I5 A4)
# =====================================================================================================================
T = "Kinematics"

u = 72 * 1000 / 3600
a_dec = u / 4
s_stop = u * 4 - 0.5 * a_dec * 16
assert close(u, 20) and close(s_stop, 40) and close(u * 4, 80) and close(u * 4 + 0.5 * a_dec * 16, 120)
assert close(72 * 4 / 2, 144)
add(T, "Motion in a straight line", "Basic", "numerical",
    "A car moving along a straight road at 72 km/h is brought to rest with uniform retardation in 4 s. The distance "
    "it covers while stopping is:",
    place("40 m", ["80 m", "120 m", "144 m"], "A"),
    "Equations of uniformly accelerated motion",
    "Convert the speed to m/s. With uniform retardation, the distance is the average velocity multiplied by the "
    "time.",
    ["u = 72 km/h = 72 × 5/18 = 20 m/s; v = 0", "s = (u + v)t/2 = (20 + 0) × 4/2 = 40 m"],
    why="80 m multiplies the initial speed by the time, as if the speed stayed 20 m/s. 120 m adds ½at² instead of "
        "subtracting it (sign of the retardation). 144 m uses 72 without converting km/h to m/s.",
    ncert="Class 11 Physics, 'Motion in a Straight Line', kinematic equations for uniformly accelerated motion",
    seconds=45, recomputed=True)

add(T, "Graphs of motion", "Basic", "direct",
    "Which of the following CANNOT be the position–time graph of a particle moving along a straight line?",
    place("A curve that bends back so that it shows two different positions at the same instant of time",
          ["A straight line parallel to the time axis", "A straight line inclined to the time axis",
           "A parabola with its vertex on the position axis"], "C"),
    "Physical meaning of a position–time graph",
    "At any one instant a particle can be at only one position. A graph that gives two positions for the same time "
    "therefore cannot describe a real motion.",
    ["Line parallel to the time axis → particle at rest", "Inclined straight line → uniform velocity",
     "Parabola → uniformly accelerated motion", "Two positions at one instant → impossible"],
    why="The other three graphs describe rest, uniform motion and uniformly accelerated motion, all of which are "
        "possible.",
    ncert="Class 11 Physics, 'Motion in a Straight Line', position-time graphs", seconds=30)

Av, Bv = (2, 3, -1), (1, -1, 1)
dot = sum(x * y for x, y in zip(Av, Bv))
assert dot == -2 and 2 - 3 + 1 == 0 and 2 + 3 + 1 == 6 and 2 + 3 - 1 == 4
add(T, "Vectors", "Basic", "numerical",
    "For the vectors A = 2î + 3ĵ − k̂ and B = î − ĵ + k̂, the scalar product A · B is:",
    place("−2", ["0", "6", "4"], "D"),
    "Scalar product in component form",
    "A · B = AₓBₓ + A_yB_y + A_zB_z, keeping the sign of every component.",
    ["AₓBₓ = 2 × 1 = 2", "A_yB_y = 3 × (−1) = −3", "A_zB_z = (−1) × 1 = −1", "A · B = 2 − 3 − 1 = −2"],
    why="0 takes (−1)(1) as +1. 6 adds the products without their signs. 4 takes 3 × (−1) as +3 and gets the k̂ "
        "term right.",
    ncert="Class 11 Physics, 'Work, Energy and Power', the scalar product", seconds=30, recomputed=True)

omega = 2 * math.pi * 2
a_c = omega ** 2 * 0.5
assert close(a_c, 8 * math.pi ** 2) and close(omega * 0.5, 2 * math.pi) and close(2 ** 2 * 0.5, 2)
assert close(omega ** 2 / 0.5, 32 * math.pi ** 2)
add(T, "Uniform circular motion", "Basic", "numerical",
    "A particle moves along a circle of radius 0.5 m at a constant rate of 2 revolutions per second. The magnitude of "
    "its centripetal acceleration is:",
    place("8π² m/s²", ["2π m/s²", "2 m/s²", "32π² m/s²"], "B"),
    "Centripetal acceleration a = ω²r",
    "Convert the frequency to angular speed (ω = 2πν) and use a = ω²r.",
    ["ω = 2π × 2 = 4π rad/s", "a = ω²r = 16π² × 0.5 = 8π² m/s² (≈ 79 m/s²)"],
    why="2π is the speed v = ωr in m/s, not the acceleration. 2 m/s² uses ω = 2 rad/s, mistaking rev/s for rad/s. "
        "32π² m/s² divides by r instead of multiplying.",
    ncert="Class 11 Physics, 'Motion in a Plane', uniform circular motion", seconds=40, recomputed=True)

t_cross = (100 + 150) / (20 + 30)
assert t_cross == 5 and (100 + 150) / (30 - 20) == 25 and 150 / 50 == 3 and 100 / 50 == 2
add(T, "Relative velocity", "Intermediate", "numerical",
    "Two trains, 100 m and 150 m long, move on parallel tracks in opposite directions with speeds of 20 m/s and "
    "30 m/s. The time they take to cross each other completely is:",
    place("5 s", ["25 s", "3 s", "2 s"], "C"),
    "Relative velocity in one dimension",
    "In the frame of one train, the other approaches with the relative speed 20 + 30 = 50 m/s and must cover the sum "
    "of the two lengths before they have fully passed.",
    ["Relative speed (opposite directions) = 20 + 30 = 50 m/s", "Distance = 100 + 150 = 250 m",
     "t = 250/50 = 5 s"],
    why="25 s uses the difference of speeds (trains moving the same way). 3 s and 2 s use the length of only one "
        "train.",
    ncert="Class 11 Physics, 'Motion in a Straight Line', relative velocity", seconds=45, recomputed=True)

th = math.atan(4)
uu, gg = 20.0, 10.0
R_ = uu ** 2 * math.sin(2 * th) / gg
H_ = uu ** 2 * math.sin(th) ** 2 / (2 * gg)
assert close(R_, H_)
th2 = math.atan(2)
assert close(uu ** 2 * math.sin(2 * th2) / gg, uu ** 2 * math.sin(th2) ** 2 / gg)
add(T, "Projectile motion", "Intermediate", "numerical",
    "A projectile is launched from level ground, and its horizontal range turns out to be equal to the maximum "
    "height it reaches. Neglecting air resistance, the angle of projection above the horizontal is:",
    place("tan⁻¹(4)", ["tan⁻¹(1/4)", "45°", "tan⁻¹(2)"], "D"),
    "Range and maximum height of a projectile",
    "Write R = u² sin 2θ / g and H = u² sin²θ / (2g), set them equal and solve for tan θ.",
    ["u² (2 sin θ cos θ)/g = u² sin²θ/(2g)", "2 cos θ = sin θ / 2 → tan θ = 4", "θ = tan⁻¹(4) ≈ 76°"],
    why="tan⁻¹(1/4) inverts the ratio. 45° is the angle for maximum range, not for R = H. tan⁻¹(2) uses "
        "H = u² sin²θ / g, dropping the 2 in the denominator.",
    shortcut="R = 4H cot θ for any projectile on level ground, so R = H gives tan θ = 4.",
    ncert="Class 11 Physics, 'Motion in a Plane', projectile motion", seconds=60, recomputed=True)

a_nth = F(10) / (F(2 * 3 - 1, 2))
assert a_nth == 4 and F(10) / 5 == 2 and F(10 * 2, 9) == F(20, 9)
add(T, "Motion in a straight line", "Intermediate", "numerical",
    "A body starts from rest and moves along a straight line with uniform acceleration. It covers 10 m during the "
    "third second of its motion. Its acceleration is:",
    place("4 m/s²", ["2 m/s²", "2.2 m/s²", "3.3 m/s²"], "A"),
    "Distance covered in the nth second",
    "The distance covered in the nth second is the distance in n seconds minus that in (n − 1) seconds: "
    "sₙ = u + a(2n − 1)/2.",
    ["s(3 s) − s(2 s) = ½a(3² − 2²) = 2.5a", "2.5a = 10 → a = 4 m/s²"],
    why="2 m/s² drops the factor ½ (uses sₙ = a(2n − 1)). 2.2 m/s² (= 20/9) treats 10 m as the distance in the first "
        "3 s. 3.3 m/s² divides the distance by the time as if it were a velocity gained per second.",
    ncert="Class 11 Physics, 'Motion in a Straight Line', kinematic equations for uniformly accelerated motion",
    seconds=50, recomputed=True)

add(T, "Vectors", "Intermediate", "assertion_reason",
    AR_STEM.format(
        a="The magnitude of the resultant of two vectors can never exceed the sum of their magnitudes.",
        r="For two vectors of magnitudes A and B inclined at an angle θ, the resultant R satisfies "
          "R² = A² + B² + 2AB cos θ, and cos θ can never exceed 1."),
    ar("A"),
    "Triangle (parallelogram) law of vector addition",
    "From R² = A² + B² + 2AB cos θ, the largest value of R occurs at cos θ = 1 (θ = 0), when R = A + B. For every "
    "other angle R < A + B. So the formula in R directly shows why A is true.",
    ["R² = A² + B² + 2AB cos θ ≤ A² + B² + 2AB = (A + B)²", "So R ≤ A + B, with equality only for parallel vectors",
     "A is true and R gives the reason → option A"],
    why="Both statements are true, and A follows directly from R, so B, C and D do not fit.",
    ncert="Class 11 Physics, 'Motion in a Plane', addition of vectors: analytical method", seconds=50)

add(T, "Projectile motion", "Intermediate", "multi_statement",
    multi("A projectile is launched from level ground at 60° above the horizontal and lands back on the same level "
          "ground. Neglecting air resistance, which of the following statements are correct?",
          ["At the highest point, its speed is half its speed of projection.",
           "At the highest point, its acceleration is zero.",
           "At the highest point, its kinetic energy is one-fourth of its initial kinetic energy.",
           "The time taken to reach the highest point is half the total time of flight.",
           "Its horizontal range is the maximum possible for this speed of projection."]),
    place("(a), (c) and (d) only",
          ["(a), (b) and (d) only", "(c), (d) and (e) only", "(a), (c), (d) and (e) only"], "B"),
    "Velocity, acceleration and energy along a projectile's path",
    "At the top, only the horizontal velocity u cos θ remains; the acceleration is still g downward. For launch and "
    "landing at the same level the path is symmetric, so the rise takes half the flight time. Maximum range needs "
    "θ = 45°.",
    ["(a) v_top = u cos 60° = u/2 → true", "(b) acceleration = g at every point → false",
     "(c) KE_top = ½m(u/2)² = ¼ × ½mu² → true", "(d) symmetric path → t_rise = T/2 → true",
     "(e) range is maximum at 45°, not 60° → false"],
    why="Options with (b) or (e) include a false statement; only (a), (c) and (d) are all true.",
    ncert="Class 11 Physics, 'Motion in a Plane', projectile motion", seconds=75)

t_fall = (10 + math.sqrt(100 + 4 * 5 * 40)) / (2 * 5)
xr = 20 * math.cos(math.radians(30)) * t_fall
assert close(t_fall, 4) and close(xr, 40 * math.sqrt(3))
assert close(20 * math.cos(math.radians(30)) * 2, 20 * math.sqrt(3)) and close(20 * 0.5 * 4, 40) and 20 * 4 == 80
add(T, "Projectile motion", "Advanced", "numerical",
    "A ball is thrown from the top of a building 40 m high with a speed of 20 m/s at 30° above the horizontal. Taking "
    "g = 10 m/s² and neglecting air resistance, the horizontal distance from the foot of the building at which the "
    "ball hits the level ground is:",
    place("40√3 m", ["20√3 m", "40 m", "80 m"], "C"),
    "Projectile launched from a height",
    "Find the time of flight from the vertical motion, taking upward as positive and the landing point 40 m below "
    "the launch point; then multiply by the constant horizontal velocity.",
    ["uₓ = 20 cos 30° = 10√3 m/s; u_y = 20 sin 30° = 10 m/s", "−40 = 10t − 5t² → t² − 2t − 8 = 0 → t = 4 s",
     "x = 10√3 × 4 = 40√3 m ≈ 69 m"],
    why="20√3 m uses the level-ground flight time of 2 s. 40 m uses the vertical component (u sin 30°) for the "
        "horizontal motion. 80 m multiplies the full speed by the time.",
    ncert="Class 11 Physics, 'Motion in a Plane', projectile motion", seconds=100, recomputed=True)

t_b = (5 + math.sqrt(25 + 4 * 5 * 30)) / (2 * 5)
assert close(t_b, 3) and close(math.sqrt(2 * 30 / 10), math.sqrt(6))
assert close((-5 + math.sqrt(25 + 600)) / 10, 2) and close(2 * 5 / 10, 1)
add(T, "Motion in a straight line", "Advanced", "numerical",
    "A balloon is rising vertically with a constant speed of 5 m/s. When it is 30 m above the ground, a packet is "
    "released from it. Taking g = 10 m/s² and neglecting air resistance, the time the packet takes to reach the "
    "ground is:",
    place("3 s", ["√6 s", "2 s", "1 s"], "A"),
    "Free fall with an initial upward velocity",
    "At release the packet has the balloon's velocity, 5 m/s upward. With upward positive, its displacement on "
    "reaching the ground is −30 m.",
    ["−30 = 5t − ½(10)t²", "5t² − 5t − 30 = 0 → t² − t − 6 = 0", "(t − 3)(t + 2) = 0 → t = 3 s"],
    why="√6 s (≈ 2.45 s) ignores the packet's initial upward velocity. 2 s takes that velocity as downward. 1 s is "
        "only the time for the packet to rise and come back to the release point.",
    ncert="Class 11 Physics, 'Motion in a Straight Line', kinematic equations for uniformly accelerated motion",
    seconds=80, recomputed=True)

# A at origin moving east 6 m/s; B at (0, 80) moving south 8 m/s.  r_BA(t) = (-6t, 80 - 8t)
ts = 80 * 8 / (6 ** 2 + 8 ** 2)
dmin = math.hypot(-6 * ts, 80 - 8 * ts)
assert close(ts, 6.4) and close(dmin, 48) and close(80 * 8 / 10, 64)
assert all(math.hypot(-6 * t, 80 - 8 * t) >= dmin - 1e-9 for t in [i / 100 for i in range(0, 2000)])
add(T, "Relative velocity", "Advanced", "numerical",
    "Two ships P and Q are on a calm sea. Initially Q is 80 m due north of P. P sails due east at 6 m/s and Q sails "
    "due south at 8 m/s, both with constant velocities. The minimum distance between the two ships is:",
    place("48 m", ["0 m", "64 m", "80 m"], "D"),
    "Relative velocity and closest approach",
    "In P's frame, Q moves in a straight line with the relative velocity v_QP = v_Q − v_P. The minimum separation is "
    "the perpendicular distance from P to this line.",
    ["v_QP = (−6, −8) m/s → |v_QP| = 10 m/s; initial position of Q relative to P = (0, 80) m",
     "Angle between the line PQ (north) and v_QP: sin α = 6/10 = 0.6",
     "d_min = 80 × sin α = 80 × 0.6 = 48 m (reached at t = 6.4 s)"],
    why="0 m assumes the ships collide, but their relative velocity does not point along PQ. 64 m uses cos α (0.8) "
        "instead of sin α. 80 m assumes the separation never decreases.",
    ncert="Class 11 Physics, 'Motion in a Plane', relative velocity in two dimensions", seconds=120, recomputed=True)

add(T, "Uniform circular motion", "Advanced", "match_list",
    match_stem("Match List-I (motion) with List-II (description of its velocity and acceleration). Neglect air "
               "resistance.",
               ["A particle in uniform circular motion",
                "A ball projected at 30° above the horizontal, during its flight",
                "A car moving with constant velocity on a straight road",
                "A ball thrown vertically upward, at its highest point"],
               ["Zero acceleration with non-zero velocity", "Zero velocity with non-zero acceleration",
                "Acceleration of constant magnitude whose direction keeps changing",
                "Constant acceleration (in magnitude and direction) along a curved path"]),
    match_options({"A": "III", "B": "IV", "C": "I", "D": "II"},
                  [{"A": "IV", "B": "III", "C": "I", "D": "II"}, {"A": "III", "B": "II", "C": "I", "D": "IV"},
                   {"A": "III", "B": "IV", "C": "II", "D": "I"}], "B"),
    "Velocity and acceleration in different kinds of motion",
    "In uniform circular motion the acceleration v²/R always points to the centre, so its direction changes. A "
    "projectile has the constant acceleration g but a parabolic path. Uniform straight-line motion has no "
    "acceleration. At the top of a vertical throw the velocity is momentarily zero but the acceleration is still g.",
    ["A: centripetal acceleration, constant magnitude, changing direction → III",
     "B: acceleration g (constant), parabolic path → IV", "C: constant velocity → zero acceleration → I",
     "D: v = 0 at the top, a = g downward → II"],
    why="The other codes swap the circular and projectile motions (both curved), or assume that zero velocity at the "
        "top of a vertical throw means zero acceleration.",
    ncert="Class 11 Physics, 'Motion in a Plane', projectile motion and uniform circular motion", seconds=60)


# =====================================================================================================================
# Laws of Motion (B4 I5 A4)
# =====================================================================================================================
T = "Laws of Motion"

v_imp = 50 * 0.2 / 2
assert v_imp == 5 and 50 * 0.2 == 10 and 50 / 2 == 25 and 50 * 0.2 * 2 == 20
add(T, "Newton's laws and impulse", "Basic", "numerical",
    "A ball of mass 2 kg is at rest on a smooth horizontal surface. A horizontal force of 50 N acts on it for 0.2 s. "
    "The speed of the ball just after the force stops acting is:",
    place("5 m/s", ["10 m/s", "25 m/s", "20 m/s"], "C"),
    "Impulse–momentum theorem",
    "The impulse of a constant force, F Δt, equals the change in momentum of the body.",
    ["Impulse = F Δt = 50 × 0.2 = 10 N s", "Δp = m v − 0 = 10 → v = 10/2 = 5 m/s"],
    why="10 m/s reports the impulse (in N s) as the speed, without dividing by the mass. 25 m/s is the acceleration "
        "F/m, not the speed. 20 m/s multiplies the impulse by the mass instead of dividing.",
    ncert="Class 11 Physics, 'Laws of Motion', impulse", seconds=30, recomputed=True)

add(T, "Newton's laws and impulse", "Basic", "direct",
    "A book rests on a horizontal table. According to Newton's third law, the reaction to the gravitational force "
    "exerted by the Earth on the book is:",
    place("The gravitational force exerted by the book on the Earth",
          ["The normal force exerted by the table on the book", "The force exerted by the book on the table",
           "The force of friction exerted by the table on the book"], "D"),
    "Action–reaction pairs",
    "An action–reaction pair consists of two forces of the same kind that two bodies exert on each other. The Earth "
    "pulls the book gravitationally, so the reaction is the book's gravitational pull on the Earth.",
    ["Action: gravitational force of the Earth on the book", "Reaction: gravitational force of the book on the Earth",
     "The table's normal force also acts on the book, so it cannot be the reaction to a force on the book"],
    why="The normal force balances the weight, but it acts on the same body (the book), so it is not the third-law "
        "pair. The book's push on the table is the reaction to the normal force. There is no friction on a book "
        "resting on a horizontal table with no other horizontal force.",
    ncert="Class 11 Physics, 'Laws of Motion', Newton's third law of motion", seconds=40)

m_h, g = 3, 10
F_h = m_h * g * F(3, 4)
T_s = m_h * g / F(4, 5)
assert F_h == F(45, 2) and T_s == F(75, 2) and m_h * g * F(3, 5) == 18 and m_h * g * F(4, 3) == 40
add(T, "Equilibrium of concurrent forces", "Basic", "numerical",
    "A block of mass 3 kg hangs from a light string tied to a fixed hook. A horizontal force F pulls the block "
    "aside, and it stays at rest with the string at 37° to the vertical. Taking g = 10 m/s², sin 37° = 0.6 and "
    "cos 37° = 0.8, F is:",
    place("22.5 N", ["37.5 N", "18 N", "40 N"], "A"),
    "Equilibrium of three concurrent forces",
    "Three forces act on the block: its weight mg, the tension T along the string and the horizontal force F. "
    "Resolving: T cos 37° = mg and T sin 37° = F, so F = mg tan 37°.",
    ["T cos 37° = 30 N → T = 30/0.8 = 37.5 N", "F = T sin 37° = 37.5 × 0.6 = 22.5 N (= mg tan 37°)"],
    why="37.5 N is the tension, not F. 18 N uses mg sin 37°. 40 N uses mg cot 37°, mixing up the components.",
    ncert="Class 11 Physics, 'Laws of Motion', equilibrium of a particle", seconds=50, recomputed=True)

lim = 0.5 * 4 * 10
a_fr = (25 - 0.3 * 4 * 10) / 4
assert lim == 20 and 25 > lim and close(a_fr, 3.25) and close((25 - lim) / 4, 1.25) and close(25 / 4, 6.25)
add(T, "Friction", "Basic", "numerical",
    "A block of mass 4 kg rests on a horizontal floor. The coefficients of static and kinetic friction between them "
    "are 0.5 and 0.3. A horizontal force of 25 N is applied to the block. Taking g = 10 m/s², the acceleration of "
    "the block is:",
    place("3.25 m/s²", ["1.25 m/s²", "6.25 m/s²", "0"], "B"),
    "Static and kinetic friction",
    "First check whether the block moves: the applied force must exceed the limiting static friction μₛN. Once it "
    "slides, kinetic friction μₖN opposes the motion.",
    ["Limiting friction = 0.5 × 40 = 20 N < 25 N → the block slides",
     "Kinetic friction = 0.3 × 40 = 12 N", "a = (25 − 12)/4 = 3.25 m/s²"],
    why="1.25 m/s² uses the static coefficient for a sliding block. 6.25 m/s² ignores friction. 0 assumes the block "
        "stays at rest, but 25 N exceeds the limiting friction of 20 N.",
    ncert="Class 11 Physics, 'Laws of Motion', friction", seconds=50, recomputed=True)

v_boat = F(60 * 2, 120)
assert v_boat == 1 and F(60 * 2, 180) == F(2, 3) and F(120 * 2, 60) == 4
add(T, "Conservation of linear momentum", "Intermediate", "numerical",
    "A man of mass 60 kg stands at rest in a boat of mass 120 kg floating at rest on still water. He jumps off "
    "horizontally with a velocity of 2 m/s relative to the ground. Neglecting water resistance, the speed with which "
    "the boat moves back is:",
    place("1 m/s", ["2 m/s", "0.67 m/s", "4 m/s"], "C"),
    "Conservation of linear momentum",
    "No external horizontal force acts on the man–boat system, so its total horizontal momentum stays zero.",
    ["Initial momentum = 0", "60 × 2 + 120 × V = 0 → V = −1 m/s", "The boat moves back at 1 m/s"],
    why="2 m/s assumes equal speeds for unequal masses. 0.67 m/s adds the man's mass to the boat's after he has left "
        "it. 4 m/s inverts the mass ratio.",
    ncert="Class 11 Physics, 'Laws of Motion', conservation of momentum", seconds=45, recomputed=True)

add(T, "Newton's laws and impulse", "Intermediate", "match_list",
    match_stem("A person of mass m stands on a weighing scale inside a lift. Match List-I (motion of the lift) with "
               "List-II (reading of the scale, in newtons). Here a is the magnitude of the lift's acceleration "
               "(a < g).",
               ["Moving upward with constant velocity", "Moving upward with increasing speed",
                "Moving upward with decreasing speed", "Falling freely after its cable breaks"],
               ["Zero", "mg", "m(g + a)", "m(g − a)"]),
    match_options({"A": "II", "B": "III", "C": "IV", "D": "I"},
                  [{"A": "II", "B": "IV", "C": "III", "D": "I"}, {"A": "I", "B": "III", "C": "IV", "D": "II"},
                   {"A": "II", "B": "III", "C": "I", "D": "IV"}], "A"),
    "Apparent weight in an accelerating lift",
    "The scale reads the normal force N. From N − mg = m a_up, N = m(g + a_up). What matters is the direction of the "
    "acceleration, not of the velocity.",
    ["A: a = 0 → N = mg → II", "B: speeding up while going up → a upward → N = m(g + a) → III",
     "C: slowing down while going up → a downward → N = m(g − a) → IV", "D: free fall → a = g downward → N = 0 → I"],
    why="The commonest error is to give m(g + a) for any upward motion. A lift moving up but slowing down has a "
        "downward acceleration, so the reading falls below mg.",
    ncert="Class 11 Physics, 'Laws of Motion', Newton's second law of motion", seconds=60)

v_max = math.sqrt(0.5 * 45 * 10)
assert close(v_max, 15) and close(v_max * 3.6, 54) and close(math.sqrt(45 * 10 / 0.5) * 3.6, 108)
assert close(math.sqrt(45 * 10) * 3.6, 76.4)
add(T, "Circular motion: level and banked roads", "Intermediate", "numerical",
    "A car takes a turn of radius 45 m on a level (unbanked) road. The coefficient of static friction between the "
    "tyres and the road is 0.5. Taking g = 10 m/s², the maximum speed at which the car can take the turn without "
    "skidding is:",
    place("54 km/h", ["15 km/h", "108 km/h", "76 km/h"], "D"),
    "Friction as the centripetal force on a level road",
    "On a level road, static friction alone provides the centripetal force: mv²/r ≤ μₛmg, so v_max = √(μₛrg).",
    ["v_max = √(0.5 × 45 × 10) = √225 = 15 m/s", "15 m/s × 18/5 = 54 km/h"],
    why="15 km/h forgets to convert m/s to km/h. 108 km/h (30 m/s) divides by μₛ instead of multiplying. 76 km/h "
        "(≈ 21.2 m/s) leaves μₛ out altogether.",
    ncert="Class 11 Physics, 'Laws of Motion', circular motion", seconds=50, recomputed=True)

add(T, "Friction", "Intermediate", "statement_pair",
    SP_STEM.format(
        s1="A block placed on a rough inclined plane remains at rest if the angle of inclination is less than the "
           "angle of repose θᵣ, where tan θᵣ = μₛ.",
        s2="For a block resting on a rough inclined plane whose angle of inclination θ is less than the angle of "
           "repose, the static friction acting on the block is mg sin θ, up the plane."),
    sp("A"),
    "Angle of repose and self-adjusting static friction",
    "The block is on the verge of sliding when mg sin θ = μₛ mg cos θ, i.e. tan θ = μₛ. Below this angle the block "
    "stays at rest, and static friction adjusts itself to exactly balance the component of gravity along the plane.",
    ["Statement I: block slips only when tan θ exceeds μₛ → true",
     "Statement II: at rest, net force along the plane is zero → f = mg sin θ (less than μₛmg cos θ) → true"],
    why="Statement II is not the limiting friction μₛmg cos θ: static friction equals mg sin θ, which is smaller "
        "than the limiting value when θ < θᵣ. Both statements are true.",
    ncert="Class 11 Physics, 'Laws of Motion', friction", seconds=50)

add(T, "Newton's laws and impulse", "Intermediate", "assertion_reason",
    AR_STEM.format(
        a="A cricketer moves his hands backward while catching a fast-moving ball.",
        r="Moving the hands back increases the time over which the ball's momentum is reduced to zero, so the "
          "average force exerted on the hands is smaller."),
    ar("A"),
    "Impulse: F_avg = Δp/Δt",
    "The change in momentum of the ball is fixed by its mass and speed. Spreading that change over a longer time "
    "reduces the average force, which is exactly why the cricketer draws his hands back.",
    ["Δp = m v (fixed)", "F_avg = Δp/Δt; larger Δt → smaller F_avg", "R explains A → option A"],
    why="Both statements are true and R is the reason for A, so B, C and D do not fit.",
    ncert="Class 11 Physics, 'Laws of Motion', impulse", seconds=40)

a_t = (3 * 10 - 0.25 * 2 * 10) / (2 + 3)
T_t = 2 * a_t + 0.25 * 2 * 10
assert close(a_t, 5) and close(T_t, 15) and close(3 * 10 - 3 * a_t, 15)
assert close(2 * (30 / 5), 12) and close(2 * a_t, 10)
add(T, "Friction", "Advanced", "numerical",
    "A block of mass 2 kg lies on a rough horizontal table (coefficient of kinetic friction 0.25). It is tied to a "
    "light inextensible string that passes over a smooth, light pulley at the edge of the table and carries a hanging "
    "block of mass 3 kg. When the system moves, the tension in the string is (g = 10 m/s²):",
    place("15 N", ["10 N", "12 N", "30 N"], "C"),
    "Connected bodies with friction",
    "Write Newton's second law for each block. For the hanging block: 3g − T = 3a. For the block on the table: "
    "T − μₖ(2g) = 2a.",
    ["Adding: 30 − 5 = 5a → a = 5 m/s²", "Table block: T = 2a + 5 = 10 + 5 = 15 N",
     "Check with the hanging block: T = 30 − 3 × 5 = 15 N ✓"],
    why="10 N writes T = 2a for the table block and forgets the friction it must also overcome. 12 N ignores "
        "friction altogether (a = 6 m/s²). 30 N takes the tension equal to the hanging weight, which holds only "
        "when nothing accelerates.",
    ncert="Class 11 Physics, 'Laws of Motion', solving problems in mechanics", seconds=100, recomputed=True)

r_b, tb, mu_b = 20, 0.75, 0.5
v2 = r_b * 10 * (mu_b + tb) / (1 - mu_b * tb)
assert close(v2, 400) and close(math.sqrt(v2), 20)
assert close(math.sqrt(r_b * 10 * tb), 12.247) and close(math.sqrt(r_b * 10 * (mu_b + tb) / (1 + mu_b * tb)), 13.484)
assert close(math.sqrt(r_b * 10 * (mu_b + tb)), 15.811)
add(T, "Circular motion: level and banked roads", "Advanced", "numerical",
    "A circular track of radius 20 m is banked at an angle θ with tan θ = 0.75. The coefficient of static friction "
    "between the tyres and the track is 0.5. Taking g = 10 m/s², the maximum speed at which a car can go round the "
    "track without skidding is:",
    place("20 m/s", ["12.2 m/s", "13.5 m/s", "15.8 m/s"], "A"),
    "Banked road with friction",
    "At the maximum speed, friction acts down the slope. Resolving forces vertically and horizontally gives "
    "v²_max = rg(μₛ + tan θ)/(1 − μₛ tan θ).",
    ["μₛ + tan θ = 1.25; 1 − μₛ tan θ = 1 − 0.375 = 0.625",
     "v² = 20 × 10 × 1.25/0.625 = 400", "v_max = 20 m/s"],
    why="12.2 m/s is the optimum (friction-free) speed √(rg tan θ). 13.5 m/s puts + instead of − in the denominator. "
        "15.8 m/s leaves out the denominator.",
    ncert="Class 11 Physics, 'Laws of Motion', circular motion (motion of a car on a banked road)", seconds=100,
    recomputed=True)

a_max = 0.3 * 10
F_max = (2 + 4) * a_max
assert close(F_max, 18) and close(0.3 * 2 * 10, 6) and close(0.3 * 4 * 10, 12)
assert close(0.3 * 2 * 10 * (2 + 4) / 4, 9)
add(T, "Friction", "Advanced", "numerical",
    "A block A of mass 2 kg rests on top of a block B of mass 4 kg, which lies on a frictionless horizontal floor. "
    "The coefficient of static friction between A and B is 0.3. A horizontal force F is applied to the lower block B. "
    "Taking g = 10 m/s², the largest value of F for which the two blocks move together without slipping is:",
    place("18 N", ["6 N", "12 N", "9 N"], "B"),
    "Friction as the only force accelerating the upper block",
    "Only static friction from B accelerates A, so A's acceleration cannot exceed μₛg. The two blocks move together "
    "at that acceleration under the largest force.",
    ["a_max (for A) = μₛ g = 0.3 × 10 = 3 m/s²", "F_max = (m_A + m_B) a_max = 6 × 3 = 18 N"],
    why="6 N is the limiting friction μₛm_A g itself, not the applied force. 12 N uses the mass of B in the friction "
        "force. 9 N is the answer when F is applied to the upper block A instead of B.",
    ncert="Class 11 Physics, 'Laws of Motion', friction", seconds=100, recomputed=True)

add(T, "Newton's laws and impulse", "Advanced", "multi_statement",
    multi("Which of the following statements are correct?",
          ["If the net external force on a body is zero, the body must be at rest.",
           "Action and reaction act on different bodies, so they do not cancel each other.",
           "The impulse of a force equals the change in momentum it produces.",
           "A body moving in a circle with constant speed has a constant linear momentum.",
           "The mass of a body is a quantitative measure of its inertia."]),
    place("(b), (c) and (e) only",
          ["(a), (b) and (c) only", "(b), (c), (d) and (e) only", "(b) and (e) only"], "D"),
    "Newton's laws of motion",
    "Zero net force means zero acceleration, which allows uniform motion as well as rest. Momentum is a vector, so "
    "it changes when the direction of motion changes even at constant speed.",
    ["(a) False: the body may move with constant velocity", "(b) True: the pair acts on two different bodies",
     "(c) True: J = Δp", "(d) False: the direction of the velocity, and hence of the momentum, keeps changing",
     "(e) True: the greater the mass, the greater the inertia"],
    why="Options with (a) or (d) include a false statement; the option without (c) leaves out a true one.",
    ncert="Class 11 Physics, 'Laws of Motion', Newton's laws of motion", seconds=70)


# =====================================================================================================================
# Work, Energy and Power (B3 I4 A3)
# =====================================================================================================================
T = "Work, Energy and Power"

W1 = 10 * 5 * math.cos(math.radians(60))
assert close(W1, 25) and close(10 * 5 * math.sin(math.radians(60)), 25 * math.sqrt(3))
add(T, "Work by constant and variable force", "Basic", "numerical",
    "A constant force of 10 N acts on a body, making an angle of 60° with the direction of its displacement. The body "
    "is displaced through 5 m. The work done by the force is:",
    place("25 J", ["50 J", "25√3 J", "−25 J"], "A"),
    "Work done by a constant force: W = F d cos θ",
    "Only the component of the force along the displacement does work.",
    ["W = F d cos θ = 10 × 5 × cos 60°", "= 50 × 0.5 = 25 J"],
    why="50 J ignores the angle. 25√3 J uses sin 60° in place of cos 60°. −25 J has the wrong sign: for an angle "
        "below 90° the work is positive.",
    ncert="Class 11 Physics, 'Work, Energy and Power', work", seconds=30, recomputed=True)

add(T, "Power", "Basic", "match_list",
    match_stem("Match List-I (quantity) with List-II (expression).",
               ["Work done by a variable force F(x) as a body moves from x₁ to x₂",
                "Kinetic energy of a body of mass m and linear momentum p",
                "Instantaneous power delivered by a force F to a body moving with velocity v",
                "Potential energy of a spring of spring constant k stretched by x"],
               ["½kx²", "F · v", "p²/2m", "∫ F dx, taken from x₁ to x₂"]),
    match_options({"A": "IV", "B": "III", "C": "II", "D": "I"},
                  [{"A": "IV", "B": "I", "C": "II", "D": "III"}, {"A": "II", "B": "III", "C": "IV", "D": "I"},
                   {"A": "IV", "B": "II", "C": "III", "D": "I"}], "C"),
    "Work, kinetic energy, power and spring potential energy",
    "Work by a variable force is the area under the F–x curve. Writing K = ½mv² with v = p/m gives p²/2m. Power is "
    "the rate of doing work, dW/dt = F · v. A spring stretched by x stores ½kx².",
    ["A → ∫F dx (IV)", "B → p²/2m (III)", "C → F · v (II)", "D → ½kx² (I)"],
    why="The other codes swap power with work, or kinetic energy with the spring's potential energy.",
    ncert="Class 11 Physics, 'Work, Energy and Power', work by a variable force, power, potential energy of a spring",
    seconds=40)

add(T, "Work-energy theorem", "Basic", "direct",
    "The kinetic energy of a moving body remains constant over a certain time interval. Which of the following must "
    "be true over that interval?",
    place("The net work done on the body is zero",
          ["No force acts on the body", "The body moves in a straight line",
           "The linear momentum of the body remains constant"], "B"),
    "Work–energy theorem",
    "The work–energy theorem states that the work done by the net force equals the change in kinetic energy. If the "
    "kinetic energy does not change, the net work is zero. Forces may still act, and the direction of motion may "
    "change.",
    ["W_net = ΔK = 0", "Example: uniform circular motion has constant K but a net (centripetal) force",
     "In that example the path is curved and the momentum changes direction"],
    why="A body in uniform circular motion keeps a constant kinetic energy although a net force acts on it, its path "
        "is not straight and its momentum keeps changing direction.",
    ncert="Class 11 Physics, 'Work, Energy and Power', the work-energy theorem", seconds=40)

d_stop = 10 ** 2 / (2 * 0.25 * 10)
assert close(d_stop, 20) and close(10 ** 2 / (0.25 * 10), 40) and close(d_stop / 2, 10) and close(10 / 2.5, 4)
add(T, "Work-energy theorem", "Intermediate", "numerical",
    "A block of mass 2 kg slides on a rough horizontal floor with an initial speed of 10 m/s. The coefficient of "
    "kinetic friction is 0.25. Taking g = 10 m/s², the distance it slides before coming to rest is:",
    place("20 m", ["40 m", "10 m", "4 m"], "D"),
    "Work–energy theorem with friction",
    "Friction is the only force doing work. The work it does, −μₖmg d, equals the change in kinetic energy, −½mv². "
    "The mass cancels.",
    ["μₖ m g d = ½ m v²", "d = v²/(2μₖg) = 100/(2 × 0.25 × 10) = 20 m"],
    why="40 m drops the ½ in the kinetic energy. 10 m divides once more by the mass (2 kg), which actually cancels. "
        "4 m is the stopping time (v/μₖg = 4 s) taken as a distance.",
    ncert="Class 11 Physics, 'Work, Energy and Power', the work-energy theorem", seconds=50, recomputed=True)

x_c = 2 * math.sqrt(0.5 / 200)
assert close(x_c, 0.1) and close(math.sqrt(0.5 * 4 / 200), 0.1) and close(math.sqrt(0.5 * 0.5 * 4 / 200), 0.0707)
assert close(0.5 * 4 / 200, 0.01) and close(0.5 * 2 / 200, 0.005)
add(T, "Spring potential energy", "Intermediate", "numerical",
    "A block of mass 0.5 kg moving at 2 m/s on a smooth horizontal surface hits the free end of a light horizontal "
    "spring of spring constant 200 N/m, whose other end is fixed. The maximum compression of the spring is:",
    place("10 cm", ["7.1 cm", "1 cm", "0.5 cm"], "A"),
    "Conservation of mechanical energy with a spring",
    "At maximum compression the block is momentarily at rest, so all its kinetic energy has become elastic "
    "potential energy of the spring.",
    ["½mv² = ½kx²", "x = v√(m/k) = 2 × √(0.5/200) = 2 × 0.05 = 0.1 m = 10 cm"],
    why="7.1 cm writes the spring energy as kx² (drops the ½ on one side only). 1 cm forgets the square root "
        "(x² = 0.01 taken as x). 0.5 cm equates kx to the momentum mv.",
    ncert="Class 11 Physics, 'Work, Energy and Power', the potential energy of a spring", seconds=50,
    recomputed=True)

add(T, "Collisions", "Intermediate", "assertion_reason",
    AR_STEM.format(
        a="In a perfectly inelastic collision, the total kinetic energy of the colliding bodies always becomes zero.",
        r="In a perfectly inelastic collision, the colliding bodies stick together and move with a common velocity "
          "after the collision."),
    ar("D"),
    "Perfectly inelastic collisions",
    "The bodies stick together, so they share a common final velocity. Momentum is conserved, so if the total "
    "momentum before the collision is not zero, the combined body must keep moving and some kinetic energy remains. "
    "The kinetic energy becomes zero only in the special case of zero total momentum.",
    ["R: bodies move together after the collision → true",
     "A: e.g. a moving body sticking to an identical body at rest keeps half the kinetic energy → false",
     "A false, R true → option D"],
    why="A is false because 'always' ignores momentum conservation, which forces the combined body to move whenever "
        "the total momentum is non-zero.",
    ncert="Class 11 Physics, 'Work, Energy and Power', collisions", seconds=50)

add(T, "Motion in a vertical circle", "Intermediate", "statement_pair",
    SP_STEM.format(
        s1="A stone tied to a string and whirled in a vertical circle, moving under gravity and the tension of the "
           "string only, moves with constant speed.",
        s2="For a stone tied to a string and whirled in a vertical circle, the tension in the string is maximum at "
           "the lowest point."),
    sp("D"),
    "Motion in a vertical circle",
    "Gravity does work on the stone as it rises and falls, so its speed is greatest at the bottom and least at the "
    "top. At the bottom, T − mg = mv²/L, so T = mg + mv²/L, which is the largest tension anywhere on the circle.",
    ["Statement I: kinetic energy changes with height → speed is not constant → false",
     "Statement II: speed is maximum and the weight acts directly away from the centre at the bottom → T is "
     "maximum there → true"],
    why="Statement I would hold only for uniform motion in a horizontal circle. In a vertical circle the speed "
        "changes with height.",
    ncert="Class 11 Physics, 'Work, Energy and Power', motion in a vertical circle", seconds=45)

m_, v_ = 1.0, 1.0
p_final = math.hypot(m_ * v_, m_ * v_)
KE_i = 2 * 0.5 * m_ * v_ ** 2
KE_f = p_final ** 2 / (2 * 2 * m_)
assert close((KE_i - KE_f) / KE_i, 0.5)
assert close((KE_i - 0.5 * 2 * m_ * (v_ / 2) ** 2) / KE_i, 0.75)
add(T, "Collisions", "Advanced", "numerical",
    "Two bodies of equal mass, moving with equal speeds along perpendicular directions on a smooth horizontal "
    "surface, collide and stick together. The fraction of their total initial kinetic energy that is lost in the "
    "collision is:",
    place("1/2", ["3/4", "0", "1"], "B"),
    "Perfectly inelastic collision in two dimensions",
    "Momentum is a vector. The two equal perpendicular momenta add to a resultant √2 mv, carried by mass 2m.",
    ["Initial KE = 2 × ½mv² = mv²", "Final momentum = √2 mv → final speed = √2 mv/(2m) = v/√2",
     "Final KE = ½(2m)(v²/2) = mv²/2", "Fraction lost = (mv² − mv²/2)/mv² = 1/2"],
    why="3/4 takes the final speed as v/2 (one body's momentum shared by 2m). 0 adds the momenta as scalars, as if "
        "the bodies moved in the same direction. 1 assumes the bodies stop, which happens only for equal and "
        "opposite momenta.",
    ncert="Class 11 Physics, 'Work, Energy and Power', collisions in two dimensions", seconds=90, recomputed=True)

m_s, L_s = 0.5, 1.0
vb2 = 5 * 10 * L_s
T_bot = m_s * 10 + m_s * vb2 / L_s
assert close(T_bot, 30) and close(m_s * vb2 / L_s, 25) and close(m_s * 10, 5) and close(m_s * 10 + m_s * 2 * 10, 15)
add(T, "Motion in a vertical circle", "Advanced", "numerical",
    "A small stone of mass 0.5 kg is whirled in a vertical circle at the end of a light string 1 m long. Its speed "
    "is such that the tension in the string just becomes zero at the highest point. Taking g = 10 m/s², the tension "
    "in the string at the lowest point is:",
    place("30 N", ["25 N", "5 N", "15 N"], "C"),
    "Vertical circle: critical speed and tension",
    "Zero tension at the top means mg alone provides the centripetal force there: v_top² = gL. Energy conservation "
    "gives the speed at the bottom, and the radial equation there gives the tension.",
    ["v_top² = gL", "v_bottom² = v_top² + 2g(2L) = 5gL",
     "T_bottom = mg + m v_bottom²/L = mg + 5mg = 6mg = 6 × 5 = 30 N"],
    why="25 N (5mg) forgets that the tension must also balance the weight at the bottom. 5 N is just the weight. "
        "15 N (3mg) takes the speed at the top as zero, which is possible only for a rod, not a string.",
    ncert="Class 11 Physics, 'Work, Energy and Power', motion in a vertical circle", seconds=90, recomputed=True)

F_drive = 20000 / 10
a_car = (F_drive - 1000) / 1000
assert close(a_car, 1) and close(F_drive / 1000, 2) and close((F_drive + 1000) / 1000, 3) and 20000 / 1000 == 20
add(T, "Power", "Advanced", "numerical",
    "A car of mass 1000 kg moves on a level road with its engine delivering a constant power of 20 kW. The total "
    "resistance to its motion is a constant 1000 N. At the instant its speed is 10 m/s, its acceleration is:",
    place("1 m/s²", ["2 m/s²", "3 m/s²", "20 m/s²"], "D"),
    "Power and force: P = F v",
    "At constant power the engine's driving force depends on speed: F = P/v. The net force is this driving force "
    "minus the resistance.",
    ["Driving force = P/v = 20000/10 = 2000 N", "Net force = 2000 − 1000 = 1000 N",
     "a = 1000/1000 = 1 m/s²"],
    why="2 m/s² ignores the resistance. 3 m/s² adds the resistance to the driving force. 20 m/s² divides the power "
        "by the mass, which is not a force at all.",
    ncert="Class 11 Physics, 'Work, Energy and Power', power", seconds=60, recomputed=True)


# =====================================================================================================================
# Rotational Motion (B4 I5 A4)
# =====================================================================================================================
T = "Rotational Motion"


def cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


tau = cross((2, 3, 0), (4, 0, 0))
assert tau == (0, 0, -12) and cross((4, 0, 0), (2, 3, 0)) == (0, 0, 12)
add(T, "Torque and angular momentum", "Basic", "numerical",
    "A force F = 4î N acts at a point whose position vector relative to the origin is r = (2î + 3ĵ) m. The torque of "
    "the force about the origin is:",
    place("−12k̂ N m", ["12k̂ N m", "8k̂ N m", "−12î N m"], "A"),
    "Torque as a vector product: τ = r × F",
    "Use î × î = 0 and ĵ × î = −k̂, keeping the order r × F.",
    ["τ = (2î + 3ĵ) × 4î = 8(î × î) + 12(ĵ × î)", "= 0 + 12(−k̂) = −12k̂ N m"],
    why="12k̂ N m takes F × r, reversing the order. 8k̂ N m multiplies the x-components, which give zero in a cross "
        "product. −12î N m has the right magnitude but a direction that is not perpendicular to both r and F.",
    ncert="Class 11 Physics, 'System of Particles and Rotational Motion', moment of force (torque)", seconds=45,
    recomputed=True)

add(T, "Torque and angular momentum", "Basic", "match_list",
    match_stem("Match List-I (quantity) with List-II (its dimensional formula).",
               ["Torque", "Angular momentum", "Moment of inertia", "Angular acceleration"],
               ["[M L² T⁻¹]", "[T⁻²]", "[M L² T⁻²]", "[M L²]"]),
    match_options({"A": "III", "B": "I", "C": "IV", "D": "II"},
                  [{"A": "I", "B": "III", "C": "IV", "D": "II"}, {"A": "III", "B": "IV", "C": "I", "D": "II"},
                   {"A": "III", "B": "I", "C": "II", "D": "IV"}], "B"),
    "Dimensions of rotational quantities",
    "Torque = force × distance; angular momentum = moment of inertia × angular velocity; moment of inertia = mass × "
    "(distance)²; angular acceleration = angular velocity per unit time, and angle is dimensionless.",
    ["Torque: [M L T⁻²][L] = [M L² T⁻²] → III", "Angular momentum: [M L²][T⁻¹] = [M L² T⁻¹] → I",
     "Moment of inertia: [M][L²] → IV", "Angular acceleration: [T⁻²] → II"],
    why="The other codes swap torque with angular momentum (they differ by one power of T), or moment of inertia "
        "with angular acceleration.",
    ncert="Class 11 Physics, 'System of Particles and Rotational Motion', torque, angular momentum, moment of "
          "inertia", seconds=40)

R_d = 20.0
k_disc = R_d / math.sqrt(2)
assert close(k_disc, 10 * math.sqrt(2)) and close(math.sqrt(2 / 5) * R_d, 4 * math.sqrt(10))
add(T, "Moment of inertia and axis theorems", "Basic", "numerical",
    "The radius of gyration of a uniform circular disc of radius 20 cm, about the axis through its centre "
    "perpendicular to its plane, is:",
    place("10√2 cm", ["20 cm", "10 cm", "4√10 cm"], "D"),
    "Radius of gyration: I = Mk²",
    "For a uniform disc about its central perpendicular axis, I = MR²/2. Equating this to Mk² gives k = R/√2.",
    ["Mk² = MR²/2 → k = R/√2", "k = 20/√2 = 10√2 cm ≈ 14.1 cm"],
    why="20 cm is the result for a thin ring (I = MR²). 10 cm takes k = R/2. 4√10 cm uses the solid-sphere "
        "result I = 2MR²/5.",
    ncert="Class 11 Physics, 'System of Particles and Rotational Motion', moment of inertia", seconds=40,
    recomputed=True)

add(T, "Centre of mass", "Basic", "direct",
    "The centre of mass of a uniform triangular lamina lies at:",
    place("The centroid, the point where its three medians meet",
          ["The orthocentre, the point where its three altitudes meet",
           "The midpoint of its longest side", "The vertex opposite its longest side"], "C"),
    "Centre of mass of a uniform lamina from symmetry",
    "Divide the lamina into thin strips parallel to one side. The centre of mass of each strip is at its midpoint, "
    "and these midpoints lie on the median to that side. So the centre of mass lies on every median, i.e. at the "
    "centroid.",
    ["Strips parallel to BC have midpoints on the median from A", "The same holds for the other two medians",
     "Centre of mass = intersection of the medians (centroid)"],
    why="The orthocentre coincides with the centroid only for an equilateral triangle. A side's midpoint and a vertex "
        "lie on the boundary, not at the balance point.",
    ncert="Class 11 Physics, 'System of Particles and Rotational Motion', centre of mass", seconds=30)

w2 = F(6, 4) * 2
assert w2 == 3 and F(4, 6) * 2 == F(4, 3) and close(2 * math.sqrt(6 / 4), 2.449)
add(T, "Torque and angular momentum", "Intermediate", "numerical",
    "An ice skater spins about a vertical axis at 2 revolutions per second with her arms stretched out, when her "
    "moment of inertia is 6 kg m². She pulls her arms in, reducing her moment of inertia to 4 kg m². Neglecting "
    "friction, her new rate of spin is:",
    place("3 rev/s", ["1.33 rev/s", "2.45 rev/s", "2 rev/s"], "A"),
    "Conservation of angular momentum",
    "With no external torque about the vertical axis, angular momentum Iω is conserved. Kinetic energy is not "
    "conserved: she does work pulling her arms in.",
    ["I₁ω₁ = I₂ω₂", "ω₂ = 6 × 2/4 = 3 rev/s"],
    why="1.33 rev/s inverts the ratio of moments of inertia. 2.45 rev/s wrongly conserves rotational kinetic energy "
        "(I₁ω₁² = I₂ω₂²). 2 rev/s assumes the rate of spin does not change.",
    ncert="Class 11 Physics, 'System of Particles and Rotational Motion', conservation of angular momentum",
    seconds=45, recomputed=True)

ms_ = [(1, (0, 0)), (2, (3, 0)), (3, (0, 3))]
M_tot = sum(m for m, _ in ms_)
cm = (F(sum(m * p[0] for m, p in ms_), M_tot), F(sum(m * p[1] for m, p in ms_), M_tot))
assert cm == (1, F(3, 2)) and M_tot == 6
add(T, "Centre of mass", "Intermediate", "numerical",
    "Particles of masses 1 kg, 2 kg and 3 kg are placed at the points (0, 0), (3 m, 0) and (0, 3 m) of the x–y "
    "plane. The coordinates of their centre of mass are:",
    place("(1 m, 1.5 m)", ["(1.5 m, 1 m)", "(1 m, 1 m)", "(2 m, 3 m)"], "B"),
    "Centre of mass of a system of particles",
    "Each coordinate of the centre of mass is the mass-weighted average of that coordinate: X = Σmᵢxᵢ/M, "
    "Y = Σmᵢyᵢ/M.",
    ["M = 1 + 2 + 3 = 6 kg", "X = (1 × 0 + 2 × 3 + 3 × 0)/6 = 1 m", "Y = (1 × 0 + 2 × 0 + 3 × 3)/6 = 1.5 m"],
    why="(1.5 m, 1 m) swaps the coordinates. (1 m, 1 m) is the simple (unweighted) average of the positions. "
        "(2 m, 3 m) divides by the number of particles (3) instead of the total mass (6 kg).",
    ncert="Class 11 Physics, 'System of Particles and Rotational Motion', centre of mass", seconds=45,
    recomputed=True)

M_r, R_r = 2.0, 0.1
I_dia = M_r * R_r ** 2 / 2
I_tan_plane = I_dia + M_r * R_r ** 2
assert close(I_tan_plane, 0.03) and close(2 * M_r * R_r ** 2, 0.04) and close(I_dia, 0.01)
add(T, "Moment of inertia and axis theorems", "Intermediate", "numerical",
    "A thin circular ring has mass 2 kg and radius 10 cm. Its moment of inertia about a tangent to the ring lying in "
    "the plane of the ring is:",
    place("0.03 kg m²", ["0.04 kg m²", "0.01 kg m²", "0.02 kg m²"], "C"),
    "Perpendicular and parallel axis theorems",
    "First find the moment of inertia about a diameter with the perpendicular axis theorem (two equal diameters add "
    "up to the central perpendicular axis). Then shift to the parallel tangent in the plane with the parallel axis "
    "theorem.",
    ["I(central perpendicular axis) = MR² = 0.02 kg m²", "I(diameter) = MR²/2 = 0.01 kg m²",
     "I(tangent in plane) = MR²/2 + MR² = 3MR²/2 = 1.5 × 2 × 0.01 = 0.03 kg m²"],
    why="0.04 kg m² (2MR²) is for a tangent perpendicular to the plane. 0.01 kg m² is about a diameter. 0.02 kg m² "
        "is about the central axis perpendicular to the plane.",
    ncert="Class 11 Physics, 'System of Particles and Rotational Motion', moment of inertia", seconds=60,
    recomputed=True)

add(T, "Torque and angular momentum", "Intermediate", "assertion_reason",
    AR_STEM.format(
        a="The handle of a door is fixed near the edge farthest from the hinges.",
        r="For a force of given magnitude applied perpendicular to the door, the torque about the hinge line is "
          "proportional to the distance of the point of application from the hinge line."),
    ar("A"),
    "Torque = force × perpendicular distance",
    "To turn the door we need a certain torque about the hinges. Since τ = F r⊥, putting the handle as far as "
    "possible from the hinges lets the smallest force produce that torque.",
    ["τ = F r⊥", "Largest r⊥ → smallest force needed", "R explains A → option A"],
    why="Both statements are true and R is exactly why the handle is placed far from the hinges.",
    ncert="Class 11 Physics, 'System of Particles and Rotational Motion', moment of force (torque)", seconds=40)

add(T, "Moment of inertia and axis theorems", "Intermediate", "statement_pair",
    SP_STEM.format(
        s1="The moment of inertia of a rigid body about an axis does not depend on how its mass is distributed "
           "about that axis.",
        s2="The radius of gyration of a rigid body has the same value about every axis."),
    sp("B"),
    "Moment of inertia and radius of gyration",
    "I = Σmᵢrᵢ² depends on the mass and on how far each part is from the axis, i.e. on the distribution of mass "
    "about the axis. Since k = √(I/M), the radius of gyration changes whenever I changes from one axis to another.",
    ["Statement I: a ring and a disc of equal mass and radius have different I → false",
     "Statement II: e.g. a rod has k = L/√12 about its centre and L/√3 about one end → false"],
    why="Both statements contradict the definition I = Σmr², so 'both false' is the only consistent choice.",
    ncert="Class 11 Physics, 'System of Particles and Rotational Motion', moment of inertia", seconds=45)

m_hang, M_disc, R_disc = 1.0, 2.0, 0.1
a_pul = m_hang * 10 / (m_hang + M_disc / 2)
assert close(a_pul, 5)
assert close(m_hang * 10 / (m_hang + M_disc), 10 / 3) and close(m_hang * 10 / (m_hang + M_disc / 4), 20 / 3)
I_p = M_disc * R_disc ** 2 / 2
assert close(m_hang * 10 * R_disc / I_p * R_disc, 10)
add(T, "Rigid-body rotation", "Advanced", "numerical",
    "A light string is wound round a uniform disc of mass 2 kg and radius 10 cm that can rotate freely about a fixed "
    "horizontal axis through its centre. A block of mass 1 kg hangs from the free end of the string. Taking "
    "g = 10 m/s², the acceleration of the block when it is released is:",
    place("5 m/s²", ["10 m/s²", "3.3 m/s²", "6.7 m/s²"], "D"),
    "Coupled translation and rotation: τ = Iα with a = Rα",
    "For the block: mg − T = ma. For the disc: TR = Iα = (MR²/2)(a/R), so T = Ma/2. Adding eliminates T.",
    ["mg − T = ma and T = (M/2)a", "a = mg/(m + M/2) = 10/(1 + 1) = 5 m/s²", "Tension T = 1 × 5 = 5 N"],
    why="10 m/s² takes T = mg (the block's weight drives the disc as if the block were not accelerating). "
        "3.3 m/s² uses I = MR² (a ring). 6.7 m/s² uses I = MR²/4 (the disc about a diameter).",
    ncert="Class 11 Physics, 'System of Particles and Rotational Motion', dynamics of rotational motion about a "
          "fixed axis", seconds=100, recomputed=True)

# plank 6 m, 30 kg, supports at x = 1.5 and 4.5; man 60 kg
d_beyond = 30 * (4.5 - 3.0) / 60
x_from_centre = (4.5 - 3.0) + d_beyond
assert close(d_beyond, 0.75) and close(x_from_centre, 2.25) and x_from_centre < 3.0
add(T, "Equilibrium of rigid bodies", "Advanced", "numerical",
    "A uniform plank 6 m long and of mass 30 kg rests horizontally on two supports, each 1.5 m from an end. A man of "
    "mass 60 kg walks along the plank from its centre towards one end. The greatest distance from the centre he can "
    "walk before the plank starts to tip is:",
    place("2.25 m", ["0.75 m", "1.5 m", "3.0 m"], "A"),
    "Rotational equilibrium and tipping",
    "When the man passes a support, the plank is on the point of tipping about that support once the reaction at the "
    "other support becomes zero. Then the torques of the man's weight and the plank's weight about the near support "
    "balance.",
    ["The plank's centre of mass is 1.5 m from each support",
     "At tipping: 60g × d = 30g × 1.5 → d = 0.75 m beyond the support",
     "Distance from centre = 1.5 + 0.75 = 2.25 m (less than the 3 m to the end)"],
    why="0.75 m is the distance beyond the support, not from the centre. 1.5 m stops at the support, where nothing "
        "tips. 3.0 m is the end of the plank; it tips before he reaches it.",
    ncert="Class 11 Physics, 'System of Particles and Rotational Motion', equilibrium of a rigid body", seconds=100,
    recomputed=True)

I_plat, w0, I_man = 300.0, 2.0, 50 * 2 ** 2
w_f = I_plat * w0 / (I_plat + I_man)
assert close(w_f, 1.2) and close(w0 * I_man / (I_plat + I_man), 0.8) and close(w0 * (I_plat + I_man) / I_plat, 10 / 3)
add(T, "Torque and angular momentum", "Advanced", "numerical",
    "A horizontal platform with a moment of inertia of 300 kg m² about its vertical axis rotates freely at 2 rad/s. "
    "A man of mass 50 kg, standing at the axis, walks out radially to a point 2 m from the axis. Treating the man as "
    "a point mass and neglecting friction, the new angular speed of the platform is:",
    place("1.2 rad/s", ["2 rad/s", "0.8 rad/s", "3.3 rad/s"], "B"),
    "Conservation of angular momentum with a changing moment of inertia",
    "No external torque acts about the vertical axis. At the axis the man adds nothing to the moment of inertia; at "
    "2 m he adds mr².",
    ["I₁ = 300 kg m² (man at the axis)", "I₂ = 300 + 50 × 2² = 500 kg m²",
     "ω₂ = I₁ω₁/I₂ = 300 × 2/500 = 1.2 rad/s"],
    why="2 rad/s ignores the change in moment of inertia. 0.8 rad/s uses the man's share (200/500) instead of the "
        "platform's. 3.3 rad/s inverts the ratio of moments of inertia.",
    ncert="Class 11 Physics, 'System of Particles and Rotational Motion', conservation of angular momentum",
    seconds=75, recomputed=True)

add(T, "Rigid-body rotation", "Advanced", "multi_statement",
    multi("Which of the following statements are correct?",
          ["If the net external torque on a system is zero, its total angular momentum is conserved.",
           "A rigid body on which the net external force is zero must also be in rotational equilibrium.",
           "Of all axes parallel to a given direction, the moment of inertia of a body is least about the axis "
           "through its centre of mass.",
           "For a rigid body rotating about a fixed axis, the torque about that axis equals the moment of inertia "
           "about the axis times the angular acceleration.",
           "The rotational kinetic energy of a body spinning with a given angular speed is the same about every "
           "axis."]),
    place("(a), (c) and (d) only",
          ["(a), (b) and (d) only", "(a), (c), (d) and (e) only", "(b), (c) and (d) only"], "C"),
    "Torque, angular momentum and moment of inertia",
    "dL/dt = τ_ext, so zero external torque keeps L constant. A couple gives zero net force but a non-zero torque. "
    "By the parallel axis theorem I = I_cm + Md², which is least when d = 0. Rotational kinetic energy ½Iω² depends "
    "on I, which depends on the axis.",
    ["(a) True: dL/dt = τ_ext = 0", "(b) False: a couple gives F_net = 0 but τ ≠ 0",
     "(c) True: I = I_cm + Md² ≥ I_cm", "(d) True: τ = Iα about a fixed axis",
     "(e) False: I, and so ½Iω², changes with the axis"],
    why="Options with (b) or (e) include a false statement; (a), (c) and (d) are all true.",
    ncert="Class 11 Physics, 'System of Particles and Rotational Motion', equilibrium of a rigid body, moment of "
          "inertia, angular momentum", seconds=80)


# =====================================================================================================================
# Gravitation (B3 I4 A3)
# =====================================================================================================================
T = "Gravitation"

G = 6.67e-11
Fg = G * 100 * 100 / 0.5 ** 2
assert close(Fg, 2.668e-6) and close(G * 1e4 / 0.3 ** 2, 7.41e-6) and close(G * 1e4 / 0.5, 1.334e-6)
assert close(G * 100 / 0.25, 2.668e-8)
add(T, "Law of gravitation", "Basic", "numerical",
    "Two uniform solid spheres, each of mass 100 kg and radius 0.1 m, are placed so that the gap between their "
    "surfaces is 0.3 m. Taking G = 6.67 × 10⁻¹¹ N m² kg⁻², the gravitational force between them is about:",
    place("2.67 × 10⁻⁶ N", ["7.41 × 10⁻⁶ N", "1.33 × 10⁻⁶ N", "2.67 × 10⁻⁸ N"], "C"),
    "Newton's law of gravitation for uniform spheres",
    "A uniform sphere attracts an outside mass as if all its mass were at its centre, so r is the distance between "
    "the centres.",
    ["r = 0.1 + 0.3 + 0.1 = 0.5 m", "F = G m₁m₂/r² = 6.67 × 10⁻¹¹ × 10⁴/0.25 ≈ 2.67 × 10⁻⁶ N"],
    why="7.41 × 10⁻⁶ N uses the 0.3 m gap between the surfaces instead of the distance between centres. "
        "1.33 × 10⁻⁶ N divides by r instead of r². 2.67 × 10⁻⁸ N uses only one of the masses.",
    ncert="Class 11 Physics, 'Gravitation', universal law of gravitation", seconds=45, recomputed=True)

add(T, "Kepler's laws", "Basic", "direct",
    "Kepler's second law (the line joining a planet to the Sun sweeps out equal areas in equal intervals of time) "
    "follows from the conservation of the planet's:",
    place("Angular momentum about the Sun",
          ["Linear momentum", "Kinetic energy", "Speed along its orbit"], "D"),
    "Kepler's law of areas and central forces",
    "The gravitational force on the planet is directed towards the Sun (a central force), so it exerts no torque "
    "about the Sun. The planet's angular momentum L about the Sun is therefore constant, and the areal velocity "
    "dA/dt = L/2m is constant.",
    ["Central force → τ about the Sun = 0 → L constant", "dA/dt = L/(2m) = constant → equal areas in equal times"],
    why="The planet's linear momentum, kinetic energy and speed all change along an elliptical orbit: it moves "
        "fastest near the Sun.",
    ncert="Class 11 Physics, 'Gravitation', Kepler's laws", seconds=30)

h_1pc = 0.01 * 6400 / 2
assert close(h_1pc, 32) and close(0.01 * 6400, 64) and close(0.01 * 6400 / 4, 16) and close(0.1 * 6400 / 2, 320)
add(T, "Variation of g", "Basic", "numerical",
    "The acceleration due to gravity at a small height h above the Earth's surface is 1% less than its value at the "
    "surface. Taking the Earth's radius as 6400 km, h is about:",
    place("32 km", ["64 km", "16 km", "320 km"], "B"),
    "Variation of g with height (h ≪ R)",
    "For h much smaller than R, g(h) ≈ g(1 − 2h/R), so the fractional decrease in g is 2h/R.",
    ["2h/R = 0.01", "h = 0.005 × 6400 km = 32 km"],
    why="64 km uses the depth formula g(1 − d/R), which has no factor 2. 16 km uses a factor 4 instead of 2. 320 km "
        "takes 1% as 0.1.",
    ncert="Class 11 Physics, 'Gravitation', acceleration due to gravity below and above the surface of the Earth",
    seconds=40, recomputed=True)

add(T, "Variation of g", "Intermediate", "match_list",
    match_stem("Match List-I (location) with List-II (acceleration due to gravity there). The Earth is a uniform "
               "sphere of radius R, g is the value at its surface and its rotation is ignored.",
               ["At a small height h above the surface (h ≪ R)", "At a depth d below the surface",
                "At the centre of the Earth", "At a height equal to R above the surface"],
               ["Zero", "g/4", "g(1 − d/R)", "g(1 − 2h/R)"]),
    match_options({"A": "IV", "B": "III", "C": "I", "D": "II"},
                  [{"A": "III", "B": "IV", "C": "I", "D": "II"}, {"A": "IV", "B": "III", "C": "II", "D": "I"},
                   {"A": "II", "B": "III", "C": "I", "D": "IV"}], "A"),
    "Variation of g with height and depth",
    "Above the surface g = gR²/(R + h)², which is g(1 − 2h/R) for small h and g/4 at h = R. Inside a uniform Earth, "
    "only the mass within radius (R − d) attracts, giving g(1 − d/R), which is zero at the centre.",
    ["A: g(1 − 2h/R) → IV", "B: g(1 − d/R) → III", "C: d = R → g = 0 → I", "D: g R²/(2R)² = g/4 → II"],
    why="The commonest swap is between the height and depth formulas (factor 2h/R versus d/R). At h = R the small-"
        "height formula does not apply; the exact result is g/4.",
    ncert="Class 11 Physics, 'Gravitation', acceleration due to gravity below and above the surface of the Earth",
    seconds=50)

v0 = 1.0
ve = math.sqrt(2) * v0
assert close(ve - v0, math.sqrt(2) - 1)
add(T, "Escape and orbital velocity", "Intermediate", "numerical",
    "A satellite revolves in a circular orbit just above the Earth's surface with orbital speed v₀. Neglecting air "
    "resistance and the Earth's rotation, the minimum additional speed it must be given along its direction of "
    "motion so that it escapes the Earth's gravity is:",
    place("(√2 − 1)v₀", ["√2 v₀", "v₀", "(√2 + 1)v₀"], "B"),
    "Orbital speed and escape speed near the surface",
    "Near the surface, the orbital speed is v₀ = √(gR) and the escape speed is vₑ = √(2gR) = √2 v₀. The satellite "
    "already moves at v₀, so it needs only the difference.",
    ["v₀ = √(GM/R) = √(gR)", "vₑ = √(2GM/R) = √2 v₀", "Extra speed = vₑ − v₀ = (√2 − 1)v₀ ≈ 0.41 v₀"],
    why="√2 v₀ is the full escape speed, not the extra speed. v₀ assumes the escape speed is twice the orbital speed. "
        "(√2 + 1)v₀ adds the two speeds instead of subtracting.",
    ncert="Class 11 Physics, 'Gravitation', escape speed and earth satellites", seconds=50, recomputed=True)

add(T, "Gravitational potential and energy", "Intermediate", "assertion_reason",
    AR_STEM.format(
        a="When the zero of gravitational potential energy is taken at infinite separation, the gravitational "
          "potential energy of a system of two particles is negative.",
        r="The universal gravitational constant G has the same value for all pairs of bodies everywhere in the "
          "universe."),
    ar("B"),
    "Gravitational potential energy and the universality of G",
    "U = −Gm₁m₂/r. The negative sign arises because gravity is attractive: the energy rises to zero as the "
    "particles are pulled apart to infinity, so at any finite separation it is below zero. R is a true statement "
    "about G being a universal constant, but it says nothing about why U is negative.",
    ["A: U = −Gm₁m₂/r < 0 for finite r → true", "R: G is a universal constant → true",
     "The sign of U comes from the attractive nature of gravity, not from the universality of G → option B"],
    why="R does not explain A: U would be negative even if G varied from place to place, because the sign comes "
        "from gravity being attractive.",
    ncert="Class 11 Physics, 'Gravitation', gravitational potential energy", seconds=45)

add(T, "Escape and orbital velocity", "Intermediate", "statement_pair",
    SP_STEM.format(
        s1="The escape speed of a body from the Earth's surface depends on the mass of the body.",
        s2="Neglecting air resistance and the Earth's rotation, the escape speed from the Earth's surface does not "
           "depend on the direction in which the body is projected."),
    sp("D"),
    "Escape speed",
    "Escape requires ½mvₑ² − GMm/R ≥ 0, so vₑ = √(2GM/R). The mass m of the body cancels, and the energy "
    "condition involves only the speed, not the direction.",
    ["Statement I: m cancels in the energy condition → false", "Statement II: kinetic energy is a scalar → true"],
    why="Statement I is false because both the kinetic energy needed and the potential energy to overcome are "
        "proportional to m.",
    ncert="Class 11 Physics, 'Gravitation', escape speed", seconds=40)

m_sat, R_e, g0 = 200, 6.4e6, 10
E_sat = -m_sat * g0 * R_e ** 2 / (2 * (2 * R_e))
assert close(E_sat, -3.2e9) and close(-m_sat * g0 * R_e ** 2 / (2 * R_e), -6.4e9) and close(-m_sat * g0 * R_e, -1.28e10)
add(T, "Satellite energy and period", "Advanced", "numerical",
    "A satellite of mass 200 kg revolves in a circular orbit at a height above the Earth's surface equal to the "
    "Earth's radius. Taking the Earth's radius as 6400 km and g at the surface as 10 m/s², the total mechanical "
    "energy of the satellite is:",
    place("−3.2 × 10⁹ J", ["−6.4 × 10⁹ J", "+3.2 × 10⁹ J", "−1.28 × 10¹⁰ J"], "C"),
    "Energy of a satellite in a circular orbit",
    "For a circular orbit of radius r, the kinetic energy is GMm/2r, the potential energy is −GMm/r, and the total "
    "energy is −GMm/2r. Use GM = gR².",
    ["r = R + R = 2R", "E = −GMm/(2r) = −gR²m/(4R) = −mgR/4",
     "E = −200 × 10 × 6.4 × 10⁶/4 = −3.2 × 10⁹ J"],
    why="−6.4 × 10⁹ J is the potential energy in this orbit (or the total energy with r taken as R). +3.2 × 10⁹ J "
        "is the kinetic energy. −1.28 × 10¹⁰ J is −mgR, the potential energy at the Earth's surface.",
    ncert="Class 11 Physics, 'Gravitation', energy of an orbiting satellite", seconds=80, recomputed=True)

x_n = 1 / (1 + 1 / 9)
assert close(x_n, 0.9) and close(81 / 82, 0.98780) and math.isclose(math.sqrt(81), 9)
add(T, "Law of gravitation", "Advanced", "numerical",
    "The mass of the Earth is 81 times that of the Moon, and the distance between their centres is d. The point on "
    "the line joining their centres where the net gravitational field due to the two bodies is zero is at a distance "
    "from the Earth's centre of:",
    place("0.9d", ["0.1d", "81d/82", "d/82"], "D"),
    "Neutral point between two masses",
    "At the neutral point the fields of the Earth and the Moon are equal and opposite: GM_E/x² = GM_M/(d − x)².",
    ["x²/(d − x)² = M_E/M_M = 81", "x/(d − x) = 9 → x = 9d/10 = 0.9d"],
    why="0.1d is the distance from the Moon, not the Earth. 81d/82 and d/82 use the mass ratio 81 directly, "
        "forgetting to take the square root.",
    ncert="Class 11 Physics, 'Gravitation', universal law of gravitation", seconds=60, recomputed=True)

add(T, "Satellite energy and period", "Advanced", "multi_statement",
    multi("For a satellite revolving round the Earth in a circular orbit, which of the following statements are "
          "correct?",
          ["Its orbital speed does not depend on its own mass.",
           "Its kinetic energy is equal to the magnitude of its total mechanical energy.",
           "Its total mechanical energy is positive.",
           "Its orbital speed increases as the radius of the orbit increases.",
           "Its gravitational potential energy is twice its total mechanical energy."]),
    place("(a), (b) and (e) only",
          ["(a), (b) and (c) only", "(b), (d) and (e) only", "(a), (b), (d) and (e) only"], "A"),
    "Speed and energy of an orbiting satellite",
    "From GMm/r² = mv²/r, v = √(GM/r), which does not involve m and falls as r grows. K = GMm/2r, U = −GMm/r and "
    "E = K + U = −GMm/2r. So K = |E| and U = 2E, and E is negative for a bound orbit.",
    ["(a) True: v = √(GM/r)", "(b) True: K = GMm/2r = −E", "(c) False: E = −GMm/2r < 0",
     "(d) False: v ∝ 1/√r decreases with r", "(e) True: U = −GMm/r = 2E"],
    why="Options with (c) or (d) include a false statement; (a), (b) and (e) are all true.",
    ncert="Class 11 Physics, 'Gravitation', earth satellites and energy of an orbiting satellite", seconds=80)


# =====================================================================================================================
# Properties of Solids and Liquids (B5 I6 A5)
# =====================================================================================================================
T = "Properties of Solids and Liquids"

stress = 100 / 2e-6
assert close(stress, 5e7) and close(100 / 2e-4, 5e5) and close(2e-6 / 100, 2e-8) and 100 / 2 == 50
add(T, "Elasticity and moduli", "Basic", "numerical",
    "A wire of cross-sectional area 2 mm² is stretched by a force of 100 N applied along its length. The tensile "
    "stress in the wire is:",
    place("5 × 10⁷ N m⁻²", ["50 N m⁻²", "5 × 10⁵ N m⁻²", "2 × 10⁻⁸ N m⁻²"], "B"),
    "Stress = force / area",
    "Convert the area to m² (1 mm² = 10⁻⁶ m²) before dividing.",
    ["A = 2 mm² = 2 × 10⁻⁶ m²", "Stress = 100/(2 × 10⁻⁶) = 5 × 10⁷ N m⁻²"],
    why="50 N m⁻² leaves the area in mm². 5 × 10⁵ N m⁻² takes 1 mm² as 10⁻⁴ m² (that is 1 cm²). 2 × 10⁻⁸ N m⁻² "
        "divides the area by the force.",
    ncert="Class 11 Physics, 'Mechanical Properties of Solids', stress and strain", seconds=30, recomputed=True)

P_abs = 1.0e5 + 1000 * 10 * 20
assert close(P_abs, 3.0e5) and close(1000 * 10 * 20, 2.0e5) and close(1.0e5 + 1000 * 20, 1.2e5)
add(T, "Fluid pressure and Pascal's law", "Basic", "numerical",
    "Taking the atmospheric pressure as 1.0 × 10⁵ Pa, the density of water as 1000 kg/m³ and g = 10 m/s², the "
    "absolute pressure at a depth of 20 m below the surface of a lake is:",
    place("3.0 × 10⁵ Pa", ["2.0 × 10⁵ Pa", "1.2 × 10⁵ Pa", "2.0 × 10⁴ Pa"], "B"),
    "Pressure at a depth in a liquid",
    "The absolute pressure at depth h is the atmospheric pressure on the surface plus the pressure of the liquid "
    "column: P = Pₐ + ρgh.",
    ["ρgh = 1000 × 10 × 20 = 2.0 × 10⁵ Pa", "P = 1.0 × 10⁵ + 2.0 × 10⁵ = 3.0 × 10⁵ Pa"],
    why="2.0 × 10⁵ Pa is the gauge pressure, leaving out the atmosphere. 1.2 × 10⁵ Pa uses ρh without g. "
        "2.0 × 10⁴ Pa is ρh alone, with neither g nor the atmospheric pressure.",
    ncert="Class 11 Physics, 'Mechanical Properties of Fluids', variation of pressure with depth", seconds=35,
    recomputed=True)

add(T, "Thermal expansion and calorimetry", "Basic", "direct",
    "Water has its maximum density at:",
    place("4 °C", ["0 °C", "100 °C", "−4 °C"], "B"),
    "Anomalous expansion of water",
    "Water contracts on heating from 0 °C to 4 °C and expands above 4 °C, so its volume is least and its density "
    "greatest at 4 °C.",
    ["0 °C → 4 °C: water contracts (anomalous behaviour)", "Above 4 °C: water expands normally",
     "Minimum volume, hence maximum density, at 4 °C"],
    why="At 0 °C water is less dense than at 4 °C (which is why lakes freeze from the top). 100 °C is the boiling "
        "point at 1 atm, and −4 °C is below the normal freezing point.",
    ncert="Class 11 Physics, 'Thermal Properties of Matter', thermal expansion", seconds=20)

add(T, "Heat transfer", "Basic", "direct",
    "As the temperature of a black body is raised, the wavelength at which it emits the maximum energy:",
    place("Decreases", ["Increases", "Remains unchanged", "First increases and then decreases"], "D"),
    "Wien's displacement law",
    "Wien's displacement law states λ_m T = constant, so λ_m is inversely proportional to the absolute temperature.",
    ["λ_m T = b (constant)", "T increases → λ_m decreases (e.g. a heated iron piece glows dull red, then orange, "
     "then yellowish white)"],
    why="λ_m T is constant, so λ_m cannot increase or stay the same when T rises, and the change is monotonic.",
    ncert="Class 11 Physics, 'Thermal Properties of Matter', radiation (Wien's displacement law)", seconds=25)

add(T, "Thermal expansion and calorimetry", "Basic", "assertion_reason",
    AR_STEM.format(
        a="Water is used as the coolant in the radiators of automobiles.",
        r="Water has a high specific heat capacity, so it absorbs a large amount of heat for a small rise in its "
          "temperature."),
    ar("A"),
    "Specific heat capacity of water",
    "A coolant must carry away a lot of heat from the engine without itself getting too hot. Because water's specific "
    "heat capacity is high, Q = mcΔT is large for a small ΔT, which is exactly why it is used.",
    ["Q = mcΔT; large c → large Q for small ΔT", "R explains A → option A"],
    why="Both statements are true and R gives the property that makes water a good coolant.",
    ncert="Class 11 Physics, 'Thermal Properties of Matter', specific heat capacity", seconds=30)

r_cap = 0.2e-3 / 2
h_cap = 2 * 0.07 / (1000 * 10 * r_cap)
assert close(h_cap, 0.14) and close(2 * 0.07 / (1000 * 10 * 0.2e-3), 0.07) and close(4 * 0.07 / (1000 * 10 * r_cap), 0.28)
add(T, "Surface tension and capillarity", "Intermediate", "numerical",
    "A clean glass capillary tube of internal diameter 0.2 mm is dipped vertically in water. The surface tension of "
    "water is 0.07 N/m, the angle of contact is 0°, the density of water is 1000 kg/m³ and g = 10 m/s². The height to "
    "which water rises in the tube is:",
    place("14 cm", ["7 cm", "28 cm", "1.4 cm"], "C"),
    "Capillary rise: h = 2S cos θ/(ρgr)",
    "The upward pull of surface tension round the circumference balances the weight of the raised column. Use the "
    "radius, which is half the given diameter.",
    ["r = 0.1 mm = 1 × 10⁻⁴ m", "h = 2 × 0.07 × 1/(1000 × 10 × 10⁻⁴) = 0.14 m = 14 cm"],
    why="7 cm puts the diameter in place of the radius. 28 cm uses 4S, the factor for a soap bubble with two "
        "surfaces. 1.4 cm is a power-of-ten slip in converting metres to centimetres.",
    ncert="Class 11 Physics, 'Mechanical Properties of Fluids', capillary rise", seconds=50, recomputed=True)

vt = 2 * (1e-3) ** 2 * (8000 - 800) * 10 / (9 * 0.8)
assert close(vt, 0.02)
assert close(2 * (1e-3) ** 2 * 8000 * 10 / (9 * 0.8), 0.02222) and close(vt / 2, 0.01) and close(4 * vt, 0.08)
add(T, "Viscosity and Stokes' law", "Intermediate", "numerical",
    "A small steel ball of radius 1 mm and density 8000 kg/m³ falls through a liquid of density 800 kg/m³ and "
    "coefficient of viscosity 0.8 Pa s. Taking g = 10 m/s² and assuming Stokes' law holds, its terminal velocity is:",
    place("2 cm/s", ["2.2 cm/s", "1 cm/s", "8 cm/s"], "D"),
    "Terminal velocity from Stokes' law",
    "At terminal velocity, weight = buoyant force + viscous drag, which gives v_t = 2r²(ρ − σ)g/(9η).",
    ["ρ − σ = 8000 − 800 = 7200 kg/m³", "v_t = 2 × (10⁻³)² × 7200 × 10/(9 × 0.8)",
     "= 0.144/7.2 = 0.02 m/s = 2 cm/s"],
    why="2.2 cm/s ignores the buoyant force (uses ρ instead of ρ − σ). 1 cm/s drops the factor 2. 8 cm/s uses the "
        "diameter (2 mm) as the radius.",
    ncert="Class 11 Physics, 'Mechanical Properties of Fluids', viscosity and Stokes' law", seconds=60,
    recomputed=True)

v_noz = 2 * (1.0 / 0.5) ** 2
h_jet = v_noz ** 2 / (2 * 10)
assert close(v_noz, 8) and close(h_jet, 3.2) and close((2 * 2) ** 2 / 20, 0.8) and close(v_noz ** 2 / 10, 6.4)
assert close(2 ** 2 / 20, 0.2)
add(T, "Bernoulli's principle", "Intermediate", "numerical",
    "Water flows steadily at 2 m/s through a horizontal hose pipe of internal radius 1 cm. At its end is a nozzle of "
    "internal radius 0.5 cm, pointed vertically upward. Neglecting viscosity and air resistance, and taking "
    "g = 10 m/s², the height above the nozzle to which the jet rises is:",
    place("3.2 m", ["0.8 m", "6.4 m", "0.2 m"], "A"),
    "Equation of continuity and conservation of energy",
    "The volume flow rate Av is the same in the pipe and the nozzle, so the speed rises as the area falls. The jet "
    "then rises until its kinetic energy is used up: h = v²/2g.",
    ["A₁v₁ = A₂v₂ → v₂ = v₁(r₁/r₂)² = 2 × 4 = 8 m/s", "h = v₂²/(2g) = 64/20 = 3.2 m"],
    why="0.8 m uses the ratio of radii instead of areas (v₂ = 4 m/s). 6.4 m drops the 2 in v²/2g. 0.2 m uses the "
        "speed in the pipe, not in the nozzle.",
    ncert="Class 11 Physics, 'Mechanical Properties of Fluids', streamline flow and Bernoulli's principle",
    seconds=60, recomputed=True)

add(T, "Elasticity and moduli", "Intermediate", "statement_pair",
    SP_STEM.format(
        s1="Gases have much smaller bulk moduli than solids.",
        s2="For most materials, the shear modulus is greater than Young's modulus."),
    sp("C"),
    "Bulk modulus and shear modulus",
    "Gases are far more compressible than solids, so their bulk moduli (B = −p/(ΔV/V)) are much smaller. NCERT notes "
    "that the shear modulus is generally less than Young's modulus; for most materials G ≈ Y/3.",
    ["Statement I: gases are highly compressible → small B → true",
     "Statement II: G is generally less than Y (about Y/3) → false"],
    why="Statement II reverses the usual order: the shear modulus is generally smaller than Young's modulus.",
    ncert="Class 11 Physics, 'Mechanical Properties of Solids', shear modulus and bulk modulus", seconds=40)

add(T, "Surface tension and capillarity", "Intermediate", "assertion_reason",
    AR_STEM.format(
        a="Small drops of a liquid take a nearly spherical shape.",
        r="Surface tension makes a liquid surface tend to have the least possible area, and for a given volume a "
          "sphere has the least surface area."),
    ar("A"),
    "Surface tension and minimum surface area",
    "Surface energy is proportional to surface area, so a free liquid surface tends to contract to the least area. "
    "For small drops, surface effects dominate over gravity, and the shape with least area for a given volume is a "
    "sphere.",
    ["Surface energy = S × area → minimised", "Least area for a given volume → sphere", "R explains A → option A"],
    why="Both statements are true and R is the reason small drops are spherical.",
    ncert="Class 11 Physics, 'Mechanical Properties of Fluids', surface tension", seconds=35)

add(T, "Elasticity and moduli", "Intermediate", "match_list",
    match_stem("Match List-I (elastic constant) with List-II (its definition).",
               ["Young's modulus", "Bulk modulus", "Shear modulus (modulus of rigidity)", "Compressibility"],
               ["Shearing (tangential) stress divided by shearing strain", "Reciprocal of the bulk modulus",
                "Tensile (or compressive) stress divided by longitudinal strain",
                "Hydraulic pressure divided by the magnitude of the volume strain"]),
    match_options({"A": "III", "B": "IV", "C": "I", "D": "II"},
                  [{"A": "I", "B": "IV", "C": "III", "D": "II"}, {"A": "III", "B": "II", "C": "I", "D": "IV"},
                   {"A": "IV", "B": "III", "C": "I", "D": "II"}], "B"),
    "Elastic moduli",
    "Each modulus is a stress divided by the matching strain: longitudinal for Young's modulus, volume for the bulk "
    "modulus and shearing for the shear modulus. Compressibility k is defined as 1/B.",
    ["A: Y = (F/A)/(ΔL/L) → III", "B: B = −p/(ΔV/V) → IV", "C: G = (F/A)/(Δx/L) → I", "D: k = 1/B → II"],
    why="The other codes swap Young's modulus with the shear modulus, or the bulk modulus with its reciprocal "
        "(compressibility).",
    ncert="Class 11 Physics, 'Mechanical Properties of Solids', elastic moduli", seconds=45)

ratio_ext = F(2, 1) / F(1, 2) ** 2
assert ratio_ext == 8 and F(2, 1) / F(1, 2) == 4 and F(2, 1) * F(1, 2) ** 2 == F(1, 2)
add(T, "Elasticity and moduli", "Advanced", "numerical",
    "Two wires P and Q are made of the same material. The length of P is twice that of Q, and the diameter of P is "
    "half that of Q. When the same load is hung from each, the ratio of the extension of P to that of Q is:",
    place("8 : 1", ["1 : 8", "4 : 1", "1 : 2"], "C"),
    "Extension from Young's modulus: ΔL = FL/(AY)",
    "With the same load and material, ΔL ∝ L/A and A ∝ d².",
    ["ΔL ∝ L/d²", "ΔL_P/ΔL_Q = (L_P/L_Q)(d_Q/d_P)² = 2 × 2² = 8", "Ratio = 8 : 1"],
    why="1 : 8 inverts the ratio. 4 : 1 uses the diameter instead of its square. 1 : 2 multiplies by the area "
        "ratio instead of dividing.",
    ncert="Class 11 Physics, 'Mechanical Properties of Solids', Young's modulus", seconds=60, recomputed=True)

Y_s, alpha_s, dT_s, A_s = 2e11, 1.2e-5, 50, 1e-4
F_th = Y_s * alpha_s * dT_s * A_s
assert close(F_th, 1.2e4) and close(Y_s * alpha_s * dT_s, 1.2e8) and close(Y_s * alpha_s * dT_s * 1e-2, 1.2e6)
assert close(Y_s * alpha_s * dT_s * 1e-6, 1.2e2)
add(T, "Thermal expansion and calorimetry", "Advanced", "numerical",
    "A steel rod of cross-sectional area 1 cm² is held between two rigid walls so that it cannot expand. Its "
    "temperature is raised by 50 °C. For steel, the coefficient of linear expansion is 1.2 × 10⁻⁵ °C⁻¹ and Young's "
    "modulus is 2 × 10¹¹ N/m². The force the rod exerts on each wall is:",
    place("1.2 × 10⁴ N", ["1.2 × 10⁸ N", "1.2 × 10⁶ N", "1.2 × 10² N"], "D"),
    "Thermal stress",
    "If free, the rod would expand by a strain αΔT. The walls prevent this, so they compress it by the same strain, "
    "which needs a stress YαΔT. The force is this stress times the area.",
    ["Strain prevented = αΔT = 1.2 × 10⁻⁵ × 50 = 6 × 10⁻⁴", "Stress = Y × strain = 2 × 10¹¹ × 6 × 10⁻⁴ = 1.2 × 10⁸ N/m²",
     "F = stress × A = 1.2 × 10⁸ × 10⁻⁴ = 1.2 × 10⁴ N"],
    why="1.2 × 10⁸ N is the stress (in N/m²) quoted as a force. 1.2 × 10⁶ N takes 1 cm² as 10⁻² m². 1.2 × 10² N "
        "takes 1 cm² as 10⁻⁶ m².",
    ncert=None, seconds=80, recomputed=True)

K_cool = F(20, 5) / (70 - 20)
t_cool = F(20) / (K_cool * (50 - 20))
assert t_cool == F(25, 3)
K_bad = F(20, 5) / (80 - 20)
assert F(20) / (K_bad * (60 - 20)) == F(15, 2)
K_bad2 = F(20, 5) / 70
assert F(20) / (K_bad2 * 50) == 7
add(T, "Heat transfer", "Advanced", "numerical",
    "A body cools from 80 °C to 60 °C in 5 minutes in a room at 20 °C. Using Newton's law of cooling in its "
    "approximate form (rate of fall of temperature = K × (average temperature of the body during the interval − room "
    "temperature)), the time it takes to cool further from 60 °C to 40 °C is:",
    place("8.3 min", ["5 min", "7.5 min", "7 min"], "B"),
    "Newton's law of cooling (average-temperature form)",
    "Apply the law to each interval with the average temperature of the body. The first interval gives K; the second "
    "then gives the time.",
    ["First interval: 20/5 = K(70 − 20) → K = 0.08 min⁻¹",
     "Second interval: 20/t = 0.08 × (50 − 20) = 2.4 °C/min", "t = 20/2.4 = 25/3 ≈ 8.3 min"],
    why="5 min assumes equal drops take equal times, but the body cools more slowly as it nears room temperature. "
        "7.5 min uses the starting temperatures (80 °C and 60 °C) instead of the averages. 7 min uses the averages "
        "but forgets to subtract the room temperature.",
    ncert="Class 11 Physics, 'Thermal Properties of Matter', Newton's law of cooling", seconds=100, recomputed=True)

W_bub = 2 * 4 * math.pi * (1e-2) ** 2 * 0.03
assert close(W_bub, 2.4 * math.pi * 1e-5) and close(W_bub / 2, 1.2 * math.pi * 1e-5)
assert close(2 * math.pi * (1e-2) ** 2 * 0.03, 0.6 * math.pi * 1e-5) and close(2 * 4 * math.pi * 1 * 0.03, 0.24 * math.pi)
add(T, "Surface tension and capillarity", "Advanced", "numerical",
    "A soap bubble of radius 1 cm is blown slowly (at constant temperature) from a soap solution of surface tension "
    "0.03 N/m. The work done in blowing it is:",
    place("2.4π × 10⁻⁵ J", ["1.2π × 10⁻⁵ J", "0.6π × 10⁻⁵ J", "0.24π J"], "A"),
    "Surface energy of a film with two surfaces",
    "Work done at constant temperature = surface tension × increase in surface area. A soap bubble is a thin film "
    "with an inner and an outer surface, so the new area is 2 × 4πr².",
    ["Area created = 2 × 4πr² = 8π × 10⁻⁴ m²", "W = S × ΔA = 0.03 × 8π × 10⁻⁴ = 2.4π × 10⁻⁵ J (≈ 7.5 × 10⁻⁵ J)"],
    why="1.2π × 10⁻⁵ J counts only one surface, as for a liquid drop. 0.6π × 10⁻⁵ J uses πr² for the area of each "
        "surface. 0.24π J leaves r in centimetres.",
    ncert="Class 11 Physics, 'Mechanical Properties of Fluids', surface tension and surface energy", seconds=60,
    recomputed=True)

add(T, "Fluid pressure and Pascal's law", "Advanced", "multi_statement",
    multi("For a liquid at rest in an open container, which of the following statements are correct?",
          ["At any point in the liquid, the pressure is the same in all directions.",
           "The pressure is the same at all points at the same horizontal level in the liquid.",
           "The pressure at a given depth depends on the shape of the container.",
           "The gauge pressure at a point is the absolute pressure there minus the atmospheric pressure.",
           "Pressure is a vector quantity, because it acts in all directions."]),
    place("(a), (b) and (d) only",
          ["(a), (b), (c) and (d) only", "(b), (d) and (e) only", "(a), (b) and (e) only"], "C"),
    "Pressure in a fluid at rest",
    "Pressure at a point in a fluid at rest acts equally in all directions and depends only on the depth "
    "(P = Pₐ + ρgh), not on the shape of the container (the hydrostatic paradox). Pressure is a scalar: the force "
    "it produces is always normal to the surface it acts on, whatever that surface's orientation.",
    ["(a) True: Pascal's observation", "(b) True: points at the same depth have the same pressure",
     "(c) False: P depends only on h (hydrostatic paradox)", "(d) True: P_gauge = P − Pₐ",
     "(e) False: pressure is a scalar"],
    why="Options with (c) or (e) include a false statement; (a), (b) and (d) are all true.",
    ncert="Class 11 Physics, 'Mechanical Properties of Fluids', pressure and Pascal's law", seconds=70)


# =====================================================================================================================
# Thermodynamics (B3 I4 A3)
# =====================================================================================================================
T = "Thermodynamics"

W_iso = 2e5 * (4 - 1) * 1e-3
assert close(W_iso, 600) and close(2e5 * 3, 6e5) and close(2e5 * 4e-3, 800) and close(2e5 * 1e-3, 200)
add(T, "Zeroth and first law", "Basic", "numerical",
    "A gas expands at a constant pressure of 2 × 10⁵ Pa from a volume of 1 L to a volume of 4 L. The work done by "
    "the gas is:",
    place("600 J", ["6 × 10⁵ J", "800 J", "200 J"], "D"),
    "Work done in an isobaric process: W = PΔV",
    "At constant pressure, the work done by the gas equals the pressure times the change in volume, with volume in "
    "m³ (1 L = 10⁻³ m³).",
    ["ΔV = 4 − 1 = 3 L = 3 × 10⁻³ m³", "W = 2 × 10⁵ × 3 × 10⁻³ = 600 J"],
    why="6 × 10⁵ J leaves the volume in litres. 800 J uses the final volume instead of the change. 200 J uses the "
        "initial volume.",
    ncert="Class 11 Physics, 'Thermodynamics', first law of thermodynamics", seconds=30, recomputed=True)

add(T, "Isothermal and adiabatic processes", "Basic", "direct",
    "Heat is supplied to an ideal gas kept in a closed vessel of fixed volume. The heat supplied:",
    place("Is used entirely to increase the internal energy of the gas",
          ["Is used entirely in doing work against the surroundings",
           "Is shared equally between doing work and raising the internal energy",
           "Leaves the internal energy of the gas unchanged"], "C"),
    "Isochoric process and the first law",
    "In an isochoric (constant-volume) process the gas does no work, W = PΔV = 0. By the first law, ΔQ = ΔU + ΔW, "
    "so all the heat supplied raises the internal energy and hence the temperature.",
    ["ΔV = 0 → ΔW = 0", "ΔQ = ΔU + 0 → ΔU = ΔQ"],
    why="With no change in volume the gas does no work, so none of the heat can go into work and the internal energy "
        "must rise by the full amount.",
    ncert="Class 11 Physics, 'Thermodynamics', thermodynamic processes (isochoric process)", seconds=30)

add(T, "Zeroth and first law", "Basic", "statement_pair",
    SP_STEM.format(
        s1="In a cyclic process, the change in the internal energy of the system is zero.",
        s2="In a cyclic process, the net heat absorbed by the system is equal to the net work done by the system."),
    sp("A"),
    "First law applied to a cyclic process",
    "Internal energy is a state variable. In a cycle the system returns to its initial state, so ΔU = 0, and the "
    "first law ΔQ = ΔU + ΔW then gives ΔQ = ΔW.",
    ["Statement I: U depends only on state → ΔU = 0 over a cycle → true",
     "Statement II: ΔQ = 0 + ΔW → true"],
    why="Both statements are true: the second follows from the first through the first law.",
    ncert="Class 11 Physics, 'Thermodynamics', first law of thermodynamics and state variables", seconds=35)

cp_m, cv_m, R_m = F(910), F(650), F(832, 100)
M_gas = R_m / (cp_m - cv_m)                     # kg/mol
assert M_gas == F(32, 1000) and cp_m / cv_m == F(7, 5)
assert round(float(R_m / cv_m) * 1000, 1) == 12.8 and round(float(R_m / cp_m) * 1000, 1) == 9.1
add(T, "Zeroth and first law", "Intermediate", "numerical",
    "For a certain ideal gas, the specific heat capacities per unit mass are c_p = 910 J kg⁻¹ K⁻¹ at constant "
    "pressure and c_v = 650 J kg⁻¹ K⁻¹ at constant volume. Taking R = 8.32 J mol⁻¹ K⁻¹, the molar mass of the gas "
    "is:",
    place("32 g mol⁻¹", ["12.8 g mol⁻¹", "9.1 g mol⁻¹", "0.032 g mol⁻¹"], "A"),
    "Specific heats of an ideal gas: C_p − C_v = R (molar), so c_p − c_v = R/M (per unit mass)",
    "The molar specific heats are the specific heats per unit mass multiplied by the molar mass M: C = Mc. "
    "Mayer's relation C_p − C_v = R then gives M(c_p − c_v) = R.",
    ["c_p − c_v = 910 − 650 = 260 J kg⁻¹ K⁻¹", "M = R/(c_p − c_v) = 8.32/260 = 0.032 kg mol⁻¹",
     "M = 32 g mol⁻¹ (γ = 910/650 = 1.4, consistent with a diatomic gas)"],
    why="12.8 g mol⁻¹ divides R by c_v alone, and 9.1 g mol⁻¹ divides R by c_p alone, instead of by their "
        "difference. 0.032 g mol⁻¹ is the right number in kg mol⁻¹ written with the wrong unit.",
    ncert="Class 11 Physics, 'Thermodynamics', specific heat capacity", seconds=60, recomputed=True)

W_ad = 2 * F(3, 2) * F(83, 10) * 150
assert W_ad == F(3735) and 2 * F(5, 2) * F(83, 10) * 150 == 6225 and 2 * F(83, 10) * 150 == 2490
add(T, "Isothermal and adiabatic processes", "Intermediate", "numerical",
    "Two moles of a monatomic ideal gas expand adiabatically, and the temperature falls from 400 K to 250 K. Taking "
    "R = 8.3 J mol⁻¹ K⁻¹, the work done by the gas is:",
    place("3735 J", ["6225 J", "2490 J", "−3735 J"], "B"),
    "Work in an adiabatic process",
    "In an adiabatic process ΔQ = 0, so the work done by the gas equals the decrease in its internal energy: "
    "W = −ΔU = nC_v(T₁ − T₂), with C_v = 3R/2 for a monatomic gas.",
    ["ΔU = nC_vΔT = 2 × 1.5 × 8.3 × (250 − 400) = −3735 J", "W = −ΔU = +3735 J (the gas does work as it expands)"],
    why="6225 J uses C_p = 5R/2 instead of C_v. 2490 J uses nRΔT. −3735 J is ΔU; the work done by an expanding gas "
        "is positive.",
    shortcut="W = nR(T₁ − T₂)/(γ − 1) = 2 × 8.3 × 150/(2/3) = 3735 J.",
    ncert="Class 11 Physics, 'Thermodynamics', adiabatic process", seconds=60, recomputed=True)

add(T, "Isothermal and adiabatic processes", "Intermediate", "assertion_reason",
    AR_STEM.format(
        a="In an isothermal expansion of an ideal gas, the heat absorbed by the gas equals the work done by it.",
        r="The internal energy of an ideal gas depends only on its temperature."),
    ar("A"),
    "Isothermal process for an ideal gas",
    "Since the internal energy of an ideal gas depends only on temperature, ΔU = 0 when T is constant. The first law "
    "then gives ΔQ = ΔW. So R is precisely the reason A holds.",
    ["R → T constant gives ΔU = 0", "First law: ΔQ = ΔU + ΔW = ΔW", "R explains A → option A"],
    why="Both are true and A follows from R through the first law. A single expansion is not a cycle, so this does "
        "not contradict the second law.",
    ncert="Class 11 Physics, 'Thermodynamics', isothermal process", seconds=40)

add(T, "Isothermal and adiabatic processes", "Intermediate", "match_list",
    match_stem("Match List-I (process undergone by an ideal gas) with List-II (the condition that holds in it).",
               ["Isothermal", "Adiabatic", "Isochoric", "Isobaric"],
               ["W = 0", "Q = 0", "ΔU = 0", "Q = nC_pΔT"]),
    match_options({"A": "III", "B": "II", "C": "I", "D": "IV"},
                  [{"A": "II", "B": "III", "C": "I", "D": "IV"}, {"A": "III", "B": "II", "C": "IV", "D": "I"},
                   {"A": "III", "B": "I", "C": "II", "D": "IV"}], "C"),
    "Special thermodynamic processes",
    "Isothermal: T constant, so ΔU = 0 for an ideal gas. Adiabatic: no heat exchanged. Isochoric: no change in "
    "volume, so no work. Isobaric: heat supplied at constant pressure is nC_pΔT.",
    ["A: isothermal → ΔU = 0 → III", "B: adiabatic → Q = 0 → II", "C: isochoric → W = 0 → I",
     "D: isobaric → Q = nC_pΔT → IV"],
    why="The other codes swap isothermal with adiabatic (ΔU = 0 versus Q = 0), or isochoric with isobaric.",
    ncert="Class 11 Physics, 'Thermodynamics', thermodynamic processes", seconds=40)

R_h, T_h0, ln2_h = 8.3, 300, 0.693
Q_isobar = 2.5 * R_h * (2 * T_h0 - T_h0)        # 1 mol monatomic, V doubles at constant P -> T doubles
Q_isoth = R_h * (2 * T_h0) * ln2_h              # isothermal at 600 K, V doubles again
assert close(Q_isobar, 6225) and close(Q_isoth, 3451.14) and round((Q_isobar + Q_isoth) / 1000, 2) == 9.68
assert round((Q_isobar + R_h * T_h0 * ln2_h) / 1000, 2) == 7.95
assert round((1.5 * R_h * T_h0 + Q_isoth) / 1000, 2) == 7.19 and close(Q_isobar, 6225)  # 6.225 kJ, shown as 6.23 kJ
add(T, "Isothermal and adiabatic processes", "Advanced", "numerical",
    "One mole of a monatomic ideal gas at 300 K is heated at constant pressure until its volume doubles. It then "
    "expands reversibly and isothermally until its volume doubles again. Taking R = 8.3 J mol⁻¹ K⁻¹ and "
    "ln 2 = 0.693, the total heat absorbed by the gas in the two processes is about:",
    place("9.68 kJ", ["7.95 kJ", "7.19 kJ", "6.23 kJ"], "D"),
    "Heat absorbed in isobaric and isothermal processes",
    "At constant pressure V ∝ T, so doubling V doubles T, and Q = nC_pΔT with C_p = 5R/2. In the isothermal step "
    "ΔU = 0, so the heat absorbed equals the work done, nRT ln(V₂/V₁), at the new temperature.",
    ["Isobaric: T goes 300 K → 600 K; Q₁ = 1 × 2.5 × 8.3 × 300 = 6225 J",
     "Isothermal at 600 K: Q₂ = W = 1 × 8.3 × 600 × 0.693 ≈ 3451 J",
     "Total Q = 6225 + 3451 ≈ 9676 J ≈ 9.68 kJ"],
    why="7.95 kJ does the isothermal step at the starting temperature of 300 K instead of 600 K. 7.19 kJ uses "
        "C_v = 3R/2 for the constant-pressure heating. 6.23 kJ assumes no heat is absorbed in the isothermal step "
        "because the temperature does not change; in fact ΔU = 0 there, so Q = W.",
    ncert="Class 11 Physics, 'Thermodynamics', thermodynamic processes; specific heat capacity", seconds=120,
    recomputed=True)

# 1 mol monatomic, P = kV from V0 to 2V0; units R*T0 = P0*V0 = 1
P0V0 = F(1)
T2 = 4  # (2P0)(2V0) = 4 P0V0
dU = F(3, 2) * (T2 - 1) * P0V0
Wl = (1 + 2) * P0V0 / 2  # trapezium area (P0 + 2P0)/2 * V0
Q = dU + Wl
assert dU == F(9, 2) and Wl == F(3, 2) and Q == 6 and dU - Wl == 3
add(T, "Zeroth and first law", "Advanced", "numerical",
    "One mole of a monatomic ideal gas at temperature T₀ expands from volume V₀ to 2V₀ in such a way that its "
    "pressure is directly proportional to its volume throughout. The heat absorbed by the gas in this process is:",
    place("6RT₀", ["4.5RT₀", "1.5RT₀", "3RT₀"], "A"),
    "First law for a process along a straight line on the P–V diagram",
    "Find the final temperature from the gas equation, the change in internal energy from C_v = 3R/2, and the work "
    "as the area under the P–V line (a trapezium). Then Q = ΔU + W.",
    ["P ∝ V: P goes from P₀ to 2P₀ while V goes from V₀ to 2V₀ → T_f = 4T₀",
     "ΔU = (3/2)R(4T₀ − T₀) = 4.5RT₀",
     "W = ½(P₀ + 2P₀)V₀ = 1.5P₀V₀ = 1.5RT₀", "Q = 4.5RT₀ + 1.5RT₀ = 6RT₀"],
    why="4.5RT₀ is only ΔU and 1.5RT₀ is only the work. 3RT₀ subtracts the work from ΔU, a sign error in the first "
        "law.",
    ncert="Class 11 Physics, 'Thermodynamics', first law of thermodynamics", seconds=120, recomputed=True)

add(T, "Second law, reversible and irreversible processes", "Advanced", "multi_statement",
    multi("Which of the following statements are correct?",
          ["A process that takes the system through non-equilibrium states, such as an explosive chemical "
           "reaction, is irreversible.",
           "A process is reversible only if it can be turned back so that both the system and its surroundings "
           "return to their original states, with no other change anywhere in the universe.",
           "Any process at the end of which the system has come back to its initial state is a reversible process.",
           "When a liquid in a thermally insulated vessel is stirred, its temperature rises; this process is "
           "irreversible, because the liquid cannot by itself convert that internal energy back into work that "
           "turns the stirrer.",
           "A process carried out very rapidly, such as a sudden compression of a gas, becomes reversible if the "
           "walls of the container are perfectly insulating."]),
    place("(a), (b) and (d) only",
          ["(a), (b), (c) and (d) only", "(b), (d) and (e) only", "(a), (d) and (e) only"], "B"),
    "Reversible and irreversible processes",
    "A reversible process can be turned back with both the system and the surroundings restored and no change "
    "anywhere else. Irreversibility arises when a process takes the system through non-equilibrium states (free "
    "expansion, an explosive reaction, a sudden compression) or when dissipative effects such as viscosity and "
    "friction turn work into internal energy.",
    ["(a) True: non-equilibrium states make a process irreversible",
     "(b) True: this is the definition of a reversible process",
     "(c) False: the system may return to its initial state while the surroundings are left changed",
     "(d) True: stirring is a dissipative process; the work done becomes internal energy and cannot be fully "
     "recovered",
     "(e) False: insulating the walls makes the process adiabatic, but a rapid process still passes through "
     "non-equilibrium states, so it stays irreversible"],
    why="Every other option includes (c) or (e), each of which is false.",
    ncert="Class 11 Physics, 'Thermodynamics', reversible and irreversible processes", seconds=75)


# =====================================================================================================================
# Kinetic Theory of Gases (B2 I2 A2)
# =====================================================================================================================
T = "Kinetic Theory of Gases"


def gamma_from_cv(cv):          # cv in units of R
    return (cv + 1) / cv


assert gamma_from_cv(F(3, 2)) == F(5, 3) and gamma_from_cv(F(5, 2)) == F(7, 5)
assert gamma_from_cv(F(7, 2)) == F(9, 7) and gamma_from_cv(F(3)) == F(4, 3)
add(T, "Degrees of freedom and equipartition", "Basic", "match_list",
    match_stem("Match List-I (ideal gas) with List-II (its ratio of specific heats γ = C_p/C_v), using the law of "
               "equipartition of energy.",
               ["Monatomic gas", "Diatomic gas with rigid molecules (no vibration)",
                "Diatomic gas whose molecules also have one mode of vibration",
                "Polyatomic gas with rigid non-linear molecules (no vibration)"],
               ["4/3", "9/7", "5/3", "7/5"]),
    match_options({"A": "III", "B": "IV", "C": "II", "D": "I"},
                  [{"A": "III", "B": "II", "C": "IV", "D": "I"}, {"A": "IV", "B": "III", "C": "II", "D": "I"},
                   {"A": "III", "B": "IV", "C": "I", "D": "II"}], "C"),
    "Specific heats from equipartition",
    "Each translational and rotational degree of freedom contributes R/2 to C_v; a vibrational mode contributes R "
    "(kinetic plus potential). Then C_p = C_v + R and γ = C_p/C_v.",
    ["Monatomic: C_v = 3R/2 → γ = 5/3 (III)", "Rigid diatomic: C_v = 5R/2 → γ = 7/5 (IV)",
     "Diatomic with vibration: C_v = 5R/2 + R = 7R/2 → γ = 9/7 (II)",
     "Rigid non-linear polyatomic: 3 translational + 3 rotational → C_v = 3R → γ = 4/3 (I)"],
    why="The other codes swap the vibrating diatomic gas with the rigid one, or with the polyatomic gas. More active "
        "degrees of freedom always mean a smaller γ.",
    ncert="Class 11 Physics, 'Kinetic Theory', specific heat capacity (law of equipartition of energy)", seconds=60)

add(T, "Pressure and rms speed", "Basic", "direct",
    "When an ideal gas in a closed, rigid container is heated, its pressure rises. According to the kinetic theory "
    "of gases, this is because:",
    place("The molecules move faster on average, so they strike the walls more often and with a greater change of "
          "momentum in each collision",
          ["The number of molecules in the container increases",
           "The molecules become larger in size",
           "The attractive forces between the molecules increase"], "A"),
    "Kinetic interpretation of pressure and temperature",
    "P = (1/3)nm v̄², where v̄² is the mean square speed. At fixed volume the number density n is fixed, and heating "
    "raises the mean kinetic energy of the molecules, so v̄² and hence P increase.",
    ["P = (1/3) n m v̄²", "Closed rigid container → n fixed", "Heating → average kinetic energy ∝ T rises → P rises"],
    why="The number of molecules in a closed container does not change. In the ideal-gas model the molecules are "
        "point-like and have no intermolecular forces, so neither size nor attraction enters.",
    ncert="Class 11 Physics, 'Kinetic Theory', pressure of an ideal gas and kinetic interpretation of temperature",
    seconds=35)

E_dens = 1.5 * 1.5e5
assert close(E_dens, 2.25e5) and close(1.5e5 * 2 / 3, 1.0e5) and close(3 * 1.5e5, 4.5e5)
add(T, "Pressure and rms speed", "Intermediate", "numerical",
    "An ideal gas is at a pressure of 1.5 × 10⁵ Pa. The total translational kinetic energy of its molecules per unit "
    "volume is:",
    place("2.25 × 10⁵ J/m³", ["1.0 × 10⁵ J/m³", "1.5 × 10⁵ J/m³", "4.5 × 10⁵ J/m³"], "D"),
    "Pressure and kinetic energy density",
    "From kinetic theory P = (1/3)ρv̄² and the translational kinetic energy per unit volume is E = ½ρv̄². "
    "Dividing gives P = (2/3)E.",
    ["E = (3/2)P", "E = 1.5 × 1.5 × 10⁵ = 2.25 × 10⁵ J/m³"],
    why="1.0 × 10⁵ J/m³ uses E = (2/3)P, inverting the relation. 1.5 × 10⁵ J/m³ equates E with P. "
        "4.5 × 10⁵ J/m³ uses E = 3P, from P = (1/3)ρv̄² without the ½ in the kinetic energy.",
    ncert="Class 11 Physics, 'Kinetic Theory', pressure of an ideal gas", seconds=45, recomputed=True)

add(T, "Mean free path", "Intermediate", "statement_pair",
    SP_STEM.format(
        s1="The mean free path of the molecules of a gas increases when the number of molecules per unit volume "
           "increases.",
        s2="The mean free path of the molecules of a gas does not depend on the size (diameter) of the molecules."),
    sp("B"),
    "Mean free path: l = 1/(√2 π n d²)",
    "The mean free path is the average distance a molecule travels between collisions. The more molecules there are "
    "per unit volume, and the larger they are, the more often they collide, so l is inversely proportional to both "
    "n and d².",
    ["Statement I: l ∝ 1/n → l decreases as n increases → false",
     "Statement II: l ∝ 1/d² → depends on molecular size → false"],
    why="Both statements contradict l = 1/(√2 π n d²), so 'both false' is the only consistent choice.",
    ncert="Class 11 Physics, 'Kinetic Theory', mean free path", seconds=40)

ratio_rms = math.sqrt((400 / 32) / (300 / 2))
assert close(ratio_rms, 1 / (2 * math.sqrt(3))) and close(math.sqrt(2 / 32), 0.25)
add(T, "Pressure and rms speed", "Advanced", "numerical",
    "The ratio of the rms speed of oxygen molecules (molar mass 32 g/mol) at 127 °C to the rms speed of hydrogen "
    "molecules (molar mass 2 g/mol) at 27 °C is:",
    place("1/(2√3)", ["2√3", "1/4", "1/12"], "B"),
    "rms speed: v_rms = √(3RT/M)",
    "Use absolute temperatures and the molar masses in v_rms ∝ √(T/M).",
    ["T(O₂) = 400 K, T(H₂) = 300 K", "Ratio = √[(400/32)/(300/2)] = √(12.5/150) = √(1/12)",
     "= 1/(2√3) ≈ 0.29"],
    why="2√3 inverts the ratio. 1/4 ignores the difference in temperature. 1/12 forgets the square root.",
    ncert="Class 11 Physics, 'Kinetic Theory', kinetic interpretation of temperature (rms speed)", seconds=60,
    recomputed=True)

T_N2 = F(320) * 28 / 32
assert T_N2 == 280 and close(320 * 32 / 28, 365.7) and close(320 * (28 / 32) ** 2, 245)
add(T, "Pressure and rms speed", "Advanced", "numerical",
    "The rms speed of oxygen molecules (molar mass 32 g/mol) at 320 K is equal to the rms speed of nitrogen molecules "
    "(molar mass 28 g/mol) at a temperature of:",
    place("280 K", ["366 K", "245 K", "320 K"], "C"),
    "Equal rms speeds: T/M must be equal",
    "Since v_rms = √(3RT/M), two gases have equal rms speeds when T/M is the same for both. The lighter gas needs the "
    "lower temperature.",
    ["T(N₂)/28 = 320/32", "T(N₂) = 320 × 28/32 = 280 K (= 7 °C)"],
    why="366 K inverts the mass ratio (320 × 32/28). 245 K squares the mass ratio. 320 K assumes rms speed depends "
        "only on temperature; it is the average kinetic energy, not the speed, that is the same for all gases at one "
        "temperature.",
    ncert="Class 11 Physics, 'Kinetic Theory', kinetic interpretation of temperature (rms speed)", seconds=50,
    recomputed=True)


# =====================================================================================================================
# Oscillations and Waves (B4 I5 A4)
# =====================================================================================================================
T = "Oscillations and Waves"

add(T, "SHM equation and phase", "Basic", "multi_statement",
    multi("For a particle executing simple harmonic motion, which of the following statements are correct?",
          ["Its acceleration is a = −ω²x, where x is its displacement from the mean position.",
           "The period of a block oscillating on a spring does not depend on the amplitude of oscillation.",
           "Its velocity leads its displacement in phase by π/2.",
           "A motion described by x = A sin ωt + B cos ωt is not simple harmonic.",
           "Every periodic motion is simple harmonic."]),
    place("(a), (b) and (c) only",
          ["(a), (b) and (d) only", "(b), (c) and (e) only", "(a), (b), (c) and (e) only"], "D"),
    "Characteristics of simple harmonic motion",
    "SHM has a restoring acceleration proportional to displacement, a period set by the system (T = 2π√(m/k) for a "
    "spring) and not by the amplitude, and a velocity v = dx/dt that is a quarter cycle ahead of x. A sin ωt + "
    "B cos ωt is a single sinusoid of the same ω, so it is SHM. Many periodic motions (e.g. uniform circular motion "
    "itself, or the motion of a planet) are not SHM.",
    ["(a) True: defining relation of SHM", "(b) True: T = 2π√(m/k), independent of A",
     "(c) True: x = A cos ωt → v = −Aω sin ωt = Aω cos(ωt + π/2)",
     "(d) False: it equals C sin(ωt + φ) → SHM", "(e) False: periodic does not imply simple harmonic"],
    why="Options with (d) or (e) include a false statement; (a), (b) and (c) are all true.",
    ncert="Class 11 Physics, 'Oscillations', simple harmonic motion", seconds=60)

add(T, "Spring and pendulum oscillations", "Basic", "assertion_reason",
    AR_STEM.format(
        a="Doubling the mass of the bob of a simple pendulum increases its time period.",
        r="For small oscillations, the time period of a simple pendulum is T = 2π√(L/g)."),
    ar("D"),
    "Period of a simple pendulum",
    "T = 2π√(L/g) contains only the length and g. The mass of the bob cancels because both the restoring torque "
    "and the moment of inertia are proportional to it. So changing the mass does not change the period.",
    ["R: T = 2π√(L/g) for small oscillations → true", "A: T has no dependence on mass → false",
     "A false, R true → option D"],
    why="A is false; in fact R shows directly that the mass of the bob does not appear in the period.",
    ncert="Class 11 Physics, 'Oscillations', the simple pendulum", seconds=30)

add(T, "Progressive waves and wave speed", "Basic", "statement_pair",
    SP_STEM.format(
        s1="For a progressive wave, the wave speed equals the product of its frequency and its wavelength.",
        s2="When a sound wave passes from air into water, its frequency changes."),
    sp("C"),
    "v = νλ and what changes at a boundary",
    "In one period the wave advances one wavelength, so v = λ/T = νλ. The frequency is set by the source and stays "
    "the same when the wave enters another medium; the speed and wavelength change.",
    ["Statement I: v = νλ → true", "Statement II: frequency is fixed by the source → false"],
    why="At a boundary the frequency is unchanged; it is the speed and the wavelength that change.",
    ncert="Class 11 Physics, 'Waves', the speed of a travelling wave", seconds=30)

add(T, "Superposition and standing waves", "Basic", "direct",
    "In a stationary wave of wavelength λ, the distance between a node and the nearest antinode is:",
    place("λ/4", ["λ/2", "λ", "2λ"], "B"),
    "Positions of nodes and antinodes",
    "Nodes are separated by λ/2, antinodes are separated by λ/2, and each antinode lies midway between two nodes, so a "
    "node and the next antinode are λ/4 apart.",
    ["Node to node = λ/2", "Antinode is midway → node to antinode = λ/4"],
    why="λ/2 is the distance between consecutive nodes (or consecutive antinodes). λ and 2λ are larger still.",
    ncert="Class 11 Physics, 'Waves', standing waves and normal modes", seconds=20)

A_ = 4 * math.sqrt(2)
x_eq = A_ / math.sqrt(2)
assert close(x_eq, 4)
k_ = 1.0
assert close(0.5 * k_ * x_eq ** 2, 0.5 * k_ * (A_ ** 2 - x_eq ** 2))
assert close(A_ / 2, 2 * math.sqrt(2)) and close(A_ * math.sqrt(3) / 2, 2 * math.sqrt(6))
add(T, "Energy in SHM", "Intermediate", "numerical",
    "A particle executes simple harmonic motion with an amplitude of 4√2 cm. At what distance from the mean position "
    "are its kinetic energy and potential energy equal?",
    place("4 cm", ["2√2 cm", "4√2 cm", "2√6 cm"], "B"),
    "Energy in SHM",
    "U = ½kx² and K = ½k(A² − x²). Setting K = U gives x² = A²/2.",
    ["½k(A² − x²) = ½kx² → x² = A²/2", "x = A/√2 = 4√2/√2 = 4 cm"],
    why="2√2 cm is A/2, where the potential energy is only a quarter of the total. 4√2 cm is the extreme position, "
        "where the kinetic energy is zero. 2√6 cm is A√3/2, where the potential energy is three times the kinetic "
        "energy.",
    ncert="Class 11 Physics, 'Oscillations', energy in simple harmonic motion", seconds=40, recomputed=True)

f1_closed = 340 / (4 * 0.85)
assert close(f1_closed, 100) and close(3 * f1_closed, 300) and close(340 / 0.85, 400)
add(T, "Organ pipes and beats", "Intermediate", "numerical",
    "A pipe 85 cm long is closed at one end. Taking the speed of sound in air as 340 m/s and neglecting end "
    "correction, the frequency of its first overtone is:",
    place("300 Hz", ["200 Hz", "100 Hz", "400 Hz"], "C"),
    "Normal modes of a pipe closed at one end",
    "A closed pipe has a node at the closed end and an antinode at the open end. Its fundamental is v/4L, and only odd "
    "harmonics occur, so the first overtone is the third harmonic, 3v/4L.",
    ["Fundamental = v/(4L) = 340/(4 × 0.85) = 100 Hz", "First overtone = 3 × 100 = 300 Hz"],
    why="200 Hz assumes even harmonics occur, as in an open pipe. 100 Hz is the fundamental, not the first overtone. "
        "400 Hz (v/L) is the second harmonic of an open pipe of this length.",
    ncert="Class 11 Physics, 'Waves', standing waves and normal modes (closed pipe)", seconds=45, recomputed=True)

T_cut = 2 / math.sqrt(2)
assert close(T_cut, math.sqrt(2)) and close(2 * math.sqrt(2), 2.828)
add(T, "Spring and pendulum oscillations", "Intermediate", "numerical",
    "A block attached to a light spring oscillates with a period of 2 s. The spring is cut into two equal halves, and "
    "the same block is attached to one half. The new period of oscillation is:",
    place("√2 s", ["1 s", "2√2 s", "2 s"], "D"),
    "Spring constant of a cut spring",
    "For a given force, each half stretches half as much as the whole spring, so each half has spring constant 2k. "
    "Since T ∝ 1/√k, the period becomes T/√2.",
    ["k' = 2k", "T' = 2π√(m/2k) = T/√2 = 2/√2 = √2 s ≈ 1.41 s"],
    why="1 s takes T ∝ 1/k (forgetting the square root). 2√2 s takes the half spring as softer (k/2). 2 s assumes "
        "the spring constant does not change on cutting.",
    ncert="Class 11 Physics, 'Oscillations', oscillations due to a spring", seconds=45, recomputed=True)

add(T, "Progressive waves and wave speed", "Intermediate", "assertion_reason",
    AR_STEM.format(
        a="The speed of sound in air increases with an increase in the temperature of the air.",
        r="The speed of sound in air is directly proportional to the absolute temperature of the air."),
    ar("C"),
    "Temperature dependence of the speed of sound",
    "v = √(γP/ρ) = √(γRT/M) for air treated as an ideal gas, so v increases with temperature but in proportion to "
    "√T, not to T.",
    ["A: v ∝ √T → v rises with T → true", "R: v ∝ T is wrong; v ∝ √T → false", "A true, R false → option C"],
    why="R overstates the dependence: doubling the absolute temperature multiplies the speed by √2, not 2.",
    ncert="Class 11 Physics, 'Waves', speed of a longitudinal wave (Laplace correction)", seconds=40)

add(T, "Superposition and standing waves", "Intermediate", "match_list",
    match_stem("Match List-I (mode of vibration) with List-II (wavelength). A string of length L is fixed at both "
               "ends; each pipe has length L. Neglect end corrections.",
               ["Fundamental mode of the string", "Third harmonic of the string",
                "Fundamental mode of a pipe closed at one end", "Second harmonic of a pipe open at both ends"],
               ["4L", "2L", "L", "2L/3"]),
    match_options({"A": "II", "B": "IV", "C": "I", "D": "III"},
                  [{"A": "I", "B": "IV", "C": "II", "D": "III"}, {"A": "II", "B": "III", "C": "I", "D": "IV"},
                   {"A": "III", "B": "IV", "C": "I", "D": "II"}], "C"),
    "Wavelengths of normal modes",
    "A string fixed at both ends (and a pipe open at both ends) fits n half-wavelengths: λ = 2L/n. A pipe closed at "
    "one end fits an odd number of quarter-wavelengths: λ = 4L/(2n − 1).",
    ["A: string, n = 1 → λ = 2L → II", "B: string, n = 3 → λ = 2L/3 → IV",
     "C: closed pipe, fundamental → λ = 4L → I", "D: open pipe, n = 2 → λ = L → III"],
    why="The other codes give the closed pipe the 2L of a string, or swap the second and third harmonics.",
    ncert="Class 11 Physics, 'Waves', standing waves and normal modes", seconds=50)

beats = 400 * (math.sqrt(1.01) - 1)
assert abs(beats - 2) < 0.01 and close(400 * 0.01, 4) and close(400 * (1.01 ** 2 - 1), 8.04)
add(T, "Organ pipes and beats", "Advanced", "numerical",
    "Two identical stretched wires, under the same tension, each vibrate in their fundamental mode at 400 Hz. The "
    "tension in one wire is increased by 1%. When the two wires now vibrate together in their fundamental modes, the "
    "number of beats heard per second is about:",
    place("2", ["4", "0.5", "8"], "B"),
    "Frequency of a string and beats",
    "The fundamental frequency of a string is ν = (1/2L)√(T/μ), so ν ∝ √T. For a small change, Δν/ν = ½ ΔT/T. The "
    "beat frequency is the difference of the two frequencies.",
    ["Δν/ν = ½ × 1% = 0.5%", "Δν = 0.005 × 400 = 2 Hz", "Beats = 2 per second"],
    why="4 takes ν ∝ T (forgets the square root). 0.5 is the percentage change in frequency, not the beat "
        "frequency. 8 takes ν ∝ T².",
    ncert="Class 11 Physics, 'Waves', speed of a transverse wave on a stretched string; beats", seconds=70,
    recomputed=True)

w_s = math.sqrt(10 / 0.1)
v_mx = 0.05 * w_s
assert close(w_s, 10) and close(v_mx, 0.5) and close(0.10 * w_s, 1.0) and close(0.15 * w_s, 1.5)
add(T, "Spring and pendulum oscillations", "Advanced", "numerical",
    "A block hung from a light vertical spring stretches it by 10 cm at equilibrium. The block is then pulled down a "
    "further 5 cm and released. Taking g = 10 m/s², the maximum speed of the block during the oscillations is:",
    place("0.5 m/s", ["1.0 m/s", "1.5 m/s", "0.05 m/s"], "C"),
    "Vertical spring–block oscillator",
    "At equilibrium kx₀ = mg, so ω² = k/m = g/x₀. The block oscillates about the equilibrium position, so the "
    "amplitude is the extra 5 cm, not the total extension. Maximum speed = Aω.",
    ["ω = √(g/x₀) = √(10/0.1) = 10 rad/s", "A = 5 cm = 0.05 m (measured from equilibrium)",
     "v_max = Aω = 0.05 × 10 = 0.5 m/s"],
    why="1.0 m/s uses the static extension (10 cm) as the amplitude. 1.5 m/s uses the total extension (15 cm). "
        "0.05 m/s gives the amplitude in metres without multiplying by ω.",
    ncert="Class 11 Physics, 'Oscillations', oscillations due to a spring", seconds=80, recomputed=True)

A_w, w_w, k_w = 0.03, 20 * math.pi, 0.5 * math.pi
assert close(A_w * w_w, 0.6 * math.pi) and close(w_w / k_w, 40) and close(A_w * w_w ** 2, 12 * math.pi ** 2)
assert close(A_w * k_w, 0.015 * math.pi)
add(T, "Progressive waves and wave speed", "Advanced", "numerical",
    "A transverse wave on a string is described by y(x, t) = 0.03 sin(20πt − 0.5πx), where x and y are in metres and "
    "t in seconds. The maximum speed of a particle of the string is:",
    place("0.6π m/s", ["40 m/s", "12π² m/s", "0.015π m/s"], "D"),
    "Particle velocity versus wave velocity",
    "Each particle of the string executes SHM with amplitude A and angular frequency ω, so its maximum speed is Aω. "
    "This is different from the wave speed ω/k, at which the disturbance travels.",
    ["A = 0.03 m, ω = 20π rad/s, k = 0.5π rad/m", "Maximum particle speed = Aω = 0.03 × 20π = 0.6π m/s ≈ 1.9 m/s",
     "(Wave speed = ω/k = 40 m/s, for comparison)"],
    why="40 m/s is the wave speed ω/k, not the particle speed. 12π² is the maximum particle acceleration Aω² "
        "(in m/s²). 0.015π is Ak, the maximum slope of the string, which has no unit of speed.",
    ncert="Class 11 Physics, 'Waves', displacement relation in a progressive wave", seconds=60, recomputed=True)

add(T, "Superposition and standing waves", "Advanced", "multi_statement",
    multi("Which of the following statements about reflection and stationary waves on a string are correct?",
          ["A wave reflected from a rigid boundary undergoes a phase change of π.",
           "Nodes are points where the displacement is zero at all times.",
           "A wave reflected from an open (free) boundary undergoes a phase change of π.",
           "A stationary wave is formed by the superposition of two identical waves travelling in opposite "
           "directions.",
           "All particles of a string carrying a stationary wave oscillate with the same amplitude."]),
    place("(a), (b) and (d) only",
          ["(a), (c) and (d) only", "(b), (d) and (e) only", "(a), (b), (d) and (e) only"], "A"),
    "Reflection of waves and stationary waves",
    "At a rigid boundary the displacement must stay zero, so the reflected wave is inverted (phase change π); at an "
    "open boundary there is no phase change. Superposing incident and reflected waves gives y = 2a sin kx cos ωt, "
    "whose amplitude 2a sin kx varies from zero at nodes to 2a at antinodes.",
    ["(a) True: rigid boundary → phase change π", "(b) True: sin kx = 0 at nodes for all t",
     "(c) False: free boundary → no phase change", "(d) True: definition of a stationary wave",
     "(e) False: amplitude 2a sin kx depends on position"],
    why="Options with (c) or (e) include a false statement; (a), (b) and (d) are all true.",
    ncert="Class 11 Physics, 'Waves', reflection of waves and standing waves", seconds=70)


# =====================================================================================================================
# Electrostatics (B5 I7 A5)
# =====================================================================================================================
T = "Electrostatics"
k_e = 9e9
eps0 = 8.85e-12

n_el = 1.6e-6 / 1.6e-19
assert close(n_el, 1e13) and close(1 / 1.6e-19 * 1.6, 1e19) and close(1.6e-9 / 1.6e-19, 1e10)
assert close(1.6e-3 / 1.6e-19, 1e16)
add(T, "Coulomb's law and superposition", "Basic", "numerical",
    "A metal sphere carries a charge of −1.6 μC. Taking the magnitude of the electronic charge as 1.6 × 10⁻¹⁹ C, "
    "the number of excess electrons on the sphere is:",
    place("10¹³", ["10¹⁹", "10¹⁰", "10¹⁶"], "B"),
    "Quantisation of charge: q = ne",
    "Every charge is an integral multiple of e, so the number of excess electrons is n = |q|/e.",
    ["|q| = 1.6 μC = 1.6 × 10⁻⁶ C", "n = 1.6 × 10⁻⁶/1.6 × 10⁻¹⁹ = 10¹³"],
    why="10¹⁹ is the number of electrons in 1.6 C (μ ignored). 10¹⁰ takes μ as 10⁻⁹ (nano). 10¹⁶ takes μ as 10⁻³ "
        "(milli).",
    ncert="Class 12 Physics, 'Electric Charges and Fields', quantisation of charge", seconds=30, recomputed=True)

add(T, "Coulomb's law and superposition", "Basic", "multi_statement",
    multi("Which of the following statements about electric charge are correct?",
          ["The total charge of an isolated system remains constant.",
           "When a glass rod is rubbed with silk, the glass rod acquires a negative charge.",
           "Charging by rubbing transfers electrons from one body to the other.",
           "Like charges attract each other.",
           "The electrostatic force between two point charges depends on the medium between them."]),
    place("(a), (c) and (e) only",
          ["(a), (b) and (c) only", "(c), (d) and (e) only", "(a), (b), (c) and (e) only"], "D"),
    "Basic properties of electric charge",
    "Charge is conserved. Rubbing transfers electrons: silk takes electrons from glass, leaving the glass rod "
    "positive. Like charges repel. In a medium of dielectric constant K the Coulomb force is reduced by the factor K.",
    ["(a) True: conservation of charge", "(b) False: the glass rod becomes positive (the silk negative)",
     "(c) True: electrons are transferred", "(d) False: like charges repel",
     "(e) True: F = q₁q₂/(4πε₀Kr²) in a medium"],
    why="Options with (b) or (d) include a false statement; (a), (c) and (e) are all true.",
    ncert="Class 12 Physics, 'Electric Charges and Fields', electric charge, basic properties of electric charge",
    seconds=45)

C_pp = eps0 * 0.02 / 0.885e-3
assert close(C_pp, 2e-10) and close(eps0 * 0.02 / 0.885, 2e-13) and close(eps0 * 0.02 / 0.0885e-3, 2e-9)
add(T, "Capacitors and dielectrics", "Basic", "numerical",
    "A parallel plate capacitor has plates of area 0.02 m² separated by 0.885 mm of air. Taking "
    "ε₀ = 8.85 × 10⁻¹² C² N⁻¹ m⁻², its capacitance is:",
    place("200 pF", ["0.2 pF", "2000 pF", "100 pF"], "B"),
    "Capacitance of a parallel plate capacitor: C = ε₀A/d",
    "Use SI units throughout: d = 0.885 mm = 0.885 × 10⁻³ m.",
    ["C = 8.85 × 10⁻¹² × 0.02/(0.885 × 10⁻³)", "= 2 × 10⁻¹⁰ F = 200 pF"],
    why="0.2 pF leaves d in millimetres. 2000 pF slips a power of ten in d (0.0885 mm). 100 pF uses ε₀A/2d.",
    ncert="Class 12 Physics, 'Electrostatic Potential and Capacitance', the parallel plate capacitor", seconds=40,
    recomputed=True)

add(T, "Gauss's law", "Basic", "direct",
    "A point charge sits at the centre of a spherical Gaussian surface. If the radius of the surface is doubled, "
    "the total electric flux through it:",
    place("Remains the same", ["Becomes half", "Becomes one-fourth", "Becomes four times"], "C"),
    "Gauss's law: Φ = q_enclosed/ε₀",
    "The total flux through a closed surface depends only on the charge enclosed. Doubling the radius makes the field "
    "four times weaker but the area four times larger, so the flux is unchanged.",
    ["Φ = q/ε₀, independent of the radius", "Check: E ∝ 1/r², area ∝ r² → E × area unchanged"],
    why="Halving or quartering the flux comes from looking at the field alone; four times comes from looking at the "
        "area alone. The two effects cancel exactly.",
    ncert="Class 12 Physics, 'Electric Charges and Fields', Gauss's law", seconds=25)

add(T, "Electric potential and energy", "Basic", "statement_pair",
    SP_STEM.format(
        s1="Electric potential is a scalar quantity.",
        s2="In electrostatics, the electric field inside the material of a conductor is zero."),
    sp("A"),
    "Potential as a scalar; field inside a conductor",
    "Potential is work done per unit charge, a scalar, so potentials due to several charges add algebraically. In a "
    "conductor in electrostatic equilibrium, free electrons move until the field inside the material is zero.",
    ["Statement I: V = W/q is a scalar → true", "Statement II: E = 0 inside the conductor in the static situation → true"],
    why="Both statements are true NCERT results.",
    ncert="Class 12 Physics, 'Electrostatic Potential and Capacitance', electrostatic potential and electrostatics "
          "of conductors", seconds=30)

F1 = k_e * (1e-6) ** 2 / 0.3 ** 2
F_res = 2 * F1 * math.cos(math.radians(30))
assert close(F1, 0.1) and close(F_res, 0.1 * math.sqrt(3)) and close(2 * F1 * math.cos(math.radians(60)), 0.1)
add(T, "Coulomb's law and superposition", "Intermediate", "numerical",
    "Three point charges, each of +1 μC, are placed at the corners of an equilateral triangle of side 30 cm in air. "
    "Taking 1/(4πε₀) = 9 × 10⁹ N m² C⁻², the magnitude of the net electrostatic force on any one of the charges is:",
    place("0.1√3 N", ["0.2 N", "0.1 N", "0.1√2 N"], "A"),
    "Superposition of Coulomb forces",
    "Each of the other two charges repels the chosen charge with the same force F, and the two forces make 60° with "
    "each other. Their resultant is 2F cos 30° = √3 F.",
    ["F = 9 × 10⁹ × (10⁻⁶)²/(0.3)² = 0.1 N", "Angle between the two forces = 60°",
     "F_net = √(F² + F² + 2F² cos 60°) = √3 F = 0.1√3 N ≈ 0.17 N"],
    why="0.2 N adds the magnitudes as if the forces were parallel. 0.1 N uses 2F cos 60° (the wrong half-angle). "
        "0.1√2 N treats the forces as perpendicular.",
    ncert="Class 12 Physics, 'Electric Charges and Fields', forces between multiple charges", seconds=60,
    recomputed=True)

tau_d = 4e-9 * 5e4 * math.sin(math.radians(30))
assert close(tau_d, 1e-4) and close(4e-9 * 5e4 * math.cos(math.radians(30)), 1.732e-4) and close(4e-9 * 5e4, 2e-4)
add(T, "Electric field and dipole", "Intermediate", "numerical",
    "An electric dipole of dipole moment 4 × 10⁻⁹ C m is placed in a uniform electric field of 5 × 10⁴ N/C, with its "
    "axis at 30° to the field. The magnitude of the torque on the dipole is:",
    place("1 × 10⁻⁴ N m", ["1.73 × 10⁻⁴ N m", "2 × 10⁻⁴ N m", "Zero"], "B"),
    "Torque on a dipole in a uniform field: τ = pE sin θ",
    "In a uniform field the forces on the two charges are equal and opposite (net force zero), but they form a couple "
    "whose torque is p × E.",
    ["τ = pE sin θ = 4 × 10⁻⁹ × 5 × 10⁴ × sin 30°", "= 2 × 10⁻⁴ × 0.5 = 1 × 10⁻⁴ N m"],
    why="1.73 × 10⁻⁴ N m uses cos 30°. 2 × 10⁻⁴ N m leaves out sin θ. Zero confuses the zero net force with zero "
        "torque.",
    ncert="Class 12 Physics, 'Electric Charges and Fields', dipole in a uniform external field", seconds=40,
    recomputed=True)

V_c = k_e * (1 + 2 - 3 + 4) * 1e-9 / 1.0
assert close(V_c, 36) and close(k_e * 10e-9, 90) and close(V_c / math.sqrt(2), 25.46)
add(T, "Electric potential and energy", "Intermediate", "numerical",
    "Point charges of +1 nC, +2 nC, −3 nC and +4 nC are placed at the four corners of a square of side √2 m. Taking "
    "1/(4πε₀) = 9 × 10⁹ N m² C⁻², the electric potential at the centre of the square is:",
    place("36 V", ["90 V", "0 V", "25.5 V"], "C"),
    "Potential due to a system of point charges",
    "Potential is a scalar, so the potentials of the four charges add algebraically. Each corner is at a distance of "
    "half the diagonal from the centre: (√2 × √2)/2 = 1 m.",
    ["Distance of each corner from the centre = 1 m", "Σq = 1 + 2 − 3 + 4 = 4 nC",
     "V = 9 × 10⁹ × 4 × 10⁻⁹/1 = 36 V"],
    why="90 V adds the magnitudes of the charges, ignoring the sign of −3 nC. 0 V assumes the potentials cancel by "
        "symmetry, which needs equal and opposite charge pairs. 25.5 V uses the side (√2 m) as the distance.",
    ncert="Class 12 Physics, 'Electrostatic Potential and Capacitance', potential due to a system of charges",
    seconds=50, recomputed=True)

U0 = 0.5 * 4e-6 * 50 ** 2
assert close(U0, 5e-3) and close(U0 / 5, 1e-3) and close(U0 * 5, 25e-3) and close(U0 / 25, 0.2e-3)
add(T, "Capacitors and dielectrics", "Intermediate", "numerical",
    "A 4 μF air-filled capacitor is charged to 50 V and then disconnected from the battery. A dielectric slab of "
    "dielectric constant 5 is then inserted to fill the space between its plates completely. The energy stored in "
    "the capacitor now is:",
    place("1 mJ", ["25 mJ", "5 mJ", "0.2 mJ"], "D"),
    "Energy of an isolated capacitor when a dielectric is inserted",
    "Once disconnected, the charge Q stays fixed. The dielectric multiplies C by K, so U = Q²/2C is divided by K.",
    ["U₀ = ½CV² = ½ × 4 × 10⁻⁶ × 2500 = 5 × 10⁻³ J = 5 mJ", "Q fixed, C → 5C → U = U₀/5 = 1 mJ"],
    why="25 mJ (U₀ × K) is the result when the battery stays connected (V fixed). 5 mJ ignores the dielectric. "
        "0.2 mJ divides by K².",
    ncert="Class 12 Physics, 'Electrostatic Potential and Capacitance', effect of dielectric on capacitance; energy "
          "stored in a capacitor", seconds=60, recomputed=True)

add(T, "Gauss's law", "Intermediate", "assertion_reason",
    AR_STEM.format(
        a="Sensitive instruments can be protected from external electric fields by enclosing them in a closed metal "
          "box.",
        r="The electric field inside a cavity in a conductor is zero when there is no charge inside the cavity, "
          "whatever the charges and fields outside the conductor."),
    ar("A"),
    "Electrostatic shielding",
    "NCERT shows (using Gauss's law and the zero field in a conductor) that a charge-free cavity inside a conductor "
    "has zero field, whatever the external charges. A closed metal box is such a cavity, so an instrument inside is "
    "shielded.",
    ["R: field in a charge-free cavity of a conductor = 0 → true", "A: the box acts as the conductor around the cavity → true",
     "R explains A → option A"],
    why="Both are true and R is the principle on which the shielding in A works.",
    ncert="Class 12 Physics, 'Electrostatic Potential and Capacitance', electrostatics of conductors (electrostatic "
          "shielding)", seconds=40)

add(T, "Electric field and dipole", "Intermediate", "match_list",
    match_stem("For a short electric dipole of dipole moment p, match List-I (quantity) with List-II (its "
               "magnitude). Here k = 1/(4πε₀) and r is the distance from the centre of the dipole (r much larger "
               "than the dipole length).",
               ["Electric field at a point on the axial line", "Electric field at a point on the equatorial line",
                "Electric potential at a point on the equatorial line",
                "Torque on the dipole in a uniform field E, its axis making angle θ with the field"],
               ["Zero", "pE sin θ", "2kp/r³", "kp/r³"]),
    match_options({"A": "III", "B": "IV", "C": "I", "D": "II"},
                  [{"A": "IV", "B": "III", "C": "I", "D": "II"}, {"A": "III", "B": "I", "C": "IV", "D": "II"},
                   {"A": "III", "B": "IV", "C": "II", "D": "I"}], "D"),
    "Field, potential and torque of a dipole",
    "On the axial line E = 2kp/r³; on the equatorial line E = kp/r³ (directed opposite to p). The equatorial plane is "
    "equidistant from +q and −q, so the potential there is zero. In a uniform field τ = pE sin θ.",
    ["A → 2kp/r³ (III)", "B → kp/r³ (IV)", "C → 0 (I)", "D → pE sin θ (II)"],
    why="The other codes swap the axial and equatorial fields (they differ by a factor 2), or give the equatorial "
        "point a non-zero potential because its field is non-zero.",
    ncert="Class 12 Physics, 'Electric Charges and Fields' and 'Electrostatic Potential and Capacitance', electric "
          "dipole", seconds=50)

add(T, "Capacitors and dielectrics", "Intermediate", "multi_statement",
    multi("Which of the following statements about capacitors are correct?",
          ["Inserting a dielectric slab between the plates of a parallel plate capacitor increases its capacitance.",
           "The energy stored in a capacitor with charge Q and potential difference V is QV/2.",
           "Capacitors connected in series all carry the same charge.",
           "Capacitors connected in parallel have different potential differences across them.",
           "The equivalent capacitance of capacitors in series is greater than the largest individual "
           "capacitance."]),
    place("(a), (b) and (c) only",
          ["(a), (b) and (d) only", "(a), (c) and (e) only", "(a), (b), (c) and (e) only"], "C"),
    "Capacitors: dielectrics, energy and combinations",
    "A dielectric raises C by the factor K. U = ½QV = Q²/2C = ½CV². In series the same charge flows onto each "
    "capacitor and 1/C = Σ1/Cᵢ, which is smaller than the smallest Cᵢ. In parallel, all capacitors share the same "
    "potential difference.",
    ["(a) True: C = Kε₀A/d", "(b) True: U = ½QV", "(c) True: same charge in series",
     "(d) False: same p.d. in parallel", "(e) False: series C is less than the smallest capacitance"],
    why="Options with (d) or (e) include a false statement; (a), (b) and (c) are all true.",
    ncert="Class 12 Physics, 'Electrostatic Potential and Capacitance', combination of capacitors and energy stored",
    seconds=60)

C_half = F(1, 2) * 1 + F(1, 2) * 4
assert C_half == F(5, 2) and F(2 * 4, 4 + 1) == F(8, 5)
add(T, "Capacitors and dielectrics", "Advanced", "numerical",
    "A parallel plate capacitor has capacitance C₀ with air between its plates. A dielectric slab of dielectric "
    "constant 4, whose thickness equals the plate separation, is inserted so that it fills exactly half the area "
    "between the plates. The new capacitance is:",
    place("2.5C₀", ["1.6C₀", "4C₀", "5C₀"], "D"),
    "Dielectric filling part of the area: capacitors in parallel",
    "The two halves have the same plate separation and the same potential difference, so they act as two capacitors "
    "in parallel, each of area A/2.",
    ["Air half: ε₀(A/2)/d = C₀/2", "Dielectric half: 4ε₀(A/2)/d = 2C₀", "C = C₀/2 + 2C₀ = 2.5C₀"],
    why="1.6C₀ is the result for a slab of half the thickness over the full area (series combination). 4C₀ takes the "
        "slab to fill the whole space. 5C₀ adds C₀ and 4C₀ without halving the areas.",
    ncert="Class 12 Physics, 'Electrostatic Potential and Capacitance', effect of dielectric on capacitance",
    seconds=70, recomputed=True)

V_mid = 2 * k_e * 2e-6 / 0.1
W_mid = 1e-6 * V_mid
assert close(V_mid, 3.6e5) and close(W_mid, 0.36) and close(W_mid / 2, 0.18) and close(1e-6 * 2 * k_e * 2e-6 / 0.05, 0.72)
add(T, "Electric potential and energy", "Advanced", "numerical",
    "Two point charges, each of +2 μC, are held fixed 20 cm apart in air. Taking 1/(4πε₀) = 9 × 10⁹ N m² C⁻², the "
    "work needed to bring a charge of +1 μC slowly from infinity to the midpoint of the line joining them is:",
    place("0.36 J", ["0 J", "0.18 J", "0.72 J"], "A"),
    "Work = charge × potential difference",
    "The work done by an external agent in bringing a charge slowly from infinity is qV, where V is the potential at "
    "the final point. At the midpoint the fields cancel, but the potentials of the two positive charges add.",
    ["Distance of the midpoint from each charge = 0.1 m",
     "V = 2 × 9 × 10⁹ × 2 × 10⁻⁶/0.1 = 3.6 × 10⁵ V", "W = qV = 10⁻⁶ × 3.6 × 10⁵ = 0.36 J"],
    why="0 J confuses zero field at the midpoint with zero potential; work depends on potential. 0.18 J counts only "
        "one of the two charges. 0.72 J uses 5 cm instead of 10 cm as the distance.",
    ncert="Class 12 Physics, 'Electrostatic Potential and Capacitance', potential due to a system of charges",
    seconds=60, recomputed=True)

sig = 8.85e-8
E_between = (2 * sig + sig) / (2 * eps0)
assert close(E_between, 1.5e4) and close((2 * sig - sig) / (2 * eps0), 5e3) and close(sig / eps0, 1e4)
assert close(3 * sig / eps0, 3e4)
add(T, "Gauss's law", "Advanced", "numerical",
    "Two large, thin, parallel plane sheets of charge carry uniform surface charge densities +2σ and −σ, where "
    "σ = 8.85 × 10⁻⁸ C/m². Taking ε₀ = 8.85 × 10⁻¹² C² N⁻¹ m⁻², the magnitude of the electric field in the region "
    "between the sheets (away from their edges) is:",
    place("1.5 × 10⁴ N/C", ["5 × 10³ N/C", "1 × 10⁴ N/C", "3 × 10⁴ N/C"], "B"),
    "Field of an infinite sheet and superposition",
    "Each sheet produces a uniform field of magnitude |σᵢ|/2ε₀, directed away from a positive sheet and towards a "
    "negative one. Between the sheets both fields point from the +2σ sheet towards the −σ sheet, so they add.",
    ["Field of the +2σ sheet = 2σ/2ε₀ = σ/ε₀; field of the −σ sheet = σ/2ε₀",
     "Between the sheets they are in the same direction: E = σ/ε₀ + σ/2ε₀ = 3σ/2ε₀",
     "σ/ε₀ = 8.85 × 10⁻⁸/8.85 × 10⁻¹² = 10⁴ N/C → E = 1.5 × 10⁴ N/C"],
    why="5 × 10³ N/C subtracts the two fields; that is the field outside the sheets. 1 × 10⁴ N/C uses the capacitor "
        "result σ/ε₀, which holds only for equal and opposite densities. 3 × 10⁴ N/C forgets the factor 2 in σ/2ε₀.",
    ncert="Class 12 Physics, 'Electric Charges and Fields', applications of Gauss's law (field due to a uniformly "
          "charged infinite plane sheet)", seconds=90, recomputed=True)

q_small = F(8) * 1 / (1 + 3)
q_large = F(8) - q_small
sig_ratio = (q_small / 1 ** 2) / (q_large / 3 ** 2)
assert q_small == 2 and q_large == 6 and sig_ratio == 3 and q_small / 1 == q_large / 3
add(T, "Electric potential and energy", "Advanced", "numerical",
    "Two isolated conducting spheres of radii 1 cm and 3 cm, far apart from each other, are connected by a thin "
    "conducting wire. A total charge of 8 μC is shared between them. The charge on the smaller sphere and the ratio "
    "of the surface charge density on the smaller sphere to that on the larger sphere are:",
    place("2 μC; 3 : 1", ["6 μC; 1 : 3", "2 μC; 1 : 3", "4 μC; 1 : 1"], "C"),
    "Charge sharing between connected conductors",
    "Connected conductors reach the same potential. For a sphere V = kq/r, so the charges are in the ratio of the "
    "radii, and the surface charge density σ = q/4πr² is inversely proportional to the radius.",
    ["kq₁/r₁ = kq₂/r₂ → q₁ : q₂ = 1 : 3 → q₁ = 2 μC, q₂ = 6 μC",
     "σ₁/σ₂ = (q₁/r₁²)/(q₂/r₂²) = (2/1)/(6/9) = 3", "σ₁ : σ₂ = 3 : 1"],
    why="6 μC; 1 : 3 gives the larger sphere's charge and inverts the density ratio. 2 μC; 1 : 3 has the right charge "
        "but takes σ ∝ r. 4 μC; 1 : 1 shares the charge equally.",
    shortcut="σ ∝ 1/r for connected spheres; this is why charge density is high at sharp points.",
    ncert="Class 12 Physics, 'Electrostatic Potential and Capacitance', electrostatics of conductors", seconds=80,
    recomputed=True)

add(T, "Capacitors and dielectrics", "Advanced", "statement_pair",
    SP_STEM.format(
        s1="If the plate separation of a parallel plate capacitor that stays connected to a battery is doubled, the "
           "energy stored in it doubles.",
        s2="If the plate separation of a charged parallel plate capacitor that has been disconnected from the "
           "battery is doubled, the energy stored in it doubles."),
    sp("D"),
    "Energy of a capacitor at fixed V and at fixed Q",
    "Doubling d halves C = ε₀A/d. Connected to a battery, V is fixed and U = ½CV² halves. Disconnected, Q is fixed "
    "and U = Q²/2C doubles; the extra energy comes from the work done in pulling the plates apart.",
    ["Statement I: V fixed, C halves → U = ½CV² halves → false",
     "Statement II: Q fixed, C halves → U = Q²/2C doubles → true"],
    why="Statement I uses the fixed-charge result for a capacitor whose voltage, not charge, is held fixed.",
    ncert="Class 12 Physics, 'Electrostatic Potential and Capacitance', energy stored in a capacitor", seconds=60)


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
    doc = {"schema_version": "1.0", "batch_id": "BATCH_002", "created_at": TODAY,
           "notes": "BATCH_002 package PHY_002_p1: 128 original Physics questions (Physics and Measurement through "
                    "Electrostatics). Every numerical answer is re-derived in tools/batch_002/PHY_002_p1.py.",
           "stimuli": [], "questions": QUESTIONS}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {OUT}: {n} questions, {dict(Counter(x['difficulty'] for x in QUESTIONS))}")
    print(f"keys {dict(sorted(keys.items()))}")
    print(f"formats {dict(fmts)}")
