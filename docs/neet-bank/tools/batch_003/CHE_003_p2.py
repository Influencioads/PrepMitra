"""Writes batches/parts/BATCH_003_CHE_p2.json: package CHE_003_p2 of BATCH_003 (Chemistry, 128 questions).

Topics: d- and f-Block Elements, Coordination Compounds, Purification and Characterisation of Organic Compounds,
Some Basic Principles of Organic Chemistry, Hydrocarbons, Organic Compounds Containing Halogens / Oxygen / Nitrogen,
Biomolecules (Chemistry), Principles Related to Practical Chemistry. IDs NEET_CHE_000623..NEET_CHE_000750.

Every numerical answer is re-derived below with an assert; multi-statement keys are derived from the truth value of
each statement, assertion-reason and statement-pair keys from the truth of each part. If any check fails, nothing is
written.

    python docs/neet-bank/tools/batch_003/CHE_003_p2.py
"""

import json
import sys
from collections import Counter
from fractions import Fraction as F
from pathlib import Path

TOOLS = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(TOOLS))
from qbank import ASSERTION_REASON, STATEMENT_PAIR, default_mappings  # noqa: E402

ROOT = TOOLS.parent
OUT = ROOT / "batches" / "parts" / "BATCH_003_CHE_p2.json"
TODAY = "2026-11-16"
LETTERS = "ABCD"
CHE = "Chemistry"
FIRST, LAST = 623, 750
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


# Atomic masses used in the stems
C_, H_, O_, N_, S_, P_, BR, I_, NA, MG, CL, K_, MN, CR, FE, AL, BA, CA = (
    12, 1, 16, 14, 32, 31, 80, 127, 23, 24, F(355, 10), 39, 55, 52, 56, 27, 137, 40)


def mm(**atoms):
    """Molar mass from atom counts, e.g. mm(C=2, H=6, O=1)."""
    table = {"C": C_, "H": H_, "O": O_, "N": N_, "S": S_, "P": P_, "Br": BR, "I": I_, "Na": NA, "Mg": MG,
             "Cl": CL, "K": K_, "Mn": MN, "Cr": CR, "Fe": FE, "Al": AL, "Ba": BA, "Ca": CA}
    return sum(table[k] * v for k, v in atoms.items())


QUESTIONS = []

# ================================================================ d- and f-Block Elements (623-635)
# 625: Cr in CrO4(2-) and Cr2O7(2-)
ox_chromate = -2 + 4 * 2          # x + 4(-2) = -2
ox_dichromate = F(-2 + 7 * 2, 2)  # 2x + 7(-2) = -2
assert ox_chromate == 6 and ox_dichromate == 6
# 627: 2KMnO4 -> K2MnO4 + MnO2 + O2 (513 K)
m_kmno4 = mm(K=1, Mn=1, O=4)
mol_o2_627 = F(316, 10) / m_kmno4 / 2
assert m_kmno4 == 158 and mol_o2_627 == F(1, 10) and mol_o2_627 * 32 == F(32, 10)
assert F(316, 10) / m_kmno4 * 32 == F(64, 10) and F(316, 10) / m_kmno4 * 2 * 32 == F(128, 10)
# 632: 4FeCr2O4 + 8Na2CO3 + 7O2 -> 8Na2CrO4 + 2Fe2O3 + 8CO2
m_chromite = mm(Fe=1, Cr=2, O=4)
mol_chromite = F(448, 10) / m_chromite
v_o2_632 = mol_chromite * F(7, 4) * F(224, 10)
assert m_chromite == 224 and mol_chromite == F(2, 10) and v_o2_632 == F(784, 100)
assert mol_chromite * 7 * F(224, 10) == F(3136, 100) and mol_chromite * F(224, 10) == F(448, 100)
assert mol_chromite * F(4, 7) * F(224, 10) == F(256, 100)
# 633: 4f electron count of the ions (Z: La 57, Ce 58, Eu 63, Gd 64, Yb 70, Lu 71; Xe core = 54)
f_count = {"La3+": 57 - 54 - 3, "Ce4+": 58 - 54 - 4, "Eu2+": 63 - 54 - 2, "Gd3+": 64 - 54 - 3,
           "Yb2+": 70 - 54 - 2, "Lu3+": 71 - 54 - 3}
assert f_count == {"La3+": 0, "Ce4+": 0, "Eu2+": 7, "Gd3+": 7, "Yb2+": 14, "Lu3+": 14}
n_dia = sum(1 for n in f_count.values() if n in (0, 14))
# 630: 4f counts of Pr3+ and Er3+
assert 59 - 54 - 3 == 2 and 68 - 54 - 3 == 11
assert n_dia == 4
# 635: 3MnO4(2-) + 4H+ -> 2MnO4- + MnO2 + 2H2O ; Mn +6 -> +7 (lose 1 e-), +6 -> +4 (gain 2 e-)
ox_to_red = F(2, 1) / 1          # electrons gained per MnO2 / electrons lost per MnO4-
mol_mno4_635 = F(6, 10) * ox_to_red / (ox_to_red + 1)
assert mol_mno4_635 == F(4, 10) and F(6, 10) - mol_mno4_635 == F(2, 10)

QUESTIONS += [
    Q(T_DF, "K2Cr2O7 and KMnO4", "Basic", "direct",
      "In the manufacture of potassium dichromate, a solution of sodium dichromate is treated with a potassium salt "
      "so that orange crystals of K₂Cr₂O₇ separate. The potassium salt used is:",
      ["KCl", "KOH", "K₂CO₃", "KMnO₄"], "A",
      "Last step in the preparation of K₂Cr₂O₇",
      "Sodium dichromate is more soluble than potassium dichromate. Adding potassium chloride to its solution makes "
      "the less soluble K₂Cr₂O₇ crystallise out.",
      ["Chromite → Na₂CrO₄ → (acidify) Na₂Cr₂O₇", "Na₂Cr₂O₇ + 2KCl → K₂Cr₂O₇ + 2NaCl"],
      why_others_wrong="KOH and K₂CO₃ are alkaline and would convert dichromate back into yellow chromate. KMnO₄ "
                       "is an oxidising agent and plays no part in this step.",
      ncert=f"{NC12}, 'The d- and f-Block Elements', preparation of potassium dichromate", seconds=25),

    Q(T_DF, "K2Cr2O7 and KMnO4", "Basic", "direct",
      "Potassium permanganate forms dark purple (almost black) crystals. These crystals are isostructural with "
      "those of:",
      ["K₂Cr₂O₇", "K₂MnO₄", "KClO₄", "K₂SO₄"], "C",
      "Properties of potassium permanganate",
      "NCERT describes KMnO₄ as dark purple, almost black, crystals that are isostructural with KClO₄. Both are "
      "salts of a univalent cation with a tetrahedral XO₄⁻ anion.",
      ["MnO₄⁻ and ClO₄⁻ are both tetrahedral and singly charged",
       "KMnO₄ and KClO₄ therefore crystallise in the same structure"],
      why_others_wrong="K₂Cr₂O₇ contains the Cr₂O₇²⁻ ion made of two tetrahedra; K₂MnO₄ and K₂SO₄ have a doubly "
                       "charged anion and two K⁺ per formula unit, so they are not of the KXO₄ type.",
      ncert=f"{NC12}, 'The d- and f-Block Elements', potassium permanganate (properties)", seconds=25),

    N(T_DF, "K2Cr2O7 and KMnO4", "Basic",
      "When the pH of a yellow chromate solution is lowered, it turns orange:\n"
      "2CrO₄²⁻ + 2H⁺ → Cr₂O₇²⁻ + H₂O\n"
      "The oxidation state of chromium in CrO₄²⁻ is +6. Its oxidation state in the product Cr₂O₇²⁻ is:",
      ["+3", "+7", "+12", "+6"], "D", "+6",
      "Oxidation state in chromate and dichromate",
      "The chromate–dichromate change is an acid–base (condensation) equilibrium, not a redox reaction. Chromium is "
      "+6 on both sides.",
      ["Cr₂O₇²⁻: 2x + 7(−2) = −2", "2x = 12 → x = +6",
       "No change in oxidation state, so no electrons are transferred"],
      why_others_wrong="+12 is the total for two Cr atoms, not each. +3 is chromium after reduction by a reducing "
                       "agent. +7 assumes the colour change is an oxidation.",
      ncert=f"{NC12}, 'The d- and f-Block Elements', potassium dichromate (chromate–dichromate equilibrium)",
      seconds=30),

    Q(T_DF, "Lanthanoids and actinoids", "Basic", "statement_pair",
      *sp("The general electronic configuration of the actinoids is [Rn] 5f¹⁻¹⁴ 6d⁰⁻¹ 7s¹.", False,
          "The actinoids, in general, show the +3 oxidation state.", True),
      "Electronic configuration and oxidation states of the actinoids",
      "All the actinoids have the 7s² arrangement outside the variable filling of 5f and 6d, written "
      "[Rn] 5f¹⁻¹⁴ 6d⁰⁻¹ 7s². NCERT states that the actinoids in general show the +3 oxidation state, with higher "
      "states also found in the earlier members.",
      ["Statement I: the outer shell is 7s², not 7s¹ → false",
       "Statement II: +3 is the general oxidation state of the actinoids → true"],
      ncert=f"{NC12}, 'The d- and f-Block Elements', the actinoids (electronic configurations, oxidation states)",
      seconds=35),

    N(T_DF, "K2Cr2O7 and KMnO4", "Intermediate",
      "On heating to 513 K, potassium permanganate decomposes:\n"
      "2KMnO₄ → K₂MnO₄ + MnO₂ + O₂\n"
      "The mass of oxygen released by complete decomposition of 31.6 g of KMnO₄ is (K = 39, Mn = 55, O = 16):",
      ["6.4 g", "3.2 g", "1.6 g", "12.8 g"], "B", "3.2 g",
      "Stoichiometry of the thermal decomposition of KMnO₄",
      "Two moles of KMnO₄ give one mole of O₂.",
      ["Molar mass of KMnO₄ = 39 + 55 + 64 = 158 g mol⁻¹", "n(KMnO₄) = 31.6/158 = 0.2 mol",
       "n(O₂) = 0.2/2 = 0.1 mol", "Mass of O₂ = 0.1 × 32 = 3.2 g"],
      why_others_wrong="6.4 g takes one O₂ per KMnO₄. 12.8 g takes two O₂ per KMnO₄. 1.6 g uses 16 g mol⁻¹ "
                       "(atomic oxygen) instead of 32 g mol⁻¹ for O₂.",
      ncert=f"{NC12}, 'The d- and f-Block Elements', potassium permanganate (action of heat)", seconds=55),

    Q(T_DF, "Transition element trends", "Intermediate", "assertion_reason",
      *ar("The E°(M²⁺/M) value of zinc is more negative than expected from the general trend in the 3d series.",
          True,
          "Zn²⁺ has a completely filled 3d¹⁰ configuration, which makes this ion particularly stable.", True,
          explains=True),
      "Irregularities in E°(M²⁺/M) across the 3d series",
      "Across the series E°(M²⁺/M) generally becomes less negative. NCERT notes that Mn, Ni and Zn have values more "
      "negative than the trend predicts, and links the values for Mn²⁺ (half-filled d⁵) and Zn²⁺ (filled d¹⁰) to "
      "the stability of these configurations.",
      ["A: E°(Zn²⁺/Zn) = −0.76 V, more negative than the trend → true",
       "R: Zn²⁺ is 3d¹⁰, a completely filled and stable subshell → true",
       "The stability of the d¹⁰ ion favours its formation, so R explains A"],
      ncert=f"{NC12}, 'The d- and f-Block Elements', trends in the M²⁺/M standard electrode potentials",
      seconds=45),

    Q(T_DF, "K2Cr2O7 and KMnO4", "Intermediate", "match_list",
      *ml("Match the compound in List-I with its colour in List-II.",
          ["K₂Cr₂O₇", "K₂CrO₄", "K₂MnO₄", "KMnO₄"],
          ["Dark green", "Orange", "Dark purple", "Yellow"],
          {"A": "II", "B": "IV", "C": "I", "D": "III"},
          [{"A": "IV", "B": "II", "C": "I", "D": "III"}, {"A": "II", "B": "IV", "C": "III", "D": "I"},
           {"A": "IV", "B": "II", "C": "III", "D": "I"}], "A"),
      "Colours of the chromium and manganese oxoanion salts",
      "Dichromate is orange and chromate yellow. In the manufacture of KMnO₄, the dark green manganate is formed "
      "first and is then oxidised to the dark purple permanganate.",
      ["K₂Cr₂O₇ → orange → II", "K₂CrO₄ → yellow → IV", "K₂MnO₄ → dark green → I", "KMnO₄ → dark purple → III"],
      why_others_wrong="A-IV, B-II swaps chromate and dichromate. C-III, D-I swaps manganate and permanganate.",
      ncert=f"{NC12}, 'The d- and f-Block Elements', potassium dichromate and potassium permanganate", seconds=40),

    Q(T_DF, "Lanthanoids and actinoids", "Intermediate", "multi_statement",
      *ms("Which of the following statements about the electronic configurations and oxidation states of the "
          "f-block elements are correct? (Atomic numbers: Pr 59, Er 68, Th 90, Np 93; Xe = 54)",
          [("The Pr³⁺ ion has the configuration [Xe] 4f².", True),
           ("The atomic radii of the lanthanoids increase steadily from lanthanum to lutetium.", False),
           ("Neptunium can show an oxidation state as high as +7.", True),
           ("Thorium commonly shows the +4 oxidation state.", True),
           ("The Er³⁺ ion has the configuration [Xe] 4f¹².", False)],
          [["a", "b", "c"], ["c", "d", "e"], ["a", "d"]], "D"),
      "Configurations and oxidation states of lanthanoids and actinoids",
      "For a lanthanoid ion Ln³⁺ the number of 4f electrons is Z − 54 − 3. In the actinoids, the maximum oxidation "
      "state rises from +4 (Th) through +5 (Pa) and +6 (U) to +7 (Np), then falls in the later members.",
      ["(a) Pr³⁺: 59 − 54 − 3 = 4f² → true", "(b) The radii decrease (lanthanoid contraction) → false",
       "(c) Np shows states up to +7 → true", "(d) Th shows +4 → true",
       "(e) Er³⁺: 68 − 54 − 3 = 4f¹¹, not 4f¹² → false"],
      why_others_wrong="Options with (b) or (e) include false statements; (a) and (d) alone leave out the true "
                       "statement (c).",
      ncert=f"{NC12}, 'The d- and f-Block Elements', the lanthanoids and the actinoids (electronic "
            "configurations, oxidation states, lanthanoid contraction)", seconds=60),

    Q(T_DF, "Lanthanoids and actinoids", "Intermediate", "direct",
      "The steady decrease in the atomic and ionic radii from lanthanum to lutetium (lanthanoid contraction) is "
      "mainly due to:",
      ["The increase in the number of electron shells across the series",
       "The filling of the 5d orbitals, which shield the 6s electrons strongly",
       "The imperfect shielding of one 4f electron by another in the same subshell",
       "The decrease in nuclear charge across the series"], "C",
      "Cause of the lanthanoid contraction",
      "Across the series the nuclear charge rises by one unit at each step while the added electron enters the 4f "
      "subshell. 4f electrons shield one another poorly, so the effective nuclear charge felt by the outer "
      "electrons increases and the size decreases.",
      ["Electron added to 4f; nuclear charge +1 at each step",
       "Shielding of one 4f electron by another is imperfect",
       "Effective nuclear charge rises → radius contracts"],
      why_others_wrong="The number of shells does not change across the series. Electrons are added to 4f, not 5d. "
                       "The nuclear charge increases, it does not decrease.",
      ncert=f"{NC12}, 'The d- and f-Block Elements', lanthanoid contraction", seconds=35),

    N(T_DF, "K2Cr2O7 and KMnO4", "Advanced",
      "Sodium chromate is made by fusing chromite ore with sodium carbonate in free access of air:\n"
      "4FeCr₂O₄ + 8Na₂CO₃ + 7O₂ → 8Na₂CrO₄ + 2Fe₂O₃ + 8CO₂\n"
      "The volume of O₂, measured at STP, needed for 44.8 g of FeCr₂O₄ is (Fe = 56, Cr = 52, O = 16; molar volume "
      "at STP = 22.4 L mol⁻¹):",
      ["31.36 L", "4.48 L", "2.56 L", "7.84 L"], "D", "7.84 L",
      "Stoichiometry of the first step in the manufacture of K₂Cr₂O₇",
      "Four moles of chromite consume seven moles of oxygen.",
      ["Molar mass of FeCr₂O₄ = 56 + 104 + 64 = 224 g mol⁻¹", "n(FeCr₂O₄) = 44.8/224 = 0.2 mol",
       "n(O₂) = 0.2 × 7/4 = 0.35 mol", "V = 0.35 × 22.4 = 7.84 L"],
      why_others_wrong="31.36 L uses 7 mol O₂ per mol chromite (ignores the 4). 4.48 L assumes a 1 : 1 ratio. "
                       "2.56 L inverts the ratio (4/7).",
      ncert=f"{NC12}, 'The d- and f-Block Elements', preparation of potassium dichromate", seconds=75),

    N(T_DF, "Lanthanoids and actinoids", "Advanced",
      "How many of the following ions are diamagnetic?\n"
      "La³⁺, Ce⁴⁺, Eu²⁺, Gd³⁺, Yb²⁺, Lu³⁺\n"
      "(Atomic numbers: La 57, Ce 58, Eu 63, Gd 64, Yb 70, Lu 71; Xe = 54)",
      ["2", "4", "3", "6"], "B", "4",
      "4f electron counts of lanthanoid ions",
      "An f-block ion is diamagnetic only when its 4f subshell is empty (4f⁰) or completely filled (4f¹⁴). Count the "
      "4f electrons as Z − 54 − charge for these ions (the 5d and 6s electrons are lost first).",
      ["La³⁺: 57 − 54 − 3 = 4f⁰ → diamagnetic", "Ce⁴⁺: 58 − 54 − 4 = 4f⁰ → diamagnetic",
       "Eu²⁺: 63 − 54 − 2 = 4f⁷ → paramagnetic", "Gd³⁺: 64 − 54 − 3 = 4f⁷ → paramagnetic",
       "Yb²⁺: 70 − 54 − 2 = 4f¹⁴ → diamagnetic", "Lu³⁺: 71 − 54 − 3 = 4f¹⁴ → diamagnetic",
       "Diamagnetic ions = 4"],
      why_others_wrong="2 counts only the common +3 ions La³⁺ and Lu³⁺. 3 misses one of the f⁰/f¹⁴ ions (often Yb²⁺). "
                       "6 treats all the ions as diamagnetic, ignoring the seven unpaired electrons of f⁷ ions.",
      ncert=f"{NC12}, 'The d- and f-Block Elements', the lanthanoids (oxidation states and magnetic properties)",
      seconds=90),

    Q(T_DF, "K2Cr2O7 and KMnO4", "Advanced", "multi_statement",
      *ms("Which of the following statements about the oxidising reactions of permanganate and dichromate are "
          "correct?",
          [("In neutral or faintly alkaline solution, permanganate oxidises iodide to iodate (IO₃⁻).", True),
           ("In neutral solution, permanganate oxidises Mn²⁺ to MnO₂, a reaction catalysed by zinc sulphate or "
            "zinc oxide.", True),
           ("Acidified dichromate oxidises tin(II) salts to tin(IV).", True),
           ("Acidified permanganate oxidises sulphite ions to free sulphur.", False),
           ("Acidified dichromate is reduced to Cr²⁺.", False)],
          [["a", "c", "d"], ["b", "c", "e"], ["a", "b", "c", "d"]], "C"),
      "Oxidising reactions of KMnO₄ and K₂Cr₂O₇",
      "The product of an oxidation depends on the medium. NCERT lists iodide → iodate and Mn²⁺ → MnO₂ for neutral "
      "or faintly alkaline permanganate; in acid, sulphite is oxidised to sulphate and dichromate always ends as "
      "Cr³⁺.",
      ["(a) 2MnO₄⁻ + H₂O + I⁻ → 2MnO₂ + 2OH⁻ + IO₃⁻ → true",
       "(b) 2MnO₄⁻ + 3Mn²⁺ + 2H₂O → 5MnO₂ + 4H⁺ (ZnSO₄/ZnO catalyse) → true",
       "(c) Cr₂O₇²⁻ + 14H⁺ + 3Sn²⁺ → 2Cr³⁺ + 3Sn⁴⁺ + 7H₂O → true",
       "(d) SO₃²⁻ is oxidised to SO₄²⁻, not to S → false",
       "(e) Dichromate (Cr +6) is reduced to Cr³⁺ → false"],
      why_others_wrong="Every option containing (d) or (e) includes a false statement; the only fully correct set "
                       "is (a), (b) and (c).",
      ncert=f"{NC12}, 'The d- and f-Block Elements', oxidising action of KMnO₄ and K₂Cr₂O₇", seconds=80),

    N(T_DF, "K2Cr2O7 and KMnO4", "Advanced",
      "In acidic solution, green manganate ions disproportionate into permanganate and manganese dioxide. How many "
      "moles of MnO₄⁻ are formed from 0.6 mol of MnO₄²⁻?",
      ["0.2 mol", "0.3 mol", "0.4 mol", "0.6 mol"], "C", "0.4 mol",
      "Disproportionation of manganate(VI)",
      "Mn is +6 in MnO₄²⁻. It is oxidised to +7 (MnO₄⁻, losing 1 electron) and reduced to +4 (MnO₂, gaining 2 "
      "electrons). Electron balance needs two MnO₄⁻ for each MnO₂.",
      ["3MnO₄²⁻ + 4H⁺ → 2MnO₄⁻ + MnO₂ + 2H₂O",
       "Fraction converted to MnO₄⁻ = 2/3", "n(MnO₄⁻) = 0.6 × 2/3 = 0.4 mol (and 0.2 mol MnO₂)"],
      shortcut="Electrons lost = electrons gained: x × 1 = (0.6 − x) × 2 → x = 0.4.",
      why_others_wrong="0.2 mol is the amount of MnO₂. 0.3 mol assumes an equal split. 0.6 mol assumes all "
                       "manganate becomes permanganate, which needs an external oxidant.",
      ncert=f"{NC12}, 'The d- and f-Block Elements', potassium permanganate (preparation)", seconds=75),
]

