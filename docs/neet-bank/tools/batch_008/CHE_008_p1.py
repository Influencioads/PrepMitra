"""Writes batches/parts/BATCH_008_CHE_p1.json: package CHE_008_p1 of BATCH_008 (Chemistry, 123 questions).

Topics: Some Basic Concepts, Atomic Structure, Chemical Bonding, Thermodynamics, Solutions, Equilibrium,
Redox and Electrochemistry, Chemical Kinetics, Classification of Elements and Periodicity, p-Block Elements,
d- and f-Block Elements. IDs NEET_CHE_001751..001873.

Every computable answer is re-derived here with an assert before anything is written; the quota per
(topic, difficulty), the ID range, the format mix and the answer-key balance are asserted too.
The position of every correct option is chosen by hand in the call that adds the question (argument `at`)
and never moved by code.

    cd docs/neet-bank && python tools/batch_008/CHE_008_p1.py
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
PACKAGE = "CHE_008_p1"
PLAN = ROOT / "batches" / "plans" / "BATCH_008_plan.json"
OUT = ROOT / "batches" / "parts" / "BATCH_008_CHE_p1.json"
TODAY = "2026-11-16"
LETTERS = "ABCD"
CHE = "Chemistry"
FIRST_ID = 1751
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

n_so2 = 3.2 / 64
assert close(n_so2 * 22.7, 1.135) and close(3.2 / 32 * 22.7, 2.27) and close(3.2 / 128 * 22.7, 0.5675) \
    and close(3 * n_so2 * 22.7, 3.405)
add("Mole concept", B, "numerical",
    "The volume occupied at STP by 3.2 g of sulphur dioxide gas is (S = 32, O = 16; molar volume of a gas at "
    "STP = 22.7 L mol⁻¹):",
    Opts("B", "1.135 L", ["2.27 L", "0.568 L", "3.405 L"]),
    "Converting a mass of gas into its volume at STP",
    "Find the amount of SO₂ in moles from its molar mass and multiply by the molar volume.",
    ["M(SO₂) = 32 + 2 × 16 = 64 g mol⁻¹", "n = 3.2/64 = 0.05 mol", "V = 0.05 × 22.7 = 1.135 L"],
    why="2.27 L uses 32 g mol⁻¹ (the mass of S only) as the molar mass. 0.568 L uses 128 g mol⁻¹, twice the "
        "correct molar mass. 3.405 L multiplies by 3, counting atoms instead of molecules.",
    ncert=f"{REF1}, mole concept and molar masses", seconds=35, checked=True)

add("Laws of chemical combination", B, "direct",
    "Which of the following is NOT a postulate of Dalton's atomic theory?",
    Opts("D", "Atoms are made up of protons, neutrons and electrons.",
         ["Matter consists of indivisible atoms.",
          "All the atoms of a given element have identical properties, including identical mass.",
          "Compounds are formed when atoms of different elements combine in a fixed ratio."]),
    "Postulates of Dalton's atomic theory",
    "Dalton (1808) took atoms to be indivisible. The sub-atomic particles were discovered much later, so a "
    "statement about protons, neutrons and electrons cannot be one of his postulates.",
    ["Indivisible atoms, identical atoms of an element, fixed-ratio combination → Dalton's postulates",
     "Atoms made of sub-atomic particles → contradicts the idea of indivisible atoms"],
    why="The other three statements are postulates of Dalton's theory as given in NCERT.",
    ncert=f"{REF1}, Dalton's atomic theory", seconds=25)

add("Mole concept", B, "statement_pair",
    sp("14 g of nitrogen gas (N₂) contains 6.022 × 10²³ atoms of nitrogen (N = 14).",
       "One mole of solid sodium chloride contains 6.022 × 10²³ ions in all."),
    SP_, "Counting atoms and ions with the mole concept",
    "14 g of N₂ is 14/28 = 0.5 mol of molecules; each molecule has two atoms, so it contains 1 mol "
    "(6.022 × 10²³) of N atoms. Statement I is true. One mole of NaCl contains one mole of Na⁺ and one mole of "
    "Cl⁻, i.e. 2 × 6.022 × 10²³ ions in all. Statement II is false.",
    ["I: n(N₂) = 0.5 mol → n(N) = 1 mol → 6.022 × 10²³ atoms → true",
     "II: 1 mol NaCl → 1 mol Na⁺ + 1 mol Cl⁻ = 1.204 × 10²⁴ ions → false"],
    answer="C",
    why="Statement II counts formula units, not ions; Statement I correctly uses two atoms per N₂ molecule.",
    ncert=f"{REF1}, mole concept and molar masses", seconds=40)

# 0.30 g compound -> 0.44 g CO2 + 0.18 g H2O ; vapour density 30
m_c = 0.44 * 12 / 44
m_h = 0.18 * 2 / 18
m_o = 0.30 - m_c - m_h
mol = (m_c / 12, m_h / 1, m_o / 16)
assert close(m_c, 0.12) and close(m_h, 0.02) and close(m_o, 0.16)
assert [round(x / min(mol), 6) for x in mol] == [1, 2, 1]  # CH2O, 30 g/mol
assert round(2 * 30 / 30) == 2  # M = 2 x VD = 60 -> (CH2O)2 = C2H4O2
add("Empirical and molecular formulae", I, "numerical",
    "0.30 g of an organic compound containing only carbon, hydrogen and oxygen gives 0.44 g of CO₂ and 0.18 g "
    "of H₂O on complete combustion. The vapour density of the compound is 30. Its molecular formula is "
    "(C = 12, H = 1, O = 16; molar mass = 2 × vapour density):",
    Opts("C", "C₂H₄O₂", ["CH₂O", "C₄H₈O₄", "C₂H₂O₂"]),
    "Empirical formula from combustion data; molecular formula from vapour density",
    "Find the masses of C and H from the CO₂ and H₂O formed, get O by difference, convert to a mole ratio, then "
    "compare the empirical formula mass with the molar mass (2 × vapour density).",
    ["C = 0.44 × 12/44 = 0.12 g; H = 0.18 × 2/18 = 0.02 g; O = 0.30 − 0.14 = 0.16 g",
     "Moles: C 0.01, H 0.02, O 0.01 → empirical formula CH₂O (formula mass 30)",
     "M = 2 × 30 = 60 g mol⁻¹ → n = 60/30 = 2 → C₂H₄O₂"],
    why="CH₂O is only the empirical formula (it takes the molar mass equal to the vapour density). C₄H₈O₄ uses a "
        "molar mass of 120 g mol⁻¹. C₂H₂O₂ counts one H atom per H₂O molecule instead of two.",
    ncert=f"{REF1}, empirical and molecular formula", seconds=90, checked=True)

n_o = 8.8 / 44 * 2
m_caco3 = n_o / 3 * 100
assert close(m_caco3, 13.33) and close(8.8 / 44 * 100, 20.0) and close(n_o * 100, 40.0) \
    and close(8.8 / 44 / 3 * 100, 6.667)
add("Mole concept", I, "numerical",
    "The mass of calcium carbonate that contains the same number of oxygen atoms as 8.8 g of carbon dioxide is "
    "(Ca = 40, C = 12, O = 16):",
    Opts("A", "13.3 g", ["20.0 g", "40.0 g", "6.67 g"]),
    "Equating numbers of atoms through the mole concept",
    "Find the moles of O atoms in the CO₂ (two per molecule); CaCO₃ has three O atoms per formula unit.",
    ["n(CO₂) = 8.8/44 = 0.20 mol → n(O) = 0.40 mol",
     "n(CaCO₃) = 0.40/3 = 0.133 mol", "Mass = 0.133 × 100 = 13.3 g"],
    why="20.0 g equates moles of CaCO₃ with moles of CO₂. 40.0 g takes one O atom per CaCO₃. 6.67 g takes one "
        "O atom per CO₂ molecule.",
    ncert=f"{REF1}, mole concept and molar masses", seconds=60, checked=True)

add("Laws of chemical combination", I, "assertion_reason",
    ar("At the same temperature and pressure, two volumes of hydrogen react with one volume of oxygen to give "
       "two volumes of water vapour, in agreement with the equation 2H₂(g) + O₂(g) → 2H₂O(g).",
       "Equal volumes of all gases at the same temperature and pressure contain equal numbers of molecules."),
    AR_, "Gay-Lussac's law explained by Avogadro's law",
    "By Avogadro's law, volumes of gases at the same temperature and pressure are proportional to the numbers "
    "of molecules. A 2 : 1 : 2 volume ratio is therefore a 2 : 1 : 2 ratio of molecules, which is exactly what "
    "the balanced equation (with diatomic H₂ and O₂) requires. R explains A.",
    ["A: observed 2 : 1 : 2 volume ratio → true", "R: Avogadro's law → true",
     "Volume ratio = molecule ratio (because of R) → matches the equation → R explains A"],
    answer="A",
    why="Both statements are true and Avogadro's hypothesis is precisely what converts the volume ratio into "
        "the mole ratio of the equation.",
    ncert=f"{REF1}, Gay-Lussac's law of gaseous volumes and Avogadro's law", seconds=45)

m_hb = 4 * 56 / 0.0034
assert close(m_hb, 6.59e4) and close(56 / 0.0034, 1.65e4) and close(4 * 56 / 0.34, 659) \
    and close(4 * m_hb, 2.64e5)
add("Mole concept", A, "numerical",
    "Haemoglobin contains 0.34% iron by mass, and each haemoglobin molecule contains four iron atoms. The molar "
    "mass of haemoglobin is about (Fe = 56):",
    Opts("D", "6.59 × 10⁴ g mol⁻¹", ["1.65 × 10⁴ g mol⁻¹", "6.59 × 10² g mol⁻¹", "2.64 × 10⁵ g mol⁻¹"]),
    "Molar mass from the mass per cent of a minor element",
    "In one mole of haemoglobin there are 4 mol of Fe, i.e. 224 g of iron, and this is 0.34% of the molar mass.",
    ["Mass of Fe per mole of haemoglobin = 4 × 56 = 224 g", "0.34% of M = 224 g → M = 224/0.0034",
     "M ≈ 6.59 × 10⁴ g mol⁻¹"],
    why="1.65 × 10⁴ g mol⁻¹ assumes one Fe atom per molecule. 6.59 × 10² g mol⁻¹ divides by 0.34 instead of "
        "0.0034. 2.64 × 10⁵ g mol⁻¹ multiplies the correct value by 4 again.",
    ncert=f"{REF1}, percentage composition", seconds=75, checked=True)

# 1 vol X_n + 6 vol H2 -> 4 vol XH3 ; volumes = molecules (Avogadro)
h_atoms = 6 * 2
hydride = 4
assert h_atoms == hydride * 3 and hydride * 1 / 1 == 4
add("Laws of chemical combination", A, "numerical",
    "At the same temperature and pressure, one volume of the vapour of an element X combines exactly with six "
    "volumes of hydrogen gas (H₂) to give four volumes of a gaseous hydride. Each molecule of the hydride "
    "contains one atom of X and three atoms of hydrogen. The number of atoms in one molecule of the vapour of X "
    "is:",
    Opts("B", "4", ["1", "2", "6"]),
    "Gay-Lussac's law with Avogadro's law: atomicity from combining volumes",
    "Equal volumes contain equal numbers of molecules, so 1 molecule of Xₙ reacts with 6 molecules of H₂ to give "
    "4 molecules of XH₃. All the X atoms of one Xₙ molecule end up in four hydride molecules.",
    ["Xₙ + 6H₂ → 4XH₃ (molecule ratio = volume ratio)", "Hydrogen check: 6 × 2 = 12 = 4 × 3 ✓",
     "X atoms: n = 4 × 1 = 4 → the vapour is X₄"],
    why="1 ignores Avogadro's law. 2 assumes the vapour is diatomic like most gases; then only two volumes of "
        "hydride would form. 6 is the number of volumes of hydrogen, not the atomicity of X.",
    ncert=f"{REF1}, Gay-Lussac's law of gaseous volumes and Avogadro's law", seconds=90, checked=True)

# ==================================================================== 2. Atomic Structure
topic("Atomic Structure")
REF2 = f"{C11}, 'Structure of Atom'"

e_ratio = (1 / 400) / (1 / 600)
assert close(e_ratio, 1.5)
add("Dual nature and uncertainty", B, "numerical",
    "The ratio of the energy of a photon of wavelength 400 nm to that of a photon of wavelength 600 nm is:",
    Opts("C", "3 : 2", ["2 : 3", "9 : 4", "4 : 9"]),
    "Energy of a photon, E = hc/λ",
    "Photon energy is inversely proportional to wavelength, so the shorter-wavelength photon carries more energy.",
    ["E = hc/λ → E₁/E₂ = λ₂/λ₁", "E(400 nm)/E(600 nm) = 600/400 = 3/2"],
    why="2 : 3 takes E proportional to λ. 9 : 4 and 4 : 9 square the ratio, as if E depended on 1/λ² or λ².",
    ncert=f"{REF2}, Planck's quantum theory", seconds=30, checked=True)

add("Quantum numbers and orbitals", B, "match_list",
    lists("Match List-I (quantum numbers of an electron) with List-II (subshell in which the electron is "
          "present).",
          ["n = 3, l = 2", "n = 4, l = 3", "n = 2, l = 1", "n = 5, l = 0"],
          ["5s", "3d", "2p", "4f"]),
    match("A", M("II IV III I"), [M("II III IV I"), M("IV II III I"), M("III IV II I")]),
    "Naming subshells from n and l",
    "l = 0, 1, 2, 3 correspond to s, p, d, f; the subshell is written as n followed by this letter.",
    ["n = 3, l = 2 → 3d (II)", "n = 4, l = 3 → 4f (IV)", "n = 2, l = 1 → 2p (III)", "n = 5, l = 0 → 5s (I)"],
    why="Each other code gives at least one wrong letter for l, e.g. pairing l = 3 with p or l = 1 with f.",
    ncert=f"{REF2}, quantum numbers", seconds=30)

add("Dual nature and uncertainty", B, "statement_pair",
    sp("In vacuum, radio waves travel faster than X-rays.",
       "The frequency (ν) and wavelength (λ) of an electromagnetic radiation are related by c = νλ, where c is "
       "the speed of light."),
    SP_, "Characteristics of electromagnetic radiation",
    "All electromagnetic radiations, whatever their wavelength, travel with the same speed in vacuum, "
    "3.0 × 10⁸ m s⁻¹, so Statement I is false. c = νλ is the relation between frequency and wavelength, so "
    "Statement II is true.",
    ["I: all EM radiations have the same speed in vacuum → false", "II: c = νλ → true"],
    answer="D",
    why="Radio waves and X-rays differ in frequency and wavelength, not in their speed in vacuum.",
    ncert=f"{REF2}, nature of electromagnetic radiation", seconds=30)

# r_n = 52.9 n^2 / Z pm ; Be3+ Z = 4
n_be = math.sqrt(4 * 1)
assert n_be == 2 and 52.9 * n_be ** 2 / 4 == 52.9
add("Bohr model and hydrogen spectrum", I, "numerical",
    "According to Bohr's model, the radius of the nth orbit of a hydrogen-like species is rₙ = 52.9 (n²/Z) pm. "
    "The orbit of the Be³⁺ ion (Z = 4) whose radius equals that of the first Bohr orbit of the hydrogen atom "
    "is:",
    Opts("D", "n = 2", ["n = 4", "n = 16", "n = 1"]),
    "Radius of Bohr orbits of hydrogen-like species",
    "Set 52.9 n²/4 equal to 52.9 pm (n = 1, Z = 1 for hydrogen) and solve for n.",
    ["52.9 × n²/4 = 52.9 × 1²/1", "n² = 4 → n = 2"],
    why="n = 4 takes r proportional to n/Z. n = 16 confuses n² with Z². n = 1 gives a radius of 13.2 pm, a quarter "
        "of the hydrogen value.",
    ncert=f"{REF2}, Bohr's model for hydrogen atom", seconds=45, checked=True)

add("Electronic configuration", I, "direct",
    "Which of the following electronic configurations represents an EXCITED state, not the ground state, of the "
    "atom named?",
    Opts("B", "Carbon (Z = 6): 1s² 2s¹ 2p³",
         ["Sodium (Z = 11): 1s² 2s² 2p⁶ 3s¹", "Chromium (Z = 24): [Ar] 3d⁵ 4s¹",
          "Copper (Z = 29): [Ar] 3d¹⁰ 4s¹"]),
    "Ground-state configurations by the Aufbau principle, with the Cr and Cu exceptions",
    "The ground state of carbon is 1s² 2s² 2p²; promoting one 2s electron to 2p gives an excited state. The "
    "chromium and copper configurations, though exceptions to the simple filling order, are their actual ground "
    "states (half-filled and filled 3d subshells are extra stable).",
    ["C: ground 1s² 2s² 2p² → 1s² 2s¹ 2p³ is excited", "Na [Ne] 3s¹, Cr [Ar] 3d⁵ 4s¹, Cu [Ar] 3d¹⁰ 4s¹ → ground"],
    why="Students often mark Cr or Cu because they do not follow the simple Aufbau order, but these are the "
        "observed ground-state configurations.",
    ncert=f"{REF2}, electronic configuration of atoms; stability of half-filled and completely filled orbitals",
    seconds=45)

add("Quantum numbers and orbitals", I, "assertion_reason",
    ar("There is no 3f subshell.",
       "For n = 3, the azimuthal quantum number l can have only the values 0, 1 and 2, whereas an f subshell "
       "needs l = 3."),
    AR_, "Allowed values of the azimuthal quantum number",
    "l can take the values 0 to (n − 1). For n = 3 this means 0, 1, 2 (3s, 3p, 3d); l = 3 (f) first becomes "
    "possible at n = 4. R is exactly the reason A is true.",
    ["l = 0 … n − 1", "n = 3 → l = 0, 1, 2 only → no 3f", "f subshells start at n = 4 (4f)"],
    answer="A",
    why="Both statements are true, and the restriction on l in R is what rules out a 3f subshell.",
    ncert=f"{REF2}, quantum numbers", seconds=35)

M_E, M_P = 9.11e-31, 1.67e-27
ratio_dx = M_P / M_E
assert close(ratio_dx, 1833) and close(math.sqrt(ratio_dx), 42.8)
add("Dual nature and uncertainty", I, "numerical",
    "An electron and a proton have the same uncertainty in velocity. The ratio of the minimum uncertainty in the "
    "position of the electron to that of the proton is (mass of electron = 9.11 × 10⁻³¹ kg; mass of proton = "
    "1.67 × 10⁻²⁷ kg):",
    Opts("A", "1833 : 1", ["1 : 1833", "1 : 1", "42.8 : 1"]),
    "Heisenberg's uncertainty principle, Δx × mΔv ≥ h/4π",
    "For the same Δv, the minimum Δx = h/(4πmΔv) is inversely proportional to the mass, so the much lighter "
    "electron has the far larger uncertainty in position.",
    ["Δx = h/(4π m Δv)", "Δx(e)/Δx(p) = m(p)/m(e) = 1.67 × 10⁻²⁷ / 9.11 × 10⁻³¹ ≈ 1833"],
    why="1 : 1833 inverts the ratio (takes Δx proportional to mass). 1 : 1 ignores the mass in Δp = mΔv. "
        "42.8 : 1 takes a square root that is not in the relation.",
    ncert=f"{REF2}, Heisenberg's uncertainty principle", seconds=50, checked=True)

add("Bohr model and hydrogen spectrum", I, "multi_statement",
    ms("Which of the following statements about the emission spectrum of atomic hydrogen are correct?",
       ["The lines of the Lyman series lie in the ultraviolet region.",
        "The lines of the Paschen series lie in the infrared region.",
        "Within a series, the lines come closer together as the wavelength decreases towards the series limit.",
        "The longest-wavelength line of the Lyman series arises from the transition n = 3 → n = 1.",
        "The Balmer series arises when electrons fall to the orbit n = 1."]),
    multi("C", {"a": True, "b": True, "c": True, "d": False, "e": False},
          ["(a), (b) and (d) only", "(b), (c) and (e) only", "(a) and (c) only"]),
    "Spectral series of hydrogen",
    "Lyman (n₁ = 1) lies in the ultraviolet, Balmer (n₁ = 2) in the visible and Paschen (n₁ = 3) in the infrared. "
    "Since 1/λ = R(1/n₁² − 1/n₂²), successive lines of a series crowd together towards the series limit "
    "(n₂ → ∞), which is the short-wavelength end. The longest wavelength of a series is the smallest energy "
    "gap, n₂ = n₁ + 1.",
    ["(a) Lyman → UV ✓", "(b) Paschen → IR ✓", "(c) lines converge at the short-wavelength limit ✓",
     "(d) longest Lyman line is 2 → 1, not 3 → 1 ✗", "(e) Balmer ends at n = 2, not n = 1 ✗"],
    why="Any option containing (d) or (e) is wrong; (a) and (c) only leaves out the true statement (b).",
    ncert=f"{REF2}, line spectrum of hydrogen", seconds=70)

r3 = 52.9 * 9
lam3 = 2 * 3.14 * r3 / 3
assert close(lam3, 996.6) and close(2 * 3.14 * 52.9, 332.2) and close(2 * 3.14 * r3, 2990) \
    and close(3.14 * r3 / 3, 498.3)
add("Bohr model and hydrogen spectrum", A, "numerical",
    "Combine Bohr's condition mvr = nh/2π with the de Broglie relation λ = h/mv to find the de Broglie "
    "wavelength of the electron in the third orbit (n = 3) of a hydrogen atom. (Radius of the nth orbit = "
    "52.9 n² pm; π = 3.14)",
    Opts("B", "997 pm", ["332 pm", "2990 pm", "498 pm"]),
    "Electron waves in Bohr orbits: nλ = 2πr",
    "From mvr = nh/2π, mv = nh/2πr, so λ = h/mv = 2πr/n: a whole number of wavelengths fits round the orbit.",
    ["r₃ = 52.9 × 9 = 476.1 pm", "λ = 2πr₃/n = 2 × 3.14 × 476.1/3", "λ ≈ 997 pm"],
    why="332 pm is the wavelength in the first orbit (2πr₁). 2990 pm forgets to divide by n. 498 pm uses πr/n "
        "instead of 2πr/n.",
    ncert=f"{REF2}, Bohr's model; dual behaviour of matter", seconds=110, checked=True)

add("Electronic configuration", A, "multi_statement",
    ms("Which of the following statements about filling electrons into orbitals are correct?",
       ["The 4s orbital is filled before the 3d orbitals because its (n + l) value is lower.",
        "In the Aufbau order, the 4f orbitals are filled after the 6s orbital and before the 5d orbitals.",
        "Hund's rule of maximum multiplicity applies to the filling of orbitals of equal energy.",
        "A single orbital can hold two electrons with the same spin."]),
    multi("D", {"a": True, "b": True, "c": True, "d": False},
          ["(a) and (c) only", "(b), (c) and (d) only", "(a), (b), (c) and (d)"]),
    "Aufbau principle, (n + l) rule, Hund's rule and the Pauli exclusion principle",
    "4s has n + l = 4 and 3d has n + l = 5, so 4s fills first. The filling order runs …, 5p, 6s, 4f, 5d, 6p, …. "
    "Hund's rule concerns degenerate orbitals such as the three p or five d orbitals. By the Pauli principle, two "
    "electrons in one orbital must have opposite spins.",
    ["(a) 4s (4) < 3d (5) ✓", "(b) 6s → 4f → 5d ✓", "(c) Hund's rule: degenerate orbitals ✓",
     "(d) violates the Pauli exclusion principle ✗"],
    why="Options including (d) break the exclusion principle; '(a) and (c) only' wrongly rejects the correct "
        "filling order in (b).",
    ncert=f"{REF2}, filling of orbitals in atoms", seconds=70)

lam_ratio = math.sqrt((1 * 8) / (2 * 1))  # lambda = h / sqrt(2mK); mA = 2mB, KA = KB/8
assert lam_ratio == 2
add("Dual nature and uncertainty", A, "numerical",
    "Particle A has twice the mass of particle B, but its kinetic energy is one-eighth of that of B. The ratio of "
    "their de Broglie wavelengths, λ_A : λ_B, is:",
    Opts("C", "2 : 1", ["1 : 2", "4 : 1", "1 : 4"]),
    "de Broglie wavelength in terms of kinetic energy",
    "Momentum p = √(2mK), so λ = h/p = h/√(2mK); the wavelength is inversely proportional to √(mK).",
    ["λ_A/λ_B = √(m_B K_B / (m_A K_A))", "m_A K_A = 2m_B × K_B/8 = m_B K_B/4",
     "λ_A/λ_B = √4 = 2 → 2 : 1"],
    why="1 : 2 inverts the ratio. 4 : 1 and 1 : 4 leave out the square root (taking λ ∝ 1/(mK)).",
    ncert=f"{REF2}, dual behaviour of matter", seconds=75, checked=True)

# ==================================================================== 3. Chemical Bonding and Molecular Structure
topic("Chemical Bonding and Molecular Structure")
REF3 = f"{C11}, 'Chemical Bonding and Molecular Structure'"

add("Ionic bonding and lattice enthalpy", B, "direct",
    "In the Kössel–Lewis description of ionic bonding, the electrovalence of an element equals the number of "
    "unit charges on its ion. In calcium fluoride, CaF₂, the electrovalences of calcium and fluorine are "
    "respectively:",
    Opts("A", "2 and 1", ["1 and 2", "2 and 2", "1 and 1"]),
    "Electrovalence in ionic compounds",
    "Calcium (2 valence electrons) loses two electrons to form Ca²⁺; each fluorine atom (7 valence electrons) "
    "gains one electron to form F⁻. CaF₂ = Ca²⁺ + 2F⁻.",
    ["Ca → Ca²⁺ + 2e⁻ → electrovalence 2", "F + e⁻ → F⁻ → electrovalence 1"],
    why="'1 and 2' swaps the two values, reading the subscript 2 in CaF₂ as the charge on fluoride. '2 and 2' and "
        "'1 and 1' do not match the ions Ca²⁺ and F⁻.",
    ncert=f"{REF3}, Kössel–Lewis approach; ionic or electrovalent bond", seconds=25)

add("VSEPR shapes", B, "match_list",
    lists("Match List-I (molecule) with List-II (its bond angle).",
          ["BeCl₂", "BF₃", "CH₄", "H₂O"], ["104.5°", "120°", "180°", "109.5°"]),
    match("B", M("III II IV I"), [M("III IV II I"), M("II III IV I"), M("III II I IV")]),
    "Bond angles predicted by VSEPR theory",
    "BeCl₂ is linear (two bond pairs), BF₃ trigonal planar (three bond pairs), CH₄ tetrahedral (four bond "
    "pairs). In H₂O two lone pairs squeeze the H–O–H angle from 109.5° down to 104.5°.",
    ["BeCl₂ → 180° (III)", "BF₃ → 120° (II)", "CH₄ → 109.5° (IV)", "H₂O → 104.5° (I)"],
    why="The other codes either swap the planar and tetrahedral angles or give water the ideal tetrahedral "
        "angle, ignoring lone pair repulsion.",
    ncert=f"{REF3}, VSEPR theory", seconds=35)

add("Fajans' rule and dipole moment", B, "statement_pair",
    sp("In H₂, O₂ and Cl₂ the shared electron pair is shared equally between the two identical atoms, so the "
       "bond is a non-polar covalent bond.",
       "In the HF molecule, the shared electron pair is displaced towards the hydrogen atom."),
    SP_, "Polar and non-polar covalent bonds",
    "Between identical atoms the electronegativities are equal, so the pair is shared equally: Statement I is "
    "true. Fluorine is far more electronegative than hydrogen, so the pair shifts towards F (H^δ+–F^δ−): "
    "Statement II is false.",
    ["I: identical atoms → equal sharing → non-polar → true",
     "II: pair shifts towards the more electronegative F, not H → false"],
    answer="C",
    why="Statement II reverses the direction of polarity; F carries the partial negative charge in HF.",
    ncert=f"{REF3}, polarity of bonds", seconds=30)

add("VSEPR shapes", B, "direct",
    "In which of the following molecules does the central atom have fewer than eight electrons in its valence "
    "shell (an incomplete octet)?",
    Opts("C", "BeH₂", ["CO₂", "NH₃", "CH₄"]),
    "Limitations of the octet rule: the incomplete octet",
    "Beryllium has only two valence electrons; in BeH₂ it forms two bonds and is surrounded by just four "
    "electrons. Carbon in CO₂ and CH₄, and nitrogen in NH₃ (three bond pairs + one lone pair), have complete "
    "octets.",
    ["BeH₂: 2 bond pairs → 4 electrons around Be", "CO₂, CH₄: 4 bonds → octet; NH₃: 3 bp + 1 lp → octet"],
    why="CO₂, NH₃ and CH₄ all obey the octet rule.",
    ncert=f"{REF3}, limitations of the octet rule", seconds=30)

fc_central = 6 - 2 - 6 / 2  # valence e - non-bonding e - half of bonding e
assert fc_central == 1 and 6 - 4 - 4 / 2 == 0 and 6 - 6 - 2 / 2 == -1
add("Hybridisation and resonance", B, "numerical",
    "In a Lewis structure of ozone, O=O–O, in which every atom has an octet, the central oxygen atom carries one "
    "lone pair. The formal charge on the central oxygen atom is:",
    Opts("D", "+1", ["0", "−1", "+2"]),
    "Formal charge = valence electrons − non-bonding electrons − ½ (bonding electrons)",
    "The central O is joined by one double and one single bond (six bonding electrons) and holds one lone pair "
    "(two non-bonding electrons).",
    ["Central O: 6 − 2 − ½(6) = +1", "Check: double-bonded terminal O 6 − 4 − 2 = 0; single-bonded terminal O "
     "6 − 6 − 1 = −1; total 0 for the neutral molecule"],
    why="0 and −1 are the formal charges of the two terminal oxygen atoms. +2 ignores the lone pair on the "
        "central atom.",
    ncert=f"{REF3}, formal charge", seconds=40, checked=True)

# tetracyanoethylene (NC)2C=C(CN)2
sigma = 1 + 4 + 4
pi = 1 + 4 * 2
assert (sigma, pi) == (9, 9)
add("Hybridisation and resonance", I, "numerical",
    "The numbers of σ bonds and π bonds in one molecule of tetracyanoethylene, (NC)₂C=C(CN)₂, are respectively:",
    Opts("A", "9 and 9", ["9 and 5", "13 and 9", "5 and 9"]),
    "Counting σ and π bonds: every bond has one σ; a double bond adds one π, a triple bond two π",
    "The molecule has one C=C bond, four C–C single bonds (each joining a CN group to the central carbon) and "
    "four C≡N triple bonds.",
    ["σ: 1 (C=C) + 4 (C–C) + 4 (C≡N) = 9", "π: 1 (C=C) + 4 × 2 (C≡N) = 9"],
    why="'9 and 5' counts only one π bond per triple bond. '13 and 9' counts π bonds of the triple bonds as σ "
        "bonds as well. '5 and 9' leaves out the σ bonds of the C≡N groups.",
    ncert=f"{REF3}, types of overlapping and nature of covalent bonds", seconds=50, checked=True)

add("VSEPR shapes", I, "assertion_reason",
    ar("The PCl₅ molecule is quite reactive.",
       "In trigonal bipyramidal PCl₅, the two axial P–Cl bonds suffer greater repulsion from the equatorial bond "
       "pairs, so they are slightly longer and weaker than the three equatorial bonds."),
    AR_, "Axial and equatorial bonds in PCl₅",
    "NCERT explains the reactivity of PCl₅ by its axial bonds: each axial bond pair is at 90° to three "
    "equatorial bond pairs, is repelled more, and becomes longer and weaker. These weaker bonds break easily, "
    "which makes the molecule reactive. R explains A.",
    ["Axial bonds: 3 bond pairs at 90° → more repulsion → longer, weaker",
     "Weak axial bonds → PCl₅ reactive → R explains A"],
    answer="A",
    why="Both statements are true and the weaker axial bonds are the stated cause of the reactivity.",
    ncert=f"{REF3}, hybridisation: formation of PCl₅", seconds=45)

add("Hybridisation and resonance", I, "multi_statement",
    ms("Taking z as the internuclear axis, which of the following overlaps of atomic orbitals of two atoms lead "
       "to a σ bond?",
       ["1s with 1s", "1s with 2p_z", "2p_z with 2p_z", "2pₓ with 2pₓ", "1s with 2pₓ"]),
    multi("B", {"a": True, "b": True, "c": True, "d": False, "e": False},
          ["(a), (b), (c) and (d) only", "(c) and (d) only", "(a), (b) and (e) only"]),
    "Types of orbital overlap: σ (head-on) and π (sideways)",
    "s–s, s–p_z and p_z–p_z overlaps take place head-on along the internuclear axis and give σ bonds. Two pₓ "
    "orbitals overlap sideways and give a π bond. A 1s and a 2pₓ orbital give zero net overlap when z is the "
    "bond axis.",
    ["(a), (b), (c): head-on along z → σ", "(d): sideways → π, not σ", "(e): zero overlap → no bond"],
    why="(d) gives a π bond, not a σ bond, and (e) gives no bond at all.",
    ncert=f"{REF3}, types of overlapping and nature of covalent bonds", seconds=50)

add("Fajans' rule and dipole moment", I, "statement_pair",
    sp("The covalent character of the silver halides decreases from AgF to AgI, because the iodide ion is the "
       "largest of the halide ions.",
       "MgCl₂ has greater covalent character than NaCl, because Mg²⁺ has a higher charge and a smaller size than "
       "Na⁺."),
    SP_, "Fajans' rules: polarising power of cations and polarisability of anions",
    "A larger anion is more easily polarised, so covalent character INCREASES from AgF to AgI: Statement I is "
    "false (its reason is right but its conclusion reversed). A cation of higher charge and smaller size "
    "polarises the anion more, so MgCl₂ is more covalent than NaCl: Statement II is true.",
    ["I: larger anion → more polarisable → more covalent → order is AgF < AgCl < AgBr < AgI → false",
     "II: Mg²⁺ (2+, smaller) polarises Cl⁻ more than Na⁺ → true"],
    answer="D",
    why="Statement I draws the wrong conclusion from a correct fact about the size of iodide.",
    ncert=f"{REF3}, polarity of bonds (partial covalent character of ionic bonds)", seconds=45)

add("Molecular orbital theory", I, "assertion_reason",
    ar("The He₂ molecule does not exist.",
       "In He₂ the numbers of electrons in bonding and antibonding molecular orbitals are equal, so its bond "
       "order is zero."),
    AR_, "Bond order and stability in molecular orbital theory",
    "He₂ has four electrons: σ1s² σ*1s². Bond order = ½(2 − 2) = 0; the antibonding electrons cancel the "
    "stabilisation by the bonding electrons, so no stable molecule forms. R explains A.",
    ["He₂: σ1s² σ*1s²", "Bond order = ½(N_b − N_a) = ½(2 − 2) = 0 → not stable"],
    answer="A",
    why="Both statements are true and the zero bond order is the reason given by MO theory.",
    ncert=f"{REF3}, molecular orbital theory: bond order", seconds=35)

nb, na = 2 + 2 + 4 + 2, 2 + 2  # C2(2-), 14 electrons, order for species up to N2
assert (nb - na) / 2 == 3
add("Molecular orbital theory", I, "numerical",
    "Using the molecular orbital energy order for species with up to 14 electrons (π2pₓ = π2p_y below σ2p_z), "
    "the bond order and the magnetic behaviour of the C₂²⁻ ion are:",
    Opts("C", "3; diamagnetic", ["2; paramagnetic", "2; diamagnetic", "3; paramagnetic"]),
    "Molecular orbital configuration of an ion isoelectronic with N₂",
    "C₂²⁻ has 6 + 6 + 2 = 14 electrons, the same as N₂: σ1s² σ*1s² σ2s² σ*2s² (π2pₓ² = π2p_y²) σ2p_z². All the "
    "electrons are paired.",
    ["N_b = 2 + 2 + 4 + 2 = 10; N_a = 2 + 2 = 4", "Bond order = ½(10 − 4) = 3", "No unpaired electron → diamagnetic"],
    why="'2; diamagnetic' is C₂ (12 electrons); the two extra electrons of C₂²⁻ enter the bonding σ2p_z orbital, "
        "raising the bond order to 3. Paramagnetic options would need unpaired electrons, of which there are "
        "none.",
    ncert=f"{REF3}, molecular orbital theory", seconds=60, checked=True)

add("VSEPR shapes", I, "match_list",
    lists("Match List-I (species) with List-II (its shape predicted by VSEPR theory).",
          ["I₃⁻", "ClO₃⁻", "SF₅⁻", "NO₂⁻"],
          ["Bent", "Square pyramidal", "Linear", "Trigonal pyramidal"]),
    match("D", M("III IV II I"), [M("III I II IV"), M("IV III II I"), M("III IV I II")]),
    "Shapes of ions from the numbers of bond pairs and lone pairs on the central atom",
    "Count the electron pairs on the central atom: I₃⁻, central I has 2 bond pairs + 3 lone pairs (AB₂E₃, "
    "linear); ClO₃⁻, Cl has 3 bp + 1 lp (AB₃E, trigonal pyramidal); SF₅⁻, S has 5 bp + 1 lp (AB₅E, square "
    "pyramidal); NO₂⁻, N has 2 σ bond pairs + 1 lp (AB₂E, bent).",
    ["I₃⁻ → linear (III)", "ClO₃⁻ → trigonal pyramidal (IV)", "SF₅⁻ → square pyramidal (II)", "NO₂⁻ → bent (I)"],
    why="The other codes ignore lone pairs, e.g. calling ClO₃⁻ planar-like or NO₂⁻ linear.",
    ncert=f"{REF3}, VSEPR theory", seconds=75)

mu_oh = 1.85 / (2 * 0.612)
assert close(mu_oh, 1.511) and close(1.85 / 2, 0.925) and close(1.85 * 0.612, 1.132) and close(1.85 / 0.612, 3.023)
add("Fajans' rule and dipole moment", A, "numerical",
    "The dipole moment of the water molecule is 1.85 D and its H–O–H bond angle is 104.5°. Treating the "
    "molecular dipole as just the vector sum of the two O–H bond dipoles, the dipole moment of one O–H bond is "
    "(cos 52.25° = 0.612):",
    Opts("A", "1.51 D", ["0.925 D", "1.13 D", "3.02 D"]),
    "Resultant of two equal bond dipoles at an angle",
    "Each bond dipole μ makes an angle of 104.5°/2 = 52.25° with the bisector, so the resultant is "
    "2μ cos 52.25°.",
    ["1.85 = 2 μ_OH cos 52.25° = 2 × 0.612 × μ_OH", "μ_OH = 1.85/1.224 ≈ 1.51 D"],
    why="0.925 D simply halves the molecular dipole, ignoring the angle. 1.13 D multiplies by cos 52.25° instead "
        "of dividing. 3.02 D forgets the factor 2 for the two bonds.",
    ncert=f"{REF3}, dipole moment", seconds=90, checked=True)

add("Hybridisation and resonance", A, "direct",
    "Which of the following shows the correct order of the carbon–oxygen bond length in carbon monoxide (:C≡O:), "
    "carbon dioxide and the carbonate ion?",
    Opts("B", "CO < CO₂ < CO₃²⁻", ["CO₂ < CO < CO₃²⁻", "CO₃²⁻ < CO₂ < CO", "CO < CO₃²⁻ < CO₂"]),
    "Bond order and bond length; average bond order in a resonance hybrid",
    "The higher the bond order between the same two atoms, the shorter the bond. CO has a triple bond (bond "
    "order 3); in CO₂ each C–O bond has bond order 2 (115 pm, between C=O and C≡O values according to NCERT's "
    "resonance description); in the carbonate ion one double bond is shared over three C–O bonds, bond order "
    "4/3.",
    ["Bond orders: CO 3 > CO₂ 2 > CO₃²⁻ 1.33", "Bond length is in the reverse order: CO < CO₂ < CO₃²⁻"],
    why="The other orders do not follow the falling bond order 3 > 2 > 4/3; the carbonate ion, with the lowest "
        "bond order, has the longest C–O bonds.",
    ncert=f"{REF3}, bond parameters; resonance structures", seconds=60)

add("Ionic bonding and lattice enthalpy", A, "multi_statement",
    ms("In the Born–Haber cycle for the formation of NaCl(s) from Na(s) and Cl₂(g), which of the following "
       "statements about the signs of the enthalpy changes are correct?",
       ["The sublimation of sodium, Na(s) → Na(g), is endothermic.",
        "The electron gain enthalpy of chlorine, Cl(g) + e⁻ → Cl⁻(g), is negative.",
        "The ionisation enthalpy of sodium, Na(g) → Na⁺(g) + e⁻, is negative.",
        "The lattice enthalpy, defined for NaCl(s) → Na⁺(g) + Cl⁻(g), is positive.",
        "The dissociation of Cl₂(g) into chlorine atoms releases energy."]),
    multi("C", {"a": True, "b": True, "c": False, "d": True, "e": False},
          ["(a), (b), (c) and (d) only", "(b), (d) and (e) only", "(a) and (d) only"]),
    "Energy changes in the formation of an ionic solid",
    "Breaking up a solid into atoms, removing an electron from an atom and breaking a bond all need energy. "
    "Chlorine releases energy when it gains an electron. Separating the ions of a crystal needs a large amount "
    "of energy, so the lattice enthalpy as defined is positive (788 kJ mol⁻¹ for NaCl).",
    ["(a) endothermic ✓", "(b) ΔegH(Cl) = −349 kJ mol⁻¹ ✓", "(c) ionisation always needs energy ✗",
     "(d) +788 kJ mol⁻¹ ✓", "(e) bond breaking absorbs energy ✗"],
    why="Options including (c) or (e) contain a wrong sign; '(a) and (d) only' leaves out the true statement (b).",
    ncert=f"{REF3}, lattice enthalpy; {C11}, 'Thermodynamics', Born–Haber cycle", seconds=70)

add("Fajans' rule and dipole moment", A, "direct",
    "Which of the following shows the molecules in order of INCREASING dipole moment?",
    Opts("D", "BF₃ < NF₃ < NH₃ < H₂O",
         ["NF₃ < BF₃ < NH₃ < H₂O", "BF₃ < NH₃ < NF₃ < H₂O", "BF₃ < NF₃ < H₂O < NH₃"]),
    "Dipole moment from bond polarity, geometry and lone pairs",
    "Trigonal planar BF₃ has zero dipole moment. In NF₃ the lone pair moment opposes the resultant of the N–F "
    "bond moments (0.23 D), whereas in NH₃ they add (1.47 D). Bent H₂O, with two lone pairs and very polar O–H "
    "bonds, has 1.85 D.",
    ["BF₃: 0 D (symmetrical)", "NF₃: 0.23 D; NH₃: 1.47 D", "H₂O: 1.85 D"],
    why="BF₃ must come first (zero dipole moment); NF₃ is below NH₃ because of the opposing lone pair; and H₂O "
        "has a larger dipole moment than NH₃.",
    ncert=f"{REF3}, dipole moment", seconds=50)

add("VSEPR shapes", A, "direct",
    "In which of the following pairs do the central atoms have the SAME hybridisation but the molecules have "
    "DIFFERENT shapes?",
    Opts("C", "XeF₄ and SF₆", ["XeF₂ and BeCl₂", "BF₃ and NH₃", "CO₂ and BeCl₂"]),
    "Hybridisation versus shape when lone pairs are present",
    "Xe in XeF₄ (4 bp + 2 lp) and S in SF₆ (6 bp) are both sp³d² hybridised, but XeF₄ is square planar while "
    "SF₆ is octahedral, because two of xenon's hybrid orbitals hold lone pairs.",
    ["XeF₄: sp³d², square planar; SF₆: sp³d², octahedral → same hybridisation, different shapes ✓",
     "XeF₂ (sp³d) and BeCl₂ (sp): different hybridisation, both linear",
     "BF₃ (sp²) and NH₃ (sp³): different hybridisation; CO₂ and BeCl₂: both sp and both linear"],
    why="XeF₂/BeCl₂ is a trap: same shape but different hybridisation. BF₃/NH₃ differ in both. CO₂/BeCl₂ agree "
        "in both.",
    ncert=f"{REF3}, VSEPR theory; hybridisation involving d orbitals", seconds=60)

# ==================================================================== 4. Chemical Thermodynamics
topic("Chemical Thermodynamics")
REF4 = f"{C11}, 'Thermodynamics'"

ds_surr = 6010 / 273
assert close(ds_surr, 22.0) and close(6.01 / 273, 0.0220) and close(6.01 * 273, 1641)
add("Entropy and Gibbs energy", B, "numerical",
    "1 mol of liquid water freezes to ice at 273 K and 1 bar, giving out heat equal to its enthalpy of fusion, "
    "6.01 kJ mol⁻¹, to the surroundings at 273 K. The entropy change of the surroundings is:",
    Opts("B", "+22.0 J K⁻¹ mol⁻¹", ["−22.0 J K⁻¹ mol⁻¹", "+0.022 J K⁻¹ mol⁻¹", "+1641 J K⁻¹ mol⁻¹"]),
    "Entropy change of the surroundings, ΔS_surr = q_surr/T = −ΔH_system/T",
    "On freezing, ΔH of the system is −6.01 kJ mol⁻¹; the surroundings absorb this heat at 273 K, so their "
    "entropy rises.",
    ["q_surr = +6010 J mol⁻¹", "ΔS_surr = 6010/273 = +22.0 J K⁻¹ mol⁻¹"],
    why="−22.0 J K⁻¹ mol⁻¹ is the entropy change of the freezing water itself. +0.022 leaves the heat in kJ "
        "while reporting J. +1641 multiplies by T instead of dividing.",
    ncert=f"{REF4}, entropy and spontaneity", seconds=45, checked=True)

add("Hess's law and enthalpies", B, "direct",
    "At a given temperature, the enthalpy of sublimation of a substance is related to its enthalpies of fusion "
    "and of vaporisation at the same temperature by:",
    Opts("A", "ΔsubH = ΔfusH + ΔvapH",
         ["ΔsubH = ΔvapH − ΔfusH", "ΔsubH = ΔfusH − ΔvapH", "ΔsubH = ½(ΔfusH + ΔvapH)"]),
    "Hess's law applied to phase changes",
    "Solid → vapour can be carried out directly, or as solid → liquid followed by liquid → vapour. Enthalpy is a "
    "state function, so both routes give the same enthalpy change.",
    ["Solid → liquid: ΔfusH; liquid → vapour: ΔvapH", "Sum: solid → vapour, ΔsubH = ΔfusH + ΔvapH"],
    why="Subtracting or averaging the two steps has no basis: by Hess's law the enthalpies of successive steps "
        "add up.",
    ncert=f"{REF4}, enthalpies for different types of reactions (phase transformations); Hess's law", seconds=30)

add("Entropy and Gibbs energy", B, "statement_pair",
    sp("A spontaneous process can be reversed only by some external agency.",
       "Every spontaneous process takes place rapidly."),
    SP_, "Meaning of a spontaneous process",
    "A spontaneous process has a natural tendency to occur in one direction; turning it back needs outside help, "
    "so Statement I is true. Spontaneity says nothing about the rate: a spontaneous reaction such as "
    "H₂ + O₂ → H₂O at room temperature can be extremely slow. Statement II is false.",
    ["I: spontaneous processes are irreversible without an external agency → true",
     "II: spontaneity ≠ speed → false"],
    answer="C",
    why="Thermodynamics (ΔG) tells whether a process is feasible, not how fast it goes.",
    ncert=f"{REF4}, spontaneity", seconds=30)

ds_iso = 5 * 8.314 * 2.303 * math.log10(20 / 2)
assert close(ds_iso, 95.74) and close(5 * 8.314 * 1, 41.57) and close(ds_iso * 300, 2.872e4)
add("Entropy and Gibbs energy", I, "numerical",
    "5 mol of an ideal gas expands isothermally and reversibly at 300 K from 2 L to 20 L. The entropy change of "
    "the gas is (R = 8.314 J K⁻¹ mol⁻¹):",
    Opts("D", "95.7 J K⁻¹", ["0", "41.6 J K⁻¹", "2.87 × 10⁴ J K⁻¹"]),
    "ΔS = q_rev/T for an isothermal reversible change",
    "For the isothermal reversible expansion of an ideal gas ΔU = 0, so q_rev = −w = 2.303 nRT log(V_f/V_i), "
    "and ΔS = q_rev/T = 2.303 nR log(V_f/V_i).",
    ["q_rev = 2.303 × 5 × 8.314 × 300 × log 10 = 28 720 J", "ΔS = q_rev/T = 28 720/300 = 95.7 J K⁻¹"],
    why="0 confuses an isothermal process (ΔT = 0) with no entropy change. 41.6 J K⁻¹ leaves out the factor "
        "2.303 when using log₁₀. 2.87 × 10⁴ J K⁻¹ is q_rev (in J), not q_rev/T.",
    ncert=f"{REF4}, entropy; work in isothermal reversible expansion", seconds=75, checked=True)

cv = 29.1 - 8.314
q_v = 2 * cv * 10
assert close(q_v, 415.7) and close(2 * 29.1 * 10, 582) and close(2 * 8.314 * 10, 166.3) and close(cv * 10, 207.9)
add("First law, work and enthalpy", I, "numerical",
    "For an ideal gas, C_p,m = 29.1 J K⁻¹ mol⁻¹. The heat needed to raise the temperature of 2 mol of this gas "
    "by 10 K at constant volume is (R = 8.314 J K⁻¹ mol⁻¹):",
    Opts("C", "416 J", ["582 J", "166 J", "208 J"]),
    "C_p − C_v = R for an ideal gas; q_V = n C_v ΔT",
    "At constant volume the heat absorbed equals ΔU = n C_v,m ΔT, and C_v,m = C_p,m − R.",
    ["C_v,m = 29.1 − 8.314 = 20.79 J K⁻¹ mol⁻¹", "q_V = 2 × 20.79 × 10 = 416 J"],
    why="582 J uses C_p (the constant-pressure heat). 166 J uses R in place of C_v. 208 J is for 1 mol only.",
    ncert=f"{REF4}, heat capacity; relationship between C_p and C_V for an ideal gas", seconds=60, checked=True)

add("Hess's law and enthalpies", I, "assertion_reason",
    ar("The standard enthalpy of formation of I₂(g) at 298 K is not zero.",
       "At 298 K and 1 bar, the reference (most stable) state of iodine is the solid, I₂(s)."),
    AR_, "Reference states in standard enthalpies of formation",
    "ΔfH° is zero only for an element in its reference state. For iodine at 298 K this is I₂(s); I₂(g) is formed "
    "from it by sublimation, which absorbs heat, so ΔfH°[I₂(g)] is positive (not zero). R explains A.",
    ["Reference state of iodine at 298 K = I₂(s) → ΔfH° = 0",
     "I₂(s) → I₂(g) is endothermic → ΔfH°[I₂(g)] > 0"],
    answer="A",
    why="Both statements are true and the choice of I₂(s) as the reference state is exactly why I₂(g) has a "
        "non-zero value.",
    ncert=f"{REF4}, standard enthalpy of formation", seconds=40)

add("Entropy and Gibbs energy", I, "multi_statement",
    ms("Which of the following statements are correct?",
       ["For a spontaneous process, the total entropy change of the system and the surroundings is positive.",
        "For a process at equilibrium, the total entropy change of the system and the surroundings is zero.",
        "The entropy of the system increases in every spontaneous process.",
        "Heating a gas at constant volume increases its entropy.",
        "ΔS = q/T gives the entropy change even when the heat q is absorbed irreversibly."]),
    multi("A", {"a": True, "b": True, "c": False, "d": True, "e": False},
          ["(a), (c) and (d) only", "(b), (d) and (e) only", "(a), (b), (c) and (d) only"]),
    "Entropy and the second law",
    "It is the TOTAL entropy (system + surroundings) that rises in a spontaneous change and stays constant at "
    "equilibrium. The system's own entropy may fall (e.g. water freezing below 273 K). Raising the temperature "
    "increases molecular motion and entropy. The relation ΔS = q/T uses the heat for a reversible path, q_rev.",
    ["(a) ΔS_total > 0 ✓", "(b) ΔS_total = 0 at equilibrium ✓", "(c) system entropy can decrease ✗",
     "(d) higher T → higher entropy ✓", "(e) needs q_rev ✗"],
    why="Options containing (c) or (e) are wrong; option (a), (c), (d) also drops the true statement (b).",
    ncert=f"{REF4}, entropy and spontaneity", seconds=70)

add("First law, work and enthalpy", I, "match_list",
    lists("Match List-I (quantity, for a closed system) with List-II (its expression).",
          ["Work done on n mol of an ideal gas in a reversible isothermal expansion from V_i to V_f",
           "Work done on a gas expanding against a constant external pressure p_ex",
           "Heat absorbed at constant volume",
           "Heat absorbed at constant pressure"],
          ["ΔH", "−p_ex (V_f − V_i)", "ΔU", "−2.303 nRT log (V_f/V_i)"]),
    match("B", M("IV II III I"), [M("II IV III I"), M("IV II I III"), M("II IV I III")]),
    "Expressions for work and heat in the first law",
    "With the IUPAC sign convention (work done on the system positive): reversible isothermal work is "
    "−2.303 nRT log(V_f/V_i); irreversible work against a constant pressure is −p_ex ΔV; q_V = ΔU and q_p = ΔH.",
    ["A → IV", "B → II", "C → III (ΔU = q_V)", "D → I (ΔH = q_p)"],
    why="The other codes swap the reversible and irreversible work expressions or the constant-volume and "
        "constant-pressure heats.",
    ncert=f"{REF4}, applications: work, enthalpy", seconds=50)

per_g = {"H₂": 286 / 2, "CH₄": 890 / 16, "C₂H₆": 1560 / 30, "C(graphite)": 393.5 / 12}
assert max(per_g, key=per_g.get) == "H₂" and close(per_g["H₂"], 143) and close(per_g["CH₄"], 55.6) \
    and close(per_g["C₂H₆"], 52.0) and close(per_g["C(graphite)"], 32.8)
add("Hess's law and enthalpies", A, "numerical",
    "The standard enthalpies of combustion (kJ mol⁻¹) of H₂(g), CH₄(g), C₂H₆(g) and C(graphite) are −286, −890, "
    "−1560 and −393.5 respectively. Which fuel gives out the most heat per gram burnt, and how much? "
    "(H = 1, C = 12)",
    Opts("C", "H₂, 143 kJ g⁻¹", ["C₂H₆, 52 kJ g⁻¹", "CH₄, 55.6 kJ g⁻¹", "C(graphite), 32.8 kJ g⁻¹"]),
    "Calorific value per gram from molar enthalpies of combustion",
    "Divide each enthalpy of combustion by the molar mass of the fuel to get the heat given out per gram.",
    ["H₂: 286/2 = 143 kJ g⁻¹", "CH₄: 890/16 = 55.6 kJ g⁻¹", "C₂H₆: 1560/30 = 52.0 kJ g⁻¹",
     "C: 393.5/12 = 32.8 kJ g⁻¹ → hydrogen is the highest"],
    why="Ethane gives the most heat per MOLE, not per gram. Methane is second per gram. Graphite gives the least "
        "per gram of the four.",
    ncert=f"{REF4}, enthalpy of combustion", seconds=90, checked=True)

add("Gibbs energy and K", A, "direct",
    "For a reaction, the equilibrium constant is less than 1 at 298 K but greater than 1 at 600 K. Assuming ΔH° "
    "and ΔS° do not change with temperature, the signs of ΔH° and ΔS° are:",
    Opts("D", "ΔH° positive, ΔS° positive",
         ["ΔH° negative, ΔS° negative", "ΔH° negative, ΔS° positive", "ΔH° positive, ΔS° negative"]),
    "ΔG° = ΔH° − TΔS° = −RT ln K",
    "K < 1 means ΔG° > 0; K > 1 means ΔG° < 0. ΔG° goes from positive at the lower temperature to negative at "
    "the higher one only if the TΔS° term, growing with T, overcomes a positive ΔH°, i.e. ΔH° > 0 and ΔS° > 0.",
    ["298 K: ΔG° > 0; 600 K: ΔG° < 0 → ΔG° decreases as T rises → ΔS° > 0",
     "ΔG° > 0 at low T with ΔS° > 0 → ΔH° > 0"],
    why="ΔH° < 0, ΔS° < 0 favours the reaction at LOW temperature (the reverse trend). ΔH° < 0, ΔS° > 0 gives "
        "ΔG° < 0 (K > 1) at every temperature. ΔH° > 0, ΔS° < 0 gives K < 1 at every temperature.",
    ncert=f"{REF4}, Gibbs energy change and equilibrium", seconds=60)

add("First law, work and enthalpy", A, "statement_pair",
    sp("When a system is taken through a complete cycle back to its initial state, ΔU = 0, but the net work "
       "done on the system need not be zero.",
       "For any cyclic process, the net heat absorbed by the system is zero."),
    SP_, "State functions and path functions in a cyclic process",
    "U is a state function, so ΔU = 0 for a cycle. Work and heat depend on the path, so a cycle can involve "
    "non-zero net work (as in a heat engine): Statement I is true. Then q = ΔU − w = −w, which is zero only if "
    "w happens to be zero: Statement II is false.",
    ["Cycle: ΔU = 0 (state function)", "q + w = 0 → q = −w; w ≠ 0 in general → q ≠ 0 in general",
     "I true, II false"],
    answer="C",
    why="Statement II treats heat as if it were a state function.",
    ncert=f"{REF4}, first law of thermodynamics; state functions", seconds=50)

# ==================================================================== 5. Solutions
topic("Solutions")
REF5 = f"{C12}, 'Solutions'"

add("Colligative properties", B, "direct",
    "Which of the following can act as a semipermeable membrane in an osmosis experiment, letting solvent "
    "molecules pass but not the larger solute molecules?",
    Opts("B", "Cellophane", ["Filter paper", "Muslin cloth", "A sheet of glass"]),
    "Semipermeable membranes",
    "NCERT names membranes of animal or vegetable origin (pig's bladder, parchment) and synthetic ones such as "
    "cellophane as semipermeable membranes: they contain a network of submicroscopic holes through which small "
    "solvent molecules can pass, but bigger solute molecules cannot.",
    ["Cellophane → semipermeable", "Filter paper and muslin let solutes through; glass lets nothing through"],
    why="Filter paper and muslin cloth have pores far too large to hold back dissolved solute molecules; glass "
        "is impermeable even to the solvent.",
    ncert=f"{REF5}, osmosis and osmotic pressure", seconds=25)

add("Colligative properties", B, "assertion_reason",
    ar("At the same temperature, a 1.0 M aqueous solution of glucose has a higher osmotic pressure than a 0.5 M "
       "aqueous solution of glucose.",
       "For a dilute solution, the osmotic pressure is proportional to the molar concentration of the solute "
       "(π = CRT)."),
    AR_, "Osmotic pressure and concentration",
    "π = CRT: at a fixed temperature the osmotic pressure is directly proportional to C, so doubling the "
    "molarity doubles π. R explains A.",
    ["π = CRT", "C doubles from 0.5 M to 1.0 M → π doubles → A follows from R"],
    answer="A",
    why="Both statements are true and the relation in R is the direct reason for A.",
    ncert=f"{REF5}, osmosis and osmotic pressure", seconds=30)

add("Raoult's law and ideal solutions", B, "statement_pair",
    sp("The relative lowering of vapour pressure of a dilute solution of a non-volatile solute depends on the "
       "chemical nature of the solute.",
       "At a given temperature, the vapour pressure of a solution of a non-volatile solute in a solvent is lower "
       "than that of the pure solvent."),
    SP_, "Relative lowering of vapour pressure as a colligative property",
    "By Raoult's law, (p° − p)/p° = x(solute): it depends only on the proportion of solute particles, not on "
    "their nature, so Statement I is false. Solute particles occupy part of the surface and reduce the "
    "escaping tendency of the solvent, so the vapour pressure is lowered: Statement II is true.",
    ["I: (p° − p)/p° = x₂ → independent of the nature of the solute → false",
     "II: p = x₁p° < p° → true"],
    answer="D",
    why="Statement I contradicts the colligative nature of vapour-pressure lowering.",
    ncert=f"{REF5}, relative lowering of vapour pressure", seconds=35)

n1 = 90 / 18
n2_exact = n1 * 0.01 / 0.99
assert close(n2_exact * 60, 3.03) and close(n2_exact * 180, 9.09) and close(n1 * 0.1 / 0.9 * 60, 33.3) \
    and close(n1 * 0.001 / 0.999 * 60, 0.3003)
add("Raoult's law and ideal solutions", I, "numerical",
    "How many grams of urea (molar mass 60 g mol⁻¹, non-volatile) must be dissolved in 90 g of water to lower "
    "the vapour pressure of the water by 1.0% at a given temperature? Use Raoult's law exactly, "
    "(p° − p)/p° = n₂/(n₁ + n₂). (H₂O = 18 g mol⁻¹)",
    Opts("B", "3.03 g", ["9.09 g", "33.3 g", "0.303 g"]),
    "Raoult's law for a solution of a non-volatile solute",
    "Lowering by 1.0% means the mole fraction of urea is 0.010. Solve n₂/(n₁ + n₂) = 0.010 with n₁ = 5 mol.",
    ["n₁ = 90/18 = 5.00 mol", "n₂/(5 + n₂) = 0.010 → n₂ = 0.0505 mol", "Mass = 0.0505 × 60 = 3.03 g"],
    why="9.09 g uses the molar mass of glucose (180). 33.3 g reads 1% as a mole fraction of 0.10. 0.303 g reads it "
        "as 0.001.",
    ncert=f"{REF5}, relative lowering of vapour pressure", seconds=75, checked=True)

assert 0.040 * 3 > 0.10  # particle concentration in Y (Na2SO4, i = 3) exceeds X (urea)
add("van't Hoff factor", I, "direct",
    "Two aqueous solutions at the same temperature are separated by a semipermeable membrane: compartment X "
    "contains 0.10 M urea and compartment Y contains 0.040 M Na₂SO₄ (completely dissociated). What happens?",
    Opts("D", "Water flows from X to Y, because Y has the higher concentration of solute particles.",
         ["Water flows from Y to X, because the urea solution has the higher molarity.",
          "There is no net flow of water, because the two solutions are isotonic.",
          "Urea passes from X to Y until the two molarities become equal."]),
    "Osmosis with an electrolyte: the van't Hoff factor",
    "Osmotic pressure depends on the total concentration of solute particles, iC. Na₂SO₄ → 2Na⁺ + SO₄²⁻ "
    "(i = 3), so Y has 3 × 0.040 = 0.12 M of particles against 0.10 M in X. Solvent moves into the solution "
    "with the higher osmotic pressure.",
    ["X: i = 1 → 0.10 M particles", "Y: i = 3 → 0.12 M particles", "Water moves from X (lower π) to Y (higher π)"],
    why="Comparing molarities without the van't Hoff factor gives the wrong direction. The solutions are not "
        "isotonic (0.10 ≠ 0.12). A semipermeable membrane does not let the solute through.",
    ncert=f"{REF5}, osmosis; abnormal molar masses (van't Hoff factor)", seconds=55)

add("Colligative properties", I, "statement_pair",
    sp("The molal depression constant (K_f) of a solvent depends on the molality of the solution.",
       "The molal depression constant of water is 1.86 K kg mol⁻¹."),
    SP_, "Cryoscopic constant",
    "K_f is a property of the solvent alone (ΔT_f = K_f m); the depression ΔT_f depends on molality, but K_f "
    "does not. Statement I is false. NCERT lists K_f = 1.86 K kg mol⁻¹ for water: Statement II is true.",
    ["I: K_f = ΔT_f/m is constant for a given solvent → false", "II: K_f(water) = 1.86 K kg mol⁻¹ → true"],
    answer="D",
    why="Statement I confuses ΔT_f, which depends on m, with the constant K_f.",
    ncert=f"{REF5}, depression of freezing point", seconds=30)

add("Colligative properties", I, "multi_statement",
    ms("Which of the following statements about osmosis and reverse osmosis are correct?",
       ["Reverse osmosis is used for the desalination of sea water.",
        "In reverse osmosis, pure solvent passes from the solution side through the membrane.",
        "A film of cellulose acetate, permeable to water but not to the impurities and ions in sea water, is "
        "used as the membrane in desalination by reverse osmosis.",
        "At a given molar concentration and temperature, the osmotic pressure depends on the chemical nature of "
        "the non-electrolyte solute.",
        "At a given temperature, the osmotic pressure of a dilute solution is proportional to its molarity."]),
    multi("B", {"a": True, "b": True, "c": True, "d": False, "e": True},
          ["(a), (b) and (d) only", "(b), (c), (d) and (e) only", "(a), (c) and (e) only"]),
    "Osmotic pressure and reverse osmosis",
    "If a pressure larger than the osmotic pressure is applied to the solution, pure solvent is squeezed out "
    "through the membrane: reverse osmosis, used with cellulose acetate membranes to desalinate sea water. "
    "π = CRT is a colligative property and does not depend on what the (non-electrolyte) solute is.",
    ["(a), (b), (c) ✓ (NCERT: reverse osmosis and water purification)", "(d) ✗ colligative",
     "(e) ✓ π = CRT"],
    why="Every other option includes the false statement (d) or leaves out one of the true ones.",
    ncert=f"{REF5}, reverse osmosis and water purification", seconds=60)

i_ba = 0.2325 / (1.86 * 0.05)
alpha_ba = (i_ba - 1) / (3 - 1)
assert close(i_ba, 2.5) and close(alpha_ba, 0.75) and close((i_ba - 1) / 3, 0.5) and close((i_ba - 1) / i_ba, 0.6)
add("van't Hoff factor", A, "numerical",
    "A 0.050 m aqueous solution of barium nitrate, Ba(NO₃)₂, freezes at −0.2325 °C. The apparent degree of "
    "dissociation of the salt in this solution is (K_f of water = 1.86 K kg mol⁻¹; freezing point of water = "
    "0 °C):",
    Opts("A", "75%", ["50%", "25%", "60%"]),
    "Degree of dissociation from the van't Hoff factor",
    "ΔT_f = iK_f m gives i. For Ba(NO₃)₂ ⇌ Ba²⁺ + 2NO₃⁻ one formula unit gives 3 ions, so "
    "i = 1 − α + 3α = 1 + 2α.",
    ["i = 0.2325/(1.86 × 0.050) = 2.5", "1 + 2α = 2.5 → α = 0.75 = 75%"],
    why="50% divides (i − 1) by 3 instead of by (3 − 1). 25% is 1 − α. 60% uses (i − 1)/i.",
    ncert=f"{REF5}, abnormal molar masses (van't Hoff factor)", seconds=90, checked=True)

m_vp = 0.02 / (0.98 * 0.018)
dtf = 1.86 * m_vp
assert close(m_vp, 1.134) and close(dtf, 2.109) and close(1.86 * 0.02, 0.0372) and close(2 * dtf, 4.22)
add("Colligative properties", A, "numerical",
    "The vapour pressure of a dilute aqueous solution of a non-volatile non-electrolyte is 2.0% lower than that "
    "of pure water at the same temperature. Using Raoult's law exactly, the depression in the freezing point of "
    "this solution is (K_f of water = 1.86 K kg mol⁻¹; H₂O = 18 g mol⁻¹):",
    Opts("D", "2.11 K", ["0.037 K", "1.13 K", "4.22 K"]),
    "Linking two colligative properties through the molality",
    "The 2.0% lowering gives x₂ = 0.020, i.e. n₂/n₁ = 0.020/0.980. Convert this ratio into molality (moles of "
    "solute per kg of water), then use ΔT_f = K_f m.",
    ["n₂/n₁ = 0.02/0.98 = 0.0204 mol of solute per mol of water",
     "m = 0.0204/0.018 kg = 1.13 mol kg⁻¹", "ΔT_f = 1.86 × 1.13 = 2.11 K"],
    why="0.037 K multiplies K_f by the mole fraction instead of the molality. 1.13 K is the molality itself "
        "(K_f left out). 4.22 K counts a van't Hoff factor of 2 for a non-electrolyte.",
    ncert=f"{REF5}, relative lowering of vapour pressure; depression of freezing point", seconds=120, checked=True)

add("Raoult's law and ideal solutions", A, "statement_pair",
    sp("For a dilute solution of a non-volatile solute, the relative lowering of vapour pressure is "
       "approximately equal to n₂/n₁, the ratio of the moles of solute to the moles of solvent.",
       "At the same temperature, a 1 m aqueous solution of glucose and a 1 m aqueous solution of urea show the "
       "same relative lowering of vapour pressure."),
    SP_, "Relative lowering of vapour pressure and molality",
    "x₂ = n₂/(n₁ + n₂) ≈ n₂/n₁ when n₂ ≪ n₁, so Statement I is true. Two 1 m aqueous solutions both contain 1 mol "
    "of solute per 1000 g (55.5 mol) of water, so their mole fractions of solute, and hence their relative "
    "lowerings, are the same whatever the non-electrolyte: Statement II is true.",
    ["I: n₂ ≪ n₁ → x₂ ≈ n₂/n₁ → true", "II: same molality, same solvent → same x₂ → true"],
    answer="A",
    why="The molar masses of glucose and urea are different, but the relative lowering depends only on the "
        "number of moles of solute per mole of solvent, which is equal in equimolal solutions.",
    ncert=f"{REF5}, relative lowering of vapour pressure", seconds=50)

# ==================================================================== 6. Equilibrium
topic("Equilibrium")
REF6 = f"{C11}, 'Equilibrium'"

h_conc = 10 ** -4.7
assert close(h_conc, 2.0e-5, 0.01) and close(1e-14 / h_conc, 5.0e-10, 0.01)
add("Acids, bases and pH", B, "numerical",
    "The pH of an aqueous solution at 298 K is 4.7. The concentration of H₃O⁺ ions in it is (log 2 = 0.30):",
    Opts("B", "2.0 × 10⁻⁵ mol L⁻¹", ["5.0 × 10⁻⁵ mol L⁻¹", "2.0 × 10⁻⁴ mol L⁻¹", "5.0 × 10⁻¹⁰ mol L⁻¹"]),
    "pH = −log[H₃O⁺]; finding the concentration from the pH",
    "[H₃O⁺] = 10⁻ᵖᴴ = 10⁻⁴·⁷ = 10⁰·³ × 10⁻⁵, and 10⁰·³ = 2 because log 2 = 0.30.",
    ["[H₃O⁺] = 10⁻⁴·⁷ = 10⁰·³ × 10⁻⁵", "= 2.0 × 10⁻⁵ mol L⁻¹"],
    why="5.0 × 10⁻⁵ is 10⁻⁴·³, which reverses the decimal part of the pH. 2.0 × 10⁻⁴ "
        "misplaces the power of ten. 5.0 × 10⁻¹⁰ is [OH⁻], not [H₃O⁺].",
    ncert=f"{REF6}, the pH scale", seconds=40, checked=True)

assert close(0.030 * 3.0 / 1.0, 0.090)
add("Physical equilibria and Henry's law", B, "numerical",
    "At 298 K, 0.030 g of a gas dissolves in 1.0 L of water when its partial pressure above the water is "
    "1.0 bar. Assuming Henry's law holds, the mass of the gas that dissolves in 1.0 L of water at 298 K when its "
    "partial pressure is 3.0 bar is:",
    Opts("D", "0.090 g", ["0.010 g", "0.030 g", "0.27 g"]),
    "Henry's law: solubility of a gas is proportional to its partial pressure",
    "At constant temperature the mass of gas dissolved in a given amount of solvent is directly proportional to "
    "the pressure of the gas above the solvent.",
    ["m ∝ p", "m = 0.030 g × (3.0/1.0) = 0.090 g"],
    why="0.010 g takes solubility inversely proportional to pressure. 0.030 g ignores the pressure change. "
        "0.27 g takes solubility proportional to p².",
    ncert=f"{REF6}, equilibrium involving dissolution of gas in liquids (Henry's law)", seconds=30, checked=True)

add("Kp, Kc and Le Chatelier", B, "direct",
    "For the heterogeneous equilibrium Fe₃O₄(s) + 4H₂(g) ⇌ 3Fe(s) + 4H₂O(g), the expression for K_p is:",
    Opts("A", "p⁴(H₂O) / p⁴(H₂)",
         ["p⁴(H₂) / p⁴(H₂O)", "p³(Fe) p⁴(H₂O) / [p(Fe₃O₄) p⁴(H₂)]", "p(H₂O) / p(H₂)"]),
    "Equilibrium constant of a heterogeneous equilibrium",
    "Pure solids have constant 'concentrations' and are left out of the equilibrium constant expression. Each "
    "gaseous partial pressure is raised to its stoichiometric coefficient, products over reactants.",
    ["Leave out Fe₃O₄(s) and Fe(s)", "K_p = p⁴(H₂O)/p⁴(H₂)"],
    why="The inverted expression is K_p of the reverse reaction. Including solids is incorrect. Dropping the "
        "power 4 ignores the coefficients.",
    ncert=f"{REF6}, heterogeneous equilibria", seconds=30)

add("Hydrolysis and buffers", B, "assertion_reason",
    ar("Adding sodium acetate to an aqueous solution of acetic acid decreases the degree of ionisation of the "
       "acetic acid.",
       "The acetate ions supplied by the salt shift the equilibrium CH₃COOH ⇌ H⁺ + CH₃COO⁻ to the left."),
    AR_, "Common ion effect",
    "Sodium acetate is a strong electrolyte and supplies a large amount of the common ion CH₃COO⁻. By Le "
    "Chatelier's principle the ionisation equilibrium of the weak acid shifts to the left, so a smaller fraction "
    "of the acid ionises. R explains A.",
    ["CH₃COONa → Na⁺ + CH₃COO⁻ (common ion)", "Equilibrium shifts left → α of CH₃COOH falls"],
    answer="A",
    why="Both are true, and the shift caused by the common ion is exactly why the degree of ionisation falls.",
    ncert=f"{REF6}, common ion effect in the ionisation of acids and bases", seconds=35)

x_b = 4.0 / (1 + 4.0)
assert close(x_b, 0.80)
add("Kp, Kc and Le Chatelier", B, "numerical",
    "For the isomerisation A(g) ⇌ B(g), K_c = 4.0 at a certain temperature. 1.0 mol of A is placed in a closed "
    "1.0 L vessel at this temperature. The concentration of B at equilibrium is:",
    Opts("C", "0.80 mol L⁻¹", ["0.20 mol L⁻¹", "0.25 mol L⁻¹", "0.50 mol L⁻¹"]),
    "Equilibrium concentrations from K_c",
    "If x mol L⁻¹ of A changes into B, then [B] = x and [A] = 1.0 − x at equilibrium.",
    ["K_c = x/(1.0 − x) = 4.0", "x = 4.0 − 4.0x → 5x = 4.0 → x = 0.80 mol L⁻¹"],
    why="0.20 mol L⁻¹ is [A] at equilibrium. 0.25 mol L⁻¹ is 1/K_c. 0.50 mol L⁻¹ assumes K_c = 1.",
    ncert=f"{REF6}, calculating equilibrium concentrations", seconds=40, checked=True)

h_ratio = math.sqrt(1.8e-4 * 0.1) / math.sqrt(1.8e-5 * 0.1)
assert close(h_ratio, 3.162)
add("Acids, bases and pH", I, "numerical",
    "At 298 K, K_a of methanoic acid (HCOOH) is 1.8 × 10⁻⁴ and K_a of ethanoic acid (CH₃COOH) is 1.8 × 10⁻⁵. "
    "Using [H₃O⁺] ≈ √(K_a c), the ratio of [H₃O⁺] in a 0.1 M solution of methanoic acid to that in a 0.1 M "
    "solution of ethanoic acid is (√10 = 3.16):",
    Opts("B", "3.16", ["10", "1", "0.316"]),
    "Relative strengths of weak acids at the same concentration",
    "For a weak acid that ionises only slightly, [H₃O⁺] = √(K_a c). At equal c the ratio is √(K_a1/K_a2).",
    ["Ratio = √(1.8 × 10⁻⁴ / 1.8 × 10⁻⁵) = √10", "= 3.16"],
    why="10 compares the K_a values directly, forgetting the square root. 1 assumes equal concentrations give "
        "equal acidity. 0.316 inverts the ratio.",
    ncert=f"{REF6}, ionisation constants of weak acids", seconds=50, checked=True)

oh = 1e-14 / 1e-10
m2 = oh / 2
ksp_m = m2 * oh ** 2
assert close(oh, 1e-4) and close(ksp_m, 5e-13) and close(oh * oh ** 2, 1e-12) and close(oh ** 2, 1e-8) \
    and close(m2 * oh, 5e-9)
add("Solubility product", I, "numerical",
    "A saturated solution of a sparingly soluble hydroxide M(OH)₂ in water at 298 K has pH 10.0. The solubility "
    "product of M(OH)₂ is (K_w = 1.0 × 10⁻¹⁴; all the OH⁻ comes from the dissolved hydroxide):",
    Opts("D", "5.0 × 10⁻¹³", ["1.0 × 10⁻¹²", "1.0 × 10⁻⁸", "5.0 × 10⁻⁹"]),
    "K_sp from the pH of a saturated solution",
    "pH 10 gives pOH 4, so [OH⁻] = 1.0 × 10⁻⁴ M. Each M(OH)₂ that dissolves gives one M²⁺ and two OH⁻, so "
    "[M²⁺] = ½[OH⁻].",
    ["[OH⁻] = 10⁻⁴ M; [M²⁺] = 5.0 × 10⁻⁵ M", "K_sp = [M²⁺][OH⁻]² = 5.0 × 10⁻⁵ × (10⁻⁴)² = 5.0 × 10⁻¹³"],
    why="1.0 × 10⁻¹² takes [M²⁺] equal to [OH⁻]. 1.0 × 10⁻⁸ is just [OH⁻]². 5.0 × 10⁻⁹ forgets to square [OH⁻].",
    ncert=f"{REF6}, solubility equilibria of sparingly soluble salts", seconds=75, checked=True)

add("Kp, Kc and Le Chatelier", I, "assertion_reason",
    ar("Adding a catalyst to a reaction mixture at equilibrium does not change the composition of the "
       "equilibrium mixture.",
       "A catalyst lowers the activation energies of the forward and the backward reactions by the same amount, "
       "so it speeds up both reactions equally."),
    AR_, "Effect of a catalyst on equilibrium",
    "Because both the forward and the backward rates are increased by the same factor, the catalyst only helps "
    "the system reach equilibrium sooner; the equilibrium constant and the equilibrium composition stay the "
    "same. R explains A.",
    ["Catalyst: same lowering of Eₐ for both directions", "Both rates rise equally → K unchanged → composition "
     "unchanged"],
    answer="A",
    why="Both statements are true and R gives the reason a catalyst cannot shift an equilibrium.",
    ncert=f"{REF6}, effect of a catalyst", seconds=35)

add("Acids, bases and pH", I, "statement_pair",
    sp("Since HCl is a stronger acid than CH₃COOH, the chloride ion is a stronger base than the acetate ion.",
       "NH₄⁺ is the conjugate acid of NH₃."),
    SP_, "Conjugate acid–base pairs and their strengths",
    "The stronger an acid, the weaker its conjugate base: Cl⁻ is a much weaker base than CH₃COO⁻, so Statement I "
    "is false. NH₃ accepts a proton to give NH₄⁺, its conjugate acid: Statement II is true.",
    ["Strong acid ↔ weak conjugate base → Cl⁻ weaker than CH₃COO⁻ → I false",
     "NH₃ + H⁺ → NH₄⁺ → conjugate acid → II true"],
    answer="D",
    why="Statement I reverses the inverse relation between the strength of an acid and that of its conjugate "
        "base.",
    ncert=f"{REF6}, Brönsted–Lowry acids and bases", seconds=35)

add("Physical equilibria and Henry's law", I, "direct",
    "Water and its vapour are in equilibrium in a closed vessel at a constant temperature, with some liquid "
    "left. The volume of the vessel is suddenly increased at the same temperature, liquid water still remaining "
    "afterwards. When equilibrium is re-established, the pressure of the water vapour:",
    Opts("B", "is the same as before",
         ["is lower than before, in proportion to the increase in volume",
          "is higher than before, because more liquid evaporates",
          "becomes zero, because the vapour spreads into the extra space"]),
    "Equilibrium vapour pressure depends only on temperature",
    "Right after the expansion the vapour pressure falls, so evaporation exceeds condensation; more liquid "
    "evaporates until the rates are equal again. That happens at the same equilibrium vapour pressure, which is "
    "fixed by the temperature as long as both phases are present.",
    ["Expansion → p falls → net evaporation", "New equilibrium at the same T → same vapour pressure"],
    why="Boyle's-law reasoning applies only to a fixed amount of gas; here extra liquid evaporates. The vapour "
        "pressure does not exceed the equilibrium value or fall to zero while liquid remains.",
    ncert=f"{REF6}, equilibrium in physical processes: liquid–vapour equilibrium", seconds=45)

add("Acids, bases and pH", I, "match_list",
    lists("Match List-I (aqueous solution at 298 K, assuming complete ionisation) with List-II (its pH). "
          "(K_w = 1.0 × 10⁻¹⁴)",
          ["0.01 M HNO₃", "0.01 M NaOH", "5 × 10⁻⁵ M Ba(OH)₂", "5 × 10⁻⁵ M H₂SO₄ (both protons ionised)"],
          ["4", "12", "2", "10"]),
    match("C", M("III II IV I"), [M("III II I IV"), M("II III IV I"), M("I II IV III")]),
    "pH of solutions of strong acids and bases",
    "Find [H₃O⁺] or [OH⁻] from the formula and concentration, then pH = −log[H₃O⁺] and pH = 14 − pOH.",
    ["HNO₃: [H⁺] = 10⁻² → pH 2 (III)", "NaOH: [OH⁻] = 10⁻² → pOH 2 → pH 12 (II)",
     "Ba(OH)₂: [OH⁻] = 2 × 5 × 10⁻⁵ = 10⁻⁴ → pH 10 (IV)", "H₂SO₄: [H⁺] = 10⁻⁴ → pH 4 (I)"],
    why="The other codes forget the factor 2 for the dibasic acid or the diacidic base, or mix up pH and pOH.",
    ncert=f"{REF6}, the pH scale", seconds=60)

alpha_vd = (92 - 2 * 38.333) / (2 * 38.333)
assert close(alpha_vd, 0.20) and close((92 - 76.667) / 92, 0.1667)
add("Kp, Kc and Le Chatelier", A, "numerical",
    "N₂O₄ partly dissociates on heating: N₂O₄(g) ⇌ 2NO₂(g). At a certain temperature the vapour density of the "
    "equilibrium mixture is 38.33 (H = 1). The degree of dissociation of N₂O₄ is (N = 14, O = 16):",
    Opts("A", "20%", ["16.7%", "40%", "83.3%"]),
    "Degree of dissociation from the vapour density of an equilibrium mixture",
    "Starting with 1 mol of N₂O₄, dissociation α gives (1 − α) + 2α = 1 + α mol of gas. The mass is unchanged, "
    "so the mean molar mass falls in the ratio 1/(1 + α).",
    ["M(N₂O₄) = 92 g mol⁻¹; M(mixture) = 2 × 38.33 = 76.67 g mol⁻¹",
     "1 + α = 92/76.67 = 1.20 → α = 0.20 = 20%"],
    why="16.7% divides the change in molar mass by 92 instead of by 76.67. 40% counts the moles of NO₂ formed "
        "(2α). 83.3% is 76.67/92, the reciprocal of 1 + α.",
    ncert=f"{REF6}, homogeneous equilibria; equilibrium constant in gaseous systems", seconds=90, checked=True)

# 100 mL 0.1 M CH3COOH = 10 mmol ; x mmol NaOH -> salt x, acid 10 - x ; ratio 2
x_naoh = 10 * 2 / 3
assert close(x_naoh / 0.1, 66.7) and close(4.74 + math.log10(x_naoh / (10 - x_naoh)), 5.04, 0.001)
add("Hydrolysis and buffers", A, "numerical",
    "What volume of 0.10 M NaOH must be added to 100 mL of 0.10 M acetic acid at 298 K to obtain a buffer of "
    "pH 5.04? (pK_a of CH₃COOH = 4.74; log 2 = 0.30)",
    Opts("D", "66.7 mL", ["50.0 mL", "33.3 mL", "100 mL"]),
    "Preparing an acidic buffer by part-neutralising a weak acid",
    "NaOH converts part of the acid into acetate. Henderson equation: pH = pK_a + log([salt]/[acid]); here the "
    "ratio must be 10⁰·³⁰ = 2.",
    ["Acid taken = 10 mmol; x mmol NaOH gives x mmol CH₃COO⁻ and leaves (10 − x) mmol CH₃COOH",
     "x/(10 − x) = 2 → x = 6.67 mmol", "V = 6.67 mmol / 0.10 M = 66.7 mL"],
    why="50.0 mL gives a 1 : 1 ratio, i.e. pH = pK_a = 4.74. 33.3 mL gives a salt-to-acid ratio of 1/2 "
        "(pH 4.44). 100 mL neutralises all the acid, leaving no buffer.",
    ncert=f"{REF6}, buffer solutions", seconds=120, checked=True)

s_vals = {"pure water": math.sqrt(1.8e-10), "0.010 M NaCl": 1.8e-10 / 0.010, "0.020 M AgNO₃": 1.8e-10 / 0.020,
          "0.020 M CaCl₂": 1.8e-10 / 0.040}
assert sorted(s_vals, key=s_vals.get, reverse=True) == ["pure water", "0.010 M NaCl", "0.020 M AgNO₃",
                                                         "0.020 M CaCl₂"]
add("Solubility product", A, "direct",
    "At 298 K, K_sp of AgCl is 1.8 × 10⁻¹⁰. Which of the following arranges the molar solubility of AgCl in the "
    "given media in DECREASING order? (The salts NaCl, AgNO₃ and CaCl₂ are completely dissociated.)",
    Opts("B", "Pure water > 0.010 M NaCl > 0.020 M AgNO₃ > 0.020 M CaCl₂",
         ["Pure water > 0.020 M CaCl₂ > 0.020 M AgNO₃ > 0.010 M NaCl",
          "0.020 M CaCl₂ > 0.020 M AgNO₃ > 0.010 M NaCl > Pure water",
          "Pure water > 0.020 M AgNO₃ = 0.020 M CaCl₂ > 0.010 M NaCl"]),
    "Common ion effect on solubility",
    "A common ion (Ag⁺ or Cl⁻) lowers the solubility: s ≈ K_sp/[common ion]. The larger the concentration of the "
    "common ion, the lower the solubility. 0.020 M CaCl₂ gives 0.040 M Cl⁻.",
    ["Water: s = √(1.8 × 10⁻¹⁰) = 1.34 × 10⁻⁵ M", "0.010 M Cl⁻: s = 1.8 × 10⁻⁸ M",
     "0.020 M Ag⁺: s = 9.0 × 10⁻⁹ M", "0.040 M Cl⁻ (from CaCl₂): s = 4.5 × 10⁻⁹ M"],
    why="Treating CaCl₂ as giving 0.020 M Cl⁻ (forgetting its two chloride ions) makes it look equal to AgNO₃; "
        "the reversed orders put the common-ion media above pure water.",
    ncert=f"{REF6}, common ion effect on solubility of ionic salts", seconds=90)

add("Acids, bases and pH", A, "multi_statement",
    ms("Which of the following statements are correct?",
       ["AlCl₃ is a Lewis acid.", "NH₄⁺ can act as a Brönsted acid.", "F⁻ can act as a Lewis base.",
        "BF₃ is a Brönsted acid.", "H₃O⁺ is the conjugate base of H₂O."]),
    multi("C", {"a": True, "b": True, "c": True, "d": False, "e": False},
          ["(a), (b), (c) and (d) only", "(b), (c) and (e) only", "(a) and (c) only"]),
    "Lewis and Brönsted–Lowry concepts",
    "AlCl₃ (aluminium with an incomplete octet) accepts an electron pair: Lewis acid. NH₄⁺ can donate a proton "
    "(to give NH₃): Brönsted acid. F⁻ has lone pairs to donate: Lewis base. BF₃ has no hydrogen to donate, so it "
    "is a Lewis acid but not a Brönsted acid. H₃O⁺ is the conjugate ACID of H₂O (H₂O + H⁺).",
    ["(a) ✓ electron-pair acceptor", "(b) ✓ proton donor", "(c) ✓ electron-pair donor",
     "(d) ✗ no proton to donate", "(e) ✗ conjugate acid, not base"],
    why="Options containing (d) or (e) are wrong; '(a) and (c) only' leaves out the true statement (b).",
    ncert=f"{REF6}, acids, bases and salts: Brönsted–Lowry and Lewis concepts", seconds=60)

ph_nh4cn = 7 + 0.5 * (9.31 - 4.75)
assert close(ph_nh4cn, 9.28) and close(7 - 0.5 * (9.31 - 4.75), 4.72) and close(7 + (9.31 - 4.75), 11.56)
add("Hydrolysis and buffers", A, "numerical",
    "The pH of an aqueous solution of ammonium cyanide, NH₄CN, at 298 K is (pK_a of HCN = 9.31; pK_b of NH₃ = "
    "4.75; pK_w = 14):",
    Opts("A", "9.28", ["4.72", "11.56", "7.00"]),
    "pH of a solution of a salt of a weak acid and a weak base",
    "Both ions hydrolyse; for such a salt pH = 7 + ½(pK_a − pK_b), independent of concentration. CN⁻ (from the "
    "much weaker acid HCN) hydrolyses more than NH₄⁺, so the solution is basic.",
    ["pH = 7 + ½(9.31 − 4.75)", "= 7 + 2.28 = 9.28"],
    why="4.72 uses 7 − ½(pK_a − pK_b), the wrong sign. 11.56 leaves out the factor ½. 7.00 assumes the two ions "
        "hydrolyse equally, which is true only when pK_a = pK_b.",
    ncert=f"{REF6}, hydrolysis of salts and the pH of their solutions", seconds=55, checked=True)

# ==================================================================== 7. Redox Reactions and Electrochemistry
topic("Redox Reactions and Electrochemistry")
REF7R = f"{C11}, 'Redox Reactions'"
REF7E = f"{C12}, 'Electrochemistry'"

on_s = (-2 - 3 * (-2)) / 2
assert on_s == 2
add("Oxidation number and balancing", B, "numerical",
    "The average oxidation number of sulphur in the thiosulphate ion, S₂O₃²⁻, is:",
    Opts("B", "+2", ["+4", "+6", "+2.5"]),
    "Oxidation number from the overall charge",
    "Take oxygen as −2. The sum of the oxidation numbers of all the atoms equals the charge on the ion.",
    ["2x + 3(−2) = −2", "2x = +4 → x = +2"],
    why="+4 forgets to share the total between the two S atoms. +6 is the value in sulphate. +2.5 is the average "
        "in the tetrathionate ion, S₄O₆²⁻.",
    ncert=f"{REF7R}, oxidation number", seconds=30, checked=True)

add("Electrode potential and cells", B, "direct",
    "In a Daniell cell, the salt bridge that connects the two half-cell solutions usually contains:",
    Opts("D", "a solution of KCl or NH₄NO₃ set in agar–agar gel",
         ["concentrated sulphuric acid", "pure distilled water", "liquid mercury"]),
    "Function and composition of a salt bridge",
    "The salt bridge is a U-tube filled with a solution of an inert electrolyte such as KCl or NH₄NO₃, usually "
    "solidified with agar–agar. Its ions migrate to keep both half-cells electrically neutral and so complete "
    "the circuit.",
    ["Needs mobile ions that do not react with the half-cell contents → KCl or NH₄NO₃ in agar–agar"],
    why="Pure water hardly conducts; concentrated acid would react and is not used; mercury is a metal conductor, "
        "which would not carry ions between the solutions.",
    ncert=f"{REF7E}, galvanic cells", seconds=25)

add("Oxidation number and balancing", B, "assertion_reason",
    ar("In the reaction 2Na(s) + Cl₂(g) → 2NaCl(s), sodium is oxidised.",
       "Each sodium atom loses an electron, and its oxidation number increases from 0 to +1."),
    AR_, "Oxidation as loss of electrons / increase in oxidation number",
    "Oxidation is the loss of electrons, equivalently an increase in oxidation number. Na → Na⁺ + e⁻ is exactly "
    "that, so R explains A; chlorine, which gains the electrons, is reduced.",
    ["Na(0) → Na⁺(+1) + e⁻ → oxidation", "Cl₂(0) + 2e⁻ → 2Cl⁻(−1) → reduction"],
    answer="A",
    why="Both statements are true and the loss of electrons in R is the definition of the oxidation stated in A.",
    ncert=f"{REF7R}, redox reactions in terms of electron transfer", seconds=25)

add("Conductance and Kohlrausch's law", B, "statement_pair",
    sp("According to Kohlrausch's law, the limiting molar conductivity of an electrolyte is the difference "
       "between the limiting molar conductivities of its cation and its anion.",
       "The conductivity of a solution is the conductance of the volume of solution that contains one mole of "
       "the electrolyte."),
    SP_, "Kohlrausch's law; conductivity and molar conductivity",
    "Kohlrausch's law states that Λ°m is the SUM of the individual contributions of the anion and the cation "
    "(e.g. Λ°m = ν₊λ°₊ + ν₋λ°₋): Statement I is false. Conductivity (κ) is the conductance of a unit volume (a "
    "1 cm cube or 1 m cube); the conductance of the volume containing one mole relates to molar conductivity: "
    "Statement II is false.",
    ["I: sum, not difference → false", "II: describes molar conductivity, not conductivity → false"],
    answer="B",
    why="Statement I subtracts where the law adds; Statement II confuses κ with Λm.",
    ncert=f"{REF7E}, conductance of electrolytic solutions; Kohlrausch's law", seconds=40)

g_star = 1.5 / 1.2
kappa = g_star / 500
lam = kappa * 1000 / 0.05
assert close(g_star, 1.25) and close(lam, 50.0) and close((1.2 / 1.5) / 500 * 1000 / 0.05, 32.0) \
    and close(kappa / 0.05, 0.050)
add("Conductance and Kohlrausch's law", I, "numerical",
    "The electrodes of a conductivity cell each have an area of cross-section of 1.2 cm² and are 1.5 cm apart. "
    "Filled with a 0.050 mol L⁻¹ solution of an electrolyte, the cell shows a resistance of 500 Ω. The molar "
    "conductivity of the solution is:",
    Opts("A", "50 S cm² mol⁻¹", ["32 S cm² mol⁻¹", "0.050 S cm² mol⁻¹", "2.5 × 10⁻³ S cm² mol⁻¹"]),
    "Cell constant, conductivity and molar conductivity",
    "Cell constant G* = l/A; κ = G*/R; Λm (S cm² mol⁻¹) = κ (S cm⁻¹) × 1000/c (mol L⁻¹).",
    ["G* = 1.5/1.2 = 1.25 cm⁻¹", "κ = 1.25/500 = 2.5 × 10⁻³ S cm⁻¹",
     "Λm = 2.5 × 10⁻³ × 1000/0.050 = 50 S cm² mol⁻¹"],
    why="32 S cm² mol⁻¹ takes the cell constant as A/l. 0.050 leaves out the factor 1000 (cm³ per litre). "
        "2.5 × 10⁻³ is the conductivity in S cm⁻¹, not the molar conductivity.",
    ncert=f"{REF7E}, measurement of the conductivity of ionic solutions", seconds=75, checked=True)

gain, loss = 5 * 1, 1 * 5  # 5 Cl: 0 -> -1 ; 1 Cl: 0 -> +5
assert gain == loss and (5, 1) == (5, 1)
add("Oxidation number and balancing", I, "numerical",
    "In hot, concentrated alkali, chlorine reacts as 3Cl₂ + 6OH⁻ → 5Cl⁻ + ClO₃⁻ + 3H₂O. In this reaction, the "
    "ratio of the number of chlorine atoms reduced to the number oxidised is:",
    Opts("C", "5 : 1", ["1 : 5", "1 : 1", "3 : 1"]),
    "Disproportionation: one element is both oxidised and reduced",
    "Chlorine (oxidation number 0) goes to Cl⁻ (−1, reduction) and to ClO₃⁻ (+5, oxidation). The electrons lost "
    "and gained must balance: each Cl oxidised loses 5 electrons, each Cl reduced gains 1.",
    ["Cl → Cl⁻: gain of 1 e⁻ each, 5 atoms", "Cl → ClO₃⁻ (+5): loss of 5 e⁻, 1 atom",
     "Electrons: 5 × 1 = 1 × 5 ✓ → reduced : oxidised = 5 : 1"],
    why="1 : 5 inverts the ratio. 1 : 1 treats it like Cl₂ + 2OH⁻ → Cl⁻ + ClO⁻ + H₂O, the reaction in cold "
        "dilute alkali. 3 : 1 compares Cl₂ molecules with ClO₃⁻.",
    ncert=f"{REF7R}, types of redox reactions: disproportionation", seconds=60, checked=True)

add("Electrode potential and cells", I, "assertion_reason",
    ar("A zinc rod dipped in copper sulphate solution becomes coated with copper.",
       "The standard reduction potential of Zn²⁺/Zn (−0.76 V) is lower than that of Cu²⁺/Cu (+0.34 V)."),
    AR_, "Electrochemical series and displacement reactions",
    "The couple with the lower reduction potential is the stronger reducing agent. Zinc therefore reduces Cu²⁺ "
    "ions to copper (which deposits on the rod) and itself goes into solution as Zn²⁺: "
    "Zn + Cu²⁺ → Zn²⁺ + Cu, E°cell = 0.34 − (−0.76) = 1.10 V > 0. R explains A.",
    ["E°cell = 1.10 V > 0 → reaction spontaneous", "Cu deposits on the zinc rod"],
    answer="A",
    why="Both are true, and the relative electrode potentials are exactly why zinc displaces copper.",
    ncert=f"{REF7R}, redox reactions and electrode processes; {REF7E}, electrochemical series", seconds=35)

add("Nernst equation and Gibbs energy", I, "match_list",
    lists("For the Daniell cell Zn(s) | Zn²⁺(aq) || Cu²⁺(aq) | Cu(s) at 298 K, "
          "E_cell = E°cell − (0.059/2) log([Zn²⁺]/[Cu²⁺]). Match List-I (change) with List-II (effect on E_cell).",
          ["[Cu²⁺] is increased, [Zn²⁺] kept the same", "[Zn²⁺] is increased, [Cu²⁺] kept the same",
           "Both [Zn²⁺] and [Cu²⁺] are doubled", "The cell is allowed to discharge completely to equilibrium"],
          ["Becomes zero", "Increases", "Decreases", "Does not change"]),
    match("B", M("II III IV I"), [M("III II IV I"), M("II III I IV"), M("IV III II I")]),
    "Nernst equation for a galvanic cell",
    "E_cell depends on the ratio [Zn²⁺]/[Cu²⁺]. A smaller ratio raises E_cell; a larger one lowers it; doubling "
    "both leaves the ratio unchanged. At equilibrium Q = K and E_cell = 0.",
    ["A: ratio falls → E increases (II)", "B: ratio rises → E decreases (III)", "C: ratio unchanged (IV)",
     "D: equilibrium → E = 0 (I)"],
    why="The other codes reverse the effects of [Cu²⁺] and [Zn²⁺] or treat doubling both concentrations as a "
        "change in E.",
    ncert=f"{REF7E}, Nernst equation", seconds=55)

add("Batteries and fuel cells", I, "statement_pair",
    sp("While a lead storage battery is being charged, it works as an electrolytic cell.",
       "During the discharge of a lead storage battery, lead(II) sulphate is formed at both electrodes."),
    SP_, "Lead storage battery",
    "On charging, an external source drives the non-spontaneous reverse reaction, so the battery acts as an "
    "electrolytic cell: Statement I is true. On discharge, Pb is oxidised to PbSO₄ at the anode and PbO₂ is "
    "reduced to PbSO₄ at the cathode: Statement II is true.",
    ["Charging: electrical energy → chemical energy (electrolytic cell)",
     "Anode: Pb + SO₄²⁻ → PbSO₄ + 2e⁻; cathode: PbO₂ + SO₄²⁻ + 4H⁺ + 2e⁻ → PbSO₄ + 2H₂O"],
    answer="A",
    why="Both statements follow from the NCERT description of the lead storage battery.",
    ncert=f"{REF7E}, batteries: secondary batteries", seconds=40)

alpha_ha = 48.0 / 384
ph_ha = -math.log10(alpha_ha * 0.0010)
assert close(alpha_ha, 0.125) and close(ph_ha, 3.90, 0.002) and close(4 + math.log10(1.25), 4.10, 0.002)
add("Conductance and Kohlrausch's law", A, "numerical",
    "A 0.0010 mol L⁻¹ solution of a weak monobasic acid HA has a molar conductivity of 48.0 S cm² mol⁻¹ at "
    "298 K. The limiting molar conductivity of HA is 384 S cm² mol⁻¹. The pH of the solution is "
    "(log 1.25 = 0.10):",
    Opts("D", "3.90", ["3.00", "4.10", "0.90"]),
    "Degree of dissociation from conductivity, then pH",
    "For a weak electrolyte α = Λm/Λ°m. Then [H₃O⁺] = cα and pH = −log[H₃O⁺].",
    ["α = 48.0/384 = 0.125", "[H₃O⁺] = 0.0010 × 0.125 = 1.25 × 10⁻⁴ M",
     "pH = 4 − log 1.25 = 4 − 0.10 = 3.90"],
    why="3.00 treats the acid as fully dissociated. 4.10 adds log 1.25 instead of subtracting it. 0.90 is "
        "−log α, which leaves out the concentration.",
    ncert=f"{REF7E}, applications of Kohlrausch's law", seconds=90, checked=True)

add("Oxidation number and balancing", A, "multi_statement",
    ms("Which of the following are disproportionation reactions?",
       ["3MnO₄²⁻ + 4H⁺ → 2MnO₄⁻ + MnO₂ + 2H₂O",
        "P₄ + 3OH⁻ + 3H₂O → PH₃ + 3H₂PO₂⁻",
        "2KClO₃ → 2KCl + 3O₂",
        "2NO₂ + 2OH⁻ → NO₂⁻ + NO₃⁻ + H₂O",
        "Zn + CuSO₄ → ZnSO₄ + Cu"]),
    multi("A", {"a": True, "b": True, "c": False, "d": True, "e": False},
          ["(a), (b), (c) and (d) only", "(b), (d) and (e) only", "(a) and (d) only"]),
    "Identifying disproportionation by oxidation numbers",
    "In a disproportionation reaction the SAME element in one oxidation state is simultaneously oxidised and "
    "reduced.",
    ["(a) Mn +6 → +7 and +4 ✓", "(b) P 0 → −3 (PH₃) and +1 (H₂PO₂⁻) ✓",
     "(c) Cl +5 → −1 is reduced but O −2 → 0 is oxidised: two different elements ✗",
     "(d) N +4 → +3 and +5 ✓", "(e) displacement: Zn oxidised, Cu reduced ✗"],
    why="KClO₃ decomposition is an intramolecular redox reaction of two different elements, not a "
        "disproportionation; (a) and (d) only leaves out phosphorus in (b).",
    ncert=f"{REF7R}, types of redox reactions", seconds=90)

add("Conductance and Kohlrausch's law", A, "assertion_reason",
    ar("When an aqueous solution of KCl is diluted, its conductivity decreases but its molar conductivity "
       "increases.",
       "On dilution the number of ions per unit volume falls, lowering κ, while Λm = κ × V, where V is the volume "
       "containing one mole of electrolyte, increases because V rises more than κ falls."),
    AR_, "Variation of conductivity and molar conductivity with dilution",
    "Conductivity refers to a unit volume, which contains fewer ions after dilution, so κ falls. Molar "
    "conductivity refers to the whole volume holding one mole of electrolyte; this volume grows on dilution and "
    "the product κV increases. R explains both parts of A, as NCERT does.",
    ["κ ∝ number of ions per unit volume → decreases", "Λm = κV; V increases faster → Λm increases"],
    answer="A",
    why="Both are true and R is the NCERT explanation of the opposite trends in κ and Λm.",
    ncert=f"{REF7E}, variation of conductivity and molar conductivity with concentration", seconds=55)

log_ag = (0.446 - 0.80) / 0.059
assert close(log_ag, -6.0) and close((0.446 - 0.80) / 0.0295, -12.0)
add("Nernst equation and Gibbs energy", A, "numerical",
    "For the electrode Ag⁺(aq) | Ag(s), E° = +0.80 V. At 298 K, the concentration of Ag⁺ ions at which the "
    "reduction potential of this electrode is +0.446 V is (2.303RT/F = 0.059 V):",
    Opts("B", "1.0 × 10⁻⁶ mol L⁻¹", ["1.0 × 10⁻³ mol L⁻¹", "1.0 × 10⁶ mol L⁻¹", "1.0 × 10⁻¹² mol L⁻¹"]),
    "Nernst equation for a metal–metal ion electrode",
    "For Ag⁺ + e⁻ → Ag (n = 1), E = E° − 0.059 log(1/[Ag⁺]) = E° + 0.059 log[Ag⁺].",
    ["0.446 = 0.80 + 0.059 log[Ag⁺]", "log[Ag⁺] = −0.354/0.059 = −6.0", "[Ag⁺] = 1.0 × 10⁻⁶ mol L⁻¹"],
    why="1.0 × 10⁻³ divides by 2 × 0.059 = 0.118 instead of by 0.059. 1.0 × 10⁶ comes from a sign "
        "error. 1.0 × 10⁻¹² uses 0.059/2 as if two electrons were transferred.",
    ncert=f"{REF7E}, Nernst equation", seconds=75, checked=True)

# ==================================================================== 8. Chemical Kinetics
topic("Chemical Kinetics")
REF8 = f"{C12}, 'Chemical Kinetics'"

t_half = 0.693 / 0.0693
n_halves = math.log2(0.80 / 0.10)
assert close(t_half, 10) and close(n_halves, 3) and close(n_halves * t_half, 30)
add("Half-life", B, "numerical",
    "A first-order reaction has a rate constant of 0.0693 min⁻¹. The time in which the concentration of the "
    "reactant falls from 0.80 mol L⁻¹ to 0.10 mol L⁻¹ is (ln 2 = 0.693):",
    Opts("D", "30 min", ["10 min", "20 min", "80 min"]),
    "Successive half-lives of a first-order reaction",
    "t½ = 0.693/k is independent of the concentration. 0.80 → 0.40 → 0.20 → 0.10 mol L⁻¹ is three half-lives.",
    ["t½ = 0.693/0.0693 = 10 min", "0.80 → 0.10 = three halvings", "t = 3 × 10 = 30 min"],
    why="10 min is a single half-life. 20 min stops at 0.20 mol L⁻¹. 80 min multiplies the half-life by the "
        "ratio of concentrations (8) instead of by the number of halvings.",
    ncert=f"{REF8}, half-life of a reaction", seconds=40, checked=True)

add("Zero and first order reactions", B, "direct",
    "For a first-order reaction R → P, which plot is a straight line passing through the origin?",
    Opts("B", "ln([R]₀/[R]) against t, with slope k",
         ["[R] against t, with slope −k", "ln[R] against t, with slope k",
          "ln([R]₀/[R]) against t, with slope −k"]),
    "Integrated rate equation of a first-order reaction",
    "kt = ln([R]₀/[R]). Plotting ln([R]₀/[R]) against t gives a straight line through the origin with slope +k "
    "(both quantities are zero at t = 0).",
    ["kt = ln([R]₀/[R]) → y = kx", "Intercept 0, slope +k"],
    why="[R] against t is linear for a zero-order reaction. ln[R] against t has slope −k and intercept ln[R]₀, "
        "so it does not pass through the origin. ln([R]₀/[R]) increases with t, so its slope is +k, not −k.",
    ncert=f"{REF8}, integrated rate equations: first order reactions", seconds=40)

add("Rate law and order", B, "assertion_reason",
    ar("The numerical value of the rate constant of a first-order reaction does not depend on the unit chosen "
       "for concentration.",
       "The rate constant of a first-order reaction has the unit (time)⁻¹, with no concentration term in it."),
    AR_, "Units of rate constants",
    "For a first-order reaction k = (2.303/t) log([R]₀/[R]): only a RATIO of concentrations appears, so k has "
    "the unit s⁻¹ (or min⁻¹) and its value is the same whether concentration is in mol L⁻¹, mol m⁻³ or as "
    "pressure. R explains A.",
    ["k = (2.303/t) log([R]₀/[R])", "Ratio of concentrations → units cancel → unit of k = time⁻¹"],
    answer="A",
    why="Both are true; the absence of a concentration term in the unit of k is precisely why its value is "
        "independent of the concentration unit.",
    ncert=f"{REF8}, units of rate constant; integrated rate equations", seconds=40)

add("Half-life", I, "direct",
    "For a reaction R → P at constant temperature, the half-life is 20 s when the initial concentration of R is "
    "0.40 mol L⁻¹, and 40 s when it is 0.80 mol L⁻¹. The order of the reaction is:",
    Opts("A", "zero", ["first", "second", "cannot be found from these data"]),
    "Dependence of half-life on initial concentration",
    "For a zero-order reaction t½ = [R]₀/2k is directly proportional to [R]₀; for a first-order reaction t½ is "
    "independent of [R]₀.",
    ["[R]₀ doubles (0.40 → 0.80) and t½ doubles (20 → 40 s) → t½ ∝ [R]₀ → zero order",
     "Check: k = [R]₀/2t½ = 0.40/40 = 0.80/80 = 0.010 mol L⁻¹ s⁻¹ in both cases"],
    why="A first-order reaction would show the same half-life at both concentrations. A second-order reaction "
        "would show a shorter half-life at the higher concentration. Two half-lives are enough to decide.",
    ncert=f"{REF8}, half-life of a reaction", seconds=45)

k_pseudo = 2.0 * 1.0
assert close(0.693 / k_pseudo, 0.3465) and close(0.693 / (2.0 * 0.001), 346.5) and close(0.693 / 2.0 / 2, 0.173)
add("Rate law and order", I, "numerical",
    "The reaction A + B → products has the rate law rate = k[A][B] with k = 2.0 L mol⁻¹ s⁻¹. It is carried out "
    "with [A]₀ = 1.0 × 10⁻³ mol L⁻¹ and B in large excess, [B] ≈ 1.0 mol L⁻¹ throughout. The half-life of A is "
    "about (ln 2 = 0.693):",
    Opts("C", "0.35 s", ["0.69 s", "347 s", "0.17 s"]),
    "Pseudo first-order reactions",
    "With B in large excess, rate = k'[A] where k' = k[B] is a pseudo first-order rate constant; then "
    "t½ = 0.693/k'.",
    ["k' = 2.0 × 1.0 = 2.0 s⁻¹", "t½ = 0.693/2.0 ≈ 0.35 s"],
    why="0.69 s uses k' = 1.0 s⁻¹, leaving out the value of k. 347 s multiplies k by [A]₀ instead of [B]. "
        "0.17 s halves the half-life again.",
    ncert=f"{REF8}, pseudo first order reaction", seconds=60, checked=True)

add("Rate law and order", I, "statement_pair",
    sp("The molecularity of a reaction can be found only by experiment.",
       "For an elementary reaction, the order is equal to the molecularity."),
    SP_, "Order versus molecularity",
    "Molecularity is the number of reacting species that collide simultaneously in an elementary step; it is a "
    "theoretical idea taken from the proposed step, whereas ORDER is found experimentally: Statement I is false. "
    "For a single elementary step the rate law follows its stoichiometry, so order = molecularity: Statement II "
    "is true.",
    ["I: it is the order, not molecularity, that is determined experimentally → false",
     "II: elementary step → rate law from its stoichiometry → order = molecularity → true"],
    answer="D",
    why="Statement I swaps the roles of order and molecularity.",
    ncert=f"{REF8}, molecularity of a reaction", seconds=40)

orders = {"A": 1, "B": round(math.log(9, 3)), "C": 0, "D": round(math.log(8, 2))}
assert orders == {"A": 1, "B": 2, "C": 0, "D": 3}
add("Rate law and order", I, "match_list",
    lists("For reactions of a single reactant, match List-I (observation) with List-II (order of the reaction).",
          ["The rate constant has the unit s⁻¹.",
           "The rate becomes 9 times when the concentration of the reactant is tripled.",
           "The rate does not change when the concentration of the reactant is doubled.",
           "The rate becomes 8 times when the concentration of the reactant is doubled."],
          ["0", "1", "2", "3"]),
    match("D", M("II III I IV"), [M("II IV I III"), M("III II I IV"), M("I III II IV")]),
    "Determining order from units and from concentration–rate data",
    "rate = k[A]ⁿ: the unit of k is (mol L⁻¹)¹⁻ⁿ s⁻¹, and multiplying [A] by a factor f multiplies the rate by fⁿ.",
    ["s⁻¹ → n = 1 (II)", "3ⁿ = 9 → n = 2 (III)", "2ⁿ = 1 → n = 0 (I)", "2ⁿ = 8 → n = 3 (IV)"],
    why="The other codes misread the powers, e.g. taking 9-fold for tripling as third order.",
    ncert=f"{REF8}, order of a reaction; units of rate constant", seconds=55)

k_obs = math.log(0.40 / 0.10) / 20
r0 = 0.40 * math.exp(k_obs * 10)
assert close(r0, 0.80) and close(0.40 + 0.015 * 10, 0.55)
add("Zero and first order reactions", A, "numerical",
    "In a first-order reaction, the concentration of the reactant is 0.40 mol L⁻¹ at t = 10 min and "
    "0.10 mol L⁻¹ at t = 30 min. Its initial concentration (t = 0) was:",
    Opts("A", "0.80 mol L⁻¹", ["0.55 mol L⁻¹", "1.60 mol L⁻¹", "0.20 mol L⁻¹"]),
    "Working back with the half-life of a first-order reaction",
    "From 10 to 30 min the concentration falls to one-quarter, i.e. two half-lives in 20 min, so t½ = 10 min. "
    "Going back 10 min from t = 10 min doubles the concentration.",
    ["0.40 → 0.10 in 20 min = 2 half-lives → t½ = 10 min",
     "t = 0 is one half-life before t = 10 min → [R]₀ = 2 × 0.40 = 0.80 mol L⁻¹"],
    why="0.55 mol L⁻¹ extrapolates linearly, as for a zero-order reaction. 1.60 mol L⁻¹ goes back two "
        "half-lives. 0.20 mol L⁻¹ is the concentration at t = 20 min.",
    ncert=f"{REF8}, integrated rate equations: first order reactions", seconds=75, checked=True)

add("Rate law and order", A, "multi_statement",
    ms("A reaction A + 2B → D is proposed to occur in two elementary steps: (i) A + B → C (slow); "
       "(ii) C + B → D (fast). Which of the following statements are correct?",
       ["The rate law of the overall reaction is rate = k[A][B].",
        "The overall order of the reaction is 2.",
        "The molecularity of the slow step is 2.",
        "C is a reaction intermediate.",
        "The rate is proportional to [B]², because two molecules of B appear in the overall equation."]),
    multi("C", {"a": True, "b": True, "c": True, "d": True, "e": False},
          ["(a), (b) and (e) only", "(b), (c) and (d) only", "(a), (d) and (e) only"]),
    "Rate-determining step of a complex reaction",
    "The slowest step decides the overall rate, so rate = k[A][B] (order 2, bimolecular step). C is formed in "
    "step (i) and used up in step (ii), so it is an intermediate. The order cannot be read from the overall "
    "equation.",
    ["(a) rate from slow step ✓", "(b) 1 + 1 = 2 ✓", "(c) A + B: bimolecular ✓", "(d) intermediate ✓",
     "(e) stoichiometric coefficients ≠ orders ✗"],
    why="(e) uses the overall equation to write the rate law; every option containing it is wrong, and "
        "'(b), (c) and (d) only' leaves out the true rate law (a).",
    ncert=f"{REF8}, mechanism of a reaction (rate determining step); molecularity", seconds=70)

add("Arrhenius equation and activation energy", A, "assertion_reason",
    ar("A reaction with a large negative ΔG° can still be extremely slow at room temperature.",
       "The rate of a reaction is governed by its activation energy, which ΔG° does not determine."),
    AR_, "Thermodynamic feasibility versus rate",
    "ΔG° tells only whether a reaction is feasible and how far it can go. How fast it goes depends on the energy "
    "barrier, Eₐ (k = A e^(−Eₐ/RT)). A feasible reaction with a high Eₐ, such as the combination of H₂ and O₂ at "
    "room temperature, proceeds immeasurably slowly. R explains A.",
    ["ΔG° < 0 → feasible", "Rate ∝ e^(−Eₐ/RT) → high Eₐ → very slow", "R explains A"],
    answer="A",
    why="Both statements are true; the independence of the barrier height from ΔG° is the reason a spontaneous "
        "reaction can be slow.",
    ncert=f"{REF8}, temperature dependence of the rate (activation energy)", seconds=45)

# ==================================================================== 9. Classification of Elements and Periodicity
topic("Classification of Elements and Periodicity in Properties")
REF9 = f"{C11}, 'Classification of Elements and Periodicity in Properties'"

add("Modern periodic table", B, "direct",
    "Which of the following atomic numbers belongs to an s-block element?",
    Opts("C", "38", ["31", "50", "26"]),
    "Blocks of the periodic table from electronic configuration",
    "The block is fixed by the subshell that receives the last electron. Z = 38 is strontium, [Kr] 5s², a "
    "group 2 (s-block) element.",
    ["Z = 38: [Kr] 5s² → s-block", "Z = 31: [Ar] 3d¹⁰ 4s² 4p¹ (Ga, p-block)",
     "Z = 50: [Kr] 4d¹⁰ 5s² 5p² (Sn, p-block)", "Z = 26: [Ar] 3d⁶ 4s² (Fe, d-block)"],
    why="31 and 50 have their last electron in a p subshell; 26 in a d subshell.",
    ncert=f"{REF9}, electronic configurations and types of elements: s-, p-, d-, f-blocks", seconds=35)

add("Atomic and ionic radii", B, "assertion_reason",
    ar("The atomic radius of potassium is larger than that of sodium.",
       "Potassium has a smaller nuclear charge than sodium."),
    AR_, "Variation of atomic radius down a group",
    "Down a group, a new shell is added (K: valence electron in n = 4; Na: n = 3), so the radius increases even "
    "though the nuclear charge increases (K, Z = 19; Na, Z = 11). A is true; R is false.",
    ["K 4s¹ vs Na 3s¹ → extra shell → larger radius", "Nuclear charge: K (+19) > Na (+11) → R false"],
    answer="C",
    why="R is factually wrong; the real reason for A is the extra electron shell, which outweighs the larger "
        "nuclear charge.",
    ncert=f"{REF9}, atomic radius", seconds=30)

add("Ionisation and electron gain enthalpy", I, "match_list",
    lists("Match List-I (periodic observation) with List-II (its explanation).",
          ["Atomic radius decreases from left to right across a period",
           "Atomic radius increases down a group",
           "First ionisation enthalpy of boron is lower than that of beryllium",
           "First ionisation enthalpy of oxygen is lower than that of nitrogen"],
          ["Repulsion between two electrons in the same 2p orbital",
           "Increase in effective nuclear charge while electrons are added to the same shell",
           "Addition of a new electron shell",
           "A 2p electron is shielded by the 2s electrons and penetrates less towards the nucleus than a 2s "
           "electron"]),
    match("B", M("II III IV I"), [M("III II IV I"), M("II III I IV"), M("IV III II I")]),
    "Explanations of trends in atomic radius and ionisation enthalpy",
    "Across a period electrons enter the same shell while the effective nuclear charge rises, pulling them in. "
    "Down a group each element has an extra shell. In B the electron removed is a 2p electron, less tightly "
    "held than the 2s electron of Be. In O one 2p orbital holds a pair, and their repulsion makes one of them "
    "easier to remove than any of nitrogen's three unpaired 2p electrons.",
    ["A → II", "B → III", "C → IV", "D → I"],
    why="The other codes swap the two radius explanations or the two ionisation-enthalpy anomalies.",
    ncert=f"{REF9}, atomic radius; ionisation enthalpy", seconds=60)

add("Valence and reactivity", I, "multi_statement",
    ms("Which of the following statements about the valence of the third-period elements are correct?",
       ["The highest valence of phosphorus, shown towards oxygen, is 5, as in P₄O₁₀.",
        "Sulphur shows a valence of 2 towards hydrogen, as in H₂S.",
        "The oxide of aluminium has the formula Al₂O₃.",
        "The simple hydride of silicon has the formula SiH₃.",
        "Chlorine shows a valence of 7 towards hydrogen."]),
    multi("D", {"a": True, "b": True, "c": True, "d": False, "e": False},
          ["(a) and (b) only", "(b), (c) and (e) only", "(a), (c) and (d) only"]),
    "Periodicity of valence",
    "Valence towards hydrogen is usually equal to the number of valence electrons or 8 minus it; towards oxygen "
    "elements of the right side can use all their valence electrons. Silicon (4 valence electrons) gives SiH₄; "
    "chlorine gives HCl (valence 1 towards hydrogen) but shows 7 in Cl₂O₇.",
    ["(a) P₄O₁₀: valence 5 ✓", "(b) H₂S: 2 ✓", "(c) Al₂O₃: Al valence 3 ✓", "(d) SiH₄, not SiH₃ ✗",
     "(e) HCl: valence 1 towards H ✗"],
    why="Options containing (d) or (e) are wrong; '(a) and (b) only' leaves out the true statement (c).",
    ncert=f"{REF9}, periodicity of valence or oxidation states", seconds=50)

add("Valence and reactivity", I, "statement_pair",
    sp("Across a period from left to right, the non-metallic character of the elements increases as their "
       "electronegativity increases.",
       "The electronegativity of the elements increases on going down a group."),
    SP_, "Electronegativity and metallic/non-metallic character",
    "Electronegativity rises across a period as the atoms become smaller and the effective nuclear charge "
    "increases; the elements become less metallic and more non-metallic: Statement I is true. Down a group the "
    "atoms become larger and electronegativity DECREASES: Statement II is false.",
    ["I: EN ↑ across period → non-metallic character ↑ → true", "II: EN ↓ down a group → false"],
    answer="C",
    why="Statement II reverses the group trend (F 4.0 > Cl 3.0 > Br 2.8 > I 2.5 on the Pauling scale).",
    ncert=f"{REF9}, electronegativity; periodic trends and chemical reactivity", seconds=35)

egh = {"Cl": -349, "F": -328, "S": -200, "O": -141}
assert sorted(egh, key=egh.get) == ["Cl", "F", "S", "O"]
add("Ionisation and electron gain enthalpy", A, "direct",
    "Which of the following arranges O, S, F and Cl in order from the MOST negative to the LEAST negative "
    "electron gain enthalpy?",
    Opts("B", "Cl > F > S > O", ["F > Cl > O > S", "Cl > S > F > O", "F > O > Cl > S"]),
    "Electron gain enthalpy: halogens versus chalcogens and the anomaly of the second-period elements",
    "Halogens (one electron short of a noble gas) have more negative values than the group 16 elements of the "
    "same period. Within each group, the small second-period atom (F, O) has a LESS negative value than the "
    "third-period atom (Cl, S), because the added electron enters a compact 2p subshell and is repelled by the "
    "electrons already there.",
    ["Cl (−349) > F (−328) > S (−200) > O (−141) kJ mol⁻¹"],
    why="Putting F before Cl or O before S ignores the anomaly of the second-period elements; putting S before F "
        "ignores the much greater tendency of halogens to gain an electron.",
    ncert=f"{REF9}, electron gain enthalpy", seconds=50)

n_na = 0.46 / 23
n_cl = 0.71 / 35.5
net = n_na * 496 + n_cl * (-349)
assert close(net, 2.94) and close(n_na * 496 + n_cl * 349, 16.9) and close(496 - 349, 147)
add("Ionisation and electron gain enthalpy", A, "numerical",
    "0.46 g of gaseous sodium atoms are converted into Na⁺(g) ions, and 0.71 g of gaseous chlorine atoms are "
    "converted into Cl⁻(g) ions. The first ionisation enthalpy of Na is 496 kJ mol⁻¹ and the electron gain "
    "enthalpy of Cl is −349 kJ mol⁻¹. The net energy change for the two processes together is (Na = 23, "
    "Cl = 35.5):",
    Opts("D", "2.94 kJ absorbed", ["16.9 kJ absorbed", "2.94 kJ released", "147 kJ absorbed"]),
    "Ionisation enthalpy and electron gain enthalpy with the mole concept",
    "Find the moles of each kind of atom; ionisation absorbs 496 kJ per mole of Na, electron gain releases "
    "349 kJ per mole of Cl.",
    ["n(Na) = 0.46/23 = 0.020 mol → +0.020 × 496 = +9.92 kJ",
     "n(Cl) = 0.71/35.5 = 0.020 mol → 0.020 × (−349) = −6.98 kJ",
     "Net = +9.92 − 6.98 = +2.94 kJ (absorbed)"],
    why="16.9 kJ adds the two magnitudes, treating electron gain as absorbing energy. '2.94 kJ released' gets "
        "the sign wrong. 147 kJ is the net value for one mole each, not 0.020 mol.",
    ncert=f"{REF9}, ionisation enthalpy; electron gain enthalpy", seconds=80, checked=True)

# ==================================================================== 10. p-Block Elements (trends only)
topic("p-Block Elements")
REF10A = f"{C11}, 'The p-Block Elements'"
REF10B = f"{C12}, 'The p-Block Elements'"

add("Group 13 and 14 trends", B, "direct",
    "Among the oxides B₂O₃, Al₂O₃, Ga₂O₃ and Tl₂O₃ of the group 13 elements in the +3 oxidation state, the one "
    "that is basic is:",
    Opts("C", "Tl₂O₃", ["B₂O₃", "Al₂O₃", "Ga₂O₃"]),
    "Trend in the acid–base character of the oxides down group 13",
    "Metallic character increases down group 13, and the oxides change from acidic to basic: B₂O₃ is acidic, "
    "Al₂O₃ and Ga₂O₃ are amphoteric, In₂O₃ and Tl₂O₃ are basic.",
    ["B₂O₃ acidic → Al₂O₃, Ga₂O₃ amphoteric → In₂O₃, Tl₂O₃ basic"],
    why="B₂O₃ is acidic, and the oxides of aluminium and gallium are amphoteric.",
    ncert=f"{REF10A}, group 13: chemical properties (trends)", seconds=30)

add("Group 17 and 18 trends", B, "direct",
    "Which of the following halide ions has the largest ionic radius?",
    Opts("B", "I⁻", ["F⁻", "Cl⁻", "Br⁻"]),
    "Trend in ionic radius down group 17",
    "Down group 17 each element adds a new electron shell, so the radii of both the atoms and the X⁻ ions "
    "increase from fluorine to iodine. The iodide ion, with its valence electrons in the fifth shell, is the "
    "largest.",
    ["Valence shell of X⁻: F⁻ n = 2, Cl⁻ n = 3, Br⁻ n = 4, I⁻ n = 5",
     "Radius increases down the group: F⁻ < Cl⁻ < Br⁻ < I⁻"],
    why="F⁻, Cl⁻ and Br⁻ lie above iodide in the group and have fewer electron shells, so they are smaller.",
    ncert=f"{REF10B}, group 17: atomic and ionic radii", seconds=20)

add("Group 13 and 14 trends", B, "match_list",
    lists("Match List-I (element) with List-II (its valence-shell electronic configuration in the ground state).",
          ["Boron (Z = 5)", "Silicon (Z = 14)", "Gallium (Z = 31)", "Tin (Z = 50)"],
          ["4s² 4p¹", "5s² 5p²", "2s² 2p¹", "3s² 3p²"]),
    match("B", M("III IV I II"), [M("III IV II I"), M("IV III I II"), M("I IV III II")]),
    "Valence-shell configurations of group 13 and group 14 elements",
    "Group 13 elements have the valence configuration ns² np¹ and group 14 elements ns² np², where n is the "
    "period number. Boron and gallium are in group 13 (periods 2 and 4); silicon and tin are in group 14 "
    "(periods 3 and 5).",
    ["B: period 2, group 13 → 2s² 2p¹ (III)", "Si: period 3, group 14 → 3s² 3p² (IV)",
     "Ga: period 4, group 13 → 4s² 4p¹ (I)", "Sn: period 5, group 14 → 5s² 5p² (II)"],
    why="The other codes give the group 13 elements an np² configuration, or swap the period numbers of "
        "gallium and tin or of silicon and tin.",
    ncert=f"{REF10A}, groups 13 and 14: electronic configuration", seconds=40)

bde = {"Cl₂": 242.6, "Br₂": 192.8, "F₂": 158.8, "I₂": 151.1}
assert sorted(bde, key=bde.get, reverse=True) == ["Cl₂", "Br₂", "F₂", "I₂"]
add("Group 17 and 18 trends", I, "direct",
    "Which of the following shows the halogens in order of DECREASING bond dissociation enthalpy of the X–X "
    "bond?",
    Opts("C", "Cl₂ > Br₂ > F₂ > I₂", ["F₂ > Cl₂ > Br₂ > I₂", "I₂ > Br₂ > Cl₂ > F₂", "Cl₂ > F₂ > Br₂ > I₂"]),
    "Trend in X–X bond dissociation enthalpy with the anomaly of fluorine",
    "From chlorine onwards the bond enthalpy falls as the atoms get larger (Cl₂ > Br₂ > I₂). F₂ breaks the trend: "
    "repulsion between the lone pairs of the small fluorine atoms weakens the F–F bond, which is weaker than "
    "Cl–Cl and Br–Br but still a little stronger than I–I.",
    ["Cl₂ 242.6 > Br₂ 192.8 > F₂ 158.8 > I₂ 151.1 kJ mol⁻¹"],
    why="Placing F₂ first follows the size trend blindly; the reversed order ignores the decrease with size; "
        "placing F₂ above Br₂ overstates the F–F bond strength.",
    ncert=f"{REF10B}, group 17: physical properties (bond dissociation enthalpy)", seconds=45)

add("Group 15 and 16 trends", I, "direct",
    "In group 15, which two elements are metalloids?",
    Opts("B", "Arsenic and antimony", ["Nitrogen and phosphorus", "Phosphorus and arsenic", "Antimony and bismuth"]),
    "Change of metallic character down group 15",
    "Metallic character increases down the group: nitrogen and phosphorus are non-metals, arsenic and antimony "
    "are metalloids, and bismuth is a metal.",
    ["N, P: non-metals", "As, Sb: metalloids", "Bi: metal"],
    why="Phosphorus is a non-metal and bismuth is a metal, so every pair containing either of them is wrong.",
    ncert=f"{REF10B}, group 15: physical properties", seconds=30)

l2_sn = 10 + 10  # Sn [Kr] 4d10 5s2 5p2 : 3d10 + 4d10
assert l2_sn == 20
add("Group 13 and 14 trends", I, "numerical",
    "Tin (Z = 50) is a group 14 element with the ground-state configuration [Kr] 4d¹⁰ 5s² 5p². The total number "
    "of electrons with azimuthal quantum number l = 2 in a tin atom is:",
    Opts("C", "20", ["10", "30", "12"]),
    "Electronic configuration of the heavier p-block elements",
    "[Kr] is 1s² 2s² 2p⁶ 3s² 3p⁶ 3d¹⁰ 4s² 4p⁶. Electrons with l = 2 are d electrons: the 3d¹⁰ inside the krypton "
    "core and the filled 4d¹⁰ subshell.",
    ["d subshells present: 3d¹⁰ (in [Kr]) and 4d¹⁰", "Total = 10 + 10 = 20"],
    why="10 counts only the 4d electrons written outside the core. 30 adds a 5d¹⁰ subshell that tin does not "
        "have. 12 adds the two 5p electrons (l = 1) to the 4d electrons.",
    ncert=f"{REF10A}, group 14: electronic configuration", seconds=45, checked=True)

ie = {"C": 1086, "B": 801, "Si": 786, "Al": 577, "Ge": 762, "Ga": 579, "Sn": 708, "In": 558, "Pb": 715, "Tl": 589}
assert all(ie[a] > ie[b] for a, b in [("C", "B"), ("Si", "Al"), ("Ge", "Ga"), ("Sn", "In"), ("Pb", "Tl")])
assert ie["Pb"] > ie["Sn"]
add("Group 13 and 14 trends", I, "statement_pair",
    sp("The first ionisation enthalpy of each group 14 element is higher than that of the group 13 element of "
       "the same period.",
       "In group 14, the first ionisation enthalpy decreases steadily all the way from carbon to lead."),
    SP_, "Ionisation enthalpy trends in groups 13 and 14",
    "Group 14 atoms are smaller and have a higher effective nuclear charge than their group 13 neighbours, so "
    "their first ionisation enthalpies are higher (e.g. C 1086 > B 801; Si 786 > Al 577 kJ mol⁻¹): Statement I "
    "is true. In group 14 the decrease is not steady: lead (715) has a slightly higher value than tin (708), "
    "because of the poor shielding by its 4f and 5d electrons: Statement II is false.",
    ["I: group 14 > group 13 in each period → true", "II: Pb > Sn → not a steady decrease → false"],
    answer="C",
    why="Statement II overlooks the small rise from Sn to Pb caused by the intervening d and f electrons.",
    ncert=f"{REF10A}, groups 13 and 14: ionisation enthalpy", seconds=45)

add("Anomalous first element", A, "multi_statement",
    ms("Which of the following statements about the first element of each of the groups 13 to 17 are correct?",
       ["It has the highest electronegativity in its group.",
        "It has the most negative electron gain enthalpy in its group.",
        "Having only four valence orbitals (2s and 2p), it cannot show a covalency greater than four.",
        "It readily forms pπ–pπ multiple bonds with itself and with other second-period elements.",
        "It has the largest atomic radius in its group."]),
    multi("D", {"a": True, "b": False, "c": True, "d": True, "e": False},
          ["(a), (b), (c) and (d) only", "(c), (d) and (e) only", "(a) and (d) only"]),
    "Anomalous behaviour of the first member of each p-block group",
    "The first member is the smallest atom with the highest electronegativity in its group (B 2.0, C 2.5, "
    "N 3.0, O 3.5, F 4.0). It has no d orbitals in its valence shell, so its maximum covalency is four, and it "
    "forms pπ–pπ multiple bonds readily (C=C, C≡C, N≡N, C=O, N=O). Its electron gain enthalpy, however, is "
    "LESS negative than that of the second member in groups 16 and 17 (O < S, F < Cl), because of electron "
    "repulsion in its compact 2p subshell.",
    ["(a) ✓ (B 2.0 is higher than Tl 1.8 in group 13)", "(b) ✗ O and F are exceptions",
     "(c) ✓ no valence d orbitals", "(d) ✓", "(e) ✗ it is the smallest"],
    why="Options with (b) or (e) are wrong; '(a) and (d) only' leaves out the true statement (c).",
    ncert=f"{REF10A}; {REF10B}, anomalous behaviour of the first member of a group", seconds=90)

add("Group 13 and 14 trends", A, "statement_pair",
    sp("Boron has a higher first ionisation enthalpy than beryllium.",
       "For every element of group 13, the sum of the first three ionisation enthalpies is very high."),
    SP_, "Ionisation enthalpies of group 13 elements",
    "Beryllium (2s²) loses a penetrating 2s electron, boron (2s² 2p¹) a less penetrating, better-shielded 2p "
    "electron, so ΔᵢH₁ of B (801 kJ mol⁻¹) is LOWER than that of Be (899): Statement I is false. NCERT notes that "
    "the sum of the first three ionisation enthalpies of the group 13 elements is very high, which is why boron "
    "does not form B³⁺ and the trivalent compounds tend to be covalent: Statement II is true.",
    ["I: B 801 < Be 899 kJ mol⁻¹ → false", "II: ΔᵢH₁ + ΔᵢH₂ + ΔᵢH₃ very high → true"],
    answer="D",
    why="Statement I reverses the well-known drop in ionisation enthalpy from group 2 to group 13.",
    ncert=f"{REF10A}, group 13: ionisation enthalpy", seconds=45)

add("Group 17 and 18 trends", A, "assertion_reason",
    ar("Helium is placed in group 2 of the s-block, along with beryllium and magnesium, because its "
       "configuration is 1s².",
       "Like the other noble gases, helium has a completely filled valence shell."),
    AR_, "Position of helium in the periodic table",
    "Although helium's configuration (1s²) is of the s type, it is placed in group 18 with the noble gases, "
    "because its completely filled valence shell makes it chemically inert like them. A is false; R is true "
    "(and R is in fact the reason helium is NOT placed in group 2).",
    ["He: 1s² — filled n = 1 shell → noble-gas behaviour → group 18",
     "Group 2 elements (ns²) are reactive metals"],
    answer="D",
    why="A misplaces helium; R correctly states its filled valence shell.",
    ncert=f"{REF10B}, group 18 elements: electronic configuration", seconds=40)

# ==================================================================== 11. d- and f-Block Elements
topic("d- and f-Block Elements")
REF11 = f"{C12}, 'The d- and f-Block Elements'"


def spin_only(n):
    return math.sqrt(n * (n + 2))


assert close(spin_only(4), 4.90) and close(spin_only(5), 5.92) and close(spin_only(3), 3.87) \
    and close(spin_only(2), 2.83)
add("Magnetic and colour properties", B, "numerical",
    "The spin-only magnetic moment of the Fe²⁺ ion (Z of Fe = 26) is about:",
    Opts("B", "4.90 BM", ["5.92 BM", "3.87 BM", "2.83 BM"]),
    "Spin-only formula μ = √[n(n + 2)] BM",
    "Fe²⁺ is [Ar] 3d⁶: five electrons occupy the five d orbitals singly and the sixth pairs up, leaving four "
    "unpaired electrons.",
    ["Fe²⁺: 3d⁶ → n = 4", "μ = √(4 × 6) = √24 ≈ 4.90 BM"],
    why="5.92 BM is for five unpaired electrons (Fe³⁺, Mn²⁺). 3.87 and 2.83 BM are for three and two unpaired "
        "electrons.",
    ncert=f"{REF11}, magnetic properties", seconds=35, checked=True)

add("Transition element trends", B, "direct",
    "Which element of the first transition series shows only the +2 oxidation state in its compounds?",
    Opts("C", "Zinc", ["Manganese", "Iron", "Copper"]),
    "Oxidation states of the 3d elements",
    "Zinc ([Ar] 3d¹⁰ 4s²) loses its two 4s electrons to give Zn²⁺ with a stable, completely filled 3d¹⁰ "
    "subshell; it shows no other oxidation state in its compounds.",
    ["Zn: 3d¹⁰ 4s² → Zn²⁺ 3d¹⁰ only", "Mn: +2 to +7; Fe: +2, +3 (and others); Cu: +1, +2"],
    why="Manganese, iron and copper all show more than one oxidation state.",
    ncert=f"{REF11}, oxidation states", seconds=25)

add("Lanthanoids and actinoids", B, "statement_pair",
    sp("The radii of the tripositive lanthanoid ions decrease steadily from La³⁺ to Lu³⁺.",
       "The ground-state electronic configuration of europium (Z = 63) is [Xe] 4f⁶ 5d¹ 6s²."),
    SP_, "Lanthanoid contraction; electronic configurations of the lanthanoids",
    "The steady decrease of the M³⁺ radii from La³⁺ to Lu³⁺ is the lanthanoid contraction: Statement I is true. "
    "Europium has the configuration [Xe] 4f⁷ 6s²: its seven 4f electrons make an exactly half-filled 4f "
    "subshell, and no electron goes into 5d. Statement II is false.",
    ["I: La³⁺ → Lu³⁺ radii decrease → true", "II: Eu is [Xe] 4f⁷ 6s² (half-filled 4f), not 4f⁶ 5d¹ 6s² → false"],
    answer="C",
    why="Statement II puts a 5d electron where europium prefers the extra-stable half-filled 4f⁷ arrangement "
        "(the 5d¹ pattern belongs to La, Ce, Gd and Lu).",
    ncert=f"{REF11}, the lanthanoids: electronic configurations; lanthanoid contraction", seconds=40)

add("Transition element trends", I, "assertion_reason",
    ar("Zinc has the lowest enthalpy of atomisation among the elements of the first transition series.",
       "Zinc has the largest atomic radius in the first transition series."),
    AR_, "Enthalpy of atomisation and metallic bonding in the 3d series",
    "The strength of metallic bonding in the transition metals comes largely from unpaired d electrons. In zinc "
    "the 3d subshell is full and no d electrons take part, so its enthalpy of atomisation is the lowest in the "
    "series: A is true. Zinc does not have the largest atomic radius of the series (scandium does; Zn ≈ 137 pm, "
    "Sc ≈ 164 pm): R is false.",
    ["A: Zn — no unpaired d electrons for metallic bonding → lowest ΔₐH → true",
     "R: largest radius in the 3d series is Sc, not Zn → false"],
    answer="C",
    why="R is factually wrong; the reason for A is the filled 3d¹⁰ subshell, not the atomic size.",
    ncert=f"{REF11}, physical properties of transition elements; enthalpies of atomisation", seconds=45)

unpaired = {"Ti³⁺": 1, "Ni²⁺": 2, "Cr³⁺": 3, "Mn³⁺": 4}
d_count = {"Ti³⁺": 1, "Ni²⁺": 8, "Cr³⁺": 3, "Mn³⁺": 4}
assert all(unpaired[k] == (d if d <= 5 else 10 - d) for k, d in d_count.items())
add("Magnetic and colour properties", I, "match_list",
    lists("Match List-I (gaseous ion in its ground state) with List-II (number of unpaired electrons). "
          "(Z: Ti = 22, Cr = 24, Mn = 25, Ni = 28)",
          ["Ti³⁺", "Ni²⁺", "Cr³⁺", "Mn³⁺"], ["3", "1", "4", "2"]),
    match("D", M("II IV I III"), [M("II I IV III"), M("IV II I III"), M("II IV III I")]),
    "d-electron count and Hund's rule",
    "Remove the 4s electrons first, then d electrons. Ti³⁺ 3d¹, Ni²⁺ 3d⁸, Cr³⁺ 3d³, Mn³⁺ 3d⁴. Fill the five d "
    "orbitals singly before pairing.",
    ["Ti³⁺ 3d¹ → 1 (II)", "Ni²⁺ 3d⁸ → 2 (IV)", "Cr³⁺ 3d³ → 3 (I)", "Mn³⁺ 3d⁴ → 4 (III)"],
    why="The other codes confuse the d-electron count with the number of unpaired electrons (e.g. 3d⁸ with 8 "
        "or 3 unpaired) or swap Cr³⁺ and Mn³⁺.",
    ncert=f"{REF11}, electronic configurations; magnetic properties", seconds=55)

add("Lanthanoids and actinoids", I, "multi_statement",
    ms("Which of the following statements about the electronic configurations of lanthanoids and their ions are "
       "correct? (Z: La = 57, Ce = 58, Nd = 60, Yb = 70, Lu = 71; Xe = 54)",
       ["La³⁺ has the configuration [Xe].",
        "Lu³⁺ has a completely filled 4f subshell, 4f¹⁴.",
        "Yb³⁺ has the configuration [Xe] 4f¹³.",
        "The ground-state configuration of neodymium is [Xe] 4f³ 5d¹ 6s².",
        "The ground-state configuration of cerium is [Xe] 4f² 6s²."]),
    multi("B", {"a": True, "b": True, "c": True, "d": False, "e": False},
          ["(a), (c) and (e) only", "(b), (c) and (d) only", "(a) and (b) only"]),
    "Electronic configurations of lanthanoid atoms and M³⁺ ions",
    "NCERT gives La [Xe] 5d¹ 6s², Ce [Xe] 4f¹ 5d¹ 6s², Nd [Xe] 4f⁴ 6s², Yb [Xe] 4f¹⁴ 6s² and Lu [Xe] 4f¹⁴ 5d¹ "
    "6s². Removing the three outermost electrons (6s² and 5d¹, or 6s² and one 4f) gives the M³⁺ ion.",
    ["(a) La³⁺: [Xe] 4f⁰ ✓", "(b) Lu³⁺: [Xe] 4f¹⁴ ✓", "(c) Yb³⁺: 4f¹⁴ → 4f¹³ ✓",
     "(d) Nd is [Xe] 4f⁴ 6s² ✗", "(e) Ce is [Xe] 4f¹ 5d¹ 6s² ✗"],
    why="Options containing (d) or (e) are wrong; '(a) and (b) only' leaves out the true statement (c).",
    ncert=f"{REF11}, the lanthanoids: electronic configurations", seconds=60)

e_m2 = {"Ti": -1.63, "V": -1.18, "Cr": -0.90, "Mn": -1.18, "Fe": -0.44, "Co": -0.28, "Ni": -0.25, "Cu": 0.34,
        "Zn": -0.76}
assert [k for k, v in e_m2.items() if v > 0] == ["Cu"]
add("Transition element trends", I, "direct",
    "Which metal of the first transition series (Ti to Zn) has a POSITIVE standard electrode potential "
    "E°(M²⁺/M) and therefore does not liberate hydrogen from dilute non-oxidising acids?",
    Opts("B", "Copper", ["Zinc", "Nickel", "Iron"]),
    "Trend in E°(M²⁺/M) across the 3d series",
    "Of the 3d metals, only copper has a positive E°(M²⁺/M) (+0.34 V): the high energy needed to convert Cu(s) to "
    "Cu²⁺(aq) is not balanced by its hydration enthalpy. Hence copper cannot displace H₂ from acids such as dilute "
    "HCl.",
    ["E°(Cu²⁺/Cu) = +0.34 V → positive", "Zn −0.76, Fe −0.44, Ni −0.25 V → negative"],
    why="Zinc, iron and nickel have negative E°(M²⁺/M) values and do liberate hydrogen from dilute acids.",
    ncert=f"{REF11}, trends in the M²⁺/M standard electrode potentials", seconds=35)

pairs = {"Cr³⁺/Co²⁺": (3, 3), "Ti³⁺/V³⁺": (1, 2), "Ni²⁺/Cu²⁺": (2, 1), "Mn²⁺/Fe²⁺": (5, 4)}
assert [k for k, (a, b) in pairs.items() if a == b] == ["Cr³⁺/Co²⁺"]
add("Magnetic and colour properties", A, "direct",
    "Which of the following pairs of gaseous ions have the SAME spin-only magnetic moment? "
    "(Z: Ti = 22, V = 23, Cr = 24, Mn = 25, Fe = 26, Co = 27, Ni = 28, Cu = 29)",
    Opts("C", "Cr³⁺ and Co²⁺", ["Ti³⁺ and V³⁺", "Ni²⁺ and Cu²⁺", "Mn²⁺ and Fe²⁺"]),
    "Spin-only magnetic moment depends only on the number of unpaired electrons",
    "Cr³⁺ is 3d³ with three unpaired electrons; Co²⁺ is 3d⁷: five electrons fill the d orbitals singly and two "
    "pair up, leaving three unpaired electrons. Both have μ = √15 ≈ 3.87 BM.",
    ["Cr³⁺ 3d³ → 3; Co²⁺ 3d⁷ → 3 ✓", "Ti³⁺ 3d¹ (1) vs V³⁺ 3d² (2)", "Ni²⁺ 3d⁸ (2) vs Cu²⁺ 3d⁹ (1)",
     "Mn²⁺ 3d⁵ (5) vs Fe²⁺ 3d⁶ (4)"],
    why="In each other pair the ions differ by one unpaired electron. The trap is Co²⁺: it has seven d "
        "electrons but only three are unpaired.",
    ncert=f"{REF11}, magnetic properties", seconds=60)

add("Transition element trends", A, "multi_statement",
    ms("Which of the following statements about the atomic sizes of the d-block elements are correct?",
       ["The 3d elements are smaller than the 4d elements of the same group.",
        "The 4d and 5d elements of the same group have almost the same atomic radii.",
        "The atomic radii of the 3d elements increase steadily from scandium to zinc.",
        "The lanthanoid contraction arises because 4f electrons shield the nucleus very effectively."]),
    multi("C", {"a": True, "b": True, "c": False, "d": False},
          ["(a), (b) and (c) only", "(b) and (d) only", "(a) and (c) only"]),
    "Atomic radii of transition elements and the lanthanoid contraction",
    "Radius increases from the 3d to the 4d series as a shell is added, but the 5d series is almost the same size "
    "as the 4d series (e.g. Zr 160 pm, Hf 159 pm) because the filling of the 4f subshell before the 5d series "
    "causes the lanthanoid contraction. That contraction is due to the IMPERFECT shielding of one 4f electron by "
    "another. Across the 3d series the radii decrease at first and then change little; they do not rise "
    "steadily.",
    ["(a) ✓", "(b) ✓ lanthanoid contraction", "(c) ✗", "(d) ✗ imperfect shielding"],
    why="Statements (c) and (d) are false, so every option containing them is wrong.",
    ncert=f"{REF11}, atomic and ionic sizes of transition metals; lanthanoid contraction", seconds=60)

e_mn, e_cr = 7 - 2, 6 - 3
assert (e_mn, e_cr) == (5, 3)
add("K2Cr2O7 and KMnO4", A, "statement_pair",
    sp("In the permanganate ion and the dichromate ion, manganese and chromium are in their group oxidation "
       "states, +7 and +6 respectively.",
       "When they act as oxidising agents in acidic solution, MnO₄⁻ gains five electrons per manganese atom, "
       "whereas Cr₂O₇²⁻ gains three electrons per chromium atom."),
    SP_, "Oxidation states and electron gain of permanganate and dichromate",
    "Mn (group 7) is +7 in MnO₄⁻ and Cr (group 6) is +6 in Cr₂O₇²⁻: Statement I is true. In acid, MnO₄⁻ → Mn²⁺ "
    "(+7 → +2, five electrons) and Cr₂O₇²⁻ → 2Cr³⁺ (+6 → +3, three electrons per Cr, six per ion): Statement II "
    "is true.",
    ["I: +7 and +6 = group numbers → true", "II: Mn +7 → +2 (5e⁻); Cr +6 → +3 (3e⁻ each) → true"],
    answer="A",
    why="Both statements hold; the 'six electrons' usually quoted for dichromate is per Cr₂O₇²⁻ ion, i.e. three "
        "per chromium atom.",
    ncert=f"{REF11}, potassium dichromate and potassium permanganate: oxidising action", seconds=45)

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
    doc = {"schema_version": "1.0", "batch_id": "BATCH_008", "created_at": TODAY,
           "notes": "Package CHE_008_p1: 123 original Chemistry questions (physical and inorganic chemistry). "
                    "Numerical answers re-derived in tools/batch_008/CHE_008_p1.py.",
           "stimuli": [], "questions": QUESTIONS}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {OUT}: {n} questions; difficulty {dict(Counter(q['difficulty'] for q in QUESTIONS))}; "
          f"formats {dict(fmts)}; keys {dict(sorted(KEYS.items()))}")
