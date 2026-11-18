"""Writes batches/parts/BATCH_005_CHE_p1.json: package CHE_005_p1 of BATCH_005 (Chemistry, 128 questions).

Topics: Some Basic Concepts, Atomic Structure, Chemical Bonding, Thermodynamics, Solutions, Equilibrium,
Redox and Electrochemistry, Chemical Kinetics, Periodicity, p-Block Elements. IDs NEET_CHE_001001..001128.

Every computable answer is re-derived here with an assert before anything is written; the quota per
(topic, difficulty), the ID range, the format mix and the answer-key balance are asserted too.
The position of every correct option is chosen by hand in the call that adds the question (argument `at`)
and never moved by code.

    cd docs/neet-bank && python tools/batch_005/CHE_005_p1.py
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
PACKAGE = "CHE_005_p1"
PLAN = ROOT / "batches" / "plans" / "BATCH_005_plan.json"
OUT = ROOT / "batches" / "parts" / "BATCH_005_CHE_p1.json"
TODAY = "2026-11-16"
LETTERS = "ABCD"
CHE = "Chemistry"
FIRST_ID = 1001
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

o_per_formula = 3 + 10  # Na2CO3 has 3 O, 10 H2O have 10 O
assert 0.5 * o_per_formula == 6.5 and 0.5 * 3 == 1.5 and 0.5 * 10 == 5.0
add("Mole concept", B, "numerical",
    "The amount of oxygen atoms present in 0.5 mol of washing soda crystals, Na₂CO₃·10H₂O, is:",
    Opts("B", "6.5 mol", ["1.5 mol", "5.0 mol", "13 mol"]),
    "Moles of atoms from moles of a formula unit",
    "Each formula unit Na₂CO₃·10H₂O contains 3 oxygen atoms in the carbonate ion and 10 in the ten water "
    "molecules, i.e. 13 oxygen atoms. So 1 mol of the crystals contains 13 mol of O atoms.",
    ["O atoms per formula unit = 3 (CO₃²⁻) + 10 (10 H₂O) = 13", "n(O) = 0.5 × 13 = 6.5 mol"],
    why="1.5 mol counts only the carbonate oxygens and 5.0 mol only the water oxygens. 13 mol is the value for "
        "1 mol of the crystals, not 0.5 mol.",
    ncert=f"{REF1}, mole concept", seconds=30, checked=True)

o_mass = {"SO3": 1 * 3 * 16, "N2O5": 0.5 * 5 * 16, "CO": 2 * 1 * 16, "CO2": 1.2 * 2 * 16}
assert max(o_mass, key=o_mass.get) == "SO3" and o_mass["SO3"] == 48 and close(o_mass["CO2"], 38.4)
add("Mole concept", B, "direct",
    "Which of the following samples contains the largest mass of oxygen? (O = 16)",
    Opts("D", "1.0 mol of SO₃", ["0.5 mol of N₂O₅", "2.0 mol of CO", "1.2 mol of CO₂"]),
    "Mass of an element in a given amount of compound",
    "Mass of oxygen = (amount of compound) × (O atoms per formula) × 16 g mol⁻¹. The sample with the "
    "largest number of moles of O atoms has the largest mass of oxygen.",
    ["SO₃: 1.0 × 3 = 3.0 mol O = 48 g", "N₂O₅: 0.5 × 5 = 2.5 mol O = 40 g", "CO: 2.0 × 1 = 2.0 mol O = 32 g",
     "CO₂: 1.2 × 2 = 2.4 mol O = 38.4 g"],
    why="N₂O₅ has the most oxygen atoms per molecule, but only 0.5 mol is taken (40 g O). 2.0 mol CO gives 32 g "
        "and 1.2 mol CO₂ gives 38.4 g, both less than 48 g.",
    ncert=f"{REF1}, mole concept", seconds=40)

add("Laws of chemical combination", B, "statement_pair",
    sp("One atomic mass unit (1 u) is equal to 1.66056 × 10⁻²⁴ g.",
       "The constituents of a compound can be separated from one another by physical methods such as "
       "filtration or distillation."),
    SP_, "Atomic mass unit; compounds versus mixtures",
    "One atomic mass unit is one-twelfth of the mass of a carbon-12 atom, 1.66056 × 10⁻²⁴ g, so Statement I is "
    "true. The constituents of a compound are combined chemically in a fixed ratio and can be separated only "
    "by chemical methods; physical methods separate the components of a mixture. Statement II is false.",
    ["1 u = mass of one ¹²C atom / 12 = 1.66056 × 10⁻²⁴ g (I true)",
     "Compound → chemical methods needed; mixture → physical methods (II false)"],
    answer="C", ncert=f"{REF1}, atomic mass and classification of matter", seconds=30)

pc, ph, po = 54.5 / 12, 9.1 / 1, 36.4 / 16
ratio = [round(x / po, 1) for x in (pc, ph, po)]
assert ratio == [2.0, 4.0, 1.0]
emp_mass = 2 * 12 + 4 * 1 + 16
assert emp_mass == 44 and 88 / emp_mass == 2
assert 3 * 12 + 4 + 3 * 16 == 88 and 5 * 12 + 12 + 16 == 88  # distractors share the molar mass
add("Empirical and molecular formulae", I, "numerical",
    "An organic compound contains 54.5% carbon, 9.1% hydrogen and 36.4% oxygen by mass. Its molar mass is "
    "88 g mol⁻¹. Its molecular formula is (C = 12, H = 1, O = 16):",
    Opts("A", "C₄H₈O₂", ["C₂H₄O", "C₃H₄O₃", "C₅H₁₂O"]),
    "Empirical formula from percentage composition, then the molecular formula",
    "Divide each mass percentage by the atomic mass to get relative moles, divide by the smallest to get the "
    "simplest ratio (empirical formula), and multiply by n = molar mass / empirical formula mass.",
    ["C: 54.5/12 = 4.54; H: 9.1/1 = 9.1; O: 36.4/16 = 2.275",
     "Divide by 2.275 → C : H : O = 2 : 4 : 1 → empirical formula C₂H₄O (mass 44)",
     "n = 88 / 44 = 2 → molecular formula C₄H₈O₂"],
    why="C₂H₄O is only the empirical formula. C₃H₄O₃ and C₅H₁₂O have molar mass 88 too, but their percentage "
        "compositions do not match the data.",
    ncert=f"{REF1}, empirical and molecular formula", seconds=75, checked=True)

n_caco3 = 10 / (40 + 12 + 48)
v_co2 = n_caco3 * 22.7
assert close(n_caco3, 0.1) and close(v_co2, 2.27) and close(2 * v_co2, 4.54) and close(v_co2 / 2, 1.135)
add("Stoichiometry", I, "numerical",
    "10 g of calcium carbonate is treated with an excess of dilute hydrochloric acid: "
    "CaCO₃(s) + 2HCl(aq) → CaCl₂(aq) + H₂O(l) + CO₂(g). The volume of CO₂ formed, measured at STP, is "
    "(Ca = 40, C = 12, O = 16; molar volume of a gas at STP = 22.7 L mol⁻¹):",
    Opts("C", "2.27 L", ["4.54 L", "1.135 L", "22.7 L"]),
    "Mass–volume stoichiometry",
    "Convert the mass of CaCO₃ to moles, use the 1 : 1 mole ratio of CaCO₃ to CO₂ from the balanced equation, "
    "and multiply by the molar volume.",
    ["M(CaCO₃) = 40 + 12 + 48 = 100 g mol⁻¹; n = 10/100 = 0.10 mol",
     "n(CO₂) = n(CaCO₃) = 0.10 mol", "V = 0.10 × 22.7 = 2.27 L"],
    why="4.54 L uses the 2 : 1 ratio of HCl to CaCO₃ for CO₂, and 1.135 L halves the amount. 22.7 L is the volume "
        "of a whole mole of CO₂.",
    ncert=f"{REF1}, stoichiometry and stoichiometric calculations", seconds=45, checked=True)

add("Laws of chemical combination", I, "match_list",
    lists("Match List-I (law of chemical combination) with List-II (observation that illustrates it).",
          ["Law of conservation of mass", "Law of definite proportions", "Law of multiple proportions",
           "Gay-Lussac's law of gaseous volumes"],
          ["Carbon forms CO and CO₂; the masses of oxygen that combine with 12 g of carbon in them are in the "
           "ratio 1 : 2.",
           "At the same temperature and pressure, 1 volume of H₂ combines with 1 volume of Cl₂ to give 2 volumes "
           "of HCl gas.",
           "Samples of cupric carbonate, whether natural or prepared in the laboratory, have the same percentage "
           "of copper, carbon and oxygen.",
           "In a chemical reaction, the total mass of the products equals the total mass of the reactants."]),
    match("B", M("IV III I II"), [M("IV I III II"), M("III IV I II"), M("IV III II I")]),
    "Laws of chemical combination",
    "Conservation of mass: total mass unchanged. Definite proportions: a compound always has the same "
    "composition by mass, whatever its source. Multiple proportions: when two elements form more than one "
    "compound, the masses of one that combine with a fixed mass of the other are in a simple whole-number "
    "ratio. Gay-Lussac: gases combine in simple whole-number ratios by volume.",
    ["A → IV (mass of products = mass of reactants)", "B → III (same composition from any source)",
     "C → I (16 g : 32 g of O per 12 g C = 1 : 2)", "D → II (1 : 1 : 2 by volume)"],
    why="Swapping I and III confuses multiple proportions (two compounds) with definite proportions (one "
        "compound). Matching D with I mixes a mass ratio with a volume ratio.",
    ncert=f"{REF1}, laws of chemical combinations", seconds=45)

assert 28 / 28 * 3 * 2 == 6 and 28 + 6 == 34  # N2 + 3H2 -> 2NH3
assert (28 / 28) * 3 < 28 / 2  # with 28 g of each, H2 needed (3 mol) < H2 present (14 mol): N2 limits
add("Stoichiometry", I, "assertion_reason",
    ar("In the reaction N₂(g) + 3H₂(g) → 2NH₃(g), 28 g of N₂ reacts completely with 6 g of H₂ to give 34 g of "
       "NH₃ (N = 14, H = 1).",
       "When equal masses of N₂ and H₂ are mixed for this reaction, H₂ is the limiting reagent."),
    AR_, "Mole ratios and the limiting reagent",
    "28 g N₂ is 1 mol; it needs 3 mol (6 g) of H₂ and gives 2 mol (34 g) of NH₃, consistent with conservation "
    "of mass, so A is true. With equal masses, say 28 g of each, there is 1 mol N₂ but 14 mol H₂; only 3 mol "
    "H₂ is needed, so N₂ is used up first and is the limiting reagent. R is false.",
    ["1 mol N₂ (28 g) + 3 mol H₂ (6 g) → 2 mol NH₃ (34 g): A true",
     "Equal masses (28 g each): N₂ 1 mol, H₂ 14 mol; H₂ in large excess → N₂ limiting: R false"],
    answer="C", ncert=f"{REF1}, limiting reagent", seconds=45)

add("Mole concept", A, "multi_statement",
    ms("Which of the following statements are correct? (H = 1, C = 12, O = 16)",
       ["The molar mass of a substance, in g mol⁻¹, is numerically equal to its atomic or molecular mass in u.",
        "One mole of Na₂SO₄ gives 3 mol of ions when it dissociates completely in water.",
        "One mole of CH₄ contains 4 g of hydrogen.",
        "The mass of one atom of carbon-12 is exactly 12 g.",
        "22 g of CO₂ contains 0.5 mol of oxygen atoms."]),
    multi("D", {"a": True, "b": True, "c": True, "d": False, "e": False},
          ["(a), (c) and (e) only", "(b), (d) and (e) only", "(a), (b), (c) and (e) only"]),
    "Molar mass and the mole",
    "Molar mass in g mol⁻¹ equals the atomic or molecular mass in u. Na₂SO₄ → 2Na⁺ + SO₄²⁻ gives 3 mol ions "
    "per mole. CH₄ has 4 mol H atoms per mole, i.e. 4 g. It is one mole of carbon-12 atoms, not one atom, "
    "that has a mass of 12 g. 22 g CO₂ is 0.5 mol, which contains 1.0 mol of O atoms.",
    ["(a) True", "(b) True: 2 Na⁺ + 1 SO₄²⁻", "(c) True: 4 mol H × 1 g mol⁻¹", "(d) False: 12 u per atom",
     "(e) False: 0.5 mol CO₂ × 2 = 1.0 mol O"],
    why="Any option with (d) or (e) is wrong, and (b) is a true statement that must be included.",
    ncert=f"{REF1}, atomic and molecular masses, mole concept and molar masses", seconds=60)

n_n2, n_h2 = 5.6 / 28, 1.5 / 2
assert close(n_n2, 0.2) and close(n_h2, 0.75) and 3 * n_n2 < n_h2  # N2 limiting
m_nh3 = 2 * n_n2 * 17
h2_left = (n_h2 - 3 * n_n2) * 2
assert close(m_nh3, 6.8) and close(h2_left, 0.3)
assert close(n_h2 / 3 * 2 * 17, 8.5) and close(3 * n_n2 * 2, 1.2) and close(n_n2 * 17, 3.4)
add("Stoichiometry", A, "numerical",
    "5.6 g of N₂ and 1.5 g of H₂ are allowed to react completely according to N₂(g) + 3H₂(g) → 2NH₃(g). The "
    "mass of NH₃ formed and the mass of the reactant left over are (N = 14, H = 1):",
    Opts("C", "6.8 g of NH₃; 0.3 g of H₂ left over",
         ["8.5 g of NH₃; no reactant left over", "6.8 g of NH₃; 1.2 g of H₂ left over",
          "3.4 g of NH₃; 0.9 g of H₂ left over"]),
    "Limiting reagent",
    "Convert both masses to moles and compare with the 1 : 3 ratio. The reactant that would be used up first "
    "fixes the amount of product; the excess of the other is left over.",
    ["n(N₂) = 5.6/28 = 0.20 mol; n(H₂) = 1.5/2 = 0.75 mol",
     "0.20 mol N₂ needs 0.60 mol H₂ (< 0.75 mol) → N₂ is the limiting reagent",
     "NH₃ = 2 × 0.20 = 0.40 mol = 0.40 × 17 = 6.8 g",
     "H₂ left = 0.75 − 0.60 = 0.15 mol = 0.3 g"],
    why="8.5 g treats H₂ as limiting (0.75/3 × 2 mol NH₃), which needs more N₂ than is present. 1.2 g is the mass "
        "of H₂ consumed, not left over. 3.4 g takes one NH₃ per N₂.",
    ncert=f"{REF1}, limiting reagent", seconds=90, checked=True)

n_h2_zn = 0.784 / 22.4
m_zn = n_h2_zn * 65
assert close(n_h2_zn, 0.035) and close(m_zn, 2.275) and close(m_zn / 2.5 * 100, 91.0)
assert close(m_zn / 2 / 2.5 * 100, 45.5) and close(0.784 / 22.7 * 65 / 2.5 * 100, 89.8, 0.002)
add("Stoichiometry", A, "numerical",
    "A 2.5 g sample of impure zinc is treated with an excess of dilute sulphuric acid: "
    "Zn(s) + H₂SO₄(aq) → ZnSO₄(aq) + H₂(g). The impurities do not react. The hydrogen evolved occupies "
    "0.784 L at STP. Taking the molar volume of a gas under these conditions as 22.4 L mol⁻¹ (Zn = 65), the "
    "percentage purity of the zinc sample is:",
    Opts("B", "91.0%", ["45.5%", "89.8%", "9.0%"]),
    "Percentage purity from the volume of gas evolved",
    "The moles of H₂ equal the moles of zinc that reacted (1 : 1). Their mass divided by the mass of the "
    "sample gives the purity.",
    ["n(H₂) = 0.784 / 22.4 = 0.035 mol = n(Zn)", "Mass of Zn = 0.035 × 65 = 2.275 g",
     "Purity = 2.275 / 2.5 × 100 = 91.0%"],
    why="45.5% assumes 2 mol of H₂ per mol of Zn. 89.8% uses 22.7 L mol⁻¹ instead of the molar volume given in "
        "the question. 9.0% is the percentage of impurity.",
    ncert=f"{REF1}, stoichiometry and stoichiometric calculations", seconds=80, checked=True)

# ==================================================================== 2. Atomic Structure
topic("Atomic Structure")
REF2 = f"{C11}, 'Structure of Atom'"

add("Quantum numbers and orbitals", B, "direct",
    "An electron has the principal quantum number n = 5 and the azimuthal quantum number l = 3. The subshell "
    "in which it is present is:",
    Opts("C", "5f", ["5d", "5p", "4f"]),
    "Subshell notation from n and l",
    "The subshell is written as n followed by the letter for l: l = 0, 1, 2, 3 correspond to s, p, d, f. So "
    "n = 5, l = 3 is the 5f subshell.",
    ["l = 3 → f", "n = 5 → 5f"],
    why="5d corresponds to l = 2 and 5p to l = 1. 4f has n = 4.",
    ncert=f"{REF2}, quantum numbers", seconds=20)

add("Bohr model and hydrogen spectrum", B, "statement_pair",
    sp("In Thomson's model of the atom, the mass of the atom is concentrated in a very small, positively "
       "charged nucleus.",
       "In Rutherford's α-particle scattering experiment, a very small fraction of the α-particles were "
       "deflected by nearly 180°."),
    SP_, "Thomson and Rutherford models",
    "Thomson pictured the atom as a uniform sphere of positive charge with electrons embedded in it; the mass "
    "was taken to be uniformly distributed over the atom. The idea of a tiny, massive nucleus came from "
    "Rutherford. So Statement I is false. In the scattering experiment most α-particles passed through, a "
    "small fraction were deflected by small angles and a very few (about 1 in 20 000) bounced back, i.e. were "
    "deflected by nearly 180°. Statement II is true.",
    ["Thomson: mass and positive charge spread uniformly (I false)",
     "Rutherford: very few α-particles deflected by ~180° (II true)"],
    answer="D", ncert=f"{REF2}, Thomson model and Rutherford's nuclear model of atom", seconds=30)

co_3d = 27 - 18 - 2  # [Ar] 3d7 4s2
assert co_3d == 7 and (5 - (co_3d - 5)) == 3
add("Electronic configuration", B, "numerical",
    "The number of unpaired electrons in a ground-state cobalt atom (Z = 27) is:",
    Opts("B", "3", ["1", "5", "7"]),
    "Hund's rule in a partly filled d subshell",
    "Co is [Ar] 3d⁷ 4s². In the 3d subshell the first five electrons occupy the five orbitals singly (Hund's "
    "rule); the remaining two pair up, leaving three unpaired electrons. The 4s² pair has no unpaired electron.",
    ["Co: [Ar] 3d⁷ 4s²", "3d⁷: five singly filled, then two paired → 5 − 2 = 3 unpaired"],
    why="7 counts every d electron as unpaired, 5 is the value for a half-filled d⁵ subshell, and 1 ignores "
        "Hund's rule.",
    ncert=f"{REF2}, filling of orbitals in atom", seconds=30, checked=True)

add("Dual nature and uncertainty", B, "assertion_reason",
    ar("The wave nature of a moving cricket ball cannot be detected.",
       "Because the mass of the ball is large, its de Broglie wavelength (λ = h/mv) is far too small to be "
       "measured."),
    AR_, "de Broglie wavelength of macroscopic objects",
    "de Broglie's relation applies to all moving objects, but λ = h/mv is inversely proportional to the "
    "mass. For an object as heavy as a cricket ball the wavelength is so small that its wave properties cannot "
    "be detected. R is the reason for A.",
    ["λ = h/(mv); h = 6.626 × 10⁻³⁴ J s is tiny", "Large m → λ immeasurably small → wave nature not detected"],
    answer="A", ncert=f"{REF2}, dual behaviour of matter", seconds=30)

p_l1 = 6 + 3  # 2p6 and 3p3
assert p_l1 == 9
add("Quantum numbers and orbitals", I, "numerical",
    "In a ground-state phosphorus atom (Z = 15), the number of electrons with azimuthal quantum number l = 1 is:",
    Opts("D", "9", ["6", "3", "12"]),
    "Counting electrons by l",
    "l = 1 means p orbitals. P is 1s² 2s² 2p⁶ 3s² 3p³, so the p electrons are the six 2p and the three 3p "
    "electrons.",
    ["P: 1s² 2s² 2p⁶ 3s² 3p³", "l = 1 → 2p⁶ + 3p³ = 9 electrons"],
    why="6 counts only the 2p electrons and 3 only the 3p electrons. 12 would need a filled 3p subshell.",
    ncert=f"{REF2}, quantum numbers and electronic configuration of atoms", seconds=35, checked=True)

e_photon = H_PLANCK * C_LIGHT / 600e-9
e_mol = e_photon * NA / 1000
assert close(e_photon, 3.313e-19) and close(e_mol, 199.5, 0.002) and close(e_mol * 10, 1995, 0.002)
add("Dual nature and uncertainty", I, "numerical",
    "The energy of one mole of photons of light of wavelength 600 nm is (h = 6.626 × 10⁻³⁴ J s, "
    "c = 3.0 × 10⁸ m s⁻¹, Nₐ = 6.022 × 10²³ mol⁻¹):",
    Opts("A", "199.5 kJ mol⁻¹", ["1995 kJ mol⁻¹", "0.1995 kJ mol⁻¹", "3.313 × 10⁻²² kJ mol⁻¹"]),
    "Energy of a mole of photons",
    "The energy of one photon is E = hc/λ; one mole of photons has Nₐ times this energy.",
    ["E(photon) = (6.626 × 10⁻³⁴ × 3.0 × 10⁸) / (600 × 10⁻⁹) = 3.313 × 10⁻¹⁹ J",
     "E(mol) = 3.313 × 10⁻¹⁹ × 6.022 × 10²³ = 1.995 × 10⁵ J mol⁻¹ = 199.5 kJ mol⁻¹"],
    why="1995 kJ mol⁻¹ results from taking 600 nm as 6 × 10⁻⁸ m. 0.1995 kJ mol⁻¹ divides by 1000 twice. "
        "3.313 × 10⁻²² kJ is the energy of a single photon, not of a mole.",
    ncert=f"{REF2}, Planck's quantum theory", seconds=50, checked=True)

add("Dual nature and uncertainty", I, "match_list",
    lists("Match List-I (observation) with List-II (what it showed).",
          ["Black-body radiation", "Photoelectric effect", "Line emission spectrum of hydrogen",
           "Diffraction of a beam of electrons by a crystal"],
          ["Moving electrons have wave character.",
           "The energy of radiation emitted by a hot body is quantised (Planck's quantum theory).",
           "Light behaves as a stream of particles (photons), and an electron is ejected from a metal only if "
           "the photon energy exceeds a threshold value.",
           "The electron in an atom can have only certain definite (quantised) energies."]),
    match("D", M("II III IV I"), [M("III II IV I"), M("II III I IV"), M("IV III II I")]),
    "Experiments that led to quantum ideas",
    "Planck explained black-body radiation by assuming energy is emitted in quanta. Einstein explained the "
    "photoelectric effect with photons. The discrete lines of the hydrogen spectrum show quantised energy "
    "levels in the atom. Diffraction of electrons confirmed de Broglie's idea that electrons behave as waves.",
    ["A → II (Planck)", "B → III (Einstein, photons)", "C → IV (quantised levels, Bohr)",
     "D → I (wave nature of electrons)"],
    why="The other codes swap Planck's and Einstein's explanations, or the line spectrum with electron "
        "diffraction.",
    ncert=f"{REF2}, particle nature of electromagnetic radiation; dual behaviour of matter", seconds=45)

add("Quantum numbers and orbitals", I, "direct",
    "Which of the following is a possible set of quantum numbers (n, l, mₗ, mₛ) for the valence electron of a "
    "ground-state potassium atom (Z = 19)?",
    Opts("B", "n = 4, l = 0, mₗ = 0, mₛ = +½",
         ["n = 3, l = 2, mₗ = 0, mₛ = +½", "n = 4, l = 1, mₗ = 0, mₛ = +½", "n = 4, l = 0, mₗ = +1, mₛ = +½"]),
    "Quantum numbers of a valence electron",
    "K is [Ar] 4s¹: the valence electron is in the 4s orbital, so n = 4, l = 0 and therefore mₗ = 0; mₛ can be "
    "+½ or −½.",
    ["K: [Ar] 4s¹ → n = 4, l = 0", "l = 0 allows only mₗ = 0", "mₛ = +½ (or −½)"],
    why="n = 3, l = 2 is a 3d electron, which potassium does not have. n = 4, l = 1 is a 4p electron. For l = 0, "
        "mₗ cannot be +1.",
    ncert=f"{REF2}, quantum numbers; electronic configuration of atoms", seconds=35)

add("Dual nature and uncertainty", I, "assertion_reason",
    ar("Red light of any brightness, shone on potassium metal for hours, ejects no photoelectrons, whereas even "
       "very weak yellow light ejects them.",
       "An electron is ejected only if the energy of each photon, hν, is at least equal to the minimum energy "
       "needed to remove it from the metal, i.e. the frequency must be at least the threshold frequency ν₀."),
    AR_, "Threshold frequency in the photoelectric effect",
    "Red light has a lower frequency than the threshold frequency of potassium, while yellow light has a "
    "higher one. Since each electron absorbs the energy of a single photon, increasing the brightness (more "
    "photons) cannot make up for a photon energy that is too small. R correctly explains A.",
    ["ν(red) ≈ 4.3–4.6 × 10¹⁴ Hz < ν₀(K); ν(yellow) ≈ 5.1–5.2 × 10¹⁴ Hz > ν₀(K)",
     "One photon ejects one electron only if hν ≥ hν₀"],
    answer="A", ncert=f"{REF2}, photoelectric effect", seconds=40)

e21 = 13.6 * (1 - 1 / 4)
assert close(e21, 10.2) and close(e21 - 2.2, 8.0) and close(13.6 - 2.2, 11.4) and close(3.4 - 2.2, 1.2)
add("Bohr model and hydrogen spectrum", A, "numerical",
    "The radiation emitted when the electron of a hydrogen atom falls from the n = 2 level to the n = 1 level "
    "falls on a metal whose work function is 2.2 eV. The maximum kinetic energy of the photoelectrons ejected "
    "is (Eₙ = −13.6/n² eV for the hydrogen atom):",
    Opts("C", "8.0 eV", ["11.4 eV", "1.2 eV", "12.4 eV"]),
    "Bohr energy levels combined with the photoelectric equation",
    "The photon energy equals the energy difference E₂ − E₁. In the photoelectric effect, the maximum kinetic "
    "energy of the ejected electron is the photon energy minus the work function.",
    ["E₂ − E₁ = −13.6/4 − (−13.6) = 10.2 eV", "KE(max) = hν − W₀ = 10.2 − 2.2 = 8.0 eV"],
    why="11.4 eV uses the ionisation energy (13.6 eV) as the photon energy. 1.2 eV uses only |E₂| = 3.4 eV. "
        "12.4 eV adds the work function instead of subtracting it.",
    ncert=f"{REF2}, Bohr's model for hydrogen atom; photoelectric effect", seconds=75, checked=True)

add("Dual nature and uncertainty", A, "multi_statement",
    ms("Which of the following statements are correct?",
       ["The energy of a photon is directly proportional to the frequency of the radiation.",
        "In the photoelectric effect, electrons are ejected as soon as light of a suitable frequency strikes the "
        "metal surface, without any time lag.",
        "The threshold frequency has the same value for all metals.",
        "According to the uncertainty principle, Δx × Δp ≥ h/4π.",
        "The speed of electromagnetic radiation in vacuum depends on its frequency."]),
    multi("A", {"a": True, "b": True, "c": False, "d": True, "e": False},
          ["(a), (c) and (d) only", "(b), (d) and (e) only", "(a), (b), (d) and (e) only"]),
    "Particle nature of light and the uncertainty principle",
    "E = hν, so photon energy is proportional to frequency. Photoemission is instantaneous once the frequency "
    "is above the threshold. ν₀ is characteristic of each metal (it depends on how tightly the metal holds its "
    "electrons). Heisenberg's principle is Δx·Δp ≥ h/4π. All electromagnetic radiation travels in vacuum with "
    "the same speed c, whatever its frequency.",
    ["(a) True", "(b) True", "(c) False: ν₀ differs from metal to metal", "(d) True",
     "(e) False: c is the same for all frequencies"],
    why="Options containing (c) or (e) include a false statement.",
    ncert=f"{REF2}, nature of electromagnetic radiation; photoelectric effect; Heisenberg's uncertainty principle",
    seconds=55)

add("Quantum numbers and orbitals", A, "statement_pair",
    sp("The probability density of the electron in a 1s orbital is maximum at the nucleus and decreases with "
       "distance from it.",
       "The number of angular nodes of an orbital is n − l − 1."),
    SP_, "Probability density and nodes",
    "For the 1s orbital, ψ² is highest at the nucleus and falls sharply with distance, so Statement I is true. "
    "An orbital has l angular nodes and n − l − 1 radial nodes, so the expression n − l − 1 belongs to radial "
    "nodes. Statement II is false.",
    ["1s: ψ² maximum at the nucleus (I true)", "Angular nodes = l; radial nodes = n − l − 1 (II false)"],
    answer="C", ncert=f"{REF2}, shapes of atomic orbitals", seconds=35)

unpaired = {"Cr": 6, "Mn2+": 5, "Fe2+": 4, "Co3+": 4}  # 3d5 4s1, 3d5, 3d6, 3d6
assert max(unpaired, key=unpaired.get) == "Cr"
add("Electronic configuration", A, "direct",
    "Which of the following ground-state species has the largest number of unpaired electrons?",
    Opts("D", "Cr (Z = 24)", ["Mn²⁺ (Z of Mn = 25)", "Fe²⁺ (Z of Fe = 26)", "Co³⁺ (Z of Co = 27)"]),
    "Unpaired electrons and the extra stability of half-filled subshells",
    "Chromium is [Ar] 3d⁵ 4s¹, not 3d⁴ 4s², because a half-filled d subshell is extra stable; all six of its "
    "outer electrons are unpaired. Mn²⁺ is 3d⁵ (5 unpaired), and Fe²⁺ and Co³⁺ are both 3d⁶ (4 unpaired).",
    ["Cr: 3d⁵ 4s¹ → 5 + 1 = 6", "Mn²⁺: 3d⁵ → 5", "Fe²⁺: 3d⁶ → 4", "Co³⁺: 3d⁶ → 4"],
    why="Mn²⁺ has the half-filled d⁵ set but no extra unpaired 4s electron. Fe²⁺ and Co³⁺ have one paired d "
        "orbital. Writing Cr as 3d⁴ 4s² (4 unpaired) is the trap.",
    ncert=f"{REF2}, stability of completely filled and half-filled subshells", seconds=45)

# ==================================================================== 3. Chemical Bonding and Molecular Structure
topic("Chemical Bonding and Molecular Structure")
REF3 = f"{C11}, 'Chemical Bonding and Molecular Structure'"

add("VSEPR shapes", B, "direct",
    "In which of the following molecules does the central atom have more than eight electrons in its valence "
    "shell (an expanded octet)?",
    Opts("B", "H₂SO₄", ["NH₃", "CO₂", "BeH₂"]),
    "Expanded octet",
    "In H₂SO₄ the sulphur atom forms two S=O double bonds and two S–OH single bonds in its Lewis structure, so "
    "12 electrons surround it. Elements of the third and later periods can use 3d orbitals in addition to 3s "
    "and 3p, so their octet can expand.",
    ["H₂SO₄: S has 2 double + 2 single bonds → 12 electrons", "NH₃ and CO₂: octet", "BeH₂: only 4 electrons "
     "around Be (incomplete octet)"],
    why="N in NH₃ and C in CO₂ have exactly eight electrons. Be in BeH₂ has fewer than eight.",
    ncert=f"{REF3}, limitations of the octet rule: the expanded octet", seconds=25)

f2_bo = (10 - 8) / 2  # 18 electrons: 10 bonding, 8 antibonding
assert f2_bo == 1
add("Molecular orbital theory", B, "numerical",
    "According to molecular orbital theory, the bond order of the F₂ molecule is:",
    Opts("C", "1", ["2", "0", "1.5"]),
    "Bond order from molecular orbital configuration",
    "F₂ has 18 electrons: σ1s² σ*1s² σ2s² σ*2s² σ2p_z² (π2pₓ² π2p_y²) (π*2pₓ² π*2p_y²). Bond order = ½(Nb − Na) "
    "= ½(10 − 8) = 1.",
    ["Bonding electrons Nb = 2 + 2 + 2 + 4 = 10", "Antibonding electrons Na = 2 + 2 + 4 = 8",
     "Bond order = ½(10 − 8) = 1"],
    why="2 is the bond order of O₂, which has two fewer antibonding electrons. 0 is the value for Ne₂. 1.5 is that "
        "of O₂⁻.",
    ncert=f"{REF3}, bonding in some homonuclear diatomic molecules", seconds=35, checked=True)

add("Ionic bonding and lattice enthalpy", B, "statement_pair",
    sp("The octet rule does not explain the shapes of molecules or their relative stability.",
       "The octet rule is based on the chemical inertness of the noble gases."),
    SP_, "Octet rule and its limitations",
    "Kössel and Lewis based the octet rule on the stable, unreactive configurations of the noble gases, so "
    "Statement II is true. NCERT lists among its limitations that the octet theory says nothing about the "
    "shape of a molecule or about its energy (relative stability). Statement I is true.",
    ["Octet rule: atoms attain a noble-gas configuration (II true)",
     "Silent about shape and energy/stability of molecules (I true)"],
    answer="A", ncert=f"{REF3}, Kössel-Lewis approach and limitations of the octet rule", seconds=30)

add("Hydrogen and metallic bonding", B, "direct",
    "Which of the following does NOT form hydrogen bonds between its own molecules?",
    Opts("B", "Dimethyl ether, CH₃OCH₃", ["Methanol, CH₃OH", "Ammonia, NH₃", "Hydrogen fluoride, HF"]),
    "Condition for hydrogen bonding",
    "A hydrogen bond needs a hydrogen atom covalently bonded to a highly electronegative atom (F, O or N). In "
    "CH₃OCH₃ every hydrogen is bonded to carbon, so although the oxygen has lone pairs, the molecules cannot "
    "hydrogen bond with one another.",
    ["CH₃OH: O–H present → H-bonds", "NH₃: N–H present → H-bonds", "HF: H–F present → H-bonds",
     "CH₃OCH₃: only C–H → no H-bond between its own molecules"],
    why="Methanol, ammonia and hydrogen fluoride all have H attached to O, N or F.",
    ncert=f"{REF3}, hydrogen bonding", seconds=25)

add("Fajans' rule and dipole moment", B, "direct",
    "Which of the following molecules is polar?",
    Opts("D", "SO₂", ["CO₂", "BeCl₂", "SF₆"]),
    "Molecular shape and dipole moment",
    "A molecule is polar when its bond dipoles do not cancel. SO₂ is bent (one lone pair on S), so its two S–O "
    "bond dipoles add to a resultant. CO₂ and BeCl₂ are linear and SF₆ is octahedral, so their bond dipoles "
    "cancel.",
    ["SO₂: bent → net dipole", "CO₂, BeCl₂: linear → μ = 0", "SF₆: octahedral → μ = 0"],
    why="CO₂, BeCl₂ and SF₆ have polar bonds but symmetrical shapes, so their dipole moments are zero.",
    ncert=f"{REF3}, polarity of bonds: dipole moment", seconds=25)

add("Hybridisation and resonance", B, "assertion_reason",
    ar("Rotation of one CH₂ group relative to the other about the C=C bond in ethene is restricted.",
       "Such a rotation would destroy the sideways overlap of the unhybridised 2p orbitals that forms the π "
       "bond."),
    AR_, "π bond and restricted rotation",
    "In ethene the π bond comes from sideways overlap of the parallel 2p orbitals on the two carbon atoms. "
    "Twisting one end would turn these orbitals away from each other and break the π bond, which needs a large "
    "amount of energy. Hence rotation about C=C is restricted. R explains A.",
    ["π bond: parallel 2p orbitals overlap sideways", "Rotation → orbitals no longer parallel → π bond broken",
     "So rotation is restricted"],
    answer="A", ncert=f"{REF3}, hybridisation: formation of the double bond in ethene", seconds=30)

o2_bond, o2_anti = 2 + 2 + 2 + 2 + 2, 2 + 2 + 2
assert o2_bond + o2_anti == 16 and (o2_bond - o2_anti) / 2 == 2
assert (8 - 4) / 2 == 2  # valence-only count gives the same bond order
add("Molecular orbital theory", I, "numerical",
    "Counting all 16 electrons of the O₂ molecule (including the 1s electrons), the numbers of electrons in "
    "bonding and in antibonding molecular orbitals are respectively:",
    Opts("C", "10 and 6", ["8 and 4", "12 and 4", "6 and 10"]),
    "Molecular orbital configuration of O₂",
    "O₂: σ1s² σ*1s² σ2s² σ*2s² σ2p_z² (π2pₓ² π2p_y²) (π*2pₓ¹ π*2p_y¹). The bonding orbitals are σ1s, σ2s, σ2p_z "
    "and the two π2p; the antibonding ones are σ*1s, σ*2s and the two π*2p.",
    ["Bonding: σ1s² + σ2s² + σ2p_z² + π2p⁴ = 10", "Antibonding: σ*1s² + σ*2s² + π*2p² = 6",
     "Check: bond order = ½(10 − 6) = 2"],
    why="8 and 4 counts only the valence electrons, which the question excludes. 12 and 4 puts the two π* "
        "electrons in bonding orbitals. 6 and 10 swaps the two numbers.",
    ncert=f"{REF3}, bonding in some homonuclear diatomic molecules: oxygen", seconds=45, checked=True)

fc_c, fc_o = 4 - 2 - 6 // 2, 6 - 2 - 6 // 2
assert (fc_c, fc_o) == (-1, 1) and fc_c + fc_o == 0
add("Hybridisation and resonance", I, "numerical",
    "In the Lewis structure of carbon monoxide, :C≡O:, each atom has one lone pair and the atoms are joined by "
    "a triple bond. The formal charges on the carbon and the oxygen atoms are respectively:",
    Opts("B", "−1 and +1", ["+1 and −1", "0 and 0", "−2 and +2"]),
    "Formal charge",
    "Formal charge = (valence electrons of the free atom) − (non-bonding electrons) − ½(bonding electrons). "
    "Each atom has 2 non-bonding electrons and shares 6 bonding electrons.",
    ["C: 4 − 2 − ½(6) = −1", "O: 6 − 2 − ½(6) = +1", "Sum = 0, the charge of the neutral molecule"],
    why="+1 and −1 is the pattern expected from electronegativity alone, but formal charge is a bookkeeping "
        "count, not an electronegativity rule. 0 and 0 would need each atom to be assigned exactly its own number "
        "of valence electrons, which is not the case here. −2 and +2 have the right signs but twice the "
        "correct magnitudes.",
    ncert=f"{REF3}, formal charge", seconds=45, checked=True)

add("Fajans' rule and dipole moment", I, "assertion_reason",
    ar("The CCl₄ molecule has a non-zero dipole moment.",
       "Each C–Cl bond in CCl₄ is polar."),
    AR_, "Bond dipoles and molecular symmetry",
    "Chlorine is more electronegative than carbon, so each C–Cl bond is polar and R is true. In the regular "
    "tetrahedral CCl₄ molecule the four equal bond dipoles cancel, so the net dipole moment is zero. A is false.",
    ["C–Cl: polar bond (R true)", "Tetrahedral, four identical bond dipoles → resultant zero (A false)"],
    answer="D", ncert=f"{REF3}, polarity of bonds", seconds=30)

add("Hybridisation and resonance", I, "match_list",
    lists("Match List-I (species) with List-II (hybridisation of the indicated or central atom).",
          ["Each carbon atom in C₂H₂", "C in CO₃²⁻", "N in NH₄⁺", "Cl in ClF₃"],
          ["sp³d", "sp²", "sp³", "sp"]),
    match("B", M("IV II III I"), [M("IV III II I"), M("II IV III I"), M("IV II I III")]),
    "Hybridisation from the number of electron pairs",
    "Count σ bonds plus lone pairs on the atom: 2 → sp, 3 → sp², 4 → sp³, 5 → sp³d.",
    ["C in C₂H₂: 2 σ bonds (one C–H, one C–C), no lone pair → sp → IV",
     "C in CO₃²⁻: 3 σ bonds, no lone pair → sp² → II", "N in NH₄⁺: 4 σ bonds → sp³ → III",
     "Cl in ClF₃: 3 bond pairs + 2 lone pairs = 5 → sp³d → I"],
    why="The other codes swap sp² and sp³ (carbonate versus ammonium) or treat ClF₃ as sp³ by ignoring a lone "
        "pair.",
    ncert=f"{REF3}, hybridisation", seconds=45)

add("Hybridisation and resonance", I, "multi_statement",
    ms("Which of the following statements about hybridisation are correct?",
       ["The number of hybrid orbitals formed equals the number of atomic orbitals that hybridise.",
        "The hybrid orbitals formed are equivalent in energy and shape.",
        "Orbitals of very different energies, such as 1s and 2p, readily hybridise.",
        "Only half-filled orbitals can take part in hybridisation.",
        "Hybrid orbitals are directed in space in preferred directions that keep the electron pairs as far "
        "apart as possible."]),
    multi("C", {"a": True, "b": True, "c": False, "d": False, "e": True},
          ["(a), (c) and (e) only", "(b), (d) and (e) only", "(a), (b), (d) and (e) only"]),
    "Salient features and conditions of hybridisation",
    "NCERT's features: the number of hybrid orbitals equals the number of orbitals mixed; hybrid orbitals are "
    "equivalent in energy and shape; they point in directions of minimum repulsion. Only orbitals of almost "
    "equal energy hybridise, and filled as well as half-filled orbitals can take part.",
    ["(a) True", "(b) True", "(c) False: energies must be nearly equal", "(d) False: filled orbitals can also take "
     "part", "(e) True"],
    why="Options containing (c) or (d) include a false statement.",
    ncert=f"{REF3}, hybridisation: salient features and important conditions", seconds=50)

add("Molecular orbital theory", I, "statement_pair",
    sp("Removal of an electron from N₂ to form N₂⁺ increases the bond order.",
       "The bond dissociation enthalpy of N₂⁺ is greater than that of N₂."),
    SP_, "Effect of ionisation on bond order of N₂",
    "In N₂ (bond order 3) the highest occupied orbital, σ2p_z, is a bonding orbital. Removing an electron from "
    "it lowers the bond order to 2.5, so Statement I is false. A lower bond order means a weaker bond, so N₂⁺ "
    "has a smaller bond dissociation enthalpy than N₂; Statement II is false too.",
    ["N₂: BO = ½(10 − 4) = 3; N₂⁺: BO = ½(9 − 4) = 2.5 (I false)",
     "Lower bond order → weaker bond → smaller bond enthalpy (II false)"],
    answer="B", ncert=f"{REF3}, bond order and its significance", seconds=40)

add("Hybridisation and resonance", I, "match_list",
    lists("Match List-I (bond) with List-II (type of orbital overlap that forms it).",
          ["σ bond in H₂", "σ bond in HCl", "σ bond in Cl₂", "π bond in N₂"],
          ["Sideways overlap of two p orbitals", "Head-on overlap of an s and a p orbital",
           "Head-on overlap of two s orbitals", "Head-on overlap of two p orbitals"]),
    match("D", M("III II IV I"), [M("II III IV I"), M("III II I IV"), M("III IV II I")]),
    "s–s, s–p and p–p overlap",
    "A σ bond results from head-on (axial) overlap; a π bond from sideways overlap of p orbitals. H₂ uses the 1s "
    "orbitals of both atoms; HCl uses H 1s and Cl 3p; Cl₂ uses a 3p orbital on each Cl; the two π bonds of N₂ "
    "come from sideways overlap of 2p orbitals.",
    ["H₂: s–s → III", "HCl: s–p → II", "Cl₂: p–p head-on → IV", "π in N₂: p–p sideways → I"],
    why="The other codes swap s–s and s–p overlap, or confuse head-on and sideways p–p overlap.",
    ncert=f"{REF3}, types of overlapping and nature of covalent bonds", seconds=40)

add("VSEPR shapes", I, "direct",
    "In which of the following molecules are all the bonds from the central atom equal in length?",
    Opts("B", "BF₃", ["PCl₅", "SF₄", "ClF₃"]),
    "Equivalent and non-equivalent positions",
    "In trigonal planar BF₃ all three positions are equivalent, so the three B–F bonds are equal. In a "
    "trigonal bipyramid the axial and equatorial positions are different: PCl₅ has longer axial bonds, and in "
    "SF₄ (see-saw) and ClF₃ (T-shaped) the bonds also occupy both kinds of position.",
    ["BF₃: three equivalent positions → equal bonds", "PCl₅: axial > equatorial",
     "SF₄, ClF₃: axial and equatorial bonds of different length"],
    why="PCl₅, SF₄ and ClF₃ are all based on a trigonal bipyramid, where axial and equatorial bonds differ.",
    ncert=f"{REF3}, VSEPR theory; hybridisation (sp³d)", seconds=35)

add("Molecular orbital theory", A, "multi_statement",
    ms("Which of the following statements about the formation of molecular orbitals by linear combination of "
       "atomic orbitals are correct?",
       ["The combining atomic orbitals must have the same or nearly the same energy.",
        "The combining atomic orbitals must have the same symmetry about the molecular axis.",
        "The combining atomic orbitals must overlap to the maximum extent.",
        "The 1s orbital of one atom combines effectively with the 2p orbital of another atom of the same "
        "element.",
        "An antibonding molecular orbital has a nodal plane between the two nuclei."]),
    multi("A", {"a": True, "b": True, "c": True, "d": False, "e": True},
          ["(a), (b) and (c) only", "(a), (c), (d) and (e) only", "(b), (c) and (e) only"]),
    "Conditions for the combination of atomic orbitals",
    "Atomic orbitals combine only if their energies are nearly equal, their symmetry about the molecular axis "
    "is the same and they overlap well. 1s and 2p differ greatly in energy, so they do not combine. In an "
    "antibonding orbital the electron density is cancelled between the nuclei, leaving a nodal plane there.",
    ["(a), (b), (c): the three conditions → true", "(d) False: energies too different",
     "(e) True: destructive interference between the nuclei"],
    why="Any option containing (d), or leaving out (e), is wrong.",
    ncert=f"{REF3}, conditions for the combination of atomic orbitals; formation of molecular orbitals",
    seconds=55)

add("Hybridisation and resonance", A, "direct",
    "In allene, H₂C=C=CH₂, the hybridisation states of the three carbon atoms, taken from left to right, are:",
    Opts("D", "sp², sp, sp²", ["sp², sp², sp²", "sp, sp², sp", "sp³, sp, sp³"]),
    "Hybridisation from σ bonds and lone pairs",
    "Each terminal carbon forms three σ bonds (two C–H and one C–C) and one π bond, so it is sp². The central "
    "carbon forms two σ bonds (to the two terminal carbons) and two π bonds, so it is sp.",
    ["Terminal C: 3 σ bonds → sp²", "Central C: 2 σ + 2 π → sp", "Result: sp², sp, sp²"],
    why="'sp² throughout' treats every doubly bonded carbon as sp², ignoring that the middle carbon has two double "
        "bonds. sp³ would need four σ bonds.",
    ncert=f"{REF3}, hybridisation of carbon (sp, sp²)", seconds=45)

add("Hybridisation and resonance", A, "assertion_reason",
    ar("The C–H bond in ethyne is shorter than the C–H bond in ethane.",
       "The carbon atoms in ethyne use sp hybrid orbitals (50% s character), which hold electrons closer to the "
       "nucleus than the sp³ orbitals (25% s character) used in ethane."),
    AR_, "s character and bond length",
    "s orbitals are held closer to the nucleus than p orbitals, so a hybrid orbital with more s character is "
    "smaller and more electronegative. The sp-hybridised carbon of ethyne forms a shorter C–H bond than the "
    "sp³ carbon of ethane. R explains A.",
    ["% s: sp = 50, sp² = 33.3, sp³ = 25", "More s character → orbital closer to nucleus → shorter bond"],
    answer="A", ncert=f"{C11}, 'Hydrocarbons', alkynes: structure of the triple bond", seconds=40)

add("Hybridisation and resonance", A, "statement_pair",
    sp("In the carbonate ion, the two negative charges are shared equally by the three oxygen atoms.",
       "Each C–O bond in CO₃²⁻ is shorter than a C=O bond in CO₂."),
    SP_, "Resonance in the carbonate ion",
    "CO₃²⁻ is a resonance hybrid of three equivalent structures, so each oxygen carries −⅔ on average and "
    "Statement I is true. Each C–O bond in carbonate has a bond order of 4/3, less than the bond order 2 of "
    "C=O in CO₂; a lower bond order means a longer bond. Statement II is false.",
    ["Three equivalent canonical forms → charge spread equally (I true)",
     "Bond order 1.33 < 2 → C–O in CO₃²⁻ longer than C=O in CO₂ (II false)"],
    answer="C", ncert=f"{REF3}, resonance structures", seconds=40)

sigma_bz, pi_bz = 6 + 6, 3
assert sigma_bz / pi_bz == 4 and 6 / 3 == 2 and 9 / 3 == 3
add("Hybridisation and resonance", A, "numerical",
    "In one molecule of benzene, C₆H₆ (one Kekulé structure), the numbers of σ and π bonds are:",
    Opts("C", "12 σ and 3 π", ["6 σ and 3 π", "12 σ and 6 π", "9 σ and 3 π"]),
    "Counting σ and π bonds",
    "Every single bond is one σ bond and every double bond is one σ + one π. Benzene has six C–C bonds in the "
    "ring (three single and three double in a Kekulé structure) and six C–H bonds.",
    ["σ: 6 C–C + 6 C–H = 12", "π: one in each of the 3 C=C = 3", "σ : π = 4 : 1"],
    why="6 σ leaves out the C–H bonds. 6 π counts each double bond as two π bonds. 9 σ counts only the three "
        "single C–C bonds and the six C–H bonds, missing the σ part of the three double bonds.",
    ncert=f"{REF3}, sigma and pi bonds", seconds=45, checked=True)

add("VSEPR shapes", A, "multi_statement",
    ms("Which of the following statements are in accordance with the VSEPR theory?",
       ["Electron pairs in the valence shell of the central atom arrange themselves so as to minimise the "
        "repulsion between them.",
        "A multiple bond is treated as if it were a single electron pair (a super pair).",
        "Bond pair–bond pair repulsion is greater than lone pair–bond pair repulsion.",
        "A lone pair occupies less space around the central atom than a bond pair.",
        "When a molecule can be represented by two or more resonance structures, the VSEPR model can be applied "
        "to any one of them."]),
    multi("B", {"a": True, "b": True, "c": False, "d": False, "e": True},
          ["(a), (c) and (e) only", "(b), (c) and (d) only", "(a), (b), (d) and (e) only"]),
    "Postulates of VSEPR theory",
    "VSEPR: electron pairs keep as far apart as possible; a multiple bond counts as one super pair; when "
    "resonance structures exist, any one can be used. The repulsion order is lp–lp > lp–bp > bp–bp, because a "
    "lone pair is held only by the central atom and spreads over more space than a bond pair.",
    ["(a) True", "(b) True", "(c) False: lp–bp > bp–bp", "(d) False: a lone pair occupies more space",
     "(e) True"],
    why="Options with (c) or (d) contain a false statement.",
    ncert=f"{REF3}, VSEPR theory", seconds=50)

# ==================================================================== 4. Chemical Thermodynamics
topic("Chemical Thermodynamics")
REF4 = f"{C11}, 'Thermodynamics'"

q_v = 2 * 12.5 * (400 - 300)
assert q_v == 2500 and round(2 * (12.5 + 8.314) * 100) == 4163 and 1 * 12.5 * 100 == 1250
add("First law, work and enthalpy", B, "numerical",
    "2 mol of a monatomic ideal gas (C_v,m = 12.5 J K⁻¹ mol⁻¹) is heated in a closed rigid container from "
    "300 K to 400 K. The heat absorbed by the gas is (R = 8.314 J K⁻¹ mol⁻¹):",
    Opts("B", "2500 J", ["4163 J", "1250 J", "0 J"]),
    "Heat at constant volume",
    "In a rigid container the volume is constant, so w = 0 and q_V = ΔU = n C_v,m ΔT.",
    ["w = 0 (no change of volume)", "q_V = ΔU = 2 × 12.5 × 100 = 2500 J"],
    why="4163 J uses C_p,m = C_v,m + R, which applies at constant pressure. 1250 J is for 1 mol. 0 J would apply "
        "to an isothermal process, not to heating.",
    ncert=f"{REF4}, measurement of ΔU and heat capacity", seconds=35, checked=True)

add("Entropy and Gibbs energy", B, "direct",
    "In which of the following processes does the entropy of the system increase?",
    Opts("A", "Sublimation of solid carbon dioxide (dry ice)",
         ["Condensation of steam into liquid water", "2SO₂(g) + O₂(g) → 2SO₃(g)", "N₂(g) + 3H₂(g) → 2NH₃(g)"]),
    "Entropy and disorder",
    "Entropy increases when a substance becomes more disordered, as on going from solid to gas, or when the "
    "number of moles of gas increases. Sublimation turns a solid directly into a gas.",
    ["Dry ice (s) → CO₂(g): solid → gas → ΔS > 0", "Steam → water: gas → liquid → ΔS < 0",
     "2SO₂ + O₂ → 2SO₃: 3 mol gas → 2 mol → ΔS < 0", "N₂ + 3H₂ → 2NH₃: 4 mol gas → 2 mol → ΔS < 0"],
    why="Condensation and the two reactions that reduce the number of gas molecules all make the system more "
        "ordered.",
    ncert=f"{REF4}, entropy and spontaneity", seconds=25)

add("First law, work and enthalpy", B, "assertion_reason",
    ar("Density is an extensive property.",
       "The value of an extensive property depends on the quantity of matter present in the system."),
    AR_, "Extensive and intensive properties",
    "R is the definition of an extensive property and is true. Density is mass divided by volume; both are "
    "extensive but their ratio does not depend on the amount of substance, so density is intensive. A is false.",
    ["Extensive: depends on amount (mass, volume) → R true", "Density = m/V: independent of amount → intensive → "
     "A false"],
    answer="D", ncert=f"{REF4}, extensive and intensive properties", seconds=25)

add("First law, work and enthalpy", B, "statement_pair",
    sp("The absolute value of the internal energy of a system can be measured.",
       "The change in internal energy, ΔU, depends only on the initial and final states of the system."),
    SP_, "Internal energy as a state function",
    "Only changes in internal energy can be measured (through heat and work); its absolute value cannot be "
    "determined, so Statement I is false. U is a state function, so ΔU depends only on the initial and final "
    "states and not on the path. Statement II is true.",
    ["Absolute U not measurable (I false)", "U is a state function → ΔU path-independent (II true)"],
    answer="D", ncert=f"{REF4}, internal energy as a state function", seconds=30)

dh_hyd = (610 + 435) - (347 + 2 * 414)
assert dh_hyd == -130 and 610 - (347 + 2 * 414) == -565 and (610 + 435) - (347 + 414) == 284
add("Hess's law and enthalpies", I, "numerical",
    "Using the bond enthalpies C=C = 610, C–C = 347, H–H = 435 and C–H = 414 kJ mol⁻¹, the enthalpy change "
    "for the hydrogenation of ethene, H₂C=CH₂(g) + H₂(g) → H₃C–CH₃(g), is:",
    Opts("C", "−130 kJ mol⁻¹", ["+130 kJ mol⁻¹", "−565 kJ mol⁻¹", "+284 kJ mol⁻¹"]),
    "Reaction enthalpy from bond enthalpies",
    "ΔrH = Σ(bond enthalpies of bonds broken) − Σ(bond enthalpies of bonds formed). The four C–H bonds of "
    "ethene survive unchanged, so only the C=C and H–H bonds are broken, and one C–C and two new C–H bonds "
    "are formed.",
    ["Broken: C=C + H–H = 610 + 435 = 1045 kJ", "Formed: C–C + 2 C–H = 347 + 828 = 1175 kJ",
     "ΔrH = 1045 − 1175 = −130 kJ mol⁻¹"],
    why="+130 kJ reverses the subtraction. −565 kJ forgets to break the H–H bond. +284 kJ forms only one new "
        "C–H bond.",
    ncert=f"{REF4}, bond enthalpy", seconds=60, checked=True)

dh_trans = -393.5 - (-395.4)
assert close(dh_trans, 1.9) and close(-393.5 + -395.4, -788.9)
add("Hess's law and enthalpies", I, "numerical",
    "The standard enthalpies of combustion of graphite and of diamond to CO₂(g) are −393.5 kJ mol⁻¹ and "
    "−395.4 kJ mol⁻¹ respectively. The enthalpy change for C(graphite) → C(diamond) is:",
    Opts("B", "+1.9 kJ mol⁻¹", ["−1.9 kJ mol⁻¹", "−788.9 kJ mol⁻¹", "0 kJ mol⁻¹"]),
    "Hess's law with combustion data",
    "Write graphite → CO₂ (ΔH = −393.5) and then CO₂ → diamond, the reverse of diamond's combustion "
    "(ΔH = +395.4). Adding the two gives the transition.",
    ["C(graphite) + O₂ → CO₂; ΔH = −393.5", "CO₂ → C(diamond) + O₂; ΔH = +395.4",
     "C(graphite) → C(diamond); ΔH = −393.5 + 395.4 = +1.9 kJ mol⁻¹"],
    shortcut="ΔH = ΔcH(reactant) − ΔcH(product) = −393.5 − (−395.4).",
    why="−1.9 kJ subtracts in the wrong order. −788.9 kJ adds the two combustion enthalpies. 0 kJ assumes that "
        "two forms of the same element have equal enthalpy; only the most stable form (graphite) has ΔfH° = 0.",
    ncert=f"{REF4}, Hess's law of constant heat summation", seconds=45, checked=True)

add("Hess's law and enthalpies", I, "match_list",
    lists("Match List-I (enthalpy change) with List-II (the change it refers to, per mole).",
          ["Enthalpy of sublimation", "Enthalpy of vaporisation", "Bond dissociation enthalpy",
           "Enthalpy of solution"],
          ["A liquid is converted into its vapour at constant temperature and pressure.",
           "A substance dissolves in a specified amount of solvent.",
           "A solid is converted directly into its vapour at constant temperature and pressure.",
           "A covalent bond of a gaseous molecule is broken to give gaseous atoms or fragments."]),
    match("C", M("III I IV II"), [M("I III IV II"), M("III I II IV"), M("IV I III II")]),
    "Enthalpies of phase change, bond dissociation and solution",
    "Sublimation: solid → vapour. Vaporisation: liquid → vapour. Bond dissociation: breaking one mole of a "
    "bond in the gas phase. Enthalpy of solution: enthalpy change when one mole of a substance dissolves in a "
    "specified amount of solvent.",
    ["A → III", "B → I", "C → IV", "D → II"],
    why="The other codes interchange sublimation with vaporisation, or bond dissociation with solution.",
    ncert=f"{REF4}, enthalpies for different types of reactions", seconds=40)

add("Gibbs energy and K", I, "multi_statement",
    ms("Which of the following statements are correct?",
       ["If ΔrG° of a reaction is zero, its equilibrium constant K equals 1.",
        "ΔrG° = −2.303 RT log K.",
        "A reaction with a positive ΔrG° gives no products at all.",
        "For every reaction at equilibrium, ΔrG° = 0.",
        "The relation ΔG = ΔH − TΔS applies to a process at constant temperature."]),
    multi("D", {"a": True, "b": True, "c": False, "d": False, "e": True},
          ["(a), (b), (d) and (e) only", "(b), (c) and (e) only", "(a), (c) and (d) only"]),
    "Gibbs energy and the equilibrium constant",
    "ΔrG° = −RT ln K = −2.303 RT log K, so ΔrG° = 0 gives K = 1. A positive ΔrG° means K < 1: products form "
    "but only to a small extent. At equilibrium it is ΔrG (under the actual conditions) that is zero, not "
    "ΔrG°. The Gibbs equation ΔG = ΔH − TΔS is written for constant temperature.",
    ["(a) True: log K = 0 → K = 1", "(b) True", "(c) False: K < 1, not K = 0", "(d) False: ΔrG = 0, ΔrG° = "
     "−RT ln K", "(e) True"],
    why="Options with (c) or (d) are wrong; (a) and (b) together with (e) are all true.",
    ncert=f"{REF4}, Gibbs energy change and equilibrium", seconds=55)

add("Entropy and Gibbs energy", I, "assertion_reason",
    ar("For a given substance, the molar entropy increases in the order solid < liquid < gas.",
       "The randomness (disorder) of the particles increases from the solid to the liquid to the gaseous state."),
    AR_, "Entropy and the physical state",
    "Entropy measures the disorder of a system. Particles in a solid are held in fixed positions, those in a "
    "liquid move about, and those in a gas move freely through the whole container, so disorder and hence "
    "entropy increase in the order solid < liquid < gas. R explains A.",
    ["Solid: ordered → lowest S", "Liquid: more disordered", "Gas: most disordered → highest S"],
    answer="A", ncert=f"{REF4}, entropy and spontaneity", seconds=30)

dg_q = 5.74 + 5.74 * math.log10(0.01)
assert close(dg_q, -5.74) and close(5.74 - 5.74 * math.log10(0.01), 17.22) and close(5.74 * math.log10(0.01), -11.48)
add("Gibbs energy and K", A, "numerical",
    "For a reaction at 300 K, ΔrG° = +5.74 kJ mol⁻¹. In a reaction mixture at 300 K the reaction quotient is "
    "Q = 0.01. The Gibbs energy change ΔrG for the reaction under these conditions, and the direction of net "
    "change, are (2.303 RT = 5.74 kJ mol⁻¹ at 300 K):",
    Opts("B", "−5.74 kJ mol⁻¹; the reaction proceeds in the forward direction",
         ["+17.22 kJ mol⁻¹; the reaction proceeds in the reverse direction",
          "+5.74 kJ mol⁻¹; the reaction proceeds in the reverse direction",
          "−11.48 kJ mol⁻¹; the reaction proceeds in the forward direction"]),
    "ΔrG = ΔrG° + RT ln Q",
    "The Gibbs energy change under the actual conditions is ΔrG = ΔrG° + 2.303 RT log Q. A negative ΔrG means "
    "the forward reaction is spontaneous under those conditions, even though ΔrG° is positive.",
    ["log Q = log 0.01 = −2", "ΔrG = 5.74 + 5.74 × (−2) = −5.74 kJ mol⁻¹",
     "ΔrG < 0 → net reaction goes forward (Q < K)"],
    why="+17.22 kJ uses log Q = +2. +5.74 kJ ignores Q and judges by ΔrG° alone. −11.48 kJ omits the ΔrG° term.",
    ncert=f"{REF4}, Gibbs energy change and equilibrium; {C11}, 'Equilibrium', relation between K, Q and G",
    seconds=80, checked=True)

w_two = -(3 * (4 - 2) + 1 * (10 - 4)) * 100
assert w_two == -1200 and -3 * (10 - 2) * 100 == -2400 and -1 * (10 - 2) * 100 == -800
add("First law, work and enthalpy", A, "numerical",
    "A gas in a cylinder expands in two steps: first from 2 L to 4 L against a constant external pressure of "
    "3 bar, and then from 4 L to 10 L against a constant external pressure of 1 bar. The total work done on "
    "the gas is (1 L bar = 100 J):",
    Opts("D", "−1200 J", ["+1200 J", "−2400 J", "−800 J"]),
    "Work of irreversible expansion in steps",
    "For expansion against a constant external pressure, w = −p_ex ΔV. Work is not a state function, so each "
    "step is calculated with its own external pressure and the results are added.",
    ["Step 1: w₁ = −3 bar × (4 − 2) L = −6 L bar", "Step 2: w₂ = −1 bar × (10 − 4) L = −6 L bar",
     "w = −12 L bar = −1200 J"],
    why="+1200 J has the wrong sign: the gas does work on the surroundings, so work done on it is negative. "
        "−2400 J uses 3 bar for the whole change of 8 L, and −800 J uses 1 bar for the whole change.",
    ncert=f"{REF4}, work in irreversible expansion", seconds=60, checked=True)

add("Entropy and Gibbs energy", A, "statement_pair",
    sp("For the reaction 2Cl(g) → Cl₂(g), both ΔH and ΔS are negative.",
       "The reaction 2Cl(g) → Cl₂(g) is spontaneous at all temperatures."),
    SP_, "Signs of ΔH and ΔS and the effect of temperature",
    "Forming a Cl–Cl bond releases energy, so ΔH < 0; two gaseous atoms become one molecule, so ΔS < 0. "
    "Statement I is true. With both negative, ΔG = ΔH − TΔS is negative only when |TΔS| < |ΔH|, i.e. at low "
    "temperatures; at very high temperatures chlorine molecules dissociate. Statement II is false.",
    ["Bond formation → ΔH < 0; 2 mol gas → 1 mol → ΔS < 0 (I true)",
     "ΔH < 0, ΔS < 0 → spontaneous only below T = ΔH/ΔS (II false)"],
    answer="C", ncert=f"{REF4}, Gibbs energy and spontaneity", seconds=40)

add("Hess's law and enthalpies", A, "assertion_reason",
    ar("The standard enthalpy of formation of CO(g) cannot be found directly by burning carbon in a limited "
       "supply of oxygen.",
       "Burning carbon in a limited supply of oxygen gives a mixture of CO and CO₂."),
    AR_, "Use of Hess's law for enthalpies that cannot be measured directly",
    "If carbon is burnt in a limited supply of oxygen, part of it is oxidised to CO₂ as well, so the heat "
    "measured does not belong to the reaction C + ½O₂ → CO alone. This is why ΔfH°(CO) is obtained indirectly, "
    "from the enthalpies of combustion of carbon and of CO, using Hess's law. R explains A.",
    ["Limited O₂ → CO + CO₂ mixture → heat measured is for a mixture",
     "ΔfH°(CO) = ΔcH°(C) − ΔcH°(CO) via Hess's law"],
    answer="A", ncert=f"{REF4}, Hess's law of constant heat summation", seconds=40)

# ==================================================================== 5. Solutions
topic("Solutions")
REF5 = f"{C12}, 'Solutions'"

assert 25 / (25 + 100) * 100 == 20 and 25 / 100 * 100 == 25 and 100 / 125 * 100 == 80
add("Concentration terms", B, "numerical",
    "25 g of a solute is dissolved in 100 g of water. The mass percentage of the solute in the solution is:",
    Opts("B", "20%", ["25%", "80%", "2.5%"]),
    "Mass percentage",
    "Mass % of a component = (mass of the component / total mass of the solution) × 100. The total mass is "
    "the solute plus the solvent.",
    ["Mass of solution = 25 + 100 = 125 g", "Mass % = 25 / 125 × 100 = 20%"],
    why="25% divides by the mass of the solvent instead of the solution. 80% is the mass percentage of water. "
        "2.5% is a factor-of-ten slip.",
    ncert=f"{REF5}, expressing concentration of solutions: mass percentage", seconds=20, checked=True)

add("Raoult's law and ideal solutions", B, "direct",
    "Which of the following pairs of liquids forms a solution that shows positive deviation from Raoult's law?",
    Opts("C", "Carbon disulphide and acetone",
         ["Chloroform and acetone", "Phenol and aniline", "n-Hexane and n-heptane"]),
    "Positive and negative deviations",
    "In a solution showing positive deviation, the A–B attractions are weaker than the A–A and B–B attractions. "
    "In carbon disulphide–acetone, the dipolar interactions between acetone molecules are weakened on mixing "
    "with non-polar CS₂, so the solution shows positive deviation.",
    ["CS₂ + acetone: A–B weaker → positive deviation", "CHCl₃ + acetone; phenol + aniline: new H-bonds → negative",
     "n-hexane + n-heptane: nearly ideal"],
    why="Chloroform–acetone and phenol–aniline form hydrogen bonds between unlike molecules (negative deviation). "
        "n-Hexane–n-heptane is nearly ideal.",
    ncert=f"{REF5}, non-ideal solutions", seconds=25)

add("Colligative properties", B, "statement_pair",
    sp("In osmosis, solvent molecules pass through a semipermeable membrane from the pure solvent (or a dilute "
       "solution) into the more concentrated solution.",
       "Osmotic pressure is the excess pressure that must be applied to the solution side to just stop the "
       "passage of solvent into it."),
    SP_, "Osmosis and osmotic pressure",
    "Both statements describe osmosis as NCERT does: the net flow of solvent through a semipermeable membrane "
    "is towards the solution of higher concentration, and the osmotic pressure is the extra pressure that just "
    "prevents this flow.",
    ["Solvent flows from low solute concentration to high (I true)",
     "Osmotic pressure = pressure needed to stop osmosis (II true)"],
    answer="A", ncert=f"{REF5}, osmosis and osmotic pressure", seconds=30)

m_sol = 0.186 / 1.86
dtb = 0.512 * m_sol
assert close(m_sol, 0.1) and close(dtb, 0.0512) and close(100 + dtb, 100.0512, 1e-6)
add("Colligative properties", I, "numerical",
    "An aqueous solution of a non-volatile non-electrolyte freezes at −0.186 °C. At 1 atm, its boiling point "
    "is (for water K_f = 1.86 K kg mol⁻¹, K_b = 0.512 K kg mol⁻¹; normal boiling point of water = 100 °C):",
    Opts("D", "100.0512 °C", ["100.186 °C", "100.512 °C", "99.9488 °C"]),
    "Linking depression of freezing point and elevation of boiling point",
    "Both effects are proportional to the molality of the same solution: ΔT_f = K_f m and ΔT_b = K_b m. The "
    "molality found from the freezing point gives the boiling point elevation.",
    ["m = ΔT_f / K_f = 0.186 / 1.86 = 0.100 mol kg⁻¹", "ΔT_b = 0.512 × 0.100 = 0.0512 K",
     "Boiling point = 100 + 0.0512 = 100.0512 °C"],
    shortcut="ΔT_b = ΔT_f × K_b / K_f = 0.186 × 0.512 / 1.86.",
    why="100.186 °C assumes the elevation equals the depression. 100.512 °C takes the molality as 1. 99.9488 °C "
        "subtracts the elevation.",
    ncert=f"{REF5}, elevation of boiling point; depression of freezing point", seconds=50, checked=True)

molarity_h2so4 = 1000 * 1.84 * 0.98 / 98
assert close(molarity_h2so4, 18.4) and close(1000 * 0.98 / 98, 10.0) and close(1000 * 1.84 / 98, 18.78, 0.002)
add("Concentration terms", I, "numerical",
    "Concentrated sulphuric acid is 98% H₂SO₄ by mass and has a density of 1.84 g mL⁻¹. Its molarity is "
    "(H = 1, S = 32, O = 16):",
    Opts("A", "18.4 M", ["10.0 M", "18.8 M", "9.2 M"]),
    "Molarity from mass percentage and density",
    "Take 1 L of the solution: its mass is 1000 mL × density. 98% of that mass is H₂SO₄; dividing by the "
    "molar mass gives the moles in 1 L.",
    ["Mass of 1 L = 1000 × 1.84 = 1840 g", "Mass of H₂SO₄ = 0.98 × 1840 = 1803.2 g",
     "Moles = 1803.2 / 98 = 18.4 mol → 18.4 M"],
    why="10.0 M ignores the density (takes 1 L as 1000 g). 18.8 M forgets the 98% factor. 9.2 M halves the "
        "answer.",
    ncert=f"{REF5}, expressing concentration of solutions: molarity", seconds=55, checked=True)

add("Colligative properties", I, "assertion_reason",
    ar("A raw mango placed in a concentrated salt solution shrivels.",
       "Water passes out of the mango through its cell membranes into the more concentrated salt solution by "
       "osmosis."),
    AR_, "Osmosis in everyday life",
    "The salt solution outside has a higher solute concentration than the fluid inside the mango cells, so "
    "water moves out of the cells through the semipermeable membranes. The mango loses water and shrivels. R "
    "explains A.",
    ["Outside: concentrated salt solution", "Water flows out by osmosis → mango shrivels"],
    answer="A", ncert=f"{REF5}, osmosis and osmotic pressure", seconds=25)

add("Concentration terms", I, "match_list",
    lists("Match List-I (quantity) with List-II (its unit).",
          ["Molality", "Molarity", "Molal depression constant, K_f", "Mole fraction"],
          ["K kg mol⁻¹", "No unit", "mol L⁻¹", "mol kg⁻¹"]),
    match("B", M("IV III I II"), [M("III IV I II"), M("IV III II I"), M("I III IV II")]),
    "Units of concentration terms and constants",
    "Molality is moles of solute per kilogram of solvent; molarity is moles per litre of solution. K_f = ΔT_f/m "
    "has the unit K ÷ (mol kg⁻¹) = K kg mol⁻¹. Mole fraction is a ratio of moles and has no unit.",
    ["Molality → mol kg⁻¹ (IV)", "Molarity → mol L⁻¹ (III)", "K_f → K kg mol⁻¹ (I)", "Mole fraction → none (II)"],
    why="The other codes swap molality and molarity, or give K_f the unit of molality.",
    ncert=f"{REF5}, concentration terms; depression of freezing point", seconds=30)

add("Raoult's law and ideal solutions", I, "multi_statement",
    ms("Which of the following are true for a solution of two volatile liquids that shows a negative deviation "
       "from Raoult's law?",
       ["The A–B interactions are stronger than the A–A and B–B interactions.",
        "The enthalpy of mixing is negative.",
        "Such solutions can form maximum-boiling azeotropes.",
        "The volume of mixing is positive.",
        "The total vapour pressure is higher than that predicted by Raoult's law."]),
    multi("C", {"a": True, "b": True, "c": True, "d": False, "e": False},
          ["(a), (b), (c) and (d) only", "(b), (c) and (e) only", "(a), (d) and (e) only"]),
    "Negative deviation from Raoult's law",
    "Stronger A–B attractions hold the molecules more tightly in the solution, so fewer escape and the vapour "
    "pressure is lower than Raoult's law predicts. Heat is released (ΔmixH < 0) and the volume usually "
    "contracts (ΔmixV < 0). Such solutions can form maximum-boiling azeotropes.",
    ["(a) True", "(b) True", "(c) True", "(d) False: ΔmixV < 0", "(e) False: vapour pressure is lower"],
    why="Any option with (d) or (e) describes positive deviation.",
    ncert=f"{REF5}, non-ideal solutions; azeotropes", seconds=45)

m_naoh = 2.0 / ((1120 - 80) / 1000)
assert close(m_naoh, 1.923) and close(2.0 / 1.12, 1.786) and close(2.0 / 0.96, 2.08, 0.002)
add("Concentration terms", A, "numerical",
    "An aqueous solution of NaOH is 2.0 M and has a density of 1.12 g mL⁻¹. Its molality is (Na = 23, O = 16, "
    "H = 1):",
    Opts("B", "1.92 m", ["1.79 m", "2.00 m", "2.08 m"]),
    "Converting molarity to molality",
    "In 1 L of solution there are 2.0 mol (80 g) of NaOH. The mass of the solution is 1120 g, so the mass of "
    "water is 1120 − 80 = 1040 g. Molality is moles of solute per kilogram of solvent.",
    ["Mass of 1 L solution = 1000 × 1.12 = 1120 g", "Mass of NaOH = 2.0 × 40 = 80 g",
     "Mass of water = 1040 g = 1.040 kg", "m = 2.0 / 1.040 = 1.92 mol kg⁻¹"],
    why="1.79 m divides by the mass of the whole solution (1.12 kg). 2.00 m assumes molality equals molarity. "
        "2.08 m adds the solute mass to the solvent mass instead of subtracting it (2.0/0.96).",
    ncert=f"{REF5}, expressing concentration of solutions", seconds=70, checked=True)

add("van't Hoff factor", A, "statement_pair",
    sp("Aqueous solutions of glucose and urea having the same mass of solute per litre are isotonic at the same "
       "temperature.",
       "Isotonic solutions have the same molar concentration of solute particles at a given temperature."),
    SP_, "Isotonic solutions",
    "Osmotic pressure π = iCRT depends on the molar concentration of particles, not on the mass of solute. "
    "Glucose (180 g mol⁻¹) and urea (60 g mol⁻¹) at the same mass per litre have different molarities, so they "
    "are not isotonic; Statement I is false. Statement II is the condition for being isotonic and is true.",
    ["Same g L⁻¹ but M(glucose) = 3 × M(urea) → C(urea) = 3 C(glucose) (I false)",
     "Equal π ⇔ equal iC at the same T (II true)"],
    answer="D", ncert=f"{REF5}, osmosis and osmotic pressure", seconds=40)

add("van't Hoff factor", A, "assertion_reason",
    ar("0.1 m aqueous solutions of NaCl and KCl have nearly the same freezing point.",
       "The Na⁺ and K⁺ ions have the same size."),
    AR_, "Colligative properties depend on the number of particles",
    "NaCl and KCl are both strong 1 : 1 electrolytes; in dilute solution each gives about two ions per formula "
    "unit (i ≈ 2). At the same molality they give the same number of particles, so their freezing points are "
    "nearly equal: A is true. K⁺ is larger than Na⁺ (it has one more shell), so R is false; in any case ion "
    "size does not decide a colligative property.",
    ["Both i ≈ 2 at the same m → same ΔT_f (A true)", "K⁺ has one more electron shell than Na⁺ → larger (R false)"],
    answer="C", ncert=f"{REF5}, abnormal molar masses: van't Hoff factor", seconds=35)

# ==================================================================== 6. Equilibrium
topic("Equilibrium")
REF6 = f"{C11}, 'Equilibrium'"

ph_h2so4 = -math.log10(2 * 0.05)
assert close(ph_h2so4, 1.0) and close(-math.log10(0.05), 1.30, 0.002)
add("Acids, bases and pH", B, "numerical",
    "The pH of a 0.05 M aqueous solution of H₂SO₄ at 298 K, assuming that both protons ionise completely, is "
    "(log 5 = 0.70):",
    Opts("C", "1.0", ["1.3", "13.0", "0.7"]),
    "pH of a strong dibasic acid",
    "Each H₂SO₄ gives two H⁺ ions when completely ionised, so [H⁺] = 2 × 0.05 = 0.10 M.",
    ["[H⁺] = 2 × 0.05 = 0.10 M", "pH = −log 0.10 = 1.0"],
    why="1.3 counts only one proton per molecule (−log 0.05). 13.0 is the pOH. 0.7 takes log 5 as the pH.",
    ncert=f"{REF6}, the pH scale", seconds=25, checked=True)

kc_pcl5 = 0.2 * 0.2 / 0.5
assert close(kc_pcl5, 0.08) and close(1 / kc_pcl5, 12.5)
add("Kp, Kc and Le Chatelier", B, "numerical",
    "At equilibrium at a certain temperature, the concentrations in the reaction PCl₅(g) ⇌ PCl₃(g) + Cl₂(g) "
    "are [PCl₅] = 0.50 mol L⁻¹, [PCl₃] = 0.20 mol L⁻¹ and [Cl₂] = 0.20 mol L⁻¹. The value of K_c is:",
    Opts("B", "0.08 mol L⁻¹", ["12.5 L mol⁻¹", "0.40 mol L⁻¹", "0.80 mol L⁻¹"]),
    "Equilibrium constant expression",
    "K_c = [PCl₃][Cl₂] / [PCl₅], with each concentration at equilibrium.",
    ["K_c = (0.20 × 0.20) / 0.50 = 0.04 / 0.50 = 0.08 mol L⁻¹"],
    why="12.5 L mol⁻¹ is K_c for the reverse reaction. 0.40 mol L⁻¹ counts only one product (0.20/0.50), "
        "and 0.80 mol L⁻¹ adds the two product concentrations instead of multiplying them (0.40/0.50).",
    ncert=f"{REF6}, law of chemical equilibrium and equilibrium constant", seconds=25, checked=True)

add("Acids, bases and pH", B, "direct",
    "Which of the following species is a Lewis acid but NOT a Brønsted–Lowry acid?",
    Opts("D", "BCl₃", ["HCl", "NH₄⁺", "H₂O"]),
    "Lewis and Brønsted–Lowry acids",
    "A Brønsted–Lowry acid donates a proton; a Lewis acid accepts an electron pair. BCl₃ has an incomplete "
    "octet on boron and accepts an electron pair, but it has no hydrogen to donate as a proton.",
    ["BCl₃: electron-pair acceptor, no H → Lewis acid only", "HCl, NH₄⁺, H₂O: can donate H⁺ → Brønsted acids"],
    why="HCl, NH₄⁺ and H₂O can each give a proton, so they are Brønsted–Lowry acids.",
    ncert=f"{REF6}, Lewis acids and bases", seconds=25)

add("Physical equilibria and Henry's law", B, "statement_pair",
    sp("Equilibrium in a physical process can be established only in a closed system at a given temperature.",
       "At equilibrium, the concentrations of the reactants and the products are equal."),
    SP_, "Characteristics of equilibrium",
    "NCERT states that equilibrium is possible only in a closed system at a given temperature, so Statement I "
    "is true. At equilibrium the rates of the forward and reverse processes are equal and the concentrations "
    "stay constant, but they are generally not equal to each other. Statement II is false.",
    ["Closed system, fixed T (I true)", "Equal rates, constant (not equal) concentrations (II false)"],
    answer="C", ncert=f"{REF6}, equilibrium in physical processes", seconds=25)

add("Acids, bases and pH", B, "match_list",
    lists("Match List-I (acid) with List-II (its conjugate base).",
          ["H₂O", "H₃O⁺", "HCO₃⁻", "NH₃"],
          ["H₂O", "CO₃²⁻", "NH₂⁻", "OH⁻"]),
    match("A", M("IV I II III"), [M("I IV II III"), M("IV I III II"), M("IV II I III")]),
    "Conjugate acid–base pairs",
    "The conjugate base of an acid is what remains after it donates one proton (H⁺).",
    ["H₂O − H⁺ → OH⁻ (IV)", "H₃O⁺ − H⁺ → H₂O (I)", "HCO₃⁻ − H⁺ → CO₃²⁻ (II)", "NH₃ − H⁺ → NH₂⁻ (III)"],
    why="The other codes give H₂O as its own conjugate base or remove a proton from the wrong species.",
    ncert=f"{REF6}, Brønsted–Lowry acids and bases", seconds=30)

oh_base = math.sqrt(1.0e-6 * 0.01)
assert close(oh_base, 1e-4) and close(14 + math.log10(oh_base), 10.0)
add("Acids, bases and pH", I, "numerical",
    "The pH of a 0.01 M aqueous solution of a weak monoacidic base BOH (K_b = 1.0 × 10⁻⁶) at 298 K is "
    "(K_w = 1.0 × 10⁻¹⁴):",
    Opts("B", "10", ["4", "6", "12"]),
    "pH of a weak base",
    "For a weak base with small ionisation, [OH⁻] = √(K_b × c). Then pOH = −log[OH⁻] and pH = 14 − pOH.",
    ["[OH⁻] = √(1.0 × 10⁻⁶ × 0.01) = √(10⁻⁸) = 1.0 × 10⁻⁴ M", "pOH = 4", "pH = 14 − 4 = 10"],
    why="4 is the pOH. 12 treats the base as fully ionised ([OH⁻] = 0.01 M). 6 uses [OH⁻] = K_b × c = 10⁻⁸ M "
        "without the square root.",
    ncert=f"{REF6}, ionization of weak bases", seconds=45, checked=True)

ph_323 = 0.5 * (14 - 0.74)
assert close(ph_323, 6.63) and close(-math.log10(math.sqrt(5.5e-14)), 6.63, 0.002)
add("Acids, bases and pH", I, "numerical",
    "The ionic product of water at 323 K is 5.5 × 10⁻¹⁴. The pH of pure water at 323 K is (log 5.5 = 0.74):",
    Opts("D", "6.63", ["7.00", "13.26", "7.37"]),
    "pH of neutral water at a temperature other than 298 K",
    "In pure water [H₃O⁺] = [OH⁻] = √K_w, so pH = ½ pK_w. K_w increases with temperature, so the pH of neutral "
    "water falls below 7 at 323 K although the water is still neutral.",
    ["pK_w = −log(5.5 × 10⁻¹⁴) = 14 − 0.74 = 13.26", "pH = ½ × 13.26 = 6.63"],
    why="7.00 is the value at 298 K only. 13.26 is pK_w. 7.37 adds 0.74 instead of subtracting it.",
    ncert=f"{REF6}, the ionization constant of water and its ionic product", seconds=45, checked=True)

add("Acids, bases and pH", I, "assertion_reason",
    ar("At the same concentration (0.1 M) and temperature, the pH of an acetic acid solution is higher than that "
       "of a hydrochloric acid solution.",
       "Acetic acid is only partially ionised in water, whereas hydrochloric acid is almost completely ionised."),
    AR_, "Strong and weak acids",
    "Because acetic acid is a weak acid, only a small fraction of its molecules give H₃O⁺ ions, so [H₃O⁺] is "
    "much less than 0.1 M and the pH is higher than that of 0.1 M HCl (pH 1). R explains A.",
    ["HCl: [H₃O⁺] ≈ 0.1 M → pH ≈ 1", "CH₃COOH: [H₃O⁺] ≪ 0.1 M → pH higher"],
    answer="A", ncert=f"{REF6}, ionization of acids and bases", seconds=30)

add("Kp, Kc and Le Chatelier", I, "statement_pair",
    sp("Adding an inert gas at constant pressure to the equilibrium mixture N₂O₄(g) ⇌ 2NO₂(g) shifts the "
       "equilibrium towards NO₂.",
       "Adding an inert gas does not change the value of K_p of this equilibrium at constant temperature."),
    SP_, "Inert gas at constant pressure",
    "At constant pressure, adding an inert gas increases the volume, which lowers the partial pressures of N₂O₄ "
    "and NO₂. The equilibrium then shifts towards the side with more moles of gas, i.e. towards NO₂; Statement "
    "I is true. An equilibrium constant changes only with temperature, so K_p is unchanged; Statement II is "
    "true.",
    ["Constant p + inert gas → V increases → shift to more gas moles (NO₂) (I true)",
     "K depends only on T (II true)"],
    answer="A", ncert=f"{REF6}, factors affecting equilibria: effect of inert gas addition", seconds=40)

add("Hydrolysis and buffers", I, "match_list",
    lists("Match List-I (solution) with List-II (expression for its pH or pOH at 298 K; c = concentration of the "
          "salt).",
          ["Buffer of a weak acid and its salt with a strong base", "Buffer of a weak base and its salt with a "
           "strong acid", "Salt of a weak acid and a strong base", "Salt of a strong acid and a weak base"],
          ["pH = 7 − ½pK_b − ½log c", "pH = pK_a + log([salt]/[acid])", "pH = 7 + ½pK_a + ½log c",
           "pOH = pK_b + log([salt]/[base])"]),
    match("D", M("II IV III I"), [M("II IV I III"), M("IV II III I"), M("III IV II I")]),
    "Henderson–Hasselbalch equation and hydrolysis of salts",
    "Acidic and basic buffers obey the Henderson–Hasselbalch equations. The salt of a weak acid and a strong "
    "base hydrolyses to give a basic solution, pH = 7 + ½(pK_a + log c); the salt of a strong acid and a weak "
    "base gives an acidic solution, pH = 7 − ½(pK_b + log c).",
    ["Acidic buffer → II", "Basic buffer → IV", "e.g. CH₃COONa → III (pH > 7)", "e.g. NH₄Cl → I (pH < 7)"],
    why="The other codes give the basic-solution formula to NH₄Cl-type salts or swap the two buffer equations.",
    ncert=f"{REF6}, buffer solutions; hydrolysis of salts and the pH of their solutions", seconds=50)

add("Physical equilibria and Henry's law", I, "multi_statement",
    ms("Which of the following statements about physical equilibria are correct?",
       ["At a given pressure, ice and liquid water coexist in equilibrium at only one temperature.",
        "In a saturated sugar solution kept in contact with undissolved sugar at constant temperature, the mass of "
        "undissolved sugar keeps decreasing with time.",
        "When a sealed bottle of soda water is opened, some dissolved carbon dioxide escapes because its partial "
        "pressure above the liquid falls.",
        "Water boils at a lower temperature at a high altitude, where the atmospheric pressure is lower.",
        "For I₂(s) ⇌ I₂(vapour) in a closed vessel, sublimation stops completely once equilibrium is reached."]),
    multi("A", {"a": True, "b": False, "c": True, "d": True, "e": False},
          ["(a), (b) and (d) only", "(c), (d) and (e) only", "(a), (c), (d) and (e) only"]),
    "Solid–liquid, liquid–vapour, solid–vapour and gas–solution equilibria",
    "The melting point is fixed at a given pressure. A saturated solution is a dynamic equilibrium: sugar "
    "dissolves and crystallises at equal rates, so the amount of solid stays constant. Opening a soda bottle "
    "lowers the pressure of CO₂ above it, so by Henry's law its solubility falls. The boiling point depends on "
    "the external pressure. At equilibrium sublimation and deposition continue at equal rates.",
    ["(a) True", "(b) False: amount of solid constant at equilibrium", "(c) True", "(d) True",
     "(e) False: equilibrium is dynamic"],
    why="Options with (b) or (e) treat equilibrium as static.",
    ncert=f"{REF6}, equilibrium in physical processes", seconds=55)

add("Physical equilibria and Henry's law", I, "direct",
    "To avoid the painful condition called 'bends' caused by nitrogen dissolving in the blood at high pressure, "
    "the tanks used by scuba divers are filled with air diluted with:",
    Opts("B", "Helium", ["Nitrogen", "Carbon dioxide", "Hydrogen"]),
    "Application of Henry's law",
    "At the high pressure under water the solubility of nitrogen in blood increases (Henry's law); on surfacing "
    "it comes out as bubbles. Diluting the air with helium, which is much less soluble in blood, avoids this. "
    "NCERT gives the composition as about 11.7% helium, 56.2% nitrogen and 32.1% oxygen.",
    ["High pressure → more N₂ dissolves", "Release of pressure → bubbles (bends)",
     "Helium: low solubility → used to dilute the air"],
    why="Adding nitrogen would make the problem worse. Carbon dioxide and hydrogen are not used; CO₂ is far more "
        "soluble and toxic at high levels, and hydrogen is flammable.",
    ncert=f"{C12}, 'Solutions', solubility of a gas in a liquid: applications of Henry's law", seconds=25)

ph_acid_alone = 0.5 * (4.74 - math.log10(0.2))
mmol_acid, mmol_base = 50 * 0.2, 25 * 0.2
assert mmol_acid - mmol_base == mmol_base and close(ph_acid_alone, 2.72, 0.002)
add("Hydrolysis and buffers", A, "numerical",
    "50 mL of 0.2 M CH₃COOH is mixed with 25 mL of 0.2 M NaOH at 298 K. The pH of the resulting solution is "
    "(pK_a of CH₃COOH = 4.74):",
    Opts("C", "4.74", ["2.72", "7.00", "9.26"]),
    "Buffer formed by partial neutralisation",
    "NaOH converts part of the acetic acid into sodium acetate. Here exactly half the acid is neutralised, so "
    "the solution contains equal amounts of CH₃COOH and CH₃COO⁻ and is a buffer with pH = pK_a.",
    ["CH₃COOH = 50 × 0.2 = 10 mmol; NaOH = 25 × 0.2 = 5 mmol",
     "After reaction: CH₃COOH 5 mmol, CH₃COO⁻ 5 mmol",
     "pH = pK_a + log(5/5) = 4.74"],
    why="2.72 is the pH of the 0.2 M acid alone. 7.00 assumes complete neutralisation to a neutral solution. "
        "9.26 is 14 − pK_a.",
    ncert=f"{REF6}, buffer solutions", seconds=60, checked=True)

x_hi = 2 / 10  # x/(2 - 2x) = 1/8
assert close(x_hi / (2 - 2 * x_hi), 1 / 8) and close((x_hi * x_hi) / (2 - 2 * x_hi) ** 2, 1 / 64)
assert close(16 / 18, 0.889, 0.002) and close(2 / 9, 0.222, 0.002)
add("Kp, Kc and Le Chatelier", A, "numerical",
    "For H₂(g) + I₂(g) ⇌ 2HI(g), K_c = 64 at a certain temperature. 2.0 mol of pure HI is placed in a closed "
    "1.0 L vessel at this temperature. The amount of H₂ present at equilibrium is:",
    Opts("A", "0.20 mol", ["0.89 mol", "1.60 mol", "0.22 mol"]),
    "Equilibrium approached from the product side",
    "For the decomposition 2HI ⇌ H₂ + I₂, K_c = 1/64. If x mol of H₂ forms, then x mol of I₂ forms and 2x mol "
    "of HI is used up.",
    ["At equilibrium: [H₂] = [I₂] = x, [HI] = 2.0 − 2x", "x² / (2.0 − 2x)² = 1/64 → x / (2.0 − 2x) = 1/8",
     "8x = 2.0 − 2x → x = 0.20 mol"],
    why="0.89 mol uses K = 64 for the decomposition instead of 1/64. 1.60 mol is the HI left, not the H₂ formed. "
        "0.22 mol uses 2.0 − x for HI, forgetting that 2 mol HI give 1 mol H₂.",
    ncert=f"{REF6}, calculating equilibrium concentrations", seconds=90, checked=True)

h_weak = 0.1 * 0.01
assert close(h_weak, 1e-3)
add("Acids, bases and pH", A, "multi_statement",
    ms("Which of the following statements are correct for aqueous solutions at 298 K?",
       ["The degree of ionisation of a weak acid increases on dilution.",
        "At a fixed temperature, the ionisation constant K_a of a weak acid changes with its concentration.",
        "In a 0.1 M solution of a weak monobasic acid that is 1% ionised, [H₃O⁺] = 1 × 10⁻³ M.",
        "A solution with pOH = 4 has pH = 10.",
        "An acid with a larger K_a has a larger pK_a."]),
    multi("D", {"a": True, "b": False, "c": True, "d": True, "e": False},
          ["(a), (b) and (c) only", "(c), (d) and (e) only", "(a), (c), (d) and (e) only"]),
    "Ionisation of weak acids and the pH scale",
    "For a weak acid α ≈ √(K_a/c), so α increases as c decreases. K_a depends only on temperature. [H₃O⁺] = cα = "
    "0.1 × 0.01 = 10⁻³ M. At 298 K, pH + pOH = 14. pK_a = −log K_a, so a larger K_a means a smaller pK_a.",
    ["(a) True", "(b) False: K_a depends only on T", "(c) True: 0.1 × 0.01", "(d) True: 14 − 4",
     "(e) False: larger K_a → smaller pK_a"],
    why="Options with (b) or (e) include a false statement.",
    ncert=f"{REF6}, ionization constants of weak acids", seconds=55)

add("Kp, Kc and Le Chatelier", A, "statement_pair",
    sp("For CaCO₃(s) ⇌ CaO(s) + CO₂(g) at equilibrium in a closed vessel, adding more CaCO₃(s) at constant "
       "temperature shifts the equilibrium in the forward direction.",
       "Removing some CO₂ from the vessel at constant temperature shifts the equilibrium in the forward "
       "direction."),
    SP_, "Heterogeneous equilibrium and Le Chatelier's principle",
    "Here K_p = p(CO₂); pure solids do not appear in the expression, so adding more CaCO₃ does not change the "
    "position of equilibrium. Statement I is false. Removing CO₂ lowers p(CO₂) below K_p, so more CaCO₃ "
    "decomposes to restore it. Statement II is true.",
    ["K_p = p(CO₂): solids excluded → extra CaCO₃ has no effect (I false)",
     "Remove CO₂ → Q < K → forward shift (II true)"],
    answer="D", ncert=f"{REF6}, heterogeneous equilibria; Le Chatelier's principle", seconds=40)

add("Kp, Kc and Le Chatelier", A, "assertion_reason",
    ar("Increasing the pressure on the equilibrium ice ⇌ liquid water at 273 K shifts it towards ice.",
       "Ice occupies a larger volume than the same mass of liquid water."),
    AR_, "Effect of pressure on the solid–liquid equilibrium of water",
    "Ice is less dense than liquid water, so a given mass of ice has the larger volume (R true). By Le "
    "Chatelier's principle, increased pressure favours the change that reduces volume, i.e. melting of ice to "
    "water. So pressure shifts the equilibrium towards liquid water, and A is false.",
    ["V(ice) > V(water) for the same mass (R true)", "Higher pressure → smaller volume favoured → ice melts (A false)"],
    answer="D", ncert=f"{REF6}, Le Chatelier's principle", seconds=40)

# ==================================================================== 7. Redox Reactions and Electrochemistry
topic("Redox Reactions and Electrochemistry")
REF7R = f"{C11}, 'Redox Reactions'"
REF7E = f"{C12}, 'Electrochemistry'"

x_n = 0 - (2 * 1 + (-2) + 1)
assert x_n == -1
add("Oxidation number and balancing", B, "numerical",
    "The oxidation number of nitrogen in hydroxylamine, NH₂OH, is:",
    Opts("B", "−1", ["+1", "−3", "+3"]),
    "Oxidation number from the rules",
    "In NH₂OH each hydrogen is +1 and oxygen is −2, and the sum of oxidation numbers in a neutral molecule is "
    "zero.",
    ["x + 2(+1) + (−2) + (+1) = 0", "x + 1 = 0 → x = −1"],
    why="−3 is the value in NH₃, where N carries three H atoms. +1 and +3 give the wrong sign or ignore the "
        "hydrogen of the OH group.",
    ncert=f"{REF7R}, oxidation number", seconds=25, checked=True)

m_water = (4 / 2) * 18
assert m_water == 36
add("Batteries and fuel cells", B, "numerical",
    "In a hydrogen–oxygen fuel cell the overall reaction is 2H₂(g) + O₂(g) → 2H₂O(l). The mass of water "
    "formed when 4 g of hydrogen is consumed is (H = 1, O = 16):",
    Opts("D", "36 g", ["18 g", "72 g", "32 g"]),
    "Stoichiometry of the fuel cell reaction",
    "Each mole of H₂ consumed gives one mole of water.",
    ["n(H₂) = 4 / 2 = 2 mol", "n(H₂O) = 2 mol", "Mass = 2 × 18 = 36 g"],
    why="18 g is for 1 mol of H₂ (2 g). 72 g doubles the mole ratio. 32 g is the mass of O₂ consumed, not of water "
        "formed.",
    ncert=f"{REF7E}, fuel cells", seconds=25, checked=True)

add("Oxidation number and balancing", B, "direct",
    "Which of the following changes is a reduction?",
    Opts("C", "MnO₄⁻ → Mn²⁺", ["Fe²⁺ → Fe³⁺", "2Cl⁻ → Cl₂", "H₂O₂ → O₂"]),
    "Reduction as a decrease in oxidation number",
    "Reduction is a gain of electrons, i.e. a decrease in the oxidation number of an element.",
    ["Mn: +7 → +2 (decrease) → reduction", "Fe: +2 → +3 (increase) → oxidation",
     "Cl: −1 → 0 → oxidation", "O: −1 → 0 → oxidation"],
    why="In the other three changes the oxidation number increases, so they are oxidations.",
    ncert=f"{REF7R}, redox reactions in terms of electron transfer; oxidation number", seconds=25)

add("Conductance and Kohlrausch's law", B, "statement_pair",
    sp("The electronic (metallic) conductance of a metal increases with increase in temperature.",
       "The conductance of an electrolytic solution is due to the movement of electrons through the solution."),
    SP_, "Electronic and electrolytic conduction",
    "In metals, conduction is by electrons, and the conductance decreases as the temperature rises, so "
    "Statement I is false. In an electrolytic solution the current is carried by the movement of ions, not of "
    "free electrons; Statement II is false too.",
    ["Metals: conductance falls as T rises (I false)", "Electrolytes: ions carry the charge (II false)"],
    answer="B", ncert=f"{REF7E}, conductance of electrolytic solutions", seconds=30)

e_cu = 0.34 - (0.059 / 2) * math.log10(1 / 0.01)
assert close(e_cu, 0.281) and close(0.34 + 0.059, 0.399) and close(0.34 - 0.118, 0.222)
add("Nernst equation and Gibbs energy", I, "numerical",
    "The reduction potential of a copper electrode dipped in 0.01 M Cu²⁺ solution at 298 K is "
    "(E°(Cu²⁺/Cu) = +0.34 V, 2.303RT/F = 0.059 V):",
    Opts("A", "0.281 V", ["0.399 V", "0.222 V", "0.340 V"]),
    "Nernst equation for a single electrode",
    "For Cu²⁺ + 2e⁻ → Cu, E = E° − (0.059/2) log(1/[Cu²⁺]). A lower concentration of Cu²⁺ makes the reduction "
    "potential less positive.",
    ["E = 0.34 − (0.059/2) log(1/0.01)", "= 0.34 − 0.0295 × 2 = 0.34 − 0.059 = 0.281 V"],
    why="0.399 V adds the correction (wrong sign). 0.222 V uses n = 1 instead of 2. 0.340 V is the standard "
        "potential, valid only at 1 M.",
    ncert=f"{REF7E}, Nernst equation", seconds=45, checked=True)

h2so4_used = 0.5 * 98  # 2 mol H2SO4 per 2 mol e-, i.e. 1 mol per faraday
assert h2so4_used == 49 and 0.25 * 98 == 24.5 and 0.125 * 98 == 12.25
add("Batteries and fuel cells", I, "numerical",
    "During discharge of a lead storage battery the overall reaction is "
    "Pb(s) + PbO₂(s) + 2H₂SO₄(aq) → 2PbSO₄(s) + 2H₂O(l), in which two electrons are transferred. The mass of "
    "H₂SO₄ consumed when 0.5 F (48 250 C) of charge is drawn from the battery is (H₂SO₄ = 98 g mol⁻¹):",
    Opts("D", "49 g", ["24.5 g", "98 g", "12.25 g"]),
    "Charge and stoichiometry in the lead storage battery",
    "As written, the reaction transfers 2 mol of electrons and consumes 2 mol of H₂SO₄, i.e. 1 mol of H₂SO₄ per "
    "faraday (1 mol of electrons).",
    ["2 mol e⁻ ↔ 2 mol H₂SO₄ → 1 mol H₂SO₄ per F", "0.5 F → 0.5 mol H₂SO₄", "Mass = 0.5 × 98 = 49 g"],
    why="24.5 g assumes 1 mol H₂SO₄ per 2 F. 98 g is for 1 F. 12.25 g divides by 2 twice.",
    ncert=f"{REF7E}, batteries: secondary batteries (lead storage battery)", seconds=55, checked=True)

add("Electrode potential and cells", I, "assertion_reason",
    ar("Fe³⁺ ions oxidise iodide ions to iodine in aqueous solution under standard conditions.",
       "E°(Fe³⁺/Fe²⁺) = +0.77 V is higher than E°(I₂/I⁻) = +0.54 V."),
    AR_, "Predicting redox reactions from standard electrode potentials",
    "The couple with the higher reduction potential is reduced and the other is oxidised. Since Fe³⁺/Fe²⁺ has "
    "the higher E°, Fe³⁺ is reduced to Fe²⁺ while I⁻ is oxidised to I₂: E°cell = 0.77 − 0.54 = +0.23 V > 0. R "
    "explains A.",
    ["2Fe³⁺ + 2I⁻ → 2Fe²⁺ + I₂", "E°cell = 0.77 − 0.54 = +0.23 V → spontaneous"],
    answer="A", ncert=f"{REF7E}, electrochemical series and electrode potentials", seconds=35)

add("Batteries and fuel cells", I, "match_list",
    lists("Match List-I (cell) with List-II (electrolyte used in it).",
          ["Dry (Leclanché) cell", "Lead storage battery", "Hydrogen–oxygen fuel cell (as described in NCERT)",
           "Daniell cell"],
          ["Concentrated aqueous sodium hydroxide solution", "Moist paste of ammonium chloride and zinc chloride",
           "Solutions of ZnSO₄ and CuSO₄ connected by a salt bridge", "About 38% sulphuric acid solution"]),
    match("C", M("II IV I III"), [M("II I IV III"), M("IV II I III"), M("II IV III I")]),
    "Electrolytes of common cells",
    "The dry cell uses a moist paste of NH₄Cl and ZnCl₂ around the carbon cathode. The lead storage battery "
    "uses about 38% H₂SO₄. In the H₂–O₂ fuel cell, H₂ and O₂ are bubbled through porous carbon electrodes into "
    "concentrated aqueous NaOH. The Daniell cell uses ZnSO₄ and CuSO₄ solutions.",
    ["A → II", "B → IV", "C → I", "D → III"],
    why="The other codes give the fuel cell the acid electrolyte of the lead battery, or swap the dry cell and "
        "the Daniell cell.",
    ncert=f"{REF7E}, batteries and fuel cells; galvanic cells", seconds=40)

e_vals = {"Zn": -0.76, "Fe": -0.44, "Ni": -0.25, "Ag": 0.80}
assert [m for m, e in e_vals.items() if e > 0.34] == ["Ag"]
add("Electrode potential and cells", I, "direct",
    "Given E°(Cu²⁺/Cu) = +0.34 V, E°(Zn²⁺/Zn) = −0.76 V, E°(Fe²⁺/Fe) = −0.44 V, E°(Ni²⁺/Ni) = −0.25 V and "
    "E°(Ag⁺/Ag) = +0.80 V, a 1 M copper sulphate solution can be stored without reaction in a vessel made of:",
    Opts("D", "Silver", ["Zinc", "Iron", "Nickel"]),
    "Displacement reactions from E° values",
    "A metal with a lower reduction potential than Cu²⁺/Cu reduces Cu²⁺ ions (displaces copper) and is itself "
    "dissolved. Only a metal with a higher E° than +0.34 V does not react.",
    ["Zn, Fe, Ni: E° < +0.34 V → they displace Cu", "Ag: E° = +0.80 V > +0.34 V → no reaction"],
    why="Zinc, iron and nickel are stronger reducing agents than copper and would react with the CuSO₄ solution.",
    ncert=f"{REF7E}, electrochemical series", seconds=35)

ons = {"Cr in CrO4": -2 + 4 * 2, "C in CH2O": 0 - (2 * 1 - 2), "Cl in ClO2": 0 + 2 * 2,
       "N in N2O": (0 + 2) / 2}
assert ons == {"Cr in CrO4": 6, "C in CH2O": 0, "Cl in ClO2": 4, "N in N2O": 1}
add("Oxidation number and balancing", I, "multi_statement",
    ms("Which of the following oxidation numbers are correct?",
       ["Cr in CrO₄²⁻: +6", "C in formaldehyde, HCHO: 0", "S in S₈: 0", "Cl in ClO₂: +3", "N in N₂O: +1"]),
    multi("B", {"a": True, "b": True, "c": True, "d": False, "e": True},
          ["(a), (b) and (c) only", "(a), (c), (d) and (e) only", "(b), (c), (d) and (e) only"]),
    "Assigning oxidation numbers",
    "Use O = −2 and H = +1, the sum equal to the charge, and zero for an element in its free state.",
    ["(a) x + 4(−2) = −2 → x = +6 ✓", "(b) x + 2(+1) + (−2) = 0 → x = 0 ✓", "(c) element → 0 ✓",
     "(d) x + 2(−2) = 0 → x = +4, not +3 ✗", "(e) 2x + (−2) = 0 → x = +1 ✓"],
    why="Options containing (d) are wrong; the option (a), (b), (c) only leaves out the correct (e).",
    ncert=f"{REF7R}, oxidation number", seconds=50)

kappa, lam0 = 1.38e-6, 138
s_agcl = 1000 * kappa / lam0
assert close(s_agcl, 1.0e-5) and close(s_agcl ** 2, 1.0e-10) and close((kappa / lam0) ** 2, 1.0e-16)
assert close(kappa / lam0, 1.0e-8)
add("Conductance and Kohlrausch's law", A, "numerical",
    "The conductivity of a saturated solution of AgCl at 298 K, after subtracting the conductivity of the water "
    "used, is 1.38 × 10⁻⁶ S cm⁻¹. The limiting molar conductivity of AgCl is 138 S cm² mol⁻¹. Taking the molar "
    "conductivity of this very dilute solution as equal to the limiting value, the solubility product of AgCl "
    "is:",
    Opts("A", "1.0 × 10⁻¹⁰", ["1.0 × 10⁻⁵", "1.0 × 10⁻¹⁶", "1.0 × 10⁻⁸"]),
    "Kohlrausch's law applied to a sparingly soluble salt",
    "For a saturated solution, Λm ≈ Λ°m and Λm = 1000 κ / c (κ in S cm⁻¹, c in mol L⁻¹). This gives the "
    "solubility c = s, and for AgCl, K_sp = s².",
    ["s = 1000 κ / Λ°m = 1000 × 1.38 × 10⁻⁶ / 138 = 1.0 × 10⁻⁵ mol L⁻¹", "K_sp = s² = (1.0 × 10⁻⁵)² = 1.0 × 10⁻¹⁰"],
    why="1.0 × 10⁻⁵ is the solubility, not K_sp. 1.0 × 10⁻⁸ and 1.0 × 10⁻¹⁶ leave out the factor 1000 that "
        "converts cm³ to L (the second also squares it).",
    ncert=f"{REF7E}, Kohlrausch law and its applications", seconds=80, checked=True)

add("Nernst equation and Gibbs energy", A, "statement_pair",
    sp("When a galvanic cell is completely discharged, i.e. its cell reaction has reached equilibrium, "
       "E_cell = 0.",
       "A cell reaction with a positive E°cell has an equilibrium constant less than 1."),
    SP_, "Cell potential at equilibrium; E° and K",
    "At equilibrium ΔrG = −nFE_cell = 0, so E_cell = 0 and Q = K; Statement I is true. From "
    "E°cell = (2.303RT/nF) log K, a positive E°cell gives log K > 0, i.e. K > 1. Statement II is false.",
    ["Equilibrium: ΔrG = 0 → E_cell = 0 (I true)", "E°cell > 0 → log K > 0 → K > 1 (II false)"],
    answer="C", ncert=f"{REF7E}, equilibrium constant from Nernst equation", seconds=40)

add("Oxidation number and balancing", A, "assertion_reason",
    ar("Fluorine does not undergo disproportionation reactions.",
       "Being the most electronegative element, fluorine cannot show a positive oxidation state."),
    AR_, "Disproportionation and the oxidation states of fluorine",
    "In disproportionation an element is oxidised and reduced at the same time, so it must be able to go both "
    "up and down from its oxidation state. Fluorine is the most electronegative element and has no positive "
    "oxidation state; in its compounds it is always −1. So it cannot be oxidised from 0, and it does not "
    "disproportionate. R explains A.",
    ["Disproportionation needs a higher and a lower oxidation state", "F: only 0 and −1 → cannot go higher"],
    answer="A", ncert=f"{REF7R}, types of redox reactions: disproportionation reactions", seconds=35)


def _balance(eq):
    """eq = (left, right) lists of (coeff, {element: n}, charge); returns True if atoms and charge balance."""
    tot = []
    for side in eq:
        atoms, charge = Counter(), 0
        for k, f, q in side:
            for el, n in f.items():
                atoms[el] += k * n
            charge += k * q
        tot.append((atoms, charge))
    return tot[0] == tot[1]


CR2O7, SO2, HP = {"Cr": 2, "O": 7}, {"S": 1, "O": 2}, {"H": 1}
CR3, SO4, H2O = {"Cr": 1}, {"S": 1, "O": 4}, {"H": 2, "O": 1}
assert _balance(([(1, CR2O7, -2), (3, SO2, 0), (2, HP, 1)], [(2, CR3, 3), (3, SO4, -2), (1, H2O, 0)]))
assert not _balance(([(1, CR2O7, -2), (3, SO2, 0), (8, HP, 1)], [(2, CR3, 3), (3, SO4, -2), (4, H2O, 0)]))
assert not _balance(([(1, CR2O7, -2), (1, SO2, 0), (2, HP, 1)], [(2, CR3, 3), (1, SO4, -2), (1, H2O, 0)]))
assert not _balance(([(1, CR2O7, -2), (3, SO2, 0), (14, HP, 1)], [(2, CR3, 3), (3, SO4, -2), (7, H2O, 0)]))
add("Oxidation number and balancing", A, "direct",
    "In acidic solution, dichromate ion oxidises sulphur dioxide to sulphate ion and is itself reduced to Cr³⁺. "
    "Which of the following is the correctly balanced ionic equation?",
    Opts("B", "Cr₂O₇²⁻ + 3SO₂ + 2H⁺ → 2Cr³⁺ + 3SO₄²⁻ + H₂O",
         ["Cr₂O₇²⁻ + 3SO₂ + 8H⁺ → 2Cr³⁺ + 3SO₄²⁻ + 4H₂O", "Cr₂O₇²⁻ + SO₂ + 2H⁺ → 2Cr³⁺ + SO₄²⁻ + H₂O",
          "Cr₂O₇²⁻ + 3SO₂ + 14H⁺ → 2Cr³⁺ + 3SO₄²⁻ + 7H₂O"]),
    "Balancing a redox equation by the oxidation number method",
    "Cr changes from +6 to +3 (each Cr₂O₇²⁻ gains 6 electrons) and S changes from +4 to +6 (each SO₂ loses 2). "
    "So 3SO₂ are needed per Cr₂O₇²⁻. Then balance charge with H⁺ and oxygen with H₂O.",
    ["Electrons: Cr₂O₇²⁻ gains 6; SO₂ loses 2 → 1 : 3", "Charge: left −2 + 2(+1) = 0; right 2(+3) + 3(−2) = 0",
     "O: left 7 + 6 = 13; right 12 + 1 = 13 → 1 H₂O, 2 H⁺"],
    why="The 14H⁺/7H₂O equation copies the Cr₂O₇²⁻ → Cr³⁺ half-reaction, and with 8H⁺/4H₂O the charge and "
        "oxygen do not balance. With only one SO₂ the electrons lost (2) do not equal those gained (6).",
    ncert=f"{REF7R}, balancing of redox reactions", seconds=80)

# ==================================================================== 8. Chemical Kinetics
topic("Chemical Kinetics")
REF8 = f"{C12}, 'Chemical Kinetics'"

ea_b = 80 - (-30)
assert ea_b == 110
add("Arrhenius equation and activation energy", B, "numerical",
    "For an exothermic elementary reaction, the activation energy of the forward reaction is 80 kJ mol⁻¹ and "
    "ΔH = −30 kJ mol⁻¹. The activation energy of the backward reaction is:",
    Opts("C", "110 kJ mol⁻¹", ["50 kJ mol⁻¹", "30 kJ mol⁻¹", "80 kJ mol⁻¹"]),
    "Energy profile of a reaction",
    "Both reactions pass over the same activated complex. For an exothermic reaction the products lie |ΔH| "
    "below the reactants, so the barrier from the product side is higher: Ea(backward) = Ea(forward) − ΔH.",
    ["Ea(b) = Ea(f) − ΔH = 80 − (−30) = 110 kJ mol⁻¹"],
    why="50 kJ mol⁻¹ subtracts |ΔH| instead of adding it. 30 kJ mol⁻¹ is |ΔH| and 80 kJ mol⁻¹ is the forward "
        "barrier.",
    ncert=f"{REF8}, temperature dependence of the rate of a reaction (energy diagram)", seconds=30, checked=True)

add("Rate law and order", B, "direct",
    "The decomposition 2HI(g) → H₂(g) + I₂(g), taking place as a single elementary step, has a molecularity of:",
    Opts("B", "2 (bimolecular)", ["1 (unimolecular)", "3 (termolecular)", "Zero"]),
    "Molecularity of an elementary reaction",
    "Molecularity is the number of reacting species that must collide simultaneously in an elementary step. "
    "Here two HI molecules collide, so the reaction is bimolecular.",
    ["Two HI molecules collide → molecularity 2"],
    why="Molecularity counts the colliding reactant molecules (two HI), not the number of product molecules, and "
        "it is never zero.",
    ncert=f"{REF8}, molecularity of a reaction", seconds=20)

add("Rate law and order", B, "statement_pair",
    sp("The unit of the rate of a reaction depends on the order of the reaction.",
       "The rate constant of a reaction equals its rate when the concentration of each reactant is unity."),
    SP_, "Rate and rate constant",
    "Rate is always a change of concentration per unit time (e.g. mol L⁻¹ s⁻¹), whatever the order; it is the "
    "unit of the rate constant that depends on the order. Statement I is false. Putting every concentration "
    "equal to 1 in the rate law gives rate = k, which is why k is also called the specific reaction rate. "
    "Statement II is true.",
    ["Rate: always mol L⁻¹ s⁻¹ (I false)", "Rate = k[A]ˣ[B]ʸ with [A] = [B] = 1 → rate = k (II true)"],
    answer="D", ncert=f"{REF8}, rate expression and rate constant", seconds=30)

assert 2 * 10 == 20  # zero order: completion time = [R]0/k = 2 t1/2
add("Zero and first order reactions", I, "numerical",
    "The concentration of the reactant of a zero-order reaction falls to half its initial value in 10 minutes. "
    "The time taken for the reaction to go to completion is:",
    Opts("A", "20 min", ["Infinite", "40 min", "15 min"]),
    "Completion time of a zero-order reaction",
    "For a zero-order reaction [R] = [R]₀ − kt, so the concentration falls linearly. Half is used in t½ = "
    "[R]₀/2k and all of it in [R]₀/k = 2t½.",
    ["t½ = [R]₀/2k = 10 min", "Completion: [R] = 0 → t = [R]₀/k = 2 × 10 = 20 min"],
    why="'Infinite' is true for a first-order reaction, whose concentration falls exponentially. 40 min and 15 min "
        "do not follow from the linear fall.",
    ncert=f"{REF8}, zero order reactions", seconds=35, checked=True)

ratio_99_90 = math.log10(100) / math.log10(10)
assert ratio_99_90 == 2
add("Half-life", I, "numerical",
    "For a first-order reaction, the ratio of the time required for 99% completion to the time required for 90% "
    "completion is:",
    Opts("D", "2", ["1.1", "10", "0.5"]),
    "Integrated rate equation of a first-order reaction",
    "t = (2.303/k) log([R]₀/[R]). After 99% completion [R]₀/[R] = 100; after 90% completion it is 10.",
    ["t₉₉ = (2.303/k) log 100 = (2.303/k) × 2", "t₉₀ = (2.303/k) log 10 = (2.303/k) × 1", "t₉₉ : t₉₀ = 2"],
    why="1.1 is 99/90, which treats the reaction as zero order. 10 compares the concentration ratios instead of "
        "their logarithms. 0.5 inverts the ratio.",
    ncert=f"{REF8}, first order reactions", seconds=40, checked=True)

add("Rate law and order", I, "assertion_reason",
    ar("Elementary reactions of molecularity three are very rare and slow.",
       "The probability that three molecules collide at the same time is very low."),
    AR_, "Termolecular reactions",
    "A termolecular step needs three particles to meet simultaneously, which happens far less often than a "
    "two-body collision. Hence reactions of molecularity three are rare and slow, and molecularity greater "
    "than three is not observed. R explains A.",
    ["Three-body collisions: low probability", "→ termolecular steps rare and slow"],
    answer="A", ncert=f"{REF8}, molecularity of a reaction", seconds=30)

add("Rate law and order", I, "match_list",
    lists("Match List-I (term) with List-II (its meaning).",
          ["Rate-determining step", "Molecularity", "Order of a reaction", "Pseudo first-order reaction"],
          ["Number of reacting species that collide simultaneously in an elementary step",
           "Reaction whose observed order is lowered because one reactant is present in large excess",
           "Slowest step in the mechanism of a complex reaction",
           "Sum of the powers of the concentration terms in the experimentally found rate law"]),
    match("B", M("III I IV II"), [M("I III IV II"), M("III IV I II"), M("III I II IV")]),
    "Terms in chemical kinetics",
    "The slowest step controls the overall rate. Molecularity is defined for an elementary step; order is "
    "found from the experimental rate law. When one reactant (e.g. water in hydrolysis) is in large excess its "
    "concentration hardly changes and the reaction appears first order.",
    ["A → III", "B → I", "C → IV", "D → II"],
    why="The other codes confuse molecularity with order, or pseudo first-order reactions with the "
        "rate-determining step.",
    ncert=f"{REF8}, order and molecularity; pseudo first order reaction", seconds=40)

rate = {(0.1, 0.1): 6.0e-3, (0.1, 0.2): 1.2e-2, (0.2, 0.1): 2.4e-2}
y_ord = round(math.log2(rate[(0.1, 0.2)] / rate[(0.1, 0.1)]))
x_ord = round(math.log2(rate[(0.2, 0.1)] / rate[(0.1, 0.1)]))
k_val = rate[(0.1, 0.1)] / (0.1 ** x_ord * 0.1 ** y_ord)
assert (x_ord, y_ord) == (2, 1) and close(k_val, 6.0)
assert close(6.0e-3 / (0.1 * 0.1), 0.6) and close(6.0e-3 / (0.1 ** 2 * 0.1 ** 2), 60)
add("Rate law and order", A, "numerical",
    "For the reaction A + B → products, the following initial rates were measured at the same temperature:\n\n"
    "Experiment 1: [A] = 0.1 M, [B] = 0.1 M, rate = 6.0 × 10⁻³ mol L⁻¹ s⁻¹\n"
    "Experiment 2: [A] = 0.1 M, [B] = 0.2 M, rate = 1.2 × 10⁻² mol L⁻¹ s⁻¹\n"
    "Experiment 3: [A] = 0.2 M, [B] = 0.1 M, rate = 2.4 × 10⁻² mol L⁻¹ s⁻¹\n\n"
    "The rate constant of the reaction is:",
    Opts("C", "6.0 L² mol⁻² s⁻¹", ["0.6 L mol⁻¹ s⁻¹", "60 L³ mol⁻³ s⁻¹", "6.0 L mol⁻¹ s⁻¹"]),
    "Rate constant from initial-rate data",
    "Find the order in each reactant by changing one concentration at a time, write the rate law, and then "
    "substitute one experiment to get k with the unit that matches the overall order.",
    ["Exp 1 → 2: [B] doubled, rate doubled → first order in B",
     "Exp 1 → 3: [A] doubled, rate × 4 → second order in A", "Rate = k[A]²[B] (overall order 3)",
     "k = 6.0 × 10⁻³ / (0.1² × 0.1) = 6.0 L² mol⁻² s⁻¹"],
    why="0.6 L mol⁻¹ s⁻¹ assumes first order in both. 60 L³ mol⁻³ s⁻¹ assumes second order in both. 6.0 L mol⁻¹ "
        "s⁻¹ has the right number but the unit of a second-order rate constant.",
    ncert=f"{REF8}, rate law: initial rate method", seconds=90, checked=True)

add("Arrhenius equation and activation energy", A, "multi_statement",
    ms("Which of the following statements about the effect of temperature and collision theory are correct?",
       ["In collision theory the rate is written as Rate = P Z_AB e^(−Ea/RT), where Z_AB is the collision "
        "frequency.",
        "The probability (steric) factor P accounts for the fact that only collisions with proper orientation "
        "are effective.",
        "All reactions have the same activation energy.",
        "On raising the temperature, the fraction of molecules with energy equal to or greater than Ea "
        "increases.",
        "On raising the temperature, the peak of the Maxwell–Boltzmann energy distribution curve shifts to "
        "lower energy."]),
    multi("A", {"a": True, "b": True, "c": False, "d": True, "e": False},
          ["(a), (b), (d) and (e) only", "(b), (c) and (d) only", "(a), (d) and (e) only"]),
    "Collision theory and the Maxwell–Boltzmann distribution",
    "Collision theory gives Rate = P Z_AB e^(−Ea/RT): Z_AB counts collisions, e^(−Ea/RT) the fraction with "
    "enough energy and P the fraction properly oriented. Ea differs from reaction to reaction. At a higher "
    "temperature the distribution curve broadens and its maximum moves to higher energy, so more molecules "
    "exceed Ea.",
    ["(a) True", "(b) True", "(c) False", "(d) True", "(e) False: the peak shifts to higher energy"],
    why="Options containing (c) or (e) are wrong.",
    ncert=f"{REF8}, collision theory of chemical reactions; temperature dependence of rate", seconds=55)

add("Arrhenius equation and activation energy", A, "direct",
    "According to the Arrhenius equation, k = A e^(−Ea/RT), as the temperature becomes very large (T → ∞) "
    "the rate constant k approaches:",
    Opts("D", "A, the pre-exponential factor", ["Zero", "Infinity", "Ea/R"]),
    "Limiting behaviour of the Arrhenius equation",
    "As T → ∞, Ea/RT → 0, so e^(−Ea/RT) → e⁰ = 1 and k → A. Physically, every collision would then have enough "
    "energy, so the rate constant is limited by the collision frequency factor A.",
    ["Ea/RT → 0", "e^(−Ea/RT) → 1", "k → A"],
    why="k tends to zero as T → 0, not as T → ∞. k cannot exceed A, so it does not become infinite. Ea/R has "
        "the unit of temperature, not of a rate constant.",
    ncert=f"{REF8}, temperature dependence of the rate of a reaction", seconds=35)

# ==================================================================== 9. Classification of Elements and Periodicity
topic("Classification of Elements and Periodicity in Properties")
REF9 = f"{C11}, 'Classification of Elements and Periodicity in Properties'"

add("Modern periodic table", B, "direct",
    "Whose work showed that the frequencies of the characteristic X-rays emitted by the elements vary "
    "regularly with atomic number, which led to the modern periodic law?",
    Opts("B", "Henry Moseley", ["Dmitri Mendeleev", "Lothar Meyer", "John Newlands"]),
    "Origin of the modern periodic law",
    "Moseley found that a plot of √ν of the characteristic X-rays against atomic number is a straight line, but "
    "not against atomic mass. This showed that atomic number is the more fundamental property, and Mendeleev's "
    "periodic law was modified accordingly.",
    ["√ν ∝ Z (Moseley)", "Properties are periodic functions of atomic number"],
    why="Mendeleev and Lothar Meyer arranged elements by atomic mass; Newlands proposed the law of octaves.",
    ncert=f"{REF9}, modern periodic law and the present form of the periodic table", seconds=20)

add("Modern periodic table", B, "direct",
    "Mendeleev left gaps in his periodic table and predicted the properties of the elements that would fill "
    "them. The element he called eka-silicon was later identified as:",
    Opts("C", "Germanium", ["Gallium", "Scandium", "Tin"]),
    "Mendeleev's predictions",
    "Mendeleev predicted eka-aluminium and eka-silicon. When gallium and germanium were discovered, their "
    "properties closely matched his predictions for eka-aluminium and eka-silicon respectively.",
    ["Eka-aluminium → gallium", "Eka-silicon → germanium"],
    why="Gallium is eka-aluminium. Scandium and tin are not the element predicted below silicon.",
    ncert=f"{REF9}, Mendeleev's periodic law", seconds=20)

add("Valence and reactivity", B, "assertion_reason",
    ar("Elements in the same group of the periodic table show similar chemical properties.",
       "Elements of the same group have similar outer (valence-shell) electronic configurations."),
    AR_, "Periodicity and electronic configuration",
    "Chemical properties are decided mainly by the valence electrons. Elements of a group have the same number "
    "and arrangement of outer electrons (e.g. ns¹ for group 1), so they show similar chemical behaviour. R "
    "explains A.",
    ["Same group → same type of valence configuration", "→ similar chemical properties"],
    answer="A", ncert=f"{REF9}, electronic configurations of elements and the periodic table", seconds=25)

e_ion = 2.3 / 23 * 496
assert close(e_ion, 49.6) and close(2.3 * 496, 1140.8)
add("Ionisation and electron gain enthalpy", I, "numerical",
    "The first ionisation enthalpy of sodium is 496 kJ mol⁻¹. The energy needed to convert 2.3 g of gaseous "
    "sodium atoms completely into gaseous Na⁺ ions is (Na = 23):",
    Opts("D", "49.6 kJ", ["496 kJ", "1140.8 kJ", "4.96 kJ"]),
    "Ionisation enthalpy per mole",
    "Ionisation enthalpy is quoted per mole of gaseous atoms, so the energy needed is the amount of sodium (in "
    "mol) multiplied by ΔᵢH₁.",
    ["n(Na) = 2.3 / 23 = 0.1 mol", "Energy = 0.1 × 496 = 49.6 kJ"],
    why="496 kJ is for a whole mole. 1140.8 kJ multiplies the mass by the molar ionisation enthalpy. 4.96 kJ is "
        "for 0.01 mol.",
    ncert=f"{REF9}, ionization enthalpy", seconds=30, checked=True)

add("Atomic and ionic radii", I, "statement_pair",
    sp("The size of a non-metal atom is usually expressed by its covalent radius, and that of a metal atom by "
       "its metallic radius.",
       "The covalent radius of an element is half the distance between the nuclei of two bonded atoms of "
       "different elements."),
    SP_, "Covalent and metallic radii",
    "NCERT uses the covalent radius for non-metals and the metallic radius for metals, so Statement I is true. "
    "The covalent radius is half the internuclear distance between two atoms of the same element joined by a "
    "single covalent bond (e.g. half the Cl–Cl distance), not between atoms of different elements. Statement "
    "II is false.",
    ["Non-metals: covalent radius; metals: metallic radius (I true)",
     "Covalent radius: two atoms of the same element (II false)"],
    answer="C", ncert=f"{REF9}, atomic radius", seconds=30)

add("Modern periodic table", I, "match_list",
    lists("Match List-I (block of the periodic table) with List-II (general outer electronic configuration).",
          ["s-block", "p-block", "d-block", "f-block"],
          ["ns² np¹⁻⁶ (except He)", "ns¹⁻²", "(n−2)f¹⁻¹⁴ (n−1)d⁰⁻¹ ns²", "(n−1)d¹⁻¹⁰ ns⁰⁻²"]),
    match("A", M("II I IV III"), [M("I II IV III"), M("II I III IV"), M("II IV I III")]),
    "Electronic configurations of the blocks",
    "The block is named after the subshell that receives the last electron: s for groups 1–2, p for groups "
    "13–18, d for the transition elements and f for the lanthanoids and actinoids.",
    ["s → ns¹⁻² (II)", "p → ns² np¹⁻⁶ (I)", "d → (n−1)d¹⁻¹⁰ ns⁰⁻² (IV)", "f → (n−2)f¹⁻¹⁴ (n−1)d⁰⁻¹ ns² (III)"],
    why="The other codes swap the s- and p-block or the d- and f-block configurations.",
    ncert=f"{REF9}, electronic configurations and types of elements: s-, p-, d-, f-blocks", seconds=35)

add("Atomic and ionic radii", I, "multi_statement",
    ms("Which of the following comparisons are correct?",
       ["Atomic radius: Na > Mg", "Electronegativity: C > Si", "Ionic radius: K⁺ > Na⁺", "Atomic radius: Si > Al",
        "First ionisation enthalpy: Mg > Na"]),
    multi("B", {"a": True, "b": True, "c": True, "d": False, "e": True},
          ["(a), (b) and (c) only", "(a), (c), (d) and (e) only", "(b), (d) and (e) only"]),
    "Trends across a period and down a group",
    "Across a period the nuclear charge increases, so atomic radius decreases and ionisation enthalpy "
    "increases (Na > Mg > Al > Si in size; Mg > Na in ΔᵢH₁). Down a group, size increases and electronegativity "
    "decreases (K⁺ > Na⁺; C > Si).",
    ["(a) True", "(b) True: C 2.5, Si 1.8", "(c) True: one more shell", "(d) False: Al > Si",
     "(e) True: 738 vs 496 kJ mol⁻¹"],
    why="Any option containing (d) is wrong, and (a), (b), (c) only leaves out the true (e).",
    ncert=f"{REF9}, periodic trends in physical properties", seconds=45)

add("Valence and reactivity", A, "direct",
    "Which of the following correctly shows the increasing order of acidic character of the oxides of "
    "third-period elements?",
    Opts("C", "MgO < Al₂O₃ < SiO₂ < P₄O₁₀",
         ["Al₂O₃ < MgO < SiO₂ < P₄O₁₀", "MgO < SiO₂ < Al₂O₃ < P₄O₁₀", "P₄O₁₀ < SiO₂ < Al₂O₃ < MgO"]),
    "Acid–base character of oxides across a period",
    "Across a period, metallic character decreases and non-metallic character increases. Oxides change from "
    "basic (MgO) through amphoteric (Al₂O₃) to acidic (SiO₂, P₄O₁₀), and acidity increases with the "
    "non-metallic character of the element.",
    ["MgO: basic", "Al₂O₃: amphoteric", "SiO₂: acidic", "P₄O₁₀: more strongly acidic"],
    why="The other orders place amphoteric Al₂O₃ below basic MgO or above acidic SiO₂, or reverse the whole "
        "trend.",
    ncert=f"{REF9}, periodic trends in chemical properties", seconds=40)

add("Modern periodic table", A, "statement_pair",
    sp("In the d-block elements, the last electron enters the outermost ns orbital.",
       "The lanthanoids are placed in the seventh period of the periodic table."),
    SP_, "d- and f-block elements in the periodic table",
    "In the d-block the differentiating electron enters the (n−1)d subshell, the penultimate shell; Statement I "
    "is false. The lanthanoids (Ce to Lu) follow lanthanum in the sixth period; the actinoids belong to the "
    "seventh. Statement II is false.",
    ["d-block: last electron in (n−1)d (I false)", "Lanthanoids: period 6; actinoids: period 7 (II false)"],
    answer="B", ncert=f"{REF9}, the d-block and f-block elements", seconds=35)

# ==================================================================== 10. p-Block Elements
topic("p-Block Elements")
REF10A = "Class 11 Chemistry (pre-2023 edition), 'The p-Block Elements'"
REF10B = f"{C12}, 'The p-Block Elements'"

add("Group 13 and 14 trends", B, "direct",
    "Among the oxides of the group 13 elements in the +3 oxidation state, the acidic one is that of:",
    Opts("B", "Boron (B₂O₃)", ["Aluminium (Al₂O₃)", "Indium (In₂O₃)", "Thallium (Tl₂O₃)"]),
    "Trend in the nature of oxides down group 13",
    "Metallic character increases down group 13. Boron, a non-metal, forms an acidic oxide; the oxides of "
    "aluminium and gallium are amphoteric, and those of indium and thallium are basic.",
    ["B₂O₃: acidic", "Al₂O₃, Ga₂O₃: amphoteric", "In₂O₃, Tl₂O₃: basic"],
    why="Al₂O₃ is amphoteric, and the oxides of indium and thallium are basic.",
    ncert=f"{REF10A}, group 13: chemical properties (reactivity towards air)", seconds=25)

add("Group 13 and 14 trends", B, "statement_pair",
    sp("Down group 13, the electronegativity first decreases from boron to aluminium and then increases "
       "marginally.",
       "The density of the group 13 elements decreases from boron to thallium."),
    SP_, "Physical trends in group 13",
    "NCERT notes that electronegativity falls from B to Al and then rises slightly (because of differences in "
    "atomic size caused by poorly shielding d and f electrons), so Statement I is true. Density increases down "
    "the group from boron to thallium, so Statement II is false.",
    ["EN: B > Al, then slight increase Ga → Tl (I true)", "Density increases down the group (II false)"],
    answer="C", ncert=f"{REF10A}, group 13: electronegativity and physical properties", seconds=30)

add("Anomalous first element", B, "assertion_reason",
    ar("Carbon is more electronegative than the other elements of group 14.",
       "Carbon has the largest atomic radius in group 14."),
    AR_, "Anomalous behaviour of carbon",
    "Carbon has an electronegativity of about 2.5, clearly higher than the other members of the group, whose "
    "values are close to one another; A is true. Atomic radius increases down the group, so carbon has the "
    "smallest radius; its small size is what makes it more electronegative. R is false.",
    ["EN: C ≈ 2.5, others ≈ 1.8 (A true)", "Radius increases C → Pb; carbon is the smallest (R false)"],
    answer="C", ncert=f"{REF10A}, group 14: electronegativity; anomalous behaviour of carbon", seconds=30)

add("Group 17 and 18 trends", I, "direct",
    "Which of the following reactions does NOT take place in aqueous solution?",
    Opts("D", "I₂ + 2Cl⁻ → 2I⁻ + Cl₂",
         ["Cl₂ + 2Br⁻ → 2Cl⁻ + Br₂", "Br₂ + 2I⁻ → 2Br⁻ + I₂", "F₂ + 2Cl⁻ → 2F⁻ + Cl₂"]),
    "Relative oxidising power of the halogens",
    "Oxidising power decreases from F₂ to I₂. A halogen therefore oxidises the halide ions of the halogens "
    "below it in the group, but not those above it.",
    ["F₂ > Cl₂ > Br₂ > I₂ as oxidising agents", "Cl₂ oxidises Br⁻; Br₂ oxidises I⁻; F₂ oxidises Cl⁻",
     "I₂ cannot oxidise Cl⁻"],
    why="Each of the other three reactions has a stronger oxidising halogen displacing a weaker one from its "
        "halide.",
    ncert=f"{REF10B}, group 17: oxidising power of halogens", seconds=30)

add("Group 15 and 16 trends", I, "direct",
    "Down group 15, which of the following properties increases from nitrogen up to arsenic and then decreases "
    "up to bismuth?",
    Opts("A", "Melting point", ["Boiling point", "Covalent radius", "First ionisation enthalpy"]),
    "Physical trends in group 15",
    "NCERT: the boiling points, in general, increase from top to bottom in group 15, but the melting point "
    "increases up to arsenic and then decreases up to bismuth.",
    ["Boiling point: increases N → Bi", "Melting point: increases up to As, then decreases",
     "Covalent radius: increases; ionisation enthalpy: decreases"],
    why="Boiling point and covalent radius increase steadily down the group, and ionisation enthalpy decreases "
        "steadily.",
    ncert=f"{REF10B}, group 15: physical properties", seconds=30)

add("Group 15 and 16 trends", I, "statement_pair",
    sp("In group 15, the trihalides are more covalent than the pentahalides.",
       "Nitrogen shows oxidation states ranging from −3 to +5 in its compounds."),
    SP_, "Oxidation states and covalent character in group 15",
    "An element in a higher oxidation state has a greater polarising power, so the pentahalides are more "
    "covalent than the trihalides; Statement I is false. Nitrogen shows all oxidation states from −3 (as in "
    "NH₃) to +5 (as in N₂O₅); Statement II is true.",
    ["Higher oxidation state → more covalent → EX₅ more covalent than EX₃ (I false)",
     "N: −3 to +5 (II true)"],
    answer="D", ncert=f"{REF10B}, group 15: oxidation states and chemical properties", seconds=35)

add("Group 13 and 14 trends", I, "match_list",
    lists("Match List-I (element) with List-II (ground-state electronic configuration).",
          ["Gallium (Z = 31)", "Antimony (Z = 51)", "Selenium (Z = 34)", "Thallium (Z = 81)"],
          ["[Kr] 4d¹⁰ 5s² 5p³", "[Xe] 4f¹⁴ 5d¹⁰ 6s² 6p¹", "[Ar] 3d¹⁰ 4s² 4p¹", "[Ar] 3d¹⁰ 4s² 4p⁴"]),
    match("B", M("III I IV II"), [M("IV I III II"), M("III II IV I"), M("I III IV II")]),
    "Electronic configurations of p-block elements",
    "The group gives the number of p electrons (group 13 → p¹, 15 → p³, 16 → p⁴) and the period gives n.",
    ["Ga: group 13, period 4 → [Ar] 3d¹⁰ 4s² 4p¹ (III)", "Sb: group 15, period 5 → [Kr] 4d¹⁰ 5s² 5p³ (I)",
     "Se: group 16, period 4 → [Ar] 3d¹⁰ 4s² 4p⁴ (IV)", "Tl: group 13, period 6 → [Xe] 4f¹⁴ 5d¹⁰ 6s² 6p¹ (II)"],
    why="The other codes swap Ga and Se (both period 4) or Sb and Tl.",
    ncert=f"{REF10A} and {REF10B}, electronic configuration of groups 13, 15 and 16", seconds=40)

add("Group 15 and 16 trends", I, "multi_statement",
    ms("Which of the following statements about trends in groups 14 and 15 are correct?",
       ["The ionisation enthalpies of the group 15 elements are much greater than those of the group 14 "
        "elements in the corresponding periods.",
        "In group 14, the covalent radius increases considerably from carbon to silicon, and only slightly from "
        "silicon to lead.",
        "The boiling points of the group 15 elements decrease from nitrogen to bismuth.",
        "All the group 15 elements are non-metals.",
        "Electronegativity decreases down group 15, but the differences among the heavier elements are small."]),
    multi("C", {"a": True, "b": True, "c": False, "d": False, "e": True},
          ["(a), (b), (c) and (e) only", "(b), (d) and (e) only", "(a), (c) and (e) only"]),
    "General trends in groups 14 and 15",
    "Group 15 elements have extra-stable half-filled p³ configurations and smaller size than their group 14 "
    "neighbours, so their ionisation enthalpies are much higher. In group 14 the radius jumps from C to Si and "
    "then increases only a little because of poorly shielding d and f electrons. Boiling points increase down "
    "group 15, which runs from non-metals (N, P) through metalloids (As, Sb) to a metal (Bi). Electronegativity "
    "decreases down the group, less sharply among the heavier members.",
    ["(a) True", "(b) True", "(c) False: boiling points increase", "(d) False: Bi is a metal", "(e) True"],
    why="Options containing (c) or (d) are wrong.",
    ncert=f"{REF10A} and {REF10B}, groups 14 and 15: atomic and physical properties", seconds=55)

add("Group 13 and 14 trends", A, "statement_pair",
    sp("The trihalides of group 13 elements behave as Lewis acids, and this tendency decreases down the group.",
       "The first ionisation enthalpy of thallium is higher than that of indium."),
    SP_, "Lewis acidity and ionisation enthalpy in group 13",
    "With only six electrons around the central atom, the group 13 trihalides accept electron pairs; NCERT notes "
    "that this Lewis acid character decreases with increasing size down the group. Statement I is true. "
    "ΔᵢH₁ is about 558 kJ mol⁻¹ for In and 589 kJ mol⁻¹ for Tl: the poor shielding by the 4f and 5d electrons "
    "raises the effective nuclear charge in Tl. Statement II is true.",
    ["EX₃: electron deficient → Lewis acids; acidity falls down the group (I true)",
     "ΔᵢH₁: In 558 < Tl 589 kJ mol⁻¹ (II true)"],
    answer="A", ncert=f"{REF10A}, group 13: ionisation enthalpy and chemical properties", seconds=40)

add("Anomalous first element", A, "assertion_reason",
    ar("The ionisation enthalpy, electronegativity and electrode potential of fluorine are all higher than "
       "would be expected from the trends shown by the other halogens.",
       "The fluorine atom is very small, being the first member of group 17."),
    AR_, "Anomalous behaviour of fluorine",
    "NCERT attributes the anomalous behaviour of fluorine mainly to its small size (together with its highest "
    "electronegativity, low F–F bond dissociation enthalpy and lack of d orbitals). Because its valence "
    "electrons are very close to the nucleus, fluorine's ionisation enthalpy, electronegativity and electrode "
    "potential are higher than the trend predicts. R explains A.",
    ["Very small atom → electrons strongly held", "→ ΔᵢH, EN and E° above the trend"],
    answer="A", ncert=f"{REF10B}, group 17: anomalous behaviour of fluorine", seconds=40)

add("Group 13 and 14 trends", A, "direct",
    "Which of the following sets contains only amphoteric oxides?",
    Opts("D", "SnO, SnO₂, PbO, PbO₂",
         ["CO, SnO, PbO, GeO", "SiO₂, GeO₂, SnO₂, PbO₂", "GeO, SnO, SnO₂, CO₂"]),
    "Acid–base character of group 14 oxides",
    "Among the dioxides, CO₂, SiO₂ and GeO₂ are acidic while SnO₂ and PbO₂ are amphoteric. Among the "
    "monoxides, CO is neutral, GeO is distinctly acidic, and SnO and PbO are amphoteric.",
    ["Amphoteric: SnO, PbO, SnO₂, PbO₂", "Acidic: CO₂, SiO₂, GeO₂, GeO", "Neutral: CO"],
    why="Each other set contains at least one acidic oxide (GeO, SiO₂, GeO₂, CO₂) or the neutral oxide CO.",
    ncert=f"{REF10A}, group 14: chemical properties (reactivity towards oxygen)", seconds=40)


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
    doc = {"schema_version": "1.0", "batch_id": "BATCH_005", "created_at": TODAY,
           "notes": "Package CHE_005_p1: 128 original Chemistry questions (physical chemistry, periodicity and "
                    "p-block). Numerical answers re-derived in tools/batch_005/CHE_005_p1.py.",
           "stimuli": [], "questions": QUESTIONS}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {OUT}: {n} questions; difficulty {dict(Counter(q['difficulty'] for q in QUESTIONS))}; "
          f"formats {dict(fmts)}; keys {dict(sorted(KEYS.items()))}")
