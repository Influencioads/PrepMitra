"""Writes batches/parts/BATCH_006_CHE_p2.json: package CHE_006_p2 of BATCH_006 (Chemistry, 119 questions).

Topics: Coordination Compounds, Purification and Characterisation of Organic Compounds, Some Basic Principles of
Organic Chemistry, Hydrocarbons, Organic Compounds Containing Halogens / Oxygen / Nitrogen, Biomolecules (Chemistry),
Principles Related to Practical Chemistry. IDs NEET_CHE_001382..NEET_CHE_001500.

Every numerical answer is re-derived below with an assert; multi-statement keys are derived from the truth value of
each statement, assertion-reason and statement-pair keys from the truth of each part. If any check fails, nothing is
written.

    python docs/neet-bank/tools/batch_006/CHE_006_p2.py
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
OUT = ROOT / "batches" / "parts" / "BATCH_006_CHE_p2.json"
TODAY = "2026-11-16"
LETTERS = "ABCD"
CHE = "Chemistry"
FIRST, LAST = 1382, 1500
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


def pct(x, nd=1):
    return f"{float(x) * 100:.{nd}f}%"


# Atomic masses used in the stems
C_, H_, O_, N_, S_, NA, CL, K_, BR, I_, AG, NI, PT, FE, MN, AL = (12, 1, 16, 14, 32, 23, F(355, 10), 39, 80, 127,
                                                                  108, 59, 195, 56, 55, 27)


def mm(**atoms):
    """Molar mass from atom counts, e.g. mm(C=2, H=6, O=1)."""
    table = {"C": C_, "H": H_, "O": O_, "N": N_, "S": S_, "Na": NA, "Cl": CL, "K": K_, "Br": BR, "I": I_,
             "Ag": AG, "Ni": NI, "Pt": PT, "Fe": FE, "Mn": MN, "Al": AL}
    return sum(table[k] * v for k, v in atoms.items())


QUESTIONS = []

# ================================================================ Coordination Compounds (1382-1397)
# 1383: Ni + 4CO -> Ni(CO)4 ; 5.9 g Ni
n_1383 = F(59, 10) / NI
assert n_1383 == F(1, 10)
v_1383 = g(n_1383 * 4 * F(224, 10), 2, " L")
assert v_1383 == "8.96 L" and g(n_1383 * F(224, 10), 2, " L") == "2.24 L" and g(n_1383 * 2 * F(224, 10), 2, " L") == "4.48 L"
# 1386: cis-platin [Pt(NH3)2Cl2], % Pt
m_cispt = mm(Pt=1, N=2, H=6, Cl=2)
assert m_cispt == 300
v_1386 = pct(F(PT) / m_cispt)
assert v_1386 == "65.0%" and pct(F(PT) / (PT + 2 * CL)) == "73.3%" and pct(F(PT) / (PT + 34)) == "85.2%"
# 1388: AgBr + 2Na2S2O3 -> Na3[Ag(S2O3)2] + NaBr ; hypo = Na2S2O3.5H2O (248)
m_agbr, m_hypo5, m_hypo = AG + BR, mm(Na=2, S=2, O=3) + 5 * 18, mm(Na=2, S=2, O=3)
assert m_agbr == 188 and m_hypo5 == 248 and m_hypo == 158
n_1388 = F(94, 100) / m_agbr
assert n_1388 == F(5, 1000)
v_1388 = g(2 * n_1388 * m_hypo5, 2)
assert v_1388 == "2.48 g" and g(n_1388 * m_hypo5, 2) == "1.24 g" and g(2 * n_1388 * m_hypo, 2) == "1.58 g"
# 1393: Ni(dmg)2 (289 g/mol) from 0.50 g alloy -> 0.578 g precipitate
n_1393 = F(578, 1000) / 289
assert n_1393 == F(2, 1000)
v_1393 = pct(n_1393 * NI / F(1, 2))
assert v_1393 == "23.6%" and pct(F(NI, 289)) == "20.4%" and pct(2 * n_1393 * NI / F(1, 2)) == "47.2%"
# 1394: d-electron counts / unpaired electrons used in the statements
unp = {"[Cr(CN)6]3-": 3, "[Mn(CN)6]4-": 1, "[Ti(H2O)6]3+": 1, "[V(H2O)6]3+": 2, "[Co(CN)6]3-": 0}
assert 24 - 18 - 3 == 3 and 25 - 18 - 2 == 5 and 22 - 18 - 3 == 1 and 23 - 18 - 3 == 2 and 27 - 18 - 3 == 6

QUESTIONS += [
    Q(T_CC, "Isomerism", "Basic", "direct",
      "In Werner's study of cobalt(III) ammine chlorides, two compounds of the same empirical formula CoCl₃·4NH₃ "
      "were obtained, one green and one violet. Both are formulated as [Co(NH₃)₄Cl₂]Cl. The two compounds are:",
      ["Ionisation isomers", "Geometrical (cis and trans) isomers", "Linkage isomers", "Coordination isomers"], "B",
      "Werner's cobalt ammine complexes and geometrical isomerism",
      "Both compounds contain the same complex cation [Co(NH₃)₄Cl₂]⁺ and the same counter ion, so they are not "
      "structural isomers. They differ only in the arrangement of the two Cl⁻ ligands around cobalt: next to each "
      "other (cis) or opposite each other (trans). Such compounds are geometrical isomers.",
      ["Same formula and same ions in and out of the coordination sphere → not ionisation/coordination isomers",
       "No ambidentate ligand → not linkage isomers",
       "Octahedral [MA₄B₂] → cis and trans forms → geometrical isomers"],
      why_others_wrong="Ionisation isomers exchange a ligand with a counter ion; linkage isomers need an ambidentate "
                       "ligand; coordination isomers need both a complex cation and a complex anion.",
      ncert=f"{NC12}, 'Coordination Compounds', Werner's theory (Table of CoCl₃·nNH₃ compounds) and isomerism",
      seconds=40),

    N(T_CC, "Applications", "Basic",
      "Impure nickel is purified by converting it into nickel tetracarbonyl, which is later decomposed:\n"
      "Ni + 4CO → [Ni(CO)₄]\n"
      "The volume of carbon monoxide, measured at STP, needed to convert 5.9 g of nickel completely into "
      "[Ni(CO)₄] is (Ni = 59; molar volume at STP = 22.4 L mol⁻¹):",
      ["2.24 L", "4.48 L", "17.92 L", "8.96 L"], "D", v_1383,
      "Stoichiometry of the formation of a metal carbonyl used in metal purification",
      "One mole of nickel combines with four moles of CO. The volatile carbonyl is separated and decomposed to give "
      "pure nickel.",
      ["n(Ni) = 5.9/59 = 0.1 mol", "n(CO) = 4 × 0.1 = 0.4 mol", "V(CO) = 0.4 × 22.4 = 8.96 L"],
      why_others_wrong="2.24 L takes Ni : CO as 1 : 1 and 4.48 L as 1 : 2. 17.92 L doubles the correct amount.",
      ncert=f"{NC12}, 'Coordination Compounds', importance and applications (purification of nickel)", seconds=45),

    Q(T_CC, "Applications", "Basic", "direct",
      "In the extraction of gold, the metal combines with cyanide in the presence of oxygen and water to form the "
      "soluble complex [Au(CN)₂]⁻. Gold is then recovered in the metallic form from this solution by adding:",
      ["Zinc", "Silver nitrate", "Aqueous ammonia", "Dimethylglyoxime"], "A",
      "Complex formation in the extraction of metals",
      "Gold forms the coordination entity [Au(CN)₂]⁻ in aqueous solution. Zinc, a more reactive metal, displaces "
      "gold from this complex, and gold separates as the metal.",
      ["Au + CN⁻ + O₂ + H₂O → [Au(CN)₂]⁻ (in solution)", "Zinc added → gold separates in metallic form"],
      why_others_wrong="Silver nitrate and ammonia do not reduce the complex to gold; dimethylglyoxime is the reagent "
                       "for estimating Ni²⁺.",
      ncert=f"{NC12}, 'Coordination Compounds', importance and applications (extraction of metals)", seconds=25),

    Q(T_CC, "Crystal field theory", "Basic", "statement_pair",
      *sp("Crystal field theory does not take into account the covalent character of the bonding between the ligand "
          "and the central atom.", True,
          "As crystal field theory treats ligands as point charges, anionic ligands such as I⁻, Br⁻ and Cl⁻ are "
          "actually found at the strong-field end of the spectrochemical series.", False),
      "Limitations of crystal field theory",
      "CFT treats the metal–ligand bond as purely ionic, so it ignores covalent character (Statement I is true). "
      "If ligands were simple point charges, anions should cause the largest splitting; in fact the halide ions "
      "lie at the weak-field (low) end of the spectrochemical series. This contradiction is listed in NCERT as a "
      "limitation of CFT, so Statement II is false.",
      ["Statement I: a stated limitation of CFT → true",
       "Statement II: halide ions are at the low (weak-field) end → false"],
      ncert=f"{NC12}, 'Coordination Compounds', limitations of crystal field theory", seconds=35),

    N(T_CC, "Applications", "Basic",
      "cis-Platin, cis-[Pt(NH₃)₂Cl₂], is used to inhibit the growth of tumours. The percentage of platinum by mass "
      "in cis-platin is (Pt = 195, N = 14, H = 1, Cl = 35.5):",
      ["73.3%", "65.0%", "85.2%", "32.5%"], "B", v_1386,
      "Percentage composition of a coordination compound",
      "Molar mass of [Pt(NH₃)₂Cl₂] = 195 + 2(17) + 2(35.5) = 300 g mol⁻¹. Platinum makes up 195 g of this.",
      ["M = 195 + 34 + 71 = 300 g mol⁻¹", "% Pt = 195/300 × 100 = 65.0%"],
      why_others_wrong="73.3% leaves out the two NH₃ ligands; 85.2% leaves out the two Cl ligands; 32.5% halves the "
                       "correct value.",
      ncert=f"{NC12}, 'Coordination Compounds', importance and applications (cis-platin)", seconds=40),

    Q(T_CC, "IUPAC nomenclature", "Intermediate", "direct",
      "The IUPAC name of K[Cr(H₂O)₂(C₂O₄)₂]·3H₂O is:",
      ["Potassium dioxalatodiaquachromium(III) trihydrate", "Potassium diaquadioxalatochromium(III) trihydrate",
       "Potassium diaquadioxalatochromate(III) trihydrate", "Potassium diaquadioxalatochromate(II) trihydrate"], "C",
      "Naming an anionic coordination entity",
      "The complex ion is an anion, so the metal name ends in -ate (chromate). Ligands are listed alphabetically: "
      "aqua before oxalato. Oxidation state: x + 2(0) + 2(−2) = −1, so x = +3. The water of crystallisation is "
      "named last as 'trihydrate'.",
      ["Charge on complex ion = −1 (one K⁺)", "Cr: x − 4 = −1 → x = +3",
       "Anionic complex → chromate; ligands alphabetical: diaqua, dioxalato",
       "Potassium diaquadioxalatochromate(III) trihydrate"],
      why_others_wrong="'chromium' is used only when the complex is a cation or neutral; oxalato before aqua breaks "
                       "the alphabetical order; chromium is +3, not +2.",
      ncert=f"{NC12}, 'Coordination Compounds', nomenclature of coordination compounds", seconds=50),

    N(T_CC, "Applications", "Intermediate",
      "In photography, unexposed silver bromide is dissolved by hypo:\n"
      "AgBr + 2Na₂S₂O₃ → Na₃[Ag(S₂O₃)₂] + NaBr\n"
      "The minimum mass of hypo crystals, Na₂S₂O₃·5H₂O (molar mass 248 g mol⁻¹), needed to dissolve 0.94 g of AgBr "
      "is (Ag = 108, Br = 80):",
      ["2.48 g", "1.24 g", "1.58 g", "4.96 g"], "A", v_1388,
      "Stoichiometry of complex formation with thiosulphate",
      "Each AgBr needs two thiosulphate ions to form the soluble complex [Ag(S₂O₃)₂]³⁻.",
      ["n(AgBr) = 0.94/188 = 0.005 mol", "n(hypo) = 2 × 0.005 = 0.010 mol", "Mass = 0.010 × 248 = 2.48 g"],
      why_others_wrong="1.24 g takes a 1 : 1 ratio; 1.58 g uses the anhydrous molar mass (158); 4.96 g doubles the "
                       "thiosulphate again.",
      ncert=f"{NC12}, 'Coordination Compounds', importance and applications (photography)", seconds=60),

    Q(T_CC, "Crystal field theory", "Intermediate", "assertion_reason",
      *ar("Ruby is red whereas emerald is green, although in both gemstones the colour is due to Cr³⁺ ions occupying "
          "octahedral sites.", True,
          "The crystal field splitting experienced by Cr³⁺ is different in aluminium oxide (ruby) and in the mineral "
          "beryl (emerald), so light of different wavelengths is absorbed.", True, explains=True),
      "Colour of gemstones from crystal field splitting",
      "In ruby, Cr³⁺ ions replace some Al³⁺ ions in Al₂O₃; in emerald, Cr³⁺ ions occupy octahedral sites in beryl, "
      "Be₃Al₂Si₆O₁₈. The different surroundings change the magnitude of the splitting, so the absorption bands of "
      "emerald are shifted and it transmits green light. R gives exactly this reason for A.",
      ["Same ion (Cr³⁺, d³) in both", "Different host lattice → different Δo → different light absorbed",
       "R explains the difference in colour stated in A"],
      ncert=f"{NC12}, 'Coordination Compounds', colour in coordination compounds (ruby and emerald)", seconds=45),

    Q(T_CC, "Werner's theory and ligands", "Intermediate", "multi_statement",
      *ms("Which of the following statements are correct?",
          [("Carnallite, KCl·MgCl₂·6H₂O, dissociates completely into simple ions when dissolved in water.", True),
           ("An aqueous solution of K₄[Fe(CN)₆] does not contain Fe²⁺ ions released from the complex ion, because "
            "[Fe(CN)₆]⁴⁻ does not dissociate into Fe²⁺ and CN⁻.", True),
           ("In [Pt(NH₃)₂Cl₂], the coordination number of platinum is 2.", False),
           ("In [Co(NH₃)₄Cl₂]Cl, the primary valence of cobalt is 3 and its secondary valence is 6.", True),
           ("Potash alum keeps its identity as a complex ion when dissolved in water.", False)],
          [["a", "b", "c"], ["b", "d", "e"], ["a", "c", "d"]], "D"),
      "Double salts versus coordination compounds; Werner's valences",
      "Double salts such as carnallite, Mohr's salt and potash alum dissociate completely into simple ions in water, "
      "whereas a complex ion such as [Fe(CN)₆]⁴⁻ stays intact. In [Pt(NH₃)₂Cl₂] four donor atoms (2 N, 2 Cl) are "
      "bonded to Pt, so its coordination number is 4. In [Co(NH₃)₄Cl₂]Cl the primary valence (oxidation state) is 3 "
      "and the secondary valence (coordination number) is 6.",
      ["(a) double salt → true", "(b) complex ion does not dissociate → true", "(c) CN = 4 → false",
       "(d) oxidation state 3, CN 6 → true", "(e) potash alum is a double salt → false"],
      why_others_wrong="Every other option includes (c) or (e), which are false, or leaves out (d).",
      ncert=f"{NC12}, 'Coordination Compounds', Werner's theory; double salts and complexes", seconds=70),

    Q(T_CC, "Valence bond theory", "Intermediate", "direct",
      "The complex ion [Co(C₂O₄)₃]³⁻ is found to be diamagnetic (Z of Co = 27). According to valence bond theory, the "
      "hybridisation of cobalt and the shape of the complex are:",
      ["sp³d², octahedral", "d²sp³, octahedral", "dsp², square planar", "sp³, tetrahedral"], "B",
      "Using magnetic data to decide the hybridisation (VBT)",
      "Cobalt is +3 (3 × −2 = −6, overall −3), so it is d⁶. Being diamagnetic, all six d electrons are paired in "
      "three 3d orbitals, leaving two inner 3d orbitals free. These, with 4s and three 4p orbitals, give d²sp³ "
      "hybridisation: an inner orbital, octahedral complex.",
      ["Co³⁺: 3d⁶", "Diamagnetic → electrons paired in three 3d orbitals",
       "Two vacant 3d + 4s + 4p → d²sp³ → octahedral"],
      why_others_wrong="sp³d² would leave four unpaired electrons (paramagnetic). Three didentate oxalate ions give "
                       "coordination number 6, so square planar and tetrahedral shapes are impossible.",
      ncert=f"{NC12}, 'Coordination Compounds', bonding: valence bond theory", seconds=50),

    Q(T_CC, "IUPAC nomenclature", "Intermediate", "statement_pair",
      *sp("The IUPAC name of [Co(NH₃)₄Cl(NO₂)]Cl is tetraamminechloridonitrito-N-cobalt(III) chloride.", True,
          "The IUPAC name of K₂[PtCl₆] is potassium hexachloridoplatinum(IV).", False),
      "Naming cationic and anionic complexes",
      "Statement I: ligands in alphabetical order (ammine, chlorido, nitrito-N); Co: x + 0 − 1 − 1 = +1, so x = +3. "
      "The name is correct. Statement II: [PtCl₆]²⁻ is an anion, so the metal must be named platinate: potassium "
      "hexachloridoplatinate(IV).",
      ["I: alphabetical order and oxidation state +3 are correct → true",
       "II: anionic complex needs -ate (platinate) → false"],
      ncert=f"{NC12}, 'Coordination Compounds', nomenclature of coordination compounds", seconds=45),

    N(T_CC, "Applications", "Advanced",
      "Ni²⁺ is estimated gravimetrically with dimethylglyoxime (DMG). The nickel in 0.50 g of an alloy is converted "
      "completely into the red precipitate Ni(DMG)₂ (molar mass 289 g mol⁻¹, one Ni per formula unit), which weighs "
      "0.578 g after drying. The percentage of nickel in the alloy is (Ni = 59):",
      ["20.4%", "47.2%", "23.6%", "11.8%"], "C", v_1393,
      "Gravimetric estimation of nickel with a chelating ligand",
      "Each mole of Ni(DMG)₂ contains one mole of Ni, so the mass of Ni is found from the moles of precipitate and "
      "then compared with the mass of the alloy.",
      ["n[Ni(DMG)₂] = 0.578/289 = 0.002 mol", "Mass of Ni = 0.002 × 59 = 0.118 g",
       "% Ni = 0.118/0.50 × 100 = 23.6%"],
      why_others_wrong="20.4% is the percentage of Ni in the precipitate, not in the alloy. 47.2% counts two Ni per "
                       "formula unit. 11.8% divides by 1.0 g instead of 0.50 g.",
      ncert=f"{NC12}, 'Coordination Compounds', importance and applications (estimation of Ni²⁺ with DMG)",
      seconds=90),

    Q(T_CC, "Valence bond theory", "Advanced", "multi_statement",
      *ms("Which of the following statements are correct? (Atomic numbers: Ti 22, V 23, Cr 24, Mn 25, Co 27)",
          [("[Cr(CN)₆]³⁻ is an inner orbital (d²sp³) complex with three unpaired electrons.", True),
           ("[Mn(CN)₆]⁴⁻ is a low-spin complex with one unpaired electron.", True),
           ("[Ti(H₂O)₆]³⁺ is diamagnetic.", False),
           ("[V(H₂O)₆]³⁺ has two unpaired electrons.", True),
           ("[Co(CN)₆]³⁻ is paramagnetic.", False)],
          [["a", "c", "d"], ["b", "d", "e"], ["a", "b", "c"]], "B"),
      "Unpaired electrons and hybridisation from d-electron counts",
      "Cr³⁺ is d³: whatever the ligand, three unpaired electrons in t₂g, and two empty 3d orbitals allow d²sp³. Mn²⁺ "
      "is d⁵; with strong-field CN⁻ the electrons pair to t₂g⁵, leaving one unpaired. Ti³⁺ is d¹ (paramagnetic). "
      "V³⁺ is d² (two unpaired). Co³⁺ with CN⁻ is low-spin t₂g⁶ (diamagnetic).",
      ["Cr³⁺ d³ → 3 unpaired, d²sp³ → (a) true", "Mn²⁺ d⁵ low spin → t₂g⁵ → 1 unpaired → (b) true",
       "Ti³⁺ d¹ → 1 unpaired → (c) false", "V³⁺ d² → 2 unpaired → (d) true", "Co³⁺ d⁶ low spin → 0 → (e) false"],
      why_others_wrong="The other options include (c) or (e), both false, or leave out a true statement.",
      ncert=f"{NC12}, 'Coordination Compounds', valence bond theory and magnetic properties", seconds=90),

    Q(T_CC, "Isomerism", "Advanced", "direct",
      "Which of the following compounds gives a white precipitate immediately with aqueous AgNO₃ AND can also exist "
      "as geometrical isomers? (All are octahedral cobalt(III) compounds.)",
      ["[Co(NH₃)₃Cl₃]", "[Co(NH₃)₅Cl]Cl₂", "[Co(NH₃)₆]Cl₃", "[Co(NH₃)₄Cl₂]Cl"], "D",
      "Ionisable chloride and geometrical isomerism together",
      "A precipitate with AgNO₃ needs Cl⁻ outside the coordination sphere. Geometrical isomerism in an octahedral "
      "complex needs a pattern such as [MA₄B₂] or [MA₃B₃]. [Co(NH₃)₄Cl₂]Cl has one ionisable Cl⁻ and a cation "
      "[Co(NH₃)₄Cl₂]⁺ that exists as cis and trans forms.",
      ["[Co(NH₃)₃Cl₃]: fac/mer isomers but no ionisable Cl⁻ → no precipitate",
       "[Co(NH₃)₅Cl]Cl₂ and [Co(NH₃)₆]Cl₃: precipitate, but [MA₅B] and [MA₆] have no geometrical isomers",
       "[Co(NH₃)₄Cl₂]Cl: both conditions met"],
      why_others_wrong="Each other compound meets only one of the two conditions.",
      ncert=f"{NC12}, 'Coordination Compounds', Werner's theory and geometrical isomerism", seconds=75),

    Q(T_CC, "Isomerism", "Advanced", "match_list",
      *ml("Match the complex ion in List-I with the stereoisomerism it shows in List-II (en = ethane-1,2-diamine; "
          "all are octahedral).",
          ["[Co(en)₃]³⁺", "[Co(NH₃)₄Cl₂]⁺", "[Co(en)₂Cl₂]⁺", "[Co(NH₃)₅Cl]²⁺"],
          ["Both geometrical and optical isomerism", "Optical isomerism only", "Geometrical isomerism only",
           "Neither geometrical nor optical isomerism"],
          "II III I IV", ["III II I IV", "II III IV I", "I III II IV"], "D"),
      "Recognising geometrical and optical isomerism in octahedral complexes",
      "[Co(en)₃]³⁺ has only one arrangement of three chelate rings but exists as non-superimposable mirror images "
      "(optical only). [Co(NH₃)₄Cl₂]⁺ has cis and trans forms, both with a mirror plane (geometrical only). "
      "[Co(en)₂Cl₂]⁺ has cis and trans forms, and the cis form is chiral (both). [Co(NH₃)₅Cl]²⁺ has only one form.",
      ["A → optical only (II)", "B → geometrical only (III)", "C → both (I)", "D → neither (IV)"],
      why_others_wrong="The other codes swap optical-only with geometrical-only, or give [Co(NH₃)₅Cl]²⁺ an isomer it "
                       "cannot have.",
      ncert=f"{NC12}, 'Coordination Compounds', stereoisomerism", seconds=80),

    Q(T_CC, "Crystal field theory", "Advanced", "assertion_reason",
      *ar("The crystal field splitting energy Δo of [Fe(H₂O)₆]³⁺ is greater than that of [Fe(H₂O)₆]²⁺.", True,
          "For the same ligand, the magnitude of Δo increases as the charge on the central metal ion increases.",
          True, explains=True),
      "Dependence of Δo on the charge of the metal ion",
      "NCERT states that Δo depends on the field produced by the ligand and on the charge of the metal ion. With the "
      "same ligand (H₂O) and the same metal, Fe³⁺ (higher charge, smaller ion) draws the ligands closer and causes a "
      "larger splitting than Fe²⁺. R is the reason for A.",
      ["Same ligand and metal; only the charge differs", "Higher charge → stronger interaction → larger Δo",
       "R explains A"],
      ncert=f"{NC12}, 'Coordination Compounds', crystal field theory (factors affecting Δo)", seconds=50),
]

# ================================================================ Purification and Characterisation (1398-1404)
# 1398: % H from 0.135 g water out of 0.25 g compound
v_1398 = pct(F(135, 1000) * 2 / 18 / F(25, 100))
assert v_1398 == "6.0%" and pct(F(135, 1000) / 18 / F(25, 100)) == "3.0%"
# 1400: P weighed as ammonium phosphomolybdate (1877 g/mol, one P per formula unit)
v_1400 = pct(F(1877, 1000) / 1877 * 31 / F(20, 100))
assert v_1400 == "15.5%" and pct(F(1877, 1000) / 1877 * 31 / 1) == "3.1%"
# 1401: 0.46 g ethanol burnt; gain of CaCl2 tube (water) and KOH bulb (CO2)
n_1401 = F(46, 100) / mm(C=2, H=6, O=1)
assert n_1401 == F(1, 100)
w_h2o, w_co2 = n_1401 * 3 * 18, n_1401 * 2 * 44
v_1401 = f"{g(w_h2o, 2)} and {g(w_co2, 2)}"
assert v_1401 == "0.54 g and 0.88 g"
# 1404: Kjeldahl, NH3 neutralises 10.0 mL of 0.50 M H2SO4; one N per molecule; 0.59 g
n_nh3 = 2 * F(50, 100) * F(10, 1000)
assert n_nh3 == F(1, 100)
v_1404 = f"{F(59, 100) / n_nh3:.0f} g mol⁻¹"
assert v_1404 == "59 g mol⁻¹" and F(59, 100) / (n_nh3 / 2) == 118

QUESTIONS += [
    N(T_PU, "Quantitative analysis and formulae", "Basic",
      "On complete combustion, 0.25 g of an organic compound gives 0.135 g of water. The percentage of hydrogen in "
      "the compound is (H = 1, O = 16):",
      ["54.0%", "6.0%", "3.0%", "12.0%"], "B", v_1398,
      "Estimation of hydrogen (Liebig's method)",
      "All the hydrogen of the compound ends up in the water. 18 g of water contains 2 g of hydrogen.",
      ["Mass of H = 0.135 × 2/18 = 0.015 g", "% H = 0.015/0.25 × 100 = 6.0%"],
      why_others_wrong="54.0% is the mass of water as a percentage of the sample. 3.0% uses 1/18 instead of 2/18. "
                       "12.0% uses 4/18.",
      ncert=f"{NC11}, 'Organic Chemistry – Some Basic Principles and Techniques', estimation of carbon and hydrogen",
      seconds=40),

    Q(T_PU, "Purification methods", "Basic", "direct",
      "In paper chromatography, the strip of paper on which the components of a mixture have been separated, after "
      "the solvent has risen through it, is known as a(n):",
      ["Eluant", "Adsorbent", "Stationary front", "Chromatogram"], "D",
      "Terms used in paper chromatography",
      "A strip of special paper, with a spot of the mixture near the bottom, is placed in a solvent. As the solvent "
      "rises, the components travel to different heights. The developed paper strip is called a chromatogram.",
      ["Developed strip = chromatogram"],
      why_others_wrong="The eluant is the solvent (mobile phase) that runs through the column or paper; an adsorbent "
                       "is used in adsorption chromatography; 'stationary front' is not a chromatography term.",
      ncert=f"{NC11}, 'Organic Chemistry – Some Basic Principles and Techniques', partition chromatography",
      seconds=25),

    N(T_PU, "Quantitative analysis and formulae", "Intermediate",
      "In the estimation of phosphorus, 0.20 g of an organic compound is oxidised, and the phosphoric acid formed is "
      "precipitated as ammonium phosphomolybdate, (NH₄)₃PO₄·12MoO₃ (molar mass 1877 g mol⁻¹). The dry precipitate "
      "weighs 1.877 g. The percentage of phosphorus in the compound is (P = 31):",
      ["31.0%", "7.8%", "15.5%", "3.1%"], "C", v_1400,
      "Estimation of phosphorus as ammonium phosphomolybdate",
      "One formula unit of ammonium phosphomolybdate contains one phosphorus atom.",
      ["n(precipitate) = 1.877/1877 = 0.001 mol", "Mass of P = 0.001 × 31 = 0.031 g",
       "% P = 0.031/0.20 × 100 = 15.5%"],
      why_others_wrong="31.0% counts two P per formula unit; 7.8% halves the answer; 3.1% divides by 1 g instead of "
                       "0.20 g.",
      ncert=f"{NC11}, 'Organic Chemistry – Some Basic Principles and Techniques', estimation of phosphorus",
      seconds=60),

    N(T_PU, "Quantitative analysis and formulae", "Intermediate",
      "In the estimation of carbon and hydrogen, 0.46 g of ethanol (C₂H₅OH) is burnt completely in a stream of "
      "oxygen. The products are passed first through a U-tube of anhydrous CaCl₂ and then through a bulb of "
      "concentrated KOH solution. The increases in mass of the CaCl₂ tube and of the KOH bulb are, respectively "
      "(C = 12, H = 1, O = 16):",
      ["0.54 g and 0.88 g", "0.88 g and 0.54 g", "0.27 g and 0.44 g", "0.54 g and 0.44 g"], "A", v_1401,
      "Absorbents used in Liebig's combustion method",
      "Anhydrous CaCl₂ absorbs the water and concentrated KOH absorbs the carbon dioxide. One mole of C₂H₆O gives "
      "2 mol CO₂ and 3 mol H₂O.",
      ["n(ethanol) = 0.46/46 = 0.01 mol", "H₂O = 0.03 mol = 0.54 g (gain of CaCl₂ tube)",
       "CO₂ = 0.02 mol = 0.88 g (gain of KOH bulb)"],
      why_others_wrong="0.88 g and 0.54 g swaps the absorbents. 0.27 g and 0.44 g halves both amounts. 0.54 g and "
                       "0.44 g counts only one CO₂ per molecule.",
      ncert=f"{NC11}, 'Organic Chemistry – Some Basic Principles and Techniques', estimation of carbon and hydrogen",
      seconds=60),

    Q(T_PU, "Qualitative analysis", "Intermediate", "statement_pair",
      *sp("If a compound is highly soluble in one solvent and only slightly soluble in another, its crystallisation "
          "can be carried out satisfactorily in a mixture of the two solvents.", True,
          "The Prussian blue colour obtained in the Lassaigne's test for nitrogen is due to the formation of "
          "iron(III) thiocyanate.", False),
      "Crystallisation from mixed solvents; chemistry of the test for nitrogen",
      "NCERT notes that crystallisation can be done in a mixture of two solvents in such a case (Statement I true). "
      "The Prussian blue is iron(III) hexacyanidoferrate(II), Fe₄[Fe(CN)₆]₃·xH₂O, formed from the sodium cyanide of "
      "the fusion extract; iron(III) thiocyanate gives the blood-red colour seen when both N and S are present "
      "(Statement II false).",
      ["I: true", "II: Prussian blue = Fe₄[Fe(CN)₆]₃·xH₂O, not a thiocyanate → false"],
      ncert=f"{NC11}, 'Organic Chemistry – Some Basic Principles and Techniques', crystallisation; detection of "
            "nitrogen", seconds=40),

    Q(T_PU, "Qualitative analysis", "Advanced", "assertion_reason",
      *ar("When an organic compound containing both nitrogen and sulphur is fused with an excess of sodium, the "
          "extract gives the Prussian blue test for nitrogen and the sodium nitroprusside test for sulphur.", True,
          "With excess sodium, the sodium thiocyanate first formed decomposes into sodium cyanide and sodium "
          "sulphide.", True, explains=True),
      "Lassaigne's test when nitrogen and sulphur are both present",
      "With a limited amount of sodium, N and S together form NaSCN, which gives a blood-red colour with Fe³⁺ but no "
      "Prussian blue (no free CN⁻). With excess sodium, NaSCN breaks down to NaCN and Na₂S, and these ions then give "
      "their usual tests. R is exactly the reason for A.",
      ["Limited Na → NaSCN (blood red with Fe³⁺)", "Excess Na → NaSCN + 2Na → NaCN + Na₂S",
       "CN⁻ → Prussian blue; S²⁻ → violet with nitroprusside; R explains A"],
      ncert=f"{NC11}, 'Organic Chemistry – Some Basic Principles and Techniques', Lassaigne's test", seconds=60),

    N(T_PU, "Quantitative analysis and formulae", "Advanced",
      "0.59 g of an organic compound containing one nitrogen atom per molecule is analysed by Kjeldahl's method. "
      "The ammonia evolved exactly neutralises 10.0 mL of 0.50 M H₂SO₄. The molar mass of the compound is:",
      ["118 g mol⁻¹", "29.5 g mol⁻¹", "5.9 g mol⁻¹", "59 g mol⁻¹"], "D", v_1404,
      "Kjeldahl's method used to find a molar mass",
      "H₂SO₄ is dibasic, so one mole of it neutralises two moles of NH₃. Each molecule of the compound gives one NH₃.",
      ["n(H₂SO₄) = 0.50 × 0.010 = 0.005 mol", "n(NH₃) = 2 × 0.005 = 0.010 mol = n(compound)",
       "M = 0.59/0.010 = 59 g mol⁻¹"],
      why_others_wrong="118 g mol⁻¹ forgets that H₂SO₄ is dibasic. 29.5 g mol⁻¹ multiplies by 2 once more. "
                       "5.9 g mol⁻¹ uses 10.0 mL as 0.10 L.",
      ncert=f"{NC11}, 'Organic Chemistry – Some Basic Principles and Techniques', Kjeldahl's method", seconds=90),
]

# ================================================================ Some Basic Principles of Organic Chemistry (1405-1424)
# 1407: 3-ethyl-2-methylhexane -> C9H20
n_c = 6 + 2 + 1
assert (n_c, 2 * n_c + 2) == (9, 20)
v_1407 = "C₉H₂₀"
# 1411: esters C4H8O2: HCOOPr, HCOOiPr, CH3COOEt, EtCOOMe
esters = ["HCOOCH2CH2CH3", "HCOOCH(CH3)2", "CH3COOCH2CH3", "CH3CH2COOCH3"]
v_1411 = str(len(esters))
assert v_1411 == "4"
# 1419: pent-3-en-2-ol: one C=C with geometrical isomerism and one chiral carbon -> 2**2
v_1419 = str(2 ** (1 + 1))
assert v_1419 == "4"
# 1422: number of sp3 carbons
sp3 = {"Benzene": 0, "Toluene": 1, "Propanoic acid": 2, "Butanone": 3}
assert sorted(sp3.values()) == [0, 1, 2, 3]

QUESTIONS += [
    Q(T_GO, "Hybridisation and functional groups", "Basic", "direct",
      "Cyclic compounds that contain an atom other than carbon in the ring may be alicyclic or aromatic. Which of "
      "the following is an alicyclic heterocyclic compound?",
      ["Pyridine", "Furan", "Tetrahydrofuran", "Cyclohexane"], "C",
      "Classification of cyclic organic compounds",
      "Tetrahydrofuran has an oxygen atom in a saturated five-membered ring, so it is heterocyclic but not "
      "aromatic (alicyclic). Pyridine and furan are heterocyclic aromatic compounds; cyclohexane is alicyclic but "
      "homocyclic (only carbon in the ring).",
      ["Heteroatom in ring + no aromatic π system → tetrahydrofuran"],
      why_others_wrong="Pyridine and furan are aromatic heterocycles; cyclohexane contains no heteroatom.",
      ncert=f"{NC11}, 'Organic Chemistry – Some Basic Principles and Techniques', classification of organic "
            "compounds", seconds=30),

    Q(T_GO, "IUPAC nomenclature", "Intermediate", "direct",
      "The IUPAC name of CH₃–CO–CH₂–CH₂–COOH is:",
      ["4-Oxopentanoic acid", "2-Oxopentan-5-oic acid", "4-Ketopentanoic acid", "1-Carboxybutan-3-one"], "A",
      "Naming a compound with a carboxyl and a keto group",
      "The –COOH group has higher priority than the ketone, so it is the suffix and its carbon is C-1. The ketonic "
      "oxygen on C-4 is cited with the prefix 'oxo'.",
      ["Principal group –COOH → 'pentanoic acid', C-1 = COOH", "C=O at C-4 → '4-oxo'", "4-Oxopentanoic acid"],
      why_others_wrong="The carboxyl carbon must be C-1; 'keto' is not the IUPAC prefix; the parent is named after "
                       "the principal group, not as a substituted ketone.",
      ncert=f"{NC11}, 'Organic Chemistry – Some Basic Principles and Techniques', nomenclature of polyfunctional "
            "compounds", seconds=40),

    N(T_GO, "IUPAC nomenclature", "Basic",
      "The molecular formula of the alkane 3-ethyl-2-methylhexane is:",
      ["C₈H₁₈", "C₁₀H₂₂", "C₉H₁₈", "C₉H₂₀"], "D", v_1407,
      "Working back from an IUPAC name to the molecular formula",
      "The parent chain has six carbons; an ethyl group adds two and a methyl group one, so there are nine carbon "
      "atoms. An open-chain alkane has the formula CₙH₂ₙ₊₂.",
      ["C = 6 + 2 + 1 = 9", "Alkane: H = 2(9) + 2 = 20", "C₉H₂₀"],
      why_others_wrong="C₈H₁₈ counts the ethyl group as one carbon; C₁₀H₂₂ adds a carbon; C₉H₁₈ is the formula of an "
                       "alkene or cycloalkane, not an alkane.",
      ncert=f"{NC11}, 'Organic Chemistry – Some Basic Principles and Techniques', IUPAC nomenclature", seconds=30),

    Q(T_GO, "Hybridisation and functional groups", "Basic", "statement_pair",
      *sp("A σ bond is formed by head-on overlap of orbitals, whereas a π bond is formed by sideways (lateral) "
          "overlap of p orbitals.", True,
          "Between the same two carbon atoms, a π bond is stronger than a σ bond.", False),
      "σ and π bonds",
      "Head-on overlap along the internuclear axis gives a σ bond; parallel p orbitals overlap sideways to give a π "
      "bond. Sideways overlap is smaller, so the π bond is weaker than the σ bond; this is why multiple bonds are "
      "sites of reaction.",
      ["I: true", "II: π bond is weaker (smaller overlap) → false"],
      ncert=f"{NC11}, 'Organic Chemistry – Some Basic Principles and Techniques', shapes of carbon compounds",
      seconds=30),

    Q(T_GO, "Hybridisation and functional groups", "Basic", "match_list",
      *ml("Match the compound in List-I with its class in List-II.",
          ["Butane", "Cyclohexane", "Naphthalene", "Thiophene"],
          ["Benzenoid aromatic compound", "Heterocyclic aromatic compound", "Open-chain (acyclic) compound",
           "Alicyclic homocyclic compound"],
          "III IV I II", ["IV III I II", "III IV II I", "III I IV II"], "B"),
      "Classification of organic compounds by structure",
      "Butane has an open chain. Cyclohexane has a ring of carbon atoms only and is not aromatic. Naphthalene "
      "contains fused benzene rings (benzenoid). Thiophene has a sulphur atom in an aromatic five-membered ring.",
      ["A → open chain (III)", "B → alicyclic (IV)", "C → benzenoid (I)", "D → heterocyclic aromatic (II)"],
      why_others_wrong="The other codes swap open-chain with alicyclic, or benzenoid with heterocyclic aromatic.",
      ncert=f"{NC11}, 'Organic Chemistry – Some Basic Principles and Techniques', classification of organic "
            "compounds", seconds=35),

    Q(T_GO, "Types of organic reactions", "Basic", "assertion_reason",
      *ar("Multiple bonds in organic molecules provide sites for chemical reactions.", True,
          "The electron cloud of a π bond lies above and below the plane of the bonding atoms, so its electrons are "
          "easily available to attacking reagents.", True, explains=True),
      "Reactivity of π bonds",
      "NCERT explains that the π electrons are more exposed than σ electrons because the π cloud lies above and "
      "below the bond axis. Attacking reagents (especially electrophiles) can reach them easily, which is why "
      "multiple bonds are reactive sites. R explains A.",
      ["π electrons exposed above and below the plane", "Easily attacked → multiple bond is a reaction site",
       "R explains A"],
      ncert=f"{NC11}, 'Organic Chemistry – Some Basic Principles and Techniques', shapes of carbon compounds "
            "(π bond)", seconds=30),

    N(T_GO, "Isomerism", "Intermediate",
      "How many esters (structural isomers only) have the molecular formula C₄H₈O₂?",
      ["3", "4", "2", "6"], "B", v_1411,
      "Metamerism among esters",
      "An ester RCOOR′ with four carbons in all can be built by sharing the carbons between the acyl part and the "
      "alkoxy part in different ways; these esters are metamers of one another.",
      ["HCOOCH₂CH₂CH₃ (propyl methanoate)", "HCOOCH(CH₃)₂ (propan-2-yl methanoate)",
       "CH₃COOCH₂CH₃ (ethyl ethanoate)", "CH₃CH₂COOCH₃ (methyl propanoate)", "Total = 4"],
      why_others_wrong="3 misses the branched methanoate; 2 counts only the ethanoate and propanoate; 6 includes the "
                       "two C₄H₈O₂ carboxylic acids, which are not esters.",
      ncert=f"{NC11}, 'Organic Chemistry – Some Basic Principles and Techniques', isomerism (metamerism)",
      seconds=60),

    Q(T_GO, "IUPAC nomenclature", "Intermediate", "direct",
      "The IUPAC name of OHC–CH₂–CH₂–CH(OH)–CH₃ is:",
      ["2-Hydroxypentan-5-al", "4-Hydroxypentan-1-one", "1-Oxopentan-4-ol", "4-Hydroxypentanal"], "D",
      "Principal functional group and numbering",
      "The aldehyde group outranks the hydroxyl group, so the suffix is '-al' and the CHO carbon is C-1. The –OH "
      "group on C-4 is shown by the prefix 'hydroxy'. For an aldehyde, the locant 1 is not written.",
      ["Principal group –CHO → pentanal, C-1 = CHO", "–OH on C-4 → 4-hydroxy", "4-Hydroxypentanal"],
      why_others_wrong="Numbering must give the aldehyde carbon locant 1; '-one' is a ketone suffix; the alcohol "
                       "cannot be the suffix when an aldehyde is present.",
      ncert=f"{NC11}, 'Organic Chemistry – Some Basic Principles and Techniques', nomenclature of polyfunctional "
            "compounds", seconds=40),

    Q(T_GO, "Electronic effects", "Intermediate", "statement_pair",
      *sp("When the inductive and electromeric effects operate in opposite directions, the electromeric effect "
          "predominates.", True,
          "The –OCOR group attached to a benzene ring through its oxygen atom shows a +R (electron-releasing) "
          "effect.", True),
      "Electromeric effect versus inductive effect; +R groups",
      "NCERT states that the electromeric effect predominates when the two act in opposite directions. It also lists "
      "–OCOR among the groups that show a +R effect (along with halogen, –OH, –OR, –NH₂, –NHR, –NR₂ and –NHCOR), "
      "because the oxygen lone pair attached to the ring can be delocalised into it.",
      ["I: true (NCERT)", "II: lone pair on O bonded to the ring → +R → true"],
      ncert=f"{NC11}, 'Organic Chemistry – Some Basic Principles and Techniques', electromeric and resonance "
            "effects", seconds=40),

    Q(T_GO, "IUPAC nomenclature", "Intermediate", "match_list",
      *ml("Match the structure in List-I with its IUPAC name in List-II.",
          ["(CH₃)₂CH–CH₂–CH₂–CH₃", "CH₃CH₂–CH(CH₂CH₃)–CH(CH₃)–CH₃", "CH₃–CH=C(CH₃)–CH₂–CH₃", "(CH₃)₃C–CH₂–OH"],
          ["3-Methylpent-2-ene", "2,2-Dimethylpropan-1-ol", "2-Methylpentane", "3-Ethyl-2-methylpentane"],
          "III IV I II", ["III I IV II", "IV III I II", "III IV II I"], "C"),
      "Applying IUPAC rules to branched compounds",
      "A: five-carbon chain with a methyl on C-2 → 2-methylpentane. B: the longest chain has five carbons; choosing "
      "the chain with more substituents gives ethyl on C-3 and methyl on C-2 → 3-ethyl-2-methylpentane. C: the "
      "double bond gets the lower locant (C-2) and the methyl is on C-3 → 3-methylpent-2-ene. D: three-carbon chain "
      "with –OH on C-1 and two methyls on C-2 → 2,2-dimethylpropan-1-ol.",
      ["A → III", "B → IV", "C → I", "D → II"],
      why_others_wrong="The other codes swap the alkene with the branched alkane or the alcohol with the alkene.",
      ncert=f"{NC11}, 'Organic Chemistry – Some Basic Principles and Techniques', IUPAC nomenclature", seconds=60),

    Q(T_GO, "Electronic effects", "Intermediate", "multi_statement",
      *ms("Which of the following statements about resonance (canonical) structures are correct?",
          [("Among canonical structures, the one with more covalent bonds is more stable.", True),
           ("A canonical structure in which all atoms (other than hydrogen) have complete octets is more stable "
            "than one in which some atom lacks an octet.", True),
           ("The molecule keeps changing (flipping) from one canonical structure to another.", False),
           ("A canonical structure with the positive charge on the more electronegative atom contributes more to "
            "the hybrid.", False),
           ("The difference in energy between the actual structure and the lowest-energy resonance structure is "
            "called the resonance stabilisation energy.", True)],
          [["a", "b", "c"], ["b", "d", "e"], ["a", "c", "e"]], "B"),
      "Rules for the stability of canonical structures",
      "A structure is more stable when it has more covalent bonds, complete octets, less separation of opposite "
      "charges, a negative charge on the more electronegative atom and a positive charge on the more electropositive "
      "atom. The canonical forms are hypothetical; the molecule is a single hybrid and does not flip between them. "
      "The energy lowering relative to the most stable canonical form is the resonance energy.",
      ["(a) true", "(b) true", "(c) hybrid does not oscillate → false",
       "(d) positive charge should be on the more electropositive atom → false", "(e) true"],
      why_others_wrong="The other options include (c) or (d), both false.",
      ncert=f"{NC11}, 'Organic Chemistry – Some Basic Principles and Techniques', resonance structure",
      seconds=60),

    Q(T_GO, "Reactive intermediates", "Intermediate", "assertion_reason",
      *ar("In the curved-arrow notation, the homolytic cleavage of a covalent bond is shown with full-headed curved "
          "arrows.", False,
          "In homolytic cleavage, each of the two bonded atoms keeps one electron of the shared pair.", True),
      "Curved arrows for homolytic and heterolytic cleavage",
      "A full-headed arrow shows the movement of an electron pair (heterolysis). In homolysis each atom takes one "
      "electron, and the movement of a single electron is shown by a half-headed (fish-hook) arrow. So A is false and "
      "R is true.",
      ["A: homolysis uses fish-hook (half-headed) arrows → false", "R: one electron to each atom → true"],
      ncert=f"{NC11}, 'Organic Chemistry – Some Basic Principles and Techniques', fission of a covalent bond",
      seconds=35),

    Q(T_GO, "Hybridisation and functional groups", "Basic", "direct",
      "In the three-dimensional (wedge-and-dash) representation of an organic molecule, a solid wedge drawn from a "
      "carbon atom indicates a bond that:",
      ["lies in the plane of the paper", "projects out of the plane of the paper towards the observer",
       "projects out of the plane of the paper away from the observer", "is a π bond"], "B",
      "Wedge-and-dash formulas",
      "Bonds in the plane of the paper are drawn as normal lines, a solid wedge shows a bond pointing out of the "
      "paper towards the viewer, and a dashed wedge a bond pointing away from the viewer.",
      ["Solid wedge → towards the observer", "Dashed wedge → away from the observer"],
      why_others_wrong="An ordinary line is used for bonds in the plane; a dashed wedge points away from the "
                       "observer; wedges show direction in space, not the type of bond.",
      ncert=f"{NC11}, 'Organic Chemistry – Some Basic Principles and Techniques', three-dimensional representation",
      seconds=25),

    Q(T_GO, "Hybridisation and functional groups", "Intermediate", "direct",
      "In which of the following molecules are sp³, sp² and sp hybridised carbon atoms all present?",
      ["CH₂=CH–C≡N", "CH₃–CH=CH–C≡N", "CH₃–CH₂–C≡N", "CH₃–CH=CH₂"], "B",
      "Identifying hybridisation from the bonding of each carbon",
      "A carbon with four single bonds is sp³, one with a double bond is sp², and one with a triple bond is sp. In "
      "CH₃–CH=CH–C≡N the carbons are sp³, sp², sp² and sp.",
      ["CH₂=CH–C≡N: sp², sp², sp (no sp³)", "CH₃–CH=CH–C≡N: sp³, sp², sp², sp ✔",
       "CH₃–CH₂–C≡N: sp³, sp³, sp (no sp²)", "CH₃–CH=CH₂: sp³, sp², sp² (no sp)"],
      why_others_wrong="Each other molecule lacks one of the three hybridisation states.",
      ncert=f"{NC11}, 'Organic Chemistry – Some Basic Principles and Techniques', hybridisation", seconds=40),

    N(T_GO, "Isomerism", "Advanced",
      "The total number of stereoisomers (geometrical and optical together) of pent-3-en-2-ol, "
      "CH₃–CH=CH–CH(OH)–CH₃, is:",
      ["2", "3", "4", "8"], "C", v_1419,
      "Combining geometrical and optical isomerism",
      "The C=C bond carries different groups on each carbon (H and CH₃; H and CH(OH)CH₃), so cis and trans forms "
      "exist. C-2 is bonded to H, OH, CH₃ and CH=CHCH₃, four different groups, so it is chiral. The two features are "
      "independent, giving 2 × 2 stereoisomers.",
      ["Geometrical: cis/trans → 2", "Chiral centre: C-2 → 2 enantiomers each", "Total = 2 × 2 = 4"],
      why_others_wrong="2 counts only one kind of isomerism; 3 is the answer for a molecule with two identical chiral "
                       "centres (meso form); 8 assumes three stereogenic units.",
      ncert=f"{NC11}, 'Organic Chemistry – Some Basic Principles and Techniques', isomerism", seconds=75),

    Q(T_GO, "Types of organic reactions", "Advanced", "multi_statement",
      *ms("In which of the following conversions is the change in hybridisation of the indicated carbon atom(s) "
          "described correctly?",
          [("CH₂=CH₂ + Br₂ → BrCH₂–CH₂Br: each carbon changes from sp² to sp³.", True),
           ("HC≡CH + H₂ (Lindlar catalyst) → CH₂=CH₂: each carbon changes from sp to sp².", True),
           ("C₆H₆ + Cl₂ (anhydrous FeCl₃) → C₆H₅Cl: the ring carbon bonded to chlorine in the product is sp³.",
            False),
           ("CH₃CH₂OH (conc. H₂SO₄, 443 K) → CH₂=CH₂: both carbons change from sp³ to sp².", True),
           ("CH₃COOH + SOCl₂ → CH₃COCl: the carbonyl carbon changes from sp² to sp³.", False)],
          [["a", "b", "c"], ["b", "d", "e"], ["a", "c", "d"]], "D"),
      "Hybridisation changes in addition, elimination and substitution",
      "Addition to a multiple bond raises the number of σ bonds on the carbons (sp² → sp³, sp → sp²). Elimination "
      "does the reverse (sp³ → sp²). In substitution reactions the hybridisation of the reacting carbon is the same "
      "in the reactant and the product: the aromatic carbon in chlorobenzene and the acyl carbon in CH₃COCl remain "
      "sp².",
      ["(a) addition → sp² → sp³: true", "(b) partial reduction → sp → sp²: true",
       "(c) chlorobenzene carbon is sp²: false", "(d) elimination → sp³ → sp²: true",
       "(e) acyl chloride carbon is sp²: false"],
      why_others_wrong="Every other option includes (c) or (e), both false, or leaves out a true statement.",
      ncert=f"{NC11}, 'Organic Chemistry – Some Basic Principles and Techniques', hybridisation and types of organic "
            "reactions", seconds=90),

    Q(T_GO, "IUPAC nomenclature", "Advanced", "statement_pair",
      *sp("CH₃–CH(CH₂CH₃)–CH₂–CH₃ is named 3-methylpentane.", True,
          "CH₃–CH(CH₃)–CH(CH₂CH₃)–CH₃ is named 3-ethyl-2-methylbutane.", False),
      "Choosing the longest chain that runs through a substituent",
      "Statement I: the longest chain runs through the ethyl group and has five carbons with a methyl on C-3, so "
      "the name 3-methylpentane is correct. Statement II: the longest chain also runs through the ethyl group and "
      "has five carbons, with methyl groups on C-2 and C-3; the correct name is 2,3-dimethylpentane.",
      ["I: longest chain = 5 C, methyl on C-3 → true",
       "II: longest chain = 5 C → 2,3-dimethylpentane, not a butane → false"],
      ncert=f"{NC11}, 'Organic Chemistry – Some Basic Principles and Techniques', IUPAC nomenclature", seconds=60),

    Q(T_GO, "Hybridisation and functional groups", "Advanced", "match_list",
      *ml("Match the compound in List-I with the number of sp³-hybridised carbon atoms in it (List-II).",
          ["Benzene", "Toluene", "Propanoic acid", "Butanone (CH₃COCH₂CH₃)"],
          ["2", "0", "3", "1"],
          "II IV I III", ["IV II I III", "II IV III I", "II I IV III"], "A"),
      "Counting hybridisation states in a molecule",
      "All ring carbons of benzene are sp². Toluene adds one sp³ methyl carbon. In CH₃CH₂COOH the CH₃ and CH₂ "
      "carbons are sp³ and the COOH carbon is sp². In butanone the C=O carbon is sp² and the other three carbons "
      "are sp³.",
      ["Benzene → 0 (II)", "Toluene → 1 (IV)", "Propanoic acid → 2 (I)", "Butanone → 3 (III)"],
      why_others_wrong="The other codes count a carbonyl or carboxyl carbon as sp³, or swap benzene and toluene.",
      ncert=f"{NC11}, 'Organic Chemistry – Some Basic Principles and Techniques', hybridisation", seconds=60),

    Q(T_GO, "IUPAC nomenclature", "Advanced", "direct",
      "The IUPAC name of CH₃–CH(OH)–CH₂–CO–CH₂–COOH is:",
      ["5-Hydroxy-3-oxohexanoic acid", "2-Hydroxy-4-oxohexanoic acid", "3-Oxo-5-hydroxyhexanoic acid",
       "1-Carboxy-4-hydroxypentan-2-one"], "A",
      "Polyfunctional nomenclature: suffix, numbering and alphabetical prefixes",
      "–COOH is the principal group, so its carbon is C-1 and the parent is hexanoic acid. The keto oxygen is on C-3 "
      "(oxo) and the –OH on C-5 (hydroxy). Prefixes are written in alphabetical order: hydroxy before oxo.",
      ["C-1 = COOH → hexanoic acid", "C=O at C-3 → 3-oxo; –OH at C-5 → 5-hydroxy",
       "Alphabetical: 5-hydroxy-3-oxohexanoic acid"],
      why_others_wrong="2-Hydroxy-4-oxo numbers from the wrong end; '3-oxo-5-hydroxy' breaks alphabetical order; the "
                       "carboxylic acid must be the suffix, not a 'carboxy' prefix on a ketone.",
      ncert=f"{NC11}, 'Organic Chemistry – Some Basic Principles and Techniques', nomenclature of polyfunctional "
            "compounds", seconds=60),

    Q(T_GO, "Isomerism", "Advanced", "assertion_reason",
      *ar("Cyclohexane and hex-1-ene are structural isomers.", True,
          "A cyclic compound and an open-chain compound can never have the same molecular formula.", False),
      "Isomerism between ring compounds and alkenes",
      "Both cyclohexane and hex-1-ene have the formula C₆H₁₂; they differ in the way the atoms are joined, so they "
      "are structural isomers. Each ring 'uses up' two hydrogens just as a double bond does, so ring compounds and "
      "open-chain alkenes often share a formula. R is false.",
      ["Cyclohexane: C₆H₁₂; hex-1-ene: C₆H₁₂ → same formula, different structure → A true",
       "R contradicts this example → false"],
      ncert=f"{NC11}, 'Organic Chemistry – Some Basic Principles and Techniques', structural isomerism", seconds=40),
]

# ================================================================ Hydrocarbons (1425-1440)
# 1426: polythene, 2000 ethene units per chain
m_c2h4 = mm(C=2, H=4)
assert m_c2h4 == 28
v_1426 = f"{2000 * m_c2h4} g mol⁻¹"
assert v_1426 == "56000 g mol⁻¹" and 2000 * mm(C=2, H=2) == 52000 and 2000 * mm(C=2, H=6) == 60000
# 1430: 2 CH3C≡CH + 2 Na -> 2 CH3C≡CNa + H2 ; 4.0 g propyne
n_1430 = F(40, 10) / mm(C=3, H=4)
assert n_1430 == F(1, 10)
v_1430 = g(n_1430 / 2 * F(224, 10), 2, " L")
assert v_1430 == "1.12 L"
# 1436: CH3CH2CH3, six 1° H and two 2° H; relative reactivity per H 1° : 2° = 1 : 4.5
share_2 = F(2 * 9, 2) / (6 * 1 + F(2 * 9, 2))
v_1436 = pct(share_2, 0)
assert v_1436 == "60%" and pct(F(2, 8), 0) == "25%" and pct(1 - share_2, 0) == "40%"
# 1437: x mol C2H4 + y mol C2H2 = 0.10 ; H2 = x + 2y = 0.14
y_1437 = F(14, 100) - F(10, 100)
v_1437 = pct(y_1437 / F(10, 100), 0)
assert v_1437 == "40%" and pct(1 - y_1437 / F(10, 100), 0) == "60%"

QUESTIONS += [
    Q(T_HC, "Alkanes and conformations", "Basic", "direct",
      "In the sawhorse projection of ethane, the central carbon–carbon bond is drawn as a somewhat longer, slightly "
      "tilted straight line. The front carbon atom is shown:",
      ["as a point at the centre of a circle", "at the upper end of the line", "at the lower end of the line",
       "as a circle behind the rear carbon"], "C",
      "Sawhorse projection",
      "In a sawhorse projection the molecule is viewed along the C–C axis from an oblique angle. The front carbon is "
      "at the lower end of the inclined line and the rear carbon at the upper end, each with its three bonds drawn.",
      ["Sawhorse: front carbon at the lower end, rear carbon at the upper end"],
      why_others_wrong="A point at the centre of a circle is the front carbon in a Newman projection; the upper end "
                       "of the line is the rear carbon.",
      ncert=f"{NC11}, 'Hydrocarbons', conformations (sawhorse projections)", seconds=25),

    N(T_HC, "Alkenes: addition and ozonolysis", "Basic",
      "Ethene polymerises at high temperature and pressure, in the presence of a catalyst, to give polythene, "
      "–(CH₂–CH₂)ₙ–. A polythene chain is made of an average of 2000 ethene units. Ignoring the end groups, its "
      "average molar mass is (C = 12, H = 1):",
      ["56000 g mol⁻¹", "52000 g mol⁻¹", "60000 g mol⁻¹", "28000 g mol⁻¹"], "A", v_1426,
      "Polymerisation of alkenes",
      "Each repeating unit of polythene has the formula C₂H₄ (molar mass 28 g mol⁻¹), because addition "
      "polymerisation does not lose any atoms.",
      ["Repeating unit –CH₂–CH₂– = 28 g mol⁻¹", "Molar mass = 2000 × 28 = 56000 g mol⁻¹"],
      why_others_wrong="52000 uses C₂H₂ (26) and 60000 uses C₂H₆ (30) as the unit; 28000 counts 1000 units.",
      ncert=f"{NC11}, 'Hydrocarbons', alkenes: polymerisation", seconds=30),

    Q(T_HC, "Alkynes", "Basic", "direct",
      "Linear polymerisation of ethyne gives a high-molecular-mass polyene that conducts electricity under special "
      "conditions; thin films of it can be used as electrodes in batteries. The polymer is:",
      ["Polythene", "Benzene", "Polypropene", "Polyacetylene (polyethyne)"], "D",
      "Polymerisation of alkynes",
      "NCERT describes two kinds of polymerisation of ethyne: linear polymerisation gives polyacetylene (polyethyne), "
      "a polyene with alternating double bonds that can conduct electricity, while cyclic polymerisation (red-hot "
      "iron tube, 873 K) gives benzene.",
      ["Linear polymer of ethyne → polyacetylene", "Cyclic trimer → benzene"],
      why_others_wrong="Polythene and polypropene are made from ethene and propene; benzene is the cyclic trimer of "
                       "ethyne, not a polymer.",
      ncert=f"{NC11}, 'Hydrocarbons', alkynes: polymerisation", seconds=25),

    Q(T_HC, "Alkenes: addition and ozonolysis", "Basic", "statement_pair",
      *sp("Cycloalkanes have the general formula CₙH₂ₙ.", True,
          "Cyclopropane and propene are isomers.", True),
      "General formula of cycloalkanes",
      "Forming a ring removes two hydrogen atoms from the open-chain alkane, so cycloalkanes are CₙH₂ₙ, the same "
      "general formula as open-chain alkenes. Cyclopropane and propene are both C₃H₆ but differ in structure, so they "
      "are isomers.",
      ["I: CₙH₂ₙ → true", "II: both C₃H₆ → true"],
      ncert=f"{NC11}, 'Hydrocarbons', classification and alkanes", seconds=25),

    Q(T_HC, "Benzene and aromaticity", "Basic", "match_list",
      *ml("Match the common name of the aromatic hydrocarbon in List-I with its IUPAC name in List-II.",
          ["o-Xylene", "m-Xylene", "p-Xylene", "Toluene"],
          ["1,4-Dimethylbenzene", "Methylbenzene", "1,2-Dimethylbenzene", "1,3-Dimethylbenzene"],
          "III IV I II", ["IV III I II", "I IV III II", "III II I IV"], "D"),
      "Nomenclature of benzene derivatives",
      "In disubstituted benzenes, the prefixes ortho (o-), meta (m-) and para (p-) correspond to the locants 1,2-, "
      "1,3- and 1,4-. Toluene is methylbenzene.",
      ["o-xylene → 1,2 (III)", "m-xylene → 1,3 (IV)", "p-xylene → 1,4 (I)", "toluene → methylbenzene (II)"],
      why_others_wrong="The other codes interchange ortho, meta and para, or the xylene and toluene names.",
      ncert=f"{NC11}, 'Hydrocarbons', aromatic hydrocarbons: nomenclature and isomerism", seconds=30),

    N(T_HC, "Alkynes", "Intermediate",
      "4.0 g of propyne, CH₃–C≡CH, reacts completely with sodium metal to form sodium propynide and hydrogen. The "
      "volume of hydrogen evolved at STP is (C = 12, H = 1; molar volume at STP = 22.4 L mol⁻¹):",
      ["2.24 L", "1.12 L", "0.56 L", "4.48 L"], "B", v_1430,
      "Acidic character of terminal alkynes",
      "Only the hydrogen attached to the triple-bonded carbon is acidic. Two molecules of propyne react with two "
      "sodium atoms to release one molecule of H₂: 2CH₃C≡CH + 2Na → 2CH₃C≡CNa + H₂.",
      ["n(propyne) = 4.0/40 = 0.1 mol", "n(H₂) = 0.1/2 = 0.05 mol", "V = 0.05 × 22.4 = 1.12 L"],
      why_others_wrong="2.24 L gives one H₂ per propyne; 0.56 L halves again; 4.48 L assumes all four H atoms are "
                       "acidic.",
      ncert=f"{NC11}, 'Hydrocarbons', alkynes: acidic character", seconds=50),

    Q(T_HC, "Alkynes", "Intermediate", "direct",
      "Ethyne is passed into an excess of bromine dissolved in CCl₄ until no more bromine is decolourised. The final "
      "product is:",
      ["1,2-Dibromoethane", "Bromoethyne", "1,1,2,2-Tetrabromoethane", "1,1-Dibromoethane"], "C",
      "Addition of halogens to alkynes",
      "Bromine adds in two steps across the triple bond: first to 1,2-dibromoethene and then, with excess bromine, "
      "to 1,1,2,2-tetrabromoethane. The reddish-orange colour of bromine is discharged, which is a test for "
      "unsaturation.",
      ["HC≡CH + Br₂ → BrCH=CHBr", "BrCH=CHBr + Br₂ → Br₂CH–CHBr₂ (1,1,2,2-tetrabromoethane)"],
      why_others_wrong="1,2-Dibromoethane comes from ethene + Br₂; bromoethyne is a substitution product; "
                       "1,1-dibromoethane comes from adding two HBr, not Br₂.",
      ncert=f"{NC11}, 'Hydrocarbons', alkynes: addition of halogens", seconds=35),

    Q(T_HC, "Electrophilic substitution", "Intermediate", "assertion_reason",
      *ar("In the arenium ion (σ-complex) formed during electrophilic substitution of benzene, one of the ring "
          "carbon atoms is sp³ hybridised.", True,
          "The electrophile forms a σ bond with one ring carbon, which then carries four σ bonds (to H, to the "
          "electrophile and to two ring carbons).", True, explains=True),
      "Structure of the arenium ion",
      "When the electrophile attacks, one carbon of the ring uses its π electrons to form a σ bond to E. That carbon "
      "now has four σ bonds and no p orbital in the π system, so it is sp³ hybridised; the positive charge is "
      "delocalised over the other five carbons. R gives the reason for A.",
      ["Attack of E⁺ → new C–E σ bond", "That carbon: 4 σ bonds → sp³", "R explains A"],
      ncert=f"{NC11}, 'Hydrocarbons', mechanism of electrophilic substitution", seconds=40),

    Q(T_HC, "Alkanes and conformations", "Intermediate", "multi_statement",
      *ms("Which of the following statements about the free-radical halogenation of alkanes are correct?",
          [("Fluorination of alkanes is too violent to be controlled.", True),
           ("In the initiation step of the chlorination of methane, a C–H bond undergoes homolysis.", False),
           ("Ethane is formed as a by-product in the chlorination of methane, in the chain termination step.",
            True),
           ("Bromination of methane proceeds faster than its chlorination.", False),
           ("In a propagation step, a chlorine free radical removes a hydrogen atom from methane to give a methyl "
            "free radical and HCl.", True)],
          [["a", "b", "c"], ["c", "d", "e"], ["a", "b", "e"]], "B"),
      "Mechanism of free-radical halogenation",
      "The reactivity of halogens is F₂ > Cl₂ > Br₂ > I₂; fluorination is too violent. Initiation is the homolysis "
      "of the weaker Cl–Cl bond by light or heat. In propagation Cl• abstracts H from CH₄ (giving CH₃• and HCl), and "
      "CH₃• attacks Cl₂. In termination, radicals combine: two CH₃• radicals give ethane, explaining its presence.",
      ["(a) true", "(b) Cl–Cl, not C–H, is broken in initiation → false", "(c) CH₃• + CH₃• → C₂H₆ → true",
       "(d) chlorination is faster → false", "(e) true"],
      why_others_wrong="The other options include (b) or (d), both false.",
      ncert=f"{NC11}, 'Hydrocarbons', alkanes: halogenation and its mechanism", seconds=60),

    Q(T_HC, "Alkenes: addition and ozonolysis", "Intermediate", "statement_pair",
      *sp("cis-But-2-ene and trans-but-2-ene give the same products on ozonolysis (O₃, then Zn/H₂O).", True,
          "trans-But-2-ene has a higher boiling point than cis-but-2-ene.", False),
      "Geometrical isomers: chemical and physical properties",
      "Ozonolysis breaks the C=C bond, so the spatial arrangement is lost and both isomers give two molecules of "
      "ethanal. The cis isomer is polar (the bond dipoles do not cancel) and boils at a higher temperature "
      "(about 277 K) than the non-polar trans isomer (about 274 K).",
      ["I: both → 2 CH₃CHO → true", "II: cis is more polar and boils higher → false"],
      ncert=f"{NC11}, 'Hydrocarbons', alkenes: geometrical isomerism and ozonolysis", seconds=45),

    Q(T_HC, "Alkenes: addition and ozonolysis", "Intermediate", "match_list",
      *ml("Match the reaction of propene in List-I with its main product in List-II.",
          ["HBr (no peroxide)", "HBr in the presence of benzoyl peroxide", "Br₂ in CCl₄",
           "Cold concentrated H₂SO₄"],
          ["1,2-Dibromopropane", "CH₃–CH(OSO₃H)–CH₃ (propan-2-yl hydrogensulphate)", "1-Bromopropane",
           "2-Bromopropane"],
          "IV III I II", ["III IV I II", "IV III II I", "IV I III II"], "A"),
      "Electrophilic and free-radical addition to an unsymmetrical alkene",
      "HBr and cold concentrated H₂SO₄ add by Markovnikov's rule, putting Br or OSO₃H on C-2. With peroxide, HBr "
      "adds by a free-radical path (anti-Markovnikov) to give 1-bromopropane. Bromine adds to both carbons of the "
      "double bond.",
      ["A → 2-bromopropane (IV)", "B → 1-bromopropane (III)", "C → 1,2-dibromopropane (I)",
       "D → propan-2-yl hydrogensulphate (II)"],
      why_others_wrong="The other codes swap the Markovnikov and anti-Markovnikov products or the bromine and "
                       "sulphuric acid products.",
      ncert=f"{NC11}, 'Hydrocarbons', alkenes: addition reactions", seconds=50),

    N(T_HC, "Alkanes and conformations", "Advanced",
      "In the free-radical monochlorination of propane at a certain temperature, a secondary hydrogen atom is "
      "replaced 4.5 times as fast as a primary hydrogen atom. The percentage of 2-chloropropane in the "
      "monochlorinated product is:",
      ["25%", "40%", "82%", "60%"], "D", v_1436,
      "Relative reactivity of 1° and 2° hydrogen atoms in halogenation",
      "The amount of each product is proportional to (number of that type of hydrogen) × (reactivity per hydrogen). "
      "Propane has six primary and two secondary hydrogen atoms.",
      ["Primary: 6 × 1 = 6", "Secondary: 2 × 4.5 = 9", "% 2-chloropropane = 9/(6 + 9) × 100 = 60%"],
      why_others_wrong="25% counts hydrogen atoms only (2 of 8); 40% is the share of 1-chloropropane; 82% "
                       "(4.5/5.5) ignores the numbers of hydrogen atoms.",
      ncert=f"{NC11}, 'Hydrocarbons', alkanes: halogenation (3° > 2° > 1° hydrogens)", seconds=90),

    N(T_HC, "Alkynes", "Advanced",
      "0.10 mol of a mixture of ethene and ethyne needs exactly 0.14 mol of H₂ for complete hydrogenation to "
      "ethane over a nickel catalyst. The percentage of ethyne (by moles) in the mixture is:",
      ["60%", "40%", "14%", "28%"], "B", v_1437,
      "Hydrogenation stoichiometry of alkenes and alkynes",
      "One mole of ethene takes up one mole of H₂, and one mole of ethyne takes up two moles of H₂ to give ethane.",
      ["x + y = 0.10 (x = ethene, y = ethyne)", "x + 2y = 0.14", "y = 0.04 mol → 0.04/0.10 = 40%"],
      why_others_wrong="60% is the percentage of ethene; 14% and 28% come from using the hydrogen amount directly.",
      ncert=f"{NC11}, 'Hydrocarbons', alkenes and alkynes: addition of hydrogen", seconds=75),

    Q(T_HC, "Alkynes", "Advanced", "direct",
      "A hydrocarbon X, C₅H₈, reacts with sodamide to form a sodium salt. On hydration with dilute H₂SO₄ and Hg²⁺ it "
      "gives a methyl ketone, and on complete hydrogenation it gives 2-methylbutane. X is:",
      ["Pent-1-yne", "3-Methylbut-1-yne", "Pent-2-yne", "2-Methylbuta-1,3-diene"], "B",
      "Using reactions to identify an alkyne",
      "Formation of a sodium salt shows a terminal alkyne (≡C–H). Hydrogenation to 2-methylbutane shows a branched "
      "carbon skeleton. The only terminal C₅ alkyne with this skeleton is HC≡C–CH(CH₃)₂, which on hydration gives "
      "3-methylbutan-2-one.",
      ["Acidic ≡C–H → terminal alkyne", "Skeleton of 2-methylbutane → branched",
       "X = HC≡C–CH(CH₃)₂ (3-methylbut-1-yne)"],
      why_others_wrong="Pent-1-yne gives n-pentane on hydrogenation. Pent-2-yne has no acidic hydrogen. "
                       "2-Methylbuta-1,3-diene gives 2-methylbutane but has no ≡C–H to react with sodamide.",
      ncert=f"{NC11}, 'Hydrocarbons', alkynes: acidic character and addition reactions", seconds=75),

    Q(T_HC, "Alkenes: addition and ozonolysis", "Advanced", "assertion_reason",
      *ar("cis-But-2-ene and trans-but-2-ene change into each other readily at room temperature.", False,
          "Rotation about a carbon–carbon double bond is restricted because it would require breaking the π bond.",
          True),
      "Restricted rotation and geometrical isomerism",
      "The π bond is formed by sideways overlap of p orbitals; rotating one carbon relative to the other would "
      "destroy this overlap. So rotation is restricted, and the cis and trans isomers are separate, stable "
      "compounds that do not interconvert at room temperature. A is false; R is true.",
      ["A: geometrical isomers are separable and do not interconvert readily → false", "R: true"],
      ncert=f"{NC11}, 'Hydrocarbons', alkenes: geometrical isomerism", seconds=40),

    Q(T_HC, "Alkynes", "Advanced", "statement_pair",
      *sp("Hydration of but-1-yne with dilute H₂SO₄ in the presence of Hg²⁺ gives butan-2-one.", True,
          "Hydration of but-2-yne under the same conditions gives butanal.", False),
      "Markovnikov hydration of alkynes",
      "Water adds to the triple bond through an enol, which changes into the carbonyl compound. For but-1-yne, OH "
      "goes to C-2 (Markovnikov), giving butan-2-one. In but-2-yne the triple bond is between C-2 and C-3, so the "
      "carbonyl group must form on one of these carbons; both directions give butan-2-one, not an aldehyde.",
      ["I: CH≡C–CH₂CH₃ → CH₃COCH₂CH₃ → true", "II: CH₃C≡CCH₃ → CH₃COCH₂CH₃ → false"],
      ncert=f"{NC11}, 'Hydrocarbons', alkynes: addition of water", seconds=50),
]

# ================================================================ Organic Compounds Containing Halogens (1441-1450)
# 1442: DDT, C14H9Cl5
m_ddt = mm(C=14, H=9, Cl=5)
assert m_ddt == F(3545, 10)
v_1442 = pct(5 * CL / m_ddt)
assert v_1442 == "50.1%" and pct(CL / m_ddt) == "10.0%" and pct(3 * CL / m_ddt) == "30.0%" and \
    pct(4 * CL / m_ddt) == "40.1%"
# 1444: CnH2n+1Cl with 38.4% Cl
pc = {n: CL / mm(C=n, H=2 * n + 1, Cl=1) for n in (2, 3, 4, 5)}
match_n = [n for n, v in pc.items() if pct(v) == "38.4%"]
assert match_n == [4]
v_1444 = "C₄H₉Cl"

QUESTIONS += [
    Q(T_HX, "SN1 and SN2", "Basic", "direct",
      "To study optical activity, plane polarised light is used. Ordinary light is converted into plane polarised "
      "light by passing it through a:",
      ["Diffraction grating", "Glass prism", "Convex lens", "Nicol prism"], "D",
      "Plane polarised light and optical activity",
      "When ordinary light is passed through a Nicol prism (made of calcite), the emerging light vibrates in a "
      "single plane. Optically active compounds rotate the plane of this light; the rotation is measured with a "
      "polarimeter.",
      ["Nicol prism → plane polarised light", "Polarimeter measures the rotation"],
      why_others_wrong="A glass prism disperses light into colours; a grating diffracts it; a lens focuses it. None "
                       "polarises light.",
      ncert=f"{NC12}, 'Haloalkanes and Haloarenes', optical isomerism", seconds=20),

    N(T_HX, "Polyhalogen compounds", "Basic",
      "DDT, p,p′-dichlorodiphenyltrichloroethane, has the molecular formula C₁₄H₉Cl₅. The percentage of chlorine by "
      "mass in DDT is (C = 12, H = 1, Cl = 35.5):",
      ["30.0%", "40.1%", "50.1%", "10.0%"], "C", v_1442,
      "Percentage composition of a polyhalogen compound",
      "Molar mass of C₁₄H₉Cl₅ = 14(12) + 9(1) + 5(35.5) = 354.5 g mol⁻¹; five chlorine atoms contribute 177.5 g.",
      ["M = 168 + 9 + 177.5 = 354.5 g mol⁻¹", "% Cl = 177.5/354.5 × 100 = 50.1%"],
      why_others_wrong="30.0% counts only the three Cl of the CCl₃ group; 40.1% counts four Cl; 10.0% counts one Cl.",
      ncert=f"{NC12}, 'Haloalkanes and Haloarenes', polyhalogen compounds (DDT)", seconds=40),

    Q(T_HX, "Polyhalogen compounds", "Basic", "statement_pair",
      *sp("The effectiveness of DDT as an insecticide was discovered by Paul Müller, who received the Nobel Prize in "
          "Medicine and Physiology in 1948 for this discovery.", True,
          "Many species of insects have developed resistance to DDT.", True),
      "DDT: discovery and problems",
      "NCERT records that DDT, first prepared in 1873, was found to be an effective insecticide by Paul Müller in "
      "1939, and he received the 1948 Nobel Prize. Its use later caused problems: many insect species became "
      "resistant to it, and it is not metabolised rapidly by animals, so it accumulates in fatty tissues.",
      ["I: true", "II: true"],
      ncert=f"{NC12}, 'Haloalkanes and Haloarenes', polyhalogen compounds (DDT)", seconds=30),

    N(T_HX, "C-X bond and preparation", "Intermediate",
      "A monochloroalkane, CₙH₂ₙ₊₁Cl, contains 38.4% chlorine by mass. Its molecular formula is "
      "(C = 12, H = 1, Cl = 35.5):",
      ["C₃H₇Cl", "C₄H₉Cl", "C₅H₁₁Cl", "C₂H₅Cl"], "B", v_1444,
      "Finding the formula of a haloalkane from its composition",
      "The compound has one chlorine atom, so its molar mass M = 35.5/0.384 ≈ 92.5 g mol⁻¹. For CₙH₂ₙ₊₁Cl, "
      "M = 14n + 36.5.",
      ["M = 35.5/0.384 ≈ 92.5 g mol⁻¹", "14n + 36.5 = 92.5 → n = 4", "Formula C₄H₉Cl"],
      why_others_wrong="C₃H₇Cl has 45.2% Cl, C₅H₁₁Cl 33.3% and C₂H₅Cl 55.0%.",
      ncert=f"{NC12}, 'Haloalkanes and Haloarenes', classification and nomenclature", seconds=60),

    Q(T_HX, "Polyhalogen compounds", "Intermediate", "direct",
      "Freon-12, CCl₂F₂, one of the most common freons in industrial use, is manufactured from tetrachloromethane "
      "by the:",
      ["Finkelstein reaction", "Swarts reaction", "Wurtz reaction", "Sandmeyer reaction"], "B",
      "Preparation of freons by halogen exchange",
      "Replacing chlorine by fluorine using a metallic fluoride (such as SbF₃ or AgF) is the Swarts reaction. NCERT "
      "states that Freon-12 is made from CCl₄ in this way.",
      ["CCl₄ + metallic fluoride → CCl₂F₂ (Swarts reaction)"],
      why_others_wrong="The Finkelstein reaction exchanges Cl/Br for I with NaI in acetone; the Wurtz reaction "
                       "couples alkyl halides with sodium; the Sandmeyer reaction uses diazonium salts.",
      ncert=f"{NC12}, 'Haloalkanes and Haloarenes', polyhalogen compounds (freons)", seconds=30),

    Q(T_HX, "C-X bond and preparation", "Intermediate", "assertion_reason",
      *ar("Chloroform, shaken with aqueous silver nitrate solution, gives an immediate white precipitate of AgCl.",
          False,
          "In chloroform the chlorine atoms are covalently bonded to carbon, so free chloride ions are not present.",
          True),
      "Covalent halogen and the silver nitrate test",
      "Silver nitrate precipitates only halide ions. In CHCl₃ the chlorine is held by covalent C–Cl bonds, so no "
      "precipitate forms directly; that is why an organic compound is first fused with sodium (Lassaigne's test) to "
      "convert covalent halogen into NaX before the AgNO₃ test. A is false, R is true.",
      ["A: no free Cl⁻ → no immediate AgCl → false", "R: covalent C–Cl → true"],
      ncert=f"{NC11}, 'Organic Chemistry – Some Basic Principles and Techniques', detection of halogens",
      seconds=40),

    Q(T_HX, "SN1 and SN2", "Intermediate", "multi_statement",
      *ms("Which of the following statements about elimination and substitution in alkyl halides are correct?",
          [("A bulkier nucleophile prefers to act as a base and abstract a proton rather than approach a carbon "
            "atom.", True),
           ("A primary alkyl halide prefers to react by the SN2 mechanism.", True),
           ("A tertiary alkyl halide treated with a strong base undergoes the SN2 reaction rather than "
            "elimination.", False),
           ("Dehydrohalogenation is called β-elimination because the hydrogen atom is removed from the β-carbon.",
            True),
           ("A secondary alkyl halide can undergo substitution but never elimination.", False)],
          [["a", "c", "d"], ["b", "d", "e"], ["a", "b", "c"]], "C"),
      "Elimination versus substitution",
      "A species with a lone pair can act as a nucleophile or a base. Bulky reagents find it easier to remove a "
      "β-hydrogen than to reach the carbon, so they favour elimination. Primary halides prefer SN2; secondary halides "
      "may give SN2 or elimination depending on the base/nucleophile; tertiary halides give SN1 or elimination "
      "(steric hindrance blocks SN2).",
      ["(a) true", "(b) true", "(c) tertiary halides do not undergo SN2 → false", "(d) true",
       "(e) secondary halides can eliminate → false"],
      why_others_wrong="The other options include (c) or (e), both false, or leave out a true statement.",
      ncert=f"{NC12}, 'Haloalkanes and Haloarenes', elimination reactions (elimination versus substitution)",
      seconds=60),

    Q(T_HX, "C-X bond and preparation", "Advanced", "match_list",
      *ml("Match the structure in List-I with its IUPAC name in List-II.",
          ["CH₃–CHCl–CHBr–CH₃", "CH₂=CH–CHCl–CH₃", "(CH₃)₂CH–CH₂Br", "ClCH₂–C≡C–CH₂Cl"],
          ["1-Bromo-2-methylpropane", "2-Bromo-3-chlorobutane", "1,4-Dichlorobut-2-yne", "3-Chlorobut-1-ene"],
          "II IV I III", ["II I IV III", "IV II I III", "II IV III I"], "A"),
      "IUPAC names of halogen compounds",
      "A: both directions give the locants {2, 3}; the tie is broken alphabetically, so bromo gets the lower locant: "
      "2-bromo-3-chlorobutane. B: the double bond gets locant 1 and Cl is on C-3: 3-chlorobut-1-ene. C: the longest "
      "chain has three carbons: 1-bromo-2-methylpropane. D: the triple bond is at C-2 and the two Cl atoms at C-1 "
      "and C-4: 1,4-dichlorobut-2-yne.",
      ["A → II", "B → IV", "C → I", "D → III"],
      why_others_wrong="The other codes swap the alkene and the dihalide, or the alkyne and the branched bromide.",
      ncert=f"{NC12}, 'Haloalkanes and Haloarenes', nomenclature", seconds=60),

    Q(T_HX, "C-X bond and preparation", "Advanced", "direct",
      "The dipole moments of the methyl halides do not simply follow the electronegativity of the halogen. Which of "
      "the following has the largest dipole moment?",
      ["CH₃F", "CH₃Br", "CH₃Cl", "CH₃I"], "C",
      "Dipole moment of the C–X bond: charge and bond length",
      "Dipole moment depends on both the charge separation and the bond length. C–F is the most polar bond, but it "
      "is much shorter than C–Cl; the longer C–Cl bond with a large charge separation gives CH₃Cl the largest dipole "
      "moment (NCERT: CH₃F 1.847 D, CH₃Cl 1.860 D, CH₃Br 1.830 D, CH₃I 1.636 D).",
      ["μ = charge × distance", "C–F: largest charge but shortest bond", "CH₃Cl has the highest value"],
      why_others_wrong="CH₃F is the common trap (most electronegative halogen); CH₃Br and CH₃I have smaller charge "
                       "separation.",
      ncert=f"{NC12}, 'Haloalkanes and Haloarenes', nature of the C–X bond (table of dipole moments)", seconds=45),

    Q(T_HX, "SN1 and SN2", "Advanced", "direct",
      "Propan-1-ol is heated with thionyl chloride to give X. X is heated with silver cyanide to give Y as the main "
      "product. Y is:",
      ["CH₃CH₂CH₂–CN", "(CH₃)₂CH–NC", "(CH₃)₂CH–CN", "CH₃CH₂CH₂–NC"], "D",
      "Alkyl halide from an alcohol, then reaction with an ambident nucleophile",
      "SOCl₂ replaces –OH by –Cl without changing the carbon skeleton, so X is 1-chloropropane. AgCN is mainly covalent; only the nitrogen "
      "lone pair is free to attack, so the main product is an isocyanide: 1-propyl isocyanide, CH₃CH₂CH₂NC.",
      ["CH₃CH₂CH₂OH + SOCl₂ → CH₃CH₂CH₂Cl (X) + SO₂ + HCl", "X + AgCN → CH₃CH₂CH₂–NC (Y, isocyanide)"],
      why_others_wrong="Nitriles (–CN) are the main products with KCN, not AgCN; the isopropyl products would need "
                       "a change in the carbon chain, which does not occur.",
      ncert=f"{NC12}, 'Haloalkanes and Haloarenes', preparation from alcohols and nucleophilic substitution",
      seconds=60),
]

# ================================================================ Organic Compounds Containing Oxygen (1451-1470)
# 1451: (CH3COOH)2
v_1451 = f"{2 * mm(C=2, H=4, O=2)} g mol⁻¹"
assert v_1451 == "120 g mol⁻¹"
# 1452: CH3COCH3 + HOCH2CH2OH -> 2,2-dimethyl-1,3-dioxolane (C5H10O2) + H2O ; 5.8 g propanone
n_1452 = F(58, 10) / mm(C=3, H=6, O=1)
assert n_1452 == F(1, 10) and mm(C=5, H=10, O=2) == 102
v_1452 = g(n_1452 * mm(C=5, H=10, O=2))
assert v_1452 == "10.2 g" and g(n_1452 * (58 + 62)) == "12.0 g"
# 1457: Ka ratio = 10**(4.76 - 2.86) = 10**1.90 ; antilog 0.90 = 7.94
v_1457 = f"≈ {7.94 * 10:.0f}"
assert v_1457 == "≈ 79" and abs(10 ** 1.90 - 79.4) < 0.1
# 1458: cumene C9H12 -> phenol + propanone ; 12.0 g
n_1458 = F(120, 10) / mm(C=9, H=12)
assert n_1458 == F(1, 10)
v_1458 = g(n_1458 * mm(C=3, H=6, O=1))
assert v_1458 == "5.8 g" and g(n_1458 * mm(C=6, H=6, O=1)) == "9.4 g"
# 1465: phenol -> salicylic acid (Kolbe) -> aspirin (C9H8O4) ; 9.4 g phenol, 80% overall yield
n_1465 = F(94, 10) / mm(C=6, H=6, O=1)
assert n_1465 == F(1, 10) and mm(C=9, H=8, O=4) == 180 and mm(C=7, H=6, O=3) == 138
v_1465 = g(n_1465 * 180 * F(8, 10))
assert v_1465 == "14.4 g" and g(n_1465 * 180) == "18.0 g" and g(n_1465 * 138) == "13.8 g" and \
    g(n_1465 * 138 * F(8, 10)) == "11.0 g"
# 1466: Kc = 4, 1 mol acid + 1 mol alcohol: x^2/(1-x)^2 = 4 -> x = 2/3
x_1466 = F(2, 3)
assert x_1466 ** 2 / (1 - x_1466) ** 2 == 4
v_1466 = f"{float(x_1466):.2f} mol"
assert v_1466 == "0.67 mol" and f"{4 / 5:.2f} mol" == "0.80 mol"
# 1467: phenol pKa 10.0, 0.010 M: [H+] = sqrt(1e-10 * 1e-2) = 1e-6
v_1467 = f"{-math.log10(math.sqrt(1e-10 * 1e-2)):.1f}"
assert v_1467 == "6.0"

QUESTIONS += [
    N(T_OX, "Carboxylic acids", "Basic",
      "In aprotic solvents such as benzene, ethanoic acid molecules associate as hydrogen-bonded dimers. If ethanoic "
      "acid were completely dimerised in benzene, the molar mass found from a colligative property would be "
      "(C = 12, H = 1, O = 16):",
      ["120 g mol⁻¹", "60 g mol⁻¹", "30 g mol⁻¹", "118 g mol⁻¹"], "A", v_1451,
      "Dimerisation of carboxylic acids",
      "Two molecules of CH₃COOH (60 g mol⁻¹) are held together by two hydrogen bonds. Complete dimerisation halves "
      "the number of particles, so the apparent molar mass doubles.",
      ["M(CH₃COOH) = 60 g mol⁻¹", "Dimer (CH₃COOH)₂ → apparent M = 2 × 60 = 120 g mol⁻¹"],
      why_others_wrong="60 g mol⁻¹ assumes no association; 30 g mol⁻¹ assumes dissociation into two particles; "
                       "118 g mol⁻¹ wrongly subtracts two hydrogen atoms for the hydrogen bonds.",
      ncert=f"{NC12}, 'Aldehydes, Ketones and Carboxylic Acids', physical properties of carboxylic acids",
      seconds=30),

    N(T_OX, "Aldehydes and ketones", "Basic",
      "Propanone reacts with ethane-1,2-diol (ethylene glycol) in the presence of dry HCl to form a cyclic ketal, "
      "2,2-dimethyl-1,3-dioxolane (C₅H₁₀O₂), and water. The mass of the ketal obtained from 5.8 g of propanone, "
      "assuming complete conversion, is (C = 12, H = 1, O = 16):",
      ["5.8 g", "12.0 g", "10.2 g", "8.4 g"], "C", v_1452,
      "Ketal formation from ketones and ethylene glycol",
      "One mole of ketone reacts with one mole of the diol and loses one mole of water to give one mole of the "
      "cyclic ketal.",
      ["n(propanone) = 5.8/58 = 0.1 mol", "M(C₅H₁₀O₂) = 60 + 10 + 32 = 102 g mol⁻¹", "Mass = 0.1 × 102 = 10.2 g"],
      why_others_wrong="12.0 g adds the diol but forgets the water lost; 5.8 g is the mass of propanone; 8.4 g has no "
                       "basis in the equation.",
      ncert=f"{NC12}, 'Aldehydes, Ketones and Carboxylic Acids', nucleophilic addition of alcohols (ethylene "
            "glycol ketals)", seconds=45),

    Q(T_OX, "Alcohols", "Basic", "direct",
      "Which of the following reagents reduces ethanal to ethanol but does NOT reduce ethanoic acid?",
      ["Lithium aluminium hydride", "Diborane", "Zinc amalgam and concentrated HCl", "Sodium borohydride"], "D",
      "Selectivity of reducing agents",
      "NaBH₄ reduces aldehydes and ketones to alcohols but does not reduce the carboxyl group. LiAlH₄ and diborane "
      "reduce both. Zn–Hg/HCl (Clemmensen) reduces a carbonyl group to CH₂, giving ethane, not ethanol.",
      ["NaBH₄: CH₃CHO → CH₃CH₂OH; –COOH unaffected"],
      why_others_wrong="LiAlH₄ and diborane also reduce carboxylic acids to primary alcohols; Clemmensen reduction "
                       "gives an alkane.",
      ncert=f"{NC12}, 'Aldehydes, Ketones and Carboxylic Acids', reduction of carboxylic acids", seconds=35),

    Q(T_OX, "Alcohols", "Basic", "direct",
      "In the preparation of ethanol by fermentation, the sugar in molasses is first converted into glucose and "
      "fructose by an enzyme. This enzyme is:",
      ["Zymase", "Invertase", "Diastase", "Maltase"], "B",
      "Fermentation of sugar to ethanol",
      "Invertase converts sucrose (from molasses, sugarcane or grapes) into glucose and fructose. Zymase, found in "
      "yeast, then ferments these to ethanol and carbon dioxide.",
      ["Sucrose → glucose + fructose (invertase)", "Glucose/fructose → ethanol + CO₂ (zymase)"],
      why_others_wrong="Zymase acts in the second step; diastase and maltase act on starch and maltose, not on the "
                       "sugar of molasses as described.",
      ncert=f"{NC12}, 'Alcohols, Phenols and Ethers', commercially important alcohols (ethanol)", seconds=25),

    Q(T_OX, "Aldehydes and ketones", "Basic", "statement_pair",
      *sp("Fehling's solution B is an alkaline solution of sodium potassium tartrate (Rochelle salt).", True,
          "Tollens' reagent is an alkaline solution of copper(II) sulphate.", False),
      "Composition of Fehling's and Tollens' reagents",
      "Fehling's reagent is made just before use from Fehling A (aqueous copper sulphate) and Fehling B (alkaline "
      "sodium potassium tartrate). Tollens' reagent is freshly prepared ammoniacal silver nitrate solution.",
      ["I: true", "II: Tollens' reagent = ammoniacal AgNO₃ → false"],
      ncert=f"{NC12}, 'Aldehydes, Ketones and Carboxylic Acids', oxidation (Tollens' and Fehling's tests)",
      seconds=30),

    Q(T_OX, "Aldehydes and ketones", "Basic", "match_list",
      *ml("Match the common name in List-I with the IUPAC name in List-II.",
          ["Acetophenone", "Benzophenone", "Isobutyraldehyde", "Methyl n-propyl ketone"],
          ["2-Methylpropanal", "Pentan-2-one", "Diphenylmethanone", "1-Phenylethan-1-one"],
          "IV III I II", ["III IV I II", "IV III II I", "IV I III II"], "D"),
      "Common and IUPAC names of carbonyl compounds",
      "Acetophenone is C₆H₅COCH₃ (1-phenylethan-1-one); benzophenone is C₆H₅COC₆H₅ (diphenylmethanone); "
      "isobutyraldehyde is (CH₃)₂CHCHO (2-methylpropanal); methyl n-propyl ketone is CH₃COCH₂CH₂CH₃ "
      "(pentan-2-one).",
      ["A → IV", "B → III", "C → I", "D → II"],
      why_others_wrong="The other codes swap the two aromatic ketones or the aldehyde and the aliphatic ketone.",
      ncert=f"{NC12}, 'Aldehydes, Ketones and Carboxylic Acids', nomenclature", seconds=40),

    N(T_OX, "Carboxylic acids", "Intermediate",
      "The pKa of chloroethanoic acid is 2.86 and that of ethanoic acid is 4.76. The ratio Ka(ClCH₂COOH) / "
      "Ka(CH₃COOH) is about (antilog 0.90 = 7.94):",
      ["≈ 1.9", "≈ 79", "≈ 7.9", "≈ 1.7"], "B", v_1457,
      "Comparing acid strengths from pKa values",
      "pKa = −log Ka, so the ratio of Ka values is 10 raised to the difference in pKa. The electron-withdrawing "
      "chlorine (−I effect) stabilises the carboxylate ion and raises Ka.",
      ["Ka ratio = 10^(4.76 − 2.86) = 10^1.90", "10^1.90 = 7.94 × 10 ≈ 79"],
      why_others_wrong="1.9 is the difference in pKa, not the ratio of Ka; 7.9 drops a factor of 10; 1.7 is the "
                       "ratio of the two pKa values (4.76/2.86).",
      ncert=f"{NC12}, 'Aldehydes, Ketones and Carboxylic Acids', acidity of carboxylic acids (effect of "
            "substituents)", seconds=60),

    N(T_OX, "Phenols", "Intermediate",
      "In the industrial preparation of phenol, cumene (isopropylbenzene, C₉H₁₂) is oxidised in air to cumene "
      "hydroperoxide, which is decomposed by dilute acid. The mass of the by-product propanone obtained from 12.0 g "
      "of cumene, assuming complete conversion, is (C = 12, H = 1, O = 16):",
      ["9.4 g", "6.0 g", "5.8 g", "11.6 g"], "C", v_1458,
      "Cumene process: stoichiometry",
      "One mole of cumene gives one mole of phenol and one mole of propanone.",
      ["n(cumene) = 12.0/120 = 0.1 mol", "n(propanone) = 0.1 mol", "Mass = 0.1 × 58 = 5.8 g"],
      why_others_wrong="9.4 g is the mass of phenol; 11.6 g takes two moles of propanone per mole of cumene; 6.0 g "
                       "uses 60 g mol⁻¹ for propanone.",
      ncert=f"{NC12}, 'Alcohols, Phenols and Ethers', preparation of phenols (from cumene)", seconds=50),

    Q(T_OX, "Ethers", "Intermediate", "direct",
      "Anisole (methoxybenzene) is treated with ethanoyl chloride in the presence of anhydrous AlCl₃. The main "
      "product(s) is/are:",
      ["Phenyl ethanoate and chloromethane", "A mixture of 2-methoxyacetophenone and 4-methoxyacetophenone",
       "3-Methoxyacetophenone", "Acetophenone and methanol"], "B",
      "Friedel–Crafts acylation of an aromatic ether",
      "The –OCH₃ group activates the ring and directs incoming electrophiles to the ortho and para positions (+R "
      "effect). In the Friedel–Crafts acylation the electrophile CH₃CO⁺ substitutes the ring, giving 2- and "
      "4-methoxyacetophenone; the ether linkage is not broken.",
      ["CH₃COCl + AlCl₃ → CH₃CO⁺ (electrophile)", "–OCH₃: ortho/para directing",
       "Products: 2- and 4-methoxyacetophenone"],
      why_others_wrong="The meta product is not the main one; AlCl₃/CH₃COCl does not cleave the C–O bonds of the "
                       "ether, so phenyl ethanoate or methanol are not formed.",
      ncert=f"{NC12}, 'Alcohols, Phenols and Ethers', electrophilic substitution in aromatic ethers", seconds=40),

    Q(T_OX, "Aldehydes and ketones", "Intermediate", "direct",
      "Toluene is treated with chromic oxide (CrO₃) in acetic anhydride, and the product is hydrolysed with aqueous "
      "acid to give benzaldehyde. The intermediate that is hydrolysed is:",
      ["Benzoic acid", "Benzyl alcohol", "Benzoyl chloride", "Benzylidene diacetate"], "D",
      "Preparation of benzaldehyde from toluene with CrO₃",
      "In acetic anhydride the methyl group of toluene is oxidised and trapped as benzylidene diacetate, "
      "C₆H₅CH(OCOCH₃)₂, which protects the aldehyde from further oxidation. Acid hydrolysis then releases "
      "benzaldehyde.",
      ["C₆H₅CH₃ + CrO₃/(CH₃CO)₂O → C₆H₅CH(OCOCH₃)₂", "Hydrolysis (H₃O⁺) → C₆H₅CHO"],
      why_others_wrong="Benzoic acid would be over-oxidation; benzyl alcohol and benzoyl chloride are not formed in "
                       "this reaction.",
      ncert=f"{NC12}, 'Aldehydes, Ketones and Carboxylic Acids', preparation of aromatic aldehydes", seconds=35),

    Q(T_OX, "Aldehydes and ketones", "Intermediate", "assertion_reason",
      *ar("The α-hydrogen atoms of aldehydes and ketones are acidic.", True,
          "The carbonyl group withdraws electrons strongly, and the conjugate base (carbanion) formed by losing an "
          "α-hydrogen is stabilised by resonance.", True, explains=True),
      "Acidity of α-hydrogens",
      "NCERT attributes the acidity of α-hydrogens to the strong electron-withdrawing effect of the carbonyl group "
      "and to resonance stabilisation of the conjugate base (the negative charge is shared with the oxygen). This "
      "acidity is the basis of aldol condensation and the haloform reaction. R explains A.",
      ["–I of C=O weakens the α C–H bond", "Enolate ion stabilised by resonance", "R explains A"],
      ncert=f"{NC12}, 'Aldehydes, Ketones and Carboxylic Acids', reactions due to α-hydrogen", seconds=40),

    Q(T_OX, "Alcohols", "Intermediate", "statement_pair",
      *sp("Commercially, carboxylic acids are reduced to alcohols by first converting them into esters and then "
          "hydrogenating the esters in the presence of a catalyst.", True,
          "Diborane reduces carboxylic acids to primary alcohols.", True),
      "Reduction of carboxylic acids to alcohols",
      "LiAlH₄ is expensive, so industrially the acid is converted to an ester and the ester is hydrogenated "
      "catalytically. Carboxylic acids are reduced to primary alcohols by LiAlH₄ or, better, by diborane, which does "
      "not easily reduce ester, nitro or halo groups.",
      ["I: true", "II: true"],
      ncert=f"{NC12}, 'Alcohols, Phenols and Ethers', preparation of alcohols; 'Aldehydes, Ketones and Carboxylic "
            "Acids', reduction", seconds=35),

    Q(T_OX, "Ethers", "Intermediate", "match_list",
      *ml("Match the common name of the ether in List-I with its IUPAC name in List-II.",
          ["Anisole", "Phenetole", "Methyl isopropyl ether", "Diethyl ether"],
          ["Ethoxyethane", "2-Methoxypropane", "Methoxybenzene", "Ethoxybenzene"],
          "III IV II I", ["IV III II I", "III IV I II", "III II IV I"], "C"),
      "Nomenclature of ethers",
      "In IUPAC names, ethers are named as alkoxy derivatives of the larger hydrocarbon. Anisole is C₆H₅OCH₃ "
      "(methoxybenzene), phenetole is C₆H₅OC₂H₅ (ethoxybenzene), methyl isopropyl ether is CH₃OCH(CH₃)₂ "
      "(2-methoxypropane), and diethyl ether is ethoxyethane.",
      ["A → III", "B → IV", "C → II", "D → I"],
      why_others_wrong="The other codes swap anisole and phenetole or the two aliphatic ethers.",
      ncert=f"{NC12}, 'Alcohols, Phenols and Ethers', nomenclature of ethers", seconds=40),

    Q(T_OX, "Carboxylic acids", "Intermediate", "direct",
      "In the acid-catalysed esterification of a carboxylic acid with an alcohol, the carbonyl oxygen is first "
      "protonated and the alcohol then adds to the carbonyl carbon. The molecule of water eliminated takes its oxygen "
      "atom from:",
      ["the carboxylic acid", "the alcohol", "the sulphuric acid used as catalyst",
       "the alcohol and the acid in equal proportion"], "A",
      "Mechanism of esterification (nucleophilic acyl substitution)",
      "After the alcohol adds, a proton transfer in the tetrahedral intermediate converts one of the acid's oxygen "
      "groups into –OH₂⁺, a good leaving group, which leaves as water. The alcohol oxygen stays in the ester as the "
      "–OR group.",
      ["Protonation of C=O", "Alcohol oxygen attacks carbonyl carbon (stays in ester)",
       "–OH₂⁺ formed from an acid oxygen leaves as H₂O"],
      why_others_wrong="The alcohol oxygen becomes the ester's –O–R; H₂SO₄ is only a catalyst and is regenerated.",
      ncert=f"{NC12}, 'Aldehydes, Ketones and Carboxylic Acids', esterification (mechanism)", seconds=45),

    N(T_OX, "Phenols", "Advanced",
      "9.4 g of phenol is converted into salicylic acid by Kolbe's reaction, and the salicylic acid is then "
      "acetylated to aspirin (acetylsalicylic acid, C₉H₈O₄). If the overall yield is 80%, the mass of aspirin "
      "obtained is (C = 12, H = 1, O = 16):",
      ["18.0 g", "14.4 g", "13.8 g", "11.0 g"], "B", v_1465,
      "Two-step synthesis with an overall yield",
      "Sodium phenoxide reacts with CO₂ (Kolbe's reaction) to give, after acidification, salicylic acid "
      "(2-hydroxybenzoic acid). Acetylation of its –OH group gives aspirin. One mole of phenol gives one mole of "
      "aspirin at 100% yield.",
      ["n(phenol) = 9.4/94 = 0.1 mol", "M(aspirin) = 108 + 8 + 64 = 180 g mol⁻¹",
       "Mass = 0.1 × 180 × 0.80 = 14.4 g"],
      why_others_wrong="18.0 g ignores the yield; 13.8 g is the theoretical mass of salicylic acid; 11.0 g is 80% of "
                       "the salicylic acid.",
      ncert=f"{NC12}, 'Alcohols, Phenols and Ethers', Kolbe's reaction and acetylation of salicylic acid",
      seconds=75),

    N(T_OX, "Carboxylic acids", "Advanced",
      "For the esterification CH₃COOH + C₂H₅OH ⇌ CH₃COOC₂H₅ + H₂O, Kc = 4 at the temperature of the experiment. "
      "If 1.0 mol of ethanoic acid and 1.0 mol of ethanol are allowed to reach equilibrium, the amount of ester "
      "formed is:",
      ["0.50 mol", "0.80 mol", "0.33 mol", "0.67 mol"], "D", v_1466,
      "Reversibility of esterification",
      "Esterification is reversible. With x mol of ester and x mol of water formed, (1 − x) mol of each reactant "
      "remains; the volume cancels because Δn = 0.",
      ["Kc = x²/(1 − x)² = 4", "x/(1 − x) = 2 → x = 2/3", "Ester ≈ 0.67 mol"],
      why_others_wrong="0.80 mol solves x/(1 − x) = 4 (no square root); 0.50 mol assumes Kc = 1; 0.33 mol is the "
                       "amount of acid left.",
      ncert=f"{NC12}, 'Aldehydes, Ketones and Carboxylic Acids', esterification; {NC11}, 'Equilibrium'",
      seconds=75),

    N(T_OX, "Phenols", "Advanced",
      "The pKa of phenol is 10.0. Treating phenol as a weak monobasic acid, the pH of a 0.010 M aqueous solution of "
      "phenol is:",
      ["5.0", "6.0", "12.0", "4.0"], "B", v_1467,
      "Weak acidity of phenol",
      "For a weak acid with small ionisation, [H⁺] = √(Ka·C).",
      ["Ka = 10⁻¹⁰, C = 10⁻² M", "[H⁺] = √(10⁻¹²) = 10⁻⁶ M", "pH = 6.0"],
      why_others_wrong="5.0 and 4.0 come from wrong square roots; 12.0 adds pKa and −log C without halving.",
      ncert=f"{NC12}, 'Alcohols, Phenols and Ethers', acidity of phenols; {NC11}, 'Equilibrium'", seconds=60),

    Q(T_OX, "Carboxylic acids", "Advanced", "multi_statement",
      *ms("Which of the following comparisons of acid strength are correct?",
          [("4-Nitrobenzoic acid is a stronger acid than benzoic acid.", True),
           ("4-Methoxybenzoic acid is a stronger acid than benzoic acid.", False),
           ("CF₃COOH is a stronger acid than CCl₃COOH.", True),
           ("Phenylethanoic acid (C₆H₅CH₂COOH) is a stronger acid than benzoic acid.", False),
           ("Ethanoic acid is a stronger acid than propanoic acid.", True)],
          [["a", "b", "c"], ["a", "d", "e"], ["b", "c", "e"]], "C"),
      "Effect of substituents on the acidity of carboxylic acids",
      "Electron-withdrawing groups (–NO₂, –CF₃, –CCl₃) stabilise the carboxylate ion and increase acidity; fluorine "
      "withdraws more strongly than chlorine. Electron-donating groups (–OCH₃, alkyl) decrease it. A phenyl group "
      "attached directly to –COOH increases acidity, but the effect falls when a CH₂ group separates them. NCERT's "
      "order includes CF₃COOH > CCl₃COOH and C₆H₅COOH > C₆H₅CH₂COOH > CH₃COOH > CH₃CH₂COOH.",
      ["(a) –NO₂ (EWG) → true", "(b) –OCH₃ (EDG) → false", "(c) –CF₃ stronger EWG → true",
       "(d) phenylethanoic acid is weaker → false", "(e) ethyl (+I) weakens → true"],
      why_others_wrong="The other options include (b) or (d), both false.",
      ncert=f"{NC12}, 'Aldehydes, Ketones and Carboxylic Acids', effect of substituents on acidity", seconds=75),

    Q(T_OX, "Aldehydes and ketones", "Advanced", "direct",
      "Benzene is treated with ethanoyl chloride in the presence of anhydrous AlCl₃ to give X. X is warmed with "
      "iodine and aqueous NaOH to give a yellow precipitate and a salt Y. Acidification of Y gives Z. Z is:",
      ["Phenylethanoic acid", "Benzaldehyde", "Phenol", "Benzoic acid"], "D",
      "Friedel–Crafts acylation followed by the haloform reaction",
      "Friedel–Crafts acylation gives acetophenone, C₆H₅COCH₃ (X). As a methyl ketone it gives the iodoform reaction: "
      "the CH₃ group becomes CHI₃ (yellow precipitate) and the rest becomes sodium benzoate (Y). Acidification gives "
      "benzoic acid (Z).",
      ["C₆H₆ + CH₃COCl (AlCl₃) → C₆H₅COCH₃", "C₆H₅COCH₃ + I₂/NaOH → CHI₃ + C₆H₅COONa",
       "C₆H₅COONa + H⁺ → C₆H₅COOH"],
      why_others_wrong="The haloform reaction removes one carbon (the methyl), so the acid has the same carbon count "
                       "as the benzoyl group, not phenylethanoic acid. No aldehyde or phenol is formed.",
      ncert=f"{NC12}, 'Aldehydes, Ketones and Carboxylic Acids', preparation of ketones and the haloform reaction",
      seconds=60),

    Q(T_OX, "Phenols", "Advanced", "assertion_reason",
      *ar("p-Nitrophenol is a stronger acid than m-nitrophenol.", True,
          "At the para position the –NO₂ group withdraws electrons by both the −I and −R effects and delocalises the "
          "negative charge of the phenoxide ion onto itself, whereas at the meta position only its −I effect "
          "operates.", True, explains=True),
      "Position of a substituent and the acidity of phenols",
      "NCERT gives pKa values of 7.1 for p-nitrophenol and 8.3 for m-nitrophenol. At the para position the negative "
      "charge of the phenoxide ion can be delocalised onto the nitro group by resonance; at the meta position it "
      "cannot, so only the weaker inductive effect helps. R explains A.",
      ["p-isomer: −I and −R → phenoxide strongly stabilised", "m-isomer: −I only",
       "Lower pKa for p-nitrophenol; R explains A"],
      ncert=f"{NC12}, 'Alcohols, Phenols and Ethers', acidity of phenols (Table of pKa values)", seconds=50),
]

# ================================================================ Organic Compounds Containing Nitrogen (1471-1480)
# 1471: CH3NH2 -> (CH3)2NH -> (CH3)3N -> (CH3)4N+ I- : one CH3I per step
steps_1471 = ["CH3NH2 -> (CH3)2NH", "(CH3)2NH -> (CH3)3N", "(CH3)3N -> (CH3)4N+I-"]
v_1471 = str(len(steps_1471))
assert v_1471 == "3"
# 1474: aniline -> sulphanilic acid (C6H7NO3S) ; 9.3 g
n_1474 = F(93, 10) / mm(C=6, H=7, N=1)
assert n_1474 == F(1, 10) and mm(C=6, H=7, N=1, O=3, S=1) == 173 and mm(C=6, H=9, N=1, O=4, S=1) == 191
v_1474 = g(n_1474 * 173)
assert v_1474 == "17.3 g" and g(n_1474 * 191) == "19.1 g"
# 1478: pKb 3.38 and 9.38 ; [OH-] = sqrt(Kb*C) -> ratio = sqrt(10**6)
ratio_kb = 10 ** (9.38 - 3.38)
v_1478 = f"{math.sqrt(ratio_kb):.0f}"
assert v_1478 == "1000" and round(ratio_kb) == 10 ** 6

QUESTIONS += [
    N(T_NI, "Amines: basicity and identification", "Basic",
      "Methanamine is treated repeatedly with iodomethane until the quaternary ammonium salt, (CH₃)₄N⁺I⁻, is "
      "formed. The minimum number of moles of CH₃I consumed per mole of methanamine is:",
      ["1", "2", "3", "4"], "C", v_1471,
      "Alkylation of amines",
      "Each reaction with CH₃I replaces one N–H hydrogen by a methyl group (and finally adds a fourth methyl to "
      "form the quaternary salt). Methanamine already carries one methyl group, so three more are needed.",
      ["CH₃NH₂ → (CH₃)₂NH → (CH₃)₃N → (CH₃)₄N⁺I⁻", "Three steps → 3 mol CH₃I"],
      why_others_wrong="1 and 2 stop at the secondary or tertiary amine; 4 counts the methyl group already present.",
      ncert=f"{NC12}, 'Amines', chemical reactions: alkylation", seconds=30),

    Q(T_NI, "Amines: basicity and identification", "Basic", "direct",
      "In Hinsberg's test for distinguishing primary, secondary and tertiary amines, benzenesulphonyl chloride is "
      "nowadays replaced by:",
      ["p-Toluenesulphonyl chloride", "Benzoyl chloride", "Ethanoyl chloride", "Chloroform and ethanolic KOH"], "A",
      "Hinsberg's reagent",
      "NCERT notes that benzenesulphonyl chloride (Hinsberg's reagent) has now been replaced by p-toluenesulphonyl "
      "chloride, which reacts with primary and secondary amines in the same way to give sulphonamides.",
      ["Hinsberg's test: ArSO₂Cl with 1°, 2° and 3° amines", "Modern reagent: p-CH₃C₆H₄SO₂Cl"],
      why_others_wrong="Benzoyl and ethanoyl chlorides give amides (acylation), not sulphonamides; chloroform with "
                       "ethanolic KOH is the carbylamine test.",
      ncert=f"{NC12}, 'Amines', reaction with arylsulphonyl chloride", seconds=25),

    Q(T_NI, "Amines: basicity and identification", "Basic", "statement_pair",
      *sp("The order of reactivity of alkyl halides with ammonia or amines is RI > RBr > RCl.", True,
          "The free amine is obtained from the ammonium salt formed in ammonolysis by treating the salt with a "
          "strong acid.", False),
      "Ammonolysis of alkyl halides",
      "NCERT gives the reactivity order RI > RBr > RCl. Ammonolysis first gives the substituted ammonium salt; the "
      "free amine is released by treating this salt with a strong base (which removes H⁺), not with an acid.",
      ["I: true", "II: a strong base is needed → false"],
      ncert=f"{NC12}, 'Amines', preparation by ammonolysis of alkyl halides", seconds=30),

    N(T_NI, "Amines: basicity and identification", "Intermediate",
      "Aniline is heated with concentrated H₂SO₄; the anilinium hydrogensulphate first formed is heated at "
      "453–473 K to give sulphanilic acid (4-aminobenzenesulphonic acid, C₆H₇NO₃S). The mass of sulphanilic acid "
      "obtained from 9.3 g of aniline, assuming complete conversion, is (C = 12, H = 1, N = 14, O = 16, S = 32):",
      ["19.1 g", "17.3 g", "15.5 g", "8.7 g"], "B", v_1474,
      "Sulphonation of aniline",
      "One mole of aniline gives one mole of sulphanilic acid. The intermediate salt, anilinium hydrogensulphate, "
      "loses water on heating.",
      ["n(aniline) = 9.3/93 = 0.1 mol", "M(C₆H₇NO₃S) = 72 + 7 + 14 + 48 + 32 = 173 g mol⁻¹",
       "Mass = 0.1 × 173 = 17.3 g"],
      why_others_wrong="19.1 g is the mass of anilinium hydrogensulphate (water not lost); 8.7 g halves the answer; "
                       "15.5 g has no basis in the equation.",
      ncert=f"{NC12}, 'Amines', electrophilic substitution: sulphonation", seconds=50),

    Q(T_NI, "Amines: basicity and identification", "Intermediate", "direct",
      "The IUPAC name of CH₃CH₂CH₂–N(CH₃)–CH₂CH₃ is:",
      ["N-Methyl-N-propylethanamine", "N-Ethyl-N-propylmethanamine", "3-Methylhexan-3-amine",
       "N-Ethyl-N-methylpropan-1-amine"], "D",
      "Naming tertiary amines",
      "In a secondary or tertiary amine, the longest alkyl group on nitrogen gives the parent name (propan-1-amine "
      "here); the other groups are cited with the locant N and listed alphabetically: N-ethyl, N-methyl.",
      ["Largest group on N: propyl → propan-1-amine", "Other groups: ethyl, methyl → N-ethyl-N-methyl",
       "N-Ethyl-N-methylpropan-1-amine"],
      why_others_wrong="Ethanamine and methanamine are not built on the largest alkyl group; 3-methylhexan-3-amine is "
                       "a primary amine with a different structure.",
      ncert=f"{NC12}, 'Amines', nomenclature", seconds=40),

    Q(T_NI, "Amines: basicity and identification", "Intermediate", "multi_statement",
      *ms("Which of the following statements about the structure and classification of amines are correct?",
          [("The nitrogen atom in amines is sp³ hybridised and the geometry around it is pyramidal.", True),
           ("Benzylamine, C₆H₅CH₂NH₂, is an arylamine.", False),
           ("The C–N–C bond angle in trimethylamine is about 108°.", True),
           ("Amines may be regarded as derivatives of ammonia in which hydrogen atoms are replaced by alkyl or aryl "
            "groups.", True),
           ("N,N-Dimethylaniline is a secondary amine.", False)],
          [["a", "b", "c"], ["a", "c", "e"], ["b", "d", "e"]], "D"),
      "Structure and classification of amines",
      "Nitrogen uses three sp³ orbitals for bonds; the fourth holds the lone pair, so amines are pyramidal and the "
      "C–N–C angle in trimethylamine is 108°, a little less than 109.5°. In an arylamine the –NH₂ group is bonded "
      "directly to the ring; benzylamine has it on a CH₂ group, so it is not an arylamine. N,N-dimethylaniline has "
      "no H on nitrogen: it is a tertiary amine.",
      ["(a) true", "(b) –NH₂ not on the ring → false", "(c) true", "(d) true", "(e) tertiary → false"],
      why_others_wrong="The other options include (b) or (e), both false.",
      ncert=f"{NC12}, 'Amines', structure and classification", seconds=55),

    Q(T_NI, "Amines: basicity and identification", "Intermediate", "match_list",
      *ml("Match the reaction in List-I with the amine formed in List-II.",
          ["CH₃CN, reduced with LiAlH₄", "CH₃CONH₂ + Br₂ + NaOH", "C₆H₅CH₂Cl + large excess of NH₃",
           "C₆H₅CONH₂ + Br₂ + NaOH"],
          ["Aniline", "Ethanamine", "Benzylamine", "Methanamine"],
          "II IV III I", ["IV II III I", "II IV I III", "II III IV I"], "A"),
      "Methods of preparing amines",
      "Reducing a nitrile adds two H₂ to C≡N with no loss of carbon: CH₃CN → CH₃CH₂NH₂. Hofmann bromamide "
      "degradation gives an amine with one carbon fewer: CH₃CONH₂ → CH₃NH₂ and C₆H₅CONH₂ → C₆H₅NH₂. Ammonolysis with "
      "excess ammonia gives mainly the primary amine: benzylamine.",
      ["A → ethanamine (II)", "B → methanamine (IV)", "C → benzylamine (III)", "D → aniline (I)"],
      why_others_wrong="The other codes forget that Hofmann degradation removes one carbon, or that nitrile reduction "
                       "keeps all the carbons.",
      ncert=f"{NC12}, 'Amines', preparation of amines", seconds=55),

    N(T_NI, "Amines: basicity and identification", "Advanced",
      "The pKb of methanamine is 3.38 and that of aniline is 9.38. For 0.01 M aqueous solutions of the two amines, "
      "each only slightly ionised, the ratio [OH⁻](methanamine) / [OH⁻](aniline) is about:",
      ["10⁶", "6", "1000", "3"], "C", v_1478,
      "Basic strength from pKb and the hydroxide ion concentration",
      "For a weak base, [OH⁻] = √(Kb·C). At equal concentrations, the ratio of [OH⁻] is the square root of the ratio "
      "of the Kb values.",
      ["Kb ratio = 10^(9.38 − 3.38) = 10⁶", "[OH⁻] ratio = √10⁶ = 10³ = 1000"],
      why_others_wrong="10⁶ is the ratio of Kb values (square root not taken); 6 and 3 confuse the pKb difference "
                       "with the ratio.",
      ncert=f"{NC12}, 'Amines', basic character (pKb values); {NC11}, 'Equilibrium'", seconds=75),

    Q(T_NI, "Diazonium salts", "Advanced", "direct",
      "Aniline is acetylated to X. X is nitrated with a mixture of concentrated HNO₃ and H₂SO₄ to give Y as the main "
      "product, and Y is hydrolysed to Z. Z is diazotised at 273–278 K and the diazonium salt is treated with "
      "hypophosphorous acid (H₃PO₂) and water. The final product is:",
      ["Aniline", "Nitrobenzene", "4-Nitrophenol", "4-Nitroacetanilide"], "B",
      "Using the amino group as a temporary directing group",
      "Acetylation gives acetanilide (X); nitration gives mainly 4-nitroacetanilide (Y); hydrolysis gives "
      "4-nitroaniline (Z). Diazotisation and reduction with H₃PO₂ replace the –N₂⁺ group by hydrogen, leaving "
      "nitrobenzene.",
      ["C₆H₅NH₂ → C₆H₅NHCOCH₃", "→ p-O₂N–C₆H₄–NHCOCH₃ → p-O₂N–C₆H₄–NH₂",
       "→ p-O₂N–C₆H₄–N₂⁺Cl⁻ → (H₃PO₂) C₆H₅NO₂"],
      why_others_wrong="4-Nitrophenol would need warming of the diazonium salt with water; aniline and "
                       "4-nitroacetanilide are earlier compounds in the sequence.",
      ncert=f"{NC12}, 'Amines', nitration of aniline and reactions of diazonium salts", seconds=75),

    Q(T_NI, "Diazonium salts", "Advanced", "assertion_reason",
      *ar("Fluorobenzene and iodobenzene are conveniently prepared from benzenediazonium salts rather than from "
          "benzene.", True,
          "Aryl fluorides and aryl iodides cannot be prepared conveniently by direct halogenation of benzene.", True,
          explains=True),
      "Importance of diazonium salts in synthesis",
      "Direct fluorination of benzene is too violent and direct iodination is reversible, so these haloarenes are "
      "made from diazonium salts: with KI for iodobenzene, and via the fluoroborate (HBF₄, then heat) for "
      "fluorobenzene. NCERT gives this as a reason for the importance of diazonium salts. R explains A.",
      ["Direct F₂: too violent; direct I₂: reversible", "ArN₂⁺ + KI → ArI; ArN₂⁺BF₄⁻ (heat) → ArF",
       "R explains A"],
      ncert=f"{NC12}, 'Amines', importance of diazonium salts in synthesis of aromatic compounds", seconds=45),
]

# ================================================================ Biomolecules (1481-1490)
# 1484: 100 base pairs, 30 A-T (2 H-bonds each), 70 G-C (3 each)
v_1484 = str(30 * 2 + 70 * 3)
assert v_1484 == "270" and 30 * 3 + 70 * 2 == 230
# 1485: amylose (C6H10O5)n, M = 81000
m_unit = mm(C=6, H=10, O=5)
assert m_unit == 162
v_1485 = str(81000 // m_unit)
assert v_1485 == "500" and 81000 // 180 == 450

QUESTIONS += [
    Q(T_BM, "Carbohydrates", "Basic", "direct",
      "The letters D and L before the names of sugars such as D-glucose indicate the relative configuration of the "
      "molecule. The reference compound for assigning D or L is:",
      ["Glyceraldehyde", "Glucose", "Fructose", "Glycine"], "A",
      "D/L configuration of sugars",
      "The configuration is compared with that of glyceraldehyde: (+)-glyceraldehyde has the D configuration. A "
      "sugar is D if the –OH on its lowest asymmetric carbon is on the right (as in D-glyceraldehyde). D and L do not "
      "tell the direction of optical rotation.",
      ["Reference: glyceraldehyde", "–OH on the right at the lowest asymmetric carbon → D"],
      why_others_wrong="Glucose and fructose are the sugars being named, not the reference; glycine has no "
                       "asymmetric carbon.",
      ncert=f"{NC12}, 'Biomolecules', configuration of monosaccharides (D/L)", seconds=25),

    Q(T_BM, "Hormones", "Basic", "match_list",
      *ml("Match the hormone in List-I with its chemical nature in List-II.",
          ["Insulin", "Testosterone", "Epinephrine (adrenaline)", "Thyroxine"],
          ["Iodothyronine", "Steroid", "Polypeptide (protein)", "Amino acid derivative"],
          "III II IV I", ["II III IV I", "III II I IV", "III IV II I"], "B"),
      "Chemical nature of hormones",
      "Hormones are chemical messengers of different kinds: insulin is a polypeptide (protein) hormone, testosterone "
      "a steroid, epinephrine an amino acid derivative, and thyroxine an iodothyronine (an iodinated derivative of "
      "tyrosine).",
      ["Insulin → polypeptide (III)", "Testosterone → steroid (II)", "Epinephrine → amino acid derivative (IV)",
       "Thyroxine → iodothyronine (I)"],
      why_others_wrong="The other codes interchange the steroid and polypeptide hormones or the two "
                       "tyrosine-derived hormones.",
      ncert="Class 11 Biology, 'Chemical Coordination and Integration', mechanism of hormone action (classes of "
            "hormones)", seconds=35),

    Q(T_BM, "Carbohydrates", "Basic", "direct",
      "Cellulose is a straight-chain polysaccharide made only of β-D-glucose units. It is the predominant "
      "constituent of:",
      ["The liver and muscles of animals", "Cane sugar", "Milk", "The cell wall of plant cells"], "D",
      "Occurrence of cellulose",
      "Cellulose occurs exclusively in plants and is the most abundant organic substance in the plant kingdom; it "
      "is the main constituent of plant cell walls. Glycogen (not cellulose) is stored in animal liver and muscle.",
      ["Cellulose → plant cell walls", "Glycogen → animal liver, muscle and brain"],
      why_others_wrong="Liver and muscle store glycogen; cane sugar is sucrose; milk sugar is lactose.",
      ncert=f"{NC12}, 'Biomolecules', polysaccharides (cellulose)", seconds=20),

    N(T_BM, "Nucleic acids", "Intermediate",
      "A double-stranded DNA segment has 100 base pairs, of which 30 are A–T pairs and the rest are G–C pairs. An "
      "A–T pair is held by two hydrogen bonds and a G–C pair by three. The total number of hydrogen bonds between "
      "the two strands of this segment is:",
      ["230", "250", "200", "270"], "D", v_1484,
      "Complementary base pairing in DNA",
      "Adenine pairs with thymine and guanine with cytosine. The number of G–C pairs is 100 − 30 = 70.",
      ["A–T: 30 × 2 = 60", "G–C: 70 × 3 = 210", "Total = 270"],
      why_others_wrong="230 swaps the hydrogen-bond numbers of the two pairs; 200 gives every pair two bonds; 250 "
                       "averages them.",
      ncert="Class 12 Biology, 'Molecular Basis of Inheritance', structure of polynucleotide chain; "
            f"{NC12}, 'Biomolecules', nucleic acids", seconds=45),

    N(T_BM, "Carbohydrates", "Intermediate",
      "Amylose is a linear polymer of α-D-glucose, represented as (C₆H₁₀O₅)ₙ. A sample of amylose has a molar mass of "
      "81000 g mol⁻¹. Ignoring the end groups, the number of glucose units in each chain is (C = 12, H = 1, O = 16):",
      ["450", "500", "1000", "250"], "B", v_1485,
      "Repeating unit of polysaccharides",
      "Each glucose unit in the chain has lost one molecule of water in forming the glycosidic links, so the "
      "repeating unit is C₆H₁₀O₅ (162 g mol⁻¹), not C₆H₁₂O₆ (180 g mol⁻¹).",
      ["M(C₆H₁₀O₅) = 72 + 10 + 80 = 162 g mol⁻¹", "n = 81000/162 = 500"],
      why_others_wrong="450 divides by 180 (glucose itself); 1000 and 250 are off by a factor of two.",
      ncert=f"{NC12}, 'Biomolecules', polysaccharides (starch: amylose)", seconds=45),

    Q(T_BM, "Carbohydrates", "Intermediate", "assertion_reason",
      *ar("A sucrose solution that has been boiled with dilute acid gives a red precipitate with Fehling's solution, "
          "although sucrose itself does not.", True,
          "Acid hydrolysis of sucrose gives glucose and fructose, both of which are reducing sugars.", True,
          explains=True),
      "Hydrolysis of a non-reducing sugar",
      "In sucrose the reducing groups of glucose (C1) and fructose (C2) are tied up in the glycosidic bond, so it does "
      "not reduce Fehling's solution. Hydrolysis frees these groups: glucose and fructose are both reducing sugars "
      "and give red Cu₂O. R explains A.",
      ["Sucrose: non-reducing", "Sucrose + H₂O (H⁺) → glucose + fructose", "Both reduce Fehling's solution → R "
       "explains A"],
      ncert=f"{NC12}, 'Biomolecules', disaccharides (sucrose)", seconds=40),

    Q(T_BM, "Nucleic acids", "Intermediate", "multi_statement",
      *ms("Which of the following statements about nucleic acids are correct?",
          [("DNA is responsible for maintaining the identity of different species of organisms over millions of "
            "years.", True),
           ("Proteins are synthesised by RNA molecules in the cell, but the message for the synthesis of a "
            "particular protein is present in DNA.", True),
           ("In RNA, thymine takes the place of uracil.", False),
           ("Nucleotides are joined to one another by peptide bonds.", False),
           ("Nucleic acids are long-chain polymers of nucleotides, so they are also called polynucleotides.", True)],
          [["a", "b", "c"], ["b", "d", "e"], ["a", "c", "e"]], "C"),
      "Structure and biological functions of nucleic acids",
      "DNA is the chemical basis of heredity and carries the message for protein synthesis, which is carried out by "
      "the different RNAs. RNA contains uracil in place of thymine (not the reverse). Nucleotides are linked by "
      "phosphodiester bonds; peptide bonds join amino acids. Nucleic acids are polynucleotides.",
      ["(a) true", "(b) true", "(c) reversed → false", "(d) phosphodiester, not peptide → false", "(e) true"],
      why_others_wrong="The other options include (c) or (d), both false.",
      ncert=f"{NC12}, 'Biomolecules', nucleic acids (biological functions)", seconds=50),

    Q(T_BM, "Carbohydrates", "Advanced", "multi_statement",
      *ms("Which of the following statements about the evidence for the structure of glucose are correct?",
          [("Prolonged heating with HI gives n-hexane, showing that the six carbon atoms are linked in a straight "
            "chain.", True),
           ("Oxidation with bromine water to gluconic acid shows that the carbonyl group of glucose is a ketone "
            "group.", False),
           ("Glucose and gluconic acid are both oxidised by nitric acid to saccharic acid, which shows that "
            "glucose contains a primary alcohol (–CH₂OH) group.", True),
           ("Formation of a cyanohydrin with HCN shows that glucose contains a primary alcohol group.", False),
           ("The six-membered cyclic form of glucose is called the pyranose structure, by analogy with pyran.",
            True)],
          [["a", "b", "c"], ["c", "d", "e"], ["a", "b", "e"]], "B"),
      "Reactions used to establish the structure of glucose",
      "HI reduction to n-hexane shows a straight chain. HCN addition and oxime formation show a carbonyl group. "
      "Oxidation by a mild agent (bromine water) to a six-carbon acid shows that the carbonyl group is an aldehyde. "
      "Oxidation of both glucose and gluconic acid to saccharic acid shows a primary alcohol group. The cyclic "
      "six-membered form is called pyranose (like pyran).",
      ["(a) true", "(b) shows an aldehyde → false", "(c) true", "(d) shows a carbonyl group → false", "(e) true"],
      why_others_wrong="The other options include (b) or (d), both false.",
      ncert=f"{NC12}, 'Biomolecules', glucose: structure", seconds=75),

    Q(T_BM, "Carbohydrates", "Advanced", "statement_pair",
      *sp("Maltose is a reducing sugar because, in solution, a free aldehyde group can be produced at C1 of its "
          "second glucose unit.", True,
          "Lactose is a non-reducing sugar because the reducing groups of both its monosaccharide units are used in "
          "the glycosidic bond.", False),
      "Reducing and non-reducing disaccharides",
      "In maltose, C1 of one α-D-glucose is linked to C4 of the other; C1 of the second unit is free and can open "
      "to an aldehyde, so maltose is reducing. In lactose, C1 of β-D-galactose is linked to C4 of β-D-glucose; C1 of "
      "the glucose unit is free, so lactose is also a reducing sugar. Only sucrose, among these, has both reducing "
      "groups tied up.",
      ["I: true", "II: lactose has a free C1 on its glucose unit → reducing → false"],
      ncert=f"{NC12}, 'Biomolecules', disaccharides (maltose and lactose)", seconds=50),

    Q(T_BM, "Amino acids and proteins", "Advanced", "assertion_reason",
      *ar("Amino acids are colourless, crystalline solids with high melting points and are soluble in water, unlike "
          "simple amines and carboxylic acids of similar molecular mass.", True,
          "In aqueous solution and in the solid, amino acids exist as dipolar ions (zwitterions), which give them a "
          "salt-like character.", True, explains=True),
      "Zwitterion and the physical properties of amino acids",
      "The –COOH group loses a proton and the –NH₂ group gains one, giving H₃N⁺–CHR–COO⁻. Strong electrostatic "
      "attractions between these dipolar ions make amino acids behave like salts: high melting points and "
      "solubility in water. NCERT links the high melting points directly to this dipolar, salt-like character. "
      "R explains A.",
      ["Zwitterion: –NH₃⁺ and –COO⁻ in the same molecule", "Ionic (salt-like) attractions → high m.p., water soluble",
       "R explains A"],
      ncert=f"{NC12}, 'Biomolecules', amino acids (zwitterion)", seconds=45),
]

# ================================================================ Principles Related to Practical Chemistry (1491-1500)
# 1491: potash alum K2SO4.Al2(SO4)3.24H2O
m_alum = mm(K=2, S=4, O=16, Al=2) + 24 * 18
assert m_alum == 948
v_1491 = pct(F(24 * 18, m_alum))
assert v_1491 == "45.6%" and pct(1 - F(24 * 18, m_alum)) == "54.4%" and pct(F(18, m_alum)) == "1.9%"
# 1495: 200 mL 0.10 M HCl + 100 mL 0.10 M NaOH ; dH = -57.1 kJ/mol ; NaOH limiting (0.010 mol)
n_1495 = min(F(2, 10) * F(1, 10), F(1, 10) * F(1, 10))
assert n_1495 == F(1, 100)
v_1495 = f"{float(n_1495 * 57100):.0f} J"
assert v_1495 == "571 J" and f"{float(F(2, 100) * 57100):.0f} J" == "1142 J"
# 1496: Na2S2O3 + 2HCl -> 2NaCl + SO2 + S + H2O ; 50.0 mL of 0.10 M
v_1496 = g(F(50, 1000) * F(1, 10) * S_, 2)
assert v_1496 == "0.16 g"
# 1498: FeC2O4 (144) gives 3 e- (Fe2+ -> Fe3+: 1, C2O4 2- -> 2CO2: 2); MnO4- takes 5 e-
m_feox = FE + mm(C=2, O=4)
assert m_feox == 144
e_mno4 = F(30, 1000) * F(2, 100) * 5
n_1498 = e_mno4 / 3
v_1498 = g(n_1498 * m_feox, 3)
assert v_1498 == "0.144 g" and g(e_mno4 / 2 * m_feox, 3) == "0.216 g" and g(e_mno4 / 1 * m_feox, 3) == "0.432 g"

QUESTIONS += [
    N(T_PR, "Preparations", "Basic",
      "Potash alum, K₂SO₄·Al₂(SO₄)₃·24H₂O, is prepared in the laboratory from potassium sulphate and aluminium "
      "sulphate. The percentage by mass of water of crystallisation in potash alum is (K = 39, Al = 27, S = 32, "
      "O = 16, H = 1):",
      ["45.6%", "54.4%", "22.8%", "1.9%"], "A", v_1491,
      "Composition of a double salt",
      "Molar mass = 2(39) + 2(27) + 4(32) + 16(16) + 24(18) = 78 + 54 + 128 + 256 + 432 = 948 g mol⁻¹, of which "
      "432 g is water.",
      ["M = 948 g mol⁻¹", "Water = 24 × 18 = 432 g", "% water = 432/948 × 100 = 45.6%"],
      why_others_wrong="54.4% is the anhydrous part; 22.8% halves the water; 1.9% counts only one water molecule.",
      ncert=f"{LAB}, preparation of potash alum", seconds=50),

    Q(T_PR, "Qualitative salt analysis", "Basic", "direct",
      "In the analysis of group V cations, the solution is treated with ammonium oxalate solution, and a white "
      "precipitate is obtained. This confirms the presence of:",
      ["Cu²⁺", "Ca²⁺", "Fe³⁺", "NH₄⁺"], "B",
      "Confirmatory test for calcium ions",
      "Ca²⁺ ions form a white precipitate of calcium oxalate with ammonium oxalate. Calcium also gives a brick-red "
      "flame.",
      ["Ca²⁺ + C₂O₄²⁻ → CaC₂O₄ (white precipitate)"],
      why_others_wrong="Cu²⁺ (group II) and Fe³⁺ (group III) are removed long before group V; NH₄⁺ is tested "
                       "separately with NaOH and Nessler's reagent.",
      ncert=f"{LAB}, systematic analysis of cations (group V)", seconds=25),

    Q(T_PR, "Detection of elements and functional groups", "Basic", "direct",
      "An organic compound is heated with phthalic anhydride and a few drops of concentrated H₂SO₄, and the melt is "
      "poured into dilute NaOH solution. A pink (red) colour appears. This phthalein dye test shows the presence of:",
      ["An aldehyde group", "A carboxyl group", "A primary amino group", "A phenolic –OH group"], "D",
      "Phthalein dye test",
      "Phenols condense with phthalic anhydride in the presence of concentrated H₂SO₄ to give phenolphthalein (from "
      "phenol), which is pink to red in alkaline solution.",
      ["Phenol + phthalic anhydride (conc. H₂SO₄) → phenolphthalein", "Pink in NaOH → phenolic –OH"],
      why_others_wrong="Aldehydes are detected with Tollens' or Fehling's reagent, carboxyl groups with NaHCO₃, and "
                       "primary aromatic amines with the azo dye test.",
      ncert=f"{LAB}, tests for functional groups (phenolic group)", seconds=30),

    Q(T_PR, "Titrimetric analysis", "Intermediate", "direct",
      "In the titration of oxalic acid with KMnO₄ the flask is warmed to 50–60 °C, but in the titration of Mohr's "
      "salt with KMnO₄ the solution is NOT heated. This is because, on heating, the Mohr's salt solution:",
      ["would decolourise KMnO₄ too slowly", "would lose its ammonium ions as ammonia",
       "would have its Fe²⁺ ions oxidised by atmospheric oxygen", "would precipitate iron(III) hydroxide only in "
       "the presence of excess acid"], "C",
      "Conditions of redox titrations",
      "The oxalate reaction is slow at room temperature, so it is warmed. Fe²⁺ reacts quickly with MnO₄⁻ at room "
      "temperature, and heating would only allow some Fe²⁺ to be oxidised by air to Fe³⁺, giving a low titre.",
      ["Oxalic acid: slow reaction → warm", "Mohr's salt: fast reaction; heating → Fe²⁺ oxidised by air → avoid"],
      why_others_wrong="The Fe²⁺–MnO₄⁻ reaction is already fast; ammonium ions do not interfere in acid solution; "
                       "the last option has no basis.",
      ncert=f"{LAB}, titrimetric analysis (Mohr's salt against KMnO₄)", seconds=40),

    N(T_PR, "Thermochemistry and kinetics experiments", "Intermediate",
      "200 mL of 0.10 M HCl is mixed with 100 mL of 0.10 M NaOH. Taking the enthalpy of neutralisation of a strong "
      "acid by a strong base as −57.1 kJ mol⁻¹, the heat evolved is:",
      ["1142 J", "571 J", "1713 J", "285 J"], "B", v_1495,
      "Heat of neutralisation with a limiting reagent",
      "Heat is released only for the moles of water formed, which equal the moles of the limiting reagent. "
      "HCl = 0.020 mol and NaOH = 0.010 mol, so NaOH is limiting.",
      ["n(HCl) = 0.020 mol, n(NaOH) = 0.010 mol", "Water formed = 0.010 mol",
       "q = 0.010 × 57.1 kJ = 0.571 kJ = 571 J"],
      why_others_wrong="1142 J uses the moles of HCl; 1713 J adds the moles of acid and base; 285 J halves the "
                       "correct value.",
      ncert=f"{LAB}, thermochemistry: enthalpy of neutralisation", seconds=50),

    N(T_PR, "Thermochemistry and kinetics experiments", "Intermediate",
      "In the kinetic study of the reaction Na₂S₂O₃ + 2HCl → 2NaCl + SO₂ + S + H₂O, 50.0 mL of 0.10 M sodium "
      "thiosulphate reacts completely with excess HCl. The mass of sulphur precipitated is (S = 32):",
      ["0.32 g", "0.08 g", "0.24 g", "0.16 g"], "D", v_1496,
      "Stoichiometry of the thiosulphate–acid reaction",
      "Each thiosulphate ion gives one atom of colloidal sulphur (the other sulphur appears as SO₂).",
      ["n(S₂O₃²⁻) = 0.10 × 0.050 = 0.0050 mol", "n(S) = 0.0050 mol", "Mass = 0.0050 × 32 = 0.16 g"],
      why_others_wrong="0.32 g counts both sulphur atoms as precipitated; 0.08 g halves the answer; 0.24 g has no "
                       "basis in the equation.",
      ncert=f"{LAB}, chemical kinetics: reaction of sodium thiosulphate with hydrochloric acid", seconds=40),

    Q(T_PR, "Qualitative salt analysis", "Intermediate", "match_list",
      *ml("Match the cation in List-I (with the reagent used) with the observation in List-II.",
          ["Fe³⁺ with potassium hexacyanidoferrate(II)", "Cu²⁺ with potassium hexacyanidoferrate(II) (acetic acid)",
           "Ba²⁺ with potassium chromate", "Zn²⁺ with sodium hydroxide solution"],
          ["Yellow precipitate", "White precipitate that dissolves in excess of the reagent",
           "Prussian blue precipitate", "Chocolate-brown precipitate"],
          "III IV I II", ["IV III I II", "III IV II I", "III I IV II"], "B"),
      "Confirmatory tests for cations",
      "Fe³⁺ gives Prussian blue (iron(III) hexacyanidoferrate(II)) with potassium ferrocyanide; Cu²⁺ gives a "
      "chocolate-brown precipitate of Cu₂[Fe(CN)₆]; Ba²⁺ gives yellow BaCrO₄; Zn²⁺ gives white Zn(OH)₂ that "
      "dissolves in excess NaOH as zincate.",
      ["A → Prussian blue (III)", "B → chocolate brown (IV)", "C → yellow (I)", "D → white, soluble in excess (II)"],
      why_others_wrong="The other codes swap the two ferrocyanide precipitates or the chromate and hydroxide tests.",
      ncert=f"{LAB}, confirmatory tests for cations", seconds=45),

    N(T_PR, "Titrimetric analysis", "Advanced",
      "Iron(II) oxalate, FeC₂O₄ (molar mass 144 g mol⁻¹), is titrated with acidified KMnO₄. Both the Fe²⁺ ion and "
      "the oxalate ion are oxidised (to Fe³⁺ and CO₂). If a sample needs 30.0 mL of 0.020 M KMnO₄, the mass of "
      "FeC₂O₄ in the sample is:",
      ["0.216 g", "0.432 g", "0.0864 g", "0.144 g"], "D", v_1498,
      "Redox titration when both ions of a salt are oxidised",
      "MnO₄⁻ gains 5 electrons (Mn +7 → +2). Each FeC₂O₄ loses 3 electrons: one from Fe²⁺ → Fe³⁺ and two from "
      "C₂O₄²⁻ → 2CO₂.",
      ["Electrons accepted = 0.030 × 0.020 × 5 = 3.0 × 10⁻³ mol", "n(FeC₂O₄) = 3.0 × 10⁻³ / 3 = 1.0 × 10⁻³ mol",
       "Mass = 1.0 × 10⁻³ × 144 = 0.144 g"],
      why_others_wrong="0.216 g counts only the oxalate (2 e⁻); 0.432 g counts only Fe²⁺ (1 e⁻); 0.0864 g takes "
                       "5 e⁻ per FeC₂O₄.",
      ncert=f"{LAB}, titrimetric analysis with KMnO₄ (oxalate and Fe²⁺)", seconds=100),

    Q(T_PR, "Titrimetric analysis", "Advanced", "multi_statement",
      *ms("Which of the following statements about titrations with potassium permanganate are correct?",
          [("The end point is the first permanent light pink colour of the solution.", True),
           ("Dilute HCl is suitable for acidifying the solution.", False),
           ("Oxalic acid dihydrate can be used as a primary standard.", True),
           ("Phenolphthalein is added as the indicator.", False),
           ("In the titration of oxalic acid, decolourisation is slow at first and becomes rapid as the Mn²⁺ ions "
            "formed catalyse the reaction.", True)],
          [["a", "b", "c"], ["c", "d", "e"], ["a", "c", "d"]], "B"),
      "Practical points in permanganate titrations",
      "KMnO₄ acts as its own indicator: the first excess drop gives a permanent light pink colour. Dilute H₂SO₄ is "
      "used because HCl would itself be oxidised by permanganate (to chlorine), giving a high titre. Oxalic acid "
      "dihydrate is a stable, pure crystalline solid and serves as a primary standard. Mn²⁺ ions formed in the "
      "reaction catalyse it (autocatalysis).",
      ["(a) true", "(b) HCl is oxidised by KMnO₄ → false", "(c) true", "(d) no external indicator → false",
       "(e) autocatalysis by Mn²⁺ → true"],
      why_others_wrong="The other options include (b) or (d), both false.",
      ncert=f"{LAB}, titrimetric analysis (redox titrations)", seconds=60),

    Q(T_PR, "Thermochemistry and kinetics experiments", "Advanced", "assertion_reason",
      *ar("The enthalpy of neutralisation of any strong acid by any strong base in dilute solution is nearly the "
          "same, about −57 kJ mol⁻¹.", True,
          "In dilute solution strong acids and strong bases are completely ionised, so the only reaction in every "
          "case is H⁺(aq) + OH⁻(aq) → H₂O(l).", True, explains=True),
      "Constancy of the enthalpy of neutralisation",
      "Because strong acids, strong bases and their salts are fully ionised, the other ions are spectators. The net "
      "change is always the formation of one mole of water from H⁺ and OH⁻, so the enthalpy change is the same. R "
      "explains A.",
      ["Complete ionisation → spectator ions", "Net: H⁺ + OH⁻ → H₂O in every case", "R explains A"],
      ncert=f"{LAB}, thermochemistry: enthalpy of neutralisation", seconds=40),
]

# ---------------------------------------------------------------- package checks and output
PLAN = {T_CC: (5, 6, 5), T_PU: (2, 3, 2), T_GO: (6, 8, 6), T_HC: (5, 6, 5), T_HX: (3, 4, 3), T_OX: (6, 8, 6),
        T_NI: (3, 4, 3), T_BM: (3, 4, 3), T_PR: (3, 4, 3)}
TOTAL = LAST - FIRST + 1

if __name__ == "__main__":
    assert len(QUESTIONS) == TOTAL == 119, len(QUESTIONS)
    assert [x["question_id"] for x in QUESTIONS] == [f"NEET_CHE_{n:06d}" for n in range(FIRST, LAST + 1)]
    have = Counter((x["topic"], x["difficulty"]) for x in QUESTIONS)
    for topic, quota in PLAN.items():
        for diff, n in zip(("Basic", "Intermediate", "Advanced"), quota):
            assert have[(topic, diff)] == n, (topic, diff, have[(topic, diff)], n)
    keys = Counter(x["correct_answer"] for x in QUESTIONS)
    fmts = Counter(x["format"] for x in QUESTIONS)
    print("keys", dict(sorted(keys.items())), "formats", dict(fmts))
    assert all(27 <= keys[k] <= 33 for k in LETTERS), keys
    assert 0.27 <= fmts["numerical"] / TOTAL <= 0.33, fmts
    assert all(fmts[f] / TOTAL >= 0.08 for f in fmts if f != "numerical") and len(fmts) == 6, fmts
    for x in QUESTIONS:  # every numerical answer is recomputed above
        assert (x["format"] == "numerical") == ("script:recompute" in x["verification"]["verified_by"]), x["question_id"]
    doc = {"schema_version": "1.0", "batch_id": "BATCH_006", "created_at": TODAY,
           "notes": "Package CHE_006_p2: 119 original Chemistry questions (coordination compounds, organic chemistry, "
                    "biomolecules, practical chemistry). Numerical answers recomputed by "
                    "tools/batch_006/CHE_006_p2.py.",
           "stimuli": [], "questions": QUESTIONS}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {OUT}: {dict(Counter(x['difficulty'] for x in QUESTIONS))}, keys {dict(sorted(keys.items()))}, "
          f"formats {dict(fmts)}")