# ================================================================ Coordination Compounds (636-651)
# Octahedral positions 0/1 = +x/-x, 2/3 = +y/-y, 4/5 = +z/-z; proper rotations generated by two 90° turns.
def _rotations():
    rx = (0, 1, 4, 5, 3, 2)
    ry = (5, 4, 2, 3, 0, 1)
    group, frontier = {tuple(range(6))}, [tuple(range(6))]
    while frontier:
        g = frontier.pop()
        for r in (rx, ry):
            h = tuple(r[g[i]] for i in range(6))
            if h not in group:
                group.add(h)
                frontier.append(h)
    return group


ROT = _rotations()
assert len(ROT) == 24
MIRROR = ROT | {tuple((1, 0, 3, 2, 5, 4)[g[i]] for i in range(6)) for g in ROT}
assert len(MIRROR) == 48


def mono_isomers(ligands):
    """(stereoisomers, geometrical isomers) of an octahedral complex of six unidentate ligands."""
    from itertools import permutations
    arrangements = set(permutations(ligands))
    canon = lambda arr, ops: min(tuple(arr[g[i]] for i in range(6)) for g in ops)
    return len({canon(a, ROT) for a in arrangements}), len({canon(a, MIRROR) for a in arrangements})


assert mono_isomers("aaaabb") == (2, 2)
# 641: [Co(NH3)3Cl3] -> fac and mer, both achiral
assert mono_isomers("aaabbb") == (2, 2)
# 638: K4[Fe(CN)6] -> 4K+ + [Fe(CN)6]4-
assert 4 + 1 == 5 and 4 + 1 + 6 == 11
# 636: oxidation state of Pt in [Pt(NH3)2Cl(NO2)]: x + 0 - 1 - 1 = 0
assert 0 - (2 * 0 - 1 - 1) == 2
# 647: EDTA titre -> hardness as CaCO3 (1 : 1 complex)
mmol_ca = F(100, 10) * F(1, 100)                 # 10.0 mL x 0.01 M
mg_caco3 = mmol_ca * mm(Ca=1, C=1, O=3)          # in 100 mL sample
ppm = mg_caco3 * 1000 / 100                      # mg per litre
assert mm(Ca=1, C=1, O=3) == 100 and mmol_ca == F(1, 10) and ppm == 100
assert mg_caco3 == 10 and ppm * 2 == 200 and ppm * 10 == 1000

QUESTIONS += [
    Q(T_CC, "IUPAC nomenclature", "Basic", "direct",
      "The IUPAC name of [Pt(NH₃)₂Cl(NO₂)] is:",
      ["Diamminechloridonitrito-N-platinate(II)", "Diamminechloridonitrito-N-platinum(II)",
       "Chloridodiamminenitrito-N-platinum(II)", "Diamminechloridonitrito-N-platinum(IV)"], "B",
      "Naming a neutral coordination entity",
      "Ligands are named in alphabetical order (ammine, chlorido, nitrito-N), multiplying prefixes are ignored for "
      "alphabetising, the metal of a neutral or cationic entity keeps its ordinary name, and its oxidation state is "
      "given in Roman numerals.",
      ["Oxidation state: x + 2(0) + (−1) + (−1) = 0 → x = +2",
       "Order: a(mmine) < c(hlorido) < n(itrito-N)",
       "Neutral entity → 'platinum', not 'platinate'",
       "Name: diamminechloridonitrito-N-platinum(II)"],
      why_others_wrong="'Platinate' is used only for an anionic entity. Placing chlorido before ammine breaks the "
                       "alphabetical order. Platinum is +2 here, not +4.",
      ncert=f"{NC12}, 'Coordination Compounds', nomenclature of coordination compounds", seconds=40),

    Q(T_CC, "IUPAC nomenclature", "Basic", "direct",
      "The formula of potassium tetrahydroxidozincate(II) is:",
      ["K[Zn(OH)₄]", "K₂[Zn(OH)₆]", "K₂[Zn(OH)₄]", "K₄[Zn(OH)₄]"], "C",
      "Writing a formula from an IUPAC name",
      "'Tetrahydroxido' means four OH⁻ ligands and '-ate' shows that the complex is an anion. With zinc in the +2 "
      "state the charge of the entity is +2 − 4 = −2, which needs two K⁺ ions.",
      ["[Zn(OH)₄]: +2 + 4(−1) = −2", "Two K⁺ balance the charge → K₂[Zn(OH)₄]"],
      why_others_wrong="K[Zn(OH)₄] and K₄[Zn(OH)₄] do not balance the −2 charge. K₂[Zn(OH)₆] has six hydroxido "
                       "ligands (hexa-), and its entity would carry −4.",
      ncert=f"{NC12}, 'Coordination Compounds', writing the formula of mononuclear coordination compounds",
      seconds=30),

    N(T_CC, "Werner's theory and ligands", "Basic",
      "Assuming complete dissociation, how many ions are produced in aqueous solution by one formula unit of "
      "K₄[Fe(CN)₆]?",
      ["2", "11", "4", "5"], "D", "5",
      "Ionisation of a complex salt",
      "Only the counter ions separate from the complex; the coordination entity [Fe(CN)₆]⁴⁻ stays intact in "
      "solution.",
      ["K₄[Fe(CN)₆] → 4K⁺ + [Fe(CN)₆]⁴⁻", "Number of ions = 4 + 1 = 5"],
      why_others_wrong="11 assumes the CN⁻ ligands are released as free ions. 4 counts only the K⁺ ions. 2 counts "
                       "one cation and one anion type rather than the number of ions.",
      ncert=f"{NC12}, 'Coordination Compounds', difference between double salts and complexes", seconds=25),

    Q(T_CC, "Isomerism", "Basic", "statement_pair",
      *sp("Tetrahedral complexes do not show geometrical isomerism, because the relative positions of the "
          "unidentate ligands around the central atom are the same with respect to each other.", True,
          "The cis and trans isomers of square planar [Pt(NH₃)₂Cl₂] are optically active.", False),
      "Geometrical and optical isomerism",
      "In a tetrahedron every corner is adjacent to every other corner, so there is no cis/trans distinction. A "
      "square planar complex has a mirror plane (the molecular plane), so it is not optically active.",
      ["Statement I: as stated in NCERT → true",
       "Statement II: both isomers are planar and superimposable on their mirror images → optically inactive → "
       "false"],
      ncert=f"{NC12}, 'Coordination Compounds', isomerism in coordination compounds", seconds=40),

    Q(T_CC, "Applications", "Basic", "multi_statement",
      *ms("Which of the following statements about the uses of coordination compounds are correct?",
          [("Ni²⁺ ions are estimated with dimethylglyoxime.", True),
           ("Impure nickel is purified by converting it into [Ni(CO)₄], which is then decomposed to give pure "
            "nickel.", True),
           ("Gold is extracted by forming the complex [Au(NH₃)₂]⁺ with aqueous ammonia.", False),
           ("Excess copper and iron in the body are removed with the chelating ligands D-penicillamine and "
            "desferrioxime B.", True),
           ("EDTA is used in the treatment of lead poisoning.", True)],
          [["a", "b", "d"], ["a", "b", "c", "d"], ["b", "c", "d", "e"]], "A"),
      "Applications of coordination compounds",
      "NCERT lists these uses in analysis, metallurgy and medicine. Gold (like silver) is extracted as a cyanido "
      "complex, [Au(CN)₂]⁻, formed with cyanide in the presence of oxygen and water.",
      ["(a) Dimethylglyoxime gives a red precipitate with Ni²⁺ → true",
       "(b) Mond process via [Ni(CO)₄] → true", "(c) The complex is [Au(CN)₂]⁻, not an ammine → false",
       "(d) Chelate therapy for excess Cu and Fe → true", "(e) EDTA for lead poisoning → true"],
      why_others_wrong="(a), (b) and (d) only misses the true statement (e); any option containing (c) is wrong.",
      ncert=f"{NC12}, 'Coordination Compounds', importance and applications of coordination compounds",
      seconds=50),

    N(T_CC, "Isomerism", "Intermediate",
      "The octahedral complex [Co(NH₃)₃Cl₃] is considered. The total number of stereoisomers (geometrical and "
      "optical together) is:",
      ["1", "2", "3", "4"], "B", "2",
      "Facial and meridional isomers of [MA₃B₃]",
      "In an octahedral [MA₃B₃] complex, the three identical ligands can occupy one face of the octahedron (fac) or "
      "lie on a meridian (mer). Each of these has a mirror plane, so there is no optical isomer.",
      ["fac: the three Cl at the corners of one triangular face", "mer: the three Cl in one plane through the metal",
       "Both are superimposable on their mirror images", "Total stereoisomers = 2"],
      why_others_wrong="1 misses the second geometrical arrangement. 3 or 4 add optical isomers that do not exist "
                       "for these achiral forms.",
      ncert=f"{NC12}, 'Coordination Compounds', geometrical isomerism (fac and mer)", seconds=45),

    Q(T_CC, "IUPAC nomenclature", "Intermediate", "match_list",
      *ml("Match the IUPAC name in List-I with the formula in List-II.",
          ["Hexaamminecobalt(III) chloride", "Potassium trioxalatoaluminate(III)", "Tetracarbonylnickel(0)",
           "Diamminesilver(I) dicyanidoargentate(I)"],
          ["[Ni(CO)₄]", "[Ag(NH₃)₂][Ag(CN)₂]", "[Co(NH₃)₆]Cl₃", "K₃[Al(C₂O₄)₃]"],
          {"A": "III", "B": "IV", "C": "I", "D": "II"},
          [{"A": "IV", "B": "III", "C": "I", "D": "II"}, {"A": "III", "B": "IV", "C": "II", "D": "I"},
           {"A": "III", "B": "I", "C": "IV", "D": "II"}], "D"),
      "Names and formulas of coordination compounds",
      "In the formula the cation is written first; in the name the cation is named first. Oxidation states in the "
      "names fix the charges.",
      ["Hexaamminecobalt(III) chloride → [Co(NH₃)₆]Cl₃ → III",
       "Potassium trioxalatoaluminate(III) → K₃[Al(C₂O₄)₃] → IV",
       "Tetracarbonylnickel(0) → [Ni(CO)₄] → I",
       "Diamminesilver(I) dicyanidoargentate(I) → [Ag(NH₃)₂][Ag(CN)₂] → II"],
      why_others_wrong="A-IV, B-III swaps the two salts. C-II, D-I swaps the neutral carbonyl and the silver salt. "
                       "B-I, C-IV gives aluminium the carbonyl formula.",
      ncert=f"{NC12}, 'Coordination Compounds', nomenclature of coordination compounds", seconds=45),

    Q(T_CC, "Werner's theory and ligands", "Intermediate", "assertion_reason",
      *ar("Complexes containing chelating ligands are generally more stable than similar complexes containing "
          "unidentate ligands.", True,
          "Ethane-1,2-diamine (en) is an ambidentate ligand.", False),
      "Chelate effect and denticity",
      "A di- or polydentate ligand that binds one metal ion through two or more donor atoms forms a ring (chelate); "
      "NCERT notes that such chelate complexes tend to be more stable. 'en' binds through both nitrogen atoms at "
      "once, so it is didentate (chelating), not ambidentate.",
      ["A: chelate complexes are more stable than comparable complexes of unidentate ligands → true",
       "R: an ambidentate ligand (NO₂⁻, SCN⁻) can bind through either of two different atoms, one at a time; en "
       "binds through both N atoms together → didentate → false"],
      ncert=f"{NC12}, 'Coordination Compounds', ligands (chelation)", seconds=40),

    Q(T_CC, "Werner's theory and ligands", "Intermediate", "multi_statement",
      *ms("Which of the following statements are correct?",
          [("The coordination number of a metal ion in a complex is the number of ligand donor atoms directly "
            "bonded to it.", True),
           ("The oxidation number of the central atom is the charge it would carry if all the ligands were removed "
            "along with the electron pairs shared with it.", True),
           ("In [PtCl₂(en)₂]²⁺, the coordination number of platinum is 4.", False),
           ("In K₄[Fe(CN)₆], the K⁺ ions are the counter ions.", True),
           ("A double salt such as Mohr's salt keeps its identity in aqueous solution, like a complex.", False)],
          [["a", "b", "c"], ["a", "d", "e"], ["b", "c", "d"]], "C"),
      "Definitions used in coordination chemistry",
      "Each 'en' supplies two donor N atoms, so two en and two Cl⁻ give six donor atoms. Double salts dissociate "
      "completely into simple ions in water, whereas complex ions do not.",
      ["(a) Definition of coordination number → true", "(b) Definition of oxidation number → true",
       "(c) 2 Cl + 2 × 2 N = 6 → false", "(d) [Fe(CN)₆]⁴⁻ is the complex ion; K⁺ are counter ions → true",
       "(e) Mohr's salt gives Fe²⁺, NH₄⁺ and SO₄²⁻ ions → false"],
      why_others_wrong="Options containing (c) or (e) include false statements; (a), (b) and (d) is the only "
                       "fully correct set.",
      ncert=f"{NC12}, 'Coordination Compounds', definitions of some important terms", seconds=55),

    Q(T_CC, "Valence bond theory", "Intermediate", "direct",
      "In metal carbonyls, the metal–carbon bond has both σ and π character. The π bond is formed by the donation "
      "of a pair of electrons from:",
      ["A filled d orbital of the metal into the vacant antibonding π* orbital of CO",
       "The lone pair on the carbon atom of CO into a vacant orbital of the metal",
       "The lone pair on the oxygen atom of CO into a vacant d orbital of the metal",
       "A filled π orbital of CO into a filled d orbital of the metal"], "A",
      "Synergic bonding in metal carbonyls",
      "CO donates its carbon lone pair to a vacant metal orbital (σ bond). The metal then donates electrons from a "
      "filled d orbital back into the empty π* orbital of CO (π back bond). The two effects reinforce each other.",
      ["σ bond: C lone pair → vacant metal orbital", "π bond: filled metal d orbital → vacant π* of CO",
       "Mutual strengthening = synergic effect"],
      why_others_wrong="Carbon lone-pair donation forms the σ bond, not the π bond. CO binds through carbon, not "
                       "oxygen. Donation into a filled orbital cannot form a bond.",
      ncert=f"{NC12}, 'Coordination Compounds', bonding in metal carbonyls", seconds=40),

    Q(T_CC, "Crystal field theory", "Intermediate", "statement_pair",
      *sp("In an octahedral crystal field, the t₂g orbitals point directly towards the ligands and are therefore "
          "raised in energy.", False,
          "In an octahedral field, the energy of the eg orbitals rises by (3/5)Δo and that of the t₂g orbitals "
          "falls by (2/5)Δo.", True),
      "Splitting of d orbitals in an octahedral field",
      "The dx²−y² and dz² orbitals (eg) point along the axes, towards the ligands, and are raised. The dxy, dyz and "
      "dxz orbitals (t₂g) lie between the axes and are lowered. The average energy (barycentre) is unchanged.",
      ["Statement I: it is the eg set that points at the ligands → false",
       "Statement II: 2 × (+0.6Δo) + 3 × (−0.4Δo) = 0 → true"],
      ncert=f"{NC12}, 'Coordination Compounds', crystal field splitting in octahedral complexes", seconds=45),

    N(T_CC, "Applications", "Advanced",
      "A 100 mL sample of hard water containing only Ca²⁺ as the hardness-causing ion needs 10.0 mL of 0.01 M "
      "Na₂EDTA for complete titration (Ca²⁺ and EDTA form a 1 : 1 complex). The hardness, expressed as mg of CaCO₃ "
      "per litre (ppm), is (Ca = 40, C = 12, O = 16):",
      ["100 ppm", "10 ppm", "200 ppm", "1000 ppm"], "A", "100 ppm",
      "Estimation of hardness of water with EDTA",
      "EDTA⁴⁻ is hexadentate and forms 1 : 1 complexes with Ca²⁺. The moles of EDTA used equal the moles of Ca²⁺, "
      "which are expressed as an equal number of moles of CaCO₃.",
      ["mmol EDTA = 10.0 × 0.01 = 0.10 mmol = mmol Ca²⁺", "Mass as CaCO₃ = 0.10 × 100 = 10 mg in 100 mL",
       "Per litre: 10 × (1000/100) = 100 mg L⁻¹ = 100 ppm"],
      why_others_wrong="10 ppm forgets to scale from 100 mL to 1 L. 200 ppm assumes a 1 : 2 metal : EDTA ratio. "
                       "1000 ppm scales by 100 instead of 10.",
      ncert=f"{NC12}, 'Coordination Compounds', importance and applications (estimation of hardness of water)",
      seconds=80),

    Q(T_CC, "Isomerism", "Advanced", "multi_statement",
      *ms("Which of the following statements about stereoisomerism in coordination compounds are correct?",
          [("cis-[PtCl₂(en)₂]²⁺ is optically active.", True),
           ("trans-[PtCl₂(en)₂]²⁺ is optically inactive.", True),
           ("[Co(NH₃)₆]³⁺ shows optical isomerism.", False),
           ("Square planar complexes of the type [MA₂B₂] show geometrical isomerism.", True),
           ("trans-[Co(NH₃)₄Cl₂]⁺ is optically active.", False)],
          [["a", "d", "e"], ["a", "b", "c"], ["b", "c", "d"]], "B"),
      "Optical and geometrical isomerism in complexes",
      "Optical isomerism is common in octahedral complexes containing didentate ligands; a trans arrangement has a "
      "mirror plane and is achiral. A homoleptic [MA₆] ion is highly symmetric and achiral.",
      ["(a) cis form has no mirror plane → enantiomers → true",
       "(b) trans form has a mirror plane → inactive → true",
       "(c) [Co(NH₃)₆]³⁺ has many mirror planes → no optical isomers → false",
       "(d) e.g. cis- and trans-[Pt(NH₃)₂Cl₂] → true",
       "(e) The trans tetraammine has mirror planes → inactive → false"],
      why_others_wrong="Options with (c) or (e) contain false statements; (a), (b) and (d) is the only fully correct "
                       "set.",
      ncert=f"{NC12}, 'Coordination Compounds', geometrical and optical isomerism", seconds=75),

    Q(T_CC, "Valence bond theory", "Advanced", "assertion_reason",
      *ar("[Ni(CO)₄] is paramagnetic.", False,
          "In [Ni(CO)₄], nickel is in the zero oxidation state, and the strong-field CO ligands cause the 4s "
          "electrons to pair up in the 3d orbitals, so nickel uses sp³ hybrid orbitals.", True),
      "Magnetic behaviour of [Ni(CO)₄] by valence bond theory",
      "Ni(0) is 3d⁸ 4s². In the carbonyl, the two 4s electrons are pushed into 3d, giving 3d¹⁰ with no unpaired "
      "electrons. The empty 4s and three 4p orbitals form sp³ hybrids for the four CO ligands, giving a tetrahedral, "
      "diamagnetic complex.",
      ["Ni(0) in the complex: 3d¹⁰ (after pairing), 4s⁰ 4p⁰",
       "sp³ hybridisation → tetrahedral", "No unpaired electrons → diamagnetic, so A is false",
       "R correctly describes the bonding → true"],
      ncert=f"{NC12}, 'Coordination Compounds', bonding in coordination compounds (valence bond theory)",
      seconds=50),

    Q(T_CC, "Crystal field theory", "Advanced", "direct",
      "Which of the following octahedral cobalt(III) complexes absorbs light of the shortest wavelength?",
      ["[CoF₆]³⁻", "[Co(CN)₆]³⁻", "[Co(H₂O)₆]³⁺", "[Co(NH₃)₆]³⁺"], "B",
      "Crystal field splitting and the wavelength absorbed",
      "The energy absorbed in a d–d transition equals Δo, and E = hc/λ. The larger Δo, the shorter the wavelength "
      "absorbed. For the same metal ion, Δo follows the spectrochemical series.",
      ["Field strength: F⁻ < H₂O < NH₃ < CN⁻", "Largest Δo → [Co(CN)₆]³⁻",
       "Largest energy → shortest wavelength absorbed"],
      why_others_wrong="F⁻ is the weakest ligand here, so [CoF₆]³⁻ absorbs the longest wavelength. H₂O and NH₃ give "
                       "intermediate splitting.",
      ncert=f"{NC12}, 'Coordination Compounds', crystal field theory (spectrochemical series, colour)",
      seconds=45),

    Q(T_CC, "Crystal field theory", "Advanced", "match_list",
      *ml("Match the octahedral metal ion (with the field strength of its ligands) in List-I with its d-electron "
          "arrangement in List-II.",
          ["d⁶, strong field (Δo > P)", "d⁶, weak field (Δo < P)", "d⁷, strong field (Δo > P)",
           "d⁸, weak field (Δo < P)"],
          ["t₂g⁶ eg²", "t₂g⁶ eg⁰", "t₂g⁴ eg²", "t₂g⁶ eg¹"],
          {"A": "II", "B": "III", "C": "IV", "D": "I"},
          [{"A": "III", "B": "II", "C": "IV", "D": "I"}, {"A": "II", "B": "III", "C": "I", "D": "IV"},
           {"A": "II", "B": "IV", "C": "III", "D": "I"}], "A"),
      "Filling of t₂g and eg levels",
      "When Δo > P, electrons pair in t₂g before entering eg. When Δo < P, the fourth and fifth electrons enter eg "
      "before pairing begins. A d⁸ ion has t₂g⁶ eg² whatever the field strength.",
      ["d⁶ strong: all six in t₂g → t₂g⁶ eg⁰ → II", "d⁶ weak: t₂g⁴ eg² (four unpaired) → III",
       "d⁷ strong: t₂g⁶ eg¹ → IV", "d⁸ weak: t₂g⁶ eg² → I"],
      why_others_wrong="A-III, B-II swaps the low-spin and high-spin d⁶ cases. C-I, D-IV gives the d⁷ ion eight "
                       "electrons. B-IV, C-III gives d⁶ seven electrons.",
      ncert=f"{NC12}, 'Coordination Compounds', crystal field splitting (high spin and low spin)", seconds=60),
]

