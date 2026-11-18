"""Writes batches/parts/BATCH_004_CHE_p1.json: package CHE_004_p1 of BATCH_004 (Chemistry, 126 questions).

Topics: Some Basic Concepts, Atomic Structure, Chemical Bonding, Thermodynamics, Solutions, Equilibrium,
Redox and Electrochemistry, Chemical Kinetics, Periodicity, p-Block Elements. IDs NEET_CHE_000751..000876.

Every computable answer is re-derived here with an assert before anything is written; the quota per
(topic, difficulty), the ID range, the format mix and the answer-key balance are asserted too.
The position of every correct option is chosen by hand in the call that adds the question (argument `at`)
and never moved by code.

    cd docs/neet-bank && python tools/batch_004/CHE_004_p1.py
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
PACKAGE = "CHE_004_p1"
PLAN = ROOT / "batches" / "plans" / "BATCH_004_plan.json"
OUT = ROOT / "batches" / "parts" / "BATCH_004_CHE_p1.json"
TODAY = "2026-11-16"
LETTERS = "ABCD"
CHE = "Chemistry"
FIRST_ID = 751
AUTHORED = ("ai:author-solve", "ai:self-recheck")
RECOMPUTED = ("script:recompute", "ai:author-solve", "ai:self-recheck")

QUESTIONS = []
KEYS = Counter()
_topic = [None]


def topic(name):
    _topic[0] = name


class Opts:
    """Four options with the correct one at a fixed, hand-chosen position."""

    def __init__(self, at, correct, wrong):
        assert at in LETTERS
        assert len(wrong) == 3 and correct not in wrong and len(set(wrong)) == 3, (correct, wrong)
        self.at = at
        self.texts = list(wrong)
        self.texts.insert(LETTERS.index(at), correct)


def combo(*labels):
    """'(a), (c) and (e) only' style option text."""
    parts = [f"({x})" for x in labels]
    return (", ".join(parts[:-1]) + " and " + parts[-1] if len(parts) > 1 else parts[0]) + " only"


def multi(at, truth, wrong):
    """Multi-statement options. truth maps each label to True/False; the correct option lists exactly the true
    ones and no wrong option may equal it."""
    correct = combo(*sorted(k for k, v in truth.items() if v))
    assert all(w != correct for w in wrong)
    return Opts(at, correct, wrong)


def code(m):
    return ", ".join(f"{k}-{m[k]}" for k in "ABCD")


def match(at, correct, wrong):
    """Match-the-list options from dicts like {'A': 'II', ...}; each numeral used once."""
    for m in [correct, *wrong]:
        assert sorted(m.values()) == sorted(["I", "II", "III", "IV"]), m
    return Opts(at, code(correct), [code(w) for w in wrong])


def M(s):
    """'II III I IV' -> {'A': 'II', 'B': 'III', 'C': 'I', 'D': 'IV'}"""
    return dict(zip("ABCD", s.split()))


def lists(intro, left, right):
    """Stem for a match-the-list question."""
    a = "\n".join(f"{k}. {v}" for k, v in zip("ABCD", left))
    b = "\n".join(f"{k}. {v}" for k, v in zip(["I", "II", "III", "IV"], right))
    return (f"{intro}\n\nList-I:\n{a}\n\nList-II:\n{b}\n\n"
            "Choose the correct answer from the options given below:")


def ar(assertion, reason):
    return ("Given below are two statements: one is labelled Assertion (A) and the other is labelled Reason (R).\n\n"
            f"Assertion (A): {assertion}\nReason (R): {reason}\n\n"
            "Choose the correct answer from the options given below:")


def sp(s1, s2):
    return (f"Given below are two statements:\n\nStatement I: {s1}\nStatement II: {s2}\n\n"
            "In the light of the above statements, choose the correct answer from the options given below:")


def ms(intro, items):
    body = "\n".join(f"({k}) {v}" for k, v in zip("abcdefg", items))
    return f"{intro}\n\n{body}\n\nChoose the correct answer from the options given below:"


def add(sub, diff, fmt, text, options, concept, explanation, steps, answer=None, shortcut=None, why=None,
        ncert=None, seconds=60, checked=False):
    if fmt == "assertion_reason":
        assert options is ASSERTION_REASON and answer in LETTERS
        opts = list(options)
    elif fmt == "statement_pair":
        assert options is STATEMENT_PAIR and answer in LETTERS
        opts = list(options)
    else:
        assert isinstance(options, Opts) and answer is None
        opts, answer = options.texts, options.at
    if fmt == "numerical":
        assert checked, "numerical answers must be recomputed by an assert"
    qid = f"NEET_CHE_{FIRST_ID + len(QUESTIONS):06d}"
    KEYS[answer] += 1
    QUESTIONS.append({
        "question_id": qid, "exam_mappings": default_mappings(CHE), "subject": CHE, "topic": _topic[0],
        "subtopic": sub, "difficulty": diff, "question_type": "MCQ", "format": fmt, "language": "en",
        "question_text": text,
        "options": [{"key": LETTERS[i], "text": t} for i, t in enumerate(opts)],
        "correct_answer": answer,
        "solution": {"concept": concept, "explanation": explanation, "steps": steps, "shortcut": shortcut,
                     "why_others_wrong": why, "ncert_reference": ncert,
                     "final_answer": f"Option {answer}: {opts[LETTERS.index(answer)]}"},
        "suggested_time_seconds": seconds,
        "source": {"source_type": "Original", "source_name": "PrepMitra", "source_url": None,
                   "original_exam_year": None, "license_note": None},
        "verification": {"answer_verified": True, "solution_verified": True, "review_status": "Pending Human Review",
                         "verified_by": list(RECOMPUTED if checked else AUTHORED), "verified_at": TODAY},
    })


def close(x, y, tol=0.005):
    """Relative closeness for rounded option values."""
    return abs(x - y) <= tol * abs(y)


B, I, A = "Basic", "Intermediate", "Advanced"
AR_, SP_ = ASSERTION_REASON, STATEMENT_PAIR
C11, C12 = "Class 11 Chemistry", "Class 12 Chemistry"
NA = 6.022e23
H_PLANCK = 6.626e-34
C_LIGHT = 3.0e8

# ==================================================================== 1. Some Basic Concepts in Chemistry
topic("Some Basic Concepts in Chemistry")
REF1 = f"{C11}, 'Some Basic Concepts of Chemistry'"

m_h2so4 = 2 * 1 + 32 + 4 * 16
assert m_h2so4 == 98 and close(0.25 * m_h2so4, 24.5) and close(0.5 * m_h2so4, 49) and close(m_h2so4 / 0.25, 392)
add("Mole concept", B, "numerical",
    "The mass of 0.25 mol of sulphuric acid, H₂SO₄, is (H = 1, S = 32, O = 16):",
    Opts("B", "24.5 g", ["49 g", "392 g", "12.25 g"]),
    "Mass from amount of substance",
    "Mass = amount (mol) × molar mass. The molar mass of H₂SO₄ is 2(1) + 32 + 4(16) = 98 g mol⁻¹.",
    ["M(H₂SO₄) = 2 + 32 + 64 = 98 g mol⁻¹", "Mass = 0.25 mol × 98 g mol⁻¹ = 24.5 g"],
    why="49 g is the mass of 0.5 mol. 392 g comes from dividing the molar mass by 0.25 instead of multiplying. "
        "12.25 g halves the correct answer.",
    ncert=f"{REF1}, mole concept and molar masses", seconds=25, checked=True)

add("Laws of chemical combination", B, "direct",
    "Which of the following is a homogeneous mixture?",
    Opts("D", "Air", ["A mixture of oil and water", "A mixture of grains and pebbles", "A mixture of dirt and stones"]),
    "Homogeneous and heterogeneous mixtures",
    "In a homogeneous mixture the components mix completely and the composition is uniform throughout; air (a "
    "mixture of gases) and a sugar solution are examples. In a heterogeneous mixture the composition is not "
    "uniform and the components can often be seen separately.",
    ["Air: uniform composition throughout → homogeneous",
     "Oil + water, grains + pebbles, dirt + stones: components remain separate → heterogeneous"],
    why="Oil and water form two layers; grains and pebbles, and dirt and stones, can be seen and picked apart, so "
        "these mixtures are heterogeneous.",
    ncert=f"{REF1}, nature of matter: mixtures", seconds=20)

n_w = 3.6 / 18
assert close(n_w * NA, 1.2044e23) and close(3 * n_w * NA, 3.613e23) and close(3.6 * NA, 2.168e24)
add("Mole concept", B, "numerical",
    "The number of water molecules in 3.6 g of water is (H = 1, O = 16, Nₐ = 6.022 × 10²³ mol⁻¹):",
    Opts("A", "1.204 × 10²³", ["3.613 × 10²³", "2.168 × 10²⁴", "6.022 × 10²²"]),
    "Number of molecules from mass",
    "Number of molecules = (mass / molar mass) × Nₐ. The molar mass of water is 18 g mol⁻¹.",
    ["n(H₂O) = 3.6 / 18 = 0.2 mol", "Molecules = 0.2 × 6.022 × 10²³ = 1.204 × 10²³"],
    why="3.613 × 10²³ is the number of atoms (three per molecule), not molecules. 2.168 × 10²⁴ multiplies the "
        "mass in grams by Nₐ without dividing by the molar mass. 6.022 × 10²² corresponds to 0.1 mol.",
    ncert=f"{REF1}, mole concept", seconds=30, checked=True)

m_anh = 63.5 + 32 + 4 * 16
m_hyd = m_anh + 5 * 18
assert close(m_hyd, 249.5) and close(90 / m_hyd * 100, 36.1, 0.002)
assert close(90 / m_anh * 100, 56.4, 0.002) and close(18 / m_hyd * 100, 7.2, 0.005) and close(m_anh / m_hyd * 100, 63.9, 0.002)
add("Mole concept", I, "numerical",
    "The percentage by mass of water of crystallisation in copper sulphate pentahydrate, CuSO₄·5H₂O, is "
    "(Cu = 63.5, S = 32, O = 16, H = 1):",
    Opts("B", "36.1%", ["56.4%", "7.2%", "63.9%"]),
    "Percentage composition",
    "Mass per cent of a component = (mass of the component in one mole / molar mass of the compound) × 100. "
    "One mole of the pentahydrate contains 5 mol of water (90 g).",
    ["M(CuSO₄) = 63.5 + 32 + 64 = 159.5 g mol⁻¹", "M(CuSO₄·5H₂O) = 159.5 + 5 × 18 = 249.5 g mol⁻¹",
     "% water = 90 / 249.5 × 100 = 36.1%"],
    why="56.4% divides the water by the mass of anhydrous CuSO₄ instead of the hydrate. 7.2% counts only one "
        "molecule of water. 63.9% is the percentage of anhydrous CuSO₄ in the hydrate.",
    ncert=f"{REF1}, percentage composition", seconds=50, checked=True)

v_final = 0.5 * 200 / 0.2
assert v_final == 500 and v_final - 200 == 300 and 0.2 * 200 / 0.5 == 80
add("Stoichiometry", I, "numerical",
    "What volume of water must be added to 200 mL of 0.5 M NaOH solution to make its concentration 0.2 M? "
    "(Assume volumes are additive.)",
    Opts("C", "300 mL", ["500 mL", "80 mL", "120 mL"]),
    "Dilution: M₁V₁ = M₂V₂",
    "On dilution the amount of solute does not change, so M₁V₁ = M₂V₂. The final volume is found first; the "
    "water to be added is the final volume minus the initial volume.",
    ["n(NaOH) = 0.5 × 0.200 = 0.10 mol", "Final volume V₂ = 0.5 × 200 / 0.2 = 500 mL",
     "Water to be added = 500 − 200 = 300 mL"],
    shortcut="Concentration falls by a factor 0.5/0.2 = 2.5, so the volume must become 2.5 × 200 = 500 mL.",
    why="500 mL is the final volume, not the water added. 80 mL inverts the ratio (0.2 × 200 / 0.5), and 120 mL "
        "is 200 − 80 from the same inverted ratio.",
    ncert=f"{REF1}, molarity", seconds=40, checked=True)

add("Laws of chemical combination", I, "assertion_reason",
    ar("A chemical equation is balanced so that the total mass of the reactants equals the total mass of the "
       "products.",
       "In every chemical reaction the total number of molecules is conserved."),
    AR_, "Balanced equations and conservation of mass",
    "A balanced equation has the same number of atoms of each element on both sides, which expresses the law "
    "of conservation of mass: A is true. The number of molecules is not necessarily conserved; in 2H₂ + O₂ → "
    "2H₂O, three molecules give two. So R is false.",
    ["Same number of atoms of each element on both sides → masses equal (A true)",
     "2H₂ + O₂ → 2H₂O: 3 molecules → 2 molecules, so molecules are not conserved (R false)"],
    answer="C", ncert=f"{REF1}, balancing a chemical equation", seconds=35)

add("Empirical and molecular formulae", I, "match_list",
    lists("Match List-I (molecular formula) with List-II (empirical formula).",
          ["C₂H₄", "H₂O₂", "N₂O₄", "B₂H₆"],
          ["NO₂", "BH₃", "CH₂", "HO"]),
    match("D", M("III IV I II"), [M("III IV II I"), M("IV III I II"), M("I IV III II")]),
    "Empirical formula as the simplest whole-number ratio",
    "The empirical formula is obtained by dividing the subscripts of the molecular formula by their highest "
    "common factor. Each of these molecular formulae is twice its empirical formula.",
    ["C₂H₄ ÷ 2 = CH₂ → III", "H₂O₂ ÷ 2 = HO → IV", "N₂O₄ ÷ 2 = NO₂ → I", "B₂H₆ ÷ 2 = BH₃ → II"],
    why="The other codes swap NO₂ with BH₃, or CH₂ with HO, or CH₂ with NO₂.",
    ncert=f"{REF1}, empirical and molecular formulae", seconds=35)

x_ca = None
for tenth in range(0, 103):
    x = tenth / 10
    co2 = x / 100 + (10.2 - x) / 84
    if abs(co2 * 44 - 4.84) < 1e-6:
        x_ca = x
assert x_ca is not None and close(x_ca, 6.0) and close(10.2 - x_ca, 4.2)
add("Stoichiometry", A, "numerical",
    "10.2 g of a mixture of CaCO₃ and MgCO₃ is heated strongly until both decompose completely: "
    "MCO₃(s) → MO(s) + CO₂(g). The mass lost as CO₂ is 4.84 g. The mass of CaCO₃ in the mixture is "
    "(Ca = 40, Mg = 24, C = 12, O = 16):",
    Opts("B", "6.0 g", ["4.2 g", "5.1 g", "7.2 g"]),
    "Stoichiometry of a two-component mixture",
    "Each carbonate gives one mole of CO₂ per mole. Let the mass of CaCO₃ be x g; then MgCO₃ is (10.2 − x) g. "
    "The total moles of CO₂ equal the moles of the two carbonates.",
    ["Moles of CO₂ = 4.84 / 44 = 0.11 mol", "x/100 + (10.2 − x)/84 = 0.11",
     "84x + 100(10.2 − x) = 0.11 × 8400 = 924 → 1020 − 16x = 924 → x = 6.0 g",
     "Check: 6.0/100 + 4.2/84 = 0.06 + 0.05 = 0.11 mol"],
    why="4.2 g is the mass of MgCO₃, not CaCO₃. 5.1 g assumes equal masses. 7.2 g does not satisfy the CO₂ "
        "balance (7.2/100 + 3.0/84 = 0.108 mol).",
    ncert=f"{REF1}, stoichiometry and stoichiometric calculations", seconds=120, checked=True)

assert F(16, 32) == F(32, 64)
add("Mole concept", A, "statement_pair",
    sp("16 g of O₂ contains twice as many molecules as 32 g of SO₂. (O = 16, S = 32)",
       "One mole of SO₂ contains 3 × 6.022 × 10²³ atoms."),
    SP_, "Comparing numbers of molecules and atoms",
    "Moles of O₂ = 16/32 = 0.5 mol; moles of SO₂ = 32/64 = 0.5 mol. Equal amounts contain equal numbers of "
    "molecules, so Statement I is false. Each SO₂ molecule has three atoms, so one mole of SO₂ has 3Nₐ atoms: "
    "Statement II is true.",
    ["n(O₂) = 16/32 = 0.5 mol; n(SO₂) = 32/64 = 0.5 mol → same number of molecules (I false)",
     "1 mol SO₂ = Nₐ molecules × 3 atoms = 3 × 6.022 × 10²³ atoms (II true)"],
    answer="D", ncert=f"{REF1}, mole concept", seconds=40)

m_alcl3 = 27 + 3 * 35.5
assert close(2 * m_alcl3, 267) and F(3, 2) > 1 and F(2, 3) != 1
add("Stoichiometry", A, "multi_statement",
    ms("For the reaction 2Al(s) + 3Cl₂(g) → 2AlCl₃(s), which of the following statements are correct? "
       "(Al = 27, Cl = 35.5)",
       ["2 mol of Al react with exactly 3 mol of Cl₂.",
        "54 g of Al gives 267 g of AlCl₃ when Cl₂ is in excess.",
        "1 mol of Cl₂ gives 1 mol of AlCl₃.",
        "If 1 mol of Al is mixed with 1 mol of Cl₂, Cl₂ is the limiting reagent.",
        "The total mass of the reactants consumed equals the mass of AlCl₃ formed."]),
    multi("C", {"a": True, "b": True, "c": False, "d": True, "e": True},
          ["(a), (b) and (c) only", "(a), (c), (d) and (e) only", "(b), (d) and (e) only"]),
    "Mole ratios, limiting reagent and conservation of mass",
    "The coefficients give the mole ratio Al : Cl₂ : AlCl₃ = 2 : 3 : 2. M(AlCl₃) = 27 + 106.5 = 133.5 g mol⁻¹.",
    ["(a) True: coefficients 2 and 3",
     "(b) True: 54 g Al = 2 mol → 2 mol AlCl₃ = 2 × 133.5 = 267 g",
     "(c) False: 3 mol Cl₂ → 2 mol AlCl₃, so 1 mol Cl₂ → 2/3 mol AlCl₃",
     "(d) True: 1 mol Al needs 1.5 mol Cl₂; only 1 mol is present, so Cl₂ runs out first",
     "(e) True: mass is conserved"],
    why="Any option containing (c) is wrong, and (a) is true, so '(b), (d) and (e) only' is incomplete.",
    ncert=f"{REF1}, stoichiometry and limiting reagent", seconds=90, checked=True)

# ==================================================================== 2. Atomic Structure
topic("Atomic Structure")
REF2 = f"{C11}, 'Structure of Atom'"

wn = 1 / 400e-9
assert close(wn, 2.5e6) and close(1 / 4e-6, 2.5e5) and close(C_LIGHT / 400e-9, 7.5e14)
add("Bohr model and hydrogen spectrum", B, "numerical",
    "The wavenumber of radiation of wavelength 400 nm is:",
    Opts("C", "2.5 × 10⁶ m⁻¹", ["2.5 × 10⁵ m⁻¹", "7.5 × 10¹⁴ m⁻¹", "4.0 × 10⁻⁷ m⁻¹"]),
    "Wavenumber",
    "Wavenumber is the number of wavelengths per unit length: ν̄ = 1/λ. In SI units λ must be in metres.",
    ["λ = 400 nm = 4.00 × 10⁻⁷ m", "ν̄ = 1/λ = 1/(4.00 × 10⁻⁷ m) = 2.5 × 10⁶ m⁻¹"],
    why="2.5 × 10⁵ m⁻¹ converts 400 nm to 4 × 10⁻⁶ m (wrong power of ten). 7.5 × 10¹⁴ is the frequency c/λ "
        "in s⁻¹, not the wavenumber. 4.0 × 10⁻⁷ is the wavelength itself.",
    ncert=f"{REF2}, wave nature of electromagnetic radiation", seconds=25, checked=True)

add("Electronic configuration", B, "direct",
    "The nuclides ¹⁴₆C and ¹⁴₇N are:",
    Opts("B", "Isobars", ["Isotopes", "Isotones", "Isoelectronic atoms"]),
    "Isotopes and isobars",
    "Isobars are atoms with the same mass number but different atomic numbers. Both nuclides have mass number "
    "14, while their atomic numbers are 6 and 7.",
    ["Mass numbers: 14 and 14 (same)", "Atomic numbers: 6 and 7 (different) → isobars"],
    why="Isotopes have the same atomic number. The neutron numbers are 8 and 7, so they are not isotones. The "
        "neutral atoms have 6 and 7 electrons, so they are not isoelectronic.",
    ncert=f"{REF2}, isobars and isotopes", seconds=20)

z_br, a_br = 35, 80
assert (z_br, a_br - z_br, z_br + 1) == (35, 45, 36)
add("Electronic configuration", B, "numerical",
    "The numbers of protons, neutrons and electrons in the ion ⁸⁰₃₅Br⁻ are respectively:",
    Opts("D", "35, 45, 36", ["35, 45, 34", "35, 80, 36", "36, 44, 35"]),
    "Composition of an ion",
    "The atomic number gives the protons; neutrons = mass number − atomic number; a singly negative ion has one "
    "electron more than the number of protons.",
    ["Protons = Z = 35", "Neutrons = 80 − 35 = 45", "Electrons = 35 + 1 = 36 (charge −1)"],
    why="35, 45, 34 treats the ion as Br⁺. 35, 80, 36 takes the mass number as the neutron count. 36, 44, 35 "
        "puts the extra charge on the protons.",
    ncert=f"{REF2}, atomic number and mass number", seconds=25, checked=True)

L3 = 3 * H_PLANCK / (2 * 3.14)
assert close(L3, 3.16e-34) and close(H_PLANCK / (2 * 3.14), 1.055e-34) and close(9 * H_PLANCK / (2 * 3.14), 9.50e-34)
assert close(3 * H_PLANCK, 1.99e-33)
add("Bohr model and hydrogen spectrum", I, "numerical",
    "According to Bohr's model, the angular momentum of the electron in the third orbit (n = 3) of a hydrogen "
    "atom is (h = 6.626 × 10⁻³⁴ J s, π = 3.14):",
    Opts("A", "3.16 × 10⁻³⁴ J s", ["1.05 × 10⁻³⁴ J s", "9.50 × 10⁻³⁴ J s", "1.99 × 10⁻³³ J s"]),
    "Quantisation of angular momentum in Bohr's model",
    "Bohr postulated that the angular momentum of the electron is quantised: mvr = nh/2π, where n is the orbit "
    "number.",
    ["mvr = nh/2π = 3 × 6.626 × 10⁻³⁴ / (2 × 3.14)", "= 1.988 × 10⁻³³ / 6.28 = 3.16 × 10⁻³⁴ J s"],
    why="1.05 × 10⁻³⁴ J s is the value for n = 1. 9.50 × 10⁻³⁴ J s uses n² instead of n. 1.99 × 10⁻³³ J s "
        "omits the division by 2π.",
    ncert=f"{REF2}, Bohr's model for hydrogen atom", seconds=45, checked=True)

ie_mol = 2.18e-18 * NA / 1000
assert close(ie_mol, 1313, 0.001) and close(ie_mol / 4, 328, 0.002)
add("Bohr model and hydrogen spectrum", I, "numerical",
    "The energy of the electron in the nth orbit of a hydrogen atom is Eₙ = −2.18 × 10⁻¹⁸ (1/n²) J. The energy "
    "needed to ionise one mole of hydrogen atoms in their ground state is (Nₐ = 6.022 × 10²³ mol⁻¹):",
    Opts("B", "1313 kJ mol⁻¹", ["328 kJ mol⁻¹", "1313 J mol⁻¹", "2626 kJ mol⁻¹"]),
    "Ionisation energy from Bohr energies",
    "Ionisation takes the electron from n = 1 to n = ∞, where its energy is zero. The energy per atom is "
    "multiplied by Nₐ to get the energy per mole.",
    ["Per atom: ΔE = 0 − (−2.18 × 10⁻¹⁸ J) = 2.18 × 10⁻¹⁸ J",
     "Per mole: 2.18 × 10⁻¹⁸ × 6.022 × 10²³ = 1.313 × 10⁶ J = 1313 kJ mol⁻¹"],
    why="328 kJ mol⁻¹ is the energy to ionise from n = 2. 1313 J mol⁻¹ misses the factor of 1000 between J and "
        "kJ. 2626 kJ mol⁻¹ doubles the value.",
    ncert=f"{REF2}, energy of the electron in Bohr orbits", seconds=50, checked=True)

add("Bohr model and hydrogen spectrum", I, "direct",
    "In Rutherford's α-particle scattering experiment, which observation showed that most of the space in an "
    "atom is empty?",
    Opts("C", "Most of the α-particles passed through the gold foil undeflected",
         ["A small fraction of the α-particles was deflected by small angles",
          "A very few α-particles (about 1 in 20 000) bounced back",
          "The α-particles were attracted towards the gold foil"]),
    "Conclusions of Rutherford's scattering experiment",
    "Since most of the α-particles went straight through the foil, there was nothing in their way over most of "
    "the volume of the atom: most of the space in an atom is empty. Small deflections showed that the positive "
    "charge is concentrated, and the rare rebounds showed that this charge and most of the mass are in a very "
    "small nucleus.",
    ["Undeflected passage of most α-particles → most of the atom is empty space",
     "Deflections and rebounds → small, dense, positively charged nucleus"],
    why="Small-angle deflections and rebounds point to a concentrated positive nucleus, not to empty space. "
        "α-particles are positive and are repelled, not attracted, by the nucleus.",
    ncert=f"{REF2}, Rutherford's nuclear model of atom", seconds=30)

add("Electronic configuration", I, "statement_pair",
    sp("Isotopes of an element have almost identical chemical properties.",
       "The chemical properties of an atom are controlled mainly by the number of its electrons, which is fixed "
       "by the number of protons in the nucleus."),
    SP_, "Chemical properties of isotopes",
    "Isotopes differ only in the number of neutrons. The number of protons, and hence of electrons in the "
    "neutral atom, is the same, so their chemical behaviour is almost the same. Both statements are true.",
    ["Isotopes: same Z, different neutron numbers", "Same number of electrons → nearly identical chemistry"],
    answer="A", ncert=f"{REF2}, isobars and isotopes", seconds=30)

add("Electronic configuration", I, "match_list",
    lists("Match List-I (ion in its ground state) with List-II (electronic configuration). "
          "(Z: Na = 11, Cl = 17, Cr = 24, Zn = 30)",
          ["Na⁺", "Cl⁻", "Zn²⁺", "Cr³⁺"],
          ["[Ar] 3d³", "1s² 2s² 2p⁶", "[Ar] 3d¹⁰", "1s² 2s² 2p⁶ 3s² 3p⁶"]),
    match("D", M("II IV III I"), [M("II IV I III"), M("IV II III I"), M("II III IV I")]),
    "Electronic configurations of ions",
    "A cation is formed by removing electrons from the outermost (highest n) shell first, so the 4s electrons "
    "of Zn and Cr go before any 3d electrons. An anion adds electrons to the next available orbital.",
    ["Na⁺: 10 electrons → 1s² 2s² 2p⁶ → II", "Cl⁻: 18 electrons → 1s² 2s² 2p⁶ 3s² 3p⁶ → IV",
     "Zn ([Ar] 3d¹⁰ 4s²) → Zn²⁺ = [Ar] 3d¹⁰ → III", "Cr ([Ar] 3d⁵ 4s¹) → Cr³⁺ = [Ar] 3d³ → I"],
    why="The other codes swap Zn²⁺ with Cr³⁺, Na⁺ with Cl⁻, or Cl⁻ with Zn²⁺.",
    ncert=f"{REF2}, electronic configuration of atoms", seconds=50)

lam_inf = 4 / 1.097e7
assert close(lam_inf * 1e9, 364.6, 0.001) and close(36 / (5 * 1.097e7) * 1e9, 656.3, 0.001)
assert close(1e9 / 1.097e7, 91.2, 0.002)
add("Bohr model and hydrogen spectrum", A, "numerical",
    "The shortest wavelength in the Balmer series of the hydrogen spectrum is (R_H = 1.097 × 10⁷ m⁻¹; "
    "1/λ = R_H (1/n₁² − 1/n₂²)):",
    Opts("B", "364.6 nm", ["656.3 nm", "91.2 nm", "121.5 nm"]),
    "Series limit of a spectral series",
    "The Balmer series has n₁ = 2. The shortest wavelength (highest energy) corresponds to the electron falling "
    "from n₂ = ∞, the series limit.",
    ["1/λ = R_H (1/2² − 1/∞²) = R_H/4", "λ = 4/R_H = 4 / (1.097 × 10⁷ m⁻¹) = 3.646 × 10⁻⁷ m = 364.6 nm"],
    why="656.3 nm is the longest-wavelength Balmer line (n = 3 → 2). 91.2 nm is the Lyman series limit "
        "(n₁ = 1). 121.5 nm is the first Lyman line.",
    ncert=f"{REF2}, line spectrum of hydrogen", seconds=60, checked=True)

add("Dual nature and uncertainty", A, "assertion_reason",
    ar("The photoelectric effect can be fully explained by the wave theory of light.",
       "According to the wave theory, the energy carried by a light beam depends on its intensity and not on "
       "its frequency."),
    AR_, "Failure of the wave theory for the photoelectric effect",
    "If the energy of light depended only on its intensity, electrons should be ejected by light of any "
    "frequency, given enough intensity, and their kinetic energy should rise with intensity. Experiment shows a "
    "threshold frequency and kinetic energy that depends on frequency. Einstein explained this with photons of "
    "energy hν. So A is false. R correctly states what the wave theory says, so R is true.",
    ["Observed: threshold frequency; KE depends on frequency, not intensity",
     "Wave theory (R) predicts the opposite → wave theory fails (A false)", "Photon picture E = hν explains it"],
    answer="D", ncert=f"{REF2}, photoelectric effect", seconds=45)

add("Bohr model and hydrogen spectrum", A, "multi_statement",
    ms("For a hydrogen-like species described by Bohr's model, which of the following statements are correct?",
       ["For a given nucleus, the radius of the orbit is proportional to n².",
        "The magnitude of the energy of the electron is proportional to 1/n².",
        "The speed of the electron increases as n increases.",
        "The energy gap between successive orbits decreases as n increases.",
        "The radius of the first orbit of He⁺ is twice that of the first orbit of hydrogen."]),
    multi("A", {"a": True, "b": True, "c": False, "d": True, "e": False},
          ["(a), (b) and (c) only", "(b), (d) and (e) only", "(a), (c) and (e) only"]),
    "Bohr model: radius, energy and speed",
    "For a hydrogen-like species rₙ = 52.9 (n²/Z) pm, Eₙ = −2.18 × 10⁻¹⁸ (Z²/n²) J and the speed of the "
    "electron is proportional to Z/n.",
    ["(a) True: r ∝ n²", "(b) True: |E| ∝ 1/n²", "(c) False: v ∝ 1/n, so the electron is slower in outer orbits",
     "(d) True: e.g. E₂ − E₁ = ¾ unit but E₃ − E₂ = 5/36 unit (in units of 2.18 × 10⁻¹⁸ J)",
     "(e) False: r ∝ 1/Z, so the He⁺ (Z = 2) first orbit is half that of hydrogen"],
    why="Options with (c) or (e) are wrong; (d) is true, so '(a), (b) and (c) only' also fails.",
    ncert=f"{REF2}, Bohr's model for hydrogen atom", seconds=75)

# ==================================================================== 3. Chemical Bonding and Molecular Structure
topic("Chemical Bonding and Molecular Structure")
REF3 = f"{C11}, 'Chemical Bonding and Molecular Structure'"

add("Hybridisation and resonance", B, "direct",
    "Which of the following is an odd-electron molecule?",
    Opts("B", "NO", ["CO", "N₂", "O₂"]),
    "Odd-electron molecules: an exception to the octet rule",
    "A molecule with an odd total number of electrons cannot give every atom an octet. Nitric oxide has "
    "7 + 8 = 15 electrons (11 valence electrons), an odd number.",
    ["NO: 7 + 8 = 15 electrons → odd", "CO: 14, N₂: 14, O₂: 16 → even"],
    why="CO, N₂ and O₂ all have an even number of electrons.",
    ncert=f"{REF3}, limitations of the octet rule: odd-electron molecules", seconds=20)

ve_co3 = 4 + 3 * 6 + 2
assert ve_co3 == 24 and 4 + 3 * 6 == 22
add("VSEPR shapes", B, "numerical",
    "The total number of valence electrons to be shown in the Lewis structure of the carbonate ion, CO₃²⁻, is:",
    Opts("D", "24", ["22", "26", "32"]),
    "Counting electrons for a Lewis structure",
    "Add the valence electrons of all atoms, then add one electron for each unit of negative charge (or remove "
    "one for each unit of positive charge).",
    ["C: 4; O: 3 × 6 = 18", "Charge −2: add 2 electrons", "Total = 4 + 18 + 2 = 24"],
    why="22 ignores the charge. 26 adds the charge twice. 32 gives every atom a full octet (4 × 8) instead of "
        "counting valence electrons.",
    ncert=f"{REF3}, Lewis representation of simple molecules", seconds=25, checked=True)

add("Hybridisation and resonance", B, "statement_pair",
    sp("A σ bond is formed by head-on (axial) overlap of atomic orbitals along the internuclear axis.",
       "A π bond is stronger than a σ bond between the same two atoms."),
    SP_, "Sigma and pi bonds",
    "A σ bond results from end-to-end overlap along the internuclear axis, so Statement I is true. In a π bond "
    "the orbitals overlap sideways and the extent of overlap is smaller, so a π bond is weaker than a σ bond: "
    "Statement II is false.",
    ["σ: axial overlap (I true)", "π: sideways overlap, smaller extent → weaker than σ (II false)"],
    answer="C", ncert=f"{REF3}, strength of sigma and pi bonds", seconds=25)

add("VSEPR shapes", B, "match_list",
    lists("Match List-I (scientists) with List-II (theory of chemical bonding they proposed or developed).",
          ["Kössel and Lewis", "Sidgwick and Powell", "Heitler and London", "Hund and Mulliken"],
          ["Valence bond theory", "Molecular orbital theory", "Electronic theory of chemical bonding (octet)",
           "Valence shell electron pair repulsion (VSEPR) theory"]),
    match("A", M("III IV I II"), [M("III IV II I"), M("IV III I II"), M("III I IV II")]),
    "History of bonding theories",
    "Kössel and Lewis (1916) explained bonding through the octet. Sidgwick and Powell (1940) proposed the "
    "electron-pair repulsion idea later developed into VSEPR. Heitler and London introduced valence bond theory "
    "(1927). Hund and Mulliken developed molecular orbital theory (1932).",
    ["Kössel–Lewis → III", "Sidgwick–Powell → IV", "Heitler–London → I", "Hund–Mulliken → II"],
    why="The other codes interchange VB theory with MO theory, or the octet theory with VSEPR.",
    ncert=f"{REF3}, Kössel–Lewis approach, VSEPR theory, valence bond theory, molecular orbital theory",
    seconds=30)

add("Hybridisation and resonance", B, "direct",
    "Taking z as the internuclear axis, which of the following pairs of atomic orbitals gives zero overlap and "
    "therefore cannot form a bond?",
    Opts("C", "2pₓ of one atom and 2p_y of the other",
         ["1s of one atom and 1s of the other", "2p_z of one atom and 2p_z of the other",
          "2pₓ of one atom and 2pₓ of the other"]),
    "Positive, negative and zero overlap",
    "Orbitals with different symmetry about the internuclear axis cannot overlap effectively. A pₓ and a p_y "
    "orbital are perpendicular to each other, so their positive and negative overlaps cancel: the net overlap is "
    "zero.",
    ["1s + 1s: σ (s–s overlap)", "2p_z + 2p_z along z: σ (head-on)", "2pₓ + 2pₓ: π (sideways)",
     "2pₓ + 2p_y: perpendicular → zero overlap, no bond"],
    why="s–s and p_z–p_z overlap head-on to form σ bonds; two parallel pₓ orbitals overlap sideways to form a π "
        "bond.",
    ncert=f"{REF3}, types of overlapping and nature of covalent bonds", seconds=30)

assert close(100 / 3, 33.3, 0.002) and 100 / 4 == 25 and 100 / 2 == 50
add("Hybridisation and resonance", I, "numerical",
    "The percentage s-character of the hybrid orbitals used by boron to form the B–F bonds in BF₃ is:",
    Opts("B", "33.3%", ["25%", "50%", "66.7%"]),
    "s-character of hybrid orbitals",
    "Boron in BF₃ has three bond pairs and no lone pair, so it is sp² hybridised. An sp² hybrid orbital is made "
    "from one s and two p orbitals, so it has one-third s-character.",
    ["BF₃: 3 bond pairs, 0 lone pairs → sp²", "s-character = 1/(1 + 2) × 100 = 33.3%"],
    why="25% is for sp³ and 50% for sp. 66.7% is the p-character of an sp² orbital.",
    ncert=f"{REF3}, hybridisation: sp² hybridisation", seconds=30, checked=True)

lp_o3 = (18 - 2 * 3) // 2
assert lp_o3 == 6 and (2 + 1 + 3) == lp_o3
add("VSEPR shapes", I, "numerical",
    "In a Lewis structure of ozone, O=O–O, in which every atom obeys the octet rule, the total number of lone "
    "pairs of electrons on all three oxygen atoms is:",
    Opts("D", "6", ["1", "9", "5"]),
    "Lone pairs in a Lewis structure",
    "Ozone has 3 × 6 = 18 valence electrons. One double bond and one single bond use three shared pairs (6 "
    "electrons); the remaining 12 electrons form 6 lone pairs.",
    ["Valence electrons = 18", "Bonding electrons: O=O (4) + O–O (2) = 6",
     "Lone-pair electrons = 18 − 6 = 12 → 6 lone pairs",
     "Distribution: double-bonded terminal O 2, central O 1, single-bonded terminal O 3"],
    why="1 counts only the lone pair on the central atom. 9 assumes three lone pairs on every atom. 5 gives the "
        "single-bonded terminal oxygen only two lone pairs, leaving it without an octet.",
    ncert=f"{REF3}, Lewis structures and resonance in ozone", seconds=45, checked=True)

add("Fajans' rule and dipole moment", I, "direct",
    "According to Fajans' rules, which of the following chlorides has the greatest covalent character?",
    Opts("C", "AlCl₃", ["NaCl", "MgCl₂", "KCl"]),
    "Polarising power of cations",
    "The covalent character of an ionic compound increases with the polarising power of the cation, which is "
    "greater for a cation of higher charge and smaller size. Al³⁺ has the highest charge and the smallest size "
    "among Na⁺, Mg²⁺, Al³⁺ and K⁺.",
    ["Charge: Al³⁺ > Mg²⁺ > Na⁺ = K⁺", "Size: Al³⁺ < Mg²⁺ < Na⁺ < K⁺",
     "Greatest polarising power → Al³⁺ → AlCl₃ most covalent"],
    why="Na⁺, Mg²⁺ and K⁺ have lower charge and larger size; KCl is the most ionic of the four.",
    ncert=f"{REF3}, ionic and covalent character (Fajans' rules)", seconds=30)

add("Hybridisation and resonance", I, "assertion_reason",
    ar("Hybrid orbitals form stronger bonds than the pure atomic orbitals from which they are made.",
       "A hybrid orbital is concentrated in one direction, so it overlaps more effectively with the orbital of "
       "the other atom."),
    AR_, "Why hybrid orbitals form stable bonds",
    "Hybrid orbitals have a larger lobe pointing towards the bonded atom. The greater extent of overlap gives "
    "a stronger bond; this is why hybridised orbitals are more effective in forming stable bonds. Both "
    "statements are true and R explains A.",
    ["Bond strength depends on the extent of overlap",
     "Hybrid orbital: one large directed lobe → better overlap (R) → stronger bond (A)"],
    answer="A", ncert=f"{REF3}, hybridisation: salient features", seconds=35)

add("Hybridisation and resonance", I, "statement_pair",
    sp("In ethene, each carbon atom uses sp² hybrid orbitals to form the C–C σ bond.",
       "The π bond in ethene is formed by sideways overlap of the unhybridised 2p orbitals of the two carbon "
       "atoms."),
    SP_, "Bonding in ethene",
    "Each carbon in ethene is sp² hybridised: one sp²–sp² overlap gives the C–C σ bond and two sp²–1s overlaps "
    "give the C–H bonds. The remaining unhybridised 2p orbital on each carbon overlaps sideways to form the π "
    "bond. Both statements are true.",
    ["C–C σ: sp²–sp² overlap (I true)", "C–C π: sideways overlap of unhybridised 2p orbitals (II true)"],
    answer="A", ncert=f"{REF3}, formation of double bond in ethene", seconds=30)

add("VSEPR shapes", I, "match_list",
    lists("Match List-I (species) with List-II (shape predicted by VSEPR theory).",
          ["H₃O⁺", "NH₂⁻", "SiCl₄", "ICl₄⁻"],
          ["Square planar", "Tetrahedral", "Bent (V-shaped)", "Trigonal pyramidal"]),
    match("B", M("IV III II I"), [M("III IV II I"), M("IV III I II"), M("II III IV I")]),
    "Shapes from bond pairs and lone pairs",
    "Count the bond pairs and lone pairs on the central atom; the lone pairs occupy positions of the electron "
    "geometry but are not counted in the shape.",
    ["H₃O⁺: 3 bp + 1 lp (tetrahedral arrangement) → trigonal pyramidal → IV",
     "NH₂⁻: 2 bp + 2 lp → bent → III", "SiCl₄: 4 bp + 0 lp → tetrahedral → II",
     "ICl₄⁻: 4 bp + 2 lp (octahedral arrangement, lone pairs trans) → square planar → I"],
    why="The other codes swap pyramidal with bent, tetrahedral with square planar, or confuse H₃O⁺ with SiCl₄.",
    ncert=f"{REF3}, VSEPR theory: shapes of molecules with lone pairs", seconds=60)

add("Ionic bonding and lattice enthalpy", I, "multi_statement",
    ms("Which of the following favour the formation of an ionic bond between a metal and a non-metal?",
       ["A small difference in the electronegativities of the two elements",
        "A low ionisation enthalpy of the metal atom",
        "A more negative electron gain enthalpy of the non-metal atom",
        "A large positive electron gain enthalpy of the non-metal atom",
        "A high lattice enthalpy of the ionic solid formed"]),
    multi("D", {"a": False, "b": True, "c": True, "d": False, "e": True},
          ["(a), (b) and (c) only", "(b), (c), (d) and (e) only", "(a), (d) and (e) only"]),
    "Conditions for ionic bond formation",
    "An ionic bond forms easily when the metal loses electrons easily (low ionisation enthalpy), the non-metal "
    "gains them readily (negative electron gain enthalpy), and the energy released when the lattice forms is "
    "large. A large electronegativity difference, not a small one, favours ionic bonding.",
    ["(a) False: a small difference favours covalent bonding", "(b) True", "(c) True",
     "(d) False: a positive electron gain enthalpy opposes anion formation", "(e) True"],
    why="Any option with (a) or (d) is wrong.",
    ncert=f"{REF3}, ionic or electrovalent bond", seconds=50)

ax = [(0, 0, 1), (0, 0, -1)]
eq = [(math.cos(t), math.sin(t), 0) for t in (0, 2 * math.pi / 3, 4 * math.pi / 3)]
vecs = ax + eq
angs = [round(math.degrees(math.acos(max(-1, min(1, sum(p * q for p, q in zip(u, v)))))))
        for i, u in enumerate(vecs) for v in vecs[i + 1:]]
assert Counter(angs) == Counter({90: 6, 120: 3, 180: 1})
add("VSEPR shapes", A, "numerical",
    "In the trigonal bipyramidal PCl₅ molecule, consider all the Cl–P–Cl bond angles. The numbers of angles "
    "equal to 90° and to 120° are respectively:",
    Opts("A", "6 and 3", ["3 and 6", "12 and 0", "6 and 2"]),
    "Geometry of a trigonal bipyramid",
    "PCl₅ has two axial and three equatorial P–Cl bonds. Each axial bond is at 90° to each equatorial bond, the "
    "three equatorial bonds are at 120° to one another and the two axial bonds are at 180°. Five bonds give "
    "5 × 4 / 2 = 10 angles in all.",
    ["Axial–equatorial: 2 × 3 = 6 angles of 90°", "Equatorial–equatorial: 3 angles of 120°",
     "Axial–axial: 1 angle of 180°", "Check: 6 + 3 + 1 = 10 = ⁵C₂"],
    why="3 and 6 interchanges the two counts. 12 and 0 is the count of 90° angles in an octahedron. 6 and 2 "
        "miscounts the equatorial pairs (three bonds make three pairs).",
    ncert=f"{REF3}, shape of PCl₅ (sp³d hybridisation)", seconds=60, checked=True)

add("Molecular orbital theory", A, "assertion_reason",
    ar("The O–O bond in O₂⁺ is longer than the O–O bond in O₂.",
       "When O₂ is ionised to O₂⁺, the electron is removed from an antibonding π* orbital, so the bond order "
       "rises from 2 to 2.5."),
    AR_, "Bond order and bond length from MO theory",
    "O₂ has the configuration ... π*2pₓ¹ π*2p_y¹ with bond order (10 − 6)/2 = 2. Removing an antibonding "
    "electron gives O₂⁺ with bond order (10 − 5)/2 = 2.5, so R is true. A higher bond order means a shorter "
    "bond, so O₂⁺ has a shorter, not longer, bond than O₂: A is false.",
    ["O₂: Nb = 10, Na = 6 → bond order 2", "O₂⁺: Nb = 10, Na = 5 → bond order 2.5 (R true)",
     "Higher bond order → shorter bond → O₂⁺ shorter (A false)"],
    answer="D", ncert=f"{REF3}, bond order and bond length", seconds=45)

assert (2 - 0) / 2 == 1 and (4 - 4) / 2 == 0
add("Molecular orbital theory", A, "statement_pair",
    sp("According to molecular orbital theory, the Li₂ molecule is paramagnetic.",
       "According to molecular orbital theory, the Be₂ molecule has a bond order of zero and is not expected to "
       "be stable."),
    SP_, "MO configurations of Li₂ and Be₂",
    "Li₂ (6 electrons): σ1s² σ*1s² σ2s². All electrons are paired, so it is diamagnetic; bond order = "
    "(4 − 2)/2 = 1. Statement I is false. Be₂ (8 electrons): σ1s² σ*1s² σ2s² σ*2s², bond order = (4 − 4)/2 = 0, "
    "so the molecule is not expected to exist as a stable species. Statement II is true.",
    ["Li₂: σ2s² → no unpaired electron → diamagnetic (I false)",
     "Be₂: σ2s² σ*2s² → bond order 0 → unstable (II true)"],
    answer="D", ncert=f"{REF3}, bonding in some homonuclear diatomic molecules", seconds=50)

add("Hybridisation and resonance", A, "multi_statement",
    ms("In which of the following species is the central atom sp³ hybridised AND carries at least one lone pair "
       "of electrons?",
       ["H₂O", "SF₄", "NH₄⁺", "PCl₃", "OF₂"]),
    multi("B", {"a": True, "b": False, "c": False, "d": True, "e": True},
          ["(a), (b) and (d) only", "(c), (d) and (e) only", "(a), (b), (d) and (e) only"]),
    "Hybridisation from the steric number",
    "The number of bond pairs plus lone pairs on the central atom (steric number) gives the hybridisation: 4 → "
    "sp³, 5 → sp³d.",
    ["(a) H₂O: 2 bp + 2 lp → sp³ with lone pairs ✓", "(b) SF₄: 4 bp + 1 lp = 5 → sp³d ✗",
     "(c) NH₄⁺: 4 bp + 0 lp → sp³ but no lone pair ✗", "(d) PCl₃: 3 bp + 1 lp → sp³ ✓",
     "(e) OF₂: 2 bp + 2 lp → sp³ ✓"],
    why="SF₄ is sp³d, and NH₄⁺ has no lone pair, so options containing (b) or (c) are wrong.",
    ncert=f"{REF3}, hybridisation and VSEPR theory", seconds=60)

add("VSEPR shapes", A, "direct",
    "Which of the following is the correct order of bond angles?",
    Opts("C", "H₂O < NH₃ < CH₄ < BF₃",
         ["NH₃ < H₂O < CH₄ < BF₃", "H₂O < NH₃ < BF₃ < CH₄", "CH₄ < NH₃ < H₂O < BF₃"]),
    "Effect of lone pairs and geometry on bond angles",
    "BF₃ is trigonal planar (120°). CH₄ is a regular tetrahedron (109.5°). In NH₃ one lone pair compresses the "
    "angle to about 107°, and in H₂O two lone pairs compress it further to about 104.5°.",
    ["H₂O 104.5° < NH₃ 107° < CH₄ 109.5° < BF₃ 120°"],
    why="Two lone pairs (H₂O) repel bond pairs more than one (NH₃), so NH₃ < H₂O is wrong. The trigonal planar "
        "angle (120°) is larger than the tetrahedral angle, and CH₄ has no lone pair to reduce its angle.",
    ncert=f"{REF3}, VSEPR theory", seconds=40)

add("Hybridisation and resonance", A, "match_list",
    lists("Match List-I (species) with List-II (hybridisation of the central atom).",
          ["SF₄", "PF₆⁻", "SO₃", "Carbon atom in HCN"],
          ["sp³d²", "sp", "sp³d", "sp²"]),
    match("D", M("III I IV II"), [M("I III IV II"), M("III I II IV"), M("IV I III II")]),
    "Hybridisation from the steric number",
    "Steric number = bond pairs (σ bonds) + lone pairs on the central atom. 2 → sp, 3 → sp², 5 → sp³d, "
    "6 → sp³d².",
    ["SF₄: 4 σ + 1 lp = 5 → sp³d → III", "PF₆⁻: 6 σ + 0 lp = 6 → sp³d² → I",
     "SO₃: 3 σ + 0 lp = 3 → sp² → IV", "C in H–C≡N: 2 σ + 0 lp = 2 → sp → II"],
    why="The other codes interchange sp³d with sp³d² or sp with sp²; π bonds do not count in the steric number.",
    ncert=f"{REF3}, hybridisation", seconds=60)

# ==================================================================== 4. Chemical Thermodynamics
topic("Chemical Thermodynamics")
REF4 = f"{C11}, 'Thermodynamics'"

q_w = (36 / 18) * 75.3 * 10
assert close(q_w, 1506) and close(q_w / 2, 753) and close(36 * 75.3 * 10, 27108) and close(q_w / 10, 150.6)
add("First law, work and enthalpy", B, "numerical",
    "The heat needed to raise the temperature of 36 g of liquid water from 298 K to 308 K at constant pressure "
    "is (molar heat capacity of water, C_p,m = 75.3 J K⁻¹ mol⁻¹; H = 1, O = 16):",
    Opts("C", "1506 J", ["753 J", "27.1 kJ", "150.6 J"]),
    "Heat from heat capacity: q = n C_m ΔT",
    "The heat absorbed is the amount of substance × molar heat capacity × temperature rise.",
    ["n = 36 / 18 = 2 mol", "ΔT = 308 − 298 = 10 K", "q = 2 × 75.3 × 10 = 1506 J"],
    why="753 J uses 1 mol. 27.1 kJ multiplies the mass in grams by the molar heat capacity. 150.6 J leaves out "
        "the temperature rise.",
    ncert=f"{REF4}, heat capacity and the relation q = C ΔT", seconds=30, checked=True)

add("First law, work and enthalpy", B, "direct",
    "Hot coffee kept in an ideal, perfectly insulated and closed thermos flask is an example of:",
    Opts("A", "An isolated system",
         ["A closed system", "An open system", "A system that exchanges matter but not energy with the "
                                               "surroundings"]),
    "Types of thermodynamic systems",
    "An isolated system exchanges neither energy nor matter with its surroundings. The closed, perfectly "
    "insulated flask lets no coffee or vapour out and no heat in or out.",
    ["Matter exchange: none (closed lid)", "Energy exchange: none (perfect insulation) → isolated system"],
    why="A closed system can exchange energy, and an open system both energy and matter. A system that exchanges "
        "matter but not energy is not one of the standard types.",
    ncert=f"{REF4}, types of the system", seconds=20)

add("Hess's law and enthalpies", B, "statement_pair",
    sp("The standard enthalpy of a reaction is its enthalpy change when all the reactants and products are in "
       "their standard states.",
       "The standard state of a substance at a given temperature is its pure form at 1 bar."),
    SP_, "Standard enthalpy of reaction",
    "Both statements reproduce the definitions used in thermochemistry: ΔrH° refers to all participants in "
    "their standard states, and the standard state is the pure substance at 1 bar at the specified "
    "temperature (usually 298 K).",
    ["Statement I: definition of ΔrH° (true)", "Statement II: definition of standard state (true)"],
    answer="A", ncert=f"{REF4}, standard enthalpy of reactions", seconds=25)

dg = -50 - 300 * (-100) / 1000
assert close(dg, -20) and close(-50 + 300 * (-100) / 1000, -80)
add("Entropy and Gibbs energy", B, "numerical",
    "For a reaction at 300 K, ΔH = −50 kJ mol⁻¹ and ΔS = −100 J K⁻¹ mol⁻¹. The Gibbs energy change ΔG is:",
    Opts("B", "−20 kJ mol⁻¹", ["−80 kJ mol⁻¹", "+20 kJ mol⁻¹", "−50 kJ mol⁻¹"]),
    "Gibbs energy: ΔG = ΔH − TΔS",
    "Use ΔG = ΔH − TΔS with ΔS converted to kJ.",
    ["TΔS = 300 × (−0.100) = −30 kJ mol⁻¹", "ΔG = −50 − (−30) = −20 kJ mol⁻¹"],
    why="−80 kJ mol⁻¹ adds TΔS instead of subtracting it. +20 kJ mol⁻¹ has the wrong sign. −50 kJ mol⁻¹ ignores "
        "the entropy term.",
    ncert=f"{REF4}, Gibbs energy and spontaneity", seconds=30, checked=True)

heat_g = 9.0 / 180 * 2808
assert close(heat_g, 140.4) and close(9 * 2808, 25272) and close(2808 / 180, 15.6)
add("Hess's law and enthalpies", I, "numerical",
    "The standard enthalpy of combustion of glucose (C₆H₁₂O₆, molar mass 180 g mol⁻¹) is −2808 kJ mol⁻¹. The "
    "heat released when 9.0 g of glucose is burnt completely is:",
    Opts("D", "140.4 kJ", ["2808 kJ", "25 272 kJ", "15.6 kJ"]),
    "Enthalpy of combustion",
    "The enthalpy of combustion refers to one mole; the heat released is proportional to the amount burnt.",
    ["n = 9.0 / 180 = 0.050 mol", "Heat released = 0.050 × 2808 = 140.4 kJ"],
    why="2808 kJ is for one mole. 25 272 kJ multiplies by the mass instead of the amount. 15.6 kJ is the heat per "
        "gram.",
    ncert=f"{REF4}, enthalpy of combustion", seconds=30, checked=True)

d_hu = 2 * 8.314 * 50
assert close(d_hu, 831.4) and close(d_hu / 2, 415.7)
add("First law, work and enthalpy", I, "numerical",
    "2 mol of an ideal gas is heated from 300 K to 350 K. The value of ΔH − ΔU for this change is "
    "(R = 8.314 J K⁻¹ mol⁻¹):",
    Opts("B", "831.4 J", ["415.7 J", "0 J", "1663 J"]),
    "Relation between ΔH and ΔU for an ideal gas",
    "H = U + pV, and for an ideal gas pV = nRT. Hence ΔH − ΔU = Δ(pV) = nRΔT, whatever the path.",
    ["ΔH − ΔU = nRΔT", "= 2 × 8.314 × 50 = 831.4 J"],
    why="415.7 J uses n = 1. 0 J assumes ΔH = ΔU, which is true only when ΔT = 0 for an ideal gas. 1663 J "
        "doubles the result.",
    ncert=f"{REF4}, enthalpy, H", seconds=35, checked=True)

add("Entropy and Gibbs energy", I, "assertion_reason",
    ar("Some endothermic processes are spontaneous at constant temperature and pressure.",
       "For such processes the entropy increase is large enough that TΔS exceeds ΔH, which makes ΔG negative."),
    AR_, "Spontaneity of endothermic processes",
    "The criterion of spontaneity at constant T and p is ΔG = ΔH − TΔS < 0. A positive ΔH can be outweighed by "
    "a large positive TΔS, as in the melting of ice above 273 K or the evaporation of water. R gives exactly "
    "this reason, so both are true and R explains A.",
    ["ΔG = ΔH − TΔS", "ΔH > 0 but TΔS > ΔH → ΔG < 0 → spontaneous"],
    answer="A", ncert=f"{REF4}, spontaneity: is decrease in enthalpy a criterion for spontaneity?", seconds=35)

add("First law, work and enthalpy", I, "statement_pair",
    sp("For a reaction carried out at constant volume, the heat absorbed is equal to ΔH.",
       "For a gaseous reaction in which the number of moles of gas does not change, ΔH is greater than ΔU."),
    SP_, "Heat at constant volume and at constant pressure",
    "At constant volume no pV work is done, so q_V = ΔU, not ΔH: Statement I is false. ΔH = ΔU + Δn_g RT; when "
    "Δn_g = 0, ΔH = ΔU, so Statement II is false.",
    ["q_V = ΔU (I false)", "ΔH − ΔU = Δn_g RT = 0 when Δn_g = 0 (II false)"],
    answer="B", ncert=f"{REF4}, measurement of ΔU and ΔH", seconds=35)

add("Entropy and Gibbs energy", I, "match_list",
    lists("Match List-I (process) with List-II (signs of ΔH and ΔS of the system).",
          ["Melting of ice at 1 bar", "Condensation of steam at 1 bar",
           "2H₂O₂(l) → 2H₂O(l) + O₂(g)", "3O₂(g) → 2O₃(g)"],
          ["ΔH < 0, ΔS > 0", "ΔH > 0, ΔS < 0", "ΔH > 0, ΔS > 0", "ΔH < 0, ΔS < 0"]),
    match("C", M("III IV I II"), [M("IV III I II"), M("III IV II I"), M("I IV III II")]),
    "Signs of ΔH and ΔS",
    "Melting absorbs heat and makes the system more disordered. Condensation releases heat and reduces "
    "disorder. Decomposition of hydrogen peroxide is exothermic and produces a gas. Conversion of oxygen to "
    "ozone is endothermic and reduces the number of gas molecules (3 → 2).",
    ["Melting: ΔH > 0, ΔS > 0 → III", "Condensation: ΔH < 0, ΔS < 0 → IV",
     "H₂O₂ decomposition: ΔH < 0, gas formed → ΔS > 0 → I", "O₃ formation: ΔH > 0, Δn_g = −1 → ΔS < 0 → II"],
    why="The other codes interchange melting with condensation, or the two chemical reactions.",
    ncert=f"{REF4}, entropy and spontaneity", seconds=50)

dfh_cs2 = -393.5 + 2 * (-297.0) - (-1100.0)
assert close(dfh_cs2, 112.5) and close(-393.5 - 297.0 + 1100.0, 409.5) and close(-393.5 - 594 - 1100, -2087.5)
add("Hess's law and enthalpies", A, "numerical",
    "Given at 298 K: C(graphite) + O₂(g) → CO₂(g), ΔH = −393.5 kJ mol⁻¹; S(rhombic) + O₂(g) → SO₂(g), "
    "ΔH = −297.0 kJ mol⁻¹; CS₂(l) + 3O₂(g) → CO₂(g) + 2SO₂(g), ΔH = −1100.0 kJ mol⁻¹. The standard enthalpy of "
    "formation of CS₂(l) is:",
    Opts("D", "+112.5 kJ mol⁻¹", ["−112.5 kJ mol⁻¹", "+409.5 kJ mol⁻¹", "−2087.5 kJ mol⁻¹"]),
    "Hess's law of constant heat summation",
    "Target: C(graphite) + 2S(rhombic) → CS₂(l). Add the formation of CO₂ and of two moles of SO₂, then reverse "
    "the combustion of CS₂.",
    ["C + O₂ → CO₂: −393.5", "2S + 2O₂ → 2SO₂: 2 × (−297.0) = −594.0",
     "CO₂ + 2SO₂ → CS₂ + 3O₂: +1100.0", "Sum: ΔfH(CS₂) = −393.5 − 594.0 + 1100.0 = +112.5 kJ mol⁻¹"],
    shortcut="ΔfH(CS₂) = ΣΔfH(products of combustion) − ΔcH(CS₂).",
    why="−112.5 has the wrong sign. +409.5 uses only one mole of SO₂. −2087.5 adds the combustion enthalpy "
        "instead of reversing it.",
    ncert=f"{REF4}, Hess's law of constant heat summation", seconds=90, checked=True)

add("Entropy and Gibbs energy", A, "direct",
    "Which of the following reactions is non-spontaneous at room temperature but becomes spontaneous at a "
    "sufficiently high temperature?",
    Opts("B", "CaCO₃(s) → CaO(s) + CO₂(g)",
         ["N₂(g) + 3H₂(g) → 2NH₃(g)", "CH₄(g) + 2O₂(g) → CO₂(g) + 2H₂O(l)", "H₂O(l) → H₂O(s)"]),
    "Temperature dependence of spontaneity",
    "A reaction that is non-spontaneous at low temperature but spontaneous at high temperature must have ΔH > 0 "
    "and ΔS > 0, so that TΔS outweighs ΔH only when T is large. Decomposition of CaCO₃ is endothermic and "
    "produces a gas.",
    ["CaCO₃ → CaO + CO₂: ΔH > 0, ΔS > 0 → spontaneous only at high T",
     "NH₃ formation: ΔH < 0, ΔS < 0 → spontaneous at low T",
     "Combustion of CH₄: strongly exothermic → spontaneous at room temperature",
     "Freezing of water: ΔH < 0, ΔS < 0 → spontaneous only below 273 K"],
    why="Formation of ammonia and freezing of water are favoured at low temperature, and combustion of methane "
        "is already spontaneous at room temperature.",
    ncert=f"{REF4}, effect of temperature on spontaneity of reactions", seconds=50)

add("Hess's law and enthalpies", A, "assertion_reason",
    ar("At 298 K, the standard enthalpy of formation of H₂O(l) is more negative than that of H₂O(g).",
       "The conversion of water vapour into liquid water absorbs heat."),
    AR_, "Enthalpy of formation and phase changes",
    "H₂(g) + ½O₂(g) → H₂O(l) can be written as formation of H₂O(g) followed by condensation. Condensation "
    "releases heat (it is the reverse of vaporisation, which absorbs heat), so ΔfH°(H₂O, l) is more negative "
    "than ΔfH°(H₂O, g): A is true. R says condensation absorbs heat, which is false.",
    ["ΔfH°(l) = ΔfH°(g) + ΔcondH", "ΔcondH = −ΔvapH < 0 → ΔfH°(l) more negative (A true)",
     "Condensation releases heat (R false)"],
    answer="C", ncert=f"{REF4}, enthalpy of phase transformation and Hess's law", seconds=40)

add("First law, work and enthalpy", A, "multi_statement",
    ms("Which of the following statements are correct?",
       ["For a system taken through a complete cycle back to its initial state, ΔU = 0.",
        "Heat (q) and work (w) are state functions.",
        "When an ideal gas expands adiabatically and does work on the surroundings, its temperature falls.",
        "For the isothermal expansion of an ideal gas between the same initial and final states, the work done "
        "by the gas is greater when the expansion is reversible than when it is against a constant external "
        "pressure equal to the final pressure.",
        "Molar heat capacity is an extensive property."]),
    multi("A", {"a": True, "b": False, "c": True, "d": True, "e": False},
          ["(a), (b) and (c) only", "(c), (d) and (e) only", "(a), (c), (d) and (e) only"]),
    "First law: state functions, adiabatic and reversible work",
    "U is a state function, so its change over a cycle is zero. q and w depend on the path. In an adiabatic "
    "process q = 0, so ΔU = w; when the gas does work, w < 0, ΔU < 0 and the temperature of an ideal gas falls. "
    "A reversible expansion is carried out against a pressure only infinitesimally smaller than that of the gas "
    "at every stage, so it gives the maximum work. Any molar quantity is intensive.",
    ["(a) True", "(b) False: q and w are path functions", "(c) True: ΔU = w < 0 → T falls",
     "(d) True: reversible work is the maximum work", "(e) False: molar heat capacity is intensive"],
    why="Any option containing (b) or (e) is wrong, and (d) is true.",
    ncert=f"{REF4}, the first law; work; reversible and irreversible processes", seconds=75)

# ==================================================================== 5. Solutions
topic("Solutions")
REF5 = f"{C12}, 'Solutions'"

ppm = 5.0e-3 / 500 * 1e6
assert close(ppm, 10)
add("Concentration terms", B, "numerical",
    "A 500 g sample of water contains 5.0 mg of dissolved oxygen. The concentration of oxygen in parts per "
    "million (by mass) is:",
    Opts("D", "10 ppm", ["1 ppm", "100 ppm", "0.01 ppm"]),
    "Parts per million",
    "ppm (by mass) = (mass of component / total mass of solution) × 10⁶. Since the oxygen is a trace, the mass "
    "of the solution is essentially 500 g.",
    ["Mass of O₂ = 5.0 mg = 5.0 × 10⁻³ g", "ppm = (5.0 × 10⁻³ / 500) × 10⁶ = 10 ppm"],
    why="1 ppm and 100 ppm are off by a factor of ten each way (milligram–gram slips). 0.01 ppm uses 10³ "
        "instead of 10⁶.",
    ncert=f"{REF5}, expressing concentration of solutions: parts per million", seconds=30, checked=True)

add("Raoult's law and ideal solutions", B, "direct",
    "On fractional distillation, a mixture of ethanol and water gives a constant-boiling mixture containing "
    "about 95% ethanol by volume. This mixture is:",
    Opts("B", "A minimum-boiling azeotrope formed by a solution showing positive deviation from Raoult's law",
         ["A maximum-boiling azeotrope formed by a solution showing negative deviation from Raoult's law",
          "A minimum-boiling azeotrope formed by a solution showing negative deviation from Raoult's law",
          "An ideal solution that can be separated completely by fractional distillation"]),
    "Azeotropes",
    "Solutions that show a large positive deviation from Raoult's law form minimum-boiling azeotropes at a "
    "particular composition. The ethanol–water azeotrope (about 95% ethanol by volume) is such a mixture, so "
    "pure ethanol cannot be obtained from it by fractional distillation.",
    ["Large positive deviation → maximum in vapour pressure → minimum boiling point",
     "Ethanol–water → minimum-boiling azeotrope at about 95% ethanol"],
    why="Maximum-boiling azeotropes come from negative deviation (e.g. nitric acid–water). An azeotrope is not "
        "separable by fractional distillation, and the solution is not ideal.",
    ncert=f"{REF5}, azeotropes", seconds=30)

add("Colligative properties", B, "statement_pair",
    sp("The unit of the molal elevation constant (K_b) is K kg mol⁻¹.",
       "A 1 molal aqueous solution contains 1 mol of solute in 1 L of solution."),
    SP_, "Molality and the ebullioscopic constant",
    "From ΔT_b = K_b m, K_b = ΔT_b / m has the unit K / (mol kg⁻¹) = K kg mol⁻¹: Statement I is true. "
    "Molality is moles of solute per kilogram of solvent; 1 mol per litre of solution defines a 1 molar "
    "solution. Statement II is false.",
    ["K_b = ΔT_b / m → K kg mol⁻¹ (I true)", "1 molal = 1 mol per kg of solvent, not per L of solution (II false)"],
    answer="C", ncert=f"{REF5}, elevation of boiling point", seconds=25)

m_sol = (1.0 / 250) / 0.050
kf = 0.40 / m_sol
assert close(m_sol, 0.08) and close(kf, 5.0) and close(m_sol / 0.40, 0.20) and close(0.40 / ((1.0 / 250) / 50), 5000) and close(0.40 / (1.0 / 250), 100)
add("Colligative properties", I, "numerical",
    "1.0 g of a non-volatile, non-electrolyte solute of molar mass 250 g mol⁻¹ is dissolved in 50 g of a "
    "solvent. The freezing point of the solvent is lowered by 0.40 K. The molal depression constant K_f of the "
    "solvent is:",
    Opts("A", "5.0 K kg mol⁻¹", ["0.20 K kg mol⁻¹", "100 K kg mol⁻¹", "5.0 × 10³ K kg mol⁻¹"]),
    "Depression of freezing point: ΔT_f = K_f m",
    "Find the molality from the data, then K_f = ΔT_f / m.",
    ["n(solute) = 1.0 / 250 = 0.0040 mol", "m = 0.0040 mol / 0.050 kg = 0.080 mol kg⁻¹",
     "K_f = 0.40 / 0.080 = 5.0 K kg mol⁻¹"],
    why="0.20 is m/ΔT_f (inverted). 100 divides ΔT_f by the moles of solute instead of the molality. 5.0 × 10³ "
        "keeps the solvent mass in grams.",
    ncert=f"{REF5}, depression of freezing point", seconds=45, checked=True)

x_1m = 1 / (1 + 1000 / 18)
assert close(x_1m, 0.0177, 0.003) and close(18 / 1000, 0.0180) and close(1 - x_1m, 0.982, 0.001)
add("Concentration terms", I, "numerical",
    "The mole fraction of the solute in a 1.00 molal aqueous solution is (H = 1, O = 16):",
    Opts("C", "0.0177", ["0.0180", "0.982", "1.00"]),
    "Converting molality to mole fraction",
    "A 1.00 m solution has 1.00 mol of solute in 1000 g of water. The mole fraction of the solute is its moles "
    "divided by the total moles.",
    ["n(water) = 1000 / 18 = 55.6 mol", "x(solute) = 1.00 / (1.00 + 55.6) = 1.00 / 56.6 = 0.0177"],
    why="0.0180 divides by the moles of water only, forgetting the solute in the total. 0.982 is the mole "
        "fraction of water. 1.00 confuses molality with mole fraction.",
    ncert=f"{REF5}, mole fraction and molality", seconds=40, checked=True)

add("Raoult's law and ideal solutions", I, "assertion_reason",
    ar("Raoult's law can be regarded as a special case of Henry's law.",
       "Both laws state that the partial vapour pressure of a volatile component is proportional to its mole "
       "fraction in the solution; in Raoult's law the proportionality constant is the vapour pressure of the "
       "pure component (p°) instead of K_H."),
    AR_, "Raoult's law and Henry's law",
    "Henry's law: p = K_H x. Raoult's law for a volatile component: p = p° x. Both are of the form p ∝ x; "
    "Raoult's law is Henry's law with K_H = p°. R states precisely this, so R explains A.",
    ["Henry: p = K_H x", "Raoult: p = p° x", "Raoult's law = Henry's law with K_H = p°"],
    answer="A", ncert=f"{REF5}, Raoult's law as a special case of Henry's law", seconds=35)

add("Raoult's law and ideal solutions", I, "match_list",
    lists("Match List-I (pair of liquids) with List-II (behaviour of the solution).",
          ["n-Hexane and n-heptane", "Ethanol and acetone", "Phenol and aniline", "Nitric acid and water"],
          ["Positive deviation; hydrogen bonds of one component are broken on mixing",
           "Maximum-boiling azeotrope at about 68% acid by mass",
           "Nearly ideal solution",
           "Negative deviation; hydrogen bonds form between molecules of the two different liquids"]),
    match("B", M("III I IV II"), [M("III I II IV"), M("I III IV II"), M("III IV I II")]),
    "Ideal and non-ideal solutions",
    "Liquids of very similar structure (n-hexane and n-heptane) form nearly ideal solutions. Acetone gets in "
    "between ethanol molecules and breaks some of their hydrogen bonds, giving positive deviation. The phenolic "
    "–OH hydrogen bonds to the nitrogen of aniline, so A–B attraction is stronger, giving negative deviation. "
    "Nitric acid and water show a large negative deviation and form a maximum-boiling azeotrope with about 68% "
    "nitric acid.",
    ["n-Hexane + n-heptane → III", "Ethanol + acetone → I", "Phenol + aniline → IV", "HNO₃ + water → II"],
    why="The other codes interchange the ideal and positive-deviation pairs, or put phenol–aniline at the "
        "nitric-acid azeotrope.",
    ncert=f"{REF5}, ideal and non-ideal solutions; azeotropes", seconds=55)

m_tot = (0.6 / 60 + 1.8 / 180) / 0.100
dtb = 0.52 * m_tot
assert close(m_tot, 0.2) and close(dtb, 0.104) and close(0.52 * 0.1, 0.052) and close(0.52 * 0.02, 0.0104)
add("Colligative properties", A, "numerical",
    "0.6 g of urea (molar mass 60 g mol⁻¹) and 1.8 g of glucose (molar mass 180 g mol⁻¹) are dissolved together "
    "in 100 g of water. The boiling point of the solution at 1 atm is (K_b of water = 0.52 K kg mol⁻¹; boiling "
    "point of water = 100 °C):",
    Opts("D", "100.104 °C", ["100.052 °C", "100.010 °C", "100.208 °C"]),
    "Colligative properties depend on the total number of solute particles",
    "Both solutes are non-volatile non-electrolytes. The elevation of boiling point depends on the total "
    "molality of all solute particles.",
    ["n(urea) = 0.6 / 60 = 0.010 mol; n(glucose) = 1.8 / 180 = 0.010 mol",
     "Total molality = 0.020 mol / 0.100 kg = 0.20 mol kg⁻¹", "ΔT_b = 0.52 × 0.20 = 0.104 K",
     "Boiling point = 100 + 0.104 = 100.104 °C"],
    why="100.052 °C counts only one solute. 100.010 °C forgets to convert 100 g into 0.100 kg. 100.208 °C doubles "
        "the molality.",
    ncert=f"{REF5}, elevation of boiling point", seconds=60, checked=True)

add("Raoult's law and ideal solutions", A, "multi_statement",
    ms("Two volatile liquids A and B form an ideal solution. At the temperature of interest, the vapour pressure "
       "of pure A is greater than that of pure B (p°A > p°B). Which of the following statements are correct?",
       ["At a given external pressure, the solution boils at a lower temperature than pure A.",
        "The vapour in equilibrium with the solution is richer in A than the liquid is.",
        "The mole fraction of B in the vapour is greater than its mole fraction in the liquid.",
        "The total vapour pressure of the solution lies between p°B and p°A.",
        "A plot of total vapour pressure against the mole fraction of A is a straight line."]),
    multi("C", {"a": False, "b": True, "c": False, "d": True, "e": True},
          ["(a), (b) and (d) only", "(b), (c) and (e) only", "(a), (b), (d) and (e) only"]),
    "Vapour pressure and vapour composition of an ideal solution",
    "For an ideal solution p_total = p°A x_A + p°B x_B = p°B + (p°A − p°B) x_A, a straight line between p°B and "
    "p°A. The vapour mole fraction y_A = p°A x_A / p_total is greater than x_A because p°A > p_total; the "
    "vapour is richer in the more volatile component A and poorer in B. Since p_total < p°A at every "
    "temperature, the solution must be heated above the boiling point of pure A before it boils.",
    ["(a) False: p_total < p°A, so it boils at a higher temperature than A", "(b) True",
     "(c) False: the vapour is poorer in B", "(d) True", "(e) True"],
    why="Options containing (a) or (c) are wrong.",
    ncert=f"{REF5}, vapour pressure of liquid–liquid solutions (Raoult's law)", seconds=75)

eff = {"urea": 0.10 * 1, "KCl": 0.10 * 2, "Al2(SO4)3": 0.05 * 5, "MgCl2": 0.08 * 3}
assert max(eff, key=eff.get) == "Al2(SO4)3" and sorted(eff.values()) == sorted([0.10, 0.20, 0.25, 0.24])
add("van't Hoff factor", A, "direct",
    "Assuming complete dissociation of the electrolytes, which of the following aqueous solutions has the "
    "highest boiling point?",
    Opts("A", "0.05 m Al₂(SO₄)₃", ["0.10 m urea", "0.10 m KCl", "0.08 m MgCl₂"]),
    "Effective molality i × m",
    "The elevation of boiling point is proportional to i × m, the total molality of solute particles.",
    ["Urea: i = 1 → 0.10", "KCl: i = 2 → 0.20", "Al₂(SO₄)₃ → 2Al³⁺ + 3SO₄²⁻: i = 5 → 0.25",
     "MgCl₂: i = 3 → 0.24", "Largest i × m: Al₂(SO₄)₃"],
    why="Urea (0.10), KCl (0.20) and MgCl₂ (0.24) all give fewer particles per kg than Al₂(SO₄)₃ (0.25), even "
        "though their stated molalities are higher.",
    ncert=f"{REF5}, abnormal molar masses and van't Hoff factor", seconds=50, checked=True)

# ==================================================================== 6. Equilibrium
topic("Equilibrium")
REF6 = f"{C11}, 'Equilibrium'"

oh = 1.0e-14 / 2.0e-3
assert close(oh, 5.0e-12) and close(1.0e-14 * 2.0e-3, 2.0e-17)
add("Acids, bases and pH", B, "numerical",
    "In an aqueous solution at 298 K, [H₃O⁺] = 2.0 × 10⁻³ mol L⁻¹. The hydroxide ion concentration is "
    "(K_w = 1.0 × 10⁻¹⁴ mol² L⁻²):",
    Opts("B", "5.0 × 10⁻¹² mol L⁻¹", ["5.0 × 10⁻¹¹ mol L⁻¹", "2.0 × 10⁻³ mol L⁻¹", "2.0 × 10⁻¹⁷ mol L⁻¹"]),
    "Ionic product of water",
    "In any aqueous solution at 298 K, [H₃O⁺][OH⁻] = K_w = 1.0 × 10⁻¹⁴, so [OH⁻] = K_w / [H₃O⁺].",
    ["[OH⁻] = 1.0 × 10⁻¹⁴ / 2.0 × 10⁻³", "= 0.5 × 10⁻¹¹ = 5.0 × 10⁻¹² mol L⁻¹"],
    why="5.0 × 10⁻¹¹ is a slip in the power of ten. 2.0 × 10⁻³ treats [OH⁻] as equal to [H₃O⁺], true only for a "
        "neutral solution. 2.0 × 10⁻¹⁷ multiplies K_w by [H₃O⁺] instead of dividing.",
    ncert=f"{REF6}, ionisation constant of water and its ionic product", seconds=25, checked=True)

add("Kp, Kc and Le Chatelier", B, "direct",
    "For the gaseous equilibrium 4NH₃(g) + 5O₂(g) ⇌ 4NO(g) + 6H₂O(g), the equilibrium constant expression K_c is:",
    Opts("C", "[NO]⁴[H₂O]⁶ / ([NH₃]⁴[O₂]⁵)",
         ["[NH₃]⁴[O₂]⁵ / ([NO]⁴[H₂O]⁶)", "[NO][H₂O] / ([NH₃][O₂])", "[NO]⁴ / ([NH₃]⁴[O₂]⁵)"]),
    "Law of chemical equilibrium",
    "K_c is the product of the equilibrium concentrations of the products, each raised to its stoichiometric "
    "coefficient, divided by the corresponding product for the reactants. Water here is a gas, so it appears in "
    "the expression.",
    ["Products: [NO]⁴[H₂O]⁶", "Reactants: [NH₃]⁴[O₂]⁵", "K_c = [NO]⁴[H₂O]⁶ / ([NH₃]⁴[O₂]⁵)"],
    why="The first option is the expression for the reverse reaction (1/K_c). The second ignores the "
        "coefficients. The fourth leaves out H₂O(g), which may be omitted only when water is a pure liquid.",
    ncert=f"{REF6}, law of chemical equilibrium and equilibrium constant", seconds=25)

add("Acids, bases and pH", B, "statement_pair",
    sp("At 298 K, a solution of pH 3 has a lower H₃O⁺ concentration than a solution of pH 5.",
       "At 298 K, a solution of pH 9 is acidic."),
    SP_, "The pH scale",
    "pH = −log[H₃O⁺]. A lower pH means a higher [H₃O⁺]: pH 3 has [H₃O⁺] = 10⁻³ M, which is 100 times that of "
    "pH 5 (10⁻⁵ M). So Statement I is false. At 298 K, pH > 7 is basic, so a solution of pH 9 is basic, not "
    "acidic: Statement II is false.",
    ["pH 3 → 10⁻³ M; pH 5 → 10⁻⁵ M → pH 3 is 100 times more acidic (I false)",
     "pH 9 > 7 → basic at 298 K (II false)"],
    answer="B", ncert=f"{REF6}, the pH scale", seconds=25)

add("Hydrolysis and buffers", B, "match_list",
    lists("Match List-I (term) with List-II (meaning).",
          ["Common ion effect", "Buffer solution", "Hydrolysis of a salt", "Solubility product"],
          ["Product of the molar concentrations of the ions in a saturated solution, each raised to the power of "
           "its stoichiometric coefficient",
           "Reaction of the cation and/or anion of a salt with water that changes the pH",
           "Suppression of the ionisation of a weak electrolyte by adding a strong electrolyte having an ion in "
           "common with it",
           "Solution that resists a change in pH when a small amount of acid or base is added"]),
    match("D", M("III IV II I"), [M("IV III II I"), M("III IV I II"), M("II IV III I")]),
    "Terms in ionic equilibrium",
    "Each term is defined in the study of ionic equilibria in solution.",
    ["Common ion effect → III", "Buffer → IV", "Salt hydrolysis → II", "Solubility product → I"],
    why="The other codes interchange the common ion effect with buffer action, or hydrolysis with the solubility "
        "product.",
    ncert=f"{REF6}, common ion effect, hydrolysis of salts, buffer solutions, solubility product", seconds=35)

add("Kp, Kc and Le Chatelier", B, "direct",
    "Which of the following is a homogeneous equilibrium?",
    Opts("A", "N₂(g) + O₂(g) ⇌ 2NO(g)",
         ["CaCO₃(s) ⇌ CaO(s) + CO₂(g)", "H₂O(l) ⇌ H₂O(g)", "C(s) + H₂O(g) ⇌ CO(g) + H₂(g)"]),
    "Homogeneous and heterogeneous equilibria",
    "In a homogeneous equilibrium all the reactants and products are in the same phase. In N₂ + O₂ ⇌ 2NO all "
    "species are gases.",
    ["N₂(g), O₂(g), NO(g): one phase → homogeneous",
     "The other three involve a solid or a liquid together with a gas → heterogeneous"],
    why="CaCO₃/CaO with CO₂, liquid water with its vapour, and carbon with steam each contain more than one "
        "phase.",
    ncert=f"{REF6}, homogeneous and heterogeneous equilibria", seconds=20)

k1, k2 = 4.0e-4, 2.5e5
assert close(k1 * k2, 100) and close(k2 / k1, 6.25e8) and close(k1 / k2, 1.6e-9) and close(k1 + k2, 2.5e5)
add("Kp, Kc and Le Chatelier", I, "numerical",
    "At a certain temperature: N₂(g) + O₂(g) ⇌ 2NO(g), K₁ = 4.0 × 10⁻⁴ and 2NO(g) + O₂(g) ⇌ 2NO₂(g), "
    "K₂ = 2.5 × 10⁵. The equilibrium constant of N₂(g) + 2O₂(g) ⇌ 2NO₂(g) at the same temperature is:",
    Opts("B", "100", ["2.5 × 10⁵", "6.25 × 10⁸", "1.6 × 10⁻⁹"]),
    "Equilibrium constant of a reaction obtained by adding two reactions",
    "When two equations are added, the equilibrium constant of the overall reaction is the product of their "
    "equilibrium constants (the concentration of the common species NO cancels).",
    ["Overall = (1) + (2): N₂ + 2O₂ ⇌ 2NO₂", "K = K₁ × K₂ = 4.0 × 10⁻⁴ × 2.5 × 10⁵ = 100",
     "Check: K₁K₂ = ([NO]²/[N₂][O₂]) × ([NO₂]²/[NO]²[O₂]) = [NO₂]²/([N₂][O₂]²)"],
    why="2.5 × 10⁵ adds the two constants. 6.25 × 10⁸ and 1.6 × 10⁻⁹ divide one by the other, as if one equation "
        "were reversed.",
    ncert=f"{REF6}, equilibrium constant for combined reactions", seconds=45, checked=True)

qc = 0.50 ** 2 / (0.10 * 0.20)
assert close(qc, 12.5) and qc < 50 and close(0.50 / (0.10 * 0.20), 25) and close(1 / qc, 0.08)
add("Kp, Kc and Le Chatelier", I, "numerical",
    "For H₂(g) + I₂(g) ⇌ 2HI(g), K_c = 50 at a certain temperature. A mixture at this temperature has "
    "[H₂] = 0.10 M, [I₂] = 0.20 M and [HI] = 0.50 M. Which of the following is correct?",
    Opts("D", "Q_c = 12.5; the net reaction proceeds in the forward direction",
         ["Q_c = 12.5; the net reaction proceeds in the backward direction",
          "Q_c = 25; the net reaction proceeds in the forward direction",
          "Q_c = 0.08; the net reaction proceeds in the forward direction"]),
    "Reaction quotient and the direction of reaction",
    "Q_c has the same form as K_c but uses the actual concentrations. If Q_c < K_c, the reaction moves forward "
    "(towards products) to reach equilibrium; if Q_c > K_c, it moves backward.",
    ["Q_c = [HI]² / ([H₂][I₂]) = 0.25 / (0.10 × 0.20) = 12.5", "Q_c (12.5) < K_c (50) → net forward reaction"],
    why="With Q_c < K_c the reaction cannot go backward. 25 forgets to square [HI]. 0.08 is the reciprocal of "
        "Q_c (the expression is inverted).",
    ncert=f"{REF6}, predicting the direction of the reaction", seconds=50, checked=True)

add("Hydrolysis and buffers", I, "direct",
    "When solid NH₄Cl is dissolved in an aqueous solution of NH₄OH (ammonia solution), the pH of the solution:",
    Opts("C", "Decreases",
         ["Increases", "Does not change", "Becomes exactly 7"]),
    "Common ion effect on a weak base",
    "NH₄OH ⇌ NH₄⁺ + OH⁻. NH₄Cl is a strong electrolyte and supplies the common ion NH₄⁺, which shifts this "
    "equilibrium to the left. [OH⁻] decreases, so the pH falls (the solution becomes a basic buffer).",
    ["NH₄Cl → NH₄⁺ + Cl⁻ (complete)", "Extra NH₄⁺ suppresses ionisation of NH₄OH → [OH⁻] falls → pH decreases"],
    why="The pH cannot rise because [OH⁻] falls. It does change, and the mixture remains basic (a basic buffer), "
        "so it does not become 7.",
    ncert=f"{REF6}, common ion effect in the ionisation of acids and bases", seconds=30)

add("Acids, bases and pH", I, "assertion_reason",
    ar("Pure water at 350 K is neutral even though its pH is less than 7.",
       "The ionic product of water, K_w, decreases with rise in temperature."),
    AR_, "Neutrality and the effect of temperature on K_w",
    "Ionisation of water is endothermic, so K_w increases with temperature; at 350 K, [H₃O⁺] = √K_w is greater "
    "than 10⁻⁷ M and the pH is below 7. Pure water is still neutral because [H₃O⁺] = [OH⁻]. A is true; R is false "
    "(K_w increases, not decreases, with temperature).",
    ["Pure water: [H₃O⁺] = [OH⁻] at every temperature → neutral",
     "K_w rises with T → [H₃O⁺] > 10⁻⁷ M → pH < 7 (A true)", "K_w increases with T (R false)"],
    answer="C", ncert=f"{REF6}, ionisation constant of water", seconds=40)

add("Kp, Kc and Le Chatelier", I, "statement_pair",
    sp("For H₂(g) + I₂(g) ⇌ 2HI(g) at equilibrium in a closed vessel, adding more H₂ at constant volume and "
       "temperature decreases the amount of HI at the new equilibrium.",
       "Adding more H₂ at constant temperature increases the value of K_c for this reaction."),
    SP_, "Le Chatelier's principle: effect of concentration",
    "Adding a reactant makes Q_c < K_c, so the equilibrium shifts forward and more HI forms: Statement I is "
    "false. K_c depends only on temperature, so it is unchanged: Statement II is false.",
    ["Extra H₂ → Q_c < K_c → shift forward → more HI (I false)", "K_c changes only with temperature (II false)"],
    answer="B", ncert=f"{REF6}, factors affecting equilibria: effect of concentration change", seconds=30)

assert (2 - 1, 2 - 4, 2 - 2, 1 - 2) == (1, -2, 0, -1)
add("Kp, Kc and Le Chatelier", I, "match_list",
    lists("Match List-I (gaseous equilibrium) with List-II (unit of K_p, with pressures in bar).",
          ["N₂O₄(g) ⇌ 2NO₂(g)", "N₂(g) + 3H₂(g) ⇌ 2NH₃(g)", "H₂(g) + I₂(g) ⇌ 2HI(g)", "2NO₂(g) ⇌ N₂O₄(g)"],
          ["bar⁻¹", "No unit", "bar⁻²", "bar"]),
    match("A", M("IV III II I"), [M("I III II IV"), M("IV II III I"), M("III IV II I")]),
    "Units of K_p",
    "The unit of K_p is bar^Δn, where Δn = (moles of gaseous products) − (moles of gaseous reactants).",
    ["N₂O₄ ⇌ 2NO₂: Δn = +1 → bar → IV", "N₂ + 3H₂ ⇌ 2NH₃: Δn = −2 → bar⁻² → III",
     "H₂ + I₂ ⇌ 2HI: Δn = 0 → no unit → II", "2NO₂ ⇌ N₂O₄: Δn = −1 → bar⁻¹ → I"],
    why="The other codes reverse the sign of Δn for the NO₂–N₂O₄ pair, or mix up Δn = 0 and Δn = −2.",
    ncert=f"{REF6}, relationship between K_p and K_c; units of equilibrium constant", seconds=40, checked=True)

add("Kp, Kc and Le Chatelier", I, "multi_statement",
    ms("For the equilibrium PCl₅(g) ⇌ PCl₃(g) + Cl₂(g), ΔH > 0, set up in a closed vessel, which of the following "
       "statements are correct?",
       ["Raising the temperature increases the equilibrium constant.",
        "Compressing the mixture to a smaller volume at constant temperature increases the amount of PCl₅.",
        "Adding a catalyst increases the amount of PCl₃ present at equilibrium.",
        "Removing some Cl₂ at constant volume shifts the equilibrium in the forward direction.",
        "K_p = K_c for this equilibrium."]),
    multi("B", {"a": True, "b": True, "c": False, "d": True, "e": False},
          ["(a), (b), (c) and (d) only", "(b), (d) and (e) only", "(a), (c) and (e) only"]),
    "Le Chatelier's principle",
    "For an endothermic forward reaction, K increases with temperature. Compression favours the side with fewer "
    "moles of gas (1 mol PCl₅ against 2 mol of products). A catalyst speeds up both directions equally and "
    "does not change the equilibrium composition. Removing a product shifts the equilibrium forward. Here "
    "Δn = +1, so K_p = K_c(RT).",
    ["(a) True", "(b) True: fewer gas moles on the left", "(c) False: a catalyst does not shift equilibrium",
     "(d) True", "(e) False: K_p = K_c RT"],
    why="Options with (c) or (e) are wrong; (a), (b) and (d) are all true.",
    ncert=f"{REF6}, factors affecting equilibria", seconds=60)

ip = (2e-4 / 2) * (2e-4 / 2)
assert close(ip, 1.0e-8) and ip > 1.1e-10 and close(2e-4 * 2e-4, 4e-8) and close(2e-4 * 1e-4, 2e-8)
add("Solubility product", A, "numerical",
    "Equal volumes of 2.0 × 10⁻⁴ M BaCl₂ and 2.0 × 10⁻⁴ M Na₂SO₄ solutions are mixed at 298 K. "
    "K_sp(BaSO₄) = 1.1 × 10⁻¹⁰. Which of the following is correct?",
    Opts("C", "Ionic product = 1.0 × 10⁻⁸; BaSO₄ precipitates",
         ["Ionic product = 4.0 × 10⁻⁸; BaSO₄ precipitates",
          "Ionic product = 1.0 × 10⁻⁸; BaSO₄ does not precipitate",
          "Ionic product = 2.0 × 10⁻⁸; BaSO₄ precipitates"]),
    "Predicting precipitation from the ionic product",
    "On mixing equal volumes, each concentration is halved. A precipitate forms when the ionic product "
    "[Ba²⁺][SO₄²⁻] exceeds K_sp.",
    ["After mixing: [Ba²⁺] = [SO₄²⁻] = 1.0 × 10⁻⁴ M", "Ionic product = (1.0 × 10⁻⁴)² = 1.0 × 10⁻⁸",
     "1.0 × 10⁻⁸ > 1.1 × 10⁻¹⁰ → BaSO₄ precipitates"],
    why="4.0 × 10⁻⁸ ignores the dilution on mixing, and 2.0 × 10⁻⁸ dilutes only one solution. An ionic product "
        "larger than K_sp means the solution is supersaturated, so precipitation does occur.",
    ncert=f"{REF6}, solubility product: predicting precipitation", seconds=60, checked=True)

x_co = 0.80 - 0.50
p_co2, p_co = 0.50 - x_co, 2 * x_co
kp_co = p_co ** 2 / p_co2
assert close(x_co, 0.30) and close(kp_co, 1.8) and close(p_co / p_co2, 3.0) and close(p_co ** 2 / x_co, 1.2)
assert close(x_co ** 2 / p_co2, 0.45)
add("Kp, Kc and Le Chatelier", A, "numerical",
    "CO₂ gas at an initial pressure of 0.50 atm is placed with excess solid carbon in a closed vessel and heated "
    "to a fixed temperature: CO₂(g) + C(s) ⇌ 2CO(g). At equilibrium the total pressure is 0.80 atm. K_p at this "
    "temperature is:",
    Opts("D", "1.8 atm", ["3.0 atm", "1.2 atm", "0.45 atm"]),
    "K_p for a heterogeneous equilibrium",
    "The pure solid carbon does not appear in K_p. If CO₂ falls by x atm, CO rises by 2x atm, so the total "
    "pressure rises by x.",
    ["p(CO₂) = 0.50 − x, p(CO) = 2x; total = 0.50 + x = 0.80 → x = 0.30 atm",
     "p(CO₂) = 0.20 atm; p(CO) = 0.60 atm", "K_p = p(CO)² / p(CO₂) = 0.36 / 0.20 = 1.8 atm"],
    why="3.0 atm forgets to square p(CO). 1.2 atm divides by the CO₂ consumed (0.30) instead of the CO₂ left "
        "(0.20). 0.45 atm uses x instead of 2x for p(CO).",
    ncert=f"{REF6}, heterogeneous equilibria", seconds=90, checked=True)

alpha_w = 1.0e-7 / (1000 / 18)
assert close(alpha_w, 1.8e-9, 0.01) and close(1.0e-14 / (1000 / 18), 1.8e-16, 0.01)
add("Acids, bases and pH", A, "numerical",
    "The degree of ionisation of pure water at 298 K is (K_w = 1.0 × 10⁻¹⁴; density of water = 1.0 g mL⁻¹; "
    "H = 1, O = 16):",
    Opts("B", "1.8 × 10⁻⁹", ["1.0 × 10⁻⁷", "1.8 × 10⁻¹⁶", "1.0 × 10⁻¹⁴"]),
    "Degree of ionisation of water",
    "Degree of ionisation = (moles ionised per litre) / (total moles per litre). In pure water [H₃O⁺] = √K_w, "
    "and one litre of water (1000 g) contains 1000/18 = 55.6 mol.",
    ["[H₃O⁺] = √(1.0 × 10⁻¹⁴) = 1.0 × 10⁻⁷ mol L⁻¹", "Molar concentration of water = 1000 / 18 = 55.6 mol L⁻¹",
     "α = 1.0 × 10⁻⁷ / 55.6 = 1.8 × 10⁻⁹"],
    why="1.0 × 10⁻⁷ is [H₃O⁺] itself, not divided by the concentration of water. 1.8 × 10⁻¹⁶ divides K_w instead "
        "of √K_w. 1.0 × 10⁻¹⁴ is K_w.",
    ncert=f"{REF6}, ionisation constant of water", seconds=60, checked=True)

s_ksp = {"AgCl": math.sqrt(1.8e-10), "AgBr": math.sqrt(5.0e-13), "AgI": math.sqrt(8.3e-17),
         "Ag2CrO4": (1.1e-12 / 4) ** (1 / 3)}
assert max(s_ksp, key=s_ksp.get) == "Ag2CrO4" and close(s_ksp["Ag2CrO4"], 6.5e-5, 0.01)
assert close(s_ksp["AgCl"], 1.34e-5, 0.005)
add("Solubility product", A, "direct",
    "At 298 K the solubility products are: AgCl 1.8 × 10⁻¹⁰, AgBr 5.0 × 10⁻¹³, AgI 8.3 × 10⁻¹⁷ and Ag₂CrO₄ "
    "1.1 × 10⁻¹². Which salt has the highest molar solubility in pure water? (√1.8 = 1.34; ∛0.275 = 0.65)",
    Opts("A", "Ag₂CrO₄", ["AgCl", "AgBr", "AgI"]),
    "Molar solubility from K_sp for salts of different formula types",
    "K_sp values can be compared directly only for salts of the same formula type. For AB, K_sp = s²; for A₂B, "
    "K_sp = (2s)²s = 4s³. Molar solubilities must be calculated before comparing.",
    ["AgCl: s = √(1.8 × 10⁻¹⁰) = 1.34 × 10⁻⁵ M", "AgBr: s = √(5.0 × 10⁻¹³) ≈ 7.1 × 10⁻⁷ M",
     "AgI: s = √(8.3 × 10⁻¹⁷) ≈ 9.1 × 10⁻⁹ M",
     "Ag₂CrO₄: 4s³ = 1.1 × 10⁻¹² → s³ = 2.75 × 10⁻¹³ → s = 6.5 × 10⁻⁵ M (highest)"],
    why="AgCl has the largest K_sp but a smaller molar solubility than Ag₂CrO₄, because K_sp of a 2 : 1 salt "
        "varies as s³. AgBr and AgI are much less soluble.",
    ncert=f"{REF6}, solubility product constant", seconds=90, checked=True)

add("Hydrolysis and buffers", A, "assertion_reason",
    ar("The pH of a buffer made of CH₃COOH and CH₃COONa changes greatly when the buffer is diluted ten times "
       "with water.",
       "The pH of such a buffer depends on the ratio [CH₃COO⁻]/[CH₃COOH], as given by the Henderson–Hasselbalch "
       "equation."),
    AR_, "Effect of dilution on buffer pH",
    "pH = pK_a + log([CH₃COO⁻]/[CH₃COOH]). Dilution reduces both concentrations by the same factor, so the ratio "
    "and hence the pH stay practically unchanged. A is false; R is a true statement of the Henderson–"
    "Hasselbalch equation.",
    ["pH = pK_a + log([salt]/[acid]) (R true)", "Dilution: ratio unchanged → pH almost unchanged (A false)"],
    answer="D", ncert=f"{REF6}, buffer solutions: designing a buffer", seconds=40)

# ==================================================================== 7. Redox Reactions and Electrochemistry
topic("Redox Reactions and Electrochemistry")
REF7A = f"{C11}, 'Redox Reactions'"
REF7B = f"{C12}, 'Electrochemistry'"

on_o = F(0 - 2 * (-1), 2)
assert on_o == 1
add("Oxidation number and balancing", B, "numerical",
    "The oxidation number of oxygen in dioxygen difluoride, O₂F₂, is:",
    Opts("C", "+1", ["+2", "−1", "−2"]),
    "Oxidation number rules: fluorine is always −1",
    "Fluorine, the most electronegative element, has oxidation number −1 in all its compounds. The sum of "
    "oxidation numbers in a neutral molecule is zero.",
    ["2x + 2(−1) = 0", "x = +1"],
    why="+2 is the value in OF₂, not O₂F₂. −1 is the value in peroxides, and −2 the usual value; neither applies "
        "when oxygen is bonded to fluorine.",
    ncert=f"{REF7A}, oxidation number", seconds=25, checked=True)

add("Batteries and fuel cells", B, "direct",
    "In the dry (Leclanché) cell, the anode is:",
    Opts("A", "The zinc container",
         ["The carbon (graphite) rod", "The paste of manganese dioxide and carbon",
          "The moist paste of ammonium chloride and zinc chloride"]),
    "Construction of the dry cell",
    "The dry cell has a zinc container that also acts as the anode; the cathode is a carbon (graphite) rod "
    "surrounded by powdered MnO₂ and carbon. The space between is filled with a moist paste of NH₄Cl and ZnCl₂. "
    "At the anode Zn(s) → Zn²⁺(aq) + 2e⁻.",
    ["Anode (oxidation): zinc container", "Cathode: graphite rod in MnO₂ + carbon", "Electrolyte: NH₄Cl + ZnCl₂ paste"],
    why="The graphite rod is the cathode, MnO₂ is reduced at the cathode, and the NH₄Cl–ZnCl₂ paste is the "
        "electrolyte.",
    ncert=f"{REF7B}, batteries: primary batteries", seconds=20)

add("Electrode potential and cells", B, "statement_pair",
    sp("In a galvanic cell, the electrode at which reduction takes place is called the cathode.",
       "In the conventional representation of a galvanic cell, the anode is written on the right-hand side."),
    SP_, "Electrodes and cell notation",
    "Reduction occurs at the cathode and oxidation at the anode, so Statement I is true. By convention the "
    "anode (oxidation half-cell) is written on the left and the cathode on the right, e.g. "
    "Zn(s) | Zn²⁺(aq) || Cu²⁺(aq) | Cu(s). Statement II is false.",
    ["Cathode = reduction (I true)", "Anode on the left, cathode on the right (II false)"],
    answer="C", ncert=f"{REF7B}, galvanic cells and their representation", seconds=25)

add("Conductance and Kohlrausch's law", B, "match_list",
    lists("Match List-I (quantity) with List-II (relation used to obtain it). (R = resistance, κ = conductivity, "
          "c = concentration, l = distance between electrodes, A = area of cross-section, G* = cell constant)",
          ["Conductance (G)", "Conductivity (κ)", "Molar conductivity (Λm)", "Cell constant (G*)"],
          ["κ / c", "l / A", "1 / R", "G* / R"]),
    match("B", M("III IV I II"), [M("IV III I II"), M("III IV II I"), M("I IV III II")]),
    "Conductance, conductivity and molar conductivity",
    "Conductance is the reciprocal of resistance. Since R = ρ l/A, conductivity κ = 1/ρ = (l/A)(1/R) = G*/R. "
    "Molar conductivity is conductivity divided by concentration, and the cell constant is l/A.",
    ["G = 1/R → III", "κ = G*/R → IV", "Λm = κ/c → I", "G* = l/A → II"],
    why="The other codes interchange conductance with conductivity, or molar conductivity with the cell "
        "constant.",
    ncert=f"{REF7B}, conductance of electrolytic solutions", seconds=35)

a_deb = (130 - 120) / (0.2 - 0.1)
lam0 = 130 + a_deb * 0.1
a_wrong = (130 - 120) / (0.04 - 0.01)
assert close(a_deb, 100) and close(lam0, 140) and close(130 + a_wrong * 0.01, 133.3, 0.001)
add("Conductance and Kohlrausch's law", I, "numerical",
    "For a strong electrolyte, Λm = Λ°m − A√c. Its molar conductivity is 120 S cm² mol⁻¹ at c = 0.04 mol L⁻¹ "
    "and 130 S cm² mol⁻¹ at c = 0.01 mol L⁻¹. Its limiting molar conductivity Λ°m is:",
    Opts("D", "140 S cm² mol⁻¹", ["133.3 S cm² mol⁻¹", "125 S cm² mol⁻¹", "130 S cm² mol⁻¹"]),
    "Debye–Hückel–Onsager equation for strong electrolytes",
    "Λm varies linearly with √c. Two data points fix the slope −A and the intercept Λ°m.",
    ["√c = 0.2 and 0.1", "130 − 120 = A(0.2 − 0.1) → A = 100", "Λ°m = 130 + 100 × 0.1 = 140 S cm² mol⁻¹"],
    why="133.3 plots Λm against c instead of √c. 125 is the average of the two values. 130 takes the value at the "
        "lower concentration as the limiting value, without extrapolating to zero concentration.",
    ncert=f"{REF7B}, variation of conductivity and molar conductivity with concentration", seconds=60,
    checked=True)

n_kmno4 = F(1 + 2, 5)
assert n_kmno4 == F(3, 5) and F(1, 5) == F(1, 5) and F(2, 5) == F(2, 5)
add("Oxidation number and balancing", I, "numerical",
    "In acidic medium, KMnO₄ oxidises iron(II) oxalate, FeC₂O₄, completely: Fe²⁺ → Fe³⁺ and C₂O₄²⁻ → 2CO₂, while "
    "MnO₄⁻ is reduced to Mn²⁺. The number of moles of KMnO₄ needed to oxidise 1 mol of FeC₂O₄ is:",
    Opts("B", "0.6", ["0.2", "0.4", "1.67"]),
    "Electron balance in redox titrations",
    "Moles of electrons lost by the reducing agent must equal moles of electrons gained by the oxidising agent. "
    "Both the Fe²⁺ and the oxalate ion in FeC₂O₄ are oxidised.",
    ["Fe²⁺ → Fe³⁺: 1 e⁻; C₂O₄²⁻ → 2CO₂ (C: +3 → +4): 2 e⁻", "Electrons lost per FeC₂O₄ = 3",
     "MnO₄⁻ → Mn²⁺ (Mn: +7 → +2): 5 e⁻ gained", "Moles of KMnO₄ = 3/5 = 0.6"],
    why="0.2 counts only the oxidation of Fe²⁺ and 0.4 only that of oxalate. 1.67 inverts the electron ratio.",
    ncert=f"{REF7A}, balancing of redox reactions", seconds=60, checked=True)

add("Oxidation number and balancing", I, "direct",
    "Which of the following is NOT a redox reaction?",
    Opts("C", "CaCO₃(s) → CaO(s) + CO₂(g)",
         ["Zn(s) + 2HCl(aq) → ZnCl₂(aq) + H₂(g)", "2Mg(s) + O₂(g) → 2MgO(s)", "H₂(g) + Cl₂(g) → 2HCl(g)"]),
    "Identifying redox reactions by oxidation numbers",
    "A reaction is a redox reaction if the oxidation number of at least one element changes. In the "
    "decomposition of CaCO₃, Ca stays +2, C stays +4 and O stays −2.",
    ["CaCO₃ → CaO + CO₂: no change in any oxidation number → not redox",
     "Zn 0 → +2, H +1 → 0; Mg 0 → +2, O 0 → −2; H 0 → +1, Cl 0 → −1 → redox"],
    why="In each of the other three reactions an element changes its oxidation number.",
    ncert=f"{REF7A}, redox reactions in terms of oxidation number", seconds=30)

add("Batteries and fuel cells", I, "assertion_reason",
    ar("A hydrogen–oxygen fuel cell works with an efficiency of about 70%, much higher than that of a thermal "
       "power plant (about 40%).",
       "In a fuel cell, the chemical energy of the fuel is converted directly into electrical energy."),
    AR_, "Efficiency of fuel cells",
    "A thermal power plant first converts chemical energy into heat, then into mechanical and finally electrical "
    "energy, losing energy at each step. A fuel cell converts the free energy of the reaction directly into "
    "electrical energy, which is why its efficiency is much higher. Both statements are true and R explains A.",
    ["Thermal plant: chemical → heat → mechanical → electrical (about 40%)",
     "Fuel cell: chemical → electrical directly (about 70%)"],
    answer="A", ncert=f"{REF7B}, fuel cells", seconds=35)

add("Electrode potential and cells", I, "multi_statement",
    ms("Given the standard reduction potentials Ag⁺/Ag = +0.80 V, Cu²⁺/Cu = +0.34 V, Fe²⁺/Fe = −0.44 V and "
       "Zn²⁺/Zn = −0.76 V, which of the following statements are correct?",
       ["Iron displaces silver from an aqueous solution of AgNO₃.",
        "Copper displaces zinc from an aqueous solution of ZnSO₄.",
        "Among the four metals, silver is the weakest reducing agent.",
        "Among the four cations, Ag⁺ is the strongest oxidising agent.",
        "The standard emf of the cell Zn | Zn²⁺ || Fe²⁺ | Fe is 1.20 V."]),
    multi("A", {"a": True, "b": False, "c": True, "d": True, "e": False},
          ["(a), (b) and (e) only", "(c), (d) and (e) only", "(a), (c), (d) and (e) only"]),
    "Electrochemical series",
    "The higher the reduction potential, the stronger the cation as an oxidising agent and the weaker the metal "
    "as a reducing agent. A metal with a lower E° can reduce the cation of a metal with a higher E°.",
    ["(a) True: E°(Fe²⁺/Fe) < E°(Ag⁺/Ag) → Fe reduces Ag⁺",
     "(b) False: Cu (+0.34) cannot reduce Zn²⁺ (−0.76)",
     "(c) True: Ag⁺/Ag has the highest E° → Ag is the weakest reducing agent", "(d) True",
     "(e) False: E° = −0.44 − (−0.76) = +0.32 V; 1.20 V adds the two potentials"],
    why="Options containing (b) or (e) are wrong.",
    ncert=f"{REF7B}, electrochemical series and electrode potential", seconds=60)

add("Batteries and fuel cells", I, "statement_pair",
    sp("In the hydrogen–oxygen fuel cell, oxygen is oxidised at the anode.",
       "Catalysts such as finely divided platinum or palladium are incorporated into the electrodes of the "
       "hydrogen–oxygen fuel cell."),
    SP_, "Hydrogen–oxygen fuel cell",
    "In this fuel cell hydrogen is oxidised at the anode and oxygen is reduced at the cathode: "
    "O₂(g) + 2H₂O(l) + 4e⁻ → 4OH⁻(aq). So Statement I is false. Finely divided Pt or Pd is incorporated into the "
    "porous carbon electrodes to increase the rate of the electrode reactions: Statement II is true.",
    ["Cathode: O₂ is reduced (I false)", "Anode: H₂ is oxidised", "Pt/Pd catalysts in the electrodes (II true)"],
    answer="D", ncert=f"{REF7B}, fuel cells", seconds=30)

alpha_ac = 40 / 400
ka_ac = 0.01 * alpha_ac ** 2 / (1 - alpha_ac)
assert close(alpha_ac, 0.1) and close(ka_ac, 1.11e-4, 0.002) and close(0.01 * 0.1 / 0.9, 1.11e-3, 0.002)
assert close(0.1 ** 2 / 0.9, 1.11e-2, 0.002)
add("Conductance and Kohlrausch's law", A, "numerical",
    "The molar conductivity of a 0.010 M solution of a weak monobasic acid HA is 40 S cm² mol⁻¹, and its "
    "limiting molar conductivity is 400 S cm² mol⁻¹. Its dissociation constant, K_a = cα²/(1 − α), is:",
    Opts("D", "1.11 × 10⁻⁴", ["1.0 × 10⁻⁴", "1.11 × 10⁻³", "1.11 × 10⁻²"]),
    "Degree of dissociation from molar conductivity",
    "For a weak electrolyte the degree of dissociation α = Λm/Λ°m. K_a then follows from Ostwald's expression.",
    ["α = 40 / 400 = 0.10", "K_a = cα²/(1 − α) = 0.010 × (0.10)² / 0.90 = 1.11 × 10⁻⁴"],
    why="1.0 × 10⁻⁴ drops the (1 − α) term that the stem asks for. 1.11 × 10⁻³ uses α instead of α². "
        "1.11 × 10⁻² leaves out the concentration c.",
    ncert=f"{REF7B}, applications of Kohlrausch law: dissociation constant of weak electrolytes", seconds=60,
    checked=True)

g_star = 0.14 * 150
kappa_x = g_star / 420
lam_x = kappa_x / (0.05 * 1000)
assert close(g_star, 21) and close(kappa_x, 0.05) and close(lam_x, 1.0e-3)
assert close(0.14 * 420 / 150 / 50, 7.84e-3) and close(kappa_x / 0.05, 1.0)
add("Conductance and Kohlrausch's law", A, "numerical",
    "A conductivity cell filled with KCl solution of conductivity 0.14 S m⁻¹ has a resistance of 150 Ω. The same "
    "cell filled with a 0.050 mol L⁻¹ solution of an electrolyte X has a resistance of 420 Ω. The molar "
    "conductivity of the solution of X is:",
    Opts("B", "1.0 × 10⁻³ S m² mol⁻¹",
         ["1.0 S m² mol⁻¹", "7.84 × 10⁻³ S m² mol⁻¹", "5.0 × 10⁻² S m² mol⁻¹"]),
    "Cell constant and molar conductivity",
    "The KCl solution calibrates the cell: G* = κR. The same cell constant gives the conductivity of X, and "
    "Λm = κ/c with c in mol m⁻³ for SI units.",
    ["G* = 0.14 S m⁻¹ × 150 Ω = 21 m⁻¹", "κ(X) = G*/R = 21 / 420 = 0.050 S m⁻¹",
     "c = 0.050 mol L⁻¹ = 50 mol m⁻³", "Λm = 0.050 / 50 = 1.0 × 10⁻³ S m² mol⁻¹"],
    why="1.0 S m² mol⁻¹ divides by c in mol L⁻¹ without converting to mol m⁻³. 7.84 × 10⁻³ multiplies by the "
        "resistance ratio the wrong way round. 5.0 × 10⁻² is the conductivity, not the molar conductivity.",
    ncert=f"{REF7B}, measurement of the conductivity of ionic solutions", seconds=90, checked=True)

add("Batteries and fuel cells", A, "match_list",
    lists("Match List-I (electrode reaction) with List-II (where it takes place).",
          ["Pb(s) + SO₄²⁻(aq) → PbSO₄(s) + 2e⁻",
           "PbO₂(s) + SO₄²⁻(aq) + 4H⁺(aq) + 2e⁻ → PbSO₄(s) + 2H₂O(l)",
           "Zn(s) → Zn²⁺(aq) + 2e⁻",
           "MnO₂ + NH₄⁺ + e⁻ → MnO(OH) + NH₃"],
          ["Cathode of the dry cell", "Anode of the lead storage battery during discharge",
           "Anode of the dry cell", "Cathode of the lead storage battery during discharge"]),
    match("C", M("II IV III I"), [M("IV II III I"), M("II IV I III"), M("III IV II I")]),
    "Electrode reactions of the lead storage battery and the dry cell",
    "Oxidation (loss of electrons) occurs at the anode and reduction at the cathode. During discharge of the "
    "lead storage battery, lead is oxidised to PbSO₄ and PbO₂ is reduced to PbSO₄. In the dry cell, the zinc "
    "container is oxidised and MnO₂ is reduced (Mn: +4 → +3).",
    ["Pb → PbSO₄ (oxidation) → lead battery anode → II", "PbO₂ → PbSO₄ (reduction) → lead battery cathode → IV",
     "Zn → Zn²⁺ (oxidation) → dry cell anode → III", "MnO₂ → MnO(OH) (reduction) → dry cell cathode → I"],
    why="The other codes swap anode and cathode in one of the two cells, or put the zinc oxidation in the lead "
        "battery.",
    ncert=f"{REF7B}, batteries: dry cell and lead storage battery", seconds=60)

add("Conductance and Kohlrausch's law", A, "assertion_reason",
    ar("At the same concentration and temperature, an aqueous solution of HCl conducts electricity better than "
       "an aqueous solution of NaCl.",
       "Pure hydrogen chloride is a gas at room temperature, whereas pure sodium chloride is a solid."),
    AR_, "Ionic conductivities of H⁺ and Na⁺",
    "Both HCl and NaCl are strong electrolytes, so the difference lies in the ions. The limiting molar "
    "conductivity of H⁺ (about 350 S cm² mol⁻¹) is about seven times that of Na⁺ (about 50 S cm² mol⁻¹), so "
    "the HCl solution conducts better: A is true. R is also true, but the physical state of the pure "
    "substances has nothing to do with the conductance of their aqueous solutions, so R does not explain A.",
    ["Λ°(H⁺) ≈ 350 vs Λ°(Na⁺) ≈ 50 S cm² mol⁻¹ → HCl(aq) conducts better (A true)",
     "HCl is a gas and NaCl a solid (R true) but irrelevant to conduction in solution"],
    answer="B", ncert=f"{REF7B}, Kohlrausch law: limiting molar conductivities of ions", seconds=40)

# ==================================================================== 8. Chemical Kinetics
topic("Chemical Kinetics")
REF8 = f"{C12}, 'Chemical Kinetics'"

frac3 = F(1, 2) ** 3
assert frac3 == F(1, 8) and float(frac3) * 100 == 12.5 and 100 - 12.5 == 87.5
add("Half-life", B, "numerical",
    "For a first-order reaction, the percentage of the initial reactant that remains unreacted after three "
    "half-lives is:",
    Opts("D", "12.5%", ["25%", "33.3%", "87.5%"]),
    "Successive half-lives of a first-order reaction",
    "The half-life of a first-order reaction does not depend on concentration, so the amount halves in every "
    "half-life.",
    ["After 1 t½: 50%", "After 2 t½: 25%", "After 3 t½: 12.5%"],
    why="25% is after two half-lives. 33.3% divides 100% by three. 87.5% is the percentage that has reacted.",
    ncert=f"{REF8}, half-life of a reaction", seconds=20, checked=True)

add("Rate law and order", B, "direct",
    "The instantaneous rate of the reaction R → P at time t is obtained from the plot of [R] against time as:",
    Opts("B", "The negative of the slope of the tangent to the curve at time t",
         ["The slope of the straight line joining the starting point and the point at time t",
          "The area under the curve up to time t", "The intercept of the curve on the concentration axis"]),
    "Average and instantaneous rate",
    "The instantaneous rate is −d[R]/dt, the limit of the average rate as the time interval tends to zero. "
    "Graphically it is found by drawing a tangent to the [R]–t curve at time t and taking the negative of its "
    "slope.",
    ["Rate = −d[R]/dt", "Draw a tangent at t; rate = −(slope of tangent)"],
    why="The line joining two points gives an average rate. The area under the curve and the intercept have no "
        "such meaning.",
    ncert=f"{REF8}, rate of a chemical reaction: instantaneous rate", seconds=25)

add("Arrhenius equation and activation energy", B, "statement_pair",
    sp("For two reactions with the same pre-exponential factor at the same temperature, the reaction with the "
       "higher activation energy has the smaller rate constant.",
       "The rate constant of a first-order reaction has the unit mol L⁻¹ s⁻¹."),
    SP_, "Arrhenius equation and units of k",
    "k = A e^(−Ea/RT): with A and T fixed, a larger Ea gives a smaller e^(−Ea/RT) and so a smaller k. "
    "Statement I is true. For a first-order reaction k = rate/[R] has the unit s⁻¹; mol L⁻¹ s⁻¹ is the unit for "
    "a zero-order reaction. Statement II is false.",
    ["k = A e^(−Ea/RT): larger Ea → smaller k (I true)", "First order: unit of k is s⁻¹ (II false)"],
    answer="C", ncert=f"{REF8}, temperature dependence of the rate of a reaction; units of rate constant",
    seconds=30)

frac_e = 10 ** (-28.7 / 5.74)
assert close(frac_e, 1e-5) and close(math.exp(-28.7 / 5.74), 6.7e-3, 0.01)
add("Arrhenius equation and activation energy", I, "numerical",
    "A reaction has an activation energy of 28.7 kJ mol⁻¹. At 300 K, the fraction of molecules having energy "
    "equal to or greater than the activation energy, e^(−Ea/RT), is (2.303RT = 5.74 kJ mol⁻¹ at 300 K):",
    Opts("A", "1 × 10⁻⁵", ["6.7 × 10⁻³", "1 × 10⁵", "2 × 10⁻¹"]),
    "Fraction of effective molecules in the Arrhenius equation",
    "In k = A e^(−Ea/RT), the factor e^(−Ea/RT) is the fraction of molecules with energy at least Ea. Taking "
    "logarithms to base 10: log f = −Ea/(2.303RT).",
    ["log f = −28.7 / 5.74 = −5", "f = 10⁻⁵"],
    why="6.7 × 10⁻³ is e⁻⁵: it uses 2.303RT in place of RT inside the natural exponential. 1 × 10⁵ drops the "
        "minus sign (a fraction cannot exceed 1). 2 × 10⁻¹ is simply 5.74/28.7.",
    ncert=f"{REF8}, temperature dependence of the rate of a reaction", seconds=45, checked=True)

assert 2 ** ((330 - 300) // 10) == 8
add("Arrhenius equation and activation energy", I, "numerical",
    "The rate constant of a reaction nearly doubles for every 10 K rise in temperature. If this holds, by what "
    "factor does the rate constant increase when the temperature is raised from 300 K to 330 K?",
    Opts("C", "8", ["6", "3", "9"]),
    "Effect of temperature on rate constant",
    "Each 10 K rise multiplies k by about 2. A 30 K rise contains three such steps, so the factors multiply.",
    ["Number of 10 K steps = 30 / 10 = 3", "Factor = 2 × 2 × 2 = 2³ = 8"],
    why="6 adds the factors (2 + 2 + 2) instead of multiplying them. 3 counts the steps. 9 is 3².",
    ncert=f"{REF8}, temperature dependence of the rate of a reaction", seconds=25, checked=True)

add("Zero and first order reactions", I, "assertion_reason",
    ar("The thermal decomposition of HI on a gold surface is a zero-order reaction.",
       "Gold is a noble metal that does not corrode in air."),
    AR_, "Zero-order surface reactions",
    "NCERT gives the decomposition of HI on a gold surface as an example of a zero-order reaction, so A is true. "
    "Gold is indeed unreactive towards air, so R is true. But R does not explain A: the zero order arises "
    "because the gold surface is saturated with HI molecules, so the rate does not depend on the gas "
    "concentration.",
    ["A: zero-order surface reaction (true)", "R: gold does not corrode (true)",
     "Reason for zero order: saturated catalyst surface, not resistance to corrosion"],
    answer="B", ncert=f"{REF8}, zero order reactions", seconds=35)

add("Zero and first order reactions", I, "match_list",
    lists("Match List-I (expression) with List-II (what it represents).",
          ["k = (2.303/t) log([R]₀/[R])", "[R] = [R]₀ − kt", "t½ = 0.693/k", "t½ = [R]₀/2k"],
          ["Integrated rate equation of a zero-order reaction", "Half-life of a first-order reaction",
           "Integrated rate equation of a first-order reaction", "Half-life of a zero-order reaction"]),
    match("D", M("III I II IV"), [M("I III II IV"), M("III I IV II"), M("II I III IV")]),
    "Integrated rate equations and half-lives",
    "For zero order, [R] falls linearly with time and t½ = [R]₀/2k. For first order, "
    "k = (2.303/t) log([R]₀/[R]) and t½ = 0.693/k.",
    ["(2.303/t) log([R]₀/[R]) → first-order integrated equation → III", "[R]₀ − kt → zero order → I",
     "0.693/k → first-order half-life → II", "[R]₀/2k → zero-order half-life → IV"],
    why="The other codes interchange the zero- and first-order equations or their half-lives.",
    ncert=f"{REF8}, integrated rate equations", seconds=35)

ratio_ab = F(1, 2) ** (40 // 10) / F(1, 2) ** (40 // 20)
assert ratio_ab == F(1, 4)
add("Half-life", A, "numerical",
    "Two first-order reactions, A → products (t½ = 10 min) and B → products (t½ = 20 min), are started at the "
    "same time with equal initial concentrations of A and B. After 40 min, the ratio [A] : [B] is:",
    Opts("B", "1 : 4", ["1 : 2", "4 : 1", "1 : 16"]),
    "Comparing first-order decays",
    "In 40 min A goes through 40/10 = 4 half-lives and B through 40/20 = 2 half-lives.",
    ["[A] = [A]₀ × (½)⁴ = [A]₀/16", "[B] = [B]₀ × (½)² = [B]₀/4", "[A] : [B] = 1/16 : 1/4 = 1 : 4"],
    why="1 : 2 is just the ratio of the half-lives. 4 : 1 inverts the ratio. 1 : 16 is the fraction of A left, "
        "not the ratio of A to B.",
    ncert=f"{REF8}, half-life of a reaction", seconds=50, checked=True)

add("Arrhenius equation and activation energy", A, "multi_statement",
    ms("Which of the following statements about a catalyst are correct?",
       ["A catalyst is consumed permanently in the reaction it catalyses.",
        "A catalyst does not change the equilibrium constant of a reversible reaction.",
        "A catalyst increases the rate of the forward reaction only.",
        "A catalyst lowers the activation energy of the forward and the backward reactions by the same amount.",
        "A small amount of a catalyst can catalyse a large amount of reactants."]),
    multi("A", {"a": False, "b": True, "c": False, "d": True, "e": True},
          ["(a), (b) and (d) only", "(b), (c) and (e) only", "(b), (c), (d) and (e) only"]),
    "Action of a catalyst",
    "A catalyst provides an alternative pathway of lower activation energy and is regenerated at the end of the "
    "reaction. The energy barrier falls equally for both directions, so both rates rise by the same factor and "
    "the position of equilibrium (K) is unchanged. A small amount of catalyst is enough for a large amount of "
    "reactants.",
    ["(a) False: the catalyst is regenerated", "(b) True", "(c) False: both directions are speeded up",
     "(d) True", "(e) True"],
    why="Options containing (a) or (c) are wrong.",
    ncert=f"{REF8}, effect of catalyst", seconds=50)

add("Zero and first order reactions", A, "direct",
    "For a first-order reaction, a plot of log[R] (common logarithm) against time t is a straight line whose "
    "slope is:",
    Opts("C", "−k/2.303", ["−k", "−2.303k", "+k/2.303"]),
    "Graphical form of the first-order rate equation",
    "The integrated first-order equation ln[R] = ln[R]₀ − kt becomes, in common logarithms, "
    "log[R] = log[R]₀ − kt/2.303.",
    ["ln[R] = ln[R]₀ − kt", "Divide by 2.303: log[R] = log[R]₀ − (k/2.303) t", "Slope = −k/2.303"],
    why="−k is the slope of the ln[R] plot, not the log[R] plot. −2.303k multiplies instead of dividing. The "
        "slope is negative because [R] falls with time.",
    ncert=f"{REF8}, first order reactions", seconds=30)

# ==================================================================== 9. Classification of Elements and Periodicity
topic("Classification of Elements and Periodicity in Properties")
REF9 = f"{C11}, 'Classification of Elements and Periodicity in Properties'"

assert 198 / 2 == 99
add("Atomic and ionic radii", B, "direct",
    "The Cl–Cl bond distance in the chlorine molecule is 198 pm. The covalent (atomic) radius of chlorine is:",
    Opts("A", "99 pm", ["198 pm", "396 pm", "49.5 pm"]),
    "Covalent radius",
    "For a non-metal forming a homonuclear diatomic molecule, the covalent radius is half the distance between "
    "the nuclei of the two bonded atoms.",
    ["Covalent radius = ½ × internuclear distance = 198 / 2 = 99 pm"],
    why="198 pm is the whole bond length. 396 pm doubles it, and 49.5 pm halves the radius again.",
    ncert=f"{REF9}, atomic radius", seconds=20, checked=True)

add("Modern periodic table", B, "direct",
    "An element has the ground-state electronic configuration [Ne] 3s² 3p³. Its position in the periodic table is:",
    Opts("D", "Period 3, group 15", ["Period 3, group 13", "Period 2, group 15", "Period 3, group 5"]),
    "Locating an element from its configuration",
    "The period is the principal quantum number of the valence shell. For a p-block element, the group number "
    "is 10 + (number of s and p valence electrons).",
    ["Valence shell n = 3 → period 3", "Valence electrons 3s² 3p³ = 5 → p-block group 10 + 5 = 15 (phosphorus)"],
    why="Group 13 counts only the s electrons plus one p electron. Period 2 ignores the [Ne] core. Group 5 is a "
        "d-block group; the old 'VA' label is now group 15.",
    ncert=f"{REF9}, electronic configurations and types of elements: p-block", seconds=25)

add("Modern periodic table", B, "statement_pair",
    sp("The s-block and p-block elements together are called the representative or main group elements.",
       "The f-block elements are called the inner-transition elements."),
    SP_, "Types of elements in the periodic table",
    "Both statements are the standard classification: s- and p-block elements are the representative (main "
    "group) elements, d-block elements are the transition elements, and the lanthanoids and actinoids "
    "(f-block) are the inner-transition elements.",
    ["s + p blocks → representative elements (I true)", "f block → inner-transition elements (II true)"],
    answer="A", ncert=f"{REF9}, electronic configurations and types of elements", seconds=20)

add("Valence and reactivity", I, "direct",
    "Which of the following pairs of elements shows a diagonal relationship?",
    Opts("B", "Beryllium and aluminium", ["Beryllium and magnesium", "Lithium and sodium", "Boron and aluminium"]),
    "Diagonal relationship",
    "The first member of groups 1 and 2 (Li, Be) resembles the second member of the next group (Mg, Al) more "
    "than its own group. This similarity between diagonally placed elements is called a diagonal relationship.",
    ["Li (group 1, period 2) ↔ Mg (group 2, period 3)", "Be (group 2, period 2) ↔ Al (group 13, period 3)"],
    why="Be–Mg, Li–Na and B–Al are pairs in the same group, not diagonal pairs.",
    ncert=f"{REF9}, anomalous properties of second period elements", seconds=25)

add("Ionisation and electron gain enthalpy", I, "assertion_reason",
    ar("Among the elements of the second period, neon has the lowest first ionisation enthalpy.",
       "Neon has a completely filled valence shell, 2s² 2p⁶."),
    AR_, "Ionisation enthalpy of noble gases",
    "A completely filled valence shell is very stable, and neon also has the highest effective nuclear charge "
    "in the period. Its first ionisation enthalpy is therefore the highest, not the lowest, in period 2 "
    "(lithium has the lowest). A is false; R is true.",
    ["Ne: 2s² 2p⁶, closed shell (R true)", "Closed shell + high Z_eff → highest ΔiH₁ in period 2 (A false)",
     "Lowest in period 2: Li"],
    answer="D", ncert=f"{REF9}, ionisation enthalpy", seconds=30)

add("Modern periodic table", I, "match_list",
    lists("Match List-I (general outer electronic configuration) with List-II (group).",
          ["[noble gas] ns² np⁶", "[noble gas] (n−1)d¹⁰ ns²", "[noble gas] ns¹", "[noble gas] (n−1)d⁵ ns¹"],
          ["Group 6", "Group 1", "Group 18", "Group 12"]),
    match("C", M("III IV II I"), [M("III IV I II"), M("IV III II I"), M("III II IV I")]),
    "Group from the outer electronic configuration",
    "For s-block elements the group equals the number of s electrons; for p-block, 10 + (s + p electrons); for "
    "d-block, the number of (n−1)d + ns electrons.",
    ["ns² np⁶: 10 + 8 = 18 → III", "(n−1)d¹⁰ ns²: 10 + 2 = 12 → IV", "ns¹: group 1 → II",
     "(n−1)d⁵ ns¹: 5 + 1 = 6 → I"],
    why="The other codes swap group 1 with group 6, or group 18 with group 12.",
    ncert=f"{REF9}, electronic configurations and types of elements", seconds=40)

add("Valence and reactivity", I, "multi_statement",
    ms("Which of the following general formulae (M = metal, E = element of the group) are correct?",
       ["Oxide of a group 2 element: MO",
        "Simple hydride of a group 14 element: EH₄",
        "Simple hydride of a group 16 element: EH₃",
        "Simple hydride of a group 15 element: EH₂",
        "Oxide of a group 13 element in its group oxidation state: E₂O₃"]),
    multi("D", {"a": True, "b": True, "c": False, "d": False, "e": True},
          ["(a), (b) and (c) only", "(b), (d) and (e) only", "(a), (c), (d) and (e) only"]),
    "Periodicity of valence",
    "The usual valence of a representative element equals the number of valence electrons (groups 1, 2, 13, "
    "14) or 8 minus that number (groups 15–17). Group 2: valence 2 → MO. Group 14: valence 4 → EH₄ (CH₄). Group "
    "16: valence 2 → H₂E (H₂O). Group 15: valence 3 → EH₃ (NH₃). Group 13: valence 3 → E₂O₃ (Al₂O₃).",
    ["(a) True", "(b) True", "(c) False: H₂E", "(d) False: EH₃", "(e) True"],
    why="Options containing (c) or (d) are wrong.",
    ncert=f"{REF9}, periodic trends in valence", seconds=45)

assert 118 - 114 == 4 and 18 - 4 == 14 and 86 < 114 <= 118
add("Modern periodic table", A, "direct",
    "The element with atomic number 114 is placed in the periodic table in:",
    Opts("A", "Period 7, group 14 (p-block)",
         ["Period 7, group 16 (p-block)", "Period 6, group 14 (p-block)", "Period 7, group 4 (d-block)"]),
    "Predicting the position of a heavy element",
    "The seventh period begins at Z = 87 and ends at Z = 118 (group 18). Element 114 is four places before 118, "
    "so it is in group 18 − 4 = 14, in the p-block of period 7, below lead.",
    ["Period 7: Z = 87 to 118", "118 − 114 = 4 → group 14", "Configuration ends ...7s² 7p² → p-block"],
    why="Group 16 would be Z = 116. Period 6 ends at Z = 86. Group 4 of period 7 is Z = 104.",
    ncert=f"{REF9}, nomenclature of elements with atomic numbers > 100; long form of periodic table", seconds=45,
    checked=True)

add("Atomic and ionic radii", A, "assertion_reason",
    ar("The listed atomic radii of the noble gases are larger than those of the halogens of the same periods.",
       "For the noble gases van der Waals (non-bonded) radii are quoted, whereas for the halogens covalent radii "
       "are quoted, and van der Waals radii are larger."),
    AR_, "Atomic radii of noble gases",
    "Noble gases are monatomic and do not form ordinary covalent bonds, so only their van der Waals radii can be "
    "measured. A van der Waals radius (half the distance between non-bonded neighbours) is much larger than a "
    "covalent radius. This is why the noble gases appear to break the trend of decreasing radius across a "
    "period. R explains A.",
    ["Noble gases: van der Waals radii", "Halogens: covalent radii (smaller by definition)",
     "Apparent increase at group 18 is due to the different definition"],
    answer="A", ncert=f"{REF9}, atomic radius (noble gases)", seconds=40)

add("Valence and reactivity", A, "statement_pair",
    sp("Chemical reactivity tends to be high for the elements at the two extremes of a period and lower for the "
       "elements in the middle.",
       "The high reactivity of the group 1 metals is due to their high ionisation enthalpies."),
    SP_, "Periodic trends in chemical reactivity",
    "On the left of a period the metals lose electrons readily, and on the right the non-metals gain electrons "
    "readily, so reactivity is highest at the two ends: Statement I is true. Alkali metals are reactive because "
    "their ionisation enthalpies are low, which makes electron loss easy; Statement II is false.",
    ["Left end: easy electron loss (low ΔiH); right end: easy electron gain (very negative ΔegH) (I true)",
     "Group 1 reactivity comes from low, not high, ionisation enthalpy (II false)"],
    answer="C", ncert=f"{REF9}, periodic trends in chemical properties: reactivity", seconds=35)

# ==================================================================== 10. p-Block Elements
topic("p-Block Elements")
REF10A = "Class 11 Chemistry (pre-2023 edition), 'The p-Block Elements'"
REF10B = f"{C12}, 'The p-Block Elements'"

bp15 = {"NH3": 238.5, "PH3": 185.5, "AsH3": 210.6, "SbH3": 254.6}
assert min(bp15, key=bp15.get) == "PH3"
add("Group 15 and 16 trends", B, "direct",
    "Among the hydrides NH₃, PH₃, AsH₃ and SbH₃, the one with the lowest boiling point is:",
    Opts("B", "PH₃", ["NH₃", "AsH₃", "SbH₃"]),
    "Boiling points of group 15 hydrides",
    "From PH₃ to SbH₃ the boiling point rises with molecular size because van der Waals forces increase. NH₃ "
    "has an abnormally high boiling point because its molecules are hydrogen bonded. So PH₃ has the lowest "
    "boiling point (about 185 K, against about 238 K for NH₃).",
    ["PH₃ < AsH₃ < SbH₃: larger molecules, stronger van der Waals forces",
     "NH₃ is raised above PH₃ by hydrogen bonding", "Lowest: PH₃"],
    why="NH₃ is hydrogen bonded, and AsH₃ and SbH₃ are larger molecules with stronger dispersion forces, so all "
        "three boil above PH₃.",
    ncert=f"{REF10B}, group 15 elements: properties of hydrides", seconds=30, checked=True)

add("Group 15 and 16 trends", B, "match_list",
    lists("Match List-I (group 16 element) with List-II (its nature).",
          ["Oxygen", "Sulphur", "Tellurium", "Polonium"],
          ["Metal", "Metalloid", "Non-metal, solid at room temperature", "Non-metal, gas at room temperature"]),
    match("A", M("IV III II I"), [M("III IV II I"), M("IV II III I"), M("IV III I II")]),
    "Metallic character down group 16",
    "Metallic character increases down group 16: oxygen and sulphur are non-metals (oxygen a gas, sulphur a "
    "solid), selenium and tellurium are metalloids and polonium is a metal.",
    ["O → IV", "S → III", "Te → II", "Po → I"],
    why="The other codes interchange oxygen and sulphur, or tellurium and polonium, or sulphur and tellurium.",
    ncert=f"{REF10B}, group 16 elements: physical properties", seconds=30)

add("Group 17 and 18 trends", B, "statement_pair",
    sp("Helium has the lowest boiling point of any known substance.",
       "The first ionisation enthalpy of the noble gases increases down the group."),
    SP_, "Physical properties of the noble gases",
    "Helium boils at about 4.2 K, the lowest boiling point of any substance, because only very weak dispersion "
    "forces act between its tiny atoms: Statement I is true. Down group 18 the atomic size increases, so the "
    "ionisation enthalpy decreases: Statement II is false.",
    ["He: b.p. ≈ 4.2 K, the lowest known (I true)", "Size increases down the group → ΔiH decreases (II false)"],
    answer="C", ncert=f"{REF10B}, group 18 elements: physical properties and ionisation enthalpy", seconds=25)

add("Anomalous first element", B, "direct",
    "The first member of each group of the p-block differs from the other members of its group. Which of the "
    "following is NOT a reason for this anomalous behaviour?",
    Opts("D", "Availability of d orbitals in its valence shell",
         ["Its small atomic size", "Its high electronegativity", "Its high ionisation enthalpy"]),
    "Reasons for the anomalous behaviour of the first member",
    "The first member of each p-block group is anomalous because of its small size, high electronegativity, "
    "high ionisation enthalpy and the ABSENCE of d orbitals in its valence shell (n = 2 has only s and p "
    "orbitals).",
    ["Second-period valence shell: 2s and 2p only → no d orbitals",
     "Small size, high electronegativity and high ionisation enthalpy are genuine reasons"],
    why="Small size, high electronegativity and high ionisation enthalpy are all listed causes of the anomaly; "
        "it is the lack, not the presence, of d orbitals that matters.",
    ncert=f"{REF10B}, anomalous behaviour of the first member of p-block groups", seconds=25)

en13 = {"B": 2.0, "Al": 1.5, "Ga": 1.6, "In": 1.7, "Tl": 1.8}
assert max(en13, key=en13.get) == "B"
add("Group 13 and 14 trends", I, "direct",
    "Which element of group 13 has the highest electronegativity (Pauling scale)?",
    Opts("C", "Boron", ["Aluminium", "Gallium", "Thallium"]),
    "Electronegativity in group 13",
    "Boron, the small first member, has the highest electronegativity in the group (about 2.0). Down the group "
    "electronegativity first falls from B to Al (1.5) and then rises slightly (Ga 1.6, In 1.7, Tl 1.8) because "
    "of differences in atomic size, but none of the heavier members reaches boron's value.",
    ["B 2.0 > Tl 1.8 > In 1.7 > Ga 1.6 > Al 1.5"],
    why="The slight rise from Al to Tl misleads some students into choosing Tl or Ga; aluminium has the lowest "
        "value in the group.",
    ncert=f"{REF10A}, group 13 elements: electronegativity", seconds=30, checked=True)

add("Anomalous first element", I, "assertion_reason",
    ar("The heavier elements of groups 15 and 16 can form dπ–pπ bonds, but nitrogen and oxygen cannot.",
       "Nitrogen and oxygen have no d orbitals in their valence shells."),
    AR_, "dπ–pπ bonding and the first element",
    "Phosphorus and the heavier elements have vacant d orbitals in their valence shells, which they can use to "
    "form dπ–pπ bonds (for example with oxygen). Nitrogen and oxygen, in the second period, have only 2s and 2p "
    "orbitals, so they cannot form such bonds; they form pπ–pπ multiple bonds instead. R explains A.",
    ["Heavier elements: vacant d orbitals → dπ–pπ bonding possible",
     "N, O: no valence d orbitals (R) → no dπ–pπ bonding (A)"],
    answer="A", ncert=f"{REF10B}, group 15: anomalous properties of nitrogen", seconds=35)

add("Group 15 and 16 trends", I, "statement_pair",
    sp("Down group 15, the covalent radius increases considerably from nitrogen to phosphorus but only slightly "
       "from arsenic to bismuth.",
       "The small increase from arsenic to bismuth is due to the presence of completely filled d and/or f "
       "orbitals in the heavier members, which shield the nucleus poorly."),
    SP_, "Atomic size trend in group 15",
    "Both statements describe the NCERT trend. A new shell causes a large jump from N to P. In As, Sb and Bi "
    "the extra nuclear charge is poorly shielded by filled d (and in Bi also f) orbitals, so the radius "
    "increases only slightly.",
    ["N → P: large increase (I true)", "As → Bi: small increase due to poor shielding by d/f electrons (II true)"],
    answer="A", ncert=f"{REF10B}, group 15 elements: atomic and ionic radii", seconds=35)

add("Group 13 and 14 trends", I, "match_list",
    lists("Match List-I (group) with List-II (trend in oxidation state down the group, due to the inert pair "
          "effect).",
          ["Group 13", "Group 14", "Group 15", "Group 16"],
          ["+3 becomes more stable than +5", "+1 becomes more stable than +3",
           "+4 becomes more stable than +6", "+2 becomes more stable than +4"]),
    match("B", M("II IV I III"), [M("IV II I III"), M("II IV III I"), M("I IV II III")]),
    "Inert pair effect",
    "Down groups 13 to 16 the ns² electrons become increasingly reluctant to take part in bonding, so an "
    "oxidation state two less than the group oxidation state becomes more stable for the heavier members.",
    ["Group 13 (ns² np¹): +1 more stable than +3 down the group (e.g. Tl) → II",
     "Group 14 (ns² np²): +2 more stable than +4 (e.g. Pb) → IV",
     "Group 15 (ns² np³): +3 more stable than +5 (e.g. Bi) → I",
     "Group 16 (ns² np⁴): +4 more stable than +6 → III"],
    why="Each group's lower stable state is the group oxidation state minus two; the other codes break this "
        "pattern.",
    ncert=f"{REF10B}, oxidation states of groups 15 and 16; {REF10A}, groups 13 and 14", seconds=40)

add("Group 17 and 18 trends", I, "multi_statement",
    ms("Which of the following statements about the group 17 elements are correct?",
       ["They have the smallest atomic radii in their respective periods.",
        "The bond dissociation enthalpy of I₂ is higher than that of Br₂.",
        "They have very high ionisation enthalpies, so they have little tendency to lose electrons.",
        "Their melting and boiling points increase steadily from fluorine to iodine.",
        "Iodine is more electronegative than chlorine."]),
    multi("A", {"a": True, "b": False, "c": True, "d": True, "e": False},
          ["(a), (b) and (c) only", "(c), (d) and (e) only", "(a), (b), (c) and (d) only"]),
    "General trends in group 17",
    "Halogens have the highest effective nuclear charge in their periods, hence the smallest radii and very high "
    "ionisation enthalpies. Their melting and boiling points rise with molecular size from F₂ to I₂. The bond "
    "dissociation enthalpy decreases from Cl₂ to I₂ (Cl₂ > Br₂ > I₂) as the atoms get larger, and "
    "electronegativity decreases down the group.",
    ["(a) True", "(b) False: Br₂ > I₂", "(c) True", "(d) True", "(e) False: Cl > I"],
    why="Options containing (b) or (e) are wrong.",
    ncert=f"{REF10B}, group 17 elements: atomic and physical properties", seconds=50)

add("Group 13 and 14 trends", A, "direct",
    "Which of the following correctly describes the tendency of the group 14 elements to show catenation?",
    Opts("D", "C ≫ Si > Ge ≈ Sn; lead does not show catenation",
         ["Si > C > Ge ≈ Sn > Pb", "All five elements catenate strongly, in the order C > Si > Ge > Sn > Pb",
          "Sn > Ge > Si > C; lead catenates the most"]),
    "Catenation in group 14",
    "Catenation depends on the strength of the E–E bond. The C–C bond is strong, so carbon catenates far more "
    "than any other element. E–E bond strength falls down the group, giving C ≫ Si > Ge ≈ Sn, and lead does not "
    "show catenation.",
    ["C–C strongest → C ≫ others", "Si > Ge ≈ Sn", "Pb: no catenation"],
    why="Silicon catenates much less than carbon. Lead does not catenate, so orders that include strong "
        "catenation by Pb, or that reverse the trend, are wrong.",
    ncert=f"{REF10A}, group 14 elements: anomalous behaviour of carbon (catenation)", seconds=35)

add("Group 15 and 16 trends", A, "assertion_reason",
    ar("The tendency of the group 15 elements to show the −3 oxidation state decreases down the group.",
       "The electronegativity of the elements increases down group 15."),
    AR_, "−3 oxidation state in group 15",
    "Down group 15 the atoms get larger and more metallic, so the tendency to gain three electrons (−3 state) "
    "decreases; bismuth hardly forms any compound in the −3 state. A is true. Electronegativity decreases, not "
    "increases, down the group, so R is false.",
    ["Size and metallic character increase down the group → −3 tendency decreases (A true)",
     "Electronegativity: N > P > As > Sb > Bi (R false)"],
    answer="C", ncert=f"{REF10B}, group 15 elements: oxidation states", seconds=35)

add("Group 17 and 18 trends", A, "statement_pair",
    sp("The colour of the halogens becomes lighter from F₂ to I₂.",
       "The halogens are coloured because their molecules absorb radiation in the visible region, which excites "
       "their outer electrons to higher energy levels."),
    SP_, "Colour of the halogens",
    "The halogens are coloured because absorption of visible light excites their outer electrons; the colour "
    "seen is the complementary colour. As the molecules get larger, less energy is needed for the excitation, "
    "so the colour deepens from pale yellow F₂ to violet I₂. Statement I is false; Statement II is true.",
    ["Absorption of visible light → electronic excitation → colour (II true)",
     "Smaller excitation energy down the group → colour deepens, not lightens (I false)"],
    answer="D", ncert=f"{REF10B}, group 17 elements: physical properties", seconds=35)

add("Group 15 and 16 trends", A, "multi_statement",
    ms("Which of the following statements about the group 16 elements are correct?",
       ["The first ionisation enthalpy increases down the group.",
        "The melting and boiling points increase down the group up to tellurium.",
        "The large difference between the melting and boiling points of oxygen and sulphur arises because oxygen "
        "exists as diatomic O₂ molecules whereas sulphur exists as polyatomic S₈ molecules.",
        "The atomic radius decreases from oxygen to tellurium.",
        "The electronegativity decreases from oxygen to polonium."]),
    multi("B", {"a": False, "b": True, "c": True, "d": False, "e": True},
          ["(a), (b) and (c) only", "(b), (d) and (e) only", "(b), (c), (d) and (e) only"]),
    "Physical trends in group 16",
    "Down the group the size increases, so ionisation enthalpy and electronegativity decrease. Melting and "
    "boiling points rise from O to Te with increasing size and atomicity; oxygen (O₂) has much weaker van der "
    "Waals forces than sulphur (S₈).",
    ["(a) False: ΔiH decreases", "(b) True", "(c) True: atomicity O₂ vs S₈", "(d) False: radius increases",
     "(e) True"],
    why="Options containing (a) or (d) are wrong.",
    ncert=f"{REF10B}, group 16 elements: atomic and physical properties", seconds=55)


# ==================================================================== checks and output
def check_plan():
    plan = json.loads(PLAN.read_text(encoding="utf-8"))
    subj = next(s for s in plan["subjects"] if s["subject"] == CHE)
    pkg = next(p for p in subj["packages"] if p["package"] == PACKAGE)
    tax = {t["topic"]: t for t in subj["topics"] if t["topic"] in pkg["topics"]}
    want = Counter({(t, d): n for t, v in tax.items() for d, n in v["quota"].items() if n})
    have = Counter((q["topic"], q["difficulty"]) for q in QUESTIONS)
    assert have == want, (have - want, want - have)
    lo, hi = (int(x.rsplit("_", 1)[1]) for x in pkg["question_ids"])
    assert [q["question_id"] for q in QUESTIONS] == [f"NEET_CHE_{n:06d}" for n in range(lo, hi + 1)]
    for q in QUESTIONS:
        assert q["subtopic"] in tax[q["topic"]]["subtopics"], (q["question_id"], q["subtopic"])
    assert OUT.as_posix().endswith(pkg["output"])


if __name__ == "__main__":
    check_plan()
    n = len(QUESTIONS)
    fmts = Counter(q["format"] for q in QUESTIONS)
    assert 0.27 * n <= fmts["numerical"] <= 0.34 * n, fmts
    assert all(fmts[f] >= 0.08 * n for f in
               ("direct", "assertion_reason", "statement_pair", "match_list", "multi_statement")), fmts
    assert all(0.22 * n <= KEYS[k] <= 0.28 * n for k in LETTERS), KEYS
    texts = [q["question_text"] for q in QUESTIONS]
    assert len(set(texts)) == n
    doc = {"schema_version": "1.0", "batch_id": "BATCH_004", "created_at": TODAY,
           "notes": "Package CHE_004_p1: 126 original Chemistry questions (physical chemistry, periodicity and "
                    "p-block). Numerical answers re-derived in tools/batch_004/CHE_004_p1.py.",
           "stimuli": [], "questions": QUESTIONS}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {OUT}: {n} questions; difficulty {dict(Counter(q['difficulty'] for q in QUESTIONS))}; "
          f"formats {dict(fmts)}; keys {dict(sorted(KEYS.items()))}")
