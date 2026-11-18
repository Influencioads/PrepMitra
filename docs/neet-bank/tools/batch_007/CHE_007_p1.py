"""Writes batches/parts/BATCH_007_CHE_p1.json: package CHE_007_p1 of BATCH_007 (Chemistry, 120 questions).

Topics: Some Basic Concepts, Atomic Structure, Chemical Bonding, Thermodynamics, Solutions, Equilibrium,
Redox and Electrochemistry, Chemical Kinetics, Classification of Elements and Periodicity.
IDs NEET_CHE_001501..001620.

Every computable answer is re-derived here with an assert before anything is written; the quota per
(topic, difficulty), the ID range, the format mix and the answer-key balance are asserted too.
The position of every correct option is chosen by hand in the call that adds the question (argument `at`)
and never moved by code.

    cd docs/neet-bank && python tools/batch_007/CHE_007_p1.py
"""

import json
import math
import sys
from collections import Counter
from pathlib import Path

TOOLS = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(TOOLS))
from qbank import ASSERTION_REASON, STATEMENT_PAIR, default_mappings  # noqa: E402

ROOT = TOOLS.parent
PACKAGE = "CHE_007_p1"
PLAN = ROOT / "batches" / "plans" / "BATCH_007_plan.json"
OUT = ROOT / "batches" / "parts" / "BATCH_007_CHE_p1.json"
TODAY = "2026-11-16"
LETTERS = "ABCD"
CHE = "Chemistry"
FIRST_ID = 1501
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
R_J = 8.314

# ==================================================================== 1. Some Basic Concepts in Chemistry
topic("Some Basic Concepts in Chemistry")
REF1 = f"{C11}, 'Some Basic Concepts of Chemistry'"

n_c14 = 7e-3 / 14
neutrons = n_c14 * 8 * NA
assert close(neutrons, 2.41e21) and close(n_c14 * 6 * NA, 1.81e21) and close(n_c14 * NA, 3.01e20) \
    and close(n_c14 * 14 * NA, 4.22e21)
add("Mole concept", B, "numerical",
    "The number of neutrons present in 7 mg of carbon-14 (¹⁴₆C, molar mass 14 g mol⁻¹) is "
    "(Nₐ = 6.022 × 10²³ mol⁻¹):",
    Opts("C", "2.41 × 10²¹", ["1.81 × 10²¹", "3.01 × 10²⁰", "4.22 × 10²¹"]),
    "Counting sub-atomic particles with the mole concept",
    "Find the number of ¹⁴C atoms from the amount in moles, then multiply by the number of neutrons in each "
    "atom: mass number − atomic number = 14 − 6 = 8.",
    ["n(¹⁴C) = 7 × 10⁻³ g / 14 g mol⁻¹ = 5 × 10⁻⁴ mol",
     "Atoms = 5 × 10⁻⁴ × 6.022 × 10²³ = 3.011 × 10²⁰", "Neutrons = 8 × 3.011 × 10²⁰ = 2.41 × 10²¹"],
    why="1.81 × 10²¹ multiplies by 6, the number of protons. 3.01 × 10²⁰ is the number of atoms, not neutrons. "
        "4.22 × 10²¹ multiplies by 14, counting all the nucleons.",
    ncert=f"{REF1}, mole concept and molar masses", seconds=45, checked=True)

ratio = (2.4 / 12, 0.6 / 1, 1.6 / 16)
assert [round(x / min(ratio), 6) for x in ratio] == [2, 6, 1]
assert [round(x / min(ratio[0], ratio[1] / 2, 1.6 / 8), 6) for x in (ratio[0], ratio[1] / 2, 1.6 / 8)] == [1, 1.5, 1]
add("Empirical and molecular formulae", B, "numerical",
    "A sample of an organic compound contains 2.4 g of carbon, 0.6 g of hydrogen and 1.6 g of oxygen. Its "
    "empirical formula is (C = 12, H = 1, O = 16):",
    Opts("A", "C₂H₆O", ["CH₃O", "C₂H₃O", "C₄H₁₂O₂"]),
    "Empirical formula from the masses of the elements",
    "Convert each mass into moles of atoms and divide by the smallest value to get the simplest whole-number "
    "ratio.",
    ["C: 2.4/12 = 0.2 mol; H: 0.6/1 = 0.6 mol; O: 1.6/16 = 0.1 mol",
     "Divide by 0.1: C = 2, H = 6, O = 1", "Empirical formula = C₂H₆O"],
    why="CH₃O uses 8 instead of 16 for oxygen. C₂H₃O uses 2 g mol⁻¹ (H₂) for hydrogen atoms. C₄H₁₂O₂ has the "
        "right ratio but is not the simplest one, so it is not an empirical formula.",
    ncert=f"{REF1}, empirical and molecular formula", seconds=40, checked=True)

add("Mole concept", B, "statement_pair",
    sp("One mole of a substance contains exactly 6.02214076 × 10²³ elementary entities (atoms, molecules, ions "
       "or other particles).",
       "The molar mass of water, 18 g mol⁻¹, is the mass of a single water molecule expressed in grams."),
    SP_, "Definition of the mole; molar mass",
    "Under the present SI definition, one mole contains exactly 6.02214076 × 10²³ elementary entities "
    "(the Avogadro number), so Statement I is true. The molar mass is the mass of one mole of a substance in "
    "grams; one water molecule has a mass of 18 u (about 2.99 × 10⁻²³ g), not 18 g. Statement II is false.",
    ["I: SI definition of the mole → true",
     "II: 18 g is the mass of 6.022 × 10²³ molecules; one molecule weighs 18 u → false"],
    answer="C",
    why="Statement I is the defining statement of the mole. Statement II confuses the mass of one molecule "
        "(18 u) with the mass of one mole (18 g).",
    ncert=f"{REF1}, mole concept and molar masses", seconds=35)

x_c = 20 / 10
y_h = (30 / 10 - x_c) * 4
assert (x_c, y_h) == (2, 4)
assert (2 + 2 / 2) == 3  # C2H2 if O2 needed were wrongly taken as x + y/2
add("Stoichiometry", I, "numerical",
    "10 mL of a gaseous hydrocarbon needs exactly 30 mL of oxygen for complete combustion and gives 20 mL of "
    "carbon dioxide. All volumes are measured at the same temperature and pressure, and the water formed "
    "condenses to a liquid. The molecular formula of the hydrocarbon is:",
    Opts("D", "C₂H₄", ["C₂H₂", "C₂H₆", "CH₄"]),
    "Combustion of a gaseous hydrocarbon: Gay-Lussac's law and Avogadro's law",
    "At the same temperature and pressure, volumes of gases are in the ratio of their moles. For "
    "CₓHᵧ + (x + y/4) O₂ → x CO₂ + (y/2) H₂O(l), the CO₂ volume fixes x and the O₂ volume then fixes y.",
    ["CO₂: 10x = 20 → x = 2", "O₂: 10(x + y/4) = 30 → x + y/4 = 3 → y = 4", "Formula = C₂H₄"],
    why="C₂H₂ follows from taking the oxygen needed as x + y/2 instead of x + y/4. C₂H₆ would need "
        "35 mL of O₂, and CH₄ would give only 10 mL of CO₂.",
    ncert=f"{REF1}, Gay-Lussac's law of gaseous volumes and Avogadro's law; stoichiometry", seconds=75,
    checked=True)

m_alsul = 2 * 27 + 3 * (32 + 4 * 16)
n_salt = 34.2 / m_alsul
assert m_alsul == 342 and close(n_salt, 0.1)
assert close(3 * n_salt * NA, 1.807e23) and close(n_salt * NA, 6.022e22) and close(2 * n_salt * NA, 1.204e23) \
    and close(12 * n_salt * NA, 7.226e23)
add("Mole concept", I, "numerical",
    "The number of sulphate ions present in 34.2 g of aluminium sulphate, Al₂(SO₄)₃, is "
    "(Al = 27, S = 32, O = 16, Nₐ = 6.022 × 10²³ mol⁻¹):",
    Opts("B", "1.807 × 10²³", ["6.022 × 10²²", "1.204 × 10²³", "7.226 × 10²³"]),
    "Moles of ions in a given mass of an ionic compound",
    "Find the moles of the formula unit from its molar mass; each Al₂(SO₄)₃ contains three SO₄²⁻ ions.",
    ["M(Al₂(SO₄)₃) = 54 + 3 × 96 = 342 g mol⁻¹", "n = 34.2/342 = 0.1 mol",
     "n(SO₄²⁻) = 3 × 0.1 = 0.3 mol → 0.3 × 6.022 × 10²³ = 1.807 × 10²³"],
    why="6.022 × 10²² is the number of formula units. 1.204 × 10²³ is the number of Al³⁺ ions. "
        "7.226 × 10²³ is the number of oxygen atoms.",
    ncert=f"{REF1}, mole concept and molar masses", seconds=45, checked=True)

add("Empirical and molecular formulae", I, "direct",
    "Which of the following pairs of compounds have the same empirical formula but different molecular "
    "formulae?",
    Opts("C", "Glucose (C₆H₁₂O₆) and methanal (HCHO)",
         ["Ethane (C₂H₆) and ethene (C₂H₄)", "Methanol (CH₃OH) and ethanol (C₂H₅OH)",
          "Water (H₂O) and hydrogen peroxide (H₂O₂)"]),
    "Empirical formula as the simplest whole-number ratio of atoms",
    "Dividing C₆H₁₂O₆ by 6 gives CH₂O, and methanal is CH₂O itself, so both have the empirical formula CH₂O "
    "while their molecular formulae differ.",
    ["Glucose: C₆H₁₂O₆ → CH₂O; methanal: CH₂O → same empirical formula",
     "Ethane CH₃ vs ethene CH₂; methanol CH₄O vs ethanol C₂H₆O; water H₂O vs H₂O₂ HO → all differ"],
    why="In each other pair the simplest ratios are different: CH₃ and CH₂; CH₄O and C₂H₆O; H₂O and HO.",
    ncert=f"{REF1}, empirical and molecular formula", seconds=40)

n_eth = 2.3 / 46
assert close(3 * n_eth * 22.7, 3.41) and close(n_eth * 22.7, 1.135) and close(2 * n_eth * 22.7, 2.27) \
    and close(6 * n_eth * 22.7, 6.81)
add("Stoichiometry", I, "numerical",
    "The volume of oxygen, measured at STP, needed to burn 2.3 g of ethanol completely, "
    "C₂H₅OH(l) + 3O₂(g) → 2CO₂(g) + 3H₂O(l), is (C = 12, H = 1, O = 16; molar volume of a gas at STP = "
    "22.7 L mol⁻¹):",
    Opts("A", "3.41 L", ["1.14 L", "2.27 L", "6.81 L"]),
    "Mass–volume relationship from a balanced equation",
    "Convert the mass of ethanol into moles, use the 1 : 3 mole ratio from the equation, and multiply the moles "
    "of O₂ by the molar volume.",
    ["M(C₂H₅OH) = 46 g mol⁻¹; n = 2.3/46 = 0.05 mol", "n(O₂) = 3 × 0.05 = 0.15 mol",
     "V(O₂) = 0.15 × 22.7 = 3.41 L"],
    why="1.14 L ignores the 1 : 3 ratio. 2.27 L is the volume of CO₂ formed (1 : 2). 6.81 L counts moles of "
        "oxygen atoms instead of O₂ molecules.",
    ncert=f"{REF1}, stoichiometry and stoichiometric calculations", seconds=50, checked=True)

# Mg + 2HCl -> MgCl2 + H2 ; 2Al + 6HCl -> 2AlCl3 + 3H2 ; 24x + 27y = 0.78 ; x + 1.5y = 0.080/2
n_h2 = 0.080 / 2
y_al = (0.78 - 24 * n_h2) / (27 - 24 * 1.5)
x_mg = n_h2 - 1.5 * y_al
assert close(y_al, 0.02) and close(x_mg, 0.01) and close(27 * y_al, 0.54) and close(24 * x_mg, 0.24)
y_wrong = (0.78 - 24 * n_h2) / (27 - 24 * 3)  # Al wrongly taken to give 3 mol H2 per mol
assert close(27 * y_wrong, 0.108) and close(27 * n_h2 / 1.5, 0.72)
add("Stoichiometry", A, "numerical",
    "0.78 g of a mixture of magnesium and aluminium powders reacts completely with an excess of dilute "
    "hydrochloric acid, and 0.080 g of hydrogen gas is evolved: Mg + 2HCl → MgCl₂ + H₂; "
    "2Al + 6HCl → 2AlCl₃ + 3H₂. The mass of aluminium in the mixture is (Mg = 24, Al = 27, H = 1):",
    Opts("D", "0.54 g", ["0.24 g", "0.108 g", "0.72 g"]),
    "Analysis of a mixture using two simultaneous mole equations",
    "Let the mixture contain x mol Mg and y mol Al. One equation comes from the total mass, the other from the "
    "total hydrogen: each mole of Mg gives 1 mol H₂, each mole of Al gives 1.5 mol H₂.",
    ["n(H₂) = 0.080/2 = 0.040 mol", "24x + 27y = 0.78 and x + 1.5y = 0.040",
     "From the second, 24x = 0.96 − 36y → 0.96 − 36y + 27y = 0.78 → y = 0.020 mol, x = 0.010 mol",
     "Mass of Al = 0.020 × 27 = 0.54 g (Mg = 0.24 g; check 0.54 + 0.24 = 0.78 g)"],
    why="0.24 g is the mass of magnesium. 0.108 g comes from taking 3 mol H₂ per mole of Al instead of 1.5. "
        "0.72 g assumes all the hydrogen came from aluminium.",
    ncert=f"{REF1}, stoichiometry and stoichiometric calculations", seconds=150, checked=True)

loss_per = 18 + 44  # 2NaHCO3 (168 g) -> Na2CO3 + H2O + CO2 : 62 g lost
m_bicarb = 0.124 * 168 / loss_per
assert close(m_bicarb, 0.336) and close(100 * 0.124 * 168 / 44, 47.3) and close(100 * 0.124 * 84 / 62, 16.8)
assert close(100 - 100 * m_bicarb, 66.4)
add("Stoichiometry", A, "numerical",
    "1.00 g of a mixture of sodium carbonate and sodium hydrogencarbonate is heated strongly until its mass "
    "becomes constant. Only the hydrogencarbonate decomposes: 2NaHCO₃(s) → Na₂CO₃(s) + H₂O(g) + CO₂(g). "
    "The loss in mass is 0.124 g. The percentage of NaHCO₃ in the mixture is (Na = 23, C = 12, O = 16, H = 1):",
    Opts("B", "33.6%", ["47.3%", "16.8%", "66.4%"]),
    "Stoichiometry of a decomposition: mass lost by a mixture",
    "Both the water and the carbon dioxide escape. 2 mol NaHCO₃ (168 g) lose 18 + 44 = 62 g, so the loss "
    "fixes the mass of NaHCO₃ present.",
    ["Mass lost per 168 g NaHCO₃ = 62 g", "m(NaHCO₃) = 0.124 × 168/62 = 0.336 g",
     "Percentage = 0.336/1.00 × 100 = 33.6%"],
    why="47.3% counts only CO₂ (44 g) as the loss. 16.8% uses 84 g of NaHCO₃ per 62 g lost, ignoring the 2 in "
        "the equation. 66.4% is the percentage of Na₂CO₃.",
    ncert=f"{REF1}, stoichiometry and stoichiometric calculations", seconds=120, checked=True)

n_fe2o3 = 16.0 / 160
assert close(3 * n_fe2o3, 0.3) and close(2 * n_fe2o3 * 56, 11.2) and close(3 * n_fe2o3 * 44, 13.2)
assert close(3 * n_fe2o3 * 22.7, 6.81) and 11.2 < 16.0
add("Stoichiometry", A, "multi_statement",
    ms("16.0 g of iron(III) oxide is reduced completely by carbon monoxide: Fe₂O₃(s) + 3CO(g) → 2Fe(s) + "
       "3CO₂(g). Which of the following statements are correct? (Fe = 56, C = 12, O = 16; molar volume of a gas "
       "at STP = 22.7 L mol⁻¹)",
       ["0.3 mol of carbon monoxide is consumed.", "11.2 g of iron is formed.",
        "13.2 g of carbon dioxide is formed.", "The carbon dioxide formed occupies 4.54 L at STP.",
        "The mass of iron formed is greater than the mass of iron(III) oxide taken."]),
    multi("D", {"a": True, "b": True, "c": True, "d": False, "e": False},
          ["(a), (b) and (d) only", "(b), (c) and (e) only", "(a), (b), (c) and (d) only"]),
    "Mole and mass relationships from a balanced equation",
    "16.0 g of Fe₂O₃ (M = 160) is 0.1 mol. The equation gives 0.3 mol CO consumed, 0.2 mol Fe and 0.3 mol CO₂ "
    "formed.",
    ["(a) 3 × 0.1 = 0.3 mol CO → true", "(b) 0.2 × 56 = 11.2 g Fe → true", "(c) 0.3 × 44 = 13.2 g CO₂ → true",
     "(d) 0.3 × 22.7 = 6.81 L, not 4.54 L → false", "(e) 11.2 g of Fe < 16.0 g of Fe₂O₃ (oxygen removed) → false"],
    why="Any option with (d) or (e) is wrong; (a), (b) and (c) are all true.",
    ncert=f"{REF1}, stoichiometry and stoichiometric calculations", seconds=110)

# ==================================================================== 2. Atomic Structure
topic("Atomic Structure")
REF2 = f"{C11}, 'Structure of Atom'"

add("Dual nature and uncertainty", B, "direct",
    "The electron microscope, which gives very highly magnified images, works on the basis of:",
    Opts("B", "the wave-like behaviour of electrons",
         ["the photoelectric effect", "the particle nature of light (photons)",
          "the Heisenberg uncertainty principle"]),
    "Dual behaviour of matter: an application",
    "de Broglie's prediction that moving electrons behave as waves was confirmed experimentally. NCERT notes "
    "that the electron microscope is based on this wave-like behaviour of electrons, just as an ordinary "
    "microscope uses the wave nature of light.",
    ["Moving electrons have a de Broglie wavelength λ = h/mv",
     "This wave behaviour (diffraction) is used in the electron microscope"],
    why="The photoelectric effect and photons concern the particle nature of light. The uncertainty principle "
        "is a consequence of dual behaviour, not the working principle of the microscope.",
    ncert=f"{REF2}, dual behaviour of matter", seconds=25)

add("Bohr model and hydrogen spectrum", B, "direct",
    "The lines of the Balmer series in the emission spectrum of atomic hydrogen lie in the:",
    Opts("D", "visible region", ["ultraviolet region", "infrared region", "microwave region"]),
    "Spectral series of hydrogen and their regions",
    "The Balmer series (transitions ending at n = 2) is the only series of hydrogen that appears in the visible "
    "region. The Lyman series (ending at n = 1) is in the ultraviolet and the Paschen, Brackett and Pfund "
    "series lie in the infrared.",
    ["Balmer: n₁ = 2 → visible", "Lyman: n₁ = 1 → ultraviolet; Paschen and beyond → infrared"],
    why="Ultraviolet belongs to the Lyman series, infrared to the Paschen, Brackett and Pfund series; no "
        "hydrogen series lies in the microwave region.",
    ncert=f"{REF2}, line spectrum of hydrogen", seconds=20)

add("Electronic configuration", B, "direct",
    "Each box below represents one 2p orbital. Which arrangement of the three 2p electrons of a ground-state "
    "nitrogen atom follows Hund's rule of maximum multiplicity?",
    Opts("A", "[↑] [↑] [↑]", ["[↑↓] [↑] [  ]", "[↑] [↓] [↑]", "[↑↓↑] [  ] [  ]"]),
    "Hund's rule of maximum multiplicity",
    "Electrons enter orbitals of equal energy singly, with parallel spins, before any pairing takes place. The "
    "three 2p electrons of nitrogen therefore occupy the three 2p orbitals singly with the same spin.",
    ["Three degenerate 2p orbitals, three electrons", "One electron in each, spins parallel → [↑] [↑] [↑]"],
    why="[↑↓] [↑] [ ] pairs electrons while an orbital is empty. [↑] [↓] [↑] does not have parallel spins. "
        "[↑↓↑] puts three electrons in one orbital, breaking the Pauli exclusion principle.",
    ncert=f"{REF2}, filling of orbitals: Hund's rule", seconds=25)

add("Dual nature and uncertainty", B, "match_list",
    lists("Match List-I (relation) with List-II (what it expresses).",
          ["λ = h/mv", "Δx × Δp ≥ h/4π", "E = hν",
           "ν̄ = 109 677 (1/n₁² − 1/n₂²) cm⁻¹"],
          ["Planck's quantum theory", "Rydberg's expression for the lines of the hydrogen spectrum",
           "de Broglie relation", "Heisenberg's uncertainty principle"]),
    match("C", M("III IV I II"), [M("IV III I II"), M("III IV II I"), M("I IV III II")]),
    "Key relations of atomic structure",
    "λ = h/mv links the wavelength of a moving particle to its momentum (de Broglie). Δx·Δp ≥ h/4π limits "
    "how precisely position and momentum can be known together (Heisenberg). E = hν gives the energy of a "
    "quantum (Planck). The wavenumber expression with 109 677 cm⁻¹ gives all the lines of the hydrogen "
    "spectrum (Rydberg).",
    ["A → III (de Broglie)", "B → IV (Heisenberg)", "C → I (Planck)", "D → II (Rydberg)"],
    why="The other codes swap de Broglie with Heisenberg, Planck with Rydberg, or de Broglie with Planck.",
    ncert=f"{REF2}, Planck's quantum theory, hydrogen spectrum, dual behaviour and uncertainty principle",
    seconds=35)

