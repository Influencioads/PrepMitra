"""Writes batches/parts/BATCH_006_CHE_p1.json: package CHE_006_p1 of BATCH_006 (Chemistry, 131 questions).

Topics: Some Basic Concepts, Atomic Structure, Chemical Bonding, Thermodynamics, Solutions, Equilibrium,
Redox and Electrochemistry, Chemical Kinetics, Periodicity, p-Block Elements, d- and f-Block Elements.
IDs NEET_CHE_001251..001381.

Every computable answer is re-derived here with an assert before anything is written; the quota per
(topic, difficulty), the ID range, the format mix and the answer-key balance are asserted too.
The position of every correct option is chosen by hand in the call that adds the question (argument `at`)
and never moved by code.

    cd docs/neet-bank && python tools/batch_006/CHE_006_p1.py
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
PACKAGE = "CHE_006_p1"
PLAN = ROOT / "batches" / "plans" / "BATCH_006_plan.json"
OUT = ROOT / "batches" / "parts" / "BATCH_006_CHE_p1.json"
TODAY = "2026-11-16"
LETTERS = "ABCD"
CHE = "Chemistry"
FIRST_ID = 1251
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

m_glu = (6 * 12 + 12 * 1 + 6 * 16) / NA
assert close(m_glu, 2.99e-22) and close(1 / NA, 1.66e-24, 0.01) and close(180 * NA, 1.08e26, 0.01)
add("Mole concept", B, "numerical",
    "The mass of a single molecule of glucose, C₆H₁₂O₆, is (C = 12, H = 1, O = 16, Nₐ = 6.022 × 10²³ mol⁻¹):",
    Opts("B", "2.99 × 10⁻²² g", ["1.66 × 10⁻²⁴ g", "1.08 × 10²⁶ g", "2.99 × 10⁻²³ g"]),
    "Mass of one molecule from the molar mass",
    "One mole of glucose (180 g) contains Nₐ molecules, so the mass of one molecule is the molar mass divided "
    "by the Avogadro constant.",
    ["M(C₆H₁₂O₆) = 72 + 12 + 96 = 180 g mol⁻¹", "m = 180 / (6.022 × 10²³) = 2.99 × 10⁻²² g"],
    why="1.66 × 10⁻²⁴ g is 1/Nₐ, the mass of 1 u, without multiplying by 180. 1.08 × 10²⁶ g multiplies by Nₐ "
        "instead of dividing. 2.99 × 10⁻²³ g has a power-of-ten slip.",
    ncert=f"{REF1}, mole concept and molar masses", seconds=30, checked=True)

assert 1.6 / 2.0 == 4.0 / 5.0 == 0.8
add("Laws of chemical combination", B, "direct",
    "A metal oxide is collected from two different sources. 2.0 g of the sample from source X contains 1.6 g of "
    "the metal, and 5.0 g of the sample from source Y contains 4.0 g of the metal. These data illustrate the:",
    Opts("D", "law of definite proportions",
         ["law of multiple proportions", "law of conservation of mass", "Gay-Lussac's law of gaseous volumes"]),
    "Law of definite proportions",
    "Both samples contain 80% metal by mass (1.6/2.0 = 4.0/5.0 = 0.80). A given compound always contains the "
    "same elements in the same proportion by mass, whatever its source: this is Proust's law of definite "
    "proportions.",
    ["Source X: 1.6/2.0 = 80% metal", "Source Y: 4.0/5.0 = 80% metal", "Same composition → definite proportions"],
    why="Multiple proportions needs two different compounds of the same two elements. No reaction masses are "
        "compared (conservation of mass), and no gas volumes are involved (Gay-Lussac).",
    ncert=f"{REF1}, law of definite proportions", seconds=30)

m_mgso4 = 24 + 32 + 4 * 16
loss = {x: 18 * x / (m_mgso4 + 18 * x) for x in (5, 6, 7, 10)}
assert m_mgso4 == 120 and round(100 * loss[7], 1) == 51.2
assert round(100 * loss[6], 1) == 47.4 and round(100 * loss[5], 1) == 42.9 and round(100 * loss[10], 1) == 60.0
add("Empirical and molecular formulae", I, "numerical",
    "A sample of hydrated magnesium sulphate, MgSO₄·xH₂O, loses 51.2% of its mass when it is heated until "
    "all the water of crystallisation is driven off, leaving anhydrous MgSO₄. The value of x is "
    "(Mg = 24, S = 32, O = 16, H = 1):",
    Opts("A", "7", ["6", "5", "10"]),
    "Formula of a hydrate from mass loss",
    "The mass lost is the water of crystallisation. Convert the mass of water and the mass of the anhydrous "
    "salt left (per 100 g) into moles; their ratio is x.",
    ["Per 100 g: water = 51.2 g, MgSO₄ = 48.8 g", "n(H₂O) = 51.2/18 = 2.84 mol; n(MgSO₄) = 48.8/120 = 0.407 mol",
     "x = 2.84/0.407 = 7.0 → MgSO₄·7H₂O"],
    shortcut="Check x = 7: 126/(120 + 126) = 0.512, i.e. 51.2%.",
    why="x = 6, 5 and 10 would give mass losses of 47.4%, 42.9% and 60.0% respectively.",
    ncert=f"{REF1}, empirical and molecular formula", seconds=75, checked=True)

n_acid = 0.050 * 0.2
m_naoh = 2 * n_acid * 40
assert close(m_naoh, 0.8) and close(n_acid * 40, 0.4) and close(2 * n_acid * 98, 1.96) \
    and close(2 * 0.5 * 0.2 * 40, 8.0)
add("Stoichiometry", I, "numerical",
    "The mass of sodium hydroxide needed to neutralise 50 mL of 0.2 M sulphuric acid completely, "
    "H₂SO₄ + 2NaOH → Na₂SO₄ + 2H₂O, is (Na = 23, O = 16, H = 1, S = 32):",
    Opts("C", "0.8 g", ["0.4 g", "1.96 g", "8.0 g"]),
    "Stoichiometry in solution: moles from molarity and volume",
    "Moles of acid = molarity × volume in litres. The balanced equation needs 2 mol NaOH per mole of H₂SO₄.",
    ["n(H₂SO₄) = 0.2 × 0.050 = 0.010 mol", "n(NaOH) = 2 × 0.010 = 0.020 mol", "m(NaOH) = 0.020 × 40 = 0.8 g"],
    why="0.4 g ignores the 1 : 2 mole ratio. 1.96 g uses the molar mass of H₂SO₄ (98) for NaOH. 8.0 g takes "
        "50 mL as 0.5 L.",
    ncert=f"{REF1}, stoichiometry and reactions in solutions", seconds=45, checked=True)

assert 3 / 2 < 2 / 1  # 3 mol A needs only 1.5 mol B: A runs out first, so A (not B) is limiting
assert 16 + 64 == 44 + 36
add("Stoichiometry", I, "statement_pair",
    sp("For the reaction 2A + B → C, when 3 mol of A is mixed with 2 mol of B, B is the limiting reagent.",
       "In the reaction CH₄ + 2O₂ → CO₂ + 2H₂O, 16 g of CH₄ burns completely in 64 g of O₂ to give 44 g of "
       "CO₂ and 36 g of H₂O (C = 12, H = 1, O = 16)."),
    SP_, "Limiting reagent; mass relationships in a balanced equation",
    "2 mol of B would need 4 mol of A, but only 3 mol of A is present, so A is used up first and is the "
    "limiting reagent (it consumes only 1.5 mol of B). Statement I is false. 1 mol CH₄ (16 g) needs 2 mol O₂ "
    "(64 g) and gives 1 mol CO₂ (44 g) and 2 mol H₂O (36 g); 16 + 64 = 44 + 36 = 80 g. Statement II is true.",
    ["3 mol A reacts with 1.5 mol B; 0.5 mol B is left → A limits (I false)",
     "1 mol CH₄ + 2 mol O₂ → 1 mol CO₂ + 2 mol H₂O: 16 g, 64 g, 44 g, 36 g (II true)"],
    answer="D", ncert=f"{REF1}, limiting reagent", seconds=45)

n_prop = 22 / 44
assert n_prop == 0.5 and n_prop * 5 * 32 == 80 and n_prop * 3 * 44 == 66 and n_prop * 4 == 2.0
assert n_prop * 5 * 2 == 5.0 and 22 + 80 == 66 + 36 == 102
add("Stoichiometry", A, "multi_statement",
    ms("22 g of propane burns completely in oxygen: C₃H₈(g) + 5O₂(g) → 3CO₂(g) + 4H₂O(l). Which of the "
       "following statements are correct? (C = 12, H = 1, O = 16)",
       ["80 g of oxygen is consumed.", "66 g of carbon dioxide is formed.", "1.5 mol of water is formed.",
        "2.5 mol of oxygen atoms is consumed.", "The total mass of the products is 102 g."]),
    multi("C", {"a": True, "b": True, "c": False, "d": False, "e": True},
          ["(a), (b), (c) and (e) only", "(b), (d) and (e) only", "(a), (b), (d) and (e) only"]),
    "Mole and mass relationships from a balanced equation",
    "22 g of propane is 0.5 mol. Multiply by each stoichiometric coefficient to get the amounts of the other "
    "species, then convert to masses where needed. Mass is conserved.",
    ["n(C₃H₈) = 22/44 = 0.5 mol", "(a) O₂: 0.5 × 5 = 2.5 mol = 80 g → true",
     "(b) CO₂: 0.5 × 3 = 1.5 mol = 66 g → true", "(c) H₂O: 0.5 × 4 = 2.0 mol, not 1.5 → false",
     "(d) 2.5 mol O₂ = 5.0 mol O atoms, not 2.5 → false", "(e) 66 + 36 = 102 g = 22 + 80 → true"],
    why="(c) uses the CO₂ coefficient for water; (d) confuses moles of O₂ molecules with moles of O atoms.",
    ncert=f"{REF1}, stoichiometry and stoichiometric calculations", seconds=90)

n_ba, n_so4 = 0.050 * 0.2, 0.050 * 0.1
ba_left = (n_ba - n_so4) / 0.100
assert close(ba_left, 0.05) and close(n_ba / 0.100, 0.10) and close((n_ba - n_so4 / 2) / 0.100, 0.075)
add("Stoichiometry", A, "numerical",
    "50 mL of 0.2 M BaCl₂ solution is mixed with 50 mL of 0.1 M Na₂SO₄ solution, and BaSO₄ precipitates "
    "completely: Ba²⁺(aq) + SO₄²⁻(aq) → BaSO₄(s). Assuming the volumes are additive, the concentration of Ba²⁺ "
    "ions left in the solution is:",
    Opts("A", "0.05 M", ["0.10 M", "0.075 M", "0.20 M"]),
    "Limiting reagent in a precipitation; concentration after mixing",
    "Find the moles of each ion, let the limiting one (SO₄²⁻) react completely in a 1 : 1 ratio, and divide the "
    "Ba²⁺ left over by the total volume of 100 mL.",
    ["n(Ba²⁺) = 0.050 × 0.2 = 0.010 mol; n(SO₄²⁻) = 0.050 × 0.1 = 0.005 mol",
     "SO₄²⁻ is limiting: 0.005 mol Ba²⁺ precipitates, 0.005 mol remains",
     "[Ba²⁺] = 0.005 / 0.100 L = 0.05 M"],
    why="0.10 M ignores the precipitation (all 0.010 mol in 100 mL). 0.075 M assumes Ba²⁺ and SO₄²⁻ react 1 : 2. "
        "0.20 M is the concentration before mixing.",
    ncert=f"{REF1}, limiting reagent and reactions in solutions", seconds=90, checked=True)

# ==================================================================== 2. Atomic Structure
topic("Atomic Structure")
REF2 = f"{C11}, 'Structure of Atom'"

lam = H_PLANCK / (1e-6 * 10)
assert close(lam, 6.626e-29) and close(H_PLANCK / (1e-3 * 10), 6.626e-32) and close(H_PLANCK / (1e-9 * 10), 6.626e-26)
add("Dual nature and uncertainty", B, "numerical",
    "The de Broglie wavelength of a dust particle of mass 1 mg moving with a speed of 10 m s⁻¹ is "
    "(h = 6.626 × 10⁻³⁴ J s):",
    Opts("C", "6.626 × 10⁻²⁹ m", ["6.626 × 10⁻³² m", "6.626 × 10⁻²⁶ m", "6.626 × 10⁻³⁹ m"]),
    "de Broglie relation λ = h/mv",
    "Convert the mass to kilograms (1 mg = 10⁻⁶ kg) and use λ = h/(mv). The wavelength is far too small to "
    "detect, which is why wave behaviour is not seen for everyday objects.",
    ["m = 1 mg = 1 × 10⁻⁶ kg", "λ = 6.626 × 10⁻³⁴ / (10⁻⁶ × 10) = 6.626 × 10⁻²⁹ m"],
    why="6.626 × 10⁻³² m takes 1 mg as 10⁻³ kg, and 6.626 × 10⁻²⁶ m takes it as 10⁻⁹ kg. 6.626 × 10⁻³⁹ m "
        "multiplies h by mv instead of dividing.",
    ncert=f"{REF2}, dual behaviour of matter", seconds=35, checked=True)

add("Bohr model and hydrogen spectrum", B, "direct",
    "Which of the following lists the radiations in order of increasing wavelength?",
    Opts("B", "X-rays < ultraviolet < visible < infrared",
         ["Infrared < visible < ultraviolet < X-rays", "Ultraviolet < X-rays < visible < infrared",
          "X-rays < visible < ultraviolet < infrared"]),
    "The electromagnetic spectrum",
    "Wavelength and frequency are inversely related (c = νλ). In the electromagnetic spectrum the frequency "
    "decreases, and hence the wavelength increases, in the order X-rays, ultraviolet, visible, infrared, "
    "microwaves, radio waves.",
    ["Highest frequency (shortest λ): X-rays", "then UV, then visible, then IR (longest λ of the four)"],
    why="The first wrong option is the order of decreasing wavelength. The other two misplace X-rays or "
        "ultraviolet with respect to visible light.",
    ncert=f"{REF2}, electromagnetic radiation", seconds=25)

assert 11 - 1 == 12 - 2 == 9 + 1 == 10
add("Electronic configuration", B, "statement_pair",
    sp("Na⁺, Mg²⁺ and F⁻ are isoelectronic species.",
       "The charge-to-mass ratio of the positively charged particles in canal rays depends on the nature of the "
       "gas present in the discharge tube."),
    SP_, "Isoelectronic species; canal rays",
    "Na⁺ (11 − 1), Mg²⁺ (12 − 2) and F⁻ (9 + 1) each have 10 electrons, so they are isoelectronic: Statement I "
    "is true. Unlike cathode rays, the positive particles of canal rays are ions of the gas in the tube, so "
    "their mass and charge-to-mass ratio depend on the gas: Statement II is true.",
    ["Electrons: Na⁺ 10, Mg²⁺ 10, F⁻ 10 (I true)", "Canal-ray particles are gaseous ions → e/m depends on the gas "
     "(II true)"],
    answer="A", ncert=f"{REF2}, discovery of the proton and isoelectronic species", seconds=30)

v1 = H_PLANCK / (2 * 3.14 * 9.11e-31 * 52.9e-12)
assert close(v1, 2.19e6) and close(v1 / 2, 1.09e6, 0.01) and close(v1 * 2 * 3.14, 1.375e7, 0.01) \
    and close(2 * v1, 4.38e6)
add("Bohr model and hydrogen spectrum", I, "numerical",
    "In Bohr's model, the angular momentum of the electron in the nth orbit is mvr = nh/2π. Using this, the "
    "speed of the electron in the first orbit (r = 52.9 pm) of a hydrogen atom is (h = 6.626 × 10⁻³⁴ J s, "
    "mass of electron = 9.11 × 10⁻³¹ kg, π = 3.14):",
    Opts("D", "2.19 × 10⁶ m s⁻¹", ["1.09 × 10⁶ m s⁻¹", "1.38 × 10⁷ m s⁻¹", "4.38 × 10⁶ m s⁻¹"]),
    "Quantisation of angular momentum in Bohr's model",
    "For n = 1, mvr = h/2π, so v = h/(2πmr). Substitute the values in SI units (52.9 pm = 52.9 × 10⁻¹² m).",
    ["v = h / (2π m r)", "2π m r = 6.28 × 9.11 × 10⁻³¹ × 52.9 × 10⁻¹² = 3.03 × 10⁻⁴⁰ kg m",
     "v = 6.626 × 10⁻³⁴ / 3.03 × 10⁻⁴⁰ = 2.19 × 10⁶ m s⁻¹"],
    why="1.09 × 10⁶ m s⁻¹ uses h/4π, 1.38 × 10⁷ m s⁻¹ leaves out 2π altogether, and 4.38 × 10⁶ m s⁻¹ divides "
        "by π instead of 2π.",
    ncert=f"{REF2}, Bohr's model for hydrogen atom", seconds=70, checked=True)

e_he2, e_h1 = F(2 ** 2, 2 ** 2), F(1, 1)
assert e_he2 / e_h1 == 1 and F(2, 4) == F(1, 2) and F(1, 4) == F(1, 4) and F(4, 2) == 2
add("Bohr model and hydrogen spectrum", I, "numerical",
    "According to Bohr's theory, the energy of the electron in a hydrogen-like species is "
    "Eₙ = −2.18 × 10⁻¹⁸ (Z²/n²) J. The ratio of the energy of the electron in the second orbit of He⁺ (Z = 2) "
    "to that in the first orbit of the hydrogen atom is:",
    Opts("A", "1 : 1", ["1 : 2", "1 : 4", "2 : 1"]),
    "Dependence of Bohr energy on Z and n",
    "Eₙ is proportional to Z²/n². For He⁺ with n = 2, Z²/n² = 4/4 = 1, which is the same as for hydrogen "
    "with n = 1 (1/1). Both energies are −2.18 × 10⁻¹⁸ J.",
    ["He⁺, n = 2: Z²/n² = 4/4 = 1", "H, n = 1: Z²/n² = 1/1 = 1", "Ratio = 1 : 1"],
    why="1 : 2 uses Z instead of Z², 1 : 4 leaves out Z altogether, and 2 : 1 divides Z² by n instead of n².",
    ncert=f"{REF2}, Bohr's model for hydrogen atom", seconds=40, checked=True)

add("Bohr model and hydrogen spectrum", I, "match_list",
    lists("Match List-I (quantity for a hydrogen-like species in Bohr's model) with List-II (how it depends on the "
          "principal quantum number n and the atomic number Z).",
          ["Radius of the nth orbit", "Energy of the electron in the nth orbit",
           "Angular momentum of the electron in the nth orbit",
           "Energy needed to remove the electron from the ground state"],
          ["Proportional to Z² alone", "Proportional to n²/Z", "Proportional to n and independent of Z",
           "Proportional to −Z²/n²"]),
    match("B", M("II IV III I"), [M("II IV I III"), M("IV II III I"), M("III IV II I")]),
    "Bohr's expressions for radius, energy and angular momentum",
    "Bohr's model gives rₙ = 52.9 (n²/Z) pm and Eₙ = −2.18 × 10⁻¹⁸ (Z²/n²) J. The angular momentum is "
    "quantised as mvr = nh/2π, which does not contain Z. The energy needed to remove the electron from n = 1 "
    "is 2.18 × 10⁻¹⁸ Z² J, proportional to Z².",
    ["A → II (rₙ ∝ n²/Z)", "B → IV (Eₙ ∝ −Z²/n²)", "C → III (mvr = nh/2π)", "D → I (IE from n = 1 ∝ Z²)"],
    why="Matching C with I or A with IV mixes up the radius, energy and angular-momentum formulae.",
    ncert=f"{REF2}, Bohr's model for hydrogen atom", seconds=50)

add("Electronic configuration", I, "multi_statement",
    ms("Which of the following statements about the energies of orbitals are correct?",
       ["In the hydrogen atom, the 3s, 3p and 3d orbitals have the same energy.",
        "In a multi-electron atom, of two orbitals with the same value of (n + l), the one with the lower value "
        "of n has the lower energy.",
        "In a multi-electron atom, the energy of an orbital depends only on its principal quantum number.",
        "For the same value of n, the effective nuclear charge experienced by an electron increases as l "
        "increases.",
        "In a ground-state nitrogen atom, the three 2p electrons occupy different 2p orbitals with parallel "
        "spins."]),
    multi("D", {"a": True, "b": True, "c": False, "d": False, "e": True},
          ["(a), (c) and (e) only", "(b), (d) and (e) only", "(a), (b), (d) and (e) only"]),
    "Energies of orbitals; effective nuclear charge; Hund's rule",
    "In hydrogen, orbital energy depends only on n, so all n = 3 orbitals are degenerate. In multi-electron "
    "atoms it depends on n and l: the lower (n + l) comes first, and for equal (n + l) the lower n. Because "
    "s electrons penetrate closer to the nucleus, the effective nuclear charge decreases as l increases for "
    "the same n. By Hund's rule, nitrogen's 2p³ electrons are unpaired with parallel spins.",
    ["(a) True: H atom energy depends on n only", "(b) True: (n + l) rule", "(c) False: depends on n and l",
     "(d) False: Zeff decreases with increasing l", "(e) True: 2pₓ¹ 2p_y¹ 2p_z¹"],
    why="Options containing (c) or (d) are wrong.",
    ncert=f"{REF2}, energies of orbitals and filling of orbitals", seconds=60)

add("Bohr model and hydrogen spectrum", I, "assertion_reason",
    ar("Rutherford's nuclear model of the atom could not explain the stability of the atom.",
       "According to classical electromagnetic theory, an electron revolving round the nucleus is accelerating, "
       "so it should radiate energy continuously and spiral into the nucleus."),
    AR_, "Drawbacks of Rutherford's model",
    "A charged particle moving in a circular orbit is accelerated, and Maxwell's theory says an accelerated "
    "charge emits electromagnetic radiation. The electron would lose energy, its orbit would shrink and it "
    "would fall into the nucleus in a tiny fraction of a second. Real atoms are stable, so the model fails. "
    "R is the reason for A.",
    ["Orbiting electron → accelerated charge → emits radiation", "Energy lost → spiral into nucleus → atom "
     "unstable, contrary to fact"],
    answer="A", ncert=f"{REF2}, drawbacks of Rutherford model", seconds=35)

nu1 = 1.2e15
nu0 = nu1 / 2   # h nu1 - h nu0 = K and 2 h nu1 - h nu0 = 3K give h nu1 = 2K, so h nu0 = h nu1 - K = h nu1 / 2
assert close((2 * nu1 - nu0) / (nu1 - nu0), 3)
for wrong_nu0, ratio in ((4.0e14, 2.5), (8.0e14, 4.0), (9.0e14, 5.0)):
    assert close((2 * nu1 - wrong_nu0) / (nu1 - wrong_nu0), ratio)
add("Dual nature and uncertainty", A, "numerical",
    "Light of frequency 1.2 × 10¹⁵ Hz ejects photoelectrons from a metal surface with a maximum kinetic energy K. "
    "When light of frequency 2.4 × 10¹⁵ Hz falls on the same surface, the maximum kinetic energy of the "
    "photoelectrons is 3K. The threshold frequency of the metal is:",
    Opts("B", "6.0 × 10¹⁴ Hz", ["4.0 × 10¹⁴ Hz", "8.0 × 10¹⁴ Hz", "9.0 × 10¹⁴ Hz"]),
    "Photoelectric equation: ½mv² = hν − hν₀",
    "Write the photoelectric equation for both frequencies and solve the two equations for hν₀.",
    ["h(1.2 × 10¹⁵) − hν₀ = K ...(1)", "h(2.4 × 10¹⁵) − hν₀ = 3K ...(2)",
     "(2) − (1): h(1.2 × 10¹⁵) = 2K, so K = h(0.6 × 10¹⁵)",
     "From (1): hν₀ = h(1.2 × 10¹⁵) − h(0.6 × 10¹⁵) → ν₀ = 6.0 × 10¹⁴ Hz"],
    why="With ν₀ = 4.0, 8.0 or 9.0 × 10¹⁴ Hz the kinetic energies at the two frequencies would be in the ratio "
        "2.5, 4 or 5, not 3. 4.0 × 10¹⁴ Hz comes from dividing 1.2 × 10¹⁵ by the ratio 3.",
    ncert=f"{REF2}, photoelectric effect", seconds=90, checked=True)

add("Electronic configuration", A, "assertion_reason",
    ar("A ground-state Cr⁺ ion (Z of Cr = 24) has five unpaired electrons.",
       "The ground-state configuration of chromium is [Ar] 3d⁵ 4s¹, and when it ionises the 4s electron is "
       "removed first."),
    AR_, "Configurations of transition-metal ions",
    "Chromium takes the configuration [Ar] 3d⁵ 4s¹ because of the extra stability of the half-filled 3d "
    "subshell. When it loses one electron, the outermost 4s electron goes, leaving Cr⁺ as [Ar] 3d⁵ with five "
    "unpaired electrons. R gives the configuration that leads to A.",
    ["Cr: [Ar] 3d⁵ 4s¹", "Cr⁺: remove 4s¹ → [Ar] 3d⁵", "Five singly occupied 3d orbitals → 5 unpaired"],
    answer="A", ncert=f"{REF2}, electronic configuration of atoms", seconds=45)

add("Dual nature and uncertainty", A, "statement_pair",
    sp("An electron and a proton moving with the same speed have the same de Broglie wavelength.",
       "If an electron and a proton have the same kinetic energy, the electron has the longer de Broglie "
       "wavelength."),
    SP_, "de Broglie wavelength in terms of speed and kinetic energy",
    "λ = h/mv: at the same speed the much lighter electron has a much longer wavelength, so Statement I is "
    "false. Since p = √(2mK), λ = h/√(2mK); at the same kinetic energy the particle of smaller mass (the "
    "electron) has the smaller momentum and the longer wavelength, so Statement II is true.",
    ["Same v: λ ∝ 1/m → λₑ ≫ λₚ (I false)", "Same K: λ = h/√(2mK) ∝ 1/√m → λₑ > λₚ (II true)"],
    answer="D", ncert=f"{REF2}, dual behaviour of matter", seconds=50)

# ==================================================================== 3. Chemical Bonding and Molecular Structure
topic("Chemical Bonding and Molecular Structure")
REF3 = f"{C11}, 'Chemical Bonding and Molecular Structure'"


def bond_order(nb, na):
    return F(nb - na, 2)


assert 12 - 2 == 8 + 2 == 10
add("Ionic bonding and lattice enthalpy", B, "direct",
    "When magnesium oxide forms from its elements, the magnesium atom loses two electrons and the oxygen atom "
    "gains two electrons. The ions Mg²⁺ and O²⁻ formed both have the electronic configuration of:",
    Opts("C", "neon", ["argon", "helium", "sodium"]),
    "Kössel's electrovalent bonding: ions with noble-gas configurations",
    "Mg (2, 8, 2) loses its two 3s electrons to become Mg²⁺ (2, 8). O (2, 6) gains two electrons to become "
    "O²⁻ (2, 8). Both have the configuration of neon, 1s² 2s² 2p⁶.",
    ["Mg²⁺: 12 − 2 = 10 electrons", "O²⁻: 8 + 2 = 10 electrons", "10 electrons, 2, 8 → neon"],
    why="Argon has 18 electrons and helium 2. Sodium is not a noble gas, and a sodium atom has 11 electrons.",
    ncert=f"{REF3}, Kössel-Lewis approach: electrovalent bond", seconds=25)

add("VSEPR shapes", B, "match_list",
    lists("Match List-I (number of electron pairs around the central atom, all of them bond pairs) with List-II "
          "(geometry predicted by VSEPR theory).",
          ["Two", "Three", "Four", "Five"],
          ["Tetrahedral", "Trigonal bipyramidal", "Linear", "Trigonal planar"]),
    match("D", M("III IV I II"), [M("III I IV II"), M("IV III I II"), M("III IV II I")]),
    "VSEPR: arrangement of electron pairs that minimises repulsion",
    "Electron pairs keep as far apart as possible: two pairs at 180° (linear), three at 120° (trigonal planar), "
    "four at 109.5° (tetrahedral) and five in a trigonal bipyramid (90° and 120°).",
    ["2 → linear (e.g. BeCl₂)", "3 → trigonal planar (e.g. BF₃)", "4 → tetrahedral (e.g. CH₄)",
     "5 → trigonal bipyramidal (e.g. PCl₅)"],
    why="The wrong codes swap trigonal planar with tetrahedral, or linear with trigonal planar, or the "
        "four- and five-pair geometries.",
    ncert=f"{REF3}, VSEPR theory (geometry of molecules with no lone pairs)", seconds=30)

add("Fajans' rule and dipole moment", B, "statement_pair",
    sp("Dipole moment is a vector quantity.",
       "In the crossed-arrow symbol used to show a bond dipole, the cross is on the positive end and the arrow "
       "head points to the negative end of the dipole."),
    SP_, "Dipole moment as a vector",
    "Dipole moment (charge × distance) has both magnitude and direction, so it is a vector; it is shown by a "
    "small arrow with a cross at its tail, the cross on the positive end and the arrow head on the negative "
    "end. Both statements are true.",
    ["μ = Q × r, with direction → vector (I true)", "Convention: +→ cross at positive end, head at negative end "
     "(II true)"],
    answer="A", ncert=f"{REF3}, polarity of bonds: dipole moment", seconds=25)

bo = {"Ne2": bond_order(10, 10), "Li2": bond_order(4, 2), "B2": bond_order(6, 4), "C2": bond_order(8, 4)}
assert bo["Ne2"] == 0 and bo["Li2"] == 1 and bo["B2"] == 1 and bo["C2"] == 2
add("Molecular orbital theory", B, "direct",
    "According to molecular orbital theory, which of the following molecules is NOT expected to exist?",
    Opts("B", "Ne₂", ["Li₂", "B₂", "C₂"]),
    "Bond order and stability",
    "A molecule is expected to be stable only if its bond order, ½(N_b − N_a), is positive. In Ne₂ (20 "
    "electrons) all the bonding and antibonding molecular orbitals up to σ*2p_z are filled, so N_b = N_a = 10 "
    "and the bond order is zero.",
    ["Ne₂: N_b = 10, N_a = 10 → bond order 0 → not expected to exist", "Li₂: (4 − 2)/2 = 1; B₂: (6 − 4)/2 = 1; "
     "C₂: (8 − 4)/2 = 2"],
    why="Li₂, B₂ and C₂ all have positive bond orders (1, 1 and 2), so they are expected to exist.",
    ncert=f"{REF3}, molecular orbital theory: bond order", seconds=35)

add("Hydrogen and metallic bonding", B, "direct",
    "The magnitude of hydrogen bonding in a compound is the greatest when the compound is in the:",
    Opts("D", "solid state", ["gaseous state", "liquid state", "same in all three states"]),
    "Hydrogen bonding and physical state",
    "NCERT notes that the magnitude of hydrogen bonding depends on the physical state of the compound: it is "
    "maximum in the solid state and minimum in the gaseous state, where the molecules are far apart.",
    ["Molecules closest and most ordered in the solid → maximum hydrogen bonding",
     "Molecules far apart in the gas → minimum"],
    why="Hydrogen bonding is weakest, not strongest, in the gaseous state; the liquid is intermediate; and it "
        "does depend on the state.",
    ncert=f"{REF3}, hydrogen bonding", seconds=20)

add("Hybridisation and resonance", B, "direct",
    "The canonical (resonance) structures of a molecule differ from one another only in the:",
    Opts("B", "arrangement of the electrons, the positions of the nuclei being the same",
         ["positions of the atomic nuclei, the electrons being the same",
          "number of unpaired electrons",
          "total number of valence electrons"]),
    "Conditions for resonance",
    "Canonical structures are different ways of writing the electron distribution of the same molecule. The "
    "positions of the nuclei, the total number of electrons and the number of unpaired electrons are the "
    "same in all of them; only the placing of bonding and non-bonding electrons differs.",
    ["Same skeleton (nuclei fixed)", "Same total and unpaired electrons", "Different placing of electron pairs"],
    why="Structures with nuclei in different positions are different compounds (isomers), not resonance "
        "structures. The numbers of unpaired and of valence electrons must be the same in every canonical form.",
    ncert=f"{REF3}, resonance structures", seconds=25)

n2, n2_2m = bond_order(10, 4), bond_order(10, 6)
assert n2 == 3 and n2_2m == 2 and bond_order(10, 5) == F(5, 2) and bond_order(12, 4) == 4
add("Molecular orbital theory", I, "numerical",
    "When a nitrogen molecule, N₂, gains two electrons to form the N₂²⁻ ion, the bond order predicted by "
    "molecular orbital theory changes from 3 to:",
    Opts("C", "2", ["2.5", "4", "1"]),
    "Bond order from the molecular orbital configuration",
    "N₂ has 14 electrons with all bonding orbitals up to σ2p_z filled (bond order 3). The two extra electrons "
    "of N₂²⁻ go into the antibonding π*2pₓ and π*2p_y orbitals, each lowering the bond order by ½.",
    ["N₂²⁻: 16 electrons", "N_b = 10 (σ1s², σ2s², π2pₓ², π2p_y², σ2p_z²)",
     "N_a = 6 (σ*1s², σ*2s², π*2pₓ¹, π*2p_y¹)", "Bond order = (10 − 6)/2 = 2"],
    why="2.5 adds only one electron. 4 puts the two electrons into bonding orbitals, but none is vacant. "
        "1 removes ½ too many for each electron added.",
    ncert=f"{REF3}, molecular orbital theory: bond order", seconds=50, checked=True)

add("Fajans' rule and dipole moment", I, "multi_statement",
    ms("Which of the following statements about the partial covalent character of ionic bonds (Fajans' rules) "
       "are correct?",
       ["The greater the charge on the cation, the greater the covalent character of the bond.",
        "The larger the anion, the more easily it is polarised.",
        "Among the halides of the same cation, the fluoride has the greatest covalent character.",
        "Polarisation of the anion by the cation increases the ionic character of the bond.",
        "The smaller the cation, the greater the covalent character of the bond."]),
    multi("B", {"a": True, "b": True, "c": False, "d": False, "e": True},
          ["(a), (b) and (c) only", "(b), (d) and (e) only", "(a), (b), (d) and (e) only"]),
    "Fajans' rules",
    "A small, highly charged cation distorts (polarises) the electron cloud of the anion towards itself, "
    "which puts electron density between the ions: the bond gains covalent character. A large anion, whose "
    "outer electrons are loosely held, is polarised most easily.",
    ["(a) True", "(b) True", "(c) False: F⁻ is the smallest, least polarisable halide → least covalent",
     "(d) False: polarisation increases covalent character", "(e) True"],
    why="Options containing (c) or (d) are wrong.",
    ncert=f"{REF3}, partial covalent character of ionic bonds", seconds=45)

add("VSEPR shapes", I, "match_list",
    lists("Match List-I (VSEPR type, A = central atom, B = bonded atom, E = lone pair on A) with List-II (shape of "
          "the molecule).",
          ["AB₂E", "AB₃E₂", "AB₄E₂", "AB₅E"],
          ["Square planar", "Square pyramidal", "Bent", "T-shaped"]),
    match("D", M("III IV I II"), [M("III I IV II"), M("IV III I II"), M("III IV II I")]),
    "Shapes of molecules having lone pairs",
    "Count all electron pairs to get the basic arrangement, then describe the shape by the positions of the "
    "atoms only. Lone pairs take the positions that minimise lone pair repulsions.",
    ["AB₂E: 3 pairs, trigonal planar arrangement → bent (e.g. SO₂)",
     "AB₃E₂: 5 pairs, two equatorial lone pairs → T-shaped (e.g. ClF₃)",
     "AB₄E₂: 6 pairs, lone pairs trans → square planar (e.g. XeF₄)",
     "AB₅E: 6 pairs, one lone pair → square pyramidal (e.g. BrF₅)"],
    why="The wrong codes interchange the two shapes derived from the octahedron (square planar and square "
        "pyramidal), or the bent and T-shaped molecules.",
    ncert=f"{REF3}, VSEPR theory (molecules with lone pairs)", seconds=50)

add("VSEPR shapes", I, "assertion_reason",
    ar("XeF₄ is square planar although there are six electron pairs around the xenon atom.",
       "The two lone pairs on xenon occupy opposite (trans) positions of the octahedron, which keeps the lone "
       "pair–lone pair repulsion to a minimum."),
    AR_, "Shape of an AB₄E₂ molecule",
    "Four bond pairs and two lone pairs give an octahedral arrangement of electron pairs. Lone pair–lone pair "
    "repulsion is the strongest, so the two lone pairs sit at 180° to each other, above and below the plane. "
    "The four F atoms then lie in one plane at the corners of a square. R explains A.",
    ["6 electron pairs → octahedral arrangement", "2 lone pairs trans (180°) → minimum lp–lp repulsion",
     "4 F atoms in a plane → square planar"],
    answer="A", ncert=f"{REF3}, VSEPR theory", seconds=40)

add("Hybridisation and resonance", I, "statement_pair",
    sp("In SF₆, the six sp³d² hybrid orbitals of sulphur are directed towards the corners of a regular "
       "octahedron.",
       "Hybridisation can take place in an isolated atom, before it forms any bond."),
    SP_, "Features of hybridisation",
    "Sulphur mixes one 3s, three 3p and two 3d orbitals to give six equivalent sp³d² orbitals pointing to the "
    "corners of an octahedron; these overlap with F orbitals to give octahedral SF₆. Statement I is true. "
    "NCERT states that hybridisation never takes place in an isolated atom; it occurs only during bond "
    "formation. Statement II is false.",
    ["SF₆: sp³d² → octahedral (I true)", "Hybridisation occurs only at the time of bond formation (II false)"],
    answer="C", ncert=f"{REF3}, hybridisation", seconds=35)

add("Molecular orbital theory", I, "multi_statement",
    ms("Which of the following statements are correct according to molecular orbital theory?",
       ["In the N₂ molecule, all the electrons are paired.",
        "The N₂ molecule has a shorter bond than the N₂⁺ ion.",
        "Adding an electron to O₂ to form O₂⁻ increases the bond order.",
        "The F₂⁺ ion has a higher bond order than the F₂ molecule.",
        "The O₂⁺ ion is less stable than the O₂ molecule."]),
    multi("B", {"a": True, "b": True, "c": False, "d": True, "e": False},
          ["(a), (b) and (c) only", "(b), (d) and (e) only", "(a) and (d) only"]),
    "Bond order, bond length, stability and magnetism",
    "Bond order = ½(N_b − N_a). A higher bond order means a shorter, stronger, more stable bond. Removing an "
    "electron from a bonding orbital lowers the bond order; removing one from an antibonding orbital raises it.",
    ["(a) True: N₂ has no electron in π* → diamagnetic",
     "(b) True: N₂ bond order 3 > N₂⁺ 2.5 (bonding electron lost) → N₂ bond shorter",
     "(c) False: the extra electron enters π*, bond order falls from 2 to 1.5",
     "(d) True: F₂⁺ loses a π* electron, bond order rises from 1 to 1.5",
     "(e) False: O₂⁺ (bond order 2.5) is more stable than O₂ (2)"],
    why="(c) and (e) reverse the effect of adding or removing an antibonding electron.",
    ncert=f"{REF3}, molecular orbital theory: bond order, bond length, magnetic nature", seconds=70)

add("Fajans' rule and dipole moment", I, "direct",
    "In which of the following pairs is one molecule polar and the other non-polar?",
    Opts("D", "BF₃ and NF₃", ["CO₂ and CH₄", "H₂O and SO₂", "NH₃ and CH₂Cl₂"]),
    "Molecular shape and dipole moment",
    "A molecule is non-polar when its bond dipoles cancel because of its symmetrical shape. BF₃ is trigonal "
    "planar and its three B–F bond dipoles cancel (μ = 0). NF₃ is pyramidal with a lone pair, so it has a net "
    "dipole moment.",
    ["BF₃: trigonal planar → μ = 0", "NF₃: pyramidal → μ ≠ 0", "CO₂ (linear), CH₄ (tetrahedral): both non-polar",
     "H₂O, SO₂ (bent), NH₃ (pyramidal), CH₂Cl₂: all polar"],
    why="CO₂ and CH₄ are both non-polar. H₂O and SO₂ are both bent and polar. NH₃ and CH₂Cl₂ are both polar.",
    ncert=f"{REF3}, dipole moment", seconds=40)

assert 110 < 115 < 121
add("Hybridisation and resonance", I, "assertion_reason",
    ar("The two carbon–oxygen bonds in CO₂ are of equal length (115 pm), a value lying between the C=O "
       "(121 pm) and C≡O (110 pm) bond lengths.",
       "CO₂ is a resonance hybrid of more than one canonical structure, and no single Lewis structure "
       "represents it correctly."),
    AR_, "Resonance and bond length",
    "NCERT points out that the experimentally found C–O bond length in CO₂ (115 pm) is shorter than a normal "
    "C=O bond and longer than a C≡O bond, and the two bonds are identical. This is explained by treating CO₂ "
    "as a resonance hybrid of its canonical structures. R explains A.",
    ["Observed: both C–O = 115 pm", "110 pm (C≡O) < 115 pm < 121 pm (C=O)",
     "Explained by resonance among canonical structures"],
    answer="A", ncert=f"{REF3}, resonance structures (CO₂)", seconds=40)

polar = {"BeF2": 0, "PCl5": 0, "SF6": 0, "CS2": 0, "ClF3": 1, "PCl3": 1, "H2S": 1, "OF2": 1}
zero = sum(1 for v in polar.values() if v == 0)
assert zero == 4
add("Fajans' rule and dipole moment", A, "numerical",
    "How many of the following molecules have zero dipole moment?\n\nBeF₂, PCl₅, ClF₃, SF₆, PCl₃, CS₂, H₂S, OF₂",
    Opts("C", "4", ["3", "5", "6"]),
    "Shape decides whether bond dipoles cancel",
    "Predict each shape by VSEPR. Bond dipoles cancel only in symmetrical shapes with no lone pair distorting "
    "the arrangement around the central atom (linear AB₂, trigonal bipyramidal AB₅, octahedral AB₆).",
    ["Zero: BeF₂ (linear), CS₂ (linear), PCl₅ (trigonal bipyramidal), SF₆ (octahedral) → 4",
     "Non-zero: ClF₃ (T-shaped), PCl₃ (pyramidal), H₂S and OF₂ (bent)"],
    why="3 misses one symmetrical molecule (usually PCl₅). 5 or 6 count T-shaped ClF₃ or the bent or pyramidal "
        "molecules as non-polar.",
    ncert=f"{REF3}, dipole moment and VSEPR shapes", seconds=75, checked=True)

add("VSEPR shapes", A, "statement_pair",
    sp("In XeF₂, the three lone pairs on xenon occupy the equatorial positions of a trigonal bipyramid, so the "
       "molecule is linear.",
       "In BrF₅, the bromine atom is sp³d hybridised."),
    SP_, "Lone-pair positions and hybridisation in AB₂E₃ and AB₅E molecules",
    "XeF₂ has 2 bond pairs and 3 lone pairs (5 pairs, trigonal bipyramidal arrangement). The lone pairs go to "
    "the three equatorial positions, where they are 120° apart, and the two F atoms sit in the axial positions "
    "at 180°: a linear molecule. Statement I is true. BrF₅ has 5 bond pairs and 1 lone pair, six pairs in all, "
    "so Br is sp³d² hybridised (square pyramidal). Statement II is false.",
    ["XeF₂: 2 bp + 3 lp, lone pairs equatorial → linear (I true)",
     "BrF₅: 5 bp + 1 lp = 6 pairs → sp³d², not sp³d (II false)"],
    answer="C", ncert=f"{REF3}, VSEPR theory and hybridisation", seconds=50)

add("VSEPR shapes", A, "multi_statement",
    ms("CF₄, SF₄ and XeF₄ all have the formula AF₄. Which of the following statements about them are correct?",
       ["CF₄ is tetrahedral and its carbon atom is sp³ hybridised.",
        "SF₄ has a non-zero dipole moment.",
        "The xenon atom in XeF₄ is sp³d² hybridised.",
        "All three molecules have the same F–A–F bond angles.",
        "The central atom of each of the three molecules carries at least one lone pair."]),
    multi("D", {"a": True, "b": True, "c": True, "d": False, "e": False},
          ["(a), (b), (c) and (e) only", "(a) and (c) only", "(b), (c) and (d) only"]),
    "Same formula type, different numbers of lone pairs",
    "C has 4 bond pairs (sp³, tetrahedral, no lone pair). S has 4 bond pairs and 1 lone pair (sp³d, see-saw, "
    "polar). Xe has 4 bond pairs and 2 lone pairs (sp³d², square planar). So the shapes and angles differ.",
    ["(a) True", "(b) True: see-saw shape, dipoles do not cancel", "(c) True: 6 electron pairs",
     "(d) False: 109.5° in CF₄, 90° in XeF₄, about 90° and 120° (distorted) in SF₄",
     "(e) False: carbon in CF₄ has no lone pair"],
    why="Options containing (d) or (e) are wrong, and (a) and (c) only leaves out the true statement (b).",
    ncert=f"{REF3}, VSEPR theory and hybridisation", seconds=80)

mo = {"O2--": (bond_order(10, 8), "dia"), "F2": (bond_order(10, 8), "dia"), "O2": (bond_order(10, 6), "para"),
      "C2": (bond_order(8, 4), "dia"), "B2": (bond_order(6, 4), "para"), "Li2": (bond_order(4, 2), "dia"),
      "O2-": (bond_order(10, 7), "para"), "N2": (bond_order(10, 4), "dia")}
assert mo["O2--"] == mo["F2"] and mo["O2"] != mo["C2"] and mo["B2"] != mo["Li2"] and mo["O2-"] != mo["N2"]
add("Molecular orbital theory", A, "direct",
    "Which of the following pairs of species have the same bond order AND the same magnetic behaviour, "
    "according to molecular orbital theory?",
    Opts("B", "O₂²⁻ and F₂", ["O₂ and C₂", "B₂ and Li₂", "O₂⁻ and N₂"]),
    "Bond order and magnetic behaviour from MO configurations",
    "O₂²⁻ and F₂ both have 18 electrons and the same configuration up to π*2p (all filled), so both have bond "
    "order 1 and no unpaired electron (diamagnetic).",
    ["O₂²⁻, F₂: (10 − 8)/2 = 1; diamagnetic", "O₂: 2, paramagnetic; C₂: 2, diamagnetic",
     "B₂: 1, paramagnetic (π2pₓ¹ π2p_y¹); Li₂: 1, diamagnetic", "O₂⁻: 1.5; N₂: 3"],
    why="O₂/C₂ and B₂/Li₂ have equal bond orders but differ in magnetism. O₂⁻ and N₂ differ in bond order.",
    ncert=f"{REF3}, molecular orbital theory", seconds=80)

assert 495.8 - 348.7 > 0 and 495.8 - 348.7 - 788 < 0
add("Ionic bonding and lattice enthalpy", A, "assertion_reason",
    ar("The change Na(g) + Cl(g) → Na⁺(g) + Cl⁻(g) is endothermic, yet sodium chloride forms as a stable "
       "ionic solid.",
       "The energy released when the gaseous ions pack together to form the crystal lattice of NaCl(s) "
       "(lattice enthalpy, 788 kJ mol⁻¹) more than makes up for this energy."),
    AR_, "Role of lattice enthalpy in ionic bond formation",
    "Ionisation of Na needs 495.8 kJ mol⁻¹ while electron gain by Cl releases only 348.7 kJ mol⁻¹, so forming "
    "the separated gaseous ions absorbs about 147 kJ mol⁻¹. The stability of the ionic solid comes from the "
    "large energy released on forming the lattice, which outweighs this. R explains A.",
    ["Na → Na⁺: +495.8; Cl → Cl⁻: −348.7 → net +147.1 kJ mol⁻¹ (endothermic)",
     "Lattice formation releases 788 kJ mol⁻¹ → overall strongly exothermic"],
    answer="A", ncert=f"{REF3}, ionic or electrovalent bond and lattice enthalpy", seconds=45)

# ==================================================================== 4. Chemical Thermodynamics
topic("Chemical Thermodynamics")
REF4 = f"{C11}, 'Thermodynamics'"

dh_no2 = 33.2
assert close(-2 * dh_no2, -66.4) and close(2 * dh_no2, 66.4) and close(-dh_no2 / 2, -16.6)
add("Hess's law and enthalpies", B, "numerical",
    "For the reaction ½N₂(g) + O₂(g) → NO₂(g), ΔrH° = +33.2 kJ mol⁻¹. The value of ΔrH° for the reaction "
    "2NO₂(g) → N₂(g) + 2O₂(g) is:",
    Opts("D", "−66.4 kJ mol⁻¹", ["+66.4 kJ mol⁻¹", "−33.2 kJ mol⁻¹", "−16.6 kJ mol⁻¹"]),
    "Manipulating thermochemical equations",
    "Reversing a thermochemical equation changes the sign of ΔrH; multiplying it by a factor multiplies ΔrH "
    "by the same factor. The required equation is the given one reversed and multiplied by 2.",
    ["Reverse: NO₂ → ½N₂ + O₂; ΔH = −33.2 kJ", "Multiply by 2: 2NO₂ → N₂ + 2O₂; ΔH = −66.4 kJ"],
    why="+66.4 kJ forgets to change the sign. −33.2 kJ forgets to double. −16.6 kJ halves instead of doubling.",
    ncert=f"{REF4}, thermochemical equations", seconds=30, checked=True)

add("Hess's law and enthalpies", B, "direct",
    "Hess's law of constant heat summation is a direct consequence of the fact that:",
    Opts("B", "enthalpy is a state function",
         ["heat is a path function", "every chemical reaction is exothermic", "the entropy of the universe "
          "increases in a spontaneous change"]),
    "Basis of Hess's law",
    "Because enthalpy is a state function, the enthalpy change between given initial and final states is "
    "the same whatever the path. So if a reaction takes place in several steps, the standard reaction enthalpy "
    "is the sum of the enthalpies of the steps.",
    ["ΔH depends only on the initial and final states", "→ ΔH(overall) = ΔH₁ + ΔH₂ + ... for any route"],
    why="Heat in general does depend on the path, which is why Hess's law must rest on enthalpy (heat at "
        "constant pressure) being a state function. Not all reactions are exothermic, and entropy is unrelated.",
    ncert=f"{REF4}, Hess's law of constant heat summation", seconds=25)

add("First law, work and enthalpy", B, "statement_pair",
    sp("For a given amount of heat supplied, a body with a larger heat capacity shows a smaller rise in "
       "temperature.",
       "The specific heat capacity of a substance is the heat needed to raise the temperature of one mole of it "
       "by one kelvin."),
    SP_, "Heat capacity, specific heat and molar heat capacity",
    "q = C ΔT, so ΔT = q/C: the larger C, the smaller the temperature rise. Statement I is true. Specific heat "
    "capacity refers to unit mass (for example one gram) of the substance; the heat needed per mole is the "
    "molar heat capacity. Statement II is false.",
    ["ΔT = q/C (I true)", "Per unit mass → specific heat; per mole → molar heat capacity (II false)"],
    answer="C", ncert=f"{REF4}, heat capacity", seconds=30)

mean_oh = (502 + 427) / 2
assert mean_oh == 464.5 and 502 + 427 == 929 and (502 - 427) / 2 == 37.5
add("Hess's law and enthalpies", I, "numerical",
    "The O–H bonds of a water molecule are broken one after the other:\n"
    "H₂O(g) → H(g) + OH(g); ΔH = 502 kJ mol⁻¹\nOH(g) → H(g) + O(g); ΔH = 427 kJ mol⁻¹\n"
    "The mean O–H bond enthalpy in water is:",
    Opts("B", "464.5 kJ mol⁻¹", ["929 kJ mol⁻¹", "427 kJ mol⁻¹", "37.5 kJ mol⁻¹"]),
    "Mean bond enthalpy in a polyatomic molecule",
    "The two O–H bonds need different energies to break, because the second bond is in OH, not H₂O. The mean "
    "(average) bond enthalpy is the total enthalpy of atomisation divided by the number of bonds broken.",
    ["Atomisation of H₂O: 502 + 427 = 929 kJ mol⁻¹", "Mean O–H bond enthalpy = 929/2 = 464.5 kJ mol⁻¹"],
    why="929 kJ mol⁻¹ is the total for both bonds. 427 kJ mol⁻¹ is only the second step. 37.5 kJ mol⁻¹ is half "
        "the difference between the steps.",
    ncert=f"{REF4}, bond enthalpy (mean bond enthalpy)", seconds=35, checked=True)

s_h2, s_o2, s_h2o = 130.7, 205.1, 69.9
ds = 2 * s_h2o - (2 * s_h2 + s_o2)
assert close(ds, -326.7) and close(s_h2o - s_h2 - s_o2, -265.9) and close(ds / 2, -163.35)
add("Entropy and Gibbs energy", I, "numerical",
    "The standard molar entropies at 298 K (J K⁻¹ mol⁻¹) are H₂(g) 130.7, O₂(g) 205.1 and H₂O(l) 69.9. The "
    "standard entropy change for the reaction 2H₂(g) + O₂(g) → 2H₂O(l) at 298 K is:",
    Opts("D", "−326.7 J K⁻¹", ["+326.7 J K⁻¹", "−265.9 J K⁻¹", "−163.4 J K⁻¹"]),
    "Standard entropy of reaction from molar entropies",
    "ΔrS° = Σ ν S°(products) − Σ ν S°(reactants), each multiplied by its stoichiometric coefficient. Two moles "
    "of gas and one more mole of gas become liquid, so ΔrS° is large and negative.",
    ["Σ S°(products) = 2 × 69.9 = 139.8", "Σ S°(reactants) = 2 × 130.7 + 205.1 = 466.5",
     "ΔrS° = 139.8 − 466.5 = −326.7 J K⁻¹"],
    why="+326.7 J K⁻¹ subtracts the wrong way. −265.9 J K⁻¹ ignores the coefficients. −163.4 J K⁻¹ is per mole "
        "of water, not for the reaction as written.",
    ncert=f"{REF4}, entropy and spontaneity", seconds=50, checked=True)

add("First law, work and enthalpy", I, "match_list",
    lists("One mole of an ideal gas expands isothermally and reversibly at temperature T from volume V to volume "
          "2V. Match List-I (quantity for this change) with List-II (its value).",
          ["Change in internal energy, ΔU", "Work done on the gas, w", "Heat absorbed by the gas, q",
           "Entropy change of the gas, ΔS"],
          ["2.303 RT log 2", "2.303 R log 2", "Zero", "−2.303 RT log 2"]),
    match("C", M("III IV I II"), [M("III I IV II"), M("IV III I II"), M("III IV II I")]),
    "First law and entropy for a reversible isothermal expansion of an ideal gas",
    "For an isothermal change of an ideal gas ΔU = 0. The reversible work is w = −2.303 nRT log(V_f/Vᵢ). "
    "From ΔU = q + w = 0, q = −w. Since the process is reversible, ΔS = q_rev/T.",
    ["A → III (ΔU = 0)", "B → IV (w = −2.303 RT log 2)", "C → I (q = −w = +2.303 RT log 2)",
     "D → II (ΔS = q_rev/T = 2.303 R log 2)"],
    why="The wrong codes swap the signs of q and w, or confuse q (an energy, containing T) with ΔS.",
    ncert=f"{REF4}, isothermal reversible expansion and entropy", seconds=60)

add("Hess's law and enthalpies", I, "statement_pair",
    sp("For sodium, Na(s) → Na(g), the enthalpy of atomisation is the same as the enthalpy of sublimation.",
       "The standard enthalpy of fusion of ice is negative."),
    SP_, "Atomisation, sublimation and fusion enthalpies",
    "Converting solid sodium into gaseous sodium atoms is both atomisation (the products are separate atoms) "
    "and sublimation (solid to vapour), so the two enthalpies are the same: Statement I is true. Melting "
    "needs heat; ΔfusH° of ice is +6.00 kJ mol⁻¹, so Statement II is false.",
    ["Na(s) → Na(g): atomisation = sublimation (I true)", "H₂O(s) → H₂O(l) absorbs heat: ΔfusH° > 0 (II false)"],
    answer="C", ncert=f"{REF4}, enthalpies of atomisation and phase transformation", seconds=35)

add("Entropy and Gibbs energy", I, "assertion_reason",
    ar("At 1 bar, ice melts spontaneously at 263 K (−10 °C).",
       "For melting, ΔH and ΔS are both positive, so melting is spontaneous only when TΔS exceeds ΔH, which at "
       "1 bar happens above 273 K."),
    AR_, "Temperature and the sign of ΔG",
    "Melting absorbs heat (ΔH > 0) and increases disorder (ΔS > 0). ΔG = ΔH − TΔS is negative only when "
    "T > ΔH/ΔS, which is 273 K at 1 bar. At 263 K, TΔS < ΔH, so ΔG > 0: ice does not melt (water freezes "
    "instead). A is false; R is true.",
    ["ΔH > 0, ΔS > 0 → spontaneous only for T > ΔH/ΔS = 273 K", "263 K < 273 K → ΔG > 0 → no melting (A false)",
     "R is a correct statement (R true)"],
    answer="D", ncert=f"{REF4}, Gibbs energy and spontaneity", seconds=40)

w_rev = 2.303 * 8.314 * 300 * math.log10(10 / 1)
p_ext = 0.08314 * 300 / 10
w_irr = p_ext * (10 - 1) * 100
assert close(w_rev, 5744, 0.001) and close(w_irr, 2245, 0.001)
assert close((w_rev - w_irr) / 1000, 3.50) and close((w_rev + w_irr) / 1000, 7.99)
add("First law, work and enthalpy", A, "numerical",
    "1 mol of an ideal gas at 300 K expands isothermally from 1 L to 10 L, (i) reversibly and (ii) in one step "
    "against a constant external pressure equal to its final pressure. The work done by the gas in (i) exceeds "
    "that in (ii) by about (R = 8.314 J K⁻¹ mol⁻¹ = 0.08314 L bar K⁻¹ mol⁻¹; 1 L bar = 100 J; log 10 = 1):",
    Opts("B", "3.50 kJ", ["5.74 kJ", "2.24 kJ", "7.99 kJ"]),
    "Reversible versus irreversible isothermal work",
    "Reversible work: |w| = 2.303 nRT log(V_f/Vᵢ). Irreversible work against constant p_ex: |w| = p_ex ΔV, where "
    "p_ex = final pressure = nRT/V_f. The reversible path always gives the larger work.",
    ["(i) |w| = 2.303 × 1 × 8.314 × 300 × log 10 = 5744 J",
     "(ii) p_ex = 0.08314 × 300 / 10 = 2.494 bar; |w| = 2.494 × 9 = 22.45 L bar = 2245 J",
     "Difference = 5744 − 2245 = 3499 J ≈ 3.50 kJ"],
    why="5.74 kJ is the reversible work alone and 2.24 kJ the irreversible work alone. 7.99 kJ adds them.",
    ncert=f"{REF4}, work in isothermal reversible and irreversible expansion", seconds=150, checked=True)

assert -1 == 2 - 3  # ethanol combustion: delta n(gas) = 2 - 3
add("First law, work and enthalpy", A, "statement_pair",
    sp("For the reaction C(graphite) + O₂(g) → CO₂(g), ΔH and ΔU are practically equal.",
       "For the combustion C₂H₅OH(l) + 3O₂(g) → 2CO₂(g) + 3H₂O(l) at 298 K, ΔH is less negative than ΔU."),
    SP_, "ΔH = ΔU + Δn_g RT",
    "Only gaseous species count in Δn_g; solids and liquids have negligible volumes. For the burning of "
    "graphite Δn_g = 1 − 1 = 0, so ΔH ≈ ΔU: Statement I is true. For ethanol Δn_g = 2 − 3 = −1, so "
    "ΔH = ΔU − RT: ΔH is more negative than ΔU, and Statement II is false.",
    ["Graphite: Δn_g = 0 → ΔH ≈ ΔU (I true)", "Ethanol: Δn_g = −1 → ΔH = ΔU − RT, more negative (II false)"],
    answer="C", ncert=f"{REF4}, enthalpy and the relation between ΔH and ΔU", seconds=50)

assert 1648e3 / 298 > 549.4  # NCERT data for 4Fe + 3O2 -> 2Fe2O3
add("Entropy and Gibbs energy", A, "assertion_reason",
    ar("Some exothermic reactions in which the entropy of the system decreases are nevertheless spontaneous.",
       "The heat given out raises the entropy of the surroundings by −ΔH/T, and when this increase is larger "
       "than the decrease in the entropy of the system, the total entropy change is positive."),
    AR_, "Total entropy change as the criterion of spontaneity",
    "For a spontaneous change, ΔS_total = ΔS_system + ΔS_surroundings > 0. An exothermic reaction transfers "
    "heat −ΔH to the surroundings, raising their entropy by −ΔH/T. For example, in the rusting of iron "
    "ΔS_system is about −549 J K⁻¹ but ΔS_surroundings is about +5530 J K⁻¹ at 298 K. R explains A.",
    ["ΔS_surr = −ΔH_sys/T > 0 for an exothermic reaction", "ΔS_total = ΔS_sys + ΔS_surr > 0 → spontaneous even "
     "if ΔS_sys < 0"],
    answer="A", ncert=f"{REF4}, entropy and spontaneity", seconds=50)

# ==================================================================== 5. Solutions
topic("Solutions")
REF5 = f"{C12}, 'Solutions'"

p_tot = 0.6 * 300 + 0.4 * 500
assert close(p_tot, 380) and close(0.4 * 300 + 0.6 * 500, 420) and (300 + 500) / 2 == 400
add("Raoult's law and ideal solutions", B, "numerical",
    "Liquids A and B form an ideal solution. At a certain temperature the vapour pressures of pure A and pure B "
    "are 300 mm Hg and 500 mm Hg respectively. The total vapour pressure of a solution in which the mole "
    "fraction of A is 0.6 is:",
    Opts("D", "380 mm Hg", ["420 mm Hg", "400 mm Hg", "800 mm Hg"]),
    "Raoult's law for a solution of two volatile liquids",
    "Each partial pressure is p = x p°, and the total pressure is their sum (Dalton's law).",
    ["p_A = 0.6 × 300 = 180 mm Hg", "p_B = 0.4 × 500 = 200 mm Hg", "p_total = 180 + 200 = 380 mm Hg"],
    why="420 mm Hg interchanges the mole fractions. 400 mm Hg is the simple average of p°A and p°B, true only "
        "for x_A = 0.5. 800 mm Hg adds the pure-liquid vapour pressures.",
    ncert=f"{REF5}, vapour pressure of liquid–liquid solutions", seconds=30, checked=True)

add("Colligative properties", B, "direct",
    "At a given temperature, a solution whose osmotic pressure is lower than that of another solution is said to "
    "be, with respect to the second solution:",
    Opts("C", "hypotonic", ["hypertonic", "isotonic", "an azeotrope"]),
    "Isotonic, hypertonic and hypotonic solutions",
    "Solutions with equal osmotic pressure are isotonic. Of two solutions, the one with the higher osmotic "
    "pressure (more concentrated in solute particles) is hypertonic and the one with the lower osmotic "
    "pressure is hypotonic.",
    ["Lower osmotic pressure → hypotonic", "Higher → hypertonic; equal → isotonic"],
    why="Hypertonic means a higher osmotic pressure, and isotonic an equal one. An azeotrope is a constant-boiling "
        "mixture of liquids, unrelated to osmosis.",
    ncert=f"{REF5}, osmosis and osmotic pressure (isotonic solutions)", seconds=20)

add("Concentration terms", B, "statement_pair",
    sp("Mass by volume percentage is commonly used in medicine and pharmacy.",
       "In a binary solution, the mole fractions of the two components add up to 1."),
    SP_, "Concentration terms",
    "NCERT notes that mass by volume percentage (mass of solute in 100 mL of solution) is commonly used in "
    "medicine and pharmacy. For a binary solution x₁ = n₁/(n₁ + n₂) and x₂ = n₂/(n₁ + n₂), so x₁ + x₂ = 1. "
    "Both statements are true.",
    ["w/V % is used in medicine and pharmacy (I true)", "x₁ + x₂ = (n₁ + n₂)/(n₁ + n₂) = 1 (II true)"],
    answer="A", ncert=f"{REF5}, expressing concentration of solutions", seconds=25)

m_eg = 3.72 / 1.86 * 62 * 1.0
assert close(m_eg, 124) and close(m_eg / 2, 62) and close(m_eg / 10, 12.4)
add("Colligative properties", I, "numerical",
    "What mass of ethylene glycol (molar mass 62 g mol⁻¹, a non-volatile non-electrolyte) must be added to "
    "1.0 kg of water so that the solution freezes at −3.72 °C? (K_f of water = 1.86 K kg mol⁻¹; freezing point "
    "of water = 0 °C)",
    Opts("D", "124 g", ["62 g", "248 g", "12.4 g"]),
    "Depression of freezing point: ΔT_f = K_f × m",
    "Find the molality needed from ΔT_f = K_f m, then the moles and mass of solute for 1.0 kg of water.",
    ["ΔT_f = 0 − (−3.72) = 3.72 K", "m = 3.72 / 1.86 = 2.0 mol kg⁻¹", "Mass = 2.0 mol × 62 g mol⁻¹ = 124 g"],
    why="62 g corresponds to only 1 mol kg⁻¹ (ΔT_f = 1.86 K). 248 g doubles the amount needed. 12.4 g has a "
        "power-of-ten slip.",
    ncert=f"{REF5}, depression of freezing point", seconds=45, checked=True)

add("Colligative properties", I, "assertion_reason",
    ar("A solution of a non-volatile solute boils at a higher temperature than the pure solvent at the same "
       "external pressure.",
       "The vapour pressure of the solution is lower than that of the pure solvent, so it becomes equal to the "
       "external pressure only at a higher temperature."),
    AR_, "Elevation of boiling point",
    "A liquid boils when its vapour pressure equals the external pressure. A non-volatile solute lowers the "
    "vapour pressure of the solvent, so the solution must be heated to a higher temperature before its "
    "vapour pressure reaches 1 atm. R explains A.",
    ["Boiling: vapour pressure = external pressure", "Solution has lower vapour pressure → needs higher T → "
     "T_b > T_b°"],
    answer="A", ncert=f"{REF5}, elevation of boiling point", seconds=35)

molal, molar = 0.1 / 0.400, 0.1 / 0.50
dtf, pi = 1.86 * molal, molar * 0.082 * 300
assert close(molal, 0.25) and close(molar, 0.20) and close(dtf, 0.465) and close(pi, 4.92)
add("Concentration terms", I, "match_list",
    lists("0.10 mol of a non-volatile non-electrolyte is dissolved in 400 g of water; the volume of the solution "
          "is 0.50 L. Match List-I (quantity) with List-II (its value). (K_f of water = 1.86 K kg mol⁻¹, "
          "R = 0.082 L atm K⁻¹ mol⁻¹, T = 300 K)",
          ["Molality", "Molarity", "Depression of freezing point", "Osmotic pressure at 300 K"],
          ["0.20 mol L⁻¹", "4.92 atm", "0.25 mol kg⁻¹", "0.465 K"]),
    match("B", M("III I IV II"), [M("I III IV II"), M("III I II IV"), M("I III II IV")]),
    "Molality, molarity and colligative properties",
    "Molality uses the mass of the solvent in kg; molarity uses the volume of the solution in L. ΔT_f uses "
    "molality, while osmotic pressure uses molarity (π = CRT).",
    ["Molality = 0.10 / 0.400 kg = 0.25 mol kg⁻¹ (A → III)", "Molarity = 0.10 / 0.50 L = 0.20 mol L⁻¹ (B → I)",
     "ΔT_f = 1.86 × 0.25 = 0.465 K (C → IV)", "π = 0.20 × 0.082 × 300 = 4.92 atm (D → II)"],
    why="The wrong codes swap molality and molarity (mass of solvent versus volume of solution), or swap the "
        "freezing-point depression and the osmotic pressure.",
    ncert=f"{REF5}, concentration terms and colligative properties", seconds=90)

add("van't Hoff factor", I, "statement_pair",
    sp("The molar mass of KCl found from the depression of the freezing point of its dilute aqueous solution is "
       "lower than its formula mass (74.5 g mol⁻¹).",
       "For a solute that dissociates in solution, the van't Hoff factor i is less than 1."),
    SP_, "Abnormal molar masses",
    "KCl dissociates into K⁺ and Cl⁻, so there are more particles than formula units and the observed ΔT_f is "
    "larger than expected. Molar mass ∝ 1/ΔT_f, so the calculated (abnormal) molar mass is lower than 74.5: "
    "Statement I is true. Dissociation gives i > 1 (i < 1 is for association): Statement II is false.",
    ["Dissociation → more particles → larger ΔT_f → lower apparent molar mass (I true)",
     "Dissociation → i > 1 (II false)"],
    answer="C", ncert=f"{REF5}, abnormal molar masses", seconds=40)

i_nacl = 58.5 / 32.5
alpha = i_nacl - 1
assert close(i_nacl, 1.8) and close(alpha, 0.8) and close(32.5 / 58.5, 0.556, 0.01) and close(i_nacl / 2, 0.9)
add("van't Hoff factor", A, "numerical",
    "The molar mass of NaCl calculated from the depression of the freezing point of its dilute aqueous solution "
    "is 32.5 g mol⁻¹. The degree of dissociation of NaCl in this solution is (Na = 23, Cl = 35.5):",
    Opts("C", "80%", ["20%", "55.6%", "90%"]),
    "van't Hoff factor from abnormal molar mass",
    "i = normal molar mass / abnormal (observed) molar mass. For NaCl ⇌ Na⁺ + Cl⁻, one formula unit gives "
    "two particles, so i = 1 + α.",
    ["Normal molar mass = 23 + 35.5 = 58.5 g mol⁻¹", "i = 58.5 / 32.5 = 1.8", "i = 1 + α → α = 0.8 = 80%"],
    why="20% is 1 − α. 55.6% is 32.5/58.5, the inverse of i. 90% divides i by 2 instead of using i = 1 + α.",
    ncert=f"{REF5}, abnormal molar masses and van't Hoff factor", seconds=75, checked=True)

add("Colligative properties", A, "multi_statement",
    ms("Which of the following statements about dilute solutions are correct? (Electrolytes are completely "
       "dissociated.)",
       ["A 0.1 m aqueous solution of K₂SO₄ freezes at a lower temperature than a 0.1 m aqueous solution of NaCl.",
        "Equimolal solutions of different non-volatile non-electrolytes in the same solvent show the same "
        "elevation of boiling point.",
        "The osmotic pressure of a given solution decreases as the temperature rises.",
        "The value of K_f depends on the nature of the solute.",
        "The lowering of vapour pressure (p° − p) caused by a given mole fraction of solute depends on the "
        "vapour pressure of the pure solvent."]),
    multi("D", {"a": True, "b": True, "c": False, "d": False, "e": True},
          ["(a), (b) and (c) only", "(b), (d) and (e) only", "(a), (b), (d) and (e) only"]),
    "Colligative properties: dependence on particles, solvent and temperature",
    "Colligative properties depend on the number of solute particles and on the solvent, not on the "
    "identity of the solute.",
    ["(a) True: i = 3 for K₂SO₄, 2 for NaCl → larger ΔT_f", "(b) True: same molality, same K_b → same ΔT_b",
     "(c) False: π = CRT increases with T", "(d) False: K_f is a property of the solvent",
     "(e) True: p° − p = x₂ p°"],
    why="Options containing (c) or (d) are wrong.",
    ncert=f"{REF5}, colligative properties", seconds=70)

urea_m = (6.0 / 60) / 0.250
nacl_m = urea_m / 2
m_nacl = nacl_m * 0.500 * 58.5
assert close(urea_m, 0.4) and close(m_nacl, 5.85) and close(2 * m_nacl, 11.7) and close(m_nacl / 2, 2.925) \
    and close(urea_m * 2 * 0.500 * 58.5, 23.4)
add("van't Hoff factor", A, "numerical",
    "What mass of NaCl must be dissolved in 500 g of water so that the solution has the same freezing point as a "
    "solution of 6.0 g of urea (molar mass 60 g mol⁻¹) in 250 g of water? Assume NaCl dissociates completely "
    "(Na = 23, Cl = 35.5).",
    Opts("B", "5.85 g", ["11.7 g", "2.93 g", "23.4 g"]),
    "Equal ΔT_f means equal effective molality, i × m",
    "The same solvent has the same K_f, so the two solutions freeze at the same temperature when i × m is the "
    "same. Urea is a non-electrolyte (i = 1); NaCl gives i = 2.",
    ["Urea: m = (6.0/60)/0.250 = 0.40 mol kg⁻¹; i m = 0.40",
     "NaCl: 2 × m = 0.40 → m = 0.20 mol kg⁻¹", "n(NaCl) = 0.20 × 0.500 = 0.10 mol → 0.10 × 58.5 = 5.85 g"],
    why="11.7 g ignores the dissociation of NaCl (i = 1). 2.93 g uses 250 g of water instead of 500 g. 23.4 g "
        "multiplies the molality by i instead of dividing by it.",
    ncert=f"{REF5}, van't Hoff factor and depression of freezing point", seconds=100, checked=True)

# ==================================================================== 6. Equilibrium
topic("Equilibrium")
REF6 = f"{C11}, 'Equilibrium'"

ph_new = -math.log10(1e-2 / 100)
assert close(ph_new, 4.0)
add("Acids, bases and pH", B, "numerical",
    "An aqueous solution of HCl has pH 2 at 298 K. It is diluted 100 times with water. The pH of the diluted "
    "solution is:",
    Opts("B", "4", ["3", "0", "2"]),
    "pH of a strong acid on dilution",
    "HCl is a strong acid, so [H₃O⁺] equals its concentration. Diluting 100 times lowers [H₃O⁺] 100 times, "
    "which raises the pH by log 100 = 2 units.",
    ["Initial [H₃O⁺] = 10⁻² M", "After dilution: 10⁻² / 100 = 10⁻⁴ M", "pH = 4"],
    why="3 corresponds to a 10-fold dilution. 0 subtracts 2 instead of adding it. 2 assumes pH does not change "
        "on dilution.",
    ncert=f"{REF6}, the pH scale", seconds=25, checked=True)

pkb = 14 - 4.74
assert close(pkb, 9.26) and close(14 + 4.74, 18.74) and close(4.74 / 2, 2.37)
add("Acids, bases and pH", B, "numerical",
    "The pK_a of acetic acid at 298 K is 4.74. The pK_b of its conjugate base, the acetate ion, at 298 K is "
    "(pK_w = 14.00):",
    Opts("C", "9.26", ["4.74", "18.74", "2.37"]),
    "K_a × K_b = K_w for a conjugate acid–base pair",
    "For a conjugate pair, K_a × K_b = K_w, so pK_a + pK_b = pK_w = 14 at 298 K.",
    ["pK_b = 14.00 − 4.74 = 9.26"],
    why="4.74 takes pK_b equal to pK_a. 18.74 adds instead of subtracting. 2.37 is half of pK_a.",
    ncert=f"{REF6}, relation between K_a and K_b", seconds=20, checked=True)

add("Physical equilibria and Henry's law", B, "direct",
    "Climbers at high altitudes may become weak and unable to think clearly, a condition called anoxia. This is "
    "because at high altitudes:",
    Opts("D", "the partial pressure of oxygen is low, so less oxygen dissolves in the blood",
         ["the partial pressure of nitrogen is high, so nitrogen bubbles form in the blood",
          "the partial pressure of oxygen is high, so too much oxygen dissolves in the blood",
          "the temperature is low, so no oxygen dissolves in the blood"]),
    "Henry's law: solubility of a gas ∝ its partial pressure",
    "By Henry's law the amount of a gas dissolved in a liquid is proportional to its partial pressure above the "
    "liquid. At high altitudes the partial pressure of oxygen is lower than at ground level, so the blood and "
    "tissues carry less oxygen, causing anoxia.",
    ["High altitude → low p(O₂)", "Henry's law → less O₂ dissolved in blood → anoxia"],
    why="Nitrogen bubbles in the blood (the bends) affect divers rising from high pressure, not climbers. The "
        "partial pressure of oxygen at altitude is lower, not higher. A low temperature would increase, not stop, "
        "the solubility of a gas.",
    ncert=f"{C12}, 'Solutions', Henry's law (applications)", seconds=25)

add("Kp, Kc and Le Chatelier", B, "statement_pair",
    sp("At equilibrium, the forward and backward reactions continue to take place at equal rates.",
       "A chemical equilibrium can be reached starting either from the reactants or from the products."),
    SP_, "Dynamic nature of equilibrium",
    "Chemical equilibrium is dynamic: both reactions go on, but at equal rates, so the composition does not "
    "change. NCERT notes that the same equilibrium can be reached whether one starts with the reactants (for "
    "example H₂ and I₂) or with the products (HI). Both statements are true.",
    ["Rate(forward) = rate(backward) ≠ 0 at equilibrium (I true)",
     "Same equilibrium from either side (II true)"],
    answer="A", ncert=f"{REF6}, equilibrium in chemical processes – dynamic equilibrium", seconds=25)

add("Kp, Kc and Le Chatelier", B, "direct",
    "For the equilibrium H₂(g) + I₂(g) ⇌ 2HI(g) in a closed vessel at constant temperature, the effect of "
    "increasing the total pressure by compressing the mixture is:",
    Opts("B", "no change in the equilibrium amounts of H₂, I₂ and HI",
         ["the equilibrium shifts towards HI", "the equilibrium shifts towards H₂ and I₂",
          "the equilibrium constant K_c increases"]),
    "Effect of pressure when Δn(gas) = 0",
    "Pressure changes affect only equilibria in which the number of moles of gas changes. Here 2 mol of gas "
    "gives 2 mol of gas (Δn = 0), so compression changes all concentrations by the same factor and Q_c stays "
    "equal to K_c: there is no shift.",
    ["Δn(gas) = 2 − 2 = 0", "Q_c = [HI]²/([H₂][I₂]) unchanged by compression → no shift"],
    why="A shift towards either side would need a change in the number of gas moles. K_c depends only on "
        "temperature.",
    ncert=f"{REF6}, effect of pressure change", seconds=30)

x_gas = 1.0 / 50e3
n_gas = x_gas * (1000 / 18)
assert close(x_gas, 2e-5) and close(n_gas * 1000, 1.11, 0.01) and close((1.0 / 50) * 1000 / 18, 1.11, 0.01)
add("Physical equilibria and Henry's law", I, "numerical",
    "The Henry's law constant of a gas in water at 298 K is K_H = 50 kbar. The amount of the gas that dissolves "
    "in 1.0 L of water (1000 g) when its partial pressure above the water is 1.0 bar is about (H₂O = 18 g mol⁻¹; "
    "the solution is very dilute):",
    Opts("C", "1.11 mmol", ["1.11 mol", "20 mmol", "0.111 mmol"]),
    "Henry's law: p = K_H × x",
    "Find the mole fraction of the gas from x = p/K_H, using the same pressure unit. In a very dilute solution "
    "x ≈ n(gas)/n(water), so n(gas) = x × n(water).",
    ["K_H = 50 kbar = 5.0 × 10⁴ bar", "x = 1.0 / 5.0 × 10⁴ = 2.0 × 10⁻⁵",
     "n(water) = 1000/18 = 55.6 mol", "n(gas) = 2.0 × 10⁻⁵ × 55.6 = 1.11 × 10⁻³ mol = 1.11 mmol"],
    why="1.11 mol forgets to convert kbar to bar. 20 mmol multiplies x by the mass of water (1000 g) instead of "
        "its moles. 0.111 mmol has a power-of-ten slip.",
    ncert=f"{C12}, 'Solutions', Henry's law", seconds=70, checked=True)

ka = 0.05 * 0.02 ** 2
assert close(ka, 2e-5) and close(0.05 * 0.02, 1e-3) and close(0.02 ** 2, 4e-4) and close(0.05 * 2e-4 ** 2, 2e-9)
add("Acids, bases and pH", I, "numerical",
    "A 0.05 M aqueous solution of a weak monobasic acid HA is 2% ionised at 298 K. Taking K_a ≈ cα², the "
    "ionisation constant of the acid is:",
    Opts("D", "2.0 × 10⁻⁵", ["1.0 × 10⁻³", "4.0 × 10⁻⁴", "2.0 × 10⁻⁹"]),
    "Ionisation constant from the degree of ionisation",
    "For HA ⇌ H⁺ + A⁻ with initial concentration c and degree of ionisation α, K_a = cα²/(1 − α) ≈ cα² for small "
    "α.",
    ["α = 2% = 0.02", "K_a ≈ cα² = 0.05 × (0.02)² = 0.05 × 4 × 10⁻⁴ = 2.0 × 10⁻⁵"],
    why="1.0 × 10⁻³ is cα, the H⁺ concentration. 4.0 × 10⁻⁴ is α² alone. 2.0 × 10⁻⁹ takes α as 0.02%, not 2%.",
    ncert=f"{REF6}, ionization constants of weak acids", seconds=40, checked=True)

pn2, ph2, pnh3 = 0.2 * 10, 0.6 * 10, 0.2 * 10
kp = pnh3 ** 2 / (pn2 * ph2 ** 3)
assert close(kp, 9.26e-3) and close(0.2 ** 2 / (0.2 * 0.6 ** 3), 0.926) and close(pnh3 / (pn2 * ph2), 0.167, 0.01)
assert close(1 / kp, 108)
add("Kp, Kc and Le Chatelier", I, "numerical",
    "In an equilibrium mixture for N₂(g) + 3H₂(g) ⇌ 2NH₃(g) at a total pressure of 10 atm, the mole fractions "
    "of N₂, H₂ and NH₃ are 0.2, 0.6 and 0.2 respectively. K_p for the reaction at this temperature is:",
    Opts("B", "9.26 × 10⁻³ atm⁻²", ["0.926 atm⁻²", "0.167 atm⁻²", "108 atm²"]),
    "K_p from partial pressures (p = x × P)",
    "Convert each mole fraction into a partial pressure by multiplying by the total pressure, then use "
    "K_p = p(NH₃)² / [p(N₂) × p(H₂)³].",
    ["p(N₂) = 2 atm, p(H₂) = 6 atm, p(NH₃) = 2 atm", "K_p = 2² / (2 × 6³) = 4/432 = 9.26 × 10⁻³ atm⁻²"],
    why="0.926 atm⁻² uses the mole fractions as if they were pressures. 0.167 atm⁻² ignores the powers from the "
        "coefficients. 108 atm² is the constant for the reverse reaction.",
    ncert=f"{REF6}, equilibrium constant in gaseous systems", seconds=70, checked=True)

add("Kp, Kc and Le Chatelier", I, "match_list",
    lists("Match List-I (condition) with List-II (what it tells us about the reaction mixture).",
          ["K_c > 10³", "K_c < 10⁻³", "K_c between 10⁻³ and 10³", "Q_c > K_c"],
          ["The net reaction proceeds in the reverse direction", "Products predominate over reactants at "
           "equilibrium", "Appreciable concentrations of both reactants and products are present at equilibrium",
           "Reactants predominate over products at equilibrium"]),
    match("C", M("II IV III I"), [M("IV II III I"), M("II IV I III"), M("III IV II I")]),
    "Applications of the equilibrium constant",
    "A large K_c means the reaction goes nearly to completion; a very small K_c means it hardly proceeds; "
    "intermediate values mean appreciable amounts of both. Comparing Q_c with K_c predicts the direction: if "
    "Q_c > K_c there are too many products, so the reaction goes backwards.",
    ["A → II", "B → IV", "C → III", "D → I"],
    why="The wrong codes interchange the meanings of large and small K_c, or give Q_c > K_c the forward "
        "direction.",
    ncert=f"{REF6}, applications of equilibrium constants", seconds=40)

add("Hydrolysis and buffers", I, "assertion_reason",
    ar("An aqueous solution of potassium cyanide, KCN, is basic.",
       "The cyanide ion reacts with water to form the weak acid HCN and hydroxide ions: "
       "CN⁻ + H₂O ⇌ HCN + OH⁻."),
    AR_, "Hydrolysis of the salt of a weak acid and a strong base",
    "KCN is the salt of the weak acid HCN and the strong base KOH. K⁺ does not hydrolyse, but CN⁻ takes a "
    "proton from water to form weakly ionised HCN, leaving excess OH⁻ ions, so pH > 7. R explains A.",
    ["K⁺: no hydrolysis", "CN⁻ + H₂O ⇌ HCN + OH⁻ → [OH⁻] > [H₃O⁺] → basic"],
    answer="A", ncert=f"{REF6}, hydrolysis of salts", seconds=35)

add("Kp, Kc and Le Chatelier", I, "multi_statement",
    ms("For the equilibrium 2SO₂(g) + O₂(g) ⇌ 2SO₃(g), ΔH < 0, set up in a closed vessel, which of the "
       "following statements are correct?",
       ["K_p = K_c(RT)⁻¹.", "Raising the temperature increases the equilibrium constant.",
        "Adding a catalyst increases the amount of SO₃ at equilibrium.",
        "Removing some SO₃ from the mixture shifts the equilibrium in the forward direction.",
        "The unit of K_c is L mol⁻¹."]),
    multi("D", {"a": True, "b": False, "c": False, "d": True, "e": True},
          ["(a), (b) and (d) only", "(c), (d) and (e) only", "(a) and (e) only"]),
    "K_p–K_c relation and Le Chatelier's principle",
    "Δn(gas) = 2 − 3 = −1, so K_p = K_c(RT)⁻¹ and K_c has the unit (mol L⁻¹)⁻¹ = L mol⁻¹. For an exothermic "
    "reaction, K decreases as the temperature rises. A catalyst only speeds up the attainment of equilibrium. "
    "Removing a product makes Q_c < K_c, so more product forms.",
    ["(a) True: Δn = −1", "(b) False: exothermic → K falls with rising T", "(c) False: catalyst does not shift "
     "equilibrium", "(d) True", "(e) True"],
    why="Options containing (b) or (c) are wrong; (a) and (e) only leaves out (d).",
    ncert=f"{REF6}, factors affecting equilibria", seconds=60)

oh = 10 ** -(14 - 11)
s_oh = 4.0e-12 / oh ** 2
assert close(oh, 1e-3) and close(s_oh, 4e-6) and close(4.0e-12 / oh, 4e-9) and close((4.0e-12 / 4) ** (1 / 3), 1e-4)
assert close(4.0e-12 / (2 * oh) ** 2, 1e-6)
add("Solubility product", A, "numerical",
    "The solubility product of a sparingly soluble hydroxide M(OH)₂ is 4.0 × 10⁻¹² at 298 K. Its molar "
    "solubility in a buffer solution of pH 11.0 at 298 K is (pK_w = 14):",
    Opts("B", "4.0 × 10⁻⁶ M", ["4.0 × 10⁻⁹ M", "1.0 × 10⁻⁴ M", "1.0 × 10⁻⁶ M"]),
    "Solubility in the presence of a common ion fixed by the pH",
    "The buffer fixes [OH⁻]. Since K_sp = [M²⁺][OH⁻]² and the dissolved salt adds negligible OH⁻, the "
    "solubility is s = [M²⁺] = K_sp/[OH⁻]².",
    ["pOH = 14 − 11 = 3 → [OH⁻] = 1.0 × 10⁻³ M", "s = 4.0 × 10⁻¹² / (1.0 × 10⁻³)² = 4.0 × 10⁻⁶ M"],
    why="4.0 × 10⁻⁹ M does not square [OH⁻]. 1.0 × 10⁻⁴ M is the solubility in pure water (K_sp = 4s³). "
        "1.0 × 10⁻⁶ M doubles [OH⁻] before squaring, but the buffer fixes [OH⁻] at 10⁻³ M.",
    ncert=f"{REF6}, common ion effect in the ionization of salts", seconds=90, checked=True)

ka_w = 0.1 * 0.01 ** 2
alpha_new = math.sqrt(ka_w / 0.001)
assert close(alpha_new, 0.10)
add("Acids, bases and pH", A, "numerical",
    "A 0.1 M solution of a weak monobasic acid is 1% ionised at 298 K. The solution is diluted to 0.001 M at the "
    "same temperature. Using α ≈ √(K_a/c), the degree of ionisation becomes:",
    Opts("C", "10%", ["100%", "0.1%", "1%"]),
    "Effect of dilution on the degree of ionisation",
    "K_a is constant at a fixed temperature. From K_a ≈ cα², α ∝ 1/√c: a 100-fold dilution increases α "
    "√100 = 10 times.",
    ["K_a ≈ cα² = 0.1 × (0.01)² = 1 × 10⁻⁵", "New α = √(1 × 10⁻⁵ / 0.001) = √0.01 = 0.10 = 10%"],
    why="100% makes α proportional to the dilution itself. 0.1% has dilution decreasing ionisation. 1% treats "
        "α, rather than K_a, as constant.",
    ncert=f"{REF6}, ionization of weak acids and degree of ionisation", seconds=70, checked=True)

add("Solubility product", A, "statement_pair",
    sp("Of two sparingly soluble salts of the same formula type (for example, both AB), the one with the smaller "
       "K_sp is the less soluble in water.",
       "At a given temperature, the molar solubility of AgCl in 0.1 M AgNO₃ is the same as in 0.1 M NaCl."),
    SP_, "Comparing solubilities; common ion effect",
    "For salts of the same type, s is the same function of K_sp (s = √K_sp for AB), so a smaller K_sp means a "
    "smaller solubility: Statement I is true. In 0.1 M AgNO₃ the common ion is Ag⁺ at 0.1 M and in 0.1 M NaCl "
    "it is Cl⁻ at 0.1 M; in both cases s = K_sp/0.1, so the solubilities are equal: Statement II is true.",
    ["Same type: s = √K_sp → smaller K_sp, smaller s (I true)",
     "AgNO₃: s = K_sp/[Ag⁺] = K_sp/0.1; NaCl: s = K_sp/[Cl⁻] = K_sp/0.1 (II true)"],
    answer="A", ncert=f"{REF6}, solubility product and common ion effect", seconds=50)

rt = 0.0831 * 300
assert rt > 1 and close(rt, 24.9, 0.01)
add("Kp, Kc and Le Chatelier", A, "assertion_reason",
    ar("For N₂O₄(g) ⇌ 2NO₂(g) at 300 K, the numerical value of K_p (pressures in bar) is greater than that of "
       "K_c (concentrations in mol L⁻¹).",
       "K_p = K_c(RT)^Δn, where Δn = +1 here, and RT at 300 K is about 24.9 L bar mol⁻¹, which is greater than 1."),
    AR_, "Relation between K_p and K_c",
    "From pV = nRT, p = cRT, so K_p = K_c(RT)^Δn, where Δn = moles of gaseous products − moles of gaseous "
    "reactants = 2 − 1 = +1. With R = 0.0831 L bar K⁻¹ mol⁻¹, RT = 24.9 at 300 K, so K_p = 24.9 K_c > K_c. "
    "R explains A.",
    ["Δn = 2 − 1 = +1", "RT = 0.0831 × 300 = 24.9", "K_p = 24.9 K_c → K_p > K_c"],
    answer="A", ncert=f"{REF6}, relationship between K_p and K_c", seconds=50)

add("Hydrolysis and buffers", A, "match_list",
    lists("Equal volumes of the two solutions named in List-I are mixed at 298 K. Match List-I with List-II "
          "(nature of the resulting solution).",
          ["0.1 M CH₃COOH and 0.1 M NaOH", "0.1 M HCl and 0.1 M NH₄OH", "0.1 M HCl and 0.1 M NaOH",
           "0.2 M CH₃COOH and 0.1 M NaOH"],
          ["pH = 7", "pH > 7, due to hydrolysis of the anion of the salt formed",
           "pH < 7, due to hydrolysis of the cation of the salt formed",
           "Acidic buffer with pH = pK_a of CH₃COOH"]),
    match("D", M("II III I IV"), [M("III II I IV"), M("II III IV I"), M("IV III I II")]),
    "Neutralisation products, salt hydrolysis and buffers",
    "Equimolar neutralisation gives just the salt: a strong acid–strong base salt (NaCl) is neutral, a weak "
    "acid–strong base salt (CH₃COONa) is basic and a strong acid–weak base salt (NH₄Cl) is acidic. When the "
    "weak acid is in excess, half of it is converted to its salt and an acidic buffer with [salt] = [acid] "
    "results, so pH = pK_a.",
    ["A → II (CH₃COONa: CH₃COO⁻ hydrolyses)", "B → III (NH₄Cl: NH₄⁺ hydrolyses)", "C → I (NaCl)",
     "D → IV (0.1 M CH₃COOH left, 0.1 M CH₃COONa formed → pH = pK_a)"],
    why="The wrong codes reverse the hydrolysis of anions and cations, or treat the equimolar mixtures as "
        "buffers.",
    ncert=f"{REF6}, hydrolysis of salts and buffer solutions", seconds=80)

# ==================================================================== 7. Redox Reactions and Electrochemistry
topic("Redox Reactions and Electrochemistry")
REF7A = f"{C11}, 'Redox Reactions'"
REF7B = f"{C12}, 'Electrochemistry'"

x_c = F(-(22 * 1 + 11 * (-2)), 12)
assert x_c == 0
add("Oxidation number and balancing", B, "numerical",
    "The average oxidation number of carbon in sucrose, C₁₂H₂₂O₁₁, is:",
    Opts("B", "0", ["+1", "−1", "+4"]),
    "Oxidation number from the rule that the sum is zero for a neutral molecule",
    "Take H as +1 and O as −2. For a neutral molecule the oxidation numbers add up to zero.",
    ["12x + 22(+1) + 11(−2) = 0", "12x + 22 − 22 = 0 → x = 0"],
    why="+4 is the oxidation number of C in CO₂, not in sucrose. +1 and −1 come from arithmetic slips with the "
        "22 H and 11 O atoms.",
    ncert=f"{REF7A}, oxidation number", seconds=30, checked=True)

lam = 150 - 100 * math.sqrt(0.01)
assert close(lam, 140) and close(150 - 100 * 0.01, 149) and close(150 + 100 * 0.1, 160) and 150 - 100 == 50
add("Conductance and Kohlrausch's law", B, "numerical",
    "For a strong electrolyte in water at 298 K, Λm = Λ°m − A√c, with Λ°m = 150 S cm² mol⁻¹ and "
    "A = 100 S cm² mol⁻¹ (mol L⁻¹)^(−1/2). Its molar conductivity at c = 0.01 mol L⁻¹ is:",
    Opts("D", "140 S cm² mol⁻¹", ["149 S cm² mol⁻¹", "160 S cm² mol⁻¹", "50 S cm² mol⁻¹"]),
    "Variation of molar conductivity of a strong electrolyte with concentration",
    "For strong electrolytes Λm decreases linearly with √c. Substitute √0.01 = 0.1.",
    ["√c = √0.01 = 0.1", "Λm = 150 − 100 × 0.1 = 140 S cm² mol⁻¹"],
    why="149 uses c instead of √c. 160 adds the correction instead of subtracting it. 50 leaves out √c "
        "altogether.",
    ncert=f"{REF7B}, variation of conductivity and molar conductivity with concentration", seconds=30,
    checked=True)

add("Batteries and fuel cells", B, "direct",
    "Which of the following is a characteristic feature of a fuel cell such as the hydrogen–oxygen fuel cell?",
    Opts("C", "The reactants are fed in continuously and the products are removed continuously",
         ["It must be recharged by passing a current through it in the reverse direction",
          "It converts heat from burning the fuel into electricity through a turbine",
          "Its electrolyte is a moist paste of ammonium chloride and zinc chloride"]),
    "Fuel cells",
    "Fuel cells are galvanic cells designed to convert the energy of combustion of fuels such as hydrogen, "
    "methane or methanol directly into electrical energy. The reactants are supplied continuously and the "
    "products removed continuously, so the cell keeps working as long as fuel is supplied.",
    ["Fuel cell = galvanic cell with continuous supply of reactants",
     "Chemical energy → electrical energy directly"],
    why="Recharging describes a secondary battery such as the lead storage battery. The conversion is direct, "
        "not through heat and a turbine. The NH₄Cl–ZnCl₂ paste is the electrolyte of the dry cell.",
    ncert=f"{REF7B}, fuel cells", seconds=25)

add("Electrode potential and cells", B, "statement_pair",
    sp("A negative standard reduction potential means that the redox couple is a stronger reducing agent than the "
       "H⁺/H₂ couple.",
       "Among the common half-cells, F₂/F⁻ has the highest standard reduction potential, so fluorine gas is the "
       "strongest oxidising agent."),
    SP_, "Meaning of standard electrode potentials",
    "NCERT: a negative E° means the couple is a stronger reducing agent than H⁺/H₂, and a positive E° means it "
    "is a weaker one. Statement I is true. E°(F₂/F⁻) = +2.87 V is the highest in the table, so F₂ is reduced "
    "most readily and is the strongest oxidising agent. Statement II is true.",
    ["E° < 0 → stronger reductant than H₂ (I true)", "E°(F₂/F⁻) = +2.87 V, highest → strongest oxidant (II true)"],
    answer="A", ncert=f"{REF7B}, measurement of electrode potential (electrochemical series)", seconds=35)

e_conc = -(0.059 / 2) * math.log10(0.001 / 0.1)
assert close(e_conc, 0.059) and close(2 * e_conc, 0.118) and close(e_conc / 2, 0.0295)
add("Nernst equation and Gibbs energy", I, "numerical",
    "The emf of the concentration cell Cu(s) | Cu²⁺(0.001 M) || Cu²⁺(0.1 M) | Cu(s) at 298 K is "
    "(2.303RT/F = 0.059 V):",
    Opts("B", "0.059 V", ["0.118 V", "0.0295 V", "0 V"]),
    "Nernst equation for a concentration cell",
    "Both electrodes are the same, so E°cell = 0. The cell reaction is Cu²⁺(0.1 M) → Cu²⁺(0.001 M) with n = 2; "
    "E = E° − (0.059/n) log([Cu²⁺]anode/[Cu²⁺]cathode).",
    ["E = 0 − (0.059/2) log(0.001/0.1)", "= −0.0295 × (−2) = +0.059 V"],
    why="0.118 V uses n = 1. 0.0295 V takes log(0.1/0.001) as 1. 0 V uses only E°cell and ignores the "
        "concentration difference.",
    ncert=f"{REF7B}, Nernst equation", seconds=60, checked=True)

e_fc = 474e3 / (4 * 96500)
assert close(e_fc, 1.228, 0.001) and close(2 * e_fc, 2.456, 0.001) and close(e_fc / 2, 0.614, 0.001)
add("Batteries and fuel cells", I, "numerical",
    "For the reaction taking place in the hydrogen–oxygen fuel cell, 2H₂(g) + O₂(g) → 2H₂O(l), "
    "ΔrG° = −474 kJ mol⁻¹ at 298 K. Four electrons are transferred in this reaction as written. The standard emf "
    "of the cell is (F = 96 500 C mol⁻¹):",
    Opts("D", "1.23 V", ["2.46 V", "4.91 V", "0.614 V"]),
    "ΔrG° = −nFE°cell",
    "Rearrange ΔrG° = −nFE° to E° = −ΔrG°/(nF), with ΔrG° in joules and n = 4 for the reaction as written.",
    ["E° = 474 000 / (4 × 96 500)", "E° = 474 000 / 386 000 = 1.23 V"],
    why="2.46 V uses n = 2 and 4.91 V uses n = 1. 0.614 V uses n = 8.",
    ncert=f"{REF7B}, cell potential and Gibbs energy; fuel cells", seconds=50, checked=True)

add("Oxidation number and balancing", I, "assertion_reason",
    ar("Hydrogen peroxide can act both as an oxidising agent and as a reducing agent.",
       "The oxidation number of oxygen in H₂O₂ is −1, which lies between its oxidation numbers in H₂O (−2) and "
       "in O₂ (0)."),
    AR_, "Intermediate oxidation state and dual redox behaviour",
    "An element in an intermediate oxidation state can be reduced (here to −2, giving H₂O) or oxidised (to 0, "
    "giving O₂). So H₂O₂ is an oxidant when its O is reduced and a reductant when its O is oxidised. R explains A.",
    ["O in H₂O₂: −1", "Reduced to −2 (H₂O) → acts as oxidant", "Oxidised to 0 (O₂) → acts as reductant"],
    answer="A", ncert=f"{REF7A}, oxidation number and types of redox reactions", seconds=35)

add("Batteries and fuel cells", I, "multi_statement",
    ms("Which of the following statements about commercial cells are correct?",
       ["In the dry (Leclanché) cell, the cathode is a carbon (graphite) rod surrounded by powdered manganese "
        "dioxide and carbon.",
        "The dry cell has a potential of nearly 1.5 V.",
        "Water is consumed in the lead storage battery during discharge.",
        "In the dry cell, the ammonia formed at the cathode combines with Zn²⁺ to form [Zn(NH₃)₄]²⁺.",
        "The lead storage battery is a primary battery."]),
    multi("C", {"a": True, "b": True, "c": False, "d": True, "e": False},
          ["(a), (b), (c) and (d) only", "(b), (d) and (e) only", "(a) and (d) only"]),
    "Dry cell and lead storage battery",
    "In the dry cell the zinc container is the anode and a graphite rod in MnO₂ and carbon is the cathode; the "
    "cell gives about 1.5 V, and the NH₃ produced at the cathode complexes the Zn²⁺. In the lead storage "
    "battery, discharge consumes H₂SO₄ and produces water: Pb + PbO₂ + 2H₂SO₄ → 2PbSO₄ + 2H₂O. It can be "
    "recharged, so it is a secondary battery.",
    ["(a) True", "(b) True", "(c) False: water is formed, sulphuric acid is consumed", "(d) True",
     "(e) False: it is a secondary (rechargeable) battery"],
    why="Options containing (c) or (e) are wrong; (a) and (d) only leaves out (b).",
    ncert=f"{REF7B}, batteries", seconds=55)

add("Conductance and Kohlrausch's law", I, "match_list",
    lists("Match List-I (quantity, at a fixed temperature) with List-II (how it changes when the solution is "
          "diluted).",
          ["Conductivity (κ) of aqueous KCl", "Molar conductivity (Λm) of aqueous KCl",
           "Molar conductivity (Λm) of aqueous CH₃COOH", "Limiting molar conductivity (Λ°m) of KCl"],
          ["Increases steeply, especially at low concentrations", "Decreases",
           "Increases slowly and almost linearly with decrease in √c",
           "Does not change; it is the value Λm approaches at zero concentration"]),
    match("B", M("II III I IV"), [M("III II I IV"), M("II I III IV"), M("IV III I II")]),
    "Variation of conductivity and molar conductivity with concentration",
    "On dilution the number of ions per unit volume falls, so κ decreases. Λm (= κ/c) increases: only slightly "
    "for a strong electrolyte, but steeply for a weak electrolyte, whose degree of dissociation increases a "
    "great deal on dilution. Λ°m is the limiting value at zero concentration, a constant at a given temperature.",
    ["A → II", "B → III", "C → I", "D → IV"],
    why="The wrong codes give conductivity the behaviour of molar conductivity, or interchange the strong and "
        "weak electrolytes.",
    ncert=f"{REF7B}, variation of conductivity and molar conductivity with concentration", seconds=50)

e_mn = 1.51 - (0.059 / 5) * math.log10(1 / (1e-2) ** 8)
assert close(e_mn, 1.321, 0.001) and close(1.51 + (0.059 / 5) * 16, 1.699, 0.001)
assert close(1.51 - (0.059 / 5) * 2, 1.486, 0.001) and close(1.51 - 0.059 * 16, 0.566, 0.001)
add("Nernst equation and Gibbs energy", A, "numerical",
    "For the half-reaction MnO₄⁻(aq) + 8H⁺(aq) + 5e⁻ → Mn²⁺(aq) + 4H₂O(l), E° = +1.51 V. The reduction potential "
    "at 298 K in a solution of pH 2 in which [MnO₄⁻] = [Mn²⁺] = 1 M is (2.303RT/F = 0.059 V):",
    Opts("D", "1.32 V", ["1.70 V", "1.49 V", "0.57 V"]),
    "Nernst equation for a half-reaction involving H⁺ ions",
    "E = E° − (0.059/n) log([Mn²⁺]/([MnO₄⁻][H⁺]⁸)), with n = 5. At pH 2, [H⁺] = 10⁻² M, so [H⁺]⁸ = 10⁻¹⁶ "
    "and the log term is 16. Less acid makes permanganate a weaker oxidant.",
    ["[H⁺] = 10⁻² M → [H⁺]⁸ = 10⁻¹⁶", "E = 1.51 − (0.059/5) × log(1/10⁻¹⁶) = 1.51 − 0.0118 × 16",
     "E = 1.51 − 0.189 = 1.32 V"],
    why="1.70 V adds the correction (sign error). 1.49 V ignores the power 8 on [H⁺]. 0.57 V uses n = 1.",
    ncert=f"{REF7B}, Nernst equation", seconds=110, checked=True)

# Gibbs energies are additive: 3 E(Fe3+/Fe) = 1(0.77) + 2(-0.44)
assert close((2 * -0.44 + 0.77) / 3, -0.0367, 0.01) and close(0.77 - 0.44, 0.33)
assert close(4.74e5 / 96500, 4.91, 0.002)
add("Electrode potential and cells", A, "assertion_reason",
    ar("The standard potential of the Fe³⁺/Fe couple cannot be obtained simply by adding E°(Fe³⁺/Fe²⁺) and "
       "E°(Fe²⁺/Fe).",
       "E° is an intensive property that does not depend on the number of electrons, whereas ΔG° = −nFE° is "
       "extensive and additive, so the half-reactions must be combined through their ΔG° values."),
    AR_, "Combining standard electrode potentials",
    "When two half-reactions are added to give a third half-reaction, the electrons do not cancel, and the "
    "potentials are not additive. The Gibbs energies are: −3F E°(Fe³⁺/Fe) = −1F(+0.77) − 2F(−0.44), giving "
    "E°(Fe³⁺/Fe) = (0.77 − 0.88)/3 = −0.037 V, not 0.77 − 0.44 = 0.33 V. R explains A.",
    ["Fe³⁺ + e⁻ → Fe²⁺: ΔG°₁ = −1F(0.77)", "Fe²⁺ + 2e⁻ → Fe: ΔG°₂ = −2F(−0.44)",
     "Fe³⁺ + 3e⁻ → Fe: ΔG° = ΔG°₁ + ΔG°₂ → E° = −0.037 V"],
    answer="A", ncert=f"{REF7B}, electrochemical cells and Gibbs energy of reaction", seconds=60)

add("Conductance and Kohlrausch's law", A, "statement_pair",
    sp("The limiting molar conductivity of acetic acid can be obtained from the Λ°m values of HCl, NaCl and "
       "CH₃COONa.",
       "At infinite dilution, the limiting molar conductivity of each ion in a solution does not depend on the "
       "other ion present."),
    SP_, "Kohlrausch's law of independent migration of ions",
    "Kohlrausch's law states that Λ°m of an electrolyte is the sum of the independent contributions of its "
    "ions (Statement II true). Hence Λ°(CH₃COOH) = Λ°(CH₃COONa) + Λ°(HCl) − Λ°(NaCl), a combination in which "
    "the Na⁺ and Cl⁻ contributions cancel (Statement I true). This is how Λ°m of weak electrolytes, which "
    "cannot be found by extrapolation, is obtained.",
    ["Λ°(CH₃COOH) = λ°(H⁺) + λ°(CH₃COO⁻) = Λ°(HCl) + Λ°(CH₃COONa) − Λ°(NaCl) (I true)",
     "Independent migration of ions (II true)"],
    answer="A", ncert=f"{REF7B}, applications of Kohlrausch's law", seconds=45)

add("Oxidation number and balancing", A, "direct",
    "Which of the following species can act ONLY as an oxidising agent in redox reactions?",
    Opts("C", "MnO₄⁻", ["NO₂⁻", "SO₃²⁻", "Fe²⁺"]),
    "Highest, lowest and intermediate oxidation states",
    "A species whose key element is in its highest possible oxidation state can only gain electrons (be "
    "reduced), so it can act only as an oxidising agent. In MnO₄⁻, manganese is +7, the highest oxidation state "
    "of manganese (all seven 3d and 4s electrons used).",
    ["MnO₄⁻: Mn +7 (maximum) → only oxidant", "NO₂⁻: N +3 (between −3 and +5) → both",
     "SO₃²⁻: S +4 (between −2 and +6) → both", "Fe²⁺: +2 (between 0 and +3) → both"],
    why="Nitrogen in NO₂⁻, sulphur in SO₃²⁻ and iron in Fe²⁺ are in intermediate oxidation states, so these "
        "species can be oxidised as well as reduced.",
    ncert=f"{REF7A}, oxidation number and redox reactions", seconds=50)

# ==================================================================== 8. Chemical Kinetics
topic("Chemical Kinetics")
REF8 = f"{C12}, 'Chemical Kinetics'"

r_avg = 0.5 * (0.50 - 0.30) / 10
assert close(r_avg, 0.01) and close(2 * r_avg, 0.02) and close(4 * r_avg, 0.04) and close(0.30 / 10, 0.03)
add("Rate law and order", B, "numerical",
    "For the reaction 2A → B, the concentration of A falls from 0.50 mol L⁻¹ to 0.30 mol L⁻¹ in 10 s. The average "
    "rate of the reaction, −½ Δ[A]/Δt, over this interval is:",
    Opts("B", "0.01 mol L⁻¹ s⁻¹", ["0.02 mol L⁻¹ s⁻¹", "0.04 mol L⁻¹ s⁻¹", "0.03 mol L⁻¹ s⁻¹"]),
    "Average rate and stoichiometric coefficients",
    "To get a single rate for the reaction, the rate of change of each concentration is divided by its "
    "stoichiometric coefficient. A has coefficient 2.",
    ["Δ[A] = 0.30 − 0.50 = −0.20 mol L⁻¹", "Rate = −½ × (−0.20)/10 = 0.01 mol L⁻¹ s⁻¹"],
    why="0.02 is the rate of disappearance of A, without dividing by 2. 0.04 multiplies by 2 instead. 0.03 "
        "divides the final concentration by the time.",
    ncert=f"{REF8}, rate of a chemical reaction", seconds=30, checked=True)

add("Arrhenius equation and activation energy", B, "direct",
    "When ln k is plotted against 1/T for a reaction obeying the Arrhenius equation, the intercept of the "
    "straight line on the ln k axis is:",
    Opts("D", "ln A", ["−Eₐ/R", "Eₐ/R", "A"]),
    "Linear form of the Arrhenius equation",
    "Taking natural logarithms of k = A e^(−Eₐ/RT) gives ln k = ln A − (Eₐ/R)(1/T). This is a straight line in "
    "ln k versus 1/T with slope −Eₐ/R and intercept ln A.",
    ["ln k = −(Eₐ/R)(1/T) + ln A", "Compare with y = mx + c → slope = −Eₐ/R, intercept = ln A"],
    why="−Eₐ/R is the slope, not the intercept; Eₐ/R has the wrong sign; A itself is not the intercept on a "
        "logarithmic axis.",
    ncert=f"{REF8}, temperature dependence of the rate of a reaction", seconds=25)

add("Rate law and order", B, "statement_pair",
    sp("For a gaseous reaction, when concentrations are expressed as partial pressures, the rate can be "
       "expressed in atm s⁻¹.",
       "For a reaction in solution, the rate is commonly expressed in mol L⁻¹ s⁻¹."),
    SP_, "Units of rate of reaction",
    "Rate is a change in concentration per unit time. In solution, concentration is in mol L⁻¹ and time in "
    "seconds, giving mol L⁻¹ s⁻¹. NCERT notes that for gaseous reactions, with concentrations expressed as "
    "partial pressures, the unit is atm s⁻¹. Both statements are true.",
    ["Solution: mol L⁻¹ s⁻¹ (II true)", "Gas phase with partial pressures: atm s⁻¹ (I true)"],
    answer="A", ncert=f"{REF8}, rate of a chemical reaction", seconds=25)

n_order = math.log(8) / math.log(4)
assert close(n_order, 1.5) and 8 / 4 == 2 and math.log2(8) == 3
add("Rate law and order", I, "numerical",
    "For a reaction A → products, the initial rate becomes 8 times when the initial concentration of A is made "
    "4 times. The order of the reaction with respect to A is:",
    Opts("B", "1.5", ["2", "0.5", "3"]),
    "Finding order from the effect of concentration on rate",
    "Rate = k[A]ⁿ, so (rate ratio) = (concentration ratio)ⁿ: 8 = 4ⁿ.",
    ["4ⁿ = 8 → 2²ⁿ = 2³", "2n = 3 → n = 1.5"],
    why="2 divides 8 by 4 instead of solving 4ⁿ = 8. 3 takes log₂ 8 and forgets that the concentration factor "
        "is 4, not 2. 0.5 would make the rate only 2 times larger.",
    ncert=f"{REF8}, order of a reaction", seconds=45, checked=True)

ratio = 0.6 / 0.8
assert close(0.6 * ratio, 0.45)
add("Zero and first order reactions", I, "numerical",
    "In a first-order reaction the concentration of the reactant falls from 0.80 mol L⁻¹ to 0.60 mol L⁻¹ in "
    "10 minutes. Its concentration 10 minutes later (20 minutes from the start) will be:",
    Opts("D", "0.45 mol L⁻¹", ["0.40 mol L⁻¹", "0.30 mol L⁻¹", "0.50 mol L⁻¹"]),
    "Equal times give equal fractional decrease in a first-order reaction",
    "For a first-order reaction [R] = [R]₀ e^(−kt), so in each equal time interval the concentration falls by the "
    "same fraction, not by the same amount.",
    ["In 10 min: 0.60/0.80 = 0.75 of the concentration remains", "Next 10 min: 0.60 × 0.75 = 0.45 mol L⁻¹"],
    why="0.40 mol L⁻¹ assumes an equal fall of 0.20 M, which is zero-order behaviour. 0.30 mol L⁻¹ halves the "
        "concentration, as if 10 min were the half-life. 0.50 mol L⁻¹ has no basis in the rate law.",
    ncert=f"{REF8}, integrated rate equations (first-order reactions)", seconds=60, checked=True)

add("Zero and first order reactions", I, "assertion_reason",
    ar("The inversion of cane sugar in acidic aqueous solution, C₁₂H₂₂O₁₁ + H₂O → C₆H₁₂O₆ + C₆H₁₂O₆, follows "
       "first-order kinetics although two reactants take part.",
       "Water is present in such large excess that its concentration remains practically constant during the "
       "reaction."),
    AR_, "Pseudo first-order reactions",
    "The true rate law is rate = k′[C₁₂H₂₂O₁₁][H₂O]. Because [H₂O] hardly changes, k′[H₂O] is a constant k, and "
    "the observed rate law is rate = k[C₁₂H₂₂O₁₁]: a pseudo first-order reaction. R explains A.",
    ["Rate = k′[sucrose][H₂O]", "[H₂O] ≈ constant → rate = k[sucrose] → pseudo first order"],
    answer="A", ncert=f"{REF8}, pseudo first-order reaction", seconds=35)

t75 = math.log(4) / math.log(2)
assert close(t75, 2.0)
add("Half-life", I, "multi_statement",
    ms("Which of the following statements are correct?",
       ["For a zero-order reaction, the half-life is directly proportional to the initial concentration of the "
        "reactant.",
        "For a first-order reaction, the half-life does not depend on the initial concentration of the reactant.",
        "For a first-order reaction, the time needed for 75% completion is twice its half-life.",
        "For a first-order reaction, a plot of [R] against t is a straight line.",
        "A zero-order reaction never goes to completion."]),
    multi("C", {"a": True, "b": True, "c": True, "d": False, "e": False},
          ["(a), (b), (c) and (d) only", "(b), (c) and (e) only", "(a) and (b) only"]),
    "Half-lives and integrated rate laws",
    "Zero order: [R] = [R]₀ − kt and t½ = [R]₀/2k. First order: ln[R] = ln[R]₀ − kt and t½ = 0.693/k. For first "
    "order, 75% completion means two successive halvings (100 → 50 → 25%), i.e. two half-lives.",
    ["(a) True: t½ = [R]₀/2k", "(b) True: t½ = 0.693/k", "(c) True: t₇₅% = (2.303/k) log 4 = 2 × 0.693/k",
     "(d) False: ln[R] (not [R]) versus t is linear",
     "(e) False: [R] becomes zero at t = [R]₀/k"],
    why="Options containing (d) or (e) are wrong; (a) and (b) only leaves out the true statement (c).",
    ncert=f"{REF8}, integrated rate equations and half-life", seconds=60)

ea_cat = 100 * 300 / 400
assert close(ea_cat, 75) and close(100 - ea_cat, 25) and close(100 * 100 / 300, 33.3, 0.01)
add("Arrhenius equation and activation energy", A, "numerical",
    "The activation energy of a reaction is 100 kJ mol⁻¹. In the presence of a catalyst, the rate constant at "
    "300 K equals the rate constant of the uncatalysed reaction at 400 K. Assuming the pre-exponential factor "
    "is unchanged, the catalyst lowers the activation energy by:",
    Opts("B", "25 kJ mol⁻¹", ["75 kJ mol⁻¹", "33.3 kJ mol⁻¹", "100 kJ mol⁻¹"]),
    "Arrhenius equation: equal k with equal A means equal Eₐ/RT",
    "k = A e^(−Eₐ/RT). With the same A, the two rate constants are equal when Eₐ(cat)/300 = Eₐ(uncat)/400.",
    ["Eₐ(cat)/(R × 300) = 100/(R × 400)", "Eₐ(cat) = 100 × 300/400 = 75 kJ mol⁻¹",
     "Lowering = 100 − 75 = 25 kJ mol⁻¹"],
    why="75 kJ mol⁻¹ is the activation energy with the catalyst, not the lowering. 33.3 kJ mol⁻¹ takes the "
        "lowering as Eₐ × 100 K/300 K. 100 kJ mol⁻¹ would mean the catalyst removes the barrier altogether.",
    ncert=f"{REF8}, temperature dependence and effect of a catalyst", seconds=90, checked=True)

t_eq = 11480 / (2.303 * 8.314 * math.log10(100))
assert close(t_eq, 300, 0.002) and close(11480 / (2.303 * 8.314), 600, 0.002) and close(11480 / 8.314, 1381, 0.001)
add("Arrhenius equation and activation energy", A, "numerical",
    "Two reactions have pre-exponential factors A₁ = 100 A₂ and activation energies such that Eₐ₁ − Eₐ₂ = "
    "11.48 kJ mol⁻¹. Assuming A and Eₐ do not depend on temperature, their rate constants are equal at about "
    "(R = 8.314 J K⁻¹ mol⁻¹; 2.303 log 100 = 4.606):",
    Opts("D", "300 K", ["600 K", "1381 K", "150 K"]),
    "Comparing two Arrhenius equations",
    "k₁ = k₂ when A₁ e^(−Eₐ₁/RT) = A₂ e^(−Eₐ₂/RT), i.e. ln(A₁/A₂) = (Eₐ₁ − Eₐ₂)/RT. Solve for T.",
    ["ln(A₁/A₂) = 2.303 log 100 = 4.606", "T = (Eₐ₁ − Eₐ₂)/(R × 4.606) = 11 480 / (8.314 × 4.606)",
     "T = 11 480 / 38.29 ≈ 300 K"],
    why="600 K takes log 100 as 1. 1381 K leaves out the logarithm altogether. 150 K doubles the logarithmic "
        "term.",
    ncert=f"{REF8}, temperature dependence of the rate of a reaction", seconds=120, checked=True)

add("Arrhenius equation and activation energy", A, "statement_pair",
    sp("For an endothermic elementary reaction, the activation energy of the forward reaction is greater than "
       "the enthalpy of reaction, ΔH.",
       "For an exothermic elementary reaction, the activation energy of the backward reaction is smaller than "
       "that of the forward reaction."),
    SP_, "Energy profile: Eₐ(forward) − Eₐ(backward) = ΔH",
    "On the energy profile the activated complex lies above both reactants and products, so "
    "Eₐ(forward) = ΔH + Eₐ(backward). For an endothermic reaction (ΔH > 0) with Eₐ(backward) > 0, Eₐ(forward) > ΔH: "
    "Statement I is true. For an exothermic reaction (ΔH < 0), Eₐ(backward) = Eₐ(forward) − ΔH = Eₐ(forward) + |ΔH|, "
    "which is larger, not smaller: Statement II is false.",
    ["Eₐ(f) = ΔH + Eₐ(b)", "Endothermic: Eₐ(f) > ΔH (I true)", "Exothermic: Eₐ(b) = Eₐ(f) + |ΔH| > Eₐ(f) "
     "(II false)"],
    answer="C", ncert=f"{REF8}, activation energy and the energy profile of a reaction", seconds=60)

# ==================================================================== 9. Classification of Elements and Periodicity
topic("Classification of Elements and Periodicity in Properties")
REF9 = f"{C11}, 'Classification of Elements and Periodicity in Properties'"

add("Valence and reactivity", B, "direct",
    "Using the valences of the elements, the formula of the simplest compound formed between silicon and "
    "bromine is predicted to be:",
    Opts("A", "SiBr₄", ["SiBr₂", "Si₂Br", "SiBr"]),
    "Valence from the position in the periodic table",
    "Silicon is in group 14 with four valence electrons, so its valence is 4. Bromine is in group 17; its "
    "valence is 8 − 7 = 1. One Si atom therefore combines with four Br atoms.",
    ["Si: group 14 → valence 4", "Br: group 17 → valence 8 − 7 = 1", "Formula: SiBr₄"],
    why="The other formulae do not satisfy the valences 4 (Si) and 1 (Br).",
    ncert=f"{REF9}, periodic trends in chemical properties (valence)", seconds=25)

add("Ionisation and electron gain enthalpy", B, "statement_pair",
    sp("The ionisation enthalpy of an atom is always positive.",
       "Depending on the element, the electron gain enthalpy can be negative or positive."),
    SP_, "Signs of ionisation enthalpy and electron gain enthalpy",
    "Energy is always needed to remove an electron from an isolated gaseous atom in its ground state, so "
    "ionisation enthalpy is always positive. Adding an electron releases energy for most elements (e.g. the "
    "halogens, large negative values), but must be forced on others such as the noble gases (positive values). "
    "Both statements are true.",
    ["Removing an electron always needs energy (I true)",
     "ΔegH negative for halogens, positive for noble gases (II true)"],
    answer="A", ncert=f"{REF9}, ionization enthalpy and electron gain enthalpy", seconds=25)

add("Atomic and ionic radii", I, "direct",
    "The main reason why the atomic radius decreases from left to right across a period is that:",
    Opts("D", "the effective nuclear charge increases while the added electrons enter the same valence shell",
         ["a new electron shell is added at each step", "the shielding by inner-shell electrons increases "
          "sharply from one element to the next", "the added electrons enter inner d orbitals"]),
    "Effective nuclear charge across a period",
    "Within a period the outer electrons are in the same principal shell. Each step adds one proton and one "
    "electron to that same shell; the extra electron shields the others poorly, so the effective nuclear charge "
    "rises and pulls the electron cloud closer to the nucleus.",
    ["Same n across a period", "Z_eff increases → stronger attraction → smaller radius"],
    why="A new shell is added only on going down a group. The number of inner (shielding) electrons does not "
        "change across a period. In the s- and p-block elements of a period, electrons do not enter inner d "
        "orbitals.",
    ncert=f"{REF9}, atomic radius", seconds=30)

add("Atomic and ionic radii", I, "multi_statement",
    ms("Which of the following statements about isoelectronic species are correct?",
       ["S²⁻ is larger than Cl⁻.", "Ca²⁺ is smaller than K⁺.", "Cl⁻ is smaller than K⁺.",
        "N³⁻ is smaller than O²⁻.",
        "Among isoelectronic species, the one with the greater nuclear charge has the smaller radius."]),
    multi("B", {"a": True, "b": True, "c": False, "d": False, "e": True},
          ["(a), (c) and (e) only", "(b), (d) and (e) only", "(a), (b), (c) and (e) only"]),
    "Radii of isoelectronic species",
    "Isoelectronic species have the same number of electrons. The larger the nuclear charge, the more strongly "
    "these electrons are pulled in and the smaller the species.",
    ["S²⁻ (Z = 16), Cl⁻ (17), K⁺ (19), Ca²⁺ (20) all have 18 electrons → S²⁻ > Cl⁻ > K⁺ > Ca²⁺",
     "N³⁻ (Z = 7) and O²⁻ (8) have 10 electrons → N³⁻ > O²⁻",
     "(a) True; (b) True; (c) False; (d) False; (e) True"],
    why="(c) and (d) put the species with the smaller nuclear charge as the smaller one, which is the reverse of "
        "the rule.",
    ncert=f"{REF9}, ionic radius", seconds=50)

add("Ionisation and electron gain enthalpy", I, "assertion_reason",
    ar("Electronegativity generally decreases on going down a group.",
       "The nuclear charge of the atoms decreases on going down a group."),
    AR_, "Periodic trend in electronegativity",
    "Electronegativity measures the ability of an atom in a compound to attract shared electrons. Down a group "
    "the atomic radius increases, the valence shell is farther from the nucleus, and the shared pair is held "
    "less strongly, so electronegativity falls: A is true. The nuclear charge (atomic number) actually increases "
    "down a group; its effect is outweighed by the larger size and extra shielding. R is false.",
    ["Down a group: radius ↑ → attraction for the shared pair ↓ → EN ↓ (A true)",
     "Nuclear charge increases down a group (R false)"],
    answer="C", ncert=f"{REF9}, electronegativity", seconds=30)

add("Valence and reactivity", A, "match_list",
    lists("Match List-I (ground-state electronic configuration of an element) with List-II (description of the "
          "element).",
          ["1s² 2s² 2p⁵", "1s² 2s² 2p⁶ 3s¹", "1s² 2s² 2p⁶", "1s² 2s² 2p⁶ 3s²"],
          ["A noble gas", "A highly reactive metal that forms a stable halide of formula MX",
           "A highly reactive non-metal", "A metal that forms a stable halide of formula MX₂"]),
    match("C", M("III II I IV"), [M("I II III IV"), M("III IV I II"), M("II III I IV")]),
    "Predicting properties from electronic configuration",
    "ns² np⁵ (one electron short of a noble gas) is a halogen, a highly reactive non-metal. ns¹ is an alkali "
    "metal with valence 1 (MX); ns² is a group 2 metal with valence 2 (MX₂). A completely filled shell, "
    "1s² 2s² 2p⁶, is a noble gas.",
    ["A: 2p⁵ → halogen → III", "B: 3s¹ → group 1 metal, MX → II", "C: 2p⁶ → noble gas → I",
     "D: 3s² → group 2 metal, MX₂ → IV"],
    why="The wrong codes mistake the 2p⁵ halogen for the noble gas, or interchange the valences of the ns¹ and "
        "ns² metals.",
    ncert=f"{REF9}, electronic configurations and periodic trends", seconds=50)

radii = {"F": 64, "O": 66, "Cl": 99, "S": 104}
assert radii["F"] < radii["O"] < radii["Cl"] < radii["S"]
add("Atomic and ionic radii", A, "direct",
    "Which of the following is the correct order of the covalent (atomic) radii of F, O, Cl and S?",
    Opts("B", "F < O < Cl < S", ["O < F < S < Cl", "F < Cl < O < S", "Cl < F < S < O"]),
    "Combining the period and group trends of atomic radius",
    "Radius decreases across a period (O > F; S > Cl) and increases down a group (Cl > F; S > O). The "
    "third-period atoms are larger than the second-period ones because they have an extra shell. NCERT's "
    "values are F 64 pm, O 66 pm, Cl 99 pm and S 104 pm.",
    ["Period 2: O > F", "Period 3: S > Cl", "Down a group: Cl > F, S > O", "→ F < O < Cl < S"],
    why="O < F and S < Cl reverse the period trend. Placing Cl below O ignores that Cl has one more shell.",
    ncert=f"{REF9}, atomic radius", seconds=40)

assert 36 + 10 + 2 + 3 == 51 and 18 + 10 + 2 + 3 == 33 and 36 + 2 + 3 == 41
add("Modern periodic table", A, "direct",
    "An element is in period 5 and group 15 of the periodic table. Its atomic number is:",
    Opts("C", "51", ["33", "41", "83"]),
    "Atomic number from position in the periodic table",
    "Period 5 starts after krypton (Z = 36). Its group 15 element has the outer configuration "
    "[Kr] 4d¹⁰ 5s² 5p³, so the ten 4d electrons of the transition series must be counted.",
    ["[Kr] = 36 electrons", "+ 4d¹⁰ 5s² 5p³ = 15 more electrons", "Z = 36 + 15 = 51 (antimony)"],
    why="33 is the group 15 element of period 4 (arsenic) and 83 that of period 6 (bismuth). 41 forgets the "
        "ten 4d electrons.",
    ncert=f"{REF9}, electronic configurations of elements and the periodic table", seconds=50)

# ==================================================================== 10. p-Block Elements
topic("p-Block Elements")
REF10A = "Class 11 Chemistry (pre-2023 edition), 'The p-Block Elements'"
REF10B = "Class 12 Chemistry (pre-2023 edition), 'The p-Block Elements'"

add("Group 17 and 18 trends", B, "direct",
    "The general chemical inertness of the noble gases is attributed to:",
    Opts("B", "their completely filled valence shells, very high ionisation enthalpies and large positive "
              "electron gain enthalpies",
         ["their very low ionisation enthalpies", "their large negative electron gain enthalpies",
          "the presence of vacant d orbitals in their valence shells"]),
    "Why noble gases are least reactive",
    "NCERT attributes the low reactivity of the noble gases to (i) their completely filled ns² np⁶ "
    "configurations (1s² for helium), (ii) their high ionisation enthalpies and (iii) their large positive "
    "electron gain enthalpies: they neither lose nor gain electrons easily.",
    ["Stable closed shells", "High ΔiH → hard to lose electrons", "Large positive ΔegH → hard to gain electrons"],
    why="Their ionisation enthalpies are very high, not low, and their electron gain enthalpies are positive, "
        "not negative. Vacant d orbitals would favour, not prevent, compound formation.",
    ncert=f"{REF10B}, group 18 elements: chemical properties", seconds=30)

add("Group 13 and 14 trends", B, "direct",
    "Boron does not react with acids or alkalies even at moderate temperatures, but aluminium dissolves both in "
    "mineral acids and in aqueous alkalies. This behaviour shows that aluminium is:",
    Opts("D", "amphoteric", ["a non-metal", "inert towards both acids and bases", "acidic only"]),
    "Reactivity of group 13 elements towards acids and alkalies",
    "A substance that reacts with both acids and bases shows amphoteric character. Aluminium dissolves in "
    "mineral acids and in aqueous alkalies, so it is amphoteric, unlike boron.",
    ["Reacts with acids and with alkalies → amphoteric"],
    why="Aluminium is a metal, not a non-metal. It is not inert: it dissolves in both. A purely acidic "
        "substance would react only with bases.",
    ncert=f"{REF10A}, group 13: chemical properties (reactivity towards acids and alkalies)", seconds=25)

add("Group 15 and 16 trends", B, "statement_pair",
    sp("The metallic character of the group 16 elements increases from oxygen to polonium.",
       "Oxygen is the most electronegative of all the elements."),
    SP_, "Metallic character and electronegativity of group 16 elements",
    "Within group 16 the electronegativity decreases with increasing atomic number, so the metallic character "
    "increases from oxygen to polonium: oxygen and sulphur are non-metals, selenium and tellurium metalloids and "
    "polonium a metal. Statement I is true. Fluorine is the most electronegative element; NCERT notes that "
    "oxygen has the highest electronegativity next to fluorine: Statement II is false.",
    ["Down group 16: electronegativity falls → metallic character rises, O (non-metal) to Po (metal) (I true)",
     "Most electronegative: F; O is second (II false)"],
    answer="C", ncert=f"{REF10B}, group 16 elements: atomic and physical properties", seconds=30)

add("Group 15 and 16 trends", B, "match_list",
    lists("Match List-I (group) with List-II (oxidation states commonly shown by its elements).",
          ["Group 14", "Group 15", "Group 16", "Group 17"],
          ["−1, +1, +3, +5, +7", "−2, +2, +4, +6", "−3, +3, +5", "+4, +2"]),
    match("C", M("IV III II I"), [M("IV II III I"), M("III IV II I"), M("IV III I II")]),
    "Oxidation states of the p-block groups",
    "With the outer configuration ns² npˣ, the highest oxidation state equals the total number of valence "
    "electrons (4, 5, 6, 7), and the most negative equals the number of electrons needed to complete the octet. "
    "Lower positive states, two units apart, also occur.",
    ["Group 14 (ns² np²): +4, +2", "Group 15 (ns² np³): −3, +3, +5", "Group 16 (ns² np⁴): −2, +2, +4, +6",
     "Group 17 (ns² np⁵): −1, +1, +3, +5, +7"],
    why="The wrong codes give a group a set of states that does not match its number of valence electrons.",
    ncert=f"{REF10A} and {REF10B}, oxidation states of the p-block groups", seconds=35)

add("Group 15 and 16 trends", I, "direct",
    "On moving down group 15 from nitrogen to bismuth, which of the following properties increases steadily?",
    Opts("B", "Density", ["First ionisation enthalpy", "Electronegativity", "Melting point"]),
    "Trends in physical properties down group 15",
    "Down group 15 the atomic mass rises much faster than the atomic volume, so the density increases "
    "steadily from nitrogen to bismuth. Ionisation enthalpy and electronegativity decrease down the group as "
    "the atoms get larger. The melting point increases only up to arsenic and then falls to bismuth.",
    ["Density: N < P < As < Sb < Bi (increases steadily)", "ΔiH and electronegativity: decrease down the group",
     "Melting point: rises up to As, then decreases"],
    why="Ionisation enthalpy and electronegativity fall, not rise, down the group. The melting point does not "
        "increase steadily; it passes through a maximum at arsenic.",
    ncert=f"{REF10B}, group 15 elements: physical properties", seconds=30)

add("Group 17 and 18 trends", I, "multi_statement",
    ms("Which of the following statements about the group 17 elements are correct?",
       ["Chlorine, bromine and iodine show the oxidation states +1, +3, +5 and +7, mainly in combination with "
        "oxygen and fluorine.",
        "The affinity of the halogens for hydrogen decreases from fluorine to iodine.",
        "The ionic character of the metal–halogen bond in metal halides decreases in the order "
        "M–F > M–Cl > M–Br > M–I.",
        "Bromine and iodine can show positive oxidation states because, unlike chlorine, they have vacant d "
        "orbitals."]),
    multi("D", {"a": True, "b": True, "c": True, "d": False},
          ["(a) and (b) only", "(b), (c) and (d) only", "(a), (b), (c) and (d) only"]),
    "Oxidation states and chemical properties of the halogens",
    "Chlorine, bromine and iodine all have vacant d orbitals and can expand their octets, showing +1, +3, +5 and "
    "+7, mostly with the small, very electronegative O and F atoms. Fluorine, with no d orbitals, shows only −1. "
    "The affinity for hydrogen falls from F to I, and the ionic character of M–X bonds falls from M–F to M–I.",
    ["(a) True", "(b) True", "(c) True", "(d) False: chlorine also has vacant d orbitals"],
    why="(d) is wrong because chlorine, too, has d orbitals; the halogen without them is fluorine.",
    ncert=f"{REF10B}, group 17 elements: chemical properties", seconds=60)

add("Anomalous first element", I, "statement_pair",
    sp("Most of the reactions of fluorine are exothermic, because of the small and strong bonds it forms with "
       "other elements.",
       "In group 13, the atomic radius increases considerably on going from boron to aluminium."),
    SP_, "Small size of the first member of a p-block group",
    "NCERT lists, among the anomalous features of fluorine, that most of its reactions are exothermic owing to "
    "the small and strong bonds it forms with other elements (Statement I true). The first member of a group is "
    "much smaller than the second: in group 13 the atomic radius rises from 85 pm for boron to 143 pm for "
    "aluminium, a large jump caused by the extra shell (Statement II true).",
    ["F: small atom → short, strong bonds → reactions mostly exothermic (I true)",
     "B 85 pm → Al 143 pm: one more shell, large increase (II true)"],
    answer="A", ncert=f"{REF10B}, group 17: anomalous behaviour of fluorine; {REF10A}, group 13: atomic radii",
    seconds=35)

add("Group 17 and 18 trends", I, "assertion_reason",
    ar("The halogens have the most negative electron gain enthalpies in their respective periods.",
       "A halogen atom has only one electron less than the stable configuration of the following noble gas."),
    AR_, "Electron gain enthalpy of the halogens across a period",
    "With the configuration ns² np⁵, a halogen atom needs just one electron to reach a stable noble-gas "
    "configuration, so it accepts an electron readily and releases the most energy in its period. NCERT gives "
    "exactly this reason. R explains A.",
    ["ns² np⁵ + e⁻ → ns² np⁶ (noble-gas configuration)", "→ most negative ΔegH in each period"],
    answer="A", ncert=f"{REF10B}, group 17 elements: electron gain enthalpy", seconds=30)

add("Group 13 and 14 trends", I, "direct",
    "On moving down group 14 from carbon to lead, the stability of the dihalides, MX₂:",
    Opts("C", "increases", ["decreases", "remains the same", "first increases and then decreases"]),
    "Stability of the +2 state down group 14",
    "Because of the inert pair effect, the +2 oxidation state becomes more stable down group 14. NCERT states "
    "that the stability of the dihalides increases down the group.",
    ["Inert pair effect grows down the group", "+2 state more stable → MX₂ more stable for Sn and Pb"],
    why="A decrease would mean that the +4 state became relatively more stable down the group, which is the "
        "reverse of the inert pair effect.",
    ncert=f"{REF10A}, group 14: chemical properties (reactivity towards halogens)", seconds=30)

add("Group 15 and 16 trends", A, "statement_pair",
    sp("For a group 15 element, the oxide in the higher oxidation state is more acidic than the oxide in the "
       "lower oxidation state.",
       "Down group 16, the reducing character of the dioxides EO₂ decreases from sulphur to tellurium."),
    SP_, "Acidic and redox character of oxides down groups 15 and 16",
    "NCERT: for a group 15 element, the oxide in the higher oxidation state is more acidic than that in the "
    "lower oxidation state (Statement I true). For group 16, the reducing property of the dioxides decreases "
    "from SO₂ to TeO₂: SO₂ is a reducing agent whereas TeO₂ is an oxidising agent, in line with the +6 state "
    "becoming less stable down the group (Statement II true).",
    ["E(+5) oxide more acidic than E(+3) oxide (I true)",
     "EO₂ reducing character: S > Se > Te (II true)"],
    answer="A", ncert=f"{REF10B}, groups 15 and 16: reactivity towards oxygen", seconds=40)

add("Group 13 and 14 trends", A, "multi_statement",
    ms("Which of the following statements comparing the group 14 elements with one another and with the group 13 "
       "elements are correct?",
       ["The melting and boiling points of the group 14 elements are much higher than those of the "
        "corresponding group 13 elements.",
        "The electronegativity values of the group 14 elements from silicon to lead are almost the same.",
        "The group 14 elements are less electronegative than the group 13 elements of the same periods.",
        "The first ionisation enthalpies of the group 14 elements are higher than those of the group 13 "
        "elements in the same periods.",
        "Germanium is a typical metal."]),
    multi("B", {"a": True, "b": True, "c": False, "d": True, "e": False},
          ["(a), (b), (c) and (d) only", "(b), (d) and (e) only", "(a) and (d) only"]),
    "Physical properties of group 14 compared with group 13",
    "Group 14 elements are held by stronger bonds than group 13 elements, so their melting and boiling points are "
    "much higher. Being smaller, they are slightly more electronegative than the group 13 elements, and from "
    "Si to Pb the values are almost the same. For the same reason their first ionisation enthalpies are higher "
    "than those of the corresponding group 13 elements. Carbon and silicon are non-metals and germanium is a "
    "metalloid.",
    ["(a) True", "(b) True", "(c) False: slightly more electronegative", "(d) True: e.g. C > B, Si > Al",
     "(e) False: germanium is a metalloid"],
    why="Options containing (c) or (e) are wrong; (a) and (d) only leaves out (b).",
    ncert=f"{REF10A}, group 14: ionisation enthalpy, electronegativity and physical properties", seconds=60)

ie13 = {"B": 801, "Al": 577, "Ga": 579, "In": 558, "Tl": 589}
assert sorted(ie13, key=ie13.get, reverse=True) == ["B", "Tl", "Ga", "Al", "In"]
add("Group 13 and 14 trends", A, "direct",
    "Which of the following is the correct order of the first ionisation enthalpies of the group 13 elements?",
    Opts("D", "B > Tl > Ga > Al > In",
         ["B > Al > Ga > In > Tl", "B > Ga > Al > Tl > In", "Tl > B > Ga > In > Al"]),
    "Irregular ionisation enthalpies in group 13",
    "ΔiH₁ falls sharply from B (801) to Al (577 kJ mol⁻¹). Ga (579) is slightly above Al because its ten 3d "
    "electrons shield poorly. In (558) is the lowest. Tl (589) rises again because of the poor shielding by its "
    "4f and 5d electrons.",
    ["B 801 > Tl 589 > Ga 579 > Al 577 > In 558 (kJ mol⁻¹)"],
    why="A steady decrease (B > Al > Ga > In > Tl) ignores the poor shielding by d and f electrons. The other "
        "orders misplace Tl, Al or In relative to the NCERT values, and B is clearly the highest.",
    ncert=f"{REF10A}, group 13: ionisation enthalpy", seconds=45)

add("Anomalous first element", A, "multi_statement",
    ms("Which of the following statements are correct?",
       ["Oxygen does not show a positive oxidation state except in its compounds with fluorine.",
        "In the +4 and +6 oxidation states, the bonding of sulphur, selenium and tellurium in their compounds "
        "is primarily covalent.",
        "The noble gases are highly soluble in water.",
        "Selenium, tellurium and polonium each have a completely filled (n − 1)d¹⁰ subshell just inside their "
        "valence shell."]),
    multi("C", {"a": True, "b": True, "c": False, "d": True},
          ["(a) and (b) only", "(b), (c) and (d) only", "(a), (b), (c) and (d) only"]),
    "Oxidation states and configurations in group 16; noble gases",
    "Oxygen, being more electronegative than every element except fluorine, shows positive oxidation states "
    "only with fluorine (as in OF₂). The heavier group 16 elements show +4 and +6, with mainly covalent "
    "bonding. The noble gases are only sparingly soluble in water. Se ([Ar] 3d¹⁰ 4s² 4p⁴), Te ([Kr] 4d¹⁰ 5s² "
    "5p⁴) and Po ([Xe] 4f¹⁴ 5d¹⁰ 6s² 6p⁴) all have a filled (n − 1)d¹⁰ subshell under the valence shell.",
    ["(a) True", "(b) True", "(c) False: sparingly soluble", "(d) True: 3d¹⁰ (Se), 4d¹⁰ (Te), 5d¹⁰ (Po)"],
    why="Options containing (c) are wrong, and (a) and (b) only leaves out the true statement (d).",
    ncert=f"{REF10B}, groups 16 and 18: electronic configuration, oxidation states and physical properties", seconds=60)

# ==================================================================== 11. d- and f-Block Elements
topic("d- and f-Block Elements")
REF11 = f"{C12}, 'The d- and f-Block Elements'"

n_oh = 2 * 0.05
assert close(n_oh, 0.10)
add("K2Cr2O7 and KMnO4", B, "numerical",
    "When an orange dichromate solution is made alkaline it turns yellow: "
    "Cr₂O₇²⁻ + 2OH⁻ → 2CrO₄²⁻ + H₂O. The amount of OH⁻ ions needed to convert 0.05 mol of Cr₂O₇²⁻ completely "
    "into chromate is:",
    Opts("B", "0.10 mol", ["0.05 mol", "0.20 mol", "0.025 mol"]),
    "Chromate–dichromate interconversion",
    "Chromates and dichromates are interconvertible in aqueous solution depending on the pH. The balanced "
    "equation shows that each Cr₂O₇²⁻ ion needs two OH⁻ ions.",
    ["Mole ratio OH⁻ : Cr₂O₇²⁻ = 2 : 1", "n(OH⁻) = 2 × 0.05 = 0.10 mol"],
    why="0.05 mol uses a 1 : 1 ratio. 0.20 mol counts the 2 mol of chromate formed and doubles again. 0.025 mol "
        "divides by 2 instead of multiplying.",
    ncert=f"{REF11}, potassium dichromate (chromate–dichromate equilibrium)", seconds=30, checked=True)

add("Magnetic and colour properties", B, "direct",
    "When a transition metal ion absorbs visible light because of a d–d transition, the colour we observe is:",
    Opts("D", "the complementary colour of the light absorbed",
         ["the colour of the light absorbed", "always blue, whatever light is absorbed",
          "the colour of the light emitted by the metal on heating"]),
    "Origin of colour in transition metal ions",
    "An electron excited from a lower-energy to a higher-energy d orbital absorbs light of a particular "
    "frequency, usually in the visible region. The light that is not absorbed reaches the eye, so the colour "
    "seen is the complementary colour of the light absorbed.",
    ["d–d transition absorbs part of white light", "Transmitted light → complementary colour observed"],
    why="We see the light that is transmitted, not the light absorbed. The colour depends on which frequency is "
        "absorbed, so it is not always blue; emission on heating is a different phenomenon.",
    ncert=f"{REF11}, formation of coloured ions", seconds=25)

add("Magnetic and colour properties", B, "statement_pair",
    sp("Diamagnetic substances are repelled by an applied magnetic field, whereas paramagnetic substances are "
       "attracted by it.",
       "Paramagnetism arises from the presence of unpaired electrons, each having a magnetic moment associated "
       "with its spin and orbital angular momentum."),
    SP_, "Diamagnetism and paramagnetism",
    "NCERT: diamagnetic substances are repelled by the applied field and paramagnetic substances are attracted; "
    "very strongly attracted substances are ferromagnetic. Paramagnetism arises from unpaired electrons, each of "
    "which has a magnetic moment from its spin and orbital angular momentum. Both statements are true.",
    ["Diamagnetic: repelled; paramagnetic: attracted (I true)",
     "Unpaired electrons → magnetic moment (spin + orbital) (II true)"],
    answer="A", ncert=f"{REF11}, magnetic properties", seconds=30)

add("Transition element trends", B, "assertion_reason",
    ar("Copper is regarded as a transition element although a copper atom has the ground-state configuration "
       "[Ar] 3d¹⁰ 4s¹.",
       "In its common oxidation state, +2, copper has an incompletely filled 3d subshell (3d⁹)."),
    AR_, "Definition of a transition element",
    "A transition element is one with incompletely filled d orbitals in its ground state or in any of its common "
    "oxidation states. The Cu²⁺ ion is 3d⁹, so copper qualifies. (Zinc does not: Zn and Zn²⁺ are both 3d¹⁰.) "
    "R explains A.",
    ["Definition: incomplete d subshell in atom OR common ion", "Cu²⁺: [Ar] 3d⁹ → incomplete → transition element"],
    answer="A", ncert=f"{REF11}, position in the periodic table and electronic configurations", seconds=30)

add("Transition element trends", I, "direct",
    "The reaction between iodide and persulphate ions, 2I⁻ + S₂O₈²⁻ → I₂ + 2SO₄²⁻, is catalysed by:",
    Opts("C", "Fe³⁺ ions", ["Zn²⁺ ions", "Sc³⁺ ions", "Al³⁺ ions"]),
    "Catalytic activity of transition metal ions through variable oxidation states",
    "NCERT gives this example: Fe³⁺ oxidises I⁻ to I₂ and is reduced to Fe²⁺; the Fe²⁺ is then oxidised back to "
    "Fe³⁺ by persulphate. The catalyst works because iron easily changes between the +3 and +2 states.",
    ["2Fe³⁺ + 2I⁻ → 2Fe²⁺ + I₂", "2Fe²⁺ + S₂O₈²⁻ → 2Fe³⁺ + 2SO₄²⁻", "Net: 2I⁻ + S₂O₈²⁻ → I₂ + 2SO₄²⁻"],
    why="Zn²⁺, Sc³⁺ and Al³⁺ each show essentially a single oxidation state, so they cannot shuttle between two "
        "states in this way.",
    ncert=f"{REF11}, catalytic properties", seconds=35)

add("K2Cr2O7 and KMnO4", I, "multi_statement",
    ms("Which of the following statements about potassium permanganate and potassium dichromate are correct? "
       "(Z: Cr = 24, Mn = 25)",
       ["In acidic solution, permanganate oxidises oxalic acid to carbon dioxide; the reaction is carried out "
        "at about 333 K.",
        "When dichromate is reduced in acidic solution, the chromium ion formed has the configuration [Ar] 3d³.",
        "Chromium is in the +7 oxidation state in K₂Cr₂O₇.",
        "When permanganate is reduced in acidic solution, the manganese ion formed has the configuration "
        "[Ar] 3d⁵."]),
    multi("B", {"a": True, "b": True, "c": False, "d": True},
          ["(a) and (b) only", "(b), (c) and (d) only", "(a), (c) and (d) only"]),
    "Oxidising actions of KMnO₄ and K₂Cr₂O₇",
    "Acidified permanganate oxidises oxalic acid at 333 K: 5C₂O₄²⁻ + 2MnO₄⁻ + 16H⁺ → 2Mn²⁺ + 10CO₂ + 8H₂O. "
    "Dichromate (Cr +6) is reduced to Cr³⁺, which is [Ar] 3d³. Permanganate (Mn +7) is reduced to Mn²⁺, which "
    "is [Ar] 3d⁵.",
    ["(a) True", "(b) True: Cr³⁺ = 24 − 3 = 21 electrons → [Ar] 3d³",
     "(c) False: 2x + 2(+1) + 7(−2) = 0 → x = +6", "(d) True: Mn²⁺ = 23 electrons → [Ar] 3d⁵"],
    why="Options containing (c) are wrong, and (a) and (b) only leaves out the true statement (d).",
    ncert=f"{REF11}, potassium dichromate and potassium permanganate", seconds=60)

add("Transition element trends", I, "statement_pair",
    sp("The high third ionisation enthalpies of copper, nickel and zinc explain why oxidation states higher "
       "than +2 are difficult to obtain for these elements.",
       "In aqueous solution, Mn³⁺ and Co³⁺ ions are the strongest oxidising agents among the M³⁺ ions of the "
       "3d series."),
    SP_, "Ionisation enthalpies and redox behaviour in the 3d series",
    "NCERT notes that the high values of the third ionisation enthalpies of Cu, Ni and Zn indicate why it is "
    "difficult to obtain an oxidation state greater than two for them (Statement I true). It also states that "
    "Mn³⁺ and Co³⁺ ions are the strongest oxidising agents in aqueous solution, since they are readily reduced "
    "to the more stable Mn²⁺ (d⁵) and Co²⁺ (Statement II true).",
    ["High ΔiH₃ for Cu, Ni, Zn → +2 is their usual limit (I true)",
     "Mn³⁺, Co³⁺: strongest oxidants among aquated M³⁺ (II true)"],
    answer="A", ncert=f"{REF11}, ionisation enthalpies and trends in M³⁺/M²⁺ standard electrode potentials",
    seconds=40)

assert 58 - 54 - 4 == 0 and 58 - 54 - 3 == 1 and 60 - 54 - 3 == 3 and 63 - 54 - 2 == 7
add("Lanthanoids and actinoids", I, "match_list",
    lists("Match List-I (lanthanoid ion) with List-II (its ground-state electronic configuration). "
          "(Atomic numbers: Ce 58, Nd 60, Eu 63; Xe = 54)",
          ["Ce⁴⁺", "Ce³⁺", "Nd³⁺", "Eu²⁺"],
          ["[Xe] 4f³", "[Xe] 4f⁷", "[Xe]", "[Xe] 4f¹"]),
    match("D", M("III IV I II"), [M("IV III I II"), M("III IV II I"), M("III I IV II")]),
    "Electronic configurations of lanthanoid ions",
    "Count the electrons beyond xenon (54) after removing the ionic charge; in the ions all of them are in the "
    "4f subshell.",
    ["Ce⁴⁺: 58 − 4 = 54 → [Xe] (III)", "Ce³⁺: 58 − 3 = 55 → [Xe] 4f¹ (IV)", "Nd³⁺: 60 − 3 = 57 → [Xe] 4f³ (I)",
     "Eu²⁺: 63 − 2 = 61 → [Xe] 4f⁷ (II)"],
    why="The wrong codes interchange the two cerium ions or subtract the wrong charge for Nd³⁺ or Eu²⁺.",
    ncert=f"{REF11}, the lanthanoids: electronic configurations and oxidation states", seconds=50)

add("Lanthanoids and actinoids", I, "direct",
    "The highest oxidation state shown by uranium (Z = 92) is:",
    Opts("B", "+6", ["+3", "+4", "+7"]),
    "Oxidation states of the actinoids",
    "Among the early actinoids the maximum oxidation state rises from +4 for Th to +5 for Pa, +6 for U and +7 for "
    "Np, and then falls in the later elements. Uranium shows +3, +4, +5 and +6.",
    ["Th +4 → Pa +5 → U +6 → Np +7 (maximum states)", "Uranium: +3, +4, +5, +6"],
    why="+3 and +4 are lower states that uranium also shows, not its highest. +7 is shown by neptunium.",
    ncert=f"{REF11}, the actinoids: oxidation states", seconds=30)

ratio_fe = F(5, 3)
assert ratio_fe == F(5, 3)
add("K2Cr2O7 and KMnO4", A, "numerical",
    "Equal amounts (in moles) of KMnO₄ are used to oxidise Fe²⁺ to Fe³⁺, once in acidic solution (MnO₄⁻ → Mn²⁺) "
    "and once in neutral solution (MnO₄⁻ → MnO₂). The ratio of the amounts of Fe²⁺ oxidised in the acidic and in "
    "the neutral solution is:",
    Opts("D", "5 : 3", ["3 : 5", "1 : 1", "5 : 1"]),
    "Electrons gained by permanganate in different media",
    "Each Fe²⁺ gives one electron. In acid, Mn goes from +7 to +2 (5 electrons gained per MnO₄⁻); in neutral "
    "solution from +7 to +4 (3 electrons). The amount of Fe²⁺ oxidised is proportional to the electrons accepted.",
    ["Acidic: MnO₄⁻ + 8H⁺ + 5e⁻ → Mn²⁺ + 4H₂O → 5 Fe²⁺ per MnO₄⁻",
     "Neutral: MnO₄⁻ + 2H₂O + 3e⁻ → MnO₂ + 4OH⁻ → 3 Fe²⁺ per MnO₄⁻", "Ratio = 5 : 3"],
    why="3 : 5 inverts the ratio. 1 : 1 ignores the different reduction products. 5 : 1 compares the acidic "
        "reaction with a one-electron change.",
    ncert=f"{REF11}, potassium permanganate: oxidising action", seconds=60, checked=True)

add("Transition element trends", A, "assertion_reason",
    ar("Ti²⁺, V²⁺ and Cr²⁺ ions liberate hydrogen from dilute acids.",
       "These ions are strong reducing agents: they are readily oxidised to the +3 state while H⁺ ions are reduced "
       "to H₂."),
    AR_, "Reducing M²⁺ ions of the early 3d metals",
    "NCERT: the ions Ti²⁺, V²⁺ and Cr²⁺ are strong reducing agents and will liberate hydrogen from a dilute acid, "
    "e.g. 2Cr²⁺(aq) + 2H⁺(aq) → 2Cr³⁺(aq) + H₂(g). Their reducing power is the reason for the reaction, so R "
    "explains A.",
    ["M²⁺ → M³⁺ + e⁻ (oxidised)", "2H⁺ + 2e⁻ → H₂ (reduced)"],
    answer="A", ncert=f"{REF11}, chemical reactivity and E° values", seconds=40)

add("Transition element trends", A, "multi_statement",
    ms("Which of the following statements about the transition metals are correct?",
       ["They form many complex compounds because of the small size and high charge of their ions and the "
        "availability of d orbitals for bond formation.",
        "In catalysis at a solid surface, bonds form between reactant molecules and atoms of the catalyst; the "
        "first-row transition metals use their 3d and 4s electrons for this bonding.",
        "Alloys form readily between metals whose atomic radii are within about 15% of each other.",
        "The paramagnetism of a transition metal ion increases as its number of unpaired electrons decreases."]),
    multi("B", {"a": True, "b": True, "c": True, "d": False},
          ["(a) and (b) only", "(b), (c) and (d) only", "(a), (b), (c) and (d) only"]),
    "Complex formation, catalysis, alloys and magnetism",
    "NCERT attributes complex formation to the small size and high charge of the ions and available d orbitals; "
    "surface catalysis to bond formation using 3d and 4s electrons; and alloy formation to similar atomic radii "
    "(within about 15%). The magnetic moment increases with the number of unpaired electrons, μ = √(n(n + 2)) BM.",
    ["(a) True", "(b) True", "(c) True", "(d) False: μ increases as n increases"],
    why="Options containing (d) are wrong, and (a) and (b) only leaves out the true statement (c).",
    ncert=f"{REF11}, general properties of the transition elements", seconds=60)

assert 1.51 > 1.36 > 1.33
add("K2Cr2O7 and KMnO4", A, "direct",
    "Given the standard reduction potentials E°(MnO₄⁻/Mn²⁺) = +1.51 V, E°(Cr₂O₇²⁻/Cr³⁺) = +1.33 V and "
    "E°(Cl₂/Cl⁻) = +1.36 V, which of the following is correct under standard conditions in acidic solution?",
    Opts("C", "Permanganate can oxidise Cl⁻ to Cl₂, but dichromate cannot",
         ["Both permanganate and dichromate can oxidise Cl⁻ to Cl₂",
          "Neither permanganate nor dichromate can oxidise Cl⁻ to Cl₂",
          "Dichromate can oxidise Cl⁻ to Cl₂, but permanganate cannot"]),
    "Predicting redox reactions from standard electrode potentials",
    "An oxidant can oxidise Cl⁻ to Cl₂ under standard conditions only if its reduction potential is higher than "
    "that of Cl₂/Cl⁻, so that E°cell is positive.",
    ["MnO₄⁻/Mn²⁺ with Cl₂/Cl⁻: E°cell = 1.51 − 1.36 = +0.15 V → feasible",
     "Cr₂O₇²⁻/Cr³⁺ with Cl₂/Cl⁻: E°cell = 1.33 − 1.36 = −0.03 V → not feasible"],
    why="The other options ignore that 1.33 V is lower, and 1.51 V higher, than 1.36 V.",
    ncert=f"{REF11}, potassium dichromate and potassium permanganate; {REF7B}, electrode potentials",
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
    doc = {"schema_version": "1.0", "batch_id": "BATCH_006", "created_at": TODAY,
           "notes": "Package CHE_006_p1: 131 original Chemistry questions (physical chemistry, periodicity, p-block and "
                    "d- and f-block). Numerical answers re-derived in tools/batch_006/CHE_006_p1.py.",
           "stimuli": [], "questions": QUESTIONS}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {OUT}: {n} questions; difficulty {dict(Counter(q['difficulty'] for q in QUESTIONS))}; "
          f"formats {dict(fmts)}; keys {dict(sorted(KEYS.items()))}")
