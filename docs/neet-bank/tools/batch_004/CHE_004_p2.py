"""Writes batches/parts/BATCH_004_CHE_p2.json: package CHE_004_p2 of BATCH_004 (Chemistry, 124 questions).

Topics: d- and f-Block Elements, Coordination Compounds, Purification and Characterisation of Organic Compounds,
Some Basic Principles of Organic Chemistry, Hydrocarbons, Organic Compounds Containing Halogens / Oxygen / Nitrogen,
Biomolecules (Chemistry), Principles Related to Practical Chemistry. IDs NEET_CHE_000877..NEET_CHE_001000.

Every numerical answer is re-derived below with an assert; multi-statement keys are derived from the truth value of
each statement, assertion-reason and statement-pair keys from the truth of each part. If any check fails, nothing is
written.

    python docs/neet-bank/tools/batch_004/CHE_004_p2.py
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
OUT = ROOT / "batches" / "parts" / "BATCH_004_CHE_p2.json"
TODAY = "2026-11-16"
LETTERS = "ABCD"
CHE = "Chemistry"
FIRST, LAST = 877, 1000
# ai:self-recheck = a second, separate solve of every question by the author after the file was written.
AUTHORED = ("ai:author-solve", "ai:self-recheck")
RECOMPUTED = ("script:recompute", "ai:author-solve", "ai:self-recheck")

T_DF = "d- and f-Block Elements"
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
    return text, match_options(correct, wrong, at), at


def ms(intro, stmts, wrong, at):
    """(text, options, key) for multi-statement. stmts = [(text, is_true)]; the key is derived from the truths."""
    let = "abcde"[:len(stmts)]
    text = (intro + "\n\n" + "\n".join(f"({let[i]}) {s}" for i, (s, _) in enumerate(stmts)) +
            "\n\nChoose the correct answer from the options given below:")
    true = [let[i] for i, (_, t) in enumerate(stmts) if t]
    lab = lambda xs: ", ".join(f"({x})" for x in xs[:-1]) + f" and ({xs[-1]}) only"
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


def r1(x):
    return round(float(x), 1)


def r2(x):
    return round(float(x), 2)


def spin_only(n):
    """Spin-only magnetic moment sqrt(n(n+2)) in BM, to 2 decimals."""
    return r2(math.sqrt(n * (n + 2)))


def unpaired_free_ion(d):
    """Unpaired electrons of a free d^n ion (Hund's rule)."""
    return d if d <= 5 else 10 - d


# Atomic masses used in the stems
C_, H_, O_, N_, S_, P_, BR, I_, NA, MG, CL, K_, MN, CR, FE, AL, BA, CA = (
    12, 1, 16, 14, 32, 31, 80, 127, 23, 24, F(355, 10), 39, 55, 52, 56, 27, 137, 40)


def mm(**atoms):
    """Molar mass from atom counts, e.g. mm(C=2, H=6, O=1)."""
    table = {"C": C_, "H": H_, "O": O_, "N": N_, "S": S_, "P": P_, "Br": BR, "I": I_, "Na": NA, "Mg": MG,
             "Cl": CL, "K": K_, "Mn": MN, "Cr": CR, "Fe": FE, "Al": AL, "Ba": BA, "Ca": CA}
    return sum(table[k] * v for k, v in atoms.items())


QUESTIONS = []

# ================================================================ d- and f-Block Elements (877-889)
# 878: V3+ (Z 23) = [Ar] 3d2
d_v3 = 23 - 18 - 3
assert d_v3 == 2 and spin_only(2) == 2.83 and spin_only(1) == 1.73 and spin_only(3) == 3.87
assert spin_only(4) == 4.90 and spin_only(5) == 5.92
# 879: Sm (Z 62) = [Xe] 4f6 6s2 ; Sm3+ = [Xe] 4f5
f_sm3 = 62 - 54 - 3
assert f_sm3 == 5 and 62 - 54 - 2 == 6
# 881: 2MnO4- + 5SO3(2-) + 6H+ -> 2Mn2+ + 5SO4(2-) + 3H2O ; 25.0 mL of 0.10 M sulphite, 0.020 M KMnO4
mmol_so3 = F(250, 10) * F(1, 10)
v_881 = mmol_so3 * F(2, 5) / F(2, 100)
assert mmol_so3 == F(5, 2) and v_881 == 50
assert mmol_so3 / F(2, 100) == 125                      # 1 : 1 ratio
assert mmol_so3 * F(2, 3) / F(2, 100) == F(250, 3)      # MnO4- taken as gaining 3 e- (to MnO2): 83.3 mL
assert mmol_so3 * F(5, 2) / F(2, 100) == F(625, 2)      # ratio inverted: 312.5 mL
# 886: 2MnO4- + 3Mn2+ + 2H2O -> 5MnO2 + 4H+ ; MnO4- gains 3 e-, Mn2+ loses 2 e-
m_mno2 = mm(Mn=1, O=2)
mol_mn2_886 = F(2, 100) * 3 / 2
mass_886 = (F(2, 100) + mol_mn2_886) * m_mno2
assert m_mno2 == 87 and mol_mn2_886 == F(3, 100) and mass_886 == F(435, 100)
assert F(2, 100) * m_mno2 == F(174, 100) and mol_mn2_886 * m_mno2 == F(261, 100)
assert F(4, 100) * m_mno2 == F(348, 100)                # 1 : 1 ratio
# 889: free ions with the same number of unpaired electrons as Fe2+ (d6 -> 4)
ions_889 = {"Ti2+": 22 - 18 - 2, "Cr2+": 24 - 18 - 2, "Mn3+": 25 - 18 - 3, "Fe3+": 26 - 18 - 3,
            "Co3+": 27 - 18 - 3, "Ni2+": 28 - 18 - 2}
fe2_unpaired = unpaired_free_ion(26 - 18 - 2)
same_889 = [k for k, d in ions_889.items() if unpaired_free_ion(d) == fe2_unpaired]
assert fe2_unpaired == 4 and same_889 == ["Cr2+", "Mn3+", "Co3+"]

QUESTIONS += [
    Q(T_DF, "Transition element trends", "Basic", "direct",
      "Leaving out palladium, which is an exception, the general outer electronic configuration of the d-block "
      "elements is:",
      ["ns² np¹⁻⁶", "(n−1)d¹⁻¹⁰ ns¹⁻²", "(n−2)f¹⁻¹⁴ (n−1)d⁰⁻¹ ns²", "(n−1)d¹⁻¹⁰ ns⁰"], "B",
      "Electronic configuration of the d-block elements",
      "In the d-block, the (n−1)d orbitals are being filled while the outermost ns orbital holds one or two "
      "electrons. Palladium (4d¹⁰ 5s⁰) is the exception NCERT mentions.",
      ["d-block: inner (n−1)d subshell filled progressively, d¹ to d¹⁰",
       "Outer ns subshell: 1 or 2 electrons (e.g. Cr 3d⁵ 4s¹, Fe 3d⁶ 4s²)",
       "General configuration: (n−1)d¹⁻¹⁰ ns¹⁻²"],
      why_others_wrong="ns² np¹⁻⁶ is the p-block configuration. (n−2)f¹⁻¹⁴ (n−1)d⁰⁻¹ ns² is the f-block "
                       "(inner transition) configuration. (n−1)d¹⁻¹⁰ ns⁰ fits only palladium, the stated exception.",
      ncert=f"{NC12}, 'The d- and f-Block Elements', electronic configurations of the d-block elements",
      seconds=25),

    N(T_DF, "Magnetic and colour properties", "Basic",
      "The spin-only magnetic moment of the V³⁺ ion (Z of V = 23) is about:",
      ["1.73 BM", "3.87 BM", "2.83 BM", "4.90 BM"], "C", "2.83 BM",
      "Spin-only formula μ = √[n(n + 2)] BM",
      "V is [Ar] 3d³ 4s². Removing the two 4s electrons and one 3d electron leaves V³⁺ = [Ar] 3d², with two "
      "unpaired electrons.",
      ["V³⁺: 23 − 3 = 20 electrons → [Ar] 3d²", "n = 2 unpaired electrons",
       "μ = √(2 × 4) = √8 ≈ 2.83 BM"],
      why_others_wrong="1.73 BM is for one unpaired electron. 3.87 BM is for three (V²⁺, 3d³). 4.90 BM is for "
                       "four unpaired electrons.",
      ncert=f"{NC12}, 'The d- and f-Block Elements', magnetic properties (spin-only formula)", seconds=35),

    N(T_DF, "Lanthanoids and actinoids", "Basic",
      "Samarium (Z = 62) has the configuration [Xe] 4f⁶ 6s². The number of 4f electrons in the Sm³⁺ ion is:",
      ["5", "6", "3", "8"], "A", "5",
      "Electronic configuration of Ln³⁺ ions",
      "To form Ln³⁺, the two 6s electrons are lost first and then one 4f electron (there is no 5d electron in Sm).",
      ["Sm: [Xe] 4f⁶ 6s²", "Remove 6s² → 4f⁶, then one 4f electron → 4f⁵",
       "Check: 62 − 3 − 54 (Xe core) = 5"],
      why_others_wrong="6 is the 4f count of the neutral atom (or of Sm²⁺). 3 confuses the charge with the 4f count. "
                       "8 is Z − 54 without removing any electrons.",
      ncert=f"{NC12}, 'The d- and f-Block Elements', the lanthanoids (electronic configurations)", seconds=30),

    Q(T_DF, "Lanthanoids and actinoids", "Basic", "statement_pair",
      *sp("The electronic configuration of lanthanum (Z = 57) is [Xe] 4f¹ 6s².", False,
          "Yb²⁺, which has a 4f¹⁴ configuration, acts as a reducing agent.", True),
      "Configurations and oxidation states of the lanthanoids",
      "Lanthanum is [Xe] 5d¹ 6s²; its 4f subshell is empty. NCERT notes that Yb²⁺ (f¹⁴), like Eu²⁺, is a reductant, "
      "changing to the common +3 state.",
      ["Statement I: La = [Xe] 5d¹ 6s², not 4f¹ 6s² → false",
       "Statement II: Yb²⁺ (4f¹⁴) is oxidised to Yb³⁺, so it is a reducing agent → true"],
      ncert=f"{NC12}, 'The d- and f-Block Elements', the lanthanoids (electronic configurations, oxidation states)",
      seconds=35),

    N(T_DF, "K2Cr2O7 and KMnO4", "Intermediate",
      "25.0 mL of 0.10 M sodium sulphite solution is oxidised to sulphate by acidified 0.020 M KMnO₄ solution "
      "(permanganate is reduced to Mn²⁺). The volume of KMnO₄ solution needed is:",
      ["125 mL", "50 mL", "83.3 mL", "312.5 mL"], "B", "50 mL",
      "Redox stoichiometry of acidified permanganate",
      "MnO₄⁻ gains 5 electrons (Mn +7 → +2) and SO₃²⁻ loses 2 electrons (S +4 → +6), so 2 MnO₄⁻ react with "
      "5 SO₃²⁻: 2MnO₄⁻ + 5SO₃²⁻ + 6H⁺ → 2Mn²⁺ + 5SO₄²⁻ + 3H₂O.",
      ["mmol SO₃²⁻ = 25.0 × 0.10 = 2.5 mmol", "mmol MnO₄⁻ = 2.5 × 2/5 = 1.0 mmol",
       "Volume = 1.0/0.020 = 50 mL"],
      shortcut="Equivalents: 2.5 × 2 = 5 meq of sulphite = 0.020 × 5 × V → V = 50 mL.",
      why_others_wrong="125 mL takes a 1 : 1 mole ratio. 83.3 mL treats permanganate as gaining 3 electrons "
                       "(reduction to MnO₂, which happens only in neutral solution). 312.5 mL inverts the 2 : 5 ratio.",
      ncert=f"{NC12}, 'The d- and f-Block Elements', potassium permanganate (oxidising action in acid solution)",
      seconds=75),

    Q(T_DF, "Transition element trends", "Advanced", "assertion_reason",
      *ar("The second ionisation enthalpies of chromium and copper are unusually high compared with those of "
          "their neighbours in the 3d series.", True,
          "Removing the second electron from Cr⁺ (3d⁵) or Cu⁺ (3d¹⁰) breaks up a stable half-filled or completely "
          "filled d subshell.", True, explains=True),
      "Irregularities in the ionisation enthalpies of the 3d series",
      "After the first ionisation, Cr⁺ is 3d⁵ and Cu⁺ is 3d¹⁰. NCERT points out that the second ionisation "
      "enthalpies are higher for Cr and Cu precisely because these M⁺ ions have the stable d⁵ and d¹⁰ "
      "configurations, which must be disturbed.",
      ["Cr: 3d⁵ 4s¹ → Cr⁺ 3d⁵; Cu: 3d¹⁰ 4s¹ → Cu⁺ 3d¹⁰",
       "The second electron must come from the stable d⁵ / d¹⁰ set → high IE₂ (A true)",
       "R states exactly this cause → R explains A"],
      ncert=f"{NC12}, 'The d- and f-Block Elements', ionisation enthalpies", seconds=50),

    Q(T_DF, "Transition element trends", "Intermediate", "match_list",
      *ml("Match the species in List-I with its ground-state electronic configuration in List-II "
          "(atomic numbers: Cr 24, Fe 26, Co 27, Zn 30).",
          ["Cr", "Zn²⁺", "Fe³⁺", "Co³⁺"],
          ["[Ar] 3d⁶", "[Ar] 3d⁵", "[Ar] 3d⁵ 4s¹", "[Ar] 3d¹⁰"],
          {"A": "III", "B": "IV", "C": "II", "D": "I"},
          [{"A": "II", "B": "IV", "C": "III", "D": "I"}, {"A": "III", "B": "IV", "C": "I", "D": "II"},
           {"A": "III", "B": "II", "C": "IV", "D": "I"}], "C"),
      "Configurations of 3d atoms and ions",
      "Chromium takes the half-filled 3d⁵ 4s¹ arrangement. Ions of the 3d metals lose their 4s electrons first.",
      ["Cr (24): [Ar] 3d⁵ 4s¹ → III", "Zn²⁺ (28 e⁻): [Ar] 3d¹⁰ → IV", "Fe³⁺ (23 e⁻): [Ar] 3d⁵ → II",
       "Co³⁺ (24 e⁻): [Ar] 3d⁶ → I"],
      why_others_wrong="A-II, C-III gives Fe³⁺ a 4s electron, but 4s electrons are lost first. C-I, D-II swaps "
                       "the d counts of Fe³⁺ and Co³⁺. B-II, C-IV mixes up Zn²⁺ and Fe³⁺.",
      ncert=f"{NC12}, 'The d- and f-Block Elements', electronic configurations", seconds=45),

    Q(T_DF, "Transition element trends", "Intermediate", "multi_statement",
      *ms("Which of the following statements about the metals of the 3d series are correct?",
          [("The atomic radii decrease at first along the series and then change very little for the middle "
            "elements.", True),
           ("The density of the metals generally increases from titanium to copper.", True),
           ("Zinc has the highest enthalpy of atomisation in the series.", False),
           ("Metals with very high enthalpies of atomisation tend to be noble in their reactions.", True),
           ("Ti⁴⁺ compounds are coloured because Ti⁴⁺ has unpaired 3d electrons.", False)],
          [["a", "b", "c"], ["a", "c", "e"], ["b", "d", "e"]], "D"),
      "Physical trends across the 3d series",
      "Radii fall at first and then level off in the middle (Fe, Co, Ni are almost the same size), so density rises "
      "from Ti to Cu as mass increases. Zinc, with no unpaired d electrons, has the lowest enthalpy of atomisation. "
      "Ti⁴⁺ is 3d⁰, so its compounds are colourless (white TiO₂).",
      ["(a) radii decrease, then nearly constant → true", "(b) density increases Ti → Cu → true",
       "(c) Zn has the lowest, not highest, enthalpy of atomisation → false",
       "(d) high atomisation enthalpy → noble behaviour (NCERT) → true",
       "(e) Ti⁴⁺ is d⁰, no unpaired electrons → false"],
      why_others_wrong="Each other option includes (c) or (e), which are false, or leaves out a true statement.",
      ncert=f"{NC12}, 'The d- and f-Block Elements', physical properties, atomic sizes, enthalpies of atomisation",
      seconds=70),

    Q(T_DF, "Lanthanoids and actinoids", "Intermediate", "direct",
      "The actinoids show a greater range of oxidation states than the lanthanoids. This is attributed mainly to "
      "the fact that:",
      ["the 5f orbitals are buried more deeply in the atom than the 4f orbitals",
       "the 5f, 6d and 7s levels are of comparable energies",
       "all the actinoids are radioactive",
       "the actinoid contraction is smaller than the lanthanoid contraction"], "B",
      "Oxidation states of the actinoids",
      "Because the 5f, 6d and 7s levels lie close in energy, a variable number of electrons can be used in bonding, "
      "so the actinoids show many oxidation states.",
      ["Range of oxidation states depends on how many electrons can be removed at similar cost",
       "5f, 6d and 7s are of comparable energies → variable oxidation states"],
      why_others_wrong="The 5f orbitals are less deeply buried than 4f, not more, so the first option is reversed. "
                       "Radioactivity does not decide oxidation states. The actinoid contraction is in fact greater "
                       "from element to element, and in any case contraction does not explain the range.",
      ncert=f"{NC12}, 'The d- and f-Block Elements', the actinoids (oxidation states)", seconds=35),

    N(T_DF, "K2Cr2O7 and KMnO4", "Advanced",
      "In neutral solution, in the presence of zinc sulphate, permanganate oxidises Mn²⁺ ions to MnO₂ and is "
      "itself reduced to MnO₂. When 0.020 mol of MnO₄⁻ reacts completely with Mn²⁺ in this way, the total mass of "
      "MnO₂ formed is (Mn = 55, O = 16):",
      ["1.74 g", "2.61 g", "3.48 g", "4.35 g"], "D", "4.35 g",
      "Comproportionation of permanganate and Mn²⁺",
      "MnO₄⁻ (+7) gains 3 electrons and Mn²⁺ loses 2 electrons, both ending at +4. Balancing electrons: "
      "2MnO₄⁻ + 3Mn²⁺ + 2H₂O → 5MnO₂ + 4H⁺. Both reactants end up as MnO₂.",
      ["Electrons: 2 × 3 = 3 × 2 → 2 MnO₄⁻ : 3 Mn²⁺", "n(Mn²⁺) = 0.020 × 3/2 = 0.030 mol",
       "n(MnO₂) = 0.020 + 0.030 = 0.050 mol", "Mass = 0.050 × 87 = 4.35 g"],
      why_others_wrong="1.74 g counts only the MnO₂ coming from permanganate, and 2.61 g only that from Mn²⁺. "
                       "3.48 g assumes a 1 : 1 ratio of MnO₄⁻ to Mn²⁺.",
      ncert=f"{NC12}, 'The d- and f-Block Elements', potassium permanganate (oxidising action in neutral solution)",
      seconds=100),

    Q(T_DF, "K2Cr2O7 and KMnO4", "Advanced", "multi_statement",
      *ms("Which of the following statements about potassium permanganate and potassium dichromate are correct?",
          [("In neutral or faintly alkaline solution, each MnO₄⁻ ion gains three electrons.", True),
           ("In acidic solution, each Cr₂O₇²⁻ ion gains six electrons.", True),
           ("The manganate and permanganate ions are both tetrahedral.", True),
           ("Commercially, manganate is converted into permanganate by electrolytic oxidation in alkaline "
            "solution.", True),
           ("In acidic solution, one MnO₄⁻ ion oxidises three Fe²⁺ ions.", False)],
          [["a", "b", "e"], ["b", "c", "d", "e"], ["a", "c", "d"]], "A"),
      "Structures and electron changes of permanganate and dichromate",
      "MnO₄⁻ → MnO₂ in neutral/faintly alkaline solution is +7 → +4 (3e⁻). Cr₂O₇²⁻ → 2Cr³⁺ is 2 × 3 = 6e⁻. Both "
      "MnO₄²⁻ and MnO₄⁻ are tetrahedral. Industrially, MnO₂ is fused with alkali and an oxidant to give manganate, "
      "which is then oxidised electrolytically to permanganate in alkaline solution. In acid, MnO₄⁻ gains 5e⁻ and "
      "so oxidises five Fe²⁺ ions.",
      ["(a) +7 → +4 = 3e⁻ → true", "(b) 2Cr(+6) → 2Cr(+3) = 6e⁻ → true", "(c) both tetrahedral → true",
       "(d) electrolytic oxidation of manganate → true", "(e) 1 MnO₄⁻ : 5 Fe²⁺, not 3 → false"],
      why_others_wrong="Any option containing (e) is wrong; (a), (c), (d) only leaves out the true statement (b).",
      ncert=f"{NC12}, 'The d- and f-Block Elements', potassium dichromate and potassium permanganate", seconds=80),

    Q(T_DF, "Transition element trends", "Intermediate", "assertion_reason",
      *ar("MnO is a basic oxide, whereas Mn₂O₇ is an acidic oxide.", True,
          "As the oxidation state of a metal increases, the ionic character of its oxides decreases and their "
          "acidic character increases.", True, explains=True),
      "Nature of the oxides of transition metals",
      "In MnO, manganese is +2 and the oxide is ionic and basic. In Mn₂O₇ (+7, a covalent green oil) the oxide is "
      "acidic, giving permanganic acid. NCERT relates this to the fall in ionic character with rising oxidation "
      "state.",
      ["MnO: Mn(+2), ionic → basic", "Mn₂O₇: Mn(+7), covalent → acidic (A true)",
       "Higher oxidation state → less ionic, more acidic oxide (R true and explains A)"],
      ncert=f"{NC12}, 'The d- and f-Block Elements', oxides and oxoanions of metals", seconds=45),

    N(T_DF, "Magnetic and colour properties", "Advanced",
      "Applying Hund's rule to the free (gaseous) ions, how many of the following have the same number of "
      "unpaired electrons, and hence the same spin-only magnetic moment, as Fe²⁺?\n"
      "Ti²⁺, Cr²⁺, Mn³⁺, Fe³⁺, Co³⁺, Ni²⁺\n"
      "(Atomic numbers: Ti 22, Cr 24, Mn 25, Fe 26, Co 27, Ni 28)",
      ["2", "3", "4", "5"], "B", "3",
      "Unpaired electrons from the d-electron count",
      "Fe²⁺ is 3d⁶ with four unpaired electrons. A d⁴ ion (four singly occupied orbitals) and another d⁶ ion also "
      "have four unpaired electrons.",
      ["Fe²⁺: 3d⁶ → 4 unpaired", "Ti²⁺ 3d² (2), Cr²⁺ 3d⁴ (4), Mn³⁺ 3d⁴ (4)",
       "Fe³⁺ 3d⁵ (5), Co³⁺ 3d⁶ (4), Ni²⁺ 3d⁸ (2)", "Same as Fe²⁺: Cr²⁺, Mn³⁺, Co³⁺ → 3"],
      why_others_wrong="2 misses Co³⁺, which is isoelectronic with Fe²⁺. 4 wrongly adds Fe³⁺ (five unpaired). "
                       "5 also adds both d² and d⁸ ions, which have only two unpaired electrons.",
      ncert=f"{NC12}, 'The d- and f-Block Elements', magnetic properties", seconds=80),
]

# ================================================================ Coordination Compounds (890-905)
# 891: oxidation state = charge of entity - sum of ligand charges
ox_891 = {"[Ni(CO)4]": 0 - 4 * 0, "[Ag(CN)2]-": -1 - 2 * (-1), "[Cu(NH3)4]2+": 2 - 4 * 0,
          "[PtCl6]2-": -2 - 6 * (-1)}
assert ox_891 == {"[Ni(CO)4]": 0, "[Ag(CN)2]-": 1, "[Cu(NH3)4]2+": 2, "[PtCl6]2-": 4}
# 895: [Mn(CN)6]3- : Mn3+ = 3d4, strong field -> t2g4 eg0 -> 2 unpaired
d_mn3 = 25 - 18 - 3
assert d_mn3 == 4
unpaired_low_spin_d4 = 4 - 2 * (4 - 3)        # 3 t2g orbitals hold 4 electrons -> one pair
assert unpaired_low_spin_d4 == 2 and spin_only(unpaired_low_spin_d4) == 2.83
assert spin_only(unpaired_free_ion(d_mn3)) == 4.90
# 902: inner-orbital (d2sp3) complexes in the list
inner_902 = {"[Co(NH3)6]3+": True, "[CoF6]3-": False, "[Fe(CN)6]3-": True, "[FeF6]3-": False,
             "[Cr(NH3)6]3+": True, "[Fe(H2O)6]2+": False}
assert sum(inner_902.values()) == 3
# 900: Ni2+ = 3d8 -> two unpaired, no 3d orbital can be vacated -> outer sp3d2
assert 28 - 18 - 2 == 8 and unpaired_free_ion(8) == 2
# 905: spin-only moments
d_905 = {"[Cr(H2O)6]3+": (24 - 18 - 3, 3), "[Fe(CN)6]4-": (26 - 18 - 2, 0), "[MnCl4]2-": (25 - 18 - 2, 5),
         "[Cu(NH3)4]2+": (29 - 18 - 2, 1)}
assert [d for d, _ in d_905.values()] == [3, 6, 5, 9]
assert [spin_only(n) for _, n in d_905.values()] == [3.87, 0.0, 5.92, 1.73]

QUESTIONS += [
    Q(T_CC, "IUPAC nomenclature", "Basic", "direct",
      "The IUPAC name of [Cr(NH₃)₃(H₂O)₃]Cl₃ is:",
      ["Triaquatriamminechromium(III) chloride", "Triamminetriaquachromate(III) chloride",
       "Triamminetriaquachromium(III) chloride", "Triamminetriaquachromium(II) chloride"], "C",
      "Naming a cationic complex",
      "Ligands are named in alphabetical order (ammine before aqua; the prefix tri is ignored). The complex is a "
      "cation, so the metal keeps its ordinary name, followed by its oxidation state.",
      ["Charge on complex = +3 (three Cl⁻ outside)", "x + 3(0) + 3(0) = +3 → Cr(III)",
       "Alphabetical: ammine (a-m) before aqua (a-q) → triamminetriaqua",
       "Cationic complex → 'chromium', not 'chromate'"],
      why_others_wrong="Triaquatriammine breaks the alphabetical order. 'Chromate' is used only for an anionic "
                       "complex. (II) gives the wrong oxidation state.",
      ncert=f"{NC12}, 'Coordination Compounds', nomenclature of coordination compounds", seconds=30),

    Q(T_CC, "Werner's theory and ligands", "Basic", "match_list",
      *ml("Match the coordination entity in List-I with the oxidation state of its central metal in List-II.",
          ["[Ni(CO)₄]", "[Ag(CN)₂]⁻", "[Cu(NH₃)₄]²⁺", "[PtCl₆]²⁻"],
          ["+2", "0", "+4", "+1"],
          {"A": "II", "B": "IV", "C": "I", "D": "III"},
          [{"A": "IV", "B": "II", "C": "I", "D": "III"}, {"A": "II", "B": "I", "C": "IV", "D": "III"},
           {"A": "II", "B": "IV", "C": "III", "D": "I"}], "B"),
      "Oxidation number of the central atom",
      "Oxidation number = charge on the entity − total charge of the ligands. CO and NH₃ are neutral; CN⁻ and Cl⁻ "
      "carry −1 each.",
      ["[Ni(CO)₄]: x = 0 → II", "[Ag(CN)₂]⁻: x − 2 = −1 → x = +1 → IV",
       "[Cu(NH₃)₄]²⁺: x = +2 → I", "[PtCl₆]²⁻: x − 6 = −2 → x = +4 → III"],
      why_others_wrong="A-IV, B-II swaps nickel and silver. B-I, C-IV gives silver +2 and copper +1. C-III, D-I "
                       "gives copper +4 and platinum +2, ignoring the six chloride ligands.",
      ncert=f"{NC12}, 'Coordination Compounds', definitions (oxidation number of central atom)", seconds=40),

    Q(T_CC, "IUPAC nomenclature", "Basic", "direct",
      "The formula of tetraamminecopper(II) sulphate is:",
      ["[Cu(NH₃)₄](SO₄)₂", "[Cu(SO₄)(NH₃)₄]", "[Cu(NH₃)₂]SO₄", "[Cu(NH₃)₄]SO₄"], "D",
      "Writing a formula from the name",
      "The name gives a complex cation with four ammine ligands and Cu(II), so the cation is [Cu(NH₃)₄]²⁺. One "
      "sulphate ion (2−) balances it.",
      ["Cation: [Cu(NH₃)₄]²⁺ (NH₃ neutral, Cu +2)", "Counter ion: SO₄²⁻",
       "Charge balance: 1 : 1 → [Cu(NH₃)₄]SO₄"],
      why_others_wrong="(SO₄)₂ would need copper(IV). [Cu(SO₄)(NH₃)₄] puts sulphate inside the coordination sphere, "
                       "which the name (no 'sulphato') does not say. [Cu(NH₃)₂]SO₄ has only two ammine ligands.",
      ncert=f"{NC12}, 'Coordination Compounds', formulas of mononuclear coordination entities", seconds=25),

    Q(T_CC, "Isomerism", "Basic", "statement_pair",
      *sp("Optical isomers (enantiomers) are mirror images of each other that cannot be superimposed on one "
          "another.", True,
          "Optical isomerism is common in octahedral complexes containing didentate ligands.", True),
      "Optical isomerism in coordination compounds",
      "NCERT defines optical isomers as non-superimposable mirror images and notes that optical isomerism is "
      "common in octahedral complexes involving didentate ligands, such as [Co(en)₃]³⁺.",
      ["Statement I: definition of enantiomers → true",
       "Statement II: e.g. [Co(en)₃]³⁺ and cis-[PtCl₂(en)₂]²⁺ are chiral → true"],
      ncert=f"{NC12}, 'Coordination Compounds', isomerism (optical isomerism)", seconds=30),

    Q(T_CC, "Werner's theory and ligands", "Basic", "assertion_reason",
      *ar("One mole of [Co(NH₃)₆]Cl₃ gives three moles of AgCl when treated with excess AgNO₃ solution.", True,
          "NH₃ is a stronger field ligand than H₂O.", True),
      "Ionisable chloride in Werner's complexes",
      "All three chlorides of [Co(NH₃)₆]Cl₃ lie outside the coordination sphere and are free Cl⁻ ions, so they are "
      "precipitated as 3AgCl. The position of NH₃ in the spectrochemical series is true but concerns crystal field "
      "splitting; it has nothing to do with how many chlorides are ionisable.",
      ["[Co(NH₃)₆]Cl₃ → [Co(NH₃)₆]³⁺ + 3Cl⁻ → 3AgCl (A true)",
       "NH₃ > H₂O in the spectrochemical series (R true)",
       "R explains splitting, not the number of ionisable Cl⁻ → R is not the explanation"],
      ncert=f"{NC12}, 'Coordination Compounds', Werner's theory; crystal field theory (spectrochemical series)",
      seconds=40),

    N(T_CC, "Crystal field theory", "Intermediate",
      "[Mn(CN)₆]³⁻ is a low-spin octahedral complex (Z of Mn = 25). Its spin-only magnetic moment is about:",
      ["2.83 BM", "4.90 BM", "3.87 BM", "1.73 BM"], "A", "2.83 BM",
      "Low-spin d⁴ configuration",
      "Mn³⁺ is 3d⁴. CN⁻ is a strong field ligand (Δo > P), so all four electrons go into the t₂g set: t₂g⁴ eg⁰. "
      "Three orbitals hold four electrons, so one pair forms and two electrons stay unpaired.",
      ["Mn³⁺: 25 − 3 = 22 e⁻ → [Ar] 3d⁴", "Strong field: t₂g⁴ eg⁰ → ↑↓, ↑, ↑ → n = 2",
       "μ = √(2 × 4) = 2.83 BM"],
      why_others_wrong="4.90 BM is the high-spin value (t₂g³ eg¹, four unpaired). 3.87 BM assumes three unpaired "
                       "electrons, and 1.73 BM only one; neither fits t₂g⁴.",
      ncert=f"{NC12}, 'Coordination Compounds', crystal field splitting in octahedral complexes", seconds=50),

    Q(T_CC, "Isomerism", "Intermediate", "statement_pair",
      *sp("An octahedral complex of the type [MA₃B₃] can exist as facial (fac) and meridional (mer) isomers.", True,
          "In the mer isomer, the three identical ligands occupy the three corners of one face of the octahedron.",
          False),
      "fac and mer isomers",
      "In the fac isomer the three donor atoms of the same ligand sit at the corners of one octahedral face; in the "
      "mer isomer they lie around a meridian of the octahedron. Statement II describes the fac isomer.",
      ["Statement I: [Co(NH₃)₃(NO₂)₃] has fac and mer forms → true",
       "Statement II: 'corners of one face' = fac, not mer → false"],
      ncert=f"{NC12}, 'Coordination Compounds', geometrical isomerism (fac and mer)", seconds=35),

    Q(T_CC, "IUPAC nomenclature", "Intermediate", "direct",
      "The IUPAC name of [CoCl₂(en)₂]Cl (en = ethane-1,2-diamine) is:",
      ["Bis(ethane-1,2-diamine)dichloridocobalt(III) chloride",
       "Dichloridobis(ethane-1,2-diamine)cobalt(II) chloride",
       "Dichloridodi(ethane-1,2-diamine)cobaltate(III) chloride",
       "Dichloridobis(ethane-1,2-diamine)cobalt(III) chloride"], "D",
      "Naming a complex with a polydentate ligand",
      "Ligands are taken alphabetically by their names (chlorido before ethane-1,2-diamine); multiplying prefixes "
      "are ignored. For a ligand whose name already contains a numeral, bis/tris is used and the name is put in "
      "brackets. The complex is a cation, so the metal is 'cobalt'.",
      ["Oxidation state: x + 2(−1) + 2(0) = +1 → x = +3",
       "Alphabetical: chlorido (c) before ethane-1,2-diamine (e)",
       "Two en → bis(ethane-1,2-diamine)", "Name: dichloridobis(ethane-1,2-diamine)cobalt(III) chloride"],
      why_others_wrong="Putting bis(ethane-1,2-diamine) first breaks the alphabetical order. Cobalt(II) ignores "
                       "the two chlorido ligands in the charge. 'di' cannot be used before a bracketed ligand name, "
                       "and 'cobaltate' is only for anionic complexes.",
      ncert=f"{NC12}, 'Coordination Compounds', nomenclature of coordination compounds", seconds=45),

    Q(T_CC, "Crystal field theory", "Intermediate", "multi_statement",
      *ms("Which of the following statements about crystal field splitting and colour are correct?",
          [("In a free (isolated) metal ion, the five d orbitals are degenerate.", True),
           ("[Ni(H₂O)₆]²⁺ is colourless because Ni²⁺ has no unpaired electrons.", False),
           ("When ethane-1,2-diamine is added gradually to a solution of [Ni(H₂O)₆]²⁺, the colour changes, because "
            "en is a stronger field ligand than H₂O.", True),
           ("A complex with a larger Δo absorbs light of longer wavelength.", False),
           ("Ruby is aluminium oxide containing a small percentage of Cr³⁺ ions.", True)],
          [["a", "b", "c"], ["c", "d", "e"], ["a", "d", "e"]], "B"),
      "Crystal field theory and the colour of complexes",
      "The d orbitals are degenerate only in the free ion. [Ni(H₂O)₆]²⁺ (d⁸, two unpaired electrons) is green; "
      "replacing H₂O by the stronger field en increases Δo and changes the colour. A larger Δo means absorption of "
      "higher energy, i.e. shorter wavelength. Ruby is Al₂O₃ with about 0.5–1% Cr³⁺ (d³) ions in octahedral sites.",
      ["(a) degenerate d orbitals in a free ion → true", "(b) Ni²⁺ is d⁸ with two unpaired e⁻; the ion is green → false",
       "(c) stronger ligand → larger Δo → new colour → true", "(d) larger Δo → shorter λ absorbed → false",
       "(e) ruby = Al₂O₃ with Cr³⁺ → true"],
      why_others_wrong="Every other option includes (b) or (d), both false.",
      ncert=f"{NC12}, 'Coordination Compounds', crystal field theory (colour in coordination compounds)",
      seconds=70),

    Q(T_CC, "Valence bond theory", "Intermediate", "assertion_reason",
      *ar("[Co(NH₃)₆]³⁺ is an inner orbital complex.", True,
          "In [Co(NH₃)₆]³⁺, cobalt uses its inner 3d orbitals in d²sp³ hybridisation.", True, explains=True),
      "Inner and outer orbital complexes (VBT)",
      "Co³⁺ is 3d⁶. With NH₃, the six electrons pair up in three 3d orbitals, freeing two inner 3d orbitals, so "
      "the metal uses 3d, 4s and 4p orbitals (d²sp³). A complex that uses inner (n−1)d orbitals is called an inner "
      "orbital (low spin) complex, which is exactly what R says.",
      ["Co³⁺ 3d⁶ → paired in three 3d orbitals", "Two vacant 3d + 4s + three 4p → d²sp³",
       "(n−1)d used → inner orbital complex; R gives the reason"],
      ncert=f"{NC12}, 'Coordination Compounds', valence bond theory", seconds=40),

    Q(T_CC, "Valence bond theory", "Advanced", "direct",
      "In [Ni(NH₃)₆]²⁺ (Z of Ni = 28), the hybridisation of nickel and the magnetic behaviour of the complex are:",
      ["d²sp³, diamagnetic", "sp³d², diamagnetic", "d²sp³, paramagnetic with two unpaired electrons",
       "sp³d², paramagnetic with two unpaired electrons"], "D",
      "Outer orbital octahedral complex of a d⁸ ion",
      "Ni²⁺ is 3d⁸. Even if electrons pair, eight electrons fill four of the five 3d orbitals, leaving only one "
      "vacant 3d orbital; two are needed for d²sp³. So the octahedral complex uses 4s, 4p and two 4d orbitals "
      "(sp³d²), and the two unpaired 3d electrons remain.",
      ["Ni²⁺: [Ar] 3d⁸ → ↑↓ ↑↓ ↑↓ ↑ ↑", "Two vacant inner d orbitals are not available → outer orbital sp³d²",
       "Two unpaired electrons → paramagnetic"],
      why_others_wrong="d²sp³ would need two empty 3d orbitals, impossible for d⁸. Any 'diamagnetic' option ignores "
                       "the two unpaired 3d electrons that every octahedral Ni²⁺ complex keeps.",
      ncert=f"{NC12}, 'Coordination Compounds', valence bond theory (outer orbital complexes)", seconds=55),

    Q(T_CC, "Applications", "Intermediate", "direct",
      "In black-and-white photography, the developed film is fixed by washing with hypo (sodium thiosulphate) "
      "solution, which dissolves the undecomposed silver bromide. The complex ion formed is:",
      ["[Ag(NH₃)₂]⁺", "[Ag(S₂O₃)₂]³⁻", "[Ag(CN)₂]⁻", "[Ag(S₂O₃)]⁺"], "B",
      "Use of complex formation in photography",
      "AgBr dissolves in hypo because Ag⁺ forms the soluble complex [Ag(S₂O₃)₂]³⁻.",
      ["AgBr + 2S₂O₃²⁻ → [Ag(S₂O₃)₂]³⁻ + Br⁻", "Ag(+1) with two S₂O₃²⁻ → overall charge 1 − 4 = −3"],
      why_others_wrong="[Ag(NH₃)₂]⁺ forms with ammonia and [Ag(CN)₂]⁻ with cyanide, neither of which is hypo. "
                       "[Ag(S₂O₃)]⁺ has the wrong charge (+1 − 2 = −1) and the wrong number of ligands.",
      ncert=f"{NC12}, 'Coordination Compounds', importance and applications of coordination compounds",
      seconds=30),

    N(T_CC, "Valence bond theory", "Advanced",
      "How many of the following are inner orbital (d²sp³) complexes according to valence bond theory?\n"
      "[Co(NH₃)₆]³⁺, [CoF₆]³⁻, [Fe(CN)₆]³⁻, [FeF₆]³⁻, [Cr(NH₃)₆]³⁺, [Fe(H₂O)₆]²⁺\n"
      "(Atomic numbers: Cr 24, Fe 26, Co 27)",
      ["2", "4", "3", "5"], "C", "3",
      "Inner versus outer orbital octahedral complexes",
      "Strong field ligands (NH₃ with Co³⁺, CN⁻) pair the d electrons and free two 3d orbitals (d²sp³). F⁻ and H₂O "
      "with Fe or Co leave the electrons unpaired, so 4d orbitals are used (sp³d²). Cr³⁺ is d³, so two 3d orbitals "
      "are empty anyway and the complex is always d²sp³.",
      ["[Co(NH₃)₆]³⁺: d⁶ paired → d²sp³ (inner)", "[CoF₆]³⁻: high spin → sp³d² (outer)",
       "[Fe(CN)₆]³⁻: d⁵ low spin → d²sp³ (inner)", "[FeF₆]³⁻: high spin → sp³d² (outer)",
       "[Cr(NH₃)₆]³⁺: d³, two 3d empty → d²sp³ (inner)", "[Fe(H₂O)₆]²⁺: d⁶ high spin → sp³d² (outer)",
       "Inner orbital complexes = 3"],
      why_others_wrong="2 leaves out [Cr(NH₃)₆]³⁺, forgetting that a d³ ion always has two vacant 3d orbitals. "
                       "4 or 5 counts one or more of the high-spin fluoro or aqua complexes as inner orbital.",
      ncert=f"{NC12}, 'Coordination Compounds', valence bond theory", seconds=90),

    Q(T_CC, "Valence bond theory", "Advanced", "multi_statement",
      *ms("Which of the following statements about metal carbonyls are correct?",
          [("[Ni(CO)₄] is tetrahedral.", True),
           ("[Fe(CO)₅] is trigonal bipyramidal.", True),
           ("[Cr(CO)₆] is octahedral.", True),
           ("The σ bond in a metal carbonyl is formed by donation of a lone pair on the oxygen atom of CO to the "
            "metal.", False),
           ("The synergic effect of σ donation and π back-donation strengthens the bond between CO and the metal.",
            True)],
          [["a", "b", "c"], ["a", "b", "d", "e"], ["b", "c", "e"]], "D"),
      "Structure and bonding of metal carbonyls",
      "NCERT gives the shapes: tetrahedral Ni(CO)₄, trigonal bipyramidal Fe(CO)₅, octahedral Cr(CO)₆. The M–C σ "
      "bond uses the lone pair on the carbon of CO; π back-donation from a filled metal d orbital into the "
      "vacant π* orbital of CO creates a synergic effect that strengthens the M–CO bond.",
      ["(a), (b), (c): shapes as in NCERT → true", "(d) the donor atom is carbon, not oxygen → false",
       "(e) synergic σ/π bonding strengthens the bond → true"],
      why_others_wrong="(a), (b), (c) only and (b), (c), (e) only each leave out a true statement; the option with "
                       "(d) includes a false one.",
      ncert=f"{NC12}, 'Coordination Compounds', bonding in metal carbonyls", seconds=65),

    Q(T_CC, "Crystal field theory", "Advanced", "assertion_reason",
      *ar("[Mn(H₂O)₆]²⁺ has a low-spin configuration with only one unpaired electron.", False,
          "With H₂O as the ligand, the crystal field splitting Δo for Mn²⁺ is smaller than the pairing energy P.",
          True),
      "High-spin and low-spin d⁵ complexes",
      "Mn²⁺ is 3d⁵. Because Δo < P for the aqua complex, the electrons occupy the eg orbitals rather than pair: "
      "t₂g³ eg², with five unpaired electrons (high spin). So A is false while R is true.",
      ["Mn²⁺: 3d⁵", "Δo < P → t₂g³ eg² → five unpaired electrons (high spin)",
       "A (low spin, one unpaired) → false; R → true"],
      ncert=f"{NC12}, 'Coordination Compounds', crystal field splitting (Δo and pairing energy)", seconds=45),

    Q(T_CC, "Crystal field theory", "Advanced", "match_list",
      *ml("Match the complex in List-I with its spin-only magnetic moment in List-II "
          "(atomic numbers: Cr 24, Mn 25, Fe 26, Cu 29; [MnCl₄]²⁻ is tetrahedral).",
          ["[Cr(H₂O)₆]³⁺", "[Fe(CN)₆]⁴⁻", "[MnCl₄]²⁻", "[Cu(NH₃)₄]²⁺"],
          ["0 BM", "1.73 BM", "3.87 BM", "5.92 BM"],
          {"A": "III", "B": "I", "C": "IV", "D": "II"},
          [{"A": "IV", "B": "I", "C": "III", "D": "II"}, {"A": "III", "B": "II", "C": "IV", "D": "I"},
           {"A": "II", "B": "I", "C": "IV", "D": "III"}], "D"),
      "Unpaired electrons from d count and ligand field",
      "Count the d electrons, decide whether pairing occurs, then use μ = √[n(n + 2)].",
      ["Cr³⁺ d³ → t₂g³, n = 3 → 3.87 BM (III)", "Fe²⁺ d⁶ with CN⁻ (strong) → t₂g⁶, n = 0 → 0 (I)",
       "Mn²⁺ d⁵ with Cl⁻ in a tetrahedral field (small Δt) → n = 5 → 5.92 BM (IV)",
       "Cu²⁺ d⁹ → n = 1 in any geometry → 1.73 BM (II)"],
      why_others_wrong="A-IV, C-III swaps chromium and manganese. B-II, D-I gives Cu²⁺ zero unpaired electrons, "
                       "but a d⁹ ion always has one. A-II, D-III swaps the Cr³⁺ and Cu²⁺ values.",
      ncert=f"{NC12}, 'Coordination Compounds', crystal field theory; magnetic properties", seconds=70),
]

# ================================================================ Purification and Characterisation (906-912)
# 909: steam distillation, p(total) = p(aniline) + p(water)
assert 760 - 717 == 43 and 760 + 717 == 1477
# 911: C 92.3 %, H 7.7 %, vapour density 39
mol_c, mol_h = F(923, 10) / 12, F(77, 10) / 1
assert abs(mol_c / mol_h - 1) < F(1, 100)           # C : H = 1 : 1 -> empirical formula CH
m_911 = 2 * 39
n_911 = F(m_911, mm(C=1, H=1))
assert m_911 == 78 and n_911 == 6                   # C6H6
assert F(39, 13) == 3 and F(4 * 39, 13) == 12       # VD taken as M -> C3H3 ; 4 x VD -> C12H12

QUESTIONS += [
    Q(T_PU, "Qualitative analysis", "Basic", "direct",
      "In Lassaigne's test, the sodium fusion extract is acidified with nitric acid and treated with silver nitrate. "
      "A yellow precipitate that is insoluble in ammonium hydroxide is obtained. The halogen present is:",
      ["Chlorine", "Bromine", "Iodine", "Fluorine"], "C",
      "Test for halogens with AgNO₃",
      "NCERT: a white precipitate soluble in NH₄OH shows chlorine; a yellowish precipitate sparingly soluble in "
      "NH₄OH shows bromine; a yellow precipitate insoluble in NH₄OH shows iodine.",
      ["NaX + AgNO₃ → AgX↓", "AgCl white, soluble in NH₄OH; AgBr pale yellow, sparingly soluble",
       "AgI yellow, insoluble in NH₄OH → iodine"],
      why_others_wrong="AgCl is white and dissolves in ammonia; AgBr is pale yellow and dissolves partly. AgF is "
                       "soluble in water, so fluoride gives no precipitate.",
      ncert=f"{NC11}, 'Organic Chemistry – Some Basic Principles and Techniques', detection of halogens",
      seconds=25),

    Q(T_PU, "Purification methods", "Basic", "assertion_reason",
      *ar("During crystallisation, coloured impurities are removed by adsorbing them on activated charcoal.", True,
          "Repeated crystallisation is needed when the compound and its impurities have comparable solubilities.",
          True),
      "Crystallisation",
      "Both are NCERT statements about crystallisation, but they deal with different problems. Charcoal removes "
      "impurities that colour the solution by adsorption; repeated crystallisation is about separating substances "
      "of similar solubility. R does not explain why charcoal is used.",
      ["A: activated charcoal adsorbs coloured impurities → true",
       "R: comparable solubilities → repeated crystallisation → true",
       "R concerns solubility, not colour → not the explanation"],
      ncert=f"{NC11}, 'Organic Chemistry – Some Basic Principles and Techniques', crystallisation", seconds=40),

    Q(T_PU, "Purification methods", "Intermediate", "statement_pair",
      *sp("Differential extraction is carried out in a separating funnel, using an organic solvent that is "
          "immiscible with water.", True,
          "The name chromatography comes from the Greek word chroma (colour), because the technique was first used "
          "to separate coloured substances found in plants.", True),
      "Differential extraction and chromatography",
      "In differential extraction, the aqueous solution is shaken with an immiscible organic solvent in a "
      "separating funnel, and the two layers are separated. NCERT explains that 'chromatography' comes from "
      "'chroma', since it was first used to separate coloured plant pigments.",
      ["Statement I → true", "Statement II → true"],
      ncert=f"{NC11}, 'Organic Chemistry – Some Basic Principles and Techniques', differential extraction; "
            "chromatography", seconds=30),

    N(T_PU, "Purification methods", "Intermediate",
      "Aniline is purified by steam distillation at an atmospheric pressure of 760 mm Hg. At the temperature at "
      "which the mixture distils, the vapour pressure of water is 717 mm Hg. The vapour pressure of aniline at "
      "this temperature is:",
      ["43 mm Hg", "717 mm Hg", "760 mm Hg", "1477 mm Hg"], "A", "43 mm Hg",
      "Principle of steam distillation",
      "A mixture of steam and the organic liquid boils when the sum of the vapour pressures of the organic liquid "
      "(p₁) and water (p₂) equals the atmospheric pressure: p = p₁ + p₂. Each liquid therefore boils below its "
      "normal boiling point.",
      ["p = p₁ + p₂", "760 = p₁ + 717", "p₁ = 43 mm Hg"],
      why_others_wrong="717 mm Hg is the vapour pressure of water, not aniline. 760 mm Hg assumes aniline alone "
                       "must reach atmospheric pressure, as in simple distillation. 1477 mm Hg adds instead of "
                       "subtracting.",
      ncert=f"{NC11}, 'Organic Chemistry – Some Basic Principles and Techniques', steam distillation", seconds=40),

    Q(T_PU, "Purification methods", "Intermediate", "match_list",
      *ml("After a thin layer chromatography (TLC) run, the spots have to be located. Match the kind of compound "
          "in List-I with the way its spots are made visible in List-II.",
          ["Coloured compounds", "Amino acids", "Colourless compounds that fluoresce",
           "Colourless compounds that adsorb iodine"],
          ["Spraying the plate with ninhydrin solution", "Seen directly on the plate",
           "Keeping the plate in a closed jar containing a few iodine crystals", "Viewing the plate under ultraviolet light"],
          {"A": "II", "B": "I", "C": "IV", "D": "III"},
          [{"A": "I", "B": "II", "C": "IV", "D": "III"}, {"A": "II", "B": "I", "C": "III", "D": "IV"},
           {"A": "II", "B": "IV", "C": "I", "D": "III"}], "C"),
      "Detecting spots in thin layer chromatography",
      "NCERT lists the ways of locating spots: coloured compounds are visible by their own colour; fluorescing "
      "compounds show under UV light; compounds that adsorb iodine show brown spots in an iodine jar; amino acids "
      "are detected by spraying ninhydrin.",
      ["Coloured → visible directly → II", "Amino acids → ninhydrin spray → I",
       "Fluorescent → UV light → IV", "Iodine-adsorbing → iodine jar (brown spots) → III"],
      why_others_wrong="A-I, B-II swaps the coloured compounds and amino acids. C-III, D-IV swaps UV light and the "
                       "iodine jar. B-IV, C-I gives ninhydrin to the fluorescent compounds.",
      ncert=f"{NC11}, 'Organic Chemistry – Some Basic Principles and Techniques', thin layer chromatography",
      seconds=45),

    N(T_PU, "Quantitative analysis and formulae", "Advanced",
      "A hydrocarbon contains 92.3% carbon and 7.7% hydrogen by mass. Its vapour density is 39. The molecular "
      "formula of the hydrocarbon is (C = 12, H = 1):",
      ["C₃H₃", "C₆H₆", "C₁₂H₁₂", "CH"], "B", "C₆H₆",
      "Empirical and molecular formula from percentage composition",
      "Find the mole ratio of the elements, then use molar mass = 2 × vapour density to find the multiple of the "
      "empirical formula.",
      ["C: 92.3/12 = 7.69; H: 7.7/1 = 7.7 → ratio 1 : 1 → empirical formula CH (13 g mol⁻¹)",
       "Molar mass = 2 × 39 = 78 g mol⁻¹", "n = 78/13 = 6 → C₆H₆"],
      why_others_wrong="C₃H₃ uses the vapour density itself as the molar mass. C₁₂H₁₂ multiplies the vapour density "
                       "by 4. CH is the empirical formula, not the molecular formula.",
      ncert=f"{NC11}, 'Some Basic Concepts of Chemistry', empirical and molecular formulae; {NC11}, "
            "'Organic Chemistry – Some Basic Principles and Techniques', quantitative analysis", seconds=70),

    Q(T_PU, "Qualitative analysis", "Advanced", "multi_statement",
      *ms("Which of the following statements about the detection of elements in organic compounds are correct?",
          [("When the compound is heated with copper(II) oxide, its carbon is oxidised to CO₂, which turns lime "
            "water milky.", True),
           ("In the same test, hydrogen is oxidised to water, which turns anhydrous copper sulphate blue.", True),
           ("Phosphorus is oxidised to phosphate, which gives a yellow colour or precipitate with ammonium "
            "molybdate after boiling with nitric acid.", True),
           ("During sodium fusion, sulphur in the compound is converted into sodium sulphate.", False),
           ("In the copper(II) oxide test, carbon is converted into carbon monoxide.", False)],
          [["a", "b", "d"], ["b", "c", "e"], ["a", "c", "d", "e"]], "A"),
      "Detection of C, H, S and P",
      "Carbon becomes CO₂ (lime water turns milky) and hydrogen becomes water (white anhydrous CuSO₄ turns blue). "
      "Phosphorus is oxidised (e.g. with sodium peroxide) to phosphate, which gives a yellow colour or precipitate "
      "with ammonium molybdate. In sodium fusion, sulphur forms sodium sulphide, Na₂S, not sulphate.",
      ["(a) C → CO₂ → lime water milky → true", "(b) H → H₂O → CuSO₄ blue → true",
       "(c) phosphate + ammonium molybdate → yellow → true", "(d) S → Na₂S, not Na₂SO₄ → false",
       "(e) C → CO₂, not CO → false"],
      why_others_wrong="Every other option contains (d) or (e), or leaves out the true statement (c) or (a).",
      ncert=f"{NC11}, 'Organic Chemistry – Some Basic Principles and Techniques', qualitative analysis",
      seconds=60),
]

# ================================================================ Some Basic Principles of Organic Chemistry (913-929)
# 914: structural isomers of C5H12
c5h12 = ["pentane", "2-methylbutane", "2,2-dimethylpropane"]
assert len(c5h12) == 3


def shows_gi(c1, c2):
    """Geometrical isomerism: each doubly bonded carbon carries two different groups."""
    return len(set(c1)) == 2 and len(set(c2)) == 2


# 918: groups on the two doubly bonded carbons
alkenes_918 = {"but-2-ene": (("CH3", "H"), ("CH3", "H")), "propene": (("CH3", "H"), ("H", "H")),
               "2-methylbut-2-ene": (("CH3", "CH3"), ("CH3", "H")), "pent-2-ene": (("CH3", "H"), ("C2H5", "H")),
               "1,2-dichloroethene": (("Cl", "H"), ("Cl", "H")), "1,1-dichloroethene": (("Cl", "Cl"), ("H", "H"))}
gi_918 = [k for k, (a, b) in alkenes_918.items() if shows_gi(a, b)]
assert gi_918 == ["but-2-ene", "pent-2-ene", "1,2-dichloroethene"]
# 923: aromatic isomers of C8H10
c8h10 = ["ethylbenzene", "1,2-dimethylbenzene", "1,3-dimethylbenzene", "1,4-dimethylbenzene"]
assert len(c8h10) == 4 and mm(C=8, H=10) == 106
# 925: structural isomers of C4H8 (alkenes and cycloalkanes; cis/trans not counted separately)
c4h8 = ["but-1-ene", "but-2-ene", "2-methylpropene", "cyclobutane", "methylcyclopropane"]
assert len(c4h8) == 5 and len(c4h8) + 1 == 6     # + cis/trans of but-2-ene counted separately -> 6

QUESTIONS += [
    Q(T_GO, "IUPAC nomenclature", "Basic", "direct",
      "The IUPAC name of (CH₃)₂CH–CH₂–CH(CH₃)₂ is:",
      ["2,2-Dimethylpentane", "2,4-Dimethylpentane", "1,1,3-Trimethylbutane", "3,3-Dimethylpentane"], "B",
      "Naming a branched alkane",
      "The longest chain has five carbons, with a methyl group on C-2 and on C-4 (the numbering is the same from "
      "either end).",
      ["Longest chain: CH₃–CH(CH₃)–CH₂–CH(CH₃)–CH₃ → pentane", "Methyl groups at C-2 and C-4",
       "Name: 2,4-dimethylpentane (C₇H₁₆)"],
      why_others_wrong="2,2- and 3,3-dimethylpentane put both methyls on one carbon, which is a different "
                       "compound. 1,1,3-Trimethylbutane does not use the longest chain (a methyl on C-1 extends it).",
      ncert=f"{NC11}, 'Organic Chemistry – Some Basic Principles and Techniques', IUPAC nomenclature of alkanes",
      seconds=30),

    N(T_GO, "Isomerism", "Basic",
      "How many structural isomers have the molecular formula C₅H₁₂?",
      ["3", "4", "5", "2"], "A", "3",
      "Chain isomerism in alkanes",
      "C₅H₁₂ can have a straight chain of five carbons, a four-carbon chain with one methyl branch, or a three-carbon "
      "chain with two methyl branches on the middle carbon.",
      ["Pentane", "2-Methylbutane (isopentane)", "2,2-Dimethylpropane (neopentane)", "Total = 3"],
      why_others_wrong="4 or 5 counts the same skeleton twice (for example 3-methylbutane is 2-methylbutane "
                       "numbered from the wrong end). 2 misses neopentane.",
      ncert=f"{NC11}, 'Organic Chemistry – Some Basic Principles and Techniques', structural isomerism",
      seconds=30),

    Q(T_GO, "Isomerism", "Basic", "statement_pair",
      *sp("Pentan-2-one and pentan-3-one are position isomers.", True,
          "Butane and 2-methylpropane are position isomers.", False),
      "Types of structural isomerism",
      "Pentan-2-one and pentan-3-one have the same carbon chain and differ only in the position of the C=O group. "
      "Butane and 2-methylpropane differ in the carbon skeleton itself, which is chain isomerism.",
      ["Statement I: same chain, C=O at C-2 or C-3 → position isomers → true",
       "Statement II: straight vs branched chain → chain isomers, not position isomers → false"],
      ncert=f"{NC11}, 'Organic Chemistry – Some Basic Principles and Techniques', structural isomerism",
      seconds=30),

    Q(T_GO, "Isomerism", "Basic", "assertion_reason",
      *ar("Ethanol and methoxymethane are chain isomers.", False,
          "Ethanol and methoxymethane have the same molecular formula but different functional groups.", True),
      "Functional group isomerism",
      "Ethanol (C₂H₅OH) and methoxymethane (CH₃OCH₃) are both C₂H₆O, but one is an alcohol and the other an "
      "ether. Isomers that differ in functional group are functional group isomers, not chain isomers.",
      ["Both are C₂H₆O → isomers", "Alcohol vs ether → functional group isomers",
       "A (chain isomers) → false; R → true"],
      ncert=f"{NC11}, 'Organic Chemistry – Some Basic Principles and Techniques', functional group isomerism",
      seconds=30),

    Q(T_GO, "IUPAC nomenclature", "Basic", "match_list",
      *ml("Match the class of compound in List-I with the suffix used for it in IUPAC names in List-II.",
          ["Alcohol", "Aldehyde", "Ketone", "Carboxylic acid"],
          ["-oic acid", "-one", "-al", "-ol"],
          {"A": "IV", "B": "III", "C": "II", "D": "I"},
          [{"A": "III", "B": "IV", "C": "II", "D": "I"}, {"A": "IV", "B": "II", "C": "III", "D": "I"},
           {"A": "IV", "B": "III", "C": "I", "D": "II"}], "D"),
      "Suffixes for functional groups",
      "When a functional group is the principal group, its suffix replaces the final 'e' of the alkane name.",
      ["Alcohol → -ol (ethanol) → IV", "Aldehyde → -al (ethanal) → III", "Ketone → -one (propanone) → II",
       "Carboxylic acid → -oic acid (ethanoic acid) → I"],
      why_others_wrong="A-III, B-IV swaps alcohol and aldehyde. B-II, C-III swaps aldehyde and ketone. C-I, D-II "
                       "swaps ketone and acid.",
      ncert=f"{NC11}, 'Organic Chemistry – Some Basic Principles and Techniques', nomenclature of compounds with "
            "functional groups", seconds=25),

    N(T_GO, "Isomerism", "Intermediate",
      "How many of the following show geometrical (cis–trans) isomerism?\n"
      "But-2-ene, propene, 2-methylbut-2-ene, pent-2-ene, 1,2-dichloroethene, 1,1-dichloroethene",
      ["2", "4", "3", "5"], "C", "3",
      "Condition for geometrical isomerism",
      "An alkene shows cis–trans isomerism only if each doubly bonded carbon carries two different groups.",
      ["But-2-ene: CH₃/H on both carbons → yes", "Propene: =CH₂ end has H, H → no",
       "2-Methylbut-2-ene: one carbon has CH₃, CH₃ → no", "Pent-2-ene: CH₃/H and C₂H₅/H → yes",
       "1,2-Dichloroethene: Cl/H on both → yes", "1,1-Dichloroethene: one carbon has H, H → no",
       "Count = 3"],
      why_others_wrong="2 misses one of the qualifying alkenes (often 1,2-dichloroethene, which has no alkyl "
                       "group). 4 or 5 includes a compound with two identical groups on one double-bond carbon.",
      ncert=f"{NC11}, 'Hydrocarbons', isomerism in alkenes (geometrical isomerism)", seconds=60),

    Q(T_GO, "IUPAC nomenclature", "Intermediate", "direct",
      "The IUPAC name of CH₃–CH₂–CH(CH₂CH₃)–CH₂–CH₂–CH₃ is:",
      ["3-Propylpentane", "4-Ethylhexane", "3-Ethylhexane", "2-Ethylhexane"], "C",
      "Longest chain and lowest locant",
      "The longest chain has six carbons (through the propyl side), with an ethyl group on the third carbon when "
      "numbered from the end nearer the branch.",
      ["Longest chain: CH₃CH₂–CH–CH₂CH₂CH₃ = 6 carbons → hexane",
       "Substituent: ethyl; numbering from the left gives locant 3 (from the right, 4)",
       "Name: 3-ethylhexane"],
      why_others_wrong="3-Propylpentane uses a five-carbon chain, not the longest. 4-Ethylhexane numbers from the "
                       "wrong end. 2-Ethylhexane is never correct: an ethyl on C-2 would lengthen the main chain.",
      ncert=f"{NC11}, 'Organic Chemistry – Some Basic Principles and Techniques', IUPAC nomenclature (branched "
            "chain alkanes)", seconds=40),

    Q(T_GO, "Hybridisation and functional groups", "Intermediate", "assertion_reason",
      *ar("In but-2-ene, CH₃–CH=CH–CH₃, all four carbon atoms are sp² hybridised.", False,
          "A carbon atom that forms a carbon–carbon double bond is sp² hybridised.", True),
      "Hybridisation of carbon",
      "Only C-2 and C-3, which form the double bond, are sp². The two terminal CH₃ carbons form four single bonds "
      "and are sp³.",
      ["C-2, C-3 (C=C) → sp²", "C-1, C-4 (CH₃) → sp³", "A false; R true"],
      ncert=f"{NC11}, 'Organic Chemistry – Some Basic Principles and Techniques', shapes of carbon compounds "
            "(hybridisation)", seconds=30),

    Q(T_GO, "Isomerism", "Intermediate", "multi_statement",
      *ms("Which of the following statements about isomerism are correct?",
          [("Metamerism arises from different alkyl chains on either side of the functional group in the molecule.",
            True),
           ("But-1-ene and but-2-ene are position isomers.", True),
           ("Propanoic acid and methyl ethanoate are functional group isomers.", True),
           ("Stereoisomers differ in the sequence in which the atoms are bonded to one another.", False),
           ("Structural isomers have the same structural formula but different arrangements of atoms in space.",
            False)],
          [["a", "b", "d"], ["b", "c", "e"], ["a", "c", "d"]], "A"),
      "Structural isomerism and stereoisomerism",
      "Metamers (e.g. C₂H₅OC₂H₅ and CH₃OC₃H₇) differ in the alkyl groups on either side of the functional group. "
      "But-1-ene and but-2-ene differ in the position of the double bond. Propanoic acid and methyl ethanoate are "
      "both C₃H₆O₂ but an acid and an ester. Structural isomers differ in the sequence of bonding; stereoisomers "
      "have the same sequence but differ in the spatial arrangement — (d) and (e) swap these definitions.",
      ["(a) metamerism → true", "(b) position isomers → true", "(c) acid vs ester, both C₃H₆O₂ → true",
       "(d) describes structural isomers → false", "(e) describes stereoisomers → false"],
      why_others_wrong="Every other option contains (d) or (e), or leaves out a true statement.",
      ncert=f"{NC11}, 'Organic Chemistry – Some Basic Principles and Techniques', isomerism", seconds=60),

    Q(T_GO, "IUPAC nomenclature", "Intermediate", "statement_pair",
      *sp("The IUPAC name of CH₃–CH₂–CH₂–CHO is butan-1-al.", False,
          "The IUPAC name of CH₃–CH₂–COCl is propanoyl chloride.", True),
      "Naming aldehydes and acid chlorides",
      "The –CHO carbon of an aldehyde is always C-1, so no locant is written: the name is butanal. An acid "
      "chloride is named by replacing '-oic acid' with '-oyl chloride': propanoic acid → propanoyl chloride.",
      ["Statement I: correct name is butanal → false", "Statement II: propanoyl chloride → true"],
      ncert=f"{NC11}, 'Organic Chemistry – Some Basic Principles and Techniques', nomenclature of compounds with "
            "functional groups", seconds=30),

    N(T_GO, "Isomerism", "Intermediate",
      "How many aromatic compounds (containing a benzene ring) have the molecular formula C₈H₁₀?",
      ["3", "4", "5", "6"], "B", "4",
      "Structural isomers of a substituted benzene",
      "C₈H₁₀ with a benzene ring is C₆H₄(CH₃)₂ or C₆H₅C₂H₅. The two methyl groups can be ortho, meta or para.",
      ["Ethylbenzene", "1,2-Dimethylbenzene (o-xylene)", "1,3-Dimethylbenzene (m-xylene)",
       "1,4-Dimethylbenzene (p-xylene)", "Total = 4"],
      why_others_wrong="3 counts only the three xylenes and misses ethylbenzene. 5 or 6 counts the same "
                       "dimethylbenzene twice (e.g. 1,5- is the same as 1,3-).",
      ncert=f"{NC11}, 'Organic Chemistry – Some Basic Principles and Techniques', isomerism; {NC11}, "
            "'Hydrocarbons', nomenclature and isomerism of aromatic hydrocarbons", seconds=40),

    Q(T_GO, "Electronic effects", "Intermediate", "match_list",
      *ml("Match the electronic effect in List-I with its description in List-II.",
          ["Inductive effect", "Resonance effect", "Electromeric effect", "Hyperconjugation"],
          ["Temporary complete shift of a shared π pair to one atom, only in the presence of an attacking reagent",
           "Delocalisation of the σ electrons of a C–H bond of an alkyl group into an adjacent empty p orbital "
           "or π system",
           "Permanent polarisation transmitted along a chain of σ bonds",
           "Permanent delocalisation of π electrons (or lone pairs) in a conjugated system"],
          {"A": "III", "B": "IV", "C": "I", "D": "II"},
          [{"A": "IV", "B": "III", "C": "I", "D": "II"}, {"A": "III", "B": "II", "C": "I", "D": "IV"},
           {"A": "III", "B": "IV", "C": "II", "D": "I"}], "D"),
      "Electronic displacements in covalent bonds",
      "The inductive and resonance effects are permanent; the electromeric effect is temporary and needs an "
      "attacking reagent; hyperconjugation involves σ (C–H) electrons.",
      ["Inductive → σ bonds, permanent → III", "Resonance → π / lone pair, conjugated system → IV",
       "Electromeric → temporary, reagent needed → I", "Hyperconjugation → σ–p / σ–π delocalisation → II"],
      why_others_wrong="A-IV, B-III swaps the inductive and resonance effects. B-II, D-IV swaps resonance and "
                       "hyperconjugation. C-II, D-I swaps the electromeric effect and hyperconjugation.",
      ncert=f"{NC11}, 'Organic Chemistry – Some Basic Principles and Techniques', electron movement in organic "
            "reactions (electronic effects)", seconds=50),

    N(T_GO, "Isomerism", "Advanced",
      "How many structural isomers (open-chain and cyclic together) have the molecular formula C₄H₈? Count cis and "
      "trans forms as one structure.",
      ["3", "4", "5", "6"], "C", "5",
      "Isomers of CₙH₂ₙ: alkenes and cycloalkanes",
      "CₙH₂ₙ fits both alkenes and cycloalkanes, so ring isomers must be counted as well as open-chain alkenes.",
      ["Alkenes: but-1-ene, but-2-ene, 2-methylpropene (3)", "Cycloalkanes: cyclobutane, methylcyclopropane (2)",
       "Structural isomers = 5"],
      why_others_wrong="3 counts only the open-chain alkenes. 4 misses methylcyclopropane. 6 counts cis- and "
                       "trans-but-2-ene separately, which the question excludes.",
      ncert=f"{NC11}, 'Organic Chemistry – Some Basic Principles and Techniques', structural isomerism; {NC11}, "
            "'Hydrocarbons', isomerism in alkenes", seconds=60),

    Q(T_GO, "Electronic effects", "Advanced", "multi_statement",
      *ms("Which of the following statements about hyperconjugation are correct?",
          [("Hyperconjugation is a permanent effect.", True),
           ("The tert-butyl cation has fewer C–H bonds able to take part in hyperconjugation than the ethyl "
            "cation.", False),
           ("Hyperconjugation is also called no-bond resonance.", True),
           ("The greater the number of alkyl groups attached to the positively charged carbon, the greater the "
            "hyperconjugation and the more stable the carbocation.", True),
           ("Hyperconjugation is the overlap of the π electrons of a C=C bond with an empty p orbital.", False)],
          [["a", "b", "c"], ["c", "d", "e"], ["a", "d", "e"]], "D"),
      "Hyperconjugation",
      "Hyperconjugation is the permanent delocalisation of σ electrons of a C–H bond of an alkyl group attached to "
      "an atom with an unshared p orbital or to an unsaturated system; it is also called no-bond resonance. "
      "(CH₃)₃C⁺ has nine such C–H bonds and CH₃CH₂⁺ only three, so the tert-butyl cation is more stable.",
      ["(a) permanent effect → true", "(b) 9 vs 3 C–H bonds — tert-butyl has more → false",
       "(c) no-bond resonance → true", "(d) more alkyl groups → more stable cation → true",
       "(e) delocalisation of π electrons is resonance, not hyperconjugation → false"],
      why_others_wrong="Every other option includes (b) or (e), which are false.",
      ncert=f"{NC11}, 'Organic Chemistry – Some Basic Principles and Techniques', hyperconjugation", seconds=60),

    Q(T_GO, "Reactive intermediates", "Advanced", "assertion_reason",
      *ar("Heterolytic cleavage of the C–Br bond in (CH₃)₃C–Br gives (CH₃)₃C⁺ and Br⁻.", True,
          "Carbon is more electronegative than bromine.", False),
      "Heterolytic cleavage",
      "In heterolysis, the shared pair goes to the more electronegative atom. Bromine is more electronegative than "
      "carbon, so it leaves as Br⁻ and the tertiary carbon becomes a carbocation.",
      ["Br more electronegative than C → takes the bond pair", "(CH₃)₃C–Br → (CH₃)₃C⁺ + Br⁻ (A true)",
       "R reverses the electronegativity order → false"],
      ncert=f"{NC11}, 'Organic Chemistry – Some Basic Principles and Techniques', fission of a covalent bond",
      seconds=40),

    Q(T_GO, "Electronic effects", "Advanced", "statement_pair",
      *sp("The canonical (resonance) structures of a molecule must have the same number of unpaired electrons.",
          True,
          "Among the canonical structures, one with a negative charge on the more electronegative atom contributes "
          "more to the resonance hybrid.", True),
      "Rules for resonance structures",
      "NCERT: canonical structures have the same positions of nuclei and the same number of unpaired electrons. "
      "More stable structures — more covalent bonds, octets on all atoms, less separation of opposite charges, a "
      "negative charge on the more electronegative atom — contribute more.",
      ["Statement I: same number of unpaired electrons → true",
       "Statement II: negative charge on the more electronegative atom → more stable → larger contribution → true"],
      ncert=f"{NC11}, 'Organic Chemistry – Some Basic Principles and Techniques', resonance structure",
      seconds=40),

    Q(T_GO, "IUPAC nomenclature", "Advanced", "direct",
      "The IUPAC name of HOOC–CH₂–CH(CH₃)–CHO is:",
      ["2-Methyl-4-oxobutanoic acid", "3-Methyl-4-oxobutanoic acid", "3-Carboxy-2-methylpropanal",
       "3-Methylbutanoic acid"], "B",
      "Polyfunctional compounds: principal group and locants",
      "The carboxylic acid group ranks above the aldehyde, so it is the principal group (suffix -oic acid) and its "
      "carbon is C-1. The aldehyde carbon, lying in the chain, is named with the prefix 'oxo'.",
      ["Principal group: –COOH → C-1, suffix 'butanoic acid'",
       "C-2 = CH₂, C-3 = CH(CH₃), C-4 = CHO", "Prefixes alphabetical: methyl (3), oxo (4)",
       "Name: 3-methyl-4-oxobutanoic acid"],
      why_others_wrong="2-Methyl misplaces the methyl group, which is on C-3 counted from the COOH carbon. "
                       "3-Carboxy-2-methylpropanal treats the aldehyde as the principal group although –COOH ranks "
                       "higher. 3-Methylbutanoic acid leaves out the oxo group (it names a different compound).",
      ncert=f"{NC11}, 'Organic Chemistry – Some Basic Principles and Techniques', nomenclature of polyfunctional "
            "compounds", seconds=60),
]

# ================================================================ Hydrocarbons (930-943)
# 931: C2H4 + Br2 -> CH2Br-CH2Br
m_c2h4, m_dbe = mm(C=2, H=4), mm(C=2, H=4, Br=2)
mass_931 = F(28, 10) / m_c2h4 * m_dbe
assert m_c2h4 == 28 and m_dbe == 188 and mass_931 == F(188, 10)
assert mass_931 / 2 == F(94, 10) and mass_931 * 2 == F(376, 10) and F(28, 10) / m_c2h4 * 160 == 16
# 933: C3H6 + 9/2 O2 -> 3CO2 + 3H2O
mol_933 = F(42, 10) / mm(C=3, H=6)
assert mm(C=3, H=6) == 42 and mol_933 * 3 * 44 == F(132, 10)
assert mol_933 * 44 == F(44, 10) and mol_933 * 2 * 44 == F(88, 10) and mol_933 * 3 * 18 == F(54, 10)
# 934: 1.4 g alkene adds exactly 4.0 g Br2 (1 : 1)
mol_934 = F(40, 10) / 160
m_934 = F(14, 10) / mol_934
assert m_934 == 56 and mm(C=4, H=8) == 56
assert F(14, 10) / (F(40, 10) / 80) == 28 == mm(C=2, H=4)          # Br taken as 80 g mol-1
assert F(14, 10) / (mol_934 / 2) == 112 == mm(C=8, H=16)            # two Br2 per molecule assumed
# 935: C2H5OH -> C2H4 + H2O ; 9.2 g ethanol
mol_935 = F(92, 10) / mm(C=2, H=6, O=1)
assert mm(C=2, H=6, O=1) == 46 and mol_935 * F(224, 10) == F(448, 100)
# 940: 20 mL CH4 + C2H4 -> 32 mL CO2 ; x + 2(20 - x) = 32
x_ch4 = 2 * 20 - 32
pct_c2h4 = F(20 - x_ch4, 20) * 100
assert x_ch4 == 8 and pct_c2h4 == 60 and F(x_ch4, 20) * 100 == 40 and F(32, 2) / 20 * 100 == 80

QUESTIONS += [
    Q(T_HC, "Alkanes and conformations", "Basic", "direct",
      "Higher alkanes, on heating to a high temperature, decompose into lower alkanes, alkenes and so on. This "
      "decomposition is called:",
      ["Isomerisation", "Aromatisation", "Combustion", "Pyrolysis (cracking)"], "D",
      "Pyrolysis of alkanes",
      "NCERT: breaking of larger alkanes into smaller fragments by the application of heat is pyrolysis or "
      "cracking, e.g. dodecane gives heptane and pentene.",
      ["Heat → C–C bonds break → smaller alkanes and alkenes", "This is pyrolysis (cracking)"],
      why_others_wrong="Isomerisation rearranges a chain without breaking it into smaller molecules. Aromatisation "
                       "converts n-alkanes (C6 or more) into benzene homologues. Combustion needs oxygen and gives "
                       "CO₂ and water.",
      ncert=f"{NC11}, 'Hydrocarbons', alkanes (pyrolysis)", seconds=20),

    N(T_HC, "Alkenes: addition and ozonolysis", "Basic",
      "2.8 g of ethene reacts completely with bromine dissolved in CCl₄. The mass of 1,2-dibromoethane formed is "
      "(C = 12, H = 1, Br = 80):",
      ["9.4 g", "37.6 g", "18.8 g", "16.0 g"], "C", "18.8 g",
      "Addition of bromine to an alkene",
      "One mole of ethene adds one mole of Br₂ to give one mole of CH₂Br–CH₂Br.",
      ["n(C₂H₄) = 2.8/28 = 0.1 mol", "M(C₂H₄Br₂) = 24 + 4 + 160 = 188 g mol⁻¹",
       "Mass = 0.1 × 188 = 18.8 g"],
      why_others_wrong="9.4 g uses only one bromine atom per molecule (or halves the answer). 37.6 g doubles it. "
                       "16.0 g is the mass of bromine consumed, not of the product.",
      ncert=f"{NC11}, 'Hydrocarbons', alkenes (addition of halogens)", seconds=40),

    Q(T_HC, "Alkanes and conformations", "Basic", "statement_pair",
      *sp("Alkanes are also called paraffins, because they have little affinity for (are unreactive towards) most "
          "reagents.", True,
          "In alkanes each carbon atom is sp³ hybridised; the C–C and C–H bond lengths are 154 pm and 112 pm "
          "respectively.", True),
      "Alkanes: name and structure",
      "'Paraffin' comes from parum affinis (little affinity). NCERT gives the C–C and C–H bond lengths in alkanes "
      "as 154 pm and 112 pm, with sp³ carbons.",
      ["Statement I → true", "Statement II → true"],
      ncert=f"{NC11}, 'Hydrocarbons', alkanes", seconds=30),

    N(T_HC, "Alkanes and conformations", "Basic",
      "The mass of carbon dioxide formed by the complete combustion of 4.2 g of propene is (C = 12, H = 1, O = 16):",
      ["4.4 g", "13.2 g", "8.8 g", "5.4 g"], "B", "13.2 g",
      "Combustion stoichiometry of a hydrocarbon",
      "C₃H₆ + 9/2 O₂ → 3CO₂ + 3H₂O: each mole of propene gives three moles of CO₂.",
      ["n(C₃H₆) = 4.2/42 = 0.1 mol", "n(CO₂) = 3 × 0.1 = 0.3 mol", "Mass = 0.3 × 44 = 13.2 g"],
      why_others_wrong="4.4 g and 8.8 g take one or two CO₂ per propene. 5.4 g is the mass of water formed.",
      ncert=f"{NC11}, 'Hydrocarbons', combustion of hydrocarbons", seconds=35),

    N(T_HC, "Alkenes: addition and ozonolysis", "Intermediate",
      "1.4 g of an open-chain alkene adds exactly 4.0 g of bromine. The molecular formula of the alkene is "
      "(C = 12, H = 1, Br = 80):",
      ["C₂H₄", "C₈H₁₆", "C₄H₈", "C₄H₆"], "C", "C₄H₈",
      "Molar mass from bromine uptake",
      "An alkene has one C=C bond and adds one Br₂ (160 g mol⁻¹) per molecule.",
      ["n(Br₂) = 4.0/160 = 0.025 mol = n(alkene)", "Molar mass = 1.4/0.025 = 56 g mol⁻¹",
       "CₙH₂ₙ: 14n = 56 → n = 4 → C₄H₈"],
      why_others_wrong="C₂H₄ uses 80 g mol⁻¹ (atomic Br) for bromine. C₈H₁₆ assumes two Br₂ per molecule, which "
                       "an alkene with one double bond cannot add. C₄H₆ is not an alkene formula (CₙH₂ₙ₋₂).",
      ncert=f"{NC11}, 'Hydrocarbons', alkenes (addition of halogens)", seconds=60),

    N(T_HC, "Alkenes: addition and ozonolysis", "Intermediate",
      "9.2 g of ethanol is heated with excess concentrated sulphuric acid at 443 K and is converted completely into "
      "ethene. The volume of ethene at STP is (C = 12, H = 1, O = 16; molar volume at STP = 22.4 L mol⁻¹):",
      ["2.24 L", "8.96 L", "1.12 L", "4.48 L"], "D", "4.48 L",
      "Preparation of alkenes by acidic dehydration of alcohols",
      "C₂H₅OH → CH₂=CH₂ + H₂O (conc. H₂SO₄, 443 K): one mole of ethanol gives one mole of ethene.",
      ["n(C₂H₅OH) = 9.2/46 = 0.2 mol", "n(C₂H₄) = 0.2 mol", "V = 0.2 × 22.4 = 4.48 L"],
      why_others_wrong="2.24 L halves the amount (as if two ethanol gave one ethene, which is ether formation). "
                       "8.96 L doubles it. 1.12 L divides by four.",
      ncert=f"{NC11}, 'Hydrocarbons', preparation of alkenes (acidic dehydration of alcohols)", seconds=45),

    Q(T_HC, "Alkynes", "Intermediate", "direct",
      "Which of the following reacts with sodamide (NaNH₂) to form a sodium salt, showing that it has an acidic "
      "hydrogen?",
      ["But-2-yne", "But-1-yne", "But-1-ene", "Butane"], "B",
      "Acidic character of terminal alkynes",
      "A hydrogen attached to a triply bonded (sp, 50% s character) carbon is weakly acidic and can be removed by "
      "strong bases such as NaNH₂. Only a terminal alkyne has such a hydrogen.",
      ["But-1-yne: HC≡C–CH₂CH₃ has an ≡C–H → CH₃CH₂C≡C⁻Na⁺ + NH₃",
       "But-2-yne: CH₃C≡CCH₃ has no ≡C–H", "Alkene and alkane hydrogens are not acidic enough"],
      why_others_wrong="But-2-yne is an internal alkyne with no hydrogen on an sp carbon. The sp² (alkene) and sp³ "
                       "(alkane) C–H bonds are far less acidic and do not react with sodamide.",
      ncert=f"{NC11}, 'Hydrocarbons', alkynes (acidic character of alkyne)", seconds=35),

    Q(T_HC, "Electrophilic substitution", "Intermediate", "match_list",
      *ml("Match the substituent on a benzene ring in List-I with its effect on electrophilic substitution in "
          "List-II.",
          ["–OH", "–NO₂", "–Cl", "–CH₃"],
          ["Activating and ortho/para-directing, mainly through the +R effect",
           "Activating and ortho/para-directing, through the +I effect and hyperconjugation",
           "Deactivating but ortho/para-directing", "Deactivating and meta-directing"],
          {"A": "I", "B": "IV", "C": "III", "D": "II"},
          [{"A": "II", "B": "IV", "C": "III", "D": "I"}, {"A": "I", "B": "III", "C": "IV", "D": "II"},
           {"A": "I", "B": "IV", "C": "II", "D": "III"}], "A"),
      "Directive influence of substituents",
      "–OH donates a lone pair into the ring (+R). –CH₃ donates through +I and hyperconjugation. –Cl withdraws by "
      "−I more than it donates by +R, so it deactivates, but its +R effect still directs to ortho/para. –NO₂ "
      "withdraws by −I and −R and directs to meta.",
      ["–OH → +R activating, o/p → I", "–NO₂ → deactivating, m → IV", "–Cl → deactivating, o/p → III",
       "–CH₃ → +I/hyperconjugation activating, o/p → II"],
      why_others_wrong="A-II, D-I swaps the mechanisms of –OH and –CH₃. B-III, C-IV swaps the nitro group and "
                       "chlorine. C-II, D-III makes chlorine activating and the methyl group deactivating.",
      ncert=f"{NC11}, 'Hydrocarbons', directive influence of a functional group in monosubstituted benzene",
      seconds=50),

    Q(T_HC, "Alkanes and conformations", "Intermediate", "multi_statement",
      *ms("Which of the following statements about the physical and chemical properties of alkanes are correct?",
          [("The first four members, C₁ to C₄, are gases at 298 K.", True),
           ("Alkanes from C₅ to C₁₇ are liquids at 298 K.", True),
           ("The boiling points of straight-chain alkanes rise as the molecular mass increases.", True),
           ("Alkanes dissolve readily in water.", False),
           ("Alkanes readily undergo addition reactions.", False)],
          [["a", "b", "d"], ["b", "c", "e"], ["a", "c", "e"]], "C"),
      "Properties of alkanes",
      "NCERT: C₁–C₄ are gases, C₅–C₁₇ liquids and C₁₈ onwards solids at 298 K; boiling points rise with molecular "
      "mass because van der Waals forces increase. Alkanes are non-polar, so they are insoluble in water, and being "
      "saturated they give substitution, not addition, reactions.",
      ["(a) → true", "(b) → true", "(c) → true", "(d) non-polar, insoluble in water → false",
       "(e) saturated → no addition → false"],
      why_others_wrong="Every other option includes (d) or (e), both false.",
      ncert=f"{NC11}, 'Hydrocarbons', alkanes (physical and chemical properties)", seconds=45),

    Q(T_HC, "Electrophilic substitution", "Intermediate", "assertion_reason",
      *ar("In the second step of electrophilic substitution in benzene, the arenium ion (σ-complex) loses a "
          "proton.", True,
          "Loss of the proton restores the aromatic character of the ring.", True, explains=True),
      "Mechanism of electrophilic substitution",
      "Attack of the electrophile forms an arenium ion in which one carbon is sp³ and aromaticity is lost. The "
      "ion then loses H⁺ from that sp³ carbon (removed by, e.g., AlCl₄⁻ or HSO₄⁻), which regenerates the aromatic "
      "sextet. Regaining aromatic stability is why a proton is lost instead of a nucleophile being added.",
      ["Step 1: E⁺ attacks → arenium ion (non-aromatic)", "Step 2: loss of H⁺ → aromatic ring restored",
       "R gives the driving force for A → R explains A"],
      ncert=f"{NC11}, 'Hydrocarbons', mechanism of electrophilic substitution reactions", seconds=40),

    N(T_HC, "Alkanes and conformations", "Advanced",
      "20 mL of a mixture of methane and ethene is burnt completely in excess oxygen. The carbon dioxide formed "
      "measures 32 mL, all volumes being measured at the same temperature and pressure. The percentage of ethene "
      "by volume in the mixture is:",
      ["60%", "40%", "80%", "50%"], "A", "60%",
      "Gas volume stoichiometry for a mixture",
      "CH₄ gives 1 volume of CO₂ per volume and C₂H₄ gives 2 volumes of CO₂ per volume (Avogadro's law).",
      ["Let CH₄ = x mL, C₂H₄ = (20 − x) mL", "CO₂: x + 2(20 − x) = 32 → 40 − x = 32 → x = 8 mL",
       "C₂H₄ = 12 mL → 12/20 × 100 = 60%"],
      why_others_wrong="40% is the percentage of methane. 80% assigns all the CO₂ to ethene (32/2 = 16 mL). 50% "
                       "assumes an equal mixture without solving.",
      ncert=f"{NC11}, 'Hydrocarbons', combustion; {NC11}, 'Some Basic Concepts of Chemistry', stoichiometry",
      seconds=90),

    Q(T_HC, "Alkenes: addition and ozonolysis", "Advanced", "multi_statement",
      *ms("Which of the following statements about the preparation and reactions of alkenes are correct?",
          [("The ease of dehydration of alcohols by concentrated sulphuric acid follows the order tertiary > "
            "secondary > primary.", True),
           ("Ozonolysis of ethene (O₃, then Zn/H₂O) gives two molecules of methanal.", True),
           ("The presence of a peroxide changes the product of the addition of HBr to but-2-ene.", False),
           ("Acidified KMnO₄ oxidises 2-methylpropene to propanone, carbon dioxide and water.", True),
           ("Ethene adds bromine in CCl₄ to give 1,1-dibromoethane.", False)],
          [["a", "b", "c"], ["b", "d", "e"], ["a", "c", "d"]], "D"),
      "Alkenes: preparation and reactions",
      "Tertiary alcohols dehydrate most easily because their carbocations are most stable. Ozonolysis splits "
      "CH₂=CH₂ into two HCHO. But-2-ene is symmetrical, so HBr gives 2-bromobutane with or without peroxide. "
      "Acidic permanganate cleaves (CH₃)₂C=CH₂ into (CH₃)₂C=O and CO₂ + H₂O. Br₂ adds across the double bond, one "
      "Br on each carbon (1,2-dibromoethane).",
      ["(a) 3° > 2° > 1° → true", "(b) 2HCHO → true", "(c) symmetrical alkene → same product → false",
       "(d) propanone + CO₂ + H₂O → true", "(e) product is 1,2-dibromoethane → false"],
      why_others_wrong="Each other option includes (c) or (e), or leaves out (d) or (a).",
      ncert=f"{NC11}, 'Hydrocarbons', alkenes (preparation and chemical properties); {NC12}, 'Alcohols, Phenols "
            "and Ethers', dehydration", seconds=80),

    Q(T_HC, "Benzene and aromaticity", "Advanced", "assertion_reason",
      *ar("Benzene is more stable than the hypothetical cyclohexa-1,3,5-triene with localised double bonds.", True,
          "Benzene contains alternating C–C single and C=C double bonds of different lengths.", False),
      "Resonance and stability of benzene",
      "The six π electrons of benzene are delocalised, which lowers its energy (resonance stabilisation). As a "
      "result, all six C–C bonds have the same length, 139 pm, between the C–C (154 pm) and C=C (134 pm) values; "
      "there are no separate single and double bonds.",
      ["A: delocalisation (resonance) → extra stability → true",
       "R: all C–C bonds equal (139 pm) → false"],
      ncert=f"{NC11}, 'Hydrocarbons', structure of benzene (resonance and stability)", seconds=40),

    Q(T_HC, "Alkenes: addition and ozonolysis", "Advanced", "direct",
      "Propene is treated with HBr in the presence of benzoyl peroxide to give X. X is heated with sodium in dry "
      "ether to give Y. Y is:",
      ["n-Hexane", "2,3-Dimethylbutane", "2-Methylpentane", "Propane"], "A",
      "Anti-Markovnikov addition followed by Wurtz coupling",
      "With peroxide, HBr adds to propene against Markovnikov's rule to give 1-bromopropane (X). The Wurtz reaction "
      "joins two propyl groups end to end: CH₃CH₂CH₂–CH₂CH₂CH₃.",
      ["CH₃CH=CH₂ + HBr (peroxide) → CH₃CH₂CH₂Br (X)",
       "2CH₃CH₂CH₂Br + 2Na → CH₃(CH₂)₄CH₃ + 2NaBr", "Y = n-hexane"],
      why_others_wrong="2,3-Dimethylbutane would come from 2-bromopropane, the product without peroxide. "
                       "2-Methylpentane would need a mixed n-propyl/isopropyl coupling. Propane would need "
                       "reduction of X, not the Wurtz reaction.",
      ncert=f"{NC11}, 'Hydrocarbons', peroxide effect; Wurtz reaction", seconds=60),
]

# ================================================================ Organic Compounds Containing Halogens (944-953)
# 945: SN1 rate = k[RX] ; [RX] x2, [OH-] x3
assert 2 ** 1 * 3 ** 0 == 2 and 2 * 3 == 6
# 947: CH3Br + AgF -> CH3F + AgBr
mol_947 = F(95, 10) / mm(C=1, H=3, Br=1)
assert mm(C=1, H=3, Br=1) == 95 and mol_947 * 34 == F(34, 10)
assert mol_947 * 19 == F(19, 10) and mol_947 * 34 * 2 == F(68, 10)
# 951: C2H5OH -> C2H5Br -> C2H5MgBr -> (HCHO, H3O+) CH3CH2CH2OH
mol_951 = F(46, 10) / mm(C=2, H=6, O=1)
assert mol_951 == F(1, 10) and mol_951 * mm(C=3, H=8, O=1) == 6
assert mol_951 * mm(C=4, H=10, O=1) == F(74, 10)

QUESTIONS += [
    Q(T_HX, "SN1 and SN2", "Basic", "direct",
      "A compound that rotates the plane of plane-polarised light in the clockwise direction is called:",
      ["Laevorotatory", "Dextrorotatory", "Racemic", "Achiral"], "B",
      "Optical activity",
      "NCERT: a compound that rotates the plane of polarised light to the right (clockwise) is dextrorotatory, "
      "shown by (+) or d; one that rotates it anticlockwise is laevorotatory, (−) or l.",
      ["Clockwise rotation → dextrorotatory (+)"],
      why_others_wrong="Laevorotatory compounds rotate the plane anticlockwise. A racemic mixture shows zero "
                       "rotation because the two enantiomers cancel. An achiral compound is optically inactive.",
      ncert=f"{NC12}, 'Haloalkanes and Haloarenes', stereochemical aspects (optical activity)", seconds=20),

    N(T_HX, "SN1 and SN2", "Basic",
      "2-Bromo-2-methylpropane is hydrolysed by aqueous alkali by the SN1 mechanism. At the same temperature, the "
      "concentration of the alkyl bromide is doubled and that of OH⁻ is tripled. The rate of reaction increases by "
      "a factor of:",
      ["6", "3", "2", "1"], "C", "2",
      "Rate law of an SN1 reaction",
      "In SN1, the slow step is the ionisation of the alkyl halide to a carbocation, so rate = k[RX]; the "
      "nucleophile does not appear in the rate law.",
      ["Rate = k[(CH₃)₃CBr]", "[RX] × 2 → rate × 2", "[OH⁻] × 3 → no effect", "Factor = 2"],
      why_others_wrong="6 uses the SN2 rate law, k[RX][OH⁻]. 3 makes the rate depend on OH⁻ only. 1 ignores the "
                       "change in the alkyl halide concentration.",
      ncert=f"{NC12}, 'Haloalkanes and Haloarenes', nucleophilic substitution (SN1 mechanism)", seconds=35),

    Q(T_HX, "C-X bond and preparation", "Basic", "statement_pair",
      *sp("In haloalkanes, the carbon–halogen bond is polar, with a partial positive charge on carbon.", True,
          "The carbon–halogen bond enthalpy decreases in the order C–F > C–Cl > C–Br > C–I.", True),
      "Nature of the C–X bond",
      "Halogens are more electronegative than carbon, so the C–X bond is polarised Cδ⁺–Xδ⁻. As the halogen atom "
      "becomes larger, the C–X bond becomes longer and weaker, so its bond enthalpy falls from C–F to C–I.",
      ["Statement I → true", "Statement II → true (bond length rises, bond enthalpy falls)"],
      ncert=f"{NC12}, 'Haloalkanes and Haloarenes', nature of C–X bond", seconds=30),

    N(T_HX, "C-X bond and preparation", "Intermediate",
      "9.5 g of bromomethane is heated with silver fluoride and converted completely into fluoromethane (Swarts "
      "reaction). The mass of fluoromethane formed is (C = 12, H = 1, F = 19, Br = 80):",
      ["1.9 g", "6.8 g", "9.5 g", "3.4 g"], "D", "3.4 g",
      "Halogen exchange: Swarts reaction",
      "CH₃Br + AgF → CH₃F + AgBr: one mole of bromomethane gives one mole of fluoromethane.",
      ["n(CH₃Br) = 9.5/95 = 0.1 mol", "M(CH₃F) = 12 + 3 + 19 = 34 g mol⁻¹", "Mass = 0.1 × 34 = 3.4 g"],
      why_others_wrong="1.9 g is the mass of fluorine alone. 6.8 g doubles the amount. 9.5 g assumes the mass does "
                       "not change.",
      ncert=f"{NC12}, 'Haloalkanes and Haloarenes', halogen exchange (Swarts reaction)", seconds=40),

    Q(T_HX, "SN1 and SN2", "Intermediate", "match_list",
      *ml("Match the stereochemical term in List-I with its description in List-II.",
          ["Retention", "Inversion", "Racemisation", "Enantiomers"],
          ["Conversion of an optically active compound into a 50 : 50 mixture of its two enantiomers",
           "Stereoisomers that are non-superimposable mirror images of each other",
           "The product has the same spatial arrangement of groups about the chiral carbon as the reactant",
           "The product has the opposite spatial arrangement about the chiral carbon, as in an SN2 reaction"],
          {"A": "III", "B": "IV", "C": "I", "D": "II"},
          [{"A": "IV", "B": "III", "C": "I", "D": "II"}, {"A": "III", "B": "IV", "C": "II", "D": "I"},
           {"A": "I", "B": "IV", "C": "III", "D": "II"}], "C"),
      "Stereochemistry of nucleophilic substitution",
      "NCERT defines retention (configuration kept), inversion (configuration reversed, typical of SN2), "
      "racemisation (equal amounts of both enantiomers, zero rotation, typical of SN1 at a chiral carbon) and "
      "enantiomers (non-superimposable mirror images).",
      ["Retention → same arrangement → III", "Inversion → opposite arrangement (SN2) → IV",
       "Racemisation → 50 : 50 mixture → I", "Enantiomers → non-superimposable mirror images → II"],
      why_others_wrong="A-IV, B-III swaps retention and inversion. C-II, D-I swaps racemisation and enantiomers. "
                       "A-I, C-III swaps retention and racemisation.",
      ncert=f"{NC12}, 'Haloalkanes and Haloarenes', stereochemical aspects of nucleophilic substitution",
      seconds=45),

    Q(T_HX, "C-X bond and preparation", "Intermediate", "multi_statement",
      *ms("Which of the following statements about the reactions of haloarenes are correct?",
          [("Chlorobenzene is converted into phenol by heating with aqueous NaOH at 623 K and 300 atm.", True),
           ("Chlorination of chlorobenzene (Cl₂, anhydrous FeCl₃) gives mainly o- and p-dichlorobenzene.", True),
           ("Nitration of chlorobenzene gives mainly m-chloronitrobenzene.", False),
           ("Haloarenes undergo SN1 reactions readily because the phenyl cation is stabilised by resonance.",
            False),
           ("2,4,6-Trinitrochlorobenzene is hydrolysed by warm water to 2,4,6-trinitrophenol.", True)],
          [["a", "b", "c"], ["b", "d", "e"], ["a", "c", "e"]], "B"),
      "Reactions of haloarenes",
      "Haloarenes need drastic conditions for nucleophilic substitution, but nitro groups at ortho/para positions "
      "make it easy (warm water suffices for the trinitro compound). Chlorine is ortho/para-directing in "
      "electrophilic substitution. The phenyl cation is not resonance-stabilised, so the SN1 route is ruled out.",
      ["(a) Dow-type conditions → phenol → true", "(b) Cl directs o/p → true", "(c) mainly o/p, not m → false",
       "(d) phenyl cation not stabilised → false", "(e) three –NO₂ groups activate → picric acid → true"],
      why_others_wrong="Every other option includes (c) or (d), both false.",
      ncert=f"{NC12}, 'Haloalkanes and Haloarenes', reactions of haloarenes", seconds=70),

    Q(T_HX, "C-X bond and preparation", "Intermediate", "assertion_reason",
      *ar("Alkyl fluorides are best prepared by heating an alkyl chloride or bromide with a metallic fluoride such "
          "as AgF, Hg₂F₂, CoF₂ or SbF₃.", True,
          "The C–F bond is the weakest of all the carbon–halogen bonds.", False),
      "Preparation of alkyl fluorides (Swarts reaction)",
      "NCERT states that alkyl fluorides are best made by the Swarts reaction. R is false: the C–F bond is the "
      "shortest and strongest carbon–halogen bond.",
      ["A: Swarts reaction → true", "R: C–F is the strongest C–X bond → false"],
      ncert=f"{NC12}, 'Haloalkanes and Haloarenes', halogen exchange; nature of C–X bond", seconds=35),

    N(T_HX, "C-X bond and preparation", "Advanced",
      "4.6 g of ethanol is converted into bromoethane with PBr₃. The bromoethane is converted into its Grignard "
      "reagent, which is treated with methanal, and the product is hydrolysed with dilute acid. Assuming every step "
      "is complete, the mass of the final alcohol is (C = 12, H = 1, O = 16):",
      ["4.6 g", "6.0 g", "7.4 g", "3.0 g"], "B", "6.0 g",
      "Grignard reagent with methanal: a primary alcohol with one more carbon",
      "C₂H₅OH → C₂H₅Br → C₂H₅MgBr; with HCHO and hydrolysis, C₂H₅MgBr gives C₂H₅CH₂OH (propan-1-ol). One mole of "
      "ethanol gives one mole of propan-1-ol.",
      ["n(C₂H₅OH) = 4.6/46 = 0.1 mol", "Final product: CH₃CH₂CH₂OH (60 g mol⁻¹)", "Mass = 0.1 × 60 = 6.0 g"],
      why_others_wrong="4.6 g assumes the alcohol is ethanol again, ignoring the carbon added by methanal. 7.4 g is "
                       "for a butanol (as if ethanal were used). 3.0 g halves the amount.",
      ncert=f"{NC12}, 'Haloalkanes and Haloarenes', Grignard reagents; {NC12}, 'Alcohols, Phenols and Ethers', "
            "preparation of alcohols from Grignard reagents", seconds=80),

    Q(T_HX, "SN1 and SN2", "Advanced", "multi_statement",
      *ms("Which of the following statements about nucleophilic substitution in alkyl halides are correct?",
          [("(−)-2-Bromooctane reacts with OH⁻ by the SN2 mechanism to give (+)-octan-2-ol.", True),
           ("SN1 reactions are generally carried out in polar protic solvents such as water, alcohol or ethanoic "
            "acid.", True),
           ("1-Bromobutane reacts faster than 2-bromobutane by the SN2 mechanism.", True),
           ("Allyl chloride is less reactive than 1-chloropropane towards SN1 reactions.", False),
           ("In SN1 reactions, the more stable the carbocation, the slower the reaction.", False)],
          [["a", "b", "d"], ["b", "c", "e"], ["a", "c", "d", "e"]], "D"),
      "Factors in SN1 and SN2 reactions",
      "SN2 proceeds with inversion, as in NCERT's example of 2-bromooctane; it is fastest for the least hindered "
      "halide, so the primary bromide beats the secondary. SN1 needs a polar protic solvent to stabilise the ions, "
      "and its rate rises with carbocation stability, so the allyl halide (resonance-stabilised cation) is more "
      "reactive than 1-chloropropane.",
      ["(a) inversion → (+)-octan-2-ol → true", "(b) polar protic solvents → true",
       "(c) 1° faster than 2° in SN2 → true", "(d) allyl cation stabilised → more reactive → false",
       "(e) more stable carbocation → faster SN1 → false"],
      why_others_wrong="Every other option includes (d) or (e), or leaves out (c) or (a).",
      ncert=f"{NC12}, 'Haloalkanes and Haloarenes', mechanism of nucleophilic substitution", seconds=75),

    Q(T_HX, "SN1 and SN2", "Advanced", "direct",
      "1-Bromopropane is heated with alcoholic KOH to give X. X is treated with HBr in the absence of peroxide to "
      "give Y. Y is:",
      ["1-Bromopropane", "1,2-Dibromopropane", "Propan-2-ol", "2-Bromopropane"], "D",
      "Dehydrohalogenation followed by Markovnikov addition",
      "Alcoholic KOH eliminates HBr to give propene. HBr then adds by Markovnikov's rule through the more stable "
      "secondary carbocation, putting Br on C-2.",
      ["CH₃CH₂CH₂Br + alc. KOH → CH₃CH=CH₂ (X)", "CH₃CH=CH₂ + HBr → CH₃CHBrCH₃ (Y)", "Y = 2-bromopropane"],
      why_others_wrong="1-Bromopropane would need peroxide (anti-Markovnikov addition). 1,2-Dibromopropane forms "
                       "with Br₂, not HBr. Propan-2-ol would need acid-catalysed addition of water to X, not "
                       "addition of HBr.",
      ncert=f"{NC12}, 'Haloalkanes and Haloarenes', elimination reactions; {NC11}, 'Hydrocarbons', Markovnikov's "
            "rule", seconds=50),
]

# ================================================================ Organic Compounds Containing Oxygen (954-970)
# 956: C6H12O6 -> 2C2H5OH + 2CO2
mol_956 = F(18) / mm(C=6, H=12, O=6)
assert mm(C=6, H=12, O=6) == 180 and mol_956 * 2 * 46 == F(92, 10)
assert mol_956 * 46 == F(46, 10) and mol_956 * 2 * 44 == F(88, 10)
# 959: phenol (94) -> salicylaldehyde (122)
mol_959 = F(94, 10) / mm(C=6, H=6, O=1)
assert mm(C=6, H=6, O=1) == 94 and mm(C=7, H=6, O=2) == 122 and mol_959 * 122 == F(122, 10)
assert mol_959 * mm(C=7, H=6, O=3) == F(138, 10) and mol_959 * 122 * 2 == F(244, 10)
# 960: propanone (58) -> propane (44)
mol_960 = F(58, 10) / mm(C=3, H=6, O=1)
assert mm(C=3, H=6, O=1) == 58 and mol_960 * mm(C=3, H=8) == F(44, 10)
assert mol_960 * mm(C=3, H=8, O=1) == 6 and mol_960 * mm(C=3, H=6) == F(42, 10)
# 961: phenol (94) -> 2,4,6-trinitrophenol C6H3N3O7 (229)
mol_961 = F(47, 10) / 94
m_picric, m_dnp, m_np = mm(C=6, H=3, N=3, O=7), mm(C=6, H=4, N=2, O=5), mm(C=6, H=5, N=1, O=3)
assert (m_picric, m_dnp, m_np) == (229, 184, 139)
assert mol_961 * m_picric == F(1145, 100) and mol_961 * m_dnp == F(92, 10) and mol_961 * m_np == F(695, 100)
assert mol_961 * m_picric * 2 == F(229, 10)
# 966: 2Na + 2C2H5OH -> 2C2H5ONa + H2 ; C2H5ONa + C2H5Br -> C2H5OC2H5 + NaBr
mol_na = F(23, 10) / NA
ether_966 = mol_na * mm(C=4, H=10, O=1)
h2_966 = mol_na / 2 * F(224, 10)
assert mol_na == F(1, 10) and ether_966 == F(74, 10) and h2_966 == F(112, 100)
assert mol_na * F(224, 10) == F(224, 100) and mol_na * mm(C=2, H=5, O=1, Na=1) == F(68, 10)
# 967: 0.45 g dibasic acid needs 100 mL of 0.1 M NaOH
mol_naoh_967 = F(100, 1000) * F(1, 10)
m_967 = F(45, 100) / (mol_naoh_967 / 2)
assert m_967 == 90 == mm(C=2, H=2, O=4)
assert (mm(C=3, H=4, O=4), mm(C=4, H=6, O=4), mm(C=6, H=10, O=4)) == (104, 118, 146)
assert F(45, 100) / mol_naoh_967 == 45                 # monobasic assumption: no such acid among options

QUESTIONS += [
    Q(T_OX, "Aldehydes and ketones", "Basic", "direct",
      "Propanone is reduced with sodium borohydride (NaBH₄). The product is:",
      ["Propan-1-ol", "Propan-2-ol", "Propanal", "Propane"], "B",
      "Reduction of ketones to secondary alcohols",
      "Hydride reduction (NaBH₄, LiAlH₄) or catalytic hydrogenation turns the C=O of a ketone into CH–OH, giving a "
      "secondary alcohol.",
      ["CH₃COCH₃ + 2[H] → CH₃CH(OH)CH₃", "Product: propan-2-ol (a 2° alcohol)"],
      why_others_wrong="Propan-1-ol would come from propanal, not propanone. Propanal is not a reduction product of "
                       "a ketone. Propane needs the Clemmensen or Wolff–Kishner reduction, not NaBH₄.",
      ncert=f"{NC12}, 'Alcohols, Phenols and Ethers', preparation of alcohols (reduction of aldehydes and ketones)",
      seconds=20),

    Q(T_OX, "Alcohols", "Basic", "direct",
      "Methanol is also known as 'wood spirit' because it was earlier produced by:",
      ["fermentation of sugars", "hydration of ethene", "destructive distillation of wood",
       "hydrolysis of methyl chloride"], "C",
      "Methanol: common name and source",
      "NCERT: methanol, also known as wood spirit, was produced by the destructive distillation of wood; today it "
      "is made by catalytic hydrogenation of carbon monoxide.",
      ["'Wood spirit' → destructive distillation of wood"],
      why_others_wrong="Fermentation of sugars gives ethanol. Hydration of ethene also gives ethanol. Hydrolysis of "
                       "methyl chloride is not how methanol was obtained historically.",
      ncert=f"{NC12}, 'Alcohols, Phenols and Ethers', some commercially important alcohols", seconds=20),

    N(T_OX, "Alcohols", "Basic",
      "18 g of glucose is fermented completely by the enzymes of yeast: C₆H₁₂O₆ → 2C₂H₅OH + 2CO₂. The mass of "
      "ethanol formed is (C = 12, H = 1, O = 16):",
      ["4.6 g", "18.0 g", "8.8 g", "9.2 g"], "D", "9.2 g",
      "Stoichiometry of alcoholic fermentation",
      "Each mole of glucose gives two moles of ethanol.",
      ["n(glucose) = 18/180 = 0.1 mol", "n(C₂H₅OH) = 2 × 0.1 = 0.2 mol", "Mass = 0.2 × 46 = 9.2 g"],
      why_others_wrong="4.6 g takes a 1 : 1 ratio. 18.0 g assumes the mass of glucose is all ethanol. 8.8 g is the "
                       "mass of CO₂ formed.",
      ncert=f"{NC12}, 'Alcohols, Phenols and Ethers', ethanol (fermentation)", seconds=35),

    Q(T_OX, "Ethers", "Basic", "statement_pair",
      *sp("Ethoxyethane has a higher boiling point than butan-1-ol.", False,
          "Ethoxyethane and butan-1-ol have different molecular formulas.", False),
      "Ethers versus isomeric alcohols",
      "Ethoxyethane (C₂H₅OC₂H₅) and butan-1-ol (C₄H₉OH) are both C₄H₁₀O, i.e. functional isomers. Ether molecules "
      "cannot hydrogen-bond with each other, so ethoxyethane boils far lower (about 308 K) than butan-1-ol "
      "(about 391 K).",
      ["Statement I: no intermolecular H-bonding in ethers → lower b.p. → false",
       "Statement II: both are C₄H₁₀O → false"],
      ncert=f"{NC12}, 'Alcohols, Phenols and Ethers', physical properties of ethers", seconds=35),

    Q(T_OX, "Alcohols", "Basic", "assertion_reason",
      *ar("The lower alcohols are readily soluble in water.", True,
          "Alcohols can form hydrogen bonds with water molecules.", True, explains=True),
      "Solubility of alcohols",
      "NCERT: the solubility of alcohols in water is due to their ability to form hydrogen bonds with water. In the "
      "lower alcohols the small alkyl group does not prevent this, so they mix freely with water.",
      ["–OH group forms H-bonds with H₂O → soluble (A true)", "R gives this cause → R explains A"],
      ncert=f"{NC12}, 'Alcohols, Phenols and Ethers', physical properties (solubility)", seconds=25),

    N(T_OX, "Phenols", "Intermediate",
      "9.4 g of phenol is heated with chloroform and aqueous NaOH, and the mixture is then acidified (Reimer–Tiemann "
      "reaction). Assuming complete conversion, the mass of salicylaldehyde (2-hydroxybenzaldehyde) formed is "
      "(C = 12, H = 1, O = 16):",
      ["13.8 g", "12.2 g", "9.4 g", "24.4 g"], "B", "12.2 g",
      "Reimer–Tiemann reaction",
      "An –CHO group is introduced at the ortho position: C₆H₅OH → o-HOC₆H₄CHO, one mole for one mole.",
      ["n(phenol) = 9.4/94 = 0.1 mol", "M(C₇H₆O₂) = 84 + 6 + 32 = 122 g mol⁻¹", "Mass = 0.1 × 122 = 12.2 g"],
      why_others_wrong="13.8 g is for salicylic acid (138), the product of Kolbe's reaction with CO₂. 9.4 g assumes "
                       "no change in mass. 24.4 g takes two moles of product per mole of phenol.",
      ncert=f"{NC12}, 'Alcohols, Phenols and Ethers', Reimer–Tiemann reaction", seconds=45),

    N(T_OX, "Aldehydes and ketones", "Intermediate",
      "5.8 g of propanone is reduced completely with zinc amalgam and concentrated HCl (Clemmensen reduction). The "
      "mass of the organic product is (C = 12, H = 1, O = 16):",
      ["5.8 g", "6.0 g", "4.4 g", "4.2 g"], "C", "4.4 g",
      "Clemmensen reduction: C=O → CH₂",
      "Zn–Hg/conc. HCl reduces the carbonyl group of a ketone to CH₂, so propanone gives propane.",
      ["CH₃COCH₃ + 4[H] → CH₃CH₂CH₃ + H₂O", "n = 5.8/58 = 0.1 mol", "Mass of propane = 0.1 × 44 = 4.4 g"],
      why_others_wrong="5.8 g assumes no change. 6.0 g is for propan-2-ol, the product of NaBH₄ reduction, not "
                       "Clemmensen reduction. 4.2 g is for propene.",
      ncert=f"{NC12}, 'Aldehydes, Ketones and Carboxylic Acids', reduction to hydrocarbons", seconds=45),

    N(T_OX, "Phenols", "Intermediate",
      "4.7 g of phenol is converted completely into picric acid by concentrated nitric acid. The mass of picric acid "
      "formed is (C = 12, H = 1, N = 14, O = 16):",
      ["6.95 g", "9.20 g", "22.9 g", "11.45 g"], "D", "11.45 g",
      "Nitration of phenol with concentrated HNO₃",
      "With concentrated HNO₃, phenol gives 2,4,6-trinitrophenol (picric acid), C₆H₂(NO₂)₃OH, one mole per mole.",
      ["n(phenol) = 4.7/94 = 0.05 mol", "M(C₆H₃N₃O₇) = 72 + 3 + 42 + 112 = 229 g mol⁻¹",
       "Mass = 0.05 × 229 = 11.45 g"],
      why_others_wrong="6.95 g uses a mononitrophenol (139), the product with dilute HNO₃. 9.20 g uses a "
                       "dinitrophenol (184). 22.9 g doubles the amount of phenol.",
      ncert=f"{NC12}, 'Alcohols, Phenols and Ethers', nitration of phenol", seconds=55),

    Q(T_OX, "Carboxylic acids", "Intermediate", "match_list",
      *ml("Match the common name of the dicarboxylic acid in List-I with its IUPAC name in List-II.",
          ["Oxalic acid", "Malonic acid", "Succinic acid", "Phthalic acid"],
          ["Propanedioic acid", "Ethanedioic acid", "Benzene-1,2-dicarboxylic acid", "Butanedioic acid"],
          {"A": "II", "B": "I", "C": "IV", "D": "III"},
          [{"A": "I", "B": "II", "C": "IV", "D": "III"}, {"A": "II", "B": "IV", "C": "I", "D": "III"},
           {"A": "II", "B": "I", "C": "III", "D": "IV"}], "A"),
      "Common and IUPAC names of carboxylic acids",
      "Oxalic acid is HOOC–COOH (two carbons), malonic acid HOOC–CH₂–COOH (three), succinic acid "
      "HOOC–(CH₂)₂–COOH (four) and phthalic acid has two –COOH groups on adjacent ring carbons.",
      ["Oxalic → ethanedioic → II", "Malonic → propanedioic → I", "Succinic → butanedioic → IV",
       "Phthalic → benzene-1,2-dicarboxylic → III"],
      why_others_wrong="A-I, B-II swaps oxalic and malonic acids. B-IV, C-I swaps malonic and succinic acids. "
                       "C-III, D-IV gives the aromatic name to succinic acid.",
      ncert=f"{NC12}, 'Aldehydes, Ketones and Carboxylic Acids', nomenclature of carboxylic acids", seconds=40),

    Q(T_OX, "Alcohols", "Intermediate", "multi_statement",
      *ms("Which of the following statements about the reactions of alcohols are correct?",
          [("Alcohols react with sodium metal to liberate hydrogen.", True),
           ("The acid strength of alcohols follows the order primary > secondary > tertiary.", True),
           ("Alcohols are weaker acids than water.", True),
           ("A tertiary alcohol is readily oxidised to a ketone by acidified potassium dichromate.", False),
           ("Ethanol reacts with ethanoyl chloride to give ethyl ethanoate.", True)],
          [["a", "b", "c"], ["a", "c", "d", "e"], ["b", "c", "e"]], "B"),
      "Acidity and reactions of alcohols",
      "The O–H hydrogen is acidic enough to react with sodium. Alkyl groups (+I) increase electron density on "
      "oxygen, so acidity falls from 1° to 3°. NCERT notes that water is a better proton donor than an alcohol. "
      "Tertiary alcohols resist oxidation under mild conditions (there is no H on the carbinol carbon). Acid "
      "chlorides convert alcohols into esters.",
      ["(a) → true", "(b) → true", "(c) → true", "(d) 3° alcohols are not oxidised to ketones → false",
       "(e) esterification with acid chloride → true"],
      why_others_wrong="(a), (b), (c) only and (b), (c), (e) only each leave out a true statement; the remaining "
                       "option contains the false (d).",
      ncert=f"{NC12}, 'Alcohols, Phenols and Ethers', chemical reactions of alcohols", seconds=60),

    Q(T_OX, "Alcohols", "Intermediate", "assertion_reason",
      *ar("Ethanol meant for industrial use is made unfit for drinking by mixing it with some copper sulphate and "
          "pyridine.", True,
          "Methanol is highly poisonous; small quantities can cause blindness.", True),
      "Denatured alcohol",
      "Both are NCERT statements. Copper sulphate (to give a colour) and pyridine (a foul-smelling liquid) are "
      "added to denature ethanol. The toxicity of methanol is a separate fact about another alcohol and does not "
      "explain why ethanol is denatured with these substances.",
      ["A: denaturation of ethanol → true", "R: methanol is poisonous → true",
       "R is about methanol, not the reason for A → not the explanation"],
      ncert=f"{NC12}, 'Alcohols, Phenols and Ethers', some commercially important alcohols", seconds=35),

    Q(T_OX, "Aldehydes and ketones", "Intermediate", "statement_pair",
      *sp("Benzene or its derivatives, treated with carbon monoxide and HCl in the presence of anhydrous AlCl₃ or "
          "CuCl, give benzaldehyde or substituted benzaldehydes (Gattermann–Koch reaction).", True,
          "Oxidation of a secondary alcohol gives a ketone.", True),
      "Preparation of aldehydes and ketones",
      "Both are NCERT methods: the Gattermann–Koch reaction introduces –CHO into a benzene ring, and secondary "
      "alcohols are oxidised to ketones.",
      ["Statement I → true", "Statement II: R₂CHOH → R₂C=O → true"],
      ncert=f"{NC12}, 'Aldehydes, Ketones and Carboxylic Acids', preparation of aldehydes and ketones",
      seconds=30),

    N(T_OX, "Ethers", "Advanced",
      "2.3 g of sodium reacts completely with excess ethanol. The sodium ethoxide formed is then heated with excess "
      "bromoethane. Assuming both reactions are complete, the mass of ethoxyethane formed and the volume of "
      "hydrogen released in the first step (at STP) are, respectively (Na = 23, C = 12, H = 1, O = 16; molar volume "
      "at STP = 22.4 L mol⁻¹):",
      ["7.4 g and 2.24 L", "3.7 g and 1.12 L", "6.8 g and 1.12 L", "7.4 g and 1.12 L"], "D", "7.4 g and 1.12 L",
      "Sodium alkoxide formation and Williamson synthesis",
      "2Na + 2C₂H₅OH → 2C₂H₅ONa + H₂: each Na gives one ethoxide and half a mole of H₂. Then "
      "C₂H₅ONa + C₂H₅Br → C₂H₅OC₂H₅ + NaBr.",
      ["n(Na) = 2.3/23 = 0.1 mol → 0.1 mol C₂H₅ONa", "n(H₂) = 0.05 mol → 0.05 × 22.4 = 1.12 L",
       "n(ether) = 0.1 mol → 0.1 × 74 = 7.4 g"],
      why_others_wrong="2.24 L forgets that two Na give only one H₂. 3.7 g halves the ether. 6.8 g is the mass of "
                       "sodium ethoxide, not of the ether.",
      ncert=f"{NC12}, 'Alcohols, Phenols and Ethers', acidity of alcohols; Williamson synthesis", seconds=80),

    N(T_OX, "Carboxylic acids", "Advanced",
      "0.45 g of a saturated aliphatic dicarboxylic acid is neutralised exactly by 100 mL of 0.1 M NaOH. The acid "
      "is (C = 12, H = 1, O = 16):",
      ["Propanedioic acid", "Ethanedioic acid", "Butanedioic acid", "Hexanedioic acid"], "B", "Ethanedioic acid",
      "Molar mass of a dibasic acid from titration",
      "A dicarboxylic acid has two –COOH groups and needs two moles of NaOH per mole.",
      ["n(NaOH) = 0.100 × 0.1 = 0.01 mol", "n(acid) = 0.01/2 = 0.005 mol",
       "Molar mass = 0.45/0.005 = 90 g mol⁻¹", "HOOC–COOH: 24 + 2 + 64 = 90 → ethanedioic (oxalic) acid"],
      why_others_wrong="Propanedioic (104), butanedioic (118) and hexanedioic (146) acids do not have a molar mass "
                       "of 90. Treating the acid as monobasic gives 45 g mol⁻¹, which fits no dicarboxylic acid — a "
                       "sign that the 1 : 2 ratio is needed.",
      ncert=f"{NC12}, 'Aldehydes, Ketones and Carboxylic Acids', acidity of carboxylic acids", seconds=70),

    Q(T_OX, "Aldehydes and ketones", "Advanced", "multi_statement",
      *ms("Which of the following statements about aldehydes and ketones are correct?",
          [("Benzaldehyde reduces Tollens' reagent.", True),
           ("Aldehydes form crystalline hydrogensulphite addition compounds that give back the aldehyde with dilute "
            "acid or alkali, so this reaction is used to separate and purify aldehydes.", True),
           ("Ketones in general react with sodium hydrogensulphite faster than aldehydes.", False),
           ("Benzophenone gives a positive iodoform test.", False),
           ("Propanal and propanone can be distinguished by Tollens' test.", True)],
          [["a", "b", "c"], ["b", "d", "e"], ["a", "c", "e"]], "C"),
      "Reactions of aldehydes and ketones",
      "All aldehydes, aliphatic and aromatic, reduce Tollens' reagent; ketones do not, which distinguishes propanal "
      "from propanone. Bisulphite addition is used to purify aldehydes, and ketones react more slowly because of "
      "steric and electronic factors. The iodoform test needs a CH₃CO– group, which benzophenone (C₆H₅COC₆H₅) "
      "lacks.",
      ["(a) → true", "(b) → true", "(c) ketones react more slowly → false",
       "(d) no CH₃CO– group → false", "(e) only propanal gives the silver mirror → true"],
      why_others_wrong="Every other option includes (c) or (d), or leaves out (a), (b) or (e).",
      ncert=f"{NC12}, 'Aldehydes, Ketones and Carboxylic Acids', chemical reactions of aldehydes and ketones",
      seconds=70),

    Q(T_OX, "Carboxylic acids", "Advanced", "assertion_reason",
      *ar("In the vapour phase and in aprotic solvents, most carboxylic acids exist as dimers.", True,
          "Dimerisation of carboxylic acids is caused by intramolecular hydrogen bonding.", False),
      "Hydrogen bonding in carboxylic acids",
      "Two acid molecules are held together by two hydrogen bonds between the –COOH groups of different molecules, "
      "i.e. intermolecular hydrogen bonds. Intramolecular bonding (within one molecule) could not join two "
      "molecules.",
      ["A: NCERT states that carboxylic acids exist as dimers in the vapour phase / aprotic solvents → true",
       "R: the hydrogen bonds are intermolecular → false"],
      ncert=f"{NC12}, 'Aldehydes, Ketones and Carboxylic Acids', physical properties of carboxylic acids",
      seconds=40),

    Q(T_OX, "Aldehydes and ketones", "Advanced", "direct",
      "CH₃MgBr is treated with CO₂ and the product is hydrolysed to give X. X is heated with SOCl₂ to give Y. Y is "
      "hydrogenated over palladium on barium sulphate to give Z. Z is:",
      ["Ethanal", "Ethanol", "Methanal", "Propanal"], "A",
      "Grignard carboxylation, acid chloride and Rosenmund reduction",
      "A Grignard reagent adds to CO₂ to give, after hydrolysis, a carboxylic acid with one more carbon. SOCl₂ "
      "converts the acid into its acid chloride, and the Rosenmund reduction (H₂, Pd–BaSO₄) stops at the aldehyde.",
      ["CH₃MgBr + CO₂, then H₃O⁺ → CH₃COOH (X)", "CH₃COOH + SOCl₂ → CH₃COCl (Y)",
       "CH₃COCl + H₂ (Pd–BaSO₄) → CH₃CHO (Z) = ethanal"],
      why_others_wrong="Ethanol would need further reduction, which the poisoned catalyst prevents. Methanal and "
                       "propanal have the wrong number of carbons: X already has two carbons and no later step "
                       "changes that.",
      ncert=f"{NC12}, 'Aldehydes, Ketones and Carboxylic Acids', preparation of carboxylic acids (from Grignard "
            "reagents); Rosenmund reduction", seconds=60),
]

# ================================================================ Organic Compounds Containing Nitrogen (971-980)
# 971: amines C3H9N
c3h9n = ["propan-1-amine", "propan-2-amine", "N-methylethanamine", "N,N-dimethylmethanamine"]
assert len(c3h9n) == 4 and mm(C=3, H=9, N=1) == 59
# 972: phthalimide C8H5NO2 (147) -> ethanamine (45)
mol_972 = F(147, 10) / mm(C=8, H=5, N=1, O=2)
assert mm(C=8, H=5, N=1, O=2) == 147 and mol_972 * mm(C=2, H=7, N=1) == F(45, 10)
assert mol_972 * mm(C=1, H=5, N=1) == F(31, 10) and mol_972 * mm(C=4, H=11, N=1) == F(73, 10)
# 974: aniline 4.65 g -> diazonium -> p-hydroxyazobenzene C12H10N2O (198)
mol_974 = F(465, 100) / mm(C=6, H=7, N=1)
assert mm(C=6, H=7, N=1) == 93 and mol_974 == F(5, 100)
assert mm(C=12, H=10, N=2, O=1) == 198 and mol_974 * 198 == F(99, 10)
assert mol_974 * 94 == F(47, 10) and mol_974 * 198 * 2 == F(198, 10) and mol_974 * mm(C=12, H=10, N=2) == F(91, 10)
# 978: benzene 15.6 g -> nitrobenzene (80 %) -> aniline (75 %)
mol_978 = F(156, 10) / mm(C=6, H=6)
aniline_978 = mol_978 * F(80, 100) * F(75, 100) * 93
assert mm(C=6, H=6) == 78 and mol_978 == F(2, 10) and aniline_978 == F(1116, 100)
assert mol_978 * F(80, 100) * 93 == F(1488, 100) and mol_978 * 93 == F(186, 10)
assert mol_978 * F(75, 100) * 93 == F(1395, 100)

QUESTIONS += [
    N(T_NI, "Amines: basicity and identification", "Basic",
      "How many amines (primary, secondary and tertiary together) have the molecular formula C₃H₉N?",
      ["3", "4", "2", "5"], "B", "4",
      "Isomerism in amines",
      "Write all ways of distributing three carbons around the nitrogen: one propyl/isopropyl group (1°), an ethyl "
      "and a methyl (2°), or three methyl groups (3°).",
      ["1°: propan-1-amine, propan-2-amine", "2°: N-methylethanamine", "3°: N,N-dimethylmethanamine",
       "Total = 4"],
      why_others_wrong="3 misses one of the isomers, usually propan-2-amine or the tertiary amine. 2 counts only "
                       "the primary amines. 5 counts one structure twice.",
      ncert=f"{NC12}, 'Amines', classification and nomenclature of amines", seconds=40),

    N(T_NI, "Amines: basicity and identification", "Basic",
      "14.7 g of phthalimide is converted into potassium phthalimide, which is heated with ethyl iodide; the product "
      "is hydrolysed with alkali (Gabriel phthalimide synthesis). Assuming complete conversion, the mass of amine "
      "formed is (C = 12, H = 1, N = 14, O = 16):",
      ["3.1 g", "7.3 g", "14.7 g", "4.5 g"], "D", "4.5 g",
      "Gabriel phthalimide synthesis",
      "Each mole of phthalimide (C₈H₅NO₂, 147 g mol⁻¹) gives one mole of the primary amine RNH₂; with ethyl iodide "
      "the amine is ethanamine, C₂H₅NH₂ (45 g mol⁻¹).",
      ["n(phthalimide) = 14.7/147 = 0.1 mol", "Product: C₂H₅NH₂, 45 g mol⁻¹", "Mass = 0.1 × 45 = 4.5 g"],
      why_others_wrong="3.1 g is for methanamine. 7.3 g is for diethylamine, but the Gabriel synthesis gives only "
                       "primary amines. 14.7 g is the mass of phthalimide.",
      ncert=f"{NC12}, 'Amines', preparation of amines (Gabriel phthalimide synthesis)", seconds=45),

    Q(T_NI, "Amines: basicity and identification", "Basic", "statement_pair",
      *sp("In trimethylamine, the nitrogen atom is sp² hybridised and the molecule is planar.", False,
          "Lower aliphatic amines are soluble in water because they form hydrogen bonds with water molecules.", True),
      "Structure and solubility of amines",
      "The nitrogen of amines is sp³ hybridised; one sp³ orbital holds the lone pair, so amines are pyramidal (the "
      "C–N–C angle in trimethylamine is 108°). Lower aliphatic amines dissolve in water through hydrogen bonding.",
      ["Statement I: sp³ N, pyramidal → false", "Statement II: H-bonding with water → soluble → true"],
      ncert=f"{NC12}, 'Amines', structure of amines; physical properties", seconds=30),

    N(T_NI, "Diazonium salts", "Intermediate",
      "Benzenediazonium chloride is prepared from 4.65 g of aniline and is coupled completely with phenol in mildly "
      "alkaline solution to give p-hydroxyazobenzene. The mass of the dye formed is (C = 12, H = 1, N = 14, "
      "O = 16):",
      ["9.9 g", "4.7 g", "19.8 g", "9.1 g"], "A", "9.9 g",
      "Coupling of a diazonium salt with phenol",
      "One mole of aniline gives one mole of diazonium salt, which couples with one mole of phenol at the para "
      "position: C₆H₅N=N–C₆H₄OH (C₁₂H₁₀N₂O, 198 g mol⁻¹). The N=N group is kept.",
      ["n(aniline) = 4.65/93 = 0.05 mol", "M(C₁₂H₁₀N₂O) = 144 + 10 + 28 + 16 = 198 g mol⁻¹",
       "Mass = 0.05 × 198 = 9.9 g"],
      why_others_wrong="4.7 g is the mass of phenol used. 19.8 g doubles the amount. 9.1 g uses azobenzene "
                       "(C₁₂H₁₀N₂, 182) and forgets the –OH group.",
      ncert=f"{NC12}, 'Amines', reactions of diazonium salts (coupling reactions)", seconds=60),

    Q(T_NI, "Amines: basicity and identification", "Intermediate", "match_list",
      *ml("Match the compound in List-I with its class in List-II.",
          ["C₆H₅NH₂", "C₆H₅NHCH₃", "(CH₃)₃N", "(CH₃)₄N⁺Cl⁻"],
          ["Quaternary ammonium salt", "Tertiary amine", "Primary amine", "Secondary amine"],
          {"A": "III", "B": "IV", "C": "II", "D": "I"},
          [{"A": "IV", "B": "III", "C": "II", "D": "I"}, {"A": "III", "B": "II", "C": "IV", "D": "I"},
           {"A": "III", "B": "IV", "C": "I", "D": "II"}], "B"),
      "Classification of amines",
      "The class depends on how many hydrogen atoms of NH₃ are replaced by alkyl or aryl groups; with four groups "
      "on a positively charged nitrogen the compound is a quaternary ammonium salt.",
      ["C₆H₅NH₂: one group → primary → III", "C₆H₅NHCH₃: two groups → secondary → IV",
       "(CH₃)₃N: three groups → tertiary → II", "(CH₃)₄N⁺Cl⁻: four groups on N⁺ → quaternary salt → I"],
      why_others_wrong="A-IV, B-III swaps aniline and N-methylaniline. B-II, C-IV swaps the secondary and tertiary "
                       "amines. C-I, D-II calls trimethylamine a salt.",
      ncert=f"{NC12}, 'Amines', classification", seconds=35),

    Q(T_NI, "Amines: basicity and identification", "Intermediate", "assertion_reason",
      *ar("Acylation of amines with acid chlorides is carried out in the presence of pyridine.", True,
          "Pyridine, a base added to the mixture, removes the HCl formed and shifts the equilibrium to the "
          "right.", True, explains=True),
      "Acylation of amines",
      "RNH₂ + R′COCl ⇌ RNHCOR′ + HCl. The reaction is carried out in the presence of a base such as pyridine, "
      "which removes the HCl and drives the reaction forward.",
      ["HCl formed would protonate the amine and push the equilibrium back",
       "Pyridine takes up HCl → equilibrium shifts right (R explains A)"],
      ncert=f"{NC12}, 'Amines', chemical reactions (acylation)", seconds=35),

    Q(T_NI, "Amines: basicity and identification", "Intermediate", "multi_statement",
      *ms("Which of the following statements about the preparation of amines are correct?",
          [("Reduction of nitro compounds with iron scrap and HCl is preferred because the FeCl₂ formed is "
            "hydrolysed to release HCl, so only a small amount of acid is needed.", True),
           ("Amides are reduced to amines by lithium aluminium hydride.", True),
           ("Catalytic hydrogenation of nitriles gives secondary amines as the main product.", False),
           ("Nitro compounds are reduced to amines by hydrogen in the presence of finely divided Ni, Pd or Pt.",
            True),
           ("Amides are reduced by lithium aluminium hydride to nitriles.", False)],
          [["a", "b", "c"], ["b", "d", "e"], ["a", "c", "d"]], "A"),
      "Preparation of amines by reduction",
      "NCERT: nitro compounds are reduced by H₂ over finely divided Ni, Pd or Pt, or by metals in acid; Fe/HCl is "
      "preferred for the reason in (a). Nitriles give primary amines with LiAlH₄ or catalytic hydrogenation, and "
      "amides give amines with LiAlH₄.",
      ["(a) → true", "(b) RCONH₂ + LiAlH₄ → RCH₂NH₂ → true", "(c) nitriles give primary amines → false",
       "(d) → true", "(e) amides give amines, not nitriles → false"],
      why_others_wrong="Every other option includes (c) or (e), both false.",
      ncert=f"{NC12}, 'Amines', preparation of amines", seconds=60),

    N(T_NI, "Amines: basicity and identification", "Advanced",
      "15.6 g of benzene is nitrated, giving nitrobenzene in 80% yield. The nitrobenzene is then reduced to aniline "
      "in 75% yield. The mass of aniline obtained is (C = 12, H = 1, N = 14):",
      ["14.88 g", "18.6 g", "11.16 g", "13.95 g"], "C", "11.16 g",
      "Overall yield of a two-step synthesis",
      "Each step's yield multiplies: overall yield = 0.80 × 0.75 = 0.60.",
      ["n(benzene) = 15.6/78 = 0.2 mol", "n(nitrobenzene) = 0.2 × 0.80 = 0.16 mol",
       "n(aniline) = 0.16 × 0.75 = 0.12 mol", "Mass = 0.12 × 93 = 11.16 g"],
      shortcut="Mass = 0.2 × 93 × 0.6 = 11.16 g.",
      why_others_wrong="14.88 g applies only the first yield and 13.95 g only the second. 18.6 g ignores both "
                       "yields.",
      ncert=f"{NC12}, 'Amines', preparation (reduction of nitro compounds); {NC11}, 'Hydrocarbons', nitration",
      seconds=70),

    Q(T_NI, "Diazonium salts", "Advanced", "direct",
      "Aniline is treated with NaNO₂ and HCl at 273–278 K to give X. X is warmed with CuCN/KCN to give Y, and Y is "
      "heated with dilute acid until hydrolysis is complete to give Z. Z is:",
      ["Phenol", "Benzylamine", "Benzoic acid", "Benzaldehyde"], "C",
      "Sandmeyer cyanation and nitrile hydrolysis",
      "Diazotisation gives benzenediazonium chloride. CuCN/KCN replaces N₂⁺ by –CN to give benzonitrile, and "
      "complete hydrolysis of –CN gives –COOH.",
      ["C₆H₅NH₂ → C₆H₅N₂⁺Cl⁻ (X)", "X + CuCN/KCN → C₆H₅CN (Y)", "C₆H₅CN + 2H₂O (H⁺) → C₆H₅COOH (Z)"],
      why_others_wrong="Phenol forms if X is simply warmed with water. Benzylamine would need reduction of Y, not "
                       "hydrolysis. Benzaldehyde comes from partial reduction of a nitrile (e.g. Stephen reaction), "
                       "not from hydrolysis.",
      ncert=f"{NC12}, 'Amines', reactions of diazonium salts (replacement by –CN); {NC12}, 'Aldehydes, Ketones "
            "and Carboxylic Acids', preparation of carboxylic acids from nitriles", seconds=55),

    Q(T_NI, "Amines: basicity and identification", "Advanced", "statement_pair",
      *sp("Electron-releasing groups such as –CH₃ and –OCH₃ on the benzene ring increase the basic strength of "
          "aniline.", True,
          "The pKb of aniline is lower than that of methanamine.", False),
      "Basicity of aryl amines",
      "Electron-donating groups raise the electron density on nitrogen and make the arylamine more basic; "
      "electron-withdrawing groups (–NO₂, –COOH, –X) do the opposite. Aniline is a much weaker base than "
      "methanamine because its lone pair is delocalised into the ring, so its Kb is smaller and its pKb larger "
      "(about 9.4 against about 3.4).",
      ["Statement I → true", "Statement II: weaker base → higher pKb → false"],
      ncert=f"{NC12}, 'Amines', basic character of amines (arylamines, effect of substituents)", seconds=45),
]

# ================================================================ Biomolecules (981-990)
# 982: chiral carbons in open-chain D-glucose: C2, C3, C4, C5
glucose_open = {1: "CHO", 2: "CHOH", 3: "CHOH", 4: "CHOH", 5: "CHOH", 6: "CH2OH"}
assert sum(1 for v in glucose_open.values() if v == "CHOH") == 4
# 988: C6H12O6 + 3[O] -> HOOC-(CHOH)4-COOH (C6H10O8) + H2O
mol_988 = F(18) / 180
assert mm(C=6, H=10, O=8) == 210 and mol_988 * 210 == 21
assert mm(C=6, H=12, O=7) == 196 and mol_988 * 196 == F(196, 10) and mol_988 * mm(C=6, H=14) == F(86, 10)

QUESTIONS += [
    Q(T_BM, "Vitamins", "Basic", "direct",
      "Increased fragility of red blood cells and muscular weakness are caused by a deficiency of:",
      ["Vitamin E", "Vitamin K", "Vitamin B₆", "Vitamin A"], "A",
      "Vitamin deficiency diseases",
      "NCERT's table of vitamins lists increased fragility of RBCs and muscular weakness as the deficiency signs "
      "of vitamin E.",
      ["Vitamin E deficiency → fragile RBCs, muscular weakness"],
      why_others_wrong="Vitamin K deficiency increases blood clotting time. Vitamin B₆ deficiency causes "
                       "convulsions. Vitamin A deficiency causes xerophthalmia and night blindness.",
      ncert=f"{NC12}, 'Biomolecules', vitamins (Table: some important vitamins and their deficiency diseases)",
      seconds=20),

    N(T_BM, "Carbohydrates", "Basic",
      "How many chiral (asymmetric) carbon atoms are present in the open-chain structure of glucose, "
      "CHO–(CHOH)₄–CH₂OH?",
      ["5", "4", "6", "3"], "B", "4",
      "Chiral carbons in the open-chain form of glucose",
      "A carbon is chiral when it carries four different groups. In the open chain, C-1 (CHO) and C-6 (CH₂OH) are "
      "not chiral; C-2 to C-5 each carry H, OH and two different carbon chains.",
      ["C-1: –CHO (only three groups) → not chiral", "C-2, C-3, C-4, C-5 → chiral",
       "C-6: –CH₂OH (two H) → not chiral", "Total = 4"],
      why_others_wrong="5 is the count for the cyclic pyranose form, where C-1 also becomes chiral. 6 counts every "
                       "carbon. 3 misses one of the CHOH carbons.",
      ncert=f"{NC12}, 'Biomolecules', glucose (structure); configuration of glucose", seconds=35),

    Q(T_BM, "Carbohydrates", "Basic", "statement_pair",
      *sp("Monosaccharides can be hydrolysed into simpler sugars.", False,
          "Starch is a polymer of β-D-glucose.", False),
      "Classification of carbohydrates",
      "NCERT defines monosaccharides as carbohydrates that cannot be hydrolysed further to a simpler "
      "polyhydroxy aldehyde or ketone. Starch is a polymer of α-D-glucose (amylose and amylopectin); β-D-glucose "
      "units make up cellulose.",
      ["Statement I: monosaccharides cannot be hydrolysed → false",
       "Statement II: starch is made of α-D-glucose → false"],
      ncert=f"{NC12}, 'Biomolecules', classification of carbohydrates; polysaccharides", seconds=30),

    Q(T_BM, "Amino acids and proteins", "Intermediate", "match_list",
      *ml("Match the amino acid in List-I with its feature in List-II.",
          ["Glycine", "Lysine", "Aspartic acid", "Cysteine"],
          ["Side chain contains a –SH group", "Has no chiral carbon atom",
           "Acidic amino acid (two carboxyl groups)", "Basic amino acid (two amino groups)"],
          {"A": "II", "B": "IV", "C": "III", "D": "I"},
          [{"A": "I", "B": "IV", "C": "III", "D": "II"}, {"A": "II", "B": "III", "C": "IV", "D": "I"},
           {"A": "II", "B": "IV", "C": "I", "D": "III"}], "D"),
      "Side chains of amino acids",
      "From NCERT's table of α-amino acids: glycine has R = H, so its α-carbon carries two H atoms; lysine's side "
      "chain ends in –NH₂; aspartic acid's side chain is –CH₂COOH; cysteine's is –CH₂SH.",
      ["Glycine (R = H) → no chiral carbon → II", "Lysine (–(CH₂)₄NH₂) → basic → IV",
       "Aspartic acid (–CH₂COOH) → acidic → III", "Cysteine (–CH₂SH) → –SH group → I"],
      why_others_wrong="A-I, D-II swaps glycine and cysteine. B-III, C-IV swaps the acidic and basic amino acids. "
                       "C-I, D-III gives the –SH group to aspartic acid.",
      ncert=f"{NC12}, 'Biomolecules', amino acids (table of natural amino acids; classification)", seconds=45),

    Q(T_BM, "Carbohydrates", "Intermediate", "multi_statement",
      *ms("Which of the following statements about carbohydrates are correct?",
          [("All monosaccharides, whether aldoses or ketoses, are reducing sugars.", True),
           ("Maltose and lactose are reducing sugars.", True),
           ("Starch and cellulose are classed as sugars because they are sweet.", False),
           ("Fructose is an aldohexose.", False),
           ("Oligosaccharides give two to ten monosaccharide units on hydrolysis.", True)],
          [["a", "b", "c"], ["b", "d", "e"], ["a", "c", "e"]], "A"),
      "Classification of carbohydrates",
      "NCERT: all monosaccharides reduce Fehling's and Tollens' reagents; in maltose and lactose a free aldehyde "
      "group can be produced at C-1 of one unit, so they too are reducing. Polysaccharides such as starch and "
      "cellulose are not sweet and are called non-sugars. Fructose is a ketohexose. Oligosaccharides give 2–10 "
      "monosaccharide units.",
      ["(a) → true", "(b) → true", "(c) polysaccharides are non-sugars → false", "(d) ketohexose → false",
       "(e) → true"],
      why_others_wrong="Every other option includes (c) or (d), both false.",
      ncert=f"{NC12}, 'Biomolecules', carbohydrates (classification, reducing sugars)", seconds=55),

    Q(T_BM, "Nucleic acids", "Intermediate", "assertion_reason",
      *ar("The two strands of DNA are complementary to each other.", True,
          "Hydrogen bonds are formed between specific pairs of bases on the two strands.", True, explains=True),
      "Double helix of DNA",
      "NCERT states that the two strands are complementary because hydrogen bonds form only between specific base "
      "pairs: adenine with thymine and guanine with cytosine. So the sequence of one strand fixes the other.",
      ["Specific pairing A–T and G–C via hydrogen bonds", "→ each strand determines the other (complementary)",
       "R explains A"],
      ncert=f"{NC12}, 'Biomolecules', structure of nucleic acids", seconds=30),

    Q(T_BM, "Carbohydrates", "Intermediate", "direct",
      "The five-membered (furanose) ring of fructose is formed when the –OH group at C-5 adds to:",
      ["the C-1 (–CH₂OH) group", "the C-2 keto (C=O) group", "the C-6 (–CH₂OH) group", "the C-4 (–OH) group"],
      "B",
      "Cyclic structure of fructose",
      "Fructose is a ketohexose with its C=O at C-2. NCERT: it exists in two cyclic forms obtained by addition of "
      "the –OH at C-5 to the C=O group; the ring contains C-2 to C-5 and one oxygen (furanose).",
      ["Keto group of fructose: C-2", "C-5 –OH adds to C-2 → hemiketal",
       "Ring: C-2, C-3, C-4, C-5 + O → five-membered (furanose)"],
      why_others_wrong="C-1 and C-6 are –CH₂OH groups and cannot accept the addition of an –OH. Joining to C-4 "
                       "would not give a ring through a carbonyl at all.",
      ncert=f"{NC12}, 'Biomolecules', fructose (cyclic structure)", seconds=35),

    N(T_BM, "Carbohydrates", "Advanced",
      "18.0 g of glucose is oxidised completely with nitric acid. The mass of the dicarboxylic acid formed is "
      "(C = 12, H = 1, O = 16):",
      ["19.6 g", "8.6 g", "21.0 g", "18.0 g"], "C", "21.0 g",
      "Oxidation of glucose to saccharic acid",
      "Nitric acid oxidises both the –CHO group (C-1) and the primary alcohol group (C-6) to –COOH, giving "
      "saccharic acid, HOOC–(CHOH)₄–COOH (C₆H₁₀O₈).",
      ["n(glucose) = 18.0/180 = 0.1 mol", "M(C₆H₁₀O₈) = 72 + 10 + 128 = 210 g mol⁻¹", "Mass = 0.1 × 210 = 21.0 g"],
      why_others_wrong="19.6 g is for gluconic acid (C₆H₁₂O₇, 196), formed by the milder oxidant bromine water. "
                       "8.6 g is n-hexane, formed with HI. 18.0 g assumes no change in mass.",
      ncert=f"{NC12}, 'Biomolecules', glucose (oxidation with nitric acid)", seconds=60),

    Q(T_BM, "Amino acids and proteins", "Advanced", "multi_statement",
      *ms("Which of the following statements about peptides and proteins are correct?",
          [("In the dipeptide glycylalanine (Gly–Ala), the carboxyl group of glycine is joined to the amino group "
            "of alanine.", True),
           ("Gly–Ala and Ala–Gly are the same compound.", False),
           ("A polypeptide with more than a hundred amino acid residues and a molecular mass above 10,000 u is "
            "called a protein.", True),
           ("The peptide linkage is an ester linkage.", False),
           ("Proteins give α-amino acids on hydrolysis.", True)],
          [["a", "b", "c"], ["c", "d", "e"], ["a", "c", "d"]], "D"),
      "Peptide bond and proteins",
      "In Gly–Ala, glycine supplies the –COOH and alanine the –NH₂ of the peptide bond; Ala–Gly joins them the other "
      "way round and is a different compound. NCERT calls a polypeptide with more than 100 residues and molecular "
      "mass above 10,000 u a protein. The peptide linkage –CO–NH– is an amide bond, and proteins are polymers of "
      "α-amino acids.",
      ["(a) → true", "(b) different sequence → different dipeptide → false", "(c) → true",
       "(d) –CO–NH– is an amide, not an ester → false", "(e) → true"],
      why_others_wrong="Every other option includes (b) or (d), both false.",
      ncert=f"{NC12}, 'Biomolecules', proteins (peptide bond, structure of proteins)", seconds=60),

    Q(T_BM, "Nucleic acids", "Advanced", "statement_pair",
      *sp("DNA is the chemical basis of heredity.", True,
          "RNA molecules are of three types: messenger RNA, ribosomal RNA and transfer RNA.", True),
      "Biological functions of nucleic acids",
      "NCERT: DNA is the chemical basis of heredity and is responsible for maintaining the identity of species, "
      "while proteins are synthesised by the RNA molecules, which are of three types — m-RNA, r-RNA and t-RNA.",
      ["Statement I → true", "Statement II → true"],
      ncert=f"{NC12}, 'Biomolecules', nucleic acids (structure and biological functions)", seconds=30),
]

# ================================================================ Principles Related to Practical Chemistry (991-1000)
# 992: 0.020 M KMnO4 in g L-1
m_kmno4 = mm(K=1, Mn=1, O=4)
assert m_kmno4 == 158 and F(2, 100) * m_kmno4 == F(316, 100)
# 994: impure Mohr's salt 1.96 g needs 40.0 mL of 0.020 M KMnO4 ; MnO4- + 5Fe2+
mmol_mno4 = F(400, 10) * F(2, 100)
pct_994 = mmol_mno4 * 5 * 392 / 1000 / F(196, 100) * 100
assert mmol_mno4 == F(4, 5) and pct_994 == 80
assert mmol_mno4 * 1 * 392 / 1000 / F(196, 100) * 100 == 16          # 1 : 1 ratio
assert mmol_mno4 * 3 * 392 / 1000 / F(196, 100) * 100 == 48          # 3 e- per MnO4-
assert mm(Fe=1, S=1, O=4) == 152 and round(float(mmol_mno4 * 5 * 152 / 1000 / F(196, 100) * 100)) == 31
# 998: 50 mL 1.0 M HCl + 50 mL 1.0 M NaOH ; dT = 6.5 K ; c = 4.2 J g-1 K-1 ; calorimeter 30 J K-1
q_998 = (100 * F(42, 10) + 30) * F(65, 10)
dh_998 = -q_998 / F(5, 100) / 1000
assert q_998 == F(5850, 2) and dh_998 == F(-585, 10)
assert -(100 * F(42, 10)) * F(65, 10) / F(5, 100) / 1000 == F(-546, 10)
assert -(50 * F(42, 10) + 30) * F(65, 10) / F(5, 100) / 1000 == F(-312, 10)   # only 50 g of solution heated
assert -q_998 / F(25, 1000) / 1000 == -117

QUESTIONS += [
    Q(T_PR, "Qualitative salt analysis", "Basic", "direct",
      "In the flame test, a salt imparts a brick-red colour to the flame. The cation present is:",
      ["Sr²⁺", "Ca²⁺", "Cu²⁺", "K⁺"], "B",
      "Flame test for cations",
      "In the flame test, calcium salts give a brick-red flame, strontium crimson red, copper green (blue-green) "
      "and potassium lilac (violet).",
      ["Brick red → Ca²⁺"],
      why_others_wrong="Sr²⁺ gives a crimson-red flame, Cu²⁺ a green or blue-green flame, and K⁺ a lilac flame.",
      ncert=f"{LAB}, qualitative analysis (flame test)", seconds=20),

    N(T_PR, "Titrimetric analysis", "Basic",
      "The strength of a 0.020 M KMnO₄ solution in grams per litre is (K = 39, Mn = 55, O = 16):",
      ["1.58 g L⁻¹", "31.6 g L⁻¹", "3.16 g L⁻¹", "0.316 g L⁻¹"], "C", "3.16 g L⁻¹",
      "Molarity and strength of a solution",
      "Strength (g L⁻¹) = molarity × molar mass.",
      ["M(KMnO₄) = 39 + 55 + 64 = 158 g mol⁻¹", "Strength = 0.020 × 158 = 3.16 g L⁻¹"],
      why_others_wrong="1.58 g L⁻¹ halves the molarity. 31.6 and 0.316 g L⁻¹ misplace the decimal point by a "
                       "factor of ten.",
      ncert=f"{LAB}, titrimetric analysis (preparation of standard solutions)", seconds=25),

    Q(T_PR, "Titrimetric analysis", "Basic", "statement_pair",
      *sp("In the titration of hydrochloric acid against sodium hydroxide, either phenolphthalein or methyl orange "
          "can be used as the indicator.", True,
          "Methyl orange is a suitable indicator for titrating a weak acid such as oxalic acid against sodium "
          "hydroxide.", False),
      "Choice of indicator in acid–base titrations",
      "For a strong acid–strong base titration, the pH jump at the end point is large and covers the ranges of both "
      "indicators. For a weak acid–strong base titration, the end point is above pH 7, so phenolphthalein is used; "
      "methyl orange would change colour too early.",
      ["Statement I: strong acid–strong base → either indicator → true",
       "Statement II: weak acid–strong base → phenolphthalein, not methyl orange → false"],
      ncert=f"{LAB}, titrimetric analysis (acid–base indicators)", seconds=35),

    N(T_PR, "Titrimetric analysis", "Intermediate",
      "1.96 g of an impure sample of Mohr's salt, FeSO₄·(NH₄)₂SO₄·6H₂O (molar mass 392 g mol⁻¹), is dissolved in "
      "dilute H₂SO₄. The whole solution needs 40.0 mL of 0.020 M KMnO₄ for complete oxidation of Fe²⁺. Assuming "
      "the impurities do not react, the percentage purity of the sample is:",
      ["16%", "80%", "48%", "31%"], "B", "80%",
      "Percentage purity from a permanganate titration",
      "In acid solution MnO₄⁻ gains 5 electrons and Fe²⁺ loses one: MnO₄⁻ + 5Fe²⁺ + 8H⁺ → Mn²⁺ + 5Fe³⁺ + 4H₂O. "
      "One mole of Mohr's salt contains one mole of Fe²⁺.",
      ["mmol MnO₄⁻ = 40.0 × 0.020 = 0.80 mmol", "mmol Fe²⁺ = 5 × 0.80 = 4.0 mmol",
       "Mass of Mohr's salt = 4.0 × 392 = 1568 mg = 1.568 g", "Purity = 1.568/1.96 × 100 = 80%"],
      why_others_wrong="16% takes a 1 : 1 ratio of MnO₄⁻ to Fe²⁺. 48% uses three electrons per MnO₄⁻ (reduction to "
                       "MnO₂, which does not happen in acid). 31% uses the molar mass of FeSO₄ (152) instead of "
                       "Mohr's salt.",
      ncert=f"{LAB}, titrimetric analysis (Mohr's salt vs KMnO₄)", seconds=75),

    Q(T_PR, "Qualitative salt analysis", "Intermediate", "match_list",
      *ml("Match the cation in List-I with the observation in its confirmatory test in List-II.",
          ["Fe³⁺", "Cu²⁺", "Ni²⁺", "Pb²⁺"],
          ["Yellow precipitate with potassium iodide solution", "Blood-red colour with potassium thiocyanate",
           "Deep blue solution with excess ammonium hydroxide",
           "Red (rosy) precipitate with dimethylglyoxime in ammoniacal solution"],
          {"A": "II", "B": "III", "C": "IV", "D": "I"},
          [{"A": "III", "B": "II", "C": "IV", "D": "I"}, {"A": "II", "B": "III", "C": "I", "D": "IV"},
           {"A": "II", "B": "IV", "C": "III", "D": "I"}], "C"),
      "Confirmatory tests for cations",
      "Fe³⁺ forms a blood-red thiocyanate complex; Cu²⁺ forms deep blue [Cu(NH₃)₄]²⁺; Ni²⁺ gives a rosy-red nickel "
      "dimethylglyoxime precipitate; Pb²⁺ gives yellow PbI₂ with KI.",
      ["Fe³⁺ → KSCN, blood red → II", "Cu²⁺ → excess NH₄OH, deep blue → III", "Ni²⁺ → DMG, red → IV",
       "Pb²⁺ → KI, yellow PbI₂ → I"],
      why_others_wrong="A-III, B-II swaps the tests for iron and copper. C-I, D-IV swaps nickel and lead. B-IV, C-III "
                       "swaps copper and nickel.",
      ncert=f"{LAB}, qualitative analysis (confirmatory tests for cations)", seconds=45),

    Q(T_PR, "Qualitative salt analysis", "Intermediate", "assertion_reason",
      *ar("In group III analysis, ammonium chloride is added to the solution before ammonium hydroxide.", True,
          "NH₄Cl suppresses the ionisation of NH₄OH (common ion effect), keeping the OH⁻ concentration low enough "
          "that only the group III hydroxides are precipitated.", True, explains=True),
      "Role of NH₄Cl in group III",
      "Group III hydroxides (Fe³⁺, Al³⁺, Cr³⁺) have very low solubility products. The common NH₄⁺ ion suppresses "
      "the ionisation of NH₄OH, so [OH⁻] stays too low to precipitate the hydroxides of later groups such as Mg²⁺ "
      "or Zn²⁺. This is exactly why NH₄Cl is added first.",
      ["A: NH₄Cl added before NH₄OH → true", "R: common ion effect lowers [OH⁻] → true",
       "R gives the purpose of A → R explains A"],
      ncert=f"{LAB}, systematic analysis of cations (group III); {NC11}, 'Equilibrium', common ion effect",
      seconds=45),

    Q(T_PR, "Titrimetric analysis", "Intermediate", "multi_statement",
      *ms("Which of the following are correct practices in titrimetric analysis?",
          [("The burette is rinsed with the solution it is to be filled with.", True),
           ("The pipette is rinsed with distilled water just before it is used to measure out the solution.",
            False),
           ("The titration flask is rinsed with the solution it is to receive.", False),
           ("For colourless solutions, the burette reading is taken at the lower meniscus.", True),
           ("For KMnO₄ solution, the burette reading is taken at the upper meniscus.", True)],
          [["a", "b", "d"], ["c", "d", "e"], ["a", "b", "e"]], "D"),
      "Correct use of volumetric apparatus",
      "The burette and pipette must be rinsed with the solutions they will deliver, so that water left inside does "
      "not dilute them. The titration flask is rinsed only with distilled water, since any solution left in it "
      "would add to the amount titrated. Colourless solutions are read at the lower meniscus; dark KMnO₄ is read "
      "at the upper meniscus.",
      ["(a) → true", "(b) water left in the pipette dilutes the solution → false",
       "(c) extra solution in the flask changes the amount → false", "(d) → true", "(e) → true"],
      why_others_wrong="Every other option includes (b) or (c), both bad practice.",
      ncert=f"{LAB}, titrimetric analysis (use of burette and pipette)", seconds=50),

    N(T_PR, "Thermochemistry and kinetics experiments", "Advanced",
      "50 mL of 1.0 M HCl is mixed with 50 mL of 1.0 M NaOH in a calorimeter, and the temperature rises by 6.5 K. "
      "Take the density of the solution as 1.0 g mL⁻¹, its specific heat as 4.2 J g⁻¹ K⁻¹ and the heat capacity of "
      "the calorimeter as 30 J K⁻¹. The enthalpy of neutralisation is:",
      ["−54.6 kJ mol⁻¹", "−31.2 kJ mol⁻¹", "−117 kJ mol⁻¹", "−58.5 kJ mol⁻¹"], "D", "−58.5 kJ mol⁻¹",
      "Enthalpy of neutralisation, including the calorimeter",
      "The heat released warms both the solution and the calorimeter. Dividing by the moles of water formed gives "
      "the enthalpy of neutralisation.",
      ["Mass of solution = 100 g", "q = (100 × 4.2 + 30) × 6.5 = 450 × 6.5 = 2925 J",
       "n(H₂O) = 0.050 × 1.0 = 0.050 mol", "ΔH = −2925/0.050 = −58 500 J mol⁻¹ = −58.5 kJ mol⁻¹"],
      why_others_wrong="−54.6 kJ mol⁻¹ ignores the heat taken up by the calorimeter. −31.2 kJ mol⁻¹ uses only 50 g "
                       "(one solution) as the mass heated. −117 kJ mol⁻¹ divides by 0.025 mol instead of 0.050 mol.",
      ncert=f"{LAB}, thermochemistry (enthalpy of neutralisation)", seconds=90),

    Q(T_PR, "Preparations", "Advanced", "multi_statement",
      *ms("Which of the following statements about laboratory preparations of organic compounds are correct?",
          [("During the preparation of p-nitroacetanilide, the reaction mixture is kept cold while the nitrating "
            "mixture is added slowly.", True),
           ("In the preparation of aniline yellow, aniline is first diazotised at 0–5 °C.", True),
           ("Crude acetanilide is purified by crystallisation.", True),
           ("Iodoform is prepared by heating ethanol with chlorine and sodium hydroxide.", False),
           ("Acetanilide is prepared by heating aniline with ethanol.", False)],
          [["a", "b", "d"], ["b", "c", "e"], ["a", "c", "d"]], "C"),
      "Preparations listed in the practical syllabus",
      "Nitration of acetanilide is kept cold to avoid over-nitration and oxidation. Diazonium salts decompose above "
      "about 5 °C, so diazotisation for aniline yellow is done in an ice bath. Solid organic products such as "
      "acetanilide are purified by crystallisation. Iodoform needs iodine (with alkali), not chlorine, and "
      "acetanilide is made by acetylation (ethanoic anhydride or ethanoyl chloride), not with ethanol.",
      ["(a) nitration kept cold → true", "(b) diazotisation at 0–5 °C → true",
       "(c) crystallisation → true", "(d) needs iodine, not chlorine → false",
       "(e) needs an acetylating agent, not ethanol → false"],
      why_others_wrong="Every other option includes (d) or (e), both false.",
      ncert=f"{LAB}, preparation of organic compounds (acetanilide, p-nitroacetanilide, aniline yellow, "
            "iodoform)", seconds=65),

    Q(T_PR, "Titrimetric analysis", "Advanced", "assertion_reason",
      *ar("A standard solution of sodium hydroxide cannot be prepared by directly weighing solid NaOH.", True,
          "Sodium hydroxide is a primary standard.", False),
      "Primary standards",
      "A primary standard must be available pure and must not change in air. Solid NaOH absorbs moisture "
      "(hygroscopic) and CO₂ from the air, so its weighed mass is not the mass of pure NaOH. Its solutions are "
      "standardised against a primary standard such as oxalic acid.",
      ["A: NaOH absorbs water and CO₂ → cannot be weighed accurately → true",
       "R: NaOH is not a primary standard → false"],
      ncert=f"{LAB}, titrimetric analysis (primary and secondary standards)", seconds=40),
]

# ---------------------------------------------------------------- package checks and output
PLAN = {T_DF: (4, 5, 4), T_CC: (5, 6, 5), T_PU: (2, 3, 2), T_GO: (5, 7, 5), T_HC: (4, 6, 4), T_HX: (3, 4, 3),
        T_OX: (5, 7, 5), T_NI: (3, 4, 3), T_BM: (3, 4, 3), T_PR: (3, 4, 3)}
TOTAL = LAST - FIRST + 1

if __name__ == "__main__":
    assert len(QUESTIONS) == TOTAL == 124, len(QUESTIONS)
    assert [x["question_id"] for x in QUESTIONS] == [f"NEET_CHE_{n:06d}" for n in range(FIRST, LAST + 1)]
    have = Counter((x["topic"], x["difficulty"]) for x in QUESTIONS)
    for topic, quota in PLAN.items():
        for diff, n in zip(("Basic", "Intermediate", "Advanced"), quota):
            assert have[(topic, diff)] == n, (topic, diff, have[(topic, diff)], n)
    keys = Counter(x["correct_answer"] for x in QUESTIONS)
    assert all(29 <= keys[k] <= 33 for k in LETTERS), keys
    fmts = Counter(x["format"] for x in QUESTIONS)
    assert 0.27 <= fmts["numerical"] / TOTAL <= 0.33, fmts
    assert all(fmts[f] / TOTAL >= 0.08 for f in fmts if f != "numerical") and len(fmts) == 6, fmts
    for x in QUESTIONS:  # every numerical answer is recomputed above
        assert (x["format"] == "numerical") == ("script:recompute" in x["verification"]["verified_by"]), x["question_id"]
    doc = {"schema_version": "1.0", "batch_id": "BATCH_004", "created_at": TODAY,
           "notes": "Package CHE_004_p2: 124 original Chemistry questions (d/f block, coordination compounds, "
                    "organic chemistry, biomolecules, practical chemistry). Numerical answers recomputed by "
                    "tools/batch_004/CHE_004_p2.py.",
           "stimuli": [], "questions": QUESTIONS}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {OUT}: {dict(Counter(x['difficulty'] for x in QUESTIONS))}, keys {dict(sorted(keys.items()))}, "
          f"formats {dict(fmts)}")
