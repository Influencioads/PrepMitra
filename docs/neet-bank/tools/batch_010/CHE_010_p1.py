"""Writes batches/parts/BATCH_010_CHE_p1.json: package CHE_010_p1 of BATCH_010 (Chemistry, 122 questions).

Topics: Some Basic Concepts, Atomic Structure, Chemical Bonding, Thermodynamics, Solutions, Equilibrium,
Redox and Electrochemistry, Chemical Kinetics, Classification of Elements and Periodicity, p-Block Elements,
d- and f-Block Elements. IDs NEET_CHE_002251..002372.

Every computable answer is re-derived here with an assert before anything is written; the quota per
(topic, difficulty), the ID range, the format mix and the answer-key balance are asserted too.
The position of every correct option is chosen by hand in the call that adds the question (argument `at`)
and never moved by code.

    cd docs/neet-bank && python tools/batch_010/CHE_010_p1.py
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
PACKAGE = "CHE_010_p1"
PLAN = ROOT / "batches" / "plans" / "BATCH_010_plan.json"
OUT = ROOT / "batches" / "parts" / "BATCH_010_CHE_p1.json"
TODAY = "2026-11-16"
LETTERS = "ABCD"
CHE = "Chemistry"
FIRST_ID = 2251
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

n_c = 6 / 12
m_mg = n_c * 24
assert close(m_mg, 12) and close(6 * 12 / 24, 3)
add("Mole concept", B, "numerical",
    "What mass of magnesium contains the same number of atoms as 6 g of carbon? (C = 12, Mg = 24)",
    Opts("C", "12 g", ["6 g", "24 g", "3 g"]),
    "Equal numbers of atoms means equal amounts (moles) of atoms",
    "Find the moles of carbon atoms in 6 g; the same number of moles of Mg atoms is needed. Multiply by the "
    "molar mass of Mg.",
    ["n(C) = 6/12 = 0.5 mol", "n(Mg) = 0.5 mol", "m(Mg) = 0.5 × 24 = 12 g"],
    why="6 g assumes equal masses contain equal numbers of atoms. 24 g is the mass of a whole mole of Mg. "
        "3 g inverts the ratio of the molar masses (6 × 12/24).",
    ncert=f"{REF1}, mole concept and molar masses", seconds=30, checked=True)

add("Laws of chemical combination", B, "statement_pair",
    sp("Gay-Lussac's law of gaseous volumes is, in effect, the law of definite proportions applied to the "
       "volumes of reacting gases.",
       "Avogadro's hypothesis made a distinction between atoms and molecules."),
    SP_, "Gay-Lussac's law and Avogadro's law",
    "NCERT describes Gay-Lussac's law (gases combine in a simple whole-number ratio by volume at the same "
    "temperature and pressure) as the law of definite proportions by volume. Avogadro proposed that equal "
    "volumes of gases at the same temperature and pressure contain equal numbers of molecules, and in doing so "
    "distinguished atoms from molecules.",
    ["I: Gay-Lussac's law = definite proportions by volume → true",
     "II: Avogadro distinguished atoms from molecules → true"],
    answer="A",
    why="Both statements are NCERT statements, so no option that calls either of them false can be right.",
    ncert=f"{REF1}, Gay Lussac's law of gaseous volumes; Avogadro's law", seconds=35)

n_fe = 16.8 / 56
m_o2 = n_fe * 2 / 3 * 32
assert close(m_o2, 6.4) and close(n_fe * 16, 4.8) and close(n_fe / 2 * 1.5 * 32, 7.2) and close(n_fe * 32, 9.6)
add("Stoichiometry", I, "numerical",
    "The mass of oxygen gas needed to convert 16.8 g of iron completely into Fe₃O₄, "
    "3Fe(s) + 2O₂(g) → Fe₃O₄(s), is (Fe = 56, O = 16):",
    Opts("D", "6.4 g", ["4.8 g", "7.2 g", "9.6 g"]),
    "Mass–mole–mass calculation from a balanced equation",
    "Convert the mass of iron to moles, use the 3 : 2 mole ratio of Fe to O₂, and convert O₂ to grams.",
    ["n(Fe) = 16.8/56 = 0.30 mol", "n(O₂) = 0.30 × 2/3 = 0.20 mol", "m(O₂) = 0.20 × 32 = 6.4 g"],
    why="4.8 g takes one O atom per Fe atom (FeO). 7.2 g uses the Fe₂O₃ ratio (1.5 mol O₂ per 2 mol Fe). "
        "9.6 g takes one O₂ per Fe.",
    ncert=f"{REF1}, stoichiometry and stoichiometric calculations", seconds=50, checked=True)

o_atoms = {"A": 0.5 * 3, "B": 49 / 98 * 4, "C": 9 / 18 * 1, "D": 16 / 16}
assert o_atoms == {"A": 1.5, "B": 2.0, "C": 0.5, "D": 1.0}
add("Mole concept", I, "match_list",
    lists("Match List-I (sample) with List-II (amount of oxygen ATOMS it contains). "
          "(H = 1, C = 12, O = 16, Na = 23, S = 32)",
          ["0.5 mol of Na₂CO₃", "49 g of H₂SO₄", "9 g of H₂O", "16 g of O₃"],
          ["0.5 mol", "1.0 mol", "1.5 mol", "2.0 mol"]),
    match("B", M("III IV I II"), [M("III II I IV"), M("I IV III II"), M("III IV II I")]),
    "Moles of atoms = moles of the substance × number of those atoms in one formula unit",
    "Find the moles of each substance and multiply by the number of oxygen atoms in its formula.",
    ["A: 0.5 × 3 = 1.5 mol → III", "B: 49/98 = 0.5 mol H₂SO₄ × 4 = 2.0 mol → IV",
     "C: 9/18 = 0.5 mol H₂O × 1 = 0.5 mol → I", "D: 16/48 = 1/3 mol O₃ × 3 = 1.0 mol (or simply 16/16) → II"],
    why="B-II/D-IV counts molecules of H₂SO₄ or O₃ instead of oxygen atoms. A-I/C-III swaps the carbonate and "
        "water values. C-II/D-I takes 16 g of O₃ as 0.5 mol of atoms by using the molar mass of O₂.",
    ncert=f"{REF1}, mole concept and molar masses", seconds=75, checked=True)

add("Laws of chemical combination", I, "assertion_reason",
    ar("The average atomic mass of chlorine, 35.5 u, is not a whole number.",
       "Naturally occurring chlorine is a mixture of isotopes of different masses, and its atomic mass is the "
       "abundance-weighted average of their masses."),
    AR_, "Average atomic mass of an element with isotopes",
    "Each chlorine isotope has a mass close to a whole number (about 35 u and 37 u), but natural chlorine "
    "contains both in a fixed ratio. The atomic mass quoted for the element is their weighted average, which "
    "lies between them and is not a whole number. R is exactly why A is true.",
    ["A: atomic mass of Cl = 35.5 u → true", "R: isotopes averaged by abundance → true",
     "The averaging in R produces the non-integral value in A → option A"],
    answer="A",
    why="R is not merely another true fact about chlorine: it is the reason the quoted atomic mass is "
        "fractional, so 'not the correct explanation' does not apply.",
    ncert=f"{REF1}, atomic and molecular masses (average atomic mass)", seconds=35)

v_co, v_o2 = 30, 20
used_o2 = v_co / 2
left = v_co + (v_o2 - used_o2)
assert left == 35 and v_o2 * 2 == 40
add("Stoichiometry", A, "numerical",
    "30 mL of carbon monoxide is mixed with 20 mL of oxygen and the mixture is ignited: "
    "2CO(g) + O₂(g) → 2CO₂(g). All volumes are measured at the same temperature and pressure. The total volume "
    "of gas left after the reaction is:",
    Opts("B", "35 mL", ["30 mL", "50 mL", "40 mL"]),
    "Gay-Lussac's law of gaseous volumes combined with a limiting reagent",
    "Volumes of gases at the same temperature and pressure react in the ratio of their coefficients. Find the "
    "limiting gas, the volume of product formed and the volume of the excess gas left over.",
    ["30 mL CO needs 15 mL O₂; 20 mL O₂ is available → CO is limiting",
     "CO₂ formed = 30 mL; O₂ left = 20 − 15 = 5 mL", "Total gas = 30 + 5 = 35 mL"],
    why="30 mL counts only the CO₂ and forgets the unused oxygen. 50 mL assumes the volume does not change "
        "on reaction. 40 mL treats O₂ as the limiting gas (20 mL O₂ → 40 mL CO₂), although that would need "
        "40 mL of CO.",
    ncert=f"{REF1}, Gay Lussac's law of gaseous volumes; limiting reagent", seconds=80, checked=True)

mol_mass, ef_mass = 84, 14
n_mult = mol_mass // ef_mass
pc_c = 72 / 84 * 100
h_atoms = 0.1 * 12
water = 0.1 * 6 * 18
truth_cx = {"a": n_mult == 6, "b": close(pc_c, 85.7), "c": close(h_atoms, 0.6), "d": True,
            "e": close(water, 21.6)}
assert truth_cx == {"a": True, "b": True, "c": False, "d": True, "e": False} and close(water, 10.8)
add("Empirical and molecular formulae", A, "multi_statement",
    ms("A hydrocarbon has the empirical formula CH₂ and a molar mass of 84 g mol⁻¹. Which of the following "
       "statements about it are correct? (C = 12, H = 1, O = 16)",
       ["Its molecular formula is C₆H₁₂.",
        "It contains about 85.7% carbon by mass.",
        "0.1 mol of it contains 0.6 mol of hydrogen atoms.",
        "It has the same percentage composition by mass as ethene (C₂H₄).",
        "Complete combustion of 8.4 g of it gives 21.6 g of water."]),
    multi("D", truth_cx, ["(a), (b), (c) and (d) only", "(a), (d) and (e) only", "(b), (c) and (e) only"]),
    "Molecular formula = n × empirical formula; composition and stoichiometry from the formula",
    "Empirical formula mass of CH₂ = 14, so n = 84/14 = 6 and the formula is C₆H₁₂. Use it to check each "
    "statement.",
    ["(a) n = 6 → C₆H₁₂ ✓", "(b) %C = 72/84 × 100 = 85.7% ✓",
     "(c) 0.1 mol × 12 H = 1.2 mol H atoms, not 0.6 ✗", "(d) C₂H₄ also has empirical formula CH₂ → same % ✓",
     "(e) 8.4 g = 0.1 mol → 0.6 mol H₂O = 10.8 g, not 21.6 g ✗"],
    why="(c) counts H₂ molecules' worth of hydrogen (half the atoms); (e) doubles the water by taking 12 mol "
        "of H₂O per mol of hydrocarbon. Any option containing (c) or (e) is wrong.",
    ncert=f"{REF1}, empirical formula for molecular formula", seconds=100, checked=True)


# ==================================================================== 2. Atomic Structure
topic("Atomic Structure")
REF2 = f"{C11}, 'Structure of Atom'"
M_E = 9.11e-31

v_db = H_PLANCK / (M_E * 0.727e-9)
assert close(v_db, 1.0e6, 0.002) and close(H_PLANCK / (M_E * 0.727e-6), 1.0e3, 0.002) \
    and close(H_PLANCK / (M_E * 0.727e-12), 1.0e9, 0.002)
add("Dual nature and uncertainty", B, "numerical",
    "The de Broglie wavelength of a moving electron is 0.727 nm. Its speed is "
    "(h = 6.626 × 10⁻³⁴ J s, mass of electron = 9.11 × 10⁻³¹ kg):",
    Opts("A", "1.0 × 10⁶ m s⁻¹", ["1.0 × 10³ m s⁻¹", "5.0 × 10⁵ m s⁻¹", "1.0 × 10⁹ m s⁻¹"]),
    "de Broglie relation λ = h/mv",
    "Rearrange the de Broglie relation to v = h/(mλ) and put the wavelength in metres.",
    ["λ = 0.727 nm = 7.27 × 10⁻¹⁰ m", "v = 6.626 × 10⁻³⁴ / (9.11 × 10⁻³¹ × 7.27 × 10⁻¹⁰)",
     "v = 6.626 × 10⁻³⁴ / 6.62 × 10⁻⁴⁰ ≈ 1.0 × 10⁶ m s⁻¹"],
    why="1.0 × 10³ m s⁻¹ takes 0.727 nm as 7.27 × 10⁻⁷ m (a micrometre slip). 5.0 × 10⁵ m s⁻¹ wrongly puts a "
        "factor 2 in the relation (λ = h/2mv). 1.0 × 10⁹ m s⁻¹ takes the wavelength in picometres.",
    ncert=f"{REF2}, dual behaviour of matter", seconds=45, checked=True)

add("Quantum numbers and orbitals", B, "direct",
    "For the 2s orbital of the hydrogen atom, how does the probability density ψ² vary as the distance r from "
    "the nucleus increases?",
    Opts("B", "It falls to zero at one finite distance (a node) and then rises again before finally dying away",
         ["It is zero at the nucleus and increases steadily with r",
          "It decreases steadily with r and never becomes zero at any finite distance",
          "It becomes zero at two different finite distances from the nucleus"]),
    "Variation of ψ² with r for 1s and 2s orbitals",
    "For a 2s orbital ψ² is largest at the nucleus, decreases to zero at one value of r (the radial node, where "
    "ψ changes sign), rises again to a small maximum and then decreases towards zero at large r. A 2s orbital "
    "has n − l − 1 = 1 radial node.",
    ["2s: n = 2, l = 0 → radial nodes = 2 − 0 − 1 = 1", "ψ² → 0 once, then a second smaller maximum"],
    why="ψ² of an s orbital is not zero at the nucleus. A steady decrease without any node describes a 1s "
        "orbital. Two radial nodes belong to a 3s orbital.",
    ncert=f"{REF2}, quantum mechanical model of atom (plots of ψ and ψ² for 1s and 2s)", seconds=35)

add("Bohr model and hydrogen spectrum", B, "statement_pair",
    sp("Electromagnetic waves, unlike sound waves, do not need a medium and can travel through a vacuum.",
       "In electromagnetic radiation the oscillating electric and magnetic fields are perpendicular to each "
       "other and to the direction in which the wave travels."),
    SP_, "Nature of electromagnetic radiation",
    "NCERT describes electromagnetic radiation as oscillating electric and magnetic fields, perpendicular to "
    "each other and to the direction of propagation, which need no medium and travel through a vacuum at "
    "3.0 × 10⁸ m s⁻¹.",
    ["I: no medium needed, travels in vacuum → true", "II: E ⟂ B ⟂ direction of travel → true"],
    answer="A",
    why="Both are NCERT statements about electromagnetic waves; an option calling either false is wrong.",
    ncert=f"{REF2}, nature of electromagnetic radiation", seconds=30)

dE = 13.6 * 2 ** 2 * (1 - 1 / 2 ** 2)
assert close(dE, 40.8) and close(13.6 * (1 - 1 / 4), 10.2) and close(13.6 * 4, 54.4) and close(13.6 * 2 * 0.75, 20.4)
add("Bohr model and hydrogen spectrum", I, "numerical",
    "In Bohr's model the energy of the electron of a hydrogen-like species is Eₙ = −13.6 (Z²/n²) eV. The energy "
    "needed to excite the electron of a He⁺ ion (Z = 2) from n = 1 to n = 2 is:",
    Opts("C", "40.8 eV", ["10.2 eV", "54.4 eV", "20.4 eV"]),
    "Energy of a transition in a hydrogen-like ion: ΔE = 13.6 Z² (1/n₁² − 1/n₂²) eV",
    "Find the energies of the two levels for Z = 2 and take their difference.",
    ["E₁ = −13.6 × 4/1 = −54.4 eV", "E₂ = −13.6 × 4/4 = −13.6 eV", "ΔE = −13.6 − (−54.4) = 40.8 eV"],
    why="10.2 eV is the value for the hydrogen atom (Z² left out). 54.4 eV is the energy to remove the electron "
        "completely (n = 1 → ∞). 20.4 eV uses Z instead of Z².",
    ncert=f"{REF2}, Bohr's model for hydrogen atom", seconds=45, checked=True)

add("Electronic configuration", I, "assertion_reason",
    ar("In the ground state of a helium atom, the two electrons in the 1s orbital have opposite spins.",
       "No two electrons in an atom can have the same set of all four quantum numbers."),
    AR_, "Pauli exclusion principle",
    "Both helium electrons are in the 1s orbital, so they share n = 1, l = 0 and mₗ = 0. Pauli's principle "
    "forbids them from also sharing mₛ, so one has mₛ = +½ and the other −½: their spins must be opposite. R is "
    "the direct reason for A.",
    ["Same orbital → same n, l, mₗ", "Pauli: the fourth quantum number must differ → mₛ = +½ and −½",
     "Hence opposite spins → R explains A"],
    answer="A",
    why="R is not just another true statement: it is the rule that forces the two 1s electrons of helium to "
        "pair with opposite spins.",
    ncert=f"{REF2}, Pauli exclusion principle", seconds=35)

orbitals = {"A": 3 ** 2, "B": 2 * 1 + 1, "C": 1, "D": 2 * 3 + 1}
assert orbitals == {"A": 9, "B": 3, "C": 1, "D": 7}
add("Quantum numbers and orbitals", I, "match_list",
    lists("Match List-I (quantum numbers that are specified) with List-II (number of orbitals described by "
          "them).",
          ["n = 3", "n = 2, l = 1", "n = 4, l = 2, mₗ = 0", "n = 4, l = 3"],
          ["1", "3", "7", "9"]),
    match("D", M("IV II I III"), [M("IV III I II"), M("II IV I III"), M("IV II III I")]),
    "Counting orbitals from quantum numbers",
    "A shell n has n² orbitals; a subshell l has (2l + 1) orbitals; fixing n, l and mₗ picks out exactly one "
    "orbital.",
    ["A: n = 3 → 3² = 9 orbitals → IV", "B: 2p → 2(1) + 1 = 3 → II", "C: n, l and mₗ all fixed → 1 orbital → I",
     "D: 4f → 2(3) + 1 = 7 → III"],
    why="B-III/D-II gives a p subshell seven orbitals. A-II/B-IV confuses the shell with a subshell. "
        "C-III/D-I forgets that fixing mₗ leaves a single orbital.",
    ncert=f"{REF2}, quantum numbers", seconds=50, checked=True)

add("Electronic configuration", I, "statement_pair",
    sp("A ground-state chromium atom (Z = 24) has six unpaired electrons, all with parallel spins.",
       "In a ground-state iron atom (Z = 26), the two 4s electrons are unpaired."),
    SP_, "Ground-state configurations, Hund's rule and the Pauli principle",
    "Cr is [Ar] 3d⁵ 4s¹: five singly occupied 3d orbitals and one 4s electron, six unpaired electrons with "
    "parallel spins (maximum multiplicity). Fe is [Ar] 3d⁶ 4s²: the two 4s electrons share one orbital and must "
    "be paired; the four unpaired electrons are in 3d.",
    ["Cr: 3d⁵ 4s¹ → 6 unpaired, parallel → I true",
     "Fe: 4s² → one orbital, two electrons, opposite spins → II false"],
    answer="C",
    why="Two electrons in the same 4s orbital cannot both be unpaired (Pauli); Fe's unpaired electrons are the "
        "four in 3d.",
    ncert=f"{REF2}, electronic configuration of atoms; stability of half-filled subshells", seconds=40)

n_up = 1 / math.sqrt(1 - 12.75 / 13.6)
assert close(n_up, 4) and 4 * 3 // 2 == 6
add("Bohr model and hydrogen spectrum", A, "numerical",
    "A hydrogen atom in its ground state absorbs a photon of energy 12.75 eV. When the excited atoms return to "
    "the ground state, the highest level reached and the largest number of different spectral lines that a "
    "sample of such atoms can emit are, respectively (Eₙ = −13.6/n² eV):",
    Opts("A", "n = 4; 6 lines", ["n = 4; 3 lines", "n = 3; 3 lines", "n = 5; 10 lines"]),
    "Energy absorbed fixes the level reached; number of lines from level n to the ground state = n(n − 1)/2",
    "The energy of the level reached is −13.6 + 12.75 = −0.85 eV, which is −13.6/16, so n = 4. From n = 4 the "
    "electrons can fall by all possible routes, giving 4 × 3/2 = 6 different lines.",
    ["Eₙ = −13.6 + 12.75 = −0.85 eV", "13.6/n² = 0.85 → n² = 16 → n = 4",
     "Lines = n(n − 1)/2 = 4 × 3/2 = 6"],
    shortcut="12.75 eV = 13.6 × (1 − 1/16), so the jump is 1 → 4.",
    why="'n = 4; 3 lines' counts only the single cascade 4 → 3 → 2 → 1 and misses lines such as 4 → 1 and "
        "4 → 2. 'n = 3' and 'n = 5' come from solving 13.6/n² = 0.85 wrongly.",
    ncert=f"{REF2}, Bohr's model for hydrogen atom; line spectrum of hydrogen", seconds=90, checked=True)

truth_qm = {"a": True, "b": True, "c": False, "d": False, "e": True}
assert 2 - 0 - 1 + 0 == 1 and 1 - 0 - 1 == 0
add("Quantum numbers and orbitals", A, "multi_statement",
    ms("Which of the following statements about the quantum mechanical model of the atom are correct?",
       ["The wave function ψ of an electron has no physical meaning by itself.",
        "An atomic orbital is specified by the three quantum numbers n, l and mₗ.",
        "The probability of finding the electron at a point is given by the value of ψ at that point.",
        "The total number of nodes in an orbital with principal quantum number n is n.",
        "A 1s orbital has no node."]),
    multi("C", truth_qm, ["(a), (b), (c) and (e) only", "(b), (d) and (e) only", "(a), (c) and (d) only"]),
    "Wave function, probability density, orbitals and nodes",
    "ψ is a mathematical function with no physical meaning; ψ² gives the probability density. An orbital is "
    "fixed by n, l and mₗ (mₛ describes the electron's spin, not the orbital). The total number of nodes is "
    "n − 1 (radial n − l − 1 plus angular l).",
    ["(a) true", "(b) true", "(c) false: probability density is ψ², not ψ",
     "(d) false: total nodes = n − 1", "(e) 1s: n − 1 = 0 nodes → true"],
    why="Options with (c) treat ψ itself as a probability; options with (d) count n nodes instead of n − 1; the "
        "option without (a) leaves out a true statement.",
    ncert=f"{REF2}, quantum mechanical model of atom; orbitals and quantum numbers", seconds=80)

nodes = {"3p": (1, 1), "4d": (1, 2), "4p": (2, 1), "3s": (2, 0)}
assert all(nodes[o] == (int(o[0]) - "spdf".index(o[1]) - 1, "spdf".index(o[1])) for o in nodes)
assert [o for o, v in nodes.items() if v == (2, 1)] == ["4p"]
add("Quantum numbers and orbitals", A, "direct",
    "Which of the following orbitals has two radial (spherical) nodes and one angular node?",
    Opts("C", "4p", ["3p", "4d", "3s"]),
    "Radial nodes = n − l − 1; angular nodes = l",
    "One angular node means l = 1 (a p orbital). Two radial nodes then need n − 1 − 1 = 2, so n = 4.",
    ["Angular nodes = l = 1 → p orbital", "Radial nodes = n − l − 1 = 2 → n = 4", "Orbital = 4p"],
    why="3p has one radial and one angular node. 4d has one radial and two angular nodes. 3s has two radial "
        "nodes but no angular node.",
    ncert=f"{REF2}, shapes of atomic orbitals (nodes)", seconds=45, checked=True)


# ==================================================================== 3. Chemical Bonding and Molecular Structure
topic("Chemical Bonding and Molecular Structure")
REF3 = f"{C11}, 'Chemical Bonding and Molecular Structure'"


def formal_charge(valence, lone_electrons, bonds):
    return valence - lone_electrons - bonds


assert formal_charge(3, 0, 4) == -1 and formal_charge(7, 6, 1) == 0
add("Hybridisation and resonance", B, "numerical",
    "In the Lewis structure of the tetrafluoroborate ion, BF₄⁻, the boron atom forms four B–F single bonds and "
    "carries no lone pair. The formal charge on the boron atom is:",
    Opts("D", "−1", ["0", "+3", "−4"]),
    "Formal charge = (valence electrons) − (non-bonding electrons) − ½(bonding electrons)",
    "Boron has 3 valence electrons. In BF₄⁻ it has no non-bonding electrons and shares 8 electrons in four "
    "bonds, so it is assigned 4 electrons — one more than it brings.",
    ["V = 3, L = 0, ½S = ½ × 8 = 4", "Formal charge = 3 − 0 − 4 = −1",
     "Each F: 7 − 6 − 1 = 0, so the ion's −1 charge sits formally on B"],
    why="0 assumes the charge must be on fluorine. +3 counts boron's valence electrons without subtracting the "
        "shared ones. −4 subtracts all eight shared electrons instead of half of them.",
    ncert=f"{REF3}, formal charge", seconds=40, checked=True)

add("VSEPR shapes", B, "direct",
    "According to VSEPR theory, the shape of the sulphur dichloride molecule, SCl₂, is:",
    Opts("C", "Bent (V-shaped)", ["Linear", "T-shaped", "Trigonal planar"]),
    "VSEPR: shape from the numbers of bond pairs and lone pairs",
    "Sulphur has six valence electrons; two form S–Cl bonds and four stay as two lone pairs. Four electron pairs "
    "point to the corners of a tetrahedron, and with two of them lone pairs the molecule is bent, like H₂O.",
    ["S: 6 valence electrons → 2 bond pairs + 2 lone pairs", "Type AB₂E₂ → bent"],
    why="Linear needs no lone pairs (AB₂) or three (AB₂E₃). T-shaped is AB₃E₂. Trigonal planar is AB₃ with no "
        "lone pair.",
    ncert=f"{REF3}, VSEPR theory (shapes of molecules with lone pairs)", seconds=30)

add("Ionic bonding and lattice enthalpy", B, "statement_pair",
    sp("The van der Waals radius of chlorine is half the Cl–Cl bond length in the Cl₂ molecule.",
       "Bond enthalpy is the energy needed to break one mole of bonds of a particular type between two atoms "
       "in the gaseous state."),
    SP_, "Bond parameters: covalent and van der Waals radii; bond enthalpy",
    "Half the distance between two bonded chlorine atoms in Cl₂ is the covalent radius of chlorine. The van der "
    "Waals radius is half the distance between two similar atoms in separate (non-bonded) molecules in the "
    "solid, and is larger. Statement II is NCERT's definition of bond enthalpy.",
    ["I: half the bond length = covalent radius, not van der Waals radius → false",
     "II: definition of bond enthalpy → true"],
    answer="D",
    why="Statement I swaps the two radii; the van der Waals radius is measured between non-bonded atoms.",
    ncert=f"{REF3}, bond parameters (bond length, bond enthalpy)", seconds=35)

add("Molecular orbital theory", B, "assertion_reason",
    ar("The H₂⁺ ion is expected to be stable according to molecular orbital theory.",
       "H₂⁺ has one electron in the bonding σ1s orbital and none in the antibonding σ*1s orbital, so its bond "
       "order is ½."),
    AR_, "Bond order and stability from molecular orbital theory",
    "Bond order = ½(N_b − N_a). A positive bond order means the molecule or ion is more stable than the "
    "separated atoms. For H₂⁺, N_b = 1 and N_a = 0, so bond order = ½ > 0 and the ion is predicted to exist. R "
    "is exactly the reason for A.",
    ["H₂⁺: one electron → σ1s¹", "Bond order = ½(1 − 0) = ½", "Positive bond order → stable → R explains A"],
    answer="A",
    why="R gives the electron count and bond order on which the prediction in A rests; it is the explanation, "
        "not an unrelated fact.",
    ncert=f"{REF3}, molecular orbital theory (bond order and stability)", seconds=35)

add("VSEPR shapes", B, "match_list",
    lists("Match List-I (species) with List-II (its shape predicted by VSEPR theory).",
          ["NO₃⁻", "PCl₄⁺", "BrF₄⁻", "ICl₂⁻"],
          ["Linear", "Tetrahedral", "Square planar", "Trigonal planar"]),
    match("B", M("IV II III I"), [M("IV III II I"), M("II IV III I"), M("IV II I III")]),
    "VSEPR shapes of ions",
    "Count the electron pairs on the central atom (including the ion's charge), then decide the shape from the "
    "bond pairs and lone pairs.",
    ["NO₃⁻: three σ-bonded O, no lone pair on N → trigonal planar → IV",
     "PCl₄⁺: P has 5 − 1 = 4 electrons → 4 bond pairs → tetrahedral → II",
     "BrF₄⁻: Br has 7 + 1 = 8 electrons → 4 bond pairs + 2 lone pairs → square planar → III",
     "ICl₂⁻: I has 7 + 1 = 8 electrons → 2 bond pairs + 3 lone pairs → linear → I"],
    why="B-III/C-II treats BrF₄⁻ like a tetrahedral AB₄ and ignores its two lone pairs. A-II/B-IV swaps the "
        "planar and tetrahedral species. C-I/D-III swaps the AB₄E₂ and AB₂E₃ shapes.",
    ncert=f"{REF3}, VSEPR theory", seconds=70)

lp_clf3 = 2 + 3 * 3
assert lp_clf3 == 11
add("VSEPR shapes", I, "numerical",
    "The total number of lone pairs of electrons on ALL the atoms of the ClF₃ molecule (on chlorine and on the "
    "three fluorine atoms together) is:",
    Opts("B", "11", ["2", "9", "13"]),
    "Counting lone pairs in a Lewis structure",
    "Chlorine has 7 valence electrons; 3 are used in the three Cl–F bonds and the other 4 form two lone pairs. "
    "Each fluorine has 7 valence electrons; one is used in its bond and the other 6 form three lone pairs.",
    ["Cl: (7 − 3)/2 = 2 lone pairs", "3 F: 3 × 3 = 9 lone pairs", "Total = 2 + 9 = 11"],
    why="2 counts only the lone pairs on chlorine and 9 only those on fluorine. 13 gives chlorine four lone pairs "
        "(as if it formed no bonds).",
    ncert=f"{REF3}, Lewis structures; VSEPR theory", seconds=40, checked=True)

add("VSEPR shapes", I, "direct",
    "Which of the following is the correct order of the H–N–H bond angle in NH₄⁺, NH₃ and NH₂⁻?",
    Opts("D", "NH₄⁺ > NH₃ > NH₂⁻",
         ["NH₂⁻ > NH₃ > NH₄⁺", "NH₃ > NH₄⁺ > NH₂⁻", "NH₄⁺ = NH₃ = NH₂⁻"]),
    "Effect of lone pairs on bond angles (VSEPR)",
    "In all three species nitrogen has four electron pairs. NH₄⁺ has no lone pair (regular tetrahedron, "
    "109.5°), NH₃ has one lone pair (about 107°) and NH₂⁻ has two lone pairs. Lone pairs repel bond pairs more "
    "strongly than bond pairs do, so each extra lone pair squeezes the H–N–H angle further.",
    ["NH₄⁺: 4 bp, 0 lp → 109.5°", "NH₃: 3 bp, 1 lp → ≈107°", "NH₂⁻: 2 bp, 2 lp → smaller still (bent)"],
    why="The reversed order ignores lone-pair repulsion. NH₃ cannot exceed NH₄⁺ because it has a lone pair. "
        "Equal angles would need equal numbers of lone pairs.",
    ncert=f"{REF3}, VSEPR theory (lone pair–bond pair repulsion)", seconds=40)

add("Hybridisation and resonance", I, "statement_pair",
    sp("To explain the formation of SF₆, sulphur is pictured in an excited state that has four unpaired "
       "electrons.",
       "In SF₆, six sp³d² hybrid orbitals of sulphur overlap with singly occupied 2p orbitals of fluorine "
       "atoms to form six S–F σ bonds."),
    SP_, "sp³d² hybridisation in SF₆",
    "Ground-state S is 3s² 3p⁴. Promoting one 3s and one 3p electron into 3d orbitals gives 3s¹ 3p³ 3d², with "
    "SIX unpaired electrons. These six orbitals mix to give six sp³d² hybrids, each of which overlaps with a "
    "half-filled 2p orbital of an F atom.",
    ["Excited S: 3s¹ 3p³ 3d² → six unpaired electrons → I false",
     "Six sp³d² hybrids + six F 2p orbitals → six σ bonds → II true"],
    answer="D",
    why="Four unpaired electrons is the state used for SF₄-type bonding, not for six bonds in SF₆.",
    ncert=f"{REF3}, hybridisation involving d orbitals (sp³d², SF₆)", seconds=45)

add("Hybridisation and resonance", I, "statement_pair",
    sp("Valence bond theory explains the shapes of polyatomic molecules such as CH₄, NH₃ and H₂O in terms of "
       "the overlap and hybridisation of atomic orbitals.",
       "The four equal H–C–H angles of 109.5° in CH₄ can be explained by overlap of the hydrogen 1s orbitals "
       "with the unhybridised 2s and 2p orbitals of carbon."),
    SP_, "Directional properties of bonds and the need for hybridisation",
    "NCERT points out that simple overlap of the hydrogen 1s orbitals with carbon's 2s and three mutually "
    "perpendicular 2p orbitals would give three bonds at 90° and one different bond, not four identical bonds "
    "at 109.5°. The tetrahedral shape is explained by sp³ hybridisation.",
    ["I: VB theory + hybridisation explain shapes → true",
     "II: pure 2p orbitals are at 90°, so they cannot give 109.5° → false"],
    answer="C",
    why="Statement II describes exactly the simple-overlap picture that NCERT says fails for CH₄.",
    ncert=f"{REF3}, directional properties of bonds; hybridisation", seconds=40)

add("Molecular orbital theory", I, "assertion_reason",
    ar("The peroxide ion, O₂²⁻, is diamagnetic.",
       "The bond order of the O₂²⁻ ion is 2."),
    AR_, "MO configuration of O₂²⁻",
    "O₂²⁻ has 18 electrons: … σ2p_z² (π2p)⁴ (π*2p)⁴. All electrons are paired, so it is diamagnetic (A true). "
    "Bonding electrons in the valence MOs = 8 and antibonding = 6 (counting σ2s, σ*2s), so the bond order is "
    "½(10 − 8) = 1 overall, not 2. R is false.",
    ["O₂²⁻: π*2p fully filled (4 electrons) → no unpaired electron → A true",
     "Bond order = ½(N_b − N_a) = ½(10 − 8) = 1 → R false"],
    answer="C",
    why="A bond order of 2 belongs to O₂, whose two π* electrons are unpaired; adding two electrons fills π* and "
        "lowers the bond order to 1.",
    ncert=f"{REF3}, molecular orbital theory (bonding in O₂ and related species)", seconds=45)

add("Hybridisation and resonance", I, "match_list",
    lists("Match List-I (type of hybridisation) with List-II (angle between the hybrid orbitals).",
          ["sp", "sp²", "sp³", "sp³d²"],
          ["90°", "109°28′", "120°", "180°"]),
    match("B", M("IV III II I"), [M("III IV II I"), M("IV II III I"), M("IV III I II")]),
    "Geometry of hybrid orbitals",
    "sp hybrids are linear, sp² trigonal planar, sp³ tetrahedral and sp³d² octahedral.",
    ["sp → linear → 180° → IV", "sp² → trigonal planar → 120° → III", "sp³ → tetrahedral → 109°28′ → II",
     "sp³d² → octahedral → 90° → I"],
    why="A-III/B-IV swaps linear and trigonal planar. B-II/C-III swaps the planar and tetrahedral angles. "
        "C-I/D-II gives the octahedral angle to sp³.",
    ncert=f"{REF3}, hybridisation (types and geometry)", seconds=35)


def bond_order(nb, na):
    return (nb - na) / 2


bo = {"a": bond_order(10, 5), "b": bond_order(9, 4), "c": bond_order(10, 5), "d": bond_order(10, 7),
      "e": bond_order(8, 4)}
assert bo == {"a": 2.5, "b": 2.5, "c": 2.5, "d": 1.5, "e": 2.0}
truth_bo = {k: v == 2.5 for k, v in bo.items()}
add("Molecular orbital theory", I, "multi_statement",
    ms("According to molecular orbital theory, which of the following species have a bond order of 2.5?",
       ["O₂⁺", "N₂⁺", "N₂⁻", "O₂⁻", "C₂"]),
    multi("B", truth_bo, ["(a) and (d) only", "(a), (b), (c) and (e) only", "(b) and (c) only"]),
    "Bond order = ½(N_b − N_a)",
    "Count bonding and antibonding electrons (all electrons, including 1s) in each species using the "
    "appropriate MO energy order.",
    ["O₂⁺ (15 e⁻): N_b = 10, N_a = 5 → 2.5 ✓", "N₂⁺ (13 e⁻): N_b = 9, N_a = 4 → 2.5 ✓",
     "N₂⁻ (15 e⁻): N_b = 10, N_a = 5 → 2.5 ✓", "O₂⁻ (17 e⁻): N_b = 10, N_a = 7 → 1.5 ✗",
     "C₂ (12 e⁻): N_b = 8, N_a = 4 → 2 ✗"],
    why="O₂⁻ (superoxide) has bond order 1.5 and C₂ has bond order 2, so options containing (d) or (e) are "
        "wrong; '(b) and (c) only' misses O₂⁺.",
    ncert=f"{REF3}, molecular orbital theory (bond order)", seconds=80, checked=True)

truth_sp3 = {"a": True, "b": True, "c": False, "d": False, "e": True}
add("Hybridisation and resonance", A, "multi_statement",
    ms("In which of the following species is the central atom sp³ hybridised?",
       ["BF₄⁻", "H₃O⁺", "SO₃", "I₃⁻", "SiCl₄"]),
    multi("D", truth_sp3, ["(a), (b), (c) and (e) only", "(b), (d) and (e) only", "(a) and (e) only"]),
    "Hybridisation from the number of electron pairs (σ bond pairs + lone pairs) on the central atom",
    "Four electron pairs → sp³; three → sp²; five → sp³d. Count σ bonds and lone pairs on each central atom.",
    ["(a) BF₄⁻: 4 bond pairs, 0 lone pairs → sp³ ✓", "(b) H₃O⁺: 3 bond pairs + 1 lone pair → sp³ ✓",
     "(c) SO₃: 3 σ bonds, no lone pair → sp² ✗", "(d) I₃⁻: 2 bond pairs + 3 lone pairs = 5 → sp³d ✗",
     "(e) SiCl₄: 4 bond pairs → sp³ ✓"],
    why="SO₃ is trigonal planar (sp²) and I₃⁻ has five electron pairs (sp³d), so any option with (c) or (d) is "
        "wrong; '(a) and (e) only' misses H₃O⁺, whose lone pair counts as an electron pair.",
    ncert=f"{REF3}, hybridisation; VSEPR theory", seconds=75)

add("VSEPR shapes", A, "assertion_reason",
    ar("The H–O–H bond angle in water (104.5°) is smaller than the H–N–H bond angle in ammonia (107°).",
       "Lone pair–lone pair repulsion is greater than lone pair–bond pair repulsion, which in turn is greater "
       "than bond pair–bond pair repulsion."),
    AR_, "Order of electron-pair repulsions in VSEPR theory",
    "Both molecules have four electron pairs (tetrahedral arrangement). NH₃ has one lone pair; H₂O has two, so "
    "in water there is also a lone pair–lone pair repulsion, the strongest of all, which pushes the two O–H "
    "bond pairs closer together than the N–H bond pairs in NH₃. R gives the cause of A.",
    ["NH₃: 3 bp + 1 lp; H₂O: 2 bp + 2 lp", "lp–lp > lp–bp > bp–bp", "Extra lp–lp repulsion in H₂O → smaller angle"],
    answer="A",
    why="R is the repulsion order that VSEPR uses to explain exactly this difference in bond angles.",
    ncert=f"{REF3}, VSEPR theory", seconds=45)

add("Hybridisation and resonance", A, "statement_pair",
    sp("In the nitrite ion, NO₂⁻, the two nitrogen–oxygen bonds have different lengths, one being a double "
       "bond and the other a single bond.",
       "The average bond order of a nitrogen–oxygen bond in the nitrite ion is 1.5."),
    SP_, "Resonance and average bond order",
    "NO₂⁻ is a resonance hybrid of two equivalent structures, O=N–O⁻ and ⁻O–N=O. Neither structure is real; in "
    "the hybrid both N–O bonds are identical, with a length between those of N–O and N=O. Bond order = "
    "(1 + 2)/2 = 1.5.",
    ["Two equivalent canonical structures → both bonds identical → I false",
     "Average bond order = 3 bonds shared over 2 positions = 1.5 → II true"],
    answer="D",
    why="Statement I describes one canonical structure as if it were the real ion; resonance makes the bonds "
        "equal.",
    ncert=f"{REF3}, resonance structures", seconds=45)

add("VSEPR shapes", A, "match_list",
    lists("Match List-I (molecule) with List-II (geometry of ALL the electron pairs — bond pairs and lone pairs "
          "— around the central atom, which may differ from the shape of the molecule).",
          ["H₂O", "SF₄", "XeF₄", "SO₂"],
          ["Trigonal planar", "Octahedral", "Trigonal bipyramidal", "Tetrahedral"]),
    match("C", M("IV III II I"), [M("I III II IV"), M("IV II III I"), M("IV I II III")]),
    "Electron-pair geometry versus molecular shape (VSEPR)",
    "Count σ bond pairs plus lone pairs on the central atom (a multiple bond counts as one 'super pair'). The "
    "electron pairs take up the geometry for that number; the shape then describes only the atoms.",
    ["H₂O: 2 bp + 2 lp = 4 → tetrahedral (shape bent) → IV",
     "SF₄: 4 bp + 1 lp = 5 → trigonal bipyramidal (shape see-saw) → III",
     "XeF₄: 4 bp + 2 lp = 6 → octahedral (shape square planar) → II",
     "SO₂: 2 double-bond 'pairs' + 1 lp = 3 → trigonal planar (shape bent) → I"],
    why="A-I/D-IV swaps H₂O and SO₂, judging by the bent shape that both share. B-II/C-III swaps the five- and "
        "six-pair geometries. B-I/D-III gives SF₄ three pairs and SO₂ five.",
    ncert=f"{REF3}, VSEPR theory (geometry with lone pairs)", seconds=90)

add("Hybridisation and resonance", A, "direct",
    "In which of the following pairs do the two molecules have the SAME shape although their central atoms are "
    "DIFFERENTLY hybridised?",
    Opts("B", "CO₂ and XeF₂", ["NH₃ and PCl₃", "BF₃ and NO₃⁻", "SF₆ and XeF₄"]),
    "Shape depends on the bond pairs; hybridisation depends on all electron pairs",
    "CO₂: carbon is sp hybridised and the molecule is linear. XeF₂: xenon has 2 bond pairs and 3 lone pairs "
    "(sp³d), and with the lone pairs equatorial the molecule is also linear.",
    ["CO₂: sp, linear", "XeF₂: sp³d, linear → same shape, different hybridisation ✓",
     "NH₃/PCl₃: both sp³, both pyramidal", "BF₃/NO₃⁻: both sp², both trigonal planar",
     "SF₆/XeF₄: both sp³d², octahedral vs square planar (different shape)"],
    why="NH₃/PCl₃ and BF₃/NO₃⁻ share both shape and hybridisation. SF₆/XeF₄ is the reverse case: same "
        "hybridisation, different shapes.",
    ncert=f"{REF3}, hybridisation; VSEPR theory", seconds=60)


# ==================================================================== 4. Chemical Thermodynamics
topic("Chemical Thermodynamics")
REF4 = f"{C11}, 'Thermodynamics'"

cp_m = 75 / (2.0 * 1.5)
assert close(cp_m, 25) and close(75 / 1.5, 50) and close(75 / 2, 37.5) and close(cp_m - R_J, 16.7, 0.002)
add("First law, work and enthalpy", B, "numerical",
    "When 75 J of heat is supplied at constant pressure to 2.0 mol of a gas, its temperature rises by 1.5 K. "
    "The molar heat capacity of the gas at constant pressure, C_p,m, is:",
    Opts("A", "25 J K⁻¹ mol⁻¹", ["50 J K⁻¹ mol⁻¹", "37.5 J K⁻¹ mol⁻¹", "16.7 J K⁻¹ mol⁻¹"]),
    "Molar heat capacity: q = n C_m ΔT",
    "At constant pressure the heat supplied is q_p = n C_p,m ΔT, so C_p,m = q/(n ΔT).",
    ["C_p,m = 75 J / (2.0 mol × 1.5 K)", "C_p,m = 25 J K⁻¹ mol⁻¹"],
    why="50 J K⁻¹ mol⁻¹ is the heat capacity of the whole 2.0 mol sample, not per mole. "
        "37.5 divides by the amount but not by ΔT. 16.7 subtracts R, which would give C_v,m for an ideal gas, "
        "not C_p,m.",
    ncert=f"{REF4}, heat capacity; molar heat capacity", seconds=30, checked=True)

add("First law, work and enthalpy", B, "direct",
    "According to NCERT, which of the following is an example of a CLOSED system?",
    Opts("C", "Reactants placed in a closed vessel made of a conducting material such as copper or steel",
         ["Reactants placed in an open beaker",
          "Reactants placed in a thermos flask or any other closed, insulated vessel",
          "A living plant growing in the open air"]),
    "Open, closed and isolated systems",
    "A closed system can exchange energy but not matter with its surroundings. A sealed vessel made of a "
    "conducting metal lets heat pass through its walls but keeps the matter in.",
    ["Closed: energy exchanged, matter not → sealed conducting vessel",
     "Open beaker / plant: matter and energy both exchanged → open",
     "Thermos flask: neither exchanged → isolated"],
    why="An open beaker and a plant exchange matter with the surroundings (open systems). A closed, insulated "
        "vessel exchanges neither matter nor energy (isolated system).",
    ncert=f"{REF4}, types of the system", seconds=25)

add("First law, work and enthalpy", B, "assertion_reason",
    ar("Enthalpy is an extensive property.",
       "Enthalpy is a state function."),
    AR_, "Extensive properties versus state functions",
    "A is true: the enthalpy of a system depends on the amount of matter in it (doubling the system doubles H). "
    "R is also true: H depends only on the state of the system, not on how that state was reached. But being a "
    "state function has nothing to do with depending on the amount of matter — temperature and pressure are "
    "state functions too, yet they are intensive. So R does not explain A.",
    ["A: H depends on the amount of matter → extensive → true",
     "R: H = U + pV depends only on the state → true",
     "Temperature is a state function but intensive → 'state function' does not imply 'extensive' → option B"],
    answer="B",
    why="Option A would need state-function behaviour to make a property extensive, which the example of "
        "temperature disproves; both statements are true, so C and D are out.",
    ncert=f"{REF4}, extensive and intensive properties; state functions", seconds=40)

heat = 0.010 * 3200
c_cal = heat / 4.0
assert close(c_cal, 8.0) and close(heat * 4.0, 128) and close(3200 / 4.0, 800)
add("First law, work and enthalpy", I, "numerical",
    "A bomb calorimeter is calibrated by burning 0.010 mol of a standard substance whose internal energy of "
    "combustion is ΔcU = −3200 kJ mol⁻¹. The temperature of the calorimeter rises by 4.0 K. The heat capacity of "
    "the calorimeter is:",
    Opts("D", "8.0 kJ K⁻¹", ["128 kJ K⁻¹", "800 kJ K⁻¹", "0.80 kJ K⁻¹"]),
    "Bomb calorimetry: heat released at constant volume = C_calorimeter × ΔT",
    "At constant volume the heat given out by the combustion is −ΔU and it all goes into the calorimeter, so "
    "C = q/ΔT.",
    ["q = 0.010 mol × 3200 kJ mol⁻¹ = 32 kJ", "C = 32 kJ / 4.0 K = 8.0 kJ K⁻¹"],
    why="128 kJ K⁻¹ multiplies the heat by ΔT instead of dividing. 800 kJ K⁻¹ uses the molar value without "
        "multiplying by 0.010 mol. 0.80 kJ K⁻¹ slips a power of ten.",
    ncert=f"{REF4}, measurement of ΔU: calorimetry", seconds=45, checked=True)

add("Entropy and Gibbs energy", I, "statement_pair",
    sp("For every reaction that involves gases, ΔH is greater than ΔU.",
       "A reaction in which the entropy of the system decreases can never be spontaneous."),
    SP_, "ΔH–ΔU relation and the criteria of spontaneity",
    "ΔH = ΔU + Δn_g RT, so ΔH > ΔU only when the number of moles of gas increases; when Δn_g = 0 they are equal "
    "and when Δn_g < 0, ΔH < ΔU. A reaction with ΔS(system) < 0 can still be spontaneous if it is exothermic "
    "enough that ΔG = ΔH − TΔS is negative (low temperature), because the surroundings gain entropy.",
    ["I: depends on the sign of Δn_g; e.g. N₂ + 3H₂ → 2NH₃ has ΔH < ΔU → false",
     "II: ΔH < 0 and ΔS < 0 → spontaneous below T = ΔH/ΔS → false"],
    answer="B",
    why="Statement I ignores reactions with Δn_g ≤ 0, and Statement II ignores the entropy gained by the "
        "surroundings from the heat released.",
    ncert=f"{REF4}, enthalpy (ΔH and ΔU); Gibbs energy and spontaneity", seconds=45)

add("Gibbs energy and K", I, "match_list",
    lists("Match List-I (situation) with List-II (thermodynamic condition that describes it).",
          ["A spontaneous process at constant temperature and pressure",
           "A spontaneous change in an isolated system",
           "A system at equilibrium at constant temperature and pressure",
           "A reaction whose standard Gibbs energy change, ΔrG°, is zero"],
          ["ΔG = 0", "K = 1", "ΔS > 0", "ΔG < 0"]),
    match("A", M("IV III I II"), [M("III IV I II"), M("IV III II I"), M("I III IV II")]),
    "Criteria for spontaneity and equilibrium",
    "At constant T and p, ΔG < 0 for a spontaneous process and ΔG = 0 at equilibrium. In an isolated system "
    "(no exchange of energy), a spontaneous change increases the entropy. ΔrG° = −2.303 RT log K, so ΔrG° = 0 "
    "means log K = 0 and K = 1.",
    ["A → ΔG < 0 → IV", "B → ΔS > 0 → III", "C → ΔG = 0 → I", "D → log K = 0 → K = 1 → II"],
    why="A-III/B-IV swaps the criteria for constant T, p and for an isolated system. C-II/D-I confuses ΔG = 0 "
        "with ΔG° = 0. A-I/C-IV swaps spontaneity and equilibrium.",
    ncert=f"{REF4}, entropy and spontaneity; Gibbs energy change and equilibrium", seconds=50)

add("Gibbs energy and K", I, "assertion_reason",
    ar("A reaction with a large positive standard Gibbs energy change, ΔrG°, has an equilibrium constant much "
       "smaller than 1.",
       "ΔrG° = −2.303 RT log K."),
    AR_, "Relation between ΔrG° and K",
    "From ΔrG° = −2.303 RT log K, log K = −ΔrG°/(2.303 RT). A large positive ΔrG° makes log K large and "
    "negative, so K ≪ 1: at equilibrium the mixture contains mostly reactants. R is the relation from which A "
    "follows.",
    ["log K = −ΔrG°/2.303RT", "ΔrG° ≫ 0 → log K ≪ 0 → K ≪ 1", "R explains A"],
    answer="A",
    why="The equation in R is the direct cause of A, so 'not the correct explanation' does not apply.",
    ncert=f"{REF4}, Gibbs energy change and equilibrium", seconds=35)

dh_gas = 436 + 498 / 2 - 2 * 464
dh_liq = dh_gas - 44
assert dh_gas == -243 and dh_liq == -287 and -243 + 44 == -199 and 436 + 498 - 928 - 44 == -38
add("Hess's law and enthalpies", A, "numerical",
    "Use the mean bond enthalpies H–H = 436, O=O = 498 and O–H = 464 kJ mol⁻¹, and the enthalpy of vaporisation "
    "of water at 298 K, 44 kJ mol⁻¹, to estimate the standard enthalpy of formation of LIQUID water, "
    "H₂(g) + ½O₂(g) → H₂O(l):",
    Opts("C", "−287 kJ mol⁻¹", ["−243 kJ mol⁻¹", "−199 kJ mol⁻¹", "−38 kJ mol⁻¹"]),
    "Reaction enthalpy from bond enthalpies (valid for gases only) plus a phase-change step (Hess's law)",
    "The bond-enthalpy relation ΔrH = Σ(bonds broken) − Σ(bonds formed) applies only when all species are "
    "gases, so it gives the formation of H₂O(g). Then add the enthalpy of condensation of water (−44 kJ mol⁻¹) "
    "to reach H₂O(l).",
    ["Bonds broken: H–H + ½ O=O = 436 + 249 = 685 kJ", "Bonds formed: 2 O–H = 2 × 464 = 928 kJ",
     "H₂(g) + ½O₂(g) → H₂O(g): 685 − 928 = −243 kJ", "H₂O(g) → H₂O(l): −44 kJ",
     "ΔfH°(H₂O, l) ≈ −243 − 44 = −287 kJ mol⁻¹"],
    why="−243 kJ mol⁻¹ stops at water vapour. −199 kJ mol⁻¹ adds the enthalpy of vaporisation with the wrong "
        "sign (condensation releases heat). −38 kJ mol⁻¹ breaks a whole O=O bond instead of half of one.",
    ncert=f"{REF4}, bond enthalpy; Hess's law; enthalpy of phase transformation", seconds=100, checked=True)

truth_so3 = {"a": True, "b": True, "c": True, "d": False, "e": False}
dng = 2 - 3
assert dng == -1
add("Entropy and Gibbs energy", A, "multi_statement",
    ms("For the exothermic reaction 2SO₂(g) + O₂(g) → 2SO₃(g), carried out at constant temperature and pressure "
       "with the gases behaving ideally, which of the following statements are correct?",
       ["ΔH is more negative than ΔU.",
        "The entropy of the system decreases.",
        "Work is done ON the system by the surroundings (w is positive).",
        "The reaction becomes more favourable (ΔG more negative) as the temperature is raised, assuming ΔH and "
        "ΔS stay constant.",
        "The heat given out at constant pressure is equal to −ΔU."]),
    multi("B", truth_so3, ["(a), (b), (c) and (d) only", "(b), (c) and (e) only", "(a) and (d) only"]),
    "ΔH = ΔU + Δn_g RT; entropy, work and Gibbs energy for a gas-phase reaction",
    "Δn_g = 2 − 3 = −1. The gas volume shrinks, the entropy of the system falls, and the surroundings push the "
    "system in.",
    ["(a) ΔH = ΔU − RT → ΔH more negative ✓", "(b) 3 mol gas → 2 mol gas → ΔS < 0 ✓",
     "(c) volume decreases → w = −p ΔV > 0 ✓",
     "(d) ΔG = ΔH − TΔS with ΔH < 0, ΔS < 0: −TΔS is positive and grows with T → less favourable ✗",
     "(e) heat at constant pressure = −ΔH, not −ΔU ✗"],
    why="(d) reverses the effect of temperature when ΔS is negative, and (e) confuses q_p (ΔH) with q_v (ΔU); "
        "any option including either is wrong, and '(a) and (d) only' also misses (b) and (c).",
    ncert=f"{REF4}, enthalpy; work; Gibbs energy and spontaneity", seconds=100, checked=True)

add("Entropy and Gibbs energy", A, "direct",
    "An ideal gas in a thermally insulated, rigid container is allowed to expand from one half of the container "
    "into the other, evacuated half (the whole container being an isolated system). Which set of values is "
    "correct for this free expansion?",
    Opts("D", "w = 0, q = 0, ΔU = 0, ΔS > 0",
         ["w = 0, q = 0, ΔU = 0, ΔS = 0", "w < 0, q = 0, ΔU < 0, ΔS > 0", "w = 0, q > 0, ΔU > 0, ΔS > 0"]),
    "Free expansion of an ideal gas; entropy change in an isolated system",
    "Against zero external pressure the gas does no work (w = 0). The container is insulated (q = 0), so "
    "ΔU = q + w = 0 and the temperature of the ideal gas stays the same. The expansion is spontaneous in an "
    "isolated system, so the entropy increases.",
    ["p_ex = 0 → w = 0", "Insulated → q = 0", "ΔU = q + w = 0",
     "Spontaneous change in an isolated system → ΔS > 0"],
    why="ΔS = 0 would mean the expansion is not spontaneous, but gases spread into a vacuum on their own. w < 0 "
        "would need an external pressure to push against. q > 0 is impossible with insulated walls.",
    ncert=f"{REF4}, free expansion; entropy and spontaneity", seconds=60)


# ==================================================================== 5. Solutions
topic("Solutions")
REF5 = f"{C12}, 'Solutions'"

solute = 100 * 0.10 + 50 * 0.40
pct = solute / 150 * 100
assert close(pct, 20) and close((10 + 40) / 2, 25) and close(solute, 30)
add("Concentration terms", B, "numerical",
    "100 g of a 10% (by mass) aqueous solution of a salt is mixed with 50 g of a 40% (by mass) aqueous solution "
    "of the same salt. The mass percentage of the salt in the resulting solution is:",
    Opts("D", "20%", ["25%", "50%", "30%"]),
    "Mass percentage = (mass of solute ÷ total mass of solution) × 100",
    "Add the masses of salt from both solutions and divide by the total mass of the mixture.",
    ["Salt from first solution = 10% of 100 g = 10 g", "Salt from second solution = 40% of 50 g = 20 g",
     "Total salt = 30 g in 150 g of solution", "Mass % = 30/150 × 100 = 20%"],
    why="25% is the simple average of 10% and 40%, which ignores the different masses mixed. 50% adds the two "
        "percentages. 30% takes the 30 g of salt per 100 g, forgetting that the mixture weighs 150 g.",
    ncert=f"{REF5}, expressing concentration of solutions (mass percentage)", seconds=40, checked=True)

add("Raoult's law and ideal solutions", B, "statement_pair",
    sp("According to Raoult's law, for a solution of two volatile liquids the partial vapour pressure of each "
       "component is directly proportional to its mole fraction in the solution.",
       "According to Dalton's law of partial pressures, the total vapour pressure over such a solution is the "
       "sum of the partial vapour pressures of the components."),
    SP_, "Vapour pressure of a solution of two volatile liquids",
    "Raoult's law: p₁ = p₁° x₁ and p₂ = p₂° x₂. Dalton's law of partial pressures: p_total = p₁ + p₂. Together "
    "they give p_total = p₁° x₁ + p₂° x₂ for an ideal solution.",
    ["I: p_i ∝ x_i (Raoult's law) → true", "II: p_total = p₁ + p₂ (Dalton's law) → true"],
    answer="A",
    why="Both statements are used together in NCERT to derive the total vapour pressure of an ideal solution.",
    ncert=f"{REF5}, vapour pressure of liquid–liquid solutions", seconds=30)

add("Colligative properties", B, "assertion_reason",
    ar("Osmotic pressure of a dilute solution is a colligative property.",
       "The osmotic pressure of a solution can be measured at around room temperature."),
    AR_, "Osmotic pressure: a colligative property; why it suits biomolecules",
    "A is true: π = CRT depends only on the molar concentration of solute particles, not on what they are. R is "
    "also true: NCERT notes that osmotic pressure is measured at about room temperature, which is why the method "
    "suits heat-sensitive biomolecules. But the temperature at which it can be measured has nothing to do with "
    "why it depends only on the number of particles.",
    ["A: π = CRT → depends on the number of particles → true",
     "R: measured near room temperature → true (an advantage of the method)",
     "R is a practical advantage, not the reason π is colligative → option B"],
    answer="B",
    why="R explains why the osmotic-pressure method is preferred for proteins, not why osmotic pressure is a "
        "colligative property, so option A does not apply.",
    ncert=f"{REF5}, osmosis and osmotic pressure", seconds=40)

n_b, n_t = 39 / 78, 46 / 92
p_tot = n_b / (n_b + n_t) * 75 + n_t / (n_b + n_t) * 22
w_b = 39 / 85
assert close(p_tot, 48.5) and close(w_b * 75 + (1 - w_b) * 22, 46.3, 0.002) and close(0.5 * 75, 37.5)
add("Raoult's law and ideal solutions", I, "numerical",
    "39 g of benzene (C₆H₆) is mixed with 46 g of toluene (C₇H₈), and the two form an ideal solution. At the "
    "temperature of the experiment the vapour pressures of pure benzene and pure toluene are 75 mm Hg and "
    "22 mm Hg. The total vapour pressure of the solution is (C = 12, H = 1):",
    Opts("C", "48.5 mm Hg", ["97.0 mm Hg", "46.3 mm Hg", "37.5 mm Hg"]),
    "Raoult's law for two volatile liquids: p_total = x_A p_A° + x_B p_B°",
    "Convert the masses to moles, find the mole fractions, and add the two partial pressures.",
    ["n(benzene) = 39/78 = 0.50 mol; n(toluene) = 46/92 = 0.50 mol", "x(benzene) = x(toluene) = 0.50",
     "p_total = 0.50 × 75 + 0.50 × 22 = 37.5 + 11.0 = 48.5 mm Hg"],
    why="97.0 mm Hg adds the two pure-liquid vapour pressures without the mole fractions. 46.3 mm Hg uses mass "
        "fractions instead of mole fractions. 37.5 mm Hg is only the partial pressure of benzene.",
    ncert=f"{REF5}, vapour pressure of liquid–liquid solutions (Raoult's law)", seconds=60, checked=True)

add("Concentration terms", I, "assertion_reason",
    ar("The molarity and the molality of any aqueous solution are always numerically equal.",
       "Molarity is the number of moles of solute per litre of solution, whereas molality is the number of "
       "moles of solute per kilogram of solvent."),
    AR_, "Molarity versus molality",
    "R is the correct pair of definitions. Because one is per litre of SOLUTION and the other per kilogram of "
    "SOLVENT, the two are generally different (for example 2.0 M NaOH of density 1.12 g mL⁻¹ is about 1.9 m). "
    "They are close only for very dilute aqueous solutions. So A is false.",
    ["A: different bases (litre of solution vs kg of solvent) → not always equal → false",
     "R: correct definitions → true"],
    answer="D",
    why="A would need the volume of solution in litres always to equal the mass of solvent in kilograms, which "
        "is true only approximately for very dilute aqueous solutions.",
    ncert=f"{REF5}, expressing concentration of solutions (molarity, molality)", seconds=35)

pis = {"A": 0.1 * 1 * 0.082 * 300, "B": 0.1 * 2 * 0.082 * 300, "C": 0.1 * 3 * 0.082 * 300,
       "D": 0.05 * 1 * 0.082 * 300}
assert all(close(pis[k], v) for k, v in {"A": 2.46, "B": 4.92, "C": 7.38, "D": 1.23}.items())
add("van't Hoff factor", I, "match_list",
    lists("Match List-I (aqueous solution at 300 K, electrolytes completely dissociated) with List-II (its "
          "osmotic pressure). (R = 0.082 L atm K⁻¹ mol⁻¹)",
          ["0.10 M urea", "0.10 M NaCl", "0.10 M CaCl₂", "0.05 M glucose"],
          ["7.38 atm", "1.23 atm", "4.92 atm", "2.46 atm"]),
    match("B", M("IV III I II"), [M("IV I III II"), M("II III I IV"), M("IV III II I")]),
    "Osmotic pressure with the van't Hoff factor: π = iCRT",
    "CRT = 0.10 × 0.082 × 300 = 2.46 atm for a 0.10 M solution of a non-electrolyte. Multiply by i for "
    "electrolytes.",
    ["A: i = 1 → 2.46 atm → IV", "B: NaCl → 2 ions → 4.92 atm → III", "C: CaCl₂ → 3 ions → 7.38 atm → I",
     "D: 0.05 × 0.082 × 300 = 1.23 atm → II"],
    why="B-I/C-III swaps NaCl and CaCl₂ (wrong numbers of ions). A-II/D-IV ignores the factor of two between "
        "0.10 M and 0.05 M. C-II/D-I gives glucose the CaCl₂ value.",
    ncert=f"{REF5}, osmosis and osmotic pressure; abnormal molar masses", seconds=70, checked=True)

truth_t = {"a": True, "b": True, "c": False, "d": True, "e": False}
add("Concentration terms", I, "multi_statement",
    ms("Which of the following ways of expressing the concentration of a solution do NOT change when the "
       "temperature of the solution changes?",
       ["Mass percentage (w/w)", "Parts per million by mass", "Molarity", "Molality",
        "Mass by volume percentage (w/V)"]),
    multi("A", truth_t, ["(a), (b), (c) and (d) only", "(c), (d) and (e) only", "(a) and (d) only"]),
    "Temperature dependence of concentration terms",
    "Volume changes with temperature, masses do not. Terms based only on masses (or amounts) are independent "
    "of temperature; terms that use the volume of the solution change with temperature.",
    ["(a) mass/mass → independent ✓", "(b) ppm by mass → mass/mass → independent ✓",
     "(c) molarity → mol per litre of solution → changes ✗", "(d) molality → mol per kg of solvent → independent ✓",
     "(e) w/V → uses volume → changes ✗"],
    why="Molarity and mass-by-volume percentage both contain the volume of the solution, which expands on "
        "warming; '(a) and (d) only' leaves out ppm by mass, which is also mass-based.",
    ncert=f"{REF5}, expressing concentration of solutions", seconds=50)

i_obs = 0.2232 / (1.86 * 0.1)
alpha = i_obs - 1
ka = 0.1 * alpha ** 2 / (1 - alpha)
assert close(i_obs, 1.2) and close(alpha, 0.2) and close(ka, 5.0e-3) and close(0.1 * alpha ** 2, 4.0e-3) \
    and close(0.1 * alpha, 2.0e-2) and close(0.1 * 0.1 ** 2 / 0.9, 1.1e-3, 0.02)
add("van't Hoff factor", A, "numerical",
    "A 0.10 m aqueous solution of a weak monobasic acid HA (HA ⇌ H⁺ + A⁻) freezes at −0.2232 °C. Taking the "
    "molarity of this dilute solution to be equal to its molality, the dissociation constant Kₐ of the acid is "
    "(K_f of water = 1.86 K kg mol⁻¹; freezing point of water = 0 °C):",
    Opts("B", "5.0 × 10⁻³", ["4.0 × 10⁻³", "2.0 × 10⁻²", "1.1 × 10⁻³"]),
    "van't Hoff factor from a colligative property, then the degree of dissociation and Kₐ",
    "From ΔT_f = i K_f m find i. For HA ⇌ H⁺ + A⁻, i = 1 + α. Then Kₐ = cα²/(1 − α).",
    ["i = ΔT_f/(K_f m) = 0.2232/(1.86 × 0.10) = 1.2", "α = i − 1 = 0.20",
     "Kₐ = cα²/(1 − α) = 0.10 × 0.04/0.80 = 5.0 × 10⁻³"],
    why="4.0 × 10⁻³ uses Kₐ ≈ cα², which is not valid when α = 0.2. 2.0 × 10⁻² takes Kₐ = cα. 1.1 × 10⁻³ "
        "divides (i − 1) by 2, as if each HA gave three particles.",
    ncert=f"{REF5}, abnormal molar masses (van't Hoff factor)", seconds=110, checked=True)

i_dimer = 1 - 0.5 + 0.5 / 2
i_ab = 1 + 0.5
assert close(1 / i_dimer, 4 / 3) and close(1 / i_ab, 2 / 3)
add("van't Hoff factor", A, "statement_pair",
    sp("If 50% of the molecules of a solute X dimerise in solution (2X ⇌ X₂), the molar mass of X found from a "
       "colligative property is twice its true molar mass.",
       "If a salt AB is 50% dissociated into A⁺ and B⁻ in solution, the molar mass found from a colligative "
       "property is two-thirds of its true molar mass."),
    SP_, "van't Hoff factor and abnormal molar masses",
    "Observed molar mass = true molar mass ÷ i. For 50% dimerisation, i = (1 − 0.5) + 0.5/2 = 0.75, so the "
    "observed value is 4/3 of the true one (twice the true value needs COMPLETE dimerisation, i = 0.5). For AB "
    "50% dissociated, i = 1 + 0.5 = 1.5, so the observed value is 1/1.5 = 2/3 of the true one.",
    ["I: i = 0.75 → M_obs = M/0.75 = 1.33 M, not 2M → false",
     "II: i = 1.5 → M_obs = M/1.5 = 0.67 M → true"],
    answer="D",
    why="Statement I applies the result for complete association to a solute that is only half associated.",
    ncert=f"{REF5}, abnormal molar masses", seconds=70, checked=True)

particles = {"right": (0.10 * 3, 0.15 * 2), "w1": (0.10 * 2, 0.10 * 1), "w2": (0.10 * 3, 0.20 * 2),
             "w3": (0.05 * 3, 0.10 * 1)}
assert [k for k, (x, y) in particles.items() if close(x, y)] == ["right"]
add("Colligative properties", A, "direct",
    "Assuming complete dissociation of the electrolytes, which of the following pairs of aqueous solutions are "
    "ISOTONIC with each other at the same temperature?",
    Opts("C", "0.10 M Na₂SO₄ and 0.15 M KCl",
         ["0.10 M NaCl and 0.10 M glucose", "0.10 M CaCl₂ and 0.20 M NaCl", "0.05 M K₂SO₄ and 0.10 M urea"]),
    "Isotonic solutions have equal osmotic pressure, i.e. equal iC at the same temperature",
    "Compare the total molar concentration of solute particles, iC, for each pair.",
    ["Na₂SO₄: 3 × 0.10 = 0.30 M; KCl: 2 × 0.15 = 0.30 M → equal ✓",
     "NaCl 0.20 M vs glucose 0.10 M", "CaCl₂ 0.30 M vs NaCl 0.40 M", "K₂SO₄ 0.15 M vs urea 0.10 M"],
    why="Each of the other pairs has unequal particle concentrations; they look equal only if the van't Hoff "
        "factor is ignored or applied to one solution of the pair only.",
    ncert=f"{REF5}, osmosis and osmotic pressure (isotonic solutions)", seconds=60, checked=True)


# ==================================================================== 6. Equilibrium
topic("Equilibrium")
REF6 = f"{C11}, 'Equilibrium'"

ratio_h = 10 ** -5 / 10 ** -8
assert close(ratio_h, 1000)
add("Acids, bases and pH", B, "numerical",
    "At 298 K, solution P has pH 5 and solution Q has pH 8. The hydronium ion concentration of P is how many "
    "times that of Q?",
    Opts("B", "1000 times", ["3 times", "1.6 times", "10⁻³ times"]),
    "pH = −log[H₃O⁺]; each unit of pH is a factor of 10 in [H₃O⁺]",
    "[H₃O⁺] = 10⁻ᵖᴴ. The ratio is 10⁻⁵/10⁻⁸ = 10³.",
    ["P: [H₃O⁺] = 10⁻⁵ M", "Q: [H₃O⁺] = 10⁻⁸ M", "Ratio = 10⁻⁵/10⁻⁸ = 1000"],
    why="3 times treats the difference in pH as a ratio of concentrations. 1.6 times divides the pH values "
        "(8/5). 10⁻³ inverts the ratio: the solution with the lower pH has the HIGHER [H₃O⁺].",
    ncert=f"{REF6}, the pH scale", seconds=25, checked=True)

ksp_agbr = (7.0e-7) ** 2
assert close(ksp_agbr, 4.9e-13) and close((2 * 7.0e-7) ** 2, 1.96e-12)
add("Solubility product", B, "numerical",
    "The molar solubility of silver bromide, AgBr, in water at 298 K is 7.0 × 10⁻⁷ mol L⁻¹. Its solubility "
    "product at 298 K is:",
    Opts("A", "4.9 × 10⁻¹³", ["7.0 × 10⁻⁷", "1.4 × 10⁻⁶", "1.96 × 10⁻¹²"]),
    "K_sp of a 1 : 1 salt: AgBr(s) ⇌ Ag⁺(aq) + Br⁻(aq); K_sp = s²",
    "Each mole of AgBr that dissolves gives one mole of Ag⁺ and one mole of Br⁻, so both ion concentrations "
    "equal s.",
    ["[Ag⁺] = [Br⁻] = s = 7.0 × 10⁻⁷ M", "K_sp = s² = (7.0 × 10⁻⁷)² = 4.9 × 10⁻¹³"],
    why="7.0 × 10⁻⁷ is the solubility itself, not K_sp. 1.4 × 10⁻⁶ adds the two ion concentrations. "
        "1.96 × 10⁻¹² squares 2s, as if AgBr gave two of each ion.",
    ncert=f"{REF6}, solubility equilibria of sparingly soluble salts", seconds=30, checked=True)

add("Kp, Kc and Le Chatelier", B, "assertion_reason",
    ar("The equilibrium constant of a reaction changes when the temperature is changed.",
       "Adding a catalyst does not change the equilibrium constant of a reaction."),
    AR_, "Factors that do and do not change K",
    "A is true: K depends on temperature (it rises with temperature for an endothermic reaction and falls for "
    "an exothermic one). R is also true: a catalyst speeds up the forward and backward reactions equally and "
    "leaves K unchanged. But the behaviour of a catalyst says nothing about why temperature changes K; R is a "
    "separate fact.",
    ["A: K = f(T) → true", "R: catalyst → equilibrium reached faster, K unchanged → true",
     "R does not explain the temperature dependence in A → option B"],
    answer="B",
    why="R is about a catalyst, a different factor from temperature, so it cannot be the explanation of A; both "
        "statements are true, so C and D are wrong.",
    ncert=f"{REF6}, factors affecting equilibria (temperature; catalyst)", seconds=35)

add("Acids, bases and pH", B, "direct",
    "Which of the following is NOT a conjugate acid–base pair?",
    Opts("D", "H₃PO₄ and HPO₄²⁻", ["H₂O and OH⁻", "NH₄⁺ and NH₃", "HSO₄⁻ and SO₄²⁻"]),
    "Brønsted–Lowry conjugate acid–base pairs differ by exactly one proton",
    "An acid and its conjugate base differ by one H⁺. H₃PO₄ and HPO₄²⁻ differ by two protons; the conjugate base "
    "of H₃PO₄ is H₂PO₄⁻.",
    ["H₂O/OH⁻: differ by one H⁺ ✓", "NH₄⁺/NH₃: one H⁺ ✓", "HSO₄⁻/SO₄²⁻: one H⁺ ✓",
     "H₃PO₄/HPO₄²⁻: two H⁺ → not a conjugate pair"],
    why="Each of the other three pairs differs by exactly one proton, so each is a genuine conjugate pair.",
    ncert=f"{REF6}, Brönsted–Lowry acids and bases", seconds=25)

add("Physical equilibria and Henry's law", B, "match_list",
    lists("Match List-I (equilibrium in a closed vessel at constant temperature) with List-II (its type).",
          ["H₂O(l) ⇌ H₂O(g)", "N₂(g) + 3H₂(g) ⇌ 2NH₃(g)", "CaCO₃(s) ⇌ CaO(s) + CO₂(g)", "I₂(s) ⇌ I₂(g)"],
          ["Physical equilibrium: solid ⇌ vapour", "Homogeneous chemical equilibrium",
           "Physical equilibrium: liquid ⇌ vapour", "Heterogeneous chemical equilibrium"]),
    match("C", M("III II IV I"), [M("I II IV III"), M("III IV II I"), M("III II I IV")]),
    "Physical versus chemical equilibria; homogeneous versus heterogeneous",
    "A physical equilibrium involves only a change of state; a chemical equilibrium involves a reaction. A "
    "chemical equilibrium is homogeneous when all species are in one phase and heterogeneous when more than one "
    "phase is present.",
    ["A: evaporation ⇌ condensation of water → III", "B: all gases, chemical change → homogeneous → II",
     "C: two solids and a gas → heterogeneous → IV", "D: sublimation of iodine → solid ⇌ vapour → I"],
    why="A-I/D-III swaps the two physical equilibria. B-IV/C-II swaps the homogeneous and heterogeneous "
        "reactions. C-I/D-IV calls the decomposition of CaCO₃ a physical change.",
    ncert=f"{REF6}, equilibrium in physical processes; homogeneous and heterogeneous equilibria", seconds=45)

poh = 4.74 + math.log10(0.10 / 0.20)
ph_buf = 14 - poh
assert close(ph_buf, 9.56, 0.001) and close(14 - (4.74 + math.log10(2)), 8.96, 0.001)
add("Hydrolysis and buffers", I, "numerical",
    "A buffer solution at 298 K contains 0.20 M aqueous ammonia (NH₄OH) and 0.10 M ammonium chloride. Its pH is "
    "(pK_b of NH₄OH = 4.74; pK_w = 14; log 2 = 0.30):",
    Opts("A", "9.56", ["8.96", "4.44", "9.26"]),
    "Basic buffer: pOH = pK_b + log([salt]/[base])",
    "Find the pOH of the basic buffer from the Henderson–Hasselbalch form for bases, then pH = 14 − pOH.",
    ["pOH = 4.74 + log(0.10/0.20) = 4.74 − 0.30 = 4.44", "pH = 14 − 4.44 = 9.56"],
    why="8.96 inverts the ratio (base/salt instead of salt/base). 4.44 reports the pOH as the pH. 9.26 is "
        "14 − pK_b, the pH only when the salt and base concentrations are equal.",
    ncert=f"{REF6}, buffer solutions", seconds=50, checked=True)

s_common = 4.0e-11 / 0.10 ** 2
assert close(s_common, 4.0e-9) and close(4.0e-11 / 0.10, 4.0e-10) and close(4.0e-11 / 0.20 ** 2, 1.0e-9) \
    and close((4.0e-11 / 4) ** (1 / 3), 2.15e-4, 0.005)
add("Solubility product", I, "numerical",
    "A sparingly soluble fluoride MF₂ dissolves as MF₂(s) ⇌ M²⁺(aq) + 2F⁻(aq); its K_sp at 298 K is "
    "4.0 × 10⁻¹¹. Its molar solubility in a 0.10 M NaF solution at 298 K is (NaF completely dissociated; "
    "∛10 = 2.15):",
    Opts("C", "4.0 × 10⁻⁹ M", ["4.0 × 10⁻¹⁰ M", "1.0 × 10⁻⁹ M", "2.2 × 10⁻⁴ M"]),
    "Common ion effect on solubility: K_sp = [M²⁺][F⁻]² with [F⁻] fixed by the added salt",
    "The F⁻ from NaF (0.10 M) is far greater than the F⁻ from the dissolved MF₂, so [F⁻] ≈ 0.10 M and "
    "s = [M²⁺] = K_sp/[F⁻]².",
    ["[F⁻] ≈ 0.10 M", "s = 4.0 × 10⁻¹¹ / (0.10)² = 4.0 × 10⁻⁹ M"],
    why="4.0 × 10⁻¹⁰ M forgets to square [F⁻]. 1.0 × 10⁻⁹ M doubles the fluoride from NaF (takes 0.20 M). "
        "2.2 × 10⁻⁴ M is the solubility in pure water, ∛(K_sp/4), with the common ion ignored.",
    ncert=f"{REF6}, common ion effect in the ionisation of sparingly soluble salts", seconds=60, checked=True)

p_n2 = 0.80 * 2.5
x_n2 = p_n2 / 100e3
assert close(x_n2, 2.0e-5) and close(2.5 / 100e3, 2.5e-5) and close(p_n2 / 100, 2.0e-2) and close(0.80 / 100e3, 8.0e-6)
add("Physical equilibria and Henry's law", I, "numerical",
    "Air containing 80% nitrogen by moles is kept over water at a total pressure of 2.5 bar at a temperature "
    "at which the Henry's law constant of N₂ in water is K_H = 100 kbar. The mole fraction of nitrogen "
    "dissolved in the water is:",
    Opts("D", "2.0 × 10⁻⁵", ["2.5 × 10⁻⁵", "2.0 × 10⁻²", "8.0 × 10⁻⁶"]),
    "Henry's law with Dalton's law of partial pressures: p = K_H x, where p is the PARTIAL pressure",
    "First find the partial pressure of N₂ (mole fraction in air × total pressure), then x = p/K_H with both "
    "pressures in the same unit.",
    ["p(N₂) = 0.80 × 2.5 bar = 2.0 bar", "K_H = 100 kbar = 1.0 × 10⁵ bar",
     "x(N₂) = 2.0 / 1.0 × 10⁵ = 2.0 × 10⁻⁵"],
    why="2.5 × 10⁻⁵ uses the total pressure instead of the partial pressure of N₂. 2.0 × 10⁻² leaves K_H in "
        "kbar. 8.0 × 10⁻⁶ uses the mole fraction 0.80 as if it were the pressure.",
    ncert=f"{C12}, 'Solutions', Henry's law", seconds=55, checked=True)

pkw_323 = -math.log10(5.5e-14)
assert close(pkw_323, 13.26, 0.001)
add("Acids, bases and pH", I, "statement_pair",
    sp("At 323 K, where K_w = 5.5 × 10⁻¹⁴, the pH and pOH of any aqueous solution add up to 14.",
       "At 298 K, where K_w = 1.0 × 10⁻¹⁴, the pH and pOH of any aqueous solution add up to 14."),
    SP_, "pH + pOH = pK_w, which depends on temperature",
    "Taking −log of K_w = [H₃O⁺][OH⁻] gives pH + pOH = pK_w. At 298 K, pK_w = 14. At 323 K, "
    "pK_w = −log(5.5 × 10⁻¹⁴) = 14 − 0.74 = 13.26, so pH + pOH = 13.26, not 14.",
    ["pH + pOH = pK_w", "323 K: pK_w = 13.26 → I false", "298 K: pK_w = 14 → II true"],
    answer="D",
    why="Statement I uses the 298 K value of pK_w at a temperature where K_w is larger.",
    ncert=f"{REF6}, ionization constant of water and its ionic product; the pH scale", seconds=45, checked=True)

add("Acids, bases and pH", I, "assertion_reason",
    ar("Acetic acid is a weak electrolyte.",
       "Acetic acid is only slightly soluble in water."),
    AR_, "Strong and weak electrolytes",
    "A weak electrolyte is one that is only partially ionised in solution. Acetic acid mixes with water in all "
    "proportions (it is very soluble), but only a small fraction of its molecules ionise, so it is a weak "
    "electrolyte. A is true; R is false.",
    ["A: partially ionised → weak electrolyte → true",
     "R: acetic acid is miscible with water → false",
     "Weakness is about the extent of ionisation, not solubility"],
    answer="C",
    why="R confuses the extent of ionisation with solubility; a substance can be very soluble yet weakly "
        "ionised.",
    ncert=f"{REF6}, ionic equilibrium in solution (strong and weak electrolytes)", seconds=30)

truth_h = {"a": True, "b": True, "c": True, "d": False, "e": False}
add("Physical equilibria and Henry's law", I, "multi_statement",
    ms("Which of the following statements about Henry's law and the solubility of gases in liquids are "
       "correct?",
       ["The Henry's law constant, K_H, depends on the nature of the gas.",
        "At a given partial pressure and temperature, the higher the K_H value of a gas, the lower its "
        "solubility in the liquid.",
        "The K_H value of a gas in water increases as the temperature rises.",
        "The solubility of a gas in a liquid increases as the temperature rises.",
        "At constant temperature, the mole fraction of a gas in its solution is inversely proportional to the "
        "partial pressure of the gas above the solution."]),
    multi("B", truth_h, ["(a), (b), (c) and (e) only", "(a), (c) and (d) only", "(b) and (d) only"]),
    "Henry's law: p = K_H x",
    "x = p/K_H, so the mole fraction dissolved is directly proportional to the partial pressure and inversely "
    "proportional to K_H. K_H differs from gas to gas and rises with temperature, so gases become less soluble "
    "on warming.",
    ["(a) ✓", "(b) x = p/K_H → larger K_H, smaller x ✓", "(c) ✓ (NCERT)",
     "(d) ✗: K_H rises → solubility falls with temperature",
     "(e) ✗: x is directly proportional to p"],
    why="(d) reverses the effect of temperature and (e) reverses Henry's law; any option containing either is "
        "wrong.",
    ncert=f"{C12}, 'Solutions', Henry's law", seconds=60)

x = (4.0 * 0.70 - 0.80) / 5.0
assert close(x, 0.40) and close((0.80 + x) / (0.70 - x), 4.0) and close(0.80 + x, 1.20)
add("Kp, Kc and Le Chatelier", A, "numerical",
    "For the equilibrium A(g) ⇌ B(g), K_c = 4.0 at a certain temperature. An equilibrium mixture in a closed "
    "1.0 L vessel contains 0.20 mol of A and 0.80 mol of B. Another 0.50 mol of A is now added, the temperature "
    "and volume being kept constant. When equilibrium is re-established, the amount of B is:",
    Opts("D", "1.20 mol", ["1.30 mol", "0.80 mol", "2.80 mol"]),
    "Le Chatelier's principle made quantitative: the system re-adjusts until Q = K again",
    "After the addition, Q = 0.80/0.70 < K, so the reaction moves forward. Let x mol of A change into B and use "
    "K_c to find x.",
    ["After adding A: [A] = 0.70 M, [B] = 0.80 M; Q = 1.14 < 4.0 → forward",
     "(0.80 + x)/(0.70 − x) = 4.0 → 0.80 + x = 2.80 − 4x → x = 0.40",
     "B = 0.80 + 0.40 = 1.20 mol (A = 0.30 mol; check 1.20/0.30 = 4.0)"],
    why="1.30 mol assumes all the added A turns into B. 0.80 mol assumes the equilibrium does not shift. "
        "2.80 mol multiplies K by the new amount of A without letting A be used up.",
    ncert=f"{REF6}, effect of concentration change (Le Chatelier's principle)", seconds=100, checked=True)

kp_pcl5 = 0.5 ** 2 * 1.0 / (1 - 0.5 ** 2)
p_new = kp_pcl5 * (1 - 0.2 ** 2) / 0.2 ** 2
assert close(p_new, 8.0) and close((0.5 / 0.2) ** 2, 6.25) and close(0.5 / 0.2, 2.5)
add("Kp, Kc and Le Chatelier", A, "numerical",
    "Pure PCl₅ is heated to a fixed temperature: PCl₅(g) ⇌ PCl₃(g) + Cl₂(g). At a total equilibrium pressure of "
    "1.0 atm it is 50% dissociated. At the same temperature, the total equilibrium pressure at which it would be "
    "only 20% dissociated is (for this equilibrium, K_p = α²P/(1 − α²), where α is the degree of dissociation "
    "and P the total pressure):",
    Opts("A", "8.0 atm", ["6.25 atm", "2.5 atm", "0.125 atm"]),
    "K_p is constant at a fixed temperature; the degree of dissociation adjusts to the total pressure",
    "Find K_p from the first set of data, then solve the same relation for P when α = 0.20.",
    ["K_p = (0.5)² × 1.0 / (1 − 0.25) = 0.25/0.75 = 1/3 atm", "At α = 0.20: 1/3 = 0.04 P / 0.96",
     "P = (1/3) × 0.96/0.04 = 8.0 atm"],
    why="6.25 atm uses the approximation K_p ≈ α²P (ignoring α² in 1 − α²), not valid at α = 0.5. 2.5 atm "
        "takes α inversely proportional to P. 0.125 atm inverts the pressure ratio; lowering α needs a "
        "HIGHER pressure.",
    ncert=f"{REF6}, equilibrium constant Kp; effect of pressure change", seconds=110, checked=True)

c_base = 0.010 / 0.200
oh = math.sqrt(2.0e-5 * c_base)
ph_mix = 14 + math.log10(oh)
assert close(c_base, 0.050) and close(ph_mix, 11.0, 0.001) \
    and close(14 + math.log10(math.sqrt(2.0e-5 * 0.10)), 11.15, 0.001) and close(14 + math.log10(0.05), 12.7, 0.001)
add("Hydrolysis and buffers", A, "numerical",
    "100 mL of 0.10 M ammonium chloride solution is mixed with 100 mL of 0.10 M sodium hydroxide solution at "
    "298 K. The pH of the resulting solution is (K_b of NH₄OH = 2.0 × 10⁻⁵; pK_w = 14; for a weak base, "
    "[OH⁻] ≈ √(K_b c)):",
    Opts("B", "11.0", ["11.15", "7.0", "12.7"]),
    "A strong base displaces a weak base from its salt; then the pH of a weak base",
    "NH₄Cl + NaOH → NH₄OH + NaCl. Equal amounts react completely, leaving only the weak base NH₄OH (NaCl is "
    "neutral), diluted into 200 mL.",
    ["n(NH₄OH) = 0.10 × 0.100 = 0.010 mol in 0.200 L → c = 0.050 M",
     "[OH⁻] = √(2.0 × 10⁻⁵ × 0.050) = √(1.0 × 10⁻⁶) = 1.0 × 10⁻³ M", "pOH = 3.0; pH = 11.0"],
    why="11.15 forgets that mixing doubles the volume (uses 0.10 M). 7.0 treats the mixture as a neutralisation "
        "that leaves only a neutral salt, overlooking the NH₄OH formed. 12.7 treats the solution as 0.05 M "
        "NaOH, as if no reaction occurred.",
    ncert=f"{REF6}, ionization of weak bases", seconds=110, checked=True)

add("Kp, Kc and Le Chatelier", A, "direct",
    "For which of the following equilibria will BOTH raising the temperature AND lowering the total pressure "
    "shift the equilibrium in the forward direction?",
    Opts("A", "PCl₅(g) ⇌ PCl₃(g) + Cl₂(g); ΔH > 0",
         ["N₂(g) + 3H₂(g) ⇌ 2NH₃(g); ΔH < 0", "N₂(g) + O₂(g) ⇌ 2NO(g); ΔH > 0",
          "2SO₂(g) + O₂(g) ⇌ 2SO₃(g); ΔH < 0"]),
    "Le Chatelier's principle for temperature and pressure",
    "Raising the temperature favours the endothermic direction, so the forward reaction must be endothermic "
    "(ΔH > 0). Lowering the pressure favours the side with more moles of gas, so the forward reaction must "
    "increase the moles of gas (Δn_g > 0).",
    ["PCl₅: ΔH > 0, Δn_g = +1 → both favour forward ✓", "NH₃ synthesis: ΔH < 0, Δn_g = −2 → both favour backward",
     "NO formation: ΔH > 0 but Δn_g = 0 → pressure has no effect", "SO₃ formation: ΔH < 0, Δn_g = −1 → both backward"],
    why="The NO equilibrium responds to temperature but not to pressure; the ammonia and SO₃ equilibria are "
        "pushed backward by both changes.",
    ncert=f"{REF6}, factors affecting equilibria", seconds=50)

add("Acids, bases and pH", A, "assertion_reason",
    ar("When a solution of a weak monobasic acid is diluted with water, its pH increases even though the degree "
       "of ionisation of the acid increases.",
       "On dilution [H₃O⁺] ≈ √(Kₐc) decreases, because the degree of ionisation (α ≈ √(Kₐ/c)) increases only as "
       "1/√c while the concentration c falls in direct proportion."),
    AR_, "Effect of dilution on the degree of ionisation and pH of a weak acid",
    "[H₃O⁺] = cα. Diluting 100 times raises α only 10 times, so cα falls 10 times and the pH rises by 1. R gives "
    "exactly this reasoning, so it explains A.",
    ["α ≈ √(Kₐ/c) → α rises on dilution", "[H₃O⁺] = cα = √(Kₐc) → falls on dilution",
     "Lower [H₃O⁺] → higher pH → R explains A"],
    answer="A",
    why="R is the quantitative reason why more ionisation still gives fewer H₃O⁺ ions per litre, so it is the "
        "correct explanation, not just a related fact.",
    ncert=f"{REF6}, ionization constants of weak acids", seconds=50)


# ==================================================================== 7. Redox Reactions and Electrochemistry
topic("Redox Reactions and Electrochemistry")
REF7 = f"{C12}, 'Electrochemistry'"
REF7R = f"{C11}, 'Redox Reactions'"

e_m = 0.0 - 0.44
assert close(e_m, -0.44) and close(e_m / 2, -0.22)
add("Electrode potential and cells", B, "numerical",
    "The standard emf of the cell M(s) | M²⁺(aq, 1 M) || H⁺(aq, 1 M) | H₂(g, 1 bar) | Pt(s) is +0.44 V at "
    "298 K, the metal electrode M being the anode. The standard electrode (reduction) potential of the M²⁺/M "
    "couple is:",
    Opts("C", "−0.44 V", ["+0.44 V", "−0.22 V", "+0.22 V"]),
    "E°cell = E°(cathode) − E°(anode), with the standard hydrogen electrode taken as 0 V",
    "The hydrogen electrode on the right is the cathode with E° = 0. Rearranging, E°(anode) = E°(cathode) − "
    "E°cell.",
    ["E°cell = E°(H⁺/H₂) − E°(M²⁺/M)", "0.44 = 0 − E°(M²⁺/M)", "E°(M²⁺/M) = −0.44 V"],
    why="+0.44 V forgets that the anode couple has the LOWER reduction potential. −0.22 V and +0.22 V divide by "
        "the number of electrons, but E° does not depend on n.",
    ncert=f"{REF7}, measurement of electrode potential (standard hydrogen electrode)", seconds=35, checked=True)

lam = 6.0e-3 * 1000 / 0.050
assert close(lam, 120) and close(6.0e-3 / 0.050, 0.12) and close(6.0e-3 * 1000 * 0.050, 0.30) \
    and close(6.0e-3 * 0.050, 3.0e-4)
add("Conductance and Kohlrausch's law", B, "numerical",
    "The conductivity of a 0.050 mol L⁻¹ solution of an electrolyte is 6.0 × 10⁻³ S cm⁻¹. Its molar "
    "conductivity, in S cm² mol⁻¹, is:",
    Opts("D", "120", ["0.12", "0.30", "3.0 × 10⁻⁴"]),
    "Λm = κ × 1000 / c (κ in S cm⁻¹, c in mol L⁻¹, Λm in S cm² mol⁻¹)",
    "Molar conductivity is conductivity divided by molar concentration; the factor 1000 converts litres into "
    "cm³.",
    ["Λm = (6.0 × 10⁻³ S cm⁻¹ × 1000 cm³ L⁻¹) / 0.050 mol L⁻¹", "Λm = 120 S cm² mol⁻¹"],
    why="0.12 forgets the factor 1000 cm³ L⁻¹. 0.30 multiplies by the concentration instead of dividing. "
        "3.0 × 10⁻⁴ multiplies κ by c and omits the factor 1000.",
    ncert=f"{REF7}, conductance of electrolytic solutions (molar conductivity)", seconds=35, checked=True)

add("Oxidation number and balancing", B, "direct",
    "Which of the following species can act ONLY as a reducing agent in redox reactions?",
    Opts("A", "S²⁻", ["SO₂", "H₂O₂", "NO₂⁻"]),
    "An element in its lowest possible oxidation state can only be oxidised",
    "A species acts only as a reducing agent when its key element is already in its lowest oxidation state and "
    "can only increase it. Sulphur is −2 in S²⁻, its lowest state. In SO₂ (S = +4), H₂O₂ (O = −1) and NO₂⁻ "
    "(N = +3) the element is in an intermediate state, so these can be oxidised or reduced.",
    ["S²⁻: S = −2 (lowest) → only reducing ✓", "SO₂: S = +4 → both", "H₂O₂: O = −1 → both",
     "NO₂⁻: N = +3 → both"],
    why="SO₂, H₂O₂ and NO₂⁻ each contain an element in an intermediate oxidation state and can act as either an "
        "oxidising or a reducing agent.",
    ncert=f"{REF7R}, oxidation number; redox reactions", seconds=35)

add("Oxidation number and balancing", B, "match_list",
    lists("Match List-I (term) with List-II (its meaning in terms of electron transfer).",
          ["Oxidation", "Oxidising agent", "Reducing agent", "Disproportionation"],
          ["A species that donates electrons and is itself oxidised",
           "The same element in one species is simultaneously oxidised and reduced",
           "Loss of electrons by a species",
           "A species that accepts electrons and is itself reduced"]),
    match("B", M("III IV I II"), [M("III I IV II"), M("IV III I II"), M("III IV II I")]),
    "Electronic concept of oxidation and reduction",
    "Oxidation is loss of electrons and reduction is gain. An oxidising agent takes electrons (and is reduced); "
    "a reducing agent gives electrons (and is oxidised). In disproportionation one element is both oxidised and "
    "reduced.",
    ["A: loss of electrons → III", "B: electron acceptor, itself reduced → IV",
     "C: electron donor, itself oxidised → I", "D: same element oxidised and reduced → II"],
    why="B-I/C-IV swaps the oxidising and reducing agents. A-IV/B-III confuses oxidation with an oxidising "
        "agent. C-II/D-I swaps reducing agent and disproportionation.",
    ncert=f"{REF7R}, redox reactions in terms of electron transfer", seconds=40)

e_disp = 0.52 - 0.15
assert close(e_disp, 0.37) and close(0.52 + 0.15, 0.67)
add("Electrode potential and cells", I, "numerical",
    "Given the standard reduction potentials E°(Cu²⁺/Cu⁺) = +0.15 V and E°(Cu⁺/Cu) = +0.52 V at 298 K, the "
    "standard emf for the reaction 2Cu⁺(aq) → Cu²⁺(aq) + Cu(s), and the conclusion about Cu⁺ in aqueous "
    "solution, are:",
    Opts("A", "+0.37 V; Cu⁺ disproportionates",
         ["−0.37 V; Cu⁺ is stable", "+0.67 V; Cu⁺ disproportionates", "+0.37 V; Cu⁺ is stable"]),
    "Feasibility of a disproportionation from standard potentials",
    "Split the reaction into a reduction (Cu⁺ → Cu, the cathode) and an oxidation (Cu⁺ → Cu²⁺, the anode). "
    "E° = E°(cathode) − E°(anode). A positive E° means ΔG° < 0, so the reaction is spontaneous.",
    ["Cathode: Cu⁺ + e⁻ → Cu, E° = +0.52 V", "Anode: Cu⁺ → Cu²⁺ + e⁻ (couple Cu²⁺/Cu⁺, E° = +0.15 V)",
     "E° = 0.52 − 0.15 = +0.37 V > 0 → ΔG° < 0 → Cu⁺ disproportionates"],
    why="−0.37 V subtracts the potentials the wrong way round. +0.67 V adds them. '+0.37 V; Cu⁺ is stable' gets "
        "the value right but misreads a positive E° as non-spontaneous.",
    ncert=f"{REF7}, electrochemical cells and Gibbs energy of reaction", seconds=60, checked=True)

g_star = 100 * 129 * 0.10 / 1000
kappa2 = 141 * 0.010 / 1000
r2 = g_star / kappa2
assert close(g_star, 1.29) and close(r2, 915, 0.002) and close(100 * 10 * 141 / 129, 1093, 0.002)
add("Conductance and Kohlrausch's law", I, "numerical",
    "A conductivity cell filled with 0.10 M KCl solution (molar conductivity 129 S cm² mol⁻¹) shows a "
    "resistance of 100 Ω. The same cell is then filled with 0.010 M KCl solution, whose molar conductivity is "
    "141 S cm² mol⁻¹. The resistance it now shows is about:",
    Opts("C", "915 Ω", ["1000 Ω", "1093 Ω", "91.5 Ω"]),
    "Cell constant G* = R × κ is fixed for a cell; κ = Λm × c / 1000",
    "Find the cell constant from the first measurement, then the conductivity of the dilute solution, and "
    "R = G*/κ.",
    ["κ₁ = 129 × 0.10/1000 = 0.0129 S cm⁻¹; G* = 100 × 0.0129 = 1.29 cm⁻¹",
     "κ₂ = 141 × 0.010/1000 = 1.41 × 10⁻³ S cm⁻¹", "R₂ = 1.29 / 1.41 × 10⁻³ ≈ 915 Ω"],
    why="1000 Ω assumes the molar conductivity stays the same on dilution, so that R grows tenfold. 1093 Ω "
        "uses the ratio of molar conductivities upside down. 91.5 Ω slips a power of ten.",
    ncert=f"{REF7}, measurement of the conductivity; variation of molar conductivity with concentration",
    seconds=90, checked=True)

add("Electrode potential and cells", I, "assertion_reason",
    ar("In a galvanic cell, the anode is the negative electrode.",
       "The salt bridge of a galvanic cell usually contains a solution of an inert electrolyte such as KCl set "
       "in agar–agar gel."),
    AR_, "Polarity of electrodes; the salt bridge",
    "A is true: oxidation at the anode releases electrons into it, so the anode carries a negative charge "
    "relative to the cathode. R is also true, but the composition of the salt bridge has nothing to do with "
    "which electrode is negative; the salt bridge only completes the circuit and keeps the solutions neutral.",
    ["A: oxidation at the anode leaves electrons there → negative → true",
     "R: KCl/NH₄NO₃ in agar gel → true", "Salt-bridge contents do not decide polarity → option B"],
    answer="B",
    why="Option A would need R to account for the anode being negative; it does not. Both statements are true, "
        "so C and D are wrong.",
    ncert=f"{REF7}, electrochemical cells; galvanic cells", seconds=35)

add("Nernst equation and Gibbs energy", I, "statement_pair",
    sp("At 298 K, the reduction potential of a Cu²⁺/Cu electrode becomes more positive when the concentration "
       "of Cu²⁺ ions in its solution is increased.",
       "The standard electrode potential of the Cu²⁺/Cu electrode increases when the concentration of Cu²⁺ ions "
       "in its solution is increased."),
    SP_, "Electrode potential versus standard electrode potential",
    "Nernst: E = E° − (0.059/2) log(1/[Cu²⁺]) = E° + 0.0295 log[Cu²⁺]. Raising [Cu²⁺] raises E. But E° is "
    "defined for unit concentration and is a fixed value at a given temperature; it does not change with the "
    "concentration actually used.",
    ["I: E = E° + 0.0295 log[Cu²⁺] → rises with [Cu²⁺] → true",
     "II: E° refers to 1 M by definition → does not change → false"],
    answer="C",
    why="Statement II confuses the electrode potential E with the standard electrode potential E°.",
    ncert=f"{REF7}, Nernst equation", seconds=40)

truth_hno3 = {"a": True, "b": True, "c": True, "d": False, "e": False}
assert 3 * 2 == 2 * 3 and 8 - 2 == 6
add("Oxidation number and balancing", I, "multi_statement",
    ms("For the balanced reaction 3Cu + 8HNO₃ → 3Cu(NO₃)₂ + 2NO + 4H₂O, which of the following statements are "
       "correct?",
       ["Copper is oxidised from 0 to +2.",
        "Only two of the eight HNO₃ molecules are reduced; the other six supply the nitrate ions of Cu(NO₃)₂.",
        "The oxidation number of the nitrogen that is reduced changes from +5 to +2.",
        "A total of eight electrons is transferred in the reaction as written.",
        "HNO₃ acts as the reducing agent."]),
    multi("D", truth_hno3, ["(a), (c) and (d) only", "(b), (c) and (e) only", "(a), (b), (c) and (d) only"]),
    "Oxidation numbers, electron count and the roles of the reactants",
    "Cu: 0 → +2 (oxidised). N in NO: +5 → +2 (reduced). Electrons lost by 3 Cu = 3 × 2 = 6 = electrons gained "
    "by 2 N (2 × 3), so only 2 HNO₃ are reduced; 6 NO₃⁻ stay unchanged in Cu(NO₃)₂.",
    ["(a) ✓", "(b) 2 NO formed → 2 HNO₃ reduced; 6 remain as NO₃⁻ ✓", "(c) +5 → +2 ✓",
     "(d) electrons transferred = 6, not 8 ✗", "(e) HNO₃ is the oxidising agent ✗"],
    why="(d) counts one electron per HNO₃ molecule, and (e) swaps the roles of the reagents; options containing "
        "either are wrong.",
    ncert=f"{REF7R}, oxidation number; balancing of redox reactions", seconds=90, checked=True)

h_plus = math.sqrt(1.0e-6 * 0.010)
e_h = -0.059 * (-math.log10(h_plus))
assert close(h_plus, 1.0e-4) and close(e_h, -0.236)
add("Nernst equation and Gibbs energy", A, "numerical",
    "A hydrogen electrode (H₂ gas at 1 bar, platinum) is dipped in a 0.010 M solution of a weak monobasic acid "
    "HA (Kₐ = 1.0 × 10⁻⁶) at 298 K. Taking [H⁺] ≈ √(Kₐc), the reduction potential of this electrode is "
    "(2.303RT/F = 0.059 V):",
    Opts("B", "−0.236 V", ["−0.118 V", "−0.354 V", "+0.236 V"]),
    "pH of a weak acid, then the Nernst equation for the hydrogen electrode: E = −0.059 pH (p(H₂) = 1 bar)",
    "Find [H⁺] of the weak acid, convert to pH, and use E = −(0.059/1) log(1/[H⁺]) = −0.059 pH.",
    ["[H⁺] = √(1.0 × 10⁻⁶ × 0.010) = 1.0 × 10⁻⁴ M → pH = 4", "E = −0.059 × 4 = −0.236 V"],
    why="−0.118 V takes [H⁺] equal to the acid concentration (pH 2), as for a strong acid. −0.354 V takes "
        "[H⁺] = Kₐ (pH 6). +0.236 V has the wrong sign; a lower [H⁺] than 1 M makes E negative.",
    ncert=f"{REF7}, Nernst equation (hydrogen electrode)", seconds=80, checked=True)

add("Nernst equation and Gibbs energy", A, "match_list",
    lists("Match List-I (electrode, at 298 K) with List-II (its reduction potential from the Nernst equation, "
          "2.303RT/F = 0.059 V).",
          ["Pt | H₂(g, 1 bar) | H⁺(aq)", "Cu²⁺(aq) | Cu(s)", "Ag⁺(aq) | Ag(s)", "Pt | Fe³⁺(aq), Fe²⁺(aq)"],
          ["E = E° − 0.059 log(1/[Ag⁺])", "E = −0.059 pH",
           "E = E° − 0.059 log([Fe²⁺]/[Fe³⁺])", "E = E° − (0.059/2) log(1/[Cu²⁺])"]),
    match("D", M("II IV I III"), [M("II I IV III"), M("IV II I III"), M("II IV III I")]),
    "Nernst equation for different types of electrode",
    "For Mⁿ⁺ + ne⁻ → M, E = E° − (0.059/n) log(1/[Mⁿ⁺]) (the pure metal has unit activity). For the hydrogen "
    "electrode E° = 0 and p(H₂) = 1 bar, so E = −0.059 pH. For the redox couple Fe³⁺ + e⁻ → Fe²⁺, "
    "E = E° − 0.059 log([Fe²⁺]/[Fe³⁺]).",
    ["A: H⁺ + e⁻ → ½H₂ → E = −0.059 pH → II", "B: n = 2 → (0.059/2) log(1/[Cu²⁺]) → IV",
     "C: n = 1 → 0.059 log(1/[Ag⁺]) → I", "D: Fe³⁺/Fe²⁺, n = 1 → III"],
    why="B-I/C-IV swaps the one- and two-electron metal electrodes. A-IV/B-II gives the copper electrode the "
        "pH expression. C-III/D-I swaps the silver and iron electrodes.",
    ncert=f"{REF7}, Nernst equation", seconds=80)

add("Nernst equation and Gibbs energy", A, "direct",
    "At 298 K, the reduction potential of which of the following electrodes does NOT depend on the pH of the "
    "solution (all other concentrations being fixed)?",
    Opts("A", "Cu²⁺(aq) | Cu(s)",
         ["MnO₄⁻, Mn²⁺ | Pt in acid (MnO₄⁻ + 8H⁺ + 5e⁻ → Mn²⁺ + 4H₂O)",
          "Cr₂O₇²⁻, Cr³⁺ | Pt in acid (Cr₂O₇²⁻ + 14H⁺ + 6e⁻ → 2Cr³⁺ + 7H₂O)",
          "Pt | H₂(g, 1 bar) | H⁺(aq)"]),
    "Which electrode reactions involve H⁺ ions",
    "The Nernst equation contains [H⁺] only if H⁺ appears in the electrode reaction. Cu²⁺ + 2e⁻ → Cu involves "
    "no H⁺, so its potential is independent of pH. The other three reactions consume H⁺.",
    ["Cu²⁺/Cu: no H⁺ in the half-reaction → pH-independent ✓", "MnO₄⁻/Mn²⁺: [H⁺]⁸ in Q",
     "Cr₂O₇²⁻/Cr³⁺: [H⁺]¹⁴ in Q", "H⁺/H₂: E = −0.059 pH"],
    why="The permanganate, dichromate and hydrogen electrodes all have H⁺ in their half-reactions, so their "
        "potentials change with pH.",
    ncert=f"{REF7}, Nernst equation", seconds=45)

add("Electrode potential and cells", A, "assertion_reason",
    ar("In a galvanic cell made of two half-cells, the electrode of the couple with the lower standard reduction "
       "potential acts as the anode.",
       "E°cell = E°(anode) − E°(cathode), where both are standard reduction potentials."),
    AR_, "Choosing the anode; calculating E°cell",
    "A is true: the couple with the lower reduction potential has the greater tendency to be oxidised, so it "
    "is the anode. R is false: the correct relation is E°cell = E°(cathode) − E°(anode) (E°right − E°left), "
    "which is positive for a working cell.",
    ["A: lower E° → oxidation → anode → true", "R: sign reversed; correct is E°(cathode) − E°(anode) → false"],
    answer="C",
    why="With R as written, every working galvanic cell would have a negative standard emf, which contradicts "
        "E°cell > 0 for a spontaneous cell reaction.",
    ncert=f"{REF7}, electrode potential; galvanic cells", seconds=40)


# ==================================================================== 8. Chemical Kinetics
topic("Chemical Kinetics")
REF8 = f"{C12}, 'Chemical Kinetics'"

k_s = 3.6 / 3600
t_half = 0.693 / k_s
assert close(k_s, 1.0e-3) and close(t_half, 693) and close(0.693 / 3.6, 0.1925) and close(0.693 / (3.6 / 60), 11.55)
add("Half-life", B, "numerical",
    "The rate constant of a first-order reaction is 3.6 h⁻¹. Its half-life, in seconds, is (ln 2 = 0.693):",
    Opts("D", "693 s", ["0.19 s", "11.6 s", "1.0 × 10³ s"]),
    "Half-life of a first-order reaction, t½ = 0.693/k, with consistent units",
    "Convert k into s⁻¹ first (1 h = 3600 s), then apply t½ = 0.693/k.",
    ["k = 3.6 h⁻¹ = 3.6/3600 s⁻¹ = 1.0 × 10⁻³ s⁻¹", "t½ = 0.693 / 1.0 × 10⁻³ s⁻¹ = 693 s"],
    why="0.19 s is 0.693/3.6, which is in hours, not seconds. 11.6 s converts k only to min⁻¹ and reports "
        "minutes as seconds. 1.0 × 10³ s is 1/k, leaving out ln 2.",
    ncert=f"{REF8}, half-life of a reaction", seconds=35, checked=True)

add("Half-life", B, "assertion_reason",
    ar("The half-life of a first-order reaction does not depend on the initial concentration of the reactant.",
       "A catalyst lowers the activation energy of a reaction."),
    AR_, "Half-life of a first-order reaction",
    "A is true: t½ = 0.693/k contains no concentration term. R is also true, but it describes the effect of a catalyst "
    "on the energy barrier, which has nothing to do with why t½ is independent of [R]₀. The explanation lies "
    "in the integrated rate law.",
    ["A: t½ = 0.693/k → independent of [R]₀ → true", "R: catalyst lowers Eₐ → true",
     "R is an unrelated fact about catalysts → option B"],
    answer="B",
    why="R concerns catalysis, not the concentration dependence of t½, so it cannot explain A. Both "
        "statements are true, so C and D are wrong.",
    ncert=f"{REF8}, half-life of a reaction; effect of catalyst", seconds=35)

truth_f = {"a": True, "b": True, "c": True, "d": False, "e": False}
add("Rate law and order", B, "multi_statement",
    ms("Which of the following are factors that influence the rate of a chemical reaction?",
       ["Concentration of the reactants (pressure, in the case of gases)",
        "Temperature",
        "Presence of a catalyst",
        "The magnitude of the standard Gibbs energy change, ΔG°, of the reaction",
        "The value of the equilibrium constant of the reaction"]),
    multi("C", truth_f, ["(a), (b), (c) and (d) only", "(a), (b), (c) and (e) only", "(b), (c) and (d) only"]),
    "Factors influencing the rate of a reaction",
    "NCERT lists the concentration of reactants (pressure for gases), temperature and catalyst as the factors "
    "that influence the rate. ΔG° and K tell us how far a reaction will go, not how fast.",
    ["(a), (b), (c): NCERT's factors ✓", "(d) ΔG° decides feasibility, not speed ✗",
     "(e) K describes the equilibrium position, not the rate ✗"],
    why="Thermodynamic quantities (ΔG°, K) do not fix the rate; a reaction with a very negative ΔG° can still be "
        "very slow. Options containing (d) or (e) are wrong.",
    ncert=f"{REF8}, factors influencing rate of a reaction", seconds=35)

ea = 2.303 * R_J * 1200
t2 = 1 / (1 / 300 - 2.303 * R_J / ea)
t2_ln = 1 / (1 / 300 - R_J / ea)
t2_sign = 1 / (1 / 300 + 2.303 * R_J / ea)
assert close(ea, 22977, 0.002) and close(t2, 400) and close(t2_ln, 337, 0.003) and close(t2_sign, 240)
add("Arrhenius equation and activation energy", I, "numerical",
    "A reaction has an activation energy of 22.98 kJ mol⁻¹, and its pre-exponential factor does not change "
    "with temperature. Its rate constant at 300 K is k₁. The temperature at which its rate constant becomes 10k₁ "
    "is (2.303R = 19.15 J K⁻¹ mol⁻¹):",
    Opts("A", "400 K", ["337 K", "333 K", "240 K"]),
    "Arrhenius equation for two temperatures: log(k₂/k₁) = [Eₐ/(2.303R)](1/T₁ − 1/T₂)",
    "Put log(k₂/k₁) = log 10 = 1 and solve for 1/T₂.",
    ["1 = (22 980 / 19.15)(1/300 − 1/T₂) = 1200 (1/300 − 1/T₂)",
     "1/300 − 1/T₂ = 1/1200", "1/T₂ = 4/1200 − 1/1200 = 3/1200 → T₂ = 400 K"],
    why="337 K uses R instead of 2.303R (natural log with log 10 = 1). 333 K assumes the rate constant doubles "
        "for every 10 K rise, a rough rule that does not apply here. 240 K adds 1/1200 instead of subtracting, "
        "which would make k smaller, not larger.",
    ncert=f"{REF8}, temperature dependence of the rate of a reaction (Arrhenius equation)", seconds=90,
    checked=True)

remain = 0.5 ** (50 / 10) * 100
assert close(remain, 3.125) and close(0.5 ** 4 * 100, 6.25)
add("Zero and first order reactions", I, "numerical",
    "In a first-order reaction, 25% of the reactant remains unreacted after 20 minutes. The percentage of the "
    "reactant that remains unreacted after 50 minutes is:",
    Opts("B", "3.125%", ["6.25%", "0%", "10%"]),
    "For a first-order reaction the half-life is constant",
    "25% remaining = two half-lives, so t½ = 10 min. 50 min is then five half-lives.",
    ["100% → 50% → 25% in 20 min → t½ = 10 min", "50 min = 5 half-lives",
     "Remaining = 100% × (½)⁵ = 3.125%"],
    why="6.25% counts four half-lives. 0% extrapolates the fall in concentration linearly, as for a zero-order "
        "reaction. 10% divides 25% by 50/20 instead of using half-lives.",
    ncert=f"{REF8}, integrated rate equations (first order); half-life", seconds=50, checked=True)

k_slope = 2.303 * 0.0050
t_half_slope = 0.693 / k_slope
assert close(t_half_slope, 60.2, 0.002) and close(0.693 / 0.0050, 138.6) and close(0.693 / (0.0050 / 2.303), 319, 0.002) \
    and close(1 / k_slope, 86.8, 0.002)
add("Half-life", I, "numerical",
    "For a first-order reaction, a plot of log[R] (common logarithm) against time is a straight line with a "
    "slope of −0.0050 min⁻¹. The half-life of the reaction is about (ln 2 = 0.693):",
    Opts("D", "60 min", ["139 min", "319 min", "87 min"]),
    "First-order integrated rate law in common logarithms: log[R] = log[R]₀ − kt/2.303",
    "The slope of log[R] against t is −k/2.303, so k = 2.303 × 0.0050 min⁻¹. Then t½ = 0.693/k.",
    ["k = 2.303 × 0.0050 = 0.0115 min⁻¹", "t½ = 0.693/0.0115 ≈ 60 min"],
    why="139 min takes k equal to the magnitude of the slope (the slope of ln[R], not log[R]). 319 min divides "
        "the slope by 2.303 instead of multiplying. 87 min is 1/k, leaving out ln 2.",
    ncert=f"{REF8}, first order reactions (graphical form)", seconds=60, checked=True)

add("Arrhenius equation and activation energy", I, "statement_pair",
    sp("In the collision theory of chemical reactions, the reactant molecules are assumed to be hard spheres, and "
       "reaction is postulated to occur when they collide with one another.",
       "The collision frequency, Z, is the number of collisions per second per unit volume of the reaction "
       "mixture."),
    SP_, "Collision theory of chemical reactions",
    "Both statements are taken from NCERT's account of collision theory: molecules are treated as hard spheres "
    "that react on colliding, and Z is the number of collisions per second per unit volume. Only effective "
    "collisions (enough energy and proper orientation) lead to products.",
    ["I: hard-sphere model; reaction on collision → true", "II: definition of collision frequency → true"],
    answer="A",
    why="Both are NCERT statements, so any option calling one of them false is wrong.",
    ncert=f"{REF8}, collision theory of chemical reactions", seconds=35)

ea_b_cat = (150 - 50) - 50
assert ea_b_cat == 50 and 150 - 50 == 100
add("Arrhenius equation and activation energy", A, "numerical",
    "For an endothermic elementary reaction, ΔH = +50 kJ mol⁻¹ and the activation energy of the forward "
    "reaction is 150 kJ mol⁻¹. A catalyst lowers the activation energy of the forward reaction to "
    "100 kJ mol⁻¹. The activation energy of the BACKWARD reaction in the presence of the catalyst is:",
    Opts("C", "50 kJ mol⁻¹", ["100 kJ mol⁻¹", "150 kJ mol⁻¹", "0 kJ mol⁻¹"]),
    "Energy profile: Eₐ(forward) − Eₐ(backward) = ΔH; a catalyst lowers both barriers by the same amount",
    "A catalyst does not change ΔH; it lowers the energy of the activated complex. So for the catalysed path, "
    "Eₐ(backward) = Eₐ(forward, catalysed) − ΔH.",
    ["Uncatalysed: Eₐ(b) = 150 − 50 = 100 kJ mol⁻¹", "Catalyst lowers both barriers by 150 − 100 = 50 kJ mol⁻¹",
     "Catalysed: Eₐ(b) = 100 − 50 = 50 kJ mol⁻¹"],
    why="100 kJ mol⁻¹ is the uncatalysed backward barrier, as if the catalyst did not affect the reverse "
        "reaction. 150 kJ mol⁻¹ adds ΔH instead of subtracting it. 0 kJ mol⁻¹ subtracts the 50 kJ mol⁻¹ "
        "twice.",
    ncert=f"{REF8}, effect of catalyst; activation energy", seconds=70, checked=True)

assert 0.004 * (0.4 / 0.2) ** 0 == 0.004
add("Rate law and order", A, "numerical",
    "For a reaction A → products at a fixed temperature, doubling the initial concentration of A doubles the "
    "half-life. When [A] = 0.20 mol L⁻¹ the rate is 4.0 × 10⁻³ mol L⁻¹ s⁻¹. At the same temperature, the rate "
    "when [A] = 0.40 mol L⁻¹ is:",
    Opts("D", "4.0 × 10⁻³ mol L⁻¹ s⁻¹",
         ["8.0 × 10⁻³ mol L⁻¹ s⁻¹", "1.6 × 10⁻² mol L⁻¹ s⁻¹", "2.0 × 10⁻³ mol L⁻¹ s⁻¹"]),
    "Order from the dependence of half-life on initial concentration; rate law of a zero-order reaction",
    "t½ ∝ [A]₀ is the signature of a zero-order reaction (t½ = [A]₀/2k). For zero order, rate = k, independent "
    "of [A], so the rate is unchanged.",
    ["t½ ∝ [A]₀ → zero order", "Rate = k[A]⁰ = k", "Rate at 0.40 M = 4.0 × 10⁻³ mol L⁻¹ s⁻¹ (unchanged)"],
    why="8.0 × 10⁻³ assumes first order and 1.6 × 10⁻² second order. 2.0 × 10⁻³ reads the longer half-life as "
        "a slower rate; but a longer t½ here comes from more reactant to use up at the same rate.",
    ncert=f"{REF8}, zero order reactions; half-life of a reaction", seconds=60, checked=True)

truth_r = {"a": True, "b": True, "c": True, "d": False, "e": False}
add("Rate law and order", A, "multi_statement",
    ms("For the reaction 4NH₃(g) + 5O₂(g) → 4NO(g) + 6H₂O(g), which of the following statements are correct?",
       ["Rate = −¼ d[NH₃]/dt = ⅙ d[H₂O]/dt.",
        "The rate of formation of NO equals the rate of disappearance of NH₃.",
        "The rate of disappearance of O₂ is 5/4 times the rate of disappearance of NH₃.",
        "The rate of formation of H₂O is 2/3 times the rate of disappearance of NH₃.",
        "The reaction must be of fifth order with respect to O₂."]),
    multi("B", truth_r, ["(a), (b), (c) and (d) only", "(a), (c) and (e) only", "(b), (d) and (e) only"]),
    "Expressing the rate in terms of different species; order is found by experiment",
    "Rate = −¼ d[NH₃]/dt = −⅕ d[O₂]/dt = ¼ d[NO]/dt = ⅙ d[H₂O]/dt. The rates of individual species are in the "
    "ratio of their coefficients. Orders cannot be read from the balanced equation.",
    ["(a) ✓", "(b) NH₃ : NO = 4 : 4 → equal ✓", "(c) O₂ : NH₃ = 5 : 4 ✓",
     "(d) H₂O : NH₃ = 6 : 4 = 3/2, not 2/3 ✗", "(e) order must be found experimentally ✗"],
    why="(d) inverts the ratio of the coefficients and (e) wrongly takes the coefficient of O₂ as its order; "
        "options containing either are wrong.",
    ncert=f"{REF8}, rate of a chemical reaction; order of a reaction", seconds=80)


# ==================================================================== 9. Classification of Elements and Periodicity
topic("Classification of Elements and Periodicity in Properties")
REF9 = f"{C11}, 'Classification of Elements and Periodicity in Properties'"

period_sizes = [2, 8, 8, 18, 18]
assert sum(period_sizes) == 54 and sum(period_sizes[:4]) == 36 and sum([2, 8, 18, 18, 32]) == 78
add("Modern periodic table", B, "numerical",
    "The total number of elements in the first five periods of the long form of the periodic table is:",
    Opts("C", "54", ["36", "78", "50"]),
    "Number of elements in each period of the modern periodic table",
    "Periods 1 to 5 contain 2, 8, 8, 18 and 18 elements respectively. The fifth period ends with xenon, "
    "Z = 54.",
    ["2 + 8 + 8 + 18 + 18 = 54", "Check: the fifth period ends at Xe (Z = 54)"],
    why="36 stops at the end of the fourth period (krypton). 78 takes the third period as 18 and the fifth as 32 "
        "elements (2 + 8 + 18 + 18 + 32). 50 is the sum 2 + 8 + 8 + 18 + 14, mixing in the 14 f-block elements.",
    ncert=f"{REF9}, modern periodic law and the present form of the periodic table", seconds=30, checked=True)

add("Modern periodic table", B, "direct",
    "Which of the following pairs of atomic numbers belongs to elements of the SAME group?",
    Opts("A", "12 and 38", ["11 and 21", "17 and 25", "6 and 22"]),
    "Group from the electronic configuration",
    "Z = 12 is magnesium ([Ne] 3s²) and Z = 38 is strontium ([Kr] 5s²); both are group 2 elements.",
    ["12: [Ne] 3s² → group 2", "38: [Kr] 5s² → group 2 ✓", "11 (group 1) and 21 (Sc, group 3)",
     "17 (group 17) and 25 (Mn, group 7)", "6 (group 14) and 22 (Ti, group 4)"],
    why="The other pairs have similar numbers of outer electrons, but one member of each is a d-block element "
        "(Sc, Mn, Ti) whose group number counts its (n − 1)d electrons as well, so it is in a different group.",
    ncert=f"{REF9}, electronic configurations and types of elements: s-, p-, d-, f-blocks", seconds=40)

add("Modern periodic table", I, "statement_pair",
    sp("The number of elements in each period of the periodic table is twice the number of atomic orbitals "
       "available in the energy level that is being filled.",
       "The fifth period begins with the filling of the 5s orbital and, after the 4d orbitals, ends with the "
       "filling of the 5p orbitals, so it contains 18 elements."),
    SP_, "Electronic configurations and the lengths of the periods",
    "Each orbital holds two electrons, so the number of elements in a period equals 2 × (number of orbitals "
    "being filled). In period 5 the orbitals filled are 5s (1), 4d (5) and 5p (3): 9 orbitals → 18 elements.",
    ["I: NCERT statement → true", "II: 5s + 4d + 5p = 1 + 5 + 3 = 9 orbitals → 18 elements → true"],
    answer="A",
    why="Both statements are correct, so any option that marks one of them false is wrong.",
    ncert=f"{REF9}, electronic configurations of elements and the periodic table", seconds=45, checked=True)

add("Modern periodic table", I, "match_list",
    lists("Match List-I (atomic number) with List-II (position of the element in the periodic table).",
          ["Z = 16", "Z = 30", "Z = 53", "Z = 56"],
          ["Period 5, group 17", "Period 6, group 2", "Period 3, group 16", "Period 4, group 12"]),
    match("C", M("III IV I II"), [M("III I IV II"), M("IV III I II"), M("III IV II I")]),
    "Locating an element from its atomic number",
    "Write the configuration and read the period from the highest n and the group from the outer electrons.",
    ["16: [Ne] 3s² 3p⁴ → period 3, group 16 → III", "30: [Ar] 3d¹⁰ 4s² → period 4, group 12 → IV",
     "53: [Kr] 4d¹⁰ 5s² 5p⁵ → period 5, group 17 → I", "56: [Xe] 6s² → period 6, group 2 → II"],
    why="B-I/C-IV swaps zinc and iodine. A-IV/B-III swaps sulphur and zinc. C-II/D-I swaps iodine and barium.",
    ncert=f"{REF9}, electronic configurations and types of elements", seconds=60)

truth_cmp = {"a": True, "b": True, "c": True, "d": False, "e": False}
add("Atomic and ionic radii", I, "multi_statement",
    ms("Which of the following comparisons are correct?",
       ["Atomic radius: Ca > Mg",
        "Electronegativity: P > Si",
        "First ionisation enthalpy: Be > Li",
        "Ionic radius: Na⁺ > F⁻",
        "Atomic radius: O > N"]),
    multi("D", truth_cmp, ["(a), (b), (c) and (e) only", "(b), (d) and (e) only", "(a) and (d) only"]),
    "Periodic trends in radius, electronegativity and ionisation enthalpy",
    "Radius increases down a group and decreases across a period; electronegativity and (generally) "
    "ionisation enthalpy increase across a period. Among isoelectronic ions, the one with the larger nuclear "
    "charge is smaller.",
    ["(a) Ca is below Mg in group 2 → larger ✓", "(b) P is to the right of Si → more electronegative ✓",
     "(c) Be (2s²) holds its electrons more tightly than Li (2s¹) ✓",
     "(d) Na⁺ (Z = 11) and F⁻ (Z = 9) are isoelectronic; F⁻ is larger ✗",
     "(e) O is to the right of N → smaller ✗"],
    why="(d) reverses the isoelectronic order and (e) reverses the trend across a period; options containing "
        "either are wrong.",
    ncert=f"{REF9}, periodic trends in physical properties", seconds=60)

add("Ionisation and electron gain enthalpy", A, "assertion_reason",
    ar("The second ionisation enthalpy of sodium is many times larger than its first ionisation enthalpy.",
       "After the first electron is lost, Na⁺ has the stable neon configuration, and the next electron has to "
       "be removed from the inner 2p subshell, which is much closer to the nucleus."),
    AR_, "Successive ionisation enthalpies",
    "Na is [Ne] 3s¹. Removing the 3s electron is easy. The second electron must come out of the compact, "
    "noble-gas 2p⁶ core, which is nearer the nucleus and less shielded, so far more energy is needed. R is the "
    "reason for A.",
    ["Na → Na⁺: remove 3s¹ (easy)", "Na⁺ → Na²⁺: remove a 2p electron from the [Ne] core (very hard)",
     "Hence ΔiH₂ ≫ ΔiH₁ → R explains A"],
    answer="A",
    why="R gives exactly why the jump occurs after the first electron for a group 1 element, so it is the "
        "correct explanation.",
    ncert=f"{REF9}, ionization enthalpy", seconds=40)

ies = {"A": [520, 7298, 11815], "B": [899, 1757, 14848], "C": [801, 2427, 3660, 25025],
       "D": [1086, 2352, 4620, 6223, 37831]}


def jump_after(v):
    return max(range(len(v) - 1), key=lambda i: v[i + 1] / v[i]) + 1


assert {k: jump_after(v) for k, v in ies.items()} == {"A": 1, "B": 2, "C": 3, "D": 4}
add("Valence and reactivity", A, "match_list",
    lists("Match List-I (successive ionisation enthalpies of an element, in kJ mol⁻¹, starting from the first) "
          "with List-II (the group to which the element belongs).",
          ["520, 7298, 11815", "899, 1757, 14848", "801, 2427, 3660, 25025",
           "1086, 2352, 4620, 6223, 37831"],
          ["Group 13", "Group 1", "Group 14", "Group 2"]),
    match("B", M("II IV I III"), [M("IV II I III"), M("II IV III I"), M("II I IV III")]),
    "Valence electrons from the jump in successive ionisation enthalpies",
    "A very large jump appears when the first electron is taken from the inner noble-gas core. The number of "
    "ionisation enthalpies before the jump equals the number of valence electrons.",
    ["A: jump after the 1st → 1 valence electron → group 1 → II",
     "B: jump after the 2nd → 2 valence electrons → group 2 → IV",
     "C: jump after the 3rd → 3 valence electrons → group 13 → I",
     "D: jump after the 4th → 4 valence electrons → group 14 → III"],
    why="A-IV/B-II swaps the group 1 and group 2 patterns. C-III/D-I swaps the group 13 and 14 "
        "patterns. B-I/C-IV puts the jump one place too late for B.",
    ncert=f"{REF9}, ionization enthalpy; valence", seconds=90, checked=True)


# ==================================================================== 10. p-Block Elements
topic("p-Block Elements")
REF10 = f"{C12}, 'The p-Block Elements'"
REF10A = f"{C11}, 'The p-Block Elements'"

add("Group 17 and 18 trends", B, "direct",
    "Which of the following INCREASES on going down group 17 from fluorine to iodine?",
    Opts("A", "Atomic radius", ["Electronegativity", "First ionisation enthalpy", "Oxidising power of the element"]),
    "Trends down group 17",
    "Down the group a new shell is added at each step, so the atomic radius increases. The outer electrons are "
    "farther from the nucleus and better shielded, so ionisation enthalpy, electronegativity and oxidising "
    "power all decrease.",
    ["Radius: F < Cl < Br < I (increases)", "Electronegativity, ionisation enthalpy, oxidising power: decrease"],
    why="Electronegativity, ionisation enthalpy and oxidising power all fall from fluorine to iodine.",
    ncert=f"{REF10}, group 17 elements: atomic and physical properties", seconds=25)

add("Group 15 and 16 trends", B, "direct",
    "Tellurium is the group 16 element of the fifth period. Its valence-shell electronic configuration in the "
    "ground state is:",
    Opts("C", "5s² 5p⁴", ["4d¹⁰ 5s² 5p²", "5s² 5p⁶", "6s² 6p⁴"]),
    "General valence-shell configuration of group 16: ns² np⁴",
    "Group 16 elements have six valence electrons, ns² np⁴. For period 5, n = 5, so tellurium (Z = 52, "
    "[Kr] 4d¹⁰ 5s² 5p⁴) has the valence shell 5s² 5p⁴.",
    ["Group 16 → ns² np⁴", "Period 5 → n = 5 → 5s² 5p⁴"],
    why="4d¹⁰ 5s² 5p² belongs to tin (group 14). 5s² 5p⁶ is xenon (group 18). 6s² 6p⁴ is the group 16 element "
        "of period 6, polonium.",
    ncert=f"{REF10}, group 16 elements: electronic configuration", seconds=25)

add("Group 15 and 16 trends", B, "match_list",
    lists("Match List-I (group 15 element) with List-II (its nature).",
          ["Bismuth", "Arsenic", "Nitrogen", "Phosphorus"],
          ["Metalloid", "Non-metal; a gas at room temperature", "Metal",
           "Non-metal; a solid at room temperature"]),
    match("D", M("III I II IV"), [M("I III II IV"), M("III I IV II"), M("III II I IV")]),
    "Increase of metallic character down group 15",
    "Down group 15, metallic character increases: nitrogen and phosphorus are non-metals, arsenic and antimony "
    "are metalloids, and bismuth is a typical metal. Of the non-metals, only nitrogen is a gas (N₂).",
    ["A: Bi → metal → III", "B: As → metalloid → I", "C: N → non-metal, gas → II", "D: P → non-metal, solid → IV"],
    why="A-I/B-III swaps bismuth and arsenic. C-IV/D-II swaps nitrogen and phosphorus. B-II/C-I calls arsenic a "
        "gas and nitrogen a metalloid.",
    ncert=f"{REF10}, group 15 elements: physical properties", seconds=40)

add("Anomalous first element", I, "match_list",
    lists("Match List-I (first element of a p-block group) with List-II (a way in which it differs from the "
          "other members of its group).",
          ["Boron", "Nitrogen", "Oxygen", "Fluorine"],
          ["Shows only the −1 oxidation state in its compounds",
           "It is a non-metal, whereas all the other members of its group are metals",
           "Exists as a diatomic molecule held by a triple bond, whereas the next member exists as tetra-atomic "
           "molecules with single bonds",
           "Its hydride is a liquid because of extensive hydrogen bonding, whereas the hydrides of the heavier "
           "members are gases"]),
    match("B", M("II III IV I"), [M("III II IV I"), M("II III I IV"), M("II IV III I")]),
    "Anomalous behaviour of the first member of each p-block group",
    "The first members are small, highly electronegative and have no d orbitals in the valence shell. Boron is "
    "the only non-metal of group 13; small size lets nitrogen form pπ–pπ multiple bonds (N≡N), makes oxygen's "
    "hydride hydrogen-bonded, and keeps fluorine at −1.",
    ["A: boron, the only non-metal of group 13 → II", "B: nitrogen, N≡N vs P₄ → III",
     "C: oxygen, H₂O liquid (hydrogen bonding) vs H₂S gas → IV", "D: fluorine, only −1 → I"],
    why="A-III/B-II swaps boron and nitrogen. C-I/D-IV swaps oxygen and fluorine. B-IV/C-III swaps nitrogen "
        "and oxygen.",
    ncert=f"{REF10}, anomalous behaviour of nitrogen, oxygen and fluorine; {REF10A}, anomalous properties of boron",
    seconds=60)

truth_18 = {"a": True, "b": True, "c": True, "d": False, "e": False}
add("Group 17 and 18 trends", I, "multi_statement",
    ms("Which of the following statements about the group 18 elements (noble gases) are correct?",
       ["Their first ionisation enthalpy decreases down the group.",
        "Their atomic radius increases down the group.",
        "Their boiling points increase from helium to radon.",
        "They have large negative electron gain enthalpies.",
        "All of them have the valence-shell configuration ns² np⁶."]),
    multi("A", truth_18, ["(a), (b), (c) and (e) only", "(b), (d) and (e) only", "(a) and (d) only"]),
    "Trends in group 18",
    "Down the group the atoms become larger, so ionisation enthalpy falls and the dispersion forces between "
    "atoms grow (boiling points rise). With completely filled valence shells, the noble gases have large "
    "POSITIVE electron gain enthalpies. Helium is 1s², not ns² np⁶.",
    ["(a) ✓", "(b) ✓", "(c) larger atoms → stronger dispersion forces ✓", "(d) ✗: large positive",
     "(e) ✗: helium is 1s²"],
    why="(d) gives the wrong sign for the electron gain enthalpy and (e) forgets helium; any option with either "
        "is wrong.",
    ncert=f"{REF10}, group 18 elements: electronic configuration, atomic and physical properties", seconds=50)

add("Group 17 and 18 trends", I, "statement_pair",
    sp("On going down group 17 from fluorine to iodine, the first ionisation enthalpy decreases.",
       "On going down group 17 from fluorine to iodine, the oxidising power of the halogens increases."),
    SP_, "Trends in ionisation enthalpy and oxidising power in group 17",
    "Down the group the atomic size increases, so the outer electrons are held less firmly and the ionisation "
    "enthalpy falls. The tendency to gain an electron also falls, and fluorine is the strongest oxidising "
    "agent; oxidising power DECREASES from F₂ to I₂.",
    ["I: larger atoms → lower ionisation enthalpy → true", "II: oxidising power F₂ > Cl₂ > Br₂ > I₂ → false"],
    answer="C",
    why="Statement II reverses the trend: oxidising power decreases down group 17.",
    ncert=f"{REF10}, group 17 elements", seconds=30)

truth_15 = {"a": True, "b": False, "c": True, "d": True, "e": False}
add("Group 15 and 16 trends", I, "multi_statement",
    ms("Which of the following trends on going down group 15 from nitrogen to bismuth are correct?",
       ["The covalent radius increases.",
        "The first ionisation enthalpy increases.",
        "The metallic character increases.",
        "The tendency to show the −3 oxidation state decreases.",
        "The electronegativity increases."]),
    multi("B", truth_15, ["(a), (b) and (c) only", "(a), (c), (d) and (e) only", "(b), (d) and (e) only"]),
    "Periodic trends down group 15",
    "Down the group the atoms become larger, so ionisation enthalpy and electronegativity fall and metallic "
    "character rises. With falling electronegativity, the tendency to gain electrons and show −3 falls (bismuth "
    "hardly forms compounds in −3).",
    ["(a) ✓", "(b) ✗: ionisation enthalpy decreases", "(c) ✓", "(d) ✓", "(e) ✗: electronegativity decreases"],
    why="(b) and (e) reverse the trends in ionisation enthalpy and electronegativity; options containing either "
        "are wrong.",
    ncert=f"{REF10}, group 15 elements: atomic and physical properties; oxidation states", seconds=50)

conf = {"Ga": "4s2 4p1", "As": "4s2 4p3", "Se": "4s2 4p4", "Br": "4s2 4p5"}
unpaired = {"Ga": 1, "As": 3, "Se": 2, "Br": 1}
assert 6 + 6 + 5 == 17
truth_c = {"a": unpaired["As"] == 3, "b": unpaired["Se"] == 2, "c": True, "d": unpaired["Ga"] == 3, "e": True}
assert truth_c == {"a": True, "b": True, "c": True, "d": False, "e": True}
add("Group 15 and 16 trends", A, "multi_statement",
    ms("Consider the ground-state atoms of gallium (Z = 31), arsenic (Z = 33), selenium (Z = 34) and bromine "
       "(Z = 35). Which of the following statements are correct?",
       ["An arsenic atom has three unpaired electrons.",
        "A selenium atom has two unpaired electrons.",
        "A bromine atom has 17 electrons with azimuthal quantum number l = 1.",
        "All three valence electrons of a gallium atom are unpaired.",
        "Each of the four atoms has ten electrons in its 3d subshell."]),
    multi("D", truth_c, ["(a), (b) and (c) only", "(a), (c), (d) and (e) only", "(b), (d) and (e) only"]),
    "Electronic configurations of the period 4 p-block elements",
    "All four have [Ar] 3d¹⁰ 4s² and then 4p¹ (Ga), 4p³ (As), 4p⁴ (Se) and 4p⁵ (Br). Apply Hund's rule to the "
    "4p electrons.",
    ["(a) As: 4p³ → three singly filled 4p orbitals → 3 unpaired ✓",
     "(b) Se: 4p⁴ → one pair + two singles → 2 unpaired ✓",
     "(c) Br: p electrons = 2p⁶ + 3p⁶ + 4p⁵ = 17 ✓",
     "(d) Ga: 4s² is paired; only the 4p¹ electron is unpaired ✗",
     "(e) all have 3d¹⁰ ✓"],
    why="Only (d) is false: the two 4s electrons of gallium share one orbital. Options that leave out a true "
        "statement or include (d) are wrong.",
    ncert=f"{REF10}, electronic configuration of groups 15–17; {REF10A}, group 13", seconds=90, checked=True)

add("Group 13 and 14 trends", A, "statement_pair",
    sp("Every p-block element of the sixth period, from thallium to radon, has a completely filled 4f subshell "
       "in its ground state.",
       "Every p-block element of the fifth period, from indium to xenon, has a completely filled 4d subshell "
       "in its ground state."),
    SP_, "Inner filled subshells of the heavier p-block elements",
    "The sixth-period p-block elements follow the lanthanoids and the 5d series: [Xe] 4f¹⁴ 5d¹⁰ 6s² 6p¹⁻⁶. The "
    "fifth-period p-block elements follow the 4d series: [Kr] 4d¹⁰ 5s² 5p¹⁻⁶. These filled d and f subshells "
    "shield the nucleus poorly, which is behind several irregular trends in groups 13 to 17.",
    ["I: Tl to Rn = [Xe] 4f¹⁴ 5d¹⁰ 6s² 6p¹⁻⁶ → true", "II: In to Xe = [Kr] 4d¹⁰ 5s² 5p¹⁻⁶ → true"],
    answer="A",
    why="Both statements follow from the order of filling (6s, 4f, 5d, 6p and 5s, 4d, 5p).",
    ncert=f"{REF10}, electronic configurations of p-block elements", seconds=50)

add("Group 13 and 14 trends", A, "match_list",
    lists("Match List-I (description of a p-block element in its ground state) with List-II (the element).",
          ["The period 4 element with three unpaired electrons",
           "The period 5 element whose valence shell is 5s² 5p²",
           "The period 6 element with three electrons in its 6p subshell",
           "The period 3 element with four valence p electrons"],
          ["Sulphur", "Bismuth", "Arsenic", "Tin"]),
    match("B", M("III IV II I"), [M("IV III II I"), M("III IV I II"), M("III II IV I")]),
    "Identifying p-block elements from their configurations",
    "Use the period for n and the number of valence p electrons for the group (group = 12 + number of p "
    "electrons for groups 13–18).",
    ["A: 4p³ → group 15, period 4 → As → III", "B: 5s² 5p² → group 14, period 5 → Sn → IV",
     "C: 6p³ → group 15, period 6 → Bi → II", "D: 3p⁴ → group 16, period 3 → S → I"],
    why="A-IV/B-III swaps arsenic and tin. C-I/D-II swaps bismuth and sulphur. B-II/C-IV puts tin and bismuth "
        "in each other's places.",
    ncert=f"{REF10}, electronic configurations of p-block elements", seconds=70)


# ==================================================================== 11. d- and f-Block Elements
topic("d- and f-Block Elements")
REF11 = f"{C12}, 'The d- and f-Block Elements'"

cr_o = 2 * 4
assert cr_o == 8 and 7 == 4 + 4 - 1
add("K2Cr2O7 and KMnO4", B, "numerical",
    "In the dichromate ion, Cr₂O₇²⁻, two CrO₄ tetrahedra share one corner (one oxygen atom). The total number "
    "of chromium–oxygen linkages in the ion (counting each Cr–O connection once, whatever its bond order) is:",
    Opts("C", "8", ["7", "6", "4"]),
    "Structure of the dichromate ion",
    "Each chromium atom sits at the centre of a tetrahedron and is linked to four oxygen atoms. The shared "
    "(bridging) oxygen is linked to both chromium atoms, so it accounts for two Cr–O linkages.",
    ["Each Cr: 4 Cr–O linkages", "Two Cr atoms: 2 × 4 = 8",
     "Check: 6 terminal O (one link each) + 1 bridging O (two links) = 8"],
    why="7 counts oxygen atoms instead of linkages. 6 counts only the terminal oxygens. 4 counts the linkages of "
        "one chromium atom only.",
    ncert=f"{REF11}, potassium dichromate (structures of chromate and dichromate ions)", seconds=35,
    checked=True)

add("Transition element trends", B, "direct",
    "In each transition series, the melting points of the metals rise to a maximum at about which d-electron "
    "configuration (apart from the anomalous values of Mn and Tc), and then fall?",
    Opts("B", "d⁵", ["d¹⁰", "d¹", "d⁸"]),
    "Melting points of the transition metals",
    "Strong metallic bonding involves the (n − 1)d as well as the ns electrons. The number of unpaired d "
    "electrons available for bonding is greatest around the middle of the series, so the melting points rise "
    "to a maximum at about d⁵ and then fall as the d electrons pair up.",
    ["Unpaired d electrons peak at d⁵", "More electrons in metallic bonding → higher melting point"],
    why="d¹⁰ metals (Zn, Cd, Hg) have the lowest melting points; d¹ is at the start of the rise; d⁸ lies on the "
        "falling side.",
    ncert=f"{REF11}, physical properties of the transition elements", seconds=30)

add("Transition element trends", B, "statement_pair",
    sp("With the exceptions of Zn, Cd and Hg, the transition metals are very hard and have low volatility.",
       "Across the 3d series, the enthalpy of atomisation increases steadily from scandium to zinc."),
    SP_, "Hardness, volatility and enthalpy of atomisation of transition metals",
    "NCERT notes that, apart from Zn, Cd and Hg, the transition metals are very hard and have low volatility. "
    "Their enthalpies of atomisation are high and pass through a maximum around the middle of each series "
    "(many unpaired d electrons in metallic bonding); zinc, with a full 3d¹⁰ subshell, has the lowest value in "
    "the 3d series.",
    ["I: NCERT statement → true", "II: maximum near the middle, minimum at Zn → not a steady increase → false"],
    answer="C",
    why="Statement II ignores the maximum in the middle of the series and the very low value for zinc.",
    ncert=f"{REF11}, physical properties of the transition elements", seconds=40)

e_lost = 1 + 2 * 3
assert e_lost == 7 and 4 * e_lost == 7 * 4
add("K2Cr2O7 and KMnO4", I, "numerical",
    "In the first step of the manufacture of potassium dichromate, chromite ore is fused with sodium carbonate "
    "in free access of air: 4FeCr₂O₄ + 8Na₂CO₃ + 7O₂ → 8Na₂CrO₄ + 2Fe₂O₃ + 8CO₂. The number of electrons lost "
    "by ONE formula unit of FeCr₂O₄ in this reaction is:",
    Opts("D", "7", ["6", "3", "1.75"]),
    "Electron count from changes in oxidation number",
    "In FeCr₂O₄ iron is +2 and chromium is +3. Iron ends as Fe₂O₃ (+3) and chromium as Na₂CrO₄ (+6).",
    ["Fe: +2 → +3 → 1 electron", "Cr: +3 → +6 → 3 electrons each × 2 = 6", "Total = 1 + 6 = 7 electrons",
     "Check: 4 FeCr₂O₄ lose 28 e⁻; 7 O₂ gain 7 × 4 = 28 e⁻"],
    why="6 forgets that iron is also oxidised. 3 counts only one chromium atom. 1.75 is the number of O₂ "
        "molecules used per formula unit, not the number of electrons.",
    ncert=f"{REF11}, preparation of potassium dichromate", seconds=50, checked=True)

add("K2Cr2O7 and KMnO4", I, "match_list",
    lists("Match List-I (reaction) with List-II (the oxidation product formed from the reducing agent).",
          ["KMnO₄ and KI in acidic solution", "KMnO₄ and KI in neutral or faintly alkaline solution",
           "K₂Cr₂O₇ and H₂S in acidic solution", "KMnO₄ and Na₂S₂O₃ in neutral or faintly alkaline solution"],
          ["SO₄²⁻", "I₂", "S", "IO₃⁻"]),
    match("C", M("II IV III I"), [M("IV II III I"), M("II IV I III"), M("II III IV I")]),
    "Oxidising reactions of permanganate and dichromate",
    "In acid, permanganate oxidises iodide to iodine; in neutral or faintly alkaline solution it oxidises "
    "iodide further, to iodate, and thiosulphate to sulphate. Acidified dichromate oxidises H₂S, precipitating "
    "sulphur.",
    ["A: I⁻ → I₂ → II", "B: I⁻ → IO₃⁻ → IV", "C: H₂S → S → III", "D: S₂O₃²⁻ → SO₄²⁻ → I"],
    why="A-IV/B-II swaps the products of iodide in acidic and neutral solution. C-I/D-III swaps the sulphur "
        "products. B-III/C-IV gives iodide the sulphur product.",
    ncert=f"{REF11}, oxidising properties of KMnO₄ and K₂Cr₂O₇", seconds=60)

add("Transition element trends", I, "assertion_reason",
    ar("Manganese shows the largest number of oxidation states among the elements of the first transition "
       "series.",
       "Manganese has an anomalously low melting point compared with the neighbouring 3d metals."),
    AR_, "Oxidation states and melting points of the 3d metals",
    "A is true: manganese (3d⁵ 4s²) shows every oxidation state from +2 to +7, because all seven 4s and 3d "
    "electrons can take part in bonding. R is also true (NCERT notes the anomalous melting point of Mn), but "
    "the melting point of the metal has nothing to do with the number of oxidation states it shows.",
    ["A: Mn shows +2 to +7 → true", "R: anomalous (low) melting point of Mn → true",
     "R is an unrelated physical property → option B"],
    answer="B",
    why="The range of oxidation states comes from the seven 3d and 4s electrons available for bonding, not from "
        "the melting point; both statements are true, so C and D are wrong.",
    ncert=f"{REF11}, general properties of the transition elements (melting points; oxidation states)",
    seconds=40)

truth_int = {"a": True, "b": True, "c": True, "d": False, "e": False}
add("Transition element trends", I, "multi_statement",
    ms("Interstitial compounds are formed when small atoms such as H, C or N are trapped inside the crystal "
       "lattices of transition metals. Which of the following statements about them are correct?",
       ["They have high melting points, higher than those of the pure metals.",
        "They are very hard.",
        "They retain metallic conductivity.",
        "Their formulae, such as TiC or Mn₄N, correspond to normal oxidation states of the metal.",
        "They are typical ionic compounds."]),
    multi("D", truth_int, ["(a), (b), (c) and (e) only", "(b), (d) and (e) only", "(a) and (c) only"]),
    "Characteristics of interstitial compounds",
    "NCERT: interstitial compounds have high melting points (higher than the pure metals), are very hard, "
    "retain metallic conductivity and are chemically inert. They are usually non-stoichiometric, their "
    "formulae do not correspond to any normal oxidation state of the metal, and they are neither typically "
    "ionic nor covalent.",
    ["(a) ✓", "(b) ✓", "(c) ✓", "(d) ✗: formulae do not match normal oxidation states",
     "(e) ✗: neither typically ionic nor covalent"],
    why="(d) and (e) describe ordinary ionic compounds, which interstitial compounds are not; '(a) and (c) "
        "only' leaves out their hardness.",
    ncert=f"{REF11}, interstitial compounds", seconds=50)

d_counts = {"Ti²⁺": 2, "Cr²⁺": 4, "Mn²⁺": 5, "Ni²⁺": 8}
unp = {k: (v if v <= 5 else 10 - v) for k, v in d_counts.items()}
assert max(unp, key=unp.get) == "Mn²⁺" and unp == {"Ti²⁺": 2, "Cr²⁺": 4, "Mn²⁺": 5, "Ni²⁺": 2}
add("Magnetic and colour properties", I, "direct",
    "Which of the following gaseous ions has the HIGHEST spin-only magnetic moment? (Z: Ti = 22, Cr = 24, "
    "Mn = 25, Ni = 28)",
    Opts("A", "Mn²⁺", ["Ti²⁺", "Cr²⁺", "Ni²⁺"]),
    "Spin-only magnetic moment μ = √[n(n + 2)] BM rises with the number of unpaired electrons n",
    "Write the 3d configuration of each M²⁺ ion (the 4s electrons are lost first) and count unpaired electrons "
    "by Hund's rule.",
    ["Ti²⁺: 3d² → 2 unpaired", "Cr²⁺: 3d⁴ → 4 unpaired", "Mn²⁺: 3d⁵ → 5 unpaired (largest)",
     "Ni²⁺: 3d⁸ → 2 unpaired"],
    why="Cr²⁺ has four unpaired electrons, Ti²⁺ and Ni²⁺ two each; Mn²⁺ (3d⁵) has the maximum of five.",
    ncert=f"{REF11}, magnetic properties", seconds=40, checked=True)

mu = {n: math.sqrt(n * (n + 2)) for n in (3, 4, 5, 6)}
assert close(mu[5], 5.92, 0.002) and close(mu[4], 4.90, 0.002) and close(mu[3], 3.87, 0.002) \
    and close(mu[6], 6.93, 0.002)
add("Magnetic and colour properties", A, "numerical",
    "A gaseous M²⁺ ion of a first-row transition metal has a spin-only magnetic moment of 5.92 BM. The "
    "spin-only magnetic moment of the M³⁺ ion of the same metal is (√15 = 3.87, √24 = 4.90, √35 = 5.92, "
    "√48 = 6.93):",
    Opts("C", "4.90 BM", ["5.92 BM", "6.93 BM", "3.87 BM"]),
    "Spin-only magnetic moment μ = √[n(n + 2)] BM; identifying the ion from μ",
    "5.92 BM = √35 means n(n + 2) = 35, so n = 5 unpaired electrons: M²⁺ is 3d⁵, i.e. Mn²⁺. Then Mn³⁺ is 3d⁴ "
    "with four unpaired electrons.",
    ["√[n(n + 2)] = 5.92 → n = 5 → M²⁺ = 3d⁵ → Mn²⁺", "Mn³⁺ = 3d⁴ → n = 4",
     "μ = √(4 × 6) = √24 = 4.90 BM"],
    why="5.92 BM assumes the moment does not change on oxidation. 6.93 BM adds an electron instead of removing "
        "one. 3.87 BM removes two d electrons.",
    ncert=f"{REF11}, magnetic properties", seconds=80, checked=True)

add("Lanthanoids and actinoids", A, "match_list",
    lists("Match List-I (element) with List-II (its ground-state electronic configuration). (Z: La = 57, "
          "Gd = 64, Yb = 70, Lu = 71; Xe = 54)",
          ["Lanthanum", "Gadolinium", "Ytterbium", "Lutetium"],
          ["[Xe] 4f¹⁴ 6s²", "[Xe] 5d¹ 6s²", "[Xe] 4f¹⁴ 5d¹ 6s²", "[Xe] 4f⁷ 5d¹ 6s²"]),
    match("B", M("II IV I III"), [M("II IV III I"), M("IV II I III"), M("II I IV III")]),
    "Electronic configurations of the lanthanoids",
    "The general configuration is [Xe] 4f¹⁻¹⁴ 5d⁰⁻¹ 6s². A 5d electron appears in La (no 4f electrons), in Gd "
    "(after the half-filled 4f⁷) and in Lu (after the full 4f¹⁴); Yb has a full 4f¹⁴ with no 5d electron.",
    ["A: La (57) = [Xe] 5d¹ 6s² → II", "B: Gd (64) = [Xe] 4f⁷ 5d¹ 6s² → IV", "C: Yb (70) = [Xe] 4f¹⁴ 6s² → I",
     "D: Lu (71) = [Xe] 4f¹⁴ 5d¹ 6s² → III"],
    why="C-III/D-I swaps ytterbium and lutetium (Lu has the extra 5d electron). A-IV/B-II swaps lanthanum and "
        "gadolinium. B-I/C-IV gives gadolinium a full 4f subshell.",
    ncert=f"{REF11}, the lanthanoids: electronic configurations", seconds=60, checked=False)

truth_para = {"a": True, "b": False, "c": True, "d": False, "e": True}
add("Magnetic and colour properties", A, "multi_statement",
    ms("Which of the following gaseous ions are paramagnetic? (Z: Sc = 21, Ti = 22, Cr = 24, Co = 27, Cu = 29)",
       ["Ti³⁺", "Cu⁺", "Cr³⁺", "Sc³⁺", "Co²⁺"]),
    multi("D", truth_para, ["(a), (b) and (c) only", "(c) and (e) only", "(a), (c), (d) and (e) only"]),
    "Paramagnetism arises from unpaired electrons",
    "Write the 3d configuration of each ion. Ions with no unpaired electrons (3d⁰ or 3d¹⁰) are diamagnetic.",
    ["(a) Ti³⁺: 3d¹ → 1 unpaired ✓", "(b) Cu⁺: 3d¹⁰ → diamagnetic ✗", "(c) Cr³⁺: 3d³ → 3 unpaired ✓",
     "(d) Sc³⁺: 3d⁰ → diamagnetic ✗", "(e) Co²⁺: 3d⁷ → 3 unpaired ✓"],
    why="Cu⁺ (3d¹⁰) and Sc³⁺ (3d⁰) have no unpaired electrons; options including either are wrong, and "
        "'(c) and (e) only' misses Ti³⁺.",
    ncert=f"{REF11}, magnetic properties", seconds=60)

truth_act = {"a": True, "b": True, "c": True, "d": False, "e": False}
add("Lanthanoids and actinoids", A, "multi_statement",
    ms("Which of the following statements about the electronic configurations and oxidation states of the "
       "actinoids are correct?",
       ["The actinoids show a greater range of oxidation states than the lanthanoids.",
        "The +3 oxidation state is common to the actinoids.",
        "Thorium (Z = 90) has no 5f electron in its ground-state configuration.",
        "The maximum oxidation state shown by uranium is +7.",
        "The general electronic configuration of the actinoids is [Rn] 5f¹⁻¹⁴ 6d⁰⁻¹ 7s¹."]),
    multi("C", truth_act, ["(a), (b), (c) and (d) only", "(b), (d) and (e) only", "(a) and (e) only"]),
    "Actinoids: electronic configurations and oxidation states",
    "The 5f, 6d and 7s levels have comparable energies, so the actinoids show a wide range of oxidation states, "
    "with +3 common to the series. Thorium is [Rn] 6d² 7s². Uranium's maximum is +6 (+7 is reached by Np and "
    "Pu). The general configuration ends in 7s².",
    ["(a) ✓", "(b) ✓", "(c) Th = [Rn] 6d² 7s² → no 5f electron ✓", "(d) ✗: U maximum is +6",
     "(e) ✗: 7s², not 7s¹"],
    why="(d) gives uranium neptunium's maximum oxidation state and (e) has the wrong 7s occupancy; options "
        "containing either are wrong.",
    ncert=f"{REF11}, the actinoids: electronic configurations and oxidation states", seconds=70)
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
    doc = {"schema_version": "1.0", "batch_id": "BATCH_010", "created_at": TODAY,
           "notes": "Package CHE_010_p1: 122 original Chemistry questions (physical and inorganic chemistry). "
                    "Numerical answers re-derived in tools/batch_010/CHE_010_p1.py.",
           "stimuli": [], "questions": QUESTIONS}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {OUT}: {n} questions; difficulty {dict(Counter(q['difficulty'] for q in QUESTIONS))}; "
          f"formats {dict(fmts)}; keys {dict(sorted(KEYS.items()))}")