# ================================================================ Purification and Characterisation (652-657)
# 653: Rf = 3.0/7.5
assert F(30, 75) == F(2, 5) and F(75, 30) == F(5, 2) and 1 - F(2, 5) == F(3, 5)
# 655: %S from BaSO4
m_baso4 = mm(Ba=1, S=1, O=4)
pct_s = F(32, 1) / m_baso4 * F(233, 1000) / F(16, 100) * 100
assert m_baso4 == 233 and pct_s == 20

QUESTIONS += [
    Q(T_PU, "Purification methods", "Basic", "direct",
      "In the petroleum industry, the different fractions of crude oil are separated by:",
      ["Steam distillation", "Fractional distillation", "Sublimation", "Distillation under reduced pressure"], "B",
      "Fractional distillation",
      "When the boiling points of the components are not far apart, the vapours are passed through a "
      "fractionating column so that repeated condensation and vaporisation separate them. NCERT names the "
      "separation of crude oil fractions as an application.",
      ["Crude oil = mixture of many hydrocarbons with close boiling points",
       "Fractionating column → fractions collected over boiling ranges"],
      why_others_wrong="Steam distillation is for steam-volatile, water-immiscible substances. Sublimation is for "
                       "solids. Reduced-pressure distillation is for liquids that decompose below their boiling "
                       "points.",
      ncert=f"{NC11}, 'Organic Chemistry – Some Basic Principles and Techniques', fractional distillation",
      seconds=20),

    N(T_PU, "Purification methods", "Basic",
      "In a thin layer chromatography experiment, a spot moves 3.0 cm from the base line while the solvent front "
      "moves 7.5 cm from the base line. The Rf value of the substance is:",
      ["0.4", "2.5", "0.6", "4.5"], "A", "0.4",
      "Retardation factor",
      "Rf = distance moved by the substance from the base line ÷ distance moved by the solvent from the base line. "
      "It is always less than 1.",
      ["Rf = 3.0/7.5 = 0.4"],
      why_others_wrong="2.5 inverts the ratio (an Rf cannot exceed 1). 0.6 is 1 − Rf. 4.5 is the difference of "
                       "the two distances in cm.",
      ncert=f"{NC11}, 'Organic Chemistry – Some Basic Principles and Techniques', chromatography (TLC)", seconds=25),

    Q(T_PU, "Quantitative analysis and formulae", "Intermediate", "direct",
      "Kjeldahl's method cannot be used to estimate nitrogen in:",
      ["Acetanilide", "Pyridine", "Aniline", "Urea"], "B",
      "Limitation of Kjeldahl's method",
      "NCERT states that Kjeldahl's method is not applicable to compounds with nitrogen in nitro and azo groups or "
      "in a ring (as in pyridine), because such nitrogen is not converted into ammonium sulphate under these "
      "conditions.",
      ["Pyridine: nitrogen is part of the ring → not converted to (NH₄)₂SO₄",
       "Amides, amines and urea give ammonium sulphate on digestion with conc. H₂SO₄"],
      why_others_wrong="Acetanilide (an amide), aniline (an amine) and urea all have nitrogen that is converted to "
                       "ammonium sulphate, so the method works for them.",
      ncert=f"{NC11}, 'Organic Chemistry – Some Basic Principles and Techniques', estimation of nitrogen "
            "(Kjeldahl's method)", seconds=30),

    N(T_PU, "Quantitative analysis and formulae", "Intermediate",
      "In the estimation of sulphur, 0.16 g of an organic compound is heated with fuming nitric acid and the "
      "sulphuric acid formed is precipitated as 0.233 g of barium sulphate. The percentage of sulphur in the "
      "compound is (Ba = 137, S = 32, O = 16):",
      ["2.0%", "40%", "20%", "10%"], "C", "20%",
      "Estimation of sulphur (Carius method)",
      "All the sulphur ends up in BaSO₄ (molar mass 233). 233 g of BaSO₄ contains 32 g of sulphur.",
      ["Mass of S = (32/233) × 0.233 = 0.032 g", "% S = (0.032/0.16) × 100 = 20%"],
      why_others_wrong="40% and 10% are off by a factor of 2. 2.0% is a decimal slip (0.0032 g of S).",
      ncert=f"{NC11}, 'Organic Chemistry – Some Basic Principles and Techniques', estimation of sulphur",
      seconds=50),

    Q(T_PU, "Qualitative analysis", "Advanced", "assertion_reason",
      *ar("Hydrazine (NH₂NH₂) does not give the Prussian blue test for nitrogen in Lassaigne's test.", True,
          "Hydrazine contains no carbon, so sodium cyanide cannot be formed when it is fused with sodium.", True,
          explains=True),
      "Basis of Lassaigne's test for nitrogen",
      "During sodium fusion, the carbon and nitrogen of the compound combine with sodium to form NaCN. The cyanide "
      "then gives sodium hexacyanidoferrate(II) and finally Prussian blue. Without carbon, no cyanide forms.",
      ["Na + C + N → NaCN (needs both C and N)", "Hydrazine has N but no C → no NaCN",
       "No Prussian blue, although nitrogen is present → R explains A"],
      ncert=f"{NC11}, 'Organic Chemistry – Some Basic Principles and Techniques', Lassaigne's test", seconds=45),

    Q(T_PU, "Purification methods", "Advanced", "multi_statement",
      *ms("Which of the following statements about methods of purification are correct?",
          [("Simple distillation separates liquids whose boiling points differ sufficiently.", True),
           ("Chloroform (b.p. 334 K) and aniline (b.p. 457 K) can be separated by distillation.", True),
           ("Fractional distillation is used when the boiling points of the liquids are far apart.", False),
           ("In steam distillation, the organic liquid boils at a temperature higher than its normal boiling "
            "point.", False),
           ("In paper chromatography, water held in the paper acts as the stationary phase.", True)],
          [["a", "b", "c"], ["b", "d", "e"], ["a", "e"]], "B"),
      "Distillation and chromatography",
      "Simple distillation suffices for a large difference in boiling points; fractional distillation is needed "
      "when they are close. In steam distillation the liquid boils when its vapour pressure plus that of water "
      "equals atmospheric pressure, i.e. below its normal boiling point.",
      ["(a) True", "(b) Boiling points differ by 123 K → simple distillation works → true",
       "(c) Fractional distillation is for close boiling points → false",
       "(d) The mixture boils below 373 K, so the organic liquid distils below its own boiling point → false",
       "(e) Paper chromatography is partition chromatography; water in the paper is stationary → true"],
      why_others_wrong="Options with (c) or (d) include false statements; (a) and (e) alone leave out the true "
                       "statement (b).",
      ncert=f"{NC11}, 'Organic Chemistry – Some Basic Principles and Techniques', methods of purification",
      seconds=60),
]

# ================================================================ Some Basic Principles of Organic Chemistry (658-676)
# 660: s character of sp2 = 1/3
assert F(1, 3) * 100 == F(100, 3)
# 664: dichloro isomers of propane: multisets of carbons (C1, C2, C3) up to end-for-end reflection
from itertools import combinations_with_replacement as cwr  # noqa: E402
_cap = {1: 3, 2: 2, 3: 3}
_dichloro = {min(c, tuple(sorted(4 - x for x in c))) for c in cwr((1, 2, 3), 2)
             if all(c.count(k) <= _cap[k] for k in c)}
assert _dichloro == {(1, 1), (1, 2), (1, 3), (2, 2)} and len(_dichloro) == 4
# 665: electrophiles in the list
_reagents = {"BF3": True, "NH3": False, "NO2+": True, "CN-": False, "AlCl3": True, "(CH3)3C+": True, "H2O": False}
assert sum(_reagents.values()) == 4
# 675: hybridisation sets of every carbon
_hyb = {"benzene": {"sp2"}, "ethyne": {"sp"}, "propene": {"sp2", "sp3"}, "buta-1,3-diene": {"sp2"},
        "propyne": {"sp", "sp3"}, "cyclohexane": {"sp3"}, "ethanenitrile": {"sp3", "sp"},
        "propa-1,2-diene": {"sp2", "sp"}}
assert sum(1 for v in _hyb.values() if len(v) == 1) == 4

