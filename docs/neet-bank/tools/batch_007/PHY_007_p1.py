"""Writes batches/parts/BATCH_007_PHY_p1.json: package PHY_007_p1 of BATCH_007 (129 Physics questions).

Topics: Physics and Measurement, Kinematics, Laws of Motion, Work Energy and Power, Rotational Motion, Gravitation,
Properties of Solids and Liquids, Thermodynamics, Kinetic Theory of Gases, Oscillations and Waves, Electrostatics.
IDs NEET_PHY_001501 .. NEET_PHY_001629, in the order the questions are listed below.

Every computable answer is re-derived with an assert before the file is written, and so is the plan quota. If any
assert fails, nothing is written. Each question's answer position is chosen by hand and fixed.

    python tools/batch_007/PHY_007_p1.py        (run from docs/neet-bank)
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
OUT = ROOT / "batches" / "parts" / "BATCH_007_PHY_p1.json"
PLAN = ROOT / "batches" / "plans" / "BATCH_007_plan.json"
PACKAGE = "PHY_007_p1"
TODAY = "2026-11-16"
LETTERS = "ABCD"
PHY = "Physics"
RECOMPUTED = ("script:recompute", "ai:author-solve", "ai:self-recheck")
AUTHORED = ("ai:author-solve", "ai:self-recheck")
FIRST_ID = 1501

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
# Physics and Measurement (B2 I3 A2)
# =====================================================================================================================
T = "Physics and Measurement"

rho_cgs = 13.6                                   # g cm^-3
rho_si = rho_cgs * 1e-3 / 1e-6                   # g -> kg, cm^3 -> m^3
assert close(rho_si, 1.36e4)
assert close(rho_cgs * 1e-3 / 1e-2, 1.36)        # cm^3 converted as if 1 cm^3 = 10^-2 m^3
assert close(rho_cgs * 1e-3 * 1e-6, 1.36e-8)     # multiplies by 10^-6 instead of dividing
assert close(rho_cgs / 1e-6, 1.36e7)             # converts cm^3 but forgets g -> kg
add(T, "Units and SI system", "Basic", "numerical",
    "The density of mercury is 13.6 g cm⁻³. Its density in SI units is:",
    place("1.36 × 10⁴ kg m⁻³", ["1.36 kg m⁻³", "1.36 × 10⁻⁸ kg m⁻³", "1.36 × 10⁷ kg m⁻³"], "B"),
    "Conversion of a derived unit from CGS to SI",
    "Convert each unit separately: 1 g = 10⁻³ kg and 1 cm³ = (10⁻² m)³ = 10⁻⁶ m³. Dividing a mass in kg by a "
    "volume in m³ gives the density in kg m⁻³.",
    ["13.6 g cm⁻³ = 13.6 × 10⁻³ kg / 10⁻⁶ m³", "= 13.6 × 10³ kg m⁻³ = 1.36 × 10⁴ kg m⁻³"],
    shortcut="1 g cm⁻³ = 1000 kg m⁻³, so multiply by 1000.",
    why="1.36 kg m⁻³ converts cm³ as if 1 cm³ were 10⁻² m³ (cubing forgotten). 1.36 × 10⁻⁸ multiplies by 10⁻⁶ "
        "instead of dividing by it. 1.36 × 10⁷ converts the volume but leaves the mass in grams.",
    ncert="Class 11 Physics, 'Units and Measurement', the international system of units", seconds=35,
    recomputed=True)

D_alpha = dims(k=-1)                                       # ΔL/(LΔT)
D_K = dmul(dims(1, 2, -3), dims(l=-1), dims(k=-1))         # H L /(A ΔT): [M L² T⁻³][L]/([L²][K])
D_L = dims(0, 2, -2)                                       # Q/m
D_kB = dmul(dims(1, 2, -2), dims(k=-1))                    # energy / temperature
assert D_K == (1, 1, -3, -1) and D_alpha == (0, 0, 0, -1) and D_L == (0, 2, -2, 0) and D_kB == (1, 2, -2, -1)
add(T, "Dimensional analysis", "Basic", "match_list",
    match_stem("Match List-I (physical quantity) with List-II (its dimensional formula). K denotes the dimension of "
               "temperature.",
               ["Coefficient of linear expansion", "Thermal conductivity", "Latent heat (specific latent heat)",
                "Boltzmann constant"],
               ["[M L² T⁻² K⁻¹]", "[K⁻¹]", "[L² T⁻²]", "[M L T⁻³ K⁻¹]"]),
    match_options({"A": "II", "B": "IV", "C": "III", "D": "I"},
                  [{"A": "II", "B": "I", "C": "III", "D": "IV"}, {"A": "III", "B": "IV", "C": "II", "D": "I"},
                   {"A": "II", "B": "IV", "C": "I", "D": "III"}], "C"),
    "Dimensional formulae of thermal quantities",
    "Each dimensional formula follows from a defining relation: α = ΔL/(L ΔT), H = KA ΔT/L for conduction, "
    "Q = mL for latent heat, and the average energy per degree of freedom ½k_BT, which makes k_B an energy per unit "
    "temperature.",
    ["α = ΔL/(L ΔT) → [K⁻¹] (II)", "K = H L/(A ΔT) = [M L² T⁻³][L]/([L²][K]) = [M L T⁻³ K⁻¹] (IV)",
     "L = Q/m = [M L² T⁻²]/[M] = [L² T⁻²] (III)", "k_B = energy/temperature = [M L² T⁻² K⁻¹] (I)"],
    why="The other codes swap thermal conductivity with the Boltzmann constant (both contain K⁻¹), or give latent "
        "heat the dimensions of a quantity per kelvin.",
    ncert="Class 11 Physics, 'Units and Measurement', dimensions of physical quantities; 'Thermal Properties of "
          "Matter' (defining relations)", seconds=60, recomputed=True)

# v_c = eta^x rho^y r^z : [L T^-1] = [M L^-1 T^-1]^x [M L^-3]^y [L]^z
x_, y_, z_ = 1, -1, -1
D_eta, D_rho, D_r = dims(1, -1, -1), dims(1, -3, 0), dims(0, 1, 0)
assert dmul(dpow(D_eta, x_), dpow(D_rho, y_), dpow(D_r, z_)) == dims(0, 1, -1)
assert dmul(dpow(D_eta, 1), dpow(D_rho, 1), dpow(D_r, -1)) != dims(0, 1, -1)
assert dmul(dpow(D_eta, -1), dpow(D_rho, 1), dpow(D_r, 1)) != dims(0, 1, -1)
assert dmul(dpow(D_eta, 1), dpow(D_rho, -1), dpow(D_r, 1)) != dims(0, 1, -1)
add(T, "Dimensional analysis", "Intermediate", "numerical",
    "The critical velocity v_c of a liquid flowing through a tube is found to depend only on the coefficient of "
    "viscosity η of the liquid, its density ρ and the radius r of the tube, as v_c ∝ ηˣ ρʸ rᶻ. By dimensional "
    "analysis, the values of x, y and z are:",
    place("x = 1, y = −1, z = −1", ["x = 1, y = 1, z = −1", "x = −1, y = 1, z = 1", "x = 1, y = −1, z = 1"], "D"),
    "Finding exponents by equating dimensions",
    "Write [η] = [M L⁻¹ T⁻¹], [ρ] = [M L⁻³] and [r] = [L], and equate the powers of M, L and T on both sides of "
    "[L T⁻¹] = [M L⁻¹ T⁻¹]ˣ [M L⁻³]ʸ [L]ᶻ.",
    ["T: −x = −1 → x = 1", "M: x + y = 0 → y = −1", "L: −x − 3y + z = 1 → −1 + 3 + z = 1 → z = −1",
     "So v_c ∝ η/(ρr)"],
    why="(1, 1, −1) gives [M² L⁻⁵ T⁻¹], with an uncancelled power of mass. (−1, 1, 1) is the reciprocal "
        "combination, with dimensions [L⁻¹ T]. (1, −1, 1) gives [L³ T⁻¹], not [L T⁻¹].",
    ncert="Class 11 Physics, 'Units and Measurement', dimensional analysis and its applications", seconds=75,
    recomputed=True)

assert close(0.1 / 50 * 100, 0.2) and close(0.1 / 5 * 100, 2.0)
add(T, "Least count and significant figures", "Intermediate", "statement_pair",
    SP_STEM.format(
        s1="Using a measuring instrument of smaller least count always removes the systematic errors from a "
           "measurement.",
        s2="When lengths are measured with a metre scale of least count 1 mm, the percentage error due to the least "
           "count is smaller for a length of 50 cm than for a length of 5 cm."),
    sp("D"),
    "Least count, precision and systematic error",
    "A smaller least count improves the precision (resolution) of a reading, but a systematic error such as a zero "
    "error, a faulty calibration or a poor technique remains whatever the least count. The uncertainty set by the "
    "least count is a fixed absolute amount, so it is a smaller fraction of a larger measured length.",
    ["Statement I: zero error or faulty technique persists with a finer scale → false",
     "Statement II: 0.1 cm/50 cm = 0.2% while 0.1 cm/5 cm = 2% → true"],
    why="Statement I confuses precision with accuracy: a finer instrument can still give consistently wrong "
        "readings. So A, B and C are wrong.",
    ncert="Class 11 Physics, 'Units and Measurement', accuracy and precision of instruments, errors in measurement",
    seconds=50)

add(T, "Errors in measurement", "Intermediate", "multi_statement",
    multi("Which of the following statements about errors in measurement are correct?",
          ["The absolute error in a measurement has the same unit as the measured quantity.",
           "The relative error of a measurement is a pure number, without units.",
           "The percentage error is the relative error multiplied by 100.",
           "The mean absolute error of a set of readings can be negative.",
           "If a quantity A has a relative error δ, the relative error in Aⁿ is nδ."]),
    place("(a), (b), (c) and (e) only", ["(a), (b) and (d) only", "(b), (c), (d) and (e) only",
                                         "(a), (c) and (d) only"], "A"),
    "Absolute, relative and percentage errors",
    "The absolute error is a difference of two values of the quantity, so it carries the quantity's unit. Dividing "
    "it by the mean value gives the relative error, a pure number; times 100 it is the percentage error. The mean "
    "absolute error is the mean of the magnitudes |Δaᵢ|, so it cannot be negative. For a power Aⁿ the relative "
    "error is multiplied by n.",
    ["(a) true", "(b) true", "(c) true", "(d) false: it averages magnitudes, so it is never negative",
     "(e) true: ΔZ/Z = n ΔA/A for Z = Aⁿ"],
    why="Any option that includes (d) is wrong, and (b), (c), (d), (e) also leaves out the true statement (a).",
    ncert="Class 11 Physics, 'Units and Measurement', errors in measurement and combination of errors", seconds=60)

D_P = dims(1, -1, -2)
D_V = dims(0, 3, 0)
D_a = dmul(D_P, dpow(D_V, 2))
D_b = D_V
assert D_a == (1, 5, -2, 0) and dmul(D_a, dinv(D_b)) == (1, 2, -2, 0) and dmul(D_a, D_b) == (1, 8, -2, 0)
add(T, "Dimensional analysis", "Advanced", "direct",
    "The van der Waals equation for one mole of a real gas is (P + a/V²)(V − b) = RT, where P is the pressure and V "
    "the volume of the gas. The quantity a/b has the dimensions of:",
    place("Energy, [M L² T⁻²]", ["Pressure, [M L⁻¹ T⁻²]", "[M L⁵ T⁻²]", "[M L⁸ T⁻²]"], "B"),
    "Principle of homogeneity applied to an equation of state",
    "Only quantities of the same dimensions can be added or subtracted. So a/V² has the dimensions of pressure and "
    "b has the dimensions of volume. Dividing [a] by [b] gives pressure × volume, which has the dimensions of "
    "energy.",
    ["[a/V²] = [P] → [a] = [M L⁻¹ T⁻²][L⁶] = [M L⁵ T⁻²]", "[b] = [V] = [L³]",
     "[a/b] = [M L⁵ T⁻²]/[L³] = [M L² T⁻²] (energy)"],
    why="Pressure is the dimension of a/V², not of a/b. [M L⁵ T⁻²] is the dimension of a alone. [M L⁸ T⁻²] is the "
        "dimension of the product ab.",
    ncert="Class 11 Physics, 'Units and Measurement', dimensional analysis (checking dimensional consistency)",
    seconds=75)

d_rel = 0.01 / 0.50
R_rel = 0.05 / 5.00
L_rel = 0.1 / 50.0
rho_err = (2 * d_rel + R_rel + L_rel) * 100
assert close(rho_err, 5.2)
assert close((d_rel + R_rel + L_rel) * 100, 3.2) and close((2 * d_rel + L_rel) * 100, 4.2)
assert close((R_rel + L_rel) * 100, 1.2)
add(T, "Errors in measurement", "Advanced", "numerical",
    "The resistivity of the material of a wire is found from ρ = πd²R/(4L). The diameter of the wire is measured as "
    "0.50 mm with an instrument of least count 0.01 mm, its length as 50.0 cm with a scale of least count 0.1 cm, "
    "and its resistance as (5.00 ± 0.05) Ω. Taking the least count as the absolute error of each length reading, "
    "the maximum percentage error in ρ is:",
    place("5.2%", ["3.2%", "4.2%", "1.2%"], "C"),
    "Combination of errors in a product, quotient and power",
    "For ρ = πd²R/(4L), the maximum relative error is 2(Δd/d) + ΔR/R + ΔL/L; π and 4 are exact numbers and add no "
    "error.",
    ["Δd/d = 0.01/0.50 = 2% → doubled for d²: 4%", "ΔR/R = 0.05/5.00 = 1%", "ΔL/L = 0.1/50.0 = 0.2%",
     "Maximum error in ρ = 4% + 1% + 0.2% = 5.2%"],
    why="3.2% forgets to double the error of d for d². 4.2% leaves out the error of the resistance. 1.2% ignores the "
        "diameter error altogether, though it is the largest contribution.",
    ncert="Class 11 Physics, 'Units and Measurement', combination of errors", seconds=90, recomputed=True)


# =====================================================================================================================
# Kinematics (B4 I5 A4)
# =====================================================================================================================
T = "Kinematics"

u1, u2, s1 = 10.0, 20.0, 10.0                    # 36 km/h and 72 km/h in m/s
a_stop = u1 ** 2 / (2 * s1)
s2 = u2 ** 2 / (2 * a_stop)
assert close(36 / 3.6, u1) and close(72 / 3.6, u2) and close(s2, 40) and close(s1 * math.sqrt(2) * 1, 14.142, 1e-3)
add(T, "Motion in a straight line", "Basic", "numerical",
    "A car moving at 36 km/h on a straight level road can be stopped within 10 m by applying its brakes. If the "
    "brakes produce the same uniform retardation, the least distance in which the car can be stopped when it is "
    "moving at 72 km/h is:",
    place("40 m", ["20 m", "80 m", "about 14 m"], "A"),
    "Stopping distance with uniform retardation",
    "From v² = u² − 2as with v = 0, the stopping distance is s = u²/(2a). For the same retardation it is "
    "proportional to the square of the initial speed.",
    ["s ∝ u² for a fixed retardation", "Speed doubles (36 → 72 km/h) → stopping distance × 4",
     "s = 4 × 10 m = 40 m"],
    shortcut="Double the speed, four times the stopping distance.",
    why="20 m takes the stopping distance as proportional to the speed. 80 m uses the cube or adds an extra factor "
        "of 2. About 14 m takes it as proportional to √u.",
    ncert="Class 11 Physics, 'Motion in a Straight Line', kinematic equations for uniformly accelerated motion "
          "(stopping distance)", seconds=40, recomputed=True)

lam = F(8 - 2, 2)                                 # 2*4 + lam*(-2) + 1*(-2) = 0
assert 2 * 4 + lam * (-2) + 1 * (-2) == 0 and lam == 3
assert 2 * 4 + 5 * (-2) + 1 * 2 == 0              # sign slip on the k term gives 5
assert 2 * 4 + 4 * (-2) == 0                      # k term dropped gives 4
add(T, "Vectors", "Basic", "numerical",
    "The vectors A = 2î + λĵ + k̂ and B = 4î − 2ĵ − 2k̂ are perpendicular to each other. The value of λ is:",
    place("3", ["−3", "5", "4"], "C"),
    "Scalar product of perpendicular vectors",
    "Two non-zero vectors are perpendicular when their scalar product is zero: AxBx + AyBy + AzBz = 0.",
    ["A · B = (2)(4) + (λ)(−2) + (1)(−2) = 6 − 2λ", "6 − 2λ = 0 → λ = 3"],
    why="−3 has a sign error in the ĵ term. 5 takes the k̂ product as +2 instead of −2. 4 leaves out the k̂ "
        "components.",
    ncert="Class 11 Physics, 'Work, Energy and Power', the scalar product", seconds=40,
    recomputed=True)

add(T, "Motion in a straight line", "Basic", "direct",
    "A particle moves along the x-axis. At a certain instant its velocity is in the negative x-direction and its "
    "acceleration is in the positive x-direction. At that instant the particle is:",
    place("Slowing down", ["Speeding up", "Moving in the positive x-direction", "Necessarily at rest"], "D"),
    "Sign of acceleration relative to velocity",
    "A particle speeds up when its acceleration is in the same direction as its velocity and slows down when the "
    "acceleration is opposite to the velocity. The sign of the acceleration alone does not decide this.",
    ["Velocity along −x, acceleration along +x → opposite directions", "Hence the speed is decreasing"],
    why="Speeding up needs acceleration along the velocity. The velocity is along −x, so it is not moving along +x, "
        "and with a non-zero velocity it is not at rest.",
    ncert="Class 11 Physics, 'Motion in a Straight Line', acceleration", seconds=30)

r_c, w_c = 2.0, 3.0
assert close(w_c * r_c, 6) and close(w_c ** 2 * r_c, 18) and close(2 * math.pi / w_c, 2.0944) \
    and close(w_c / (2 * math.pi), 0.47746)
add(T, "Uniform circular motion", "Basic", "match_list",
    match_stem("A particle moves uniformly along a circle of radius 2 m with an angular speed of 3 rad/s. Match "
               "List-I (quantity) with List-II (its value).",
               ["Linear speed", "Magnitude of the centripetal acceleration", "Time period", "Frequency"],
               ["18 m s⁻²", "3/(2π) Hz", "6 m s⁻¹", "2π/3 s"]),
    match_options({"A": "III", "B": "I", "C": "IV", "D": "II"},
                  [{"A": "I", "B": "III", "C": "IV", "D": "II"}, {"A": "III", "B": "I", "C": "II", "D": "IV"},
                   {"A": "IV", "B": "I", "C": "III", "D": "II"}], "B"),
    "Relations between linear and angular quantities in uniform circular motion",
    "v = ωR, a = ω²R = v²/R, T = 2π/ω and ν = 1/T = ω/(2π).",
    ["v = 3 × 2 = 6 m/s (III)", "a = 3² × 2 = 18 m/s² (I)", "T = 2π/3 s (IV)", "ν = 3/(2π) Hz (II)"],
    why="The other codes swap the speed with the acceleration, or the period with the frequency.",
    ncert="Class 11 Physics, 'Motion in a Plane', uniform circular motion", seconds=50, recomputed=True)

H_ = F(1)                                            # u^2/(2g) taken as 1 unit
h_half = (1 - F(1, 4)) * H_                          # (u^2 - u^2/4)/(2g)
assert h_half == F(3, 4)
add(T, "Motion in a straight line", "Intermediate", "numerical",
    "A ball thrown vertically upward with speed u reaches a maximum height H. Neglecting air resistance, the height "
    "at which its speed is u/2 while it is going up is:",
    place("3H/4", ["H/2", "H/4", "H/√2"], "C"),
    "Speed–height relation under gravity",
    "With v² = u² − 2gh, the maximum height is H = u²/(2g), and the height at any speed v is (u² − v²)/(2g).",
    ["H = u²/(2g)", "At v = u/2: h = (u² − u²/4)/(2g) = (3/4)(u²/2g) = 3H/4"],
    why="H/2 assumes the speed falls linearly with height. H/4 gives the height still to be climbed from that point, "
        "not the height reached. H/√2 has no basis in v² = u² − 2gh.",
    ncert="Class 11 Physics, 'Motion in a Straight Line', kinematic equations for uniformly accelerated motion",
    seconds=50, recomputed=True)

down_, up_ = 12 / 1, 12 / 2
river = (down_ - up_) / 2
assert river == 3 and (down_ + up_) / 2 == 9 and down_ - up_ == 6
add(T, "Relative velocity", "Intermediate", "numerical",
    "A motorboat covers 12 km downstream along a straight river in 1 hour and returns the same 12 km upstream in 2 "
    "hours. Its speed relative to the water is the same throughout. The speed of the river current is:",
    place("3 km/h", ["6 km/h", "9 km/h", "4.5 km/h"], "B"),
    "Relative velocity along a line",
    "Downstream the speeds add (boat + current); upstream they subtract (boat − current). Two equations give both "
    "speeds.",
    ["b + c = 12/1 = 12 km/h", "b − c = 12/2 = 6 km/h", "c = (12 − 6)/2 = 3 km/h (and b = 9 km/h)"],
    why="6 km/h is the difference of the two ground speeds, which is twice the current. 9 km/h is the boat's speed "
        "in still water. 4.5 km/h has no basis in the two equations.",
    ncert="Class 11 Physics, 'Motion in a Straight Line', relative velocity", seconds=50, recomputed=True)

Tf, Rg = 2.0, 40.0
uy = g * Tf / 2
ux = Rg / Tf
assert uy == 10 and ux == 20 and close(math.hypot(ux, uy), 10 * math.sqrt(5))
assert close(math.hypot(ux, g * Tf), 20 * math.sqrt(2))
add(T, "Projectile motion", "Intermediate", "numerical",
    "A ball projected from level ground lands back on the ground 2 s later, at a horizontal distance of 40 m from "
    "the point of projection. Taking g = 10 m/s² and neglecting air resistance, its speed of projection is:",
    place("10√5 m/s", ["30 m/s", "20 m/s", "20√2 m/s"], "D"),
    "Independent horizontal and vertical motions of a projectile",
    "The time of flight fixes the vertical component of the initial velocity, T = 2u_y/g, and the range fixes the "
    "constant horizontal component, R = u_x T.",
    ["u_y = gT/2 = 10 × 2/2 = 10 m/s", "u_x = R/T = 40/2 = 20 m/s", "u = √(20² + 10²) = √500 = 10√5 m/s"],
    why="30 m/s adds the components instead of combining them as vectors. 20 m/s is only the horizontal component. "
        "20√2 m/s uses T = u_y/g, which is only the time to reach the top.",
    ncert="Class 11 Physics, 'Motion in a Plane', projectile motion", seconds=60, recomputed=True)

add(T, "Graphs of motion", "Intermediate", "statement_pair",
    SP_STEM.format(
        s1="For a particle moving along a straight line with uniform acceleration, the velocity–time graph is a "
           "straight line inclined to the time axis.",
        s2="The position–time graph of a particle moving along a straight line can have a negative slope only if "
           "the acceleration of the particle is negative."),
    sp("C"),
    "Reading slopes of motion graphs",
    "With uniform acceleration, v = u + at is linear in t, so the v–t graph is a straight line of slope a. The slope "
    "of an x–t graph is the velocity, not the acceleration: a particle moving steadily in the −x direction has a "
    "negative x–t slope and zero acceleration.",
    ["Statement I: v = u + at is a straight line → true",
     "Statement II: negative x–t slope means negative velocity, which needs no particular sign of acceleration → "
     "false"],
    why="Statement II confuses velocity (slope of x–t) with acceleration (slope of v–t), so A, B and D are wrong.",
    ncert="Class 11 Physics, 'Motion in a Straight Line', instantaneous velocity and acceleration (graphs)",
    seconds=45)

add(T, "Projectile motion", "Intermediate", "assertion_reason",
    AR_STEM.format(
        a="For a projectile launched from level ground at an angle between 0° and 90° above the horizontal, with air "
          "resistance neglected, the speed is least at the highest point of the path.",
        r="At the highest point the vertical component of the velocity is zero, while the horizontal component has "
          "the same value as at every other point of the flight."),
    ar("A"),
    "Components of velocity in projectile motion",
    "The horizontal component u cos θ never changes, because the only acceleration is vertical. The speed is "
    "√(u²cos²θ + v_y²), which is least when v_y = 0, i.e. at the top of the path.",
    ["v_x = u cos θ at all times", "v_y = 0 only at the highest point", "Speed = √(v_x² + v_y²) is least there"],
    why="R gives exactly why the speed is least at the top, so B is wrong, and both statements are true, so C and "
        "D are wrong.",
    ncert="Class 11 Physics, 'Motion in a Plane', projectile motion", seconds=45)

aA, vB = 2.0, 10.0
t_eq = vB / aA
sep_max = vB * t_eq - 0.5 * aA * t_eq ** 2
t_over = 2 * vB / aA
assert t_eq == 5 and close(sep_max, 25) and t_over == 10 and close(0.5 * aA * t_over ** 2, 100)
add(T, "Relative velocity", "Advanced", "numerical",
    "Car A is at rest beside a straight road. At the instant car B passes it, moving at a constant 10 m/s, car A "
    "starts in the same direction with a uniform acceleration of 2 m/s² (the two cars are in adjacent lanes). The "
    "greatest distance between the cars before A overtakes B, and the time after which A overtakes B, are "
    "respectively:",
    place("25 m and 10 s", ["50 m and 10 s", "25 m and 5 s", "100 m and 10 s"], "B"),
    "Relative motion of two cars, one accelerating",
    "B pulls ahead while it is faster than A; the gap is largest when their velocities become equal, and A overtakes "
    "when both have covered the same distance.",
    ["Equal velocities: 2t = 10 → t = 5 s", "Gap then = 10 × 5 − ½ × 2 × 5² = 50 − 25 = 25 m",
     "Overtaking: t² = 10t → t = 10 s (both at 100 m)"],
    why="50 m is B's own distance at t = 5 s, not the gap. 25 m and 5 s gives the time of the largest gap instead "
        "of the overtaking time. 100 m is the distance from the start at which A overtakes.",
    ncert="Class 11 Physics, 'Motion in a Straight Line', relative velocity and kinematic equations", seconds=100,
    recomputed=True)

v_air, w_wind = 200.0, 100.0
phi = math.degrees(math.asin(w_wind / v_air))
v_ground = math.sqrt(v_air ** 2 - w_wind ** 2)
assert close(phi, 30) and close(v_ground, 100 * math.sqrt(3)) and close(math.hypot(v_air, w_wind), 100 * math.sqrt(5))
add(T, "Relative velocity", "Advanced", "numerical",
    "An aircraft flies at 200 km/h relative to the air. A steady wind blows towards the east at 100 km/h. The pilot "
    "wants the aircraft to travel due north over the ground. The direction in which the aircraft must head, and its "
    "speed relative to the ground, are:",
    place("30° west of north; 100√3 km/h", ["30° east of north; 100√3 km/h", "30° west of north; 100√5 km/h",
                                            "60° west of north; 100 km/h"], "C"),
    "Relative velocity in two dimensions",
    "Velocity over the ground = velocity relative to air + wind velocity. For the ground velocity to be due north, "
    "the aircraft's velocity relative to the air must have a westward component that cancels the 100 km/h wind.",
    ["200 sin φ = 100 → φ = 30° west of north", "Ground speed = 200 cos 30° = 100√3 ≈ 173 km/h"],
    why="Heading east of north would add to the wind's drift. 100√5 km/h adds the two speeds at right angles as if "
        "the wind were across a northward heading. 60° and 100 km/h interchange sine and cosine.",
    ncert="Class 11 Physics, 'Motion in a Plane', relative velocity in two dimensions", seconds=100, recomputed=True)

h1, h2 = 5.0, 20.0
u2sum = 2 * g * (h1 + h2)                         # u^2 = 2g(h1 + h2) for complementary angles
sin2 = h1 / (h1 + h2)
R_ = u2sum * 2 * math.sqrt(sin2 * (1 - sin2)) / g
assert close(R_, 40) and close(4 * math.sqrt(h1 * h2), 40)
add(T, "Projectile motion", "Advanced", "numerical",
    "Two balls are projected from the same point on level ground with the same speed, at two different angles, and "
    "land at the same point. Their maximum heights are 5 m and 20 m. Neglecting air resistance, their common "
    "horizontal range is:",
    place("40 m", ["20 m", "25 m", "100 m"], "D"),
    "Complementary angles of projection",
    "Equal ranges for the same speed need angles θ and 90° − θ. Then h₁ = u²sin²θ/(2g) and h₂ = u²cos²θ/(2g), so "
    "√(h₁h₂) = u² sin θ cos θ/(2g) = R/4.",
    ["R = u² sin 2θ/g = 2u² sin θ cos θ/g = 4√(h₁h₂)", "R = 4√(5 × 20) = 4 × 10 = 40 m",
     "Check: h₁ + h₂ = u²/(2g) = 25 m → u² = 500; sin²θ = 0.2 → R = 500 × 2 × √0.2 × √0.8/10 = 40 m"],
    shortcut="R = 4√(h₁h₂) for the two complementary angles.",
    why="20 m uses 2√(h₁h₂). 25 m adds the heights (that sum is u²/2g, not the range). 100 m multiplies the heights.",
    ncert="Class 11 Physics, 'Motion in a Plane', projectile motion", seconds=100, recomputed=True)

H0, ux0 = 20.0, 15.0
t0 = math.sqrt(2 * H0 / g)
vy0 = g * t0
assert t0 == 2 and ux0 * t0 == 30 and close(math.hypot(ux0, vy0), 25) and not close(math.degrees(math.atan(vy0 / ux0)), 45)
multi_key([t0 == 2, ux0 * t0 == 30, close(math.hypot(ux0, vy0), 25), close(vy0, ux0), True], "abce")
add(T, "Projectile motion", "Advanced", "multi_statement",
    multi("A stone is thrown horizontally with a speed of 15 m/s from the top of a cliff 20 m above level ground. "
          "Taking g = 10 m/s² and neglecting air resistance, which of the following statements are correct?",
          ["The stone takes 2 s to reach the ground.",
           "It lands 30 m from the foot of the cliff.",
           "It strikes the ground with a speed of 25 m/s.",
           "Its velocity makes an angle of 45° with the horizontal as it strikes the ground.",
           "Throughout its flight, its acceleration is 10 m/s² directed vertically downward."]),
    place("(a), (b), (c) and (e) only", ["(a), (b) and (d) only", "(a), (c), (d) and (e) only",
                                         "(b), (c) and (e) only"], "A"),
    "Horizontal projection",
    "The vertical motion starts from rest and is free fall; the horizontal velocity stays 15 m/s. The time of fall "
    "fixes everything else.",
    ["(a) 20 = ½ × 10 × t² → t = 2 s (true)", "(b) x = 15 × 2 = 30 m (true)",
     "(c) v_y = 10 × 2 = 20 m/s; v = √(15² + 20²) = 25 m/s (true)",
     "(d) tan α = 20/15 = 4/3 → α ≈ 53°, not 45° (false)", "(e) only gravity acts (true)"],
    why="(d) would need v_y = v_x = 15 m/s; options containing (d) or leaving out a true statement are wrong.",
    ncert="Class 11 Physics, 'Motion in a Plane', projectile motion", seconds=100, recomputed=True)


# =====================================================================================================================
# Laws of Motion (B4 I5 A4)
# =====================================================================================================================
T = "Laws of Motion"

M_tr, v_tr, m_man = 200.0, 3.0, 100.0
v_new = M_tr * v_tr / (M_tr + m_man)
assert v_new == 2 and close(m_man * v_tr / (M_tr + m_man), 1) and close((M_tr + m_man) / M_tr * v_tr, 4.5)
add(T, "Conservation of linear momentum", "Basic", "numerical",
    "A trolley of mass 200 kg moves at 3 m/s along a smooth, straight horizontal track. A man of mass 100 kg drops "
    "vertically onto it from a small height, with no horizontal velocity, and stays on it. The speed of the trolley "
    "with the man on it is:",
    place("2 m/s", ["1 m/s", "3 m/s", "4.5 m/s"], "B"),
    "Conservation of horizontal momentum",
    "No horizontal external force acts on the trolley–man system, so its horizontal momentum is conserved. The man "
    "brings no horizontal momentum but adds to the moving mass.",
    ["Before: 200 × 3 + 100 × 0 = 600 kg m/s", "After: (200 + 100)v = 600 → v = 2 m/s"],
    why="1 m/s uses the man's mass in place of the trolley's in the numerator. 3 m/s ignores the extra mass. "
        "4.5 m/s inverts the mass ratio.",
    ncert="Class 11 Physics, 'Laws of Motion', conservation of momentum", seconds=40, recomputed=True)

a_dec = 2.0
mu_k = a_dec / g
assert close(mu_k, 0.2) and close(g / a_dec, 5)
add(T, "Friction", "Basic", "numerical",
    "A block sliding on a rough horizontal floor slows down uniformly at 2 m/s² with no force acting on it other "
    "than gravity, the normal reaction and friction. Taking g = 10 m/s², the coefficient of kinetic friction "
    "between the block and the floor is:",
    place("0.2", ["2", "0.02", "5"], "D"),
    "Kinetic friction as the only horizontal force",
    "On a horizontal floor the normal reaction is mg, so the friction force is μₖmg and the retardation is μₖg.",
    ["μₖmg = ma → μₖ = a/g", "μₖ = 2/10 = 0.2"],
    why="2 equates μₖ to the retardation itself. 0.02 divides by g twice. 5 inverts the ratio (g/a).",
    ncert="Class 11 Physics, 'Laws of Motion', friction", seconds=30, recomputed=True)

add(T, "Newton's laws and impulse", "Basic", "direct",
    "From his experiments with balls rolling down one smooth inclined plane and up another, Galileo concluded that:",
    place("On a frictionless horizontal plane, a moving ball would keep moving with constant velocity",
          ["A force is needed to keep a body moving with uniform velocity",
           "A heavier ball always rolls down an inclined plane faster than a lighter one",
           "The acceleration of a body is proportional to the net force on it"], "C"),
    "Galileo's law of inertia",
    "With a second, less steep plane the ball still rose to nearly its starting height, travelling farther. Galileo "
    "argued that if the second plane were made horizontal and friction removed, the ball would go on moving for ever "
    "with constant velocity: an external force is needed to change a body's velocity, not to maintain it.",
    ["Double inclined plane: the ball rises to nearly the same height", "Horizontal second plane, no friction → "
     "motion continues with uniform velocity (law of inertia)"],
    why="'A force is needed to keep a body moving' is Aristotle's view that Galileo overturned. The other two are "
        "not what the inclined-plane experiments showed; the force–acceleration relation is Newton's second law.",
    ncert="Class 11 Physics, 'Laws of Motion', the law of inertia", seconds=35)

add(T, "Newton's laws and impulse", "Basic", "assertion_reason",
    AR_STEM.format(
        a="Mud on the rim of a wheel spinning rapidly about a fixed axle flies off along the tangent to the rim at "
          "the point where it leaves.",
        r="An outward centrifugal force acting on the mud throws it off radially, along the line from the axle to "
          "the rim."),
    ar("C"),
    "Newton's first law in circular motion",
    "While stuck to the wheel, the mud needs a centripetal force, supplied by adhesion. When adhesion can no longer "
    "provide it, no horizontal force acts on the mud, so by the first law it continues with the velocity it had at "
    "that instant, which is along the tangent. In the ground frame there is no outward 'centrifugal' force, and the "
    "mud does not fly off radially.",
    ["Velocity of a point on the rim is tangential", "Once released, the mud keeps that velocity (first law) → A true",
     "No outward force in the inertial frame, and motion is not radial → R false"],
    why="R is false, so A and B are wrong; A is true, so D is wrong.",
    ncert="Class 11 Physics, 'Laws of Motion', Newton's first law of motion", seconds=45)

m_bob, a_car = 4.0, 7.5
T_bob = m_bob * math.hypot(g, a_car)
th_bob = math.degrees(math.atan(a_car / g))
assert close(T_bob, 50) and close(th_bob, 36.87) and close(m_bob * (g + a_car), 70)
add(T, "Newton's laws and impulse", "Intermediate", "numerical",
    "A bob of mass 4 kg hangs by a light string from the roof of a car moving on a level road with a constant "
    "acceleration of 7.5 m/s². The bob hangs at rest relative to the car. Taking g = 10 m/s², the tension in the "
    "string and the angle the string makes with the vertical are:",
    place("50 N and 37°", ["40 N and 37°", "30 N and 53°", "70 N and 37°"], "A"),
    "Newton's second law for an accelerating bob (ground frame)",
    "Seen from the ground, the bob accelerates horizontally with the car. The horizontal component of the tension "
    "gives it this acceleration; the vertical component balances its weight.",
    ["T sin θ = ma = 30 N, T cos θ = mg = 40 N", "tan θ = 0.75 → θ = 37°", "T = √(30² + 40²) = 50 N"],
    why="40 N is only the weight. 30 N and 53° take the horizontal component as the tension and swap the angle. "
        "70 N adds ma and mg as if they were along the same line.",
    ncert="Class 11 Physics, 'Laws of Motion', Newton's second law of motion", seconds=70, recomputed=True)

Lr, span, W_ = 10.0, 8.0, 60.0
sag = math.sqrt((Lr / 2) ** 2 - (span / 2) ** 2)
sin_h = sag / (Lr / 2)
T_rope = W_ / (2 * sin_h)
assert close(sag, 3) and close(T_rope, 50) and close(W_ / (2 * 0.8), 37.5)
add(T, "Equilibrium of concurrent forces", "Intermediate", "numerical",
    "A light inextensible rope 10 m long is tied at its ends to two hooks at the same level, 8 m apart. A load of "
    "weight 60 N hangs from the midpoint of the rope and is at rest. The tension in each half of the rope is:",
    place("50 N", ["37.5 N", "30 N", "100 N"], "D"),
    "Equilibrium of three concurrent forces",
    "The two halves of the rope and the load meet at the midpoint. By symmetry the tensions are equal; their "
    "vertical components together balance the load.",
    ["Each half is 5 m long, with a horizontal reach of 4 m → sag = √(5² − 4²) = 3 m",
     "Each half makes an angle with the horizontal whose sine is 3/5",
     "2T × 3/5 = 60 → T = 50 N"],
    why="37.5 N uses the cosine (4/5) instead of the sine. 30 N simply shares the load equally, as if the rope "
        "halves were vertical. 100 N takes the sine as 3/10, dividing the sag by the whole rope length instead "
        "of by one half.",
    ncert="Class 11 Physics, 'Laws of Motion', equilibrium of a particle", seconds=70, recomputed=True)

M_lift, a_up = 800.0, 2.0
T_cable = M_lift * (g + a_up)
assert T_cable == 9600 and M_lift * (g - a_up) == 6400 and M_lift * g == 8000 and M_lift * a_up == 1600
add(T, "Newton's laws and impulse", "Intermediate", "numerical",
    "A lift of total mass 800 kg is moving downward and is slowing down at a uniform rate of 2 m/s². Taking "
    "g = 10 m/s², the tension in its supporting cable is:",
    place("9600 N", ["6400 N", "8000 N", "1600 N"], "B"),
    "Direction of acceleration when slowing down",
    "A body moving downward and slowing down has an acceleration directed upward. Newton's second law along the "
    "upward direction then gives T − Mg = Ma.",
    ["Acceleration = 2 m/s² upward", "T = M(g + a) = 800 × 12 = 9600 N"],
    why="6400 N takes the acceleration as downward because the lift moves down. 8000 N ignores the acceleration. "
        "1600 N is only Ma.",
    ncert="Class 11 Physics, 'Laws of Motion', Newton's second law of motion", seconds=50, recomputed=True)

res = lambda f, th: 2 * f * math.cos(math.radians(th) / 2)
assert close(math.hypot(3, 4), 5) and close(res(10, 120), 10) and close(res(10, 60), 10 * math.sqrt(3)) \
    and close(res(10, 90), 10 * math.sqrt(2))
add(T, "Equilibrium of concurrent forces", "Intermediate", "match_list",
    match_stem("In each case of List-I, two forces act at a point and a third force is applied there so that the "
               "particle is in equilibrium. Match List-I (the two given forces) with List-II (magnitude of the third "
               "force).",
               ["3 N and 4 N, perpendicular to each other", "10 N and 10 N, with an angle of 120° between them",
                "10 N and 10 N, with an angle of 60° between them",
                "10 N and 10 N, perpendicular to each other"],
               ["10 N", "10√2 N", "5 N", "10√3 N"]),
    match_options({"A": "III", "B": "I", "C": "IV", "D": "II"},
                  [{"A": "III", "B": "IV", "C": "I", "D": "II"}, {"A": "I", "B": "III", "C": "IV", "D": "II"},
                   {"A": "III", "B": "I", "C": "II", "D": "IV"}], "C"),
    "Equilibrium of three concurrent forces",
    "For equilibrium the third force must be equal and opposite to the resultant of the other two, "
    "R = √(P² + Q² + 2PQ cos θ); for equal forces this is 2P cos(θ/2).",
    ["A: √(9 + 16) = 5 N (III)", "B: 2 × 10 × cos 60° = 10 N (I)", "C: 2 × 10 × cos 30° = 10√3 N (IV)",
     "D: 2 × 10 × cos 45° = 10√2 N (II)"],
    why="The other codes swap the 60° and 120° cases (a smaller angle gives a larger resultant) or the 60° and 90° "
        "cases.",
    ncert="Class 11 Physics, 'Laws of Motion', equilibrium of a particle", seconds=70, recomputed=True)

add(T, "Newton's laws and impulse", "Intermediate", "statement_pair",
    SP_STEM.format(
        s1="When a light inextensible string passes over a light, frictionless pulley, the tension in the string is "
           "the same on both sides of the pulley.",
        s2="The tension is the same at every point of a heavy uniform rope that hangs vertically from a ceiling with "
           "nothing attached to its lower end."),
    sp("C"),
    "Tension in light and heavy strings",
    "A light (massless) string needs no net force to accelerate any part of it, and a light frictionless pulley "
    "exerts no tangential force on it, so the tension is the same throughout. In a heavy rope, each point must "
    "support the weight of the rope below it: the tension is zero at the free lower end and equal to the full weight "
    "at the top.",
    ["Statement I: massless string, frictionless massless pulley → equal tensions (true)",
     "Statement II: tension at height y above the free end = weight of the length y → varies (false)"],
    why="Statement II ignores the rope's own weight, so A, B and D are wrong.",
    ncert="Class 11 Physics, 'Laws of Motion', Newton's second law and equilibrium (strings and pulleys)",
    seconds=45)

sin37, cos37, mu37 = 0.6, 0.8, 0.5
a_up37 = g * (sin37 + mu37 * cos37)
a_dn37 = g * (sin37 - mu37 * cos37)
assert close(a_up37, 10) and close(a_dn37, 2) and mu37 < sin37 / cos37
ratio_t = math.sqrt(a_up37 / a_dn37)
assert close(ratio_t, math.sqrt(5)) and close(math.sqrt(a_up37 / (g * sin37)), math.sqrt(5 / 3))
add(T, "Friction", "Advanced", "numerical",
    "A block is projected up a rough plane inclined at 37° to the horizontal (sin 37° = 0.6, cos 37° = 0.8). The "
    "coefficient of friction between the block and the plane is 0.5 (both static and kinetic). The block goes up, "
    "stops and slides back to its starting point. Taking g = 10 m/s², the ratio of the time taken to come down to "
    "the time taken to go up is:",
    place("√5", ["5", "1", "√(5/3)"], "B"),
    "Friction reverses direction when the motion reverses",
    "Going up, gravity and friction both act down the slope; coming down, friction acts up the slope. The block does "
    "slide back because tan 37° = 0.75 exceeds μ = 0.5. Both legs cover the same distance s from rest or to rest, so "
    "t = √(2s/a) for each.",
    ["Up: a₁ = g(sin θ + μ cos θ) = 10(0.6 + 0.4) = 10 m/s²",
     "Down: a₂ = g(sin θ − μ cos θ) = 10(0.6 − 0.4) = 2 m/s²",
     "t_down/t_up = √(a₁/a₂) = √(10/2) = √5"],
    why="5 is the ratio of the accelerations, not of the times. 1 assumes the motion is symmetric, which is true "
        "only without friction. √(5/3) leaves out friction on the way down.",
    ncert="Class 11 Physics, 'Laws of Motion', friction", seconds=110, recomputed=True)

m_p, M_t, v_rel = 50.0, 100.0, 6.0
v_trol = -m_p * v_rel / (m_p + M_t)
assert close(v_trol, -2) and close(v_trol + v_rel, 4) and close(m_p * v_rel / M_t, 3)
add(T, "Conservation of linear momentum", "Advanced", "numerical",
    "A person of mass 50 kg stands at rest on a trolley of mass 100 kg, which is at rest on a smooth horizontal "
    "floor. The person starts running on the trolley and quickly reaches a velocity of 6 m/s relative to the "
    "trolley. The speed of the trolley relative to the floor is then:",
    place("2 m/s, opposite to the person's motion", ["3 m/s, opposite to the person's motion",
                                                     "4 m/s, opposite to the person's motion",
                                                     "6 m/s, opposite to the person's motion"], "D"),
    "Momentum conservation with a relative velocity",
    "No horizontal external force acts, so the total momentum stays zero. Momentum must be written with velocities "
    "relative to the ground: if the trolley moves with velocity v, the person moves with v + 6.",
    ["50(v + 6) + 100v = 0", "150v = −300 → v = −2 m/s", "The person moves at +4 m/s relative to the floor"],
    why="3 m/s treats 6 m/s as the person's velocity relative to the floor. 4 m/s is the person's own speed relative "
        "to the floor. 6 m/s assumes equal and opposite velocities.",
    ncert="Class 11 Physics, 'Laws of Motion', conservation of momentum", seconds=100, recomputed=True)

m_ball, u_b, v_b, dt = 0.5, 4.0, -6.0, 0.01
dp = m_ball * (v_b - u_b)
Favg = dp / dt
KE1, KE2 = 0.5 * m_ball * u_b ** 2, 0.5 * m_ball * v_b ** 2
assert close(dp, -5) and close(Favg, -500) and KE1 == 4 and KE2 == 9
multi_key([close(dp, -5), close(abs(dp), 5), close(Favg, -500), close(-Favg, 500), KE1 == KE2], "abcd")
add(T, "Newton's laws and impulse", "Advanced", "multi_statement",
    multi("A ball of mass 0.5 kg moving at 4 m/s in the +x direction is struck by a bat and moves off at 6 m/s in "
          "the −x direction. The bat is in contact with the ball for 0.01 s. Which of the following statements are "
          "correct?",
          ["The change in the momentum of the ball has magnitude 5 kg m/s and is directed along −x.",
           "The magnitude of the impulse delivered to the ball is 5 N s.",
           "The average force exerted by the bat on the ball is 500 N, directed along −x.",
           "The average force exerted by the ball on the bat is 500 N, directed along +x.",
           "The kinetic energy of the ball is unchanged by the hit."]),
    place("(a), (b), (c) and (d) only", ["(a), (b) and (e) only", "(b), (c) and (d) only",
                                         "(a), (c), (d) and (e) only"], "A"),
    "Impulse, average force and Newton's third law",
    "Impulse equals change in momentum, with velocities taken with sign. The average force is impulse divided by "
    "the contact time, and by the third law the ball pushes the bat with an equal and opposite force.",
    ["(a) Δp = 0.5(−6 − 4) = −5 kg m/s (true)", "(b) impulse = |Δp| = 5 N s (true)",
     "(c) F = −5/0.01 = −500 N, i.e. 500 N along −x (true)", "(d) third law: 500 N along +x on the bat (true)",
     "(e) KE changes from 4 J to 9 J (false)"],
    why="(e) is false, and (b), (c), (d) only leaves out the true statement (a).",
    ncert="Class 11 Physics, 'Laws of Motion', impulse and Newton's third law", seconds=100, recomputed=True)

r_bk, tan_bk = 50.0, 0.2
v_opt = math.sqrt(r_bk * g * tan_bk)
assert close(v_opt, 10)
need = lambda v: v ** 2 / (r_bk * g) - tan_bk     # >0 friction down the slope, <0 friction up the slope
assert need(5) < 0 and need(15) > 0 and close(need(10), 0)
multi_key([close(need(10), 0), need(5) < 0, need(15) > 0, False, False], "abc")
add(T, "Circular motion: level and banked roads", "Advanced", "multi_statement",
    multi("A circular road of radius 50 m is banked at an angle θ with tan θ = 0.2. Take g = 10 m/s². Which of the "
          "following statements about a car going round it at a steady speed are correct?",
          ["At 10 m/s the car needs no friction to go round the curve.",
           "At 5 m/s the friction force on the tyres acts up the slope.",
           "At 15 m/s the friction force on the tyres acts down the slope.",
           "At 10 m/s the normal reaction of the road on the car equals mg cos θ.",
           "A heavier car has a larger speed at which no friction is needed."]),
    place("(a), (b) and (c) only", ["(a), (b), (c) and (d) only", "(a) and (e) only",
                                    "(b), (c) and (d) only"], "B"),
    "Optimum speed on a banked road",
    "Without friction, N sin θ = mv²/r and N cos θ = mg, so v₀ = √(rg tan θ), independent of mass. Below v₀ the car "
    "tends to slide down the slope and friction acts up it; above v₀ friction acts down the slope.",
    ["(a) v₀ = √(50 × 10 × 0.2) = 10 m/s (true)", "(b) 5 m/s < v₀ → friction up the slope (true)",
     "(c) 15 m/s > v₀ → friction down the slope (true)",
     "(d) N cos θ = mg → N = mg/cos θ, not mg cos θ (false)", "(e) v₀ does not depend on mass (false)"],
    why="(d) uses the inclined-plane result N = mg cos θ, which holds only without the horizontal centripetal "
        "acceleration; (e) is false because the mass cancels.",
    ncert="Class 11 Physics, 'Laws of Motion', circular motion (motion of a car on a banked road)", seconds=110,
    recomputed=True)


# =====================================================================================================================
# Work, Energy and Power (B4 I5 A4)
# =====================================================================================================================
T = "Work, Energy and Power"

KE = lambda m, v: F(1, 2) * m * v * v
assert KE(F(1, 2), 2) / KE(1, 1) == 2
add(T, "Work-energy theorem", "Basic", "numerical",
    "The mass of a moving body is halved and its speed is doubled. Its kinetic energy:",
    place("Becomes twice its earlier value", ["Becomes four times its earlier value", "Remains unchanged",
                                              "Becomes half its earlier value"], "D"),
    "Kinetic energy K = ½mv²",
    "Kinetic energy is proportional to the mass and to the square of the speed.",
    ["K' = ½ (m/2)(2v)² = ½ m v² × (4/2)", "K' = 2K"],
    why="Four times ignores the halving of the mass. 'Unchanged' treats K as proportional to v, not v². Half "
        "ignores the change in speed.",
    ncert="Class 11 Physics, 'Work, Energy and Power', kinetic energy", seconds=30, recomputed=True)

Fw, dw = 10.0, 2.0
Wa = lambda th: Fw * dw * math.cos(math.radians(th))
assert close(Wa(0), 20) and close(Wa(60), 10) and abs(Wa(90)) < 1e-9 and close(Wa(180), -20)
add(T, "Work by constant and variable force", "Basic", "match_list",
    match_stem("A constant force of 10 N acts on a body while the body is displaced through 2 m in a straight line. "
               "Match List-I (angle between the force and the displacement) with List-II (work done by the force).",
               ["0°", "60°", "90°", "180°"],
               ["Zero", "−20 J", "+20 J", "+10 J"]),
    match_options({"A": "III", "B": "IV", "C": "I", "D": "II"},
                  [{"A": "III", "B": "I", "C": "IV", "D": "II"}, {"A": "IV", "B": "III", "C": "I", "D": "II"},
                   {"A": "III", "B": "IV", "C": "II", "D": "I"}], "A"),
    "Work done by a constant force, W = Fd cos θ",
    "Work is the scalar product of force and displacement. It is positive for θ < 90°, zero at 90° and negative for "
    "θ > 90°.",
    ["0°: 10 × 2 × 1 = +20 J (III)", "60°: 20 × ½ = +10 J (IV)", "90°: cos 90° = 0 → zero (I)",
     "180°: 20 × (−1) = −20 J (II)"],
    why="The other codes give 60° the full 20 J, use sin θ in place of cos θ, or treat 90° and 180° alike.",
    ncert="Class 11 Physics, 'Work, Energy and Power', work", seconds=40, recomputed=True)

add(T, "Work-energy theorem", "Basic", "direct",
    "The gravitational potential energy of a body near the Earth's surface is written as mgh, where h is measured "
    "from a chosen reference level. Which of the following does NOT depend on the choice of this reference level?",
    place("The change in its potential energy when it moves from one point to another",
          ["The value of its potential energy at a given point", "The sign of its potential energy at a given point",
           "The value of h for a given point"], "B"),
    "Only differences of potential energy are physically meaningful",
    "Shifting the zero of potential energy adds the same constant to the potential energy at every point. Values "
    "and signs at a point change with the choice, but the difference between two points does not, and it is this "
    "difference that equals the work done by gravity.",
    ["U(point) = mgh changes when the reference level changes", "U₂ − U₁ = mg(h₂ − h₁) is unaffected"],
    why="The value, the sign of U and the height h at a point all depend on where the zero is placed.",
    ncert="Class 11 Physics, 'Work, Energy and Power', the concept of potential energy", seconds=35)

add(T, "Spring potential energy", "Basic", "assertion_reason",
    AR_STEM.format(
        a="An ideal spring stretched by 2 cm and the same spring compressed by 2 cm from its natural length store "
          "equal amounts of elastic potential energy.",
        r="The potential energy of an ideal spring is ½kx², which depends on the square of its displacement x from "
          "the natural length."),
    ar("A"),
    "Potential energy of a spring",
    "Because the spring force is −kx, the work done in deforming the spring by x from its natural length is ½kx², "
    "whatever the sign of x. An extension and a compression of the same size therefore store the same energy.",
    ["U = ½kx²; x = +2 cm and x = −2 cm give the same x²", "So A is true, and R is the reason"],
    why="R directly gives why the energy is the same for +x and −x, so B is wrong; both are true, so C and D are "
        "wrong.",
    ncert="Class 11 Physics, 'Work, Energy and Power', the potential energy of a spring", seconds=35)

dU = {"5x²": "−10x", "−5x²": "+10x", "5x": "−5", "5/x": "+5/x²"}
xs = 1.7
num_der = lambda f, x, h=1e-6: (f(x + h) - f(x - h)) / (2 * h)
assert close(-num_der(lambda x: 5 * x * x, xs), -10 * xs) and close(-num_der(lambda x: -5 * x * x, xs), 10 * xs)
assert close(-num_der(lambda x: 5 * x, xs), -5) and close(-num_der(lambda x: 5 / x, xs), 5 / xs ** 2)
add(T, "Work by constant and variable force", "Intermediate", "match_list",
    match_stem("A particle moves along the positive x-axis under a conservative force. Match List-I (potential energy "
               "U(x), in joules, with x in metres) with List-II (the force F(x) on the particle, in newtons).",
               ["U = 5x²", "U = −5x²", "U = 5x", "U = 5/x"],
               ["F = −5", "F = +10x", "F = −10x", "F = +5/x²"]),
    match_options({"A": "III", "B": "II", "C": "I", "D": "IV"},
                  [{"A": "II", "B": "III", "C": "I", "D": "IV"}, {"A": "III", "B": "II", "C": "IV", "D": "I"},
                   {"A": "I", "B": "II", "C": "III", "D": "IV"}], "D"),
    "Force from potential energy, F = −dU/dx",
    "For a conservative force in one dimension, the force is the negative of the slope of the potential energy "
    "curve: it points towards decreasing potential energy.",
    ["A: −d(5x²)/dx = −10x (III)", "B: −d(−5x²)/dx = +10x (II)", "C: −d(5x)/dx = −5 (I)",
     "D: −d(5/x)/dx = −(−5/x²) = +5/x² (IV)"],
    why="The other codes drop the minus sign in F = −dU/dx, or confuse U = 5x with U = 5/x.",
    ncert="Class 11 Physics, 'Work, Energy and Power', the concept of potential energy (F = −dV/dx)", seconds=60,
    recomputed=True)

v0p, v1p = 300.0, 100.0
loss_per = v0p ** 2 - v1p ** 2
frac2 = v1p ** 2 / loss_per
assert close(frac2, 1 / 8) and close(v1p / (v0p - v1p), 0.5) and close(v1p ** 2 / v0p ** 2, 1 / 9)
add(T, "Work-energy theorem", "Intermediate", "numerical",
    "A bullet moving at 300 m/s passes through a wooden plank and comes out at 100 m/s. It then enters a second, "
    "identical plank. Assuming the planks exert the same constant resistive force on the bullet, the fraction of the "
    "thickness of the second plank it penetrates before stopping is:",
    place("1/8", ["1/2", "1/9", "1/3"], "C"),
    "Work–energy theorem with a constant resistive force",
    "The work done by a constant resistive force is proportional to the distance moved, so equal thicknesses remove "
    "equal amounts of kinetic energy.",
    ["KE ∝ v²: loss in one plank ∝ 300² − 100² = 80 000", "KE left ∝ 100² = 10 000",
     "Fraction of second plank = 10 000/80 000 = 1/8"],
    why="1/2 compares speeds (it loses 200 m/s per plank and has 100 m/s left), which is wrong because the work done "
        "depends on KE, not speed. 1/9 divides by the initial KE instead of by the loss per plank. 1/3 divides the "
        "speeds 100/300.",
    ncert="Class 11 Physics, 'Work, Energy and Power', the work–energy theorem", seconds=75, recomputed=True)

ratio = F(2)
assert (ratio - 1) / (ratio + 1) == F(1, 3) and (F(1, 2) - 1) / (F(1, 2) + 1) == F(-1, 3)
add(T, "Collisions", "Intermediate", "numerical",
    "A body of mass m₁ moving with speed u collides head-on and elastically with a body of mass m₂ at rest. After "
    "the collision m₁ continues to move in its original direction with speed u/3. The ratio m₁/m₂ is:",
    place("2", ["3", "1/2", "4"], "A"),
    "One-dimensional elastic collision",
    "For an elastic head-on collision with the second body at rest, v₁ = (m₁ − m₂)u/(m₁ + m₂). A positive v₁ means "
    "the first body keeps moving forward, which needs m₁ > m₂.",
    ["(m₁ − m₂)/(m₁ + m₂) = 1/3", "3m₁ − 3m₂ = m₁ + m₂ → 2m₁ = 4m₂ → m₁/m₂ = 2"],
    why="1/2 gives v₁ = −u/3, i.e. the first body rebounds. 3 and 4 do not satisfy the elastic-collision result "
        "(they give u/2 and 3u/5).",
    ncert="Class 11 Physics, 'Work, Energy and Power', collisions in one dimension", seconds=60, recomputed=True)
assert (F(3) - 1) / (F(3) + 1) == F(1, 2) and (F(4) - 1) / (F(4) + 1) == F(3, 5)

vt2 = 2                                    # v_top^2 in units of gL
T_top = vt2 - 1                            # in units of mg
vb2 = vt2 + 4
T_bot = vb2 + 1
assert T_top == 1 and T_bot == 7 and F(T_bot, 1 + vt2) == F(7, 3) and (vt2 + 2) + 1 == 5
add(T, "Motion in a vertical circle", "Intermediate", "numerical",
    "A small stone tied to a light string of length L is whirled in a vertical circle. Its speed at the highest "
    "point is √(2gL). Neglecting air resistance, the ratio of the tension in the string at the lowest point to that "
    "at the highest point is:",
    place("7 : 1", ["6 : 1", "7 : 3", "5 : 1"], "B"),
    "Tension and energy conservation in a vertical circle",
    "At the top, gravity and tension both point towards the centre: T + mg = mv²/L. At the bottom, tension points "
    "to the centre and gravity away: T − mg = mv²/L. Energy conservation links the two speeds.",
    ["Top: T₁ = m(2gL)/L − mg = mg", "Bottom: v² = 2gL + 2g(2L) = 6gL",
     "T₂ = m(6gL)/L + mg = 7mg", "T₂ : T₁ = 7 : 1"],
    why="6 : 1 forgets to add mg at the lowest point. 7 : 3 adds mg at the top instead of subtracting it. 5 : 1 "
        "takes the speed at the bottom as if the stone fell through only L (v² = 4gL).",
    ncert="Class 11 Physics, 'Work, Energy and Power', conservation of mechanical energy (motion in a vertical circle)",
    seconds=80, recomputed=True)

add(T, "Work-energy theorem", "Intermediate", "statement_pair",
    SP_STEM.format(
        s1="The kinetic energy of a body has the same value in every inertial frame of reference.",
        s2="The work–energy theorem can be derived from Newton's second law of motion."),
    sp("D"),
    "Frame dependence of kinetic energy; origin of the work–energy theorem",
    "Velocity depends on the frame of reference, so ½mv² does too: a passenger sitting in a moving train has zero "
    "kinetic energy relative to the train but not relative to the ground. The work–energy theorem follows by "
    "integrating Newton's second law along the path (from v² − u² = 2as for a constant force).",
    ["Statement I: KE depends on the observer's frame → false",
     "Statement II: multiply v² − u² = 2as by m/2 → ½mv² − ½mu² = Fs → true"],
    why="Statement I is false and Statement II is true, so only D fits.",
    ncert="Class 11 Physics, 'Work, Energy and Power', the work–energy theorem", seconds=45)

m1c, m2c, u1c, kc = 1.0, 1.0, 2.0, 400.0
vc = m1c * u1c / (m1c + m2c)
Espring = 0.5 * m1c * u1c ** 2 - 0.5 * (m1c + m2c) * vc ** 2
xmax = math.sqrt(2 * Espring / kc)
assert close(Espring, 1) and close(xmax, 0.05 * math.sqrt(2))
assert close(math.sqrt(2 * 2 / kc), 0.1) and close(math.sqrt(2 * 0.5 / kc), 0.05) and close(math.sqrt(2 * 4 / kc), 0.1 * math.sqrt(2))
add(T, "Collisions", "Advanced", "numerical",
    "Two blocks, each of mass 1 kg, lie on a smooth horizontal surface. A light spring of spring constant 400 N/m is "
    "attached to block B. Block A moves towards B at 2 m/s along the axis of the spring, while B is at rest. The "
    "maximum compression of the spring is:",
    place("5√2 cm", ["10 cm", "5 cm", "10√2 cm"], "C"),
    "Collision through a spring: momentum and energy",
    "At maximum compression the two blocks move with a common velocity. Momentum is conserved throughout, and the "
    "kinetic energy 'missing' at that instant is stored in the spring.",
    ["Common velocity = (1 × 2)/(1 + 1) = 1 m/s", "KE before = ½ × 1 × 2² = 2 J; KE at max compression = "
     "½ × 2 × 1² = 1 J", "½ × 400 × x² = 1 J → x² = 0.005 m² → x = 0.05√2 m = 5√2 cm"],
    why="10 cm puts all of A's 2 J into the spring, ignoring that B must also move. 5 cm uses only 0.5 J. "
        "10√2 cm treats both blocks as moving at 2 m/s initially (4 J).",
    ncert="Class 11 Physics, 'Work, Energy and Power', collisions and the potential energy of a spring",
    seconds=110, recomputed=True)

Mch, Lch = F(1), F(1)
f_h = F(1, 4)
W_chain = (f_h * Mch) * g * (f_h * Lch / 2)
assert W_chain == F(1, 32) * g and (f_h * Mch) * (f_h * Lch) == F(1, 16) and Mch * f_h * Lch / 2 == F(1, 8)
add(T, "Work by constant and variable force", "Advanced", "numerical",
    "A uniform chain of mass M and length L lies on a smooth horizontal table with one-quarter of its length hanging "
    "vertically over the edge. The minimum work needed to pull the hanging part slowly back onto the table is (g is "
    "the acceleration due to gravity):",
    place("MgL/32", ["MgL/16", "MgL/8", "MgL/4"], "A"),
    "Work against gravity on a distributed mass",
    "Only the hanging part has to be raised. Its mass is M/4 and its centre of mass is L/8 below the table top, "
    "so the work equals the gain in its gravitational potential energy.",
    ["Hanging mass = M/4", "Its centre of mass is (L/4)/2 = L/8 below the edge",
     "W = (M/4) g (L/8) = MgL/32"],
    why="MgL/16 raises the hanging mass through its full length L/4. MgL/8 uses the whole mass M with depth L/8. "
        "MgL/4 uses the whole mass and the full hanging length.",
    ncert="Class 11 Physics, 'Work, Energy and Power', work and potential energy", seconds=90, recomputed=True)
assert Mch * g * f_h * Lch == F(1, 4) * g

mdot, hp, vn, eff = 5.0, 10.0, 10.0, 0.75
P_out = mdot * (g * hp + 0.5 * vn ** 2)
P_in = P_out / eff
assert close(P_out, 750) and close(P_in, 1000) and close(mdot * g * hp / eff, 666.67) \
    and close(mdot * (g * hp + vn ** 2) / eff, 1333.3)
add(T, "Power", "Advanced", "numerical",
    "An electric pump lifts water from a well through a height of 10 m and delivers it through a nozzle at a speed "
    "of 10 m/s, at the rate of 5 kg per second. The efficiency of the pump is 75%. Taking g = 10 m/s², the electrical "
    "power drawn by the pump is:",
    place("1000 W", ["750 W", "about 667 W", "about 1333 W"], "D"),
    "Power to raise and accelerate a fluid",
    "Each second the pump must give 5 kg of water both potential energy mgh and kinetic energy ½mv². Dividing the "
    "useful power by the efficiency gives the power drawn.",
    ["Useful power = 5(10 × 10 + ½ × 10²) = 5(100 + 50) = 750 W", "Power drawn = 750/0.75 = 1000 W"],
    why="750 W is the useful output, not the input. About 667 W ignores the kinetic energy given to the water. "
        "About 1333 W uses v² instead of ½v².",
    ncert="Class 11 Physics, 'Work, Energy and Power', power", seconds=90, recomputed=True)

ma_, mb_, ua_ = 1.0, 3.0, 8.0
vcm = ma_ * ua_ / (ma_ + mb_)
K1 = 0.5 * ma_ * ua_ ** 2
K2 = 0.5 * (ma_ + mb_) * vcm ** 2
assert vcm == 2 and K1 == 32 and K2 == 8 and K1 - K2 == 24 and close((K1 - K2) / K1, 0.75) and mb_ * vcm == 6
multi_key([vcm == 2, K1 - K2 == 24, close((K1 - K2) / K1, 0.25), (ma_ + mb_) * vcm == 8, mb_ * vcm == 6], "abde")
add(T, "Collisions", "Advanced", "multi_statement",
    multi("A block of mass 1 kg moving at 8 m/s on a smooth horizontal surface collides with a block of mass 3 kg at "
          "rest. The two blocks stick together. Which of the following statements are correct?",
          ["The blocks move together at 2 m/s after the collision.",
           "24 J of kinetic energy is lost in the collision.",
           "One-quarter of the initial kinetic energy is lost.",
           "The total linear momentum after the collision is 8 kg m/s.",
           "The impulse delivered to the 3 kg block is 6 N s."]),
    place("(a), (b), (d) and (e) only", ["(a), (b) and (c) only", "(a), (c), (d) and (e) only",
                                         "(b), (d) and (e) only"], "B"),
    "Perfectly inelastic collision",
    "Momentum is conserved in every collision. When the bodies stick together, kinetic energy is not conserved; the "
    "loss follows from the common velocity.",
    ["(a) v = (1 × 8)/4 = 2 m/s (true)", "(b) KE: 32 J → ½ × 4 × 2² = 8 J; loss 24 J (true)",
     "(c) 24/32 = 3/4 is lost, not 1/4 (false)", "(d) p = 1 × 8 = 8 kg m/s, conserved (true)",
     "(e) Impulse on 3 kg block = 3 × 2 − 0 = 6 N s (true)"],
    why="(c) gives the fraction retained (8/32) instead of the fraction lost; (b), (d), (e) only leaves out the true "
        "statement (a).",
    ncert="Class 11 Physics, 'Work, Energy and Power', collisions", seconds=100, recomputed=True)


# =====================================================================================================================
# Rotational Motion (B4 I5 A4)
# =====================================================================================================================
T = "Rotational Motion"

Ms, Rs = 5.0, 0.2
I_tan = (0.4 + 1) * Ms * Rs ** 2
assert close(I_tan, 0.28) and close(0.4 * Ms * Rs ** 2, 0.08) and close(Ms * Rs ** 2, 0.2) \
    and close((2 / 3 + 1) * Ms * Rs ** 2, 0.3333)
add(T, "Moment of inertia and axis theorems", "Basic", "numerical",
    "A uniform solid sphere has mass 5 kg and radius 0.2 m. Its moment of inertia about a tangent to its surface is "
    "(the moment of inertia of a solid sphere about a diameter is 2MR²/5):",
    place("0.28 kg m²", ["0.08 kg m²", "0.20 kg m²", "0.33 kg m²"], "C"),
    "Theorem of parallel axes",
    "A tangent is parallel to a diameter and at a distance R from it, so I = I_cm + MR².",
    ["I_diameter = (2/5) × 5 × 0.04 = 0.08 kg m²", "I_tangent = 0.08 + 5 × 0.04 = 0.28 kg m²"],
    shortcut="I_tangent = (7/5)MR².",
    why="0.08 kg m² is the value about a diameter. 0.20 kg m² is only the MR² term. 0.33 kg m² uses 2/3, the factor "
        "for a thin spherical shell.",
    ncert="Class 11 Physics, 'System of Particles and Rotational Motion', theorems of perpendicular and parallel axes",
    seconds=40, recomputed=True)

w0r, w1r, thr = 10.0, 30.0, 40.0
alpha = (w1r ** 2 - w0r ** 2) / (2 * thr)
assert alpha == 10 and close((w1r - w0r) / thr, 0.5) and (w1r ** 2 - w0r ** 2) / thr == 20
add(T, "Rigid-body rotation", "Basic", "numerical",
    "The angular speed of a wheel rotating about a fixed axis increases uniformly from 10 rad/s to 30 rad/s while "
    "it turns through 40 rad. Its angular acceleration is:",
    place("10 rad/s²", ["0.5 rad/s²", "20 rad/s²", "5 rad/s²"], "A"),
    "Kinematics of rotation with uniform angular acceleration",
    "The rotational analogue of v² = u² + 2as is ω² = ω₀² + 2αθ.",
    ["30² = 10² + 2α(40)", "900 − 100 = 80α → α = 10 rad/s²"],
    why="0.5 rad/s² divides the change in ω by the angle, which is not an equation of rotational kinematics. "
        "20 rad/s² forgets the factor 2. 5 rad/s² doubles the 2.",
    ncert="Class 11 Physics, 'System of Particles and Rotational Motion', kinematics of rotational motion about a "
          "fixed axis", seconds=35, recomputed=True)

add(T, "Moment of inertia and axis theorems", "Basic", "direct",
    "The moment of inertia of a thin-walled hollow cylinder of mass M and radius R about its own axis is:",
    place("MR²", ["MR²/2", "2MR²/5", "MR²/4"], "D"),
    "Moment of inertia of a thin cylindrical shell",
    "Every element of a thin-walled cylinder lies at the same distance R from its axis, so I = Σmᵢ R² = MR², just as "
    "for a thin ring about its axis.",
    ["All mass at distance R from the axis → I = MR²"],
    why="MR²/2 is for a solid cylinder or disc. 2MR²/5 is for a solid sphere about a diameter. MR²/4 is for a disc "
        "about a diameter.",
    ncert="Class 11 Physics, 'System of Particles and Rotational Motion', moment of inertia (table of moments of "
          "inertia)", seconds=25)

add(T, "Centre of mass", "Basic", "assertion_reason",
    AR_STEM.format(
        a="The centre of mass of a system of two particles lies on the line joining them, closer to the heavier "
          "particle.",
        r="When no external force acts on a system of particles, its centre of mass moves with a constant velocity."),
    ar("B"),
    "Location and motion of the centre of mass",
    "For two particles, X = (m₁x₁ + m₂x₂)/(m₁ + m₂), which divides the line joining them in the inverse ratio of the "
    "masses, so it is nearer the heavier one. Separately, with zero external force, M dV/dt = 0 and the centre of "
    "mass moves uniformly. The second fact is about how the centre of mass moves, not where it lies.",
    ["A: r₁/r₂ = m₂/m₁ → nearer the heavier mass (true)", "R: F_ext = 0 → V_cm constant (true)",
     "R says nothing about the position of the centre of mass between the particles"],
    why="Both statements are true but R concerns the motion of the centre of mass, not its location, so A is "
        "wrong; C and D are wrong because both are true.",
    ncert="Class 11 Physics, 'System of Particles and Rotational Motion', centre of mass and motion of centre of mass",
    seconds=45)

d_em = 3.84e5
x_cm = d_em * 1 / (81 + 1)
assert close(x_cm, 4683, 1e-3) and x_cm < 6400 and close(d_em / 81, 4741, 1e-3) and close(d_em * 81 / 82, 3.793e5)
add(T, "Centre of mass", "Intermediate", "numerical",
    "The mass of the Earth is 81 times the mass of the Moon, and the distance between their centres is "
    "3.84 × 10⁵ km. The radius of the Earth is 6400 km. Treating both as particles at their centres, the centre of "
    "mass of the Earth–Moon system is at a distance from the Earth's centre of about:",
    place("4.68 × 10³ km, which is inside the Earth",
          ["4.74 × 10³ km, which is inside the Earth", "1.92 × 10⁵ km, midway between the two",
           "3.79 × 10⁵ km, close to the Moon"], "B"),
    "Centre of mass of a two-particle system",
    "Taking the Earth's centre as origin, X = m_M d/(M_E + m_M) = d/(81 + 1).",
    ["X = 3.84 × 10⁵/82 km ≈ 4.68 × 10³ km", "4680 km < 6400 km → the point lies inside the Earth"],
    why="4.74 × 10³ km divides by 81 instead of 82. The midpoint would need equal masses. 3.79 × 10⁵ km measures the "
        "distance with the masses interchanged.",
    ncert="Class 11 Physics, 'System of Particles and Rotational Motion', centre of mass", seconds=60, recomputed=True)

I_d, w_d, rev = 0.5, 20.0, 50
th_d = 2 * math.pi * rev
al_d = w_d ** 2 / (2 * th_d)
tau_d = I_d * al_d
assert close(al_d, 2 / math.pi) and close(tau_d, 1 / math.pi) and close(I_d * w_d ** 2 / (2 * rev), 2)
add(T, "Torque and angular momentum", "Intermediate", "numerical",
    "A disc of moment of inertia 0.5 kg m² about its axle rotates at 20 rad/s. A constant frictional torque brings "
    "it to rest after it has made 50 revolutions. The magnitude of the frictional torque is:",
    place("1/π N m", ["2/π N m", "2 N m", "1/(2π) N m"], "C"),
    "Rotational kinematics with τ = Iα",
    "First find the angular retardation from ω² = ω₀² − 2αθ, with θ in radians, then the torque from τ = Iα.",
    ["θ = 50 × 2π = 100π rad", "α = ω₀²/(2θ) = 400/(200π) = 2/π rad/s²", "τ = Iα = 0.5 × 2/π = 1/π N m ≈ 0.32 N m"],
    why="2/π N m is the angular retardation, not the torque. 2 N m uses 50 rad instead of 50 revolutions. 1/(2π) N m "
        "double-counts the factor 2π.",
    ncert="Class 11 Physics, 'System of Particles and Rotational Motion', dynamics of rotational motion about a fixed "
          "axis", seconds=75, recomputed=True)

Fx, Fy, mtot = 6.0, 3.0, 3.0
acm = math.hypot(Fx, Fy) / mtot
assert close(acm, math.sqrt(5)) and close(math.hypot(Fx, Fy), 3 * math.sqrt(5)) and close((Fx + Fy) / mtot, 3)
assert close(math.hypot(6 / 2, 1.5 / 2), 3.092, 1e-3)
add(T, "Centre of mass", "Intermediate", "numerical",
    "Two particles of masses 1 kg and 2 kg are acted on by external forces of 6î N and 3ĵ N respectively; no other "
    "forces act. The magnitude of the acceleration of their centre of mass is:",
    place("√5 m/s²", ["3 m/s²", "3√5 m/s²", "about 3.1 m/s²"], "D"),
    "Motion of the centre of mass",
    "The centre of mass moves as if the total mass were there and all the external forces acted on it: "
    "M a_cm = ΣF_ext.",
    ["ΣF = 6î + 3ĵ N, |ΣF| = √45 = 3√5 N", "a_cm = 3√5/3 = √5 m/s² ≈ 2.24 m/s²"],
    why="3 m/s² adds the magnitudes of perpendicular forces. 3√5 m/s² forgets to divide by the total mass. About "
        "3.1 m/s² averages the two particles' accelerations (6 and 1.5 m/s²) instead of weighting them by mass.",
    ncert="Class 11 Physics, 'System of Particles and Rotational Motion', motion of centre of mass", seconds=60,
    recomputed=True)

Id = {"axis": F(1, 2), "diam": F(1, 4)}
Id["tan_plane"] = Id["diam"] + 1
Id["rim_perp"] = Id["axis"] + 1
assert Id["tan_plane"] == F(5, 4) and Id["rim_perp"] == F(3, 2) and 2 * Id["diam"] == Id["axis"]
add(T, "Moment of inertia and axis theorems", "Intermediate", "match_list",
    match_stem("A uniform circular disc has mass M and radius R. Match List-I (axis) with List-II (moment of inertia "
               "of the disc about that axis).",
               ["Through the centre, perpendicular to the plane of the disc", "A diameter",
                "A tangent to the rim, lying in the plane of the disc",
                "Through a point on the rim, perpendicular to the plane of the disc"],
               ["5MR²/4", "MR²/2", "3MR²/2", "MR²/4"]),
    match_options({"A": "II", "B": "IV", "C": "I", "D": "III"},
                  [{"A": "II", "B": "IV", "C": "III", "D": "I"}, {"A": "IV", "B": "II", "C": "I", "D": "III"},
                   {"A": "II", "B": "I", "C": "IV", "D": "III"}], "A"),
    "Perpendicular and parallel axes theorems for a disc",
    "Start from I = MR²/2 about the central perpendicular axis. The perpendicular axes theorem gives each diameter "
    "half of this, and the parallel axes theorem adds MR² for an axis shifted by R.",
    ["A: MR²/2 (II)", "B: I_z = 2I_d → I_d = MR²/4 (IV)", "C: MR²/4 + MR² = 5MR²/4 (I)",
     "D: MR²/2 + MR² = 3MR²/2 (III)"],
    why="The other codes swap the tangent in the plane with the perpendicular axis through the rim, or the diameter "
        "with the central axis.",
    ncert="Class 11 Physics, 'System of Particles and Rotational Motion', theorems of perpendicular and parallel axes",
    seconds=60, recomputed=True)

add(T, "Rigid-body rotation", "Intermediate", "statement_pair",
    SP_STEM.format(
        s1="All the particles of a rigid body rotating about a fixed axis with a non-zero angular acceleration have "
           "the same tangential acceleration.",
        s2="Different particles of a rigid body rotating about a fixed axis have different angular accelerations."),
    sp("B"),
    "Angular and linear quantities in fixed-axis rotation",
    "In rotation about a fixed axis every particle turns through the same angle in the same time, so ω and α are the "
    "same for all particles. The tangential acceleration of a particle is a_t = rα, which grows with its distance r "
    "from the axis.",
    ["Statement I: a_t = rα differs with r → false", "Statement II: α is common to the whole body → false"],
    why="Both statements are false: the angular quantities are shared, the linear ones are not.",
    ncert="Class 11 Physics, 'System of Particles and Rotational Motion', angular velocity and its relation with "
          "linear velocity; angular acceleration", seconds=45)

Rw, Iw, tf = 0.4, 0.8, 4.0
ang_imp = Rw * (2 * tf ** 2 / 2)                  # ∫ R·2t dt from 0 to 4
w_f = ang_imp / Iw
assert close(ang_imp, 6.4) and close(w_f, 8) and close(Rw * 2 * tf ** 2 / Iw, 16) and close(2 * tf ** 2 / 2 / Iw, 20)
assert close(Rw * 2 * tf / Iw, 4)
add(T, "Torque and angular momentum", "Advanced", "numerical",
    "A wheel of radius 0.4 m and moment of inertia 0.8 kg m² about its fixed axle is at rest. A force acting "
    "tangentially at its rim varies with time as F = 2t, where F is in newtons and t in seconds. Neglecting "
    "friction, the angular velocity of the wheel at t = 4 s is:",
    place("8 rad/s", ["16 rad/s", "20 rad/s", "4 rad/s"], "C"),
    "Angular impulse equals change in angular momentum",
    "Since the torque varies with time, use τ = dL/dt and integrate: the change in angular momentum Iω equals "
    "∫τ dt = ∫RF dt.",
    ["τ = RF = 0.4 × 2t = 0.8t N m", "∫₀⁴ 0.8t dt = 0.4 × 16 = 6.4 kg m² s⁻¹", "ω = 6.4/0.8 = 8 rad/s"],
    why="16 rad/s takes the final force (8 N) as acting for the whole 4 s. 20 rad/s leaves out the radius in the "
        "torque. 4 rad/s is the angular acceleration at t = 4 s, not the angular velocity.",
    ncert="Class 11 Physics, 'System of Particles and Rotational Motion', torque and angular momentum", seconds=100,
    recomputed=True)

m1r, m2r, dr, Lr2 = 2.0, 3.0, 1.0, 6.0
mu_r = m1r * m2r / (m1r + m2r)
I_cm2 = mu_r * dr ** 2
K_rot = Lr2 ** 2 / (2 * I_cm2)
assert close(I_cm2, 1.2) and close(K_rot, 15) and close(Lr2 ** 2 / (2 * 3.0), 6) and close(Lr2 ** 2 / (2 * 1.25), 14.4)
assert close(Lr2 ** 2 / I_cm2, 30)
add(T, "Moment of inertia and axis theorems", "Advanced", "numerical",
    "Particles of masses 2 kg and 3 kg are fixed at the ends of a light rigid rod 1 m long. The system rotates about "
    "an axis perpendicular to the rod passing through its centre of mass, with an angular momentum of 6 kg m² s⁻¹ "
    "about this axis. Its rotational kinetic energy is:",
    place("15 J", ["6 J", "14.4 J", "30 J"], "D"),
    "Moment of inertia about the centre of mass; K = L²/(2I)",
    "First locate the centre of mass, then add mr² for the two particles about it. The kinetic energy follows from "
    "K = L²/(2I).",
    ["Centre of mass from the 2 kg mass: 3 × 1/5 = 0.6 m", "I = 2(0.6)² + 3(0.4)² = 0.72 + 0.48 = 1.2 kg m²",
     "K = 6²/(2 × 1.2) = 15 J"],
    shortcut="For two particles, I_cm = [m₁m₂/(m₁ + m₂)] d² = (6/5)(1)² = 1.2 kg m².",
    why="6 J takes the axis through the 2 kg mass (I = 3 kg m²). 14.4 J takes the axis through the midpoint of the "
        "rod (I = 1.25 kg m²). 30 J uses L²/I without the factor ½.",
    ncert="Class 11 Physics, 'System of Particles and Rotational Motion', moment of inertia and kinetic energy of "
          "rotation", seconds=100, recomputed=True)

pts = [(0, 0), (1, 0), (0, 1), (1, 1)]
I_x = sum(y ** 2 for x, y in pts)
I_y = sum(x ** 2 for x, y in pts)
I_z = sum(x ** 2 + y ** 2 for x, y in pts)
I_c = sum((x - 0.5) ** 2 + (y - 0.5) ** 2 for x, y in pts)
I_mid = sum((y - 0.5) ** 2 for x, y in pts)
assert I_x == 2 and I_y == 2 and I_z == 4 and close(I_c, 2) and close(I_mid, 1)
multi_key([I_x == 2, close(I_c, 2), I_z == 3, I_y == 2, close(I_mid, 1)], "abde")
add(T, "Moment of inertia and axis theorems", "Advanced", "multi_statement",
    multi("Four small particles, each of mass 1 kg, are fixed at the corners (0, 0), (1 m, 0), (0, 1 m) and "
          "(1 m, 1 m) of a light square frame lying in the x–y plane. Which of the following statements about the "
          "moment of inertia of the system are correct?",
          ["About the x-axis, it is 2 kg m².",
           "About the axis through the centre of the square, perpendicular to its plane, it is 2 kg m².",
           "About the z-axis (perpendicular to the plane, through the corner at the origin), it is 3 kg m².",
           "About the y-axis, it is 2 kg m².",
           "About the line y = 0.5 m in the plane of the square, it is 1 kg m²."]),
    place("(a), (b), (d) and (e) only", ["(a), (c) and (d) only", "(b), (c) and (e) only",
                                         "(a), (b), (c) and (d) only"], "B"),
    "Moment of inertia of a system of particles; axis theorems",
    "I = Σmr², with r the perpendicular distance of each particle from the axis. The perpendicular axes theorem "
    "(I_z = I_x + I_y) and the parallel axes theorem give useful checks.",
    ["(a) particles at y = 1 m: 1 + 1 = 2 kg m² (true)", "(b) each corner is √0.5 m from the centre: 4 × 0.5 = 2 "
     "kg m² (true)", "(c) 0 + 1 + 1 + 2 = 4 kg m², not 3 (false); check: I_z = I_x + I_y = 4",
     "(d) particles at x = 1 m: 2 kg m² (true)", "(e) each particle 0.5 m away: 4 × 0.25 = 1 kg m² (true)"],
    why="(c) leaves out the far corner, which is √2 m from the origin; any option with (c) is wrong.",
    ncert="Class 11 Physics, 'System of Particles and Rotational Motion', moment of inertia and the theorems of "
          "perpendicular and parallel axes", seconds=110, recomputed=True)

W_rod, L_rod, xC = 60.0, 2.0, 1.5
T_C = W_rod * 1.0 / xC
T_A = W_rod - T_C
assert close(T_C, 40) and close(T_A, 20)
TA_new = (W_rod * (xC - 1.0) - 60.0 * (L_rod - xC)) / xC
assert close(TA_new, 0)
multi_key([close(T_A + T_C, 60), close(T_C, 40), close(T_A, 30), T_A > T_C, close(TA_new, 0)], "abe")
add(T, "Equilibrium of rigid bodies", "Advanced", "multi_statement",
    multi("A uniform rod AB, 2 m long and of weight 60 N, hangs horizontally from two vertical strings, one tied at "
          "the end A and the other at a point C that is 0.5 m from the end B. Which of the following statements are "
          "correct?",
          ["The sum of the tensions in the two strings is 60 N.",
           "The tension in the string at C is 40 N.",
           "The tension in the string at A is 30 N.",
           "The tension in the string at A is greater than that in the string at C.",
           "If a 60 N weight is hung from the end B, the tension in the string at A becomes zero."]),
    place("(a), (b) and (e) only", ["(a), (c) and (d) only", "(b), (d) and (e) only",
                                    "(a), (b), (c) and (e) only"], "A"),
    "Conditions of equilibrium of a rigid body",
    "For equilibrium the net force and the net torque about any point must both be zero. The weight acts at the "
    "midpoint, 1 m from A, i.e. 0.5 m from C.",
    ["Forces: T_A + T_C = 60 N (a true)", "Torques about A: T_C × 1.5 = 60 × 1 → T_C = 40 N (b true)",
     "T_A = 20 N (c false; d false, since 20 < 40)",
     "With 60 N at B, torques about C: T_A × 1.5 = 60 × 0.5 − 60 × 0.5 = 0 → T_A = 0 (e true)"],
    why="(c) shares the weight equally, as if C were at B; (d) is false because C is nearer the centre of gravity.",
    ncert="Class 11 Physics, 'System of Particles and Rotational Motion', equilibrium of a rigid body", seconds=110,
    recomputed=True)


# =====================================================================================================================
# Gravitation (B3 I3 A2)
# =====================================================================================================================
T = "Gravitation"

W0 = 72.0
W_h = W0 / (1 + 0.5) ** 2
assert close(W_h, 32) and close(W0 / 1.5, 48) and close(W0 / 4, 18)
add(T, "Variation of g", "Basic", "numerical",
    "A body weighs 72 N on the surface of the Earth. Ignoring the Earth's rotation, its weight at a height equal to "
    "half the radius of the Earth above the surface is:",
    place("32 N", ["48 N", "18 N", "36 N"], "C"),
    "Acceleration due to gravity above the surface",
    "Above the surface, g(h) = GM/(R + h)² = g R²/(R + h)². The weight changes in the same ratio.",
    ["g(h)/g = [R/(R + R/2)]² = (2/3)² = 4/9", "Weight = 72 × 4/9 = 32 N"],
    why="48 N uses the first power of R/(R + h). 18 N takes the height as R. 36 N simply halves the weight.",
    ncert="Class 11 Physics, 'Gravitation', acceleration due to gravity above the surface of the Earth", seconds=40,
    recomputed=True)

G_ = 6.67e-11
R_E = 6.4e6
M_E = g * R_E ** 2 / G_
assert close(M_E, 6.14e24, 2e-3) and close(g * R_E / G_, 9.6e17, 2e-3) and close(g * 6400 ** 2 / G_, 6.14e18, 2e-3)
assert close(R_E ** 2 / (G_ * g), 6.14e22, 2e-3)
add(T, "Law of gravitation", "Basic", "numerical",
    "Taking the acceleration due to gravity at the Earth's surface as 10 m/s², the radius of the Earth as 6400 km "
    "and G = 6.67 × 10⁻¹¹ N m² kg⁻², and ignoring the Earth's rotation, the mass of the Earth is about:",
    place("6.1 × 10²⁴ kg", ["9.6 × 10¹⁷ kg", "6.1 × 10¹⁸ kg", "6.1 × 10²² kg"], "A"),
    "Weighing the Earth with g = GM/R²",
    "The weight of a body at the surface is the gravitational force of the Earth on it: mg = GMm/R², so M = gR²/G.",
    ["M = gR²/G = 10 × (6.4 × 10⁶)²/(6.67 × 10⁻¹¹)", "= 10 × 4.096 × 10¹³/(6.67 × 10⁻¹¹) ≈ 6.1 × 10²⁴ kg"],
    why="9.6 × 10¹⁷ kg uses R instead of R². 6.1 × 10¹⁸ kg leaves the radius in kilometres. 6.1 × 10²² kg divides by "
        "g instead of multiplying.",
    ncert="Class 11 Physics, 'Gravitation', acceleration due to gravity of the Earth", seconds=50, recomputed=True)

add(T, "Law of gravitation", "Basic", "direct",
    "The gravitational field intensity at a point is expressed in N kg⁻¹. This unit is equivalent to:",
    place("m s⁻²", ["J kg⁻¹", "N m² kg⁻²", "kg m s⁻²"], "B"),
    "Gravitational field intensity is force per unit mass",
    "Field intensity = force/mass, and 1 N = 1 kg m s⁻², so N kg⁻¹ = m s⁻². The field intensity at a point equals the "
    "acceleration that gravity gives a body placed there.",
    ["1 N kg⁻¹ = (1 kg m s⁻²)/(1 kg) = 1 m s⁻²"],
    why="J kg⁻¹ is the unit of gravitational potential. N m² kg⁻² is the unit of G. kg m s⁻² is the newton itself.",
    ncert="Class 11 Physics, 'Gravitation', acceleration due to gravity of the Earth", seconds=25)

h_s = 100.0
d_s = 2 * h_s
assert d_s == 200
add(T, "Variation of g", "Intermediate", "numerical",
    "Treat the Earth as a uniform sphere and ignore its rotation. The acceleration due to gravity at a height of "
    "100 km above the surface (small compared with the Earth's radius) is equal to its value at a depth d below the "
    "surface. The depth d is about:",
    place("200 km", ["100 km", "50 km", "400 km"], "D"),
    "Variation of g with small height and with depth",
    "For h ≪ R, g(h) ≈ g(1 − 2h/R). At depth d, g(d) = g(1 − d/R) exactly for a uniform sphere.",
    ["g(1 − 2h/R) = g(1 − d/R)", "d = 2h = 200 km"],
    why="100 km assumes g falls equally fast above and below the surface. 50 km and 400 km halve or double the "
        "correct factor of 2.",
    ncert="Class 11 Physics, 'Gravitation', acceleration due to gravity below and above the surface of the Earth",
    seconds=45, recomputed=True)

add(T, "Law of gravitation", "Intermediate", "assertion_reason",
    AR_STEM.format(
        a="The gravitational force exerted by the Earth on the Sun is much smaller than the gravitational force "
          "exerted by the Sun on the Earth, because the Earth's mass is much smaller.",
        r="The gravitational forces that two bodies exert on each other are equal in magnitude and opposite in "
          "direction."),
    ar("D"),
    "Gravitational forces form an action–reaction pair",
    "Newton's law of gravitation gives a force of magnitude Gm₁m₂/r² on each body, a symmetric expression, and the "
    "two forces are a third-law pair. The Earth's smaller mass makes its acceleration larger, not the force on it "
    "larger.",
    ["F(Sun on Earth) = F(Earth on Sun) = GMm/r² → A false", "Equal and opposite forces → R true"],
    why="A is false, so options A, B and C (which need A true) are wrong.",
    ncert="Class 11 Physics, 'Gravitation', universal law of gravitation", seconds=40)

add(T, "Variation of g", "Intermediate", "statement_pair",
    SP_STEM.format(
        s1="Treating the Earth as a sphere of uniform density, the acceleration due to gravity inside it increases "
           "linearly with distance from its centre.",
        s2="A uniform thin spherical shell attracts a point mass outside it as if the whole mass of the shell were "
           "concentrated at its centre."),
    sp("A"),
    "Gravity of spherical mass distributions",
    "At distance r inside a uniform sphere, only the mass within radius r attracts: M(r) = M r³/R³, so "
    "g(r) = GM(r)/r² = (GM/R³) r, which is proportional to r. For a point outside a uniform shell, the shell acts like "
    "a point mass at its centre (the shell theorem used in NCERT).",
    ["Statement I: g(r) = gr/R inside → linear in r (true)", "Statement II: shell theorem for outside points (true)"],
    why="Both statements are true, so options B, C and D are wrong.",
    ncert="Class 11 Physics, 'Gravitation', acceleration due to gravity below the surface of the Earth", seconds=45)

Vv = lambda: -1 / F(1, 2) - F(1)          # in units of GM/R, point mass M at centre + shell M, at r = R/2
Ef = 1 / F(1, 2) ** 2                     # in units of GM/R^2
assert Vv() == -3 and Ef == 4 and -1 / F(1, 2) == -2 and -2 / F(1, 2) == -4 and 2 / F(1, 2) ** 2 == 8
add(T, "Gravitational potential and energy", "Advanced", "numerical",
    "A point mass M is placed at the centre of a thin uniform spherical shell of mass M and radius R. Taking the "
    "gravitational potential to be zero at infinity, the gravitational potential and the magnitude of the "
    "gravitational field at a distance R/2 from the centre are respectively (G is the universal gravitational "
    "constant):",
    place("−3GM/R and 4GM/R²", ["−3GM/R and 8GM/R²", "−2GM/R and 4GM/R²", "−4GM/R and 8GM/R²"], "C"),
    "Superposition of potentials and fields; shell inside points",
    "Potentials add as scalars. Inside a uniform shell the shell's field is zero but its potential is not: it is "
    "constant and equal to its surface value −GM/R. The point mass contributes −GM/r and GM/r².",
    ["Potential: −GM/(R/2) + (−GM/R) = −2GM/R − GM/R = −3GM/R",
     "Field: point mass only → GM/(R/2)² = 4GM/R²; shell gives zero inside"],
    why="8GM/R² treats the shell as if its mass were at the centre for the field too. −2GM/R forgets the shell's "
        "constant potential inside it. −4GM/R and 8GM/R² treat the shell as a point mass at the centre for both "
        "quantities.",
    ncert="Class 11 Physics, 'Gravitation', gravitational potential energy and the field of a spherical shell",
    seconds=100, recomputed=True)

rA, rB = 2.0, 18.0
q = rB / rA
assert close(math.sqrt(q), 3) and close(q ** 1.5, 27) and close(q ** 2, 81) and close(q, 9) and close(math.sqrt(1 / q), 1 / 3)
multi_key([close(math.sqrt(q), 3), close(q ** 1.5, 27), close(q ** 2, 81), close(q, 9), close(math.sqrt(q), 1 / 3)],
          "abcd")
add(T, "Satellite energy and period", "Advanced", "multi_statement",
    multi("Two satellites A and B of equal mass revolve round the Earth in circular orbits of radii 2R and 18R, where "
          "R is the radius of the Earth. Which of the following statements are correct?",
          ["The orbital speed of A is 3 times that of B.",
           "The period of B is 27 times that of A.",
           "The centripetal acceleration of A is 81 times that of B.",
           "The kinetic energy of A is 9 times that of B.",
           "The angular momentum of A about the Earth's centre is 3 times that of B."]),
    place("(a), (b), (c) and (d) only", ["(a), (b) and (e) only", "(b), (c), (d) and (e) only",
                                         "(a), (c) and (e) only"], "B"),
    "Scaling of orbital quantities with radius",
    "For a circular orbit of radius r: v = √(GM/r), T = 2π√(r³/GM), a = GM/r², K = GMm/(2r) and L = mvr = "
    "m√(GMr). With r_B/r_A = 9 each ratio follows.",
    ["(a) v ∝ r^(−1/2): v_A/v_B = √9 = 3 (true)", "(b) T ∝ r^(3/2): T_B/T_A = 9^(3/2) = 27 (true)",
     "(c) a ∝ r⁻²: a_A/a_B = 81 (true)", "(d) K ∝ 1/r: K_A/K_B = 9 (true)",
     "(e) L ∝ √r: L_A/L_B = 1/3, not 3 (false)"],
    why="(e) inverts the ratio: the outer satellite moves more slowly, but its larger radius gives it the larger "
        "angular momentum.",
    ncert="Class 11 Physics, 'Gravitation', earth satellites and energy of an orbiting satellite", seconds=110,
    recomputed=True)


# =====================================================================================================================
# Properties of Solids and Liquids (B4 I6 A5)
# =====================================================================================================================
T = "Properties of Solids and Liquids"

tc = F(-160, 4)                                   # C = 9C/5 + 32 → -4C/5 = 32 → C = -40
assert tc == -40 and F(9, 5) * tc + 32 == tc and F(5, 9) * (0 - 32) == F(-160, 9)
add(T, "Thermal expansion and calorimetry", "Basic", "numerical",
    "The temperature at which a Celsius thermometer and a Fahrenheit thermometer show the same numerical reading "
    "is:",
    place("−40 °C", ["40 °C", "0 °C", "about −17.8 °C"], "D"),
    "Relation between the Celsius and Fahrenheit scales",
    "The two scales are related by t_F = (9/5)t_C + 32. Setting t_F = t_C gives the common reading.",
    ["t = (9/5)t + 32", "−(4/5)t = 32 → t = −40", "So −40 °C = −40 °F"],
    why="40 °C has the wrong sign (40 °C = 104 °F). 0 °C corresponds to 32 °F. About −17.8 °C is the "
        "Celsius temperature at which the Fahrenheit reading is zero, not equal.",
    ncert="Class 11 Physics, 'Thermal Properties of Matter', measurement of temperature", seconds=35, recomputed=True)

rho_w, rho_o, depth, Pa = 1000.0, 800.0, 5.0, 1.0e5
pg = rho_w * g * depth
assert pg == 5e4 and Pa + pg == 1.5e5 and rho_o * g * depth == 4e4
add(T, "Fluid pressure and Pascal's law", "Basic", "match_list",
    match_stem("Take g = 10 m/s², the density of water as 1000 kg/m³ and the atmospheric pressure as 1.0 × 10⁵ Pa. "
               "The liquids are at rest in open containers. Match List-I (quantity) with List-II (its value).",
               ["Gauge pressure at a depth of 5 m in water",
                "Absolute pressure at a depth of 5 m in water",
                "Difference in pressure between two points at the same depth of 5 m in the same water",
                "Gauge pressure at a depth of 5 m in a liquid of density 800 kg/m³"],
               ["4.0 × 10⁴ Pa", "Zero", "1.5 × 10⁵ Pa", "5.0 × 10⁴ Pa"]),
    match_options({"A": "IV", "B": "III", "C": "II", "D": "I"},
                  [{"A": "III", "B": "IV", "C": "II", "D": "I"}, {"A": "IV", "B": "III", "C": "I", "D": "II"},
                   {"A": "I", "B": "III", "C": "II", "D": "IV"}], "B"),
    "Pressure at a depth in a liquid at rest",
    "The pressure at depth h is P = Pₐ + ρgh; the gauge pressure is the excess ρgh over atmospheric pressure. Points "
    "at the same depth in the same liquid at rest are at the same pressure.",
    ["A: 1000 × 10 × 5 = 5.0 × 10⁴ Pa (IV)", "B: 1.0 × 10⁵ + 5.0 × 10⁴ = 1.5 × 10⁵ Pa (III)",
     "C: same depth → same pressure → zero (II)", "D: 800 × 10 × 5 = 4.0 × 10⁴ Pa (I)"],
    why="The other codes interchange gauge and absolute pressure, or the water and the lighter liquid.",
    ncert="Class 11 Physics, 'Mechanical Properties of Fluids', pressure (variation of pressure with depth; gauge "
          "pressure)", seconds=50, recomputed=True)

add(T, "Viscosity and Stokes' law", "Basic", "direct",
    "A small steel ball falls through a long column of glycerine. It attains its terminal velocity when:",
    place("The viscous drag and the buoyant force together balance its weight, so the net force on it is zero",
          ["The viscous drag on it becomes zero", "Its acceleration becomes equal to g",
           "The buoyant force alone becomes equal to its weight"], "A"),
    "Terminal velocity",
    "The viscous drag 6πηrv grows with speed. When the drag plus the upthrust equals the weight, the net force and "
    "hence the acceleration become zero, and the ball falls at constant (terminal) velocity.",
    ["Weight = buoyant force + 6πηrv_t → net force zero → constant velocity"],
    why="The drag is largest, not zero, at terminal velocity. Acceleration g occurs only at the start, when there is "
        "no drag (and ignoring upthrust). The upthrust alone is smaller than the weight of a steel ball.",
    ncert="Class 11 Physics, 'Mechanical Properties of Fluids', viscosity (Stokes' law and terminal velocity)",
    seconds=30)

add(T, "Fluid pressure and Pascal's law", "Basic", "assertion_reason",
    AR_STEM.format(
        a="The wall of a dam is made much thicker at the bottom than at the top.",
        r="The pressure exerted by water at rest increases with depth below its free surface."),
    ar("A"),
    "Variation of pressure with depth",
    "The pressure at depth h exceeds the surface pressure by ρgh. The lower part of the dam wall therefore has to "
    "withstand a much larger pressure, so it is built thicker.",
    ["P = Pₐ + ρgh grows linearly with depth", "Greatest pressure at the base → thickest wall there"],
    why="R gives the very reason for the thicker base, so B is wrong; both are true, so C and D are wrong.",
    ncert="Class 11 Physics, 'Mechanical Properties of Fluids', variation of pressure with depth", seconds=30)

alpha_s, L_read, dT = 1.2e-5, 50.00, 25.0
L_true = L_read * (1 + alpha_s * dT)
assert close(L_true, 50.015, 1e-6) and close(L_read * (1 - alpha_s * dT), 49.985, 1e-6) \
    and close(L_read * (1 + 2 * alpha_s * dT), 50.030, 1e-6)
add(T, "Thermal expansion and calorimetry", "Intermediate", "numerical",
    "A steel metre scale is correctly graduated at 20 °C. At 45 °C it is used to measure the length of a rod, and "
    "the reading is 50.00 cm. The coefficient of linear expansion of steel is 1.2 × 10⁻⁵ °C⁻¹. The actual length of "
    "the rod at 45 °C is:",
    place("50.015 cm", ["49.985 cm", "50.000 cm", "50.030 cm"], "C"),
    "Expansion of a measuring scale",
    "At 45 °C each centimetre division of the steel scale has expanded to (1 + αΔT) cm. A reading of 50.00 "
    "divisions therefore corresponds to a true length of 50.00(1 + αΔT) cm.",
    ["Each division = 1 + 1.2 × 10⁻⁵ × 25 = 1.0003 cm", "True length = 50.00 × 1.0003 = 50.015 cm"],
    why="49.985 cm corrects in the wrong direction: an expanded scale reads too low, not too high. 50.000 cm "
        "ignores the expansion of the scale. 50.030 cm uses 2α.",
    ncert="Class 11 Physics, 'Thermal Properties of Matter', thermal expansion", seconds=60, recomputed=True)

add(T, "Surface tension and capillarity", "Intermediate", "match_list",
    match_stem("Match List-I (quantity) with List-II (its expression). S is the surface tension, r a radius, θ the "
               "angle of contact, ρ and σ densities, η the coefficient of viscosity and g the acceleration due to "
               "gravity.",
               ["Excess pressure inside a liquid drop of radius r",
                "Excess pressure inside a soap bubble of radius r, in air",
                "Height of rise of a liquid of density ρ in a capillary tube of radius r",
                "Terminal velocity of a small sphere of radius r and density ρ falling through a fluid of density σ"],
               ["2r²(ρ − σ)g/(9η)", "4S/r", "2S/r", "2S cos θ/(ρgr)"]),
    match_options({"A": "III", "B": "II", "C": "IV", "D": "I"},
                  [{"A": "II", "B": "III", "C": "IV", "D": "I"}, {"A": "III", "B": "II", "C": "I", "D": "IV"},
                   {"A": "IV", "B": "II", "C": "III", "D": "I"}], "D"),
    "Standard results of surface tension and viscosity",
    "A drop has one liquid surface (excess pressure 2S/r); a soap bubble has two surfaces (4S/r). Capillary rise "
    "comes from balancing the surface tension force with the weight of the raised column. Terminal velocity comes "
    "from Stokes' law with the upthrust included.",
    ["Drop: 2S/r (III)", "Soap bubble: 4S/r (II)", "Capillary rise: h = 2S cos θ/(ρgr) (IV)",
     "Terminal velocity: v = 2r²(ρ − σ)g/(9η) (I)"],
    why="The other codes swap the drop and the bubble (one surface versus two) or the capillary rise and the "
        "terminal velocity.",
    ncert="Class 11 Physics, 'Mechanical Properties of Fluids', surface tension and viscosity", seconds=60)

add(T, "Heat transfer", "Intermediate", "statement_pair",
    SP_STEM.format(
        s1="When two rods of different thermal conductivities are joined end to end and conduct heat in the steady "
           "state, with their sides insulated, the rate of heat flow is greater through the rod of higher "
           "conductivity.",
        s2="In the steady state, the rate of heat flow through a rod of a given material, with given temperatures "
           "at its ends, increases when the length of the rod is increased."),
    sp("B"),
    "Steady-state conduction, H = KA(T₁ − T₂)/L",
    "In the steady state no heat accumulates at the junction, so the same heat current flows through both rods in "
    "series; the better conductor simply has a smaller temperature drop across it. For a single rod, H = KA(T₁ − "
    "T₂)/L falls as the length increases.",
    ["Statement I: series rods carry the same heat current → false", "Statement II: H ∝ 1/L → false"],
    why="Both statements are false, so A, C and D are wrong.",
    ncert="Class 11 Physics, 'Thermal Properties of Matter', heat transfer (conduction)", seconds=50)

c_pb, dT_pb, L_pb = 125.0, 300.0, 2.5e4
v_pb = math.sqrt(2 * (c_pb * dT_pb + L_pb))
assert close(v_pb, 353.55) and close(math.sqrt(2 * c_pb * dT_pb), 273.86) and close(math.sqrt(c_pb * dT_pb + L_pb), 250) \
    and close(math.sqrt(2 * L_pb), 223.6)
add(T, "Thermal expansion and calorimetry", "Intermediate", "numerical",
    "A lead bullet at 27 °C strikes a rigid target and just melts completely. Assume that all its kinetic energy "
    "becomes heat that stays in the bullet. For lead, the specific heat capacity is 125 J kg⁻¹ K⁻¹, the melting "
    "point is 327 °C and the latent heat of fusion is 2.5 × 10⁴ J kg⁻¹. The speed of the bullet just before impact "
    "is about:",
    place("354 m/s", ["274 m/s", "250 m/s", "224 m/s"], "C"),
    "Energy conservation with heating and change of state",
    "Per kilogram, the kinetic energy ½v² must raise the bullet from 27 °C to 327 °C and then melt it at 327 °C.",
    ["Heat per kg = cΔT + L = 125 × 300 + 2.5 × 10⁴ = 62 500 J/kg", "½v² = 62 500 → v² = 125 000 → v ≈ 354 m/s"],
    why="274 m/s leaves out the latent heat. 250 m/s forgets the ½ in the kinetic energy. 224 m/s uses only the "
        "latent heat and ignores warming the bullet up to its melting point.",
    ncert="Class 11 Physics, 'Thermal Properties of Matter', calorimetry and change of state (latent heat)",
    seconds=80, recomputed=True)

add(T, "Bernoulli's principle", "Intermediate", "direct",
    "Water flows out through a small hole in the side of a wide open tank, at a depth h below the water surface. If "
    "the water is replaced by mercury filled to the same level, the speed of efflux from the hole:",
    place("Remains the same", ["Decreases by a factor of √13.6", "Increases by a factor of 13.6",
                               "Decreases by a factor of 13.6"], "B"),
    "Torricelli's law",
    "From Bernoulli's equation, the speed of efflux is v = √(2gh): equal to the speed of a body falling freely "
    "through h. The density appears on both sides of the equation (in ρgh and ½ρv²) and cancels.",
    ["Pₐ + ρgh = Pₐ + ½ρv² → v = √(2gh), independent of ρ"],
    why="The other options assume the speed depends on density. A denser liquid has a larger pressure at the hole "
        "but also more mass to accelerate, and the two effects cancel.",
    ncert="Class 11 Physics, 'Mechanical Properties of Fluids', Bernoulli's principle (speed of efflux: "
          "Torricelli's law)", seconds=35)

Fr = lambda r: r * r ** 2                          # drag at terminal velocity ∝ r × v_t, v_t ∝ r²
assert Fr(2) / Fr(1) == 8 and (2 * 2) == 4
add(T, "Viscosity and Stokes' law", "Intermediate", "numerical",
    "A small sphere falling through a viscous liquid reaches a terminal velocity at which the viscous force on it is "
    "F. A second sphere of the same material, but of twice the radius, falls through the same liquid. Assuming "
    "Stokes' law holds, the viscous force on the second sphere at its terminal velocity is:",
    place("8F", ["4F", "2F", "16F"], "A"),
    "Viscous drag at terminal velocity",
    "At terminal velocity the drag balances the weight minus the upthrust, both proportional to r³. Equivalently, "
    "F = 6πηrv_t with v_t ∝ r², so F ∝ r³.",
    ["v_t ∝ r² → doubles radius → 4 × v_t", "F = 6πηr v_t ∝ r × r² = r³ → 8F"],
    why="4F takes only the change in terminal velocity. 2F takes only the factor r in 6πηrv and forgets that v_t "
        "changes. 16F multiplies r² by r².",
    ncert="Class 11 Physics, 'Mechanical Properties of Fluids', viscosity (Stokes' law)", seconds=60, recomputed=True)

h_ratio = (1 / F(1, 2)) * F(1, 2)                 # h ∝ 1/(r g_eff): r → r/2, g_eff → 2g
assert h_ratio == 1
add(T, "Surface tension and capillarity", "Advanced", "numerical",
    "Water rises to a height h in a clean glass capillary tube of radius r when the tube stands in a vessel at rest "
    "on the ground. A capillary tube of radius r/2, of the same glass, is placed in the same water inside a lift "
    "that is accelerating upward with acceleration g. The height to which the water rises in it is:",
    place("h", ["2h", "4h", "h/2"], "D"),
    "Capillary rise in an accelerating frame",
    "h = 2S cos θ/(ρ g_eff r). Halving the radius doubles the rise, but in a lift accelerating upward at g the "
    "effective gravity is g + g = 2g, which halves it again.",
    ["h' = 2S cos θ/(ρ(2g)(r/2)) = 2S cos θ/(ρgr) = h"],
    why="2h ignores the lift's acceleration. 4h treats the effective gravity as g/2. h/2 ignores the change in "
        "radius.",
    ncert="Class 11 Physics, 'Mechanical Properties of Fluids', surface tension (capillary rise)", seconds=80,
    recomputed=True)

v1b, v2b, hb = 1.0, 2.0, 2.0
dP = 0.5 * rho_w * (v2b ** 2 - v1b ** 2) + rho_w * g * hb
assert close(dP, 21500) and close(rho_w * g * hb, 2e4) and close(0.5 * rho_w * (v2b ** 2 - v1b ** 2), 1500) \
    and close(rho_w * g * hb - 1500, 18500)
add(T, "Bernoulli's principle", "Advanced", "numerical",
    "Water flows steadily through a pipe that rises as it goes. At a lower section the water moves at 1 m/s; at an "
    "upper section, 2 m higher, the cross-sectional area of the pipe is half that of the lower section. Treating "
    "water as non-viscous and incompressible (density 1000 kg/m³) and taking g = 10 m/s², the pressure at the lower "
    "section exceeds that at the upper section by:",
    place("2.15 × 10⁴ Pa", ["2.0 × 10⁴ Pa", "1.5 × 10³ Pa", "1.85 × 10⁴ Pa"], "B"),
    "Equation of continuity with Bernoulli's equation",
    "Continuity (Av constant) gives the speed in the narrow upper section. Bernoulli's equation then balances "
    "pressure, kinetic energy per unit volume and potential energy per unit volume between the two sections.",
    ["v₂ = v₁ A₁/A₂ = 2 m/s", "P₁ − P₂ = ½ρ(v₂² − v₁²) + ρgh",
     "= ½ × 1000 × (4 − 1) + 1000 × 10 × 2 = 1500 + 20 000 = 2.15 × 10⁴ Pa"],
    why="2.0 × 10⁴ Pa ignores the change in speed. 1.5 × 10³ Pa ignores the rise in height. 1.85 × 10⁴ Pa subtracts "
        "the kinetic term instead of adding it.",
    ncert="Class 11 Physics, 'Mechanical Properties of Fluids', streamline flow and Bernoulli's principle",
    seconds=100, recomputed=True)

mw, tw, mi, ti, ci, Lf = 100, 20, 100, -20, F(1, 2), 80
q_avail = mw * 1 * tw
q_warm = mi * ci * (0 - ti)
melted = F(q_avail - q_warm, Lf)
assert q_avail == 2000 and q_warm == 1000 and melted == F(25, 2) and F(q_avail, Lf) == 25
add(T, "Thermal expansion and calorimetry", "Advanced", "numerical",
    "100 g of water at 20 °C and 100 g of ice at −20 °C are mixed in an insulated container of negligible heat "
    "capacity. Take the specific heat capacity of water as 1 cal g⁻¹ °C⁻¹, that of ice as 0.5 cal g⁻¹ °C⁻¹ and the "
    "latent heat of fusion of ice as 80 cal g⁻¹. When equilibrium is reached:",
    place("The temperature is 0 °C and 12.5 g of the ice has melted",
          ["The temperature is 0 °C and 25 g of the ice has melted",
           "The temperature is 0 °C and none of the ice has melted",
           "All the ice has melted and the temperature is above 0 °C"], "C"),
    "Calorimetry with partial melting",
    "First compare the heat the water can give out in cooling to 0 °C with the heat the ice needs to warm up to "
    "0 °C. Any heat left over melts ice at 0 °C; if it cannot melt all the ice, the mixture stays at 0 °C.",
    ["Water 20 → 0 °C gives 100 × 1 × 20 = 2000 cal", "Ice −20 → 0 °C needs 100 × 0.5 × 20 = 1000 cal",
     "Remaining 1000 cal melts 1000/80 = 12.5 g of ice", "Final state: 0 °C, 112.5 g water and 87.5 g ice"],
    why="25 g forgets the heat needed to warm the ice to 0 °C. 'None melted' assumes the warming uses up all the "
        "heat. Melting all 100 g would need 8000 cal more than is available.",
    ncert="Class 11 Physics, 'Thermal Properties of Matter', calorimetry and change of state", seconds=110,
    recomputed=True)

multi_key([True, True, True, False, True], "abce")
add(T, "Heat transfer", "Advanced", "multi_statement",
    multi("Which of the following statements about the modes of heat transfer are correct?",
          ["In conduction, heat passes between neighbouring parts of a body without any bulk motion of the material.",
           "In natural convection, gravity plays an essential part: the warmer, less dense fluid rises and the "
           "cooler, denser fluid sinks.",
           "In forced convection, the fluid is made to move by a pump, a fan or some other physical means.",
           "Heat can be transferred through a vacuum by conduction but not by radiation.",
           "Gases are poor conductors of heat compared with metals."]),
    place("(a), (b), (c) and (e) only", ["(a), (b) and (d) only", "(b), (c), (d) and (e) only",
                                         "(a), (c) and (d) only"], "D"),
    "Conduction, convection and radiation",
    "Conduction passes energy between adjacent parts by molecular collisions (and free electrons in metals) without "
    "bulk flow. Convection needs bulk flow of a fluid: natural convection is driven by buoyancy, which needs gravity, "
    "and forced convection by a pump or fan. Radiation needs no medium; conduction does.",
    ["(a) true", "(b) true", "(c) true", "(d) false: it is the other way round", "(e) true"],
    why="Every option except D includes the false statement (d).",
    ncert="Class 11 Physics, 'Thermal Properties of Matter', heat transfer (conduction, convection, radiation)",
    seconds=70, recomputed=True)

ext = lambda L, A: F(L) / F(A)
assert ext(F(1, 2), 2) / ext(1, 1) == F(1, 4) and ext(F(1, 2), 1) / ext(1, 1) == F(1, 2)
add(T, "Elasticity and moduli", "Advanced", "numerical",
    "A load W hung from a uniform wire of length L stretches it by x. The same wire is folded at its middle into "
    "two equal strands, each of length L/2, and the same load W is hung from the folded wire so that it is shared "
    "equally by the two strands. Within the elastic limit, the extension now is:",
    place("x/4", ["x/2", "x", "2x"], "A"),
    "Extension of a wire, ΔL = WL/(AY)",
    "Folding halves the length of wire that is stretched and doubles the cross-sectional area that carries the load "
    "(each strand carries W/2). Both changes reduce the extension.",
    ["ΔL = WL/(AY)", "Folded: ΔL' = W(L/2)/((2A)Y) = (1/4)WL/(AY) = x/4"],
    why="x/2 accounts for only one of the two changes (length or area). x assumes no change. 2x doubles instead of "
        "halving.",
    ncert="Class 11 Physics, 'Mechanical Properties of Solids', Young's modulus", seconds=70, recomputed=True)


# =====================================================================================================================
# Thermodynamics (B2 I3 A2)
# =====================================================================================================================
T = "Thermodynamics"
R_ = 8.3

add(T, "Zeroth and first law", "Basic", "direct",
    "In the first law of thermodynamics written as ΔQ = ΔU + ΔW, as in NCERT, the quantities ΔQ and ΔW are taken as "
    "positive when:",
    place("Heat is supplied to the system, and work is done by the system on its surroundings",
          ["Heat is given out by the system, and work is done by the system on its surroundings",
           "Heat is supplied to the system, and work is done on the system by its surroundings",
           "Heat is given out by the system, and work is done on the system by its surroundings"], "C"),
    "Sign convention in the first law",
    "ΔQ is the heat supplied to the system and ΔW the work done by the system. Heat supplied either raises the "
    "internal energy or is used by the system to do work on its surroundings.",
    ["ΔQ > 0: heat flows into the system", "ΔW > 0: the system does work (for example, a gas expands)"],
    why="The other options reverse the sign convention for heat, for work, or for both.",
    ncert="Class 11 Physics, 'Thermodynamics', first law of thermodynamics", seconds=30)

Qv = 5 * 2.5 * R_ * 20
assert close(Qv, 2075) and close(5 * 3.5 * R_ * 20, 2905) and close(5 * 1.5 * R_ * 20, 1245) and close(5 * R_ * 20, 830)
add(T, "Zeroth and first law", "Basic", "numerical",
    "Five moles of an ideal diatomic gas, whose molecules are rigid (no vibration), are heated in a closed rigid "
    "vessel so that the temperature rises by 20 K. Taking R = 8.3 J mol⁻¹ K⁻¹, the heat supplied to the gas is:",
    place("2075 J", ["2905 J", "1245 J", "830 J"], "B"),
    "Heat at constant volume, Q = nC_vΔT",
    "In a rigid vessel no work is done, so all the heat goes into internal energy. For a rigid diatomic gas "
    "C_v = (5/2)R.",
    ["Q = nC_vΔT = 5 × (5/2) × 8.3 × 20", "= 2075 J"],
    why="2905 J uses C_p = 7R/2, which applies at constant pressure. 1245 J uses the monatomic value 3R/2. 830 J "
        "uses R alone.",
    ncert="Class 11 Physics, 'Thermodynamics', specific heat capacity; first law of thermodynamics", seconds=40,
    recomputed=True)

Qp, P_c, dV = 250.0, 1.0e5, 1.0e-3
W_c = P_c * dV
dU_c = Qp - W_c
gam = F(int(Qp), int(dU_c))
assert W_c == 100 and dU_c == 150 and gam == F(5, 3)
add(T, "Zeroth and first law", "Intermediate", "numerical",
    "An ideal gas absorbs 250 J of heat while it expands at a constant pressure of 1.0 × 10⁵ Pa from a volume of "
    "1 L to 2 L. The increase in its internal energy and the ratio of its specific heats γ = C_p/C_v are "
    "respectively:",
    place("150 J and 5/3", ["350 J and 5/7", "150 J and 3/5", "150 J and 7/5"], "D"),
    "First law at constant pressure; Q = nC_pΔT and ΔU = nC_vΔT",
    "The work done by the gas is PΔV. The first law gives ΔU. At constant pressure the heat is nC_pΔT and the "
    "change in internal energy is nC_vΔT, so their ratio is γ.",
    ["W = 1.0 × 10⁵ × 1 × 10⁻³ = 100 J", "ΔU = 250 − 100 = 150 J", "γ = Q/ΔU = 250/150 = 5/3 (a monatomic gas)"],
    why="350 J adds the work to the heat (wrong sign), giving 5/7. 3/5 is ΔU/Q, the inverse of γ. 7/5 assumes a "
        "diatomic gas without using the data.",
    ncert="Class 11 Physics, 'Thermodynamics', first law of thermodynamics and specific heat capacity", seconds=70,
    recomputed=True)

gamma_d = F(7, 5)
P0, V0 = F(3), F(2)
iso = -P0 / V0
adi = -gamma_d * P0 / V0
assert adi / iso == F(7, 5)
add(T, "Isothermal and adiabatic processes", "Intermediate", "numerical",
    "On a P–V diagram, an isothermal curve and a reversible adiabatic curve of an ideal diatomic gas (rigid "
    "molecules, γ = 7/5) pass through the same point. The ratio of the slope of the adiabatic curve to that of the "
    "isothermal curve at that point is:",
    place("7/5", ["5/7", "1", "5/3"], "A"),
    "Slopes of isothermal and adiabatic curves",
    "Differentiate PV = constant and PV^γ = constant. The isothermal slope is dP/dV = −P/V and the adiabatic slope "
    "is dP/dV = −γP/V, so at the same point the adiabatic curve is steeper by the factor γ.",
    ["Isothermal: P dV + V dP = 0 → dP/dV = −P/V", "Adiabatic: γPV^(γ−1)dV + V^γ dP = 0 → dP/dV = −γP/V",
     "Ratio = γ = 7/5"],
    why="5/7 inverts the ratio; the adiabatic curve is the steeper one. 1 says the curves have equal slopes. 5/3 is "
        "γ for a monatomic gas.",
    ncert="Class 11 Physics, 'Thermodynamics', isothermal and adiabatic processes", seconds=60, recomputed=True)

fl = {"A": (100, 40), "B": (-50, -80), "C": (0, 50), "D": (120, 200)}
dUs = {k_: q_ - w_ for k_, (q_, w_) in fl.items()}
assert dUs == {"A": 60, "B": 30, "C": -50, "D": -80}
add(T, "Zeroth and first law", "Intermediate", "match_list",
    match_stem("For a closed system, Q is the heat supplied to the system and W the work done by the system. Match "
               "List-I (values of Q and W in one process) with List-II (the change ΔU in its internal energy).",
               ["Q = +100 J, W = +40 J", "Q = −50 J, W = −80 J", "Q = 0, W = +50 J", "Q = +120 J, W = +200 J"],
               ["−80 J", "+60 J", "−50 J", "+30 J"]),
    match_options({"A": "II", "B": "IV", "C": "III", "D": "I"},
                  [{"A": "II", "B": "III", "C": "IV", "D": "I"}, {"A": "IV", "B": "II", "C": "III", "D": "I"},
                   {"A": "II", "B": "IV", "C": "I", "D": "III"}], "C"),
    "Applying ΔU = Q − W with signs",
    "With heat supplied to the system and work done by it both counted as positive, ΔU = Q − W.",
    ["A: 100 − 40 = +60 J (II)", "B: −50 − (−80) = +30 J (IV)", "C: 0 − 50 = −50 J (III)",
     "D: 120 − 200 = −80 J (I)"],
    why="The other codes add W instead of subtracting it in case B, or interchange the two negative results.",
    ncert="Class 11 Physics, 'Thermodynamics', first law of thermodynamics", seconds=60, recomputed=True)

n_m = 2
W_iso_p = n_m * R_ * 300
W_adi = n_m * 2.5 * R_ * 300
assert close(W_iso_p, 4980) and close(W_adi, 12450) and close(W_iso_p + W_adi, 17430) \
    and close(n_m * 3.5 * R_ * 300, 17430) and close(W_adi - W_iso_p, 7470)
add(T, "Isothermal and adiabatic processes", "Advanced", "numerical",
    "Two moles of an ideal diatomic gas (rigid molecules, C_v = 5R/2) at 300 K are heated at constant pressure until "
    "the temperature is 600 K. The gas then expands reversibly and adiabatically until its temperature falls back "
    "to 300 K. Taking R = 8.3 J mol⁻¹ K⁻¹, the total work done by the gas in the two processes is:",
    place("17.43 kJ", ["4.98 kJ", "12.45 kJ", "7.47 kJ"], "B"),
    "Work in isobaric and adiabatic processes",
    "In the isobaric step W = nRΔT. In the adiabatic step no heat flows, so the work done equals the fall in "
    "internal energy, nC_vΔT.",
    ["Isobaric: W₁ = 2 × 8.3 × 300 = 4980 J", "Adiabatic: W₂ = 2 × (5/2) × 8.3 × 300 = 12 450 J",
     "Total W = 17 430 J ≈ 17.43 kJ", "Check: the net ΔU is zero, so W equals the heat absorbed, nC_pΔT = 17 430 J"],
    why="4.98 kJ counts only the isobaric step and 12.45 kJ only the adiabatic step. 7.47 kJ subtracts the two "
        "works although the gas expands, doing positive work, in both steps.",
    ncert="Class 11 Physics, 'Thermodynamics', thermodynamic processes (isobaric and adiabatic)", seconds=110,
    recomputed=True)

add(T, "Zeroth and first law", "Advanced", "assertion_reason",
    AR_STEM.format(
        a="When an ideal gas is taken from an equilibrium state A to another equilibrium state B, the heat it "
          "absorbs is the same whatever path it follows.",
        r="The change in the internal energy of an ideal gas in going from state A to state B is the same for every "
          "path."),
    ar("D"),
    "State functions and path functions",
    "Internal energy is a state variable, so ΔU between A and B is fixed. The work done, the area under the P–V "
    "path, depends on the path, and therefore so does Q = ΔU + W.",
    ["ΔU(A → B) is path-independent → R true", "W depends on the path → Q = ΔU + W depends on the path → A false"],
    why="A is false, so options A, B and C, which need A to be true, are wrong.",
    ncert="Class 11 Physics, 'Thermodynamics', heat, internal energy and work; first law of thermodynamics",
    seconds=50)

# =====================================================================================================================
# Kinetic Theory of Gases (B2 I2 A2)
# =====================================================================================================================
T = "Kinetic Theory of Gases"

v_h2 = math.sqrt(3 * R_ * 300 / 0.002)
assert close(v_h2, 1932.6, 1e-3) and close(math.sqrt(3 * R_ * 300 / 2), 61.1, 1e-3) \
    and close(math.sqrt(R_ * 300 / 0.002), 1115.8, 1e-3) and close(3 * R_ * 300 / 0.002, 3.735e6)
add(T, "Pressure and rms speed", "Basic", "numerical",
    "Taking R = 8.3 J mol⁻¹ K⁻¹, the root mean square speed of hydrogen molecules (molar mass 2 g/mol) at 300 K is "
    "about:",
    place("1.93 km/s", ["61 m/s", "1.12 km/s", "3.7 × 10⁶ m/s"], "A"),
    "rms speed, v_rms = √(3RT/M)",
    "The molar mass must be in kg/mol: M = 2 × 10⁻³ kg/mol.",
    ["v_rms = √(3 × 8.3 × 300/(2 × 10⁻³))", "= √(3.735 × 10⁶) ≈ 1.93 × 10³ m/s"],
    why="61 m/s keeps the molar mass in g/mol. 1.12 km/s leaves out the factor 3. 3.7 × 10⁶ m/s forgets to take the "
        "square root.",
    ncert="Class 11 Physics, 'Kinetic Theory', kinetic interpretation of temperature", seconds=45, recomputed=True)

add(T, "Degrees of freedom and equipartition", "Basic", "assertion_reason",
    AR_STEM.format(
        a="The molar specific heat at constant volume of an ideal gas of rigid diatomic molecules is 3R/2.",
        r="A rigid diatomic molecule has three translational and two rotational degrees of freedom."),
    ar("D"),
    "Specific heat from the law of equipartition",
    "Each quadratic degree of freedom contributes ½k_BT per molecule, i.e. ½RT per mole. With 3 translational and 2 "
    "rotational degrees of freedom, U = (5/2)RT per mole, so C_v = 5R/2. The value 3R/2 belongs to a monatomic gas.",
    ["R: 3 + 2 = 5 degrees of freedom (true)", "U = (5/2)RT → C_v = 5R/2, not 3R/2 → A false"],
    why="A is false, so A, B and C are wrong.",
    ncert="Class 11 Physics, 'Kinetic Theory', law of equipartition of energy and specific heat capacity",
    seconds=40)

E_mol = {"trans_mono": F(3, 2), "rot_di": F(1), "tot_di": F(5, 2), "poly": F(3)}
assert E_mol["trans_mono"] + E_mol["rot_di"] == E_mol["tot_di"] and E_mol["poly"] == 6 * F(1, 2)
add(T, "Degrees of freedom and equipartition", "Intermediate", "match_list",
    match_stem("One mole of each ideal gas is at absolute temperature T, and vibrations are not excited. Using the "
               "law of equipartition of energy, match List-I (energy) with List-II (its value; R is the gas "
               "constant).",
               ["Total translational kinetic energy of a monatomic gas",
                "Total rotational kinetic energy of a diatomic gas",
                "Total kinetic energy of a diatomic gas",
                "Internal energy of a gas of non-linear polyatomic molecules"],
               ["RT", "3RT", "3RT/2", "5RT/2"]),
    match_options({"A": "III", "B": "I", "C": "IV", "D": "II"},
                  [{"A": "III", "B": "IV", "C": "I", "D": "II"}, {"A": "I", "B": "III", "C": "IV", "D": "II"},
                   {"A": "III", "B": "I", "C": "II", "D": "IV"}], "B"),
    "Law of equipartition of energy",
    "Each degree of freedom carries ½RT per mole. A monatomic molecule has 3 translational degrees of freedom, a "
    "rigid diatomic one adds 2 rotational, and a rigid non-linear polyatomic one has 3 rotational.",
    ["A: 3 × ½RT = 3RT/2 (III)", "B: 2 × ½RT = RT (I)", "C: 5 × ½RT = 5RT/2 (IV)", "D: 6 × ½RT = 3RT (II)"],
    why="The other codes give the diatomic molecule 3 rotational degrees of freedom or count only translation for "
        "the total.",
    ncert="Class 11 Physics, 'Kinetic Theory', law of equipartition of energy", seconds=60, recomputed=True)

add(T, "Ideal gas equation", "Intermediate", "statement_pair",
    SP_STEM.format(
        s1="The internal energy of an ideal gas is the sum of the kinetic energies of its molecules; there is no "
           "potential energy of interaction between the molecules.",
        s2="The internal energy of a given mass of an ideal gas increases when it is compressed isothermally."),
    sp("C"),
    "Internal energy of an ideal gas depends only on temperature",
    "Molecules of an ideal gas do not interact except during collisions, so the internal energy is entirely kinetic "
    "and, by equipartition, depends only on the temperature. In an isothermal compression the temperature, and "
    "hence the internal energy, stays the same.",
    ["Statement I: no intermolecular forces → U is purely kinetic (true)",
     "Statement II: T constant → U constant (false)"],
    why="Statement II would need intermolecular potential energy that depends on volume, which an ideal gas does not "
        "have; so A, B and D are wrong.",
    ncert="Class 11 Physics, 'Kinetic Theory', molecular nature of matter and kinetic theory of an ideal gas",
    seconds=45)

P_new = F(2) / (1 + F(1, 2))                      # n_total fixed: P'(1/300 + 1/600) = 2P/300
assert P_new == F(4, 3) and 2 * F(300, 450) == F(4, 3)
add(T, "Ideal gas equation", "Advanced", "numerical",
    "Two identical vessels connected by a narrow tube of negligible volume contain an ideal gas at 300 K and "
    "pressure P. One vessel is then heated to 600 K while the other is kept at 300 K. The pressure of the gas in the "
    "vessels becomes:",
    place("4P/3", ["3P/2", "2P", "P"], "C"),
    "Ideal gas equation with a fixed total amount of gas",
    "The total number of moles stays the same, and when equilibrium is reached the pressure is the same in both "
    "vessels. Write n = PV/(RT) for each vessel.",
    ["Before: n = 2PV/(R × 300)", "After: P'V/(R × 300) + P'V/(R × 600) = 2PV/(R × 300)",
     "P'(2 + 1)/600 = 2P/300 → P' = 4P/3"],
    why="3P/2 uses the average temperature (450 K) for the whole gas, which is not how moles are shared. 2P assumes "
        "the gas in the heated vessel keeps its moles. P ignores the heating.",
    ncert="Class 11 Physics, 'Kinetic Theory', behaviour of gases (ideal gas equation)", seconds=90, recomputed=True)

T_new = F(300) / (1 - F(1, 4))
assert T_new == 400 and T_new - 273 == 127 and 300 * F(5, 4) == 375 and 27 * F(4, 3) == 36
add(T, "Ideal gas equation", "Advanced", "numerical",
    "A vessel open to the atmosphere contains air at 27 °C. It is heated slowly, the pressure inside staying equal "
    "to the atmospheric pressure, until one-quarter of the air that was in the vessel has escaped. Neglecting the "
    "expansion of the vessel and treating air as an ideal gas, the temperature of the air in the vessel is now:",
    place("127 °C", ["102 °C", "36 °C", "400 °C"], "A"),
    "Ideal gas equation with escaping gas (P and V fixed)",
    "With P and V fixed, PV = nRT gives nT = constant: as the gas is heated, the amount remaining in the vessel "
    "falls in inverse proportion to the absolute temperature.",
    ["n₁T₁ = n₂T₂ with n₂ = (3/4)n₁", "T₂ = 300 × 4/3 = 400 K = 127 °C"],
    why="102 °C (375 K) multiplies T by 5/4 instead of 4/3. 36 °C applies the ratio to the Celsius temperature. "
        "400 °C confuses kelvin with degrees Celsius.",
    ncert="Class 11 Physics, 'Kinetic Theory', behaviour of gases (ideal gas equation)", seconds=80, recomputed=True)


# =====================================================================================================================
# Oscillations and Waves (B4 I6 A4)
# =====================================================================================================================
T = "Oscillations and Waves"

B_w, rho_ww = 2.25e9, 1000.0
v_w = math.sqrt(B_w / rho_ww)
assert close(v_w, 1500) and close(B_w / rho_ww, 2.25e6) and close(math.sqrt(B_w / 1e6), 47.43) \
    and close(math.sqrt(B_w), 47434)
add(T, "Progressive waves and wave speed", "Basic", "numerical",
    "The bulk modulus of water is 2.25 × 10⁹ Pa and its density is 1000 kg/m³. The speed of sound (longitudinal "
    "waves) in water is:",
    place("1500 m/s", ["2.25 × 10⁶ m/s", "about 47 m/s", "about 4.7 × 10⁴ m/s"], "B"),
    "Speed of longitudinal waves in a fluid",
    "For longitudinal waves in a fluid, v = √(B/ρ), where B is the bulk modulus.",
    ["v = √(2.25 × 10⁹/1000) = √(2.25 × 10⁶) = 1500 m/s"],
    why="2.25 × 10⁶ m/s forgets the square root. About 47 m/s takes the density as 10⁶ kg/m³ instead "
        "of 10³ kg/m³. About 4.7 × 10⁴ m/s takes the density as 1 (its value in g/cm³).",
    ncert="Class 11 Physics, 'Waves', speed of a longitudinal wave (speed of sound)", seconds=35, recomputed=True)

w_a = math.sqrt(16 * math.pi ** 2)
f_a = w_a / (2 * math.pi)
assert close(f_a, 2) and close(w_a, 4 * math.pi) and close(16 / 2, 8)
add(T, "SHM equation and phase", "Basic", "numerical",
    "The acceleration a of a particle is related to its displacement x by a = −16π²x, with a in m/s² and x in "
    "metres. The frequency of its oscillation is:",
    place("2 Hz", ["4π Hz", "0.5 Hz", "8 Hz"], "D"),
    "Defining relation of SHM, a = −ω²x",
    "Comparing with a = −ω²x gives ω² = 16π², so ω = 4π rad/s and ν = ω/2π.",
    ["ω = √(16π²) = 4π rad/s", "ν = 4π/2π = 2 Hz"],
    why="4π is the angular frequency in rad/s, not the frequency in Hz. 0.5 Hz is the period in seconds read as a "
        "frequency. 8 Hz divides ω² by 2π².",
    ncert="Class 11 Physics, 'Oscillations', simple harmonic motion and uniform circular motion (a = −ω²x)",
    seconds=30, recomputed=True)

add(T, "SHM equation and phase", "Basic", "direct",
    "For a particle executing simple harmonic motion x = A sin ωt, the phase difference between its velocity and "
    "its acceleration is:",
    place("π/2", ["π", "zero", "π/4"], "C"),
    "Phase relations in SHM",
    "v = Aω cos ωt and a = −Aω² sin ωt = Aω² cos(ωt + π/2). The acceleration leads the velocity by π/2: when the "
    "speed is greatest (at the mean position) the acceleration is zero, and vice versa.",
    ["v = Aω cos ωt", "a = Aω² cos(ωt + π/2) → phase difference π/2"],
    why="π is the phase difference between displacement and acceleration. Zero would make velocity and acceleration "
        "greatest together. π/4 has no basis.",
    ncert="Class 11 Physics, 'Oscillations', velocity and acceleration in simple harmonic motion", seconds=30)

fb1, fb2 = 256, 260
beat = fb2 - fb1
assert beat == 4 and F(1, beat) == F(1, 4)
add(T, "Organ pipes and beats", "Basic", "numerical",
    "Two tuning forks of frequencies 256 Hz and 260 Hz are sounded together. The time interval between two "
    "successive maxima of sound intensity is:",
    place("0.25 s", ["4 s", "0.5 s", "about 0.004 s"], "A"),
    "Beat frequency and beat period",
    "The beat frequency is the difference of the two frequencies, and the interval between successive maxima is its "
    "reciprocal.",
    ["Beat frequency = 260 − 256 = 4 Hz", "Time between maxima = 1/4 = 0.25 s"],
    why="4 s takes the beat frequency itself as the time. 0.5 s halves the beat frequency. About 0.004 s is the "
        "period of either fork.",
    ncert="Class 11 Physics, 'Waves', beats", seconds=30, recomputed=True)

phi0 = math.asin(0.5)
assert close(phi0, math.pi / 6) and math.cos(phi0) > 0 and math.cos(5 * math.pi / 6) < 0
add(T, "SHM equation and phase", "Intermediate", "numerical",
    "A particle executes simple harmonic motion x = A sin(ωt + φ). At t = 0 it is at x = +A/2 and moving towards the "
    "positive extreme position x = +A. The value of φ is:",
    place("π/6", ["5π/6", "π/3", "π/2"], "B"),
    "Phase constant from the initial position and direction of motion",
    "At t = 0, x = A sin φ and v = Aω cos φ. The position fixes sin φ; the direction of motion fixes the sign of "
    "cos φ.",
    ["A sin φ = A/2 → φ = π/6 or 5π/6", "Moving towards +A → v > 0 → cos φ > 0 → φ = π/6"],
    why="5π/6 also gives x = A/2 but with the particle moving towards the mean position (v < 0). π/3 gives x = A sin "
        "60° ≈ 0.87A. π/2 puts the particle at the extreme.",
    ncert="Class 11 Physics, 'Oscillations', simple harmonic motion (phase)", seconds=50, recomputed=True)

g_eff = math.hypot(g, g * math.sqrt(3))
T_ratio = math.sqrt(g / g_eff)
assert close(g_eff, 2 * g) and close(T_ratio, 1 / math.sqrt(2))
add(T, "Spring and pendulum oscillations", "Intermediate", "numerical",
    "A simple pendulum has a period T for small oscillations when it hangs in a car at rest. The car now moves on a "
    "level road with a constant acceleration of √3 g. The period of small oscillations of the pendulum about its new "
    "equilibrium position becomes:",
    place("T/√2", ["T/2", "T", "√2 T"], "C"),
    "Pendulum with an effective gravity",
    "In the accelerating car the bob's equilibrium is tilted; the effective gravity is the vector combination of g "
    "(down) and the car's acceleration (horizontal): g_eff = √(g² + a²). The period is 2π√(L/g_eff).",
    ["g_eff = √(g² + 3g²) = 2g", "T' = 2π√(L/2g) = T/√2"],
    why="T/2 forgets the square root. T assumes a horizontal acceleration does not affect the pendulum. √2 T "
        "inverts the effect: a larger effective gravity shortens the period.",
    ncert="Class 11 Physics, 'Oscillations', the simple pendulum", seconds=60, recomputed=True)

KE_f = 1 - F(1, 4)
PE_f = F(1, 4)
assert KE_f / PE_f == 3
add(T, "Energy in SHM", "Intermediate", "numerical",
    "A particle executes simple harmonic motion with amplitude A. When its displacement from the mean position is "
    "A/2, the ratio of its kinetic energy to its potential energy is:",
    place("3 : 1", ["1 : 1", "1 : 3", "2 : 1"], "D"),
    "Energy at a displacement in SHM",
    "The potential energy is ½kx² and the total energy is ½kA². The kinetic energy is the difference.",
    ["U = ½k(A/2)² = (1/4) × ½kA²", "K = ½kA² − U = (3/4) × ½kA²", "K : U = 3 : 1"],
    why="1 : 1 happens at x = A/√2, not A/2. 1 : 3 inverts the ratio. 2 : 1 takes the energies as proportional to "
        "x rather than x².",
    ncert="Class 11 Physics, 'Oscillations', energy in simple harmonic motion", seconds=45, recomputed=True)

add(T, "Spring and pendulum oscillations", "Intermediate", "assertion_reason",
    AR_STEM.format(
        a="A block hanging from a light vertical spring oscillates with the same period as when the same block, "
          "attached to the same spring, oscillates on a smooth horizontal surface.",
        r="Gravity increases the force constant of a spring that hangs vertically."),
    ar("C"),
    "Spring–block period is independent of gravity",
    "For the hanging block, gravity only shifts the equilibrium position (to an extension mg/k). About that position "
    "the net restoring force is still −kx, so T = 2π√(m/k) in both cases. The force constant is a property of the "
    "spring and is not changed by gravity.",
    ["Vertical: net force about the new equilibrium = −kx → T = 2π√(m/k) (A true)",
     "k does not depend on gravity (R false)"],
    why="R is false, so A and B are wrong; A is true, so D is wrong.",
    ncert="Class 11 Physics, 'Oscillations', oscillations due to a spring", seconds=45)

add(T, "Superposition and standing waves", "Intermediate", "statement_pair",
    SP_STEM.format(
        s1="In a stationary wave on a stretched string, the amplitude of oscillation differs from point to point, "
           "being zero at the nodes.",
        s2="In a sinusoidal progressive wave travelling along a string without loss of energy, every particle of the "
           "string oscillates with the same amplitude."),
    sp("A"),
    "Amplitude in stationary and progressive waves",
    "A stationary wave y = 2a sin kx cos ωt has the position-dependent amplitude 2a sin kx, zero at the nodes and 2a "
    "at the antinodes. In a progressive wave y = a sin(kx − ωt), every particle has amplitude a; only the phase "
    "differs from point to point.",
    ["Stationary: amplitude 2a|sin kx| (Statement I true)", "Progressive: amplitude a everywhere (Statement II true)"],
    why="Both statements are true, so B, C and D are wrong.",
    ncert="Class 11 Physics, 'Waves', displacement relation in a progressive wave; standing waves", seconds=45)

A_s, w_s, ph_s = 0.05, 10.0, math.pi / 6
assert close(2 * math.pi / w_s, math.pi / 5) and close(A_s * w_s, 0.5) and close(A_s * w_s ** 2, 5) \
    and close(A_s * math.sin(ph_s), 0.025)
add(T, "SHM equation and phase", "Intermediate", "match_list",
    match_stem("The displacement of a particle is x = 0.05 sin(10t + π/6), where x is in metres and t in seconds. "
               "Match List-I (quantity) with List-II (its value).",
               ["Period of the motion", "Maximum speed", "Maximum magnitude of acceleration",
                "Displacement at t = 0"],
               ["5 m s⁻²", "0.025 m", "π/5 s", "0.5 m s⁻¹"]),
    match_options({"A": "III", "B": "IV", "C": "I", "D": "II"},
                  [{"A": "III", "B": "I", "C": "IV", "D": "II"}, {"A": "II", "B": "IV", "C": "I", "D": "III"},
                   {"A": "III", "B": "IV", "C": "II", "D": "I"}], "B"),
    "Reading an SHM equation",
    "Compare with x = A sin(ωt + φ): A = 0.05 m, ω = 10 rad/s, φ = π/6. Then T = 2π/ω, v_max = Aω and a_max = Aω².",
    ["T = 2π/10 = π/5 s (III)", "v_max = 0.05 × 10 = 0.5 m/s (IV)", "a_max = 0.05 × 100 = 5 m/s² (I)",
     "x(0) = 0.05 sin(π/6) = 0.025 m (II)"],
    why="The other codes swap the maximum speed with the maximum acceleration, or the period with the initial "
        "displacement.",
    ncert="Class 11 Physics, 'Oscillations', simple harmonic motion", seconds=60, recomputed=True)

w_pl = 2 * math.pi * (5 / math.pi)
A_max = g / w_pl ** 2
assert close(w_pl, 10) and close(A_max, 0.1) and close(g / w_pl, 1) and close(2 * g / w_pl ** 2, 0.2)
add(T, "SHM equation and phase", "Advanced", "numerical",
    "A horizontal platform moves up and down in simple harmonic motion with a frequency of (5/π) Hz. A small block "
    "rests on it. Taking g = 10 m/s², the largest amplitude of the motion for which the block never loses contact "
    "with the platform is:",
    place("10 cm", ["1 m", "20 cm", "1 cm"], "D"),
    "Losing contact in vertical SHM",
    "The block stays in contact only while the normal force is positive: N = m(g − a), where a is the platform's "
    "downward acceleration. The largest downward acceleration, ω²A, occurs at the top of the motion, so we need "
    "ω²A ≤ g.",
    ["ω = 2π × (5/π) = 10 rad/s", "ω²A ≤ g → A ≤ 10/100 = 0.1 m = 10 cm"],
    why="1 m uses g/ω instead of g/ω². 20 cm allows a downward acceleration of 2g. 1 cm has an error of a factor of "
        "10 in ω².",
    ncert="Class 11 Physics, 'Oscillations', velocity and acceleration in simple harmonic motion", seconds=90,
    recomputed=True)

f_src, v_snd = 170.0, 340.0
lam_s = v_snd / f_src
dphi = 2 * math.pi * (4.5 - 3.0) / lam_s
amp = abs(2 * math.cos(dphi / 2))
assert close(lam_s, 2) and close(dphi, 1.5 * math.pi) and close(amp, math.sqrt(2))
add(T, "Superposition and standing waves", "Advanced", "numerical",
    "Two small sources of sound S₁ and S₂ vibrate in phase with the same frequency of 170 Hz. A point P is 3.0 m "
    "from S₁ and 4.5 m from S₂, and the waves from the two sources reach P with the same amplitude a. Taking the "
    "speed of sound as 340 m/s, the amplitude of the resultant oscillation at P is:",
    place("a√2", ["0", "2a", "a"], "A"),
    "Superposition of two waves with a phase difference",
    "The path difference gives a phase difference φ = 2π(Δx)/λ. Two oscillations of equal amplitude a and phase "
    "difference φ combine to give amplitude 2a|cos(φ/2)|.",
    ["λ = 340/170 = 2 m", "Δx = 1.5 m → φ = 2π × 1.5/2 = 3π/2", "Amplitude = 2a|cos(3π/4)| = 2a/√2 = a√2"],
    why="0 needs a path difference of an odd number of half-wavelengths (φ = π, 3π, …); 1.5 m is three-quarters of a "
        "wavelength. 2a needs a whole number of wavelengths. a corresponds to φ = 2π/3.",
    ncert="Class 11 Physics, 'Waves', the principle of superposition of waves", seconds=100, recomputed=True)

Lp = 0.17
f1c = v_snd / (4 * Lp)
assert close(f1c, 500) and close(3 * f1c, 1500) and close(v_snd / (2 * Lp), 1000) and not close(1000 / f1c % 2, 1)
multi_key([close(f1c, 500), close(3 * f1c, 1500), True, close(v_snd / (2 * Lp), 1000), False], "abcd")
add(T, "Organ pipes and beats", "Advanced", "multi_statement",
    multi("A pipe 17 cm long is closed at one end and open at the other. Taking the speed of sound in air as "
          "340 m/s and neglecting end corrections, which of the following statements are correct?",
          ["Its fundamental frequency is 500 Hz.",
           "The next higher frequency at which it resonates is 1500 Hz.",
           "It cannot resonate at 1000 Hz.",
           "If its closed end is opened, its fundamental frequency becomes 1000 Hz.",
           "There is a displacement antinode at its closed end."]),
    place("(a), (b), (c) and (d) only", ["(a), (b) and (e) only", "(a), (c), (d) and (e) only",
                                         "(b), (c) and (d) only"], "C"),
    "Normal modes of closed and open pipes",
    "A pipe closed at one end has a displacement node at the closed end and an antinode at the open end, so "
    "L = λ/4, 3λ/4, …: only odd harmonics v/4L, 3v/4L, … occur. A pipe open at both ends has fundamental v/2L.",
    ["(a) f₁ = 340/(4 × 0.17) = 500 Hz (true)", "(b) next: 3f₁ = 1500 Hz (true)",
     "(c) 1000 Hz = 2f₁, an even harmonic, is absent (true)", "(d) open pipe: 340/(2 × 0.17) = 1000 Hz (true)",
     "(e) the closed end is a displacement node (false)"],
    why="(e) reverses node and antinode; (b), (c) and (d) only leaves out the true statement (a).",
    ncert="Class 11 Physics, 'Waves', standing waves in pipes (closed and open)", seconds=100, recomputed=True)

m_o, k_o, A_o = 1.0, 100.0, 0.2
w_o = math.sqrt(k_o / m_o)
assert w_o == 10 and close(A_o * w_o, 2) and close(0.5 * k_o * A_o ** 2, 2) \
    and close(w_o * math.sqrt(A_o ** 2 - 0.1 ** 2), math.sqrt(3)) and close(k_o * A_o, 20)
multi_key([w_o == 10, close(A_o * w_o, 2), close(0.5 * k_o * A_o ** 2, 4),
           close(w_o * math.sqrt(A_o ** 2 - 0.01), math.sqrt(3)), close(k_o * A_o, 20)], "abde")
add(T, "Energy in SHM", "Advanced", "multi_statement",
    multi("A block of mass 1 kg attached to a light spring of force constant 100 N/m oscillates on a smooth "
          "horizontal surface with an amplitude of 0.2 m. Which of the following statements are correct?",
          ["The angular frequency of the oscillation is 10 rad/s.",
           "The maximum speed of the block is 2 m/s.",
           "The total mechanical energy of the oscillation is 4 J.",
           "When the displacement is 0.1 m, the speed of the block is √3 m/s.",
           "The maximum magnitude of the force on the block is 20 N."]),
    place("(a), (b), (d) and (e) only", ["(a), (b), (c) and (d) only", "(a), (c) and (e) only",
                                         "(b), (c), (d) and (e) only"], "B"),
    "Spring–block oscillator: frequency, speed, energy and force",
    "ω = √(k/m); the speed at displacement x is ω√(A² − x²); the total energy is ½kA²; the restoring force is "
    "greatest, kA, at the extremes.",
    ["(a) ω = √(100/1) = 10 rad/s (true)", "(b) v_max = Aω = 2 m/s (true)",
     "(c) E = ½ × 100 × 0.04 = 2 J, not 4 J (false)", "(d) v = 10√(0.04 − 0.01) = √3 m/s (true)",
     "(e) F_max = 100 × 0.2 = 20 N (true)"],
    why="(c) forgets the ½ in ½kA²; every option with (c) is wrong.",
    ncert="Class 11 Physics, 'Oscillations', oscillations due to a spring and energy in SHM", seconds=100,
    recomputed=True)


# =====================================================================================================================
# Electrostatics (B6 I8 A6)
# =====================================================================================================================
T = "Electrostatics"

p_d, E_d = 2e-8, 5e3
U_d = -p_d * E_d * math.cos(math.radians(60))
assert close(U_d, -5e-5) and close(-p_d * E_d * math.sin(math.radians(60)), -8.66e-5) and close(-p_d * E_d, -1e-4)
add(T, "Electric field and dipole", "Basic", "numerical",
    "An electric dipole of dipole moment 2 × 10⁻⁸ C m is placed in a uniform electric field of 5 × 10³ N/C, with its "
    "dipole moment at 60° to the field. Taking the potential energy to be zero when the dipole is perpendicular to "
    "the field, its potential energy is:",
    place("−5 × 10⁻⁵ J", ["+5 × 10⁻⁵ J", "−8.7 × 10⁻⁵ J", "−1 × 10⁻⁴ J"], "A"),
    "Potential energy of a dipole in a uniform field, U = −pE cos θ",
    "With zero potential energy at θ = 90°, the potential energy of a dipole in a uniform field is U = −p·E = "
    "−pE cos θ.",
    ["U = −(2 × 10⁻⁸)(5 × 10³) cos 60°", "= −10⁻⁴ × ½ = −5 × 10⁻⁵ J"],
    why="+5 × 10⁻⁵ J drops the minus sign. −8.7 × 10⁻⁵ J uses sin θ, which belongs in the torque. −1 × 10⁻⁴ J is "
        "the value for θ = 0.",
    ncert="Class 12 Physics, 'Electrostatic Potential and Capacitance', potential energy of a dipole in an external "
          "field", seconds=40, recomputed=True)

sig = 8.85e-9
E_sheet = sig / (2 * EPS0)
assert close(E_sheet, 500) and close(sig / EPS0, 1000) and close(sig / (4 * EPS0), 250) and close(2 * sig / EPS0, 2000)
add(T, "Gauss's law", "Basic", "numerical",
    "A large, thin, plane sheet carries a uniform surface charge density of 8.85 × 10⁻⁹ C/m². Taking "
    "ε₀ = 8.85 × 10⁻¹² C² N⁻¹ m⁻², the magnitude of the electric field near the sheet, away from its edges, is:",
    place("500 N/C", ["1000 N/C", "250 N/C", "2000 N/C"], "C"),
    "Field of an infinite plane sheet of charge",
    "Applying Gauss's law to a cylinder that pierces the sheet, the flux leaves through both flat faces: "
    "2EA = σA/ε₀, so E = σ/(2ε₀), independent of the distance from the sheet.",
    ["E = σ/(2ε₀) = 8.85 × 10⁻⁹/(2 × 8.85 × 10⁻¹²)", "= 500 N/C"],
    why="1000 N/C is σ/ε₀, the field just outside a charged conductor. 250 N/C divides by 4ε₀. 2000 N/C multiplies "
        "instead of dividing by 2.",
    ncert="Class 12 Physics, 'Electric Charges and Fields', applications of Gauss's law (field due to a uniformly "
          "charged infinite plane sheet)", seconds=35, recomputed=True)

add(T, "Coulomb's law and superposition", "Basic", "direct",
    "The quantisation of electric charge, first suggested by the laws of electrolysis, was demonstrated "
    "experimentally in 1912 by:",
    place("R. A. Millikan", ["Michael Faraday", "Charles Coulomb", "J. J. Thomson"], "D"),
    "Quantisation of charge",
    "NCERT notes that the laws of electrolysis found by Faraday first suggested that charge is quantised, and that "
    "Millikan demonstrated it experimentally in 1912 (the oil-drop experiment).",
    ["Faraday: suggested by electrolysis", "Millikan (1912): experimental demonstration"],
    why="Faraday's electrolysis laws only suggested quantisation. Coulomb measured the force between charges. "
        "Thomson's work is not what NCERT credits for this demonstration.",
    ncert="Class 12 Physics, 'Electric Charges and Fields', basic properties of electric charge (quantisation of "
          "charge)", seconds=25)

E_p, d_p = 1e4, 0.01
K_p = E_CH * E_p * d_p
assert close(K_p, 1.6e-17) and close(K_p / E_CH, 100) and close(E_CH * E_p * 1, 1.6e-15) and close(K_p / 2, 8e-18)
add(T, "Electric potential and energy", "Basic", "numerical",
    "A proton is released from rest in a uniform electric field of 1 × 10⁴ N/C. Taking the charge of a proton as "
    "1.6 × 10⁻¹⁹ C, its kinetic energy after it has moved 1 cm along the field is:",
    place("1.6 × 10⁻¹⁷ J", ["1.6 × 10⁻¹⁵ J", "1.6 × 10⁻¹⁹ J", "8 × 10⁻¹⁸ J"], "B"),
    "Work done by a uniform field on a charge",
    "The field does work qEd on the proton, which becomes its kinetic energy (work–energy theorem). Equivalently the "
    "proton falls through a potential difference Ed = 100 V and gains 100 eV.",
    ["W = qEd = 1.6 × 10⁻¹⁹ × 10⁴ × 0.01", "= 1.6 × 10⁻¹⁷ J (= 100 eV)"],
    why="1.6 × 10⁻¹⁵ J leaves the distance in centimetres. 1.6 × 10⁻¹⁹ J is just the charge, or 1 eV. "
        "8 × 10⁻¹⁸ J puts in an unwanted factor ½.",
    ncert="Class 12 Physics, 'Electrostatic Potential and Capacitance', electrostatic potential and potential "
          "difference", seconds=35, recomputed=True)

add(T, "Electric field and dipole", "Basic", "match_list",
    match_stem("A particle of charge q and mass m is in a uniform electric field E; no other force acts on it. It "
               "moves through a distance d along the field. Match List-I (quantity) with List-II (expression).",
               ["Force on the particle", "Acceleration of the particle", "Work done by the field over the distance d",
                "Potential difference between the starting and the end point"],
               ["Ed", "qEd", "qE", "qE/m"]),
    match_options({"A": "III", "B": "IV", "C": "II", "D": "I"},
                  [{"A": "III", "B": "II", "C": "IV", "D": "I"}, {"A": "IV", "B": "III", "C": "II", "D": "I"},
                   {"A": "III", "B": "IV", "C": "I", "D": "II"}], "D"),
    "Charge in a uniform electric field",
    "F = qE; a = F/m; the work done by a constant force along its own direction is Fd; and in a uniform field the "
    "potential falls by E per unit distance along the field, so the potential difference is Ed.",
    ["Force qE (III)", "Acceleration qE/m (IV)", "Work qEd (II)", "Potential difference Ed (I)"],
    why="The other codes confuse work (qEd, energy) with potential difference (Ed, energy per unit charge), or force "
        "with acceleration.",
    ncert="Class 12 Physics, 'Electric Charges and Fields', electric field; 'Electrostatic Potential and "
          "Capacitance', relation between field and potential", seconds=40)

caps = [2.0, 3.0, 6.0]
Cp, Cs = sum(caps), 1 / sum(1 / c for c in caps)
assert Cp > max(caps) and Cs < min(caps)
add(T, "Capacitors and dielectrics", "Basic", "statement_pair",
    SP_STEM.format(
        s1="The equivalent capacitance of capacitors connected in parallel is greater than the largest of the "
           "individual capacitances.",
        s2="The equivalent capacitance of capacitors connected in series is less than the smallest of the individual "
           "capacitances."),
    sp("A"),
    "Combination of capacitors",
    "In parallel, C = C₁ + C₂ + …, a sum of positive terms, so it exceeds each term. In series, 1/C = 1/C₁ + 1/C₂ + …"
    " exceeds each 1/Cᵢ, so C is smaller than every Cᵢ.",
    ["Parallel: 2 + 3 + 6 = 11 μF > 6 μF", "Series: 1/C = 1/2 + 1/3 + 1/6 = 1 → C = 1 μF < 2 μF"],
    why="Both statements are true, so B, C and D are wrong.",
    ncert="Class 12 Physics, 'Electrostatic Potential and Capacitance', combination of capacitors", seconds=35)

phi_in, phi_out = 8e3, 4e3
q_enc = EPS0 * (phi_out - phi_in)
assert close(q_enc, -3.54e-8) and close(EPS0 * (phi_out + phi_in), 1.062e-7)
add(T, "Gauss's law", "Intermediate", "numerical",
    "Electric flux of 8 × 10³ N m² C⁻¹ enters a closed surface and flux of 4 × 10³ N m² C⁻¹ leaves it. Taking "
    "ε₀ = 8.85 × 10⁻¹² C² N⁻¹ m⁻², the net charge enclosed by the surface is:",
    place("−3.54 × 10⁻⁸ C", ["+3.54 × 10⁻⁸ C", "−1.06 × 10⁻⁷ C", "+1.06 × 10⁻⁷ C"], "B"),
    "Gauss's law with inward and outward flux",
    "Outward flux is positive and inward flux negative. Gauss's law gives q_enclosed = ε₀ × (net outward flux).",
    ["Net outward flux = 4 × 10³ − 8 × 10³ = −4 × 10³ N m² C⁻¹", "q = ε₀Φ = 8.85 × 10⁻¹² × (−4 × 10³) = "
     "−3.54 × 10⁻⁸ C"],
    why="+3.54 × 10⁻⁸ C has the sign reversed: more flux enters than leaves, so the enclosed charge is negative. The "
        "1.06 × 10⁻⁷ C options add the two fluxes instead of subtracting.",
    ncert="Class 12 Physics, 'Electric Charges and Fields', electric flux and Gauss's law", seconds=50,
    recomputed=True)

r_b = 0.53e-10
U_b = -k * E_CH ** 2 / r_b / E_CH
assert close(U_b, -27.17, 1e-3) and close(U_b / 2, -13.6, 1e-2)
add(T, "Electric potential and energy", "Intermediate", "numerical",
    "In a hydrogen atom, treat the electron and the proton as point charges 0.53 Å apart. Taking "
    "1/(4πε₀) = 9 × 10⁹ N m² C⁻², e = 1.6 × 10⁻¹⁹ C and 1 eV = 1.6 × 10⁻¹⁹ J, and the potential energy to be zero "
    "at infinite separation, the electrostatic potential energy of the pair is about:",
    place("−27.2 eV", ["+27.2 eV", "−13.6 eV", "−2.72 eV"], "C"),
    "Potential energy of two point charges",
    "U = kq₁q₂/r with q₁ = +e and q₂ = −e. Dividing the energy in joules by e converts it to electron volts.",
    ["U = −ke²/r = −9 × 10⁹ × (1.6 × 10⁻¹⁹)²/(0.53 × 10⁻¹⁰) J", "≈ −4.35 × 10⁻¹⁸ J",
     "= −4.35 × 10⁻¹⁸/1.6 × 10⁻¹⁹ eV ≈ −27.2 eV"],
    why="+27.2 eV ignores the opposite signs of the charges. −13.6 eV is half of the potential energy (the total "
        "energy in Bohr's model), not the potential energy. −2.72 eV is an error of a factor of 10 in converting "
        "ångströms to metres.",
    ncert="Class 12 Physics, 'Electrostatic Potential and Capacitance', potential energy of a system of charges",
    seconds=60, recomputed=True)

d_c = F(1)
C_new = 1 / (d_c - d_c / 2)
assert C_new == 2
add(T, "Capacitors and dielectrics", "Intermediate", "numerical",
    "A parallel plate capacitor with air between its plates has capacitance C₀ and plate separation d. An uncharged "
    "metal slab of thickness d/2, of the same area as the plates, is inserted between them parallel to the plates "
    "without touching them. The capacitance becomes:",
    place("2C₀", ["C₀", "C₀/2", "4C₀"], "A"),
    "Conductor inside a capacitor",
    "The field inside the metal slab is zero, so the potential difference between the plates is set only by the air "
    "gaps, whose total thickness is d − d/2 = d/2, wherever the slab sits. The capacitor behaves as one with plate "
    "separation d/2.",
    ["V = E₀(d − t) with t = d/2", "C = ε₀A/(d − d/2) = 2ε₀A/d = 2C₀"],
    why="C₀ ignores the slab. C₀/2 treats the slab as increasing the separation. 4C₀ squares the effect.",
    ncert="Class 12 Physics, 'Electrostatic Potential and Capacitance', the parallel plate capacitor (with a "
          "conductor inside: field inside a conductor is zero)", seconds=55, recomputed=True)

K_e, E_e = 100.0, 1000.0
d_stop = K_e / E_e
assert close(d_stop, 0.1)
add(T, "Electric potential and energy", "Intermediate", "numerical",
    "An electron with a kinetic energy of 100 eV enters a region of uniform electric field of 1000 V/m, moving in the "
    "same direction as the field. The distance it travels in the field before it momentarily comes to rest is:",
    place("10 cm", ["1 cm", "1 m", "20 cm"], "D"),
    "Retardation of an electron by an electric field",
    "The force on an electron is opposite to the field, so an electron moving along the field is slowed down. It "
    "stops after climbing a potential difference equal to its kinetic energy in electron volts.",
    ["Kinetic energy 100 eV → it can move against a potential difference of 100 V",
     "In a field of 1000 V/m, 100 V corresponds to 100/1000 = 0.1 m = 10 cm"],
    why="1 cm and 1 m are errors of a factor of 10 in converting units. 20 cm doubles the distance.",
    ncert="Class 12 Physics, 'Electrostatic Potential and Capacitance', relation between electric field and potential",
    seconds=50, recomputed=True)

add(T, "Coulomb's law and superposition", "Intermediate", "direct",
    "An uncharged metal sphere stands on an insulating stand. A negatively charged rod is brought near it without "
    "touching it. With the rod held there, the sphere is connected to the earth by a wire, and the wire is then "
    "removed. Finally the rod is taken away. The sphere is left with:",
    place("A positive charge spread uniformly over its surface",
          ["A negative charge spread uniformly over its surface", "No net charge",
           "A positive charge confined to the side that was nearer the rod"], "C"),
    "Charging by induction",
    "The negative rod repels free electrons to the far side of the sphere, leaving the near side positive. Earthing "
    "lets those repelled electrons flow away to the earth. When the earth connection and then the rod are removed, "
    "the sphere has a deficit of electrons, a net positive charge, which spreads uniformly over the conducting "
    "surface.",
    ["Rod near: electrons pushed to the far side", "Earthing: those electrons go to the earth",
     "Rod removed: net positive charge redistributes uniformly over the sphere"],
    why="Induction gives a charge opposite to that of the rod, so 'negative' is wrong. 'No net charge' forgets the "
        "electrons that left through the earth wire. Once the rod is removed, the charge on an isolated sphere "
        "spreads evenly; it does not stay on one side.",
    ncert="Class 12 Physics, 'Electric Charges and Fields', charging by induction", seconds=45)

add(T, "Electric potential and energy", "Intermediate", "assertion_reason",
    AR_STEM.format(
        a="An electron released from rest in an electrostatic field moves towards the region of higher potential.",
        r="The force on a negative charge is opposite to the electric field, and the electric field points in the "
          "direction in which the potential decreases."),
    ar("A"),
    "Motion of a negative charge in a potential gradient",
    "The field points from higher to lower potential. A negative charge experiences a force opposite to the field, "
    "i.e. towards higher potential, and starting from rest it moves that way, its potential energy (−e)V falling.",
    ["E points along decreasing V", "F = −eE points along increasing V → the electron moves towards higher V"],
    why="R gives the complete reason for A, so B is wrong; both are true, so C and D are wrong.",
    ncert="Class 12 Physics, 'Electrostatic Potential and Capacitance', relation between electric field and potential",
    seconds=40)

A_pp, d_pp, V_pp = 0.01, 1e-3, 100.0
C_pp = EPS0 * A_pp / d_pp
Q_pp = C_pp * V_pp
U_pp = 0.5 * C_pp * V_pp ** 2
assert close(C_pp, 88.5e-12) and close(Q_pp, 8.85e-9) and close(V_pp / d_pp, 1e5) and close(U_pp, 4.425e-7) \
    and close(Q_pp / A_pp, 8.85e-7)
multi_key([close(C_pp, 88.5e-12), close(Q_pp, 8.85e-9), close(V_pp / d_pp, 1e5), close(U_pp, 8.85e-7),
           close(Q_pp / A_pp, 8.85e-7)], "abce")
add(T, "Capacitors and dielectrics", "Intermediate", "multi_statement",
    multi("A parallel plate capacitor has plates of area 0.01 m² separated by 1 mm of air and is connected to a "
          "100 V battery. Taking ε₀ = 8.85 × 10⁻¹² C² N⁻¹ m⁻², which of the following statements are correct?",
          ["Its capacitance is 88.5 pF.",
           "The charge on each plate has magnitude 8.85 nC.",
           "The electric field between the plates is 10⁵ V/m.",
           "The energy stored in the capacitor is 8.85 × 10⁻⁷ J.",
           "The surface charge density on each plate has magnitude 8.85 × 10⁻⁷ C/m²."]),
    place("(a), (b), (c) and (e) only", ["(a), (b) and (d) only", "(b), (c), (d) and (e) only",
                                         "(a), (c) and (d) only"], "B"),
    "Parallel plate capacitor: C, Q, E, U and σ",
    "C = ε₀A/d, Q = CV, E = V/d, U = ½CV² and σ = Q/A.",
    ["(a) C = 8.85 × 10⁻¹² × 0.01/10⁻³ = 8.85 × 10⁻¹¹ F = 88.5 pF (true)",
     "(b) Q = 88.5 × 10⁻¹² × 100 = 8.85 × 10⁻⁹ C (true)", "(c) E = 100/10⁻³ = 10⁵ V/m (true)",
     "(d) U = ½ × 88.5 × 10⁻¹² × 10⁴ ≈ 4.4 × 10⁻⁷ J, not 8.85 × 10⁻⁷ J (false)",
     "(e) σ = 8.85 × 10⁻⁹/0.01 = 8.85 × 10⁻⁷ C/m² (true)"],
    why="(d) uses CV² without the factor ½; every option containing (d) is wrong.",
    ncert="Class 12 Physics, 'Electrostatic Potential and Capacitance', the parallel plate capacitor and energy "
          "stored in a capacitor", seconds=90, recomputed=True)

add(T, "Capacitors and dielectrics", "Intermediate", "statement_pair",
    SP_STEM.format(
        s1="When a dielectric slab is placed in an external electric field, free charges in it move to its surfaces "
           "and make the field inside it zero, as happens in a conductor.",
        s2="A dielectric placed in an external electric field gets polarised through the displacement or "
           "reorientation of its bound charges, that is, of its molecular dipoles."),
    sp("D"),
    "Conductors versus dielectrics in an external field",
    "A dielectric has no free charges that can move through it. The field stretches non-polar molecules and partly "
    "aligns polar ones, giving a net dipole moment per unit volume. The resulting bound surface charges reduce the "
    "field inside the dielectric but do not cancel it.",
    ["Statement I: describes a conductor, not a dielectric → false",
     "Statement II: polarisation by bound charges → true"],
    why="Statement I is false and Statement II is true, so only D fits.",
    ncert="Class 12 Physics, 'Electrostatic Potential and Capacitance', dielectrics and polarisation", seconds=45)

q4, a4 = 1e-6, 0.3
F0 = k * q4 ** 2 / a4 ** 2
F_net = math.sqrt(2) * F0 + F0 / 2
assert close(F0, 0.1) and close(F_net, 0.1914, 1e-3) and close(math.sqrt(2) * F0, 0.1414, 1e-3) \
    and close(2 * F0 + F0 / 2, 0.25) and close(math.sqrt(2) * F0 + F0 / math.sqrt(2), 0.2121, 1e-3)
add(T, "Coulomb's law and superposition", "Advanced", "numerical",
    "Four identical point charges, each of +1 μC, are fixed at the corners of a square of side 0.3 m in air. Taking "
    "1/(4πε₀) = 9 × 10⁹ N m² C⁻², the magnitude of the net electrostatic force on any one of the charges is about:",
    place("0.19 N", ["0.14 N", "0.25 N", "0.21 N"], "C"),
    "Superposition of Coulomb forces",
    "The two neighbours at distance a push the charge along the two sides; their resultant lies along the diagonal. "
    "The charge at the opposite corner, at distance a√2, also pushes it along the diagonal.",
    ["kq²/a² = 9 × 10⁹ × 10⁻¹²/0.09 = 0.1 N", "Two side forces at 90°: 0.1√2 ≈ 0.141 N along the diagonal",
     "Diagonal charge: kq²/(2a²) = 0.05 N along the diagonal", "Net = 0.141 + 0.05 ≈ 0.19 N"],
    why="0.14 N leaves out the charge at the opposite corner. 0.25 N adds the magnitudes of all three forces as if "
        "they were along one line. 0.21 N uses a√2 instead of (a√2)² for the diagonal force.",
    ncert="Class 12 Physics, 'Electric Charges and Fields', forces between multiple charges", seconds=100,
    recomputed=True)

C1s, C2s, Vmax = 2e-6, 4e-6, 100.0
Qmax = min(C1s, C2s) * Vmax
Vtot = Qmax / C1s + Qmax / C2s
assert close(Vtot, 150) and close(C2s * Vmax / C1s + Vmax, 300)
add(T, "Capacitors and dielectrics", "Advanced", "numerical",
    "A 2 μF capacitor and a 4 μF capacitor, each of which can safely withstand a potential difference of at most "
    "100 V, are connected in series. The largest potential difference that can safely be applied across the series "
    "combination is:",
    place("150 V", ["200 V", "100 V", "300 V"], "B"),
    "Sharing of voltage in a series combination",
    "In series both capacitors carry the same charge, so the smaller capacitance takes the larger voltage (V = Q/C). "
    "The 2 μF capacitor reaches its limit first.",
    ["Limit for 2 μF: Q = 2 μF × 100 V = 200 μC", "Then V across 4 μF = 200 μC/4 μF = 50 V",
     "Maximum total = 100 + 50 = 150 V"],
    why="200 V assumes both can be at 100 V together, which is impossible since they carry equal charges. 100 V "
        "wastes the 4 μF capacitor's share. 300 V lets the 4 μF capacitor reach 100 V, which would put 200 V across "
        "the 2 μF capacitor.",
    ncert="Class 12 Physics, 'Electrostatic Potential and Capacitance', combination of capacitors (in series)",
    seconds=90, recomputed=True)

n_dr = 27
R_ratio = round(n_dr ** (1 / 3))
V_ratio = F(n_dr, R_ratio)
assert R_ratio == 3 and V_ratio == 9
add(T, "Electric potential and energy", "Advanced", "numerical",
    "Twenty-seven identical spherical drops of mercury, each charged to the same potential V, coalesce to form a "
    "single large spherical drop. Taking the potential to be zero at infinity, the potential of the large drop is:",
    place("9V", ["27V", "3V", "V/3"], "D"),
    "Potential of a charged conducting sphere, V = kQ/R",
    "Charge is conserved and so is the volume: the total charge is 27q, and 27 small spheres of radius r make one "
    "sphere of radius 3r.",
    ["Volume: (4/3)πR³ = 27 × (4/3)πr³ → R = 3r", "Charge: Q = 27q",
     "V' = kQ/R = k(27q)/(3r) = 9 kq/r = 9V"],
    why="27V forgets that the radius also grows. 3V takes the radius to grow 9 times. V/3 inverts the radius ratio.",
    ncert="Class 12 Physics, 'Electrostatic Potential and Capacitance', potential due to a point charge (charged "
          "conducting sphere)", seconds=80, recomputed=True)

Rsph, Qsph = 0.09, 3e-6
C_sph = Rsph / k
U_sph = Qsph ** 2 / (2 * C_sph)
assert close(C_sph, 1e-11) and close(U_sph, 0.45) and close(Qsph ** 2 / C_sph, 0.9) \
    and close(Qsph ** 2 / (2 * (9 / k)), 4.5e-3) and close(k * Qsph ** 2 / Rsph ** 2, 10)
add(T, "Capacitors and dielectrics", "Advanced", "numerical",
    "An isolated conducting sphere of radius 9 cm in air carries a charge of 3 μC. Taking 1/(4πε₀) = "
    "9 × 10⁹ N m² C⁻², the electrostatic energy stored in its field is:",
    place("0.45 J", ["0.9 J", "4.5 × 10⁻³ J", "10 J"], "A"),
    "Energy stored by a charged isolated conductor",
    "An isolated sphere has capacitance C = 4πε₀R, and the energy stored when it carries charge Q is Q²/(2C).",
    ["C = R/k = 0.09/(9 × 10⁹) = 10⁻¹¹ F = 10 pF", "U = Q²/(2C) = (3 × 10⁻⁶)²/(2 × 10⁻¹¹) = 0.45 J",
     "Check: V = kQ/R = 3 × 10⁵ V and ½QV = 0.45 J"],
    why="0.9 J leaves out the ½. 4.5 × 10⁻³ J keeps the radius in centimetres. 10 J computes kQ²/R², which is a "
        "force, not an energy.",
    ncert="Class 12 Physics, 'Electrostatic Potential and Capacitance', capacitors and capacitance; energy stored in "
          "a capacitor", seconds=90, recomputed=True)

add(T, "Gauss's law", "Advanced", "assertion_reason",
    AR_STEM.format(
        a="Just outside the surface of a charged conductor in electrostatic equilibrium, the electric field has "
          "magnitude σ/ε₀, which is twice the field σ/(2ε₀) of a large thin plane sheet carrying the same surface "
          "charge density σ.",
        r="Inside the conductor the field is zero, so all the flux through a small pillbox-shaped Gaussian surface "
          "drawn across the conductor's surface leaves through its outer face; for the thin sheet the flux leaves "
          "through both faces of the pillbox."),
    ar("A"),
    "Gauss's law at a conductor's surface versus a sheet of charge",
    "For a pillbox of face area ΔS enclosing charge σΔS, Gauss's law gives total flux σΔS/ε₀. At a conductor the "
    "inner face lies in the conductor (E = 0), so E ΔS = σΔS/ε₀ → E = σ/ε₀. For the sheet the same flux is shared "
    "by two faces, 2EΔS = σΔS/ε₀ → E = σ/(2ε₀).",
    ["Conductor: one face carries all the flux → σ/ε₀", "Sheet: two faces share it → σ/(2ε₀)"],
    why="R is exactly the Gauss's-law reason for the factor of two, so B is wrong; both statements are true, so C "
        "and D are wrong.",
    ncert="Class 12 Physics, 'Electric Charges and Fields', applications of Gauss's law; 'Electrostatic Potential "
          "and Capacitance', electrostatics of conductors", seconds=75)

multi_key([True, True, True, True, False], "abcd")
add(T, "Gauss's law", "Advanced", "multi_statement",
    multi("A point charge +q is placed at the centre of the cavity of a thick, uncharged, conducting spherical shell "
          "of inner radius a and outer radius b. In electrostatic equilibrium, which of the following statements "
          "are correct? (k = 1/(4πε₀); r is the distance from the centre.)",
          ["A charge −q is induced on the inner surface of the shell.",
           "A charge +q appears on the outer surface of the shell.",
           "The electric field within the material of the shell (a < r < b) is zero.",
           "The electric field at a point outside the shell (r > b) has magnitude kq/r².",
           "The electric field everywhere inside the cavity (r < a) is zero."]),
    place("(a), (b), (c) and (d) only", ["(a), (c) and (e) only", "(b), (c), (d) and (e) only",
                                         "(a), (b) and (e) only"], "C"),
    "Gauss's law and conductors: induced charges",
    "In equilibrium the field in the conducting material is zero. A Gaussian sphere drawn inside the material then "
    "has zero flux, so it must enclose zero charge: the inner surface carries −q. The shell is neutral, so +q sits "
    "on the outer surface. Outside, a Gaussian sphere encloses q − q + q = q.",
    ["(a) true: enclosed charge must be zero within the metal", "(b) true: shell is neutral overall",
     "(c) true: electrostatic field inside a conductor is zero", "(d) true: net enclosed charge is +q",
     "(e) false: the cavity contains the charge +q, so the field there is kq/r²"],
    why="The zero-field result for a cavity holds only when the cavity contains no charge, so (e) is false.",
    ncert="Class 12 Physics, 'Electric Charges and Fields', Gauss's law; 'Electrostatic Potential and Capacitance', "
          "electrostatics of conductors", seconds=100)

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
    doc = {"schema_version": "1.0", "batch_id": "BATCH_007", "created_at": TODAY,
           "notes": "BATCH_007 package PHY_007_p1: 129 original Physics questions (Physics and Measurement through "
                    "Electrostatics). Every numerical answer is re-derived in tools/batch_007/PHY_007_p1.py.",
           "stimuli": [], "questions": QUESTIONS}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {OUT}: {n} questions, {dict(Counter(x['difficulty'] for x in QUESTIONS))}")
    print(f"keys {dict(sorted(keys.items()))}")
    print(f"formats {dict(fmts)}")