add("Bohr model and hydrogen spectrum", I, "multi_statement",
    ms("Which of the following are limitations of Bohr's model of the atom?",
       ["It cannot explain the fine structure (doublets, closely spaced lines) of the hydrogen spectrum.",
        "It cannot explain the spectra of atoms with more than one electron, such as helium.",
        "It cannot explain the splitting of spectral lines in a magnetic field (Zeeman effect) or an electric "
        "field (Stark effect).",
        "It cannot account for the line spectrum of the hydrogen atom.",
        "It is consistent with the dual behaviour of matter and the Heisenberg uncertainty principle."]),
    multi("B", {"a": True, "b": True, "c": True, "d": False, "e": False},
          ["(a) and (b) only", "(a), (b), (c) and (e) only", "(b), (c) and (d) only"]),
    "Limitations of Bohr's model",
    "Bohr's model explains the line spectrum of hydrogen (and of hydrogen-like ions), but it fails for the fine "
    "structure, for multi-electron atoms and for the Zeeman and Stark effects. It also ignores the dual "
    "behaviour of matter and contradicts the uncertainty principle, since it gives the electron a definite "
    "orbit.",
    ["(a), (b), (c): limitations listed in NCERT → true",
     "(d) Bohr's model does explain the hydrogen line spectrum → false",
     "(e) Definite orbits are inconsistent with dual behaviour and the uncertainty principle → false"],
    why="(d) and (e) are false, and (a) and (b) only leaves out the true statement (c).",
    ncert=f"{REF2}, limitations of Bohr's model", seconds=60)

add("Bohr model and hydrogen spectrum", I, "statement_pair",
    sp("Rubidium, caesium, thallium, indium, gallium and scandium were discovered when their minerals were "
       "analysed by spectroscopic methods.",
       "In an absorption spectrum, bright lines appear on a dark background."),
    SP_, "Emission and absorption spectra; spectroscopy",
    "Each element has a characteristic line spectrum, a 'fingerprint', and NCERT names rubidium, caesium, "
    "thallium, indium, gallium and scandium as elements discovered by spectroscopic analysis. Statement I is "
    "true. An absorption spectrum is like the photographic negative of an emission spectrum: dark lines appear "
    "on a bright continuous background where the radiation has been absorbed. Statement II describes an "
    "emission spectrum and is false.",
    ["I: elements discovered by spectroscopy → true",
     "II: absorption spectrum = dark lines on a bright background → false"],
    answer="C",
    why="Statement II interchanges the appearance of absorption and emission spectra.",
    ncert=f"{REF2}, emission and absorption spectra", seconds=40)

MN_CONFIG = [("1s", 2), ("2s", 2), ("2p", 6), ("3s", 2), ("3p", 6), ("4s", 2), ("3d", 5)]


def ml0_count(config):
    """Electrons with ml = 0: all s electrons; for p⁶ two; for half-filled d⁵ exactly one."""
    total = 0
    for sub, ne in config:
        if sub.endswith("s"):
            total += ne
        elif sub.endswith("p"):
            assert ne == 6
            total += 2
        else:
            assert ne == 5  # Hund: one electron in each 3d orbital, so exactly one has ml = 0
            total += 1
    return total


assert sum(ne for _, ne in MN_CONFIG) == 25 and ml0_count(MN_CONFIG) == 13
add("Quantum numbers and orbitals", I, "numerical",
    "In a ground-state manganese atom (Z = 25), the number of electrons that have the magnetic quantum number "
    "mₗ = 0 is:",
    Opts("D", "13", ["12", "14", "8"]),
    "Magnetic quantum number and electronic configuration",
    "Every s orbital has mₗ = 0, each p subshell has one orbital with mₗ = 0, and each d subshell has one. "
    "Mn is 1s² 2s² 2p⁶ 3s² 3p⁶ 3d⁵ 4s²; its five 3d electrons occupy the five 3d orbitals singly (Hund's "
    "rule), so exactly one of them is in the mₗ = 0 orbital.",
    ["s electrons: 1s², 2s², 3s², 4s² → 8", "p subshells: one mₗ = 0 orbital each in 2p and 3p, both full → 4",
     "3d⁵: one electron in the mₗ = 0 orbital → 1", "Total = 8 + 4 + 1 = 13"],
    why="12 leaves out the 3d electron. 14 puts two 3d electrons in the mₗ = 0 orbital, which Hund's rule does "
        "not allow for 3d⁵. 8 counts only the s electrons.",
    ncert=f"{REF2}, quantum numbers and electronic configuration of atoms", seconds=75, checked=True)

add("Electronic configuration", I, "assertion_reason",
    ar("In a multi-electron atom, a 2s electron is held more tightly by the nucleus (has lower energy) than a 2p "
       "electron.",
       "An s electron penetrates closer to the nucleus than a p electron of the same shell, so it is shielded "
       "less and experiences a larger effective nuclear charge."),
    AR_, "Energies of orbitals: penetration and shielding",
    "In atoms with more than one electron, orbitals of the same shell differ in energy. The s orbital is more "
    "penetrating than the p orbital, so an s electron is less shielded by the inner electrons, feels a larger "
    "effective nuclear charge, and is more strongly attracted. Hence 2s is lower in energy than 2p. R explains A.",
    ["A: E(2s) < E(2p) in multi-electron atoms → true",
     "R: greater penetration of s → less shielding, larger Zeff → true and explains A"],
    answer="A",
    why="Both statements are true and R is the reason given by NCERT for the order s < p < d < f within a shell.",
    ncert=f"{REF2}, energies of orbitals", seconds=45)

add("Quantum numbers and orbitals", I, "statement_pair",
    sp("A Bohr orbit is a definite circular path of the electron around the nucleus, whereas an atomic orbital "
       "describes the region around the nucleus in which there is a probability of finding the electron.",
       "The boundary surface diagram of an orbital encloses a region in which the probability of finding the "
       "electron is very high, for example about 90%."),
    SP_, "Orbit versus orbital; boundary surface diagrams",
    "NCERT stresses that an orbit and an orbital are not the same: an orbit is Bohr's circular path, while an "
    "orbital is a one-electron wave function ψ, with ψ² giving the probability density. A boundary surface "
    "is drawn so that it encloses a region of high probability, such as 90%, of finding the electron. Both "
    "statements are true.",
    ["I: orbit = definite path; orbital = probability region → true",
     "II: boundary surface encloses ~90% probability → true"],
    answer="A",
    why="Neither statement is false; a boundary surface cannot enclose 100% probability, so NCERT uses a high "
        "value such as 90%.",
    ncert=f"{REF2}, quantum mechanical model; shapes of atomic orbitals", seconds=35)

m_e = 9.11e-31
dp = math.sqrt(H_PLANCK / (4 * math.pi))      # Δx·Δp = h/4π with Δx = Δp
dv = dp / m_e
assert close(dv, (1 / (2 * m_e)) * math.sqrt(H_PLANCK / math.pi), 1e-9)
assert not close(dv, (1 / m_e) * math.sqrt(H_PLANCK / math.pi), 0.1)
assert not close(dv, 0.5 * math.sqrt(H_PLANCK / (math.pi * m_e)), 0.1)
add("Dual nature and uncertainty", A, "numerical",
    "For a moving particle of mass m, the uncertainty in its position (Δx) is numerically equal to the "
    "uncertainty in its momentum (Δp). Using Δx × Δp = h/4π, the minimum uncertainty in its velocity is:",
    Opts("A", "(1/2m)√(h/π)", ["(1/m)√(h/π)", "½√(h/πm)", "h/(4πm)"]),
    "Heisenberg's uncertainty principle",
    "With Δx = Δp, the product becomes (Δp)² = h/4π. Then Δp = √(h/4π) = ½√(h/π), and Δv = Δp/m.",
    ["(Δp)² = h/4π → Δp = √(h/4π) = ½√(h/π)", "Δv = Δp/m = (1/2m)√(h/π)"],
    why="(1/m)√(h/π) drops the factor 4 under the root. ½√(h/πm) sets Δx equal to Δv instead of Δp. "
        "h/(4πm) takes Δp itself as 1 instead of solving for it.",
    ncert=f"{REF2}, Heisenberg's uncertainty principle", seconds=75, checked=True)

from fractions import Fraction as F  # noqa: E402

he_line = 4 * (F(1, 16) - F(1, 36))
assert he_line == F(1, 4) - F(1, 9)
assert he_line != F(1, 16) - F(1, 36) and he_line != F(1, 64) - F(1, 144) and he_line != F(1, 1) - F(1, 4)
add("Bohr model and hydrogen spectrum", A, "numerical",
    "The wavenumber of a spectral line of a hydrogen-like species is ν̄ = R_H Z² (1/n₁² − 1/n₂²). Which "
    "transition in the hydrogen atom gives a line of the same wavelength as the transition from n = 6 to n = 4 "
    "in the He⁺ ion (Z = 2)?",
    Opts("C", "n = 3 → n = 2", ["n = 6 → n = 4", "n = 12 → n = 8", "n = 2 → n = 1"]),
    "Rydberg equation for hydrogen-like species",
    "Same wavelength means the same value of Z²(1/n₁² − 1/n₂²). For He⁺, Z² = 4, so dividing both n values "
    "by Z = 2 gives the matching hydrogen transition.",
    ["He⁺: 4 × (1/16 − 1/36) = 4 × 20/576 = 5/36", "H: 1/n₁² − 1/n₂² = 5/36 → n₁ = 2, n₂ = 3 (1/4 − 1/9 = 5/36)",
     "The line is the first Balmer line of hydrogen (n = 3 → 2)"],
    shortcut="For He⁺ → H, halve both quantum numbers: 6 → 4 becomes 3 → 2.",
    why="n = 6 → 4 in hydrogen ignores the Z² factor. n = 12 → 8 multiplies by Z instead of dividing. "
        "n = 2 → 1 gives 3/4, far larger than 5/36.",
    ncert=f"{REF2}, Bohr's model for hydrogen-like species; line spectrum of hydrogen", seconds=90,
    checked=True)

add("Electronic configuration", A, "multi_statement",
    ms("Which of the following statements about ground-state species are correct? "
       "(Z: Sc = 21, Ti = 22, Mn = 25, Fe = 26, Ni = 28, Cu = 29)",
       ["Mn²⁺ and Fe³⁺ have the same number of 3d electrons.",
        "A copper atom has one unpaired electron.",
        "The electronic configuration of Ti²⁺ is [Ar] 3d².",
        "The electronic configuration of a nickel atom is [Ar] 3d¹⁰.",
        "Sc³⁺ has one unpaired electron."]),
    multi("B", {"a": True, "b": True, "c": True, "d": False, "e": False},
          ["(a) and (b) only", "(a), (b), (c) and (d) only", "(b), (c) and (e) only"]),
    "Electronic configurations of atoms and ions",
    "Mn ([Ar] 3d⁵ 4s²) loses 4s² to give Mn²⁺ 3d⁵; Fe ([Ar] 3d⁶ 4s²) loses 4s² and one 3d electron to give "
    "Fe³⁺ 3d⁵. Cu is [Ar] 3d¹⁰ 4s¹, with the single 4s electron unpaired. Ti ([Ar] 3d² 4s²) loses the 4s "
    "electrons to give Ti²⁺ [Ar] 3d². Ni is [Ar] 3d⁸ 4s², and Sc³⁺ is [Ar] with no unpaired electron.",
    ["(a) both 3d⁵ → true", "(b) 4s¹ electron unpaired → true", "(c) Ti²⁺ = [Ar] 3d² → true",
     "(d) Ni = [Ar] 3d⁸ 4s² → false", "(e) Sc³⁺ = [Ar], no unpaired electron → false"],
    why="Options with (d) or (e) are wrong, and (a) and (b) only misses the true statement (c).",
    ncert=f"{REF2}, electronic configuration of atoms; stability of filled and half-filled subshells",
    seconds=90)

add("Quantum numbers and orbitals", A, "match_list",
    lists("Match List-I (atomic orbital) with List-II (its nodes), taking z as the vertical axis.",
          ["2p_z", "3d_xy", "3s", "2s"],
          ["One spherical (radial) node and no nodal plane", "The xz and yz planes are nodal planes",
           "Two spherical (radial) nodes and no nodal plane", "The xy plane is a nodal plane"]),
    match("B", M("IV II III I"), [M("II IV III I"), M("IV II I III"), M("I II III IV")]),
    "Radial and angular nodes of orbitals",
    "An orbital has n − l − 1 radial (spherical) nodes and l angular nodes (nodal planes for p and these d "
    "orbitals). 2p_z: 0 radial, 1 angular – the xy plane. 3d_xy: 0 radial, 2 angular – its lobes lie between "
    "the x and y axes, so the planes containing the z axis and the x axis (xz) and the z axis and the y axis "
    "(yz) are nodal. 3s: 2 radial nodes. 2s: 1 radial node.",
    ["2p_z → xy plane (IV)", "3d_xy → xz and yz planes (II)", "3s → 3 − 0 − 1 = 2 radial nodes (III)",
     "2s → 2 − 0 − 1 = 1 radial node (I)"],
    why="The other codes give 2p_z two nodal planes, swap the radial-node counts of 2s and 3s, or give 2p_z a "
        "spherical node.",
    ncert=f"{REF2}, shapes of atomic orbitals and nodes", seconds=75)

# ==================================================================== 3. Chemical Bonding and Molecular Structure
topic("Chemical Bonding and Molecular Structure")
REF3 = f"{C11}, 'Chemical Bonding and Molecular Structure'"

LOW = [("s1", 2, 1), ("s1*", 2, -1), ("s2", 2, 1), ("s2*", 2, -1), ("pi", 4, 1), ("sz", 2, 1), ("pi*", 4, -1),
       ("sz*", 2, -1)]
HIGH = [("s1", 2, 1), ("s1*", 2, -1), ("s2", 2, 1), ("s2*", 2, -1), ("sz", 2, 1), ("pi", 4, 1), ("pi*", 4, -1),
        ("sz*", 2, -1)]


def mo(n_electrons):
    """(bond order, unpaired electrons) from NCERT's MO energy orders (N2-type up to 14 electrons)."""
    left, nb, na, unpaired = n_electrons, 0, 0, 0
    for _, cap, sign in (LOW if n_electrons <= 14 else HIGH):
        k = min(cap, left)
        left -= k
        if sign > 0:
            nb += k
        else:
            na += k
        unpaired += (k % 2) if cap == 2 else (k if k <= 2 else 4 - k)
    return F(nb - na, 2), unpaired


SPECIES = {"H2+": 1, "Li2": 6, "B2": 10, "C2": 12, "N2+": 13, "N2": 14, "N2-": 15, "O2+": 15, "O2": 16,
           "O2-": 17, "O2 2-": 18}
assert mo(14) == (3, 0) and mo(16) == (2, 2) and mo(10) == (1, 2) and mo(12) == (2, 0)

add("Hybridisation and resonance", B, "direct",
    "When more than one Lewis structure can be drawn for a molecule, formal charges help to choose the most "
    "likely one. According to this idea, the lowest-energy structure is generally the one that has:",
    Opts("D", "the smallest formal charges on the atoms",
         ["the largest formal charges on the atoms", "the largest number of lone pairs on the central atom",
          "a positive formal charge on the most electronegative atom"]),
    "Formal charge and the choice of Lewis structure",
    "Formal charge = (valence electrons in the free atom) − (non-bonding electrons) − ½(bonding electrons). "
    "NCERT notes that formal charges help select the lowest-energy structure from several possible Lewis "
    "structures: generally it is the one with the smallest formal charges on the atoms.",
    ["Formal charge = V − L − ½S", "Lowest energy ↔ smallest formal charges"],
    why="Large formal charges, or a positive charge on the most electronegative atom, make a structure less "
        "stable; the number of lone pairs is not the criterion.",
    ncert=f"{REF3}, formal charge", seconds=25)

add("Molecular orbital theory", B, "match_list",
    lists("Match List-I (type of molecular orbital) with List-II (its description).",
          ["Bonding molecular orbital", "Antibonding molecular orbital", "σ molecular orbital",
           "π molecular orbital"],
          ["Formed by sideways overlap; its electron density lies above and below the internuclear axis",
           "Formed by addition (constructive interference) of the atomic wave functions; lower in energy than "
           "the combining atomic orbitals",
           "Symmetrical about the internuclear axis",
           "Formed by subtraction of the atomic wave functions; has a nodal plane between the nuclei"]),
    match("B", M("II IV III I"), [M("IV II III I"), M("II IV I III"), M("III IV II I")]),
    "Formation and types of molecular orbitals (LCAO)",
    "Adding the wave functions of the combining atoms builds up electron density between the nuclei and gives "
    "a bonding MO of lower energy. Subtracting them gives an antibonding MO with a node between the nuclei and "
    "higher energy. σ MOs are symmetrical about the internuclear axis; π MOs, formed by sideways overlap of p "
    "orbitals, have electron density above and below the axis.",
    ["A → II (addition, lower energy)", "B → IV (subtraction, node between nuclei)",
     "C → III (cylindrical symmetry about the axis)", "D → I (sideways overlap)"],
    why="The other codes interchange bonding with antibonding, or σ with π.",
    ncert=f"{REF3}, formation of molecular orbitals; types of molecular orbitals", seconds=40)

add("Hydrogen and metallic bonding", B, "assertion_reason",
    ar("At room temperature water is a liquid, whereas hydrogen sulphide, a heavier molecule, is a gas.",
       "Water molecules are held together by intermolecular hydrogen bonds, whereas sulphur is not "
       "electronegative enough for H₂S molecules to form such hydrogen bonds."),
    AR_, "Hydrogen bonding and physical state",
    "A hydrogen bond forms when hydrogen is attached to a highly electronegative atom such as F, O or N. "
    "Intermolecular hydrogen bonds associate water molecules, so much more energy is needed to separate them; "
    "H₂S has only weak van der Waals forces. That is why water is a liquid and H₂S a gas at room temperature. "
    "R explains A.",
    ["A: H₂O liquid, H₂S gas at room temperature → true",
     "R: O–H···O hydrogen bonding; S is not electronegative enough → true and explains A"],
    answer="A",
    why="Without hydrogen bonding, the heavier H₂S would be expected to be the less volatile; R accounts for "
        "the observed order.",
    ncert=f"{REF3}, hydrogen bonding", seconds=35)

add("Hybridisation and resonance", B, "direct",
    "The phosphorus atom in PCl₅ is sp³d hybridised. The atomic orbitals of phosphorus that take part in this "
    "hybridisation are:",
    Opts("C", "3s, 3pₓ, 3p_y, 3p_z and 3d_z²",
         ["3s, 3pₓ, 3p_y, 3p_z and 3d_x²−y²", "3s, 3pₓ, 3p_y, 3p_z and 4s", "3s, 3pₓ, 3p_y, 3d_z² and 3d_x²−y²"]),
    "Hybridisation involving d orbitals",
    "In the excited state phosphorus has five half-filled orbitals: one 3s, three 3p and one 3d. NCERT states "
    "that the d orbital used in sp³d hybridisation is d_z², whose lobes point along the z axis and so suit the "
    "two axial positions of the trigonal bipyramid. (sp³d² uses both d_z² and d_x²−y².)",
    ["sp³d = one s + three p + one d", "The d orbital is 3d_z²"],
    why="d_x²−y² is used along with d_z² only in sp³d². 4s is not a valence orbital that hybridises with 3s. "
        "Using only two 3p orbitals with two d orbitals is not sp³d.",
    ncert=f"{REF3}, hybridisation involving s, p and d orbitals: PCl₅", seconds=30)

# CH2=CH–C≡CH : carbons 1,2 have a double bond (sp2); carbons 3,4 have a triple bond (sp)
vinylacetylene = {"C1": "sp2", "C2": "sp2", "C3": "sp", "C4": "sp"}
assert Counter(vinylacetylene.values()) == Counter({"sp2": 2, "sp": 2})
add("Hybridisation and resonance", B, "numerical",
    "The numbers of sp² and sp hybridised carbon atoms in but-1-en-3-yne, CH₂=CH–C≡CH, are respectively:",
    Opts("B", "2 and 2", ["3 and 1", "1 and 3", "2 and 0"]),
    "Hybridisation of carbon from the bonds it forms",
    "A carbon atom with one double bond (three σ bonds) is sp²; a carbon atom with a triple bond (two σ "
    "bonds) is sp. The two carbons of C=C are sp², and the two carbons of C≡C are sp.",
    ["CH₂= and =CH– : sp² (2 atoms)", "–C≡ and ≡CH : sp (2 atoms)"],
    why="3 and 1 or 1 and 3 assign the middle carbons to the wrong bond type; 2 and 0 treats the C≡C carbons "
        "as sp³.",
    ncert=f"{REF3}, hybridisation; sp and sp² hybridisation in C₂H₂ and C₂H₄", seconds=30, checked=True)