QUESTIONS += [
    Q(T_GO, "Reactive intermediates", "Basic", "direct",
      "Which of the following alkyl free radicals is the most stable?",
      ["(CH₃)₃C•", "(CH₃)₂CH•", "CH₃CH₂•", "•CH₃"], "A",
      "Stability of alkyl free radicals",
      "Alkyl radicals are classified as primary, secondary or tertiary. Their stability increases from methyl to "
      "primary to secondary to tertiary, because alkyl groups release electrons to the electron-deficient carbon.",
      ["•CH₃ < CH₃CH₂• (1°) < (CH₃)₂CH• (2°) < (CH₃)₃C• (3°)"],
      why_others_wrong="The secondary, primary and methyl radicals have fewer alkyl groups on the radical carbon "
                       "and are less stable.",
      ncert=f"{NC11}, 'Organic Chemistry – Some Basic Principles and Techniques', homolytic cleavage (free "
            "radicals)", seconds=20),

    Q(T_GO, "IUPAC nomenclature", "Basic", "direct",
      "The IUPAC name of HC≡C–CH(CH₃)–CH₃ is:",
      ["2-Methylbut-3-yne", "3-Methylbut-1-yne", "1,1-Dimethylprop-2-yne", "2-Methylbutyne"], "B",
      "Naming an alkyne",
      "Choose the longest chain containing the triple bond (four carbons) and number it so that the triple bond "
      "gets the lowest locant.",
      ["Parent chain: C≡C–C–C = butyne", "Numbering from the triple-bond end: triple bond at C-1, methyl at C-3",
       "Name: 3-methylbut-1-yne"],
      why_others_wrong="2-Methylbut-3-yne numbers from the wrong end. '1,1-Dimethylprop-2-yne' does not use the "
                       "longest chain. '2-Methylbutyne' omits the locant and puts the methyl on the wrong carbon.",
      ncert=f"{NC11}, 'Organic Chemistry – Some Basic Principles and Techniques', IUPAC nomenclature", seconds=30),

    N(T_GO, "Hybridisation and functional groups", "Basic",
      "The percentage s character of the hybrid orbitals used by each carbon atom of ethene is:",
      ["25%", "50%", "33.3%", "66.7%"], "C", "33.3%",
      "s character of hybrid orbitals",
      "Each carbon of ethene is sp² hybridised: one s and two p orbitals mix, so each hybrid has 1/3 s character.",
      ["sp²: s : p = 1 : 2", "s character = 1/3 × 100 = 33.3%"],
      why_others_wrong="25% is sp³ (ethane) and 50% is sp (ethyne). 66.7% is the p character of sp².",
      ncert=f"{NC11}, 'Organic Chemistry – Some Basic Principles and Techniques', hybridisation and properties",
      seconds=20),

    Q(T_GO, "Hybridisation and functional groups", "Basic", "statement_pair",
      *sp("In a bond-line formula, all the carbon and hydrogen atoms are shown explicitly.", False,
          "The functional group of a nitrile is –N≡C.", False),
      "Bond-line formulas and functional groups",
      "In bond-line formulas, carbon and hydrogen atoms are not shown; lines are drawn in zig-zag fashion and only "
      "heteroatoms are written. A nitrile contains –C≡N, bonded through carbon; –N≡C is the isocyanide group.",
      ["Statement I: C and H are not shown in bond-line formulas → false",
       "Statement II: nitrile = –C≡N; –N≡C is an isocyanide (isonitrile) → false"],
      ncert=f"{NC11}, 'Organic Chemistry – Some Basic Principles and Techniques', structural representations; "
            "functional groups", seconds=35),

    Q(T_GO, "IUPAC nomenclature", "Basic", "match_list",
      *ml("Match the common name in List-I with the IUPAC name in List-II.",
          ["Isopentane", "Neopentane", "Acetone", "Isobutane"],
          ["2-Methylpropane", "Propanone", "2,2-Dimethylpropane", "2-Methylbutane"],
          {"A": "IV", "B": "III", "C": "II", "D": "I"},
          [{"A": "III", "B": "IV", "C": "II", "D": "I"}, {"A": "IV", "B": "I", "C": "II", "D": "III"},
           {"A": "I", "B": "III", "C": "II", "D": "IV"}], "D"),
      "Common and IUPAC names",
      "Iso- names have a (CH₃)₂CH– end; neo- names have a (CH₃)₃C– end.",
      ["Isopentane = (CH₃)₂CH–CH₂–CH₃ = 2-methylbutane → IV",
       "Neopentane = (CH₃)₃C–CH₃ = 2,2-dimethylpropane → III", "Acetone = CH₃COCH₃ = propanone → II",
       "Isobutane = (CH₃)₃CH = 2-methylpropane → I"],
      why_others_wrong="A-III, B-IV swaps isopentane and neopentane. B-I, D-III swaps neopentane and isobutane. "
                       "A-I, D-IV swaps isopentane and isobutane.",
      ncert=f"{NC11}, 'Organic Chemistry – Some Basic Principles and Techniques', nomenclature (common names)",
      seconds=35),

    Q(T_GO, "Hybridisation and functional groups", "Basic", "assertion_reason",
      *ar("The C–H bond in ethyne is shorter than the C–H bond in ethane.", True,
          "Rotation about the C–C single bond allows ethane to exist in staggered and eclipsed conformations.",
          True, explains=False),
      "Hybridisation and bond length",
      "An sp orbital has 50% s character and is held closer to the nucleus than an sp³ orbital (25% s), so bonds "
      "formed by sp carbon are shorter. The conformations of ethane are a different property and say nothing about "
      "C–H bond lengths.",
      ["A: C(sp)–H is shorter than C(sp³)–H → true",
       "R: ethane has staggered and eclipsed conformations → true",
       "The reason for A is the greater s character of the sp carbon; R is unrelated → R does not explain A"],
      ncert=f"{NC11}, 'Organic Chemistry – Some Basic Principles and Techniques', hybridisation", seconds=40),

    N(T_GO, "Isomerism", "Intermediate",
      "How many structural isomers are possible for the dichloro derivatives of propane, C₃H₆Cl₂?",
      ["3", "4", "5", "6"], "B", "4",
      "Counting position isomers",
      "Place the two chlorine atoms on the three-carbon chain in every way that gives a different compound; C-1 "
      "and C-3 are equivalent by symmetry.",
      ["1,1-Dichloropropane: CHCl₂–CH₂–CH₃", "1,2-Dichloropropane: CH₂Cl–CHCl–CH₃",
       "1,3-Dichloropropane: CH₂Cl–CH₂–CH₂Cl", "2,2-Dichloropropane: CH₃–CCl₂–CH₃",
       "2,3- is the same as 1,2-, and 3,3- is the same as 1,1- → 4 isomers"],
      why_others_wrong="3 misses a gem-dihalide (usually 2,2-). 5 or 6 count 2,3- and 3,3- as new compounds.",
      ncert=f"{NC11}, 'Organic Chemistry – Some Basic Principles and Techniques', structural isomerism",
      seconds=50),

    N(T_GO, "Reactive intermediates", "Intermediate",
      "How many of the following species can act as electrophiles?\n"
      "BF₃, NH₃, NO₂⁺, CN⁻, AlCl₃, (CH₃)₃C⁺, H₂O",
      ["3", "5", "2", "4"], "D", "4",
      "Electrophiles and nucleophiles",
      "An electrophile is electron-seeking: a positive ion or a neutral molecule with an electron-deficient atom "
      "(incomplete octet). A nucleophile has an electron pair to donate.",
      ["BF₃ and AlCl₃: incomplete octet → electrophiles", "NO₂⁺ and (CH₃)₃C⁺: positive → electrophiles",
       "NH₃, CN⁻ and H₂O: carry lone pairs → nucleophiles", "Electrophiles = 4"],
      why_others_wrong="3 or 2 leave out the neutral Lewis acids (BF₃, AlCl₃) or one cation. 5 wrongly counts a "
                       "lone-pair donor such as H₂O.",
      ncert=f"{NC11}, 'Organic Chemistry – Some Basic Principles and Techniques', nucleophiles and electrophiles",
      seconds=45),

    Q(T_GO, "IUPAC nomenclature", "Intermediate", "direct",
      "The IUPAC name of HO–CH₂–CH₂–CO–CH₃ is:",
      ["1-Hydroxybutan-3-one", "3-Oxobutan-1-ol", "4-Hydroxybutan-2-one", "3-Hydroxybutan-2-one"], "C",
      "Priority of functional groups in naming",
      "When a compound has both a ketone and an alcohol group, the ketone is the principal group (suffix -one) "
      "and the –OH is named as the prefix 'hydroxy'. The principal group gets the lower locant.",
      ["Chain of four carbons: butanone", "Number from the CH₃ end: C=O at C-2, –OH at C-4",
       "Name: 4-hydroxybutan-2-one"],
      why_others_wrong="1-Hydroxybutan-3-one gives the principal group the higher locant. 3-Oxobutan-1-ol makes "
                       "the alcohol the principal group. 3-Hydroxybutan-2-one is a different compound, "
                       "CH₃–CH(OH)–CO–CH₃.",
      ncert=f"{NC11}, 'Organic Chemistry – Some Basic Principles and Techniques', nomenclature of compounds with "
            "more than one functional group", seconds=40),

    Q(T_GO, "Electronic effects", "Intermediate", "multi_statement",
      *ms("Which of the following statements about the resonance effect are correct?",
          [("The –NHCOCH₃ group attached to a benzene ring shows a +R effect.", True),
           ("In aniline, the electron density increases at the ortho and para positions of the ring.", True),
           ("The resonance effect is transmitted through σ bonds and dies out after about three bonds.", False),
           ("A halogen attached to a benzene ring shows a −I effect as well as a +R effect.", True),
           ("The resonance effect operates only when an attacking reagent is present.", False)],
          [["a", "b", "c"], ["b", "d", "e"], ["a", "c", "d"]], "A"),
      "Resonance (mesomeric) effect",
      "The resonance effect is the polarity produced by the interaction of π bonds, or of a π bond and a lone pair, "
      "in a conjugated system. It is a permanent effect transmitted through the π system. Groups with a lone pair "
      "on the atom joined to the ring (halogens, –OH, –OR, –NH₂, –NHCOR) show +R.",
      ["(a) Lone pair on N is delocalised into the ring → +R → true",
       "(b) +R of –NH₂ raises electron density at o- and p-positions → true",
       "(c) Transmission through σ bonds describes the inductive effect → false",
       "(d) Halogens: −I (electronegative) and +R (lone pairs) → true",
       "(e) That describes the electromeric effect; resonance is permanent → false"],
      why_others_wrong="Options with (c) or (e) include a property of the inductive or electromeric effect.",
      ncert=f"{NC11}, 'Organic Chemistry – Some Basic Principles and Techniques', resonance effect", seconds=60),

    Q(T_GO, "Hybridisation and functional groups", "Intermediate", "statement_pair",
      *sp("Furan is an alicyclic compound.", False,
          "Tropolone is a benzenoid aromatic compound.", False),
      "Classification of organic compounds",
      "NCERT classifies cyclic compounds as alicyclic (cyclohexane, cyclohexene, tetrahydrofuran), aromatic "
      "benzenoid (benzene and its derivatives), aromatic non-benzenoid (tropolone) and heterocyclic aromatic "
      "(furan, thiophene, pyridine).",
      ["Statement I: furan is a heterocyclic aromatic compound → false",
       "Statement II: tropolone is a non-benzenoid aromatic compound → false"],
      ncert=f"{NC11}, 'Organic Chemistry – Some Basic Principles and Techniques', classification of organic "
            "compounds", seconds=35),

    Q(T_GO, "Types of organic reactions", "Intermediate", "match_list",
      *ml("Match the reaction in List-I with its type in List-II.",
          ["CH₃CH₂Br + CN⁻ → CH₃CH₂CN + Br⁻", "C₆H₆ + Br₂ (FeBr₃) → C₆H₅Br + HBr",
           "CH₄ + Cl₂ (light) → CH₃Cl + HCl", "CH₃CHO + HCN → CH₃CH(OH)CN"],
          ["Free radical substitution", "Nucleophilic addition", "Nucleophilic substitution",
           "Electrophilic substitution"],
          {"A": "III", "B": "IV", "C": "I", "D": "II"},
          [{"A": "IV", "B": "III", "C": "I", "D": "II"}, {"A": "III", "B": "IV", "C": "II", "D": "I"},
           {"A": "III", "B": "I", "C": "IV", "D": "II"}], "B"),
      "Classifying reactions by the attacking species",
      "The type of reaction is named after the attacking species (nucleophile, electrophile or free radical) and "
      "the overall change (substitution or addition).",
      ["CN⁻ replaces Br⁻ → nucleophilic substitution → III",
       "Br⁺ (from Br₂/FeBr₃) replaces H on benzene → electrophilic substitution → IV",
       "Cl• chain reaction replaces H → free radical substitution → I",
       "CN⁻ adds to C=O → nucleophilic addition → II"],
      why_others_wrong="A-IV, B-III swaps the nucleophilic and electrophilic substitutions. C-II, D-I mixes up the "
                       "radical chlorination and the cyanohydrin formation.",
      ncert=f"{NC11}, 'Organic Chemistry – Some Basic Principles and Techniques', types of organic reactions",
      seconds=50),

    Q(T_GO, "Electronic effects", "Intermediate", "assertion_reason",
      *ar("The ethyl carbocation, CH₃CH₂⁺, is more stable than the methyl carbocation, CH₃⁺.", True,
          "In CH₃CH₂⁺, the σ electrons of the C–H bonds of the methyl group are partly delocalised into the vacant "
          "p orbital of the positive carbon (hyperconjugation).", True, explains=True),
      "Hyperconjugation and carbocation stability",
      "Delocalisation of C–H σ electrons into the empty p orbital spreads the positive charge. CH₃⁺ has no "
      "adjacent C–H bonds to do this.",
      ["A: CH₃CH₂⁺ (1°) is more stable than CH₃⁺ → true",
       "R: three C–H bonds next to C⁺ overlap with its empty p orbital → true",
       "This charge dispersal is the cause of the greater stability → R explains A"],
      ncert=f"{NC11}, 'Organic Chemistry – Some Basic Principles and Techniques', hyperconjugation", seconds=40),

    Q(T_GO, "Electronic effects", "Advanced", "direct",
      "Which of the following does NOT show hyperconjugation involving C–H bonds?",
      ["CH₃–CH=CH₂", "CH₃CH₂⁺", "(CH₃)₃C–CH=CH₂", "(CH₃)₂CH⁺"], "C",
      "Requirement for hyperconjugation",
      "Hyperconjugation needs a C–H bond on the saturated carbon directly attached to the unsaturated carbon or the "
      "carbon with the vacant p orbital (an α-hydrogen).",
      ["CH₃–CH=CH₂: three α-H → yes", "CH₃CH₂⁺: three α-H → yes", "(CH₃)₂CH⁺: six α-H → yes",
       "(CH₃)₃C–CH=CH₂: the carbon attached to C=C is quaternary, so it has no α-H → no"],
      why_others_wrong="Each of the other species has C–H bonds on the carbon next to the π bond or the positive "
                       "carbon. The C–H bonds of the tert-butyl group in option C are one carbon too far away.",
      ncert=f"{NC11}, 'Organic Chemistry – Some Basic Principles and Techniques', hyperconjugation", seconds=50),

    Q(T_GO, "IUPAC nomenclature", "Advanced", "multi_statement",
      *ms("Which of the following IUPAC names are correct?",
          [("(CH₃)₂CH–CH(CH₃)₂: 2,3-dimethylbutane", True),
           ("CH₃CH₂–CH(CH₃)–CH(CH₃)–CH₂CH₃: 3,4-dimethylhexane", True),
           ("CH₂=CH–CH₂–OH: prop-2-en-1-ol", True),
           ("CH₃–CO–CH₂–CH₂–CH₃: pentan-4-one", False),
           ("Cl–CH₂–CH₂–CH₂–OH: 3-chloropropan-1-ol", True)],
          [["a", "b", "c"], ["a", "c", "d", "e"], ["b", "c", "d", "e"]], "A"),
      "Applying IUPAC rules",
      "Choose the longest chain, give the principal functional group the lowest locant, and cite halogens as "
      "prefixes.",
      ["(a) Butane chain with methyls at C-2 and C-3 → true",
       "(b) Six-carbon chain with methyls at C-3 and C-4 → true",
       "(c) –OH is principal (C-1), double bond at C-2 → prop-2-en-1-ol → true",
       "(d) Numbering must give C=O the lower locant → pentan-2-one → false",
       "(e) –OH at C-1, chloro at C-3 → 3-chloropropan-1-ol → true"],
      why_others_wrong="(a), (b) and (c) only leaves out the correct name (e); the other two options include the "
                       "wrong name (d).",
      ncert=f"{NC11}, 'Organic Chemistry – Some Basic Principles and Techniques', IUPAC nomenclature", seconds=70),

    Q(T_GO, "Electronic effects", "Advanced", "assertion_reason",
      *ar("The –OCH₃ group activates the benzene ring towards electrophilic substitution, although oxygen is more "
          "electronegative than carbon.", True,
          "For an –OCH₃ group attached to a benzene ring, the −I effect outweighs the +R effect.", False),
      "Competition between inductive and resonance effects",
      "The oxygen of –OCH₃ withdraws electrons through the σ bond (−I) but donates its lone pair into the ring (+R). "
      "For –OCH₃, –OH and –NH₂, the +R effect dominates, so the ring becomes more electron-rich (activated) at the "
      "ortho and para positions. For halogens, −I dominates.",
      ["A: anisole undergoes electrophilic substitution faster than benzene → true",
       "R: for –OCH₃ the +R effect is stronger than the −I effect → R as written is false"],
      ncert=f"{NC11}, 'Organic Chemistry – Some Basic Principles and Techniques', electronic displacements; "
            f"{NC11}, 'Hydrocarbons', directive influence of functional groups", seconds=50),

    Q(T_GO, "Electronic effects", "Advanced", "statement_pair",
      *sp("In the addition of H⁺ to an alkene, the π electrons are transferred to the carbon atom to which H⁺ gets "
          "attached; this is a +E (electromeric) effect.", True,
          "In the addition of CN⁻ to a carbonyl group, the π electrons shift towards the carbon atom to which CN⁻ "
          "gets attached; this is also a +E effect.", False),
      "The +E and −E electromeric effects",
      "In the +E effect the π electrons move to the atom to which the attacking reagent becomes bonded; in the −E "
      "effect they move to the other atom. An electrophile such as H⁺ takes the π pair (+E). A nucleophile such as "
      "CN⁻ brings its own pair, so the π electrons of C=O move to oxygen (−E).",
      ["Statement I: H⁺ bonds to the carbon that receives the π pair → +E → true",
       "Statement II: the π pair moves to O, away from the carbon attacked by CN⁻ → −E → false"],
      ncert=f"{NC11}, 'Organic Chemistry – Some Basic Principles and Techniques', electromeric effect", seconds=55),

    N(T_GO, "Hybridisation and functional groups", "Advanced",
      "In how many of the following molecules are all the carbon atoms in the same state of hybridisation?\n"
      "Benzene, ethyne, propene, buta-1,3-diene, propyne, cyclohexane, ethanenitrile (CH₃CN), propa-1,2-diene "
      "(CH₂=C=CH₂)",
      ["5", "3", "6", "4"], "D", "4",
      "Assigning hybridisation to every carbon",
      "A carbon with four σ bonds is sp³, with one double bond sp², and with a triple bond or two double bonds sp.",
      ["Benzene: all sp² → yes", "Ethyne: both sp → yes", "Propene: sp², sp², sp³ → no",
       "Buta-1,3-diene: all sp² → yes", "Propyne: sp, sp, sp³ → no", "Cyclohexane: all sp³ → yes",
       "CH₃CN: sp³ and sp → no", "CH₂=C=CH₂: sp², sp, sp² → no", "Count = 4"],
      why_others_wrong="5 usually counts propa-1,2-diene, whose central carbon is sp. 3 misses cyclohexane. 6 also "
                       "counts molecules that contain a CH₃ group.",
      ncert=f"{NC11}, 'Organic Chemistry – Some Basic Principles and Techniques', hybridisation", seconds=70),

    Q(T_GO, "Hybridisation and functional groups", "Advanced", "direct",
      "In which of the following molecules is the C2–C3 bond the shortest?",
      ["CH₃–CH₂–CH₃", "HC≡C–C≡CH", "CH₂=CH–CH₃", "HC≡C–CH₃"], "B",
      "Effect of hybridisation on single-bond length",
      "Each C2–C3 bond here is a single bond, but the carbons forming it differ in hybridisation. The more s "
      "character in the bonding orbitals, the closer the electrons to the nuclei and the shorter the bond.",
      ["Propane C2–C3: sp³–sp³", "Propene C2–C3: sp²–sp³", "Propyne C2–C3: sp–sp³",
       "Buta-1,3-diyne C2–C3: sp–sp → most s character → shortest"],
      why_others_wrong="Each of the other molecules has at least one sp³ carbon in the C2–C3 bond, so the bond is "
                       "longer than the sp–sp bond.",
      ncert=f"{NC11}, 'Organic Chemistry – Some Basic Principles and Techniques', hybridisation and bond length",
      seconds=45),
]

# ================================================================ Hydrocarbons (677-692)
# 679: CnH2n+2 with M = 72
n_679 = (72 - 2) // 14
assert 14 * n_679 + 2 == 72 and n_679 == 5
# 682: CaC2 + 2H2O -> C2H2 + Ca(OH)2
m_cac2 = mm(Ca=1, C=2)
mass_cac2 = F(56, 10) / F(224, 10) * m_cac2
assert m_cac2 == 64 and mass_cac2 == 16 and mass_cac2 * 2 == 32 and mass_cac2 / 2 == 8
# 683: 2CH3COONa + 2H2O -> C2H6 + 2CO2 (anode) + H2 + 2NaOH (cathode)
mol_salt = F(2, 10)
anode = mol_salt / 2 + mol_salt                       # ethane + CO2
assert anode * F(224, 10) == F(672, 100)
assert mol_salt * F(224, 10) == F(448, 100) and mol_salt / 2 * F(224, 10) == F(224, 100)
assert (anode + mol_salt / 2) * F(224, 10) == F(896, 100)
# 688: C6H6 + CH3COCl -> C6H5COCH3 + HCl, 75% yield
m_benz, m_acph = mm(C=6, H=6), mm(C=8, H=8, O=1)
mass_688 = F(156, 10) / m_benz * F(75, 100) * m_acph
assert m_benz == 78 and m_acph == 120 and mass_688 == 18
assert F(156, 10) / m_benz * m_acph == 24 and mass_688 * F(75, 100) == F(135, 10) and 24 / F(75, 100) == 32
# 689: 3C2H2 -> C6H6
v_689 = F(78, 10) / m_benz * 3 * F(224, 10)
assert v_689 == F(672, 100) and F(78, 10) / m_benz * F(224, 10) == F(224, 100)
assert r2(F(78, 10) / m_benz / 3 * F(224, 10)) == 0.75 and F(78, 10) / m_benz * 2 * F(224, 10) == F(448, 100)

