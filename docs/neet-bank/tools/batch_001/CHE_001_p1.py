"""Writes batches/parts/BATCH_001_CHE_p1.json: package CHE_001_p1 of BATCH_001 (Chemistry, 126 questions).

Topics: Some Basic Concepts, Atomic Structure, Chemical Bonding, Thermodynamics, Solutions, Equilibrium,
Redox and Electrochemistry, Chemical Kinetics, Periodicity, p-Block Elements. IDs NEET_CHE_000006..000131.

Every computable answer is re-derived here with an assert before anything is written; the quota per
(topic, difficulty), the ID range, the format mix and the answer-key balance are asserted too.
For flexible formats the correct option is placed at the least-used key so far, so keys stay balanced.

    cd docs/neet-bank && python tools/batch_001/CHE_001_p1.py
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
PACKAGE = "CHE_001_p1"
PLAN = ROOT / "batches" / "plans" / "BATCH_001_plan.json"
OUT = ROOT / "batches" / "parts" / "BATCH_001_CHE_p1.json"
TODAY = "2026-11-16"
LETTERS = "ABCD"
CHE = "Chemistry"
FIRST_ID = 6
AUTHORED = ("ai:author-solve", "ai:self-recheck")
RECOMPUTED = ("script:recompute", "ai:author-solve", "ai:self-recheck")
# The coordinator's separate blind solve covered all 126 questions of the first version. 000087, 000094 and 000128
# were replaced on 2026-11-16 after the syllabus-scope audit and have not been blind-solved yet.
# 000043 was rewritten on 2026-11-18 (final fact audit: IF7/XeF6 replaced by SF4/ClF3) and needs a new blind solve.
REPLACED = {"NEET_CHE_000087", "NEET_CHE_000094", "NEET_CHE_000128", "NEET_CHE_000043"}
BLIND_CHECKED = {f"NEET_CHE_{n:06d}" for n in range(6, 132)} - REPLACED

QUESTIONS = []
KEYS = Counter()
_topic = [None]


def topic(name):
    _topic[0] = name


class Flex:
    """Options whose correct answer can sit at any position: placed at the least-used key so far."""

    def __init__(self, correct, wrong):
        assert len(wrong) == 3 and correct not in wrong and len(set(wrong)) == 3, (correct, wrong)
        self.correct, self.wrong = correct, list(wrong)

    def resolve(self):
        low = min(KEYS[k] for k in LETTERS)
        cands = [k for k in LETTERS if KEYS[k] == low]
        at = cands[len(QUESTIONS) % len(cands)]
        opts = list(self.wrong)
        opts.insert(LETTERS.index(at), self.correct)
        return opts, at


def combo(*labels):
    """'(a), (c) and (e) only' style option text."""
    parts = [f"({x})" for x in labels]
    return (", ".join(parts[:-1]) + " and " + parts[-1] if len(parts) > 1 else parts[0]) + " only"


def multi(truth, correct, wrong):
    """Multi-statement options. truth maps each label to True/False; the correct option must list exactly the true
    ones and no wrong option may."""
    true = sorted(k for k, v in truth.items() if v)
    assert correct == combo(*true), (correct, true)
    assert all(w != correct for w in wrong)
    return Flex(correct, wrong)


def code(m):
    return ", ".join(f"{k}-{m[k]}" for k in "ABCD")


def match(correct, wrong):
    """Match-the-list options from dicts like {'A': 'II', ...}; each numeral used once."""
    for m in [correct, *wrong]:
        assert sorted(m.values()) == sorted(["I", "II", "III", "IV"]), m
    return Flex(code(correct), [code(w) for w in wrong])


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
        assert isinstance(options, Flex) and answer is None
        opts, answer = options.resolve()
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
                         "verified_by": list(RECOMPUTED if checked else AUTHORED)
                         + (["ai:independent-check"] if qid in BLIND_CHECKED else []), "verified_at": TODAY},
    })


def close(x, y, tol=0.005):
    """Relative closeness for rounded option values."""
    return abs(x - y) <= tol * abs(y)


B, I, A = "Basic", "Intermediate", "Advanced"
AR_, SP_ = ASSERTION_REASON, STATEMENT_PAIR
C11, C12 = "Class 11 Chemistry", "Class 12 Chemistry"

# ==================================================================== 1. Some Basic Concepts in Chemistry
topic("Some Basic Concepts in Chemistry")
REF1 = f"{C11}, 'Some Basic Concepts of Chemistry'"
NA = 6.022e23

n_co2 = 4.4 / 44
atoms = n_co2 * 3 * NA
assert close(atoms, 1.807e23) and close(n_co2 * NA, 6.022e22) and close(n_co2 * 2 * NA, 1.204e23)
assert close(3 * NA, 1.807e24)
add("Mole concept", B, "numerical",
    "How many atoms in all are present in 4.4 g of carbon dioxide? (C = 12, O = 16, Nₐ = 6.022 × 10²³ mol⁻¹)",
    Flex("1.807 × 10²³", ["6.022 × 10²²", "1.204 × 10²³", "1.807 × 10²⁴"]),
    "Mole concept: moles = mass / molar mass; atoms = moles of molecules × atoms per molecule × Nₐ",
    "Find the moles of CO₂ first. Each CO₂ molecule has three atoms (one C and two O).",
    ["Molar mass of CO₂ = 12 + 2 × 16 = 44 g mol⁻¹", "Moles of CO₂ = 4.4 / 44 = 0.1 mol",
     "Molecules = 0.1 × 6.022 × 10²³ = 6.022 × 10²²",
     "Atoms = 3 × 6.022 × 10²² = 1.807 × 10²³"],
    why="6.022 × 10²² counts molecules, not atoms. 1.204 × 10²³ counts only the oxygen atoms. 1.807 × 10²⁴ "
        "treats the 4.4 g sample as one mole of CO₂.",
    seconds=40, checked=True)

add("Laws of chemical combination", B, "match_list",
    lists("Match List-I (law) with List-II (scientist who proposed it).",
          ["Law of conservation of mass", "Law of definite proportions", "Law of gaseous volumes",
           "Law of multiple proportions"],
          ["Joseph Proust", "Antoine Lavoisier", "Joseph Gay-Lussac", "John Dalton"]),
    match({"A": "II", "B": "I", "C": "III", "D": "IV"},
          [{"A": "I", "B": "II", "C": "III", "D": "IV"}, {"A": "II", "B": "I", "C": "IV", "D": "III"},
           {"A": "II", "B": "IV", "C": "III", "D": "I"}]),
    "Laws of chemical combination and the scientists who stated them",
    "Lavoisier stated that mass is neither created nor destroyed in a chemical reaction. Proust found that a "
    "given compound always contains the same elements in the same proportion by mass. Gay-Lussac observed that "
    "gases combine in simple whole-number ratios by volume. Dalton proposed the law of multiple proportions.",
    ["Conservation of mass → Lavoisier → II", "Definite proportions → Proust → I",
     "Gaseous volumes → Gay-Lussac → III", "Multiple proportions → Dalton → IV"],
    ncert=f"{REF1}, laws of chemical combinations", seconds=35)

pct_n = F(28, 60) * 100
assert round(float(pct_n), 1) == 46.7 and round(float(F(14, 60) * 100), 1) == 23.3
assert round(float(F(16, 60) * 100), 1) == 26.7 and round(float(F(12, 60) * 100), 1) == 20.0
add("Empirical and molecular formulae", B, "numerical",
    "The percentage by mass of nitrogen in urea, CO(NH₂)₂, is (C = 12, N = 14, O = 16, H = 1):",
    Flex("46.7%", ["23.3%", "26.7%", "20.0%"]),
    "Mass per cent of an element in a compound",
    "Mass per cent = (mass of the element in one mole of the compound / molar mass) × 100. Urea has two "
    "nitrogen atoms per molecule.",
    ["Molar mass of urea = 12 + 16 + 2 × (14 + 2) = 60 g mol⁻¹", "Mass of N per mole = 2 × 14 = 28 g",
     "Mass % of N = 28/60 × 100 = 46.7%"],
    why="23.3% counts only one nitrogen atom. 26.7% is the mass per cent of oxygen and 20.0% that of carbon.",
    seconds=40, checked=True)

n_h2, n_o2 = 4 / 2, 40 / 32
water = min(n_h2, 2 * n_o2) * 18
assert water == 36 and 2 * n_o2 * 18 == 45 and n_h2 < 2 * n_o2
add("Stoichiometry", I, "numerical",
    "4 g of hydrogen gas is mixed with 40 g of oxygen gas and the mixture is exploded. The maximum mass of water "
    "that can be formed is (H = 1, O = 16):",
    Flex("36 g", ["45 g", "44 g", "18 g"]),
    "Limiting reagent",
    "2H₂ + O₂ → 2H₂O. Find which reactant runs out first; it alone decides how much product forms.",
    ["Moles of H₂ = 4/2 = 2 mol; moles of O₂ = 40/32 = 1.25 mol",
     "2 mol H₂ needs only 1 mol O₂, and 1.25 mol is available → H₂ is the limiting reagent",
     "2 mol H₂ gives 2 mol H₂O = 2 × 18 = 36 g (0.25 mol O₂ is left over)"],
    why="45 g takes O₂ as the limiting reagent (1.25 mol O₂ would need 2.5 mol H₂). 44 g simply adds the masses "
        "and ignores the unused oxygen. 18 g wrongly takes 2 mol H₂ to give 1 mol water.",
    seconds=70, checked=True)

ratio_h_c = (14.3 / 1) / (85.7 / 12)
assert round(ratio_h_c) == 2 and 56 // 14 == 4 and 4 * 12 + 8 == 56
add("Empirical and molecular formulae", I, "numerical",
    "A hydrocarbon contains 85.7% carbon and 14.3% hydrogen by mass. Its molar mass is 56 g mol⁻¹. Its "
    "molecular formula is (C = 12, H = 1):",
    Flex("C₄H₈", ["CH₂", "C₂H₄", "C₄H₁₀"]),
    "Empirical formula from mass per cent, then molecular formula from molar mass",
    "Divide each mass per cent by the atomic mass to get relative moles, reduce to the simplest whole-number "
    "ratio, then multiply the empirical formula by n = molar mass / empirical formula mass.",
    ["C: 85.7/12 = 7.14; H: 14.3/1 = 14.3", "Ratio C : H = 7.14 : 14.3 = 1 : 2 → empirical formula CH₂ (mass 14)",
     "n = 56/14 = 4 → molecular formula C₄H₈"],
    why="CH₂ is only the empirical formula. C₂H₄ has the right ratio but a molar mass of 28. C₄H₁₀ has mass 58 and "
        "a C : H ratio of 2 : 5.",
    seconds=75, checked=True)

assert F(1, 32) * 2 == F(1, 48) * 3 == F(1, 16)
add("Mole concept", I, "assertion_reason",
    ar("1 g of O₂ and 1 g of O₃ contain the same number of oxygen atoms.",
       "O₂ and O₃ have the same molar mass."),
    AR_, "Moles of atoms in equal masses of allotropes",
    "Both samples are made only of oxygen atoms, so equal masses contain equal numbers of oxygen atoms: 1 g "
    "contains 1/16 mol of O atoms either way. A is true. The molar masses are different (32 and 48 g mol⁻¹), so R "
    "is false.",
    ["O₂: 1/32 mol molecules × 2 = 1/16 mol O atoms", "O₃: 1/48 mol molecules × 3 = 1/16 mol O atoms → A true",
     "Molar mass of O₂ = 32 g mol⁻¹, of O₃ = 48 g mol⁻¹ → R false"],
    answer="C", why="The numbers of molecules differ (O₂ has more molecules); only the numbers of atoms are equal.",
    seconds=45, checked=True)

e_mass_mg = 9.11e-31 * NA * 1e6
assert round(e_mass_mg, 2) == 0.55
add("Mole concept", I, "statement_pair",
    sp("One mole of water contains 6.022 × 10²³ atoms.",
       "The mass of one mole of electrons is about 0.55 mg (mass of an electron = 9.11 × 10⁻³¹ kg, "
       "Nₐ = 6.022 × 10²³ mol⁻¹)."),
    SP_, "Counting particles in a mole",
    "One mole of water contains 6.022 × 10²³ molecules. Each molecule has three atoms, so it contains "
    "3 × 6.022 × 10²³ = 1.807 × 10²⁴ atoms: Statement I is false. One mole of electrons has a mass of "
    "9.11 × 10⁻³¹ × 6.022 × 10²³ = 5.49 × 10⁻⁷ kg = 0.55 mg: Statement II is true.",
    ["1 mol H₂O = Nₐ molecules = 3Nₐ atoms → Statement I false",
     "Mass of 1 mol e⁻ = 9.11 × 10⁻³¹ kg × 6.022 × 10²³ = 5.49 × 10⁻⁷ kg ≈ 0.55 mg → Statement II true"],
    answer="D", seconds=50, checked=True)

pure = 25 * 0.80
n_caco3 = pure / 100
cao = n_caco3 * 56
assert close(cao, 11.2) and close(25 / 100 * 56, 14.0) and close(n_caco3 * 44, 8.8) and close(25 - 8.8, 16.2)
add("Stoichiometry", A, "numerical",
    "25 g of a limestone sample containing 80% CaCO₃ by mass (the rest being inert, non-volatile impurities) is "
    "heated strongly until no more CO₂ is given off: CaCO₃ → CaO + CO₂. The mass of CaO formed is "
    "(Ca = 40, C = 12, O = 16):",
    Flex("11.2 g", ["14.0 g", "8.8 g", "16.2 g"]),
    "Stoichiometry with an impure reactant",
    "Only the CaCO₃ in the sample decomposes. Find its moles, then use the 1 : 1 mole ratio with CaO.",
    ["Mass of CaCO₃ = 80% of 25 g = 20 g", "Moles of CaCO₃ = 20/100 = 0.2 mol",
     "Moles of CaO = 0.2 mol → mass = 0.2 × 56 = 11.2 g"],
    why="14.0 g ignores the impurity and treats all 25 g as CaCO₃. 8.8 g is the mass of CO₂ given off. 16.2 g is "
        "the mass of the whole residue (CaO plus 5 g of impurity), not of CaO alone.",
    seconds=90, checked=True)

n_c = 13.2 / 44 / 0.1
n_h = 2 * (5.4 / 18) / 0.1
assert round(n_c) == 3 and round(n_h) == 6
add("Empirical and molecular formulae", A, "numerical",
    "Complete combustion of 0.1 mol of a hydrocarbon gives 13.2 g of CO₂ and 5.4 g of H₂O. The molecular formula "
    "of the hydrocarbon is (C = 12, H = 1, O = 16):",
    Flex("C₃H₆", ["C₃H₃", "C₃H₈", "CH₂"]),
    "Molecular formula from combustion data",
    "All the carbon of the hydrocarbon ends up in CO₂ and all its hydrogen in H₂O. Each H₂O carries two H atoms.",
    ["Moles of CO₂ = 13.2/44 = 0.3 mol → 0.3 mol C from 0.1 mol compound → 3 C per molecule",
     "Moles of H₂O = 5.4/18 = 0.3 mol → 0.6 mol H → 6 H per molecule",
     "Molecular formula = C₃H₆"],
    why="C₃H₃ forgets that each water molecule has two hydrogen atoms. C₃H₈ assumes the compound is an alkane "
        "instead of using the data. CH₂ is only the empirical formula; the moles of compound fix the molecular "
        "formula.",
    seconds=90, checked=True)

mol_atoms = {"a": 12 / 12, "b": 9 / 18 * 3, "c": 4 / 4, "d": 8 / 32 * 2, "e": 14 / 28 * 2}
truth = {k: math.isclose(v, 1.0) for k, v in mol_atoms.items()}
add("Mole concept", A, "multi_statement",
    ms("Which of the following samples contain exactly one mole of atoms (6.022 × 10²³ atoms)? "
       "(H = 1, He = 4, C = 12, N = 14, O = 16)",
       ["12 g of carbon-12", "9 g of water", "4 g of helium", "8 g of oxygen gas (O₂)", "14 g of nitrogen gas (N₂)"]),
    multi(truth, "(a), (c) and (e) only", ["(a), (b) and (c) only", "(a) and (c) only", "(c), (d) and (e) only"]),
    "Moles of atoms = moles of molecules × atoms per molecule",
    "Convert each mass to moles of the species, then multiply by the number of atoms in each species.",
    ["(a) 12/12 = 1 mol C atoms → yes", "(b) 9/18 = 0.5 mol H₂O × 3 = 1.5 mol atoms → no",
     "(c) 4/4 = 1 mol He atoms (monatomic) → yes", "(d) 8/32 = 0.25 mol O₂ × 2 = 0.5 mol atoms → no",
     "(e) 14/28 = 0.5 mol N₂ × 2 = 1 mol atoms → yes"],
    why="Nitrogen gas is diatomic, so 14 g (half a mole of N₂) still gives one mole of atoms; water has three atoms "
        "per molecule, so 9 g gives 1.5 mol of atoms.",
    seconds=90, checked=True)

# ==================================================================== 2. Atomic Structure
topic("Atomic Structure")
REF2 = f"{C11}, 'Structure of Atom'"

add("Quantum numbers and orbitals", B, "direct",
    "Which of the following sets of quantum numbers (n, l, mₗ, mₛ) is NOT possible for an electron in an atom?",
    Flex("n = 2, l = 2, mₗ = +1, mₛ = +½",
         ["n = 2, l = 1, mₗ = 0, mₛ = +½", "n = 3, l = 2, mₗ = −2, mₛ = −½", "n = 4, l = 0, mₗ = 0, mₛ = −½"]),
    "Allowed values of quantum numbers",
    "l can take values 0 to (n − 1), mₗ from −l to +l, and mₛ is +½ or −½. For n = 2, l can only be 0 or 1.",
    ["n = 2, l = 2: l must be less than n → not allowed",
     "n = 2, l = 1, mₗ = 0: a 2p electron → allowed", "n = 3, l = 2, mₗ = −2: a 3d electron → allowed",
     "n = 4, l = 0, mₗ = 0: a 4s electron → allowed"],
    ncert=f"{REF2}, quantum numbers", seconds=30)

add("Electronic configuration", B, "direct",
    "The ground-state electronic configuration of the Fe²⁺ ion (Z of Fe = 26) is:",
    Flex("[Ar] 3d⁶", ["[Ar] 3d⁴ 4s²", "[Ar] 3d⁵ 4s¹", "[Ar] 3d⁶ 4s²"]),
    "Electronic configuration of transition-metal cations",
    "Fe is [Ar] 3d⁶ 4s². When a transition metal forms a cation, the 4s electrons are removed before the 3d "
    "electrons.",
    ["Fe (26): [Ar] 3d⁶ 4s²", "Remove two electrons, both from 4s", "Fe²⁺: [Ar] 3d⁶"],
    why="[Ar] 3d⁴ 4s² removes the electrons from 3d instead of 4s. [Ar] 3d⁶ 4s² is neutral Fe. [Ar] 3d⁵ 4s¹ has "
        "the right count but a wrong distribution for the ion.",
    seconds=30)

r_he = 52.9 * 2 ** 2 / 2
assert close(r_he, 105.8) and close(52.9 * 2 / 2, 52.9) and close(52.9 * 4, 211.6) and close(52.9 * 4 * 2, 423.2)
add("Bohr model and hydrogen spectrum", B, "numerical",
    "Using Bohr's model, the radius of the second orbit (n = 2) of the He⁺ ion is (radius of the first Bohr "
    "orbit of hydrogen = 52.9 pm):",
    Flex("105.8 pm", ["52.9 pm", "211.6 pm", "423.2 pm"]),
    "Radius of a Bohr orbit for a hydrogen-like species: rₙ = 52.9 n²/Z pm",
    "The radius grows as n² and shrinks as the nuclear charge Z grows. He⁺ has Z = 2 and one electron.",
    ["rₙ = 52.9 × n²/Z pm", "For n = 2, Z = 2: r = 52.9 × 4/2 = 105.8 pm"],
    why="52.9 pm uses n instead of n². 211.6 pm ignores Z. 423.2 pm multiplies by Z instead of dividing.",
    ncert=f"{REF2}, Bohr's model for hydrogen atom", seconds=35, checked=True)

add("Dual nature and uncertainty", B, "statement_pair",
    sp("The de Broglie wavelength of a moving particle is inversely proportional to its momentum.",
       "The Heisenberg uncertainty principle has a significant effect on the motion of macroscopic objects such "
       "as a cricket ball."),
    SP_, "de Broglie relation and the uncertainty principle",
    "λ = h/p = h/mv, so the wavelength is inversely proportional to momentum: Statement I is true. Because h is "
    "so small, the uncertainties for objects of ordinary mass are negligible; the principle matters only for "
    "microscopic particles such as electrons: Statement II is false.",
    ["λ = h/mv → λ ∝ 1/p → Statement I true",
     "Δx·Δv ≥ h/4πm: for m of about 0.1 kg the product is negligible → Statement II false"],
    answer="C", ncert=f"{REF2}, dual behaviour of matter and Heisenberg's uncertainty principle", seconds=35)

inv = lambda lo, hi: F(1, lo * lo) - F(1, hi * hi)
ratio = inv(1, 2) / inv(2, 3)  # lambda_Balmer / lambda_Lyman = (1/λL)/(1/λB)
assert ratio == F(27, 5)
add("Bohr model and hydrogen spectrum", I, "numerical",
    "The ratio of the wavelength of the first line of the Balmer series to that of the first line of the Lyman "
    "series in the hydrogen spectrum is:",
    Flex("27 : 5", ["5 : 27", "9 : 4", "4 : 1"]),
    "Rydberg formula: 1/λ = R_H (1/n₁² − 1/n₂²)",
    "The first line of a series is the transition from the next higher level: 3 → 2 for Balmer, 2 → 1 for Lyman. "
    "Wavelength is inversely proportional to (1/n₁² − 1/n₂²).",
    ["Balmer first line (3 → 2): 1/4 − 1/9 = 5/36", "Lyman first line (2 → 1): 1 − 1/4 = 3/4",
     "λ_B/λ_L = (3/4)/(5/36) = 27/5"],
    why="5 : 27 is the ratio of the wave numbers (or frequencies), the inverse of what is asked. 9 : 4 and 4 : 1 "
        "compare squares of single quantum numbers instead of energy differences.",
    ncert=f"{REF2}, line spectrum of hydrogen", seconds=70, checked=True)

lam_a, lam_b, m_a, m_b = 1, 2, 4, 1
v_ratio = F(1, m_a * lam_a) / F(1, m_b * lam_b)
assert v_ratio == F(1, 2)
add("Dual nature and uncertainty", I, "numerical",
    "Particle P has four times the mass of particle Q. Their de Broglie wavelengths are in the ratio "
    "λ_P : λ_Q = 1 : 2. The ratio of their speeds v_P : v_Q is:",
    Flex("1 : 2", ["2 : 1", "1 : 8", "8 : 1"]),
    "de Broglie relation λ = h/mv",
    "Rearranged, v = h/(mλ), so speed is inversely proportional to the product of mass and wavelength.",
    ["v = h/(mλ) → v_P/v_Q = (m_Q λ_Q)/(m_P λ_P)", "= (1 × 2)/(4 × 1) = 1/2", "v_P : v_Q = 1 : 2"],
    why="2 : 1 inverts the answer. 1 : 8 and 8 : 1 multiply the mass ratio by the wavelength ratio instead of "
        "letting them act in opposite directions.",
    seconds=60, checked=True)

nodes = {o: (n - l - 1, l) for o, n, l in [("2s", 2, 0), ("3p", 3, 1), ("3d", 3, 2), ("4s", 4, 0)]}
right = {"I": (0, 2), "II": (3, 0), "III": (1, 0), "IV": (1, 1)}
got = {k: next(r for r, v in right.items() if v == nodes[o]) for k, o in zip("ABCD", ["2s", "3p", "3d", "4s"])}
assert got == {"A": "III", "B": "IV", "C": "I", "D": "II"}
add("Quantum numbers and orbitals", I, "match_list",
    lists("Match List-I (orbital) with List-II (numbers of radial and angular nodes).",
          ["2s", "3p", "3d", "4s"],
          ["0 radial, 2 angular", "3 radial, 0 angular", "1 radial, 0 angular", "1 radial, 1 angular"]),
    match(got, [{"A": "IV", "B": "III", "C": "I", "D": "II"}, {"A": "III", "B": "IV", "C": "II", "D": "I"},
                {"A": "II", "B": "IV", "C": "I", "D": "III"}]),
    "Nodes of an orbital",
    "An orbital has (n − l − 1) radial nodes and l angular nodes, so (n − 1) nodes in all.",
    ["2s: n − l − 1 = 1 radial, l = 0 angular → III", "3p: 1 radial, 1 angular → IV",
     "3d: 0 radial, 2 angular → I", "4s: 3 radial, 0 angular → II"],
    ncert=f"{REF2}, shapes of atomic orbitals", seconds=50, checked=True)

add("Electronic configuration", I, "multi_statement",
    ms("Which of the following statements are correct?",
       ["No two electrons in an atom can have the same set of all four quantum numbers.",
        "Pairing of electrons in orbitals of equal energy (such as the three p orbitals) does not take place "
        "until each of them has one electron.",
        "The total number of orbitals in a shell with principal quantum number n is n².",
        "A single 2p orbital can hold up to six electrons.",
        "The (n + l) value of a 4s orbital is greater than that of a 3d orbital."]),
    multi({"a": True, "b": True, "c": True, "d": False, "e": False}, "(a), (b) and (c) only",
          ["(a), (b), (c) and (e) only", "(b), (c) and (d) only", "(a) and (d) only"]),
    "Pauli exclusion principle, Hund's rule and orbital counting",
    "(a) is the Pauli exclusion principle and (b) is Hund's rule of maximum multiplicity. A shell n has n² "
    "orbitals. Any one orbital holds at most two electrons; six is the capacity of the whole 2p subshell. For 4s, "
    "n + l = 4 + 0 = 4; for 3d it is 3 + 2 = 5, which is why 4s fills first.",
    ["(a) True: Pauli exclusion principle", "(b) True: Hund's rule", "(c) True: n = 3 has 1 + 3 + 5 = 9 = 3² orbitals",
     "(d) False: one orbital holds at most 2 electrons", "(e) False: 4s has n + l = 4, 3d has n + l = 5"],
    ncert=f"{REF2}, filling of orbitals in atoms", seconds=60)

add("Electronic configuration", I, "assertion_reason",
    ar("The ground-state electronic configuration of copper (Z = 29) is [Ar] 3d¹⁰ 4s¹ and not [Ar] 3d⁹ 4s².",
       "Completely filled and exactly half-filled subshells have extra stability because of their symmetrical "
       "distribution and larger exchange energy."),
    AR_, "Stability of completely filled and half-filled subshells",
    "Moving one electron from 4s to 3d gives copper a completely filled 3d¹⁰ subshell. Such subshells (and "
    "half-filled ones) are extra stable because of symmetry and larger exchange energy. R is true and is exactly "
    "why A is true.",
    ["Expected by the Aufbau order: [Ar] 3d⁹ 4s²", "Observed: [Ar] 3d¹⁰ 4s¹ (filled 3d subshell)",
     "Reason: symmetry and exchange energy stabilise d¹⁰ → R explains A"],
    answer="A", ncert=f"{REF2}, stability of completely filled and half-filled subshells", seconds=40)

h, me = 6.626e-34, 9.11e-31
dv = h / (4 * math.pi * me * 1e-10)
assert close(dv, 5.79e5) and close(h / (me * 1e-10), 7.27e6) and close(h / (2 * math.pi * me * 1e-10), 1.16e6)
assert close(h / (4 * math.pi * me * 1e-9), 5.79e4)
add("Dual nature and uncertainty", A, "numerical",
    "The uncertainty in the position of an electron is 0.1 nm. The minimum uncertainty in its velocity is "
    "(h = 6.626 × 10⁻³⁴ J s, mass of electron = 9.11 × 10⁻³¹ kg):",
    Flex("5.79 × 10⁵ m s⁻¹", ["7.27 × 10⁶ m s⁻¹", "1.16 × 10⁶ m s⁻¹", "5.79 × 10⁴ m s⁻¹"]),
    "Heisenberg's uncertainty principle: Δx · m Δv ≥ h/4π",
    "Convert Δx to metres and rearrange for the smallest Δv.",
    ["Δx = 0.1 nm = 1 × 10⁻¹⁰ m", "Δv = h/(4π m Δx) = 6.626 × 10⁻³⁴ / (4 × 3.1416 × 9.11 × 10⁻³¹ × 10⁻¹⁰)",
     "= 6.626 × 10⁻³⁴ / 1.145 × 10⁻³⁹ = 5.79 × 10⁵ m s⁻¹"],
    why="7.27 × 10⁶ leaves out 4π. 1.16 × 10⁶ uses h/2π instead of h/4π. 5.79 × 10⁴ takes Δx as 1 nm.",
    ncert=f"{REF2}, Heisenberg's uncertainty principle", seconds=100, checked=True)

lines = [(hi, lo) for hi in range(2, 6) for lo in range(1, hi)]
balmer = [x for x in lines if x[1] == 2]
assert len(lines) == 10 == 5 * 4 // 2 and len(balmer) == 3
add("Bohr model and hydrogen spectrum", A, "numerical",
    "In a sample of hydrogen atoms, electrons are excited to the n = 5 level. When they return to the ground "
    "state by all possible routes, how many different spectral lines can appear in all, and how many of them "
    "belong to the Balmer series?",
    Flex("10 lines in all, 3 of them in the Balmer series",
         ["10 lines in all, 4 of them in the Balmer series", "4 lines in all, 1 of them in the Balmer series",
          "15 lines in all, 3 of them in the Balmer series"]),
    "Number of spectral lines from level n: n(n − 1)/2",
    "Every pair of levels from 1 to 5 gives one line. The Balmer series contains only the transitions that end "
    "on n = 2.",
    ["Total lines = n(n − 1)/2 = 5 × 4/2 = 10", "Balmer lines end on n = 2: 5 → 2, 4 → 2, 3 → 2 → 3 lines"],
    why="4 Balmer lines wrongly counts 2 → 1 (a Lyman line) or a 6 → 2 line that cannot occur here. 4 lines in all "
        "is the most one single atom can emit (n − 1), not a whole sample. 15 uses n(n + 1)/2.",
    seconds=80, checked=True)

ie = 13.6 * 3 ** 2 / 2 ** 2
assert close(ie, 30.6) and close(13.6 * 9, 122.4) and close(13.6 * 3 / 4, 10.2) and close(13.6 * 9 / 2, 61.2)
add("Bohr model and hydrogen spectrum", A, "numerical",
    "The ionisation energy of a hydrogen atom in its ground state is 13.6 eV. The energy needed to remove the "
    "electron from the n = 2 level of the Li²⁺ ion (Z = 3) is:",
    Flex("30.6 eV", ["122.4 eV", "10.2 eV", "61.2 eV"]),
    "Energy of a level in a hydrogen-like species: Eₙ = −13.6 Z²/n² eV",
    "Removing the electron from level n needs energy equal to |Eₙ|.",
    ["|E₂| for Li²⁺ = 13.6 × Z²/n² = 13.6 × 9/4", "= 30.6 eV"],
    why="122.4 eV is the ionisation energy from n = 1. 10.2 eV uses Z instead of Z². 61.2 eV uses n instead of n².",
    ncert=f"{REF2}, Bohr's model for hydrogen atom", seconds=60, checked=True)

add("Quantum numbers and orbitals", A, "assertion_reason",
    ar("In a hydrogen atom, the 2s orbital is lower in energy than the 2p orbital.",
       "In atoms with more than one electron, the energy of an orbital depends on both n and l."),
    AR_, "Energies of orbitals in hydrogen and in multi-electron atoms",
    "In the hydrogen atom, the energy of an orbital depends only on n, so 2s and 2p are degenerate: A is false. "
    "In multi-electron atoms, electron–electron repulsion and shielding make the energy depend on both n and l "
    "(2s < 2p): R is true.",
    ["Hydrogen: energy depends on n only → 2s = 2p → A false",
     "Multi-electron atoms: energy depends on n and l → R true"],
    answer="D", why="The trap is to apply the multi-electron order (2s < 2p) to hydrogen.",
    ncert=f"{REF2}, energies of orbitals", seconds=40)

# ==================================================================== 3. Chemical Bonding and Molecular Structure
topic("Chemical Bonding and Molecular Structure")
REF3 = f"{C11}, 'Chemical Bonding and Molecular Structure'"


def mo(electrons, light=True):
    """(bond order, unpaired electrons) for a homonuclear second-period diatomic species.
    light=True: B2, C2, N2 order (pi2p below sigma2p); False: O2, F2 order."""
    s = [("s1", 2, 1), ("s1*", 2, -1), ("s2", 2, 1), ("s2*", 2, -1)]
    p = [("pi", 4, 1), ("s2p", 2, 1)] if light else [("s2p", 2, 1), ("pi", 4, 1)]
    levels = s + p + [("pi*", 4, -1), ("s2p*", 2, -1)]
    nb = na = unpaired = 0
    left = electrons
    for name, cap, sign in levels:
        e = min(cap, left)
        left -= e
        nb, na = (nb + e, na) if sign > 0 else (nb, na + e)
        unpaired += (e if e <= 2 else 4 - e) if cap == 4 else e % 2
    return F(nb - na, 2), unpaired


assert mo(16, False) == (2, 2) and mo(14) == (3, 0) and mo(15, False) == (F(5, 2), 1) and mo(18, False) == (1, 0)
assert mo(13) == (F(5, 2), 1) and mo(15) == (F(5, 2), 1) and mo(12) == (2, 0)

add("VSEPR shapes", B, "direct",
    "The shape of the ClF₃ molecule is:",
    Flex("T-shaped", ["Trigonal planar", "Trigonal pyramidal", "See-saw"]),
    "VSEPR theory: 3 bond pairs and 2 lone pairs",
    "Cl has 7 valence electrons; 3 form bonds with F and 4 remain as 2 lone pairs. Five electron pairs take a "
    "trigonal bipyramidal arrangement with both lone pairs equatorial, leaving a T shape.",
    ["Cl: 7 valence electrons → 3 bond pairs + 2 lone pairs = 5 pairs",
     "Lone pairs occupy equatorial positions to reduce lone pair–lone pair repulsion",
     "The three F atoms and Cl form a T shape"],
    why="Trigonal planar needs 3 bond pairs and no lone pair (BF₃). Trigonal pyramidal needs 3 bond pairs and 1 "
        "lone pair (NH₃). See-saw needs 4 bond pairs and 1 lone pair (SF₄).",
    ncert=f"{REF3}, VSEPR theory", seconds=35)

add("Hybridisation and resonance", B, "direct",
    "In which of the following molecules is the central atom sp hybridised?",
    Flex("BeCl₂", ["BCl₃", "H₂O", "CH₄"]),
    "Hybridisation from the number of electron pairs around the central atom",
    "Be in BeCl₂ forms two bonds and has no lone pair, so one 2s and one 2p orbital mix to give two sp hybrid "
    "orbitals at 180°: the molecule is linear.",
    ["BeCl₂: 2 bond pairs, 0 lone pairs → sp, linear", "BCl₃: 3 bond pairs → sp²",
     "H₂O: 2 bond pairs + 2 lone pairs → sp³", "CH₄: 4 bond pairs → sp³"],
    ncert=f"{REF3}, hybridisation", seconds=30)

add("Molecular orbital theory", B, "assertion_reason",
    ar("The O₂ molecule is paramagnetic.", "The O₂ molecule contains an even number of electrons."),
    AR_, "Magnetic behaviour from molecular orbital theory",
    "O₂ has 16 electrons, an even number, so R is true. But an even total does not decide magnetism: in O₂ the "
    "last two electrons go singly into the two degenerate π*2p orbitals (Hund's rule), giving two unpaired "
    "electrons, so O₂ is paramagnetic. A is true, but R does not explain it.",
    ["O₂: KK σ2s² σ*2s² σ2p_z² π2p_x² π2p_y² π*2p_x¹ π*2p_y¹", "Two unpaired electrons → paramagnetic → A true",
     "16 electrons is even → R true, but it is the unpaired π* electrons that cause paramagnetism"],
    answer="B", why="Option A is the trap: an even electron count would, if anything, suggest diamagnetism.",
    ncert=f"{REF3}, bonding in some homonuclear diatomic molecules", seconds=45, checked=True)

add("Ionic bonding and lattice enthalpy", B, "statement_pair",
    sp("Formation of an ionic bond is favoured by a high ionisation enthalpy of the metal atom.",
       "Lattice enthalpy of an ionic solid is the energy required to completely separate one mole of the solid "
       "into its gaseous ions."),
    SP_, "Factors favouring ionic bonding; lattice enthalpy",
    "An ionic bond forms more easily when the metal loses electrons easily (low ionisation enthalpy) and the "
    "non-metal gains them readily: Statement I is false. Statement II is the definition of lattice enthalpy.",
    ["Low ionisation enthalpy of the metal favours cation formation → Statement I false",
     "Lattice enthalpy: solid → gaseous ions, per mole → Statement II true"],
    answer="D", ncert=f"{REF3}, ionic or electrovalent bond and lattice enthalpy", seconds=35)

add("Fajans' rule and dipole moment", B, "direct",
    "Which of the following molecules has zero dipole moment?",
    Flex("BF₃", ["NH₃", "H₂O", "NF₃"]),
    "Dipole moment depends on bond polarity and molecular geometry",
    "BF₃ is trigonal planar and symmetrical; the three B–F bond dipoles are at 120° and cancel.",
    ["BF₃: trigonal planar, bond dipoles cancel → μ = 0", "NH₃ and NF₃: pyramidal → net dipole",
     "H₂O: bent → net dipole"],
    ncert=f"{REF3}, polarity of bonds", seconds=30)

bo = {"N₂": mo(14)[0], "O₂": mo(16, False)[0], "O₂⁺": mo(15, False)[0], "O₂²⁻": mo(18, False)[0]}
num = {"I": 1, "II": 2, "III": F(5, 2), "IV": 3}
got = {k: next(r for r, v in num.items() if v == bo[s]) for k, s in zip("ABCD", bo)}
assert got == {"A": "IV", "B": "II", "C": "III", "D": "I"}
add("Molecular orbital theory", I, "match_list",
    lists("Match List-I (species) with List-II (bond order from molecular orbital theory).",
          ["N₂", "O₂", "O₂⁺", "O₂²⁻"], ["1", "2", "2.5", "3"]),
    match(got, [{"A": "IV", "B": "III", "C": "II", "D": "I"}, {"A": "III", "B": "II", "C": "IV", "D": "I"},
                {"A": "IV", "B": "II", "C": "I", "D": "III"}]),
    "Bond order = ½ (Nb − Na)",
    "Fill the molecular orbitals with all the electrons of the species and count bonding (Nb) and antibonding "
    "(Na) electrons. Valence-shell counting gives the same result.",
    ["N₂ (14 e⁻): Nb = 10, Na = 4 → 3 → IV", "O₂ (16 e⁻): Nb = 10, Na = 6 → 2 → II",
     "O₂⁺ (15 e⁻): Nb = 10, Na = 5 → 2.5 → III", "O₂²⁻ (18 e⁻): Nb = 10, Na = 8 → 1 → I"],
    shortcut="Removing an electron from O₂ (from π*) raises the bond order by ½; adding one lowers it by ½.",
    ncert=f"{REF3}, bond order", seconds=60, checked=True)

add("VSEPR shapes", I, "assertion_reason",
    ar("The H–N–H bond angle in NH₃ (about 107°) is smaller than the H–C–H bond angle in CH₄ (109.5°).",
       "Lone pair–bond pair repulsion is stronger than bond pair–bond pair repulsion."),
    AR_, "VSEPR: order of electron-pair repulsions",
    "Both molecules have four electron pairs around the central atom. In NH₃ one of them is a lone pair, which "
    "repels the bond pairs more strongly than they repel each other, squeezing the H–N–H angle below the "
    "tetrahedral value. R is true and explains A.",
    ["CH₄: 4 bond pairs → regular tetrahedron, 109.5°", "NH₃: 3 bond pairs + 1 lone pair",
     "lp–bp > bp–bp repulsion → angle reduced to about 107°"],
    answer="A", ncert=f"{REF3}, VSEPR theory", seconds=40)

pairs = {"a": (6, 0), "b": (5, 0), "c": (5, 1), "d": (4, 1), "e": (6, 0)}  # (bond pairs, lone pairs)
truth = {k: bp + lp == 6 for k, (bp, lp) in pairs.items()}
add("Hybridisation and resonance", I, "multi_statement",
    ms("In which of the following species is the central atom sp³d² hybridised?",
       ["SF₆", "PCl₅", "IF₅", "SF₄", "[SiF₆]²⁻"]),
    multi(truth, "(a), (c) and (e) only", ["(a), (b) and (c) only", "(a) and (c) only", "(b), (d) and (e) only"]),
    "Hybridisation from the number of electron pairs (bond pairs + lone pairs)",
    "Six electron pairs around the central atom need six hybrid orbitals: sp³d². Five pairs need sp³d.",
    ["(a) SF₆: 6 bond pairs → sp³d²", "(b) PCl₅: 5 bond pairs → sp³d",
     "(c) IF₅: 5 bond pairs + 1 lone pair → sp³d² (square pyramidal)",
     "(d) SF₄: 4 bond pairs + 1 lone pair → sp³d", "(e) [SiF₆]²⁻: 6 bond pairs → sp³d²"],
    why="IF₅ is easy to miss: its lone pair counts as the sixth electron pair.",
    seconds=60, checked=True)

add("Fajans' rule and dipole moment", I, "statement_pair",
    sp("NF₃ has a much smaller dipole moment than NH₃, although both molecules are pyramidal.",
       "In NH₃ the orbital dipole of the lone pair is in the same direction as the resultant of the N–H bond "
       "dipoles, whereas in NF₃ it is opposite to the resultant of the N–F bond dipoles."),
    SP_, "Dipole moment as a vector sum including the lone pair",
    "In NH₃, N is more electronegative than H, so the bond dipoles point towards N, the same way as the lone "
    "pair: they add. In NF₃, F is more electronegative than N, so the bond dipoles point away from N, opposing "
    "the lone pair: they partly cancel. Both statements are true (and II explains I).",
    ["NH₃: bond dipoles towards N + lone pair → add → larger μ (about 1.47 D)",
     "NF₃: bond dipoles towards F oppose the lone pair → smaller μ (about 0.23 D)"],
    answer="A", ncert=f"{REF3}, polarity of bonds", seconds=45)

add("Hydrogen and metallic bonding", I, "assertion_reason",
    ar("o-Nitrophenol is steam volatile, whereas p-nitrophenol is not.",
       "o-Nitrophenol has intramolecular hydrogen bonding, whereas p-nitrophenol molecules are associated "
       "through intermolecular hydrogen bonding."),
    AR_, "Intramolecular versus intermolecular hydrogen bonding",
    "In o-nitrophenol the –OH and –NO₂ groups are next to each other and form a hydrogen bond within the same "
    "molecule, so the molecules do not associate and the compound is volatile. In p-nitrophenol the groups are "
    "far apart, so hydrogen bonds form between molecules; the association lowers volatility. R explains A.",
    ["ortho: intramolecular H-bond → no association → steam volatile",
     "para: intermolecular H-bonds → associated molecules → less volatile"],
    answer="A", ncert=f"{C12}, 'Alcohols, Phenols and Ethers', physical properties of phenols", seconds=40)

add("Hybridisation and resonance", I, "statement_pair",
    sp("The two O–O bonds in ozone have the same length (128 pm), which lies between the O–O single bond "
       "(148 pm) and the O=O double bond (121 pm) lengths.",
       "The ozone molecule keeps switching rapidly between its two canonical (resonance) structures."),
    SP_, "Resonance: the resonance hybrid is the real structure",
    "Experiment shows both O–O bonds in O₃ are equal and intermediate between single and double bonds: "
    "Statement I is true. The canonical forms are only ways of writing the structure; they have no real "
    "existence and the molecule does not oscillate between them: Statement II is false.",
    ["Equal O–O bonds of 128 pm → resonance hybrid → Statement I true",
     "Canonical structures do not exist on their own; there is no switching → Statement II false"],
    answer="C", ncert=f"{REF3}, resonance structures", seconds=40)

fc_n = 5 - 0 - 8 // 2
assert fc_n == 1
add("Hybridisation and resonance", I, "numerical",
    "In a Lewis structure of the nitrate ion (NO₃⁻) with one N=O double bond and two N–O single bonds, the "
    "formal charge on the nitrogen atom is:",
    Flex("+1", ["+5", "−1", "0"]),
    "Formal charge = valence electrons − non-bonding electrons − ½ (bonding electrons)",
    "Nitrogen forms four bonds in this structure (one double + two single) and has no lone pair.",
    ["Valence electrons of N = 5", "Non-bonding electrons on N = 0", "Bonding electrons = 8 (4 bonds)",
     "Formal charge = 5 − 0 − 8/2 = +1"],
    why="+5 is the oxidation number of nitrogen in nitrate, not its formal charge. −1 is the formal charge on each "
        "singly bonded oxygen (and the overall ion charge). 0 is the formal charge of the doubly bonded oxygen.",
    ncert=f"{REF3}, formal charge", seconds=50, checked=True)

assert mo(13)[0] == mo(15)[0] and mo(13)[1] == 1 and mo(15)[1] == 1
add("Molecular orbital theory", A, "assertion_reason",
    ar("N₂⁺ and N₂⁻ have the same bond order.", "N₂⁺ and N₂⁻ are both diamagnetic."),
    AR_, "Bond order and magnetism of N₂ ions",
    "N₂⁺ (13 electrons) loses a bonding σ2p electron: bond order (9 − 4)/2 = 2.5. N₂⁻ (15 electrons) gains an "
    "antibonding π* electron: bond order (10 − 5)/2 = 2.5. A is true. Each ion has one unpaired electron, so "
    "both are paramagnetic: R is false.",
    ["N₂⁺: Nb = 9, Na = 4 → 2.5, one unpaired electron", "N₂⁻: Nb = 10, Na = 5 → 2.5, one unpaired electron",
     "Same bond order → A true; both paramagnetic → R false"],
    answer="C", ncert=f"{REF3}, molecular orbital theory", seconds=60, checked=True)

shape = {"XeF₂": "linear", "CO₂": "linear", "NH₃": "pyramidal", "BF₃": "planar", "CH₄": "tetrahedral",
         "XeF₄": "square planar", "H₂O": "bent", "SO₂": "bent", "PCl₅": "trigonal bipyramidal",
         "BrF₅": "square pyramidal"}
prs = {"a": ("XeF₂", "CO₂"), "b": ("NH₃", "BF₃"), "c": ("CH₄", "XeF₄"), "d": ("H₂O", "SO₂"), "e": ("PCl₅", "BrF₅")}
truth = {k: shape[x] == shape[y] for k, (x, y) in prs.items()}
add("VSEPR shapes", A, "multi_statement",
    ms("In which of the following pairs do both molecules have the same shape?",
       [f"{x} and {y}" for x, y in prs.values()]),
    multi(truth, "(a) and (d) only", ["(a), (b) and (d) only", "(c) and (e) only", "(a), (d) and (e) only"]),
    "Shape depends on bond pairs and lone pairs together",
    "Count bond pairs and lone pairs on each central atom; lone pairs change the shape even when the number of "
    "electron pairs is the same.",
    ["(a) XeF₂ (2 bp + 3 lp) linear; CO₂ linear → same", "(b) NH₃ pyramidal; BF₃ trigonal planar → different",
     "(c) CH₄ tetrahedral; XeF₄ (4 bp + 2 lp) square planar → different",
     "(d) H₂O (2 bp + 2 lp) bent; SO₂ (2 σ bonds + 1 lp on S) bent → same",
     "(e) PCl₅ trigonal bipyramidal; BrF₅ square pyramidal → different"],
    why="XeF₂ looks crowded, but its three lone pairs sit in the equatorial plane and leave the molecule linear.",
    ncert=f"{REF3}, VSEPR theory", seconds=75, checked=True)

add("VSEPR shapes", A, "match_list",
    lists("Match List-I (molecule) with List-II (shape).", ["XeF₄", "SF₄", "BrF₅", "ClF₃"],
          ["Square pyramidal", "T-shaped", "Square planar", "See-saw"]),
    match({"A": "III", "B": "IV", "C": "I", "D": "II"},
          [{"A": "I", "B": "IV", "C": "III", "D": "II"}, {"A": "III", "B": "II", "C": "I", "D": "IV"},
           {"A": "III", "B": "IV", "C": "II", "D": "I"}]),
    "Shapes of molecules with lone pairs on the central atom (VSEPR)",
    "Count bond pairs and lone pairs on the central atom, place the electron pairs to minimise repulsion (lone "
    "pairs equatorial in a trigonal bipyramid, opposite each other in an octahedron) and name the shape from the "
    "positions of the atoms only.",
    ["XeF₄: 4 bp + 2 lp (6 pairs, octahedral arrangement, lone pairs trans) → square planar → III",
     "SF₄: 4 bp + 1 lp (5 pairs, lone pair equatorial) → see-saw → IV",
     "BrF₅: 5 bp + 1 lp (6 pairs, octahedral arrangement) → square pyramidal → I",
     "ClF₃: 3 bp + 2 lp (5 pairs, both lone pairs equatorial) → T-shaped → II"],
    why="Option A swaps XeF₄ and BrF₅, which both have six electron pairs. Option B swaps SF₄ and ClF₃, which both "
        "have five electron pairs. Option C gives BrF₅ the T shape and ClF₃ the square pyramid, mixing up a "
        "six-pair and a five-pair molecule.",
    ncert=f"{REF3}, VSEPR theory", seconds=60)

add("Molecular orbital theory", A, "statement_pair",
    sp("The C₂ molecule is diamagnetic.",
       "The double bond in C₂ consists of one σ bond and one π bond."),
    SP_, "Molecular orbital configuration of C₂",
    "C₂ has 12 electrons: KK σ2s² σ*2s² π2p_x² π2p_y². All electrons are paired, so C₂ is diamagnetic: "
    "Statement I is true. Its bond order is 2, but both bonds come from the two filled π orbitals; there is no "
    "electron in σ2p_z. So the double bond is made of two π bonds: Statement II is false.",
    ["12 electrons fill up to π2p_x² π2p_y² (σ2p_z is empty)", "All paired → diamagnetic → Statement I true",
     "Bond order 2 from four π electrons → two π bonds → Statement II false"],
    answer="C", ncert=f"{REF3}, bonding in some homonuclear diatomic molecules", seconds=60, checked=True)

add("Fajans' rule and dipole moment", A, "direct",
    "Which of the following orders of covalent character is correct?",
    Flex("LiCl > NaCl > KCl", ["LiF > LiCl > LiI", "NaCl > MgCl₂ > AlCl₃", "KCl > NaCl > LiCl"]),
    "Fajans' rules: covalent character of ionic bonds",
    "Covalent character increases as the cation becomes smaller and more highly charged (more polarising) and "
    "as the anion becomes larger (more polarisable).",
    ["Li⁺ < Na⁺ < K⁺ in size → polarising power Li⁺ > Na⁺ > K⁺ → LiCl > NaCl > KCl (correct)",
     "I⁻ is the largest anion → LiI is the most covalent of the lithium halides, so LiF > LiCl > LiI is reversed",
     "Al³⁺ is smallest and most charged → AlCl₃ > MgCl₂ > NaCl, so that option is reversed",
     "KCl > NaCl > LiCl is the reverse of the correct order"],
    ncert=f"{REF3}, polarity of bonds (Fajans' rules)", seconds=50)

# ==================================================================== 4. Chemical Thermodynamics
topic("Chemical Thermodynamics")
REF4 = f"{C11}, 'Thermodynamics'"

add("First law, work and enthalpy", B, "match_list",
    lists("Match List-I (type of process) with List-II (quantity that stays zero or constant).",
          ["Isothermal process", "Adiabatic process", "Isochoric process", "Isobaric process"],
          ["q = 0", "ΔT = 0", "Δp = 0", "ΔV = 0"]),
    match({"A": "II", "B": "I", "C": "IV", "D": "III"},
          [{"A": "I", "B": "II", "C": "IV", "D": "III"}, {"A": "II", "B": "I", "C": "III", "D": "IV"},
           {"A": "III", "B": "I", "C": "IV", "D": "II"}]),
    "Types of thermodynamic processes",
    "Each process is named after the quantity that does not change: iso-thermal (temperature), adiabatic (no heat "
    "exchange), iso-choric (volume), iso-baric (pressure).",
    ["Isothermal: temperature constant → ΔT = 0 → II", "Adiabatic: no heat exchanged → q = 0 → I",
     "Isochoric: volume constant → ΔV = 0 → IV", "Isobaric: pressure constant → Δp = 0 → III"],
    seconds=30)

add("First law, work and enthalpy", B, "direct",
    "Which of the following is NOT a state function?",
    Flex("Work (w)", ["Internal energy (U)", "Enthalpy (H)", "Entropy (S)"]),
    "State functions and path functions",
    "A state function depends only on the state of the system, not on how it got there. Work and heat depend on "
    "the path; U, H and S do not.",
    ["U, H and S: fixed by the state → state functions", "w: depends on the path (e.g. reversible or irreversible) "
     "→ not a state function"],
    ncert=f"{REF4}, state functions", seconds=25)

add("Entropy and Gibbs energy", B, "statement_pair",
    sp("For an isolated system, ΔU = 0.",
       "For a spontaneous process in an isolated system, the change in entropy is positive."),
    SP_, "Isolated systems and the entropy criterion",
    "An isolated system exchanges neither energy nor matter with the surroundings, so its internal energy cannot "
    "change: Statement I is true. For such a system, a spontaneous process is one in which entropy increases "
    "(ΔS > 0): Statement II is true.",
    ["Isolated: q = 0, w = 0 → ΔU = 0 → Statement I true", "Spontaneous change in isolated system: ΔS > 0 → "
     "Statement II true"],
    answer="A", ncert=f"{REF4}, first law and entropy", seconds=35)

add("Hess's law and enthalpies", B, "direct",
    "For which of the following substances is the standard enthalpy of formation, ΔfH°, equal to zero at 298 K?",
    Flex("Br₂(l)", ["O₃(g)", "C(diamond)", "H₂O(l)"]),
    "Standard enthalpy of formation of an element in its reference state is zero",
    "ΔfH° is zero only for an element in its most stable (reference) form at 1 bar and 298 K. Bromine's reference "
    "state at 298 K is the liquid.",
    ["Br₂(l): reference state of bromine → ΔfH° = 0", "O₃(g): not the reference form of oxygen (O₂ is) → ≠ 0",
     "C(diamond): reference form of carbon is graphite → ≠ 0", "H₂O(l): a compound → ≠ 0"],
    ncert=f"{REF4}, standard enthalpy of formation", seconds=35)

R = 8.314
dU = -92.4 - (-2) * R * 298 / 1000
assert round(dU, 1) == -87.4 and round(-92.4 + (-2) * R * 298 / 1000, 1) == -97.4
assert round(-92.4 + R * 298 / 1000, 1) == -89.9
add("First law, work and enthalpy", I, "numerical",
    "For the reaction N₂(g) + 3H₂(g) → 2NH₃(g), ΔH = −92.4 kJ mol⁻¹ at 298 K. Treating the gases as ideal, "
    "ΔU for the reaction at 298 K is (R = 8.314 J K⁻¹ mol⁻¹):",
    Flex("−87.4 kJ mol⁻¹", ["−97.4 kJ mol⁻¹", "−92.4 kJ mol⁻¹", "−89.9 kJ mol⁻¹"]),
    "Relation between ΔH and ΔU: ΔH = ΔU + Δn_g RT",
    "Δn_g is the change in the number of moles of gas from reactants to products.",
    ["Δn_g = 2 − (1 + 3) = −2", "Δn_g RT = −2 × 8.314 × 298 J = −4955 J = −4.96 kJ",
     "ΔU = ΔH − Δn_g RT = −92.4 − (−4.96) = −87.4 kJ mol⁻¹"],
    why="−97.4 kJ adds Δn_g RT instead of subtracting it. −92.4 kJ assumes ΔU = ΔH. −89.9 kJ takes Δn_g = −1.",
    ncert=f"{REF4}, relation between ΔH and ΔU", seconds=75, checked=True)

dfh_co = -393.5 - (-283.0)
assert round(dfh_co, 1) == -110.5
add("Hess's law and enthalpies", I, "numerical",
    "Given: C(graphite) + O₂(g) → CO₂(g); ΔH = −393.5 kJ mol⁻¹ and CO(g) + ½O₂(g) → CO₂(g); "
    "ΔH = −283.0 kJ mol⁻¹. The standard enthalpy of formation of CO(g) is:",
    Flex("−110.5 kJ mol⁻¹", ["−676.5 kJ mol⁻¹", "+110.5 kJ mol⁻¹", "−221.0 kJ mol⁻¹"]),
    "Hess's law of constant heat summation",
    "Formation of CO: C(graphite) + ½O₂(g) → CO(g). Get it by taking the first equation and reversing the second.",
    ["C + O₂ → CO₂; ΔH = −393.5", "CO₂ → CO + ½O₂; ΔH = +283.0 (reversed)",
     "Add: C + ½O₂ → CO; ΔH = −393.5 + 283.0 = −110.5 kJ mol⁻¹"],
    why="−676.5 adds the two equations without reversing the second. +110.5 has the sign wrong. −221.0 is the "
        "value for forming 2 mol of CO.",
    ncert=f"{REF4}, Hess's law of constant heat summation", seconds=60, checked=True)

add("Entropy and Gibbs energy", I, "assertion_reason",
    ar("Every exothermic reaction is spontaneous.",
       "ΔG = ΔH − TΔS, so the sign of ΔG depends on both ΔH and TΔS."),
    AR_, "Gibbs energy criterion for spontaneity",
    "A negative ΔH helps, but if ΔS is negative and T is high enough, −TΔS can outweigh ΔH and make ΔG positive. "
    "So exothermic reactions are not always spontaneous: A is false. R is the correct relation and is true.",
    ["ΔG = ΔH − TΔS", "ΔH < 0 and ΔS < 0 → ΔG > 0 at high T → not spontaneous",
     "So A is false; R is true"],
    answer="D", ncert=f"{REF4}, Gibbs energy and spontaneity", seconds=40)

ds = 31.5e3 / 350
assert close(ds, 90) and close(31.5 / 350, 0.09) and close(350 / 31.5, 11.1)
add("Entropy and Gibbs energy", I, "numerical",
    "A liquid boils at 350 K and its enthalpy of vaporisation is 31.5 kJ mol⁻¹. The entropy of vaporisation "
    "at its boiling point is:",
    Flex("90 J K⁻¹ mol⁻¹", ["0.09 J K⁻¹ mol⁻¹", "11.1 J K⁻¹ mol⁻¹", "−90 J K⁻¹ mol⁻¹"]),
    "Entropy change for a phase change at equilibrium: ΔS = ΔH/T",
    "At the boiling point, liquid and vapour are in equilibrium, so ΔvapS = ΔvapH / Tb. Convert kJ to J.",
    ["ΔvapH = 31.5 kJ mol⁻¹ = 31 500 J mol⁻¹", "ΔvapS = 31 500 / 350 = 90 J K⁻¹ mol⁻¹"],
    why="0.09 forgets to convert kJ to J. 11.1 divides T by ΔH. −90 has the wrong sign: vaporisation increases "
        "disorder.",
    seconds=40, checked=True)

add("Hess's law and enthalpies", I, "match_list",
    lists("Match List-I (enthalpy change) with List-II (process it refers to).",
          ["Standard enthalpy of formation of methane", "Enthalpy of combustion of methane",
           "Enthalpy of atomisation of methane", "Enthalpy of fusion of ice"],
          ["CH₄(g) → C(g) + 4H(g)", "CH₄(g) + 2O₂(g) → CO₂(g) + 2H₂O(l)", "H₂O(s) → H₂O(l)",
           "C(graphite) + 2H₂(g) → CH₄(g)"]),
    match({"A": "IV", "B": "II", "C": "I", "D": "III"},
          [{"A": "I", "B": "II", "C": "IV", "D": "III"}, {"A": "IV", "B": "III", "C": "I", "D": "II"},
           {"A": "II", "B": "IV", "C": "I", "D": "III"}]),
    "Types of enthalpy changes",
    "Formation starts from elements in their reference states; combustion burns one mole completely in oxygen; "
    "atomisation breaks all bonds to give gaseous atoms; fusion melts the solid.",
    ["Formation: C(graphite) + 2H₂(g) → CH₄(g) → IV", "Combustion: CH₄ + 2O₂ → CO₂ + 2H₂O(l) → II",
     "Atomisation: CH₄(g) → C(g) + 4H(g) → I", "Fusion: H₂O(s) → H₂O(l) → III"],
    ncert=f"{REF4}, enthalpies for different types of reactions", seconds=45)

logk = 11.42 / 5.71
assert logk == 2 and round(math.exp(2), 2) == 7.39
add("Gibbs energy and K", A, "numerical",
    "The standard Gibbs energy change of a reaction at 298 K is −11.42 kJ mol⁻¹. Its equilibrium constant at this "
    "temperature is (2.303 RT = 5.71 kJ mol⁻¹ at 298 K):",
    Flex("100", ["0.01", "7.39", "2"]),
    "ΔG° = −2.303 RT log K",
    "Rearrange for log K and take the antilog.",
    ["log K = −ΔG°/(2.303 RT) = 11.42/5.71 = 2", "K = 10² = 100"],
    why="0.01 drops the minus sign (log K = −2). 7.39 uses e² by treating 5.71 kJ as RT. 2 is log K, not K.",
    ncert=f"{REF4}, Gibbs energy change and equilibrium", seconds=60, checked=True)

t_min = 176e3 / 160
assert t_min == 1100 and t_min - 273 == 827 and t_min + 273 == 1373
add("Entropy and Gibbs energy", A, "numerical",
    "For a decomposition reaction, ΔH = +176 kJ mol⁻¹ and ΔS = +160 J K⁻¹ mol⁻¹. Assuming both stay constant "
    "with temperature, the reaction becomes spontaneous above:",
    Flex("1100 K", ["1.1 K", "827 K", "1373 K"]),
    "Temperature at which ΔG changes sign: T = ΔH/ΔS",
    "With ΔH > 0 and ΔS > 0, ΔG = ΔH − TΔS becomes negative once TΔS exceeds ΔH.",
    ["ΔG = 0 when T = ΔH/ΔS", "T = 176 000 J mol⁻¹ / 160 J K⁻¹ mol⁻¹ = 1100 K",
     "Above 1100 K, ΔG < 0 → spontaneous"],
    why="1.1 K leaves ΔH in kJ. 827 K is the Celsius value (1100 − 273) written as kelvin. 1373 K adds 273 to a "
        "value that is already in kelvin.",
    seconds=60, checked=True)

add("First law, work and enthalpy", A, "multi_statement",
    ms("Which of the following statements are correct?",
       ["For the free expansion of an ideal gas into vacuum, w = 0.",
        "For the isothermal expansion of an ideal gas, ΔU = 0.",
        "For the reversible isothermal expansion of n mol of an ideal gas from Vᵢ to V_f, "
        "w = −2.303 nRT log (V_f/Vᵢ).",
        "The enthalpy change of a reaction equals the heat absorbed at constant volume.",
        "For one mole of an ideal gas, C_p − C_v = R."]),
    multi({"a": True, "b": True, "c": True, "d": False, "e": True}, "(a), (b), (c) and (e) only",
          ["(a), (b) and (d) only", "(b), (c), (d) and (e) only", "(a), (c) and (e) only"]),
    "First law applied to ideal gases",
    "Free expansion is against zero external pressure, so no work is done. The internal energy of an ideal gas "
    "depends only on temperature. Heat at constant volume equals ΔU, while heat at constant pressure equals ΔH.",
    ["(a) True: p_ext = 0 → w = 0", "(b) True: U of an ideal gas depends only on T",
     "(c) True: reversible isothermal work", "(d) False: q_v = ΔU; it is q_p that equals ΔH",
     "(e) True: C_p − C_v = R for one mole of ideal gas"],
    ncert=f"{REF4}, applications: work, enthalpy and heat capacity", seconds=75)

dh = (435 + 243) - 2 * 431
assert dh == -184 and (435 + 243) - 431 == 247
add("Hess's law and enthalpies", A, "numerical",
    "Using the bond enthalpies H–H = 435 kJ mol⁻¹, Cl–Cl = 243 kJ mol⁻¹ and H–Cl = 431 kJ mol⁻¹, the enthalpy "
    "change for the reaction H₂(g) + Cl₂(g) → 2HCl(g) is:",
    Flex("−184 kJ", ["+184 kJ", "+247 kJ", "−92 kJ"]),
    "ΔrH from bond enthalpies (gas-phase reaction)",
    "ΔrH = Σ(bond enthalpies of bonds broken) − Σ(bond enthalpies of bonds formed).",
    ["Bonds broken: H–H + Cl–Cl = 435 + 243 = 678 kJ", "Bonds formed: 2 H–Cl = 2 × 431 = 862 kJ",
     "ΔrH = 678 − 862 = −184 kJ"],
    why="+184 kJ subtracts in the wrong order. +247 kJ counts only one H–Cl bond formed. −92 kJ is the value per "
        "mole of HCl, not for the reaction as written.",
    ncert=f"{REF4}, bond enthalpy", seconds=60, checked=True)

# ==================================================================== 5. Solutions
topic("Solutions")
REF5 = f"{C12}, 'Solutions'"

add("Concentration terms", B, "match_list",
    lists("Match List-I (concentration term) with List-II (definition).",
          ["Molarity", "Molality", "Mole fraction", "Parts per million"],
          ["Moles of solute per kilogram of solvent", "Moles of solute per litre of solution",
           "Parts of a component per 10⁶ parts of the solution", "Moles of a component divided by the total "
           "moles of all components"]),
    match({"A": "II", "B": "I", "C": "IV", "D": "III"},
          [{"A": "I", "B": "II", "C": "IV", "D": "III"}, {"A": "II", "B": "I", "C": "III", "D": "IV"},
           {"A": "II", "B": "IV", "C": "I", "D": "III"}]),
    "Ways of expressing concentration",
    "Molarity uses the volume of the solution; molality uses the mass of the solvent; mole fraction is a ratio of "
    "moles; ppm is used for very small amounts.",
    ["Molarity → mol per litre of solution → II", "Molality → mol per kg of solvent → I",
     "Mole fraction → moles of component / total moles → IV", "ppm → parts per million parts → III"],
    ncert=f"{REF5}, expressing concentration of solutions", seconds=30)

add("Raoult's law and ideal solutions", B, "direct",
    "Which of the following liquid pairs forms a solution showing negative deviation from Raoult's law?",
    Flex("Chloroform and acetone", ["Ethanol and acetone", "Carbon disulphide and acetone",
                                    "n-Hexane and n-heptane"]),
    "Non-ideal solutions: negative deviation",
    "Negative deviation occurs when the A–B attractions are stronger than A–A and B–B attractions. Chloroform "
    "forms a hydrogen bond with the oxygen of acetone, so the vapour pressure falls below the Raoult's law value.",
    ["Chloroform + acetone: new H-bonds between unlike molecules → negative deviation",
     "Ethanol + acetone: acetone breaks some H-bonds of ethanol → positive deviation",
     "CS₂ + acetone: weaker unlike interactions → positive deviation",
     "n-Hexane + n-heptane: nearly ideal"],
    ncert=f"{REF5}, ideal and non-ideal solutions", seconds=35)

add("Colligative properties", B, "statement_pair",
    sp("The elevation of boiling point of a dilute solution depends on the chemical nature of the solute.",
       "Osmotic pressure measurement is preferred for finding the molar masses of proteins and other "
       "biomolecules."),
    SP_, "Colligative properties and their uses",
    "Colligative properties depend only on the number of solute particles, not on their nature: Statement I is "
    "false. Osmotic pressure is measured at room temperature and is large even for very dilute solutions, so it "
    "suits biomolecules that are unstable at high temperatures and have large molar masses: Statement II is true.",
    ["Boiling point elevation ΔTb = Kb m → depends on number of particles only → Statement I false",
     "Osmotic pressure method used for proteins and polymers → Statement II true"],
    answer="D", ncert=f"{REF5}, colligative properties and osmotic pressure", seconds=35)

m_urea = (3.0 / 60) / 0.5
dtf = 1.86 * m_urea
assert close(m_urea, 0.1) and close(dtf, 0.186) and close(1.86 * 0.05, 0.093)
add("Colligative properties", I, "numerical",
    "3.0 g of urea (molar mass 60 g mol⁻¹) is dissolved in 500 g of water. The freezing point of the solution is "
    "(K_f of water = 1.86 K kg mol⁻¹; freezing point of water = 0 °C):",
    Flex("−0.186 °C", ["−0.093 °C", "−0.372 °C", "−1.86 °C"]),
    "Depression of freezing point: ΔT_f = K_f × m",
    "Urea is a non-electrolyte (i = 1). Molality uses the mass of solvent in kilograms.",
    ["Moles of urea = 3.0/60 = 0.05 mol", "Molality = 0.05/0.500 kg = 0.1 mol kg⁻¹",
     "ΔT_f = 1.86 × 0.1 = 0.186 K → freezing point = −0.186 °C"],
    why="−0.093 °C divides by 1 kg instead of 0.5 kg. −0.372 °C treats urea as if it gave two particles. −1.86 °C "
        "takes the molality as 1.",
    ncert=f"{REF5}, depression of freezing point", seconds=60, checked=True)

pA, pB, xA = 450, 700, 0.4
ptot = xA * pA + (1 - xA) * pB
yA = xA * pA / ptot
assert close(ptot, 600) and close(yA, 0.30)
add("Raoult's law and ideal solutions", I, "numerical",
    "Two liquids A and B form an ideal solution. At a certain temperature the vapour pressures of pure A and pure "
    "B are 450 mm Hg and 700 mm Hg. For a solution in which the mole fraction of A is 0.4, the mole fraction of A "
    "in the vapour in equilibrium with it is:",
    Flex("0.30", ["0.40", "0.70", "0.60"]),
    "Raoult's law and Dalton's law of partial pressures",
    "Each partial pressure is p° × x (Raoult). The vapour composition is the partial pressure divided by the "
    "total pressure (Dalton).",
    ["p_A = 0.4 × 450 = 180 mm Hg; p_B = 0.6 × 700 = 420 mm Hg", "p_total = 600 mm Hg",
     "y_A = 180/600 = 0.30"],
    why="0.40 is the mole fraction in the liquid. 0.70 is y_B. 0.60 is x_B. The vapour is richer in the more "
        "volatile component B.",
    ncert=f"{REF5}, vapour pressure of liquid–liquid solutions", seconds=75, checked=True)

add("van't Hoff factor", I, "assertion_reason",
    ar("The depression of freezing point of a 0.01 m aqueous KCl solution is nearly twice that of a 0.01 m aqueous "
       "glucose solution.",
       "In dilute aqueous solution, KCl dissociates almost completely into K⁺ and Cl⁻ ions, so its van't Hoff "
       "factor is close to 2."),
    AR_, "van't Hoff factor for electrolytes",
    "Colligative properties depend on the number of solute particles. Each KCl unit gives two ions, while glucose "
    "stays as one molecule, so ΔT_f = i K_f m is nearly doubled for KCl. R is true and explains A.",
    ["Glucose: i = 1", "KCl → K⁺ + Cl⁻: i ≈ 2", "ΔT_f ∝ i → KCl shows nearly twice the depression"],
    answer="A", ncert=f"{REF5}, abnormal molar masses and van't Hoff factor", seconds=40)

add("Raoult's law and ideal solutions", I, "multi_statement",
    ms("Which of the following are true for an ideal solution of two liquids?",
       ["The enthalpy of mixing is zero.", "The volume of mixing is zero.",
        "It obeys Raoult's law over the entire range of concentration.",
        "The A–B interactions are stronger than the A–A and B–B interactions.",
        "It forms a minimum-boiling azeotrope."]),
    multi({"a": True, "b": True, "c": True, "d": False, "e": False}, "(a), (b) and (c) only",
          ["(a), (b) and (d) only", "(c), (d) and (e) only", "(a), (c) and (e) only"]),
    "Ideal solutions",
    "In an ideal solution the A–B interactions are nearly equal to the A–A and B–B interactions, so no heat is "
    "absorbed or released and there is no volume change on mixing. Such solutions follow Raoult's law at all "
    "compositions. Azeotropes form only with large deviations from Raoult's law.",
    ["(a) True: Δ_mix H = 0", "(b) True: Δ_mix V = 0", "(c) True: obeys Raoult's law at all compositions",
     "(d) False: that describes negative deviation", "(e) False: minimum-boiling azeotropes come from large "
     "positive deviation"],
    ncert=f"{REF5}, ideal and non-ideal solutions", seconds=50)

i_ab2 = 1 + 0.8 * (3 - 1)
dtf2 = i_ab2 * 1.86 * 0.1
assert close(i_ab2, 2.6) and round(dtf2, 3) == 0.484 and round(3 * 0.186, 3) == 0.558 and round(1.8 * 0.186, 3) == 0.335
add("van't Hoff factor", A, "numerical",
    "A salt of type AB₂ is 80% dissociated into A²⁺ and B⁻ ions in a 0.1 m aqueous solution. The depression of "
    "freezing point of this solution is (K_f of water = 1.86 K kg mol⁻¹):",
    Flex("0.484 K", ["0.186 K", "0.558 K", "0.335 K"]),
    "van't Hoff factor from degree of dissociation: i = 1 + α(n − 1)",
    "AB₂ → A²⁺ + 2B⁻ gives n = 3 particles per formula unit. Partial dissociation gives i between 1 and 3.",
    ["n = 3, α = 0.8", "i = 1 + 0.8 × (3 − 1) = 2.6", "ΔT_f = i K_f m = 2.6 × 1.86 × 0.1 = 0.484 K"],
    why="0.186 K ignores dissociation (i = 1). 0.558 K assumes complete dissociation (i = 3). 0.335 K uses "
        "n − 1 = 1 as if the salt gave only two ions (i = 1.8).",
    ncert=f"{REF5}, abnormal molar masses and van't Hoff factor", seconds=90, checked=True)

M_prot = 2.0 * 0.082 * 300 / (0.0246 * 0.250)
assert close(M_prot, 8000) and close(2.0 * 0.082 * 300 / 0.0246, 2000)
assert close(2.0 * 0.082 * 300 * 0.25 / 0.0246, 500) and close(2.0 * 0.082 * 300 / (0.0246 * 250), 8)
add("Colligative properties", A, "numerical",
    "A solution of 2.0 g of a protein in 250 mL of water has an osmotic pressure of 0.0246 atm at 300 K. The "
    "molar mass of the protein is (R = 0.082 L atm K⁻¹ mol⁻¹):",
    Flex("8.0 × 10³ g mol⁻¹", ["2.0 × 10³ g mol⁻¹", "5.0 × 10² g mol⁻¹", "8.0 g mol⁻¹"]),
    "Molar mass from osmotic pressure: π = (w/M)RT/V",
    "Rearrange to M = wRT/(πV), with V in litres to match R in L atm K⁻¹ mol⁻¹.",
    ["V = 250 mL = 0.250 L", "M = (2.0 × 0.082 × 300)/(0.0246 × 0.250)", "= 49.2/0.00615 = 8000 g mol⁻¹"],
    why="2.0 × 10³ ignores the volume (takes V = 1 L). 5.0 × 10² multiplies by V instead of dividing. 8.0 uses "
        "V = 250 without converting mL to L.",
    ncert=f"{REF5}, osmosis and osmotic pressure", seconds=90, checked=True)

add("van't Hoff factor", A, "statement_pair",
    sp("For a solute that associates in solution, the van't Hoff factor i is less than 1.",
       "Ethanoic acid dimerises in benzene through hydrogen bonding, so the molar mass found from colligative "
       "properties is about twice its true value."),
    SP_, "Association and abnormal molar mass",
    "Association reduces the number of particles, so i = (normal molar mass)/(observed molar mass) is less than "
    "1: Statement I is true. Two ethanoic acid molecules join by hydrogen bonds in benzene, halving the number of "
    "particles; the colligative effect halves and the calculated molar mass doubles (about 120 instead of 60): "
    "Statement II is true.",
    ["Association → fewer particles → i < 1 → Statement I true",
     "2CH₃COOH ⇌ (CH₃COOH)₂ in benzene → observed molar mass ≈ 2 × 60 → Statement II true"],
    answer="A", ncert=f"{REF5}, abnormal molar masses", seconds=45)

# ==================================================================== 6. Equilibrium
topic("Equilibrium")
REF6 = f"{C11}, 'Equilibrium'"

oh = 2 * 0.005
assert close(14 + math.log10(oh), 12) and round(14 + math.log10(0.005), 1) == 11.7
add("Acids, bases and pH", B, "numerical",
    "The pH of a 0.005 M aqueous solution of Ba(OH)₂ at 298 K, assuming complete dissociation, is "
    "(K_w = 10⁻¹⁴; log 5 = 0.70):",
    Flex("12", ["2", "11.7", "2.3"]),
    "pH of a strong base that gives two OH⁻ ions per formula unit",
    "Ba(OH)₂ → Ba²⁺ + 2OH⁻, so [OH⁻] is twice the concentration of the base.",
    ["[OH⁻] = 2 × 0.005 = 0.01 M", "pOH = −log(0.01) = 2", "pH = 14 − 2 = 12"],
    why="2 is the pOH, not the pH. 11.7 forgets that each Ba(OH)₂ gives two OH⁻ ions (pOH = 2.3). 2.3 is the pOH "
        "from that same mistake.",
    ncert=f"{REF6}, the pH scale", seconds=40, checked=True)

add("Kp, Kc and Le Chatelier", B, "direct",
    "For the equilibrium N₂(g) + 3H₂(g) ⇌ 2NH₃(g), ΔH < 0, the yield of ammonia at equilibrium is increased by:",
    Flex("Increasing the pressure", ["Increasing the temperature", "Decreasing the pressure",
                                     "Adding a catalyst"]),
    "Le Chatelier's principle",
    "The forward reaction reduces the number of gas moles (4 → 2) and releases heat. Higher pressure favours the "
    "side with fewer gas moles, so it shifts the equilibrium towards NH₃.",
    ["Δn_g = 2 − 4 = −2 → higher pressure favours NH₃",
     "Exothermic → higher temperature favours the reverse reaction",
     "A catalyst speeds up both directions equally and does not change the equilibrium yield"],
    ncert=f"{REF6}, factors affecting equilibria", seconds=30)

add("Physical equilibria and Henry's law", B, "direct",
    "The Henry's law constants (K_H) of four gases W, X, Y and Z in water at the same temperature are 1.6, 35, 70 "
    "and 145 kbar respectively. At the same partial pressure, which gas is the most soluble in water?",
    Flex("W", ["X", "Y", "Z"]),
    "Henry's law: p = K_H x",
    "At a fixed partial pressure p, the mole fraction of dissolved gas is x = p/K_H. The smaller K_H, the larger "
    "the solubility.",
    ["x = p/K_H", "Smallest K_H (1.6 kbar) → largest x → W is the most soluble"],
    why="Z has the largest K_H and is the least soluble; reading K_H as a solubility gets the order backwards.",
    ncert=f"{REF6}, equilibrium involving dissolution of gases in liquids", seconds=35)

add("Acids, bases and pH", B, "statement_pair",
    sp("BF₃ is a Lewis acid because it can accept a pair of electrons.",
       "The conjugate base of a strong acid is a strong base."),
    SP_, "Lewis acids; conjugate acid–base pairs",
    "Boron in BF₃ has only six valence electrons and accepts an electron pair (for example from NH₃): Statement I "
    "is true. A strong acid gives up its proton easily, so its conjugate base has little tendency to take a proton "
    "back: it is a weak base. Statement II is false.",
    ["BF₃: electron-deficient, accepts a lone pair → Lewis acid → Statement I true",
     "Strong acid ↔ weak conjugate base (e.g. HCl / Cl⁻) → Statement II false"],
    answer="C", ncert=f"{REF6}, acids, bases and salts", seconds=35)

add("Kp, Kc and Le Chatelier", B, "direct",
    "For which of the following equilibria is K_p equal to K_c?",
    Flex("H₂(g) + I₂(g) ⇌ 2HI(g)", ["N₂(g) + 3H₂(g) ⇌ 2NH₃(g)", "PCl₅(g) ⇌ PCl₃(g) + Cl₂(g)",
                                     "2SO₂(g) + O₂(g) ⇌ 2SO₃(g)"]),
    "Relation between K_p and K_c: K_p = K_c (RT)^Δn",
    "K_p = K_c when Δn, the change in the number of moles of gas, is zero.",
    ["H₂ + I₂ ⇌ 2HI: Δn = 2 − 2 = 0 → K_p = K_c", "N₂ + 3H₂ ⇌ 2NH₃: Δn = −2", "PCl₅ ⇌ PCl₃ + Cl₂: Δn = +1",
     "2SO₂ + O₂ ⇌ 2SO₃: Δn = −1"],
    ncert=f"{REF6}, relationship between K_p and K_c", seconds=30)

x = 1.5 / 2
kc = 1.5 ** 2 / ((1 - x) * (1 - x))
assert close(kc, 36) and close(1.5 / 0.0625, 24) and close(1.5 ** 2 / (1 - x), 9)
add("Kp, Kc and Le Chatelier", I, "numerical",
    "1.0 mol of H₂ and 1.0 mol of I₂ are heated in a closed 1.0 L vessel. At equilibrium, 1.5 mol of HI is "
    "present: H₂(g) + I₂(g) ⇌ 2HI(g). The value of K_c is:",
    Flex("36", ["24", "9", "1/36"]),
    "Equilibrium constant from an ICE table",
    "2 mol of HI form from 1 mol each of H₂ and I₂, so forming 1.5 mol HI uses 0.75 mol of each.",
    ["H₂ and I₂ used = 1.5/2 = 0.75 mol each", "At equilibrium: [H₂] = [I₂] = 0.25 M, [HI] = 1.5 M",
     "K_c = [HI]²/([H₂][I₂]) = 2.25/0.0625 = 36"],
    why="24 forgets to square [HI]. 9 leaves one of the reactant concentrations out of the denominator. 1/36 is "
        "K_c for the reverse reaction.",
    ncert=f"{REF6}, equilibrium constant", seconds=70, checked=True)

h_ion = math.sqrt(1e-5 * 0.1)
assert close(-math.log10(h_ion), 3) and close(-math.log10(1e-5 * 0.1), 6)
add("Acids, bases and pH", I, "numerical",
    "The pH of a 0.1 M solution of a weak monobasic acid HA (K_a = 1.0 × 10⁻⁵) is:",
    Flex("3", ["5", "6", "1"]),
    "Ionisation of a weak acid: [H⁺] = √(K_a C) when α is small",
    "HA ⇌ H⁺ + A⁻. For a small degree of ionisation, K_a ≈ [H⁺]²/C.",
    ["[H⁺] = √(1.0 × 10⁻⁵ × 0.1) = √(10⁻⁶) = 10⁻³ M", "pH = 3",
     "Check: α = 10⁻³/0.1 = 1%, small, so the approximation holds"],
    why="5 is the pK_a. 6 forgets the square root (uses K_a C). 1 treats HA as a strong acid.",
    ncert=f"{REF6}, ionisation of weak acids", seconds=50, checked=True)

ph_buf = 4.74 + math.log10(0.1 / 0.2)
assert round(ph_buf, 2) == 4.44 and round(4.74 + math.log10(2), 2) == 5.04
add("Hydrolysis and buffers", I, "numerical",
    "A buffer solution contains 0.2 M CH₃COOH and 0.1 M CH₃COONa. Its pH is (pK_a of CH₃COOH = 4.74; "
    "log 2 = 0.30):",
    Flex("4.44", ["5.04", "4.74", "9.26"]),
    "Henderson–Hasselbalch equation for an acidic buffer: pH = pK_a + log([salt]/[acid])",
    "The acid is in excess over the salt, so the pH is below the pK_a.",
    ["[salt]/[acid] = 0.1/0.2 = 0.5", "log 0.5 = −0.30", "pH = 4.74 − 0.30 = 4.44"],
    why="5.04 puts [acid]/[salt] in the log. 4.74 assumes equal concentrations. 9.26 is 14 − pK_a, as if it were a "
        "basic buffer.",
    ncert=f"{REF6}, buffer solutions", seconds=50, checked=True)

ksp_coef = {"AgCl": (1, 1), "CaF₂": (1, 2), "Al(OH)₃": (1, 3), "Ca₃(PO₄)₂": (3, 2)}
expr = {k: (a ** a * b ** b, a + b) for k, (a, b) in ksp_coef.items()}
assert expr == {"AgCl": (1, 2), "CaF₂": (4, 3), "Al(OH)₃": (27, 4), "Ca₃(PO₄)₂": (108, 5)}
add("Solubility product", I, "match_list",
    lists("Match List-I (sparingly soluble salt) with List-II (K_sp in terms of its molar solubility s).",
          ["AgCl", "CaF₂", "Al(OH)₃", "Ca₃(PO₄)₂"], ["27s⁴", "108s⁵", "s²", "4s³"]),
    match({"A": "III", "B": "IV", "C": "I", "D": "II"},
          [{"A": "III", "B": "I", "C": "IV", "D": "II"}, {"A": "IV", "B": "III", "C": "I", "D": "II"},
           {"A": "III", "B": "IV", "C": "II", "D": "I"}]),
    "Solubility product: for MₓAᵧ, K_sp = xˣ yʸ s⁽ˣ⁺ʸ⁾",
    "Write the dissolution equation, express each ion concentration in terms of s, and multiply with powers equal "
    "to the coefficients.",
    ["AgCl → Ag⁺ + Cl⁻: K_sp = s·s = s² → III", "CaF₂ → Ca²⁺ + 2F⁻: K_sp = s(2s)² = 4s³ → IV",
     "Al(OH)₃ → Al³⁺ + 3OH⁻: K_sp = s(3s)³ = 27s⁴ → I",
     "Ca₃(PO₄)₂ → 3Ca²⁺ + 2PO₄³⁻: K_sp = (3s)³(2s)² = 108s⁵ → II"],
    ncert=f"{REF6}, solubility equilibria of sparingly soluble salts", seconds=60, checked=True)

add("Kp, Kc and Le Chatelier", I, "assertion_reason",
    ar("Adding an inert gas at constant volume does not shift the equilibrium N₂(g) + 3H₂(g) ⇌ 2NH₃(g).",
       "Adding an inert gas at constant volume increases the total pressure of the system."),
    AR_, "Effect of an inert gas on equilibrium",
    "At constant volume, the inert gas does not change the partial pressures (or molar concentrations) of N₂, H₂ "
    "and NH₃, so Q stays equal to K and nothing shifts: A is true. The total pressure does rise because more gas "
    "is present, so R is true. But the rise in total pressure is not why there is no shift; the reason is that "
    "the partial pressures of the reacting gases are unchanged.",
    ["Constant V: partial pressures of N₂, H₂, NH₃ unchanged → no shift → A true",
     "Total pressure increases → R true", "R does not explain A (if anything it would suggest a shift)"],
    answer="B", ncert=f"{REF6}, effect of inert gas addition", seconds=45)

add("Hydrolysis and buffers", I, "match_list",
    lists("Match List-I (salt dissolved in water) with List-II (nature of the solution at 298 K).",
          ["NaCl", "NH₄Cl", "CH₃COONa", "CH₃COONH₄"],
          ["Acidic (pH < 7)", "Basic (pH > 7)", "Neutral; salt of a strong acid and a strong base",
           "pH = 7 + ½(pK_a − pK_b)"]),
    match({"A": "III", "B": "I", "C": "II", "D": "IV"},
          [{"A": "III", "B": "II", "C": "I", "D": "IV"}, {"A": "IV", "B": "I", "C": "II", "D": "III"},
           {"A": "I", "B": "III", "C": "II", "D": "IV"}]),
    "Hydrolysis of salts",
    "Only ions from weak acids or weak bases hydrolyse. The cation of a weak base makes the solution acidic; the "
    "anion of a weak acid makes it basic; when both hydrolyse, the pH depends on pK_a and pK_b.",
    ["NaCl: no hydrolysis → neutral → III", "NH₄Cl: NH₄⁺ hydrolyses → acidic → I",
     "CH₃COONa: CH₃COO⁻ hydrolyses → basic → II", "CH₃COONH₄: both ions hydrolyse → pH = 7 + ½(pK_a − pK_b) → IV"],
    ncert=f"{REF6}, hydrolysis of salts and the pH of their solutions", seconds=45)

add("Acids, bases and pH", I, "multi_statement",
    ms("Which of the following statements are correct?",
       ["Water can act both as a Brønsted acid and as a Brønsted base.",
        "The conjugate base of H₂SO₄ is SO₄²⁻.",
        "The ionic product of water, K_w, increases with rise in temperature.",
        "AlCl₃ is a Lewis base.",
        "The pH of pure water at 298 K is 7."]),
    multi({"a": True, "b": False, "c": True, "d": False, "e": True}, "(a), (c) and (e) only",
          ["(a), (b) and (c) only", "(c), (d) and (e) only", "(a) and (e) only"]),
    "Acid–base concepts and the ionisation of water",
    "Water donates a proton to NH₃ and accepts one from HCl. The conjugate base of an acid is the acid minus one "
    "proton. Ionisation of water is endothermic, so K_w rises with temperature. AlCl₃ is electron-deficient and "
    "accepts electron pairs.",
    ["(a) True: amphoteric (amphiprotic) behaviour of water", "(b) False: H₂SO₄ − H⁺ = HSO₄⁻",
     "(c) True: endothermic ionisation → K_w increases with T", "(d) False: AlCl₃ is a Lewis acid",
     "(e) True: [H⁺] = 10⁻⁷ M at 298 K"],
    ncert=f"{REF6}, ionisation of acids and bases", seconds=50)

alpha, P = 0.5, 1.0
p_no2 = 2 * alpha / (1 + alpha) * P
p_n2o4 = (1 - alpha) / (1 + alpha) * P
kp = p_no2 ** 2 / p_n2o4
assert close(kp, 4 / 3) and close((2 * alpha) ** 2 / (1 - alpha), 2) and close(alpha ** 2 / (1 - alpha ** 2), 1 / 3)
add("Kp, Kc and Le Chatelier", A, "numerical",
    "N₂O₄(g) is 50% dissociated into NO₂(g) at equilibrium at a total pressure of 1.0 atm: N₂O₄(g) ⇌ 2NO₂(g). "
    "K_p for this equilibrium at the same temperature is:",
    Flex("1.33 atm", ["2.0 atm", "0.33 atm", "1.0 atm"]),
    "K_p from degree of dissociation using mole fractions",
    "Start with 1 mol N₂O₄. With α = 0.5, the total moles become 1 + α. Partial pressure = mole fraction × total "
    "pressure.",
    ["At equilibrium: N₂O₄ = 1 − α = 0.5 mol, NO₂ = 2α = 1.0 mol, total = 1.5 mol",
     "p(NO₂) = (1.0/1.5) × 1 = 2/3 atm; p(N₂O₄) = (0.5/1.5) × 1 = 1/3 atm",
     "K_p = (2/3)²/(1/3) = 4/3 ≈ 1.33 atm"],
    shortcut="K_p = 4α²P/(1 − α²) = 4 × 0.25 × 1/0.75 = 1.33 atm.",
    why="2.0 atm forgets that the total number of moles rises to 1 + α. 0.33 atm drops the factor 4 that comes "
        "from (2α)². 1.0 atm uses 4α²P without the (1 − α²) denominator.",
    ncert=f"{REF6}, equilibrium constant in gaseous systems", seconds=110, checked=True)

s_common = 1.8e-10 / 0.01
assert close(s_common, 1.8e-8) and close(math.sqrt(1.8e-10), 1.34e-5)
add("Solubility product", A, "numerical",
    "The solubility product of AgCl at 298 K is 1.8 × 10⁻¹⁰. Its molar solubility in 0.01 M NaCl solution is "
    "(√1.8 = 1.34):",
    Flex("1.8 × 10⁻⁸ M", ["1.34 × 10⁻⁵ M", "1.8 × 10⁻¹⁰ M", "1.8 × 10⁻¹² M"]),
    "Common ion effect on solubility",
    "Cl⁻ from NaCl suppresses the dissolution of AgCl. Since s is tiny, [Cl⁻] ≈ 0.01 M.",
    ["K_sp = [Ag⁺][Cl⁻] = s × (0.01 + s) ≈ s × 0.01", "s = 1.8 × 10⁻¹⁰/0.01 = 1.8 × 10⁻⁸ M"],
    why="1.34 × 10⁻⁵ M is the solubility in pure water, ignoring the common ion. 1.8 × 10⁻¹⁰ M takes s = K_sp. "
        "1.8 × 10⁻¹² M multiplies by 0.01 instead of dividing.",
    ncert=f"{REF6}, common ion effect in the ionisation of salts", seconds=60, checked=True)

excess = 50 * 0.2 - 50 * 0.1
h_mix = excess / 100
assert close(-math.log10(h_mix), 1.30, 0.01) and close(-math.log10(excess / 50), 1.0) and \
    close(-math.log10(0.2), 0.70, 0.01)
add("Acids, bases and pH", A, "numerical",
    "50 mL of 0.2 M HCl is mixed with 50 mL of 0.1 M NaOH at 298 K. The pH of the resulting solution is "
    "(log 2 = 0.30):",
    Flex("1.30", ["1.00", "0.70", "12.70"]),
    "pH after partial neutralisation of a strong acid by a strong base",
    "H⁺ and OH⁻ neutralise mole for mole. The excess H⁺ is spread over the total volume of the mixture.",
    ["H⁺ = 50 × 0.2 = 10 mmol; OH⁻ = 50 × 0.1 = 5 mmol", "Excess H⁺ = 5 mmol in 100 mL → [H⁺] = 0.05 M",
     "pH = −log(0.05) = 2 − log 5 = 2 − 0.70 = 1.30"],
    why="1.00 forgets that the volume doubles (uses 50 mL). 0.70 ignores the neutralisation and uses 0.2 M. "
        "12.70 treats the base as the reagent in excess.",
    seconds=80, checked=True)

add("Kp, Kc and Le Chatelier", A, "statement_pair",
    sp("At a fixed temperature, the value of K_c for a reaction changes when the concentration of one of the "
       "reactants is increased.",
       "A catalyst increases the equilibrium constant of a reaction."),
    SP_, "What can and cannot change an equilibrium constant",
    "Adding a reactant changes Q, and the system shifts until Q = K again, but K itself depends only on "
    "temperature: Statement I is false. A catalyst lowers the activation energy of the forward and reverse "
    "reactions equally; equilibrium is reached faster, but K is unchanged: Statement II is false.",
    ["K_c depends only on temperature (for a given reaction as written) → Statement I false",
     "Catalyst speeds up both directions equally → K unchanged → Statement II false"],
    answer="B", ncert=f"{REF6}, factors affecting equilibria", seconds=45)

add("Hydrolysis and buffers", A, "multi_statement",
    ms("Which of the following statements about buffer solutions are correct? (pK_a of CH₃COOH = 4.74, pK_b of "
       "NH₄OH = 4.75)",
       ["A mixture of CH₃COOH and CH₃COONa is an acidic buffer.",
        "A mixture of HCl and NaCl acts as a buffer.",
        "For an acidic buffer, pH = pK_a when the concentrations of the salt and the acid are equal.",
        "A buffer of pH about 9 can be prepared from CH₃COOH and CH₃COONa.",
        "A mixture of NH₄OH and NH₄Cl is a basic buffer."]),
    multi({"a": True, "b": False, "c": True, "d": False, "e": True}, "(a), (c) and (e) only",
          ["(a), (b) and (c) only", "(a), (c), (d) and (e) only", "(c) and (e) only"]),
    "Composition and pH range of buffers",
    "A buffer needs a weak acid with its salt (acidic buffer) or a weak base with its salt (basic buffer). By the "
    "Henderson–Hasselbalch equation, pH = pK_a + log([salt]/[acid]); a weak acid–salt buffer works only within "
    "about one unit of its pK_a.",
    ["(a) True: weak acid + its salt", "(b) False: HCl is a strong acid; no reservoir to absorb added H⁺ or OH⁻",
     "(c) True: log 1 = 0 → pH = pK_a",
     "(d) False: an acetate buffer gives pH near 4.74 (about 3.7 to 5.7); pH 9 needs a basic buffer such as "
     "NH₄OH/NH₄Cl (pH = 14 − pK_b ≈ 9.25)",
     "(e) True: weak base + its salt"],
    ncert=f"{REF6}, buffer solutions", seconds=75)

# ==================================================================== 7. Redox Reactions and Electrochemistry
topic("Redox Reactions and Electrochemistry")
REF7R, REF7E = f"{C11}, 'Redox Reactions'", f"{C12}, 'Electrochemistry'"

on = {"Mn": (0 - (1 - 4 * 2)) / 1, "Cr": (0 - (2 * 1 - 7 * 2)) / 2, "P": (0 - (3 * 1 - 3 * 2)) / 1,
      "N": (1 - 4 * 1) / 1}
num = {"I": 6, "II": -3, "III": 7, "IV": 3}
got = {k: next(r for r, v in num.items() if v == on[e]) for k, e in zip("ABCD", on)}
assert got == {"A": "III", "B": "I", "C": "IV", "D": "II"}
add("Oxidation number and balancing", B, "match_list",
    lists("Match List-I (element in a species) with List-II (its oxidation number).",
          ["Mn in KMnO₄", "Cr in K₂Cr₂O₇", "P in H₃PO₃", "N in NH₄⁺"], ["+6", "−3", "+7", "+3"]),
    match(got, [{"A": "I", "B": "III", "C": "IV", "D": "II"}, {"A": "III", "B": "I", "C": "II", "D": "IV"},
                {"A": "III", "B": "IV", "C": "I", "D": "II"}]),
    "Rules for assigning oxidation numbers",
    "Take K = +1, H = +1 and O = −2, and set the sum of oxidation numbers equal to the charge on the species.",
    ["KMnO₄: 1 + x − 8 = 0 → x = +7 → III", "K₂Cr₂O₇: 2 + 2x − 14 = 0 → x = +6 → I",
     "H₃PO₃: 3 + x − 6 = 0 → x = +3 → IV", "NH₄⁺: x + 4 = +1 → x = −3 → II"],
    ncert=f"{REF7R}, oxidation number", seconds=45, checked=True)

add("Batteries and fuel cells", B, "direct",
    "Which of the following was used to provide electrical power in the Apollo space programme, with the water it "
    "produced being added to the astronauts' drinking water?",
    Flex("Hydrogen–oxygen fuel cell", ["Dry (Leclanché) cell", "Lead storage battery", "Daniell cell"]),
    "Fuel cells",
    "A fuel cell converts the energy of combustion of a fuel such as hydrogen directly into electrical energy. In "
    "the H₂–O₂ fuel cell the overall reaction is 2H₂(g) + O₂(g) → 2H₂O(l), so its only product is water. Such cells "
    "powered the Apollo spacecraft, and the water vapour formed was condensed and added to the drinking water.",
    ["Overall reaction of the H₂–O₂ fuel cell: 2H₂ + O₂ → 2H₂O", "Only product: water → usable as drinking water",
     "Used in the Apollo space programme"],
    why="The dry cell and the lead storage battery store a fixed amount of reactants and give no water; the Daniell "
        "cell is a laboratory cell that gives Zn²⁺ and Cu, not water.",
    ncert=f"{REF7E}, fuel cells", seconds=30)

add("Conductance and Kohlrausch's law", B, "statement_pair",
    sp("The conductivity (κ) of an electrolyte solution increases on dilution.",
       "The molar conductivity of an aqueous KCl solution decreases on dilution."),
    SP_, "Variation of conductivity and molar conductivity with concentration",
    "Conductivity is the conductance of a unit volume of solution; on dilution there are fewer ions per unit "
    "volume, so κ decreases: Statement I is false. Molar conductivity is the conductance of all the ions from one "
    "mole of electrolyte; for a strong electrolyte such as KCl, interionic attractions weaken on dilution, so Λm "
    "increases: Statement II is false.",
    ["κ decreases on dilution (fewer ions per cm³) → Statement I false",
     "Λm of KCl increases on dilution → Statement II false"],
    answer="B", ncert=f"{REF7E}, variation of conductivity and molar conductivity with concentration",
    seconds=40)

add("Electrode potential and cells", B, "direct",
    "Given the standard reduction potentials Li⁺/Li = −3.05 V, Zn²⁺/Zn = −0.76 V, Cu²⁺/Cu = +0.34 V and "
    "Ag⁺/Ag = +0.80 V, the strongest reducing agent among the four metals is:",
    Flex("Li", ["Zn", "Cu", "Ag"]),
    "Electrochemical series",
    "The more negative the standard reduction potential, the less the ion wants to be reduced and the more "
    "readily the metal is oxidised, so the stronger the metal is as a reducing agent.",
    ["Most negative E°: Li⁺/Li (−3.05 V)", "Li loses electrons most readily → strongest reducing agent"],
    why="Ag has the most positive E°, so Ag⁺ is the best oxidising agent and Ag the weakest reducing agent.",
    ncert=f"{REF7E}, electrochemical series", seconds=30)

lam = 426 + 105 - 126
assert lam == 405 and 426 + 105 + 126 == 657 and 426 + 126 - 105 == 447 and 426 - 105 - 126 == 195
add("Conductance and Kohlrausch's law", I, "numerical",
    "The limiting molar conductivities (in S cm² mol⁻¹) of HCl, HCOONa and NaCl at 298 K are 426, 105 and 126 "
    "respectively. The limiting molar conductivity of HCOOH (in S cm² mol⁻¹) is:",
    Flex("405", ["657", "447", "195"]),
    "Kohlrausch's law of independent migration of ions",
    "Λ°m of an electrolyte is the sum of the limiting ionic conductivities of its ions. Combine the given values so "
    "that only H⁺ and HCOO⁻ remain.",
    ["Λ°(HCOOH) = λ°(H⁺) + λ°(HCOO⁻)", "= Λ°(HCl) + Λ°(HCOONa) − Λ°(NaCl)",
     "= 426 + 105 − 126 = 405 S cm² mol⁻¹"],
    why="657 adds all three. 447 adds NaCl and subtracts HCOONa, which leaves Na⁺ and Cl⁻ in the sum. 195 "
        "subtracts both salts from HCl.",
    ncert=f"{REF7E}, Kohlrausch's law and its applications", seconds=50, checked=True)

e_cell = 0.80 - 0.34
dg = -2 * 96500 * e_cell / 1000
assert close(e_cell, 0.46) and round(dg, 1) == -88.8 and round(dg / 2, 1) == -44.4
assert round(-2 * 96500 * (0.80 + 0.34) / 1000, 1) == -220.0
add("Nernst equation and Gibbs energy", I, "numerical",
    "For the cell Cu(s) | Cu²⁺(aq, 1 M) || Ag⁺(aq, 1 M) | Ag(s), the standard Gibbs energy change of the cell "
    "reaction is (E°(Ag⁺/Ag) = +0.80 V, E°(Cu²⁺/Cu) = +0.34 V, F = 96 500 C mol⁻¹):",
    Flex("−88.8 kJ mol⁻¹", ["−44.4 kJ mol⁻¹", "+88.8 kJ mol⁻¹", "−220.0 kJ mol⁻¹"]),
    "ΔG° = −nFE°cell",
    "Cell reaction: Cu + 2Ag⁺ → Cu²⁺ + 2Ag, so two electrons are transferred. E°cell = E°cathode − E°anode.",
    ["E°cell = 0.80 − 0.34 = 0.46 V", "n = 2", "ΔG° = −2 × 96 500 × 0.46 = −88 780 J ≈ −88.8 kJ mol⁻¹"],
    why="−44.4 kJ uses n = 1 (the 2 in 2Ag⁺ is not a reason to halve). +88.8 kJ has the wrong sign for a cell "
        "that works spontaneously. −220.0 kJ adds the two electrode potentials.",
    ncert=f"{REF7E}, cell potential and Gibbs energy of the reaction", seconds=75, checked=True)

kappa = 1.29 / 100
lam_m = kappa * 1000 / 0.1
assert close(lam_m, 129) and close(kappa / 0.1, 0.129) and close(kappa * 1000, 12.9)
add("Conductance and Kohlrausch's law", I, "numerical",
    "A conductivity cell with cell constant 1.29 cm⁻¹ shows a resistance of 100 Ω when filled with 0.1 M KCl "
    "solution. The molar conductivity of the solution is:",
    Flex("129 S cm² mol⁻¹", ["0.129 S cm² mol⁻¹", "12.9 S cm² mol⁻¹", "1.29 × 10⁶ S cm² mol⁻¹"]),
    "κ = G*/R and Λm = κ × 1000/C (κ in S cm⁻¹, C in mol L⁻¹)",
    "First get the conductivity from the cell constant and resistance, then convert to molar conductivity. The "
    "factor 1000 converts litres to cm³.",
    ["κ = G*/R = 1.29/100 = 0.0129 S cm⁻¹", "Λm = κ × 1000/C = 0.0129 × 1000/0.1 = 129 S cm² mol⁻¹"],
    why="0.129 leaves out the factor 1000. 12.9 uses C = 1 M. 1.29 × 10⁶ multiplies the cell constant by R "
        "instead of dividing.",
    ncert=f"{REF7E}, measurement of the conductivity of ionic solutions", seconds=70, checked=True)

add("Conductance and Kohlrausch's law", I, "assertion_reason",
    ar("The molar conductivity of acetic acid increases steeply on dilution.",
       "The limiting molar conductivity of a weak electrolyte cannot be obtained by extrapolating its Λm versus √c "
       "graph to zero concentration."),
    AR_, "Weak electrolytes: molar conductivity and degree of dissociation",
    "Acetic acid is a weak electrolyte. On dilution its degree of dissociation rises sharply, so the number of "
    "ions from one mole rises and Λm increases steeply: A is true. Because Λm rises so steeply near zero "
    "concentration, its graph against √c cannot be extrapolated; Λ°m is found with Kohlrausch's law instead: R is "
    "true. But R is a consequence of the steep rise, not its cause; the cause is the increase in the degree of "
    "dissociation.",
    ["Weak electrolyte: α increases sharply on dilution → Λm rises steeply → A true",
     "Λ°m found from Kohlrausch's law, not by extrapolation → R true",
     "R does not explain A"],
    answer="B", ncert=f"{REF7E}, variation of molar conductivity with concentration", seconds=50)

add("Batteries and fuel cells", I, "match_list",
    lists("Match List-I (electrode of a commercial cell) with List-II (reaction taking place at it).",
          ["Anode of the dry (Leclanché) cell", "Cathode of the dry (Leclanché) cell",
           "Anode of the lead storage battery during discharge", "Cathode of the hydrogen–oxygen fuel cell"],
          ["Pb(s) + SO₄²⁻(aq) → PbSO₄(s) + 2e⁻", "O₂(g) + 2H₂O(l) + 4e⁻ → 4OH⁻(aq)", "Zn(s) → Zn²⁺ + 2e⁻",
           "MnO₂ + NH₄⁺ + e⁻ → MnO(OH) + NH₃"]),
    match({"A": "III", "B": "IV", "C": "I", "D": "II"},
          [{"A": "I", "B": "IV", "C": "III", "D": "II"}, {"A": "III", "B": "II", "C": "I", "D": "IV"},
           {"A": "IV", "B": "III", "C": "I", "D": "II"}]),
    "Electrode reactions in the dry cell, lead storage battery and fuel cell",
    "Oxidation (loss of electrons) takes place at the anode and reduction (gain of electrons) at the cathode. The "
    "two oxidation half-reactions belong to the two anodes: zinc in the dry cell and lead in the lead storage "
    "battery. Of the two reductions, the one involving MnO₂ and NH₄⁺ belongs to the dry cell and the reduction of "
    "O₂ to OH⁻ in alkaline electrolyte to the fuel cell.",
    ["Dry cell anode: the zinc container is oxidised, Zn → Zn²⁺ + 2e⁻ → III",
     "Dry cell cathode: MnO₂ is reduced, MnO₂ + NH₄⁺ + e⁻ → MnO(OH) + NH₃ → IV",
     "Lead storage battery anode (discharge): Pb + SO₄²⁻ → PbSO₄ + 2e⁻ → I",
     "H₂–O₂ fuel cell cathode: O₂ + 2H₂O + 4e⁻ → 4OH⁻ → II"],
    why="Swapping the two dry-cell electrodes puts an oxidation at the cathode, and matching zinc to the lead "
        "battery (or lead to the dry cell) mixes up which metal each anode is made of.",
    ncert=f"{REF7E}, batteries and fuel cells", seconds=50)

add("Oxidation number and balancing", A, "multi_statement",
    ms("Which of the following statements are correct?",
       ["The oxidation number of oxygen in OF₂ is +2.", "The oxidation number of oxygen in H₂O₂ is −1.",
        "The oxidation number of oxygen in KO₂ is −½.", "The oxidation number of hydrogen in NaH is +1.",
        "The reaction 2H₂O₂ → 2H₂O + O₂ is a disproportionation reaction."]),
    multi({"a": True, "b": True, "c": True, "d": False, "e": True}, "(a), (b), (c) and (e) only",
          ["(a), (b) and (d) only", "(b), (c), (d) and (e) only", "(a), (c) and (e) only"]),
    "Exceptions in oxidation numbers; disproportionation",
    "Fluorine is always −1, so oxygen in OF₂ is +2. In peroxides oxygen is −1 and in superoxides −½. In metal "
    "hydrides hydrogen is −1. In 2H₂O₂ → 2H₂O + O₂ oxygen goes from −1 to both −2 and 0.",
    ["(a) True: x + 2(−1) = 0 → +2", "(b) True: peroxide → −1", "(c) True: +1 + 2x = 0 → x = −½",
     "(d) False: in NaH, H is −1 (hydride)", "(e) True: O (−1) is both reduced to −2 and oxidised to 0"],
    ncert=f"{REF7R}, oxidation number and types of redox reactions", seconds=60)

e_h = -0.059 * 3
assert close(e_h, -0.177) and close(-0.059 / 2 * 3, -0.0885)
add("Nernst equation and Gibbs energy", A, "numerical",
    "A hydrogen electrode (H₂ gas at 1 bar) is dipped in a solution of pH 3 at 298 K. Its reduction potential is "
    "(2.303 RT/F = 0.059 V):",
    Flex("−0.177 V", ["+0.177 V", "−0.059 V", "−0.089 V"]),
    "Nernst equation for the hydrogen electrode",
    "H⁺ + e⁻ → ½H₂. With p(H₂) = 1 bar, E = E° − 0.059 log(1/[H⁺]) = −0.059 pH.",
    ["E° = 0 for the standard hydrogen electrode", "E = −0.059 × pH = −0.059 × 3", "E = −0.177 V"],
    why="+0.177 V has the sign of the log term reversed. −0.059 V ignores the pH. −0.089 V divides by n = 2 for "
        "2H⁺ + 2e⁻ → H₂ without squaring [H⁺] in the quotient.",
    ncert=f"{REF7E}, Nernst equation", seconds=60, checked=True)

logk = 2 * 0.295 / 0.059
assert close(logk, 10) and close(0.295 / 0.059, 5)
add("Nernst equation and Gibbs energy", A, "numerical",
    "The standard emf of a cell in which two electrons are transferred in the cell reaction is 0.295 V at 298 K. "
    "The equilibrium constant of the cell reaction is (2.303 RT/F = 0.059 V):",
    Flex("1 × 10¹⁰", ["1 × 10⁵", "1 × 10²⁰", "1 × 10⁻¹⁰"]),
    "Equilibrium constant from E°cell: log K = nE°/0.059",
    "At equilibrium Ecell = 0, so E° = (0.059/n) log K.",
    ["log K = nE°/0.059 = 2 × 0.295/0.059 = 10", "K = 10¹⁰"],
    why="1 × 10⁵ uses n = 1. 1 × 10²⁰ multiplies by n twice. 1 × 10⁻¹⁰ has the sign wrong; a positive E° means "
        "K > 1.",
    ncert=f"{REF7E}, equilibrium constant from Nernst equation", seconds=50, checked=True)

mmol_fe = 50 * 0.1
v_mno4 = mmol_fe / 5 / 0.1
assert close(v_mno4, 10) and close(mmol_fe * 5 / 0.1, 250) and round(mmol_fe / 6 / 0.1, 1) == 8.3
add("Oxidation number and balancing", A, "numerical",
    "In acidic medium, MnO₄⁻ oxidises Fe²⁺ to Fe³⁺ and is itself reduced to Mn²⁺. The volume of 0.1 M KMnO₄ "
    "needed to oxidise 50 mL of 0.1 M FeSO₄ completely is:",
    Flex("10 mL", ["50 mL", "250 mL", "8.3 mL"]),
    "Balanced redox equation (ion–electron method) and stoichiometry",
    "Mn goes from +7 to +2 (gains 5 electrons) while each Fe²⁺ loses 1 electron, so one MnO₄⁻ oxidises five Fe²⁺: "
    "MnO₄⁻ + 5Fe²⁺ + 8H⁺ → Mn²⁺ + 5Fe³⁺ + 4H₂O.",
    ["Fe²⁺ = 50 × 0.1 = 5 mmol", "MnO₄⁻ needed = 5/5 = 1 mmol", "Volume = 1 mmol / 0.1 M = 10 mL"],
    why="50 mL assumes a 1 : 1 ratio. 250 mL multiplies by 5 instead of dividing. 8.3 mL uses the 1 : 6 ratio that "
        "belongs to dichromate.",
    ncert=f"{REF7R}, balancing of redox reactions", seconds=80, checked=True)

# ==================================================================== 8. Chemical Kinetics
topic("Chemical Kinetics")
REF8 = f"{C12}, 'Chemical Kinetics'"

add("Rate law and order", B, "direct",
    "The unit of the rate constant of a zero-order reaction is:",
    Flex("mol L⁻¹ s⁻¹", ["s⁻¹", "L mol⁻¹ s⁻¹", "L² mol⁻² s⁻¹"]),
    "Units of rate constant: (mol L⁻¹)¹⁻ⁿ s⁻¹",
    "For a zero-order reaction, rate = k[R]⁰ = k, so k has the same unit as the rate.",
    ["Rate = k → unit of k = unit of rate = mol L⁻¹ s⁻¹", "First order: s⁻¹; second: L mol⁻¹ s⁻¹; third: "
     "L² mol⁻² s⁻¹"],
    ncert=f"{REF8}, units of rate constant", seconds=25)

t_half = 0.693 / 6.93e-3
assert close(t_half, 100) and close(1 / 6.93e-3, 144.3) and close(2.303 / 6.93e-3, 332.3)
assert close(0.693 * 6.93e-3, 4.8e-3, 0.01)
add("Half-life", B, "numerical",
    "The rate constant of a first-order reaction is 6.93 × 10⁻³ s⁻¹. Its half-life is:",
    Flex("100 s", ["144 s", "332 s", "4.8 × 10⁻³ s"]),
    "Half-life of a first-order reaction: t½ = 0.693/k",
    "For a first-order reaction the half-life depends only on k.",
    ["t½ = 0.693/k = 0.693/(6.93 × 10⁻³ s⁻¹)", "t½ = 100 s"],
    why="144 s is 1/k. 332 s is 2.303/k. 4.8 × 10⁻³ s multiplies 0.693 by k instead of dividing.",
    ncert=f"{REF8}, half-life of a reaction", seconds=30, checked=True)

add("Rate law and order", B, "statement_pair",
    sp("The molecularity of a reaction can be zero or a fraction.",
       "The order of a reaction is found experimentally and can be zero or a fraction."),
    SP_, "Order versus molecularity",
    "Molecularity is the number of species colliding in an elementary step, so it is always a small whole number "
    "(1, 2 or 3): Statement I is false. Order is the sum of the powers of concentrations in the experimentally "
    "found rate law, and it can be 0, a fraction or a whole number: Statement II is true.",
    ["Molecularity: whole number, never zero → Statement I false",
     "Order: experimental, may be zero or fractional → Statement II true"],
    answer="D", ncert=f"{REF8}, molecularity of a reaction", seconds=35)

data = [(0.1, 0.1, 2e-3), (0.2, 0.1, 4e-3), (0.1, 0.2, 8e-3)]
order_a = math.log2(data[1][2] / data[0][2])
order_b = math.log2(data[2][2] / data[0][2])
assert round(order_a) == 1 and round(order_b) == 2
add("Rate law and order", I, "direct",
    "For the reaction A + B → products, the following initial rates were measured at the same temperature:\n\n"
    "Experiment 1: [A] = 0.1 M, [B] = 0.1 M, rate = 2.0 × 10⁻³ mol L⁻¹ s⁻¹\n"
    "Experiment 2: [A] = 0.2 M, [B] = 0.1 M, rate = 4.0 × 10⁻³ mol L⁻¹ s⁻¹\n"
    "Experiment 3: [A] = 0.1 M, [B] = 0.2 M, rate = 8.0 × 10⁻³ mol L⁻¹ s⁻¹\n\n"
    "The rate law for the reaction is:",
    Flex("Rate = k[A][B]²", ["Rate = k[A]²[B]", "Rate = k[A][B]", "Rate = k[A]²[B]²"]),
    "Finding orders by the initial rate method",
    "Change one concentration at a time and see how the rate changes: if doubling a concentration multiplies the "
    "rate by 2ⁿ, the order with respect to that reactant is n.",
    ["Expts 1 → 2: [A] doubled, rate doubled → order in A = 1",
     "Expts 1 → 3: [B] doubled, rate × 4 → order in B = 2", "Rate = k[A][B]² (overall order 3)"],
    why="Rate = k[A]²[B] swaps the two orders. The other two options do not match the factor of 4 for B and 2 for A.",
    ncert=f"{REF8}, rate law and order of a reaction", seconds=60, checked=True)

ea = 2.303 * 8.314 * 0.301 * (300 * 310 / 10)
assert round(ea / 1000, 1) == 53.6 and round(8.314 * 0.301 * 9300 / 1000, 1) == 23.3
assert round(2.303 * 8.314 * 0.693 * 9300 / 1000, 1) == 123.4
add("Arrhenius equation and activation energy", I, "numerical",
    "The rate constant of a reaction doubles when the temperature is raised from 300 K to 310 K. The activation "
    "energy of the reaction is (R = 8.314 J K⁻¹ mol⁻¹, log 2 = 0.301):",
    Flex("53.6 kJ mol⁻¹", ["23.3 kJ mol⁻¹", "123.4 kJ mol⁻¹", "53.6 J mol⁻¹"]),
    "Arrhenius equation at two temperatures: log(k₂/k₁) = (Eₐ/2.303R)(T₂ − T₁)/(T₁T₂)",
    "Put k₂/k₁ = 2 and rearrange for Eₐ.",
    ["Eₐ = 2.303 R log(k₂/k₁) × T₁T₂/(T₂ − T₁)", "= 2.303 × 8.314 × 0.301 × (300 × 310/10)",
     "= 5.763 × 9300 = 53 600 J mol⁻¹ ≈ 53.6 kJ mol⁻¹"],
    why="23.3 kJ leaves out the 2.303 while using log. 123.4 kJ uses ln 2 (0.693) together with 2.303. 53.6 J "
        "mixes up the units: the calculation gives 53 600 J mol⁻¹, which is 53.6 kJ mol⁻¹.",
    ncert=f"{REF8}, temperature dependence of the rate of a reaction", seconds=100, checked=True)

add("Arrhenius equation and activation energy", I, "assertion_reason",
    ar("The rate of most chemical reactions increases with rise in temperature.",
       "A rise in temperature increases the activation energy of the reaction."),
    AR_, "Effect of temperature on rate",
    "Rates generally increase with temperature (often roughly doubling for a 10 K rise): A is true. Temperature "
    "does not raise the activation energy; it increases the fraction of molecules whose energy is equal to or "
    "greater than Eₐ (the Maxwell–Boltzmann curve shifts to higher energies), so more collisions are effective. "
    "R is false.",
    ["Higher T → larger fraction of molecules with E ≥ Eₐ → faster reaction → A true",
     "Eₐ is a property of the reaction path, practically independent of temperature → R false"],
    answer="C", ncert=f"{REF8}, temperature dependence of the rate of a reaction", seconds=40)

add("Rate law and order", I, "multi_statement",
    ms("Which of the following statements are correct?",
       ["Acid-catalysed hydrolysis of ethyl acetate in a large excess of water follows pseudo first-order kinetics.",
        "For 2HI(g) → H₂(g) + I₂(g), rate = −½ d[HI]/dt = d[H₂]/dt.",
        "For 2N₂O₅ → 4NO₂ + O₂, the rate of formation of NO₂ equals the rate of disappearance of N₂O₅.",
        "The rate constant of a reaction depends on the initial concentrations of the reactants.",
        "A reaction with rate = k[A]^½[B]² has an overall order of 2.5."]),
    multi({"a": True, "b": True, "c": False, "d": False, "e": True}, "(a), (b) and (e) only",
          ["(a), (b) and (c) only", "(b), (d) and (e) only", "(a), (c), (d) and (e) only"]),
    "Rate expressions, rate constant and order",
    "When water is in large excess its concentration hardly changes, so the reaction behaves as first order. "
    "Rates are written with each concentration change divided by its stoichiometric coefficient. The rate "
    "constant depends on temperature, not on concentration. Order is the sum of the exponents.",
    ["(a) True: pseudo first order", "(b) True: divide by coefficients",
     "(c) False: d[NO₂]/dt = 2 × (−d[N₂O₅]/dt), since 4 NO₂ form per 2 N₂O₅",
     "(d) False: k is independent of concentration", "(e) True: ½ + 2 = 2.5"],
    ncert=f"{REF8}, rate of a chemical reaction and pseudo first-order reactions", seconds=70)

lg = 4.606e-3 * 300 / 2.303
remaining = 10 ** -lg
assert close(lg, 0.6) and close(1 - remaining, 0.75, 0.01)
add("Zero and first order reactions", A, "numerical",
    "The rate constant of a first-order reaction is 4.606 × 10⁻³ s⁻¹. The percentage of the reactant decomposed "
    "after 300 s is approximately (log 4 = 0.602):",
    Flex("75%", ["25%", "60%", "40%"]),
    "Integrated rate law for a first-order reaction: k = (2.303/t) log([R]₀/[R])",
    "Find log([R]₀/[R]), take the antilog to get the fraction remaining, then subtract from 100%.",
    ["log([R]₀/[R]) = kt/2.303 = 4.606 × 10⁻³ × 300/2.303 = 0.6", "[R]₀/[R] = antilog 0.6 ≈ 4 → [R] = [R]₀/4",
     "Remaining = 25% → decomposed = 75%"],
    why="25% is the fraction that remains, not the fraction decomposed. 60% reads the value of the log as a "
        "percentage. 40% is 100% minus that same misreading.",
    ncert=f"{REF8}, first order reactions", seconds=100, checked=True)

ratio_cat = 10 ** (17.22 / 5.74)
assert close(ratio_cat, 1000) and close(math.exp(3), 20.1)
add("Arrhenius equation and activation energy", A, "numerical",
    "A catalyst lowers the activation energy of a reaction by 17.22 kJ mol⁻¹ at 300 K, without changing the "
    "pre-exponential factor. The rate of the catalysed reaction is how many times the rate of the uncatalysed "
    "reaction? (2.303 RT = 5.74 kJ mol⁻¹ at 300 K)",
    Flex("1000", ["3", "20.1", "0.001"]),
    "Effect of a catalyst through the Arrhenius equation: k = A e^(−Eₐ/RT)",
    "With the same A, k_cat/k = e^(ΔEₐ/RT), so log(k_cat/k) = ΔEₐ/(2.303 RT).",
    ["log(k_cat/k) = 17.22/5.74 = 3", "k_cat/k = 10³ = 1000"],
    why="3 is the value of the log, not the ratio. 20.1 is e³, which treats 5.74 kJ mol⁻¹ as RT. 0.001 inverts "
        "the ratio, as if the catalyst slowed the reaction.",
    ncert=f"{REF8}, effect of catalyst", seconds=80, checked=True)

add("Zero and first order reactions", A, "match_list",
    lists("Match List-I (plot) with List-II (its form).",
          ["[R] versus t for a zero-order reaction", "ln[R] versus t for a first-order reaction",
           "t½ versus [R]₀ for a zero-order reaction", "t½ versus [R]₀ for a first-order reaction"],
          ["Straight line with slope −k and intercept ln[R]₀",
           "Straight line parallel to the [R]₀ axis (t½ independent of [R]₀)",
           "Straight line with slope −k and intercept [R]₀",
           "Straight line through the origin with slope 1/(2k)"]),
    match({"A": "III", "B": "I", "C": "IV", "D": "II"},
          [{"A": "I", "B": "III", "C": "IV", "D": "II"}, {"A": "III", "B": "I", "C": "II", "D": "IV"},
           {"A": "IV", "B": "I", "C": "III", "D": "II"}]),
    "Integrated rate laws and half-lives of zero- and first-order reactions",
    "Zero order: [R] = [R]₀ − kt and t½ = [R]₀/2k. First order: ln[R] = ln[R]₀ − kt and t½ = 0.693/k.",
    ["[R] = −kt + [R]₀ → slope −k, intercept [R]₀ → III", "ln[R] = −kt + ln[R]₀ → slope −k, intercept ln[R]₀ → I",
     "t½ = [R]₀/2k → line through the origin, slope 1/2k → IV", "t½ = 0.693/k → constant → II"],
    ncert=f"{REF8}, integrated rate equations", seconds=60)

# ==================================================================== 9. Classification of Elements and Periodicity
topic("Classification of Elements and Periodicity in Properties")
REF9 = f"{C11}, 'Classification of Elements and Periodicity in Properties'"

add("Modern periodic table", B, "direct",
    "In the modern (long form) periodic table, the period number of an element corresponds to:",
    Flex("The principal quantum number (n) of its outermost shell",
         ["The number of its valence electrons", "The number of electrons in its penultimate shell",
          "The azimuthal quantum number of its last electron"]),
    "Structure of the long form of the periodic table",
    "Each period starts with the filling of a new principal energy level, so the period number equals the value "
    "of n for the outermost (valence) shell.",
    ["Period 1: n = 1 (H, He)", "Period 3: n = 3 (Na to Ar), and so on",
     "Valence electrons relate to the group, not the period"],
    ncert=f"{REF9}, modern periodic law and the present form of the periodic table", seconds=25)

add("Valence and reactivity", B, "direct",
    "Which of the following oxides is amphoteric?",
    Flex("Al₂O₃", ["Na₂O", "Cl₂O₇", "MgO"]),
    "Periodic trend in the nature of oxides",
    "Across a period, oxides change from strongly basic (left) to strongly acidic (right). Aluminium oxide lies "
    "between and reacts with both acids and bases.",
    ["Na₂O and MgO: basic", "Al₂O₃: amphoteric", "Cl₂O₇: strongly acidic"],
    ncert=f"{REF9}, periodic trends in chemical properties", seconds=25)

add("Atomic and ionic radii", B, "statement_pair",
    sp("Atomic radius generally decreases from left to right across a period.",
       "Noble gases have large positive electron gain enthalpies."),
    SP_, "Periodic trends in atomic radius and electron gain enthalpy",
    "Across a period, the nuclear charge increases while electrons enter the same shell, so the outer electrons "
    "are pulled closer: Statement I is true. A noble gas would have to place an added electron in a new, higher "
    "shell, which is very unfavourable, so its electron gain enthalpy is large and positive: Statement II is true.",
    ["Same shell, rising effective nuclear charge → smaller atoms across a period → Statement I true",
     "Added electron must enter the next shell → large positive ΔegH → Statement II true"],
    answer="A", ncert=f"{REF9}, atomic radius and electron gain enthalpy", seconds=35)

add("Ionisation and electron gain enthalpy", I, "assertion_reason",
    ar("The first ionisation enthalpy of nitrogen is higher than that of oxygen.",
       "Nitrogen has a stable half-filled 2p³ configuration, while in oxygen one 2p orbital holds a pair of "
       "electrons whose mutual repulsion makes one of them easier to remove."),
    AR_, "Irregularities in ionisation enthalpy across a period",
    "Ionisation enthalpy usually rises across a period, but oxygen's is lower than nitrogen's. In N each 2p "
    "electron is in a different orbital (half-filled, stable). In O the fourth 2p electron pairs up, and the "
    "repulsion between the paired electrons makes it easier to remove. R explains A.",
    ["N: 2p_x¹ 2p_y¹ 2p_z¹ (half-filled)", "O: 2p_x² 2p_y¹ 2p_z¹; the paired electron is repelled by its partner",
     "So ΔiH₁(N) > ΔiH₁(O)"],
    answer="A", ncert=f"{REF9}, ionization enthalpy", seconds=40)

add("Modern periodic table", I, "multi_statement",
    ms("Which of the following statements about the modern periodic table are correct?",
       ["Elements of groups 1 and 2 make up the s-block.", "The p-block consists of groups 13 to 18.",
        "The third period contains 18 elements.",
        "Elements in the same period have the same number of valence electrons.",
        "The d-block elements occupy groups 3 to 12."]),
    multi({"a": True, "b": True, "c": False, "d": False, "e": True}, "(a), (b) and (e) only",
          ["(a), (b) and (c) only", "(b), (d) and (e) only", "(a), (c) and (d) only"]),
    "Blocks, groups and periods",
    "The blocks are named after the subshell being filled. The third period fills only 3s and 3p, so it has 8 "
    "elements. Elements in the same group, not the same period, have the same number of valence electrons.",
    ["(a) True: s-block = groups 1 and 2", "(b) True: p-block = groups 13–18",
     "(c) False: period 3 has 8 elements (Na to Ar)", "(d) False: valence electrons are the same within a group",
     "(e) True: d-block = groups 3–12"],
    ncert=f"{REF9}, electronic configurations and types of elements", seconds=45)

pos = {37: "Group 1", 35: "Group 17", 26: "Group 8", 58: "f-block"}
right = {"I": "f-block", "II": "Group 17", "III": "Group 1", "IV": "Group 8"}
got = {k: next(r for r, v in right.items() if v == pos[z]) for k, z in zip("ABCD", [37, 35, 26, 58])}
assert got == {"A": "III", "B": "II", "C": "IV", "D": "I"}
add("Modern periodic table", I, "match_list",
    lists("Match List-I (atomic number) with List-II (position in the periodic table).",
          ["Z = 37", "Z = 35", "Z = 26", "Z = 58"],
          ["f-block (lanthanoid)", "Group 17", "Group 1", "Group 8"]),
    match(got, [{"A": "II", "B": "III", "C": "IV", "D": "I"}, {"A": "III", "B": "II", "C": "I", "D": "IV"},
                {"A": "IV", "B": "II", "C": "III", "D": "I"}]),
    "Locating an element from its electronic configuration",
    "Write the configuration, then read the block from the last subshell being filled and the group from the "
    "number of outer electrons.",
    ["Z = 37: [Kr] 5s¹ → group 1 → III", "Z = 35: [Ar] 3d¹⁰ 4s² 4p⁵ → group 17 → II",
     "Z = 26: [Ar] 3d⁶ 4s² → group 8 (d-block) → IV", "Z = 58: [Xe] 4f¹ 5d¹ 6s² → f-block lanthanoid → I"],
    ncert=f"{REF9}, electronic configurations of elements and the periodic table", seconds=55, checked=True)

add("Ionisation and electron gain enthalpy", I, "direct",
    "Which of the following elements has the most negative electron gain enthalpy?",
    Flex("Chlorine", ["Fluorine", "Bromine", "Iodine"]),
    "Electron gain enthalpy of the halogens",
    "Electron gain enthalpy usually becomes less negative down a group, but fluorine is an exception: its 2p "
    "subshell is so small that an added electron feels strong repulsion from the electrons already there. So "
    "chlorine, not fluorine, has the most negative value.",
    ["Small, compact 2p of F → interelectronic repulsion → less negative ΔegH than Cl",
     "Br and I: larger atoms, added electron farther from nucleus → less negative than Cl"],
    ncert=f"{REF9}, electron gain enthalpy", seconds=30)

add("Ionisation and electron gain enthalpy", A, "multi_statement",
    ms("Which of the following comparisons of ionisation enthalpy (ΔiH) are correct?",
       ["ΔiH₁ of Be > ΔiH₁ of B", "ΔiH₁ of Mg > ΔiH₁ of Al", "ΔiH₂ of Na > ΔiH₂ of Mg",
        "ΔiH₁ of Ne < ΔiH₁ of F", "For any element, ΔiH₂ < ΔiH₁"]),
    multi({"a": True, "b": True, "c": True, "d": False, "e": False}, "(a), (b) and (c) only",
          ["(a), (b), (c) and (d) only", "(b), (c) and (e) only", "(a), (d) and (e) only"]),
    "Ionisation enthalpy: penetration, configuration and successive ionisation",
    "A 2s (or 3s) electron penetrates closer to the nucleus than a 2p (or 3p) electron, so Be and Mg hold their "
    "outer electrons more firmly than B and Al. Na⁺ has the stable neon configuration, so removing a second "
    "electron from Na is very hard. Neon has the highest ΔiH₁ in period 2. Removing an electron from a positive "
    "ion always needs more energy.",
    ["(a) True: B loses a 2p electron, which is more shielded than Be's 2s",
     "(b) True: same reason for Al (3p) versus Mg (3s)",
     "(c) True: Na⁺ = [Ne]; Mg⁺ = [Ne] 3s¹ loses a 3s electron easily",
     "(d) False: Ne (noble gas) has a higher ΔiH₁ than F", "(e) False: ΔiH₂ > ΔiH₁ always"],
    ncert=f"{REF9}, ionization enthalpy", seconds=80)

add("Atomic and ionic radii", A, "assertion_reason",
    ar("The atomic radius of gallium is slightly smaller than that of aluminium.",
       "The ten 3d electrons in gallium shield the nucleus poorly, so its outer electrons feel a larger effective "
       "nuclear charge."),
    AR_, "Effect of poor shielding by d electrons",
    "Atomic radius normally increases down a group, but Ga (about 135 pm) is smaller than Al (about 143 pm). "
    "Between Al and Ga the 3d subshell is filled; d electrons shield poorly, so the increased nuclear charge is "
    "felt more strongly by the 4s and 4p electrons. R explains A.",
    ["Expected: radius increases down group 13", "Ga has an extra 3d¹⁰ that shields poorly",
     "Higher effective nuclear charge → Ga slightly smaller than Al"],
    answer="A", ncert=f"{REF9}, atomic radius", seconds=45)

add("Atomic and ionic radii", A, "direct",
    "Which of the following is the correct order of radii of the isoelectronic species?",
    Flex("O²⁻ > F⁻ > Na⁺ > Mg²⁺", ["Mg²⁺ > Na⁺ > F⁻ > O²⁻", "F⁻ > O²⁻ > Na⁺ > Mg²⁺", "Na⁺ > Mg²⁺ > F⁻ > O²⁻"]),
    "Radii of isoelectronic species",
    "All four species have 10 electrons. The greater the nuclear charge, the more strongly these 10 electrons are "
    "pulled in, so the radius falls as the atomic number rises.",
    ["Nuclear charges: O (8) < F (9) < Na (11) < Mg (12)", "Same number of electrons → larger Z, smaller size",
     "Order: O²⁻ > F⁻ > Na⁺ > Mg²⁺"],
    ncert=f"{REF9}, ionic radius", seconds=40)

# ==================================================================== 10. p-Block Elements
topic("p-Block Elements")
REF10A = "Class 11 Chemistry (pre-2023 edition), 'The p-Block Elements'"
REF10B = "Class 12 Chemistry (pre-2023 edition), 'The p-Block Elements'"

add("Group 13 and 14 trends", B, "direct",
    "The general valence-shell electronic configuration of group 14 elements is:",
    Flex("ns² np²", ["ns² np¹", "ns² np³", "ns² np⁴"]),
    "Electronic configuration of p-block groups",
    "Group number − 10 gives the number of valence electrons in the p-block: group 14 has four valence electrons, "
    "two in ns and two in np.",
    ["Group 13: ns² np¹", "Group 14: ns² np² (C, Si, Ge, Sn, Pb)", "Group 15: ns² np³; group 16: ns² np⁴"],
    ncert=f"{REF10A}, group 14 elements", seconds=20)

add("Group 15 and 16 trends", B, "direct",
    "Which element of group 15 is a typical metal?",
    Flex("Bismuth", ["Nitrogen", "Phosphorus", "Arsenic"]),
    "Metallic character down group 15",
    "Metallic character increases down the group as atomic size grows and ionisation enthalpy falls: N and P are "
    "non-metals, As and Sb are metalloids, and Bi is a metal.",
    ["N, P: non-metals", "As, Sb: metalloids", "Bi: metal"],
    ncert=f"{REF10B}, group 15 elements", seconds=25)

add("Anomalous first element", B, "statement_pair",
    sp("Nitrogen exists as a diatomic molecule with a triple bond, whereas phosphorus exists as discrete P₄ "
       "molecules with single bonds.",
       "Nitrogen readily forms pπ–pπ multiple bonds with itself, but the heavier elements of group 15 do not."),
    SP_, "Anomalous behaviour of nitrogen",
    "Because of its small size and high electronegativity, nitrogen forms strong pπ–pπ bonds and exists as N≡N: "
    "both statements are true. The larger p orbitals of phosphorus overlap poorly sideways, so it prefers single "
    "bonds in the tetrahedral P₄ unit.",
    ["N₂: N≡N (one σ + two π) → Statement I true (P₄ has P–P single bonds)",
     "Small N atom → effective pπ–pπ overlap; heavier atoms → weak pπ–pπ → Statement II true"],
    answer="A", ncert=f"{REF10B}, group 15 elements: anomalous properties of nitrogen", seconds=35)

add("Group 17 and 18 trends", B, "direct",
    "Which of the following halogens is the strongest oxidising agent?",
    Flex("F₂", ["Cl₂", "Br₂", "I₂"]),
    "Oxidising power of the halogens",
    "Halogens oxidise by accepting electrons. Fluorine's low F–F bond dissociation enthalpy, high hydration "
    "enthalpy of F⁻ and high electronegativity make F₂ the strongest oxidising agent; oxidising power decreases "
    "down the group.",
    ["Order of oxidising power: F₂ > Cl₂ > Br₂ > I₂"],
    ncert=f"{REF10B}, group 17 elements: chemical properties", seconds=20)

add("Anomalous first element", I, "assertion_reason",
    ar("Nitrogen forms a pentachloride, NCl₅, just as phosphorus forms PCl₅.",
       "Nitrogen has no d orbitals in its valence shell, so its covalency cannot exceed four."),
    AR_, "Maximum covalency of nitrogen",
    "With only 2s and 2p orbitals in its valence shell, nitrogen can form at most four bonds (as in NH₄⁺). So NCl₅ "
    "does not exist: A is false. Phosphorus can use its 3d orbitals to expand its covalency and forms PCl₅. "
    "R is true.",
    ["N: valence shell n = 2 → 2s + three 2p orbitals → maximum covalency 4 → R true",
     "NCl₅ would need five bonds → does not exist → A false"],
    answer="D", ncert=f"{REF10B}, group 15 elements: anomalous properties of nitrogen", seconds=40)

add("Group 15 and 16 trends", I, "multi_statement",
    ms("Which of the following statements about group 16 elements are correct?",
       ["Besides −2, sulphur shows the +4 and +6 oxidation states, which oxygen does not show.",
        "The thermal stability of the hydrides decreases from H₂O to H₂Te.",
        "The acidic character of the hydrides increases from H₂O to H₂Te.",
        "The H–O–H bond angle in H₂O is smaller than the H–S–H bond angle in H₂S.",
        "Like H₂S, water is a gas at room temperature."]),
    multi({"a": True, "b": True, "c": True, "d": False, "e": False}, "(a), (b) and (c) only",
          ["(a), (b) and (d) only", "(b), (c) and (e) only", "(a), (c), (d) and (e) only"]),
    "Trends in group 16",
    "Oxygen has no d orbitals and is more electronegative than every element except fluorine, so it does not show "
    "the +4 and +6 states that S, Se and Te show. Down the group the H–E bond becomes longer and weaker, so the hydrides become less stable and "
    "more acidic. Water is a liquid because of hydrogen bonding.",
    ["(a) True: e.g. SO₂ (+4), SO₃ and H₂SO₄ (+6); no such states for O", "(b) True: H–E bond enthalpy falls from O to Te", "(c) True: weaker H–E bond releases H⁺ more easily",
     "(d) False: H₂O ≈ 104.5°, H₂S ≈ 92°; the angle decreases down the group",
     "(e) False: H₂O is a liquid because of hydrogen bonding"],
    ncert=f"{REF10B}, group 16 elements", seconds=60)

add("Group 17 and 18 trends", I, "assertion_reason",
    ar("HF has a higher boiling point than HCl.", "HF is a stronger acid than HCl in aqueous solution."),
    AR_, "Hydrogen halides: boiling point and acid strength",
    "HF molecules are associated through strong hydrogen bonds, so HF boils at a much higher temperature than HCl: "
    "A is true. In water HF is a weak acid because the H–F bond is very strong; acid strength rises "
    "HF < HCl < HBr < HI. R is false.",
    ["HF: intermolecular hydrogen bonding → higher boiling point → A true",
     "H–F bond strongest → HF is the weakest hydrohalic acid → R false"],
    answer="C", ncert=f"{REF10B}, group 17 elements: hydrogen halides", seconds=40)

stable = {"Tl": 1, "Pb": 2, "Bi": 3, "Sn": 4}
right = {"I": 3, "II": 1, "III": 4, "IV": 2}
got = {k: next(r for r, v in right.items() if v == stable[e]) for k, e in zip("ABCD", stable)}
assert got == {"A": "II", "B": "IV", "C": "I", "D": "III"}
add("Group 13 and 14 trends", I, "match_list",
    lists("Match List-I (element) with List-II (its more stable oxidation state in compounds).",
          ["Thallium", "Lead", "Bismuth", "Tin"], ["+3", "+1", "+4", "+2"]),
    match(got, [{"A": "I", "B": "IV", "C": "II", "D": "III"}, {"A": "II", "B": "III", "C": "I", "D": "IV"},
                {"A": "IV", "B": "II", "C": "I", "D": "III"}]),
    "Inert pair effect",
    "In the heavier p-block elements the ns² electrons are reluctant to take part in bonding, so the oxidation "
    "state two below the group valency becomes more stable down the group. The effect is strong for Tl, Pb and Bi "
    "but weak for Sn.",
    ["Tl (group 13): +1 more stable than +3 → II", "Pb (group 14): +2 more stable than +4 → IV",
     "Bi (group 15): +3 more stable than +5 → I",
     "Sn (group 14): +4 more stable; Sn(II) compounds act as reducing agents → III"],
    why="Tin is the trap: unlike lead, its +4 state is the more stable one.",
    ncert=f"{REF10A}, groups 13 and 14: oxidation states", seconds=50, checked=True)

add("Group 13 and 14 trends", I, "direct",
    "Which of the following group 14 elements shows the greatest tendency for catenation?",
    Flex("Carbon", ["Silicon", "Germanium", "Tin"]),
    "Catenation in group 14",
    "Catenation is the linking of atoms of the same element into chains and rings. It depends on the strength of "
    "the element–element bond. The C–C bond is much stronger than Si–Si, Ge–Ge or Sn–Sn, so carbon catenates the "
    "most; the tendency falls down the group.",
    ["Bond enthalpy: C–C > Si–Si > Ge–Ge ≈ Sn–Sn", "Order of catenation: C ≫ Si > Ge ≈ Sn; Pb shows none"],
    ncert=f"{REF10A}, group 14 elements: anomalous behaviour of carbon", seconds=25)

add("Group 13 and 14 trends", A, "assertion_reason",
    ar("In group 14, the first ionisation enthalpy does not decrease steadily down the group: lead has a slightly "
       "higher first ionisation enthalpy than tin.",
       "In lead, the intervening 4f and 5d electrons shield the nucleus poorly, so the outer 6p electrons feel a "
       "larger effective nuclear charge."),
    AR_, "Irregular trend in ionisation enthalpy down group 14",
    "Ionisation enthalpy is expected to fall down a group as the atoms grow. From Sn to Pb, however, fourteen 4f "
    "electrons (and the 5d electrons) are added; f and d electrons shield the nuclear charge poorly, so the "
    "increase in nuclear charge outweighs the increase in size and Pb holds its outer electrons slightly more "
    "firmly than Sn. A is true, R is true, and R is the reason for A.",
    ["Expected: ΔiH₁ decreases down the group as size increases",
     "Observed: large fall from C to Si, small decreases to Ge and Sn, then a slight rise from Sn to Pb → A true",
     "Pb has filled 4f¹⁴ and 5d¹⁰ subshells that shield poorly → higher effective nuclear charge → R true and "
     "explains A"],
    answer="A", why="Option B is the trap: R is not a separate true fact here; it is exactly the cause of the "
                    "irregularity in A.",
    ncert=f"{REF10A}, group 14 elements: ionisation enthalpy", seconds=50)

add("Anomalous first element", A, "multi_statement",
    ms("Which of the following statements about the first elements of the p-block groups are correct?",
       ["Fluorine shows only the −1 oxidation state in its compounds.",
        "Boron forms the [BF₆]³⁻ ion, just as aluminium forms [AlF₆]³⁻.",
        "Carbon forms pπ–pπ multiple bonds (C=C, C≡C, C=O) readily, whereas silicon rarely does.",
        "The first member of each p-block group has the largest atomic radius in that group.",
        "Fluorine forms only one oxoacid, HOF."]),
    multi({"a": True, "b": False, "c": True, "d": False, "e": True}, "(a), (c) and (e) only",
          ["(a), (b) and (c) only", "(c), (d) and (e) only", "(a), (b), (d) and (e) only"]),
    "Anomalous behaviour of the first member of each group",
    "The first member of each group is the smallest, is highly electronegative and has no d orbitals in its "
    "valence shell. So F has no positive oxidation states and forms only HOF, B cannot exceed covalency 4, and C "
    "forms strong pπ–pπ multiple bonds.",
    ["(a) True: F is the most electronegative element", "(b) False: B has no d orbitals; maximum covalency 4 "
     "([BF₄]⁻)", "(c) True: small C atom → strong pπ–pπ overlap",
     "(d) False: the first member is the smallest", "(e) True: HOF is the only oxoacid of fluorine"],
    why="Boron is the usual trap: aluminium can use 3d orbitals to reach covalency 6, boron cannot.",
    ncert=f"{REF10A}; {REF10B}: anomalous behaviour of the first member", seconds=70)

add("Group 17 and 18 trends", A, "statement_pair",
    sp("The bond dissociation enthalpy of F₂ is smaller than that of Cl₂.",
       "The F–F bond is weakened by repulsion between the lone pairs of the two small fluorine atoms."),
    SP_, "Anomalously low bond enthalpy of F₂",
    "Bond dissociation enthalpy normally decreases down a group, yet F₂ (about 159 kJ mol⁻¹) is weaker than Cl₂ "
    "(about 243 kJ mol⁻¹): Statement I is true. The F atoms are so small that the lone pairs on the two atoms come "
    "close and repel each other strongly: Statement II is true.",
    ["F₂ BDE < Cl₂ BDE → Statement I true", "Small size → strong lone pair–lone pair repulsion → weak F–F bond → "
     "Statement II true"],
    answer="A", ncert=f"{REF10B}, group 17 elements: bond dissociation enthalpy", seconds=45)

add("Group 15 and 16 trends", A, "direct",
    "Which of the following orders for the hydrides of group 15 is correct?",
    Flex("Thermal stability: NH₃ > PH₃ > AsH₃", ["Reducing character: NH₃ > PH₃ > AsH₃",
                                                 "Basic character: AsH₃ > PH₃ > NH₃",
                                                 "Bond angle: AsH₃ > PH₃ > NH₃"]),
    "Trends in group 15 hydrides",
    "Down the group the E–H bond becomes longer and weaker. So thermal stability falls, the hydrides become "
    "stronger reducing agents (they lose hydrogen more easily), the lone pair becomes more diffuse (weaker base), "
    "and the bond angle decreases.",
    ["Thermal stability: NH₃ > PH₃ > AsH₃ (correct)", "Reducing character: AsH₃ > PH₃ > NH₃ (option reversed)",
     "Basicity: NH₃ > PH₃ > AsH₃ (option reversed)", "Bond angle: NH₃ (107.8°) > PH₃ (93.6°) > AsH₃ (91.8°) "
     "(option reversed)"],
    ncert=f"{REF10B}, group 15 elements: hydrides", seconds=50)


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
    doc = {"schema_version": "1.0", "batch_id": "BATCH_001", "created_at": TODAY,
           "notes": "Package CHE_001_p1: 126 original Chemistry questions (physical chemistry, periodicity and "
                    "p-block). Numerical answers re-derived in tools/batch_001/CHE_001_p1.py.",
           "stimuli": [], "questions": QUESTIONS}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {OUT}: {n} questions; difficulty {dict(Counter(q['difficulty'] for q in QUESTIONS))}; "
          f"formats {dict(fmts)}; keys {dict(sorted(KEYS.items()))}")
