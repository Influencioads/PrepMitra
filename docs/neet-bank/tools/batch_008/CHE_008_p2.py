"""Writes batches/parts/BATCH_008_CHE_p2.json: package CHE_008_p2 of BATCH_008 (Chemistry, 127 questions).

Topics: Coordination Compounds, Purification and Characterisation of Organic Compounds, Some Basic Principles of
Organic Chemistry, Hydrocarbons, Organic Compounds Containing Halogens / Oxygen / Nitrogen, Biomolecules (Chemistry),
Principles Related to Practical Chemistry. IDs NEET_CHE_001874..NEET_CHE_002000.

Every numerical answer is re-derived below with an assert; multi-statement keys are derived from the truth value of
each statement, assertion-reason and statement-pair keys from the truth of each part. If any check fails, nothing is
written.

    python docs/neet-bank/tools/batch_008/CHE_008_p2.py
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
OUT = ROOT / "batches" / "parts" / "BATCH_008_CHE_p2.json"
TODAY = "2026-11-16"
LETTERS = "ABCD"
CHE = "Chemistry"
FIRST, LAST = 1874, 2000
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
      "Ca": 40, "Ba": 137, "P": 31}


def mm(**atoms):
    """Molar mass from atom counts, e.g. mm(C=2, H=6, O=1)."""
    return sum(AM[k] * v for k, v in atoms.items())


def bm(n):
    """Spin-only magnetic moment sqrt(n(n+2)) in BM."""
    return math.sqrt(n * (n + 2))


QUESTIONS = []

# ================================================================ Coordination Compounds (1874-1888)
# 1875: [CoF6]3-: Co3+ = 3d6, weak field -> t2g4 eg2 -> 4 unpaired
v_1875 = f"{bm(4):.2f} BM"
assert v_1875 == "4.90 BM" and f"{bm(3):.2f}" == "3.87" and f"{bm(5):.2f}" == "5.92"
# 1878: chiral species among six (True = chiral)
chiral = {"cis-[CrCl2(ox)2]3-": True, "trans-[CrCl2(ox)2]3-": False, "[Fe(ox)3]3-": True,
          "cis-[Pt(NH3)2Cl2]": False, "fac-[Co(NH3)3Cl3]": False, "cis-[Co(NH3)2(en)2]3+": True}
v_1878 = str(sum(chiral.values()))
assert v_1878 == "3"
# 1884: octahedral complexes with eg empty: (d electrons, strong field?)
def octa(d, strong):
    """(t2g, eg) occupation of an octahedral d^n ion."""
    if strong:
        t = min(d, 6)
        return t, d - t
    order = [0, 0, 0, 1, 1, 0, 0, 0, 1, 1]  # 0 = t2g, 1 = eg (Hund filling, high spin)
    eg = sum(order[:d])
    return d - eg, eg
cpx = {"[Co(NH3)6]3+": (6, True), "[Fe(CN)6]4-": (6, True), "[Cr(H2O)6]3+": (3, False), "[Fe(H2O)6]3+": (5, False),
       "[CoF6]3-": (6, False), "[Ti(H2O)6]3+": (1, False), "[Ni(NH3)6]2+": (8, True), "[Mn(CN)6]3-": (4, True)}
v_1884 = str(sum(1 for d, s in cpx.values() if octa(d, s)[1] == 0))
assert v_1884 == "5" and octa(8, True) == (6, 2) and octa(5, False) == (3, 2) and octa(6, False) == (4, 2)
# 1885: ions per formula unit: potash alum K2SO4.Al2(SO4)3.24H2O -> 2K+ + 2Al3+ + 4SO4 2- ; K3[Al(C2O4)3] -> 3K+ + 1
alum_ions, cpx_ions = 2 + 2 + (1 + 3), 3 + 1
v_1885 = f"{alum_ions} and {cpx_ions}"
assert v_1885 == "8 and 4"
# 1886: CFT configurations
assert octa(1, False) == (1, 0) and octa(3, True) == (3, 0) and octa(5, False) == (3, 2) and octa(6, True) == (6, 0)

QUESTIONS += [
    Q(T_CC, "IUPAC nomenclature", "Basic", "direct",
      "The IUPAC name of [Ni(NH₃)₆]Cl₂ is:",
      ["Hexaamminenickelate(II) chloride", "Hexaamminenickel(II) chloride", "Hexaammonianickel(II) chloride",
       "Hexaamminenickel(IV) chloride"], "B",
      "Naming a complex cation",
      "The complex is a cation, so the metal keeps its ordinary name (no -ate ending). NH₃ as a ligand is 'ammine'. "
      "Two Cl⁻ counter ions balance the charge, so the complex ion is [Ni(NH₃)₆]²⁺ and nickel is +2.",
      ["Charge of complex ion = +2 (two Cl⁻ outside)", "x + 6(0) = +2 → Ni(II)",
       "NH₃ → ammine; cationic complex → 'nickel'", "Name: hexaamminenickel(II) chloride"],
      why_others_wrong="'-ate' is used only for anionic complexes; 'ammonia' is not the ligand name for NH₃; the "
                       "oxidation state of Ni is +2, not +4.",
      ncert=f"{NC12}, 'Coordination Compounds', nomenclature of coordination compounds", seconds=25),

    N(T_CC, "Crystal field theory", "Basic",
      "[CoF₆]³⁻ is a high-spin octahedral complex (atomic number of Co = 27). Its spin-only magnetic moment is about:",
      ["3.87 BM", "0 BM", "5.92 BM", "4.90 BM"], "D", v_1875,
      "Spin-only magnetic moment μ = √(n(n + 2)) BM",
      "Co³⁺ is 3d⁶. F⁻ is a weak field ligand (Δo < P), so the configuration is t₂g⁴ eg², with four unpaired electrons.",
      ["Co (27): [Ar] 3d⁷ 4s² → Co³⁺: 3d⁶", "Weak field: t₂g⁴ eg² → n = 4", "μ = √(4 × 6) = √24 ≈ 4.90 BM"],
      why_others_wrong="0 BM is the low-spin t₂g⁶ case (as in [Co(NH₃)₆]³⁺); 3.87 BM is for three unpaired electrons "
                       "and 5.92 BM for five.",
      ncert=f"{NC12}, 'Coordination Compounds', crystal field theory: octahedral complexes", seconds=40),

    Q(T_CC, "Werner's theory and ligands", "Basic", "match_list",
      *ml("For the compound K₃[Fe(C₂O₄)₃], match each term in List-I with the corresponding species or value in "
          "List-II.",
          ["Central ion", "Ligand", "Coordination number", "Counter ion"],
          ["K⁺", "Fe³⁺", "C₂O₄²⁻", "6"],
          "II III IV I", ["II IV III I", "III II IV I", "I III IV II"], "C"),
      "Terms used for coordination compounds",
      "Fe³⁺ is the central ion; each oxalate ion, C₂O₄²⁻, is a didentate ligand, so three of them give a coordination "
      "number of 6; the three K⁺ ions outside the square brackets are the counter ions.",
      ["Central ion: Fe³⁺ (II)", "Ligand: C₂O₄²⁻ (III)", "Coordination number: 3 × 2 = 6 (IV)", "Counter ion: K⁺ (I)"],
      why_others_wrong="Taking the coordination number as 3 (number of ligands) confuses it with the oxalate entry; "
                       "K⁺ is outside the coordination sphere and is not the central ion.",
      ncert=f"{NC12}, 'Coordination Compounds', definitions of some important terms", seconds=40),

    Q(T_CC, "Crystal field theory", "Basic", "assertion_reason",
      *ar("Aqueous solutions containing [Sc(H₂O)₆]³⁺ are colourless.", True,
          "Sc³⁺ has no d electron, so no d–d transition can take place.", True, explains=True),
      "Origin of colour in complexes",
      "In crystal field theory the colour of a complex comes from excitation of a d electron from a lower to a higher "
      "set of d orbitals (d–d transition). Sc³⁺ is 3d⁰, so no such transition is possible and visible light is not "
      "absorbed. R explains A.",
      ["Sc (21): [Ar] 3d¹ 4s² → Sc³⁺: 3d⁰", "No d electron → no d–d transition", "No absorption in the visible → colourless"],
      ncert=f"{NC12}, 'Coordination Compounds', colour in coordination compounds", seconds=30),

    N(T_CC, "Isomerism", "Intermediate",
      "How many of the following species are optically active (ox = oxalate, C₂O₄²⁻; en = ethane-1,2-diamine)?\n"
      "cis-[CrCl₂(ox)₂]³⁻, trans-[CrCl₂(ox)₂]³⁻, [Fe(ox)₃]³⁻, cis-[Pt(NH₃)₂Cl₂] (square planar), "
      "fac-[Co(NH₃)₃Cl₃], cis-[Co(NH₃)₂(en)₂]³⁺",
      ["2", "3", "4", "5"], "B", v_1878,
      "Optical isomerism in octahedral complexes with didentate ligands",
      "Octahedral complexes with two or three didentate ligands in a cis arrangement have no plane of symmetry and "
      "are chiral. A trans arrangement, a square planar complex and the fac isomer of [MA₃B₃] all have a mirror plane.",
      ["cis-[CrCl₂(ox)₂]³⁻: chiral", "trans-[CrCl₂(ox)₂]³⁻: mirror plane → inactive", "[Fe(ox)₃]³⁻: chiral (like [Co(en)₃]³⁺)",
       "cis-[Pt(NH₃)₂Cl₂]: planar → inactive", "fac-[Co(NH₃)₃Cl₃]: mirror plane → inactive",
       "cis-[Co(NH₃)₂(en)₂]³⁺: chiral", "Total = 3"],
      why_others_wrong="2 misses the tris(oxalato) complex; 4 counts the trans isomer; 5 also counts a planar or fac "
                       "species, which have mirror planes.",
      ncert=f"{NC12}, 'Coordination Compounds', stereoisomerism: optical isomerism", seconds=75),

    Q(T_CC, "Werner's theory and ligands", "Intermediate", "direct",
      "Which of the following contains a complex ion that is both homoleptic and anionic?",
      ["[Co(NH₃)₆]Cl₃", "[Co(NH₃)₄Cl₂]Cl", "K[Cr(H₂O)₂(C₂O₄)₂]", "K₃[Fe(CN)₆]"], "D",
      "Homoleptic and heteroleptic complexes; cationic and anionic complexes",
      "A homoleptic complex has only one kind of ligand. [Fe(CN)₆]³⁻ has only CN⁻ ligands and carries a negative "
      "charge, so it is homoleptic and anionic.",
      ["[Co(NH₃)₆]³⁺: homoleptic but cationic", "[Co(NH₃)₄Cl₂]⁺: heteroleptic, cationic",
       "[Cr(H₂O)₂(C₂O₄)₂]⁻: anionic but heteroleptic", "[Fe(CN)₆]³⁻: homoleptic and anionic"],
      why_others_wrong="Each of the other complex ions fails one of the two conditions, as shown in the steps.",
      ncert=f"{NC12}, 'Coordination Compounds', definitions of some important terms", seconds=40),

    Q(T_CC, "Crystal field theory", "Intermediate", "statement_pair",
      *sp("In the spectrochemical series, OH⁻ is a weaker field ligand than H₂O.", True,
          "Thiocyanate bonded through sulphur (SCN⁻) produces a larger crystal field splitting than thiocyanate "
          "bonded through nitrogen (NCS⁻).", False),
      "Spectrochemical series",
      "NCERT's series runs I⁻ < Br⁻ < SCN⁻ < Cl⁻ < S²⁻ < F⁻ < OH⁻ < C₂O₄²⁻ < H₂O < NCS⁻ < edta⁴⁻ < NH₃ < en < CN⁻ < CO. "
      "OH⁻ comes before H₂O, so it is the weaker field ligand (Statement I true). S-bonded SCN⁻ lies near the weak end "
      "and N-bonded NCS⁻ after H₂O, so NCS⁻ gives the larger splitting (Statement II false).",
      ["OH⁻ < C₂O₄²⁻ < H₂O → Statement I true", "SCN⁻ (weak end) < NCS⁻ → Statement II false"],
      ncert=f"{NC12}, 'Coordination Compounds', crystal field theory: spectrochemical series", seconds=45),

    Q(T_CC, "Valence bond theory", "Intermediate", "multi_statement",
      *ms("Which of the following statements about [Co(NH₃)₆]³⁺ and [CoF₆]³⁻ are correct (atomic number of Co = 27)?",
          [("In both complexes cobalt is in the +3 oxidation state with a 3d⁶ configuration.", True),
           ("[CoF₆]³⁻ is an outer orbital complex in which cobalt uses sp³d² hybrid orbitals.", True),
           ("[Co(NH₃)₆]³⁺ has four unpaired electrons.", False),
           ("Both complexes are octahedral.", True),
           ("F⁻ is a stronger field ligand than NH₃.", False)],
          [["a", "b"], ["a", "c", "d"], ["b", "d", "e"]], "B"),
      "Inner and outer orbital octahedral complexes of Co(III)",
      "Both are Co³⁺ (3d⁶), six-coordinate and octahedral. NH₃ pairs the 3d electrons, leaving two 3d orbitals free for "
      "d²sp³ hybridisation (inner orbital, diamagnetic). F⁻ is weak field, so the 4d orbitals are used (sp³d², outer "
      "orbital, four unpaired electrons).",
      ["(a) true", "(b) true: sp³d², outer orbital", "(c) false: [Co(NH₃)₆]³⁺ is diamagnetic", "(d) true",
       "(e) false: F⁻ is a weaker field ligand than NH₃"],
      ncert=f"{NC12}, 'Coordination Compounds', valence bond theory", seconds=60),

    Q(T_CC, "Werner's theory and ligands", "Intermediate", "match_list",
      *ml("Match the ligand in List-I with its description in List-II.",
          ["Ethane-1,2-diamine", "Oxalate ion", "Ethylenediaminetetraacetate ion", "Pyridine"],
          ["Anionic, didentate", "Neutral, unidentate", "Anionic, hexadentate", "Neutral, didentate"],
          "IV I III II", ["I IV III II", "IV I II III", "IV III I II"], "D"),
      "Charge and denticity of ligands",
      "en, H₂N–CH₂–CH₂–NH₂, is neutral and binds through both N atoms. C₂O₄²⁻ is a dianion that binds through two O "
      "atoms. EDTA⁴⁻ binds through two N and four O atoms. Pyridine, C₅H₅N, is neutral and binds only through N.",
      ["en → neutral, didentate (IV)", "C₂O₄²⁻ → anionic, didentate (I)", "EDTA⁴⁻ → anionic, hexadentate (III)",
       "Pyridine → neutral, unidentate (II)"],
      why_others_wrong="The other codes swap the neutral en and the anionic oxalate, or mix up the denticities of EDTA "
                       "and pyridine.",
      ncert=f"{NC12}, 'Coordination Compounds', definitions of some important terms: ligands", seconds=40),

    Q(T_CC, "Crystal field theory", "Intermediate", "assertion_reason",
      *ar("The crystal field splitting Δo of [CrCl₆]³⁻ is smaller than that of [Cr(NH₃)₆]³⁺.", True,
          "Cl⁻ lies before NH₃ in the spectrochemical series, i.e. it is a weaker field ligand.", True, explains=True),
      "Dependence of Δo on the ligand",
      "For the same metal ion in the same oxidation state (Cr³⁺) and the same geometry, Δo depends on the field "
      "strength of the ligand. Cl⁻ is a weaker field ligand than NH₃, so the splitting is smaller. R explains A.",
      ["Same metal, oxidation state and geometry", "Cl⁻ < NH₃ in the spectrochemical series", "→ Δo(CrCl₆³⁻) < Δo(Cr(NH₃)₆³⁺)"],
      ncert=f"{NC12}, 'Coordination Compounds', crystal field theory", seconds=35),

    N(T_CC, "Crystal field theory", "Advanced",
      "According to crystal field theory, in how many of the following octahedral complexes are the eg orbitals "
      "completely empty? (Atomic numbers: Ti 22, Cr 24, Mn 25, Fe 26, Co 27, Ni 28; [Mn(CN)₆]³⁻ is low spin.)\n"
      "[Co(NH₃)₆]³⁺, [Fe(CN)₆]⁴⁻, [Cr(H₂O)₆]³⁺, [Fe(H₂O)₆]³⁺, [CoF₆]³⁻, [Ti(H₂O)₆]³⁺, [Ni(NH₃)₆]²⁺, [Mn(CN)₆]³⁻",
      ["4", "6", "5", "3"], "C", v_1884,
      "Filling of t₂g and eg orbitals in octahedral complexes",
      "d¹–d³ ions always have empty eg orbitals. A d⁴–d⁶ ion keeps eg empty only with strong field ligands (low spin). "
      "A d⁸ ion must place two electrons in eg whatever the ligand, because t₂g holds only six.",
      ["[Co(NH₃)₆]³⁺ d⁶ LS: t₂g⁶ → empty", "[Fe(CN)₆]⁴⁻ d⁶ LS: t₂g⁶ → empty", "[Cr(H₂O)₆]³⁺ d³: t₂g³ → empty",
       "[Fe(H₂O)₆]³⁺ d⁵ HS: t₂g³ eg² → not empty", "[CoF₆]³⁻ d⁶ HS: t₂g⁴ eg² → not empty",
       "[Ti(H₂O)₆]³⁺ d¹ → empty", "[Ni(NH₃)₆]²⁺ d⁸: t₂g⁶ eg² → not empty", "[Mn(CN)₆]³⁻ d⁴ LS: t₂g⁴ → empty",
       "Total = 5"],
      why_others_wrong="6 assumes the strong field NH₃ empties eg in the d⁸ nickel complex; 4 misses the low-spin "
                       "manganese complex; 3 counts only the d¹ and d³ ions and one d⁶ ion.",
      ncert=f"{NC12}, 'Coordination Compounds', crystal field splitting in octahedral complexes", seconds=110),

    N(T_CC, "Werner's theory and ligands", "Advanced",
      "Potash alum, K₂SO₄·Al₂(SO₄)₃·24H₂O, is a double salt, whereas K₃[Al(C₂O₄)₃] is a coordination compound. "
      "Assuming complete dissociation of each in dilute aqueous solution, the numbers of ions given by one formula "
      "unit of potash alum and of K₃[Al(C₂O₄)₃] are, respectively:",
      ["8 and 4", "3 and 4", "8 and 7", "4 and 4"], "A", v_1885,
      "Double salts versus complexes in solution",
      "A double salt dissociates completely into simple ions in water. A complex ion keeps its identity, so only the "
      "counter ions separate from it.",
      ["Alum: 2K⁺ + 2Al³⁺ + 4SO₄²⁻ = 8 ions", "K₃[Al(C₂O₄)₃]: 3K⁺ + [Al(C₂O₄)₃]³⁻ = 4 ions"],
      why_others_wrong="'3 and 4' treats alum as a complex ion with two K⁺; '8 and 7' breaks the oxalato complex into "
                       "Al³⁺ and three C₂O₄²⁻; '4 and 4' uses the half formula KAl(SO₄)₂·12H₂O instead of the formula "
                       "unit given.",
      ncert=f"{NC12}, 'Coordination Compounds', Werner's theory: double salts and complexes", seconds=70),

    Q(T_CC, "Crystal field theory", "Advanced", "match_list",
      *ml("Match the octahedral complex ion in List-I with its d-electron configuration according to crystal field "
          "theory in List-II (atomic numbers: Ti 22, Cr 24, Fe 26, Co 27).",
          ["[Ti(H₂O)₆]³⁺", "[Cr(NH₃)₆]³⁺", "[Fe(H₂O)₆]³⁺", "[Co(NH₃)₆]³⁺"],
          ["t₂g⁶ eg⁰", "t₂g³ eg²", "t₂g¹ eg⁰", "t₂g³ eg⁰"],
          "III IV II I", ["III II IV I", "IV III II I", "III IV I II"], "B"),
      "Writing t₂g/eg configurations from oxidation state and ligand strength",
      "Find the d-electron count from the oxidation state, then fill t₂g first; for d⁴–d⁷ use the ligand strength to "
      "decide between high and low spin.",
      ["Ti³⁺ d¹ → t₂g¹ (III)", "Cr³⁺ d³ → t₂g³ (IV)", "Fe³⁺ d⁵ with weak field H₂O → t₂g³ eg² (II)",
       "Co³⁺ d⁶ with NH₃ (Δo > P, diamagnetic) → t₂g⁶ (I)"],
      why_others_wrong="'A-III, B-II, C-IV, D-I' gives Cr³⁺ five d electrons and Fe³⁺ three; 'A-IV, B-III, ...' swaps "
                       "the d¹ and d³ ions; 'A-III, B-IV, C-I, D-II' swaps the Fe³⁺ (d⁵) and Co³⁺ (d⁶) "
                       "configurations.",
      ncert=f"{NC12}, 'Coordination Compounds', crystal field splitting in octahedral complexes", seconds=80),

    Q(T_CC, "Valence bond theory", "Advanced", "statement_pair",
      *sp("[Ni(CN)₄]²⁻ and [Ni(CO)₄] are both diamagnetic, although nickel is in different oxidation states in them.",
          True,
          "[NiCl₄]²⁻ is square planar, because Cl⁻ is a strong field ligand that forces the 3d electrons to pair up.",
          False),
      "Four-coordinate nickel complexes in valence bond theory",
      "In [Ni(CN)₄]²⁻ (Ni²⁺, 3d⁸) the strong field CN⁻ pairs the d electrons, giving dsp², square planar and "
      "diamagnetic. In [Ni(CO)₄] (Ni⁰) all ten electrons pair in 3d, giving sp³, tetrahedral and diamagnetic. So "
      "Statement I is true. Cl⁻ is a weak field ligand: [NiCl₄]²⁻ is sp³, tetrahedral and paramagnetic with two "
      "unpaired electrons, so Statement II is false.",
      ["[Ni(CN)₄]²⁻: Ni(II), dsp², 0 unpaired", "[Ni(CO)₄]: Ni(0), sp³, 0 unpaired → Statement I true",
       "[NiCl₄]²⁻: weak field, sp³, tetrahedral, 2 unpaired → Statement II false"],
      ncert=f"{NC12}, 'Coordination Compounds', valence bond theory: tetrahedral and square planar complexes",
      seconds=55),

    Q(T_CC, "Isomerism", "Advanced", "multi_statement",
      *ms("Consider the complex K₃[Cr(C₂O₄)₃] (atomic number of Cr = 24). Which of the following statements are "
          "correct?",
          [("The oxidation state of chromium is +3.", True),
           ("The coordination number of chromium is 6.", True),
           ("The complex ion exists as a pair of enantiomers.", True),
           ("The complex ion has three unpaired electrons.", True),
           ("Its IUPAC name is potassium trioxalatochromium(III).", False)],
          [["a", "b", "c"], ["a", "b", "d", "e"], ["b", "c", "d"]], "D"),
      "Oxidation state, coordination number, optical isomerism and magnetism of a tris(chelate) complex",
      "x + 3(−2) = −3 gives Cr(III), 3d³. Three didentate oxalate ions give coordination number 6. Like [Co(en)₃]³⁺, "
      "a tris(didentate) octahedral ion is chiral. A d³ ion has t₂g³, three unpaired electrons. As the complex is an "
      "anion, the metal name ends in -ate: potassium trioxalatochromate(III).",
      ["(a) true", "(b) true", "(c) true", "(d) true", "(e) false: 'chromate(III)' for an anionic complex"],
      ncert=f"{NC12}, 'Coordination Compounds', nomenclature and isomerism", seconds=70),
]

# ================================================================ Purification and Characterisation (1889-1895)
# 1890: C 40.0 %, H 6.67 %, O 53.33 % -> CH2O
mol_ratio = [F(4000, 100) / 12, F(667, 100) / 1, F(5333, 100) / 16]
small = min(mol_ratio)
assert [round(float(x / small), 2) for x in mol_ratio] == [1.0, 2.0, 1.0]
v_1890 = "CH₂O"
# 1891: M from vapour: 0.88 g occupies 224 mL at STP -> 88 g/mol; C 54.55 %, H 9.09 %, O rest
M_1891 = F(88, 100) / F(224, 22400)
assert M_1891 == 88
nC, nH = round(88 * 0.5455 / 12), round(88 * 0.0909 / 1)
nO = (88 - 12 * nC - nH) // 16
assert (nC, nH, nO) == (4, 8, 2) and 12 * nC + nH + 16 * nO == 88
v_1891 = "C₄H₈O₂"
# 1894: Dumas 56 mL N2 at STP -> mol N atoms; Kjeldahl NH3 = mol N; 2NH3 + H2SO4 -> 1 : 2
nN = 2 * F(56, 22400)
v_mL = nN / 2 / F(1, 10) * 1000
assert v_mL == 25
v_1894 = "25 mL"

QUESTIONS += [
    Q(T_PU, "Qualitative analysis", "Basic", "direct",
      "The sodium fusion extract of an organic compound is acidified with acetic acid and lead acetate solution is "
      "added. A black precipitate forms. This shows the presence of:",
      ["Nitrogen", "Chlorine", "Sulphur", "Phosphorus"], "C",
      "Test for sulphur in Lassaigne's extract",
      "During sodium fusion, sulphur of the compound is converted into sodium sulphide. With lead acetate, sulphide "
      "ions give black lead sulphide: S²⁻ + Pb²⁺ → PbS (black).",
      ["Na + S (from compound) → Na₂S", "Na₂S + (CH₃COO)₂Pb → PbS↓ (black)"],
      why_others_wrong="Nitrogen is shown by Prussian blue, chlorine by a white AgCl precipitate, and phosphorus by "
                       "the yellow ammonium molybdate test.",
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', qualitative analysis: test for "
            f"sulphur", seconds=25),

    N(T_PU, "Quantitative analysis and formulae", "Basic",
      "An organic compound contains 40.0% carbon, 6.67% hydrogen and 53.33% oxygen by mass. Its empirical formula is "
      "(C = 12, H = 1, O = 16):",
      ["CH₂O", "CHO", "C₂H₄O", "CH₃O"], "A", v_1890,
      "Empirical formula from percentage composition",
      "Divide each percentage by the atomic mass and then by the smallest quotient.",
      ["C: 40.0/12 = 3.33", "H: 6.67/1 = 6.67", "O: 53.33/16 = 3.33", "Ratio C : H : O = 1 : 2 : 1 → CH₂O"],
      why_others_wrong="CHO ignores the factor 2 for hydrogen; C₂H₄O doubles C and H but not O; CH₃O misreads the "
                       "hydrogen ratio.",
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', quantitative analysis", seconds=40),

    N(T_PU, "Quantitative analysis and formulae", "Intermediate",
      "An organic compound containing only C, H and O has 54.55% carbon and 9.09% hydrogen by mass. 0.88 g of its "
      "vapour occupies 224 mL at STP. Its molecular formula is (C = 12, H = 1, O = 16; molar volume at STP = "
      "22400 mL):",
      ["C₂H₄O", "C₃H₄O₃", "C₅H₁₂O", "C₄H₈O₂"], "D", v_1891,
      "Molecular formula from percentage composition and molar mass",
      "Molar mass = mass / moles of vapour. Oxygen is found by difference. Then each element's share of the molar "
      "mass gives the number of atoms.",
      ["n = 224/22400 = 0.01 mol → M = 0.88/0.01 = 88 g mol⁻¹", "%O = 100 − 54.55 − 9.09 = 36.36",
       "C: 0.5455 × 88/12 = 4; H: 0.0909 × 88 = 8; O: 0.3636 × 88/16 = 2", "Molecular formula C₄H₈O₂"],
      why_others_wrong="C₂H₄O is only the empirical formula (M = 44); C₃H₄O₃ and C₅H₁₂O have M = 88 but the wrong "
                       "percentages of C and H.",
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', quantitative analysis", seconds=75),

    Q(T_PU, "Qualitative analysis", "Intermediate", "assertion_reason",
      *ar("Nitrogen, sulphur and halogens present in an organic compound cannot be detected directly with the usual "
          "reagents for their ions, so the compound is first fused with sodium.", True,
          "These elements are covalently bonded in organic compounds; fusion with sodium converts them into ionic "
          "compounds such as NaCN, Na₂S and NaX.", True, explains=True),
      "Purpose of sodium fusion (Lassaigne's test)",
      "Ionic tests (Prussian blue, nitroprusside, AgNO₃) need the elements as ions. Because they are covalently "
      "bonded in the compound, fusion with sodium is used to convert them into ionic salts, which are extracted "
      "with water. R explains A.",
      ["Elements covalently bonded → no ions to test", "Na fusion → NaCN, Na₂S, NaX", "Extract tested for ions"],
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', qualitative analysis", seconds=40),

    Q(T_PU, "Qualitative analysis", "Intermediate", "statement_pair",
      *sp("In the test for nitrogen, the sodium fusion extract is boiled with iron(II) sulphate and then acidified "
          "with concentrated sulphuric acid; on heating, some iron(II) ions are oxidised to iron(III) ions, which "
          "react with the hexacyanidoferrate(II) formed.", True,
          "The Prussian blue precipitate obtained in this test is iron(III) hexacyanidoferrate(II), "
          "Fe₄[Fe(CN)₆]₃·xH₂O.", True),
      "Chemistry of the Prussian blue test",
      "NaCN in the extract gives Na₄[Fe(CN)₆] with iron(II) sulphate. On heating with concentrated H₂SO₄, some Fe²⁺ "
      "is oxidised to Fe³⁺, "
      "which with [Fe(CN)₆]⁴⁻ gives Prussian blue, Fe₄[Fe(CN)₆]₃·xH₂O. Both statements are true.",
      ["6CN⁻ + Fe²⁺ → [Fe(CN)₆]⁴⁻", "Some Fe²⁺ → Fe³⁺ on heating", "3[Fe(CN)₆]⁴⁻ + 4Fe³⁺ → Fe₄[Fe(CN)₆]₃·xH₂O"],
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', test for nitrogen", seconds=45),

    N(T_PU, "Quantitative analysis and formulae", "Advanced",
      "In a Dumas determination, 0.30 g of an organic compound gave 56 mL of nitrogen gas, corrected to STP. If "
      "another 0.30 g of the same compound were analysed by Kjeldahl's method (assume the method is applicable), the "
      "ammonia evolved would exactly neutralise what volume of 0.10 M H₂SO₄? (Molar volume at STP = 22400 mL)",
      ["50 mL", "25 mL", "12.5 mL", "250 mL"], "B", v_1894,
      "Linking the Dumas and Kjeldahl methods through the moles of nitrogen atoms",
      "Each N₂ molecule carries two N atoms, and each N atom gives one NH₃ in Kjeldahl's method. Two NH₃ "
      "neutralise one H₂SO₄.",
      ["n(N₂) = 56/22400 = 0.0025 mol → n(N) = 0.0050 mol", "n(NH₃) = 0.0050 mol",
       "n(H₂SO₄) = 0.0050/2 = 0.0025 mol", "V = 0.0025/0.10 L = 25 mL"],
      why_others_wrong="50 mL treats H₂SO₄ as monobasic; 12.5 mL takes one N atom per N₂ molecule; 250 mL "
                       "divides 0.0025 mol by 0.010 M instead of 0.10 M (a slip of one decimal place).",
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', estimation of nitrogen", seconds=90),

    Q(T_PU, "Quantitative analysis and formulae", "Advanced", "multi_statement",
      *ms("Which of the following statements about the quantitative analysis of organic compounds are correct?",
          [("In the Carius method, the halogen of the compound is finally weighed as a silver halide.", True),
           ("Kjeldahl's method is suitable for estimating nitrogen in azo compounds.", False),
           ("In the estimation of sulphur, the sulphuric acid formed is precipitated as barium sulphate.", True),
           ("In the estimation of carbon and hydrogen, the carbon dioxide formed is absorbed in concentrated "
            "potassium hydroxide solution.", True),
           ("The percentage of oxygen is usually found by direct weighing of the oxygen set free from the "
            "compound.", False)],
          [["a", "b", "c"], ["c", "d", "e"], ["a", "c", "d", "e"]], "C"),
      "Methods of quantitative elemental analysis",
      "Halogen is weighed as AgX (Carius) and sulphur as BaSO₄. CO₂ is absorbed in KOH and water in anhydrous CaCl₂. "
      "Kjeldahl's method fails for nitro and azo compounds and for nitrogen in a ring (e.g. pyridine), because their "
      "nitrogen is not converted into ammonium sulphate. Oxygen is usually estimated by difference.",
      ["(a) true", "(b) false: azo nitrogen is not converted to (NH₄)₂SO₄", "(c) true", "(d) true",
       "(e) false: %O = 100 − sum of the other percentages"],
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', quantitative analysis", seconds=70),
]

# ================================================================ Some Basic Principles of Organic Chemistry (1896-1915)
# 1897: +I groups among eight (NCERT: alkyl groups release electrons; NO2, CN, COOH, halogen, ester withdraw)
plus_i = {"-CH3": True, "-CH2CH3": True, "-C(CH3)3": True, "-NO2": False, "-CN": False, "-COOH": False,
          "-Cl": False, "-COOR": False}
v_1897 = str(sum(plus_i.values()))
assert v_1897 == "3"
# 1902: molecules with at least one sp carbon
has_sp = {"CO2": True, "HCN": True, "CH2=C=CH2": True, "CH3CN": True, "C2H4": False, "C6H6": False,
          "CH3C≡CH": True, "CH3CHO": False}
v_1902 = str(sum(has_sp.values()))
assert v_1902 == "5"
# 1903: isomers of C6H3Cl3 = 3-subsets of ring positions up to the 12 ring symmetries
from itertools import combinations  # noqa: E402
def canon(s):
    forms = []
    for r in range(6):
        for sgn in (1, -1):
            forms.append(tuple(sorted(((sgn * p + r) % 6) for p in s)))
    return min(forms)
v_1903 = str(len({canon(c) for c in combinations(range(6), 3)}))
assert v_1903 == "3" and len({canon(c) for c in combinations(range(6), 2)}) == 3
# 1910: the eight structural isomers of C5H11Cl and whether each has a chiral carbon
c5 = {"1-chloropentane": False, "2-chloropentane": True, "3-chloropentane": False,
      "1-chloro-2-methylbutane": True, "2-chloro-2-methylbutane": False, "2-chloro-3-methylbutane": True,
      "1-chloro-3-methylbutane": False, "1-chloro-2,2-dimethylpropane": False}
assert len(c5) == 8
v_1910 = str(sum(c5.values()))
assert v_1910 == "3"
# 1911: chain of 8 C; locant sets from the two ends, first point of difference
ends = ([3, 5, 6], [3, 4, 6])
assert min(ends) == [3, 4, 6]

QUESTIONS += [
    Q(T_GO, "IUPAC nomenclature", "Basic", "direct",
      "The IUPAC name of CH₃–CH₂–CH(Br)–CH₂–OH is:",
      ["3-Bromobutan-4-ol", "1-Hydroxy-2-bromobutane", "2-Bromobutan-4-ol", "2-Bromobutan-1-ol"], "D",
      "Numbering a chain that carries a principal functional group and a substituent",
      "–OH is the principal functional group (suffix -ol) and must get the lowest locant, so the carbon carrying "
      "–OH is C-1. Bromine is then on C-2. Halogens are always cited as prefixes.",
      ["Parent chain: 4 C → butane", "–OH at C-1 → butan-1-ol", "Br at C-2 → 2-bromo", "Name: 2-bromobutan-1-ol"],
      why_others_wrong="'3-Bromobutan-4-ol' and '2-Bromobutan-4-ol' number from the wrong end; '1-Hydroxy-2-bromobutane' "
                       "cites the principal group as a prefix.",
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', nomenclature of compounds having "
            f"functional groups", seconds=30),

    N(T_GO, "Electronic effects", "Basic",
      "How many of the following groups, attached to a carbon chain, show an electron-releasing (+I) inductive "
      "effect?\n–CH₃, –CH₂CH₃, –C(CH₃)₃, –NO₂, –CN, –COOH, –Cl, –COOR",
      ["4", "3", "5", "2"], "B", v_1897,
      "Electron-releasing and electron-withdrawing groups (inductive effect)",
      "Alkyl groups such as methyl and ethyl release electrons (+I). Nitro, cyano, carboxyl, ester and halogen groups "
      "withdraw electrons (−I).",
      ["+I: –CH₃, –CH₂CH₃, –C(CH₃)₃ → 3", "−I: –NO₂, –CN, –COOH, –Cl, –COOR"],
      why_others_wrong="4 or 5 wrongly add the ester or carboxyl group, whose carbonyl carbon withdraws electrons; "
                       "2 leaves out one of the alkyl groups.",
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', inductive effect", seconds=30),

    Q(T_GO, "Hybridisation and functional groups", "Basic", "assertion_reason",
      *ar("Ethyne, HC≡CH, is a linear molecule.", True,
          "Each carbon atom of ethyne is sp hybridised, and its two sp hybrid orbitals point in opposite directions "
          "at 180°.", True, explains=True),
      "Hybridisation and shape",
      "Each carbon uses its two sp orbitals to form σ bonds to H and to the other carbon. As the two sp orbitals are "
      "at 180°, H–C–C–H lies on a straight line. R explains A.",
      ["C in ethyne: sp", "sp orbitals at 180°", "→ linear H–C≡C–H"],
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', shapes of carbon compounds", seconds=25),

    Q(T_GO, "Isomerism", "Basic", "statement_pair",
      *sp("Ethyl ethanoate (CH₃COOC₂H₅) and methyl propanoate (C₂H₅COOCH₃) are metamers.", True,
          "Pentan-2-ol and pentan-3-ol are chain isomers.", False),
      "Metamerism and position isomerism",
      "Metamers have the same functional group with different alkyl groups on either side of it; both esters are "
      "C₄H₈O₂ with the alkyl groups distributed differently about –COO–, so Statement I is true. Pentan-2-ol and "
      "pentan-3-ol have the same chain and differ only in the position of –OH: they are position isomers, so "
      "Statement II is false.",
      ["Esters: same group, different alkyl groups on either side → metamers", "Same chain, –OH moved → position isomers"],
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', structural isomerism", seconds=35),

    Q(T_GO, "Reactive intermediates", "Basic", "match_list",
      *ml("Match the species in List-I with its description in List-II.",
          ["(CH₃)₃C⁺", "CH₃•", "CH₃⁻", "NH₃"],
          ["Has a carbon atom with six valence electrons and a vacant p orbital",
           "Has a carbon atom with an unpaired electron",
           "Has a carbon atom carrying an unshared pair, with pyramidal shape",
           "A neutral molecule that acts as a nucleophile"],
          "I II III IV", ["II I III IV", "I III II IV", "IV II III I"], "A"),
      "Carbocations, free radicals, carbanions and nucleophiles",
      "A carbocation has a sextet on the sp² carbon with an empty p orbital; a free radical has an odd (unpaired) "
      "electron; a carbanion has an unshared pair on an sp³ carbon and is pyramidal; NH₃ is a neutral molecule with "
      "a lone pair, so it acts as a nucleophile.",
      ["(CH₃)₃C⁺ → I", "CH₃• → II", "CH₃⁻ → III", "NH₃ → IV"],
      why_others_wrong="The other codes swap the carbocation and free radical, the radical and carbanion, or treat "
                       "NH₃ as the carbocation.",
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', fission of a covalent bond", seconds=35),

    Q(T_GO, "Hybridisation and functional groups", "Basic", "multi_statement",
      *ms("Which of the following statements about the representation of organic molecules are correct?",
          [("In a bond-line formula, carbon and hydrogen atoms are not shown and the lines represent carbon–carbon "
            "bonds drawn in a zig-zag fashion.", True),
           ("In a bond-line formula, the terminals of the lines represent methyl groups unless a functional group "
            "is indicated there.", True),
           ("The condensed formula CH₃(CH₂)₃CH₃ represents hexane.", False),
           ("In a wedge-and-dash formula, a dashed wedge represents a bond projecting away from the observer.", True),
           ("In a bond-line formula, heteroatoms such as oxygen and nitrogen are not shown.", False)],
          [["a", "b", "c"], ["b", "d", "e"], ["a", "d"]], "D"),
      "Bond-line, condensed and three-dimensional formulas",
      "In bond-line formulas only the heteroatoms and the hydrogens attached to them are written; C and H are "
      "implied, and line ends are methyl groups. CH₃(CH₂)₃CH₃ has five carbons (pentane). A dashed wedge points "
      "away from the observer, a solid wedge towards the observer.",
      ["(a) true", "(b) true", "(c) false: C₅H₁₂, pentane", "(d) true", "(e) false: heteroatoms are shown"],
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', structural representations", seconds=50),

    N(T_GO, "Hybridisation and functional groups", "Intermediate",
      "How many of the following molecules contain at least one sp-hybridised carbon atom?\n"
      "CO₂, HCN, CH₂=C=CH₂, CH₃CN, CH₂=CH₂, C₆H₆, CH₃–C≡CH, CH₃CHO",
      ["4", "6", "5", "3"], "C", v_1902,
      "Recognising sp carbon atoms",
      "A carbon with two σ bonds and two π bonds (a triple bond, or two double bonds) is sp hybridised.",
      ["CO₂: O=C=O → sp", "HCN: H–C≡N → sp", "Allene: central C=C=C → sp", "CH₃–C≡N: nitrile C → sp",
       "Propyne: both C≡ carbons → sp", "Ethene, benzene, ethanal: only sp² and sp³", "Total = 5"],
      why_others_wrong="4 usually misses the central carbon of allene or the CO₂ carbon; 6 counts the carbonyl carbon "
                       "of ethanal, which is sp²; 3 counts only the C≡C and C≡N compounds.",
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', hybridisation", seconds=50),

    N(T_GO, "Isomerism", "Intermediate",
      "How many structural isomers are possible for trichlorobenzene, C₆H₃Cl₃ (all three chlorine atoms on the "
      "benzene ring)?",
      ["3", "4", "2", "6"], "A", v_1903,
      "Position isomerism in trisubstituted benzenes",
      "Place three identical substituents on the six ring positions and remove arrangements that are the same after "
      "rotating or turning over the ring.",
      ["Three adjacent: 1,2,3-", "Two adjacent and one apart: 1,2,4-", "Alternate: 1,3,5-", "Total = 3"],
      why_others_wrong="2 forgets the unsymmetrical 1,2,4-isomer; 4 counts 1,2,4- and 1,2,5- (the same compound) "
                       "separately; 6 counts numbering variants as different compounds.",
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', isomerism", seconds=50),

    Q(T_GO, "IUPAC nomenclature", "Intermediate", "direct",
      "The IUPAC name of CH₃–CH(CH₃)–CH(OH)–CH₂–CH=CH₂ is:",
      ["5-Methylhex-1-en-4-ol", "2-Methylhex-5-en-3-ol", "2-Methylhex-5-en-4-ol", "5-Methylhex-1-en-3-ol"], "B",
      "Lowest locant to the principal functional group (–OH) in preference to a double bond",
      "The parent chain has six carbons and contains both the C=C and the C bearing –OH. The suffix group –OH gets "
      "the lowest locant: numbering from the left gives –OH at C-3 (from the right it would be C-4). The double bond "
      "is then C5=C6 and the methyl group is on C-2.",
      ["Six-carbon chain with C=C and –OH", "From the left: OH at 3; from the right: OH at 4 → number from the left",
       "Double bond at 5, methyl at 2", "Name: 2-methylhex-5-en-3-ol"],
      why_others_wrong="Names with '-1-en' give the double bond the lowest locant, which is wrong when –OH is the "
                       "principal group; '2-methylhex-5-en-4-ol' mixes the two numberings.",
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', nomenclature", seconds=55),

    Q(T_GO, "Reactive intermediates", "Intermediate", "assertion_reason",
      *ar("Carbanions behave as nucleophiles.", True,
          "The negatively charged carbon of a carbanion carries an unshared pair of electrons that it can donate to "
          "an electron-deficient centre.", True, explains=True),
      "Carbanions as electron-pair donors",
      "A nucleophile is an electron-pair donor that seeks an electron-deficient centre. The carbanion carbon has an "
      "unshared electron pair, so it acts as a nucleophile. R explains A.",
      ["Carbanion: carbon with an unshared pair and negative charge", "Electron-pair donor → nucleophile"],
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', nucleophiles and carbanions",
      seconds=30),

    Q(T_GO, "Types of organic reactions", "Intermediate", "statement_pair",
      *sp("The conversion of ethanol into ethene by heating with concentrated sulphuric acid is an elimination "
          "reaction.", True,
          "In a rearrangement reaction, atoms or groups shift within the same molecule to give a structural isomer "
          "of it.", True),
      "Types of organic reactions",
      "Loss of H₂O from adjacent carbon atoms of ethanol to form a C=C bond is an elimination. A rearrangement "
      "reaction changes the skeleton or positions of groups within one molecule (e.g. n-hexane → 2-methylpentane), "
      "giving an isomer. Both statements are true.",
      ["CH₃CH₂OH → CH₂=CH₂ + H₂O: elimination", "Rearrangement: groups shift within the molecule → isomer"],
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', types of organic reactions",
      seconds=35),

    Q(T_GO, "IUPAC nomenclature", "Intermediate", "match_list",
      *ml("Match the compound in List-I with its IUPAC name in List-II.",
          ["CH₃–CH=CH–CHO", "CH₃–CO–CH=CH₂", "HC≡C–CH₂–OH", "CH₃–CH(CN)–CH₃"],
          ["Prop-2-yn-1-ol", "2-Methylpropanenitrile", "But-2-enal", "But-3-en-2-one"],
          "III IV I II", ["IV III I II", "III IV II I", "III I IV II"], "D"),
      "Names of unsaturated and polyfunctional compounds",
      "In each name the principal group (–CHO, C=O, –OH, –CN) gets the lowest locant; the carbon of –CHO and of "
      "–CN is counted as C-1 of the chain.",
      ["CH₃CH=CHCHO: C-1 is CHO, C=C at 2 → but-2-enal (III)",
       "CH₃COCH=CH₂: C=O at 2, C=C at 3 → but-3-en-2-one (IV)",
       "HC≡CCH₂OH: OH at 1, C≡C at 2 → prop-2-yn-1-ol (I)",
       "(CH₃)₂CHCN: CN carbon is C-1, methyl at 2 → 2-methylpropanenitrile (II)"],
      why_others_wrong="The other codes swap the aldehyde and the ketone, or the alcohol and the nitrile.",
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', nomenclature", seconds=55),

    Q(T_GO, "Electronic effects", "Intermediate", "multi_statement",
      *ms("Which of the following statements about electronic effects are correct?",
          [("In chloroethane, CH₃–CH₂–Cl, the carbon atom bonded to chlorine carries a partial positive charge.", True),
           ("In chloroethane, the carbon atom farther from chlorine carries a smaller partial positive charge than "
            "the carbon bonded to chlorine.", True),
           ("The inductive effect is transmitted only through π bonds.", False),
           ("The electromeric effect is a permanent effect.", False),
           ("Alkyl groups such as –CH₃ show an electron-releasing inductive (+I) effect.", True)],
          [["a", "b"], ["a", "c", "e"], ["b", "d", "e"]], "C"),
      "Inductive and electromeric effects",
      "Cl pulls the C–Cl bond electrons, making C-1 δ+; C-1 in turn pulls a little from C-2, which becomes δδ+, so "
      "the effect weakens along the chain of σ bonds. The electromeric effect is temporary, operating only when an "
      "attacking reagent is present. Alkyl groups are +I.",
      ["(a) true", "(b) true (δδ+)", "(c) false: transmitted through σ bonds", "(d) false: temporary", "(e) true"],
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', electron movement in organic "
            f"reactions", seconds=50),

    Q(T_GO, "Electronic effects", "Intermediate", "direct",
      "Which of the following is the strongest acid?",
      ["CH₃CH₂CH₂COOH", "ClCH₂CH₂CH₂COOH", "CH₃CH(Cl)CH₂COOH", "CH₃CH₂CH(Cl)COOH"], "D",
      "Inductive effect decreases with distance",
      "The −I effect of chlorine stabilises the carboxylate ion and increases acidity, but the effect fades rapidly "
      "as the number of bonds between Cl and –COO⁻ increases. It is greatest when Cl is on the α-carbon.",
      ["Cl on α-carbon (C-2): strongest −I at –COOH", "Cl on β (C-3) or γ (C-4): weaker", "No Cl: weakest acid",
       "→ 2-chlorobutanoic acid"],
      why_others_wrong="Moving chlorine to C-3 or C-4 weakens its effect on the carboxyl group; butanoic acid has no "
                       "electron-withdrawing group.",
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', inductive effect", seconds=35),

    N(T_GO, "Isomerism", "Advanced",
      "Among all the structural isomers of the monochloroalkane C₅H₁₁Cl, how many contain a chiral carbon atom "
      "(a carbon bonded to four different groups)?",
      ["2", "3", "4", "5"], "B", v_1910,
      "Generating structural isomers and finding chiral centres",
      "C₅H₁₁Cl has eight structural isomers (three on the pentane chain, four on the 2-methylbutane chain, one on "
      "the 2,2-dimethylpropane chain). Check each carbon bearing Cl or a branch.",
      ["Pentane: 1-Cl (no), 2-Cl (yes), 3-Cl (no)",
       "2-Methylbutane: 1-Cl (C-2: H, CH₃, C₂H₅, CH₂Cl → yes), 2-Cl (two CH₃ → no), "
       "3-Cl i.e. 2-chloro-3-methylbutane (yes), 4-Cl i.e. 1-chloro-3-methylbutane (no)",
       "2,2-Dimethylpropane: 1-Cl (no)", "Total chiral = 3"],
      why_others_wrong="2 misses 1-chloro-2-methylbutane, whose chiral carbon does not carry chlorine; 4 or 5 wrongly "
                       "count 3-chloropentane or 2-chloro-2-methylbutane, which have two identical groups.",
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', isomerism", seconds=120),

    Q(T_GO, "IUPAC nomenclature", "Advanced", "direct",
      "The IUPAC name of CH₃–CH(C₂H₅)–CH₂–CH(CH₃)–CH(CH₃)–CH₂–CH₃ is:",
      ["2-Ethyl-4,5-dimethylheptane", "3,5,6-Trimethyloctane", "3,4,6-Trimethyloctane", "6-Ethyl-3,4-dimethylheptane"],
      "C",
      "Longest chain and lowest locants at the first point of difference",
      "The longest chain runs from the CH₃ of the ethyl group to the far CH₃: eight carbons (octane), with methyl "
      "groups on three carbons. Numbering from the right gives {3, 4, 6}; from the left {3, 5, 6}. At the first point "
      "of difference 4 < 5, so number from the right.",
      ["Longest chain = 8 C (through the ethyl group)", "Substituents: three methyl groups",
       "Locants {3,4,6} vs {3,5,6} → {3,4,6}", "Name: 3,4,6-trimethyloctane"],
      why_others_wrong="Names ending in 'heptane' miss the longer chain that runs through the ethyl group (an ethyl "
                       "group at C-2 or C-6 always means a longer chain exists); 3,5,6- numbers from the wrong end.",
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', nomenclature of branched alkanes",
      seconds=75),

    Q(T_GO, "Hybridisation and functional groups", "Advanced", "assertion_reason",
      *ar("An sp-hybridised carbon atom attracts bonding electrons more strongly than an sp³-hybridised carbon atom.",
          True,
          "The greater the s character of a hybrid orbital, the farther its electrons lie from the nucleus.", False),
      "s character and electronegativity of carbon",
      "s orbitals are held closer to the nucleus than p orbitals, so a hybrid orbital with more s character (sp: 50%) "
      "keeps its electrons nearer the nucleus. An sp carbon is therefore more electronegative than sp² or sp³ carbon. "
      "A is true; R reverses the relationship and is false.",
      ["sp: 50% s; sp²: 33%; sp³: 25%", "More s character → electrons closer to the nucleus",
       "→ sp carbon more electronegative (A true)", "R says 'farther' → false"],
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', hybridisation and electronegativity",
      seconds=45),

    Q(T_GO, "Electronic effects", "Advanced", "statement_pair",
      *sp("For chloroethene, CH₂=CH–Cl, a canonical structure with a positive charge on chlorine and a negative charge "
          "on the terminal CH₂ carbon contributes to the resonance hybrid.", True,
          "As a result, the carbon–chlorine bond in chloroethene acquires partial double bond character.", True),
      "Resonance (+R) involving a halogen lone pair",
      "A lone pair of chlorine is delocalised into the C=C π bond, giving ⁻CH₂–CH=Cl⁺ as a minor canonical "
      "structure. Because a C=Cl double bond appears in one contributor, the real C–Cl bond has partial double bond "
      "character. Both statements are true.",
      ["CH₂=CH–Cl̈ ↔ ⁻CH₂–CH=Cl⁺", "Hybrid: C–Cl with partial double bond character"],
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', resonance effect", seconds=45),

    Q(T_GO, "Electronic effects", "Advanced", "match_list",
      *ml("Match the observation in List-I with the electronic effect mainly responsible for it in List-II.",
          ["Stabilisation of propene by delocalisation of the σ electrons of its methyl C–H bonds into the π bond",
           "Equal length of the two carbon–oxygen bonds in the methanoate ion, HCOO⁻",
           "Chloroethanoic acid is a stronger acid than ethanoic acid",
           "Complete shift of the π electrons of an alkene to one carbon when H⁺ approaches"],
          ["Inductive effect", "Electromeric effect", "Hyperconjugation", "Resonance effect"],
          "III IV I II", ["IV III I II", "III I IV II", "III IV II I"], "B"),
      "Choosing the electronic effect that explains an observation",
      "σ–π delocalisation of C–H bonds is hyperconjugation; equal C–O bonds arise because the negative charge is "
      "delocalised over both oxygens (resonance); Cl withdraws electrons through σ bonds (−I), stabilising "
      "ClCH₂COO⁻; the temporary, complete shift of a π pair on the approach of a reagent is the electromeric effect.",
      ["A → hyperconjugation (III)", "B → resonance (IV)", "C → inductive effect (I)", "D → electromeric effect (II)"],
      why_others_wrong="The other codes confuse resonance with hyperconjugation, or the permanent inductive effect "
                       "with the temporary electromeric effect.",
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', electronic displacements", seconds=60),

    Q(T_GO, "Electronic effects", "Advanced", "multi_statement",
      *ms("Which of the following pairs are resonance (canonical) structures of the same species, rather than "
          "different compounds?",
          [("CH₃–CO–CH₃ and CH₂=C(OH)–CH₃", False),
           ("The two Kekulé structures of benzene", True),
           ("CH₂=CH–CH₂⁺ and ⁺CH₂–CH=CH₂", True),
           ("CH₃–O–N=O and CH₃–NO₂", False),
           ("The two structures of the ethanoate ion with the negative charge on either oxygen atom", True)],
          [["a", "b", "c"], ["b", "c", "d"], ["a", "c", "e"]], "D"),
      "Rules for writing canonical structures",
      "Canonical structures differ only in the positions of electrons; the positions of all nuclei stay the same. "
      "In (a) a hydrogen atom has moved (the two are different compounds), and in (d) the atoms are connected "
      "differently (methyl nitrite and nitromethane are isomers). In (b), (c) and (e) only π electrons or charges move.",
      ["(a) H moves → different compounds", "(b) resonance", "(c) resonance (allyl cation)",
       "(d) different connectivity → isomers", "(e) resonance"],
      ncert=f"{NC11}, 'Organic Chemistry: Some Basic Principles and Techniques', resonance structure", seconds=60),
]

# ================================================================ Hydrocarbons (1916-1931)
# 1916: CH4 + 2O2 -> CO2 + 2H2O, dcH = -890 kJ/mol; 4.0 g CH4
v_1916 = f"{float(F(4, mm(C=1, H=4)) * 890):.1f} kJ"
assert v_1916 == "222.5 kJ"
# 1920: CH3CHBrCH2Br (M 202) + 2 NaNH2 -> CH3C≡CH (M 40)
n_1920 = F(202, 10) / mm(C=3, H=6, Br=2)
assert n_1920 == F(1, 10)
v_1920 = g(n_1920 * mm(C=3, H=4))
assert v_1920 == "4.0 g"
# 1921: CH4 + 4Cl2 -> CCl4 + 4HCl; 1.6 g CH4
v_1921 = g(F(16, 10) / mm(C=1, H=4) * 4 * 2 * AM["Cl"])
assert v_1921 == "28.4 g"
# 1922: alkenes giving propanone on ozonolysis (have a (CH3)2C= end)
gives_acetone = {"2-methylpropene": True, "2,3-dimethylbut-2-ene": True, "2-methylbut-2-ene": True,
                 "but-2-ene": False, "propene": False, "2-methylbut-1-ene": False, "3-methylbut-1-ene": False}
v_1922 = str(sum(gives_acetone.values()))
assert v_1922 == "3"
# 1925: equal masses of C6H6 and C2H2 -> mol CO2 per gram identical (both CH empirical formula)
co2_benz = F(78, 10) / mm(C=6, H=6) * 6
co2_ethy = F(78, 10) / mm(C=2, H=2) * 2
assert co2_benz == co2_ethy == F(6, 10)
v_1925 = "1 : 1"
# 1927: distinct mononitro derivatives of o-, m-, p-xylene
def ring_canon(labels):
    forms = []
    for r in range(6):
        for sgn in (1, -1):
            forms.append(tuple(labels[(sgn * i + r) % 6] for i in range(6)))
    return min(forms)
def mononitro(me_positions):
    out = set()
    for p in range(6):
        if p in me_positions:
            continue
        lab = ["M" if i in me_positions else ("N" if i == p else "H") for i in range(6)]
        out.add(ring_canon(lab))
    return len(out)
xyl = {"o": mononitro({0, 1}), "m": mononitro({0, 2}), "p": mononitro({0, 3})}
assert xyl == {"o": 2, "m": 3, "p": 1}
v_1927 = str(sum(xyl.values()))
assert v_1927 == "6"
# 1930: monochloro structural isomers (distinct H environments)
mono = {"2,2-dimethylpropane": 1, "n-butane": 2, "n-pentane": 3, "3-methylpentane": 4}
assert sorted(mono.values()) == [1, 2, 3, 4]

QUESTIONS += [
    N(T_HC, "Alkanes and conformations", "Basic",
      "Methane burns completely according to CH₄(g) + 2O₂(g) → CO₂(g) + 2H₂O(l); ΔcH = −890 kJ mol⁻¹. The heat "
      "released by the complete combustion of 4.0 g of methane is (C = 12, H = 1):",
      ["890 kJ", "55.6 kJ", "3560 kJ", "222.5 kJ"], "D", v_1916,
      "Heat of combustion of alkanes",
      "The enthalpy change is for one mole of methane, so scale it by the number of moles burnt.",
      ["M(CH₄) = 16 g mol⁻¹ → n = 4.0/16 = 0.25 mol", "q = 0.25 × 890 = 222.5 kJ released"],
      why_others_wrong="890 kJ is for one whole mole; 55.6 kJ is the heat per gram (890/16); 3560 kJ multiplies by "
                       "4 instead of dividing by the molar mass.",
      ncert=f"{NC11}, 'Hydrocarbons', alkanes: combustion", seconds=35),

    Q(T_HC, "Electrophilic substitution", "Basic", "direct",
      "In the sulphonation of benzene with fuming sulphuric acid (oleum), the electrophile that attacks the ring is:",
      ["H₃O⁺", "SO₃", "HSO₄⁻", "SO₄²⁻"], "B",
      "Electrophiles in aromatic substitution",
      "Fuming sulphuric acid contains dissolved SO₃. Sulphur in SO₃ is strongly electron-deficient, so SO₃ is the "
      "electrophile that attacks the π electrons of the ring, giving benzenesulphonic acid.",
      ["Oleum = H₂SO₄ + SO₃", "SO₃ (electron-deficient S) attacks the ring", "Product: C₆H₅SO₃H"],
      why_others_wrong="H₃O⁺ does not substitute the ring; HSO₄⁻ and SO₄²⁻ are anions (electron-rich) and cannot act "
                       "as electrophiles.",
      ncert=f"{NC11}, 'Hydrocarbons', electrophilic substitution reactions: sulphonation", seconds=25),

    Q(T_HC, "Alkenes: addition and ozonolysis", "Basic", "match_list",
      *ml("Match the method of preparing an alkene in List-I with the name of the process in List-II.",
          ["Heating an alkyl halide with alcoholic KOH", "Heating a vicinal dihalide with zinc metal",
           "Heating an alcohol with concentrated H₂SO₄", "Hydrogenating an alkyne over Lindlar's catalyst"],
          ["Partial reduction", "Acidic dehydration", "Dehydrohalogenation", "Dehalogenation"],
          "III IV II I", ["IV III II I", "III II IV I", "III IV I II"], "C"),
      "Preparation of alkenes",
      "Alcoholic KOH removes HX (dehydrohalogenation); zinc removes two halogen atoms from adjacent carbons "
      "(dehalogenation); concentrated H₂SO₄ removes water from an alcohol (acidic dehydration); Lindlar's catalyst "
      "stops hydrogenation of an alkyne at the alkene (partial reduction).",
      ["A → dehydrohalogenation (III)", "B → dehalogenation (IV)", "C → acidic dehydration (II)",
       "D → partial reduction (I)"],
      why_others_wrong="The other codes interchange the halogen-removing processes or the dehydration and partial "
                       "reduction.",
      ncert=f"{NC11}, 'Hydrocarbons', preparation of alkenes", seconds=40),

    Q(T_HC, "Alkanes and conformations", "Basic", "statement_pair",
      *sp("Among isomeric alkanes, the straight-chain isomer has the highest boiling point.", True,
          "2,2-Dimethylpropane (neopentane) has a higher boiling point than 2-methylbutane (isopentane).", False),
      "Effect of branching on boiling points of alkanes",
      "Branching makes a molecule more compact (nearly spherical), reducing its surface area and therefore the van "
      "der Waals forces. So the boiling point falls as branching increases: n-pentane (309 K) > isopentane (301 K) > "
      "neopentane (282.5 K). Statement I is true and Statement II false.",
      ["More branching → smaller surface area → weaker van der Waals forces → lower b.p.",
       "n-pentane > isopentane > neopentane"],
      ncert=f"{NC11}, 'Hydrocarbons', alkanes: physical properties", seconds=30),

    N(T_HC, "Alkynes", "Basic",
      "1,2-Dibromopropane, CH₃–CHBr–CH₂Br, is converted into propyne by treatment with alcoholic KOH followed by "
      "sodamide. The mass of propyne obtained from 20.2 g of 1,2-dibromopropane, assuming complete conversion, is "
      "(C = 12, H = 1, Br = 80):",
      ["8.0 g", "4.0 g", "4.2 g", "2.0 g"], "B", v_1920,
      "Preparation of alkynes from vicinal dihalides",
      "Two molecules of HBr are removed from one molecule of the vicinal dihalide, so 1 mol of dihalide gives 1 mol "
      "of propyne.",
      ["M(C₃H₆Br₂) = 36 + 6 + 160 = 202 g mol⁻¹ → n = 0.10 mol", "n(C₃H₄) = 0.10 mol",
       "Mass = 0.10 × 40 = 4.0 g"],
      why_others_wrong="4.2 g is the mass of propene (only one HBr removed); 8.0 g and 2.0 g double or halve the mole "
                       "ratio.",
      ncert=f"{NC11}, 'Hydrocarbons', preparation of alkynes from vicinal dihalides", seconds=45),

    N(T_HC, "Alkanes and conformations", "Intermediate",
      "Methane is chlorinated in light until it is converted completely into tetrachloromethane:\n"
      "CH₄ + 4Cl₂ → CCl₄ + 4HCl\n"
      "The minimum mass of chlorine needed for 1.6 g of methane is (C = 12, H = 1, Cl = 35.5):",
      ["7.1 g", "14.2 g", "56.8 g", "28.4 g"], "D", v_1921,
      "Stepwise free-radical chlorination of methane",
      "Each substitution replaces one H by Cl and uses one Cl₂ molecule (the other Cl atom leaves as HCl). Four "
      "hydrogens are replaced, so 4 mol Cl₂ per mol CH₄.",
      ["n(CH₄) = 1.6/16 = 0.10 mol", "n(Cl₂) = 4 × 0.10 = 0.40 mol", "Mass = 0.40 × 71 = 28.4 g"],
      why_others_wrong="7.1 g uses one Cl₂ per CH₄; 14.2 g uses Cl (35.5) instead of Cl₂ (71) for 0.40 mol; 56.8 g "
                       "counts eight Cl₂ per CH₄.",
      ncert=f"{NC11}, 'Hydrocarbons', alkanes: halogenation", seconds=45),

    N(T_HC, "Alkenes: addition and ozonolysis", "Intermediate",
      "How many of the following alkenes give propanone as one of the products of ozonolysis (O₃, then Zn/H₂O)?\n"
      "2-Methylpropene, 2,3-dimethylbut-2-ene, 2-methylbut-2-ene, but-2-ene, propene, 2-methylbut-1-ene, "
      "3-methylbut-1-ene",
      ["2", "3", "4", "5"], "B", v_1922,
      "Ozonolysis: each doubly bonded carbon becomes a carbonyl carbon",
      "Propanone, (CH₃)₂C=O, is formed only from a doubly bonded carbon that carries two methyl groups, i.e. an "
      "alkene containing (CH₃)₂C=.",
      ["2-Methylpropene: (CH₃)₂C=CH₂ → yes", "2,3-Dimethylbut-2-ene: (CH₃)₂C=C(CH₃)₂ → yes (2 mol)",
       "2-Methylbut-2-ene: (CH₃)₂C=CHCH₃ → yes", "But-2-ene → ethanal only; propene → ethanal + methanal",
       "2-Methylbut-1-ene → butanone + methanal; 3-methylbut-1-ene → 2-methylpropanal + methanal", "Total = 3"],
      why_others_wrong="4 or 5 count 2-methylbut-1-ene or 3-methylbut-1-ene, whose (CH₃) groups are not both on a "
                       "doubly bonded carbon; 2 misses one of the three correct alkenes.",
      ncert=f"{NC11}, 'Hydrocarbons', alkenes: ozonolysis", seconds=75),

    Q(T_HC, "Alkanes and conformations", "Intermediate", "assertion_reason",
      *ar("When a single alkyl halide is used in the Wurtz reaction, the alkane formed has twice the number of carbon "
          "atoms present in the alkyl halide.", True,
          "In the Wurtz reaction, two alkyl groups from two molecules of the alkyl halide are joined by a new C–C "
          "bond when the halide is treated with sodium in dry ether.", True, explains=True),
      "Wurtz reaction",
      "2R–X + 2Na → R–R + 2NaX. Because the product joins two identical R groups, it has double the carbon atoms "
      "of R–X (e.g. CH₃Br → ethane, C₂H₅Br → butane). R is why A is true.",
      ["2R–X + 2Na → R–R + 2NaX", "Carbon count of R–R = 2 × carbon count of R"],
      ncert=f"{NC11}, 'Hydrocarbons', preparation of alkanes: Wurtz reaction", seconds=35),

    Q(T_HC, "Benzene and aromaticity", "Intermediate", "multi_statement",
      *ms("Which of the following statements about benzene are correct?",
          [("Under ordinary conditions benzene prefers electrophilic substitution to addition.", True),
           ("All six carbon atoms of benzene are sp² hybridised and the ring is planar.", True),
           ("Benzene has (4n + 2) π electrons with n = 1.", True),
           ("Benzene is hydrogenated over nickel at high temperature and pressure mainly to cyclohexene.", False),
           ("The Kekulé structure with fixed alternate single and double bonds explains the equal lengths of all "
            "the C–C bonds.", False)],
          [["a", "b"], ["b", "c", "d"], ["a", "c", "e"]], "D"),
      "Structure and stability of benzene",
      "Substitution keeps the aromatic sextet, so benzene favours it. The six sp² carbons form a planar ring whose six "
      "π electrons (n = 1 in 4n + 2) are delocalised. Hydrogenation over Ni goes on to cyclohexane. A Kekulé structure "
      "would have unequal bonds; the equal 139 pm bonds are explained by resonance.",
      ["(a) true", "(b) true", "(c) true", "(d) false: cyclohexane", "(e) false: resonance hybrid explains it"],
      ncert=f"{NC11}, 'Hydrocarbons', aromatic hydrocarbons: structure of benzene", seconds=55),

    N(T_HC, "Benzene and aromaticity", "Intermediate",
      "Equal masses (7.8 g each) of benzene, C₆H₆, and ethyne, C₂H₂, are burnt completely in oxygen. The ratio of "
      "the volumes of carbon dioxide formed from benzene and from ethyne, measured under the same conditions, is "
      "(C = 12, H = 1):",
      ["3 : 1", "1 : 3", "1 : 1", "6 : 1"], "C", v_1925,
      "Same empirical formula → same CO₂ per gram",
      "Benzene and ethyne both have the empirical formula CH. Equal masses therefore contain the same number of moles "
      "of carbon atoms, and each carbon atom gives one CO₂.",
      ["Benzene: 7.8/78 = 0.10 mol × 6 C = 0.60 mol CO₂", "Ethyne: 7.8/26 = 0.30 mol × 2 C = 0.60 mol CO₂",
       "Ratio = 1 : 1"],
      why_others_wrong="3 : 1 compares the carbon atoms per molecule (6 : 2) without using moles; 1 : 3 compares the "
                       "moles of the two hydrocarbons; 6 : 1 compares the carbon atoms per molecule with one mole of "
                       "ethyne giving one CO₂.",
      ncert=f"{NC11}, 'Hydrocarbons', combustion of hydrocarbons", seconds=50),

    Q(T_HC, "Alkenes: addition and ozonolysis", "Intermediate", "statement_pair",
      *sp("The addition of HBr to propene in the presence of benzoyl peroxide takes place by a free-radical "
          "mechanism.", True,
          "Addition of HBr to an unsymmetrical alkene in the presence of a peroxide is also called the peroxide effect "
          "or Kharash effect.", True),
      "Anti-Markovnikov addition of HBr",
      "Benzoyl peroxide forms free radicals that generate Br• from HBr; Br• adds to give the more stable free radical, "
      "so the product is 1-bromopropane (anti-Markovnikov). NCERT calls this the peroxide or Kharash effect. Both "
      "statements are true.",
      ["Peroxide → radicals → Br•", "Br• adds to CH₂ end → secondary radical → 1-bromopropane",
       "Named peroxide (Kharash) effect"],
      ncert=f"{NC11}, 'Hydrocarbons', alkenes: anti-Markovnikov addition", seconds=35),

    N(T_HC, "Electrophilic substitution", "Advanced",
      "Each of the three xylenes (o-, m- and p-dimethylbenzene) is mononitrated on the ring. Counting only "
      "structurally different products, the total number of mononitro derivatives that can be obtained from all "
      "three xylenes together is:",
      ["5", "6", "7", "4"], "B", v_1927,
      "Counting distinct ring positions in disubstituted benzenes",
      "Use the symmetry of each xylene to find how many ring positions are different.",
      ["o-Xylene (1,2): positions 3 (=6) and 4 (=5) → 2 products",
       "m-Xylene (1,3): positions 2, 4 (=6) and 5 → 3 products",
       "p-Xylene (1,4): all four free positions equivalent → 1 product", "Total = 2 + 3 + 1 = 6"],
      why_others_wrong="5 misses position 2 of m-xylene (between the methyl groups); 7 counts positions 4 and 6 of "
                       "m-xylene separately; 4 assumes each xylene has the same number of products as toluene's o/p.",
      ncert=f"{NC11}, 'Hydrocarbons', isomerism in aromatic compounds and electrophilic substitution", seconds=90),

    Q(T_HC, "Alkenes: addition and ozonolysis", "Advanced", "direct",
      "An alkene X, C₆H₁₂, on ozonolysis (O₃, then Zn/H₂O) gives one mole of ethanal and one mole of butanone per "
      "mole of X. X is:",
      ["Hex-2-ene", "2-Methylpent-2-ene", "3-Methylpent-1-ene", "3-Methylpent-2-ene"], "D",
      "Working back from ozonolysis products",
      "Join the two carbonyl carbons by a double bond after removing the oxygen atoms: CH₃CH=O + O=C(CH₃)CH₂CH₃ → "
      "CH₃CH=C(CH₃)CH₂CH₃. The longest chain containing the double bond has five carbons, with a methyl group on C-3.",
      ["Ethanal: CH₃CH= ; butanone: =C(CH₃)CH₂CH₃", "X = CH₃–CH=C(CH₃)–CH₂–CH₃", "Name: 3-methylpent-2-ene"],
      why_others_wrong="Hex-2-ene gives ethanal and butanal; 2-methylpent-2-ene gives propanone and propanal; "
                       "3-methylpent-1-ene gives methanal and 2-methylbutanal.",
      ncert=f"{NC11}, 'Hydrocarbons', alkenes: ozonolysis", seconds=60),

    Q(T_HC, "Alkynes", "Advanced", "assertion_reason",
      *ar("Hydrogenation of but-2-yne over palladium on charcoal partially deactivated with quinoline gives "
          "cis-but-2-ene.", True,
          "Reduction of but-2-yne with sodium in liquid ammonia gives trans-but-2-ene.", True, explains=False),
      "Partial reduction of alkynes to cis and trans alkenes",
      "Lindlar's catalyst stops the hydrogenation at the alkene stage and gives the cis alkene. Sodium in liquid "
      "ammonia gives the trans alkene. Both statements are true, but R describes a different reagent and a different "
      "product; it does not explain why Lindlar reduction gives the cis isomer.",
      ["Lindlar (Pd/C + quinoline) → cis-alkene: A true", "Na/liquid NH₃ → trans-alkene: R true",
       "R is about another reaction → not the explanation"],
      ncert=f"{NC11}, 'Hydrocarbons', preparation of alkenes from alkynes", seconds=40),

    Q(T_HC, "Alkanes and conformations", "Advanced", "match_list",
      *ml("Match the alkane in List-I with the number of structurally different monochloro derivatives it can give "
          "on free-radical chlorination (List-II).",
          ["2,2-Dimethylpropane", "n-Butane", "n-Pentane", "3-Methylpentane"],
          ["2", "4", "1", "3"],
          "III I IV II", ["I III IV II", "III I II IV", "III IV I II"], "D"),
      "Counting different kinds of hydrogen atoms",
      "Each set of equivalent hydrogen atoms gives one monochloro product.",
      ["Neopentane: all 12 H equivalent → 1 (III)", "n-Butane: CH₃ and CH₂ → 2 (I)",
       "n-Pentane: C1, C2, C3 → 3 (IV)", "3-Methylpentane: C1, C2, C3 and the branch CH₃ → 4 (II)"],
      why_others_wrong="The other codes miscount n-pentane (forgetting C-3) or 3-methylpentane (forgetting the "
                       "branch methyl or the tertiary C-3).",
      ncert=f"{NC11}, 'Hydrocarbons', alkanes: halogenation", seconds=70),

    Q(T_HC, "Alkanes and conformations", "Advanced", "multi_statement",
      *ms("Which of the following statements about the chemical reactions of alkanes are correct?",
          [("On pyrolysis, dodecane gives a mixture containing heptane and pentene, among other products.", True),
           ("Under normal conditions alkanes are generally inert towards acids, bases and most oxidising and "
            "reducing agents.", True),
           ("Free-radical chlorination of methane proceeds through a carbocation intermediate.", False),
           ("Heating n-alkanes with anhydrous AlCl₃ and HCl gas converts them into branched-chain isomers.", True),
           ("Complete combustion of an alkane gives carbon monoxide and hydrogen.", False)],
          [["a", "b", "c"], ["b", "d", "e"], ["a", "d"]], "C"),
      "Reactions of alkanes",
      "Pyrolysis (cracking) breaks large alkanes into smaller alkanes and alkenes, e.g. C₁₂H₂₆ → C₇H₁₆ + C₅H₁₀ + "
      "other products. Alkanes are generally inert to most reagents under ordinary conditions. Halogenation is a "
      "free-radical chain reaction. Anhydrous AlCl₃/HCl isomerises n-alkanes. Complete combustion gives CO₂ and H₂O.",
      ["(a) true", "(b) true", "(c) false: free radicals", "(d) true", "(e) false: CO₂ and H₂O"],
      ncert=f"{NC11}, 'Hydrocarbons', alkanes: chemical properties", seconds=60),
]

# ================================================================ Organic Compounds Containing Halogens (1932-1944)
# 1933: C6H5Cl + CH3Cl + 2Na -> C6H5CH3 ; 11.25 g chlorobenzene
n_1933 = F(1125, 100) / mm(C=6, H=5, Cl=1)
assert n_1933 == F(1, 10)
v_1933 = g(n_1933 * mm(C=7, H=8))
assert v_1933 == "9.2 g" and g(n_1933 / 2 * mm(C=12, H=10)) == "7.7 g"
# 1936: 3CCl4 + 2SbF3 -> 3CCl2F2 + 2SbCl3 ; 15.4 g CCl4
n_1936 = F(154, 10) / mm(C=1, Cl=4)
assert n_1936 == F(1, 10)
v_1936 = g(n_1936 * mm(C=1, Cl=2) + n_1936 * 2 * 19)
assert v_1936 == "12.1 g"
# 1941: SN1 first order, k = 6.93e-4 s^-1, ln2 = 0.693 -> t1/2 = 1000 s; 25 % left after 2 half-lives
t_half = 0.693 / 6.93e-4
assert abs(t_half - 1000) < 1e-6
v_1941 = f"{round(2 * t_half)} s"
assert v_1941 == "2000 s"
# 1942: C6H5Br -> C6H5MgBr -> (CO2, H3O+) C6H5COOH ; 7.85 g bromobenzene
n_1942 = F(785, 100) / mm(C=6, H=5, Br=1)
assert n_1942 == F(5, 100)
v_1942 = g(n_1942 * mm(C=7, H=6, O=2))
assert v_1942 == "6.1 g" and g(n_1942 * mm(C=6, H=6)) == "3.9 g"

QUESTIONS += [
    Q(T_HX, "C-X bond and preparation", "Basic", "direct",
      "Primary and secondary alcohols are converted into alkyl chlorides by heating with concentrated hydrochloric "
      "acid in the presence of:",
      ["Anhydrous ZnCl₂", "Red phosphorus", "Aqueous NaOH", "Dry ether"], "A",
      "Preparation of haloalkanes from alcohols",
      "Anhydrous zinc chloride is used with concentrated HCl to replace the –OH group of primary and secondary "
      "alcohols by –Cl; tertiary alcohols react with concentrated HCl simply by shaking at room temperature.",
      ["R–OH + HCl (ZnCl₂) → R–Cl + H₂O"],
      why_others_wrong="Red phosphorus is used with bromine or iodine (to give PBr₃/PI₃ in situ); aqueous NaOH would "
                       "hydrolyse an alkyl halide back to the alcohol; dry ether is the solvent for Grignard and Wurtz "
                       "reactions.",
      ncert=f"{NC12}, 'Haloalkanes and Haloarenes', preparation of haloalkanes from alcohols", seconds=25),

    N(T_HX, "C-X bond and preparation", "Basic",
      "Chlorobenzene is treated with chloromethane and sodium in dry ether (Wurtz–Fittig reaction):\n"
      "C₆H₅Cl + CH₃Cl + 2Na → C₆H₅CH₃ + 2NaCl\n"
      "The mass of toluene formed from 11.25 g of chlorobenzene, assuming complete conversion, is (C = 12, H = 1, "
      "Cl = 35.5):",
      ["7.7 g", "18.4 g", "4.6 g", "9.2 g"], "D", v_1933,
      "Wurtz–Fittig reaction",
      "One mole of chlorobenzene gives one mole of toluene.",
      ["M(C₆H₅Cl) = 112.5 g mol⁻¹ → n = 0.10 mol", "n(toluene) = 0.10 mol", "Mass = 0.10 × 92 = 9.2 g"],
      why_others_wrong="7.7 g is the biphenyl that the Fittig reaction (two aryl halides) would give; 18.4 g and 4.6 g "
                       "double or halve the 1 : 1 ratio.",
      ncert=f"{NC12}, 'Haloalkanes and Haloarenes', reactions of haloarenes with metals", seconds=40),

    Q(T_HX, "C-X bond and preparation", "Basic", "statement_pair",
      *sp("Free-radical halogenation of alkanes is not a good method for preparing a particular haloalkane, because it "
          "gives a mixture of isomeric mono- and polyhaloalkanes.", True,
          "Ethene reacts with hydrogen chloride to give chloroethane.", True),
      "Preparation of haloalkanes from hydrocarbons",
      "Chlorination of an alkane such as butane gives several monochloro isomers and polychloro products that are "
      "hard to separate, so the method is unsuitable for a pure product (Statement I true). Hydrogen halides add to "
      "alkenes: CH₂=CH₂ + HCl → CH₃CH₂Cl (Statement II true).",
      ["Alkane + Cl₂ (light) → mixture", "CH₂=CH₂ + HCl → CH₃CH₂Cl"],
      ncert=f"{NC12}, 'Haloalkanes and Haloarenes', preparation of haloalkanes", seconds=30),

    Q(T_HX, "SN1 and SN2", "Basic", "multi_statement",
      *ms("Which of the following statements about optical activity are correct?",
          [("A racemic mixture shows zero optical rotation.", True),
           ("The two enantiomers of a compound rotate plane-polarised light by equal amounts but in opposite "
            "directions.", True),
           ("Butan-2-ol is a chiral molecule.", True),
           ("A laevorotatory compound is indicated by the sign (+) before its name.", False),
           ("Propan-2-ol is a chiral molecule.", False)],
          [["a", "b"], ["a", "c", "e"], ["b", "c", "d"]], "B"),
      "Chirality and optical rotation",
      "In a racemic mixture the rotation due to one enantiomer is cancelled by the other. Butan-2-ol has a carbon "
      "bonded to H, OH, CH₃ and C₂H₅, so it is chiral; propan-2-ol's C-2 carries two CH₃ groups. Laevorotatory "
      "compounds carry the sign (−); dextrorotatory ones (+).",
      ["(a) true", "(b) true", "(c) true", "(d) false: (−) for laevo", "(e) false: two identical CH₃ groups"],
      ncert=f"{NC12}, 'Haloalkanes and Haloarenes', optical isomerism", seconds=40),

    N(T_HX, "Polyhalogen compounds", "Intermediate",
      "Freon-12 is made from tetrachloromethane by the Swarts reaction:\n"
      "3CCl₄ + 2SbF₃ → 3CCl₂F₂ + 2SbCl₃\n"
      "The mass of CCl₂F₂ obtained from 15.4 g of CCl₄, assuming complete conversion, is (C = 12, Cl = 35.5, "
      "F = 19):",
      ["13.8 g", "10.5 g", "12.1 g", "8.1 g"], "C", v_1936,
      "Stoichiometry of the Swarts reaction",
      "CCl₄ and CCl₂F₂ are in the mole ratio 3 : 3, i.e. 1 : 1.",
      ["n(CCl₄) = 15.4/154 = 0.10 mol", "n(CCl₂F₂) = 0.10 mol", "M(CCl₂F₂) = 12 + 71 + 38 = 121 g mol⁻¹",
       "Mass = 12.1 g"],
      why_others_wrong="13.8 g is for CCl₃F (one F only); 10.5 g is for CClF₃ (three F); 8.1 g wrongly uses the "
                       "2 : 3 ratio of SbF₃ to CCl₂F₂ for CCl₄.",
      ncert=f"{NC12}, 'Haloalkanes and Haloarenes', polyhalogen compounds: freons", seconds=50),

    Q(T_HX, "SN1 and SN2", "Intermediate", "assertion_reason",
      *ar("An SN2 reaction at a chiral carbon atom gives a product with the inverted configuration.", True,
          "In an SN2 reaction the nucleophile attacks the carbon atom from the side opposite to the leaving group.",
          True, explains=True),
      "Stereochemistry of SN2 reactions",
      "Because the nucleophile approaches from the back, the other three groups are pushed over to the other side as "
      "the leaving group departs, like an umbrella turning inside out. This backside attack is why the configuration "
      "is inverted. R explains A.",
      ["Backside attack", "Transition state: Nu···C···X", "Three groups flip → inversion"],
      ncert=f"{NC12}, 'Haloalkanes and Haloarenes', SN2 mechanism and stereochemistry", seconds=30),

    Q(T_HX, "SN1 and SN2", "Intermediate", "match_list",
      *ml("Match the reaction of haloalkanes in List-I with its feature in List-II.",
          ["SN2 reaction", "SN1 reaction", "β-Elimination (dehydrohalogenation)", "Reaction with magnesium in dry ether"],
          ["Carbocation intermediate; racemisation of a chiral substrate",
           "Organometallic product with a polar carbon–magnesium bond",
           "Alkene formed by loss of HX from adjacent carbon atoms",
           "Single step with inversion of configuration"],
          "IV I III II", ["I IV III II", "IV III I II", "IV I II III"], "D"),
      "Reactions of haloalkanes",
      "SN2 is concerted with inversion; SN1 goes through a planar carbocation and racemises a chiral substrate; "
      "β-elimination removes H from the β-carbon and X from the α-carbon to give an alkene; Mg in dry ether gives "
      "the Grignard reagent R–MgX.",
      ["SN2 → IV", "SN1 → I", "β-Elimination → III", "Mg/dry ether → II"],
      why_others_wrong="The other codes swap SN1 and SN2, or the elimination and Grignard entries.",
      ncert=f"{NC12}, 'Haloalkanes and Haloarenes', chemical reactions of haloalkanes", seconds=40),

    Q(T_HX, "Polyhalogen compounds", "Intermediate", "statement_pair",
      *sp("Iodoform was used earlier as an antiseptic, but because of its objectionable smell it has been replaced by "
          "other formulations containing iodine.", True,
          "Freons are extremely stable, unreactive, non-toxic, non-corrosive and easily liquefiable gases.", True),
      "Polyhalogen compounds",
      "Both statements follow NCERT's account: iodoform's antiseptic action comes from free iodine, but its smell led "
      "to its replacement; freons (chlorofluorocarbons) are stable, non-toxic, non-corrosive, easily liquefied gases, "
      "which is why they were used in refrigeration and aerosol propellants.",
      ["Iodoform: antiseptic, replaced due to smell → true", "Freons: stable, unreactive, easily liquefied → true"],
      ncert=f"{NC12}, 'Haloalkanes and Haloarenes', polyhalogen compounds", seconds=35),

    Q(T_HX, "SN1 and SN2", "Intermediate", "multi_statement",
      *ms("Which of the following statements about 2-bromo-2-methylpropane, (CH₃)₃C–Br, are correct?",
          [("It is a secondary alkyl halide.", False),
           ("Its hydrolysis in water takes place mainly by the SN1 mechanism.", True),
           ("The rate of its SN1 hydrolysis does not depend on the concentration of the nucleophile.", True),
           ("When heated with alcoholic KOH it gives 2-methylpropene.", True),
           ("Its hydrolysis by SN2 gives a product with inverted configuration at a chiral carbon.", False)],
          [["a", "b", "c"], ["b", "c", "d", "e"], ["c", "d"]], "B"),
      "Behaviour of a tertiary alkyl halide",
      "The C–Br carbon is bonded to three carbons, so the halide is tertiary. Tertiary halides react by SN1, whose "
      "rate depends only on [RX]. With alcoholic KOH they undergo β-elimination to (CH₃)₂C=CH₂. The molecule has no "
      "chiral carbon (three identical CH₃ groups) and is too hindered for SN2.",
      ["(a) false: tertiary", "(b) true", "(c) true", "(d) true", "(e) false: no chiral carbon; SN2 is hindered"],
      ncert=f"{NC12}, 'Haloalkanes and Haloarenes', SN1 mechanism and elimination", seconds=55),

    N(T_HX, "SN1 and SN2", "Advanced",
      "The hydrolysis of 2-bromo-2-methylpropane in a large excess of water follows the SN1 mechanism, with "
      "rate = k[(CH₃)₃CBr] and k = 6.93 × 10⁻⁴ s⁻¹ at a certain temperature. The time taken for 75% of the alkyl "
      "bromide to react is (ln 2 = 0.693):",
      ["1000 s", "2000 s", "4000 s", "500 s"], "B", v_1941,
      "First-order kinetics of an SN1 reaction",
      "An SN1 reaction is first order in the alkyl halide, so its half-life is constant: t½ = 0.693/k. 75% reaction "
      "means 25% left, i.e. two half-lives.",
      ["t½ = 0.693 / (6.93 × 10⁻⁴) = 1000 s", "100% → 50% → 25%: two half-lives", "t = 2 × 1000 = 2000 s"],
      why_others_wrong="1000 s is one half-life (50% reaction); 4000 s is four half-lives; 500 s halves t½.",
      ncert=f"{NC12}, 'Haloalkanes and Haloarenes', SN1 mechanism (first-order rate)", seconds=60),

    N(T_HX, "C-X bond and preparation", "Advanced",
      "7.85 g of bromobenzene is converted completely into phenylmagnesium bromide in dry ether. The Grignard reagent "
      "is treated with dry ice (solid CO₂) and the product is hydrolysed with dilute acid. Assuming every step is "
      "complete, the mass of the organic acid obtained is (C = 12, H = 1, O = 16, Br = 80):",
      ["12.2 g", "3.9 g", "6.8 g", "6.1 g"], "D", v_1942,
      "Grignard reagent + CO₂ → carboxylic acid",
      "C₆H₅Br → C₆H₅MgBr → (CO₂) C₆H₅COOMgBr → (H₃O⁺) C₆H₅COOH. One mole of bromobenzene gives one mole of benzoic "
      "acid.",
      ["n(C₆H₅Br) = 7.85/157 = 0.05 mol", "n(C₆H₅COOH) = 0.05 mol", "Mass = 0.05 × 122 = 6.1 g"],
      why_others_wrong="12.2 g takes 0.10 mol; 3.9 g is the benzene formed if the Grignard reagent were hydrolysed by "
                       "water before reacting with CO₂; 6.8 g is the mass of phenylethanoic acid (M = 136), which would "
                       "need one more carbon atom than CO₂ supplies.",
      ncert=f"{NC12}, 'Haloalkanes and Haloarenes', Grignard reagents; 'Aldehydes, Ketones and Carboxylic Acids', "
            f"preparation of carboxylic acids", seconds=60),

    Q(T_HX, "C-X bond and preparation", "Advanced", "direct",
      "Propene is treated with HBr in the presence of benzoyl peroxide to give X. X is heated with ethanolic KCN to "
      "give Y, and Y is reduced with lithium aluminium hydride to give Z. Z is:",
      ["Propan-1-amine", "2-Methylpropan-1-amine", "Butan-1-amine", "N-Propylmethanamine"], "C",
      "Anti-Markovnikov addition, nucleophilic substitution by CN⁻ and reduction of nitriles",
      "With peroxide, HBr adds anti-Markovnikov: X = CH₃CH₂CH₂Br. KCN gives the nitrile Y = CH₃CH₂CH₂CN (one carbon "
      "added). LiAlH₄ reduces –C≡N to –CH₂NH₂: Z = CH₃CH₂CH₂CH₂NH₂.",
      ["X: 1-bromopropane", "Y: butanenitrile", "Z: butan-1-amine"],
      why_others_wrong="2-Methylpropan-1-amine would come from 2-bromopropane (no peroxide); propan-1-amine forgets the "
                       "carbon added by cyanide; N-propylmethanamine would come from an isocyanide, which forms with "
                       "AgCN, not KCN.",
      ncert=f"{NC12}, 'Haloalkanes and Haloarenes', nucleophilic substitution; 'Amines', reduction of nitriles",
      seconds=60),

    Q(T_HX, "SN1 and SN2", "Advanced", "assertion_reason",
      *ar("Tertiary alkyl halides undergo SN1 reactions faster than primary alkyl halides.", True,
          "An SN1 reaction takes place in a single step without forming any intermediate.", False),
      "SN1 mechanism and carbocation stability",
      "SN1 takes place in two steps: slow ionisation of R–X to a carbocation, then fast attack of the nucleophile. "
      "The more stable the carbocation (3° > 2° > 1°), the faster the reaction, so A is true. R describes an SN2 "
      "reaction and is false.",
      ["Step 1 (slow): R–X → R⁺ + X⁻", "Step 2 (fast): R⁺ + Nu⁻ → R–Nu", "3° carbocation most stable → A true",
       "R false: SN1 has a carbocation intermediate"],
      ncert=f"{NC12}, 'Haloalkanes and Haloarenes', SN1 mechanism", seconds=35),
]

# ================================================================ Organic Compounds Containing Oxygen (1945-1964)
# 1945: hydroboration-oxidation: propene (4.2 g) -> propan-1-ol
v_1945 = "Propan-1-ol, " + g(F(42, 10) / mm(C=3, H=6) * mm(C=3, H=8, O=1))
assert v_1945 == "Propan-1-ol, 6.0 g"
# 1946: CH3CHO + H2 -> CH3CH2OH ; 4.4 g ethanal
v_1946 = f"{float(F(44, 10) / mm(C=2, H=4, O=1) * F(224, 10)):.2f} L"
assert v_1946 == "2.24 L"
# 1951: esters from {ethanoic, propanoic} x {methanol, ethanol}
acids, alcohols = ["ethanoic", "propanoic"], ["methyl", "ethyl"]
esters = {f"{al} {ac[:-2]}ate" for ac in acids for al in alcohols}
v_1951 = str(len(esters))
assert v_1951 == "4"
# 1952: (CH3)2CO + H2NCONHNH2 -> (CH3)2C=NNHCONH2 + H2O ; 5.8 g propanone
semi = mm(C=4, H=9, N=3, O=1)
assert semi == mm(C=3, H=6, O=1) + mm(C=1, H=5, N=3, O=1) - mm(H=2, O=1) == 115
v_1952 = g(F(58, 10) / mm(C=3, H=6, O=1) * semi)
assert v_1952 == "11.5 g"
# 1953: Rosenmund: C6H5COCl (140.5) -> C6H5CHO ; 7.025 g
n_1953 = F(7025, 1000) / mm(C=7, H=5, O=1, Cl=1)
assert n_1953 == F(5, 100)
v_1953 = g(n_1953 * mm(C=7, H=6, O=1))
assert v_1953 == "5.3 g"
# 1959: C2H5OH -> CH3CHO -> (CH3MgBr) CH3CH(OH)CH3 -> CH3COCH3 -> CHI3 ; 2.3 g ethanol, 1 : 1 throughout
n_1959 = F(23, 10) / mm(C=2, H=6, O=1)
v_1959 = g(n_1959 * mm(C=1, H=1, I=3))
assert v_1959 == "19.7 g" and g(n_1959 * 3 * 127) == "19.1 g"

QUESTIONS += [
    N(T_OX, "Alcohols", "Basic",
      "4.2 g of propene is treated with diborane and the product is oxidised with alkaline hydrogen peroxide "
      "(hydroboration–oxidation). Assuming complete conversion, the alcohol formed and its mass are (C = 12, H = 1, "
      "O = 16):",
      ["Propan-2-ol, 6.0 g", "Propan-1-ol, 3.0 g", "Propan-1-ol, 6.0 g", "Propan-2-ol, 4.2 g"], "C", v_1945,
      "Hydroboration–oxidation gives the anti-Markovnikov alcohol",
      "In hydroboration–oxidation, water is effectively added so that –OH ends up on the less substituted carbon: "
      "propene gives propan-1-ol. One mole of propene gives one mole of alcohol.",
      ["n(C₃H₆) = 4.2/42 = 0.10 mol", "Product: CH₃CH₂CH₂OH (M = 60)", "Mass = 0.10 × 60 = 6.0 g"],
      why_others_wrong="Propan-2-ol is the product of acid-catalysed hydration (Markovnikov); 3.0 g halves the mole "
                       "ratio; 4.2 g simply repeats the mass of propene and ignores the added H₂O.",
      ncert=f"{NC12}, 'Alcohols, Phenols and Ethers', preparation of alcohols: hydroboration–oxidation", seconds=40),

    N(T_OX, "Aldehydes and ketones", "Basic",
      "4.4 g of ethanal is reduced completely to ethanol by catalytic hydrogenation over nickel. The volume of "
      "hydrogen consumed, measured at STP, is (C = 12, H = 1, O = 16; molar volume at STP = 22.4 L mol⁻¹):",
      ["4.48 L", "2.24 L", "1.12 L", "22.4 L"], "B", v_1946,
      "Reduction of aldehydes to primary alcohols",
      "CH₃CHO + H₂ → CH₃CH₂OH: one mole of H₂ per mole of aldehyde.",
      ["n(CH₃CHO) = 4.4/44 = 0.10 mol", "n(H₂) = 0.10 mol", "V = 0.10 × 22.4 = 2.24 L"],
      why_others_wrong="4.48 L assumes two moles of H₂ per mole of ethanal; 1.12 L halves the ratio; 22.4 L is for "
                       "one whole mole.",
      ncert=f"{NC12}, 'Alcohols, Phenols and Ethers', preparation of alcohols by reduction of aldehydes", seconds=30),

    Q(T_OX, "Carboxylic acids", "Basic", "direct",
      "Methanoic acid (formic acid) gets its common name from the source from which it was first obtained. This "
      "source is:",
      ["Vinegar", "Rancid butter", "Goat fat", "Red ants"], "D",
      "Common names of carboxylic acids",
      "Methanoic acid was first obtained from red ants; its common name comes from the Latin formica, meaning ant.",
      ["formica (Latin) = ant → formic acid"],
      why_others_wrong="Vinegar gives acetic acid (acetum); rancid butter gives butyric acid (butyrum); goat fat gives "
                       "caproic acid.",
      ncert=f"{NC12}, 'Aldehydes, Ketones and Carboxylic Acids', nomenclature of carboxylic acids", seconds=20),

    Q(T_OX, "Ethers", "Basic", "assertion_reason",
      *ar("Ethanol has a much higher boiling point than its isomer methoxymethane.", True,
          "Ethanol molecules are associated through intermolecular hydrogen bonds, which are absent in "
          "methoxymethane.", True, explains=True),
      "Hydrogen bonding and boiling points of alcohols and ethers",
      "Both have M = 46 g mol⁻¹, but ethanol has an O–H group and forms intermolecular hydrogen bonds; an ether has no "
      "hydrogen on oxygen. Extra energy is needed to break the hydrogen bonds, so ethanol boils much higher. R "
      "explains A.",
      ["Same molar mass", "Ethanol: O–H → intermolecular H-bonds", "Ether: no O–H → only dipole interactions"],
      ncert=f"{NC12}, 'Alcohols, Phenols and Ethers', physical properties of ethers", seconds=30),

    Q(T_OX, "Alcohols", "Basic", "statement_pair",
      *sp("A primary alcohol can be oxidised to an aldehyde by CrO₃ in an anhydrous medium.", True,
          "Tertiary alcohols are readily oxidised to ketones by CrO₃.", False),
      "Oxidation of alcohols",
      "Using CrO₃ in an anhydrous medium (or PCC) stops the oxidation of a primary alcohol at the aldehyde stage "
      "(Statement I true). Tertiary alcohols have no hydrogen on the carbinol carbon and are not oxidised to "
      "carbonyl compounds by such reagents (Statement II false).",
      ["RCH₂OH → RCHO (CrO₃, anhydrous)", "R₃C–OH: no H on the C–OH carbon → no ketone"],
      ncert=f"{NC12}, 'Alcohols, Phenols and Ethers', chemical reactions of alcohols: oxidation", seconds=30),

    Q(T_OX, "Phenols", "Basic", "multi_statement",
      *ms("Which of the following methods can be used to prepare phenol?",
          [("Heating chlorobenzene with NaOH at 623 K and 300 atm, followed by acidification", True),
           ("Fusing sodium benzenesulphonate with NaOH, followed by acidification", True),
           ("Warming an aqueous solution of benzenediazonium chloride", True),
           ("Air oxidation of cumene to cumene hydroperoxide, followed by treatment with dilute acid", True),
           ("Heating benzene with dilute aqueous NaOH", False)],
          [["a", "b", "c"], ["b", "c", "d", "e"], ["a", "d"]], "A"),
      "Preparation of phenols",
      "Phenol is obtained from haloarenes, from benzenesulphonic acid, from diazonium salts and from cumene. Benzene "
      "itself does not react with aqueous NaOH.",
      ["(a) from haloarene: true", "(b) from sulphonic acid: true", "(c) from diazonium salt: true",
       "(d) from cumene: true", "(e) false"],
      ncert=f"{NC12}, 'Alcohols, Phenols and Ethers', preparation of phenols", seconds=45),

    N(T_OX, "Carboxylic acids", "Intermediate",
      "A mixture of ethanoic acid and propanoic acid is heated with a mixture of methanol and ethanol in the presence "
      "of a few drops of concentrated sulphuric acid. How many different esters can be formed?",
      ["2", "4", "3", "6"], "B", v_1951,
      "Esterification: each acid can combine with each alcohol",
      "An ester R–COO–R′ takes its acyl part from the acid and its alkyl part from the alcohol. Two acids × two "
      "alcohols give four combinations.",
      ["Methyl ethanoate", "Ethyl ethanoate", "Methyl propanoate", "Ethyl propanoate", "Total = 4"],
      why_others_wrong="2 pairs each acid with only one alcohol; 3 treats ethyl ethanoate and methyl propanoate (which "
                       "are isomers) as the same compound; 6 counts acid–acid or alcohol–alcohol products as esters.",
      ncert=f"{NC12}, 'Aldehydes, Ketones and Carboxylic Acids', esterification", seconds=40),

    N(T_OX, "Aldehydes and ketones", "Intermediate",
      "5.8 g of propanone reacts completely with semicarbazide, H₂N–CO–NH–NH₂, in weakly acidic solution to form "
      "propanone semicarbazone. The mass of the semicarbazone formed is (C = 12, H = 1, N = 14, O = 16):",
      ["13.3 g", "7.2 g", "5.8 g", "11.5 g"], "D", v_1952,
      "Reaction of carbonyl compounds with ammonia derivatives",
      ">C=O + H₂N–Z → >C=N–Z + H₂O. Propanone gives (CH₃)₂C=N–NH–CO–NH₂, C₄H₉N₃O (M = 115).",
      ["n(propanone) = 5.8/58 = 0.10 mol", "M(semicarbazone) = 58 + 75 − 18 = 115 g mol⁻¹",
       "Mass = 0.10 × 115 = 11.5 g"],
      why_others_wrong="13.3 g forgets that water is eliminated; 7.2 g is for the hydrazone (C₃H₈N₂); 5.8 g just "
                       "repeats the mass of propanone.",
      ncert=f"{NC12}, 'Aldehydes, Ketones and Carboxylic Acids', reactions with ammonia derivatives", seconds=50),

    N(T_OX, "Aldehydes and ketones", "Intermediate",
      "7.025 g of benzoyl chloride is hydrogenated over palladium on barium sulphate (Rosenmund reduction). Assuming "
      "complete conversion, the mass of benzaldehyde formed is (C = 12, H = 1, O = 16, Cl = 35.5):",
      ["5.3 g", "5.4 g", "6.1 g", "10.6 g"], "A", v_1953,
      "Rosenmund reduction of acyl chlorides",
      "C₆H₅COCl + H₂ → C₆H₅CHO + HCl. The poisoned catalyst stops the reduction at the aldehyde.",
      ["M(C₆H₅COCl) = 140.5 g mol⁻¹ → n = 0.05 mol", "n(C₆H₅CHO) = 0.05 mol", "Mass = 0.05 × 106 = 5.3 g"],
      why_others_wrong="5.4 g is benzyl alcohol (over-reduction, which the Pd–BaSO₄ catalyst prevents); 6.1 g is "
                       "benzoic acid (hydrolysis); 10.6 g takes 0.10 mol.",
      ncert=f"{NC12}, 'Aldehydes, Ketones and Carboxylic Acids', preparation of aldehydes from acyl chlorides",
      seconds=45),

    Q(T_OX, "Ethers", "Intermediate", "direct",
      "Ethyl methyl ether (methoxyethane), CH₃–O–CH₂CH₃, is heated with one equivalent of concentrated HI. The main "
      "products are:",
      ["CH₃CH₂I and CH₃OH", "CH₃I and CH₃I", "CH₃I and CH₃CH₂OH", "CH₃CH₂I and CH₃CH₂OH"], "C",
      "Cleavage of unsymmetrical ethers by HI",
      "The ether oxygen is first protonated. The iodide ion then attacks by SN2, choosing the less hindered (smaller) "
      "alkyl group, so iodomethane and ethanol are formed.",
      ["CH₃–O⁺(H)–C₂H₅ formed", "I⁻ attacks the less hindered CH₃ (SN2)", "→ CH₃I + C₂H₅OH"],
      why_others_wrong="CH₃CH₂I + CH₃OH would need I⁻ to attack the more hindered ethyl group; the other two options "
                       "are not balanced products of a single cleavage.",
      ncert=f"{NC12}, 'Alcohols, Phenols and Ethers', reactions of ethers: cleavage of the C–O bond", seconds=40),

    Q(T_OX, "Aldehydes and ketones", "Intermediate", "assertion_reason",
      *ar("Methanal undergoes the Cannizzaro reaction with concentrated alkali.", True,
          "Methanal is a gas at room temperature.", True, explains=False),
      "Cannizzaro reaction",
      "The Cannizzaro reaction is shown by aldehydes that have no α-hydrogen; methanal has none, so it disproportionates "
      "into methanol and methanoate. R is a true physical property of methanal, but it has nothing to do with the "
      "reaction.",
      ["Methanal: no α-H → Cannizzaro (A true)", "Methanal is a gas (R true)", "R does not explain A"],
      ncert=f"{NC12}, 'Aldehydes, Ketones and Carboxylic Acids', Cannizzaro reaction; physical properties", seconds=30),

    Q(T_OX, "Alcohols", "Intermediate", "statement_pair",
      *sp("Alcohols can act both as Brönsted acids and as Brönsted bases.", True,
          "Sodium ethoxide is a stronger base than sodium hydroxide.", True),
      "Acidic and basic character of alcohols",
      "An alcohol donates the O–H proton (acid) and its oxygen lone pairs accept a proton (base). Alcohols are weaker "
      "acids than water, so the alkoxide ion is a better proton acceptor than hydroxide: sodium ethoxide is a stronger "
      "base than NaOH. Both statements are true.",
      ["R–OH → R–O⁻ + H⁺ (acid)", "R–OH + H⁺ → R–OH₂⁺ (base)", "ROH weaker acid than H₂O → RO⁻ stronger base than OH⁻"],
      ncert=f"{NC12}, 'Alcohols, Phenols and Ethers', acidity of alcohols", seconds=35),

    Q(T_OX, "Aldehydes and ketones", "Intermediate", "match_list",
      *ml("Match the reaction in List-I with its name in List-II.",
          ["An alkyl halide is heated with a sodium alkoxide",
           "An aldehyde having α-hydrogen is treated with dilute NaOH",
           "An aldehyde having no α-hydrogen is heated with concentrated NaOH",
           "A carboxylic acid having α-hydrogen is treated with Cl₂ and a little red phosphorus"],
          ["Cannizzaro reaction", "Hell–Volhard–Zelinsky reaction", "Williamson synthesis", "Aldol reaction"],
          "III IV I II", ["IV III I II", "III I IV II", "III IV II I"], "D"),
      "Named reactions of oxygen compounds",
      "Alkoxide + alkyl halide → ether (Williamson); α-H aldehyde + dilute alkali → β-hydroxy aldehyde (aldol); "
      "no α-H aldehyde + concentrated alkali → alcohol + carboxylate (Cannizzaro); α-halogenation of acids with "
      "X₂/red P → HVZ reaction.",
      ["A → Williamson (III)", "B → aldol (IV)", "C → Cannizzaro (I)", "D → HVZ (II)"],
      why_others_wrong="The other codes interchange the aldol and Cannizzaro reactions (which depend on the presence "
                       "or absence of α-H) or the Williamson and HVZ reactions.",
      ncert=f"{NC12}, 'Alcohols, Phenols and Ethers'; 'Aldehydes, Ketones and Carboxylic Acids', named reactions",
      seconds=45),

    Q(T_OX, "Aldehydes and ketones", "Intermediate", "multi_statement",
      *ms("Which of the following statements are correct?",
          [("Propanal undergoes aldol condensation in the presence of dilute alkali.", True),
           ("2,2-Dimethylpropanal undergoes the Cannizzaro reaction with concentrated alkali.", True),
           ("Benzaldehyde undergoes self aldol condensation with dilute alkali.", False),
           ("The aldol formed from two molecules of propanal is 3-hydroxy-2-methylpentanal.", True),
           ("Ethanal undergoes the Cannizzaro reaction with concentrated alkali.", False)],
          [["a", "b"], ["b", "d", "e"], ["a", "c", "d"]], "C"),
      "α-Hydrogen decides between aldol and Cannizzaro reactions",
      "Aldehydes with α-H (propanal, ethanal) undergo aldol reactions; those without α-H (2,2-dimethylpropanal, "
      "benzaldehyde, methanal) undergo the Cannizzaro reaction. In propanal's aldol, the α-carbanion CH₃CH⁻–CHO adds "
      "to the C=O of a second molecule: CH₃CH₂CH(OH)–CH(CH₃)–CHO, 3-hydroxy-2-methylpentanal.",
      ["(a) true", "(b) true: no α-H", "(c) false: no α-H", "(d) true", "(e) false: has α-H"],
      ncert=f"{NC12}, 'Aldehydes, Ketones and Carboxylic Acids', aldol and Cannizzaro reactions", seconds=60),

    N(T_OX, "Aldehydes and ketones", "Advanced",
      "2.3 g of ethanol is oxidised with PCC to X. X is treated with CH₃MgBr and the product is hydrolysed to give Y. "
      "Y is oxidised with acidified K₂Cr₂O₇ to Z, and Z is warmed with iodine and aqueous NaOH. Assuming every step "
      "is complete, the mass of iodoform formed is (C = 12, H = 1, O = 16, I = 127):",
      ["39.4 g", "19.7 g", "9.85 g", "19.1 g"], "B", v_1959,
      "Multi-step conversion: aldehyde → secondary alcohol → methyl ketone → iodoform",
      "X = ethanal; Y = propan-2-ol; Z = propanone. Each step is 1 : 1, and one mole of propanone gives one mole of "
      "CHI₃.",
      ["n(C₂H₅OH) = 2.3/46 = 0.05 mol", "→ 0.05 mol CH₃CHO → 0.05 mol CH₃CH(OH)CH₃ → 0.05 mol CH₃COCH₃",
       "n(CHI₃) = 0.05 mol; M(CHI₃) = 394", "Mass = 0.05 × 394 = 19.7 g"],
      why_others_wrong="39.4 g doubles the amount; 9.85 g halves it; 19.1 g uses only the mass of three iodine atoms "
                       "(381) as the molar mass of iodoform.",
      ncert=f"{NC12}, 'Aldehydes, Ketones and Carboxylic Acids', Grignard addition and haloform reaction", seconds=90),

    Q(T_OX, "Alcohols", "Advanced", "direct",
      "A compound X, C₇H₈O, contains a benzene ring. It does not dissolve in aqueous NaOH, but it liberates hydrogen "
      "with sodium metal. On vigorous oxidation with alkaline KMnO₄ followed by acidification, it gives benzoic acid. "
      "X is:",
      ["Benzyl alcohol", "Anisole (methoxybenzene)", "o-Cresol", "p-Cresol"], "A",
      "Distinguishing an aromatic alcohol from phenols and ethers",
      "Insolubility in NaOH rules out the acidic cresols (phenols). Reaction with sodium shows an O–H group, which "
      "rules out anisole. Oxidation of the side chain –CH₂OH to –COOH gives benzoic acid. X is C₆H₅CH₂OH.",
      ["Not soluble in NaOH → not a phenol", "H₂ with Na → has O–H → not an ether", "Side chain → –COOH → benzyl alcohol"],
      why_others_wrong="Anisole has no O–H and does not liberate H₂ with Na; o- and p-cresol are phenols and dissolve "
                       "in aqueous NaOH.",
      ncert=f"{NC12}, 'Alcohols, Phenols and Ethers', acidity of alcohols and phenols", seconds=60),

    Q(T_OX, "Aldehydes and ketones", "Advanced", "assertion_reason",
      *ar("Ketones are generally more reactive than aldehydes in nucleophilic addition reactions.", False,
          "The two relatively large substituents in a ketone hinder the approach of a nucleophile to the carbonyl "
          "carbon more than the single substituent and hydrogen of an aldehyde do.", True),
      "Relative reactivity of aldehydes and ketones",
      "Aldehydes are more reactive than ketones for both steric and electronic reasons: the two alkyl groups of a "
      "ketone hinder the nucleophile and also reduce the electrophilicity of the carbonyl carbon. A is false; R is a "
      "true statement (and in fact explains why ketones are less reactive).",
      ["Aldehydes > ketones in nucleophilic addition → A false", "Steric hindrance by two groups in ketones → R true"],
      ncert=f"{NC12}, 'Aldehydes, Ketones and Carboxylic Acids', nucleophilic addition reactions", seconds=35),

    Q(T_OX, "Carboxylic acids", "Advanced", "statement_pair",
      *sp("Esterification of a carboxylic acid with an alcohol in the presence of concentrated H₂SO₄ is an "
          "irreversible reaction.", False,
          "Esterification of a carboxylic acid with an alcohol is catalysed by a small amount of concentrated "
          "sulphuric acid or HCl gas.", True),
      "Equilibrium nature of esterification",
      "Esterification is reversible; the equilibrium is shifted towards the ester by removing water or ester as it "
      "forms. A mineral acid such as concentrated H₂SO₄ or HCl gas catalyses it. Statement I is false and Statement II "
      "is true.",
      ["RCOOH + R′OH ⇌ RCOOR′ + H₂O (reversible)", "H⁺ catalyst (conc. H₂SO₄ or HCl gas)"],
      ncert=f"{NC12}, 'Aldehydes, Ketones and Carboxylic Acids', esterification", seconds=35),

    Q(T_OX, "Phenols", "Advanced", "match_list",
      *ml("Match the compound in List-I with its approximate pKa in List-II.",
          ["Ethanol", "Phenol", "4-Nitrophenol", "2,4,6-Trinitrophenol"],
          ["≈ 0.5", "≈ 7.1", "≈ 10.0", "≈ 15.9"],
          "IV III II I", ["III IV II I", "IV II III I", "IV III I II"], "C"),
      "Acid strength of alcohols and phenols",
      "The lower the pKa, the stronger the acid. Ethanol is a weaker acid than phenol (no resonance stabilisation of "
      "ethoxide). Each nitro group at an ortho or para position withdraws electrons and stabilises the phenoxide ion, "
      "so 4-nitrophenol is stronger than phenol and 2,4,6-trinitrophenol is very strong.",
      ["Acid strength: picric acid > 4-nitrophenol > phenol > ethanol", "pKa: ≈0.5 < ≈7.1 < ≈10.0 < ≈15.9",
       "A-IV, B-III, C-II, D-I"],
      why_others_wrong="The other codes make phenol weaker than ethanol, or 4-nitrophenol weaker than phenol, or give "
                       "the trinitro compound a higher pKa than 4-nitrophenol.",
      ncert=f"{NC12}, 'Alcohols, Phenols and Ethers', acidity of phenols (pKa table)", seconds=55),

    Q(T_OX, "Aldehydes and ketones", "Advanced", "multi_statement",
      *ms("Which of the following are shown by BOTH ethanal and propanone?",
          [("A yellow precipitate of iodoform when warmed with iodine and aqueous NaOH", True),
           ("An orange-yellow precipitate with 2,4-dinitrophenylhydrazine", True),
           ("A silver mirror with Tollens' reagent", False),
           ("A red-brown precipitate with Fehling's solution", False),
           ("Addition of HCN to form a cyanohydrin", True)],
          [["a", "b", "c"], ["b", "e"], ["a", "c", "d", "e"]], "B"),
      "Common and distinguishing reactions of an aldehyde and a ketone",
      "Both contain a CH₃–CO– group (iodoform positive) and a carbonyl group (2,4-DNP derivative, cyanohydrin). Only "
      "the aldehyde is oxidised by the mild oxidants in Tollens' and Fehling's reagents.",
      ["(a) both: CH₃CO– group", "(b) both: C=O", "(c) only ethanal", "(d) only ethanal", "(e) both"],
      ncert=f"{NC12}, 'Aldehydes, Ketones and Carboxylic Acids', chemical reactions", seconds=50),
]

# ================================================================ Organic Compounds Containing Nitrogen (1965-1977)
# 1966: C6H5NO2 + 3H2 -> C6H5NH2 + 2H2O ; 12.3 g nitrobenzene
n_1966 = F(123, 10) / mm(C=6, H=5, N=1, O=2)
assert n_1966 == F(1, 10)
v_1966 = f"{float(n_1966 * 3 * F(224, 10)):.2f} L"
assert v_1966 == "6.72 L"
# 1969: C6H5N2+BF4- -> C6H5F + BF3 + N2 ; 9.3 g aniline -> 0.1 mol salt -> 0.2 mol gas
n_1969 = F(93, 10) / mm(C=6, H=7, N=1)
assert n_1969 == F(1, 10)
v_1969 = f"{float(n_1969 * 2 * F(224, 10)):.2f} L"
assert v_1969 == "4.48 L"
# 1970: NCERT pKb values; ammonia 4.75; count stronger bases (smaller pKb)
pkb = {"CH3NH2": 3.38, "(CH3)2NH": 3.27, "(CH3)3N": 4.22, "C2H5NH2": 3.29, "C6H5NH2": 9.38, "C6H5NHCH3": 9.30,
       "p-nitroaniline": 13.0}
v_1970 = str(sum(1 for v in pkb.values() if v < 4.75))
assert v_1970 == "4"
# 1974: Hinsberg: secondary amines give alkali-insoluble sulphonamides; tertiary do not react
cls = {"CH3NH2": 1, "(CH3)2NH": 2, "(CH3)3N": 3, "C6H5NH2": 1, "C6H5NHCH3": 2, "(C2H5)2NH": 2, "C6H5N(CH3)2": 3}
v_1974 = str(sum(1 for c in cls.values() if c == 2))
assert v_1974 == "3"

QUESTIONS += [
    Q(T_NI, "Amines: basicity and identification", "Basic", "direct",
      "The IUPAC name of CH₃–CH(NH₂)–CH₂–CH₃ is:",
      ["2-Aminobutane", "Butan-3-amine", "1-Methylpropanamine", "Butan-2-amine"], "D",
      "IUPAC names of amines",
      "The –NH₂ group is the principal group, named by replacing the final 'e' of the alkane by 'amine'. The chain "
      "is numbered so that the carbon bearing –NH₂ gets the lowest locant.",
      ["Chain: 4 C → butane", "–NH₂ on C-2 (lowest)", "Name: butan-2-amine"],
      why_others_wrong="'2-Aminobutane' cites the principal group as a prefix; 'butan-3-amine' numbers from the wrong "
                       "end; '1-methylpropanamine' does not use the longest chain.",
      ncert=f"{NC12}, 'Amines', nomenclature", seconds=25),

    N(T_NI, "Amines: basicity and identification", "Basic",
      "12.3 g of nitrobenzene is reduced completely to aniline by catalytic hydrogenation:\n"
      "C₆H₅NO₂ + 3H₂ → C₆H₅NH₂ + 2H₂O\n"
      "The volume of hydrogen consumed, measured at STP, is (C = 12, H = 1, N = 14, O = 16; molar volume at STP = "
      "22.4 L mol⁻¹):",
      ["2.24 L", "6.72 L", "4.48 L", "8.96 L"], "B", v_1966,
      "Reduction of nitro compounds to amines",
      "Three moles of H₂ are needed per mole of nitrobenzene: two to remove the oxygen atoms as water and one to "
      "supply the two hydrogens on nitrogen.",
      ["n(C₆H₅NO₂) = 12.3/123 = 0.10 mol", "n(H₂) = 3 × 0.10 = 0.30 mol", "V = 0.30 × 22.4 = 6.72 L"],
      why_others_wrong="2.24 L uses a 1 : 1 ratio; 4.48 L counts only the H₂ that forms water; 8.96 L uses four moles "
                       "of H₂.",
      ncert=f"{NC12}, 'Amines', preparation of amines by reduction of nitro compounds", seconds=40),

    Q(T_NI, "Amines: basicity and identification", "Basic", "statement_pair",
      *sp("The –NH₂ group attached to a benzene ring is a strongly activating, ortho- and para-directing group.", True,
          "The activating effect of the –NH₂ group can be controlled by first acetylating it to –NHCOCH₃.", True),
      "Electrophilic substitution in aniline and its control",
      "The lone pair on nitrogen is delocalised into the ring (+R), making the ortho and para positions very electron "
      "rich. In acetanilide the nitrogen lone pair is also delocalised onto the acetyl oxygen, so the group is less "
      "activating and monosubstitution becomes possible. Both statements are true.",
      ["–NH₂: +R → o/p, strongly activating", "–NHCOCH₃: lone pair shared with C=O → moderate activation"],
      ncert=f"{NC12}, 'Amines', electrophilic substitution", seconds=30),

    Q(T_NI, "Amines: basicity and identification", "Basic", "multi_statement",
      *ms("Which of the following statements are correct?",
          [("Amines react with mineral acids to form ammonium salts.", True),
           ("Anilinium chloride regenerates aniline when treated with aqueous NaOH.", True),
           ("Aniline is highly soluble in water.", False),
           ("Aniline dissolves in dilute hydrochloric acid.", True),
           ("Tertiary aliphatic amines liberate nitrogen gas with nitrous acid.", False)],
          [["a", "b"], ["b", "d", "e"], ["a", "c", "d"]], "C"),
      "Salt formation by amines",
      "Amines are bases and form salts with acids: C₆H₅NH₂ + HCl → C₆H₅NH₃⁺Cl⁻, which is water soluble, so aniline "
      "dissolves in dilute HCl. A strong base sets the amine free again. Aniline itself, with its large hydrophobic "
      "phenyl group, is only sparingly soluble in water. Evolution of N₂ with nitrous acid is a reaction of primary "
      "aliphatic amines.",
      ["(a) true", "(b) true", "(c) false", "(d) true", "(e) false"],
      ncert=f"{NC12}, 'Amines', physical properties and basic character", seconds=45),

    N(T_NI, "Diazonium salts", "Intermediate",
      "9.3 g of aniline is diazotised and the diazonium salt is converted completely into benzenediazonium "
      "fluoroborate, C₆H₅N₂⁺BF₄⁻. This is heated until it decomposes completely into fluorobenzene, boron trifluoride "
      "and nitrogen. The total volume of gases released, measured at STP, is (C = 12, H = 1, N = 14; molar volume at "
      "STP = 22.4 L mol⁻¹):",
      ["2.24 L", "6.72 L", "1.12 L", "4.48 L"], "D", v_1969,
      "Balz–Schiemann reaction",
      "C₆H₅N₂⁺BF₄⁻ → C₆H₅F + BF₃↑ + N₂↑. Each mole of the salt releases two moles of gas.",
      ["n(aniline) = 9.3/93 = 0.10 mol → 0.10 mol salt", "Gas: 0.10 mol N₂ + 0.10 mol BF₃ = 0.20 mol",
       "V = 0.20 × 22.4 = 4.48 L"],
      why_others_wrong="2.24 L counts only N₂ (or only BF₃); 6.72 L adds a third gas; 1.12 L halves the amount.",
      ncert=f"{NC12}, 'Amines', reactions of diazonium salts: replacement by fluoride", seconds=55),

    N(T_NI, "Amines: basicity and identification", "Intermediate",
      "NCERT's table lists the pKb values of several amines in aqueous solution; for ammonia, pKb = 4.75. How many of "
      "the following are stronger bases than ammonia in aqueous solution?\n"
      "CH₃NH₂, (CH₃)₂NH, (CH₃)₃N, C₂H₅NH₂, C₆H₅NH₂, C₆H₅NHCH₃, p-nitroaniline",
      ["3", "4", "5", "7"], "B", v_1970,
      "Basic strength of aliphatic and aromatic amines",
      "A smaller pKb means a stronger base. All the aliphatic amines (pKb ≈ 3.3–4.2) are stronger bases than ammonia "
      "because of the +I effect of the alkyl groups. In aryl amines the lone pair is delocalised into the ring, so "
      "they are much weaker bases (pKb ≈ 9.3–9.4, even higher for p-nitroaniline).",
      ["Aliphatic: CH₃NH₂ 3.38, (CH₃)₂NH 3.27, (CH₃)₃N 4.22, C₂H₅NH₂ 3.29 → all < 4.75",
       "Aromatic: C₆H₅NH₂ 9.38, C₆H₅NHCH₃ 9.30, p-nitroaniline → all > 4.75", "Total = 4"],
      why_others_wrong="3 leaves out trimethylamine, which in water is weaker than the other methylamines but still "
                       "stronger than ammonia; 5 or 7 count aromatic amines, which are weaker than ammonia.",
      ncert=f"{NC12}, 'Amines', basic character of amines (pKb values)", seconds=60),

    Q(T_NI, "Amines: basicity and identification", "Intermediate", "assertion_reason",
      *ar("Direct nitration of aniline gives, besides the ortho and para derivatives, a significant amount of "
          "m-nitroaniline.", True,
          "In the strongly acidic nitrating mixture, aniline is protonated to the anilinium ion, which is "
          "meta-directing.", True, explains=True),
      "Nitration of aniline",
      "–NH₂ is ortho/para directing, but in concentrated acid much of the aniline exists as C₆H₅NH₃⁺. The –NH₃⁺ group "
      "has no lone pair and withdraws electrons, so it directs to the meta position. R explains A.",
      ["C₆H₅NH₂ + H⁺ → C₆H₅NH₃⁺", "–NH₃⁺: electron-withdrawing, meta-directing", "→ m-nitroaniline formed"],
      ncert=f"{NC12}, 'Amines', electrophilic substitution: nitration", seconds=35),

    Q(T_NI, "Amines: basicity and identification", "Intermediate", "match_list",
      *ml("Match the conversion in List-I with the reagent(s) used in List-II.",
          ["Nitrobenzene → aniline", "Benzamide → aniline", "Ethanenitrile → ethanamine",
           "Phthalimide → primary aliphatic amine"],
          ["Bromine and aqueous NaOH, warmed", "Ethanolic KOH, then an alkyl halide, then alkaline hydrolysis",
           "Iron scrap and hydrochloric acid", "Lithium aluminium hydride (or H₂ with a nickel catalyst)"],
          "III I IV II", ["I III IV II", "III IV I II", "III I II IV"], "C"),
      "Methods of preparing amines",
      "Nitro compounds are reduced by Fe/HCl. Amides lose a carbon in the Hofmann bromamide degradation (Br₂/NaOH). "
      "Nitriles are reduced to primary amines by LiAlH₄ or by catalytic hydrogenation. Gabriel synthesis converts "
      "phthalimide, via its potassium salt and an alkyl halide, into a primary amine on alkaline hydrolysis.",
      ["A → III", "B → I", "C → IV", "D → II"],
      why_others_wrong="The other codes swap the reduction of the nitro group with the Hofmann degradation, or the "
                       "nitrile reduction with the Gabriel synthesis.",
      ncert=f"{NC12}, 'Amines', preparation of amines", seconds=45),

    Q(T_NI, "Amines: basicity and identification", "Intermediate", "assertion_reason",
      *ar("Ethanamine is soluble in water.", True,
          "Ethanamine is a stronger base than ammonia in aqueous solution.", True, explains=False),
      "Solubility versus basicity of lower amines",
      "Lower aliphatic amines dissolve in water because they form hydrogen bonds with water molecules. Ethanamine's "
      "greater basicity than ammonia comes from the +I effect of the ethyl group. Both statements are true, but the "
      "basic strength is a separate property and does not explain the solubility.",
      ["Solubility: H-bonding with water (A true)", "Basicity: +I of C₂H₅ (R true)", "R does not explain A"],
      ncert=f"{NC12}, 'Amines', physical properties and basic character", seconds=30),

    N(T_NI, "Amines: basicity and identification", "Advanced",
      "Each of the following is shaken with benzenesulphonyl chloride (Hinsberg's reagent). How many of them give a "
      "product that is insoluble in aqueous alkali?\n"
      "CH₃NH₂, (CH₃)₂NH, (CH₃)₃N, C₆H₅NH₂, C₆H₅NHCH₃, (C₂H₅)₂NH, C₆H₅N(CH₃)₂",
      ["5", "2", "4", "3"], "D", v_1974,
      "Hinsberg's test",
      "Primary amines give N-substituted sulphonamides that still carry an acidic N–H, so they dissolve in alkali. "
      "Secondary amines give N,N-disubstituted sulphonamides with no N–H: insoluble in alkali. Tertiary amines do "
      "not react.",
      ["Primary (CH₃NH₂, C₆H₅NH₂): product soluble in alkali", "Secondary ((CH₃)₂NH, C₆H₅NHCH₃, (C₂H₅)₂NH): insoluble",
       "Tertiary ((CH₃)₃N, C₆H₅N(CH₃)₂): no reaction", "Count = 3"],
      why_others_wrong="5 adds the tertiary amines, which give no product at all; 2 misses N-methylaniline, an aryl "
                       "secondary amine; 4 counts aniline, a primary amine.",
      ncert=f"{NC12}, 'Amines', reaction with arylsulphonyl chloride (Hinsberg's test)", seconds=60),

    Q(T_NI, "Amines: basicity and identification", "Advanced", "direct",
      "Benzoic acid is heated with thionyl chloride, and the product is treated with ammonia to give X. X is warmed "
      "with bromine and aqueous NaOH to give Y. Y is:",
      ["Benzylamine", "Benzonitrile", "Aniline", "Benzamide"], "C",
      "Acid → acyl chloride → amide → amine with one carbon fewer",
      "C₆H₅COOH + SOCl₂ → C₆H₅COCl; with NH₃ → X = C₆H₅CONH₂ (benzamide). Hofmann bromamide degradation removes the "
      "carbonyl carbon: Y = C₆H₅NH₂.",
      ["C₆H₅COCl → C₆H₅CONH₂ (X)", "Br₂ + NaOH → C₆H₅NH₂ (Y)"],
      why_others_wrong="Benzylamine would keep all seven carbons (reduction of the amide with LiAlH₄); benzonitrile "
                       "needs dehydration of the amide; benzamide is X, not Y.",
      ncert=f"{NC12}, 'Amines', Hofmann bromamide degradation", seconds=50),

    Q(T_NI, "Amines: basicity and identification", "Advanced", "statement_pair",
      *sp("In the acylation of amines, a hydrogen atom of the –NH₂ or >NH group is replaced by an acyl group.", True,
          "Tertiary amines are readily acylated by ethanoyl chloride to give amides.", False),
      "Acylation of amines",
      "Acylation is nucleophilic substitution in which the amine nitrogen attacks the acyl chloride and an N–H "
      "hydrogen is lost (as HCl, removed by pyridine). Tertiary amines have no hydrogen on nitrogen, so they do not "
      "give amides. Statement I is true and Statement II false.",
      ["R–NH₂ + CH₃COCl → R–NHCOCH₃ + HCl", "R₃N: no N–H → no amide"],
      ncert=f"{NC12}, 'Amines', acylation", seconds=35),

    Q(T_NI, "Diazonium salts", "Advanced", "match_list",
      *ml("Match the reagent in List-I, used with benzenediazonium chloride, with the main organic product in List-II.",
          ["Copper powder and HCl", "Hypophosphorous acid (H₃PO₂) and water", "Phenol in mildly alkaline medium",
           "Aniline in mildly acidic medium"],
          ["p-Aminoazobenzene (yellow dye)", "Chlorobenzene", "p-Hydroxyazobenzene (orange dye)", "Benzene"],
          "II IV III I", ["IV II III I", "II IV I III", "II III IV I"], "A"),
      "Replacement and coupling reactions of diazonium salts",
      "Cu/HCl replaces –N₂⁺ by –Cl (Gattermann reaction); H₃PO₂ replaces it by H; coupling with phenoxide gives the "
      "orange p-hydroxyazobenzene and with aniline the yellow p-aminoazobenzene, both retaining –N=N–.",
      ["A → chlorobenzene (II)", "B → benzene (IV)", "C → p-hydroxyazobenzene (III)", "D → p-aminoazobenzene (I)"],
      why_others_wrong="The other codes swap the two replacement reactions or the two coupling products.",
      ncert=f"{NC12}, 'Amines', chemical reactions of diazonium salts", seconds=50),
]

# ================================================================ Biomolecules (1978-1990)
# 1979: glucose + HI (prolonged heating) -> n-hexane C6H14 ; 18 g glucose
v_1979 = g(F(18) / mm(C=6, H=12, O=6) * mm(C=6, H=14))
assert v_1979 == "8.6 g"
# 1982: reducing sugars among five
reducing = {"glucose": True, "fructose": True, "sucrose": False, "maltose": True, "lactose": True}
v_1982 = str(sum(reducing.values()))
assert v_1982 == "4"
# 1987: glucose + 5 (CH3CO)2O -> pentaacetate + 5 CH3COOH ; 9.0 g glucose
n_1987 = F(9) / mm(C=6, H=12, O=6)
v_1987 = g(n_1987 * 5 * mm(C=4, H=6, O=3), 2)
assert v_1987 == "25.50 g" and g(n_1987 * mm(C=4, H=6, O=3), 2) == "5.10 g"

QUESTIONS += [
    Q(T_BM, "Carbohydrates", "Basic", "direct",
      "Which of the following gives only D-glucose on complete hydrolysis?",
      ["Sucrose", "Maltose", "Lactose", "Fructose"], "B",
      "Composition of disaccharides",
      "Maltose is made of two α-D-glucose units, so its hydrolysis gives only glucose. Sucrose gives glucose and "
      "fructose; lactose gives galactose and glucose; fructose is a monosaccharide and is not hydrolysed.",
      ["Maltose → 2 glucose", "Sucrose → glucose + fructose", "Lactose → galactose + glucose"],
      why_others_wrong="Sucrose and lactose each give a second sugar; fructose cannot be hydrolysed.",
      ncert=f"{NC12}, 'Biomolecules', disaccharides", seconds=20),

    N(T_BM, "Carbohydrates", "Basic",
      "On prolonged heating with HI, glucose is converted into n-hexane. The mass of n-hexane obtained from 18 g of "
      "glucose, assuming complete conversion, is (C = 12, H = 1, O = 16):",
      ["18.0 g", "4.3 g", "17.2 g", "8.6 g"], "D", v_1979,
      "Evidence for the straight chain of glucose",
      "One molecule of glucose (six carbons in a straight chain) gives one molecule of n-hexane, C₆H₁₄.",
      ["n(glucose) = 18/180 = 0.10 mol", "n(C₆H₁₄) = 0.10 mol; M = 86", "Mass = 8.6 g"],
      why_others_wrong="18.0 g repeats the mass of glucose; 4.3 g and 17.2 g halve or double the 1 : 1 ratio.",
      ncert=f"{NC12}, 'Biomolecules', structure of glucose", seconds=35),

    Q(T_BM, "Carbohydrates", "Basic", "statement_pair",
      *sp("Carbohydrates are classified as monosaccharides, oligosaccharides and polysaccharides according to their "
          "behaviour on hydrolysis.", True,
          "A monosaccharide that contains an aldehyde group is called an aldose.", True),
      "Classification of carbohydrates",
      "Monosaccharides cannot be hydrolysed further, oligosaccharides give two to ten monosaccharide units and "
      "polysaccharides give a large number. A monosaccharide with –CHO is an aldose; one with a keto group is a "
      "ketose. Both statements are true.",
      ["Classification by hydrolysis → true", "Aldehyde group → aldose → true"],
      ncert=f"{NC12}, 'Biomolecules', classification of carbohydrates", seconds=25),

    Q(T_BM, "Vitamins", "Basic", "match_list",
      *ml("Match the vitamin in List-I with its chemical name in List-II.",
          ["Vitamin B₁", "Vitamin B₂", "Vitamin B₆", "Vitamin C"],
          ["Ascorbic acid", "Pyridoxine", "Thiamine", "Riboflavin"],
          "III IV II I", ["IV III II I", "III II IV I", "III IV I II"], "D"),
      "Names of vitamins",
      "Vitamin B₁ is thiamine, B₂ riboflavin, B₆ pyridoxine and C ascorbic acid.",
      ["B₁ → thiamine (III)", "B₂ → riboflavin (IV)", "B₆ → pyridoxine (II)", "C → ascorbic acid (I)"],
      why_others_wrong="The other codes swap thiamine and riboflavin, or riboflavin and pyridoxine, or pyridoxine and "
                       "ascorbic acid.",
      ncert=f"{NC12}, 'Biomolecules', vitamins (table of vitamins and their sources)", seconds=30),

    N(T_BM, "Carbohydrates", "Intermediate",
      "How many of the following are reducing sugars?\nGlucose, fructose, sucrose, maltose, lactose",
      ["3", "4", "5", "2"], "B", v_1982,
      "Reducing and non-reducing sugars",
      "A sugar is reducing if it has (or can open to give) a free aldehydic or ketonic group. All monosaccharides are "
      "reducing. In maltose and lactose one unit keeps a free anomeric carbon. In sucrose the reducing groups of both "
      "glucose (C1) and fructose (C2) are used in the glycosidic bond.",
      ["Glucose, fructose: reducing", "Maltose, lactose: reducing", "Sucrose: non-reducing", "Total = 4"],
      why_others_wrong="3 usually leaves out fructose, a ketose that is still a reducing sugar; 5 counts sucrose; 2 "
                       "counts only the monosaccharides.",
      ncert=f"{NC12}, 'Biomolecules', reducing and non-reducing sugars", seconds=35),

    Q(T_BM, "Amino acids and proteins", "Intermediate", "assertion_reason",
      *ar("Glycine is optically inactive.", True,
          "Glycine is a basic amino acid.", False),
      "Structure of glycine",
      "Glycine, H₂N–CH₂–COOH, has R = H, so its α-carbon carries two hydrogen atoms and is not chiral: glycine is "
      "optically inactive (A true). With one amino and one carboxyl group it is a neutral amino acid, not a basic one "
      "(R false).",
      ["α-C of glycine: H, H, NH₂, COOH → not chiral", "One –NH₂ and one –COOH → neutral amino acid"],
      ncert=f"{NC12}, 'Biomolecules', amino acids", seconds=30),

    Q(T_BM, "Nucleic acids", "Intermediate", "match_list",
      *ml("Match the description in List-I with the component of nucleic acids in List-II.",
          ["Purine bases present in both DNA and RNA", "Pyrimidine base present in DNA but not in RNA",
           "Pyrimidine base present in RNA but not in DNA", "Sugar present in DNA"],
          ["Adenine and guanine", "Uracil", "2-Deoxy-D-ribose", "Thymine"],
          "I IV II III", ["I II IV III", "IV I II III", "I IV III II"], "A"),
      "Chemical composition of nucleic acids",
      "DNA contains adenine, guanine, cytosine and thymine with 2-deoxy-D-ribose; RNA contains adenine, guanine, "
      "cytosine and uracil with D-ribose. Adenine and guanine are purines; cytosine, thymine and uracil are "
      "pyrimidines.",
      ["Purines: A, G (I)", "DNA-only pyrimidine: thymine (IV)", "RNA-only pyrimidine: uracil (II)",
       "DNA sugar: 2-deoxy-D-ribose (III)"],
      why_others_wrong="The other codes swap thymine and uracil, or put a base in place of the sugar.",
      ncert=f"{NC12}, 'Biomolecules', nucleic acids: chemical composition", seconds=35),

    Q(T_BM, "Amino acids and proteins", "Intermediate", "multi_statement",
      *ms("Which of the following statements about proteins are correct?",
          [("In fibrous proteins the polypeptide chains run parallel and are held together by hydrogen and "
            "disulphide bonds.", True),
           ("Denaturation of a protein destroys its primary structure.", False),
           ("Keratin is a globular protein.", False),
           ("The spatial arrangement of two or more polypeptide subunits with respect to each other is the "
            "quaternary structure.", True),
           ("A peptide bond is formed between the –COOH group of one amino acid and the –NH₂ group of another, "
            "with the loss of a water molecule.", True)],
          [["a", "b", "d"], ["d", "e"], ["a", "c", "e"]], "D"),
      "Structure of proteins",
      "Fibrous proteins have parallel chains linked by hydrogen and disulphide bonds (keratin, myosin). Denaturation "
      "disturbs the secondary and tertiary structures but leaves the primary structure (sequence) intact. A peptide "
      "bond, –CO–NH–, forms by a condensation that releases water.",
      ["(a) true", "(b) false: primary structure intact", "(c) false: keratin is fibrous", "(d) true", "(e) true"],
      ncert=f"{NC12}, 'Biomolecules', structure of proteins", seconds=50),

    Q(T_BM, "Amino acids and proteins", "Intermediate", "direct",
      "The side chain R of an α-amino acid, H₂N–CH(R)–COOH, is –CH₂–C₆H₄–OH, with the –OH group at the para position "
      "of the benzene ring. The amino acid is:",
      ["Phenylalanine", "Tyrosine", "Tryptophan", "Serine"], "B",
      "Side chains of α-amino acids",
      "Tyrosine has a p-hydroxybenzyl side chain. Phenylalanine has a benzyl side chain without –OH; serine has "
      "–CH₂OH; tryptophan has an indole-containing side chain.",
      ["–CH₂–C₆H₄–OH (p) → tyrosine"],
      why_others_wrong="Phenylalanine lacks the –OH; serine has no ring; tryptophan's ring contains nitrogen (indole).",
      ncert=f"{NC12}, 'Biomolecules', amino acids (table of natural amino acids)", seconds=30),

    N(T_BM, "Carbohydrates", "Advanced",
      "Glucose reacts with acetic anhydride to form glucose pentaacetate, every –OH group being acetylated. The "
      "minimum mass of acetic anhydride, (CH₃CO)₂O, needed to convert 9.0 g of glucose completely into its "
      "pentaacetate is (C = 12, H = 1, O = 16):",
      ["25.50 g", "5.10 g", "15.00 g", "12.75 g"], "A", v_1987,
      "Five –OH groups in glucose",
      "Each –OH group is acetylated by one molecule of acetic anhydride, which also gives one molecule of ethanoic "
      "acid. Glucose has five –OH groups.",
      ["n(glucose) = 9.0/180 = 0.05 mol", "n(anhydride) = 5 × 0.05 = 0.25 mol", "M[(CH₃CO)₂O] = 102 g mol⁻¹",
       "Mass = 0.25 × 102 = 25.50 g"],
      why_others_wrong="5.10 g assumes one anhydride per glucose; 15.00 g is the mass of ethanoic acid formed "
                       "(0.25 × 60); 12.75 g counts one anhydride per two –OH groups.",
      ncert=f"{NC12}, 'Biomolecules', structure of glucose (acetylation)", seconds=60),

    Q(T_BM, "Carbohydrates", "Advanced", "assertion_reason",
      *ar("Lactose is a reducing sugar.", True,
          "Lactose is found in milk.", True, explains=False),
      "Reducing nature of lactose",
      "In lactose, C1 of β-D-galactose is linked to C4 of β-D-glucose, so the glucose unit keeps a free anomeric "
      "carbon (C1) that can open to an aldehyde: lactose is reducing. Its occurrence in milk is true, but it says "
      "nothing about its reducing property.",
      ["Galactose C1 → glucose C4: glucose C1 free → reducing (A true)", "Milk sugar (R true)", "R does not explain A"],
      ncert=f"{NC12}, 'Biomolecules', disaccharides: lactose", seconds=30),

    Q(T_BM, "Hormones", "Advanced", "statement_pair",
      *sp("Hormones are molecules that act as intercellular messengers; they are produced by endocrine glands and "
          "carried by the blood to their target sites.", True,
          "All hormones are steroids.", False),
      "General introduction to hormones",
      "Hormones are chemical messengers released by endocrine glands into the blood. Chemically they are of different "
      "kinds: steroids (e.g. oestrogens, androgens), polypeptides (e.g. insulin) and amino acid derivatives (e.g. "
      "epinephrine, thyroxine). So Statement II is false.",
      ["Statement I: definition → true", "Insulin is a polypeptide, thyroxine an amino acid derivative → II false"],
      ncert=f"{NC12}, 'Biomolecules', hormones (general introduction)", seconds=30),

    Q(T_BM, "Carbohydrates", "Advanced", "multi_statement",
      *ms("Which of the following statements about glucose and its cyclic (hemiacetal) structure are correct?",
          [("Glucose does not give the 2,4-DNP test, although it contains an aldehyde group in its open-chain form.",
            True),
           ("Glucose does not form a hydrogensulphite addition product with NaHSO₃.", True),
           ("In the six-membered ring of glucose, the ring is closed by the –OH group at C-5 adding to the –CHO "
            "group.", True),
           ("Oxidation of glucose by bromine water gives saccharic acid.", False),
           ("The α and β forms of glucose differ in the configuration at C-1, which becomes a new chiral centre on "
            "ring formation.", True)],
          [["a", "b", "c"], ["b", "c", "d", "e"], ["a", "d", "e"]], "D"),
      "Cyclic structure of glucose",
      "The open-chain formula could not explain why glucose does not give the 2,4-DNP test or Schiff's test and does "
      "not form a NaHSO₃ adduct. The C-5 –OH adds to the –CHO group to give a six-membered (pyranose) ring, and C-1 "
      "becomes chiral, giving the α and β anomers. Bromine water oxidises glucose to gluconic acid, not saccharic "
      "acid, and this is a property of the aldehyde group, not evidence for the ring.",
      ["(a) true", "(b) true", "(c) true", "(d) false: gluconic acid", "(e) true"],
      ncert=f"{NC12}, 'Biomolecules', cyclic structure of glucose", seconds=60),
]

# ================================================================ Principles Related to Practical Chemistry (1991-2000)
# 1991: % Fe in Mohr's salt FeSO4.(NH4)2SO4.6H2O (M 392)
mohr = mm(Fe=1, S=2, O=8, N=2, H=8) + 6 * mm(H=2, O=1)
assert mohr == 392
v_1991 = pct(F(56, mohr))
assert v_1991 == "14.3%"
# 1994: KNO3 dissolution: 10.1 g (0.1 mol) in water, solution 100 g, c 4.2 J/g/K, temperature falls 8.0 K
q_1994 = 100 * F(42, 10) * 8
n_1994 = F(101, 10) / mm(K=1, N=1, O=3)
assert n_1994 == F(1, 10)
v_1994 = f"+{float(q_1994 / n_1994 / 1000):.1f} kJ mol⁻¹"
assert v_1994 == "+33.6 kJ mol⁻¹" and f"{float(F(1101, 10) * F(42, 10) * 8 / n_1994 / 1000):.1f}" == "37.0"
# 1995: dissociation enthalpy of CH3COOH = dH_neut(weak) - dH_neut(strong)
v_1995 = f"+{-55.8 - (-57.1):.1f} kJ mol⁻¹"
assert v_1995 == "+1.3 kJ mol⁻¹"
# 1998: 50 mL 0.5 M H2SO4 + 50 mL 1.0 M NaOH -> 0.05 mol water; 100 g solution
n_h = F(50, 1000) * F(5, 10) * 2
n_oh = F(50, 1000) * 1
assert n_h == n_oh == F(5, 100)
dT = n_h * F(571, 10) * 1000 / (100 * F(42, 10))
v_1998 = f"{float(dT):.2f} K"
assert v_1998 == "6.80 K"

QUESTIONS += [
    N(T_PR, "Preparations", "Basic",
      "Mohr's salt, FeSO₄·(NH₄)₂SO₄·6H₂O, is prepared in the laboratory and used as a primary standard. The "
      "percentage of iron by mass in Mohr's salt is (Fe = 56, S = 32, O = 16, N = 14, H = 1):",
      ["36.8%", "20.1%", "14.3%", "28.6%"], "C", v_1991,
      "Percentage composition of a double salt",
      "Mohr's salt has one iron atom per formula unit and a molar mass of 392 g mol⁻¹.",
      ["M = 152 (FeSO₄) + 132 ((NH₄)₂SO₄) + 108 (6H₂O) = 392", "%Fe = 56/392 × 100 = 14.3%"],
      why_others_wrong="36.8% is iron in anhydrous FeSO₄; 20.1% is iron in FeSO₄·7H₂O; 28.6% counts two iron atoms.",
      ncert=f"{LAB}, preparation of double salts: ferrous ammonium sulphate", seconds=40),

    Q(T_PR, "Qualitative salt analysis", "Basic", "direct",
      "In the flame test, a salt gives a lilac (pale violet) colour to the flame, best seen through blue (cobalt) "
      "glass. The cation present is:",
      ["Na⁺", "K⁺", "Ca²⁺", "Sr²⁺"], "B",
      "Flame colours of cations",
      "Potassium salts give a lilac flame; the blue glass absorbs any yellow sodium light that would mask it.",
      ["Lilac through blue glass → K⁺"],
      why_others_wrong="Na⁺ gives a persistent golden-yellow flame, Ca²⁺ brick red and Sr²⁺ crimson red.",
      ncert=f"{LAB}, qualitative analysis: flame test", seconds=20),

    Q(T_PR, "Titrimetric analysis", "Basic", "match_list",
      *ml("Match the titration or experiment in List-I with the indicator used to detect its end point in List-II.",
          ["Oxalic acid against sodium hydroxide", "Sodium carbonate against hydrochloric acid",
           "Oxalic acid against acidified potassium permanganate",
           "Iodine clock reaction of H₂O₂ with iodide (with a little thiosulphate)"],
          ["KMnO₄ itself (self-indicator)", "Starch solution", "Phenolphthalein", "Methyl orange"],
          "III IV I II", ["IV III I II", "III IV II I", "III I IV II"], "A"),
      "Choice of indicator",
      "A weak acid–strong base titration needs phenolphthalein (end point in the alkaline range); the carbonate–strong "
      "acid titration uses methyl orange (end point in the acidic range); permanganate is its own indicator (first "
      "permanent pink); free iodine is detected with starch (blue).",
      ["A → phenolphthalein (III)", "B → methyl orange (IV)", "C → self-indicator (I)", "D → starch (II)"],
      why_others_wrong="The other codes swap phenolphthalein and methyl orange, or the starch and permanganate entries.",
      ncert=f"{LAB}, titrimetric analysis and chemical kinetics experiments", seconds=40),

    N(T_PR, "Thermochemistry and kinetics experiments", "Intermediate",
      "10.1 g of potassium nitrate (molar mass 101 g mol⁻¹) is dissolved in water in a calorimeter, and the "
      "temperature falls by 8.0 K. Take the mass of the solution as 100 g and its specific heat as 4.2 J g⁻¹ K⁻¹, and "
      "ignore the heat capacity of the calorimeter. The enthalpy of solution of KNO₃ is:",
      ["−33.6 kJ mol⁻¹", "+3.4 kJ mol⁻¹", "+37.0 kJ mol⁻¹", "+33.6 kJ mol⁻¹"], "D", v_1994,
      "Enthalpy of solution from a calorimetric experiment",
      "A fall in temperature means heat is absorbed from the surroundings: the dissolution is endothermic. "
      "q = m c ΔT, divided by the moles of salt.",
      ["q = 100 × 4.2 × 8.0 = 3360 J absorbed", "n(KNO₃) = 10.1/101 = 0.10 mol",
       "ΔsolH = +3360/0.10 = +33 600 J mol⁻¹ = +33.6 kJ mol⁻¹"],
      why_others_wrong="−33.6 kJ mol⁻¹ has the wrong sign for a temperature fall; +3.4 kJ mol⁻¹ does not divide by "
                       "the number of moles correctly; +37.0 kJ mol⁻¹ uses 110.1 g (water + salt) instead of the "
                       "100 g stated.",
      ncert=f"{LAB}, thermochemistry: enthalpy of dissolution", seconds=60),

    N(T_PR, "Thermochemistry and kinetics experiments", "Intermediate",
      "In two calorimetric experiments, the enthalpy of neutralisation of hydrochloric acid by NaOH is found to be "
      "−57.1 kJ mol⁻¹ and that of ethanoic acid by NaOH −55.8 kJ mol⁻¹. On this basis, the enthalpy of ionisation "
      "(dissociation) of ethanoic acid is:",
      ["−1.3 kJ mol⁻¹", "+1.3 kJ mol⁻¹", "+112.9 kJ mol⁻¹", "−55.8 kJ mol⁻¹"], "B", v_1995,
      "Neutralisation of a weak acid includes its ionisation",
      "For a strong acid only H⁺ + OH⁻ → H₂O occurs. For ethanoic acid, some of the heat released is used to ionise "
      "the weak acid, so less heat is given out. ΔH(ionisation) = ΔH(neut, weak) − ΔH(neut, strong).",
      ["ΔH(ion) = (−55.8) − (−57.1)", "= +1.3 kJ mol⁻¹ (endothermic)"],
      why_others_wrong="−1.3 kJ mol⁻¹ subtracts in the wrong order; +112.9 kJ mol⁻¹ adds the two magnitudes; −55.8 "
                       "kJ mol⁻¹ is simply the enthalpy of neutralisation of ethanoic acid.",
      ncert=f"{LAB}, thermochemistry: enthalpy of neutralisation of strong and weak acids", seconds=45),

    Q(T_PR, "Detection of elements and functional groups", "Intermediate", "assertion_reason",
      *ar("Carboxylic acids give brisk effervescence with aqueous sodium hydrogencarbonate, but phenols generally "
          "do not.", True,
          "Carboxylic acids are stronger acids than carbonic acid, whereas phenol is a weaker acid than carbonic "
          "acid.", True, explains=True),
      "Sodium hydrogencarbonate test for the carboxyl group",
      "An acid displaces CO₂ from HCO₃⁻ only if it is stronger than carbonic acid. Carboxylic acids are, so CO₂ is "
      "evolved; phenol is weaker, so no effervescence occurs. R explains A.",
      ["RCOOH + NaHCO₃ → RCOONa + H₂O + CO₂↑", "Phenol (weaker than H₂CO₃): no reaction"],
      ncert=f"{LAB}, tests for functional groups: carboxyl group", seconds=35),

    Q(T_PR, "Qualitative salt analysis", "Intermediate", "match_list",
      *ml("Match the precipitate obtained in systematic salt analysis (List-I) with its colour (List-II).",
          ["Fe(OH)₃ (group III)", "Al(OH)₃ (group III)", "CuS (group II)", "MnS (group IV)"],
          ["Black", "Buff (flesh-coloured)", "Reddish-brown", "White, gelatinous"],
          "III IV I II", ["IV III I II", "III IV II I", "II IV I III"], "C"),
      "Colours of group precipitates",
      "Iron(III) hydroxide is reddish-brown and aluminium hydroxide white and gelatinous; copper(II) sulphide is "
      "black; manganese(II) sulphide is buff (flesh) coloured.",
      ["Fe(OH)₃ → III", "Al(OH)₃ → IV", "CuS → I", "MnS → II"],
      why_others_wrong="The other codes swap the two hydroxides, or the two sulphides.",
      ncert=f"{LAB}, systematic analysis of cations", seconds=40),

    N(T_PR, "Thermochemistry and kinetics experiments", "Advanced",
      "50 mL of 0.50 M H₂SO₄ is mixed with 50 mL of 1.0 M NaOH in a calorimeter. Take the enthalpy of neutralisation "
      "as −57.1 kJ per mole of water formed, the mass of the solution as 100 g and its specific heat as "
      "4.2 J g⁻¹ K⁻¹, and ignore the heat capacity of the calorimeter. The rise in temperature is:",
      ["3.40 K", "6.80 K", "13.60 K", "0.68 K"], "B", v_1998,
      "Neutralisation of a dibasic acid",
      "H₂SO₄ is dibasic: 0.025 mol of acid supplies 0.050 mol H⁺, which exactly neutralises 0.050 mol OH⁻ to give "
      "0.050 mol water.",
      ["n(H⁺) = 2 × 0.050 × 0.50 = 0.050 mol; n(OH⁻) = 0.050 mol", "q = 0.050 × 57 100 = 2855 J",
       "ΔT = 2855 / (100 × 4.2) = 6.80 K"],
      why_others_wrong="3.40 K treats H₂SO₄ as monobasic (0.025 mol water); 13.60 K counts 0.10 mol water; 0.68 K "
                       "slips a factor of 10 in the heat capacity of the solution.",
      ncert=f"{LAB}, thermochemistry: enthalpy of neutralisation", seconds=75),

    Q(T_PR, "Qualitative salt analysis", "Advanced", "statement_pair",
      *sp("Zn²⁺ and Mn²⁺ are precipitated in group IV as their sulphides when H₂S is passed through the ammoniacal "
          "solution.", True,
          "Ni²⁺ and Co²⁺ are precipitated in group III as hydroxides by NH₄OH in the presence of NH₄Cl.", False),
      "Group III and group IV cations",
      "Group III (Fe³⁺, Al³⁺, Cr³⁺) is precipitated as hydroxides by NH₄OH/NH₄Cl. Ni²⁺, Co²⁺, Mn²⁺ and Zn²⁺ stay in "
      "solution and are precipitated in group IV as sulphides by H₂S in ammoniacal medium (NiS and CoS black, MnS "
      "buff, ZnS white). Statement I is true and Statement II false.",
      ["Group IV: Ni²⁺, Co²⁺, Mn²⁺, Zn²⁺ as sulphides", "Ni²⁺ and Co²⁺ are not group III → Statement II false"],
      ncert=f"{LAB}, systematic analysis of cations: groups III and IV", seconds=40),

    Q(T_PR, "Qualitative salt analysis", "Advanced", "multi_statement",
      *ms("Which of the following statements about systematic analysis of cations are correct?",
          [("Group I cations are precipitated as chlorides by dilute HCl.", True),
           ("Lead chloride is appreciably soluble in water, so Pb²⁺ may also appear in group II.", True),
           ("Group V cations are precipitated as carbonates by ammonium carbonate in the presence of NH₄OH.", True),
           ("Mg²⁺ is precipitated in group V as magnesium carbonate.", False),
           ("The test for NH₄⁺ is performed on the original salt, because ammonium salts are added as reagents during "
            "the analysis.", True)],
          [["a", "b", "c"], ["b", "c", "d", "e"], ["a", "c", "d"]], "A"),
      "Principles of group separation",
      "Pb²⁺ is precipitated incompletely as PbCl₂ in group I and the rest as PbS in group II. Group V (Ba²⁺, Sr²⁺, "
      "Ca²⁺) comes down as carbonates; Mg²⁺ is not precipitated in the presence of NH₄Cl and is tested in group VI. "
      "Because NH₄Cl, NH₄OH and (NH₄)₂CO₃ are added during the scheme, NH₄⁺ (zero group) must be tested in the "
      "original salt.",
      ["(a) true", "(b) true", "(c) true", "(d) false: Mg²⁺ is group VI", "(e) true"],
      ncert=f"{LAB}, systematic qualitative analysis of cations", seconds=55),
]

# ---------------------------------------------------------------- package checks and output
PLAN = {T_CC: (4, 6, 5), T_PU: (2, 3, 2), T_GO: (6, 8, 6), T_HC: (5, 6, 5), T_HX: (4, 5, 4), T_OX: (6, 8, 6),
        T_NI: (4, 5, 4), T_BM: (4, 5, 4), T_PR: (3, 4, 3)}
TOTAL = LAST - FIRST + 1

if __name__ == "__main__":
    assert len(QUESTIONS) == TOTAL == 127, len(QUESTIONS)
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
    doc = {"schema_version": "1.0", "batch_id": "BATCH_008", "created_at": TODAY,
           "notes": "Package CHE_008_p2: 127 original Chemistry questions (coordination compounds, organic chemistry, "
                    "biomolecules, practical chemistry). Numerical answers recomputed by "
                    "tools/batch_008/CHE_008_p2.py.",
           "stimuli": [], "questions": QUESTIONS}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {OUT}: {dict(Counter(x['difficulty'] for x in QUESTIONS))}, keys {dict(sorted(keys.items()))}, "
          f"formats {dict(fmts)}")