QUESTIONS += [
    Q(T_HC, "Alkynes", "Basic", "direct",
      "But-2-yne is reduced with sodium in liquid ammonia. The main product is:",
      ["cis-But-2-ene", "Butane", "But-1-ene", "trans-But-2-ene"], "D",
      "Partial reduction of alkynes",
      "NCERT: alkynes are reduced by sodium in liquid ammonia to trans-alkenes, whereas Lindlar's catalyst "
      "(palladised charcoal deactivated with quinoline) gives cis-alkenes.",
      ["CH₃–C≡C–CH₃ + Na/liq. NH₃ → trans-CH₃CH=CHCH₃"],
      why_others_wrong="cis-But-2-ene is the Lindlar product. Na/liq. NH₃ stops at the alkene (no butane), and "
                       "the double bond stays where the triple bond was (no but-1-ene).",
      ncert=f"{NC11}, 'Hydrocarbons', preparation of alkenes from alkynes", seconds=25),

    Q(T_HC, "Alkenes: addition and ozonolysis", "Basic", "direct",
      "Ethanol is heated with concentrated sulphuric acid at 443 K. The main organic product is:",
      ["Ethene", "Ethoxyethane", "Ethanal", "Ethane"], "A",
      "Acidic dehydration of alcohols",
      "Alcohols lose a molecule of water when heated with concentrated H₂SO₄, giving alkenes. At 443 K ethanol "
      "gives ethene.",
      ["CH₃CH₂OH → (conc. H₂SO₄, 443 K) → CH₂=CH₂ + H₂O"],
      why_others_wrong="Ethoxyethane is formed at the lower temperature of 413 K with excess alcohol. Ethanal "
                       "needs an oxidising agent, and ethane needs a reducing agent.",
      ncert=f"{NC11}, 'Hydrocarbons', preparation of alkenes (from alcohols by acidic dehydration)", seconds=20),

    N(T_HC, "Alkanes and conformations", "Basic",
      "An open-chain alkane has a molar mass of 72 g mol⁻¹. Its molecular formula is (C = 12, H = 1):",
      ["C₆H₁₄", "C₅H₁₀", "C₄H₁₀", "C₅H₁₂"], "D", "C₅H₁₂",
      "General formula of alkanes",
      "Open-chain alkanes have the formula CₙH₂ₙ₊₂, so the molar mass is 14n + 2.",
      ["14n + 2 = 72", "n = 5 → C₅H₁₂"],
      why_others_wrong="C₆H₁₄ has mass 86 and C₄H₁₀ has 58. C₅H₁₀ (mass 70) fits CₙH₂ₙ, the formula of alkenes "
                       "and cycloalkanes.",
      ncert=f"{NC11}, 'Hydrocarbons', alkanes", seconds=25),

    Q(T_HC, "Alkenes: addition and ozonolysis", "Basic", "statement_pair",
      *sp("Vicinal dihalides give alkenes when heated with zinc metal.", True,
          "Alkyl halides give alkenes when heated with alcoholic potash (dehydrohalogenation).", True),
      "Preparation of alkenes",
      "Removal of two halogen atoms from adjacent carbons (dehalogenation, with Zn) or of HX from an alkyl halide "
      "(β-elimination, with alcoholic KOH) both create a C=C bond.",
      ["Statement I: CH₂Br–CH₂Br + Zn → CH₂=CH₂ + ZnBr₂ → true",
       "Statement II: CH₃CH₂Br + KOH (alc.) → CH₂=CH₂ + KBr + H₂O → true"],
      ncert=f"{NC11}, 'Hydrocarbons', preparation of alkenes", seconds=30),

    Q(T_HC, "Alkenes: addition and ozonolysis", "Basic", "assertion_reason",
      *ar("Alkenes undergo electrophilic addition reactions.", True,
          "Alkenes are insoluble in water.", True, explains=False),
      "Reactivity of alkenes",
      "Alkenes are a rich source of loosely held π electrons, which attract electrophiles; this is why they "
      "undergo electrophilic addition. Their insolubility in water is a physical property due to their non-polar "
      "nature and has nothing to do with this reactivity.",
      ["A: e.g. CH₂=CH₂ + HBr → CH₃CH₂Br → true",
       "R: alkenes are non-polar and insoluble in water → true",
       "R does not explain A (the π electrons do)"],
      ncert=f"{NC11}, 'Hydrocarbons', alkenes (physical and chemical properties)", seconds=30),

    N(T_HC, "Alkynes", "Intermediate",
      "The minimum mass of calcium carbide needed to produce 5.6 L of ethyne, measured at STP, by the action of "
      "water is (Ca = 40, C = 12; molar volume at STP = 22.4 L mol⁻¹):",
      ["16 g", "32 g", "8 g", "64 g"], "A", "16 g",
      "Preparation of ethyne from calcium carbide",
      "CaC₂ + 2H₂O → Ca(OH)₂ + C₂H₂. One mole of carbide gives one mole of ethyne.",
      ["n(C₂H₂) = 5.6/22.4 = 0.25 mol", "n(CaC₂) = 0.25 mol",
       "Mass = 0.25 × 64 = 16 g"],
      why_others_wrong="32 g assumes two carbide units per ethyne. 8 g assumes two ethyne per carbide. 64 g is the "
                       "mass of a full mole.",
      ncert=f"{NC11}, 'Hydrocarbons', preparation of alkynes (from calcium carbide)", seconds=45),

    N(T_HC, "Alkanes and conformations", "Intermediate",
      "A solution containing 0.2 mol of sodium ethanoate is electrolysed completely by Kolbe's method:\n"
      "2CH₃COONa + 2H₂O → C₂H₆ + 2CO₂ + H₂ + 2NaOH\n"
      "The total volume of gases released at the anode, measured at STP, is (molar volume = 22.4 L mol⁻¹):",
      ["4.48 L", "2.24 L", "6.72 L", "8.96 L"], "C", "6.72 L",
      "Products at each electrode in Kolbe's electrolysis",
      "The carboxylate ions are discharged at the anode: 2CH₃COO⁻ → C₂H₆ + 2CO₂ + 2e⁻. Hydrogen is formed at the "
      "cathode.",
      ["Anode: 0.1 mol C₂H₆ + 0.2 mol CO₂ = 0.3 mol", "Volume = 0.3 × 22.4 = 6.72 L",
       "(0.1 mol H₂ is released at the cathode)"],
      why_others_wrong="4.48 L counts only CO₂, and 2.24 L only ethane. 8.96 L adds the hydrogen formed at the "
                       "cathode.",
      ncert=f"{NC11}, 'Hydrocarbons', preparation of alkanes (Kolbe's electrolytic method)", seconds=60),

    Q(T_HC, "Electrophilic substitution", "Intermediate", "direct",
      "In the Friedel–Crafts acylation of benzene with ethanoyl chloride and anhydrous AlCl₃, the electrophile that "
      "attacks the ring is:",
      ["CH₃⁺", "CH₃CO⁺", "Cl⁺", "AlCl₄⁻"], "B",
      "Generation of electrophiles in aromatic substitution",
      "The Lewis acid AlCl₃ removes Cl⁻ from the acyl chloride, producing the acylium ion, which is the attacking "
      "electrophile.",
      ["CH₃COCl + AlCl₃ → CH₃CO⁺ + AlCl₄⁻", "CH₃CO⁺ attacks benzene → acetophenone after loss of H⁺"],
      why_others_wrong="CH₃⁺ is the electrophile in alkylation with CH₃Cl. Cl⁺ is the electrophile in "
                       "chlorination. AlCl₄⁻ is an anion and cannot be an electrophile.",
      ncert=f"{NC11}, 'Hydrocarbons', mechanism of electrophilic substitution", seconds=30),

    Q(T_HC, "Alkenes: addition and ozonolysis", "Intermediate", "multi_statement",
      *ms("Which of the following statements about alkenes are correct?",
          [("Alkenes are called olefins because ethylene gives an oily liquid with chlorine.", True),
           ("Ethene is a planar molecule.", True),
           ("Propene, CH₃–CH=CH₂, shows geometrical isomerism.", False),
           ("Acidified KMnO₄ oxidises but-2-ene to ethanoic acid.", True),
           ("Alkenes are less reactive than alkanes because the π bond is stronger than a σ bond.", False)],
          [["a", "b", "c"], ["b", "d", "e"], ["a", "c", "d"]], "D"),
      "Structure and reactions of alkenes",
      "Geometrical isomerism needs two different groups on each doubly bonded carbon; =CH₂ has two identical "
      "hydrogens. The π bond is weaker than the σ bond, which makes alkenes more reactive than alkanes.",
      ["(a) Origin of the name 'olefin' (oil forming) → true",
       "(b) Both carbons sp², all six atoms in one plane → true",
       "(c) C-1 of propene carries two H atoms → no cis/trans → false",
       "(d) CH₃CH=CHCH₃ + acidified KMnO₄ → 2CH₃COOH → true",
       "(e) The π bond is weaker; alkenes are more reactive → false"],
      why_others_wrong="Every option other than (a), (b) and (d) contains (c) or (e).",
      ncert=f"{NC11}, 'Hydrocarbons', alkenes (structure, isomerism and chemical properties)", seconds=60),

    Q(T_HC, "Alkanes and conformations", "Intermediate", "match_list",
      *ml("Match the reaction of an alkane in List-I with its main product in List-II.",
          ["CH₄ + O₂ (Cu, 523 K, 100 atm)", "CH₄ + O₂ (Mo₂O₃, heat)", "(CH₃)₃CH + KMnO₄",
           "n-Hexane (Cr₂O₃ on alumina, 773 K, 10–20 atm)"],
          ["Benzene", "Methanal", "Methanol", "2-Methylpropan-2-ol"],
          {"A": "III", "B": "II", "C": "IV", "D": "I"},
          [{"A": "II", "B": "III", "C": "IV", "D": "I"}, {"A": "III", "B": "II", "C": "I", "D": "IV"},
           {"A": "IV", "B": "II", "C": "III", "D": "I"}], "A"),
      "Controlled oxidation and aromatisation of alkanes",
      "Under controlled conditions alkanes are oxidised to alcohols or aldehydes rather than burnt. Alkanes with "
      "six or more carbons cyclise and dehydrogenate to arenes over oxide catalysts.",
      ["2CH₄ + O₂ → 2CH₃OH (Cu, 523 K, 100 atm) → III", "CH₄ + O₂ → HCHO + H₂O (Mo₂O₃) → II",
       "(CH₃)₃CH → (CH₃)₃COH (KMnO₄) → IV", "n-C₆H₁₄ → C₆H₆ + 4H₂ (aromatisation) → I"],
      why_others_wrong="A-II, B-III swaps the two catalysts for methane. C-I, D-IV swaps oxidation of isobutane and "
                       "aromatisation of hexane.",
      ncert=f"{NC11}, 'Hydrocarbons', chemical properties of alkanes (controlled oxidation, aromatisation)",
      seconds=50),

    Q(T_HC, "Alkanes and conformations", "Intermediate", "statement_pair",
      *sp("In free radical halogenation of alkanes, the reactivity of the halogens is I₂ > Br₂ > Cl₂ > F₂.", False,
          "Iodination of alkanes is very slow and reversible, so it is carried out in the presence of an oxidising "
          "agent such as HIO₃ or HNO₃.", True),
      "Halogenation of alkanes",
      "NCERT gives the order of reactivity F₂ > Cl₂ > Br₂ > I₂. Fluorination is too violent to control, and "
      "iodination is reversible because the HI formed reduces the alkyl iodide; an oxidant removes the HI.",
      ["Statement I: the order is reversed → false", "Statement II: as stated in NCERT → true"],
      ncert=f"{NC11}, 'Hydrocarbons', chemical properties of alkanes (halogenation)", seconds=40),

    N(T_HC, "Electrophilic substitution", "Advanced",
      "15.6 g of benzene is treated with excess ethanoyl chloride in the presence of anhydrous AlCl₃. If the yield "
      "of acetophenone is 75%, its mass is (C = 12, H = 1, O = 16):",
      ["24.0 g", "18.0 g", "32.0 g", "13.5 g"], "B", "18.0 g",
      "Yield in Friedel–Crafts acylation",
      "One mole of benzene gives one mole of acetophenone, C₆H₅COCH₃ (molar mass 120 g mol⁻¹).",
      ["n(C₆H₆) = 15.6/78 = 0.2 mol", "Theoretical mass = 0.2 × 120 = 24.0 g",
       "Actual mass = 0.75 × 24.0 = 18.0 g"],
      why_others_wrong="24.0 g ignores the yield. 32.0 g divides by 0.75 instead of multiplying. 13.5 g applies "
                       "the 75% factor twice.",
      ncert=f"{NC11}, 'Hydrocarbons', electrophilic substitution (Friedel–Crafts acylation)", seconds=60),

    N(T_HC, "Benzene and aromaticity", "Advanced",
      "Ethyne passed through a red-hot iron tube at 873 K trimerises to benzene. The minimum volume of ethyne, "
      "measured at STP, needed to obtain 7.8 g of benzene is (C = 12, H = 1; molar volume = 22.4 L mol⁻¹):",
      ["2.24 L", "4.48 L", "0.75 L", "6.72 L"], "D", "6.72 L",
      "Cyclic polymerisation of ethyne",
      "3C₂H₂ → C₆H₆: three moles of ethyne give one mole of benzene.",
      ["n(C₆H₆) = 7.8/78 = 0.1 mol", "n(C₂H₂) = 3 × 0.1 = 0.3 mol", "V = 0.3 × 22.4 = 6.72 L"],
      why_others_wrong="2.24 L assumes a 1 : 1 ratio and 4.48 L a 2 : 1 ratio. 0.75 L divides by 3 instead of "
                       "multiplying.",
      ncert=f"{NC11}, 'Hydrocarbons', preparation of benzene (cyclic polymerisation of ethyne)", seconds=50),

    Q(T_HC, "Electrophilic substitution", "Advanced", "multi_statement",
      *ms("Which of the following statements about electrophilic substitution in benzene derivatives are correct?",
          [("Nitration of nitrobenzene gives mainly m-dinitrobenzene.", True),
           ("Chlorination of toluene with Cl₂ and anhydrous FeCl₃ in the dark gives mainly o- and p-chlorotoluene.",
            True),
           ("Benzene reacts with ethanoic anhydride in the presence of anhydrous AlCl₃ to give acetophenone.", True),
           ("The –CHO group directs an incoming electrophile to the ortho and para positions.", False),
           ("The –OCH₃ group directs an incoming electrophile to the meta position.", False)],
          [["a", "b", "d"], ["b", "c", "e"], ["a", "c", "d", "e"]], "C"),
      "Directive influence of substituents",
      "Electron-withdrawing groups (–NO₂, –CHO, –COOH, –CN) deactivate the ring and direct meta. Alkyl groups and "
      "groups with lone pairs on the attached atom (–OH, –OCH₃, –NH₂) direct ortho and para.",
      ["(a) –NO₂ is meta directing → true", "(b) –CH₃ is o/p directing → true",
       "(c) Acylation works with acyl chlorides or anhydrides → true",
       "(d) –CHO is meta directing → false", "(e) –OCH₃ is o/p directing → false"],
      why_others_wrong="Every option other than (a), (b) and (c) includes (d) or (e) or leaves out a true "
                       "statement.",
      ncert=f"{NC11}, 'Hydrocarbons', directive influence of a functional group in monosubstituted benzene",
      seconds=60),

    Q(T_HC, "Alkenes: addition and ozonolysis", "Advanced", "assertion_reason",
      *ar("Addition of HBr to propene in the absence of peroxide gives 2-bromopropane as the major product.", True,
          "Protonation of propene at C-1 gives a secondary carbocation, which is more stable than the primary "
          "carbocation formed by protonation at C-2.", True, explains=True),
      "Mechanism behind Markovnikov's rule",
      "The electrophile H⁺ can add to either carbon of the double bond. Addition to C-1 gives CH₃–C⁺H–CH₃ (2°); "
      "addition to C-2 gives CH₃CH₂CH₂⁺ (1°). The more stable 2° carbocation forms faster and is attacked by Br⁻.",
      ["A: CH₃CH=CH₂ + HBr → CH₃CHBrCH₃ (major) → true",
       "R: 2° carbocation is more stable than 1° → true",
       "The product is decided by the more stable carbocation → R explains A"],
      ncert=f"{NC11}, 'Hydrocarbons', addition of hydrogen halides (mechanism)", seconds=45),

    Q(T_HC, "Alkenes: addition and ozonolysis", "Advanced", "direct",
      "An alkene of formula C₅H₁₀ on ozonolysis (O₃, then Zn/H₂O) gives methanal and butan-2-one. The alkene is:",
      ["Pent-1-ene", "2-Methylbut-2-ene", "2-Methylbut-1-ene", "3-Methylbut-1-ene"], "C",
      "Locating a double bond from ozonolysis products",
      "Join the two carbonyl carbons by a double bond after removing their oxygen atoms.",
      ["HCHO → CH₂=", "CH₃COCH₂CH₃ → =C(CH₃)CH₂CH₃", "Alkene: CH₂=C(CH₃)–CH₂–CH₃ = 2-methylbut-1-ene"],
      why_others_wrong="Pent-1-ene gives methanal and butanal. 2-Methylbut-2-ene gives propanone and ethanal. "
                       "3-Methylbut-1-ene gives methanal and 2-methylpropanal.",
      ncert=f"{NC11}, 'Hydrocarbons', ozonolysis of alkenes", seconds=60),
]

# ================================================================ Organic Compounds Containing Halogens (693-702)
# 696: 3C2H5OH + PBr3 -> 3C2H5Br + H3PO3
m_pbr3 = mm(P=1, Br=3)
mass_pbr3 = F(46, 10) / mm(C=2, H=6, O=1) / 3 * m_pbr3
assert m_pbr3 == 271 and r2(mass_pbr3) == 9.03 and F(1, 10) * m_pbr3 == F(271, 10)
assert F(1, 100) * m_pbr3 == F(271, 100) and F(5, 100) * m_pbr3 == F(1355, 100)
# 697: 2CHCl3 + O2 -> 2COCl2 + 2HCl
m_chcl3, m_cocl2 = mm(C=1, H=1, Cl=3), mm(C=1, O=1, Cl=2)
mol_697 = F(239, 10) / m_chcl3
assert m_chcl3 == F(1195, 10) and m_cocl2 == 99 and mol_697 == F(2, 10)
assert mol_697 * m_cocl2 == F(198, 10) and mol_697 / 2 * m_cocl2 == F(99, 10) and mol_697 * 2 * m_cocl2 == F(396, 10)
assert mol_697 * mm(H=1, Cl=1) == F(73, 10)
# 700: Wurtz on CH3Br + C2H5Br -> R-R' for every pair (with repetition)
_alkyl = {"CH3": 1, "C2H5": 2}
_alkanes = {a + b for a in _alkyl.values() for b in _alkyl.values()}
assert _alkanes == {2, 3, 4} and len(_alkanes) == 3

QUESTIONS += [
    Q(T_HX, "Polyhalogen compounds", "Basic", "direct",
      "Freon 12, one of the most common freons in industrial use, has the formula:",
      ["CCl₃F", "CHClF₂", "CCl₂F₂", "CF₄"], "C",
      "Freons",
      "Freons are chlorofluorocarbon compounds of methane and ethane. Freon 12 is dichlorodifluoromethane, made "
      "from tetrachloromethane by the Swarts reaction.",
      ["Freon 12 = CCl₂F₂ (dichlorodifluoromethane)"],
      why_others_wrong="CCl₃F is a different freon (Freon 11). CHClF₂ is the refrigerant R-22 made from chloroform. "
                       "CF₄ contains no chlorine and is not Freon 12.",
      ncert=f"{NC12}, 'Haloalkanes and Haloarenes', polyhalogen compounds (freons)", seconds=20),

    Q(T_HX, "Polyhalogen compounds", "Basic", "statement_pair",
      *sp("Chloroform was once used as a general anaesthetic in surgery but has been replaced by less toxic, safer "
          "anaesthetics such as ether.", True,
          "Carbon tetrachloride released into the air rises to the upper atmosphere and depletes the ozone layer.",
          True),
      "Uses and environmental effects of polyhalogen compounds",
      "Both statements are given in NCERT's account of trichloromethane and tetrachloromethane.",
      ["Statement I: chloroform's past use as an anaesthetic → true",
       "Statement II: CCl₄ contributes to ozone depletion → true"],
      ncert=f"{NC12}, 'Haloalkanes and Haloarenes', polyhalogen compounds", seconds=30),

    Q(T_HX, "C-X bond and preparation", "Basic", "match_list",
      *ml("Match the compound in List-I with its class in List-II.",
          ["CH₂=CH–CH₂Cl", "C₆H₅CH₂Cl", "CH₂=CHCl", "C₆H₅Cl"],
          ["Aryl halide", "Vinylic halide", "Benzylic halide", "Allylic halide"],
          {"A": "IV", "B": "III", "C": "II", "D": "I"},
          [{"A": "II", "B": "III", "C": "IV", "D": "I"}, {"A": "IV", "B": "I", "C": "II", "D": "III"},
           {"A": "IV", "B": "III", "C": "I", "D": "II"}], "B"),
      "Classification of halogen compounds by the carbon bearing the halogen",
      "The class depends on the carbon to which X is bonded: an sp³ carbon next to C=C (allylic) or next to a "
      "benzene ring (benzylic), an sp² carbon of C=C (vinylic) or a ring carbon of benzene (aryl).",
      ["CH₂=CH–CH₂Cl → allylic → IV", "C₆H₅CH₂Cl → benzylic → III", "CH₂=CHCl → vinylic → II",
       "C₆H₅Cl → aryl → I"],
      why_others_wrong="A-II, C-IV swaps allylic and vinylic. B-I, D-III swaps benzylic and aryl. C-I, D-II calls "
                       "chlorobenzene vinylic.",
      ncert=f"{NC12}, 'Haloalkanes and Haloarenes', classification", seconds=35),

    N(T_HX, "C-X bond and preparation", "Intermediate",
      "Bromoethane is prepared from ethanol and phosphorus tribromide:\n"
      "3C₂H₅OH + PBr₃ → 3C₂H₅Br + H₃PO₃\n"
      "The minimum mass of PBr₃ needed to convert 4.6 g of ethanol completely is (C = 12, H = 1, O = 16, P = 31, "
      "Br = 80):",
      ["27.1 g", "2.71 g", "13.55 g", "9.03 g"], "D", "9.03 g",
      "Stoichiometry of the PBr₃ method",
      "One mole of PBr₃ converts three moles of alcohol.",
      ["n(C₂H₅OH) = 4.6/46 = 0.1 mol", "n(PBr₃) = 0.1/3 mol", "Molar mass of PBr₃ = 31 + 240 = 271 g mol⁻¹",
       "Mass = (0.1/3) × 271 = 9.03 g"],
      why_others_wrong="27.1 g assumes a 1 : 1 ratio. 13.55 g assumes a 2 : 1 ratio. 2.71 g uses 0.01 mol of PBr₃.",
      ncert=f"{NC12}, 'Haloalkanes and Haloarenes', preparation of haloalkanes from alcohols", seconds=55),

    N(T_HX, "Polyhalogen compounds", "Intermediate",
      "Chloroform is slowly oxidised by air in light:\n"
      "2CHCl₃ + O₂ → 2COCl₂ + 2HCl\n"
      "The mass of phosgene formed from 23.9 g of chloroform, assuming complete oxidation, is (C = 12, H = 1, "
      "O = 16, Cl = 35.5):",
      ["9.9 g", "19.8 g", "39.6 g", "7.3 g"], "B", "19.8 g",
      "Oxidation of chloroform to phosgene",
      "Chloroform and phosgene are formed and consumed in a 1 : 1 mole ratio.",
      ["Molar mass of CHCl₃ = 12 + 1 + 106.5 = 119.5 g mol⁻¹", "n = 23.9/119.5 = 0.2 mol",
       "Molar mass of COCl₂ = 12 + 16 + 71 = 99 g mol⁻¹", "Mass = 0.2 × 99 = 19.8 g"],
      why_others_wrong="9.9 g halves the ratio and 39.6 g doubles it. 7.3 g is the mass of HCl formed.",
      ncert=f"{NC12}, 'Haloalkanes and Haloarenes', trichloromethane", seconds=50),

    Q(T_HX, "C-X bond and preparation", "Intermediate", "assertion_reason",
      *ar("Grignard reagents must be prepared and handled under strictly anhydrous conditions.", True,
          "Grignard reagents react with any source of protons, including water, to give hydrocarbons.", True,
          explains=True),
      "Reactivity of Grignard reagents",
      "The carbon of the C–Mg bond is strongly basic. Even traces of moisture destroy the reagent.",
      ["A: dry ether and dry apparatus are used → true", "R: RMgX + H₂O → RH + Mg(OH)X → true",
       "The reaction with water is why moisture must be excluded → R explains A"],
      ncert=f"{NC12}, 'Haloalkanes and Haloarenes', reaction with metals (Grignard reagents)", seconds=35),

    Q(T_HX, "Polyhalogen compounds", "Intermediate", "multi_statement",
      *ms("Which of the following statements about polyhalogen compounds are correct?",
          [("Dichloromethane is used as a paint remover and as a solvent.", True),
           ("The major use of chloroform today is in the production of the freon refrigerant R-22.", True),
           ("Carbon tetrachloride is used in the manufacture of refrigerants and propellants for aerosol cans.",
            True),
           ("Dichloromethane does not affect the human central nervous system.", False),
           ("Freons are highly reactive and toxic compounds.", False)],
          [["a", "b", "d"], ["b", "c", "e"], ["a", "c", "d", "e"]], "A"),
      "Uses and effects of polyhalogen compounds",
      "NCERT notes that methylene chloride harms the human central nervous system, and that freons are extremely "
      "stable, unreactive, non-toxic, non-corrosive and easily liquefiable gases.",
      ["(a) True", "(b) True", "(c) True", "(d) Dichloromethane harms the CNS → false",
       "(e) Freons are unreactive and non-toxic → false"],
      why_others_wrong="Every other option contains (d) or (e).",
      ncert=f"{NC12}, 'Haloalkanes and Haloarenes', polyhalogen compounds", seconds=50),

    N(T_HX, "C-X bond and preparation", "Advanced",
      "A mixture of bromomethane and bromoethane is heated with sodium in dry ether (Wurtz reaction). How many "
      "different alkanes can be formed?",
      ["1", "2", "3", "4"], "C", "3",
      "Wurtz reaction with two different alkyl halides",
      "In the Wurtz reaction any two alkyl groups can couple. With two different halides, both like and unlike "
      "pairs combine.",
      ["CH₃ + CH₃ → ethane", "CH₃ + C₂H₅ → propane", "C₂H₅ + C₂H₅ → butane", "3 alkanes"],
      why_others_wrong="1 assumes only the cross product forms. 2 counts only the symmetrical products. 4 counts "
                       "CH₃–C₂H₅ and C₂H₅–CH₃ as different compounds.",
      ncert=f"{NC12}, 'Haloalkanes and Haloarenes', reactions with metals (Wurtz reaction)", seconds=45),

    Q(T_HX, "C-X bond and preparation", "Advanced", "assertion_reason",
      *ar("2-Bromo-2-methylpropane has a higher boiling point than its isomer 1-bromobutane.", False,
          "Branching decreases the surface area of a molecule, so the van der Waals forces become weaker.", True),
      "Boiling points of isomeric haloalkanes",
      "For isomeric haloalkanes the boiling point falls as branching increases: 1-bromobutane (375 K) > "
      "2-bromobutane (364 K) > 2-bromo-2-methylpropane (346 K).",
      ["A: the branched isomer has the lower boiling point → false",
       "R: a more spherical molecule has a smaller contact area → weaker attractions → true"],
      ncert=f"{NC12}, 'Haloalkanes and Haloarenes', physical properties (boiling points)", seconds=40),

    Q(T_HX, "C-X bond and preparation", "Advanced", "statement_pair",
      *sp("Of the three isomeric dichlorobenzenes, the para isomer has the lowest melting point.", False,
          "The boiling points of the isomeric dichlorobenzenes differ widely from one another.", False),
      "Melting and boiling points of dihalobenzenes",
      "NCERT: the boiling points of isomeric dihalobenzenes are very nearly the same, but the para isomers have "
      "high melting points because their symmetry lets them fit better in the crystal lattice.",
      ["Statement I: p-dichlorobenzene has the highest melting point → false",
       "Statement II: their boiling points are nearly the same → false"],
      ncert=f"{NC12}, 'Haloalkanes and Haloarenes', physical properties (melting and boiling points)", seconds=40),
]