bo = {s: mo(SPECIES[s])[0] for s in ("O2+", "O2", "O2-", "O2 2-")}
assert bo["O2+"] > bo["O2"] > bo["O2-"] > bo["O2 2-"] and bo["O2+"] == F(5, 2) and bo["O2 2-"] == 1
add("Molecular orbital theory", I, "direct",
    "Which of the following shows the oxygen species in order of INCREASING O–O bond length?",
    Opts("D", "O₂⁺ < O₂ < O₂⁻ < O₂²⁻",
         ["O₂²⁻ < O₂⁻ < O₂ < O₂⁺", "O₂ < O₂⁺ < O₂⁻ < O₂²⁻", "O₂⁺ < O₂⁻ < O₂ < O₂²⁻"]),
    "Bond order and bond length from MO theory",
    "Bond length decreases as bond order increases. From MO theory, the bond orders are O₂⁺ 2.5, O₂ 2, O₂⁻ 1.5 "
    "and O₂²⁻ 1, because each added electron enters an antibonding π* orbital.",
    ["Bond orders: O₂⁺ 2.5 > O₂ 2 > O₂⁻ 1.5 > O₂²⁻ 1",
     "Higher bond order → shorter bond: O₂⁺ < O₂ < O₂⁻ < O₂²⁻"],
    why="O₂²⁻ < … < O₂⁺ is the order of decreasing length. The other two orders misplace O₂⁺ or O₂⁻ relative to "
        "O₂.",
    ncert=f"{REF3}, bond order and bond length; bonding in O₂", seconds=45)

