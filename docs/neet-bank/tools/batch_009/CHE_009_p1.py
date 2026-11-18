"""Writes batches/parts/BATCH_009_CHE_p1.json: package CHE_009_p1 of BATCH_009 (Chemistry, 123 questions).

Topics: Some Basic Concepts, Atomic Structure, Chemical Bonding, Thermodynamics, Solutions, Equilibrium,
Redox and Electrochemistry, Chemical Kinetics, Classification of Elements and Periodicity. IDs NEET_CHE_002001..002123.

Every computable answer is re-derived here with an assert before anything is written; the quota per
(topic, difficulty), the ID range, the format mix and the answer-key balance are asserted too.
The position of every correct option is chosen by hand in the call that adds the question (argument `at`)
and never moved by code.

    cd docs/neet-bank && python tools/batch_009/CHE_009_p1.py
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
PACKAGE = "CHE_009_p1"
PLAN = ROOT / "batches" / "plans" / "BATCH_009_plan.json"
OUT = ROOT / "batches" / "parts" / "BATCH_009_CHE_p1.json"
TODAY = "2026-11-16"
LETTERS = "ABCD"
CHE = "Chemistry"
FIRST_ID = 2001
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
F_CONST = 96500


# ==================================================================== 1. Some Basic Concepts in Chemistry
topic("Some Basic Concepts in Chemistry")
REF1 = f"{C11}, 'Some Basic Concepts of Chemistry'"

m_nh3 = 1.204e22 / NA * 17
assert close(m_nh3, 0.34) and close(1.204e22 / NA * 14, 0.28) and close(1.204e22 / NA * 4 * 17, 1.36)
add("Mole concept", B, "numerical",
    "The mass of 1.204 × 10²² molecules of ammonia is (N = 14, H = 1, Nₐ = 6.022 × 10²³ mol⁻¹):",
    Opts("C", "0.34 g", ["0.28 g", "3.4 g", "1.36 g"]),
    "Converting a number of molecules into a mass through the mole",
    "Divide the number of molecules by the Avogadro constant to get moles, then multiply by the molar mass of NH₃.",
    ["n = 1.204 × 10²² / 6.022 × 10²³ = 0.020 mol", "M(NH₃) = 14 + 3 = 17 g mol⁻¹",
     "Mass = 0.020 × 17 = 0.34 g"],
    why="0.28 g uses the molar mass of nitrogen alone (14 g mol⁻¹). 3.4 g misplaces the power of ten (0.2 mol). "
        "1.36 g counts four atoms per molecule as if they were four molecules.",
    ncert=f"{REF1}, mole concept and molar masses", seconds=35, checked=True)

masses = {"H₂": 2, "N₂": 28, "O₂": 32, "CO₂": 44}
assert min(masses, key=masses.get) == "H₂"
add("Mole concept", B, "direct",
    "Which of the following samples contains the LARGEST number of molecules? (H = 1, C = 12, N = 14, O = 16)",
    Opts("A", "1 g of H₂", ["1 g of N₂", "1 g of O₂", "1 g of CO₂"]),
    "For equal masses, the number of molecules is inversely proportional to the molar mass",
    "Number of molecules = (mass/molar mass) × Nₐ. With the mass fixed at 1 g, the gas with the smallest molar "
    "mass (H₂, 2 g mol⁻¹) has the most moles and so the most molecules.",
    ["n = 1/M: H₂ 0.5 mol; N₂ 0.036 mol; O₂ 0.031 mol; CO₂ 0.023 mol", "Largest n → H₂"],
    why="N₂, O₂ and CO₂ have larger molar masses, so 1 g of each contains fewer moles and fewer molecules.",
    ncert=f"{REF1}, mole concept and molar masses", seconds=25)

p_mol, o_mol = 43.66 / 31, 56.34 / 16
assert close(o_mol / p_mol, 2.5)
add("Empirical and molecular formulae", I, "numerical",
    "An oxide of phosphorus contains 43.66% phosphorus and 56.34% oxygen by mass. Its empirical formula is "
    "(P = 31, O = 16):",
    Opts("D", "P₂O₅", ["PO₂", "P₂O₃", "PO₃"]),
    "Empirical formula from percentage composition",
    "Convert the mass per cent of each element into moles, divide by the smaller value, and multiply by a whole "
    "number if the ratio is not a whole-number ratio.",
    ["P: 43.66/31 = 1.408 mol; O: 56.34/16 = 3.521 mol", "O : P = 3.521/1.408 = 2.5",
     "P : O = 1 : 2.5 = 2 : 5 → P₂O₅"],
    why="PO₂ rounds 2.5 down to 2 instead of doubling the ratio. P₂O₃ is a different oxide (P : O = 1 : 1.5). "
        "PO₃ rounds 2.5 up to 3.",
    ncert=f"{REF1}, empirical formula for molecular formula", seconds=60, checked=True)

n_mg = 2.4 / 24
v_acid = n_mg / 0.25 * 1000
assert close(v_acid, 400) and close(n_mg / 2 / 0.25 * 1000, 200) and close(2 * n_mg / 0.25 * 1000, 800)
add("Stoichiometry", I, "numerical",
    "The volume of 0.25 M sulphuric acid needed to react completely with 2.4 g of magnesium, "
    "Mg(s) + H₂SO₄(aq) → MgSO₄(aq) + H₂(g), is (Mg = 24):",
    Opts("B", "400 mL", ["200 mL", "800 mL", "40 mL"]),
    "Stoichiometry with a solution: moles = molarity × volume",
    "Find the moles of Mg, use the 1 : 1 mole ratio with H₂SO₄, and divide by the molarity to get the volume.",
    ["n(Mg) = 2.4/24 = 0.10 mol", "n(H₂SO₄) = 0.10 mol (1 : 1)", "V = 0.10/0.25 = 0.40 L = 400 mL"],
    why="200 mL takes two Mg per H₂SO₄. 800 mL takes two H₂SO₄ per Mg (confusing it with HCl, which needs 2 mol "
        "per mol Mg). 40 mL is a slip of a power of ten in the litre-to-millilitre conversion.",
    ncert=f"{REF1}, stoichiometry and stoichiometric calculations", seconds=50, checked=True)

add("Empirical and molecular formulae", I, "assertion_reason",
    ar("Two different compounds can have exactly the same percentage composition by mass.",
       "Percentage composition fixes only the simplest whole-number ratio of atoms (the empirical formula), "
       "not the actual number of atoms in a molecule."),
    AR_, "Empirical formula versus molecular formula",
    "Compounds such as ethyne (C₂H₂) and benzene (C₆H₆) share the empirical formula CH and therefore the same "
    "mass per cent of each element, though their molecular formulae differ. This is possible precisely because "
    "percentage composition determines only the atom ratio, not the molecular formula. R explains A.",
    ["A: same empirical formula → same percentage composition → true",
     "R: % composition → empirical formula only → true", "R is the reason A can happen → option A"],
    answer="A",
    why="Both statements are true, and R is exactly why compounds with different molecular formulae can share a "
        "composition, so the 'not the explanation' option does not apply.",
    ncert=f"{REF1}, empirical formula for molecular formula", seconds=40)

add("Stoichiometry", I, "statement_pair",
    sp("In a balanced chemical equation, the coefficients give the ratio of the amounts (in moles) of the "
       "reactants and products.",
       "For a reaction between gases, the coefficients of a balanced equation also give the ratio of the masses "
       "of the reacting gases."),
    SP_, "What the coefficients of a balanced equation mean",
    "The coefficients are mole (and molecule) ratios; for gases at the same temperature and pressure they are "
    "also volume ratios. They are not mass ratios: in 2H₂ + O₂ → 2H₂O, 2 mol (4 g) of H₂ reacts with 1 mol "
    "(32 g) of O₂, a mass ratio of 1 : 8, not 2 : 1.",
    ["I: coefficients = mole ratio → true", "II: masses depend on molar masses; 2 : 1 by moles is 4 g : 32 g → false"],
    answer="C",
    why="Statement II confuses the mole (or volume) ratio with the mass ratio.",
    ncert=f"{REF1}, stoichiometry and stoichiometric calculations", seconds=35)

n_na2co3_total = 0.53 / 106
n_aliquot = n_na2co3_total * 20 / 100
m_hcl = 2 * n_aliquot / 0.025
assert close(m_hcl, 0.08) and close(n_aliquot / 0.025, 0.04) and close(2 * n_na2co3_total / 0.025, 0.4) \
    and close(2 * n_aliquot / 0.020, 0.10)
add("Stoichiometry", A, "numerical",
    "0.53 g of anhydrous sodium carbonate is dissolved in water and the solution is made up to 100 mL. 20.0 mL of "
    "this solution reacts completely with 25.0 mL of a hydrochloric acid solution: "
    "Na₂CO₃ + 2HCl → 2NaCl + H₂O + CO₂. The molarity of the hydrochloric acid is (Na = 23, C = 12, O = 16):",
    Opts("A", "0.080 M", ["0.040 M", "0.40 M", "0.10 M"]),
    "Stoichiometry of a titration with an aliquot of a standard solution",
    "Find the moles of Na₂CO₃ in the 20 mL portion that was titrated, double it for HCl (1 : 2), and divide by "
    "the volume of acid used.",
    ["n(Na₂CO₃) in 100 mL = 0.53/106 = 0.0050 mol", "In 20.0 mL: 0.0050 × 20/100 = 0.0010 mol",
     "n(HCl) = 2 × 0.0010 = 0.0020 mol", "M = 0.0020/0.0250 = 0.080 M"],
    why="0.040 M ignores the 1 : 2 ratio. 0.40 M uses all the Na₂CO₃ in 100 mL instead of the 20 mL portion. "
        "0.10 M divides by the 20.0 mL of carbonate solution instead of the 25.0 mL of acid.",
    ncert=f"{REF1}, reactions in solutions (molarity)", seconds=100, checked=True)

n_salt = 0.5 * 0.2
truth1 = {"a": close(n_salt * 142, 14.2), "b": close(2 * n_salt, 0.2), "c": close(3 * n_salt, 0.2),
          "d": close(2 * 0.2, 0.4), "e": close(n_salt * 32, 6.4)}
assert truth1 == {"a": True, "b": True, "c": False, "d": True, "e": False}
add("Mole concept", A, "multi_statement",
    ms("500 mL of a 0.20 M aqueous solution of sodium sulphate, Na₂SO₄, is prepared. Assuming complete "
       "dissociation, which of the following statements are correct? (Na = 23, S = 32, O = 16)",
       ["The solution contains 14.2 g of Na₂SO₄.",
        "The solution contains 0.20 mol of Na⁺ ions.",
        "The solution contains 0.20 mol of ions in all.",
        "The concentration of Na⁺ ions in the solution is 0.40 M.",
        "The mass of sulphur in the solution is 6.4 g."]),
    multi("B", truth1, ["(a), (b), (c) and (d) only", "(a) and (e) only", "(b), (d) and (e) only"]),
    "Moles of a solute and of its ions from molarity and volume",
    "n(Na₂SO₄) = 0.20 × 0.500 = 0.10 mol. Each formula unit gives 2 Na⁺ and 1 SO₄²⁻.",
    ["(a) 0.10 × 142 = 14.2 g ✓", "(b) 2 × 0.10 = 0.20 mol Na⁺ ✓", "(c) 3 × 0.10 = 0.30 mol of ions ✗",
     "(d) [Na⁺] = 2 × 0.20 = 0.40 M ✓", "(e) 0.10 × 32 = 3.2 g of S ✗"],
    why="(c) forgets that each formula unit gives three ions; (e) doubles the amount of sulphur. Every option "
        "containing (c) or (e) is wrong, and the remaining option omitting (a) is incomplete.",
    ncert=f"{REF1}, mole concept; reactions in solutions", seconds=90, checked=True)

o2 = {"A": 3 / 12 * 1 * 32, "B": 4 / 16 * 2 * 32, "C": 4 / 2 * 0.5 * 32, "D": 15 / 30 * 3.5 * 32}
assert {k: round(v) for k, v in o2.items()} == {"A": 8, "B": 16, "C": 32, "D": 56}
add("Stoichiometry", A, "match_list",
    lists("Match List-I (substance burnt completely in an excess of oxygen) with List-II (mass of O₂ consumed). "
          "(H = 1, C = 12, O = 16)",
          ["3 g of carbon (C + O₂ → CO₂)", "4 g of methane (CH₄ + 2O₂ → CO₂ + 2H₂O)",
           "4 g of hydrogen (2H₂ + O₂ → 2H₂O)", "15 g of ethane (2C₂H₆ + 7O₂ → 4CO₂ + 6H₂O)"],
          ["16 g", "32 g", "56 g", "8 g"]),
    match("D", M("IV I II III"), [M("I IV II III"), M("IV I III II"), M("IV II I III")]),
    "Mass–mole–mass stoichiometry",
    "Convert each mass to moles, use the mole ratio with O₂ from the equation, and convert O₂ to grams.",
    ["A: 0.25 mol C × 1 = 0.25 mol O₂ = 8 g → IV", "B: 0.25 mol CH₄ × 2 = 0.5 mol O₂ = 16 g → I",
     "C: 2 mol H₂ × ½ = 1 mol O₂ = 32 g → II", "D: 0.5 mol C₂H₆ × 3.5 = 1.75 mol O₂ = 56 g → III"],
    why="A-I/B-IV swaps carbon and methane; C-III/D-II forgets the factor 3.5 for ethane; B-II/C-I ignores that "
        "two H₂ need only one O₂.",
    ncert=f"{REF1}, stoichiometry and stoichiometric calculations", seconds=100, checked=True)


# ==================================================================== 2. Atomic Structure
topic("Atomic Structure")
REF2 = f"{C11}, 'Structure of Atom'"
R_H = 1.097e7
M_E = 9.11e-31

nu0 = 3.313e-19 / H_PLANCK
assert close(nu0, 5.0e14)
add("Dual nature and uncertainty", B, "numerical",
    "The work function (minimum energy needed to eject an electron) of a metal is 3.313 × 10⁻¹⁹ J. The threshold "
    "frequency of the metal is (h = 6.626 × 10⁻³⁴ J s):",
    Opts("B", "5.0 × 10¹⁴ Hz", ["5.0 × 10¹³ Hz", "2.0 × 10⁻¹⁵ Hz", "5.0 × 10¹⁵ Hz"]),
    "Threshold frequency in the photoelectric effect: W₀ = hν₀",
    "A photon can just eject an electron when its energy equals the work function, so ν₀ = W₀/h.",
    ["ν₀ = W₀/h = 3.313 × 10⁻¹⁹ / 6.626 × 10⁻³⁴", "ν₀ = 0.5 × 10¹⁵ = 5.0 × 10¹⁴ Hz"],
    why="5.0 × 10¹³ Hz and 5.0 × 10¹⁵ Hz are slips in the power of ten. 2.0 × 10⁻¹⁵ Hz inverts the ratio (h/W₀).",
    ncert=f"{REF2}, photoelectric effect", seconds=30, checked=True)

add("Electronic configuration", B, "direct",
    "The ground-state electronic configuration of gallium (Z = 31) is:",
    Opts("C", "[Ar] 3d¹⁰ 4s² 4p¹", ["[Ar] 4s² 4p¹", "[Ar] 3d⁹ 4s² 4p²", "[Ar] 3d¹⁰ 4s¹ 4p²"]),
    "Aufbau order: 4s, then 3d, then 4p",
    "After argon (18 electrons), 13 electrons remain. Following the Aufbau order they fill 4s (2), then 3d (10), "
    "and the last one enters 4p.",
    ["Z = 31 → 31 − 18 = 13 electrons beyond [Ar]", "4s² (2) + 3d¹⁰ (10) + 4p¹ (1) = 13",
     "[Ar] 3d¹⁰ 4s² 4p¹"],
    why="[Ar] 4s² 4p¹ leaves out the ten 3d electrons (it has only 21 electrons). The other two move electrons "
        "out of filled 3d or 4s orbitals into 4p, which is not the ground state.",
    ncert=f"{REF2}, electronic configuration of atoms", seconds=30)

add("Dual nature and uncertainty", B, "statement_pair",
    sp("A photon of red light has more energy than a photon of violet light.",
       "As the temperature of a black body is raised, the wavelength at which the intensity of the emitted "
       "radiation is maximum shifts to shorter wavelengths."),
    SP_, "Photon energy and black-body radiation",
    "E = hν = hc/λ. Red light has a longer wavelength (lower frequency) than violet light, so a red photon has "
    "LESS energy: Statement I is false. NCERT notes that as the temperature of a black body rises, the maximum of "
    "the intensity–wavelength curve moves to shorter wavelengths (a heated iron rod glows dull red, then orange, "
    "then white): Statement II is true.",
    ["I: λ(red) > λ(violet) → E(red) < E(violet) → false", "II: higher T → peak at shorter λ → true"],
    answer="D",
    why="Statement I reverses the relation between wavelength and photon energy; Statement II is the NCERT "
        "description of black-body radiation.",
    ncert=f"{REF2}, particle nature of electromagnetic radiation: Planck's quantum theory", seconds=35)

add("Quantum numbers and orbitals", B, "match_list",
    lists("Match List-I (quantum number) with List-II (what it describes).",
          ["Principal quantum number, n", "Azimuthal quantum number, l", "Magnetic quantum number, mₗ",
           "Spin quantum number, mₛ"],
          ["Orientation of the orbital in space", "Three-dimensional shape of the orbital (the subshell)",
           "The shell; the size and, largely, the energy of the orbital", "Orientation of the spin of the electron"]),
    match("A", M("III II I IV"), [M("II III I IV"), M("III I II IV"), M("III II IV I")]),
    "Meaning of the four quantum numbers",
    "n identifies the shell and fixes the size and (largely) the energy; l identifies the subshell and the shape; "
    "mₗ gives the orientation of the orbital; mₛ gives the orientation of the electron's spin.",
    ["A → III", "B → II", "C → I", "D → IV"],
    why="The other codes swap shell with shape, shape with orbital orientation, or orbital orientation with spin "
        "orientation.",
    ncert=f"{REF2}, quantum numbers", seconds=30)

lam_53 = 1 / (R_H * (1 / 9 - 1 / 25)) * 1e9
lam_52 = 1 / (R_H * (1 / 4 - 1 / 25)) * 1e9
lam_bad = 1 / (R_H * (1 / 3 - 1 / 5)) * 1e9
assert round(lam_53) == 1282 and round(lam_52) == 434 and round(lam_bad) == 684
add("Bohr model and hydrogen spectrum", I, "numerical",
    "The electron of a hydrogen atom falls from the n = 5 orbit to the n = 3 orbit. The wavelength of the "
    "radiation emitted, and the region of the spectrum in which it lies, are (R_H = 1.097 × 10⁷ m⁻¹; "
    "1/λ = R_H (1/n₁² − 1/n₂²)):",
    Opts("D", "1282 nm, infrared", ["1282 nm, visible", "434 nm, visible", "684 nm, visible"]),
    "Rydberg formula for the hydrogen spectrum; the Paschen series",
    "Put n₁ = 3 and n₂ = 5 in the Rydberg formula. A transition ending at n = 3 belongs to the Paschen series, "
    "whose lines lie in the infrared.",
    ["1/λ = 1.097 × 10⁷ × (1/9 − 1/25) = 1.097 × 10⁷ × 16/225 = 7.80 × 10⁵ m⁻¹",
     "λ = 1.282 × 10⁻⁶ m = 1282 nm", "Ends at n = 3 → Paschen series → infrared (beyond 700 nm)"],
    why="'1282 nm, visible' has the right wavelength but the wrong region (visible light is about 400–750 nm). "
        "434 nm is the 5 → 2 Balmer line. 684 nm uses 1/n instead of 1/n².",
    ncert=f"{REF2}, line spectrum of hydrogen", seconds=70, checked=True)

e_bond = 242e3 / NA
lam_cl = H_PLANCK * C_LIGHT / e_bond
assert round(lam_cl * 1e9) == 495 and round(2 * lam_cl * 1e9) == 989 and round(lam_cl / 2 * 1e9) == 247
add("Dual nature and uncertainty", I, "numerical",
    "The energy needed to break the Cl–Cl bond is 242 kJ mol⁻¹. The longest wavelength of light whose photons "
    "can each break one Cl₂ molecule into atoms is (h = 6.626 × 10⁻³⁴ J s, c = 3.0 × 10⁸ m s⁻¹, "
    "Nₐ = 6.022 × 10²³ mol⁻¹):",
    Opts("A", "495 nm", ["989 nm", "247 nm", "4.95 × 10⁻⁴ m"]),
    "Energy of a photon, E = hc/λ, related to the energy per molecule",
    "One photon breaks one molecule, so the photon energy must be at least the bond energy per molecule. "
    "The longest wavelength corresponds to exactly that energy.",
    ["Energy per molecule = 242 000 / 6.022 × 10²³ = 4.02 × 10⁻¹⁹ J",
     "λ = hc/E = (6.626 × 10⁻³⁴ × 3.0 × 10⁸) / 4.02 × 10⁻¹⁹ = 4.95 × 10⁻⁷ m = 495 nm"],
    why="989 nm uses half the energy (energy per Cl atom). 247 nm uses twice the energy. 4.95 × 10⁻⁴ m leaves "
        "the energy in kJ instead of converting it to J.",
    ncert=f"{REF2}, particle nature of electromagnetic radiation", seconds=70, checked=True)

add("Bohr model and hydrogen spectrum", I, "assertion_reason",
    ar("A hydrogen atom has only one electron, yet the emission spectrum of a sample of atomic hydrogen contains "
       "many lines.",
       "A sample contains a very large number of atoms, and the electrons in different atoms fall between "
       "different pairs of energy levels, each such transition giving a line of its own frequency."),
    AR_, "Origin of the many lines of the hydrogen spectrum",
    "Each line corresponds to one transition between two quantised energy levels, ν = ΔE/h. In a sample of "
    "hydrogen, excited atoms make many different transitions at the same time (for example 3 → 2, 4 → 2, 2 → 1), "
    "so the spectrum shows many lines. R explains A.",
    ["A: many lines observed → true", "R: different atoms, different transitions, each with its own ΔE → true",
     "R is why one-electron atoms give a many-line spectrum → option A"],
    answer="A",
    why="Both are true and R directly accounts for A. A is not false: the many-line spectrum is observed.",
    ncert=f"{REF2}, Bohr's model and the line spectrum of hydrogen", seconds=40)

e_tr = {"4→1": 13.6 * (1 - 1 / 16), "2→1": 13.6 * (1 - 1 / 4), "∞→2": 13.6 / 4, "6→3": 13.6 * (1 / 9 - 1 / 36)}
assert max(e_tr, key=e_tr.get) == "4→1"
add("Bohr model and hydrogen spectrum", I, "direct",
    "In a hydrogen atom, which of the following electron transitions emits the photon of the HIGHEST energy?",
    Opts("B", "n = 4 → n = 1", ["n = 2 → n = 1", "n = ∞ → n = 2", "n = 6 → n = 3"]),
    "Energy of emitted photons in the hydrogen atom, ΔE = 13.6 (1/n₁² − 1/n₂²) eV",
    "The energy levels crowd together at high n, so the largest gaps are those that end in n = 1. Of the two "
    "transitions ending at n = 1, the one starting higher (n = 4) releases more energy.",
    ["4 → 1: 13.6 × 15/16 = 12.75 eV", "2 → 1: 13.6 × 3/4 = 10.2 eV", "∞ → 2: 13.6/4 = 3.4 eV",
     "6 → 3: 13.6 × (1/9 − 1/36) = 1.13 eV"],
    why="Starting at n = ∞ does not make ∞ → 2 the largest; it ends at n = 2, so it releases only 3.4 eV. "
        "2 → 1 and 6 → 3 are smaller gaps than 4 → 1.",
    ncert=f"{REF2}, Bohr's model: energy of the electron and line spectrum", seconds=45)

add("Quantum numbers and orbitals", I, "statement_pair",
    sp("In an isolated atom, the 2pₓ, 2p_y and 2p_z orbitals differ in their orientation in space but have the "
       "same energy.",
       "The 3p orbitals are larger than the 2p orbitals and have a higher energy than them."),
    SP_, "Orientation, size and energy of p orbitals",
    "The three p orbitals of a shell are identical in size, shape and energy and differ only in orientation "
    "(they are degenerate). NCERT also states that p orbitals increase in size and energy with n: 4p > 3p > 2p. "
    "Both statements are true.",
    ["I: three p orbitals → different orientation, same energy → true", "II: size and energy 3p > 2p → true"],
    answer="A",
    why="Neither statement is false: degeneracy is within a subshell, while size and energy rise from one shell "
        "to the next.",
    ncert=f"{REF2}, shapes of atomic orbitals (p orbitals)", seconds=35)

e_ph = H_PLANCK * C_LIGHT / 150e-9
ke = e_ph - 3.61e-19


def lam_db(energy):
    return H_PLANCK / math.sqrt(2 * M_E * energy) * 1e9


assert close(lam_db(ke), 0.500) and close(lam_db(e_ph), 0.426) and close(lam_db(e_ph + 3.61e-19), 0.378) \
    and close(H_PLANCK / math.sqrt(M_E * ke) * 1e9, 0.707)
add("Dual nature and uncertainty", A, "numerical",
    "Light of wavelength 150 nm falls on a metal whose work function is 3.61 × 10⁻¹⁹ J. The de Broglie "
    "wavelength of the fastest photoelectrons emitted is (h = 6.626 × 10⁻³⁴ J s, c = 3.0 × 10⁸ m s⁻¹, mass of "
    "electron = 9.11 × 10⁻³¹ kg; for a particle, momentum p = √(2m × kinetic energy)):",
    Opts("C", "0.500 nm", ["0.426 nm", "0.707 nm", "0.378 nm"]),
    "Photoelectric equation combined with the de Broglie relation",
    "The kinetic energy of the fastest electrons is the photon energy minus the work function. Convert it into "
    "momentum and use λ = h/p.",
    ["E(photon) = hc/λ = 6.626 × 10⁻³⁴ × 3.0 × 10⁸ / 1.50 × 10⁻⁷ = 1.325 × 10⁻¹⁸ J",
     "Kinetic energy = 1.325 × 10⁻¹⁸ − 0.361 × 10⁻¹⁸ = 9.64 × 10⁻¹⁹ J",
     "p = √(2 × 9.11 × 10⁻³¹ × 9.64 × 10⁻¹⁹) = 1.325 × 10⁻²⁴ kg m s⁻¹",
     "λ = h/p = 6.626 × 10⁻³⁴ / 1.325 × 10⁻²⁴ = 5.00 × 10⁻¹⁰ m = 0.500 nm"],
    why="0.426 nm takes the whole photon energy as kinetic energy (forgets the work function). 0.378 nm adds the "
        "work function instead of subtracting it. 0.707 nm leaves out the factor 2 in p = √(2mE).",
    ncert=f"{REF2}, photoelectric effect; dual behaviour of matter", seconds=150, checked=True)

add("Bohr model and hydrogen spectrum", A, "assertion_reason",
    ar("Every line of the Lyman series of hydrogen has a shorter wavelength than every line of the Balmer series.",
       "The smallest energy released in a transition ending at n = 1 is larger than the largest energy released "
       "in a transition ending at n = 2."),
    AR_, "Comparing the Lyman and Balmer series",
    "The least energetic Lyman line (2 → 1) carries 13.6 × 3/4 = 10.2 eV; the most energetic Balmer photon "
    "(∞ → 2) carries only 13.6/4 = 3.4 eV. So every Lyman photon has more energy, and since λ = hc/E, a shorter "
    "wavelength (Lyman lines lie between about 91 and 122 nm; Balmer lines between about 365 and 656 nm). R is "
    "the reason for A.",
    ["Smallest Lyman energy: 10.2 eV; largest Balmer energy: 3.4 eV → R true",
     "Higher energy → shorter wavelength → A true", "R explains A → option A"],
    answer="A",
    why="Both are true and the energy comparison in R, through λ = hc/E, is exactly why A holds.",
    ncert=f"{REF2}, line spectrum of hydrogen", seconds=60)

cfg = {"Mn_d": 5, "Fe_shell3": 2 + 6 + 6, "Cr_s": 2 + 2 + 2 + 1, "Mn_p": 6 + 6, "Cu_3d4s": (10, 1)}
truth2 = {"a": cfg["Mn_d"] == 5, "b": cfg["Fe_shell3"] == 8, "c": cfg["Cr_s"] == 7, "d": cfg["Mn_p"] == 12,
          "e": cfg["Cu_3d4s"] == (10, 2)}
assert truth2 == {"a": True, "b": False, "c": True, "d": True, "e": False}
add("Electronic configuration", A, "multi_statement",
    ms("Which of the following statements about ground-state atoms are correct? (Z: Cr = 24, Mn = 25, Fe = 26, "
       "Cu = 29)",
       ["A manganese atom has five electrons in d orbitals.",
        "An iron atom has eight electrons in its third shell (n = 3).",
        "A chromium atom has seven electrons in s orbitals.",
        "A manganese atom has twelve electrons in p orbitals.",
        "A copper atom has ten electrons in its 3d orbitals and two in its 4s orbital."]),
    multi("D", truth2, ["(a), (b) and (d) only", "(c), (d) and (e) only", "(a) and (c) only"]),
    "Ground-state configurations, including the exceptions Cr and Cu",
    "Mn: [Ar] 3d⁵ 4s²; Fe: [Ar] 3d⁶ 4s²; Cr: [Ar] 3d⁵ 4s¹; Cu: [Ar] 3d¹⁰ 4s¹.",
    ["(a) Mn 3d⁵ → 5 d electrons ✓", "(b) Fe n = 3: 3s² 3p⁶ 3d⁶ = 14, not 8 ✗",
     "(c) Cr: 1s² 2s² 3s² 4s¹ = 7 s electrons ✓", "(d) Mn: 2p⁶ + 3p⁶ = 12 p electrons ✓",
     "(e) Cu is 3d¹⁰ 4s¹, not 3d¹⁰ 4s² ✗"],
    why="(b) forgets the 3d electrons in the third shell; (e) ignores the extra stability of the filled 3d "
        "subshell in copper. '(a) and (c) only' misses (d).",
    ncert=f"{REF2}, electronic configuration of atoms; stability of half-filled and completely filled orbitals",
    seconds=90, checked=True)

n_he = math.sqrt(423.2 * 2 / 52.9)
assert close(n_he, 4)
e_he = -13.6 * 2 ** 2 / 4 ** 2
assert close(e_he, -3.40) and close(-13.6 / 16, -0.85) and close(-13.6 * 2 / 16, -1.70) \
    and close(-13.6 * 4 / 4, -13.6)
add("Bohr model and hydrogen spectrum", A, "numerical",
    "For a hydrogen-like species, Bohr's model gives the radius of the nth orbit as rₙ = 52.9 (n²/Z) pm and the "
    "energy of the electron in it as Eₙ = −13.6 (Z²/n²) eV. The energy of the electron of a He⁺ ion (Z = 2) "
    "moving in an orbit of radius 423.2 pm is:",
    Opts("B", "−3.40 eV", ["−0.85 eV", "−1.70 eV", "−13.6 eV"]),
    "Bohr model of hydrogen-like species: find n from the radius, then the energy",
    "First find the orbit number from the radius (with Z = 2), then substitute n and Z into the energy "
    "expression.",
    ["n² = r Z / 52.9 = 423.2 × 2 / 52.9 = 16 → n = 4", "E₄ = −13.6 × 2²/4² = −13.6 × 4/16 = −3.40 eV"],
    why="−0.85 eV leaves out Z² in the energy. −1.70 eV uses Z instead of Z². −13.6 eV divides by n instead of n².",
    ncert=f"{REF2}, Bohr's model for hydrogen atom", seconds=80, checked=True)


# ==================================================================== 3. Chemical Bonding and Molecular Structure
topic("Chemical Bonding and Molecular Structure")
REF3 = f"{C11}, 'Chemical Bonding and Molecular Structure'"

add("Hybridisation and resonance", B, "statement_pair",
    sp("When two hydrogen atoms approach each other, the potential energy of the system falls to a minimum at an "
       "internuclear distance of 74 pm, which is the bond length of H₂.",
       "435.8 kJ of energy is absorbed when one mole of H₂ molecules is formed from hydrogen atoms."),
    SP_, "Valence bond picture of the formation of H₂",
    "As the atoms approach, the attraction between each nucleus and the other atom's electron outweighs the "
    "repulsions, and the energy falls to a minimum at 74 pm: Statement I is true. Because the energy falls, "
    "bond formation RELEASES energy: 435.8 kJ mol⁻¹ is given out when H₂ forms (and must be supplied to break "
    "it). Statement II is false.",
    ["I: energy minimum at 74 pm = bond length → true", "II: bond formation is exothermic (energy released) → false"],
    answer="C",
    why="Statement II reverses the sign: 435.8 kJ mol⁻¹ is the bond dissociation enthalpy, absorbed on breaking "
        "the bond, not on forming it.",
    ncert=f"{REF3}, valence bond theory: formation of the hydrogen molecule", seconds=35)

add("Fajans' rule and dipole moment", B, "direct",
    "Which of the following hydrogen halides has the LARGEST dipole moment?",
    Opts("C", "HF", ["HCl", "HBr", "HI"]),
    "Bond polarity and the electronegativity difference",
    "In a heteronuclear diatomic molecule the shared pair is displaced towards the more electronegative atom. "
    "Fluorine is the most electronegative halogen, so the H–F bond is the most polar and HF has the largest "
    "dipole moment.",
    ["Electronegativity: F > Cl > Br > I", "Largest difference from H → H–F → largest dipole moment"],
    why="HCl, HBr and HI have smaller electronegativity differences between H and the halogen, so their bonds are "
        "less polar.",
    ncert=f"{REF3}, polarity of bonds; dipole moment", seconds=25)

add("Molecular orbital theory", B, "direct",
    "Which of the following species has the same bond order as the N₂ molecule?",
    Opts("B", "NO⁺", ["O₂⁺", "N₂⁺", "O₂"]),
    "Isoelectronic species have the same bond order",
    "NO⁺ has 7 + 8 − 1 = 14 electrons, the same as N₂, and NCERT notes that isoelectronic species such as N₂, CO "
    "and NO⁺ have the same bond order, 3.",
    ["N₂: 14 electrons, bond order 3", "NO⁺: 14 electrons → bond order 3",
     "O₂⁺ 2.5; N₂⁺ 2.5; O₂ 2"],
    why="O₂⁺ and N₂⁺ both have bond order 2.5 and O₂ has bond order 2.",
    ncert=f"{REF3}, bond parameters (bond order); molecular orbital theory", seconds=30)

add("Molecular orbital theory", B, "statement_pair",
    sp("A molecular orbital can hold a maximum of four electrons.",
       "Electrons are filled into molecular orbitals in order of increasing energy, following the Pauli exclusion "
       "principle and Hund's rule, just as in atomic orbitals."),
    SP_, "Filling of molecular orbitals",
    "Like an atomic orbital, a molecular orbital holds at most two electrons of opposite spin, so Statement I is "
    "false. Molecular orbitals are filled according to the Aufbau principle, the Pauli exclusion principle and "
    "Hund's rule: Statement II is true.",
    ["I: max 2 electrons per molecular orbital → false", "II: Aufbau, Pauli and Hund apply → true"],
    answer="D",
    why="Four electrons fit into a PAIR of degenerate molecular orbitals (such as π2pₓ and π2p_y), not into one.",
    ncert=f"{REF3}, molecular orbital theory: electronic configuration of molecules", seconds=30)

add("Ionic bonding and lattice enthalpy", B, "direct",
    "In which of the following pairs do BOTH ions have the electronic configuration of argon? "
    "(Z: F = 9, Na = 11, Mg = 12, S = 16, Cl = 17, K = 19, Ca = 20)",
    Opts("B", "Ca²⁺ and S²⁻", ["Na⁺ and Cl⁻", "Mg²⁺ and Cl⁻", "K⁺ and F⁻"]),
    "Ions formed by electron transfer attain noble-gas configurations",
    "Argon has 18 electrons. Ca²⁺ has 20 − 2 = 18 and S²⁻ has 16 + 2 = 18 electrons, so both have the argon "
    "configuration.",
    ["Ca²⁺: 18 e⁻ (Ar); S²⁻: 18 e⁻ (Ar) ✓", "Na⁺ 10 (Ne), Cl⁻ 18 (Ar)", "Mg²⁺ 10 (Ne), Cl⁻ 18 (Ar)",
     "K⁺ 18 (Ar), F⁻ 10 (Ne)"],
    why="In each other pair one ion (Na⁺, Mg²⁺ or F⁻) has only 10 electrons, the configuration of neon.",
    ncert=f"{REF3}, Kössel–Lewis approach: ionic or electrovalent bond", seconds=35)

add("Hydrogen and metallic bonding", B, "assertion_reason",
    ar("The water molecule has a bent shape.",
       "In liquid water, the molecules are associated with one another through intermolecular hydrogen bonds."),
    AR_, "Shape of a molecule versus intermolecular forces",
    "The bent shape of H₂O comes from the four electron pairs on oxygen (two bond pairs and two lone pairs) "
    "arranged tetrahedrally, with the lone pairs pushing the O–H bonds closer (104.5°). Intermolecular hydrogen "
    "bonding is a different property: it acts BETWEEN molecules and does not decide the shape of a single "
    "molecule. Both statements are true, but R does not explain A.",
    ["A: 2 bond pairs + 2 lone pairs on O → bent → true", "R: O–H···O hydrogen bonds between molecules → true",
     "Shape is fixed by electron pairs on O, not by hydrogen bonding → option B"],
    answer="B",
    why="R is true but describes how molecules attract one another; an isolated water molecule in the vapour is "
        "bent too.",
    ncert=f"{REF3}, VSEPR theory; hydrogen bonding", seconds=40)

truth3 = {"a": True, "b": True, "c": True, "d": False, "e": False}
add("Hybridisation and resonance", I, "multi_statement",
    ms("Which of the following statements about the ethyne molecule, HC≡CH, are correct?",
       ["Each carbon atom is sp hybridised.",
        "The C–C σ bond is formed by the overlap of an sp hybrid orbital of each carbon atom.",
        "The two π bonds lie in mutually perpendicular planes.",
        "The H–C–C bond angle is 120°.",
        "Each carbon atom has one unhybridised 2p orbital."]),
    multi("C", truth3, ["(a), (b) and (d) only", "(a), (c) and (e) only", "(b), (c), (d) and (e) only"]),
    "sp hybridisation and the triple bond in ethyne",
    "Each carbon mixes its 2s and one 2p orbital into two sp hybrids at 180°: one overlaps the other carbon's sp "
    "orbital (C–C σ) and one overlaps the 1s orbital of H (C–H σ). The two remaining 2p orbitals of each carbon "
    "(2pₓ and 2p_y) overlap sideways to give two π bonds in perpendicular planes. The molecule is linear.",
    ["(a) ✓", "(b) ✓ sp–sp overlap", "(c) ✓", "(d) ✗ the angle is 180° (linear)",
     "(e) ✗ each carbon keeps TWO unhybridised p orbitals"],
    why="(d) is the angle for sp² carbon and (e) would allow only one π bond; any option with (d) or (e) is wrong.",
    ncert=f"{REF3}, hybridisation: formation of C₂H₂", seconds=60)

add("Molecular orbital theory", I, "direct",
    "Using the molecular orbital energy order that applies to molecules up to N₂, the electronic configuration of "
    "the valence electrons of the N₂ molecule is:",
    Opts("D", "σ2s² σ*2s² (π2pₓ² = π2p_y²) σ2p_z²",
         ["σ2s² σ*2s² σ2p_z² (π2pₓ² = π2p_y²)", "σ2s² σ*2s² (π2pₓ² = π2p_y²) (π*2pₓ¹ = π*2p_y¹)",
          "σ2s² σ2p_z² (π2pₓ² = π2p_y²) σ*2s²"]),
    "Molecular orbital configuration of N₂",
    "N₂ has 10 valence electrons. For B₂, C₂ and N₂ the π2p orbitals lie below σ2p_z, so after σ2s and σ*2s the "
    "four π electrons are placed before the last pair goes into σ2p_z.",
    ["10 valence electrons", "σ2s² σ*2s² (4) → π2pₓ² π2p_y² (8) → σ2p_z² (10)", "Bond order = (8 − 2)/2 = 3"],
    why="Placing σ2p_z below π2p is the order for O₂ and F₂. Putting electrons in π* while σ2p_z is empty breaks "
        "the Aufbau principle and would make N₂ paramagnetic. σ*2s cannot be filled after the higher-energy "
        "orbitals.",
    ncert=f"{REF3}, energy level diagram for molecular orbitals; electronic configuration of molecules",
    seconds=45)

bonds = {"C₂H₄": (5, 1), "C₂H₂": (3, 2), "HCN": (2, 2), "N₂": (1, 2)}
assert len(set(bonds.values())) == 4
add("Hybridisation and resonance", I, "match_list",
    lists("Match List-I (molecule) with List-II (numbers of σ and π bonds in one molecule).",
          ["Ethene, H₂C=CH₂", "Ethyne, HC≡CH", "Hydrogen cyanide, H–C≡N", "Nitrogen, N≡N"],
          ["1 σ and 2 π", "2 σ and 2 π", "3 σ and 2 π", "5 σ and 1 π"]),
    match("B", M("IV III II I"), [M("IV II III I"), M("III IV II I"), M("IV III I II")]),
    "Counting σ and π bonds: every single bond is σ; a double bond is 1σ + 1π; a triple bond is 1σ + 2π",
    "Count each bond once, then split multiple bonds into one σ and the rest π.",
    ["C₂H₄: 4 C–H + 1 C=C → 5 σ, 1 π → IV", "C₂H₂: 2 C–H + 1 C≡C → 3 σ, 2 π → III",
     "HCN: 1 C–H + 1 C≡N → 2 σ, 2 π → II", "N₂: N≡N → 1 σ, 2 π → I"],
    why="The other codes swap ethyne with HCN, or ethene with ethyne, or HCN with N₂, each of which miscounts "
        "the C–H σ bonds.",
    ncert=f"{REF3}, types of overlapping and nature of covalent bonds (σ and π bonds)", seconds=50)

add("Hybridisation and resonance", I, "direct",
    "In which of the following pairs are the central atoms hybridised DIFFERENTLY?",
    Opts("C", "PCl₅ and SF₆", ["CH₄ and NH₄⁺", "BF₃ and NO₃⁻", "BeCl₂ and CO₂"]),
    "Hybridisation from the number of electron pairs (σ bonds + lone pairs) around the central atom",
    "Count the σ bond pairs and lone pairs on the central atom: 2 → sp, 3 → sp², 4 → sp³, 5 → sp³d, 6 → sp³d².",
    ["CH₄, NH₄⁺: 4 pairs → sp³, sp³", "BF₃, NO₃⁻: 3 σ pairs, no lone pair → sp², sp²",
     "BeCl₂, CO₂: 2 σ pairs → sp, sp", "PCl₅: 5 pairs → sp³d; SF₆: 6 pairs → sp³d² → different"],
    why="Each of the other pairs has the same number of σ pairs plus lone pairs on the central atom, and so the "
        "same hybridisation.",
    ncert=f"{REF3}, hybridisation (including s, p and d orbitals)", seconds=45)

add("Hybridisation and resonance", I, "assertion_reason",
    ar("The CO₂ molecule is linear.",
       "The carbon atom in CO₂ is sp² hybridised."),
    AR_, "Hybridisation of carbon in CO₂",
    "Carbon in CO₂ forms two σ bonds (one to each O) and has no lone pair, so it is sp hybridised and the "
    "molecule is linear (O=C=O, 180°). A is true. R is false: an sp² carbon would give a 120° arrangement.",
    ["A: O=C=O, 180° → true", "R: 2 σ pairs, no lone pair → sp, not sp² → false"],
    answer="C",
    why="R is false, so options A and B are out; A is true, so option D is out.",
    ncert=f"{REF3}, hybridisation; VSEPR shapes", seconds=35)

add("VSEPR shapes", I, "statement_pair",
    sp("Like CO₂, the SO₂ molecule is linear.",
       "The BrF₃ molecule is T-shaped."),
    SP_, "Shapes predicted by VSEPR theory",
    "In SO₂ the sulphur atom has two bonding domains and one lone pair; the lone pair bends the molecule (it is "
    "polar), so Statement I is false. In BrF₃, bromine (7 valence electrons) forms three bonds and keeps two lone "
    "pairs; the five pairs are arranged trigonal bipyramidally with both lone pairs equatorial, giving a "
    "T-shaped molecule: Statement II is true.",
    ["I: SO₂ is AB₂E → bent → false", "II: BrF₃ is AB₃E₂ → T-shaped → true"],
    answer="D",
    why="Statement I ignores the lone pair on sulphur, which CO₂'s carbon does not have.",
    ncert=f"{REF3}, VSEPR theory: shapes of molecules with lone pairs", seconds=40)

add("Ionic bonding and lattice enthalpy", I, "statement_pair",
    sp("In Kössel's approach, an electron is transferred from one atom to another to form positive and negative "
       "ions, and the bond formed by the electrostatic attraction between these ions is called an electrovalent "
       "bond.",
       "Lewis pictured an atom as a positively charged 'kernel' (the nucleus together with the inner electrons) "
       "surrounded by the outer shell, which can hold up to eight electrons."),
    SP_, "The Kössel–Lewis approach to chemical bonding",
    "Both statements are as given in NCERT. Kössel described ionic (electrovalent) bonding by electron transfer "
    "and electrostatic attraction. Lewis described the atom as a kernel plus an outer shell of at most eight "
    "electrons, and represented the valence electrons by dots in Lewis symbols.",
    ["I: Kössel → electron transfer → electrovalent bond → true", "II: Lewis → kernel + outer shell (octet) → true"],
    answer="A",
    why="Neither statement is false; they describe the two halves of the Kössel–Lewis approach.",
    ncert=f"{REF3}, Kössel–Lewis approach to chemical bonding", seconds=35)

add("VSEPR shapes", I, "direct",
    "Which of the following species has the same shape as the NH₃ molecule?",
    Opts("B", "SO₃²⁻", ["SO₃", "NO₃⁻", "BF₃"]),
    "VSEPR: three bond pairs and one lone pair give a trigonal pyramid",
    "NH₃ is AB₃E (trigonal pyramidal). In SO₃²⁻, sulphur has 6 + 2 = 8 electrons to place; three go into bonds "
    "with the three O atoms (counted as three bonding domains, any multiple bond counting as one) and one pair "
    "remains, so SO₃²⁻ is also AB₃E, trigonal pyramidal.",
    ["NH₃: 3 bp + 1 lp → trigonal pyramidal", "SO₃²⁻: 3 bonding domains + 1 lp → trigonal pyramidal",
     "SO₃, NO₃⁻, BF₃: 3 bonding domains, no lone pair → trigonal planar"],
    why="SO₃, NO₃⁻ and BF₃ have no lone pair on the central atom and are trigonal planar.",
    ncert=f"{REF3}, VSEPR theory", seconds=50)

truth3a = {"a": True, "b": True, "c": True, "d": False, "e": False}
add("VSEPR shapes", A, "multi_statement",
    ms("In which of the following molecules is at least one bond angle around the central atom exactly 90°?",
       ["SF₆", "XeF₄", "PCl₅", "XeF₂", "BF₃"]),
    multi("B", truth3a, ["(a), (b), (c) and (d) only", "(a) and (b) only", "(b), (c) and (e) only"]),
    "Bond angles in octahedral, square planar, trigonal bipyramidal and linear molecules",
    "SF₆ (octahedral) has 90° angles between adjacent bonds. XeF₄ (square planar) has 90° between adjacent "
    "Xe–F bonds. PCl₅ (trigonal bipyramidal) has 90° between each axial and each equatorial bond. XeF₂ is "
    "linear: its only F–Xe–F angle is 180° (the 90° angles involve lone pairs, not bonds). BF₃ has only 120°.",
    ["(a) SF₆: 90°, 180° ✓", "(b) XeF₄: 90°, 180° ✓", "(c) PCl₅: 90°, 120°, 180° ✓",
     "(d) XeF₂: 180° only ✗", "(e) BF₃: 120° only ✗"],
    why="The trap is XeF₂: its electron-pair geometry is trigonal bipyramidal, but with only two bonds, both "
        "axial, the bond angle is 180°. '(a) and (b) only' misses the axial–equatorial 90° angles of PCl₅.",
    ncert=f"{REF3}, VSEPR theory: shapes of molecules", seconds=70)

add("Molecular orbital theory", A, "assertion_reason",
    ar("The Li₂ molecule has a bond order of one.",
       "In Li₂, the four 1s electrons fill σ1s and σ*1s, whose effects cancel, and the two 2s electrons occupy the "
       "bonding σ2s orbital."),
    AR_, "Bond order from the molecular orbital configuration",
    "Li₂ has 6 electrons: σ1s² σ*1s² σ2s². Bonding electrons Nb = 4, antibonding Na = 2, so bond order = "
    "(4 − 2)/2 = 1. The configuration in R is exactly what gives this bond order.",
    ["Configuration: σ1s² σ*1s² σ2s²", "Bond order = (4 − 2)/2 = 1 → A true",
     "R states this configuration → true and explains A"],
    answer="A",
    why="Both are true, and the bond order is calculated directly from the configuration stated in R.",
    ncert=f"{REF3}, bonding in some homonuclear diatomic molecules", seconds=50)

anti = {"N₂": 2 + 2, "O₂": 2 + 2 + 2, "F₂": 2 + 2 + 4, "Ne₂": 2 + 2 + 4 + 2}
assert anti == {"N₂": 4, "O₂": 6, "F₂": 8, "Ne₂": 10}
add("Molecular orbital theory", A, "match_list",
    lists("Match List-I (species) with List-II (total number of electrons, including the 1s electrons, in "
          "antibonding molecular orbitals).",
          ["N₂", "O₂", "F₂", "Ne₂"], ["8", "10", "4", "6"]),
    match("C", M("III IV I II"), [M("III IV II I"), M("IV III I II"), M("I IV III II")]),
    "Counting antibonding electrons in homonuclear diatomic molecules",
    "Write each configuration including σ1s and σ*1s. Antibonding orbitals: σ*1s, σ*2s, π*2p and σ*2p.",
    ["N₂ (14 e): σ*1s² σ*2s² → 4 → III", "O₂ (16 e): σ*1s² σ*2s² π*2p² → 6 → IV",
     "F₂ (18 e): σ*1s² σ*2s² π*2p⁴ → 8 → I", "Ne₂ (20 e): σ*1s² σ*2s² π*2p⁴ σ*2p² → 10 → II"],
    why="The wrong codes swap neighbouring species; each of these molecules has 10 bonding electrons, so the "
        "antibonding count rises by 2 from N₂ to O₂ to F₂ to Ne₂ (bond orders 3, 2, 1, 0).",
    ncert=f"{REF3}, molecular orbital theory: bond order", seconds=70, checked=True)

add("Hybridisation and resonance", A, "statement_pair",
    sp("In the nitrate ion, NO₃⁻, all three N–O bonds are of equal length.",
       "Each N–O bond in the nitrate ion has a bond order of 1.5."),
    SP_, "Resonance in the nitrate ion",
    "NO₃⁻ is a resonance hybrid of three equivalent structures, each with one N=O and two N–O bonds, so the "
    "three bonds are identical: Statement I is true. The four bonds (one double + two single) are shared over "
    "three positions, so each has bond order 4/3 ≈ 1.33, not 1.5: Statement II is false.",
    ["I: three equivalent canonical structures → equal bonds → true",
     "II: bond order = (2 + 1 + 1)/3 = 1.33, not 1.5 → false"],
    answer="C",
    why="1.5 is the bond order for a hybrid of TWO equivalent structures (as in O₃), not three.",
    ncert=f"{REF3}, resonance structures", seconds=50)

add("Hybridisation and resonance", A, "assertion_reason",
    ar("The sulphur atom in SF₄ is sp³ hybridised.",
       "The sulphur atom in SF₄ has four bond pairs and one lone pair of electrons."),
    AR_, "Hybridisation from the number of electron pairs",
    "Five electron pairs (four bond pairs + one lone pair) around sulphur need five hybrid orbitals: S is sp³d "
    "hybridised, giving a trigonal bipyramidal arrangement and a see-saw molecule. A is false; R is true.",
    ["R: S (6 valence e⁻) uses 4 in bonds, keeps 1 lone pair → true",
     "5 pairs → sp³d, not sp³ → A false"],
    answer="D",
    why="sp³ hybridisation would accommodate only four electron pairs, so A cannot be true while R is.",
    ncert=f"{REF3}, hybridisation of elements involving d orbitals", seconds=40)

truth3b = {"a": True, "b": False, "c": True, "d": False, "e": True}
add("Fajans' rule and dipole moment", A, "multi_statement",
    ms("Which of the following molecules have a NON-ZERO dipole moment?",
       ["CHCl₃", "BCl₃", "SO₂", "XeF₂", "BrF₃"]),
    multi("D", truth3b, ["(a), (b) and (c) only", "(c), (d) and (e) only", "(a) and (c) only"]),
    "Dipole moment from molecular shape",
    "A molecule is non-polar only when its bond dipoles (and lone-pair effects) cancel by symmetry.",
    ["(a) CHCl₃: tetrahedral but with unlike substituents → bond dipoles do not cancel ✓",
     "(b) BCl₃: trigonal planar, three identical bonds → 0 ✗", "(c) SO₂: bent → polar ✓",
     "(d) XeF₂: linear, two opposite Xe–F dipoles cancel → 0 ✗", "(e) BrF₃: T-shaped → polar ✓"],
    why="BCl₃ and XeF₂ are symmetric and have zero dipole moment even though their bonds are polar; "
        "'(a) and (c) only' misses BrF₃.",
    ncert=f"{REF3}, polarity of bonds; dipole moment", seconds=60)


# ==================================================================== 4. Chemical Thermodynamics
topic("Chemical Thermodynamics")
REF4 = f"{C11}, 'Thermodynamics'"

dg = 97.9 - 2 * 51.3
assert close(dg, -4.7) and close(97.9 - 51.3, 46.6) and close(97.9 + 2 * 51.3, 200.5)
add("Gibbs energy and K", B, "numerical",
    "The standard Gibbs energies of formation at 298 K are ΔfG°(NO₂, g) = 51.3 kJ mol⁻¹ and "
    "ΔfG°(N₂O₄, g) = 97.9 kJ mol⁻¹. The standard Gibbs energy change for 2NO₂(g) → N₂O₄(g) at 298 K is:",
    Opts("D", "−4.7 kJ mol⁻¹", ["+46.6 kJ mol⁻¹", "+4.7 kJ mol⁻¹", "+200.5 kJ mol⁻¹"]),
    "ΔrG° from standard Gibbs energies of formation",
    "Like enthalpy, Gibbs energy is a state function: ΔrG° = Σ ΔfG°(products) − Σ ΔfG°(reactants), each "
    "multiplied by its coefficient.",
    ["ΔrG° = ΔfG°(N₂O₄) − 2 ΔfG°(NO₂)", "= 97.9 − 2 × 51.3 = 97.9 − 102.6 = −4.7 kJ mol⁻¹"],
    why="+46.6 kJ mol⁻¹ forgets the coefficient 2 of NO₂. +4.7 kJ mol⁻¹ subtracts products from reactants. "
        "+200.5 kJ mol⁻¹ adds the terms instead of subtracting.",
    ncert=f"{REF4}, Gibbs energy change and equilibrium", seconds=35, checked=True)

add("First law, work and enthalpy", B, "direct",
    "For a system enclosed by adiabatic walls, the change in internal energy, ΔU, in a process is equal to:",
    Opts("A", "the work done on the system", ["the heat absorbed by the system", "zero, in every process",
                                              "the enthalpy change of the system"]),
    "First law of thermodynamics for an adiabatic process",
    "ΔU = q + w. Adiabatic walls allow no heat exchange (q = 0), so ΔU = w_ad, the work done on the system.",
    ["ΔU = q + w", "Adiabatic → q = 0", "ΔU = w_ad"],
    why="The heat absorbed is zero in an adiabatic process, so ΔU cannot equal it. ΔU is zero only if no work is "
        "done either. ΔH equals the heat absorbed at constant pressure, not ΔU in an adiabatic change.",
    ncert=f"{REF4}, internal energy as a state function: work", seconds=25)

add("Entropy and Gibbs energy", B, "statement_pair",
    sp("The Gibbs energy change, ΔG, of a process at constant temperature and pressure is the net energy "
       "available to do useful work.",
       "For a spontaneous process at constant temperature and pressure, ΔG is positive."),
    SP_, "Meaning of Gibbs energy and the criterion of spontaneity",
    "NCERT describes ΔG as the net energy available to do useful work (Statement I true). A process at constant "
    "T and p is spontaneous when ΔG is NEGATIVE; a positive ΔG means the process is non-spontaneous "
    "(Statement II false).",
    ["I: ΔG = net energy available for useful work → true", "II: spontaneous ↔ ΔG < 0 → false"],
    answer="C",
    why="Statement II reverses the sign of the criterion.",
    ncert=f"{REF4}, Gibbs energy and spontaneity", seconds=30)

du = 120 + 80
assert du == 200 and 120 - 80 == 40
add("First law, work and enthalpy", B, "numerical",
    "A system absorbs 120 J of heat from its surroundings, and at the same time the surroundings do 80 J of work "
    "on it. The change in the internal energy of the system is:",
    Opts("C", "+200 J", ["+40 J", "−40 J", "−200 J"]),
    "First law of thermodynamics, ΔU = q + w (IUPAC sign convention)",
    "Heat absorbed by the system and work done on the system both increase its internal energy, so both are "
    "positive.",
    ["q = +120 J (absorbed)", "w = +80 J (done on the system)", "ΔU = 120 + 80 = +200 J"],
    why="+40 J takes the work done on the system as negative. −40 J and −200 J also use wrong signs for q or w.",
    ncert=f"{REF4}, first law of thermodynamics", seconds=25, checked=True)

dh_hyd = -1300 + 2 * (-286) - (-1560)
assert dh_hyd == -312 and (-1300 - 286 + 1560) == -26
add("Hess's law and enthalpies", I, "numerical",
    "The standard enthalpies of combustion (kJ mol⁻¹) of ethyne C₂H₂(g), hydrogen H₂(g) and ethane C₂H₆(g) are "
    "−1300, −286 and −1560 respectively (water formed as liquid). The standard enthalpy change of the reaction "
    "C₂H₂(g) + 2H₂(g) → C₂H₆(g) is:",
    Opts("A", "−312 kJ mol⁻¹", ["+312 kJ mol⁻¹", "−26 kJ mol⁻¹", "−3146 kJ mol⁻¹"]),
    "Hess's law with enthalpies of combustion",
    "Burn the reactants and 'un-burn' the product: ΔrH = Σ ΔcH(reactants) − Σ ΔcH(products), with every "
    "combustion giving the same CO₂ and H₂O on both sides.",
    ["ΔrH = [ΔcH(C₂H₂) + 2 ΔcH(H₂)] − ΔcH(C₂H₆)", "= [−1300 + 2(−286)] − (−1560)",
     "= −1872 + 1560 = −312 kJ mol⁻¹"],
    why="+312 kJ mol⁻¹ subtracts the reactant terms from the product term (the rule for enthalpies of "
        "formation). −26 kJ mol⁻¹ forgets the coefficient 2 of H₂. −3146 kJ mol⁻¹ adds all three values.",
    ncert=f"{REF4}, Hess's law of constant heat summation; enthalpy of combustion", seconds=70, checked=True)

rt = R_J * 373 / 1000
du_vap = 40.7 - rt
assert close(du_vap, 37.6) and close(40.7 + rt, 43.8) and close(40.7 - R_J * 100 / 1000, 39.87)
add("First law, work and enthalpy", I, "numerical",
    "The enthalpy of vaporisation of water at 373 K and 1 bar is 40.7 kJ mol⁻¹. Treating the vapour as an "
    "ideal gas and neglecting the volume of the liquid, the change in internal energy when 1 mol of water "
    "vaporises at 373 K is (R = 8.314 J K⁻¹ mol⁻¹):",
    Opts("B", "37.6 kJ mol⁻¹", ["43.8 kJ mol⁻¹", "40.7 kJ mol⁻¹", "39.9 kJ mol⁻¹"]),
    "Relation between ΔH and ΔU: ΔH = ΔU + Δn_g RT",
    "Vaporisation creates 1 mol of gas from a liquid (Δn_g = +1). Part of the enthalpy supplied goes into "
    "pushing back the atmosphere (pΔV = RT), so ΔU is smaller than ΔH by RT.",
    ["Δn_g = 1 − 0 = 1", "RT = 8.314 × 373 = 3101 J = 3.10 kJ", "ΔU = ΔH − Δn_g RT = 40.7 − 3.10 = 37.6 kJ mol⁻¹"],
    why="43.8 kJ mol⁻¹ adds RT instead of subtracting it. 40.7 kJ mol⁻¹ ignores the expansion work. 39.9 kJ "
        "mol⁻¹ uses the temperature in °C (100) instead of kelvin.",
    ncert=f"{REF4}, enthalpy: relation between ΔH and ΔU", seconds=60, checked=True)

add("Hess's law and enthalpies", I, "assertion_reason",
    ar("The standard enthalpy of formation of O₂(g) at 298 K is zero.",
       "The O₂ molecule is paramagnetic."),
    AR_, "Standard enthalpy of formation of an element in its reference state",
    "By convention, ΔfH° of an element in its reference (most stable) state at 1 bar is zero; at 298 K oxygen's "
    "reference state is O₂(g), so A is true. R is also true (O₂ has two unpaired electrons), but it is a "
    "magnetic property that has nothing to do with the enthalpy convention.",
    ["A: element in its reference state → ΔfH° = 0 → true", "R: two unpaired electrons in π* orbitals → true",
     "R does not explain A → option B"],
    answer="B",
    why="ΔfH° of O₂(g) would be zero even if O₂ were diamagnetic, because it is the reference state of oxygen.",
    ncert=f"{REF4}, standard enthalpy of formation", seconds=35)

add("Entropy and Gibbs energy", I, "statement_pair",
    sp("The entropy of a substance decreases when it is heated.",
       "For a reversible change at temperature T, the entropy change of a system is ΔS = q_rev/T, where q_rev is "
       "the heat absorbed reversibly."),
    SP_, "Entropy and temperature",
    "Heating increases the random motion of the particles, so entropy increases with temperature: Statement I "
    "is false. The definition ΔS = q_rev/T is as given in NCERT: Statement II is true.",
    ["I: higher T → more randomness → higher entropy → false", "II: ΔS = q_rev/T → true"],
    answer="D",
    why="Statement I reverses the effect of temperature on entropy.",
    ncert=f"{REF4}, entropy and spontaneity", seconds=30)

add("Hess's law and enthalpies", I, "match_list",
    lists("Match List-I (process) with List-II (name of its enthalpy change).",
          ["Na(g) → Na⁺(g) + e⁻", "Cl(g) + e⁻ → Cl⁻(g)", "NaCl(s) → Na⁺(g) + Cl⁻(g)", "Cl₂(g) → 2Cl(g)"],
          ["Lattice enthalpy", "Bond dissociation enthalpy", "Ionisation enthalpy", "Electron gain enthalpy"]),
    match("D", M("III IV I II"), [M("IV III I II"), M("III IV II I"), M("I IV III II")]),
    "Enthalpy changes used in a Born–Haber cycle",
    "Removing an electron from a gaseous atom is ionisation; adding one to a gaseous atom is electron gain; "
    "separating one mole of an ionic solid into gaseous ions is the lattice enthalpy; breaking the bond of a "
    "gaseous diatomic molecule into atoms is bond dissociation.",
    ["A → III", "B → IV", "C → I", "D → II"],
    why="The wrong codes swap ionisation with electron gain, lattice with bond dissociation, or ionisation with "
        "lattice enthalpy.",
    ncert=f"{REF4}, enthalpies for different types of reactions: lattice enthalpy (Born–Haber cycle)",
    seconds=35)

ds_sys = 40700 / 373
ds_surr = -40700 / 383
ds_tot = ds_sys + ds_surr
assert close(ds_tot, 2.85, 0.01) and close(ds_sys - ds_surr, 215.4, 0.01)
add("Entropy and Gibbs energy", A, "numerical",
    "Water boils at 373 K at 1 bar, and its enthalpy of vaporisation is 40.7 kJ mol⁻¹. Assuming ΔvapH and "
    "ΔvapS do not change with temperature, the TOTAL entropy change (system + surroundings) when 1 mol of "
    "liquid water vaporises at 383 K and 1 bar, and the nature of the process, are:",
    Opts("C", "+2.85 J K⁻¹; spontaneous", ["−2.85 J K⁻¹; non-spontaneous", "0; at equilibrium",
                                          "+215 J K⁻¹; spontaneous"]),
    "Total entropy change as the criterion of spontaneity",
    "At the boiling point ΔG = 0, so ΔvapS = ΔvapH/T_b. At 383 K the surroundings supply 40.7 kJ of heat, so "
    "their entropy falls by ΔH/383. The sum decides spontaneity.",
    ["ΔS(system) = 40 700/373 = +109.1 J K⁻¹", "ΔS(surroundings) = −40 700/383 = −106.3 J K⁻¹",
     "ΔS(total) = 109.1 − 106.3 = +2.85 J K⁻¹ > 0 → spontaneous (water boils above 373 K)"],
    why="−2.85 J K⁻¹ swaps the two temperatures. 'At equilibrium' applies only at 373 K. +215 J K⁻¹ adds the "
        "magnitudes, forgetting that the surroundings lose heat.",
    ncert=f"{REF4}, entropy and spontaneity; Gibbs energy", seconds=120, checked=True)

be_co = (717 + 498 + 393.5) / 2
assert close(be_co, 804.25) and close(2 * be_co, 1608.5) and close((717 + 498 - 393.5) / 2, 410.75) \
    and close((498 + 393.5) / 2, 445.75)
add("Hess's law and enthalpies", A, "numerical",
    "Use the data (kJ mol⁻¹): ΔfH°(CO₂, g) = −393.5; enthalpy of atomisation of graphite, C(graphite) → C(g), "
    "= 717; bond dissociation enthalpy of O₂ = 498. The mean C=O bond enthalpy in CO₂ is about:",
    Opts("A", "804 kJ mol⁻¹", ["1608 kJ mol⁻¹", "411 kJ mol⁻¹", "446 kJ mol⁻¹"]),
    "Bond enthalpy from a Hess's-law cycle",
    "Form CO₂ from the elements by a two-route cycle: (i) directly, ΔfH°; (ii) atomise graphite and break O₂ "
    "into atoms, then form two C=O bonds. The two routes must have the same enthalpy change.",
    ["ΔfH° = ΔaH(C) + D(O=O) − 2 × D(C=O)", "−393.5 = 717 + 498 − 2 D(C=O)",
     "2 D(C=O) = 1608.5 → D(C=O) = 804 kJ mol⁻¹"],
    why="1608 kJ mol⁻¹ is the energy of both C=O bonds together. 411 kJ mol⁻¹ uses +393.5 for ΔfH°. "
        "446 kJ mol⁻¹ leaves out the atomisation of graphite.",
    ncert=f"{REF4}, bond enthalpy; Hess's law", seconds=100, checked=True)

add("Gibbs energy and K", A, "statement_pair",
    sp("For a reaction with negative ΔH° and negative ΔS° (both independent of temperature), the equilibrium "
       "constant decreases as the temperature is raised.",
       "Raising the temperature increases the equilibrium constant of every reaction."),
    SP_, "Effect of temperature on K through ΔG° = ΔH° − TΔS° and ΔG° = −RT ln K",
    "With ΔH° < 0 and ΔS° < 0, the term −TΔS° is positive and grows with T, so ΔG° becomes less negative (or "
    "positive) as T rises, and K = e^(−ΔG°/RT) falls: Statement I is true. For an endothermic reaction K rises "
    "with temperature, but for an exothermic one it falls, so Statement II is false.",
    ["I: ΔG° = ΔH° − TΔS° rises with T when ΔS° < 0 → K falls → true",
     "II: K rises with T only when ΔH° > 0 → false"],
    answer="C",
    why="Statement II ignores the sign of ΔH°; Statement I describes an exothermic reaction correctly.",
    ncert=f"{REF4}, Gibbs energy change and equilibrium", seconds=60)

add("Entropy and Gibbs energy", A, "assertion_reason",
    ar("When an ideal gas is compressed isothermally and reversibly, its entropy decreases.",
       "During this compression heat flows out of the gas (q_rev is negative), and the entropy change of the gas "
       "is ΔS = q_rev/T."),
    AR_, "Sign of the entropy change from the heat exchanged reversibly",
    "In an isothermal change of an ideal gas ΔU = 0, so q = −w. During compression work is done on the gas "
    "(w > 0), hence q_rev < 0: heat leaves the gas. With ΔS = q_rev/T, the entropy change is negative. R gives "
    "exactly this reasoning.",
    ["Isothermal ideal gas: ΔU = 0 → q_rev = −w", "Compression: w > 0 → q_rev < 0",
     "ΔS = q_rev/T < 0 → A true, R true and explains A"],
    answer="A",
    why="Both statements are true and R is the direct cause: a negative q_rev at constant T means a negative ΔS.",
    ncert=f"{REF4}, entropy and spontaneity; isothermal work of an ideal gas", seconds=60)


# ==================================================================== 5. Solutions
topic("Solutions")
REF5 = f"{C12}, 'Solutions'"

assert close(0.9 / 100 * 500, 4.5)
add("Concentration terms", B, "numerical",
    "A saline solution used in medicine is 0.9% (mass by volume) sodium chloride. The mass of NaCl present in "
    "500 mL of this solution is:",
    Opts("B", "4.5 g", ["0.18 g", "45 g", "9.0 g"]),
    "Mass by volume percentage (w/V)",
    "0.9% (w/V) means 0.9 g of solute in every 100 mL of solution.",
    ["0.9 g per 100 mL", "500 mL → 0.9 × 500/100 = 4.5 g"],
    why="0.18 g divides 0.9 by 5 instead of multiplying. 45 g reads 0.9% as 9 g per 100 mL. 9.0 g treats the "
        "percentage as grams per 50 mL.",
    ncert=f"{REF5}, expressing concentration of solutions: mass by volume percentage", seconds=25, checked=True)

ratio_tf = (1 / 60) / (1 / 180)
assert close(ratio_tf, 3)
add("Colligative properties", B, "numerical",
    "Equal masses of urea (molar mass 60 g mol⁻¹) and glucose (molar mass 180 g mol⁻¹) are dissolved "
    "separately in equal masses of water. The ratio of the depression of freezing point of the urea solution "
    "to that of the glucose solution is:",
    Opts("C", "3 : 1", ["1 : 3", "1 : 1", "9 : 1"]),
    "Depression of freezing point is proportional to molality, ΔTf = K_f m",
    "For the same mass of solute and solvent, molality is inversely proportional to the molar mass of the "
    "solute; both are non-electrolytes, so the ratio of ΔTf is the ratio of molalities.",
    ["m ∝ 1/M", "ΔTf(urea)/ΔTf(glucose) = M(glucose)/M(urea) = 180/60 = 3"],
    why="1 : 3 inverts the ratio. 1 : 1 assumes equal masses give equal effects, ignoring that colligative "
        "properties depend on the number of particles. 9 : 1 squares the ratio.",
    ncert=f"{REF5}, depression of freezing point", seconds=30, checked=True)

add("Colligative properties", B, "assertion_reason",
    ar("Salting of meat helps to preserve it from bacterial decay.",
       "A bacterium on salted meat loses water through osmosis, shrivels and dies."),
    AR_, "Osmosis in everyday life",
    "NCERT explains that preservation of meat by salting (and of fruits by adding sugar) protects them against "
    "bacterial action: a bacterium on salted meat or candied fruit loses water by osmosis to the concentrated "
    "surroundings, shrivels and dies. R is the reason for A.",
    ["A: salted meat resists bacterial decay → true",
     "R: water moves out of the bacterium into the more concentrated salt → it dies → true and explains A"],
    answer="A",
    why="Both statements are true, and the osmotic loss of water from bacteria is exactly why salting preserves "
        "meat.",
    ncert=f"{REF5}, osmosis and osmotic pressure", seconds=30)

add("Concentration terms", B, "match_list",
    lists("Match List-I (concentration term) with List-II (its definition).",
          ["Mass percentage (w/w)", "Volume percentage (V/V)", "Mass by volume percentage (w/V)", "Molality"],
          ["(Volume of the component ÷ total volume of the solution) × 100",
           "(Mass of the component ÷ total mass of the solution) × 100",
           "Moles of solute ÷ mass of solvent in kilograms",
           "(Mass of solute in grams ÷ volume of the solution in mL) × 100"]),
    match("D", M("II I IV III"), [M("I II IV III"), M("II I III IV"), M("IV I II III")]),
    "Ways of expressing the concentration of a solution",
    "w/w compares masses; V/V compares volumes; w/V gives grams of solute per 100 mL of solution; molality is "
    "moles of solute per kilogram of solvent.",
    ["A → II", "B → I", "C → IV", "D → III"],
    why="The wrong codes interchange the mass and volume percentages, or w/V with molality, or w/V with w/w.",
    ncert=f"{REF5}, expressing concentration of solutions", seconds=30)

pi_k2so4 = 3 * 0.1 * 0.082 * 300
assert close(pi_k2so4, 7.38) and close(pi_k2so4 / 3, 2.46) and close(pi_k2so4 * 2 / 3, 4.92) \
    and close(pi_k2so4 * 4 / 3, 9.84)
add("van't Hoff factor", I, "numerical",
    "The osmotic pressure at 300 K of a 0.10 M aqueous solution of potassium sulphate, assuming complete "
    "dissociation, is (R = 0.082 L atm K⁻¹ mol⁻¹):",
    Opts("C", "7.38 atm", ["2.46 atm", "4.92 atm", "9.84 atm"]),
    "Osmotic pressure of an electrolyte solution, π = iCRT",
    "K₂SO₄ → 2K⁺ + SO₄²⁻ gives three ions per formula unit, so i = 3.",
    ["i = 3", "π = 3 × 0.10 × 0.082 × 300", "π = 7.38 atm"],
    why="2.46 atm ignores dissociation (i = 1). 4.92 atm takes i = 2, counting K₂ as one particle. 9.84 atm takes "
        "i = 4.",
    ncert=f"{REF5}, abnormal molar masses: van't Hoff factor", seconds=45, checked=True)

x_hcl = 1 / (1 + 63.5 / 18)
assert close(x_hcl, 0.221) and close(1 / (63.5 / 18), 0.2835) and close(36.5 / 63.5, 0.575)
add("Concentration terms", I, "numerical",
    "Concentrated hydrochloric acid is 36.5% HCl by mass. The mole fraction of HCl in it is (H = 1, Cl = 35.5, "
    "O = 16):",
    Opts("B", "0.221", ["0.365", "0.283", "0.575"]),
    "Converting mass percentage into mole fraction",
    "Take 100 g of solution: 36.5 g is HCl and the rest is water. Convert both to moles; the mole fraction is the "
    "moles of HCl divided by the total moles.",
    ["n(HCl) = 36.5/36.5 = 1.00 mol", "n(H₂O) = 63.5/18 = 3.53 mol", "x(HCl) = 1.00/(1.00 + 3.53) = 0.221"],
    why="0.365 is the mass fraction, not the mole fraction. 0.283 divides by the moles of water only (a mole "
        "ratio). 0.575 is the ratio of the masses of HCl and water.",
    ncert=f"{REF5}, expressing concentration of solutions: mole fraction", seconds=50, checked=True)

truth5 = {"a": True, "b": True, "c": False, "d": False, "e": True}
add("Colligative properties", I, "multi_statement",
    ms("Which of the following statements about osmosis are correct?",
       ["Wilted flowers revive when they are placed in fresh water.",
        "People who take a lot of salt may experience water retention in tissue cells and intercellular spaces, "
        "with puffiness or swelling (oedema).",
        "In the osmotic pressure method of finding molar masses, the molality of the solution is used.",
        "In osmosis, solvent molecules move from the more concentrated solution into the more dilute one.",
        "Compared with the other colligative properties, osmotic pressure has a large magnitude even for very "
        "dilute solutions."]),
    multi("D", truth5, ["(a), (b) and (c) only", "(c), (d) and (e) only", "(a) and (d) only"]),
    "Osmosis in everyday life; the osmotic pressure method",
    "Water enters the cells of wilted flowers by osmosis, and excess salt in the body draws water into the "
    "tissues (oedema). The osmotic pressure method uses MOLARITY (π = CRT) and is measured near room "
    "temperature; its magnitude is large even for dilute solutions, which makes it suitable for macromolecules. "
    "In osmosis the solvent moves from the dilute side (or pure solvent) into the more concentrated solution.",
    ["(a) ✓", "(b) ✓", "(c) ✗ molarity, not molality", "(d) ✗ direction reversed", "(e) ✓"],
    why="(c) and (d) are false; every option containing either of them is wrong.",
    ncert=f"{REF5}, osmosis and osmotic pressure", seconds=60)

add("Colligative properties", I, "assertion_reason",
    ar("A 0.1 m aqueous solution of sucrose and a 0.1 m aqueous solution of urea (both non-volatile "
       "non-electrolytes) show the same depression of freezing point.",
       "A sucrose molecule (C₁₂H₂₂O₁₁) contains many more atoms than a urea molecule (CO(NH₂)₂)."),
    AR_, "Colligative properties depend on the number of solute particles, not on their nature",
    "ΔTf = K_f m for a non-electrolyte. Both solutions have the same molality and neither solute dissociates or "
    "associates, so both contain the same number of solute particles per kilogram of water and show the same "
    "ΔTf: A is true. R is also true, but the size or composition of the solute molecule plays no part in a "
    "colligative property, so R does not explain A.",
    ["A: same m, i = 1 for both → same ΔTf = 1.86 × 0.1 = 0.186 K → true",
     "R: C₁₂H₂₂O₁₁ has 45 atoms, CO(NH₂)₂ has 8 → true",
     "ΔTf does not depend on the nature of the solute particles → R is unrelated → option B"],
    answer="B",
    why="R is a true statement about the two molecules, but colligative properties depend only on the number of "
        "solute particles, so R cannot be the explanation of A (if anything it would wrongly suggest a "
        "difference).",
    ncert=f"{REF5}, colligative properties and determination of molar mass", seconds=40)

add("Raoult's law and ideal solutions", I, "statement_pair",
    sp("The components of an azeotropic mixture can be separated completely by fractional distillation.",
       "For a solution showing positive deviation from Raoult's law, the total vapour pressure at every "
       "composition lies above the straight line expected for an ideal solution."),
    SP_, "Azeotropes and vapour pressure–composition plots of non-ideal solutions",
    "Azeotropes boil at a constant temperature and the liquid and vapour have the same composition, so they "
    "cannot be separated by fractional distillation: Statement I is false. In a positive deviation the A–B "
    "attractions are weaker than A–A and B–B, molecules escape more easily, and the vapour pressure is higher "
    "than predicted by Raoult's law: Statement II is true.",
    ["I: azeotrope → same composition in liquid and vapour → cannot be separated → false",
     "II: positive deviation → vapour pressure above the ideal line → true"],
    answer="D",
    why="Statement I contradicts the definition of an azeotrope; Statement II is the meaning of a positive "
        "deviation.",
    ncert=f"{REF5}, non-ideal solutions; azeotropes", seconds=40)

kb_w = R_J * 18 * 373 ** 2 / (1000 * 40660)
assert close(kb_w, 0.512) and close(kb_w * 1000, 512) and close(R_J * 18 * 100 ** 2 / (1000 * 40660), 0.0368) \
    and close(R_J * 18 * 373 / (1000 * 40660), 1.373e-3)
add("Colligative properties", A, "numerical",
    "The molal elevation constant of a solvent is given by K_b = R M₁ T_b² / (1000 Δ_vapH), where M₁ is the "
    "molar mass of the solvent in g mol⁻¹, T_b its boiling point in kelvin and Δ_vapH its molar enthalpy of "
    "vaporisation in J mol⁻¹. For water, T_b = 373 K and Δ_vapH = 40.66 kJ mol⁻¹. K_b of water is "
    "(R = 8.314 J K⁻¹ mol⁻¹, M₁ = 18 g mol⁻¹):",
    Opts("A", "0.512 K kg mol⁻¹", ["512 K kg mol⁻¹", "0.0368 K kg mol⁻¹", "1.37 × 10⁻³ K kg mol⁻¹"]),
    "Ebullioscopic constant from the properties of the solvent",
    "Substitute the data with Δ_vapH in J mol⁻¹ and T_b in kelvin, squaring T_b.",
    ["Numerator: 8.314 × 18 × 373² = 8.314 × 18 × 139 129 = 2.082 × 10⁷",
     "Denominator: 1000 × 40 660 = 4.066 × 10⁷", "K_b = 0.512 K kg mol⁻¹"],
    why="512 leaves out the factor 1000 in the denominator. 0.0368 uses 100 (the temperature in °C) for T_b. "
        "1.37 × 10⁻³ forgets to square T_b.",
    ncert=f"{REF5}, elevation of boiling point", seconds=90, checked=True)

dtf_mix = 1.86 * (0.01 * 2 + 0.01 * 3)
assert close(dtf_mix, 0.093) and close(1.86 * 0.02, 0.0372) and close(1.86 * 0.04, 0.0744) \
    and close(1.86 * 0.03, 0.0558)
add("van't Hoff factor", A, "numerical",
    "0.010 mol of NaCl and 0.010 mol of CaCl₂ are dissolved together in 1.0 kg of water. Assuming complete "
    "dissociation of both salts, the depression of the freezing point of the solution is (K_f of water = "
    "1.86 K kg mol⁻¹):",
    Opts("D", "0.093 K", ["0.0372 K", "0.0744 K", "0.0558 K"]),
    "Colligative properties depend on the total molality of solute particles",
    "Add up the particles: NaCl gives 2 ions and CaCl₂ gives 3 ions per formula unit. The total particle "
    "molality fixes ΔTf.",
    ["Particles from NaCl: 2 × 0.010 = 0.020 mol", "Particles from CaCl₂: 3 × 0.010 = 0.030 mol",
     "Total = 0.050 mol in 1.0 kg → 0.050 mol kg⁻¹", "ΔTf = 1.86 × 0.050 = 0.093 K"],
    why="0.0372 K ignores dissociation. 0.0744 K takes i = 2 for both salts. 0.0558 K counts only the ions "
        "from CaCl₂ and leaves out the NaCl.",
    ncert=f"{REF5}, abnormal molar masses: van't Hoff factor", seconds=70, checked=True)

m_sol = 0.93 / 1.86
pi_sol = m_sol * 0.0821 * 300
assert close(m_sol, 0.5) and close(pi_sol, 12.3, 0.01) and close(m_sol * 0.0821 * 27, 1.108) \
    and close(2 * pi_sol, 24.6, 0.01)
add("Colligative properties", A, "numerical",
    "A dilute aqueous solution of a non-volatile non-electrolyte freezes at −0.93 °C. Taking its molarity to be "
    "equal to its molality, its osmotic pressure at 27 °C is (K_f of water = 1.86 K kg mol⁻¹, "
    "R = 0.0821 L atm K⁻¹ mol⁻¹; freezing point of water = 0 °C):",
    Opts("B", "12.3 atm", ["1.11 atm", "24.6 atm", "6.16 atm"]),
    "Linking two colligative properties through the concentration",
    "Find the molality from ΔTf, take it as the molarity C, and use π = CRT with T in kelvin.",
    ["m = ΔTf/K_f = 0.93/1.86 = 0.50 mol kg⁻¹ ≈ 0.50 mol L⁻¹", "T = 27 + 273 = 300 K",
     "π = 0.50 × 0.0821 × 300 = 12.3 atm"],
    why="1.11 atm uses 27 (°C) for T. 24.6 atm doubles the concentration as if the solute dissociated into two "
        "particles. 6.16 atm halves it.",
    ncert=f"{REF5}, depression of freezing point; osmotic pressure", seconds=80, checked=True)

i_vals = {"AB": 1 + 0.5 * 1, "AB₂": 1 + 0.5 * 2, "dimer": 1 - 0.5 / 2, "AB₃": 1 + 0.5 * 3}
assert i_vals == {"AB": 1.5, "AB₂": 2.0, "dimer": 0.75, "AB₃": 2.5}
add("van't Hoff factor", A, "match_list",
    lists("Match List-I (behaviour of the solute in a dilute solution) with List-II (van't Hoff factor, i).",
          ["A salt AB that is 50% dissociated into A⁺ and B⁻",
           "A salt AB₂ that is 50% dissociated into A²⁺ and 2B⁻",
           "A solute X of which 50% of the molecules have dimerised (2X ⇌ X₂)",
           "A salt AB₃ that is 50% dissociated into A³⁺ and 3B⁻"],
          ["2.0", "0.75", "2.5", "1.5"]),
    match("A", M("IV I II III"), [M("I IV II III"), M("IV III II I"), M("IV I III II")]),
    "van't Hoff factor for partial dissociation and association",
    "For dissociation into n particles with degree α: i = 1 + (n − 1)α. For dimerisation with degree of "
    "association α: i = 1 − α/2.",
    ["AB: 1 + 0.5 × 1 = 1.5 → IV", "AB₂: 1 + 0.5 × 2 = 2.0 → I", "Dimerisation: 1 − 0.5/2 = 0.75 → II",
     "AB₃: 1 + 0.5 × 3 = 2.5 → III"],
    why="The wrong codes swap AB with AB₂, AB₂ with AB₃, or the dimer with AB₃ (association LOWERS i below 1).",
    ncert=f"{REF5}, abnormal molar masses: van't Hoff factor", seconds=80, checked=True)


# ==================================================================== 6. Equilibrium
topic("Equilibrium")
REF6 = f"{C11}, 'Equilibrium'"

add("Physical equilibria and Henry's law", B, "direct",
    "Bottles of soda water and soft drinks are sealed under high pressure in order to:",
    Opts("C", "increase the solubility of carbon dioxide in the drink",
         ["decrease the solubility of carbon dioxide in the drink", "raise the boiling point of the drink",
          "stop carbon dioxide from reacting with water"]),
    "Henry's law: the solubility of a gas in a liquid increases with its pressure",
    "By Henry's law, the mass of a gas dissolved in a given mass of liquid at a given temperature is "
    "proportional to the pressure of the gas above it. Sealing under high pressure keeps more CO₂ dissolved; "
    "when the bottle is opened the pressure falls and gas escapes as bubbles.",
    ["Solubility of a gas ∝ its partial pressure (Henry's law)", "High pressure → more CO₂ dissolved"],
    why="Higher pressure raises, not lowers, the solubility of a gas. The purpose is not to change the boiling "
        "point or to prevent a reaction.",
    ncert=f"{REF6}, equilibrium in physical processes: dissolution of gases in liquids", seconds=20)

add("Physical equilibria and Henry's law", B, "direct",
    "Which of the following substances can set up a solid ⇌ vapour equilibrium (it sublimes) when kept in a "
    "closed vessel and warmed gently?",
    Opts("A", "Camphor", ["Sodium chloride", "Sugar", "Copper sulphate"]),
    "Solid–vapour equilibrium (sublimation)",
    "NCERT gives iodine, camphor and ammonium chloride as substances that pass directly from the solid to the "
    "vapour; in a closed vessel the solid and its vapour reach a dynamic equilibrium.",
    ["Camphor(solid) ⇌ camphor(vapour)"],
    why="Sodium chloride, sugar and copper sulphate do not sublime on gentle warming.",
    ncert=f"{REF6}, equilibrium in physical processes: solid–vapour equilibrium", seconds=20)

ph_b3 = -math.log10(2.0e-3)
assert close(ph_b3, 2.70, 0.002)
add("Acids, bases and pH", B, "numerical",
    "The pH of a 2.0 × 10⁻³ M aqueous solution of hydrochloric acid at 298 K, assuming complete ionisation, is "
    "(log 2 = 0.30):",
    Opts("B", "2.70", ["3.30", "11.30", "2.30"]),
    "pH of a strong acid, pH = −log[H₃O⁺]",
    "HCl ionises completely, so [H₃O⁺] equals the concentration of the acid.",
    ["[H₃O⁺] = 2.0 × 10⁻³ M", "pH = −log(2.0 × 10⁻³) = 3 − log 2 = 3 − 0.30 = 2.70"],
    why="3.30 adds log 2 instead of subtracting it. 11.30 is 14 − 2.70, the pOH. 2.30 uses log 5 instead of "
        "log 2.",
    ncert=f"{REF6}, the pH scale", seconds=30, checked=True)

kp_b4 = 0.6 ** 2 / 0.4
assert close(kp_b4, 0.90) and close(0.6 / 0.4, 1.5) and close(0.4 / 0.36, 1.11, 0.01)
add("Kp, Kc and Le Chatelier", B, "numerical",
    "At equilibrium at a certain temperature, the partial pressures in the reaction N₂O₄(g) ⇌ 2NO₂(g) are "
    "p(N₂O₄) = 0.40 bar and p(NO₂) = 0.60 bar. K_p for the reaction at this temperature is:",
    Opts("A", "0.90 bar", ["1.5 bar", "1.11 bar⁻¹", "0.90 bar⁻¹"]),
    "Writing and evaluating K_p",
    "K_p = p²(NO₂)/p(N₂O₄); the coefficient 2 becomes a power, and the unit is bar²/bar = bar.",
    ["K_p = (0.60)² / 0.40 = 0.36/0.40 = 0.90 bar"],
    why="1.5 bar forgets to square p(NO₂). 1.11 bar⁻¹ inverts the expression. 0.90 bar⁻¹ has the right number "
        "but the wrong unit (Δn = +1, so the unit is bar).",
    ncert=f"{REF6}, equilibrium constant in gaseous systems", seconds=35, checked=True)

add("Acids, bases and pH", B, "direct",
    "Which of the following species can act as a Lewis acid?",
    Opts("D", "Mg²⁺", ["NH₃", "OH⁻", "H₂O"]),
    "Lewis acids are electron-pair acceptors",
    "Metal cations such as Mg²⁺ and Co³⁺ can accept electron pairs (from water molecules or other ligands) and "
    "so are Lewis acids. NH₃, OH⁻ and H₂O have lone pairs that they donate: they are Lewis bases.",
    ["Mg²⁺: electron-deficient cation → accepts electron pairs → Lewis acid",
     "NH₃, OH⁻, H₂O: lone-pair donors → Lewis bases"],
    why="NH₃, OH⁻ and H₂O are given in NCERT as examples of Lewis bases.",
    ncert=f"{REF6}, Lewis acids and bases", seconds=25)

alpha_p = math.sqrt(0.45 / (0.45 + 0.8))
assert close(alpha_p, 0.6) and close(alpha_p ** 2, 0.36) and close(math.sqrt(0.45 / 0.8), 0.75)
add("Kp, Kc and Le Chatelier", I, "numerical",
    "For PCl₅(g) ⇌ PCl₃(g) + Cl₂(g), K_p = 0.45 atm at a certain temperature. Pure PCl₅ is allowed to reach "
    "equilibrium at this temperature, and the total pressure at equilibrium is 0.80 atm. The degree of "
    "dissociation of PCl₅ is:",
    Opts("C", "0.60", ["0.36", "0.75", "0.40"]),
    "Relating K_p to the degree of dissociation and the total pressure",
    "Start with 1 mol PCl₅; at equilibrium there are (1 − α) mol PCl₅, α mol PCl₃ and α mol Cl₂, total (1 + α). "
    "Partial pressures are mole fractions × P.",
    ["p(PCl₃) = p(Cl₂) = αP/(1 + α); p(PCl₅) = (1 − α)P/(1 + α)", "K_p = α²P/(1 − α²)",
     "0.45 = 0.80 α²/(1 − α²) → α² = 0.45/(0.45 + 0.80) = 0.36", "α = 0.60"],
    why="0.36 is α², not α. 0.75 uses K_p = α²P (forgets the 1 − α² term). 0.40 is 1 − α, the fraction left "
        "undissociated.",
    ncert=f"{REF6}, equilibrium constant in gaseous systems; applications of equilibrium constants",
    seconds=90, checked=True)

n_h = 1e-13 * 1e-3
assert close(n_h * NA, 6.022e7) and close(1e-13 * NA, 6.022e10) and close(0.1 * 1e-3 * NA, 6.022e19)
add("Acids, bases and pH", I, "numerical",
    "The number of H₃O⁺ ions present in 1.0 mL of an aqueous solution of pH 13 at 298 K is "
    "(Nₐ = 6.0 × 10²³ mol⁻¹):",
    Opts("A", "6.0 × 10⁷", ["6.0 × 10¹⁰", "6.0 × 10¹⁹", "1.0 × 10⁻¹⁶"]),
    "From pH to concentration to number of ions",
    "pH 13 means [H₃O⁺] = 10⁻¹³ mol L⁻¹. Convert the volume to litres, find the moles and multiply by Nₐ.",
    ["[H₃O⁺] = 10⁻¹³ mol L⁻¹", "In 1.0 mL = 10⁻³ L: 10⁻¹³ × 10⁻³ = 10⁻¹⁶ mol",
     "Number = 10⁻¹⁶ × 6.0 × 10²³ = 6.0 × 10⁷"],
    why="6.0 × 10¹⁰ is the number in one litre (mL not converted). 6.0 × 10¹⁹ counts OH⁻ ions (0.1 M) instead "
        "of H₃O⁺. 1.0 × 10⁻¹⁶ is the amount in moles, not the number of ions.",
    ncert=f"{REF6}, the pH scale", seconds=50, checked=True)

add("Solubility product", I, "assertion_reason",
    ar("Calcium phosphate, a salt of a weak acid, is more soluble in an acidic solution than in pure water.",
       "In acid, phosphate ions are protonated, which lowers their concentration, so more of the salt dissolves "
       "before the ionic product again equals K_sp."),
    AR_, "Effect of pH on the solubility of salts of weak acids",
    "NCERT notes that the solubility of salts of weak acids such as phosphates increases at lower pH: the anion "
    "is protonated, its concentration falls, the ionic product drops below K_sp and more salt dissolves until "
    "Q_sp = K_sp again. R is the reason for A.",
    ["A: phosphate salt dissolves more at low pH → true",
     "R: PO₄³⁻ + H⁺ → HPO₄²⁻ … lowers [PO₄³⁻] → more dissolves → true and explains A"],
    answer="A",
    why="Both statements are true and the protonation of the anion described in R is exactly why the solubility "
        "rises in acid.",
    ncert=f"{REF6}, solubility equilibria: common ion effect and effect of pH on solubility", seconds=40)

truth6 = {"a": True, "b": True, "c": False, "d": False, "e": True}
add("Acids, bases and pH", I, "multi_statement",
    ms("Which of the following statements are correct at 298 K?",
       ["In aqueous solution, the proton exists as the hydronium ion, H₃O⁺, and not as a bare H⁺ ion.",
        "Human blood is slightly basic, with a pH of about 7.4.",
        "Gastric juice is basic.",
        "Milk of magnesia is acidic.",
        "Lemon juice is more acidic than black coffee."]),
    multi("B", truth6, ["(a), (b), (c) and (e) only", "(b), (d) and (e) only", "(a) and (b) only"]),
    "The hydronium ion and the pH of some common fluids",
    "A bare proton is very reactive and attaches to a water molecule, giving H₃O⁺. Blood has pH about 7.4 "
    "(slightly basic); gastric juice is strongly acidic (pH about 1.2); milk of magnesia is basic (pH about "
    "10); lemon juice (pH about 2.2) is more acidic than black coffee (pH about 5).",
    ["(a) ✓", "(b) ✓", "(c) ✗ strongly acidic", "(d) ✗ basic", "(e) ✓"],
    why="(c) and (d) reverse the nature of gastric juice and milk of magnesia; '(a) and (b) only' misses (e).",
    ncert=f"{REF6}, Arrhenius concept (hydronium ion); the pH scale (pH of some common substances)", seconds=50)

oh = {"A": 1e-14 / 1e-3, "B": 1e-14 / 1e-9, "C": 1e-4, "D": 1e-14 / 1e-7}
assert all(close(v, w) for v, w in zip(oh.values(), (1e-11, 1e-5, 1e-4, 1e-7)))
add("Acids, bases and pH", I, "match_list",
    lists("Match List-I (aqueous solution at 298 K) with List-II (its hydroxide ion concentration). "
          "(K_w = 1.0 × 10⁻¹⁴)",
          ["A solution of pH 3", "A solution of pH 9", "A solution of pOH 4",
           "A solution in which [H₃O⁺] = 1.0 × 10⁻⁷ M"],
          ["1.0 × 10⁻⁴ M", "1.0 × 10⁻⁷ M", "1.0 × 10⁻¹¹ M", "1.0 × 10⁻⁵ M"]),
    match("B", M("III IV I II"), [M("IV III I II"), M("III I IV II"), M("III IV II I")]),
    "pH, pOH and K_w",
    "At 298 K, pH + pOH = 14 and [OH⁻] = 10^(−pOH).",
    ["pH 3 → pOH 11 → 10⁻¹¹ M → III", "pH 9 → pOH 5 → 10⁻⁵ M → IV", "pOH 4 → 10⁻⁴ M → I",
     "[H₃O⁺] = 10⁻⁷ → [OH⁻] = 10⁻⁷ M → II"],
    why="The wrong codes give [H₃O⁺] instead of [OH⁻] for one of the solutions, or swap pH 9 with pOH 4.",
    ncert=f"{REF6}, ionisation constant of water and the pH scale", seconds=50, checked=True)

add("Physical equilibria and Henry's law", I, "statement_pair",
    sp("At high altitudes, water boils at a higher temperature than at sea level.",
       "At a given temperature, of two liquids the one with the higher vapour pressure has the lower boiling "
       "point."),
    SP_, "Liquid–vapour equilibrium and boiling point",
    "A liquid boils when its vapour pressure equals the external pressure. At high altitude the atmospheric "
    "pressure is lower, so this happens at a LOWER temperature: Statement I is false. A liquid that already has "
    "a higher vapour pressure at a given temperature reaches the external pressure sooner on heating, so it "
    "boils at a lower temperature: Statement II is true.",
    ["I: lower atmospheric pressure → lower boiling point → false",
     "II: higher vapour pressure → more volatile → lower boiling point → true"],
    answer="D",
    why="Statement I reverses the effect of pressure on the boiling point.",
    ncert=f"{REF6}, equilibrium in physical processes: liquid–vapour equilibrium", seconds=35)

add("Kp, Kc and Le Chatelier", I, "assertion_reason",
    ar("For the equilibrium N₂(g) + O₂(g) ⇌ 2NO(g), ΔH > 0, raising the temperature increases the amount of NO "
       "at equilibrium.",
       "Raising the temperature increases the equilibrium constant of every reaction."),
    AR_, "Effect of temperature on equilibrium (Le Chatelier's principle)",
    "For an endothermic reaction, a rise in temperature is absorbed by shifting the equilibrium forward, so K "
    "increases and more NO forms: A is true. But for an exothermic reaction K DECREASES with rise in "
    "temperature, so R, which claims this for every reaction, is false.",
    ["A: endothermic → higher T favours products → true", "R: K falls with T for exothermic reactions → false"],
    answer="C",
    why="R is a false generalisation, so options A and B are wrong; A itself is true, so option D is wrong.",
    ncert=f"{REF6}, factors affecting equilibria: effect of temperature", seconds=40)

kp_carb = 2.0 ** 2 * 1.0
assert kp_carb == 4.0 and 2.0 * 1.0 == 2.0 and close(1.5 ** 3, 3.375)
add("Kp, Kc and Le Chatelier", A, "numerical",
    "Solid ammonium carbamate is placed in an evacuated vessel and allowed to reach equilibrium at a certain "
    "temperature: NH₂COONH₄(s) ⇌ 2NH₃(g) + CO₂(g). The total pressure at equilibrium is 3.0 atm. K_p for the "
    "equilibrium is:",
    Opts("D", "4.0 atm³", ["2.0 atm³", "3.375 atm³", "27 atm³"]),
    "K_p for a heterogeneous equilibrium in which the gases come only from the solid",
    "The solid does not appear in K_p. Because the gases are formed in the ratio 2 : 1, p(NH₃) = 2p(CO₂); the "
    "two partial pressures add up to the total pressure.",
    ["p(NH₃) + p(CO₂) = 3p(CO₂) = 3.0 atm → p(CO₂) = 1.0 atm, p(NH₃) = 2.0 atm",
     "K_p = p²(NH₃) × p(CO₂) = (2.0)² × 1.0 = 4.0 atm³"],
    why="2.0 atm³ forgets to square p(NH₃). 3.375 atm³ shares the pressure equally (1.5 atm each), ignoring "
        "the 2 : 1 ratio. 27 atm³ cubes the total pressure.",
    ncert=f"{REF6}, heterogeneous equilibria", seconds=70, checked=True)

ka_a2 = 1e-5
c_new = (1e-4) ** 2 / ka_a2
assert close(math.sqrt(ka_a2 * 0.1), 1e-3) and close(c_new, 1e-3) and close(0.1 / c_new, 100)
add("Acids, bases and pH", A, "numerical",
    "A 0.10 M aqueous solution of a weak monobasic acid HA (K_a = 1.0 × 10⁻⁵) is diluted with water at 298 K. "
    "Using [H₃O⁺] ≈ √(K_a c), by what factor must the solution be diluted to raise its pH by exactly one unit?",
    Opts("C", "100 times", ["10 times", "1000 times", "√10 ≈ 3.2 times"]),
    "Dilution of a weak acid: [H₃O⁺] varies as √c",
    "Raising the pH by one unit means lowering [H₃O⁺] ten times. For a weak acid [H₃O⁺] ∝ √c, so the "
    "concentration must fall 10² = 100 times.",
    ["Initially [H₃O⁺] = √(10⁻⁵ × 0.1) = 10⁻³ M (pH 3)", "Target pH 4: [H₃O⁺] = 10⁻⁴ M",
     "c = [H₃O⁺]²/K_a = 10⁻⁸/10⁻⁵ = 10⁻³ M", "Dilution factor = 0.1/10⁻³ = 100"],
    why="10 times would be enough for a STRONG acid, whose [H₃O⁺] is proportional to c. 1000 times overshoots "
        "(pH would rise by 1.5). √10 times raises the pH by only 0.25.",
    ncert=f"{REF6}, ionisation of weak acids", seconds=90, checked=True)

truth6a = {"a": True, "b": True, "c": False, "d": True, "e": False}
add("Kp, Kc and Le Chatelier", A, "multi_statement",
    ms("For the equilibrium CO(g) + 2H₂(g) ⇌ CH₃OH(g), ΔH < 0, set up in a closed vessel, which of the "
       "following statements are correct?",
       ["K_p = K_c (RT)⁻².",
        "Compressing the mixture to a smaller volume at constant temperature increases the amount of CH₃OH at "
        "equilibrium.",
        "Raising the temperature increases the equilibrium constant.",
        "The unit of K_c is L² mol⁻².",
        "Adding a catalyst increases the amount of CH₃OH at equilibrium."]),
    multi("A", truth6a, ["(a), (b), (c) and (d) only", "(b), (d) and (e) only", "(a) and (d) only"]),
    "K_p–K_c relation, units of K and Le Chatelier's principle",
    "Δn(gas) = 1 − 3 = −2, so K_p = K_c(RT)⁻² and K_c = [CH₃OH]/([CO][H₂]²) has the unit (mol L⁻¹)⁻² = "
    "L² mol⁻². Compression favours the side with fewer gas molecules (CH₃OH). The reaction is exothermic, so K "
    "falls when the temperature rises. A catalyst only helps the system reach equilibrium faster.",
    ["(a) Δn = −2 ✓", "(b) 3 mol gas → 1 mol gas favoured at higher pressure ✓", "(c) exothermic → K falls ✗",
     "(d) ✓", "(e) catalyst does not shift equilibrium ✗"],
    why="Options containing (c) or (e) are wrong; '(a) and (d) only' leaves out the pressure effect (b).",
    ncert=f"{REF6}, relationship between K_p and K_c; factors affecting equilibria", seconds=80)

s_ba = 1.0e-10 / 0.01
assert close(s_ba * 233, 2.33e-6) and close(math.sqrt(1.0e-10) * 233, 2.33e-3) \
    and close(1.0e-10 / 0.01 ** 2 * 233, 2.33e-4)
add("Solubility product", A, "numerical",
    "K_sp of BaSO₄ at 298 K is 1.0 × 10⁻¹⁰. The mass of BaSO₄ that can dissolve in 1.0 L of a 0.010 M Na₂SO₄ "
    "solution at 298 K is (molar mass of BaSO₄ = 233 g mol⁻¹; Na₂SO₄ is completely dissociated):",
    Opts("B", "2.33 × 10⁻⁶ g", ["2.33 × 10⁻³ g", "1.0 × 10⁻⁸ g", "2.33 × 10⁻⁴ g"]),
    "Common ion effect on solubility",
    "The sulphate from Na₂SO₄ (0.010 M) swamps the tiny amount from BaSO₄, so [SO₄²⁻] ≈ 0.010 M and the "
    "solubility s = [Ba²⁺] = K_sp/0.010.",
    ["K_sp = [Ba²⁺][SO₄²⁻] = s × 0.010", "s = 1.0 × 10⁻¹⁰ / 0.010 = 1.0 × 10⁻⁸ mol L⁻¹",
     "Mass in 1.0 L = 1.0 × 10⁻⁸ × 233 = 2.33 × 10⁻⁶ g"],
    why="2.33 × 10⁻³ g is the solubility in pure water (s = √K_sp), ignoring the common ion. 1.0 × 10⁻⁸ g is "
        "the amount in moles written as grams. 2.33 × 10⁻⁴ g divides K_sp by (0.010)².",
    ncert=f"{REF6}, common ion effect in the ionisation of salts", seconds=80, checked=True)

ph_buf = 4.74 + math.log10(0.095 / 0.105)
assert close(4.74 - ph_buf, 0.0435, 0.02) and 4.74 - ph_buf < 0.05 and close(-math.log10(0.005), 2.30, 0.002)
add("Hydrolysis and buffers", A, "statement_pair",
    sp("Adding 0.005 mol of HCl to 1 L of a buffer containing 0.10 mol of CH₃COOH and 0.10 mol of CH₃COONa "
       "(pK_a = 4.74) lowers its pH by less than 0.05 unit (log (19/21) = −0.043).",
       "Adding 0.005 mol of HCl to 1 L of pure water at 298 K lowers its pH from 7 to about 2.3 "
       "(log 5 = 0.70)."),
    SP_, "Buffer action compared with unbuffered water",
    "In the buffer, the added H⁺ converts 0.005 mol CH₃COO⁻ into CH₃COOH: the ratio becomes 0.095/0.105 = 19/21 "
    "and pH = 4.74 − 0.043 = 4.70, a drop of only 0.043. Statement I is true. In water, [H₃O⁺] becomes "
    "5 × 10⁻³ M and pH = 3 − 0.70 = 2.30, a drop of nearly 5 units. Statement II is true.",
    ["I: pH = 4.74 + log(0.095/0.105) = 4.74 − 0.043 = 4.70 → drop < 0.05 → true",
     "II: [H₃O⁺] = 0.005 M → pH 2.30 → true"],
    answer="A",
    why="Both statements hold; together they show how strongly the buffer resists the change in pH.",
    ncert=f"{REF6}, buffer solutions (Henderson–Hasselbalch equation)", seconds=90, checked=True)


# ==================================================================== 7. Redox Reactions and Electrochemistry
topic("Redox Reactions and Electrochemistry")
REF7R = f"{C11}, 'Redox Reactions'"
REF7 = f"{C12}, 'Electrochemistry'"

x_p = -1 - 2 * 1 + 2 * 2
assert x_p == 1
add("Oxidation number and balancing", B, "numerical",
    "The oxidation number of phosphorus in barium hypophosphite, Ba(H₂PO₂)₂, is:",
    Opts("B", "+1", ["+3", "+5", "−1"]),
    "Rules for assigning oxidation numbers",
    "Ba is +2, so each H₂PO₂⁻ ion carries a charge of −1. In it, H is +1 and O is −2.",
    ["H₂PO₂⁻: 2(+1) + x + 2(−2) = −1", "2 + x − 4 = −1 → x = +1"],
    why="+3 and +5 are the oxidation numbers of P in phosphite (H₃PO₃) and phosphate. −1 treats the hydrogen "
        "atoms as hydride (−1).",
    ncert=f"{REF7R}, oxidation number", seconds=35, checked=True)

add("Electrode potential and cells", B, "direct",
    "In the cell representation Zn(s) | Zn²⁺(aq) || Cu²⁺(aq) | Cu(s), the double vertical line stands for:",
    Opts("D", "a salt bridge", ["the boundary between an electrode and its solution", "the anode",
                                "the direction in which electrons flow"]),
    "Conventional representation of a galvanic cell",
    "In the cell notation, a single vertical line marks a phase boundary (metal | solution), and a double "
    "vertical line marks the salt bridge joining the two half-cells. The anode is written on the left.",
    ["| → phase boundary", "|| → salt bridge"],
    why="A phase boundary is shown by a single line; the anode and the direction of electron flow are shown by "
        "the order of writing (anode on the left), not by the double line.",
    ncert=f"{REF7}, galvanic cells: representation of a cell", seconds=20)

add("Batteries and fuel cells", B, "direct",
    "In the dry (Leclanché) cell, the ammonia produced in the cathode reaction:",
    Opts("A", "combines with Zn²⁺ ions to form the complex [Zn(NH₃)₄]²⁺",
         ["escapes as a gas through a vent in the cell", "is oxidised at the zinc anode",
          "reduces manganese dioxide to manganese metal"]),
    "Reactions in the dry cell",
    "At the cathode MnO₂ + NH₄⁺ + e⁻ → MnO(OH) + NH₃. NCERT notes that the ammonia formed combines with the Zn²⁺ "
    "ions (produced at the anode) to give the complex [Zn(NH₃)₄]²⁺.",
    ["Anode: Zn → Zn²⁺ + 2e⁻", "Cathode: MnO₂ + NH₄⁺ + e⁻ → MnO(OH) + NH₃",
     "NH₃ + Zn²⁺ → [Zn(NH₃)₄]²⁺"],
    why="The dry cell is sealed and the ammonia is taken up as a complex; it is not oxidised at the anode, and "
        "manganese is reduced only from +4 to +3, not to the metal.",
    ncert=f"{REF7}, batteries: primary batteries (dry cell)", seconds=30)

add("Conductance and Kohlrausch's law", B, "statement_pair",
    sp("The SI unit of conductance is the siemens (S), which is equal to Ω⁻¹.",
       "The conductivity of a solution is the reciprocal of its resistance."),
    SP_, "Conductance, resistivity and conductivity",
    "Conductance G = 1/R, measured in siemens (S = Ω⁻¹): Statement I is true. Conductivity κ is the reciprocal "
    "of RESISTIVITY (κ = 1/ρ, unit S m⁻¹), not of resistance; the reciprocal of resistance is the conductance. "
    "Statement II is false.",
    ["I: G = 1/R, unit S = Ω⁻¹ → true", "II: κ = 1/ρ (not 1/R) → false"],
    answer="C",
    why="Statement II confuses conductivity with conductance.",
    ncert=f"{REF7}, conductance of electrolytic solutions", seconds=30)

q_fc = 2 / 2 * 2 * F_CONST
assert q_fc == 193000
add("Batteries and fuel cells", B, "numerical",
    "In a hydrogen–oxygen fuel cell, the anode reaction is 2H₂(g) + 4OH⁻(aq) → 4H₂O(l) + 4e⁻. The quantity of "
    "electricity produced when 2.0 g of hydrogen is consumed is (H = 1, F = 96 500 C mol⁻¹):",
    Opts("D", "1.93 × 10⁵ C", ["9.65 × 10⁴ C", "3.86 × 10⁵ C", "4.83 × 10⁴ C"]),
    "Charge from the amount of reactant: Q = n(e⁻) × F",
    "Each H₂ molecule gives two electrons (2H₂ → 4e⁻). 2.0 g of H₂ is 1.0 mol, which gives 2.0 mol of electrons.",
    ["n(H₂) = 2.0/2 = 1.0 mol", "n(e⁻) = 2 × 1.0 = 2.0 mol", "Q = 2.0 × 96 500 = 1.93 × 10⁵ C"],
    why="9.65 × 10⁴ C takes one electron per H₂. 3.86 × 10⁵ C takes four electrons per H₂ (reading the 4e⁻ of "
        "the equation as per molecule). 4.83 × 10⁴ C takes half a mole of electrons.",
    ncert=f"{REF7}, fuel cells", seconds=40, checked=True)

add("Oxidation number and balancing", I, "direct",
    "Which of the following compounds is given an INCORRECT name in the Stock notation?",
    Opts("C", "Cr₂O₃ – chromium(II) oxide", ["MnO₂ – manganese(IV) oxide", "Hg₂Cl₂ – mercury(I) chloride",
                                             "SnCl₄ – tin(IV) chloride"]),
    "Stock notation: the oxidation number of the metal in Roman numerals",
    "Find the oxidation number of the metal in each compound: Cr₂O₃: 2x = +6 → Cr is +3, so the name should be "
    "chromium(III) oxide.",
    ["MnO₂: Mn +4 ✓", "Hg₂Cl₂: 2x = +2 → Hg +1 ✓", "SnCl₄: Sn +4 ✓", "Cr₂O₃: Cr +3, not +2 ✗"],
    why="The other three names show the correct oxidation numbers; in Hg₂Cl₂ each mercury is +1 (the Hg₂²⁺ unit).",
    ncert=f"{REF7R}, oxidation number: Stock notation", seconds=40)

e_mg = 0.80 - (-2.37) - 0.059 / 2 * math.log10(0.01 / 0.001 ** 2)
assert close(e_mg, 3.052, 0.001) and close(3.17 - 0.0295, 3.14, 0.002) and close(3.17 - 0.059 * 4, 2.93, 0.002) \
    and close(3.17 + 0.118, 3.29, 0.002)
add("Nernst equation and Gibbs energy", I, "numerical",
    "The emf at 298 K of the cell Mg(s) | Mg²⁺(0.010 M) || Ag⁺(0.0010 M) | Ag(s), whose cell reaction is "
    "Mg(s) + 2Ag⁺(aq) → Mg²⁺(aq) + 2Ag(s), is (E°(Mg²⁺/Mg) = −2.37 V, E°(Ag⁺/Ag) = +0.80 V, "
    "2.303RT/F = 0.059 V):",
    Opts("B", "3.05 V", ["3.14 V", "2.93 V", "3.29 V"]),
    "Nernst equation for a cell with unequal numbers of ions",
    "E°cell = E°(cathode) − E°(anode). The reaction quotient contains [Ag⁺]² because two Ag⁺ ions appear in the "
    "balanced equation, and n = 2.",
    ["E°cell = 0.80 − (−2.37) = 3.17 V", "Q = [Mg²⁺]/[Ag⁺]² = 0.010/(0.0010)² = 1.0 × 10⁴",
     "E = 3.17 − (0.059/2) × log 10⁴ = 3.17 − 0.118 = 3.05 V"],
    why="3.14 V forgets to square [Ag⁺] (Q = 10). 2.93 V uses n = 1. 3.29 V adds the correction term, inverting Q.",
    ncert=f"{REF7}, Nernst equation", seconds=90, checked=True)

add("Conductance and Kohlrausch's law", I, "direct",
    "Which of the following ions has the HIGHEST limiting molar conductivity in water at 298 K?",
    Opts("D", "H⁺", ["Na⁺", "K⁺", "Cl⁻"]),
    "Limiting molar conductivities of ions",
    "NCERT's table of limiting molar conductivities at 298 K shows H⁺ (349.6 S cm² mol⁻¹) far above all other "
    "ions; OH⁻ (199.1) comes next. Na⁺ (50.1), K⁺ (73.5) and Cl⁻ (76.3) are much lower.",
    ["H⁺ 349.6 > Cl⁻ 76.3 > K⁺ 73.5 > Na⁺ 50.1 (S cm² mol⁻¹)"],
    why="Na⁺, K⁺ and Cl⁻ have limiting molar conductivities between about 50 and 76 S cm² mol⁻¹.",
    ncert=f"{REF7}, variation of molar conductivity with concentration: Kohlrausch's law (table of λ°)",
    seconds=25)

add("Oxidation number and balancing", I, "assertion_reason",
    ar("In the reaction 2H₂S(g) + SO₂(g) → 3S(s) + 2H₂O(l), sulphur dioxide acts as an oxidising agent.",
       "Sulphur dioxide is a gas at room temperature."),
    AR_, "Identifying the oxidising agent from changes in oxidation number",
    "In SO₂ sulphur is +4 and it becomes 0 in S: it is reduced, so SO₂ is the oxidising agent (H₂S, with S at "
    "−2 going to 0, is the reducing agent). A is true. R is true as well, but being a gas has nothing to do with "
    "the change in oxidation number.",
    ["S in SO₂: +4 → 0 (reduced) → SO₂ is the oxidising agent → A true",
     "SO₂ is a gas at 298 K → R true", "Physical state does not decide the redox role → option B"],
    answer="B",
    why="R is a true property of SO₂ but plainly unrelated to why it oxidises H₂S.",
    ncert=f"{REF7R}, oxidising and reducing agents (oxidation number concept)", seconds=40)

add("Nernst equation and Gibbs energy", I, "match_list",
    lists("Match List-I (quantity for a cell reaction in which n electrons are transferred) with List-II (its "
          "expression). (K = equilibrium constant, Q = reaction quotient; 2.303RT/F = 0.059 V at 298 K)",
          ["Standard Gibbs energy change, ΔrG°", "Standard emf, E°cell, at 298 K",
           "Emf, E_cell, at 298 K", "Gibbs energy change under the actual conditions, ΔrG"],
          ["−nF E_cell", "E°cell − (0.059/n) log Q", "−nF E°cell", "(0.059/n) log K"]),
    match("C", M("III IV II I"), [M("III II IV I"), M("I IV II III"), M("IV III II I")]),
    "Relations between emf, Gibbs energy and the equilibrium constant",
    "ΔrG° = −nFE°cell and ΔrG = −nFE_cell. Combining ΔrG° = −2.303RT log K with the first gives "
    "E°cell = (0.059/n) log K at 298 K. The Nernst equation gives E_cell = E°cell − (0.059/n) log Q.",
    ["A → III", "B → IV", "C → II", "D → I"],
    why="The wrong codes swap the standard and actual quantities, or the Nernst equation with the E°–K relation.",
    ncert=f"{REF7}, Nernst equation; equilibrium constant from Nernst equation; electrochemical cell and "
          f"Gibbs energy of the reaction", seconds=50)

truth7 = {"a": False, "b": False, "c": True, "d": True, "e": True}
add("Electrode potential and cells", I, "multi_statement",
    ms("Which of the following statements about galvanic cells are correct?",
       ["The anode of a galvanic cell is its positive electrode.",
        "Electrons flow through the salt bridge from one half-cell to the other.",
        "E°cell = E°(cathode) − E°(anode), using standard reduction potentials.",
        "In a working Daniell cell, the zinc electrode loses mass.",
        "If an external opposing potential greater than 1.1 V is applied to a Daniell cell, zinc is deposited on "
        "the zinc electrode and copper dissolves."]),
    multi("D", truth7, ["(a), (c) and (d) only", "(b), (c) and (e) only", "(c) and (d) only"]),
    "Working of a galvanic cell",
    "Oxidation occurs at the anode, which releases electrons into the external circuit and is the NEGATIVE "
    "electrode. Electrons flow only through the external wire; the salt bridge carries ions. In the Daniell cell "
    "Zn is oxidised to Zn²⁺, so the zinc rod loses mass. When an external potential larger than 1.1 V opposes "
    "the cell, the reaction reverses: the cell works as an electrolytic cell, zinc is deposited and copper "
    "dissolves.",
    ["(a) ✗ anode is negative", "(b) ✗ ions, not electrons, move in the salt bridge", "(c) ✓", "(d) ✓", "(e) ✓"],
    why="(a) and (b) are false; '(c) and (d) only' misses the NCERT description of the reversed cell in (e).",
    ncert=f"{REF7}, electrochemical cells; galvanic cells", seconds=60)

ph_a1 = (0.517 - 0.34) / 0.059
assert close(ph_a1, 3.0) and close((0.517 - 0.34) / 0.0295, 6.0) and close((0.517 - 0.34) / 0.118, 1.5) and close(0.517 / 0.059, 8.76)
add("Nernst equation and Gibbs energy", A, "numerical",
    "The emf of the cell Pt | H₂(g, 1 bar) | H⁺(aq) || Cu²⁺(aq, 1 M) | Cu(s) at 298 K is 0.517 V. The cell "
    "reaction is H₂(g) + Cu²⁺(aq) → 2H⁺(aq) + Cu(s). The pH of the solution in the hydrogen half-cell is "
    "(E°(Cu²⁺/Cu) = +0.34 V, 2.303RT/F = 0.059 V):",
    Opts("B", "3.0", ["6.0", "1.5", "8.8"]),
    "Nernst equation used to find pH",
    "Apply the Nernst equation to the whole cell with n = 2. Since [H⁺]² appears in Q, the log term becomes "
    "−2 × 0.059/2 × log[H⁺] = 0.059 pH.",
    ["E°cell = 0.34 − 0 = 0.34 V", "E = 0.34 − (0.059/2) log([H⁺]²/[Cu²⁺]) = 0.34 + 0.059 pH",
     "0.517 = 0.34 + 0.059 pH → pH = 0.177/0.059 = 3.0"],
    why="6.0 forgets the square on [H⁺] (uses 0.0295 per pH unit). 1.5 doubles the coefficient (0.118 per pH "
        "unit). 8.8 ignores E° of the copper electrode and "
        "takes E = 0.059 pH.",
    ncert=f"{REF7}, Nernst equation", seconds=120, checked=True)

w_max = 6.54 / 65.4 * 2 * F_CONST * 1.10 / 1000
assert close(w_max, 21.23, 0.001) and close(w_max / 2, 10.6, 0.002) and close(2 * F_CONST * 1.10 / 1000, 212.3)
add("Nernst equation and Gibbs energy", A, "numerical",
    "The standard emf of the Daniell cell is 1.10 V. The maximum electrical work that can be obtained when "
    "6.54 g of zinc is used up in the cell under standard conditions is (Zn = 65.4, F = 96 500 C mol⁻¹):",
    Opts("C", "21.2 kJ", ["10.6 kJ", "212 kJ", "2.12 kJ"]),
    "Maximum electrical work = −ΔG = nFE",
    "For Zn + Cu²⁺ → Zn²⁺ + Cu, n = 2 per mole of zinc. Scale the work per mole to the amount of zinc used.",
    ["n(Zn) = 6.54/65.4 = 0.100 mol", "Charge = 0.100 × 2 × 96 500 = 19 300 C",
     "Work = 19 300 × 1.10 = 21 230 J ≈ 21.2 kJ"],
    why="10.6 kJ uses one electron per Zn atom. 212 kJ is the work per mole of zinc (the 0.1 mol is ignored). "
        "2.12 kJ is a slip of a power of ten.",
    ncert=f"{REF7}, electrochemical cell and Gibbs energy of the reaction", seconds=70, checked=True)

e7 = {"Cl2": 1.36, "Br2": 1.09, "Fe3": 0.77, "I2": 0.54}
truth7a = {"a": e7["Cl2"] > e7["Br2"], "b": e7["Br2"] > e7["I2"], "c": e7["I2"] > e7["Fe3"],
           "d": e7["Fe3"] > e7["Br2"], "e": e7["Br2"] > e7["Fe3"]}
assert truth7a == {"a": True, "b": True, "c": False, "d": False, "e": True}
add("Electrode potential and cells", A, "multi_statement",
    ms("The standard reduction potentials at 298 K are: Cl₂/Cl⁻ +1.36 V, Br₂/Br⁻ +1.09 V, Fe³⁺/Fe²⁺ +0.77 V "
       "and I₂/I⁻ +0.54 V. Which of the following reactions are feasible under standard conditions?",
       ["Cl₂ oxidises Br⁻ to Br₂.", "Br₂ oxidises I⁻ to I₂.", "I₂ oxidises Fe²⁺ to Fe³⁺.",
        "Fe³⁺ oxidises Br⁻ to Br₂.", "Br₂ oxidises Fe²⁺ to Fe³⁺."]),
    multi("A", truth7a, ["(a), (b), (c) and (e) only", "(a), (d) and (e) only", "(b) and (e) only"]),
    "Using the electrochemical series to predict redox reactions",
    "A species can oxidise the reduced form of any couple with a LOWER reduction potential (E°cell > 0).",
    ["(a) 1.36 > 1.09 → feasible ✓", "(b) 1.09 > 0.54 ✓", "(c) 0.54 < 0.77 → not feasible ✗",
     "(d) 0.77 < 1.09 ✗", "(e) 1.09 > 0.77 ✓"],
    why="(c) and (d) would need the oxidant to have the higher reduction potential, which it does not; "
        "'(b) and (e) only' misses (a).",
    ncert=f"{REF7}, electrode potential: the electrochemical series", seconds=70, checked=True)

cr_ox = 0 + 2 + 2 * 2
s_ox = 0 - 2 * 1 + 3 * 2 + 2 * 1
assert cr_ox == 6 and s_ox == 6
add("Oxidation number and balancing", A, "statement_pair",
    sp("In CrO₅, which contains one oxide oxygen atom and two peroxide (–O–O–) groups, chromium has the "
       "oxidation number +6.",
       "In peroxomonosulphuric acid, H₂SO₅, which contains one peroxide (–O–O–) group, sulphur has the "
       "oxidation number +8."),
    SP_, "Oxidation numbers in compounds containing peroxide linkages",
    "Peroxide oxygen is −1. CrO₅: x + (−2) + 4(−1) = 0 → x = +6, so Statement I is true. H₂SO₅ has two "
    "peroxide O atoms (−1 each) and three ordinary O atoms (−2 each): 2(+1) + x + 3(−2) + 2(−1) = 0 → x = +6, "
    "not +8. Statement II is false.",
    ["I: x − 2 − 4 = 0 → +6 → true", "II: 2 + x − 6 − 2 = 0 → +6 → false"],
    answer="C",
    why="+8 is obtained for H₂SO₅ only if all five O atoms are wrongly taken as −2; sulphur cannot exceed its "
        "group oxidation state of +6.",
    ncert=f"{REF7R}, oxidation number", seconds=60, checked=True)


# ==================================================================== 8. Chemical Kinetics
topic("Chemical Kinetics")
REF8 = f"{C12}, 'Chemical Kinetics'"

rate_b1 = 2.0e-2 * 0.50
assert close(rate_b1, 1.0e-2) and close(2.0e-2 / 0.50, 4.0e-2) and close(2.0e-2 * 0.25, 5.0e-3)
add("Rate law and order", B, "numerical",
    "A first-order reaction A → products has a rate constant of 2.0 × 10⁻² s⁻¹. Its rate at the moment when "
    "[A] = 0.50 mol L⁻¹ is:",
    Opts("D", "1.0 × 10⁻² mol L⁻¹ s⁻¹", ["4.0 × 10⁻² mol L⁻¹ s⁻¹", "5.0 × 10⁻³ mol L⁻¹ s⁻¹",
                                         "2.0 × 10⁻² mol L⁻¹ s⁻¹"]),
    "Rate law of a first-order reaction, rate = k[A]",
    "For a first-order reaction the rate is the rate constant multiplied by the concentration of the reactant "
    "at that moment.",
    ["Rate = k[A] = 2.0 × 10⁻² s⁻¹ × 0.50 mol L⁻¹", "= 1.0 × 10⁻² mol L⁻¹ s⁻¹"],
    why="4.0 × 10⁻² divides k by [A]. 5.0 × 10⁻³ uses [A]² (second order). 2.0 × 10⁻² takes the rate equal to k, "
        "which is true only when [A] = 1 mol L⁻¹.",
    ncert=f"{REF8}, rate expression and rate constant", seconds=25, checked=True)

c_b2 = 0.10 - 2.0e-3 * 20
assert close(c_b2, 0.06) and close(0.10 * math.exp(-2.0e-3 * 20), 0.0961, 0.002)
add("Zero and first order reactions", B, "numerical",
    "A zero-order reaction R → P has a rate constant of 2.0 × 10⁻³ mol L⁻¹ s⁻¹. If the initial concentration of "
    "R is 0.10 mol L⁻¹, its concentration after 20 s is:",
    Opts("A", "0.060 mol L⁻¹", ["0.040 mol L⁻¹", "0.140 mol L⁻¹", "0.096 mol L⁻¹"]),
    "Integrated rate equation of a zero-order reaction, [R] = [R]₀ − kt",
    "For a zero-order reaction the concentration falls linearly with time at the rate k.",
    ["[R] = 0.10 − (2.0 × 10⁻³ × 20)", "= 0.10 − 0.040 = 0.060 mol L⁻¹"],
    why="0.040 mol L⁻¹ is the amount that has reacted, not the amount left. 0.140 mol L⁻¹ adds kt. "
        "0.096 mol L⁻¹ uses the first-order equation [R] = [R]₀e^(−kt).",
    ncert=f"{REF8}, integrated rate equations: zero order reactions", seconds=30, checked=True)

add("Rate law and order", B, "direct",
    "At a given temperature, the rate constant of a reaction does NOT depend on:",
    Opts("B", "the concentrations of the reactants", ["the temperature", "the presence of a catalyst",
                                                    "the nature of the reaction"]),
    "Rate versus rate constant",
    "The rate of a reaction changes as the concentrations change, but the rate constant k is fixed for a given "
    "reaction at a given temperature. It changes with temperature (Arrhenius equation) and when a catalyst "
    "provides a path of lower activation energy.",
    ["Rate = k[A]ˣ[B]ʸ: the concentration dependence is in the concentration terms, not in k",
     "k = A e^(−Ea/RT): depends on T and Ea (nature of reaction, catalyst)"],
    why="Temperature, a catalyst and the nature of the reaction all change the value of k.",
    ncert=f"{REF8}, rate expression and rate constant; temperature dependence of the rate of a reaction",
    seconds=25)

add("Arrhenius equation and activation energy", B, "match_list",
    lists("Match List-I (quantity) with List-II (its unit). (Concentrations in mol L⁻¹, time in s.)",
          ["Activation energy, Eₐ", "Pre-exponential factor, A, for a first-order reaction",
           "Rate of a reaction in solution", "Slope of the plot of ln k against 1/T"],
          ["K", "s⁻¹", "J mol⁻¹", "mol L⁻¹ s⁻¹"]),
    match("D", M("III II IV I"), [M("II III IV I"), M("III II I IV"), M("III IV II I")]),
    "Units in chemical kinetics",
    "Eₐ is an energy per mole. A has the same unit as k (s⁻¹ for first order). Rate is a change of "
    "concentration per unit time. The slope of ln k against 1/T is −Eₐ/R, whose unit is (J mol⁻¹)/(J K⁻¹ "
    "mol⁻¹) = K.",
    ["A → III", "B → II", "C → IV", "D → I"],
    why="The wrong codes swap the units of Eₐ and A, of the rate and the slope, or of A and the rate.",
    ncert=f"{REF8}, rate constant; temperature dependence (Arrhenius equation)", seconds=40)

add("Zero and first order reactions", I, "assertion_reason",
    ar("The decomposition of ammonia on a hot platinum surface at high pressure, 2NH₃(g) → N₂(g) + 3H₂(g), is a "
       "zero-order reaction.",
       "At high pressure the metal surface is saturated with ammonia molecules, so increasing the concentration "
       "of ammonia cannot increase the amount adsorbed on the surface, and the rate does not change."),
    AR_, "Zero-order surface reactions",
    "NCERT cites this reaction as zero order: the platinum surface acts as a catalyst, and at high pressure it is "
    "fully covered by gas molecules. The rate depends on the (fixed) amount on the surface, not on the "
    "ammonia concentration in the gas. R explains A.",
    ["A: rate = k[NH₃]⁰ = k → zero order → true", "R: surface saturated → rate independent of [NH₃] → true",
     "R is the cause of the zero order → option A"],
    answer="A",
    why="Both statements are true, and saturation of the catalyst surface is exactly why the order is zero.",
    ncert=f"{REF8}, zero order reactions", seconds=40)

t_i2 = 10 * math.log(1 / 0.64) / math.log(1 / 0.8)
assert close(t_i2, 20) and close(10 * math.log(0.64) / math.log(0.2), 2.77, 0.01)
add("Zero and first order reactions", I, "numerical",
    "A first-order reaction is 20% complete in 10 minutes. The time it takes to be 36% complete is:",
    Opts("C", "20 min", ["18 min", "2.8 min", "40 min"]),
    "Equal fractions react in equal times in a first-order reaction",
    "In each 10-minute interval the same fraction (20%) of the remaining reactant reacts, i.e. 80% is left. "
    "After two such intervals (0.8)² = 0.64 is left, which is 36% completion.",
    ["After 10 min: 0.80 of the reactant left", "After 20 min: 0.80 × 0.80 = 0.64 left → 36% reacted",
     "Check: t = (2.303/k) log(1/0.64) = 2 × (2.303/k) log(1/0.80)"],
    why="18 min scales the time in proportion to the percentage reacted (a zero-order assumption). 2.8 min uses "
        "the fraction reacted instead of the fraction left in the logarithm. 40 min squares the time instead of "
        "the fraction left.",
    ncert=f"{REF8}, integrated rate equations: first order reactions", seconds=70, checked=True)

truth8 = {"a": True, "b": True, "c": False, "d": False}
add("Arrhenius equation and activation energy", I, "multi_statement",
    ms("Which of the following statements about the energy profile of a reaction are correct?",
       ["The activation energy is the energy of the activated complex minus the energy of the reactants.",
        "For an exothermic reaction, the products lie lower in energy than the reactants.",
        "The activated complex is a stable species that can be isolated.",
        "A catalyst changes the enthalpy change of the reaction."]),
    multi("B", truth8, ["(a), (b) and (c) only", "(b) and (d) only", "(a) and (c) only"]),
    "Activated complex, activation energy and the effect of a catalyst",
    "The reaction passes through an unstable, short-lived activated complex at the top of the energy barrier; "
    "the height of this barrier above the reactants is Eₐ. In an exothermic reaction the products end below "
    "the reactants. A catalyst lowers the barrier (provides a new path) but leaves the energies of reactants "
    "and products, and so ΔH, unchanged.",
    ["(a) ✓", "(b) ✓", "(c) ✗ unstable, cannot be isolated", "(d) ✗ ΔH unchanged"],
    why="(c) and (d) are false; every option containing either of them is wrong.",
    ncert=f"{REF8}, temperature dependence of the rate of a reaction; effect of catalyst", seconds=45)

add("Rate law and order", I, "statement_pair",
    sp("The average rate of a reaction over a time interval equals its instantaneous rate at every moment in "
       "that interval.",
       "The rate of a reaction can be expressed as the rate of decrease of the concentration of a reactant, or "
       "the rate of increase of the concentration of a product, each divided by its stoichiometric coefficient."),
    SP_, "Average and instantaneous rates; expressing the rate of a reaction",
    "As reactants are used up the rate usually falls, so the instantaneous rate changes within an interval and "
    "the average rate equals it only at some instant (or when the rate is constant): Statement I is false. "
    "Statement II is how NCERT defines a single rate for a reaction such as 2HI → H₂ + I₂: "
    "rate = −½ d[HI]/dt = d[H₂]/dt = d[I₂]/dt.",
    ["I: instantaneous rate varies within the interval → false", "II: rate = −(1/a)d[A]/dt = (1/p)d[P]/dt → true"],
    answer="D",
    why="Statement I would be true only for a zero-order reaction, not in general.",
    ncert=f"{REF8}, rate of a chemical reaction", seconds=40)

add("Arrhenius equation and activation energy", I, "match_list",
    lists("Match List-I (change made) with List-II (its effect on the rate constant k of a reaction).",
          ["The temperature is raised", "A catalyst is added",
           "The concentration of a reactant is increased at constant temperature",
           "A second reaction with the same A but a higher Eₐ is compared at the same temperature"],
          ["k increases because the activation energy is lowered", "k does not change",
           "k increases because a larger fraction of molecules has energy ≥ Eₐ", "k is smaller"]),
    match("A", M("III I II IV"), [M("I III II IV"), M("III II I IV"), M("III I IV II")]),
    "Factors that change the rate constant",
    "k = A e^(−Eₐ/RT). Raising T increases the fraction e^(−Eₐ/RT) of molecules able to react. A catalyst "
    "provides a path of lower Eₐ. Concentration changes the rate, not k. A higher Eₐ with the same A and T "
    "gives a smaller k.",
    ["A → III", "B → I", "C → II", "D → IV"],
    why="The wrong codes give the catalyst's mechanism to temperature (and vice versa), or claim that "
        "concentration changes k.",
    ncert=f"{REF8}, temperature dependence of the rate; effect of catalyst", seconds=45)

ea_a1 = 19.15 * 1 / (1 / 300 - 1 / 320)
log_ratio = 91.9e3 / 19.15 * (1 / 300 - 1 / 320)
assert close(ea_a1, 91.9e3, 0.001) and close(10 ** log_ratio, 10, 0.01)
add("Arrhenius equation and activation energy", A, "numerical",
    "A reaction has an activation energy of 91.9 kJ mol⁻¹. Assuming the pre-exponential factor does not change, "
    "by about what factor does its rate constant increase when the temperature is raised from 300 K to 320 K? "
    "(2.303R = 19.15 J K⁻¹ mol⁻¹)",
    Opts("C", "10", ["4", "100", "2.7"]),
    "Arrhenius equation at two temperatures",
    "log(k₂/k₁) = [Eₐ/(2.303R)] × (1/T₁ − 1/T₂).",
    ["1/300 − 1/320 = 20/96 000 = 2.083 × 10⁻⁴ K⁻¹",
     "log(k₂/k₁) = (91 900/19.15) × 2.083 × 10⁻⁴ = 4799 × 2.083 × 10⁻⁴ = 1.00", "k₂/k₁ = 10"],
    why="4 applies the rough 'doubling for every 10 K' rule instead of the given Eₐ. 100 takes the logarithm as "
        "2. 2.7 treats the value 1.00 as the natural "
        "logarithm of the ratio (e¹ ≈ 2.7).",
    ncert=f"{REF8}, temperature dependence of the rate of a reaction", seconds=90, checked=True)

k_a2 = (0.80 - 0.20) / 30
t_half_a2 = 0.40 / (2 * k_a2)
assert close(k_a2, 0.020) and close(t_half_a2, 10) and close(0.20 / (2 * k_a2), 5) \
    and close(math.log(2) / (math.log(4) / 30), 15)
add("Half-life", A, "numerical",
    "For a zero-order reaction R → P at a constant temperature, the concentration of R falls from 0.80 mol L⁻¹ "
    "to 0.20 mol L⁻¹ in 30 minutes. The half-life of the same reaction when the initial concentration of R is "
    "0.40 mol L⁻¹ is:",
    Opts("B", "10 min", ["20 min", "15 min", "5 min"]),
    "Half-life of a zero-order reaction, t½ = [R]₀/2k",
    "First find k from the linear fall in concentration, then use the zero-order half-life with the NEW initial "
    "concentration.",
    ["k = (0.80 − 0.20)/30 = 0.020 mol L⁻¹ min⁻¹", "t½ = 0.40/(2 × 0.020) = 10 min"],
    why="20 min leaves out the factor 2 in t½ = [R]₀/2k. 15 min treats the reaction as first order (0.80 → 0.20 "
        "is two half-lives in 30 min). 5 min uses 0.20 mol L⁻¹ as the initial concentration.",
    ncert=f"{REF8}, zero order reactions; half-life of a reaction", seconds=80, checked=True)

add("Arrhenius equation and activation energy", A, "direct",
    "Two reactions have the same pre-exponential factor A, but the activation energy of reaction 1 is larger "
    "than that of reaction 2 (Eₐ₁ > Eₐ₂). Assuming A and Eₐ do not change with temperature, which statement "
    "about their rate constants k₁ and k₂ is correct?",
    Opts("D", "k₁ < k₂ at every temperature, and the ratio k₂/k₁ decreases as the temperature rises",
         ["k₁ < k₂ at every temperature, and the ratio k₂/k₁ increases as the temperature rises",
          "k₁ > k₂ at every temperature",
          "k₁ > k₂ at low temperatures but k₁ < k₂ at high temperatures"]),
    "Comparing rate constants with the Arrhenius equation",
    "k₂/k₁ = e^((Eₐ₁ − Eₐ₂)/RT). The exponent is positive, so k₂ > k₁ at every temperature; as T rises the "
    "exponent becomes smaller, so the ratio falls towards 1. The reaction with the larger Eₐ is the more "
    "sensitive to temperature.",
    ["k₂/k₁ = exp[(Eₐ₁ − Eₐ₂)/RT] > 1 → k₁ < k₂ always",
     "Higher T → smaller exponent → k₂/k₁ decreases (k₁ catches up)"],
    why="The ratio cannot increase with T because the exponent (Eₐ₁ − Eₐ₂)/RT shrinks as T grows. With equal A, "
        "k₁ never exceeds k₂, so the last two options are wrong.",
    ncert=f"{REF8}, temperature dependence of the rate of a reaction", seconds=70)

d8 = {1: (0.1, 0.1, 2.0e-3), 2: (0.3, 0.1, 1.8e-2), 3: (0.1, 0.3, 2.0e-3)}
order_a = round(math.log(d8[2][2] / d8[1][2]) / math.log(3))
order_b = round(math.log(d8[3][2] / d8[1][2]) / math.log(3))
k_d8 = d8[1][2] / (0.1 ** order_a)
truth8a = {"a": order_a == 2, "b": order_b == 0, "c": close(k_d8, 0.20), "d": order_a + order_b == 3,
           "e": close(k_d8 * 0.2 ** 2, 8.0e-3)}
assert truth8a == {"a": True, "b": True, "c": True, "d": False, "e": True}
add("Rate law and order", A, "multi_statement",
    ms("For the reaction A + B → products, the following initial rates were measured at the same temperature:\n"
       "Experiment 1: [A] = 0.10 M, [B] = 0.10 M, rate = 2.0 × 10⁻³ mol L⁻¹ s⁻¹\n"
       "Experiment 2: [A] = 0.30 M, [B] = 0.10 M, rate = 1.8 × 10⁻² mol L⁻¹ s⁻¹\n"
       "Experiment 3: [A] = 0.10 M, [B] = 0.30 M, rate = 2.0 × 10⁻³ mol L⁻¹ s⁻¹\n"
       "Which of the following statements are correct?",
       ["The reaction is second order with respect to A.",
        "The reaction is zero order with respect to B.",
        "The rate constant is 0.20 L mol⁻¹ s⁻¹.",
        "The overall order of the reaction is 3.",
        "When [A] = 0.20 M and [B] = 0.50 M, the rate is 8.0 × 10⁻³ mol L⁻¹ s⁻¹."]),
    multi("C", truth8a, ["(a), (b) and (d) only", "(a), (c), (d) and (e) only", "(b), (c) and (e) only"]),
    "Rate law from initial rates (method of initial rates)",
    "Compare experiments in which only one concentration changes. Tripling [A] multiplies the rate by 9 = 3², "
    "so the order in A is 2. Tripling [B] leaves the rate unchanged, so the order in B is 0. Rate = k[A]².",
    ["(a) 1.8 × 10⁻²/2.0 × 10⁻³ = 9 = 3² → order 2 in A ✓", "(b) rate unchanged → order 0 in B ✓",
     "(c) k = 2.0 × 10⁻³/(0.10)² = 0.20 L mol⁻¹ s⁻¹ ✓", "(d) overall order = 2 + 0 = 2, not 3 ✗",
     "(e) rate = 0.20 × (0.20)² = 8.0 × 10⁻³ mol L⁻¹ s⁻¹ (B has no effect) ✓"],
    why="(d) adds an order of 1 for B, which the data rule out. Options leaving out (a) or (c) are incomplete.",
    ncert=f"{REF8}, factors influencing the rate of a reaction: order of a reaction", seconds=120, checked=True)


# ==================================================================== 9. Classification of Elements and Periodicity
topic("Classification of Elements and Periodicity in Properties")
REF9 = f"{C11}, 'Classification of Elements and Periodicity in Properties'"

add("Valence and reactivity", B, "direct",
    "Using the usual valences of the elements (magnesium 2, nitrogen 3), the formula of the simplest compound "
    "formed between magnesium and nitrogen is predicted to be:",
    Opts("B", "Mg₃N₂", ["Mg₂N₃", "MgN", "MgN₂"]),
    "Predicting formulae from the valences of elements",
    "The valence of a group 2 element is 2 and that of a group 15 element towards a metal is 3 (8 − 5). Cross the "
    "valences: Mg₃N₂ (3 × 2 = 2 × 3).",
    ["Mg: valence 2; N: valence 8 − 5 = 3", "Lowest common multiple 6 → 3 Mg and 2 N → Mg₃N₂"],
    why="Mg₂N₃ swaps the valences. MgN and MgN₂ do not balance the valences of the two elements.",
    ncert=f"{REF9}, periodic trends in chemical properties: periodicity of valence", seconds=25)

add("Modern periodic table", B, "direct",
    "In the modern periodic table, the lanthanoid series consists of the elements with atomic numbers:",
    Opts("A", "58 to 71 (cerium to lutetium)", ["57 to 70", "90 to 103 (thorium to lawrencium)",
                                               "21 to 30 (scandium to zinc)"]),
    "Position of the f-block elements",
    "The lanthanoids are the fourteen elements that follow lanthanum, from cerium (Z = 58) to lutetium "
    "(Z = 71); they are placed separately at the bottom of the table, with the actinoids, thorium (Z = 90) to "
    "lawrencium (Z = 103).",
    ["Lanthanoids: Ce (58) – Lu (71)", "Actinoids: Th (90) – Lr (103)"],
    why="57 to 70 starts at lanthanum and stops before lutetium. 90 to 103 is the actinoid series. 21 to 30 is "
        "the first transition (3d) series.",
    ncert=f"{REF9}, the f-block elements (inner-transition elements)", seconds=25)

add("Modern periodic table", B, "match_list",
    lists("Match List-I (group of the periodic table) with List-II (family name of its elements).",
          ["Group 1", "Group 2", "Group 16", "Group 17"],
          ["Chalcogens", "Halogens", "Alkali metals", "Alkaline earth metals"]),
    match("B", M("III IV I II"), [M("IV III I II"), M("III IV II I"), M("III I IV II")]),
    "Family names of groups in the periodic table",
    "Group 1: alkali metals; group 2: alkaline earth metals; group 16: chalcogens; group 17: halogens; group 18: "
    "noble gases.",
    ["A → III", "B → IV", "C → I", "D → II"],
    why="The wrong codes interchange the alkali and alkaline earth metals, or the chalcogens and halogens.",
    ncert=f"{REF9}, electronic configurations and types of elements: s-, p-, d-, f-blocks", seconds=20)

add("Modern periodic table", I, "statement_pair",
    sp("The elements of group 18 have completely filled valence shells, ns² np⁶ (helium: 1s²).",
       "All the p-block elements are non-metals."),
    SP_, "The p-block and group 18",
    "Group 18 (noble gases) have filled valence shells: Statement I is true. The p-block contains metals (such "
    "as aluminium, tin and lead), metalloids (such as silicon and germanium) and non-metals; non-metallic "
    "character increases from left to right and decreases down a group. Statement II is false.",
    ["I: noble gases ns² np⁶ (He 1s²) → true", "II: p-block has metals, metalloids and non-metals → false"],
    answer="C",
    why="Statement II ignores the metals of the lower left part of the p-block.",
    ncert=f"{REF9}, p-block elements; metals, non-metals and metalloids", seconds=30)

add("Valence and reactivity", I, "assertion_reason",
    ar("Carbon and nitrogen form multiple bonds to themselves (C=C, C≡C, N≡N) much more readily than silicon and "
       "phosphorus do.",
       "Because of their small size, the second-period elements show a greater ability to form pπ–pπ multiple "
       "bonds to themselves and to other second-period elements."),
    AR_, "Anomalous behaviour of the first member of a group",
    "NCERT notes that the first member of each p-block group, being small (with only four valence orbitals and "
    "high electronegativity), differs from the rest of its group; in particular it forms pπ–pπ multiple bonds "
    "with itself (C=C, C≡C, N=N, N≡N) and with other second-period elements (C=O, C≡N, N=O) far more readily "
    "than the later members. R gives this reason for A.",
    ["A: C and N form strong multiple bonds; Si and P much less → true",
     "R: small size → effective sideways p–p overlap → pπ–pπ bonds → true and explains A"],
    answer="A",
    why="Both are true, and the greater pπ–pπ bonding ability of the small second-period atoms is exactly the "
        "cause of A.",
    ncert=f"{REF9}, anomalous properties of second period elements", seconds=45)

truth9 = {"a": True, "b": True, "c": True, "d": False, "e": False}
add("Atomic and ionic radii", I, "multi_statement",
    ms("Which of the following comparisons of size are correct?",
       ["Atomic radius: Be > B", "Ionic radius: Li⁺ < Na⁺", "Radius: S²⁻ > S", "Atomic radius: C < N",
        "Ionic radius: Fe²⁺ < Fe³⁺"]),
    multi("D", truth9, ["(a), (b), (c) and (d) only", "(b), (c) and (e) only", "(a) and (d) only"]),
    "Trends in atomic and ionic radii",
    "Atomic radius falls across a period (Be > B; C > N) and rises down a group (Li⁺ < Na⁺). An anion is larger "
    "than its atom (S²⁻ > S). Removing more electrons from the same atom gives a smaller ion (Fe³⁺ < Fe²⁺).",
    ["(a) across period 2 the radius falls → Be > B ✓", "(b) down group 1 → Li⁺ < Na⁺ ✓", "(c) anion > atom ✓",
     "(d) C (77 pm) > N (74 pm) ✗", "(e) Fe³⁺ < Fe²⁺ ✗"],
    why="(d) reverses the trend across a period and (e) reverses the effect of the ionic charge.",
    ncert=f"{REF9}, atomic radius; ionic radius", seconds=50)

egh = {"Li": -60, "Na": -53, "K": -48}
assert sorted(egh, key=egh.get) == ["Li", "Na", "K"]
add("Ionisation and electron gain enthalpy", I, "direct",
    "Which of the following arranges lithium, sodium and potassium in order from the MOST negative to the LEAST "
    "negative electron gain enthalpy?",
    Opts("B", "Li > Na > K", ["K > Na > Li", "Na > Li > K", "Na > K > Li"]),
    "Variation of electron gain enthalpy down a group",
    "Down a group the size increases and the added electron is farther from the nucleus, so less energy is "
    "released. NCERT's values (kJ mol⁻¹): Li −60, Na −53, K −48.",
    ["Li −60 (most negative) → Na −53 → K −48 (least negative)"],
    why="The other orders place a larger atom before a smaller one, against the trend (and the NCERT values) "
        "for the alkali metals.",
    ncert=f"{REF9}, electron gain enthalpy", seconds=30)

add("Valence and reactivity", A, "assertion_reason",
    ar("The highest valence shown by chlorine in its compounds with oxygen is 1.",
       "Chlorine shows a valence of 1 in its hydride, HCl."),
    AR_, "Periodicity of valence: valence towards hydrogen and towards oxygen",
    "Towards hydrogen a group 17 element shows valence 8 − 7 = 1 (HCl), so R is true. Towards oxygen, however, "
    "chlorine can use all seven valence electrons: its highest valence is 7, as in Cl₂O₇. A is false.",
    ["R: HCl → valence 1 → true", "A: Cl₂O₇ → valence 7 → highest valence is 7, not 1 → false"],
    answer="D",
    why="The valence towards hydrogen (8 − group electrons) and the highest valence towards oxygen (equal to the "
        "number of valence electrons) differ for the p-block non-metals.",
    ncert=f"{REF9}, periodic trends in chemical properties: periodicity of valence", seconds=45)

truth9a = {"a": True, "b": True, "c": True, "d": False, "e": False}
add("Valence and reactivity", A, "multi_statement",
    ms("Which of the following pairs of elements show a diagonal relationship?",
       ["Lithium and magnesium", "Beryllium and aluminium", "Boron and silicon", "Lithium and sodium",
        "Magnesium and aluminium"]),
    multi("A", truth9a, ["(a), (b), (c) and (e) only", "(b), (d) and (e) only", "(a) and (b) only"]),
    "Diagonal relationship of second-period elements",
    "The first members of groups 1, 2 and 13 (Li, Be, B) show many similarities with the SECOND member of the "
    "NEXT group (Mg, Al, Si), lying diagonally below and to the right. Li and Na are in the same group; Mg and "
    "Al are neighbours in the same period.",
    ["(a) Li ↘ Mg ✓", "(b) Be ↘ Al ✓", "(c) B ↘ Si ✓", "(d) same group ✗", "(e) same period ✗"],
    why="Pairs in the same group or the same period are not diagonal pairs; '(a) and (b) only' misses B and Si.",
    ncert=f"{REF9}, anomalous properties of second period elements (diagonal relationship)", seconds=40)

add("Atomic and ionic radii", A, "assertion_reason",
    ar("The Mg²⁺ ion is smaller than the Na⁺ ion.",
       "The Mg²⁺ ion has more electrons than the Na⁺ ion."),
    AR_, "Radii of isoelectronic ions",
    "Na⁺ and Mg²⁺ both have 10 electrons (they are isoelectronic), so R is false. Mg²⁺ has the greater nuclear "
    "charge (+12 against +11) acting on the same number of electrons, so it pulls them closer and is smaller: "
    "A is true.",
    ["Na⁺: 11 − 1 = 10 e⁻; Mg²⁺: 12 − 2 = 10 e⁻ → R false",
     "Same electrons, larger nuclear charge → smaller ion → A true"],
    answer="C",
    why="R is false because the two ions are isoelectronic; the size difference comes from the nuclear charge, "
        "not from the number of electrons.",
    ncert=f"{REF9}, ionic radius (isoelectronic species)", seconds=40)
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
    doc = {"schema_version": "1.0", "batch_id": "BATCH_009", "created_at": TODAY,
           "notes": "Package CHE_009_p1: 123 original Chemistry questions (physical and inorganic chemistry). "
                    "Numerical answers re-derived in tools/batch_009/CHE_009_p1.py.",
           "stimuli": [], "questions": QUESTIONS}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {OUT}: {n} questions; difficulty {dict(Counter(q['difficulty'] for q in QUESTIONS))}; "
          f"formats {dict(fmts)}; keys {dict(sorted(KEYS.items()))}")