# ================================================================ Organic Compounds Containing Oxygen (703-720)
m_etoh, m_acoh, m_ethanal = mm(C=2, H=6, O=1), mm(C=2, H=4, O=2), mm(C=2, H=4, O=1)
assert (m_etoh, m_acoh, m_ethanal) == (46, 60, 44)
# 705: C2H5OH -> CH3COOH (1 : 1)
assert F(46, 10) / m_etoh * m_acoh == 6 and F(46, 10) / m_etoh * m_ethanal == F(44, 10)
assert F(46, 10) / m_etoh * m_acoh / 2 == 3 and F(46, 10) / m_etoh * m_acoh * 2 == 12
# 709: RCOOH + NaHCO3 -> RCOONa + CO2 + H2O (1 : 1); CnH2n+1COOH has M = 14n + 46
mol_co2_709 = F(112, 100) / F(224, 10)
m_acid_709 = F(37, 10) / mol_co2_709
n_709 = (m_acid_709 - 46) / 14
assert mol_co2_709 == F(5, 100) and m_acid_709 == 74 and n_709 == 2          # C2H5COOH
# 710: 2CH3CHO -> CH3CH(OH)CH2CHO (aldol, M 88); dehydration product but-2-enal M 70
m_aldol, m_crot = mm(C=4, H=8, O=2), mm(C=4, H=6, O=1)
mass_710 = F(88, 10) / m_ethanal / 2 * m_aldol
assert m_aldol == 88 and m_crot == 70 and mass_710 == F(88, 10)
assert F(88, 10) / m_ethanal * m_aldol == F(176, 10) and F(88, 10) / m_ethanal / 2 * m_crot == 7
# 716: ROH + CH3MgI -> CH4 + Mg(OR)I ; CnH2n+2O has M = 14n + 18
mol_ch4 = F(112, 1) / 22400
m_alc_716 = F(37, 100) / mol_ch4
assert mol_ch4 == F(5, 1000) and m_alc_716 == 74 and (m_alc_716 - 18) / 14 == 4
# 717: CH3CHO -> CH3CH(OH)CN -> CH3CH(OH)COOH
m_cyanohydrin, m_lactic = mm(C=3, H=5, N=1, O=1), mm(C=3, H=6, O=3)
mol_717 = F(44, 10) / m_ethanal
assert m_cyanohydrin == 71 and m_lactic == 90 and mol_717 * m_lactic == 9 and mol_717 * m_cyanohydrin == F(71, 10)
assert mol_717 * 2 * m_lactic == 18

QUESTIONS += [
    Q(T_OX, "Alcohols", "Basic", "direct",
      "Today, most of the methanol produced industrially is made by:",
      ["Destructive distillation of wood", "Catalytic hydrogenation of carbon monoxide",
       "Fermentation of sugars with yeast", "Acid-catalysed hydration of ethene"], "B",
      "Industrial preparation of methanol",
      "Methanol ('wood spirit') was once obtained by destructive distillation of wood. NCERT states that today "
      "most methanol is produced by catalytic hydrogenation of carbon monoxide at high pressure and temperature "
      "over a ZnO–Cr₂O₃ catalyst.",
      ["CO + 2H₂ → CH₃OH (ZnO–Cr₂O₃, 200–300 atm, 573–673 K)"],
      why_others_wrong="Destructive distillation of wood is the old source. Fermentation gives ethanol, and "
                       "hydration of ethene also gives ethanol.",
      ncert=f"{NC12}, 'Alcohols, Phenols and Ethers', some commercially important alcohols (methanol)",
      seconds=20),

    Q(T_OX, "Ethers", "Basic", "direct",
      "Ethanol is heated with concentrated sulphuric acid at 413 K, keeping the alcohol in excess. The main "
      "organic product is:",
      ["Ethene", "Ethanal", "Ethoxyethane", "Ethanoic acid"], "C",
      "Preparation of ethers by dehydration of alcohols",
      "At 413 K, a protonated alcohol molecule is attacked by a second alcohol molecule (SN2), giving a symmetrical "
      "ether. At the higher temperature of 443 K, elimination to ethene dominates.",
      ["2CH₃CH₂OH → (conc. H₂SO₄, 413 K) → C₂H₅–O–C₂H₅ + H₂O"],
      why_others_wrong="Ethene is formed at 443 K. Ethanal and ethanoic acid need an oxidising agent.",
      ncert=f"{NC12}, 'Alcohols, Phenols and Ethers', preparation of ethers (dehydration of alcohols)",
      seconds=25),

    N(T_OX, "Alcohols", "Basic",
      "4.6 g of ethanol is oxidised completely to ethanoic acid by acidified potassium dichromate. The mass of "
      "ethanoic acid formed is (C = 12, H = 1, O = 16):",
      ["4.4 g", "3.0 g", "12.0 g", "6.0 g"], "D", "6.0 g",
      "Oxidation of a primary alcohol to a carboxylic acid",
      "A strong oxidising agent converts a primary alcohol, through the aldehyde, into the carboxylic acid with "
      "the same number of carbon atoms (1 : 1 in moles).",
      ["n(C₂H₅OH) = 4.6/46 = 0.1 mol", "n(CH₃COOH) = 0.1 mol", "Mass = 0.1 × 60 = 6.0 g"],
      why_others_wrong="4.4 g is the mass of ethanal (the intermediate). 3.0 g and 12.0 g use ratios of 2 : 1 and "
                       "1 : 2.",
      ncert=f"{NC12}, 'Alcohols, Phenols and Ethers', chemical reactions of alcohols (oxidation)", seconds=30),

    Q(T_OX, "Alcohols", "Basic", "statement_pair",
      *sp("The boiling points of alcohols increase with an increase in the number of carbon atoms.", True,
          "Among isomeric alcohols, the boiling point increases with increased branching of the carbon chain.",
          False),
      "Boiling points of alcohols",
      "Larger molecules have stronger van der Waals forces, so boiling points rise along the series. Branching "
      "reduces the surface area and so lowers the boiling point.",
      ["Statement I: true (NCERT)",
       "Statement II: branching decreases the boiling point, e.g. butan-1-ol > 2-methylpropan-2-ol → false"],
      ncert=f"{NC12}, 'Alcohols, Phenols and Ethers', physical properties (boiling points)", seconds=30),

    Q(T_OX, "Carboxylic acids", "Basic", "direct",
      "Ethanoic acid reacts with chlorine in the presence of a small amount of red phosphorus to give "
      "chloroethanoic acid. This reaction is known as the:",
      ["Kolbe reaction", "Rosenmund reduction", "Etard reaction", "Hell–Volhard–Zelinsky reaction"], "D",
      "α-Halogenation of carboxylic acids",
      "Carboxylic acids with an α-hydrogen are halogenated at the α-carbon by Cl₂ or Br₂ with a little red "
      "phosphorus; this is the Hell–Volhard–Zelinsky (HVZ) reaction.",
      ["CH₃COOH + Cl₂ → (red P) → ClCH₂COOH + HCl"],
      why_others_wrong="The Kolbe reaction makes salicylic acid from phenoxide and CO₂. Rosenmund reduction turns "
                       "acyl chlorides into aldehydes. The Etard reaction oxidises toluene to benzaldehyde.",
      ncert=f"{NC12}, 'Aldehydes, Ketones and Carboxylic Acids', reactions of carboxylic acids (HVZ reaction)",
      seconds=20),

    Q(T_OX, "Phenols", "Basic", "match_list",
      *ml("Match the common name in List-I with the IUPAC name in List-II.",
          ["Catechol", "Resorcinol", "Quinol (hydroquinone)", "o-Cresol"],
          ["Benzene-1,4-diol", "2-Methylphenol", "Benzene-1,2-diol", "Benzene-1,3-diol"],
          {"A": "III", "B": "IV", "C": "I", "D": "II"},
          [{"A": "IV", "B": "III", "C": "I", "D": "II"}, {"A": "III", "B": "I", "C": "IV", "D": "II"},
           {"A": "I", "B": "IV", "C": "III", "D": "II"}], "C"),
      "Nomenclature of phenols",
      "NCERT gives the common names of the dihydroxybenzenes and the methylphenols (cresols).",
      ["Catechol = 1,2-dihydroxybenzene → III", "Resorcinol = 1,3- → IV", "Quinol = 1,4- → I",
       "o-Cresol = 2-methylphenol → II"],
      why_others_wrong="A-IV, B-III swaps catechol and resorcinol. B-I, C-IV swaps resorcinol and quinol. A-I, C-III "
                       "swaps catechol and quinol.",
      ncert=f"{NC12}, 'Alcohols, Phenols and Ethers', nomenclature (phenols)", seconds=35),

    N(T_OX, "Carboxylic acids", "Intermediate",
      "3.7 g of a saturated monocarboxylic acid reacts completely with sodium hydrogencarbonate solution and "
      "liberates 1.12 L of CO₂ measured at STP. The acid is (C = 12, H = 1, O = 16; molar volume = 22.4 L mol⁻¹):",
      ["Propanoic acid", "Ethanoic acid", "Butanoic acid", "Methanoic acid"], "A", "Propanoic acid",
      "Molar mass of an acid from CO₂ evolved with NaHCO₃",
      "RCOOH + NaHCO₃ → RCOONa + H₂O + CO₂: one mole of a monocarboxylic acid gives one mole of CO₂.",
      ["n(CO₂) = 1.12/22.4 = 0.05 mol = n(acid)", "Molar mass = 3.7/0.05 = 74 g mol⁻¹",
       "CₙH₂ₙ₊₁COOH: 14n + 46 = 74 → n = 2 → C₂H₅COOH = propanoic acid"],
      why_others_wrong="Methanoic (46), ethanoic (60) and butanoic (88 g mol⁻¹) acids do not have molar mass 74; "
                       "taking two CO₂ per acid would give 148, which matches none of them either.",
      ncert=f"{NC12}, 'Aldehydes, Ketones and Carboxylic Acids', reactions of carboxylic acids with "
            "hydrogencarbonates", seconds=55),

    N(T_OX, "Aldehydes and ketones", "Intermediate",
      "8.8 g of ethanal is converted completely by dilute NaOH into the aldol, 3-hydroxybutanal. The mass of aldol "
      "formed is (C = 12, H = 1, O = 16):",
      ["17.6 g", "8.8 g", "4.4 g", "7.0 g"], "B", "8.8 g",
      "Stoichiometry of the aldol reaction",
      "Two molecules of ethanal combine without losing any atoms: 2CH₃CHO → CH₃CH(OH)CH₂CHO. The mass is "
      "therefore conserved.",
      ["n(CH₃CHO) = 8.8/44 = 0.2 mol", "n(aldol) = 0.1 mol", "Mass = 0.1 × 88 = 8.8 g"],
      why_others_wrong="17.6 g takes one aldol per ethanal. 4.4 g halves the mass. 7.0 g is the mass of but-2-enal, "
                       "formed only if the aldol is dehydrated on heating.",
      ncert=f"{NC12}, 'Aldehydes, Ketones and Carboxylic Acids', aldol condensation", seconds=50),

    Q(T_OX, "Phenols", "Intermediate", "direct",
      "Phenol is treated with bromine in carbon disulphide (CS₂) at low temperature. The main product is:",
      ["2,4,6-Tribromophenol", "m-Bromophenol", "Bromobenzene", "A mixture of o-bromophenol and p-bromophenol"],
      "D",
      "Effect of solvent on bromination of phenol",
      "In a solvent of low polarity such as CS₂ or CHCl₃ at low temperature, phenol gives monobromophenols. With "
      "bromine water, the ring is so strongly activated that 2,4,6-tribromophenol is formed.",
      ["–OH is o/p directing", "Low polarity solvent, low temperature → monosubstitution",
       "Products: o-bromophenol and p-bromophenol"],
      why_others_wrong="2,4,6-Tribromophenol forms with bromine water. –OH does not direct meta. The C–O bond of "
                       "phenol is not replaced by bromine.",
      ncert=f"{NC12}, 'Alcohols, Phenols and Ethers', electrophilic substitution in phenols (halogenation)",
      seconds=35),

    Q(T_OX, "Aldehydes and ketones", "Intermediate", "assertion_reason",
      *ar("Aldehydes are generally more reactive than ketones in nucleophilic addition reactions.", True,
          "The +I effect of the two alkyl groups in a ketone increases the electrophilicity of the carbonyl "
          "carbon.", False),
      "Relative reactivity of aldehydes and ketones",
      "Two alkyl groups in a ketone hinder the approach of the nucleophile (steric effect) and, by their +I effect, "
      "reduce the positive character of the carbonyl carbon. Both effects make ketones less reactive.",
      ["A: e.g. ethanal reacts faster than propanone → true",
       "R: the +I effect decreases, not increases, the electrophilicity → false"],
      ncert=f"{NC12}, 'Aldehydes, Ketones and Carboxylic Acids', nucleophilic addition (reactivity)", seconds=40),

    Q(T_OX, "Ethers", "Intermediate", "multi_statement",
      *ms("Which of the following statements about ethers are correct?",
          [("The alkoxy group of anisole directs electrophiles to the ortho and para positions.", True),
           ("Anisole reacts with bromine in ethanoic acid, even without FeBr₃, to give mainly p-bromoanisole.",
            True),
           ("Methyl tert-butyl ether reacts with HI to give methanol and tert-butyl iodide.", True),
           ("Williamson synthesis with a tertiary alkyl halide and sodium methoxide gives a good yield of the "
            "ether.", False),
           ("Diethyl ether reacts with sodium metal to liberate hydrogen.", False)],
          [["a", "b", "d"], ["b", "c", "e"], ["a", "c", "d", "e"]], "A"),
      "Reactions of ethers",
      "The –OR group activates the ring and directs o/p. With HI, a tertiary alkyl group leaves as a stable "
      "carbocation (SN1), so iodide ends up on the tertiary carbon. A tertiary halide with an alkoxide undergoes "
      "elimination. Ethers have no O–H bond, so sodium does not react.",
      ["(a) +R of –OCH₃ → o/p directing → true", "(b) p-bromoanisole is the main product → true",
       "(c) (CH₃)₃C–O–CH₃ + HI → CH₃OH + (CH₃)₃C–I → true",
       "(d) The alkoxide acts as a base; the alkene is formed → false",
       "(e) No acidic hydrogen → no reaction with Na → false"],
      why_others_wrong="Every other option contains (d) or (e), or leaves out a true statement.",
      ncert=f"{NC12}, 'Alcohols, Phenols and Ethers', preparation and chemical reactions of ethers", seconds=60),

    Q(T_OX, "Alcohols", "Intermediate", "match_list",
      *ml("Each compound in List-I is treated with CH₃MgBr and the product is hydrolysed. Match it with the final "
          "organic product in List-II.",
          ["CH₃CHO", "HCHO", "CH₃COCH₃", "CO₂"],
          ["Ethanoic acid", "2-Methylpropan-2-ol", "Ethanol", "Propan-2-ol"],
          {"A": "IV", "B": "III", "C": "II", "D": "I"},
          [{"A": "III", "B": "IV", "C": "II", "D": "I"}, {"A": "IV", "B": "III", "C": "I", "D": "II"},
           {"A": "II", "B": "III", "C": "IV", "D": "I"}], "A"),
      "Grignard reagents with carbonyl compounds and CO₂",
      "CH₃⁻ of the Grignard reagent adds to the carbonyl carbon. Methanal gives a primary alcohol, other aldehydes "
      "secondary alcohols, ketones tertiary alcohols, and CO₂ a carboxylic acid.",
      ["CH₃CHO → CH₃CH(OH)CH₃ (propan-2-ol) → IV", "HCHO → CH₃CH₂OH (ethanol) → III",
       "CH₃COCH₃ → (CH₃)₃COH → II", "CO₂ → CH₃COOH → I"],
      why_others_wrong="A-III, B-IV swaps the products of ethanal and methanal. C-I, D-II gives the acid to the "
                       "ketone. A-II, C-IV swaps the secondary and tertiary alcohols.",
      ncert=f"{NC12}, 'Alcohols, Phenols and Ethers', preparation of alcohols from Grignard reagents; "
            f"{NC12}, 'Aldehydes, Ketones and Carboxylic Acids', preparation of carboxylic acids", seconds=50),

    Q(T_OX, "Carboxylic acids", "Intermediate", "statement_pair",
      *sp("Electron-donating groups increase the acidity of carboxylic acids.", False,
          "Benzoic acid is a stronger acid than ethanoic acid.", True),
      "Effect of substituents on acidity of carboxylic acids",
      "Electron-withdrawing groups stabilise the carboxylate anion and increase acidity; electron-donating groups "
      "destabilise it and decrease acidity. Benzoic acid (pKa 4.19) is stronger than ethanoic acid (pKa 4.76).",
      ["Statement I: electron-donating groups decrease acidity → false",
       "Statement II: pKa 4.19 < 4.76 → benzoic acid is stronger → true"],
      ncert=f"{NC12}, 'Aldehydes, Ketones and Carboxylic Acids', acidity of carboxylic acids", seconds=40),

    N(T_OX, "Alcohols", "Advanced",
      "0.37 g of a saturated monohydric alcohol reacts with excess methylmagnesium iodide and gives 112 mL of "
      "methane measured at STP. The molecular formula of the alcohol is (C = 12, H = 1, O = 16; molar volume at "
      "STP = 22400 mL):",
      ["C₃H₈O", "C₄H₁₀O", "C₅H₁₂O", "C₂H₆O"], "B", "C₄H₁₀O",
      "Molar mass from the reaction of an alcohol with a Grignard reagent",
      "A Grignard reagent takes the acidic hydrogen of the –OH group: ROH + CH₃MgI → CH₄ + Mg(OR)I. One mole of a "
      "monohydric alcohol gives one mole of methane.",
      ["n(CH₄) = 112/22400 = 0.005 mol = n(alcohol)", "Molar mass = 0.37/0.005 = 74 g mol⁻¹",
       "CₙH₂ₙ₊₂O: 14n + 18 = 74 → n = 4 → C₄H₁₀O"],
      why_others_wrong="C₃H₈O (60), C₅H₁₂O (88) and C₂H₆O (46 g mol⁻¹) do not have molar mass 74.",
      ncert=f"{NC12}, 'Haloalkanes and Haloarenes', Grignard reagents (reaction with proton sources)",
      seconds=70),

    N(T_OX, "Aldehydes and ketones", "Advanced",
      "4.4 g of ethanal is converted into its cyanohydrin with HCN, and the cyanohydrin is hydrolysed completely "
      "with dilute acid to 2-hydroxypropanoic acid (lactic acid). Assuming complete conversion in both steps, the "
      "mass of lactic acid formed is (C = 12, H = 1, N = 14, O = 16):",
      ["9.0 g", "7.1 g", "4.4 g", "18.0 g"], "A", "9.0 g",
      "Two-step synthesis through a cyanohydrin",
      "HCN adds to C=O to give CH₃CH(OH)CN; acid hydrolysis converts –CN into –COOH. Each step is 1 : 1 in moles.",
      ["n(CH₃CHO) = 4.4/44 = 0.1 mol", "CH₃CH(OH)CN (71 g mol⁻¹) → CH₃CH(OH)COOH (90 g mol⁻¹)",
       "Mass of lactic acid = 0.1 × 90 = 9.0 g"],
      why_others_wrong="7.1 g is the mass of the cyanohydrin, before hydrolysis. 4.4 g assumes no change in mass. "
                       "18.0 g doubles the amount.",
      ncert=f"{NC12}, 'Aldehydes, Ketones and Carboxylic Acids', nucleophilic addition of HCN; preparation of "
            "carboxylic acids from nitriles", seconds=70),

    Q(T_OX, "Carboxylic acids", "Advanced", "direct",
      "An ester X (C₄H₈O₂) is hydrolysed to a carboxylic acid Y and an alcohol Z. Oxidation of Z with acidified "
      "dichromate gives Y. X is:",
      ["Methyl propanoate", "Propyl methanoate", "Ethyl ethanoate", "Isopropyl methanoate"], "C",
      "Identifying an ester from its hydrolysis products",
      "A primary alcohol is oxidised to the acid with the same number of carbon atoms. If Z gives Y, the acid and "
      "alcohol parts of the ester have the same carbon count, i.e. two carbons each in C₄H₈O₂.",
      ["X = CH₃COOC₂H₅", "Hydrolysis → CH₃COOH (Y) + C₂H₅OH (Z)", "C₂H₅OH → CH₃COOH (= Y)"],
      why_others_wrong="Methyl propanoate gives methanol, which oxidises to methanoic acid, not propanoic acid. "
                       "Propyl methanoate gives propan-1-ol, which oxidises to propanoic acid, not methanoic acid. "
                       "Isopropyl methanoate gives propan-2-ol, which oxidises to propanone.",
      ncert=f"{NC12}, 'Aldehydes, Ketones and Carboxylic Acids', esters; oxidation of alcohols", seconds=60),

    Q(T_OX, "Aldehydes and ketones", "Advanced", "multi_statement",
      *ms("Which of the following statements about aldol and related reactions are correct?",
          [("Methanal and benzaldehyde cannot undergo aldol condensation by themselves.", True),
           ("A cross aldol reaction between ethanal and propanal gives a mixture of four products.", True),
           ("Ketones that have α-hydrogen atoms do not undergo aldol condensation.", False),
           ("Benzaldehyde condenses with acetophenone in dilute alkali to give an α,β-unsaturated ketone "
            "(Claisen–Schmidt condensation).", True),
           ("Aldehydes that have α-hydrogen atoms undergo the Cannizzaro reaction with concentrated alkali.",
            False)],
          [["a", "b", "c"], ["a", "c", "d"], ["b", "d", "e"]], "B"),
      "Aldol, cross aldol and Cannizzaro reactions",
      "Aldol condensation needs at least one α-hydrogen; aldehydes and ketones with α-H both react. With two "
      "different enolisable aldehydes, each can act as donor and acceptor, giving four products. Aldehydes without "
      "α-H undergo the Cannizzaro reaction.",
      ["(a) HCHO and C₆H₅CHO have no α-H → true", "(b) 2 donors × 2 acceptors = 4 products → true",
       "(c) e.g. propanone gives 4-hydroxy-4-methylpentan-2-one → false",
       "(d) C₆H₅CHO + C₆H₅COCH₃ → C₆H₅CH=CHCOC₆H₅ → true",
       "(e) Cannizzaro is for aldehydes without α-H → false"],
      why_others_wrong="(a), (b) and (c) includes the false (c); the other options contain (c) or (e).",
      ncert=f"{NC12}, 'Aldehydes, Ketones and Carboxylic Acids', aldol, cross aldol and Cannizzaro reactions",
      seconds=70),

    Q(T_OX, "Aldehydes and ketones", "Advanced", "assertion_reason",
      *ar("Propanal has a higher boiling point than propan-1-ol.", False,
          "Aldehydes show dipole–dipole interactions but cannot form intermolecular hydrogen bonds as alcohols "
          "do.", True),
      "Boiling points of aldehydes compared with alcohols",
      "Aldehydes and ketones boil higher than hydrocarbons and ethers of comparable mass (dipole–dipole forces) "
      "but lower than alcohols, which are associated through hydrogen bonds.",
      ["A: propanal (b.p. about 322 K) boils below propan-1-ol (about 370 K) → false",
       "R: no O–H bond in aldehydes → no intermolecular H-bonding → true"],
      ncert=f"{NC12}, 'Aldehydes, Ketones and Carboxylic Acids', physical properties", seconds=40),
]