lone = {"XeF4": (8 - 4) // 2, "ClF3": (7 - 3) // 2, "SF4": (6 - 4) // 2, "BrF5": (7 - 5) // 2,
        "OF2": (6 - 2) // 2}
assert lone == {"XeF4": 2, "ClF3": 2, "SF4": 1, "BrF5": 1, "OF2": 2} and (6 - 2) // 2 == 2  # H2O has 2
add("VSEPR shapes", I, "multi_statement",
    ms("In which of the following molecules does the central atom carry the same number of lone pairs as the "
       "oxygen atom in H₂O?",
       ["XeF₄", "ClF₃", "SF₄", "BrF₅", "OF₂"]),
    multi("C", {"a": True, "b": True, "c": False, "d": False, "e": True},
          ["(a), (b) and (c) only", "(b), (d) and (e) only", "(a) and (e) only"]),
    "Counting lone pairs on the central atom (VSEPR)",
    "The oxygen of H₂O has two lone pairs. For each molecule, lone pairs = (valence electrons of the central "
    "atom − electrons used in single bonds)/2.",
    ["XeF₄: (8 − 4)/2 = 2 ✓", "ClF₃: (7 − 3)/2 = 2 ✓", "SF₄: (6 − 4)/2 = 1 ✗", "BrF₅: (7 − 5)/2 = 1 ✗",
     "OF₂: (6 − 2)/2 = 2 ✓"],
    why="SF₄ and BrF₅ each have only one lone pair on the central atom, and (a) and (e) only misses ClF₃.",
    ncert=f"{REF3}, VSEPR theory: molecules with lone pairs", seconds=60)

add("Hybridisation and resonance", I, "assertion_reason",
    ar("All four C–H bonds in methane are identical in length and strength, and the H–C–H angles are all "
       "109.5°.",
       "Carbon uses four equivalent sp³ hybrid orbitals, rather than one 2s and three 2p orbitals, to overlap "
       "with the 1s orbitals of the four hydrogen atoms."),
    AR_, "Why hybridisation is needed to explain methane",
    "If carbon used one 2s and three 2p orbitals directly, one C–H bond would differ from the other three and "
    "the three p-based bonds would be at 90°. Mixing the 2s and three 2p orbitals gives four equivalent sp³ "
    "orbitals pointing to the corners of a tetrahedron, which explains four identical bonds at 109.5°. R "
    "explains A.",
    ["A: four equivalent C–H bonds, tetrahedral angles → true",
     "R: four equivalent sp³ orbitals directed tetrahedrally → true and explains A"],
    answer="A",
    why="R is exactly the explanation NCERT gives for the shape of CH₄.",
    ncert=f"{REF3}, hybridisation: sp³ hybridisation in CH₄", seconds=40)

props = {s: mo(SPECIES[s]) for s in ("N2", "O2", "B2", "C2")}
assert props == {"N2": (3, 0), "O2": (2, 2), "B2": (1, 2), "C2": (2, 0)}
add("Molecular orbital theory", I, "match_list",
    lists("Match List-I (molecule) with List-II (bond order and magnetic behaviour predicted by molecular "
          "orbital theory).",
          ["N₂", "O₂", "B₂", "C₂"],
          ["Bond order 2; diamagnetic", "Bond order 2; paramagnetic", "Bond order 1; paramagnetic",
           "Bond order 3; diamagnetic"]),
    match("B", M("IV II III I"), [M("IV I III II"), M("I II III IV"), M("IV II I III")]),
    "Bond order and magnetism of homonuclear diatomic molecules",
    "Using the energy order in which π2p lies below σ2p_z for B₂, C₂ and N₂, and the reverse for O₂: N₂ has "
    "all electrons paired with bond order 3; O₂ has two unpaired electrons in π* with bond order 2; B₂ has two "
    "unpaired electrons in the π2p orbitals with bond order 1; C₂ has its four π electrons paired with bond "
    "order 2.",
    ["N₂: (10 − 4)/2 = 3, diamagnetic → IV", "O₂: (10 − 6)/2 = 2, two unpaired π* → II",
     "B₂: (6 − 4)/2 = 1, two unpaired π → III", "C₂: (8 − 4)/2 = 2, all paired → I"],
    why="O₂ and C₂ both have bond order 2; the trap is to swap them, but O₂ is paramagnetic and C₂ diamagnetic.",
    ncert=f"{REF3}, bonding in some homonuclear diatomic molecules", seconds=60)

add("Hydrogen and metallic bonding", I, "direct",
    "In which of the following pairs can BOTH compounds form intermolecular hydrogen bonds in the liquid "
    "state?",
    Opts("D", "NH₃ and HF", ["CH₄ and H₂O", "H₂S and HCl", "PH₃ and NH₃"]),
    "Condition for hydrogen bonding",
    "A hydrogen bond needs hydrogen attached to a small, highly electronegative atom (F, O or N), and a lone "
    "pair on such an atom of a neighbouring molecule. NH₃ (N–H) and HF (F–H) both qualify.",
    ["NH₃: N–H···N → yes; HF: F–H···F → yes"],
    why="CH₄, H₂S, HCl and PH₃ have hydrogen bonded to C, S, Cl or P, which are not electronegative enough "
        "(as NCERT restricts hydrogen bonding to F, O and N), so each other pair has one compound that cannot "
        "form hydrogen bonds.",
    ncert=f"{REF3}, hydrogen bonding", seconds=30)

electrons = {"NO3-": 7 + 3 * 8 + 1, "CO3 2-": 6 + 3 * 8 + 2, "NH4+": 7 + 4 - 1, "H3O+": 8 + 3 - 1,
             "CO2": 6 + 16, "SO2": 16 + 16, "CH4": 10, "NH3": 10}
assert electrons["NO3-"] == electrons["CO3 2-"] == 32 and electrons["NH4+"] == electrons["H3O+"] == 10
assert electrons["CO2"] != electrons["SO2"]
add("VSEPR shapes", I, "direct",
    "Which of the following pairs of species are both isoelectronic (same total number of electrons) and "
    "isostructural (same shape)?",
    Opts("D", "NO₃⁻ and CO₃²⁻", ["NH₄⁺ and H₃O⁺", "CO₂ and SO₂", "CH₄ and NH₃"]),
    "Isoelectronic and isostructural species",
    "NO₃⁻ (7 + 24 + 1) and CO₃²⁻ (6 + 24 + 2) each have 32 electrons, and in both the central atom has three "
    "σ bond pairs and no lone pair, so both are trigonal planar.",
    ["NO₃⁻ = 32 e, CO₃²⁻ = 32 e → isoelectronic", "Both AB₃ with no lone pair → trigonal planar"],
    why="NH₄⁺ and H₃O⁺, and CH₄ and NH₃, are isoelectronic (10 e) but one of each pair is tetrahedral and the "
        "other pyramidal. CO₂ (22 e, linear) and SO₂ (32 e, bent) are neither.",
    ncert=f"{REF3}, VSEPR theory; resonance in CO₃²⁻", seconds=45)

add("Fajans' rule and dipole moment", I, "statement_pair",
    sp("BeF₂ has zero dipole moment whereas H₂O has a dipole moment, which shows that BeF₂ is linear and H₂O "
       "is bent.",
       "Any molecule that contains polar bonds must have a non-zero dipole moment."),
    SP_, "Dipole moment and molecular shape",
    "The dipole moment of a molecule is the vector sum of its bond dipoles (and lone-pair contributions). In "
    "linear BeF₂ the two Be–F dipoles are equal and opposite and cancel; in bent H₂O the O–H dipoles add to "
    "give a resultant. So Statement I is true. Statement II is false: CO₂, BF₃ and CCl₄ have polar bonds but "
    "zero dipole moment because their bond dipoles cancel.",
    ["I: μ = 0 for linear BeF₂; μ ≠ 0 for bent H₂O → true",
     "II: symmetric molecules with polar bonds (CO₂, BF₃) have μ = 0 → false"],
    answer="C",
    why="Statement II ignores that dipole moment is a vector quantity, so bond dipoles can cancel.",
    ncert=f"{REF3}, polarity of bonds: dipole moment", seconds=40)

planar = {"BF3": True, "NH3": False, "XeF4": True, "H2O": True, "SF4": False, "ClF3": True, "PCl5": False,
          "CH4": False}
assert sum(planar.values()) == 4
add("VSEPR shapes", A, "numerical",
    "How many of the following molecules have all their atoms lying in one plane?\n"
    "BF₃, NH₃, XeF₄, H₂O, SF₄, ClF₃, PCl₅, CH₄",
    Opts("C", "4", ["3", "2", "5"]),
    "Planarity from VSEPR shapes",
    "Work out each shape: trigonal planar BF₃, square planar XeF₄, bent H₂O (any triatomic molecule lies in "
    "one plane) and T-shaped ClF₃ are planar. Pyramidal NH₃, see-saw SF₄, trigonal bipyramidal PCl₅ and "
    "tetrahedral CH₄ are not.",
    ["Planar: BF₃ (trigonal planar), XeF₄ (square planar), H₂O (bent), ClF₃ (T-shaped)",
     "Not planar: NH₃, SF₄, PCl₅, CH₄", "Count = 4"],
    why="3 usually leaves out bent H₂O; 2 also leaves out T-shaped ClF₃; 5 wrongly counts see-saw SF₄ as "
        "planar.",
    ncert=f"{REF3}, VSEPR theory: shapes of molecules", seconds=75, checked=True)

para = [s for s in ("O2", "O2-", "O2 2-", "N2+", "C2", "B2", "Li2", "H2+") if mo(SPECIES[s])[1] > 0]
assert para == ["O2", "O2-", "N2+", "B2", "H2+"]
add("Molecular orbital theory", A, "numerical",
    "According to molecular orbital theory, how many of the following species are paramagnetic?\n"
    "O₂, O₂⁻, O₂²⁻, N₂⁺, C₂, B₂, Li₂, H₂⁺",
    Opts("A", "5", ["4", "6", "3"]),
    "Magnetic behaviour from MO electronic configurations",
    "A species is paramagnetic if it has one or more unpaired electrons. Fill the molecular orbitals "
    "(π2p below σ2p_z up to N₂; σ2p_z below π2p for O₂ and its ions) and count unpaired electrons.",
    ["O₂: π*¹ π*¹ → 2 unpaired; O₂⁻: 1 unpaired; O₂²⁻: π* full → 0",
     "N₂⁺ (13 e): σ2p_z¹ → 1 unpaired; C₂: π⁴ → 0; B₂: π¹ π¹ → 2 unpaired",
     "Li₂: σ2s² → 0; H₂⁺: σ1s¹ → 1 unpaired", "Paramagnetic: O₂, O₂⁻, N₂⁺, B₂, H₂⁺ = 5"],
    why="4 usually misses H₂⁺ or N₂⁺; 6 wrongly counts C₂ as paramagnetic (it would be only if σ2p_z were "
        "filled before π2p); 3 counts only the species with two unpaired electrons or misses the one-electron ions.",
    ncert=f"{REF3}, molecular orbital theory; bonding in homonuclear diatomic molecules", seconds=100,
    checked=True)


def change(a, b):
    (bo1, u1), (bo2, u2) = mo(SPECIES[a]), mo(SPECIES[b])
    return bo2 > bo1 and u1 > 0 and u2 == 0


assert change("N2+", "N2") and not change("O2", "O2+") and not change("O2-", "O2") and not change("N2", "N2-")
add("Molecular orbital theory", A, "direct",
    "In which of the following changes does the bond order INCREASE and the species change from paramagnetic "
    "to diamagnetic?",
    Opts("B", "N₂⁺ → N₂", ["O₂ → O₂⁺", "O₂⁻ → O₂", "N₂ → N₂⁻"]),
    "Effect of adding or removing an electron on bond order and magnetism",
    "N₂⁺ (13 electrons) has one unpaired electron in σ2p_z and bond order 2.5. Adding that electron gives N₂ "
    "with all electrons paired and bond order 3.",
    ["N₂⁺: BO 2.5, 1 unpaired → N₂: BO 3, 0 unpaired ✓",
     "O₂ (BO 2, 2 unpaired) → O₂⁺ (BO 2.5, 1 unpaired): still paramagnetic",
     "O₂⁻ (BO 1.5, 1 unpaired) → O₂ (BO 2, 2 unpaired): still paramagnetic",
     "N₂ (BO 3) → N₂⁻ (BO 2.5): bond order falls and N₂⁻ is paramagnetic"],
    why="In O₂ → O₂⁺ and O₂⁻ → O₂ the bond order rises but the product is still paramagnetic. N₂ → N₂⁻ lowers "
        "the bond order and gives a paramagnetic ion.",
    ncert=f"{REF3}, molecular orbital theory: bond order and magnetic nature", seconds=75)

add("VSEPR shapes", A, "multi_statement",
    ms("Consider the molecules XeF₂, ClF₃, SF₄ and PCl₅. Which of the following statements are correct?",
       ["The central atom in each of them is sp³d hybridised.",
        "All four molecules have zero dipole moment.",
        "In each molecule, any lone pairs on the central atom occupy equatorial positions of the trigonal "
        "bipyramid.",
        "The numbers of lone pairs on the central atoms of XeF₂, ClF₃, SF₄ and PCl₅ are 3, 2, 1 and 0 "
        "respectively.",
        "SF₄ and ClF₃ have the same shape."]),
    multi("D", {"a": True, "b": False, "c": True, "d": True, "e": False},
          ["(a), (b) and (c) only", "(a) and (d) only", "(c), (d) and (e) only"]),
    "Molecules with five electron pairs around the central atom",
    "Each central atom has five electron pairs (steric number 5) and is sp³d hybridised. Lone pairs go to the "
    "equatorial positions, where they have fewer 90° repulsions: XeF₂ (3 lone pairs) is linear, ClF₃ (2) is "
    "T-shaped, SF₄ (1) is see-saw and PCl₅ (0) is trigonal bipyramidal. XeF₂ and PCl₅ are non-polar, but "
    "ClF₃ and SF₄ have dipole moments.",
    ["(a) steric number 5 → sp³d → true", "(b) ClF₃ and SF₄ are polar → false",
     "(c) lone pairs equatorial → true", "(d) (8 − 2)/2 = 3, (7 − 3)/2 = 2, (6 − 4)/2 = 1, 0 → true",
     "(e) SF₄ is see-saw, ClF₃ is T-shaped → false"],
    why="Options with (b) or (e) are wrong, and (a) and (d) only leaves out the true statement (c).",
    ncert=f"{REF3}, VSEPR theory and sp³d hybridisation", seconds=100)

add("Ionic bonding and lattice enthalpy", A, "assertion_reason",
    ar("The lattice enthalpy of MgO is much greater than that of NaF, although all four ions (Mg²⁺, O²⁻, Na⁺ "
       "and F⁻) are isoelectronic with neon.",
       "Lattice enthalpy increases as the charges on the ions increase; Mg²⁺ and O²⁻ carry twice the charges "
       "of Na⁺ and F⁻."),
    AR_, "Factors affecting lattice enthalpy",
    "The energy released when gaseous ions form a crystal depends on the attraction between the ions, which "
    "grows with the product of their charges and falls as the ions get larger. The ions in MgO and NaF are of "
    "similar size (all have the neon configuration), but the charge product is 4 for MgO and 1 for NaF, so MgO "
    "has a much larger lattice enthalpy. R explains A.",
    ["A: MgO (2+, 2−) vs NaF (1+, 1−), similar ionic sizes → MgO much larger → true",
     "R: lattice enthalpy rises with ionic charge → true and explains A"],
    answer="A",
    why="Since the sizes are similar, the difference in charge is the reason for the difference, so R is the "
        "correct explanation.",
    ncert=f"{REF3}, ionic or electrovalent bond: lattice enthalpy", seconds=50)

add("Fajans' rule and dipole moment", A, "direct",
    "Which of the following molecules has zero dipole moment even though its central atom carries lone pairs "
    "of electrons?",
    Opts("C", "XeF₄", ["NH₃", "SF₄", "ClF₃"]),
    "Dipole moment, shape and lone pairs",
    "XeF₄ has two lone pairs on xenon placed opposite each other (trans) in the octahedral arrangement, so "
    "the molecule is square planar: the four Xe–F bond dipoles cancel in pairs and the two lone pairs also "
    "cancel. Its dipole moment is zero.",
    ["XeF₄: AB₄E₂ → square planar, symmetric → μ = 0",
     "NH₃ (pyramidal), SF₄ (see-saw), ClF₃ (T-shaped) are unsymmetrical → μ ≠ 0"],
    why="NH₃, SF₄ and ClF₃ also carry lone pairs, but their shapes are unsymmetrical, so their bond dipoles "
        "do not cancel.",
    ncert=f"{REF3}, VSEPR theory; dipole moment", seconds=50)

# ==================================================================== 4. Chemical Thermodynamics
topic("Chemical Thermodynamics")
REF4 = f"{C11}, 'Thermodynamics'"

add("First law, work and enthalpy", B, "direct",
    "A process is called reversible when:",
    Opts("C", "it is carried out infinitesimally slowly, so that the system stays practically in equilibrium "
              "with the surroundings at every stage and its direction can be reversed by an infinitesimal "
              "change",
         ["it takes place rapidly in one step against a constant external pressure",
          "no heat is exchanged between the system and the surroundings",
          "the temperature of the system remains constant throughout"]),
    "Reversible and irreversible processes",
    "NCERT describes a reversible process as one carried out so slowly, through a series of infinitesimal "
    "steps, that the system is always almost in equilibrium with the surroundings; reversing an infinitesimal "
    "change of a variable reverses the process. Real processes, which go at a finite rate, are irreversible.",
    ["Reversible = infinitesimally slow, quasi-equilibrium at every stage",
     "One-step expansion against a constant pressure is irreversible"],
    why="No heat exchange defines an adiabatic process and constant temperature an isothermal one; either can "
        "be reversible or irreversible. A rapid one-step change is irreversible.",
    ncert=f"{REF4}, work: reversible and irreversible processes", seconds=30)

q_in, dU = 250, 100
w_on = dU - q_in
assert w_on == -150 and -w_on == 150
add("First law, work and enthalpy", B, "numerical",
    "A gas absorbs 250 J of heat, and its internal energy increases by 100 J. The work done BY the gas on the "
    "surroundings is:",
    Opts("A", "150 J", ["350 J", "−150 J", "−350 J"]),
    "First law of thermodynamics, ΔU = q + w",
    "In the IUPAC convention, q is positive for heat absorbed and w is the work done on the system. The work "
    "done by the system is −w.",
    ["ΔU = q + w → 100 = 250 + w → w = −150 J (work done on the gas)",
     "Work done by the gas = −w = +150 J"],
    why="350 J adds q and ΔU. −150 J is the work done on the gas, not by it. −350 J combines both slips.",
    ncert=f"{REF4}, first law of thermodynamics", seconds=30, checked=True)

add("Hess's law and enthalpies", B, "direct",
    "Which of the following equations represents the standard enthalpy of formation of methanol, CH₃OH(l)?",
    Opts("B", "C(graphite) + 2H₂(g) + ½O₂(g) → CH₃OH(l)",
         ["C(diamond) + 2H₂(g) + ½O₂(g) → CH₃OH(l)", "CO(g) + 2H₂(g) → CH₃OH(l)",
          "2C(graphite) + 4H₂(g) + O₂(g) → 2CH₃OH(l)"]),
    "Standard enthalpy of formation",
    "ΔfH° refers to the formation of ONE mole of a compound from its elements in their most stable states "
    "(reference states) at 1 bar: carbon as graphite, hydrogen and oxygen as H₂(g) and O₂(g).",
    ["One mole of CH₃OH(l)", "Elements in reference states: C(graphite), H₂(g), O₂(g)"],
    why="Diamond is not the reference state of carbon. CO is a compound, not an element. The last equation "
        "forms two moles, so its ΔH is 2ΔfH°.",
    ncert=f"{REF4}, standard enthalpy of formation", seconds=30)

add("Entropy and Gibbs energy", B, "statement_pair",
    sp("Gibbs energy is an intensive property.",
       "A negative value of ΔG for a reaction tells us that the reaction is feasible, but not how fast it will "
       "take place."),
    SP_, "Gibbs energy; feasibility versus rate",
    "G = H − TS is an extensive property and a state function, so Statement I is false. ΔG < 0 at constant "
    "temperature and pressure means the process is spontaneous (thermodynamically feasible), but "
    "thermodynamics says nothing about the rate; that is the subject of chemical kinetics. Statement II is "
    "true.",
    ["I: G depends on the amount of substance → extensive → false",
     "II: thermodynamics gives feasibility, kinetics gives rate → true"],
    answer="D",
    why="Statement I is false because G, like H and S, is extensive; Statement II is a point NCERT makes at the "
        "start of chemical kinetics.",
    ncert=f"{REF4}, Gibbs energy and spontaneity; {C12}, 'Chemical Kinetics', introduction", seconds=30)

q_abs = 100 * 4.18 * 2.0
dH_sol = q_abs / 0.10 / 1000
assert close(q_abs, 836) and close(dH_sol, 8.36)
add("First law, work and enthalpy", I, "numerical",
    "When 0.10 mol of a salt dissolves in water in an insulated constant-pressure (coffee-cup) calorimeter, "
    "100 g of solution is formed and its temperature falls by 2.0 K. Taking the specific heat of the solution "
    "as 4.18 J g⁻¹ K⁻¹ and neglecting the heat capacity of the calorimeter, the enthalpy of solution of the "
    "salt is:",
    Opts("C", "+8.36 kJ mol⁻¹", ["−8.36 kJ mol⁻¹", "+0.836 kJ mol⁻¹", "+83.6 kJ mol⁻¹"]),
    "Measuring ΔH at constant pressure: q_p = ΔH",
    "The temperature falls, so the dissolution absorbs heat from the solution: the process is endothermic. "
    "The heat absorbed is mcΔT, and dividing by the moles dissolved gives the molar enthalpy of solution.",
    ["q = m c ΔT = 100 × 4.18 × 2.0 = 836 J absorbed by the dissolving salt",
     "ΔsolH = +836 J / 0.10 mol = +8360 J mol⁻¹ = +8.36 kJ mol⁻¹"],
    why="−8.36 kJ mol⁻¹ has the wrong sign: a fall in temperature means an endothermic process. +0.836 is the "
        "total heat in kJ without dividing by the moles. +83.6 divides by 0.010 mol.",
    ncert=f"{REF4}, measurement of ΔU and ΔH: calorimetry", seconds=60, checked=True)

dng = 0 - 3
w_rxn = -dng * R_J * 300 / 1000
assert close(w_rxn, 7.48) and close(2 * R_J * 300 / 1000, 4.99) and close(R_J * 300 / 1000, 2.49)
add("First law, work and enthalpy", I, "numerical",
    "The reaction 2H₂(g) + O₂(g) → 2H₂O(l) is carried out at a constant pressure and 300 K. Treating the "
    "gases as ideal and neglecting the volume of the liquid, the work done ON the system when 2 mol of H₂ "
    "reacts completely is (R = 8.314 J K⁻¹ mol⁻¹):",
    Opts("D", "+7.48 kJ", ["−7.48 kJ", "+4.99 kJ", "+2.49 kJ"]),
    "Pressure–volume work in a reaction involving gases",
    "At constant pressure, w = −pΔV = −Δn(g)RT. Three moles of gas disappear, so the surroundings compress the "
    "system and the work done on it is positive.",
    ["Δn(g) = 0 − (2 + 1) = −3", "w = −Δn(g)RT = −(−3)(8.314)(300) = +7483 J ≈ +7.48 kJ"],
    why="−7.48 kJ is the sign of work done BY the system. +4.99 kJ uses Δn = −2, counting only H₂. +2.49 kJ "
        "uses Δn = −1.",
    ncert=f"{REF4}, work, enthalpy and the relation ΔH = ΔU + Δn(g)RT", seconds=60, checked=True)

add("First law, work and enthalpy", I, "assertion_reason",
    ar("For an ideal gas, the molar heat capacity at constant pressure, C_p, is greater than the molar heat "
       "capacity at constant volume, C_v.",
       "At constant pressure part of the heat supplied is used by the gas to do work of expansion against the "
       "surroundings, so more heat is needed for the same rise in temperature."),
    AR_, "Relation between C_p and C_v",
    "At constant volume all the heat raises the internal energy (q_v = ΔU = C_vΔT). At constant pressure the "
    "gas also expands and does work pΔV = RΔT per mole, so q_p = C_vΔT + RΔT and C_p − C_v = R. R explains A.",
    ["A: C_p > C_v; for an ideal gas C_p − C_v = R → true",
     "R: extra heat at constant pressure goes into expansion work → true and explains A"],
    answer="A",
    why="R is the physical origin of the relation C_p − C_v = R.",
    ncert=f"{REF4}, heat capacity: relation between C_p and C_v for an ideal gas", seconds=40)

add("Hess's law and enthalpies", I, "statement_pair",
    sp("The enthalpy change for C(graphite) + O₂(g) → CO₂(g) equals the sum of the enthalpy changes for "
       "C(graphite) + ½O₂(g) → CO(g) and CO(g) + ½O₂(g) → CO₂(g).",
       "The standard enthalpy of combustion of graphite is numerically equal to the standard enthalpy of "
       "formation of CO₂(g)."),
    SP_, "Hess's law of constant heat summation",
    "Because enthalpy is a state function, the enthalpy change from graphite and O₂ to CO₂ is the same whether "
    "the change happens in one step or through CO; Statement I is true. Burning one mole of graphite, the "
    "reference state of carbon, in O₂ forms one mole of CO₂ from its elements, so ΔcH°(graphite) = "
    "ΔfH°(CO₂, g); Statement II is true.",
    ["I: one-step ΔH = sum of the two-step ΔH values (Hess's law) → true",
     "II: C(graphite) + O₂ → CO₂ is both combustion of graphite and formation of CO₂ → true"],
    answer="A",
    why="Both statements are true.",
    ncert=f"{REF4}, Hess's law of constant heat summation; enthalpy of combustion", seconds=40)

RT303 = 5.74
K_of = {dg: 10 ** (-dg / RT303) for dg in (-11.48, 0.0, 5.74, -5.74)}
assert close(K_of[-11.48], 100) and K_of[0.0] == 1 and close(K_of[5.74], 0.1) and close(K_of[-5.74], 10)
add("Gibbs energy and K", I, "match_list",
    lists("For four reactions at 300 K (take 2.303RT = 5.74 kJ mol⁻¹), match List-I (standard Gibbs energy "
          "change, ΔrG°) with List-II (equilibrium constant, K).",
          ["−11.48 kJ mol⁻¹", "0", "+5.74 kJ mol⁻¹", "−5.74 kJ mol⁻¹"],
          ["1", "10", "0.1", "100"]),
    match("C", M("IV I III II"), [M("III I IV II"), M("IV I II III"), M("II I III IV")]),
    "Relation between ΔrG° and K",
    "ΔrG° = −2.303RT log K, so log K = −ΔrG°/(2.303RT). A negative ΔrG° gives K > 1, zero gives K = 1 and a "
    "positive value gives K < 1.",
    ["A: log K = 11.48/5.74 = 2 → K = 100 (IV)", "B: log K = 0 → K = 1 (I)",
     "C: log K = −1 → K = 0.1 (III)", "D: log K = 1 → K = 10 (II)"],
    why="The other codes reverse the sign relation (a positive ΔrG° giving K > 1) or mix up 10 and 100.",
    ncert=f"{REF4}, Gibbs energy change and equilibrium", seconds=50)

dG = -35.0 - 300 * (-40) / 1000
logK = -dG / 5.75
assert close(dG, -23.0) and close(logK, 4.0) and close((35.0 + 12.0) / 5.75, 8.17)
add("Gibbs energy and K", A, "numerical",
    "For a reaction, ΔH° = −35.0 kJ mol⁻¹ and ΔS° = −40 J K⁻¹ mol⁻¹, both independent of temperature. Its "
    "equilibrium constant at 300 K is (take 2.303RT = 5.75 kJ mol⁻¹ at 300 K):",
    Opts("B", "1 × 10⁴", ["1 × 10⁻⁴", "1.5 × 10⁸", "4"]),
    "ΔG° from ΔH° and ΔS°, then K from ΔG°",
    "First find ΔG° = ΔH° − TΔS° (with ΔS° in kJ), then use ΔG° = −2.303RT log K.",
    ["TΔS° = 300 × (−0.040) = −12.0 kJ mol⁻¹", "ΔG° = −35.0 − (−12.0) = −23.0 kJ mol⁻¹",
     "log K = 23.0/5.75 = 4.0 → K = 1 × 10⁴"],
    why="1 × 10⁻⁴ drops the minus sign in ΔG° = −2.303RT log K. 1.5 × 10⁸ adds TΔS° instead of subtracting "
        "it (ΔG° = −47 kJ). 4 is log K, not K.",
    ncert=f"{REF4}, Gibbs energy change and equilibrium", seconds=90, checked=True)

dfH_ch4 = 717 + 2 * 436 - 4 * 416
assert dfH_ch4 == -75 and 2 * 436 - 4 * 416 == -792 and 717 + 436 - 4 * 416 == -511
add("Hess's law and enthalpies", A, "numerical",
    "Using the following data (kJ mol⁻¹), the standard enthalpy of formation of methane, "
    "C(graphite) + 2H₂(g) → CH₄(g), is:\n"
    "Enthalpy of atomisation of graphite, C(graphite) → C(g): 717\n"
    "Bond dissociation enthalpy of H–H: 436\n"
    "Mean C–H bond enthalpy in methane: 416",
    Opts("D", "−75 kJ mol⁻¹", ["−792 kJ mol⁻¹", "−511 kJ mol⁻¹", "+75 kJ mol⁻¹"]),
    "Enthalpy of formation from atomisation and bond enthalpies (Hess's law)",
    "Go from the elements to gaseous atoms (atomise graphite, break two H–H bonds), then form four C–H bonds. "
    "Energy absorbed in the first step is positive; energy released in forming bonds is negative.",
    ["Atomisation: 717 + 2 × 436 = 1589 kJ", "Bond formation: −4 × 416 = −1664 kJ",
     "ΔfH°(CH₄) = 1589 − 1664 = −75 kJ mol⁻¹"],
    why="−792 kJ mol⁻¹ leaves out the atomisation of graphite. −511 kJ mol⁻¹ breaks only one H–H bond. "
        "+75 kJ mol⁻¹ has the sign reversed.",
    ncert=f"{REF4}, enthalpy of atomisation; bond enthalpy; Hess's law", seconds=90, checked=True)

dU_w = -571.6 + 3 * R_J * 298 / 1000
assert close(dU_w, -564.2, 0.0005) and -571.6 / 2 == -285.8
add("First law, work and enthalpy", A, "multi_statement",
    ms("For the reaction 2H₂(g) + O₂(g) → 2H₂O(l), ΔH° = −571.6 kJ at 298 K. Treating the gases as ideal, "
       "which of the following statements are correct? (R = 8.314 J K⁻¹ mol⁻¹)",
       ["The standard enthalpy of formation of H₂O(l) is −285.8 kJ mol⁻¹.",
        "ΔU° for the reaction as written is about −564.2 kJ.",
        "ΔU° for the reaction is more negative than ΔH°.",
        "The entropy of the system decreases in this reaction.",
        "ΔH° for 2H₂O(l) → 2H₂(g) + O₂(g) is −571.6 kJ."]),
    multi("B", {"a": True, "b": True, "c": False, "d": True, "e": False},
          ["(a), (b) and (c) only", "(b), (d) and (e) only", "(a) and (d) only"]),
    "ΔH, ΔU and entropy for a reaction involving gases",
    "ΔfH° refers to one mole: −571.6/2 = −285.8 kJ mol⁻¹. ΔH = ΔU + Δn(g)RT with Δn(g) = −3, so "
    "ΔU = ΔH + 3RT = −571.6 + 7.4 = −564.2 kJ, which is less negative than ΔH. Three moles of gas become "
    "liquid, so the entropy of the system falls. The reverse reaction has ΔH° = +571.6 kJ.",
    ["(a) −571.6/2 = −285.8 → true", "(b) ΔU = −571.6 + 3 × 8.314 × 298/1000 = −564.2 kJ → true",
     "(c) −564.2 is less negative than −571.6 → false", "(d) gas → liquid → ΔS < 0 → true",
     "(e) reversing a reaction reverses the sign of ΔH → false"],
    why="Options with (c) or (e) are wrong, and (a) and (d) only leaves out the true statement (b).",
    ncert=f"{REF4}, enthalpy, ΔH = ΔU + Δn(g)RT, and standard enthalpy of formation", seconds=110,
    checked=True)

dG400 = 40 - 400 * 80 / 1000
dG500 = 40 - 500 * 80 / 1000
assert dG400 == 8 and dG500 == 0
add("Gibbs energy and K", A, "statement_pair",
    sp("For a reaction with ΔH° = +40 kJ mol⁻¹ and ΔS° = +80 J K⁻¹ mol⁻¹ (both independent of temperature), "
       "the equilibrium constant at 400 K is less than 1.",
       "For the same reaction, the equilibrium constant at 500 K is equal to 1."),
    SP_, "Temperature, ΔG° and the equilibrium constant",
    "ΔG° = ΔH° − TΔS°. At 400 K, ΔG° = 40 − 32 = +8 kJ mol⁻¹ > 0, so K < 1. At 500 K, ΔG° = 40 − 40 = 0, so "
    "log K = 0 and K = 1. Both statements are true; above 500 K K exceeds 1.",
    ["400 K: ΔG° = 40 − 400 × 0.080 = +8 kJ mol⁻¹ → K < 1 (I true)",
     "500 K: ΔG° = 40 − 500 × 0.080 = 0 → K = 1 (II true)"],
    answer="A",
    why="Both statements follow directly from ΔG° = ΔH° − TΔS° and ΔG° = −2.303RT log K.",
    ncert=f"{REF4}, Gibbs energy and spontaneity; Gibbs energy change and equilibrium", seconds=75,
    checked=True)

# ==================================================================== 5. Solutions
topic("Solutions")
REF5 = f"{C12}, 'Solutions'"

add("Concentration terms", B, "statement_pair",
    sp("A 10% (volume/volume) solution of ethanol in water contains 10 mL of ethanol dissolved in 100 mL of "
       "water.",
       "A solution of 35% (v/v) ethylene glycol in water is used as an antifreeze in the cooling systems of "
       "cars, because it lowers the freezing point of water."),
    SP_, "Volume percentage; an application of freezing-point depression",
    "Volume percentage = volume of component/total volume of SOLUTION × 100. A 10% (v/v) ethanol solution has "
    "10 mL of ethanol in 100 mL of solution, not in 100 mL of water, so Statement I is false. NCERT notes "
    "that 35% (v/v) ethylene glycol is used as an antifreeze in cars; it lowers the freezing point of water to "
    "about 255.4 K. Statement II is true.",
    ["I: 10 mL ethanol per 100 mL of solution → false as written",
     "II: ethylene glycol antifreeze lowers the freezing point → true"],
    answer="D",
    why="Statement I uses 100 mL of solvent instead of 100 mL of solution.",
    ncert=f"{REF5}, expressing concentration of solutions: volume percentage", seconds=35)

pi_suc = 0.05 * 0.0821 * 300
assert close(pi_suc, 1.23) and close(2 * pi_suc, 2.46) and close(0.05 * 0.0821 * 27, 0.111, 0.01) \
    and close(10 * pi_suc, 12.3)
add("Colligative properties", B, "numerical",
    "The osmotic pressure of a 0.05 M aqueous solution of sucrose (a non-electrolyte) at 27 °C is "
    "(R = 0.0821 L atm K⁻¹ mol⁻¹):",
    Opts("B", "1.23 atm", ["2.46 atm", "0.111 atm", "12.3 atm"]),
    "Osmotic pressure, π = CRT",
    "For a dilute solution of a non-electrolyte, π = CRT with C in mol L⁻¹ and T in kelvin.",
    ["T = 27 + 273 = 300 K", "π = 0.05 × 0.0821 × 300 = 1.23 atm"],
    why="2.46 atm uses i = 2, but sucrose does not dissociate. 0.111 atm uses 27 instead of 300 K. 12.3 atm "
        "takes the concentration as 0.5 M.",
    ncert=f"{REF5}, osmosis and osmotic pressure", seconds=30, checked=True)

add("van't Hoff factor", B, "direct",
    "Assuming complete dissociation, the van't Hoff factor of potassium hexacyanidoferrate(II), K₄[Fe(CN)₆], "
    "in dilute aqueous solution is:",
    Opts("C", "5", ["4", "11", "2"]),
    "van't Hoff factor of an ionic solute",
    "The complex ion stays intact in solution: K₄[Fe(CN)₆] → 4K⁺ + [Fe(CN)₆]⁴⁻, giving five ions per formula "
    "unit, so i = 5.",
    ["K₄[Fe(CN)₆] → 4K⁺ + [Fe(CN)₆]⁴⁻", "Particles per formula unit = 4 + 1 = 5 → i = 5"],
    why="4 counts only the K⁺ ions. 11 breaks the complex ion into Fe²⁺ and six CN⁻, which does not happen. "
        "2 treats it like a 1 : 1 salt.",
    ncert=f"{REF5}, abnormal molar masses: van't Hoff factor", seconds=30)

add("Raoult's law and ideal solutions", B, "direct",
    "For an ideal solution of two volatile liquids A and B at a fixed temperature, the plot of the total "
    "vapour pressure against the mole fraction of A is:",
    Opts("D", "a straight line joining p°B (at x_A = 0) and p°A (at x_A = 1)",
         ["a curve showing a maximum", "a curve showing a minimum",
          "a straight line parallel to the composition axis"]),
    "Raoult's law for a solution of two volatile liquids",
    "p_total = p°B + (p°A − p°B) x_A, which is linear in x_A. At x_A = 0 it equals p°B and at x_A = 1 it equals "
    "p°A.",
    ["p_total = x_A p°A + (1 − x_A) p°B = p°B + (p°A − p°B) x_A → linear"],
    why="A maximum or a minimum appears only for non-ideal solutions with positive or negative deviations. A "
        "horizontal line would need p°A = p°B.",
    ncert=f"{REF5}, vapour pressure of liquid–liquid solutions: Raoult's law", seconds=25)

pA, pB = 600, 200
xA = 0.25
assert pA * xA / (pA * xA + pB * (1 - xA)) == 0.5
assert pB * 0.75 / (pB * 0.75 + pA * 0.25) == 0.5  # 0.75 comes from swapping the two pure vapour pressures
add("Raoult's law and ideal solutions", I, "numerical",
    "Liquids A and B form an ideal solution. At a certain temperature p°A = 600 mm Hg and p°B = 200 mm Hg. "
    "For the vapour in equilibrium with the solution to contain equal mole fractions of A and B, the mole "
    "fraction of A in the liquid must be:",
    Opts("A", "0.25", ["0.50", "0.75", "0.33"]),
    "Composition of the vapour over an ideal solution (Raoult's and Dalton's laws)",
    "The mole fraction of A in the vapour is y_A = p_A/p_total = x_A p°A/(x_A p°A + x_B p°B). Equal mole "
    "fractions in the vapour means the partial pressures are equal: x_A p°A = x_B p°B.",
    ["600 x_A = 200 (1 − x_A)", "800 x_A = 200 → x_A = 0.25", "Check: p_A = p_B = 150 mm Hg → y_A = 0.5"],
    why="0.50 assumes the liquid has the same composition as the vapour. 0.75 interchanges p°A and p°B. "
        "0.33 is just the ratio p°B/p°A.",
    ncert=f"{REF5}, vapour pressure of liquid–liquid solutions", seconds=75, checked=True)

c_mix = (0.1 * 100 + 0.2 * 100) / 200
pi_mix = c_mix * 0.082 * 300
assert close(c_mix, 0.15) and close(pi_mix, 3.69) and close(0.3 * 0.082 * 300, 7.38) \
    and close(0.1 * 0.082 * 300, 2.46) and close(0.2 * 0.082 * 300, 4.92)
add("Colligative properties", I, "numerical",
    "100 mL of a 0.1 M aqueous solution of urea is mixed with 100 mL of a 0.2 M aqueous solution of glucose. "
    "Assuming the volumes are additive, the osmotic pressure of the mixture at 300 K is "
    "(R = 0.082 L atm K⁻¹ mol⁻¹):",
    Opts("C", "3.69 atm", ["7.38 atm", "2.46 atm", "4.92 atm"]),
    "Osmotic pressure of a mixture of non-electrolytes",
    "Osmotic pressure depends on the total molar concentration of solute particles. Both solutes are "
    "non-electrolytes, so add their moles and divide by the total volume.",
    ["Moles: urea 0.010 + glucose 0.020 = 0.030 mol in 0.200 L → C = 0.15 M",
     "π = 0.15 × 0.082 × 300 = 3.69 atm"],
    why="7.38 atm adds the two molarities without allowing for dilution. 2.46 atm and 4.92 atm use only one "
        "solute's original concentration.",
    ncert=f"{REF5}, osmosis and osmotic pressure", seconds=60, checked=True)

add("Concentration terms", I, "assertion_reason",
    ar("The molarity of an aqueous solution decreases slightly when the solution is warmed.",
       "The volume of the solution increases with temperature, while the amount of solute in it stays the "
       "same."),
    AR_, "Temperature dependence of molarity",
    "Molarity is moles of solute per litre of solution. Warming expands the solution, so the same number of "
    "moles is spread over a larger volume and the molarity falls. Molality, mass percentage and mole fraction "
    "do not change, as they involve only masses. R explains A.",
    ["A: M = n/V and V rises with T → M falls → true",
     "R: V increases, n unchanged → true and explains A"],
    answer="A",
    why="R gives exactly the reason why molarity depends on temperature.",
    ncert=f"{REF5}, expressing concentration of solutions", seconds=35)

i_vals = {"Al2(SO4)3": 2 + 3, "MgSO4": 1 + 1, "urea": 1, "CaCl2": 1 + 2}
assert i_vals["Al2(SO4)3"] == 5 and i_vals["MgSO4"] == 2 and i_vals["urea"] == 1
assert close(i_vals["CaCl2"] * 1.86 * 0.1, 0.558) and not close(i_vals["CaCl2"] * 1.86 * 0.1, 0.372)
add("van't Hoff factor", I, "multi_statement",
    ms("For 0.1 m aqueous solutions of the following solutes, assuming complete dissociation of the "
       "electrolytes (K_f of water = 1.86 K kg mol⁻¹), which statements are correct?",
       ["The van't Hoff factor of Al₂(SO₄)₃ is 5.", "The van't Hoff factor of MgSO₄ is 2.",
        "The van't Hoff factor of urea is 1.",
        "The depression of freezing point of the CaCl₂ solution is 0.372 K.",
        "Of the solutions of Al₂(SO₄)₃, MgSO₄, urea and CaCl₂, the MgSO₄ solution has the lowest freezing "
        "point."]),
    multi("B", {"a": True, "b": True, "c": True, "d": False, "e": False},
          ["(a), (b) and (d) only", "(b), (c) and (e) only", "(a), (c) and (d) only"]),
    "van't Hoff factor and depression of freezing point",
    "Al₂(SO₄)₃ → 2Al³⁺ + 3SO₄²⁻ (i = 5); MgSO₄ → Mg²⁺ + SO₄²⁻ (i = 2); urea does not ionise (i = 1); "
    "CaCl₂ → Ca²⁺ + 2Cl⁻ (i = 3). ΔT_f = i K_f m, so CaCl₂ gives 3 × 1.86 × 0.1 = 0.558 K, and the solution "
    "with the largest i, Al₂(SO₄)₃, freezes lowest.",
    ["(a), (b), (c) true", "(d) 3 × 1.86 × 0.1 = 0.558 K, not 0.372 K → false",
     "(e) largest i is Al₂(SO₄)₃ (5) → it has the lowest freezing point → false"],
    why="0.372 K uses i = 2 for CaCl₂, and (e) ignores that Al₂(SO₄)₃ gives the most particles.",
    ncert=f"{REF5}, abnormal molar masses: van't Hoff factor", seconds=75)

i_obs = 122 / 203.3
alpha_assoc = 2 * (1 - i_obs)
assert close(i_obs, 0.6, 0.001) and close(alpha_assoc, 0.8, 0.005)
add("van't Hoff factor", I, "numerical",
    "Benzoic acid (C₆H₅COOH, molar mass 122 g mol⁻¹) partly dimerises in benzene: 2C₆H₅COOH ⇌ "
    "(C₆H₅COOH)₂. Its molar mass found from the depression of the freezing point of a dilute benzene "
    "solution is 203.3 g mol⁻¹. The percentage of benzoic acid molecules that are dimerised is:",
    Opts("D", "80%", ["40%", "60%", "20%"]),
    "Degree of association from the van't Hoff factor",
    "i = normal molar mass / observed molar mass. For dimerisation, if a fraction α of the molecules "
    "associates, the particles per original molecule are (1 − α) + α/2 = 1 − α/2.",
    ["i = 122/203.3 = 0.60", "1 − α/2 = 0.60 → α/2 = 0.40 → α = 0.80, i.e. 80%"],
    why="40% takes α = 1 − i, forgetting that two molecules make one dimer. 60% is i itself. 20% is 1 − α.",
    ncert=f"{REF5}, abnormal molar masses: association of ethanoic acid and benzoic acid in benzene",
    seconds=75, checked=True)

m_glu = (10 / 180) / 0.090
dTf = 1.86 * m_glu
assert close(dTf, 1.15, 0.005) and close(1.86 * (10 / 180) / 0.100, 1.03, 0.005)
add("Colligative properties", A, "numerical",
    "An aqueous solution of glucose (molar mass 180 g mol⁻¹) is 10% by mass. Its freezing point is "
    "(K_f of water = 1.86 K kg mol⁻¹; freezing point of water = 0 °C):",
    Opts("A", "−1.15 °C", ["−1.03 °C", "−0.10 °C", "+1.15 °C"]),
    "Freezing-point depression from a mass percentage",
    "Take 100 g of solution: 10 g of glucose in 90 g of water. Convert to molality and use ΔT_f = K_f m.",
    ["n(glucose) = 10/180 = 0.0556 mol; water = 90 g = 0.090 kg",
     "m = 0.0556/0.090 = 0.617 mol kg⁻¹", "ΔT_f = 1.86 × 0.617 = 1.15 K → freezing point = −1.15 °C"],
    why="−1.03 °C uses 100 g (the solution) instead of 90 g of water. −0.10 °C takes 10 g of glucose in 1 kg "
        "of water. +1.15 °C forgets that the freezing point is lowered.",
    ncert=f"{REF5}, depression of freezing point", seconds=90, checked=True)

pA2, pB2 = 400, 100
y_A = 0.5 * pA2 / (0.5 * pA2 + 0.5 * pB2)
p_cond = y_A * pA2 + (1 - y_A) * pB2
assert close(y_A, 0.8) and close(p_cond, 340) and 0.5 * pA2 + 0.5 * pB2 == 250
add("Raoult's law and ideal solutions", A, "numerical",
    "Liquids A and B form an ideal solution; at temperature T, p°A = 400 mm Hg and p°B = 100 mm Hg. The vapour "
    "in equilibrium with a solution containing equal numbers of moles of A and B is removed and condensed "
    "completely. The vapour pressure of this condensate at the same temperature T is:",
    Opts("C", "340 mm Hg", ["250 mm Hg", "320 mm Hg", "400 mm Hg"]),
    "Vapour composition over an ideal solution and repeated vaporisation",
    "First find the composition of the vapour, which is richer in the more volatile A. The condensate is a "
    "liquid of that composition, and Raoult's law then gives its vapour pressure.",
    ["Original liquid: p_A = 0.5 × 400 = 200, p_B = 0.5 × 100 = 50, total 250 mm Hg",
     "Vapour: y_A = 200/250 = 0.8, y_B = 0.2",
     "Condensate (x_A = 0.8): p = 0.8 × 400 + 0.2 × 100 = 320 + 20 = 340 mm Hg"],
    why="250 mm Hg is the vapour pressure of the original solution. 320 mm Hg leaves out B's contribution. "
        "400 mm Hg is the vapour pressure of pure A.",
    ncert=f"{REF5}, vapour pressure of liquid–liquid solutions", seconds=100, checked=True)

i_ha = 1 + 0.10
assert close(i_ha * 1.86 * 0.1, 0.205, 0.005) and close(i_ha * 0.52 * 0.1, 0.0572) and i_ha < 2
add("van't Hoff factor", A, "multi_statement",
    ms("A 0.1 m aqueous solution of a weak monobasic acid HA is 10% ionised (HA ⇌ H⁺ + A⁻). Which of the "
       "following statements are correct? (For water, K_f = 1.86 K kg mol⁻¹ and K_b = 0.52 K kg mol⁻¹.)",
       ["The van't Hoff factor of HA in this solution is 1.1.",
        "The depression of freezing point is about 0.205 K.",
        "The elevation of boiling point is 0.052 K.",
        "The solution contains fewer solute particles per kilogram of water than a 0.1 m solution of NaCl "
        "(completely dissociated).",
        "The van't Hoff factor of HA is greater than 2."]),
    multi("B", {"a": True, "b": True, "c": False, "d": True, "e": False},
          ["(a), (b) and (c) only", "(b), (d) and (e) only", "(a) and (d) only"]),
    "van't Hoff factor of a partly ionised solute",
    "For HA ⇌ H⁺ + A⁻ with degree of ionisation α, particles per formula unit = (1 − α) + 2α = 1 + α = 1.1. "
    "Colligative properties are multiplied by i: ΔT_f = 1.1 × 1.86 × 0.1 = 0.205 K and ΔT_b = 1.1 × 0.52 × "
    "0.1 = 0.0572 K. NaCl gives i = 2, more particles than HA (i = 1.1).",
    ["(a) i = 1 + α = 1.1 → true", "(b) 0.2046 K → true", "(c) 0.0572 K, not 0.052 K (that ignores i) → false",
     "(d) 1.1 < 2 → true", "(e) i = 1.1 < 2 → false"],
    why="0.052 K forgets the van't Hoff factor; (e) is false since a 1 : 1 weak acid cannot exceed i = 2.",
    ncert=f"{REF5}, abnormal molar masses: van't Hoff factor", seconds=100, checked=True)

add("Raoult's law and ideal solutions", A, "assertion_reason",
    ar("The total vapour pressure of a mixture of acetone and chloroform is lower than the value predicted by "
       "Raoult's law.",
       "Chloroform molecules form hydrogen bonds with acetone molecules, so the attractions between unlike "
       "molecules are stronger than those between like molecules, which reduces the escaping tendency of both "
       "components."),
    AR_, "Negative deviation from Raoult's law",
    "On mixing, a chloroform molecule hydrogen-bonds to the oxygen of an acetone molecule. These A–B "
    "interactions are stronger than the A–A and B–B interactions they replace, so fewer molecules escape "
    "into the vapour and the vapour pressure is below the ideal value (negative deviation). R explains A.",
    ["A: acetone–chloroform shows negative deviation → true",
     "R: stronger A–B attraction via hydrogen bonding lowers vapour pressure → true and explains A"],
    answer="A",
    why="R is the molecular reason NCERT gives for the negative deviation of this mixture.",
    ncert=f"{REF5}, non-ideal solutions", seconds=45)

# ==================================================================== 6. Equilibrium
topic("Equilibrium")
REF6 = f"{C11}, 'Equilibrium'"

add("Physical equilibria and Henry's law", B, "direct",
    "A little sugar containing radioactive carbon is added to a saturated solution of ordinary sugar that is in "
    "contact with undissolved sugar at constant temperature. After some time, radioactivity is found both in "
    "the solution and in the undissolved solid sugar. This shows that:",
    Opts("B", "dissolution and crystallisation continue at equal rates, i.e. the equilibrium is dynamic",
         ["the solubility of sugar increases with time", "radioactive sugar is more soluble than ordinary sugar",
          "the solution is no longer saturated"]),
    "Dynamic nature of physical equilibrium",
    "At equilibrium the concentration of the saturated solution stays constant, but molecules keep leaving the "
    "solid and returning to it at the same rate. That is how radioactive sugar molecules end up in the solid as "
    "well as in the solution.",
    ["Rate of dissolution = rate of crystallisation", "Exchange of molecules → radioactivity in both phases"],
    why="The concentration of a saturated solution is constant at a fixed temperature, so the solubility does "
        "not change and the solution stays saturated. Labelled and ordinary sugar have the same solubility.",
    ncert=f"{REF6}, solid–liquid equilibrium: dynamic nature of equilibrium", seconds=30)

add("Physical equilibria and Henry's law", B, "assertion_reason",
    ar("Aquatic species are more comfortable in cold water than in warm water.",
       "The Henry's law constant (K_H) of oxygen in water increases with rise in temperature, so less oxygen "
       "dissolves in warm water."),
    AR_, "Henry's law and the effect of temperature on gas solubility",
    "By Henry's law, p = K_H x. A larger K_H at a higher temperature means a smaller mole fraction x of the "
    "gas in solution at the same partial pressure. Warm water therefore holds less dissolved oxygen, which is "
    "why aquatic animals are more comfortable in cold water. R explains A.",
    ["A: more dissolved O₂ in cold water → true",
     "R: K_H rises with T → solubility of O₂ falls → true and explains A"],
    answer="A",
    why="NCERT links these two facts directly in its discussion of Henry's law.",
    ncert=f"{C12}, 'Solutions', solubility of a gas in a liquid: Henry's law", seconds=35)

add("Acids, bases and pH", B, "statement_pair",
    sp("For a polyprotic acid such as H₂CO₃, the first ionisation constant is larger than the second "
       "(K_a1 > K_a2).",
       "It is more difficult to remove a proton from a negatively charged ion such as HCO₃⁻ than from a "
       "neutral H₂CO₃ molecule."),
    SP_, "Ionisation of polybasic acids",
    "NCERT notes that the higher-order ionisation constants of a polyprotic acid are smaller than the "
    "lower-order ones, because the positively charged proton is harder to remove from an anion that already "
    "carries negative charge than from a neutral molecule. Both statements are true.",
    ["I: K_a1 > K_a2 > K_a3 for polyprotic acids → true",
     "II: electrostatic attraction of the anion holds the proton more strongly → true"],
    answer="A",
    why="Both statements are true; Statement II is in fact the reason for Statement I.",
    ncert=f"{REF6}, di- and polybasic acids", seconds=30)

s_ab2 = (3.2e-11 / 4) ** (1 / 3)
assert close(s_ab2, 2.0e-4) and close(math.sqrt(3.2e-11), 5.66e-6) and close(3.2e-11 ** (1 / 3), 3.17e-4)
add("Solubility product", B, "numerical",
    "The solubility product of a sparingly soluble salt MX₂, which dissolves as MX₂(s) ⇌ M²⁺(aq) + 2X⁻(aq), "
    "is 3.2 × 10⁻¹¹ at 298 K. Its molar solubility in water at 298 K is:",
    Opts("C", "2.0 × 10⁻⁴ mol L⁻¹", ["5.66 × 10⁻⁶ mol L⁻¹", "3.17 × 10⁻⁴ mol L⁻¹", "4.0 × 10⁻⁴ mol L⁻¹"]),
    "Molar solubility from K_sp for an AB₂-type salt",
    "If s mol L⁻¹ dissolves, [M²⁺] = s and [X⁻] = 2s, so K_sp = s(2s)² = 4s³.",
    ["4s³ = 3.2 × 10⁻¹¹ → s³ = 8.0 × 10⁻¹²", "s = 2.0 × 10⁻⁴ mol L⁻¹"],
    why="5.66 × 10⁻⁶ treats the salt as AB-type (s = √K_sp). 3.17 × 10⁻⁴ takes the cube root of K_sp without "
        "the factor 4. 4.0 × 10⁻⁴ mol L⁻¹ is [X⁻] = 2s, not the solubility.",
    ncert=f"{REF6}, solubility product constant", seconds=40, checked=True)

add("Kp, Kc and Le Chatelier", B, "assertion_reason",
    ar("When the equilibrium mixture C(s) + H₂O(g) ⇌ CO(g) + H₂(g) is compressed to a smaller volume at "
       "constant temperature, the equilibrium shifts in the backward direction.",
       "Compressing the mixture increases the equilibrium constant K_p of this reaction."),
    AR_, "Effect of pressure on a heterogeneous gaseous equilibrium",
    "Counting only gases, the forward reaction turns 1 mol of gas into 2 mol. Raising the pressure by "
    "compression favours the side with fewer moles of gas, so the equilibrium shifts backward; A is true. "
    "K_p depends only on temperature, so compression does not change it; R is false. The shift happens "
    "because the reaction quotient becomes larger than K_p.",
    ["A: Δn(g) = +1, compression favours fewer gas moles → backward → true",
     "R: K changes only with temperature → false"],
    answer="C",
    why="The shift is explained by Le Chatelier's principle (Q_p > K_p after compression), not by any change in "
        "K_p.",
    ncert=f"{REF6}, effect of pressure change; factors affecting equilibria", seconds=40)

V = 2.0
so3, so2, o2 = 1.2 / V, (2.0 - 1.2) / V, (1.5 - 0.6) / V
kc = so3 ** 2 / (so2 ** 2 * o2)
assert close(kc, 5.0) and close(so3 / (so2 * o2), 3.33, 0.01) and close(1.2 ** 2 / (0.8 ** 2 * 0.9), 2.5) \
    and close(so3 ** 2 / (so2 ** 2 * (0.3 / V)), 15.0)
add("Kp, Kc and Le Chatelier", I, "numerical",
    "2.0 mol of SO₂ and 1.5 mol of O₂ are heated in a closed 2.0 L vessel. At equilibrium, 1.2 mol of SO₃ is "
    "present: 2SO₂(g) + O₂(g) ⇌ 2SO₃(g). The value of K_c at this temperature is:",
    Opts("D", "5.0 L mol⁻¹", ["3.33 L mol⁻¹", "2.5 L mol⁻¹", "15 L mol⁻¹"]),
    "Equilibrium constant from initial amounts and the amount of product",
    "Use the stoichiometry to find the equilibrium amounts, convert them to concentrations with the vessel "
    "volume, and substitute in K_c = [SO₃]²/([SO₂]²[O₂]).",
    ["SO₃ formed = 1.2 mol → SO₂ used = 1.2 mol, O₂ used = 0.6 mol",
     "At equilibrium: SO₂ = 0.8 mol, O₂ = 0.9 mol, SO₃ = 1.2 mol",
     "Concentrations: [SO₃] = 0.6, [SO₂] = 0.4, [O₂] = 0.45 mol L⁻¹",
     "K_c = 0.6²/(0.4² × 0.45) = 0.36/0.072 = 5.0 L mol⁻¹"],
    why="3.33 ignores the squares in the expression. 2.5 uses amounts in moles instead of concentrations. "
        "15 subtracts all 1.2 mol from the O₂, ignoring the 2 : 1 ratio.",
    ncert=f"{REF6}, equilibrium constant and its calculation", seconds=90, checked=True)

add("Hydrolysis and buffers", I, "assertion_reason",
    ar("The pH of an aqueous solution of ammonium acetate at 298 K is practically independent of its "
       "concentration.",
       "For a salt of a weak acid and a weak base, pH = 7 + ½(pK_a − pK_b), an expression that contains no "
       "concentration term."),
    AR_, "Hydrolysis of a salt of a weak acid and a weak base",
    "Both NH₄⁺ and CH₃COO⁻ hydrolyse. NCERT gives pH = 7 + ½(pK_a − pK_b) for such a salt, which depends only "
    "on the two ionisation constants, so diluting the solution does not change its pH appreciably. R explains "
    "A.",
    ["A: pH of CH₃COONH₄ solution does not depend on c → true",
     "R: pH = 7 + ½(pK_a − pK_b) has no c → true and explains A"],
    answer="A",
    why="The concentration cancels out because both ions hydrolyse; R states this result.",
    ncert=f"{REF6}, hydrolysis of salts and the pH of their solutions", seconds=40)

add("Hydrolysis and buffers", I, "multi_statement",
    ms("Which of the following statements about 0.1 M aqueous solutions at 298 K are correct?",
       ["A solution of (NH₄)₂SO₄ is acidic.", "A solution of Na₂CO₃ is basic.",
        "A solution of KNO₃ has pH 7.", "A solution of NaCl is acidic.",
        "A solution of CH₃COOK is acidic."]),
    multi("B", {"a": True, "b": True, "c": True, "d": False, "e": False},
          ["(a) and (b) only", "(a), (b), (c) and (e) only", "(b), (c) and (d) only"]),
    "Acidic, basic and neutral salt solutions",
    "A salt of a strong acid and a weak base, such as (NH₄)₂SO₄, gives an acidic solution because NH₄⁺ "
    "hydrolyses. Salts of weak acids with strong bases, such as Na₂CO₃ and CH₃COOK, give basic solutions "
    "because the anion hydrolyses. Salts of a strong acid and a strong base, such as KNO₃ and NaCl, do not "
    "hydrolyse and are neutral.",
    ["(a) NH₄⁺ + H₂O ⇌ NH₃ + H₃O⁺ → acidic → true", "(b) CO₃²⁻ + H₂O ⇌ HCO₃⁻ + OH⁻ → basic → true",
     "(c) KNO₃ neutral → true", "(d) NaCl neutral → false", "(e) CH₃COO⁻ hydrolysis → basic → false"],
    why="Options with (d) or (e) are wrong, and (a) and (b) only misses the true statement (c).",
    ncert=f"{REF6}, hydrolysis of salts and the pH of their solutions", seconds=60)

dn = {"N2O4 -> 2NO2": 2 - 1, "N2 + 3H2 -> 2NH3": 2 - 4, "H2 + I2 -> 2HI": 2 - 2, "PCl3 + Cl2 -> PCl5": 1 - 2}
assert list(dn.values()) == [1, -2, 0, -1]
add("Kp, Kc and Le Chatelier", I, "match_list",
    lists("Match List-I (gaseous equilibrium) with List-II (relation between K_p and K_c).",
          ["N₂O₄(g) ⇌ 2NO₂(g)", "N₂(g) + 3H₂(g) ⇌ 2NH₃(g)", "H₂(g) + I₂(g) ⇌ 2HI(g)",
           "PCl₃(g) + Cl₂(g) ⇌ PCl₅(g)"],
          ["K_p = K_c", "K_p = K_c(RT)", "K_p = K_c(RT)⁻¹", "K_p = K_c(RT)⁻²"]),
    match("D", M("II IV I III"), [M("III IV I II"), M("II I IV III"), M("IV II I III")]),
    "Relation between K_p and K_c",
    "K_p = K_c(RT)^Δn, where Δn = (moles of gaseous products) − (moles of gaseous reactants) in the balanced "
    "equation.",
    ["A: Δn = 2 − 1 = +1 → K_c(RT) (II)", "B: Δn = 2 − 4 = −2 → K_c(RT)⁻² (IV)", "C: Δn = 0 → K_p = K_c (I)",
     "D: Δn = 1 − 2 = −1 → K_c(RT)⁻¹ (III)"],
    why="The other codes take Δn as reactants minus products, or mix up −1 and −2.",
    ncert=f"{REF6}, relationship between K_p and K_c", seconds=50)

ratio_buf = 10 ** (5.74 - 4.74)
assert close(ratio_buf, 10)
add("Hydrolysis and buffers", I, "numerical",
    "A buffer of pH 5.74 is to be made from acetic acid and sodium acetate at 298 K. The ratio "
    "[CH₃COO⁻]/[CH₃COOH] needed is (pK_a of CH₃COOH = 4.74):",
    Opts("B", "10", ["0.1", "1", "100"]),
    "Henderson–Hasselbalch equation for an acidic buffer",
    "pH = pK_a + log([salt]/[acid]), so log([CH₃COO⁻]/[CH₃COOH]) = pH − pK_a.",
    ["log ratio = 5.74 − 4.74 = 1.00", "ratio = 10¹ = 10"],
    why="0.1 inverts the ratio (acid/salt). 1 gives pH = pK_a = 4.74. 100 corresponds to pH 6.74.",
    ncert=f"{REF6}, buffer solutions", seconds=35, checked=True)

ka = {"HF": 6.8e-4, "HCOOH": 1.8e-4, "CH3COOH": 1.8e-5, "HCN": 4.9e-10}
kb_conj = {k: 1e-14 / v for k, v in ka.items()}
assert max(kb_conj, key=kb_conj.get) == "HCN"
add("Acids, bases and pH", I, "direct",
    "The ionisation constants of four acids at 298 K are: HF 6.8 × 10⁻⁴, HCOOH 1.8 × 10⁻⁴, CH₃COOH 1.8 × 10⁻⁵ "
    "and HCN 4.9 × 10⁻¹⁰. Which of the following is the strongest base?",
    Opts("C", "CN⁻", ["F⁻", "HCOO⁻", "CH₃COO⁻"]),
    "Strengths of conjugate acid–base pairs, K_a × K_b = K_w",
    "For a conjugate pair, K_a × K_b = K_w, so the weaker the acid, the stronger its conjugate base. HCN has "
    "the smallest K_a, so CN⁻ has the largest K_b (about 2 × 10⁻⁵).",
    ["K_b = K_w/K_a", "Smallest K_a (HCN) → largest K_b → CN⁻ is the strongest base"],
    why="F⁻, HCOO⁻ and CH₃COO⁻ are conjugate bases of stronger acids, so they are weaker bases than CN⁻.",
    ncert=f"{REF6}, relation between K_a and K_b", seconds=40)

add("Acids, bases and pH", I, "statement_pair",
    sp("At 298 K, a solution of pH 8 has [OH⁻] = 1.0 × 10⁻⁸ mol L⁻¹.",
       "At any temperature, an aqueous solution in which [H₃O⁺] = [OH⁻] is neutral."),
    SP_, "pH, pOH and neutrality",
    "At 298 K, pH + pOH = 14, so pH 8 means pOH 6 and [OH⁻] = 1.0 × 10⁻⁶ mol L⁻¹; it is [H₃O⁺] that equals "
    "10⁻⁸ mol L⁻¹. Statement I is false. Neutrality means [H₃O⁺] = [OH⁻], whatever the temperature; only the "
    "pH of a neutral solution changes with temperature because K_w changes. Statement II is true.",
    ["I: pOH = 14 − 8 = 6 → [OH⁻] = 10⁻⁶ M → false", "II: definition of a neutral solution → true"],
    answer="D",
    why="Statement I gives [H₃O⁺] instead of [OH⁻].",
    ncert=f"{REF6}, ionisation of water and the pH scale", seconds=35)

ag_cl = 1.8e-10 / 0.010
ag_cro4 = math.sqrt(1.1e-12 / 0.010)
assert ag_cl < ag_cro4 and close(ag_cl, 1.8e-8) and close(ag_cro4, 1.05e-5, 0.01)
assert 1.1e-12 / 0.010 < ag_cl  # the trap: forgetting the square root makes chromate look first
add("Solubility product", A, "numerical",
    "Silver nitrate solution is added drop by drop to a solution that is 0.010 M in Cl⁻ and 0.010 M in CrO₄²⁻ "
    "at 298 K. K_sp(AgCl) = 1.8 × 10⁻¹⁰ and K_sp(Ag₂CrO₄) = 1.1 × 10⁻¹². Ignoring the volume change, which "
    "salt precipitates first, and at what [Ag⁺] does it begin to precipitate? (√1.1 = 1.05)",
    Opts("D", "AgCl first, at [Ag⁺] = 1.8 × 10⁻⁸ M",
         ["Ag₂CrO₄ first, at [Ag⁺] = 1.1 × 10⁻¹⁰ M", "AgCl first, at [Ag⁺] = 1.34 × 10⁻⁵ M",
          "Ag₂CrO₄ first, at [Ag⁺] = 1.05 × 10⁻⁵ M"]),
    "Selective precipitation using K_sp",
    "A salt starts to precipitate when its ionic product reaches K_sp. Find the [Ag⁺] needed for each salt; "
    "the one needing the smaller [Ag⁺] precipitates first. Note the square in K_sp(Ag₂CrO₄) = [Ag⁺]²[CrO₄²⁻].",
    ["AgCl: [Ag⁺] = 1.8 × 10⁻¹⁰/0.010 = 1.8 × 10⁻⁸ M",
     "Ag₂CrO₄: [Ag⁺]² = 1.1 × 10⁻¹²/0.010 = 1.1 × 10⁻¹⁰ → [Ag⁺] = 1.05 × 10⁻⁵ M",
     "1.8 × 10⁻⁸ M < 1.05 × 10⁻⁵ M → AgCl precipitates first"],
    why="1.1 × 10⁻¹⁰ M forgets to take the square root for Ag₂CrO₄. 1.34 × 10⁻⁵ M is the solubility of AgCl in "
        "pure water, ignoring the 0.010 M Cl⁻. 1.05 × 10⁻⁵ M is where Ag₂CrO₄ starts, which is later.",
    ncert=f"{REF6}, solubility product; common ion effect on solubility", seconds=120, checked=True)

c_salt = 0.2 * 50 / 100
ph_nh4cl = 7 - 0.5 * 4.74 - 0.5 * math.log10(c_salt)
assert close(c_salt, 0.1) and close(ph_nh4cl, 5.13, 0.002)
assert close(7 - 0.5 * 4.74 - 0.5 * math.log10(0.2), 4.98, 0.002) and close(7 - 2.37 - 0.5, 4.13) \
    and close(7 + 2.37 - 0.5, 8.87)
add("Hydrolysis and buffers", A, "numerical",
    "50 mL of 0.2 M aqueous ammonia (NH₄OH) is mixed with 50 mL of 0.2 M HCl at 298 K. The pH of the resulting "
    "solution is (pK_b of NH₄OH = 4.74; log 2 = 0.30):",
    Opts("B", "5.13", ["4.98", "4.13", "8.87"]),
    "pH at the equivalence point of a weak base–strong acid reaction (salt hydrolysis)",
    "Equal amounts of NH₄OH and HCl react completely to give NH₄Cl, the salt of a weak base and a strong acid, "
    "in 100 mL. NH₄⁺ hydrolyses, and pH = 7 − ½pK_b − ½log c.",
    ["n(NH₄OH) = n(HCl) = 0.010 mol → 0.010 mol NH₄Cl in 0.100 L → c = 0.10 M",
     "pH = 7 − ½(4.74) − ½ log 0.10 = 7 − 2.37 + 0.50 = 5.13"],
    why="4.98 forgets that mixing halves the concentration (uses c = 0.2 M). 4.13 subtracts ½ log c with the "
        "wrong sign. 8.87 uses the formula for the salt of a weak acid and a strong base.",
    ncert=f"{REF6}, hydrolysis of salts and the pH of their solutions", seconds=100, checked=True)

mixes = {"NH4OH 5.0 mmol + HCl 2.5 mmol": ("buffer", 2.5, 2.5), "NH4OH 5.0 + HCl 5.0": ("salt only", 0, 5.0),
         "CH3COOH 5.0 + NaOH 6.0": ("excess strong base", 0, 5.0)}
assert 5.0 - 2.5 == 2.5
add("Hydrolysis and buffers", A, "direct",
    "Which of the following mixtures acts as a buffer solution?",
    Opts("C", "50 mL of 0.1 M NH₄OH + 25 mL of 0.1 M HCl",
         ["50 mL of 0.1 M NH₄OH + 50 mL of 0.1 M HCl", "50 mL of 0.1 M CH₃COOH + 60 mL of 0.1 M NaOH",
          "50 mL of 0.1 M HCl + 50 mL of 0.1 M NaCl"]),
    "Preparing a buffer by partial neutralisation",
    "A buffer needs a weak acid with its salt, or a weak base with its salt. Half-neutralising NH₄OH with HCl "
    "leaves equal amounts of NH₄OH and NH₄Cl, which is a basic buffer.",
    ["5.0 mmol NH₄OH + 2.5 mmol HCl → 2.5 mmol NH₄OH + 2.5 mmol NH₄Cl → buffer"],
    why="Equal amounts of NH₄OH and HCl leave only NH₄Cl. 6.0 mmol NaOH with 5.0 mmol CH₃COOH leaves excess "
        "strong base and no weak acid. HCl with NaCl is a strong acid with its salt, which does not buffer.",
    ncert=f"{REF6}, buffer solutions", seconds=75)

add("Kp, Kc and Le Chatelier", A, "multi_statement",
    ms("For the equilibrium C(s) + CO₂(g) ⇌ 2CO(g), ΔH > 0, set up in a closed vessel, which of the "
       "following statements are correct?",
       ["K_p = p²(CO)/p(CO₂).", "K_p = K_c(RT).",
        "Adding more solid carbon at constant volume and temperature shifts the equilibrium in the forward "
        "direction.",
        "Raising the temperature increases the equilibrium constant.",
        "Compressing the mixture to a smaller volume at constant temperature increases the amount of CO at "
        "equilibrium."]),
    multi("B", {"a": True, "b": True, "c": False, "d": True, "e": False},
          ["(a), (b) and (c) only", "(a), (d) and (e) only", "(b) and (d) only"]),
    "Heterogeneous equilibrium: K_p expression, K_p–K_c relation and Le Chatelier's principle",
    "A pure solid does not appear in the equilibrium constant, so K_p = p²(CO)/p(CO₂). Δn(g) = 2 − 1 = +1, so "
    "K_p = K_c(RT). Adding carbon changes nothing because its 'concentration' is constant. For an endothermic "
    "reaction, K increases with temperature. Compression favours the side with fewer gas moles, so CO "
    "decreases.",
    ["(a) solid omitted → true", "(b) Δn(g) = +1 → true", "(c) pure solid does not shift the equilibrium → false",
     "(d) endothermic → K rises with T → true", "(e) compression shifts backward → CO decreases → false"],
    why="Options with (c) or (e) are wrong, and (b) and (d) only leaves out the true statement (a).",
    ncert=f"{REF6}, heterogeneous equilibria; relation between K_p and K_c; Le Chatelier's principle",
    seconds=90)

pkw = 14 - 0.74  # Kw = 5.5e-14 -> pKw = -log(5.5e-14) = 14 - log 5.5
ph_hot = pkw - 3
assert close(-math.log10(5.5e-14), pkw, 0.001) and close(ph_hot, 10.26)
add("Acids, bases and pH", A, "numerical",
    "The ionic product of water at 323 K is K_w = 5.5 × 10⁻¹⁴. The pH of a 1.0 × 10⁻³ M aqueous solution of "
    "NaOH at 323 K, assuming complete dissociation, is (log 5.5 = 0.74):",
    Opts("A", "10.26", ["11.00", "11.74", "6.63"]),
    "pH of a strong base when K_w is not 10⁻¹⁴",
    "pH + pOH = pK_w at any temperature. At 323 K, pK_w is less than 14, so a base of given [OH⁻] has a lower "
    "pH than it would at 298 K.",
    ["pOH = −log(1.0 × 10⁻³) = 3.00", "pK_w = −log(5.5 × 10⁻¹⁴) = 14 − 0.74 = 13.26",
     "pH = 13.26 − 3.00 = 10.26"],
    why="11.00 uses pK_w = 14, valid only at 298 K. 11.74 adds log 5.5 instead of subtracting it. 6.63 is the "
        "pH of pure (neutral) water at 323 K.",
    ncert=f"{REF6}, ionisation of water; the pH scale", seconds=90, checked=True)

# ==================================================================== 7. Redox Reactions and Electrochemistry
topic("Redox Reactions and Electrochemistry")
REF7A = f"{C11}, 'Redox Reactions'"
REF7B = f"{C12}, 'Electrochemistry'"

assert 1e-4 * (100 ** 2) == 1  # 1 m² = 10⁴ cm², so 1 S cm² mol⁻¹ = 10⁻⁴ S m² mol⁻¹
add("Conductance and Kohlrausch's law", B, "direct",
    "A molar conductivity of 1 S cm² mol⁻¹ is equal to:",
    Opts("D", "1 × 10⁻⁴ S m² mol⁻¹", ["1 × 10⁻² S m² mol⁻¹", "1 × 10² S m² mol⁻¹", "1 × 10⁴ S m² mol⁻¹"]),
    "Units of molar conductivity",
    "Since 1 m = 100 cm, 1 m² = 10⁴ cm², so 1 cm² = 10⁻⁴ m². Therefore 1 S cm² mol⁻¹ = 10⁻⁴ S m² mol⁻¹.",
    ["1 cm² = (10⁻² m)² = 10⁻⁴ m²", "1 S cm² mol⁻¹ = 10⁻⁴ S m² mol⁻¹"],
    why="10⁻² converts a length, not an area. 10² and 10⁴ convert in the wrong direction.",
    ncert=f"{REF7B}, measurement of the conductivity of ionic solutions; molar conductivity", seconds=25)

on_nh4 = 0 - 4 * (+1)       # N in NH4+ : x + 4 = +1
on_no3 = -1 - 3 * (-2)      # N in NO3- : x - 6 = -1
assert (on_nh4 + 1, on_no3) == (-3, 5)
add("Oxidation number and balancing", B, "direct",
    "The oxidation numbers of the two nitrogen atoms in ammonium nitrate, NH₄NO₃, are:",
    Opts("C", "−3 and +5", ["+1 and +1", "−3 and +3", "+3 and +5"]),
    "Oxidation numbers in a compound with two different ions",
    "Treat the ions separately. In NH₄⁺: x + 4(+1) = +1 → x = −3. In NO₃⁻: x + 3(−2) = −1 → x = +5.",
    ["NH₄⁺: x = −3", "NO₃⁻: x = +5"],
    why="+1 and +1 is the average (sum zero shared over two atoms), which hides the two different "
        "environments. −3 and +3, and +3 and +5, miscalculate one of the ions.",
    ncert=f"{REF7A}, oxidation number", seconds=30)

add("Batteries and fuel cells", B, "assertion_reason",
    ar("In the dry (Leclanché) cell, manganese is reduced at the cathode.",
       "In the cathode reaction MnO₂ + NH₄⁺ + e⁻ → MnO(OH) + NH₃, the oxidation state of manganese changes "
       "from +4 to +3."),
    AR_, "Electrode reactions of the dry cell",
    "Reduction is a decrease in oxidation number. In MnO₂, Mn is +4. In MnO(OH), with O = −2 and H = +1, "
    "x + (−2) + (−2) + 1 = 0 gives x = +3. The gain of one electron by each Mn at the carbon cathode is the "
    "reduction stated in A. R explains A.",
    ["MnO₂: Mn = +4; MnO(OH): Mn = +3", "Decrease in oxidation number → reduction at the cathode"],
    answer="A",
    why="R shows the change in oxidation state that makes the cathode process a reduction.",
    ncert=f"{REF7B}, batteries: primary batteries (dry cell); {REF7A}, oxidation number", seconds=40)

add("Batteries and fuel cells", B, "match_list",
    lists("Match List-I (cell) with List-II (its description).",
          ["Dry (Leclanché) cell", "Lead storage battery", "Hydrogen–oxygen fuel cell", "Daniell cell"],
          ["Reactants are fed in continuously, and the energy of combustion of the fuel is converted directly "
           "into electrical energy",
           "Zinc and copper electrodes in solutions of their ions; standard emf 1.1 V",
           "Primary battery: its reaction occurs only once, and it cannot be recharged",
           "Secondary battery: it can be recharged by passing a current through it in the opposite direction"]),
    match("D", M("III IV I II"), [M("IV III I II"), M("III IV II I"), M("I IV III II")]),
    "Types of electrochemical cells",
    "The dry cell is a primary battery; after use it cannot be recharged. The lead storage battery is a "
    "secondary battery and is recharged by reversing the current. A fuel cell converts the energy of "
    "combustion of fuels such as hydrogen directly into electrical energy, with reactants supplied "
    "continuously. The Daniell cell uses Zn and Cu electrodes and has E° = 1.1 V.",
    ["A → III", "B → IV", "C → I", "D → II"],
    why="The other codes interchange primary and secondary batteries, or the fuel cell with the Daniell cell.",
    ncert=f"{REF7B}, batteries and fuel cells; galvanic cells", seconds=40)

# 2MnO4- + 6I- + 4H2O -> 2MnO2 + 3I2 + 8OH-
left = {"Mn": 2, "O": 8 + 4, "I": 6, "H": 8}
right = {"Mn": 2, "O": 4 + 8, "I": 6, "H": 8}
assert left == right and (2 * -1 + 6 * -1) == (8 * -1)
assert 2 * 3 == 6 * 1  # electrons: each Mn gains 3 (+7 -> +4), each I- loses 1
add("Oxidation number and balancing", I, "numerical",
    "In a basic solution, permanganate ion oxidises iodide ion to iodine and is itself reduced to manganese "
    "dioxide: MnO₄⁻(aq) + I⁻(aq) → MnO₂(s) + I₂(s). When the ionic equation is balanced with the smallest whole "
    "numbers (using H₂O and OH⁻), the coefficients of I⁻ and OH⁻ are respectively:",
    Opts("C", "6 and 8", ["10 and 16", "6 and 4", "3 and 8"]),
    "Balancing a redox equation in basic medium (half-reaction method)",
    "Mn goes from +7 to +4 (gains 3 e⁻) and I from −1 to 0 (loses 1 e⁻ per I⁻). Balance the half-reactions in "
    "basic medium and multiply to equalise the electrons.",
    ["Reduction: MnO₄⁻ + 2H₂O + 3e⁻ → MnO₂ + 4OH⁻ (× 2)", "Oxidation: 2I⁻ → I₂ + 2e⁻ (× 3)",
     "Sum: 2MnO₄⁻ + 6I⁻ + 4H₂O → 2MnO₂ + 3I₂ + 8OH⁻",
     "Check: charge −8 on each side; O 12 = 12; H 8 = 8"],
    why="10 and 16 come from the acidic-medium equation (MnO₄⁻ → Mn²⁺, with 16H⁺). 4 is the coefficient of "
        "H₂O, not OH⁻. 3 is the coefficient of I₂, not I⁻.",
    ncert=f"{REF7A}, balancing of redox reactions: half-reaction method", seconds=100, checked=True)

add("Conductance and Kohlrausch's law", I, "multi_statement",
    ms("Which of the following statements about the conductivity of electrolytic (ionic) solutions are "
       "correct?",
       ["It depends on the nature of the electrolyte added.",
        "It depends on the size of the ions produced and their solvation.",
        "It depends on the nature of the solvent and its viscosity.",
        "It decreases as the temperature of the solution increases.",
        "It is due to the movement of electrons through the solution."]),
    multi("D", {"a": True, "b": True, "c": True, "d": False, "e": False},
          ["(a) and (b) only", "(a), (b), (c) and (d) only", "(b), (c) and (e) only"]),
    "Factors affecting ionic (electrolytic) conductance",
    "NCERT lists the factors on which the conductivity of electrolytic solutions depends: the nature of the "
    "electrolyte, the size of the ions and their solvation, the nature of the solvent and its viscosity, the "
    "concentration and the temperature. Ionic conductance is due to the movement of ions, and it increases "
    "with rising temperature.",
    ["(a), (b), (c): listed factors → true", "(d) ionic conductance increases with temperature → false",
     "(e) charge is carried by ions, not electrons → false"],
    why="(d) describes metallic conduction, and (e) confuses electronic with electrolytic conduction; (a) and "
        "(b) only misses the true statement (c).",
    ncert=f"{REF7B}, conductance of electrolytic solutions", seconds=50)

e_ph = {ph: -0.059 * ph for ph in (1, 4, 7)}
assert e_ph[1] > e_ph[4] > e_ph[7]
add("Nernst equation and Gibbs energy", I, "assertion_reason",
    ar("At 298 K, the reduction potential of a hydrogen electrode with p(H₂) = 1 bar becomes more negative as "
       "the pH of its solution increases.",
       "For this electrode, the Nernst equation gives E = −0.059 pH volt at 298 K."),
    AR_, "Nernst equation for the hydrogen electrode",
    "For H⁺(aq) + e⁻ → ½H₂(g), E = E° − 0.059 log(p(H₂)^½/[H⁺]) = 0 + 0.059 log[H⁺] = −0.059 pH at 298 K "
    "with p(H₂) = 1 bar. As pH rises, E falls (becomes more negative). R explains A.",
    ["E = −0.059 log(1/[H⁺]) = −0.059 pH", "pH 1 → −0.059 V; pH 7 → −0.413 V: more negative"],
    answer="A",
    why="R gives the quantitative relation from which A follows.",
    ncert=f"{REF7B}, Nernst equation", seconds=45)

couples = {"Ag+": 0.80, "Cu2+": 0.34, "Ni2+": -0.25, "Zn2+": -0.76}
assert [k for k, v in couples.items() if v - 0.77 > 0] == ["Ag+"]
add("Electrode potential and cells", I, "direct",
    "Given the standard reduction potentials E°(Fe³⁺/Fe²⁺) = +0.77 V, E°(Ag⁺/Ag) = +0.80 V, "
    "E°(Cu²⁺/Cu) = +0.34 V, E°(Ni²⁺/Ni) = −0.25 V and E°(Zn²⁺/Zn) = −0.76 V, which of the following ions can "
    "oxidise Fe²⁺ to Fe³⁺ under standard conditions?",
    Opts("A", "Ag⁺", ["Cu²⁺", "Ni²⁺", "Zn²⁺"]),
    "Predicting redox reactions from electrode potentials",
    "An ion can oxidise Fe²⁺ to Fe³⁺ under standard conditions only if its own reduction potential is higher "
    "than that of Fe³⁺/Fe²⁺ (+0.77 V), so that E°cell is positive.",
    ["Ag⁺: E°cell = 0.80 − 0.77 = +0.03 V > 0 → feasible",
     "Cu²⁺: 0.34 − 0.77 < 0; Ni²⁺ and Zn²⁺ even more negative → not feasible"],
    why="Cu²⁺, Ni²⁺ and Zn²⁺ all have reduction potentials below +0.77 V, so the reaction would have a negative "
        "E°cell.",
    ncert=f"{REF7B}, electrode potential and the electrochemical series", seconds=45)

add("Batteries and fuel cells", I, "statement_pair",
    sp("During the discharge of a lead storage battery, PbO₂ at the cathode is oxidised.",
       "During the charging of a lead storage battery, sulphuric acid is consumed."),
    SP_, "Reactions in the lead storage battery",
    "During discharge, Pb at the anode is oxidised (0 → +2) and PbO₂ at the cathode is REDUCED (+4 → +2), both "
    "forming PbSO₄ and consuming H₂SO₄. Charging reverses this: PbSO₄ is converted back to Pb and PbO₂ and "
    "sulphuric acid is regenerated, not consumed. Both statements are false.",
    ["I: PbO₂ (+4) → PbSO₄ (+2) is a reduction → false",
     "II: charging regenerates H₂SO₄ → false"],
    answer="B",
    why="Statement I mistakes the cathode reduction for an oxidation; Statement II describes discharge, not "
        "charging.",
    ncert=f"{REF7B}, secondary batteries: lead storage battery", seconds=40)

add("Nernst equation and Gibbs energy", I, "match_list",
    lists("Match List-I (condition for a cell) with List-II (what it implies about the cell reaction at that "
          "temperature).",
          ["E°cell > 0", "E°cell < 0", "E°cell = 0", "E_cell = 0"],
          ["ΔrG° = 0 and K = 1", "The cell reaction has reached equilibrium (Q = K)",
           "ΔrG° < 0 and K > 1", "ΔrG° > 0 and K < 1"]),
    match("C", M("III IV I II"), [M("IV III I II"), M("III IV II I"), M("I IV III II")]),
    "Relations among E°cell, ΔrG°, K and E_cell",
    "ΔrG° = −nFE°cell and ΔrG° = −RT ln K. A positive E°cell gives a negative ΔrG° and K > 1; a negative "
    "E°cell gives K < 1; E°cell = 0 gives ΔrG° = 0 and K = 1. E_cell (not E°) becomes zero when the cell is "
    "fully discharged, i.e. the reaction is at equilibrium and Q = K.",
    ["A → III", "B → IV", "C → I", "D → II"],
    why="The trap is to treat E°cell = 0 and E_cell = 0 as the same condition; one is about standard states, "
        "the other about the actual mixture reaching equilibrium.",
    ncert=f"{REF7B}, equilibrium constant from the Nernst equation; electrochemical cell and Gibbs energy",
    seconds=55)

e_cell = 0.76 - (0.059 / 2) * math.log10(0.1 / 0.01 ** 2)
assert close(e_cell, 0.67, 0.005) and close(0.76 + 0.0295 * 3, 0.85, 0.005) \
    and close(0.76 - 0.0295 * math.log10(0.1 / 0.01), 0.73, 0.005) and close(0.76 - 0.059 * 3, 0.58, 0.01)
add("Nernst equation and Gibbs energy", A, "numerical",
    "Calculate the emf at 298 K of the cell Zn(s) | Zn²⁺(aq, 0.1 M) || H⁺(aq, pH = 2) | H₂(g, 1 bar) | Pt, whose "
    "cell reaction is Zn(s) + 2H⁺(aq) → Zn²⁺(aq) + H₂(g). (E°(Zn²⁺/Zn) = −0.76 V; 2.303RT/F = 0.059 V)",
    Opts("D", "0.67 V", ["0.85 V", "0.73 V", "0.58 V"]),
    "Nernst equation for a cell with a hydrogen electrode",
    "E°cell = E°(cathode) − E°(anode) = 0 − (−0.76) = +0.76 V. Two electrons are transferred, and "
    "E_cell = E°cell − (0.059/2) log([Zn²⁺] p(H₂)/[H⁺]²).",
    ["[H⁺] = 10⁻² M; Q = 0.1 × 1/(10⁻²)² = 10³",
     "E_cell = 0.76 − 0.0295 × log 10³ = 0.76 − 0.0885 = 0.67 V"],
    why="0.85 V adds the correction (Q inverted). 0.73 V forgets to square [H⁺]. 0.58 V uses 0.059 instead of "
        "0.059/2 for a two-electron reaction.",
    ncert=f"{REF7B}, Nernst equation", seconds=100, checked=True)

# 2MnO4- + 5H2O2 + 6H+ -> 2Mn2+ + 5O2 + 8H2O
lhs = {"Mn": 2, "O": 8 + 10, "H": 10 + 6, "charge": -2 + 6}
rhs = {"Mn": 2, "O": 10 + 8, "H": 16, "charge": 2 * 2}
assert lhs == rhs and 2 * 5 == 5 * 2 == 10
add("Oxidation number and balancing", A, "multi_statement",
    ms("Consider the balanced equation 2MnO₄⁻ + 5H₂O₂ + 6H⁺ → 2Mn²⁺ + 5O₂ + 8H₂O. Which of the following "
       "statements are correct?",
       ["H₂O₂ acts as a reducing agent.",
        "The oxidation number of oxygen in H₂O₂ changes from −1 to 0.",
        "Each MnO₄⁻ ion gains five electrons.",
        "A total of five electrons is transferred in the reaction as written.",
        "The coefficient of H⁺ in the balanced equation would be 16 if it were written correctly."]),
    multi("C", {"a": True, "b": True, "c": True, "d": False, "e": False},
          ["(a) and (c) only", "(a), (b), (c) and (d) only", "(b), (c) and (e) only"]),
    "Oxidising and reducing agents; electron count in a balanced redox equation",
    "Mn goes from +7 in MnO₄⁻ to +2 in Mn²⁺, a gain of 5 electrons per ion, so MnO₄⁻ is the oxidising "
    "agent. Oxygen in H₂O₂ (−1) goes to O₂ (0), losing 1 electron per O atom, 2 per H₂O₂, so H₂O₂ is the "
    "reducing agent. As written, 2 × 5 = 10 electrons are transferred (5 H₂O₂ × 2). The equation is already "
    "balanced with 6H⁺: charge +4 on both sides, O 18 = 18, H 16 = 16.",
    ["(a) O.N. of O rises → H₂O₂ is oxidised → reducing agent → true", "(b) −1 → 0 → true",
     "(c) +7 → +2 → 5 e⁻ per MnO₄⁻ → true", "(d) 10 electrons, not 5 → false",
     "(e) the given equation with 6H⁺ is balanced; 16H⁺ belongs to the oxalate reaction → false"],
    why="(d) counts the electrons for one MnO₄⁻ only, and (e) recalls the coefficient from a different reaction.",
    ncert=f"{REF7A}, redox reactions in terms of oxidation number; balancing of redox reactions", seconds=100)

E0_k = 0.059 / 2 * 20
dG0 = -2 * 96500 * E0_k / 1000
assert close(E0_k, 0.59) and close(dG0, -113.9, 0.001) and close(dG0 / 2, -56.9, 0.002) \
    and close(2 * dG0, -227.7, 0.001)
add("Nernst equation and Gibbs energy", A, "numerical",
    "The equilibrium constant of a cell reaction in which two electrons are transferred is 1 × 10²⁰ at 298 K. "
    "The standard Gibbs energy change of the reaction is (2.303RT/F = 0.059 V; F = 96 500 C mol⁻¹):",
    Opts("B", "−113.9 kJ mol⁻¹", ["−56.9 kJ mol⁻¹", "−227.7 kJ mol⁻¹", "+113.9 kJ mol⁻¹"]),
    "Linking K, E°cell and ΔrG°",
    "First find E°cell from log K = nE°cell/0.059, then ΔrG° = −nFE°cell.",
    ["E°cell = (0.059/2) × log 10²⁰ = 0.0295 × 20 = 0.59 V",
     "ΔrG° = −2 × 96 500 × 0.59 = −113 870 J mol⁻¹ ≈ −113.9 kJ mol⁻¹"],
    why="−56.9 kJ mol⁻¹ uses n = 1 in ΔrG° = −nFE°. −227.7 kJ mol⁻¹ forgets to divide by n when finding E° "
        "(taking E° = 0.059 × 20 = 1.18 V). +113.9 kJ mol⁻¹ has the wrong sign for K > 1.",
    ncert=f"{REF7B}, equilibrium constant from the Nernst equation; electrochemical cell and Gibbs energy",
    seconds=90, checked=True)

add("Batteries and fuel cells", A, "statement_pair",
    sp("In the hydrogen–oxygen fuel cell, the reaction at the anode is O₂(g) + 2H₂O(l) + 4e⁻ → 4OH⁻(aq).",
       "The dry (Leclanché) cell has a potential of about 2.0 V."),
    SP_, "Electrode reactions and potentials of commercial cells",
    "In the H₂–O₂ fuel cell, oxidation takes place at the anode: 2H₂(g) + 4OH⁻(aq) → 4H₂O(l) + 4e⁻. The "
    "reaction O₂ + 2H₂O + 4e⁻ → 4OH⁻ is a reduction and occurs at the cathode, so Statement I is false. NCERT "
    "gives the dry cell a potential of nearly 1.5 V, so Statement II is false too.",
    ["I: the reaction quoted is a reduction → cathode, not anode → false",
     "II: dry cell ≈ 1.5 V → false"],
    answer="B",
    why="Both statements are false: Statement I swaps the electrodes and Statement II gives the wrong "
        "potential.",
    ncert=f"{REF7B}, primary batteries; fuel cells", seconds=45)

# ==================================================================== 8. Chemical Kinetics
topic("Chemical Kinetics")
REF8 = f"{C12}, 'Chemical Kinetics'"

add("Rate law and order", B, "direct",
    "The hydrogenation of ethene, C₂H₄(g) + H₂(g) → C₂H₆(g), has the experimentally found rate law "
    "rate = k[C₂H₄]. The overall order of this reaction is:",
    Opts("B", "1", ["2", "0", "3/2"]),
    "Order of reaction from the rate law",
    "The order is the sum of the powers of the concentration terms in the experimental rate law, not the sum "
    "of the coefficients in the balanced equation. Here only [C₂H₄] appears, to the first power.",
    ["rate = k[C₂H₄]¹ → order = 1"],
    why="2 adds the stoichiometric coefficients of the balanced equation, which do not decide the order. "
        "0 and 3/2 do not match the rate law.",
    ncert=f"{REF8}, order of a reaction; first-order reactions", seconds=20)

add("Rate law and order", B, "match_list",
    lists("Match List-I (rate law) with List-II (unit of the rate constant, concentration in mol L⁻¹ and time "
          "in s).",
          ["Rate = k", "Rate = k[A]", "Rate = k[A]^½[B]^(3/2)", "Rate = k[A][B]²"],
          ["s⁻¹", "L mol⁻¹ s⁻¹", "mol L⁻¹ s⁻¹", "L² mol⁻² s⁻¹"]),
    match("D", M("III I II IV"), [M("I III II IV"), M("III I IV II"), M("III II I IV")]),
    "Units of the rate constant for different orders",
    "For an overall order n, k has units (mol L⁻¹)^(1−n) s⁻¹. Order 0 → mol L⁻¹ s⁻¹, order 1 → s⁻¹, order 2 "
    "→ L mol⁻¹ s⁻¹, order 3 → L² mol⁻² s⁻¹.",
    ["A: n = 0 → III", "B: n = 1 → I", "C: n = ½ + 3/2 = 2 → II", "D: n = 1 + 2 = 3 → IV"],
    why="The other codes swap the zero- and first-order units, or treat the half-integer powers as a third-"
        "order law.",
    ncert=f"{REF8}, units of rate constant", seconds=40)

add("Arrhenius equation and activation energy", B, "statement_pair",
    sp("When the temperature is raised, the peak of the kinetic energy distribution curve of the molecules "
       "shifts towards higher energy and the curve broadens out.",
       "When the temperature is raised, the total area under the distribution curve increases."),
    SP_, "Maxwell–Boltzmann distribution and the effect of temperature",
    "At a higher temperature the most probable kinetic energy increases, so the peak moves to higher energy, "
    "and the curve spreads out, so a greater fraction of molecules has energy above E_a. Statement I is true. "
    "The area under the curve represents the total number (or fraction) of molecules, which does not change, "
    "so Statement II is false.",
    ["I: peak shifts right and the curve broadens → true",
     "II: area = total probability (number of molecules) → constant → false"],
    answer="C",
    why="Statement II forgets that the curve only redistributes the same number of molecules over energies.",
    ncert=f"{REF8}, temperature dependence of the rate of a reaction", seconds=35)

add("Zero and first order reactions", B, "direct",
    "For a zero-order reaction, a plot of the rate of the reaction against the concentration of the reactant "
    "is:",
    Opts("B", "a straight line parallel to the concentration axis",
         ["a straight line through the origin with slope k", "a straight line with a negative slope",
          "a curve that rises steeply and then levels off"]),
    "Rate of a zero-order reaction",
    "For a zero-order reaction, rate = k[R]⁰ = k, so the rate does not depend on concentration: the plot is a "
    "horizontal line at height k.",
    ["rate = k, independent of [R] → horizontal straight line"],
    why="A straight line through the origin with slope k is the rate–concentration plot of a first-order "
        "reaction. The other shapes do not describe rate = constant.",
    ncert=f"{REF8}, zero-order reactions", seconds=25)

conc = [0.80, 0.60, 0.40]
assert conc[0] - conc[1] == conc[1] - conc[2] or close(conc[0] - conc[1], conc[1] - conc[2])
k1 = math.log(conc[0] / conc[1]) / 10
k2 = math.log(conc[1] / conc[2]) / 10
assert not close(k1, k2, 0.05) and close(k1, 0.0288, 0.005) and close((0.80 - 0.60) / 10, 0.020)
add("Zero and first order reactions", I, "direct",
    "For a reaction R → P at constant temperature, the following data were obtained:\n"
    "t = 0 min: [R] = 0.80 mol L⁻¹; t = 10 min: [R] = 0.60 mol L⁻¹; t = 20 min: [R] = 0.40 mol L⁻¹.\n"
    "The order of the reaction and its rate constant are:",
    Opts("D", "zero order; k = 0.020 mol L⁻¹ min⁻¹",
         ["first order; k = 0.0288 min⁻¹", "zero order; k = 0.20 mol L⁻¹ min⁻¹", "first order; k = 0.020 min⁻¹"]),
    "Identifying the order from concentration–time data",
    "Equal decreases in [R] (0.20 mol L⁻¹) in equal times (10 min) show a constant rate, the mark of a "
    "zero-order reaction, [R] = [R]₀ − kt. For a first-order reaction [R] would fall by equal FRACTIONS in "
    "equal times, but 0.60/0.80 = 0.75 while 0.40/0.60 = 0.67.",
    ["Δ[R] = 0.20 mol L⁻¹ every 10 min → constant rate → zero order",
     "k = 0.20/10 = 0.020 mol L⁻¹ min⁻¹"],
    why="0.0288 min⁻¹ comes from applying the first-order equation to the first interval only; the second "
        "interval would give a different k, so the data are not first order. 0.20 mol L⁻¹ min⁻¹ forgets to "
        "divide by 10 min. 0.020 min⁻¹ has the right number but the first-order unit.",
    ncert=f"{REF8}, integrated rate equations: zero-order reactions", seconds=75)

assert 2 ** 2 * 2 == 8
add("Rate law and order", I, "numerical",
    "The reaction 2NO(g) + O₂(g) → 2NO₂(g) has the rate law rate = k[NO]²[O₂]. If the volume of the reaction "
    "vessel is suddenly reduced to half at constant temperature, the rate of the reaction becomes:",
    Opts("C", "8 times the original rate", ["4 times the original rate", "2 times the original rate",
                                            "1/8 of the original rate"]),
    "Effect of concentration on rate through the rate law",
    "Halving the volume doubles the concentration of every gas. Substitute 2[NO] and 2[O₂] in the rate law.",
    ["New rate = k(2[NO])²(2[O₂]) = 8k[NO]²[O₂]", "Rate becomes 8 times"],
    why="4 times doubles only [NO]. 2 times doubles only [O₂]. 1/8 treats halving the volume as halving the "
        "concentrations.",
    ncert=f"{REF8}, dependence of rate on concentration: rate law", seconds=40, checked=True)

t_half = [1.0 / 2, 0.5 / 2]  # successive half-lives ∝ starting concentration (zero order, k = 1)
assert t_half[1] == t_half[0] / 2
add("Half-life", I, "assertion_reason",
    ar("For a zero-order reaction, each successive half-life is half as long as the one before it.",
       "The half-life of a zero-order reaction, t½ = [R]₀/2k, is directly proportional to the initial "
       "concentration of the reactant."),
    AR_, "Half-life of a zero-order reaction",
    "After one half-life the concentration is [R]₀/2, and this becomes the 'initial' concentration for the "
    "next half-life. Since t½ ∝ [R]₀, the second half-life is [R]₀/4k, half of the first, and so on. R "
    "explains A.",
    ["First t½ = [R]₀/2k", "Second t½ = ([R]₀/2)/2k = [R]₀/4k = ½ × first t½"],
    answer="A",
    why="A follows directly from the proportionality stated in R.",
    ncert=f"{REF8}, half-life of a reaction", seconds=45)

add("Rate law and order", I, "multi_statement",
    ms("A reaction A + B → products follows the rate law rate = k[A][B]. Which of the following statements are "
       "correct?",
       ["The reaction is of second order overall.",
        "The unit of k is L mol⁻¹ s⁻¹ (concentration in mol L⁻¹, time in s).",
        "If B is present in large excess, the reaction behaves as a first-order reaction.",
        "Doubling the concentrations of both A and B makes the rate four times as fast.",
        "The reaction must be an elementary bimolecular reaction."]),
    multi("B", {"a": True, "b": True, "c": True, "d": True, "e": False},
          ["(a), (b) and (c) only", "(a), (c), (d) and (e) only", "(b), (d) and (e) only"]),
    "Order, units of k and pseudo first-order behaviour",
    "The overall order is 1 + 1 = 2, so k has units L mol⁻¹ s⁻¹. With B in large excess, [B] stays almost "
    "constant and rate = k′[A] (pseudo first order). Doubling both concentrations multiplies the rate by "
    "2 × 2 = 4. A rate law of this form does not prove that the reaction is elementary; order is found "
    "experimentally and a complex reaction can have the same rate law.",
    ["(a) true", "(b) true", "(c) true", "(d) true", "(e) the rate law does not establish the mechanism → false"],
    why="(e) is false, so the options containing it are wrong; (a), (b) and (c) only leaves out the true "
        "statement (d).",
    ncert=f"{REF8}, order and molecularity; pseudo first-order reactions", seconds=60)

ratio_k = 10 ** (53600 / (2.303 * R_J) * (1 / 300 - 1 / 310))
assert close(ratio_k, 2.0, 0.005) and close(40 / ratio_k, 20, 0.005)
add("Arrhenius equation and activation energy", A, "numerical",
    "A first-order reaction has an activation energy of 53.6 kJ mol⁻¹ and a half-life of 40 min at 300 K. "
    "Assuming the Arrhenius pre-exponential factor is constant, its half-life at 310 K is "
    "(R = 8.314 J K⁻¹ mol⁻¹; log 2 = 0.301):",
    Opts("D", "20 min", ["80 min", "40 min", "10 min"]),
    "Arrhenius equation combined with the first-order half-life",
    "Use log(k₂/k₁) = (E_a/2.303R)(1/T₁ − 1/T₂) to find how much k increases; since t½ = 0.693/k, the "
    "half-life falls by the same factor.",
    ["log(k₂/k₁) = 53 600/(2.303 × 8.314) × (1/300 − 1/310)", "= 2799 × 1.075 × 10⁻⁴ = 0.301 → k₂/k₁ = 2",
     "t½(310 K) = 40/2 = 20 min"],
    why="80 min multiplies instead of dividing. 40 min ignores the temperature change. 10 min treats the rate "
        "constant as increasing four times.",
    ncert=f"{REF8}, temperature dependence: Arrhenius equation; half-life of a first-order reaction",
    seconds=110, checked=True)

# 2N2O5 -> 4NO2 + O2 : -½ d[N2O5]/dt = ¼ d[NO2]/dt = d[O2]/dt
k_1 = 1.0
k_2 = 4 * (k_1 / 2)
k_3 = k_1 / 2
assert 2 * k_1 == k_2 == 4 * k_3
add("Rate law and order", A, "direct",
    "For the first-order decomposition 2N₂O₅(g) → 4NO₂(g) + O₂(g), the rates are written as "
    "−d[N₂O₅]/dt = k₁[N₂O₅], d[NO₂]/dt = k₂[N₂O₅] and d[O₂]/dt = k₃[N₂O₅]. The relation among k₁, k₂ and k₃ "
    "is:",
    Opts("C", "2k₁ = k₂ = 4k₃", ["k₁ = k₂ = k₃", "4k₁ = 2k₂ = k₃", "k₁ = 2k₂ = 4k₃"]),
    "Rates of reaction in terms of different reactants and products",
    "The rate of reaction is −½ d[N₂O₅]/dt = ¼ d[NO₂]/dt = d[O₂]/dt. Substitute each expression.",
    ["½k₁[N₂O₅] = ¼k₂[N₂O₅] = k₃[N₂O₅]", "Multiply by 4: 2k₁ = k₂ = 4k₃"],
    why="k₁ = k₂ = k₃ ignores the stoichiometric coefficients. The other two invert the factors (for example, "
        "NO₂ is formed twice as fast as N₂O₅ disappears, not half as fast).",
    ncert=f"{REF8}, rate of a chemical reaction", seconds=70)

k_fo = 0.693 / 20
assert close(k_fo, 0.03465) and close(1 - 0.5 ** 2, 0.75) and close(1 - 0.5 ** 3, 0.875) \
    and close(2.303 * 3 / k_fo, 199.4, 0.005)
add("Half-life", A, "multi_statement",
    ms("A first-order reaction has a half-life of 20 min. Which of the following statements are correct? "
       "(ln 2 = 0.693; 2.303 log 1000 = 6.909)",
       ["Its rate constant is 0.0347 min⁻¹.", "75% of the reactant reacts in 40 min.",
        "93.75% of the reactant reacts in 60 min.", "About 200 min is needed for 99.9% completion.",
        "Doubling the initial concentration doubles the half-life."]),
    multi("B", {"a": True, "b": True, "c": False, "d": True, "e": False},
          ["(a), (b) and (c) only", "(b), (d) and (e) only", "(a), (b), (c) and (d) only"]),
    "Half-life relations for a first-order reaction",
    "k = 0.693/t½ = 0.0347 min⁻¹. After n half-lives, (½)ⁿ of the reactant remains: two half-lives (40 min) "
    "leave 25%, i.e. 75% reacted; three half-lives (60 min) leave 12.5%, i.e. 87.5% reacted. For 99.9% "
    "completion, t = 6.909/k ≈ 199 min ≈ 10 half-lives. The half-life of a first-order reaction does not "
    "depend on the initial concentration.",
    ["(a) 0.693/20 = 0.0347 min⁻¹ → true", "(b) 2 half-lives → 75% → true",
     "(c) 3 half-lives → 87.5%, not 93.75% (that needs 4) → false", "(d) 6.909/0.03465 ≈ 199 min → true",
     "(e) t½ independent of [R]₀ → false"],
    why="Options with (c) or (e) are wrong; (c) counts four half-lives in 60 min, and (e) describes a "
        "zero-order reaction.",
    ncert=f"{REF8}, half-life of a reaction", seconds=100, checked=True)

add("Arrhenius equation and activation energy", A, "assertion_reason",
    ar("A catalyst increases the rate constants of the forward and the backward reactions of a reversible "
       "reaction by the same factor.",
       "A catalyst lowers the activation energies of the forward and the backward reactions by the same "
       "amount."),
    AR_, "Effect of a catalyst on a reversible reaction",
    "A catalyst provides an alternative path whose energy barrier is lower by the same amount for both "
    "directions (the energies of reactants and products are unchanged). With k = A e^(−Ea/RT), equal lowering "
    "of Ea multiplies both rate constants by the same factor, so their ratio, the equilibrium constant, is "
    "unchanged. R explains A.",
    ["Ea(f) and Ea(b) both fall by the same ΔE", "k_f and k_b both multiplied by e^(ΔE/RT) → K = k_f/k_b unchanged"],
    answer="A",
    why="R is the reason the factor is the same; this is also why a catalyst does not change K.",
    ncert=f"{REF8}, effect of catalyst", seconds=50)

# ==================================================================== 9. Classification of Elements and Periodicity
topic("Classification of Elements and Periodicity in Properties")
REF9 = f"{C11}, 'Classification of Elements and Periodicity in Properties'"

add("Modern periodic table", B, "match_list",
    lists("Match List-I (scientist) with List-II (contribution to the classification of elements).",
          ["Johann Dobereiner", "John Newlands", "Lothar Meyer", "Henry Moseley"],
          ["Plotted atomic volume against atomic weight and obtained a periodically repeating pattern",
           "Showed that the frequencies of the characteristic X-rays of the elements vary regularly with their "
           "atomic numbers",
           "Groups of three elements (triads) in which the atomic weight of the middle element is about the "
           "mean of the other two",
           "Law of octaves: every eighth element, in order of atomic weight, resembles the first"]),
    match("D", M("III IV I II"), [M("IV III I II"), M("III IV II I"), M("I IV III II")]),
    "History of the periodic table",
    "Dobereiner noted triads; Newlands proposed the law of octaves; Lothar Meyer plotted physical properties "
    "such as atomic volume against atomic weight and saw periodicity; Moseley's X-ray work showed that atomic "
    "number is the more fundamental property, leading to the modern periodic law.",
    ["A → III (triads)", "B → IV (octaves)", "C → I (atomic volume curve)", "D → II (X-ray frequencies)"],
    why="The other codes swap triads with octaves or Lothar Meyer with Moseley.",
    ncert=f"{REF9}, genesis of periodic classification", seconds=35)

add("Modern periodic table", B, "direct",
    "Mendeleev placed iodine after tellurium in his periodic table, even though iodine has the lower atomic "
    "weight. He did this because:",
    Opts("B", "iodine resembles fluorine, chlorine and bromine in its properties, so it belongs in their group",
         ["he arranged the elements strictly in order of increasing atomic number",
          "the atomic weight of tellurium had not yet been measured",
          "iodine and tellurium were both thought to be metals"]),
    "Mendeleev's periodic table: properties given priority over atomic weight",
    "Mendeleev arranged elements by atomic weight but gave greater importance to similarities in properties. "
    "Where the two conflicted, as for tellurium and iodine, he placed iodine with the halogens it resembles, "
    "ignoring the order of atomic weights.",
    ["Property similarity was given priority", "Iodine placed in the group of F, Cl and Br"],
    why="Atomic numbers were introduced only later by Moseley. Both atomic weights were known, and neither "
        "element was considered a typical metal.",
    ncert=f"{REF9}, Mendeleev's periodic law", seconds=30)

add("Valence and reactivity", B, "statement_pair",
    sp("The elements on the extreme left of a period, the alkali metals, show the strongest tendency to lose "
       "electrons, i.e. the strongest reducing behaviour in the period.",
       "Among the elements of a period other than the noble gas, the halogen on the extreme right shows the "
       "strongest tendency to gain electrons, i.e. the strongest oxidising behaviour."),
    SP_, "Periodic trends in reactivity: reducing and oxidising behaviour",
    "Across a period, ionisation enthalpy generally rises and electron gain enthalpy becomes more negative. "
    "So the element at the far left loses electrons most easily (strong reducing agent), and the halogen at "
    "the far right gains electrons most readily (strong oxidising agent). Both statements are true.",
    ["I: lowest ionisation enthalpy at the far left → strongest reducing behaviour → true",
     "II: most negative electron gain enthalpy near the far right → strongest oxidising behaviour → true"],
    answer="A",
    why="Both statements describe NCERT's account of reactivity at the two extremes of a period.",
    ncert=f"{REF9}, periodic trends in chemical properties", seconds=35)

add("Valence and reactivity", I, "assertion_reason",
    ar("Boron, the first member of group 13, forms at most four covalent bonds, as in [BF₄]⁻, whereas "
       "aluminium forms [AlF₆]³⁻.",
       "The first member of a p-block group has only four valence orbitals (2s and three 2p) available for "
       "bonding, whereas the second member can also use its 3d orbitals."),
    AR_, "Anomalous behaviour of the first member of a group",
    "NCERT uses this example: with only the 2s and 2p orbitals in its valence shell, boron (like other "
    "second-period elements) has a maximum covalency of 4. Aluminium has 3s, 3p and 3d orbitals available, "
    "so its covalency can go beyond 4, as in [AlF₆]³⁻. R explains A.",
    ["A: B max covalency 4; Al forms [AlF₆]³⁻ → true",
     "R: four valence orbitals for the first member vs nine (3s, 3p, 3d) for the second → true and explains A"],
    answer="A",
    why="R is the reason NCERT gives for the limited covalency of the first member.",
    ncert=f"{REF9}, anomalous properties of second-period elements", seconds=45)

ie1 = {"Na": 496, "Mg": 737, "Al": 577, "Si": 786}
assert sorted(ie1, key=ie1.get) == ["Na", "Al", "Mg", "Si"]
add("Ionisation and electron gain enthalpy", I, "direct",
    "Which of the following is the correct order of the first ionisation enthalpies of these third-period "
    "elements?",
    Opts("C", "Na < Al < Mg < Si", ["Na < Mg < Al < Si", "Al < Na < Mg < Si", "Si < Al < Mg < Na"]),
    "First ionisation enthalpy across the third period",
    "Ionisation enthalpy generally increases across a period, but aluminium is lower than magnesium. The "
    "electron removed from Al is a 3p electron, which is shielded by the 3s electrons and held less tightly "
    "than a 3s electron of Mg.",
    ["General increase: Na < … < Si", "Exception: Mg (3s²) > Al (3s² 3p¹)",
     "Order (kJ mol⁻¹): Na 496 < Al 577 < Mg 737 < Si 786"],
    why="Na < Mg < Al < Si ignores the Mg/Al exception. Al < Na wrongly puts aluminium below sodium. "
        "Si < … < Na reverses the general trend.",
    ncert=f"{REF9}, ionisation enthalpy", seconds=40)

positions = {"[Ar]3d10 4s2 4p5": (4, 17), "[Kr]5s1": (5, 1), "[Ar]3d5 4s2": (4, 7), "[Ar]3d6 4s2": (4, 8),
             "[Ne]3s2 3p1": (3, 13)}
assert positions["[Ar]3d6 4s2"][1] != 6 and positions["[Ne]3s2 3p1"][1] != 3
add("Modern periodic table", I, "multi_statement",
    ms("Which of the following assignments of an element, from its ground-state electronic configuration, to "
       "a period and group are correct?",
       ["[Ar] 3d¹⁰ 4s² 4p⁵ : period 4, group 17", "[Kr] 5s¹ : period 5, group 1",
        "[Ar] 3d⁵ 4s² : period 4, group 7", "[Ar] 3d⁶ 4s² : period 4, group 6",
        "[Ne] 3s² 3p¹ : period 3, group 3"]),
    multi("D", {"a": True, "b": True, "c": True, "d": False, "e": False},
          ["(a) and (b) only", "(a), (b), (c) and (e) only", "(b), (c) and (d) only"]),
    "Locating elements from their electronic configurations",
    "The period is the principal quantum number of the outermost shell. For s-block elements the group equals "
    "the number of s electrons; for d-block elements it equals (n−1)d + ns electrons; for p-block elements it "
    "is 10 + ns + np electrons.",
    ["(a) 4s² 4p⁵: 10 + 7 = group 17, period 4 → true", "(b) 5s¹: group 1, period 5 → true",
     "(c) 3d⁵ 4s²: 5 + 2 = group 7 → true", "(d) 3d⁶ 4s²: 6 + 2 = group 8, not 6 → false",
     "(e) 3s² 3p¹: 10 + 3 = group 13, not 3 → false"],
    why="(d) counts only the d electrons, and (e) forgets to add 10 for a p-block element; (a) and (b) only "
        "leaves out the true statement (c).",
    ncert=f"{REF9}, electronic configurations and types of elements: s-, p-, d- and f-blocks", seconds=75)

add("Ionisation and electron gain enthalpy", I, "statement_pair",
    sp("Among fluorine, chlorine, bromine and iodine, chlorine has the most negative electron gain enthalpy.",
       "On going down a group, the electron gain enthalpy always becomes less negative from the first member "
       "to the second member."),
    SP_, "Electron gain enthalpy down group 17",
    "Electron gain enthalpy generally becomes less negative down a group, but the first member is an "
    "exception: the added electron enters the small n = 2 shell of fluorine and suffers strong repulsion, so "
    "fluorine's value is less negative than chlorine's. Chlorine has the most negative electron gain enthalpy "
    "of the group (and of all elements). Statement I is true; Statement II is false because from F to Cl "
    "(and from O to S) the value becomes MORE negative.",
    ["I: ΔegH (kJ mol⁻¹) F −328, Cl −349, Br −325, I −295 → Cl most negative → true",
     "II: from F to Cl the value becomes more negative → false"],
    answer="C",
    why="Statement II overlooks the anomaly of the small first member of the group.",
    ncert=f"{REF9}, electron gain enthalpy", seconds=40)

add("Valence and reactivity", A, "multi_statement",
    ms("Which of the following statements about periodic trends and the anomalous behaviour of the first "
       "member of a group are correct?",
       ["Metallic character increases down group 14 from carbon to lead.",
        "The maximum covalency of nitrogen is four, whereas phosphorus can show a covalency greater than four.",
        "The anomalous behaviour of the first member of a group is attributed to its small size, large "
        "charge/radius ratio and high electronegativity.",
        "The first member of each p-block group shows the highest maximum covalency in its group.",
        "The reactivity of the halogens increases down group 17."]),
    multi("B", {"a": True, "b": True, "c": True, "d": False, "e": False},
          ["(a) and (c) only", "(a), (b), (c) and (e) only", "(b), (c) and (d) only"]),
    "Group trends and anomalous properties of second-period elements",
    "Down group 14, carbon is a non-metal, silicon and germanium are metalloids, and tin and lead are metals. "
    "Nitrogen, with only 2s and 2p orbitals, is limited to a covalency of four, while phosphorus can use 3d "
    "orbitals. NCERT attributes the anomalous behaviour of the first member to its small size, large charge/"
    "radius ratio, high electronegativity and the absence of d orbitals. So the first member has the LOWEST "
    "maximum covalency, and the reactivity (oxidising power) of the halogens decreases down the group.",
    ["(a) true", "(b) true", "(c) true", "(d) the first member is limited to 4 → false",
     "(e) halogen reactivity decreases down the group → false"],
    why="Options with (d) or (e) are wrong, and (a) and (c) only misses the true statement (b).",
    ncert=f"{REF9}, periodic trends in chemical properties; anomalous properties of second-period elements",
    seconds=90)

e_mg = 0.24 / 24 * (738 + 1451)
assert close(e_mg, 21.89) and close(0.01 * 738, 7.38) and close(0.01 * 1451, 14.51)
add("Ionisation and electron gain enthalpy", A, "numerical",
    "The first and second ionisation enthalpies of magnesium are 738 kJ mol⁻¹ and 1451 kJ mol⁻¹. The energy "
    "needed to convert 0.24 g of gaseous magnesium atoms completely into gaseous Mg²⁺ ions is (Mg = 24):",
    Opts("D", "21.9 kJ", ["7.38 kJ", "14.5 kJ", "2189 kJ"]),
    "Successive ionisation enthalpies and the mole concept",
    "Forming Mg²⁺(g) from Mg(g) needs both the first and the second ionisation enthalpies. Multiply their sum "
    "by the amount of magnesium in moles.",
    ["n(Mg) = 0.24/24 = 0.010 mol", "Energy per mole = 738 + 1451 = 2189 kJ",
     "Energy = 0.010 × 2189 = 21.9 kJ"],
    why="7.38 kJ stops at Mg⁺ (first ionisation only). 14.5 kJ uses only the second ionisation enthalpy. "
        "2189 kJ is the energy for one mole, not 0.24 g.",
    ncert=f"{REF9}, ionisation enthalpy", seconds=60, checked=True)

ie_pairs = {("Si", "P"): (786, 1012), ("Be", "B"): (899, 801), ("N", "O"): (1402, 1314), ("Mg", "Al"): (737, 577)}
assert [p for p, (a, b) in ie_pairs.items() if a < b] == [("Si", "P")]
add("Ionisation and electron gain enthalpy", A, "direct",
    "In which of the following pairs is the first ionisation enthalpy of the FIRST element lower than that of "
    "the second?",
    Opts("A", "Si and P", ["Be and B", "N and O", "Mg and Al"]),
    "Exceptions to the trend of ionisation enthalpy across a period",
    "Ionisation enthalpy normally increases across a period, but it drops from Be to B and from Mg to Al (a "
    "p electron is easier to remove than a penetrating s electron) and from N to O (the half-filled p³ "
    "configuration is extra stable; O has a paired p electron). Si (3p²) to P (3p³) follows the normal "
    "increase.",
    ["Si 786 < P 1012 kJ mol⁻¹ → first is lower ✓", "Be 899 > B 801; N 1402 > O 1314; Mg 737 > Al 577"],
    why="Be/B, N/O and Mg/Al are exactly the pairs where the first element has the HIGHER ionisation "
        "enthalpy.",
    ncert=f"{REF9}, ionisation enthalpy", seconds=50)


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
    doc = {"schema_version": "1.0", "batch_id": "BATCH_007", "created_at": TODAY,
           "notes": "Package CHE_007_p1: 120 original Chemistry questions (physical chemistry and periodicity). "
                    "Numerical answers re-derived in tools/batch_007/CHE_007_p1.py.",
           "stimuli": [], "questions": QUESTIONS}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {OUT}: {n} questions; difficulty {dict(Counter(q['difficulty'] for q in QUESTIONS))}; "
          f"formats {dict(fmts)}; keys {dict(sorted(KEYS.items()))}")
