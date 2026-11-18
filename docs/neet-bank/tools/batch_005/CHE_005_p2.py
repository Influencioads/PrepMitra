"""Writes batches/parts/BATCH_005_CHE_p2.json: package CHE_005_p2 of BATCH_005 (Chemistry, 122 questions).

Topics: d- and f-Block Elements, Coordination Compounds, Purification and Characterisation of Organic Compounds,
Some Basic Principles of Organic Chemistry, Hydrocarbons, Organic Compounds Containing Halogens / Oxygen / Nitrogen,
Biomolecules (Chemistry), Principles Related to Practical Chemistry. IDs NEET_CHE_001129..NEET_CHE_001250.

Every numerical answer is re-derived below with an assert; multi-statement keys are derived from the truth value of
each statement, assertion-reason and statement-pair keys from the truth of each part. If any check fails, nothing is
written.

    python docs/neet-bank/tools/batch_005/CHE_005_p2.py
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
OUT = ROOT / "batches" / "parts" / "BATCH_005_CHE_p2.json"
TODAY = "2026-11-16"
LETTERS = "ABCD"
CHE = "Chemistry"
FIRST, LAST = 1129, 1250
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


def g(x, nd=1, unit=" g"):
    """Format a number with nd decimals and a unit."""
    return f"{float(x):.{nd}f}{unit}"


# Atomic masses used in the stems
C_, H_, O_, N_, S_, NA, CL, K_, MN, BR, I_, CR = 12, 1, 16, 14, 32, 23, F(355, 10), 39, 55, 80, 127, 52


def mm(**atoms):
    """Molar mass from atom counts, e.g. mm(C=2, H=6, O=1)."""
    table = {"C": C_, "H": H_, "O": O_, "N": N_, "S": S_, "Na": NA, "Cl": CL, "K": K_, "Mn": MN, "Br": BR,
             "I": I_, "Cr": CR}
    return sum(table[k] * v for k, v in atoms.items())


QUESTIONS = []

# ================================================================ d- and f-Block Elements (1129-1139)
# 1130: 2MnO2 + 4KOH + O2 -> 2K2MnO4 + 2H2O ; 8.7 g MnO2
m_mno2, m_k2mno4, m_kmno4 = mm(Mn=1, O=2), mm(K=2, Mn=1, O=4), mm(K=1, Mn=1, O=4)
n_1130 = F(87, 10) / m_mno2
assert m_mno2 == 87 and m_k2mno4 == 197 and m_kmno4 == 158 and n_1130 == F(1, 10)
v_1130 = g(n_1130 * m_k2mno4)
assert v_1130 == "19.7 g" and g(n_1130 * m_kmno4) == "15.8 g"
# 1132: 2MnO4- + I- + H2O -> 2MnO2 + IO3- + 2OH- ; I-: -1 -> +5 (6 e-), MnO4-: +7 -> +4 (3 e-)
e_i, e_mn = 5 - (-1), 7 - 4
n_1132 = F(15, 100) * e_i / e_mn
assert n_1132 == F(30, 100)
assert F(15, 100) * e_mn / e_i == F(75, 1000)          # ratio inverted
assert F(15, 100) * 1 / 5 == F(3, 100)                   # acidic: 2I- -> I2 (1 e- each), Mn gains 5
v_1132 = "0.30 mol"
# 1137: d-electron counts of the ions (Ti 22, V 23, Cr 24, Mn 25, Ni 28, Cu 29, Zn 30, Sc 21)
d_1137 = {"Ti4+": 22 - 18 - 4, "V3+": 23 - 18 - 3, "Cu+": 29 - 18 - 1, "Zn2+": 30 - 18 - 2, "Sc3+": 21 - 18 - 3,
          "Cr3+": 24 - 18 - 3, "Mn2+": 25 - 18 - 2, "Ni2+": 28 - 18 - 2}
colourless = [k for k, d in d_1137.items() if d in (0, 10)]
assert colourless == ["Ti4+", "Cu+", "Zn2+", "Sc3+"]
v_1137 = str(len(colourless))

QUESTIONS += [
    Q(T_DF, "Transition element trends", "Basic", "direct",
      "Transition metals and their compounds are known for their catalytic activity. In the Contact process for "
      "the manufacture of sulphuric acid, the transition metal compound used as the catalyst is:",
      ["Manganese dioxide, MnO₂", "Vanadium(V) oxide, V₂O₅", "Finely divided iron", "Finely divided nickel"], "B",
      "Catalytic properties of the transition metals",
      "NCERT gives three examples: vanadium(V) oxide in the Contact process, finely divided iron in Haber's process "
      "and nickel in catalytic hydrogenation. The catalytic activity is linked to the ability of these metals to "
      "adopt several oxidation states and to form complexes.",
      ["Contact process (SO₂ → SO₃): V₂O₅", "Haber's process (NH₃): finely divided iron",
       "Catalytic hydrogenation: nickel"],
      why_others_wrong="Finely divided iron is the catalyst of Haber's process and nickel of catalytic hydrogenation. "
                       "MnO₂ is not the Contact process catalyst.",
      ncert=f"{NC12}, 'The d- and f-Block Elements', catalytic properties", seconds=25),

    N(T_DF, "K2Cr2O7 and KMnO4", "Basic",
      "In the first step of making potassium permanganate, MnO₂ is fused with KOH in the presence of air:\n"
      "2MnO₂ + 4KOH + O₂ → 2K₂MnO₄ + 2H₂O\n"
      "The mass of potassium manganate formed from 8.7 g of MnO₂ is (K = 39, Mn = 55, O = 16):",
      ["39.4 g", "9.85 g", "19.7 g", "15.8 g"], "C", v_1130,
      "Stoichiometry of the manganate step in the preparation of KMnO₄",
      "MnO₂ and K₂MnO₄ are in a 1 : 1 mole ratio (2 : 2 in the equation).",
      ["M(MnO₂) = 55 + 32 = 87 g mol⁻¹ → 8.7 g = 0.10 mol", "Mole ratio MnO₂ : K₂MnO₄ = 1 : 1 → 0.10 mol K₂MnO₄",
       "M(K₂MnO₄) = 78 + 55 + 64 = 197 g mol⁻¹ → mass = 19.7 g"],
      why_others_wrong="39.4 g doubles the moles (reading 2K₂MnO₄ as per mole of MnO₂). 9.85 g halves them. "
                       "15.8 g is the mass of 0.10 mol of KMnO₄, the final product, not of the manganate.",
      ncert=f"{NC12}, 'The d- and f-Block Elements', potassium permanganate (preparation)", seconds=40),

    Q(T_DF, "K2Cr2O7 and KMnO4", "Basic", "match_list",
      *ml("Match each step in the manufacture of potassium dichromate and potassium permanganate (List-I) with "
          "the product it gives (List-II).",
          ["Chromite ore fused with sodium carbonate in free access of air",
           "Sodium chromate solution acidified with sulphuric acid",
           "MnO₂ fused with KOH and an oxidising agent such as KNO₃",
           "Manganate oxidised electrolytically in alkaline solution"],
          ["Potassium permanganate", "Sodium dichromate", "Sodium chromate", "Potassium manganate"],
          "III II IV I", ["II III IV I", "III II I IV", "IV II III I"], "D"),
      "Manufacture of K₂Cr₂O₇ and KMnO₄",
      "Chromite (FeCr₂O₄) fused with Na₂CO₃ in air gives sodium chromate; acidifying the chromate gives sodium "
      "dichromate (then treated with KCl). MnO₂ fused with KOH and an oxidant gives green K₂MnO₄, and the "
      "manganate is oxidised (electrolytically in alkaline solution) to permanganate.",
      ["A: chromite + Na₂CO₃ + air → Na₂CrO₄ (III)", "B: Na₂CrO₄ + H⁺ → Na₂Cr₂O₇ (II)",
       "C: MnO₂ + KOH + KNO₃ → K₂MnO₄ (IV)", "D: MnO₄²⁻ → MnO₄⁻ electrolytically (I)"],
      ncert=f"{NC12}, 'The d- and f-Block Elements', potassium dichromate and potassium permanganate",
      seconds=45),

    N(T_DF, "K2Cr2O7 and KMnO4", "Intermediate",
      "In neutral or faintly alkaline solution, permanganate oxidises iodide to iodate and is itself reduced to "
      "manganese dioxide:\n2MnO₄⁻ + I⁻ + H₂O → 2MnO₂ + IO₃⁻ + 2OH⁻\n"
      "The amount of KMnO₄ needed to oxidise 0.15 mol of KI completely to KIO₃ is:",
      ["0.30 mol", "0.075 mol", "0.15 mol", "0.03 mol"], "A", v_1132,
      "Redox stoichiometry of permanganate in neutral or faintly alkaline medium",
      "Each I⁻ loses 6 electrons (−1 → +5) and each MnO₄⁻ gains 3 electrons (+7 → +4), so 2 MnO₄⁻ are needed "
      "per I⁻, as the balanced equation shows.",
      ["Mole ratio MnO₄⁻ : I⁻ = 2 : 1", "n(KMnO₄) = 2 × 0.15 = 0.30 mol",
       "Electron check: 0.15 × 6 = 0.90 mol e⁻ = 0.30 × 3"],
      why_others_wrong="0.075 mol inverts the 2 : 1 ratio. 0.15 mol takes a 1 : 1 ratio. 0.03 mol is the answer "
                       "for acidic solution, where iodide goes only to I₂ (1 e⁻ per I⁻) and Mn gains 5 e⁻.",
      ncert=f"{NC12}, 'The d- and f-Block Elements', potassium permanganate (oxidising action)", seconds=50),

    Q(T_DF, "Transition element trends", "Intermediate", "multi_statement",
      *ms("Which of the following statements about the oxidation states of the transition elements are correct?",
          [("From Sc to Mn, the highest oxidation state shown in the oxides equals the group number, e.g. +7 in "
            "Mn₂O₇.", True),
           ("The most common oxidation state of scandium is +2.", False),
           ("Iron reaches an oxidation state of +8 in its common compounds.", False),
           ("Low oxidation states, such as zero in Ni(CO)₄, are found with ligands that can act as π-acceptors in "
            "addition to forming σ bonds.", True),
           ("The oxidation states of a transition element usually differ from each other by one unit, whereas those "
            "of p-block elements normally differ by two units.", True)],
          [["a", "b", "d"], ["c", "d", "e"], ["a", "c", "e"]], "B"),
      "Variable oxidation states of the transition elements",
      "NCERT: the highest oxidation number in the oxides coincides with the group number up to Mn₂O₇; scandium "
      "shows +3; iron shows states up to +6; zero states occur with π-acceptor ligands (Ni(CO)₄, Fe(CO)₅); and "
      "the oxidation states of a transition element differ by unity (e.g. V(II) to V(V)), unlike non-transition "
      "elements, where they normally differ by two.",
      ["(a) Sc₂O₃ … Mn₂O₇: highest state = group number → true", "(b) Sc is +3 → false",
       "(c) +8 is not shown by iron (up to +6) → false", "(d) π-acceptor ligands stabilise low states → true",
       "(e) differences of one unit → true"],
      why_others_wrong="Every other option includes (b) or (c), both false, or leaves out a true statement.",
      ncert=f"{NC12}, 'The d- and f-Block Elements', variation in oxidation states; oxides and oxoanions",
      seconds=70),

    Q(T_DF, "Transition element trends", "Intermediate", "assertion_reason",
      *ar("E°(Fe³⁺/Fe²⁺) is comparatively low, being much less positive than E°(Mn³⁺/Mn²⁺).", True,
          "Fe³⁺ has the extra-stable, half-filled 3d⁵ configuration.", True, explains=True),
      "Stability of half-filled d⁵ ions and E°(M³⁺/M²⁺)",
      "Fe²⁺ (3d⁶) loses one electron to reach the half-filled 3d⁵ state of Fe³⁺, so Fe³⁺ is not easily reduced and "
      "E°(Fe³⁺/Fe²⁺) is low. For manganese the situation is reversed: Mn²⁺ is the d⁵ ion, so Mn³⁺ is readily "
      "reduced and E°(Mn³⁺/Mn²⁺) is high.",
      ["A: E°(Fe³⁺/Fe²⁺) is low compared with E°(Mn³⁺/Mn²⁺) → true",
       "R: Fe³⁺ = [Ar] 3d⁵, half-filled → true",
       "The stability of Fe³⁺ (d⁵) is exactly why it resists reduction → R explains A"],
      ncert=f"{NC12}, 'The d- and f-Block Elements', trends in the M³⁺/M²⁺ standard electrode potentials",
      seconds=45),

    Q(T_DF, "Lanthanoids and actinoids", "Intermediate", "statement_pair",
      *sp("Besides +3, the lanthanoids show +2 and +4 states, which often arise when the ion gets an empty, "
          "half-filled or completely filled 4f subshell.", True,
          "In the lanthanoid contraction, the decrease in atomic radii from La to Lu is less regular than the "
          "decrease in the radii of the M³⁺ ions.", True),
      "Oxidation states of lanthanoids and the lanthanoid contraction",
      "NCERT explains the occasional +2 and +4 ions by the extra stability of empty, half-filled or filled f "
      "subshells (e.g. Ce⁴⁺ f⁰, Eu²⁺ f⁷, Yb²⁺ f¹⁴). It also notes that the decrease in atomic radii (derived from "
      "metal structures) is not as regular as the decrease in the M³⁺ ionic radii.",
      ["Statement I: f⁰, f⁷, f¹⁴ explain +2 and +4 states → true",
       "Statement II: atomic radii decrease less regularly than M³⁺ radii → true"],
      ncert=f"{NC12}, 'The d- and f-Block Elements', the lanthanoids (atomic and ionic sizes, oxidation states)",
      seconds=40),

    Q(T_DF, "Transition element trends", "Intermediate", "direct",
      "Across the 3d series, the E°(M²⁺/M) values of manganese, nickel and zinc do not fit the general trend. "
      "NCERT relates the value for nickel to:",
      ["the highest negative enthalpy of hydration of Ni²⁺ in the series",
       "the half-filled 3d⁵ configuration of Ni²⁺",
       "the completely filled 3d¹⁰ configuration of Ni²⁺",
       "the very low enthalpy of atomisation of nickel"], "A",
      "Irregularities in E°(M²⁺/M) across the 3d series",
      "NCERT: the stability of the half-filled d subshell in Mn²⁺ and of the completely filled d¹⁰ configuration in "
      "Zn²⁺ are related to their E° values, whereas E° for Ni is related to the highest negative ΔhydH°.",
      ["Mn²⁺ (3d⁵): half-filled → irregular E°", "Zn²⁺ (3d¹⁰): filled → irregular E°",
       "Ni²⁺ (3d⁸): neither; its E° is linked to its very negative hydration enthalpy"],
      why_others_wrong="Ni²⁺ is 3d⁸, neither half-filled (that is Mn²⁺) nor completely filled (that is Zn²⁺). Nickel "
                       "has a high, not a very low, enthalpy of atomisation.",
      ncert=f"{NC12}, 'The d- and f-Block Elements', trends in the M²⁺/M standard electrode potentials",
      seconds=40),

    N(T_DF, "Magnetic and colour properties", "Advanced",
      "How many of the following ions have no possibility of d–d transitions and are therefore expected to give "
      "colourless compounds?\nTi⁴⁺, V³⁺, Cu⁺, Zn²⁺, Sc³⁺, Cr³⁺, Mn²⁺, Ni²⁺\n"
      "(Atomic numbers: Sc 21, Ti 22, V 23, Cr 24, Mn 25, Ni 28, Cu 29, Zn 30)",
      ["3", "5", "2", "4"], "D", v_1137,
      "Colour of transition metal ions and d–d transitions",
      "A d–d transition needs a partly filled d subshell. Ions with d⁰ or d¹⁰ configurations cannot show it and "
      "are colourless.",
      ["Ti⁴⁺ d⁰, Sc³⁺ d⁰ → colourless", "Cu⁺ d¹⁰, Zn²⁺ d¹⁰ → colourless",
       "V³⁺ d² (green), Cr³⁺ d³ (violet), Mn²⁺ d⁵ (pink), Ni²⁺ d⁸ (green) → coloured", "Count = 4"],
      why_others_wrong="3 or 2 miss Cu⁺ (d¹⁰) or one of the d⁰ ions. 5 wrongly counts Mn²⁺: d⁵ has unpaired "
                       "electrons, and Mn²⁺ is pale pink.",
      ncert=f"{NC12}, 'The d- and f-Block Elements', formation of coloured ions", seconds=60),

    Q(T_DF, "K2Cr2O7 and KMnO4", "Advanced", "multi_statement",
      *ms("Which of the following statements about potassium dichromate and potassium permanganate are correct?",
          [("Sodium dichromate is more soluble in water than potassium dichromate.", True),
           ("Potassium dichromate is used in the leather industry and as an oxidant for preparing many azo "
            "compounds.", True),
           ("Potassium permanganate is highly soluble in water, dissolving to well over 50 g per 100 g of water at "
            "293 K.", False),
           ("Acidified dichromate oxidises iodide ions to iodine.", True),
           ("When an orange dichromate solution is made alkaline and turns yellow, chromium is reduced from +6 to "
            "+3.", False)],
          [["a", "c", "d"], ["b", "d", "e"], ["a", "b", "e"]], "C"),
      "Properties and uses of K₂Cr₂O₇ and KMnO₄",
      "Sodium dichromate is more soluble, which is why KCl is added to crystallise K₂Cr₂O₇. NCERT lists the uses "
      "of K₂Cr₂O₇ in the leather industry and for azo compounds, and its oxidation of I⁻ to I₂ in acid. KMnO₄ is "
      "not very soluble (6.4 g per 100 g of water at 293 K). The dichromate → chromate change in alkali is not a "
      "redox reaction: chromium stays +6.",
      ["(a) true", "(b) true", "(c) 6.4 g/100 g, not very soluble → false", "(d) Cr₂O₇²⁻ + 6I⁻ → 3I₂ → true",
       "(e) Cr remains +6 in chromate → false"],
      why_others_wrong="Every other option includes (c) or (e), both false.",
      ncert=f"{NC12}, 'The d- and f-Block Elements', potassium dichromate and potassium permanganate",
      seconds=70),

    Q(T_DF, "K2Cr2O7 and KMnO4", "Advanced", "assertion_reason",
      *ar("In acidic solution, permanganate is a stronger oxidising agent than dichromate.", True,
          "Potassium dichromate forms orange crystals.", True),
      "Comparing the oxidising power of MnO₄⁻ and Cr₂O₇²⁻",
      "E°(MnO₄⁻/Mn²⁺) = 1.52 V is more positive than E°(Cr₂O₇²⁻/Cr³⁺) = 1.33 V, so permanganate is the stronger "
      "oxidant in acid. The colour of K₂Cr₂O₇ crystals is a true fact but has nothing to do with the relative "
      "oxidising power.",
      ["A: 1.52 V > 1.33 V → permanganate stronger → true", "R: K₂Cr₂O₇ crystals are orange → true",
       "Colour does not decide oxidising strength → R is not the explanation"],
      ncert=f"{NC12}, 'The d- and f-Block Elements', potassium dichromate and potassium permanganate",
      seconds=40),
]

# ================================================================ Coordination Compounds (1140-1153)
# 1140: didentate ligands among en, C2O4(2-), NH3, EDTA(4-), CN-, Cl-, H2O
dent = {"en": 2, "ox": 2, "NH3": 1, "EDTA": 6, "CN": 1, "Cl": 1, "H2O": 1}
v_1140 = str(sum(1 for d in dent.values() if d == 2))
assert v_1140 == "2"
# 1142: Dt = (4/9) Do
v_1142 = F(4, 9) * 18000
assert v_1142 == 8000 and F(2, 3) * 18000 == 12000 and F(9, 4) * 18000 == 40500 and F(3, 5) * 18000 == 10800
# 1144: PtCl4.4NH3, Pt(IV), CN 6 -> [Pt(NH3)4Cl2]Cl2
cl_inside = 6 - 4
ions_1144 = 1 + (4 - cl_inside)
assert ions_1144 == 3
# 1150: geometrical isomerism
geo = {"[Pt(NH3)2Cl2] sq. planar": True, "[Co(NH3)4Cl2]+": True, "[Co(NH3)3Cl3]": True,
       "[Zn(NH3)2Cl2] tetrahedral": False, "[Co(NH3)5Cl]2+": False, "[Co(en)3]3+": False, "[PtCl2(en)2]2+": True}
v_1150 = str(sum(geo.values()))
assert v_1150 == "4"

QUESTIONS += [
    N(T_CC, "Werner's theory and ligands", "Basic",
      "How many of the following ligands are didentate?\nH₂NCH₂CH₂NH₂ (en), C₂O₄²⁻, NH₃, EDTA⁴⁻, CN⁻, Cl⁻, H₂O",
      ["2", "1", "3", "4"], "A", v_1140,
      "Denticity of ligands",
      "A didentate ligand binds through two donor atoms. NCERT's examples are ethane-1,2-diamine (two N atoms) and "
      "oxalate (two O atoms). EDTA⁴⁻ is hexadentate; NH₃, CN⁻, Cl⁻ and H₂O are unidentate.",
      ["en: 2 N donors → didentate", "C₂O₄²⁻: 2 O donors → didentate", "EDTA⁴⁻: hexadentate",
       "NH₃, CN⁻, Cl⁻, H₂O: unidentate", "Count = 2"],
      why_others_wrong="1 misses oxalate. 3 counts EDTA⁴⁻ or the ambidentate CN⁻ (which binds through one atom at a "
                       "time) as didentate. 4 counts both.",
      ncert=f"{NC12}, 'Coordination Compounds', ligands (denticity)", seconds=35),

    Q(T_CC, "IUPAC nomenclature", "Basic", "direct",
      "The IUPAC name of [Co(NH₃)₄(H₂O)Cl]Cl₂ is:",
      ["Aquatetraamminechloridocobalt(III) chloride", "Tetraammineaquachloridocobalt(II) chloride",
       "Tetraammineaquachloridocobaltate(III) chloride", "Tetraammineaquachloridocobalt(III) chloride"], "D",
      "Naming a cationic complex",
      "Ligands are named in alphabetical order (ammine, aqua, chlorido), ignoring multiplying prefixes. The "
      "oxidation state of cobalt: x + 4(0) + 0 + (−1) = +2 (charge of the complex ion) → x = +3. A cationic complex "
      "keeps the plain metal name.",
      ["Complex ion [Co(NH₃)₄(H₂O)Cl]²⁺ (two Cl⁻ outside)", "x − 1 = +2 → Co(III)",
       "Order: ammine (a-m) before aqua (a-q) before chlorido", "Tetraammineaquachloridocobalt(III) chloride"],
      why_others_wrong="'Aquatetraammine…' puts aqua before ammine, breaking the alphabetical order. Cobalt(II) "
                       "gets the oxidation state wrong. '-ate' is used only for anionic complexes.",
      ncert=f"{NC12}, 'Coordination Compounds', nomenclature of coordination compounds", seconds=40),

    N(T_CC, "Crystal field theory", "Basic",
      "For a certain metal ion and set of ligands, Δo in an octahedral field is 18000 cm⁻¹. For the corresponding "
      "tetrahedral complex (same metal, ligands and metal–ligand distance), the splitting Δt is about:",
      ["8000 cm⁻¹", "12000 cm⁻¹", "40500 cm⁻¹", "10800 cm⁻¹"], "A", f"{int(v_1142)} cm⁻¹",
      "Relation between Δt and Δo",
      "In a tetrahedral field the splitting is smaller: Δt = (4/9)Δo.",
      ["Δt = (4/9) × 18000", "= 8000 cm⁻¹"],
      why_others_wrong="12000 cm⁻¹ uses 2/3, 40500 cm⁻¹ uses 9/4 (the ratio inverted) and 10800 cm⁻¹ uses 3/5, "
                       "the fraction by which eg is raised in an octahedral field.",
      ncert=f"{NC12}, 'Coordination Compounds', crystal field splitting in tetrahedral coordination entities",
      seconds=30),

    Q(T_CC, "Werner's theory and ligands", "Basic", "statement_pair",
      *sp("When a didentate or polydentate ligand uses two or more donor atoms at the same time to bind a single "
          "metal ion, it is called a chelating ligand.", True,
          "In [Co(NH₃)₆]Cl₃, the chloride ions lie inside the coordination sphere.", False),
      "Chelate ligands; coordination sphere and counter ions",
      "NCERT defines a chelate ligand exactly as in Statement I. In [Co(NH₃)₆]Cl₃, the coordination sphere is "
      "[Co(NH₃)₆]³⁺ (the part in square brackets); the three Cl⁻ ions are counter ions outside it.",
      ["Statement I: definition of a chelating ligand → true",
       "Statement II: Cl⁻ ions are outside the brackets (counter ions) → false"],
      ncert=f"{NC12}, 'Coordination Compounds', definitions of some important terms", seconds=30),

    N(T_CC, "Werner's theory and ligands", "Intermediate",
      "A platinum(IV) complex has the composition PtCl₄·4NH₃, and platinum has a coordination number of 6 in it. "
      "Assuming complete ionisation, the number of ions produced in aqueous solution by one formula unit is:",
      ["5", "2", "3", "4"], "C", str(ions_1144),
      "Werner's theory: deducing the formula from the coordination number",
      "Four NH₃ fill four of the six positions, so two Cl⁻ must also be in the coordination sphere. The formula is "
      "[Pt(NH₃)₄Cl₂]Cl₂, which ionises into one complex cation and two chloride ions.",
      ["CN 6 = 4 NH₃ + 2 Cl⁻ → [Pt(NH₃)₄Cl₂]²⁺", "Charge check: +4 − 2 = +2",
       "[Pt(NH₃)₄Cl₂]Cl₂ → [Pt(NH₃)₄Cl₂]²⁺ + 2Cl⁻ → 3 ions"],
      why_others_wrong="5 puts all four Cl⁻ outside, which leaves only four ligands. 2 puts three Cl⁻ inside "
                       "(coordination number 7). 4 corresponds to [Pt(NH₃)₄Cl]Cl₃, with coordination number 5.",
      ncert=f"{NC12}, 'Coordination Compounds', Werner's theory of coordination compounds", seconds=50),

    Q(T_CC, "Isomerism", "Intermediate", "match_list",
      *ml("Match each pair of coordination compounds in List-I with the type of isomerism it shows in List-II.",
          ["[Co(NH₃)₅(SCN)]²⁺ and [Co(NH₃)₅(NCS)]²⁺", "[Pt(NH₃)₄Cl₂]Br₂ and [Pt(NH₃)₄Br₂]Cl₂",
           "[Cu(NH₃)₄][PtCl₄] and [Pt(NH₃)₄][CuCl₄]", "cis- and trans-[Co(NH₃)₄Cl₂]⁺"],
          ["Coordination isomerism", "Geometrical isomerism", "Linkage isomerism", "Ionisation isomerism"],
          "III IV I II", ["IV III I II", "III I IV II", "III IV II I"], "B"),
      "Structural and stereoisomerism in coordination compounds",
      "Linkage: the ambidentate SCN⁻ binds through S or N. Ionisation: a ligand inside and a counter ion outside "
      "change places. Coordination: ligands are interchanged between the cationic and anionic entities. "
      "Geometrical: same ligands, different spatial arrangement (cis/trans).",
      ["A: SCN vs NCS → linkage (III)", "B: Cl⁻ and Br⁻ swap between sphere and counter ion → ionisation (IV)",
       "C: NH₃ and Cl⁻ swap between Cu and Pt → coordination (I)", "D: cis/trans → geometrical (II)"],
      ncert=f"{NC12}, 'Coordination Compounds', isomerism in coordination compounds", seconds=50),

    Q(T_CC, "Crystal field theory", "Intermediate", "statement_pair",
      *sp("For d¹, d² and d³ ions in an octahedral field, the electron arrangement is the same whether the ligands "
          "are strong field or weak field.", True,
          "The magnitude of Δo depends on the field produced by the ligands and on the charge of the metal ion.",
          True),
      "Filling of t₂g and eg orbitals; factors affecting Δo",
      "The first three electrons go singly into the three t₂g orbitals (Hund's rule) in every case; the choice "
      "between t₂g⁴ and t₂g³ eg¹ arises only from d⁴ onwards. NCERT states that Δo depends on the field produced "
      "by the ligand and on the charge on the metal ion.",
      ["Statement I: d¹–d³ → t₂g¹ to t₂g³ regardless of Δo vs P → true",
       "Statement II: Δo depends on ligand field and metal-ion charge → true"],
      ncert=f"{NC12}, 'Coordination Compounds', crystal field splitting in octahedral coordination entities",
      seconds=40),

    Q(T_CC, "Werner's theory and ligands", "Intermediate", "assertion_reason",
      *ar("The coordination number of iron in [Fe(C₂O₄)₃]³⁻ is 6.", True,
          "In the spectrochemical series, the oxalate ion is a weaker field ligand than water.", True),
      "Coordination number with didentate ligands",
      "Each oxalate binds through two O atoms, so three oxalates supply 6 donor atoms. The position of oxalate in "
      "the spectrochemical series (C₂O₄²⁻ < H₂O) is true but concerns the size of Δo, not the number of donor "
      "atoms.",
      ["A: 3 × 2 = 6 donor atoms → true", "R: … OH⁻ < C₂O₄²⁻ < H₂O < NCS⁻ … → true",
       "Field strength does not decide the coordination number → R is not the explanation"],
      ncert=f"{NC12}, 'Coordination Compounds', coordination number; spectrochemical series", seconds=40),

    Q(T_CC, "Applications", "Intermediate", "direct",
      "Articles can be electroplated with silver much more smoothly and evenly from a solution of:",
      ["AgNO₃", "Ag₂SO₄", "AgClO₄", "the complex K[Ag(CN)₂]"], "D",
      "Applications of coordination compounds: electroplating",
      "NCERT: articles are electroplated with silver and gold much more smoothly and evenly from solutions of the "
      "complexes [Ag(CN)₂]⁻ and [Au(CN)₂]⁻ than from solutions of simple metal ions.",
      ["Complexing keeps the concentration of free Ag⁺ low", "Metal deposits slowly and evenly",
       "Use [Ag(CN)₂]⁻"],
      why_others_wrong="AgNO₃, Ag₂SO₄ and AgClO₄ all supply simple Ag⁺ ions, which give a less smooth, uneven "
                       "deposit.",
      ncert=f"{NC12}, 'Coordination Compounds', importance and applications of coordination compounds",
      seconds=30),

    Q(T_CC, "IUPAC nomenclature", "Intermediate", "multi_statement",
      *ms("Which of the following are correct IUPAC rules for naming mononuclear coordination compounds?",
          [("The cation is named first, whether the coordination entity is the cation or the anion.", True),
           ("Anionic ligands are always named before neutral ligands, irrespective of alphabetical order.", False),
           ("Names of anionic ligands end in -o; neutral ligands keep their names, except aqua (H₂O), ammine (NH₃), "
            "carbonyl (CO) and nitrosyl (NO).", True),
           ("When the complex is an anion, the name of the metal ends in -ate, e.g. ferrate for iron.", True),
           ("The prefixes di-, tri- are used for ligands whose names already contain a numerical prefix, such as "
            "ethane-1,2-diamine.", False)],
          [["a", "b", "d"], ["a", "c", "e"], ["b", "c", "d"]], "C"),
      "IUPAC nomenclature of coordination compounds",
      "Ligands are named in alphabetical order, not by charge. Ligands that already contain a numerical prefix are "
      "counted with bis, tris, tetrakis, e.g. tris(ethane-1,2-diamine). The other three rules are as NCERT states.",
      ["(a) cation first → true", "(b) order is alphabetical → false", "(c) -o endings; aqua, ammine, carbonyl, "
       "nitrosyl → true", "(d) -ate for anionic complexes → true", "(e) bis/tris for such ligands → false"],
      why_others_wrong="Every other option includes (b) or (e), both false.",
      ncert=f"{NC12}, 'Coordination Compounds', nomenclature of coordination compounds", seconds=60),

    N(T_CC, "Isomerism", "Advanced",
      "How many of the following show geometrical isomerism? ([Pt(NH₃)₂Cl₂] and [PtCl₂(en)₂]²⁺ are square "
      "planar and octahedral respectively; [Zn(NH₃)₂Cl₂] is tetrahedral.)\n"
      "[Pt(NH₃)₂Cl₂], [Co(NH₃)₄Cl₂]⁺, [Co(NH₃)₃Cl₃], [Zn(NH₃)₂Cl₂], [Co(NH₃)₅Cl]²⁺, [Co(en)₃]³⁺, [PtCl₂(en)₂]²⁺",
      ["3", "4", "5", "6"], "B", v_1150,
      "Geometrical isomerism in square planar, tetrahedral and octahedral complexes",
      "Square planar MA₂B₂ and octahedral MA₄B₂, MA₃B₃ (fac/mer) and M(AA)₂B₂ show geometrical isomerism. "
      "Tetrahedral complexes, MA₅B and M(AA)₃ do not.",
      ["[Pt(NH₃)₂Cl₂]: cis/trans → yes", "[Co(NH₃)₄Cl₂]⁺: cis/trans → yes", "[Co(NH₃)₃Cl₃]: fac/mer → yes",
       "[Zn(NH₃)₂Cl₂]: tetrahedral → no", "[Co(NH₃)₅Cl]²⁺: MA₅B → no", "[Co(en)₃]³⁺: only optical → no",
       "[PtCl₂(en)₂]²⁺: cis/trans → yes", "Count = 4"],
      why_others_wrong="3 usually leaves out the fac/mer pair of [Co(NH₃)₃Cl₃]. 5 counts [Co(en)₃]³⁺, whose "
                       "isomers are optical only. 6 also counts the tetrahedral zinc complex.",
      ncert=f"{NC12}, 'Coordination Compounds', geometric isomerism", seconds=75),

    Q(T_CC, "Crystal field theory", "Advanced", "multi_statement",
      *ms("Which of the following statements about the colour of coordination compounds are correct?",
          [("The colour observed is the complementary colour of the light absorbed.", True),
           ("[Ti(H₂O)₆]³⁺ looks violet because it absorbs light in the blue-green region.", True),
           ("Complexes with strong field ligands are always colourless.", False),
           ("In [Ti(H₂O)₆]³⁺, absorption of light excites the electron from t₂g¹ eg⁰ to t₂g⁰ eg¹.", True),
           ("The colour of a complex depends only on the metal ion and not on the ligands.", False)],
          [["a", "b", "c"], ["b", "d", "e"], ["a", "c", "e"]], "D"),
      "Colour in coordination compounds (CFT)",
      "A complex absorbs part of visible light for a d–d transition and shows the complementary colour; "
      "[Ti(H₂O)₆]³⁺ absorbs blue-green and appears violet (t₂g¹ → eg¹). Strong field complexes such as "
      "[Co(NH₃)₆]³⁺ (yellow-orange) are coloured too; they simply absorb at shorter wavelength. The ligands change "
      "Δo and hence the colour, e.g. [Ni(H₂O)₆]²⁺ green vs [Ni(en)₃]²⁺ violet.",
      ["(a) complementary colour → true", "(b) absorbs blue-green, appears violet → true",
       "(c) strong field complexes are coloured too → false", "(d) t₂g¹ → eg¹ → true",
       "(e) ligands affect Δo and colour → false"],
      why_others_wrong="Every other option includes (c) or (e), both false.",
      ncert=f"{NC12}, 'Coordination Compounds', colour in coordination compounds", seconds=65),

    Q(T_CC, "Valence bond theory", "Advanced", "assertion_reason",
      *ar("[Fe(CN)₆]⁴⁻ and [Fe(H₂O)₆]²⁺ have the same number of unpaired electrons.", False,
          "CN⁻ is a strong field ligand, whereas H₂O is a weaker field ligand.", True),
      "Effect of ligand field strength on the number of unpaired electrons",
      "Both contain Fe²⁺ (3d⁶). With strong field CN⁻, the six electrons pair up in t₂g (t₂g⁶, 0 unpaired, "
      "d²sp³). With weak field H₂O, the complex is high spin (t₂g⁴ eg², 4 unpaired). So A is false while R is true.",
      ["Fe²⁺ = 3d⁶", "[Fe(CN)₆]⁴⁻: t₂g⁶ → 0 unpaired", "[Fe(H₂O)₆]²⁺: t₂g⁴ eg² → 4 unpaired",
       "A false; R true"],
      ncert=f"{NC12}, 'Coordination Compounds', valence bond theory; crystal field theory", seconds=45),

    Q(T_CC, "IUPAC nomenclature", "Advanced", "direct",
      "The formula of pentaamminenitrito-O-cobalt(III) chloride is:",
      ["[Co(NH₃)₅(ONO)]Cl₂", "[Co(NH₃)₅(NO₂)]Cl₂", "[Co(NH₃)₅(ONO)]Cl", "[Co(NH₃)₅(ONO)]Cl₃"], "A",
      "Writing formulas from names; linkage of NO₂⁻",
      "Nitrito-O means the nitrite ion is bound through oxygen, written –ONO. Cobalt(III) with five neutral NH₃ "
      "and one ONO⁻ gives a complex ion of charge +3 − 1 = +2, balanced by two Cl⁻.",
      ["Nitrito-O → Co–ONO (O-bonded)", "Charge: +3 + 5(0) + (−1) = +2", "Two chloride counter ions → "
       "[Co(NH₃)₅(ONO)]Cl₂"],
      why_others_wrong="[Co(NH₃)₅(NO₂)]Cl₂ is the nitrito-N (N-bonded) linkage isomer. With one Cl⁻ the cobalt would "
                       "be +2, and with three Cl⁻ it would be +4.",
      ncert=f"{NC12}, 'Coordination Compounds', nomenclature; linkage isomerism", seconds=45),
]

# ================================================================ Purification and Characterisation (1154-1159)
# 1158: Dumas with corrections. 0.325 g; 50.0 mL over water at 300 K, 775 mm, aqueous tension 15 mm.
def pct_n(v_ml, p_mm, t_k, mass):
    v0 = F(v_ml) * F(p_mm, 760) * F(273, 1) / F(t_k)
    return v0 * 28 / 22400 / F(mass) * 100


v_1158 = pct_n(50, 775 - 15, 300, F(325, 1000))
assert v_1158 == F(35, 2)                                             # 17.5 %
assert g(pct_n(50, 760, 273, F(325, 1000)), 1, "%") == "19.2%"       # no temperature correction
assert g(pct_n(50, 775, 300, F(325, 1000)), 1, "%") == "17.8%"       # aqueous tension ignored
assert g(v_1158 / 2, 2, "%") == "8.75%"                               # N taken as 14 per 22400 mL

QUESTIONS += [
    Q(T_PU, "Quantitative analysis and formulae", "Basic", "direct",
      "In the Carius method for estimating halogens, a known mass of the organic compound is heated in a sealed "
      "tube with fuming nitric acid in the presence of:",
      ["barium chloride", "magnesia mixture", "silver nitrate", "copper(II) oxide"], "C",
      "Carius method for halogens",
      "The carbon and hydrogen are oxidised by fuming HNO₃, and the halogen forms the silver halide (AgX), which is "
      "filtered, washed, dried and weighed.",
      ["Compound + fuming HNO₃ + AgNO₃, heated in a Carius tube", "Halogen → AgX precipitate",
       "% X from the mass of AgX"],
      why_others_wrong="Barium chloride precipitates sulphate in the estimation of sulphur. Magnesia mixture is used "
                       "for phosphorus. Copper(II) oxide is used in the estimation of carbon, hydrogen and nitrogen "
                       "(Dumas).",
      ncert=f"{NC11}, 'Organic Chemistry – Some Basic Principles and Techniques', quantitative analysis (halogens)",
      seconds=25),

    Q(T_PU, "Quantitative analysis and formulae", "Basic", "statement_pair",
      *sp("Sulphur in an organic compound is estimated by converting it into H₂S and weighing it as lead "
          "sulphide.", False,
          "In Kjeldahl's method, the nitrogen is converted into ammonium sulphate by heating with concentrated "
          "H₂SO₄, and the ammonia set free with NaOH is absorbed in a known volume of standard acid.", True),
      "Estimation of sulphur and of nitrogen",
      "Sulphur is oxidised (fuming HNO₃ or Na₂O₂ in a Carius tube) to sulphuric acid and weighed as BaSO₄. "
      "Statement II correctly describes Kjeldahl's method.",
      ["Statement I: sulphur is weighed as BaSO₄, not PbS → false",
       "Statement II: (NH₄)₂SO₄ → NH₃ with NaOH → absorbed in standard acid → true"],
      ncert=f"{NC11}, 'Organic Chemistry – Some Basic Principles and Techniques', quantitative analysis",
      seconds=35),

    Q(T_PU, "Qualitative analysis", "Intermediate", "direct",
      "When testing for halogens in a compound that also contains nitrogen or sulphur, the sodium fusion extract is "
      "first boiled with concentrated nitric acid before silver nitrate is added. This is done to:",
      ["convert the halide ions into free halogens",
       "decompose the sodium cyanide and sodium sulphide, which would otherwise interfere with the silver nitrate "
       "test",
       "remove the excess sodium metal left after fusion",
       "oxidise the halide ions to halate ions"], "B",
      "Lassaigne's test for halogens",
      "CN⁻ and S²⁻ also give precipitates with Ag⁺ (AgCN, Ag₂S). Boiling with concentrated HNO₃ decomposes NaCN and "
      "Na₂S (HCN and H₂S are expelled), so the precipitate with AgNO₃ is due only to the halide.",
      ["NaCN, Na₂S present if N or S is in the compound", "Boil with conc. HNO₃ → HCN, H₂S expelled",
       "Then AgNO₃ → AgX only"],
      why_others_wrong="The halide must stay as X⁻ to be precipitated as AgX, so it is neither converted into free "
                       "halogen nor oxidised. Any sodium is destroyed when the fused mass is plunged into water.",
      ncert=f"{NC11}, 'Organic Chemistry – Some Basic Principles and Techniques', detection of halogens",
      seconds=40),

    Q(T_PU, "Purification methods", "Intermediate", "match_list",
      *ml("Match the separation technique in List-I with its description in List-II.",
          ["Thin layer chromatography", "Column chromatography", "Paper chromatography", "Differential extraction"],
          ["Shaking with an organic solvent immiscible with water in a separating funnel",
           "Partition between water held in the paper and the mobile phase",
           "Adsorption on a layer of silica gel or alumina spread on a glass plate",
           "Adsorbent packed in a glass tube, with the eluant flowing down through it"],
          "III IV II I", ["IV III II I", "III IV I II", "II IV III I"], "D"),
      "Purification and separation methods",
      "TLC and column chromatography are adsorption methods: TLC uses a thin layer of adsorbent on a glass plate; "
      "column chromatography uses an adsorbent packed in a column through which the eluant passes. Paper "
      "chromatography is partition chromatography (water held in the paper is the stationary phase). Differential "
      "extraction uses an immiscible organic solvent in a separating funnel.",
      ["A: TLC → III", "B: column → IV", "C: paper → II", "D: differential extraction → I"],
      ncert=f"{NC11}, 'Organic Chemistry – Some Basic Principles and Techniques', methods of purification",
      seconds=45),

    N(T_PU, "Quantitative analysis and formulae", "Advanced",
      "In a Dumas determination, 0.325 g of an organic compound gave 50.0 mL of nitrogen, collected over water at "
      "300 K and a total pressure of 775 mm Hg. The aqueous tension at 300 K is 15 mm Hg. The percentage of "
      "nitrogen in the compound is (STP: 273 K and 760 mm Hg; 1 mol of N₂ = 28 g and occupies 22400 mL at STP):",
      ["19.2%", "8.75%", "17.5%", "17.8%"], "C", g(v_1158, 1, "%"),
      "Dumas method with corrections for temperature, pressure and aqueous tension",
      "The gas collected over water is moist, so its partial pressure is the total pressure minus the aqueous "
      "tension. The volume is then reduced to STP and converted into mass of nitrogen.",
      ["Pressure of dry N₂ = 775 − 15 = 760 mm Hg", "V(STP) = 50.0 × (760/760) × (273/300) = 45.5 mL",
       "Mass of N₂ = 45.5 × 28/22400 = 0.056875 g", "% N = 0.056875/0.325 × 100 = 17.5%"],
      why_others_wrong="19.2% skips the temperature correction. 17.8% ignores the aqueous tension (uses 775 mm Hg). "
                       "8.75% takes 14 g instead of 28 g of nitrogen per 22400 mL.",
      ncert=f"{NC11}, 'Organic Chemistry – Some Basic Principles and Techniques', estimation of nitrogen (Dumas)",
      seconds=120),

    Q(T_PU, "Purification methods", "Advanced", "multi_statement",
      *ms("Which of the following statements about methods of purification are correct?",
          [("In crystallisation, a solvent is chosen in which the compound is sparingly soluble at room temperature "
            "but appreciably soluble at a higher temperature.", True),
           ("In fractional distillation, the vapours of the liquid with the higher boiling point condense first, "
            "so the lower-boiling liquid passes over first.", True),
           ("Distillation under reduced pressure lets a liquid boil at a temperature lower than its normal boiling "
            "point.", True),
           ("Steam distillation is used for substances that are miscible with water.", False),
           ("Sublimation separates a sublimable compound from impurities that also sublime.", False)],
          [["a", "b", "d"], ["b", "c", "e"], ["a", "d", "e"]], "A"),
      "Crystallisation, distillation and sublimation",
      "NCERT: crystallisation uses a solvent in which the compound is sparingly soluble cold and appreciably "
      "soluble hot; in a fractionating column the higher-boiling vapours condense first; under reduced pressure a "
      "liquid boils below its normal boiling point. Steam distillation needs a steam-volatile substance that is "
      "immiscible with water, and sublimation separates a sublimable compound from non-sublimable impurities.",
      ["(a) true", "(b) true", "(c) true", "(d) immiscible, not miscible → false",
       "(e) impurities must be non-sublimable → false"],
      why_others_wrong="Every other option includes (d) or (e), both false.",
      ncert=f"{NC11}, 'Organic Chemistry – Some Basic Principles and Techniques', methods of purification",
      seconds=65),
]

# ================================================================ Some Basic Principles of Organic Chemistry (1160-1178)
minus_r = {"-NO2": True, "-CN": True, "-CHO": True, "-COOH": True, "-OH": False, "-NH2": False, "-OCH3": False,
           "-Cl": False}
v_1166 = str(sum(minus_r.values()))
assert v_1166 == "4"
resonance = {"aniline": True, "ethanamine": False, "chloroethene": True, "phenol": True, "ethanol": False,
             "propene": False, "chloroethane": False}
v_1172 = str(sum(resonance.values()))
assert v_1172 == "3"
conj_cation = {"CH2=CH-CH2+": True, "C6H5CH2+": True, "(CH3)3C+": False, "CH3CH2+": False,
               "CH2=CH-CH+-CH3": True, "C6H5-CH+-CH3": True, "(CH3)2CH+": False}
v_1173 = str(sum(conj_cation.values()))
assert v_1173 == "4"

QUESTIONS += [
    Q(T_GO, "IUPAC nomenclature", "Basic", "direct",
      "The IUPAC name of CH₃–C≡C–CH(CH₃)–CH₃ is:",
      ["2-Methylpent-3-yne", "4-Methylpent-3-yne", "1,1-Dimethylbut-2-yne", "4-Methylpent-2-yne"], "D",
      "Naming alkynes",
      "The longest chain containing the triple bond has five carbons. Numbering starts from the end nearer the "
      "triple bond, so the triple bond is at C-2 and the methyl group at C-4.",
      ["Parent chain: 5 C including C≡C → pentyne", "Number from the left: C≡C at 2, CH₃ at 4",
       "4-Methylpent-2-yne"],
      why_others_wrong="2-Methylpent-3-yne numbers from the wrong end (the multiple bond must get the lower "
                       "locant). 4-Methylpent-3-yne puts the triple bond at the wrong position. 1,1-Dimethylbut-2-yne "
                       "does not use the longest chain.",
      ncert=f"{NC11}, 'Organic Chemistry – Some Basic Principles and Techniques', IUPAC nomenclature", seconds=35),

    Q(T_GO, "Hybridisation and functional groups", "Basic", "direct",
      "Which of the following is a heterocyclic aromatic compound?",
      ["Cyclohexene", "Pyridine", "Cyclohexane", "Benzene"], "B",
      "Classification of organic compounds",
      "Heterocyclic compounds have a ring that contains an atom other than carbon. Pyridine has a nitrogen atom in "
      "an aromatic six-membered ring; furan and thiophene are other examples NCERT gives.",
      ["Pyridine: N in the ring, aromatic → heterocyclic aromatic",
       "Benzene: aromatic but the ring has only carbon (benzenoid)", "Cyclohexane, cyclohexene: alicyclic"],
      why_others_wrong="Cyclohexene and cyclohexane are alicyclic (carbocyclic, non-aromatic). Benzene is aromatic "
                       "but homocyclic: its ring has only carbon atoms.",
      ncert=f"{NC11}, 'Organic Chemistry – Some Basic Principles and Techniques', classification of organic compounds",
      seconds=25),

    Q(T_GO, "Types of organic reactions", "Basic", "statement_pair",
      *sp("In the carbonyl group, the carbon atom is an electrophilic centre.", True,
          "In CH₃–OH, the oxygen atom is an electrophilic centre.", False),
      "Electrophilic and nucleophilic centres",
      "The carbonyl carbon carries a partial positive charge (oxygen is more electronegative), so it is an "
      "electrophilic centre that nucleophiles attack. The oxygen of an –OH group has lone pairs and is a "
      "nucleophilic centre, not an electrophilic one.",
      ["Statement I: δ⁺ carbonyl carbon → electrophilic centre → true",
       "Statement II: hydroxyl O with lone pairs → nucleophilic centre → false"],
      ncert=f"{NC11}, 'Organic Chemistry – Some Basic Principles and Techniques', nucleophiles and electrophiles",
      seconds=30),

    Q(T_GO, "IUPAC nomenclature", "Basic", "match_list",
      *ml("Match the group (when cited as a substituent prefix) in List-I with its prefix in List-II.",
          ["–OH", "–NO₂", "–OCH₃", ">C=O (ketonic, as a substituent)"],
          ["Oxo", "Methoxy", "Hydroxy", "Nitro"],
          "III IV II I", ["IV III II I", "III IV I II", "III II IV I"], "C"),
      "Prefixes for substituent groups in IUPAC names",
      "When these groups are not the principal group (or, for –NO₂ and –OR, always), they are cited as prefixes: "
      "hydroxy, nitro, methoxy (alkoxy) and oxo.",
      ["A: –OH → hydroxy (III)", "B: –NO₂ → nitro (IV)", "C: –OCH₃ → methoxy (II)", "D: >C=O → oxo (I)"],
      ncert=f"{NC11}, 'Organic Chemistry – Some Basic Principles and Techniques', IUPAC nomenclature (functional "
            "groups)", seconds=35),

    Q(T_GO, "Reactive intermediates", "Basic", "assertion_reason",
      *ar("Carbocations behave as electrophiles.", True,
          "The positively charged carbon of a carbocation has only six electrons in its valence shell.", True,
          explains=True),
      "Carbocations as electron-deficient species",
      "With only a sextet of electrons, the carbocation carbon is electron deficient and seeks an electron pair, "
      "which is what makes it an electrophile.",
      ["A: carbocations accept electron pairs → electrophiles → true", "R: sextet on C⁺ → true",
       "Electron deficiency is the reason it seeks electrons → R explains A"],
      ncert=f"{NC11}, 'Organic Chemistry – Some Basic Principles and Techniques', carbocations", seconds=30),

    Q(T_GO, "IUPAC nomenclature", "Basic", "direct",
      "A compound contains –OH, –NH₂, a C=C bond and a –CHO group. In its IUPAC name, which group is the principal "
      "functional group (cited as the suffix)?",
      ["–OH", "–NH₂", "C=C", "–CHO"], "D",
      "Order of preference of functional groups",
      "NCERT's order of preference: –COOH > –SO₃H > –COOR > –COCl > –CONH₂ > –CN > –CHO > >C=O > –OH > –NH₂ > "
      "C=C > C≡C. Of the four groups here, –CHO ranks highest.",
      ["Compare positions in the preference order", "–CHO comes before –OH, –NH₂ and C=C",
       "So the suffix is -al; –OH and –NH₂ become prefixes (hydroxy, amino)"],
      why_others_wrong="–OH, –NH₂ and C=C all rank below –CHO, so they cannot supply the suffix here.",
      ncert=f"{NC11}, 'Organic Chemistry – Some Basic Principles and Techniques', nomenclature of polyfunctional "
            "compounds", seconds=30),

    N(T_GO, "Electronic effects", "Intermediate",
      "How many of the following groups, attached to a benzene ring, show an electron-withdrawing resonance (−R) "
      "effect?\n–NO₂, –CN, –CHO, –COOH, –OH, –NH₂, –OCH₃, –Cl",
      ["4", "3", "5", "6"], "A", v_1166,
      "Positive and negative resonance effects",
      "Groups with a π bond to a more electronegative atom conjugated with the ring (–NO₂, –CN, –CHO, –COOH) pull "
      "π electrons out of the ring (−R). Groups with a lone pair on the atom attached to the ring (–OH, –NH₂, "
      "–OCH₃, –Cl) donate electrons by resonance (+R).",
      ["−R: –NO₂, –CN, –CHO, –COOH", "+R: –OH, –NH₂, –OCH₃, –Cl", "Count of −R groups = 4"],
      why_others_wrong="3 leaves out one of the −R groups. 5 or 6 count –Cl (and –OCH₃), whose −I effect is "
                       "electron-withdrawing but whose resonance effect is +R.",
      ncert=f"{NC11}, 'Organic Chemistry – Some Basic Principles and Techniques', resonance effect", seconds=45),

    Q(T_GO, "IUPAC nomenclature", "Intermediate", "direct",
      "The IUPAC name of CH₃–CH(Cl)–CH₂–CH(CH₃)–CH₃ is:",
      ["2-Chloro-4-methylpentane", "4-Chloro-2-methylpentane", "2-Methyl-4-chloropentane",
       "1-Chloro-1,3-dimethylbutane"], "A",
      "Lowest locants and alphabetical order",
      "Both directions of numbering give the locant set {2, 4}. When the sets tie, the substituent cited first in "
      "alphabetical order (chloro before methyl) gets the lower number.",
      ["Parent: pentane (5 C)", "Locants either way: 2 and 4 → tie",
       "Alphabetical: chloro gets 2 → 2-chloro-4-methylpentane"],
      why_others_wrong="4-Chloro-2-methylpentane gives the lower number to methyl, against the alphabetical rule. "
                       "2-Methyl-4-chloropentane does not cite the prefixes alphabetically. "
                       "1-Chloro-1,3-dimethylbutane does not use the longest chain.",
      ncert=f"{NC11}, 'Organic Chemistry – Some Basic Principles and Techniques', IUPAC nomenclature", seconds=45),

    Q(T_GO, "Isomerism", "Intermediate", "statement_pair",
      *sp("Methyl ethanoate and ethyl methanoate are functional group isomers.", False,
          "Butanal and butan-2-one are chain isomers.", False),
      "Metamerism and functional group isomerism",
      "Methyl ethanoate (CH₃COOCH₃) and ethyl methanoate (HCOOC₂H₅) are both esters; they differ only in the alkyl "
      "groups on either side of the functional group, so they are metamers. Butanal (aldehyde) and butan-2-one "
      "(ketone) have different functional groups, so they are functional group isomers, not chain isomers.",
      ["Statement I: same functional group (ester) → metamers, not functional isomers → false",
       "Statement II: aldehyde vs ketone → functional group isomers → false"],
      ncert=f"{NC11}, 'Organic Chemistry – Some Basic Principles and Techniques', structural isomerism",
      seconds=40),

    Q(T_GO, "Electronic effects", "Intermediate", "assertion_reason",
      *ar("Both carbon–oxygen bonds in the ethanoate ion, CH₃COO⁻, have the same length.", True,
          "In ethanoic acid itself, the two carbon–oxygen bonds also have the same length.", False),
      "Resonance in the carboxylate ion",
      "The ethanoate ion is a resonance hybrid of two equivalent structures, so both C–O bonds are identical. In "
      "ethanoic acid, one bond is C=O and the other C–OH; the two equivalent structures are not possible, so the "
      "bonds differ in length.",
      ["A: equivalent canonical forms → equal C–O bonds → true",
       "R: acid has one C=O and one C–OH → unequal → false"],
      ncert=f"{NC11}, 'Organic Chemistry – Some Basic Principles and Techniques', resonance structure",
      seconds=40),

    Q(T_GO, "Reactive intermediates", "Intermediate", "match_list",
      *ml("Match the reaction in List-I with the reactive species that attacks or is formed in its key step "
          "(List-II).",
          ["CH₄ + Cl₂ in diffused sunlight", "Hydrolysis of (CH₃)₃C–Br in water (SN1)",
           "Nitration of benzene with a mixture of conc. HNO₃ and conc. H₂SO₄",
           "Addition of HCN to CH₃CHO in the presence of a little base"],
          ["Cyanide ion attacking the carbonyl carbon", "Nitronium ion, NO₂⁺", "Chlorine free radical, Cl•",
           "tert-Butyl carbocation"],
          "III IV II I", ["IV III II I", "III IV I II", "II IV III I"], "D"),
      "Reactive intermediates and attacking reagents",
      "Light causes homolysis of Cl₂, so chlorination of methane is a free radical chain. SN1 hydrolysis of a "
      "tertiary bromide goes through the (CH₃)₃C⁺ ion. Nitration uses the nitronium ion as the electrophile. In "
      "cyanohydrin formation, CN⁻ (made from HCN by the base) attacks the carbonyl carbon.",
      ["A → Cl• (III)", "B → (CH₃)₃C⁺ (IV)", "C → NO₂⁺ (II)", "D → CN⁻ (I)"],
      ncert=f"{NC11}, 'Organic Chemistry – Some Basic Principles and Techniques', reaction mechanism",
      seconds=50),

    Q(T_GO, "IUPAC nomenclature", "Intermediate", "multi_statement",
      *ms("Which of the following IUPAC names are correct?",
          [("CH₃–CH₂–CH(CH₃)–CH₂–OH: 2-methylbutan-1-ol", True),
           ("CH₃–CH=CH–CH₂–OH: but-2-en-1-ol", True),
           ("CH₃–CH(NH₂)–CH₃: propan-2-amine", True),
           ("CH₂=CH–CHO: prop-1-enal", False),
           ("Cl–CH₂–COOH: 1-chloroethanoic acid", False)],
          [["a", "b", "d"], ["b", "c", "e"], ["a", "c", "d"]], "A"),
      "Naming compounds with functional groups",
      "The carbon of –CHO or –COOH is C-1. So CH₂=CH–CHO is prop-2-enal (double bond between C-2 and C-3), and "
      "ClCH₂COOH is chloroethanoic (2-chloroethanoic) acid, since C-1 is the carboxyl carbon. The other three names "
      "follow the rules: the –OH or –NH₂ carbon gets the lowest number.",
      ["(a) OH on C-1, CH₃ on C-2 → true", "(b) OH on C-1, C=C from C-2 → true", "(c) NH₂ on C-2 → true",
       "(d) should be prop-2-enal → false", "(e) C-1 is COOH; Cl is on C-2 → false"],
      why_others_wrong="Every other option includes (d) or (e), both false.",
      ncert=f"{NC11}, 'Organic Chemistry – Some Basic Principles and Techniques', IUPAC nomenclature", seconds=60),

    N(T_GO, "Electronic effects", "Intermediate",
      "Ignoring hyperconjugation, how many of the following show resonance (delocalisation of π electrons or of a "
      "lone pair through a π system)?\nAniline, ethanamine, chloroethene (CH₂=CHCl), phenol, ethanol, propene, "
      "chloroethane",
      ["2", "3", "4", "5"], "B", v_1172,
      "Conditions for resonance",
      "Resonance needs a lone pair or π bond conjugated with another π system. In aniline and phenol the N or O lone "
      "pair is conjugated with the ring; in chloroethene a Cl lone pair is conjugated with the C=C bond.",
      ["Aniline, phenol: lone pair + ring → resonance", "Chloroethene: Cl lone pair + C=C → resonance",
       "Ethanamine, ethanol, chloroethane: no π system", "Propene: only one C=C, no conjugated lone pair "
       "(hyperconjugation only)", "Count = 3"],
      why_others_wrong="2 misses chloroethene. 4 or 5 count propene (whose only delocalisation is hyperconjugation, "
                       "excluded here) or a saturated compound with no π system.",
      ncert=f"{NC11}, 'Organic Chemistry – Some Basic Principles and Techniques', resonance effect", seconds=50),

    N(T_GO, "Reactive intermediates", "Advanced",
      "In how many of the following carbocations is the positive charge delocalised through conjugation with a C=C "
      "bond or a benzene ring (not counting hyperconjugation)?\n"
      "CH₂=CH–CH₂⁺, C₆H₅–CH₂⁺, (CH₃)₃C⁺, CH₃–CH₂⁺, CH₂=CH–CH⁺–CH₃, C₆H₅–CH⁺–CH₃, (CH₃)₂CH⁺",
      ["2", "3", "4", "5"], "C", v_1173,
      "Resonance stabilisation of allylic and benzylic carbocations",
      "Delocalisation through a π system needs the positive carbon to be directly attached to a C=C or a benzene "
      "ring (allylic or benzylic). Alkyl cations are stabilised only by +I and hyperconjugation.",
      ["Allylic: CH₂=CH–CH₂⁺, CH₂=CH–CH⁺–CH₃", "Benzylic: C₆H₅–CH₂⁺, C₆H₅–CH⁺–CH₃",
       "Alkyl only: (CH₃)₃C⁺, CH₃CH₂⁺, (CH₃)₂CH⁺", "Count = 4"],
      why_others_wrong="2 or 3 leave out the substituted allylic or benzylic ions. 5 counts the tert-butyl cation, "
                       "which is very stable but only through +I and hyperconjugation.",
      ncert=f"{NC11}, 'Organic Chemistry – Some Basic Principles and Techniques', carbocations; resonance",
      seconds=60),

    Q(T_GO, "Reactive intermediates", "Advanced", "assertion_reason",
      *ar("The tert-butyl cation, (CH₃)₃C⁺, is less stable than the methyl cation, CH₃⁺.", False,
          "Alkyl groups attached to the positively charged carbon release electrons to it (inductive effect and "
          "hyperconjugation) and disperse the positive charge.", True),
      "Stability order of carbocations",
      "Electron release by the three methyl groups (+I and hyperconjugation) disperses the charge of (CH₃)₃C⁺, so "
      "the order of stability is (CH₃)₃C⁺ > (CH₃)₂CH⁺ > CH₃CH₂⁺ > CH₃⁺. The assertion reverses this.",
      ["A: tertiary cation is the most stable → A false", "R: correct description of alkyl group effects → true"],
      ncert=f"{NC11}, 'Organic Chemistry – Some Basic Principles and Techniques', carbocations", seconds=35),

    Q(T_GO, "Electronic effects", "Advanced", "statement_pair",
      *sp("Among the canonical structures of a molecule, those with greater separation of opposite charges "
          "contribute more to the resonance hybrid.", False,
          "The greater the number of important contributing structures, the greater the resonance energy.", True),
      "Rules for the relative importance of canonical structures",
      "Structures with more covalent bonds, every atom (except H) with an octet, less separation of opposite "
      "charges and negative charge on the more electronegative atom contribute more. NCERT also notes that more "
      "important contributing structures mean a larger resonance energy.",
      ["Statement I: less (not more) charge separation means a larger contribution → false",
       "Statement II: true as NCERT states"],
      ncert=f"{NC11}, 'Organic Chemistry – Some Basic Principles and Techniques', resonance structure",
      seconds=40),

    Q(T_GO, "Isomerism", "Advanced", "match_list",
      *ml("Match each pair of compounds in List-I with the relationship between them in List-II.",
          ["cis-But-2-ene and trans-but-2-ene", "The two non-superimposable mirror-image forms of butan-2-ol",
           "Propan-1-ol and methoxyethane", "Hexan-2-one and hexan-3-one"],
          ["Position isomers", "Functional group isomers", "Optical isomers (enantiomers)",
           "Geometrical isomers"],
          "IV III II I", ["III IV II I", "IV III I II", "IV II III I"], "D"),
      "Structural isomerism and stereoisomerism",
      "cis/trans forms differ in the arrangement about a double bond (geometrical); mirror-image forms of a chiral "
      "molecule are enantiomers (optical); an alcohol and an ether of the same formula differ in functional group; "
      "the two hexanones differ only in the position of the carbonyl group.",
      ["A → geometrical (IV)", "B → optical (III)", "C → functional group (II)", "D → position (I)"],
      ncert=f"{NC11}, 'Organic Chemistry – Some Basic Principles and Techniques', isomerism", seconds=40),

    Q(T_GO, "IUPAC nomenclature", "Advanced", "multi_statement",
      *ms("Which of the following are correct rules of IUPAC nomenclature?",
          [("The parent chain is the longest chain that contains the principal functional group.", True),
           ("The chain is numbered so that the substituents get the lowest set of locants, compared at the first "
            "point of difference.", True),
           ("The chain is numbered so that the carbon bearing the principal functional group gets the lowest "
            "possible number.", True),
           ("Multiplying prefixes such as di- and tri- are taken into account when substituent names are arranged "
            "alphabetically.", False),
           ("In a carboxylic acid containing a C=C bond, the double bond gets locant 1 in preference to the "
            "carboxyl carbon.", False)],
          [["a", "b", "d"], ["a", "c", "e"], ["b", "d", "e"]], "B"),
      "Rules of IUPAC nomenclature",
      "The principal group decides the parent chain and gets the lowest locant (the –COOH carbon is always C-1). "
      "Lowest locants are compared at the first point of difference. Multiplying prefixes (di, tri) are ignored "
      "when alphabetising: e.g. 'ethyl' comes before 'dimethyl'.",
      ["(a) true", "(b) true", "(c) true", "(d) di/tri ignored in alphabetising → false",
       "(e) –COOH carbon is C-1 → false"],
      why_others_wrong="Every other option includes (d) or (e), both false.",
      ncert=f"{NC11}, 'Organic Chemistry – Some Basic Principles and Techniques', IUPAC nomenclature", seconds=60),

    Q(T_GO, "IUPAC nomenclature", "Advanced", "direct",
      "The IUPAC name of (CH₃)₃C–CH₂–CH(CH₃)–CH(CH₃)₂ is:",
      ["2,3,5,5-Tetramethylhexane", "2,4,5,5-Tetramethylhexane", "2,2,4,5-Tetramethylhexane",
       "2,2,4-Trimethylheptane"], "C",
      "Longest chain and lowest set of locants",
      "The longest chain has six carbons: CH₃–C(CH₃)₂–CH₂–CH(CH₃)–CH(CH₃)–CH₃. Numbering from the tert-butyl end "
      "gives {2,2,4,5}; from the other end {2,3,5,5}. At the first point of difference (second locant) 2 < 3, so "
      "the first set is chosen.",
      ["Total carbons: 4 + 1 + 2 + 3 = 10 (C₁₀H₂₂)", "Longest chain: 6 C (hexane) with four methyl groups",
       "Left numbering {2,2,4,5} vs right {2,3,5,5} → choose {2,2,4,5}"],
      why_others_wrong="2,3,5,5 numbers from the wrong end. 2,4,5,5 is not a possible set of locants for this "
                       "molecule. A heptane chain cannot be traced in it; the longest chain has six carbons.",
      ncert=f"{NC11}, 'Organic Chemistry – Some Basic Principles and Techniques', IUPAC nomenclature (branched "
            "alkanes)", seconds=75),
]

# ================================================================ Hydrocarbons (1179-1194)
# 1180: staggered ethane - C-H bonds on each carbon are 120 deg apart; rear set rotated by half of that
v_1180 = 360 // 3 // 2
assert v_1180 == 60
# 1185: CH4 + H2O -> CO + 3H2 ; 8 g CH4
n_ch4 = F(8, mm(C=1, H=4))
assert n_ch4 == F(1, 2)
v_1185 = g(n_ch4 * 3 * F(224, 10), 1, " L")
assert v_1185 == "33.6 L" and g(n_ch4 * F(224, 10), 1, " L") == "11.2 L"
assert g(n_ch4 * 4 * F(224, 10), 1, " L") == "44.8 L" and g(n_ch4 * 2 * F(224, 10), 1, " L") == "22.4 L"
# 1186: CH3CH2CH2Br + KOH(alc) -> CH3CH=CH2 ; 12.3 g
n_1186 = F(123, 10) / mm(C=3, H=7, Br=1)
assert mm(C=3, H=7, Br=1) == 123 and n_1186 == F(1, 10)
v_1186 = g(n_1186 * F(224, 10), 2, " L")
assert v_1186 == "2.24 L"
# 1190: CH2=CH-CH=CH2 + 2O3, Zn/H2O -> 2HCHO + OHC-CHO ; 2.7 g
n_bd = F(27, 10) / mm(C=4, H=6)
assert mm(C=4, H=6) == 54 and n_bd == F(1, 20)
v_1190 = g(2 * n_bd * mm(C=1, H=2, O=1))
assert v_1190 == "3.0 g" and g(n_bd * 30) == "1.5 g" and g(n_bd * mm(C=2, H=2, O=2), 1) == "2.9 g"
assert g(4 * n_bd * 30) == "6.0 g"
# 1191: decolourise bromine water
unsat = {"ethene": True, "ethyne": True, "benzene": False, "cyclohexane": False, "propene": True,
         "cyclohexene": True, "ethane": False}
v_1191 = str(sum(unsat.values()))
assert v_1191 == "4"

QUESTIONS += [
    Q(T_HC, "Alkanes and conformations", "Basic", "direct",
      "Which of the following alkanes cannot be prepared by the Wurtz reaction?",
      ["Methane", "Ethane", "Butane", "Hexane"], "A",
      "Scope of the Wurtz reaction",
      "In the Wurtz reaction, two alkyl groups join, so the product always has at least two carbon atoms (ethane "
      "from CH₃Br, butane from C₂H₅Br, hexane from C₃H₇Br). Methane, with one carbon, cannot be made this way.",
      ["2R–X + 2Na → R–R + 2NaX", "Smallest product: CH₃–CH₃ (ethane)", "Methane is impossible"],
      why_others_wrong="Ethane, butane and hexane are R–R products of CH₃X, C₂H₅X and n-C₃H₇X respectively.",
      ncert=f"{NC11}, 'Hydrocarbons', preparation of alkanes (Wurtz reaction)", seconds=25),

    N(T_HC, "Alkanes and conformations", "Basic",
      "In the Newman projection of the staggered conformation of ethane, the smallest dihedral angle between a C–H "
      "bond on the front carbon and a C–H bond on the rear carbon is:",
      ["0°", "120°", "109.5°", "60°"], "D", f"{v_1180}°",
      "Conformations of ethane",
      "Seen along the C–C axis, the three C–H bonds on each carbon are 120° apart. In the staggered form the rear "
      "bonds lie exactly between the front bonds, so the smallest dihedral angle is 120°/2 = 60°. In the eclipsed "
      "form it is 0°.",
      ["C–H bonds on one carbon: 360°/3 = 120° apart in projection",
       "Staggered: rear bonds bisect the front ones → 60°", "Eclipsed: 0°"],
      why_others_wrong="0° is the eclipsed conformation. 120° is the angle between two bonds on the same carbon. "
                       "109.5° is the tetrahedral bond angle, not a dihedral angle.",
      ncert=f"{NC11}, 'Hydrocarbons', conformations of ethane", seconds=30),

    Q(T_HC, "Benzene and aromaticity", "Basic", "statement_pair",
      *sp("Benzene was first isolated by Kekulé in 1865.", False,
          "The molecular formula of benzene, C₆H₆, indicates a high degree of unsaturation.", True),
      "History and formula of benzene",
      "NCERT: benzene was isolated by Michael Faraday in 1825. Kekulé proposed its cyclic structure with alternating "
      "single and double bonds in 1865. The formula C₆H₆ indicates a high degree of unsaturation.",
      ["Statement I: Faraday isolated it (1825); Kekulé gave the structure (1865) → false",
       "Statement II: C₆H₆ vs C₆H₁₄ for hexane → highly unsaturated → true"],
      ncert=f"{NC11}, 'Hydrocarbons', aromatic hydrocarbons (structure of benzene)", seconds=30),

    Q(T_HC, "Alkanes and conformations", "Basic", "match_list",
      *ml("Match the class of hydrocarbon in List-I with its general formula in List-II.",
          ["Open-chain alkanes", "Open-chain alkenes (one C=C)", "Open-chain alkynes (one C≡C)",
           "Benzene and its alkyl homologues"],
          ["CₙH₂ₙ₋₆", "CₙH₂ₙ₋₂", "CₙH₂ₙ", "CₙH₂ₙ₊₂"],
          "IV III II I", ["III IV II I", "IV II III I", "IV III I II"], "B"),
      "General formulas of hydrocarbons",
      "Each ring or π bond removes two hydrogen atoms from CₙH₂ₙ₊₂. An alkene (one π bond) is CₙH₂ₙ, an alkyne (two "
      "π bonds) CₙH₂ₙ₋₂, and benzene and its alkyl homologues (one ring + three π bonds) CₙH₂ₙ₋₆.",
      ["A: CₙH₂ₙ₊₂ (IV)", "B: CₙH₂ₙ (III)", "C: CₙH₂ₙ₋₂ (II)", "D: CₙH₂ₙ₋₆, e.g. C₆H₆, C₇H₈ (I)"],
      ncert=f"{NC11}, 'Hydrocarbons', classification and general formulas", seconds=30),

    Q(T_HC, "Alkanes and conformations", "Basic", "assertion_reason",
      *ar("Alkanes release a large amount of heat on complete combustion.", True,
          "All the carbon atoms in an alkane are sp³ hybridised.", True),
      "Combustion of alkanes",
      "Combustion of alkanes to CO₂ and H₂O is strongly exothermic, which is why they are used as fuels. That all "
      "the carbons are sp³ hybridised is also true but describes their bonding geometry, not why combustion "
      "releases energy.",
      ["A: e.g. CH₄ + 2O₂ → CO₂ + 2H₂O, ΔcH° = −890 kJ mol⁻¹ → true", "R: alkanes are saturated, sp³ carbons → "
       "true", "Hybridisation does not explain the heat released → R is not the explanation"],
      ncert=f"{NC11}, 'Hydrocarbons', alkanes (structure; combustion)", seconds=30),

    Q(T_HC, "Electrophilic substitution", "Intermediate", "direct",
      "In the chlorination of benzene with Cl₂ in the presence of anhydrous AlCl₃, the role of AlCl₃ is to:",
      ["generate chlorine free radicals", "absorb the HCl formed and shift the equilibrium",
       "act as a Lewis acid that generates the Cl⁺ electrophile", "act as a reducing agent"], "C",
      "Generation of the electrophile in halogenation",
      "AlCl₃ accepts a chloride ion from Cl₂ (Cl₂ + AlCl₃ → Cl⁺ + [AlCl₄]⁻). The Cl⁺ electrophile attacks the ring "
      "to give the arenium ion, which loses H⁺ to form chlorobenzene.",
      ["AlCl₃ is electron deficient → Lewis acid", "Cl₂ + AlCl₃ → Cl⁺ + AlCl₄⁻", "Cl⁺ attacks benzene"],
      why_others_wrong="Free radicals form in light, which leads to addition (benzene hexachloride), not ring "
                       "substitution. AlCl₃ neither absorbs HCl to drive the reaction nor acts as a reductant.",
      ncert=f"{NC11}, 'Hydrocarbons', electrophilic substitution reactions (mechanism)", seconds=30),

    N(T_HC, "Alkanes and conformations", "Intermediate",
      "Methane reacts with steam at 1273 K in the presence of nickel:\nCH₄ + H₂O → CO + 3H₂\n"
      "The volume of hydrogen, measured at STP, obtained from 8.0 g of methane is (C = 12, H = 1; molar volume "
      "at STP = 22.4 L mol⁻¹):",
      ["11.2 L", "33.6 L", "44.8 L", "22.4 L"], "B", v_1185,
      "Stoichiometry of the reaction of methane with steam",
      "One mole of methane gives three moles of hydrogen.",
      ["n(CH₄) = 8.0/16 = 0.50 mol", "n(H₂) = 3 × 0.50 = 1.5 mol", "V = 1.5 × 22.4 = 33.6 L"],
      why_others_wrong="11.2 L takes a 1 : 1 ratio. 44.8 L adds the CO (0.5 mol) to the hydrogen. 22.4 L takes two "
                       "moles of H₂ per mole of methane.",
      ncert=f"{NC11}, 'Hydrocarbons', chemical properties of alkanes (reaction with steam)", seconds=40),

    N(T_HC, "Alkenes: addition and ozonolysis", "Intermediate",
      "12.3 g of 1-bromopropane is heated with alcoholic KOH and converted completely into propene. The volume of "
      "propene at STP is (C = 12, H = 1, Br = 80; molar volume at STP = 22.4 L mol⁻¹):",
      ["1.12 L", "4.48 L", "2.24 L", "3.36 L"], "C", v_1186,
      "Dehydrohalogenation stoichiometry",
      "CH₃CH₂CH₂Br + KOH (alc) → CH₃CH=CH₂ + KBr + H₂O: one mole of alkyl halide gives one mole of alkene.",
      ["M(C₃H₇Br) = 36 + 7 + 80 = 123 g mol⁻¹", "n = 12.3/123 = 0.10 mol propene", "V = 0.10 × 22.4 = 2.24 L"],
      why_others_wrong="1.12 L halves the moles, as if two molecules of halide gave one alkene. 4.48 L doubles them. "
                       "3.36 L multiplies by 1.5, as if three carbon atoms mattered.",
      ncert=f"{NC11}, 'Hydrocarbons', preparation of alkenes from alkyl halides", seconds=40),

    Q(T_HC, "Benzene and aromaticity", "Intermediate", "multi_statement",
      *ms("Which of the following statements about the structure of benzene are correct?",
          [("Kekulé proposed a cyclic arrangement of six carbon atoms with alternate single and double bonds.",
            True),
           ("Benzene forms only one monosubstituted derivative, which shows that all six hydrogen atoms are "
            "equivalent.", True),
           ("Benzene forms three isomeric disubstituted derivatives.", True),
           ("Each carbon atom of benzene is sp³ hybridised.", False),
           ("The six π electrons of benzene are localised in three separate π bonds.", False)],
          [["a", "b", "d"], ["b", "c", "e"], ["a", "c", "d"]], "A"),
      "Structure of benzene",
      "NCERT: Kekulé's structure; one monosubstituted and three (o, m, p) disubstituted derivatives; each carbon "
      "sp² hybridised, with the six π electrons delocalised over the ring (the source of its stability).",
      ["(a) true", "(b) true", "(c) o-, m-, p- → true", "(d) sp² → false", "(e) delocalised → false"],
      why_others_wrong="Every other option includes (d) or (e), both false.",
      ncert=f"{NC11}, 'Hydrocarbons', structure of benzene", seconds=50),

    Q(T_HC, "Alkynes", "Intermediate", "statement_pair",
      *sp("Hydration of an alkyne (with Hg²⁺ and dilute H₂SO₄) proceeds through an unstable enol, which changes "
          "into a carbonyl compound.", True,
          "Ethyne gives ethanal on hydration.", True),
      "Hydration of alkynes",
      "Water adds across the triple bond to give an enol (C=C–OH), which tautomerises to the more stable carbonyl "
      "compound. For ethyne this gives ethanal; higher alkynes give ketones.",
      ["Statement I: enol → carbonyl (tautomerism) → true",
       "Statement II: HC≡CH + H₂O → [CH₂=CHOH] → CH₃CHO → true"],
      ncert=f"{NC11}, 'Hydrocarbons', chemical properties of alkynes (addition of water)", seconds=35),

    Q(T_HC, "Alkanes and conformations", "Intermediate", "assertion_reason",
      *ar("In the chlorination of methane, light or heat brings about homolysis of the Cl–Cl bond in the initiation "
          "step.", True,
          "The C–H bond is weaker than the Cl–Cl bond.", False),
      "Mechanism of free radical halogenation",
      "The chain is initiated by homolysis of Cl₂ because the Cl–Cl bond is weaker than the C–C and C–H bonds, so "
      "it breaks most easily. R states the opposite.",
      ["A: Cl₂ → 2Cl• (hν or heat) → true", "R: Cl–Cl (≈242 kJ mol⁻¹) is weaker than C–H (≈435 kJ mol⁻¹) → R "
       "false"],
      ncert=f"{NC11}, 'Hydrocarbons', halogenation of alkanes (mechanism)", seconds=35),

    N(T_HC, "Alkenes: addition and ozonolysis", "Advanced",
      "2.7 g of buta-1,3-diene, CH₂=CH–CH=CH₂, undergoes complete ozonolysis (O₃, then Zn/H₂O). The mass of "
      "methanal formed is (C = 12, H = 1, O = 16):",
      ["2.9 g", "1.5 g", "3.0 g", "6.0 g"], "C", v_1190,
      "Ozonolysis of a diene",
      "Both double bonds are cleaved. The two terminal CH₂= groups become two HCHO, and the middle =CH–CH= unit "
      "becomes ethanedial, OHC–CHO.",
      ["n(C₄H₆) = 2.7/54 = 0.050 mol", "Each mole gives 2 mol HCHO + 1 mol OHC–CHO",
       "Mass of HCHO = 0.10 × 30 = 3.0 g"],
      why_others_wrong="2.9 g is the mass of ethanedial (0.050 × 58). 1.5 g counts only one HCHO per diene. 6.0 g "
                       "counts four HCHO per diene.",
      ncert=f"{NC11}, 'Hydrocarbons', ozonolysis of alkenes", seconds=60),

    N(T_HC, "Alkenes: addition and ozonolysis", "Advanced",
      "How many of the following decolourise bromine water at room temperature?\n"
      "Ethene, ethyne, benzene, cyclohexane, propene, cyclohexene, ethane",
      ["3", "5", "6", "4"], "D", v_1191,
      "Addition of bromine as a test for unsaturation",
      "Compounds with C=C or C≡C bonds add bromine readily, so the reddish-brown colour disappears. Benzene, "
      "despite its formal unsaturation, does not add bromine under these conditions because of its aromatic "
      "stability; alkanes and cycloalkanes do not react.",
      ["Ethene, propene, cyclohexene (C=C) → decolourise", "Ethyne (C≡C) → decolourises",
       "Benzene (aromatic), cyclohexane, ethane → no", "Count = 4"],
      why_others_wrong="3 misses ethyne or cyclohexene. 5 or 6 count benzene and/or a saturated hydrocarbon.",
      ncert=f"{NC11}, 'Hydrocarbons', addition of halogens (test for unsaturation); aromaticity", seconds=50),

    Q(T_HC, "Alkenes: addition and ozonolysis", "Advanced", "match_list",
      *ml("Match the alkene in List-I with the products of its ozonolysis (O₃, then Zn/H₂O) in List-II.",
          ["Propene", "2-Methylpropene", "Pent-2-ene", "But-1-ene"],
          ["Methanal and propanal", "Ethanal and propanal", "Methanal and propanone", "Methanal and ethanal"],
          "IV III II I", ["IV I II III", "III IV II I", "IV III I II"], "A"),
      "Ozonolysis: locating the double bond",
      "Each carbon of the C=C becomes a C=O. CH₃CH=CH₂ → CH₃CHO + HCHO; (CH₃)₂C=CH₂ → (CH₃)₂CO + HCHO; "
      "CH₃CH=CHCH₂CH₃ → CH₃CHO + CH₃CH₂CHO; CH₃CH₂CH=CH₂ → CH₃CH₂CHO + HCHO.",
      ["A → methanal + ethanal (IV)", "B → methanal + propanone (III)", "C → ethanal + propanal (II)",
       "D → methanal + propanal (I)"],
      ncert=f"{NC11}, 'Hydrocarbons', ozonolysis of alkenes", seconds=55),

    Q(T_HC, "Benzene and aromaticity", "Advanced", "multi_statement",
      *ms("Which of the following statements about benzene and arenes are correct?",
          [("Polynuclear hydrocarbons with more than two fused benzene rings are toxic and are said to be "
            "carcinogenic.", True),
           ("In the presence of ultraviolet light, benzene adds three molecules of chlorine to give benzene "
            "hexachloride, C₆H₆Cl₆.", True),
           ("Arenes burn with a sooty flame.", True),
           ("Friedel–Crafts methylation of benzene with CH₃Cl stops cleanly at toluene, because the methyl group "
            "deactivates the ring.", False),
           ("Benzene is hydrogenated to cyclohexane at room temperature without a catalyst.", False)],
          [["a", "b", "d"], ["a", "c", "e"], ["b", "d", "e"]], "C"),
      "Properties of benzene and arenes",
      "Statements (a)–(c) are NCERT facts. The methyl group activates the ring, so toluene reacts further and "
      "Friedel–Crafts alkylation tends to give polysubstitution. Hydrogenation of benzene needs a nickel catalyst "
      "and high temperature or pressure.",
      ["(a) true", "(b) true (gammaxane)", "(c) true", "(d) CH₃ activates the ring → false",
       "(e) needs Ni, heat and pressure → false"],
      why_others_wrong="Every other option includes (d) or (e), both false.",
      ncert=f"{NC11}, 'Hydrocarbons', aromatic hydrocarbons (properties; carcinogenicity and toxicity)",
      seconds=60),

    Q(T_HC, "Electrophilic substitution", "Advanced", "direct",
      "The correct order of reactivity towards nitration (electrophilic substitution) is:",
      ["Toluene > benzene > chlorobenzene > nitrobenzene", "Benzene > toluene > chlorobenzene > nitrobenzene",
       "Chlorobenzene > toluene > benzene > nitrobenzene", "Toluene > chlorobenzene > benzene > nitrobenzene"], "A",
      "Activating and deactivating groups",
      "–CH₃ activates the ring (+I and hyperconjugation), so toluene reacts faster than benzene. –Cl deactivates "
      "slightly (−I outweighs +R) and –NO₂ deactivates strongly (−I and −R).",
      ["Activating: –CH₃ → toluene fastest", "Reference: benzene", "Weakly deactivating: –Cl",
       "Strongly deactivating: –NO₂ → slowest"],
      why_others_wrong="Placing benzene above toluene ignores the activating methyl group. Placing chlorobenzene "
                       "above benzene treats –Cl as activating, although its −I effect outweighs its +R effect.",
      ncert=f"{NC11}, 'Hydrocarbons', directive influence of a functional group in monosubstituted benzene",
      seconds=40),
]

# ================================================================ Organic Compounds Containing Halogens (1195-1204)
n_1197 = F(109, 10) / mm(C=2, H=5, Br=1)
assert mm(C=2, H=5, Br=1) == 109 and n_1197 == F(1, 10)
v_1197 = g(n_1197 * mm(C=2, H=5, I=1))
assert mm(C=2, H=5, I=1) == 156 and v_1197 == "15.6 g" and g(n_1197 * mm(C=1, H=3, I=1)) == "14.2 g"
assert g(n_1197 * 156 / 2) == "7.8 g"
n_1202 = F(785, 100) / mm(C=3, H=7, Cl=1)
assert mm(C=3, H=7, Cl=1) == F(785, 10) and n_1202 == F(1, 10)
v_1202 = g(n_1202 * mm(C=3, H=6, Br=2))
assert mm(C=3, H=6, Br=2) == 202 and v_1202 == "20.2 g" and g(n_1202 * mm(C=2, H=4, Br=2)) == "18.8 g"
assert g(n_1202 * mm(C=3, H=7, Br=1)) == "12.3 g" and g(n_1202 * 202 / 2) == "10.1 g"

QUESTIONS += [
    Q(T_HX, "C-X bond and preparation", "Basic", "direct",
      "When an alcohol is converted into an alkyl chloride with phosphorus pentachloride, the by-products are:",
      ["SO₂ and HCl", "H₃PO₃ only", "PCl₃ and Cl₂", "POCl₃ and HCl"], "D",
      "Preparation of haloalkanes from alcohols",
      "R–OH + PCl₅ → R–Cl + POCl₃ + HCl.",
      ["PCl₅ replaces –OH by –Cl", "By-products: phosphorus oxychloride and hydrogen chloride"],
      why_others_wrong="SO₂ and HCl are the by-products with thionyl chloride. H₃PO₃ is the by-product with PCl₃ "
                       "(3R–OH + PCl₃ → 3R–Cl + H₃PO₃). PCl₃ and Cl₂ are not formed.",
      ncert=f"{NC12}, 'Haloalkanes and Haloarenes', preparation of haloalkanes from alcohols", seconds=25),

    Q(T_HX, "SN1 and SN2", "Basic", "direct",
      "A haloalkane, R–X, is treated with potassium nitrite, KNO₂. The main product is:",
      ["a nitroalkane, R–NO₂", "an alkyl nitrite, R–O–N=O", "an alkyl isocyanide, R–NC", "an alcohol, R–OH"], "B",
      "Nucleophilic substitution with the ambident nitrite ion",
      "The nitrite ion is ambident. With ionic KNO₂, attack occurs mainly through oxygen, giving the alkyl nitrite "
      "R–O–N=O. With covalent AgNO₂, attack occurs through nitrogen, giving the nitroalkane.",
      ["KNO₂ → free NO₂⁻ attacks through O → R–O–N=O", "AgNO₂ → R–NO₂ (for contrast)"],
      why_others_wrong="R–NO₂ is the main product with AgNO₂. Isocyanides come from AgCN, and alcohols from aqueous "
                       "KOH.",
      ncert=f"{NC12}, 'Haloalkanes and Haloarenes', nucleophilic substitution reactions (table of nucleophiles)",
      seconds=30),

    N(T_HX, "C-X bond and preparation", "Basic",
      "10.9 g of bromoethane is heated with sodium iodide in dry acetone and converted completely into iodoethane "
      "(Finkelstein reaction). The mass of iodoethane formed is (C = 12, H = 1, Br = 80, I = 127):",
      ["14.2 g", "10.9 g", "15.6 g", "7.8 g"], "C", v_1197,
      "Halogen exchange stoichiometry",
      "C₂H₅Br + NaI → C₂H₅I + NaBr: 1 : 1 mole ratio.",
      ["M(C₂H₅Br) = 109 g mol⁻¹ → 0.10 mol", "M(C₂H₅I) = 24 + 5 + 127 = 156 g mol⁻¹", "Mass = 0.10 × 156 = 15.6 g"],
      why_others_wrong="14.2 g is the mass of 0.10 mol of iodomethane. 10.9 g assumes the mass does not change. "
                       "7.8 g halves the moles.",
      ncert=f"{NC12}, 'Haloalkanes and Haloarenes', halogen exchange (Finkelstein reaction)", seconds=35),

    Q(T_HX, "C-X bond and preparation", "Intermediate", "statement_pair",
      *sp("The order of reactivity of alcohols with a given halogen acid is 1° > 2° > 3°.", False,
          "The order of reactivity of the halogen acids with a given alcohol is HI > HBr > HCl.", True),
      "Preparation of haloalkanes from alcohols and HX",
      "NCERT: the order of reactivity of alcohols with a given haloacid is 3° > 2° > 1°; tertiary alcohols react "
      "with concentrated HCl even at room temperature, while primary and secondary alcohols need ZnCl₂. For the "
      "acids, HI > HBr > HCl.",
      ["Statement I: reversed order → false", "Statement II: HI > HBr > HCl → true"],
      ncert=f"{NC12}, 'Haloalkanes and Haloarenes', preparation from alcohols", seconds=35),

    Q(T_HX, "C-X bond and preparation", "Intermediate", "assertion_reason",
      *ar("2-Bromopentane, heated with alcoholic KOH, gives pent-2-ene as the major product rather than pent-1-ene.",
          True,
          "In dehydrohalogenation, the preferred alkene is the one with the greater number of alkyl groups "
          "attached to the doubly bonded carbon atoms (Zaitsev rule).", True, explains=True),
      "Zaitsev (Saytzeff) rule",
      "β-Hydrogen can be lost from C-1 (giving pent-1-ene, one alkyl group on the C=C) or from C-3 (giving "
      "pent-2-ene, two alkyl groups on the C=C). The more substituted alkene is preferred, as the rule states.",
      ["A: pent-2-ene is major → true", "R: Zaitsev rule → true", "R is the rule that predicts A → R explains A"],
      ncert=f"{NC12}, 'Haloalkanes and Haloarenes', elimination reactions", seconds=40),

    Q(T_HX, "Polyhalogen compounds", "Intermediate", "match_list",
      *ml("Match the common name in List-I with the formula in List-II.",
          ["Ethylidene chloride", "Ethylene dichloride", "Methylene chloride", "Vinyl chloride"],
          ["CH₂Cl₂", "CH₂=CHCl", "ClCH₂–CH₂Cl", "CH₃CHCl₂"],
          "IV III I II", ["III IV I II", "IV III II I", "IV I III II"], "D"),
      "Common names of di- and polyhalogen compounds",
      "Ethylidene (CH₃CH=) gives the geminal dihalide CH₃CHCl₂ (1,1-dichloroethane). Ethylene dichloride is the "
      "vicinal dihalide ClCH₂CH₂Cl (1,2-dichloroethane). Methylene chloride is CH₂Cl₂ (dichloromethane). Vinyl "
      "chloride is CH₂=CHCl (chloroethene).",
      ["A → CH₃CHCl₂ (IV)", "B → ClCH₂CH₂Cl (III)", "C → CH₂Cl₂ (I)", "D → CH₂=CHCl (II)"],
      ncert=f"{NC12}, 'Haloalkanes and Haloarenes', nomenclature (common names)", seconds=40),

    Q(T_HX, "C-X bond and preparation", "Intermediate", "multi_statement",
      *ms("Which of the following statements about the physical properties of haloalkanes are correct?",
          [("Methyl chloride, methyl bromide, ethyl chloride and some chlorofluoromethanes are gases at room "
            "temperature.", True),
           ("All chloroalkanes are denser than water.", False),
           ("For the same alkyl group, alkyl iodides have lower boiling points than alkyl chlorides.", False),
           ("Haloalkanes tend to dissolve in organic solvents.", True),
           ("Pure alkyl halides are colourless, but bromides and iodides develop colour on exposure to light.",
            True)],
          [["a", "b", "d"], ["b", "c", "e"], ["a", "c", "e"]], "B"),
      "Physical properties of haloalkanes",
      "NCERT: the lower members listed are gases; bromo, iodo and polychloro derivatives are heavier than water, "
      "but monochloroalkanes such as n-propyl chloride are lighter; boiling points rise in the order "
      "RCl < RBr < RI with the increase in size and van der Waals forces; haloalkanes dissolve in organic "
      "solvents; bromides and iodides develop colour in light.",
      ["(a) true", "(b) e.g. n-propyl chloride is lighter than water → false", "(c) RI > RBr > RCl → false",
       "(d) true", "(e) true"],
      why_others_wrong="Every other option includes (b) or (c), both false.",
      ncert=f"{NC12}, 'Haloalkanes and Haloarenes', physical properties", seconds=60),

    N(T_HX, "C-X bond and preparation", "Advanced",
      "7.85 g of 2-chloropropane is heated with alcoholic KOH and the alkene formed is passed into bromine "
      "dissolved in CCl₄. Assuming both reactions are complete, the mass of the dibromo compound formed is "
      "(C = 12, H = 1, Cl = 35.5, Br = 80):",
      ["18.8 g", "20.2 g", "12.3 g", "10.1 g"], "B", v_1202,
      "Two-step stoichiometry: dehydrohalogenation, then addition of bromine",
      "CH₃CHClCH₃ → CH₃CH=CH₂ (alc. KOH); CH₃CH=CH₂ + Br₂ → CH₃CHBrCH₂Br (1,2-dibromopropane). Each step is 1 : 1.",
      ["M(C₃H₇Cl) = 36 + 7 + 35.5 = 78.5 g mol⁻¹ → 0.10 mol", "0.10 mol propene → 0.10 mol C₃H₆Br₂",
       "M(C₃H₆Br₂) = 36 + 6 + 160 = 202 g mol⁻¹ → 20.2 g"],
      why_others_wrong="18.8 g is the mass of 0.10 mol of 1,2-dibromoethane (the wrong alkene). 12.3 g is 0.10 mol "
                       "of a monobromopropane (HBr instead of Br₂). 10.1 g halves the moles.",
      ncert=f"{NC12}, 'Haloalkanes and Haloarenes', elimination reactions; {NC11}, 'Hydrocarbons', addition of "
            "halogens", seconds=70),

    Q(T_HX, "SN1 and SN2", "Advanced", "multi_statement",
      *ms("Which of the following statements about haloarenes are correct?",
          [("A nitro group meta to the chlorine has practically no effect on the reactivity of chlorobenzene "
            "towards nucleophiles.", True),
           ("The C–Cl bond in chlorobenzene is shorter than in chloromethane, because the carbon bonded to Cl is "
            "sp² hybridised.", True),
           ("Haloarenes are more reactive than haloalkanes towards nucleophilic substitution, because the sp² "
            "carbon is more electrophilic.", False),
           ("Chlorobenzene is converted into phenol by aqueous NaOH at room temperature.", False),
           ("1-Chloro-2,4-dinitrobenzene is hydrolysed under milder conditions than 1-chloro-4-nitrobenzene.",
            True)],
          [["a", "b", "c"], ["b", "d", "e"], ["a", "c", "d"]], "C"),
      "Nucleophilic substitution in haloarenes",
      "An –NO₂ group at the ortho or para position stabilises the negative charge of the intermediate by resonance; "
      "at the meta position it cannot, so no effect is observed. More nitro groups at o/p allow milder conditions "
      "(4-nitro: 443 K; 2,4-dinitro: 368 K). The sp² carbon holds the C–Cl electron pair more tightly, giving a "
      "shorter, stronger bond; haloarenes are therefore less reactive, and chlorobenzene needs 623 K and 300 atm "
      "to give phenol.",
      ["(a) true", "(b) true", "(c) haloarenes are less reactive → false", "(d) needs 623 K, 300 atm → false",
       "(e) true"],
      why_others_wrong="Every other option includes (c) or (d), both false.",
      ncert=f"{NC12}, 'Haloalkanes and Haloarenes', reactions of haloarenes (nucleophilic substitution)",
      seconds=70),

    Q(T_HX, "C-X bond and preparation", "Advanced", "assertion_reason",
      *ar("Haloalkanes are only very slightly soluble in water.", True,
          "The carbon–halogen bond in a haloalkane is non-polar.", False),
      "Solubility of haloalkanes",
      "The C–X bond is polar (halogen more electronegative than carbon). Haloalkanes are only slightly soluble "
      "because the energy released in forming new haloalkane–water attractions is less than the energy needed to "
      "break the hydrogen bonds between water molecules.",
      ["A: only very slightly soluble → true", "R: C–X is polar (C δ⁺, X δ⁻) → false"],
      ncert=f"{NC12}, 'Haloalkanes and Haloarenes', nature of C–X bond; physical properties (solubility)",
      seconds=35),
]

# ================================================================ Organic Compounds Containing Oxygen (1205-1223)
# 1205: C6H5CHCl2 + H2O (373 K) -> C6H5CHO ; 16.1 g
assert mm(C=7, H=6, Cl=2) == 161
n_1205 = F(161, 10) / mm(C=7, H=6, Cl=2)
v_1205 = g(n_1205 * mm(C=7, H=6, O=1))
assert n_1205 == F(1, 10) and v_1205 == "10.6 g"
assert g(n_1205 * mm(C=7, H=6, O=2)) == "12.2 g" and g(n_1205 * mm(C=7, H=8, O=1)) == "10.8 g"
# 1206: CH3COOH --LiAlH4--> CH3CH2OH ; 6.0 g
n_1206 = F(6) / mm(C=2, H=4, O=2)
v_1206 = g(n_1206 * mm(C=2, H=6, O=1))
assert n_1206 == F(1, 10) and v_1206 == "4.6 g" and g(n_1206 * mm(C=2, H=4, O=1)) == "4.4 g"
assert g(n_1206 * mm(C=2, H=6, O=1) / 2, 2) == "2.30 g" and g(n_1206 * mm(C=1, H=4, O=1)) == "3.2 g"
# 1207: 2CH3COOH -> (CH3CO)2O + H2O ; 12.0 g
n_1207 = F(12) / 60
v_1207 = g(n_1207 / 2 * mm(C=4, H=6, O=3))
assert mm(C=4, H=6, O=3) == 102 and v_1207 == "10.2 g" and g(n_1207 * 102) == "20.4 g"
assert g(n_1207 / 4 * 102) == "5.1 g" and g(12 - n_1207 * 18) == "8.4 g"
# 1211: CH3CN + C6H5MgBr, then H3O+ -> C6H5COCH3 ; 4.1 g
n_1211 = F(41, 10) / mm(C=2, H=3, N=1)
v_1211 = g(n_1211 * mm(C=8, H=8, O=1))
assert n_1211 == F(1, 10) and v_1211 == "12.0 g" and g(n_1211 * mm(C=7, H=6, O=2)) == "12.2 g"
assert g(n_1211 * mm(C=7, H=6, O=1)) == "10.6 g" and g(n_1211 * 120 / 2) == "6.0 g"
# 1212: C6H5SO3H -> (fused NaOH) C6H5ONa -> (H+) C6H5OH ; 15.8 g
assert mm(C=6, H=6, O=3, S=1) == 158
n_1212 = F(158, 10) / 158
v_1212 = g(n_1212 * mm(C=6, H=6, O=1))
assert v_1212 == "9.4 g" and g(n_1212 * mm(C=6, H=5, O=1, Na=1)) == "11.6 g"
assert g(n_1212 * mm(C=6, H=6)) == "7.8 g" and g(n_1212 * 94 / 2) == "4.7 g"
# 1213: C6H5OCH3 + HI -> C6H5OH + CH3I ; 10.8 g
n_1213 = F(108, 10) / mm(C=7, H=8, O=1)
v_1213 = g(n_1213 * mm(C=1, H=3, I=1))
assert n_1213 == F(1, 10) and v_1213 == "14.2 g" and g(n_1213 * mm(C=6, H=5, I=1)) == "20.4 g"
assert g(n_1213 * 94) == "9.4 g" and g(n_1213 * 142 / 2) == "7.1 g"
# 1218: self aldol needs an alpha-hydrogen
alpha_h = {"ethanal": 3, "propanone": 6, "methanal": 0, "benzaldehyde": 0, "2,2-dimethylpropanal": 0,
           "acetophenone": 3, "propanal": 2}
v_1218 = str(sum(1 for n in alpha_h.values() if n > 0))
assert v_1218 == "4"
# 1219: pKa values (NCERT table); phenol 10.0
pka = {"ethanol": 15.9, "p-nitrophenol": 7.1, "o-cresol": 10.2, "picric acid": 0.71, "water": 15.7,
       "m-nitrophenol": 8.3, "p-cresol": 10.2}
v_1219 = str(sum(1 for v in pka.values() if v < 10.0))
assert v_1219 == "3"

QUESTIONS += [
    N(T_OX, "Aldehydes and ketones", "Basic",
      "Benzal chloride, C₆H₅CHCl₂, obtained by side-chain chlorination of toluene, is hydrolysed at 373 K to "
      "benzaldehyde. The mass of benzaldehyde formed from 16.1 g of benzal chloride, assuming complete conversion, "
      "is (C = 12, H = 1, O = 16, Cl = 35.5):",
      ["12.2 g", "10.8 g", "5.3 g", "10.6 g"], "D", v_1205,
      "Preparation of benzaldehyde from toluene via benzal chloride",
      "C₆H₅CHCl₂ + H₂O → C₆H₅CHO + 2HCl (the gem-diol formed loses water). Mole ratio 1 : 1.",
      ["M(C₆H₅CHCl₂) = 84 + 6 + 71 = 161 g mol⁻¹ → 0.10 mol", "M(C₆H₅CHO) = 106 g mol⁻¹",
       "Mass = 0.10 × 106 = 10.6 g"],
      why_others_wrong="12.2 g is 0.10 mol of benzoic acid (over-oxidation is not involved). 10.8 g is 0.10 mol of "
                       "benzyl alcohol. 5.3 g halves the moles.",
      ncert=f"{NC12}, 'Aldehydes, Ketones and Carboxylic Acids', preparation of aromatic aldehydes (side-chain "
            "chlorination followed by hydrolysis)", seconds=40),

    N(T_OX, "Carboxylic acids", "Basic",
      "6.0 g of ethanoic acid is reduced completely with lithium aluminium hydride, and the product is hydrolysed. "
      "The mass of the organic product is (C = 12, H = 1, O = 16):",
      ["4.4 g", "4.6 g", "3.2 g", "2.30 g"], "B", v_1206,
      "Reduction of carboxylic acids",
      "LiAlH₄ reduces a carboxylic acid all the way to the primary alcohol: CH₃COOH → CH₃CH₂OH.",
      ["n(CH₃COOH) = 6.0/60 = 0.10 mol", "Product: ethanol, 46 g mol⁻¹", "Mass = 0.10 × 46 = 4.6 g"],
      why_others_wrong="4.4 g assumes the reduction stops at ethanal. 3.2 g is 0.10 mol of methanol (a carbon "
                       "lost). 2.30 g halves the moles.",
      ncert=f"{NC12}, 'Aldehydes, Ketones and Carboxylic Acids', reactions of carboxylic acids (reduction)",
      seconds=35),

    N(T_OX, "Carboxylic acids", "Basic",
      "Ethanoic acid is heated with P₂O₅, which removes water: 2CH₃COOH → (CH₃CO)₂O + H₂O. The mass of ethanoic "
      "anhydride obtained from 12.0 g of ethanoic acid, assuming complete conversion, is (C = 12, H = 1, O = 16):",
      ["20.4 g", "5.1 g", "10.2 g", "8.4 g"], "C", v_1207,
      "Formation of acid anhydrides",
      "Two molecules of acid lose one molecule of water to give one molecule of anhydride.",
      ["n(CH₃COOH) = 12.0/60 = 0.20 mol", "n(anhydride) = 0.20/2 = 0.10 mol",
       "M((CH₃CO)₂O) = 102 g mol⁻¹ → 10.2 g (check: 12.0 − 0.10 × 18 = 10.2 g)"],
      why_others_wrong="20.4 g takes a 1 : 1 ratio. 5.1 g divides by 2 twice. 8.4 g subtracts one water for each "
                       "molecule of acid (0.20 mol) instead of for each pair.",
      ncert=f"{NC12}, 'Aldehydes, Ketones and Carboxylic Acids', formation of anhydride", seconds=40),

    Q(T_OX, "Alcohols", "Basic", "statement_pair",
      *sp("Acid-catalysed hydration of propene gives propan-1-ol as the main product.", False,
          "Catalytic hydrogenation of an aldehyde gives a secondary alcohol.", False),
      "Preparation of alcohols from alkenes and carbonyl compounds",
      "Acid-catalysed hydration follows Markovnikov's rule: H adds to C-1 and OH to C-2, giving propan-2-ol. "
      "Hydrogenation (H₂ with Pt, Pd or Ni) of an aldehyde gives a primary alcohol; ketones give secondary "
      "alcohols.",
      ["Statement I: Markovnikov → propan-2-ol → false", "Statement II: RCHO → RCH₂OH (primary) → false"],
      ncert=f"{NC12}, 'Alcohols, Phenols and Ethers', preparation of alcohols", seconds=30),

    Q(T_OX, "Carboxylic acids", "Basic", "assertion_reason",
      *ar("Benzoic acid is highly soluble in cold water.", False,
          "Aliphatic carboxylic acids with up to four carbon atoms are miscible with water because they form "
          "hydrogen bonds with it.", True),
      "Solubility of carboxylic acids",
      "NCERT: simple aliphatic acids up to four carbons are miscible with water (hydrogen bonding); solubility falls "
      "as the hydrocarbon part grows, and benzoic acid is nearly insoluble in cold water.",
      ["A: benzoic acid is nearly insoluble in cold water → false", "R: true"],
      ncert=f"{NC12}, 'Aldehydes, Ketones and Carboxylic Acids', physical properties of carboxylic acids",
      seconds=30),

    Q(T_OX, "Alcohols", "Basic", "match_list",
      *ml("Match the alcohol in List-I with its class in List-II.",
          ["CH₂=CH–CH₂–OH", "C₆H₅–CH₂–OH", "CH₂=CH–OH", "(CH₃)₃C–OH"],
          ["Vinylic alcohol", "Benzylic alcohol", "Tertiary (3°) alcohol", "Allylic alcohol"],
          "IV II I III", ["II IV I III", "IV II III I", "I II IV III"], "A"),
      "Classification of alcohols",
      "In an allylic alcohol the –OH is on an sp³ carbon next to a C=C; in a benzylic alcohol it is on an sp³ carbon "
      "next to a benzene ring; in a vinylic alcohol it is on a C=C carbon itself; a tertiary alcohol has the –OH on "
      "a carbon bonded to three other carbons.",
      ["A: allylic (IV)", "B: benzylic (II)", "C: vinylic (I)", "D: tertiary (III)"],
      ncert=f"{NC12}, 'Alcohols, Phenols and Ethers', classification", seconds=35),

    N(T_OX, "Aldehydes and ketones", "Intermediate",
      "4.1 g of ethanenitrile, CH₃CN, is treated with an excess of phenylmagnesium bromide, and the product is "
      "hydrolysed. Assuming complete conversion, the mass of ketone formed is (C = 12, H = 1, N = 14, O = 16):",
      ["12.2 g", "10.6 g", "6.0 g", "12.0 g"], "D", v_1211,
      "Preparation of ketones from nitriles and Grignard reagents",
      "The Grignard reagent adds to the C≡N group; hydrolysis of the imine salt gives a ketone: CH₃CN + C₆H₅MgBr → "
      "(H₃O⁺) C₆H₅COCH₃ (acetophenone).",
      ["n(CH₃CN) = 4.1/41 = 0.10 mol", "Product: acetophenone, C₈H₈O = 120 g mol⁻¹", "Mass = 12.0 g"],
      why_others_wrong="12.2 g is 0.10 mol of benzoic acid and 10.6 g is 0.10 mol of benzaldehyde; neither is "
                       "formed. 6.0 g halves the moles.",
      ncert=f"{NC12}, 'Aldehydes, Ketones and Carboxylic Acids', preparation of ketones from nitriles",
      seconds=45),

    N(T_OX, "Phenols", "Intermediate",
      "15.8 g of benzenesulphonic acid is fused with molten NaOH, and the product is acidified. Assuming complete "
      "conversion, the mass of phenol formed is (C = 12, H = 1, O = 16, S = 32, Na = 23):",
      ["9.4 g", "11.6 g", "7.8 g", "4.7 g"], "A", v_1212,
      "Preparation of phenol from benzenesulphonic acid",
      "C₆H₅SO₃H → (fused NaOH) C₆H₅ONa → (H⁺) C₆H₅OH. One mole of sulphonic acid gives one mole of phenol.",
      ["M(C₆H₅SO₃H) = 72 + 6 + 32 + 48 = 158 g mol⁻¹ → 0.10 mol", "Phenol: 94 g mol⁻¹ → 9.4 g"],
      why_others_wrong="11.6 g is the mass of sodium phenoxide, before acidification. 7.8 g is 0.10 mol of benzene. "
                       "4.7 g halves the moles.",
      ncert=f"{NC12}, 'Alcohols, Phenols and Ethers', preparation of phenols (from benzenesulphonic acid)",
      seconds=40),

    N(T_OX, "Ethers", "Intermediate",
      "10.8 g of anisole (methoxybenzene) is heated with excess HI until it is completely cleaved. The mass of "
      "the alkyl iodide formed is (C = 12, H = 1, O = 16, I = 127):",
      ["14.2 g", "20.4 g", "9.4 g", "7.1 g"], "A", v_1213,
      "Cleavage of alkyl aryl ethers by HI",
      "The O–CH₃ bond breaks (the O–aryl bond has partial double bond character), so the products are phenol and "
      "methyl iodide: C₆H₅OCH₃ + HI → C₆H₅OH + CH₃I.",
      ["n(anisole) = 10.8/108 = 0.10 mol", "CH₃I = 142 g mol⁻¹ → 14.2 g"],
      why_others_wrong="20.4 g is 0.10 mol of iodobenzene, which is not formed. 9.4 g is the mass of phenol, the "
                       "other product. 7.1 g halves the moles.",
      ncert=f"{NC12}, 'Alcohols, Phenols and Ethers', reactions of ethers (cleavage of C–O bond)", seconds=40),

    Q(T_OX, "Aldehydes and ketones", "Intermediate", "statement_pair",
      *sp("Nitration of benzaldehyde gives mainly o- and p-nitrobenzaldehyde.", False,
          "Bromination of benzoic acid in the presence of FeBr₃ gives mainly p-bromobenzoic acid.", False),
      "Directive influence of –CHO and –COOH",
      "Both –CHO and –COOH are electron-withdrawing, deactivating and meta-directing. Nitration of benzaldehyde gives "
      "m-nitrobenzaldehyde, and bromination of benzoic acid gives m-bromobenzoic acid.",
      ["Statement I: –CHO is meta-directing → false", "Statement II: –COOH is meta-directing → false"],
      ncert=f"{NC12}, 'Aldehydes, Ketones and Carboxylic Acids', electrophilic substitution reactions",
      seconds=35),

    Q(T_OX, "Aldehydes and ketones", "Intermediate", "assertion_reason",
      *ar("The addition of HCN to ethanal is catalysed by a base.", True,
          "The base converts HCN into the cyanide ion, a stronger nucleophile, which adds readily to the carbonyl "
          "carbon.", True, explains=True),
      "Base catalysis in cyanohydrin formation",
      "With pure HCN the reaction is very slow. A base generates CN⁻, which is a much stronger nucleophile than "
      "HCN; it attacks the carbonyl carbon, and the alkoxide formed takes a proton from HCN to give the "
      "cyanohydrin.",
      ["A: base catalyses the reaction → true", "R: base gives CN⁻, the stronger nucleophile → true",
       "That is why the base speeds up the addition → R explains A"],
      ncert=f"{NC12}, 'Aldehydes, Ketones and Carboxylic Acids', nucleophilic addition (addition of HCN)",
      seconds=35),

    Q(T_OX, "Aldehydes and ketones", "Intermediate", "match_list",
      *ml("Each reagent in List-I reacts with a carbonyl compound, >C=O. Match it with the group formed in the "
          "product (List-II).",
          ["Hydrazine, NH₂NH₂", "Phenylhydrazine, C₆H₅NHNH₂", "Semicarbazide, NH₂CONHNH₂",
           "Hydroxylamine, NH₂OH"],
          [">C=N–OH", ">C=N–NH–CO–NH₂", ">C=N–NH₂", ">C=N–NH–C₆H₅"],
          "III IV II I", ["IV III II I", "III IV I II", "II IV III I"], "D"),
      "Reactions with ammonia derivatives",
      "Ammonia derivatives Z–NH₂ condense with the carbonyl group, losing water, to give >C=N–Z: hydrazone "
      "(Z = NH₂), phenylhydrazone (Z = NHC₆H₅), semicarbazone (Z = NHCONH₂) and oxime (Z = OH).",
      ["A → hydrazone, >C=N–NH₂ (III)", "B → phenylhydrazone, >C=N–NHC₆H₅ (IV)",
       "C → semicarbazone, >C=N–NHCONH₂ (II)", "D → oxime, >C=N–OH (I)"],
      ncert=f"{NC12}, 'Aldehydes, Ketones and Carboxylic Acids', reactions with ammonia and its derivatives",
      seconds=45),

    Q(T_OX, "Carboxylic acids", "Intermediate", "multi_statement",
      *ms("Which of the following statements about carboxylic acids and their derivatives are correct?",
          [("Carboxylic acids react with PCl₃ to give acyl chlorides.", True),
           ("Nitriles are hydrolysed, through amides, to carboxylic acids in the presence of H⁺ or OH⁻.", True),
           ("Carboxylic acids react with alkalis but not with metals such as sodium.", False),
           ("Esterification of a carboxylic acid with an alcohol is an irreversible reaction.", False),
           ("Acyl chlorides and acid anhydrides are hydrolysed by water to give carboxylic acids.", True)],
          [["a", "b", "c"], ["b", "d", "e"], ["a", "c", "d"]], "A"),
      "Preparation and reactions of carboxylic acids",
      "NCERT: acids give acyl chlorides with PCl₅, PCl₃ or SOCl₂; nitriles are hydrolysed to amides and then to "
      "acids; acids react with electropositive metals (liberating H₂) as well as with alkalis; esterification is "
      "reversible, so water is removed to shift the equilibrium; acyl chlorides and anhydrides are hydrolysed to "
      "acids.",
      ["(a) true", "(b) true", "(c) they react with Na too (H₂ evolved) → false",
       "(d) esterification is reversible → false", "(e) true"],
      why_others_wrong="Every other option includes (c) or (d), both false.",
      ncert=f"{NC12}, 'Aldehydes, Ketones and Carboxylic Acids', methods of preparation and chemical reactions of "
            "carboxylic acids", seconds=60),

    N(T_OX, "Aldehydes and ketones", "Advanced",
      "How many of the following can undergo self aldol condensation in the presence of dilute alkali?\n"
      "Ethanal, propanone, methanal, benzaldehyde, 2,2-dimethylpropanal, acetophenone, propanal",
      ["3", "4", "5", "7"], "B", v_1218,
      "Requirement of an α-hydrogen for aldol condensation",
      "Aldol condensation needs at least one α-hydrogen, which the base removes to form the carbanion (enolate). "
      "Methanal and benzaldehyde have no α-carbon bearing hydrogen; in 2,2-dimethylpropanal, (CH₃)₃C–CHO, the "
      "α-carbon carries no hydrogen.",
      ["α-H present: ethanal, propanone, acetophenone (CH₃ group), propanal", "No α-H: methanal, benzaldehyde, "
       "2,2-dimethylpropanal", "Count = 4"],
      why_others_wrong="3 usually misses acetophenone, whose methyl group supplies α-hydrogens. 5 counts "
                       "2,2-dimethylpropanal, whose α-carbon is quaternary. 7 counts every carbonyl compound.",
      ncert=f"{NC12}, 'Aldehydes, Ketones and Carboxylic Acids', aldol condensation", seconds=60),

    N(T_OX, "Phenols", "Advanced",
      "How many of the following are stronger acids than phenol?\n"
      "Ethanol, p-nitrophenol, o-cresol, picric acid (2,4,6-trinitrophenol), water, m-nitrophenol, p-cresol",
      ["2", "4", "3", "5"], "C", v_1219,
      "Effect of substituents on the acidity of phenol",
      "Electron-withdrawing –NO₂ groups stabilise the phenoxide ion and increase acidity (pKa: p-nitrophenol 7.1, "
      "m-nitrophenol 8.3, picric acid 0.71, against phenol 10.0). Electron-releasing –CH₃ groups decrease it "
      "(cresols pKa about 10.2). Ethanol (15.9) and water are weaker acids than phenol.",
      ["Stronger: p-nitrophenol, m-nitrophenol, picric acid", "Weaker: o-cresol, p-cresol, ethanol, water",
       "Count = 3"],
      why_others_wrong="2 leaves out m-nitrophenol (–NO₂ still withdraws electrons by −I at the meta position). 4 "
                       "or 5 count a cresol, whose methyl group makes it a weaker acid than phenol.",
      ncert=f"{NC12}, 'Alcohols, Phenols and Ethers', acidity of phenols (pKa table)", seconds=60),

    Q(T_OX, "Aldehydes and ketones", "Advanced", "direct",
      "Compound X, C₅H₁₀O, does not reduce Tollens' reagent but gives a yellow precipitate with iodine and NaOH. "
      "On Clemmensen reduction, X gives n-pentane. X is:",
      ["Pentan-3-one", "3-Methylbutan-2-one", "Pentanal", "Pentan-2-one"], "D",
      "Identifying a carbonyl compound from its tests",
      "No Tollens' test → a ketone, not an aldehyde. Iodoform test → a CH₃CO– group. Clemmensen reduction gives the "
      "alkane with the same carbon skeleton, so the chain must be unbranched.",
      ["Ketone (Tollens' negative) with CH₃CO– (iodoform positive)", "Unbranched C₅ chain (gives n-pentane)",
       "CH₃COCH₂CH₂CH₃ = pentan-2-one"],
      why_others_wrong="Pentan-3-one has no CH₃CO– group, so it gives no iodoform. 3-Methylbutan-2-one gives "
                       "2-methylbutane, not n-pentane. Pentanal is an aldehyde and reduces Tollens' reagent.",
      ncert=f"{NC12}, 'Aldehydes, Ketones and Carboxylic Acids', chemical reactions (Clemmensen reduction, "
            "haloform reaction, Tollens' test)", seconds=60),

    Q(T_OX, "Ethers", "Advanced", "multi_statement",
      *ms("Which of the following statements about ethers are correct?",
          [("Anisole reacts with CH₃Cl and anhydrous AlCl₃ to give mainly 2- and 4-methoxytoluene.", True),
           ("Nitration of anisole gives mainly 2- and 4-nitroanisole.", True),
           ("In the cleavage of ethers, the order of reactivity of the hydrogen halides is HI > HBr > HCl.", True),
           ("Ethers are prepared in good yield by heating tertiary alcohols with concentrated H₂SO₄ at 413 K.",
            False),
           ("Molecules of methoxymethane form hydrogen bonds with one another, like those of ethanol.", False)],
          [["a", "b", "d"], ["b", "c", "e"], ["a", "c", "e"]], "B"),
      "Preparation and reactions of ethers",
      "The –OCH₃ group activates the ring and directs to ortho and para positions (Friedel–Crafts, nitration). NCERT "
      "gives the order HI > HBr > HCl for cleavage. Acid dehydration of tertiary alcohols gives alkenes, because "
      "elimination competes. Ethers have no O–H, so they cannot hydrogen bond with one another.",
      ["(a) true", "(b) true", "(c) true", "(d) tertiary alcohols give alkenes → false",
       "(e) no O–H in ethers → false"],
      why_others_wrong="Every other option includes (d) or (e), both false.",
      ncert=f"{NC12}, 'Alcohols, Phenols and Ethers', ethers (preparation, physical and chemical properties)",
      seconds=60),

    Q(T_OX, "Alcohols", "Advanced", "statement_pair",
      *sp("In the acid-catalysed dehydration of ethanol to ethene, the first step is protonation of the oxygen atom "
          "of the alcohol.", True,
          "The last step of this mechanism is the loss of a water molecule from the carbocation.", False),
      "Mechanism of acid-catalysed dehydration of alcohols",
      "Step 1: protonation of the alcohol to give the oxonium ion. Step 2: loss of water to give the carbocation "
      "(the slowest, rate-determining step). Step 3: loss of a proton from the carbocation to give the alkene.",
      ["Statement I: protonation is step 1 → true",
       "Statement II: water is lost in step 2; step 3 is loss of H⁺ → false"],
      ncert=f"{NC12}, 'Alcohols, Phenols and Ethers', dehydration of alcohols (mechanism)", seconds=40),

    Q(T_OX, "Phenols", "Advanced", "assertion_reason",
      *ar("Phenol is a weaker acid than ethanoic acid.", True,
          "In the ethanoate ion the negative charge is delocalised over two electronegative oxygen atoms, whereas "
          "in the phenoxide ion it is delocalised over the less electronegative carbon atoms of the ring.", True,
          explains=True),
      "Relative acidity of carboxylic acids and phenols",
      "The carboxylate ion has two equivalent resonance structures with the negative charge on oxygen, so it is "
      "much more stabilised than phenoxide, where the canonical structures place the charge on ring carbons. The "
      "more stable conjugate base means the stronger acid.",
      ["A: pKa 4.76 (ethanoic) < 10.0 (phenol) → true", "R: true", "Stability of the conjugate base decides "
       "acidity → R explains A"],
      ncert=f"{NC12}, 'Aldehydes, Ketones and Carboxylic Acids', acidity of carboxylic acids", seconds=40),
]

# ================================================================ Organic Compounds Containing Nitrogen (1224-1233)
n_anil = F(93, 10) / mm(C=6, H=7, N=1)
assert mm(C=6, H=7, N=1) == 93 and n_anil == F(1, 10)
v_1225 = g(n_anil * mm(C=6, H=5, N=1, O=2))
assert v_1225 == "12.3 g" and g(n_anil * mm(C=7, H=5, N=1)) == "10.3 g" and g(n_anil * mm(C=6, H=5, Br=1)) == "15.7 g"
assert g(n_anil * 123 / 2) == "6.2 g"
# 1231: RCONH2 + Br2 + 4NaOH -> RNH2 + Na2CO3 + 2NaBr + 2H2O ; 5.9 g ethanamide
n_1231 = F(59, 10) / mm(C=2, H=5, N=1, O=1)
assert mm(C=2, H=5, N=1, O=1) == 59 and n_1231 == F(1, 10)
v_1231 = g(n_1231 * 4 * mm(Na=1, O=1, H=1))
assert v_1231 == "16.0 g" and g(n_1231 * 40) == "4.0 g" and g(n_1231 * 2 * 40) == "8.0 g"
assert g(n_1231 * 3 * 40) == "12.0 g"
# 1232: aniline -> acetanilide -> p-bromoacetanilide -> p-bromoaniline ; 9.3 g
v_1232 = g(n_anil * mm(C=6, H=6, Br=1, N=1))
assert v_1232 == "17.2 g" and g(n_anil * mm(C=8, H=9, N=1, O=1)) == "13.5 g"
assert g(n_anil * mm(C=8, H=8, Br=1, N=1, O=1)) == "21.4 g" and g(n_anil * mm(C=6, H=4, Br=3, N=1)) == "33.0 g"

QUESTIONS += [
    Q(T_NI, "Amines: basicity and identification", "Basic", "direct",
      "The amine (CH₃)₃C–NH₂ (2-methylpropan-2-amine) is classified as a:",
      ["secondary amine", "tertiary amine", "primary amine", "quaternary ammonium compound"], "C",
      "Classification of amines",
      "Amines are classified by the number of hydrogen atoms of NH₃ replaced by alkyl or aryl groups, not by the "
      "nature of the carbon bearing the nitrogen. Here only one H is replaced (by a tert-butyl group), so it is a "
      "primary amine.",
      ["N bonded to one carbon group and two H atoms", "→ primary (1°) amine",
       "(The carbon attached to N is tertiary, but that does not decide the class of an amine)"],
      why_others_wrong="Secondary and tertiary amines have two and three carbon groups on nitrogen. A quaternary "
                       "ammonium compound has four groups on a positively charged nitrogen.",
      ncert=f"{NC12}, 'Amines', structure and classification of amines", seconds=25),

    N(T_NI, "Diazonium salts", "Basic",
      "9.3 g of aniline is diazotised. The diazonium salt is converted into its fluoroborate, which is treated with "
      "aqueous sodium nitrite in the presence of copper powder, so that the diazo group is replaced by –NO₂. "
      "Assuming every step is complete, the mass of nitrobenzene formed is (C = 12, H = 1, N = 14, O = 16):",
      ["12.3 g", "10.3 g", "15.7 g", "6.2 g"], "A", v_1225,
      "Replacement of the diazo group by a nitro group",
      "C₆H₅NH₂ → C₆H₅N₂⁺ → C₆H₅N₂⁺BF₄⁻ → (NaNO₂, Cu) C₆H₅NO₂ + N₂. Every step is 1 : 1.",
      ["n(aniline) = 9.3/93 = 0.10 mol", "Nitrobenzene: 123 g mol⁻¹", "Mass = 12.3 g"],
      why_others_wrong="10.3 g is 0.10 mol of benzonitrile (the CuCN product). 15.7 g is 0.10 mol of bromobenzene. "
                       "6.2 g halves the moles.",
      ncert=f"{NC12}, 'Amines', reactions of diazonium salts (replacement by nitro group)", seconds=45),

    Q(T_NI, "Amines: basicity and identification", "Basic", "direct",
      "Amines behave as Lewis bases because:",
      ["they contain hydrogen atoms bonded to nitrogen", "nitrogen is more electronegative than carbon",
       "they are soluble in water", "the nitrogen atom has an unshared pair of electrons"], "D",
      "Basic character of amines",
      "The lone pair on nitrogen can be donated to an electron-pair acceptor such as H⁺ (forming R–NH₃⁺) or a "
      "Lewis acid. That is what makes amines bases.",
      ["Nitrogen in amines: three bonds + one lone pair", "Lone pair donated to H⁺ → ammonium ion"],
      why_others_wrong="Tertiary amines have no N–H bond yet are bases. The electronegativity of N and water "
                       "solubility do not by themselves make a compound a base (higher amines are insoluble but "
                       "still basic).",
      ncert=f"{NC12}, 'Amines', chemical reactions (basic character of amines)", seconds=25),

    Q(T_NI, "Amines: basicity and identification", "Intermediate", "statement_pair",
      *sp("Primary amines have lower boiling points than alcohols of comparable molecular mass.", True,
          "Methanamine reacts with benzoyl chloride to give N-methylbenzamide.", True),
      "Physical properties of amines; benzoylation",
      "The N–H···N hydrogen bond is weaker than O–H···O because nitrogen is less electronegative than oxygen, so "
      "amines boil lower than comparable alcohols (e.g. n-butylamine 350.8 K vs butan-1-ol 390.3 K). NCERT gives "
      "benzoylation: CH₃NH₂ + C₆H₅COCl → C₆H₅CONHCH₃ + HCl.",
      ["Statement I: weaker H-bonding in amines → true", "Statement II: benzoylation gives N-methylbenzamide → "
       "true"],
      ncert=f"{NC12}, 'Amines', physical properties; chemical reactions (benzoylation)", seconds=35),

    Q(T_NI, "Amines: basicity and identification", "Intermediate", "assertion_reason",
      *ar("An aqueous solution of methylamine gives a precipitate of ferric hydroxide with FeCl₃ solution.", True,
          "Methylamine is a base; in water it accepts a proton and produces hydroxide ions.", True, explains=True),
      "Basicity of aliphatic amines in water",
      "CH₃NH₂ + H₂O ⇌ CH₃NH₃⁺ + OH⁻. The hydroxide ions precipitate Fe³⁺ as hydrated ferric oxide: "
      "Fe³⁺ + 3OH⁻ → Fe(OH)₃.",
      ["A: brown precipitate of Fe(OH)₃ → true", "R: CH₃NH₂ produces OH⁻ in water → true",
       "The OH⁻ produced is what precipitates Fe(OH)₃ → R explains A"],
      ncert=f"{NC12}, 'Amines', basic character of amines", seconds=35),

    Q(T_NI, "Amines: basicity and identification", "Intermediate", "match_list",
      *ml("Match the amine in List-I with its IUPAC name in List-II.",
          ["C₆H₅N(CH₃)₂", "CH₃CH₂NHCH₃", "(C₂H₅)₃N", "H₂N–CH₂–CH₂–NH₂"],
          ["Ethane-1,2-diamine", "N,N-Diethylethanamine", "N-Methylethanamine", "N,N-Dimethylbenzenamine"],
          "IV III II I", ["III IV II I", "IV II III I", "IV III I II"], "B"),
      "IUPAC names of amines",
      "The longest alkyl chain (or benzene) gives the parent amine; other groups on nitrogen are cited with the "
      "locant N. A diamine gets the suffix -diamine with the locants of both nitrogen-bearing carbons.",
      ["A: benzenamine with two N-methyls → N,N-dimethylbenzenamine (IV)",
       "B: ethanamine with one N-methyl → N-methylethanamine (III)",
       "C: ethanamine with two N-ethyls → N,N-diethylethanamine (II)", "D: ethane-1,2-diamine (I)"],
      ncert=f"{NC12}, 'Amines', nomenclature", seconds=40),

    Q(T_NI, "Amines: basicity and identification", "Intermediate", "multi_statement",
      *ms("Which of the following statements about the basic strength of amines are correct?",
          [("In aqueous solution, the basic strength of an amine is decided by the combination of the inductive "
            "effect, solvation and steric hindrance of the alkyl groups.", True),
           ("The larger the Kb of an amine, the weaker it is as a base.", False),
           ("The smaller the pKb of an amine, the stronger it is as a base.", True),
           ("Bulky alkyl groups on nitrogen hinder the hydrogen bonding (solvation) of the substituted ammonium "
            "ion with water, which lowers the basic strength.", True),
           ("Among the ethyl-substituted amines in water, triethylamine is the strongest base.", False)],
          [["a", "b", "d"], ["b", "c", "e"], ["a", "d", "e"]], "C"),
      "Basicity of amines: Kb, pKb and the factors involved",
      "A larger Kb (smaller pKb) means a stronger base. In water, +I effect, solvation of the ammonium ion and "
      "steric hindrance together decide basicity; for the ethyl series the order is (C₂H₅)₂NH > (C₂H₅)₃N > "
      "C₂H₅NH₂ > NH₃.",
      ["(a) true", "(b) larger Kb → stronger base → false", "(c) true", "(d) true",
       "(e) diethylamine is the strongest → false"],
      why_others_wrong="Every other option includes (b) or (e), both false.",
      ncert=f"{NC12}, 'Amines', basic character of amines (structure–basicity relationship)", seconds=60),

    N(T_NI, "Amines: basicity and identification", "Advanced",
      "In the Hofmann bromamide degradation,\nRCONH₂ + Br₂ + 4NaOH → RNH₂ + Na₂CO₃ + 2NaBr + 2H₂O\n"
      "the minimum mass of NaOH needed to convert 5.9 g of ethanamide completely into methanamine is "
      "(C = 12, H = 1, N = 14, O = 16, Na = 23):",
      ["4.0 g", "8.0 g", "12.0 g", "16.0 g"], "D", v_1231,
      "Stoichiometry of the Hofmann bromamide reaction",
      "Four moles of NaOH are used per mole of amide (to form NaBr, Na₂CO₃ and to neutralise the reaction "
      "intermediates).",
      ["n(CH₃CONH₂) = 5.9/59 = 0.10 mol", "n(NaOH) = 4 × 0.10 = 0.40 mol", "Mass = 0.40 × 40 = 16.0 g"],
      why_others_wrong="4.0 g, 8.0 g and 12.0 g take 1, 2 or 3 mol of NaOH per mole of amide instead of the 4 shown "
                       "in the balanced equation.",
      ncert=f"{NC12}, 'Amines', preparation of amines (Hofmann bromamide degradation)", seconds=45),

    N(T_NI, "Amines: basicity and identification", "Advanced",
      "9.3 g of aniline is acetylated with ethanoic anhydride; the product is brominated with Br₂ in ethanoic acid "
      "to give the para-bromo compound, which is then hydrolysed. Assuming every step is complete, the mass of the "
      "final product is (C = 12, H = 1, N = 14, O = 16, Br = 80):",
      ["13.5 g", "17.2 g", "21.4 g", "33.0 g"], "B", v_1232,
      "Controlling the reactivity of aniline by acetylation",
      "Acetylation moderates the activating –NH₂ group so that only monobromination occurs (at the para position). "
      "Hydrolysis then removes the acetyl group, giving 4-bromoaniline.",
      ["C₆H₅NH₂ → C₆H₅NHCOCH₃ → p-BrC₆H₄NHCOCH₃ → p-BrC₆H₄NH₂", "n = 9.3/93 = 0.10 mol at every stage",
       "M(C₆H₆BrN) = 72 + 6 + 80 + 14 = 172 → 17.2 g"],
      why_others_wrong="13.5 g is the mass of acetanilide and 21.4 g that of p-bromoacetanilide (the steps before "
                       "hydrolysis). 33.0 g is 2,4,6-tribromoaniline, formed only if aniline itself is brominated.",
      ncert=f"{NC12}, 'Amines', electrophilic substitution (bromination of aniline via acetanilide)", seconds=70),

    Q(T_NI, "Diazonium salts", "Advanced", "assertion_reason",
      *ar("Ethanol reduces benzenediazonium chloride to benzene.", True,
          "In this reaction, ethanol is oxidised to ethanoic acid.", False),
      "Replacement of the diazo group by hydrogen",
      "Mild reducing agents such as hypophosphorous acid or ethanol replace –N₂⁺ by –H. NCERT's equation: "
      "ArN₂⁺Cl⁻ + CH₃CH₂OH → ArH + N₂ + CH₃CHO + HCl. Ethanol is oxidised only to ethanal.",
      ["A: C₆H₅N₂Cl + C₂H₅OH → C₆H₆ → true", "R: the oxidation product is ethanal, not ethanoic acid → false"],
      ncert=f"{NC12}, 'Amines', reactions of diazonium salts (replacement by hydrogen)", seconds=40),
]

# ================================================================ Biomolecules (1234-1243)
a_pct = 20
c_pct = (100 - 2 * a_pct) // 2
assert c_pct == 30
# 1241: (C6H10O5)n + nH2O -> nC6H12O6 ; C6H12O6 -> 2C2H5OH + 2CO2 ; 8.1 g
n_glu = F(81, 10) / mm(C=6, H=10, O=5)
assert mm(C=6, H=10, O=5) == 162 and n_glu == F(1, 20)
v_1241 = g(2 * n_glu * F(224, 10), 2, " L")
assert v_1241 == "2.24 L" and g(n_glu * F(224, 10), 2, " L") == "1.12 L"
assert g(F(81, 10) / 180 * 2 * F(224, 10), 2, " L") == "2.02 L"

QUESTIONS += [
    Q(T_BM, "Carbohydrates", "Basic", "direct",
      "Commercially, glucose is obtained by boiling which substance with dilute H₂SO₄ at 393 K under 2–3 bar "
      "pressure?",
      ["Starch", "Cellulose", "Sucrose", "Lactose"], "A",
      "Preparation of glucose",
      "NCERT: glucose is obtained commercially by hydrolysis of starch: (C₆H₁₀O₅)ₙ + nH₂O → nC₆H₁₂O₆ (dilute "
      "H₂SO₄, 393 K, 2–3 bar). In the laboratory it is made by boiling sucrose with dilute acid, which gives "
      "glucose and fructose.",
      ["Commercial source: starch", "Lab method: sucrose (gives glucose + fructose)"],
      why_others_wrong="Sucrose hydrolysis is the laboratory method and also gives fructose. Lactose gives galactose "
                       "as well. Cellulose is not the commercial source NCERT describes.",
      ncert=f"{NC12}, 'Biomolecules', preparation of glucose", seconds=25),

    Q(T_BM, "Vitamins", "Basic", "match_list",
      *ml("Match the vitamin in List-I with a source of it in List-II.",
          ["Vitamin D", "Vitamin E", "Vitamin C", "Vitamin B₁₂"],
          ["Citrus fruits, amla and green leafy vegetables", "Exposure to sunlight; fish and egg yolk",
           "Meat, fish, egg and curd", "Vegetable oils such as wheat germ oil and sunflower oil"],
          "II IV I III", ["IV II I III", "II IV III I", "II I IV III"], "C"),
      "Sources of vitamins",
      "From NCERT's table: vitamin D – exposure to sunlight, fish and egg yolk; vitamin E – vegetable oils like "
      "wheat germ oil and sunflower oil; vitamin C – citrus fruits, amla and green leafy vegetables; vitamin B₁₂ – "
      "meat, fish, egg and curd.",
      ["A → II", "B → IV", "C → I", "D → III"],
      ncert=f"{NC12}, 'Biomolecules', vitamins (sources and deficiency diseases table)", seconds=40),

    Q(T_BM, "Carbohydrates", "Basic", "statement_pair",
      *sp("Amylose is insoluble in water, whereas amylopectin is water soluble.", False,
          "Cellulose is a branched-chain polymer of β-D-glucose units.", False),
      "Starch and cellulose",
      "NCERT: amylose is the water-soluble component of starch (15–20%) and amylopectin is insoluble in water. "
      "Cellulose is a straight-chain polysaccharide of β-D-glucose units joined by C1–C4 glycosidic linkages.",
      ["Statement I: reversed → false", "Statement II: cellulose is unbranched → false"],
      ncert=f"{NC12}, 'Biomolecules', polysaccharides", seconds=30),

    N(T_BM, "Nucleic acids", "Intermediate",
      "In a sample of double-stranded DNA, 20% of the bases are adenine. The percentage of cytosine is:",
      ["20%", "60%", "40%", "30%"], "D", f"{c_pct}%",
      "Base pairing in DNA",
      "In double-stranded DNA, adenine pairs with thymine and guanine with cytosine, so A = T and G = C.",
      ["A = 20% → T = 20%", "G + C = 100 − 40 = 60%", "C = 60/2 = 30%"],
      why_others_wrong="20% equates cytosine with adenine. 60% is G + C together. 40% is A + T.",
      ncert=f"{NC12}, 'Biomolecules', structure of nucleic acids (base pairing)", seconds=30),

    Q(T_BM, "Nucleic acids", "Intermediate", "direct",
      "In a nucleoside, the base is attached to the pentose sugar at its:",
      ["5′ position", "1′ position", "3′ position", "2′ position"], "B",
      "Structure of nucleosides",
      "NCERT: a unit formed by the attachment of a base to the 1′ position of the sugar is a nucleoside. When the "
      "5′ position of the sugar carries a phosphate, the unit is a nucleotide.",
      ["Base–sugar link at C-1′ → nucleoside", "Phosphate at C-5′ → nucleotide"],
      why_others_wrong="The 5′ position carries the phosphate in a nucleotide, and 3′ and 5′ are joined in the "
                       "phosphodiester links of the chain. The 2′ position differs between ribose (OH) and "
                       "deoxyribose (H).",
      ncert=f"{NC12}, 'Biomolecules', chemical composition and structure of nucleic acids", seconds=30),

    Q(T_BM, "Amino acids and proteins", "Intermediate", "assertion_reason",
      *ar("Almost all enzymes are globular proteins.", True,
          "Enzymes are very specific for a particular reaction and for a particular substrate.", True),
      "Enzymes",
      "Both statements are NCERT facts about enzymes. That enzymes are proteins with a globular shape does not "
      "follow from their specificity, and their specificity is not why they are proteins, so R does not explain A.",
      ["A: enzymes are biocatalysts, almost all globular proteins → true", "R: high specificity → true",
       "R describes a different property → not the explanation"],
      ncert=f"{NC12}, 'Biomolecules', enzymes", seconds=30),

    Q(T_BM, "Nucleic acids", "Intermediate", "multi_statement",
      *ms("Which of the following statements about nucleic acids are correct?",
          [("The double-helix structure of DNA was proposed by James Watson and Francis Crick.", True),
           ("In nucleic acids, nucleotides are joined by phosphodiester linkages between the 5′ and 3′ carbon "
            "atoms of the pentose sugars.", True),
           ("DNA contains uracil.", False),
           ("Adenine and guanine are pyrimidine bases.", False),
           ("The sugar in RNA lacks an –OH group at the 2′ position.", False)],
          [["a", "b", "c"], ["b", "d"], ["a", "e"]], "C"),
      "Structure of nucleic acids",
      "Watson and Crick proposed the double helix; nucleotides are linked by 5′–3′ phosphodiester bonds. DNA "
      "contains A, G, C and T (uracil occurs in RNA instead of thymine). Adenine and guanine are purines; cytosine, "
      "thymine and uracil are pyrimidines. Ribose in RNA has a 2′-OH; deoxyribose in DNA lacks it.",
      ["(a) true", "(b) true", "(c) uracil is in RNA → false", "(d) A and G are purines → false",
       "(e) it is deoxyribose (DNA) that lacks the 2′-OH → false"],
      why_others_wrong="Every other option includes (c), (d) or (e), all false, or leaves out (a) or (b).",
      ncert=f"{NC12}, 'Biomolecules', nucleic acids", seconds=50),

    N(T_BM, "Carbohydrates", "Advanced",
      "8.1 g of a polysaccharide (C₆H₁₀O₅)ₙ is hydrolysed completely to glucose, and all the glucose is fermented: "
      "C₆H₁₂O₆ → 2C₂H₅OH + 2CO₂. The volume of CO₂ at STP is (C = 12, H = 1, O = 16; molar volume at STP = "
      "22.4 L mol⁻¹):",
      ["2.24 L", "1.12 L", "4.48 L", "2.02 L"], "A", v_1241,
      "Hydrolysis of a polysaccharide and fermentation of glucose",
      "Each C₆H₁₀O₅ unit (162 g mol⁻¹) gives one glucose molecule on hydrolysis, and each glucose gives two CO₂.",
      ["n(units) = 8.1/162 = 0.050 mol → 0.050 mol glucose", "n(CO₂) = 2 × 0.050 = 0.10 mol",
       "V = 0.10 × 22.4 = 2.24 L"],
      why_others_wrong="1.12 L takes one CO₂ per glucose. 4.48 L doubles again. 2.02 L uses 180 g mol⁻¹ (glucose) "
                       "instead of 162 g mol⁻¹ for the polysaccharide unit.",
      ncert=f"{NC12}, 'Biomolecules', polysaccharides; {NC12}, 'Alcohols, Phenols and Ethers', ethanol by "
            "fermentation", seconds=60),

    Q(T_BM, "Amino acids and proteins", "Advanced", "statement_pair",
      *sp("A protein found in a biological system with a unique three-dimensional structure and biological "
          "activity is called a native protein.", True,
          "The main forces that stabilise the secondary and tertiary structures of proteins are hydrogen bonds, "
          "disulphide linkages, van der Waals forces and electrostatic forces of attraction.", True),
      "Native proteins and the forces that stabilise protein structure",
      "Both are NCERT statements. When these stabilising interactions are disturbed (by heat or change of pH), the "
      "protein loses its biological activity: denaturation.",
      ["Statement I: definition of native protein → true", "Statement II: true as NCERT lists them"],
      ncert=f"{NC12}, 'Biomolecules', structure of proteins; denaturation", seconds=35),

    Q(T_BM, "Amino acids and proteins", "Advanced", "match_list",
      *ml("Match the amino acid in List-I with its one-letter code in List-II.",
          ["Lysine", "Phenylalanine", "Tyrosine", "Tryptophan"],
          ["Y", "W", "K", "F"],
          "III IV I II", ["IV III I II", "III IV II I", "III I IV II"], "D"),
      "Codes of the α-amino acids",
      "NCERT's table of amino acids gives: lysine K, phenylalanine F, tyrosine Y, tryptophan W (the first letters L, "
      "P and T belong to leucine, proline and threonine).",
      ["A: lysine → K (III)", "B: phenylalanine → F (IV)", "C: tyrosine → Y (I)", "D: tryptophan → W (II)"],
      ncert=f"{NC12}, 'Biomolecules', amino acids (table of natural amino acids)", seconds=40),
]

# ================================================================ Principles Related to Practical Chemistry (1244-1250)
v_1245 = F(2, 100) * 250 / F(1, 10)
assert v_1245 == 50 and F(1, 10) * 250 / F(2, 100) == 1250 and F(2, 100) * 250 / 1 == 5
n_acet = F(135, 10) / mm(C=8, H=9, N=1, O=1)
assert n_acet == F(1, 10) and mm(C=8, H=8, N=2, O=3) == 180
v_1247 = g(n_acet * 180 * F(70, 100))
assert v_1247 == "12.6 g" and g(n_acet * 180) == "18.0 g" and g(F(135, 10) * F(70, 100), 2) == "9.45 g"
assert g(n_acet * mm(C=6, H=6, N=2, O=2) * F(70, 100), 2) == "9.66 g"
# 1249: 25.0 mL portions; NaOH 20.0 mL x 0.10 M ; KMnO4 40.0 mL x 0.020 M ; 2MnO4- : 5C2O4(2-)
mmol_oxalic = F(20) * F(1, 10) / 2
mmol_total = F(40) * F(2, 100) * F(5, 2)
c_1249 = (mmol_total - mmol_oxalic) / 25
assert mmol_oxalic == 1 and mmol_total == 2 and c_1249 == F(4, 100)
assert mmol_total / 25 == F(8, 100) and (mmol_total + mmol_oxalic) / 25 == F(12, 100)
assert (F(40) * F(2, 100) * 2 - mmol_oxalic) / 25 == F(24, 1000)

QUESTIONS += [
    Q(T_PR, "Preparations", "Basic", "direct",
      "A ferric hydroxide sol is prepared by adding ferric chloride solution drop by drop to:",
      ["ice-cold distilled water", "boiling distilled water", "sodium hydroxide solution",
       "ammonium hydroxide solution"], "B",
      "Preparation of a lyophobic sol by hydrolysis",
      "FeCl₃ is hydrolysed in boiling water: FeCl₃ + 3H₂O → Fe(OH)₃ (sol) + 3HCl, giving a reddish-brown sol. The "
      "Fe(OH)₃ particles adsorb Fe³⁺ ions, which keep the sol stable.",
      ["Add FeCl₃ dropwise to boiling water", "Hydrolysis → Fe(OH)₃ sol (reddish brown)"],
      why_others_wrong="In cold water hydrolysis is too slow. NaOH or NH₄OH solution gives a precipitate of Fe(OH)₃, "
                       "not a sol.",
      ncert=f"{LAB}, preparation of lyophobic sols (ferric hydroxide)", seconds=25),

    N(T_PR, "Titrimetric analysis", "Basic",
      "The volume of 0.10 M oxalic acid solution needed to prepare 250 mL of 0.020 M oxalic acid solution by "
      "dilution is:",
      ["200 mL", "5.0 mL", "50 mL", "1250 mL"], "C", f"{int(v_1245)} mL",
      "Dilution (M₁V₁ = M₂V₂)",
      "The number of moles of solute does not change on dilution.",
      ["M₁V₁ = M₂V₂", "0.10 × V₁ = 0.020 × 250", "V₁ = 50 mL (made up to 250 mL with water)"],
      why_others_wrong="200 mL is the water added, not the volume of stock solution. 1250 mL inverts the ratio of "
                       "molarities. 5.0 mL uses 1.0 M for the stock solution.",
      ncert=f"{LAB}, titrimetric analysis (preparation of standard solutions)", seconds=30),

    Q(T_PR, "Preparations", "Intermediate", "statement_pair",
      *sp("Starch forms a lyophilic sol when warmed and stirred with water.", True,
          "Arsenious sulphide forms a lyophilic sol.", False),
      "Lyophilic and lyophobic sols",
      "Starch, gum and egg albumin form lyophilic (solvent-loving) sols directly with water. Arsenious sulphide "
      "sol is lyophobic; it is prepared by a chemical reaction (double decomposition of As₂O₃ with H₂S).",
      ["Statement I: starch → lyophilic → true", "Statement II: As₂S₃ → lyophobic → false"],
      ncert=f"{LAB}, preparation of lyophilic and lyophobic sols", seconds=30),

    N(T_PR, "Preparations", "Intermediate",
      "13.5 g of acetanilide is nitrated to p-nitroacetanilide, and the yield of the purified product is 70%. The "
      "mass of p-nitroacetanilide obtained is (C = 12, H = 1, N = 14, O = 16):",
      ["18.0 g", "9.45 g", "9.66 g", "12.6 g"], "D", v_1247,
      "Percentage yield in a laboratory preparation",
      "C₆H₅NHCOCH₃ + HNO₃ → p-O₂NC₆H₄NHCOCH₃ + H₂O; one mole of acetanilide gives at most one mole of product.",
      ["M(acetanilide) = 135 g mol⁻¹ → 0.10 mol", "M(p-nitroacetanilide, C₈H₈N₂O₃) = 180 g mol⁻¹",
       "Theoretical 18.0 g × 0.70 = 12.6 g"],
      why_others_wrong="18.0 g is the theoretical (100%) yield. 9.45 g takes 70% of the mass of acetanilide. "
                       "9.66 g is 70% of 0.10 mol of p-nitroaniline, the product after hydrolysis, which is not "
                       "formed here.",
      ncert=f"{LAB}, preparation of p-nitroacetanilide", seconds=45),

    Q(T_PR, "Detection of elements and functional groups", "Intermediate", "match_list",
      *ml("Match the substance or group in List-I with the observation in its laboratory test in List-II.",
          ["Carbohydrate (Molisch's test)", "Oil or fat (heating with KHSO₄)", "Protein (ninhydrin test)",
           "Ketone (sodium nitroprusside test)"],
          ["Violet ring at the junction of the two layers", "Blue-violet colour",
           "Red colour in alkaline solution", "Pungent smell of acrolein"],
          "I IV II III", ["IV I II III", "I IV III II", "II IV I III"], "A"),
      "Tests for carbohydrates, fats, proteins and ketones",
      "Molisch's test (α-naphthol, then conc. H₂SO₄ down the side) gives a violet ring for carbohydrates. Heating a "
      "fat or oil with KHSO₄ gives acrolein, with a pungent smell. Ninhydrin gives a blue-violet colour with "
      "proteins (amino acids). Ketones such as propanone give a red colour with sodium nitroprusside in alkali.",
      ["A → violet ring (I)", "B → acrolein smell (IV)", "C → blue-violet (II)", "D → red colour (III)"],
      ncert=f"{LAB}, tests for carbohydrates, fats and proteins; tests for functional groups", seconds=45),

    N(T_PR, "Titrimetric analysis", "Advanced",
      "A solution contains both oxalic acid and sodium oxalate. 25.0 mL of it needs 20.0 mL of 0.10 M NaOH for "
      "neutralisation (phenolphthalein). Another 25.0 mL portion, acidified with dilute H₂SO₄ and warmed, needs "
      "40.0 mL of 0.020 M KMnO₄. The molarity of sodium oxalate in the solution is:",
      ["0.080 M", "0.040 M", "0.120 M", "0.024 M"], "B", "0.040 M",
      "Combining an acid–base titration with a redox titration",
      "Only oxalic acid (dibasic) reacts with NaOH, but both oxalic acid and oxalate ions are oxidised by "
      "permanganate (2MnO₄⁻ : 5C₂O₄²⁻).",
      ["NaOH: 2.0 mmol → oxalic acid = 2.0/2 = 1.0 mmol",
       "KMnO₄: 0.80 mmol → total oxalate = 0.80 × 5/2 = 2.0 mmol",
       "Sodium oxalate = 2.0 − 1.0 = 1.0 mmol in 25.0 mL → 0.040 M"],
      why_others_wrong="0.080 M is the total oxalate (oxalic acid not subtracted). 0.120 M adds the oxalic acid "
                       "instead of subtracting it. 0.024 M takes the MnO₄⁻ : C₂O₄²⁻ ratio as 1 : 2.",
      ncert=f"{LAB}, titrimetric analysis (oxalic acid against NaOH and against KMnO₄)", seconds=120),

    Q(T_PR, "Qualitative salt analysis", "Advanced", "multi_statement",
      *ms("Which of the following observations in salt analysis are correctly described?",
          [("Al³⁺: the white gelatinous precipitate of group III, dissolved in dilute HCl and treated with blue "
            "litmus and NH₄OH, gives a blue 'lake'.", True),
           ("Mg²⁺ is precipitated in group V by ammonium carbonate in the presence of NH₄Cl and NH₄OH.", False),
           ("Zn²⁺ is precipitated in group IV as a black sulphide.", False),
           ("A nitrite gives brown fumes when warmed with dilute H₂SO₄.", True),
           ("A phosphate gives a yellow precipitate when heated with concentrated HNO₃ and ammonium molybdate.",
            True)],
          [["a", "b", "d"], ["b", "c", "e"], ["a", "c", "e"]], "C"),
      "Identification of cations and anions in salt analysis",
      "Al(OH)₃ adsorbs litmus to give a blue lake. Mg²⁺ is not precipitated in group V (the NH₄⁺ salts keep "
      "MgCO₃ in solution); it is detected in group VI with disodium hydrogen phosphate. ZnS is white (MnS buff, "
      "NiS and CoS black). Nitrite gives brown NO₂ with dilute acid (nitrate needs concentrated acid). Phosphate "
      "gives yellow ammonium phosphomolybdate.",
      ["(a) true", "(b) Mg²⁺ is group VI → false", "(c) ZnS is white → false", "(d) true", "(e) true"],
      why_others_wrong="Every other option includes (b) or (c), both false.",
      ncert=f"{LAB}, systematic qualitative analysis of cations and anions", seconds=70),
]

# ---------------------------------------------------------------- package checks and output
PLAN = {T_DF: (3, 5, 3), T_CC: (4, 6, 4), T_PU: (2, 2, 2), T_GO: (6, 7, 6), T_HC: (5, 6, 5), T_HX: (3, 4, 3),
        T_OX: (6, 7, 6), T_NI: (3, 4, 3), T_BM: (3, 4, 3), T_PR: (2, 3, 2)}
TOTAL = LAST - FIRST + 1

if __name__ == "__main__":
    assert len(QUESTIONS) == TOTAL == 122, len(QUESTIONS)
    assert [x["question_id"] for x in QUESTIONS] == [f"NEET_CHE_{n:06d}" for n in range(FIRST, LAST + 1)]
    have = Counter((x["topic"], x["difficulty"]) for x in QUESTIONS)
    for topic, quota in PLAN.items():
        for diff, n in zip(("Basic", "Intermediate", "Advanced"), quota):
            assert have[(topic, diff)] == n, (topic, diff, have[(topic, diff)], n)
    keys = Counter(x["correct_answer"] for x in QUESTIONS)
    fmts = Counter(x["format"] for x in QUESTIONS)
    print("keys", dict(sorted(keys.items())), "formats", dict(fmts))
    assert all(28 <= keys[k] <= 33 for k in LETTERS), keys
    assert 0.27 <= fmts["numerical"] / TOTAL <= 0.33, fmts
    assert all(fmts[f] / TOTAL >= 0.08 for f in fmts if f != "numerical") and len(fmts) == 6, fmts
    for x in QUESTIONS:  # every numerical answer is recomputed above
        assert (x["format"] == "numerical") == ("script:recompute" in x["verification"]["verified_by"]), x["question_id"]
    doc = {"schema_version": "1.0", "batch_id": "BATCH_005", "created_at": TODAY,
           "notes": "Package CHE_005_p2: 122 original Chemistry questions (d/f block, coordination compounds, "
                    "organic chemistry, biomolecules, practical chemistry). Numerical answers recomputed by "
                    "tools/batch_005/CHE_005_p2.py.",
           "stimuli": [], "questions": QUESTIONS}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {OUT}: {dict(Counter(x['difficulty'] for x in QUESTIONS))}, keys {dict(sorted(keys.items()))}, "
          f"formats {dict(fmts)}")