# ================================================================ Organic Compounds Containing Nitrogen (721-730)
m_aniline, m_acetanilide = mm(C=6, H=7, N=1), mm(C=8, H=9, N=1, O=1)
mass_724 = F(93, 10) / m_aniline * m_acetanilide
assert m_aniline == 93 and m_acetanilide == 135 and mass_724 == F(135, 10) and mass_724 / 2 == F(675, 100) and mass_724 * 2 == 27
# 725: carbylamine test is given only by primary amines
_amines = {"CH3NH2": 1, "(CH3)2NH": 2, "C6H5NH2": 1, "(CH3)3N": 3, "C6H5CH2NH2": 1, "C6H5NHCH3": 2}
assert sum(1 for d in _amines.values() if d == 1) == 3
# 728: RNH2 + HNO2 -> ROH + N2 + H2O ; CnH2n+1NH2 has M = 14n + 17
mol_n2 = F(224, 22400)
m_amine = F(59, 100) / mol_n2
assert mol_n2 == F(1, 100) and m_amine == 59 and (m_amine - 17) / 14 == 3

QUESTIONS += [
    Q(T_NI, "Amines: basicity and identification", "Basic", "direct",
      "Ethanenitrile, CH₃CN, is reduced with lithium aluminium hydride. The product is:",
      ["Methanamine", "Ethanamide", "Ethanamine", "N-Methylmethanamine"], "C",
      "Reduction of nitriles",
      "Nitriles are reduced by LiAlH₄ (or by catalytic hydrogenation) to primary amines with the same number of "
      "carbon atoms: R–C≡N → R–CH₂–NH₂.",
      ["CH₃–C≡N + 4[H] → CH₃–CH₂–NH₂ (ethanamine)"],
      why_others_wrong="Methanamine has one carbon fewer (that is a Hofmann-type result). Ethanamide is formed by "
                       "partial hydrolysis, not reduction. A secondary amine is not formed.",
      ncert=f"{NC12}, 'Amines', preparation of amines (reduction of nitriles)", seconds=20),

    Q(T_NI, "Amines: basicity and identification", "Basic", "direct",
      "Freshly distilled aniline is colourless, but on storage it gradually becomes coloured. This is due to:",
      ["Absorption of moisture from the air", "Atmospheric oxidation", "Polymerisation by light into a dye",
       "Reaction with carbon dioxide of the air"], "B",
      "Physical properties of aniline",
      "NCERT notes that pure amines are colourless, but aryl amines such as aniline become coloured on storage "
      "because of atmospheric oxidation.",
      ["Aniline is easily oxidised; air slowly converts it into coloured products"],
      why_others_wrong="Moisture or CO₂ does not give coloured products, and the colour is not due to "
                       "polymerisation into a dye.",
      ncert=f"{NC12}, 'Amines', physical properties", seconds=20),

    Q(T_NI, "Amines: basicity and identification", "Basic", "statement_pair",
      *sp("In the ammonolysis of an alkyl halide, the primary amine is obtained as the main product if a large "
          "excess of ammonia is used.", True,
          "The lower aliphatic amines are gases with a fishy odour.", True),
      "Preparation and properties of amines",
      "With excess ammonia, the alkyl halide is more likely to meet NH₃ than the amine already formed, so further "
      "alkylation is suppressed. NCERT describes the lower aliphatic amines as gases with a fishy odour.",
      ["Statement I: true (NCERT)", "Statement II: true (NCERT)"],
      ncert=f"{NC12}, 'Amines', preparation (ammonolysis) and physical properties", seconds=30),

    N(T_NI, "Amines: basicity and identification", "Intermediate",
      "9.3 g of aniline is acetylated completely with ethanoic anhydride. The mass of acetanilide formed is "
      "(C = 12, H = 1, N = 14, O = 16):",
      ["9.3 g", "27.0 g", "13.5 g", "6.75 g"], "C", "13.5 g",
      "Acylation of aniline",
      "C₆H₅NH₂ + (CH₃CO)₂O → C₆H₅NHCOCH₃ + CH₃COOH: one mole of aniline gives one mole of acetanilide.",
      ["n(aniline) = 9.3/93 = 0.1 mol", "Molar mass of C₆H₅NHCOCH₃ = 135 g mol⁻¹", "Mass = 0.1 × 135 = 13.5 g"],
      why_others_wrong="9.3 g ignores the added acetyl group. 6.75 g halves the amount and 27.0 g doubles it.",
      ncert=f"{NC12}, 'Amines', chemical reactions (acylation)", seconds=40),

    N(T_NI, "Amines: basicity and identification", "Intermediate",
      "How many of the following give the carbylamine (isocyanide) test?\n"
      "CH₃NH₂, (CH₃)₂NH, C₆H₅NH₂, (CH₃)₃N, C₆H₅CH₂NH₂, C₆H₅NHCH₃",
      ["2", "4", "6", "3"], "D", "3",
      "Carbylamine test for primary amines",
      "Only primary amines (aliphatic or aromatic) give a foul-smelling isocyanide when heated with chloroform "
      "and ethanolic KOH. Secondary and tertiary amines do not.",
      ["Primary: CH₃NH₂, C₆H₅NH₂, C₆H₅CH₂NH₂ → 3",
       "Secondary: (CH₃)₂NH, C₆H₅NHCH₃; tertiary: (CH₃)₃N → no test"],
      why_others_wrong="2 usually leaves out benzylamine, which is a primary amine. 4 wrongly includes "
                       "N-methylaniline (secondary). 6 counts every amine.",
      ncert=f"{NC12}, 'Amines', chemical reactions (carbylamine reaction)", seconds=45),

    Q(T_NI, "Amines: basicity and identification", "Intermediate", "assertion_reason",
      *ar("Tertiary amines have higher boiling points than isomeric primary amines.", False,
          "Tertiary amines have no hydrogen atom on nitrogen, so they cannot form intermolecular hydrogen bonds.",
          True),
      "Boiling points of isomeric amines",
      "Primary amines have two N–H hydrogens available for hydrogen bonding, secondary amines one and tertiary "
      "amines none. Hence the boiling points of isomeric amines follow primary > secondary > tertiary.",
      ["A: tertiary amines boil lowest → false", "R: no N–H → no intermolecular H-bonding → true"],
      ncert=f"{NC12}, 'Amines', physical properties (boiling points)", seconds=35),

    Q(T_NI, "Amines: basicity and identification", "Intermediate", "match_list",
      *ml("Match the method of preparing amines in List-I with its characteristic in List-II.",
          ["Gabriel phthalimide synthesis", "Hofmann bromamide degradation", "Reduction of a nitrile",
           "Ammonolysis of an alkyl halide"],
          ["Gives a mixture of 1°, 2° and 3° amines and a quaternary ammonium salt",
           "Gives a primary amine with one carbon atom fewer than the amide",
           "Gives only primary aliphatic amines; not used for aromatic amines",
           "Gives a primary amine with one carbon atom more than the alkyl halide used to make the nitrile"],
          {"A": "III", "B": "II", "C": "IV", "D": "I"},
          [{"A": "II", "B": "III", "C": "IV", "D": "I"}, {"A": "III", "B": "IV", "C": "II", "D": "I"},
           {"A": "I", "B": "II", "C": "IV", "D": "III"}], "C"),
      "Methods of preparing amines",
      "Each method has a characteristic feature that NCERT highlights.",
      ["Gabriel: 1° aliphatic only (aryl halides do not react with phthalimide anion) → III",
       "Hofmann: RCONH₂ → RNH₂, one carbon lost → II",
       "R–X → R–CN → R–CH₂NH₂: one carbon added (ascent of series) → IV",
       "Ammonolysis: mixture of amines and quaternary salt → I"],
      why_others_wrong="A-II, B-III swaps the Gabriel and Hofmann methods. B-IV, C-II swaps the step-down and "
                       "step-up methods. A-I, D-III swaps the Gabriel synthesis and ammonolysis.",
      ncert=f"{NC12}, 'Amines', preparation of amines", seconds=55),

    N(T_NI, "Amines: basicity and identification", "Advanced",
      "0.59 g of a saturated aliphatic primary amine, CₙH₂ₙ₊₁NH₂, reacts completely with nitrous acid and "
      "liberates 224 mL of nitrogen measured at STP. The amine is (C = 12, H = 1, N = 14; molar volume at STP = "
      "22400 mL):",
      ["Propan-1-amine", "Ethanamine", "Butan-1-amine", "Methanamine"], "A", "Propan-1-amine",
      "Quantitative evolution of nitrogen from primary aliphatic amines",
      "Aliphatic primary amines react with nitrous acid through unstable diazonium salts, giving the alcohol and "
      "one mole of N₂ per mole of amine. NCERT notes that this quantitative evolution of N₂ is used in estimating "
      "amino acids and proteins.",
      ["RNH₂ + HNO₂ → ROH + N₂ + H₂O", "n(N₂) = 224/22400 = 0.01 mol = n(amine)",
       "Molar mass = 0.59/0.01 = 59 g mol⁻¹", "14n + 17 = 59 → n = 3 → C₃H₇NH₂"],
      why_others_wrong="Methanamine (31), ethanamine (45) and butan-1-amine (73 g mol⁻¹) do not have molar mass 59.",
      ncert=f"{NC12}, 'Amines', reaction with nitrous acid", seconds=70),

    Q(T_NI, "Amines: basicity and identification", "Advanced", "direct",
      "Which of the following is the weakest base?",
      ["Aniline", "p-Toluidine (4-methylaniline)", "N-Methylaniline", "p-Nitroaniline"], "D",
      "Effect of ring substituents on the basicity of arylamines",
      "Electron-releasing groups such as –CH₃ increase the basic strength of aniline; electron-withdrawing groups "
      "such as –NO₂ decrease it. A p-nitro group withdraws the nitrogen lone pair by both −I and −R effects.",
      ["p-NO₂: strongly withdraws electron density from –NH₂ → lone pair least available",
       "p-CH₃ and N-CH₃: electron-releasing → slightly stronger bases than aniline"],
      why_others_wrong="Aniline is a stronger base than p-nitroaniline, and the methyl-substituted anilines are "
                       "stronger still.",
      ncert=f"{NC12}, 'Amines', basic character (arylamines)", seconds=40),

    Q(T_NI, "Diazonium salts", "Advanced", "multi_statement",
      *ms("Which of the following statements about arenediazonium salts are correct?",
          [("Benzenediazonium chloride is a colourless crystalline solid that is readily soluble in water.", True),
           ("Benzenediazonium fluoroborate is insoluble in water and is stable at room temperature.", True),
           ("Replacement of the diazo group by –Cl using CuCl/HCl is the Sandmeyer reaction.", True),
           ("Diazotisation of aniline is carried out above 300 K for the best yield.", False),
           ("Nitrogen is retained in the product in every reaction of diazonium salts.", False)],
          [["a", "b", "d"], ["a", "c", "e"], ["b", "c", "e"]], "B"),
      "Properties and reactions of diazonium salts",
      "Diazonium salts are prepared at 273–278 K because they decompose on warming. In most of their reactions "
      "N₂ is lost (replacement reactions); in coupling reactions nitrogen is retained.",
      ["(a) True (NCERT)", "(b) True (NCERT)", "(c) True: Cu(I) salts → Sandmeyer reaction",
       "(d) Carried out at 273–278 K → false",
       "(e) Replacement reactions lose N₂; only coupling retains it → false"],
      why_others_wrong="Every option other than (a), (b) and (c) contains (d) or (e).",
      ncert=f"{NC12}, 'Amines', diazonium salts (preparation, properties and reactions)", seconds=60),
]

# ================================================================ Biomolecules (Chemistry) (731-740)
# 733: n amino acids in a chain are joined by n - 1 peptide bonds
assert 5 - 1 == 4
# 734: C12H22O11 + H2O -> C6H12O6 (glucose) + C6H12O6 (fructose)
m_sucrose, m_glucose = mm(C=12, H=22, O=11), mm(C=6, H=12, O=6)
mol_734 = F(342, 10) / m_sucrose
assert m_sucrose == 342 and m_glucose == 180 and mol_734 * m_glucose == 18 and mol_734 * 2 * m_glucose == 36
assert mol_734 / 2 * m_glucose == 9
# 739: in the pyranose ring of glucose, C1 (anomeric), C2, C3, C4 and C5 carry four different groups; C6 is CH2OH
_chiral_pyranose = [c for c in range(1, 7) if c != 6]
assert len(_chiral_pyranose) == 5

