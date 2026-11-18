"""Writes batches/parts/BATCH_003_CHE_p1.json: package CHE_003_p1 of BATCH_003 (Chemistry, 122 questions).

Topics: Some Basic Concepts, Atomic Structure, Chemical Bonding, Thermodynamics, Solutions, Equilibrium,
Redox and Electrochemistry, Chemical Kinetics, Periodicity, p-Block Elements. IDs NEET_CHE_000501..000622.

Every computable answer is re-derived here with an assert before anything is written; the quota per
(topic, difficulty), the ID range, the format mix and the answer-key balance are asserted too.
The position of every correct option is chosen by hand in the call that adds the question (argument `at`)
and never moved by code.

    cd docs/neet-bank && python tools/batch_003/CHE_003_p1.py
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
PACKAGE = "CHE_003_p1"
PLAN = ROOT / "batches" / "plans" / "BATCH_003_plan.json"
OUT = ROOT / "batches" / "parts" / "BATCH_003_CHE_p1.json"
TODAY = "2026-11-16"
LETTERS = "ABCD"
CHE = "Chemistry"
FIRST_ID = 501
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

avg_cl = 35 * 0.75 + 37 * 0.25
assert close(avg_cl, 35.5) and close((35 + 37) / 2, 36.0) and close(35 * 0.25 + 37 * 0.75, 36.5)
add("Mole concept", B, "numerical",
    "Naturally occurring chlorine consists of 75% ³⁵Cl (atomic mass 35 u) and 25% ³⁷Cl (atomic mass 37 u) by "
    "number of atoms. The average atomic mass of chlorine is:",
    Opts("B", "35.5 u", ["36.0 u", "36.5 u", "35.0 u"]),
    "Average atomic mass from isotopic abundances",
    "The average atomic mass is the abundance-weighted mean of the isotopic masses: each isotopic mass is "
    "multiplied by its fractional abundance and the products are added.",
    ["Contribution of ³⁵Cl = 35 × 0.75 = 26.25 u", "Contribution of ³⁷Cl = 37 × 0.25 = 9.25 u",
     "Average atomic mass = 26.25 + 9.25 = 35.5 u"],
    why="36.0 u is a simple average that ignores the abundances. 36.5 u swaps the two abundances. 35.0 u takes "
        "only the more abundant isotope.",
    ncert=f"{REF1}, average atomic mass", seconds=35, checked=True)

add("Laws of chemical combination", B, "direct",
    "At the same temperature and pressure, 100 mL of hydrogen combines with 50 mL of oxygen to give 100 mL of "
    "water vapour. The simple whole-number ratio of these volumes (2 : 1 : 2) illustrates:",
    Opts("A", "Gay-Lussac's law of gaseous volumes",
         ["The law of multiple proportions", "The law of definite proportions", "The law of conservation of mass"]),
    "Gay-Lussac's law of gaseous volumes",
    "Gay-Lussac observed that when gases combine or are produced in a reaction, they do so in a simple ratio by "
    "volume, provided all the gases are at the same temperature and pressure. Hydrogen, oxygen and water vapour "
    "here are in the volume ratio 100 : 50 : 100 = 2 : 1 : 2.",
    ["The data compare volumes of gases at the same T and p", "Ratio 100 : 50 : 100 = 2 : 1 : 2 (simple whole numbers)",
     "This is the law of gaseous volumes"],
    why="Multiple proportions compares two different compounds of the same elements. Definite proportions and "
        "conservation of mass are statements about masses, not volumes of gases.",
    ncert=f"{REF1}, Gay Lussac's law of gaseous volumes", seconds=25)

add("Empirical and molecular formulae", B, "statement_pair",
    sp("The empirical formula of ethanoic acid (CH₃COOH) is C₂H₄O₂.",
       "The molecular formula of a compound is a whole-number multiple of its empirical formula."),
    SP_, "Empirical and molecular formulae",
    "The empirical formula gives the simplest whole-number ratio of atoms. Ethanoic acid has the molecular "
    "formula C₂H₄O₂; dividing by 2 gives the empirical formula CH₂O, so Statement I is false. The molecular "
    "formula is n × (empirical formula), where n = molar mass / empirical formula mass, so Statement II is true.",
    ["C₂H₄O₂ ÷ 2 = CH₂O → empirical formula is CH₂O → Statement I false",
     "Molecular formula = n × empirical formula → Statement II true"],
    answer="D", ncert=f"{REF1}, empirical formula for molecular formula", seconds=30)

n_fe, n_o = F(70, 10) / 56, F(30, 10) / 16
assert n_o / n_fe == F(3, 2)
add("Empirical and molecular formulae", I, "numerical",
    "7.0 g of iron combines completely with 3.0 g of oxygen to form an oxide. The empirical formula of the "
    "oxide is (Fe = 56, O = 16):",
    Opts("D", "Fe₂O₃", ["FeO", "Fe₃O₄", "Fe₃O₂"]),
    "Empirical formula from combining masses",
    "Convert each mass to moles of atoms and find the simplest whole-number ratio.",
    ["Moles of Fe = 7.0 / 56 = 0.125", "Moles of O = 3.0 / 16 = 0.1875",
     "Fe : O = 0.125 : 0.1875 = 1 : 1.5 = 2 : 3", "Empirical formula = Fe₂O₃"],
    why="FeO assumes a 1 : 1 ratio. Fe₃O₄ would need Fe : O = 3 : 4 (0.75), not 2 : 3. Fe₃O₂ inverts the "
        "mole ratio.",
    ncert=f"{REF1}, empirical formula", seconds=50, checked=True)

n_ag = 0.050 * 0.2
assert close(n_ag * 143.5, 1.435) and close(n_ag * 108, 1.08) and close(2 * n_ag * 143.5, 2.87)
assert close(0.005 * 0.2 * 143.5, 0.1435)
add("Stoichiometry", I, "numerical",
    "50 mL of 0.2 M AgNO₃ solution is added to an excess of NaCl solution: AgNO₃ + NaCl → AgCl↓ + NaNO₃. The "
    "mass of AgCl precipitated is (Ag = 108, Cl = 35.5):",
    Opts("B", "1.435 g", ["1.08 g", "2.87 g", "0.1435 g"]),
    "Stoichiometry of a precipitation reaction",
    "AgNO₃ is the limiting reagent (NaCl is in excess). One mole of AgNO₃ gives one mole of AgCl.",
    ["Moles of AgNO₃ = 0.2 mol L⁻¹ × 0.050 L = 0.010 mol", "Moles of AgCl = 0.010 mol",
     "Molar mass of AgCl = 108 + 35.5 = 143.5 g mol⁻¹", "Mass of AgCl = 0.010 × 143.5 = 1.435 g"],
    why="1.08 g is the mass of silver alone. 2.87 g assumes two moles of AgCl per mole of AgNO₃. 0.1435 g "
        "comes from writing 50 mL as 0.005 L.",
    ncert=f"{REF1}, stoichiometry and reactions in solutions", seconds=50, checked=True)

add("Laws of chemical combination", I, "assertion_reason",
    ar("When calcium carbonate is heated strongly in an open container, the solid left behind weighs less "
       "than the calcium carbonate taken.",
       "Mass is not conserved in a decomposition reaction."),
    AR_, "Law of conservation of mass",
    "CaCO₃ → CaO + CO₂. The carbon dioxide escapes from the open container, so the solid residue (CaO) weighs "
    "less than the CaCO₃: A is true. The total mass of CaO and CO₂ equals the mass of CaCO₃; mass is "
    "conserved in every chemical reaction, so R is false.",
    ["CaCO₃(s) → CaO(s) + CO₂(g); the gas escapes → residue is lighter (A true)",
     "Mass of CaO + mass of CO₂ = mass of CaCO₃ → mass is conserved (R false)"],
    answer="C", ncert=f"{REF1}, law of conservation of mass", seconds=35)

moles = {"CH4": 8 / 16, "CO2": 88 / 44, "NH3": 1.7 / 17, "H2O": 54 / 18}
assert [round(v, 3) for v in moles.values()] == [0.5, 2.0, 0.1, 3.0]
add("Mole concept", I, "match_list",
    lists("Match List-I (sample) with List-II (amount of substance). (H = 1, C = 12, N = 14, O = 16)",
          ["8 g of CH₄", "88 g of CO₂", "1.7 g of NH₃", "54 g of H₂O"],
          ["0.1 mol", "0.5 mol", "2 mol", "3 mol"]),
    match("C", M("II III I IV"), [M("III II I IV"), M("II III IV I"), M("I III II IV")]),
    "Moles from mass and molar mass",
    "Amount of substance n = mass / molar mass. Molar masses: CH₄ 16, CO₂ 44, NH₃ 17 and H₂O 18 g mol⁻¹.",
    ["8 / 16 = 0.5 mol → II", "88 / 44 = 2 mol → III", "1.7 / 17 = 0.1 mol → I", "54 / 18 = 3 mol → IV"],
    why="The other codes swap 0.5 mol with 2 mol, or 0.1 mol with 3 mol, or 0.1 mol with 0.5 mol.",
    ncert=f"{REF1}, mole concept and molar masses", seconds=45, checked=True)

n_co2 = (0.50 - 0.28) / 44
m_carb = 0.50 / n_co2
assert close(m_carb, 100) and close(m_carb - 60, 40) and close(0.28 / n_co2, 56)
add("Stoichiometry", A, "numerical",
    "0.50 g of a metal carbonate MCO₃ on strong heating decomposes completely: MCO₃(s) → MO(s) + CO₂(g). The "
    "residue of MO weighs 0.28 g. The atomic mass of the metal M is (C = 12, O = 16):",
    Opts("A", "40", ["56", "100", "24"]),
    "Stoichiometry: molar mass from mass loss",
    "The loss in mass is the CO₂ given off. Its moles equal the moles of MCO₃ decomposed, which gives the "
    "molar mass of MCO₃ and hence the atomic mass of M.",
    ["Mass of CO₂ = 0.50 − 0.28 = 0.22 g = 0.22 / 44 = 0.005 mol", "Moles of MCO₃ = 0.005 mol",
     "Molar mass of MCO₃ = 0.50 / 0.005 = 100 g mol⁻¹", "Atomic mass of M = 100 − (12 + 48) = 40"],
    shortcut="Mass of MO / mass of CO₂ = (M + 16) / 44 → 0.28 / 0.22 × 44 = 56 = M + 16 → M = 40.",
    why="56 is the molar mass of MO, not of M. 100 is the molar mass of MCO₃. 24 is the atomic mass of Mg, "
        "but MgCO₃ (84 g mol⁻¹) would leave 0.24 g of MgO, not 0.28 g.",
    ncert=f"{REF1}, stoichiometry and stoichiometric calculations", seconds=90, checked=True)

n_cl = 0.100 * 0.1 + 0.100 * 0.2 * 2
assert close(n_cl / 0.200, 0.25) and close((0.100 * 0.1 + 0.100 * 0.2) / 0.200, 0.15)
assert close(n_cl / 0.100, 0.50) and close(0.1 + 0.2, 0.30)
add("Mole concept", A, "numerical",
    "100 mL of 0.1 M NaCl solution is mixed with 100 mL of 0.2 M CaCl₂ solution. Assuming complete "
    "dissociation and that the volumes are additive, the molar concentration of Cl⁻ ions in the mixture is:",
    Opts("D", "0.25 M", ["0.15 M", "0.50 M", "0.30 M"]),
    "Molarity of an ion in a mixture of solutions",
    "Count the moles of Cl⁻ from each solution (CaCl₂ gives two Cl⁻ per formula unit) and divide by the total "
    "volume of the mixture.",
    ["Cl⁻ from NaCl = 0.1 × 0.100 = 0.010 mol", "Cl⁻ from CaCl₂ = 2 × 0.2 × 0.100 = 0.040 mol",
     "Total Cl⁻ = 0.050 mol; total volume = 0.200 L", "[Cl⁻] = 0.050 / 0.200 = 0.25 M"],
    why="0.15 M forgets that each CaCl₂ gives two Cl⁻ ions. 0.50 M divides by 100 mL instead of the total "
        "200 mL. 0.30 M simply adds the two molarities.",
    ncert=f"{REF1}, reactions in solutions: molarity", seconds=75, checked=True)

add("Mole concept", A, "multi_statement",
    ms("Which of the following statements are correct? (H = 1, O = 16)",
       ["One mole of any substance contains 6.022 × 10²³ elementary entities (atoms, molecules or ions).",
        "A pure compound has the same mass per cent of each element whatever its source or method of "
        "preparation.",
        "1 g of H₂ and 1 g of O₂ contain the same number of molecules.",
        "2 g of H₂ and 32 g of O₂ contain the same number of molecules.",
        "In the reaction 2H₂ + O₂ → 2H₂O, 4 g of H₂ reacts completely with exactly 16 g of O₂."]),
    multi("B", {"a": True, "b": True, "c": False, "d": True, "e": False},
          ["(a), (b), (c) and (d) only", "(b), (d) and (e) only", "(a), (d) and (e) only"]),
    "Mole concept, law of definite proportions and stoichiometry",
    "Equal numbers of moles contain equal numbers of molecules. 1 g of H₂ is 0.5 mol but 1 g of O₂ is only "
    "1/32 mol. 2 g of H₂ and 32 g of O₂ are each 1 mol. 4 g of H₂ (2 mol) needs 1 mol = 32 g of O₂, not 16 g.",
    ["(a) True: definition of the mole", "(b) True: law of definite proportions",
     "(c) False: 0.5 mol versus 0.03125 mol", "(d) True: 1 mol each",
     "(e) False: 4 g H₂ = 2 mol needs 1 mol O₂ = 32 g"],
    why="Any option containing (c) or (e) is wrong, and (a), (b) and (d) must all appear.",
    ncert=f"{REF1}, mole concept; law of definite proportions; stoichiometry", seconds=75)

# ==================================================================== 2. Atomic Structure
topic("Atomic Structure")
REF2 = f"{C11}, 'Structure of Atom'"

add("Quantum numbers and orbitals", B, "direct",
    "The maximum number of electrons that can be accommodated in a subshell with azimuthal quantum number "
    "l = 3 is:",
    Opts("C", "14", ["6", "10", "7"]),
    "Orbitals in a subshell",
    "A subshell with azimuthal quantum number l has (2l + 1) orbitals, each holding at most two electrons. "
    "For l = 3 (an f subshell) there are 7 orbitals and up to 14 electrons.",
    ["Number of orbitals = 2l + 1 = 7", "Maximum electrons = 2 × 7 = 14"],
    why="6 and 10 are the capacities of p (l = 1) and d (l = 2) subshells. 7 is the number of orbitals, not "
        "electrons.",
    ncert=f"{REF2}, quantum numbers: azimuthal quantum number", seconds=20)

nu = C_LIGHT / 500e-9
assert close(nu, 6.0e14) and close(C_LIGHT / 500, 6.0e5) and close(500e-9 / C_LIGHT, 1.67e-15, 0.01)
assert close(1 / 500e-9, 2.0e6)
add("Dual nature and uncertainty", B, "numerical",
    "The frequency of electromagnetic radiation of wavelength 500 nm is (c = 3.0 × 10⁸ m s⁻¹):",
    Opts("D", "6.0 × 10¹⁴ Hz", ["6.0 × 10⁵ Hz", "1.67 × 10⁻¹⁵ Hz", "2.0 × 10⁶ Hz"]),
    "Relation between frequency and wavelength, c = νλ",
    "Frequency ν = c / λ, with λ converted to metres.",
    ["λ = 500 nm = 500 × 10⁻⁹ m = 5.0 × 10⁻⁷ m", "ν = (3.0 × 10⁸) / (5.0 × 10⁻⁷) = 6.0 × 10¹⁴ s⁻¹ (Hz)"],
    why="6.0 × 10⁵ Hz leaves the wavelength in nanometres. 1.67 × 10⁻¹⁵ inverts the ratio (λ/c). 2.0 × 10⁶ "
        "is the wavenumber 1/λ in m⁻¹, not a frequency.",
    ncert=f"{REF2}, wave nature of electromagnetic radiation", seconds=30, checked=True)

add("Bohr model and hydrogen spectrum", B, "statement_pair",
    sp("In a discharge tube, cathode rays travel in straight lines in the absence of electric and magnetic "
       "fields.",
       "The characteristics of cathode rays depend on the material of the electrodes and on the nature of the "
       "gas present in the tube."),
    SP_, "Discovery of the electron: properties of cathode rays",
    "Cathode rays start from the cathode and move towards the anode in straight lines when no electric or "
    "magnetic field is applied, so Statement I is true. Their characteristics do not depend on the material "
    "of the electrodes or the nature of the gas, which showed that electrons are a basic constituent of all "
    "atoms, so Statement II is false.",
    ["Straight-line travel without fields → Statement I true",
     "Properties independent of electrode material and gas → Statement II false"],
    answer="C", ncert=f"{REF2}, discovery of electron", seconds=30)

add("Bohr model and hydrogen spectrum", B, "match_list",
    lists("Match List-I (scientist) with List-II (contribution to the structure of the atom).",
          ["J. J. Thomson", "R. A. Millikan", "Ernest Rutherford", "James Chadwick"],
          ["Discovery of the neutron", "Oil-drop experiment: charge on the electron",
           "α-particle scattering experiment: the nuclear model", "Charge-to-mass ratio (e/mₑ) of the electron"]),
    match("B", M("IV II III I"), [M("II IV III I"), M("IV II I III"), M("IV III II I")]),
    "Discovery of sub-atomic particles",
    "Thomson measured the charge-to-mass ratio of the electron with cathode rays in electric and magnetic "
    "fields. Millikan found the charge on the electron by the oil-drop experiment. Rutherford's α-particle "
    "scattering experiment led to the nuclear model. Chadwick discovered the neutron in 1932.",
    ["Thomson → e/mₑ → IV", "Millikan → oil drop → II", "Rutherford → α scattering → III",
     "Chadwick → neutron → I"],
    why="The other codes swap Thomson with Millikan, Rutherford with Chadwick, or Millikan with Rutherford.",
    ncert=f"{REF2}, sub-atomic particles; Rutherford's nuclear model", seconds=35)

e_ph = H_PLANCK * C_LIGHT / 600e-9
n_ph = 6.626 / e_ph
assert close(e_ph, 3.313e-19) and close(n_ph, 2.0e19)
assert close(6.626 / (H_PLANCK * C_LIGHT / 600), 2.0e28) and close(e_ph / 6.626, 5.0e-20) and close(60 * n_ph, 1.2e21)
add("Dual nature and uncertainty", I, "numerical",
    "A lamp emits monochromatic light of wavelength 600 nm with a power of 6.626 W (1 W = 1 J s⁻¹). The number "
    "of photons it emits per second is (h = 6.626 × 10⁻³⁴ J s, c = 3.0 × 10⁸ m s⁻¹):",
    Opts("A", "2.0 × 10¹⁹", ["2.0 × 10²⁸", "5.0 × 10⁻²⁰", "1.2 × 10²¹"]),
    "Planck's quantum theory: energy of a photon, E = hc/λ",
    "Find the energy of one photon, then divide the energy emitted per second (the power) by it.",
    ["E(photon) = (6.626 × 10⁻³⁴ × 3.0 × 10⁸) / (600 × 10⁻⁹) = 3.313 × 10⁻¹⁹ J",
     "Energy emitted per second = 6.626 J", "Photons per second = 6.626 / (3.313 × 10⁻¹⁹) = 2.0 × 10¹⁹"],
    why="2.0 × 10²⁸ leaves the wavelength in nanometres. 5.0 × 10⁻²⁰ divides the photon energy by the power. "
        "1.2 × 10²¹ is the number emitted per minute, not per second.",
    ncert=f"{REF2}, particle nature of electromagnetic radiation: Planck's quantum theory", seconds=70,
    checked=True)

orbitals = {"4d": (4, 2), "5p": (5, 1), "6s": (6, 0), "4f": (4, 3)}
first = min(orbitals, key=lambda k: (sum(orbitals[k]), orbitals[k][0]))
assert first == "4d"
add("Electronic configuration", I, "direct",
    "According to the (n + l) rule, which of the following orbitals is filled first?",
    Opts("C", "4d", ["5p", "6s", "4f"]),
    "Aufbau principle and the (n + l) rule",
    "Orbitals are filled in order of increasing (n + l); when two orbitals have the same (n + l), the one with "
    "the lower n is filled first. 4d, 5p and 6s all have n + l = 6, and 4d has the lowest n. 4f has "
    "n + l = 7.",
    ["4d: 4 + 2 = 6; 5p: 5 + 1 = 6; 6s: 6 + 0 = 6; 4f: 4 + 3 = 7",
     "Among equal (n + l) = 6, lowest n → 4d"],
    why="5p and 6s have the same (n + l) as 4d but a higher n. 4f has a larger (n + l) of 7.",
    ncert=f"{REF2}, filling of orbitals in atom: aufbau principle", seconds=40)

add("Bohr model and hydrogen spectrum", I, "assertion_reason",
    ar("The energy of the electron in a hydrogen atom, as given by Bohr's theory, is negative.",
       "The energy of the electron is taken as zero when it is completely free from the nucleus, and the "
       "electron bound in the atom has a lower energy than this free electron."),
    AR_, "Negative sign of electron energy in Bohr's model",
    "In Bohr's theory, Eₙ = −R_H (1/n²). The zero of energy is the free electron at infinite distance (n = ∞). "
    "An electron attracted by the nucleus is more stable and has less energy than the free electron, so its "
    "energy is negative. R states exactly why A is true.",
    ["Reference: free electron (n = ∞) has E = 0", "Bound electron is more stable → lower than zero → negative",
     "R explains A"],
    answer="A", ncert=f"{REF2}, Bohr's model for hydrogen atom", seconds=40)

add("Quantum numbers and orbitals", I, "multi_statement",
    ms("Which of the following statements are correct?",
       ["For l = 1, the magnetic quantum number mₗ can be −1, 0 or +1.",
        "The spin quantum number mₛ can have only the values +½ and −½.",
        "The principal quantum number determines the size and, to a large extent, the energy of an orbital.",
        "The lobes of the 3d_{x²−y²} orbital lie between the x and y axes.",
        "For a given n, the azimuthal quantum number l can take the values 0, 1, 2, ... up to n."]),
    multi("D", {"a": True, "b": True, "c": True, "d": False, "e": False},
          ["(a), (b), (c) and (e) only", "(b), (c) and (d) only", "(a), (c), (d) and (e) only"]),
    "Quantum numbers",
    "mₗ runs from −l to +l. The spin quantum number has two values, ±½. n fixes the size and largely the "
    "energy of the orbital. The 3d_{x²−y²} orbital has its lobes along the x and y axes (it is 3d_xy whose "
    "lobes lie between them). l can take the values 0 to (n − 1), not up to n.",
    ["(a) True", "(b) True", "(c) True", "(d) False: lobes along the axes",
     "(e) False: l = 0 to n − 1"],
    why="Any option with (d) or (e) is wrong.",
    ncert=f"{REF2}, quantum numbers; shapes of atomic orbitals", seconds=60)

RH_HZ = 3.29e15
nu32 = RH_HZ * (1 / 4 - 1 / 9)
assert close(nu32, 4.57e14) and close(RH_HZ * (1 / 2 - 1 / 3), 5.48e14) and close(RH_HZ * (1 / 4 + 1 / 9), 1.19e15)
assert close(RH_HZ / 4, 8.23e14)
add("Bohr model and hydrogen spectrum", I, "numerical",
    "The frequency of the line emitted when the electron of a hydrogen atom falls from the n = 3 orbit to the "
    "n = 2 orbit is (ν = 3.29 × 10¹⁵ (1/n₁² − 1/n₂²) Hz):",
    Opts("B", "4.57 × 10¹⁴ Hz", ["5.48 × 10¹⁴ Hz", "1.19 × 10¹⁵ Hz", "8.23 × 10¹⁴ Hz"]),
    "Frequencies of lines in the hydrogen spectrum",
    "Put n₁ = 2 (lower level) and n₂ = 3 (upper level) in the given expression.",
    ["1/n₁² − 1/n₂² = 1/4 − 1/9 = 5/36", "ν = 3.29 × 10¹⁵ × 5/36 = 4.57 × 10¹⁴ Hz (a Balmer line)"],
    why="5.48 × 10¹⁴ Hz uses 1/n instead of 1/n². 1.19 × 10¹⁵ Hz adds the two terms instead of subtracting. "
        "8.23 × 10¹⁴ Hz keeps only the 1/n₁² term (the series limit).",
    ncert=f"{REF2}, line spectrum of hydrogen", seconds=50, checked=True)

ORDER = ["1s", "2s", "2p", "3s", "3p", "4s", "3d", "4p"]
CAP = {"s": 2, "p": 6, "d": 10}
L_OF = {"s": 0, "p": 1, "d": 2}


def config(z):
    out, left = {}, z
    for o in ORDER:
        k = min(left, CAP[o[1]])
        if k:
            out[o] = k
        left -= k
    return out


s_conf = config(16)
assert s_conf == {"1s": 2, "2s": 2, "2p": 6, "3s": 2, "3p": 4}
nl3 = sum(v for o, v in s_conf.items() if int(o[0]) + L_OF[o[1]] == 3)
assert nl3 == 8 and s_conf["2p"] == 6 and s_conf["3s"] == 2
add("Electronic configuration", A, "numerical",
    "In a ground-state sulphur atom (Z = 16), the number of electrons for which n + l = 3 is:",
    Opts("C", "8", ["6", "2", "4"]),
    "Electronic configuration and quantum numbers",
    "Write the configuration and find the (n + l) value of each occupied subshell. Both 2p (2 + 1) and 3s "
    "(3 + 0) have n + l = 3.",
    ["S: 1s² 2s² 2p⁶ 3s² 3p⁴", "n + l: 1s = 1, 2s = 2, 2p = 3, 3s = 3, 3p = 4",
     "Electrons with n + l = 3: 2p⁶ + 3s² = 8"],
    why="6 counts only the 2p electrons and 2 only the 3s electrons. 4 counts the 3p electrons, which have "
        "n + l = 4.",
    ncert=f"{REF2}, quantum numbers; electronic configuration of atoms", seconds=60, checked=True)

RH = 1.097e7
lam = {n: 1 / (RH * (1 - 1 / n ** 2)) * 1e9 for n in (2, 3, 4, 5)}
assert close(lam[3], 102.6, 0.002) and not any(close(lam[n], 102.6, 0.02) for n in (2, 4, 5))
add("Bohr model and hydrogen spectrum", A, "numerical",
    "A line of wavelength 102.6 nm appears in the emission spectrum of atomic hydrogen, produced when the "
    "electron falls to the n = 1 orbit. The orbit from which the electron fell is "
    "(R_H = 1.097 × 10⁷ m⁻¹; 1/λ = R_H (1/n₁² − 1/n₂²)):",
    Opts("B", "n = 3", ["n = 2", "n = 4", "n = 5"]),
    "Rydberg formula for the Lyman series",
    "Use 1/λ = R_H (1 − 1/n²) for a Lyman line and solve for n.",
    ["1/λ = 1 / (102.6 × 10⁻⁹ m) = 9.747 × 10⁶ m⁻¹",
     "1 − 1/n² = 9.747 × 10⁶ / 1.097 × 10⁷ = 0.889", "1/n² = 0.111 ≈ 1/9 → n = 3"],
    shortcut="Lyman lines: n = 2 → 121.5 nm, n = 3 → 102.6 nm, n = 4 → 97.2 nm.",
    why="n = 2 gives 121.5 nm, n = 4 gives 97.2 nm and n = 5 gives 95.0 nm.",
    ncert=f"{REF2}, line spectrum of hydrogen", seconds=90, checked=True)

add("Bohr model and hydrogen spectrum", A, "assertion_reason",
    ar("The emission spectrum of atomic hydrogen is a continuous spectrum.",
       "The electron in a hydrogen atom can have only certain definite (quantised) energies."),
    AR_, "Line spectrum and quantised energy levels",
    "Because the electron can have only certain energies, it can emit only photons whose energies equal the "
    "differences between these levels. The emission spectrum of hydrogen is therefore a line spectrum, not a "
    "continuous one: A is false and R is true.",
    ["Quantised energy levels → only certain ΔE values → R true",
     "Only certain frequencies emitted → line spectrum → A false"],
    answer="D", ncert=f"{REF2}, atomic spectra; Bohr's model for hydrogen atom", seconds=35)

add("Electronic configuration", A, "multi_statement",
    ms("Which of the following statements about ground-state species are correct? (Z: K = 19, Fe = 26, "
       "Ni = 28, Zn = 30)",
       ["Fe³⁺ has five unpaired electrons.",
        "Zn²⁺ has no unpaired electron.",
        "The electronic configuration of potassium is [Ar] 3d¹.",
        "Ni²⁺ has two unpaired electrons.",
        "When iron forms Fe²⁺, the electrons are removed from the 3d orbitals before the 4s orbital."]),
    multi("C", {"a": True, "b": True, "c": False, "d": True, "e": False},
          ["(a), (b) and (e) only", "(a), (b), (c) and (d) only", "(b), (d) and (e) only"]),
    "Electronic configurations of atoms and ions",
    "Fe is [Ar] 3d⁶ 4s²; on ionisation the 4s electrons leave first, so Fe²⁺ is [Ar] 3d⁶ and Fe³⁺ is [Ar] 3d⁵ "
    "(five unpaired). Zn²⁺ is [Ar] 3d¹⁰ (none unpaired). Ni²⁺ is [Ar] 3d⁸ (two unpaired). Potassium fills 4s "
    "before 3d: [Ar] 4s¹.",
    ["(a) True: 3d⁵", "(b) True: 3d¹⁰", "(c) False: K is [Ar] 4s¹", "(d) True: 3d⁸ has two unpaired",
     "(e) False: 4s electrons are removed first"],
    why="Options with (c) or (e) are wrong, and (d) must appear with (a) and (b).",
    ncert=f"{REF2}, electronic configuration of atoms", seconds=75)

# ==================================================================== 3. Chemical Bonding and Molecular Structure
topic("Chemical Bonding and Molecular Structure")
REF3 = f"{C11}, 'Chemical Bonding and Molecular Structure'"

assert 8 - 4 == 4 and (8 - 4) // 2 == 2   # Xe: 8 valence electrons, 4 used in Xe–F bonds -> 2 lone pairs
add("VSEPR shapes", B, "direct",
    "The number of lone pairs of electrons on the central xenon atom in XeF₄ is:",
    Opts("D", "2", ["0", "1", "3"]),
    "Lone pairs on the central atom (VSEPR)",
    "Xenon has 8 valence electrons. Four of them form four Xe–F bonds, leaving 4 electrons, i.e. 2 lone pairs. "
    "Four bond pairs and two lone pairs (octahedral arrangement) give a square planar molecule.",
    ["Valence electrons of Xe = 8", "Used in 4 Xe–F bonds = 4", "Remaining 4 electrons = 2 lone pairs"],
    why="0 would make XeF₄ tetrahedral. 1 is the number for XeF₆. 3 is the number for XeF₂.",
    ncert=f"{REF3}, VSEPR theory: molecules with bond pairs and lone pairs", seconds=25)

add("Ionic bonding and lattice enthalpy", B, "direct",
    "Which of the following ionic solids has the highest lattice enthalpy?",
    Opts("B", "MgO", ["NaCl", "KCl", "NaF"]),
    "Factors affecting lattice enthalpy",
    "Lattice enthalpy increases with the charges on the ions and decreases with their size. MgO is made of "
    "doubly charged ions (Mg²⁺ and O²⁻) that are also small, so the attraction between them is far greater "
    "than in the solids made of singly charged ions.",
    ["MgO: ions of charge +2 and −2", "NaCl, KCl, NaF: ions of charge +1 and −1",
     "Higher ionic charges → much larger lattice enthalpy → MgO"],
    why="NaCl, KCl and NaF all contain singly charged ions. Among them NaF is highest (smallest ions), but it "
        "is still far below MgO.",
    ncert=f"{REF3}, ionic or electrovalent bond: lattice enthalpy", seconds=25)

add("Hydrogen and metallic bonding", B, "statement_pair",
    sp("In solid and liquid hydrogen fluoride, the HF molecules are associated through hydrogen bonds into "
       "zig-zag chains.",
       "Intermolecular hydrogen bonding lowers the boiling point of a compound."),
    SP_, "Hydrogen bonding and its effect on physical properties",
    "Each H of an HF molecule is attracted to the F of a neighbouring molecule, giving zig-zag (HF)ₙ chains, so "
    "Statement I is true. Intermolecular hydrogen bonds hold the molecules together, so extra energy is needed "
    "to separate them; the boiling point is raised, not lowered. Statement II is false.",
    ["H–F···H–F···H–F chains → Statement I true", "Intermolecular H-bonds raise boiling points → Statement II false"],
    answer="C", ncert=f"{REF3}, hydrogen bonding: types of H-bonds", seconds=30)

add("VSEPR shapes", B, "match_list",
    lists("Match List-I (molecule) with List-II (its shape).",
          ["BF₃", "NH₃", "SF₆", "CH₄"],
          ["Tetrahedral", "Trigonal pyramidal", "Trigonal planar", "Octahedral"]),
    match("C", M("III II IV I"), [M("II III IV I"), M("III II I IV"), M("III IV II I")]),
    "Shapes of molecules from VSEPR theory",
    "BF₃: 3 bond pairs, no lone pair → trigonal planar. NH₃: 3 bond pairs + 1 lone pair → trigonal pyramidal. "
    "SF₆: 6 bond pairs → octahedral. CH₄: 4 bond pairs → tetrahedral.",
    ["BF₃ → III", "NH₃ → II", "SF₆ → IV", "CH₄ → I"],
    why="The other codes swap BF₃ with NH₃ (planar versus pyramidal), SF₆ with CH₄, or NH₃ with SF₆.",
    ncert=f"{REF3}, VSEPR theory", seconds=30)

assert 6 * 2 == 12   # six S–F bond pairs around S
add("VSEPR shapes", B, "numerical",
    "The number of electrons around the central sulphur atom in SF₆ (counting the shared pairs of all the S–F "
    "bonds) is:",
    Opts("A", "12", ["8", "6", "10"]),
    "Expanded octet",
    "In SF₆, sulphur forms six S–F single bonds, each a shared pair of electrons. Sulphur therefore has "
    "6 × 2 = 12 electrons around it, an expanded octet that is possible because sulphur (period 3) has 3d "
    "orbitals available.",
    ["Six S–F bonds", "Electrons around S = 6 × 2 = 12"],
    why="8 is the octet that SF₆ exceeds. 6 is the number of valence electrons of S (or the number of bonds). "
        "10 is the count for PCl₅.",
    ncert=f"{REF3}, limitations of the octet rule: the expanded octet", seconds=25, checked=True)

add("VSEPR shapes", B, "assertion_reason",
    ar("In BCl₃, the boron atom has only six electrons in its valence shell.",
       "Boron has only three valence electrons, and all three are used in forming the three B–Cl bonds."),
    AR_, "Incomplete octet of the central atom",
    "Boron (2s² 2p¹) has three valence electrons. Each forms one shared pair with a chlorine atom, so boron is "
    "surrounded by 3 × 2 = 6 electrons, an incomplete octet. R gives the reason for A.",
    ["B has 3 valence electrons → 3 B–Cl bonds", "Electrons around B = 6 → incomplete octet (A)",
     "R explains A"],
    answer="A", ncert=f"{REF3}, limitations of the octet rule: the incomplete octet of the central atom",
    seconds=30)

add("Fajans' rule and dipole moment", I, "direct",
    "Which of the following molecules has a non-zero dipole moment?",
    Opts("D", "CH₂Cl₂", ["CCl₄", "SF₆", "PCl₅"]),
    "Molecular geometry and dipole moment",
    "A molecule has zero dipole moment when its bond dipoles cancel by symmetry. In CCl₄ (regular "
    "tetrahedral), SF₆ (octahedral) and PCl₅ (trigonal bipyramidal) the identical bond dipoles cancel. In "
    "CH₂Cl₂ two C–H and two C–Cl bonds of different polarity point to the corners of a tetrahedron, so they "
    "cannot cancel.",
    ["CCl₄, SF₆, PCl₅: identical bonds, symmetrical shapes → μ = 0",
     "CH₂Cl₂: unlike bonds in a tetrahedral arrangement → μ ≠ 0"],
    why="CCl₄, SF₆ and PCl₅ are symmetrical with identical bonds, so their bond dipoles cancel.",
    ncert=f"{REF3}, polarity of bonds: dipole moment", seconds=35)

b2 = {"σ1s": 2, "σ*1s": 2, "σ2s": 2, "σ*2s": 2, "π2px": 1, "π2py": 1}
assert sum(b2.values()) == 10
nb = sum(v for k, v in b2.items() if "*" not in k)
na = sum(v for k, v in b2.items() if "*" in k)
assert (nb - na) / 2 == 1 and [v for v in b2.values()].count(1) == 2
add("Molecular orbital theory", I, "numerical",
    "Using the molecular orbital energy order for molecules up to N₂, in which the π2pₓ and π2p_y orbitals lie "
    "below the σ2p_z orbital, the bond order of B₂ and the number of unpaired electrons in it are:",
    Opts("B", "1 and 2", ["1 and 0", "2 and 0", "0.5 and 1"]),
    "Molecular orbital configuration of B₂",
    "B₂ has 10 electrons. After σ1s², σ*1s², σ2s² and σ*2s², the last two electrons enter the two degenerate π2p "
    "orbitals singly (Hund's rule).",
    ["B₂: σ1s² σ*1s² σ2s² σ*2s² (π2pₓ¹ = π2p_y¹)", "N_b = 6, N_a = 4 → bond order = (6 − 4)/2 = 1",
     "Two singly occupied π orbitals → 2 unpaired electrons (paramagnetic)"],
    why="'1 and 0' puts both electrons in σ2p_z (the order used for O₂ and F₂). '2 and 0' is the result for "
        "C₂. '0.5 and 1' counts only one electron beyond σ*2s.",
    ncert=f"{REF3}, molecular orbital theory: energy level diagram", seconds=60, checked=True)

add("Hybridisation and resonance", I, "statement_pair",
    sp("The canonical structures of a molecule that shows resonance have no real existence.",
       "The resonance hybrid is lower in energy, and hence more stable, than any single canonical structure."),
    SP_, "Resonance",
    "A molecule showing resonance is described by its resonance hybrid; the individual canonical structures "
    "are not real and the molecule does not switch between them, so Statement I is true. The energy of the "
    "hybrid is less than that of any single canonical structure, so resonance stabilises the molecule: "
    "Statement II is true.",
    ["Canonical forms are only on paper → Statement I true",
     "Hybrid has lower energy than any canonical form → Statement II true"],
    answer="A", ncert=f"{REF3}, resonance structures", seconds=30)

add("Hybridisation and resonance", I, "multi_statement",
    ms("Which of the following statements about bond parameters are correct?",
       ["The bond lengths of carbon–carbon bonds follow the order C≡C < C=C < C–C.",
        "For bonds between the same two atoms, the bond enthalpy increases as the bond order increases.",
        "For bonds between the same two atoms, the bond length increases as the bond order increases.",
        "The covalent radius of an atom is larger than its van der Waals radius.",
        "In the Lewis structure of carbon monoxide, the bond order between C and O is 3."]),
    multi("C", {"a": True, "b": True, "c": False, "d": False, "e": True},
          ["(a), (b) and (c) only", "(b), (d) and (e) only", "(a), (c) and (e) only"]),
    "Bond length, bond enthalpy and bond order",
    "As bond order increases, bond enthalpy increases and bond length decreases, so C≡C is shortest and C–C "
    "longest. The van der Waals radius (half the distance between non-bonded atoms of neighbouring molecules) "
    "is larger than the covalent radius. In C≡O there are three shared pairs, so the bond order is 3.",
    ["(a) True", "(b) True", "(c) False: bond length decreases", "(d) False: van der Waals radius is larger",
     "(e) True"],
    why="Options containing (c) or (d) are wrong.",
    ncert=f"{REF3}, bond parameters: bond length, bond enthalpy, bond order", seconds=60)

add("Molecular orbital theory", I, "assertion_reason",
    ar("The bond dissociation enthalpy of N₂ is higher than that of O₂.",
       "Nitrogen is less electronegative than oxygen."),
    AR_, "Bond order and bond strength",
    "N₂ has bond order 3 (a triple bond) and O₂ has bond order 2, so N₂ has the higher bond dissociation "
    "enthalpy: A is true. Nitrogen is indeed less electronegative than oxygen, so R is true. But "
    "electronegativity measures the pull of an atom on shared electrons in a bond with a different atom; it "
    "plays no part in comparing these two bonds between identical atoms. The strength follows from the bond "
    "order, so R does not explain A.",
    ["Bond order: N₂ = 3, O₂ = 2 → N₂ bond stronger (A true)", "Electronegativity N < O (R true)",
     "Strength is set by bond order, not electronegativity → R is not the explanation"],
    answer="B", ncert=f"{REF3}, bonding in some homonuclear diatomic molecules", seconds=40)

pairs = {"SF4": (4, 1), "ClF3": (3, 2), "XeF2": (2, 3), "BrF5": (5, 1)}
for mol, (bp, lp) in pairs.items():
    valence = {"SF4": 6, "ClF3": 7, "XeF2": 8, "BrF5": 7}[mol]
    assert valence - bp == 2 * lp
add("VSEPR shapes", I, "match_list",
    lists("Match List-I (molecule) with List-II (numbers of bond pairs and lone pairs on the central atom).",
          ["SF₄", "ClF₃", "XeF₂", "BrF₅"],
          ["2 bond pairs, 3 lone pairs", "3 bond pairs, 2 lone pairs", "4 bond pairs, 1 lone pair",
           "5 bond pairs, 1 lone pair"]),
    match("D", M("III II I IV"), [M("II III I IV"), M("III I II IV"), M("IV II I III")]),
    "Counting bond pairs and lone pairs",
    "Lone pairs = (valence electrons of central atom − number of bonds) / 2. S has 6, Cl and Br 7, Xe 8 "
    "valence electrons.",
    ["SF₄: (6 − 4)/2 = 1 lone pair, 4 bond pairs → III", "ClF₃: (7 − 3)/2 = 2 lone pairs → II",
     "XeF₂: (8 − 2)/2 = 3 lone pairs → I", "BrF₅: (7 − 5)/2 = 1 lone pair → IV"],
    why="The other codes swap SF₄ with ClF₃, ClF₃ with XeF₂, or SF₄ with BrF₅.",
    ncert=f"{REF3}, VSEPR theory: shapes of molecules with lone pairs", seconds=50, checked=True)

mu_cm = 1.6e-19 * 1.0e-10
mu_d = mu_cm / 3.33564e-30
assert close(mu_d, 4.80) and close(mu_d / 10, 0.48) and close(mu_d * 10, 48)
add("Fajans' rule and dipole moment", I, "numerical",
    "Charges of +1.6 × 10⁻¹⁹ C and −1.6 × 10⁻¹⁹ C are separated by a distance of 1.0 Å (1 Å = 10⁻¹⁰ m). The "
    "dipole moment of this pair, in debye, is (1 D = 3.33564 × 10⁻³⁰ C m):",
    Opts("B", "4.80 D", ["0.48 D", "48.0 D", "1.60 D"]),
    "Dipole moment μ = charge × distance",
    "Multiply the magnitude of the charge by the separation in metres to get C m, then convert to debye.",
    ["μ = (1.6 × 10⁻¹⁹ C) × (1.0 × 10⁻¹⁰ m) = 1.6 × 10⁻²⁹ C m",
     "μ = 1.6 × 10⁻²⁹ / 3.33564 × 10⁻³⁰ = 4.80 D"],
    why="0.48 D and 48.0 D are off by a factor of 10 (an error in the power of ten when converting Å to m). "
        "1.60 D reads the charge coefficient as the answer without converting to debye.",
    ncert=f"{REF3}, polarity of bonds: dipole moment", seconds=45, checked=True)

add("Molecular orbital theory", A, "multi_statement",
    ms("Which of the following species are paramagnetic according to molecular orbital theory?",
       ["O₂⁺", "N₂", "Li₂", "He₂⁺", "O₂²⁻"]),
    multi("A", {"a": True, "b": False, "c": False, "d": True, "e": False},
          ["(a), (b) and (d) only", "(a), (d) and (e) only", "(b), (c) and (e) only"]),
    "Magnetic behaviour from MO configurations",
    "A species is paramagnetic if it has one or more unpaired electrons in its MO configuration.",
    ["(a) O₂⁺ (15 e⁻): ... π*2p¹ → 1 unpaired → paramagnetic",
     "(b) N₂ (14 e⁻): all paired → diamagnetic", "(c) Li₂ (6 e⁻): σ1s² σ*1s² σ2s² → diamagnetic",
     "(d) He₂⁺ (3 e⁻): σ1s² σ*1s¹ → 1 unpaired → paramagnetic",
     "(e) O₂²⁻ (18 e⁻): π* orbitals full → diamagnetic"],
    why="N₂, Li₂ and O₂²⁻ have all electrons paired, so any option containing (b), (c) or (e) is wrong.",
    ncert=f"{REF3}, molecular orbital theory: bonding in homonuclear diatomic molecules", seconds=80)

mu_res = 2 * 1.5 * math.cos(math.radians(120 / 2))
assert close(mu_res, 1.5) and close(2 * 1.5 * math.cos(math.radians(30)), 2.60)
add("Fajans' rule and dipole moment", A, "numerical",
    "In a bent molecule AB₂, each A–B bond has a dipole moment of 1.5 D and the B–A–B bond angle is 120°. "
    "Ignoring any contribution from lone pairs, the resultant dipole moment of the molecule is "
    "(cos 60° = 0.5):",
    Opts("C", "1.5 D", ["3.0 D", "0 D", "2.6 D"]),
    "Dipole moment as a vector sum of bond dipoles",
    "The resultant of two equal vectors μ at an angle θ is 2μ cos(θ/2).",
    ["Resultant = 2 × 1.5 × cos(120°/2)", "= 2 × 1.5 × cos 60° = 2 × 1.5 × 0.5 = 1.5 D"],
    why="3.0 D adds the bond dipoles as if they were parallel. 0 D treats the molecule as linear. 2.6 D uses "
        "cos 30° instead of cos 60°.",
    ncert=f"{REF3}, polarity of bonds: dipole moment as a vector quantity", seconds=60, checked=True)

add("Fajans' rule and dipole moment", A, "assertion_reason",
    ar("SnCl₄ is more covalent than SnCl₂.",
       "Sn⁴⁺, having a higher charge and a smaller size than Sn²⁺, polarises the chloride ion more strongly."),
    AR_, "Fajans' rules: effect of cationic charge",
    "The greater the charge and the smaller the size of the cation, the greater its polarising power and the "
    "greater the covalent character of the bond. Sn⁴⁺ carries a higher charge and is smaller than Sn²⁺, so it "
    "distorts the electron cloud of Cl⁻ more, making SnCl₄ more covalent. R explains A.",
    ["Sn⁴⁺: higher charge, smaller radius → higher polarising power",
     "More polarisation of Cl⁻ → more covalent character → SnCl₄ more covalent", "R explains A"],
    answer="A", ncert=f"{REF3}, polarity of bonds: partial covalent character of ionic bonds", seconds=35)

add("VSEPR shapes", A, "statement_pair",
    sp("In ClF₃, both lone pairs on the chlorine atom occupy axial positions of the trigonal bipyramid.",
       "In SF₄, the lone pair on the sulphur atom occupies an equatorial position of the trigonal bipyramid."),
    SP_, "Positions of lone pairs in a trigonal bipyramid",
    "In a trigonal bipyramidal arrangement, lone pairs go to equatorial positions, where they suffer fewer "
    "90° repulsions. In ClF₃ both lone pairs are equatorial, giving a bent T-shape: Statement I is false. In SF₄ "
    "the lone pair is equatorial, giving the see-saw shape: Statement II is true.",
    ["ClF₃: 3 bp + 2 lp; lone pairs equatorial → T-shape → Statement I false",
     "SF₄: 4 bp + 1 lp; lone pair equatorial → see-saw → Statement II true"],
    answer="D", ncert=f"{REF3}, VSEPR theory: shapes of SF₄ and ClF₃", seconds=40)

add("VSEPR shapes", A, "direct",
    "Which of the following pairs of species are isostructural (have the same shape)?",
    Opts("D", "NH₄⁺ and BF₄⁻", ["SF₄ and XeF₄", "H₂O and BeCl₂", "PCl₅ and IF₅"]),
    "Isostructural species from VSEPR theory",
    "NH₄⁺ and BF₄⁻ each have four bond pairs and no lone pair around the central atom, so both are "
    "tetrahedral.",
    ["NH₄⁺: 4 bp, 0 lp → tetrahedral; BF₄⁻: 4 bp, 0 lp → tetrahedral",
     "SF₄ see-saw vs XeF₄ square planar; H₂O bent vs BeCl₂ linear; PCl₅ trigonal bipyramidal vs IF₅ square "
     "pyramidal"],
    why="In each of the other pairs the numbers of lone pairs differ, so the shapes differ: see-saw and square "
        "planar, bent and linear, trigonal bipyramidal and square pyramidal.",
    ncert=f"{REF3}, VSEPR theory", seconds=45)

# ==================================================================== 4. Chemical Thermodynamics
topic("Chemical Thermodynamics")
REF4 = f"{C11}, 'Thermodynamics'"

assert 1664 / 4 == 416 and 1664 / 2 == 832 and close(1664 / 3, 554.7)
add("Hess's law and enthalpies", B, "numerical",
    "The enthalpy of atomisation of methane, CH₄(g) → C(g) + 4H(g), is 1664 kJ mol⁻¹. The mean C–H bond "
    "enthalpy in methane is:",
    Opts("B", "416 kJ mol⁻¹", ["1664 kJ mol⁻¹", "832 kJ mol⁻¹", "554.7 kJ mol⁻¹"]),
    "Mean bond enthalpy",
    "Atomising one mole of CH₄ breaks four moles of C–H bonds. The four bonds are broken in steps that need "
    "different energies, so the mean value is the total divided by four.",
    ["Bonds broken per CH₄ = 4 C–H", "Mean C–H bond enthalpy = 1664 / 4 = 416 kJ mol⁻¹"],
    why="1664 kJ mol⁻¹ is the enthalpy for breaking all four bonds. 832 and 554.7 kJ mol⁻¹ divide by 2 and 3 "
        "instead of 4.",
    ncert=f"{REF4}, enthalpies for different types of reactions: bond enthalpy", seconds=25, checked=True)

add("First law, work and enthalpy", B, "direct",
    "Which of the following is an extensive property?",
    Opts("C", "Heat capacity", ["Molar heat capacity", "Density", "Specific heat capacity"]),
    "Extensive and intensive properties",
    "An extensive property depends on the amount of matter in the system. The heat capacity of a sample "
    "doubles when the sample is doubled. Molar heat capacity, specific heat capacity (per unit mass) and "
    "density are ratios of two extensive properties and do not depend on the amount, so they are intensive.",
    ["Heat capacity C ∝ amount of matter → extensive",
     "C/n, C/m and m/V are independent of the amount → intensive"],
    why="Molar heat capacity, density and specific heat capacity do not change with the size of the sample.",
    ncert=f"{REF4}, extensive and intensive properties", seconds=25)

add("First law, work and enthalpy", B, "statement_pair",
    sp("A closed system can exchange matter, but not energy, with its surroundings.",
       "An open system can exchange neither energy nor matter with its surroundings."),
    SP_, "Types of systems",
    "A closed system exchanges energy but not matter with its surroundings (for example a reaction in a "
    "closed vessel). An open system exchanges both energy and matter. A system that exchanges neither is "
    "isolated. Both statements are false.",
    ["Closed: energy yes, matter no → Statement I false", "Open: both energy and matter → Statement II false"],
    answer="B", ncert=f"{REF4}, the system and the surroundings: types of the system", seconds=25)

q_rel = 10.0 * 8.85
du = -q_rel / (1.6 / 16)
assert close(du, -885) and close(-q_rel, -88.5) and close(-q_rel / 1.6, -55.3)
add("First law, work and enthalpy", I, "numerical",
    "1.6 g of methane is burnt completely in excess oxygen in a bomb calorimeter (constant volume). The heat "
    "capacity of the calorimeter is 10.0 kJ K⁻¹ and its temperature rises by 8.85 K. The internal energy "
    "change of combustion of methane, ΔcU, is (C = 12, H = 1):",
    Opts("B", "−885 kJ mol⁻¹", ["−88.5 kJ mol⁻¹", "+885 kJ mol⁻¹", "−55.3 kJ mol⁻¹"]),
    "Bomb calorimetry: q at constant volume equals ΔU",
    "In a bomb calorimeter no expansion work is done, so the heat released at constant volume is ΔU. The "
    "heat absorbed by the calorimeter is C × ΔT; this heat came from the reaction, so ΔU is negative.",
    ["Heat absorbed by calorimeter = 10.0 × 8.85 = 88.5 kJ", "Moles of CH₄ = 1.6 / 16 = 0.10 mol",
     "ΔcU = −88.5 / 0.10 = −885 kJ mol⁻¹"],
    why="−88.5 kJ mol⁻¹ is the heat for 0.10 mol, not per mole. +885 has the wrong sign for a reaction that "
        "gives out heat. −55.3 divides by the mass (1.6 g) instead of the moles.",
    ncert=f"{REF4}, measurement of ΔU and ΔH: calorimetry", seconds=60, checked=True)

ds_surr = -(-60e3) / 300
assert ds_surr == 200 and ds_surr + (-150) == 50 and -150 - 200 == -350 and 150 + 200 == 350
add("Entropy and Gibbs energy", I, "numerical",
    "For a reaction at 300 K and constant pressure, ΔH = −60 kJ mol⁻¹ and ΔS(system) = −150 J K⁻¹ mol⁻¹. "
    "Taking the heat given out to be absorbed by the surroundings at 300 K, the total entropy change "
    "(system + surroundings) is:",
    Opts("A", "+50 J K⁻¹ mol⁻¹", ["−350 J K⁻¹ mol⁻¹", "+350 J K⁻¹ mol⁻¹", "−150 J K⁻¹ mol⁻¹"]),
    "Total entropy change and spontaneity",
    "The surroundings gain the heat released by the system, so ΔS(surroundings) = −ΔH(system)/T. Add this to "
    "ΔS(system). A positive total means the process is spontaneous.",
    ["ΔS(surr) = −(−60 000 J) / 300 K = +200 J K⁻¹ mol⁻¹", "ΔS(total) = −150 + 200 = +50 J K⁻¹ mol⁻¹",
     "ΔS(total) > 0 → spontaneous at 300 K"],
    why="−350 takes ΔS(surr) as −200 (sign error). +350 changes the sign of ΔS(system). −150 ignores the "
        "surroundings.",
    ncert=f"{REF4}, spontaneity: entropy and spontaneity", seconds=60, checked=True)

add("First law, work and enthalpy", I, "assertion_reason",
    ar("Although heat (q) and work (w) are not state functions, their sum q + w is a state function.",
       "q + w equals ΔU, and internal energy U is a state function, so ΔU depends only on the initial and "
       "final states of the system."),
    AR_, "First law of thermodynamics",
    "q and w depend on the path followed. By the first law, ΔU = q + w, and U is a state function, so the "
    "sum q + w has the same value for every path between the same two states. R explains A.",
    ["ΔU = q + w (first law)", "U is a state function → ΔU path-independent", "So q + w is path-independent"],
    answer="A", ncert=f"{REF4}, the first law of thermodynamics", seconds=35)

add("Entropy and Gibbs energy", I, "match_list",
    lists("Match List-I (signs of ΔH and ΔS of a reaction, both independent of temperature) with List-II "
          "(spontaneity).",
          ["ΔH negative, ΔS positive", "ΔH positive, ΔS negative", "ΔH negative, ΔS negative",
           "ΔH positive, ΔS positive"],
          ["Spontaneous only at high temperature", "Spontaneous at all temperatures",
           "Non-spontaneous at all temperatures", "Spontaneous only at low temperature"]),
    match("D", M("II III IV I"), [M("II III I IV"), M("III II IV I"), M("II IV III I")]),
    "Effect of temperature on spontaneity, ΔG = ΔH − TΔS",
    "ΔG = ΔH − TΔS must be negative for spontaneity. With ΔH < 0 and ΔS > 0 both terms favour it. With ΔH > 0 "
    "and ΔS < 0 neither does. When the two terms oppose each other, temperature decides: −TΔS dominates at "
    "high T, ΔH at low T.",
    ["ΔH −, ΔS + → ΔG always negative → II", "ΔH +, ΔS − → ΔG always positive → III",
     "ΔH −, ΔS − → ΔG negative only when |ΔH| > T|ΔS| (low T) → IV",
     "ΔH +, ΔS + → ΔG negative only when TΔS > ΔH (high T) → I"],
    why="The other codes swap the low- and high-temperature cases, or the 'all temperatures' cases.",
    ncert=f"{REF4}, Gibbs energy and spontaneity: effect of temperature", seconds=50)

add("Hess's law and enthalpies", I, "multi_statement",
    ms("Which of the following statements are correct?",
       ["The standard enthalpy of formation of a compound refers to the formation of one mole of it from its "
        "elements in their most stable states.",
        "The standard enthalpy of formation of diamond is zero.",
        "Combustion reactions are exothermic.",
        "For a diatomic molecule such as H₂, the enthalpy of atomisation equals the bond dissociation "
        "enthalpy.",
        "At a given temperature, ΔsubH = ΔfusH + ΔvapH."]),
    multi("B", {"a": True, "b": False, "c": True, "d": True, "e": True},
          ["(a), (b), (c) and (d) only", "(a), (b), (d) and (e) only", "(c), (d) and (e) only"]),
    "Enthalpies of formation, combustion, atomisation and sublimation",
    "The most stable form of carbon is graphite, so ΔfH° of graphite (not diamond) is zero. Combustion "
    "reactions release heat. Atomising H₂ breaks just one H–H bond. Sublimation can be done as fusion followed "
    "by vaporisation, so by Hess's law ΔsubH = ΔfusH + ΔvapH.",
    ["(a) True", "(b) False: diamond is not the reference state of carbon", "(c) True", "(d) True",
     "(e) True"],
    why="Any option with (b) is wrong, and (a) must appear.",
    ncert=f"{REF4}, standard enthalpy of formation; enthalpies of combustion, atomisation and phase "
          "transformation", seconds=60)

dsol = 750 + (-730)
assert dsol == 20 and close(0.2 * dsol, 4.0) and close(0.2 * (750 + 730), 296)
add("Hess's law and enthalpies", A, "numerical",
    "For a salt MX, the lattice enthalpy (MX(s) → M⁺(g) + X⁻(g)) is +750 kJ mol⁻¹ and the enthalpy of "
    "hydration of its gaseous ions (M⁺(g) + X⁻(g) → M⁺(aq) + X⁻(aq)) is −730 kJ mol⁻¹. When 0.20 mol of MX "
    "dissolves in a large amount of water:",
    Opts("C", "4.0 kJ of heat is absorbed", ["4.0 kJ of heat is released", "296 kJ of heat is absorbed",
                                             "20 kJ of heat is absorbed"]),
    "Enthalpy of solution from lattice and hydration enthalpies",
    "Dissolution can be imagined as breaking the lattice into gaseous ions and then hydrating them, so by "
    "Hess's law ΔsolH = ΔlatticeH + ΔhydH.",
    ["ΔsolH = 750 + (−730) = +20 kJ mol⁻¹", "For 0.20 mol: 0.20 × 20 = 4.0 kJ",
     "Positive ΔsolH → heat is absorbed (the solution cools)"],
    why="'Released' has the wrong sign: the lattice enthalpy outweighs the hydration enthalpy. 296 kJ adds "
        "the magnitudes. 20 kJ is the value per mole, not for 0.20 mol.",
    ncert=f"{REF4}, enthalpy of solution", seconds=70, checked=True)

w_ad = 2 * 12.5 * (280 - 300)
assert w_ad == -500 and close(2 * (12.5 + 8.314) * 20, 832.6)
add("First law, work and enthalpy", A, "numerical",
    "2 mol of a monatomic ideal gas (C_v,m = 12.5 J K⁻¹ mol⁻¹) expands adiabatically, and its temperature "
    "falls from 300 K to 280 K. The work done on the gas is:",
    Opts("A", "−500 J", ["+500 J", "0 J", "−833 J"]),
    "Adiabatic process: w = ΔU",
    "For an adiabatic process q = 0, so the first law gives ΔU = w. For an ideal gas ΔU = n C_v,m ΔT.",
    ["ΔU = 2 × 12.5 × (280 − 300) = −500 J", "q = 0 → w = ΔU = −500 J",
     "The gas does 500 J of work on the surroundings; its temperature falls"],
    why="+500 J has the wrong sign: an expanding gas does work, so work done on it is negative. 0 J confuses "
        "q = 0 with w = 0. −833 J uses C_p,m (= C_v,m + R) instead of C_v,m.",
    ncert=f"{REF4}, first law: work; heat capacity: relation between C_p and C_v", seconds=70, checked=True)

add("Gibbs energy and K", A, "statement_pair",
    sp("For the process H₂O(l) → H₂O(g) at 373 K and 1 atm, the entropy change of the system is negative.",
       "For the same process at 373 K and 1 atm, ΔG = 0."),
    SP_, "Phase equilibrium and Gibbs energy",
    "Vaporisation turns a liquid into a much more disordered gas, so ΔS(system) is positive: Statement I is "
    "false. At 373 K and 1 atm liquid water and steam are in equilibrium (the normal boiling point), and for "
    "a process at equilibrium ΔG = 0: Statement II is true.",
    ["Liquid → gas: disorder increases → ΔS > 0 → Statement I false",
     "373 K, 1 atm: liquid ⇌ vapour equilibrium → ΔG = 0 → Statement II true"],
    answer="D", ncert=f"{REF4}, entropy and spontaneity; Gibbs energy change and equilibrium", seconds=35)

# ==================================================================== 5. Solutions
topic("Solutions")
REF5 = f"{C12}, 'Solutions'"

x_eth = (46 / 46) / (46 / 46 + 90 / 18)
assert close(x_eth, 0.167, 0.01) and close(1 / 5, 0.20) and close(46 / 136, 0.338, 0.01)
add("Concentration terms", B, "numerical",
    "46 g of ethanol (C₂H₅OH) is mixed with 90 g of water. The mole fraction of ethanol in the solution is "
    "(H = 1, C = 12, O = 16):",
    Opts("D", "0.167", ["0.20", "0.338", "0.833"]),
    "Mole fraction",
    "Mole fraction of a component = its moles / total moles of all components.",
    ["Moles of ethanol = 46 / 46 = 1 mol", "Moles of water = 90 / 18 = 5 mol",
     "x(ethanol) = 1 / (1 + 5) = 0.167"],
    why="0.20 is the mole ratio ethanol : water (1/5), not the mole fraction. 0.338 is the mass fraction "
        "(46/136). 0.833 is the mole fraction of water.",
    ncert=f"{REF5}, expressing concentration of solutions: mole fraction", seconds=35, checked=True)

add("Colligative properties", B, "direct",
    "Which of the following is a colligative property of a dilute solution of a non-volatile solute?",
    Opts("B", "Osmotic pressure", ["Viscosity", "Surface tension", "Optical rotation"]),
    "Colligative properties",
    "Colligative properties depend only on the number of solute particles, not on their nature. They are the "
    "relative lowering of vapour pressure, elevation of boiling point, depression of freezing point and "
    "osmotic pressure.",
    ["The four colligative properties include osmotic pressure"],
    why="Viscosity, surface tension and optical rotation depend on the nature of the solute, not only on the "
        "number of solute particles.",
    ncert=f"{REF5}, colligative properties and determination of molar mass", seconds=20)

add("Concentration terms", B, "statement_pair",
    sp("The mass percentage of a component of a solution changes with temperature.",
       "The mole fraction of a component of a solution changes with temperature."),
    SP_, "Temperature dependence of concentration terms",
    "Mass percentage, mole fraction and molality are defined through masses or moles only, which do not "
    "change with temperature. Only terms based on volume, such as molarity, change with temperature. Both "
    "statements are false.",
    ["Mass % uses masses only → independent of T → Statement I false",
     "Mole fraction uses moles only → independent of T → Statement II false"],
    answer="B", ncert=f"{REF5}, expressing concentration of solutions", seconds=25)

m_naoh = (20 / 40) / 0.080
assert close(m_naoh, 6.25) and close((20 / 40) / 0.100, 5.0) and close((20 / 40) / 0.80, 0.625)
add("Concentration terms", I, "numerical",
    "An aqueous solution of NaOH is 20% by mass. Its molality is (Na = 23, O = 16, H = 1):",
    Opts("C", "6.25 m", ["5.00 m", "0.625 m", "0.50 m"]),
    "Molality from mass percentage",
    "Take 100 g of solution: it contains 20 g of NaOH and 80 g of water. Molality = moles of solute per "
    "kilogram of solvent.",
    ["Moles of NaOH = 20 / 40 = 0.50 mol", "Mass of solvent = 100 − 20 = 80 g = 0.080 kg",
     "Molality = 0.50 / 0.080 = 6.25 mol kg⁻¹"],
    why="5.00 m divides by the mass of the solution (100 g) instead of the solvent. 0.625 m converts 80 g to "
        "0.80 kg. 0.50 m is just the number of moles of NaOH, not divided by the mass of solvent.",
    ncert=f"{REF5}, expressing concentration of solutions: molality", seconds=50, checked=True)

n1 = 39 / 78
n2 = (8 / 640) * n1
M2 = 2.0 / n2
assert close(M2, 320) and close(2.0 / ((8 / 640) * 2), 80) and close(2.0 / ((8 / 640) * 39), 4.10, 0.01)
assert close(2.0 / ((8 / 640) * 1), 160)
add("Raoult's law and ideal solutions", I, "numerical",
    "2.0 g of a non-volatile, non-electrolyte solute is dissolved in 39 g of benzene (C₆H₆). The vapour "
    "pressure of benzene falls from 640 mm Hg to 632 mm Hg at the same temperature. Treating the solution "
    "as dilute (moles of solute much smaller than moles of benzene), the molar mass of the solute is "
    "(C = 12, H = 1):",
    Opts("D", "320 g mol⁻¹", ["80 g mol⁻¹", "4.10 g mol⁻¹", "160 g mol⁻¹"]),
    "Relative lowering of vapour pressure",
    "For a dilute solution, (p° − p)/p° = n₂/n₁, where n₂ and n₁ are the moles of solute and solvent.",
    ["(p° − p)/p° = (640 − 632)/640 = 0.0125", "n₁ = 39 / 78 = 0.50 mol of benzene",
     "n₂ = 0.0125 × 0.50 = 6.25 × 10⁻³ mol", "M₂ = 2.0 / 6.25 × 10⁻³ = 320 g mol⁻¹"],
    why="80 g mol⁻¹ inverts the benzene mole calculation (78/39 = 2 mol). 4.10 g mol⁻¹ uses the mass of "
        "benzene (39) in place of its moles. 160 g mol⁻¹ takes the benzene as 1 mol.",
    ncert=f"{REF5}, relative lowering of vapour pressure", seconds=80, checked=True)

add("Colligative properties", I, "assertion_reason",
    ar("A 0.1 m aqueous solution of sucrose freezes below 0 °C, the freezing point of pure water.",
       "A non-volatile solute lowers the vapour pressure of the solvent, so the vapour pressure of the "
       "solution becomes equal to that of the solid solvent only at a lower temperature."),
    AR_, "Depression of freezing point",
    "At the freezing point the vapour pressure of the liquid equals that of the solid. Dissolving sucrose "
    "lowers the vapour pressure of the liquid, so the two vapour pressures become equal only at a lower "
    "temperature: the solution freezes below 0 °C. R gives the reason for A.",
    ["Freezing point: p(liquid) = p(solid)", "Solute lowers p(liquid) → equality reached at a lower T",
     "R explains A"],
    answer="A", ncert=f"{REF5}, depression of freezing point", seconds=40)

add("Colligative properties", I, "match_list",
    lists("Match List-I (colligative property of a dilute solution of a non-volatile non-electrolyte) with "
          "List-II (its expression). (x₂ = mole fraction of solute, m = molality, C = molarity)",
          ["Relative lowering of vapour pressure", "Elevation of boiling point", "Depression of freezing point",
           "Osmotic pressure"],
          ["K_f × m", "C R T", "x₂", "K_b × m"]),
    match("B", M("III IV I II"), [M("III I IV II"), M("II IV I III"), M("IV III I II")]),
    "Expressions for the colligative properties",
    "Raoult's law gives (p° − p)/p° = x₂. ΔT_b = K_b m and ΔT_f = K_f m. The osmotic pressure is π = CRT.",
    ["Relative lowering → x₂ → III", "Elevation of b.p. → K_b m → IV", "Depression of f.p. → K_f m → I",
     "Osmotic pressure → CRT → II"],
    why="The other codes interchange K_b with K_f, or the vapour-pressure and osmotic-pressure expressions.",
    ncert=f"{REF5}, colligative properties", seconds=35)

i_f = 2.706 / (0.1 * 0.082 * 300)
alpha = i_f - 1
assert close(i_f, 1.10) and close(alpha, 0.10) and close((i_f - 1) / 2, 0.05)
add("van't Hoff factor", A, "numerical",
    "A 0.10 M aqueous solution of a weak electrolyte AB, which dissociates as AB ⇌ A⁺ + B⁻, has an osmotic "
    "pressure of 2.706 atm at 300 K. The degree of dissociation of AB is (R = 0.082 L atm K⁻¹ mol⁻¹):",
    Opts("A", "0.10", ["0.90", "1.10", "0.05"]),
    "van't Hoff factor and degree of dissociation",
    "π = iCRT gives the van't Hoff factor i. For AB → A⁺ + B⁻, one formula unit gives two particles, so "
    "i = 1 + α.",
    ["CRT = 0.10 × 0.082 × 300 = 2.46 atm", "i = 2.706 / 2.46 = 1.10", "i = 1 + α → α = 0.10"],
    why="0.90 is the fraction left undissociated (1 − α). 1.10 is the van't Hoff factor, not α. 0.05 uses "
        "i = 1 + 2α, as for a solute giving three ions.",
    ncert=f"{REF5}, abnormal molar masses: van't Hoff factor", seconds=75, checked=True)

slope = (450 - 550) / (0.75 - 0.25)
pB0 = 550 - slope * 0.25
pA0 = pB0 + slope
assert pB0 == 600 and pA0 == 400 and pB0 + slope * 0.5 == 500
add("Raoult's law and ideal solutions", A, "numerical",
    "Liquids A and B form an ideal solution. At a certain temperature, a solution with mole fraction of A = 0.25 "
    "has a total vapour pressure of 550 mm Hg, and a solution with mole fraction of A = 0.75 has a total "
    "vapour pressure of 450 mm Hg. The vapour pressure of pure A at this temperature is:",
    Opts("C", "400 mm Hg", ["600 mm Hg", "500 mm Hg", "200 mm Hg"]),
    "Raoult's law for two volatile components",
    "For an ideal solution p(total) = p_A° x_A + p_B° (1 − x_A) = p_B° + (p_A° − p_B°) x_A, a straight line in x_A. "
    "Two data points give both pure-component vapour pressures.",
    ["Slope (p_A° − p_B°) = (450 − 550)/(0.75 − 0.25) = −200 mm Hg",
     "p_B° = 550 − (−200)(0.25) = 600 mm Hg", "p_A° = 600 − 200 = 400 mm Hg",
     "Check: x_A = 0.75 → 600 − 150 = 450 mm Hg"],
    why="600 mm Hg is the vapour pressure of pure B. 500 mm Hg is the total pressure at x_A = 0.5. 200 mm Hg is "
        "the magnitude of the slope.",
    ncert=f"{REF5}, vapour pressure of liquid–liquid solutions: Raoult's law", seconds=90, checked=True)

add("Colligative properties", A, "multi_statement",
    ms("Which of the following statements are correct?",
       ["Two solutions having the same osmotic pressure at a given temperature are called isotonic solutions.",
        "A 0.9% (mass/volume) sodium chloride solution is isotonic with the fluid inside blood cells.",
        "Red blood cells placed in a solution containing more than 0.9% (mass/volume) NaCl swell up.",
        "The molal elevation constant K_b depends on the nature of the solvent.",
        "The depression of the freezing point of a dilute solution depends on the chemical nature of the "
        "solute."]),
    multi("D", {"a": True, "b": True, "c": False, "d": True, "e": False},
          ["(a), (b) and (c) only", "(b), (c), (d) and (e) only", "(a), (d) and (e) only"]),
    "Osmosis, isotonic solutions and colligative constants",
    "Normal saline (0.9% NaCl) is isotonic with blood cell fluid. In a more concentrated (hypertonic) NaCl "
    "solution, water flows out of the cells and they shrink. K_b and K_f are properties of the solvent. "
    "Depression of freezing point is colligative: it depends on the number, not the nature, of solute "
    "particles.",
    ["(a) True", "(b) True", "(c) False: cells shrink in a hypertonic solution", "(d) True",
     "(e) False: colligative properties do not depend on the nature of the solute"],
    why="Options with (c) or (e) are wrong.",
    ncert=f"{REF5}, osmosis and osmotic pressure; elevation of boiling point", seconds=60)

# ==================================================================== 6. Equilibrium
topic("Equilibrium")
REF6 = f"{C11}, 'Equilibrium'"

add("Acids, bases and pH", B, "direct",
    "The conjugate acid of ammonia (NH₃) is:",
    Opts("B", "NH₄⁺", ["NH₂⁻", "N³⁻", "H₃O⁺"]),
    "Brønsted–Lowry conjugate acid–base pairs",
    "A conjugate acid is formed when a base accepts a proton. NH₃ + H⁺ → NH₄⁺, so NH₄⁺ is the conjugate acid "
    "of NH₃.",
    ["Base + H⁺ → conjugate acid", "NH₃ + H⁺ → NH₄⁺"],
    why="NH₂⁻ is the conjugate base of NH₃ (NH₃ minus a proton). N³⁻ is the nitride ion. H₃O⁺ is the conjugate "
        "acid of water.",
    ncert=f"{REF6}, Brönsted–Lowry acids and bases", seconds=20)

x_gas = 2.0 / 40e3
assert close(x_gas, 5.0e-5) and close(40e3 / 2.0, 2.0e4) and close(2.0 / 40, 5.0e-2)
add("Physical equilibria and Henry's law", B, "numerical",
    "The Henry's law constant (K_H) of a gas X in water at 298 K is 40 kbar. The mole fraction of X dissolved "
    "in water when its partial pressure above the water is 2.0 bar at 298 K is:",
    Opts("C", "5.0 × 10⁻⁵", ["2.0 × 10⁴", "80", "5.0 × 10⁻²"]),
    "Henry's law, p = K_H x",
    "Henry's law states that the partial pressure of a gas in the vapour phase is proportional to its mole "
    "fraction in the solution: p = K_H x, so x = p / K_H. Both pressures must be in the same unit.",
    ["K_H = 40 kbar = 4.0 × 10⁴ bar", "x = 2.0 / (4.0 × 10⁴) = 5.0 × 10⁻⁵"],
    why="2.0 × 10⁴ inverts the ratio (K_H/p). 80 multiplies p and K_H. 5.0 × 10⁻² leaves K_H in kbar.",
    ncert=f"{C12}, 'Solutions', solubility of a gas in a liquid: Henry's law", seconds=35, checked=True)

add("Physical equilibria and Henry's law", B, "statement_pair",
    sp("The solubility of gases in liquids decreases with rise in temperature.",
       "At its normal boiling point, the vapour pressure of a liquid equals 1.013 bar (1 atm)."),
    SP_, "Physical equilibria: gases in liquids and liquid–vapour equilibrium",
    "Dissolving a gas is exothermic, and gases come out of solution on heating, so their solubility falls "
    "with rise in temperature: Statement I is true. The normal boiling point is the temperature at which the "
    "vapour pressure of the liquid equals the atmospheric pressure of 1.013 bar: Statement II is true.",
    ["Gas solubility falls as T rises → Statement I true",
     "Normal boiling point: vapour pressure = 1.013 bar → Statement II true"],
    answer="A", ncert=f"{REF6}, equilibrium in physical processes", seconds=30)

add("Physical equilibria and Henry's law", B, "match_list",
    lists("Match List-I (type of physical equilibrium) with List-II (example).",
          ["Liquid ⇌ vapour", "Solid ⇌ liquid", "Solid ⇌ vapour", "Gas ⇌ gas dissolved in a liquid"],
          ["Ice and water at 273 K and 1 atm", "Carbon dioxide in a sealed bottle of soda water",
           "Water and water vapour in a closed vessel at constant temperature",
           "Solid iodine and iodine vapour in a closed vessel"]),
    match("A", M("III I IV II"), [M("I III IV II"), M("III I II IV"), M("III IV I II")]),
    "Equilibria in physical processes",
    "Each physical equilibrium is a dynamic balance between two phases or between a dissolved and an "
    "undissolved form of a substance.",
    ["Liquid ⇌ vapour: water in a closed vessel → III", "Solid ⇌ liquid: ice and water at 273 K → I",
     "Solid ⇌ vapour: sublimation of iodine → IV", "Gas ⇌ dissolved gas: CO₂ in soda water → II"],
    why="The other codes swap the liquid–vapour and solid–liquid cases, or the sublimation and dissolved-gas "
        "cases.",
    ncert=f"{REF6}, equilibrium in physical processes", seconds=30)

add("Physical equilibria and Henry's law", B, "assertion_reason",
    ar("When water is kept in a closed vessel at constant temperature, the pressure of its vapour rises at "
       "first and then becomes constant.",
       "At equilibrium, both evaporation and condensation stop."),
    AR_, "Dynamic nature of equilibrium",
    "At first evaporation is faster than condensation, so the vapour pressure rises. Soon the rates become "
    "equal and the vapour pressure stays constant: A is true. At equilibrium the two processes do not stop; "
    "they go on at equal rates (dynamic equilibrium), so R is false.",
    ["Rate of evaporation = rate of condensation → constant vapour pressure (A true)",
     "Both processes continue → equilibrium is dynamic (R false)"],
    answer="C", ncert=f"{REF6}, equilibrium in physical processes: liquid–vapour equilibrium", seconds=30)

kp = 0.3 * 0.3
assert close(kp, 0.09) and close(0.6 ** 2, 0.36) and close(0.15 ** 2, 0.0225)
add("Kp, Kc and Le Chatelier", I, "numerical",
    "Solid NH₄HS is placed in an evacuated flask and allowed to reach equilibrium: NH₄HS(s) ⇌ NH₃(g) + H₂S(g). "
    "The total pressure at equilibrium is 0.60 atm. K_p for the equilibrium is:",
    Opts("C", "0.09 atm²", ["0.36 atm²", "0.0225 atm²", "0.30 atm²"]),
    "Heterogeneous equilibrium: K_p involves only the gases",
    "The solid does not appear in K_p. NH₃ and H₂S are formed in equal amounts, so each has half the total "
    "pressure.",
    ["p(NH₃) = p(H₂S) = 0.60 / 2 = 0.30 atm", "K_p = p(NH₃) × p(H₂S) = 0.30 × 0.30 = 0.09 atm²"],
    why="0.36 atm² squares the total pressure. 0.0225 atm² halves each partial pressure again (0.15 atm). "
        "0.30 atm² gives just one partial pressure.",
    ncert=f"{REF6}, heterogeneous equilibria", seconds=45, checked=True)

ka = 1.8e-5
alpha_ci = ka / 0.1
assert close(alpha_ci, 1.8e-4) and close(math.sqrt(ka / 0.1), 1.34e-2, 0.01) and close(math.sqrt(ka), 4.24e-3, 0.01)
add("Acids, bases and pH", I, "numerical",
    "The degree of ionisation of acetic acid in a solution that is 0.1 M in CH₃COOH and 0.1 M in HCl is "
    "(K_a of CH₃COOH = 1.8 × 10⁻⁵):",
    Opts("D", "1.8 × 10⁻⁴", ["1.34 × 10⁻²", "1.8 × 10⁻⁵", "4.24 × 10⁻³"]),
    "Common ion effect on the ionisation of a weak acid",
    "HCl ionises completely and fixes [H⁺] ≈ 0.1 M. This common ion suppresses the ionisation of acetic acid. "
    "With [CH₃COOH] ≈ 0.1 M and [CH₃COO⁻] = 0.1α, K_a = [H⁺][CH₃COO⁻]/[CH₃COOH] = (0.1)(0.1α)/0.1.",
    ["[H⁺] ≈ 0.1 M (from HCl)", "K_a = 0.1 × α → α = 1.8 × 10⁻⁵ / 0.1 = 1.8 × 10⁻⁴"],
    why="1.34 × 10⁻² is √(K_a/c), the value without HCl. 1.8 × 10⁻⁵ is K_a itself. 4.24 × 10⁻³ is √K_a.",
    ncert=f"{REF6}, common ion effect in the ionization of acids and bases", seconds=60, checked=True)

h_mix = (1e-2 + 1e-4) / 2
ph_mix = -math.log10(h_mix)
assert close(ph_mix, 2.30, 0.002) and close(-math.log10(2e-2), 1.70, 0.003)
add("Acids, bases and pH", I, "numerical",
    "Equal volumes of two solutions of HCl, of pH 2 and pH 4, are mixed. The pH of the mixture is "
    "(log 5.05 = 0.703):",
    Opts("B", "2.30", ["3.00", "2.00", "1.70"]),
    "pH of a mixture of strong acids",
    "pH values cannot be averaged. Find the moles of H⁺ from each solution, add them, and divide by the total "
    "volume.",
    ["[H⁺] = 10⁻² M and 10⁻⁴ M; equal volumes V", "[H⁺] in mixture = (10⁻² + 10⁻⁴) V / 2V = 5.05 × 10⁻³ M",
     "pH = 3 − log 5.05 = 3 − 0.703 = 2.30"],
    why="3.00 averages the two pH values. 2.00 ignores the dilution on mixing. 1.70 doubles [H⁺] instead of "
        "halving it.",
    ncert=f"{REF6}, the pH scale", seconds=60, checked=True)

add("Acids, bases and pH", I, "direct",
    "Which of the following species can act both as a Brønsted acid and as a Brønsted base in water?",
    Opts("C", "HCO₃⁻", ["CO₃²⁻", "NH₄⁺", "Cl⁻"]),
    "Amphiprotic species",
    "HCO₃⁻ can donate a proton (giving CO₃²⁻) and can accept a proton (giving H₂CO₃), so it acts both as an "
    "acid and as a base.",
    ["HCO₃⁻ → CO₃²⁻ + H⁺ (acid)", "HCO₃⁻ + H⁺ → H₂CO₃ (base)"],
    why="CO₃²⁻ has no proton to give, so it is only a base. NH₄⁺ can only give a proton. Cl⁻ has no proton "
        "to donate.",
    ncert=f"{REF6}, Brönsted–Lowry acids and bases", seconds=30)

add("Hydrolysis and buffers", I, "assertion_reason",
    ar("A solution containing CH₃COOH and CH₃COONa resists a change in pH when a small amount of HCl is added "
       "to it.",
       "The added H⁺ ions combine with CH₃COO⁻ ions to form weakly ionised CH₃COOH molecules."),
    AR_, "Action of an acidic buffer",
    "The acetate ions supplied by CH₃COONa remove added H⁺ as un-ionised acetic acid, so [H⁺] hardly changes "
    "and the pH stays almost constant. R is the mechanism by which the buffer works, so it explains A.",
    ["CH₃COO⁻ + H⁺ → CH₃COOH (weak acid)", "Free H⁺ hardly increases → pH nearly constant", "R explains A"],
    answer="A", ncert=f"{REF6}, buffer solutions", seconds=35)

add("Kp, Kc and Le Chatelier", I, "match_list",
    lists("For the equilibrium N₂O₄(g) ⇌ 2NO₂(g), ΔH > 0, set up in a closed vessel, match List-I (change made) "
          "with List-II (effect).",
          ["Temperature is raised", "Volume is decreased at constant temperature",
           "A catalyst is added", "More N₂O₄ is added at constant volume and temperature"],
          ["No shift; K unchanged", "Shifts forward; K unchanged", "Shifts forward; K increases",
           "Shifts backward; K unchanged"]),
    match("A", M("III IV I II"), [M("II IV I III"), M("III II I IV"), M("III IV II I")]),
    "Le Chatelier's principle and the equilibrium constant",
    "Only a change of temperature changes K. For an endothermic forward reaction, raising T increases K and "
    "shifts the equilibrium forward. Decreasing the volume raises the pressure, favouring the side with fewer "
    "gas moles (N₂O₄). A catalyst speeds up both directions equally. Adding a reactant makes Q < K, so the "
    "reaction shifts forward with K unchanged.",
    ["Raise T (endothermic) → forward, K increases → III", "Decrease V → towards fewer moles (backward), K "
     "same → IV", "Catalyst → no shift → I", "Add N₂O₄ → forward, K same → II"],
    why="The other codes either let K change on adding N₂O₄ or a catalyst, or move the equilibrium forward on "
        "compression.",
    ncert=f"{REF6}, factors affecting equilibria", seconds=60)

add("Kp, Kc and Le Chatelier", I, "multi_statement",
    ms("Which of the following statements are correct?",
       ["The equilibrium constant K_c of a reaction depends on temperature.",
        "For a gaseous reaction in which Δn(gas) = −1, K_p = K_c (RT)⁻¹.",
        "The concentrations of pure solids and pure liquids appear in the expression for K_c.",
        "K_c for N₂(g) + 3H₂(g) ⇌ 2NH₃(g) has the unit L² mol⁻².",
        "K_c for a reverse reaction has the same value as K_c for the forward reaction."]),
    multi("D", {"a": True, "b": True, "c": False, "d": True, "e": False},
          ["(a), (b), (c) and (d) only", "(b), (d) and (e) only", "(a), (c) and (e) only"]),
    "Equilibrium constants: K_p, K_c and their units",
    "K_c changes with temperature. K_p = K_c (RT)^Δn, so Δn = −1 gives K_c (RT)⁻¹. Pure solids and liquids have "
    "constant concentrations and are left out of K_c. For the ammonia equilibrium K_c = [NH₃]²/([N₂][H₂]³) has "
    "the unit (mol L⁻¹)⁻² = L² mol⁻². The reverse reaction has K_c' = 1/K_c.",
    ["(a) True", "(b) True: (RT)^Δn with Δn = −1", "(c) False: they are omitted", "(d) True: (mol L⁻¹)^(2 − 4)",
     "(e) False: K_c' = 1/K_c"],
    why="Any option with (c) or (e) is wrong.",
    ncert=f"{REF6}, equilibrium constant; relationship between K_p and K_c; heterogeneous equilibria",
    seconds=70)

oh = math.sqrt(1.0e-11 / 0.1)
assert close(oh, 1e-5) and close(14 + math.log10(oh), 9.0)
assert close(14 + math.log10(1.0e-11 / 0.1), 4.0) and close(14 + math.log10(math.sqrt(1.0e-11)), 8.5, 0.002)
add("Solubility product", A, "numerical",
    "A solution is 0.10 M in Mg²⁺ ions. The pH at which Mg(OH)₂ just begins to precipitate when NaOH is added "
    "slowly at 298 K is (K_sp of Mg(OH)₂ = 1.0 × 10⁻¹¹, K_w = 1.0 × 10⁻¹⁴; ignore the change in volume):",
    Opts("B", "9.0", ["5.0", "4.0", "8.5"]),
    "Solubility product and the start of precipitation",
    "Precipitation begins when the ionic product [Mg²⁺][OH⁻]² reaches K_sp.",
    ["[OH⁻]² = K_sp / [Mg²⁺] = 1.0 × 10⁻¹¹ / 0.10 = 1.0 × 10⁻¹⁰", "[OH⁻] = 1.0 × 10⁻⁵ M → pOH = 5.0",
     "pH = 14 − 5.0 = 9.0"],
    why="5.0 is the pOH, not the pH. 4.0 forgets to take the square root of [OH⁻]². 8.5 ignores the "
        "[Mg²⁺] of 0.10 M and takes [OH⁻] = √K_sp.",
    ncert=f"{REF6}, solubility equilibria of sparingly soluble salts: solubility product", seconds=80,
    checked=True)

x = F(2, 3)
assert x ** 2 / (1 - x) ** 2 == 4 and close(float(x), 0.667, 0.002)
assert F(4, 5) ** 2 / (1 - F(4, 5)) ** 2 == 16
add("Kp, Kc and Le Chatelier", A, "numerical",
    "For the reaction A(g) + B(g) ⇌ C(g) + D(g), K_c = 4.0 at a certain temperature. 1.0 mol of A and 1.0 mol "
    "of B are placed in a closed 1.0 L vessel at this temperature. The amount of C present at equilibrium is:",
    Opts("C", "0.67 mol", ["0.50 mol", "0.80 mol", "0.33 mol"]),
    "Calculating equilibrium amounts from K_c",
    "Let x mol of A react. At equilibrium [A] = [B] = 1 − x and [C] = [D] = x (V = 1 L). Then "
    "K_c = x²/(1 − x)² = 4, so x/(1 − x) = 2.",
    ["x/(1 − x) = √4 = 2", "x = 2 − 2x → 3x = 2 → x = 0.67 mol"],
    why="0.50 mol would give K_c = 1. 0.80 mol uses x/(1 − x) = 4 (not taking the square root). 0.33 mol is "
        "the amount of A left, not of C formed.",
    ncert=f"{REF6}, applications of equilibrium constants: calculating equilibrium concentrations",
    seconds=70, checked=True)

add("Kp, Kc and Le Chatelier", A, "assertion_reason",
    ar("At constant temperature, K_c of the equilibrium N₂(g) + 3H₂(g) ⇌ 2NH₃(g) increases when the total "
       "pressure is increased.",
       "Increasing the pressure shifts this equilibrium in the direction of ammonia."),
    AR_, "Effect of pressure on equilibrium composition versus K",
    "Compressing the mixture shifts the equilibrium towards the side with fewer moles of gas (NH₃), so R is "
    "true. But the shift only restores Q_c to the same K_c; the equilibrium constant changes only with "
    "temperature. A is false.",
    ["Higher pressure → more NH₃ (R true)", "K_c depends only on T → unchanged at constant T (A false)"],
    answer="D", ncert=f"{REF6}, factors affecting equilibria: effect of pressure change", seconds=40)

add("Solubility product", A, "statement_pair",
    sp("At a given temperature, AgCl is less soluble in 0.1 M NaCl solution than in pure water.",
       "At the same temperature, the solubility product of AgCl is smaller in 0.1 M NaCl solution than in "
       "pure water."),
    SP_, "Common ion effect on solubility",
    "The Cl⁻ ions from NaCl shift AgCl(s) ⇌ Ag⁺ + Cl⁻ to the left, so less AgCl dissolves: Statement I is true. "
    "K_sp is an equilibrium constant and has a fixed value at a given temperature; it is the solubility that "
    "falls, not K_sp. Statement II is false.",
    ["Common ion Cl⁻ → lower solubility → Statement I true",
     "K_sp depends only on temperature → Statement II false"],
    answer="C", ncert=f"{REF6}, common ion effect on solubility of ionic salts", seconds=35)

add("Acids, bases and pH", A, "multi_statement",
    ms("Which of the following statements about the strengths of acids are correct?",
       ["The acid strength of the hydrogen halides in water follows the order HF < HCl < HBr < HI.",
        "H₂S is a stronger acid than H₂O.",
        "The acidity of the hydrides of the second-period elements follows the order CH₄ < NH₃ < H₂O < HF.",
        "Down a group, the acid strength of the hydrides decreases because the H–A bond becomes weaker.",
        "NH₃ is a stronger acid than H₂O."]),
    multi("D", {"a": True, "b": True, "c": True, "d": False, "e": False},
          ["(a), (b), (c) and (d) only", "(b), (c) and (e) only", "(a) and (d) only"]),
    "Factors affecting acid strength",
    "Down a group, the size of A increases and the H–A bond becomes weaker, so H⁺ is released more easily and "
    "the acid becomes stronger: HF < HCl < HBr < HI and H₂O < H₂S. Across a period, the electronegativity of A "
    "increases, the H–A bond becomes more polar, and acidity rises: CH₄ < NH₃ < H₂O < HF.",
    ["(a) True", "(b) True", "(c) True", "(d) False: a weaker H–A bond makes the acid stronger",
     "(e) False: H₂O is more acidic than NH₃"],
    why="Any option with (d) or (e) is wrong; (a), (b) and (c) are all true.",
    ncert=f"{REF6}, ionization of acids and bases: factors affecting acid strength", seconds=60)

# ==================================================================== 7. Redox Reactions and Electrochemistry
topic("Redox Reactions and Electrochemistry")
REF7R, REF7E = f"{C11}, 'Redox Reactions'", f"{C12}, 'Electrochemistry'"

s_on = F(-(2 * 1 + 6 * -2), 4)
assert s_on == F(5, 2)
add("Oxidation number and balancing", B, "direct",
    "The average oxidation number of sulphur in sodium tetrathionate, Na₂S₄O₆, is:",
    Opts("B", "+2.5", ["+2", "+5", "+6"]),
    "Average oxidation number",
    "Let the average oxidation number of S be x. Na is +1 and O is −2, and the sum for the neutral compound "
    "is zero.",
    ["2(+1) + 4x + 6(−2) = 0", "4x = 10 → x = +2.5",
     "(Structurally, two S atoms are +5 and two are 0; their average is +2.5.)"],
    why="+2 is the value in thiosulphate (S₂O₃²⁻). +5 is the oxidation number of only the two terminal S "
        "atoms. +6 is the value in sulphate.",
    ncert=f"{REF7R}, oxidation number", seconds=30)

e_cell = 0.80 - (-0.76)
assert close(e_cell, 1.56) and close(0.80 - 0.76, 0.04) and close(2 * 0.80 + 0.76, 2.36)
add("Electrode potential and cells", B, "numerical",
    "The standard emf of the cell Zn(s) | Zn²⁺(aq, 1 M) || Ag⁺(aq, 1 M) | Ag(s) at 298 K is "
    "(E°(Zn²⁺/Zn) = −0.76 V, E°(Ag⁺/Ag) = +0.80 V):",
    Opts("A", "1.56 V", ["0.04 V", "2.36 V", "−1.56 V"]),
    "Standard emf from standard electrode potentials",
    "E°cell = E°(cathode) − E°(anode), using standard reduction potentials. The cell as written has zinc as "
    "anode (left) and silver as cathode (right). Electrode potentials are intensive, so they are not "
    "multiplied by the stoichiometric coefficient.",
    ["E°cell = E°(Ag⁺/Ag) − E°(Zn²⁺/Zn)", "= 0.80 − (−0.76) = 1.56 V"],
    why="0.04 V ignores the negative sign of the zinc potential. 2.36 V doubles the silver potential because "
        "two Ag⁺ ions are reduced. −1.56 V subtracts in the wrong order.",
    ncert=f"{REF7E}, galvanic cells: measurement of electrode potential", seconds=30, checked=True)

add("Electrode potential and cells", B, "statement_pair",
    sp("In a galvanic cell, the Gibbs energy of a spontaneous redox reaction is converted into electrical "
       "work.",
       "In an electrolytic cell, electrical energy is used to bring about a non-spontaneous chemical "
       "reaction."),
    SP_, "Galvanic and electrolytic cells",
    "A galvanic (voltaic) cell converts the chemical energy of a spontaneous reaction into electrical energy: "
    "Statement I is true. An electrolytic cell uses an external source of electricity to drive a reaction that "
    "would not occur by itself: Statement II is true.",
    ["Galvanic: chemical → electrical (spontaneous) → I true",
     "Electrolytic: electrical → chemical (non-spontaneous) → II true"],
    answer="A", ncert=f"{REF7E}, electrochemical cells; electrolytic cells and electrolysis", seconds=25)

add("Oxidation number and balancing", B, "match_list",
    lists("Match List-I (redox reaction) with List-II (its type).",
          ["2KClO₃(s) → 2KCl(s) + 3O₂(g)", "Cl₂(g) + 2OH⁻(aq) → ClO⁻(aq) + Cl⁻(aq) + H₂O(l)",
           "Zn(s) + CuSO₄(aq) → ZnSO₄(aq) + Cu(s)", "3Mg(s) + N₂(g) → Mg₃N₂(s)"],
          ["Combination", "Decomposition", "Displacement", "Disproportionation"]),
    match("C", M("II IV III I"), [M("IV II III I"), M("II IV I III"), M("II III IV I")]),
    "Types of redox reactions",
    "A decomposition breaks one compound into two or more substances. In disproportionation one element in "
    "one oxidation state is both oxidised and reduced (Cl: 0 → +1 and 0 → −1). In displacement one element "
    "replaces another in a compound. In combination two substances join to form one product.",
    ["KClO₃ → KCl + O₂: decomposition → II", "Cl₂ → ClO⁻ + Cl⁻: disproportionation → IV",
     "Zn displaces Cu: displacement → III", "Mg + N₂ → Mg₃N₂: combination → I"],
    why="The other codes interchange decomposition with disproportionation, combination with displacement, "
        "or displacement with disproportionation.",
    ncert=f"{REF7R}, types of redox reactions", seconds=40)

lam_bacl2 = 127.2 + 2 * 76.3
assert close(lam_bacl2, 279.8) and close(127.2 + 76.3, 203.5) and close(2 * 127.2 + 76.3, 330.7)
add("Conductance and Kohlrausch's law", I, "numerical",
    "The limiting molar conductivities of Ba²⁺ and Cl⁻ ions at 298 K are 127.2 and 76.3 S cm² mol⁻¹. The "
    "limiting molar conductivity of BaCl₂ is:",
    Opts("D", "279.8 S cm² mol⁻¹", ["203.5 S cm² mol⁻¹", "330.7 S cm² mol⁻¹", "152.6 S cm² mol⁻¹"]),
    "Kohlrausch's law of independent migration of ions",
    "Λ°m of an electrolyte is the sum of the limiting molar conductivities of its ions, each multiplied by "
    "the number of such ions in the formula: Λ°m = ν₊λ°₊ + ν₋λ°₋.",
    ["BaCl₂ → Ba²⁺ + 2Cl⁻", "Λ°m = 127.2 + 2 × 76.3 = 279.8 S cm² mol⁻¹"],
    why="203.5 forgets that there are two Cl⁻ ions. 330.7 doubles Ba²⁺ instead of Cl⁻. 152.6 counts only the "
        "chloride ions.",
    ncert=f"{REF7E}, Kohlrausch law", seconds=35, checked=True)

e_mn = 7 - 2
e_fe = 1
assert (6 * e_fe) // 1 == 2 * (6 - 3) and e_mn == 5
add("Oxidation number and balancing", I, "numerical",
    "In acidic medium, dichromate ion oxidises Fe²⁺ to Fe³⁺ and is itself reduced to Cr³⁺. The number of "
    "moles of Fe²⁺ oxidised by one mole of Cr₂O₇²⁻ is:",
    Opts("B", "6", ["3", "1", "5"]),
    "Electron balance in a redox titration",
    "Each Cr changes from +6 to +3, gaining 3 electrons, so one Cr₂O₇²⁻ (two Cr atoms) gains 6 electrons. Each "
    "Fe²⁺ loses one electron. Six Fe²⁺ are therefore needed per dichromate ion.",
    ["Cr: +6 → +3, gain 3 e⁻ per Cr; 2 Cr → 6 e⁻", "Fe: +2 → +3, lose 1 e⁻",
     "Cr₂O₇²⁻ + 6Fe²⁺ + 14H⁺ → 2Cr³⁺ + 6Fe³⁺ + 7H₂O"],
    why="3 counts the change of only one Cr atom. 1 assumes a 1 : 1 reaction. 5 is the number for MnO₄⁻.",
    ncert=f"{REF7R}, balancing of redox reactions", seconds=40, checked=True)

add("Oxidation number and balancing", I, "direct",
    "In a neutral or faintly alkaline solution, the permanganate ion is reduced to manganese dioxide (MnO₂). "
    "The number of electrons gained by each MnO₄⁻ ion is:",
    Opts("C", "3", ["5", "1", "4"]),
    "Change in oxidation number",
    "Mn is +7 in MnO₄⁻ (x + 4(−2) = −1) and +4 in MnO₂. The decrease of 3 in oxidation number equals the "
    "electrons gained.",
    ["MnO₄⁻: x − 8 = −1 → x = +7", "MnO₂: x − 4 = 0 → x = +4", "Electrons gained = 7 − 4 = 3"],
    why="5 is the change to Mn²⁺ in acidic medium. 1 is the change to MnO₄²⁻ (manganate) in strongly "
        "alkaline medium. 4 is the oxidation number of Mn in MnO₂, not the change.",
    ncert=f"{REF7R}, oxidation number; {C12}, 'The d- and f-Block Elements', potassium permanganate",
    seconds=30)

add("Batteries and fuel cells", I, "assertion_reason",
    ar("The lead storage battery can be recharged and used again.",
       "When a current is passed through it in the reverse direction, the PbSO₄ deposited on the electrodes "
       "during discharge is converted back into Pb on the negative plate and PbO₂ on the positive plate."),
    AR_, "Lead storage battery as a secondary cell",
    "During discharge, Pb(s) + PbO₂(s) + 2H₂SO₄(aq) → 2PbSO₄(s) + 2H₂O(l). The PbSO₄ stays on the electrodes. "
    "On charging, the reaction is reversed by the external current, regenerating Pb and PbO₂, so the battery "
    "can be used again. R explains A.",
    ["Discharge: Pb + PbO₂ + 2H₂SO₄ → 2PbSO₄ + 2H₂O", "Charging reverses this: 2PbSO₄ + 2H₂O → Pb + PbO₂ + 2H₂SO₄",
     "Reversible cell reaction → rechargeable (R explains A)"],
    answer="A", ncert=f"{REF7E}, batteries: secondary batteries", seconds=35)

add("Electrode potential and cells", I, "multi_statement",
    ms("Which of the following statements are correct?",
       ["The standard hydrogen electrode is a platinum electrode coated with platinum black, dipped in an "
        "acidic solution in which pure hydrogen gas is bubbled.",
        "When a cell works as a galvanic cell, its emf is positive.",
        "A salt bridge completes the electrical circuit and keeps the two half-cell solutions electrically "
        "neutral.",
        "In a galvanic cell, electrons flow in the external circuit from the cathode to the anode.",
        "Oxidation takes place at the cathode."]),
    multi("B", {"a": True, "b": True, "c": True, "d": False, "e": False},
          ["(a), (c) and (d) only", "(b), (c) and (e) only", "(a), (b), (c) and (d) only"]),
    "Galvanic cells and the standard hydrogen electrode",
    "In the SHE, H₂ at 1 bar is bubbled over platinised platinum in a solution with H⁺ at unit concentration. A "
    "spontaneous cell reaction has ΔG = −nFE < 0, so E > 0. The salt bridge carries ions between the "
    "half-cells. Electrons leave the anode (where oxidation occurs) and travel to the cathode.",
    ["(a) True", "(b) True: ΔG = −nFE < 0 → E > 0", "(c) True", "(d) False: anode → cathode",
     "(e) False: oxidation at the anode"],
    why="Options with (d) or (e) are wrong.",
    ncert=f"{REF7E}, galvanic cells; measurement of electrode potential", seconds=55)

e_fe3 = (2 * -0.44 + 1 * 0.77) / 3
assert close(e_fe3, -0.037, 0.02) and close(-0.44 + 0.77, 0.33) and close((-0.44 + 0.77) / 2, 0.165)
assert close(-0.44 - 0.77, -1.21)
add("Nernst equation and Gibbs energy", A, "numerical",
    "Given E°(Fe²⁺/Fe) = −0.44 V and E°(Fe³⁺/Fe²⁺) = +0.77 V, the standard electrode potential E°(Fe³⁺/Fe) "
    "is:",
    Opts("C", "−0.037 V", ["+0.33 V", "+0.165 V", "−1.21 V"]),
    "Combining half-reactions through ΔG° = −nFE°",
    "Electrode potentials are not additive, but Gibbs energies are. Add the ΔG° values of the two half-"
    "reactions and convert back with n = 3.",
    ["Fe²⁺ + 2e⁻ → Fe: ΔG°₁ = −2F(−0.44) = +0.88F", "Fe³⁺ + e⁻ → Fe²⁺: ΔG°₂ = −1F(0.77) = −0.77F",
     "Fe³⁺ + 3e⁻ → Fe: ΔG°₃ = 0.88F − 0.77F = +0.11F", "E°₃ = −ΔG°₃ / 3F = −0.11/3 = −0.037 V"],
    shortcut="E°₃ = (n₁E°₁ + n₂E°₂)/(n₁ + n₂) = (2 × −0.44 + 1 × 0.77)/3.",
    why="+0.33 V adds the two potentials directly. +0.165 V averages them without weighting by n. −1.21 V "
        "subtracts them.",
    ncert=f"{REF7E}, relation between ΔrG° and E°cell", seconds=90, checked=True)

d_e = 0.059 / 2 * math.log10(100)
assert close(d_e, 0.059) and close(0.059 * math.log10(100), 0.118) and close(0.059 / 2, 0.0295)
add("Nernst equation and Gibbs energy", A, "numerical",
    "In the cell Zn(s) | Zn²⁺(aq, 1 M) || Cu²⁺(aq, 1 M) | Cu(s) at 298 K, the Cu²⁺ solution is diluted 100 "
    "times, with [Zn²⁺] unchanged. The emf of the cell (2.303RT/F = 0.059 V):",
    Opts("D", "Decreases by 0.059 V", ["Increases by 0.059 V", "Decreases by 0.118 V",
                                       "Decreases by 0.0295 V"]),
    "Nernst equation: effect of concentration on emf",
    "For Zn + Cu²⁺ → Zn²⁺ + Cu (n = 2), E = E° − (0.059/2) log([Zn²⁺]/[Cu²⁺]). Lowering [Cu²⁺] 100 times raises "
    "the log term by log 100 = 2.",
    ["Before: E = E° (both 1 M)", "After: E = E° − (0.059/2) log(1/0.01) = E° − 0.0295 × 2",
     "Change = −0.059 V (emf decreases)"],
    why="'Increases' has the wrong sign: diluting the cathode solution makes the reaction less favourable. "
        "0.118 V uses n = 1. 0.0295 V takes log 100 as 1.",
    ncert=f"{REF7E}, Nernst equation", seconds=70, checked=True)

add("Batteries and fuel cells", A, "statement_pair",
    sp("Sulphuric acid is consumed during the discharge of a lead storage battery.",
       "The dry (Leclanché) cell is a secondary battery that can be recharged."),
    SP_, "Lead storage battery and dry cell",
    "During discharge the cell reaction is Pb(s) + PbO₂(s) + 2H₂SO₄(aq) → 2PbSO₄(s) + 2H₂O(l), so sulphuric "
    "acid is used up: Statement I is true. The dry cell is a primary battery; its reaction cannot be "
    "reversed, and it is discarded once used up. Statement II is false.",
    ["Discharge consumes H₂SO₄ → Statement I true",
     "Dry cell: primary battery, not rechargeable → Statement II false"],
    answer="C", ncert=f"{REF7E}, batteries: primary and secondary batteries", seconds=35)

c3o2 = F(4, 3)
hn3 = F(-1, 3)
assert 3 * c3o2 + 2 * -2 == 0 and 1 + 3 * hn3 == 0
add("Oxidation number and balancing", A, "multi_statement",
    ms("Which of the following statements are correct?",
       ["In the reaction 2Cu⁺(aq) → Cu²⁺(aq) + Cu(s), copper undergoes disproportionation.",
        "In the reaction Fe₂O₃ + 3CO → 2Fe + 3CO₂, carbon is oxidised from +2 to +4.",
        "The oxidation number of carbon in carbon suboxide, C₃O₂, is +4/3.",
        "The perchlorate ion, ClO₄⁻, undergoes disproportionation in aqueous solution.",
        "The oxidation number of nitrogen in hydrazoic acid, HN₃, is −3."]),
    multi("B", {"a": True, "b": True, "c": True, "d": False, "e": False},
          ["(a), (b), (c) and (d) only", "(a), (c) and (e) only", "(b), (d) and (e) only"]),
    "Oxidation numbers and disproportionation",
    "Cu⁺ (+1) goes to both Cu²⁺ (+2) and Cu (0): disproportionation. Carbon goes from +2 in CO to +4 in CO₂. In "
    "C₃O₂, 3x − 4 = 0 → x = +4/3. In ClO₄⁻, chlorine is already in its highest oxidation state (+7), so it "
    "cannot be oxidised further and cannot disproportionate. In HN₃, 1 + 3x = 0 → x = −1/3.",
    ["(a) True", "(b) True", "(c) True", "(d) False: Cl is +7, the highest state", "(e) False: −1/3"],
    why="Any option with (d) or (e) is wrong.",
    ncert=f"{REF7R}, types of redox reactions: disproportionation reactions", seconds=75, checked=True)

# ==================================================================== 8. Chemical Kinetics
topic("Chemical Kinetics")
REF8 = f"{C12}, 'Chemical Kinetics'"

r_nh3 = 0.03 * 2 / 3
assert close(r_nh3, 0.02) and close(0.03 * 3 / 2, 0.045) and close(0.03 / 3, 0.01)
add("Rate law and order", B, "numerical",
    "For the reaction N₂(g) + 3H₂(g) → 2NH₃(g), hydrogen is consumed at a rate of 0.03 mol L⁻¹ s⁻¹. The rate of "
    "formation of ammonia is:",
    Opts("C", "0.02 mol L⁻¹ s⁻¹", ["0.045 mol L⁻¹ s⁻¹", "0.03 mol L⁻¹ s⁻¹", "0.01 mol L⁻¹ s⁻¹"]),
    "Rates of reaction in terms of different species",
    "Rate = −(1/3) d[H₂]/dt = +(1/2) d[NH₃]/dt, so d[NH₃]/dt = (2/3)(−d[H₂]/dt).",
    ["−d[H₂]/dt = 0.03 mol L⁻¹ s⁻¹", "d[NH₃]/dt = (2/3) × 0.03 = 0.02 mol L⁻¹ s⁻¹"],
    why="0.045 multiplies by 3/2 instead of 2/3. 0.03 ignores the stoichiometric coefficients. 0.01 is the "
        "rate of the reaction (1/3 of the H₂ rate), equal to the rate of consumption of N₂.",
    ncert=f"{REF8}, rate of a chemical reaction", seconds=30, checked=True)

add("Zero and first order reactions", B, "direct",
    "The radioactive decay of unstable nuclei follows:",
    Opts("A", "First-order kinetics", ["Zero-order kinetics", "Second-order kinetics", "Third-order kinetics"]),
    "Examples of first-order reactions",
    "All natural and artificial radioactive decays of unstable nuclei take place by first-order kinetics; the "
    "rate is proportional to the number of nuclei present, and the half-life is constant.",
    ["Rate ∝ number of undecayed nuclei → first order"],
    why="The rate of radioactive decay depends on the amount of the isotope present to the first power, not to "
        "the zeroth, second or third power.",
    ncert=f"{REF8}, integrated rate equations: first order reactions", seconds=20)

add("Arrhenius equation and activation energy", B, "statement_pair",
    sp("A catalyst changes the Gibbs energy change (ΔG) of a reaction.",
       "A catalyst provides an alternative pathway with a lower activation energy."),
    SP_, "Effect of a catalyst",
    "A catalyst changes the path of a reaction, lowering the activation energy so that the reaction goes "
    "faster: Statement II is true. It does not change the energies of the reactants and products, so ΔG and "
    "the equilibrium constant are unchanged: Statement I is false.",
    ["ΔG depends only on reactants and products → unchanged → Statement I false",
     "Alternative path with lower Ea → Statement II true"],
    answer="D", ncert=f"{REF8}, effect of catalyst", seconds=25)

t75 = 0.75 * 0.5 / 2.5e-3
assert close(t75, 150) and close(0.5 / 2.5e-3, 200) and close(0.5 * 0.5 / 2.5e-3, 100)
add("Zero and first order reactions", I, "numerical",
    "A zero-order reaction has a rate constant of 2.5 × 10⁻³ mol L⁻¹ s⁻¹. If the initial concentration of the "
    "reactant is 0.50 mol L⁻¹, the time taken for 75% of the reactant to react is:",
    Opts("D", "150 s", ["200 s", "100 s", "300 s"]),
    "Integrated rate law of a zero-order reaction",
    "For a zero-order reaction [R] = [R]₀ − kt, so the time to use up an amount Δ[R] is Δ[R]/k; the rate does "
    "not slow down as the reactant is used.",
    ["Amount reacted = 0.75 × 0.50 = 0.375 mol L⁻¹", "t = 0.375 / 2.5 × 10⁻³ = 150 s"],
    why="200 s is the time for complete reaction. 100 s is the half-life. 300 s assumes that 75% takes two "
        "half-lives, which is true only for a first-order reaction.",
    ncert=f"{REF8}, integrated rate equations: zero order reactions", seconds=50, checked=True)

r_avg = (0.40 - 0.30) / (20 * 60)
assert close(r_avg, 8.33e-5) and close(0.10 / 20, 5.0e-3) and close(1200 / 0.10, 1.2e4) and close(0.40 / 1200, 3.33e-4)
add("Rate law and order", I, "numerical",
    "In the reaction A → products, the concentration of A falls from 0.40 mol L⁻¹ to 0.30 mol L⁻¹ in 20 "
    "minutes. The average rate of the reaction during this interval, in mol L⁻¹ s⁻¹, is:",
    Opts("B", "8.33 × 10⁻⁵", ["5.0 × 10⁻³", "1.2 × 10⁴", "3.33 × 10⁻⁴"]),
    "Average rate of reaction",
    "Average rate = −Δ[A]/Δt. The time must be converted to seconds for the unit asked.",
    ["Δ[A] = 0.30 − 0.40 = −0.10 mol L⁻¹", "Δt = 20 min = 1200 s",
     "Average rate = 0.10 / 1200 = 8.33 × 10⁻⁵ mol L⁻¹ s⁻¹"],
    why="5.0 × 10⁻³ is the rate per minute, not per second. 1.2 × 10⁴ inverts the ratio. 3.33 × 10⁻⁴ divides "
        "the initial concentration instead of its change.",
    ncert=f"{REF8}, rate of a chemical reaction: average rate", seconds=35, checked=True)

add("Zero and first order reactions", I, "assertion_reason",
    ar("The rate of a first-order reaction decreases as the reaction proceeds.",
       "The rate of a first-order reaction is directly proportional to the concentration of the reactant, "
       "which decreases with time."),
    AR_, "Rate of a first-order reaction",
    "For a first-order reaction, rate = k[R]. As the reaction proceeds, [R] falls, so the rate falls in "
    "proportion, while k stays the same. R explains A.",
    ["Rate = k[R]", "[R] decreases with time → rate decreases", "R explains A"],
    answer="A", ncert=f"{REF8}, integrated rate equations: first order reactions", seconds=30)

add("Arrhenius equation and activation energy", I, "match_list",
    lists("Match List-I (term in the Arrhenius treatment, k = A e^(−Ea/RT)) with List-II (its meaning).",
          ["Ea", "A", "e^(−Ea/RT)", "Activated complex"],
          ["Pre-exponential (frequency) factor, a constant for the reaction",
           "Fraction of molecules with kinetic energy equal to or greater than Ea",
           "Energy needed to form the activated complex from the reactants",
           "Unstable intermediate at the top of the energy barrier"]),
    match("C", M("III I II IV"), [M("I III II IV"), M("III II I IV"), M("III I IV II")]),
    "Arrhenius equation and activated complex",
    "Ea is the activation energy, the energy needed to form the activated complex. A is the Arrhenius "
    "(frequency) factor. The Boltzmann factor e^(−Ea/RT) is the fraction of molecules with energy ≥ Ea. The "
    "activated complex is the unstable intermediate at the peak of the energy curve.",
    ["Ea → III", "A → I", "e^(−Ea/RT) → II", "Activated complex → IV"],
    why="The other codes interchange Ea with A, A with the Boltzmann factor, or the Boltzmann factor with the "
        "activated complex.",
    ncert=f"{REF8}, temperature dependence of the rate of a reaction", seconds=40)

n_half = math.log2(8)
assert n_half == 3 and 30 / n_half == 10 and close(30 / 8, 3.75) and 30 / 2 == 15
add("Half-life", A, "numerical",
    "The rate of a first-order reaction at constant temperature falls from 1.6 × 10⁻² mol L⁻¹ min⁻¹ to "
    "2.0 × 10⁻³ mol L⁻¹ min⁻¹ in 30 minutes. The half-life of the reaction is:",
    Opts("D", "10 min", ["3.75 min", "15 min", "7.5 min"]),
    "Half-life of a first-order reaction from rate data",
    "For a first-order reaction the rate is proportional to the reactant concentration, so the rate falls by "
    "the same factor as the concentration. A fall to 1/8 is three half-lives.",
    ["Rate ratio = 1.6 × 10⁻² / 2.0 × 10⁻³ = 8 = 2³", "So [R] has fallen to 1/8 → 3 half-lives",
     "t½ = 30 / 3 = 10 min"],
    why="3.75 min divides the time by the factor 8. 15 min treats the fall as one halving per 15 min (two "
        "half-lives). 7.5 min assumes four half-lives.",
    ncert=f"{REF8}, half-life of a reaction", seconds=60, checked=True)

ea = 2.303 * 8.314 * 5000 / 1000
assert close(ea, 95.7) and close(8.314 * 5000 / 1000, 41.6, 0.002)
add("Arrhenius equation and activation energy", A, "numerical",
    "A plot of log k against 1/T for a reaction is a straight line with slope −5000 K. The activation energy "
    "of the reaction is (R = 8.314 J K⁻¹ mol⁻¹):",
    Opts("B", "95.7 kJ mol⁻¹", ["41.6 kJ mol⁻¹", "−95.7 kJ mol⁻¹", "11.5 kJ mol⁻¹"]),
    "Arrhenius plot",
    "log k = log A − Ea/(2.303RT), so the slope of log k against 1/T is −Ea/(2.303R).",
    ["−Ea/(2.303R) = −5000 K", "Ea = 2.303 × 8.314 × 5000 = 95 735 J mol⁻¹ ≈ 95.7 kJ mol⁻¹"],
    why="41.6 kJ mol⁻¹ uses the slope of ln k (forgets 2.303). −95.7 kJ mol⁻¹ carries the sign of the slope; "
        "activation energy is positive. 11.5 kJ mol⁻¹ multiplies 5000 by 2.303 but leaves out R.",
    ncert=f"{REF8}, temperature dependence of the rate of a reaction", seconds=50, checked=True)
assert close(2.303 * 5000 / 1000, 11.5)

add("Arrhenius equation and activation energy", A, "assertion_reason",
    ar("If a reaction had zero activation energy, its rate constant would not change with temperature "
       "(taking the pre-exponential factor A as constant).",
       "When Ea = 0, the factor e^(−Ea/RT) equals 1 at every temperature."),
    AR_, "Arrhenius equation for Ea = 0",
    "k = A e^(−Ea/RT). With Ea = 0 the exponential factor is e⁰ = 1 at all temperatures, so k = A, which is "
    "independent of temperature. R gives the reason for A.",
    ["k = A e^(−Ea/RT)", "Ea = 0 → e⁰ = 1 → k = A at every T", "R explains A"],
    answer="A", ncert=f"{REF8}, temperature dependence of the rate of a reaction", seconds=35)

# ==================================================================== 9. Classification of Elements and Periodicity
topic("Classification of Elements and Periodicity in Properties")
REF9 = f"{C11}, 'Classification of Elements and Periodicity in Properties'"

ROOTS = {0: "nil", 1: "un", 2: "bi", 3: "tri", 4: "quad", 5: "pent", 6: "hex", 7: "sept", 8: "oct", 9: "enn"}


def iupac(z):
    name = "".join(ROOTS[int(d)] for d in str(z)) + "ium"
    return name.replace("nnn", "nn").replace("iium", "ium").capitalize()


assert iupac(115) == "Ununpentium" and iupac(111) == "Unununium" and iupac(114) == "Ununquadium"
assert iupac(116) == "Ununhexium"
add("Modern periodic table", B, "direct",
    "The temporary IUPAC (systematic) name of the element with atomic number 115 is:",
    Opts("A", "Ununpentium", ["Unununium", "Ununquadium", "Ununhexium"]),
    "Nomenclature of elements with atomic numbers above 100",
    "The IUPAC systematic name is built from numerical roots for the digits of the atomic number (0 nil, "
    "1 un, 2 bi, 3 tri, 4 quad, 5 pent, 6 hex, 7 sept, 8 oct, 9 enn) followed by 'ium'. 115 = 1-1-5 → "
    "un-un-pent-ium.",
    ["1 → un, 1 → un, 5 → pent", "Name = Ununpentium (symbol Uup)"],
    why="Unununium is element 111, Ununquadium is 114 and Ununhexium is 116.",
    ncert=f"{REF9}, nomenclature of elements with atomic numbers > 100", seconds=25, checked=True)

add("Valence and reactivity", B, "direct",
    "Which of the following elements is a metalloid (semi-metal)?",
    Opts("C", "Germanium", ["Sodium", "Sulphur", "Chlorine"]),
    "Metals, non-metals and metalloids",
    "Elements bordering the zig-zag line between metals and non-metals in the p-block, such as silicon, "
    "germanium, arsenic, antimony and tellurium, show properties of both metals and non-metals and are "
    "called metalloids.",
    ["Germanium lies on the metal–non-metal border → metalloid"],
    why="Sodium is a typical metal. Sulphur and chlorine are typical non-metals.",
    ncert=f"{REF9}, metals, non-metals and metalloids", seconds=20)

add("Atomic and ionic radii", B, "statement_pair",
    sp("An anion is larger than the atom from which it is formed.",
       "A cation is smaller than the atom from which it is formed."),
    SP_, "Ionic radii compared with atomic radii",
    "When an atom gains electrons, the same nuclear charge holds more electrons, repulsion increases and the "
    "electron cloud expands: anions are larger than their parent atoms. When an atom loses electrons, the "
    "same nuclear charge acts on fewer electrons and pulls them closer: cations are smaller. Both statements "
    "are true.",
    ["Anion: more electrons, same Z → expands → Statement I true",
     "Cation: fewer electrons, same Z → contracts → Statement II true"],
    answer="A", ncert=f"{REF9}, periodic trends: ionic radius", seconds=25)

add("Modern periodic table", I, "match_list",
    lists("Match List-I (atomic number) with List-II (type of element).",
          ["Z = 54", "Z = 92", "Z = 29", "Z = 20"],
          ["Representative (s-block) element", "Transition (d-block) element",
           "Inner transition (actinoid) element", "Noble gas"]),
    match("D", M("IV III II I"), [M("IV II III I"), M("I III II IV"), M("IV III I II")]),
    "Types of elements from electronic configuration",
    "Z = 54 is xenon ([Kr] 4d¹⁰ 5s² 5p⁶), a noble gas. Z = 92 is uranium, filling 5f: an actinoid. Z = 29 is "
    "copper ([Ar] 3d¹⁰ 4s¹), a d-block transition element. Z = 20 is calcium ([Ar] 4s²), an s-block "
    "representative element.",
    ["54 → noble gas → IV", "92 → actinoid → III", "29 → transition → II", "20 → s-block → I"],
    why="The other codes interchange the transition and inner transition elements, or the s-block element "
        "with the noble gas or the transition element.",
    ncert=f"{REF9}, electronic configurations and types of elements: s-, p-, d-, f-blocks", seconds=45)

add("Ionisation and electron gain enthalpy", I, "assertion_reason",
    ar("The first ionisation enthalpy of the elements generally decreases down a group.",
       "Down a group, the outermost electron is farther from the nucleus and better shielded by the inner "
       "electrons, which outweighs the increase in nuclear charge."),
    AR_, "Trend of ionisation enthalpy in a group",
    "Going down a group, a new shell is added for each period. The valence electron is farther from the "
    "nucleus and more inner electrons screen it, so it is held less firmly despite the larger nuclear charge. "
    "Less energy is needed to remove it. R explains A.",
    ["Larger distance + more shielding → weaker hold on the valence electron",
     "→ lower ionisation enthalpy down the group", "R explains A"],
    answer="A", ncert=f"{REF9}, periodic trends: ionization enthalpy", seconds=35)

add("Modern periodic table", I, "multi_statement",
    ms("Which of the following statements about the long form of the periodic table are correct?",
       ["The f-block elements are placed separately at the bottom of the periodic table.",
        "The long form of the periodic table has 7 periods and 18 groups.",
        "The elements of group 18 are called chalcogens.",
        "The sixth period contains 32 elements.",
        "All transition elements are non-metals."]),
    multi("B", {"a": True, "b": True, "c": False, "d": True, "e": False},
          ["(a), (b), (c) and (d) only", "(b), (d) and (e) only", "(a) and (c) only"]),
    "Structure of the modern periodic table",
    "The lanthanoids and actinoids (f-block) are placed in two rows below the main body of the table. The "
    "long form has 7 periods and 18 groups. Group 16 elements are the chalcogens; group 18 elements are the "
    "noble gases. The sixth period (6s, 4f, 5d, 6p) holds 32 elements. Transition elements are all metals.",
    ["(a) True", "(b) True", "(c) False: chalcogens are group 16", "(d) True: 2 + 14 + 10 + 6 = 32",
     "(e) False: they are metals"],
    why="Options with (c) or (e) are wrong.",
    ncert=f"{REF9}, modern periodic law and the present form of the periodic table", seconds=50)

ie1 = {"B": 801, "C": 1086, "N": 1402, "O": 1314}
assert sorted(ie1, key=ie1.get) == ["B", "C", "O", "N"]
add("Ionisation and electron gain enthalpy", A, "direct",
    "Which of the following is the correct order of first ionisation enthalpy?",
    Opts("C", "B < C < O < N", ["B < C < N < O", "C < B < O < N", "B < O < C < N"]),
    "Irregularities in the trend of ionisation enthalpy across period 2",
    "Ionisation enthalpy generally rises across a period, but oxygen is lower than nitrogen: nitrogen has a "
    "stable half-filled 2p³ set, while in oxygen two electrons share one 2p orbital and their repulsion makes "
    "one of them easier to remove. Boron (removing a 2p electron) is lower than beryllium and also lowest of "
    "these four.",
    ["Approximate ΔiH₁ (kJ mol⁻¹): B 801, C 1086, O 1314, N 1402", "Order: B < C < O < N"],
    why="B < C < N < O ignores the drop from N to O. C < B places carbon below boron. B < O < C puts oxygen "
        "below carbon.",
    ncert=f"{REF9}, periodic trends: ionization enthalpy", seconds=45, checked=True)

add("Valence and reactivity", A, "assertion_reason",
    ar("Metallic character increases from left to right across a period.",
       "Ionisation enthalpy generally increases from left to right across a period."),
    AR_, "Metallic character and ionisation enthalpy",
    "Metallic character is the tendency to lose electrons. Across a period the ionisation enthalpy generally "
    "increases (R true), so atoms lose electrons less readily and metallic character decreases from left to "
    "right. A is false.",
    ["ΔiH increases across a period (R true)", "Higher ΔiH → harder to lose electrons → less metallic",
     "Metallic character decreases left to right (A false)"],
    answer="D", ncert=f"{REF9}, periodic trends in chemical properties", seconds=30)

add("Atomic and ionic radii", A, "multi_statement",
    ms("Which of the following comparisons are correct?",
       ["Atomic radius: Li > Be",
        "Electron gain enthalpy: Cl is more negative than Br",
        "First ionisation enthalpy: He > Ne",
        "Electronegativity: Cl > F",
        "Radius: Cl⁻ < Cl"]),
    multi("B", {"a": True, "b": True, "c": True, "d": False, "e": False},
          ["(a), (b) and (d) only", "(b), (c) and (e) only", "(a), (c), (d) and (e) only"]),
    "Periodic trends in radius, electron gain enthalpy, ionisation enthalpy and electronegativity",
    "Atomic radius falls across a period (Li > Be). Electron gain enthalpy becomes less negative down group 17 "
    "below chlorine (Cl −349, Br −325 kJ mol⁻¹). He (1s²) holds its electrons closer to the nucleus than Ne "
    "and has the highest ionisation enthalpy of all. Fluorine is the most electronegative element. An anion "
    "is larger than its atom.",
    ["(a) True", "(b) True", "(c) True: He 2372, Ne 2080 kJ mol⁻¹", "(d) False: F > Cl",
     "(e) False: Cl⁻ > Cl"],
    why="Options with (d) or (e) are wrong; (a), (b) and (c) are all true.",
    ncert=f"{REF9}, periodic trends in physical properties", seconds=60)

# ==================================================================== 10. p-Block Elements
topic("p-Block Elements")
REF10A = "Class 11 Chemistry (pre-2023 edition), 'The p-Block Elements'"
REF10B = "Class 12 Chemistry (pre-2023 edition), 'The p-Block Elements'"

add("Group 15 and 16 trends", B, "direct",
    "Which of the following elements of group 16 has the highest first ionisation enthalpy?",
    Opts("C", "Oxygen", ["Sulphur", "Selenium", "Tellurium"]),
    "Trend of ionisation enthalpy in group 16",
    "Down group 16 the atomic size increases, so the valence electrons are farther from the nucleus and "
    "better shielded. The ionisation enthalpy therefore decreases from oxygen to tellurium, and oxygen, the "
    "smallest atom, has the highest value.",
    ["Atomic size: O < S < Se < Te", "Ionisation enthalpy: O > S > Se > Te"],
    why="Sulphur, selenium and tellurium are larger atoms, so their outer electrons are removed more easily.",
    ncert=f"{REF10B}, group 16 elements: ionisation enthalpy", seconds=20)

add("Group 15 and 16 trends", B, "direct",
    "Which element of group 16 is radioactive?",
    Opts("D", "Polonium", ["Sulphur", "Selenium", "Tellurium"]),
    "Occurrence of group 16 elements",
    "Oxygen, sulphur, selenium, tellurium and polonium make up group 16. Polonium is radioactive and short-"
    "lived; it occurs in nature as a decay product of thorium and uranium minerals.",
    ["Group 16: O, S, Se, Te, Po", "Po → radioactive"],
    why="Sulphur, selenium and tellurium have stable isotopes and are not radioactive elements.",
    ncert=f"{REF10B}, group 16 elements: occurrence", seconds=20)

add("Group 15 and 16 trends", B, "statement_pair",
    sp("The first ionisation enthalpy increases from nitrogen to bismuth in group 15.",
       "The covalent radius decreases from nitrogen to bismuth in group 15."),
    SP_, "Trends in group 15",
    "Down group 15 the atoms become larger (a new shell is added in each period), so the covalent radius "
    "increases and the outer electrons are held less firmly; the ionisation enthalpy decreases. Both "
    "statements are false.",
    ["Ionisation enthalpy decreases down the group → Statement I false",
     "Covalent radius increases down the group → Statement II false"],
    answer="B", ncert=f"{REF10B}, group 15 elements: atomic and ionic radii; ionisation enthalpy", seconds=25)

add("Group 15 and 16 trends", I, "direct",
    "Among the hydrides of group 15 (NH₃, PH₃, AsH₃, SbH₃, BiH₃), the strongest reducing agent is:",
    Opts("B", "BiH₃", ["NH₃", "PH₃", "SbH₃"]),
    "Reducing character of group 15 hydrides",
    "The E–H bond becomes longer and weaker down the group, so the hydride gives up hydrogen more readily. The "
    "reducing character therefore increases from NH₃ to BiH₃, and BiH₃ is the strongest reducing agent.",
    ["E–H bond strength decreases down the group", "Reducing character: NH₃ < PH₃ < AsH₃ < SbH₃ < BiH₃"],
    why="NH₃ has the strongest E–H bond and is the weakest reducing agent. PH₃ and SbH₃ are weaker reducing "
        "agents than BiH₃.",
    ncert=f"{REF10B}, group 15 elements: reactivity towards hydrogen", seconds=30)

add("Group 17 and 18 trends", I, "assertion_reason",
    ar("The noble gases have high boiling points.",
       "The only forces between noble gas atoms are weak dispersion forces."),
    AR_, "Physical properties of the noble gases",
    "Noble gases are monoatomic and held together only by weak dispersion (London) forces, so R is true. "
    "Little energy is needed to overcome these forces, which is why the noble gases have very low boiling "
    "points; A is false.",
    ["Interatomic forces: only weak dispersion forces (R true)", "Weak forces → very low boiling points (A false)"],
    answer="D", ncert=f"{REF10B}, group 18 elements: physical properties", seconds=30)

CONF = {13: "ns² np¹", 15: "ns² np³", 16: "ns² np⁴", 17: "ns² np⁵"}
assert all(int(CONF[g][-1].translate(str.maketrans("¹³⁴⁵", "1345"))) == g - 12 for g in CONF)
add("Group 15 and 16 trends", I, "match_list",
    lists("Match List-I (group of the p-block) with List-II (general valence-shell electronic configuration).",
          ["Group 13", "Group 15", "Group 16", "Group 17"],
          ["ns² np⁴", "ns² np¹", "ns² np⁵", "ns² np³"]),
    match("C", M("II IV I III"), [M("II I IV III"), M("IV II I III"), M("II IV III I")]),
    "Valence-shell configurations of the p-block groups",
    "In the p-block the ns subshell is full and the number of np electrons is (group number − 12). So group 13 "
    "has np¹, group 15 np³, group 16 np⁴ and group 17 np⁵.",
    ["Group 13 → ns² np¹ → II", "Group 15 → ns² np³ → IV", "Group 16 → ns² np⁴ → I", "Group 17 → ns² np⁵ → III"],
    why="The other codes interchange groups 15 and 16, groups 13 and 15, or groups 16 and 17.",
    ncert=f"{REF10A}, p-block elements: electronic configuration; {REF10B}, groups 15–17: electronic "
          "configuration", seconds=35, checked=True)

add("Group 15 and 16 trends", I, "multi_statement",
    ms("Which of the following statements about group 15 elements are correct?",
       ["Dinitrogen is rather inert at room temperature because of the high bond enthalpy of the N≡N bond.",
        "The +5 oxidation state is more stable for phosphorus than for bismuth.",
        "The basic character of the hydrides increases from NH₃ to BiH₃.",
        "The H–E–H bond angle of the hydrides decreases from NH₃ to SbH₃.",
        "Nitrogen has the largest atomic radius in group 15."]),
    multi("A", {"a": True, "b": True, "c": False, "d": True, "e": False},
          ["(a), (b), (c) and (d) only", "(b), (d) and (e) only", "(a), (c) and (e) only"]),
    "General trends in group 15",
    "The N≡N bond enthalpy is very high, so N₂ reacts only at high temperature. Because of the inert pair "
    "effect, the stability of the +5 state falls down the group; bismuth forms hardly any +5 compounds. "
    "Basicity of the hydrides decreases from NH₃ to BiH₃. The bond angle falls from about 107.8° in NH₃ to "
    "about 91° in SbH₃. Atomic radius increases down the group, so nitrogen is the smallest.",
    ["(a) True", "(b) True: +5 state less stable down the group", "(c) False: basicity decreases",
     "(d) True", "(e) False: nitrogen is the smallest"],
    why="Any option with (c) or (e) is wrong.",
    ncert=f"{REF10B}, group 15 elements: properties of hydrides; oxidation states; dinitrogen", seconds=70)

add("Group 15 and 16 trends", I, "statement_pair",
    sp("The stability of the −2 oxidation state decreases down group 16.",
       "Polonium hardly shows the −2 oxidation state."),
    SP_, "Oxidation states in group 16",
    "Down group 16 the electronegativity falls, so the tendency to gain two electrons and the stability of "
    "the −2 state decrease: Statement I is true. Polonium, at the bottom of the group, hardly shows the −2 "
    "state: Statement II is true.",
    ["Electronegativity falls down the group → −2 state less stable → I true",
     "Po: −2 state hardly shown → II true"],
    answer="A", ncert=f"{REF10B}, group 16 elements: oxidation states", seconds=30)

ega = {"F": -333, "Cl": -349, "Br": -325, "I": -296}
assert sorted(ega, key=ega.get) == ["Cl", "F", "Br", "I"]
add("Group 17 and 18 trends", A, "direct",
    "Which of the following is the correct order of electron gain enthalpy of the halogens, from the most "
    "negative to the least negative?",
    Opts("D", "Cl > F > Br > I", ["F > Cl > Br > I", "Cl > Br > F > I", "I > Br > Cl > F"]),
    "Electron gain enthalpy of the halogens",
    "Electron gain enthalpy generally becomes less negative down group 17, but fluorine is an exception: its "
    "small 2p subshell is crowded, and the incoming electron feels strong repulsion. So chlorine has the most "
    "negative value, followed by fluorine, bromine and iodine.",
    ["Approximate ΔegH (kJ mol⁻¹): Cl −349, F −333, Br −325, I −296", "Order: Cl > F > Br > I"],
    why="F > Cl > Br > I ignores the anomaly of fluorine. Cl > Br > F > I puts fluorine too low. "
        "I > Br > Cl > F reverses the trend.",
    ncert=f"{REF10B}, group 17 elements: electron gain enthalpy", seconds=40, checked=True)

add("Group 15 and 16 trends", A, "assertion_reason",
    ar("For oxides of group 15 elements in the same oxidation state, the acidic character decreases down the "
       "group.",
       "The metallic character of the elements increases down group 15."),
    AR_, "Trend in the nature of oxides down group 15",
    "Down group 15 the elements change from non-metals (N, P) through metalloids (As, Sb) to a metal (Bi). "
    "Oxides of non-metals are acidic and oxides of metals are basic, so as metallic character increases the "
    "oxides become less acidic and more basic: oxides of N and P are acidic, those of As and Sb amphoteric and "
    "that of Bi basic. R explains A.",
    ["Metallic character: N < P < As < Sb < Bi (R true)", "More metallic → oxide less acidic, more basic",
     "Acidic character of E₂O₃ decreases down the group (A true, explained by R)"],
    answer="A", ncert=f"{REF10B}, group 15 elements: chemical properties (oxides)", seconds=40)

add("Group 15 and 16 trends", A, "multi_statement",
    ms("Which of the following statements about trends in the p-block are correct?",
       ["Electronegativity decreases down group 17.",
        "Atomic radius increases down group 16.",
        "Nitrogen is much more electronegative than the other elements of group 15.",
        "The atomic radius of nitrogen is larger than that of phosphorus.",
        "The first ionisation enthalpy of the group 17 elements increases down the group."]),
    multi("B", {"a": True, "b": True, "c": True, "d": False, "e": False},
          ["(a), (b), (c) and (d) only", "(b), (d) and (e) only", "(a), (c) and (e) only"]),
    "General trends down p-block groups and the anomalous first element",
    "Down a group a new shell is added in each period, so atomic radius increases and the attraction of the "
    "nucleus for valence and shared electrons falls: electronegativity and ionisation enthalpy decrease. "
    "Nitrogen, the small first member of group 15, has a much higher electronegativity (3.0) than P, As, Sb "
    "and Bi, and it is smaller than phosphorus.",
    ["(a) True", "(b) True", "(c) True: anomalous first member", "(d) False: N is smaller than P",
     "(e) False: ionisation enthalpy decreases down the group"],
    why="Options with (d) or (e) are wrong; (a), (b) and (c) are all true.",
    ncert=f"{REF10B}, group 15–17 elements: atomic radii, ionisation enthalpy, electronegativity", seconds=60)



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
    doc = {"schema_version": "1.0", "batch_id": "BATCH_003", "created_at": TODAY,
           "notes": "Package CHE_003_p1: 122 original Chemistry questions (physical chemistry, periodicity and "
                    "p-block). Numerical answers re-derived in tools/batch_003/CHE_003_p1.py.",
           "stimuli": [], "questions": QUESTIONS}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {OUT}: {n} questions; difficulty {dict(Counter(q['difficulty'] for q in QUESTIONS))}; "
          f"formats {dict(fmts)}; keys {dict(sorted(KEYS.items()))}")
