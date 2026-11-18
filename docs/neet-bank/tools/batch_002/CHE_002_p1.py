"""Writes batches/parts/BATCH_002_CHE_p1.json: package CHE_002_p1 of BATCH_002 (Chemistry, 128 questions).

Topics: Some Basic Concepts, Atomic Structure, Chemical Bonding, Thermodynamics, Solutions, Equilibrium,
Redox and Electrochemistry, Chemical Kinetics, Periodicity, p-Block Elements. IDs NEET_CHE_000251..000378.

Every computable answer is re-derived here with an assert before anything is written; the quota per
(topic, difficulty), the ID range, the format mix and the answer-key balance are asserted too.
The position of every correct option is chosen by hand in the call that adds the question (argument `at`)
and never moved by code.

    cd docs/neet-bank && python tools/batch_002/CHE_002_p1.py
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
PACKAGE = "CHE_002_p1"
PLAN = ROOT / "batches" / "plans" / "BATCH_002_plan.json"
OUT = ROOT / "batches" / "parts" / "BATCH_002_CHE_p1.json"
TODAY = "2026-11-16"
LETTERS = "ABCD"
CHE = "Chemistry"
FIRST_ID = 251
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
M_E = 9.11e-31

# ==================================================================== 1. Some Basic Concepts in Chemistry
topic("Some Basic Concepts in Chemistry")
REF1 = f"{C11}, 'Some Basic Concepts of Chemistry'"

n_naoh = 4.0 / 40
assert close(n_naoh / 0.250, 0.4) and close(n_naoh, 0.1) and close(4.0 / 250, 0.016) and close(n_naoh / 2.5, 0.04)
add("Mole concept", B, "numerical",
    "4.0 g of sodium hydroxide is dissolved in water and the solution is made up to 250 mL. The molarity of the "
    "solution is (Na = 23, O = 16, H = 1):",
    Opts("A", "0.4 M", ["0.1 M", "0.016 M", "0.04 M"]),
    "Molarity = moles of solute per litre of solution",
    "Convert the mass of NaOH to moles, and the volume of the solution to litres, then divide.",
    ["Molar mass of NaOH = 23 + 16 + 1 = 40 g mol⁻¹", "Moles of NaOH = 4.0 / 40 = 0.1 mol",
     "Volume = 250 mL = 0.250 L", "Molarity = 0.1 / 0.250 = 0.4 M"],
    why="0.1 M is the number of moles, not divided by the volume. 0.016 M divides grams by millilitres. "
        "0.04 M comes from writing 250 mL as 2.5 L.",
    ncert=f"{REF1}, reactions in solutions: molarity", seconds=35, checked=True)

add("Laws of chemical combination", B, "direct",
    "Which of the following pairs of compounds illustrates the law of multiple proportions?",
    Opts("B", "H₂O and H₂O₂", ["NaCl and KCl", "H₂O and H₂S",
                               "CO₂ made by burning carbon and CO₂ made by heating limestone"]),
    "Law of multiple proportions",
    "The law applies when the same two elements form more than one compound. The masses of one element that "
    "combine with a fixed mass of the other are then in a simple whole-number ratio. In H₂O and H₂O₂, 2 g of "
    "hydrogen combines with 16 g and 32 g of oxygen, a ratio of 1 : 2.",
    ["H₂O: 2 g H with 16 g O; H₂O₂: 2 g H with 32 g O", "Oxygen masses for a fixed mass of H: 16 : 32 = 1 : 2",
     "Same two elements, simple ratio → law of multiple proportions"],
    why="NaCl and KCl, and H₂O and H₂S, are not made of the same two elements. Two samples of CO₂ from "
        "different sources show the law of definite proportions, not multiple proportions.",
    ncert=f"{REF1}, laws of chemical combinations: law of multiple proportions", seconds=30)

add("Mole concept", B, "match_list",
    lists("Match List-I (physical quantity) with List-II (its SI base unit).",
          ["Mass", "Amount of substance", "Thermodynamic temperature", "Electric current"],
          ["Kelvin", "Mole", "Ampere", "Kilogram"]),
    match("C", M("IV II I III"), [M("IV I II III"), M("II IV I III"), M("IV II III I")]),
    "SI base units",
    "The SI has seven base units. Mass is measured in kilogram (kg), amount of substance in mole (mol), "
    "thermodynamic temperature in kelvin (K) and electric current in ampere (A).",
    ["Mass → kilogram → IV", "Amount of substance → mole → II", "Thermodynamic temperature → kelvin → I",
     "Electric current → ampere → III"],
    why="The other codes swap the mole with the kelvin or the kilogram, or the kelvin with the ampere.",
    ncert=f"{REF1}, the international system of units (SI)", seconds=30)

o1, o2 = F(3636, 6364), F(5333, 4667)
assert abs(o2 / o1 - 2) < 0.002
add("Laws of chemical combination", I, "numerical",
    "Two oxides of nitrogen contain 63.64% and 46.67% nitrogen by mass. The masses of oxygen that combine with a "
    "fixed mass of nitrogen in the first and the second oxide are in the ratio:",
    Opts("D", "1 : 2", ["2 : 1", "2 : 3", "1 : 1"]),
    "Law of multiple proportions applied to percentage composition",
    "Find the mass of oxygen per gram of nitrogen in each oxide and compare the two numbers.",
    ["Oxide 1: O = 100 − 63.64 = 36.36 g per 63.64 g N → 0.571 g O per g N",
     "Oxide 2: O = 100 − 46.67 = 53.33 g per 46.67 g N → 1.143 g O per g N",
     "Ratio = 0.571 : 1.143 = 1 : 2 (the oxides are N₂O and NO)"],
    why="2 : 1 inverts the ratio. 2 : 3 compares the oxygen percentages directly without fixing the mass of "
        "nitrogen. 1 : 1 assumes the oxygen content is the same.",
    ncert=f"{REF1}, law of multiple proportions", seconds=70, checked=True)

n_h2o = 1.8 / 18
assert close(n_h2o * 10 * NA, 6.022e23) and close(n_h2o * NA, 6.022e22)
assert close(n_h2o * 3 * NA, 1.807e23) and close(n_h2o * 8 * NA, 4.818e23)
add("Mole concept", I, "numerical",
    "The number of electrons present in 1.8 mL of liquid water (density 1.0 g mL⁻¹) is (H = 1, O = 16, "
    "Nₐ = 6.022 × 10²³ mol⁻¹):",
    Opts("A", "6.022 × 10²³", ["6.022 × 10²²", "1.807 × 10²³", "4.818 × 10²³"]),
    "Mole concept: counting sub-atomic particles",
    "Mass = 1.8 g, so the sample is 0.1 mol of water. Each H₂O molecule has 2 × 1 + 8 = 10 electrons.",
    ["Mass of water = 1.8 mL × 1.0 g mL⁻¹ = 1.8 g", "Moles = 1.8 / 18 = 0.1 mol",
     "Molecules = 0.1 × 6.022 × 10²³ = 6.022 × 10²²",
     "Electrons = 10 × 6.022 × 10²² = 6.022 × 10²³"],
    why="6.022 × 10²² is the number of molecules. 1.807 × 10²³ is the number of atoms. 4.818 × 10²³ counts only "
        "the 8 electrons of oxygen.",
    seconds=50, checked=True)

add("Laws of chemical combination", I, "multi_statement",
    ms("Which of the following statements are correct?",
       ["According to Dalton's atomic theory, chemical reactions involve reorganisation of atoms, which are "
        "neither created nor destroyed.",
        "Dalton's atomic theory could explain the law of gaseous volumes.",
        "One atomic mass unit is defined as exactly one-twelfth of the mass of one carbon-12 atom.",
        "Equal volumes of all gases at the same temperature and pressure contain equal numbers of molecules.",
        "According to Dalton, atoms of different elements have the same mass."]),
    multi("B", {"a": True, "b": False, "c": True, "d": True, "e": False},
          ["(a), (b) and (c) only", "(b), (d) and (e) only", "(a), (c), (d) and (e) only"]),
    "Dalton's atomic theory, atomic mass unit and Avogadro's law",
    "Dalton's theory explained the laws of chemical combination but not Gay-Lussac's law of gaseous volumes; "
    "Avogadro's hypothesis was needed for that. Dalton held that atoms of different elements differ in mass.",
    ["(a) True: a postulate of Dalton's theory", "(b) False: the theory could not explain the law of gaseous "
     "volumes", "(c) True: definition of 1 u", "(d) True: Avogadro's law",
     "(e) False: atoms of different elements have different masses"],
    why="Any option with (b) or (e) is wrong; (a), (c) and (d) must all appear.",
    ncert=f"{REF1}, Dalton's atomic theory; Avogadro's law; atomic mass", seconds=60)

add("Stoichiometry", I, "statement_pair",
    sp("In a chemical reaction, the reactant present in the smaller mass is always the limiting reagent.",
       "The amount of product formed in a reaction is decided by the limiting reagent."),
    SP_, "Limiting reagent",
    "The limiting reagent is the one that is used up first, judged by moles and the stoichiometric ratio, not "
    "by mass. For 2H₂ + O₂ → 2H₂O, 2 g of H₂ (1 mol) with 8 g of O₂ (0.25 mol): O₂ has the larger mass but is "
    "used up first, so Statement I is false. The product formed depends on the limiting reagent, so Statement "
    "II is true.",
    ["2 g H₂ = 1 mol needs 0.5 mol O₂; only 0.25 mol O₂ is present → O₂ (larger mass) limits",
     "Statement I false", "Product is fixed by the reagent used up first → Statement II true"],
    answer="D", ncert=f"{REF1}, limiting reagent", seconds=45)

v_ch4 = (7 / 2 * 20 - 55) / (7 / 2 - 2)
v_c2h6 = 20 - v_ch4
assert close(v_ch4, 10) and close(v_ch4 + 2 * v_c2h6, 30)
y_bad = (55 - 2 * 20) / (7 - 2)
assert close((20 - y_bad) + 2 * y_bad, 23)
add("Stoichiometry", A, "numerical",
    "20 mL of a mixture of methane and ethane needs exactly 55 mL of oxygen for complete combustion. All volumes "
    "are measured at the same temperature and pressure, and the water formed condenses. The volume of carbon "
    "dioxide formed is:",
    Opts("C", "30 mL", ["20 mL", "40 mL", "23 mL"]),
    "Stoichiometry of gaseous reactions (Gay-Lussac's law of gaseous volumes)",
    "At the same temperature and pressure, volumes of gases are in the ratio of their moles. Write the two "
    "combustion equations, find the composition of the mixture from the oxygen used, then add the CO₂.",
    ["CH₄ + 2O₂ → CO₂ + 2H₂O; C₂H₆ + 7/2 O₂ → 2CO₂ + 3H₂O",
     "Let CH₄ = x mL, C₂H₆ = (20 − x) mL: 2x + 3.5(20 − x) = 55 → x = 10 mL",
     "CO₂ = 1 × 10 + 2 × 10 = 30 mL"],
    why="20 mL assumes each molecule gives one CO₂. 40 mL treats the whole mixture as ethane. 23 mL comes from "
        "using 7 instead of 7/2 volumes of O₂ per volume of ethane.",
    ncert=f"{REF1}, Gay Lussac's law of gaseous volumes; stoichiometry", seconds=120, checked=True)

n_mg = 7.2 / 24
n_o2 = n_mg / 2
m_kclo3 = n_o2 * 2 / 3 * 122.5
assert close(m_kclo3, 12.25)
assert close(n_mg * 2 / 3 * 122.5, 24.5) and close(n_o2 * 122.5, 18.4, 0.01) and close(n_o2 * 3 / 2 * 122.5, 27.6, 0.01)
add("Stoichiometry", A, "numerical",
    "Oxygen obtained by heating potassium chlorate (2KClO₃ → 2KCl + 3O₂) is used to burn magnesium completely "
    "(2Mg + O₂ → 2MgO). The mass of KClO₃ needed to burn 7.2 g of magnesium is (K = 39, Cl = 35.5, O = 16, "
    "Mg = 24):",
    Opts("D", "12.25 g", ["24.5 g", "18.4 g", "27.6 g"]),
    "Stoichiometry of consecutive reactions",
    "Work backwards: moles of Mg → moles of O₂ needed → moles of KClO₃ that give this O₂ → mass.",
    ["Moles of Mg = 7.2 / 24 = 0.30 mol", "O₂ needed = 0.30 / 2 = 0.15 mol (2Mg : 1O₂)",
     "KClO₃ = 0.15 × 2/3 = 0.10 mol (2KClO₃ : 3O₂)", "Molar mass of KClO₃ = 39 + 35.5 + 48 = 122.5 g mol⁻¹",
     "Mass = 0.10 × 122.5 = 12.25 g"],
    why="24.5 g takes 1 mol O₂ per mol Mg. 18.4 g takes 1 mol KClO₃ per mol O₂. 27.6 g inverts the 2 : 3 ratio "
        "of KClO₃ to O₂.",
    ncert=f"{REF1}, stoichiometry and stoichiometric calculations", seconds=100, checked=True)

pc_c2h2 = F(24, 26)
pc_c6h6 = F(72, 78)
assert pc_c2h2 == pc_c6h6
add("Empirical and molecular formulae", A, "assertion_reason",
    ar("Equal masses of ethyne (C₂H₂) and benzene (C₆H₆) contain equal numbers of carbon atoms.",
       "Ethyne and benzene have the same empirical formula, CH, and therefore the same mass per cent of carbon."),
    AR_, "Empirical formula and percentage composition",
    "Mass per cent depends only on the ratio of atoms, which the empirical formula gives. Both compounds are "
    "(CH)ₙ, so both are 12/13 = 92.3% carbon by mass. Equal masses therefore contain equal masses of carbon, "
    "and so equal numbers of carbon atoms. R is true and explains A.",
    ["%C in C₂H₂ = 24/26 × 100 = 92.3%; in C₆H₆ = 72/78 × 100 = 92.3%",
     "Same mass of compound → same mass of carbon → same number of C atoms (A true)",
     "Same empirical formula CH → same % C (R true and explains A)"],
    answer="A", ncert=f"{REF1}, empirical formula for molecular formula", seconds=50)

# ==================================================================== 2. Atomic Structure
topic("Atomic Structure")
REF2 = f"{C11}, 'Structure of Atom'"

e_ph = H_PLANCK * C_LIGHT / 300e-9
assert close(e_ph, 6.626e-19) and close(H_PLANCK * C_LIGHT / 300, 6.626e-28)
assert close(H_PLANCK / 300e-9, 2.209e-27, 0.001) and close(H_PLANCK * C_LIGHT, 1.988e-25, 0.001)
add("Dual nature and uncertainty", B, "numerical",
    "The energy of one photon of light of wavelength 300 nm is (h = 6.626 × 10⁻³⁴ J s, c = 3.0 × 10⁸ m s⁻¹):",
    Opts("B", "6.626 × 10⁻¹⁹ J", ["6.626 × 10⁻²⁸ J", "2.209 × 10⁻²⁷ J", "1.988 × 10⁻²⁵ J"]),
    "Planck's quantum theory: E = hν = hc/λ",
    "Convert the wavelength to metres before using E = hc/λ.",
    ["λ = 300 nm = 3.0 × 10⁻⁷ m", "E = (6.626 × 10⁻³⁴ × 3.0 × 10⁸) / (3.0 × 10⁻⁷)", "E = 6.626 × 10⁻¹⁹ J"],
    why="6.626 × 10⁻²⁸ J leaves λ in nanometres. 2.209 × 10⁻²⁷ J is h/λ (leaves out c). 1.988 × 10⁻²⁵ J is "
        "hc without dividing by λ.",
    ncert=f"{REF2}, particle nature of electromagnetic radiation: Planck's quantum theory", seconds=40,
    checked=True)

add("Quantum numbers and orbitals", B, "direct",
    "Which quantum number gives the orientation of an atomic orbital in space?",
    Opts("C", "Magnetic quantum number (mₗ)", ["Principal quantum number (n)", "Azimuthal quantum number (l)",
                                               "Spin quantum number (mₛ)"]),
    "Meaning of the four quantum numbers",
    "n gives the shell (size and, largely, energy), l gives the subshell and the shape of the orbital, mₗ "
    "gives the spatial orientation of the orbital, and mₛ gives the orientation of the electron's spin.",
    ["n → size and energy", "l → shape", "mₗ → orientation in space", "mₛ → spin of the electron"],
    why="n fixes size and energy, l fixes shape, and mₛ describes the electron's spin, not the orbital.",
    ncert=f"{REF2}, quantum numbers", seconds=25)

add("Electronic configuration", B, "direct",
    "The ground-state electronic configuration of chromium (Z = 24) is:",
    Opts("B", "[Ar] 3d⁵ 4s¹", ["[Ar] 3d⁴ 4s²", "[Ar] 3d⁶", "[Ar] 3d³ 4s² 4p¹"]),
    "Exceptional configurations: extra stability of half-filled subshells",
    "Chromium has 24 electrons. The configuration with one electron in each of the five 3d orbitals and one "
    "in 4s (3d⁵ 4s¹) is more stable than 3d⁴ 4s², because exactly half-filled subshells have extra stability "
    "(symmetrical distribution and larger exchange energy).",
    ["[Ar] = 18 electrons; 6 electrons remain", "Expected 3d⁴ 4s², but 3d⁵ 4s¹ is observed",
     "Six unpaired electrons in Cr"],
    why="[Ar] 3d⁴ 4s² is the expected but not the observed configuration. [Ar] 3d⁶ leaves 4s empty, which is "
        "not the ground state of the atom. Filling 4p before 3d breaks the Aufbau order.",
    ncert=f"{REF2}, stability of completely filled and half-filled subshells", seconds=30)

add("Bohr model and hydrogen spectrum", B, "match_list",
    lists("Match List-I (spectral series of the hydrogen atom) with List-II (orbit n in which the electron "
          "ends after the transition).",
          ["Lyman series", "Balmer series", "Paschen series", "Brackett series"],
          ["n = 3", "n = 1", "n = 4", "n = 2"]),
    match("D", M("II IV I III"), [M("II IV III I"), M("IV II I III"), M("I IV II III")]),
    "Spectral series of hydrogen",
    "Each series is named by the lower orbit reached: Lyman ends in n = 1 (ultraviolet), Balmer in n = 2 "
    "(visible), Paschen in n = 3 and Brackett in n = 4 (infrared).",
    ["Lyman → n = 1 → II", "Balmer → n = 2 → IV", "Paschen → n = 3 → I", "Brackett → n = 4 → III"],
    why="The other codes swap Lyman with Balmer, or Paschen with Brackett.",
    ncert=f"{REF2}, line spectrum of hydrogen", seconds=30)

de = 2.18e-18 * (1 - F(1, 9))
assert close(float(de), 1.94e-18, 0.002) and close(2.18e-18 / 9, 2.42e-19, 0.002)
assert close(2.18e-18 * (1 - 1 / 3), 1.45e-18, 0.003)
add("Bohr model and hydrogen spectrum", I, "numerical",
    "In a hydrogen atom the energy of the electron in the nth orbit is Eₙ = −2.18 × 10⁻¹⁸ (1/n²) J. The "
    "energy needed to excite the electron from n = 1 to n = 3 is:",
    Opts("A", "1.94 × 10⁻¹⁸ J", ["2.42 × 10⁻¹⁹ J", "1.45 × 10⁻¹⁸ J", "2.18 × 10⁻¹⁸ J"]),
    "Bohr model: energy of a transition ΔE = E(final) − E(initial)",
    "The energy absorbed equals the difference between the energies of the two orbits.",
    ["E₁ = −2.18 × 10⁻¹⁸ J; E₃ = −2.18 × 10⁻¹⁸/9 = −2.42 × 10⁻¹⁹ J",
     "ΔE = E₃ − E₁ = 2.18 × 10⁻¹⁸ (1 − 1/9) J", "ΔE = 2.18 × 10⁻¹⁸ × 8/9 = 1.94 × 10⁻¹⁸ J"],
    why="2.42 × 10⁻¹⁹ J is the size of E₃ alone. 1.45 × 10⁻¹⁸ J uses 1/n instead of 1/n². 2.18 × 10⁻¹⁸ J is "
        "the ionisation energy (n = 1 to n = ∞).",
    ncert=f"{REF2}, Bohr's model for hydrogen atom", seconds=50, checked=True)

ke = 2.41e-19
v = math.sqrt(2 * ke / M_E)
lam = H_PLANCK / (M_E * v)
assert close(lam, 1.00e-9, 0.003)
assert close(H_PLANCK / (M_E * math.sqrt(ke / M_E)), 1.41e-9, 0.003)
assert close(H_PLANCK * C_LIGHT / ke, 8.25e-7, 0.003)
assert close(H_PLANCK / (M_E * 2 * ke / M_E), 1.37e-15, 0.005)
add("Dual nature and uncertainty", I, "numerical",
    "An electron has a kinetic energy of 2.41 × 10⁻¹⁹ J. Its de Broglie wavelength is (h = 6.626 × 10⁻³⁴ J s, "
    "mass of electron = 9.11 × 10⁻³¹ kg):",
    Opts("C", "1.00 × 10⁻⁹ m", ["1.41 × 10⁻⁹ m", "8.25 × 10⁻⁷ m", "1.37 × 10⁻¹⁵ m"]),
    "de Broglie relation λ = h/mv, with v found from the kinetic energy",
    "First find the speed from KE = ½mv², then use λ = h/(mv). Equivalently λ = h/√(2m·KE).",
    ["v = √(2 × 2.41 × 10⁻¹⁹ / 9.11 × 10⁻³¹) = 7.27 × 10⁵ m s⁻¹",
     "mv = 9.11 × 10⁻³¹ × 7.27 × 10⁵ = 6.63 × 10⁻²⁵ kg m s⁻¹",
     "λ = 6.626 × 10⁻³⁴ / 6.63 × 10⁻²⁵ = 1.00 × 10⁻⁹ m (1 nm)"],
    shortcut="λ = h/√(2m·KE) = 6.626 × 10⁻³⁴ / √(2 × 9.11 × 10⁻³¹ × 2.41 × 10⁻¹⁹) = 1.0 × 10⁻⁹ m",
    why="1.41 × 10⁻⁹ m uses KE = mv² (drops the ½). 8.25 × 10⁻⁷ m wrongly applies the photon relation "
        "E = hc/λ to an electron. 1.37 × 10⁻¹⁵ m forgets to take the square root when finding v.",
    ncert=f"{REF2}, dual behaviour of matter", seconds=90, checked=True)

add("Dual nature and uncertainty", I, "statement_pair",
    sp("In the photoelectric effect, for light above the threshold frequency, the number of electrons ejected "
       "per second increases with the intensity of the light.",
       "In the photoelectric effect, the kinetic energy of the ejected electrons increases with the intensity "
       "of the light."),
    SP_, "Photoelectric effect",
    "A brighter beam has more photons, so more electrons are ejected: Statement I is true. The kinetic energy of "
    "each ejected electron depends on the frequency of the light (KE = hν − hν₀), not on its intensity: "
    "Statement II is false.",
    ["Intensity → number of photons → number of electrons (I true)",
     "KE = hν − hν₀ depends on frequency only (II false)"],
    answer="C", ncert=f"{REF2}, photoelectric effect", seconds=40)

add("Quantum numbers and orbitals", I, "multi_statement",
    ms("Which of the following statements about atomic orbitals are correct?",
       ["ψ² at a point gives the probability density of finding the electron at that point.",
        "An s orbital is spherically symmetric.",
        "For n = 3, the allowed values of l are 1, 2 and 3.",
        "The d_z² orbital has two lobes along the z axis and a ring of electron density in the xy plane.",
        "All five 3d orbitals have the same shape."]),
    multi("D", {"a": True, "b": True, "c": False, "d": True, "e": False},
          ["(a), (b) and (c) only", "(b), (d) and (e) only", "(a), (b), (d) and (e) only"]),
    "Wave function and shapes of orbitals",
    "ψ itself has no physical meaning; ψ² is the probability density. For a given n, l runs from 0 to n − 1, "
    "so for n = 3 it is 0, 1 and 2. Four of the d orbitals have the same four-lobed shape, but d_z² is "
    "different.",
    ["(a) True", "(b) True", "(c) False: l = 0, 1, 2 for n = 3", "(d) True: shape of d_z²",
     "(e) False: d_z² differs from the other four"],
    why="Options with (c) or (e) are wrong, and (a), (b) and (d) are all true.",
    ncert=f"{REF2}, quantum mechanical model of atom; shapes of atomic orbitals", seconds=60)

add("Electronic configuration", I, "match_list",
    lists("Match List-I (species in its ground state) with List-II (number of unpaired electrons).",
          ["N (Z = 7)", "O (Z = 8)", "Mn²⁺ (Z of Mn = 25)", "Cu⁺ (Z of Cu = 29)"],
          ["0", "2", "3", "5"]),
    match("A", M("III II IV I"), [M("II III IV I"), M("III II I IV"), M("IV II III I")]),
    "Hund's rule and configurations of ions",
    "N: 1s² 2s² 2p³, three unpaired (one in each 2p orbital). O: 2p⁴, two unpaired. Mn²⁺: [Ar] 3d⁵ (4s "
    "electrons are removed first), five unpaired. Cu⁺: [Ar] 3d¹⁰, none unpaired.",
    ["N → 3 → III", "O → 2 → II", "Mn²⁺ → 5 → IV", "Cu⁺ → 0 → I"],
    why="The other codes swap N and O, or Mn²⁺ and Cu⁺, or N and Mn²⁺.",
    ncert=f"{REF2}, filling of orbitals: Hund's rule", seconds=60)

R_H = 1.097e7
lam_he = 1 / (R_H * 4 * (F(1, 4) - F(1, 16)))
assert close(lam_he, 121.5e-9, 0.002)
assert close(1 / (R_H * (1 / 4 - 1 / 16)), 486.2e-9, 0.002) and close(1 / (R_H * 2 * (1 / 4 - 1 / 16)), 243.1e-9, 0.002)
assert close(1 / (R_H * 16 * (1 / 4 - 1 / 16)), 30.4e-9, 0.003)
add("Bohr model and hydrogen spectrum", A, "numerical",
    "The wavelength of the radiation emitted when the electron of a He⁺ ion (Z = 2) falls from n = 4 to n = 2 is "
    "(Rydberg constant R_H = 1.097 × 10⁷ m⁻¹):",
    Opts("B", "121.5 nm", ["486.2 nm", "243.1 nm", "30.4 nm"]),
    "Spectrum of a hydrogen-like ion: 1/λ = R_H Z² (1/n₁² − 1/n₂²)",
    "For a one-electron ion the energy of each level is Z² times that of hydrogen, so the wave number of every "
    "line is multiplied by Z².",
    ["1/λ = 1.097 × 10⁷ × 2² × (1/4 − 1/16)", "= 1.097 × 10⁷ × 4 × 3/16 = 8.23 × 10⁶ m⁻¹",
     "λ = 1.215 × 10⁻⁷ m = 121.5 nm"],
    shortcut="4 × (1/4 − 1/16) = 3/4, which is the factor for the H Lyman n = 2 → 1 line, so λ equals that "
             "line's wavelength, 121.5 nm.",
    why="486.2 nm leaves out Z² (it is the hydrogen line for the same transition). 243.1 nm uses Z instead of "
        "Z². 30.4 nm uses Z⁴.",
    ncert=f"{REF2}, Bohr's model; line spectrum of hydrogen", seconds=90, checked=True)

ke_pe = H_PLANCK * C_LIGHT * (1 / 300e-9 - 1 / 600e-9)
vmax = math.sqrt(2 * ke_pe / M_E)
assert close(vmax, 8.53e5, 0.002)
assert close(math.sqrt(ke_pe / M_E), 6.03e5, 0.002)
assert close(math.sqrt(2 * H_PLANCK * C_LIGHT / 300e-9 / M_E), 1.21e6, 0.005)
assert close(math.sqrt(2 * H_PLANCK * C_LIGHT * (1 / 300e-9 + 1 / 600e-9) / M_E), 1.48e6, 0.003)
add("Dual nature and uncertainty", A, "numerical",
    "The threshold wavelength for a metal is 600 nm. Light of wavelength 300 nm falls on it. The maximum speed "
    "of the photoelectrons emitted is (h = 6.626 × 10⁻³⁴ J s, c = 3.0 × 10⁸ m s⁻¹, mass of electron = "
    "9.11 × 10⁻³¹ kg):",
    Opts("C", "8.53 × 10⁵ m s⁻¹", ["6.03 × 10⁵ m s⁻¹", "1.21 × 10⁶ m s⁻¹", "1.48 × 10⁶ m s⁻¹"]),
    "Photoelectric equation: ½mv² = hν − hν₀ = hc(1/λ − 1/λ₀)",
    "The photon energy minus the work function (hc/λ₀) is the maximum kinetic energy of the electron; then "
    "solve ½mv² for v.",
    ["hc = 6.626 × 10⁻³⁴ × 3.0 × 10⁸ = 1.988 × 10⁻²⁵ J m",
     "KE = 1.988 × 10⁻²⁵ × (1/3.0 × 10⁻⁷ − 1/6.0 × 10⁻⁷) = 3.31 × 10⁻¹⁹ J",
     "v = √(2 × 3.31 × 10⁻¹⁹ / 9.11 × 10⁻³¹) = 8.53 × 10⁵ m s⁻¹"],
    why="6.03 × 10⁵ m s⁻¹ drops the factor 2 (uses KE = mv²). 1.21 × 10⁶ m s⁻¹ ignores the work function. "
        "1.48 × 10⁶ m s⁻¹ adds the work function instead of subtracting it.",
    ncert=f"{REF2}, photoelectric effect", seconds=120, checked=True)

add("Dual nature and uncertainty", A, "assertion_reason",
    ar("Bohr's picture of an electron moving in a well-defined circular orbit around the nucleus is not "
       "consistent with the Heisenberg uncertainty principle.",
       "The exact position and the exact momentum of an electron cannot both be determined at the same time."),
    AR_, "Heisenberg uncertainty principle and the failure of the Bohr model",
    "A definite orbit means knowing exactly where the electron is and how fast it moves at every instant. The "
    "uncertainty principle (R, true) says this is impossible for a microscopic particle, which is exactly why "
    "the Bohr orbit idea fails (A, true). R explains A.",
    ["R: Δx · Δp ≥ h/4π → true", "A defined orbit needs exact x and p at once → ruled out by R",
     "A true and explained by R"],
    answer="A", ncert=f"{REF2}, significance of uncertainty principle; reasons for the failure of the Bohr model",
    seconds=45)

orbitals = [(l, ml) for l in range(4) for ml in range(-l, l + 1) if ml == 1]
assert 2 * len(orbitals) == 6
add("Quantum numbers and orbitals", A, "direct",
    "The maximum number of electrons in an atom that can have the quantum numbers n = 4 and mₗ = +1 is:",
    Opts("D", "6", ["2", "8", "32"]),
    "Allowed combinations of quantum numbers",
    "For n = 4, l can be 0, 1, 2 or 3. mₗ = +1 is possible only when l ≥ 1, so there is one orbital with "
    "mₗ = +1 in each of the 4p, 4d and 4f subshells. Each orbital holds two electrons.",
    ["n = 4 → l = 0, 1, 2, 3", "mₗ = +1 exists for l = 1, 2, 3 → 3 orbitals", "Electrons = 3 × 2 = 6"],
    why="2 counts only one orbital. 8 wrongly includes l = 0, where mₗ can only be 0. 32 is the capacity of the "
        "whole n = 4 shell.",
    ncert=f"{REF2}, quantum numbers", seconds=60)

# ==================================================================== 3. Chemical Bonding and Molecular Structure
topic("Chemical Bonding and Molecular Structure")
REF3 = f"{C11}, 'Chemical Bonding and Molecular Structure'"


def bond_order(nb, na):
    return F(nb - na, 2)


add("VSEPR shapes", B, "direct",
    "The shape of the PCl₅ molecule is:",
    Opts("B", "Trigonal bipyramidal", ["Square pyramidal", "Octahedral", "See-saw"]),
    "VSEPR theory: five bond pairs and no lone pair",
    "Phosphorus in PCl₅ has five bond pairs and no lone pair. Five electron pairs arrange themselves at the "
    "corners of a trigonal bipyramid: three equatorial and two axial P–Cl bonds.",
    ["Valence electrons on P = 5, all used in five P–Cl bonds", "5 bond pairs, 0 lone pairs → trigonal "
     "bipyramidal"],
    why="Square pyramidal needs five bond pairs and one lone pair (as in BrF₅). Octahedral needs six bond pairs. "
        "See-saw is four bond pairs and one lone pair (as in SF₄).",
    ncert=f"{REF3}, VSEPR theory; PCl₅ molecule", seconds=25)

add("Hybridisation and resonance", B, "direct",
    "The hybridisation of each carbon atom in ethene (C₂H₄) is:",
    Opts("C", "sp²", ["sp", "sp³", "dsp²"]),
    "Hybridisation in ethene",
    "Each carbon in ethene forms three σ bonds (two C–H and one C–C) and has no lone pair. It uses three sp² "
    "hybrid orbitals for the σ bonds; the unhybridised 2p orbital on each carbon forms the π bond.",
    ["σ bonds per carbon = 3, lone pairs = 0 → 3 hybrid orbitals → sp²",
     "C=C = one σ (sp²–sp²) + one π (2p–2p)"],
    why="sp is the hybridisation of carbon in ethyne, sp³ in ethane. dsp² needs a d orbital and is not used by "
        "carbon.",
    ncert=f"{REF3}, hybridisation; formation of C₂H₄ molecule", seconds=25)

bo_he2p = bond_order(2, 1)
assert bo_he2p == F(1, 2)
add("Molecular orbital theory", B, "numerical",
    "According to molecular orbital theory, the bond order of the He₂⁺ ion is:",
    Opts("A", "0.5", ["0", "1", "1.5"]),
    "Bond order = ½ (Nb − Na)",
    "He₂⁺ has 2 + 2 − 1 = 3 electrons. Two go into the bonding σ1s orbital and one into the antibonding "
    "σ*1s orbital.",
    ["Configuration: (σ1s)² (σ*1s)¹", "Nb = 2, Na = 1", "Bond order = ½ (2 − 1) = 0.5"],
    why="0 is the bond order of He₂ (four electrons). 1 counts the antibonding electron as non-bonding. 1.5 adds "
        "instead of subtracting.",
    ncert=f"{REF3}, molecular orbital theory: bond order", seconds=30, checked=True)

add("Hydrogen and metallic bonding", B, "statement_pair",
    sp("Methane molecules cannot form hydrogen bonds with one another.",
       "A hydrogen bond forms when a hydrogen atom covalently bonded to a highly electronegative atom such as F, "
       "O or N is attracted to another such electronegative atom."),
    SP_, "Conditions for hydrogen bonding",
    "Carbon is not electronegative enough to make the C–H bond strongly polar, and methane has no lone pair "
    "on a small electronegative atom, so methane cannot form hydrogen bonds: Statement I is true. Statement II "
    "correctly states the condition for a hydrogen bond.",
    ["C–H is nearly non-polar; no N, O or F in CH₄ → Statement I true", "Statement II: definition → true"],
    answer="A", ncert=f"{REF3}, hydrogen bonding", seconds=35)

add("VSEPR shapes", B, "match_list",
    lists("Match List-I (molecule) with List-II (number of lone pairs on the central atom).",
          ["CH₄", "NH₃", "H₂O", "XeF₂"], ["2", "0", "3", "1"]),
    match("B", M("II IV I III"), [M("II I IV III"), M("IV II I III"), M("II IV III I")]),
    "Lone pairs on the central atom",
    "Lone pairs on the central atom = (valence electrons − electrons used in bonds) / 2. C in CH₄ uses all "
    "four electrons. N in NH₃ keeps one pair, O in H₂O keeps two pairs, and Xe in XeF₂ keeps three pairs "
    "(8 − 2 = 6 electrons).",
    ["CH₄: (4 − 4)/2 = 0 → II", "NH₃: (5 − 3)/2 = 1 → IV", "H₂O: (6 − 2)/2 = 2 → I", "XeF₂: (8 − 2)/2 = 3 → III"],
    why="The other codes swap NH₃ with H₂O, CH₄ with NH₃, or H₂O with XeF₂.",
    ncert=f"{REF3}, VSEPR theory", seconds=40)

sigma = 3 + 1 + 1 + 1
pi = 1 + 2
assert (sigma, pi) == (6, 3)
add("Hybridisation and resonance", I, "direct",
    "The numbers of σ and π bonds in acrylonitrile, CH₂=CH–C≡N, are:",
    Opts("D", "6 σ and 3 π", ["6 σ and 2 π", "5 σ and 4 π", "9 σ and 0 π"]),
    "Counting σ and π bonds",
    "Every single bond is one σ bond. A double bond is one σ + one π. A triple bond is one σ + two π.",
    ["C–H bonds: 3 σ", "C=C: 1 σ + 1 π", "C–C: 1 σ", "C≡N: 1 σ + 2 π", "Total: 6 σ and 3 π"],
    why="6 σ and 2 π counts the triple bond as having one π bond. 5 σ and 4 π treats both bonds of the "
        "double bond as π. 9 σ and 0 π counts every line as a σ bond.",
    ncert=f"{REF3}, types of overlapping and nature of covalent bonds", seconds=40)

add("Fajans' rule and dipole moment", I, "assertion_reason",
    ar("LiI has more covalent character than LiF.",
       "The fluoride ion is larger than the iodide ion, so it is more easily polarised."),
    AR_, "Fajans' rules: size of the anion",
    "By Fajans' rules, the larger the anion, the more easily its electron cloud is distorted by the cation and "
    "the greater the covalent character. I⁻ is much larger than F⁻, so LiI is more covalent than LiF: A is "
    "true. R gets the sizes the wrong way round (F⁻ is the smaller ion) and is false.",
    ["Ionic size: I⁻ > F⁻", "Larger anion → more polarisable → more covalent → LiI more covalent (A true)",
     "R says F⁻ is larger → false"],
    answer="C", ncert=f"{REF3}, ionic or electrovalent bond; polar character of covalent bond (Fajans' rules)",
    seconds=40)

add("Fajans' rule and dipole moment", I, "statement_pair",
    sp("CO₂ has zero dipole moment even though each C=O bond is polar.",
       "H₂O has zero dipole moment because its two O–H bond dipoles cancel each other."),
    SP_, "Dipole moment and molecular shape",
    "CO₂ is linear (O=C=O), so the two equal bond dipoles point in opposite directions and cancel: Statement "
    "I is true. H₂O is bent (bond angle about 104.5°), so its O–H bond dipoles add to a resultant of about "
    "1.85 D: Statement II is false.",
    ["CO₂ linear → resultant 0 → I true", "H₂O bent → resultant ≠ 0 → II false"],
    answer="C", ncert=f"{REF3}, polarity of bonds: dipole moment", seconds=35)

add("Molecular orbital theory", I, "multi_statement",
    ms("Which of the following statements of molecular orbital theory are correct?",
       ["The higher the bond order, the longer the bond.",
        "A bonding molecular orbital has lower energy than the atomic orbitals that combine to form it.",
        "The number of molecular orbitals formed equals the number of atomic orbitals that combine.",
        "π molecular orbitals are symmetrical about the internuclear axis.",
        "The He₂ molecule is not expected to exist because its bond order is zero."]),
    multi("C", {"a": False, "b": True, "c": True, "d": False, "e": True},
          ["(a), (b) and (c) only", "(b), (c) and (d) only", "(a), (d) and (e) only"]),
    "Features of molecular orbital theory",
    "Bond length decreases as bond order increases. σ MOs are symmetrical about the bond axis; π MOs are not "
    "(they have a nodal plane containing the axis). He₂ has (σ1s)²(σ*1s)², bond order 0, and does not exist.",
    ["(a) False: higher bond order → shorter bond", "(b) True", "(c) True", "(d) False: that describes σ MOs",
     "(e) True: bond order ½(2 − 2) = 0"],
    why="Any option with (a) or (d) is wrong.",
    ncert=f"{REF3}, molecular orbital theory; bonding in some homonuclear diatomic molecules", seconds=60)

bo_co3 = F(4, 3)
assert round(float(bo_co3), 2) == 1.33
add("Hybridisation and resonance", I, "numerical",
    "The carbonate ion is a resonance hybrid of three equivalent structures, each with one C=O and two C–O "
    "bonds. The average bond order of a C–O bond in CO₃²⁻ is:",
    Opts("B", "1.33", ["1.50", "1.00", "2.00"]),
    "Resonance: average bond order",
    "Across the three equivalent structures each C–O bond is double in one and single in two. The total number "
    "of bonds (4) is shared by the three C–O links.",
    ["Bonds from C to O in one structure = 2 + 1 + 1 = 4", "Average bond order = 4/3 = 1.33",
     "All three C–O bonds are equal in length"],
    why="1.50 would hold for two equivalent structures (as in the nitrite ion or ozone). 1.00 and 2.00 treat "
        "the bonds as pure single or pure double bonds, which resonance rules out.",
    ncert=f"{REF3}, resonance structures: carbonate ion", seconds=40, checked=True)

add("Hybridisation and resonance", I, "match_list",
    lists("Match List-I (molecule) with List-II (hybridisation of the central atom).",
          ["CO₂", "BCl₃", "H₂O", "PF₅"], ["sp³", "sp³d", "sp", "sp²"]),
    match("A", M("III IV I II"), [M("III I IV II"), M("IV III I II"), M("III IV II I")]),
    "Hybridisation from σ bonds plus lone pairs",
    "Count σ bonds and lone pairs on the central atom. CO₂: 2 σ, 0 lp → sp. BCl₃: 3 σ, 0 lp → sp². H₂O: 2 σ, "
    "2 lp → 4 → sp³ (bent shape). PF₅: 5 σ, 0 lp → sp³d.",
    ["CO₂ → sp → III", "BCl₃ → sp² → IV", "H₂O → sp³ → I", "PF₅ → sp³d → II"],
    why="The usual trap is H₂O: its two lone pairs also occupy hybrid orbitals, so it is sp³, not sp².",
    ncert=f"{REF3}, hybridisation", seconds=45)

add("Hydrogen and metallic bonding", I, "statement_pair",
    sp("A hydrogen bond is stronger than a covalent bond.",
       "Intramolecular hydrogen bonding occurs when the hydrogen atom lies between two highly electronegative "
       "atoms present within the same molecule."),
    SP_, "Strength and types of hydrogen bonds",
    "A hydrogen bond is a weak attraction, much weaker than a covalent bond (roughly 10–40 kJ mol⁻¹ against "
    "hundreds of kJ mol⁻¹): Statement I is false. Statement II is the definition of intramolecular hydrogen "
    "bonding (as in o-nitrophenol) and is true.",
    ["H-bond ≪ covalent bond → I false", "Intramolecular H-bond: within one molecule → II true"],
    answer="D", ncert=f"{REF3}, hydrogen bonding: types", seconds=35)

n_o2m = 17
nb, na = 10, 7
assert nb + na + 0 == n_o2m - 0 and bond_order(nb, na) == F(3, 2)
add("Molecular orbital theory", A, "numerical",
    "For the superoxide ion, O₂⁻, molecular orbital theory gives the bond order and the number of unpaired "
    "electrons as:",
    Opts("D", "1.5 and 1", ["2.5 and 1", "1.5 and 2", "1 and 0"]),
    "MO configuration of O₂ and its ions",
    "O₂⁻ has 16 + 1 = 17 electrons. The extra electron enters one of the two half-filled π* orbitals of O₂.",
    ["σ1s² σ*1s² σ2s² σ*2s² σ2p_z² π2p_x² π2p_y² π*2p_x² π*2p_y¹",
     "Nb = 10, Na = 7 → bond order = ½ (10 − 7) = 1.5",
     "One π* orbital singly occupied → 1 unpaired electron (paramagnetic)"],
    why="2.5 and 1 describe O₂⁺. 1.5 and 2 keeps two unpaired electrons as in O₂. 1 and 0 describe the peroxide "
        "ion O₂²⁻.",
    ncert=f"{REF3}, bonding in some homonuclear diatomic molecules: oxygen", seconds=60, checked=True)

add("VSEPR shapes", A, "multi_statement",
    ms("Which of the following statements are correct?",
       ["The nitrogen atom is sp³ hybridised in both NH₃ and NH₄⁺.",
        "The H–N–H bond angle in NH₄⁺ is larger than that in NH₃.",
        "All five P–Cl bonds in PCl₅ are of equal length.",
        "All six S–F bonds in SF₆ are equivalent.",
        "The oxygen atom in H₂O is sp² hybridised."]),
    multi("B", {"a": True, "b": True, "c": False, "d": True, "e": False},
          ["(a), (b) and (c) only", "(b), (c) and (e) only", "(a), (d) and (e) only"]),
    "Hybridisation, lone pairs and bond lengths",
    "N in NH₃ has 3 bond pairs + 1 lone pair and in NH₄⁺ 4 bond pairs: both sp³. In NH₄⁺ there is no lone "
    "pair to squeeze the bonds, so the angle is 109.5° against about 107° in NH₃. In PCl₅ the two axial bonds "
    "suffer more repulsion and are longer than the three equatorial bonds. SF₆ is a regular octahedron. O in "
    "H₂O is sp³.",
    ["(a) True", "(b) True: 109.5° > 107°", "(c) False: axial bonds are longer", "(d) True",
     "(e) False: O is sp³ (2 bond pairs + 2 lone pairs)"],
    why="Options containing (c) or (e) are wrong.",
    ncert=f"{REF3}, VSEPR theory; hybridisation: sp³d and sp³d² (PCl₅, SF₆)", seconds=75)

add("Fajans' rule and dipole moment", A, "assertion_reason",
    ar("CuCl has more covalent character than NaCl.",
       "A cation with an (n−1)dⁿ ns⁰ configuration, such as Cu⁺, polarises an anion more strongly than a cation "
       "with a noble-gas configuration, such as Na⁺."),
    AR_, "Fajans' rules: electronic configuration of the cation",
    "Fajans' rules state that cations with an (n−1)dⁿ ns⁰ configuration, typical of transition metal ions, "
    "are more polarising than cations with the noble-gas ns² np⁶ configuration, because d electrons shield "
    "the nuclear charge poorly. Cu⁺ (3d¹⁰) therefore distorts Cl⁻ more than Na⁺ does, and CuCl is more "
    "covalent. R is true and explains A.",
    ["Cu⁺: [Ar] 3d¹⁰ (pseudo noble gas); Na⁺: [Ne]", "d electrons shield poorly → Cu⁺ more polarising",
     "More polarisation of Cl⁻ → more covalent CuCl"],
    answer="A", ncert=f"{REF3}, polar character of covalent bond (Fajans' rules)", seconds=50)

add("Molecular orbital theory", A, "statement_pair",
    sp("For the N₂ molecule, the σ2p_z molecular orbital is higher in energy than the π2p_x and π2p_y "
       "orbitals.",
       "For the O₂ and F₂ molecules, the σ2p_z molecular orbital is lower in energy than the π2p_x and π2p_y "
       "orbitals."),
    SP_, "Order of molecular orbital energies",
    "For B₂, C₂ and N₂ (up to 14 electrons) the order is … π2p_x = π2p_y < σ2p_z < π*2p … because of "
    "s–p mixing: Statement I is true. For O₂ and F₂ the order is σ2p_z < π2p_x = π2p_y < π*2p …: Statement "
    "II is also true.",
    ["N₂: π2p below σ2p_z → I true", "O₂, F₂: σ2p_z below π2p → II true"],
    answer="A", ncert=f"{REF3}, energy level diagram for molecular orbitals", seconds=45)

lat = 437 + 89 + 419 + 242 / 2 + (-349)
assert lat == 717
assert 437 + 89 + 419 + 242 - 349 == 838 and 437 + 89 + 419 + 121 + 349 == 1415 and -437 + 89 + 419 + 121 - 349 == -157
add("Ionic bonding and lattice enthalpy", A, "numerical",
    "Use the following data (kJ mol⁻¹) to find the lattice enthalpy of KCl(s), defined as the enthalpy change "
    "for KCl(s) → K⁺(g) + Cl⁻(g): enthalpy of sublimation of K = 89; first ionisation enthalpy of K = 419; "
    "bond dissociation enthalpy of Cl₂ = 242; electron gain enthalpy of Cl = −349; standard enthalpy of "
    "formation of KCl(s) = −437.",
    Opts("C", "+717 kJ mol⁻¹", ["+838 kJ mol⁻¹", "+1415 kJ mol⁻¹", "−157 kJ mol⁻¹"]),
    "Born–Haber cycle (Hess's law applied to an ionic solid)",
    "Go from K(s) + ½Cl₂(g) to the gaseous ions by steps, and back to KCl(s) by −(lattice enthalpy). The sum "
    "of the steps equals ΔfH.",
    ["ΔfH = ΔsubH + ΔiH + ½ΔbondH + ΔegH − ΔlatticeH",
     "ΔlatticeH = 89 + 419 + 121 + (−349) − (−437)", "ΔlatticeH = +717 kJ mol⁻¹"],
    why="+838 uses the whole bond enthalpy of Cl₂ instead of half of it. +1415 takes the electron gain enthalpy "
        "as +349. −157 adds ΔfH instead of subtracting it.",
    ncert=f"{C11}, 'Thermodynamics', lattice enthalpy (Born–Haber cycle); {REF3}, lattice enthalpy",
    seconds=100, checked=True)

add("Hybridisation and resonance", A, "direct",
    "When BF₃ combines with a fluoride ion to give BF₄⁻, the hybridisation of boron and the shape around it "
    "change as follows:",
    Opts("D", "sp², trigonal planar → sp³, tetrahedral",
         ["sp³, tetrahedral → sp³d, trigonal bipyramidal", "sp², trigonal planar → sp³, square planar",
          "sp, linear → sp², trigonal planar"]),
    "Change of hybridisation on accepting a lone pair",
    "In BF₃ boron has three bond pairs and an empty 2p orbital: sp², trigonal planar. F⁻ donates a lone pair "
    "into that orbital, so boron now has four bond pairs: sp³, tetrahedral.",
    ["BF₃: 3 σ, 0 lp → sp² (trigonal planar)", "BF₄⁻: 4 σ, 0 lp → sp³ (tetrahedral)"],
    why="Boron has no d orbitals, so sp³d is impossible. Four bond pairs with no lone pair give a tetrahedron, "
        "not a square plane. BF₃ is not sp.",
    ncert=f"{REF3}, hybridisation; VSEPR theory", seconds=45)

# ==================================================================== 4. Chemical Thermodynamics
topic("Chemical Thermodynamics")
REF4 = f"{C11}, 'Thermodynamics'"

assert 300 - 100 == 200 and 300 + 100 == 400
add("First law, work and enthalpy", B, "statement_pair",
    sp("When a system absorbs 300 J of heat and does 100 J of work on the surroundings, its internal energy "
       "increases by 400 J.",
       "In the IUPAC sign convention, work done by the system on the surroundings is taken as positive."),
    SP_, "First law of thermodynamics: ΔU = q + w",
    "With the IUPAC convention used in NCERT, heat absorbed by the system and work done on the system are "
    "positive; work done by the system is negative. So q = +300 J, w = −100 J and ΔU = +200 J, not 400 J: "
    "Statement I is false. Statement II reverses the convention and is false.",
    ["q = +300 J (absorbed)", "w = −100 J (work done by the system)", "ΔU = 300 − 100 = +200 J → I false",
     "Work by the system is negative → II false"],
    answer="B", ncert=f"{REF4}, first law of thermodynamics", seconds=40)

add("Entropy and Gibbs energy", B, "direct",
    "For which of the following processes is the entropy change of the system negative?",
    Opts("A", "Freezing of liquid water into ice", ["Melting of ice", "Evaporation of water",
                                                  "Sublimation of solid iodine"]),
    "Entropy and the state of matter",
    "Entropy measures disorder. Solids are more ordered than liquids, and liquids more than gases. A change "
    "towards a more ordered state lowers the entropy of the system.",
    ["Liquid → solid: particles become fixed → ΔS < 0", "Solid → liquid, liquid → gas and solid → gas: ΔS > 0"],
    why="Melting, evaporation and sublimation all move to a less ordered state, so ΔS is positive.",
    ncert=f"{REF4}, entropy and spontaneity", seconds=25)

add("First law, work and enthalpy", B, "direct",
    "Which of the following is an intensive property?",
    Opts("B", "Temperature", ["Volume", "Internal energy", "Enthalpy"]),
    "Extensive and intensive properties",
    "An extensive property depends on the amount of matter in the system; an intensive property does not. "
    "Temperature is the same whether we take a cupful or a bucketful of water at the same state.",
    ["Volume, internal energy, enthalpy → depend on amount → extensive", "Temperature → independent → intensive"],
    why="Volume, internal energy and enthalpy all double when the system is doubled.",
    ncert=f"{REF4}, extensive and intensive properties", seconds=20)

w_irr = -2 * (15 - 5) * 100
assert w_irr == -2000
add("First law, work and enthalpy", B, "numerical",
    "A gas expands from 5 L to 15 L against a constant external pressure of 2 bar. The work done on the gas is "
    "(1 L bar = 100 J):",
    Opts("C", "−2000 J", ["+2000 J", "−20 J", "−200 J"]),
    "Work against a constant external pressure: w = −p_ext ΔV",
    "During expansion the system does work on the surroundings, so w is negative.",
    ["ΔV = 15 − 5 = 10 L", "w = −2 bar × 10 L = −20 L bar", "w = −20 × 100 J = −2000 J"],
    why="+2000 J has the wrong sign for an expansion. −20 J leaves the answer in L bar. −200 J uses 10 J per "
        "L bar.",
    ncert=f"{REF4}, work (pressure–volume work)", seconds=35, checked=True)

dh_comb = -393.5 + 2 * (-285.8) - (-74.8)
assert close(dh_comb, -890.3, 0.0005)
assert close(-393.5 - 285.8 + 74.8, -604.5, 0.0005) and close(-393.5 + 2 * (-285.8) - 74.8, -1039.9, 0.0005)
add("Hess's law and enthalpies", I, "numerical",
    "The standard enthalpies of formation (kJ mol⁻¹) of CH₄(g), CO₂(g) and H₂O(l) are −74.8, −393.5 and −285.8 "
    "respectively. The standard enthalpy of combustion of methane, CH₄(g) + 2O₂(g) → CO₂(g) + 2H₂O(l), is:",
    Opts("D", "−890.3 kJ mol⁻¹", ["−604.5 kJ mol⁻¹", "−1039.9 kJ mol⁻¹", "+890.3 kJ mol⁻¹"]),
    "ΔrH° = Σ ΔfH°(products) − Σ ΔfH°(reactants)",
    "ΔfH° of an element in its standard state (O₂) is zero. Multiply each ΔfH° by its coefficient.",
    ["Products: −393.5 + 2(−285.8) = −965.1 kJ", "Reactants: −74.8 + 0 = −74.8 kJ",
     "ΔcH° = −965.1 − (−74.8) = −890.3 kJ mol⁻¹"],
    why="−604.5 uses one mole of water instead of two. −1039.9 adds ΔfH of methane instead of subtracting it. "
        "+890.3 subtracts products from reactants.",
    ncert=f"{REF4}, standard enthalpy of reaction from enthalpies of formation", seconds=60, checked=True)

dg = -10 - 300 * (-40) / 1000
assert close(dg, 2.0) and close(-10 / (-40 / 1000), 250)
add("Entropy and Gibbs energy", I, "assertion_reason",
    ar("A reaction with ΔH = −10 kJ mol⁻¹ and ΔS = −40 J K⁻¹ mol⁻¹ (both independent of temperature) is "
       "non-spontaneous at 300 K.",
       "When ΔH and ΔS are both negative, a reaction is spontaneous only below the temperature T = ΔH/ΔS, which "
       "is 250 K for this reaction."),
    AR_, "Gibbs energy and the effect of temperature",
    "ΔG = ΔH − TΔS = −10 − 300 × (−0.040) = +2 kJ mol⁻¹ > 0 at 300 K, so the reaction is non-spontaneous: A "
    "is true. With both ΔH and ΔS negative, ΔG < 0 only while |ΔH| > T|ΔS|, i.e. below ΔH/ΔS = 250 K. Since "
    "300 K is above 250 K, R is true and explains A.",
    ["ΔG(300 K) = −10 + 12 = +2 kJ mol⁻¹ → A true", "T* = ΔH/ΔS = 10 000/40 = 250 K → R true",
     "300 K > 250 K → non-spontaneous, as R predicts"],
    answer="A", ncert=f"{REF4}, Gibbs energy and spontaneity; effect of temperature", seconds=70)

add("Entropy and Gibbs energy", I, "assertion_reason",
    ar("At its melting point, a substance has the same entropy in the solid and in the liquid state.",
       "The entropy of fusion is ΔfusS = ΔfusH/Tf, and ΔfusH is positive."),
    AR_, "Entropy change at a phase transition",
    "Melting absorbs heat (ΔfusH > 0) at constant temperature Tf, so ΔfusS = ΔfusH/Tf is positive: R is "
    "true. Therefore the liquid has a higher entropy than the solid at the melting point, and A is false.",
    ["ΔfusH > 0 and Tf > 0 → ΔfusS > 0 (R true)", "S(liquid) > S(solid) at Tf → A false"],
    answer="D", ncert=f"{REF4}, entropy change in phase transitions", seconds=40)

add("First law, work and enthalpy", I, "multi_statement",
    ms("Which of the following statements are correct?",
       ["For a reaction involving only solids and liquids, ΔH and ΔU differ by a negligible amount.",
        "The heat absorbed by a system at constant pressure equals its enthalpy change.",
        "Enthalpy is an intensive property.",
        "Internal energy is a state function.",
        "When a system loses heat and no work is done on or by it, ΔU is positive."]),
    multi("B", {"a": True, "b": True, "c": False, "d": True, "e": False},
          ["(a), (b) and (c) only", "(b), (d) and (e) only", "(a), (c) and (d) only"]),
    "Enthalpy, internal energy and the first law",
    "For solids and liquids ΔV is very small, so ΔH ≈ ΔU. At constant pressure q_p = ΔH. Enthalpy depends on "
    "the amount of matter, so it is extensive. U is a state function. If q < 0 and w = 0, ΔU = q < 0.",
    ["(a) True", "(b) True: q_p = ΔH", "(c) False: extensive", "(d) True", "(e) False: ΔU = q is negative"],
    why="Options containing (c) or (e) are wrong.",
    ncert=f"{REF4}, enthalpy; extensive and intensive properties", seconds=60)

add("Gibbs energy and K", I, "statement_pair",
    sp("If the standard Gibbs energy change of a reaction is negative, its equilibrium constant is greater "
       "than 1.",
       "For a reaction at equilibrium, the Gibbs energy change ΔG (under the actual conditions) is zero."),
    SP_, "Relation between ΔG°, ΔG and K",
    "ΔG° = −RT ln K. If ΔG° < 0, ln K > 0, so K > 1: Statement I is true. At equilibrium the system has no "
    "further tendency to change, so ΔG = 0 (ΔG°, a fixed number for the reaction, need not be zero): "
    "Statement II is true.",
    ["ΔG° < 0 → ln K > 0 → K > 1 (I true)", "At equilibrium ΔG = 0 (II true)"],
    answer="A", ncert=f"{REF4}, Gibbs energy change and equilibrium", seconds=40)

dfh = 2 * (-393.5) + 3 * (-285.8) - (-1560.0)
assert close(dfh, -84.4, 0.001)
assert close(-393.5 + 3 * (-285.8) + 1560, 309.1, 0.001) and close(2 * (-393.5) + 3 * (-285.8) - 1560, -3204.4, 0.001)
add("Hess's law and enthalpies", A, "numerical",
    "The standard enthalpies of combustion (kJ mol⁻¹) of C(graphite), H₂(g) and C₂H₆(g) are −393.5, −285.8 and "
    "−1560.0 respectively, the water formed being liquid. The standard enthalpy of formation of ethane is:",
    Opts("A", "−84.4 kJ mol⁻¹", ["+84.4 kJ mol⁻¹", "+309.1 kJ mol⁻¹", "−3204.4 kJ mol⁻¹"]),
    "Hess's law: enthalpy of formation from enthalpies of combustion",
    "For the target 2C(graphite) + 3H₂(g) → C₂H₆(g): ΔfH = Σ ΔcH(reactants) − Σ ΔcH(products).",
    ["Σ ΔcH(reactants) = 2(−393.5) + 3(−285.8) = −787.0 − 857.4 = −1644.4 kJ",
     "ΔfH = −1644.4 − (−1560.0) = −84.4 kJ mol⁻¹"],
    why="+84.4 subtracts the wrong way round. +309.1 uses one mole of carbon instead of two. −3204.4 adds the "
        "enthalpy of combustion of ethane instead of subtracting it.",
    ncert=f"{REF4}, Hess's law of constant heat summation; enthalpy of combustion", seconds=90, checked=True)

w_rev = -2.303 * 2 * 8.314 * 300 * math.log10(100 / 10)
assert close(w_rev, -11490, 0.002) and close(2 * 8.314 * 300, 4990, 0.002)
add("First law, work and enthalpy", A, "numerical",
    "2 mol of an ideal gas expands isothermally and reversibly at 300 K from 10 L to 100 L. The heat absorbed "
    "by the gas (q) and the change in its internal energy (ΔU) are (R = 8.314 J K⁻¹ mol⁻¹):",
    Opts("C", "q = +11.49 kJ, ΔU = 0", ["q = −11.49 kJ, ΔU = 0", "q = 0, ΔU = −11.49 kJ",
                                         "q = +4.99 kJ, ΔU = 0"]),
    "Reversible isothermal expansion of an ideal gas",
    "For an ideal gas at constant temperature ΔU = 0, so q = −w. The reversible work is "
    "w = −2.303 nRT log (V_f/Vᵢ).",
    ["w = −2.303 × 2 × 8.314 × 300 × log (100/10) J", "w = −11 488 J = −11.49 kJ (log 10 = 1)",
     "ΔU = 0 (isothermal, ideal gas) → q = −w = +11.49 kJ"],
    why="q = −11.49 kJ gives the sign of w to q. q = 0, ΔU = −11.49 kJ describes an adiabatic change, not an "
        "isothermal one. q = +4.99 kJ uses log instead of ln (leaves out 2.303).",
    ncert=f"{REF4}, isothermal and free expansion of an ideal gas", seconds=90, checked=True)

ds = 2 * 193 - 192 - 3 * 131
dg_nh3 = -92.2 - 298 * ds / 1000
assert ds == -199 and close(dg_nh3, -32.9, 0.002)
assert close(-92.2 + 298 * ds / 1000, -151.5, 0.002)
assert close(-92.2 - 298 * (193 - 192 - 131) / 1000, -53.5, 0.002) and close(-92.2 - 25 * ds / 1000, -87.2, 0.002)
add("Entropy and Gibbs energy", A, "numerical",
    "For N₂(g) + 3H₂(g) → 2NH₃(g), ΔH° = −92.2 kJ mol⁻¹ at 298 K. The standard molar entropies (J K⁻¹ mol⁻¹) "
    "are N₂ = 192, H₂ = 131 and NH₃ = 193. ΔG° for the reaction at 298 K is:",
    Opts("B", "−32.9 kJ mol⁻¹", ["−151.5 kJ mol⁻¹", "−53.5 kJ mol⁻¹", "−87.2 kJ mol⁻¹"]),
    "ΔrS° from standard entropies, then ΔG° = ΔH° − TΔS°",
    "Find ΔrS° with the stoichiometric coefficients, convert it to kJ, and use the temperature in kelvin.",
    ["ΔrS° = 2(193) − [192 + 3(131)] = 386 − 585 = −199 J K⁻¹ mol⁻¹",
     "TΔS° = 298 × (−0.199) = −59.3 kJ mol⁻¹", "ΔG° = −92.2 − (−59.3) = −32.9 kJ mol⁻¹"],
    why="−151.5 takes ΔrS° as +199. −53.5 ignores the coefficients when finding ΔrS° (gets −130). −87.2 uses "
        "the temperature in °C (25) instead of 298 K.",
    ncert=f"{REF4}, entropy; Gibbs energy change", seconds=110, checked=True)

add("First law, work and enthalpy", A, "match_list",
    lists("Match List-I (reaction, all gases ideal) with List-II (relation between ΔH and ΔU at temperature T).",
          ["N₂O₄(g) → 2NO₂(g)", "2SO₂(g) + O₂(g) → 2SO₃(g)", "H₂(g) + Cl₂(g) → 2HCl(g)",
           "CH₄(g) + 2O₂(g) → CO₂(g) + 2H₂O(l)"],
          ["ΔH = ΔU", "ΔH = ΔU + RT", "ΔH = ΔU − RT", "ΔH = ΔU − 2RT"]),
    match("D", M("II III I IV"), [M("II III IV I"), M("III II I IV"), M("II I III IV")]),
    "ΔH = ΔU + Δn_g RT",
    "Only gaseous species count in Δn_g. In the combustion of methane the water is liquid.",
    ["N₂O₄ → 2NO₂: Δn_g = 2 − 1 = +1 → ΔH = ΔU + RT → II",
     "2SO₂ + O₂ → 2SO₃: Δn_g = 2 − 3 = −1 → ΔH = ΔU − RT → III",
     "H₂ + Cl₂ → 2HCl: Δn_g = 0 → ΔH = ΔU → I",
     "CH₄ + 2O₂ → CO₂ + 2H₂O(l): Δn_g = 1 − 3 = −2 → ΔH = ΔU − 2RT → IV"],
    why="The trap is the last reaction: counting liquid water as gas gives Δn_g = 0 and ΔH = ΔU.",
    ncert=f"{REF4}, enthalpy: ΔH = ΔU + Δn_g RT", seconds=75)

# ==================================================================== 5. Solutions
topic("Solutions")
REF5 = f"{C12}, 'Solutions'"

m_glu = (9 / 180) / 0.250
assert close(m_glu, 0.2) and close(9 / 180, 0.05) and close(9 / 250, 0.036) and close((9 / 180) / 250, 0.0002)
add("Concentration terms", B, "numerical",
    "9 g of glucose (molar mass 180 g mol⁻¹) is dissolved in 250 g of water. The molality of the solution is:",
    Opts("B", "0.2 m", ["0.05 m", "0.036 m", "0.0002 m"]),
    "Molality = moles of solute per kilogram of solvent",
    "Find the moles of glucose and divide by the mass of water in kilograms.",
    ["Moles of glucose = 9 / 180 = 0.05 mol", "Mass of water = 250 g = 0.250 kg", "Molality = 0.05 / 0.250 = 0.2 m"],
    why="0.05 m is just the number of moles. 0.036 m divides grams of solute by grams of water. 0.0002 m divides "
        "by the mass of water in grams.",
    ncert=f"{REF5}, expressing concentration of solutions: molality", seconds=30, checked=True)

add("Raoult's law and ideal solutions", B, "direct",
    "Which of the following pairs of liquids forms a nearly ideal solution?",
    Opts("A", "Benzene and toluene", ["Phenol and aniline", "Carbon disulphide and acetone",
                                      "Ethanol and acetone"]),
    "Ideal solutions",
    "An ideal solution forms when the A–B interactions are nearly the same as the A–A and B–B interactions, as "
    "for two similar non-polar hydrocarbons such as benzene and toluene (or n-hexane and n-heptane).",
    ["Benzene and toluene: similar molecules, similar forces → nearly ideal",
     "Phenol + aniline: negative deviation; CS₂ + acetone and ethanol + acetone: positive deviation"],
    why="Phenol and aniline form a hydrogen bond between unlike molecules (negative deviation). Carbon "
        "disulphide–acetone and ethanol–acetone mixtures show positive deviation.",
    ncert=f"{REF5}, ideal and non-ideal solutions", seconds=30)

add("Colligative properties", B, "statement_pair",
    sp("Reverse osmosis takes place when a pressure larger than the osmotic pressure is applied to the solution "
       "side.",
       "The relative lowering of vapour pressure of a solution containing a non-volatile solute equals the mole "
       "fraction of the solvent."),
    SP_, "Reverse osmosis and relative lowering of vapour pressure",
    "If a pressure greater than the osmotic pressure is applied on the solution side, pure solvent is pushed "
    "out through the semipermeable membrane: reverse osmosis, used in desalination. Statement I is true. "
    "Relative lowering (p° − p)/p° equals the mole fraction of the solute, not of the solvent: Statement II is "
    "false.",
    ["Applied pressure > π → solvent flows out of the solution → I true", "(p° − p)/p° = x(solute) → II false"],
    answer="C", ncert=f"{REF5}, reverse osmosis and water purification; relative lowering of vapour pressure",
    seconds=40)

n_w, n_g = 178.2 / 18, 18 / 180
p = 760 * n_w / (n_w + n_g)
assert close(p, 752.4, 0.0005) and close(760 - p, 7.6, 0.005) and close(760 * (1 - 18 / 178.2), 683.2, 0.002)
add("Raoult's law and ideal solutions", I, "numerical",
    "18 g of glucose (C₆H₁₂O₆) is dissolved in 178.2 g of water at 100 °C, where the vapour pressure of pure "
    "water is 760 mm Hg. The vapour pressure of the solution is (H = 1, C = 12, O = 16):",
    Opts("C", "752.4 mm Hg", ["7.6 mm Hg", "683.2 mm Hg", "760.0 mm Hg"]),
    "Raoult's law for a non-volatile solute: p = x(solvent) · p°",
    "Only water contributes to the vapour pressure. Find its mole fraction from the moles of water and glucose.",
    ["Moles of water = 178.2 / 18 = 9.9 mol; moles of glucose = 18 / 180 = 0.1 mol",
     "x(water) = 9.9 / 10.0 = 0.99", "p = 0.99 × 760 = 752.4 mm Hg"],
    why="7.6 mm Hg is the lowering of vapour pressure, not the vapour pressure. 683.2 mm Hg uses the mass ratio "
        "18/178.2 as if it were the mole fraction of the solute. 760.0 mm Hg ignores the solute.",
    ncert=f"{REF5}, vapour pressure of solutions of solids in liquids; relative lowering", seconds=60,
    checked=True)

M_x = 2.53 * 1.28 * 1000 / (0.253 * 100)
assert close(M_x, 128)
assert close(2.53 * 1.28 / (0.253 * 1), 12.8) and close(1.28 * 1000 / (100 * 0.253 * 2.53), 20.0)
assert close(2.53 * 1.28 * 1000 / (0.253 * 10), 1280)
add("Colligative properties", I, "numerical",
    "1.28 g of a non-volatile, non-electrolyte solute dissolved in 100 g of benzene raises its boiling point by "
    "0.253 K. The molar mass of the solute is (K_b of benzene = 2.53 K kg mol⁻¹):",
    Opts("D", "128 g mol⁻¹", ["12.8 g mol⁻¹", "20.0 g mol⁻¹", "1280 g mol⁻¹"]),
    "Elevation of boiling point: ΔT_b = K_b · m",
    "Molality m = ΔT_b / K_b, and m = (w₂/M₂) / (w₁ in kg). Solve for M₂.",
    ["m = 0.253 / 2.53 = 0.100 mol kg⁻¹", "Moles of solute = 0.100 × 0.100 kg = 0.0100 mol",
     "M₂ = 1.28 / 0.0100 = 128 g mol⁻¹"],
    shortcut="M₂ = K_b × w₂ × 1000 / (ΔT_b × w₁) = 2.53 × 1.28 × 1000 / (0.253 × 100) = 128",
    why="12.8 takes the benzene as 1 kg. 20.0 multiplies ΔT_b by K_b instead of dividing. 1280 takes 100 g as "
        "0.01 kg.",
    ncert=f"{REF5}, elevation of boiling point", seconds=70, checked=True)

add("Raoult's law and ideal solutions", I, "multi_statement",
    ms("Which of the following are true for a solution of two volatile liquids A and B that shows a positive "
       "deviation from Raoult's law?",
       ["The A–B interactions are weaker than the A–A and B–B interactions.",
        "Such solutions form maximum-boiling azeotropes.",
        "The enthalpy of mixing is positive.",
        "The volume of mixing is positive.",
        "Its azeotrope can be separated into pure A and pure B by fractional distillation."]),
    multi("B", {"a": True, "b": False, "c": True, "d": True, "e": False},
          ["(a), (b) and (c) only", "(c), (d) and (e) only", "(a), (b), (c) and (d) only"]),
    "Non-ideal solutions with positive deviation",
    "Weaker A–B attractions let molecules escape more easily, so the vapour pressure is higher than Raoult's "
    "law predicts. Mixing absorbs heat (ΔmixH > 0) and the volume increases (ΔmixV > 0). Large positive "
    "deviation gives a minimum-boiling azeotrope; an azeotrope boils at constant composition, so fractional "
    "distillation cannot separate it.",
    ["(a) True", "(b) False: positive deviation → minimum-boiling azeotrope", "(c) True", "(d) True",
     "(e) False: azeotropes distil unchanged"],
    why="Options with (b) or (e) are wrong.",
    ncert=f"{REF5}, ideal and non-ideal solutions; azeotropes", seconds=60)

add("van't Hoff factor", I, "match_list",
    lists("Match List-I (solute in dilute aqueous solution, assuming complete dissociation of electrolytes) with "
          "List-II (van't Hoff factor, i).",
          ["Glucose", "KCl", "K₂SO₄", "Na₃PO₄"], ["3", "1", "4", "2"]),
    match("C", M("II IV I III"), [M("II I IV III"), M("IV II I III"), M("II IV III I")]),
    "van't Hoff factor for complete dissociation",
    "i equals the number of ions produced from one formula unit. A non-electrolyte gives i = 1.",
    ["Glucose: no dissociation → 1 → II", "KCl → K⁺ + Cl⁻ → 2 → IV", "K₂SO₄ → 2K⁺ + SO₄²⁻ → 3 → I",
     "Na₃PO₄ → 3Na⁺ + PO₄³⁻ → 4 → III"],
    why="The other codes swap KCl with K₂SO₄, glucose with KCl, or K₂SO₄ with Na₃PO₄.",
    ncert=f"{REF5}, abnormal molar masses: van't Hoff factor", seconds=35)

c_glu = 3 * 0.05
assert close(c_glu * 180, 27) and close(0.05 * 180, 9) and close(0.10 * 180, 18) and close(0.05 / 3 * 180, 3.0)
add("van't Hoff factor", A, "numerical",
    "At 300 K, what mass of glucose (molar mass 180 g mol⁻¹) must be dissolved per litre of solution to make it "
    "isotonic with a 0.05 M aqueous solution of CaCl₂? Assume that CaCl₂ is completely dissociated.",
    Opts("A", "27 g", ["9.0 g", "18 g", "3.0 g"]),
    "Isotonic solutions have equal osmotic pressure: π = iCRT",
    "At the same temperature, equal osmotic pressure means equal i × C. CaCl₂ gives three ions (i = 3); "
    "glucose does not dissociate (i = 1).",
    ["i(CaCl₂) × C = 3 × 0.05 = 0.15 mol L⁻¹ of particles", "Glucose needed = 0.15 mol L⁻¹",
     "Mass = 0.15 × 180 = 27 g per litre"],
    why="9.0 g ignores the dissociation of CaCl₂. 18 g takes i = 2. 3.0 g divides by i instead of multiplying.",
    ncert=f"{REF5}, osmosis and osmotic pressure; van't Hoff factor", seconds=60, checked=True)

i_assoc = 1 - 0.8 / 2
dtf = i_assoc * 5.12 * 0.1
assert close(dtf, 0.307, 0.002) and close(5.12 * 0.1, 0.512) and close(0.5 * 0.512, 0.256)
assert close((1 - 0.8) * 0.512, 0.102, 0.005)
add("van't Hoff factor", A, "numerical",
    "A solute X dimerises in benzene (2X ⇌ X₂). In a 0.1 m solution of X in benzene, 80% of X is dimerised. "
    "The depression of freezing point of this solution is (K_f of benzene = 5.12 K kg mol⁻¹):",
    Opts("B", "0.307 K", ["0.512 K", "0.256 K", "0.102 K"]),
    "van't Hoff factor for association",
    "For 2X ⇌ X₂ with degree of association α, 1 mol of X gives (1 − α) mol X + α/2 mol X₂. So "
    "i = 1 − α/2.",
    ["i = 1 − 0.8/2 = 0.6", "ΔT_f = i K_f m = 0.6 × 5.12 × 0.1", "ΔT_f = 0.307 K"],
    why="0.512 K ignores association (i = 1). 0.256 K assumes complete dimerisation (i = 0.5). 0.102 K uses "
        "i = 1 − α, forgetting the dimers formed.",
    ncert=f"{REF5}, abnormal molar masses: van't Hoff factor", seconds=90, checked=True)

add("Concentration terms", A, "statement_pair",
    sp("A 0.1 m aqueous solution of NaCl and a 0.1 m aqueous solution of glucose have the same freezing point.",
       "Molality does not change with temperature, whereas molarity does."),
    SP_, "Colligative properties of electrolytes; temperature dependence of concentration terms",
    "NaCl dissociates into Na⁺ and Cl⁻ (i ≈ 2), so its 0.1 m solution has nearly twice as many solute "
    "particles and a lower freezing point than 0.1 m glucose: Statement I is false. Molality uses the mass of "
    "solvent, which does not change with temperature; molarity uses the volume of solution, which does: "
    "Statement II is true.",
    ["i(NaCl) ≈ 2, i(glucose) = 1 → different ΔT_f → I false",
     "Mass is independent of temperature, volume is not → II true"],
    answer="D", ncert=f"{REF5}, expressing concentration of solutions; van't Hoff factor", seconds=45)

# ==================================================================== 6. Equilibrium
topic("Equilibrium")
REF6 = f"{C11}, 'Equilibrium'"

poh = -math.log10(1e-4)
assert close(14 - poh, 10)
add("Acids, bases and pH", B, "numerical",
    "An aqueous solution at 298 K has [OH⁻] = 1.0 × 10⁻⁴ mol L⁻¹. Its pH is (K_w = 1.0 × 10⁻¹⁴):",
    Opts("C", "10", ["4", "−4", "1.0 × 10⁻¹⁰"]),
    "pH + pOH = 14 at 298 K",
    "Find pOH = −log [OH⁻] and subtract it from 14.",
    ["pOH = −log (1.0 × 10⁻⁴) = 4", "pH = 14 − 4 = 10"],
    why="4 is the pOH. −4 drops the minus sign in the definition. 1.0 × 10⁻¹⁰ is [H⁺], not the pH.",
    ncert=f"{REF6}, the pH scale", seconds=25, checked=True)

add("Kp, Kc and Le Chatelier", B, "direct",
    "For the equilibrium CaCO₃(s) ⇌ CaO(s) + CO₂(g), the equilibrium constant K_p is:",
    Opts("B", "p(CO₂)", ["p(CO₂) × [CaO]/[CaCO₃]", "1/p(CO₂)", "p(CO₂)²"]),
    "Heterogeneous equilibrium",
    "The concentration (activity) of a pure solid is constant and is taken as 1, so solids do not appear in "
    "the expression. Only the gas remains.",
    ["Kp = p(CO₂) × a(CaO)/a(CaCO₃)", "a(solid) = 1 → Kp = p(CO₂)"],
    why="Pure solids are left out of K. 1/p(CO₂) is the expression for the reverse reaction. The coefficient "
        "of CO₂ is 1, so it is not squared.",
    ncert=f"{REF6}, heterogeneous equilibria", seconds=25)

add("Acids, bases and pH", B, "direct",
    "The conjugate base of H₂PO₄⁻ is:",
    Opts("D", "HPO₄²⁻", ["H₃PO₄", "PO₄³⁻", "H₂PO₄²⁻"]),
    "Brønsted–Lowry conjugate acid–base pairs",
    "A conjugate base is what remains after the acid gives up one proton (H⁺): remove one H and add one "
    "negative charge.",
    ["H₂PO₄⁻ − H⁺ → HPO₄²⁻"],
    why="H₃PO₄ is the conjugate acid of H₂PO₄⁻. PO₄³⁻ is two protons away. H₂PO₄²⁻ adds a charge without "
        "removing a proton.",
    ncert=f"{REF6}, Brønsted–Lowry acids and bases", seconds=20)

add("Physical equilibria and Henry's law", B, "statement_pair",
    sp("At a given temperature, the equilibrium vapour pressure of water in a closed vessel depends on the "
       "amount of liquid water present.",
       "The solubility of a gas in a liquid decreases when the pressure of the gas over the liquid is "
       "increased."),
    SP_, "Liquid–vapour equilibrium and Henry's law",
    "Equilibrium vapour pressure depends only on the liquid and the temperature, not on how much liquid is "
    "present (as long as some liquid remains): Statement I is false. By Henry's law the solubility of a gas "
    "increases with its partial pressure (soda bottles are sealed under high CO₂ pressure): Statement II is "
    "false.",
    ["Vapour pressure: fixed at a given T → I false", "Henry's law: solubility ∝ pressure → II false"],
    answer="B", ncert=f"{REF6}, equilibrium in physical processes; Henry's law", seconds=40)

add("Acids, bases and pH", B, "match_list",
    lists("Match List-I (term) with List-II (definition).",
          ["Arrhenius acid", "Brønsted–Lowry acid", "Lewis acid", "Lewis base"],
          ["Electron-pair donor", "Proton donor", "Gives H⁺ (H₃O⁺) ions when dissolved in water",
           "Electron-pair acceptor"]),
    match("A", M("III II IV I"), [M("II III IV I"), M("III II I IV"), M("IV II III I")]),
    "Concepts of acids and bases",
    "Arrhenius: an acid increases H⁺ ions in water. Brønsted–Lowry: an acid donates a proton. Lewis: an acid "
    "accepts an electron pair and a base donates one.",
    ["Arrhenius acid → III", "Brønsted–Lowry acid → II", "Lewis acid → IV", "Lewis base → I"],
    why="The other codes swap the Arrhenius and Brønsted definitions, or the Lewis acid and base.",
    ncert=f"{REF6}, acids, bases and salts", seconds=30)

add("Kp, Kc and Le Chatelier", I, "match_list",
    lists("The equilibrium constant of N₂(g) + 3H₂(g) ⇌ 2NH₃(g) at a certain temperature is K. Match List-I "
          "(equilibrium at the same temperature) with List-II (its equilibrium constant).",
          ["2NH₃(g) ⇌ N₂(g) + 3H₂(g)", "½N₂(g) + 3/2 H₂(g) ⇌ NH₃(g)", "2N₂(g) + 6H₂(g) ⇌ 4NH₃(g)",
           "NH₃(g) ⇌ ½N₂(g) + 3/2 H₂(g)"],
          ["K²", "1/K", "1/√K", "√K"]),
    match("B", M("II IV I III"), [M("II III I IV"), M("IV II I III"), M("I IV II III")]),
    "Equilibrium constant of related equations",
    "Reversing an equation inverts K. Multiplying an equation by n raises K to the power n (halving gives the "
    "square root).",
    ["Reverse → 1/K → II", "Halve → K^½ → IV", "Double → K² → I", "Reverse and halve → 1/K^½ → III"],
    why="The other codes mix up the halved forward reaction with the halved reverse reaction, or reversing "
        "with doubling.",
    ncert=f"{REF6}, equilibrium constant: relations for reverse and multiplied equations", seconds=50)

RT = 0.0831 * 500
kp = 0.04 * RT
assert close(kp, 1.66, 0.002) and close(0.04 / RT, 9.63e-4, 0.002) and close(0.04 * RT ** 2, 69.1, 0.002)
add("Kp, Kc and Le Chatelier", I, "numerical",
    "For PCl₅(g) ⇌ PCl₃(g) + Cl₂(g), K_c = 0.04 mol L⁻¹ at 500 K. K_p at the same temperature is "
    "(R = 0.0831 L bar K⁻¹ mol⁻¹):",
    Opts("C", "1.66 bar", ["9.63 × 10⁻⁴ bar", "0.04 bar", "69.1 bar"]),
    "K_p = K_c (RT)^Δn",
    "Δn = moles of gaseous products − moles of gaseous reactants = 2 − 1 = 1.",
    ["RT = 0.0831 × 500 = 41.55 L bar mol⁻¹", "K_p = 0.04 × (41.55)¹ = 1.66 bar"],
    why="9.63 × 10⁻⁴ divides by RT (Δn taken as −1). 0.04 assumes K_p = K_c (Δn = 0). 69.1 uses (RT)².",
    ncert=f"{REF6}, relationship between K_p and K_c", seconds=45, checked=True)

add("Kp, Kc and Le Chatelier", I, "assertion_reason",
    ar("Increasing the pressure on the equilibrium 2SO₂(g) + O₂(g) ⇌ 2SO₃(g) favours the dissociation of SO₃.",
       "When the pressure on a gaseous equilibrium is increased, it shifts in the direction in which the number "
       "of moles of gas decreases."),
    AR_, "Le Chatelier's principle: effect of pressure",
    "The forward reaction goes from 3 mol of gas to 2 mol. Raising the pressure shifts the equilibrium "
    "towards fewer moles of gas, i.e. towards SO₃, so formation of SO₃ (not its dissociation) is favoured: A "
    "is false. R is the correct statement of the pressure effect.",
    ["Reactants: 2 + 1 = 3 mol gas; products: 2 mol gas", "Higher pressure → shift to SO₃ side → A false",
     "R true"],
    answer="D", ncert=f"{REF6}, effect of pressure change", seconds=40)

ph_salt = 7 + 0.5 * (4.74 + math.log10(0.1))
assert close(ph_salt, 8.87, 0.001) and close(7 + 0.5 * 4.74, 9.37, 0.001)
assert close(14 - ph_salt, 5.13, 0.002) and close(7 + 0.5 * 4.74 + math.log10(0.1), 8.37, 0.001)
add("Hydrolysis and buffers", I, "numerical",
    "The pH of a 0.1 M aqueous solution of sodium acetate at 298 K is (pK_a of acetic acid = 4.74, pK_w = 14):",
    Opts("D", "8.87", ["9.37", "5.13", "8.37"]),
    "Hydrolysis of the salt of a weak acid and a strong base: pH = 7 + ½(pK_a + log c)",
    "Acetate ions take a proton from water (CH₃COO⁻ + H₂O ⇌ CH₃COOH + OH⁻), so the solution is basic.",
    ["pH = 7 + ½ pK_a + ½ log c", "= 7 + 2.37 + ½(−1)", "= 8.87"],
    why="9.37 leaves out the concentration term. 5.13 is 14 − 8.87, as if the salt gave an acidic solution. "
        "8.37 forgets to halve log c.",
    ncert=f"{REF6}, hydrolysis of salts and the pH of their solutions", seconds=60, checked=True)

add("Solubility product", I, "statement_pair",
    sp("A precipitate of a sparingly soluble salt forms only when its ionic product is less than its K_sp.",
       "At a given temperature, the solubility product of a sparingly soluble salt is a constant."),
    SP_, "Solubility product and precipitation",
    "Precipitation occurs when the ionic product exceeds K_sp (the solution would be supersaturated); if the "
    "ionic product is less than K_sp, more salt can dissolve. Statement I is false. K_sp is an equilibrium "
    "constant and depends only on temperature: Statement II is true.",
    ["Q > K_sp → precipitation; Q < K_sp → no precipitate → I false", "K_sp constant at fixed T → II true"],
    answer="D", ncert=f"{REF6}, solubility equilibria of sparingly soluble salts", seconds=40)

ph_naoh = 14 + math.log10(1e-3)
assert close(ph_naoh, 11)
add("Acids, bases and pH", I, "multi_statement",
    ms("Which of the following statements are correct for aqueous solutions at 298 K?",
       ["The pH of a 1.0 × 10⁻³ M NaOH solution is 3.",
        "When the pH increases by one unit, [H⁺] decreases ten times.",
        "Ammonia acts as a Lewis base.",
        "A strong acid has a large pK_a value.",
        "For a conjugate acid–base pair, K_a × K_b = K_w."]),
    multi("B", {"a": False, "b": True, "c": True, "d": False, "e": True},
          ["(a), (b) and (c) only", "(c), (d) and (e) only", "(a), (b), (c) and (e) only"]),
    "pH, Lewis bases and K_a–K_b relation",
    "1.0 × 10⁻³ M NaOH has pOH 3 and pH 11. pH is a log scale, so one unit is a factor of ten in [H⁺]. NH₃ has a "
    "lone pair to donate. A strong acid has a large K_a, hence a small (even negative) pK_a. K_a K_b = K_w for "
    "a conjugate pair.",
    ["(a) False: pH = 11", "(b) True", "(c) True", "(d) False: small pK_a", "(e) True"],
    why="Options containing (a) or (d) are wrong.",
    ncert=f"{REF6}, ionisation of acids and bases; relation between K_a and K_b", seconds=60)

add("Kp, Kc and Le Chatelier", I, "direct",
    "The equilibrium Fe³⁺(aq) + SCN⁻(aq) ⇌ [Fe(SCN)]²⁺(aq) gives a deep red colour. When oxalic acid, which forms "
    "a stable complex with Fe³⁺ ions, is added to this equilibrium mixture:",
    Opts("A", "The intensity of the red colour decreases",
         ["The intensity of the red colour increases",
          "The colour does not change because the equilibrium constant stays the same",
          "The concentration of [Fe(SCN)]²⁺ increases"]),
    "Le Chatelier's principle: removing a reactant",
    "Oxalic acid removes free Fe³⁺ ions as a stable complex. To make up for the loss, the equilibrium shifts "
    "to the left, so [Fe(SCN)]²⁺ decreases and the red colour fades. K is unchanged; the composition changes.",
    ["Fe³⁺ removed → Q > K", "Equilibrium shifts backwards → less [Fe(SCN)]²⁺ → red colour fades"],
    why="Removing a reactant cannot increase the product. K stays the same, but the concentrations shift "
        "to satisfy it again.",
    ncert=f"{REF6}, effect of concentration change (Fe³⁺/SCN⁻ equilibrium)", seconds=40)

c0, a = 2 / 4, 0.4
kc = (c0 * a) ** 2 / (c0 * (1 - a))
assert close(kc, 0.133, 0.003)
assert close((2 * a) ** 2 / (2 * (1 - a)), 0.533, 0.003) and close(a ** 2 / (1 - a), 0.267, 0.003)
assert close(c0 * a ** 2, 0.080)
add("Kp, Kc and Le Chatelier", A, "numerical",
    "2.0 mol of COCl₂(g) is heated in a closed 4.0 L vessel. At equilibrium, 40% of it has dissociated: "
    "COCl₂(g) ⇌ CO(g) + Cl₂(g). The value of K_c is:",
    Opts("C", "0.133 mol L⁻¹", ["0.533 mol L⁻¹", "0.267 mol L⁻¹", "0.080 mol L⁻¹"]),
    "K_c from the degree of dissociation",
    "Find the equilibrium moles from α, convert them to concentrations using the volume, then substitute.",
    ["Initial [COCl₂] = 2.0 / 4.0 = 0.50 M", "At equilibrium: [CO] = [Cl₂] = 0.50 × 0.4 = 0.20 M; "
     "[COCl₂] = 0.50 × 0.6 = 0.30 M", "K_c = (0.20 × 0.20)/0.30 = 0.133 mol L⁻¹"],
    why="0.533 uses moles instead of concentrations (ignores the 4.0 L). 0.267 uses α²/(1 − α) without the "
        "concentration. 0.080 forgets the (1 − α) term in the denominator.",
    ncert=f"{REF6}, calculating equilibrium concentrations", seconds=90, checked=True)

poh_buf = 4.75 + 0.087
assert close(14 - poh_buf, 9.16, 0.001) and close(14 - (4.75 - 0.087), 9.34, 0.001)
assert close((0.11 / 0.09), 10 ** 0.087, 0.002) and close(-math.log10(0.01), 2)
add("Hydrolysis and buffers", A, "numerical",
    "One litre of a buffer contains 0.10 mol NH₄OH and 0.10 mol NH₄Cl. 0.01 mol of HCl is added to it (volume "
    "change negligible). The pH of the solution becomes (pK_b of NH₄OH = 4.75, pK_w = 14, log (11/9) = 0.087):",
    Opts("B", "9.16", ["9.25", "9.34", "2.00"]),
    "Basic buffer: pOH = pK_b + log ([salt]/[base])",
    "The added H⁺ reacts with the base of the buffer: NH₄OH + H⁺ → NH₄⁺ + H₂O. The base falls by 0.01 mol and "
    "the salt rises by 0.01 mol.",
    ["After reaction: NH₄OH = 0.09 mol, NH₄⁺ = 0.11 mol", "pOH = 4.75 + log (0.11/0.09) = 4.75 + 0.087 = 4.837",
     "pH = 14 − 4.837 = 9.16"],
    why="9.25 is the pH before HCl is added. 9.34 puts the ratio upside down. 2.00 treats the HCl as if it "
        "were in pure water, ignoring the buffer.",
    ncert=f"{REF6}, buffer solutions", seconds=100, checked=True)

s = 0.0332 / 332
ksp = (2 * s) ** 2 * s
assert close(s, 1e-4) and close(ksp, 4e-12) and close(s ** 2, 1e-8) and close(s ** 3, 1e-12)
assert close(4 * 0.0332 ** 3, 1.46e-4, 0.005)
add("Solubility product", A, "numerical",
    "The solubility of silver chromate, Ag₂CrO₄, in water at 298 K is 0.0332 g L⁻¹. Its solubility product is "
    "(Ag = 108, Cr = 52, O = 16):",
    Opts("D", "4.0 × 10⁻¹²", ["1.0 × 10⁻⁸", "1.0 × 10⁻¹²", "1.46 × 10⁻⁴"]),
    "K_sp of an A₂B salt: K_sp = (2s)² s = 4s³",
    "Convert the solubility to mol L⁻¹ first. Each Ag₂CrO₄ gives two Ag⁺ and one CrO₄²⁻.",
    ["Molar mass = 2 × 108 + 52 + 4 × 16 = 332 g mol⁻¹", "s = 0.0332 / 332 = 1.0 × 10⁻⁴ mol L⁻¹",
     "[Ag⁺] = 2.0 × 10⁻⁴, [CrO₄²⁻] = 1.0 × 10⁻⁴", "K_sp = (2.0 × 10⁻⁴)² × 1.0 × 10⁻⁴ = 4.0 × 10⁻¹²"],
    why="1.0 × 10⁻⁸ uses s² (as for an AB salt). 1.0 × 10⁻¹² forgets that [Ag⁺] = 2s. 1.46 × 10⁻⁴ puts the "
        "solubility in g L⁻¹ into 4s³.",
    ncert=f"{REF6}, solubility product constant", seconds=80, checked=True)

add("Kp, Kc and Le Chatelier", A, "multi_statement",
    ms("Which of the following statements about a reaction at constant temperature are correct?",
       ["If Q_c > K_c, the reaction proceeds in the forward direction.",
        "ΔG° = −RT ln K.",
        "If Q_c < K_c, the net reaction proceeds in the forward direction.",
        "The equilibrium constant of an exothermic reaction increases with increase in temperature.",
        "A very large value of K (say above 10³) means that products predominate at equilibrium."]),
    multi("C", {"a": False, "b": True, "c": True, "d": False, "e": True},
          ["(a), (b) and (e) only", "(a), (c) and (d) only", "(b), (c), (d) and (e) only"]),
    "Reaction quotient, K and ΔG°",
    "If Q < K the reaction moves forward to make more products; if Q > K it moves backward. ΔG° = −RT ln K. "
    "For an exothermic reaction, raising the temperature lowers K. A large K means the equilibrium mixture is "
    "mostly products.",
    ["(a) False: Q > K → backward", "(b) True", "(c) True", "(d) False: K decreases", "(e) True"],
    why="Options containing (a) or (d) are wrong.",
    ncert=f"{REF6}, applications of equilibrium constants; relationship between K, Q and G", seconds=60)

h_total = (1e-8 + math.sqrt(1e-16 + 4e-14)) / 2
assert 6.9 < -math.log10(h_total) < 7.0
add("Acids, bases and pH", A, "assertion_reason",
    ar("The pH of a 1.0 × 10⁻⁸ M aqueous solution of HCl at 298 K is slightly less than 7, not 8.",
       "At such a low acid concentration, the H⁺ ions coming from the ionisation of water cannot be neglected."),
    AR_, "pH of a very dilute strong acid",
    "pH = −log (10⁻⁸) = 8 would make an acid solution basic, which is impossible. Water itself supplies about "
    "10⁻⁷ M H⁺, ten times more than the acid. Adding both (with the water equilibrium shifted slightly) gives "
    "[H⁺] ≈ 1.05 × 10⁻⁷ M and pH ≈ 6.98. R is true and is the reason for A.",
    ["Acid gives 10⁻⁸ M H⁺; water gives ~10⁻⁷ M H⁺", "Total [H⁺] ≈ 1.05 × 10⁻⁷ M → pH ≈ 6.98 < 7",
     "Both true; R explains A"],
    answer="A", ncert=f"{REF6}, ionisation constant of water; the pH scale", seconds=50)

# ==================================================================== 7. Redox Reactions and Electrochemistry
topic("Redox Reactions and Electrochemistry")
REF7R, REF7E = f"{C11}, 'Redox Reactions'", f"{C12}, 'Electrochemistry'"

x_mn = 0 - (2 * 1 + 4 * (-2))
assert x_mn == 6 and 0 - 4 * (-2) == 8
add("Oxidation number and balancing", B, "numerical",
    "The oxidation number of manganese in potassium manganate, K₂MnO₄, is:",
    Opts("B", "+6", ["+7", "+4", "+8"]),
    "Rules for oxidation numbers",
    "In a neutral compound the oxidation numbers add up to zero. K is +1 and O is −2 here.",
    ["2(+1) + x + 4(−2) = 0", "x = +6"],
    why="+7 is the oxidation number of Mn in KMnO₄ (permanganate). +4 is Mn in MnO₂. +8 forgets the two "
        "potassium atoms.",
    ncert=f"{REF7R}, oxidation number", seconds=25, checked=True)

add("Electrode potential and cells", B, "direct",
    "In the Daniell cell, Zn(s) | ZnSO₄(aq) || CuSO₄(aq) | Cu(s), the anode and its polarity are:",
    Opts("A", "Zinc electrode; negative", ["Zinc electrode; positive", "Copper electrode; negative",
                                           "Copper electrode; positive"]),
    "Electrodes of a galvanic cell",
    "Oxidation takes place at the anode. In the Daniell cell zinc is oxidised (Zn → Zn²⁺ + 2e⁻). The electrons "
    "left behind make the zinc electrode the negative terminal; copper is the positive cathode.",
    ["Zn → Zn²⁺ + 2e⁻ (oxidation) → anode", "Electrons accumulate on Zn → negative pole",
     "Cu²⁺ + 2e⁻ → Cu at the cathode (positive)"],
    why="In a galvanic cell the anode is negative; in electrolysis it is positive. Copper is the cathode here.",
    ncert=f"{REF7E}, galvanic cells", seconds=25)

add("Batteries and fuel cells", B, "statement_pair",
    sp("In the lead storage battery, the anode is lead and the cathode is a grid of lead packed with lead "
       "dioxide (PbO₂).",
       "In the hydrogen–oxygen fuel cell, hydrogen is oxidised at the anode."),
    SP_, "Lead storage battery and H₂–O₂ fuel cell",
    "The lead storage battery has a lead anode and a lead grid packed with PbO₂ as the cathode, in sulphuric "
    "acid: Statement I is true. In the fuel cell, H₂ gives up electrons at the anode "
    "(2H₂ + 4OH⁻ → 4H₂O + 4e⁻) and O₂ is reduced at the cathode: Statement II is true.",
    ["Lead battery: Pb anode, PbO₂ cathode → I true", "Fuel cell anode: H₂ oxidised → II true"],
    answer="A", ncert=f"{REF7E}, batteries; fuel cells", seconds=35)

add("Electrode potential and cells", B, "direct",
    "The electrode potential assigned to the standard hydrogen electrode is:",
    Opts("C", "Zero at all temperatures", ["Zero only at 298 K", "+1.00 V at 298 K", "−0.059 V at 298 K"]),
    "Standard hydrogen electrode as the reference",
    "Single electrode potentials cannot be measured alone. By convention the standard hydrogen electrode "
    "(Pt, H₂ at 1 bar, H⁺ at unit activity) is assigned a potential of zero at all temperatures, and other "
    "electrode potentials are measured against it.",
    ["SHE: Pt(s) | H₂(g, 1 bar) | H⁺(aq, 1 M)", "E° = 0 V by convention, at all temperatures"],
    why="The zero is a convention, not a measurement at 298 K, so it holds at every temperature. +1.00 V and "
        "−0.059 V are not the conventional value.",
    ncert=f"{REF7E}, measurement of electrode potential", seconds=20)

lhs = {"Mn": 2, "O": 2 * 4 + 5 * 4, "C": 10, "H": 16}
rhs = {"Mn": 2, "O": 10 * 2 + 8, "C": 10, "H": 8 * 2}
assert lhs == rhs and 2 * (-1) + 5 * (-2) + 16 * (+1) == 2 * (+2)
add("Oxidation number and balancing", I, "numerical",
    "When the equation MnO₄⁻ + C₂O₄²⁻ + H⁺ → Mn²⁺ + CO₂ + H₂O is balanced with the smallest whole-number "
    "coefficients, the coefficient of H⁺ is:",
    Opts("D", "16", ["8", "10", "5"]),
    "Balancing a redox equation (ion–electron or oxidation number method)",
    "Mn goes from +7 to +2 (gains 5e⁻); each C goes from +3 to +4, so one C₂O₄²⁻ loses 2e⁻. Equalise the "
    "electrons, then balance O with H₂O and H with H⁺.",
    ["Reduction: MnO₄⁻ + 8H⁺ + 5e⁻ → Mn²⁺ + 4H₂O (× 2)", "Oxidation: C₂O₄²⁻ → 2CO₂ + 2e⁻ (× 5)",
     "Sum: 2MnO₄⁻ + 5C₂O₄²⁻ + 16H⁺ → 2Mn²⁺ + 10CO₂ + 8H₂O",
     "Check charge: −2 − 10 + 16 = +4 = 2 × (+2)"],
    why="8 is the H⁺ of a single permanganate half-reaction (also the coefficient of H₂O). 10 is the "
        "coefficient of CO₂ and 5 that of C₂O₄²⁻.",
    ncert=f"{REF7R}, balancing of redox reactions", seconds=90, checked=True)

lam0 = 349.6 + 40.9
alpha = 39.05 / lam0
assert close(lam0, 390.5) and close(alpha, 0.100)
assert close(39.05 / 349.6, 0.112, 0.003) and close(39.05 / 40.9, 0.955, 0.002)
add("Conductance and Kohlrausch's law", I, "numerical",
    "The molar conductivity of a dilute acetic acid solution is 39.05 S cm² mol⁻¹. The limiting molar "
    "conductivities of H⁺ and CH₃COO⁻ are 349.6 and 40.9 S cm² mol⁻¹. The degree of dissociation of acetic acid "
    "in this solution is:",
    Opts("B", "0.100", ["0.112", "0.955", "10.0"]),
    "Kohlrausch's law and degree of dissociation: α = Λm / Λ°m",
    "Λ°m of acetic acid is the sum of the limiting molar conductivities of its two ions. The ratio Λm/Λ°m gives "
    "the fraction dissociated.",
    ["Λ°m(CH₃COOH) = 349.6 + 40.9 = 390.5 S cm² mol⁻¹", "α = 39.05 / 390.5 = 0.100"],
    why="0.112 divides by λ°(H⁺) alone. 0.955 divides by λ°(CH₃COO⁻) alone. 10.0 inverts the ratio.",
    ncert=f"{REF7E}, applications of Kohlrausch's law", seconds=45, checked=True)

e_conc = 0.059 * math.log10(0.001 / 0.1)
assert close(e_conc, -0.118)
add("Nernst equation and Gibbs energy", I, "assertion_reason",
    ar("The concentration cell Ag(s) | Ag⁺(0.1 M) || Ag⁺(0.001 M) | Ag(s), as written, has a positive emf at "
       "298 K.",
       "For a concentration cell made of two identical electrodes, E°cell = 0."),
    AR_, "Concentration cells and the Nernst equation",
    "For this cell the reaction is Ag⁺(0.001 M) → Ag⁺(0.1 M) and E = E° − 0.059 log (0.1/0.001) = "
    "0 − 0.059 × 2 = −0.118 V (2.303RT/F = 0.059 V). The emf as written is negative, because the dilute "
    "solution has been placed at the cathode. A is false. Both electrodes are the same, so E°cell = 0: R is "
    "true.",
    ["Cathode: Ag⁺(0.001 M) + e⁻ → Ag; anode: Ag → Ag⁺(0.1 M) + e⁻",
     "E = 0 − 0.059 log (0.1/0.001) = −0.118 V → A false", "E° = E°(Ag⁺/Ag) − E°(Ag⁺/Ag) = 0 → R true"],
    answer="D", ncert=f"{REF7E}, Nernst equation", seconds=60)

add("Electrode potential and cells", I, "assertion_reason",
    ar("Copper metal does not liberate hydrogen gas from dilute hydrochloric acid.",
       "Copper is a good conductor of electricity."),
    AR_, "Electrochemical series: displacement of hydrogen",
    "A metal liberates H₂ from dilute acid only if it is a stronger reducing agent than hydrogen, i.e. if its "
    "standard reduction potential is negative. E°(Cu²⁺/Cu) = +0.34 V, so copper cannot reduce H⁺: A is true. "
    "Copper is indeed a good conductor (R true), but electrical conductivity has nothing to do with whether a "
    "metal can reduce H⁺ ions, so R does not explain A.",
    ["E°(Cu²⁺/Cu) = +0.34 V > 0 → Cu cannot reduce H⁺ → A true",
     "R true, but conduction is a different property → not the explanation"],
    answer="B", ncert=f"{REF7E}, electrochemical series; {REF7R}, redox reactions and electrode processes",
    seconds=40)

add("Conductance and Kohlrausch's law", I, "match_list",
    lists("Match List-I (quantity) with List-II (SI unit).",
          ["Resistivity (ρ)", "Conductivity (κ)", "Molar conductivity (Λm)", "Cell constant (l/A)"],
          ["S m² mol⁻¹", "m⁻¹", "Ω m", "S m⁻¹"]),
    match("C", M("III IV I II"), [M("IV III I II"), M("III IV II I"), M("III I IV II")]),
    "Units of conductance quantities",
    "R = ρ l/A, so ρ = RA/l has the unit Ω m. κ = 1/ρ has the unit S m⁻¹. Λm = κ/c has the unit "
    "S m⁻¹ / mol m⁻³ = S m² mol⁻¹. The cell constant l/A has the unit m⁻¹.",
    ["ρ → Ω m → III", "κ → S m⁻¹ → IV", "Λm → S m² mol⁻¹ → I", "l/A → m⁻¹ → II"],
    why="The other codes swap resistivity with conductivity, molar conductivity with cell constant, or "
        "conductivity with molar conductivity.",
    ncert=f"{REF7E}, measurement of the conductivity of ionic solutions", seconds=40)

assert F(8, 3) == F(0 - 4 * (-2), 3)
add("Oxidation number and balancing", I, "multi_statement",
    ms("Which of the following statements are correct?",
       ["In the reaction Zn(s) + Cu²⁺(aq) → Zn²⁺(aq) + Cu(s), zinc acts as the reducing agent.",
        "In MnO₂ + 4HCl → MnCl₂ + Cl₂ + 2H₂O, HCl acts only as an oxidising agent.",
        "Oxidation is an increase in the oxidation number of an element.",
        "The average oxidation number of iron in Fe₃O₄ is +8/3.",
        "An oxidising agent is itself oxidised in a redox reaction."]),
    multi("B", {"a": True, "b": False, "c": True, "d": True, "e": False},
          ["(a), (b) and (c) only", "(c), (d) and (e) only", "(a), (b), (c) and (d) only"]),
    "Oxidation number, oxidising and reducing agents",
    "Zn loses electrons (0 → +2), so it is the reducing agent. In MnO₂ + HCl, part of the chloride is oxidised "
    "to Cl₂ (−1 → 0): HCl is the reducing agent there, not an oxidising agent. In Fe₃O₄, 3x + 4(−2) = 0 gives "
    "x = +8/3. An oxidising agent gains electrons and is itself reduced.",
    ["(a) True", "(b) False: HCl is oxidised (it is the reducing agent)", "(c) True", "(d) True",
     "(e) False: an oxidising agent is reduced"],
    why="Options containing (b) or (e) are wrong.",
    ncert=f"{REF7R}, classical idea of redox reactions; oxidation number", seconds=60)

e_cell = (0.80 - (-0.25)) - 0.059 / 2 * math.log10(0.01 / 0.1 ** 2)
dG = -2 * 96500 * e_cell / 1000
assert close(e_cell, 1.05) and close(dG, -202.7, 0.001)
e_bad = 1.05 - 0.059 / 2 * math.log10(0.01 / 0.1)
assert close(-1 * 96500 * 1.05 / 1000, -101.3, 0.001) and close(-2 * 96500 * e_bad / 1000, -208.3, 0.001)
add("Nernst equation and Gibbs energy", A, "numerical",
    "For the cell Ni(s) | Ni²⁺(0.01 M) || Ag⁺(0.1 M) | Ag(s) at 298 K, the cell reaction is "
    "Ni(s) + 2Ag⁺(aq) → Ni²⁺(aq) + 2Ag(s). The Gibbs energy change of this reaction under these conditions is "
    "(E°(Ag⁺/Ag) = +0.80 V, E°(Ni²⁺/Ni) = −0.25 V, 2.303RT/F = 0.059 V, F = 96 500 C mol⁻¹):",
    Opts("D", "−202.7 kJ mol⁻¹", ["−101.3 kJ mol⁻¹", "−208.3 kJ mol⁻¹", "+202.7 kJ mol⁻¹"]),
    "Nernst equation and ΔG = −nFE",
    "Find E°cell, then correct it with the Nernst equation using Q = [Ni²⁺]/[Ag⁺]² (the square comes from the "
    "coefficient 2), and finally ΔG = −nFE with n = 2.",
    ["E°cell = 0.80 − (−0.25) = 1.05 V", "Q = 0.01 / (0.1)² = 1 → log Q = 0",
     "E = 1.05 − (0.059/2) × 0 = 1.05 V", "ΔG = −2 × 96 500 × 1.05 = −202 650 J ≈ −202.7 kJ mol⁻¹"],
    why="−101.3 uses n = 1. −208.3 forgets to square [Ag⁺] (takes Q = 0.1, E = 1.0795 V). +202.7 has the wrong "
        "sign for a cell with positive emf.",
    ncert=f"{REF7E}, Nernst equation; electrochemical cell and Gibbs energy of the reaction", seconds=120,
    checked=True)

x_s = (0 - (2 * 1 + 6 * (-2) + 2 * (-1))) / 2
assert x_s == 6
assert (0 - (2 * 1 + 8 * (-2))) / 2 == 7 and 2 * x_s == 12 and (0 - (2 * 1 + 6 * (-2))) / 2 == 5
add("Oxidation number and balancing", A, "numerical",
    "In peroxodisulphuric acid, H₂S₂O₈, the two sulphur atoms are linked through one peroxide (–O–O–) "
    "bridge; the other six oxygen atoms are ordinary (oxide-type) oxygens. The oxidation number of each "
    "sulphur atom is:",
    Opts("A", "+6", ["+7", "+12", "+5"]),
    "Oxidation number when peroxide oxygen is present",
    "Peroxide oxygens have oxidation number −1, the other oxygens −2, hydrogen +1. The molecule is neutral.",
    ["2(+1) + 2x + 6(−2) + 2(−1) = 0", "2x = 12 → x = +6"],
    why="+7 treats all eight oxygens as −2 (an oxidation number above the group maximum of +6). +12 is the "
        "total for both sulphur atoms. +5 counts the peroxide oxygens as 0.",
    ncert=f"{REF7R}, oxidation number", seconds=60, checked=True)

add("Electrode potential and cells", A, "statement_pair",
    sp("For the Daniell cell Zn | Zn²⁺ || Cu²⁺ | Cu, increasing the concentration of Zn²⁺ increases the emf of "
       "the cell.",
       "The standard emf of a cell doubles when its cell reaction is multiplied by 2."),
    SP_, "Nernst equation and the intensive nature of emf",
    "E = E° − (0.059/2) log ([Zn²⁺]/[Cu²⁺]). Raising [Zn²⁺] raises log Q and lowers E: Statement I is false. "
    "E° is an intensive property; multiplying the equation by 2 doubles n and ΔG° but leaves E° unchanged: "
    "Statement II is false.",
    ["Higher [Zn²⁺] → larger Q → smaller E → I false", "E° intensive; ΔG° = −nFE° doubles → II false"],
    answer="B", ncert=f"{REF7E}, Nernst equation; electrochemical cell and Gibbs energy", seconds=50)

add("Conductance and Kohlrausch's law", A, "multi_statement",
    ms("Which of the following statements about conductance are correct?",
       ["Metallic (electronic) conduction is due to the movement of ions.",
        "For a strong electrolyte, Λm = Λ°m − A√c, where A is a constant.",
        "The molar conductivity of a strong electrolyte decreases on dilution.",
        "The constant A in Λm = Λ°m − A√c has the same value for all electrolytes of a given type (for example "
        "NaCl and KCl) in a given solvent at a given temperature.",
        "Λ°m of an electrolyte equals the sum of the limiting molar conductivities of its cation and anion, each "
        "multiplied by the number of such ions in its formula."]),
    multi("C", {"a": False, "b": True, "c": False, "d": True, "e": True},
          ["(a), (b) and (d) only", "(b), (c) and (e) only", "(a), (c), (d) and (e) only"]),
    "Variation of molar conductivity with concentration; Kohlrausch's law",
    "Metals conduct by moving electrons. For strong electrolytes Λm rises slowly on dilution, following "
    "Λm = Λ°m − A√c; A depends on the type of electrolyte (1-1, 2-1, 2-2 …), so NaCl and KCl share the same A. "
    "Kohlrausch's law: Λ°m = ν₊λ°₊ + ν₋λ°₋.",
    ["(a) False: electrons carry the current in metals", "(b) True", "(c) False: Λm increases on dilution",
     "(d) True", "(e) True"],
    why="Options containing (a) or (c) are wrong.",
    ncert=f"{REF7E}, variation of conductivity and molar conductivity with concentration; Kohlrausch's law",
    seconds=70)

# ==================================================================== 8. Chemical Kinetics
topic("Chemical Kinetics")
REF8 = f"{C12}, 'Chemical Kinetics'"

add("Rate law and order", B, "direct",
    "The rate of a reaction is found to be proportional to the square of the concentration of its only "
    "reactant. In which unit is its rate constant expressed?",
    Opts("C", "L mol⁻¹ s⁻¹", ["mol L⁻¹ s⁻¹", "s⁻¹", "L² mol⁻² s⁻¹"]),
    "Units of rate constant: (mol L⁻¹)¹⁻ⁿ s⁻¹",
    "Rate (mol L⁻¹ s⁻¹) = k (mol L⁻¹)². So k = (mol L⁻¹ s⁻¹)/(mol L⁻¹)² = L mol⁻¹ s⁻¹.",
    ["n = 2: k = (mol L⁻¹)¹⁻² s⁻¹ = mol⁻¹ L s⁻¹"],
    why="mol L⁻¹ s⁻¹ is for a zero-order reaction, s⁻¹ for first order and L² mol⁻² s⁻¹ for third order.",
    ncert=f"{REF8}, units of rate constant", seconds=25)

t_half0 = 0.5 / (2 * 0.01)
assert close(t_half0, 25) and close(0.5 / 0.01, 50) and close(0.693 / 0.01, 69.3)
add("Half-life", B, "numerical",
    "A zero-order reaction has a rate constant of 0.01 mol L⁻¹ s⁻¹. If the initial concentration of the "
    "reactant is 0.5 mol L⁻¹, the half-life of the reaction is:",
    Opts("B", "25 s", ["50 s", "69.3 s", "12.5 s"]),
    "Half-life of a zero-order reaction: t½ = [R]₀ / 2k",
    "For a zero-order reaction [R] = [R]₀ − kt; half of [R]₀ is used up when kt = [R]₀/2.",
    ["t½ = 0.5 / (2 × 0.01)", "t½ = 25 s"],
    why="50 s is the time for the reaction to go to completion ([R]₀/k). 69.3 s applies the first-order formula "
        "0.693/k. 12.5 s divides by 4k.",
    ncert=f"{REF8}, half-life of a reaction", seconds=30, checked=True)

add("Arrhenius equation and activation energy", B, "statement_pair",
    sp("According to collision theory, every collision between reactant molecules leads to the formation of "
       "products.",
       "For a collision to be effective, the colliding molecules must have at least a threshold energy and the "
       "proper orientation."),
    SP_, "Collision theory of chemical reactions",
    "Only a small fraction of collisions, the effective collisions, produce products: Statement I is false. "
    "Effective collisions need energy at least equal to the threshold energy and a proper orientation of the "
    "molecules: Statement II is true.",
    ["Most collisions are not effective → I false", "Energy ≥ threshold and correct orientation → II true"],
    answer="D", ncert=f"{REF8}, collision theory of chemical reactions", seconds=35)

k1 = 0.693 / 5
t999 = 2.303 * 3 / k1
assert close(t999, 50, 0.005)
assert close(2.303 * 3 / (1 / 5), 34.5, 0.002) and close(3 / k1, 21.6, 0.005)
add("Zero and first order reactions", I, "numerical",
    "The half-life of a first-order reaction is 5.0 min. The time needed for 99.9% of the reactant to react is "
    "approximately (ln 2 = 0.693, 2.303 log 1000 = 6.909):",
    Opts("D", "50 min", ["15 min", "34.5 min", "21.6 min"]),
    "Integrated first-order rate equation: t = (2.303/k) log ([R]₀/[R])",
    "For 99.9% completion, [R]₀/[R] = 100/0.1 = 1000. Find k from the half-life.",
    ["k = 0.693 / 5.0 = 0.1386 min⁻¹", "t = 6.909 / 0.1386 = 49.9 min ≈ 50 min"],
    shortcut="t(99.9%) / t½ = (2.303 × 3)/0.693 ≈ 10, so t ≈ 10 × 5 = 50 min.",
    why="15 min assumes 99.9% needs three half-lives (it needs about ten). 34.5 min takes k = 1/t½, leaving "
        "out 0.693. 21.6 min uses log instead of ln (leaves out 2.303).",
    ncert=f"{REF8}, first order reactions; half-life", seconds=60, checked=True)

ratio = F(1, 2) ** 2 * 2
assert ratio == F(1, 2)
add("Rate law and order", I, "numerical",
    "The rate law for a reaction is rate = k[A]²[B]. If the concentration of A is halved and that of B is "
    "doubled, the rate of the reaction becomes:",
    Opts("A", "Half of the original rate", ["Double the original rate", "Equal to the original rate",
                                            "One-fourth of the original rate"]),
    "Using a rate law",
    "Substitute the new concentrations into the rate law and compare with the old rate.",
    ["New rate = k(½[A])²(2[B])", "= k × ¼ × 2 × [A]²[B]", "= ½ × original rate"],
    why="'Double' ignores the square on [A]. 'Equal' treats both changes as cancelling. 'One-fourth' ignores the "
        "doubling of [B].",
    ncert=f"{REF8}, rate expression and rate constant", seconds=35, checked=True)

add("Rate law and order", I, "multi_statement",
    ms("Which of the following statements are correct?",
       ["Molecularity is defined only for elementary reactions.",
        "For a complex reaction, the overall rate is decided by its slowest step.",
        "The order of a reaction can always be found from its balanced chemical equation.",
        "The rate of a zero-order reaction decreases as the reaction proceeds.",
        "The decomposition of gaseous ammonia on a hot platinum surface at high pressure is a zero-order "
        "reaction."]),
    multi("A", {"a": True, "b": True, "c": False, "d": False, "e": True},
          ["(a), (b) and (c) only", "(b), (d) and (e) only", "(a), (c), (d) and (e) only"]),
    "Order, molecularity and rate-determining step",
    "Molecularity has meaning only for an elementary step. The slowest step of a mechanism determines the "
    "rate. Order is found by experiment, not from the stoichiometric equation. The rate of a zero-order "
    "reaction equals k and stays constant until the reactant is used up. On hot Pt at high pressure the "
    "surface is saturated with NH₃, so the rate is independent of its concentration.",
    ["(a) True", "(b) True: rate-determining step", "(c) False: order is experimental",
     "(d) False: rate = k is constant", "(e) True"],
    why="Options containing (c) or (d) are wrong.",
    ncert=f"{REF8}, molecularity of a reaction; zero order reactions", seconds=60)

add("Rate law and order", I, "match_list",
    lists("Match List-I (reaction, with its experimentally found rate law) with List-II (overall order).",
          ["H₂(g) + Cl₂(g) → 2HCl(g) in light; rate = k",
           "2N₂O₅(g) → 4NO₂(g) + O₂(g); rate = k[N₂O₅]",
           "CHCl₃ + Cl₂ → CCl₄ + HCl; rate = k[CHCl₃][Cl₂]^½",
           "2NO(g) + O₂(g) → 2NO₂(g); rate = k[NO]²[O₂]"],
          ["3/2", "3", "0", "1"]),
    match("C", M("III IV I II"), [M("IV III I II"), M("III IV II I"), M("III I IV II")]),
    "Order from the rate law",
    "The overall order is the sum of the powers of the concentration terms in the experimental rate law, "
    "whatever the stoichiometric coefficients are.",
    ["rate = k → 0 → III", "k[N₂O₅] → 1 → IV", "k[CHCl₃][Cl₂]^½ → 1 + ½ = 3/2 → I", "k[NO]²[O₂] → 3 → II"],
    why="Reading the order from the coefficients (2 for N₂O₅, 2 for H₂ + Cl₂) gives the wrong codes.",
    ncert=f"{REF8}, order of a reaction", seconds=45)

ea = 6 * 5.74
k_arr = 1e11 * 10 ** (-ea / 5.74)
t_half = 0.693 / k_arr
assert close(k_arr, 1e5) and close(t_half, 6.93e-6)
assert close(0.693 / 1e11, 6.93e-12) and close(1 / k_arr, 1.0e-5) and close(0.301 / k_arr, 3.01e-6)
add("Arrhenius equation and activation energy", A, "numerical",
    "A first-order reaction has activation energy 34.44 kJ mol⁻¹ and pre-exponential factor 1.0 × 10¹¹ s⁻¹. "
    "Using the Arrhenius equation, its half-life at 300 K is (2.303RT = 5.74 kJ mol⁻¹ at 300 K; "
    "ln 2 = 0.693):",
    Opts("D", "6.93 × 10⁻⁶ s", ["6.93 × 10⁻¹² s", "1.0 × 10⁻⁵ s", "3.01 × 10⁻⁶ s"]),
    "Arrhenius equation k = A e^(−Ea/RT) combined with t½ = 0.693/k",
    "Write the exponential factor as a power of ten: e^(−Ea/RT) = 10^(−Ea/2.303RT).",
    ["Ea / 2.303RT = 34.44 / 5.74 = 6", "k = 1.0 × 10¹¹ × 10⁻⁶ = 1.0 × 10⁵ s⁻¹",
     "t½ = 0.693 / 1.0 × 10⁵ = 6.93 × 10⁻⁶ s"],
    why="6.93 × 10⁻¹² s takes k = A and ignores the activation energy. 1.0 × 10⁻⁵ s is 1/k, without 0.693. "
        "3.01 × 10⁻⁶ s uses log 2 (0.301) instead of ln 2.",
    ncert=f"{REF8}, temperature dependence of the rate of a reaction (Arrhenius equation)", seconds=90,
    checked=True)

p0, pt = 0.4, 0.7
pa = 2 * p0 - pt
kk = 2.303 / 100 * math.log10(p0 / pa)
assert close(pa, 0.1) and close(kk, 1.39e-2, 0.003)
assert close(2.303 / 100 * math.log10(p0 / (pt - p0)), 2.88e-3, 0.003)
assert close(2.303 / 100 * math.log10(pt / p0), 5.60e-3, 0.003)
add("Zero and first order reactions", A, "numerical",
    "The gas-phase reaction A(g) → B(g) + C(g) is first order. It is started with pure A at a pressure of "
    "0.4 atm in a closed vessel at constant volume and temperature. After 100 s the total pressure is 0.7 atm. "
    "The rate constant is (log 2 = 0.301):",
    Opts("B", "1.39 × 10⁻² s⁻¹", ["2.88 × 10⁻³ s⁻¹", "6.93 × 10⁻³ s⁻¹", "5.60 × 10⁻³ s⁻¹"]),
    "First-order kinetics from total pressure: k = (2.303/t) log (p₀/p_A)",
    "If x atm of A reacts, p_A = p₀ − x and the total pressure is p₀ + x. So p_A = 2p₀ − p_t.",
    ["x = 0.7 − 0.4 = 0.3 atm", "p_A = 0.4 − 0.3 = 0.1 atm", "k = (2.303/100) log (0.4/0.1) = "
     "(2.303/100) × 0.602 = 1.39 × 10⁻² s⁻¹"],
    shortcut="p_A falls from 0.4 to 0.1 atm, i.e. to one-quarter: two half-lives in 100 s, so t½ = 50 s and "
             "k = 0.693/50 = 1.39 × 10⁻² s⁻¹.",
    why="2.88 × 10⁻³ s⁻¹ takes p_A as x (0.3 atm). 6.93 × 10⁻³ s⁻¹ assumes only half of A has reacted. "
        "5.60 × 10⁻³ s⁻¹ uses p_t/p₀ instead of p₀/p_A.",
    ncert=f"{REF8}, first order gas phase reaction", seconds=120, checked=True)

add("Arrhenius equation and activation energy", A, "assertion_reason",
    ar("The rate constant of a reaction with a high activation energy changes more for a given rise in "
       "temperature than that of a reaction with a low activation energy.",
       "A plot of ln k against 1/T is a straight line of slope −Ea/R, so the larger Ea is, the steeper the "
       "line."),
    AR_, "Temperature sensitivity and the Arrhenius plot",
    "From ln k = ln A − Ea/RT, the change in ln k for a given change in 1/T is proportional to Ea. A steeper "
    "line (larger Ea) therefore means a larger change in k for the same rise in temperature. Both statements "
    "are true and R explains A.",
    ["ln k = ln A − (Ea/R)(1/T) → slope = −Ea/R (R true)", "Δ ln k = −(Ea/R) Δ(1/T) → larger Ea, larger change "
     "(A true)"],
    answer="A", ncert=f"{REF8}, temperature dependence of the rate of a reaction", seconds=50)

# ==================================================================== 9. Classification of Elements and Periodicity
topic("Classification of Elements and Periodicity in Properties")
REF9 = f"{C11}, 'Classification of Elements and Periodicity in Properties'"

add("Modern periodic table", B, "direct",
    "According to the modern periodic law, the physical and chemical properties of the elements are periodic "
    "functions of their:",
    Opts("B", "Atomic numbers", ["Atomic masses", "Numbers of neutrons", "Densities"]),
    "Modern periodic law",
    "Moseley showed that atomic number, not atomic mass, is the more fundamental property of an element. The "
    "modern periodic law therefore states that properties are periodic functions of atomic number.",
    ["Mendeleev: atomic mass", "Modern law (after Moseley): atomic number"],
    why="Atomic mass was the basis of Mendeleev's law. Neutron number and density do not order the elements.",
    ncert=f"{REF9}, modern periodic law and the present form of the periodic table", seconds=20)

add("Atomic and ionic radii", B, "direct",
    "Which of the following species has the largest radius?",
    Opts("D", "Na", ["Na⁺", "Mg", "Mg²⁺"]),
    "Atomic radius across a period and the size of cations",
    "Na and Mg are in the same period; Na has the smaller nuclear charge, so it is larger. A cation is "
    "smaller than its parent atom because it has fewer electrons held by the same nuclear charge (and Na⁺ "
    "loses its whole outer shell).",
    ["Na > Mg (radius decreases across a period)", "Na > Na⁺ and Mg > Mg²⁺ (cation smaller than atom)"],
    why="Na⁺ and Mg²⁺ have lost their 3s electrons and are much smaller. Mg is smaller than Na.",
    ncert=f"{REF9}, atomic radius; ionic radius", seconds=20)

add("Modern periodic table", B, "statement_pair",
    sp("The fourth period of the periodic table contains 18 elements.",
       "Metallic character decreases on going down a group."),
    SP_, "Periods and the trend of metallic character",
    "The fourth period fills 4s, 3d and 4p (2 + 10 + 6 = 18 elements, K to Kr): Statement I is true. Down a "
    "group the atoms get larger and lose electrons more easily, so metallic character increases (for example "
    "C and Si are non-metals while Sn and Pb are metals): Statement II is false.",
    ["Period 4: 4s² + 3d¹⁰ + 4p⁶ → 18 elements → I true", "Metallic character increases down a group → II false"],
    answer="C", ncert=f"{REF9}, electronic configurations and types of elements; periodic trends", seconds=35)

ie = [738, 1451, 7733]
jumps = [ie[i + 1] / ie[i] for i in range(2)]
assert jumps.index(max(jumps)) == 1
add("Ionisation and electron gain enthalpy", I, "direct",
    "The first three ionisation enthalpies of an element are 738, 1451 and 7733 kJ mol⁻¹. The element most "
    "likely belongs to:",
    Opts("C", "Group 2", ["Group 1", "Group 13", "Group 14"]),
    "Successive ionisation enthalpies and valence electrons",
    "Successive ionisation enthalpies rise gradually while valence electrons are removed and jump sharply "
    "when an electron must be taken from the noble-gas core. Here the big jump comes after the second "
    "electron (1451 → 7733), so the atom has two valence electrons.",
    ["ΔiH₂/ΔiH₁ ≈ 2; ΔiH₃/ΔiH₂ ≈ 5.3 → jump after 2 electrons", "Two valence electrons → group 2"],
    why="A group 1 element would show the jump after the first electron; group 13 and 14 elements only after "
        "the third and fourth.",
    ncert=f"{REF9}, ionization enthalpy", seconds=45)

add("Ionisation and electron gain enthalpy", I, "assertion_reason",
    ar("The second electron gain enthalpy of oxygen (O⁻ → O²⁻) is positive.",
       "The negative charge of the O⁻ ion attracts the incoming electron strongly."),
    AR_, "Successive electron gain enthalpies",
    "When an electron is added to O⁻, it is repelled by the negative charge already on the ion, so energy "
    "must be supplied: the second electron gain enthalpy of oxygen is positive (A true). R is false: a "
    "negative ion repels, not attracts, an incoming electron.",
    ["O⁻ + e⁻ → O²⁻ needs energy (repulsion) → A true", "Negative ion repels the electron → R false"],
    answer="C", ncert=f"{REF9}, electron gain enthalpy", seconds=40)

add("Valence and reactivity", I, "multi_statement",
    ms("Which of the following statements are correct?",
       ["The reactivity of the halogens increases down group 17.",
        "The elements of group 1 show a valence of 1.",
        "The reactivity of the alkali metals increases down group 1.",
        "The elements of group 2 commonly show a valence of 3.",
        "The oxides of elements on the extreme left of a period are basic."]),
    multi("A", {"a": False, "b": True, "c": True, "d": False, "e": True},
          ["(a), (b) and (c) only", "(b), (d) and (e) only", "(a), (c), (d) and (e) only"]),
    "Periodic trends in valence and chemical reactivity",
    "Halogens react by gaining an electron; this becomes harder down the group, so reactivity decreases. "
    "Alkali metals react by losing an electron, which becomes easier down the group. Group 1 shows valence 1 "
    "and group 2 valence 2. Elements on the left form basic oxides (Na₂O), those on the right acidic oxides "
    "(Cl₂O₇).",
    ["(a) False: decreases (F most reactive)", "(b) True", "(c) True", "(d) False: valence 2",
     "(e) True"],
    why="Options containing (a) or (d) are wrong.",
    ncert=f"{REF9}, periodic trends in chemical properties", seconds=55)

add("Valence and reactivity", I, "match_list",
    lists("Match List-I (oxide) with List-II (its nature).",
          ["Na₂O", "Cl₂O₇", "As₂O₃", "N₂O"],
          ["Neutral", "Amphoteric", "Strongly basic", "Strongly acidic"]),
    match("B", M("III IV II I"), [M("IV III II I"), M("III IV I II"), M("II IV III I")]),
    "Nature of oxides across a period",
    "Oxides of elements on the extreme left are the most basic (Na₂O) and those on the extreme right the most "
    "acidic (Cl₂O₇). Oxides of elements in the centre are amphoteric (Al₂O₃, As₂O₃) or neutral (CO, NO, N₂O).",
    ["Na₂O → strongly basic → III", "Cl₂O₇ → strongly acidic → IV", "As₂O₃ → amphoteric → II",
     "N₂O → neutral → I"],
    why="The other codes swap basic with acidic, amphoteric with neutral, or Na₂O with As₂O₃.",
    ncert=f"{REF9}, periodic trends in chemical properties: nature of oxides", seconds=40)

add("Ionisation and electron gain enthalpy", A, "multi_statement",
    ms("Which of the following comparisons are correct?",
       ["Electronegativity: F > O > N",
        "Atomic radius: F > Cl",
        "Ionic radius: Al³⁺ > Mg²⁺",
        "Electron gain enthalpy: S is more negative than O",
        "First ionisation enthalpy: Li > Na"]),
    multi("D", {"a": True, "b": False, "c": False, "d": True, "e": True},
          ["(a), (b) and (d) only", "(b), (c) and (e) only", "(a), (c), (d) and (e) only"]),
    "Periodic trends: electronegativity, radii, electron gain and ionisation enthalpy",
    "Electronegativity increases across period 2 (N < O < F). Radius increases down a group (F < Cl). For the "
    "isoelectronic Mg²⁺ and Al³⁺, the higher nuclear charge makes Al³⁺ smaller. The added electron in O enters "
    "the small, crowded n = 2 shell and is repelled more, so S has the more negative electron gain enthalpy. "
    "Ionisation enthalpy decreases down a group (Li > Na).",
    ["(a) True", "(b) False: F < Cl", "(c) False: Al³⁺ < Mg²⁺", "(d) True: S ≈ −200, O ≈ −141 kJ mol⁻¹",
     "(e) True"],
    why="Options with (b) or (c) are wrong.",
    ncert=f"{REF9}, periodic trends in physical properties", seconds=75)

add("Atomic and ionic radii", A, "assertion_reason",
    ar("The ionic radius of Fe³⁺ is smaller than that of Fe²⁺.",
       "The Fe³⁺ ion has a higher nuclear charge than the Fe²⁺ ion."),
    AR_, "Radii of ions of the same element",
    "Fe²⁺ and Fe³⁺ both have 26 protons, so their nuclear charge is the same: R is false. Fe³⁺ has one electron "
    "fewer, so the same nuclear charge pulls on fewer electrons, the effective nuclear charge per electron is "
    "greater and the ion is smaller: A is true.",
    ["Both ions: Z = 26 → same nuclear charge → R false",
     "Fe³⁺ (23 e⁻) vs Fe²⁺ (24 e⁻): fewer electrons → greater pull per electron → smaller → A true"],
    answer="C", ncert=f"{REF9}, ionic radius", seconds=45)

add("Ionisation and electron gain enthalpy", A, "statement_pair",
    sp("Electronegativity is a measurable quantity with a fixed value for each element, like ionisation "
       "enthalpy.",
       "On the Pauling scale, fluorine is assigned an electronegativity of 4.0."),
    SP_, "Electronegativity",
    "Unlike ionisation enthalpy and electron gain enthalpy, electronegativity is not a measurable quantity; it "
    "is a relative tendency of an atom in a compound and is not strictly constant for an element: Statement I "
    "is false. Pauling arbitrarily assigned fluorine, the most electronegative element, a value of 4.0: "
    "Statement II is true.",
    ["Electronegativity is not directly measurable → I false", "Pauling scale: F = 4.0 → II true"],
    answer="D", ncert=f"{REF9}, electronegativity", seconds=40)

# ==================================================================== 10. p-Block Elements
topic("p-Block Elements")
REF10A = "Class 11 Chemistry (pre-2023 edition), 'The p-Block Elements'"
REF10B = "Class 12 Chemistry (pre-2023 edition), 'The p-Block Elements'"

add("Group 13 and 14 trends", B, "direct",
    "Which element of group 13 is a typical non-metal?",
    Opts("C", "Boron", ["Aluminium", "Gallium", "Indium"]),
    "Metallic character in group 13",
    "Boron is a non-metal: it is extremely hard, black and has a very high melting point. Aluminium, gallium, "
    "indium and thallium are metals.",
    ["B → non-metal", "Al, Ga, In, Tl → metals"],
    why="Aluminium, gallium and indium are all metals.",
    ncert=f"{REF10A}, group 13 elements: physical properties", seconds=20)

add("Group 17 and 18 trends", B, "match_list",
    lists("Match List-I (halogen) with List-II (its colour).",
          ["F₂", "Cl₂", "Br₂", "I₂"], ["Violet", "Greenish yellow", "Yellow", "Red"]),
    match("D", M("III II IV I"), [M("II III IV I"), M("III II I IV"), M("III IV II I")]),
    "Colour of the halogens",
    "All halogens are coloured because they absorb visible light and excite outer electrons. The colour "
    "deepens down the group: fluorine is yellow, chlorine greenish yellow, bromine red and iodine violet.",
    ["F₂ → yellow → III", "Cl₂ → greenish yellow → II", "Br₂ → red → IV", "I₂ → violet → I"],
    why="The other codes swap F₂ with Cl₂, Br₂ with I₂, or Cl₂ with Br₂.",
    ncert=f"{REF10B}, group 17 elements: physical properties", seconds=30)

add("Group 17 and 18 trends", B, "direct",
    "Which of the following halogens is a liquid at room temperature?",
    Opts("A", "Bromine", ["Chlorine", "Iodine", "Fluorine"]),
    "Physical state of the halogens",
    "The van der Waals forces between halogen molecules grow with size. Fluorine and chlorine are gases, "
    "bromine is a liquid and iodine is a solid at room temperature.",
    ["F₂, Cl₂ → gases", "Br₂ → liquid", "I₂ → solid"],
    why="Chlorine and fluorine are gases and iodine is a solid.",
    ncert=f"{REF10B}, group 17 elements: physical properties", seconds=20)

add("Anomalous first element", B, "statement_pair",
    sp("Oxygen shows a maximum covalency of four.",
       "Oxygen exists as a diatomic molecule, whereas sulphur exists as a polyatomic S₈ molecule."),
    SP_, "Anomalous behaviour of oxygen",
    "Oxygen has no d orbitals in its valence shell, so its covalency is limited to four, while sulphur and "
    "the heavier members can exceed it: Statement I is true. Oxygen forms pπ–pπ double bonds and exists as "
    "O₂, while sulphur forms rings of single bonds (S₈): Statement II is true.",
    ["No d orbitals → maximum covalency 4 → I true", "O₂ (O=O) vs S₈ (S–S rings) → II true"],
    answer="A", ncert=f"{REF10B}, group 16 elements: anomalous behaviour of oxygen; elemental state", seconds=35)

add("Group 13 and 14 trends", I, "assertion_reason",
    ar("Boron readily forms B³⁺ ions in its compounds.",
       "The sum of the first three ionisation enthalpies of boron is very high."),
    AR_, "Covalent nature of boron compounds",
    "Because boron is very small, the sum of its first three ionisation enthalpies is very high (R true). This "
    "prevents it from losing three electrons, so boron does not form B³⁺ ions; it forms covalent compounds "
    "instead. A is false.",
    ["ΔiH₁ + ΔiH₂ + ΔiH₃ of B is very high → R true", "So B³⁺ is not formed; boron is covalent → A false"],
    answer="D", ncert=f"{REF10A}, group 13 elements: chemical properties (oxidation state)", seconds=40)

add("Group 13 and 14 trends", I, "multi_statement",
    ms("Which of the following statements about group 14 elements are correct?",
       ["All the elements of group 14 are metals.",
        "SiCl₄ is hydrolysed by water, whereas CCl₄ is not.",
        "The common oxidation states of group 14 elements are +4 and +2.",
        "Tin is a non-metal.",
        "Carbon has the highest first ionisation enthalpy in group 14."]),
    multi("B", {"a": False, "b": True, "c": True, "d": False, "e": True},
          ["(a), (b) and (c) only", "(b), (d) and (e) only", "(a), (c), (d) and (e) only"]),
    "Trends in group 14",
    "Carbon is a typical non-metal and germanium a metalloid, while tin and lead are metals. Silicon can accept a lone pair from water into its d orbitals, so SiCl₄ is hydrolysed; "
    "carbon has no d orbitals and CCl₄ is not. The group shows +4 and +2. Ionisation enthalpy is highest for "
    "carbon, the smallest atom.",
    ["(a) False: C is a non-metal", "(b) True", "(c) True", "(d) False: Sn is a metal", "(e) True"],
    why="Options containing (a) or (d) are wrong.",
    ncert=f"{REF10A}, group 14 elements: trends in properties", seconds=60)

add("Group 15 and 16 trends", I, "direct",
    "Among the oxides of group 15 elements in the +3 oxidation state, the most basic is:",
    Opts("D", "Bi₂O₃", ["N₂O₃", "P₄O₆", "As₄O₆"]),
    "Acid–base character of group 15 oxides",
    "For oxides in the same oxidation state, acidic character decreases down the group as the elements "
    "become more metallic. The +3 oxides of N and P are acidic, those of As and Sb amphoteric, and that of Bi "
    "predominantly basic.",
    ["N₂O₃, P₄O₆ → acidic", "As₄O₆, Sb₄O₆ → amphoteric", "Bi₂O₃ → basic"],
    why="N₂O₃ and P₄O₆ are acidic, and As₄O₆ is amphoteric.",
    ncert=f"{REF10B}, group 15 elements: chemical properties (oxides)", seconds=30)

add("Group 17 and 18 trends", I, "statement_pair",
    sp("Among the hydrogen halides, H–F has the highest bond dissociation enthalpy.",
       "The thermal stability of the hydrogen halides increases from HF to HI."),
    SP_, "Hydrogen halides: bond strength and stability",
    "The small F atom forms the shortest, strongest bond with hydrogen, and the H–X bond dissociation "
    "enthalpy falls from HF to HI: Statement I is true. Since the bond gets weaker, thermal stability "
    "decreases from HF to HI: Statement II is false.",
    ["H–X bond enthalpy: HF > HCl > HBr > HI → I true", "Weaker bond → less stable → stability HF > HI → II false"],
    answer="C", ncert=f"{REF10B}, group 17 elements: reactivity towards hydrogen", seconds=35)

add("Group 15 and 16 trends", I, "match_list",
    lists("Match List-I (group) with List-II (highest oxidation state shown by elements of the group).",
          ["Group 13", "Group 15", "Group 16", "Group 17"], ["+7", "+6", "+3", "+5"]),
    match("A", M("III IV II I"), [M("IV III II I"), M("III IV I II"), M("III II IV I")]),
    "Highest oxidation state = number of valence electrons",
    "For p-block groups 13 to 17 the highest oxidation state equals the number of valence electrons "
    "(group number − 10): +3, +5, +6 and +7. (Oxygen and fluorine, the first members, do not reach these.)",
    ["Group 13: ns² np¹ → +3 → III", "Group 15: ns² np³ → +5 → IV", "Group 16: ns² np⁴ → +6 → II",
     "Group 17: ns² np⁵ → +7 → I"],
    why="The other codes swap neighbouring groups.",
    ncert=f"{REF10A}, p-block elements: oxidation states; {REF10B}, oxidation states of groups 15–17",
    seconds=35)

add("Anomalous first element", A, "multi_statement",
    ms("Which of the following statements about the first elements of p-block groups are correct?",
       ["Carbon can show a maximum covalency of six.",
        "Water molecules are associated through hydrogen bonds, whereas H₂S molecules are not.",
        "Nitrogen shows allotropy, like the other elements of group 15.",
        "The single N–N bond is weaker than the single P–P bond.",
        "Nitrogen is a gas at room temperature, whereas the other elements of group 15 are solids."]),
    multi("A", {"a": False, "b": True, "c": False, "d": True, "e": True},
          ["(a), (b) and (d) only", "(b), (c) and (e) only", "(a), (c), (d) and (e) only"]),
    "Anomalous behaviour of the first member of a group",
    "Carbon has no d orbitals, so its maximum covalency is four. Oxygen is small and highly electronegative, "
    "so water is hydrogen bonded; H₂S is not. All group 15 elements except nitrogen show allotropy. The N–N "
    "single bond is weaker than P–P because the lone pairs on the closely spaced N atoms repel strongly. N₂ is "
    "a diatomic gas; P, As, Sb and Bi are solids.",
    ["(a) False: maximum covalency of C is 4", "(b) True", "(c) False: nitrogen does not show allotropy",
     "(d) True", "(e) True"],
    why="Options with (a) or (c) are wrong.",
    ncert=f"{REF10A}, anomalous behaviour of carbon; {REF10B}, anomalous properties of nitrogen and oxygen",
    seconds=75)

add("Group 15 and 16 trends", A, "assertion_reason",
    ar("Among the hydrides of group 16, H₂Te is the strongest reducing agent.",
       "The E–H bond dissociation enthalpy decreases from H₂S to H₂Te."),
    AR_, "Reducing character of group 16 hydrides",
    "All the hydrides except water show reducing character, and it increases from H₂S to H₂Te. The reason is "
    "that the E–H bond becomes longer and weaker down the group, so H₂Te gives up hydrogen most easily. Both "
    "statements are true and R explains A.",
    ["E–H bond enthalpy: H₂S > H₂Se > H₂Te (R true)", "Weaker bond → easier release of H → stronger reductant "
     "(A true, explained by R)"],
    answer="A", ncert=f"{REF10B}, group 16 elements: reactivity with hydrogen", seconds=45)

add("Group 13 and 14 trends", A, "statement_pair",
    sp("Boron has an unusually high melting point compared with the other elements of group 13.",
       "Gallium has the highest melting point among the elements of group 13."),
    SP_, "Melting points in group 13",
    "Boron has a very high melting point because of its very strong crystalline lattice: Statement I is true. "
    "Gallium has an unusually low melting point (303 K) and can be liquid on a hot summer day, so it does not "
    "have the highest melting point: Statement II is false.",
    ["Boron: strong covalent lattice → very high m.p. → I true", "Gallium: m.p. 303 K (very low) → II false"],
    answer="C", ncert=f"{REF10A}, group 13 elements: physical properties", seconds=35)

add("Group 17 and 18 trends", A, "multi_statement",
    ms("Which of the following statements about the noble gases (group 18) are correct?",
       ["Helium has the configuration 1s², while the others have ns² np⁶.",
        "Noble gases exist as diatomic molecules.",
        "They have very high ionisation enthalpies.",
        "Their boiling points decrease down the group.",
        "Atomic radius increases from helium to xenon."]),
    multi("B", {"a": True, "b": False, "c": True, "d": False, "e": True},
          ["(a), (b) and (c) only", "(b), (d) and (e) only", "(a), (c), (d) and (e) only"]),
    "General properties of the noble gases",
    "Noble gases have completely filled valence shells and very high ionisation enthalpies. They are "
    "monoatomic; their only interatomic forces are weak dispersion forces, which grow with atomic size, so "
    "their boiling points increase down the group. Each step down the group adds a new electron shell, so "
    "the atomic radius increases from He to Xe.",
    ["(a) True", "(b) False: monoatomic", "(c) True", "(d) False: boiling points increase down the group",
     "(e) True: one more shell per period"],
    why="Options containing (b) or (d) are wrong.",
    ncert=f"{REF10B}, group 18 elements: electronic configuration; atomic radii; physical properties",
    seconds=60)


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
    doc = {"schema_version": "1.0", "batch_id": "BATCH_002", "created_at": TODAY,
           "notes": "Package CHE_002_p1: 128 original Chemistry questions (physical chemistry, periodicity and "
                    "p-block). Numerical answers re-derived in tools/batch_002/CHE_002_p1.py.",
           "stimuli": [], "questions": QUESTIONS}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {OUT}: {n} questions; difficulty {dict(Counter(q['difficulty'] for q in QUESTIONS))}; "
          f"formats {dict(fmts)}; keys {dict(sorted(KEYS.items()))}")