QUESTIONS += [
    Q(T_BM, "Amino acids and proteins", "Basic", "direct",
      "In proteins, the α-amino acids are joined by peptide linkages. A peptide linkage is:",
      ["–CO–O–", "–O–", "–CH=N–", "–CO–NH–"], "D",
      "Peptide bond",
      "A peptide bond is an amide bond formed between the –COOH group of one amino acid and the –NH₂ group of "
      "another, with loss of a water molecule.",
      ["–COOH + H₂N– → –CO–NH– + H₂O"],
      why_others_wrong="–CO–O– is an ester linkage, –O– is the glycosidic (ether-type) linkage of carbohydrates, "
                       "and –CH=N– is an imine.",
      ncert=f"{NC12}, 'Biomolecules', structure of proteins (peptide bond)", seconds=20),

    Q(T_BM, "Carbohydrates", "Basic", "direct",
      "Amylose constitutes about what percentage of starch?",
      ["80–85%", "50%", "15–20%", "98%"], "C",
      "Composition of starch",
      "Starch is a polymer of α-glucose made of two components: amylose (water soluble, about 15–20%) and "
      "amylopectin (water insoluble, about 80–85%).",
      ["Amylose: unbranched, C1–C4 α-glycosidic links, 15–20% of starch",
       "Amylopectin: branched, 80–85% of starch"],
      why_others_wrong="80–85% is the share of amylopectin. 50% and 98% are not the NCERT values.",
      ncert=f"{NC12}, 'Biomolecules', polysaccharides (starch)", seconds=20),

    N(T_BM, "Amino acids and proteins", "Basic",
      "How many peptide bonds are present in a linear pentapeptide?",
      ["4", "5", "3", "10"], "A", "4",
      "Counting peptide bonds",
      "Each peptide bond joins two neighbouring amino acid residues, so a chain of n residues has n − 1 peptide "
      "bonds.",
      ["Pentapeptide: n = 5", "Peptide bonds = 5 − 1 = 4"],
      why_others_wrong="5 counts one bond per residue. 3 subtracts two. 10 counts all pairs of residues, not only "
                       "neighbours.",
      ncert=f"{NC12}, 'Biomolecules', proteins (peptides)", seconds=20),

    N(T_BM, "Carbohydrates", "Intermediate",
      "34.2 g of sucrose is hydrolysed completely with dilute acid. The mass of glucose formed is (C = 12, H = 1, "
      "O = 16):",
      ["36.0 g", "34.2 g", "9.0 g", "18.0 g"], "D", "18.0 g",
      "Hydrolysis of sucrose",
      "C₁₂H₂₂O₁₁ + H₂O → C₆H₁₂O₆ (glucose) + C₆H₁₂O₆ (fructose). One mole of sucrose gives one mole of glucose "
      "and one mole of fructose.",
      ["n(sucrose) = 34.2/342 = 0.1 mol", "n(glucose) = 0.1 mol", "Mass = 0.1 × 180 = 18.0 g"],
      why_others_wrong="36.0 g is the combined mass of glucose and fructose. 34.2 g assumes no change in mass. "
                       "9.0 g halves the amount of glucose.",
      ncert=f"{NC12}, 'Biomolecules', disaccharides (sucrose)", seconds=40),

    Q(T_BM, "Amino acids and proteins", "Intermediate", "statement_pair",
      *sp("A dipeptide contains two peptide bonds.", False,
          "In nucleic acids, nucleotides are joined by glycosidic linkages between the sugar units.", False),
      "Peptides and the nucleic acid backbone",
      "A dipeptide is formed from two amino acids joined by one peptide bond. In nucleic acids, nucleotides are "
      "joined by phosphodiester linkages between the 5′ and 3′ carbon atoms of the pentose sugars.",
      ["Statement I: two residues → one peptide bond → false",
       "Statement II: the linkage is a phosphodiester, not a glycosidic linkage → false"],
      ncert=f"{NC12}, 'Biomolecules', proteins; structure of nucleic acids", seconds=35),

    Q(T_BM, "Amino acids and proteins", "Intermediate", "match_list",
      *ml("Match the level of protein structure in List-I with its description in List-II.",
          ["Primary structure", "Secondary structure", "Tertiary structure", "Quaternary structure"],
          ["α-helix and β-pleated sheet arrangements of the chain",
           "Spatial arrangement of two or more polypeptide subunits",
           "Sequence of amino acids in the polypeptide chain",
           "Overall folding of the chain, giving fibrous or globular shapes"],
          {"A": "III", "B": "I", "C": "IV", "D": "II"},
          [{"A": "I", "B": "III", "C": "IV", "D": "II"}, {"A": "III", "B": "I", "C": "II", "D": "IV"},
           {"A": "III", "B": "IV", "C": "I", "D": "II"}], "C"),
      "Levels of protein structure",
      "NCERT describes four levels. A change in the amino acid sequence changes the primary structure; hydrogen "
      "bonds within the backbone give the secondary structure; further folding gives the tertiary structure; "
      "association of subunits gives the quaternary structure.",
      ["Primary → sequence → III", "Secondary → α-helix, β-sheet → I",
       "Tertiary → overall folding (fibrous/globular) → IV", "Quaternary → arrangement of subunits → II"],
      why_others_wrong="A-I, B-III swaps the primary and secondary levels. C-II, D-IV swaps the tertiary and "
                       "quaternary levels. B-IV, C-I swaps the secondary and tertiary levels.",
      ncert=f"{NC12}, 'Biomolecules', structure of proteins", seconds=40),

    Q(T_BM, "Vitamins", "Intermediate", "assertion_reason",
      *ar("Vitamin C must be supplied regularly in the diet.", True,
          "Water-soluble vitamins are readily excreted in urine and cannot be stored in the body (vitamin B₁₂ "
          "excepted).", True, explains=True),
      "Water-soluble vitamins",
      "Vitamin C is water soluble. Because such vitamins are not stored and are lost in urine, a regular intake is "
      "needed.",
      ["A: true (NCERT)", "R: true (NCERT)", "Vitamin C belongs to this group → R explains A"],
      ncert=f"{NC12}, 'Biomolecules', vitamins (classification)", seconds=35),

    Q(T_BM, "Amino acids and proteins", "Advanced", "multi_statement",
      *ms("Which of the following statements about amino acids are correct?",
          [("Amino acids are classified as acidic, basic or neutral according to the relative numbers of amino and "
            "carboxyl groups in their molecules.", True),
           ("Lysine, which has two amino groups and one carboxyl group, is a basic amino acid.", True),
           ("Amino acids are usually colourless, crystalline, high-melting solids.", True),
           ("Amino acids that can be synthesised in the body are called essential amino acids.", False),
           ("Proteins are polymers of β-amino acids.", False)],
          [["a", "b", "d"], ["b", "c", "e"], ["a", "c", "d", "e"]], "A"),
      "Classification and properties of amino acids",
      "Amino acids exist as zwitterions and so behave like salts (high melting, crystalline). Those that the body "
      "can make are non-essential; those that must come from the diet are essential. Proteins are made of "
      "α-amino acids.",
      ["(a) True (NCERT)", "(b) More amino than carboxyl groups → basic → true", "(c) True (NCERT)",
       "(d) These are the non-essential amino acids → false", "(e) Proteins contain α-amino acids → false"],
      why_others_wrong="Every option other than (a), (b) and (c) contains (d) or (e).",
      ncert=f"{NC12}, 'Biomolecules', amino acids (classification and properties)", seconds=60),

    N(T_BM, "Carbohydrates", "Advanced",
      "How many chiral (asymmetric) carbon atoms are present in the six-membered cyclic (pyranose) form of "
      "α-D-glucose?",
      ["4", "5", "6", "3"], "B", "5",
      "Chiral centres in the cyclic form of glucose",
      "Open-chain glucose has four chiral carbons (C2–C5). On ring formation, the –OH at C5 adds to the C1 "
      "aldehyde group, and C1 becomes a new chiral centre (the anomeric carbon).",
      ["C1: H, OH, ring O, C2 → chiral (anomeric)", "C2, C3, C4: chiral as in the open chain",
       "C5: H, ring O, C4, CH₂OH → chiral", "C6 (CH₂OH): not chiral", "Total = 5"],
      why_others_wrong="4 is the count for the open-chain form. 6 wrongly includes the CH₂OH carbon. 3 leaves out "
                       "C1 and one more centre.",
      ncert=f"{NC12}, 'Biomolecules', cyclic structure of glucose (anomers)", seconds=60),

    Q(T_BM, "Carbohydrates", "Advanced", "direct",
      "Sucrose is a non-reducing sugar because:",
      ["It is a disaccharide with a molar mass greater than that of glucose",
       "It contains a fructose unit, and ketoses can never reduce Fehling's solution",
       "Its glucose unit has no free –OH groups",
       "The reducing groups of both glucose (C1) and fructose (C2) are used up in the glycosidic bond"], "D",
      "Reducing and non-reducing sugars",
      "A sugar reduces Fehling's or Tollens' reagent when it has a free aldehydic or ketonic group (a free anomeric "
      "carbon). In sucrose, C1 of α-D-glucose is joined to C2 of β-D-fructose, so neither unit has a free "
      "reducing group.",
      ["Sucrose: α-D-glucose C1 – O – C2 β-D-fructose", "Both anomeric carbons are tied up → non-reducing",
       "Maltose and lactose keep one free anomeric carbon → reducing"],
      why_others_wrong="Molar mass has nothing to do with reducing power. Fructose itself is a reducing sugar. The "
                       "glucose unit of sucrose still has free –OH groups at C2, C3, C4 and C6.",
      ncert=f"{NC12}, 'Biomolecules', disaccharides (sucrose)", seconds=45),
]

# ================================================================ Principles Related to Practical Chemistry (741-750)
# 744: rate doubles for every 10 K rise; time is inversely proportional to rate
t_744 = F(80) / 2 ** ((313 - 293) // 10)
assert t_744 == 20 and F(80) / 2 == 40 and F(80) / 8 == 10 and F(80) * 2 == 160
# 745: Al2(SO4)3 + K2SO4 + 24H2O -> K2SO4.Al2(SO4)3.24H2O
m_alsulf = mm(Al=2, S=3, O=12)
m_alum = mm(K=2, S=1, O=4) + m_alsulf + 24 * mm(H=2, O=1)
mol_745 = F(342, 100) / m_alsulf
assert m_alsulf == 342 and m_alum == 948 and mol_745 * m_alum == F(948, 100)
assert mol_745 * m_alum / 2 == F(474, 100) and mol_745 * m_alum * 2 == F(1896, 100)
# 748: Na2CO3 + 2HCl -> 2NaCl + H2O + CO2 (methyl orange end point)
m_na2co3 = mm(Na=2, C=1, O=3)
mmol_hcl = 80 * F(1, 10)
g_na2co3 = mmol_hcl / 2 * m_na2co3 / 1000
purity = g_na2co3 / F(53, 100) * 100
assert m_na2co3 == 106 and g_na2co3 == F(424, 1000) and purity == 80
assert mmol_hcl / 4 * m_na2co3 / 1000 / F(53, 100) * 100 == 40
assert mmol_hcl / 8 * m_na2co3 / 1000 / F(53, 100) * 100 == 20

QUESTIONS += [
    Q(T_PR, "Qualitative salt analysis", "Basic", "direct",
      "A salt is heated with sodium hydroxide solution. The gas evolved gives a brown precipitate with Nessler's "
      "reagent. The salt contains:",
      ["Na⁺", "Ca²⁺", "Zn²⁺", "NH₄⁺"], "D",
      "Test for the ammonium ion (group zero)",
      "Ammonium salts give ammonia gas when warmed with NaOH. Ammonia forms a brown precipitate with Nessler's "
      "reagent (alkaline K₂HgI₄).",
      ["NH₄⁺ + OH⁻ → NH₃↑ + H₂O", "NH₃ + Nessler's reagent → brown precipitate"],
      why_others_wrong="Na⁺, Ca²⁺ and Zn²⁺ do not release any gas when warmed with NaOH.",
      ncert=f"{LAB}, qualitative analysis (test for NH₄⁺, group zero)", seconds=20),

    Q(T_PR, "Qualitative salt analysis", "Basic", "direct",
      "In the flame test, a salt imparts an apple-green (grassy green) colour to the flame. The cation present is:",
      ["Ba²⁺", "Ca²⁺", "Sr²⁺", "K⁺"], "A",
      "Flame test for group V cations",
      "Volatile chlorides of some metals give characteristic flame colours: barium apple green, calcium brick "
      "red, strontium crimson red, potassium lilac (violet).",
      ["Apple green → barium"],
      why_others_wrong="Calcium gives brick red, strontium crimson red and potassium lilac.",
      ncert=f"{LAB}, qualitative analysis (flame test, group V)", seconds=20),

    Q(T_PR, "Titrimetric analysis", "Basic", "statement_pair",
      *sp("In titrations with potassium permanganate, the solution is acidified with dilute sulphuric acid.", True,
          "Nitric acid is preferred to sulphuric acid for acidifying permanganate titrations, because it is "
          "itself an oxidising agent.", False),
      "Choice of acid in permanganate titrations",
      "The acid used must not react with permanganate or with the substance titrated. Dilute H₂SO₄ is stable "
      "towards both. Nitric acid is avoided precisely because it is an oxidising agent and would oxidise the "
      "reducing agent being estimated.",
      ["Statement I: dilute H₂SO₄ is used → true",
       "Statement II: HNO₃ is not used, because its own oxidising action would give a wrong titre → false"],
      ncert=f"{LAB}, titrimetric analysis (redox titrations with KMnO₄)", seconds=35),

    N(T_PR, "Thermochemistry and kinetics experiments", "Intermediate",
      "In a study of the effect of temperature on the reaction between sodium thiosulphate and hydrochloric acid, "
      "the cross under the flask disappears after 80 s at 293 K. Assuming the rate doubles for every 10 K rise "
      "and that the time is inversely proportional to the rate, the time at 313 K (all concentrations unchanged) "
      "will be:",
      ["40 s", "20 s", "10 s", "160 s"], "B", "20 s",
      "Effect of temperature on reaction rate",
      "A 20 K rise is two 10 K steps, so the rate becomes 2 × 2 = 4 times; the time becomes one quarter.",
      ["Rate factor = 2^(20/10) = 4", "Time = 80/4 = 20 s"],
      why_others_wrong="40 s doubles the rate only once. 10 s uses a factor of 8 (three steps). 160 s makes the "
                       "time longer, as if the rate fell with temperature.",
      ncert=f"{LAB}, chemical kinetics (effect of temperature on the rate of reaction of thiosulphate with HCl)",
      seconds=45),

    N(T_PR, "Preparations", "Intermediate",
      "Potash alum, K₂SO₄·Al₂(SO₄)₃·24H₂O, is prepared from aluminium sulphate and potassium sulphate. The maximum "
      "mass of potash alum that can be obtained from 3.42 g of anhydrous Al₂(SO₄)₃ is (K = 39, Al = 27, S = 32, "
      "O = 16, H = 1):",
      ["4.74 g", "18.96 g", "3.42 g", "9.48 g"], "D", "9.48 g",
      "Stoichiometry of the preparation of potash alum",
      "One mole of Al₂(SO₄)₃ is present in one formula unit K₂SO₄·Al₂(SO₄)₃·24H₂O (molar mass 948 g mol⁻¹).",
      ["Molar mass of Al₂(SO₄)₃ = 54 + 96 + 192 = 342 g mol⁻¹ → n = 3.42/342 = 0.01 mol",
       "Molar mass of the alum = 174 + 342 + 432 = 948 g mol⁻¹", "Mass = 0.01 × 948 = 9.48 g"],
      why_others_wrong="4.74 g uses the formula KAl(SO₄)₂·12H₂O (474) with a 1 : 1 ratio, forgetting that each "
                       "Al₂(SO₄)₃ gives two such units. 18.96 g doubles the answer. 3.42 g ignores the added "
                       "K₂SO₄ and water.",
      ncert=f"{LAB}, preparation of inorganic compounds (potash alum)", seconds=60),

    Q(T_PR, "Detection of elements and functional groups", "Intermediate", "match_list",
      *ml("Match the functional group in List-I with an observation that detects it in List-II.",
          ["Carbon–carbon double bond", "Alcoholic –OH", "Carboxyl group", "Aldehyde group"],
          ["Silver mirror with Tollens' reagent", "Brisk effervescence with sodium hydrogencarbonate solution",
           "Decolourisation of bromine water", "Red colour with ceric ammonium nitrate"],
          {"A": "III", "B": "IV", "C": "II", "D": "I"},
          [{"A": "IV", "B": "III", "C": "II", "D": "I"}, {"A": "III", "B": "IV", "C": "I", "D": "II"},
           {"A": "III", "B": "II", "C": "IV", "D": "I"}], "A"),
      "Tests for functional groups",
      "Each functional group has a characteristic laboratory test.",
      ["C=C → adds bromine → bromine water decolourised → III",
       "Alcohol → ceric ammonium nitrate turns from yellow to red → IV",
       "–COOH → CO₂ with NaHCO₃ → II", "–CHO → Tollens' reagent reduced to silver → I"],
      why_others_wrong="A-IV, B-III swaps the tests for unsaturation and alcohols. C-I, D-II swaps the acid and "
                       "aldehyde tests. B-II, C-IV gives the effervescence to the alcohol.",
      ncert=f"{LAB}, tests for functional groups in organic compounds", seconds=45),

    Q(T_PR, "Qualitative salt analysis", "Intermediate", "assertion_reason",
      *ar("In salt analysis, group II cations are precipitated as sulphides by H₂S in the presence of dilute HCl, "
          "whereas group IV cations are not precipitated under these conditions.", True,
          "Dilute HCl increases the ionisation of H₂S, raising the sulphide ion concentration.", False),
      "Role of HCl in group II precipitation",
      "H⁺ from HCl suppresses the ionisation of H₂S (common ion effect), so the S²⁻ concentration is low. Only the "
      "sulphides of very low solubility product (group II) exceed their Ksp; group IV sulphides need the higher "
      "S²⁻ concentration available in ammoniacal solution.",
      ["A: true", "R: HCl decreases, not increases, the ionisation of H₂S → false"],
      ncert=f"{LAB}, systematic qualitative analysis of cations; {NC11}, 'Equilibrium', common ion effect",
      seconds=45),

    N(T_PR, "Titrimetric analysis", "Advanced",
      "0.53 g of an impure sample of sodium carbonate is dissolved in water and titrated with 0.1 M HCl using "
      "methyl orange as indicator. 80.0 mL of the acid is needed. Assuming the impurities do not react, the "
      "percentage purity of the sample is (Na = 23, C = 12, O = 16):",
      ["40%", "80%", "42.4%", "20%"], "B", "80%",
      "Percentage purity from an acid–base titration",
      "With methyl orange the end point corresponds to complete neutralisation: Na₂CO₃ + 2HCl → 2NaCl + H₂O + CO₂.",
      ["mmol HCl = 80.0 × 0.1 = 8.0 mmol", "mmol Na₂CO₃ = 8.0/2 = 4.0 mmol",
       "Mass = 4.0 × 106 = 424 mg = 0.424 g", "Purity = 0.424/0.53 × 100 = 80%"],
      why_others_wrong="40% takes a 1 : 1 ratio of HCl to Na₂CO₃. 20% takes four HCl per Na₂CO₃. 42.4% reports "
                       "the mass of pure carbonate (0.424 g) as if it were a percentage.",
      ncert=f"{LAB}, titrimetric analysis (acid–base titrations)", seconds=75),

    Q(T_PR, "Qualitative salt analysis", "Advanced", "multi_statement",
      *ms("Which of the following tests for anions are correctly described?",
          [("Sulphate: a white precipitate with BaCl₂ solution that is insoluble in concentrated HCl or HNO₃.",
            True),
           ("Acetate: a deep red colour with neutral iron(III) chloride solution.", True),
           ("Sulphite: warming with dilute H₂SO₄ gives H₂S, which turns lead acetate paper black.", False),
           ("Oxalate: decolourises warm, acidified KMnO₄ solution with evolution of CO₂.", True),
           ("Nitrate: brown fumes of NO₂ with dilute H₂SO₄ in the cold.", False)],
          [["a", "b", "c"], ["a", "d", "e"], ["b", "c", "d"]], "D"),
      "Tests for anions",
      "Dilute H₂SO₄ releases SO₂ (not H₂S) from sulphites; SO₂ turns acidified dichromate paper green. Brown fumes "
      "with dilute acid are given by nitrite; nitrate needs concentrated H₂SO₄ (with copper turnings) or the brown "
      "ring test.",
      ["(a) BaSO₄ is insoluble in acids → true", "(b) Iron(III) acetate gives a deep red colour → true",
       "(c) Sulphite gives SO₂ → false", "(d) Oxalate is oxidised to CO₂ by MnO₄⁻ → true",
       "(e) Nitrate does not give NO₂ with dilute acid → false"],
      why_others_wrong="Every other option contains (c) or (e), or leaves out the true statement (d).",
      ncert=f"{LAB}, qualitative analysis (tests for anions)", seconds=70),

    Q(T_PR, "Thermochemistry and kinetics experiments", "Advanced", "statement_pair",
      *sp("The enthalpy of neutralisation of ethanoic acid by sodium hydroxide is less negative than that of "
          "hydrochloric acid by sodium hydroxide.", True,
          "The enthalpy of solution of every salt in water is negative, so a salt always warms the water when it "
          "dissolves.", False),
      "Enthalpy changes measured in the laboratory",
      "Part of the heat released when a weak acid is neutralised is used to complete its ionisation, so the "
      "enthalpy of neutralisation is less negative than about −57 kJ mol⁻¹. Many salts (e.g. KNO₃, NH₄Cl) dissolve "
      "endothermically and cool the water.",
      ["Statement I: weak acid → energy used for ionisation → less heat released → true",
       "Statement II: enthalpy of solution can be positive (KNO₃, NH₄Cl) → false"],
      ncert=f"{LAB}, thermochemistry (enthalpy of solution and of neutralisation)", seconds=45),
]

# ---------------------------------------------------------------- package checks and output
PLAN = {T_DF: (4, 5, 4), T_CC: (5, 6, 5), T_PU: (2, 2, 2), T_GO: (6, 7, 6), T_HC: (5, 6, 5), T_HX: (3, 4, 3),
        T_OX: (6, 7, 5), T_NI: (3, 4, 3), T_BM: (3, 4, 3), T_PR: (3, 4, 3)}
TOTAL = LAST - FIRST + 1

if __name__ == "__main__":
    assert len(QUESTIONS) == TOTAL == 128, len(QUESTIONS)
    assert [x["question_id"] for x in QUESTIONS] == [f"NEET_CHE_{n:06d}" for n in range(FIRST, LAST + 1)]
    have = Counter((x["topic"], x["difficulty"]) for x in QUESTIONS)
    for topic, quota in PLAN.items():
        for diff, n in zip(("Basic", "Intermediate", "Advanced"), quota):
            assert have[(topic, diff)] == n, (topic, diff, have[(topic, diff)], n)
    keys = Counter(x["correct_answer"] for x in QUESTIONS)
    assert all(29 <= keys[k] <= 35 for k in LETTERS), keys
    fmts = Counter(x["format"] for x in QUESTIONS)
    assert 0.27 <= fmts["numerical"] / TOTAL <= 0.33, fmts
    assert all(fmts[f] / TOTAL >= 0.08 for f in fmts if f != "numerical") and len(fmts) == 6, fmts
    for x in QUESTIONS:  # every numerical answer is recomputed above
        assert (x["format"] == "numerical") == ("script:recompute" in x["verification"]["verified_by"]), x["question_id"]
    doc = {"schema_version": "1.0", "batch_id": "BATCH_003", "created_at": TODAY,
           "notes": "Package CHE_003_p2: 128 original Chemistry questions (d/f block, coordination compounds, "
                    "organic chemistry, biomolecules, practical chemistry). Numerical answers recomputed by "
                    "tools/batch_003/CHE_003_p2.py.",
           "stimuli": [], "questions": QUESTIONS}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {OUT}: {dict(Counter(x['difficulty'] for x in QUESTIONS))}, keys {dict(sorted(keys.items()))}, "
          f"formats {dict(fmts)}")
