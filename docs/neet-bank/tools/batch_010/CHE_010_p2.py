"""Writes batches/parts/BATCH_010_CHE_p2.json: package CHE_010_p2 of BATCH_010 (Chemistry, 128 questions).

Topics: Coordination Compounds, Purification and Characterisation of Organic Compounds, Some Basic Principles of
Organic Chemistry, Hydrocarbons, Organic Compounds Containing Halogens / Oxygen / Nitrogen, Biomolecules (Chemistry),
Principles Related to Practical Chemistry. IDs NEET_CHE_002373..002500.

Every numerical answer is re-derived below with an assert; multi-statement keys are derived from the truth value of
each statement, assertion-reason and statement-pair keys from the truth of each part. If any check fails, nothing is
written.

    python docs/neet-bank/tools/batch_010/CHE_010_p2.py
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
OUT = ROOT / "batches" / "parts" / "BATCH_010_CHE_p2.json"
TODAY = "2026-11-16"
LETTERS = "ABCD"
CHE = "Chemistry"
FIRST, LAST = 2373, 2500
# ai:self-recheck = a second, separate solve of every question by the author after the file was written.
AUTHORED = ("ai:author-solve", "ai:self-recheck")
RECOMPUTED = ("script:recompute", "ai:author-solve", "ai:self-recheck")

T_CC = "Coordination Compounds"
T_PU = "Purification and Characterisation of Organic Compounds"
T_GO = "Some Basic Principles of Organic Chemistry"
T_HC = "Hydrocarbons"
T_HX = "Organic Compounds Containing Halogens"
T_OX = "Organic Compounds Containing Oxygen"
T_NI = "Organic Compounds Containing Nitrogen"
T_BM = "Biomolecules (Chemistry)"
T_PR = "Principles Related to Practical Chemistry"

NC12 = "Class 12 Chemistry"
NC11 = "Class 11 Chemistry"
LAB = "NCERT Laboratory Manual Chemistry (Class 11/12)"


def q(qid, subject, topic, subtopic, difficulty, fmt, text, options, answer, concept, explanation, steps,
      shortcut=None, why_others_wrong=None, ncert=None, seconds=60, verified_by=AUTHORED):
    assert answer in LETTERS and len(options) == 4 and len(set(options)) == 4
    return {
        "question_id": qid, "exam_mappings": default_mappings(subject), "subject": subject, "topic": topic,
        "subtopic": subtopic, "difficulty": difficulty, "question_type": "MCQ", "format": fmt, "language": "en",
        "question_text": text,
        "options": [{"key": LETTERS[i], "text": t} for i, t in enumerate(options)],
        "correct_answer": answer,
        "solution": {"concept": concept, "explanation": explanation, "steps": steps, "shortcut": shortcut,
                     "why_others_wrong": why_others_wrong, "ncert_reference": ncert,
                     "final_answer": f"Option {answer}: {options[LETTERS.index(answer)]}"},
        "suggested_time_seconds": seconds,
        "source": {"source_type": "Original", "source_name": "PrepMitra", "source_url": None,
                   "original_exam_year": None, "license_note": None},
        "verification": {"answer_verified": True, "solution_verified": True, "review_status": "Pending Human Review",
                         "verified_by": list(verified_by), "verified_at": TODAY},
    }


_NEXT = iter(range(FIRST, LAST + 1))


def Q(topic, subtopic, difficulty, fmt, text, options, answer, *rest, **kw):
    """q() with the next ID of this package (questions are written in ID order)."""
    return q(f"NEET_CHE_{next(_NEXT):06d}", CHE, topic, subtopic, difficulty, fmt, text, options, answer, *rest, **kw)


def N(topic, subtopic, difficulty, text, options, answer, value, *rest, **kw):
    """A numerical question: `value` is the recomputed answer text and must be the keyed option."""
    assert options[LETTERS.index(answer)] == value, (text[:60], value, options)
    kw.setdefault("verified_by", RECOMPUTED)
    return Q(topic, subtopic, difficulty, "numerical", text, options, answer, *rest, **kw)


def P(s):
    """'III IV I II' -> {'A': 'III', 'B': 'IV', 'C': 'I', 'D': 'II'}"""
    return dict(zip("ABCD", s.split()))


def match_options(correct: dict, wrong: list, at: str) -> list:
    """Option texts for a match-the-list question with the correct code at position `at`."""
    code = lambda m: ", ".join(f"{k}-{m[k]}" for k in "ABCD")
    for m in [correct, *wrong]:
        assert sorted(m.values()) == sorted(["I", "II", "III", "IV"])
    opts = [code(w) for w in wrong]
    opts.insert(LETTERS.index(at), code(correct))
    assert len(set(opts)) == 4
    return opts


def ml(intro, list1, list2, correct, wrong, at):
    """(text, options, key) for match-the-list. list1/list2 are 4 strings each; correct maps A..D to I..IV."""
    roman = ["I", "II", "III", "IV"]
    text = (intro + "\n\nList-I:\n" + "\n".join(f"{k}. {v}" for k, v in zip("ABCD", list1)) +
            "\n\nList-II:\n" + "\n".join(f"{r}. {v}" for r, v in zip(roman, list2)) +
            "\n\nChoose the correct answer from the options given below:")
    return text, match_options(P(correct), [P(w) for w in wrong], at), at


def ms(intro, stmts, wrong, at):
    """(text, options, key) for multi-statement. stmts = [(text, is_true)]; the key is derived from the truths."""
    let = "abcde"[:len(stmts)]
    text = (intro + "\n\n" + "\n".join(f"({let[i]}) {s}" for i, (s, _) in enumerate(stmts)) +
            "\n\nChoose the correct answer from the options given below:")
    true = [let[i] for i, (_, t) in enumerate(stmts) if t]
    lab = lambda xs: ", ".join(f"({x})" for x in xs[:-1]) + f" and ({xs[-1]}) only" if len(xs) > 1 else f"({xs[0]}) only"
    assert all(sorted(w) != true for w in wrong)
    opts = [lab(sorted(w)) for w in wrong]
    opts.insert(LETTERS.index(at), lab(true))
    assert len(set(opts)) == 4
    return text, opts, at


def ar(assertion, a_true, reason, r_true, explains=False):
    """(text, options, key) for assertion-reason; the key follows from the truth of A and R."""
    assert a_true or r_true, "NEET's fixed set has no 'both false' option"
    key = "A" if (a_true and r_true and explains) else "B" if (a_true and r_true) else "C" if a_true else "D"
    text = ("Given below are two statements: one is labelled Assertion (A) and the other is labelled Reason (R).\n\n"
            f"Assertion (A): {assertion}\nReason (R): {reason}\n\n"
            "Choose the correct answer from the options given below:")
    return text, ASSERTION_REASON, key


def sp(s1, t1, s2, t2):
    """(text, options, key) for statement-pair; the key follows from the truth of each statement."""
    key = {(True, True): "A", (False, False): "B", (True, False): "C", (False, True): "D"}[(t1, t2)]
    text = (f"Given below are two statements:\n\nStatement I: {s1}\nStatement II: {s2}\n\n"
            "In the light of the above statements, choose the correct answer from the options given below:")
    return text, STATEMENT_PAIR, key


def g(x, nd=1, unit=" g"):
    """Format a number with nd decimals and a unit."""
    return f"{float(x):.{nd}f}{unit}"


def pct(x, nd=1):
    return f"{float(x) * 100:.{nd}f}%"


AM = {"C": 12, "H": 1, "O": 16, "N": 14, "S": 32, "Na": 23, "Cl": F(355, 10), "K": 39, "Br": 80, "I": 127,
      "Ag": 108, "Mn": 55, "Cr": 52, "Fe": 56, "Co": 59, "Ni": 59, "Pt": 195, "Cu": F(635, 10), "Zn": 65, "Mg": 24,
      "Ca": 40, "Ba": 137, "P": 31, "B": F(108, 10), "Al": 27, "As": 75, "Sb": 122, "Sn": 119, "Rh": 103}


def mm(**atoms):
    """Molar mass from atom counts, e.g. mm(C=2, H=6, O=1)."""
    return sum(AM[k] * v for k, v in atoms.items())


def bm(n):
    """Spin-only magnetic moment sqrt(n(n+2)) in BM."""
    return math.sqrt(n * (n + 2))


QUESTIONS = []

# ================================================================ Coordination Compounds (2373-2388)
# 2375: heteroleptic entities in the list
het_2375 = {"[Co(NH3)6]3+": 1, "[Co(NH3)4Cl2]+": 2, "[Ni(CO)4]": 1, "[Fe(CN)6]4-": 1, "[Co(en)2Cl2]+": 2,
            "[Pt(NH3)2Cl2]": 2, "[Cr(C2O4)3]3-": 1, "[Co(NH3)5(H2O)]3+": 2}  # number of kinds of ligand
v_2375 = str(sum(1 for k in het_2375.values() if k > 1))
assert v_2375 == "4"
# 2378: only [Co(NH3)5Br]SO4 releases free sulphate; 0.010 mol BaSO4
m_2378 = F(10, 1000) * (AM["Ba"] + AM["S"] + 4 * AM["O"])
assert m_2378 == F(233, 100)
v_2378 = f"{float(m_2378):.2f} g"
# 2379: Cr3+ d3, t2g3: CFSE = 3 x (-0.4 Do) = -1.2 Do; Do = 260 kJ/mol
cfse = lambda t2g, eg: F(-4, 10) * t2g + F(6, 10) * eg
e_2379 = cfse(3, 0) * 260
assert e_2379 == -312
v_2379 = "−312 kJ mol⁻¹"
assert (F(-4, 10) * 260, F(-6, 10) * 260, F(-18, 10) * 260) == (-104, -156, -468)
# 2384: 2.665 g of CrCl3.6H2O (266.5 g/mol) gives 2.87 g AgCl (143.5 g/mol) -> 2 ionisable Cl
M_2384 = AM["Cr"] + 3 * AM["Cl"] + 6 * mm(H=2, O=1)
assert M_2384 == F(2665, 10)
n_cplx = F(2665, 1000) / M_2384
n_agcl = F(287, 100) / (AM["Ag"] + AM["Cl"])
assert n_cplx == F(1, 100) and n_agcl == F(2, 100) and n_agcl / n_cplx == 2
v_2384 = "[Cr(H₂O)₅Cl]Cl₂·H₂O"
# 2385: [Cr(NH3)6]3+ (d3, 3 unpaired) + [Fe(CN)6]3- (low-spin d5, 1 unpaired)
v_2385 = str(3 + 1)
assert v_2385 == "4" and 3 + 5 == 8
# 2388: CFSE values (ignoring pairing): HS d5 = 0, d10 = 0, HS d4 = -0.6, LS d5 = -2.0
assert cfse(3, 2) == 0 and cfse(6, 4) == 0 and cfse(3, 1) == F(-6, 10) and cfse(5, 0) == -2
assert abs(cfse(3, 2)) < abs(cfse(3, 1))  # statement (e) is false

QUESTIONS += [
    Q(T_CC, "IUPAC nomenclature", "Basic", "direct",
      "The IUPAC name of the complex ion [Pt(NH₃)BrCl(NO₂)]⁻, in which the nitrite ligand is bonded through "
      "nitrogen, is:",
      ["Amminebromidochloridonitrito-N-platinum(II) ion", "Amminechloridobromidonitrito-N-platinate(II) ion",
       "Amminebromidochloridonitrito-N-platinate(II) ion", "Amminebromidochloridonitrito-N-platinate(IV) ion"], "C",
      "Naming an anionic coordination entity",
      "The ligands are named in alphabetical order: ammine, bromido, chlorido, nitrito-N. The oxidation state of "
      "platinum is x + 0 − 1 − 1 − 1 = −1, so x = +2. Because the entity is an anion, the metal name takes the "
      "ending -ate: platinate(II).",
      ["Ligands alphabetically: ammine (a), bromido (b), chlorido (c), nitrito-N (n)",
       "Oxidation state: x − 3 = −1 → x = +2", "Anionic entity → platinate(II)"],
      why_others_wrong="'Platinum(II)' is used only when the entity is a cation or neutral; chlorido before bromido "
                       "breaks the alphabetical order; (IV) ignores the three anionic ligands in the charge balance.",
      ncert=f"{NC12}, 'Coordination Compounds', naming of mononuclear coordination compounds", seconds=40),

    Q(T_CC, "IUPAC nomenclature", "Basic", "direct",
      "The formula of dichloridobis(ethane-1,2-diamine)platinum(IV) nitrate is:",
      ["[PtCl₂(en)₂]NO₃", "[PtCl₂(en)₂](NO₃)₄", "[Pt(en)₂]Cl₂(NO₃)₂", "[PtCl₂(en)₂](NO₃)₂"], "D",
      "Writing the formula from the name",
      "The coordination entity contains two chloride ions and two neutral en ligands around Pt⁴⁺, so its charge is "
      "+4 − 2 = +2. Two nitrate ions balance this charge.",
      ["Entity: [PtCl₂(en)₂]ˣ, x = +4 + 2(−1) + 2(0) = +2", "Two NO₃⁻ counter ions → [PtCl₂(en)₂](NO₃)₂"],
      why_others_wrong="One or four nitrate ions do not balance a +2 entity; writing the chlorides outside the square "
                       "brackets contradicts the name, which lists them as ligands (dichlorido).",
      ncert=f"{NC12}, 'Coordination Compounds', formulas of mononuclear coordination entities", seconds=30),

    N(T_CC, "Werner's theory and ligands", "Basic",
      "How many of the following coordination entities are heteroleptic?\n"
      "[Co(NH₃)₆]³⁺, [Co(NH₃)₄Cl₂]⁺, [Ni(CO)₄], [Fe(CN)₆]⁴⁻, [Co(en)₂Cl₂]⁺, [Pt(NH₃)₂Cl₂], [Cr(C₂O₄)₃]³⁻, "
      "[Co(NH₃)₅(H₂O)]³⁺",
      ["3", v_2375, "5", "6"], "B", v_2375,
      "Homoleptic and heteroleptic complexes",
      "A complex in which the metal is bound to only one kind of donor group is homoleptic; one bound to more than "
      "one kind of donor group is heteroleptic.",
      ["Homoleptic: [Co(NH₃)₆]³⁺, [Ni(CO)₄], [Fe(CN)₆]⁴⁻, [Cr(C₂O₄)₃]³⁻",
       "Heteroleptic: [Co(NH₃)₄Cl₂]⁺, [Co(en)₂Cl₂]⁺, [Pt(NH₃)₂Cl₂], [Co(NH₃)₅(H₂O)]³⁺ → 4"],
      why_others_wrong="3 usually misses [Co(NH₃)₅(H₂O)]³⁺, where one water molecule makes the complex heteroleptic; "
                       "5 or 6 counts charged or chelate complexes such as [Fe(CN)₆]⁴⁻ or [Cr(C₂O₄)₃]³⁻, which have "
                       "only one kind of ligand.",
      ncert=f"{NC12}, 'Coordination Compounds', homoleptic and heteroleptic complexes", seconds=40),

    Q(T_CC, "Werner's theory and ligands", "Basic", "statement_pair",
      *sp("According to Werner's theory, the secondary valence of the central metal ion in a complex corresponds to "
          "its coordination number.", True,
          "In [Co(en)₃]Cl₃ (en = ethane-1,2-diamine), the secondary valence of cobalt is 3.", False),
      "Primary and secondary valences",
      "Werner's secondary valence is the coordination number. Each en is didentate, so three en ligands supply six "
      "donor nitrogen atoms: the coordination number (secondary valence) of cobalt is 6. Its primary valence "
      "(oxidation state) is 3.",
      ["Statement I: true (secondary valence = coordination number)",
       "Statement II: false; 3 en × 2 donor atoms = 6, so the secondary valence is 6"],
      ncert=f"{NC12}, 'Coordination Compounds', Werner's theory; coordination number", seconds=35),

    Q(T_CC, "Werner's theory and ligands", "Basic", "match_list",
      *ml("Match the ligand in List-I with the donor atom(s) through which it binds the metal in List-II.",
          ["Ethane-1,2-diamine (en)", "Oxalate ion, C₂O₄²⁻", "Carbonyl, CO", "Nitrite ion, bound as nitrito-O"],
          ["One oxygen atom", "Two nitrogen atoms", "One carbon atom", "Two oxygen atoms"],
          "II IV III I", ["II I III IV", "IV II III I", "II IV I III"], "D"),
      "Donor atoms of common ligands",
      "en, H₂N–CH₂–CH₂–NH₂, is didentate through its two nitrogen atoms; oxalate is didentate through two oxygen "
      "atoms; CO binds through carbon; the ambidentate nitrite ion binds through oxygen in the nitrito-O form.",
      ["en → two N", "C₂O₄²⁻ → two O", "CO → C", "–ONO → one O"],
      why_others_wrong="Codes that give oxalate a single oxygen confuse it with nitrito-O; code with CO → one O "
                       "forgets that CO donates the lone pair on carbon.",
      ncert=f"{NC12}, 'Coordination Compounds', ligands: didentate and ambidentate ligands", seconds=40),

    N(T_CC, "Isomerism", "Intermediate",
      "[Co(NH₃)₅Br]SO₄ and [Co(NH₃)₅(SO₄)]Br are ionisation isomers. 0.010 mol of each is dissolved together in "
      "water and an excess of BaCl₂ solution is added. The mass of BaSO₄ precipitated is (Ba = 137, S = 32, "
      "O = 16):",
      ["0 g", "1.17 g", v_2378, "4.66 g"], "C", v_2378,
      "Ionisation isomers give different ions in solution",
      "In [Co(NH₃)₅Br]SO₄ the sulphate is a counter ion and is free in solution, so it is precipitated by Ba²⁺. In "
      "[Co(NH₃)₅(SO₄)]Br the sulphate is coordinated to cobalt and is not available; this isomer gives free Br⁻ "
      "instead.",
      ["Free SO₄²⁻ comes only from [Co(NH₃)₅Br]SO₄: 0.010 mol", "BaSO₄ = 0.010 × 233 = 2.33 g"],
      why_others_wrong="4.66 g assumes that both isomers release sulphate; 1.17 g halves the correct amount; 0 g "
                       "assumes that sulphate is never free in a cobalt ammine complex.",
      ncert=f"{NC12}, 'Coordination Compounds', structural isomerism: ionisation isomerism", seconds=60),

    N(T_CC, "Crystal field theory", "Intermediate",
      "For the octahedral complex [Cr(NH₃)₆]³⁺ (Z of Cr = 24), the crystal field splitting energy Δo is "
      "260 kJ mol⁻¹. Taking the energy of each t₂g electron as −0.4Δo and of each eg electron as +0.6Δo, the "
      "crystal field stabilisation energy of the complex is:",
      [v_2379, "−104 kJ mol⁻¹", "−156 kJ mol⁻¹", "−468 kJ mol⁻¹"], "A", v_2379,
      "Crystal field stabilisation energy of a d³ ion",
      "Cr³⁺ is 3d³. In an octahedral field the three electrons occupy the t₂g orbitals singly (t₂g³ eg⁰), "
      "whatever the field strength, so CFSE = 3 × (−0.4Δo) = −1.2Δo.",
      ["Cr³⁺: 3d³ → t₂g³ eg⁰", "CFSE = 3 × (−0.4 × 260) = −312 kJ mol⁻¹"],
      why_others_wrong="−104 kJ mol⁻¹ counts only one electron; −156 kJ mol⁻¹ uses 0.6Δo for a single electron; "
                       "−468 kJ mol⁻¹ uses 0.6Δo for each of the three electrons, the eg value, with a minus sign.",
      ncert=f"{NC12}, 'Coordination Compounds', crystal field splitting in octahedral complexes", seconds=60),

    Q(T_CC, "Valence bond theory", "Intermediate", "assertion_reason",
      *ar("[Mn(CN)₆]³⁻ has two unpaired electrons, whereas [MnCl₆]³⁻ has four unpaired electrons (Z of Mn = 25).",
          True,
          "CN⁻ is a strong field ligand that makes two of the four 3d electrons of Mn³⁺ pair up, whereas Cl⁻ is a "
          "weak field ligand that cannot do so.", True, explains=True),
      "Magnetic behaviour of inner and outer orbital complexes",
      "Mn³⁺ is 3d⁴. With CN⁻ the electrons pair into three 3d orbitals (two unpaired), leaving two 3d orbitals for "
      "d²sp³ hybridisation. With Cl⁻ no pairing occurs, so four electrons stay unpaired and the outer 4d orbitals are "
      "used (sp³d²). The ligand field strength is exactly why the numbers differ.",
      ["Mn³⁺: 3d⁴", "CN⁻ (strong field): paired → 2 unpaired, inner orbital",
       "Cl⁻ (weak field): unpaired → 4 unpaired, outer orbital"],
      ncert=f"{NC12}, 'Coordination Compounds', magnetic properties of coordination compounds", seconds=45),

    Q(T_CC, "Valence bond theory", "Intermediate", "multi_statement",
      *ms("Which of the following statements, based on valence bond theory, are correct?",
          [("dsp² hybridisation of the central atom gives a square planar coordination entity.", True),
           ("sp³d hybridisation of the central atom gives a trigonal bipyramidal coordination entity.", True),
           ("In [CoF₆]³⁻, the six 3d electrons of Co³⁺ are paired up in three 3d orbitals.", False),
           ("An inner orbital complex uses (n−1)d orbitals in hybridisation, whereas an outer orbital complex uses "
            "nd orbitals.", True),
           ("Every inner orbital octahedral complex is diamagnetic.", False)],
          [["a", "b", "d", "e"], ["b", "c", "d"], ["a", "d"]], "B"),
      "Hybridisation, geometry and inner/outer orbital complexes",
      "dsp² → square planar and sp³d → trigonal bipyramidal. In [CoF₆]³⁻, F⁻ is a weak field ligand: the 3d⁶ "
      "electrons stay unpaired as far as possible (four unpaired) and cobalt uses sp³d² hybrid orbitals. Inner "
      "orbital complexes use (n−1)d orbitals, but they need not be diamagnetic: [Fe(CN)₆]³⁻ has one and "
      "[Cr(NH₃)₆]³⁺ three unpaired electrons.",
      ["(a) true", "(b) true", "(c) false: [CoF₆]³⁻ has four unpaired electrons (outer orbital)",
       "(d) true", "(e) false: [Fe(CN)₆]³⁻ and [Cr(NH₃)₆]³⁺ are inner orbital yet paramagnetic"],
      why_others_wrong="Options with (e) forget paramagnetic inner orbital complexes; options with (c) treat F⁻ as "
                       "a strong field ligand; (a) and (d) only leaves out the correct shape for sp³d.",
      ncert=f"{NC12}, 'Coordination Compounds', valence bond theory; magnetic properties", seconds=75),

    Q(T_CC, "Werner's theory and ligands", "Intermediate", "match_list",
      *ml("Werner also studied platinum(IV) ammine chlorides. Assume that platinum has a coordination number of 6 "
          "in each compound below and that each is treated with an excess of AgNO₃ solution. Match the compound in "
          "List-I with the number of moles of AgCl precipitated per mole of compound in List-II.",
          ["PtCl₄·6NH₃", "PtCl₄·5NH₃", "PtCl₄·4NH₃", "PtCl₄·3NH₃"],
          ["1", "2", "3", "4"],
          "IV III II I", ["I II III IV", "IV III I II", "III IV II I"], "C"),
      "Werner's theory: ionisable chlorides",
      "With six positions to fill, every NH₃ is coordinated and the remaining positions are taken by chloride ions; "
      "only the chlorides outside the coordination sphere are precipitated by Ag⁺.",
      ["PtCl₄·6NH₃ = [Pt(NH₃)₆]Cl₄ → 4 AgCl", "PtCl₄·5NH₃ = [Pt(NH₃)₅Cl]Cl₃ → 3",
       "PtCl₄·4NH₃ = [Pt(NH₃)₄Cl₂]Cl₂ → 2", "PtCl₄·3NH₃ = [Pt(NH₃)₃Cl₃]Cl → 1"],
      shortcut="Ionisable Cl⁻ = 4 − (6 − number of NH₃).",
      why_others_wrong="The reversed code takes the coordinated chlorides as the ionisable ones; the other codes "
                       "pair a compound with a count that leaves the coordination number different from 6.",
      ncert=f"{NC12}, 'Coordination Compounds', Werner's theory of coordination compounds", seconds=60),

    Q(T_CC, "Isomerism", "Intermediate", "statement_pair",
      *sp("[Co(NH₃)₅(NO₂)]Cl₂ is obtained in a yellow form, in which the nitrite ligand is bound through nitrogen, "
          "and in a red form, in which it is bound through oxygen.", True,
          "According to Werner, the ions or groups bound to the metal by secondary linkages have characteristic "
          "spatial arrangements corresponding to different coordination numbers.", True),
      "Linkage isomerism; Werner's postulates",
      "NCERT describes the two linkage isomers of [Co(NH₃)₅(NO₂)]Cl₂: the yellow –NO₂ (nitrito-N) form and the red "
      "–ONO (nitrito-O) form. Werner's postulates include that secondary linkages give characteristic spatial "
      "arrangements, the coordination polyhedra (octahedral, tetrahedral, square planar).",
      ["Statement I: true (linkage isomers, yellow N-bound and red O-bound)", "Statement II: true"],
      ncert=f"{NC12}, 'Coordination Compounds', linkage isomerism; Werner's theory", seconds=40),

    N(T_CC, "Isomerism", "Advanced",
      "CrCl₃·6H₂O (molar mass 266.5 g mol⁻¹) exists as hydrate (solvate) isomers in which chromium has a "
      "coordination number of 6. A solution containing 2.665 g of one isomer gives 2.87 g of AgCl with an excess "
      "of AgNO₃ solution (molar mass of AgCl = 143.5 g mol⁻¹). The isomer is:",
      ["[Cr(H₂O)₆]Cl₃", "[Cr(H₂O)₄Cl₂]Cl·2H₂O", "[Cr(H₂O)₃Cl₃]·3H₂O", v_2384], "D", v_2384,
      "Identifying a hydrate isomer from the ionisable chloride",
      "Only chloride ions outside the coordination sphere are precipitated as AgCl. The mole ratio AgCl : complex "
      "tells how many chlorides are ionisable; the rest are coordinated, and water fills the remaining positions.",
      ["Complex: 2.665 / 266.5 = 0.0100 mol", "AgCl: 2.87 / 143.5 = 0.0200 mol → 2 ionisable Cl⁻",
       "One Cl⁻ coordinated + five H₂O → [Cr(H₂O)₅Cl]Cl₂·H₂O"],
      why_others_wrong="[Cr(H₂O)₆]Cl₃ would give 3 mol AgCl per mole (4.31 g); [Cr(H₂O)₄Cl₂]Cl·2H₂O would give "
                       "1.435 g; the neutral [Cr(H₂O)₃Cl₃]·3H₂O gives no precipitate.",
      ncert=f"{NC12}, 'Coordination Compounds', solvate (hydrate) isomerism", seconds=90),

    N(T_CC, "Crystal field theory", "Advanced",
      "In the compound [Cr(NH₃)₆][Fe(CN)₆], chromium is in the +3 oxidation state, and the cyanido complex of iron "
      "is low spin (atomic numbers: Cr 24, Fe 26). The total number of unpaired electrons in one formula unit is:",
      ["3", v_2385, "5", "8"], "B", v_2385,
      "Charge balance and spin state in a complex salt",
      "The cation is [Cr(NH₃)₆]³⁺, so the anion must be [Fe(CN)₆]³⁻, which contains Fe³⁺ (3d⁵). Cr³⁺ (3d³, t₂g³) "
      "has three unpaired electrons; low-spin Fe³⁺ (t₂g⁵) has one.",
      ["[Cr(NH₃)₆]³⁺ → anion [Fe(CN)₆]³⁻ → Fe³⁺", "Cr³⁺: t₂g³ → 3 unpaired", "Fe³⁺ (low spin): t₂g⁵ → 1 unpaired",
       "Total = 4"],
      why_others_wrong="3 treats the anion as [Fe(CN)₆]⁴⁻ with diamagnetic Fe²⁺ (charge does not balance); 5 counts "
                       "only a high-spin Fe³⁺; 8 adds a high-spin Fe³⁺ (5) to Cr³⁺ (3).",
      ncert=f"{NC12}, 'Coordination Compounds', crystal field theory; magnetic properties", seconds=75),

    Q(T_CC, "Valence bond theory", "Advanced", "direct",
      "Which pair of complexes has the same number of unpaired electrons AND the same type of hybridisation of the "
      "central atom, according to valence bond theory? ([Fe(H₂O)₆]²⁺ is a high-spin complex; atomic numbers: Cr 24, "
      "Mn 25, Fe 26, Co 27, Ni 28.)",
      ["[Ni(CN)₄]²⁻ and [Ni(CO)₄]", "[Fe(CN)₆]³⁻ and [Mn(CN)₆]³⁻", "[CoF₆]³⁻ and [Fe(H₂O)₆]²⁺",
       "[Cr(NH₃)₆]³⁺ and [Co(NH₃)₆]³⁺"], "C",
      "Comparing hybridisation and magnetic moments",
      "Co³⁺ and Fe²⁺ are both 3d⁶. With the weak field ligands F⁻ and H₂O, both keep four unpaired electrons and "
      "use outer 4d orbitals: sp³d², octahedral, four unpaired electrons each.",
      ["[CoF₆]³⁻: 3d⁶, 4 unpaired, sp³d²", "[Fe(H₂O)₆]²⁺: 3d⁶, 4 unpaired, sp³d²",
       "Other pairs differ in one of the two properties"],
      why_others_wrong="[Ni(CN)₄]²⁻ (dsp²) and [Ni(CO)₄] (sp³) are both diamagnetic but differently hybridised; "
                       "[Fe(CN)₆]³⁻ (1 unpaired) and [Mn(CN)₆]³⁻ (2 unpaired) are both d²sp³; [Cr(NH₃)₆]³⁺ (3) and "
                       "[Co(NH₃)₆]³⁺ (0) are both d²sp³.",
      ncert=f"{NC12}, 'Coordination Compounds', valence bond theory", seconds=90),

    Q(T_CC, "Valence bond theory", "Advanced", "assertion_reason",
      *ar("[Co(C₂O₄)₃]³⁻ is an outer orbital (sp³d²) complex with four unpaired electrons (Z of Co = 27).", False,
          "In the spectrochemical series, the oxalate ion lies before water, i.e. it is a weaker field ligand than "
          "water.", True),
      "Spin state of cobalt(III) complexes",
      "NCERT reports [Co(C₂O₄)₃]³⁻ as diamagnetic: the six 3d electrons of Co³⁺ are paired, and cobalt uses d²sp³ "
      "hybrid orbitals (inner orbital complex). So A is false. R is true: in the spectrochemical series "
      "C₂O₄²⁻ < H₂O. Even so, Co³⁺ (high charge) gives a splitting large enough for pairing with oxalate.",
      ["A: false; [Co(C₂O₄)₃]³⁻ is diamagnetic, d²sp³", "R: true (… C₂O₄²⁻ < H₂O < NCS⁻ …)"],
      ncert=f"{NC12}, 'Coordination Compounds', magnetic properties; spectrochemical series", seconds=60),

    Q(T_CC, "Crystal field theory", "Advanced", "multi_statement",
      *ms("Ignoring pairing energy, and taking the energy of each t₂g electron as −0.4Δo and of each eg electron as "
          "+0.6Δo in an octahedral field, which of the following statements are correct?",
          [("For high-spin [Fe(H₂O)₆]³⁺ (t₂g³ eg²), the crystal field stabilisation energy (CFSE) is zero.", True),
           ("A d¹⁰ ion such as Zn²⁺ has zero CFSE in an octahedral field.", True),
           ("A high-spin d⁴ octahedral complex has a CFSE of −0.6Δo.", True),
           ("A low-spin d⁵ octahedral complex has a CFSE of −2.4Δo.", False),
           ("For the same Δo, the magnitude of the CFSE of a high-spin d⁵ ion is larger than that of a high-spin d⁴ "
            "ion.", False)],
          [["a", "c", "d"], ["b", "d", "e"], ["a", "b", "c", "d"]], "A"),
      "Calculating CFSE",
      "CFSE = −0.4Δo × (t₂g electrons) + 0.6Δo × (eg electrons).",
      ["(a) t₂g³ eg²: −1.2 + 1.2 = 0 → true", "(b) t₂g⁶ eg⁴: −2.4 + 2.4 = 0 → true",
       "(c) t₂g³ eg¹: −1.2 + 0.6 = −0.6Δo → true", "(d) t₂g⁵: −2.0Δo, not −2.4Δo → false",
       "(e) high-spin d⁵ has 0, high-spin d⁴ has −0.6Δo → false"],
      why_others_wrong="Options containing (d) use the low-spin d⁶ value for d⁵; the option with (e) reverses the "
                       "comparison; (b), (d) and (e) misses two correct statements.",
      ncert=f"{NC12}, 'Coordination Compounds', crystal field splitting in octahedral complexes", seconds=90),
]

# ================================================================ Purification and Characterisation (2389-2395)
# 2389: Kjeldahl works for urea, ethanamide, aniline; not for nitro, ring N (pyridine), azo
kj_2389 = {"urea": True, "ethanamide": True, "aniline": True, "nitrobenzene": False, "pyridine": False,
           "azobenzene": False}
v_2389 = str(sum(kj_2389.values()))
assert v_2389 == "3"
# 2391: Dumas on 0.30 g urea, CO(NH2)2: 1 mol urea -> 1 mol N2 -> 22400 mL at STP
M_urea = mm(C=1, H=4, N=2, O=1)
assert M_urea == 60
v_2391_n = F(30, 100) / M_urea * 22400
assert v_2391_n == 112
v_2391 = "112 mL"
# 2392: Carius on 0.239 g CHCl3 (119.5) -> 3 AgCl (143.5) per molecule
M_chcl3 = mm(C=1, H=1, Cl=3)
M_agcl = AM["Ag"] + AM["Cl"]
assert M_chcl3 == F(1195, 10) and M_agcl == F(1435, 10)
m_2392 = F(239, 1000) / M_chcl3 * 3 * M_agcl
assert m_2392 == F(861, 1000)
v_2392 = "0.861 g"
# 2394: Carius on 0.259 g CH2BrCl (129.5) -> AgCl + AgBr
M_cbc = mm(C=1, H=2, Br=1, Cl=1)
assert M_cbc == F(1295, 10)
n_2394 = F(259, 1000) / M_cbc
m_2394 = n_2394 * (M_agcl + AM["Ag"] + AM["Br"])
assert n_2394 == F(2, 1000) and m_2394 == F(663, 1000)
v_2394 = "0.663 g"

QUESTIONS += [
    N(T_PU, "Quantitative analysis and formulae", "Basic",
      "Kjeldahl's method is to be used to estimate nitrogen. For how many of the following compounds is the method "
      "applicable?\nUrea, ethanamide (CH₃CONH₂), aniline, nitrobenzene, pyridine, azobenzene (C₆H₅–N=N–C₆H₅)",
      ["2", v_2389, "4", "6"], "B", v_2389,
      "Limitation of Kjeldahl's method",
      "In Kjeldahl's method the nitrogen is converted into ammonium sulphate by heating with concentrated H₂SO₄. "
      "The method is not applicable to compounds containing nitrogen in nitro and azo groups or in a ring (such as "
      "pyridine), because their nitrogen does not change to ammonium sulphate under these conditions.",
      ["Applicable: urea, ethanamide, aniline (3)", "Not applicable: nitrobenzene (nitro), pyridine (ring N), "
       "azobenzene (azo)"],
      why_others_wrong="2 usually leaves out aniline, whose –NH₂ nitrogen is converted normally; 4 or 6 forget the "
                       "NCERT exclusions for nitro, azo and ring nitrogen.",
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', estimation of nitrogen: "
            "Kjeldahl's method", seconds=40),

    Q(T_PU, "Purification methods", "Basic", "direct",
      "In differential extraction, if the organic compound is only slightly soluble in the organic solvent, a very "
      "large quantity of solvent would be needed to extract even a small quantity of the compound. The technique "
      "used in such cases, in which the same solvent is used repeatedly for extraction, is:",
      ["Simple distillation", "Steam distillation", "Sublimation", "Continuous extraction"], "D",
      "Differential extraction",
      "NCERT: when the compound is less soluble in the organic solvent, the technique of continuous extraction is "
      "employed, in which the same solvent is repeatedly used for extraction of the compound.",
      ["Low solubility in the organic solvent → large volume needed",
       "Solution: re-use the same solvent repeatedly → continuous extraction"],
      why_others_wrong="Simple and steam distillation separate liquids by volatility; sublimation separates a "
                       "sublimable solid from a non-sublimable one. None of them reuses an extracting solvent.",
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', differential extraction",
      seconds=30),

    N(T_PU, "Quantitative analysis and formulae", "Intermediate",
      "If 0.30 g of urea, CO(NH₂)₂, were analysed by Dumas' method, the volume of nitrogen gas collected, corrected "
      "to STP, would be (C = 12, H = 1, N = 14, O = 16; molar volume at STP = 22400 mL):",
      ["56 mL", v_2391, "224 mL", "448 mL"], "B", v_2391,
      "Dumas' method: all nitrogen is collected as N₂",
      "In Dumas' method the nitrogen of the compound is set free as N₂ gas. One molecule of urea has two nitrogen "
      "atoms, which give one molecule of N₂.",
      ["Urea: 0.30 / 60 = 0.0050 mol", "N₂ formed = 0.0050 mol (2 N per urea → 1 N₂)",
       "Volume = 0.0050 × 22400 = 112 mL"],
      why_others_wrong="56 mL treats urea as having one nitrogen atom; 224 mL counts one N₂ per nitrogen atom; "
                       "448 mL also doubles the moles of urea.",
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', estimation of nitrogen: Dumas "
            "method", seconds=50),

    N(T_PU, "Quantitative analysis and formulae", "Intermediate",
      "0.239 g of chloroform, CHCl₃, is analysed by the Carius method. Assuming that all its chlorine is converted "
      "into silver chloride, the mass of AgCl obtained is (C = 12, H = 1, Cl = 35.5, Ag = 108):",
      ["0.287 g", "0.574 g", v_2392, "1.148 g"], "C", v_2392,
      "Carius method: halogen → silver halide",
      "In the Carius method the halogen of the compound is converted into silver halide. Each molecule of CHCl₃ "
      "gives three molecules of AgCl.",
      ["CHCl₃: 0.239 / 119.5 = 0.0020 mol", "AgCl: 3 × 0.0020 = 0.0060 mol",
       "Mass = 0.0060 × 143.5 = 0.861 g"],
      why_others_wrong="0.287 g counts one chlorine atom per molecule and 0.574 g two; 1.148 g counts four, as for "
                       "CCl₄.",
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', estimation of halogens: Carius "
            "method", seconds=50),

    Q(T_PU, "Quantitative analysis and formulae", "Intermediate", "match_list",
      *ml("Match the method of quantitative estimation in List-I with the quantity that is finally measured in "
          "List-II.",
          ["Dumas' method for nitrogen", "Kjeldahl's method for nitrogen", "Carius method for halogens",
           "Carius method for sulphur"],
          ["Volume of nitrogen gas collected over aqueous KOH", "Mass of barium sulphate",
           "Amount of ammonia absorbed in a known volume of standard acid", "Mass of silver halide"],
          "I III IV II", ["III I IV II", "I III II IV", "IV III I II"], "A"),
      "Principles of quantitative estimation",
      "Dumas: nitrogen is collected as N₂ gas over KOH solution. Kjeldahl: nitrogen is converted to ammonium "
      "sulphate, the ammonia set free by alkali is absorbed in standard acid, and the unused acid is titrated. "
      "Carius: halogen is weighed as silver halide; sulphur is oxidised to sulphuric acid and weighed as barium "
      "sulphate.",
      ["Dumas → N₂ volume", "Kjeldahl → NH₃ in standard acid", "Carius (X) → AgX mass", "Carius (S) → BaSO₄ mass"],
      why_others_wrong="Codes that swap Dumas and Kjeldahl confuse gas collection with acid absorption; codes that "
                       "swap the two Carius estimations give sulphur as the silver salt.",
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', quantitative analysis", seconds=45),

    N(T_PU, "Quantitative analysis and formulae", "Advanced",
      "0.259 g of bromochloromethane, CH₂BrCl, is heated with fuming nitric acid and silver nitrate in a Carius "
      "tube. Assuming complete conversion of both halogens, the total mass of the silver halide precipitate is "
      "(C = 12, H = 1, Cl = 35.5, Br = 80, Ag = 108):",
      ["0.574 g", v_2394, "0.752 g", "1.326 g"], "B", v_2394,
      "Carius method with two halogens",
      "Each molecule of CH₂BrCl gives one AgCl and one AgBr. The precipitate is a mixture of the two silver halides.",
      ["CH₂BrCl: 0.259 / 129.5 = 0.0020 mol", "AgCl: 0.0020 × 143.5 = 0.287 g",
       "AgBr: 0.0020 × 188 = 0.376 g", "Total = 0.663 g"],
      why_others_wrong="0.574 g treats both halogens as chlorine and 0.752 g both as bromine; 1.326 g doubles the "
                       "moles of compound.",
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', estimation of halogens: Carius "
            "method", seconds=80),

    Q(T_PU, "Purification methods", "Advanced", "assertion_reason",
      *ar("In fractional distillation, the vapour that reaches the top of the fractionating column is richer in the "
          "more volatile component.", True,
          "The fractionating column provides many surfaces for heat exchange between the ascending vapours and the "
          "descending condensed liquid, so at each stage part of the less volatile component condenses and returns "
          "towards the flask.", True, explains=True),
      "Fractional distillation",
      "NCERT: the fractionating column provides many surfaces for heat exchange between the ascending vapours and "
      "the descending condensed liquid. Some of the condensing liquid takes heat from the rising vapours and "
      "vaporises, so the vapours become richer in the low-boiling component. Each such condensation and "
      "vaporisation unit is a theoretical plate. R is the reason for A.",
      ["Repeated condensation and vaporisation along the column",
       "Less volatile component condenses and runs back; vapour at the top is enriched in the more volatile one"],
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', fractional distillation",
      seconds=50),
]

# ================================================================ Some Basic Principles of Organic Chemistry (2396-2415)
# 2396: benzenoid aromatic compounds (contain a benzene ring)
bz_2396 = {"benzene": True, "toluene": True, "naphthalene": True, "pyridine": False, "furan": False,
           "cyclohexane": False, "tropolone": False}
v_2396 = str(sum(bz_2396.values()))
assert v_2396 == "3"
# 2411: functional group isomers of propanoic acid (C3H6O2) = same formula, different functional group
f_2411 = {"methyl ethanoate": (mm(C=3, H=6, O=2), True), "ethyl methanoate": (mm(C=3, H=6, O=2), True),
          "propanal": (mm(C=3, H=6, O=1), False), "2-hydroxypropanal": (mm(C=3, H=6, O=2), True),
          "ethanoic acid": (mm(C=2, H=4, O=2), False), "propan-1-ol": (mm(C=3, H=8, O=1), False),
          "propane-1,2-diol": (mm(C=3, H=8, O=2), False)}
target = mm(C=3, H=6, O=2)
assert all((m == target) == iso for m, iso in f_2411.values())  # every C3H6O2 compound listed is not an acid
v_2411 = str(sum(1 for m, iso in f_2411.values() if iso))
assert v_2411 == "3"

QUESTIONS += [
    N(T_GO, "Hybridisation and functional groups", "Basic",
      "Aromatic compounds that contain one or more benzene rings are called benzenoid aromatic compounds. How many of "
      "the following are benzenoid aromatic compounds?\n"
      "Benzene, toluene, naphthalene, pyridine, furan, cyclohexane, tropolone",
      ["2", v_2396, "4", "5"], "B", v_2396,
      "Classification of cyclic compounds",
      "Benzenoid aromatic compounds contain a benzene ring: benzene, toluene and naphthalene (two fused benzene "
      "rings). Pyridine and furan are heterocyclic aromatic compounds, tropolone is a non-benzenoid aromatic "
      "compound and cyclohexane is alicyclic.",
      ["Benzenoid: benzene, toluene, naphthalene → 3",
       "Not benzenoid: pyridine, furan (heterocyclic), tropolone (non-benzenoid), cyclohexane (alicyclic)"],
      why_others_wrong="2 leaves out naphthalene, whose fused rings are both benzene rings; 4 or 5 count pyridine or "
                       "tropolone, which are aromatic but not benzenoid.",
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', classification of organic "
            "compounds", seconds=35),

    Q(T_GO, "Hybridisation and functional groups", "Basic", "direct",
      "In ketene, CH₂=C=O, the hybridisation states of the CH₂ carbon and of the central carbon are, respectively:",
      ["sp and sp²", "sp² and sp²", "sp³ and sp", "sp² and sp"], "D",
      "Hybridisation from the number of σ bonds and π bonds",
      "The CH₂ carbon forms three σ bonds (two C–H, one C–C) and one π bond: sp². The central carbon forms two "
      "double bonds (two σ and two π bonds): sp, like the central carbon of an allene.",
      ["CH₂ carbon: 3 σ + 1 π → sp²", "Central carbon: 2 σ + 2 π → sp"],
      why_others_wrong="sp and sp² reverses the two carbons; sp² for the central carbon ignores its second π bond; "
                       "sp³ would need four σ bonds and no π bond.",
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', shapes of carbon compounds",
      seconds=30),

    Q(T_GO, "IUPAC nomenclature", "Basic", "direct",
      "The IUPAC name of CH₃–C(CH₃)=CH–CH₂–CH₃ is:",
      ["4-Methylpent-3-ene", "2-Methylpent-2-ene", "2-Methylpent-3-ene", "4-Methylpent-2-ene"], "B",
      "Naming an alkene",
      "The longest chain containing the double bond has five carbons. It is numbered from the end nearer the double "
      "bond, so the double bond starts at C-2 and the methyl group is on C-2.",
      ["Parent: pentene; number from the left: C1–C2(=C3)", "Double bond at 2, methyl at 2 → 2-methylpent-2-ene"],
      why_others_wrong="4-Methylpent-3-ene and 2-methylpent-3-ene number the chain from the wrong end, giving the "
                       "double bond a higher locant; 4-methylpent-2-ene is a different compound, "
                       "CH₃–CH=CH–CH(CH₃)–CH₃.",
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', IUPAC nomenclature", seconds=30),

    Q(T_GO, "Hybridisation and functional groups", "Basic", "statement_pair",
      *sp("The members of a homologous series can be represented by a general formula, and successive members "
          "differ from each other by a –CH₂– unit.", True,
          "Alicyclic compounds, such as cyclohexane, show some properties similar to those of aliphatic compounds.",
          True),
      "Homologous series; alicyclic compounds",
      "A homologous series is a group of compounds with the same functional group, represented by a general "
      "formula, in which successive members differ by –CH₂–. NCERT notes that alicyclic (closed-chain, non-aromatic) "
      "compounds exhibit some properties similar to those of aliphatic compounds.",
      ["Statement I: true", "Statement II: true"],
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', classification of organic "
            "compounds", seconds=30),

    Q(T_GO, "Reactive intermediates", "Basic", "assertion_reason",
      *ar("Alkyl free radicals are highly reactive species.", True,
          "The carbon atom of an alkyl free radical carries an unpaired electron and has only seven electrons in its "
          "valence shell, so it readily reacts to pair up this electron.", True, explains=True),
      "Free radicals as reactive intermediates",
      "Homolytic cleavage gives free radicals, in which a carbon atom carries an unpaired electron. With an "
      "incomplete octet, the radical reacts at once (for example with Cl₂ or another radical) to pair the "
      "electron, so free radicals are short-lived, highly reactive intermediates. R explains A.",
      ["A: true (reactive intermediate)", "R: true; the unpaired electron/incomplete octet is the cause"],
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', homolytic cleavage; free radicals",
      seconds=35),

    Q(T_GO, "Hybridisation and functional groups", "Basic", "match_list",
      *ml("Match the compound in List-I with its next higher homologue in List-II.",
          ["Methanal, HCHO", "Propanone, CH₃COCH₃", "Methanoic acid, HCOOH", "Methanamine, CH₃NH₂"],
          ["CH₃CH₂NH₂", "CH₃COOH", "CH₃COCH₂CH₃", "CH₃CHO"],
          "IV III II I", ["III IV II I", "IV III I II", "IV II III I"], "D"),
      "Homologous series",
      "The next higher homologue has the same functional group and one more –CH₂– unit.",
      ["HCHO → CH₃CHO", "CH₃COCH₃ → CH₃COCH₂CH₃", "HCOOH → CH₃COOH", "CH₃NH₂ → CH₃CH₂NH₂"],
      why_others_wrong="The other codes pair a compound with a member of a different series (for example an "
                       "aldehyde with a ketone), which has a different functional group.",
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', homologous series", seconds=30),

    Q(T_GO, "Isomerism", "Intermediate", "direct",
      "Which of the following shows geometrical (cis–trans) isomerism?",
      ["1-Chloroprop-1-ene, ClCH=CH–CH₃", "2-Chloroprop-1-ene, CH₂=CCl–CH₃", "3-Chloroprop-1-ene, CH₂=CH–CH₂Cl",
       "1,1-Dichloroprop-1-ene, Cl₂C=CH–CH₃"], "A",
      "Condition for geometrical isomerism",
      "Geometrical isomerism about a C=C bond needs each doubly bonded carbon to carry two different groups. In "
      "ClCH=CH–CH₃, C-1 has H and Cl and C-2 has H and CH₃.",
      ["ClCH=CHCH₃: both carbons carry two different groups → cis and trans",
       "Other three: one doubly bonded carbon carries two identical groups"],
      why_others_wrong="2-Chloro- and 3-chloroprop-1-ene have a =CH₂ end (two H atoms); 1,1-dichloroprop-1-ene has "
                       "two Cl atoms on the same carbon.",
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', stereoisomerism", seconds=40),

    Q(T_GO, "Reactive intermediates", "Intermediate", "direct",
      "In which of the following does heterolytic cleavage of the indicated bond normally leave the shared pair of "
      "electrons on carbon, giving a carbanion?",
      ["The C–Br bond of CH₃CH₂Br", "The C–O bond of protonated ethanol, CH₃CH₂–OH₂⁺",
       "The C–Mg bond of CH₃CH₂MgBr", "The C–Cl bond of (CH₃)₃C–Cl"], "C",
      "Direction of heterolysis",
      "In heterolysis the shared pair goes to the more electronegative atom. Carbon is more electronegative than "
      "magnesium, so in a Grignard reagent the polar C–Mg bond leaves the electron pair on carbon (carbanion "
      "character). With Br, O or Cl, the more electronegative atom takes the pair and a carbocation forms.",
      ["C–Mg: carbon is the more electronegative atom → carbanion",
       "C–Br, C–O, C–Cl: the heteroatom takes the pair → carbocation"],
      why_others_wrong="Bromoethane, protonated ethanol and tert-butyl chloride all lose an electronegative leaving "
                       "group with the bonding pair, leaving a positively charged carbon.",
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', heterolytic cleavage", seconds=45),

    Q(T_GO, "Electronic effects", "Intermediate", "assertion_reason",
      *ar("The C–O bond in CH₃–OH is more polar than the C–S bond in CH₃–SH.", True,
          "Sulphur is more electronegative than oxygen.", False),
      "Bond polarity and electronegativity",
      "Oxygen is more electronegative than sulphur, so the electronegativity difference, and hence the polarity, is "
      "greater for the C–O bond. A is true; R is false.",
      ["A: true", "R: false; electronegativity O > S"],
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', inductive effect; polarity of "
            "bonds", seconds=35),

    Q(T_GO, "Electronic effects", "Intermediate", "statement_pair",
      *sp("Hyperconjugation is possible in the methyl cation, CH₃⁺.", False,
          "Hyperconjugation is also possible in alkenes and alkylarenes.", True),
      "Hyperconjugation",
      "Hyperconjugation is the delocalisation of the σ electrons of a C–H bond of an alkyl group directly attached "
      "to an atom of an unsaturated system or to an atom with an unshared p orbital. CH₃⁺ has no alkyl group on the "
      "positive carbon (its own C–H bonds lie in the nodal plane of the empty p orbital), so it cannot be "
      "stabilised by hyperconjugation. NCERT notes hyperconjugation in alkenes (propene) and alkylarenes.",
      ["Statement I: false; no C–H bond adjacent to the cationic carbon", "Statement II: true"],
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', hyperconjugation", seconds=40),

    Q(T_GO, "Isomerism", "Intermediate", "match_list",
      *ml("Match the compound in List-I with the type of stereoisomerism it shows in List-II.",
          ["2-Chlorobutane", "Pent-2-ene", "4-Chloropent-2-ene, CH₃–CH=CH–CHCl–CH₃", "Propan-2-ol"],
          ["Both geometrical and optical isomerism", "Optical isomerism only", "Neither", "Geometrical isomerism only"],
          "II IV I III", ["IV II I III", "II IV III I", "I IV II III"], "B"),
      "Geometrical and optical isomerism",
      "Optical isomerism needs a carbon bonded to four different groups; geometrical isomerism needs two different "
      "groups on each doubly bonded carbon.",
      ["2-Chlorobutane: C-2 chiral, no C=C → optical only", "Pent-2-ene: cis/trans, no chiral carbon → geometrical only",
       "4-Chloropent-2-ene: cis/trans and chiral C-4 → both", "Propan-2-ol: C-2 has two CH₃ groups, no C=C → neither"],
      why_others_wrong="Codes that give pent-2-ene optical isomerism look for a chiral carbon that is not there; "
                       "codes that give propan-2-ol any isomerism overlook its two identical methyl groups.",
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', stereoisomerism", seconds=60),

    Q(T_GO, "Isomerism", "Intermediate", "multi_statement",
      *ms("Which of the following statements about structural isomerism are correct?",
          [("Butan-1-ol and 2-methylpropan-1-ol are chain isomers.", True),
           ("Propan-1-ol and propan-2-ol are position isomers.", True),
           ("Propanal and prop-2-en-1-ol (CH₂=CH–CH₂OH) are functional group isomers.", True),
           ("But-1-ene and 2-methylpropene are position isomers.", False),
           ("Methoxyethane and propan-2-ol are metamers.", False)],
          [["a", "b", "d"], ["b", "c", "e"], ["a", "b", "c", "d"]], "B"),
      "Chain, position and functional isomers; metamers",
      "Chain isomers differ in the carbon skeleton; position isomers differ in the position of the substituent or "
      "functional group on the same skeleton; functional isomers have different functional groups. Metamerism arises "
      "from different alkyl groups on either side of the same functional group.",
      ["(a) C₄H₁₀O, straight vs branched chain → true", "(b) –OH on C-1 vs C-2 → true",
       "(c) both C₃H₆O; aldehyde vs alcohol (with C=C) → true",
       "(d) straight vs branched skeleton → chain isomers, false",
       "(e) ether vs alcohol → functional isomers, not metamers, false"],
      why_others_wrong="Options with (d) mistake a change of skeleton for a change of position; the option with (e) "
                       "calls an ether–alcohol pair metamers, although metamers must share the functional group.",
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', structural isomerism", seconds=75),

    Q(T_GO, "Types of organic reactions", "Intermediate", "multi_statement",
      *ms("For the reaction CH₃CH₂Br + HS⁻ → CH₃CH₂SH + Br⁻, which of the following statements are correct?",
          [("HS⁻ acts as the nucleophile.", True),
           ("CH₃CH₂Br is the substrate.", True),
           ("Br⁻ is the leaving group.", True),
           ("The carbon atom attacked by HS⁻ carries a partial negative charge.", False),
           ("The reaction is a substitution reaction.", True)],
          [["a", "b", "c"], ["a", "d", "e"], ["b", "c", "d", "e"]], "D"),
      "Substrate, reagent and reaction type",
      "The substrate supplies the carbon to the new bond: here CH₃CH₂Br. The reagent HS⁻ brings an electron pair, "
      "so it is a nucleophile, and it attacks the carbon bonded to bromine, which carries a partial positive charge "
      "because Br is more electronegative. Br⁻ leaves, and one group replaces another: a substitution.",
      ["(a), (b), (c), (e) true", "(d) false: the C–Br carbon is δ+"],
      why_others_wrong="Options containing (d) reverse the polarity of the C–Br bond; (a), (b) and (c) only leaves out "
                       "the correct classification as substitution.",
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', substrate and reagent; types of "
            "organic reactions", seconds=60),

    Q(T_GO, "Hybridisation and functional groups", "Intermediate", "multi_statement",
      *ms("Which of the following statements about hybridisation and shape are correct?",
          [("In CH₃–C≡N, the carbon of the CH₃ group is sp³ and the nitrile carbon is sp hybridised.", True),
           ("In benzene, all six carbon atoms are sp² hybridised.", True),
           ("An sp² hybridised carbon is more electronegative than an sp³ hybridised carbon.", True),
           ("In propyne, CH₃–C≡CH, the C–C≡C bond angle is 120°.", False),
           ("In the carbocation (CH₃)₃C⁺, the positively charged carbon is sp³ hybridised.", False)],
          [["a", "b", "d"], ["b", "c", "e"], ["a", "c", "d", "e"]], "A"),
      "Hybridisation, electronegativity and bond angles",
      "A carbon with four σ bonds is sp³, with one π bond sp², and with two π bonds sp. Greater s character makes "
      "the carbon more electronegative (sp > sp² > sp³). The sp carbons of an alkyne are linear (180°). The positive "
      "carbon of a carbocation uses three sp² orbitals and has an empty p orbital.",
      ["(a) true", "(b) true", "(c) true (33% vs 25% s character)", "(d) false: 180°", "(e) false: sp²"],
      why_others_wrong="(d) uses the sp² angle for sp carbons; (e) gives a carbocation the hybridisation of a "
                       "carbanion; options containing either are wrong.",
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', hybridisation; carbocations",
      seconds=60),

    N(T_GO, "Isomerism", "Advanced",
      "How many of the following are functional group isomers of propanoic acid, CH₃CH₂COOH?\n"
      "Methyl ethanoate, ethyl methanoate, propanal, 2-hydroxypropanal (CH₃CH(OH)CHO), ethanoic acid, propan-1-ol, "
      "propane-1,2-diol",
      ["0", "1", "2", v_2411], "D", v_2411,
      "Functional group isomers: same molecular formula, different functional group",
      "Propanoic acid is C₃H₆O₂. A functional group isomer must have the same molecular formula but a different "
      "functional group. Check the formula of each compound first.",
      ["C₃H₆O₂: methyl ethanoate, ethyl methanoate (esters), 2-hydroxypropanal (aldehyde + alcohol) → isomers",
       "Propanal C₃H₆O, ethanoic acid C₂H₄O₂, propan-1-ol C₃H₈O, propane-1,2-diol C₃H₈O₂ → not isomers",
       "Count = 3"],
      why_others_wrong="2 counts only the two esters and misses the hydroxy aldehyde; lower counts also judge by "
                       "functional group alone without checking the molecular formula.",
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', functional group isomerism",
      seconds=75),

    Q(T_GO, "IUPAC nomenclature", "Advanced", "direct",
      "The IUPAC name of HOOC–CH₂–CH(OH)–CH₂–C≡N is:",
      ["3-Hydroxy-4-cyanobutanoic acid", "4-Cyano-3-hydroxybutanoic acid", "4-Cyano-3-hydroxypentanoic acid",
       "4-Carboxy-3-hydroxybutanenitrile"], "B",
      "Principal functional group, prefixes and alphabetical order",
      "–COOH ranks above –CN, so the compound is named as a butanoic acid (C-1 = COOH, chain of four carbons). The "
      "–C≡N group, cited as a prefix (cyano), is not counted in the parent chain. Prefixes are cited "
      "alphabetically: cyano before hydroxy.",
      ["Principal group –COOH → '-oic acid'; parent chain C1–C4 = butanoic acid",
       "Substituents: OH on C-3, CN on C-4", "Alphabetical: 4-cyano-3-hydroxybutanoic acid"],
      why_others_wrong="'3-Hydroxy-4-cyano' breaks the alphabetical order; 'pentanoic acid' counts the nitrile carbon "
                       "both in the chain and in the prefix; naming it as a nitrile ignores the higher priority of "
                       "–COOH.",
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', nomenclature of polyfunctional "
            "compounds", seconds=60),

    Q(T_GO, "Reactive intermediates", "Advanced", "assertion_reason",
      *ar("In the tert-butyl cation, (CH₃)₃C⁺, the positively charged carbon and the three carbon atoms attached to "
          "it lie in one plane.", True,
          "The tert-butyl cation is more stable than the isopropyl cation, (CH₃)₂CH⁺.", True, explains=False),
      "Shape and stability of carbocations",
      "The planarity comes from the sp² hybridisation of the positive carbon: its three σ bonds lie in one plane "
      "at 120°, with the vacant p orbital perpendicular to it. R is a true but separate property: tert-butyl is more "
      "stable than isopropyl because of more hyperconjugation and +I effect of three methyl groups. Stability does "
      "not decide the shape (the isopropyl cation is planar too).",
      ["A: true (sp², trigonal planar)", "R: true (3° > 2°)", "R does not explain the planar shape"],
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', carbocations", seconds=50),

    Q(T_GO, "Isomerism", "Advanced", "statement_pair",
      *sp("2,3-Dimethylbutane and 2,2-dimethylbutane are chain isomers.", True,
          "Pentan-2-one and 3-methylbutan-2-one are position isomers.", False),
      "Chain versus position isomers",
      "Both pairs are C₆H₁₄ and C₅H₁₀O isomers respectively. 2,3- and 2,2-dimethylbutane differ in the carbon "
      "skeleton, so they are chain isomers. Pentan-2-one (straight chain) and 3-methylbutan-2-one (branched chain) "
      "also differ in the skeleton, with the C=O at C-2 in both; they are chain isomers, not position isomers.",
      ["Statement I: true", "Statement II: false; different skeletons → chain isomers"],
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', structural isomerism", seconds=50),

    Q(T_GO, "IUPAC nomenclature", "Advanced", "match_list",
      *ml("Match the structure in List-I with its IUPAC name in List-II.",
          ["CH₂=CH–CH₂–C≡N", "HC≡C–CH₂–CH₂–OH", "CH₃–CO–CH₂–CHO", "HO–CH₂–CH₂–COO–CH₃"],
          ["Methyl 3-hydroxypropanoate", "3-Oxobutanal", "But-3-enenitrile", "But-3-yn-1-ol"],
          "III IV II I", ["III IV I II", "IV III II I", "II IV III I"], "A"),
      "Naming polyfunctional compounds",
      "The principal group decides the suffix and gets the lowest locant; the nitrile carbon is C-1 of the chain; "
      "the –CHO carbon is C-1 and a ketonic C=O is cited as 'oxo'; esters are named alkyl alkanoate.",
      ["CH₂=CH–CH₂–CN: C1 = CN, C=C at 3 → but-3-enenitrile",
       "HC≡C–CH₂–CH₂OH: C1 bears OH, C≡C at 3 → but-3-yn-1-ol",
       "CH₃COCH₂CHO: C1 = CHO, C=O at 3 → 3-oxobutanal",
       "HOCH₂CH₂COOCH₃: methyl ester of 3-hydroxypropanoic acid"],
      why_others_wrong="Codes that swap the ester and the oxo-aldehyde mistake a –COO– group for a ketone; codes "
                       "that swap the nitrile and the alkynol ignore which group carries C-1.",
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', IUPAC nomenclature", seconds=75),

    Q(T_GO, "Reactive intermediates", "Advanced", "multi_statement",
      *ms("Which of the following statements about carbocations are correct?",
          [("In CH₃CH₂⁺, the C–H bonds of the CH₃ group, not those on the positively charged carbon, take part in "
            "hyperconjugation.", True),
           ("The benzyl cation, C₆H₅CH₂⁺, is stabilised by delocalisation of its positive charge over the benzene "
            "ring.", True),
           ("The isopropyl cation, (CH₃)₂CH⁺, has six C–H bonds that can take part in hyperconjugation.", True),
           ("Carbocations behave as nucleophiles because they carry a positive charge.", False),
           ("The order of stability of carbocations is CH₃⁺ > CH₃CH₂⁺ > (CH₃)₂CH⁺.", False)],
          [["a", "b", "d"], ["c", "d", "e"], ["a", "b", "c", "e"]], "B"),
      "Stability and reactivity of carbocations",
      "Hyperconjugation uses C–H bonds on carbons adjacent to the positive carbon: three in CH₃CH₂⁺ and six in "
      "(CH₃)₂CH⁺. Benzylic and allylic carbocations are stabilised by resonance. Carbocations are electron "
      "deficient and act as electrophiles; their stability order is 3° > 2° > 1° > CH₃⁺.",
      ["(a) true", "(b) true", "(c) true: two CH₃ groups × 3 C–H", "(d) false: electrophiles",
       "(e) false: the order is reversed"],
      why_others_wrong="Options with (d) confuse electron-deficient species with nucleophiles; the option with (e) "
                       "reverses the stability order.",
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', carbocations; hyperconjugation; "
            "resonance", seconds=70),
]

# ================================================================ Hydrocarbons (2416-2431)
# 2416: C6H6 + SO3 (oleum) -> C6H5SO3H; 7.8 g benzene
M_bz = mm(C=6, H=6)
M_bsa = mm(C=6, H=6, S=1, O=3)
assert (M_bz, M_bsa) == (78, 158)
m_2416 = F(78, 10) / M_bz * M_bsa
assert m_2416 == F(158, 10)
v_2416 = "15.8 g"
assert F(1, 10) * mm(S=1, O=3) == 8 and F(1, 10) * mm(C=6, H=6, S=2, O=6) == F(238, 10)
# 2421: BrCH2CH2Br + Zn -> CH2=CH2 + ZnBr2; 18.8 g
M_dbe = mm(C=2, H=4, Br=2)
assert M_dbe == 188
V_2421 = F(188, 10) / M_dbe * F(224, 10)
assert V_2421 == F(224, 100)
v_2421 = "2.24 L"
# 2422: 0.10 mol CH4 -> 0.05 mol CH3Cl + 0.05 mol CH2Cl2; one HCl per H replaced
n_hcl = F(5, 100) * 1 + F(5, 100) * 2
assert n_hcl == F(15, 100)
v_2422 = "0.15 mol"
# 2427: 4.2 g propene -> 2-bromopropane (Markovnikov) -> Wurtz -> 2,3-dimethylbutane (C6H14)
n_prop = F(42, 10) / mm(C=3, H=6)
m_2427 = n_prop / 2 * mm(C=6, H=14)
assert n_prop == F(1, 10) and m_2427 == F(43, 10)
v_2427 = "2,3-Dimethylbutane, 4.3 g"
# 2428: alkenes giving the same product with HBr with and without peroxide = symmetrical alkenes
sym_2428 = {"ethene": True, "propene": False, "but-1-ene": False, "but-2-ene": True, "2-methylpropene": False,
            "cyclohexene": True, "2,3-dimethylbut-2-ene": True}
v_2428 = str(sum(sym_2428.values()))
assert v_2428 == "4"

QUESTIONS += [
    N(T_HC, "Electrophilic substitution", "Basic",
      "7.8 g of benzene is heated with fuming sulphuric acid (oleum) and is converted completely into "
      "benzenesulphonic acid, C₆H₅SO₃H. The mass of benzenesulphonic acid formed is (C = 12, H = 1, S = 32, O = 16):",
      ["8.0 g", v_2416, "7.8 g", "23.8 g"], "B", v_2416,
      "Sulphonation of benzene",
      "Benzene reacts with fuming sulphuric acid to give benzenesulphonic acid: C₆H₆ + SO₃ (H₂SO₄) → C₆H₅SO₃H. "
      "One mole of benzene gives one mole of product.",
      ["Benzene: 7.8 / 78 = 0.10 mol", "C₆H₅SO₃H: M = 158 g mol⁻¹", "Mass = 0.10 × 158 = 15.8 g"],
      why_others_wrong="8.0 g is the mass of SO₃ used; 7.8 g simply repeats the mass of benzene; 23.8 g is for a "
                       "disulphonic acid, C₆H₄(SO₃H)₂.",
      ncert=f"{NC11}, 'Hydrocarbons', electrophilic substitution reactions: sulphonation", seconds=40),

    Q(T_HC, "Alkanes and conformations", "Basic", "direct",
      "In the free radical chlorination of methane in light, which of the following is a chain propagation step?",
      ["Cl₂ → Cl• + Cl•", "Cl• + Cl• → Cl₂", "CH₃• + CH₃• → CH₃–CH₃", "CH₄ + Cl• → CH₃• + HCl"], "D",
      "Mechanism of halogenation of alkanes",
      "Initiation: homolysis of Cl₂ by light. Propagation: a chlorine radical abstracts H from methane to give a "
      "methyl radical and HCl; the methyl radical then reacts with Cl₂ to give CH₃Cl and a new chlorine radical. "
      "Termination: two radicals combine.",
      ["Cl₂ → 2Cl•: initiation", "CH₄ + Cl• → CH₃• + HCl: propagation (radical in, radical out)",
       "Radical + radical → molecule: termination"],
      why_others_wrong="Homolysis of Cl₂ starts the chain (initiation); Cl• + Cl• and CH₃• + CH₃• consume radicals "
                       "without forming new ones, so they end the chain (termination).",
      ncert=f"{NC11}, 'Hydrocarbons', alkanes: halogenation mechanism", seconds=30),

    Q(T_HC, "Alkanes and conformations", "Basic", "direct",
      "An aqueous solution of sodium propanoate, CH₃CH₂COONa, is electrolysed by Kolbe's electrolytic method. The "
      "hydrocarbon formed at the anode is:",
      ["Ethane", "Propane", "Butane", "Hexane"], "C",
      "Kolbe's electrolytic method",
      "In Kolbe's electrolysis 2RCOONa + 2H₂O → R–R + 2CO₂ + H₂ + 2NaOH. The alkyl groups of two carboxylate ions "
      "join after losing CO₂. With R = C₂H₅, the product is C₂H₅–C₂H₅, butane.",
      ["R = CH₃CH₂–", "R–R = CH₃CH₂–CH₂CH₃ = butane"],
      why_others_wrong="Ethane is formed from sodium ethanoate; propane would need the carboxyl carbon to stay in "
                       "the chain; hexane would need two propyl groups.",
      ncert=f"{NC11}, 'Hydrocarbons', preparation of alkanes from carboxylic acids", seconds=30),

    Q(T_HC, "Alkenes: addition and ozonolysis", "Basic", "assertion_reason",
      *ar("Ozonolysis is used to locate the position of the double bond in an alkene.", True,
          "On ozonolysis followed by treatment with zinc and water, the alkene is cleaved at the double bond, and "
          "each carbon that was part of the double bond becomes the carbon of a C=O group in the products.", True,
          explains=True),
      "Ozonolysis as a structural tool",
      "Because the molecule is cut exactly at the C=C bond and both doubly bonded carbons end up as carbonyl "
      "carbons, identifying the carbonyl products tells where the double bond was. R is the reason for A.",
      ["Alkene + O₃ → ozonide; Zn/H₂O → two carbonyl compounds",
       "Carbonyl carbons = former doubly bonded carbons → position of C=C"],
      ncert=f"{NC11}, 'Hydrocarbons', alkenes: ozonolysis", seconds=35),

    Q(T_HC, "Alkynes", "Basic", "statement_pair",
      *sp("Ethyne adds one molecule of HBr to give bromoethene, which adds a second molecule of HBr to give "
          "1,1-dibromoethane.", True,
          "Propyne, on hydration with dilute H₂SO₄ in the presence of Hg²⁺ ions, gives propanal.", False),
      "Addition reactions of alkynes",
      "HBr adds to ethyne first to give CH₂=CHBr; the second addition follows Markovnikov's rule, putting Br on the "
      "carbon that already carries Br: CH₃CHBr₂ (1,1-dibromoethane). Hydration of propyne also follows Markovnikov's "
      "rule: the enol CH₃C(OH)=CH₂ changes into propanone, not propanal.",
      ["Statement I: true", "Statement II: false; propyne → propanone"],
      ncert=f"{NC11}, 'Hydrocarbons', alkynes: addition of hydrogen halides and water", seconds=40),

    N(T_HC, "Alkenes: addition and ozonolysis", "Intermediate",
      "18.8 g of 1,2-dibromoethane is heated with zinc dust and is converted completely into ethene. The volume of "
      "ethene formed, measured at STP, is (C = 12, H = 1, Br = 80; molar volume at STP = 22.4 L mol⁻¹):",
      ["1.12 L", "4.48 L", "0.224 L", v_2421], "D", v_2421,
      "Dehalogenation of vicinal dihalides",
      "Vicinal dihalides lose both halogen atoms on heating with zinc: BrCH₂–CH₂Br + Zn → CH₂=CH₂ + ZnBr₂. One "
      "mole of dihalide gives one mole of ethene.",
      ["BrCH₂CH₂Br: M = 188 g mol⁻¹ → 18.8 / 188 = 0.10 mol", "Ethene: 0.10 mol × 22.4 = 2.24 L"],
      why_others_wrong="4.48 L assumes two moles of gas per mole of dihalide; 1.12 L halves the moles; 0.224 L "
                       "misplaces the decimal (0.01 mol).",
      ncert=f"{NC11}, 'Hydrocarbons', preparation of alkenes from vicinal dihalides", seconds=45),

    N(T_HC, "Alkanes and conformations", "Intermediate",
      "0.10 mol of methane is chlorinated in diffused sunlight, and the methane is converted completely into an "
      "equimolar mixture of CH₃Cl and CH₂Cl₂ only. The amount of HCl formed is:",
      ["0.10 mol", v_2422, "0.20 mol", "0.30 mol"], "B", v_2422,
      "Stoichiometry of free radical substitution",
      "Each hydrogen atom replaced by chlorine gives one molecule of HCl: CH₄ + Cl₂ → CH₃Cl + HCl and "
      "CH₄ + 2Cl₂ → CH₂Cl₂ + 2HCl.",
      ["Equimolar: 0.05 mol CH₃Cl + 0.05 mol CH₂Cl₂", "HCl = 0.05 × 1 + 0.05 × 2 = 0.15 mol"],
      why_others_wrong="0.10 mol counts one HCl per methane; 0.20 mol counts two for every methane; 0.30 mol counts "
                       "the chlorine atoms used (0.15 mol Cl₂ = 0.30 mol Cl) instead of the HCl formed.",
      ncert=f"{NC11}, 'Hydrocarbons', alkanes: substitution reactions (halogenation)", seconds=50),

    Q(T_HC, "Benzene and aromaticity", "Intermediate", "statement_pair",
      *sp("With chlorine in the presence of ultraviolet light, benzene gives hexachlorobenzene, C₆Cl₆, by "
          "substitution.", False,
          "With an excess of chlorine in the presence of anhydrous AlCl₃ in the dark, benzene can be converted into "
          "hexachlorobenzene.", True),
      "Substitution versus addition in benzene",
      "In UV light benzene adds three molecules of chlorine to give benzene hexachloride, C₆H₆Cl₆ (an addition "
      "product), not hexachlorobenzene. With a Lewis acid and an excess of the electrophilic reagent, substitution "
      "continues until all six hydrogens are replaced: C₆H₆ + 6Cl₂ → C₆Cl₆ + 6HCl.",
      ["Statement I: false; UV light → C₆H₆Cl₆ by addition",
       "Statement II: true; excess Cl₂ / anhydrous AlCl₃ → C₆Cl₆ by substitution"],
      ncert=f"{NC11}, 'Hydrocarbons', aromatic hydrocarbons: chemical properties", seconds=45),

    Q(T_HC, "Alkenes: addition and ozonolysis", "Intermediate", "match_list",
      *ml("Match the conversion in List-I with the catalyst or conditions used for it in List-II.",
          ["Hydrogenation of an alkene to an alkane", "Partial hydrogenation of an alkyne to a cis-alkene",
           "Hydration of ethyne to ethanal", "Conversion of n-hexane into benzene"],
          ["Hg²⁺ ions in dilute H₂SO₄ at 333 K", "Cr₂O₃ supported on alumina at 773 K and 10–20 atm",
           "Palladium on charcoal partly deactivated with quinoline", "Finely divided Pt, Pd or Ni"],
          "IV III I II", ["III IV I II", "IV III II I", "I III IV II"], "C"),
      "Catalysts in hydrocarbon reactions",
      "Alkenes and alkynes are hydrogenated completely over finely divided Pt, Pd or Ni; Lindlar's catalyst (Pd on "
      "charcoal deactivated with quinoline) stops the reduction of an alkyne at the cis-alkene; alkynes are hydrated "
      "with Hg²⁺/dilute H₂SO₄ at 333 K; n-hexane is aromatised over Cr₂O₃ (or V₂O₅, Mo₂O₃) on alumina at 773 K.",
      ["A → IV", "B → III", "C → I", "D → II"],
      why_others_wrong="Codes that swap the two palladium/nickel catalysts would reduce an alkyne fully or stop an "
                       "alkene reaction; codes that swap hydration and aromatisation mix up the mercury catalyst with "
                       "the oxide catalyst.",
      ncert=f"{NC11}, 'Hydrocarbons', preparation and properties of alkanes, alkenes and alkynes", seconds=50),

    Q(T_HC, "Electrophilic substitution", "Intermediate", "multi_statement",
      *ms("Which of the following statements about substituents on a benzene ring in electrophilic substitution are "
          "correct?",
          [("The –COOR group is meta directing.", True),
           ("The –NHCOCH₃ group is ortho and para directing.", True),
           ("The –SO₃H group is ortho and para directing.", False),
           ("The –CN group deactivates the benzene ring.", True),
           ("The –Br group activates the benzene ring.", False)],
          [["a", "b", "c"], ["b", "d", "e"], ["a", "b", "d", "e"]], "D"),
      "Directive influence of functional groups",
      "Ortho/para directors: –OH, –NH₂, –NHR, –NHCOCH₃, –OCH₃, –CH₃ and halogens. Meta directors (deactivating): "
      "–NO₂, –CN, –CHO, –COR, –COOH, –COOR, –SO₃H. Halogens are ortho/para directing but deactivate the ring because "
      "of their strong −I effect.",
      ["(a) true", "(b) true", "(c) false: –SO₃H is meta directing", "(d) true", "(e) false: halogens deactivate"],
      why_others_wrong="Options with (c) treat –SO₃H as an electron-releasing group; options with (e) confuse the "
                       "ortho/para direction of halogens with activation.",
      ncert=f"{NC11}, 'Hydrocarbons', directive influence of a functional group in monosubstituted benzene",
      seconds=60),

    Q(T_HC, "Alkenes: addition and ozonolysis", "Intermediate", "assertion_reason",
      *ar("The peroxide effect is not observed when HCl adds to propene.", True,
          "The H–Cl bond is weaker than the H–Br bond, so HCl is readily cleaved by free radicals.", False),
      "Why only HBr shows the peroxide effect",
      "NCERT explains that the H–Cl bond (430.5 kJ mol⁻¹) is stronger than the H–Br bond (363.7 kJ mol⁻¹) and is "
      "not cleaved by the free radicals formed from the peroxide. So A is true and R, which reverses the bond "
      "strengths, is false.",
      ["A: true", "R: false; H–Cl is stronger than H–Br"],
      ncert=f"{NC11}, 'Hydrocarbons', alkenes: anti-Markovnikov addition (peroxide effect)", seconds=40),

    N(T_HC, "Alkenes: addition and ozonolysis", "Advanced",
      "4.2 g of propene is treated with HBr in the absence of peroxide, and the product is heated with sodium in dry "
      "ether. Assuming every step is complete, the final hydrocarbon and its mass are (C = 12, H = 1, Br = 80):",
      ["n-Hexane, 4.3 g", v_2427, "2,3-Dimethylbutane, 8.6 g", "n-Hexane, 8.6 g"], "B", v_2427,
      "Markovnikov addition followed by the Wurtz reaction",
      "Without peroxide, HBr adds by Markovnikov's rule to give 2-bromopropane. In the Wurtz reaction two "
      "isopropyl groups join: (CH₃)₂CH–CH(CH₃)₂, 2,3-dimethylbutane. Two moles of alkyl halide give one mole of "
      "alkane.",
      ["Propene: 4.2 / 42 = 0.10 mol → 0.10 mol (CH₃)₂CHBr",
       "Wurtz: 0.10 mol RBr → 0.05 mol R–R", "C₆H₁₄: 0.05 × 86 = 4.3 g of 2,3-dimethylbutane"],
      why_others_wrong="n-Hexane would come from 1-bromopropane (peroxide addition); 8.6 g forgets that two "
                       "molecules of alkyl halide give one molecule of alkane.",
      ncert=f"{NC11}, 'Hydrocarbons', Markovnikov rule; Wurtz reaction", seconds=80),

    N(T_HC, "Alkenes: addition and ozonolysis", "Advanced",
      "HBr is added to each of the following alkenes, once in the absence and once in the presence of benzoyl "
      "peroxide. For how many of them is the main product the same in both cases?\n"
      "Ethene, propene, but-1-ene, but-2-ene, 2-methylpropene, cyclohexene, 2,3-dimethylbut-2-ene",
      ["1", "2", "3", v_2428], "D", v_2428,
      "Peroxide effect matters only for unsymmetrical alkenes",
      "Markovnikov and anti-Markovnikov additions give different products only when the two doubly bonded carbons "
      "are differently substituted. For a symmetrical alkene, Br goes to an equivalent carbon either way.",
      ["Symmetrical: ethene, but-2-ene, cyclohexene, 2,3-dimethylbut-2-ene → same product (4)",
       "Unsymmetrical: propene, but-1-ene, 2-methylpropene → different products"],
      why_others_wrong="Lower counts usually leave out cyclohexene or 2,3-dimethylbut-2-ene, whose doubly bonded "
                       "carbons are equivalent even though the molecules are not straight chains.",
      ncert=f"{NC11}, 'Hydrocarbons', alkenes: addition of hydrogen halides", seconds=60),

    Q(T_HC, "Electrophilic substitution", "Advanced", "direct",
      "m-Bromonitrobenzene is to be prepared from benzene as the main product, using Br₂/FeBr₃ and a mixture of "
      "concentrated HNO₃ and H₂SO₄. The correct sequence is:",
      ["Nitration first, then bromination", "Bromination first, then nitration",
       "Either order, as both give the same main product", "Both reagents together in a single step"], "A",
      "Using directive influence in synthesis",
      "The –NO₂ group is meta directing, so brominating nitrobenzene puts Br at the meta position. Bromine is "
      "ortho/para directing, so nitrating bromobenzene would give mainly o- and p-bromonitrobenzene.",
      ["C₆H₆ → (HNO₃/H₂SO₄) C₆H₅NO₂", "C₆H₅NO₂ → (Br₂/FeBr₃) m-BrC₆H₄NO₂"],
      why_others_wrong="Bromination first gives ortho and para products; the order matters because the first group "
                       "directs the second; a one-step mixture gives no control over position.",
      ncert=f"{NC11}, 'Hydrocarbons', directive influence of a functional group in monosubstituted benzene",
      seconds=50),

    Q(T_HC, "Alkenes: addition and ozonolysis", "Advanced", "match_list",
      *ml("Each alkene in List-I is hydrated with water in the presence of an acid. Match it with its main product "
          "in List-II.",
          ["Propene", "2-Methylpropene", "But-1-ene", "Ethene"],
          ["Ethanol", "Butan-2-ol", "Propan-2-ol", "2-Methylpropan-2-ol"],
          "III IV II I", ["III IV I II", "IV III II I", "II IV III I"], "D"),
      "Markovnikov addition of water",
      "Acid-catalysed hydration goes through the more stable carbocation, so the –OH ends up on the more "
      "substituted carbon of the double bond (Markovnikov's rule).",
      ["Propene → (CH₃)₂CH⁺ → propan-2-ol", "2-Methylpropene → (CH₃)₃C⁺ → 2-methylpropan-2-ol",
       "But-1-ene → CH₃CH₂CH⁺CH₃ → butan-2-ol", "Ethene → ethanol"],
      why_others_wrong="The other codes give an alcohol whose carbon skeleton differs from that of the alkene (for "
                       "example ethene → butan-2-ol or propene → 2-methylpropan-2-ol); the trap in this set is "
                       "but-1-ene, which gives butan-2-ol, not butan-1-ol.",
      ncert=f"{NC11}, 'Hydrocarbons', alkenes: addition of water", seconds=50),

    Q(T_HC, "Alkenes: addition and ozonolysis", "Advanced", "multi_statement",
      *ms("Which of the following statements about the addition of HBr to propene are correct?",
          [("In the absence of peroxide, the first step is the attack of H⁺, an electrophile, on the double bond.",
            True),
           ("Protonation at C-1 gives a secondary carbocation, which is formed in preference to the primary one.",
            True),
           ("In the second step, Br⁻ attacks the carbocation.", True),
           ("In the presence of a peroxide, a bromine free radical adds first to C-1, giving the more stable "
            "secondary free radical.", True),
           ("The addition in the presence of a peroxide proceeds through a carbocation intermediate.", False)],
          [["a", "b", "c"], ["a", "c", "d", "e"], ["b", "d", "e"]], "A"),
      "Mechanisms of Markovnikov and anti-Markovnikov addition",
      "Ionic addition: H⁺ adds to C-1 to give the 2° carbocation CH₃CH⁺CH₃, which Br⁻ attacks → 2-bromopropane. "
      "Peroxide addition is a free radical chain: Br• adds to C-1, giving the 2° radical CH₃ĊHCH₂Br, which takes "
      "H from HBr → 1-bromopropane. No carbocation is involved in the peroxide reaction.",
      ["(a), (b), (c) true: ionic mechanism", "(d) true: free radical mechanism", "(e) false"],
      why_others_wrong="(a), (b) and (c) only misses the radical step; options with (e) attribute a carbocation to "
                       "the free radical pathway.",
      ncert=f"{NC11}, 'Hydrocarbons', alkenes: mechanism of addition of HBr", seconds=75),
]

# ================================================================ Organic Compounds Containing Halogens (2432-2444)
# 2432: (CH3)3COH + HCl -> (CH3)3CCl; 7.4 g alcohol
M_tbuoh = mm(C=4, H=10, O=1)
M_tbucl = mm(C=4, H=9, Cl=1)
assert M_tbuoh == 74 and M_tbucl == F(925, 10)
m_2432 = F(74, 10) / M_tbuoh * M_tbucl
assert m_2432 == F(925, 100)
v_2432 = "9.25 g"
assert F(1, 10) * mm(H=1, Cl=1) == F(365, 100) and F(1, 10) * mm(C=4, H=9, Br=1) == F(137, 10)
# 2436: C2H5OH + SOCl2 -> C2H5Cl + SO2(g) + HCl(g); 4.6 g ethanol
n_2436 = F(46, 10) / mm(C=2, H=6, O=1)
V_2436 = 2 * n_2436 * F(224, 10)
assert n_2436 == F(1, 10) and V_2436 == F(448, 100)
v_2436 = "4.48 L"
# 2437: Fittig 2 C6H5Cl + 2 Na -> C6H5-C6H5 + 2 NaCl; 11.25 g chlorobenzene
M_phcl = mm(C=6, H=5, Cl=1)
assert M_phcl == F(1125, 10)
m_2437 = F(1125, 100) / M_phcl / 2 * mm(C=12, H=10)
assert m_2437 == F(77, 10)
v_2437 = "7.7 g"
# 2441: structural isomers of C5H11Br classified as 1/2/3 degree
c5_2441 = {"1-bromopentane": 1, "2-bromopentane": 2, "3-bromopentane": 2, "1-bromo-2-methylbutane": 1,
           "2-bromo-2-methylbutane": 3, "2-bromo-3-methylbutane": 2, "1-bromo-3-methylbutane": 1,
           "1-bromo-2,2-dimethylpropane": 1}
assert len(c5_2441) == 8
v_2441 = str(sum(1 for d in c5_2441.values() if d == 2))
assert v_2441 == "3" and sum(1 for d in c5_2441.values() if d == 1) == 4

QUESTIONS += [
    N(T_HX, "C-X bond and preparation", "Basic",
      "7.4 g of 2-methylpropan-2-ol is shaken with concentrated hydrochloric acid at room temperature and is "
      "converted completely into 2-chloro-2-methylpropane. The mass of the alkyl chloride formed is (C = 12, H = 1, "
      "O = 16, Cl = 35.5):",
      ["3.65 g", "7.40 g", "13.7 g", v_2432], "D", v_2432,
      "Preparation of a tertiary alkyl chloride from an alcohol",
      "Tertiary alcohols react with concentrated HCl even at room temperature: (CH₃)₃C–OH + HCl → (CH₃)₃C–Cl + "
      "H₂O. One mole of alcohol gives one mole of alkyl chloride.",
      ["Alcohol: 7.4 / 74 = 0.10 mol", "(CH₃)₃CCl: M = 92.5 g mol⁻¹", "Mass = 0.10 × 92.5 = 9.25 g"],
      why_others_wrong="3.65 g is the mass of HCl consumed; 7.40 g repeats the mass of the alcohol; 13.7 g uses the "
                       "molar mass of the bromide, C₄H₉Br.",
      ncert=f"{NC12}, 'Haloalkanes and Haloarenes', preparation of haloalkanes from alcohols", seconds=40),

    Q(T_HX, "C-X bond and preparation", "Basic", "direct",
      "The IUPAC name of benzyl chloride, C₆H₅CH₂Cl, is:",
      ["1-Chloro-2-methylbenzene", "(Chloromethyl)benzene", "Chlorobenzene", "1-Chloro-4-methylbenzene"], "B",
      "Naming a benzylic halide",
      "In C₆H₅CH₂Cl the chlorine is on the side-chain carbon, not on the ring. The substituent –CH₂Cl on benzene "
      "is named chloromethyl, so the compound is (chloromethyl)benzene.",
      ["Cl on the CH₂ group attached to the ring", "Substituent –CH₂Cl = chloromethyl → (chloromethyl)benzene"],
      why_others_wrong="1-Chloro-2-methylbenzene and 1-chloro-4-methylbenzene are chlorotoluenes, with chlorine on the "
                       "ring; chlorobenzene, C₆H₅Cl, has no CH₂ group.",
      ncert=f"{NC12}, 'Haloalkanes and Haloarenes', nomenclature", seconds=25),

    Q(T_HX, "Polyhalogen compounds", "Basic", "statement_pair",
      *sp("Exposure to lower levels of dichloromethane in air can lead to slightly impaired hearing and vision.",
          True,
          "Exposure to carbon tetrachloride can make the heart beat irregularly or stop.", True),
      "Health effects of polyhalogen compounds",
      "NCERT notes that lower levels of methylene chloride in air can lead to slightly impaired hearing and vision, "
      "and that exposure to carbon tetrachloride can make the heart beat irregularly or stop (besides liver damage "
      "and effects on the nervous system).",
      ["Statement I: true", "Statement II: true"],
      ncert=f"{NC12}, 'Haloalkanes and Haloarenes', polyhalogen compounds: dichloromethane, tetrachloromethane",
      seconds=30),

    Q(T_HX, "SN1 and SN2", "Basic", "match_list",
      *ml("Match the reagent in List-I, reacting with a haloalkane R–X, with the main organic product in List-II.",
          ["A primary amine, R′NH₂", "Silver cyanide, AgCN", "Potassium nitrite, KNO₂",
           "Silver salt of a carboxylic acid, R′COOAg"],
          ["Alkyl nitrite, R–O–N=O", "Isocyanide, R–NC", "Ester, R′COOR", "Secondary amine, R–NH–R′"],
          "IV II I III", ["II IV I III", "IV II III I", "IV I II III"], "B"),
      "Nucleophilic substitution products of haloalkanes",
      "A primary amine attacks through nitrogen to give a secondary amine; AgCN, being mainly covalent, attacks "
      "through nitrogen to give an isocyanide; KNO₂ (ionic) attacks through oxygen to give an alkyl nitrite; the "
      "carboxylate ion of a silver salt gives an ester.",
      ["R′NH₂ → RNHR′", "AgCN → RNC", "KNO₂ → R–O–N=O", "R′COOAg → R′COOR"],
      why_others_wrong="Swapping AgCN and the amine mixes up an isocyanide and an amine; swapping KNO₂ with AgCN "
                       "or the silver carboxylate confuses the ambident nitrite attack with other reagents.",
      ncert=f"{NC12}, 'Haloalkanes and Haloarenes', nucleophilic substitution reactions", seconds=40),

    N(T_HX, "C-X bond and preparation", "Intermediate",
      "4.6 g of ethanol is converted completely into chloroethane by heating with thionyl chloride. The total volume "
      "of the gaseous by-products, measured at STP, is (C = 12, H = 1, O = 16; molar volume at STP = "
      "22.4 L mol⁻¹):",
      ["2.24 L", v_2436, "6.72 L", "1.12 L"], "B", v_2436,
      "Thionyl chloride method",
      "C₂H₅OH + SOCl₂ → C₂H₅Cl + SO₂↑ + HCl↑. Both by-products are gases, which is why this method gives a fairly "
      "pure alkyl chloride.",
      ["Ethanol: 4.6 / 46 = 0.10 mol", "SO₂ + HCl = 0.10 + 0.10 = 0.20 mol", "Volume = 0.20 × 22.4 = 4.48 L"],
      why_others_wrong="2.24 L counts only one of the two gases; 6.72 L also counts chloroethane, which is the "
                       "product and not a by-product; 1.12 L halves one gas.",
      ncert=f"{NC12}, 'Haloalkanes and Haloarenes', preparation from alcohols: thionyl chloride", seconds=45),

    N(T_HX, "C-X bond and preparation", "Intermediate",
      "11.25 g of chlorobenzene is treated with sodium in dry ether, and the Fittig reaction goes to completion. The "
      "mass of biphenyl, C₆H₅–C₆H₅, formed is (C = 12, H = 1, Cl = 35.5):",
      ["3.85 g", "15.4 g", v_2437, "11.25 g"], "C", v_2437,
      "Fittig reaction",
      "Aryl halides couple with sodium in dry ether: 2C₆H₅Cl + 2Na → C₆H₅–C₆H₅ + 2NaCl. Two moles of aryl halide "
      "give one mole of biphenyl.",
      ["C₆H₅Cl: 11.25 / 112.5 = 0.10 mol", "Biphenyl: 0.10 / 2 = 0.050 mol",
       "Mass = 0.050 × 154 = 7.7 g"],
      why_others_wrong="15.4 g forgets that two aryl groups make one biphenyl; 3.85 g halves twice; 11.25 g repeats "
                       "the mass of chlorobenzene.",
      ncert=f"{NC12}, 'Haloalkanes and Haloarenes', reactions of haloarenes with metals: Fittig reaction",
      seconds=45),

    Q(T_HX, "C-X bond and preparation", "Intermediate", "assertion_reason",
      *ar("Alkyl chlorides are converted into alkyl iodides by heating with NaI in dry acetone.", True,
          "The NaCl formed is precipitated in dry acetone, which drives the reaction forward according to Le "
          "Chatelier's principle.", True, explains=True),
      "Finkelstein reaction",
      "R–Cl + NaI ⇌ R–I + NaCl is an equilibrium. In dry acetone NaI is soluble but NaCl is not; as NaCl "
      "precipitates, it is removed from the equilibrium, so the reaction goes to completion. R explains A.",
      ["Halogen exchange (Finkelstein)", "Removal of NaCl as a precipitate shifts the equilibrium to the right"],
      ncert=f"{NC12}, 'Haloalkanes and Haloarenes', halogen exchange", seconds=35),

    Q(T_HX, "C-X bond and preparation", "Intermediate", "statement_pair",
      *sp("Alkyl bromides can be prepared from alcohols using red phosphorus and bromine, which generate PBr₃ in "
          "situ.", True,
          "Primary alcohols are converted into alkyl chlorides simply by shaking with concentrated HCl at room "
          "temperature, without any catalyst.", False),
      "Preparing haloalkanes from alcohols",
      "PBr₃ and PI₃ are usually generated in situ by the reaction of red phosphorus with bromine or iodine. Only "
      "tertiary alcohols react with concentrated HCl at room temperature; primary and secondary alcohols need "
      "anhydrous ZnCl₂ as catalyst (and heating).",
      ["Statement I: true", "Statement II: false; this works only for tertiary alcohols"],
      ncert=f"{NC12}, 'Haloalkanes and Haloarenes', preparation of haloalkanes from alcohols", seconds=40),

    Q(T_HX, "Polyhalogen compounds", "Intermediate", "multi_statement",
      *ms("Which of the following statements about polyhalogen compounds are correct?",
          [("Chloroform is used as a solvent for fats, alkaloids and iodine.", True),
           ("In the stratosphere, freons initiate radical chain reactions that upset the natural ozone balance.",
            True),
           ("Iodoform is now widely preferred as an antiseptic because of its pleasant smell.", False),
           ("Dichloromethane is used as a propellant in aerosols and as a process solvent in the manufacture of "
            "drugs.", True),
           ("DDT has been used to kill mosquitoes that spread malaria and lice that carry typhus.", True)],
          [["a", "b", "c"], ["b", "c", "d", "e"], ["a", "d", "e"]], "C"),
      "Uses and environmental effects of polyhalogen compounds",
      "NCERT: chloroform is a solvent for fats, alkaloids and iodine; freons that reach the stratosphere start "
      "radical chain reactions upsetting the ozone balance; dichloromethane is a paint remover, aerosol propellant "
      "and process solvent for drugs; DDT was used against malaria-spreading mosquitoes and typhus-carrying lice. "
      "Iodoform has an objectionable smell and has been replaced by other iodine formulations.",
      ["(a) true", "(b) true", "(c) false: objectionable smell", "(d) true", "(e) true"],
      why_others_wrong="Options containing (c) accept the wrong claim about iodoform; (a), (d) and (e) only leaves "
                       "out the role of freons in ozone depletion.",
      ncert=f"{NC12}, 'Haloalkanes and Haloarenes', polyhalogen compounds", seconds=60),

    N(T_HX, "C-X bond and preparation", "Advanced",
      "Considering all the structural isomers of the monobromoalkane C₅H₁₁Br, how many of them are secondary (2°) "
      "alkyl bromides?",
      ["1", "2", v_2441, "4"], "C", v_2441,
      "Classifying isomeric haloalkanes",
      "C₅H₁₁Br has eight structural isomers. An alkyl halide is secondary when the carbon carrying the halogen is "
      "bonded to two other carbon atoms.",
      ["1°: 1-bromopentane, 1-bromo-2-methylbutane, 1-bromo-3-methylbutane, 1-bromo-2,2-dimethylpropane (4)",
       "2°: 2-bromopentane, 3-bromopentane, 2-bromo-3-methylbutane (3)", "3°: 2-bromo-2-methylbutane (1)"],
      why_others_wrong="2 usually misses the branched 2-bromo-3-methylbutane; 4 counts 2-bromo-2-methylbutane, which "
                       "is tertiary; 1 counts only the tertiary bromide.",
      ncert=f"{NC12}, 'Haloalkanes and Haloarenes', classification of haloalkanes", seconds=90),

    Q(T_HX, "SN1 and SN2", "Advanced", "direct",
      "Which of the following reacts fastest with OH⁻ ions by the SN2 mechanism?",
      ["1-Bromo-2,2-dimethylpropane, (CH₃)₃C–CH₂Br", "2-Bromopentane", "2-Bromo-2-methylbutane", "1-Bromopentane"],
      "D",
      "Steric hindrance in SN2 reactions",
      "In SN2 the nucleophile attacks the carbon from the side opposite the leaving group, in a single step. Bulky "
      "groups on or next to that carbon hinder the attack. 1-Bromopentane is primary with an unbranched chain, so "
      "it is attacked most easily.",
      ["1-Bromopentane: 1°, unhindered → fastest", "2-Bromopentane: 2° → slower",
       "2-Bromo-2-methylbutane: 3° → very slow by SN2",
       "(CH₃)₃C–CH₂Br: 1°, but the bulky tert-butyl group next to the reacting carbon hinders attack"],
      why_others_wrong="Neopentyl bromide is primary, but the adjacent tert-butyl group blocks the back-side approach; "
                       "secondary and tertiary bromides are more crowded at the reacting carbon itself.",
      ncert=f"{NC12}, 'Haloalkanes and Haloarenes', SN2 mechanism: steric effects", seconds=60),

    Q(T_HX, "SN1 and SN2", "Advanced", "assertion_reason",
      *ar("SN1 reactions of alkyl halides are favoured by non-polar solvents.", False,
          "In SN1 reactions, polar protic solvents stabilise the carbocation and the leaving halide ion by "
          "solvation.", True),
      "Solvent effects in SN1 reactions",
      "The slow step of SN1 is the ionisation of R–X into R⁺ and X⁻. Polar protic solvents such as water, alcohols "
      "and ethanoic acid help this step by solvating both ions, so SN1 reactions are generally carried out in "
      "polar protic solvents. A is false; R is true.",
      ["A: false; SN1 needs polar protic solvents", "R: true"],
      ncert=f"{NC12}, 'Haloalkanes and Haloarenes', SN1 mechanism", seconds=40),

    Q(T_HX, "SN1 and SN2", "Advanced", "multi_statement",
      *ms("Which of the following statements about dehydrohalogenation (β-elimination) are correct?",
          [("2-Bromo-2-methylbutane, heated with alcoholic KOH, gives mainly 2-methylbut-2-ene.", True),
           ("1-Bromobutane, heated with alcoholic KOH, gives but-1-ene.", True),
           ("A tertiary alkyl halide treated with a strong base mainly undergoes SN2 substitution.", False),
           ("1-Bromo-2,2-dimethylpropane, (CH₃)₃C–CH₂Br, cannot undergo β-elimination, because its β-carbon "
            "carries no hydrogen atom.", True),
           ("In dehydrohalogenation, the halogen and a hydrogen atom are removed from the same carbon atom.", False)],
          [["a", "b", "c"], ["a", "d", "e"], ["b", "c", "d"]], "B"),
      "β-Elimination and Zaitsev's rule",
      "In β-elimination, H is lost from the β-carbon (next to the carbon bearing X). Zaitsev's rule: the alkene with "
      "more alkyl groups on the doubly bonded carbons is preferred. A tertiary halide with a strong base prefers "
      "elimination. In neopentyl bromide the only β-carbon is a quaternary carbon with no hydrogen.",
      ["(a) true (Zaitsev product)", "(b) true (only one kind of β-H)", "(c) false: elimination is preferred",
       "(d) true", "(e) false: H comes from the β-carbon"],
      why_others_wrong="Options with (c) ignore the competition that favours elimination for 3° halides; the option "
                       "with (e) describes an α-elimination, which is not dehydrohalogenation.",
      ncert=f"{NC12}, 'Haloalkanes and Haloarenes', elimination reactions", seconds=75),
]

# ================================================================ Organic Compounds Containing Oxygen (2445-2464)
# 2445: C6H5OH + Zn -> C6H6 + ZnO; 9.4 g phenol
m_2445 = F(94, 10) / mm(C=6, H=6, O=1) * mm(C=6, H=6)
assert mm(C=6, H=6, O=1) == 94 and m_2445 == F(78, 10)
v_2445 = "7.8 g"
# 2446: CH3CN + 2H2O (H+) -> CH3COOH + NH4+; 4.1 g nitrile
n_2446 = F(41, 10) / mm(C=2, H=3, N=1)
m_2446 = n_2446 * mm(C=2, H=4, O=2)
assert n_2446 == F(1, 10) and m_2446 == 6 and n_2446 * mm(C=2, H=5, N=1, O=1) == F(59, 10)
v_2446 = "6.0 g"
# 2451: acids with pKa below 6.4 (carbonic acid) liberate CO2 from NaHCO3
pka_2451 = {"ethanoic acid": 4.76, "benzoic acid": 4.19, "methanoic acid": 3.75, "phenol": 10.0,
            "4-nitrophenol": 7.1, "picric acid": 0.5, "ethanol": 15.9}
v_2451 = str(sum(1 for p in pka_2451.values() if p < 6.4))
assert v_2451 == "4"
# 2452: immediate turbidity with Lucas reagent at room temperature = tertiary alcohols
deg_2452 = {"2-methylpropan-2-ol": 3, "butan-2-ol": 2, "2-methylbutan-2-ol": 3, "propan-1-ol": 1,
            "1-methylcyclohexan-1-ol": 3, "cyclohexanol": 2, "butan-1-ol": 1}
v_2452 = str(sum(1 for d in deg_2452.values() if d == 3))
assert v_2452 == "3"
# 2459: C2H5OH -> CH3COOH loses 4 e-; Cr2O7^2- gains 6 e-; K2Cr2O7 = 294 g/mol
n_e = F(46, 10) / mm(C=2, H=6, O=1) * 4
m_2459 = n_e / 6 * 294
assert n_e == F(4, 10) and m_2459 == F(196, 10)
assert F(1, 10) * 2 / 6 * 294 == F(98, 10) and F(1, 10) * 294 == F(294, 10)
v_2459 = "19.6 g"
# 2460: propene -> (B2H6; H2O2/OH-) propan-1-ol -> (PCC) propanal -> 2 Ag per CHO
n_2460 = F(42, 10) / mm(C=3, H=6)
m_2460 = n_2460 * 2 * AM["Ag"]
assert n_2460 == F(1, 10) and m_2460 == F(216, 10)
v_2460 = "21.6 g"

QUESTIONS += [
    N(T_OX, "Phenols", "Basic",
      "9.4 g of phenol is heated with zinc dust and is converted completely into benzene. The mass of benzene formed "
      "is (C = 12, H = 1, O = 16):",
      ["3.9 g", v_2445, "9.4 g", "15.6 g"], "B", v_2445,
      "Reduction of phenol by zinc dust",
      "Phenol is converted into benzene on heating with zinc dust: C₆H₅OH + Zn → C₆H₆ + ZnO. One mole of phenol "
      "gives one mole of benzene.",
      ["Phenol: 9.4 / 94 = 0.10 mol", "Benzene: 0.10 × 78 = 7.8 g"],
      why_others_wrong="9.4 g repeats the mass of phenol; 3.9 g and 15.6 g halve or double the 1 : 1 mole ratio.",
      ncert=f"{NC12}, 'Alcohols, Phenols and Ethers', reactions of phenol with zinc dust", seconds=30),

    N(T_OX, "Carboxylic acids", "Basic",
      "4.1 g of ethanenitrile, CH₃CN, is hydrolysed completely with dilute acid. The mass of the carboxylic acid "
      "formed is (C = 12, H = 1, N = 14, O = 16):",
      ["4.1 g", "4.6 g", "5.9 g", v_2446], "D", v_2446,
      "Preparation of carboxylic acids from nitriles",
      "Nitriles are hydrolysed, through amides, to carboxylic acids in the presence of H⁺ or OH⁻ as catalyst: "
      "CH₃C≡N → CH₃CONH₂ → CH₃COOH. One mole of nitrile gives one mole of acid.",
      ["CH₃CN: 4.1 / 41 = 0.10 mol", "CH₃COOH: 0.10 × 60 = 6.0 g"],
      why_others_wrong="5.9 g stops at the amide, CH₃CONH₂; 4.6 g is the mass of 0.10 mol of ethanol; 4.1 g repeats "
                       "the mass of the nitrile.",
      ncert=f"{NC12}, 'Aldehydes, Ketones and Carboxylic Acids', methods of preparation of carboxylic acids",
      seconds=30),

    Q(T_OX, "Alcohols", "Basic", "direct",
      "The IUPAC name of glycerol, HOCH₂–CH(OH)–CH₂OH, is:",
      ["Propane-1,3-diol", "1,2,3-Trihydroxypropane", "Propane-1,2,3-triol", "Propan-1,2,3-ol"], "C",
      "Naming polyhydric alcohols",
      "For a polyol the 'e' of the alkane name is kept and multiplying prefixes are added to 'ol': three –OH groups "
      "on a three-carbon chain at C-1, C-2 and C-3 give propane-1,2,3-triol.",
      ["Parent: propane", "Three –OH at 1, 2, 3 → propane-1,2,3-triol"],
      why_others_wrong="Propane-1,3-diol has only two –OH groups; 'trihydroxypropane' cites the principal group as a "
                       "prefix; 'propan-1,2,3-ol' drops the multiplying prefix 'tri' and the 'e'.",
      ncert=f"{NC12}, 'Alcohols, Phenols and Ethers', nomenclature", seconds=25),

    Q(T_OX, "Alcohols", "Basic", "statement_pair",
      *sp("In the acid-catalysed dehydration of ethanol, the formation of the carbocation is the slowest, "
          "rate-determining step.", True,
          "The reaction of an alcohol with an acid chloride to give an ester is carried out in the presence of a base "
          "such as pyridine, which neutralises the HCl formed.", True),
      "Dehydration mechanism; esterification with acid chlorides",
      "Dehydration of ethanol: (1) protonation of the –OH group, (2) loss of water to form the carbocation, the "
      "slowest step, (3) loss of a proton to give ethene. In acylation by an acid chloride, HCl is formed; pyridine "
      "removes it and shifts the equilibrium forward.",
      ["Statement I: true", "Statement II: true"],
      ncert=f"{NC12}, 'Alcohols, Phenols and Ethers', chemical reactions of alcohols", seconds=35),

    Q(T_OX, "Phenols", "Basic", "assertion_reason",
      *ar("Sodium phenoxide reacts with carbon dioxide, a weak electrophile, and the product on acidification gives "
          "salicylic acid.", True,
          "The phenoxide ion is even more reactive than phenol towards electrophilic aromatic substitution.", True,
          explains=True),
      "Kolbe's reaction",
      "NCERT: the phenoxide ion, generated by treating phenol with NaOH, is even more reactive than phenol towards "
      "electrophilic substitution, and hence it reacts even with CO₂, a weak electrophile, giving "
      "ortho-hydroxybenzoic acid (salicylic acid) after acidification. R is the reason for A.",
      ["–O⁻ is a stronger electron donor than –OH", "Strongly activated ring attacks the weak electrophile CO₂"],
      ncert=f"{NC12}, 'Alcohols, Phenols and Ethers', Kolbe's reaction", seconds=35),

    Q(T_OX, "Alcohols", "Basic", "match_list",
      *ml("Match the common name of the alcohol in List-I with its IUPAC name in List-II.",
          ["Isobutyl alcohol", "tert-Butyl alcohol", "sec-Butyl alcohol", "Neopentyl alcohol"],
          ["Butan-2-ol", "2,2-Dimethylpropan-1-ol", "2-Methylpropan-1-ol", "2-Methylpropan-2-ol"],
          "III IV I II", ["IV III I II", "III IV II I", "I IV III II"], "B"),
      "Common and IUPAC names of alcohols",
      "Isobutyl = (CH₃)₂CHCH₂–; tert-butyl = (CH₃)₃C–; sec-butyl = CH₃CH₂CH(CH₃)–; neopentyl = (CH₃)₃CCH₂–.",
      ["(CH₃)₂CHCH₂OH → 2-methylpropan-1-ol", "(CH₃)₃COH → 2-methylpropan-2-ol",
       "CH₃CH₂CH(OH)CH₃ → butan-2-ol", "(CH₃)₃CCH₂OH → 2,2-dimethylpropan-1-ol"],
      why_others_wrong="Swapping isobutyl and tert-butyl confuses a 1° alcohol with a 3° alcohol; swapping sec-butyl "
                       "and neopentyl confuses a C₄ with a C₅ alcohol.",
      ncert=f"{NC12}, 'Alcohols, Phenols and Ethers', nomenclature", seconds=40),

    N(T_OX, "Carboxylic acids", "Intermediate",
      "An acid liberates CO₂ from aqueous sodium hydrogencarbonate only if it is a stronger acid than carbonic acid "
      "(pKa = 6.4). Using the pKa values given in brackets, how many of the following liberate CO₂ from NaHCO₃?\n"
      "Ethanoic acid (4.76), benzoic acid (4.19), methanoic acid (3.75), phenol (10.0), 4-nitrophenol (7.1), "
      "picric acid, i.e. 2,4,6-trinitrophenol (0.5), ethanol (15.9)",
      ["3", v_2451, "5", "6"], "B", v_2451,
      "Acid strength and the hydrogencarbonate test",
      "A lower pKa means a stronger acid. Acids with pKa below 6.4 are stronger than carbonic acid and displace CO₂ "
      "from NaHCO₃.",
      ["pKa < 6.4: ethanoic, benzoic, methanoic acids and picric acid → 4",
       "pKa > 6.4: phenol, 4-nitrophenol, ethanol → no CO₂"],
      why_others_wrong="3 counts only the carboxylic acids and leaves out picric acid, a phenol with a pKa of 0.5; "
                       "5 includes 4-nitrophenol, which is still weaker than carbonic acid.",
      ncert=f"{NC12}, 'Aldehydes, Ketones and Carboxylic Acids', acidity of carboxylic acids", seconds=50),

    N(T_OX, "Alcohols", "Intermediate",
      "How many of the following alcohols give turbidity immediately with Lucas reagent (concentrated HCl and "
      "anhydrous ZnCl₂) at room temperature?\n"
      "2-Methylpropan-2-ol, butan-2-ol, 2-methylbutan-2-ol, propan-1-ol, 1-methylcyclohexan-1-ol, cyclohexanol, "
      "butan-1-ol",
      ["1", "2", v_2452, "5"], "C", v_2452,
      "Lucas test",
      "Tertiary alcohols form the insoluble alkyl chloride at once and give turbidity immediately; primary alcohols "
      "give no turbidity at room temperature (secondary alcohols react more slowly).",
      ["Tertiary: 2-methylpropan-2-ol, 2-methylbutan-2-ol, 1-methylcyclohexan-1-ol → 3",
       "Secondary: butan-2-ol, cyclohexanol; primary: propan-1-ol, butan-1-ol"],
      why_others_wrong="1 or 2 misses the cyclic tertiary alcohol 1-methylcyclohexan-1-ol or 2-methylbutan-2-ol; 5 "
                       "adds the secondary alcohols, which do not react immediately.",
      ncert=f"{NC12}, 'Alcohols, Phenols and Ethers', distinguishing primary, secondary and tertiary alcohols",
      seconds=45),

    Q(T_OX, "Phenols", "Intermediate", "direct",
      "In the Reimer–Tiemann reaction, phenol is treated with chloroform in the presence of aqueous sodium "
      "hydroxide, and salicylaldehyde is obtained after acidification. The intermediate that is hydrolysed by the "
      "alkali in this reaction is:",
      ["Benzoyl chloride", "Chlorobenzene", "Benzyl chloride", "A substituted benzal chloride"], "D",
      "Reimer–Tiemann reaction",
      "NCERT: a –CHO group is introduced at the ortho position of the benzene ring; an intermediate substituted "
      "benzal chloride (a –CHCl₂ group on the phenoxide ring) is hydrolysed in the presence of alkali to give "
      "salicylaldehyde.",
      ["–CHCl₂ group introduced ortho to –O⁻", "Hydrolysis of –CHCl₂ → –CHO"],
      why_others_wrong="Benzoyl chloride (C₆H₅COCl) and benzyl chloride (C₆H₅CH₂Cl) carry the wrong number of "
                       "chlorine atoms on the side chain; chlorobenzene has chlorine on the ring and cannot give an "
                       "aldehyde group.",
      ncert=f"{NC12}, 'Alcohols, Phenols and Ethers', Reimer–Tiemann reaction", seconds=40),

    Q(T_OX, "Carboxylic acids", "Intermediate", "direct",
      "Which reagent reduces carboxylic acids to primary alcohols but does not easily reduce functional groups such "
      "as ester, nitro and halo groups?",
      ["Lithium aluminium hydride", "Sodium borohydride", "Diborane", "Zinc amalgam and concentrated HCl"], "C",
      "Selective reduction of carboxylic acids",
      "NCERT: carboxylic acids are reduced to primary alcohols by lithium aluminium hydride or, better, by "
      "diborane. Diborane does not easily reduce functional groups such as ester, nitro and halo. Sodium "
      "borohydride does not reduce the carboxyl group.",
      ["Diborane: –COOH → –CH₂OH; leaves ester, nitro, halo largely untouched"],
      why_others_wrong="LiAlH₄ reduces esters as well; NaBH₄ does not reduce –COOH; Zn–Hg/HCl is used for "
                       "Clemmensen reduction of aldehydes and ketones.",
      ncert=f"{NC12}, 'Aldehydes, Ketones and Carboxylic Acids', reduction of carboxylic acids", seconds=35),

    Q(T_OX, "Aldehydes and ketones", "Intermediate", "assertion_reason",
      *ar("Ketones are readily oxidised by Tollens' reagent to carboxylic acids having the same number of carbon "
          "atoms.", False,
          "In aldehydes, the hydrogen atom on the carbonyl carbon is converted into an –OH group on oxidation, "
          "without breaking any carbon–carbon bond.", True),
      "Oxidation of aldehydes versus ketones",
      "Aldehydes are oxidised easily, even by mild oxidising agents such as Tollens' reagent, because of the H on "
      "the carbonyl carbon (R). Ketones lack this hydrogen; they are oxidised only under vigorous conditions by "
      "strong oxidising agents, with cleavage of C–C bonds, giving acids with fewer carbon atoms. A is false.",
      ["A: false", "R: true"],
      ncert=f"{NC12}, 'Aldehydes, Ketones and Carboxylic Acids', oxidation of aldehydes and ketones", seconds=40),

    Q(T_OX, "Aldehydes and ketones", "Intermediate", "statement_pair",
      *sp("Esters are reduced to aldehydes by diisobutylaluminium hydride (DIBAL-H).", True,
          "Propanone undergoes the Cannizzaro reaction when heated with concentrated NaOH.", False),
      "DIBAL-H reduction; Cannizzaro reaction",
      "NCERT notes that DIBAL-H reduces nitriles to imines (then aldehydes on hydrolysis) and that esters are also "
      "reduced to aldehydes with DIBAL-H. The Cannizzaro reaction is shown by aldehydes with no α-hydrogen; "
      "propanone is a ketone with six α-hydrogens and instead undergoes aldol reaction.",
      ["Statement I: true", "Statement II: false"],
      ncert=f"{NC12}, 'Aldehydes, Ketones and Carboxylic Acids', preparation of aldehydes; Cannizzaro reaction",
      seconds=40),

    Q(T_OX, "Alcohols", "Intermediate", "match_list",
      *ml("The vapours of each alcohol in List-I are passed over heated copper at 573 K. Match it with the main "
          "organic product in List-II.",
          ["Ethanol", "Propan-2-ol", "2-Methylpropan-2-ol", "Methanol"],
          ["Methanal", "2-Methylpropene", "Propanone", "Ethanal"],
          "IV III II I", ["IV III I II", "III IV II I", "II III IV I"], "D"),
      "Dehydrogenation of alcohols",
      "Over heated copper, primary alcohols are dehydrogenated to aldehydes and secondary alcohols to ketones. A "
      "tertiary alcohol has no H on the carbinol carbon, so it is dehydrated to an alkene instead.",
      ["Ethanol → ethanal", "Propan-2-ol → propanone", "2-Methylpropan-2-ol → 2-methylpropene",
       "Methanol → methanal"],
      why_others_wrong="Codes that give the tertiary alcohol a carbonyl product ignore the missing α-hydrogen on the "
                       "carbinol carbon; codes that swap ethanol and propan-2-ol mix up aldehyde and ketone formation.",
      ncert=f"{NC12}, 'Alcohols, Phenols and Ethers', dehydrogenation of alcohols", seconds=45),

    Q(T_OX, "Aldehydes and ketones", "Intermediate", "multi_statement",
      *ms("Which of the following give benzaldehyde as the main organic product?",
          [("Toluene treated with chromyl chloride in CS₂, followed by hydrolysis", True),
           ("Benzene treated with carbon monoxide and HCl in the presence of anhydrous AlCl₃ or CuCl", True),
           ("Benzoyl chloride hydrogenated over palladium on barium sulphate", True),
           ("Benzonitrile reduced with SnCl₂ and HCl, followed by hydrolysis", True),
           ("Toluene oxidised with alkaline KMnO₄, followed by acidification", False)],
          [["a", "b", "c"], ["a", "c", "d", "e"], ["b", "d", "e"]], "A"),
      "Preparation of aromatic aldehydes",
      "Etard reaction (chromyl chloride), Gattermann–Koch reaction (CO + HCl), Rosenmund reduction (H₂, Pd–BaSO₄) "
      "and Stephen reaction (SnCl₂/HCl, then H₃O⁺) all give benzaldehyde. Strong oxidation of toluene with KMnO₄ "
      "goes on to benzoic acid.",
      ["(a) Etard → C₆H₅CHO", "(b) Gattermann–Koch → C₆H₅CHO", "(c) Rosenmund → C₆H₅CHO",
       "(d) Stephen → C₆H₅CHO", "(e) KMnO₄ → C₆H₅COOH"],
      why_others_wrong="Options with (e) forget that KMnO₄ oxidises the side chain right up to –COOH; (a), (b) and "
                       "(c) only leaves out the Stephen reaction.",
      ncert=f"{NC12}, 'Aldehydes, Ketones and Carboxylic Acids', preparation of aldehydes", seconds=60),

    N(T_OX, "Alcohols", "Advanced",
      "Ethanol is oxidised to ethanoic acid by acidified potassium dichromate. The half-reactions are\n"
      "Cr₂O₇²⁻ + 14H⁺ + 6e⁻ → 2Cr³⁺ + 7H₂O and C₂H₅OH + H₂O → CH₃COOH + 4H⁺ + 4e⁻.\n"
      "The minimum mass of K₂Cr₂O₇ (molar mass 294 g mol⁻¹) needed to oxidise 4.6 g of ethanol completely is "
      "(C = 12, H = 1, O = 16):",
      ["9.8 g", "14.7 g", "29.4 g", v_2459], "D", v_2459,
      "Electron balance in the oxidation of an alcohol",
      "Equate the electrons lost by ethanol to the electrons gained by dichromate.",
      ["Ethanol: 4.6 / 46 = 0.10 mol → electrons lost = 0.10 × 4 = 0.40 mol",
       "K₂Cr₂O₇ = 0.40 / 6 = 0.0667 mol", "Mass = 0.0667 × 294 = 19.6 g"],
      shortcut="3C₂H₅OH needs 2Cr₂O₇²⁻ (12 electrons each side).",
      why_others_wrong="9.8 g counts only 2 electrons per ethanol (oxidation stopping at ethanal); 29.4 g takes a "
                       "1 : 1 mole ratio; 14.7 g uses 3 electrons per ethanol.",
      ncert=f"{NC12}, 'Alcohols, Phenols and Ethers', oxidation of alcohols", seconds=90),

    N(T_OX, "Aldehydes and ketones", "Advanced",
      "4.2 g of propene is converted into an alcohol by hydroboration–oxidation (B₂H₆, then H₂O₂/OH⁻). The alcohol "
      "is oxidised with pyridinium chlorochromate (PCC), and the product is warmed with an excess of Tollens' "
      "reagent. Assuming every step is complete, the mass of silver deposited is (C = 12, H = 1, Ag = 108):",
      ["0 g", v_2460, "10.8 g", "43.2 g"], "B", v_2460,
      "Regiochemistry of hydroboration and the Tollens' test",
      "Hydroboration–oxidation adds water in an anti-Markovnikov manner, giving propan-1-ol. PCC oxidises a primary "
      "alcohol only to the aldehyde, propanal, which reduces Tollens' reagent: RCHO + 2[Ag(NH₃)₂]⁺ + 3OH⁻ → "
      "RCOO⁻ + 2Ag + 2H₂O + 4NH₃.",
      ["Propene: 4.2 / 42 = 0.10 mol → 0.10 mol propan-1-ol → 0.10 mol propanal",
       "Ag = 2 × 0.10 = 0.20 mol → 0.20 × 108 = 21.6 g"],
      why_others_wrong="0 g assumes Markovnikov addition (propan-2-ol → propanone, which gives no silver mirror); "
                       "10.8 g uses one Ag per aldehyde; 43.2 g uses four, as for methanal.",
      ncert=f"{NC12}, 'Alcohols, Phenols and Ethers', hydroboration–oxidation; 'Aldehydes, Ketones and Carboxylic "
            "Acids', Tollens' test", seconds=90),

    Q(T_OX, "Ethers", "Advanced", "assertion_reason",
      *ar("When methyl tert-butyl ether, CH₃–O–C(CH₃)₃, is heated with HI, the products are methanol and "
          "2-iodo-2-methylpropane.", True,
          "In this cleavage, the iodide ion attacks the methyl carbon by the SN2 mechanism.", False),
      "Cleavage of ethers containing a tertiary alkyl group",
      "When one alkyl group is tertiary, the protonated ether ionises by the SN1 mechanism to give the stable "
      "tert-butyl carbocation, which combines with I⁻; methanol is the other product. An SN2 attack on the methyl "
      "carbon would instead give CH₃I and tert-butyl alcohol. So A is true and R is false.",
      ["A: true (tert-butyl iodide + methanol)", "R: false; the reaction follows SN1"],
      ncert=f"{NC12}, 'Alcohols, Phenols and Ethers', cleavage of C–O bond in ethers", seconds=50),

    Q(T_OX, "Phenols", "Advanced", "statement_pair",
      *sp("Phenol reacts with dilute nitric acid at 298 K to give p-nitrophenol as the only product.", False,
          "2,4,6-Trinitrophenol is a weaker acid than phenol.", False),
      "Nitration of phenol; acidity of nitrophenols",
      "With dilute HNO₃ at low temperature (298 K), phenol gives a mixture of ortho- and para-nitrophenols, which "
      "are separated by steam distillation. Three –NO₂ groups make picric acid a much stronger acid than phenol "
      "(pKa about 0.5 against 10.0).",
      ["Statement I: false; o- and p-nitrophenols are formed", "Statement II: false; picric acid is far stronger"],
      ncert=f"{NC12}, 'Alcohols, Phenols and Ethers', nitration of phenol; acidity of phenols", seconds=45),

    Q(T_OX, "Aldehydes and ketones", "Advanced", "multi_statement",
      *ms("Which of the following pairs can be distinguished by the test given?",
          [("Propanal and propanone: Tollens' reagent", True),
           ("Pentan-2-one and pentan-3-one: iodoform test (I₂ and NaOH)", True),
           ("Benzaldehyde and acetophenone: Fehling's solution", False),
           ("Phenol and benzoic acid: aqueous NaHCO₃", True),
           ("Ethanol and methanol: 2,4-dinitrophenylhydrazine", False)],
          [["a", "b", "c"], ["a", "c", "d", "e"], ["b", "d", "e"]], "A"),
      "Chemical tests that distinguish oxygen compounds",
      "Propanal reduces Tollens' reagent, propanone does not. Pentan-2-one is a methyl ketone and gives iodoform; "
      "pentan-3-one does not. Aromatic aldehydes such as benzaldehyde do not respond to Fehling's test, and "
      "acetophenone (a ketone) does not either, so Fehling's solution cannot tell them apart. Benzoic acid "
      "liberates CO₂ from NaHCO₃, phenol does not. Neither alcohol has a carbonyl group, so neither reacts with "
      "2,4-DNP.",
      ["(a) true", "(b) true", "(c) false: neither gives a positive Fehling's test", "(d) true",
       "(e) false: both negative"],
      why_others_wrong="Options containing (c) assume every aldehyde reduces Fehling's solution; options containing "
                       "(e) use a carbonyl reagent on two alcohols.",
      ncert=f"{NC12}, 'Aldehydes, Ketones and Carboxylic Acids', chemical tests to distinguish aldehydes and "
            "ketones", seconds=75),

    Q(T_OX, "Aldehydes and ketones", "Advanced", "multi_statement",
      *ms("Which of the following statements about the carbonyl group are correct?",
          [("The carbonyl carbon is sp² hybridised and lies at the centre of a trigonal planar arrangement, with "
            "bond angles of about 120°.", True),
           ("The carbonyl carbon is an electrophilic (Lewis acid) centre and the carbonyl oxygen a nucleophilic "
            "(Lewis base) centre.", True),
           ("Carbonyl compounds have substantial dipole moments and are more polar than ethers.", True),
           ("The carboxylic carbon of a carboxylic acid is more electrophilic than the carbonyl carbon of an "
            "aldehyde.", False),
           ("The C=O bond of an aldehyde is non-polar, because both atoms share the π electrons equally.", False)],
          [["a", "b", "d"], ["b", "c", "e"], ["a", "b", "c", "d"]], "D"),
      "Nature of the carbonyl group",
      "NCERT: the carbonyl carbon is sp² hybridised, trigonal planar, with ~120° bond angles; the C=O bond is "
      "polarised because oxygen is more electronegative, making carbon an electrophilic centre and oxygen a "
      "nucleophilic centre; carbonyl compounds have substantial dipole moments and are more polar than ethers. "
      "In carboxylic acids the carboxylic carbon is less electrophilic than the carbonyl carbon because of "
      "resonance with the –OH oxygen.",
      ["(a) true", "(b) true", "(c) true", "(d) false: resonance makes it less electrophilic",
       "(e) false: the C=O bond is polar"],
      why_others_wrong="Options containing (d) overlook the resonance of the carboxyl group; the option with (e) "
                       "ignores the electronegativity difference between carbon and oxygen.",
      ncert=f"{NC12}, 'Aldehydes, Ketones and Carboxylic Acids', nature of carbonyl group; structure of carboxyl "
            "group", seconds=60),
]

# ================================================================ Organic Compounds Containing Nitrogen (2465-2477)
# 2465: arylamines = N bonded directly to an aromatic ring
aryl_2465 = {"aniline": True, "benzylamine": False, "N-methylaniline": True, "4-methylaniline": True,
             "cyclohexanamine": False, "N,N-dimethylaniline": True, "2-phenylethanamine": False}
v_2465 = str(sum(aryl_2465.values()))
assert v_2465 == "4"
# 2469: 2,4,6-tribromoaniline (C6H4Br3N) -> diazonium -> H3PO2 -> 1,3,5-tribromobenzene (C6H3Br3)
M_tba = mm(C=6, H=4, Br=3, N=1)
M_tbb = mm(C=6, H=3, Br=3)
assert (M_tba, M_tbb) == (330, 315)
m_2469 = F(330, 100) / M_tba * M_tbb
assert m_2469 == F(315, 100)
v_2469 = "3.15 g"
assert round(float(F(1, 100) * mm(C=6, H=4, Br=2)), 2) == 2.36
# 2470: stable arenediazonium salts at 273-278 K only from primary aromatic amines
pa_2470 = {"aniline": True, "4-methylaniline": True, "4-nitroaniline": True, "benzylamine": False,
           "ethanamine": False, "N-methylaniline": False}
v_2470 = str(sum(pa_2470.values()))
assert v_2470 == "3"
# 2474: pH of 0.10 M aniline, pKb = 9.38: pOH = (pKb - log C)/2
pOH = (9.38 + 1) / 2
pH_2474 = 14 - pOH
assert abs(pOH - 5.19) < 1e-9 and abs(pH_2474 - 8.81) < 1e-9
v_2474 = "8.81"

QUESTIONS += [
    N(T_NI, "Amines: basicity and identification", "Basic",
      "In an arylamine, the nitrogen atom is bonded directly to a carbon atom of an aromatic ring. How many of the "
      "following are arylamines?\n"
      "Aniline, benzylamine (C₆H₅CH₂NH₂), N-methylaniline, 4-methylaniline, cyclohexanamine, N,N-dimethylaniline, "
      "2-phenylethanamine (C₆H₅CH₂CH₂NH₂)",
      ["1", "2", "3", v_2465], "D", v_2465,
      "Classification of amines",
      "Only the position of nitrogen matters: it must be attached to the ring itself. Benzylamine and "
      "2-phenylethanamine have the amino group on a side-chain carbon, so they are aliphatic amines; cyclohexanamine "
      "has no aromatic ring.",
      ["Arylamines: aniline, N-methylaniline, 4-methylaniline, N,N-dimethylaniline → 4",
       "Not arylamines: benzylamine, 2-phenylethanamine, cyclohexanamine"],
      why_others_wrong="Lower counts leave out the secondary and tertiary arylamines (N-methyl and N,N-dimethyl "
                       "anilines); being 2° or 3° does not change the aryl classification.",
      ncert=f"{NC12}, 'Amines', classification of amines", seconds=35),

    Q(T_NI, "Amines: basicity and identification", "Basic", "direct",
      "Ethanamine is soluble in water, whereas aniline is only sparingly soluble. The reason is that:",
      ["aniline is a stronger base than ethanamine",
       "ethanamine forms hydrogen bonds with water, whereas the large hydrophobic C₆H₅ group of aniline decreases "
       "the extent of hydrogen bonding with water",
       "ethanamine is an ionic compound", "the nitrogen atom of aniline has no lone pair of electrons"], "B",
      "Solubility of amines in water",
      "Lower aliphatic amines dissolve in water because they form hydrogen bonds with water molecules. In aniline "
      "the large hydrocarbon (phenyl) part is hydrophobic, so the extent of hydrogen bonding, and hence the "
      "solubility, decreases.",
      ["Both have –NH₂ able to hydrogen bond", "Large hydrophobic C₆H₅ part in aniline → lower solubility"],
      why_others_wrong="Aniline is a weaker base than ethanamine; ethanamine is a covalent molecule; aniline's "
                       "nitrogen does carry a lone pair, though it is partly delocalised into the ring.",
      ncert=f"{NC12}, 'Amines', physical properties", seconds=30),

    Q(T_NI, "Diazonium salts", "Basic", "statement_pair",
      *sp("In replacing the diazonium group by chlorine, the yield in the Sandmeyer reaction (CuCl/HCl) is better "
          "than in the Gattermann reaction (copper powder/HCl).", True,
          "If the temperature of a benzenediazonium chloride solution is allowed to rise up to 283 K, the salt is "
          "hydrolysed to phenol.", True),
      "Reactions of arenediazonium salts",
      "NCERT: chloro and bromo groups can be introduced either with Cu(I) halides (Sandmeyer) or with copper "
      "powder and the halogen acid (Gattermann); the yield in the Sandmeyer reaction is found to be better. A "
      "diazonium salt solution warmed up to 283 K is hydrolysed to phenol.",
      ["Statement I: true", "Statement II: true"],
      ncert=f"{NC12}, 'Amines', chemical reactions of diazonium salts", seconds=35),

    Q(T_NI, "Amines: basicity and identification", "Basic", "match_list",
      *ml("Match the common name of the amine in List-I with its IUPAC name in List-II.",
          ["Allylamine, CH₂=CH–CH₂–NH₂", "Hexamethylenediamine, H₂N–(CH₂)₆–NH₂", "Isopropylamine, (CH₃)₂CH–NH₂",
           "Dimethylamine, (CH₃)₂NH"],
          ["N-Methylmethanamine", "Propan-2-amine", "Prop-2-en-1-amine", "Hexane-1,6-diamine"],
          "III IV II I", ["IV III II I", "III IV I II", "II IV III I"], "B"),
      "Nomenclature of amines",
      "Amines are named by replacing the 'e' of the alkane with 'amine' (keeping 'e' before 'diamine'); the position "
      "of –NH₂ is given by a locant; extra alkyl groups on nitrogen are shown with the prefix N-.",
      ["Allylamine → prop-2-en-1-amine", "Hexamethylenediamine → hexane-1,6-diamine",
       "Isopropylamine → propan-2-amine", "Dimethylamine → N-methylmethanamine"],
      why_others_wrong="Swapping isopropylamine and dimethylamine confuses a 1° amine with a 2° amine; swapping the "
                       "first two pairs a C₃ unsaturated amine with a C₆ diamine.",
      ncert=f"{NC12}, 'Amines', nomenclature", seconds=35),

    N(T_NI, "Diazonium salts", "Intermediate",
      "1,3,5-Tribromobenzene cannot be made by direct bromination of benzene but can be made from aniline. 3.30 g of "
      "2,4,6-tribromoaniline is diazotised at 273–278 K, and the diazonium salt is treated with hypophosphorous "
      "acid (H₃PO₂). Assuming every step is complete, the mass of 1,3,5-tribromobenzene formed is (C = 12, H = 1, "
      "N = 14, Br = 80):",
      ["2.36 g", "3.30 g", v_2469, "6.30 g"], "C", v_2469,
      "Replacing –N₂⁺ by hydrogen",
      "Hypophosphorous acid reduces the diazonium salt and replaces –N₂⁺ by –H, so the three bromine atoms are left "
      "in the 1,3,5 positions, which direct bromination of benzene cannot give.",
      ["C₆H₂Br₃NH₂: M = 330 g mol⁻¹ → 3.30 / 330 = 0.010 mol", "C₆H₃Br₃: M = 315 g mol⁻¹",
       "Mass = 0.010 × 315 = 3.15 g"],
      why_others_wrong="3.30 g repeats the mass of the amine; 2.36 g is for a dibromobenzene; 6.30 g doubles the "
                       "moles.",
      ncert=f"{NC12}, 'Amines', importance of diazonium salts in synthesis of aromatic compounds", seconds=60),

    N(T_NI, "Diazonium salts", "Intermediate",
      "How many of the following give a diazonium salt that is stable enough to be used in solution at "
      "273–278 K when treated with NaNO₂ and dilute HCl?\n"
      "Aniline, 4-methylaniline, 4-nitroaniline, benzylamine, ethanamine, N-methylaniline",
      ["2", v_2470, "4", "5"], "B", v_2470,
      "Which amines form arenediazonium salts",
      "Only primary aromatic amines form arenediazonium salts, which are stable for a short time at low "
      "temperature. Primary aliphatic amines (including benzylamine, where –NH₂ is on a side chain) give unstable "
      "aliphatic diazonium salts that decompose at once with evolution of N₂. A secondary amine such as "
      "N-methylaniline has only one H on nitrogen and cannot form a diazonium salt.",
      ["Primary aromatic: aniline, 4-methylaniline, 4-nitroaniline → 3",
       "Benzylamine, ethanamine: primary aliphatic; N-methylaniline: secondary"],
      why_others_wrong="4 includes benzylamine, whose nitrogen is not on the ring; 2 leaves out 4-nitroaniline, "
                       "which is still a primary aromatic amine.",
      ncert=f"{NC12}, 'Amines', reaction with nitrous acid; diazonium salts", seconds=45),

    Q(T_NI, "Amines: basicity and identification", "Intermediate", "assertion_reason",
      *ar("N,N-Dimethylaniline reacts with benzenesulphonyl chloride to give a sulphonamide that is insoluble in "
          "aqueous alkali.", False,
          "Tertiary amines have no hydrogen atom on the nitrogen atom.", True),
      "Hinsberg's test and tertiary amines",
      "Benzenesulphonyl chloride replaces a hydrogen atom on nitrogen. N,N-Dimethylaniline is a tertiary amine "
      "with no N–H, so it does not react with Hinsberg's reagent at all; an alkali-insoluble sulphonamide is "
      "characteristic of secondary amines. A is false, R is true.",
      ["A: false; no reaction", "R: true"],
      ncert=f"{NC12}, 'Amines', reaction with arylsulphonyl chloride", seconds=40),

    Q(T_NI, "Amines: basicity and identification", "Intermediate", "statement_pair",
      *sp("Secondary amines react with benzenesulphonyl chloride to give a sulphonamide that dissolves in aqueous "
          "alkali.", False,
          "Primary aromatic amines react with nitrous acid at 273–278 K to form arenediazonium salts.", True),
      "Identification reactions of amines",
      "The N,N-dialkylbenzenesulphonamide from a secondary amine has no hydrogen on nitrogen and so is not acidic; "
      "it is insoluble in alkali (the alkali-soluble product comes from a primary amine). Primary aromatic amines "
      "give arenediazonium salts with nitrous acid in the cold.",
      ["Statement I: false", "Statement II: true"],
      ncert=f"{NC12}, 'Amines', chemical reactions: Hinsberg's test; reaction with nitrous acid", seconds=40),

    Q(T_NI, "Amines: basicity and identification", "Intermediate", "direct",
      "The correct order of basic strength in aqueous solution is:",
      ["4-Methylaniline > aniline > 4-nitroaniline", "Aniline > 4-methylaniline > 4-nitroaniline",
       "4-Nitroaniline > aniline > 4-methylaniline", "Aniline > 4-nitroaniline > 4-methylaniline"], "A",
      "Effect of substituents on the basicity of aniline",
      "Electron-releasing groups such as –CH₃ increase the electron density on nitrogen and raise the basic "
      "strength; electron-withdrawing groups such as –NO₂ lower it.",
      ["–CH₃ (+I, hyperconjugation): stronger base than aniline",
       "–NO₂ (−I, −R): much weaker base than aniline"],
      why_others_wrong="The other orders either ignore the activating effect of –CH₃ or treat –NO₂ as electron "
                       "releasing.",
      ncert=f"{NC12}, 'Amines', basic character of arylamines", seconds=35),

    N(T_NI, "Amines: basicity and identification", "Advanced",
      "The pKb of aniline is 9.38. Treating aniline as a weak base that is only slightly ionised, the pH of a "
      "0.10 M aqueous solution of aniline at 298 K is (pKw = 14.00):",
      ["4.62", "5.19", "9.38", v_2474], "D", v_2474,
      "pH of a solution of a weak base",
      "For a weak base, [OH⁻] = √(Kb·C), so pOH = ½(pKb − log C).",
      ["pOH = ½(9.38 + 1.00) = 5.19", "pH = 14.00 − 5.19 = 8.81"],
      why_others_wrong="5.19 is the pOH, not the pH; 4.62 is 14 − 9.38, which treats pKb as pOH; 9.38 is simply the "
                       "pKb.",
      ncert=f"{NC12}, 'Amines', basic character of amines (pKb values)", seconds=75),

    Q(T_NI, "Amines: basicity and identification", "Advanced", "direct",
      "An amine X, C₃H₉N, reacts with benzenesulphonyl chloride to give a product that is insoluble in aqueous "
      "alkali, and it does not give the carbylamine test. X is:",
      ["Propan-1-amine", "Propan-2-amine", "N-Methylethanamine", "N,N-Dimethylmethanamine"], "C",
      "Identifying an amine by Hinsberg's and carbylamine tests",
      "An alkali-insoluble Hinsberg product is given by a secondary amine. The carbylamine test is given only by "
      "primary amines, so a negative result is consistent. The only secondary amine of formula C₃H₉N is "
      "CH₃–NH–C₂H₅.",
      ["Insoluble sulphonamide → 2° amine", "No isocyanide → not 1°", "C₃H₉N, 2° → N-methylethanamine"],
      why_others_wrong="Propan-1-amine and propan-2-amine are primary (alkali-soluble product, positive carbylamine "
                       "test); trimethylamine (N,N-dimethylmethanamine) does not react with benzenesulphonyl "
                       "chloride.",
      ncert=f"{NC12}, 'Amines', identification of primary, secondary and tertiary amines", seconds=60),

    Q(T_NI, "Amines: basicity and identification", "Advanced", "assertion_reason",
      *ar("4-Nitroaniline is a much weaker base than aniline.", True,
          "The –NO₂ group at the para position withdraws electron density from the nitrogen lone pair by its −R and "
          "−I effects, making the lone pair less available for protonation.", True, explains=True),
      "Electron-withdrawing groups and the basicity of arylamines",
      "In aniline the nitrogen lone pair is already partly delocalised into the ring. A para –NO₂ group pulls this "
      "electron density further, through the ring onto itself (−R) and through σ bonds (−I), so protonation is much "
      "less favourable. R gives the reason for A.",
      ["A: true", "R: true and the cause of A"],
      ncert=f"{NC12}, 'Amines', basic character of arylamines", seconds=40),

    Q(T_NI, "Amines: basicity and identification", "Advanced", "multi_statement",
      *ms("Consider three amines: X = ethanamine, Y = aniline and Z = N-methylaniline. Which of the following "
          "statements are correct?",
          [("X and Y both give a foul-smelling isocyanide when warmed with chloroform and ethanolic KOH.", True),
           ("Y, after treatment with NaNO₂ and dilute HCl at 273–278 K, gives a coloured azo dye with an alkaline "
            "solution of phenol.", True),
           ("Z gives a product with benzenesulphonyl chloride that is insoluble in aqueous alkali.", True),
           ("X gives a diazonium salt that is stable in solution at 273–278 K.", False),
           ("Z gives the carbylamine test.", False)],
          [["a", "b", "d"], ["b", "c", "e"], ["a", "b", "c", "e"]], "B"),
      "Distinguishing primary aliphatic, primary aromatic and secondary amines",
      "The carbylamine test is given by primary amines, aliphatic and aromatic. Only primary aromatic amines give "
      "stable diazonium salts, which couple with phenol to give azo dyes; ethanamine's diazonium salt decomposes "
      "at once, releasing N₂. N-Methylaniline, a secondary amine, gives an alkali-insoluble sulphonamide and no "
      "isocyanide.",
      ["(a) true", "(b) true", "(c) true", "(d) false", "(e) false"],
      why_others_wrong="Options with (d) forget that aliphatic diazonium salts are unstable; options with (e) apply "
                       "the carbylamine test to a secondary amine.",
      ncert=f"{NC12}, 'Amines', chemical reactions; diazonium salts", seconds=75),
]

# ================================================================ Biomolecules (Chemistry) (2478-2490)
# 2482: linear double-stranded DNA of 50 base pairs: each strand of 50 nucleotides has 49 phosphodiester links
v_2482 = str(2 * (50 - 1))
assert v_2482 == "98"
# 2487: ds DNA, 1000 nucleotides (500 bp), 22% G -> G = C = 220 -> 220 G-C pairs, 280 A-T pairs
nuc, pg = 1000, F(22, 100)
g = nuc * pg
gc_pairs = g
at_pairs = nuc // 2 - gc_pairs
hb_2487 = 2 * at_pairs + 3 * gc_pairs
assert (g, at_pairs, hb_2487) == (220, 280, 1220)
assert 2 * 220 + 3 * 280 == 1280 and 2 * 390 + 3 * 110 == 1110 and 3 * 500 == 1500
v_2487 = str(hb_2487)

QUESTIONS += [
    Q(T_BM, "Carbohydrates", "Basic", "direct",
      "According to NCERT, amylose is a long unbranched chain of α-D-(+)-glucose units held together by C1–C4 "
      "glycosidic linkages. The number of glucose units in such a chain is about:",
      ["2 to 10", "20 to 50", "200 to 1000", "50,000 to 100,000"], "C",
      "Structure of amylose",
      "Amylose, the water-soluble component (15–20%) of starch, is a long unbranched chain of 200–1000 "
      "α-D-(+)-glucose units joined by C1–C4 glycosidic linkages.",
      ["Amylose: unbranched, C1–C4, 200–1000 glucose units"],
      why_others_wrong="2 to 10 units defines an oligosaccharide; 20 to 50 and 50,000 to 100,000 are not the "
                       "figures NCERT gives for amylose.",
      ncert=f"{NC12}, 'Biomolecules', polysaccharides: starch", seconds=25),

    Q(T_BM, "Vitamins", "Basic", "match_list",
      *ml("Match the vitamin in List-I with its sources, as given in NCERT, in List-II.",
          ["Vitamin A", "Vitamin B₁ (thiamine)", "Vitamin B₂ (riboflavin)", "Vitamin K"],
          ["Green leafy vegetables", "Milk, egg white, liver, kidney", "Fish liver oil, carrots, butter and milk",
           "Yeast, milk, green vegetables and cereals"],
          "III IV II I", ["IV III II I", "III II IV I", "III IV I II"], "D"),
      "Sources of vitamins",
      "NCERT's table of vitamins lists: A — fish liver oil, carrots, butter and milk; B₁ — yeast, milk, green "
      "vegetables and cereals; B₂ — milk, egg white, liver, kidney; K — green leafy vegetables.",
      ["A → III", "B₁ → IV", "B₂ → II", "K → I"],
      why_others_wrong="Codes that swap B₁ and B₂ or A and B₁ mix up two lists that both contain milk; the last code "
                       "gives vitamin K the animal sources of riboflavin.",
      ncert=f"{NC12}, 'Biomolecules', vitamins: sources and deficiency diseases", seconds=40),

    Q(T_BM, "Amino acids and proteins", "Basic", "statement_pair",
      *sp("In the zwitter ionic form, amino acids show amphoteric behaviour, as they react with both acids and "
          "bases.", True,
          "Most naturally occurring α-amino acids have the L-configuration.", True),
      "Properties of amino acids",
      "In water the –COOH group loses a proton and the –NH₂ group gains one, giving a dipolar ion (zwitterion). It "
      "can accept a proton (acting as a base) through –COO⁻ or give one (acting as an acid) through –NH₃⁺. All "
      "naturally occurring α-amino acids except glycine are optically active, and most of them have the "
      "L-configuration.",
      ["Statement I: true", "Statement II: true"],
      ncert=f"{NC12}, 'Biomolecules', amino acids: properties", seconds=30),

    Q(T_BM, "Carbohydrates", "Basic", "assertion_reason",
      *ar("Sucrose reduces Tollens' reagent.", False,
          "On hydrolysis, sucrose gives glucose and fructose.", True),
      "Non-reducing nature of sucrose",
      "In sucrose, C1 of α-D-glucose is joined to C2 of β-D-fructose, so the reducing groups of both units are used "
      "up in the glycosidic bond; sucrose is a non-reducing sugar and does not reduce Tollens' reagent. R is a true "
      "statement about its hydrolysis (to invert sugar). A is false.",
      ["A: false (non-reducing sugar)", "R: true"],
      ncert=f"{NC12}, 'Biomolecules', disaccharides: sucrose", seconds=30),

    N(T_BM, "Nucleic acids", "Intermediate",
      "In a nucleic acid strand, successive nucleotides are joined by phosphodiester linkages between the 5′ and 3′ "
      "carbon atoms of their pentose sugars. How many phosphodiester linkages are present in a linear, "
      "double-stranded DNA segment of 50 base pairs?",
      ["49", v_2482, "50", "100"], "B", v_2482,
      "Phosphodiester linkages in a polynucleotide",
      "A linear strand of n nucleotides has n − 1 linkages between neighbouring nucleotides. A double-stranded "
      "segment of 50 base pairs has two strands of 50 nucleotides each. Base pairing between the strands is by "
      "hydrogen bonds, not phosphodiester linkages.",
      ["One strand: 50 − 1 = 49", "Two strands: 2 × 49 = 98"],
      why_others_wrong="49 counts only one strand; 50 and 100 count one linkage per nucleotide, which would be true "
                       "only for a circular strand.",
      ncert=f"{NC12}, 'Biomolecules', structure of nucleic acids", seconds=45),

    Q(T_BM, "Amino acids and proteins", "Intermediate", "direct",
      "In the dipeptide glycylalanine (Gly–Ala), the carboxyl group of glycine is joined to the amino group of "
      "alanine. By the same convention, in the tripeptide Gly–Ala–Val, the amino acid residue that carries the free "
      "α-amino (–NH₂) group is:",
      ["Glycine", "Alanine", "Valine", "None; all the α-amino groups are used in peptide bonds"], "A",
      "Writing peptides",
      "In Gly–Ala–Val, the –COOH of glycine forms a peptide bond with the –NH₂ of alanine, and the –COOH of alanine "
      "with the –NH₂ of valine. The –NH₂ of glycine remains free, and the –COOH of valine remains free.",
      ["Gly(–NH₂ free)–CO–NH–Ala–CO–NH–Val(–COOH free)"],
      why_others_wrong="Alanine's amino group and valine's amino group are both used in peptide bonds; a linear "
                       "peptide always keeps one free amino group at one end.",
      ncert=f"{NC12}, 'Biomolecules', proteins: peptide bond", seconds=35),

    Q(T_BM, "Amino acids and proteins", "Intermediate", "assertion_reason",
      *ar("A protein loses its biological activity on denaturation.", True,
          "During denaturation, the secondary and tertiary structures of the protein are destroyed, although its "
          "primary structure remains intact.", True, explains=True),
      "Denaturation of proteins",
      "A native protein owes its biological activity to its unique three-dimensional structure. A change in "
      "temperature or pH disturbs the hydrogen bonds; the globules unfold and the helix uncoils, destroying the "
      "secondary and tertiary structures, and the protein loses its biological activity. R explains A.",
      ["Activity depends on the 3-D (2° and 3°) structure", "Denaturation destroys 2° and 3° structure → activity lost"],
      ncert=f"{NC12}, 'Biomolecules', denaturation of proteins", seconds=35),

    Q(T_BM, "Carbohydrates", "Intermediate", "statement_pair",
      *sp("Glycogen is less highly branched than amylopectin.", False,
          "Cellulose is a straight-chain polysaccharide made of α-D-glucose units.", False),
      "Glycogen and cellulose",
      "Glycogen, the animal starch, has a structure similar to amylopectin but is more highly branched. Cellulose "
      "is a straight-chain polysaccharide made only of β-D-glucose units, joined by glycosidic linkages between C1 "
      "of one unit and C4 of the next.",
      ["Statement I: false (glycogen is more branched)", "Statement II: false (β-D-glucose)"],
      ncert=f"{NC12}, 'Biomolecules', polysaccharides: cellulose and glycogen", seconds=35),

    Q(T_BM, "Nucleic acids", "Intermediate", "multi_statement",
      *ms("Which of the following statements about nucleic acids are correct?",
          [("Nucleic acids are long-chain polymers of nucleotides and are therefore also called polynucleotides.",
            True),
           ("The sugar in DNA is β-D-2-deoxyribose, whereas the sugar in RNA is β-D-ribose.", True),
           ("Cytosine is present in both DNA and RNA.", True),
           ("In a nucleotide, the phosphoric acid is linked to the 1′ position of the pentose sugar.", False),
           ("A nucleoside contains a base, a pentose sugar and a phosphate group.", False)],
          [["a", "b", "d"], ["b", "c", "e"], ["a", "b", "c", "d"]], "D"),
      "Chemical composition of nucleic acids",
      "Nucleic acids are polynucleotides. DNA contains β-D-2-deoxyribose and RNA β-D-ribose; cytosine and the two "
      "purines occur in both, while thymine is only in DNA and uracil only in RNA. The base is attached at C-1′ of "
      "the sugar (nucleoside); the phosphoric acid is esterified at C-5′ (nucleotide).",
      ["(a) true", "(b) true", "(c) true", "(d) false: phosphate at 5′", "(e) false: that is a nucleotide"],
      why_others_wrong="Options with (d) put the phosphate where the base is attached; options with (e) confuse a "
                       "nucleoside with a nucleotide.",
      ncert=f"{NC12}, 'Biomolecules', chemical composition and structure of nucleic acids", seconds=50),

    N(T_BM, "Nucleic acids", "Advanced",
      "A linear double-stranded DNA molecule contains 1000 nucleotides, of which 22% are guanine. An A–T pair is "
      "held by two hydrogen bonds and a G–C pair by three. The total number of hydrogen bonds between the two "
      "strands is:",
      [v_2487, "1110", "1280", "1500"], "A", v_2487,
      "Complementary base pairing",
      "In double-stranded DNA, G pairs with C and A with T, so the number of G–C pairs equals the number of G "
      "nucleotides. 1000 nucleotides make 500 base pairs.",
      ["G = 22% of 1000 = 220 → 220 G–C pairs", "A–T pairs = 500 − 220 = 280",
       "H bonds = 2 × 280 + 3 × 220 = 560 + 660 = 1220"],
      why_others_wrong="1280 swaps the numbers of A–T and G–C pairs; 1110 takes 22% of the 500 pairs as G–C pairs; "
                       "1500 assumes three hydrogen bonds for every pair.",
      ncert=f"{NC12}, 'Biomolecules', structure of DNA", seconds=75),

    Q(T_BM, "Carbohydrates", "Advanced", "match_list",
      *ml("Match the carbohydrate in List-I with the product(s) of its complete hydrolysis in List-II.",
          ["Sucrose", "Lactose", "Cellulose", "Amylose"],
          ["α-D-Glucose only", "D-Glucose and D-galactose", "D-Glucose and D-fructose", "β-D-Glucose only"],
          "III II IV I", ["III II I IV", "II III IV I", "III IV II I"], "C"),
      "Monosaccharide units of di- and polysaccharides",
      "Sucrose is made of α-D-glucose and β-D-fructose; lactose of β-D-galactose and β-D-glucose; cellulose only of "
      "β-D-glucose units; amylose only of α-D-glucose units.",
      ["Sucrose → glucose + fructose", "Lactose → galactose + glucose", "Cellulose → β-D-glucose",
       "Amylose → α-D-glucose"],
      why_others_wrong="Swapping cellulose and amylose confuses the α and β linkages of starch and cellulose; "
                       "swapping sucrose and lactose mixes up fructose and galactose.",
      ncert=f"{NC12}, 'Biomolecules', disaccharides and polysaccharides", seconds=50),

    Q(T_BM, "Carbohydrates", "Advanced", "multi_statement",
      *ms("Which of the following conclusions about the structure of glucose are correctly drawn from the "
          "observation stated?",
          [("Glucose forms a pentaacetate with acetic anhydride, so it contains five –OH groups.", True),
           ("Prolonged heating with HI gives n-hexane, so the six carbon atoms are linked in a straight chain.",
            True),
           ("Glucose exists in two crystalline forms, α and β, which the open-chain structure cannot explain.", True),
           ("α-D-Glucose and β-D-glucose differ in the configuration at C-5.", False),
           ("Bromine water oxidises glucose to gluconic acid, so glucose contains a ketonic carbonyl group.", False)],
          [["a", "b", "d"], ["c", "d", "e"], ["a", "b", "c", "e"]], "B"),
      "Evidence for the structure of glucose",
      "Acetylation to a pentaacetate shows five –OH groups; reduction to n-hexane shows a straight six-carbon chain; "
      "the α and β forms (anomers) need the cyclic hemiacetal structure. The anomers differ at C-1, the anomeric "
      "carbon. Oxidation by the mild oxidant bromine water to gluconic acid, a six-carbon acid, shows an aldehyde "
      "group.",
      ["(a) true", "(b) true", "(c) true", "(d) false: they differ at C-1", "(e) false: an aldehyde group"],
      why_others_wrong="Options with (d) put the anomeric difference at the ring-closing carbon C-5; options with (e) "
                       "reverse the meaning of the bromine water test.",
      ncert=f"{NC12}, 'Biomolecules', structure of glucose", seconds=70),

    Q(T_BM, "Amino acids and proteins", "Advanced", "multi_statement",
      *ms("Which of the following statements about the structure of proteins are correct?",
          [("The primary structure is the sequence of amino acids, and any change in this sequence creates a "
            "different protein.", True),
           ("Quaternary structure is found only in proteins made up of two or more polypeptide chains (subunits).",
            True),
           ("Denaturation of a protein hydrolyses its peptide bonds.", False),
           ("In the α-helix, the –NH group of each amino acid residue is hydrogen bonded to the >C=O of an adjacent "
            "turn of the helix.", True),
           ("Globular proteins such as insulin are usually insoluble in water.", False)],
          [["a", "b", "c"], ["a", "d", "e"], ["b", "c", "d"]], "C"),
      "Levels of protein structure",
      "Primary structure = amino acid sequence; changing it gives a different protein. Quaternary structure is the "
      "spatial arrangement of two or more subunits. In the α-helix, the chain twists into a right-handed screw with "
      "–NH···O=C hydrogen bonds between successive turns. Denaturation destroys 2° and 3° structure but leaves the "
      "peptide bonds (primary structure) intact. Globular proteins are usually water soluble.",
      ["(a) true", "(b) true", "(c) false", "(d) true", "(e) false"],
      why_others_wrong="Options with (c) treat denaturation as hydrolysis; the option with (e) gives globular proteins "
                       "the solubility of fibrous ones.",
      ncert=f"{NC12}, 'Biomolecules', structure of proteins", seconds=60),
]

# ================================================================ Principles Related to Practical Chemistry (2491-2500)
# 2491: lyophilic sols among the listed substances
lyo_2491 = {"starch": True, "gum": True, "egg albumin": True, "ferric hydroxide": False,
            "arsenious sulphide": False, "aluminium hydroxide": False}
v_2491 = str(sum(lyo_2491.values()))
assert v_2491 == "3"
# 2494: anions that give a gas when warmed with dilute H2SO4: CO3 2- (CO2), S 2- (H2S), NO2- (NO2 fumes)
dil_2494 = {"CO3": True, "S": True, "NO2": True, "SO4": False, "NO3": False, "Cl": False, "Br": False, "I": False}
v_2494 = str(sum(dil_2494.values()))
assert v_2494 == "3"
# 2495: 0.535 g NH4Cl -> NH3 (with NaOH) -> neutralised by 0.10 M HCl
n_2495 = F(535, 1000) / mm(N=1, H=4, Cl=1)
V_2495 = n_2495 / F(1, 10) * 1000
assert mm(N=1, H=4, Cl=1) == F(535, 10) and n_2495 == F(1, 100) and V_2495 == 100
v_2495 = "100 mL"
# 2498: rate = k[H2O2]^x [I-]^y from three experiments
exps = [(F(1, 100), F(2, 100), F(2, 10**6)), (F(2, 100), F(2, 100), F(4, 10**6)), (F(2, 100), F(4, 100), F(8, 10**6))]
x = exps[1][2] / exps[0][2]  # [H2O2] doubled
y = exps[2][2] / exps[1][2]  # [I-] doubled
assert x == 2 and y == 2  # first order in each
k_2498 = exps[0][2] / (exps[0][0] * exps[0][1])
assert k_2498 == F(1, 100) and all(r / (a * b) == k_2498 for a, b, r in exps)
assert exps[0][2] / exps[0][0] == F(2, 10**4) and exps[0][2] / exps[0][1] == F(1, 10**4)
assert exps[0][2] / (exps[0][0] * exps[0][1] ** 2) == F(5, 10)
v_2498 = "1.0 × 10⁻² L mol⁻¹ s⁻¹"

QUESTIONS += [
    N(T_PR, "Preparations", "Basic",
      "In the laboratory, sols are prepared of the following substances. How many of them form lyophilic sols?\n"
      "Starch, gum, egg albumin, ferric hydroxide, arsenious sulphide, aluminium hydroxide",
      ["1", "2", v_2491, "4"], "C", v_2491,
      "Lyophilic and lyophobic sols",
      "Lyophilic sols are formed directly by warming and stirring substances such as starch, gum and egg albumin "
      "with water. Ferric hydroxide, aluminium hydroxide and arsenious sulphide give lyophobic sols, which need "
      "special methods (hydrolysis, double decomposition).",
      ["Lyophilic: starch, gum, egg albumin → 3", "Lyophobic: Fe(OH)₃, As₂S₃, Al(OH)₃"],
      why_others_wrong="Counts of 1 or 2 miss gum or egg albumin; 4 counts a metal hydroxide sol, which is "
                       "lyophobic.",
      ncert=f"{LAB}, preparation of lyophilic and lyophobic sols", seconds=30),

    Q(T_PR, "Preparations", "Basic", "direct",
      "In the laboratory, a lyophobic sol of arsenious sulphide, As₂S₃, is prepared by:",
      ["adding iron(III) chloride solution drop by drop to boiling water",
       "passing hydrogen sulphide gas through a dilute aqueous solution of arsenious oxide",
       "warming arsenious oxide with water and stirring well",
       "adding sodium hydroxide solution to aluminium sulphate solution"], "B",
      "Preparation of a lyophobic sol by double decomposition",
      "Arsenious sulphide sol is made by a chemical reaction: H₂S is passed through a dilute solution of As₂O₃ in "
      "water, As₂O₃ + 3H₂S → As₂S₃ (sol) + 3H₂O.",
      ["As₂O₃ + 3H₂S → As₂S₃ (colloidal) + 3H₂O"],
      why_others_wrong="FeCl₃ in boiling water gives a ferric hydroxide sol; simply warming and stirring works only "
                       "for lyophilic substances; NaOH with aluminium sulphate gives a precipitate of Al(OH)₃.",
      ncert=f"{LAB}, preparation of lyophobic sols", seconds=30),

    Q(T_PR, "Titrimetric analysis", "Basic", "statement_pair",
      *sp("Phenolphthalein is colourless in acidic solution and pink in alkaline solution.", True,
          "Methyl orange is red in acidic solution and yellow in alkaline solution.", True),
      "Acid–base indicators",
      "Phenolphthalein is colourless in acid and turns pink in alkali; methyl orange is red in acid and yellow in "
      "alkali. These colour changes are used to detect the end points of acid–base titrations.",
      ["Statement I: true", "Statement II: true"],
      ncert=f"{LAB}, titrimetric analysis: indicators", seconds=25),

    N(T_PR, "Qualitative salt analysis", "Intermediate",
      "In salt analysis, a little of each salt is warmed with dilute H₂SO₄. How many of the following anions give a "
      "gas under these conditions?\nCO₃²⁻, S²⁻, NO₂⁻, SO₄²⁻, NO₃⁻, Cl⁻, Br⁻, I⁻",
      ["2", v_2494, "4", "5"], "B", v_2494,
      "Dilute sulphuric acid group of anions",
      "Carbonate gives CO₂ (turns lime water milky), sulphide gives H₂S (turns lead acetate paper black) and nitrite "
      "gives brown fumes of NO₂ with dilute H₂SO₄. Nitrate, chloride, bromide and iodide react only with "
      "concentrated H₂SO₄; sulphate does not react.",
      ["Dilute H₂SO₄ group: CO₃²⁻, S²⁻, NO₂⁻ → 3",
       "Concentrated H₂SO₄ group: NO₃⁻, Cl⁻, Br⁻, I⁻; SO₄²⁻: neither"],
      why_others_wrong="2 usually forgets the nitrite ion; 4 or 5 add halides or nitrate, which need concentrated "
                       "H₂SO₄.",
      ncert=f"{LAB}, qualitative analysis: tests for anions", seconds=40),

    N(T_PR, "Qualitative salt analysis", "Intermediate",
      "In the test for NH₄⁺, 0.535 g of ammonium chloride is heated with an excess of NaOH solution, and all the "
      "ammonia evolved is absorbed in 0.10 M HCl. The volume of the acid exactly neutralised is (N = 14, H = 1, "
      "Cl = 35.5):",
      ["10 mL", "50 mL", "200 mL", v_2495], "D", v_2495,
      "Ammonia from ammonium salts",
      "NH₄Cl + NaOH → NaCl + NH₃ + H₂O; NH₃ + HCl → NH₄Cl. One mole of ammonium chloride gives one mole of NH₃, "
      "which neutralises one mole of HCl.",
      ["NH₄Cl: 0.535 / 53.5 = 0.010 mol → 0.010 mol NH₃", "HCl: 0.010 mol / 0.10 M = 0.10 L = 100 mL"],
      why_others_wrong="50 mL halves the ammonia; 200 mL doubles it; 10 mL uses the molarity as 1.0 M.",
      ncert=f"{LAB}, qualitative analysis: test for ammonium ion", seconds=40),

    Q(T_PR, "Thermochemistry and kinetics experiments", "Intermediate", "statement_pair",
      *sp("In the reaction of iodide ions with hydrogen peroxide in acidic solution at room temperature, the rate "
          "increases when the concentration of iodide ions is increased.", True,
          "The rate of this reaction does not depend on the concentration of hydrogen peroxide.", False),
      "Kinetics of the iodide–hydrogen peroxide reaction",
      "The reaction H₂O₂ + 2I⁻ + 2H⁺ → I₂ + 2H₂O follows the rate law rate = k[H₂O₂][I⁻] under the experimental "
      "conditions, so the rate rises with an increase in the concentration of either reactant.",
      ["Statement I: true", "Statement II: false; first order in H₂O₂"],
      ncert=f"{LAB}, chemical kinetics: reaction of iodide ions with hydrogen peroxide", seconds=35),

    Q(T_PR, "Preparations", "Intermediate", "match_list",
      *ml("Match the compound prepared in the laboratory (List-I) with the starting materials used (List-II).",
          ["Mohr's salt", "Potash alum", "p-Nitroacetanilide", "Iodoform"],
          ["Acetanilide, with a mixture of concentrated HNO₃ and concentrated H₂SO₄",
           "Ethanol or acetone, warmed with iodine and alkali",
           "Iron(II) sulphate and ammonium sulphate, with a little dilute H₂SO₄",
           "Potassium sulphate and aluminium sulphate"],
          "III IV I II", ["IV III I II", "III IV II I", "I IV III II"], "A"),
      "Laboratory preparations",
      "Mohr's salt crystallises from an equimolar solution of FeSO₄ and (NH₄)₂SO₄ (dilute H₂SO₄ prevents "
      "hydrolysis); potash alum from K₂SO₄ and Al₂(SO₄)₃; p-nitroacetanilide by nitrating acetanilide; iodoform by "
      "the haloform reaction of ethanol or acetone with iodine and alkali.",
      ["A → III", "B → IV", "C → I", "D → II"],
      why_others_wrong="Swapping Mohr's salt and potash alum confuses the two double sulphates; swapping "
                       "p-nitroacetanilide and iodoform pairs a nitration with a haloform reaction.",
      ncert=f"{LAB}, preparation of inorganic and organic compounds", seconds=40),

    N(T_PR, "Thermochemistry and kinetics experiments", "Advanced",
      "The initial rate of the reaction H₂O₂ + 2I⁻ + 2H⁺ → I₂ + 2H₂O was measured at room temperature at a fixed, "
      "excess acidity:\n"
      "Experiment 1: [H₂O₂] = 0.010 M, [I⁻] = 0.020 M, rate = 2.0 × 10⁻⁶ mol L⁻¹ s⁻¹\n"
      "Experiment 2: [H₂O₂] = 0.020 M, [I⁻] = 0.020 M, rate = 4.0 × 10⁻⁶ mol L⁻¹ s⁻¹\n"
      "Experiment 3: [H₂O₂] = 0.020 M, [I⁻] = 0.040 M, rate = 8.0 × 10⁻⁶ mol L⁻¹ s⁻¹\n"
      "The rate constant of the reaction is:",
      ["2.0 × 10⁻⁴ s⁻¹", "1.0 × 10⁻⁴ s⁻¹", v_2498, "5.0 × 10⁻¹ L² mol⁻² s⁻¹"], "C", v_2498,
      "Finding orders and the rate constant from initial rates",
      "Compare experiments in which only one concentration changes to find each order, then substitute any one "
      "experiment into the rate law.",
      ["Exp 1 → 2: [H₂O₂] doubled, rate doubled → first order in H₂O₂",
       "Exp 2 → 3: [I⁻] doubled, rate doubled → first order in I⁻",
       "k = 2.0 × 10⁻⁶ / (0.010 × 0.020) = 1.0 × 10⁻² L mol⁻¹ s⁻¹"],
      why_others_wrong="2.0 × 10⁻⁴ s⁻¹ and 1.0 × 10⁻⁴ s⁻¹ treat the reaction as first order overall in one reactant "
                       "only; 5.0 × 10⁻¹ L² mol⁻² s⁻¹ assumes second order in iodide.",
      ncert=f"{LAB}, chemical kinetics: reaction of iodide ions with hydrogen peroxide", seconds=90),

    Q(T_PR, "Qualitative salt analysis", "Advanced", "assertion_reason",
      *ar("Zn²⁺ is precipitated as ZnS when H₂S is passed through its ammoniacal solution, but not when H₂S is passed "
          "through its solution acidified with dilute HCl.", True,
          "In ammoniacal solution the ionisation of H₂S increases, so the sulphide ion concentration becomes high "
          "enough for the ionic product of ZnS to exceed its solubility product.", True, explains=True),
      "Group separation by control of sulphide ion concentration",
      "H₂S ⇌ 2H⁺ + S²⁻. In dilute HCl the common ion H⁺ suppresses ionisation, and [S²⁻] is so low that only sulphides "
      "with very low Ksp (group II) precipitate. NH₄OH removes H⁺, increasing ionisation and [S²⁻], so ZnS (higher "
      "Ksp, group IV) precipitates. R explains A.",
      ["Acidic: low [S²⁻] → ionic product of ZnS < Ksp", "Ammoniacal: high [S²⁻] → ionic product > Ksp → ZnS"],
      ncert=f"{LAB}, qualitative analysis of cations: group IV", seconds=50),

    Q(T_PR, "Thermochemistry and kinetics experiments", "Advanced", "multi_statement",
      *ms("The enthalpy of neutralisation of hydrochloric acid by sodium hydroxide is determined by mixing equal "
          "volumes of the two solutions, of the same molarity, in a calorimeter. Which of the following statements "
          "are correct?",
          [("Using 1.0 M solutions instead of 0.5 M solutions (same volumes) gives a larger rise in temperature.",
            True),
           ("Using half the volumes of the same solutions gives about half the rise in temperature.", False),
           ("The heat capacity of the calorimeter must be taken into account to get an accurate value.", True),
           ("Per mole of water formed, about the same value is obtained if nitric acid is used instead of "
            "hydrochloric acid.", True),
           ("The enthalpy of neutralisation of ethanoic acid by NaOH is more negative than that of HCl by NaOH.",
            False)],
          [["a", "b", "c"], ["c", "d", "e"], ["a", "b", "d", "e"]], "B"),
      "Calorimetric determination of the enthalpy of neutralisation",
      "Doubling the concentrations doubles the heat released into the same mass of solution, so ΔT is larger. "
      "Halving both volumes halves both the heat released and the mass to be heated, so ΔT stays about the same "
      "(ignoring the calorimeter). Part of the heat warms the calorimeter, so its heat capacity is needed. Any strong "
      "acid with a strong base gives about −57 kJ per mole of water. A weak acid such as ethanoic acid gives a less "
      "negative value, because some heat is used to ionise it.",
      ["(a) true", "(b) false: ΔT is about the same", "(c) true", "(d) true", "(e) false: less negative"],
      why_others_wrong="Options with (b) forget that the mass of solution is halved along with the heat; options "
                       "with (e) reverse the weak-acid effect.",
      ncert=f"{LAB}, thermochemistry: enthalpy of neutralisation", seconds=75),
]

# ---------------------------------------------------------------- package checks and output
PLAN = {T_CC: (5, 6, 5), T_PU: (2, 3, 2), T_GO: (6, 8, 6), T_HC: (5, 6, 5), T_HX: (4, 5, 4), T_OX: (6, 8, 6),
        T_NI: (4, 5, 4), T_BM: (4, 5, 4), T_PR: (3, 4, 3)}
TOTAL = LAST - FIRST + 1

if __name__ == "__main__":
    assert len(QUESTIONS) == TOTAL == 128, len(QUESTIONS)
    assert [x["question_id"] for x in QUESTIONS] == [f"NEET_CHE_{n:06d}" for n in range(FIRST, LAST + 1)]
    have = Counter((x["topic"], x["difficulty"]) for x in QUESTIONS)
    for topic, quota in PLAN.items():
        for diff, n in zip(("Basic", "Intermediate", "Advanced"), quota):
            assert have[(topic, diff)] == n, (topic, diff, have[(topic, diff)], n)
    assert sum(have.values()) == sum(sum(v) for v in PLAN.values())
    keys = Counter(x["correct_answer"] for x in QUESTIONS)
    fmts = Counter(x["format"] for x in QUESTIONS)
    print("keys", dict(sorted(keys.items())), "formats", dict(fmts))
    assert all(28 <= keys[k] <= 36 for k in LETTERS), keys
    assert 0.27 <= fmts["numerical"] / TOTAL <= 0.33, fmts
    assert all(fmts[f] / TOTAL >= 0.08 for f in fmts if f != "numerical") and len(fmts) == 6, fmts
    for x in QUESTIONS:  # every numerical answer is recomputed above
        assert (x["format"] == "numerical") == ("script:recompute" in x["verification"]["verified_by"]), x["question_id"]
    doc = {"schema_version": "1.0", "batch_id": "BATCH_010", "created_at": TODAY,
           "notes": "Package CHE_010_p2: 128 original Chemistry questions (coordination compounds, purification and "
                    "characterisation, basic principles of organic chemistry, hydrocarbons, halogen, oxygen and "
                    "nitrogen compounds, biomolecules, practical chemistry). Numerical answers recomputed by "
                    "tools/batch_010/CHE_010_p2.py.",
           "stimuli": [], "questions": QUESTIONS}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {OUT}: {dict(Counter(x['difficulty'] for x in QUESTIONS))}, keys {dict(sorted(keys.items()))}, "
          f"formats {dict(fmts)}")
